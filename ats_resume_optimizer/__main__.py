"""CLI entry point: python -m ats_resume_optimizer."""

import argparse
from pathlib import Path

from ats_resume_optimizer import run_resume_agent
from ats_resume_optimizer.config import RESUME_DIR


def main() -> None:
    parser = argparse.ArgumentParser(description="AI ATS Resume Optimizer")
    parser.add_argument("--jd-text", type=str, help="Job description text")
    parser.add_argument("--jd-url", type=str, help="Job URL to fetch description from")
    parser.add_argument(
        "--resume",
        type=str,
        default=str(RESUME_DIR / "base_resume.pdf"),
        help="Path to base resume PDF",
    )
    args = parser.parse_args()

    output_pdf = run_resume_agent(
        base_resume_pdf=Path(args.resume),
        jd_text=args.jd_text,
        jd_url=args.jd_url,
        target_score=95,
    )
    print(f"Optimized resume saved to: {output_pdf}")


if __name__ == "__main__":
    main()
