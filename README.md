# Habit Report Endpoints

The following API endpoints are available for retrieving reports on habits:

* `GET /measure/resume/{hab_id}`
  * Description: Get the resume of the measure for the habit with the given ID.
  * Response model: `md.HabitMeasureResumeReportModel`

* `GET /measure/history/{hab_id}`
  * Description: Get the history of the measure for the habit with the given ID.
  * Response model: `md.HabitMeasureHistoryReportModel`

* `GET /yn/resume/{hab_id}`
  * Description: Get the resume of the yes/no entries for the habit with the given ID.
  * Response model: `md.HabitYNResumeReportModel`

* `GET /yn/history/{hab_id}`
  * Description: Get the history of the yes/no entries for the habit with the given ID.
  * Response model: `md.HabitYNHistoryReportModel`

* `GET /yn/streaks/{hab_id}`
  * Description: Get the best streak of yes/no entries for the habit with the given ID.
  * Response model: `md.HabitYNBestStreakReportModel`

* `GET /freq_week_day/{hab_id}`
  * Description: Get the frequency of the habit on each day of the week for the habit with the given ID.
  * Response model: `md.HabitFreqWeekDayReportModel`