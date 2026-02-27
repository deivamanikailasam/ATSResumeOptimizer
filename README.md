# ATS Resume Optimizer

An AI-powered resume optimization tool that tailors your resume to specific job descriptions, maximizing Applicant Tracking System (ATS) compatibility. Built with OpenAI GPT-4o-mini, Streamlit, and Playwright.

## Documentation

| Document | Description |
|---|---|
| [Architecture](docs/architecture.md) | System design, module responsibilities, and data flow diagrams |
| [API Reference](docs/api-reference.md) | Complete reference for all public functions and constants |
| [Template Guide](docs/templates.md) | How the template system works and how to author new themes |
| [Configuration](docs/configuration.md) | Environment variables, paths, CLI arguments, and all settings |
| [Deployment](docs/deployment.md) | Local setup, Docker, Streamlit Cloud, and production considerations |
| [Contributing](CONTRIBUTING.md) | Development setup, code style, and contribution workflow |
| [Changelog](CHANGELOG.md) | Version history and release notes |

## Features

- **AI-Driven Optimization** — Uses GPT-4o-mini to rewrite and tailor resume content to match job description keywords, phrasing, and requirements.
- **Iterative Refinement** — Runs up to N optimization passes, tracking missing keywords and ATS score improvements until a target score is reached.
- **37 Premium Themes** — Choose from a curated collection of professionally designed resume templates (Modern Minimal, Executive Classic, Neon Glass, Aurora Borealis, and more).
- **Customizable Accent Color** — Pick any accent color; templates dynamically adapt their palette.
- **Live Theme Preview** — Preview any theme with sample data before committing.
- **PDF Export** — Generates print-ready A4 PDFs via headless Chromium (Playwright).
- **Dual Interface** — Use the Streamlit web UI for an interactive experience, or the CLI for scripting and automation.
- **Job URL Scraping** — Paste a job listing URL and the tool fetches and parses the description automatically.
- **Smart Caching** — Change theme or color without re-running the AI; re-export instantly from cached results.

## Architecture

```
app.py                              Streamlit web UI
agent.py                            CLI wrapper
ats_resume_optimizer/
├── __init__.py                     Package exports
├── __main__.py                     CLI entry point (argparse)
├── agent.py                        Orchestration pipeline
├── config.py                       Paths and directories
├── job_description.py              JD fetching (URL / text)
├── llm.py                          OpenAI prompts and iterative optimization
├── pdf_export.py                   HTML → PDF via Playwright subprocess
├── _pdf_worker.py                  Subprocess Playwright worker
├── resume.py                       PDF text extraction (pypdf)
├── utils.py                        Filename / path helpers
└── templates/
    ├── __init__.py                 Template registry, render API, content structure
    ├── _colors.py                  Color manipulation utilities
    ├── modern_minimal.py           Theme: Modern Minimal
    ├── executive_classic.py        Theme: Executive Classic
    ├── ...                         35 more themes
    └── sunset_boulevard.py         Theme: Sunset Boulevard
```

### Pipeline

```
Resume PDF ──► Text Extraction (pypdf)
                        │
Job Description ──► URL scraping (requests + BeautifulSoup) or raw text
                        │
                        ▼
              LLM Optimization Loop
              (GPT-4o-mini, up to N iterations)
                        │
                  ┌─────┴─────┐
                  │  Score ≥   │── yes ──► Best Result
                  │  Target?   │
                  └─────┬─────┘
                        │ no
                  Refine missing
                  keywords & retry
                        │
                        ▼
              Render HTML with Theme + Color
                        │
                        ▼
              Export to PDF (Playwright / Chromium)
```

## Prerequisites

- **Python 3.12+**
- **OpenAI API key** — requires access to `gpt-4o-mini` (or another chat model)
- **Chromium for Playwright** — installed via `playwright install chromium`

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/ATSResumeOptimizer.git
   cd ATSResumeOptimizer
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install the Playwright browser**

   ```bash
   playwright install chromium
   ```

5. **Configure your API key**

   Create a `.env` file in the project root:

   ```
   OPENAI_API_KEY=sk-...
   ```

   Alternatively, enter the key directly in the Streamlit sidebar at runtime.

6. **Place your base resume** (optional)

   Copy your resume PDF to `memory/docs/base_resume.pdf` for use as the default input. You can also upload a resume through the web UI.

## Usage

### Web UI (Streamlit)

```bash
streamlit run app.py
```

This launches a local web app where you can:

1. Enter or paste a job description (or provide a job listing URL).
2. Select a theme and accent color, with live preview.
3. Click **Optimize Resume** to run the AI pipeline.
4. Download the generated PDF.

### Command Line

```bash
python -m ats_resume_optimizer \
  --jd-text "Paste the full job description here..." \
  --resume memory/docs/base_resume.pdf \
  --target-score 95 \
  --max-iterations 5 \
  --template modern_minimal \
  --color "#2563eb"
```

You can also fetch a job description from a URL:

```bash
python -m ats_resume_optimizer \
  --jd-url "https://example.com/job-posting" \
  --template executive_classic
```

#### CLI Arguments

| Argument | Default | Description |
|---|---|---|
| `--jd-text` | — | Job description text |
| `--jd-url` | — | URL to scrape job description from |
| `--resume` | `memory/docs/base_resume.pdf` | Path to your base resume PDF |
| `--target-score` | `95` | Target ATS score (70–100) |
| `--max-iterations` | `5` | Max optimization iterations (1–10) |
| `--template` | `modern_minimal` | Resume theme template ID |
| `--color` | `#2563eb` | Accent color (hex) |

