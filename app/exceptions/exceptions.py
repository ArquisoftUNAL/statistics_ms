class AppDatabaseError(Exception):
    pass

class AppConnectionError(AppDatabaseError):
    pass

class HabitNotFoundError(Exception):
    pass

class GraphqlMutationError(Exception):
    pass
