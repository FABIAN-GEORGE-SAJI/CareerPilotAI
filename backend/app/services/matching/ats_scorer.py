from typing import Any, Dict, List

from app.schemas.ai_ats_validation import AIATSValidation
from app.schemas.ats_result import ATSResult
from app.schemas.job_data import JobDescriptionData
from app.schemas.resume_data import ResumeData
from app.services.ai.gemini_service import GeminiService
from app.schemas.ai_ats_validation import AISkillEvidence


class ATSScorer:
    def __init__(self) -> None:
        self.gemini = GeminiService()

    def _token_baseline(self, resume_tokens: List[str], job_tokens: List[str]) -> Dict[str, Any]:
        """
        Deterministic overlap score between two token lists (skills, or
        keywords). This is the mathematical ground truth handed to Gemini -
        it never sees the job description without this baseline attached,
        so its score_adjustment is always relative to a known, reproducible
        starting point rather than a blank page.
        """
        resume_set = {t.lower().strip() for t in resume_tokens if t}
        job_set = {t.lower().strip() for t in job_tokens if t}

        if not job_set:
            return {"score": 100.0, "matched": list(resume_tokens), "missing": []}

        matched_set = resume_set.intersection(job_set)
        missing_set = job_set.difference(resume_set)
        score = (len(matched_set) / len(job_set)) * 100.0

        matched_output = [t for t in resume_tokens if t.lower().strip() in matched_set]
        missing_output = [t for t in job_tokens if t.lower().strip() in missing_set]

        return {"score": round(score, 2), "matched": matched_output, "missing": missing_output}

    def _keyword_baseline(self, resume: ResumeData, job: JobDescriptionData) -> Dict[str, Any]:
        """
        Deterministic baseline for how many of the job's stated keywords
        show up anywhere in the resume (skills, summary, experience and
        project descriptions) - a coarser, text-level check than the
        skill-list overlap above, since keywords aren't always modeled as
        discrete skills.
        """
        if not job.keywords:
            return {"score": 100.0, "job_keywords": []}

        haystack_parts = [resume.summary, *resume.skills]
        for exp in resume.experience:
            haystack_parts.extend(exp.description)
        for project in resume.projects:
            haystack_parts.extend(project.description)
            haystack_parts.extend(project.technologies)

        haystack = " ".join(p for p in haystack_parts if p).lower()
        found = sum(1 for kw in job.keywords if kw and kw.lower().strip() in haystack)
        score = (found / len(job.keywords)) * 100.0

        return {"score": round(score, 2), "job_keywords": job.keywords}

    async def score(self, resume: ResumeData, job: JobDescriptionData) -> ATSResult:
        """Runs the two-step ATS pipeline: a deterministic baseline, then a Gemini audit that refines it."""
        resume_dump = resume.model_dump()
        job_dump = job.model_dump()

        job_requirements = job.required_skills or job.skills

        overall_baseline = self._token_baseline(resume.skills, job_requirements)
        required_baseline = self._token_baseline(resume.skills, job.required_skills)
        preferred_baseline = self._token_baseline(resume.skills, job.preferred_skills)
        soft_baseline = self._token_baseline(resume.skills, job.soft_skills)
        keyword_baseline = self._keyword_baseline(resume, job)

        audit_payload = {
            "resume_profile": resume_dump,
            "job_profile": job_dump,
            "deterministic_metrics": {
                "overall": {
                    "score": overall_baseline["score"],
                    "matched": overall_baseline["matched"],
                    "missing": overall_baseline["missing"],
                },
                "required_skills": {"score": required_baseline["score"]},
                "preferred_skills": {"score": preferred_baseline["score"]},
                "soft_skills": {"score": soft_baseline["score"]},
                "keyword_coverage": {
                    "baseline_score": keyword_baseline["score"],
                    "job_keywords": keyword_baseline["job_keywords"],
                },
            },
        }

        raw_audit = await self.gemini._generate_structured(
            prompt_name="ats_validator",
            payload=audit_payload,
            response_schema=AIATSValidation,
            use_pro=False,
        )

        report = ATSResult()
        report.ats_score = overall_baseline["score"]
        report.overall_score = float(raw_audit.get("final_score", overall_baseline["score"]))
        report.score_adjustment = float(raw_audit.get("score_adjustment", 0.0))
        report.matched_skills = raw_audit.get("matched_skills", overall_baseline["matched"])
        report.missing_skills = raw_audit.get("missing_skills", overall_baseline["missing"])
        report.recommendations = raw_audit.get("recommendations", [])

        report.hire = bool(raw_audit.get("hire", False))
        report.hire_reason = raw_audit.get("hire_reason", "")
        report.confidence = float(raw_audit.get("confidence", 0.0))
        report.strengths = raw_audit.get("strengths", [])
        report.weaknesses = raw_audit.get("weaknesses", [])
        report.experience_reason = raw_audit.get("experience_reason", "")
        report.keyword_coverage = float(raw_audit.get("keyword_coverage", keyword_baseline["score"]))
        report.skill_evidence = [
            item if isinstance(item, AISkillEvidence)
            else AISkillEvidence.model_validate(item)
            for item in raw_audit.get("skill_evidence", [])
        ]

        sec_scores = raw_audit.get("section_scores", {})
        report.skill_score = float(sec_scores.get("skills", report.overall_score))
        report.required_skill_score = float(sec_scores.get("required_skills", required_baseline["score"]))
        report.preferred_skill_score = float(sec_scores.get("preferred_skills", preferred_baseline["score"]))
        report.soft_skill_score = float(sec_scores.get("soft_skills", soft_baseline["score"]))
        report.education_score = float(sec_scores.get("education", report.overall_score))
        report.experience_score = float(sec_scores.get("experience", report.overall_score))
        report.project_score = float(sec_scores.get("projects", report.overall_score))
        report.semantic_score = float(sec_scores.get("semantic", report.overall_score))

        # Keep the nested analysis tree in sync with the flat fields above -
        # both are populated from the same audit so pages reading either
        # shape (some read `report.experience_score`, the ATS page also
        # reads `report.analysis.experience.reason`) stay consistent.
        report.analysis.overall.overall_score = report.overall_score
        report.analysis.education.score = report.education_score
        report.analysis.experience.score = report.experience_score
        report.analysis.experience.reason = report.experience_reason
        report.analysis.projects.overall_score = report.project_score

        report.ai_validation = raw_audit

        return report
