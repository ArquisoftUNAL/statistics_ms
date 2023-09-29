from abc import ABC, abstractmethod
from uuid import UUID
from app.models.habits_db_models import HabData, Hab

class AbstractHabitReposiory(ABC):
    @abstractmethod
    async def get_hab(self, hab_id: UUID) -> Hab:
        pass

    @abstractmethod
    async def get_habit_data(self, hab_id: UUID) -> HabData:
        pass