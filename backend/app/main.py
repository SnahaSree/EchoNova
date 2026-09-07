from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.database.connection import mongodb


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongodb.connect()

    yield

    mongodb.close()


settings = get_settings()

app = FastAPI(
    title=settings.project_name,
    description="The AI Curiosity Universe",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "EchoNova API",
        "environment": settings.environment,
    }