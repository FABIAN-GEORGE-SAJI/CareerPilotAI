from fastapi import APIRouter, HTTPException

from app.schemas.ai import AIRequest
from app.schemas.ai_responses import (
    FeedbackResponse,
    CoverLetterResponse,
    ResumeRewriteResponse,
    InterviewQuestionsResponse,
    LearningRoadmapResponse,
)

from app.services.ai.ai_orchestrator import AIOrchestrator

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)

orchestrator = AIOrchestrator()


@router.post(
    "/feedback",
    response_model=FeedbackResponse,
)
async def generate_feedback(
    request: AIRequest,
):

    try:

        result = await orchestrator.generate_feedback(
            request.resume_id,
            request.job_id,
        )

        return FeedbackResponse(
            result=result,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.post(
    "/cover-letter",
    response_model=CoverLetterResponse,
)
async def generate_cover_letter(
    request: AIRequest,
):

    try:

        result = await orchestrator.generate_cover_letter(
            request.resume_id,
            request.job_id,
        )

        return CoverLetterResponse(
            result=result,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.post(
    "/rewrite",
    response_model=ResumeRewriteResponse,
)
async def rewrite_resume(
    request: AIRequest,
):

    try:

        result = await orchestrator.rewrite_resume(
            request.resume_id,
            request.job_id,
        )

        return ResumeRewriteResponse(
            result=result,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.post(
    "/interview",
    response_model=InterviewQuestionsResponse,
)
async def generate_interview_questions(
    request: AIRequest,
):

    try:

        result = await orchestrator.generate_interview_questions(
            request.resume_id,
            request.job_id,
        )

        return InterviewQuestionsResponse(
            result=result,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.post(
    "/roadmap",
    response_model=LearningRoadmapResponse,
)
async def generate_learning_roadmap(
    request: AIRequest,
):

    try:

        result = await orchestrator.generate_learning_roadmap(
            request.resume_id,
            request.job_id,
        )

        return LearningRoadmapResponse(
            result=result,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )