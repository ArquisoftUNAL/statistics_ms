from fastapi import APIRouter, Depends
from app.models import report_models as md
from app.services.habit_report import HabitReport
from app.repositories.habits_repository import HabitRepository

router = APIRouter()

def get_hs():
    repo = HabitRepository()
    return HabitReport(repo)


@router.get("/habit/{hab_id}/measure/resume", response_model=md.HabitMeasureResumeReportModel)
async def get_habit_measure_resume(hab_id: int, hs: HabitReport = Depends(get_hs)):
    return hs.get_habit_measure_resume(hab_id)

@router.get("/habit/{hab_id}/measure/history", response_model=md.HabitMeasureHistoryReportModel)
async def get_habit_measure_history(hab_id: int, hs: HabitReport = Depends(get_hs)):
    return hs.get_habit_measure_history(hab_id)

@router.get("/habit/{hab_id}/yn/resume", response_model=md.HabitYNResumeReportModel)
async def get_habit_yn_resume(hab_id: int, hs: HabitReport = Depends(get_hs)):
    return hs.get_habit_yn_resume(hab_id)

@router.get("/habit/{hab_id}/yn/history", response_model=md.HabitYNHistoryReportModel)
async def get_habit_yn_history(hab_id: int, hs: HabitReport = Depends(get_hs)):
    return hs.get_habit_yn_history(hab_id)

@router.get("/habit/{hab_id}/yn/best_streak", response_model=md.HabitYNBestStreakReportModel)
async def get_habit_yn_best_streak(hab_id: int, hs: HabitReport = Depends(get_hs)):
    return hs.get_habit_yn_best_streak(hab_id)

@router.get("/habit/{hab_id}/freq/week_day", response_model=md.HabitFreqWeekDayReportModel)
async def get_habit_freq_week_day(hab_id: int, hs: HabitReport = Depends(get_hs)):
    return hs.get_habit_freq_week_day(hab_id)
