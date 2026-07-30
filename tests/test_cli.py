from daily_arxiv_notes.cli import build_parser


def test_repeated_paper_id_targets_specific_papers() -> None:
    args = build_parser().parse_args(
        [
            "run",
            "--paper-id",
            "2502.02061",
            "--paper-id",
            "2508.00344",
        ]
    )

    assert args.paper_id == ["2502.02061", "2508.00344"]
