"""OpenAI client and resume optimization prompts / API calls."""

import json
import os
import re
from html.parser import HTMLParser
from typing import Callable

from bs4 import BeautifulSoup, NavigableString
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


def _create_chat_completion(
    client: OpenAI,
    model: str,
    messages: list[dict],
    temperature: float | None = None,
):
    """Create a chat completion, omitting unsupported params for GPT-5 models."""
    kwargs = {
        "model": model,
        "messages": messages,
    }
    if temperature is not None and not model.lower().startswith("gpt-5"):
        kwargs["temperature"] = temperature
    return client.chat.completions.create(**kwargs)


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
- "company": the company/employer name from the posting, or "UnknownCompany"
  if not clearly stated
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
    resp = _create_chat_completion(
        client,
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

STRICT_SYSTEM_PROMPT = """\
You are an ATS resume optimizer operating in STRICT truthfulness mode.

The base resume is ground truth. Improve ATS alignment only by:
- Rephrasing existing content with JD terminology without changing meaning.
- Moving, grouping, and ordering existing skills and experience.
- Surfacing skills that are clearly present in the resume body.
- Expanding acronyms already present in the resume.
- Improving formatting, headings, and concise summary wording.

Never add skills, tools, certifications, companies, projects, metrics,
responsibilities, or experience that are absent from the base resume.
If a JD keyword cannot be added honestly, leave it out and report it as
missing. Preserve every original section and keep the output as semantic
resume-body HTML only. Return valid JSON only.

Do not optimize by dumping JD keywords into the Skills section. ATS quality
comes from relevant, evidence-backed context. Keep the Skills section concise:
include original skills plus only the most relevant hard skills/tools that are
clearly supported by the resume. Put responsibilities, domains, and soft skills
in Summary or Experience only when the resume proves them.
"""

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


def _format_keyword_checklist(jd_keywords: dict, strict_mode: bool = False) -> str:
    """Build a keyword checklist section for the user prompt."""
    if not jd_keywords:
        return ""

    hard_skill_label = (
        "- MUST-HAVE Hard Skills (highest priority — each must appear "
        "in 2-3 sections): "
    )
    soft_skill_label = "- MUST-HAVE Soft Skills (weave into Summary and bullets): "
    preferred_skill_label = (
        "- PREFERRED Skills (include where candidate has real experience): "
    )
    if strict_mode:
        hard_skill_label = (
            "- MUST-HAVE Hard Skills (highest priority — include only where "
            "the resume provides evidence): "
        )
        soft_skill_label = (
            "- MUST-HAVE Soft Skills (use only in Summary/Experience when "
            "supported by evidence): "
        )
        preferred_skill_label = (
            "- PREFERRED Skills (skip unless clearly supported by the resume): "
        )

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
            hard_skill_label + ", ".join(jd_keywords["required_hard_skills"])
        )
    if jd_keywords.get("required_soft_skills"):
        lines.append(
            soft_skill_label + ", ".join(jd_keywords["required_soft_skills"])
        )
    if jd_keywords.get("preferred_skills"):
        lines.append(
            preferred_skill_label + ", ".join(jd_keywords["preferred_skills"])
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


_STRICT_ATS_SCORING_NOTE = """\
**Strict Mode Scoring Note:** Do NOT increase ats_score for keyword stuffing
or long skill lists. Penalize overloaded Skills sections. Reward only concise,
evidence-backed keyword placement in Summary/Experience and clearly proven
hard skills/tools in Skills.
"""


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


_STRICT_MODE_TASK_ADDENDUM = """\
**STRICT MODE:** Use only facts, skills, tools, metrics, and experience
already present in the original resume. Rephrase, reorder, surface latent
skills, and expand existing acronyms. Do not invent anything. Leave any
unverifiable JD keyword in "missing_keywords".

**Skills discipline:** Do not fill the Skills section with every JD keyword.
Add only high-signal hard skills/tools that are clearly supported by the
resume. Keep soft skills, responsibilities, domains, and generic phrases out
of Skills unless they were already listed there. Prefer weaving supported
keywords into existing experience bullets with evidence.

All skill subheadings/categories (Languages and Frameworks, Cloud, DevOps,
Databases, Tools, Methodologies, Libraries, etc.) MUST be nested inside the
single Skills section as `.skill-category` blocks. Never create standalone
resume sections for skill categories.

"""


def build_user_prompt(
    resume_text: str,
    jd_text: str,
    jd_keywords: dict | None = None,
    primary_color: str = "#2563eb",
    resume_analysis: dict | None = None,
    strict_mode: bool = True,
) -> str:
    keyword_checklist = _format_keyword_checklist(
        jd_keywords or {}, strict_mode=strict_mode
    )
    analysis_section = _format_resume_analysis(resume_analysis)
    content_structure = build_content_structure(resume_analysis)
    strict_section = _STRICT_MODE_TASK_ADDENDUM if strict_mode else ""
    keyword_frequency_guidance = (
        "- Prioritize contextual evidence over repeated keyword frequency.\n"
        "   - A supported keyword in a strong Experience bullet is better than\n"
        "     repeating it in Summary + Skills without proof.\n"
        "   - Do not force every keyword into multiple sections; leave weak or\n"
        "     unsupported keywords in missing_keywords."
        if strict_mode
        else "- Each must-have keyword MUST appear in at least 2-3 sections\n"
        "   - Weave exact phrases and terminology from the JD into existing bullets\n"
        "   - Replace generic verbs with the JD's own action verbs\n"
        "   - Include both hard skills and soft skills from the JD"
    )
    skills_guidance = (
        "Keep original skills; reorder by relevance. Add only a few high-signal "
        "hard skills/tools that are explicitly supported by the resume body. "
        "Do NOT add every JD keyword, soft skill, responsibility, domain, or "
        "generic phrase to Skills. Keep all skill categories inside the single "
        "Skills section as .skill-category blocks; never create separate "
        "resume sections for Languages and Frameworks, Cloud, DevOps, Tools, "
        "Databases, Methodologies, Libraries, or similar skill groupings."
        if strict_mode
        else "Keep original skills; add new JD-relevant ones the candidate "
        "genuinely has. Keep all skill categories inside the single Skills "
        "section as .skill-category blocks; never create separate resume "
        "sections for skill groupings."
    )

    return f"""\
I will give you my current resume and a target job description.
{keyword_checklist}
{analysis_section}
{strict_section}
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
   - Add new JD-relevant keywords or skills where they fit naturally{" — but ONLY if already present in my resume (strict mode)" if strict_mode else ""}.
   - Remove content that is clearly irrelevant to the target role.
   - Strengthen existing bullets with better action verbs or metrics{" based solely on original content (strict mode)" if strict_mode else ""}.
3. Open the Professional Summary with the exact target job title from the JD,
   followed by matching years of experience. Refine the rest of the summary
   to incorporate JD keywords while keeping the original narrative.
4. Maximize ATS match by naturally incorporating critical keywords INTO
   existing content:
   {keyword_frequency_guidance}
5. Order skills by relevance to the JD (most relevant first in each category).
   {skills_guidance}
6. Create semantic skill clusters inside the Skills section only — group
   related technologies as `.skill-category` blocks, not standalone sections.
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
{_STRICT_ATS_SCORING_NOTE if strict_mode else ""}

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
    strict_mode: bool = True,
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

    strict_refinement_reminder = ""
    if strict_mode:
        strict_refinement_reminder = """\
**STRICT MODE:** Add only missing keywords already supported by the original
resume. If unsupported, keep them missing. Do not invent facts.
Do not place missing keywords into Skills unless they are concrete hard
skills/tools already proven in the resume. Prefer evidence-backed Experience
phrasing over repeated keywords.
Keep any skill category inside the existing Skills section as `.skill-category`;
do not create standalone skill-category sections.

"""

    placement_guidance = (
        "- Supported hard skills/tools -> Skills only if concise and clearly "
        "proven by the resume.\n"
        "- Responsibilities, domains, soft skills, and generic phrases -> "
        "Summary/Experience only when evidenced.\n"
        "- Do not force keywords into multiple sections. Keep unsupported or "
        "weak keywords in missing_keywords."
        if strict_mode
        else "- Must-have keywords -> add to Professional Summary + Skills "
        "section + at least one Experience bullet each.\n"
        "- Preferred keywords -> add to Skills section and/or relevant "
        "Experience bullets.\n"
        "- Verify each primary keyword appears in at least 2-3 sections.\n"
        "- Verify all keywords are in meaningful, achievement-based contexts."
    )

    return f"""\
The following important keywords are still weak or missing in the resume:
{json.dumps(missing_keywords)}
{priority_section}{preserve_section}{strict_refinement_reminder}
Revise the resume HTML to incorporate the missing keywords naturally —
without exaggeration or keyword stuffing. Keep the same HTML structure
and class names. Weave keywords into EXISTING sentences and bullets
rather than replacing original content. The resume should still closely
resemble the candidate's original resume with targeted enhancements.

**Placement guidance:**
{placement_guidance}

{_ATS_SCORING_RUBRIC}
{_STRICT_ATS_SCORING_NOTE if strict_mode else ""}

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
    resp = _create_chat_completion(
        client,
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
    on_status: Callable[[str], None] | None = None,
    resume_analysis: dict | None = None,
    strict_mode: bool = True,
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
    on_status : callable, optional
        Called with plain-text status updates before longer-running steps.
    resume_analysis : dict, optional
        Structural analysis of the original resume from
        ``analyze_resume_structure``.
    strict_mode : bool, default True
        When True, the LLM is forbidden from adding any skill, experience,
        metric, or content not already present in the original resume.
        Optimization is limited to rephrasing, surfacing latent skills,
        acronym expansion, STAR restructuring, and keyword placement.
    """
    client = get_client(api_key)

    system_content = STRICT_SYSTEM_PROMPT if strict_mode else SYSTEM_PROMPT

    messages: list[dict] = [
        {"role": "system", "content": system_content},
        {
            "role": "user",
            "content": build_user_prompt(
                resume_text, jd_text, jd_keywords, primary_color,
                resume_analysis=resume_analysis,
                strict_mode=strict_mode,
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
        if on_status:
            on_status(f"Running optimization iteration {i + 1}...")
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
                    strict_mode=strict_mode,
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
    resp = _create_chat_completion(
        client,
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
# Two-phase approach: (1) extract structured JSON verbatim, (2) format to HTML.
# Separating extraction from formatting prevents the LLM from rephrasing or
# missing content when it has to do both tasks simultaneously.
# ---------------------------------------------------------------------------

_EXTRACT_SYSTEM_PROMPT = """\
You are a precise data extraction specialist. Your only task is to copy
resume content into a structured JSON format.

CRITICAL rules:
- Copy ALL text VERBATIM. Do NOT paraphrase, summarize, rephrase, add,
  or remove ANY content.
- Every job title, company name, date, location, bullet point, skill,
  degree, and metric must appear in the output EXACTLY as written.
- Preserve the EXACT section order from the source text. Do NOT reorder
  sections to match a "standard" resume format — output sections in the
  same sequence they appear in the input.
- When populating "bullets", "items", or any list field, strip any
  leading bullet/list character (•, ·, ▪, –, —, *, -, etc.) from the
  start of each item's text.  These are PDF rendering artefacts; the
  HTML <li> element provides the visual marker.
- For skill items: each individual skill/technology/tool MUST be its
  own separate string in the "skills" array — exactly one entry per
  skill, matching the boundaries from the original resume.  If the
  resume lists skills separated by spaces without commas (e.g.
  "TypeScript JavaScript React"), split them into individual array
  items: ["TypeScript", "JavaScript", "React"].  Multi-word skill names
  that form a single concept (e.g. "Material UI", "Angular (Latest)",
  "Node.js", "Tailwind CSS") stay as one item.  Skills with
  parenthetical sub-details are ONE item — do NOT split on commas
  inside parentheses, e.g. "GenAI (LLMs,RAG,embeddings,LangChain)"
  must remain a single array entry, not be split into GenAI, LLMs,
  RAG, etc.  Never concatenate multiple distinct skills into a single
  array entry.
- Do not infer or invent any information not present in the text.
"""

_FORMAT_SYSTEM_PROMPT = """\
You are an expert HTML formatter for resumes. You receive a structured
JSON representation of a resume and convert it to semantic HTML using the
exact CSS class names provided.

CRITICAL rules:
- Use the structured data AS-IS. Do NOT modify, rephrase, or add any
  content.
- Copy ALL text values VERBATIM from the input JSON into the HTML.
- Output sections in the EXACT order they appear in the JSON "sections"
  array. Do NOT reorder sections to match any assumed resume convention.
- Use the provided HTML structure and CSS class names precisely.
- Do NOT add <html>, <head>, <body>, or <style> tags.
- Do NOT add any inline style="" attributes — all styling is handled by
  the external template CSS.
- Do NOT insert extra <br> tags for spacing — use only the semantic
  block elements defined in the structure (<div>, <ul>, <li>, <p>).
- Do NOT add extra whitespace or blank lines inside text nodes — the
  template CSS controls all spacing and line-height.
"""


def _extract_resume_structured(
    resume_text: str,
    client: OpenAI,
    model: str = "gpt-4o-mini",
) -> dict:
    """Phase 1: Extract resume text into a structured JSON with verbatim content.

    Locks down the content before any formatting happens, preventing the
    formatter from rephrasing or dropping information.
    """
    prompt = f"""\
Extract the following resume into a structured JSON object.

CRITICAL: Copy all text VERBATIM — do not change, rephrase, summarize,
or omit any content. Every job title, company name, date, bullet point,
skill, and description must appear EXACTLY as written in the original.

Return a JSON object with this structure:
{{
  "name": "Full name exactly as written",
  "contact": {{
    "email": "email or null",
    "phone": "phone or null",
    "location": "city/state/country or null",
    "linkedin": "linkedin URL or handle or null",
    "github": "github URL or handle or null",
    "website": "personal website or null",
    "other": ["any other contact line items"]
  }},
  "sections": [
    {{
      "id": "lowercase_identifier",
      "heading": "Exact heading text as it appears in the resume",
      "type": "one of: summary|skills|experience|education|projects|certifications|other",
      "content": "verbatim paragraph text (for summary/other free-text sections)",
      "items": [
        // experience items:
        // {{"title": "verbatim", "company": "verbatim", "location": "verbatim or null",
        //   "dates": "verbatim", "bullets": ["verbatim bullet 1", ...]}}
        //
        // education items:
        // {{"degree": "verbatim", "school": "verbatim", "location": "verbatim or null",
        //   "dates": "verbatim or null", "details": ["verbatim detail"]}}
        //
        // project items:
        // {{"name": "verbatim", "dates": "verbatim or null",
        //   "description": "verbatim", "bullets": ["verbatim"]}}
        //
        // skill items:
        // {{"category": "verbatim category name", "skills": ["skill1", "skill2"]}}
        //
        // certification items:
        // {{"name": "verbatim", "issuer": "verbatim or null", "date": "verbatim or null"}}
        //
        // other items:
        // {{"text": "verbatim line or item"}}
      ]
    }}
  ]
}}

Include ALL sections present in the resume in the EXACT order they
appear in the text — do NOT reorder sections based on any assumed
"standard" resume format. The order in the JSON must match the order
in the source text.

If a section has both free-text content and list items, populate both
"content" and "items" fields.

RESUME TEXT:
\"\"\"{resume_text}\"\"\"
"""
    resp = _create_chat_completion(
        client,
        model=model,
        messages=[
            {"role": "system", "content": _EXTRACT_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    data = _parse_json_from_content(resp.choices[0].message.content)
    if not isinstance(data, dict) or "sections" not in data:
        raise RuntimeError(
            "Structured extraction did not return expected JSON format."
        )
    return data


def _format_structured_resume_to_html(
    resume_data: dict,
    content_structure: str,
    primary_color: str,
    client: OpenAI,
    model: str = "gpt-4o-mini",
) -> str:
    """Phase 2: Convert structured resume JSON to HTML.

    Because the content is already locked into the JSON, the LLM only
    needs to decide how to apply HTML tags — not interpret raw text.
    """
    prompt = f"""\
Convert the following structured resume data into HTML using the exact
structure below. Copy ALL text values VERBATIM from the JSON — do not
change any words, dates, or descriptions.

**HTML structure to use:**
{content_structure}

The accent color is {primary_color} — no inline styles needed; the
template CSS handles all fonts, sizes, colors, and spacing automatically.

**Formatting rules:**
- No inline style="" attributes anywhere.
- No extra <br> tags — use only the semantic block elements from the
  structure above.
- No extra whitespace inside text nodes (e.g. no leading/trailing spaces
  inside <li> or <p>).
- Section order must match the JSON "sections" array exactly.
- Skills: EVERY item in the JSON "skills" array MUST become its own
  SEPARATE <span class="skill-tag">SkillName</span> element.
  If the JSON has ["TypeScript","React","Next.js"], output:
      <span class="skill-tag">TypeScript</span>
      <span class="skill-tag">React</span>
      <span class="skill-tag">Next.js</span>
  NEVER concatenate multiple skills into one span. NEVER put skills as
  comma-separated bare text — each skill = one span, always.
- Do NOT include bullet characters (•, -, *, etc.) inside <li> text —
  the CSS list-style provides the bullet automatically.

**RESUME DATA (JSON):**
```json
{json.dumps(resume_data, indent=2, ensure_ascii=False)}
```

**Return a single JSON object with exactly this key:**
- "resume_html": the full resume as HTML following the structure above.
"""
    resp = _create_chat_completion(
        client,
        model=model,
        messages=[
            {"role": "system", "content": _FORMAT_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    data = _parse_json_from_content(resp.choices[0].message.content)
    if not isinstance(data, dict) or "resume_html" not in data:
        raise RuntimeError("Model did not return the expected JSON format.")
    return data["resume_html"]


def _split_on_top_level_delimiters(text: str) -> list[str]:
    """Split text on commas, semicolons, or pipes that are NOT inside parentheses.

    This keeps parenthetical sub-lists as part of the parent skill, e.g.:
        "GenAI (LLMs,RAG,embeddings,LangChain)"  → one item
        "Python, JavaScript, React"               → three items
    """
    items: list[str] = []
    current: list[str] = []
    depth = 0
    for ch in text:
        if ch in "([{":
            depth += 1
            current.append(ch)
        elif ch in ")]}":
            depth = max(depth - 1, 0)
            current.append(ch)
        elif ch in ",;|" and depth == 0:
            item = "".join(current).strip()
            if item:
                items.append(item)
            current = []
        else:
            current.append(ch)
    tail = "".join(current).strip()
    if tail:
        items.append(tail)
    return items


def _skills_from_text(text: str) -> list[str]:
    """Split a skill list text into individual skill names.

    Only splits on explicit top-level delimiters (comma, semicolon, pipe).
    Delimiters inside parentheses are treated as part of the skill name,
    so "GenAI (LLMs,RAG,embeddings,LangChain)" stays as a single item.

    Space-separated skill lists without any delimiter are NOT split here —
    that boundary information must come from Phase 1 JSON extraction where
    the LLM identifies each skill from context.  Guessing at space-
    separated boundaries causes incorrect splits for multi-word skills
    like "Material UI", "Angular (Latest)", etc.
    """
    stripped = text.strip().lstrip(":").strip()
    if not stripped:
        return []
    if re.search(r"[,;|]", stripped):
        return [s for s in _split_on_top_level_delimiters(stripped) if s]
    return [stripped]


def _replace_skill_tags(div, soup: BeautifulSoup, skills: list[str]) -> None:
    """Remove existing skill-tag spans in div and add one span per skill."""
    for tag in div.find_all(class_="skill-tag"):
        tag.extract()
    # Clean up leftover whitespace-only text nodes after the strong label.
    strong = div.find("strong")
    if strong:
        # Snapshot siblings before mutating the tree during iteration.
        for node in [*strong.next_siblings]:
            if isinstance(node, NavigableString) and not node.strip():
                node.extract()
    for i, skill in enumerate(skills):
        if i > 0:
            div.append(NavigableString(" "))
        span = soup.new_tag("span")
        span["class"] = "skill-tag"
        span.string = skill
        div.append(span)


def _fix_skill_categories(html: str) -> str:
    """Ensure each skill in .skill-category elements is its own skill-tag span.

    Handles three common LLM failure modes:

    A) No skill-tag spans at all — skills are a plain text node:
           <strong>Languages:</strong> Python, JavaScript, React

    B) A single skill-tag span containing comma-separated multiple skills:
           <span class="skill-tag">Python, JavaScript, React</span>

    C) A single skill-tag span containing space-separated multiple skills
       (no explicit delimiter), e.g.:
           <span class="skill-tag">TypeScript React Angular (Latest) Next.js</span>

    All three patterns are rewritten to individual per-skill spans.
    """
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception:
        return html

    modified = False

    for div in soup.find_all(class_="skill-category"):
        existing_tags = div.find_all(class_="skill-tag")
        strong = div.find("strong")

        if not existing_tags:
            # ── Case A: plain text, no spans yet ──────────────────────────
            if strong:
                text_nodes = [
                    n for n in strong.next_siblings
                    if isinstance(n, NavigableString)
                ]
            else:
                text_nodes = [
                    n for n in div.children
                    if isinstance(n, NavigableString)
                ]
            raw = "".join(str(n) for n in text_nodes)
            skills = _skills_from_text(raw)
            if len(skills) < 1:
                continue
            for node in text_nodes:
                node.extract()
            for i, skill in enumerate(skills):
                if i > 0:
                    div.append(NavigableString(" "))
                span = soup.new_tag("span")
                span["class"] = "skill-tag"
                span.string = skill
                div.append(span)
            modified = True

        else:
            # ── Case B: already has spans — fix only when explicit delimiter
            #    (comma/semicolon/pipe) is found inside a span.  Space-only
            #    spans are left untouched: their correct split boundaries
            #    must come from Phase 1 JSON extraction, not from guessing.
            all_skills: list[str] = []
            needs_fix = False

            for tag in existing_tags:
                tag_text = tag.get_text().strip()
                if re.search(r"[,;|]", tag_text):
                    parts = _skills_from_text(tag_text)
                    all_skills.extend(parts)
                    if len(parts) > 1:
                        needs_fix = True
                else:
                    if tag_text:
                        all_skills.append(tag_text)

            if not needs_fix:
                continue

            skills = [s for s in all_skills if s]
            if not skills:
                continue

            _replace_skill_tags(div, soup, skills)
            modified = True

    if not modified:
        return html

    return str(soup)


_SPACING_CSS_PROPS = {
    "margin",
    "margin-top",
    "margin-bottom",
    "margin-left",
    "margin-right",
    "padding",
    "padding-top",
    "padding-bottom",
    "padding-left",
    "padding-right",
    "gap",
    "row-gap",
    "column-gap",
    "line-height",
}


def _filter_style_attr(m: re.Match) -> str:
    """Keep only spacing-related CSS declarations from an inline style attribute.

    Non-spacing properties (font, color, background, etc.) are stripped so
    they cannot override the template CSS. Spacing properties (margin,
    padding, gap, line-height) are preserved so user-requested spacing
    edits survive PDF export.
    """
    style_value = m.group(1)
    kept = []
    for decl in style_value.split(";"):
        decl = decl.strip()
        if not decl:
            continue
        prop = decl.split(":")[0].strip().lower()
        if prop in _SPACING_CSS_PROPS:
            kept.append(decl)
    if kept:
        return f' style="{"; ".join(kept)}"'
    return ""


def clean_resume_html(html: str) -> str:
    """Sanitise LLM-generated resume HTML before PDF export or preview.

    Applied to every content_html that flows into a PDF — whether it came
    from the initial load (convert_resume_to_html), an AI edit
    (edit_resume_html), or the ATS optimiser (optimize_until_target).

    Fixes applied:
    1. Inline style="" attributes — strip properties that override the
       template CSS (font, color, background, etc.) while preserving
       spacing properties (margin, padding, gap, line-height) so that
       user-requested spacing edits survive PDF export.
    2. Leading bullet glyphs inside <li> — PDF bullet chars copied
       verbatim produce a double-bullet alongside the CSS list marker.
    3. Comma-separated skill lists — skills not wrapped in individual
       <span class="skill-tag"> elements are split and wrapped so the
       template CSS renders them correctly.
    """
    # 1. Filter inline style attributes — preserve spacing, strip the rest.
    html = re.sub(r'\s*style\s*=\s*"([^"]*)"', _filter_style_attr, html)
    # 2. Remove leading bullet chars from <li> content.
    html = re.sub(
        r"(<li[^>]*>)\s*[•·◦▪▸▹►▶●○◉‣⁃–—]\s*",
        r"\1",
        html,
    )
    # 3. Split comma-separated skills into individual skill-tag spans.
    html = _fix_skill_categories(html)
    return html


def convert_resume_to_html(
    resume_text: str,
    primary_color: str = "#2563eb",
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
    resume_analysis: dict | None = None,
    on_status: Callable[[str], None] | None = None,
) -> str:
    """Convert resume text to structured HTML without any ATS optimization.

    Uses a two-phase approach for faithful reproduction:
    1. Extract a verbatim structured JSON representation of the resume.
    2. Format the locked-down JSON into semantic HTML.

    This separation prevents the single-pass problem where the LLM
    simultaneously parses raw text and produces HTML, which causes it to
    rephrase or drop content.
    """
    client = get_client(api_key)
    content_structure = build_content_structure(resume_analysis)

    if on_status:
        on_status("Extracting resume content (verbatim)...")
    resume_data = _extract_resume_structured(resume_text, client, model)

    if on_status:
        on_status("Formatting resume to HTML...")
    html = _format_structured_resume_to_html(
        resume_data=resume_data,
        content_structure=content_structure,
        primary_color=primary_color,
        client=client,
        model=model,
    )

    return clean_resume_html(html)


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

    resp = _create_chat_completion(
        client,
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
