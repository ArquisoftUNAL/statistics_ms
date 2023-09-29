from pydantic import BaseModel
from uuid import UUID
from pydantic import BaseModel
from datetime import date

class Streak(BaseModel):
    date_start: date
    date_end: date
    data: float
class UpdateStreak(BaseModel):
    hab_id: UUID
    streak: Streak

class UpDateStreakMutation(BaseModel):
    def __init__(self, variables: UpdateStreak):
        self.query = """
        mutation notifyStreakUpdate($hab_id: UUID!, $streak: Streak!) {
                notifyStreakUpdate(hab_id: $hab_id, streak: $streak) {
                    status
                    message
                }
            }
        """
        self.variables = dict(variables)

    def get_query(self):
        return self.query, self.variables

