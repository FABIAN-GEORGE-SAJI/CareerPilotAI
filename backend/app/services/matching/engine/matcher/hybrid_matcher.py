from app.schemas.hybrid_match_result import HybridMatchResult
from app.services.matching.engine.matcher.exact_matcher import (
    ExactMatcher,
)
from app.services.matching.engine.assignment.greedy_assignment import (
    GreedyAssignment,
)

from app.services.matching.engine.matcher.semantic_matcher import (
    SemanticMatcher,
)
from app.schemas.skill_match import SkillMatch
from app.services.matching.engine.policy.decision_policy import (
    DecisionPolicy,
)


class HybridMatcher:

    def __init__(self):

        self.exact = ExactMatcher()
        self.semantic = SemanticMatcher()

    async def match(
        self,
        resume_skills: list[str],
        job_skills: list[str],
    ) -> HybridMatchResult:

        result = HybridMatchResult()

        exact_matches = self.exact.match(
            resume_skills,
            job_skills,
        )

        semantic_result = await self.semantic.match(
            resume_skills,
            job_skills,
        )

        

        total_weight = 0.0

        for semantic in semantic_result.matched:

            job_skill = semantic.job_skill

            if job_skill.lower() in exact_matches:

                decision = DecisionPolicy.evaluate(1.0)

                result.matched.append(
                    SkillMatch(
                        resume_skill=job_skill,
                        job_skill=job_skill,
                        matched=True,
                        exact=True,
                        similarity=1.0,
                        relationship=decision.relationship,
                        weight=decision.weight,
                    )
                )

                total_weight += decision.weight

                continue
                

                

            decision = DecisionPolicy.evaluate(
                semantic.similarity
            )

            result.matched.append(
                SkillMatch(
                    resume_skill=semantic.resume_skill,
                    job_skill=semantic.job_skill,
                    matched=decision.accepted,
                    exact=False,
                    similarity=semantic.similarity,
                    relationship=decision.relationship,
                    weight=decision.weight,
                )
            )

            if decision.accepted:

                total_weight += decision.weight

            else:

                result.missing.append(
                    semantic.job_skill
                )

        if job_skills:
            result.score = round(
                total_weight / len(job_skills) * 100,
                2,
            )

        return result