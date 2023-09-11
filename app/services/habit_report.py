from app.repositories.habits_repository import HabitRepository
import app.models.report_models as md
from datetime import date
from . import functions as fn

freq_types = {
    'daily': 1,
    'weekly': 2,
    'monthly': 3,
}

class HabitReport:
    def __init__(self, habit_repository: HabitRepository):
        self.repo = habit_repository()

    def get_habit_measure_resume(self, hab_id: int) -> md.HabitMeasureResumeReportModel:
        """
        Calculates the progress of a habit with a measure type frequency.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitMeasureResumeReportModel: The report with the progress of the habit.
        """
        today = date.today()
        habit_data = self.repo.get_habit_data(hab_id)
        freq_type = habit_data.hab_rec.hab_rec_freq_type
        goal = habit_data.hab_rec.hab_rec_goal
        df = habit_data.data

        report = md.HabitMeasureResumeReportModel()

        report.year = fn.year_progress(df, goal, today, freq_types[freq_type])
        report.semester = fn.semester_progress(df, goal, today, freq_types[freq_type])
        report.month = fn.month_progress(df, goal, today, freq_types[freq_type])
        if freq_types[freq_type] < 3:
            report.week = fn.week_progress(df, goal, today, freq_types[freq_type])
        if freq_types[freq_type] == 1:
            report.today = fn.day_progress(df, goal, today)

        return report
    
    def get_habit_measure_history(self, hab_id: int) -> md.HabitMeasureHistoryReportModel:
        """
        Calculates the history of a habit with a measure type frequency.
        
        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitMeasureHistoryReportModel: The report with the history of the habit.
        
        """
        habit_data = self.repo.habit_data(hab_id)
        df = habit_data.data
        report = md.HabitMeasureHistoryReportModel()

        report.year = fn.ms_year_history(df)
        report.semester = fn.ms_semester_history(df)
        report.month = fn.ms_month_history(df)
        report.week = fn.ms_week_history(df)
        report.day = fn.ms_day_history(df)

        return report
    
    def get_habit_yn_resume(self, hab_id: int) -> md.HabitYNResumeReportModel:
        """
        Calculates the progress of a habit with a yes/no type.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitYNResumeReportModel: The report with the progress of the habit.
        """
        today = date.today()
        habit_data = self.repo.habit_data(hab_id)
        df = habit_data.data
        freq_type = habit_data.hab_rec.hab_rec_freq_type
        goal = None

        report = md.HabitYNResumeReportModel()

        report.year = fn.year_yn_resume(df, goal, today)
        report.semester = fn.semester_yn_resume(df, goal, today)
        report.month = fn.month_yn_resume(df, goal, today)
        report.total = fn.total_yn_resume(df, today)

        return report
    
    def get_habit_yn_history(self, hab_id: int) -> md.HabitYNHistoryReportModel:
        """
        Calculates the history of a habit with a yes/no type.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitYNHistoryReportModel: The report with the history of the habit.
        """
        habit_data = self.repo.habit_data(hab_id)
        df = habit_data.data

        report = md.HabitYNHistoryReportModel()

        report.year = fn.yn_year_history(df)
        report.semester = fn.yn_semester_history(df)
        report.month = fn.yn_month_history(df)
        report.week = fn.yn_week_history(df)

        return report
    
    def get_habit_yn_streaks(self, hab_id: int) -> md.HabitYNBestStreakReportModel:
        """
        Calculates the best streak of a habit with a yes/no type.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitYNBestStreakReportModel: The report with the best streak of the habit.
        """
        today = date.today()
        habit_data = self.repo.habit_data(hab_id)
        df = habit_data.data
        report = md.HabitYNBestStreakReportModel()
        return report
    
    def get_habit_freq_week_day(self, hab_id: int) -> md.HabitFreqWeekDayReportModel:
        """
        Calculates the frequency of a habit with a week day type.
        
        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitFreqWeekDayReportModel: The report with the frequency of the habit. 
        """
        habit_data = self.repo.habit_data(hab_id)
        df = habit_data.data
        report = fn.freq_week_day(df)
        return report
    