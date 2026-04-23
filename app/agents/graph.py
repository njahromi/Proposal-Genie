from __future__ import annotations

from dataclasses import dataclass, field

from app.agents.nodes.drafter import draft_answer
from app.agents.nodes.orchestrator import parse_rfp_into_questions
from app.agents.nodes.researcher import research_question
from app.agents.nodes.reviewer import review_answer
from app.config import settings
from app.models import DraftAnswer, RFPQuestion


@dataclass
class QuestionRun:
    question: RFPQuestion
    loops: int = 0
    draft: DraftAnswer | None = None
    status: str = "pending"
    review_reason: str | None = None


@dataclass
class ProposalRunResult:
    questions: list[QuestionRun] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = ["# Proposal Draft", ""]
        for idx, qr in enumerate(self.questions, start=1):
            lines.append(f"## {idx}. {qr.question.prompt}")
            lines.append("")
            lines.append(qr.draft.answer if qr.draft else "No answer generated.")
            lines.append("")
            if qr.draft and qr.draft.citations:
                lines.append(f"Citations: {', '.join(qr.draft.citations)}")
                lines.append("")
        return "\n".join(lines)


def run_proposal_graph(rfp_text: str) -> ProposalRunResult:
    parsed_questions = parse_rfp_into_questions(rfp_text)
    result = ProposalRunResult()

    for question in parsed_questions:
        run = QuestionRun(question=question)
        while run.loops < settings.max_review_loops:
            context = research_question(question)
            run.draft = draft_answer(question, context)
            review = review_answer(question, run.draft)
            run.loops += 1
            run.review_reason = review.reason
            if review.passed:
                run.status = "passed"
                break
            if review.route == "rewrite_needed":
                continue
            if review.route == "needs_more_context":
                continue
        else:
            run.status = "failed_review"

        if run.status == "pending":
            run.status = "failed_review"
        result.questions.append(run)
    return result
