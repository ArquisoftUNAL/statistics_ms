from pydantic import BaseModel, validator, Field
import pandas as pd
from typing import Type

class DataFrameModel(BaseModel):
    data: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not isinstance(value, pd.DataFrame):
            raise ValueError('data must be a Pandas DataFrame')
        return value

class HabRec(BaseModel):
    hab_rec_id: int
    hab_rec_freq_type: str
    hab_rec_goal: float

class HabData(BaseModel):
    hab_rec: HabRec
    data: DataFrameModel