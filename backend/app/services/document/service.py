import shutil
import uuid
from pathlib import Path
from app.core.logging import logger

from fastapi import HTTPException, UploadFile

from app.core.config import settings
from app.services.resume.pdf_parser import PDFParser


class DocumentService:

    @staticmethod
    async def save_document(
        file: UploadFile,
        destination: Path,
    ):
        logger.info("=" * 50)
        logger.info(
            "Filename: %s",
            file.filename,
        )
        logger.info(
            "Content type: %s",
            file.content_type,
        )
        logger.info("=" * 50)

        extension = Path(file.filename).suffix.lower()

        if extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type."
            )
        unique_name = f"{uuid.uuid4()}{extension}"

        save_path = destination / unique_name

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extracted_text = ""

        if extension == ".pdf":
            extracted_text = PDFParser.extract_text(save_path)

        return extracted_text, unique_name
            