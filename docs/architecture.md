# Architecture

This document describes the system design, module responsibilities, and data flow of ATS Resume Optimizer.

## High-Level Overview

ATS Resume Optimizer is a pipeline-based application that takes a resume PDF and a job description as input, then produces an ATS-optimized resume PDF styled with a user-selected theme.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                        │
│                                                                    │
│   ┌──────────────────────┐      ┌──────────────────────────────┐   │
│   │   Streamlit Web UI   │      │   CLI (argparse)             │   │
│   │   app.py             │      │   __main__.py / agent.py     │   │
│   └──────────┬───────────┘      └──────────────┬───────────────┘   │
│              │                                  │                  │
└──────────────┼──────────────────────────────────┼──────────────────┘
               │                                  │
               ▼                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Orchestration Layer                          │
│                                                                    │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │   agent.py                                                  │  │
│   │   optimize_resume()  →  export_resume_pdf()                 │  │
│   │   run_resume_agent() (convenience: optimize + export)       │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
└────────┬──────────┬──────────┬──────────┬──────────┬───────────────┘
         │          │          │          │          │
         ▼          ▼          ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌────────┐ ┌────────┐ ┌────────────────┐
│resume.py │ │job_desc. │ │llm.py  │ │templat-│ │pdf_export.py   │
│          │ │py        │ │        │ │es/     │ │+ _pdf_worker.py│
│ Extract  │ │ Fetch JD │ │ OpenAI │ │ Render │ │ HTML → PDF     │
│ text     │ │ text/URL │ │ calls  │ │ HTML   │ │ (Playwright)   │
└──────────┘ └──────────┘ └────────┘ └────────┘ └────────────────┘
```

## Module Responsibilities

### User Interface Layer

| Module | Role |
|---|---|
| `app.py` | Streamlit web application. Manages UI state, input validation, session caching, theme preview, progress display (including strategies and verified scores), and file downloads. |
| `__main__.py` | CLI entry point (`python -m ats_resume_optimizer`). Parses arguments with argparse and calls `run_resume_agent()`. Displays iteration progress with strategies and keyword categories. |
| `agent.py` (root) | Thin CLI wrapper that imports and runs `__main__.main()`. |

### Orchestration Layer

| Module | Role |
|---|---|
| `ats_resume_optimizer/agent.py` | Central pipeline coordinator. Composes the extraction, JD keyword analysis, optimization, rendering, and export steps into two high-level functions: `optimize_resume()` and `export_resume_pdf()`. Supports `on_status` and `on_iteration` callbacks for progress reporting. |

### Service Layer

| Module | Role |
|---|---|
| `resume.py` | Extracts plain text from a resume PDF using `pypdf`. |
| `job_description.py` | Resolves a job description from either raw text or a URL (fetched with `requests` and User-Agent header, parsed with BeautifulSoup using platform-specific selectors for Greenhouse, Lever, Workday, LinkedIn, Indeed, and generic pages). Strips EEO boilerplate from URL-fetched content. |
| `llm.py` | All OpenAI interactions — client setup, system/user/refinement prompts with ATS scoring rubric, JD keyword extraction (`extract_jd_keywords`), programmatic keyword verification (`verify_keyword_coverage`), single-call optimization, iterative refinement loop with strategy tracking, and title/company extraction. |
| `templates/` | Template registry and rendering. Each theme is a self-contained module; the registry provides a unified `render_resume()` API. |
| `pdf_export.py` | Converts fully-rendered HTML to an A4 PDF using Playwright's Chromium engine. Runs in a subprocess to avoid event-loop conflicts. |
| `_pdf_worker.py` | Subprocess script that performs the actual Playwright PDF rendering. |
| `config.py` | Defines project-wide path constants (`BASE_DIR`, `RESUME_DIR`, `OUTPUT_DIR`). |
| `utils.py` | Filename sanitization and output path construction. |
| `templates/_colors.py` | Color manipulation: `hex_to_rgb`, `rgb_to_hex`, `lighten`, `darken`. |

## Data Flow

### 1. Input Acquisition

```
Resume PDF  ──► resume.py:extract_resume_text()  ──► plain text string
Job URL     ──► job_description.py:fetch_jd_from_url()  ──► cleaned text string
Job Text    ──► passed through directly
```

### 2. JD Keyword Extraction (new in v1.1)

```
JD text  ──► llm.py:extract_jd_keywords()  ──► structured keyword dict
                                                 ├── job_title
                                                 ├── required_hard_skills  (must-have)
                                                 ├── required_soft_skills  (must-have)
                                                 ├── preferred_skills      (preferred)
                                                 ├── required_experience
                                                 ├── required_education
                                                 ├── key_responsibilities
                                                 ├── industry_terms        (preferred)
                                                 ├── action_verbs
                                                 └── certifications        (preferred)
