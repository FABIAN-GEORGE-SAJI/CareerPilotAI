from app.schemas.semantic_match_result import (
    SemanticSkillMatch,
)


class GreedyAssignment:
    """
    Greedy one-to-one assignment.

    Each resume skill can only satisfy one job skill.
    """

    @staticmethod
    def assign(
        matches: list[SemanticSkillMatch],
    ) -> list[SemanticSkillMatch]:

        matches = sorted(
            matches,
            key=lambda x: x.similarity,
            reverse=True,
        )

        used_resume = set()

        used_job = set()

        assigned = []

        for match in matches:

            if match.resume_skill in used_resume:
                continue

            if match.job_skill in used_job:
                continue

            assigned.append(match)

            used_resume.add(match.resume_skill)

            used_job.add(match.job_skill)

        return assigned