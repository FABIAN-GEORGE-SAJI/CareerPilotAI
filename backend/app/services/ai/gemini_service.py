import asyncio
import json
from typing import Any, Dict, Optional

from google import genai
from google.genai import types
from google.genai.errors import APIError

from app.core.config import settings
from app.core.logging import logger
from app.schemas.ai_cover_letter import AICoverLetter
from app.schemas.ai_feedback import AIFeedback
from app.schemas.ai_interview_questions import AIInterviewQuestions
from app.schemas.ai_job import AIJob
from app.schemas.ai_learning_roadmap import AILearningRoadmap
from app.schemas.ai_resume import AIResume
from app.schemas.ai_resume_rewrite import AIResumeRewrite
from app.utils.json_parser import JSONParser
from app.utils.prompt_loader import PromptLoader


class GeminiService:
    _client: Optional[genai.Client] = None

    def __init__(self) -> None:
        if GeminiService._client is None:
            GeminiService._client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.client = GeminiService._client
        self.default_model = settings.GEMINI_MODEL
        self.pro_model = settings.GEMINI_MODEL_PRO
        logger.info(f"Loaded GEMINI_MODEL={self.default_model}")
        logger.info(f"Loaded GEMINI_MODEL_PRO={self.pro_model}")

    async def _generate_structured(
        self,
        prompt_name: str,
        payload: Dict[str, Any],
        response_schema: Any,
        use_pro: bool = False,
    ) -> Any:
        """
        Executes structured JSON content generation.

        ``response_schema`` is passed straight through to Gemini's native
        structured-output enforcement (a Pydantic model class, or None for
        the rare case where a call genuinely has no fixed shape). Passing an
        actual schema means malformed/incomplete JSON is rejected by the API
        itself rather than only being caught after the fact by
        ``JSONParser`` - the prompt's own "return exactly this JSON shape"
        instructions are a second line of defense, not the only one.
        """
        system_instruction = PromptLoader.load(prompt_name)
        model_target = self.pro_model if use_pro else self.default_model

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1 if not use_pro else 0.3,
            response_mime_type="application/json",
            response_schema=response_schema,
        )

        for attempt in range(3):
            try:
                response = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model=model_target,
                    contents=json.dumps(payload, ensure_ascii=False),
                    config=config,
                )
                return JSONParser.parse(response.text)
            except APIError as exc:
                if attempt == 2:
                    logger.error(f"Gemini API execution failed after 3 attempts: {exc}")
                    raise
                await asyncio.sleep(2 ** attempt)

    async def parse_document(self, text: str, is_resume: bool = True) -> Dict[str, Any]:
        """Parses unstructured resume/job text into a structured profile."""
        prompt_target = "resume_parser" if is_resume else "job_parser"
        schema = AIResume if is_resume else AIJob
        payload = {"document_text": text}
        return await self._generate_structured(prompt_target, payload, schema, use_pro=False)

    async def generate_feedback(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generates line-by-line quantitative analysis and assessment critiques."""
        return await self._generate_structured("feedback_generator", report_data, AIFeedback, use_pro=False)

    async def rewrite_resume(
        self,
        resume_data: Dict[str, Any],
        job_data: Dict[str, Any],
        known_gaps: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Rewrites the resume for the target job, grounded on the ATS gap analysis when available."""
        payload = {"resume": resume_data, "job": job_data, "known_gaps": known_gaps or {}}
        return await self._generate_structured("resume_rewrite", payload, AIResumeRewrite, use_pro=True)

    async def generate_cover_letter(
        self,
        resume_data: Dict[str, Any],
        job_data: Dict[str, Any],
        known_gaps: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Writes a tailored cover letter, grounded on the ATS gap analysis when available."""
        payload = {"resume": resume_data, "job": job_data, "known_gaps": known_gaps or {}}
        return await self._generate_structured("cover_letter", payload, AICoverLetter, use_pro=True)

    async def generate_interview_questions(
        self,
        resume_data: Dict[str, Any],
        job_data: Dict[str, Any],
        known_gaps: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Builds a tailored interview question bank, weighted toward the ATS gap analysis when available."""
        payload = {"resume": resume_data, "job": job_data, "known_gaps": known_gaps or {}}
        return await self._generate_structured("interview_questions", payload, AIInterviewQuestions, use_pro=True)

    async def generate_learning_roadmap(
        self, resume_data: Dict[str, Any], job_data: Dict[str, Any], ats_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Builds a phased upskilling roadmap from the resume/job pair and their ATS gap analysis."""
        payload = {"resume": resume_data, "job": job_data, "ats_report": ats_report}
        return await self._generate_structured("learning_roadmap", payload, AILearningRoadmap, use_pro=True)
