import json

from daily_arxiv_notes.llm import (
    NoteGenerator,
    _chat_completions_url,
    _extract_stream_content,
    _relevant_excerpt,
)
from daily_arxiv_notes.models import FullText, Paper


STRUCTURED_SOURCE = """PilotRL title and authors
[SECTION level=6] Abstract
Abstract body.
[SECTION level=2] 1 Introduction
Motivation and problem background.
[SECTION level=2] 2 PilotRL
The proposed system overview.
[SECTION level=3] 2.1 AdaPlan
The planner method details.
[SECTION level=3] 2.2 Progressive Reinforcement Learning
Training objective and reward details.
[SECTION level=2] 3 Experiments
Datasets, baselines, metrics, and main results.
[SECTION level=3] 3.1 Experimental Setup
Setup details.
[SECTION level=2] 4 Ablations and Analysis
Ablation results.
[SECTION level=2] 5 Related Work
Prior agent planning methods.
[SECTION level=2] 6 Conclusion
Summary and limitations.
[SECTION level=2] References
Reference entries containing words such as method and experiment.
[SECTION level=2] Appendix B Experiment Details
Additional datasets and baseline details.
"""


def test_chat_completions_url_accepts_host_or_v1_base() -> None:
    assert _chat_completions_url("https://api.example.com") == (
        "https://api.example.com/v1/chat/completions"
    )
    assert _chat_completions_url("https://api.example.com/v1") == (
        "https://api.example.com/v1/chat/completions"
    )
    assert _chat_completions_url("https://api.example.com/v1/chat/completions") == (
        "https://api.example.com/v1/chat/completions"
    )


def test_streamed_chat_content_is_reassembled() -> None:
    lines = [
        b'data: {"choices":[{"delta":{"content":"{\\"ok\\""}}]}\n',
        b'data: {"choices":[{"delta":{"content":":true}"}}]}\n',
        b"data: [DONE]\n",
    ]

    assert _extract_stream_content(lines) == '{"ok":true}'


def test_relevant_excerpt_uses_complete_structured_chapters() -> None:
    method = _relevant_excerpt(
        STRUCTURED_SOURCE,
        "method",
        ("method", "training", "objective"),
        max_chars=10000,
    )
    experiments = _relevant_excerpt(
        STRUCTURED_SOURCE,
        "experiments",
        ("experiment", "result", "dataset", "ablation"),
        max_chars=10000,
    )
    background = _relevant_excerpt(
        STRUCTURED_SOURCE,
        "background",
        ("introduction", "background", "related work"),
        max_chars=10000,
    )

    assert "2 PilotRL" in method
    assert "2.1 AdaPlan" in method
    assert "3 Experiments" not in method
    assert "References" not in method

    assert "3 Experiments" in experiments
    assert "4 Ablations and Analysis" in experiments
    assert "Appendix B Experiment Details" in experiments
    assert "2 PilotRL" not in experiments

    assert "Abstract" in background
    assert "1 Introduction" in background
    assert "5 Related Work" in background
    assert "2 PilotRL" not in background


def test_main_experiments_take_priority_over_experiment_appendix() -> None:
    source = STRUCTURED_SOURCE.replace(
        "Additional datasets and baseline details.",
        "Additional datasets and baseline details. " * 80,
    )
    experiments = _relevant_excerpt(
        source,
        "experiments",
        ("experiment", "result", "dataset", "ablation", "appendix"),
        max_chars=1000,
    )

    assert "3 Experiments" in experiments
    assert "Appendix B Experiment Details" not in experiments


class FakeJsonClient:
    model = "fake-model"
    timeout_seconds = 180

    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def chat_json(self, system: str, user: str, **kwargs: object) -> dict[str, object]:
        request = json.loads(user)
        self.calls.append({"system": system, "request": request, **kwargs})
        section = request["analysis_section"]
        responses = {
            "background": {
                "background": {"field_overview": "背景"},
                "related_work": [],
                "keywords": ["agent"],
                "code_url": "",
                "project_url": "",
            },
            "motivation": {
                "one_sentence_summary": "摘要",
                "plain_language_problem": "问题",
                "contributions": ["贡献"],
                "motivation": {"research_gap": "缺口"},
            },
            "method": {
                "method": {"overview": "方法", "training_objective": "训练目标"},
            },
            "experiments": {
                "experiments": {
                    "setup": {"datasets": ["数据集"]},
                    "key_findings": ["结果"],
                },
                "limitations": ["局限"],
            },
        }
        return responses[section]


def test_note_generator_calls_four_sections_and_resumes(tmp_path) -> None:
    client = FakeJsonClient()
    checkpoint = tmp_path / "generation.json"
    note = NoteGenerator(client).generate(
        Paper(arxiv_id="2508.00344", title="PilotRL"),
        FullText(text=STRUCTURED_SOURCE, source="arxiv_html"),
        checkpoint_path=checkpoint,
    )

    assert [call["request"]["analysis_section"] for call in client.calls] == [
        "background",
        "motivation",
        "method",
        "experiments",
    ]
    assert note.content["background"]["field_overview"] == "背景"
    assert note.content["motivation"]["research_gap"] == "缺口"
    assert note.content["method"]["overview"] == "方法"
    assert note.content["method"]["training_objective"] == "训练目标"
    assert note.content["experiments"]["setup"]["datasets"] == ["数据集"]
    assert note.content["experiments"]["key_findings"] == ["结果"]
    assert note.content["limitations"] == ["局限"]

    resumed = NoteGenerator(client).generate(
        Paper(arxiv_id="2508.00344", title="PilotRL"),
        FullText(text=STRUCTURED_SOURCE, source="arxiv_html"),
        checkpoint_path=checkpoint,
    )

    assert len(client.calls) == 4
    assert resumed.content == note.content
