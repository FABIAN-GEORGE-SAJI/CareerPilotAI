from fastapi import APIRouter, HTTPException

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
)
async def chat(
    request: CareerAgentRequest,
):

    try:

        prompt = f"""
Resume ID: {request.resume_id}

Job ID: {request.job_id}

User Request:

{request.message}
"""

        result = await career_agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]
            }
        )

        messages = result["messages"]

        answer = ""

        for message in reversed(messages):

            if getattr(message, "type", "") == "ai":

                if hasattr(message, "text"):
                    answer = message.text
                else:
                    answer = str(message.content)

                break

        return CareerAgentResponse(
            response=answer,
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )