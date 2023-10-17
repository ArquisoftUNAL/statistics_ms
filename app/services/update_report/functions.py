import app.models.report_models as rm
from app.models.queue_msgs import NewHabitData
from app.utils.frequency import freq_streaks
from app.utils.date_to_datetime import date_to_datetime

# Functions for update measure habits

## Update progress


## Update history
async def update_ms_day_history(
    day: rm.ListDateValue, newData: NewHabitData
) -> rm.ListDateValue:
    day.data.append(
        rm.DateValue(
            year=newData.hab_dat_collected_at.year,
            month=newData.hab_dat_collected_at.month,
            day=newData.hab_dat_collected_at.day,
            value=newData.hab_dat_amount,
        )
    )
    return day


async def update_ms_week_history(
    week: rm.ListDateValue, newData: NewHabitData
) -> rm.ListDateValue:
    last_week = week.data[-1]

    if (
        last_week.year == newData.hab_dat_collected_at.year
        and last_week.week == newData.hab_dat_collected_at.isocalendar()[1]
    ):
        last_week.value += newData.hab_dat_amount
    else:
        week.data.append(
            rm.DateValue(
                year=newData.hab_dat_collected_at.year,
                week=newData.hab_dat_collected_at.isocalendar()[1],
                value=newData.hab_dat_amount,
            )
        )
    return week


async def update_ms_month_history(
    month: rm.ListDateValue, newData: NewHabitData
) -> rm.ListDateValue:
    last_month = month.data[-1]

    if (
        last_month.year == newData.hab_dat_collected_at.year
        and last_month.month == newData.hab_dat_collected_at.month
    ):
        last_month.value += newData.hab_dat_amount
    else:
        month.data.append(
            rm.DateValue(
                year=newData.hab_dat_collected_at.year,
                month=newData.hab_dat_collected_at.month,
                value=newData.hab_dat_amount,
            )
        )
    return month


async def update_ms_semester_history(
    semester: rm.ListDateValue, newData: NewHabitData
) -> rm.ListDateValue:
    last_semester = semester.data[-1]

    if (
        last_semester.year == newData.hab_dat_collected_at.year
        and last_semester.semester == newData.hab_dat_collected_at.month // 6
    ):
        last_semester.value += newData.hab_dat_amount
    else:
        semester.data.append(
            rm.DateValue(
                year=newData.hab_dat_collected_at.year,
                semester=newData.hab_dat_collected_at.month // 6,
                value=newData.hab_dat_amount,
            )
        )
    return semester


async def update_ms_year_history(
    year: rm.ListDateValue, newData: NewHabitData
) -> rm.ListDateValue:
    last_year = year.data[-1]

    if last_year.year == newData.hab_dat_collected_at.year:
        last_year.value += newData.hab_dat_amount
    else:
        year.data.append(
            rm.DateValue(
                year=newData.hab_dat_collected_at.year,
                value=newData.hab_dat_amount,
            )
        )
    return year


## Update streaks
async def update_ms_streaks(
    streaks: rm.ListHabitStreak, freq: int, newData: NewHabitData
) -> rm.ListHabitStreak:
    freq = freq_streaks[freq]
    last_streak = streaks.data[-1]
    last_streak_end_date = last_streak.end_date
    date = date_to_datetime(newData.hab_dat_collected_at)
    diff_date = date - last_streak_end_date

    if diff_date.days <= freq:
        last_streak.end_date = date
        last_streak.quantity += newData.hab_dat_amount

    else:
        streaks.data.append(
            rm.HabitStreak(
                start_date=date,
                end_date=date,
                quantity=newData.hab_dat_amount,
            )
        )

    return streaks


# Functions for update yes/no habits


## Update history
async def update_yn_week_history(
    week: rm.ListDateCount, newData: NewHabitData
) -> rm.ListDateCount:
    last_week = week.data[-1]

    if (
        last_week.year == newData.hab_dat_collected_at.year
        and last_week.week == newData.hab_dat_collected_at.isocalendar()[1]
    ):
        last_week.count += 1
    else:
        week.data.append(
            rm.DateCount(
                year=newData.hab_dat_collected_at.year,
                week=newData.hab_dat_collected_at.isocalendar()[1],
                count=1,
            )
        )
    return week


async def update_yn_month_history(
    month: rm.ListDateCount, newData: NewHabitData
) -> rm.ListDateCount:
    last_month = month.data[-1]

    if (
        last_month.year == newData.hab_dat_collected_at.year
        and last_month.month == newData.hab_dat_collected_at.month
    ):
        last_month.count += 1
    else:
        month.data.append(
            rm.DateCount(
                year=newData.hab_dat_collected_at.year,
                month=newData.hab_dat_collected_at.month,
                count=1,
            )
        )
    return month


async def update_yn_semester_history(
    semester: rm.ListDateCount, newData: NewHabitData
) -> rm.ListDateCount:
    last_semester = semester.data[-1]

    if (
        last_semester.year == newData.hab_dat_collected_at.year
        and last_semester.semester == newData.hab_dat_collected_at.month // 6
    ):
        last_semester.count += 1
    else:
        semester.data.append(
            rm.DateCount(
                year=newData.hab_dat_collected_at.year,
                semester=newData.hab_dat_collected_at.month // 6,
                count=1,
            )
        )
    return semester


async def update_yn_year_history(
    year: rm.ListDateCount, newData: NewHabitData
) -> rm.ListDateCount:
    last_year = year.data[-1]

    if last_year.year == newData.hab_dat_collected_at.year:
        last_year.count += 1
    else:
        year.data.append(
            rm.DateCount(
                year=newData.hab_dat_collected_at.year,
                count=1,
            )
        )
    return year


## Update streaks
async def update_yn_streaks(
    streaks: rm.ListHabitStreak, freq: int, newData: NewHabitData
) -> rm.ListHabitStreak:
    freq = freq_streaks[freq]
    last_streak = streaks.data[-1]
    last_streak_end_date = last_streak.end_date
    date = date_to_datetime(newData.hab_dat_collected_at)
    diff_date = date - last_streak_end_date

    if diff_date.days <= freq:
        last_streak.end_date = date
        last_streak.quantity += 1

    else:
        streaks.data.append(
            rm.HabitStreak(
                start_date=date,
                end_date=date,
                quantity=1,
            )
        )

    return streaks


# Functions for update frequency habits
async def update_freq_week_day(
    freq_week_day: rm.ListHabitFreqWeekDay, newData: NewHabitData
) -> rm.ListHabitFreqWeekDay:
    last_freq_week_day = freq_week_day.data[-1]

    if (
        last_freq_week_day.year == newData.hab_dat_collected_at.year
        and last_freq_week_day.month == newData.hab_dat_collected_at.month
        and last_freq_week_day.week_day == newData.hab_dat_collected_at.isocalendar()[2]
    ):
        last_freq_week_day.quantity += 1
    else:
        freq_week_day.data.append(
            rm.HabitFreqWeekDay(
                year=newData.hab_dat_collected_at.year,
                month=newData.hab_dat_collected_at.month,
                week_day=newData.hab_dat_collected_at.isocalendar()[2],
                quantity=1,
            )
        )
    return freq_week_day
