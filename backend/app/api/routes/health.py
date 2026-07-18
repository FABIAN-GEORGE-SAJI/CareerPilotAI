from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "/",
    summary="Health check",
    description="Lightweight liveness check used by deployment platforms and the frontend to confirm the API is reachable.",
)
async def health_check():
    return {
        "status": "healthy",
        "service": "CareerPilot AI",
        "version": "1.0.0",
    }
