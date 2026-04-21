from fastapi import FastAPI
from app.api.routes import router
from app.db.session import init_db
from app.core.config import settings

app = FastAPI(title=settings.app_name, version="2.0.0")

@app.on_event("startup")
def startup_event() -> None:
    init_db()

app.include_router(router, prefix="/api/v1")

@app.get("/")
def health() -> dict:
    return {
        "app": settings.app_name,
        "status": "ok",
        "version": "2.0.0",
        "docs": "/docs",
    }
