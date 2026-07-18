from pydantic import BaseModel

from app.schemas.ai_cover_letter import AICoverLetter
from app.schemas.ai_feedback import AIFeedback
from app.schemas.ai_interview_questions import AIInterviewQuestions
from app.schemas.ai_learning_roadmap import AILearningRoadmap
from app.schemas.ai_resume_rewrite import AIResumeRewrite


class FeedbackResponse(BaseModel):
    result: AIFeedback


class CoverLetterResponse(BaseModel):
    result: AICoverLetter


class ResumeRewriteResponse(BaseModel):
    result: AIResumeRewrite


class InterviewQuestionsResponse(BaseModel):
    result: AIInterviewQuestions


class LearningRoadmapResponse(BaseModel):
    result: AILearningRoadmap