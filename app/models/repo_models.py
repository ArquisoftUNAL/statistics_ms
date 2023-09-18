from pydantic import BaseModel
from pandas import DataFrame
from uuid import UUID

class HabRec(BaseModel):
    hab_rec_id: str
    hab_rec_freq_type: str
    hab_rec_goal: float

class HabData(BaseModel):
    hab_rec: HabRec
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