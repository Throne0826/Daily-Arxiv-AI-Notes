from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from .config import load_settings
from .pipeline import DailyPipeline, PipelineError, validate_output_tree


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="arxiv-notes",
        description="Fetch, classify, and summarize daily arXiv AI papers.",
    )
    parser.add_argument("--config", default="config.toml", help="Path to config.toml")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="Run the complete daily pipeline")
    run.add_argument(
        "--date",
        default="latest",
        help="Expected arXiv listing date (YYYY-MM-DD) or latest",
    )
    run.add_argument("--max-papers", type=int, default=None, help="Limit selected papers; 0 means all")
    run.add_argument("--metadata-only", action="store_true", help="Do not generate full-text notes")
    run.add_argument("--require-llm", action="store_true", help="Fail unless an LLM endpoint is configured")
    run.add_argument("--force", action="store_true", help="Regenerate already-seen arXiv IDs")
    run.add_argument(
        "--paper-id",
        action="append",
        default=[],
        help="Process only this arXiv ID; repeat to target multiple papers",
    )

    rerender = subparsers.add_parser(
        "rerender",
        help="Rebuild Markdown from cached metadata and generation checkpoints",
    )
    rerender.add_argument(
        "--date",
        action="append",
        default=[],
        help="Cached date to rebuild; repeat for multiple dates, omit for all",
    )

    affiliations = subparsers.add_parser(
        "enrich-affiliations",
        help="Backfill author institutions from arXiv HTML and rerender cached notes",
    )
    affiliations.add_argument(
        "--date",
        action="append",
        required=True,
        help="Cached date to enrich; repeat for multiple dates",
    )

    validate = subparsers.add_parser("validate", help="Validate generated Markdown notes")
    validate.add_argument("--output", default="", help="Override output directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = load_settings(args.config)
    try:
        if args.command == "run":
            requested = None if args.date == "latest" else date.fromisoformat(args.date)
            manifest = DailyPipeline(settings).run(
                requested_date=requested,
                max_papers=args.max_papers,
                metadata_only=args.metadata_only,
                require_llm=args.require_llm,
                force=args.force,
                paper_ids=set(args.paper_id) or None,
            )
            print(json.dumps(manifest, ensure_ascii=False, indent=2))
            return 1 if manifest["failures"] else 0
        if args.command == "rerender":
            result = DailyPipeline(settings).rerender(args.date or None)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1 if result["failures"] else 0
        if args.command == "enrich-affiliations":
            result = DailyPipeline(settings).enrich_affiliations(args.date)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1 if result["failures"] else 0
        output = Path(args.output).resolve() if args.output else settings.project_path("output_dir")
        issues = validate_output_tree(output)
        print(json.dumps(issues, ensure_ascii=False, indent=2))
        return 1 if issues else 0
    except (PipelineError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
