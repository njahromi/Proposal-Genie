from __future__ import annotations

import json
from pathlib import Path

from app.agents.graph import run_proposal_graph


def score_relevance(answer: str, question: str) -> float:
    q_terms = set(question.lower().split())
    a_terms = set(answer.lower().split())
    if not q_terms:
        return 0.0
    return len(q_terms.intersection(a_terms)) / len(q_terms)


def score_faithfulness(answer: str, citations: list[str]) -> float:
    return 1.0 if citations else 0.0


def run_evaluation(golden_path: str = "app/evals/golden_set.jsonl") -> dict:
    rows = []
    for line in Path(golden_path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))

    relevance_scores: list[float] = []
    faithfulness_scores: list[float] = []
    context_precision_scores: list[float] = []

    for item in rows:
        result = run_proposal_graph(item["question"])
        question_run = result.questions[0]
        answer = question_run.draft.answer if question_run.draft else ""
        citations = question_run.draft.citations if question_run.draft else []

        relevance = score_relevance(answer, item["question"])
        faithfulness = score_faithfulness(answer, citations)
        context_precision = 1.0 if citations else 0.0

        relevance_scores.append(relevance)
        faithfulness_scores.append(faithfulness)
        context_precision_scores.append(context_precision)

    report = {
        "samples": len(rows),
        "relevance": round(sum(relevance_scores) / max(len(relevance_scores), 1), 3),
        "faithfulness": round(sum(faithfulness_scores) / max(len(faithfulness_scores), 1), 3),
        "context_precision": round(sum(context_precision_scores) / max(len(context_precision_scores), 1), 3),
    }
    return report


if __name__ == "__main__":
    results = run_evaluation()
    print(json.dumps(results, indent=2))
