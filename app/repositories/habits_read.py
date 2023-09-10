""" a class to read from postgresql database using sqlalchemy and pandas"""
from sqlalchemy import create_engine, URL, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pandas as pd
import asyncio
import os

load_dotenv()
url = URL(
    drivername="postgresql",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
)

class HabitReadRepository:
    def __init__(self):
        self.engine = create_engine(url)
        self.session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()

        self.cat = Table('Category', self.metadata, autoload=True)
        self.hab = Table('Habit', self.metadata, autoload=True)
        self.hab_rec = Table('Habit_Recurrency', self.metadata, autoload=True)
        self.hab_data = Table('Habit_data_Collected', self.metadata, autoload=True)
    
    async def get_habit_data(self, hab_id):
        query = select([
            self.hab.c.hab_type_yn,
            self.hab_rec.c.hab_rec_freq_type,
            self.hab_rec.c.hab_rec_freq_goal,
            self.hab_rec.c.hab_rec_freq_date,
            self.hab_data.c.hab_data_amount,
            self.hab_data.c.hab_data_collected,
        ]).select_from(
            self.hab.join(self.hab_rec, self.hab.c.hab_id == self.hab_rec.c.hab_id)
            .join(self.hab_data, self.hab_rec.c.hab_rec_id == self.hab_data.c.hab_rec_id)
        ).where(self.hab.c.hab_id == hab_id)

        return await asyncio.get_event_loop().run_in_executor(None, pd.read_sql, query, self.engine)

