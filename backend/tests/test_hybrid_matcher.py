import asyncio

from app.services.matching.engine.matcher.hybrid_matcher import HybridMatcher


async def main():

    matcher = HybridMatcher()

    resume = [
        "Python",
        "SQL",
        "Docker",
        "AWS",
    ]

    job = [
        "Python",
        "MySQL",
        "Amazon Web Services",
        "Machine Learning",
        "Tableau",
    ]

    result = await matcher.match(
        resume,
        job,
    )

    print(f"\nOverall Score: {result.score}%\n")

    for match in result.matched:

        print(
            f"{match.job_skill:25}"
            f" <- {match.resume_skill:20}"
            f" | Exact={match.exact}"
            f" | {match.relationship.value:12}"
            f" | {match.similarity:.3f}"
            f" | Weight={match.weight:.2f}"
        )

    print("\nMissing Skills:")

    for skill in result.missing:

        print("-", skill)


if __name__ == "__main__":
    asyncio.run(main())