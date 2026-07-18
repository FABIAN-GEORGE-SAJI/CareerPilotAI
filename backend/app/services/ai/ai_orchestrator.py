from typing import Any, Dict, Tuple

from app.core.exceptions import NotFoundError
from app.database.session import SessionLocal
from app.repositories.job_repository import JobRepository
from app.repositories.resume_repository import ResumeRepository
from app.schemas.ats_result import ATSResult
from app.schemas.job_data import JobDescriptionData
from app.schemas.resume_data import ResumeData
from app.services.ai.gemini_service import GeminiService
from app.services.matching.ats_scorer import ATSScorer
from app.services.matching.report_cache import ReportCache


class AIOrchestrator:
    """
    Resolves a resume/job pair by ID and drives the appropriate Gemini
    generation call.

    Callers only ever have resume_id/job_id (the frontend never sends parsed
    resume/job payloads to /ai/* or the career agent) - this class owns the
    ID -> domain-object lookup itself via the repository layer, rather than
    requiring callers to pre-fetch ResumeData/JobDescriptionData.

    Each public method opens and closes its own short-lived DB session
    instead of taking one injected via FastAPI's Depends(). That's
    deliberate: this class is used both from FastAPI routes (which have a
    request-scoped session available) and from the LangChain career-agent
    tools (app/services/langchain/tools.py), which run outside any FastAPI
    request context and have no session to inject.

    ATS is the single source of truth for this application. Every
    downstream feature (Feedback, Resume Rewrite, Cover Letter, Interview
    Questions, Learning Roadmap) is grounded in the *same* ATSResult for a
    given (resume_id, job_id) pair - retrieved via ReportCache rather than
    each feature re-running ATSScorer independently. This guarantees every
    page agrees with what the ATS page showed, and avoids paying for a
    redundant Gemini scoring call on every follow-up feature. ATSScorer
    itself is never duplicated here - _get_ats_report only ever decides
    whether to call it, never re-implements what it does.
    """

    def __init__(self) -> None:
        self.gemini = GeminiService()
        self.ats_scorer = ATSScorer()

    def _resolve(self, resume_id: int, job_id: int) -> Tuple[ResumeData, JobDescriptionData]:
        session = SessionLocal()
        try:
            resume_record = ResumeRepository(session).get_by_id(resume_id)
            if not resume_record:
                raise NotFoundError(f"Resume {resume_id} not found.")

            job_record = JobRepository(session).get_by_id(job_id)
            if not job_record:
                raise NotFoundError(f"Job {job_id} not found.")

            return (
                ResumeData(**resume_record.parsed_data),
                JobDescriptionData(**job_record.parsed_data),
            )
        finally:
            session.close()

    async def _get_ats_report(
        self,
        resume_id: int,
        job_id: int,
        resume: ResumeData,
        job: JobDescriptionData,
    ) -> ATSResult:
        """
        Returns the cached ATS report for this (resume_id, job_id) pair - the
        one already computed by the ATS page, or by an earlier call to any
        of these features - if one exists. Otherwise runs ATSScorer once and
        caches the result for every subsequent caller. Resumes and jobs are
        immutable once uploaded, so this is safe to reuse for the lifetime
        of the process (see ReportCache's docstring).
        """
        cached = ReportCache.get(resume_id, job_id)
        if cached is not None:
            return cached

        report = await self.ats_scorer.score(resume=resume, job=job)
        ReportCache.set(resume_id, job_id, report)
        return report

    @staticmethod
    def _known_gaps(report: ATSResult) -> Dict[str, Any]:
        """
        Condenses an ATSResult into the compact gap summary handed to the
        Rewrite / Cover Letter / Interview prompts, so those features
        prioritize the exact gaps the ATS page already surfaced instead of
        each re-deriving their own independent (and possibly contradictory)
        view of what's missing.
        """
        return {
            "missing_skills": report.missing_skills,
            "weaknesses": report.weaknesses,
            "recommendations": report.recommendations,
            "experience_reason": report.experience_reason,
        }

    async def generate_feedback(self, resume_id: int, job_id: int) -> Dict[str, Any]:
        resume, job = self._resolve(resume_id, job_id)
        report = await self._get_ats_report(resume_id, job_id, resume, job)
        return await self.gemini.generate_feedback(report.model_dump())

    async def rewrite_resume(self, resume_id: int, job_id: int) -> Dict[str, Any]:
        resume, job = self._resolve(resume_id, job_id)
        report = await self._get_ats_report(resume_id, job_id, resume, job)
        return await self.gemini.rewrite_resume(
            resume.model_dump(),
            job.model_dump(),
            known_gaps=self._known_gaps(report),
        )

    async def generate_cover_letter(self, resume_id: int, job_id: int) -> Dict[str, Any]:
        resume, job = self._resolve(resume_id, job_id)
        report = await self._get_ats_report(resume_id, job_id, resume, job)
        return await self.gemini.generate_cover_letter(
            resume.model_dump(),
            job.model_dump(),
            known_gaps=self._known_gaps(report),
        )

    async def generate_interview_questions(self, resume_id: int, job_id: int) -> Dict[str, Any]:
        resume, job = self._resolve(resume_id, job_id)
        report = await self._get_ats_report(resume_id, job_id, resume, job)
        return await self.gemini.generate_interview_questions(
            resume.model_dump(),
            job.model_dump(),
            known_gaps=self._known_gaps(report),
        )

    async def generate_learning_roadmap(self, resume_id: int, job_id: int) -> Dict[str, Any]:
        resume, job = self._resolve(resume_id, job_id)
        report = await self._get_ats_report(resume_id, job_id, resume, job)
        return await self.gemini.generate_learning_roadmap(
            resume.model_dump(), job.model_dump(), report.model_dump()
        )
