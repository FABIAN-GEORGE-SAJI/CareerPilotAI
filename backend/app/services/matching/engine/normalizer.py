class SkillNormalizer:
    """
    Normalizes skill names before matching.
    """

    def normalize(
        self,
        skill: str,
    ) -> str:

        return (
            skill
            .strip()
            .lower()
        )

    def normalize_many(
        self,
        skills: list[str],
    ) -> set[str]:

        return {
            self.normalize(skill)
            for skill in skills
            if skill.strip()
        }