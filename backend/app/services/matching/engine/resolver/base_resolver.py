from abc import ABC, abstractmethod


class BaseResolver(ABC):
    """
    Base interface for all skill resolvers.

    A resolver receives a normalized skill and returns
    its canonical representation.
    """

    @abstractmethod
    async def resolve(
        self,
        skill: str,
    ) -> str:
        """
        Resolve a skill into its canonical form.
        """
        pass