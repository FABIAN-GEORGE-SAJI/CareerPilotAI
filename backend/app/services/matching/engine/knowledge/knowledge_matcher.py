from app.services.matching.engine.knowledge.knowledge_service import (
    KnowledgeService,
)


class KnowledgeMatcher:

    def __init__(self):

        self.knowledge = KnowledgeService()

    def match(
        self,
        resume_skills: list[str],
        job_skill: str,
    ) -> bool:

        knowledge = self.knowledge.search(
            job_skill,
            k=1,
        )

        if not knowledge:
            return False

        aliases = knowledge[0]["aliases"]

        resume_lower = {
            skill.lower()
            for skill in resume_skills
        }

        for alias in aliases:

            if alias.lower() in resume_lower:
                return True

        return False