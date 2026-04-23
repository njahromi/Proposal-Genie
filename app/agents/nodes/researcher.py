from __future__ import annotations

from app.models import RFPQuestion, RetrievedContext, RetrievalMode
from app.retrieval.router import route_query
from app.retrieval.sql_retriever import sql_retriever
from app.retrieval.vector_store import vector_store


def research_question(question: RFPQuestion) -> RetrievedContext:
    mode = route_query(question.prompt)
    snippets: list[str] = []
    sql_rows: list[dict] = []
    citations: list[str] = []

    if mode in (RetrievalMode.VECTOR, RetrievalMode.HYBRID):
        docs = vector_store.search(question.prompt)
        snippets.extend([doc.content for doc in docs])
        citations.extend([doc.source for doc in docs])

    if mode in (RetrievalMode.SQL, RetrievalMode.HYBRID):
        query = sql_retriever.text_to_sql(question.prompt)
        sql_rows = sql_retriever.safe_execute(query)
        citations.append("company_sql_db")

    return RetrievedContext(
        question_id=question.id,
        mode=mode,
        snippets=snippets,
        sql_rows=sql_rows,
        citations=sorted(set(citations)),
    )
