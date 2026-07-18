from langchain_core.tools import tool

from app.services.ai.ai_orchestrator import AIOrchestrator


orchestrator = AIOrchestrator()


@tool
async def generate_feedback(
    resume_id: int,
    job_id: int,
):
    """
    Generate ATS feedback.
    """

    return await orchestrator.generate_feedback(
        resume_id,
        job_id,
    )


@tool
async def generate_cover_letter(
    resume_id: int,
    job_id: int,
):
    """
    Generate a cover letter.
    """

    return await orchestrator.generate_cover_letter(
        resume_id,
        job_id,
    )


@tool
async def rewrite_resume(
    resume_id: int,
    job_id: int,
):
    """
    Rewrite the resume.
    """

    return await orchestrator.rewrite_resume(
        resume_id,
        job_id,
    )


@tool
async def generate_interview_questions(
    resume_id: int,
    job_id: int,
):
    """
    Generate interview questions.
    """

    return await orchestrator.generate_interview_questions(
        resume_id,
        job_id,
    )


@tool
async def generate_learning_roadmap(
    resume_id: int,
    job_id: int,
):
    """
    Generate a learning roadmap.
    """

    return await orchestrator.generate_learning_roadmap(
        resume_id,
        job_id,
    )


TOOLS = [
    generate_feedback,
    generate_cover_letter,
    rewrite_resume,
    generate_interview_questions,
    generate_learning_roadmap,
]