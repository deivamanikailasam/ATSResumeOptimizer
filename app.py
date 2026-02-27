# app.py
import hashlib
import os
from pathlib import Path

import streamlit as st

from ats_resume_optimizer.agent import optimize_resume, export_resume_pdf
from ats_resume_optimizer.config import RESUME_DIR, OUTPUT_DIR
from ats_resume_optimizer.templates import TEMPLATES, get_template_choices, render_resume

st.set_page_config(
    page_title="ATS Resume Optimizer", page_icon="📄", layout="centered"
)


# ── Disk cleanup helpers ─────────────────────────────────────────────────────

def _cleanup_generated_pdfs():
    """Remove all files from the generated-PDF output directory."""
    if OUTPUT_DIR.exists():
        for f in OUTPUT_DIR.iterdir():
            if f.is_file():
                f.unlink(missing_ok=True)


def _cleanup_uploaded_resume():
    """Remove the uploaded resume file from disk."""
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
    help="Required for resume optimization. Can also be set via OPENAI_API_KEY in a .env file.",
)

target_score = st.sidebar.slider(
    "Target ATS score", min_value=70, max_value=100, value=95, step=1
)

max_iterations = st.sidebar.number_input(
    "Max optimization iterations", min_value=1, max_value=10, value=5, step=1
)

st.sidebar.divider()

uploaded_resume = st.sidebar.file_uploader("Upload base resume PDF", type=["pdf"])

# ── Main area ────────────────────────────────────────────────────────────────

