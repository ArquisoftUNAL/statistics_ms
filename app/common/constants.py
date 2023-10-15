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

API_GATEWAY_URL = f"{os.getenv('API_GATEWAY_URL')}"

STATISTICS_DB_URL = f"{os.getenv('MONGODB_URL')}"
STATISTICS_DB = f"{os.getenv('MONDODB_NAME')}"

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")