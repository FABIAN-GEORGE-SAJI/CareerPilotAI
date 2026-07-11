from app.services.matching.engine.resolver.base_resolver import BaseResolver
from app.services.matching.engine.resolver.identity_resolver import (
    IdentityResolver,
)


class ResolverChain:
    """
    Applies a sequence of resolvers to transform
    a skill into its canonical representation.
    """

    def __init__(self):

        self.resolvers: list[BaseResolver] = [
            IdentityResolver(),
        ]

    async def resolve(
        self,
        skill: str,
    ) -> str:

        current_skill = skill

        for resolver in self.resolvers:

            current_skill = await resolver.resolve(
                current_skill,
            )

        return current_skill

    async def resolve_many(
        self,
        skills: list[str] | set[str],
    ) -> set[str]:

        resolved = set()

        for skill in skills:

            resolved.add(
                await self.resolve(
                    skill,
                )
            )

        return resolved