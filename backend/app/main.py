from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.users.router import router as users_router
from app.core.database import engine
from sqlalchemy import text

app = FastAPI(
    title="Employee Portal API",
    version="1.0.0",
)

app.include_router(
    users_router,
    prefix="/api/v1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.get("/health/database")
def database_health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "database": "connected"
    }