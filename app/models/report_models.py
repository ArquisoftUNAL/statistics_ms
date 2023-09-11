from pydantic import BaseModel
from typing import Dict, Tuple, Optional
from datetime import date

class DataReportModel(BaseModel):
    percentage: float
    progress: float
    remaining: float

class DateFloatDir(BaseModel):
    data: Dict[date, float]

class HabitMeasureResumeReportModel(BaseModel):
    toDay: Optional[DataReportModel] = None
    week: Optional[DataReportModel] = None
    month: DataReportModel
    semester: DataReportModel
    year: DataReportModel

class HabitMeasureHistoryReportModel(BaseModel):
    day: DateFloatDir
    week: DateFloatDir
    month: DateFloatDir
    semester: DateFloatDir
    year: DateFloatDir


class HabitYNResumeReportModel(BaseModel):
    month: float
    semester: float
    year: float
    total: int

class HabitYNHistoryReportModel(BaseModel):
    #data: {week(<start date>, <end date>): <quantity>}
    week: Dict[Tuple[date, date], int]
    #data: {month(<month>, <year>): <quantity>}
    month: Dict[Tuple[int, int], int]
    #data: {semester(<semester>, <year>): <quantity>}
    semester: Dict[Tuple[int, int], int]
    #data: {year(<year>): <quantity>}
    year: Dict[int, int]

class HabitYNBestStreakReportModel(BaseModel):
    #data: {(<start date>, <end date>): <quantity>}
    data: Dict[Tuple[date, date], int]

class HabitFreqWeekDayReportModel(BaseModel):
    #data: {(<month>, <year>): {<day of week>: <quantity>}}
    data: Dict[Tuple[int, int], Dict[int, int]]

