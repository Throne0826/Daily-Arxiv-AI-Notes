from pathlib import Path

from hooks.dynamic_nav import build_navigation


def test_navigation_contains_fields_categories_and_primary_papers() -> None:
    taxonomy = {
        "groups": {
            "llm": {
                "label": "LLM",
                "categories": ["llm_reasoning", "llm_agent"],
            }
        },
        "categories": {
            "llm_reasoning": {"label": "LLM Reasoning"},
            "llm_agent": {"label": "LLM Agent"},
        },
    }
    state = {
        "seen": {
            "2607.00001": {
                "announcement_date": "2026-07-29",
                "title": "Planning Agents",
                "path": "2026-07-29/llm_agent/planning-agents.md",
                "primary_category": "llm_agent",
                "categories": ["llm_agent", "llm_reasoning"],
            }
        }
    }

    navigation = build_navigation(taxonomy, state)
    assert [next(iter(item)) for item in navigation] == ["首页", "每日论文", "关注领域"]
    daily = navigation[1]["每日论文"]
    fields = navigation[2]["关注领域"]
    llm_categories = fields[1]["LLM（1）"]
    agent_link = llm_categories[1]["LLM Agent（1）"]

    assert {"2026-07-29（1）": "arxiv_daily/2026-07-29/index.md"} in daily
    assert agent_link == "categories/llm_agent/index.md"
    assert llm_categories[0]["LLM Reasoning（1）"] == "categories/llm_reasoning/index.md"


def test_homepage_html_links_use_built_site_routes() -> None:
    homepage = (Path(__file__).resolve().parents[1] / "docs/index.md").read_text(
        encoding="utf-8"
    )

    assert 'href="arxiv_daily/"' in homepage
    assert 'href="categories/"' in homepage
    assert 'href="arxiv_daily/index.md"' not in homepage
    assert 'href="categories/index.md"' not in homepage
