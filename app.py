# app.py
import hashlib
import os
import threading
import time
from pathlib import Path

import streamlit as st

from ats_resume_optimizer.agent import (
    apply_resume_edit,
    convert_resume,
    export_resume_pdf,
    optimize_resume,
)
from ats_resume_optimizer.config import RESUME_DIR, OUTPUT_DIR
from ats_resume_optimizer.templates import TEMPLATES, get_template_choices, render_resume

st.set_page_config(
    page_title="ATS Resume Optimizer", page_icon="📄", layout="centered"
)


# ── Disk cleanup helpers ─────────────────────────────────────────────────────

def _cleanup_generated_pdfs():
    if OUTPUT_DIR.exists():
        for f in OUTPUT_DIR.iterdir():
            if f.is_file():
                f.unlink(missing_ok=True)


def _cleanup_uploaded_resume():
    (RESUME_DIR / "uploaded_resume.pdf").unlink(missing_ok=True)


if "_session_initialized" not in st.session_state:
    _cleanup_generated_pdfs()
    _cleanup_uploaded_resume()
    st.session_state["_session_initialized"] = True

# ── Sidebar ──────────────────────────────────────────────────────────────────

st.sidebar.header("⚙️ Configuration")

api_key = st.sidebar.text_input(
    "OpenAI API key",
    type="password",
    placeholder="sk-… (or set OPENAI_API_KEY in .env)",
    help="Required. Can also be set via OPENAI_API_KEY in a .env file.",
)
_env_key_set = bool(os.environ.get("OPENAI_API_KEY", "").strip())
if api_key.strip():
    st.sidebar.caption("✅ API key entered")
elif _env_key_set:
    st.sidebar.caption("✅ Using OPENAI_API_KEY from environment")
else:
    st.sidebar.caption("⚠️ API key required to run the optimizer")

uploaded_resume = st.sidebar.file_uploader("Upload base resume PDF", type=["pdf"])
if uploaded_resume:
    _size_kb = uploaded_resume.size // 1024
    st.sidebar.caption(f"✅ {uploaded_resume.name} ({_size_kb} KB)")
else:
    st.sidebar.caption("ℹ️ Upload your base resume PDF to get started")

# ── Main area — Header ──────────────────────────────────────────────────────

@st.dialog("How to Use This App", width="large")
def _show_help():
    st.markdown(
        """
#### Setup
1. **API Key** — paste your OpenAI key in the sidebar (or set
   `OPENAI_API_KEY` in a `.env` file).
2. **Upload Resume** — upload your base resume PDF in the sidebar.

---

#### Tab 1: ATS Optimize
Tailor your resume for a specific job posting.

1. Paste the **Job URL** or **Job description text** (or both).
2. Pick a **Theme** and **Accent color**.
3. **Strict Optimization** (default: on) — keeps all content 100% faithful
   to your base resume. Uncheck to allow the AI broader creative latitude.
4. Click **🚀 Optimize Resume** — the AI iteratively refines your
   resume to maximize ATS keyword coverage.
5. **Download** the optimized PDF using the green button that appears,
   or **Re-export** with a different style without re-running the AI.
6. Use the **Edit** section (scroll down after results appear) to make
   further changes in plain English.
7. After each edit, a **Download Current Resume** button appears
   directly below the chat history — always up-to-date.

---

#### Tab 2: Edit Resume
Edit your resume freely — no job description needed.

1. Pick a **Theme** and **Accent color**.
2. Click **📄 Load Resume** to convert your uploaded PDF into a
   themed, editable format.
3. Describe changes in plain English:
   - *"Add Docker and Kubernetes to skills"*
   - *"Rewrite the summary to emphasize leadership"*
   - *"Remove the Projects section"*
4. Click **✏️ Apply Edit** — the AI updates your resume and
   regenerates the PDF instantly.
5. The **Download Current Resume** button below the chat always
   reflects the latest version of your resume.
6. Use **↩️ Undo** to revert the last edit.

---

> **Tip:** Results persist across page refreshes during your session.
> Each tab maintains its own independent state.
> Use **👁️ Preview** to see your resume without downloading.
"""
    )

st.markdown(
    """<style>
    [data-testid="stButton"] button p {
        margin: 0;
        line-height: 1;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    </style>""",
    unsafe_allow_html=True,
)

_version = (Path(__file__).parent / "VERSION").read_text(encoding="utf-8").strip()

col_title, col_help = st.columns([10, 0.6], vertical_alignment="bottom")
with col_title:
    st.markdown(
        f'<h1 style="margin:0">📄 AI ATS Resume Optimizer'
        f' <span style="font-size:0.4em;color:gray">v{_version}</span></h1>',
        unsafe_allow_html=True,
    )
with col_help:
    if st.button("❓", help="How to use this app", key="help_btn"):
        _show_help()
st.caption(
    "Upload your resume, pick a theme, then optimize for a job or edit freely."
)

_DL_LABEL_OPT = "⬇️ Download Optimized Resume (PDF)"
_DL_LABEL_RESUME = "⬇️ Download Resume (PDF)"

# ── Theme & Color (shared across tabs) ───────────────────────────────────────

st.markdown("### 🎨 Resume Style")

template_choices = get_template_choices()
template_labels = {t[1]: t[0] for t in template_choices}

