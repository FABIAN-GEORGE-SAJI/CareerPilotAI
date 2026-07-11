from app.schemas.match_result import MatchResult

from app.services.matching.engine.normalizer import SkillNormalizer
from app.services.matching.engine.exact_matcher import ExactMatcher

from app.services.matching.engine.resolver.chain import ResolverChain


class MatchingPipeline:
    """
    Complete skill matching workflow.

    Workflow

        Raw Skills
            ↓
        Normalize
            ↓
        Resolve
            ↓
        Match
    """

    def __init__(self):

        self.normalizer = SkillNormalizer()

        self.resolver = ResolverChain()

        self.matcher = ExactMatcher()

    async def match(
        self,
        resume_skills: list[str],
        job_skills: list[str],
    ) -> MatchResult:

        # -----------------------------
        # Normalize
        # -----------------------------
        normalized_resume = (
            self.normalizer.normalize_many(
                resume_skills,
            )
        )

        normalized_job = (
            self.normalizer.normalize_many(
                job_skills,
            )
        )

        # -----------------------------
        # Resolve
        # -----------------------------
        resolved_resume = (
            await self.resolver.resolve_many(
                normalized_resume,
            )
        )

        resolved_job = (
            await self.resolver.resolve_many(
                normalized_job,
            )
        )

        # -----------------------------
        # Match
        # -----------------------------
        result = await self.matcher.match(
            resolved_resume,
            resolved_job,
        )

        result.normalized_resume = resolved_resume

        result.normalized_job = resolved_job

        return result