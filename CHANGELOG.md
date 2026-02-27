# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
