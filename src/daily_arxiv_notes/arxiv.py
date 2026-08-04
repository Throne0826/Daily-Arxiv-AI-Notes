from __future__ import annotations

import gzip
import http.client
import io
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Iterable

from bs4 import BeautifulSoup
from bs4.element import Tag
from pypdf import PdfReader

from .models import FullText, Paper


ARXIV_ID_RE = re.compile(r"(?P<id>\d{4}\.\d{4,5})(?:v\d+)?")
ATOM_NS = "http://www.w3.org/2005/Atom"
ARXIV_NS = "http://arxiv.org/schemas/atom"

AFFILIATION_HINT_RE = re.compile(
    r"\b(?:"
    r"universit(?:y|ies)|institute|institution|college|school|department|faculty|"
    r"laborator(?:y|ies)|\blab\b|centre|center|academy|research|foundation|"
    r"hospital|clinic|corporation|\bcorp\b|\binc\b|\bltd\b|"
    r"polytechnic|polytechnique|telecom|télécom|chapel hill|ucla|kaist|"
    r"tsinghua|peking|stanford|berkeley|max planck|allen institute|"
    r"amazon|alibaba|apple|bytedance|deepmind|google|huawei|meta ai|"
    r"nvidia|openai|tencent|anthropic|inria|cnrs|epfl|\beth\b|\bmit\b|"
    r"microsoft|honor|orange|kuaishou|xiaohongshu|hermeneutic ai|"
    r"hku|pku|hkust|thu|szu|sjtu|uestc|zju|sysu|iflytek|ibm"
    r")\b",
    re.IGNORECASE,
)
NON_AFFILIATION_RE = re.compile(
    r"\b(?:corresponding author|equal(?:ly)? contribut|work done|e-?mail|"
    r"arxiv|github|project page|funded by|supported by|grant no)\b",
    re.IGNORECASE,
)


class ArxivError(RuntimeError):
    pass


@dataclass(slots=True)
class ListingEntry:
    arxiv_id: str
    title: str
    authors: list[str] = field(default_factory=list)
    source_category: str = ""
    section: str = "new"


class PoliteHttpClient:
    def __init__(
        self,
        user_agent: str,
        interval_seconds: float = 3.0,
        timeout_seconds: int = 90,
        retries: int = 4,
    ) -> None:
        self.user_agent = user_agent
        self.interval_seconds = interval_seconds
        self.timeout_seconds = timeout_seconds
        self.retries = retries
        self._last_request = 0.0

    def _wait(self) -> None:
        remaining = self.interval_seconds - (time.monotonic() - self._last_request)
        if remaining > 0:
            time.sleep(remaining)

    def get_bytes(
        self,
        url: str,
        *,
        timeout_seconds: int | None = None,
        retries: int | None = None,
    ) -> bytes:
        last_error: Exception | None = None
        effective_timeout = timeout_seconds or self.timeout_seconds
        effective_retries = retries or self.retries
        for attempt in range(effective_retries):
            self._wait()
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": self.user_agent,
                    "Accept-Encoding": "gzip",
                },
            )
            try:
                with urllib.request.urlopen(request, timeout=effective_timeout) as response:
                    payload = response.read()
                    if response.headers.get("Content-Encoding") == "gzip":
                        payload = gzip.decompress(payload)
                    self._last_request = time.monotonic()
                    return payload
            except (
                urllib.error.URLError,
                urllib.error.HTTPError,
                http.client.HTTPException,
                ConnectionError,
                TimeoutError,
                OSError,
            ) as exc:
                last_error = exc
                self._last_request = time.monotonic()
                if attempt + 1 < effective_retries:
                    time.sleep(min(2**attempt, 8))
        raise ArxivError(f"request failed after {effective_retries} attempts: {url}: {last_error}")

    def get_text(
        self,
        url: str,
        *,
        timeout_seconds: int | None = None,
        retries: int | None = None,
    ) -> str:
        return self.get_bytes(
            url,
            timeout_seconds=timeout_seconds,
            retries=retries,
        ).decode("utf-8", errors="replace")


