from pydantic import BaseModel, Field


class SkillEntry(BaseModel):
    """
    Represents a canonical skill and its metadata.
    """

    canonical: str

    aliases: set[str] = Field(default_factory=set)

    category: str = ""

    description: str = ""