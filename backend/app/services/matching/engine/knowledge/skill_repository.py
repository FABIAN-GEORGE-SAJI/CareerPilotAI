from app.services.matching.engine.knowledge.chroma_client import (
    ChromaClient,
)


class SkillRepository:

    def __init__(self):

        self.db = ChromaClient()

    def add(
        self,
        skill_id: str,
        canonical: str,
        aliases: list[str],
        description: str,
        category: str,
    ):

        text = " ".join(
            [
                canonical,
                *aliases,
                description,
                category,
            ]
        )

        self.db.collection.add(

            ids=[skill_id],

            documents=[text],

            metadatas=[
                {
                    "canonical": canonical,
                    "aliases": ",".join(aliases),
                    "category": category,
                }
            ],
        )

    def search(
        self,
        query: str,
        k: int = 5,
    ):

        return self.db.collection.query(

            query_texts=[query],

            n_results=k,
        )