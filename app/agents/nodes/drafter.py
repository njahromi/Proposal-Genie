from __future__ import annotations

from app.llm.llm_client import llm_client
from app.models import DraftAnswer, RetrievedContext, RFPQuestion


FEW_SHOT_BRAND_VOICE = """
You are writing in a concise, confident B2B SaaS proposal style.
Example style:
- We deliver measurable outcomes with transparent SLAs.
- We avoid vague claims and ground statements in evidence.
"""


def draft_answer(question: RFPQuestion, context: RetrievedContext) -> DraftAnswer:
    prompt = f"""
{FEW_SHOT_BRAND_VOICE}

Question:
{question.prompt}

Constraint:
Keep response under {question.max_words} words.

Context snippets:
{context.snippets}

Structured facts:
{context.sql_rows}

Write only the answer body.
"""
    result = llm_client.generate(prompt=prompt, task_type="summarization", temperature=0.2)
    return DraftAnswer(question_id=question.id, answer=result.text, citations=context.citations)
