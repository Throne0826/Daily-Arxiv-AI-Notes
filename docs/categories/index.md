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
<p>把 565 篇论文看成一个持续变化的研究网络：节点表示细分方向，节点大小表示累计论文量，连线来自同一论文的多标签共现。</p>
</header>

<section class="research-map__metrics" aria-label="论文版图概览">
<div><strong>565</strong><span>不重复论文</span></div>
<div><strong>1270</strong><span>方向归属</span></div>
<div><strong>78%</strong><span>多标签论文</span></div>
<div><strong>87</strong><span>跨主域论文</span></div>
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
<span>1107 条归属</span>
</div>
<div class="research-node-field">
<a class="research-node" href="llm_reasoning/" style="--node-size:7.60rem" data-map-group="llm" title="LLM Reasoning：463 篇"><strong>463</strong><span>LLM Reasoning</span><small>最新日 +7</small></a>
<a class="research-node" href="llm_agent/" style="--node-size:5.58rem" data-map-group="llm" title="LLM Agent：76 篇"><strong>76</strong><span>LLM Agent</span><small>最新日 +2</small></a>
<a class="research-node" href="multi_agent/" style="--node-size:4.83rem" data-map-group="llm" title="Multi-Agent：16 篇"><strong>16</strong><span>Multi-Agent</span><small>最新日 +1</small></a>
<a class="research-node" href="llm_alignment/" style="--node-size:5.60rem" data-map-group="llm" title="对齐 / RLHF：79 篇"><strong>79</strong><span>对齐 / RLHF</span><small>最新日 +2</small></a>
<a class="research-node" href="llm_safety/" style="--node-size:5.01rem" data-map-group="llm" title="LLM 安全：26 篇"><strong>26</strong><span>LLM 安全</span><small>最新日 -1</small></a>
<a class="research-node" href="hallucination/" style="--node-size:4.55rem" data-map-group="llm" title="幻觉检测：5 篇"><strong>5</strong><span>幻觉检测</span><small>最新日持平</small></a>
<a class="research-node" href="llm_evaluation/" style="--node-size:5.89rem" data-map-group="llm" title="LLM 评测：114 篇"><strong>114</strong><span>LLM 评测</span><small>最新日 +2</small></a>
<a class="research-node" href="llm_efficiency/" style="--node-size:5.27rem" data-map-group="llm" title="LLM 效率：46 篇"><strong>46</strong><span>LLM 效率</span><small>最新日 +1</small></a>
<a class="research-node" href="llm_pretraining/" style="--node-size:4.52rem" data-map-group="llm" title="预训练：4 篇"><strong>4</strong><span>预训练</span><small>最新日持平</small></a>
<a class="research-node" href="knowledge_editing/" style="--node-size:4.47rem" data-map-group="llm" title="知识编辑：3 篇"><strong>3</strong><span>知识编辑</span><small>最新日持平</small></a>
<a class="research-node" href="llm_interpretability/" style="--node-size:5.16rem" data-map-group="llm" title="LLM 机制与可解释性：37 篇"><strong>37</strong><span>LLM 机制与可解释性</span><small>最新日 +1</small></a>
<a class="research-node" href="llm_nlp/" style="--node-size:6.64rem" data-map-group="llm" title="LLM 其他：238 篇"><strong>238</strong><span>LLM 其他</span><small>最新日 +2</small></a>
</div>
</section>