```

A dedicated LLM call extracts and categorizes all keywords from the JD before optimization begins. This checklist is passed to the optimizer and used for programmatic verification.

### 3. Metadata Extraction

```
JD text  ──► llm.py:extract_title_and_company()  ──► (job_title, company)
```

A lightweight LLM call extracts structured fields from the JD for use in the output filename.

### 4. Iterative Optimization

```
                    ┌──────────────────────────────────────────┐
                    │     optimize_until_target()               │
                    │                                          │
resume_text ──►     │  ┌─► Build messages ─► LLM call          │
jd_text     ──►     │  │   (system + user prompt               │
jd_keywords ──►     │  │    + keyword checklist                 │
                    │  │    + ATS scoring rubric)               │
                    │  │                                        │
                    │  │   ◄── JSON response:                   │
                    │  │       tailored_resume_html              │
                    │  │       ats_score (rubric-based)          │
                    │  │       missing_keywords                  │
                    │  │       strategies_applied                │
                    │  │       changes_summary                   │
                    │  │                                        │
                    │  │   ──► verify_keyword_coverage()         │
                    │  │       (programmatic check against       │
                    │  │        extracted JD keywords)           │
                    │  │       ◄── verified_score, must-have     │
                    │  │           score, missing by priority    │
                    │  │                                        │
                    │  │   Score ≥ target? ── yes ──► return     │
                    │  │       │ no                              │
                    │  │       ▼                                 │
                    │  └── Append priority-aware refinement      │
                    │      prompt with:                          │
                    │      - must-have missing keywords          │
                    │      - preferred missing keywords          │
                    │      - placement guidance                  │
                    │      - resolved keywords to preserve       │
                    │      - title/experience warnings           │
                    │                                          │
                    └──────────────────────────────────────────┘
```

The loop maintains a growing conversation history (multi-turn chat) so each iteration builds on the previous result. The best result (highest verified score when available, otherwise highest LLM score) is always tracked and returned. Applied strategies are accumulated across iterations.

### 5. Template Rendering

```
content_html  ──► templates:render_resume(template_id, content_html, color)
                       │
                       ▼
              Full HTML document (DOCTYPE, head with CSS, body with content)
```

The AI produces content HTML with semantic class names. The template wraps it in a complete HTML document with its own CSS that targets those class names.

### 6. PDF Export

```
full_html  ──► pdf_export.py:html_to_pdf()
                    │
                    ├── Inject page-break CSS
                    ├── Write to temp .html file
                    ├── Spawn subprocess: _pdf_worker.py
                    │       │
                    │       ├── Launch headless Chromium
                    │       ├── Load HTML (wait for networkidle)
                    │       └── page.pdf() → output .pdf
                    │
                    └── Clean up temp file