def _clean_affiliation_candidate(value: str) -> str:
    value = " ".join(value.split()).strip(" ,;:.-")
    value = re.sub(r"^[\d*†‡§¶∗#\s,]+", "", value).strip(" ,;:.-")
    value = re.sub(r"^with\s+(?:the\s+)?", "", value, flags=re.I)
    value = re.sub(r"\s+(?:\S+@\S+).*$", "", value).strip(" ,;:.-")
    value = re.sub(r"\s*\([^)]*$", "", value).strip(" ,;:.-")
    if "@" in value or not value or len(value) > 240 or NON_AFFILIATION_RE.search(value):
        return ""
    if not AFFILIATION_HINT_RE.search(value):
        return ""

    # LaTeXML sometimes puts a prose footnote around a short institution name.
    # Keep the named organization instead of rendering the whole explanatory note.
    subject = re.search(
        r"(?:^|[.!?]\s+)(.{2,90}?)\s+is\s+(?:an?|the)\s+.*"
        r"(?:research|institute|university|centre|center)",
        value,
        flags=re.IGNORECASE,
    )
    if subject:
        value = subject.group(1).strip(" ,;:.-")
    return value


def extract_affiliations_from_html(soup: BeautifulSoup) -> list[str]:
    """Extract institution strings from LaTeXML's inconsistent author byline."""
    candidates: list[str] = []

    for node in soup.select(
        ".ltx_role_affiliationtext, .ltx_affiliation, "
        "[class*='affiliation'], [itemprop='affiliation']"
    ):
        candidates.append(node.get_text(" ", strip=True))

    author_block = soup.select_one(".ltx_authors")
    if author_block is not None:
        # A large share of arXiv HTML has no affiliation-specific class. Superscript
        # markers and line breaks are the only stable boundaries in the byline.
        author_copy = BeautifulSoup(str(author_block), "html.parser")
        for node in author_copy.select("br"):
            node.replace_with("\n")
        for node in author_copy.select("sup"):
            marker = " ".join(node.get_text(" ", strip=True).split())
            node.replace_with(f"\n[[AFFILIATION_MARKER:{marker}]] ")
        text = author_copy.get_text(" ", strip=False)
        candidates.extend(
            part
            for part in re.split(r"\[\[AFFILIATION_MARKER:[^\]]*\]\]|\n", text)
            if part.strip()
        )

    cleaned: list[str] = []
    for candidate in candidates:
        value = _clean_affiliation_candidate(candidate)
        if value and value.casefold() not in {item.casefold() for item in cleaned}:
            cleaned.append(value)
    return cleaned[:12]


def extract_affiliations_from_pdf_text(text: str) -> list[str]:
    """Extract numbered institution lines from the first page of a paper PDF."""
    raw_lines = [" ".join(line.split()) for line in text.splitlines() if line.strip()]
    lines: list[str] = []
    index = 0
    while index < len(raw_lines):
        line = raw_lines[index]
        # PDF extraction commonly breaks words such as "Na-\ntional" in footnotes.
        while line.endswith("-") and index + 1 < len(raw_lines):
            index += 1
            line = line[:-1] + raw_lines[index]
        lines.append(line)
        index += 1

    abstract_index = next(
        (i for i, line in enumerate(lines) if re.match(r"^(?:abstract|abstract—)", line, re.I)),
        len(lines),
    )
    header_lines = lines[:abstract_index]
    footnote_lines = [
        " ".join(lines[max(0, i - 1) : min(len(lines), i + 3)])
        for i, line in enumerate(lines)
        if re.search(r"\b(?:authors? are|author is|is with|are with)\b", line, re.I)
    ]

    candidates: list[str] = []
    for line in [*header_lines, *footnote_lines]:
        if not AFFILIATION_HINT_RE.search(line):
            continue
        line = re.sub(r"^.*?\b(?:authors? are|author is|is with|are with)\s+", "", line, flags=re.I)
        line = re.split(r"(?:\be-?mail\b|\bcorrespond(?:ing|ence)\b|\*equal|†|‡)", line, maxsplit=1, flags=re.I)[0]
        # Superscript affiliation markers become leading digits in extracted PDF text.
        parts = re.split(r"(?<!\d)(?=[1-9](?:[A-Z]|The\b|Independent\b))", line)
        for part in parts:
            value = _clean_affiliation_candidate(part)
            if value:
                candidates.append(value)

    cleaned: list[str] = []
    for value in candidates:
        key = value.casefold()
        if key not in {item.casefold() for item in cleaned}:
            cleaned.append(value)
    return cleaned[:12]


