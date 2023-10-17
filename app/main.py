from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
from app.models.statistics_db_models import ReportDocument
from app.exceptions.exceptions import (
    AppConnectionError,
    AppDatabaseError,
    HabitNotFoundError,
)
from app.routers import report_router
from app.common.constants import (
    HABITS_DB_URL,
    STATISTICS_DB_URL,
    STATISTICS_DB,
    RABBITMQ_QUEUE,
    RABBITMQ_URL,
)
from app.rabbitmq.rabbitmq_client import RabbitMQClient

app = FastAPI()

"""origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3003",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)"""


@app.on_event("startup")
async def startup():
    app.state.engine = create_async_engine(HABITS_DB_URL)
    app.state.client = AsyncIOMotorClient(STATISTICS_DB_URL)
    await init_beanie(
        database=app.state.client[STATISTICS_DB], document_models=[ReportDocument]
    )
    app.state.rabbitmq_client = RabbitMQClient(
        RABBITMQ_URL,
        RABBITMQ_QUEUE,
        app.state.engine,
        app.state.client
    )
    await app.state.rabbitmq_client.connect()
    await app.state.rabbitmq_client.start_consuming()


@app.on_event("shutdown")
async def shutdown():
    await app.state.client.close()
    await app.state.engine.dispose()
    #await app.state.rabbitmq_client.disconnect()


@app.exception_handler(AppConnectionError)
async def connection_error_handler(request: Request, exc: AppConnectionError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"message": str(exc)},
    )


@app.exception_handler(AppDatabaseError)
async def database_error_handler(request: Request, exc: AppDatabaseError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": str(exc)},
    )


@app.exception_handler(HabitNotFoundError)
async def habit_not_found_error_handler(request: Request, exc: HabitNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)},
    )


app.include_router(report_router.router, prefix="/api/stats", tags=["statistics"])


@app.get("/")
async def health():
    return {"message": "Ok"}


if __name__ == "__main__":
    uvicorn.run(app)
