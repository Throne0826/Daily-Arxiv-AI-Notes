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
<p>把 373 篇论文看成一个持续变化的研究网络：节点表示细分方向，节点大小表示累计论文量，连线来自同一论文的多标签共现。</p>
</header>

<section class="research-map__metrics" aria-label="论文版图概览">
<div><strong>373</strong><span>不重复论文</span></div>
<div><strong>803</strong><span>方向归属</span></div>
<div><strong>73%</strong><span>多标签论文</span></div>
<div><strong>64</strong><span>跨主域论文</span></div>
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
<span>668 条归属</span>
</div>
<div class="research-node-field">
<a class="research-node" href="llm_reasoning/" style="--node-size:7.60rem" data-map-group="llm" title="LLM Reasoning：271 篇"><strong>271</strong><span>LLM Reasoning</span><small>最新日 -27</small></a>
<a class="research-node" href="llm_agent/" style="--node-size:5.76rem" data-map-group="llm" title="LLM Agent：57 篇"><strong>57</strong><span>LLM Agent</span><small>最新日 -3</small></a>
<a class="research-node" href="multi_agent/" style="--node-size:4.92rem" data-map-group="llm" title="Multi-Agent：12 篇"><strong>12</strong><span>Multi-Agent</span><small>最新日 -2</small></a>
<a class="research-node" href="llm_alignment/" style="--node-size:5.59rem" data-map-group="llm" title="对齐 / RLHF：45 篇"><strong>45</strong><span>对齐 / RLHF</span><small>最新日 -2</small></a>
<a class="research-node" href="llm_safety/" style="--node-size:5.10rem" data-map-group="llm" title="LLM 安全：19 篇"><strong>19</strong><span>LLM 安全</span><small>最新日 -1</small></a>
<a class="research-node" href="hallucination/" style="--node-size:4.49rem" data-map-group="llm" title="幻觉检测：2 篇"><strong>2</strong><span>幻觉检测</span><small>最新日持平</small></a>
<a class="research-node" href="llm_evaluation/" style="--node-size:5.96rem" data-map-group="llm" title="LLM 评测：73 篇"><strong>73</strong><span>LLM 评测</span><small>最新日 -7</small></a>
<a class="research-node" href="llm_efficiency/" style="--node-size:5.31rem" data-map-group="llm" title="LLM 效率：29 篇"><strong>29</strong><span>LLM 效率</span><small>最新日 -2</small></a>
<a class="research-node" href="llm_pretraining/" style="--node-size:4.49rem" data-map-group="llm" title="预训练：2 篇"><strong>2</strong><span>预训练</span><small>最新日持平</small></a>
<a class="research-node" href="knowledge_editing/" style="--node-size:4.56rem" data-map-group="llm" title="知识编辑：3 篇"><strong>3</strong><span>知识编辑</span><small>最新日持平</small></a>
<a class="research-node" href="llm_interpretability/" style="--node-size:5.05rem" data-map-group="llm" title="LLM 机制与可解释性：17 篇"><strong>17</strong><span>LLM 机制与可解释性</span><small>最新日持平</small></a>
<a class="research-node" href="llm_nlp/" style="--node-size:6.63rem" data-map-group="llm" title="LLM 其他：138 篇"><strong>138</strong><span>LLM 其他</span><small>最新日 -1</small></a>
</div>
</section>

<section class="research-domain" data-map-group="generation_multimodal">
<div class="research-domain__head">
<h2>生成与多模态</h2>
<span>57 条归属</span>
</div>
<div class="research-node-field">
<a class="research-node" href="image_generation/" style="--node-size:4.41rem" data-map-group="generation_multimodal" title="图像生成：1 篇"><strong>1</strong><span>图像生成</span><small>最新日持平</small></a>
<a class="research-node" href="video_generation/" style="--node-size:4.49rem" data-map-group="generation_multimodal" title="视频生成：2 篇"><strong>2</strong><span>视频生成</span><small>最新日持平</small></a>
<a class="research-node" href="multimodal_vlm/" style="--node-size:5.19rem" data-map-group="generation_multimodal" title="多模态 VLM：23 篇"><strong>23</strong><span>多模态 VLM</span><small>最新日持平</small></a>
<a class="research-node" href="vlm_reasoning/" style="--node-size:5.23rem" data-map-group="generation_multimodal" title="VLM Reasoning：25 篇"><strong>25</strong><span>VLM Reasoning</span><small>最新日持平</small></a>
<a class="research-node" href="vlm_efficiency/" style="--node-size:4.71rem" data-map-group="generation_multimodal" title="VLM Efficiency：6 篇"><strong>6</strong><span>VLM Efficiency</span><small>最新日持平</small></a>
</div>
</section>

