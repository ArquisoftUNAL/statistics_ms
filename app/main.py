from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import report_router
import uvicorn

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

app.include_router(report_router.router, prefix="/api/stats", tags=["statistics"])

@app.get("/")
async def health():
    return {"message": "Ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
