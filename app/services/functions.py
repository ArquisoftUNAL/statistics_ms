import pandas as pd
from datetime import date
import calendar
import app.models.report_models as rm

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

def day_history(df: pd.DataFrame) -> rm.DateFloatDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount']]
    df = df.set_index('hab_dat_collected_at')
    df = df.sort_index()
    return rm.DateFloatDir(data=df.to_dict()['hab_dat_amount'])

def week_history(df: pd.DataFrame) -> rm.DateFloatDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'week']]
    df = df.set_index('hab_dat_collected_at')
    df = df.sort_index()
    df = df.groupby(['year', 'week']).sum()
    return rm.DateFloatDir(data=df.to_dict()['hab_dat_amount'])

def month_history(df: pd.DataFrame) -> rm.DateFloatDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'month']]
    df = df.set_index('hab_dat_collected_at')
    df = df.sort_index()
    df = df.groupby(['year', 'month']).sum()
    return rm.DateFloatDir(data=df.to_dict()['hab_dat_amount'])

def semester_history(df: pd.DataFrame) -> rm.DateFloatDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year', 'month']]
    df = df.set_index('hab_dat_collected_at')
    df = df.sort_index()
    df = df.groupby(['year', 'month']).sum()
    df['semester'] = df['month'].apply(lambda x: 1 if x <= 6 else 2)
    df = df.groupby(['year', 'semester']).sum()
    return rm.DateFloatDir(data=df.to_dict()['hab_dat_amount'])

def year_history(df: pd.DataFrame) -> rm.DateFloatDir:
    df = df[['hab_dat_collected_at', 'hab_dat_amount', 'year']]
    df = df.set_index('hab_dat_collected_at')
    df = df.sort_index()
    df = df.groupby(['year']).sum()
    return rm.DateFloatDir(data=df.to_dict()['hab_dat_amount'])

