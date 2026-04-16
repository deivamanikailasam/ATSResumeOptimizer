"""OpenAI client and resume optimization prompts / API calls."""

import json
import os
import re
from html.parser import HTMLParser
from typing import Callable

from dotenv import load_dotenv
from openai import OpenAI

from ats_resume_optimizer.templates import CONTENT_STRUCTURE, build_content_structure

load_dotenv()


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ATS_STRATEGIES = [
    "Job Title Mirroring",
    "Keyword Frequency Optimization",
    "Semantic Skill Clustering",
    "Action Verb Matching",
    "Experience Alignment",
    "Soft Skills Integration",
    "Acronym Expansion",
    "STAR Method Bullets",
    "Must-Have Prioritization",
    "Contextual Keyword Embedding",
    "Skills Ordering by Relevance",
    "Exact Phrase Matching",
    "Quantified Achievements",
    "Date Format Consistency",
]


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


def _extract_text_from_html(html: str) -> str:
    """Extract plain text from HTML content."""

    class _TextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.parts: list[str] = []

        def handle_data(self, data):
            self.parts.append(data)

    extractor = _TextExtractor()
    extractor.feed(html)
    return " ".join(extractor.parts)


# ---------------------------------------------------------------------------
# Programmatic keyword verification
# ---------------------------------------------------------------------------

def _keyword_present(keyword: str, text: str) -> bool:
    """Check if keyword appears in text using word-boundary matching.

    Prevents false positives like 'Java' matching 'JavaScript' or 'ML'
    matching 'HTML'. For short keywords (<=3 chars), requires exact word
    boundaries on both sides. For longer keywords, uses regex word boundaries.
    """
    kw_lower = keyword.lower()
    text_lower = text.lower()
    if len(kw_lower) <= 3:
        pattern = r"(?<![a-zA-Z])" + re.escape(kw_lower) + r"(?![a-zA-Z])"
    else:
        pattern = r"\b" + re.escape(kw_lower) + r"\b"
    return bool(re.search(pattern, text_lower))


def verify_keyword_coverage(html_content: str, jd_keywords: dict) -> dict:
    """Check which JD keywords actually appear in the generated resume HTML."""
    resume_text = _extract_text_from_html(html_content).lower()

    categories = [
        ("required_hard_skills", "must_have"),
        ("required_soft_skills", "must_have"),
        ("preferred_skills", "preferred"),
        ("industry_terms", "preferred"),
        ("certifications", "preferred"),
    ]

    all_results: dict[str, list[dict]] = {}
    total = 0
    found = 0
    must_have_total = 0
    must_have_found = 0

    for jd_key, priority in categories:
        keywords = jd_keywords.get(jd_key, [])
        cat_results = []
        for kw in keywords:
            present = _keyword_present(kw, resume_text)
            cat_results.append(
                {"keyword": kw, "found": present, "priority": priority}
            )
            total += 1
            if present:
                found += 1
            if priority == "must_have":
                must_have_total += 1
                if present:
                    must_have_found += 1
        all_results[jd_key] = cat_results

    jd_title = jd_keywords.get("job_title", "")
    title_match = _keyword_present(jd_title, resume_text) if jd_title else True

    req_exp = jd_keywords.get("required_experience", "")
    exp_match = True
    if req_exp:
        exp_numbers = re.findall(r"\d+", req_exp)
        exp_match = any(
            re.search(r"\b" + re.escape(n) + r"\b", resume_text)
            for n in exp_numbers
        )

    return {
        "by_category": all_results,
        "title_match": title_match,
        "experience_match": exp_match,
        "programmatic_score": round(
            (found / total * 100) if total > 0 else 0
        ),
        "must_have_score": round(
            (must_have_found / must_have_total * 100)
            if must_have_total > 0
            else 0
        ),
        "total_keywords": total,
        "found_keywords": found,
        "must_have_total": must_have_total,
        "must_have_found": must_have_found,
        "missing_must_have": [
            item["keyword"]
            for cat in all_results.values()
            for item in cat
            if item["priority"] == "must_have" and not item["found"]
        ],
        "missing_preferred": [
            item["keyword"]
            for cat in all_results.values()
            for item in cat
            if item["priority"] == "preferred" and not item["found"]
        ],
    }


# ---------------------------------------------------------------------------
# JD keyword extraction
# ---------------------------------------------------------------------------

def extract_jd_keywords(
    jd_text: str,
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
) -> dict:
    """Extract structured, prioritized keywords from a job description."""
    client = get_client(api_key)
    prompt = f"""\
Analyze the following job description and extract structured keyword data.
Be thorough — capture every skill, technology, tool, methodology, and
qualification mentioned.

Return a JSON object with exactly these keys:
- "job_title": the exact job title from the posting
- "required_hard_skills": array of mandatory technical skills, tools,
  technologies, programming languages, and frameworks explicitly required
- "required_soft_skills": array of soft skills mentioned as required
  (e.g., leadership, communication, collaboration, problem-solving)
- "preferred_skills": array of nice-to-have/preferred/bonus skills
- "required_experience": string describing required years of experience
  (e.g., "5+ years") or empty string if not specified
- "required_education": string describing required education level
  or empty string if not specified
- "key_responsibilities": array of 5-10 core responsibility phrases
  verbatim from the JD
- "industry_terms": array of industry-specific jargon, methodologies,
  or domain terms mentioned
- "action_verbs": array of specific action verbs used in the JD
  (e.g., "design", "develop", "deploy", "manage", "optimize")
- "certifications": array of any mentioned certifications or licenses

JOB DESCRIPTION:
\"\"\"{jd_text}\"\"\"
"""
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract structured data from job descriptions "
                    "with high precision. Include every relevant keyword."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    data = _parse_json_from_content(resp.choices[0].message.content)
    return data if isinstance(data, dict) else {}


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a senior technical recruiter, expert resume writer, and HTML specialist.
You deeply understand Applicant Tracking Systems (ATS), keyword matching,
and how large companies screen resumes.

Rules:

**CRITICAL — Preserve the Original Resume:**
- The candidate's original resume is the FOUNDATION. You must NOT rewrite
  it from scratch or completely change its content.
- Keep the original sentences, bullet points, and descriptions as much as
  possible. Only make TARGETED modifications:
  (a) Update wording and phrasing to better align with JD terminology.
  (b) Add new keywords, skills, or short phrases where they fit naturally.
  (c) Remove content that is clearly irrelevant to the target role.
  (d) Strengthen weak bullets by incorporating JD-relevant action verbs
      or metrics — but keep the original meaning and context intact.
- Do NOT replace the candidate's actual achievements, project descriptions,
  or role narratives with generic or fabricated content.
- The optimized resume should read like a refined version of the original,
  NOT like a completely different resume.

**Truthfulness & Integrity:**
- Always tell the truth about the candidate's experience.
- Optimize for ATS without keyword stuffing.
- Maintain only realistic, honest claims based on the original resume.
- NEVER invent experience, roles, companies, degrees, or certifications
  that are not present in the original resume.

**ATS Keyword Strategy:**
- Mirror exact keywords, phrases, and job-specific terminology from the
  job description — especially in the Summary, Skills section, and
  Experience bullets — to maximize ATS keyword match rate.
- Integrate keywords by weaving them INTO existing sentences and bullets
  rather than replacing original content wholesale.
- Prioritize REQUIRED/MUST-HAVE skills over preferred/nice-to-have ones.
  Required skills must appear prominently; preferred skills should be
  included only where the candidate has genuine experience.
- Each primary keyword should appear in at least 2-3 different sections
  (e.g., Summary + Skills + Experience) to register across ATS scanning
  passes.
- Front-load the most important and relevant keywords in the Summary and
  the first two bullets of each role for maximum ATS weight.
- Incorporate both spelled-out terms and their acronyms where applicable
  (e.g., "Continuous Integration / Continuous Deployment (CI/CD)") to
  catch all ATS keyword variations.
