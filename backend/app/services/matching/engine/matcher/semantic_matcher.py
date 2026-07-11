from sklearn.metrics.pairwise import cosine_similarity

from app.schemas.semantic_match_result import (
    SemanticMatchResult,
    SemanticSkillMatch,
)

from app.services.matching.engine.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider,
)


class SemanticMatcher:
    """
    Performs semantic matching between
    resume skills and job skills.
    """

    def __init__(self):

        self.provider = SentenceTransformerProvider()

    async def match(
        self,
        resume_skills: list[str],
        job_skills: list[str],
    ) -> SemanticMatchResult:

        result = SemanticMatchResult()

        if not resume_skills or not job_skills:
            return result

        resume_embeddings = await self.provider.embed(
            resume_skills,
        )

        job_embeddings = await self.provider.embed(
            job_skills,
        )

        similarity_matrix = cosine_similarity(
            resume_embeddings.vectors,
            job_embeddings.vectors,
        )

        similarities = []

        for job_index, job_skill in enumerate(job_skills):

            best_score = -1.0
            best_resume = ""

            for resume_index, resume_skill in enumerate(
                resume_skills
            ):

                score = similarity_matrix[
                    resume_index
                ][
                    job_index
                ]

                if score > best_score:

                    best_score = float(score)
                    best_resume = resume_skill

            result.matched.append(

                SemanticSkillMatch(

                    resume_skill=best_resume,

                    job_skill=job_skill,

                    similarity=round(
                        best_score,
                        3,
                    ),
                )

            )

            similarities.append(
                best_score
            )

        if similarities:

            result.average_similarity = round(

                sum(similarities)
                / len(similarities),

                3,
            )

        return result