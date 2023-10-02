import pika
import logging
from pika.adapters.asyncio_connection import AsyncioConnection

class RabbitMQClient:
    def __init__(self, host: str, queue: str, username: str, password: str):
        self.host = host
        self.queue = queue
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    async def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        self.connection = AsyncioConnection(pika.ConnectionParameters(host=self.host, credentials=credentials))
        self.channel = await self.connection.channel()
        await self.channel.queue_declare(queue=self.queue)

    async def disconnect(self):
        await self.connection.close()

    async def callback(self, ch, method, properties, body):
        #Logic for handling messages
        try:
            "Procesamiento del mensaje"
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    async def start_consuming(self):
        await self.channel.basic_qos(prefetch_count=1)
        await self.channel.basic_consume(self.queue, self.callback, auto_ack=False)
        await self.channel.start_consuming()