- Use the exact multi-word phrases from the JD (e.g., "stakeholder
  management" not "client relations") — ATS systems match exact phrases.
- Use the exact action verbs from the JD in experience bullets where
  possible (e.g., if JD says "design, develop, and deploy", use those
  exact verbs).
- Include both hard skills AND soft skills mentioned in the JD
  (e.g., leadership, collaboration, communication, problem-solving).

**Job Title & Experience Alignment:**
- The Professional Summary MUST open with or contain the exact job title
  from the JD (e.g., "Senior Data Engineer with 8+ years...").
- Use industry-standard job titles that ATS taxonomies recognize
  (e.g., "Software Engineer" not "Code Ninja").
- If the JD specifies years of experience (e.g., "5+ years"), explicitly
  state matching experience duration in the Summary and relevant bullets.

**Skills Section Optimization:**
- Keep all skills from the original resume. Add new JD-relevant skills
  that the candidate genuinely has, but do NOT remove original skills
  unless they are completely irrelevant.
- Group technical skills into clear, relevant categories that align with
  the job description's requirements.
- Order skills within each category by relevance to the JD — most
  relevant first.
- Create semantic skill clusters (group related technologies together,
  e.g., "Python, Django, Flask, FastAPI" as a backend cluster).

**Experience Bullets — Targeted Enhancement:**
- Keep the original bullets largely intact. Enhance them by:
  (a) Swapping generic verbs with JD-specific action verbs.
  (b) Adding quantifiable metrics where the original lacked them.
  (c) Weaving in 1-2 JD keywords per bullet naturally.
- Match the bullet count to the depth of each role in the original resume.
  A role with 3 original bullets should get 3-5 optimized bullets; a role
  with 8 original bullets can have up to 8-10. Do NOT pad short roles
  with filler or truncate rich roles arbitrarily.
- Each bullet should start with a strong action verb and include
  quantifiable achievements or measurable impact wherever possible.
- Use digits for all numbers and metrics (e.g., "5 years", "40%",
  "2M users") rather than spelling out numbers — ATS systems parse
  digits more reliably.

**Preserve All Original Sections:**
- The original resume may contain sections beyond the standard six
  (Summary, Skills, Experience, Education, Projects, Certifications).
  You MUST preserve every section present in the original resume,
  including but not limited to: Publications, Awards, Volunteer
  Experience, Languages, Affiliations, Patents, Research, Teaching,
  Leadership, Training, Interests, etc.
- Use the section's original heading (or a close ATS-friendly variant).
- For extra sections, use the HTML pattern:
  <div class="resume-section {section-id}">
    <h2>Section Heading</h2>
    ...content...
  </div>
- You may reorder sections for maximum ATS impact (most relevant first),
  but never drop them entirely.

**Section Headings & Formatting:**
- Use standard ATS-friendly section headings for the core sections:
  Summary, Skills, Experience, Education, Projects, Certifications.
- Use consistent date formatting across all entries: "Mon YYYY - Mon YYYY"
  (e.g., "Jan 2023 - Mar 2026").
- Avoid special characters that may confuse ATS parsers — use standard
  hyphens (-), not em-dashes, and avoid decorative symbols.

**HTML Output:**
- Output resume content as semantic HTML using the exact CSS class names
  provided in the template structure — no <html>, <head>, <body>, or
  <style> tags.
- Keep the resume concise (aim for content that fits 1-2 printed pages,
  but up to 3 pages is acceptable for senior candidates with extensive
  experience).
"""


def _format_keyword_checklist(jd_keywords: dict) -> str:
    """Build a keyword checklist section for the user prompt."""
    if not jd_keywords:
        return ""

    lines = [
        "\n**Pre-extracted JD Keyword Checklist — ensure ALL are addressed:**"
    ]

    if jd_keywords.get("job_title"):
        lines.append(f"- Target Job Title: {jd_keywords['job_title']}")
    if jd_keywords.get("required_experience"):
        lines.append(
            f"- Required Experience: {jd_keywords['required_experience']}"
        )
    if jd_keywords.get("required_education"):
        lines.append(
            f"- Required Education: {jd_keywords['required_education']}"
        )
    if jd_keywords.get("required_hard_skills"):
        lines.append(
            "- MUST-HAVE Hard Skills (highest priority — each must appear "
            "in 2-3 sections): "
            + ", ".join(jd_keywords["required_hard_skills"])
        )
    if jd_keywords.get("required_soft_skills"):
        lines.append(
            "- MUST-HAVE Soft Skills (weave into Summary and bullets): "
            + ", ".join(jd_keywords["required_soft_skills"])
        )
    if jd_keywords.get("preferred_skills"):
        lines.append(
            "- PREFERRED Skills (include where candidate has real "
            "experience): "
            + ", ".join(jd_keywords["preferred_skills"])
        )
    if jd_keywords.get("industry_terms"):
        lines.append(
            "- Industry Terms & Methodologies: "
            + ", ".join(jd_keywords["industry_terms"])
        )
    if jd_keywords.get("certifications"):
        lines.append(
            "- Certifications to highlight: "
            + ", ".join(jd_keywords["certifications"])
        )
    if jd_keywords.get("action_verbs"):
        lines.append(
            "- JD Action Verbs (use these exact verbs in experience "
            "bullets): "
            + ", ".join(jd_keywords["action_verbs"])
        )
    if jd_keywords.get("key_responsibilities"):
        lines.append(
            "- Key Responsibilities to address in bullets: "
            + ", ".join(jd_keywords["key_responsibilities"])
        )

    return "\n".join(lines)


_ATS_SCORING_RUBRIC = """\
**ATS Scoring Rubric** (use this to calculate ats_score accurately):
- Keyword Match (40%): What % of must-have JD keywords appear in the resume?
- Contextual Relevance (25%): Are keywords in achievement-based contexts, \
not just listed?
- Section Completeness (15%): All standard ATS sections present and properly \
structured?
- Job Title Alignment (10%): Does the summary/header match the JD's target \
title?
- Experience Alignment (10%): Does the resume reflect required years and \
experience level?"""


_STRATEGIES_LIST = """\
Choose from: "Job Title Mirroring", "Keyword Frequency Optimization", \
"Semantic Skill Clustering", "Action Verb Matching", "Experience Alignment", \
"Soft Skills Integration", "Acronym Expansion", "STAR Method Bullets", \
"Must-Have Prioritization", "Contextual Keyword Embedding", \
"Skills Ordering by Relevance", "Exact Phrase Matching", \
"Quantified Achievements", "Date Format Consistency"."""


def _format_resume_analysis(resume_analysis: dict | None) -> str:
    """Build an analysis summary to inform the LLM about the original structure."""
    if not resume_analysis:
        return ""

    lines = ["\n**Original Resume Structure Analysis:**"]

    section_ids = resume_analysis.get("section_ids", [])
    if section_ids:
        lines.append(f"- Sections found: {', '.join(section_ids)}")

    extra = resume_analysis.get("extra_sections", [])
    if extra:
        extra_names = [s["heading"] for s in extra]
        lines.append(
            f"- Non-standard sections to PRESERVE: {', '.join(extra_names)}"
        )

    avg = resume_analysis.get("avg_bullets_per_role", 0)
    if avg:
        lines.append(f"- Average bullets per role in original: {avg}")

    roles = resume_analysis.get("experience_roles", [])
    if roles:
        counts = [str(r["bullet_count"]) for r in roles]
        lines.append(
            f"- Bullets per role (newest to oldest): {', '.join(counts)}"
        )
        lines.append(
            "  Use these as your baseline — you may add 1-2 extra bullets "
            "per role to weave in JD keywords, but do not inflate thin roles "
            "or truncate rich ones."
        )

    return "\n".join(lines)


def build_user_prompt(
    resume_text: str,
    jd_text: str,
    jd_keywords: dict | None = None,
    primary_color: str = "#2563eb",
    resume_analysis: dict | None = None,
) -> str:
    keyword_checklist = _format_keyword_checklist(jd_keywords or {})
    analysis_section = _format_resume_analysis(resume_analysis)
    content_structure = build_content_structure(resume_analysis)

    return f"""\
I will give you my current resume and a target job description.
{keyword_checklist}
{analysis_section}

**Your task:**
1. Analyze the job description and categorize requirements into:
   (a) Required/must-have hard skills and technologies
   (b) Required soft skills
   (c) Preferred/nice-to-have skills
   (d) Required experience level and years
   (e) Required education and certifications
2. REFINE my resume with TARGETED changes to align it with this job.
   Do NOT rewrite it from scratch. Keep my original content, sentences,
   and bullet points as the foundation. Only:
   - Update wording and phrasing to use JD-specific terminology.
   - Add new JD-relevant keywords or skills where they fit naturally.
   - Remove content that is clearly irrelevant to the target role.
   - Strengthen existing bullets with better action verbs or metrics.
3. Open the Professional Summary with the exact target job title from the JD,
   followed by matching years of experience. Refine the rest of the summary
   to incorporate JD keywords while keeping the original narrative.
4. Maximize ATS match by naturally incorporating critical keywords INTO
   existing content:
   - Each must-have keyword MUST appear in at least 2-3 sections
   - Weave exact phrases and terminology from the JD into existing bullets
   - Replace generic verbs with the JD's own action verbs
   - Include both hard skills and soft skills from the JD
5. Order skills by relevance to the JD (most relevant first in each category).
   Keep original skills; add new JD-relevant ones the candidate genuinely has.
6. Create semantic skill clusters — group related technologies together.
7. Keep the resume concise — 1-2 pages for mid-level, up to 3 for senior
   candidates with extensive relevant experience.
8. Maintain only realistic, honest claims based on my original resume.
9. Match bullet depth to the original resume — adapt bullet counts per role
   based on the original content depth. Add 1-2 extra bullets only when
   needed to incorporate critical JD keywords. Use digits for all numbers.
10. Use consistent date format: "Mon YYYY - Mon YYYY" across all entries.
11. Preserve ALL sections from my original resume. Do NOT drop sections
    like Publications, Awards, Volunteer, Languages, Affiliations, etc.
    Reorder sections for maximum ATS impact, but keep all content.

**HTML output format:**
{content_structure}

The selected accent color is {primary_color} — you do NOT need to add any
inline color styles; the template CSS handles colors automatically.

{_ATS_SCORING_RUBRIC}

**Return a single JSON object with exactly these keys:**
- "tailored_resume_html": the full resume body as HTML following the
  structure above.
- "ats_score": an integer 0-100 based on the scoring rubric above.
- "missing_keywords": a flat array of important JD keywords still missing
  or weakly represented in the resume.
- "strategies_applied": an array of optimization strategy names applied
  in this iteration.
  {_STRATEGIES_LIST}
- "changes_summary": a brief 2-3 sentence summary of the targeted changes
  and optimizations you made. Highlight what was added, updated, or removed
  — the original content should remain largely recognizable.

JOB DESCRIPTION:
\"\"\"{jd_text}\"\"\"

CURRENT RESUME:
\"\"\"{resume_text}\"\"\"
"""


def _build_refinement_prompt(
    missing_keywords: list[str],
    verification: dict | None = None,
    resolved_keywords: list[str] | None = None,
) -> str:
    priority_section = ""
    if verification:
        must_have_missing = verification.get("missing_must_have", [])
        preferred_missing = verification.get("missing_preferred", [])

        if must_have_missing:
            priority_section += (
                "\n**CRITICAL — Must-have keywords still missing "
                "(highest priority, add to Summary + Skills + Experience):**\n"
                f"{json.dumps(must_have_missing)}\n"
            )
        if preferred_missing:
            priority_section += (
                "\n**Preferred keywords still missing "
                "(add where candidate has real experience):**\n"
                f"{json.dumps(preferred_missing)}\n"
            )
        if not verification.get("title_match"):
            priority_section += (
                "\n**WARNING:** The JD's job title is NOT found in the "
                "resume. Add it to the Professional Summary opening.\n"
            )
        if not verification.get("experience_match"):
            priority_section += (
                "\n**WARNING:** The JD's required experience years are NOT "
                "reflected in the resume. Add explicit years of experience.\n"
            )

    preserve_section = ""
    if resolved_keywords:
        preserve_section = (
            "\n**IMPORTANT — preserve these already-resolved keywords "
            f"(do NOT remove them):**\n{json.dumps(resolved_keywords)}\n"
        )

    return f"""\
The following important keywords are still weak or missing in the resume:
{json.dumps(missing_keywords)}
{priority_section}{preserve_section}
Revise the resume HTML to incorporate the missing keywords naturally —
without exaggeration or keyword stuffing. Keep the same HTML structure
and class names. Weave keywords into EXISTING sentences and bullets
rather than replacing original content. The resume should still closely
resemble the candidate's original resume with targeted enhancements.

**Placement guidance:**
- Must-have keywords -> add to Professional Summary + Skills section + at
  least one Experience bullet each.
- Preferred keywords -> add to Skills section and/or relevant Experience
  bullets.
- Verify each primary keyword appears in at least 2-3 sections.
- Verify all keywords are in meaningful, achievement-based contexts.

{_ATS_SCORING_RUBRIC}

Return the updated JSON object in the same format:
- "tailored_resume_html"
- "ats_score" (based on rubric)
- "missing_keywords" (flat array of what's still missing after this revision)
- "strategies_applied" (array of strategy names applied in this revision)
  {_STRATEGIES_LIST}
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
        temperature=0.2,
    )
    content = resp.choices[0].message.content
    data = _parse_json_from_content(content)
    if not isinstance(data, dict):
        raise RuntimeError("Model did not return a JSON object.")
    return data


# ---------------------------------------------------------------------------
# Iterative optimization loop
# ---------------------------------------------------------------------------

_STALE_LIMIT = 2


def optimize_until_target(
    resume_text: str,
    jd_text: str,
    jd_keywords: dict | None = None,
    target_score: int = 95,
    max_iterations: int = 15,
    primary_color: str = "#2563eb",
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
    on_iteration: Callable[[dict], None] | None = None,
    resume_analysis: dict | None = None,
) -> dict:
    """Iteratively optimize resume until target ATS score or plateau.

    Stops when:
    - The target score is reached, OR
    - The score hasn't improved for ``_STALE_LIMIT`` consecutive iterations
      (plateau detection), OR
    - ``max_iterations`` is exhausted (safety limit).

    Always uses the **best** result so far as the baseline for the next
    refinement round, preventing score regressions from compounding.

    Parameters
    ----------
    jd_keywords : dict, optional
        Pre-extracted structured keywords from the JD (from
        ``extract_jd_keywords``).  Enables programmatic verification
        and priority-aware refinement.
    on_iteration : callable, optional
        Called after each iteration with a dict containing:
        ``iteration``, ``ats_score``, ``verified_score``,
        ``missing_keywords``, ``improvements``, ``strategies``,
        ``verification``, ``changes_summary``.
    resume_analysis : dict, optional
        Structural analysis of the original resume from
        ``analyze_resume_structure``.
    """
    client = get_client(api_key)

    messages: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": build_user_prompt(
                resume_text, jd_text, jd_keywords, primary_color,
                resume_analysis=resume_analysis,
            ),
        },
    ]

    best_result: dict | None = None
    best_verified_score: int = 0
    best_verification: dict | None = None
    stale_count: int = 0
    all_seen_keywords: dict[str, bool] = {}
    all_strategies: dict[str, bool] = {}

    for i in range(max_iterations):
        result = optimize_resume_once(client, messages, model=model)
        ats_score = int(result.get("ats_score", 0))

        # --- keyword tracking (flat list, backward-compatible) ---
        missing = result.get("missing_keywords", [])
        if isinstance(missing, dict):
            flat: list[str] = []
            for v in missing.values():
                if isinstance(v, list):
                    flat.extend(v)
            missing = flat

        for kw in missing:
            if kw not in all_seen_keywords:
                all_seen_keywords[kw] = False

        resolved_this_round = [
            kw
            for kw, resolved in all_seen_keywords.items()
            if not resolved and kw not in missing
        ]
        for kw in resolved_this_round:
            all_seen_keywords[kw] = True

        improvements = [
            {"keyword": kw, "resolved": resolved}
            for kw, resolved in all_seen_keywords.items()
        ]

        # --- strategy tracking ---
        strategies = result.get("strategies_applied", [])
        if isinstance(strategies, list):
            for s in strategies:
                if isinstance(s, str) and s not in all_strategies:
                    all_strategies[s] = True

        strategy_list = [
            {"strategy": s, "applied": applied}
            for s, applied in all_strategies.items()
        ]

        # --- programmatic verification ---
        verification = None
        verified_score = ats_score
        if jd_keywords and result.get("tailored_resume_html"):
            verification = verify_keyword_coverage(
                result["tailored_resume_html"], jd_keywords
            )
            verified_score = verification["programmatic_score"]

        effective_score = verified_score if verification else ats_score

        # --- best-result tracking with plateau detection ---
        improved = best_result is None or effective_score > best_verified_score
        if improved:
            best_result = result
            best_verified_score = effective_score
            best_verification = verification
            stale_count = 0
        else:
            stale_count += 1

        changes_summary = result.get("changes_summary", "")

        if on_iteration:
            on_iteration(
                {
                    "iteration": i + 1,
                    "ats_score": ats_score,
                    "verified_score": verified_score,
                    "missing_keywords": missing,
                    "improvements": improvements,
                    "strategies": strategy_list,
                    "verification": verification,
                    "changes_summary": changes_summary,
                }
            )

        if effective_score >= target_score:
            break

        if stale_count >= _STALE_LIMIT:
            break

        # --- build next refinement round ---
        # Always use the BEST result as baseline to prevent regressions
        # from compounding across iterations.
        baseline_result = best_result
        refinement_verification = best_verification
        refinement_missing = missing

        if not improved and jd_keywords and best_result.get("tailored_resume_html"):
            refinement_verification = verify_keyword_coverage(
                best_result["tailored_resume_html"], jd_keywords
            )
            refinement_missing = (
                refinement_verification.get("missing_must_have", [])
                + refinement_verification.get("missing_preferred", [])
            )

        resolved_kws = [kw for kw, r in all_seen_keywords.items() if r]

        # Context optimization: only keep the latest assistant response
        # in the message history to prevent token bloat. The system prompt
        # and original user prompt provide full context; refinement turns
        # only need the most recent HTML output as baseline.
        if len(messages) > 3:
            messages = messages[:2]

        assistant_content = json.dumps(baseline_result, ensure_ascii=False)
        messages.append({"role": "assistant", "content": assistant_content})
        messages.append(
            {
                "role": "user",
                "content": _build_refinement_prompt(
                    refinement_missing,
                    verification=refinement_verification,
                    resolved_keywords=resolved_kws,
                ),
            }
        )

    return best_result


