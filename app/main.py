from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine
from app.exceptions.exceptions import AppConnectionError, AppDatabaseError, HabitNotFoundError
from app.routers import report_router
from app.common.constants import (
    HABITS_DB_URL,
    RABBITMQ_URL,
    RABBITMQ_QUEUE,
)
from app.rabbitmq.s_client import RabbitMQClient
import uvicorn
import logging
from pika.exceptions import AMQPError

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
async def startup_event():
    try:
        app.state.engine = create_async_engine(HABITS_DB_URL)
        app.state.rabbitmq_client = RabbitMQClient(
            RABBITMQ_URL,
            RABBITMQ_QUEUE,
            app.state.engine,
        )
        await app.state.rabbitmq_client.connect()
        await app.state.rabbitmq_client.start_consuming()
    except AMQPError as e:
        logging.error(f"Error connecting to RabbitMQ: {e}")
        raise e
    except Exception as e:
        logging.error(f"Unknown error: {e}")
        raise e

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.rabbitmq_client.disconnect()
    await app.state.engine.dispose()

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
