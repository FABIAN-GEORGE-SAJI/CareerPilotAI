import asyncio

from app.services.matching.engine.matcher.semantic_matcher import (
    SemanticMatcher,
)


async def main():

    matcher = SemanticMatcher()

    resume = [

        "Python",

        "SQL",

        "Docker",

        "AWS",

    ]

    job = [

        "MySQL",

        "Amazon Web Services",

        "Machine Learning",

    ]

    result = await matcher.match(
        resume,
        job,
    )

    print()

    for match in result.matched:

        print(

            f"{match.resume_skill:15}"

            f" -> "

            f"{match.job_skill:25}"

            f"{match.similarity:.3f}"

        )

    print()

    print(
        "Average:",
        result.average_similarity,
    )


if __name__ == "__main__":
    asyncio.run(main())