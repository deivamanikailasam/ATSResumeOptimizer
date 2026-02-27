# API Reference

Complete reference for all public modules, functions, and constants in the `ats_resume_optimizer` package.

---

## `ats_resume_optimizer`

**Package-level exports** from `__init__.py`.

| Export | Type | Description |
|---|---|---|
| `__version__` | `str` | Package version, read from the `VERSION` file. |
| `optimize_resume` | function | Run the optimization pipeline; return cached-friendly results. |
| `export_resume_pdf` | function | Render and export a PDF from cached content. |
| `run_resume_agent` | function | Full pipeline: optimize + export in one call. |
| `BASE_DIR` | `Path` | Project root directory. |
| `RESUME_DIR` | `Path` | Base resume directory (`memory/docs/`). |
| `OUTPUT_DIR` | `Path` | Generated PDF output directory (`memory/docs/generated/`). |

---

## `ats_resume_optimizer.agent`

Orchestration module — composes extraction, JD keyword analysis, optimization, rendering, and export.

### `optimize_resume()`

```python
def optimize_resume(
    base_resume_pdf: Path,
    jd_text: str | None = None,
    jd_url: str | None = None,
    target_score: int = 95,
    max_iterations: int = 5,
    primary_color: str = "#2563eb",
    api_key: str | None = None,
    on_iteration: Callable[[dict], None] | None = None,
    on_status: Callable[[str], None] | None = None,
) -> dict
```

Run the full optimization pipeline without exporting to PDF. Internally calls `extract_jd_keywords()` for structured keyword extraction, `extract_title_and_company()` for metadata, and `optimize_until_target()` for iterative optimization with programmatic verification.

**Parameters:**

| Name | Type | Default | Description |
|---|---|---|---|
| `base_resume_pdf` | `Path` | — | Path to the input resume PDF. |
| `jd_text` | `str \| None` | `None` | Job description text. |
| `jd_url` | `str \| None` | `None` | URL to scrape job description from. |
| `target_score` | `int` | `95` | Target ATS score (0–100). |
| `max_iterations` | `int` | `5` | Maximum optimization iterations. |
| `primary_color` | `str` | `"#2563eb"` | Accent color hex code. |
| `api_key` | `str \| None` | `None` | OpenAI API key (falls back to env). |
| `on_iteration` | `Callable` | `None` | Callback invoked after each iteration (see below). |
| `on_status` | `Callable` | `None` | Callback invoked with progress messages (e.g., `"Extracting keywords from job description..."`). |

**Returns:** `dict` with keys:

| Key | Type | Description |
|---|---|---|
| `content_html` | `str` | Optimized resume as semantic HTML. |
| `job_title` | `str` | Extracted job title. |
| `company` | `str` | Extracted company name. |
| `jd_keywords` | `dict` | Structured keywords extracted from the JD (see `extract_jd_keywords()`). |

---

### `export_resume_pdf()`

```python
def export_resume_pdf(
    content_html: str,
    template_id: str,
    primary_color: str,
    job_title: str,
    company: str,
) -> Path
```

Render content HTML with a template and export to PDF.

**Parameters:**

| Name | Type | Description |
|---|---|---|
| `content_html` | `str` | Semantic HTML content (from `optimize_resume()`). |
| `template_id` | `str` | Template identifier (e.g., `"modern_minimal"`). |
| `primary_color` | `str` | Accent color hex code. |
| `job_title` | `str` | Job title for output filename. |
| `company` | `str` | Company name for output filename. |

**Returns:** `Path` — path to the generated PDF file.

---

### `run_resume_agent()`

```python
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
    on_status: Callable[[str], None] | None = None,
) -> Path
```

Convenience function that runs `optimize_resume()` followed by `export_resume_pdf()`.

**Parameters:** Same as `optimize_resume()` plus `template_id`.

**Returns:** `Path` — path to the generated PDF file.

---

## `ats_resume_optimizer.llm`

OpenAI client management, prompt construction, keyword extraction, programmatic verification, and optimization logic.

### Constants

| Name | Type | Description |
|---|---|---|
| `SYSTEM_PROMPT` | `str` | System message defining the LLM's role with research-backed ATS optimization rules covering keyword strategy, job title alignment, skills optimization, experience bullets, and formatting. |
| `ATS_STRATEGIES` | `list[str]` | The 14 named ATS optimization strategies tracked across iterations. |

**`ATS_STRATEGIES` values:**

`"Job Title Mirroring"`, `"Keyword Frequency Optimization"`, `"Semantic Skill Clustering"`, `"Action Verb Matching"`, `"Experience Alignment"`, `"Soft Skills Integration"`, `"Acronym Expansion"`, `"STAR Method Bullets"`, `"Must-Have Prioritization"`, `"Contextual Keyword Embedding"`, `"Skills Ordering by Relevance"`, `"Exact Phrase Matching"`, `"Quantified Achievements"`, `"Date Format Consistency"`.

