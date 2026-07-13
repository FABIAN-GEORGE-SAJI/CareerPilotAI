import asyncio

from app.schemas.resume_data import (
    ResumeData,
    BasicInfo,
)

from app.schemas.job_data import JobDescriptionData

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
            "Docker",
        ],
    )

    job = JobDescriptionData(
        title="Backend Python Developer",
        company="OpenAI",
        required_skills=[
            "Python",
            "FastAPI",
            "Docker",
        ],
        preferred_skills=[
            "AWS",
            "Kubernetes",
        ],
        responsibilities=[
            "Build REST APIs",
            "Write scalable backend services",
        ],
    )

    rewrite = await service.rewrite_resume(
        resume,
        job,
    )

    print(rewrite.model_dump())


asyncio.run(main())