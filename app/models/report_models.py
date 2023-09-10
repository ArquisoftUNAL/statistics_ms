from pydantic import BaseModel
from typing import Dict, Tuple, Optional
from datetime import date

class ReportData(BaseModel):
    percentage: float
    progress: float
    remaining: float

class HabitYNResumeReport(BaseModel):
    month: float
    semester: float
    year: float
    total: int

class HabitYNHistoryReport(BaseModel):
    #data: {week(<start date>, <end date>): <quantity>}
    week: Dict[Tuple[date, date], int]
    #data: {month(<month>, <year>): <quantity>}
    month: Dict[Tuple[int, int], int]
    #data: {semester(<semester>, <year>): <quantity>}
    semester: Dict[Tuple[int, int], int]
    #data: {year(<year>): <quantity>}
    year: Dict[int, int]

class HabitYNBestStreakReport(BaseModel):
    #data: {(<start date>, <end date>): <quantity>}
    data: Dict[Tuple[date, date], int]

class HabitMeasureResumeReport(BaseModel):
    toDay: Optional[ReportData] = None
    week: Optional[ReportData] = None
    month: ReportData
    semester: ReportData
    year: ReportData

class HabitMeasureHistoryReport(BaseModel):
    #data: {<date>: <quantity>}
    day: Dict[date, float]
    #data: {week(<start date>, <end date>): <quantity>}
    week: Dict[Tuple[date, date], float]
    #data: {month(<month>, <year>): <quantity>}
    month: Dict[Tuple[int, int], float]
    #data: {semester(<semester>, <year>): <quantity>}
    semester: Dict[Tuple[int, int], float]
    #data: {year(<year>): <quantity>}
    year: Dict[int, float]


class HabitFreqWeekDayReport(BaseModel):
    #data: {(<month>, <year>): {<day of week>: <quantity>}}
    data: Dict[Tuple[int, int], Dict[int, int]]

