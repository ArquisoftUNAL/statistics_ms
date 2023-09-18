""" a class to read from postgresql database using sqlalchemy"""
from dotenv import load_dotenv
import pandas as pd
import asyncio
import os
import app.models.repo_models as rm
import json
from datetime import datetime, date

load_dotenv()
url = os.getenv("GATEWAY_URL")

# TODO: Connect with actual gateway when it's implemented

class HabitRepository:
    def __init__(self):

        # Delete and query microservice on each request
        habits_file = open('data/habits.json')
        self.habits = json.load(habits_file)["habits"]

    def get_habit(self, hab_id):
        # Query to microservice rather than on local file
        for habit in self.habits:
            if habit['hab_id'] == hab_id:
                return habit
        return None

    def get_recurrence_data(self, rec_id):
        # Query to microservice rather than on local file
        for habit in self.habits:
            for rec in habit['recurrences']:
                if rec['hab_rec_id'] == rec_id:
                    return rec['data']
                
        return None
    
    def get_habit_recurrences(self, hab_id):
        habit = self.get_habit(hab_id)

        if habit is None:
            return None

        return habit['recurrences']
    
    async def get_hab_is_yn(self, hab_id):
        habit = self.get_habit(hab_id)

        if habit is None:
            return None

        return habit['hab_is_yn']

    async def get_hab_rec(self, hab_id) -> rm.HabRec:
        
        recurrences = self.get_habit_recurrences(hab_id)

        if recurrences is None or len(recurrences) == 0:
            return None
        
        recurrence = recurrences[0]

        return rm.HabRec(
            hab_rec_id=recurrence['hab_rec_id'],
            hab_rec_freq_type=recurrence['hab_rec_freq_type'],
            hab_rec_goal=recurrence.get('hab_rec_goal', 0)
        )

    async def get_habit_data(self, hab_id) -> rm.HabData:
        hab_rec = await self.get_hab_rec(hab_id)

        if hab_rec is None:
            return None
        
        data = self.get_recurrence_data(hab_rec.hab_rec_id)

        if data is None:
            return None
        
        # Generate data
        data = pd.json_normalize(data)

        data['hab_dat_collected_at'] = data['hab_dat_collected_at'].apply(lambda x: datetime.fromisoformat(x))
        data['hab_dat_amount'] = data['hab_dat_amount'].astype(float)
        data[['year', 'week', 'weekday']] = data['hab_dat_collected_at'].apply(lambda x: pd.Series(x.isocalendar()))
        data['month'] = data['hab_dat_collected_at'].apply(lambda x: x.month)
        
        return rm.HabData(
            hab_rec=hab_rec,
            data=data
        )
        