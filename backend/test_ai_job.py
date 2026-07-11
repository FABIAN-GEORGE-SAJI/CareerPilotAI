import asyncio
from pathlib import Path

from app.services.ai.gemini_service import GeminiService
from app.services.resume.pdf_parser import PDFParser


async def main():

    pdf_path = Path(
        "sample_data/jds/JD_1_Backend_Software_Engineer.pdf"
    )

    text = PDFParser.extract_text(pdf_path)

    service = GeminiService()

    job = await service.parse_job(text)

    print()

    print("=" * 60)
    print("AI Parsed Job")
    print("=" * 60)

    print(job.model_dump())


asyncio.run(main())