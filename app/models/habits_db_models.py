from pydantic import BaseModel
from pandas import DataFrame
from uuid import UUID
from datetime import date

class Hab(BaseModel):
    hab_is_yn: bool
    hab_freq_type: str
    hab_goal: float

class HabDataCollected(BaseModel):
    hab_dat_id: UUID
    hab_dat_amount: float
    hab_dat_collected_at: date
    hab_id: UUID

class HabData(BaseModel):
    hab: Hab
    data: DataFrame

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not isinstance(value, DataFrame):
            raise ValueError('data must be a Pandas DataFrame')
        return value