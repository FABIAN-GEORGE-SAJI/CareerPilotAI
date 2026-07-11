from app.schemas.job_data import JobDescriptionData
import asyncio
from app.services.matching.ats_scorer import ATSScorer
from app.schemas.resume_data import ResumeData, BasicInfo


async def main():

    resume = ResumeData(
        basic_info=BasicInfo(
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
        ),
        skills=[
            "Python",
            "FastAPI",
            "Docker",
            "Git",
            "SQL",
        ],
    )

    job = JobDescriptionData(
        title="Backend Engineer",
        company="Nimbus",
        skills=[
            "Python",
            "Docker",
            "Redis",
            "AWS",
            "Git",
            "SQL",
        ],
    )

    ats_scorer = ATSScorer()

    report = await ats_scorer.score(
        resume,
        job,
    )
    

    print("=" * 60)
    print("ATS REPORT")
    print("=" * 60)

    print(f"Overall Score      : {report.overall_score}")
    print(f"Skill Score        : {report.skill_score}")
    print(f"Education Score    : {report.education_score}")
    print(f"Experience Score   : {report.experience_score}")
    print(f"Project Score      : {report.project_score}")
    print(f"Semantic Score     : {report.semantic_score}")
    print()

    print(f"Matched Skills     : {report.matched_skills}")
    print(f"Missing Skills     : {report.missing_skills}")
    print(f"Recommendations    : {report.recommendations}")


if __name__ == "__main__":
    asyncio.run(main())