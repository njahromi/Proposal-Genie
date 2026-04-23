from app.agents.graph import run_proposal_graph


def test_graph_generates_answers() -> None:
    text = "1. What is enterprise pricing?\n2. Describe your security policy under 100 words?"
    result = run_proposal_graph(text)
    assert len(result.questions) >= 1
    assert result.questions[0].draft is not None