<section class="research-domain" data-map-group="decision_embodied">
<div class="research-domain__head">
<h2>决策与具身</h2>
<span>78 条归属</span>
</div>
<div class="research-node-field">
<a class="research-node" href="autonomous_driving/" style="--node-size:4.56rem" data-map-group="decision_embodied" title="自动驾驶：3 篇"><strong>3</strong><span>自动驾驶</span><small>最新日持平</small></a>
<a class="research-node" href="robotics/" style="--node-size:5.59rem" data-map-group="decision_embodied" title="机器人 / 具身智能：45 篇"><strong>45</strong><span>机器人 / 具身智能</span><small>最新日 +1</small></a>
<a class="research-node" href="reinforcement_learning/" style="--node-size:5.12rem" data-map-group="decision_embodied" title="强化学习：20 篇"><strong>20</strong><span>强化学习</span><small>最新日 -1</small></a>
<a class="research-node" href="recommender/" style="--node-size:4.85rem" data-map-group="decision_embodied" title="推荐系统：10 篇"><strong>10</strong><span>推荐系统</span><small>最新日持平</small></a>
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
<div><time>2026-08-21</time><span>6 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:85.71%" title="LLM：6 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:0.00%" title="生成与多模态：0 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:14.29%" title="决策与具身：1 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-08-18</time><span>33 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:97.06%" title="LLM：33 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:0.00%" title="生成与多模态：0 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:2.94%" title="决策与具身：1 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-08-17</time><span>16 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:100.00%" title="LLM：16 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:0.00%" title="生成与多模态：0 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:0.00%" title="决策与具身：0 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-08-14</time><span>28 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:87.50%" title="LLM：28 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:9.38%" title="生成与多模态：3 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:3.12%" title="决策与具身：1 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-08-13</time><span>18 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:78.26%" title="LLM：18 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:17.39%" title="生成与多模态：4 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:4.35%" title="决策与具身：1 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-08-12</time><span>19 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:79.17%" title="LLM：19 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:16.67%" title="生成与多模态：4 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:4.17%" title="决策与具身：1 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-08-10</time><span>15 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:88.24%" title="LLM：15 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:5.88%" title="生成与多模态：1 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:5.88%" title="决策与具身：1 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-08-06</time><span>28 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:84.85%" title="LLM：28 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:12.12%" title="生成与多模态：4 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:3.03%" title="决策与具身：1 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-08-05</time><span>37 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:80.43%" title="LLM：37 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:8.70%" title="生成与多模态：4 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:10.87%" title="决策与具身：5 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-08-04</time><span>51 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:77.27%" title="LLM：51 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:15.15%" title="生成与多模态：10 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:7.58%" title="决策与具身：5 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-08-03</time><span>12 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:80.00%" title="LLM：12 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:0.00%" title="生成与多模态：0 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:20.00%" title="决策与具身：3 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-07-31</time><span>50 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:41.67%" title="LLM：25 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:10.00%" title="生成与多模态：6 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:48.33%" title="决策与具身：29 篇"></span>
</div>
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
<strong>LLM 其他 × LLM Reasoning</strong>
<p>共有 109 篇论文同时进入这两个方向。</p>
</aside>
</div>
<ol class="research-connection-list">
<li><a href="llm_nlp/">LLM 其他</a><span>×</span><a href="llm_reasoning/">LLM Reasoning</a><strong>109</strong></li>
<li><a href="llm_evaluation/">LLM 评测</a><span>×</span><a href="llm_reasoning/">LLM Reasoning</a><strong>56</strong></li>
<li><a href="llm_alignment/">对齐 / RLHF</a><span>×</span><a href="llm_reasoning/">LLM Reasoning</a><strong>40</strong></li>
<li><a href="llm_agent/">LLM Agent</a><span>×</span><a href="llm_reasoning/">LLM Reasoning</a><strong>35</strong></li>
<li><a href="llm_evaluation/">LLM 评测</a><span>×</span><a href="llm_nlp/">LLM 其他</a><strong>33</strong></li>
<li><a href="llm_agent/">LLM Agent</a><span>×</span><a href="llm_nlp/">LLM 其他</a><strong>26</strong></li>
</ol>
</section>

