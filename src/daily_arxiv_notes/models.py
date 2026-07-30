from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class Paper:
    arxiv_id: str
    title: str
    abstract: str = ""
    authors: list[str] = field(default_factory=list)
    affiliations: list[str] = field(default_factory=list)
    subjects: list[str] = field(default_factory=list)
    primary_subject: str = ""
    published: str = ""
    updated: str = ""
    announcement_date: str = ""
    comments: str = ""
    doi: str = ""
    arxiv_url: str = ""
    pdf_url: str = ""
    source_categories: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Paper":
        allowed = cls.__dataclass_fields__.keys()
        return cls(**{key: value[key] for key in allowed if key in value})


@dataclass(slots=True)
class Classification:
    relevant: bool
    primary_category: str = ""
    categories: list[str] = field(default_factory=list)
    confidence: float = 0.0
    reason: str = ""
    source: str = "rules"
    rule_scores: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Classification":
        allowed = cls.__dataclass_fields__.keys()
        return cls(**{key: value[key] for key in allowed if key in value})


@dataclass(slots=True)
class FullText:
    text: str
    source: str
    links: list[str] = field(default_factory=list)


@dataclass(slots=True)
class GeneratedNote:
    content: dict[str, Any]
    generator_model: str
    review_status: str
    source_sha256: str
