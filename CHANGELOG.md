# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
                                

## [1.3.0] - 2026-02-28

### Added

- **Automatic disk cleanup on session start** — Generated PDFs (`memory/docs/generated/`) and the uploaded resume file (`memory/docs/uploaded_resume.pdf`) are automatically deleted when a new session begins, the page is reloaded, or the Streamlit server restarts. Prevents stale files from accumulating on disk.
- **Disk cleanup on regenerate** — All previously generated PDFs in the output directory are deleted from disk when the user clicks Regenerate, ensuring a clean slate before the new optimization begins.
- **Button loading states** — The Optimize/Regenerate button shows a disabled "⏳ Optimizing…" state during optimization, and the Re-export with Style button shows "⏳ Exporting…" during PDF re-export, providing clear visual feedback.

### Changed

- **Clean UI on regenerate (two-phase rerun)** — Clicking Regenerate now clears all cached session state (including `_opt_content_html`, `_opt_job_title`, `_opt_company`) and triggers `st.rerun()` before starting the optimization. This eliminates Streamlit's stale-element dimming — old iterations, download buttons, and success messages are fully removed before the new optimization renders.
- **Download and re-export buttons hidden during optimization** — The download button and the "Re-export with Style" button are completely hidden (not just disabled) while optimization is in progress.
- **`st.empty()` placeholders for buttons and results** — The optimize, re-export, and results area use `st.empty()` placeholders, allowing immediate visual replacement when the UI state changes.
- **Mutually exclusive result branches** — The optimization, re-export, and persist sections now use `if`/`elif`/`else` flow instead of independent `if` blocks, preventing any overlap between states.

## [1.2.1] - 2026-02-28

### Added

- **In-app help guide** — Added a ❓ button next to the application title that opens a dialog with step-by-step instructions covering API key setup, resume upload, optimization parameters, job description input, theme selection, optimization workflow, PDF download, and re-export.

## [1.2.0] - 2026-02-28

### Added

- **Persistent results across reruns** — Optimization results (status log, PDF download button, and success message) now persist across Streamlit reruns (e.g., after clicking the download button), preventing results from disappearing on page rerun.
- **Session-state status logging** — All pipeline status messages and iteration details are captured in `_opt_status_log` session state and replayed in a collapsed status block when the page reruns.
- **PDF bytes cached in session state** — Generated PDF bytes and filename are stored in `_opt_pdf_bytes` and `_opt_pdf_name`, keeping the download button functional after rerun.

### Changed

- **Simplified resume input** — Removed the "Use default resume" checkbox. Users now always upload a base resume PDF directly through the sidebar file uploader.
- **Unified optimization workflow** — Optimization and PDF generation now run inside a single `st.status` progress block instead of two separate status sections, providing a cleaner progress experience.
- **Re-export button visibility** — The "Re-export with Style" button is now hidden while the optimize button is active, preventing conflicting actions during a run.
- **Re-export uses spinner** — Re-exporting with a new style now shows a simple `st.spinner` instead of a full `st.status` block.
- **Expanded cache invalidation** — Input fingerprint changes now clear additional session keys (`_opt_status_log`, `_opt_pdf_bytes`, `_opt_pdf_name`, `_opt_success_msg`) alongside the existing content/title/company keys.
- **Input fingerprint simplified** — Removed `use_default_resume` flag from the fingerprint hash since the default resume option no longer exists.

### Removed

- **Default resume fallback** — The "Use default resume (memory/docs)" checkbox and the automatic lookup of `memory/docs/base_resume.pdf` have been removed from the web UI. Users must upload their resume PDF each session.

## [1.1.0] - 2026-02-28

### Added

