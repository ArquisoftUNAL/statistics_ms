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
        return rm.DataReportModel(
            percentage=0,
            progress=0,
            remaining=goal,
        )
    
def week_progress(data_frame: pd.DataFrame, goal: int, today: date, freq_type: int) -> rm.DataReportModel:
    year, week, _ = today.isocalendar()
    df = data_frame[(data_frame['year'] == year) & (data_frame['week'] == week)]
    if goal == 0:
        return None

    if df.empty:
        return rm.DataReportModel(
            percentage=0,
            progress=0,
            remaining=goal,
        )
    
    progress = df['hab_dat_amount'].sum()

    if freq_type == 1:
        goal = goal * 7
    if freq_type == 2:
        goal = goal * 7/2

    return rm.DataReportModel(
        percentage=progress / goal,
        progress=progress,
        remaining=goal - progress,
    )

def month_progress(data_frame: pd.DataFrame, goal: int, today: date, freq_type: int) -> rm.DataReportModel:
    year, *_ = today.isocalendar()
    month = today.month

    if goal == 0:
        return None

    df = data_frame[(data_frame['year'] == year) & (data_frame['month'] == month)]
    if df.empty:
        return None
    
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

    return rm.DataReportModel(
        percentage=progress / goal,
        progress=progress,
        remaining=goal - progress,
    )

def semester_progress(df: pd.DataFrame, goal: int, today: date, freq_type: int) -> rm.DataReportModel:
    year, *_ = today.isocalendar()
    month = today.month

    if goal == 0:
        return None

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
        goal = goal * 365 / 4
    if freq_type == 3:
        goal = goal * 52 / 2
    if freq_type == 4:
        goal = goal * 52 / 4
    if freq_type == 5:
        goal = goal * 6
    if freq_type == 6:
        goal = goal * 3

    return rm.DataReportModel(
        percentage=progress / goal,
        progress=progress,
        remaining=goal - progress,
    )

def year_progress(df: pd.DataFrame, goal: int, today: date, freq_type: int) -> rm.DataReportModel:
    year, *_ = today.isocalendar()
    df = df[(df['year'] == year)]

    if goal == 0:
        return None

    if df.empty:
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
    data = df.to_dict()['hab_dat_amount']
    return rm.DateFloatDir(data=data)

def ms_week_history(df: pd.DataFrame) -> rm.DateFloatDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'week']]
    #old_dates = df.groupby(['year', 'week']).min()['hab_dat_collected_at'].astype(str)
    df = df.groupby(['year', 'week'])['hab_dat_amount'].sum()
    data = df.to_dict()
    return rm.DateFloatDir(data=data)

def ms_month_history(df: pd.DataFrame) -> rm.DateFloatDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'month']]
    #old_dates = df.groupby(['year', 'month']).min()['hab_dat_collected_at'].astype(str)
    df = df.groupby(['year', 'month'])['hab_dat_amount'].sum()
    data = df.to_dict()
    return rm.DateFloatDir(data=data)

def ms_semester_history(df: pd.DataFrame) -> rm.DateFloatDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'month']]
    df['semester'] = df['month'].apply(lambda x: 1 if x <= 6 else 2)
    #old_dates = df.groupby(['year', 'semester']).min()['hab_dat_collected_at'].astype(str)
    df = df.groupby(['year', 'semester'])['hab_dat_amount'].sum()
    data = df.to_dict()
    return rm.DateFloatDir(data=data)

def ms_year_history(df: pd.DataFrame) -> rm.DateFloatDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year']]
    #old_dates = df.groupby('year').min()['hab_dat_collected_at'].astype(str)
    df = df.groupby(df['year'])['hab_dat_amount'].sum()
    data = df.to_dict()
    return rm.DateFloatDir(data=data)

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

    progress = df[(df['month'] == month) & (df['year'] == year)].size

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

    progress = df[(df['month'] == month) & (df['year'] == year)].size

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
    progress = df[(df['month'] == month) & (df['year'] == year)].size

    return progress/goal

def total_yn_resume(df: pd.DataFrame, today:date) -> int:
    df = df[df['year'] == today.year]
    return df.shape[0]

#Functions for get_habit_yn_history report:
def yn_week_history(df: pd.DataFrame) -> rm.DateIntDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'week']]
    #old_dates = df.groupby(['year', 'week']).min()['hab_dat_collected_at']
    df = df.groupby(['year', 'week']).count()
    #df.set_index(#old_dates, inplace=True)
    data = df.to_dict()['hab_dat_collected_at']
    return rm.DateIntDir(data=data)

def yn_month_history(df: pd.DataFrame) -> rm.DateIntDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'month']]
    #old_dates = df.groupby(['year', 'month']).min()['hab_dat_collected_at']
    df = df.groupby(['year', 'month']).count()
    #df.set_index(#old_dates, inplace=True)
    data = df.to_dict()['hab_dat_collected_at']
    return rm.DateIntDir(data=data)

def yn_semester_history(df: pd.DataFrame) -> rm.DateIntDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'month']]
    df['semester'] = df['month'].apply(lambda x: 1 if x <= 6 else 2)
    #old_dates = df.groupby(['year', 'semester']).min()['hab_dat_collected_at']
    df = df.groupby(['year', 'semester']).count()
    #df.set_index(#old_dates, inplace=True)
    data = df.to_dict()['hab_dat_collected_at']
    return rm.DateIntDir(data=data)

def yn_year_history(df: pd.DataFrame) -> rm.DateIntDir:
    df = df[['hab_dat_collected_at', 'year']]
    #old_dates = df.groupby('year').min()['hab_dat_collected_at']
    df = df.groupby('year').count()
    #df.set_index(#old_dates, inplace=True)
    data = df.to_dict()['hab_dat_collected_at']
    return rm.DateIntDir(data=data)

#Functions for get_habit_yn_best_streak report:
def yn_streaks(df: pd.DataFrame, today: date) -> rm.HabitYNStreakReportModel:
    df = df[['hab_dat_collected_at', 'hab_dat_amount']].where(df['year'] == today.year).dropna()
    df['diff_days'] = df['hab_dat_collected_at'].diff().dt.days
    df['streak'] = (df['diff_days'] != 1).cumsum()
    streaks = df.groupby('streak')['hab_dat_collected_at'].count()
    streak_start_end = df.groupby('streak')['hab_dat_collected_at'].agg(['min', 'max']).rename(columns={'min': 'start_date', 'max': 'end_date'})
    streaks = streaks.to_frame(name='count').join(streak_start_end)
    streaks.set_index(['start_date', 'end_date'], inplace=True)
    streaks = streaks.sort_index(ascending=False)
    streaks = streaks.to_dict()['count']
    return rm.HabitYNStreakReportModel(data=streaks)

#Functions for get_habit_freq_week_per_day report:
def freq_week_day(df: pd.DataFrame) -> rm.HabitFreqWeekDayReportModel:
    df = df[['year', 'month', 'weekday', 'hab_dat_amount']]
    df = df.groupby(['year', 'month', 'weekday'])['hab_dat_amount'].count()
    df = df.to_frame(name='count').reset_index().groupby(['year', 'month'])[['weekday', 'count']]
    df = df.apply(lambda x: dict(x.values)).to_dict()
    return rm.HabitFreqWeekDayReportModel(data=df)