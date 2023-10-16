import pandas as pd
from datetime import date
import calendar
import app.models.report_models as rm

def create_empty_habit_measure_report() -> rm.HabitMeasureReport:
    return rm.HabitMeasureReport(
        resume=rm.HabitMeasureResume(),
        history=rm.HabitMeasureHistory(
            day=rm.ListDateValue(data=[]),
            week=rm.ListDateValue(data=[]),
            month=rm.ListDateValue(data=[]),
            semester=rm.ListDateValue(data=[]),
            year=rm.ListDateValue(data=[]),
        ),
        streaks=rm.ListHabitStreak(data=[]),
        days_frequency=rm.ListHabitFreqWeekDay(data=[]),
    )

def create_empty_habit_yn_report() -> rm.HabitYNReport:
    return rm.HabitYNReport(
        resume=rm.HabitYNResume(month=0.0, semester=0.0, year=0.0, total=0),
        history=rm.HabitYNHistory(
            week=rm.ListDateCount(data=[]),
            month=rm.ListDateCount(data=[]),
            semester=rm.ListDateCount(data=[]),
            year=rm.ListDateCount(data=[]),
        ),
        streaks=rm.ListHabitStreak(data=[]),
        days_frequency=rm.ListHabitFreqWeekDay(data=[]),
    )

#Functions for get_habit_measure_resume report:
def day_progress(df: pd.DataFrame, goal: int, today: date) -> rm.DataResume:    
    if df['hab_dat_collected_at'].iloc[0] == today:
        progress = df['hab_dat_amount'].iloc[0]
        return rm.DataResume(
            percentage=progress / goal,
            progress=progress,
            remaining=goal - progress,
        )
    else:
        return rm.DataResume(
            percentage=0,
            progress=0,
            remaining=goal,
        )
    
def week_progress(data_frame: pd.DataFrame, goal: int, today: date, freq_type: int) -> rm.DataResume:
    year, week, _ = today.isocalendar()
    df = data_frame[(data_frame['year'] == year) & (data_frame['week'] == week)]
    if goal == 0:
        return None

    if df.empty:
        return rm.DataResume(
            percentage=0,
            progress=0,
            remaining=goal,
        )
    
    progress = df['hab_dat_amount'].sum()

    if freq_type == 1:
        goal = goal * 7
    if freq_type == 2:
        goal = goal * 7/2

    return rm.DataResume(
        percentage=progress / goal,
        progress=progress,
        remaining=goal - progress,
    )

def month_progress(data_frame: pd.DataFrame, goal: int, today: date, freq_type: int) -> rm.DataResume:
    year, *_ = today.isocalendar()
    month = today.month

    if goal == 0:
        return None

    df = data_frame[(data_frame['year'] == year) & (data_frame['month'] == month)]
    
    progress = df['hab_dat_amount'].sum()
    month_days = calendar.monthrange(year, month)[1]
    if freq_type == 1:
        goal = goal * month_days
    if freq_type == 2:
        goal = goal * month_days / 2
    if freq_type == 3:
        goal = goal * month_days / 7
    if freq_type == 4:
        goal = goal * month_days / 7 / 2

    return rm.DataResume(
        percentage=progress / goal,
        progress=progress,
        remaining=goal - progress,
    )

def semester_progress(df: pd.DataFrame, goal: int, today: date, freq_type: int) -> rm.DataResume:
    year, *_ = today.isocalendar()
    month = today.month

    if goal == 0:
        return None

    if month <= 6:
        df = df[(df['year'] == year) & (df['month'] <= 6)]
    else:
        df = df[(df['year'] == year) & (df['month'] > 6)]

    
    progress = df['hab_dat_amount'].sum()
    if freq_type == 1:
        goal = goal * 365 / 2
    if freq_type == 2:
        goal = goal * 365 / 4
    if freq_type == 3:
        goal = goal * 52 / 2
    if freq_type == 4:
        goal = goal * 52 / 4
    if freq_type == 5:
        goal = goal * 6
    if freq_type == 6:
        goal = goal * 3

    return rm.DataResume(
        percentage=progress / goal,
        progress=progress,
        remaining=goal - progress,
    )

def year_progress(df: pd.DataFrame, goal: int, today: date, freq_type: int) -> rm.DataResume:
    year, *_ = today.isocalendar()
    df = df[(df['year'] == year)]

    if goal == 0:
        return None

    progress = df['hab_dat_amount'].sum()
    if freq_type == 1:
        goal = goal * 365
    if freq_type == 2:
        goal = goal * 365 / 2
    if freq_type == 3:
        goal = goal * 52
    if freq_type == 4:
        goal = goal * 52 / 2
    if freq_type == 5:
        goal = goal * 12
    if freq_type == 6:
        goal = goal * 6

    return rm.DataResume(
        percentage=progress / goal,
        progress=progress,
        remaining=goal - progress,
    )

