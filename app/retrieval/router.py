from __future__ import annotations

from app.models import RetrievalMode


def route_query(question: str) -> RetrievalMode:
    q = question.lower()
    pricing_terms = {"price", "cost", "sla", "uptime", "availability", "region", "server"}
    policy_terms = {"policy", "security", "process", "compliance", "handbook", "approach"}

    has_pricing = any(term in q for term in pricing_terms)
    has_policy = any(term in q for term in policy_terms)

    if has_pricing and has_policy:
        return RetrievalMode.HYBRID
    if has_pricing:
        return RetrievalMode.SQL
    return RetrievalMode.VECTOR
