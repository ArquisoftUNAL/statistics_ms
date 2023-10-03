from pydantic import BaseModel
from uuid import UUID
from pydantic import BaseModel
from datetime import date

class Streak(BaseModel):
    date_start: date
    date_end: date
    data: float

class UpDateStreak(BaseModel):
    freq_type: str
    hab_id: UUID
    streak: Streak

class UpDateStreakMutation(UpDateStreak):
    def __init__(self, variables: UpDateStreak):
        self.query = """
        mutation notifyStreakUpdate($hab_id: UUID!, $freq_type: String!, $streak: Streak!) {
                notifyStreakUpdate(hab_id: $hab_id, freq_type: $freq_type, streak: $streak) {
                    status
                    message
                }
            }
        """
        self.variables = dict(variables)

    def get_mutation(self):
        return self.query, self.variables