from sqlalchemy import  URL
from dotenv import load_dotenv
import os

load_dotenv()

HABITS_DB_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
)

API_GATEWAY_URL = f"http://{os.getenv('API_GATEWAY_HOST')}:{os.getenv('API_GATEWAY_PORT')}"

STATISTICS_DB_URL = ""