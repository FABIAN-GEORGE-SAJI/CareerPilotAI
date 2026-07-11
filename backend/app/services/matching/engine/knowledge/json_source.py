import json
from pathlib import Path

from app.schemas.skill_entry import SkillEntry

from app.services.matching.engine.knowledge.base_source import (
    BaseKnowledgeSource,
)


class JSONKnowledgeSource(BaseKnowledgeSource):
    """
    Loads skill knowledge from a JSON file.
    """

    def __init__(self):

        self.data = self._load()

    @staticmethod
    def _load() -> dict:

        path = (
            Path(__file__)
            .parent
            / "skills.json"
        )

        if not path.exists():
            return {}

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    async def get(
        self,
        skill: str,
    ) -> SkillEntry | None:

        skill = skill.lower()

        if skill not in self.data:
            return None

        item = self.data[skill]

        return SkillEntry(

            canonical=item["canonical"],

            aliases=set(
                item.get(
                    "aliases",
                    [],
                )
            ),

            category=item.get(
                "category",
                "",
            ),

            description=item.get(
                "description",
                "",
            ),
        )