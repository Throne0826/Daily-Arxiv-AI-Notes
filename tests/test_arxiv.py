from datetime import date

from daily_arxiv_notes.arxiv import ArxivClient, parse_listing_page
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
