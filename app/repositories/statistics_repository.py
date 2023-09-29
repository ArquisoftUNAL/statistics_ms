from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from beanie.odm.operators.update.general import Set, CurrentDate
from app.common.constants import STATISTICS_DB_URL
from app.models.statistics_db_models import ReportDocument
from app.exceptions.exceptions import (
    AppConnectionError,
    AppDatabaseError,
    HabitNotFoundError,
)
from typing import List, Optional, Union
from app.models.report_models import HabitMeasureReport, HabitYNReport
from uuid import UUID

class StatisticsRepository:
    def __init__(self):
        self.client = AsyncIOMotorClient(STATISTICS_DB_URL)
        self.db = self.client["statistics"]
        self.collection = self.db["reports"]

    async def connect(self):
        try:
            await init_beanie(database=self.db, document_models=[ReportDocument])
        except Exception as e:
            raise AppConnectionError(e)

    async def disconnect(self):
        self.client.close()

    async def get_all_reports(self) -> List[ReportDocument]:
        try:
            reports = await ReportDocument.find_all().to_list()
            return reports
        except Exception as e:
            raise AppDatabaseError(e)

    async def get_report_by_id(self, hab_id: UUID) -> Optional[ReportDocument]:
        try:
            report = await ReportDocument.find_one(ReportDocument.hab_id == hab_id)
            if report:
                return report
            else:
                raise HabitNotFoundError(f"Habit with id {hab_id} not found")
        except Exception as e:
            raise AppDatabaseError(e)

    async def create_report(self, report: ReportDocument):
        try:
            report.current_date({ReportDocument.created_at, True})
            report.current_date({ReportDocument.updated_at, True})
            await report.insert()
        except Exception as e:
            raise AppDatabaseError(e)

    async def update_report(self, hab_id: UUID, new_report: Union[HabitMeasureReport, HabitYNReport]):
        try:
            report = await ReportDocument.find_one(ReportDocument.hab_id == hab_id)
            await report.update(
                Set({
                    ReportDocument.hab_data_count: report.hab_data_count + 1,
                    ReportDocument.report: new_report
                    }),
                CurrentDate({ReportDocument.updated_at: True})
            )
        except Exception as e:
            raise AppDatabaseError(e)

    async def delete_report(self, hab_id: UUID) -> None:
        try:
            report = await ReportDocument.find_one(ReportDocument.hab_id == hab_id)
            if report:
                await report.delete()
            else:
                raise HabitNotFoundError(f"Habit with id {hab_id} not found")
        except Exception as e:
            raise AppDatabaseError(e)