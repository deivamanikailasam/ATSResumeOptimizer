# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
                                

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
