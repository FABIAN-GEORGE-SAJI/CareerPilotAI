from fastapi import UploadFile

from app.database.dependencies import get_session
from app.repositories.job_repository import JobRepository
from app.core.config import settings
from app.services.document.service import DocumentService
from app.services.ai.gemini_service import GeminiService


class JobUploadService:

    @staticmethod
    async def save_job(file: UploadFile):

        extracted_text, unique_name = await DocumentService.save_document(
            file,
            settings.JOB_DESCRIPTION_DIR,
        )

        gemini = GeminiService()

        parsed_job = await gemini.parse_job(extracted_text)
        session = next(get_session())

        repository = JobRepository(session)

        repository.save(
            filename=unique_name,
            parsed_data=parsed_job.model_dump(),
        )

        session.close()

        return {
            "message": "Job description uploaded successfully.",
            "filename": unique_name,
            "job": parsed_job.model_dump()
        }