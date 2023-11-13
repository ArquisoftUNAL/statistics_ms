from sqlalchemy.ext.asyncio import create_async_engine
from . import functions as fn
from app.repositories.habits_repository import HabitRepository
from app.common.constants import HABITS_DB_URL

async def get_data(id: str):
    hab_rep = HabitRepository(await create_async_engine(HABITS_DB_URL))
    habit_data = await hab_rep.get_habit_data(id)

    return habit_data

async def test_get_habit_yn_streaks(id: str, freq: int):
    habit_data = await get_data(id)
    streak = fn.yn_streaks(df=habit_data.data, freq=freq)

    return streak

streak = test_get_habit_yn_streaks(id="001e0baf-3810-4ab8-b561-6f60fe0af84b", freq=1)

print(streak)