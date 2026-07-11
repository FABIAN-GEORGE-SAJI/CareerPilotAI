from app.schemas.match_result import MatchResult

from app.services.matching.engine.base_matcher import BaseMatcher


class ExactMatcher(BaseMatcher):
    """
    Performs exact skill matching.
    """

    async def match(
        self,
        resume_skills: set[str],
        job_skills: set[str],
    ) -> MatchResult:

        matched = sorted(
            resume_skills & job_skills
        )

        missing = sorted(
            job_skills - resume_skills
        )

        if not job_skills:
            score = 100.0
        else:
            score = round(
                len(matched)
                / len(job_skills)
                * 100,
                2,
            )

        return MatchResult(
            matched=matched,
            missing=missing,
            score=score,
            confidence=1.0,
        )