import asyncio
from pathlib import Path

from app.services.ai.gemini_service import GeminiService
from app.services.resume.pdf_parser import PDFParser


async def main():

    pdf_path = Path(
        "sample_data/resumes/leadership_resume.pdf"
    )

    text = PDFParser.extract_text(pdf_path)

    service = GeminiService()

    resume = await service.parse_resume(text)

    print()

    print("=" * 60)
    print("AI Parsed Resume")
    print("=" * 60)

    print(resume.model_dump())


asyncio.run(main())