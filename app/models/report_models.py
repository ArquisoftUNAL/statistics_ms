from pydantic import BaseModel
from typing import Dict, Tuple, Optional, Union
from datetime import date

class DataReportModel(BaseModel):
    percentage: float
    progress: float
    remaining: float

class DateFloatDir(BaseModel):
    data: Dict[Union[int, Tuple[int, int], date], float]

class DateIntDir(BaseModel):
    data: Dict[Union[int, Tuple[int, int]], int]

class HabitMeasureResumeReportModel(BaseModel):
    toDay: Optional[DataReportModel] = None
    week: Optional[DataReportModel] = None
    month: Optional[DataReportModel] = None
    semester: Optional[DataReportModel] = None
    year: Optional[DataReportModel] = None

class HabitMeasureHistoryReportModel(BaseModel):
    day: DateFloatDir
    week: DateFloatDir
    month: DateFloatDir
    semester: DateFloatDir
    year: DateFloatDir

class HabitMeasureStreakReportModel(BaseModel):
    #data: {(<start date>, <end date>): <quantity>}
    data: Dict[Tuple[date, date], float]

class HabitYNResumeReportModel(BaseModel):
    month: float
    semester: float
    year: float
    total: int

class HabitYNHistoryReportModel(BaseModel):
    week: DateIntDir
    month: DateIntDir
    semester: DateIntDir
    year: DateIntDir

class HabitYNStreakReportModel(BaseModel):
    #data: {(<start date>, <end date>): <quantity>}
    data: Dict[Tuple[date, date], int]

class HabitFreqWeekDayReportModel(BaseModel):
    #data: {(<year>, <month>): {<day of week>: <quantity>}}
    data: Dict[Tuple[int, int], Dict[int, int]]

class HabitYNReportModel(BaseModel):
    resume: HabitYNResumeReportModel
    history: HabitYNHistoryReportModel
    streaks: HabitYNStreakReportModel
    days_frequency: HabitFreqWeekDayReportModel

class HabitMeasureReportModel(BaseModel):
    resume: HabitMeasureResumeReportModel
    history: HabitMeasureHistoryReportModel
    streaks: HabitMeasureStreakReportModel
    days_frequency: HabitFreqWeekDayReportModel