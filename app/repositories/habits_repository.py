""" a class to read from postgresql database using sqlalchemy"""
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from app.exceptions.exceptions import AppConnectionError, AppDatabaseError, HabitNotFoundError
from app.models.habits_db_models import Hab, HabData
from .interfaces.habits_repository_interface import AbstractHabitReposiory
from app.queries.habits_queries import GET_HAB_QUERY, GET_HABIT_DATA_QUERY
from uuid import UUID
import logging
import pandas as pd

class HabitRepository(AbstractHabitReposiory):
    def __init__(self, engine: Engine):
        self.logger = logging.getLogger(__name__)
        self.engine = engine
        self.sessionmaker = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)

    async def get_hab(self, hab_id: UUID, session: AsyncSession) -> Hab:
        query = text(GET_HAB_QUERY)
        result = await session.execute(query, {"hab_id": hab_id})
        data = result.fetchone()

        if data is not None:
            return Hab(
                hab_is_yn=data[0],
                hab_freq_type=data[1],
                hab_goal=data[2],
            )
        return data

    async def get_habit_data(self, hab_id: UUID) -> HabData:
        try:
            async with self.sessionmaker() as session:
                hab = await self.get_hab(hab_id, session)

                if hab is None:
                    raise HabitNotFoundError("Habit not found")

                query = text(GET_HAB_QUERY)
                result = await session.execute(query, {"hab_id": hab_id})

                await session.commit()

                response = result.fetchall()
                data = pd.DataFrame(response)

                if data.empty:
                    return None
                data['hab_dat_collected_at'] = pd.to_datetime(data['hab_dat_collected_at']).dt.date
                data['hab_dat_amount'] = data['hab_dat_amount'].astype(float)
                data[['year', 'week', 'weekday']] = data['hab_dat_collected_at'].apply(lambda x: pd.Series(x.isocalendar()))
                data['month'] = data['hab_dat_collected_at'].apply(lambda x: x.month)

                return HabData(hab=hab, data=data)
        except OperationalError as e:
            self.logger.error(str(e))
            raise AppConnectionError("Connection to database failed") from e
        except SQLAlchemyError as e:
            self.logger.error(str(e))
            raise AppDatabaseError("Database error") from e
        except Exception as e:
            self.logger.error(str(e))
            raise AppDatabaseError("Database error") from e
        finally:
            await session.close()
            logging.info("Session closed")
        