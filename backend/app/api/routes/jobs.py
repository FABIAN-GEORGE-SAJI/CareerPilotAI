from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.job import JobUploadResponse
from app.services.jobs.upload_service import JobUploadService

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post(
    "/upload",
    response_model=JobUploadResponse
)
async def upload_job(
    file: UploadFile = File(...)
):

    try:
        return await JobUploadService.save_job(file)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )