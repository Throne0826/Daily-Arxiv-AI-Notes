---
title: AI 研究版图
description: 用研究分布、每日变化与多标签关联探索 LLM、生成与多模态、决策与具身方向的 arXiv 论文。
hide:
  - toc
---

<div class="research-map" data-research-map>

<header class="research-map__header">
<p class="research-map__eyebrow">LIVE RESEARCH LANDSCAPE</p>
<h1>AI 研究版图</h1>
<p>把 60 篇论文看成一个持续变化的研究网络：节点表示细分方向，节点大小表示累计论文量，连线来自同一论文的多标签共现。</p>
</header>

<section class="research-map__metrics" aria-label="论文版图概览">
<div><strong>60</strong><span>不重复论文</span></div>
<div><strong>113</strong><span>方向归属</span></div>
<div><strong>57%</strong><span>多标签论文</span></div>
<div><strong>8</strong><span>跨主域论文</span></div>
</section>

<div class="research-map__toolbar" role="tablist" aria-label="研究地图视图">
<button type="button" class="is-active" role="tab" aria-selected="true" data-map-view="landscape">研究版图</button>
<button type="button" role="tab" aria-selected="false" data-map-view="trend">每日变化</button>
<button type="button" role="tab" aria-selected="false" data-map-view="network">方向关联</button>
</div>

<section class="research-map__panel is-active" role="tabpanel" data-map-panel="landscape">
<div class="research-domain-grid">

<section class="research-domain" data-map-group="llm">
<div class="research-domain__head">
<h2>LLM</h2>
<span>81 条归属</span>
</div>
<div class="research-node-field">
<a class="research-node" href="llm_reasoning/" style="--node-size:5.86rem" data-map-group="llm" title="LLM Reasoning：5 篇"><strong>5</strong><span>LLM Reasoning</span><small>最新日 -1</small></a>
<a class="research-node" href="llm_agent/" style="--node-size:6.88rem" data-map-group="llm" title="LLM Agent：13 篇"><strong>13</strong><span>LLM Agent</span><small>最新日 +5</small></a>
<a class="research-node" href="multi_agent/" style="--node-size:5.25rem" data-map-group="llm" title="Multi-Agent：2 篇"><strong>2</strong><span>Multi-Agent</span><small>最新日 +2</small></a>
<a class="research-node" href="llm_alignment/" style="--node-size:5.86rem" data-map-group="llm" title="对齐 / RLHF：5 篇"><strong>5</strong><span>对齐 / RLHF</span><small>最新日 -1</small></a>
<a class="research-node" href="llm_safety/" style="--node-size:6.43rem" data-map-group="llm" title="LLM 安全：9 篇"><strong>9</strong><span>LLM 安全</span><small>最新日 +5</small></a>
<a class="research-node" href="hallucination/" style="--node-size:4.94rem" data-map-group="llm" title="幻觉检测：1 篇"><strong>1</strong><span>幻觉检测</span><small>最新日 +1</small></a>
<a class="research-node" href="llm_evaluation/" style="--node-size:6.98rem" data-map-group="llm" title="LLM 评测：14 篇"><strong>14</strong><span>LLM 评测</span><small>最新日 +6</small></a>
<a class="research-node" href="llm_efficiency/" style="--node-size:6.02rem" data-map-group="llm" title="LLM 效率：6 篇"><strong>6</strong><span>LLM 效率</span><small>最新日 +4</small></a>
<a class="research-node" href="llm_pretraining/" style="--node-size:4.20rem" data-map-group="llm" title="预训练：0 篇"><strong>0</strong><span>预训练</span><small>最新日持平</small></a>
<a class="research-node" href="knowledge_editing/" style="--node-size:4.94rem" data-map-group="llm" title="知识编辑：1 篇"><strong>1</strong><span>知识编辑</span><small>最新日 +1</small></a>
<a class="research-node" href="llm_interpretability/" style="--node-size:5.68rem" data-map-group="llm" title="LLM 机制与可解释性：4 篇"><strong>4</strong><span>LLM 机制与可解释性</span><small>最新日 +2</small></a>
<a class="research-node" href="llm_nlp/" style="--node-size:7.60rem" data-map-group="llm" title="LLM 其他：21 篇"><strong>21</strong><span>LLM 其他</span><small>最新日 +11</small></a>
</div>
</section>

