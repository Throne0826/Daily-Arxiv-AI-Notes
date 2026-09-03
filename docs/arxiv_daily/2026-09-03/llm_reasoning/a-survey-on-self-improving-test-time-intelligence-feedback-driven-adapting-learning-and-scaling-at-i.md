---
title: "[论文解读] A Survey on Self-Improving Test-Time Intelligence: Feedback-Driven Adapting, Learning, and Scaling at Inference"
description: "[arXiv 2609.01679][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2609.01679"
announcement_date: "2026-09-03"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-03T04:33:41.664353+00:00"
source_sha256: "9d702c9b53b92544aba60f9dfb157363e664f0466398d5c269829f5f8a8bcae4"
tags:
  - "LLM Reasoning"
  - "测试时智能"
  - "测试时学习"
  - "测试时适应"
  - "测试时扩展"
  - "反馈驱动自我改进"
  - "推理时计算"
  - "状态更新"
  - "分布偏移"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.01679</p>

# A Survey on Self-Improving Test-Time Intelligence: Feedback-Driven Adapting, Learning, and Scaling at Inference

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-03</span>
<span><strong>作者</strong> Shuaicheng Niu, Guohao Chen, Yaofo Chen, Zhiquan Wen, Jinwu Hu, Zeshuai Deng, Deyu Chen, Shuhai Zhang, Renjie Chen, Zihao Lian, Shoukai Xu, Gang Dai, Yunbei Zhang, Wei Luo, Yifan Zhang, Mingkui Tan, Cheng Deng</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> South China University of Technology；Nanyang Technological University；Tulane University；Pazhou Laboratory；National University of Singapore；Hohai University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.01679v1) · [PDF 下载](https://arxiv.org/pdf/2609.01679v1) · **关键词** 测试时智能, 测试时学习, 测试时适应, 测试时扩展, 反馈驱动自我改进, 推理时计算, 状态更新, 分布偏移<br>
**项目页**: [https://github.com/mr-eggplant/awesome_test_time_intelligence](https://github.com/mr-eggplant/awesome_test_time_intelligence)

</div>

<nav class="paper-jump" aria-label="论文解读章节">
  <a href="#研究背景"><span>01</span>研究背景</a>
  <a href="#研究动机"><span>02</span>研究动机</a>
  <a href="#研究方法"><span>03</span>研究方法</a>
  <a href="#实验"><span>04</span>实验结果</a>
</nav>

<div class="paper-quickread" markdown="1">

<div class="paper-quickread__main" markdown="1">

<span class="paper-mini-label">先用一句话判断</span>

原文未明确报告。

**不用术语来说**：原文未明确报告。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 原文未明确报告。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

传统人工智能遵循“先训练、后推理”范式：模型在训练阶段完成优化，部署后保持冻结，并对每个测试输入进行一次静态前向计算。然而，开放世界与个性化部署会持续带来分布偏移、用户需求变化以及样本难度差异，固定模型的一次性输出因而未必可靠。本文以“反馈驱动的测试时智能”（Test-Time Intelligence，TTI）统一描述部署期间的自我改进：系统利用无标签测试数据、模型反馈、环境交互结果或验证信号，通过更新内部状态、增加推理计算，或同时采用两者来改善当前及后续行为。该视角覆盖视觉、语言、多模态学习、生成模型、机器人和医疗等场景，并以“状态更新—额外计算”作为比较不同方法的共同坐标。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试时学习与测试时适应（TTL/TTA）**

测试时学习指模型在部署期间利用测试信号更新模型状态，例如归一化统计量、提示、低秩适配器、输入或完整参数。本文将测试时适应视为测试时学习的子集，其中大量工作特别关注分布偏移下的鲁棒性。

</div>
<div class="concept-item" markdown="1">

**测试时扩展（TTS）**

测试时扩展通过投入更多推理阶段资源提高预测质量，而不一定持续修改模型状态，典型手段包括重复解码、自一致性、搜索、工具调用及生成模型中的推理时优化。直观上，它不是让模型永久“学会”新知识，而是让模型在困难样本上多尝试、多检查或借助外部能力。

</div>
<div class="concept-item" markdown="1">

**测试时反馈**

测试时反馈是部署阶段可用于判断、修正或强化模型行为的信号，可来自测试数据本身、模型生成结果的一致性、重建目标、验证过程、工具返回值或环境交互。TTI的关键不只是增加计算或更新参数，而是利用这些反馈决定如何更新状态、分配计算并改进输出。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文研究的不是一个具有固定输入输出格式的单项预测任务，而是统一刻画部署阶段的自我改进系统。系统输入包括测试实例、部署环境中可获得的反馈，以及可选的额外推理资源；其内部操作分为两条互补路径：一是根据反馈更新参数、提示、适配器、归一化统计量或其他模型状态，二是在不必改变状态的情况下增加采样、搜索、规划、验证或工具使用。输出是相较静态单次推理具有更高质量或更强任务能力的预测与行动。该问题设定不要求测试标签始终可用，也不把目标限定为抵抗分布偏移；核心假设是部署期间存在可利用的反馈和计算预算。两条路径还可形成混合系统，例如用扩展计算产生更可靠的伪标签以促进学习，或学习一个策略来决定何时以及如何增加推理计算。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Sun et al. [356] 的测试时学习工作**: 该工作提出利用无标签测试数据更新模型状态，是本文所归纳的状态更新路线的重要起点；本文进一步把由此发展的测试时适应方法纳入更广义的TTI框架。
- **既有TTA综述[214, 407, 423]与TTS综述[480, 59]**: 前者主要围绕分布偏移与适应组织研究，后者通常侧重大语言模型及推理阶段计算；本文试图跨越两类文献的术语和应用边界，用状态更新与额外计算的共同视角说明TTL、TTA、TTS及其混合形式之间的关系。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<p class="paper-minor-label">关键流程</p>

原文未明确报告完整流程。

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

原文未明确报告。

**训练与推理**

原文未明确报告。

**复现信息**

原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

原文未明确报告，或这里不需要额外前置概念。

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 该文没有统一复现实验或标准化定量汇总，因此无法从本文本身判断各类方法在相同数据、预算与模型规模下的相对优势；文中的方法比较主要是机制层面的综合，而不是统计受控的排行榜结论。
- 所给材料多为代表性工作与作者的定性归纳，且明确指出现有理论仅覆盖特定代理目标、反馈机制和部署假设。因此，关于有效性、稳定性和适用范围的总结仍需回查被引论文的完整实验设置与原始结果。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。

**实验想回答的问题**

- 该文是综述而非提出新算法的实证研究，因此没有统一实验用于回答性能优劣问题；其主要工作是以反馈驱动的测试时智能为框架，整理测试时适应、测试时学习与测试时扩展之间的关系。
- 文中对既有方法的讨论主要考察：不同测试时反馈、状态更新方式及额外推理计算分别适用于什么部署条件，并可能带来哪些成本、偏差与失效风险。

**实验实现**

原文未设置统一的数据集、训练与测试划分、基线、评价指标或复现实验协议。所给章节按反馈来源、更新机制和应用领域归纳既有研究，例如预测一致性、特征统计对齐、重建式自监督、外部模型监督、环境奖励、工具验证及人工反馈。由于不同被综述工作面向视觉、语言、生成模型、机器人和医疗等不同任务，其结果不能被视为同一受控实验中的横向比较。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文综述利用额外推理计算、反馈和测试时适应提升模型推理与行为的自我改进方法，覆盖面虽广但与推理期扩展直接相关。; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`9d702c9b53b92544aba60f9dfb157363e664f0466398d5c269829f5f8a8bcae4`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
