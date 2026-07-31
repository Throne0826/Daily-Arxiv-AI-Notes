import json
from pathlib import Path

from daily_arxiv_notes.models import Classification, GeneratedNote, Paper
from daily_arxiv_notes.render import (
    _normalize_inline_math,
    _sanitize_generated_text,
    render_category_index,
    render_categories_master,
    render_daily_index,
    render_global_category_index,
    render_note,
    render_review_index,
    validate_generated_content,
    validate_rendered_note,
)
from daily_arxiv_notes.taxonomy import Taxonomy


ROOT = Path(__file__).resolve().parents[1]


def taxonomy() -> Taxonomy:
    return Taxonomy(json.loads((ROOT / "taxonomy.json").read_text(encoding="utf-8")))


def generated_note() -> GeneratedNote:
    return GeneratedNote(
        generator_model="test-model",
        review_status="ai_draft",
        source_sha256="a" * 64,
        content={
            "one_sentence_summary": "本文研究训练分布漂移下的验证器可靠性。",
            "plain_language_problem": "模型训练越久，打分器看到的答案就越不一样，原来的打分标准可能失效。",
            "contributions": ["提出跨 checkpoint 的验证器可靠性评测。"],
            "background": {
                "field_overview": "验证器被用于后训练。",
                "prerequisite_concepts": [
                    {"term": "checkpoint", "explanation": "训练过程中保存的模型状态。"}
                ],
                "problem_setup": "比较不同策略检查点下验证器的判断。",
                "notation": [{"symbol": "r_\\phi", "meaning": "验证器给出的分数"}],
            },
            "motivation": {
                "practical_problem": "静态评测不能覆盖训练中的新输入。",
                "existing_approaches": [{"name": "静态基准", "how_it_works": "在固定数据集上测一次准确率。"}],
                "limitations_of_existing": ["策略会持续改变验证器的输入分布。"],
                "research_gap": "缺少跨 checkpoint 的动态可靠性监测。",
                "core_question": "如何用少量审计数据发现验证器失效？",
                "intuition": "优先审计高分但不确定的样本。",
            },
            "method": {
                "overview": "收集不同策略检查点的 rollout。",
                "pipeline_steps": [
                    {
                        "name": "动态审计",
                        "input": "当前 checkpoint 的 rollout",
                        "operation": "选择高风险样本并人工标注",
                        "output": "当前可靠性估计",
                        "plain_explanation": "像对可疑试卷做抽查。",
                    }
                ],
                "key_modules": [
                    {"name": "风险选样", "technical_detail": "结合分数与不确定性。", "plain_explanation": "把标注预算用在最可疑的样本上。"}
                ],
                "equations": [
                    {
                        "name": "校准损失",
                        "latex": "\\mathcal{L}=\\mathbb{E}_{(x,y)\\sim D_t}(r_\\phi(x)-y)^2",
                        "symbols": [{"symbol": "D_t", "meaning": "第 t 个检查点的审计数据"}],
                        "plain_explanation": "让验证器分数尽量接近可信标签。",
                        "source_location": "Section 3",
                    }
                ],
                "training_objective": "最小化验证器分数与可信标签的偏差。",
                "training_or_inference": "使用在线校准。",
                "implementation_details": "每个检查点采样 rollout。",
            },
            "experiments": {
                "research_questions": ["动态审计能否更早发现验证器漂移？"],
                "setup": {
                    "datasets": ["数学和代码任务。"],
                    "baselines": ["固定抽样审计。"],
                    "metrics": [{"name": "AUROC", "meaning": "区分正误答案的能力", "better_when": "越高越好"}],
                    "implementation": "每个 checkpoint 采样 100 条轨迹。",
                },
                "main_results": [
                    {
                        "setting": "test",
                        "result": "提高 3.0 点",
                        "plain_explanation": "在该设置下更能识别错误高分样本。",
                        "evidence_quote": "+3.0",
                        "source_location": "Table 1",
                    }
                ],
                "ablations": [],
                "case_studies": ["高分错误往往出现在新的代码模式上。"],
                "key_findings": ["静态准确率不能反映高分错误。"],
            },
            "limitations": ["只测试两个领域。"],
            "related_work": [{"work": "RewardBench", "relationship": "静态评测基线"}],
            "keywords": ["verifier drift"],
            "code_url": "",
            "project_url": "",
        },
    )


