import logging
from datetime import date, datetime
from uuid import UUID
from typing import Union
from pymongo.errors import WriteError
from app.repositories.interfaces.habits_repository_interface import (
    AbstractHabitReposiory,
)
from app.repositories.interfaces.statistic_repository_interface import (
    AbstractStatisticRepository,
)
from app.models.habits_db_models import HabData
from app.models.statistics_db_models import ReportDocument
import app.models.report_models as rm
from app.utils.frequency import freq_types
from . import functions as fn


class CreateHabitReport:
    def __init__(
        self,
        habit_repository: AbstractHabitReposiory,
        statistic_repository: AbstractStatisticRepository,
    ):
        self.hab_repo = habit_repository
        self.stat_repo = statistic_repository

    async def create_habit_report(
        self, hab_id: UUID
    ) -> Union[ReportDocument, None]:
        habit_data = await self.hab_repo.get_habit_data(hab_id)
        if habit_data is None:
            return None

        if habit_data.hab.hab_is_yn:
            report_doc = await self.create_habit_yn_report(hab_id, habit_data)
        else:
            report_doc = await self.create_habit_measure_report(hab_id, habit_data)

        try:
            await self.stat_repo.create_report(report_doc)
            return report_doc
        except WriteError as e:
            logging.error(f"Error creating report on statistics database: {e}")
            return None

    async def create_habit_yn_report(
        self, hab_id: UUID, habit_data: HabData
    ) -> ReportDocument:
        if habit_data.data.empty:
            report = await fn.create_empty_habit_yn_report()
        else:
            report = rm.HabitYNReport(
                resume=await self.create_habit_yn_resume(habit_data),
                history=await self.create_habit_yn_history(habit_data),
                streaks=await self.create_habit_yn_streaks(habit_data),
                days_frequency=await self.create_habit_freq_week_day(habit_data),
            )

        report_doc = ReportDocument(
            hab_id=hab_id,
            hab_is_yn=True,
            hab_freq_type=habit_data.hab.hab_freq_type,
            hab_data_count=habit_data.data.shape[0],
            report=report,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return report_doc

    async def create_habit_measure_report(
        self, hab_id: UUID, habit_data: HabData
    ) -> ReportDocument:
        if habit_data.data.empty:
            report = await fn.create_empty_habit_measure_report()
        else:
            report = rm.HabitMeasureReport(
                resume=await self.create_habit_measure_resume(habit_data),
                history=await self.create_habit_measure_history(habit_data),
                streaks=await self.create_habit_measure_streaks(habit_data),
                days_frequency=await self.create_habit_freq_week_day(habit_data),
            )

        report_doc = ReportDocument(
            hab_id=hab_id,
            hab_is_yn=False,
            hab_freq_type=habit_data.hab.hab_freq_type,
            hab_goal=habit_data.hab.hab_goal,
            hab_data_count=habit_data.data.shape[0],
            report=report,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return report_doc

    async def create_habit_measure_resume(
        self, habit_data: HabData
    ) -> rm.HabitMeasureResume:
        """
        Calculates the progress of a habit with a measure type frequency.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitMeasureResume: The report with the progress of the habit.
        """
        today = date.today()
        goal = habit_data.hab.hab_goal
        if goal is None:
            goal = 0
        freq_type = freq_types[habit_data.hab.hab_freq_type]
        df = habit_data.data
        year = await fn.year_progress(df, goal, today, freq_type)

        semester = await fn.semester_progress(df, goal, today, freq_type)
        month = (
            await fn.month_progress(df, goal, today, freq_type)
            if freq_type < 6
            else None
        )
        week = (
            await fn.week_progress(df, goal, today, freq_type)
            if freq_type < 4
            else None
        )
        today = await fn.day_progress(df, goal, today) if freq_type == 1 else None

        report = rm.HabitMeasureResume(
            toDay=today, week=week, month=month, semester=semester, year=year
        )

        return report

    async def create_habit_measure_history(
        self, habit_data: HabData
    ) -> rm.HabitMeasureHistory:
        """
        Calculates the history of a habit with a measure type frequency.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitMeasureHistory: The report with the history of the habit.
        """
        df = habit_data.data

        year = await fn.ms_year_history(df)
        semester = await fn.ms_semester_history(df)
        month = await fn.ms_month_history(df)
        week = await fn.ms_week_history(df)
        day = await fn.ms_day_history(df)

        report = rm.HabitMeasureHistory(
            day=day, week=week, month=month, semester=semester, year=year
        )

        return report

    async def create_habit_measure_streaks(
        self, habit_data: HabData
    ) -> rm.ListHabitStreak:
        """
        Calculates the best streak of a habit with a measure type frequency.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            ListHabitStreak: The report with the best streak of the habit.
        """
        freq_type = freq_types[habit_data.hab.hab_freq_type]
        df = habit_data.data

        return await fn.ms_streaks(df, freq_type)

    async def create_habit_yn_resume(self, habit_data: HabData) -> rm.HabitYNResume:
        """
        Calculates the progress of a habit with a yes/no type.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitYNResume: The report with the progress of the habit.
        """
        today = date.today()
        df = habit_data.data
        freq_type = freq_types[habit_data.hab.hab_freq_type]

        year = await fn.year_yn_resume(df, freq_type, today)
        semester = await fn.semester_yn_resume(df, freq_type, today)
        month = await fn.month_yn_resume(df, freq_type, today)
        total = await fn.total_yn_resume(df, today)

        report = rm.HabitYNResume(
            month=month, semester=semester, year=year, total=total
        )
        return report

    async def create_habit_yn_history(self, habit_data: HabData) -> rm.HabitYNHistory:
        """
        Calculates the history of a habit with a yes/no type.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitYNHistory: The report with the history of the habit.
        """
        df = habit_data.data

        year = await fn.yn_year_history(df)
        semester = await fn.yn_semester_history(df)
        month = await fn.yn_month_history(df)
        week = await fn.yn_week_history(df)

        report = rm.HabitYNHistory(week=week, month=month, semester=semester, year=year)

        return report

    async def create_habit_yn_streaks(self, habit_data: HabData) -> rm.ListHabitStreak:
        """
        Calculates the best streak of a habit with a yes/no type.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitYNBestStreak: The report with the best streak of the habit.
        """
        freq_type = freq_types[habit_data.hab.hab_freq_type]
        df = habit_data.data
        return await fn.yn_streaks(df, freq_type)

    async def create_habit_freq_week_day(
        self, habit_data: HabData
    ) -> rm.HabitFreqWeekDay:
        """
        Calculates the frequency of a habit with a week day type.

        Args:
            hab_id (int): The id of the habit.

        Returns:
            HabitFreqWeekDay: The report with the frequency of the habit.
        """
        df = habit_data.data
        report = await fn.freq_week_day(df)

        return report
