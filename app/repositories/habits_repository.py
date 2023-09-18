""" a class to read from postgresql database using sqlalchemy"""
from sqlalchemy import MetaData, Table, select
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
        self.metadata = MetaData()

        self.cat = Table('Category', self.metadata, autoload=True)
        self.hab = Table('Habit', self.metadata, autoload=True)
        self.hab_rec = Table('Habit_Recurrency', self.metadata, autoload=True)
        self.hab_data = Table('Habit_data_Collected', self.metadata, autoload=True)
    
    async def get_hab_is_yn(self, hab_id: UUID, session: AsyncSession):
        query = select([
            self.hab.c.hab_is_yn,
        ]).select_from(
            self.hab
        ).where(
            self.hab.c.hab_id == hab_id
        )

        result = await session.execute(query)
        return result.scalar()
    
    async def get_hab_rec(self, hab_id: UUID, session: AsyncSession) -> rm.HabRec:
        query = select([
            self.hab_rec.c.hab_rec_id,
            self.hab_rec.c.hab_rec_freq_type,
            self.hab_rec.c.hab_rec_goal,
        ]).select_from(
            self.hab_rec
        ).where(
            self.hab_rec.c.hab_id == hab_id
        )

        result = await session.execute(query)
        data = result.fetchone()

        if data is not None:
            return rm.HabRec(
                hab_rec_id=data[0],
                hab_rec_freq_type=data[1],
                hab_rec_goal=data[2],
            )
        return data
        
    async def get_habit_data(self, hab_id: UUID) -> rm.HabData:
        try:
            async with self.sessionmaker() as session:
                #is_yn = await self.get_hab_is_yn(hab_id)
                hab_rec = await self.get_hab_rec(hab_id, session)
                
                if hab_rec is None:
                    raise HabitNotFoundError("Habit not found")
                
                query = select([
                    self.hab_data.c.hab_dat_id,
                    self.hab_data.c.hab_dat_amount,
                    self.hab_data.c.hab_dat_collected_at,
                ]).select_from(
                    self.hab_data
                ).where(
                    self.hab.c.hab_rec_id == hab_rec[0]
                ).order_by(self.hab_data.c.hab_dat_collected_at.desc())

                response = await session.execute(query).fetchall()
                data = pd.DataFrame(response, columns=response[0].keys())

                if data.empty:
                    return None
                data['hab_dat_collected_at'] = pd.to_datetime(data['hab_dat_collected_at'])
                data['hab_dat_amount'] = data['hab_dat_amount'].astype(float)
                data[['year', 'week', 'weekday']] = data['hab_dat_collected_at'].apply(lambda x: pd.Series(x.isocalendar()))
                data['month'] = data['hab_dat_collected_at'].apply(lambda x: x.month)

                return rm.HabData(hab_rec=hab_rec, data=data)
        except OperationalError as e:
            self.logger.error(str(e))
            raise AppConnectionError("Connection to database failed") from e
        except SQLAlchemyError as e:
            self.logger.error(str(e))
            raise AppDatabaseError("Database error") from e
            
