from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config import settings
from app.api.routes.resume import router as resume_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.match import router as match_router
from app.api.routes.ai import router as ai_router
from google.genai.errors import (
    ClientError,
    ServerError,
)
from app.api.routes.career_agent import (
    router as career_agent_router,
)

from app.core.exceptions import (
    gemini_server_error_handler,
    gemini_client_error_handler,
    generic_exception_handler,
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Career Assistant",
)

app.add_exception_handler(
    ServerError,
    gemini_server_error_handler,
)

app.add_exception_handler(
    ClientError,
    gemini_client_error_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)

app.include_router(health_router)
app.include_router(resume_router)
app.include_router(jobs_router)
app.include_router(match_router)
app.include_router(ai_router)
app.include_router(
    career_agent_router,
)


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "status": "running",
    }
