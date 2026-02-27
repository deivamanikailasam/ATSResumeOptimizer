# Configuration

This document covers all configuration options for ATS Resume Optimizer.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key. Used for all LLM calls (resume optimization, title/company extraction). Can also be entered at runtime via the Streamlit sidebar. |

### Setting Up `.env`

Create a `.env` file in the project root (it is gitignored):

```
OPENAI_API_KEY=sk-proj-...
```

The key is loaded automatically at module import time via `python-dotenv`.

## Directory Structure

Configured in `ats_resume_optimizer/config.py`:

| Constant | Path | Description |
|---|---|---|
| `BASE_DIR` | Project root | Resolved from the package location. |
| `RESUME_DIR` | `memory/docs/` | Input resume directory. Place `base_resume.pdf` here. |
| `OUTPUT_DIR` | `memory/docs/generated/` | Output directory for generated PDFs. Created automatically. |

The `memory/` directory is gitignored. It contains user-specific data (resumes and generated output).

### Directory Layout

```
memory/
└── docs/
    ├── base_resume.pdf           ← Your default resume (place here manually)
    ├── uploaded_resume.pdf       ← Created when uploading via Streamlit
    └── generated/
        ├── Senior_Engineer_Acme.pdf
        └── ...                   ← Generated PDFs named by job title + company
```

## Streamlit UI Settings

These options are configured in the sidebar at runtime:

| Setting | Default | Range | Description |
|---|---|---|---|
| OpenAI API key | — | — | API key (overrides `.env` if provided). |
| Target ATS score | 95 | 70–100 | The optimization loop stops when this score is reached. |
| Max iterations | 5 | 1–10 | Maximum number of LLM refinement passes. |
| Use default resume | Checked | — | Use `memory/docs/base_resume.pdf`. Uncheck to upload. |

### Main Area Settings

| Setting | Default | Description |
|---|---|---|
| Job URL | — | URL to a job posting page. |
| Job description | — | Raw job description text. Text takes precedence over URL. |
| Theme | Modern Minimal | One of 37+ available resume templates. |
| Accent color | `#2563eb` | Primary color used by the template. |

## CLI Arguments

Full reference for `python -m ats_resume_optimizer`:

| Argument | Type | Default | Description |
|---|---|---|---|
| `--jd-text` | `str` | — | Job description text. |
| `--jd-url` | `str` | — | URL to scrape job description from. |
| `--resume` | `str` | `memory/docs/base_resume.pdf` | Path to base resume PDF. |
| `--target-score` | `int` | `95` | Target ATS score. |
| `--max-iterations` | `int` | `5` | Max optimization iterations. |
| `--template` | `str` | `modern_minimal` | Template ID (use `--help` to see all choices). |
| `--color` | `str` | `#2563eb` | Accent color hex code. |

## LLM Configuration

Configured in `ats_resume_optimizer/llm.py`:

| Setting | Value | Location | Description |
|---|---|---|---|
| Model | `gpt-4o-mini` | `optimize_resume_once()`, `extract_title_and_company()` | OpenAI chat model used for all calls. |
| Temperature | `0.3` | `optimize_resume_once()` | Controls output randomness. Low value for consistent, focused output. |
| Temperature (extraction) | `0.0` | `extract_title_and_company()` | Deterministic for structured extraction. |

To use a different model, modify the `model` parameter in `llm.py` or pass it through the `optimize_until_target()` function.

## PDF Export Configuration

Configured in `ats_resume_optimizer/pdf_export.py` and `_pdf_worker.py`:

| Setting | Value | Description |
|---|---|---|
| Page format | A4 | Standard international paper size. |
| Print background | `True` | Renders background colors and images in the PDF. |
| CSS page size | `True` (`prefer_css_page_size`) | Respects `@page` CSS rules from templates. |
| Wait strategy | `networkidle` | Waits for network idle before rendering (ensures fonts/assets load). |

## Output Naming Convention

Generated PDFs are named using the pattern:

```
{JobTitle}_{Company}.pdf
```

Both values are sanitized to contain only alphanumeric characters, underscores, and hyphens. Spaces are converted to underscores. Defaults to `UnknownRole_UnknownCompany.pdf` if extraction fails.

**Examples:**

- `Senior_Software_Engineer_Google.pdf`
- `Data_Scientist_Netflix.pdf`
- `Product_Manager_Stripe.pdf`
