""" a class to read from postgresql database using sqlalchemy"""
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from app.exceptions.exceptions import AppConnectionError, AppDatabaseError, HabitNotFoundError
from uuid import UUID
import logging
import pandas as pd
import app.models.repo_models as rm

class HabitRepository:
    def __init__(self, engine: Engine):
        self.logger = logging.getLogger(__name__)
        self.engine = engine
        self.sessionmaker = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)

    async def get_hab(self, hab_id: UUID, session: AsyncSession) -> rm.Hab:
        query = text("""
                     SELECT hab_is_yn, hab_freq_type, hab_goal
                     FROM habit 
                     WHERE hab_id = :hab_id
                     """)
        result = await session.execute(query, {"hab_id": hab_id})
        data = result.fetchone()

        if data is not None:
            return rm.Hab(
                hab_is_yn=data[0],
                hab_freq_type=data[1],
                hab_goal=data[2],
            )
        return data

    async def get_habit_data(self, hab_id: UUID) -> rm.HabData:
        try:
            async with self.sessionmaker() as session:
                hab = await self.get_hab(hab_id, session)

                if hab is None:
                    raise HabitNotFoundError("Habit not found")

                query = text("""
                             SELECT hab_dat_amount, hab_dat_collected_at
                             FROM habit_data_collected
                             WHERE hab_id = :hab_id
                             ORDER BY hab_dat_collected_at DESC
                            """)
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

                return rm.HabData(hab=hab, data=data)
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
        