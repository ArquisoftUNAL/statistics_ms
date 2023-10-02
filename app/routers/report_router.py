from fastapi import APIRouter, Depends, Request
from typing import Union
from app.models.report_models import HabitYNReport, HabitMeasureReport
from app.services.get_report.get_report import HabitReport
from app.repositories.habits_repository import HabitRepository
from app.repositories.statistics_repository import StatisticsRepository
from app.repositories.interfaces.habits_repository_interface import AbstractHabitReposiory
from app.repositories.interfaces.statistic_repository_interface import AbstractStatisticRepository
from uuid import UUID

def get_hr(request: Request):
    hab_repo: AbstractHabitReposiory = HabitRepository(request.app.state.engine)
    stat_repo: AbstractStatisticRepository = StatisticsRepository(request.app.state.client)
    return HabitReport(hab_repo, stat_repo)

router = APIRouter()

@router.get("/report/{hab_id}", response_model=Union[HabitMeasureReport, HabitYNReport])
async def get_habit_report(hab_id: UUID, hr: HabitReport = Depends(get_hr)):
    return await hr.get_habit_report(hab_id=hab_id)
