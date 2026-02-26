"""OpenAI client and resume optimization prompts / API calls."""

import json
import os
import re
from typing import Callable

from dotenv import load_dotenv
from openai import OpenAI

from ats_resume_optimizer.templates import CONTENT_STRUCTURE

load_dotenv()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_json_from_content(content: str | None) -> dict:
    """Parse JSON from LLM response, handling None, empty, or markdown-wrapped JSON."""
    if content is None or not content.strip():
        raise RuntimeError(
            "Model returned no content. Check your API key, model, and rate limits."
        )
    text = content.strip()
    code_block = re.search(r"^```(?:json)?\s*\n?(.*?)\n?```\s*$", text, re.DOTALL)
    if code_block:
        text = code_block.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        preview = (text[:300] + "…") if len(text) > 300 else text
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


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a senior technical recruiter, expert resume writer, and HTML specialist.
You deeply understand Applicant Tracking Systems (ATS), keyword matching,
and how large companies screen resumes.

Rules:
- Always tell the truth about the candidate's experience.
- Optimize for ATS without keyword stuffing.
- Use standard ATS-friendly section headings (Summary, Skills, Experience,
  Education, Projects, Certifications as relevant).
- Every role under Experience MUST have at least 5 bullet points.
  Each bullet should start with a strong action verb and include
  quantifiable achievements or measurable impact wherever possible.
- Use the proven STAR method (Situation, Task, Action, Result) to frame
  bullet points that demonstrate impact clearly.
- Mirror exact keywords, phrases, and job-specific terminology from the
  job description throughout the resume — especially in the Summary,
  Skills section, and Experience bullets — to maximize ATS keyword match
  rate.
- Front-load the most important and relevant keywords in the Summary and
  the first two bullets of each role for maximum ATS weight.
- Incorporate both spelled-out terms and their acronyms where applicable
  (e.g., "Continuous Integration / Continuous Deployment (CI/CD)") to
  catch all ATS keyword variations.
- Group technical skills into clear, relevant categories that align with
  the job description's requirements.
- Output resume content as semantic HTML using the exact CSS class names
  provided in the template structure — no <html>, <head>, <body>, or <style> tags.
- Keep the resume concise (aim for content that fits 1-2 printed pages).
"""


def build_user_prompt(
    resume_text: str,
    jd_text: str,
    primary_color: str = "#2563eb",
) -> str:
    return f"""\
I will give you my current resume and a target job description.

**Your task:**
1. Analyze the job description and extract the most important required skills,
   technologies, and responsibilities.
2. Rewrite my resume so it is tailored specifically to this job.
3. Maximize ATS match by naturally incorporating all critical keywords,
   especially in the summary, skills, and experience bullet points.
4. Keep the resume to at most two pages of concise bullets.
5. Maintain only realistic, honest claims based on my original resume.
6. Ensure every role in the Experience section has at least 5 strong bullet
   points with quantifiable impact — expand existing bullets or derive new
   ones from the original resume context if needed.

**HTML output format:**
{CONTENT_STRUCTURE}

The selected accent color is {primary_color} — you do NOT need to add any
inline color styles; the template CSS handles colors automatically.

**Return a single JSON object with exactly these keys:**
- "tailored_resume_html": the full resume body as HTML following the structure above.
- "ats_score": an integer 0–100 estimating the ATS match to the job description.
- "missing_keywords": an array of important JD keywords that are not yet
  represented or are weakly represented in the resume.
- "changes_summary": a brief 2-3 sentence summary of the key changes and
  optimizations you made compared to the original resume (e.g., keywords
  added, sections restructured, bullets expanded).

JOB DESCRIPTION:
\"\"\"{jd_text}\"\"\"

CURRENT RESUME:
\"\"\"{resume_text}\"\"\"
"""


def _build_refinement_prompt(missing_keywords: list[str]) -> str:
    return f"""\
The following important keywords are still weak or missing in the resume:
{json.dumps(missing_keywords)}

Revise the resume HTML to incorporate these keywords naturally — without
exaggeration or keyword stuffing. Keep the same HTML structure and class names.

Return the updated JSON object in the same format:
- "tailored_resume_html"
- "ats_score"
- "missing_keywords"
- "changes_summary": a brief 2-3 sentence summary of what you changed in
  this revision to incorporate the missing keywords and improve the score.
"""


# ---------------------------------------------------------------------------
# Single optimization call
# ---------------------------------------------------------------------------

def optimize_resume_once(
    client: OpenAI,
    messages: list[dict],
    model: str = "gpt-4o-mini",
) -> dict:
    """Run one LLM call with the given message history. Returns parsed JSON."""
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
    )
    content = resp.choices[0].message.content
    data = _parse_json_from_content(content)
    if not isinstance(data, dict):
        raise RuntimeError("Model did not return a JSON object.")
    return data


# ---------------------------------------------------------------------------
# Iterative optimization loop
# ---------------------------------------------------------------------------

def optimize_until_target(
    resume_text: str,
    jd_text: str,
    target_score: int = 95,
    max_iterations: int = 5,
    primary_color: str = "#2563eb",
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
    on_iteration: Callable[[dict], None] | None = None,
) -> dict:
    """Iteratively optimize resume until target ATS score or max iterations.

    Parameters
    ----------
    on_iteration : callable, optional
        Called after each iteration with a dict containing:
        ``iteration``, ``ats_score``, ``missing_keywords``,
        ``improvements`` (list of {keyword, resolved} dicts).
    """
    client = get_client(api_key)

    messages: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": build_user_prompt(resume_text, jd_text, primary_color),
        },
    ]

    best_result: dict | None = None
    all_seen_keywords: dict[str, bool] = {}

    for i in range(max_iterations):
        result = optimize_resume_once(client, messages, model=model)
        ats_score = int(result.get("ats_score", 0))
        missing = result.get("missing_keywords", [])

        for kw in missing:
            if kw not in all_seen_keywords:
                all_seen_keywords[kw] = False

        resolved_this_round = [
            kw for kw, resolved in all_seen_keywords.items()
            if not resolved and kw not in missing
        ]
        for kw in resolved_this_round:
            all_seen_keywords[kw] = True

        improvements = [
            {"keyword": kw, "resolved": resolved}
            for kw, resolved in all_seen_keywords.items()
        ]

        changes_summary = result.get("changes_summary", "")

        if on_iteration:
            on_iteration({
                "iteration": i + 1,
                "ats_score": ats_score,
                "missing_keywords": missing,
                "improvements": improvements,
                "changes_summary": changes_summary,
            })

        if best_result is None or ats_score > int(best_result.get("ats_score", 0)):
            best_result = result

        if ats_score >= target_score:
            break

        assistant_content = json.dumps(result, ensure_ascii=False)
        messages.append({"role": "assistant", "content": assistant_content})
        messages.append({
            "role": "user",
            "content": _build_refinement_prompt(missing),
        })

    return best_result


# ---------------------------------------------------------------------------
# Title / company extraction (unchanged)
# ---------------------------------------------------------------------------

def extract_title_and_company(
    jd_text: str,
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
) -> tuple[str, str]:
    """Extract job title and company name from job description using LLM."""
    client = get_client(api_key)
    prompt = f"""\
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
