import logging
from pymongo.errors import WriteError
from app.repositories.interfaces.habits_repository_interface import (
    AbstractHabitReposiory,
)
from app.repositories.interfaces.statistic_repository_interface import (
    AbstractStatisticRepository,
)
from app.services.create_report.create_report import CreateHabitReport
from app.models.habits_db_models import HabDataCollected
from app.graphql.graphql_client import GraphQLClient
from app.graphql.mutations import UpDateStreakMutation, Streak, UpDateStreak
import app.models.report_models as rm
from app.utils.frequency import freq_types
from . import functions as fn


class UpdateReport:
    def __init__(
        self,
        habit_repository: AbstractHabitReposiory,
        statistic_repository: AbstractStatisticRepository,
    ):
        self.hab_repo = habit_repository
        self.stat_repo = statistic_repository

    async def update_habit_report(self, new_hab_data: HabDataCollected):
        report_doc = await self.stat_repo.get_report_by_id(new_hab_data.hab_id)
        if report_doc is None:
            create_habit = CreateHabitReport(self.hab_repo, self.stat_repo)
            report_doc = await create_habit.create_habit_report(new_hab_data.hab_id)

        if report_doc is not None:
            if report_doc.hab_is_yn:
                report = await self.update_habit_yn_report(
                    report_doc.report,
                    report_doc.hab_data_count,
                    report_doc.hab_freq_type,
                    new_hab_data,
                )
                report_doc.report = report
            else:
                report = await self.update_habit_measure_report(
                    report_doc.report,
                    report_doc.hab_data_count,
                    report_doc.hab_freq_type,
                    new_hab_data,
                )
                report_doc.report = report
            try:
                await self.stat_repo.update_report(report_doc.hab_id, report_doc.report)
            except WriteError as e:
                logging.error(f"Error updating report on statistics database: {e}")

        return report_doc

    async def update_habit_yn_report(
        self,
        report: rm.HabitYNReport,
        count: int,
        freq: str,
        new_hab_data: HabDataCollected,
    ) -> rm.HabitYNReport:
        freqn = freq_types[freq]
        return rm.HabitYNReport(
            resume=await self.update_habit_yn_resume(
                report.resume, count, new_hab_data
            ),
            history=await self.update_habit_yn_history(report.history, new_hab_data),
            streaks=await self.update_habit_yn_streaks(
                report.streaks, freqn, new_hab_data
            ),
            days_frequency=await self.update_habit_freq_week_day(
                report.days_frequency, count, new_hab_data
            ),
        )

    async def update_habit_measure_report(
        self,
        report: rm.HabitMeasureReport,
        count: int,
        freq: str,
        new_hab_data: HabDataCollected,
    ) -> rm.HabitMeasureReport:
        freqn = freq_types[freq]
        return rm.HabitMeasureReport(
            resume=await self.update_habit_measure_resume(
                report.resume, count, new_hab_data
            ),
            history=await self.update_habit_measure_history(
                report.history, new_hab_data
            ),
            streaks=await self.update_habit_measure_streaks(
                report.streaks, freqn, new_hab_data
            ),
            days_frequency=await self.update_habit_freq_week_day(
                report.days_frequency, count, new_hab_data
            ),
        )

    async def update_habit_measure_resume(
        self, resume: rm.HabitMeasureResume, count: int, new_hab_data: HabDataCollected
    ) -> rm.HabitMeasureResume:
        return resume

    async def update_habit_measure_history(
        self, history: rm.HabitMeasureHistory, new_hab_data: HabDataCollected
    ) -> rm.HabitMeasureHistory:
        history.day = await fn.update_ms_day_history(history.day, new_hab_data)
        history.week = await fn.update_ms_week_history(history.week, new_hab_data)
        history.month = await fn.update_ms_month_history(history.month, new_hab_data)
        history.semester = await fn.update_ms_semester_history(
            history.semester, new_hab_data
        )
        history.year = await fn.update_ms_year_history(history.year, new_hab_data)

        return history

    async def update_habit_measure_streaks(
        self, streaks: rm.ListHabitStreak, freq: int, new_hab_data: HabDataCollected
    ) -> rm.ListHabitStreak:
        streaks = await fn.update_ms_streaks(streaks, freq, new_hab_data)

        return streaks

    async def update_habit_yn_resume(
        self, resume: rm.HabitYNResume, count: int, new_hab_data: HabDataCollected
    ) -> rm.HabitYNResume:
        return resume

    async def update_habit_yn_history(
        self, history: rm.HabitYNHistory, new_hab_data: HabDataCollected
    ) -> rm.HabitYNHistory:
        history.week = await fn.update_yn_week_history(history.week, new_hab_data)
        history.month = await fn.update_yn_month_history(history.month, new_hab_data)
        history.semester = await fn.update_yn_semester_history(
            history.semester, new_hab_data
        )
        history.year = await fn.update_yn_year_history(history.year, new_hab_data)

        return history

    async def update_habit_yn_streaks(
        self, streaks: rm.ListHabitStreak, count: int, new_hab_data: HabDataCollected
    ) -> rm.ListHabitStreak:
        streaks = await fn.update_yn_streaks(streaks, count, new_hab_data)

        return streaks

    async def update_habit_freq_week_day(
        self,
        freq_week_day: rm.ListHabitFreqWeekDay,
        count: int,
        new_hab_data: HabDataCollected,
    ) -> rm.ListHabitFreqWeekDay:
        freq_week_day = await fn.update_freq_week_day(
            freq_week_day, new_hab_data
        )

        return freq_week_day
