import copy
import json
import threading
import time
from datetime import date

import pytest

from daily_arxiv_notes.config import Settings, load_settings
from daily_arxiv_notes.models import Classification, FullText, GeneratedNote, Paper
from daily_arxiv_notes.pipeline import DailyPipeline, PipelineError, validate_output_tree


class FakeArxivClient:
    def fetch_daily_listings(self, categories, requested_date=None):
        return date(2026, 7, 29), {"2607.99991": object()}

    def fetch_metadata(self, listings, announcement_date):
        return [
            Paper(
                arxiv_id="2607.99991",
                title="Process Reward Models for Chain-of-Thought Reasoning",
                abstract="We study process reward models and GRPO for mathematical reasoning.",
                authors=["Alice Example"],
                announcement_date=announcement_date.isoformat(),
                arxiv_url="https://arxiv.org/abs/2607.99991",
                pdf_url="https://arxiv.org/pdf/2607.99991",
            )
        ]


def test_metadata_pipeline_is_idempotent(tmp_path) -> None:
    base = load_settings("config.toml")
    settings = Settings(root=tmp_path, raw=copy.deepcopy(base.raw), taxonomy=base.taxonomy)
    pipeline = DailyPipeline(settings)
    pipeline.arxiv = FakeArxivClient()

    first = pipeline.run(metadata_only=True)
    second = pipeline.run(metadata_only=True)

    assert first["generated"] == 1
    assert second["generated"] == 0
    assert not validate_output_tree(settings.project_path("output_dir"))
    daily_index = settings.project_path("output_dir") / "2026-07-29" / "index.md"
    assert "Process Reward Models" in daily_index.read_text(encoding="utf-8")
    category_index = settings.project_path("category_index_dir") / "llm_reasoning" / "index.md"
    review_index = settings.project_path("review_index_file")
    assert "Process Reward Models" in category_index.read_text(encoding="utf-8")
    assert "2607.99991" in review_index.read_text(encoding="utf-8")


def test_full_run_requires_a_configured_llm(tmp_path, monkeypatch) -> None:
    base = load_settings("config.toml")
    for name in ("OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL"):
        monkeypatch.delenv(name, raising=False)
    settings = Settings(root=tmp_path, raw=copy.deepcopy(base.raw), taxonomy=base.taxonomy)
    pipeline = DailyPipeline(settings)
    pipeline.arxiv = FakeArxivClient()

    with pytest.raises(PipelineError, match="Full-text note generation requires"):
        pipeline.run()


def test_metadata_only_entry_is_upgraded_when_llm_becomes_available() -> None:
    seen = {"2607.99991": {"review_status": "metadata_only"}}

    assert not DailyPipeline._needs_processing(
        "2607.99991",
        seen,
        force=False,
        metadata_only=True,
        llm_available=False,
    )
    assert DailyPipeline._needs_processing(
        "2607.99991",
        seen,
        force=False,
        metadata_only=False,
        llm_available=True,
    )


def test_regeneration_removes_stale_category_path(tmp_path) -> None:
    output_dir = tmp_path / "docs" / "arxiv_daily"
    stale = output_dir / "2026-07-29" / "llm_nlp" / "paper.md"
    stale.parent.mkdir(parents=True)
    stale.write_text("old", encoding="utf-8")

    DailyPipeline._remove_stale_note(
        output_dir,
        "2026-07-29/llm_nlp/paper.md",
        "2026-07-29/llm_agent/paper.md",
    )

    assert not stale.exists()


def test_targeted_regeneration_can_reuse_stored_classification(tmp_path) -> None:
    base = load_settings("config.toml")
    settings = Settings(root=tmp_path, raw=copy.deepcopy(base.raw), taxonomy=base.taxonomy)
    pipeline = DailyPipeline(settings)
    stored = {
        "primary_category": "llm_agent",
        "categories": ["llm_agent", "reinforcement_learning"],
        "classification_confidence": 0.94,
    }
    classification = pipeline._classification_from_state(stored)

    assert classification is not None
    assert classification.source == "state"
    assert classification.primary_category == "llm_agent"
    assert classification.categories == ["llm_agent", "reinforcement_learning"]


def test_target_category_filter_excludes_unmatched_classification() -> None:
    classification = Classification(
        relevant=True,
        primary_category="llm_agent",
        categories=["llm_agent"],
    )

    assert not DailyPipeline._matches_target_categories(
        classification,
        {"llm_reasoning"},
    )


