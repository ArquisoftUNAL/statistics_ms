from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional, Union
from app.models.statistics_db_models import ReportDocument
from app.models.report_models import HabitMeasureReport, HabitYNReport

class AbstractStatisticRepository(ABC):
    @abstractmethod
    async def get_all_reports(self) -> List[ReportDocument]:
        pass

    @abstractmethod
    async def get_report_by_id(self, hab_id: UUID) -> Optional[ReportDocument]:
        pass

    @abstractmethod
    async def create_report(self, report: ReportDocument):
        pass

    @abstractmethod
    async def update_report(self, hab_id: UUID, new_report: Union[HabitMeasureReport, HabitYNReport]):
        pass

    @abstractmethod
    async def delete_report(self, hab_id: UUID):
        pass