def parse_listing_page(
    html: str,
    source_category: str,
    include_crosslists: bool = True,
) -> tuple[date | None, list[ListingEntry]]:
    soup = BeautifulSoup(html, "html.parser")
    announcement_date: date | None = None
    for heading in soup.find_all("h3"):
        text = " ".join(heading.get_text(" ", strip=True).split())
        match = re.search(r"Showing new listings for \w+, (\d{1,2} \w+ \d{4})", text)
        if match:
            announcement_date = datetime.strptime(match.group(1), "%d %B %Y").date()
            break

    accepted = ("new submissions", "cross submissions") if include_crosslists else ("new submissions",)
    entries: list[ListingEntry] = []

    # arXiv now places each section heading inside its own dl#articles. Looking
    # for the next <dl> associates New with Cross and Cross with Replacements
    # after BeautifulSoup repairs that otherwise-invalid HTML structure.
    sections: list[tuple[str, Tag]] = []
    for listing in soup.select("dl#articles"):
        heading = listing.find("h3", recursive=False)
        if heading is not None:
            sections.append((heading.get_text(" ", strip=True), listing))

    # Retain compatibility with older pages and small parser fixtures where the
    # heading precedes a plain <dl> instead of being nested inside it.
    if not sections:
        for heading in soup.find_all("h3"):
            listing = heading.find_next("dl")
            if listing is not None:
                sections.append((heading.get_text(" ", strip=True), listing))

    for heading_value, listing in sections:
        heading_text = " ".join(heading_value.lower().split())
        section = next((name for name in accepted if heading_text.startswith(name)), None)
        if section is None:
            continue
        for item in listing.find_all("dt", recursive=False):
            match = ARXIV_ID_RE.search(item.get_text(" ", strip=True))
            if not match:
                continue
            details = item.find_next_sibling("dd")
            if details is None:
                continue
            title_node = details.select_one(".list-title")
            title = title_node.get_text(" ", strip=True) if title_node else ""
            title = re.sub(r"^Title:\s*", "", title).strip()
            authors = [node.get_text(" ", strip=True) for node in details.select(".list-authors a")]
            entries.append(
                ListingEntry(
                    arxiv_id=match.group("id"),
                    title=title,
                    authors=authors,
                    source_category=source_category,
                    section="cross" if section.startswith("cross") else "new",
                )
            )
    return announcement_date, entries


