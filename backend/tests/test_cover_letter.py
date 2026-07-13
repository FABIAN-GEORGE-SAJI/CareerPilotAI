import asyncio

from app.schemas.resume_data import (
    ResumeData,
    BasicInfo,
)

from app.schemas.job_data import JobDescriptionData

from app.services.ai.gemini_service import GeminiService


async def main():

    resume = ResumeData(

        basic_info=BasicInfo(
            name="John Doe",
            email="john@example.com",
            phone="+91 9876543210",
        ),

        skills=[
            "Python",
            "FastAPI",
            "SQL",
            "Docker",
        ],

        summary="Backend developer with experience building REST APIs.",

        education=[],

        experience=[],

        projects=[],

        certifications=[],

        languages=[],
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
        ],

        soft_skills=[
            "Communication",
        ],

        responsibilities=[
            "Develop REST APIs",
            "Write scalable backend services",
        ],

        qualifications=[
            "Bachelor's Degree",
        ],

        summary="Looking for an experienced backend developer.",

        location="Remote",

        employment_type="Full-time",

        experience="2+ years",

        education="Bachelor's Degree",

        keywords=[
            "Python",
            "FastAPI",
            "Docker",
            "AWS",
        ],
    )

    gemini = GeminiService()

    result = await gemini.generate_cover_letter(
        resume,
        job,
    )

    print(result.model_dump())


asyncio.run(main())