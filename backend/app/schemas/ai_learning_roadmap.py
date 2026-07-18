from pydantic import BaseModel, Field


class LearningItem(BaseModel):

    skill: str = ""

    reason: str = ""

    estimated_time: str = ""

    learning_resources: list[str] = Field(
        default_factory=list
    )


class AILearningRoadmap(BaseModel):

    immediate: list[LearningItem] = Field(
        default_factory=list
    )

    short_term: list[LearningItem] = Field(
        default_factory=list
    )

    medium_term: list[LearningItem] = Field(
        default_factory=list
    )

    long_term: list[LearningItem] = Field(
        default_factory=list
    )

    final_goal: str = ""