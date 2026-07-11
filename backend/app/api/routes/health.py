from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
async def health_check():
    return {
        "status": "healthy",
        "service": "CareerPilot AI",
        "version": "1.0.0",
    }