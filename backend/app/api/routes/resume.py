from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.models.user import UserModel

from app.core.logging import logger
from app.core.validators import validate_upload_file
from app.database.dependencies import get_session
from app.repositories.resume_repository import ResumeRepository
from app.services.document_service import extract_text_from_pdf
from app.services.ai.gemini_service import GeminiService

router = APIRouter(
    tags=["Resume"],
)
gemini_service = GeminiService()


@router.post(
    "/upload",
    summary="Upload and parse a resume",
    description=(
        "Accepts a single PDF resume, extracts its text, and uses Gemini to "
        "parse it into a structured profile (contact info, skills, "
        "experience, education, projects). The parsed resume is persisted "
        "and its resume_id is returned for use by the ATS, feedback, "
        "rewrite, cover letter, interview, and roadmap endpoints."
    ),
)
async def upload_resume(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
):
    # Validation (filename, extension, non-empty, size limit) is centralized
    # in app.core.validators so this logic isn't duplicated with jobs.py.
    # Any failure here raises HTTPException(400) directly.
    await validate_upload_file(file)

    # Unexpected failures (Gemini errors, parsing errors, etc.) are not
    # caught here - they propagate to the global exception handlers
    # registered in main.py, which log them and return a consistent 500.
    raw_text = await extract_text_from_pdf(file)
    parsed_data = await gemini_service.parse_document(raw_text, is_resume=True)

    resume_repository = ResumeRepository(session)
    db_resume = resume_repository.save(filename=file.filename, parsed_data=parsed_data)

    logger.info("Resume uploaded and parsed: resume_id=%s filename=%s", db_resume.id, file.filename)

    # Response shape kept identical to before - pages/1_Resume.py expects this.
    return {
        "message": "Resume parsed successfully.",
        "resume_id": db_resume.id,
        "resume": parsed_data,
    }
