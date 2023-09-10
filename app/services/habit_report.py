from app.repositories.habits_repository import HabitRepository
import app.models.report_models as md
from datetime import date, timedelta

freq_types = {
    1: 'daily',
    2: 'weekly',
    3: 'monthly',
}


class HabitReport:
    def __init__(self, habit_repository: HabitRepository):
        self.repo = habit_repository()

    def get_habit_measure_resume(self, hab_id: int):
        habit_data = self.repo.habit_data(hab_id)
        today = date.today()
        yn = habit_data[0]
        freq_type = habit_data[2]
        goal = habit_data[3]
        freq_date = habit_data[4]
        data = habit_data[5]

        report = md.HabitMeasureResumeReportModel()
        if freq_type == freq_types[1]:
            if data['hab_dat_collected_at'].iloc[0] == today:
                report.toDay = md.DataReportModel(
                    percentage=data['hab_dat_amount'].iloc[0] / goal,
                    progress=data['hab_dat_amount'].iloc[0],
                    remaining=goal - data['hab_dat_amount'].iloc[0],
                )
        elif freq_type == freq_types[2]:
            #get the first day of the actual week at the dataframe if exists
            first_date = data['hab_dat_collected_at'].iloc[0]
            year, week, weekday = first_date.isocalendar()
            if year == today.year and week == today.isocalendar()[1]:
                week = date.fromisocalendar(year, week, 1)
                if first_date < week:
                    week -= timedelta(days=7)
            else:
                week = first_date - timedelta(days=weekday - 1)

        return report
    
    def get_habit_measure_history(self, hab_id: int):
        habit_data = self.repo.habit_data(hab_id)
        report = md.HabitMeasureHistoryReportModel()
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
    
    