class ArxivClient:
    def __init__(
        self,
        http: PoliteHttpClient,
        page_size: int = 100,
        metadata_batch_size: int = 50,
        include_crosslists: bool = True,
        fallback_to_abs_metadata: bool = True,
    ) -> None:
        self.http = http
        self.page_size = page_size
        self.metadata_batch_size = metadata_batch_size
        self.include_crosslists = include_crosslists
        self.fallback_to_abs_metadata = fallback_to_abs_metadata

    def fetch_daily_listings(
        self,
        categories: Iterable[str],
        requested_date: date | None = None,
    ) -> tuple[date, dict[str, ListingEntry]]:
        by_id: dict[str, ListingEntry] = {}
        observed_dates: set[date] = set()
        for category in categories:
            skip = 0
            while True:
                query = urllib.parse.urlencode({"skip": skip, "show": self.page_size})
                url = f"https://arxiv.org/list/{category}/new?{query}"
                html = self.http.get_text(url)
                announcement_date, entries = parse_listing_page(
                    html,
                    source_category=category,
                    include_crosslists=self.include_crosslists,
                )
                if announcement_date:
                    observed_dates.add(announcement_date)
                for entry in entries:
                    existing = by_id.get(entry.arxiv_id)
                    if existing is None:
                        by_id[entry.arxiv_id] = entry
                    elif category not in existing.source_category.split(","):
                        existing.source_category = f"{existing.source_category},{category}"
                if len(entries) < self.page_size:
                    break
                skip += self.page_size
                if skip > 5000:
                    raise ArxivError(f"pagination guard triggered for {category}")

        if not observed_dates:
            raise ArxivError("arXiv listings did not expose an announcement date")
        if len(observed_dates) != 1:
            rendered = ", ".join(sorted(item.isoformat() for item in observed_dates))
            raise ArxivError(f"category listings disagree on announcement date: {rendered}")
        announcement_date = observed_dates.pop()
        if requested_date and announcement_date != requested_date:
            raise ArxivError(
                f"latest arXiv listing is {announcement_date.isoformat()}, "
                f"not requested {requested_date.isoformat()}"
            )
        return announcement_date, by_id

    def fetch_metadata(
        self,
        listings: dict[str, ListingEntry],
        announcement_date: date,
    ) -> list[Paper]:
        ids = sorted(listings)
        papers: dict[str, Paper] = {}
        atom_api_available = True
        for start in range(0, len(ids), self.metadata_batch_size):
            batch = ids[start : start + self.metadata_batch_size]
            query = urllib.parse.urlencode(
                {"id_list": ",".join(batch), "start": 0, "max_results": len(batch)}
            )
            if atom_api_available:
                try:
                    xml_text = self._fetch_atom_batch(query)
                    root = ET.fromstring(xml_text)
                    for entry in root.findall(f"{{{ATOM_NS}}}entry"):
                        paper = self._parse_atom_entry(entry, announcement_date)
                        listing = listings.get(paper.arxiv_id)
                        if listing:
                            paper.source_categories = listing.source_category.split(",")
                            if not paper.title:
                                paper.title = listing.title
                            if not paper.authors:
                                paper.authors = listing.authors
                        papers[paper.arxiv_id] = paper
                except (ArxivError, ET.ParseError):
                    # A rate-limited Atom endpoint normally remains unavailable for
                    # the whole run. Avoid repeating the same delay for every batch.
                    atom_api_available = False

            if not atom_api_available and self.fallback_to_abs_metadata:
                for arxiv_id in batch:
                    listing = listings[arxiv_id]
                    try:
                        paper = self._fetch_abs_metadata(arxiv_id, announcement_date)
                        paper.source_categories = listing.source_category.split(",")
                        papers[arxiv_id] = paper
                    except ArxivError:
                        continue

        for arxiv_id, listing in listings.items():
            if arxiv_id not in papers:
                papers[arxiv_id] = Paper(
                    arxiv_id=arxiv_id,
                    title=listing.title,
                    authors=listing.authors,
                    announcement_date=announcement_date.isoformat(),
                    arxiv_url=f"https://arxiv.org/abs/{arxiv_id}",
                    pdf_url=f"https://arxiv.org/pdf/{arxiv_id}",
                    source_categories=listing.source_category.split(","),
                )
        return [papers[arxiv_id] for arxiv_id in sorted(papers)]

    def _fetch_atom_batch(self, query: str) -> str:
        errors: list[str] = []
        for base_url in ("https://export.arxiv.org/api/query", "https://arxiv.org/api/query"):
            try:
                return self.http.get_text(
                    f"{base_url}?{query}",
                    timeout_seconds=min(20, self.http.timeout_seconds),
                    retries=1,
                )
            except ArxivError as exc:
                errors.append(str(exc))
        raise ArxivError("; ".join(errors))

    @staticmethod
    def _parse_atom_entry(entry: ET.Element, announcement_date: date) -> Paper:
        def text(namespace: str, name: str) -> str:
            node = entry.find(f"{{{namespace}}}{name}")
            return " ".join((node.text or "").split()) if node is not None else ""

        raw_id = text(ATOM_NS, "id")
        match = ARXIV_ID_RE.search(raw_id)
        if not match:
            raise ArxivError(f"invalid arXiv entry id: {raw_id}")
        arxiv_id = match.group("id")
        arxiv_url = ""
        pdf_url = ""
        for node in entry.findall(f"{{{ATOM_NS}}}link"):
            if node.attrib.get("rel") == "alternate":
                arxiv_url = node.attrib.get("href", "")
            if node.attrib.get("type") == "application/pdf":
                pdf_url = node.attrib.get("href", "")
        categories = [node.attrib.get("term", "") for node in entry.findall(f"{{{ATOM_NS}}}category")]
        primary = entry.find(f"{{{ARXIV_NS}}}primary_category")
        authors = [
            " ".join((node.findtext(f"{{{ATOM_NS}}}name") or "").split())
            for node in entry.findall(f"{{{ATOM_NS}}}author")
        ]
        affiliations = [
            " ".join((node.findtext(f"{{{ARXIV_NS}}}affiliation") or "").split())
            for node in entry.findall(f"{{{ATOM_NS}}}author")
        ]
        return Paper(
            arxiv_id=arxiv_id,
            title=text(ATOM_NS, "title"),
            abstract=text(ATOM_NS, "summary"),
            authors=[author for author in authors if author],
            affiliations=list(dict.fromkeys(value for value in affiliations if value)),
            subjects=[category for category in categories if category],
            primary_subject=primary.attrib.get("term", "") if primary is not None else "",
            published=text(ATOM_NS, "published"),
            updated=text(ATOM_NS, "updated"),
            announcement_date=announcement_date.isoformat(),
            comments=text(ARXIV_NS, "comment"),
            doi=text(ARXIV_NS, "doi"),
            arxiv_url=arxiv_url or f"https://arxiv.org/abs/{arxiv_id}",
            pdf_url=pdf_url or f"https://arxiv.org/pdf/{arxiv_id}",
        )

    def _fetch_abs_metadata(self, arxiv_id: str, announcement_date: date) -> Paper:
        html = self.http.get_text(f"https://arxiv.org/abs/{arxiv_id}")
        soup = BeautifulSoup(html, "html.parser")

        def meta(name: str) -> str:
            node = soup.find("meta", attrs={"name": name})
            return " ".join(str(node.get("content", "")).split()) if node else ""

        title = meta("citation_title")
        if not title:
            raise ArxivError(f"arXiv abstract page did not expose metadata for {arxiv_id}")
        authors = [
            " ".join(str(node.get("content", "")).split())
            for node in soup.find_all("meta", attrs={"name": "citation_author"})
        ]
        affiliations = [
            " ".join(str(node.get("content", "")).split())
            for node in soup.find_all(
                "meta",
                attrs={"name": re.compile(r"^citation_author_(?:institution|affiliation)$", re.I)},
            )
        ]
        subjects = [value.strip() for value in meta("citation_keywords").split(",") if value.strip()]
        return Paper(
            arxiv_id=arxiv_id,
            title=title,
            abstract=meta("citation_abstract"),
            authors=[author for author in authors if author],
            affiliations=list(dict.fromkeys(value for value in affiliations if value)),
            subjects=subjects,
            primary_subject=subjects[0] if subjects else "",
            published=meta("citation_date"),
            updated=meta("citation_online_date"),
            announcement_date=announcement_date.isoformat(),
            doi=meta("citation_doi"),
            arxiv_url=f"https://arxiv.org/abs/{arxiv_id}",
            pdf_url=meta("citation_pdf_url") or f"https://arxiv.org/pdf/{arxiv_id}",
        )

    def fetch_affiliations(self, paper: Paper) -> list[str]:
        try:
            html = self.http.get_text(
                f"https://arxiv.org/html/{paper.arxiv_id}",
                timeout_seconds=min(20, self.http.timeout_seconds),
                retries=1,
            )
            affiliations = extract_affiliations_from_html(BeautifulSoup(html, "html.parser"))
            if affiliations:
                return affiliations
        except ArxivError:
            pass

        return self._fetch_pdf_affiliations(paper)

    def _fetch_pdf_affiliations(self, paper: Paper) -> list[str]:
        pdf = self.http.get_bytes(
            paper.pdf_url or f"https://arxiv.org/pdf/{paper.arxiv_id}",
            timeout_seconds=min(45, self.http.timeout_seconds),
            retries=1,
        )
        reader = PdfReader(io.BytesIO(pdf))
        if not reader.pages:
            return []
        return extract_affiliations_from_pdf_text(reader.pages[0].extract_text() or "")

    def fetch_full_text(self, paper: Paper, max_chars: int = 90000) -> FullText:
        html_url = f"https://arxiv.org/html/{paper.arxiv_id}"
        try:
            html = self.http.get_text(html_url)
            soup = BeautifulSoup(html, "html.parser")
            if not paper.affiliations:
                paper.affiliations = extract_affiliations_from_html(soup)
            if not paper.affiliations:
                try:
                    paper.affiliations = self._fetch_pdf_affiliations(paper)
                except Exception:
                    # Affiliation enrichment is useful metadata, but a missing or
                    # malformed PDF must not discard an otherwise valid HTML source.
                    pass
            for node in soup.select("script, style, nav, footer, .ltx_page_footer"):
                node.decompose()
            article = soup.find("article") or soup.select_one("main")
            if article is not None:
                # Preserve arXiv HTML's section hierarchy in the plain-text source. The
                # generator uses these markers to send complete relevant chapters to the
                # LLM instead of arbitrary keyword-matched character windows.
                for heading in article.select("h2, h3, h4, h5, h6"):
                    title = " ".join(heading.get_text(" ", strip=True).split())
                    if not title:
                        continue
                    level = heading.name.removeprefix("h")
                    heading.clear()
                    heading.append(f"[SECTION level={level}] {title}")
                text = "\n".join(
                    line.strip()
                    for line in article.get_text("\n", strip=True).splitlines()
                    if line.strip()
                )
                links = sorted(
                    {
                        urllib.parse.urljoin(html_url, node.get("href"))
                        for node in article.find_all("a", href=True)
                        if node.get("href")
                    }
                )
                if len(text) >= 1000:
                    return FullText(text=text[:max_chars], source="arxiv_html", links=links)
        except ArxivError:
            pass

        pdf = self.http.get_bytes(paper.pdf_url or f"https://arxiv.org/pdf/{paper.arxiv_id}")
        reader = PdfReader(io.BytesIO(pdf))
        chunks: list[str] = []
        size = 0
        for page in reader.pages:
            page_text = page.extract_text() or ""
            chunks.append(page_text)
            size += len(page_text)
            if size >= max_chars:
                break
        text = "\n".join(chunks)[:max_chars]
        if len(text) < 500:
            raise ArxivError(f"could not extract full text for {paper.arxiv_id}")
        return FullText(text=text, source="arxiv_pdf", links=[])
