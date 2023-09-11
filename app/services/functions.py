import pandas as pd
from datetime import date
import calendar
import app.models.report_models as rm

#Functions for get_habit_measure_resume report:
def day_progress(df: pd.DataFrame, goal: int, today: date) -> rm.DataReportModel:    
    if df['hab_dat_collected_at'].iloc[0] == today:
        progress = df['hab_dat_amount'].iloc[0]
        return rm.DataReportModel(
            percentage=progress / goal,
            progress=progress,
            remaining=goal - progress,
        )
    else:
        return None
    
def week_progress(data_frame: pd.DataFrame, goal: int, today: date, freq_type: int) -> rm.DataReportModel:
    year, week, _ = today.isocalendar()
    df = data_frame[(data_frame['year'] == year) & (data_frame['week'] == week)]

    if df.empty:
        return None
    
    progress = df['hab_dat_amount'].sum()

    if freq_type == 1:
        goal = goal * 7

    return rm.DataReportModel(
        percentage=progress / goal,
        progress=progress,
        remaining=goal - progress,
    )

def month_progress(data_frame: pd.DataFrame, goal: int, today: date, freq_type: int) -> rm.DataReportModel:
    year, *_ = today.isocalendar()
    month = today.month
    df = data_frame[(data_frame['year'] == year) & (data_frame['month'] == month)]
    if df.empty:
        return None
    
    progress = df['hab_dat_amount'].sum()
    month_days = calendar.monthrange(year, month)[1]
    if freq_type == 1:
        goal = goal * month_days
    if freq_type == 2:
        goal = goal * month_days / 7

    return rm.DataReportModel(
        percentage=progress / goal,
        progress=progress,
        remaining=goal - progress,
    )

def semester_progress(df: pd.DataFrame, goal: int, today: date, freq_type: int) -> rm.DataReportModel:
    year, *_ = today.isocalendar()
    month = today.month
    if month <= 6:
        df = df[(df['year'] == year) & (df['month'] <= 6)]
    else:
        df = df[(df['year'] == year) & (df['month'] > 6)]

    if df.empty:
        return None
    
    progress = df['hab_dat_amount'].sum()
    if freq_type == 1:
        goal = goal * 365 / 2
    if freq_type == 2:
        goal = goal * 52 / 2
    if freq_type == 3:
        goal = goal * 12 / 2

    return rm.DataReportModel(
        percentage=progress / goal,
        progress=progress,
        remaining=goal - progress,
    )

def year_progress(df: pd.DataFrame, goal: int, today: date, freq_type: int) -> rm.DataReportModel:
    year, *_ = today.isocalendar()
    df = df[(df['year'] == year)]

    if df.empty:
        return None
    
    progress = df['hab_dat_amount'].sum()
    if freq_type == 1:
        goal = goal * 365
    if freq_type == 2:
        goal = goal * 52
    if freq_type == 3:
        goal = goal * 12

    return rm.DataReportModel(
        percentage=progress / goal,
        progress=progress,
        remaining=goal - progress,
    )

#Functions for get_habit_measure_history report:
def ms_day_history(df: pd.DataFrame) -> rm.DateFloatDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount']]
    df = df.set_index('hab_dat_collected_at')
    df = df.sort_index()
    return rm.DateFloatDir(data=df.to_dict()['hab_dat_amount'])

def ms_week_history(df: pd.DataFrame) -> rm.DateFloatDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'week']]
    df = df.set_index('hab_dat_collected_at')
    df = df.sort_index()
    df = df.groupby(['year', 'week']).sum()
    return rm.DateFloatDir(data=df.to_dict()['hab_dat_amount'])

def ms_month_history(df: pd.DataFrame) -> rm.DateFloatDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'month']]
    df = df.set_index('hab_dat_collected_at')
    df = df.sort_index()
    df = df.groupby(['year', 'month']).sum()
    return rm.DateFloatDir(data=df.to_dict()['hab_dat_amount'])