def test_note_has_required_sections() -> None:
    paper = Paper(
        arxiv_id="2607.00003",
        title="Reliable Learned Verifiers",
        authors=["Alice Example"],
        affiliations=["Example University"],
        announcement_date="2026-07-29",
        arxiv_url="https://arxiv.org/abs/2607.00003",
        pdf_url="https://arxiv.org/pdf/2607.00003",
    )
    classification = Classification(
        relevant=True,
        primary_category="llm_alignment",
        categories=["llm_alignment", "llm_reasoning"],
        confidence=0.9,
        reason="test",
        source="hybrid",
    )
    markdown = render_note(paper, classification, generated_note(), taxonomy())

    assert not validate_rendered_note(markdown)
    assert "## 研究背景" in markdown
    assert "## 研究动机" in markdown
    assert "## 研究方法" in markdown
    assert "## 实验" in markdown
    assert "\\mathcal{L}" in markdown
    assert "提高 3.0 点" in markdown
    assert '通讯单位</strong> Example University' in markdown
    assert "分类置信度" not in markdown


def test_note_keeps_main_results_compact_and_evidence_collapsed() -> None:
    note = generated_note()
    note.content["experiments"]["main_results"].extend(
        {
            "setting": f"补充结果 {index}",
            "result": f"结果 {index}",
            "plain_explanation": "用于验证结果展示上限。",
            "evidence_quote": f"evidence {index}",
            "source_location": f"Table {index}",
        }
        for index in range(2, 5)
    )
    markdown = render_note(
        Paper(arxiv_id="2607.00003", title="Reliable Learned Verifiers"),
        Classification(
            relevant=True,
            primary_category="llm_alignment",
            categories=["llm_alignment"],
            confidence=0.9,
            reason="test",
            source="hybrid",
        ),
        note,
        taxonomy(),
    )

    assert '<div class="result-list"' in markdown
    assert '<details class="result-evidence"' in markdown
    assert "补充结果 3" in markdown
    assert "补充结果 4" not in markdown


def test_number_without_evidence_is_flagged() -> None:
    note = generated_note()
    note.content["experiments"]["main_results"][0]["evidence_quote"] = ""
    assert "contains a number without evidence" in validate_generated_content(note.content)[0]


def test_equation_without_plain_explanation_is_flagged() -> None:
    note = generated_note()
    note.content["method"]["equations"][0]["plain_explanation"] = ""

    assert "equations[0] has no plain-language explanation" in validate_generated_content(note.content)


def test_note_marks_equation_availability() -> None:
    paper = Paper(
        arxiv_id="2607.00003",
        title="Reliable Learned Verifiers",
        authors=["Alice Example"],
        affiliations=["Example University"],
        announcement_date="2026-07-29",
        arxiv_url="https://arxiv.org/abs/2607.00003",
        pdf_url="https://arxiv.org/pdf/2607.00003",
    )
    note = generated_note()
    classification = Classification(
        relevant=True,
        primary_category="llm_reasoning",
        categories=["llm_reasoning"],
    )
    assert "formula-status--ready" in render_note(paper, classification, note, taxonomy())
    note.content["method"]["equations"] = []
    assert "formula-status--none" in render_note(paper, classification, note, taxonomy())


def test_categories_master_contains_data_views_and_network_payload() -> None:
    seen = {
        "2607.00001": {
            "announcement_date": "2026-07-29",
            "primary_category": "llm_reasoning",
            "categories": ["llm_reasoning", "llm_agent"],
        },
        "2607.00002": {
            "announcement_date": "2026-07-30",
            "primary_category": "robotics",
            "categories": ["robotics", "reinforcement_learning"],
        },
    }
    rendered = render_categories_master(seen, taxonomy())
    assert 'data-map-panel="landscape"' in rendered
    assert 'data-map-panel="trend"' in rendered
    assert 'data-map-panel="network"' in rendered
    assert '"latestDate": "2026-07-30"' in rendered
    assert "LLM Reasoning" in rendered
    assert "机器人 / 具身智能" in rendered


