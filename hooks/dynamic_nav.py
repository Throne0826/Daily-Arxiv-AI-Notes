"""Build the Paper-Notes-style navigation from taxonomy and generated state."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_navigation(taxonomy: dict[str, Any], state: dict[str, Any]) -> list[dict[str, Any]]:
    seen = state.get("seen", {})
    dates = sorted(
        {
            str(item.get("announcement_date", ""))
            for item in seen.values()
            if item.get("announcement_date")
        },
        reverse=True,
    )
    daily_nav: list[dict[str, Any]] = [{"每日论文": "arxiv_daily/index.md"}]
    daily_counts = {
        date: sum(1 for item in seen.values() if item.get("announcement_date") == date)
        for date in dates
    }
    daily_nav.extend(
        {f"{date}（{daily_counts[date]}）": f"arxiv_daily/{date}/index.md"}
        for date in dates
    )

    categories = taxonomy.get("categories", {})
    category_counts = {category: 0 for category in categories}
    for item in seen.values():
        primary = str(item.get("primary_category", ""))
        paper_categories = set(item.get("categories", [primary]))
        for category in paper_categories:
            if category in category_counts:
                category_counts[category] += 1
    field_nav: list[dict[str, Any]] = [{"关注领域": "categories/index.md"}]
    for group in taxonomy.get("groups", {}).values():
        group_nav = []
        group_categories = set(group.get("categories", []))
        group_count = sum(
            1
            for item in seen.values()
            if group_categories.intersection(
                set(item.get("categories", [item.get("primary_category", "")]))
            )
        )
        for category in group.get("categories", []):
            category_config = categories.get(category, {})
            label = str(category_config.get("label", category))
            counted_label = f"{label}（{category_counts.get(category, 0)}）"
            group_nav.append({counted_label: f"categories/{category}/index.md"})
        group_label = f"{str(group.get('label', '其他'))}（{group_count}）"
        field_nav.append({group_label: group_nav})

    return [
        {"首页": "index.md"},
        {"每日论文": daily_nav},
        {"关注领域": field_nav},
    ]


def on_config(config, **kwargs):
    config_path = Path(config.config_file_path).resolve()
    root = config_path.parent
    taxonomy = json.loads((root / "taxonomy.json").read_text(encoding="utf-8"))
    state_path = root / "data" / "state.json"
    state = (
        json.loads(state_path.read_text(encoding="utf-8"))
        if state_path.exists()
        else {"seen": {}}
    )
    config["nav"] = build_navigation(taxonomy, state)
    return config
