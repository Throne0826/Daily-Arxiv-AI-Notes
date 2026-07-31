from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
from typing import Any

from .arxiv import ArxivClient, PoliteHttpClient
from .config import Settings
from .io_utils import append_jsonl, atomic_write_json, atomic_write_text, load_json
from .llm import JsonChatClient, LlmClassifier, LlmError, NoteGenerator, metadata_only_note
from .models import Classification, FullText, GeneratedNote, Paper
from .render import (
    render_categories_master,
    render_category_index,
    render_daily_index,
    render_daily_master,
    render_global_category_index,
    render_note,
    render_review_index,
    slugify,
    validate_generated_content,
    validate_rendered_note,
)
from .taxonomy import RuleClassifier, Taxonomy


class PipelineError(RuntimeError):
    pass


def _merge_dict(target: dict[str, Any], source: dict[str, Any]) -> None:
    for key, value in source.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            _merge_dict(target[key], value)
        else:
            target[key] = value


def _evidence_tokens(value: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", value).casefold().replace("\u00ad", "")
    return re.findall(r"\w+(?:\.\w+)*", normalized, flags=re.UNICODE)


def _quote_supported_by_source(quote: str, source_text: str) -> bool:
    needle = _evidence_tokens(quote)
    haystack = _evidence_tokens(source_text)
    if not needle:
        return False
    if len(needle) >= 8 and needle[-1] in {
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

    width = len(needle)
    for start in range(0, len(haystack) - width + 1):
        if haystack[start : start + width] == needle:
            return True

    # LaTeXML table extraction inserts column labels between cells. Permit a
    # tightly bounded ordered match, while still requiring every word and number.
    max_gap = 12
    max_span = max(32, width * 4)
    first = needle[0]
    for start, token in enumerate(haystack):
        if token != first:
            continue
        cursor = start
        matched = True
        for expected in needle[1:]:
            stop = min(len(haystack), cursor + max_gap + 1)
            next_index = next(
                (index for index in range(cursor + 1, stop) if haystack[index] == expected),
                None,
            )
            if next_index is None:
                matched = False
                break
            cursor = next_index
        if matched and cursor - start + 1 <= max_span:
            return True
    return False


class DailyPipeline:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.taxonomy = Taxonomy(settings.taxonomy)
        arxiv_config = settings.section("arxiv")
        contact = os.getenv("ARXIV_CONTACT_EMAIL", "").strip()
        user_agent = str(arxiv_config.get("user_agent", "daily-arxiv-notes/0.1"))
        if contact:
            user_agent = f"{user_agent}; contact={contact}"
        http = PoliteHttpClient(
            user_agent=user_agent,
            interval_seconds=float(arxiv_config.get("request_interval_seconds", 3.0)),
            timeout_seconds=int(arxiv_config.get("request_timeout_seconds", 90)),
        )
        self.arxiv = ArxivClient(
            http=http,
            page_size=int(arxiv_config.get("page_size", 100)),
            metadata_batch_size=int(arxiv_config.get("metadata_batch_size", 50)),
            include_crosslists=bool(arxiv_config.get("include_crosslists", True)),
            fallback_to_abs_metadata=bool(
                arxiv_config.get("fallback_to_abs_metadata", True)
            ),
        )
        api_key = settings.llm_value("api_key")
        base_url = settings.llm_value("base_url")
        if api_key and not base_url:
            base_url = "https://api.openai.com/v1"
        self.llm = JsonChatClient(
            base_url=base_url,
            model=settings.llm_value("model"),
            api_key=api_key,
            temperature=float(settings.section("llm").get("temperature", 0.1)),
            timeout_seconds=int(settings.section("llm").get("timeout_seconds", 180)),
            max_output_tokens=int(settings.section("llm").get("max_output_tokens", 8192)),
            reasoning_effort=str(settings.section("llm").get("reasoning_effort", "")),
        )

    def rerender(self, dates: list[str] | None = None) -> dict[str, Any]:
        """Rebuild Markdown from cached metadata and generation checkpoints only."""
        data_dir = self.settings.project_path("data_dir")
        output_dir = self.settings.project_path("output_dir")
        state_path = self.settings.project_path("state_file")
        state = load_json(state_path, {"version": 1, "seen": {}})
        seen: dict[str, Any] = state.get("seen", {})
        available_dates = sorted(
            {
                str(item.get("announcement_date", ""))
                for item in seen.values()
                if item.get("announcement_date")
            }
        )
        selected_dates = dates or available_dates
        unknown = [value for value in selected_dates if value not in available_dates]
        if unknown:
            raise PipelineError(f"no cached papers for: {', '.join(unknown)}")

        rendered = 0
        failures: list[dict[str, str]] = []
        for date_string in selected_dates:
            raw_dir = data_dir / "raw" / date_string
            papers_payload = load_json(raw_dir / "papers.json", [])
            papers = {
                paper.arxiv_id: paper
                for paper in (
                    Paper.from_dict(value)
                    for value in papers_payload
                    if isinstance(value, dict)
                )
            }
            classifications = load_json(raw_dir / "classifications.json", {})
            records: list[dict[str, Any]] = []
            prefix = f"{date_string}/"
            for arxiv_id, stored in seen.items():
                if stored.get("announcement_date") != date_string:
                    continue
                paper = papers.get(arxiv_id)
                path = str(stored.get("path", ""))
                if paper is None or not path.startswith(prefix):
                    failures.append(
                        {"arxiv_id": arxiv_id, "error": "cached metadata or output path missing"}
                    )
                    continue
                classification = self._classification_from_cache(
                    classifications.get(arxiv_id) if isinstance(classifications, dict) else None
                ) or self._classification_from_state(stored)
                if classification is None:
                    failures.append({"arxiv_id": arxiv_id, "error": "classification missing"})
                    continue

                checkpoint = load_json(raw_dir / "generation" / f"{arxiv_id}.json", {})
                if isinstance(checkpoint.get("completed"), dict):
                    content: dict[str, Any] = {}
                    for section in checkpoint["completed"].values():
                        if isinstance(section, dict):
                            _merge_dict(content, section)
                    generated = GeneratedNote(
                        content=content,
                        generator_model=str(checkpoint.get("generator_model", "cached")),
                        review_status=str(stored.get("review_status", "ai_draft")),
                        source_sha256=str(checkpoint.get("source_sha256", "")),
                    )
                elif stored.get("review_status") == "metadata_only":
                    generated = metadata_only_note(paper)
                else:
                    failures.append({"arxiv_id": arxiv_id, "error": "generation checkpoint missing"})
                    continue

                relative_path = Path(path[len(prefix) :])
                atomic_write_text(
                    output_dir / date_string / relative_path,
                    render_note(paper, classification, generated, self.taxonomy),
                )
                records.append(
                    {
                        "arxiv_id": arxiv_id,
                        "paper": paper,
                        "classification": classification,
                        "path": relative_path.as_posix(),
                        "summary": generated.content.get("one_sentence_summary", ""),
                        "review_status": generated.review_status,
                        "issues": stored.get("issues", []),
                    }
                )
                rendered += 1
            records.sort(
                key=lambda record: (
                    record["classification"].primary_category,
                    record["paper"].title,
                )
            )
            self._write_indexes(output_dir / date_string, date_string, records, seen)
        return {"dates": selected_dates, "rendered": rendered, "failures": failures}

    def run(
        self,
        requested_date: date | None = None,
        max_papers: int | None = None,
        metadata_only: bool = False,
        require_llm: bool = False,
        force: bool = False,
        paper_ids: set[str] | None = None,
    ) -> dict[str, Any]:
        if (require_llm or not metadata_only) and not self.llm.available:
            raise PipelineError(
                "Full-text note generation requires OPENAI_BASE_URL and OPENAI_MODEL. "
                "Use --metadata-only only for an explicit smoke test."
            )

        data_dir = self.settings.project_path("data_dir")
        output_dir = self.settings.project_path("output_dir")
        arxiv_config = self.settings.section("arxiv")
        requested_cache_path = (
            data_dir / "raw" / requested_date.isoformat() / "papers.json"
            if requested_date is not None
            else None
        )
        use_cached_target = bool(
            requested_cache_path
            and requested_cache_path.exists()
            and (not force or paper_ids)
        )
        cached_target_date = requested_date if use_cached_target else None
        cached_target_path = requested_cache_path if use_cached_target else None
        if cached_target_path is not None and cached_target_path.exists():
            announcement_date = cached_target_date
            listings = {}
        else:
            print("[arxiv] fetching daily listings", file=sys.stderr, flush=True)
            announcement_date, listings = self.arxiv.fetch_daily_listings(
                arxiv_config["categories"],
                requested_date=requested_date,
            )
            print(
                f"[arxiv] fetched {len(listings)} unique listings for "
                f"{announcement_date.isoformat()}",
                file=sys.stderr,
                flush=True,
            )
        date_string = announcement_date.isoformat()
        raw_dir = data_dir / "raw" / date_string
        daily_dir = output_dir / date_string
        papers_cache = raw_dir / "papers.json"
        if papers_cache.exists() and (not force or cached_target_path == papers_cache):
            papers = [
                Paper.from_dict(value)
                for value in json.loads(papers_cache.read_text(encoding="utf-8"))
            ]
        else:
            print("[arxiv] fetching paper metadata", file=sys.stderr, flush=True)
            papers = self.arxiv.fetch_metadata(listings, announcement_date)
            atomic_write_json(papers_cache, [paper.to_dict() for paper in papers])
            print(
                f"[arxiv] cached metadata for {len(papers)} papers",
                file=sys.stderr,
                flush=True,
            )

        state_path = self.settings.project_path("state_file")
        state = load_json(state_path, {"version": 1, "seen": {}})
        seen: dict[str, Any] = state.setdefault("seen", {})
        seen_before_run = set(seen)
        candidates = [
            paper
            for paper in papers
            if (paper_ids is None or paper.arxiv_id in paper_ids)
            and self._needs_processing(
                paper.arxiv_id,
                seen,
                force=force,
                metadata_only=metadata_only,
                llm_available=self.llm.available,
            )
        ]

        classification_path = raw_dir / "classifications.json"
        reused_classifications: dict[str, Classification] = {}
        if not force:
            cached_classifications = load_json(classification_path, {})
            if isinstance(cached_classifications, dict):
                for paper in candidates:
                    cached = cached_classifications.get(paper.arxiv_id)
                    classification = self._classification_from_cache(cached)
                    if classification is not None:
                        reused_classifications[paper.arxiv_id] = classification

        papers_to_classify = [
            paper for paper in candidates if paper.arxiv_id not in reused_classifications
        ]
        if force and paper_ids:
            papers_to_classify = []
            for paper in candidates:
                stored = seen.get(paper.arxiv_id, {})
                reused = self._classification_from_state(stored)
                if reused is not None:
                    reused_classifications[paper.arxiv_id] = reused
                else:
                    papers_to_classify.append(paper)

        if papers_to_classify:
            classifications, classification_errors = self._classify(papers_to_classify)
        else:
            classifications, classification_errors = {}, []
        classifications = {**reused_classifications, **classifications}
        classification_payload = load_json(classification_path, {})
        if not isinstance(classification_payload, dict):
            classification_payload = {}
        classification_payload.update(
            {
                arxiv_id: classification.to_dict()
                for arxiv_id, classification in classifications.items()
            }
        )
        atomic_write_json(classification_path, classification_payload)
        selected = [
            paper
            for paper in candidates
            if classifications.get(paper.arxiv_id, Classification(False)).relevant
        ]
        selected.sort(
            key=lambda paper: (
                classifications[paper.arxiv_id].confidence,
                paper.published,
                paper.updated,
                paper.arxiv_id,
            ),
            reverse=True,
        )
        relevant_total = len(selected)
        configured_max = int(self.settings.section("generation").get("max_papers_per_run", 0))
        effective_max = configured_max if max_papers is None else max_papers
        if effective_max and effective_max > 0:
            selected = selected[:effective_max]

        records: list[dict[str, Any]] = []
        failures: list[dict[str, str]] = []
        generation_config = self.settings.section("generation")
        full_texts: dict[str, FullText] = {}
        generation_candidates: list[Paper] = []
        if self.llm.available and not metadata_only:
            max_chars = int(generation_config.get("max_fulltext_chars", 90000))
            for index, paper in enumerate(selected, start=1):
                print(
                    f"[fulltext] fetch {index}/{len(selected)}: {paper.arxiv_id}",
                    file=sys.stderr,
                    flush=True,
                )
                try:
                    full_texts[paper.arxiv_id] = self.arxiv.fetch_full_text(
                        paper,
                        max_chars=max_chars,
                    )
                    generation_candidates.append(paper)
                except Exception as exc:
                    failures.append({"arxiv_id": paper.arxiv_id, "error": str(exc)})
        else:
            generation_candidates = selected

        configured_workers = max(1, int(generation_config.get("workers", 1)))
        worker_count = (
            min(configured_workers, len(generation_candidates))
            if self.llm.available and not metadata_only and generation_candidates
            else 1
        )
        if generation_candidates:
            print(
                f"[generation] {len(generation_candidates)} papers with {worker_count} worker(s)",
                file=sys.stderr,
                flush=True,
            )

        def commit(record: dict[str, Any]) -> None:
            paper = record["paper"]
            classification = record["classification"]
            relative_path = Path(record["path"])
            atomic_write_text(daily_dir / relative_path, record.pop("markdown"))
            previous_path = str(seen.get(paper.arxiv_id, {}).get("path", ""))
            new_state_path = f"{date_string}/{relative_path.as_posix()}"
            self._remove_stale_note(output_dir, previous_path, new_state_path)
            records.append(record)
            append_jsonl(
                self.settings.project_path("review_queue_file"),
                {
                    "arxiv_id": paper.arxiv_id,
                    "announcement_date": date_string,
                    "path": new_state_path,
                    "status": record["review_status"],
                    "classification_confidence": classification.confidence,
                    "issues": record["issues"],
                },
            )
            seen[paper.arxiv_id] = {
                "announcement_date": date_string,
                "path": new_state_path,
                "review_status": record["review_status"],
                "title": paper.title,
                "primary_category": classification.primary_category,
                "categories": classification.categories,
                "classification_confidence": classification.confidence,
                "summary": record["summary"],
                "issues": record["issues"],
            }
            atomic_write_json(state_path, state)

        if worker_count == 1:
            for paper in generation_candidates:
                try:
                    commit(
                        self._prepare_note(
                            paper,
                            classifications[paper.arxiv_id],
                            raw_dir,
                            metadata_only=metadata_only,
                            full_text=full_texts.get(paper.arxiv_id),
                        )
                    )
                except Exception as exc:  # Continue the daily batch and report this paper.
                    failures.append({"arxiv_id": paper.arxiv_id, "error": str(exc)})
        else:
            with ThreadPoolExecutor(
                max_workers=worker_count,
                thread_name_prefix="paper-note",
            ) as executor:
                futures = {
                    executor.submit(
                        self._prepare_note,
                        paper,
                        classifications[paper.arxiv_id],
                        raw_dir,
                        metadata_only=metadata_only,
                        full_text=full_texts[paper.arxiv_id],
                    ): paper
                    for paper in generation_candidates
                }
                for completed, future in enumerate(as_completed(futures), start=1):
                    paper = futures[future]
                    try:
                        commit(future.result())
                        print(
                            f"[generation] committed {completed}/{len(futures)}: "
                            f"{paper.arxiv_id}",
                            file=sys.stderr,
                            flush=True,
                        )
                    except Exception as exc:  # One worker failure must not stop the batch.
                        failures.append({"arxiv_id": paper.arxiv_id, "error": str(exc)})

        index_records = self._merge_index_records(date_string, records, seen)
        self._write_indexes(daily_dir, date_string, index_records, seen)
        manifest_path = raw_dir / "manifest.json"
        manifest = {
            "announcement_date": date_string,
            "fetched_unique": len(papers),
            "new_candidates": len(candidates),
            "relevant_total": relevant_total,
            "selected": len(selected),
            "generated": len(records),
            "generated_this_run": len(records),
            "daily_total": self._daily_total(seen, date_string),
            "metadata_only": metadata_only or not self.llm.available,
            "llm_model": self.llm.model if self.llm.available else "",
            "classification_errors": classification_errors,
            "failures": failures,
        }
        if paper_ids:
            previous_manifest = load_json(manifest_path, {})
            if (
                isinstance(previous_manifest, dict)
                and previous_manifest.get("announcement_date") == date_string
            ):
                retried_ids = set(paper_ids)
                previous_failures = [
                    failure
                    for failure in previous_manifest.get("failures", [])
                    if isinstance(failure, dict)
                    and failure.get("arxiv_id") not in retried_ids
                ]
                newly_generated = sum(
                    record.get("arxiv_id") not in seen_before_run for record in records
                )
                previous_manifest["generated"] = int(
                    previous_manifest.get("generated", 0)
                ) + newly_generated
                previous_manifest["generated_this_run"] = len(records)
                previous_manifest["daily_total"] = self._daily_total(seen, date_string)
                previous_manifest["failures"] = previous_failures + failures
                previous_manifest["llm_model"] = manifest["llm_model"]
                manifest = previous_manifest
        atomic_write_json(manifest_path, manifest)
        return manifest

    def _prepare_note(
        self,
        paper: Paper,
        classification: Classification,
        raw_dir: Path,
        *,
        metadata_only: bool,
        full_text: FullText | None = None,
    ) -> dict[str, Any]:
        issues: list[str] = []
        if self.llm.available and not metadata_only:
            if full_text is None:
                raise PipelineError(f"full text missing for {paper.arxiv_id}")
            generated = NoteGenerator(self.llm).generate(
                paper,
                full_text,
                checkpoint_path=raw_dir / "generation" / f"{paper.arxiv_id}.json",
            )
            issues.extend(self._sanitize_source_urls(generated, full_text.links, full_text.text))
            issues.extend(self._validate_evidence_quotes(generated, full_text.text))
        else:
            generated = metadata_only_note(paper)
        issues.extend(validate_generated_content(generated.content))
        filename = f"{slugify(paper.title, paper.arxiv_id)}.md"
        relative_path = Path(classification.primary_category) / filename
        markdown = render_note(paper, classification, generated, self.taxonomy)
        issues.extend(validate_rendered_note(markdown))
        return {
            "arxiv_id": paper.arxiv_id,
            "paper": paper,
            "classification": classification,
            "path": relative_path.as_posix(),
            "summary": generated.content.get("one_sentence_summary", ""),
            "review_status": generated.review_status,
            "issues": issues,
            "markdown": markdown,
        }

    @staticmethod
    def _daily_total(seen: dict[str, Any], date_string: str) -> int:
        return sum(
            1
            for value in seen.values()
            if isinstance(value, dict)
            and value.get("announcement_date") == date_string
            and value.get("path")
            and value.get("review_status") != "metadata_only"
        )

    def _classification_from_state(self, stored: dict[str, Any]) -> Classification | None:
        primary = str(stored.get("primary_category", ""))
        categories = [
            value
            for value in stored.get("categories", [primary])
            if isinstance(value, str) and self.taxonomy.valid_category(value)
        ]
        if not self.taxonomy.valid_category(primary) or not categories:
            return None
        if primary not in categories:
            categories.insert(0, primary)
        return Classification(
            relevant=True,
            primary_category=primary,
            categories=categories,
            confidence=float(stored.get("classification_confidence", 0.0)),
            reason="reused verified category during targeted regeneration",
            source="state",
        )

    def _classification_from_cache(self, stored: Any) -> Classification | None:
        if not isinstance(stored, dict) or "relevant" not in stored:
            return None
        classification = Classification.from_dict(stored)
        if not classification.relevant:
            classification.source = "cache"
            return classification
        categories = [
            category
            for category in classification.categories
            if self.taxonomy.valid_category(category)
        ]
        if not self.taxonomy.valid_category(classification.primary_category) or not categories:
            return None
        if classification.primary_category not in categories:
            categories.insert(0, classification.primary_category)
        classification.categories = categories
        classification.source = "cache"
        return classification

    @staticmethod
    def _remove_stale_note(
        output_dir: Path,
        previous_path: str,
        new_state_path: str,
    ) -> None:
        if not previous_path or previous_path == new_state_path:
            return
        stale_path = (output_dir / previous_path).resolve()
        if stale_path.is_relative_to(output_dir.resolve()):
            stale_path.unlink(missing_ok=True)

    @staticmethod
    def _needs_processing(
        arxiv_id: str,
        seen: dict[str, Any],
        *,
        force: bool,
        metadata_only: bool,
        llm_available: bool,
    ) -> bool:
        if force or arxiv_id not in seen:
            return True
        return (
            llm_available
            and not metadata_only
            and seen[arxiv_id].get("review_status") == "metadata_only"
        )

    @staticmethod
    def _merge_index_records(
        date_string: str,
        current: list[dict[str, Any]],
        seen: dict[str, Any],
    ) -> list[dict[str, Any]]:
        records = list(current)
        current_ids = {record["paper"].arxiv_id for record in current}
        prefix = f"{date_string}/"
        for arxiv_id, value in seen.items():
            if arxiv_id in current_ids or value.get("announcement_date") != date_string:
                continue
            title = str(value.get("title", "")).strip()
            primary = str(value.get("primary_category", "")).strip()
            path = str(value.get("path", ""))
            if not title or not primary or not path.startswith(prefix):
                continue
            categories = [
                item for item in value.get("categories", [primary]) if isinstance(item, str)
            ]
            records.append(
                {
                    "paper": Paper(arxiv_id=arxiv_id, title=title, announcement_date=date_string),
                    "classification": Classification(
                        relevant=True,
                        primary_category=primary,
                        categories=categories or [primary],
                        confidence=float(value.get("classification_confidence", 0.0)),
                        source="state",
                    ),
                    "path": path[len(prefix) :],
                    "summary": str(value.get("summary", "")),
                    "review_status": str(value.get("review_status", "")),
                    "issues": [],
                }
            )
        records.sort(key=lambda record: (record["classification"].primary_category, record["paper"].title))
        return records

    def _classify(self, papers: list[Paper]) -> tuple[dict[str, Classification], list[str]]:
        config = self.settings.section("classification")
        rule_classifier = RuleClassifier(
            self.taxonomy,
            minimum_score=float(config.get("minimum_rule_score", 2.0)),
            max_categories=int(config.get("max_categories_per_paper", 4)),
        )
        rule_results = {paper.arxiv_id: rule_classifier.classify(paper) for paper in papers}
        mode = str(config.get("mode", "hybrid")).lower()
        if mode == "rules":
            return rule_results, []
        if not self.llm.available:
            if mode == "llm":
                raise PipelineError("classification.mode=llm but no LLM endpoint is configured")
            return rule_results, ["LLM unavailable; used rule classification"]

        classifier = LlmClassifier(
            self.llm,
            self.taxonomy,
            minimum_confidence=float(config.get("minimum_llm_confidence", 0.6)),
            max_categories=int(config.get("max_categories_per_paper", 4)),
        )
        batch_size = int(config.get("llm_batch_size", 8))
        total_batches = (len(papers) + batch_size - 1) // batch_size
        configured_workers = max(1, int(config.get("workers", 1)))
        worker_count = min(configured_workers, total_batches) if total_batches else 1
        llm_results: dict[str, Classification] = {}
        errors: list[str] = []
        batches = [papers[start : start + batch_size] for start in range(0, len(papers), batch_size)]
        print(
            f"[classification] {len(papers)} papers in {total_batches} batches with "
            f"{worker_count} worker(s)",
            file=sys.stderr,
            flush=True,
        )

        def classify_batch(batch_number: int, batch: list[Paper]) -> dict[str, Classification]:
            print(
                f"[classification] batch {batch_number}/{total_batches}: {len(batch)} papers",
                file=sys.stderr,
                flush=True,
            )
            return classifier.classify_batch(batch)

        with ThreadPoolExecutor(
            max_workers=worker_count,
            thread_name_prefix="paper-classification",
        ) as executor:
            futures = {
                executor.submit(classify_batch, batch_number, batch): batch_number
                for batch_number, batch in enumerate(batches, start=1)
            }
            for future in as_completed(futures):
                batch_number = futures[future]
                try:
                    batch_results = future.result()
                    llm_results.update(batch_results)
                    relevant_count = sum(result.relevant for result in batch_results.values())
                    print(
                        f"[classification] completed {batch_number}/{total_batches}: "
                        f"{relevant_count} relevant",
                        file=sys.stderr,
                        flush=True,
                    )
                except LlmError as exc:
                    errors.append(f"classification batch {batch_number}: {exc}")
                    print(
                        f"[classification] fallback {batch_number}/{total_batches}: {exc}",
                        file=sys.stderr,
                        flush=True,
                    )

        if mode == "llm":
            return {
                paper.arxiv_id: llm_results.get(paper.arxiv_id, Classification(False, source="llm"))
                for paper in papers
            }, errors

        merged: dict[str, Classification] = {}
        max_categories = int(config.get("max_categories_per_paper", 4))
        for paper in papers:
            rule = rule_results[paper.arxiv_id]
            model = llm_results.get(paper.arxiv_id)
            if model is None:
                merged[paper.arxiv_id] = rule
                continue
            high_rule_score = max(rule.rule_scores.values(), default=0.0) >= 5.0
            relevant = model.relevant or (rule.relevant and high_rule_score)
            if not relevant:
                merged[paper.arxiv_id] = Classification(
                    relevant=False,
                    confidence=max(model.confidence, rule.confidence),
                    reason=f"LLM excluded; {rule.reason}",
                    source="hybrid",
                    rule_scores=rule.rule_scores,
                )
                continue
            categories = list(model.categories if model.relevant else rule.categories)
            for category in rule.categories:
                if rule.rule_scores.get(category, 0.0) >= 4.0 and category not in categories:
                    categories.append(category)
            categories = categories[:max_categories]
            primary = model.primary_category if model.relevant else categories[0]
            merged[paper.arxiv_id] = Classification(
                relevant=True,
                primary_category=primary,
                categories=categories,
                confidence=max(model.confidence, rule.confidence),
                reason=f"{model.reason}; rule check: {rule.reason}",
                source="hybrid",
                rule_scores=rule.rule_scores,
            )
        return merged, errors

    @staticmethod
    def _sanitize_source_urls(
        generated: GeneratedNote,
        source_links: list[str],
        source_text: str,
    ) -> list[str]:
        issues: list[str] = []
        normalized_links = {link.rstrip("/") for link in source_links}
        for key in ("code_url", "project_url"):
            value = str(generated.content.get(key, "")).strip()
            if not value:
                continue
            verified = value.rstrip("/") in normalized_links or value in source_text
            if not verified:
                generated.content[key] = ""
                issues.append(f"removed unverified {key}: {value}")
        return issues

    @staticmethod
    def _validate_evidence_quotes(generated: GeneratedNote, source_text: str) -> list[str]:
        issues: list[str] = []
        experiments = generated.content.get("experiments", {})
        for section in ("main_results", "ablations"):
            for index, row in enumerate(experiments.get(section, [])):
                if not isinstance(row, dict):
                    continue
                quote = str(row.get("evidence_quote", "")).strip()
                if quote and not _quote_supported_by_source(quote, source_text):
                    issues.append(f"{section}[{index}] evidence quote not found in source")
        return issues

    def _write_indexes(
        self,
        daily_dir: Path,
        date_string: str,
        records: list[dict[str, Any]],
        seen: dict[str, Any],
    ) -> None:
        atomic_write_text(
            daily_dir / "index.md",
            render_daily_index(date_string, records, self.taxonomy),
        )
        for category in self.taxonomy.categories:
            category_records = [
                record
                for record in records
                if category
                in (
                    record["classification"].categories
                    or [record["classification"].primary_category]
                )
            ]
            if category_records:
                atomic_write_text(
                    daily_dir / category / "index.md",
                    render_category_index(category, category_records, self.taxonomy),
                )
            else:
                (daily_dir / category / "index.md").unlink(missing_ok=True)
        output_dir = self.settings.project_path("output_dir")
        dates = sorted(
            [path.name for path in output_dir.iterdir() if path.is_dir() and re_date(path.name)],
            reverse=True,
        ) if output_dir.exists() else []
        atomic_write_text(output_dir / "index.md", render_daily_master(dates, seen))

        category_dir = self.settings.project_path("category_index_dir")
        atomic_write_text(
            category_dir / "index.md",
            render_categories_master(seen, self.taxonomy),
        )
        for category in self.taxonomy.categories:
            entries = [
                (arxiv_id, item)
                for arxiv_id, item in seen.items()
                if category
                in item.get("categories", [item.get("primary_category")])
                and item.get("path")
            ]
            entries.sort(
                key=lambda pair: (
                    str(pair[1].get("announcement_date", "")),
                    str(pair[1].get("title", "")),
                ),
                reverse=True,
            )
            atomic_write_text(
                category_dir / category / "index.md",
                render_global_category_index(category, entries, self.taxonomy),
            )

        atomic_write_text(
            self.settings.project_path("review_index_file"),
            render_review_index(seen),
        )


def re_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def validate_output_tree(output_dir: Path) -> dict[str, list[str]]:
    issues: dict[str, list[str]] = {}
    for path in output_dir.rglob("*.md"):
        if path.name == "index.md":
            continue
        file_issues = validate_rendered_note(path.read_text(encoding="utf-8"))
        if file_issues:
            issues[str(path)] = file_issues
    return issues
