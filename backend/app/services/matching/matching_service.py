from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.schemas.match_context import MatchContext
from app.schemas.ats_result import ATSResult

from app.schemas.job_data import JobDescriptionData
from app.schemas.resume_data import ResumeData
from app.repositories.job_repository import JobRepository
from app.repositories.resume_repository import ResumeRepository
from app.services.matching.ats_scorer import ATSScorer
from app.services.matching.report_cache import ReportCache

class MatchingService:
    """
    Resolves a resume/job pair and runs the ATS scoring engine.

    The session is injected rather than opened internally (see
    app/api/dependencies.py::get_matching_service) so its lifecycle is
    owned by the request - it's closed automatically once the request
    completes, the same way every other request-scoped session in this
    app is managed via app.database.dependencies.get_session.

    Every call to match()/build_context() always computes a fresh report
    and writes it to ReportCache (rather than reading a cached one first) -
    this is the entry point behind the ATS page's "Regenerate" button, so
    it must always be able to produce a genuinely new audit. Other AI
    features (see AIOrchestrator) read from this same cache instead of
    recomputing, so they stay in sync with whatever the ATS page most
    recently showed without each needing their own scoring call.
    """

    def __init__(self, session: Session):

        self.resume_repository = ResumeRepository(
            session,
        )

        self.job_repository = JobRepository(
            session,
        )

        self.ats_scorer = ATSScorer()

    async def match(
        self,
        resume_id: int,
        job_id: int,
    ) -> ATSResult:

        context = await self.build_context(
            resume_id,
            job_id,
        )

        return context.report

    async def build_context(
        self,
        resume_id: int,
        job_id: int,
    ) -> MatchContext:

        resume_model = self.resume_repository.get_by_id(
            resume_id,
        )

        job_model = self.job_repository.get_by_id(
            job_id,
        )

        if resume_model is None:
            raise NotFoundError("Resume not found.")

        if job_model is None:
            raise NotFoundError("Job description not found.")

        resume = ResumeData(
            **resume_model.parsed_data,
        )

        job = JobDescriptionData(
            **job_model.parsed_data,
        )

        report = await self.ats_scorer.score(
            resume,
            job,
        )

        # Refresh the shared cache so every downstream AI feature
        # (Feedback, Rewrite, Cover Letter, Interview, Roadmap - see
        # AIOrchestrator) picks up this exact report instead of running its
        # own scoring pass. This was previously only claimed in the
        # docstring above; the actual .set() call was missing.
        ReportCache.set(resume_id, job_id, report)

        return MatchContext(
            resume=resume,
            job=job,
            report=report,
        )
