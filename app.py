# app.py
import os
from pathlib import Path

import streamlit as st

from ats_resume_optimizer import run_resume_agent
from ats_resume_optimizer.config import RESUME_DIR, OUTPUT_DIR
from ats_resume_optimizer.templates import TEMPLATES, get_template_choices

st.set_page_config(
    page_title="ATS Resume Optimizer", page_icon="📄", layout="centered"
)

# ── Sidebar ──────────────────────────────────────────────────────────────────

st.sidebar.header("⚙️ Configuration")

api_key = st.sidebar.text_input(
    "OpenAI API key",
    type="password",
    placeholder="sk-… (or set OPENAI_API_KEY in .env)",
    help="Required for resume optimization. Can also be set via OPENAI_API_KEY in a .env file.",
)

target_score = st.sidebar.slider(
    "Target ATS score", min_value=70, max_value=100, value=95, step=1
)

max_iterations = st.sidebar.number_input(
    "Max optimization iterations", min_value=1, max_value=10, value=5, step=1
)

st.sidebar.divider()

use_default_resume = st.sidebar.checkbox(
    "Use default resume (memory/docs)", value=True
)

uploaded_resume = None
if not use_default_resume:
    uploaded_resume = st.sidebar.file_uploader("Upload resume PDF", type=["pdf"])

# ── Main area ────────────────────────────────────────────────────────────────

st.title("📄 AI ATS Resume Optimizer")
st.caption(
    "Upload your resume, paste a job description, pick a premium theme, "
    "and get an ATS-optimized PDF in seconds."
)

st.markdown("### 💼 Job Info")

jd_url = st.text_input("Job URL (optional)")
jd_text = st.text_area("Job description (optional)", height=200)
st.caption(
    "Provide a job URL, a job description, or both (description takes precedence)."
)

# ── Theme & Color selection ──────────────────────────────────────────────────

st.markdown("### 🎨 Resume Style")

template_choices = get_template_choices()
template_labels = {t[1]: t[0] for t in template_choices}

col_theme, col_color = st.columns([3, 1])

with col_theme:
    selected_label = st.selectbox(
        "Theme",
        options=list(template_labels.keys()),
        help="Choose a premium resume layout style",
    )
    selected_template_id = template_labels[selected_label]

with col_color:
    primary_color = st.color_picker("Accent color", value="#2563eb")

selected_meta = TEMPLATES[selected_template_id]
st.caption(f"**{selected_meta['name']}** — {selected_meta['description']}")

# ── Run ──────────────────────────────────────────────────────────────────────

st.divider()

run_button = st.button("🚀 Optimize Resume", type="primary", use_container_width=True)

if run_button:
    if not jd_text and not jd_url:
        st.error("Please provide at least a job URL or a job description.")
        st.stop()

    api_key_to_use = api_key.strip() if api_key else None
    if not api_key_to_use and not os.environ.get("OPENAI_API_KEY", "").strip():
        st.error(
            "Please enter your OpenAI API key in the sidebar, "
            "or set OPENAI_API_KEY in a .env file."
        )
        st.stop()

    if use_default_resume:
        base_resume_path = RESUME_DIR / "base_resume.pdf"
        if not base_resume_path.exists():
            st.error(f"Default resume not found at: {base_resume_path}")
            st.stop()
    else:
        if not uploaded_resume:
            st.error("Please upload a resume PDF or enable 'Use default resume'.")
            st.stop()
        base_resume_path = RESUME_DIR / "uploaded_resume.pdf"
        RESUME_DIR.mkdir(parents=True, exist_ok=True)
        with open(base_resume_path, "wb") as f:
            f.write(uploaded_resume.getbuffer())

    # ── Iteration progress display ───────────────────────────────────────
    progress_placeholder = st.empty()
    iteration_lines: list[str] = []

    def on_iteration(data: dict) -> None:
        i = data["iteration"]
        score = data["ats_score"]
        improvements = data["improvements"]
        changes_summary = data.get("changes_summary", "")

        resolved = [imp["keyword"] for imp in improvements if imp["resolved"]]
        pending = [imp["keyword"] for imp in improvements if not imp["resolved"]]

        parts = [f"**Iteration {i}** — Score: **{score}**/100"]
        if resolved:
            resolved_str = "  ".join(f"✅ {kw}" for kw in resolved)
            parts.append(resolved_str)
        if pending:
            parts.append(f"⬜ Missing: {', '.join(pending)}")
        if score >= target_score:
            parts.append("🎯 **Target reached!**")

        header = " &nbsp;|&nbsp; ".join(parts)
        if changes_summary:
            header += f"\n\n> 📝 {changes_summary}"

        iteration_lines.append(header)
        progress_placeholder.markdown("\n\n---\n\n".join(iteration_lines))

    # ── Run optimization ─────────────────────────────────────────────────
    with st.status("Optimizing resume…", expanded=True) as status:
        st.write("Extracting resume text and analyzing job description…")
        try:
            output_pdf_path: Path = run_resume_agent(
                base_resume_pdf=base_resume_path,
                jd_text=jd_text.strip() or None,
                jd_url=jd_url.strip() or None,
                target_score=target_score,
                max_iterations=max_iterations,
                template_id=selected_template_id,
                primary_color=primary_color,
                api_key=api_key_to_use,
                on_iteration=on_iteration,
            )
        except Exception as e:
            status.update(label="Optimization failed", state="error")
            st.error(f"Error during optimization: {e}")
            st.stop()

        status.update(label="✅ Optimization complete!", state="complete")

    # ── Results ──────────────────────────────────────────────────────────
    st.success(f"Resume optimized! Saved to: **{output_pdf_path.name}**")

    with open(output_pdf_path, "rb") as f:
        pdf_bytes = f.read()

    st.download_button(
        label="⬇️ Download Optimized Resume (PDF)",
        data=pdf_bytes,
        file_name=output_pdf_path.name,
        mime="application/pdf",
        type="primary",
    )
