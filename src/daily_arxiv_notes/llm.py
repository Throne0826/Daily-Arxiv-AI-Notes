from __future__ import annotations

import http.client
import json
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

from .io_utils import atomic_write_json, load_json
from .models import Classification, FullText, GeneratedNote, Paper
from .taxonomy import Taxonomy


class LlmError(RuntimeError):
    pass


def _chat_completions_url(base_url: str) -> str:
    endpoint = base_url.rstrip("/")
    if endpoint.endswith("/chat/completions"):
        return endpoint
    if not re.search(r"/v\d+$", endpoint, re.IGNORECASE):
        endpoint += "/v1"
    return endpoint + "/chat/completions"


def _extract_json(content: str) -> dict[str, Any]:
    content = content.strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
    try:
        value = json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}")
        if start < 0 or end <= start:
            raise LlmError("model response did not contain a JSON object")
        value = json.loads(content[start : end + 1])
    if not isinstance(value, dict):
        raise LlmError("model response must be a JSON object")
    return value


def _content_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            item.get("text", "") for item in content if isinstance(item, dict)
        )
    return ""


def _extract_stream_content(lines: Any) -> str:
    parts: list[str] = []
    for raw_line in lines:
        line = raw_line.decode("utf-8").strip()
        if not line.startswith("data:"):
            continue
        payload = line[5:].strip()
        if payload == "[DONE]":
            break
        event = json.loads(payload)
        choice = (event.get("choices") or [{}])[0]
        delta = choice.get("delta") or choice.get("message") or {}
        parts.append(_content_text(delta.get("content")))
    return "".join(parts)