def test_target_category_filter_accepts_matching_secondary_label() -> None:
    classification = Classification(
        relevant=True,
        primary_category="llm_alignment",
        categories=["llm_alignment", "llm_reasoning"],
    )

    assert DailyPipeline._matches_target_categories(
        classification,
        {"llm_reasoning"},
    )


def test_empty_target_category_filter_preserves_relevant_papers() -> None:
    classification = Classification(
        relevant=True,
        primary_category="llm_agent",
        categories=["llm_agent"],
    )

    assert DailyPipeline._matches_target_categories(classification, set())


def test_daily_run_reuses_cached_classification(tmp_path, monkeypatch) -> None:
    base = load_settings("config.toml")
    settings = Settings(root=tmp_path, raw=copy.deepcopy(base.raw), taxonomy=base.taxonomy)
    raw_dir = tmp_path / "data" / "raw" / "2026-07-29"
    raw_dir.mkdir(parents=True)
    paper = Paper(
        arxiv_id="2607.99991",
        title="Cached Agent Reasoning Paper",
        abstract="An agent reasoning paper.",
        announcement_date="2026-07-29",
    )
    (raw_dir / "papers.json").write_text(
        json.dumps([paper.to_dict()]),
        encoding="utf-8",
    )
    (raw_dir / "classifications.json").write_text(
        json.dumps(
            {
                paper.arxiv_id: {
                    "relevant": True,
                    "primary_category": "llm_agent",
                    "categories": ["llm_agent", "llm_reasoning"],
                    "confidence": 0.91,
                    "reason": "cached result",
                    "source": "hybrid",
                    "rule_scores": {},
                }
            }
        ),
        encoding="utf-8",
    )
    pipeline = DailyPipeline(settings)

    class NoNetworkArxiv:
        def fetch_daily_listings(self, *args, **kwargs):
            raise AssertionError("an explicitly dated run must reuse its papers cache")

    pipeline.arxiv = NoNetworkArxiv()

    def fail_if_classified(papers):
        raise AssertionError("valid cached classifications must skip the LLM classifier")

    monkeypatch.setattr(pipeline, "_classify", fail_if_classified)
    manifest = pipeline.run(requested_date=date(2026, 7, 29), metadata_only=True)

    assert manifest["generated"] == 1
    assert manifest["relevant_total"] == 1
    assert manifest["selected"] == 1


def test_targeted_run_preserves_other_cached_classifications(tmp_path) -> None:
    base = load_settings("config.toml")
    raw = copy.deepcopy(base.raw)
    raw["generation"]["target_categories"] = []
    settings = Settings(root=tmp_path, raw=raw, taxonomy=base.taxonomy)
    raw_dir = tmp_path / "data" / "raw" / "2026-07-29"
    raw_dir.mkdir(parents=True)
    papers = [
        Paper(
            arxiv_id=arxiv_id,
            title=f"Cached paper {arxiv_id}",
            abstract="Agent reasoning and reinforcement learning.",
            announcement_date="2026-07-29",
        )
        for arxiv_id in ("2607.99991", "2607.99992")
    ]
    (raw_dir / "papers.json").write_text(
        json.dumps([paper.to_dict() for paper in papers]),
        encoding="utf-8",
    )
    preserved = {
        "relevant": False,
        "primary_category": "",
        "categories": [],
        "confidence": 0.8,
        "reason": "cached exclusion",
        "source": "hybrid",
        "rule_scores": {},
    }
    (raw_dir / "classifications.json").write_text(
        json.dumps({"2607.99992": preserved}),
        encoding="utf-8",
    )
    (raw_dir / "manifest.json").write_text(
        json.dumps(
            {
                "announcement_date": "2026-07-29",
                "fetched_unique": 137,
                "new_candidates": 132,
                "relevant_total": 101,
                "selected": 5,
                "generated": 4,
                "metadata_only": False,
                "llm_model": "test",
                "classification_errors": [],
                "failures": [{"arxiv_id": "2607.99991", "error": "temporary"}],
            }
        ),
        encoding="utf-8",
    )
    pipeline = DailyPipeline(settings)
    pipeline.arxiv = FakeArxivClient()

    manifest = pipeline.run(
        requested_date=date(2026, 7, 29),
        metadata_only=True,
        force=True,
        paper_ids={"2607.99991"},
    )
    cached = json.loads((raw_dir / "classifications.json").read_text(encoding="utf-8"))

    assert manifest["generated"] == 5
    assert cached["2607.99992"] == preserved
    assert "2607.99991" in cached
    daily_manifest = json.loads((raw_dir / "manifest.json").read_text(encoding="utf-8"))
    assert daily_manifest["new_candidates"] == 132
    assert daily_manifest["relevant_total"] == 101
    assert daily_manifest["generated"] == 5
    assert daily_manifest["failures"] == []


