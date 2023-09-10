from pydantic import BaseModel
import datetime

class Report(BaseModel):
    usr_id: int
    hab_id: int
    hab_type_yn: bool
    cat_id: int
    hab_rec_id: int
    hab_rec_goal: float
    hab_rec_freq_date: str
    hab_data_id: int
    hab_data_collected: float
    hab_data_date: datetime.date

class Cateogry(BaseModel):
    cat_id: int
    cat_name: str

class Habit(BaseModel):
    hab_id: int
    hab_name: str
    hab_created_at: datetime.date
    hab_updated_at: datetime.date
    hab_is_favorite: bool
    hab_type_yn: bool
    hab_color: str
    hab_units: str
    usr_id: int
    cat_id: int

class HabitRecurrency(BaseModel):
    hab_rec_id: int
    hab_rec_freq_type: str
    hab_rec_freq_date: datetime.date
    hab_rec_goal: float
    hab_id: int

class HabitDataCollected(BaseModel):
    hab_data_id: int
    hab_data_amount: float
    hab_data_collected: float
    hab_rec_id: int
