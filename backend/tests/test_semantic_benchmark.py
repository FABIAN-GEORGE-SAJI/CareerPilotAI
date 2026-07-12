import asyncio

import pandas as pd

from app.services.matching.engine.matcher.semantic_matcher import (
    SemanticMatcher,
)
from app.services.matching.engine.policy.similarity_policy import (
    SimilarityPolicy,
)


async def main():

    matcher = SemanticMatcher()

    df = pd.read_csv(
        "tests/benchmark/semantic_pairs.csv"
    )

    passed = 0

    total = len(df)

    category_stats = {}

    print()

    print(
        f"{'Category':12}"
        f"{'Resume Skill':22}"
        f"{'Job Skill':25}"
        f"{'Similarity':12}"
        f"{'Expected':12}"
        f"{'Policy':15}"
        f"{'Result'}"
    )

    print("-" * 120)

    for _, row in df.iterrows():

        resume_skill = row["resume_skill"]

        job_skill = row["job_skill"]

        expected = row["expected"]

        category = row["category"]

        result = await matcher.match(
            [resume_skill],
            [job_skill],
        )

        similarity = result.matched[0].similarity

        from app.services.matching.engine.policy.decision_policy import (
            DecisionPolicy,
        )

        decision = DecisionPolicy.evaluate(
            similarity
        )

        # -----------------------------
        # Convert policy to benchmark label
        # -----------------------------

        if decision.relationship.value == "Exact":
            predicted = "exact"

        elif decision.accepted:
            predicted = "match"

        elif similarity >= 0.60:
            predicted = "partial"

        else:
            predicted = "no_match"

        success = predicted == expected

        if success:
            passed += 1

        category_stats.setdefault(
            category,
            {"pass": 0, "total": 0},
        )

        category_stats[category]["total"] += 1

        if success:
            category_stats[category]["pass"] += 1

        print(
            f"{category:12}"
            f"{resume_skill:22}"
            f"{job_skill:25}"
            f"{similarity:<12.3f}"
            f"{expected:12}"
            f"{predicted:15}"
            f"{'PASS' if success else 'FAIL'}"
        )

    print("\n")

    print("=" * 60)

    print(
        f"Overall Accuracy : {passed}/{total}"
    )

    print(
        f"Accuracy         : {passed/total*100:.2f}%"
    )

    print()

    print("Per Category")

    for category, stats in category_stats.items():

        accuracy = (
            stats["pass"]
            / stats["total"]
            * 100
        )

        print(
            f"{category:12}"
            f"{accuracy:.2f}%"
        )


if __name__ == "__main__":
    asyncio.run(main())