_PREVIEW_CONTENT_HTML = """\
<div class="resume-header">
    <h1>Alexandra Chen</h1>
    <div class="contact-info">
        <span>alex.chen@email.com</span>
        <span>(415) 987-6543</span>
        <span>San Francisco, CA</span>
        <span>linkedin.com/in/alexandrachen</span>
    </div>
</div>
<div class="resume-section summary">
    <h2>Professional Summary</h2>
    <p>Results-driven Senior Software Engineer with 8+ years of experience building \
scalable cloud-native applications. Proven track record of leading cross-functional \
teams and delivering high-impact products that serve millions of users.</p>
</div>
<div class="resume-section skills">
    <h2>Technical Skills</h2>
    <div class="skills-grid">
        <div class="skill-category">
            <strong>Languages:</strong>
            <span class="skill-tag">Python</span>
            <span class="skill-tag">TypeScript</span>
            <span class="skill-tag">Go</span>
            <span class="skill-tag">SQL</span>
        </div>
        <div class="skill-category">
            <strong>Frameworks:</strong>
            <span class="skill-tag">React</span>
            <span class="skill-tag">FastAPI</span>
            <span class="skill-tag">Next.js</span>
            <span class="skill-tag">Django</span>
        </div>
        <div class="skill-category">
            <strong>Cloud & DevOps:</strong>
            <span class="skill-tag">AWS</span>
            <span class="skill-tag">Docker</span>
            <span class="skill-tag">Kubernetes</span>
            <span class="skill-tag">Terraform</span>
        </div>
    </div>
</div>
<div class="resume-section experience">
    <h2>Professional Experience</h2>
    <div class="experience-item">
        <div class="item-header">
            <h3>Senior Software Engineer</h3>
            <span class="date">Jan 2022 – Present</span>
        </div>
        <div class="company">Stripe · San Francisco, CA</div>
        <ul>
            <li>Led architecture redesign of payment processing pipeline, reducing \
latency by 40% and handling 2M+ daily transactions.</li>
            <li>Mentored a team of 5 engineers and established code review standards \
that cut production bugs by 30%.</li>
        </ul>
    </div>
    <div class="experience-item">
        <div class="item-header">
            <h3>Software Engineer</h3>
            <span class="date">Jun 2019 – Dec 2021</span>
        </div>
        <div class="company">Airbnb · San Francisco, CA</div>
        <ul>
            <li>Built real-time search ranking service using ML models, improving \
booking conversion by 18%.</li>
            <li>Designed and deployed microservices architecture serving 50M+ monthly \
active users.</li>
        </ul>
    </div>
</div>
<div class="resume-section education">
    <h2>Education</h2>
    <div class="education-item">
        <div class="item-header">
            <h3>M.S. Computer Science</h3>
            <span class="date">2017 – 2019</span>
        </div>
        <div class="company">Stanford University · Stanford, CA</div>
    </div>
</div>
<div class="resume-section certifications">
    <h2>Certifications</h2>
    <ul class="cert-list">
        <li><strong>AWS Solutions Architect Professional</strong> – Amazon (2023)</li>
        <li><strong>Certified Kubernetes Administrator</strong> – CNCF (2022)</li>
    </ul>
</div>
"""


@st.dialog("Theme Preview", width="large")
def _show_theme_preview(template_id: str, color: str):
    import streamlit.components.v1 as components

    meta = TEMPLATES[template_id]
    st.caption(f"**{meta['name']}** — {meta['description']}")
    full_html = render_resume(template_id, _PREVIEW_CONTENT_HTML, color)
    doc_style = """
    <style>
        html { background: #f0f0f0; }
        body {
            background: #fff;
            max-width: 800px;
            margin: 20px auto;
            padding: 24px;
            box-shadow: 0 2px 16px rgba(0,0,0,0.12);
            border-radius: 4px;
        }
    </style>
    """
    full_html = full_html.replace("</head>", doc_style + "</head>", 1)
    components.html(full_html, height=700, scrolling=True)


@st.dialog("Resume Preview", width="large")
def _show_resume_preview(content_html: str, template_id: str, color: str):
    """Show the rendered resume HTML in a scrollable dialog."""
    import streamlit.components.v1 as components

    meta = TEMPLATES[template_id]
    st.caption(f"**{meta['name']}** — previewing your actual resume content")
    full_html = render_resume(template_id, content_html, color)
    doc_style = """
    <style>
        html { background: #f0f0f0; }
        body {
            background: #fff;
            max-width: 800px;
            margin: 20px auto;
            padding: 24px;
            box-shadow: 0 2px 16px rgba(0,0,0,0.12);
            border-radius: 4px;
        }
    </style>
    """
    full_html = full_html.replace("</head>", doc_style + "</head>", 1)
    components.html(full_html, height=700, scrolling=True)


col_theme, col_color, col_preview = st.columns([3, 1, 0.4])

with col_theme:
    selected_label = st.selectbox(
        "Theme",
        options=list(template_labels.keys()),
        help="Choose a premium resume layout style",
    )
    selected_template_id = template_labels[selected_label]

with col_color:
    primary_color = st.color_picker("Accent color", value="#2563eb")

with col_preview:
    st.markdown("<div style='height: 26px'></div>", unsafe_allow_html=True)
    if st.button("👁️", help="Preview this theme with sample data", key="preview_btn"):
        _show_theme_preview(selected_template_id, primary_color)

selected_meta = TEMPLATES[selected_template_id]
st.caption(f"**{selected_meta['name']}** — {selected_meta['description']}")


# ── Shared helpers ───────────────────────────────────────────────────────────


