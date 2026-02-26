"""CLI entry point: python -m ats_resume_optimizer."""

import argparse
from pathlib import Path

from ats_resume_optimizer import run_resume_agent
from ats_resume_optimizer.config import RESUME_DIR
from ats_resume_optimizer.templates import get_template_choices


def _print_iteration(data: dict) -> None:
    i = data["iteration"]
    score = data["ats_score"]
    improvements = data["improvements"]

    resolved = [f"[+] {imp['keyword']}" for imp in improvements if imp["resolved"]]
    pending = [imp["keyword"] for imp in improvements if not imp["resolved"]]

    parts = [f"Iteration {i} | Score: {score}/100"]
    if resolved:
        parts.append("  ".join(resolved))
    if pending:
        parts.append(f"Missing: {', '.join(pending)}")

    print(" | ".join(parts))


def main() -> None:
    template_ids = [t[0] for t in get_template_choices()]

    parser = argparse.ArgumentParser(description="AI ATS Resume Optimizer")
    parser.add_argument("--jd-text", type=str, help="Job description text")
    parser.add_argument("--jd-url", type=str, help="Job URL to fetch description from")
    parser.add_argument(
        "--resume",
        type=str,
        default=str(RESUME_DIR / "base_resume.pdf"),
        help="Path to base resume PDF",
    )
    parser.add_argument(
        "--target-score", type=int, default=95, help="Target ATS score (default: 95)"
    )
    parser.add_argument(
        "--max-iterations", type=int, default=5, help="Max optimization iterations (default: 5)"
    )
    parser.add_argument(
        "--template",
        type=str,
        default="modern_minimal",
        choices=template_ids,
        help="Resume theme template (default: modern_minimal)",
    )
    parser.add_argument(
        "--color", type=str, default="#2563eb", help="Accent color hex (default: #2563eb)"
    )
    args = parser.parse_args()

    output_pdf = run_resume_agent(
        base_resume_pdf=Path(args.resume),
        jd_text=args.jd_text,
        jd_url=args.jd_url,
        target_score=args.target_score,
        max_iterations=args.max_iterations,
        template_id=args.template,
        primary_color=args.color,
        on_iteration=_print_iteration,
    )
    print(f"\nOptimized resume saved to: {output_pdf}")


if __name__ == "__main__":
    main()