def ms_semester_history(df: pd.DataFrame) -> rm.DateFloatDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'month']]
    df = df.set_index('hab_dat_collected_at')
    df = df.sort_index()
    df = df.groupby(['year', 'month']).sum()
    df['semester'] = df['month'].apply(lambda x: 1 if x <= 6 else 2)
    df = df.groupby(['year', 'semester']).sum()
    return rm.DateFloatDir(data=df.to_dict()['hab_dat_amount'])

def ms_year_history(df: pd.DataFrame) -> rm.DateFloatDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year']]
    df = df.set_index('hab_dat_collected_at')
    df = df.sort_index()
    df = df.groupby(['year']).sum()
    return rm.DateFloatDir(data=df.to_dict()['hab_dat_amount'])

#Functions for get_habit_yn_resume report:
def month_yn_resume(df: pd.DataFrame, goal: int, today: date) -> float:
    return 0.0

def semester_yn_resume(df: pd.DataFrame, goal: int, today: date) -> float:
    return 0.0

def year_yn_resume(df: pd.DataFrame, goal: int, today: date) -> float:
    return 0.0

def total_yn_resume(df: pd.DataFrame, today:date) -> int:
    df = df[df['hab_dat_collected_at'] == today.year]
    return df['hab_dat_amount'].sum()

#Functions for get_habit_yn_history report:
def yn_week_history(df: pd.DataFrame) -> rm.DateIntDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'week']]
    df = df.set_index('hab_dat_collected_at')
    df = df.sort_index()
    df = df.groupby(['year', 'week']).sum()
    return rm.DateIntDir(data=df.to_dict()['hab_dat_amount'])

def yn_month_history(df: pd.DataFrame) -> rm.DateIntDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'month']]
    df = df.set_index('hab_dat_collected_at')
    df = df.sort_index()
    df = df.groupby(['year', 'month']).sum()
    return rm.DateIntDir(data=df.to_dict()['hab_dat_amount'])

def yn_semester_history(df: pd.DataFrame) -> rm.DateIntDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'month']]
    df = df.set_index('hab_dat_collected_at')
    df = df.sort_index()
    df = df.groupby(['year', 'month']).sum()
    df['semester'] = df['month'].apply(lambda x: 1 if x <= 6 else 2)
    df = df.groupby(['year', 'semester']).sum()
    return rm.DateIntDir(data=df.to_dict()['hab_dat_amount'])

def yn_year_history(df: pd.DataFrame) -> rm.DateIntDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year']]
    df = df.set_index('hab_dat_collected_at')
    df = df.sort_index()
    df = df.groupby(['year']).sum()
    return rm.DateIntDir(data=df.to_dict()['hab_dat_amount'])

#Functions for get_habit_yn_best_streak report:
def yn_streaks(df: pd.DataFrame, today: date) -> rm.HabitYNBestStreakReportModel:
    df = df[['hab_dat_collected_at', 'hab_dat_amount']].where(df['year'] == today.year).dropna()
    df['diff_days'] = df['hab_dat_collected_at'].diff().dt.days
    df['streak'] = (df['diff_days'] != 1).cumsum()
    streaks = df.groupby('streak')['hab_dat_collected_at'].count()
    streak_start_end = df.groupby('streak')['hab_dat_collected_at'].agg(['min', 'max'])
    streaks = streaks.to_frame(name='count').join(streak_start_end)
    streaks.rename(columns={'min': 'start_date', 'max': 'end_date'}, inplace=True)
    streaks.set_index(['start_date', 'end_date'], inplace=True)
    streaks = streaks.sort_index(ascending=False)
    streaks = streaks.to_dict()['count']
    return rm.HabitYNBestStreakReportModel(data=streaks)

#Functions for get_habit_freq_week_per_day report:
def freq_week_day(df: pd.DataFrame) -> rm.HabitFreqWeekDayReportModel:
    df = df[['year', 'month', 'weekday']]
    df = df.groupby(['year', 'month', 'weekday']).count()
    df = df.to_frame(name='count').reset_index().groupby(['year', 'month'])[['weekday', 'count']]
    df = df.apply(lambda x: dict(x.values)).to_dict()
    return rm.HabitFreqWeekDayReportModel(data=df)