from __future__ import annotations

from dataclasses import dataclass


@dataclass
class VectorDocument:
    doc_id: str
    content: str
    source: str


class VectorStore:
    def __init__(self) -> None:
        self._docs: list[VectorDocument] = []

    def add_documents(self, docs: list[VectorDocument]) -> None:
        self._docs.extend(docs)

    def semantic_chunk(self, text: str, chunk_size: int = 450) -> list[str]:
        words = text.split()
        chunks: list[str] = []
        for idx in range(0, len(words), chunk_size):
            chunks.append(" ".join(words[idx : idx + chunk_size]))
        return chunks

    def search(self, query: str, top_k: int = 4) -> list[VectorDocument]:
        query_terms = set(query.lower().split())
        scored: list[tuple[int, VectorDocument]] = []
        for doc in self._docs:
            overlap = len(query_terms.intersection(set(doc.content.lower().split())))
            scored.append((overlap, doc))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [doc for score, doc in scored if score > 0][:top_k]


vector_store = VectorStore()
