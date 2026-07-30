from __future__ import annotations

import json
import html
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import Classification, GeneratedNote, Paper
from .taxonomy import Taxonomy


REQUIRED_HEADINGS = [
    "## 研究背景",
    "## 研究动机",
    "## 研究方法",
    "## 实验",
]


def slugify(title: str, arxiv_id: str, max_length: int = 100) -> str:
    slug = title.lower().replace("&", " and ")
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    slug = slug[:max_length].rstrip("-")
    return slug or arxiv_id.replace(".", "-")


def _yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _list_items(
    values: list[str],
    empty: str = "- 原文未明确报告。",
    limit: int | None = None,
) -> str:
    cleaned = [str(value).strip() for value in values if str(value).strip()]
    if limit is not None:
        cleaned = cleaned[:limit]
    return "\n".join(f"- {value}" for value in cleaned) if cleaned else empty


def _text(value: Any, empty: str = "原文未明确报告。") -> str:
    cleaned = str(value or "").strip()
    return cleaned or empty


def _object_items(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _concept_grid(
    items: Any,
    css_class: str,
    title_key: str,
    detail_key: str,
    limit: int | None = None,
) -> str:
    blocks = []
    values = _object_items(items)
    if limit is not None:
        values = values[:limit]
    for item in values:
        title = _text(item.get(title_key, ""), "未命名概念")
        detail = _text(item.get(detail_key, ""))
        blocks.append(
            f'<div class="{css_class[:-5]}item" markdown="1">\n\n'
            f"**{title}**\n\n{detail}\n\n</div>"
        )
    if not blocks:
        return "原文未明确报告，或这里不需要额外前置概念。"
    return f'<div class="{css_class}" markdown="1">\n\n' + "\n".join(blocks) + "\n\n</div>"


def _notation_grid(items: Any, limit: int = 6) -> str:
    normalized = []
    for item in _object_items(items):
        symbol = str(item.get("symbol", "")).strip().strip("$")
        if not symbol:
            continue
        normalized.append({"symbol": f"${symbol}$", "meaning": item.get("meaning", "")})
    return _concept_grid(normalized, "notation-list", "symbol", "meaning", limit=limit)


def _named_explanations(
    items: Any,
    name_key: str,
    detail_key: str,
    limit: int | None = None,
) -> str:
    lines = []
    values = _object_items(items)
    if limit is not None:
        values = values[:limit]
    for item in values:
        name = _text(item.get(name_key, ""), "未命名方法")
        detail = _text(item.get(detail_key, ""))
        lines.append(f"- **{name}**：{detail}")
    return "\n".join(lines) if lines else "- 原文未明确报告。"


def _method_steps(items: Any, limit: int = 4) -> str:
    blocks = []
    for item in _object_items(items)[:limit]:
        name = _text(item.get("name", ""), "未命名步骤")
        operation = _text(item.get("operation", ""))
        input_value = _text(item.get("input", ""))
        output_value = _text(item.get("output", ""))
        plain = _text(item.get("plain_explanation", ""))
        blocks.append(
            '<div class="method-step" markdown="1">\n\n'
            '<div class="method-step__body" markdown="1">\n\n'
            f"#### {name}\n\n{operation}\n\n"
            '<div class="method-step__io" markdown="1">\n\n'
            f"**输入**：{input_value}  \n**输出**：{output_value}\n\n</div>\n\n"
            f"**直观理解**：{plain}\n\n</div>\n\n</div>"
        )
    if not blocks:
        return "原文未明确报告完整流程。"
    return '<div class="method-steps" markdown="1">\n\n' + "\n".join(blocks) + "\n\n</div>"


def _key_modules(items: Any, limit: int = 4) -> str:
    lines = []
    for index, item in enumerate(_object_items(items)[:limit], start=1):
        name = _text(item.get("name", ""), f"模块 {index}")
        technical = _text(item.get("technical_detail", ""))
        plain = _text(item.get("plain_explanation", ""))
        lines.append(f"**{index}. {name}**\n\n{technical}\n\n> 直观理解：{plain}")
    return "\n\n".join(lines) if lines else "原文未明确报告。"


def _normalize_latex(value: Any) -> str:
    latex = str(value or "").strip()
    fence = re.fullmatch(r"```(?:latex|tex|math)?\s*\n?(.*?)\n?```", latex, re.DOTALL | re.I)
    if fence:
        latex = fence.group(1).strip()
    wrappers = (("$$", "$$"), ("\\[", "\\]"), ("\\(", "\\)"))
    changed = True
    while changed:
        changed = False
        for opening, closing in wrappers:
            if latex.startswith(opening) and latex.endswith(closing):
                latex = latex[len(opening) : -len(closing)].strip()
                changed = True
                break
    return latex


def _equation_blocks(items: Any, limit: int = 2) -> str:
    blocks = []
    for item in _object_items(items)[:limit]:
        latex = _normalize_latex(item.get("latex", ""))
        if not latex:
            continue
        name = _text(item.get("name", ""), "关键公式")
        source = _text(item.get("source_location", ""), "原文位置未明确报告")
        symbols = []
        for symbol in _object_items(item.get("symbols", [])):
            raw_symbol = str(symbol.get("symbol", "")).strip().strip("$")
            if raw_symbol:
                symbols.append(f"- ${raw_symbol}$：{_text(symbol.get('meaning', ''))}")
        symbol_text = "\n".join(symbols) if symbols else "- 原文未单独列出符号定义。"
        plain = _text(item.get("plain_explanation", ""))
        blocks.append(
            '<div class="equation-block" markdown="1">\n\n'
            f"#### {name}\n\n$$\n{latex}\n$$\n\n"
            f"**符号说明**\n\n{symbol_text}\n\n"
            '<div class="equation-explanation" markdown="1">\n\n'
            f"**直观理解**：{plain}  \n**原文位置**：{source}\n\n</div>\n\n</div>"
        )
    if not blocks:
        return (
            '<div class="formula-status formula-status--none" markdown="1">\n\n'
            "**未收录可核对的关键公式**\n\n"
            "该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。\n\n"
            "</div>"
        )
    status = (
        '<div class="formula-status formula-status--ready" markdown="1">\n\n'
        f"**已定位 {len(blocks)} 个关键公式**\n\n"
        "以下方程保留符号说明、直观解释与原文位置。\n\n"
        "</div>"
    )
    return status + "\n\n" + "\n\n".join(blocks)


def _experiment_table(rows: list[dict[str, Any]], limit: int = 4) -> str:
    if not rows:
        return "原文未明确报告，或自动提取阶段未获得可靠数据。"
    rendered = ["| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |", "|---|---|---|---|"]
    for row in rows[:limit]:
        setting = str(row.get("setting", "")).replace("|", "\\|")
        result = str(row.get("result", "")).replace("|", "\\|")
        explanation = str(row.get("plain_explanation", "")).replace("|", "\\|")
        location = str(row.get("source_location", "")).replace("|", "\\|")
        evidence = str(row.get("evidence_quote", "")).replace("|", "\\|")
        rendered.append(
            f"| {setting} | {result} | {explanation or '待核对。'} | "
            f"{location}<br><span class=\"experiment-evidence\">{evidence}</span> |"
        )
    return "\n".join(rendered)


def _experiment_results(rows: list[dict[str, Any]], limit: int = 3) -> str:
    blocks = []
    for index, row in enumerate(rows[:limit], start=1):
        setting = _text(row.get("setting", ""), f"核心结果 {index}")
        result = _text(row.get("result", ""))
        explanation = _text(row.get("plain_explanation", ""), "该结果仍需结合原文语境解读。")
        location = _text(row.get("source_location", ""), "原文位置未明确报告")
        evidence = str(row.get("evidence_quote", "")).strip()
        evidence_block = ""
        if evidence:
            evidence_block = (
                '<details class="result-evidence" markdown="1">\n'
                '<summary>核对原文证据</summary>\n\n'
                f'<span class="experiment-evidence">{evidence}</span>\n\n'
                "</details>"
            )
        blocks.append(
            '<article class="result-item" markdown="1">\n\n'
            f'<span class="result-index">{index:02d}</span>\n\n'
            f"#### {setting}\n\n"
            '<div class="result-value" markdown="1">\n\n'
            f"{result}\n\n</div>\n\n"
            f"{explanation}\n\n"
            '<div class="result-source" markdown="1">\n\n'
            f"来源：{location}\n\n</div>\n\n"
            f"{evidence_block}\n\n"
            "</article>"
        )
    if not blocks:
        return "原文未明确报告，或自动提取阶段未获得可靠数据。"
    return '<div class="result-list" markdown="1">\n\n' + "\n".join(blocks) + "\n\n</div>"


def render_note(
    paper: Paper,
    classification: Classification,
    generated: GeneratedNote,
    taxonomy: Taxonomy,
) -> str:
    content = generated.content
    legacy_background = content.get("background_motivation", {})
    background = content.get("background", {})
    if not isinstance(background, dict) or not background:
        background = {
            "field_overview": legacy_background.get("field_status", ""),
            "prerequisite_concepts": [],
            "problem_setup": legacy_background.get("pain_point", ""),
            "notation": [],
        }
    motivation = content.get("motivation", {})
    if not isinstance(motivation, dict) or not motivation:
        motivation = {
            "practical_problem": legacy_background.get("pain_point", ""),
            "existing_approaches": [],
            "limitations_of_existing": [legacy_background.get("core_conflict", "")],
            "research_gap": legacy_background.get("objective", ""),
            "core_question": legacy_background.get("objective", ""),
            "intuition": legacy_background.get("core_idea", ""),
        }
    method = content.get("method", {}) if isinstance(content.get("method", {}), dict) else {}
    experiments = (
        content.get("experiments", {})
        if isinstance(content.get("experiments", {}), dict)
        else {}
    )
    setup = experiments.get("setup", {})
    if not isinstance(setup, dict):
        setup = {"datasets": [], "baselines": [], "metrics": [], "implementation": setup}

    pipeline_steps = method.get("pipeline_steps", [])
    if not pipeline_steps:
        pipeline_steps = [
            {
                "name": item.get("name", ""),
                "input": "原文未明确报告。",
                "operation": item.get("detail", ""),
                "output": "原文未明确报告。",
                "plain_explanation": item.get("detail", ""),
            }
            for item in _object_items(method.get("key_designs", []))
        ]

    metrics = []
    for metric in _object_items(setup.get("metrics", [])):
        meaning = _text(metric.get("meaning", ""))
        better_when = str(metric.get("better_when", "")).strip()
        if better_when:
            meaning = f"{meaning} （{better_when}）"
        metrics.append({"name": metric.get("name", ""), "detail": meaning})

    keywords = [str(value) for value in content.get("keywords", []) if str(value).strip()]
    tag_values = [taxonomy.label(category) for category in classification.categories] + keywords
    tags = "\n".join(f"  - {_yaml_string(value)}" for value in dict.fromkeys(tag_values))
    category_label = taxonomy.label(classification.primary_category)
    code_url = str(content.get("code_url", "")).strip()
    project_url = str(content.get("project_url", "")).strip()
    links = []
    if code_url:
        links.append(f"**代码**: [{code_url}]({code_url})  ")
    if project_url:
        links.append(f"**项目页**: [{project_url}]({project_url})  ")

    related = []
    for item in content.get("related_work", [])[:3]:
        if not isinstance(item, dict):
            continue
        work = str(item.get("work", "")).strip()
        relationship = str(item.get("relationship", "")).strip()
        if work:
            related.append(f"- **{work}**: {relationship or '关系待人工核验。'}")

    authors = ", ".join(paper.authors) if paper.authors else "原文元数据未获取"
    affiliations = "；".join(paper.affiliations) if paper.affiliations else "arXiv 元数据未标注"
    generated_at = datetime.now(timezone.utc).isoformat()
    summary = str(content.get("one_sentence_summary", "原文未明确报告。")).strip()
    plain_problem = _text(content.get("plain_language_problem", ""), summary)
    description = f"[arXiv {paper.arxiv_id}][{category_label}] {summary}"[:300]
    frontmatter = "\n".join(
        [
            "---",
            f"title: {_yaml_string('[论文解读] ' + paper.title)}",
            f"description: {_yaml_string(description)}",
            f"arxiv_id: {_yaml_string(paper.arxiv_id)}",
            f"announcement_date: {_yaml_string(paper.announcement_date)}",
            f"primary_category: {_yaml_string(classification.primary_category)}",
            f"review_status: {_yaml_string(generated.review_status)}",
            f"generator_model: {_yaml_string(generated.generator_model)}",
            f"generated_at: {_yaml_string(generated_at)}",
            f"source_sha256: {_yaml_string(generated.source_sha256)}",
            "tags:",
            tags or "  - \"待分类\"",
            "---",
        ]
    )
    return f"""{frontmatter}

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">{category_label} · arXiv {paper.arxiv_id}</p>

# {paper.title}

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> {paper.announcement_date or '未知'}</span>
<span><strong>作者</strong> {authors}</span>
<span><strong>通讯单位</strong> {affiliations}</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文]({paper.arxiv_url or f'https://arxiv.org/abs/{paper.arxiv_id}'}) · [PDF 下载]({paper.pdf_url or f'https://arxiv.org/pdf/{paper.arxiv_id}'}) · **关键词** {', '.join(keywords) if keywords else category_label}  
{''.join(links)}

</div>

<nav class="paper-jump" aria-label="论文解读章节">
  <a href="#研究背景"><span>01</span>研究背景</a>
  <a href="#研究动机"><span>02</span>研究动机</a>
  <a href="#研究方法"><span>03</span>研究方法</a>
  <a href="#实验"><span>04</span>实验结果</a>
</nav>

<div class="paper-quickread" markdown="1">

<div class="paper-quickread__main" markdown="1">

<span class="paper-mini-label">先用一句话判断</span>

{summary}

**不用术语来说**：{plain_problem}

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

{_list_items(content.get('contributions', []), limit=2)}

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

{_text(background.get('field_overview', ''))}

</div>

<p class="paper-minor-label">小白先知道</p>

{_concept_grid(background.get('prerequisite_concepts', []), 'concept-list', 'term', 'explanation', limit=3)}

<div class="paper-focus" markdown="1">

**论文具体研究什么**

{_text(background.get('problem_setup', ''))}

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

{_notation_grid(background.get('notation', []))}

**直接相关的工作**

{chr(10).join(related) if related else '- 原文未明确报告，待核对引用关系。'}

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

{_text(motivation.get('practical_problem', ''))}

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

{_named_explanations(motivation.get('existing_approaches', []), 'name', 'how_it_works', limit=2)}

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

{_list_items(motivation.get('limitations_of_existing', []), limit=2)}

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

{_text(motivation.get('research_gap', ''))}

</div>
<div markdown="1"><span>核心问题</span>

{_text(motivation.get('core_question', ''))}

</div>
<div markdown="1"><span>作者直觉</span>

{_text(motivation.get('intuition', ''))}

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

{_text(method.get('overview', ''))}

</div>

<p class="paper-minor-label">关键流程</p>

{_method_steps(pipeline_steps)}

<p class="paper-minor-label">真正需要看懂的公式</p>

{_equation_blocks(method.get('equations', []))}

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：{_text(method.get('training_objective', ''))}

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

{_key_modules(method.get('key_modules', []))}

**训练与推理**

{_text(method.get('training_or_inference', ''))}

**复现信息**

{_text(method.get('implementation_details', ''))}

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>{_list_items(setup.get('datasets', []), limit=3)}</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span>{_concept_grid(metrics, 'metric-list', 'name', 'detail', limit=3)}</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

{_experiment_results(experiments.get('main_results', []))}

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

{_list_items(content.get('limitations', []), limit=2)}

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

{_list_items(setup.get('baselines', []), limit=4)}

**实验想回答的问题**

{_list_items(experiments.get('research_questions', []), limit=2)}

**实验实现**

{_text(setup.get('implementation', ''))}

**关键消融**

{_experiment_table(experiments.get('ablations', []), limit=3)}

**定性案例**

{_list_items(experiments.get('case_studies', []), limit=2)}

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`{generated.review_status}`
- 分类理由：{classification.reason}
- 全文指纹：`{generated.source_sha256}`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
"""


def validate_rendered_note(markdown: str) -> list[str]:
    issues = [f"missing heading: {heading}" for heading in REQUIRED_HEADINGS if heading not in markdown]
    if "review_status:" not in markdown:
        issues.append("missing review_status frontmatter")
    if "source_sha256:" not in markdown:
        issues.append("missing source fingerprint")
    return issues


def validate_generated_content(content: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for section in ("background", "motivation", "method", "experiments"):
        if not isinstance(content.get(section), dict):
            issues.append(f"missing structured section: {section}")

    method = content.get("method", {})
    if isinstance(method, dict):
        for index, equation in enumerate(method.get("equations", [])):
            if not isinstance(equation, dict):
                issues.append(f"equations[{index}] is not an object")
                continue
            if equation.get("latex") and not str(equation.get("plain_explanation", "")).strip():
                issues.append(f"equations[{index}] has no plain-language explanation")

    experiments = content.get("experiments", {})
    if not isinstance(experiments, dict):
        return issues
    for section in ("main_results", "ablations"):
        for index, row in enumerate(experiments.get(section, [])):
            if not isinstance(row, dict):
                issues.append(f"{section}[{index}] is not an object")
                continue
            result = str(row.get("result", ""))
            evidence = str(row.get("evidence_quote", ""))
            if re.search(r"\d", result) and not evidence.strip():
                issues.append(f"{section}[{index}] contains a number without evidence")
    return issues


def _record_categories(record: dict[str, Any]) -> list[str]:
    classification = record.get("classification")
    if isinstance(classification, Classification):
        values = classification.categories or [classification.primary_category]
    else:
        primary = str(record.get("primary_category", ""))
        values = record.get("categories", [primary])
    return list(dict.fromkeys(str(value) for value in values if str(value)))


def _paper_index_item(
    record: dict[str, Any],
    href: str,
    taxonomy: Taxonomy,
    *,
    show_date: bool = False,
) -> str:
    paper = record.get("paper")
    title = paper.title if isinstance(paper, Paper) else str(record.get("title", "未命名论文"))
    arxiv_id = paper.arxiv_id if isinstance(paper, Paper) else str(record.get("arxiv_id", ""))
    announcement_date = (
        paper.announcement_date
        if isinstance(paper, Paper)
        else str(record.get("announcement_date", ""))
    )
    summary = str(record.get("summary", "")).replace("\n", " ").strip()
    if not summary:
        summary = "中文摘要尚未生成，请进入论文页查看现有元数据。"
    safe_title = title.replace("[", "\\[").replace("]", "\\]")
    category_chips = "".join(
        f'<span class="paper-category-chip">{html.escape(taxonomy.label(category))}</span>'
        for category in _record_categories(record)
        if taxonomy.valid_category(category)
    )
    date_meta = (
        f'<span class="daily-paper-date">{html.escape(announcement_date)}</span>'
        if show_date and announcement_date
        else ""
    )
    return (
        '<article class="daily-paper-item" markdown="1">\n\n'
        f"#### [{safe_title}]({href})\n\n"
        '<div class="daily-paper-meta">'
        f'<span class="daily-paper-id">arXiv {html.escape(arxiv_id)}</span>'
        f"{date_meta}{category_chips}</div>\n\n"
        '<div class="daily-paper-summary" markdown="1">\n\n'
        f"{summary}\n\n</div>\n\n</article>"
    )


def render_daily_index(
    announcement_date: str,
    records: list[dict[str, Any]],
    taxonomy: Taxonomy,
) -> str:
    assignments = sum(len(_record_categories(record)) for record in records)
    lines = [
        "---",
        f"title: {_yaml_string('arXiv 每日论文 · ' + announcement_date)}",
        f"description: {_yaml_string(f'{announcement_date} 筛选出的 {len(records)} 篇 AI arXiv 新论文中文解读。')}",
        "---",
        "",
        f"# arXiv 每日论文：{announcement_date}",
        "",
        '<div class="daily-overview" markdown="1">',
        "",
        f"收录 **{len(records)}** 篇不重复论文，形成 **{assignments}** 条分类记录。多标签论文会同时出现在所有相关方向中。",
        "",
        "</div>",
        "",
    ]
    for group_name, group in taxonomy.groups.items():
        group_records = [
            record
            for record in records
            if any(taxonomy.group_for(category) == group_name for category in _record_categories(record))
        ]
        if not group_records:
            continue
        group_ids = {record["paper"].arxiv_id for record in group_records}
        lines.extend([f"## {group['label']} · {len(group_ids)} 篇", ""])
        for category in group["categories"]:
            category_records = [
                record
                for record in group_records
                if category in _record_categories(record)
            ]
            if not category_records:
                continue
            lines.extend(
                [
                    '<section class="daily-category-section" markdown="1">',
                    "",
                    f"### {taxonomy.label(category)} · {len(category_records)} 篇",
                    "",
                    '<div class="daily-paper-list" markdown="1">',
                    "",
                ]
            )
            for record in category_records:
                relative_path = Path(record["path"]).as_posix()
                lines.extend(
                    [_paper_index_item(record, relative_path, taxonomy), ""]
                )
            lines.extend(["</div>", "", "</section>", ""])
    return "\n".join(lines).rstrip() + "\n"


def render_category_index(
    category: str,
    records: list[dict[str, Any]],
    taxonomy: Taxonomy,
) -> str:
    lines = [
        "---",
        f"title: {_yaml_string(taxonomy.label(category))}",
        "---",
        "",
        f"# {taxonomy.label(category)}",
        "",
        f"当日共 **{len(records)}** 篇相关论文。多标签论文链接到其唯一正文页。",
        "",
        '<div class="daily-paper-list" markdown="1">',
        "",
    ]
    for record in records:
        classification = record["classification"]
        canonical = Path(record["path"])
        href = (
            canonical.name
            if classification.primary_category == category
            else (Path("..") / canonical).as_posix()
        )
        lines.extend([_paper_index_item(record, href, taxonomy), ""])
    lines.extend(["</div>", ""])
    return "\n".join(lines).rstrip() + "\n"


def render_daily_master(dates: list[str], seen: dict[str, Any]) -> str:
    lines = [
        "---",
        "title: 每日 arXiv 论文",
        "description: 按发布日期浏览筛选后的 AI arXiv 新论文与中文解读。",
        "---",
        "",
        "# 每日 arXiv 论文",
        "",
    ]
    if not dates:
        return "\n".join(lines + ["尚未生成日报。", ""])
    lines.extend(["| 日期 | 论文数 |", "|---|---:|"])
    for value in dates:
        papers = [item for item in seen.values() if item.get("announcement_date") == value]
        lines.append(f"| [{value}]({value}/index.md) | {len(papers)} |")
    lines.extend(["", "日榜只包含当日新投稿和 cross-list，并按 arXiv ID 去重。", ""])
    return "\n".join(lines)


def render_categories_master(seen: dict[str, Any], taxonomy: Taxonomy) -> str:
    records = list(seen.values())
    dates = sorted(
        {str(item.get("announcement_date", "")) for item in records if item.get("announcement_date")}
    )
    latest_date = dates[-1] if dates else ""
    previous_date = dates[-2] if len(dates) > 1 else ""
    counts: Counter[str] = Counter()
    latest_counts: Counter[str] = Counter()
    previous_counts: Counter[str] = Counter()
    pair_counts: Counter[tuple[str, str]] = Counter()
    assignments = 0
    multi_label = 0
    cross_domain = 0

    for item in records:
        primary = str(item.get("primary_category", ""))
        categories = list(
            dict.fromkeys(
                category
                for category in item.get("categories", [primary])
                if taxonomy.valid_category(str(category))
            )
        )
        counts.update(categories)
        assignments += len(categories)
        if len(categories) > 1:
            multi_label += 1
        item_groups = {taxonomy.group_for(category) for category in categories}
        if len(item_groups) > 1:
            cross_domain += 1
        if str(item.get("announcement_date", "")) == latest_date:
            latest_counts.update(categories)
        if str(item.get("announcement_date", "")) == previous_date:
            previous_counts.update(categories)
        for left_index, left in enumerate(categories):
            for right in categories[left_index + 1 :]:
                pair_counts[tuple(sorted((left, right)))] += 1

    group_rows = []
    category_rows = []
    for group_id, group in taxonomy.groups.items():
        group_categories = list(group["categories"])
        group_total = sum(counts[category] for category in group_categories)
        group_unique = sum(
            1
            for item in records
            if any(
                category in set(item.get("categories", [item.get("primary_category", "")]))
                for category in group_categories
            )
        )
        group_rows.append(
            {
                "id": group_id,
                "label": group["label"],
                "assignments": group_total,
                "papers": group_unique,
            }
        )
        for category in group_categories:
            category_rows.append(
                {
                    "id": category,
                    "label": taxonomy.label(category),
                    "group": group_id,
                    "count": counts[category],
                    "latest": latest_counts[category],
                    "delta": latest_counts[category] - previous_counts[category],
                    "href": f"{category}/",
                }
            )

    date_rows = []
    for date_value in dates:
        date_records = [
            item for item in records if str(item.get("announcement_date", "")) == date_value
        ]
        date_groups = []
        for group_id, group in taxonomy.groups.items():
            category_set = set(group["categories"])
            group_count = sum(
                1
                for item in date_records
                if category_set
                & set(item.get("categories", [item.get("primary_category", "")]))
            )
            date_groups.append(
                {"id": group_id, "label": group["label"], "count": group_count}
            )
        date_rows.append(
            {"date": date_value, "papers": len(date_records), "groups": date_groups}
        )

    connections = [
        {
            "source": left,
            "target": right,
            "count": count,
            "source_label": taxonomy.label(left),
            "target_label": taxonomy.label(right),
        }
        for (left, right), count in pair_counts.most_common(18)
    ]
    map_data = {
        "latestDate": latest_date,
        "previousDate": previous_date,
        "groups": group_rows,
        "categories": category_rows,
        "dates": date_rows,
        "connections": connections,
    }
    map_json = json.dumps(map_data, ensure_ascii=False).replace("</", "<\\/")
    multi_rate = round(multi_label / len(records) * 100) if records else 0
    lines = [
        "---",
        "title: AI 研究版图",
        "description: 用研究分布、每日变化与多标签关联探索 LLM、生成与多模态、决策与具身方向的 arXiv 论文。",
        "hide:",
        "  - toc",
        "---",
        "",
        '<div class="research-map" data-research-map>',
        "",
        '<header class="research-map__header">',
        '<p class="research-map__eyebrow">LIVE RESEARCH LANDSCAPE</p>',
        "<h1>AI 研究版图</h1>",
        (
            f"<p>把 {len(records)} 篇论文看成一个持续变化的研究网络：节点表示细分方向，"
            "节点大小表示累计论文量，连线来自同一论文的多标签共现。</p>"
        ),
        "</header>",
        "",
        '<section class="research-map__metrics" aria-label="论文版图概览">',
        f'<div><strong>{len(records)}</strong><span>不重复论文</span></div>',
        f'<div><strong>{assignments}</strong><span>方向归属</span></div>',
        f'<div><strong>{multi_rate}%</strong><span>多标签论文</span></div>',
        f'<div><strong>{cross_domain}</strong><span>跨主域论文</span></div>',
        "</section>",
        "",
        '<div class="research-map__toolbar" role="tablist" aria-label="研究地图视图">',
        '<button type="button" class="is-active" role="tab" aria-selected="true" data-map-view="landscape">研究版图</button>',
        '<button type="button" role="tab" aria-selected="false" data-map-view="trend">每日变化</button>',
        '<button type="button" role="tab" aria-selected="false" data-map-view="network">方向关联</button>',
        "</div>",
        "",
        '<section class="research-map__panel is-active" role="tabpanel" data-map-panel="landscape">',
        '<div class="research-domain-grid">',
        "",
    ]
    maximum = max(counts.values(), default=1) or 1
    for group_id, group in taxonomy.groups.items():
        group_categories = list(group["categories"])
        group_assignments = sum(counts[category] for category in group_categories)
        lines.extend(
            [
                f'<section class="research-domain" data-map-group="{group_id}">',
                '<div class="research-domain__head">',
                f"<h2>{html.escape(group['label'])}</h2>",
                f"<span>{group_assignments} 条归属</span>",
                "</div>",
                '<div class="research-node-field">',
            ]
        )
        for category in group["categories"]:
            count = counts[category]
            size = 4.2 + (count / maximum) ** 0.5 * 3.4
            delta = latest_counts[category] - previous_counts[category]
            delta_label = f"最新日 +{delta}" if delta > 0 else (f"最新日 {delta}" if delta < 0 else "最新日持平")
            lines.append(
                f'<a class="research-node" href="{category}/" style="--node-size:{size:.2f}rem" '
                f'data-map-group="{group_id}" title="{html.escape(taxonomy.label(category))}：{count} 篇">'
                f'<strong>{count}</strong><span>{html.escape(taxonomy.label(category))}</span>'
                f'<small>{delta_label}</small></a>'
            )
        lines.extend(["</div>", "</section>", ""])
    lines.extend(
        [
            "</div>",
            "</section>",
            "",
            '<section class="research-map__panel" role="tabpanel" data-map-panel="trend" hidden>',
            '<div class="research-trend">',
            '<div class="research-trend__legend">',
        ]
    )
    for group_id, group in taxonomy.groups.items():
        lines.append(
            f'<span data-map-group="{group_id}">{html.escape(group["label"])}</span>'
        )
    lines.extend(["</div>", ""])
    for date_row in reversed(date_rows):
        group_sum = sum(group["count"] for group in date_row["groups"]) or 1
        lines.extend(
            [
                '<div class="research-trend__row">',
                f'<div><time>{date_row["date"]}</time><span>{date_row["papers"]} 篇论文</span></div>',
                '<div class="research-trend__bar" aria-label="各主域相关论文占比">',
            ]
        )
        for group in date_row["groups"]:
            share = group["count"] / group_sum * 100
            lines.append(
                f'<span data-map-group="{group["id"]}" style="--segment-share:{share:.2f}%" '
                f'title="{html.escape(group["label"])}：{group["count"]} 篇"></span>'
            )
        lines.extend(["</div>", "</div>", ""])
    lines.extend(
        [
            "</div>",
            '<p class="research-map__note">同一篇多标签论文可以同时计入多个主域，因此主域计数之和可能高于当日论文数。</p>',
            "</section>",
            "",
            '<section class="research-map__panel" role="tabpanel" data-map-panel="network" hidden>',
            '<div class="research-network">',
            '<svg class="research-network__canvas" data-map-network viewBox="0 0 1000 560" role="img" aria-label="论文方向共现网络"></svg>',
            '<aside class="research-network__detail" data-map-detail>',
            "<span>最强关联</span>",
            (
                f"<strong>{html.escape(connections[0]['source_label'])} × {html.escape(connections[0]['target_label'])}</strong>"
                if connections
                else "<strong>等待更多多标签论文</strong>"
            ),
            (
                f"<p>共有 {connections[0]['count']} 篇论文同时进入这两个方向。</p>"
                if connections
                else "<p>当前数据还不足以形成稳定的方向关联。</p>"
            ),
            "</aside>",
            "</div>",
            '<ol class="research-connection-list">',
        ]
    )
    for connection in connections[:6]:
        lines.append(
            "<li>"
            f'<a href="{connection["source"]}/">{html.escape(connection["source_label"])}</a>'
            "<span>×</span>"
            f'<a href="{connection["target"]}/">{html.escape(connection["target_label"])}</a>'
            f'<strong>{connection["count"]}</strong>'
            "</li>"
        )
    lines.extend(
        [
            "</ol>",
            "</section>",
            "",
            f'<script type="application/json" data-research-map-data>{map_json}</script>',
            "",
            "</div>",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_global_category_index(
    category: str,
    entries: list[tuple[str, dict[str, Any]]],
    taxonomy: Taxonomy,
) -> str:
    label = taxonomy.label(category)
    lines = [
        "---",
        f"title: {_yaml_string(label + ' · 每日 arXiv')}",
        f"description: {_yaml_string(f'{label} 方向每日 arXiv 论文中文解读。')}",
        "---",
        "",
        f"# {label}",
        "",
        f"共收录 **{len(entries)}** 篇，按 arXiv 日榜日期倒序排列。",
        "",
    ]
    current_date = ""
    for _, item in entries:
        date_value = str(item.get("announcement_date", "未知日期"))
        if date_value != current_date:
            if current_date:
                lines.extend(["</div>", ""])
            lines.extend([f"## {date_value}", ""])
            lines.extend(['<div class="daily-paper-list" markdown="1">', ""])
            current_date = date_value
        path = str(item.get("path", ""))
        record = {
            "arxiv_id": _,
            "title": item.get("title", "未命名论文"),
            "announcement_date": date_value,
            "summary": item.get("summary", ""),
            "primary_category": item.get("primary_category", ""),
            "categories": item.get("categories", [item.get("primary_category", "")]),
        }
        lines.extend(
            [
                _paper_index_item(
                    record,
                    f"../../arxiv_daily/{path}",
                    taxonomy,
                    show_date=False,
                ),
                "",
            ]
        )
    if current_date:
        lines.extend(["</div>", ""])
    return "\n".join(lines).rstrip() + "\n"


def render_review_index(seen: dict[str, Any]) -> str:
    pending = [
        (arxiv_id, item)
        for arxiv_id, item in seen.items()
        if item.get("review_status") != "human_verified"
    ]
    pending.sort(
        key=lambda pair: (
            str(pair[1].get("announcement_date", "")),
            -float(pair[1].get("classification_confidence", 0.0)),
        ),
        reverse=True,
    )
    lines = [
        "---",
        "title: 人工审核队列",
        "description: 每日 arXiv AI 草稿的人工核验入口与自动检查问题。",
        "---",
        "",
        "# 人工审核",
        "",
        f"当前共有 **{len(pending)}** 篇待核验。优先检查带自动审核问题的页面。",
        "",
        '<div class="review-table" markdown="1">',
        "",
        "| 日期 | 论文 | 状态 | 置信度 | 自动检查 |",
        "|---|---|---|---:|---|",
    ]
    for arxiv_id, item in pending:
        issues = item.get("issues", [])
        issue_text = "；".join(str(issue) for issue in issues) if issues else "无结构性问题"
        path = str(item.get("path", ""))
        title = str(item.get("title", arxiv_id)).replace("|", "\\|")
        status = str(item.get("review_status", "ai_draft"))
        confidence = float(item.get("classification_confidence", 0.0))
        lines.append(
            f"| {item.get('announcement_date', '')} | [{title}](../arxiv_daily/{path}) "
            f"<br><code>{arxiv_id}</code> | `{status}` | {confidence:.2f} | {issue_text} |"
        )
    lines.extend(["", "</div>", ""])
    return "\n".join(lines)
