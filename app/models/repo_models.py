from pydantic import BaseModel
import pandas as pd

class HabRec(BaseModel):
    hab_rec_id: int
    hab_rec_freq_type: str
    hab_rec_goal: float

class HabData(BaseModel):
    hab_rec: HabRec
    data: pd.DataFrame