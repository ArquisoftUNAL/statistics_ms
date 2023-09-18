from app.repositories.habits_repository import HabitRepository
from app.models.repo_models import HabData
from datetime import date
from uuid import UUID
from . import functions as fn
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
    def __init__(self, habit_repository: HabitRepository):
        self.repo = habit_repository

    async def get_habit_yn_report(self, hab_id: UUID) -> md.HabitYNReportModel:
        habit_data = await self.repo.get_habit_data(hab_id)

        return md.HabitYNReportModel(
            resume = await self.get_habit_yn_resume(habit_data),
            history = await self.get_habit_yn_history(habit_data),
            streaks = await self.get_habit_yn_streaks(habit_data),
            days_frequency = await self.get_habit_freq_week_day(habit_data)
        )

    async def get_habit_measure_report(self, hab_id: UUID) -> md.HabitMeasureReportModel:
        habit_data = await self.repo.get_habit_data(hab_id)

        return md.HabitMeasureReportModel(
            resume = await self.get_habit_measure_resume(habit_data),
            history = await self.get_habit_measure_history(habit_data),
            days_frequency = await self.get_habit_freq_week_day(habit_data)
        )

    async def get_habit_measure_resume(self, habit_data: HabData) -> md.HabitMeasureResumeReportModel:
        """
        Calculates the progress of a habit with a measure type frequency.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitMeasureResumeReportModel: The report with the progress of the habit.
        """
        today = date.today()
        goal = habit_data.hab_rec.hab_rec_goal
        freq_type = freq_types[habit_data.hab_rec.hab_rec_freq_type]
        df = habit_data.data

        year = fn.year_progress(df, goal, today, freq_type)
        semester = fn.semester_progress(df, goal, today, freq_type)
        month = fn.month_progress(df, goal, today, freq_type)
        week = fn.week_progress(df, goal, today, freq_type) if freq_type < 3 else None
        today = fn.day_progress(df, goal, today) if freq_type == 1 else None

        report = md.HabitMeasureResumeReportModel(toDay=today, week=week, month=month, semester=semester, year=year)

        return report
    
    async def get_habit_measure_history(self, habit_data: HabData) -> md.HabitMeasureHistoryReportModel:
        """
        Calculates the history of a habit with a measure type frequency.
        
        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitMeasureHistoryReportModel: The report with the history of the habit.      
        """
        df = habit_data.data

        year = fn.ms_year_history(df)
        semester = fn.ms_semester_history(df)
        month = fn.ms_month_history(df)
        week = fn.ms_week_history(df)
        day = fn.ms_day_history(df)

        report = md.HabitMeasureHistoryReportModel(day=day, week=week, month=month, semester=semester, year=year)

        return report
    
    async def get_habit_yn_resume(self, habit_data: HabData) -> md.HabitYNResumeReportModel:
        """
        Calculates the progress of a habit with a yes/no type.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitYNResumeReportModel: The report with the progress of the habit.
        """
        today = date.today()
        df = habit_data.data
        freq_type = freq_types[habit_data.hab_rec.hab_rec_freq_type]

        year = fn.year_yn_resume(df, freq_type, today)
        semester = fn.semester_yn_resume(df, freq_type, today)
        month = fn.month_yn_resume(df, freq_type, today)
        total = fn.total_yn_resume(df, today)

        report = md.HabitYNResumeReportModel(month=month, semester=semester, year=year, total=total)
        return report
    
    async def get_habit_yn_history(self, habit_data: HabData) -> md.HabitYNHistoryReportModel:
        """
        Calculates the history of a habit with a yes/no type.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitYNHistoryReportModel: The report with the history of the habit.
        """
        df = habit_data.data

        year = fn.yn_year_history(df)
        semester = fn.yn_semester_history(df)
        month = fn.yn_month_history(df)
        week = fn.yn_week_history(df)

        report = md.HabitYNHistoryReportModel(week=week, month=month, semester=semester, year=year)

        return report
    
    async def get_habit_yn_streaks(self, habit_data: HabData) -> md.HabitYNStreakReportModel:
        """
        Calculates the best streak of a habit with a yes/no type.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitYNBestStreakReportModel: The report with the best streak of the habit.
        """
        today = date.today()
        df = habit_data.data
        return fn.yn_streaks(df, today)
    
    async def get_habit_freq_week_day(self, habit_data: HabData) -> md.HabitFreqWeekDayReportModel:
        """
        Calculates the frequency of a habit with a week day type.
        
        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitFreqWeekDayReportModel: The report with the frequency of the habit. 
        """
        df = habit_data.data
        report = fn.freq_week_day(df)
        return report
    