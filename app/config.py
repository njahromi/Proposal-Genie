from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    app_name: str = "Proposal-Genie"
    app_env: str = os.getenv("APP_ENV", "dev")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    default_model: str = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "./.chroma")
    sql_db_path: str = os.getenv("SQL_DB_PATH", "./app/data/company.db")
    max_review_loops: int = int(os.getenv("MAX_REVIEW_LOOPS", "3"))


settings = Settings()