### `get_client()`

```python
def get_client(api_key: str | None = None) -> OpenAI
```

Return an OpenAI client. Uses the provided `api_key`, or falls back to the `OPENAI_API_KEY` environment variable.

**Raises:** `ValueError` if no API key is available.

---

### `extract_jd_keywords()`

```python
def extract_jd_keywords(
    jd_text: str,
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
) -> dict
```

Extract structured, prioritized keywords from a job description using a dedicated LLM call (temperature 0).

**Returns:** `dict` with keys:

| Key | Type | Description |
|---|---|---|
| `job_title` | `str` | Exact job title from the posting. |
| `required_hard_skills` | `list[str]` | Mandatory technical skills, tools, technologies. |
| `required_soft_skills` | `list[str]` | Required soft skills (leadership, communication, etc.). |
| `preferred_skills` | `list[str]` | Nice-to-have / preferred skills. |
| `required_experience` | `str` | Required years of experience (e.g., `"5+ years"`). |
| `required_education` | `str` | Required education level. |
| `key_responsibilities` | `list[str]` | Core responsibility phrases from the JD. |
| `industry_terms` | `list[str]` | Industry-specific jargon and methodologies. |
| `action_verbs` | `list[str]` | Specific action verbs from the JD. |
| `certifications` | `list[str]` | Mentioned certifications or licenses. |

---

### `verify_keyword_coverage()`

```python
def verify_keyword_coverage(html_content: str, jd_keywords: dict) -> dict
```

Programmatically check which JD keywords actually appear in the generated resume HTML. Extracts plain text from the HTML and performs case-insensitive substring matching against all categorized keywords.

**Returns:** `dict` with keys:

| Key | Type | Description |
|---|---|---|
| `by_category` | `dict[str, list[dict]]` | Per-category results. Each item: `{"keyword": str, "found": bool, "priority": str}`. |
| `title_match` | `bool` | Whether the JD job title appears in the resume. |
| `experience_match` | `bool` | Whether the JD's required experience years appear. |
| `programmatic_score` | `int` | Overall keyword match percentage (0–100). |
| `must_have_score` | `int` | Must-have keyword match percentage (0–100). |
| `total_keywords` | `int` | Total keywords checked. |
| `found_keywords` | `int` | Keywords found in the resume. |
| `must_have_total` | `int` | Total must-have keywords. |
| `must_have_found` | `int` | Must-have keywords found. |
| `missing_must_have` | `list[str]` | Must-have keywords not found. |
| `missing_preferred` | `list[str]` | Preferred keywords not found. |

---

### `build_user_prompt()`

```python
def build_user_prompt(
    resume_text: str,
    jd_text: str,
    jd_keywords: dict | None = None,
    primary_color: str = "#2563eb",
) -> str
```

Construct the initial user prompt containing the resume text, job description, pre-extracted keyword checklist (with priority tags), HTML structure guide, ATS scoring rubric, and output format instructions (including `strategies_applied`).

---

### `optimize_resume_once()`

```python
def optimize_resume_once(
    client: OpenAI,
    messages: list[dict],
    model: str = "gpt-4o-mini",
) -> dict
```

Execute a single LLM chat completion call (temperature 0.2) and parse the JSON response.

**Returns:** `dict` with keys `tailored_resume_html`, `ats_score`, `missing_keywords`, `strategies_applied`, `changes_summary`.

**Raises:** `RuntimeError` if the response is not valid JSON.

---

### `optimize_until_target()`

```python
def optimize_until_target(
    resume_text: str,
    jd_text: str,
    jd_keywords: dict | None = None,
    target_score: int = 95,
    max_iterations: int = 5,
    primary_color: str = "#2563eb",
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
    on_iteration: Callable[[dict], None] | None = None,
) -> dict
```

Iteratively call the LLM, refining missing keywords with priority-aware prompts, until the ATS score meets the target or max iterations is reached. When `jd_keywords` is provided, runs programmatic verification after each iteration and uses the verified score for best-result selection. Tracks all seen keywords and applied strategies across iterations.

**Callback `on_iteration` receives:**

| Key | Type | Description |
|---|---|---|
| `iteration` | `int` | 1-based iteration number. |
| `ats_score` | `int` | LLM-assessed ATS score for this iteration. |
| `verified_score` | `int` | Programmatic keyword match percentage (same as `ats_score` if `jd_keywords` not available). |
| `missing_keywords` | `list[str]` | Keywords still missing (from LLM response). |
| `improvements` | `list[dict]` | `[{"keyword": str, "resolved": bool}, ...]` — all keywords seen across iterations with resolution status. |
| `strategies` | `list[dict]` | `[{"strategy": str, "applied": bool}, ...]` — all strategies applied across iterations. |
| `verification` | `dict \| None` | Full output of `verify_keyword_coverage()` (or `None` if `jd_keywords` not available). |
| `changes_summary` | `str` | Summary of changes made in this iteration. |

