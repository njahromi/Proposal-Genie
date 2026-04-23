from __future__ import annotations

import re
from uuid import uuid4

from app.models import RFPQuestion


def parse_rfp_into_questions(rfp_text: str) -> list[RFPQuestion]:
    lines = [line.strip() for line in rfp_text.splitlines() if line.strip()]
    question_like = [
        line
        for line in lines
        if line.endswith("?") or re.match(r"^(\d+[\).\s]|-\s+)", line)
    ]
    if not question_like:
        question_like = [line for line in lines[:10]]

    questions: list[RFPQuestion] = []
    for item in question_like:
        max_words = 500
        match = re.search(r"(\d+)\s*words?", item.lower())
        if match:
            max_words = int(match.group(1))
        questions.append(
            RFPQuestion(
                id=str(uuid4()),
                prompt=item,
                max_words=max_words,
            )
        )
    return questions
