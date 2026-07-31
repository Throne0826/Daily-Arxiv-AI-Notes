---
title: Daily arXiv AI Notes
description: 每日筛选 LLM、生成与多模态、决策与具身领域的 arXiv 新论文，并生成适合从零阅读的中文研究笔记。
hide:
  - navigation
  - toc
---

<div class="home-shell">

<section class="home-hero" aria-labelledby="home-title">
  <canvas id="home-scene" aria-hidden="true"></canvas>
  <div class="home-hero__content">
    <p class="home-kicker">DAILY ARXIV · AI RESEARCH MAP</p>
    <h1 id="home-title">Daily arXiv AI Notes</h1>
    <p class="home-deck">从每天涌入 arXiv 的论文里，筛出值得细读的工作；把研究背景、动机、方法与实验，整理成真正能读懂的中文笔记。</p>
    <div class="home-actions">
      <a class="home-action home-action--primary" href="arxiv_daily/">浏览每日论文</a>
      <a class="home-action" href="categories/">进入研究地图</a>
    </div>
    <dl class="home-signals">
      <div><dt>3</dt><dd>研究主域</dd></div>
      <div><dt>21</dt><dd>细分方向</dd></div>
      <div><dt>全文级</dt><dd>中文解析</dd></div>
    </dl>
  </div>
  <div class="home-stream" aria-hidden="true">
    <span>LLM Reasoning</span><span>Agentic RL</span><span>Multimodal</span><span>Embodied AI</span>
  </div>
</section>

<section class="home-band home-intro" aria-labelledby="home-intro-title">
  <div class="home-section__head">
    <p class="home-section__index">01 / READING PIPELINE</p>
    <h2 id="home-intro-title">从论文列表，到可复用的研究理解</h2>
  </div>
  <div class="home-reading-lab" data-active-step="0">
    <figure class="home-reading-visual" aria-label="论文从原始列表转化为结构化中文笔记的动态示意图">
      <div class="home-visual__rail" aria-hidden="true">
        <span>ARXIV FEED</span><i></i><span>RESEARCH NOTE</span>
      </div>
      <div class="home-visual__stage" aria-hidden="true">
        <div class="home-feed-stack">
          <div class="home-feed-paper"><b>2607.31</b><span></span><span></span><em>cs.CL</em></div>
          <div class="home-feed-paper"><b>2607.30</b><span></span><span></span><em>cs.RO</em></div>
          <div class="home-feed-paper"><b>2607.29</b><span></span><span></span><em>cs.CV</em></div>
        </div>
        <div class="home-analysis-core">
          <span class="home-core-ring home-core-ring--one"></span>
          <span class="home-core-ring home-core-ring--two"></span>
          <strong>AI</strong>
          <i class="home-core-scan"></i>
        </div>
        <div class="home-note-sheet">
          <div class="home-note-sheet__head"><span>研究笔记</span><b>ZH</b></div>
          <div class="home-note-sheet__title"></div>
          <div class="home-note-sheet__line"></div>
          <div class="home-note-sheet__line home-note-sheet__line--short"></div>
          <div class="home-note-sheet__formula">L(θ) = E[r · log π<sub>θ</sub>]</div>
          <div class="home-note-sheet__chart"><i></i><i></i><i></i><i></i></div>
        </div>
        <span class="home-flow-dot home-flow-dot--one"></span>
        <span class="home-flow-dot home-flow-dot--two"></span>
        <span class="home-flow-dot home-flow-dot--three"></span>
      </div>
      <figcaption class="home-visual__caption">
        <span>当前处理</span>
        <strong data-pipeline-caption>过滤噪声，留下真正相关的工作</strong>
        <small><b data-pipeline-counter>01</b> / 04</small>
      </figcaption>
    </figure>

    <ol class="home-pipeline">
      <li class="is-active" data-pipeline-step="0" tabindex="0">
        <span>01</span><strong>筛选</strong><p>按日获取新投稿与跨区投稿，去重后聚焦真正相关的研究问题。</p>
      </li>
      <li data-pipeline-step="1" tabindex="0">
        <span>02</span><strong>归类</strong><p>一篇论文可进入多个相关方向，保留它在研究地图中的真实连接。</p>
      </li>
      <li data-pipeline-step="2" tabindex="0">
        <span>03</span><strong>深读</strong><p>从全文定位背景、动机、方法、公式与实验，而不是只改写摘要。</p>
      </li>
      <li data-pipeline-step="3" tabindex="0">
        <span>04</span><strong>校验</strong><p>关键数字关联原文证据，清楚区分作者结论与辅助分析。</p>
      </li>
    </ol>
  </div>
</section>

<section class="home-band home-fields" aria-labelledby="home-fields-title">
  <div class="home-section__head">
    <p class="home-section__index">02 / RESEARCH FIELDS</p>
    <h2 id="home-fields-title">沿着问题，而不是关键词浏览论文</h2>
  </div>
  <div class="home-field-grid">
    <section data-domain="llm">
      <p class="home-field__code">LLM</p>
      <h3>语言、推理与智能体</h3>
      <p><a href="categories/llm_reasoning/">推理</a> · <a href="categories/llm_agent/">Agent</a> · <a href="categories/multi_agent/">多智能体</a> · <a href="categories/llm_alignment/">对齐 / RLHF</a> · <a href="categories/llm_safety/">安全</a> · <a href="categories/llm_evaluation/">评测</a> · <a href="categories/llm_interpretability/">机制与可解释性</a></p>
    </section>
    <section data-domain="generation_multimodal">
      <p class="home-field__code">GEN / MM</p>
      <h3>生成与多模态</h3>
      <p><a href="categories/image_generation/">图像生成</a> · <a href="categories/video_generation/">视频生成</a> · <a href="categories/multimodal_vlm/">多模态 VLM</a> · <a href="categories/vlm_reasoning/">VLM Reasoning</a> · <a href="categories/vlm_efficiency/">VLM Efficiency</a></p>
    </section>
    <section data-domain="decision_embodied">
      <p class="home-field__code">DECISION</p>
      <h3>决策与具身</h3>
      <p><a href="categories/autonomous_driving/">自动驾驶</a> · <a href="categories/robotics/">机器人 / 具身智能</a> · <a href="categories/reinforcement_learning/">强化学习</a> · <a href="categories/recommender/">推荐系统</a></p>
    </section>
  </div>
</section>

<section class="home-band home-standard" aria-labelledby="home-standard-title">
  <p class="home-section__index">03 / NOTE STANDARD</p>
  <div>
    <h2 id="home-standard-title">每篇笔记只回答四件关键的事</h2>
    <p>先用速览判断是否值得读，再沿研究背景、动机、方法与实验四个章节深入；必要概念保留，补充证据按需展开。</p>
  </div>
  <a class="home-text-link" href="arxiv_daily/">开始阅读论文</a>
</section>

</div>
