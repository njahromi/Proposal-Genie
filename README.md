# Proposal-Genie: Multi-Agent RFP Automation

Proposal-Genie is a job-ready backend project that automates RFP responses using a multi-node agent workflow, hybrid retrieval (vector + SQL), and evaluation reporting.

## What it demonstrates
- Multi-step stateful agent workflow with review loop behavior.
- Hybrid RAG with query routing between unstructured and structured sources.
- Unified LLM abstraction with model routing, retries, and fallback behavior.
- Evaluation runner with a golden dataset and quality metrics.

## Architecture
1. `Orchestrator` parses RFP text into individual questions and constraints.
2. `Researcher` routes each question to vector retrieval, SQL retrieval, or both.
3. `Drafter` generates an answer using context only.
4. `Reviewer` validates word limits and grounding, then loops back if needed.
5. Final answers compile into a proposal document.

## Project structure
- `app/main.py` - FastAPI app and startup seeding.
- `app/api/rfp.py` - upload/process/status/export endpoints.
- `app/agents/graph.py` - cyclical workflow engine.
- `app/agents/nodes/*` - orchestrator, researcher, drafter, reviewer logic.
- `app/retrieval/*` - router, vector store, SQL retriever.
- `app/llm/llm_client.py` - provider-standardized LLM client.
- `app/evals/run_eval.py` - evaluation runner.
- `streamlit_app.py` - optional visual demo of run traces.

## Quickstart
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run API:
```bash
uvicorn app.main:app --reload
```

Run evaluation:
```bash
python -m app.evals.run_eval
```

Run Streamlit demo:
```bash
streamlit run streamlit_app.py
```

## API endpoints
- `POST /rfp/upload` - upload TXT/PDF and process immediately.
- `POST /rfp/process` - submit raw RFP text.
- `GET /rfp/status/{run_id}` - run progress summary.
- `GET /rfp/export/{run_id}` - proposal markdown output.
- `GET /health` - health check.

## Notes for contributors
- The code is intentionally modular
- You can swap in real OpenAI/Anthropic SDK calls inside `LLMClient._simulate_or_call`.
- You can replace in-memory vector retrieval with Chroma/Pinecone and connect LangSmith/Ragas instrumentation.
