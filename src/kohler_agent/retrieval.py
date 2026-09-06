"""In-memory semantic (embedding + cosine similarity) retrieval index.

Deliberately dependency-light (no vector database) since the target
deployment is a single-machine local-first prototype. Swapping this out for
FAISS/Chroma later only requires changing this one file.
"""

from __future__ import annotations

import math
from typing import Any

from . import config


class SemanticIndex:
    def __init__(self, embedding_model: Any, documents: list[Any]):
        self.embedding_model = embedding_model
        self.documents = documents
        self.vectors = (
            embedding_model.embed_documents([document.page_content for document in documents])
            if documents
            else []
        )

    @staticmethod
    def cosine(left: list[float], right: list[float]) -> float:
        if not left or not right or len(left) != len(right):
            return 0.0
        left_norm = math.sqrt(sum(value * value for value in left))
        right_norm = math.sqrt(sum(value * value for value in right))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return sum(a * b for a, b in zip(left, right)) / (left_norm * right_norm)

    def search(self, query: str, k: int = config.TOP_K) -> list[tuple[Any, float]]:
        if not self.documents:
            return []
        query_vector = self.embedding_model.embed_query(query)
        ranked = [
            (document, self.cosine(query_vector, vector))
            for document, vector in zip(self.documents, self.vectors)
        ]
        ranked.sort(key=lambda item: item[1], reverse=True)
        return [item for item in ranked[:k] if item[1] >= config.MIN_RELEVANCE_SCORE]
