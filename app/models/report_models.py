from pydantic import BaseModel
from typing import Dict, Tuple, Optional, Union
from datetime import date

class DataResume(BaseModel):
    percentage: float
    progress: float
    remaining: float

class DateFloatDir(BaseModel):
    data: Dict[Union[int, Tuple[int, int], date], float]

class DateIntDir(BaseModel):
    data: Dict[Union[int, Tuple[int, int]], int]

class HabitMeasureResume(BaseModel):
    toDay: Optional[DataResume] = None
    week: Optional[DataResume] = None
    month: Optional[DataResume] = None
    semester: Optional[DataResume] = None
    year: Optional[DataResume] = None

class HabitMeasureHistory(BaseModel):
    day: DateFloatDir
    week: DateFloatDir
    month: DateFloatDir
    semester: DateFloatDir
    year: DateFloatDir

class HabitMeasureStreak(BaseModel):
    #data: {(<start date>, <end date>): <quantity>}
    data: Dict[Tuple[date, date], float]

class HabitYNResume(BaseModel):
    month: float
    semester: float
    year: float
    total: int

class HabitYNHistory(BaseModel):
    week: DateIntDir
    month: DateIntDir
    semester: DateIntDir
    year: DateIntDir

class HabitYNStreak(BaseModel):
    #data: {(<start date>, <end date>): <quantity>}
    data: Dict[Tuple[date, date], int]

class HabitFreqWeekDay(BaseModel):
    #data: {(<year>, <month>): {<day of week>: <quantity>}}
    data: Dict[Tuple[int, int], Dict[int, int]]

class HabitYNReport(BaseModel):
    resume: HabitYNResume
    history: HabitYNHistory
    streaks: HabitYNStreak
    days_frequency: HabitFreqWeekDay

class HabitMeasureReport(BaseModel):
    resume: HabitMeasureResume
    history: HabitMeasureHistory
    streaks: HabitMeasureStreak
    days_frequency: HabitFreqWeekDay