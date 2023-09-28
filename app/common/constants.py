from sqlalchemy import  URL
from dotenv import load_dotenv
import os

load_dotenv()

habits_db_url = URL.create(
    drivername="postgresql+asyncpg",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
)

api_gateway_url = f"http://{os.getenv('API_GATEWAY_HOST')}:{os.getenv('API_GATEWAY_PORT')}"