class JsonChatClient:
    def __init__(
        self,
        base_url: str,
        model: str,
        api_key: str,
        temperature: float = 0.1,
        timeout_seconds: int = 180,
        max_output_tokens: int = 8192,
        reasoning_effort: str = "",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.timeout_seconds = timeout_seconds
        self.max_output_tokens = max_output_tokens
        self.reasoning_effort = reasoning_effort.strip()

    @property
    def available(self) -> bool:
        return bool(self.base_url and self.model)

    def chat_json(
        self,
        system: str,
        user: str,
        retries: int = 3,
        max_output_tokens: int | None = None,
        timeout_seconds: int | None = None,
    ) -> dict[str, Any]:
        if not self.available:
            raise LlmError("LLM endpoint is not configured")
        endpoint = _chat_completions_url(self.base_url)
        request_body = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": max_output_tokens or self.max_output_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "response_format": {"type": "json_object"},
            "stream": True,
        }
        if self.reasoning_effort:
            request_body["reasoning_effort"] = self.reasoning_effort
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        last_error: Exception | None = None
        for attempt in range(retries):
            payload = json.dumps(request_body, ensure_ascii=False).encode("utf-8")
            request = urllib.request.Request(endpoint, data=payload, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(
                    request,
                    timeout=timeout_seconds or self.timeout_seconds,
                ) as response:
                    content_type = response.headers.get("Content-Type", "").casefold()
                    if "text/event-stream" in content_type:
                        content = _extract_stream_content(response)
                    else:
                        body = json.loads(response.read().decode("utf-8"))
                        content = _content_text(body["choices"][0]["message"]["content"])
                return _extract_json(content)
            except urllib.error.HTTPError as exc:
                last_error = exc
                if exc.code in (400, 422) and "response_format" in request_body:
                    request_body.pop("response_format")
                if attempt + 1 < retries:
                    time.sleep(2**attempt)
            except (
                KeyError,
                json.JSONDecodeError,
                urllib.error.URLError,
                LlmError,
                http.client.HTTPException,
                TimeoutError,
                ConnectionError,
                OSError,
            ) as exc:
                last_error = exc
                if attempt + 1 < retries:
                    time.sleep(2**attempt)
        raise LlmError(f"LLM request failed: {last_error}")


class LlmClassifier:
    def __init__(
        self,
        client: JsonChatClient,
        taxonomy: Taxonomy,
        minimum_confidence: float = 0.6,
        max_categories: int = 4,
    ) -> None:
        self.client = client
        self.taxonomy = taxonomy
        self.minimum_confidence = minimum_confidence
        self.max_categories = max_categories

    def classify_batch(self, papers: list[Paper]) -> dict[str, Classification]:
        system = (
            "You triage daily arXiv papers into a fixed AI taxonomy. Classify the paper's "
            "research contribution, not merely its application nouns. Return strict JSON only. "
            "Use multiple categories only when each is central. Do not invent categories."
        )
        request = {
            "taxonomy": self.taxonomy.prompt_catalog(),
            "papers": [
                {
                    "arxiv_id": paper.arxiv_id,
                    "title": paper.title,
                    "abstract": paper.abstract,
                    "subjects": paper.subjects,
                }
                for paper in papers
            ],
            "output_schema": {
                "results": [
                    {
                        "arxiv_id": "string",
                        "relevant": "boolean",
                        "primary_category": "taxonomy id or empty",
                        "categories": ["taxonomy ids"],
                        "confidence": "number from 0 to 1",
                        "reason": "one concise sentence",
                    }
                ]
            },
        }
        response = self.client.chat_json(
            system,
            json.dumps(request, ensure_ascii=False),
            retries=2,
            max_output_tokens=max(1024, min(2048, len(papers) * 240 + 256)),
            timeout_seconds=min(self.client.timeout_seconds, 90),
        )
        output: dict[str, Classification] = {}
        for item in response.get("results", []):
            if not isinstance(item, dict):
                continue
            arxiv_id = str(item.get("arxiv_id", ""))
            categories = [
                value
                for value in item.get("categories", [])
                if isinstance(value, str) and self.taxonomy.valid_category(value)
            ][: self.max_categories]
            primary = str(item.get("primary_category", ""))
            if primary not in categories:
                if self.taxonomy.valid_category(primary):
                    categories.insert(0, primary)
                elif categories:
                    primary = categories[0]
            confidence = max(0.0, min(1.0, float(item.get("confidence", 0.0))))
            relevant = bool(item.get("relevant")) and bool(categories)
            if confidence < self.minimum_confidence:
                relevant = False
            output[arxiv_id] = Classification(
                relevant=relevant,
                primary_category=primary if relevant else "",
                categories=categories if relevant else [],
                confidence=confidence,
                reason=str(item.get("reason", "")),
                source="llm",
            )
        return output


NOTE_SYSTEM_PROMPT = """You are a rigorous Chinese research-paper teacher and analyst. Read the supplied
paper chapters and return strict JSON. The intended reader is an advanced undergraduate who may have no
background in this exact subfield. Write professional but concise Chinese. Introduce only the technical terms
needed to understand this paper, and explain important designs in plain language after the technical account.

Organize the analysis around four distinct questions: research background, research motivation, research
method, and experiments. Background establishes the field, prerequisites, problem setup, and notation.
Motivation explains why existing approaches are insufficient and what precise research gap remains. Method
must describe the end-to-end pipeline with inputs, operations, and outputs. Experiments must explain what each
dataset, baseline, metric, result, and ablation is testing, rather than merely copying a score table.

Prioritize decision-relevant information. Do not write a broad field history, repeat the abstract in different
words, enumerate minor implementation details, or restate the same contribution across sections. Keep prose
fields to one or two compact paragraphs. Respect every list limit in the task constraints. Across all four
sections, target roughly 4,000 to 7,000 Chinese characters, excluding evidence quotes and equations.

Do not omit equations that are central to the method or objective. Copy their mathematical meaning faithfully
into LaTeX without surrounding dollar delimiters, define every symbol, cite the source location, and give an
intuitive Chinese explanation. For a survey, dataset paper, or method without a central equation, return an
empty equations list instead of inventing one. Never invent metrics, baselines, datasets, equations, URLs,
venues, or conclusions.

In every prose field, enclose inline mathematical notation in single dollar delimiters, for example
`$D_{\\mathrm{task}}$`, `$s(x)\\in\\{\\mathrm{task},\\mathrm{harm}\\}$`, and `$T_d$`. Never leave LaTeX
commands, subscripts, or superscripts bare in prose. The `latex` value inside an equations item and each
notation `symbol` are the only exceptions: keep those values free of surrounding dollar delimiters.

Every numerical claim in a main-result or ablation row must include a short verbatim evidence quote and its
table, figure, or section location when available. Evidence quotes must be copied from the supplied source in
the source language. If the source does not report something, write '原文未明确报告'. Clearly separate author
claims from analytical interpretation. This is a detailed AI draft that still requires source checking."""


@dataclass(slots=True)
class _PaperChapter:
    title: str
    text: str
    index: int


_SECTION_MARKER_RE = re.compile(r"^\[SECTION level=(\d+)\]\s+(.+?)\s*$", re.IGNORECASE)
_NUMBERED_HEADING_RE = re.compile(
    r"^(?P<number>(?:\d+(?:\.\d+)*|[A-Z](?:\.\d+)+))[.)]?\s+(?P<title>\S.*)$"
)
_CANONICAL_HEADING_RE = re.compile(
    r"^(?:abstract|introduction|background|related work|preliminaries|method(?:ology)?|"
    r"approach|framework|experiments?|experimental setup|evaluation|results?|"
    r"ablations?(?: and analysis)?|analysis|conclusion|limitations?|references|appendix)$",
    re.IGNORECASE,
)


def _heading(line: str) -> tuple[int, str] | None:
    stripped = " ".join(line.strip().split())
    marker = _SECTION_MARKER_RE.fullmatch(stripped)
    if marker:
        level = int(marker.group(1))
        title = marker.group(2)
        # Abstract is an h6 in arXiv HTML but semantically behaves like a chapter.
        return (2 if title.casefold() == "abstract" else level, title)

    if len(stripped) > 140 or stripped.endswith(('.', ',', ';', ':')):
        return None
    numbered = _NUMBERED_HEADING_RE.fullmatch(stripped)
    if numbered and re.search(r"[A-Za-z]", numbered.group("title")):
        number = numbered.group("number")
        return (number.count(".") + 1, stripped)
    if _CANONICAL_HEADING_RE.fullmatch(stripped):
        return (1, stripped)
    if re.fullmatch(r"Appendix\s+[A-Z](?:\s+.+)?", stripped, re.IGNORECASE):
        return (1, stripped)
    return None


def _paper_chapters(text: str) -> list[_PaperChapter]:
    lines = text.splitlines()
    headings = [
        (index, *parsed)
        for index, line in enumerate(lines)
        if (parsed := _heading(line)) is not None
    ]
    if not headings:
        return []

    has_markers = any(_SECTION_MARKER_RE.fullmatch(line.strip()) for line in lines)
    top_level = 2 if has_markers else min(level for _, level, _ in headings)
    starts = [
        (line_index, title)
        for line_index, level, title in headings
        if level <= top_level
    ]
    chapters: list[_PaperChapter] = []
    for chapter_index, (start, title) in enumerate(starts):
        end = starts[chapter_index + 1][0] if chapter_index + 1 < len(starts) else len(lines)
        chapter_text = "\n".join(lines[start:end]).strip()
        if chapter_text:
            chapters.append(_PaperChapter(title=title, text=chapter_text, index=chapter_index))
    return chapters


def _clean_heading_title(title: str) -> str:
    title = _SECTION_MARKER_RE.sub(r"\2", title)
    title = re.sub(r"^(?:\d+(?:\.\d+)*|[A-Z](?:\.\d+)*)[.)]?\s+", "", title)
    return title.casefold()


def _chapter_score(
    chapter: _PaperChapter,
    section_name: str,
    keywords: tuple[str, ...],
    intro_index: int | None,
    experiment_index: int | None,
) -> float:
    title = _clean_heading_title(chapter.title)
    body_head = chapter.text[:4000].casefold()
    keyword_score = sum(title.count(keyword.casefold()) * 4 for keyword in keywords)
    keyword_score += min(4, sum(body_head.count(keyword.casefold()) for keyword in keywords))

    is_abstract = title == "abstract"
    is_intro = "introduction" in title
    is_background = any(word in title for word in ("background", "preliminar"))
    is_related = "related work" in title
    is_appendix = title.startswith("appendix")
    is_experiment = any(
        word in title
        for word in ("experiment", "evaluation", "benchmark", "result", "ablation", "analysis")
    )
    is_backmatter = any(
        word in title for word in ("conclusion", "limitation", "ethical", "reference")
    )
    is_method = any(
        word in title
        for word in ("method", "approach", "framework", "algorithm", "architecture", "training")
    )

    role_score = 0.0
    if section_name in ("background", "background_core", "background_setup"):
        if is_abstract:
            role_score = 100 if section_name != "background_setup" else 0
        elif is_intro:
            role_score = 95
        elif is_background:
            role_score = 92
        elif is_related and section_name != "background_core":
            role_score = 88
    elif section_name in ("motivation", "motivation_problem", "motivation_gap"):
        if is_abstract or is_intro:
            role_score = 100
        elif "limitation" in title and section_name != "motivation_problem":
            role_score = 80
        elif "conclusion" in title and section_name != "motivation_problem":
            role_score = 45
    elif section_name == "method":
        if is_appendix and any(
            word in title for word in ("algorithm", "method", "training", "implementation")
        ):
            role_score = 75
        elif is_method and not is_experiment:
            role_score = 100
        elif (
            intro_index is not None
            and chapter.index > intro_index
            and (experiment_index is None or chapter.index < experiment_index)
            and not (is_related or is_backmatter)
        ):
            # Method chapters are often named after the paper itself, e.g. "2 PilotRL".
            role_score = 96
    elif section_name in ("experiments", "experiments_main", "experiments_analysis"):
        if is_appendix and any(
            word in title for word in ("experiment", "dataset", "baseline", "evaluation")
        ) and section_name == "experiments":
            role_score = 80
        elif (
            any(word in title for word in ("experiment", "evaluation", "benchmark"))
            and section_name != "experiments_analysis"
        ):
            role_score = 120
        elif (
            any(word in title for word in ("result", "ablation", "analysis"))
            and section_name != "experiments_main"
        ):
            role_score = 105
    # Once headings are available, chapter roles are authoritative. Body keyword
    # hits only refine the ordering among structurally relevant chapters.
    return role_score + keyword_score if role_score > 0 else 0


def _keyword_excerpt(
    text: str,
    keywords: tuple[str, ...],
    max_chars: int,
    chunk_size: int = 3600,
    overlap: int = 320,
) -> str:
    """Select ordered source chunks relevant to one analysis section."""
    if len(text) <= max_chars:
        return text
    step = max(1, chunk_size - overlap)
    chunks = [text[start : start + chunk_size] for start in range(0, len(text), step)]
    lowered_keywords = tuple(keyword.casefold() for keyword in keywords)
    scored: list[tuple[float, int]] = []
    for index, chunk in enumerate(chunks):
        lowered = chunk.casefold()
        score = sum(lowered.count(keyword) for keyword in lowered_keywords)
        if re.search(r"(?:equation|objective|loss|reward|theorem|公式|损失|奖励)", lowered):
            score += 1.5
        scored.append((score, index))

    selected = {0, 1, max(0, len(chunks) - 2), len(chunks) - 1}
    used = sum(len(chunks[index]) for index in selected)
    for _, index in sorted(scored, key=lambda item: (-item[0], item[1])):
        if index in selected:
            continue
        if used + len(chunks[index]) > max_chars:
            continue
        selected.add(index)
        used += len(chunks[index])
    return "\n\n[... source excerpt boundary ...]\n\n".join(
        chunks[index] for index in sorted(selected)
    )[:max_chars]


def _relevant_excerpt(
    text: str,
    section_name: str,
    keywords: tuple[str, ...],
    max_chars: int,
) -> str:
    """Select complete, relevant paper chapters and preserve their source order."""
    chapters = _paper_chapters(text)
    if not chapters:
        return _keyword_excerpt(text, keywords, max_chars)

    intro_index = next(
        (chapter.index for chapter in chapters if "introduction" in _clean_heading_title(chapter.title)),
        None,
    )
    experiment_index = next(
        (
            chapter.index
            for chapter in chapters
            if any(
                word in _clean_heading_title(chapter.title)
                for word in ("experiment", "evaluation", "benchmark")
            )
        ),
        None,
    )
    ranked = sorted(
        (
            (
                _chapter_score(
                    chapter,
                    section_name,
                    keywords,
                    intro_index,
                    experiment_index,
                ),
                chapter,
            )
            for chapter in chapters
        ),
        key=lambda item: (-item[0], item[1].index),
    )

    selected: list[_PaperChapter] = []
    used = 0
    for score, chapter in ranked:
        if score <= 0:
            continue
        separator_size = 52 if selected else 0
        if used + separator_size + len(chapter.text) <= max_chars:
            selected.append(chapter)
            used += separator_size + len(chapter.text)
        elif not selected:
            selected.append(
                _PaperChapter(
                    title=chapter.title,
                    text=chapter.text[:max_chars],
                    index=chapter.index,
                )
            )
            break

    if not selected:
        return _keyword_excerpt(text, keywords, max_chars)
    selected.sort(key=lambda chapter: chapter.index)
    return "\n\n[... next selected paper chapter ...]\n\n".join(
        chapter.text for chapter in selected
    )


def _deep_merge(target: dict[str, Any], incoming: dict[str, Any]) -> None:
    for key, value in incoming.items():
        current = target.get(key)
        if isinstance(current, dict) and isinstance(value, dict):
            _deep_merge(current, value)
        else:
            target[key] = value


def _cached_section_is_usable(task_name: str, section: dict[str, Any]) -> bool:
    if task_name not in {"experiment_main_results", "experiments"}:
        return True
    rows = section.get("experiments", {}).get("main_results", [])
    for row in rows:
        if not isinstance(row, dict):
            continue
        words = re.findall(r"\w+", str(row.get("evidence_quote", "")).casefold())
        if len(words) >= 8 and words[-1] in {
            "a",
            "an",
            "and",
            "between",
            "for",
            "of",
            "or",
            "the",
            "to",
            "with",
        }:
            return False
    return True


class NoteGenerator:
    def __init__(self, client: JsonChatClient) -> None:
        self.client = client

    def generate(
        self,
        paper: Paper,
        full_text: FullText,
        checkpoint_path: Path | None = None,
    ) -> GeneratedNote:
        paper_context = paper.to_dict()
        section_specs = [
            (
                "background",
                "background",
                ("introduction", "background", "related work", "preliminaries", "notation"),
                14000,
                1200,
                {
                    "background": {
                        "field_overview": "one compact paragraph on the minimum field context needed for this paper",
                        "prerequisite_concepts": [
                            {"term": "technical term", "explanation": "beginner-friendly Chinese explanation"}
                        ],
                        "problem_setup": "concise task definition: inputs, outputs, assumptions, and setting",
                        "notation": [
                            {"symbol": "LaTeX symbol without dollar delimiters", "meaning": "Chinese meaning"}
                        ],
                    },
                    "related_work": [{"work": "string", "relationship": "string"}],
                    "keywords": ["string"],
                    "code_url": "verified URL from source or empty",
                    "project_url": "verified URL from source or empty",
                },
            ),
            (
                "motivation",
                "motivation",
                ("introduction", "motivation", "limitation", "challenge", "we propose", "contribution"),
                12000,
                1200,
                {
                    "one_sentence_summary": "string",
                    "plain_language_problem": "one short paragraph explaining the problem without jargon",
                    "contributions": ["specific contribution in Chinese"],
                    "motivation": {
                        "practical_problem": "real or scientific problem that creates demand for this research",
                        "existing_approaches": [
                            {"name": "approach family or named method", "how_it_works": "concise Chinese explanation"}
                        ],
                        "limitations_of_existing": ["specific limitation and its consequence"],
                        "research_gap": "the unresolved gap after prior work",
                        "core_question": "the exact research question answered by this paper",
                        "intuition": "why the authors' entry point may work, explained intuitively",
                    },
                },
            ),
            (
                "method",
                "method",
                ("method", "approach", "framework", "algorithm", "training", "inference", "objective", "loss", "equation"),
                26000,
                2200,
                {
                    "method": {
                        "overview": "compact end-to-end overview, technically accurate and then intuitive",
                        "pipeline_steps": [
                            {
                                "name": "step name",
                                "input": "input to this step",
                                "operation": "technical operation",
                                "output": "output of this step",
                                "plain_explanation": "beginner-friendly analogy or explanation",
                            }
                        ],
                        "key_modules": [
                            {
                                "name": "module name",
                                "technical_detail": "architecture or algorithm detail",
                                "plain_explanation": "why it is needed in plain Chinese",
                            }
                        ],
                        "equations": [
                            {
                                "name": "equation or objective name",
                                "latex": "faithful LaTeX without surrounding dollar delimiters",
                                "symbols": [{"symbol": "LaTeX symbol", "meaning": "Chinese definition"}],
                                "plain_explanation": "what the equation is doing and why it matters",
                                "source_location": "equation number or section",
                            }
                        ],
                        "training_objective": "how the objective connects to optimization; or not applicable",
                        "training_or_inference": "complete training and inference procedure",
                        "implementation_details": "only implementation details needed to reproduce or fairly interpret results",
                    }
                },
            ),
            (
                "experiments",
                "experiments",
                ("experiment", "evaluation", "result", "baseline", "dataset", "metric", "ablation", "appendix"),
                20000,
                1800,
                {
                    "experiments": {
                        "research_questions": ["question the experiment is designed to answer"],
                        "setup": {
                            "datasets": ["dataset, scale, split, and role"],
                            "baselines": ["baseline and why it is a meaningful comparison"],
                            "metrics": [
                                {"name": "metric", "meaning": "what it measures", "better_when": "higher/lower and why"}
                            ],
                            "implementation": "evaluation protocol and reported implementation details",
                        },
                        "main_results": [
                            {
                                "setting": "string",
                                "result": "string",
                                "plain_explanation": "what this result means and what it does not prove",
                                "evidence_quote": "short verbatim source quote",
                                "source_location": "table, figure, or section when available",
                            }
                        ],
                        "key_findings": ["string"],
                        "ablations": [
                            {
                                "setting": "string",
                                "result": "string",
                                "plain_explanation": "what component this isolates and how to interpret the change",
                                "evidence_quote": "short verbatim source quote",
                                "source_location": "table, figure, or section when available",
                            }
                        ],
                        "case_studies": ["qualitative result and its interpretation"],
                    },
                    "limitations": ["string"],
                },
            ),
        ]

        task_constraints = {
            "background": [
                "Explain at most 3 prerequisite concepts; each explanation must be no more than 2 sentences.",
                "Include at most 4 notation entries and 2 directly relevant prior works.",
                "Do not include a general history unless it is required to understand the paper's problem setup.",
            ],
            "motivation": [
                "Return at most 2 contributions, 2 existing approach families, and 2 concrete limitations.",
                "Do not repeat the same point in practical_problem, research_gap, core_question, and intuition.",
            ],
            "method": [
                "Return 3 to 5 pipeline steps, at most 3 key modules, and at most 2 central equations.",
                "Omit routine implementation details and minor formulas.",
                "Keep each operation and plain-language explanation to no more than 2 sentences.",
            ],
            "experiments": [
                "Return at most 2 research questions, 3 datasets, 4 baselines, and 3 metrics.",
                "Return exactly the 3 most central non-duplicate main results when available, and at most 2 decisive ablations.",
                "Return at most 1 case study and 2 limitations.",
                "Each evidence_quote must be a complete source sentence or complete table row; never return a cut-off fragment.",
            ],
        }

        digest = sha256(full_text.text.encode("utf-8")).hexdigest()
        checkpoint: dict[str, Any] = {
            "version": 3,
            "source_sha256": digest,
            "generator_model": self.client.model,
            "completed": {},
        }
        if checkpoint_path is not None:
            stored = load_json(checkpoint_path, {})
            if (
                isinstance(stored, dict)
                and stored.get("version") == checkpoint["version"]
                and stored.get("source_sha256") == digest
                and stored.get("generator_model") == self.client.model
                and isinstance(stored.get("completed"), dict)
            ):
                checkpoint = stored

        completed: dict[str, Any] = checkpoint["completed"]
        content: dict[str, Any] = {}
        total_tasks = len(section_specs)
        for task_index, (
            task_name,
            source_section,
            keywords,
            max_chars,
            max_tokens,
            output_schema,
        ) in enumerate(section_specs, start=1):
            excerpt = _relevant_excerpt(
                full_text.text,
                source_section,
                keywords,
                max_chars=max_chars,
            )
            section = completed.get(task_name)
            if isinstance(section, dict) and not _cached_section_is_usable(task_name, section):
                completed.pop(task_name, None)
                section = None
            if isinstance(section, dict):
                print(
                    f"[{paper.arxiv_id}] reuse {task_index}/{total_tasks}: {task_name}",
                    file=sys.stderr,
                    flush=True,
                )
            else:
                print(
                    f"[{paper.arxiv_id}] generate {task_index}/{total_tasks}: {task_name} "
                    f"({len(excerpt)} source chars)",
                    file=sys.stderr,
                    flush=True,
                )
                request = {
                    "paper": paper_context,
                    "full_text_source": full_text.source,
                    "analysis_section": task_name,
                    "source_excerpt": excerpt,
                    "source_selection": (
                        "Complete relevant chapters selected from the paper's heading hierarchy; "
                        "unrelated chapters may be omitted."
                    ),
                    "output_schema": output_schema,
                    "task_constraints": task_constraints[task_name],
                }
                section = self.client.chat_json(
                    NOTE_SYSTEM_PROMPT
                    + f"\nReturn only the requested {task_name} fields. Do not discuss other tasks.",
                    json.dumps(request, ensure_ascii=False),
                    retries=2,
                    max_output_tokens=max_tokens,
                    timeout_seconds=min(self.client.timeout_seconds, 300),
                )
                completed[task_name] = section
                if checkpoint_path is not None:
                    atomic_write_json(checkpoint_path, checkpoint)
                print(
                    f"[{paper.arxiv_id}] completed {task_index}/{total_tasks}: {task_name}",
                    file=sys.stderr,
                    flush=True,
                )
            _deep_merge(content, section)

        content.setdefault("related_work", [])
        content.setdefault("keywords", [])
        content.setdefault("code_url", "")
        content.setdefault("project_url", "")
        return GeneratedNote(
            content=content,
            generator_model=self.client.model,
            review_status="ai_draft",
            source_sha256=digest,
        )


def metadata_only_note(paper: Paper) -> GeneratedNote:
    digest = sha256((paper.title + "\n" + paper.abstract).encode("utf-8")).hexdigest()
    content = {
        "one_sentence_summary": paper.abstract or "原文摘要尚未成功获取。",
        "plain_language_problem": "待配置兼容模型后从论文全文生成。",
        "contributions": [],
        "background": {
            "field_overview": "待配置兼容模型后从论文全文生成。",
            "prerequisite_concepts": [],
            "problem_setup": "原文未解析。",
            "notation": [],
        },
        "motivation": {
            "practical_problem": "待人工审核。",
            "existing_approaches": [],
            "limitations_of_existing": [],
            "research_gap": "待人工审核。",
            "core_question": "待人工审核。",
            "intuition": "待人工审核。",
        },
        "method": {
            "overview": "当前为 metadata-only 草稿，未调用生成模型。",
            "pipeline_steps": [],
            "key_modules": [],
            "equations": [],
            "training_objective": "原文未解析。",
            "training_or_inference": "原文未解析。",
            "implementation_details": "原文未解析。",
        },
        "experiments": {
            "research_questions": [],
            "setup": {"datasets": [], "baselines": [], "metrics": [], "implementation": "原文未解析。"},
            "main_results": [],
            "ablations": [],
            "case_studies": [],
            "key_findings": [],
        },
        "limitations": ["该页面是元数据草稿，不能作为论文结论引用。"],
        "related_work": [],
        "keywords": [],
        "code_url": "",
        "project_url": "",
    }
    return GeneratedNote(
        content=content,
        generator_model="none",
        review_status="metadata_only",
        source_sha256=digest,
    )
