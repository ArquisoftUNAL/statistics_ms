import datetime as dt

def date_to_datetime(date):
    time = dt.time.min
    return dt.datetime.combine(date, time)