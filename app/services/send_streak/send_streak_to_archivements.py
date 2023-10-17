from app.graphql.mutations import UpDateStreakMutation, Streak, UpDateStreak
from app.graphql.graphql_client import GraphQLClient
from app.models.statistics_db_models import ReportDocument
from app.exceptions.exceptions import GraphqlMutationError

async def send_streak_to_archivements(report_doc: ReportDocument):
    last_streak = Streak(**report_doc.report.streaks.data[-1].model_dump())
    update_streak = UpDateStreak(
        freq_type=report_doc.hab_freq_type,
        hab_id=report_doc.hab_id,
        streak=last_streak,
    )
    mutation = UpDateStreakMutation(update_streak)

    client = GraphQLClient()
    for i in range(3):
        try:
            result = await client.execute(*mutation.get_mutation())
            if result:
                break
        except Exception as e:
            if i == 2:
                raise GraphqlMutationError("Failed to update streak after 3 attempts")