- **Structured JD keyword extraction** — A dedicated LLM call (`extract_jd_keywords()`) now analyzes the job description before optimization, extracting categorized keywords: required hard skills, required soft skills, preferred skills, experience requirements, education, key responsibilities, industry terms, action verbs, and certifications.
- **Programmatic keyword verification** — New `verify_keyword_coverage()` function checks the generated resume HTML against extracted JD keywords after each iteration, producing a deterministic match percentage independent of the LLM's self-assessed score.
- **Must-have vs. preferred prioritization** — Keywords are categorized by priority. Must-have skills are given highest weight in prompts and verification; preferred skills are included only where the candidate has real experience.
- **14 named ATS optimization strategies** tracked across iterations: Job Title Mirroring, Keyword Frequency Optimization, Semantic Skill Clustering, Action Verb Matching, Experience Alignment, Soft Skills Integration, Acronym Expansion, STAR Method Bullets, Must-Have Prioritization, Contextual Keyword Embedding, Skills Ordering by Relevance, Exact Phrase Matching, Quantified Achievements, Date Format Consistency.
- **ATS scoring rubric** — The LLM now follows a defined rubric (40% keyword match, 25% contextual relevance, 15% section completeness, 10% title alignment, 10% experience alignment) instead of producing arbitrary scores.
- **Priority-aware refinement prompts** — Refinement iterations now receive must-have vs. preferred keyword lists, placement guidance (Summary + Skills + Experience for must-haves), warnings for missing job title or experience years, and instructions to preserve previously resolved keywords.
- **Enhanced iteration display** (Web UI and CLI) — Each iteration now shows: LLM score, verified programmatic score, must-have match percentage, applied strategies (with checkmarks), and keywords categorized by priority.
- **Pipeline status callbacks** — `optimize_resume()` and `run_resume_agent()` accept an `on_status` callback for real-time progress reporting (e.g., "Extracting keywords from job description...").
- **Expanded JD URL selectors** — Added selectors for Greenhouse, Lever, Workday, LinkedIn, Indeed, and generic `<main>` elements, plus User-Agent header for more reliable fetching.
- **JD boilerplate cleaning** — EEO statements and legal boilerplate paragraphs are automatically stripped from URL-fetched job descriptions to improve keyword extraction accuracy.

### Changed

- **System prompt rewritten** with research-backed ATS strategies: job title mirroring, keyword frequency across 2-3 sections, exact phrase matching, action verb matching from JD, soft skills integration, semantic skill clustering, skills ordering by relevance, digits for metrics, consistent date formatting, and ATS-safe characters.
- **User prompt restructured** to include a pre-extracted keyword checklist with priority tags, a 10-step optimization task list, and the ATS scoring rubric.
- **Refinement prompt enhanced** with placement guidance per priority level, resolved-keyword preservation, and programmatic verification warnings.
- **LLM temperature lowered** from 0.3 to 0.2 for more deterministic, consistent optimization results.
- **Best-result selection** now uses the programmatic verified score (when available) instead of the LLM's self-assessed score.
- **`build_user_prompt()` signature** updated to accept optional `jd_keywords` parameter.
- **`optimize_until_target()` signature** updated to accept optional `jd_keywords` parameter.
- **`optimize_resume()` return value** now includes `jd_keywords` dict alongside `content_html`, `job_title`, and `company`.
- **Iteration callback data** expanded with `verified_score`, `strategies`, and `verification` fields.
- Increased `@page` left/right margins from 3mm to 14mm (~0.55 in) on 36 standard-layout themes to meet professional resume margin standards (minimum 0.5 in). Four edge-to-edge themes (Sidebar Pro, Gradient Wave, Neon Glass, Aurora Borealis) retain 0 mm side margins by design.
- Updated template authoring example in `docs/templates.md` to reflect new default margins.

## [1.0.0] - 2026-02-27

### Added

- Streamlit web UI with sidebar configuration (API key, target score, max iterations).
- CLI entry point via `python -m ats_resume_optimizer` and `python agent.py`.
- Iterative ATS optimization loop with GPT-4o-mini — refines missing keywords until a target score is reached.
- Job description input via raw text or URL scraping (BeautifulSoup).
- Automatic job title and company extraction from job descriptions using LLM.
- PDF export via headless Chromium (Playwright) in a subprocess worker.
- 37 professionally designed resume themes with customizable accent color.
- Live theme preview dialog with sample resume data.
- Smart input fingerprinting — re-export with a new theme/color without re-running the AI.
- Semantic HTML content structure shared across all templates (`CONTENT_STRUCTURE`).
- Color manipulation utilities (`lighten`, `darken`, `hex_to_rgb`, `rgb_to_hex`).
- Print-safe CSS injection (page-break rules, orphan/widow control).
- Resume PDF text extraction via `pypdf`.
- Sanitized output filenames derived from job title and company.

### Themes

Modern Minimal, Executive Classic, Creative Bold, Tech Professional, Elegant Serif,
Nordic Frost, Midnight Luxe, Swiss Grid, Coral Ribbon, Monograph, Sidebar Pro,
Gradient Wave, Art Deco, Tokyo Metro, Neon Glass, Ivory Press, Blueprint,
Aurora Borealis, Terracotta, Brushstroke, Obsidian Gold, Marble Hall,
Vintage Typewriter, Emerald Dusk, Lavender Haze, Copper Forge, Paper Cut,
Ink Wash, Sahara Dune, Glacier Blue, Crimson Tide, Bamboo Zen, Polaris Star,
Rosewood, Gazette, Slate Mosaic, Vintage Wine, Origami, Carbon Fiber,
Sunset Boulevard.
