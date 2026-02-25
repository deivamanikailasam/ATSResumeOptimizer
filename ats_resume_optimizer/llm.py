"""OpenAI client and resume optimization prompts / API calls."""

import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def _parse_json_from_content(content: str | None) -> dict:
    """Parse JSON from LLM response, handling None, empty, or markdown-wrapped JSON."""
    if content is None or not content.strip():
        raise RuntimeError(
            "Model returned no content. Check your API key, model, and rate limits."
        )
    text = content.strip()
    # Strip optional markdown code block (```json ... ``` or ``` ... ```)
    code_block = re.search(r"^```(?:json)?\s*\n?(.*?)\n?```\s*$", text, re.DOTALL)
    if code_block:
        text = code_block.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        preview = (text[:200] + "…") if len(text) > 200 else text
        raise RuntimeError(
            f"Model did not return valid JSON. Parse error: {e}. "
            f"Content preview: {preview!r}"
        ) from e


def get_client(api_key: str | None = None) -> OpenAI:
    """Return OpenAI client using api_key if provided, else OPENAI_API_KEY env."""
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key or not key.strip():
        raise ValueError(
            "OpenAI API key is required. Set OPENAI_API_KEY in .env or enter it in the app."
        )
    return OpenAI(api_key=key.strip())

SYSTEM_PROMPT = """
You are a senior technical recruiter and expert resume writer.
You deeply understand Applicant Tracking Systems (ATS), keyword matching,
and how large companies screen resumes.

Rules:
- Always tell the truth about the candidate's experience.
- Optimize for ATS without keyword stuffing.
- Use a clean, ATS-friendly layout with standard section headings
  (Summary, Skills, Experience, Education, Projects, Certifications as relevant).
- Use bullet points with quantifiable achievements where possible.
"""


def build_user_prompt(resume_text: str, jd_text: str) -> str:
    """Build the user prompt for resume tailoring."""
    return f"""
I will give you my current resume and a target job description.

1. Analyze the job description and extract the most important required skills,
   technologies, and responsibilities.
2. Rewrite my resume so it is tailored specifically to this job.
3. Maximize ATS match by naturally incorporating all critical keywords,
   especially in the title, skills, and experience bullet points.
4. Keep the resume to at most two pages of concise bullets.
5. Maintain only realistic, honest claims based on my original resume.

Return a single JSON object with:
- "tailored_resume_md": the full resume in Markdown format.
- "ats_score": an integer from 0 to 100 estimating the match to the job.
- "missing_keywords": an array of important keywords from the JD that are not
  yet represented or are weakly represented.

JOB DESCRIPTION:
\"\"\"{jd_text}\"\"\"

CURRENT RESUME:
\"\"\"{resume_text}\"\"\"
"""


def optimize_resume_once(
    resume_text: str,
    jd_text: str,
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
) -> dict:
    """Run one iteration of resume optimization. Returns dict with tailored_resume_md, ats_score, missing_keywords."""
    client = get_client(api_key)
    prompt = build_user_prompt(resume_text, jd_text)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    content = resp.choices[0].message.content
    data = _parse_json_from_content(content)
    if not isinstance(data, dict):
        raise RuntimeError("Model did not return a JSON object.")
    return data


def optimize_until_target(
    resume_text: str,
    jd_text: str,
    target_score: int = 95,
    max_iterations: int = 4,
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
) -> dict:
    """Iteratively optimize resume until target ATS score or max iterations."""
    current_resume_text = resume_text
    best_result = None

    for i in range(max_iterations):
        result = optimize_resume_once(
            current_resume_text, jd_text, model=model, api_key=api_key
        )
        ats_score = int(result.get("ats_score", 0))
        missing = result.get("missing_keywords", [])
        print(
            f"Iteration {i+1}: ATS score = {ats_score}, missing keywords = {missing}"
        )

        if best_result is None or ats_score > int(
            best_result.get("ats_score", 0)
        ):
            best_result = result

        if ats_score >= target_score:
            break

        refinement_instructions = f"""
The following important keywords are still weak or missing: {missing}.
Revise the resume to incorporate these keywords naturally without exaggeration or keyword stuffing.
Return the updated JSON object in the same format as before.
"""
        current_resume_text = (
            best_result["tailored_resume_md"] + "\n\n" + refinement_instructions
        )

    return best_result


def extract_title_and_company(
    jd_text: str,
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
) -> tuple[str, str]:
    """Extract job title and company name from job description using LLM."""
    client = get_client(api_key)
    prompt = f"""
From the following job description, extract:
1. The job title.
2. The company name.

Return a JSON object: {{"job_title": "...", "company": "..."}}.

JOB DESCRIPTION:
\"\"\"{jd_text}\"\"\"
"""
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You extract structured fields from job descriptions.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    data = _parse_json_from_content(resp.choices[0].message.content)
    if not isinstance(data, dict):
        data = {}
    job_title = data.get("job_title", "UnknownRole")
    company = data.get("company", "UnknownCompany")
    return job_title, company
