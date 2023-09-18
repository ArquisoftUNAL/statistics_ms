from fastapi import APIRouter, Depends
from app.models import report_models as md
from app.services.habit_report import HabitReport
from app.repositories.habits_repository import HabitRepository
from sqlalchemy import  URL
from uuid import UUID
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os

load_dotenv()
url = URL.create(
    drivername="postgresql+asyncpg",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
)

engine = create_async_engine(url)

def get_hs():
    repo = HabitRepository(engine)
    return HabitReport(repo)


router = APIRouter()

@router.get("/yn_report/{hab_id}", response_model=md.HabitYNResumeReportModel)
async def get_habit_yn_report(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    return await hs.get_habit_yn_report(hab_id)

@router.get("/measure_report/{hab_id}", response_model=md.HabitMeasureReportModel)
async def get_habit_measure_report(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    return await hs.get_habit_measure_report(hab_id)

@router.get("/measure/resume/{hab_id}", response_model=md.HabitMeasureResumeReportModel)
async def get_habit_measure_resume(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    body = hs.get_habit_measure_resume(hab_id)
    return body

@router.get("/measure/history/{hab_id}", response_model=md.HabitMeasureHistoryReportModel)
async def get_habit_measure_history(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    return hs.get_habit_measure_history(hab_id)

@router.get("/yn/resume/{hab_id}", response_model=md.HabitYNResumeReportModel)
async def get_habit_yn_resume(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    return hs.get_habit_yn_resume(hab_id)

@router.get("/yn/history/{hab_id}", response_model=md.HabitYNHistoryReportModel)
async def get_habit_yn_history(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    return hs.get_habit_yn_history(hab_id)

@router.get("/yn/streaks/{hab_id}", response_model=md.HabitYNStreakReportModel)
async def get_habit_yn_streaks(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    return hs.get_habit_yn_streaks(hab_id)

@router.get("/freq_week_day/{hab_id}", response_model=md.HabitFreqWeekDayReportModel)
async def get_habit_freq_week_day(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    return hs.get_habit_freq_week_day(hab_id)
