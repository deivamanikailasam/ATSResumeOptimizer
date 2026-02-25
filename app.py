# app.py
import os
from pathlib import Path

import streamlit as st

from ats_resume_optimizer import run_resume_agent
from ats_resume_optimizer.config import RESUME_DIR, OUTPUT_DIR

st.set_page_config(
    page_title="ATS Resume Optimizer", page_icon="📄", layout="centered"
)

st.title("📄 AI ATS Resume Optimizer")
st.write(
    "Upload your base resume PDF (or use the one in memory/docs), "
    "paste a job description or URL, and get a tailored PDF optimized for ATS."
)

# Sidebar config
st.sidebar.header("Configuration")

# OpenAI API key: UI input (optional if set in .env)
api_key_placeholder = (
    "Or set OPENAI_API_KEY in .env to skip entering here"
)
api_key = st.sidebar.text_input(
    "OpenAI API key",
    type="password",
    placeholder=api_key_placeholder,
    help="Required for resume optimization. You can also set OPENAI_API_KEY in a .env file.",
)

target_score = st.sidebar.slider(
    "Target ATS score", min_value=70, max_value=100, value=95, step=1
)
use_default_resume = st.sidebar.checkbox(
    "Use default resume in memory/docs", value=True
)

uploaded_resume = None
if not use_default_resume:
    uploaded_resume = st.sidebar.file_uploader("Upload resume PDF", type=["pdf"])

st.markdown("### Job Info")

jd_url = st.text_input("Job URL (optional)")
jd_text = st.text_area("Job description (optional)", height=250)

st.caption("Provide either a job URL, a job description, or both (description takes precedence).")

run_button = st.button("Optimize Resume")

if run_button:
    if not jd_text and not jd_url:
        st.error("Please provide at least a job URL or a job description.")
        st.stop()

    # API key: use UI value if non-empty, else None (env will be used by agent)
    api_key_to_use = api_key.strip() if api_key else None
    if not api_key_to_use and not os.environ.get("OPENAI_API_KEY", "").strip():
        st.error(
            "Please enter your OpenAI API key in the sidebar, or set OPENAI_API_KEY in a .env file."
        )
        st.stop()

    # Determine base resume path / source
    if use_default_resume:
        base_resume_path = RESUME_DIR / "base_resume.pdf"
        if not base_resume_path.exists():
            st.error(f"Default resume not found at: {base_resume_path}")
            st.stop()
    else:
        if not uploaded_resume:
            st.error("Please upload a resume PDF or enable 'Use default resume'.")
            st.stop()
        # Save uploaded resume to a temp path under memory/docs
        base_resume_path = RESUME_DIR / "uploaded_resume.pdf"
        RESUME_DIR.mkdir(parents=True, exist_ok=True)
        with open(base_resume_path, "wb") as f:
            f.write(uploaded_resume.getbuffer())

    with st.spinner("Optimizing resume with AI... this may take up to a minute."):
        try:
            output_pdf_path: Path = run_resume_agent(
                base_resume_pdf=base_resume_path,
                jd_text=jd_text.strip() or None,
                jd_url=jd_url.strip() or None,
                target_score=target_score,
                api_key=api_key_to_use,
            )
        except Exception as e:
            st.error(f"Error during optimization: {e}")
            st.stop()

    st.success(f"Resume optimized successfully! Saved to: {output_pdf_path}")

    # Read the generated PDF into memory for download_button
    with open(output_pdf_path, "rb") as f:
        pdf_bytes = f.read()

    st.download_button(
        label="⬇️ Download optimized resume (PDF)",
        data=pdf_bytes,
        file_name=output_pdf_path.name,
        mime="application/pdf",  # per Streamlit docs for binary file download[web:16][web:19]
        type="primary",
    )

    # Optionally show some metadata
    st.write("**Output file name:**", output_pdf_path.name)
    st.write("**Saved in:**", OUTPUT_DIR)
