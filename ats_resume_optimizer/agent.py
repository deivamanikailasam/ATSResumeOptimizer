"""Main agent: orchestrate resume extraction, JD loading, optimization, and PDF export."""

from pathlib import Path

from ats_resume_optimizer.job_description import get_job_description
from ats_resume_optimizer.llm import extract_title_and_company, optimize_until_target
from ats_resume_optimizer.pdf_export import markdown_to_pdf
from ats_resume_optimizer.resume import extract_resume_text
from ats_resume_optimizer.utils import build_output_path


def run_resume_agent(
    base_resume_pdf: Path,
    jd_text: str | None = None,
    jd_url: str | None = None,
    target_score: int = 95,
    api_key: str | None = None,
) -> Path:
    """
    Load resume, get job description, optimize for ATS, and save tailored PDF.
    Returns the path to the generated PDF.
    api_key: Optional OpenAI API key; if not set, OPENAI_API_KEY env is used.
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
        api_key=api_key,
    )
    tailored_md = best_result["tailored_resume_md"]
    final_score = best_result["ats_score"]
    print(f"Final ATS score (model-estimated): {final_score}")

    output_path = build_output_path(job_title, company)
    markdown_to_pdf(tailored_md, output_path)

    return output_path