@st.dialog("How to Use This App", width="large")
def _show_help():
    st.markdown(
        """
#### 1. Add Your OpenAI API Key
- In the **sidebar** on the left, find the **OpenAI API key** field.
- Paste your API key (starts with `sk-…`).
- Alternatively, create a `.env` file in the project root with:
  ```
  OPENAI_API_KEY=sk-your-key-here
  ```
- The key is required to power the AI optimization (uses GPT-4o-mini).

---

#### 2. Upload Your Base Resume
- In the sidebar, click **Upload base resume PDF** and select your current resume.
- This is the starting point the AI will optimize from.

---

#### 3. Set Optimization Parameters
- **Target ATS score** (slider, 70–100): the minimum ATS score the optimizer
  will try to reach. Higher values mean more keyword optimization.
- **Max optimization iterations** (1–10): how many refinement rounds the AI
  can perform. More iterations give better results but take longer.

---

#### 4. Enter the Job Description
- **Job URL**: paste the link to the job posting — the app will scrape the
  description automatically (supports LinkedIn, Indeed, Greenhouse, Lever,
  Workday, and more).
- **Job description text**: paste the full job description directly.
- You can provide either or both (pasted text takes precedence).

---

#### 5. Choose a Resume Theme & Accent Color
- Pick from **40 premium templates** in the **Theme** dropdown.
- Use the **Accent color** picker to customize the highlight color.
- Click the **👁️ preview** button to see a live preview with sample data
  before running the optimization.

---

#### 6. Optimize Your Resume
- Click **🚀 Optimize Resume** to start the AI pipeline.
- The app will:
  1. Extract keywords from the job description.
  2. Iteratively rewrite your resume to maximize ATS keyword coverage.
  3. Show real-time progress — ATS score, verified keyword match, and
     applied strategies per iteration.
  4. Generate a polished PDF with your chosen theme.

---

#### 7. Download Your Optimized Resume
- Once complete, click **⬇️ Download Optimized Resume (PDF)** to save
  the file.
- The filename is automatically derived from the job title and company.

---

#### 8. Re-export with a Different Style
- After optimization, you can change the **Theme** or **Accent color** and
  click **🎨 Re-export with Style** to generate a new PDF instantly —
  without re-running the AI.

---

> **Tip:** Results persist across page refreshes during your session, so you
> won't lose your optimized resume if you accidentally reload the page.
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


# ── Input fingerprinting for cache invalidation ─────────────────────────────

def _compute_input_fingerprint() -> str:
    """Hash all non-style inputs so we can detect when cache must be cleared."""
    uploaded_id = ""
    if uploaded_resume is not None:
        uploaded_id = f"{uploaded_resume.name}:{uploaded_resume.size}"
    parts = [
        uploaded_id,
        jd_text.strip(),
        jd_url.strip(),
        str(target_score),
        str(max_iterations),
    ]
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


current_fingerprint = _compute_input_fingerprint()

if st.session_state.get("_opt_fingerprint") != current_fingerprint:
    for _key in (
        "_opt_content_html", "_opt_job_title", "_opt_company",
        "_opt_status_log", "_opt_pdf_bytes", "_opt_pdf_name",
        "_opt_success_msg",
    ):
        st.session_state.pop(_key, None)
    st.session_state["_opt_fingerprint"] = current_fingerprint

has_cached = "_opt_content_html" in st.session_state


# ── Run ──────────────────────────────────────────────────────────────────────

st.divider()

_optimizing = st.session_state.get("_start_optimization", False)

col_opt, col_export = st.columns(2)

with col_opt:
    opt_area = st.empty()
    if _optimizing:
        run_button = False
        opt_area.button(
            "⏳ Optimizing…", disabled=True, type="primary",
            use_container_width=True,
        )
    else:
        run_button = opt_area.button(
            "🔄 Regenerate" if has_cached else "🚀 Optimize Resume",
            type="primary",
            use_container_width=True,
        )

with col_export:
    export_area = st.empty()
    if run_button or _optimizing:
        export_button = False
    else:
        export_button = export_area.button(
            "🎨 Re-export with Style",
            use_container_width=True,
            disabled=not has_cached,
            help="Use cached optimized content with the current theme & color"
            if has_cached
            else "Optimize a resume first",
        )


def _resolve_resume_path() -> Path | None:
    """Validate and return the resume path, or show errors and return None."""
    if not uploaded_resume:
        st.error("Please upload a base resume PDF.")
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


results_area = st.empty()

# ── Handle optimize / regenerate click → clear cache and rerun clean ─────────

if run_button:
    api_key_to_use = _validate_common_inputs()
    if api_key_to_use is None:
        st.stop()

    base_resume_path = _resolve_resume_path()
    if base_resume_path is None:
        st.stop()

    for _key in (
        "_opt_content_html", "_opt_job_title", "_opt_company",
        "_opt_status_log", "_opt_pdf_bytes", "_opt_pdf_name",
        "_opt_success_msg",
    ):
        st.session_state.pop(_key, None)

    _cleanup_generated_pdfs()

    st.session_state["_start_optimization"] = True
    st.session_state["_opt_resume_path"] = str(base_resume_path)
    st.session_state["_opt_api_key"] = api_key_to_use
    st.rerun()

# ── Full optimization (runs on the clean rerun) ──────────────────────────────

if _optimizing:
    st.session_state.pop("_start_optimization", None)
    base_resume_path = Path(st.session_state.pop("_opt_resume_path"))
    api_key_to_use = st.session_state.pop("_opt_api_key", "")

    st.session_state["_opt_status_log"] = []

    def _log_status(msg: str) -> None:
        st.session_state["_opt_status_log"].append(("status", msg))
        st.write(msg)

    def on_iteration(data: dict) -> None:
        i = data["iteration"]
        score = data["ats_score"]
        verified_score = data.get("verified_score")
        improvements = data["improvements"]
        strategies = data.get("strategies", [])
        verification = data.get("verification")
        changes_summary = data.get("changes_summary", "")

        resolved = [imp["keyword"] for imp in improvements if imp["resolved"]]
        pending = [imp["keyword"] for imp in improvements if not imp["resolved"]]

        score_parts = [f"**Iteration {i}** — ATS Score: **{score}**/100"]
        if verified_score is not None and verification:
            score_parts.append(
                f"Verified: **{verified_score}%** "
                f"({verification['found_keywords']}/{verification['total_keywords']})"
            )
            if verification.get("must_have_total", 0) > 0:
                score_parts.append(
                    f"Must-haves: **{verification['must_have_score']}%** "
                    f"({verification['must_have_found']}/{verification['must_have_total']})"
                )

        header = " &nbsp;|&nbsp; ".join(score_parts)

        if strategies:
            applied = [s["strategy"] for s in strategies if s.get("applied")]
            if applied:
                strat_str = " &nbsp; ".join(f"✅ {s}" for s in applied)
                header += f"\n\n📋 **Strategies:** {strat_str}"

        if resolved or pending:
            header += "\n\n🔑 **Keywords:**"
            if resolved:
                resolved_str = " &nbsp; ".join(f"✅ {kw}" for kw in resolved)
                header += f"\n{resolved_str}"
            if pending and verification:
                must_have_missing = verification.get("missing_must_have", [])
                preferred_missing = verification.get("missing_preferred", [])
                if must_have_missing:
                    header += f"\n⬜ **Must-have:** {', '.join(must_have_missing)}"
                if preferred_missing:
                    header += f"\n⬜ **Preferred:** {', '.join(preferred_missing)}"
                other_missing = [
                    kw for kw in pending
                    if kw not in must_have_missing
                    and kw not in preferred_missing
                ]
                if other_missing:
                    header += f"\n⬜ **Other:** {', '.join(other_missing)}"
            elif pending:
                header += f"\n⬜ Missing: {', '.join(pending)}"

        if score >= target_score:
            header += "\n\n🎯 **Target reached!**"

        if changes_summary:
            header += f"\n\n> 📝 {changes_summary}"

        st.session_state["_opt_status_log"].append(("iteration", header))
        st.markdown(header)
        st.divider()

    with results_area.container():
        with st.status("Optimizing resume…", expanded=True) as status:
            _log_status("Starting optimization pipeline…")
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
                    on_status=_log_status,
                )
            except Exception as e:
                status.update(label="Optimization failed", state="error")
                st.error(f"Error during optimization: {e}")
                st.stop()

            _log_status("Generating PDF…")
            try:
                output_pdf_path = export_resume_pdf(
                    content_html=result["content_html"],
                    template_id=selected_template_id,
                    primary_color=primary_color,
                    job_title=result["job_title"],
                    company=result["company"],
                )
            except Exception as e:
                status.update(label="PDF export failed", state="error")
                st.error(f"Error generating PDF: {e}")
                st.stop()

            status.update(label="✅ Optimization complete!", state="complete")

        st.session_state["_opt_content_html"] = result["content_html"]
        st.session_state["_opt_job_title"] = result["job_title"]
        st.session_state["_opt_company"] = result["company"]
        st.session_state["_opt_fingerprint"] = current_fingerprint

        with open(output_pdf_path, "rb") as f:
            pdf_bytes = f.read()
        st.session_state["_opt_pdf_bytes"] = pdf_bytes
        st.session_state["_opt_pdf_name"] = output_pdf_path.name
        st.session_state["_opt_success_msg"] = (
            f"Resume optimized! Saved to: **{output_pdf_path.name}**"
        )

        st.success(st.session_state["_opt_success_msg"])
        st.download_button(
            label="⬇️ Download Optimized Resume (PDF)",
            data=pdf_bytes,
            file_name=output_pdf_path.name,
            mime="application/pdf",
            type="primary",
        )

# ── Re-export with new style (cached) ────────────────────────────────────────

elif export_button and has_cached:
    export_area.button(
        "⏳ Exporting…", disabled=True, use_container_width=True,
    )

    content_html = st.session_state["_opt_content_html"]
    job_title = st.session_state["_opt_job_title"]
    company = st.session_state["_opt_company"]

    with results_area.container():
        with st.spinner("Generating PDF with new style…"):
            try:
                output_pdf_path = export_resume_pdf(
                    content_html=content_html,
                    template_id=selected_template_id,
                    primary_color=primary_color,
                    job_title=job_title,
                    company=company,
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
                st.stop()

        with open(output_pdf_path, "rb") as f:
            pdf_bytes = f.read()
        st.session_state["_opt_pdf_bytes"] = pdf_bytes
        st.session_state["_opt_pdf_name"] = output_pdf_path.name
        st.session_state["_opt_success_msg"] = (
            f"PDF re-exported with new style! Saved to: **{output_pdf_path.name}**"
        )

        st.success(st.session_state["_opt_success_msg"])
        st.download_button(
            label="⬇️ Download Optimized Resume (PDF)",
            data=pdf_bytes,
            file_name=output_pdf_path.name,
            mime="application/pdf",
            type="primary",
        )

# ── Persist results across reruns (e.g. after download click) ────────────────

else:
    with results_area.container():
        cached_log = st.session_state.get("_opt_status_log")
        if cached_log:
            with st.status(
                "✅ Optimization complete!", state="complete", expanded=False
            ):
                for entry_type, content in cached_log:
                    if entry_type == "status":
                        st.write(content)
                    else:
                        st.markdown(content)
                        st.divider()
        if "_opt_success_msg" in st.session_state:
            st.success(st.session_state["_opt_success_msg"])
        if "_opt_pdf_bytes" in st.session_state:
            st.download_button(
                label="⬇️ Download Optimized Resume (PDF)",
                data=st.session_state["_opt_pdf_bytes"],
                file_name=st.session_state["_opt_pdf_name"],
                mime="application/pdf",
                type="primary",
            )
