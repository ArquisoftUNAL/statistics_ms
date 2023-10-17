from .report_models import HabitMeasureReport, HabitYNReport
from beanie import Document, Indexed
from pydantic import BaseModel
from typing import Union, Optional
from datetime import datetime
from uuid import UUID

class Report(BaseModel):
    hab_id: UUID
    hab_is_yn: bool
    hab_freq_type: str
    hab_goal: Optional[float]
    hab_data_count: int
    report: Union[HabitMeasureReport, HabitYNReport]
    updated_at: datetime
    created_at: datetime

class ReportDocument(Document, Report):
    hab_id: UUID = Indexed(UUID, unique=True)

    class Settings:
        name = "reports"
