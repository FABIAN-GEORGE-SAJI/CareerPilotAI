from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.models.user import UserModel

from app.core.logging import logger
from app.schemas.career_agent import (
    CareerAgentRequest,
    CareerAgentResponse,
)

from app.services.langchain.agent import career_agent
router = APIRouter(
    prefix="/career-agent",
    tags=["Career Agent"],
)


@router.post(
    "",
    response_model=CareerAgentResponse,
    summary="Chat with the AI career assistant",
    description=(
        "Sends a message to the conversational career agent, which has "
        "access to the given resume, job description, and ATS report (via "
        "its tools) to answer questions, suggest improvements, or generate "
        "career-related content on request. Optionally accepts prior turns "
        "of the conversation (history) so the agent has real multi-turn "
        "memory rather than treating every message as the start of a new "
        "conversation."
    ),
)
async def chat(
    request: CareerAgentRequest,
    current_user: UserModel = Depends(get_current_user),
):
    # Unexpected failures (LangChain/Gemini errors, etc.) propagate to the
    # global exception handlers registered in main.py, which log them and
    # return a consistent 500 instead of being caught and re-wrapped here.
    prompt = (
        f"Resume ID: {request.resume_id}\n\n"
        f"Job ID: {request.job_id}\n\n"
        f"User Request:\n\n{request.message}"
    )

    # Prior turns are replayed ahead of the new message so the agent has
    # genuine conversational memory - previously only the latest message was
    # ever sent, so the frontend's "Conversation memory enabled" badge was
    # inaccurate (it only "remembered" because the frontend re-displayed old
    # chat bubbles, not because the backend retained anything).
    history_messages = [
        {"role": turn.role, "content": turn.content} for turn in request.history
    ]

    result = await career_agent.ainvoke(
        {"messages": [*history_messages, {"role": "user", "content": prompt}]}
    )

    messages = result["messages"]
    answer = ""

    for message in reversed(messages):
        if getattr(message, "type", "") == "ai":
            answer = message.text if hasattr(message, "text") else str(message.content)
            break

    logger.info(
        "Career agent responded: resume_id=%s job_id=%s history_turns=%s",
        request.resume_id,
        request.job_id,
        len(request.history),
    )

    return CareerAgentResponse(response=answer)
