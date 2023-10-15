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
            report_doc = CreateHabitReport(self.hab_repo, self.stat_repo).create_habit_report(
                new_hab_data.hab_id
            )
            report = report_doc.report

        elif report_doc.hab_is_yn:
            report = await self.update_habit_yn_report(
                report_doc.report, report_doc.hab_data_count, new_hab_data
            )
        else:
            report = await self.update_habit_measure_report(
                report_doc.report, report_doc.hab_data_count, new_hab_data
            )
        
        await self.stat_repo.update_report(report_doc.hab_id, report)

        streaks = dict(report.streaks)
        keys = streaks.keys()
        last_key = keys[0]

        for key in keys:
            if key[1] > last_key[1]:
                last_key = key

        start_date, end_date = last_key
        value = streaks[last_key]
        last_streak = Streak(
            date_start=start_date,
            date_end=end_date,
            data=value,
        )
        update_streak = UpDateStreak(
            freq_type=report_doc.hab_freq_type,
            hab_id=report_doc.hab_id,
            streak=last_streak
        )
        mutation = UpDateStreakMutation(update_streak)

        client = GraphQLClient()
        client.execute(*mutation.get_mutation())


    async def update_habit_yn_report(
        self, report: rm.HabitYNReport, count: int, new_hab_data: HabDataCollected
    ) -> rm.HabitYNReport:
        return rm.HabitYNReport(
            resume=await self.update_habit_yn_resume(
                report.resume, count, new_hab_data
            ),
            history=await self.update_habit_yn_history(
                report.history, count, new_hab_data
            ),
            streaks=await self.update_habit_yn_streaks(
                report.streaks, count, new_hab_data
            ),
            days_frequency=await self.update_habit_freq_week_day(
                report.days_frequency, count, new_hab_data
            ),
        )

    async def update_habit_measure_report(
        self, report: rm.HabitMeasureReport, count: int, new_hab_data: HabDataCollected
    ) -> rm.HabitMeasureReport:
        return rm.HabitMeasureReport(
            resume=await self.update_habit_measure_resume(
                report.resume, count, new_hab_data
            ),
            history=await self.update_habit_measure_history(
                report.history, count, new_hab_data
            ),
            streaks=await self.update_habit_measure_streaks(
                report.streaks, count, new_hab_data
            ),
            days_frequency=await self.update_habit_freq_week_day(
                report.days_frequency, count, new_hab_data
            ),
        )

    async def update_habit_measure_resume(
        self, report: rm.HabitMeasureResume, count: int, new_hab_data: HabDataCollected
    ) -> rm.HabitMeasureResume:
        pass

    async def update_habit_measure_history(
        self, report: rm.HabitMeasureHistory, count: int, new_hab_data: HabDataCollected
    ) -> rm.HabitMeasureHistory:
        pass

    async def update_habit_measure_streaks(
        self, report: rm.ListHabitStreak, count: int, new_hab_data: HabDataCollected
    ) -> rm.ListHabitStreak:
        pass

    async def update_habit_yn_resume(
        self, report: rm.HabitYNResume, count: int, new_hab_data: HabDataCollected
    ) -> rm.HabitYNResume:
        pass

    async def update_habit_yn_history(
        self, report: rm.HabitYNHistory, count: int, new_hab_data: HabDataCollected
    ) -> rm.HabitYNHistory:
        pass

    async def update_habit_yn_streaks(
        self, report: rm.ListHabitStreak, count: int, new_hab_data: HabDataCollected
    ) -> rm.ListHabitStreak:
        pass

    async def update_habit_freq_week_day(
        self, report: rm.HabitFreqWeekDay, count: int, new_hab_data: HabDataCollected
    ) -> rm.HabitFreqWeekDay:
        pass
