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
| `app.py` | Streamlit web application. Manages UI state, input validation, session caching, theme preview, progress display, and file downloads. |
| `__main__.py` | CLI entry point (`python -m ats_resume_optimizer`). Parses arguments with argparse and calls `run_resume_agent()`. |
| `agent.py` (root) | Thin CLI wrapper that imports and runs `__main__.main()`. |

### Orchestration Layer

| Module | Role |
|---|---|
| `ats_resume_optimizer/agent.py` | Central pipeline coordinator. Composes the extraction, optimization, rendering, and export steps into two high-level functions: `optimize_resume()` and `export_resume_pdf()`. |

### Service Layer

| Module | Role |
|---|---|
| `resume.py` | Extracts plain text from a resume PDF using `pypdf`. |
| `job_description.py` | Resolves a job description from either raw text or a URL (fetched with `requests`, parsed with BeautifulSoup). |
| `llm.py` | All OpenAI interactions — client setup, system/user prompts, single-call optimization, iterative refinement loop, and title/company extraction. |
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
Job URL     ──► job_description.py:fetch_jd_from_url()  ──► plain text string
Job Text    ──► passed through directly
```

### 2. Metadata Extraction

```
JD text  ──► llm.py:extract_title_and_company()  ──► (job_title, company)
```

A lightweight LLM call extracts structured fields from the JD for use in the output filename.

### 3. Iterative Optimization

```
                    ┌──────────────────────────────────────┐
                    │     optimize_until_target()           │
                    │                                      │
resume_text ──►     │  ┌─► Build messages ─► LLM call      │
jd_text     ──►     │  │   (system + user prompt)          │
                    │  │                                    │
                    │  │   ◄── JSON response:               │
                    │  │       tailored_resume_html          │
                    │  │       ats_score                     │
                    │  │       missing_keywords              │
                    │  │       changes_summary               │
                    │  │                                    │
                    │  │   Score ≥ target? ── yes ──► return │
                    │  │       │ no                          │
                    │  │       ▼                             │
                    │  └── Append refinement prompt          │
                    │      with missing keywords             │
                    │                                      │
                    └──────────────────────────────────────┘
```

The loop maintains a growing conversation history (multi-turn chat) so each iteration builds on the previous result. The best result (highest ATS score) is always tracked and returned.

### 4. Template Rendering

```
content_html  ──► templates:render_resume(template_id, content_html, color)
                       │
                       ▼
              Full HTML document (DOCTYPE, head with CSS, body with content)
```

The AI produces content HTML with semantic class names. The template wraps it in a complete HTML document with its own CSS that targets those class names.

### 5. PDF Export

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
| **Subprocess for PDF export** | Playwright requires its own asyncio event loop, which conflicts with Streamlit's loop on Windows. A subprocess isolates the two. |
| **Semantic HTML contract** | Decouples AI-generated content from visual presentation. Any template can style the same content differently. |
| **Iterative refinement** | A single LLM pass often misses niche keywords. Multi-turn conversation allows progressive improvement. |
| **Best-result tracking** | The loop returns the highest-scoring result, not necessarily the last one, guarding against score regression. |
| **OrderedDict for templates** | Preserves insertion order in the UI dropdown, ensuring a curated presentation sequence. |
| **Color utilities in `_colors.py`** | Lets templates derive consistent light/dark variants from any user-chosen accent color. |

## Error Handling

| Layer | Strategy |
|---|---|
| **LLM responses** | `_parse_json_from_content()` handles `None`, empty strings, and markdown-wrapped JSON. Raises `RuntimeError` with a content preview on parse failure. |
| **API key validation** | `get_client()` raises `ValueError` early if no key is available. |
| **Resume extraction** | `extract_resume_text()` raises `ValueError` if no text is found (e.g., scanned/image-only PDFs). |
| **JD resolution** | `get_job_description()` raises `ValueError` if neither text nor URL is provided. URL fetching propagates HTTP errors. |
| **PDF generation** | `html_to_pdf()` raises `RuntimeError` with stderr output on subprocess failure. Temp files are cleaned up in a `finally` block. |
| **Streamlit UI** | Wraps pipeline calls in try/except, displaying errors via `st.error()` and halting with `st.stop()`. |
