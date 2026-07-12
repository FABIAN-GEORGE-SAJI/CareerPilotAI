from app.services.matching.engine.knowledge.knowledge_service import (
    KnowledgeService,
)


class Canonicalizer:

    def __init__(self):

        self.knowledge = KnowledgeService()

    def canonicalize(
        self,
        skills: list[str],
    ) -> list[str]:

        canonical = []

        for skill in skills:

            knowledge = self.knowledge.search(
                skill,
                k=1,
            )

            if knowledge:

                canonical.append(
                    knowledge[0]["canonical"]
                )

            else:

                canonical.append(skill)

        return list(dict.fromkeys(canonical))