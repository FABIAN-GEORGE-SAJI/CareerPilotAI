from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config import settings
from app.api.routes.resume import router as resume_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.match import router as match_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Career Assistant",
)

app.include_router(health_router)
app.include_router(resume_router)
app.include_router(jobs_router)
app.include_router(match_router)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "status": "running",
    }
