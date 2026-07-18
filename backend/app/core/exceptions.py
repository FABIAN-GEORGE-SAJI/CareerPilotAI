from fastapi import Request
from fastapi.responses import JSONResponse

from google.genai.errors import (
    ClientError,
    ServerError,
)

from app.core.logging import logger


# ---------------------------------------------------------------------------
# Domain exceptions
#
# Services raise these instead of a bare ValueError so that routes don't need
# to know (or duplicate) which HTTP status a given failure maps to. Each one
# is registered against a handler in main.py. Status codes here match what
# the routes previously raised by hand - this is a refactor of *where* the
# mapping lives, not a change to the API contract.
# ---------------------------------------------------------------------------

class NotFoundError(Exception):
    """Raised when a requested resource (resume, job, etc.) does not exist."""


class ConflictError(Exception):
    """Raised when a request conflicts with existing state (e.g. duplicate email)."""


class InvalidCredentialsError(Exception):
    """Raised when authentication credentials are missing or incorrect."""


async def not_found_error_handler(
    request: Request,
    exc: NotFoundError,
):

    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
        },
    )


async def conflict_error_handler(
    request: Request,
    exc: ConflictError,
):

    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc),
        },
    )


async def invalid_credentials_error_handler(
    request: Request,
    exc: InvalidCredentialsError,
):

    return JSONResponse(
        status_code=401,
        content={
            "detail": str(exc),
        },
    )


async def gemini_server_error_handler(
    request: Request,
    exc: ServerError,
):

    return JSONResponse(
        status_code=503,
        content={
            "detail":
            "Gemini API is temporarily unavailable. Please try again in a few moments."
        },
    )


async def gemini_client_error_handler(
    request: Request,
    exc: ClientError,
):

    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc),
        },
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
):

    logger.exception(
        "Unhandled exception on %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail":
            "An unexpected server error occurred."
        },
    )