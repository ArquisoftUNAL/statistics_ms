from uuid import UUID
from typing import List, Optional, Union
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from beanie.odm.operators.update.general import Set, CurrentDate
from app.models.statistics_db_models import ReportDocument
from app.models.report_models import HabitMeasureReport, HabitYNReport
from .interfaces.statistic_repository_interface import AbstractStatisticRepository


class StatisticsRepository(AbstractStatisticRepository):
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.db = self.client["statistics"]
        self.collection = self.db["reports"]

    async def get_all_reports(self) -> List[ReportDocument]:
        reports = await ReportDocument.find_all().to_list()
        return reports

    async def get_report_by_id(self, hab_id: UUID) -> Optional[ReportDocument]:
        report = await ReportDocument.find_one(ReportDocument.hab_id == hab_id)
        return report

    async def create_report(self, report: ReportDocument):
        report.current_date({ReportDocument.created_at, True})
        report.current_date({ReportDocument.updated_at, True})
        await report.insert()

    async def update_report(self, hab_id: UUID, new_report: Union[HabitMeasureReport, HabitYNReport]):
        report = await ReportDocument.find_one(ReportDocument.hab_id == hab_id)
        await report.update(
            Set(
                {
                    ReportDocument.hab_data_count: report.hab_data_count + 1,
                    ReportDocument.report: new_report,
                }
            ),
            CurrentDate({ReportDocument.updated_at: True}),
        )

    async def delete_report(self, hab_id: UUID) -> None:
        report = await ReportDocument.find_one(ReportDocument.hab_id == hab_id)
        if report:
            await report.delete()
