import aio_pika
import logging
from app.repositories.habits_repository import HabitRepository
from app.services.habit_report import HabitReport
from app.exceptions.exceptions import HabitNotFoundError
from app.models.incom_msgs import NewHabitData
from app.graphql.mutations import UpDateStreak, UpDateStreakMutation, Streak
from app.graphql.graphql_client import GraphQLClient

class RabbitMQClient:
    def __init__(self, url: str, queue: str, sql_engine):
        self.url = url
        self.queue = queue
        self.connection = None
        self.channel = None
        self.repo = HabitRepository(sql_engine)
        self.habit_report = HabitReport(self.repo)

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
                new_hab_data = NewHabitData.from_json(message.body.decode())

                session_maker = self.repo.sessionmaker()
                with session_maker() as session:
                    hab = await self.repo.get_hab(new_hab_data.hab_id, session)
                    if hab is None:
                        raise HabitNotFoundError("Habit not found")
                    if hab.hab_is_yn:
                        streak = await self.habit_report.get_habit_yn_streaks(hab_id=new_hab_data.hab_id)
                    else:
                        streak = await self.habit_report.get_habit_ms_streaks(hab_id=new_hab_data.hab_id)

                    from datetime import datetime

                latest_date_range = max(streak.data.keys(), key=lambda x: datetime.strptime(x[1], '%Y-%m-%d'))

                latest_quantity = streak.data[latest_date_range]

                new_streak = Streak(
                    date_start=latest_date_range[0],
                    date_end=latest_date_range[1],
                    data=latest_quantity
                )

                update_streak = UpDateStreak(
                    freq_type=hab.hab_freq_type,
                    hab_id=new_hab_data.hab_id,
                    streak=new_streak
                )

                mutation = UpDateStreakMutation(update_streak).get_mutation()

                grapql_client = GraphQLClient()

                await grapql_client.execute(*mutation)

            except Exception as e:
                await message.reject(requeue=True)
                logging.error(f"Error processing message: {e}")

            await message.ack()

    async def start_consuming(self):
        queue = await self.channel.declare_queue(self.queue, durable=True)
        await queue.consume(self.callback)