<section class="research-domain" data-map-group="generation_multimodal">
<div class="research-domain__head">
<h2>生成与多模态</h2>
<span>6 条归属</span>
</div>
<div class="research-node-field">
<a class="research-node" href="image_generation/" style="--node-size:4.20rem" data-map-group="generation_multimodal" title="图像生成：0 篇"><strong>0</strong><span>图像生成</span><small>最新日持平</small></a>
<a class="research-node" href="video_generation/" style="--node-size:4.94rem" data-map-group="generation_multimodal" title="视频生成：1 篇"><strong>1</strong><span>视频生成</span><small>最新日 +1</small></a>
<a class="research-node" href="multimodal_vlm/" style="--node-size:5.68rem" data-map-group="generation_multimodal" title="多模态 VLM：4 篇"><strong>4</strong><span>多模态 VLM</span><small>最新日 +4</small></a>
<a class="research-node" href="vlm_reasoning/" style="--node-size:4.20rem" data-map-group="generation_multimodal" title="VLM Reasoning：0 篇"><strong>0</strong><span>VLM Reasoning</span><small>最新日持平</small></a>
<a class="research-node" href="vlm_efficiency/" style="--node-size:4.94rem" data-map-group="generation_multimodal" title="VLM Efficiency：1 篇"><strong>1</strong><span>VLM Efficiency</span><small>最新日 +1</small></a>
</div>
</section>

<section class="research-domain" data-map-group="decision_embodied">
<div class="research-domain__head">
<h2>决策与具身</h2>
<span>26 条归属</span>
</div>
<div class="research-node-field">
<a class="research-node" href="autonomous_driving/" style="--node-size:4.20rem" data-map-group="decision_embodied" title="自动驾驶：0 篇"><strong>0</strong><span>自动驾驶</span><small>最新日持平</small></a>
<a class="research-node" href="robotics/" style="--node-size:7.43rem" data-map-group="decision_embodied" title="机器人 / 具身智能：19 篇"><strong>19</strong><span>机器人 / 具身智能</span><small>最新日 +15</small></a>
<a class="research-node" href="reinforcement_learning/" style="--node-size:6.02rem" data-map-group="decision_embodied" title="强化学习：6 篇"><strong>6</strong><span>强化学习</span><small>最新日 +4</small></a>
<a class="research-node" href="recommender/" style="--node-size:4.94rem" data-map-group="decision_embodied" title="推荐系统：1 篇"><strong>1</strong><span>推荐系统</span><small>最新日 +1</small></a>
</div>
</section>

</div>
</section>

<section class="research-map__panel" role="tabpanel" data-map-panel="trend" hidden>
<div class="research-trend">
<div class="research-trend__legend">
<span data-map-group="llm">LLM</span>
<span data-map-group="generation_multimodal">生成与多模态</span>
<span data-map-group="decision_embodied">决策与具身</span>
</div>

<div class="research-trend__row">
<div><time>2026-07-30</time><span>50 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:55.17%" title="LLM：32 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:8.62%" title="生成与多模态：5 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:36.21%" title="决策与具身：21 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-07-29</time><span>10 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:72.73%" title="LLM：8 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:0.00%" title="生成与多模态：0 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:27.27%" title="决策与具身：3 篇"></span>
</div>
</div>

</div>
<p class="research-map__note">同一篇多标签论文可以同时计入多个主域，因此主域计数之和可能高于当日论文数。</p>
</section>

