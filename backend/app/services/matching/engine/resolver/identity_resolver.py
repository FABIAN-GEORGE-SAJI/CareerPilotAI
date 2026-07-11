from app.services.matching.engine.resolver.base_resolver import BaseResolver


class IdentityResolver(BaseResolver):
    """
    Default resolver.

    Returns the skill unchanged.
    """

    async def resolve(
        self,
        skill: str,
    ) -> str:

        return skill