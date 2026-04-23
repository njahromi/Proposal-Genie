from __future__ import annotations

import sqlite3
from pathlib import Path

from app.config import settings


ALLOWED_TABLES = {"pricing", "availability"}


class SQLRetriever:
    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or settings.sql_db_path
        self._ensure_seed_data()

    def _ensure_seed_data(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS pricing (sku TEXT PRIMARY KEY, plan_name TEXT, monthly_price REAL)"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS availability (region TEXT PRIMARY KEY, uptime_sla REAL, status TEXT)"
        )
        cursor.execute("INSERT OR IGNORE INTO pricing VALUES ('PG-STD','Standard',99.0)")
        cursor.execute("INSERT OR IGNORE INTO pricing VALUES ('PG-ENT','Enterprise',499.0)")
        cursor.execute("INSERT OR IGNORE INTO availability VALUES ('us-east',99.95,'healthy')")
        cursor.execute("INSERT OR IGNORE INTO availability VALUES ('eu-west',99.9,'healthy')")
        conn.commit()
        conn.close()

    def safe_execute(self, sql_query: str) -> list[dict]:
        lowered = sql_query.lower()
        if "drop " in lowered or "delete " in lowered or "update " in lowered or "insert " in lowered:
            raise ValueError("Unsafe SQL operation detected.")
        if not any(f" {table}" in lowered or f"from {table}" in lowered for table in ALLOWED_TABLES):
            raise ValueError("Query references a non-allowlisted table.")

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def text_to_sql(self, question: str) -> str:
        q = question.lower()
        if "price" in q or "cost" in q:
            return "SELECT sku, plan_name, monthly_price FROM pricing;"
        if "availability" in q or "sla" in q or "uptime" in q:
            return "SELECT region, uptime_sla, status FROM availability;"
        return "SELECT sku, plan_name, monthly_price FROM pricing;"


sql_retriever = SQLRetriever()
