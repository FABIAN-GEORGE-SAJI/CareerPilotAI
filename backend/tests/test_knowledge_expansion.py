from app.services.matching.engine.matcher.hybrid_matcher import (
    HybridMatcher,
)

matcher = HybridMatcher()

print()

print(
    matcher._expand_skills(
        [
            "AWS",
        ]
    )
)

print()

print(
    matcher._expand_skills(
        [
            "Amazon Web Services",
        ]
    )
)