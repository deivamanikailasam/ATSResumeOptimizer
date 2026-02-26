"""Main agent: orchestrate resume extraction, JD loading, optimization, and PDF export."""

from pathlib import Path
from typing import Callable

from ats_resume_optimizer.job_description import get_job_description
from ats_resume_optimizer.llm import extract_title_and_company, optimize_until_target
from ats_resume_optimizer.pdf_export import html_to_pdf
from ats_resume_optimizer.resume import extract_resume_text
from ats_resume_optimizer.templates import render_resume
from ats_resume_optimizer.utils import build_output_path


def optimize_resume(
    base_resume_pdf: Path,
    jd_text: str | None = None,
    jd_url: str | None = None,
    target_score: int = 95,
    max_iterations: int = 5,
    primary_color: str = "#2563eb",
    api_key: str | None = None,
    on_iteration: Callable[[dict], None] | None = None,
) -> dict:
    """Run the full optimization pipeline and return cached-friendly results.

    Returns a dict with keys: content_html, job_title, company.
    """
    resume_text = extract_resume_text(base_resume_pdf)
    job_description = get_job_description(jd_text=jd_text, jd_url=jd_url)

    job_title, company = extract_title_and_company(
        job_description, api_key=api_key
    )

    best_result = optimize_until_target(
        resume_text=resume_text,
        jd_text=job_description,
        target_score=target_score,
        max_iterations=max_iterations,
        primary_color=primary_color,
        api_key=api_key,
        on_iteration=on_iteration,
    )

    return {
        "content_html": best_result["tailored_resume_html"],
        "job_title": job_title,
        "company": company,
    }


def export_resume_pdf(
    content_html: str,
    template_id: str,
    primary_color: str,
    job_title: str,
    company: str,
) -> Path:
    """Render cached content HTML with a template and export to PDF."""
    full_html = render_resume(template_id, content_html, primary_color)
    output_path = build_output_path(job_title, company)
    html_to_pdf(full_html, output_path)
    return output_path


def run_resume_agent(
    base_resume_pdf: Path,
    jd_text: str | None = None,
    jd_url: str | None = None,
    target_score: int = 95,
    max_iterations: int = 5,
    template_id: str = "modern_minimal",
    primary_color: str = "#2563eb",
    api_key: str | None = None,
    on_iteration: Callable[[dict], None] | None = None,
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
    )

    return export_resume_pdf(
        content_html=result["content_html"],
        template_id=template_id,
        primary_color=primary_color,
        job_title=result["job_title"],
        company=result["company"],
    )
