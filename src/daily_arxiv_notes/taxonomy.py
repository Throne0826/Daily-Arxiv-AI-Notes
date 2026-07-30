from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .models import Classification, Paper


def _normalize(value: str) -> str:
    value = value.lower().replace("_", "-")
    return re.sub(r"\s+", " ", value)


@dataclass(slots=True)
class Taxonomy:
    raw: dict[str, Any]

    @property
    def categories(self) -> dict[str, dict[str, Any]]:
        return self.raw["categories"]

    @property
    def groups(self) -> dict[str, dict[str, Any]]:
        return self.raw["groups"]

    def valid_category(self, name: str) -> bool:
        return name in self.categories

    def label(self, name: str) -> str:
        return self.categories[name]["label"]

    def group_for(self, category: str) -> str:
        for group_name, group in self.groups.items():
            if category in group["categories"]:
                return group_name
        raise KeyError(category)

    def prompt_catalog(self) -> list[dict[str, str]]:
        return [
            {
                "id": category_id,
                "label": value["label"],
                "description": value["description"],
            }
            for category_id, value in self.categories.items()
        ]


class RuleClassifier:
    def __init__(
        self,
        taxonomy: Taxonomy,
        minimum_score: float = 2.0,
        max_categories: int = 4,
    ) -> None:
        self.taxonomy = taxonomy
        self.minimum_score = minimum_score
        self.max_categories = max_categories

    def classify(self, paper: Paper) -> Classification:
        text = _normalize(" ".join([paper.title, paper.abstract, paper.comments]))
        scores: dict[str, float] = {}
        for category_id, category in self.taxonomy.categories.items():
            score = 0.0
            for phrase in category.get("strong_keywords", []):
                if _normalize(phrase) in text:
                    score += 3.0
            for phrase in category.get("keywords", []):
                if _normalize(phrase) in text:
                    score += 1.0
            for phrase in category.get("exclude_keywords", []):
                if _normalize(phrase) in text:
                    score -= 2.0
            if score > 0:
                scores[category_id] = score

        ranked = sorted(scores, key=lambda item: (-scores[item], item))
        selected = [
            category
            for category in ranked
            if scores[category] >= self.minimum_score
        ][: self.max_categories]
        if not selected:
            return Classification(
                relevant=False,
                confidence=0.0,
                reason="no taxonomy category reached the rule threshold",
                source="rules",
                rule_scores=scores,
            )
        best = scores[selected[0]]
        confidence = min(0.95, 0.45 + best / 12.0)
        return Classification(
            relevant=True,
            primary_category=selected[0],
            categories=selected,
            confidence=confidence,
            reason=f"matched taxonomy keywords; top rule score={best:.1f}",
            source="rules",
            rule_scores=scores,
        )
