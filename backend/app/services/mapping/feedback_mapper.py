from app.schemas.ai_feedback import AIFeedback


class FeedbackMapper:

    @staticmethod
    def to_feedback(
        feedback: AIFeedback,
    ) -> AIFeedback:

        return feedback