#Functions for get_habit_measure_history report:
def ms_day_history(df: pd.DataFrame) -> rm.ListDateValue:
    df = df[['hab_dat_collected_at', 'hab_dat_amount']]
    list_date = df.apply(lambda row: rm.DateValue(year=row['hab_dat_collected_at'].year, month=row['hab_dat_collected_at'].month, day=row['hab_dat_collected_at'].day, value=row['hab_dat_amount']), axis=1).to_list()
    return rm.ListDateValue(data=list_date)

def ms_week_history(df: pd.DataFrame) -> rm.ListDateValue:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'week']]
    df = df.groupby(['year', 'week'])['hab_dat_amount'].sum().to_frame()
    df.reset_index(inplace=True)
    list_date = df.apply(lambda row: rm.DateValue(year=row['year'], week=row['week'], value=row['hab_dat_amount']), axis=1).to_list()
    return rm.ListDateValue(data=list_date)

def ms_month_history(df: pd.DataFrame) -> rm.ListDateValue:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'month']]
    df = df.groupby(['year', 'month'])['hab_dat_amount'].sum().to_frame()
    df.reset_index(inplace=True)
    list_date = df.apply(lambda row: rm.DateValue(year=row['year'], month=row['month'], value=row['hab_dat_amount']), axis=1).to_list()
    return rm.ListDateValue(data=list_date)

def ms_semester_history(df: pd.DataFrame) -> rm.ListDateValue:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'month']]
    df['semester'] = df['month'].apply(lambda x: 1 if x <= 6 else 2)
    df = df.groupby(['year', 'semester'])['hab_dat_amount'].sum().to_frame()
    df.reset_index(inplace=True)
    list_date = df.apply(lambda row: rm.DateValue(year=row['year'], semester=row['semester'], value=row['hab_dat_amount']), axis=1).to_list()
    return rm.ListDateValue(data=list_date)

def ms_year_history(df: pd.DataFrame) -> rm.ListDateValue:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year']].astype(str)
    df = df.groupby(df['year'])['hab_dat_amount'].sum().to_frame()
    df.reset_index(inplace=True)
    list_date = df.apply(lambda row: rm.DateValue(year=row['year'], value=row['hab_dat_amount']), axis=1).to_list()
    return rm.ListDateValue(data= list_date)

#Functions for get_habit_yn_resume report:
def month_yn_resume(df: pd.DataFrame, freq: int, today: date) -> float:
    year = today.year
    month = today.month
    month_days = calendar.monthrange(year, month)[1]
    goal = 0
    if freq == 1:
        goal = month_days
    if freq == 2:
        goal = month_days/2
    if freq == 3:
        goal = month_days/7
    if freq == 4:
        goal = month_days/14
    if freq == 5:
        goal = 1
    if freq == 6:
        goal = 0.5

    progress = df[(df['month'] == month) & (df['year'] == year)].shape[0]

    return progress/goal

def semester_yn_resume(df: pd.DataFrame, freq: int, today: date) -> float:
    year = today.year
    month = today.month
    goal = 0
    if freq == 1:
        goal = 365/2
    if freq == 2:
        goal = 365/4
    if freq == 3:
        goal = 52/2
    if freq == 4:
        goal = 52/4
    if freq == 5:
        goal = 6
    if freq == 6:
        goal = 3

    progress = df[(df['month'] == month) & (df['year'] == year)].shape[0]

    return progress/goal

def year_yn_resume(df: pd.DataFrame, freq: int, today: date) -> float:
    year = today.year
    month = today.month
    goal = 0
    if freq == 1:
        goal = 365
    if freq == 2:
        goal = 365/2
    if freq == 3:
        goal = 52
    if freq == 4:
        goal = 52/2
    if freq == 5:
        goal = 12
    if freq == 6:
        goal = 6
    progress = df[(df['month'] == month) & (df['year'] == year)].shape[0]

    return progress/goal

def total_yn_resume(df: pd.DataFrame, today:date) -> int:
    df = df[df['year'] == today.year]
    return df.shape[0]

#Functions for get_habit_yn_history report:
def yn_week_history(df: pd.DataFrame) -> rm.ListDateCount:
    df = df[['hab_dat_collected_at', 'year', 'week']].rename(columns={'hab_dat_collected_at': 'count'})
    df = df.groupby(['year', 'week']).count()
    df.reset_index(inplace=True)
    list_date = df.apply(lambda row: rm.DateCount(year=row['year'], week=row['week'], count=row['count']), axis=1).to_list()
    return rm.ListDateCount(data=list_date)

