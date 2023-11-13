from uuid import UUID
from pydantic import BaseModel
from datetime import date


class Streak(BaseModel):
    start_date: date
    end_date: date
    quantity: float


class UpDateStreak(BaseModel):
    freq_type: str
    hab_id: UUID
    streak: Streak


class UpDateStreakMutation(UpDateStreak):
    query: str = """mutation notifyStreakUpdate($hab_id: UUID!, $freq_type: String!, $streak: Streak!) {
                notifyStreakUpdate(hab_id: $hab_id, freq_type: $freq_type, streak: $streak) {
                    status
                    message
                }
            }"""
    variables: dict = {}

    def __init__(self, data: UpDateStreak):
        super().__init__(**data.dict())
        self.variables = data.dict()

    def get_mutation(self):
        return self.query, self.variables