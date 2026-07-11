from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.resume import ResumeUploadResponse
from app.services.resume.upload_service import ResumeUploadService

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post(
    "/upload",
    response_model=ResumeUploadResponse
)
async def upload_resume(
    file: UploadFile = File(...)
):

    try:
        return await ResumeUploadService.save_resume(file)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )