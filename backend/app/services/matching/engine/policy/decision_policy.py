from app.schemas.decision import Decision
from app.schemas.similarity_level import SimilarityLevel


class DecisionPolicy:

    @staticmethod
    def evaluate(
        similarity: float,
    ) -> Decision:

        reasons = []

        if similarity >= 0.95:

            reasons.append("Exact match")

            return Decision(
                accepted=True,
                relationship=SimilarityLevel.EXACT,
                weight=1.0,
                confidence=similarity,
                reasons=reasons,
            )

        if similarity >= 0.85:

            reasons.append("Equivalent skill")

            return Decision(
                accepted=True,
                relationship=SimilarityLevel.EQUIVALENT,
                weight=0.95,
                confidence=similarity,
                reasons=reasons,
            )

        if similarity >= 0.80:

            reasons.append("Very strong semantic match")

            return Decision(
                accepted=True,
                relationship=SimilarityLevel.VERY_STRONG,
                weight=0.80,
                confidence=similarity,
                reasons=reasons,
            )

        reasons.append("Below acceptance threshold")

        return Decision(
            accepted=False,
            relationship=SimilarityLevel.WEAK,
            weight=0.0,
            confidence=similarity,
            reasons=reasons,
        )