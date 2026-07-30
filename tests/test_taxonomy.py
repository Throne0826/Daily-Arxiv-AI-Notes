import json
from pathlib import Path

from daily_arxiv_notes.models import Paper
from daily_arxiv_notes.taxonomy import RuleClassifier, Taxonomy


ROOT = Path(__file__).resolve().parents[1]


def load_taxonomy() -> Taxonomy:
    return Taxonomy(json.loads((ROOT / "taxonomy.json").read_text(encoding="utf-8")))


def test_reasoning_alignment_multilabel() -> None:
    paper = Paper(
        arxiv_id="2607.00001",
        title="Process Reward Models for Chain-of-Thought Reasoning",
        abstract="We use GRPO and reinforcement fine-tuning for mathematical reasoning.",
    )
    result = RuleClassifier(load_taxonomy(), minimum_score=2).classify(paper)

    assert result.relevant
    assert "llm_reasoning" in result.categories
    assert "llm_alignment" in result.categories


def test_unrelated_paper_is_rejected() -> None:
    paper = Paper(
        arxiv_id="2607.00002",
        title="A New Measurement of Coastal Sediment",
        abstract="We report field measurements from three beaches.",
    )
    result = RuleClassifier(load_taxonomy(), minimum_score=2).classify(paper)
    assert not result.relevant
