import asyncio

from app.schemas.resume_data import (
    ResumeData,
    BasicInfo,
)
from app.schemas.job_data import JobDescriptionData

from app.services.matching.skill_scorer import SkillScorer


async def main():

    scorer = SkillScorer()

    resume = ResumeData(

        basic_info=BasicInfo(),

        skills=[
            "Python",
            "SQL",
            "Docker",
            "AWS",
        ],
    )

    job = JobDescriptionData(

        required_skills=[
            "Python",
            "MySQL",
        ],

        preferred_skills=[
            "Amazon Web Services",
        ],

        soft_skills=[
            "Communication",
        ],
    )

    result = await scorer.score(
        resume,
        job,
    )

    print()

    print("Overall Score:", result[0])

    print("Required Score:", result[1])

    print("Preferred Score:", result[2])

    print("Soft Score:", result[3])

    print()

    print("Matched Skills")

    for skill in result[4]:
        print("-", skill)

    print()

    print("Missing Skills")

    for skill in result[5]:
        print("-", skill)


if __name__ == "__main__":
    asyncio.run(main())