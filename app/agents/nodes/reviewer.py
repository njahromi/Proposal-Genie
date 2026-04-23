from __future__ import annotations

from app.models import DraftAnswer, ReviewResult, RFPQuestion


def review_answer(question: RFPQuestion, draft: DraftAnswer) -> ReviewResult:
    word_count = len(draft.answer.split())
    if word_count > question.max_words:
        return ReviewResult(
            question_id=question.id,
            passed=False,
            reason=f"Answer length {word_count} exceeds {question.max_words}.",
            route="rewrite_needed",
        )
    if len(draft.citations) == 0:
        return ReviewResult(
            question_id=question.id,
            passed=False,
            reason="No citations available in draft context.",
            route="needs_more_context",
        )
    if question.prompt.lower().split()[0] not in draft.answer.lower():
        # Soft check for relevance signal.
        return ReviewResult(
            question_id=question.id,
            passed=False,
            reason="Answer appears weakly aligned with the question.",
            route="needs_more_context",
        )
    return ReviewResult(question_id=question.id, passed=True, reason="Passed all checks.", route="pass")
