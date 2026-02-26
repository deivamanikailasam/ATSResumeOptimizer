# app.py
import hashlib
import os
from pathlib import Path

import streamlit as st

from ats_resume_optimizer.agent import optimize_resume, export_resume_pdf
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


# ── Input fingerprinting for cache invalidation ─────────────────────────────

def _compute_input_fingerprint() -> str:
    """Hash all non-style inputs so we can detect when cache must be cleared."""
    uploaded_id = ""
    if not use_default_resume and uploaded_resume is not None:
        uploaded_id = f"{uploaded_resume.name}:{uploaded_resume.size}"
    parts = [
        str(use_default_resume),
        uploaded_id,
        jd_text.strip(),
        jd_url.strip(),
        str(target_score),
        str(max_iterations),
    ]
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


current_fingerprint = _compute_input_fingerprint()

if st.session_state.get("_opt_fingerprint") != current_fingerprint:
    st.session_state.pop("_opt_content_html", None)
    st.session_state.pop("_opt_job_title", None)
    st.session_state.pop("_opt_company", None)
    st.session_state["_opt_fingerprint"] = current_fingerprint

has_cached = "_opt_content_html" in st.session_state


# ── Run ──────────────────────────────────────────────────────────────────────

st.divider()

col_opt, col_export = st.columns(2)

with col_opt:
    run_button = st.button(
        "🔄 Regenerate" if has_cached else "🚀 Optimize Resume",
        type="primary",
        use_container_width=True,
    )

with col_export:
    export_button = st.button(
        "🎨 Re-export with Style",
        use_container_width=True,
        disabled=not has_cached,
        help="Use cached optimized content with the current theme & color"
        if has_cached
        else "Optimize a resume first",
    )


def _resolve_resume_path() -> Path | None:
    """Validate and return the resume path, or show errors and return None."""
    if use_default_resume:
        path = RESUME_DIR / "base_resume.pdf"
        if not path.exists():
            st.error(f"Default resume not found at: {path}")
            return None
        return path
    if not uploaded_resume:
        st.error("Please upload a resume PDF or enable 'Use default resume'.")
        return None
    path = RESUME_DIR / "uploaded_resume.pdf"
    RESUME_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(uploaded_resume.getbuffer())
    return path


def _validate_common_inputs() -> str | None:
    """Validate JD and API key. Returns the API key to use, or None on failure."""
    if not jd_text and not jd_url:
        st.error("Please provide at least a job URL or a job description.")
        return None
    key = api_key.strip() if api_key else None
    if not key and not os.environ.get("OPENAI_API_KEY", "").strip():
        st.error(
            "Please enter your OpenAI API key in the sidebar, "
            "or set OPENAI_API_KEY in a .env file."
        )
        return None
    return key or ""


# ── Full optimization ────────────────────────────────────────────────────────

if run_button:
    api_key_to_use = _validate_common_inputs()
    if api_key_to_use is None:
        st.stop()

    base_resume_path = _resolve_resume_path()
    if base_resume_path is None:
        st.stop()

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

    with st.status("Optimizing resume…", expanded=True) as status:
        st.write("Extracting resume text and analyzing job description…")
        try:
            result = optimize_resume(
                base_resume_pdf=base_resume_path,
                jd_text=jd_text.strip() or None,
                jd_url=jd_url.strip() or None,
                target_score=target_score,
                max_iterations=max_iterations,
                primary_color=primary_color,
                api_key=api_key_to_use or None,
                on_iteration=on_iteration,
            )
        except Exception as e:
            status.update(label="Optimization failed", state="error")
            st.error(f"Error during optimization: {e}")
            st.stop()

        status.update(label="✅ Optimization complete!", state="complete")

    st.session_state["_opt_content_html"] = result["content_html"]
    st.session_state["_opt_job_title"] = result["job_title"]
    st.session_state["_opt_company"] = result["company"]
    st.session_state["_opt_fingerprint"] = current_fingerprint

    with st.status("Generating PDF…") as pdf_status:
        try:
            output_pdf_path = export_resume_pdf(
                content_html=result["content_html"],
                template_id=selected_template_id,
                primary_color=primary_color,
                job_title=result["job_title"],
                company=result["company"],
            )
        except Exception as e:
            pdf_status.update(label="PDF export failed", state="error")
            st.error(f"Error generating PDF: {e}")
            st.stop()
        pdf_status.update(label="✅ PDF ready!", state="complete")

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

# ── Re-export with new style (cached) ────────────────────────────────────────

if export_button and has_cached:
    content_html = st.session_state["_opt_content_html"]
    job_title = st.session_state["_opt_job_title"]
    company = st.session_state["_opt_company"]

    with st.status("Generating PDF with new style…") as pdf_status:
        try:
            output_pdf_path = export_resume_pdf(
                content_html=content_html,
                template_id=selected_template_id,
                primary_color=primary_color,
                job_title=job_title,
                company=company,
            )
        except Exception as e:
            pdf_status.update(label="PDF export failed", state="error")
            st.error(f"Error generating PDF: {e}")
            st.stop()
        pdf_status.update(label="✅ PDF ready!", state="complete")

    st.success(f"PDF re-exported with new style! Saved to: **{output_pdf_path.name}**")
    with open(output_pdf_path, "rb") as f:
        pdf_bytes = f.read()
    st.download_button(
        label="⬇️ Download Optimized Resume (PDF)",
        data=pdf_bytes,
        file_name=output_pdf_path.name,
        mime="application/pdf",
        type="primary",
    )
