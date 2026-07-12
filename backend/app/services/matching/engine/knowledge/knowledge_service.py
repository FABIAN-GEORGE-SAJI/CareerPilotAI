from app.services.matching.engine.knowledge.skill_repository import (
    SkillRepository,
)


class KnowledgeService:

    def __init__(self):

        self.repository = SkillRepository()

    def search(
        self,
        skill: str,
        k: int = 3,
    ):

        result = self.repository.search(
            skill,
            k,
        )

        if not result["ids"][0]:
            return []

        knowledge = []

        for metadata, distance in zip(
            
            result["metadatas"][0],
            result["distances"][0],
        ):
            if distance > 1.0:
                continue

            aliases = metadata["aliases"].split(",")

            canonical = metadata["canonical"]

            if canonical not in aliases:
                aliases.insert(0, canonical)

            knowledge.append(
                {
                    "canonical": canonical,
                    "aliases": aliases,
                    "category": metadata["category"],
                    "distance": distance,
                }
            )

        return knowledge