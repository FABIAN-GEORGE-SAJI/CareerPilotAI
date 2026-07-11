class ScoreCalculator:
    """
    Calculates the overall ATS score.
    """

    @staticmethod
    def calculate(
        *scores: float,
    ) -> float:

        valid_scores = [
            score
            for score in scores
            if score is not None
        ]

        if not valid_scores:
            return 0.0

        return round(
            sum(valid_scores) / len(valid_scores),
            2,
        )