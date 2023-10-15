from fastapi import APIRouter, Depends, Request
from typing import Union
from app.models.report_models import HabitYNReport, HabitMeasureReport
from app.services.get_report.get_report import GetReport
from app.services.create_report.create_report import CreateHabitReport
from app.repositories.habits_repository import HabitRepository
from app.repositories.statistics_repository import StatisticsRepository
from app.repositories.interfaces.habits_repository_interface import AbstractHabitReposiory
from app.repositories.interfaces.statistic_repository_interface import AbstractStatisticRepository
from uuid import UUID

def get_gr(request: Request):
    hab_repo: AbstractHabitReposiory = HabitRepository(request.app.state.engine)
    stat_repo: AbstractStatisticRepository = StatisticsRepository(request.app.state.client)
    return GetReport(hab_repo, stat_repo)

router = APIRouter()

@router.get("/{hab_id}", response_model=Union[HabitMeasureReport, HabitYNReport])
async def get_habit_report(hab_id: UUID, gr: GetReport = Depends(get_gr)):
    return await gr.get_habit_report(hab_id)