---

### `extract_title_and_company()`

```python
def extract_title_and_company(
    jd_text: str,
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
) -> tuple[str, str]
```

Extract the job title and company name from job description text using a lightweight LLM call (temperature 0).

**Returns:** `(job_title, company)` — defaults to `"UnknownRole"` / `"UnknownCompany"` on parse failure.

---

## `ats_resume_optimizer.resume`

### `extract_resume_text()`

```python
def extract_resume_text(pdf_path: Path) -> str
```

Extract all text from a resume PDF using `pypdf`.

**Raises:** `ValueError` if no text is extracted (e.g., scanned or image-only PDFs).

---

## `ats_resume_optimizer.job_description`

### `fetch_jd_from_url()`

```python
def fetch_jd_from_url(url: str) -> str
```

Fetch a web page (with browser User-Agent header) and extract job description text. Strips `script`, `style`, `nav`, `footer`, `header`, and `noscript` tags before parsing. Tries platform-specific selectors for Greenhouse, Lever, Workday, LinkedIn, Indeed, and generic HTML structures (`<article>`, `.job-description`, `.description`, `<main>`, `<body>`). Returns the first match with 500+ characters. EEO boilerplate paragraphs are stripped from the result.

---

### `get_job_description()`

```python
def get_job_description(
    jd_text: str | None = None,
    jd_url: str | None = None,
) -> str
```

Resolve a job description from raw text or URL. Text input takes precedence.

**Raises:** `ValueError` if neither is provided.

---

## `ats_resume_optimizer.pdf_export`

### `html_to_pdf()`

```python
def html_to_pdf(html: str, output_path: Path) -> None
```

Render a full HTML document to an A4 PDF via headless Chromium. Automatically injects page-break CSS for print safety. Runs Playwright in a subprocess to avoid event-loop conflicts.

**Raises:** `RuntimeError` on subprocess failure (includes stderr output).

---

## `ats_resume_optimizer.config`

| Constant | Value | Description |
|---|---|---|
| `BASE_DIR` | `Path` to project root | Resolved from the module's file path. |
| `RESUME_DIR` | `BASE_DIR / "memory" / "docs"` | Base resume input directory. |
| `OUTPUT_DIR` | `RESUME_DIR / "generated"` | Generated PDF output directory (auto-created). |

---

## `ats_resume_optimizer.utils`

### `sanitize_for_filename()`

```python
def sanitize_for_filename(text: str) -> str
```

Strip a string down to alphanumeric characters, underscores, and hyphens. Returns `"file"` if the result is empty.

### `build_output_path()`

```python
def build_output_path(job_title: str, company: str) -> Path
```

Build the output PDF path: `OUTPUT_DIR / {JobTitle}_{Company}.pdf` (sanitized).

---

## `ats_resume_optimizer.templates`

### Registry

| Name | Type | Description |
|---|---|---|
| `TEMPLATES` | `OrderedDict[str, dict]` | Ordered mapping of template ID → template metadata dict. |

Each template dict contains:

| Key | Type | Description |
|---|---|---|
| `id` | `str` | Template identifier. |
| `name` | `str` | Display name. |
| `description` | `str` | Short description. |
| `render` | `Callable[[str, str], str]` | `(content_html, primary_color) → full HTML`. |

### `get_template()`

```python
def get_template(template_id: str) -> dict
```

Return the template metadata dict for a given ID.

### `get_template_choices()`

```python
def get_template_choices() -> list[tuple[str, str]]
```

Return a list of `(template_id, display_name)` tuples for all registered templates.

### `render_resume()`

```python
def render_resume(template_id: str, content_html: str, primary_color: str) -> str
```

Render content HTML with the specified template and accent color. Returns a full HTML document string.

### `CONTENT_STRUCTURE`

`str` — The semantic HTML structure guide sent to the LLM. Defines the expected class names and element hierarchy that all templates target.

---

## `ats_resume_optimizer.templates._colors`

### `hex_to_rgb()`

```python
def hex_to_rgb(hex_color: str) -> tuple[int, int, int]
```

Convert a hex color string (e.g., `"#2563eb"`) to an `(R, G, B)` tuple.

### `rgb_to_hex()`

```python
def rgb_to_hex(r: int, g: int, b: int) -> str
```

Convert an `(R, G, B)` tuple to a hex color string.

### `lighten()`

```python
def lighten(hex_color: str, factor: float = 0.85) -> str
```

Lighten a hex color by blending toward white. `factor=0.0` returns the original; `factor=1.0` returns white.

### `darken()`

```python
def darken(hex_color: str, factor: float = 0.3) -> str
```

Darken a hex color by scaling toward black. `factor=0.0` returns the original; `factor=1.0` returns black.