# ---------------------------------------------------------------------------
# Title / company extraction
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


# ---------------------------------------------------------------------------
# Resume-to-HTML conversion (no optimization, faithful formatting)
# ---------------------------------------------------------------------------

_CONVERT_SYSTEM_PROMPT = """\
You are an expert resume formatter and HTML specialist.
You convert resume text into well-structured semantic HTML using the
exact CSS class names provided, preserving ALL original content faithfully.

Rules:
- Convert the resume text AS-IS into the HTML structure. Do NOT modify,
  add, remove, or rephrase any content.
- Preserve the original section order, bullet points, dates, company
  names, job titles, skills, and education exactly as they appear.
- Use the provided HTML structure and CSS class names precisely.
- Do NOT add <html>, <head>, <body>, or <style> tags.
- Identify and format sections correctly (Summary, Skills, Experience,
  Education, Projects, Certifications, and any others present).
- For skills, group them into logical categories based on how they
  appear in the original resume.
- Use consistent date formatting: "Mon YYYY - Mon YYYY".
"""


def convert_resume_to_html(
    resume_text: str,
    primary_color: str = "#2563eb",
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
    resume_analysis: dict | None = None,
) -> str:
    """Convert resume text to structured HTML without any ATS optimization."""
    client = get_client(api_key)
    content_structure = build_content_structure(resume_analysis)

    prompt = f"""\
Convert the following resume text into HTML using the exact structure below.
Preserve ALL content faithfully — do not add, remove, or modify anything.
Just format it into the proper HTML structure.

**HTML structure to use:**
{content_structure}

The accent color is {primary_color} — no inline styles needed; the
template CSS handles colors automatically.

**Return a single JSON object with exactly this key:**
- "resume_html": the full resume as HTML following the structure above.

RESUME TEXT:
\"\"\"{resume_text}\"\"\"
"""
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _CONVERT_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )
    data = _parse_json_from_content(resp.choices[0].message.content)
    if not isinstance(data, dict) or "resume_html" not in data:
        raise RuntimeError("Model did not return the expected JSON format.")
    return data["resume_html"]