def yn_month_history(df: pd.DataFrame) -> rm.ListDateCount:
    df = df[['hab_dat_collected_at', 'year', 'month']].rename(columns={'hab_dat_collected_at': 'count'})
    df = df.groupby(['year', 'month']).count()
    df.reset_index(inplace=True)
    list_date = df.apply(lambda row: rm.DateCount(year=row['year'], month=row['month'], count=row['count']), axis=1).to_list()
    return rm.ListDateCount(data=list_date)

def yn_semester_history(df: pd.DataFrame) -> rm.ListDateCount:
    df = df[['hab_dat_collected_at', 'year', 'month']].rename(columns={'hab_dat_collected_at': 'count'})
    df['semester'] = df['month'].apply(lambda x: 1 if x <= 6 else 2)
    df = df.groupby(['year', 'semester']).count()
    df.reset_index(inplace=True)
    list_date = df.apply(lambda row: rm.DateCount(year=row['year'], semester=row['semester'], count=row['count']), axis=1).to_list()
    return rm.ListDateCount(data=list_date)

def yn_year_history(df: pd.DataFrame) -> rm.ListDateCount:
    df = df[['hab_dat_collected_at', 'year']].rename(columns={'hab_dat_collected_at': 'count'})
    df = df.groupby('year').count()
    df.reset_index(inplace=True)
    list_date = df.apply(lambda row: rm.DateCount(year=row['year'], count=row['count']), axis=1).to_list()
    return rm.ListDateCount(data=list_date)

#Functions for get_habit_yn_best_streak report:
def yn_streaks(df: pd.DataFrame, freq: int) -> rm.ListHabitStreak:
    if freq == 3: #weekly
        freq = 7
    if freq == 4: #biweekly
        freq = 14
    if freq == 5: #monthly
        freq = 30
    if freq == 6: #bimonthly
        freq = 60

    df = df[['hab_dat_collected_at']]
    df.loc[:, 'diff_days'] = df['hab_dat_collected_at'].diff().dt.days
    df.loc[:, 'streak'] = (df['diff_days'] > freq).cumsum()
    streaks = df.groupby('streak')['hab_dat_collected_at'].count()
    streak_start_end = df.groupby('streak')['hab_dat_collected_at'].agg(['min', 'max']).rename(columns={'min': 'start_date', 'max': 'end_date'})
    streaks = streaks.to_frame(name='count').join(streak_start_end)
    list_streaks = streaks.apply(lambda row: rm.HabitStreak(start_date=row['start_date'], end_date=row['end_date'], quantity=row['count']), axis=1).to_list()
    
    return rm.ListHabitStreak(data=list_streaks)

def ms_streaks(df: pd.DataFrame, freq: int) -> rm.ListHabitStreak:
    if freq == 3: #weekly
        freq = 7
    if freq == 4: #biweekly
        freq = 14
    if freq == 5: #monthly
        freq = 30
    if freq == 6: #bimonthly
        freq = 60

    df = df[['hab_dat_collected_at', 'hab_dat_amount']]
    df['diff_days'] = df['hab_dat_collected_at'].diff().dt.days
    df['streak'] = (df['diff_days'] > freq).cumsum()
    streaks = df.groupby('streak')['hab_dat_amount'].sum()
    streak_start_end = df.groupby('streak')['hab_dat_collected_at'].agg(['min', 'max']).rename(columns={'min': 'start_date', 'max': 'end_date'})
    streaks = streaks.to_frame(name='count').join(streak_start_end)
    list_streaks = streaks.apply(lambda row: rm.HabitStreak(start_date=row['start_date'], end_date=row['end_date'], quantity=row['count']), axis=1).to_list()
    
    return rm.ListHabitStreak(data=list_streaks)

#Functions for get_habit_freq_week_per_day report:
def freq_week_day(df: pd.DataFrame) -> rm.ListHabitFreqWeekDay:
    df = df[['year', 'month', 'weekday', 'hab_dat_amount']]
    df = df.groupby(['year', 'month', 'weekday']).count()
    df.reset_index(inplace=True)
    list_data = df.apply(lambda row: rm.HabitFreqWeekDay(year=row['year'], month=row['month'], week_day=row['weekday'], quantity=row['hab_dat_amount']), axis=1).to_list()
    
    return rm.ListHabitFreqWeekDay(data=list_data)