from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.models.user import UserModel

from app.core.logging import logger
from app.core.validators import validate_upload_file
from app.database.dependencies import get_session
from app.repositories.job_repository import JobRepository
from app.services.document_service import extract_text_from_pdf
from app.services.ai.gemini_service import GeminiService

router = APIRouter(
    tags=["Jobs"],
)
gemini_service = GeminiService()


@router.post(
    "/upload",
    summary="Upload and parse a job description",
    description=(
        "Accepts a single PDF job description, extracts its text, and uses "
        "Gemini to parse it into a structured profile (title, required and "
        "preferred skills, responsibilities, qualifications). The parsed "
        "job is persisted and its job_id is returned for use by the ATS, "
        "feedback, rewrite, cover letter, interview, and roadmap endpoints."
    ),
)
async def upload_job(
    file: UploadFile = File(..., description="Job description file (PDF only)."),
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
):
    # Validation (filename, extension, non-empty, size limit) is centralized
    # in app.core.validators so this logic isn't duplicated with resume.py.
    # Any failure here raises HTTPException(400) directly.
    await validate_upload_file(file)

    # Unexpected failures propagate to the global exception handlers
    # registered in main.py, which log them and return a consistent 500.
    raw_text = await extract_text_from_pdf(file)
    parsed_data = await gemini_service.parse_document(raw_text, is_resume=False)

    job_repository = JobRepository(session)
    db_job = job_repository.save(filename=file.filename, parsed_data=parsed_data)

    logger.info("Job description uploaded and parsed: job_id=%s filename=%s", db_job.id, file.filename)

    # Response shape kept identical to before - pages/2_Job.py expects this.
    return {
        "message": "Job description parsed successfully.",
        "job_id": db_job.id,
        "job": parsed_data,
    }
