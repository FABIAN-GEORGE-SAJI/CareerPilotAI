from app.core.weights import SKILL_WEIGHTS

from app.schemas.job_data import JobDescriptionData
from app.schemas.resume_data import ResumeData

from app.services.matching.base_scorer import BaseScorer
from app.services.matching.engine.matcher.hybrid_matcher import (
    HybridMatcher,
)


class SkillScorer(BaseScorer):
    """
    Scores resume skills using the HybridMatcher.

    Responsible only for:
    - Running the matcher for each skill category
    - Combining category scores
    """

    def __init__(self):

        self.matcher = HybridMatcher()

    async def score(
        self,
        resume: ResumeData,
        job: JobDescriptionData,
    ) -> tuple[
        float,
        float,
        float,
        float,
        list[str],
        list[str],
    ]:

        # ------------------------------------
        # Required Skills
        # ------------------------------------
        required_result = await self.matcher.match(
            resume.skills,
            job.required_skills,
        )

        # ------------------------------------
        # Preferred Skills
        # ------------------------------------
        preferred_result = await self.matcher.match(
            resume.skills,
            job.preferred_skills,
        )

        # ------------------------------------
        # Soft Skills
        # ------------------------------------
        soft_result = await self.matcher.match(
            resume.skills,
            job.soft_skills,
        )

        # ------------------------------------
        # Weighted Overall Score
        # ------------------------------------
        total_weight = (
            SKILL_WEIGHTS["required"]
            + SKILL_WEIGHTS["preferred"]
            + SKILL_WEIGHTS["soft"]
        )

        overall_score = round(
            (
                required_result.score * SKILL_WEIGHTS["required"]
                + preferred_result.score * SKILL_WEIGHTS["preferred"]
                + soft_result.score * SKILL_WEIGHTS["soft"]
            )
            / total_weight,
            2,
        )

        # ------------------------------------
        # Collect Matched Skills
        # ------------------------------------
        matched_skills = []

        for result in (
            required_result,
            preferred_result,
            soft_result,
        ):
            matched_skills.extend(
                [
                    skill.job_skill
                    for skill in result.matched
                    if skill.matched
                ]
            )

        matched_skills = sorted(set(matched_skills))

        # ------------------------------------
        # Collect Missing Skills
        # ------------------------------------
        missing_skills = sorted(
            set(
                required_result.missing
                + preferred_result.missing
                + soft_result.missing
            )
        )

        return (
            overall_score,
            required_result.score,
            preferred_result.score,
            soft_result.score,
            matched_skills,
            missing_skills,
        )