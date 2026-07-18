from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.models.user import UserModel
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

# NOTE: AIOrchestrator raises NotFoundError when the resume_id/job_id given
# doesn't resolve to a record. That's translated into a 404 response by the
# global exception handler registered in main.py, so these routes don't need
# their own try/except blocks.


@router.post(
    "/feedback",
    response_model=FeedbackResponse,
    summary="Generate resume feedback",
    description="Runs the ATS scoring engine against the given resume/job pair, then asks Gemini for line-by-line strengths, weaknesses, hiring-readiness assessment, priorities, and missing keywords.",
)
async def generate_feedback(
    request: AIRequest,
    current_user: UserModel = Depends(get_current_user),
):
    result = await orchestrator.generate_feedback(request.resume_id, request.job_id)
    return FeedbackResponse(result=result)


@router.post(
    "/cover-letter",
    response_model=CoverLetterResponse,
    summary="Generate a cover letter",
    description="Generates a tailored cover letter (subject, greeting, body, closing) for the given resume/job pair.",
)
async def generate_cover_letter(
    request: AIRequest,
    current_user: UserModel = Depends(get_current_user),
):
    result = await orchestrator.generate_cover_letter(request.resume_id, request.job_id)
    return CoverLetterResponse(result=result)


@router.post(
    "/rewrite",
    response_model=ResumeRewriteResponse,
    summary="Rewrite a resume",
    description="Rewrites the resume's summary, experience, and projects for the given job, plus improved skills and recommendations.",
)
async def rewrite_resume(
    request: AIRequest,
    current_user: UserModel = Depends(get_current_user),
):
    result = await orchestrator.rewrite_resume(request.resume_id, request.job_id)
    return ResumeRewriteResponse(result=result)


@router.post(
    "/interview",
    response_model=InterviewQuestionsResponse,
    summary="Generate interview questions",
    description="Generates technical, behavioural, project, and HR interview questions tailored to the resume/job pair, each with difficulty, rationale, and ideal-answer points.",
)
async def generate_interview_questions(
    request: AIRequest,
    current_user: UserModel = Depends(get_current_user),
):
    result = await orchestrator.generate_interview_questions(request.resume_id, request.job_id)
    return InterviewQuestionsResponse(result=result)


@router.post(
    "/roadmap",
    response_model=LearningRoadmapResponse,
    summary="Generate a learning roadmap",
    description="Generates an immediate/short-term/medium-term/long-term upskilling roadmap toward the given job, based on the ATS gap analysis for the resume/job pair.",
)
async def generate_learning_roadmap(
    request: AIRequest,
    current_user: UserModel = Depends(get_current_user),
):
    result = await orchestrator.generate_learning_roadmap(request.resume_id, request.job_id)
    return LearningRoadmapResponse(result=result)
