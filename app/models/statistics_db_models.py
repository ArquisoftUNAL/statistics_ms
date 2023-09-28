from .report_models import HabitMeasureReport, HabitYNReport
from beanie import Document, Indexed
from pydantic import BaseModel
from typing import Union, Optional
from datetime import datetime
from uuid import UUID

class Report(BaseModel):
    hab_id: UUID
    hab_data_count: int
    report: Union[HabitMeasureReport, HabitYNReport]
    updated_at: Optional[datetime]
    created_at: Optional[datetime]

class ReportDocument(Document, Report):
    hab_id: Indexed = Indexed(Report.hab_id, unique=True)

    class Settings:
        name = "reports"
