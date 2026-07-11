from fastapi import UploadFile

from app.database.dependencies import get_session
from app.repositories.resume_repository import ResumeRepository
from app.core.config import settings
from app.services.document.service import DocumentService
from app.services.ai.gemini_service import GeminiService


class ResumeUploadService:

    @staticmethod
    async def save_resume(file: UploadFile):

        extracted_text, unique_name = await DocumentService.save_document(
            file,
            settings.RESUME_DIR,
        )

        gemini = GeminiService()

        parsed_resume = await gemini.parse_resume(extracted_text)

        session = next(get_session())

        repository = ResumeRepository(session)

        repository.save(
            filename=unique_name,
            parsed_data=parsed_resume.model_dump(),
        )

        session.close()

        return {
            "message": "Resume uploaded successfully.",
            "filename": unique_name,
            "resume": parsed_resume.model_dump()
        }