## Available Themes

<details>
<summary>View all 37 themes</summary>

| # | Theme ID | Name |
|---|---|---|
| 1 | `modern_minimal` | Modern Minimal |
| 2 | `executive_classic` | Executive Classic |
| 3 | `creative_bold` | Creative Bold |
| 4 | `tech_professional` | Tech Professional |
| 5 | `elegant_serif` | Elegant Serif |
| 6 | `nordic_frost` | Nordic Frost |
| 7 | `midnight_luxe` | Midnight Luxe |
| 8 | `swiss_grid` | Swiss Grid |
| 9 | `coral_ribbon` | Coral Ribbon |
| 10 | `monograph` | Monograph |
| 11 | `sidebar_pro` | Sidebar Pro |
| 12 | `gradient_wave` | Gradient Wave |
| 13 | `art_deco` | Art Deco |
| 14 | `tokyo_metro` | Tokyo Metro |
| 15 | `neon_glass` | Neon Glass |
| 16 | `ivory_press` | Ivory Press |
| 17 | `blueprint` | Blueprint |
| 18 | `aurora_borealis` | Aurora Borealis |
| 19 | `terracotta` | Terracotta |
| 20 | `brushstroke` | Brushstroke |
| 21 | `obsidian_gold` | Obsidian Gold |
| 22 | `marble_hall` | Marble Hall |
| 23 | `vintage_typewriter` | Vintage Typewriter |
| 24 | `emerald_dusk` | Emerald Dusk |
| 25 | `lavender_haze` | Lavender Haze |
| 26 | `copper_forge` | Copper Forge |
| 27 | `paper_cut` | Paper Cut |
| 28 | `ink_wash` | Ink Wash |
| 29 | `sahara_dune` | Sahara Dune |
| 30 | `glacier_blue` | Glacier Blue |
| 31 | `crimson_tide` | Crimson Tide |
| 32 | `bamboo_zen` | Bamboo Zen |
| 33 | `polaris_star` | Polaris Star |
| 34 | `rosewood` | Rosewood |
| 35 | `gazette` | Gazette |
| 36 | `slate_mosaic` | Slate Mosaic |
| 37 | `vintage_wine` | Vintage Wine |
| 38 | `origami` | Origami |
| 39 | `carbon_fiber` | Carbon Fiber |
| 40 | `sunset_boulevard` | Sunset Boulevard |

</details>

## Configuration

| Variable | Source | Description |
|---|---|---|
| `OPENAI_API_KEY` | `.env` or Streamlit sidebar | Required. Your OpenAI API key. |

All file paths are configured in `ats_resume_optimizer/config.py`:

- **Base resume directory** — `memory/docs/`
- **Generated PDFs** — `memory/docs/generated/`

## How It Works

1. **Text Extraction** — The base resume PDF is read with `pypdf` and its text content is extracted.
2. **Job Description Parsing** — If a URL is provided, the page is fetched with `requests` and parsed with BeautifulSoup to extract the job description text. Direct text input is used as-is.
3. **Title & Company Extraction** — A lightweight LLM call extracts the job title and company name from the job description for use in the output filename.
4. **Iterative ATS Optimization** — The resume text and job description are sent to GPT-4o-mini with a specialized system prompt. The model returns:
   - Tailored resume HTML (using semantic class names matching the template system)
   - An estimated ATS score (0–100)
   - A list of missing/weak keywords
   - A summary of changes made

   If the score is below the target, the missing keywords are fed back for refinement. This loop repeats until the score meets the target or max iterations is reached.
5. **Template Rendering** — The optimized HTML content is wrapped in a full HTML document by the selected theme, which applies its CSS, typography, and layout.
6. **PDF Generation** — The final HTML is rendered to an A4 PDF using Playwright's Chromium engine in a subprocess (to avoid event-loop conflicts with Streamlit).

## Project Structure Details

### Templates

Each template is a standalone Python module that exports:

- `TEMPLATE` dict with `id`, `name`, `description`, and `render` function
- `_render(content_html, primary_color) -> str` — returns a complete HTML document

All templates target the same set of semantic CSS class names (`.resume-header`, `.resume-section`, `.experience-item`, `.skill-tag`, etc.), defined in `CONTENT_STRUCTURE`. This decouples the AI-generated content from the visual presentation.

### Color Utilities

`templates/_colors.py` provides `hex_to_rgb`, `rgb_to_hex`, `lighten`, and `darken` functions used by templates to derive color variants from the user-selected accent color.

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `openai` | 2.24.0 | OpenAI API client |
| `python-dotenv` | 1.2.1 | Load `.env` variables |
| `pypdf` | 6.7.3 | Extract text from resume PDFs |
| `beautifulsoup4` | 4.14.3 | Parse job description HTML |
| `requests` | 2.32.5 | HTTP requests for job URL scraping |
| `streamlit` | latest | Web UI framework |
| `playwright` | latest | Headless Chromium for PDF export |

## Versioning

This project uses [Semantic Versioning](https://semver.org/). The current version is defined in the [`VERSION`](VERSION) file and accessible programmatically:

```python
from ats_resume_optimizer import __version__
```

See the [Changelog](CHANGELOG.md) for release history.

## License

This project is provided as-is for personal use. See [LICENSE](LICENSE) if a license file is present.