```

## ATS Optimization Strategies

The system tracks 14 named optimization strategies across iterations:

| Strategy | Description |
|---|---|
| Job Title Mirroring | Opens the Professional Summary with the exact JD job title. |
| Keyword Frequency Optimization | Ensures primary keywords appear in 2-3 sections. |
| Semantic Skill Clustering | Groups related technologies into coherent clusters. |
| Action Verb Matching | Uses the exact action verbs from the JD in bullets. |
| Experience Alignment | Matches the JD's required years/level of experience. |
| Soft Skills Integration | Includes soft skills mentioned in the JD. |
| Acronym Expansion | Provides both spelled-out terms and acronyms. |
| STAR Method Bullets | Frames bullets with Situation, Task, Action, Result. |
| Must-Have Prioritization | Prioritizes required skills over preferred ones. |
| Contextual Keyword Embedding | Places keywords in achievement-based contexts. |
| Skills Ordering by Relevance | Orders skills by relevance to the JD. |
| Exact Phrase Matching | Uses the JD's exact multi-word phrases. |
| Quantified Achievements | Uses digits for all metrics and achievements. |
| Date Format Consistency | Maintains consistent "Mon YYYY - Mon YYYY" format. |

## Session Caching (Streamlit)

The web UI implements input fingerprinting for cache efficiency:

```
Input fingerprint = SHA-256(
    use_default_resume | uploaded_file_id | jd_text | jd_url | target_score | max_iterations
)
```

When the fingerprint changes, the cached optimization result is invalidated. When only the theme or color changes, the cached `content_html` is reused and only the rendering + PDF export steps are re-run (via the "Re-export with Style" button).

## Key Design Decisions

| Decision | Rationale |
|---|---|
| **Pre-optimization keyword extraction** | A dedicated LLM call extracts and categorizes JD keywords before optimization. This provides a ground-truth checklist for both the optimizer and the programmatic verifier, eliminating reliance on the model's ad-hoc keyword discovery. |
| **Programmatic verification** | The LLM's self-assessed ATS score is supplemented by a deterministic keyword-match check against extracted JD keywords. This catches inflated scores and ensures real keyword coverage. |
| **Must-have vs. preferred prioritization** | Real ATS systems use knockout filters for required skills. The optimization mirrors this by giving must-have keywords explicit placement guidance and higher weight. |
| **Strategy tracking** | Named strategies make the optimization process transparent and debuggable. Users can see exactly which techniques were applied in each iteration. |
| **ATS scoring rubric** | Providing a rubric (keyword match 40%, contextual relevance 25%, section completeness 15%, title alignment 10%, experience alignment 10%) grounds the LLM's scoring instead of allowing arbitrary estimates. |
| **Resolved-keyword preservation** | Refinement prompts explicitly list previously resolved keywords and instruct the model not to remove them, preventing regression across iterations. |
| **Subprocess for PDF export** | Playwright requires its own asyncio event loop, which conflicts with Streamlit's loop on Windows. A subprocess isolates the two. |
| **Semantic HTML contract** | Decouples AI-generated content from visual presentation. Any template can style the same content differently. |
| **Iterative refinement** | A single LLM pass often misses niche keywords. Multi-turn conversation allows progressive improvement. |
| **Best-result tracking** | The loop returns the highest-scoring result (by verified score), not necessarily the last one, guarding against score regression. |
| **OrderedDict for templates** | Preserves insertion order in the UI dropdown, ensuring a curated presentation sequence. |
| **Color utilities in `_colors.py`** | Lets templates derive consistent light/dark variants from any user-chosen accent color. |

## Error Handling

| Layer | Strategy |
|---|---|
| **LLM responses** | `_parse_json_from_content()` handles `None`, empty strings, and markdown-wrapped JSON. Raises `RuntimeError` with a content preview on parse failure. |
| **API key validation** | `get_client()` raises `ValueError` early if no key is available. |
| **Resume extraction** | `extract_resume_text()` raises `ValueError` if no text is found (e.g., scanned/image-only PDFs). |
| **JD resolution** | `get_job_description()` raises `ValueError` if neither text nor URL is provided. URL fetching propagates HTTP errors. |
| **JD keyword extraction** | `extract_jd_keywords()` falls back to an empty dict on parse failure, allowing optimization to proceed without the keyword checklist. |
| **Keyword verification** | `verify_keyword_coverage()` handles missing categories gracefully, returning zero scores when no keywords are available. |
| **Strategy tracking** | Missing or malformed `strategies_applied` in LLM responses defaults to an empty list without failing. |
| **PDF generation** | `html_to_pdf()` raises `RuntimeError` with stderr output on subprocess failure. Temp files are cleaned up in a `finally` block. |
| **Streamlit UI** | Wraps pipeline calls in try/except, displaying errors via `st.error()` and halting with `st.stop()`. |
