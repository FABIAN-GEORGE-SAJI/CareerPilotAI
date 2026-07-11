from app.schemas.similarity_level import SimilarityLevel


class SimilarityPolicy:
    """
    Converts cosine similarity into
    ATS relationship and weight.
    """

    RULES = [

        (0.99, SimilarityLevel.EXACT, 1.00),

        (0.85, SimilarityLevel.EQUIVALENT, 0.95),

        (0.75, SimilarityLevel.VERY_STRONG, 0.80),

        (0.65, SimilarityLevel.STRONG, 0.60),

        (0.55, SimilarityLevel.RELATED, 0.30),

        (0.00, SimilarityLevel.WEAK, 0.00),
    ]

    @classmethod
    def classify(
        cls,
        similarity: float,
    ):

        for threshold, level, weight in cls.RULES:

            if similarity >= threshold:

                return level, weight

        return SimilarityLevel.NONE, 0.0