def test_targeted_historical_regeneration_uses_cached_metadata(tmp_path) -> None:
    base = load_settings("config.toml")
    settings = Settings(root=tmp_path, raw=copy.deepcopy(base.raw), taxonomy=base.taxonomy)
    cached = tmp_path / "data" / "raw" / "2026-07-29" / "papers.json"
    cached.parent.mkdir(parents=True)
    cached.write_text(
        json.dumps(
            [
                Paper(
                    arxiv_id="2607.99991",
                    title="Cached Chain-of-Thought Reasoning Paper",
                    abstract="A cached process reward model for mathematical reasoning.",
                    announcement_date="2026-07-29",
                ).to_dict()
            ]
        ),
        encoding="utf-8",
    )
    pipeline = DailyPipeline(settings)

    class NoNetworkArxiv:
        def fetch_daily_listings(self, *args, **kwargs):
            raise AssertionError("historical cached regeneration must not fetch the latest listing")

    pipeline.arxiv = NoNetworkArxiv()
    manifest = pipeline.run(
        requested_date=date(2026, 7, 29),
        metadata_only=True,
        force=True,
        paper_ids={"2607.99991"},
    )

    assert manifest["announcement_date"] == "2026-07-29"
    assert manifest["generated"] == 1


def test_table_evidence_allows_column_labels_but_rejects_wrong_number() -> None:
    source = (
        "Standard Pipeline 1 -> 2 -> 3 ID 73.68 OOD 61.39 Avg 69.58 "
        "Other row 70.00 60.00 66.00"
    )
    note = GeneratedNote(
        content={
            "experiments": {
                "main_results": [],
                "ablations": [
                    {
                        "evidence_quote": "Standard Pipeline 1 → 2 → 3 73.68 61.39 69.58"
                    }
                ],
            }
        },
        generator_model="test",
        review_status="ai_draft",
        source_sha256="a" * 64,
    )

    assert not DailyPipeline._validate_evidence_quotes(note, source)

    note.content["experiments"]["ablations"][0]["evidence_quote"] = (
        "Standard Pipeline 1 → 2 → 3 73.68 61.39 99.99"
    )
    assert DailyPipeline._validate_evidence_quotes(note, source) == [
        "ablations[0] evidence quote not found in source"
    ]


def test_latexml_duplicate_numbers_match_but_truncated_sentence_does_not() -> None:
    source = (
        "we find a substantial overlap, with 17.55 17.55 % ( 719 719 ) of the "
        "activation vector shared across all."
    )
    note = GeneratedNote(
        content={
            "experiments": {
                "main_results": [
                    {
                        "evidence_quote": (
                            "we find a substantial overlap, with 17.55% (719) of the "
                            "activation vector shared across all."
                        )
                    }
                ],
                "ablations": [],
            }
        },
        generator_model="test",
        review_status="ai_draft",
        source_sha256="a" * 64,
    )

    assert not DailyPipeline._validate_evidence_quotes(note, source)

    note.content["experiments"]["main_results"][0]["evidence_quote"] = (
        "there is no overlap between Ethics and Personality, and"
    )
    assert DailyPipeline._validate_evidence_quotes(note, source) == [
        "main_results[0] evidence quote not found in source"
    ]


