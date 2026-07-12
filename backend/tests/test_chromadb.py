from app.services.matching.engine.knowledge.skill_repository import (
    SkillRepository,
)

repo = SkillRepository()

repo.add(
    "aws",
    "AWS",
    [
        "Amazon Web Services",
        "Amazon AWS",
    ],
    "Cloud computing platform",
    "Cloud",
)

result = repo.search("Amazon Web Services")

print(result)