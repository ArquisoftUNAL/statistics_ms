import aio_pika
import logging
import json
from sqlalchemy.engine import Engine
from motor.motor_asyncio import AsyncIOMotorClient
from app.repositories.habits_repository import HabitRepository
from app.repositories.statistics_repository import StatisticsRepository
from app.services.update_report.update_report import UpdateReport
from app.models.queue_msgs import NewHabitData
from app.services.send_streak.send_streak_to_archivements import (
    send_streak_to_archivements,
)
from app.exceptions.exceptions import GraphqlMutationError


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

    async def disconnect(self):
        await self.connection.close()

    async def callback(self, message: aio_pika.IncomingMessage):
        try:
            async with message.process(requeue=True):
                msg_data = json.loads(message.body.decode())
                new_hab_data = NewHabitData(**msg_data)
                print("new_hab_data: ", new_hab_data)
                report_doc = await UpdateReport(
                    self.hab_repo, self.stat_repo
                ).update_habit_report(new_hab_data)

        except Exception as e:
            logging.error(f"Error processing message: {e}")

        else:
            try:
                await send_streak_to_archivements(report_doc)
            except GraphqlMutationError as e:
                logging.error(f"Error sending streak to archivements: {e}")

    async def start_consuming(self):
        queue = await self.channel.declare_queue(self.queue, durable=True)
        # await self.channel.set_qos(prefetch_count=1)
        await queue.consume(self.callback)
