import json

from app.services.matching.engine.knowledge.skill_repository import (
    SkillRepository,
)


repo = SkillRepository()

with open(
    "data/skills/skills.json",
    "r",
    encoding="utf-8",
) as f:

    skills = json.load(f)

for skill in skills:

    try:

        repo.add(
            skill["id"],
            skill["canonical"],
            skill["aliases"],
            skill["description"],
            skill["category"],
        )

        print(f"Added: {skill['canonical']}")

    except Exception:

        print(f"Skipped: {skill['canonical']}")

print()

print("Knowledge base ready.")