<script type="application/json" data-research-map-data>{"latestDate": "2026-08-21", "previousDate": "2026-08-18", "groups": [{"id": "llm", "label": "LLM", "assignments": 668, "papers": 328}, {"id": "generation_multimodal", "label": "生成与多模态", "assignments": 57, "papers": 41}, {"id": "decision_embodied", "label": "决策与具身", "assignments": 78, "papers": 73}], "categories": [{"id": "llm_reasoning", "label": "LLM Reasoning", "group": "llm", "count": 271, "latest": 6, "delta": -27, "href": "llm_reasoning/"}, {"id": "llm_agent", "label": "LLM Agent", "group": "llm", "count": 57, "latest": 1, "delta": -3, "href": "llm_agent/"}, {"id": "multi_agent", "label": "Multi-Agent", "group": "llm", "count": 12, "latest": 0, "delta": -2, "href": "multi_agent/"}, {"id": "llm_alignment", "label": "对齐 / RLHF", "group": "llm", "count": 45, "latest": 0, "delta": -2, "href": "llm_alignment/"}, {"id": "llm_safety", "label": "LLM 安全", "group": "llm", "count": 19, "latest": 0, "delta": -1, "href": "llm_safety/"}, {"id": "hallucination", "label": "幻觉检测", "group": "llm", "count": 2, "latest": 0, "delta": 0, "href": "hallucination/"}, {"id": "llm_evaluation", "label": "LLM 评测", "group": "llm", "count": 73, "latest": 1, "delta": -7, "href": "llm_evaluation/"}, {"id": "llm_efficiency", "label": "LLM 效率", "group": "llm", "count": 29, "latest": 0, "delta": -2, "href": "llm_efficiency/"}, {"id": "llm_pretraining", "label": "预训练", "group": "llm", "count": 2, "latest": 0, "delta": 0, "href": "llm_pretraining/"}, {"id": "knowledge_editing", "label": "知识编辑", "group": "llm", "count": 3, "latest": 0, "delta": 0, "href": "knowledge_editing/"}, {"id": "llm_interpretability", "label": "LLM 机制与可解释性", "group": "llm", "count": 17, "latest": 1, "delta": 0, "href": "llm_interpretability/"}, {"id": "llm_nlp", "label": "LLM 其他", "group": "llm", "count": 138, "latest": 3, "delta": -1, "href": "llm_nlp/"}, {"id": "image_generation", "label": "图像生成", "group": "generation_multimodal", "count": 1, "latest": 0, "delta": 0, "href": "image_generation/"}, {"id": "video_generation", "label": "视频生成", "group": "generation_multimodal", "count": 2, "latest": 0, "delta": 0, "href": "video_generation/"}, {"id": "multimodal_vlm", "label": "多模态 VLM", "group": "generation_multimodal", "count": 23, "latest": 0, "delta": 0, "href": "multimodal_vlm/"}, {"id": "vlm_reasoning", "label": "VLM Reasoning", "group": "generation_multimodal", "count": 25, "latest": 0, "delta": 0, "href": "vlm_reasoning/"}, {"id": "vlm_efficiency", "label": "VLM Efficiency", "group": "generation_multimodal", "count": 6, "latest": 0, "delta": 0, "href": "vlm_efficiency/"}, {"id": "autonomous_driving", "label": "自动驾驶", "group": "decision_embodied", "count": 3, "latest": 0, "delta": 0, "href": "autonomous_driving/"}, {"id": "robotics", "label": "机器人 / 具身智能", "group": "decision_embodied", "count": 45, "latest": 1, "delta": 1, "href": "robotics/"}, {"id": "reinforcement_learning", "label": "强化学习", "group": "decision_embodied", "count": 20, "latest": 0, "delta": -1, "href": "reinforcement_learning/"}, {"id": "recommender", "label": "推荐系统", "group": "decision_embodied", "count": 10, "latest": 0, "delta": 0, "href": "recommender/"}], "dates": [{"date": "2026-07-29", "papers": 10, "groups": [{"id": "llm", "label": "LLM", "count": 8}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 0}, {"id": "decision_embodied", "label": "决策与具身", "count": 3}]}, {"date": "2026-07-30", "papers": 50, "groups": [{"id": "llm", "label": "LLM", "count": 32}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 5}, {"id": "decision_embodied", "label": "决策与具身", "count": 21}]}, {"date": "2026-07-31", "papers": 50, "groups": [{"id": "llm", "label": "LLM", "count": 25}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 6}, {"id": "decision_embodied", "label": "决策与具身", "count": 29}]}, {"date": "2026-08-03", "papers": 12, "groups": [{"id": "llm", "label": "LLM", "count": 12}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 0}, {"id": "decision_embodied", "label": "决策与具身", "count": 3}]}, {"date": "2026-08-04", "papers": 51, "groups": [{"id": "llm", "label": "LLM", "count": 51}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 10}, {"id": "decision_embodied", "label": "决策与具身", "count": 5}]}, {"date": "2026-08-05", "papers": 37, "groups": [{"id": "llm", "label": "LLM", "count": 37}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 4}, {"id": "decision_embodied", "label": "决策与具身", "count": 5}]}, {"date": "2026-08-06", "papers": 28, "groups": [{"id": "llm", "label": "LLM", "count": 28}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 4}, {"id": "decision_embodied", "label": "决策与具身", "count": 1}]}, {"date": "2026-08-10", "papers": 15, "groups": [{"id": "llm", "label": "LLM", "count": 15}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 1}, {"id": "decision_embodied", "label": "决策与具身", "count": 1}]}, {"date": "2026-08-12", "papers": 19, "groups": [{"id": "llm", "label": "LLM", "count": 19}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 4}, {"id": "decision_embodied", "label": "决策与具身", "count": 1}]}, {"date": "2026-08-13", "papers": 18, "groups": [{"id": "llm", "label": "LLM", "count": 18}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 4}, {"id": "decision_embodied", "label": "决策与具身", "count": 1}]}, {"date": "2026-08-14", "papers": 28, "groups": [{"id": "llm", "label": "LLM", "count": 28}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 3}, {"id": "decision_embodied", "label": "决策与具身", "count": 1}]}, {"date": "2026-08-17", "papers": 16, "groups": [{"id": "llm", "label": "LLM", "count": 16}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 0}, {"id": "decision_embodied", "label": "决策与具身", "count": 0}]}, {"date": "2026-08-18", "papers": 33, "groups": [{"id": "llm", "label": "LLM", "count": 33}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 0}, {"id": "decision_embodied", "label": "决策与具身", "count": 1}]}, {"date": "2026-08-21", "papers": 6, "groups": [{"id": "llm", "label": "LLM", "count": 6}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 0}, {"id": "decision_embodied", "label": "决策与具身", "count": 1}]}], "connections": [{"source": "llm_nlp", "target": "llm_reasoning", "count": 109, "source_label": "LLM 其他", "target_label": "LLM Reasoning"}, {"source": "llm_evaluation", "target": "llm_reasoning", "count": 56, "source_label": "LLM 评测", "target_label": "LLM Reasoning"}, {"source": "llm_alignment", "target": "llm_reasoning", "count": 40, "source_label": "对齐 / RLHF", "target_label": "LLM Reasoning"}, {"source": "llm_agent", "target": "llm_reasoning", "count": 35, "source_label": "LLM Agent", "target_label": "LLM Reasoning"}, {"source": "llm_evaluation", "target": "llm_nlp", "count": 33, "source_label": "LLM 评测", "target_label": "LLM 其他"}, {"source": "llm_agent", "target": "llm_nlp", "count": 26, "source_label": "LLM Agent", "target_label": "LLM 其他"}, {"source": "llm_reasoning", "target": "vlm_reasoning", "count": 25, "source_label": "LLM Reasoning", "target_label": "VLM Reasoning"}, {"source": "llm_alignment", "target": "llm_nlp", "count": 24, "source_label": "对齐 / RLHF", "target_label": "LLM 其他"}, {"source": "llm_efficiency", "target": "llm_reasoning", "count": 21, "source_label": "LLM 效率", "target_label": "LLM Reasoning"}, {"source": "llm_interpretability", "target": "llm_reasoning", "count": 14, "source_label": "LLM 机制与可解释性", "target_label": "LLM Reasoning"}, {"source": "llm_efficiency", "target": "llm_nlp", "count": 13, "source_label": "LLM 效率", "target_label": "LLM 其他"}, {"source": "llm_reasoning", "target": "multimodal_vlm", "count": 13, "source_label": "LLM Reasoning", "target_label": "多模态 VLM"}, {"source": "llm_reasoning", "target": "reinforcement_learning", "count": 11, "source_label": "LLM Reasoning", "target_label": "强化学习"}, {"source": "llm_reasoning", "target": "llm_safety", "count": 10, "source_label": "LLM Reasoning", "target_label": "LLM 安全"}, {"source": "llm_nlp", "target": "reinforcement_learning", "count": 9, "source_label": "LLM 其他", "target_label": "强化学习"}, {"source": "llm_agent", "target": "llm_evaluation", "count": 9, "source_label": "LLM Agent", "target_label": "LLM 评测"}, {"source": "llm_reasoning", "target": "multi_agent", "count": 9, "source_label": "LLM Reasoning", "target_label": "Multi-Agent"}, {"source": "multimodal_vlm", "target": "vlm_reasoning", "count": 9, "source_label": "多模态 VLM", "target_label": "VLM Reasoning"}]}</script>

</div>
