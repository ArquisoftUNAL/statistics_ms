class AppDatabaseError(Exception):
    pass

class AppConnectionError(AppDatabaseError):
    pass

class HabitNotFoundError(Exception):
    pass