def test_generation_workers_run_concurrently_and_keep_daily_total(
    tmp_path,
    monkeypatch,
) -> None:
    base = load_settings("config.toml")
    raw = copy.deepcopy(base.raw)
    raw["generation"]["workers"] = 3
    raw["generation"]["target_categories"] = []
    settings = Settings(root=tmp_path, raw=raw, taxonomy=base.taxonomy)
    raw_dir = tmp_path / "data" / "raw" / "2026-07-30"
    raw_dir.mkdir(parents=True)
    papers = [
        Paper(
            arxiv_id=f"2607.9000{index}",
            title=f"Concurrent paper {index}",
            abstract="Agent reasoning and reinforcement learning.",
            announcement_date="2026-07-30",
        )
        for index in range(3)
    ]
    (raw_dir / "papers.json").write_text(
        json.dumps([paper.to_dict() for paper in papers]),
        encoding="utf-8",
    )
    (raw_dir / "classifications.json").write_text(
        json.dumps(
            {
                paper.arxiv_id: Classification(
                    relevant=True,
                    primary_category="llm_agent",
                    categories=["llm_agent"],
                    confidence=0.9,
                    source="cache",
                ).to_dict()
                for paper in papers
            }
        ),
        encoding="utf-8",
    )
    state_path = tmp_path / "data" / "state.json"
    state_path.write_text(
        json.dumps(
            {
                "version": 1,
                "seen": {
                    "2607.89999": {
                        "announcement_date": "2026-07-30",
                        "path": "2026-07-30/llm_agent/already-generated.md",
                        "review_status": "ai_draft",
                        "title": "Already generated",
                        "primary_category": "llm_agent",
                        "categories": ["llm_agent"],
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    pipeline = DailyPipeline(settings)
    pipeline.llm = type("FakeLlm", (), {"available": True, "model": "test"})()

    class FullTextArxiv:
        def fetch_full_text(self, paper, max_chars):
            return FullText(text=f"full text {paper.arxiv_id}", source="test")

    pipeline.arxiv = FullTextArxiv()
    lock = threading.Lock()
    active = 0
    max_active = 0

    def fake_prepare(paper, classification, raw_dir, *, metadata_only, full_text):
        nonlocal active, max_active
        with lock:
            active += 1
            max_active = max(max_active, active)
        time.sleep(0.05)
        with lock:
            active -= 1
        return {
            "arxiv_id": paper.arxiv_id,
            "paper": paper,
            "classification": classification,
            "path": f"llm_agent/{paper.arxiv_id}.md",
            "summary": "summary",
            "review_status": "ai_draft",
            "issues": [],
            "markdown": f"# {paper.title}\n",
        }

    monkeypatch.setattr(pipeline, "_prepare_note", fake_prepare)
    manifest = pipeline.run(requested_date=date(2026, 7, 30))

    assert max_active >= 2
    assert manifest["generated"] == 3
    assert manifest["generated_this_run"] == 3
    assert manifest["daily_total"] == 4
    assert not manifest["failures"]


def test_worker_failure_does_not_stop_other_papers(tmp_path, monkeypatch) -> None:
    base = load_settings("config.toml")
    raw = copy.deepcopy(base.raw)
    raw["generation"]["workers"] = 2
    raw["generation"]["target_categories"] = []
    settings = Settings(root=tmp_path, raw=raw, taxonomy=base.taxonomy)
    raw_dir = tmp_path / "data" / "raw" / "2026-07-30"
    raw_dir.mkdir(parents=True)
    papers = [
        Paper(
            arxiv_id=f"2607.9100{index}",
            title=f"Failure isolation paper {index}",
            announcement_date="2026-07-30",
        )
        for index in range(2)
    ]
    (raw_dir / "papers.json").write_text(
        json.dumps([paper.to_dict() for paper in papers]),
        encoding="utf-8",
    )
    (raw_dir / "classifications.json").write_text(
        json.dumps(
            {
                paper.arxiv_id: Classification(
                    relevant=True,
                    primary_category="llm_agent",
                    categories=["llm_agent"],
                    confidence=0.9,
                ).to_dict()
                for paper in papers
            }
        ),
        encoding="utf-8",
    )
    pipeline = DailyPipeline(settings)
    pipeline.llm = type("FakeLlm", (), {"available": True, "model": "test"})()

    class FullTextArxiv:
        def fetch_full_text(self, paper, max_chars):
            return FullText(text="full text", source="test")

    pipeline.arxiv = FullTextArxiv()

    def fake_prepare(paper, classification, raw_dir, *, metadata_only, full_text):
        if paper.arxiv_id.endswith("0"):
            raise RuntimeError("expected worker failure")
        return {
            "arxiv_id": paper.arxiv_id,
            "paper": paper,
            "classification": classification,
            "path": f"llm_agent/{paper.arxiv_id}.md",
            "summary": "summary",
            "review_status": "ai_draft",
            "issues": [],
            "markdown": f"# {paper.title}\n",
        }

    monkeypatch.setattr(pipeline, "_prepare_note", fake_prepare)
    manifest = pipeline.run(requested_date=date(2026, 7, 30))

    assert manifest["generated"] == 1
    assert manifest["daily_total"] == 1
    assert manifest["failures"] == [
        {"arxiv_id": "2607.91000", "error": "expected worker failure"}
    ]
