from typing import Literal

from pydantic import BaseModel, Field


class CareerAgentTurn(BaseModel):
    """A single prior turn in the conversation, as displayed in the frontend chat."""

    role: Literal["user", "assistant"]
    content: str


class CareerAgentRequest(BaseModel):
    resume_id: int
    job_id: int
    message: str

    # Prior turns of this conversation, oldest first. Optional and defaults
    # to empty so existing callers (and the very first message of a new
    # conversation) keep working unchanged. When provided, the agent
    # actually sees this history - this is what makes the frontend's
    # "Conversation memory enabled" badge true rather than aspirational.
    history: list[CareerAgentTurn] = Field(default_factory=list)


class CareerAgentResponse(BaseModel):
    response: str
