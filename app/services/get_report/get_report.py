from uuid import UUID
from typing import Union
from app.repositories.interfaces.habits_repository_interface import (
    AbstractHabitReposiory,
)
from app.repositories.interfaces.statistic_repository_interface import (
    AbstractStatisticRepository,
)
from app.services.create_report.create_report import CreateHabitReport
from app.models.report_models import HabitMeasureReport, HabitYNReport
from app.exceptions.handle_exeptions import handle_exception
from app.exceptions.exceptions import (
    HabitNotFoundError,
)

class GetReport:
    def __init__(
        self,
        habit_repository: AbstractHabitReposiory,
        statistic_repository: AbstractStatisticRepository,
    ):
        self.hab_repo = habit_repository
        self.stat_repo = statistic_repository

    async def get_habit_report(
        self, habit_id: UUID
    ) -> Union[HabitMeasureReport, HabitYNReport]:
        try:
            report_doc = await self.stat_repo.get_report_by_id(habit_id)

            if report_doc is None:
                report_doc = await CreateHabitReport(
                    self.hab_repo, self.stat_repo
                ).create_habit_report(habit_id)

                if report_doc is None:
                    raise HabitNotFoundError("Habit not found")

                return report_doc.report

            return report_doc.report

        except Exception as e:
            handle_exception(e)
            return None
