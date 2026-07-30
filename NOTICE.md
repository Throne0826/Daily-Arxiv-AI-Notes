# Attribution and changes

This repository is derived from [zhaoyang97/Paper-Notes](https://github.com/zhaoyang97/Paper-Notes), upstream commit `2a378054bdca25df4b5418e9cd64b02fc6aa789e` (2026-07-21).

Reused and adapted components include the MkDocs Material configuration, theme overrides, visual styles, search experience, and paper-note organization. The original conference-note corpus is not included.

Material changes in this derivative:

- replaced conference navigation with daily arXiv and research-area indexes;
- added automated arXiv retrieval, classification, full-text parsing, evidence checks, and review state;
- replaced conference/date assumptions in search and indexing;
- removed upstream production domains, analytics, community links, and conference content;
- added AI-draft and human-review status throughout the site.

The derivative site material remains licensed under CC BY-NC-SA 4.0. See `LICENSE`.

The site vendors MathJax 3.2.2's `tex-svg-full` browser component for reliable
local formula rendering. MathJax is licensed under Apache-2.0; its license is
included at `docs/vendor/mathjax/LICENSE`.
