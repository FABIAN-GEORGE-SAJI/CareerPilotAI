from abc import ABC, abstractmethod

from app.schemas.match_result import MatchResult


class BaseMatcher(ABC):
    """
    Base interface for all matching algorithms.
    """

    @abstractmethod
    async def match(
        self,
        resume_skills: set[str],
        job_skills: set[str],
    ) -> MatchResult:
        """
        Compare resume skills with job skills.
        """
        pass