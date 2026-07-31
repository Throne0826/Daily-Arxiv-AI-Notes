from datetime import date

from daily_arxiv_notes.arxiv import (
    ArxivClient,
    ArxivError,
    ListingEntry,
    extract_affiliations_from_html,
    extract_affiliations_from_pdf_text,
    parse_listing_page,
)
from bs4 import BeautifulSoup
from daily_arxiv_notes.models import Paper


LISTING_HTML = """
<html><body>
<h3>Showing new listings for Wednesday, 29 July 2026</h3>
<h3>New submissions (showing 1 of 1 entries)</h3>
<dl>
  <dt><a href="/abs/2607.99991">arXiv:2607.99991</a></dt>
  <dd><div class="meta">
    <div class="list-title"><span>Title:</span> Reliable Verifiers for Reasoning</div>
    <div class="list-authors"><a>Alice Example</a><a>Bob Example</a></div>
  </div></dd>
</dl>
<h3>Cross submissions (showing 1 of 1 entries)</h3>
<dl>
  <dt><a href="/abs/2607.99992">arXiv:2607.99992</a></dt>
  <dd><div class="meta">
    <div class="list-title"><span>Title:</span> An Embodied Agent</div>
    <div class="list-authors"><a>Carol Example</a></div>
  </div></dd>
</dl>
<h3>Replacements (showing 1 of 1 entries)</h3>
<dl>
  <dt><a href="/abs/2501.00001">arXiv:2501.00001</a></dt>
  <dd><div class="meta"><div class="list-title"><span>Title:</span> Old Paper</div></div></dd>
</dl>
</body></html>
"""


def test_parse_new_and_cross_submissions_only() -> None:
    announcement, entries = parse_listing_page(LISTING_HTML, "cs.AI", include_crosslists=True)

    assert announcement == date(2026, 7, 29)
    assert [entry.arxiv_id for entry in entries] == ["2607.99991", "2607.99992"]
    assert entries[0].title == "Reliable Verifiers for Reasoning"
    assert entries[0].authors == ["Alice Example", "Bob Example"]
    assert entries[1].section == "cross"


def test_cross_submissions_can_be_disabled() -> None:
    _, entries = parse_listing_page(LISTING_HTML, "cs.AI", include_crosslists=False)
    assert [entry.arxiv_id for entry in entries] == ["2607.99991"]


class FakeFullTextHttp:
    def get_text(self, url: str) -> str:
        method_body = "Method body with enough detail for full-text extraction. " * 30
        return f"""
        <html><article>
          <h1>Example Paper</h1>
          <div class="ltx_authors"><span>Alice<sup>1</sup></span><span><sup>1</sup>Example University</span></div>
          <h6>Abstract</h6><p>Abstract body.</p>
          <h2>1 Introduction</h2><p>Introduction body.</p>
          <h2>2 Named Method</h2><p>{method_body}</p>
          <h3>2.1 Training</h3><p>Training body.</p>
        </article></html>
        """


def test_full_text_preserves_html_section_hierarchy() -> None:
    full_text = ArxivClient(FakeFullTextHttp()).fetch_full_text(
        Paper(arxiv_id="2607.99991", title="Example Paper")
    )

    assert full_text.source == "arxiv_html"
    assert "[SECTION level=6] Abstract" in full_text.text
    assert "[SECTION level=2] 2 Named Method" in full_text.text
    assert "[SECTION level=3] 2.1 Training" in full_text.text


def test_extract_affiliations_from_latexml_author_notes() -> None:
    soup = BeautifulSoup(
        """
        <div class="ltx_authors"><span class="ltx_personname">
          Alice<sup>1,*</sup>, Bob<sup>2</sup></span>
          <span class="ltx_author_notes"><sup>*</sup>Corresponding author: Alice
          <sup>1</sup>Technical University of Munich
          <sup>2</sup>Example AI Research Lab</span>
        </div>
        """,
        "html.parser",
    )

    assert extract_affiliations_from_html(soup) == [
        "Technical University of Munich",
        "Example AI Research Lab",
    ]


def test_full_text_backfills_affiliations_from_same_html_request() -> None:
    paper = Paper(arxiv_id="2607.99991", title="Example Paper")
    ArxivClient(FakeFullTextHttp()).fetch_full_text(paper)

    assert paper.affiliations == ["Example University"]


def test_extract_affiliations_from_pdf_first_page() -> None:
    text = """
    Example Paper
    Alice Example1, Bob Example2
    1Sichuan University
    2Dexmal Inc.
    *Equal contribution
    Abstract
    We study a research problem at university scale.
    """

    assert extract_affiliations_from_pdf_text(text) == [
        "Sichuan University",
        "Dexmal Inc",
    ]


def test_atom_rate_limit_falls_back_to_listing_metadata_once(monkeypatch) -> None:
    client = ArxivClient(
        object(),
        metadata_batch_size=1,
        fallback_to_abs_metadata=False,
    )
    atom_calls = []

    def rate_limited(query: str) -> str:
        atom_calls.append(query)
        raise ArxivError("rate limited")

    monkeypatch.setattr(client, "_fetch_atom_batch", rate_limited)
    monkeypatch.setattr(
        client,
        "_fetch_abs_metadata",
        lambda *_: (_ for _ in ()).throw(AssertionError("unexpected per-paper fallback")),
    )
    listings = {
        "2607.99991": ListingEntry("2607.99991", "First paper", ["Alice"], "cs.AI"),
        "2607.99992": ListingEntry("2607.99992", "Second paper", ["Bob"], "cs.CL"),
    }

    papers = client.fetch_metadata(listings, date(2026, 7, 31))

    assert len(atom_calls) == 1
    assert [paper.title for paper in papers] == ["First paper", "Second paper"]
    assert [paper.source_categories for paper in papers] == [["cs.AI"], ["cs.CL"]]
