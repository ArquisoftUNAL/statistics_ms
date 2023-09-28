from fastapi import APIRouter, Depends, Request
from app.models import report_models as md
from app.services.habit_report import HabitReport
from app.repositories.habits_repository import HabitRepository
from uuid import UUID

def get_hs(request: Request):
    repo = HabitRepository(request.app.state.engine)
    return HabitReport(repo)

router = APIRouter()

@router.get("/report/yn/{hab_id}", response_model=md.HabitYNReport)
async def get_habit_yn_report(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    return await hs.get_habit_yn_report(hab_id=hab_id)

@router.get("/report/measure/{hab_id}", response_model=md.HabitMeasureReport)
async def get_habit_measure_report(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    return await hs.get_habit_measure_report(hab_id=hab_id)

@router.get("/measure/resume/{hab_id}", response_model=md.HabitMeasureResume)
async def get_habit_measure_resume(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    return await hs.get_habit_measure_resume(hab_id=hab_id)

@router.get("/measure/history/{hab_id}", response_model=md.HabitMeasureHistory)
async def get_habit_measure_history(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    return await hs.get_habit_measure_history(hab_id=hab_id)

@router.get("/measure/streaks/{hab_id}", response_model=md.HabitMeasureStreak)
async def get_habit_measure_streaks(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    return await hs.get_habit_measure_streaks(hab_id=hab_id)

@router.get("/yn/resume/{hab_id}", response_model=md.HabitYNResume)
async def get_habit_yn_resume(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    return await hs.get_habit_yn_resume(hab_id=hab_id)

@router.get("/yn/history/{hab_id}", response_model=md.HabitYNHistory)
async def get_habit_yn_history(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    return await hs.get_habit_yn_history(hab_id=hab_id)

@router.get("/yn/streaks/{hab_id}", response_model=md.HabitYNStreak)
async def get_habit_yn_streaks(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    return await hs.get_habit_yn_streaks(hab_id=hab_id)

@router.get("/freq_week_day/{hab_id}", response_model=md.HabitFreqWeekDay)
async def get_habit_freq_week_day(hab_id: UUID, hs: HabitReport = Depends(get_hs)):
    return await hs.get_habit_freq_week_day(hab_id=hab_id)
