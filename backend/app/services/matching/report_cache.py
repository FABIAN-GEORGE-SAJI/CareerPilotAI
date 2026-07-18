from typing import Optional

from app.schemas.ats_result import ATSResult


class ReportCache:
    """
    Process-local cache of ATS reports, keyed by (resume_id, job_id).

    Resumes and job descriptions are immutable once uploaded (there's no
    edit endpoint), so a report for a given (resume_id, job_id) pair never
    goes stale for the lifetime of the process - it's safe to cache
    indefinitely rather than needing a TTL or invalidation logic.

    This serves two purposes:

    1. Avoids re-running the full ATS scoring pipeline (a Gemini call) every
       time Feedback, Rewrite, Cover Letter, Interview, or Roadmap need the
       same report that the ATS page already computed.
    2. Guarantees every page that talks about "the ATS score" for a given
       resume/job pair is looking at the exact same numbers. Since scoring
       goes through an LLM, two independent calls are not guaranteed to
       return identical output - without this cache, the ATS page and (say)
       the Feedback page could quietly disagree.

    Kept intentionally simple (a class-level dict) for this application's
    scale. A multi-instance deployment would move this to a shared store
    (Redis, or persisting the report on the match record itself) instead.
    """

    _store: dict[tuple[int, int], ATSResult] = {}

    @classmethod
    def get(cls, resume_id: int, job_id: int) -> Optional[ATSResult]:
        return cls._store.get((resume_id, job_id))

    @classmethod
    def set(cls, resume_id: int, job_id: int, report: ATSResult) -> None:
        cls._store[(resume_id, job_id)] = report

    @classmethod
    def clear(cls) -> None:
        """Exposed for tests - not used in normal request handling."""
        cls._store.clear()
