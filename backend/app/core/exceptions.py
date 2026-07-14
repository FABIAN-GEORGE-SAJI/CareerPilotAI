from fastapi import Request
from fastapi.responses import JSONResponse

from google.genai.errors import (
    ClientError,
    ServerError,
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

    return JSONResponse(
        status_code=500,
        content={
            "detail":
            "An unexpected server error occurred."
        },
    )