def test_fenced_latex_is_normalized_and_symbols_remain_math() -> None:
    note = generated_note()
    note.content["method"]["equations"][0]["latex"] = (
        "```latex\n$$\\mathcal{L}=\\mathbb{E}[x]$$\n```"
    )
    markdown = render_note(
        Paper(arxiv_id="2607.00003", title="Reliable Learned Verifiers"),
        Classification(
            relevant=True,
            primary_category="llm_alignment",
            categories=["llm_alignment"],
        ),
        note,
        taxonomy(),
    )

    assert "```latex" not in markdown
    assert "$$\n\\mathcal{L}=\\mathbb{E}[x]\n$$" in markdown
    assert "$D_t$" in markdown


def test_bare_inline_latex_is_delimited_without_touching_code_names() -> None:
    prose = (
        "形成 D=D_{\\mathrm{task}}\\cup D_{\\mathrm{harm}}，"
        "保留 s(x)\\in\\{\\mathrm{task},\\mathrm{harm}\\}，"
        "并按 T_d\\in\\{\\textsc{raw},\\textsc{self}\\} 渲染；"
        "防御者无需观察 T_a，字段 is_reflected 保持原样。"
    )

    normalized = _normalize_inline_math(prose)

    assert "$D=D_{\\mathrm{task}}\\cup D_{\\mathrm{harm}}$" in normalized
    assert "$s(x)\\in\\{\\mathrm{task},\\mathrm{harm}\\}$" in normalized
    assert "$T_d\\in\\{\\textsc{raw},\\textsc{self}\\}$" in normalized
    assert "$T_a$" in normalized
    assert "is_reflected" in normalized
    assert "$is_reflected$" not in normalized


def test_existing_inline_math_is_not_double_wrapped() -> None:
    value = "$D_{\\mathrm{task}}$ 与 \\(T_d\\) 已经带有定界符。"

    assert _normalize_inline_math(value) == value.replace(r"\(T_d\)", "$T_d$")


def test_generated_control_bytes_are_repaired_before_math_rendering() -> None:
    value = (
        "params $\x07gamma=\x07lambda=1$, state $\x00mathcal{M}$, label $\x1bC$, "
        "normalized $(\x08ar\\u0007delta, \\tilde\tu0007varphi)$, time $\tau$"
    )

    assert _sanitize_generated_text(value) == (
        r"params $\gamma=\lambda=1$, state $\mathcal{M}$, label $C$, "
        r"normalized $(\bar\delta, \tilde\varphi)$, time $\tau$"
    )


def test_rendered_note_rejects_control_bytes_and_legacy_delimiters() -> None:
    assert "contains unsupported control characters" in validate_rendered_note("\x07gamma")
    assert "contains legacy LaTeX delimiters" in validate_rendered_note(r"value \(x\)")


def test_inline_math_keeps_spaced_expressions_together() -> None:
    examples = {
        "X\\in\\mathbb{R}^{n\\times d}": "$X\\in\\mathbb{R}^{n\\times d}$",
        "p_t=\\pi_\\theta(\\cdot\\mid x_{<t})": "$p_t=\\pi_\\theta(\\cdot\\mid x_{<t})$",
        "\\mathbf A_n^*": "$\\mathbf A_n^*$",
        "Ω_{\\mathrm{BEV}}": "$Ω_{\\mathrm{BEV}}$",
        "V\\rightarrow\\mathbf{L}\\rightarrow A": "$V\\rightarrow\\mathbf{L}\\rightarrow A$",
        "d_i=(p_i,s_i,ℓ_i)": "$d_i=(p_i,s_i,ℓ_i)$",
        "h_o=[h_o^c,h_o^a,h_o^i]^⊤": "$h_o=[h_o^c,h_o^a,h_o^i]^⊤$",
        "S_{50\\%}": "$S_{50\\%}$",
        "S_{50\\%}^{$32\\times64$}": "$S_{50\\%}^{32\\times64}$",
        "\\hat y_i": "$\\hat y_i$",
        "\\lVert v_{k,c}\\rVert_2^2": "$\\lVert v_{k,c}\\rVert_2^2$",
        "λ_u L_{FM}^u+Σ_m λ_m L_{FM}^m": "$λ_u L_{FM}^u+Σ_m λ_m L_{FM}^m$",
        "\\Delta t s_j^*": "$\\Delta t s_j^*$",
    }

    for source, expected in examples.items():
        assert _normalize_inline_math(source) == expected


