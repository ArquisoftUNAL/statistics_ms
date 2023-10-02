import logging
from .exceptions import (
    AppConnectionError,
    AppDatabaseError,
    HabitNotFoundError,
)

def handle_exception(e: Exception):
    if isinstance(e, AppConnectionError):
        logging.error(f"Connection error: {e}")
    elif isinstance(e, AppDatabaseError):
        logging.error(f"Database error: {e}")
    elif isinstance(e, HabitNotFoundError):
        logging.error(f"Habit not found: {e}")
    else:
        logging.error(f"Unknown error: {e}")
