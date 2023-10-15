import aio_pika
import logging
from sqlalchemy.engine import Engine
from motor.motor_asyncio import AsyncIOMotorClient
from app.repositories.habits_repository import HabitRepository
from app.repositories.statistics_repository import StatisticsRepository
from app.services.update_report.update_report import UpdateReport
from app.exceptions.exceptions import HabitNotFoundError
from app.models.queue_msgs import NewHabitData
from app.graphql.mutations import UpDateStreak, UpDateStreakMutation, Streak
from app.graphql.graphql_client import GraphQLClient


class RabbitMQClient:
    def __init__(
        self, url: str, queue: str, sql_engine: Engine, mongo_client: AsyncIOMotorClient
    ):
        self.url = url
        self.queue = queue
        self.connection = None
        self.channel = None
        self.hab_repo = HabitRepository(sql_engine)
        self.stat_repo = StatisticsRepository(mongo_client)

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)
        await self.channel.declare_queue(self.queue, durable=True)
        print("Connected to RabbitMQ")

    async def disconnect(self):
        await self.connection.close()

    async def callback(self, message: aio_pika.IncomingMessage):
        print("On callback...")
        async with message.process():
            # Lógica para manejar mensajes
            try:
                raise HabitNotFoundError

            except Exception as e:
                await message.nack(requeue=True)
                logging.error(f"Error processing message: {e}")

            await message.ack()

    async def start_consuming(self):
        queue = await self.channel.declare_queue(self.queue, durable=True)
        await queue.consume(self.callback)
