from pydantic import BaseModel
from typing import Dict, Tuple, Optional
from datetime import datetime, date

class DataReportModel(BaseModel):
    percentage: float
    progress: float
    remaining: float

class DateFloatDir(BaseModel):
    data: Dict[Tuple[int, int], float]

class DateIntDir(BaseModel):
    data: Dict[datetime, int]

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

class HabitYNBestStreakReportModel(BaseModel):
    #data: {(<start date>, <end date>): <quantity>}
    data: Dict[Tuple[datetime, datetime], int]

class HabitFreqWeekDayReportModel(BaseModel):
    #data: {(<year>, <month>): {<day of week>: <quantity>}}
    data: Dict[Tuple[int, int], Dict[int, int]]

