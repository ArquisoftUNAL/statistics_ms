from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DataResume(BaseModel):
    percentage: float
    progress: float
    remaining: float

class DateValue(BaseModel):
    year: int
    semester: Optional[int] = None
    month: Optional[int] = None
    week: Optional[int] = None
    day: Optional[int] = None
    value: float

class ListDateValue(BaseModel):
    data: List[DateValue]

class DateCount(BaseModel):
    year: int
    week: Optional[int] = None
    month: Optional[int] = None
    semester: Optional[int] = None
    count: int

class ListDateCount(BaseModel):
    data: List[DateCount]

class HabitMeasureResume(BaseModel):
    toDay: Optional[DataResume] = None
    week: Optional[DataResume] = None
    month: Optional[DataResume] = None
    semester: Optional[DataResume]
    year: Optional[DataResume]

class HabitMeasureHistory(BaseModel):
    day: ListDateValue
    week: ListDateValue
    month: ListDateValue
    semester: ListDateValue
    year: ListDateValue

class HabitYNResume(BaseModel):
    month: float
    semester: float
    year: float
    total: int

class HabitYNHistory(BaseModel):
    week: ListDateCount
    month: ListDateCount
    semester: ListDateCount
    year: ListDateCount

class HabitStreak(BaseModel):
    start_date: datetime
    end_date: datetime
    quantity: float

class ListHabitStreak(BaseModel):
    data: List[HabitStreak]

class HabitFreqWeekDay(BaseModel):
    year: int
    month: int
    week_day: int
    quantity: int

class ListHabitFreqWeekDay(BaseModel):
    data: List[HabitFreqWeekDay]

class HabitYNReport(BaseModel):
    resume: HabitYNResume
    history: HabitYNHistory
    streaks: ListHabitStreak
    days_frequency: ListHabitFreqWeekDay

class HabitMeasureReport(BaseModel):
    resume: HabitMeasureResume
    history: HabitMeasureHistory
    streaks: ListHabitStreak
    days_frequency: ListHabitFreqWeekDay