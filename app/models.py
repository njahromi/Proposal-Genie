from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RetrievalMode(str, Enum):
    VECTOR = "vector"
    SQL = "sql"
    HYBRID = "hybrid"


@dataclass
class RFPQuestion:
    id: str
    prompt: str
    max_words: int = 500
    section: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RetrievedContext:
    question_id: str
    mode: RetrievalMode
    snippets: list[str] = field(default_factory=list)
    sql_rows: list[dict[str, Any]] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)


@dataclass
class DraftAnswer:
    question_id: str
    answer: str
    citations: list[str] = field(default_factory=list)


@dataclass
class ReviewResult:
    question_id: str
    passed: bool
    reason: str
    route: str
