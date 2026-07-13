import asyncio

from app.schemas.resume_data import (
    ResumeData,
    BasicInfo,
)

from app.schemas.job_data import JobDescriptionData
from app.schemas.ats_result import ATSResult

from app.services.ai.gemini_service import GeminiService


async def main():

    service = GeminiService()

    resume = ResumeData(
        basic_info=BasicInfo(
            name="John Doe",
            email="john@example.com",
            phone="9999999999",
        ),
        summary="Backend developer with experience building REST APIs.",
        skills=[
            "Python",
            "FastAPI",
            "SQL",
        ],
    )

    job = JobDescriptionData(
        title="Backend Python Developer",
        company="OpenAI",
        required_skills=[
            "Python",
            "FastAPI",
            "Docker",
            "AWS",
        ],
        preferred_skills=[
            "Kubernetes",
        ],
    )

    report = ATSResult(
        overall_score=76,
        skill_score=82,
        experience_score=65,
        education_score=100,
        project_score=70,
        required_skill_score=50,
        missing_skills=[
            "Docker",
            "AWS",
        ],
    )

    roadmap = await service.generate_learning_roadmap(
        resume,
        job,
        report,
    )

    print(roadmap.model_dump())


asyncio.run(main())