from pydantic import BaseModel
from pandas import DataFrame

class Hab(BaseModel):
    hab_is_yn: bool
    hab_freq_type: str
    hab_goal: float

class HabData(BaseModel):
    hab_rec: Hab
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