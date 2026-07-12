from app.services.matching.engine.knowledge.knowledge_matcher import (
    KnowledgeMatcher,
)

matcher = KnowledgeMatcher()

resume = [
    "Python",
    "AWS",
    "SQL",
]

print()

print(
    matcher.match(
        resume,
        "Amazon Web Services",
    )
)

print(
    matcher.match(
        resume,
        "MySQL",
    )
)

print(
    matcher.match(
        resume,
        "Docker",
    )
)