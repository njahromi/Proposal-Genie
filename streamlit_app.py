from __future__ import annotations

import streamlit as st

from app.agents.graph import run_proposal_graph

st.set_page_config(page_title="Proposal-Genie Demo", layout="wide")
st.title("Proposal-Genie: Multi-Agent RFP Automation")

rfp_text = st.text_area(
    "Paste RFP content",
    height=260,
    value="1. Describe your security policy in under 150 words?\n2. What is enterprise pricing?",
)

if st.button("Run Proposal-Genie"):
    with st.spinner("Processing..."):
        result = run_proposal_graph(rfp_text)

    st.success("Run complete")
    for idx, qr in enumerate(result.questions, start=1):
        with st.expander(f"Question {idx}: {qr.question.prompt}"):
            st.write(f"Status: {qr.status}")
            st.write(f"Loops: {qr.loops}")
            st.write(f"Review: {qr.review_reason}")
            if qr.draft:
                st.markdown(qr.draft.answer)
                st.caption(f"Citations: {', '.join(qr.draft.citations)}")

    st.download_button(
        "Download proposal markdown",
        data=result.to_markdown(),
        file_name="proposal_draft.md",
        mime="text/markdown",
    )