<section class="research-domain" data-map-group="generation_multimodal">
<div class="research-domain__head">
<h2>生成与多模态</h2>
<span>71 条归属</span>
</div>
<div class="research-node-field">
<a class="research-node" href="image_generation/" style="--node-size:4.36rem" data-map-group="generation_multimodal" title="图像生成：1 篇"><strong>1</strong><span>图像生成</span><small>最新日持平</small></a>
<a class="research-node" href="video_generation/" style="--node-size:4.47rem" data-map-group="generation_multimodal" title="视频生成：3 篇"><strong>3</strong><span>视频生成</span><small>最新日持平</small></a>
<a class="research-node" href="multimodal_vlm/" style="--node-size:5.04rem" data-map-group="generation_multimodal" title="多模态 VLM：28 篇"><strong>28</strong><span>多模态 VLM</span><small>最新日持平</small></a>
<a class="research-node" href="vlm_reasoning/" style="--node-size:5.11rem" data-map-group="generation_multimodal" title="VLM Reasoning：33 篇"><strong>33</strong><span>VLM Reasoning</span><small>最新日 -1</small></a>
<a class="research-node" href="vlm_efficiency/" style="--node-size:4.59rem" data-map-group="generation_multimodal" title="VLM Efficiency：6 篇"><strong>6</strong><span>VLM Efficiency</span><small>最新日持平</small></a>
</div>
</section>

<section class="research-domain" data-map-group="decision_embodied">
<div class="research-domain__head">
<h2>决策与具身</h2>
<span>92 条归属</span>
</div>
<div class="research-node-field">
<a class="research-node" href="autonomous_driving/" style="--node-size:4.52rem" data-map-group="decision_embodied" title="自动驾驶：4 篇"><strong>4</strong><span>自动驾驶</span><small>最新日 -1</small></a>
<a class="research-node" href="robotics/" style="--node-size:5.28rem" data-map-group="decision_embodied" title="机器人 / 具身智能：47 篇"><strong>47</strong><span>机器人 / 具身智能</span><small>最新日持平</small></a>
<a class="research-node" href="reinforcement_learning/" style="--node-size:5.07rem" data-map-group="decision_embodied" title="强化学习：30 篇"><strong>30</strong><span>强化学习</span><small>最新日持平</small></a>
<a class="research-node" href="recommender/" style="--node-size:4.72rem" data-map-group="decision_embodied" title="推荐系统：11 篇"><strong>11</strong><span>推荐系统</span><small>最新日 +1</small></a>
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
<div><time>2026-09-04</time><span>21 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:91.30%" title="LLM：21 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:0.00%" title="生成与多模态：0 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:8.70%" title="决策与具身：2 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-09-03</time><span>14 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:82.35%" title="LLM：14 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:5.88%" title="生成与多模态：1 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:11.76%" title="决策与具身：2 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-09-02</time><span>34 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:85.00%" title="LLM：34 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:12.50%" title="生成与多模态：5 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:2.50%" title="决策与具身：1 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-09-01</time><span>50 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:87.72%" title="LLM：50 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:7.02%" title="生成与多模态：4 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:5.26%" title="决策与具身：3 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-08-31</time><span>23 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:88.46%" title="LLM：23 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:3.85%" title="生成与多模态：1 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:7.69%" title="决策与具身：2 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-08-28</time><span>33 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:89.19%" title="LLM：33 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:0.00%" title="生成与多模态：0 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:10.81%" title="决策与具身：4 篇"></span>
</div>
</div>

<div class="research-trend__row">
<div><time>2026-08-24</time><span>17 篇论文</span></div>
<div class="research-trend__bar" aria-label="各主域相关论文占比">
<span data-map-group="llm" style="--segment-share:100.00%" title="LLM：17 篇"></span>
<span data-map-group="generation_multimodal" style="--segment-share:0.00%" title="生成与多模态：0 篇"></span>
<span data-map-group="decision_embodied" style="--segment-share:0.00%" title="决策与具身：0 篇"></span>
</div>
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
<p>共有 209 篇论文同时进入这两个方向。</p>
</aside>
</div>
<ol class="research-connection-list">
<li><a href="llm_nlp/">LLM 其他</a><span>×</span><a href="llm_reasoning/">LLM Reasoning</a><strong>209</strong></li>
<li><a href="llm_evaluation/">LLM 评测</a><span>×</span><a href="llm_reasoning/">LLM Reasoning</a><strong>97</strong></li>
<li><a href="llm_alignment/">对齐 / RLHF</a><span>×</span><a href="llm_reasoning/">LLM Reasoning</a><strong>74</strong></li>
<li><a href="llm_evaluation/">LLM 评测</a><span>×</span><a href="llm_nlp/">LLM 其他</a><strong>56</strong></li>
<li><a href="llm_agent/">LLM Agent</a><span>×</span><a href="llm_reasoning/">LLM Reasoning</a><strong>54</strong></li>
<li><a href="llm_alignment/">对齐 / RLHF</a><span>×</span><a href="llm_nlp/">LLM 其他</a><strong>38</strong></li>
</ol>
</section>

