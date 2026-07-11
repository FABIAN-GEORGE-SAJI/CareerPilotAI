from app.schemas.ats_result import ATSResult


class RecommendationEngine:
    """
    Generates actionable recommendations
    based on ATS scoring results.
    """

    @staticmethod
    def generate(
        report: ATSResult,
    ) -> list[str]:

        recommendations: list[str] = []

        # -----------------------------
        # Skill Recommendations
        # -----------------------------
        if report.skill_score < 70:

            top_missing = report.missing_skills[:5]

            if top_missing:
                recommendations.append(
                    "Add or strengthen these skills: "
                    + ", ".join(top_missing)
                    + "."
                )

        # -----------------------------
        # Education
        # -----------------------------
        if report.education_score < 100:
            recommendations.append(
                "Include your education details more clearly."
            )

        # -----------------------------
        # Projects
        # -----------------------------
        if report.project_score < 60:
            recommendations.append(
                "Add more relevant projects and clearly list the technologies used."
            )

        # -----------------------------
        # Experience
        # -----------------------------
        if report.experience_score < 60:
            recommendations.append(
                report.experience_reason
            )

        # -----------------------------
        # Overall
        # -----------------------------
        if report.overall_score >= 85:
            recommendations.append(
                "Excellent ATS compatibility. Focus on tailoring your resume for each application."
            )

        elif report.overall_score >= 70:
            recommendations.append(
                "Good match. Strengthening a few missing skills can significantly improve your ATS score."
            )

        else:
            recommendations.append(
                "Your resume needs additional improvements to better match this job description."
            )

        return recommendations