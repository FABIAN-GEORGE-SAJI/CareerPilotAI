from app.services.matching.engine.policy.decision_policy import (
    DecisionPolicy,
)

tests = [
    1.0,
    0.92,
    0.85,
    0.81,
    0.79,
    0.70,
    0.60,
]

print()

for score in tests:

    decision = DecisionPolicy.evaluate(score)

    print(
        f"{score:.2f}"
        f" -> "
        f"{decision.accepted}"
        f" | "
        f"{decision.relationship.value}"
        f" | "
        f"{decision.weight}"
    )