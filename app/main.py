from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import logger
from app.api.v1.websocket import router as ws_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Real-time Voice Assistant with OpenAI",
)

app.include_router(ws_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    logger.info(f"{settings.PROJECT_NAME} starting in {settings.ENVIRONMENT} mode...")

@app.get("/")
async def root():
    return {"message": "Nava Voice Assistant is running!", "version": settings.VERSION}