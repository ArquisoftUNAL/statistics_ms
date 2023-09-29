from uuid import UUID
from app.repositories.interfaces.habits_repository_interface import AbstractHabitReposiory
from app.repositories.interfaces.statistic_repository_interface import AbstractStatisticRepository
from app.models.habits_db_models import HabData
import app.models.report_models as md

freq_types = {
    'daily': 1,
    'daily2': 2,
    'weekly': 3,
    'weekly2': 4,
    'monthly': 5,
    'monthly2': 6
}

class HabitReport:
    def __init__(self, habit_repository: AbstractHabitReposiory, statistic_repository: AbstractStatisticRepository):
        self.hab_repo = habit_repository
        self.stat_repo = statistic_repository
        

    async def get_habit_yn_report(self, hab_id: UUID) -> md.HabitYNReport:
        habit_data = await self.hab_repo.get_habit_data(hab_id)

        return md.HabitYNReport(
            resume = await self.get_habit_yn_resume(habit_data),
            history = await self.get_habit_yn_history(habit_data),
            streaks = await self.get_habit_yn_streaks(habit_data),
            days_frequency = await self.get_habit_freq_week_day(habit_data)
        )

    async def get_habit_measure_report(self, hab_id: UUID) -> md.HabitMeasureReport:
        habit_data = await self.hab_repo.get_habit_data(hab_id)

        return md.HabitMeasureReport(
            resume = await self.get_habit_measure_resume(habit_data),
            history = await self.get_habit_measure_history(habit_data),
            streaks = await self.get_habit_measure_streaks(habit_data),
            days_frequency = await self.get_habit_freq_week_day(habit_data)
        )

    async def get_habit_measure_resume(self, habit_data: HabData = None, hab_id: UUID = None) -> md.HabitMeasureResume:
        pass
    
    async def get_habit_measure_history(self, habit_data: HabData = None, hab_id: UUID = None) -> md.HabitMeasureHistory:
        pass
    
    async def get_habit_measure_streaks(self, habit_data: HabData = None, hab_id: UUID = None) -> md.HabitMeasureStreak:
        pass
    
    async def get_habit_yn_resume(self, habit_data: HabData = None, hab_id: UUID = None) -> md.HabitYNResume:
        pass
    
    async def get_habit_yn_history(self, habit_data: HabData = None, hab_id: UUID = None) -> md.HabitYNHistory:
        pass
    
    async def get_habit_yn_streaks(self, habit_data: HabData = None, hab_id: UUID = None) -> md.HabitYNStreak:
        pass
    
    async def get_habit_freq_week_day(self, habit_data: HabData = None, hab_id: UUID = None) -> md.HabitFreqWeekDay:
        pass