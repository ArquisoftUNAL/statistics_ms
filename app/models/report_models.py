from pydantic import BaseModel
from typing import Dict, Tuple, Optional, Union, List
from datetime import date

class DataResume(BaseModel):
    percentage: float
    progress: float
    remaining: float

class DateValue(BaseModel):
    year: int
    month: Optional[int]
    day: Optional[int]
    value: float

class ListDateValue(BaseModel): #DateFloatDir
    data: List[DateValue]
    #data: Dict[Union[int, Tuple[int, int], date], float]

class DateCount(BaseModel):
    year: int
    week: Optional[int]
    month: Optional[int]
    semester: Optional[int]
    count: int

class ListDateCount(BaseModel):#DateIntDir(BaseModel):
    data: List[DateCount]
    #data: Dict[Union[int, Tuple[int, int]], int]

class HabitMeasureResume(BaseModel):
    toDay: Optional[DataResume] = None
    week: Optional[DataResume] = None
    month: Optional[DataResume] = None
    semester: Optional[DataResume] = None
    year: Optional[DataResume] = None

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
    start_date: date
    end_date: date
    quantity: float

class ListHabitStreak(BaseModel):
    data: List[HabitStreak]
    #data: Dict[Tuple[date, date], int]

class HabitFreqWeekDay(BaseModel):
    year: int
    month: int
    week_day: int
    quantity: int

class ListHabitFreqWeekDay(BaseModel):
    data: List[HabitFreqWeekDay]
    #data: {(<year>, <month>): {<day of week>: <quantity>}}
    #data: Dict[Tuple[int, int], Dict[int, int]]

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