<section class="research-map__panel" role="tabpanel" data-map-panel="network" hidden>
<div class="research-network">
<svg class="research-network__canvas" data-map-network viewBox="0 0 1000 560" role="img" aria-label="论文方向共现网络"></svg>
<aside class="research-network__detail" data-map-detail>
<span>最强关联</span>
<strong>LLM Agent × LLM 其他</strong>
<p>共有 7 篇论文同时进入这两个方向。</p>
</aside>
</div>
<ol class="research-connection-list">
<li><a href="llm_agent/">LLM Agent</a><span>×</span><a href="llm_nlp/">LLM 其他</a><strong>7</strong></li>
<li><a href="llm_evaluation/">LLM 评测</a><span>×</span><a href="llm_nlp/">LLM 其他</a><strong>6</strong></li>
<li><a href="llm_agent/">LLM Agent</a><span>×</span><a href="llm_evaluation/">LLM 评测</a><strong>6</strong></li>
<li><a href="llm_alignment/">对齐 / RLHF</a><span>×</span><a href="llm_nlp/">LLM 其他</a><strong>5</strong></li>
<li><a href="llm_efficiency/">LLM 效率</a><span>×</span><a href="llm_nlp/">LLM 其他</a><strong>4</strong></li>
<li><a href="llm_nlp/">LLM 其他</a><span>×</span><a href="llm_safety/">LLM 安全</a><strong>4</strong></li>
</ol>
</section>

