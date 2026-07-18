import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.genai.errors import ClientError, ServerError

from app.api.routes import auth, resume, jobs, match, ai, career_agent, health
from app.core.exceptions import (
    NotFoundError,
    ConflictError,
    InvalidCredentialsError,
    not_found_error_handler,
    conflict_error_handler,
    invalid_credentials_error_handler,
    gemini_server_error_handler,
    gemini_client_error_handler,
    generic_exception_handler,
)
from app.database.database import init_db

app = FastAPI(
    title="CareerPilot AI Backend",
    version="2.0.0",
    description="Streamlined AI Talent Matching and Document Optimization Engine"
)

# Enable connection suite from Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in strict staging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route Registry
# NOTE: auth.router, ai.router, and career_agent.router already declare their
# own `prefix=` internally (see their respective route files). Passing
# `prefix=` again here would double it up (e.g. "/auth/auth/register"
# instead of "/auth/register"), breaking every endpoint the frontend calls
# on those three routers. resume.router, jobs.router, and match.router have
# no internal prefix, so they still need it supplied here.
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(resume.router, prefix="/resume")
app.include_router(jobs.router, prefix="/jobs")
app.include_router(match.router, prefix="/match")
app.include_router(ai.router)
app.include_router(career_agent.router)

# Centralized exception handling
# Services raise these domain exceptions; routes no longer need their own
# try/except blocks to translate them into HTTP responses. See
# app/core/exceptions.py for details.
app.add_exception_handler(NotFoundError, not_found_error_handler)
app.add_exception_handler(ConflictError, conflict_error_handler)
app.add_exception_handler(InvalidCredentialsError, invalid_credentials_error_handler)
app.add_exception_handler(ServerError, gemini_server_error_handler)
app.add_exception_handler(ClientError, gemini_client_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.on_event("startup")
def on_startup() -> None:
    # Ensures the canonical (app/models) tables exist on a fresh environment.
    # Idempotent: only creates tables that don't already exist.
    init_db()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)