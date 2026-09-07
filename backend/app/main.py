from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.database.connection import mongodb
from app.database.indexes import create_indexes


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongodb.connect()

    create_indexes()

    yield

    mongodb.close()


settings = get_settings()

app = FastAPI(
    title=settings.project_name,
    description="The AI Curiosity Universe",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "EchoNova API",
        "environment": settings.environment,
    }