<script type="application/json" data-research-map-data>{"latestDate": "2026-07-30", "previousDate": "2026-07-29", "groups": [{"id": "llm", "label": "LLM", "assignments": 81, "papers": 40}, {"id": "generation_multimodal", "label": "生成与多模态", "assignments": 6, "papers": 5}, {"id": "decision_embodied", "label": "决策与具身", "assignments": 26, "papers": 24}], "categories": [{"id": "llm_reasoning", "label": "LLM Reasoning", "group": "llm", "count": 5, "latest": 2, "delta": -1, "href": "llm_reasoning/"}, {"id": "llm_agent", "label": "LLM Agent", "group": "llm", "count": 13, "latest": 9, "delta": 5, "href": "llm_agent/"}, {"id": "multi_agent", "label": "Multi-Agent", "group": "llm", "count": 2, "latest": 2, "delta": 2, "href": "multi_agent/"}, {"id": "llm_alignment", "label": "对齐 / RLHF", "group": "llm", "count": 5, "latest": 2, "delta": -1, "href": "llm_alignment/"}, {"id": "llm_safety", "label": "LLM 安全", "group": "llm", "count": 9, "latest": 7, "delta": 5, "href": "llm_safety/"}, {"id": "hallucination", "label": "幻觉检测", "group": "llm", "count": 1, "latest": 1, "delta": 1, "href": "hallucination/"}, {"id": "llm_evaluation", "label": "LLM 评测", "group": "llm", "count": 14, "latest": 10, "delta": 6, "href": "llm_evaluation/"}, {"id": "llm_efficiency", "label": "LLM 效率", "group": "llm", "count": 6, "latest": 5, "delta": 4, "href": "llm_efficiency/"}, {"id": "llm_pretraining", "label": "预训练", "group": "llm", "count": 0, "latest": 0, "delta": 0, "href": "llm_pretraining/"}, {"id": "knowledge_editing", "label": "知识编辑", "group": "llm", "count": 1, "latest": 1, "delta": 1, "href": "knowledge_editing/"}, {"id": "llm_interpretability", "label": "LLM 机制与可解释性", "group": "llm", "count": 4, "latest": 3, "delta": 2, "href": "llm_interpretability/"}, {"id": "llm_nlp", "label": "LLM 其他", "group": "llm", "count": 21, "latest": 16, "delta": 11, "href": "llm_nlp/"}, {"id": "image_generation", "label": "图像生成", "group": "generation_multimodal", "count": 0, "latest": 0, "delta": 0, "href": "image_generation/"}, {"id": "video_generation", "label": "视频生成", "group": "generation_multimodal", "count": 1, "latest": 1, "delta": 1, "href": "video_generation/"}, {"id": "multimodal_vlm", "label": "多模态 VLM", "group": "generation_multimodal", "count": 4, "latest": 4, "delta": 4, "href": "multimodal_vlm/"}, {"id": "vlm_reasoning", "label": "VLM Reasoning", "group": "generation_multimodal", "count": 0, "latest": 0, "delta": 0, "href": "vlm_reasoning/"}, {"id": "vlm_efficiency", "label": "VLM Efficiency", "group": "generation_multimodal", "count": 1, "latest": 1, "delta": 1, "href": "vlm_efficiency/"}, {"id": "autonomous_driving", "label": "自动驾驶", "group": "decision_embodied", "count": 0, "latest": 0, "delta": 0, "href": "autonomous_driving/"}, {"id": "robotics", "label": "机器人 / 具身智能", "group": "decision_embodied", "count": 19, "latest": 17, "delta": 15, "href": "robotics/"}, {"id": "reinforcement_learning", "label": "强化学习", "group": "decision_embodied", "count": 6, "latest": 5, "delta": 4, "href": "reinforcement_learning/"}, {"id": "recommender", "label": "推荐系统", "group": "decision_embodied", "count": 1, "latest": 1, "delta": 1, "href": "recommender/"}], "dates": [{"date": "2026-07-29", "papers": 10, "groups": [{"id": "llm", "label": "LLM", "count": 8}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 0}, {"id": "decision_embodied", "label": "决策与具身", "count": 3}]}, {"date": "2026-07-30", "papers": 50, "groups": [{"id": "llm", "label": "LLM", "count": 32}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 5}, {"id": "decision_embodied", "label": "决策与具身", "count": 21}]}], "connections": [{"source": "llm_agent", "target": "llm_nlp", "count": 7, "source_label": "LLM Agent", "target_label": "LLM 其他"}, {"source": "llm_evaluation", "target": "llm_nlp", "count": 6, "source_label": "LLM 评测", "target_label": "LLM 其他"}, {"source": "llm_agent", "target": "llm_evaluation", "count": 6, "source_label": "LLM Agent", "target_label": "LLM 评测"}, {"source": "llm_alignment", "target": "llm_nlp", "count": 5, "source_label": "对齐 / RLHF", "target_label": "LLM 其他"}, {"source": "llm_efficiency", "target": "llm_nlp", "count": 4, "source_label": "LLM 效率", "target_label": "LLM 其他"}, {"source": "llm_nlp", "target": "llm_safety", "count": 4, "source_label": "LLM 其他", "target_label": "LLM 安全"}, {"source": "llm_nlp", "target": "llm_reasoning", "count": 3, "source_label": "LLM 其他", "target_label": "LLM Reasoning"}, {"source": "llm_alignment", "target": "llm_reasoning", "count": 2, "source_label": "对齐 / RLHF", "target_label": "LLM Reasoning"}, {"source": "llm_interpretability", "target": "llm_reasoning", "count": 2, "source_label": "LLM 机制与可解释性", "target_label": "LLM Reasoning"}, {"source": "llm_interpretability", "target": "llm_nlp", "count": 2, "source_label": "LLM 机制与可解释性", "target_label": "LLM 其他"}, {"source": "llm_evaluation", "target": "llm_safety", "count": 2, "source_label": "LLM 评测", "target_label": "LLM 安全"}, {"source": "llm_nlp", "target": "reinforcement_learning", "count": 2, "source_label": "LLM 其他", "target_label": "强化学习"}, {"source": "llm_alignment", "target": "llm_safety", "count": 2, "source_label": "对齐 / RLHF", "target_label": "LLM 安全"}, {"source": "reinforcement_learning", "target": "robotics", "count": 2, "source_label": "强化学习", "target_label": "机器人 / 具身智能"}, {"source": "llm_alignment", "target": "llm_interpretability", "count": 1, "source_label": "对齐 / RLHF", "target_label": "LLM 机制与可解释性"}, {"source": "llm_reasoning", "target": "llm_safety", "count": 1, "source_label": "LLM Reasoning", "target_label": "LLM 安全"}, {"source": "llm_evaluation", "target": "llm_reasoning", "count": 1, "source_label": "LLM 评测", "target_label": "LLM Reasoning"}, {"source": "llm_agent", "target": "reinforcement_learning", "count": 1, "source_label": "LLM Agent", "target_label": "强化学习"}]}</script>

</div>
