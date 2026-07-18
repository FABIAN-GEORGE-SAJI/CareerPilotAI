from pydantic import BaseModel, Field


class InterviewQuestion(BaseModel):

    question: str = ""

    category: str = ""

    difficulty: str = ""

    why_asked: str = ""

    ideal_answer_points: list[str] = Field(
        default_factory=list
    )


class AIInterviewQuestions(BaseModel):

    technical: list[InterviewQuestion] = Field(
        default_factory=list
    )

    behavioral: list[InterviewQuestion] = Field(
        default_factory=list
    )

    project_based: list[InterviewQuestion] = Field(
        default_factory=list
    )

    hr: list[InterviewQuestion] = Field(
        default_factory=list
    )