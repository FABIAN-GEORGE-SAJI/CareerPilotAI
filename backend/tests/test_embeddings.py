import asyncio

from sklearn.metrics.pairwise import cosine_similarity

from app.services.matching.engine.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider,
)


async def main():

    provider = SentenceTransformerProvider()

    skills = [
        "Python",
        "SQL",
        "MySQL",
        "TensorFlow",
        "Machine Learning",
        "AWS",
        "Amazon Web Services",
    ]

    result = await provider.embed(skills)

    print("\nEmbedding Model:", result.model)
    print("Dimension:", result.dimension)
    print("Normalized:", result.normalized)

    similarity = cosine_similarity(result.vectors)

    print("\nCosine Similarity Matrix\n")

    print(" " * 20, end="")

    for skill in skills:
        print(f"{skill[:12]:>14}", end="")

    print()

    for i, skill in enumerate(skills):

        print(f"{skill[:18]:<20}", end="")

        for score in similarity[i]:
            print(f"{score:>14.2f}", end="")

        print()


if __name__ == "__main__":
    asyncio.run(main())