from app.repositories.habits_repository import HabitRepository
import app.models.report_models as md
from datetime import date, timedelta
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
    
    def get_habit_measure_history(self, hab_id: int):
        habit_data = self.repo.habit_data(hab_id)
        df = habit_data.data
        report = md.HabitMeasureHistoryReportModel()

        report.year = fn.year_history(df)
        report.semester = fn.semester_history(df)
        report.month = fn.month_history(df)
        report.week = fn.week_history(df)
        report.day = fn.day_history(df)

        return report
    
    def get_habit_yn_resume(self, hab_id: int):
        habit_data = self.repo.habit_data(hab_id)
        report = md.HabitYNResumeReportModel()
        return report
    
    def get_habit_yn_history(self, hab_id: int):
        habit_data = self.repo.habit_data(hab_id)
        report = md.HabitYNHistoryReportModel()
        return report
    
    def get_habit_yn_best_streak(self, hab_id: int):
        habit_data = self.repo.habit_data(hab_id)
        report = md.HabitYNBestStreakReportModel()
        return report
    
    def get_habit_freq_week_day(self, hab_id: int):
        habit_data = self.repo.habit_data(hab_id)
        report = md.HabitFreqWeekDayReportModel()
        return report
    
    