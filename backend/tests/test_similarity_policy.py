from app.services.matching.engine.policy.similarity_policy import (
    SimilarityPolicy,
)

print()

print(
    f"{'Similarity':<12}"
    f"{'Relationship':<18}"
    f"{'Weight':<10}"
)

print("-" * 42)

tests = [
    1.00,
    0.95,
    0.90,
    0.85,
    0.80,
    0.75,
    0.70,
    0.65,
    0.60,
    0.55,
    0.50,
    0.40,
    0.30,
]

for similarity in tests:

    relationship, weight = SimilarityPolicy.classify(
        similarity
    )

    print(
        f"{similarity:<12.2f}"
        f"{relationship.value:<18}"
        f"{weight:<10.2f}"
    )