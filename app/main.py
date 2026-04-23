from __future__ import annotations

from fastapi import FastAPI

from app.api.rfp import router as rfp_router
from app.config import settings
from app.retrieval.vector_store import VectorDocument, vector_store


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.include_router(rfp_router)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "app": settings.app_name}

    @app.on_event("startup")
    def seed_vector_data() -> None:
        if vector_store.search("security policy"):
            return
        vector_store.add_documents(
            [
                VectorDocument(
                    doc_id="policy-001",
                    source="employee_handbook.pdf",
                    content=(
                        "Our security policy includes annual penetration tests, SOC2 controls, "
                        "and least-privilege access for customer systems."
                    ),
                ),
                VectorDocument(
                    doc_id="proposal-001",
                    source="past_proposal_acme.pdf",
                    content=(
                        "Implementation follows a phased rollout with weekly governance updates "
                        "and a dedicated solution architect."
                    ),
                ),
            ]
        )

    return app


app = create_app()
