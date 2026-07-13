import asyncio

from app.schemas.ats_result import ATSResult
from app.services.ai.gemini_service import GeminiService


async def main():

    report = ATSResult(
        overall_score=78,
        skill_score=82,
        education_score=100,
        experience_score=65,
        project_score=70,
        matched_skills=[
            "Python",
            "FastAPI",
            "SQL",
        ],
        missing_skills=[
            "Docker",
            "AWS",
        ],
        experience_reason="Experience is below the preferred requirement.",
    )

    gemini = GeminiService()

    feedback = await gemini.generate_feedback(
        report
    )

    print(feedback.model_dump())


asyncio.run(main())