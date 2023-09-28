from app.repositories.habits_repository import HabitRepository
from app.models.habits_db_models import HabData
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

    async def get_habit_yn_report(self, hab_id: UUID) -> md.HabitYNReport:
        habit_data = await self.repo.get_habit_data(hab_id)

        return md.HabitYNReport(
            resume = await self.get_habit_yn_resume(habit_data),
            history = await self.get_habit_yn_history(habit_data),
            streaks = await self.get_habit_yn_streaks(habit_data),
            days_frequency = await self.get_habit_freq_week_day(habit_data)
        )

    async def get_habit_measure_report(self, hab_id: UUID) -> md.HabitMeasure:
        habit_data = await self.repo.get_habit_data(hab_id)

        return md.HabitMeasure(
            resume = await self.get_habit_measure_resume(habit_data),
            history = await self.get_habit_measure_history(habit_data),
            streaks = await self.get_habit_measure_streaks(habit_data),
            days_frequency = await self.get_habit_freq_week_day(habit_data)
        )

    async def get_habit_measure_resume(self, habit_data: HabData = None, hab_id: UUID = None) -> md.HabitMeasureResume:
        """
        Calculates the progress of a habit with a measure type frequency.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitMeasureResume: The report with the progress of the habit.
        """
        if habit_data == None:
            habit_data = await self.repo.get_habit_data(hab_id)

        today = date.today()
        goal = habit_data.hab.hab_goal
        if goal is None:
            goal = 0
        freq_type = freq_types[habit_data.hab.hab_freq_type]
        df = habit_data.data

        year = fn.year_progress(df, goal, today, freq_type)
        semester = fn.semester_progress(df, goal, today, freq_type)
        month = fn.month_progress(df, goal, today, freq_type) if freq_type < 6 else None
        week = fn.week_progress(df, goal, today, freq_type) if freq_type < 4 else None
        today = fn.day_progress(df, goal, today) if freq_type == 1 else None

        report = md.HabitMeasureResume(toDay=today, week=week, month=month, semester=semester, year=year)

        return report
    
    async def get_habit_measure_history(self, habit_data: HabData = None, hab_id: UUID = None) -> md.HabitMeasureHistory:
        """
        Calculates the history of a habit with a measure type frequency.
        
        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitMeasureHistory: The report with the history of the habit.      
        """
        if habit_data == None:
            habit_data = await self.repo.get_habit_data(hab_id)

        df = habit_data.data

        year = fn.ms_year_history(df)
        semester = fn.ms_semester_history(df)
        month = fn.ms_month_history(df)
        week = fn.ms_week_history(df)
        day = fn.ms_day_history(df)

        report = md.HabitMeasureHistory(day=day, week=week, month=month, semester=semester, year=year)

        return report
    
    async def get_habit_measure_streaks(self, habit_data: HabData = None, hab_id: UUID = None) -> md.HabitMeasureStreak:
        """
        Calculates the best streak of a habit with a measure type frequency.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitMeasureStreak: The report with the best streak of the habit.
        """
        if habit_data == None:
            habit_data = await self.repo.get_habit_data(hab_id)

        today = date.today()
        freq_type = freq_types[habit_data.hab.hab_freq_type]
        df = habit_data.data
        return fn.ms_streaks(df, today, freq_type)
    
    async def get_habit_yn_resume(self, habit_data: HabData = None, hab_id: UUID = None) -> md.HabitYNResume:
        """
        Calculates the progress of a habit with a yes/no type.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitYNResume: The report with the progress of the habit.
        """
        if habit_data == None:
            habit_data = await self.repo.get_habit_data(hab_id)

        today = date.today()
        df = habit_data.data
        freq_type = freq_types[habit_data.hab.hab_freq_type]

        year = fn.year_yn_resume(df, freq_type, today)
        semester = fn.semester_yn_resume(df, freq_type, today)
        month = fn.month_yn_resume(df, freq_type, today)
        total = fn.total_yn_resume(df, today)

        report = md.HabitYNResume(month=month, semester=semester, year=year, total=total)
        return report
    
    async def get_habit_yn_history(self, habit_data: HabData = None, hab_id: UUID = None) -> md.HabitYNHistory:
        """
        Calculates the history of a habit with a yes/no type.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitYNHistory: The report with the history of the habit.
        """
        if habit_data == None:
            habit_data = await self.repo.get_habit_data(hab_id)

        df = habit_data.data

        year = fn.yn_year_history(df)
        semester = fn.yn_semester_history(df)
        month = fn.yn_month_history(df)
        week = fn.yn_week_history(df)

        report = md.HabitYNHistory(week=week, month=month, semester=semester, year=year)

        return report
    
    async def get_habit_yn_streaks(self, habit_data: HabData = None, hab_id: UUID = None) -> md.HabitYNStreak:
        """
        Calculates the best streak of a habit with a yes/no type.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitYNBestStreak: The report with the best streak of the habit.
        """
        if habit_data == None:
            habit_data = await self.repo.get_habit_data(hab_id)

        today = date.today()
        freq_type = freq_types[habit_data.hab.hab_freq_type]
        df = habit_data.data
        return fn.yn_streaks(df, today, freq_type)
    
    async def get_habit_freq_week_day(self, habit_data: HabData = None, hab_id: UUID = None) -> md.HabitFreqWeekDay:
        """
        Calculates the frequency of a habit with a week day type.
        
        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitFreqWeekDay: The report with the frequency of the habit. 
        """
        if habit_data == None:
            habit_data = await self.repo.get_habit_data(hab_id)

        df = habit_data.data
        report = fn.freq_week_day(df)
        return report
    