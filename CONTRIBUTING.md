# Contributing

Thank you for your interest in contributing to ATS Resume Optimizer. This guide will help you get started.

## Development Setup

1. **Fork and clone** the repository.

2. **Create a virtual environment and install dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   playwright install chromium
   ```

3. **Create a `.env` file** in the project root:

   ```
   OPENAI_API_KEY=sk-...
   ```

4. **Run the Streamlit app** to verify everything works:

   ```bash
   streamlit run app.py
   ```

## Project Structure

```
ats_resume_optimizer/
├── agent.py              Orchestration pipeline (keyword extraction + optimization + export)
├── config.py             Path constants
├── job_description.py    JD fetching (URL / text), boilerplate cleaning
├── llm.py                OpenAI prompts, JD keyword extraction, keyword verification,
│                          ATS scoring rubric, strategy tracking, optimization loop
├── pdf_export.py         HTML → PDF via Playwright
├── _pdf_worker.py        Subprocess Playwright worker
├── resume.py             PDF text extraction
├── utils.py              Filename helpers
└── templates/
    ├── __init__.py        Registry, render API, CONTENT_STRUCTURE
    ├── _colors.py         Color utilities
    └── *.py               Individual theme modules
```

## Making Changes

### Branch Naming

Use descriptive branch names:

- `feature/theme-name` — new template
- `fix/pdf-export-issue` — bug fix
- `docs/update-readme` — documentation
- `refactor/llm-prompts` — code refactoring

### Code Style

- Python 3.12+ syntax (union types with `|`, etc.).
- Use type hints on all public function signatures.
- Keep modules focused — one responsibility per file.
- Write docstrings for all public functions and modules.
- No unused imports; no wildcard imports.

### Commit Messages

Write clear, concise commit messages:

```
Add Origami resume theme

Fix PDF export failing on Windows with long paths

Update LLM system prompt to improve keyword coverage
```

## Adding a New Template

See the [Template Authoring Guide](docs/templates.md) for step-by-step instructions.

**Quick summary:**

1. Create `ats_resume_optimizer/templates/your_theme.py`.
2. Export a `TEMPLATE` dict with `id`, `name`, `description`.
3. Implement `_render(content_html, primary_color) -> str` returning a full HTML document.
4. Assign `TEMPLATE["render"] = _render`.
5. Register it in `templates/__init__.py` (import + add to `TEMPLATES` OrderedDict).

## Modifying LLM Prompts

The system prompt, user prompt, refinement prompt, and ATS scoring rubric live in `ats_resume_optimizer/llm.py`. When modifying prompts:

- Test with at least 3 different job descriptions across different industries.
- Verify the output JSON structure remains valid (must include `tailored_resume_html`, `ats_score`, `missing_keywords`, `strategies_applied`, `changes_summary`).
- Ensure ATS scores remain reasonable and the model does not hallucinate experience.
- Verify that `strategies_applied` values match the names defined in `ATS_STRATEGIES`.
- Check that programmatic verification (`verify_keyword_coverage()`) aligns with the LLM's self-assessed score — large discrepancies indicate prompt issues.
- Ensure the refinement prompt preserves previously resolved keywords and respects must-have vs. preferred priority.
- If adding new strategies, update the `ATS_STRATEGIES` list, `_STRATEGIES_LIST` prompt fragment, and the strategies table in `docs/architecture.md`.

## Reporting Issues

When opening an issue, please include:

- Python version (`python --version`).
- OS and version.
- Steps to reproduce the problem.
- Full error traceback (if applicable).
- The job description or URL used (if relevant and non-confidential).

## Pull Requests

1. Keep PRs focused on a single change.
2. Update documentation if your change affects usage or configuration.
3. Ensure the app runs without errors via both the CLI and Streamlit UI.
4. Add a `CHANGELOG.md` entry under an `[Unreleased]` section.
