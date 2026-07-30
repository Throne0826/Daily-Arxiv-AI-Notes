"""Post-build hook: slim down search_index.json for fast client-side search.

Why this matters
----------------
MkDocs' search plugin emits one document per heading. Every paper note shares
the same Chinese section headings
("一句话总结", "研究背景与动机", "方法详解", ...), so if we naively concatenate
those into each paper's title field, those generic phrases end up in ~14k
documents. Lunr.js then spends forever building the inverted index and the
desktop UI sits on "正在初始化搜索引擎" forever.

Strategy
--------
  1. Collapse all section-level entries (#anchor) into a single doc per page.
  2. Keep **only the base page's title** — do NOT merge section headings into
     the title field. This is the single biggest win for lunr performance.
  3. Set each page's 'text' field to its **keywords only** (read from the
     note's `**关键词**:` / `**Keywords**:` line) — never the full body. This
     makes keyword search work (e.g. a paper whose title omits "diffusion" but
     is tagged so) while costing only ~1.8 MB over title-only, vs the ~250 MB
     a full-body index would weigh.
  4. Preserve the first doc's `tags` so tag-based filtering still works.
  5. Keep the taxonomy and paper tags used by the daily search filters.
  6. Index only daily paper pages, never homepage/date/category index pages.
"""

import json
import os
import re
from collections import OrderedDict

# Body metadata line listing a paper's keywords, e.g.
#   **关键词**: diffusion model, image editing      (zh notes)
#   **Keywords**: diffusion model, image editing    (en notes)
_KW_PATTERN = re.compile(r"\*\*(?:关键词|Keywords)\*\*\s*[:：]\s*(.+)")


_PAPER_PATH = re.compile(
    r"^arxiv_daily/\d{4}-\d{2}-\d{2}/[a-z0-9_\-]+/[^/]+/$"
)


def _is_paper_page(base: str) -> bool:
    """Return whether a generated URL is a dated daily-paper page."""
    return bool(_PAPER_PATH.fullmatch(base))


def _read_keywords(docs_dir: str, base: str) -> str:
    """Return the space-joined keywords for a page, read from its source note.

    ``base`` is the directory URL (for example
    ``arxiv_daily/2026-07-29/llm_reasoning/slug/``). Only the
    file head is scanned since the keyword line lives in the metadata block.
    """
    rel = base.strip("/")
    if not rel:
        return ""
    src = os.path.join(docs_dir, rel + ".md")
    try:
        with open(src, encoding="utf-8") as f:
            head = f.read(2000)
    except OSError:
        return ""
    m = _KW_PATTERN.search(head)
    if not m:
        return ""
    kws = [k.strip() for k in m.group(1).split(",") if k.strip()]
    # Comma-join (not space-join) so multi-word keywords keep their boundaries
    # for chip rendering on /search/. Search is unaffected: the tokenizers on
    # both lunr and the /search/ page split on punctuation + whitespace alike.
    return ", ".join(kws)


def on_post_build(config, **kwargs):
    index_path = os.path.join(config["site_dir"], "search", "search_index.json")
    if not os.path.exists(index_path):
        return

    with open(index_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = data.get("docs", [])
    if not docs:
        return

    original_count = len(docs)
    original_size = os.path.getsize(index_path)

    docs_dir = config["docs_dir"]

    # ── Pass 1: collapse section entries, keep only the base page title ──
    pages: "OrderedDict[str, dict]" = OrderedDict()
    for doc in docs:
        loc = doc.get("location", "")
        base = loc.split("#")[0]

        if not _is_paper_page(base):
            continue

        if base not in pages:
            pages[base] = {
                "location": base,
                "title": doc.get("title", "").strip(),
                "text": _read_keywords(docs_dir, base),
                "_tags": set(doc.get("tags") or []),
            }
        else:
            # Subsequent section entry: only collect tags, never merge titles.
            tags = doc.get("tags") or []
            if tags:
                pages[base]["_tags"].update(tags)

    # ── Pass 2: normalize the small tag set used by field filtering ──
    for page in pages.values():
        raw_tags = page.pop("_tags")
        kept = sorted(tag.strip() for tag in raw_tags if tag.strip())
        if kept:
            page["tags"] = kept

    slim_docs = list(pages.values())
    data["docs"] = slim_docs

    kw_pages = sum(1 for p in slim_docs if p.get("text"))

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    new_size = os.path.getsize(index_path)
    print(
        f"[slim_search_index] {original_count} -> {len(slim_docs)} docs "
        f"({kw_pages} with keywords), "
        f"{original_size / 1024 / 1024:.1f} MB -> {new_size / 1024 / 1024:.1f} MB"
    )
