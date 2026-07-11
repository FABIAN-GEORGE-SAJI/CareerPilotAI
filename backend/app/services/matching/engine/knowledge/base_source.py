from abc import ABC, abstractmethod

from app.schemas.skill_entry import SkillEntry


class BaseKnowledgeSource(ABC):
    """
    Base interface for knowledge providers.
    """

    @abstractmethod
    async def get(
        self,
        skill: str,
    ) -> SkillEntry | None:
        """
        Return information about a skill.

        Returns None if the skill is unknown.
        """
        pass