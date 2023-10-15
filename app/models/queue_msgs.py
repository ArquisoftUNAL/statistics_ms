import json
from datetime import date
from uuid import UUID
from pydantic import BaseModel

class NewHabitData(BaseModel):
    hab_dat_id: UUID
    hab_dat_amount: float
    hab_dat_collected_at: date
    hab_id: UUID

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)