<script type="application/json" data-research-map-data>{"latestDate": "2026-09-04", "previousDate": "2026-09-03", "groups": [{"id": "llm", "label": "LLM", "assignments": 1107, "papers": 520}, {"id": "generation_multimodal", "label": "生成与多模态", "assignments": 71, "papers": 52}, {"id": "decision_embodied", "label": "决策与具身", "assignments": 92, "papers": 87}], "categories": [{"id": "llm_reasoning", "label": "LLM Reasoning", "group": "llm", "count": 463, "latest": 21, "delta": 7, "href": "llm_reasoning/"}, {"id": "llm_agent", "label": "LLM Agent", "group": "llm", "count": 76, "latest": 3, "delta": 2, "href": "llm_agent/"}, {"id": "multi_agent", "label": "Multi-Agent", "group": "llm", "count": 16, "latest": 1, "delta": 1, "href": "multi_agent/"}, {"id": "llm_alignment", "label": "对齐 / RLHF", "group": "llm", "count": 79, "latest": 5, "delta": 2, "href": "llm_alignment/"}, {"id": "llm_safety", "label": "LLM 安全", "group": "llm", "count": 26, "latest": 0, "delta": -1, "href": "llm_safety/"}, {"id": "hallucination", "label": "幻觉检测", "group": "llm", "count": 5, "latest": 0, "delta": 0, "href": "hallucination/"}, {"id": "llm_evaluation", "label": "LLM 评测", "group": "llm", "count": 114, "latest": 4, "delta": 2, "href": "llm_evaluation/"}, {"id": "llm_efficiency", "label": "LLM 效率", "group": "llm", "count": 46, "latest": 1, "delta": 1, "href": "llm_efficiency/"}, {"id": "llm_pretraining", "label": "预训练", "group": "llm", "count": 4, "latest": 0, "delta": 0, "href": "llm_pretraining/"}, {"id": "knowledge_editing", "label": "知识编辑", "group": "llm", "count": 3, "latest": 0, "delta": 0, "href": "knowledge_editing/"}, {"id": "llm_interpretability", "label": "LLM 机制与可解释性", "group": "llm", "count": 37, "latest": 3, "delta": 1, "href": "llm_interpretability/"}, {"id": "llm_nlp", "label": "LLM 其他", "group": "llm", "count": 238, "latest": 9, "delta": 2, "href": "llm_nlp/"}, {"id": "image_generation", "label": "图像生成", "group": "generation_multimodal", "count": 1, "latest": 0, "delta": 0, "href": "image_generation/"}, {"id": "video_generation", "label": "视频生成", "group": "generation_multimodal", "count": 3, "latest": 0, "delta": 0, "href": "video_generation/"}, {"id": "multimodal_vlm", "label": "多模态 VLM", "group": "generation_multimodal", "count": 28, "latest": 0, "delta": 0, "href": "multimodal_vlm/"}, {"id": "vlm_reasoning", "label": "VLM Reasoning", "group": "generation_multimodal", "count": 33, "latest": 0, "delta": -1, "href": "vlm_reasoning/"}, {"id": "vlm_efficiency", "label": "VLM Efficiency", "group": "generation_multimodal", "count": 6, "latest": 0, "delta": 0, "href": "vlm_efficiency/"}, {"id": "autonomous_driving", "label": "自动驾驶", "group": "decision_embodied", "count": 4, "latest": 0, "delta": -1, "href": "autonomous_driving/"}, {"id": "robotics", "label": "机器人 / 具身智能", "group": "decision_embodied", "count": 47, "latest": 0, "delta": 0, "href": "robotics/"}, {"id": "reinforcement_learning", "label": "强化学习", "group": "decision_embodied", "count": 30, "latest": 1, "delta": 0, "href": "reinforcement_learning/"}, {"id": "recommender", "label": "推荐系统", "group": "decision_embodied", "count": 11, "latest": 1, "delta": 1, "href": "recommender/"}], "dates": [{"date": "2026-07-29", "papers": 10, "groups": [{"id": "llm", "label": "LLM", "count": 8}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 0}, {"id": "decision_embodied", "label": "决策与具身", "count": 3}]}, {"date": "2026-07-30", "papers": 50, "groups": [{"id": "llm", "label": "LLM", "count": 32}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 5}, {"id": "decision_embodied", "label": "决策与具身", "count": 21}]}, {"date": "2026-07-31", "papers": 50, "groups": [{"id": "llm", "label": "LLM", "count": 25}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 6}, {"id": "decision_embodied", "label": "决策与具身", "count": 29}]}, {"date": "2026-08-03", "papers": 12, "groups": [{"id": "llm", "label": "LLM", "count": 12}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 0}, {"id": "decision_embodied", "label": "决策与具身", "count": 3}]}, {"date": "2026-08-04", "papers": 51, "groups": [{"id": "llm", "label": "LLM", "count": 51}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 10}, {"id": "decision_embodied", "label": "决策与具身", "count": 5}]}, {"date": "2026-08-05", "papers": 37, "groups": [{"id": "llm", "label": "LLM", "count": 37}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 4}, {"id": "decision_embodied", "label": "决策与具身", "count": 5}]}, {"date": "2026-08-06", "papers": 28, "groups": [{"id": "llm", "label": "LLM", "count": 28}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 4}, {"id": "decision_embodied", "label": "决策与具身", "count": 1}]}, {"date": "2026-08-10", "papers": 15, "groups": [{"id": "llm", "label": "LLM", "count": 15}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 1}, {"id": "decision_embodied", "label": "决策与具身", "count": 1}]}, {"date": "2026-08-12", "papers": 19, "groups": [{"id": "llm", "label": "LLM", "count": 19}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 4}, {"id": "decision_embodied", "label": "决策与具身", "count": 1}]}, {"date": "2026-08-13", "papers": 18, "groups": [{"id": "llm", "label": "LLM", "count": 18}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 4}, {"id": "decision_embodied", "label": "决策与具身", "count": 1}]}, {"date": "2026-08-14", "papers": 28, "groups": [{"id": "llm", "label": "LLM", "count": 28}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 3}, {"id": "decision_embodied", "label": "决策与具身", "count": 1}]}, {"date": "2026-08-17", "papers": 16, "groups": [{"id": "llm", "label": "LLM", "count": 16}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 0}, {"id": "decision_embodied", "label": "决策与具身", "count": 0}]}, {"date": "2026-08-18", "papers": 33, "groups": [{"id": "llm", "label": "LLM", "count": 33}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 0}, {"id": "decision_embodied", "label": "决策与具身", "count": 1}]}, {"date": "2026-08-21", "papers": 6, "groups": [{"id": "llm", "label": "LLM", "count": 6}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 0}, {"id": "decision_embodied", "label": "决策与具身", "count": 1}]}, {"date": "2026-08-24", "papers": 17, "groups": [{"id": "llm", "label": "LLM", "count": 17}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 0}, {"id": "decision_embodied", "label": "决策与具身", "count": 0}]}, {"date": "2026-08-28", "papers": 33, "groups": [{"id": "llm", "label": "LLM", "count": 33}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 0}, {"id": "decision_embodied", "label": "决策与具身", "count": 4}]}, {"date": "2026-08-31", "papers": 23, "groups": [{"id": "llm", "label": "LLM", "count": 23}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 1}, {"id": "decision_embodied", "label": "决策与具身", "count": 2}]}, {"date": "2026-09-01", "papers": 50, "groups": [{"id": "llm", "label": "LLM", "count": 50}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 4}, {"id": "decision_embodied", "label": "决策与具身", "count": 3}]}, {"date": "2026-09-02", "papers": 34, "groups": [{"id": "llm", "label": "LLM", "count": 34}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 5}, {"id": "decision_embodied", "label": "决策与具身", "count": 1}]}, {"date": "2026-09-03", "papers": 14, "groups": [{"id": "llm", "label": "LLM", "count": 14}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 1}, {"id": "decision_embodied", "label": "决策与具身", "count": 2}]}, {"date": "2026-09-04", "papers": 21, "groups": [{"id": "llm", "label": "LLM", "count": 21}, {"id": "generation_multimodal", "label": "生成与多模态", "count": 0}, {"id": "decision_embodied", "label": "决策与具身", "count": 2}]}], "connections": [{"source": "llm_nlp", "target": "llm_reasoning", "count": 209, "source_label": "LLM 其他", "target_label": "LLM Reasoning"}, {"source": "llm_evaluation", "target": "llm_reasoning", "count": 97, "source_label": "LLM 评测", "target_label": "LLM Reasoning"}, {"source": "llm_alignment", "target": "llm_reasoning", "count": 74, "source_label": "对齐 / RLHF", "target_label": "LLM Reasoning"}, {"source": "llm_evaluation", "target": "llm_nlp", "count": 56, "source_label": "LLM 评测", "target_label": "LLM 其他"}, {"source": "llm_agent", "target": "llm_reasoning", "count": 54, "source_label": "LLM Agent", "target_label": "LLM Reasoning"}, {"source": "llm_alignment", "target": "llm_nlp", "count": 38, "source_label": "对齐 / RLHF", "target_label": "LLM 其他"}, {"source": "llm_efficiency", "target": "llm_reasoning", "count": 38, "source_label": "LLM 效率", "target_label": "LLM Reasoning"}, {"source": "llm_agent", "target": "llm_nlp", "count": 35, "source_label": "LLM Agent", "target_label": "LLM 其他"}, {"source": "llm_interpretability", "target": "llm_reasoning", "count": 34, "source_label": "LLM 机制与可解释性", "target_label": "LLM Reasoning"}, {"source": "llm_reasoning", "target": "vlm_reasoning", "count": 33, "source_label": "LLM Reasoning", "target_label": "VLM Reasoning"}, {"source": "llm_efficiency", "target": "llm_nlp", "count": 23, "source_label": "LLM 效率", "target_label": "LLM 其他"}, {"source": "llm_reasoning", "target": "reinforcement_learning", "count": 21, "source_label": "LLM Reasoning", "target_label": "强化学习"}, {"source": "llm_reasoning", "target": "multimodal_vlm", "count": 18, "source_label": "LLM Reasoning", "target_label": "多模态 VLM"}, {"source": "llm_reasoning", "target": "llm_safety", "count": 17, "source_label": "LLM Reasoning", "target_label": "LLM 安全"}, {"source": "llm_alignment", "target": "reinforcement_learning", "count": 16, "source_label": "对齐 / RLHF", "target_label": "强化学习"}, {"source": "llm_interpretability", "target": "llm_nlp", "count": 15, "source_label": "LLM 机制与可解释性", "target_label": "LLM 其他"}, {"source": "llm_nlp", "target": "reinforcement_learning", "count": 14, "source_label": "LLM 其他", "target_label": "强化学习"}, {"source": "llm_agent", "target": "llm_evaluation", "count": 14, "source_label": "LLM Agent", "target_label": "LLM 评测"}]}</script>

</div>