# ---------------------------------------------------------------------------
# Manual resume editing via natural-language instructions
# ---------------------------------------------------------------------------

_EDIT_SYSTEM_PROMPT = """\
You are an expert resume editor and HTML specialist.
You receive an optimized resume as HTML and a user instruction describing
changes they want. Apply the requested changes precisely while:

- Preserving the existing HTML structure and CSS class names exactly.
- Keeping all content the user did NOT ask to change.
- Maintaining ATS-friendly formatting (action verbs, quantified achievements,
  consistent date format, keyword-rich bullets).
- NOT adding <html>, <head>, <body>, or <style> tags — only the inner content.
- NOT removing sections unless the user explicitly asks to remove them.
"""


def edit_resume_html(
    current_html: str,
    instruction: str,
    edit_history: list[dict] | None = None,
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
) -> dict:
    """Apply a natural-language edit instruction to the resume HTML.

    Parameters
    ----------
    current_html : str
        The current resume content HTML.
    instruction : str
        The user's edit instruction (e.g., "Add Docker to skills",
        "Remove the second job", "Change summary to emphasize leadership").
    edit_history : list[dict], optional
        Previous edit turns as [{"instruction": ..., "summary": ...}, ...].
        Provides context so the model understands cumulative edits.
    model : str
        OpenAI model to use.
    api_key : str, optional
        OpenAI API key.

    Returns
    -------
    dict with keys:
        - "updated_html": the modified resume HTML
        - "changes_summary": brief description of what was changed
    """
    client = get_client(api_key)

    messages: list[dict] = [
        {"role": "system", "content": _EDIT_SYSTEM_PROMPT},
    ]

    # Include edit history as conversation context so cumulative edits
    # are understood (e.g., "now undo that" or "also change...")
    if edit_history:
        for turn in edit_history[-5:]:
            messages.append({
                "role": "user",
                "content": f"Edit instruction: {turn['instruction']}",
            })
            messages.append({
                "role": "assistant",
                "content": json.dumps({
                    "changes_summary": turn.get("summary", "Changes applied."),
                }),
            })

    prompt = f"""\
Here is the current resume HTML:

```html
{current_html}
```

**Edit instruction:** {instruction}

Apply the requested changes and return a JSON object with exactly these keys:
- "updated_html": the full updated resume HTML (complete, not a diff).
- "changes_summary": a brief 1-2 sentence summary of what you changed.

Return ONLY the JSON object, no other text.
"""
    messages.append({"role": "user", "content": prompt})

    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.1,
    )

    data = _parse_json_from_content(resp.choices[0].message.content)
    if not isinstance(data, dict) or "updated_html" not in data:
        raise RuntimeError("Model did not return the expected JSON format.")

    return {
        "updated_html": data["updated_html"],
        "changes_summary": data.get("changes_summary", "Changes applied."),
    }