@st.dialog("Confirm Re-optimize", width="small")
def _confirm_reoptimize():
    st.warning(
        "Re-optimizing will **discard your current resume and all edits** "
        "and start fresh from your uploaded PDF."
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, re-optimize", type="primary", use_container_width=True):
            st.session_state["_opt_confirm_yes"] = True
            st.rerun()
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()


@st.dialog("Confirm Reload Resume", width="small")
def _confirm_reload_resume():
    st.warning(
        "Reloading will **discard all edits** you have made "
        "and convert the PDF from scratch."
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, reload", type="primary", use_container_width=True):
            st.session_state["_qe_confirm_yes"] = True
            st.rerun()
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()


def _resolve_resume_path() -> Path | None:
    if not uploaded_resume:
        st.error("Please upload a base resume PDF in the sidebar.")
        return None
    path = RESUME_DIR / "uploaded_resume.pdf"
    RESUME_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(uploaded_resume.getbuffer())
    return path


def _get_api_key() -> str | None:
    key = api_key.strip() if api_key else None
    if not key and not os.environ.get("OPENAI_API_KEY", "").strip():
        st.error(
            "Please enter your OpenAI API key in the sidebar, "
            "or set OPENAI_API_KEY in a .env file."
        )
        return None
    return key or ""


def _rebuild_pdf(content_html: str, company: str | None = None) -> tuple[bytes, str]:
    """Re-export PDF and return (pdf_bytes, filename)."""
    output_pdf_path = export_resume_pdf(
        content_html=content_html,
        template_id=selected_template_id,
        primary_color=primary_color,
        company=company,
    )
    with open(output_pdf_path, "rb") as f:
        pdf_bytes = f.read()
    return pdf_bytes, output_pdf_path.name


def _render_edit_section(
    content_key: str,
    history_key: str,
    undo_key: str,
    pdf_bytes_key: str,
    pdf_name_key: str,
    success_msg_key: str,
    company: str | None,
    form_id: str,
    applying_flag: str,
):
    """Render the shared AI edit UI. Used by both tabs."""
    st.divider()
    st.markdown("### ✏️ Edit Resume")
    st.caption(
        "Describe changes in plain English — the AI will update your resume "
        "and regenerate the PDF."
    )

    if history_key not in st.session_state:
        st.session_state[history_key] = []

    for edit in st.session_state[history_key]:
        with st.chat_message("user"):
            st.markdown(edit["instruction"])
        with st.chat_message("assistant", avatar="📄"):
            st.markdown(f"✅ {edit['summary']}")

    is_applying = st.session_state.get(applying_flag, False)

    if is_applying:
        pending = st.session_state.get(f"{applying_flag}_instruction", "")
        if pending:
            with st.chat_message("user"):
                st.markdown(pending)
            with st.chat_message("assistant", avatar="📄"):
                with st.spinner("Applying changes…"):
                    st.session_state.pop(applying_flag, None)
                    edit_api_key = st.session_state.pop(
                        f"{applying_flag}_api_key", ""
                    )
                    instruction = st.session_state.pop(
                        f"{applying_flag}_instruction", ""
                    )

                    try:
                        result = apply_resume_edit(
                            content_html=st.session_state[content_key],
                            instruction=instruction,
                            edit_history=st.session_state.get(history_key),
                            api_key=edit_api_key or None,
                        )
                    except Exception as e:
                        st.error(f"Edit failed: {e}")
                        st.stop()

                    st.session_state[undo_key] = st.session_state[content_key]
                    st.session_state[content_key] = result["updated_html"]

                    st.session_state[history_key].append({
                        "instruction": instruction,
                        "summary": result["changes_summary"],
                    })

                    try:
                        pdf_bytes, pdf_name = _rebuild_pdf(
                            result["updated_html"], company
                        )
                        st.session_state[pdf_bytes_key] = pdf_bytes
                        st.session_state[pdf_name_key] = pdf_name
                        st.session_state[success_msg_key] = (
                            "✅ Edit applied — resume updated."
                        )
                    except Exception as e:
                        st.error(f"PDF export failed: {e}")
                        st.stop()

                    st.markdown(f"✅ {result['changes_summary']}")

            st.rerun()

    # ── Persistent download – always visible when a PDF is ready ──────────
    if st.session_state.get(pdf_bytes_key):
        _dl_col, _pv_col = st.columns([5, 1])
        with _dl_col:
            st.download_button(
                label="⬇️ Download Current Resume (PDF)",
                data=st.session_state[pdf_bytes_key],
                file_name=st.session_state[pdf_name_key],
                mime="application/pdf",
                type="primary",
                key=f"{form_id}_dl_persistent",
                use_container_width=True,
            )
        with _pv_col:
            if st.button(
                "👁️",
                key=f"{form_id}_preview_btn",
                use_container_width=True,
                help="Preview current resume",
            ):
                _show_resume_preview(
                    st.session_state[content_key],
                    selected_template_id,
                    primary_color,
                )


    with st.form(form_id, clear_on_submit=True):
        edit_instruction = st.text_area(
            "What would you like to change?",
            placeholder=(
                "Examples:\n"
                "• Add 'Terraform' to the skills section\n"
                "• Rewrite the summary to emphasize leadership\n"
                "• Remove the Projects section\n"
                "• Change my job title at Acme Corp to 'Lead Engineer'\n"
                "• Add a bullet about reducing deployment time by 50%"
            ),
            height=100,
            label_visibility="collapsed",
        )

        col_apply, col_undo = st.columns([3, 1])
        with col_apply:
            apply_edit = st.form_submit_button(
                "✏️ Apply Edit",
                type="primary",
                use_container_width=True,
            )
        with col_undo:
            undo_edit = st.form_submit_button(
                "↩️ Undo",
                use_container_width=True,
                disabled=not st.session_state.get(undo_key),
            )

    if apply_edit and not edit_instruction.strip():
        st.warning("Please describe the changes you'd like to make before clicking Apply Edit.")

    if apply_edit and edit_instruction.strip():
        key_to_use = _get_api_key()
        if key_to_use is None:
            st.stop()
        st.session_state[applying_flag] = True
        st.session_state[f"{applying_flag}_instruction"] = edit_instruction.strip()
        st.session_state[f"{applying_flag}_api_key"] = key_to_use
        st.rerun()

    if undo_edit and st.session_state.get(undo_key):
        st.session_state[content_key] = st.session_state.pop(undo_key)
        if st.session_state.get(history_key):
            st.session_state[history_key].pop()
        try:
            pdf_bytes, pdf_name = _rebuild_pdf(
                st.session_state[content_key], company
            )
            st.session_state[pdf_bytes_key] = pdf_bytes
            st.session_state[pdf_name_key] = pdf_name
            st.session_state[success_msg_key] = (
                "↩️ Edit undone — previous version restored."
            )
        except Exception as e:
            st.error(f"PDF export failed after undo: {e}")
            st.stop()
        st.rerun()


# ── Tabs ─────────────────────────────────────────────────────────────────────

st.divider()
tab_optimize, tab_edit = st.tabs(["🎯 ATS Optimize", "✏️ Edit Resume"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: ATS OPTIMIZE
# ══════════════════════════════════════════════════════════════════════════════

_OPT_STATE_KEYS = (
    "_opt_content_html", "_opt_job_title", "_opt_company",
    "_opt_status_log", "_opt_pdf_bytes", "_opt_pdf_name",
    "_opt_success_msg", "_opt_edit_history", "_opt_edit_undo_html",
    # thread lifecycle keys — cleared at start of each new run
    "_opt_thread_active", "_opt_thread_done", "_opt_thread_result",
    "_opt_thread", "_opt_thread_state", "_opt_cancel_event", "_opt_error",
)

with tab_optimize:
    st.markdown("### 💼 Job Info")

    jd_url = st.text_input("Job URL (optional)", key="opt_jd_url")
    jd_text = st.text_area("Job description (optional)", height=200, key="opt_jd_text")
    st.caption(
        "Provide a job URL, a job description, or both (text takes precedence)."
    )

    strict_mode = st.checkbox(
        "🔒 Strict Optimization",
        value=True,
        key="opt_strict_mode",
        help=(
            "**Checked (recommended):** Optimization stays 100% faithful to your "
            "base resume. The AI can rephrase existing content using JD terminology, "
            "surface skills already demonstrated in your experience, expand acronyms, "
            "and restructure bullets — but will NEVER add skills, technologies, "
            "certifications, metrics, or experiences not present in your original resume.\n\n"
            "**Unchecked:** Standard optimization mode. The AI may add relevant skills "
            "or context beyond the base resume to maximize ATS keyword match rate."
        ),
    )

    # ── Fingerprinting for cache invalidation ────────────────────────────

    def _opt_fingerprint() -> str:
        uploaded_id = ""
        if uploaded_resume is not None:
            uploaded_id = f"{uploaded_resume.name}:{uploaded_resume.size}"
        parts = [uploaded_id, jd_text.strip(), jd_url.strip(), str(strict_mode)]
        return hashlib.sha256("|".join(parts).encode()).hexdigest()

    _opt_fp = _opt_fingerprint()

    if st.session_state.get("_opt_fingerprint") != _opt_fp:
        for _key in _OPT_STATE_KEYS:
            st.session_state.pop(_key, None)
        st.session_state["_opt_fingerprint"] = _opt_fp

    _opt_has_cached = "_opt_content_html" in st.session_state
    _opt_running = st.session_state.get("_opt_start", False)

    # ── Action buttons ───────────────────────────────────────────────────

    _opt_thread_active = st.session_state.get("_opt_thread_active", False)
    _opt_thread_state = st.session_state.get("_opt_thread_state", {})
    _opt_thread_done = bool(
        st.session_state.get("_opt_thread_done", False)
        or _opt_thread_state.get("done", False)
    )
    _is_busy = _opt_running or (_opt_thread_active and not _opt_thread_done)

    st.markdown("")
    if _opt_has_cached:
        col_opt_btn, col_exp_btn = st.columns(2)
        with col_opt_btn:
            if _is_busy:
                opt_run = False
                st.button(
                    "⏳ Optimizing…", disabled=True, type="primary",
                    use_container_width=True, key="opt_busy",
                )
            else:
                opt_run = st.button(
                    "🔄 Re-optimize", type="primary",
                    use_container_width=True, key="opt_rerun",
                )
        with col_exp_btn:
            if _is_busy:
                opt_export = False
                if _opt_thread_active and not _opt_thread_done:
                    if st.button(
                        "❌ Cancel",
                        type="secondary",
                        use_container_width=True,
                        key="opt_cancel",
                        help="Stop the current optimization",
                    ):
                        _ev = st.session_state.get("_opt_cancel_event")
                        if _ev:
                            _ev.set()
            else:
                opt_export = st.button(
                    "🎨 Re-export with Style",
                    use_container_width=True, key="opt_export",
                    help="Regenerate PDF with the current theme & accent color",
                )
    else:
        opt_export = False
        if _is_busy:
            opt_run = False
            col_busy, col_cancel = st.columns(2)
            with col_busy:
                st.button(
                    "⏳ Optimizing…", disabled=True, type="primary",
                    use_container_width=True, key="opt_busy2",
                )
            with col_cancel:
                if _opt_thread_active and not _opt_thread_done:
                    if st.button(
                        "❌ Cancel",
                        type="secondary",
                        use_container_width=True,
                        key="opt_cancel2",
                        help="Stop the current optimization",
                    ):
                        _ev = st.session_state.get("_opt_cancel_event")
                        if _ev:
                            _ev.set()
        else:
            opt_run = st.button(
                "🚀 Optimize Resume", type="primary",
                use_container_width=True, key="opt_go",
            )

    opt_results = st.empty()

    # ── Start optimization → clear state and rerun ───────────────────────

    if opt_run:
        if not jd_text.strip() and not jd_url.strip():
            st.error("Please provide at least a job URL or a job description.")
            st.stop()
        key_to_use = _get_api_key()
        if key_to_use is None:
            st.stop()
        resume_path = _resolve_resume_path()
        if resume_path is None:
            st.stop()

        # Confirm before discarding existing edits
        _has_opt_edits = bool(st.session_state.get("_opt_edit_history"))
        if _has_opt_edits and not st.session_state.pop("_opt_confirm_yes", False):
            _confirm_reoptimize()
            st.stop()

        # Cancel any running thread before starting fresh
        _ev = st.session_state.get("_opt_cancel_event")
        if _ev:
            _ev.set()

        opt_results.empty()
        for _key in _OPT_STATE_KEYS:
            st.session_state.pop(_key, None)
        _cleanup_generated_pdfs()

        st.session_state["_opt_start"] = True
        st.session_state["_opt_resume_path"] = str(resume_path)
        st.session_state["_opt_api_key"] = key_to_use
        st.session_state["_opt_strict_mode"] = strict_mode
        st.rerun()

    # ── Phase 1: launch optimization thread ──────────────────────────────

    if _opt_running:
        st.session_state.pop("_opt_start", None)
        _base_path = Path(st.session_state.pop("_opt_resume_path"))
        _api = st.session_state.pop("_opt_api_key", "")
        _strict_mode_t = st.session_state.pop("_opt_strict_mode", True)

        for _key in _OPT_STATE_KEYS:
            st.session_state.pop(_key, None)
        opt_results.empty()
        st.session_state["_opt_status_log"] = []

        _cancel_ev = threading.Event()
        st.session_state["_opt_cancel_event"] = _cancel_ev
        _thread_state = {
            "status_log": [],
            "done": False,
            "result": None,
            "error": None,
        }
        st.session_state["_opt_thread_state"] = _thread_state

        # Capture widget values now — thread closure stays stable across reruns
        _jd_text_t = jd_text.strip() or None
        _jd_url_t = jd_url.strip() or None
        _primary_color_t = primary_color

        def _log_t(msg: str) -> None:
            _thread_state["status_log"].append(("status", msg))

        def _on_iter_t(data: dict) -> None:
            if _cancel_ev.is_set():
                raise RuntimeError("Optimization cancelled by user.")
            i = data["iteration"]
            score = data["ats_score"]
            vscore = data.get("verified_score")
            improvements = data["improvements"]
            strategies = data.get("strategies", [])
            verification = data.get("verification")
            changes = data.get("changes_summary", "")

            resolved = [x["keyword"] for x in improvements if x["resolved"]]
            pending = [x["keyword"] for x in improvements if not x["resolved"]]

            if vscore is not None and verification:
                effective = vscore
                parts = [
                    f"**Iteration {i}** — Keyword Match: **{vscore}%** "
                    f"({verification['found_keywords']}/{verification['total_keywords']})"
                ]
                if verification.get("must_have_total", 0) > 0:
                    parts.append(
                        f"Must-haves: **{verification['must_have_score']}%** "
                        f"({verification['must_have_found']}/{verification['must_have_total']})"
                    )
            else:
                effective = score
                parts = [f"**Iteration {i}** — ATS Score: **{score}**/100"]

            hdr = " &nbsp;|&nbsp; ".join(parts)

            if strategies:
                applied = [s["strategy"] for s in strategies if s.get("applied")]
                if applied:
                    hdr += "\n\n📋 **Strategies:** " + " &nbsp; ".join(
                        f"✅ {s}" for s in applied
                    )

            if resolved or pending:
                hdr += "\n\n🔑 **Keywords:**"
                if resolved:
                    hdr += "\n" + " &nbsp; ".join(f"✅ {k}" for k in resolved)
                if pending and verification:
                    mh = verification.get("missing_must_have", [])
                    pr = verification.get("missing_preferred", [])
                    if mh:
                        hdr += f"\n⬜ **Must-have:** {', '.join(mh)}"
                    if pr:
                        hdr += f"\n⬜ **Preferred:** {', '.join(pr)}"
                    other = [k for k in pending if k not in mh and k not in pr]
                    if other:
                        hdr += f"\n⬜ **Other:** {', '.join(other)}"
                elif pending:
                    hdr += f"\n⬜ Missing: {', '.join(pending)}"

            if effective >= 95:
                hdr += "\n\n🎯 **Target reached!**"
            if changes:
                hdr += f"\n\n> 📝 {changes}"

            _thread_state["status_log"].append(("iteration", hdr))

        def _run_opt_thread() -> None:
            try:
                result = optimize_resume(
                    base_resume_pdf=_base_path,
                    jd_text=_jd_text_t,
                    jd_url=_jd_url_t,
                    primary_color=_primary_color_t,
                    api_key=_api or None,
                    on_iteration=_on_iter_t,
                    on_status=_log_t,
                    strict_mode=_strict_mode_t,
                )
                _thread_state["result"] = result
            except Exception as e:
                _msg = str(e)
                _thread_state["error"] = (
                    "cancelled" if "cancelled" in _msg.lower() else _msg
                )
            finally:
                _thread_state["done"] = True

        _thr = threading.Thread(target=_run_opt_thread, daemon=True)
        st.session_state["_opt_thread_active"] = True
        _thr.start()
        st.session_state["_opt_thread"] = _thr
        st.rerun()

    # ── Phase 2: poll thread / process results ────────────────────────────

    elif _opt_thread_active:
        if _opt_thread_done:
            # Thread finished — clear thread state and act on result
            _thread_state = st.session_state.get("_opt_thread_state", {})
            _status_log = list(_thread_state.get("status_log", []))
            st.session_state["_opt_status_log"] = _status_log
            st.session_state.pop("_opt_thread_active", None)
            st.session_state.pop("_opt_thread_done", None)
            st.session_state.pop("_opt_thread", None)
            st.session_state.pop("_opt_thread_state", None)
            st.session_state.pop("_opt_cancel_event", None)
            _thread_error = (
                st.session_state.pop("_opt_error", None)
                or _thread_state.get("error")
            )
            _thread_result = (
                st.session_state.pop("_opt_thread_result", None)
                or _thread_state.get("result")
            )

            if _thread_error == "cancelled":
                with opt_results.container():
                    with st.status(
                        "⏹️ Optimization cancelled",
                        state="error", expanded=False,
                    ):
                        for _etype, _content in _status_log:
                            if _etype == "status":
                                st.write(_content)
                            else:
                                st.markdown(_content)
                                st.divider()
                    st.info(
                        "Optimization was cancelled. Your uploaded resume is still "
                        "available — click **Optimize Resume** to try again."
                    )

            elif _thread_error:
                with opt_results.container():
                    with st.status(
                        "❌ Optimization failed",
                        state="error", expanded=True,
                    ):
                        for _etype, _content in _status_log:
                            if _etype == "status":
                                st.write(_content)
                            else:
                                st.markdown(_content)
                                st.divider()
                    st.error(f"Error: {_thread_error}")
                    st.info(
                        "Your uploaded resume is still available — "
                        "click **Optimize Resume** to retry."
                    )
                # Clear partial log so it doesn't show as "complete" on next run
                st.session_state["_opt_status_log"] = []

            else:
                # Success — build PDF in main thread (can use Streamlit globals)
                with opt_results.container():
                    with st.status("Generating PDF…", expanded=True) as _status:
                        try:
                            pdf_bytes, pdf_name = _rebuild_pdf(
                                _thread_result["content_html"],
                                company=_thread_result.get("company"),
                            )
                        except Exception as e:
                            _status.update(label="PDF export failed", state="error")
                            st.error(f"PDF export failed: {e}")
                            st.stop()
                        _status.update(
                            label="✅ Optimization complete!", state="complete"
                        )

                    st.session_state["_opt_content_html"] = _thread_result["content_html"]
                    st.session_state["_opt_job_title"] = _thread_result["job_title"]
                    st.session_state["_opt_company"] = _thread_result["company"]
                    st.session_state["_opt_fingerprint"] = _opt_fp
                    st.session_state["_opt_pdf_bytes"] = pdf_bytes
                    st.session_state["_opt_pdf_name"] = pdf_name
                    st.session_state["_opt_success_msg"] = (
                        "✅ Resume optimized! Your tailored PDF is ready to download."
                    )

                    st.success(st.session_state["_opt_success_msg"])
                    _dl_c, _pv_c = st.columns([5, 1])
                    with _dl_c:
                        st.download_button(
                            label=_DL_LABEL_OPT,
                            data=pdf_bytes,
                            file_name=pdf_name,
                            mime="application/pdf",
                            type="primary",
                            key="opt_dl_fresh",
                            use_container_width=True,
                        )
                    with _pv_c:
                        if st.button(
                            "👁️",
                            key="opt_preview_fresh",
                            use_container_width=True,
                            help="Preview current resume",
                        ):
                            _show_resume_preview(
                                _thread_result["content_html"],
                                selected_template_id,
                                primary_color,
                            )

        else:
            # Thread still running — render live log and poll every 0.5 s
            with opt_results.container():
                _thread_state = st.session_state.get("_opt_thread_state", {})
                _current_log = list(_thread_state.get("status_log", []))
                _status = st.status(
                    "Optimizing resume…",
                    state="running",
                    expanded=True,
                )
                for _etype, _content in _current_log:
                    if _etype == "status":
                        _status.write(_content)
                    else:
                        _status.markdown(_content)
                        _status.divider()
            time.sleep(0.5)
            st.rerun()

    # ── Re-export with new style ─────────────────────────────────────────

    elif opt_export and _opt_has_cached:
        content_html = st.session_state["_opt_content_html"]
        with opt_results.container():
            with st.spinner("Generating PDF with new style…"):
                try:
                    pdf_bytes, pdf_name = _rebuild_pdf(
                        content_html,
                        company=st.session_state.get("_opt_company"),
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.stop()
            st.session_state["_opt_pdf_bytes"] = pdf_bytes
            st.session_state["_opt_pdf_name"] = pdf_name
            st.session_state["_opt_success_msg"] = (
                "✅ PDF re-exported with the new style. Ready to download."
            )
            st.success(st.session_state["_opt_success_msg"])
            _dl_c, _pv_c = st.columns([5, 1])
            with _dl_c:
                st.download_button(
                    label=_DL_LABEL_OPT,
                    data=pdf_bytes,
                    file_name=pdf_name,
                    mime="application/pdf",
                    type="primary",
                    key="opt_dl_reexport",
                    use_container_width=True,
                )
            with _pv_c:
                if st.button(
                    "👁️",
                    key="opt_preview_reexport",
                    use_container_width=True,
                    help="Preview current resume",
                ):
                    _show_resume_preview(
                        content_html,
                        selected_template_id,
                        primary_color,
                    )

    # ── Persist cached results ───────────────────────────────────────────

    else:
        with opt_results.container():
            cached_log = st.session_state.get("_opt_status_log")
            if cached_log:
                with st.status(
                    "✅ Optimization complete!",
                    state="complete", expanded=False,
                ):
                    for etype, content in cached_log:
                        if etype == "status":
                            st.write(content)
                        else:
                            st.markdown(content)
                            st.divider()
            if "_opt_success_msg" in st.session_state:
                st.success(st.session_state["_opt_success_msg"])
            if "_opt_pdf_bytes" in st.session_state:
                _dl_c, _pv_c = st.columns([5, 1])
                with _dl_c:
                    st.download_button(
                        label=_DL_LABEL_OPT,
                        data=st.session_state["_opt_pdf_bytes"],
                        file_name=st.session_state["_opt_pdf_name"],
                        mime="application/pdf",
                        type="primary",
                        key="opt_dl_cached",
                        use_container_width=True,
                    )
                with _pv_c:
                    if st.button(
                        "👁️",
                        key="opt_preview_cached",
                        use_container_width=True,
                        help="Preview current resume",
                    ):
                        _show_resume_preview(
                            st.session_state["_opt_content_html"],
                            selected_template_id,
                            primary_color,
                        )

    # ── Edit section (Tab 1) ─────────────────────────────────────────────

    if "_opt_content_html" in st.session_state:
        _render_edit_section(
            content_key="_opt_content_html",
            history_key="_opt_edit_history",
            undo_key="_opt_edit_undo_html",
            pdf_bytes_key="_opt_pdf_bytes",
            pdf_name_key="_opt_pdf_name",
            success_msg_key="_opt_success_msg",
            company=st.session_state.get("_opt_company"),
            form_id="edit_form_opt",
            applying_flag="_opt_edit_apply",
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: EDIT RESUME
# ══════════════════════════════════════════════════════════════════════════════

_QE_STATE_KEYS = (
    "_qe_content_html", "_qe_pdf_bytes", "_qe_pdf_name",
    "_qe_success_msg", "_qe_edit_history", "_qe_edit_undo_html",
)

with tab_edit:
    st.caption(
        "Load your uploaded resume, then edit it with AI — no job description needed."
    )

    # ── Fingerprint for the quick-edit tab (resume only) ─────────────────

    def _qe_fingerprint() -> str:
        uploaded_id = ""
        if uploaded_resume is not None:
            uploaded_id = f"{uploaded_resume.name}:{uploaded_resume.size}"
        return hashlib.sha256(uploaded_id.encode()).hexdigest()

    _qe_fp = _qe_fingerprint()

    if st.session_state.get("_qe_fingerprint") != _qe_fp:
        for _key in _QE_STATE_KEYS:
            st.session_state.pop(_key, None)
        st.session_state["_qe_fingerprint"] = _qe_fp

    _qe_has_content = "_qe_content_html" in st.session_state
    _qe_loading = st.session_state.get("_qe_start", False)

    # ── Action buttons ───────────────────────────────────────────────────

    if _qe_has_content:
        col_load, col_exp = st.columns(2)
        with col_load:
            _qe_load_area = st.empty()
            if _qe_loading:
                qe_load = False
                _qe_load_area.button(
                    "⏳ Loading…", disabled=True, type="primary",
                    use_container_width=True, key="qe_busy",
                )
            else:
                qe_load = _qe_load_area.button(
                    "🔄 Reload Resume", type="primary",
                    use_container_width=True, key="qe_reload",
                )
        with col_exp:
            _qe_exp_area = st.empty()
            if qe_load or _qe_loading:
                qe_export = False
            else:
                qe_export = _qe_exp_area.button(
                    "🎨 Re-export with Style",
                    use_container_width=True, key="qe_export",
                    help="Regenerate PDF with the current theme & accent color",
                )
    else:
        _qe_load_area = st.empty()
        _qe_exp_area = st.empty()
        qe_export = False
        if _qe_loading:
            qe_load = False
            _qe_load_area.button(
                "⏳ Loading…", disabled=True, type="primary",
                use_container_width=True, key="qe_busy2",
            )
        else:
            qe_load = _qe_load_area.button(
                "📄 Load Resume", type="primary",
                use_container_width=True, key="qe_go",
            )

    qe_results = st.empty()

    # ── Start loading → clear state and rerun ────────────────────────────

    if qe_load:
        key_to_use = _get_api_key()
        if key_to_use is None:
            st.stop()
        resume_path = _resolve_resume_path()
        if resume_path is None:
            st.stop()

        # Confirm before discarding existing edits
        _has_qe_edits = bool(st.session_state.get("_qe_edit_history"))
        if _has_qe_edits and not st.session_state.pop("_qe_confirm_yes", False):
            _confirm_reload_resume()
            st.stop()

        qe_results.empty()
        for _key in _QE_STATE_KEYS:
            st.session_state.pop(_key, None)
        _cleanup_generated_pdfs()

        st.session_state["_qe_start"] = True
        st.session_state["_qe_resume_path"] = str(resume_path)
        st.session_state["_qe_api_key"] = key_to_use
        st.rerun()

    # ── Conversion execution ─────────────────────────────────────────────

    if _qe_loading:
        st.session_state.pop("_qe_start", None)
        _base_path = Path(st.session_state.pop("_qe_resume_path"))
        _api = st.session_state.pop("_qe_api_key", "")

        for _key in _QE_STATE_KEYS:
            st.session_state.pop(_key, None)
        qe_results.empty()

        with qe_results.container():
            _qe_status = st.empty()
            _qe_status.info("⏳ Step 1/3 — Extracting resume text…")

            def _qe_on_status(msg: str) -> None:
                _qe_status.info(f"⏳ {msg}")

            with st.spinner("Loading resume faithfully…"):
                try:
                    result = convert_resume(
                        base_resume_pdf=_base_path,
                        primary_color=primary_color,
                        api_key=_api or None,
                        on_status=_qe_on_status,
                    )
                except Exception as e:
                    st.error(f"Conversion failed: {e}")
                    st.stop()

            _qe_status.empty()

            with st.spinner("Generating PDF…"):
                try:
                    pdf_bytes, pdf_name = _rebuild_pdf(result["content_html"])
                except Exception as e:
                    st.error(f"PDF export failed: {e}")
                    st.stop()

            st.session_state["_qe_content_html"] = result["content_html"]
            st.session_state["_qe_fingerprint"] = _qe_fp
            st.session_state["_qe_pdf_bytes"] = pdf_bytes
            st.session_state["_qe_pdf_name"] = pdf_name
            st.session_state["_qe_success_msg"] = (
                "✅ Resume loaded and converted! Ready to download."
            )

            st.success(st.session_state["_qe_success_msg"])
            _dl_c, _pv_c = st.columns([5, 1])
            with _dl_c:
                st.download_button(
                    label=_DL_LABEL_RESUME,
                    data=pdf_bytes,
                    file_name=pdf_name,
                    mime="application/pdf",
                    type="primary",
                    key="qe_dl_fresh",
                    use_container_width=True,
                )
            with _pv_c:
                if st.button(
                    "👁️",
                    key="qe_preview_fresh",
                    use_container_width=True,
                    help="Preview current resume",
                ):
                    _show_resume_preview(
                        result["content_html"],
                        selected_template_id,
                        primary_color,
                    )

    # ── Re-export with new style ─────────────────────────────────────────

    elif qe_export and _qe_has_content:
        content_html = st.session_state["_qe_content_html"]
        with qe_results.container():
            with st.spinner("Generating PDF with new style…"):
                try:
                    pdf_bytes, pdf_name = _rebuild_pdf(content_html)
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.stop()
            st.session_state["_qe_pdf_bytes"] = pdf_bytes
            st.session_state["_qe_pdf_name"] = pdf_name
            st.session_state["_qe_success_msg"] = (
                "✅ PDF re-exported with the new style. Ready to download."
            )
            st.success(st.session_state["_qe_success_msg"])
            _dl_c, _pv_c = st.columns([5, 1])
            with _dl_c:
                st.download_button(
                    label=_DL_LABEL_RESUME,
                    data=pdf_bytes,
                    file_name=pdf_name,
                    mime="application/pdf",
                    type="primary",
                    key="qe_dl_reexport",
                    use_container_width=True,
                )
            with _pv_c:
                if st.button(
                    "👁️",
                    key="qe_preview_reexport",
                    use_container_width=True,
                    help="Preview current resume",
                ):
                    _show_resume_preview(
                        content_html,
                        selected_template_id,
                        primary_color,
                    )

    # ── Persist cached results ───────────────────────────────────────────

    else:
        with qe_results.container():
            if "_qe_success_msg" in st.session_state:
                st.success(st.session_state["_qe_success_msg"])
            if "_qe_pdf_bytes" in st.session_state:
                _dl_c, _pv_c = st.columns([5, 1])
                with _dl_c:
                    st.download_button(
                        label=_DL_LABEL_RESUME,
                        data=st.session_state["_qe_pdf_bytes"],
                        file_name=st.session_state["_qe_pdf_name"],
                        mime="application/pdf",
                        type="primary",
                        key="qe_dl_cached",
                        use_container_width=True,
                    )
                with _pv_c:
                    if st.button(
                        "👁️",
                        key="qe_preview_cached",
                        use_container_width=True,
                        help="Preview current resume",
                    ):
                        _show_resume_preview(
                            st.session_state["_qe_content_html"],
                            selected_template_id,
                            primary_color,
                        )

    # ── Edit section (Tab 2) ─────────────────────────────────────────────

    if "_qe_content_html" in st.session_state:
        _render_edit_section(
            content_key="_qe_content_html",
            history_key="_qe_edit_history",
            undo_key="_qe_edit_undo_html",
            pdf_bytes_key="_qe_pdf_bytes",
            pdf_name_key="_qe_pdf_name",
            success_msg_key="_qe_success_msg",
            company=None,
            form_id="edit_form_qe",
            applying_flag="_qe_edit_apply",
        )
