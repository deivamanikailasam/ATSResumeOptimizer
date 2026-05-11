"""Main agent: orchestrate resume extraction, JD loading, optimization, and PDF export."""

from pathlib import Path
from typing import Callable

from ats_resume_optimizer.job_description import get_job_description
from ats_resume_optimizer.llm import (
    clean_resume_html,
    convert_resume_to_html,
    edit_resume_html,
    extract_jd_keywords,
    extract_title_and_company,
    optimize_until_target,
)
from ats_resume_optimizer.pdf_export import html_to_pdf
from ats_resume_optimizer.resume import analyze_resume_structure, extract_resume_text
from ats_resume_optimizer.templates import render_resume
from ats_resume_optimizer.utils import build_output_path, extract_name_from_html


def optimize_resume(
    base_resume_pdf: Path,
    jd_text: str | None = None,
    jd_url: str | None = None,
    target_score: int = 95,
    max_iterations: int = 15,
    primary_color: str = "#2563eb",
    api_key: str | None = None,
    on_iteration: Callable[[dict], None] | None = None,
    on_status: Callable[[str], None] | None = None,
    strict_mode: bool = True,
) -> dict:
    """Run the full optimization pipeline and return cached-friendly results.

    Returns a dict with keys: content_html, job_title, company, jd_keywords.
    """
    if on_status:
        on_status("Extracting resume text...")
    resume_text = extract_resume_text(base_resume_pdf)

    if on_status:
        on_status("Analyzing resume structure...")
    resume_analysis = analyze_resume_structure(resume_text)

    if on_status:
        on_status("Loading job description...")
    job_description = get_job_description(jd_text=jd_text, jd_url=jd_url)

    if on_status:
        on_status("Analyzing job description and extracting keywords...")
    jd_keywords = extract_jd_keywords(job_description, api_key=api_key)

    job_title = jd_keywords.get("job_title") or "UnknownRole"
    company = jd_keywords.get("company") or "UnknownCompany"
    if company == "UnknownCompany":
        if on_status:
            on_status("Extracting job title and company...")
        job_title, company = extract_title_and_company(
            job_description, api_key=api_key
        )

    if on_status:
        mode_label = "strict" if strict_mode else "standard"
        on_status(f"Starting ATS optimization loop ({mode_label} mode)...")
    if strict_mode:
        # Strict mode has a real honesty ceiling: unsupported JD keywords
        # must remain missing, so repeated refinement often just burns tokens.
        max_iterations = min(max_iterations, 3)
    best_result = optimize_until_target(
        resume_text=resume_text,
        jd_text=job_description,
        jd_keywords=jd_keywords,
        target_score=target_score,
        max_iterations=max_iterations,
        primary_color=primary_color,
        api_key=api_key,
        on_iteration=on_iteration,
        on_status=on_status,
        resume_analysis=resume_analysis,
        strict_mode=strict_mode,
    )

    return {
        "content_html": best_result["tailored_resume_html"],
        "job_title": job_title,
        "company": company,
        "jd_keywords": jd_keywords,
    }


def convert_resume(
    base_resume_pdf: Path,
    primary_color: str = "#2563eb",
    api_key: str | None = None,
    on_status: Callable[[str], None] | None = None,
) -> dict:
    """Convert a resume PDF to structured HTML without ATS optimization.

    Returns a dict with key: content_html.
    """
    if on_status:
        on_status("Extracting resume text...")
    resume_text = extract_resume_text(base_resume_pdf)

    if on_status:
        on_status("Analyzing resume structure...")
    resume_analysis = analyze_resume_structure(resume_text)

    content_html = convert_resume_to_html(
        resume_text,
        primary_color=primary_color,
        api_key=api_key,
        resume_analysis=resume_analysis,
        on_status=on_status,
    )

    return {"content_html": content_html}


def apply_resume_edit(
    content_html: str,
    instruction: str,
    edit_history: list[dict] | None = None,
    api_key: str | None = None,
) -> dict:
    """Apply a natural-language edit to the optimized resume content.

    Returns a dict with keys: updated_html, changes_summary.
    """
    return edit_resume_html(
        current_html=content_html,
        instruction=instruction,
        edit_history=edit_history,
        api_key=api_key,
    )


def export_resume_pdf(
    content_html: str,
    template_id: str,
    primary_color: str,
    company: str | None = None,
) -> Path:
    """Render cached content HTML with a template and export to PDF.

    Applies clean_resume_html() before rendering so that artefacts from
    any source (initial load, AI edits, ATS optimiser) are removed from
    every PDF that is downloaded — not just those from the load path.
    """
    content_html = clean_resume_html(content_html)
    full_html = render_resume(template_id, content_html, primary_color)
    candidate_name = extract_name_from_html(content_html)
    output_path = build_output_path(candidate_name, company=company)
    html_to_pdf(full_html, output_path)
    return output_path


def run_resume_agent(
    base_resume_pdf: Path,
    jd_text: str | None = None,
    jd_url: str | None = None,
    target_score: int = 95,
    max_iterations: int = 15,
    template_id: str = "modern_minimal",
    primary_color: str = "#2563eb",
    api_key: str | None = None,
    on_iteration: Callable[[dict], None] | None = None,
    on_status: Callable[[str], None] | None = None,
    strict_mode: bool = True,
) -> Path:
    """Load resume, get JD, optimize for ATS, render with template, and save PDF.

    Returns the path to the generated PDF.
    """
    result = optimize_resume(
        base_resume_pdf=base_resume_pdf,
        jd_text=jd_text,
        jd_url=jd_url,
        target_score=target_score,
        max_iterations=max_iterations,
        primary_color=primary_color,
        api_key=api_key,
        on_iteration=on_iteration,
        on_status=on_status,
        strict_mode=strict_mode,
    )

    return export_resume_pdf(
        content_html=result["content_html"],
        template_id=template_id,
        primary_color=primary_color,
        company=result.get("company"),
    )
