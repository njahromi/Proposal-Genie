from __future__ import annotations

from io import BytesIO
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.agents.graph import ProposalRunResult, run_proposal_graph

router = APIRouter(prefix="/rfp", tags=["rfp"])
RUN_STORE: dict[str, ProposalRunResult] = {}


class ProcessRequest(BaseModel):
    rfp_text: str


@router.post("/upload")
async def upload_rfp(file: UploadFile = File(...)) -> dict:
    content = await file.read()
    text = extract_text(file.filename, content)
    run = run_proposal_graph(text)
    run_id = str(uuid4())
    RUN_STORE[run_id] = run
    return {"run_id": run_id, "question_count": len(run.questions)}


@router.post("/process")
def process_rfp(payload: ProcessRequest) -> dict:
    run = run_proposal_graph(payload.rfp_text)
    run_id = str(uuid4())
    RUN_STORE[run_id] = run
    return {"run_id": run_id, "question_count": len(run.questions)}


@router.get("/status/{run_id}")
def get_status(run_id: str) -> dict:
    run = RUN_STORE.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    passed = sum(1 for item in run.questions if item.status == "passed")
    return {"run_id": run_id, "total_questions": len(run.questions), "passed_questions": passed}


@router.get("/export/{run_id}")
def export_run(run_id: str) -> dict:
    run = RUN_STORE.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"run_id": run_id, "proposal_markdown": run.to_markdown()}


def extract_text(filename: str | None, content: bytes) -> str:
    if filename and filename.lower().endswith(".pdf"):
        try:
            from pypdf import PdfReader

            reader = PdfReader(BytesIO(content))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            return content.decode("utf-8", errors="ignore")
    return content.decode("utf-8", errors="ignore")
