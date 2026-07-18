# CareerPilotAI - Project Status

Last Updated: 2026-07-17

Version: v2.0 Gemini-Audited ATS

Overall Progress: ~95%

---

# Current Goal

All Critical and High priority items from the 2026-07-17 Design Review are
implemented. ATS is the shared intelligence layer reused by every
downstream AI feature. Remaining work is polish only.

---

# Architecture (actual, as implemented)

PDF Upload
    |
PDF Extractor
    |
Gemini Parser (resume_parser / job_parser, structured output)
    |
Structured Data (ResumeData / JobDescriptionData)
    |
ATSScorer:
    - deterministic token-overlap baseline (skills, required, preferred,
      soft, keyword coverage) computed in Python
    - single Gemini call (ats_validator) audits/refines the baseline with
      full resume+job context, returning score, hire/hire_reason/
      confidence, strengths/weaknesses, per-section scores, and
      evidence-tagged skill matches
    |
ATSResult  (cached per (resume_id, job_id) in ReportCache)
    |
    +--> Feedback / Rewrite / Cover Letter / Interview / Roadmap
         (each reuses the cached ATSResult instead of re-scoring;
         Rewrite/Cover Letter/Interview additionally receive a
         known_gaps summary derived from it)
    |
Frontend (Streamlit)

There is no separate ExactMatcher / SemanticMatcher / HybridMatcher /
GreedyAssignment / DecisionPolicy / SimilarityPolicy module stack. Earlier
versions of this document described that architecture; it was never built.
The single Gemini-audited scorer above is the real (and only) scoring
engine, and is treated as the locked, single source of truth for ATS
analysis across the whole app.

---

# Backend Progress

## Database

Status: DONE. SQLAlchemy, repository layer, models, CRUD. Locked.

## Resume Pipeline

Status: DONE. PDF upload, PDF extraction, Gemini parsing, resume mapper,
database storage. Locked.

## Job Pipeline

Status: DONE. PDF upload, extraction, Gemini parsing into required/
preferred/soft skills, education, experience, responsibilities, keywords.

## ATS Scoring Engine (ATSScorer)

Status: DONE. Deterministic baseline + single Gemini audit call
(ats_validator, response_schema-enforced via AIATSValidation). Produces
the full ATSResult contract the frontend expects: hire, hire_reason,
confidence, strengths, weaknesses, experience_reason, keyword_coverage,
per-section required/preferred/soft skill scores, and evidence-tagged
skill matches. Locked.

## Report Caching (ReportCache)

Status: DONE. Process-local cache keyed by (resume_id, job_id).
MatchingService writes to it on every /match call; AIOrchestrator reads
from it first and only falls back to ATSScorer on a cache miss. Guarantees
every feature agrees with the ATS page's numbers and avoids redundant
Gemini scoring calls.

## AI Features

Status: DONE for all five.

- Feedback: reuses cached ATSResult.
- Resume Rewrite: reuses cached ATSResult; grounded via known_gaps.
- Cover Letter: reuses cached ATSResult; grounded via known_gaps.
- Interview Questions: reuses cached ATSResult; grounded via known_gaps,
  weighted toward missing_skills/weaknesses.
- Learning Roadmap: reuses cached ATSResult; already received the full
  report by design.

All Gemini calls pass a real Pydantic response_schema (native structured
output), not just prompt-text instructions.

## Career Agent

Status: DONE. Real LangChain tool-calling agent (5 tools, one per AI
feature above) with a mentor-voice system prompt and explicit guidance for
requests outside its toolset (e.g. salary negotiation). Multi-turn memory
is real: the frontend sends prior chat turns as `history` on every
request, and the route replays them into the agent's message list before
the new turn.

## API

Status: DONE. Resume upload, job upload, match, all five /ai/* routes,
career agent. `match.py` dead code removed.

---

# Frontend

Status: DONE. All 9 pages (Resume, Job, ATS, Feedback, Resume Rewrite,
Cover Letter, Interview, Roadmap, Career Agent) plus Login/Register.
Sidebar shows a live funnel progress indicator. Resume Rewrite offers both
.txt and formatted .docx export. Landing page copy matches what the
product actually does (no unbacked format-detection claim).

---

# Technical Debt

Status: Resolved as of this update.

- Dead duplicated code in match.py: removed.
- Orphaned pre-Gemini-audit modules (weights.py, experience_score.txt,
  hybrid_match_result.py, semantic_match_result.py): deleted.
- GEMINI_MODEL_PRO now points at a distinct, stronger model than
  GEMINI_MODEL, so the use_pro=True flag has a real effect.

---

# Locked Modules

DO NOT MODIFY unless there is a confirmed bug.

- ATSScorer (deterministic baseline + Gemini audit)
- ReportCache
- ai_orchestrator.py's cache-then-score-then-cache flow

---

# Parking Lot

Ideas that are intentionally postponed.

- Authentication hardening beyond the current JWT flow
- Resume history / versioning
- Analytics
- Multi-user support
- Email integration
- Recruiter dashboard
- Persisting ReportCache beyond process lifetime (Redis or a DB-backed
  match record) if this ever needs to run as more than one process

---

# Rules

1. No rebuilding completed modules without a confirmed bug.
2. Update this file when architecture actually changes - not the other
   way around.
3. Every completed feature must include a test.
4. Production bugs have priority over new features.
5. Keep architecture simple.
6. Gemini handles understanding and generation. ATSScorer's deterministic
   baseline handles reproducible ground truth; Gemini refines it with
   context. Neither replaces the other.
7. ATS is the single source of truth - no downstream feature computes its
   own independent resume/job match analysis.