def test_concept_and_metric_items_use_styled_class_names() -> None:
    markdown = render_note(
        Paper(arxiv_id="2607.00003", title="Reliable Learned Verifiers"),
        Classification(
            relevant=True,
            primary_category="llm_alignment",
            categories=["llm_alignment"],
        ),
        generated_note(),
        taxonomy(),
    )

    assert 'class="concept-item"' in markdown
    assert 'class="notation-item"' in markdown
    assert 'class="metric-item"' in markdown
    assert 'class="conceptitem"' not in markdown
    assert '<span class="paper-mini-label">数据与任务</span>\n\n-' in markdown


def test_inline_math_is_normalized_in_related_work_tables_and_evidence() -> None:
    note = generated_note()
    note.content["related_work"][0]["work"] = "\\pi_{0.5}\\text{-DROID}"
    note.content["experiments"]["ablations"] = [
        {
            "setting": "移除 F_set",
            "result": "H_train 下降",
            "plain_explanation": "比较符号指标。",
            "source_location": "Table 2",
            "evidence_quote": "N(k_{2}\\delta)\\rho",
        }
    ]
    note.content["experiments"]["main_results"][0]["evidence_quote"] = (
        "N(k_{2}\\delta)\\rho"
    )

    markdown = render_note(
        Paper(arxiv_id="2607.00003", title="Reliable Learned Verifiers"),
        Classification(
            relevant=True,
            primary_category="llm_alignment",
            categories=["llm_alignment"],
        ),
        note,
        taxonomy(),
    )

    assert "$\\pi_{0.5}\\text{-DROID}$" in markdown
    assert "$F_set$" in markdown
    assert "$H_train$" in markdown
    assert "$N(k_{2}\\delta)\\rho$" in markdown
    assert '<div class="experiment-evidence" markdown="1">' in markdown


def test_daily_and_category_indexes_include_every_matching_category() -> None:
    paper = Paper(
        arxiv_id="2607.00003",
        title="Reliable Learned Verifiers",
        announcement_date="2026-07-29",
    )
    classification = Classification(
        relevant=True,
        primary_category="llm_alignment",
        categories=["llm_alignment", "llm_reasoning"],
    )
    record = {
        "paper": paper,
        "classification": classification,
        "path": "llm_alignment/reliable-learned-verifiers.md",
        "summary": "同时属于对齐和推理。",
        "review_status": "ai_draft",
    }

    daily = render_daily_index("2026-07-29", [record], taxonomy())
    secondary = render_category_index("llm_reasoning", [record], taxonomy())

    assert daily.count("Reliable Learned Verifiers") == 2
    assert "形成 **2** 条分类记录" in daily
    assert "(../llm_alignment/reliable-learned-verifiers.md)" in secondary


def test_cross_site_indexes_link_to_daily_note() -> None:
    seen = {
        "2607.00003": {
            "announcement_date": "2026-07-29",
            "path": "2026-07-29/llm_alignment/reliable-learned-verifiers.md",
            "title": "Reliable Learned Verifiers",
            "summary": "研究训练分布漂移下的验证器可靠性。",
            "primary_category": "llm_alignment",
            "review_status": "ai_draft",
            "classification_confidence": 0.9,
            "issues": ["main_results[0] evidence quote not found in source"],
        }
    }
    review = render_review_index(seen)
    category = render_global_category_index(
        "llm_alignment",
        list(seen.items()),
        taxonomy(),
    )

    assert "(../arxiv_daily/2026-07-29/llm_alignment/reliable-learned-verifiers.md)" in review
    assert "(../../arxiv_daily/2026-07-29/llm_alignment/reliable-learned-verifiers.md)" in category
    assert "evidence quote not found" in review
