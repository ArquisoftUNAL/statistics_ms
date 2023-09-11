""" a class to read from postgresql database using sqlalchemy"""
from sqlalchemy import create_engine, URL, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pandas as pd
import asyncio
import os
import app.models.repo_models as rm

load_dotenv()
url = URL.create(
    drivername="postgresql",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
)

class HabitRepository:
    def __init__(self):
        self.engine = create_engine(url)
        self.session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()

        self.cat = Table('Category', self.metadata, autoload=True)
        self.hab = Table('Habit', self.metadata, autoload=True)
        self.hab_rec = Table('Habit_Recurrency', self.metadata, autoload=True)
        self.hab_data = Table('Habit_data_Collected', self.metadata, autoload=True)
    
    async def get_hab_is_yn(self, hab_id):
        query = select([
            self.hab.c.hab_is_yn,
        ]).select_from(
            self.hab
        ).where(
            self.hab.c.hab_id == hab_id
        )

        result = await asyncio.get_event_loop().run_in_executor(None, self.engine.execute, query)
        return result.scalar()
    
    async def get_hab_rec(self, hab_id) -> rm.HabRec:
        query = select([
            self.hab_rec.c.hab_rec_id,
            self.hab_rec.c.hab_rec_freq_type,
            self.hab_rec.c.hab_rec_goal,
        ]).select_from(
            self.hab.rec
        ).where(
            self.hab_rec.c.hab_id == hab_id
        )

        result = await asyncio.get_event_loop().run_in_executor(None, self.engine.execute, query)
        data = result.fetchone()

        if data is not None:
            return rm.HabRec(
                hab_rec_id=data[0],
                hab_rec_freq_type=data[1],
                hab_rec_goal=data[2],
            )
        return data
        
    async def get_habit_data(self, hab_id) -> rm.HabData:
        #is_yn = await self.get_hab_is_yn(hab_id)
        hab_rec = await self.get_hab_rec(hab_id)
        
        if hab_rec is None:
            return None
        
        query = select([
            self.hab_data.c.hab_dat_id,
            self.hab_data.c.hab_dat_amount,
            self.hab_data.c.hab_dat_collected_at,
        ]).select_from(
            self.hab_data
        ).where(
            self.hab.c.hab_rec_id == hab_rec[0]
        ).order_by(self.hab_data.c.hab_dat_collected_at.desc())

        response = await asyncio.get_event_loop().run_in_executor(None, pd.read_sql, query, self.engine)
        if response.empty:
            return None
        response['hab_dat_collected_at'] = pd.to_datetime(response['hab_dat_collected_at'])
        response[['year', 'week', 'weekday']] = response['hab_dat_collected_at'].apply(lambda x: pd.Series(x.isocalendar()))
        response['month'] = response['hab_dat_collected_at'].apply(lambda x: x.month)

        return rm.HabData(hab_rec=hab_rec, data=response)
