---
title: 搜索每日 arXiv 论文
description: 按标题、关键词和细分领域检索每日 arXiv 中文论文笔记。
hide:
  - toc
---

# 搜索论文

<div id="daily-search-root">
  <div class="daily-search-controls">
    <label for="daily-search-input">标题或关键词</label>
    <input id="daily-search-input" type="search" autocomplete="off" placeholder="例如 verifier drift、agentic RL、视频生成">
    <label for="daily-search-category">细分领域</label>
    <select id="daily-search-category">
      <option value="">全部领域</option>
    </select>
  </div>
  <p id="daily-search-status" role="status" aria-live="polite">正在加载索引...</p>
  <ol id="daily-search-results"></ol>
</div>
