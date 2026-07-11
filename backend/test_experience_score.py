import asyncio

from app.schemas.entities import Experience
from app.schemas.job_data import JobDescriptionData
from app.schemas.resume_data import ResumeData, BasicInfo
from app.services.ai.gemini_service import GeminiService


async def main():

    resume = ResumeData(
        basic_info=BasicInfo(
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
        ),
        experience=[
            Experience(
                company="ABC Technologies",
                position="Backend Developer",
                start_date="2022",
                end_date="2025",
                description=[
                    "Built REST APIs using FastAPI",
                    "Worked with PostgreSQL",
                    "Dockerized backend services",
                ],
            )
        ],
    )

    job = JobDescriptionData(
        title="Backend Software Engineer",
        company="Nimbus Cloud Systems",
        responsibilities=[
            "Develop REST APIs",
            "Deploy Docker containers",
            "Optimize PostgreSQL databases",
        ],
        skills=[
            "Python",
            "FastAPI",
            "Docker",
            "PostgreSQL",
        ],
    )

    gemini = GeminiService()

    result = await gemini.score_experience(
        resume,
        job,
    )

    print("=" * 60)
    print("AI EXPERIENCE SCORE")
    print("=" * 60)
    print(f"Score  : {result.score}")
    print(f"Reason : {result.reason}")


if __name__ == "__main__":
    asyncio.run(main())