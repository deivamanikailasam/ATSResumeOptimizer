"""Subprocess worker for Playwright PDF generation.

Invoked as a separate process to avoid event-loop conflicts with Streamlit.
Usage: python _pdf_worker.py <html_file> <output_pdf>
"""

import sys

from playwright.sync_api import sync_playwright


def main() -> None:
    html_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until="networkidle")
        page.pdf(
            path=output_path,
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
        )
        browser.close()


if __name__ == "__main__":
    main()
