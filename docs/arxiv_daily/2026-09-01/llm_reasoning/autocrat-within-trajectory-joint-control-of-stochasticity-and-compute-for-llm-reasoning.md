---
title: "[论文解读] AutoCRAT: Within-trajectory Joint Control of Stochasticity and Compute for LLM Reasoning"
description: "[arXiv 2608.29988][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.29988"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:28:37.434894+00:00"
source_sha256: "f400342872f70827f61498fcfa4f1a7025d3ed14f620c97c6f182c338b27f892"
tags:
  - "LLM Reasoning"
  - "LLM 效率"
  - "LLM 其他"
  - "大语言模型推理"
  - "测试时计算"
  - "解码随机性"
  - "推理预算"
  - "轨迹内联合控制"
  - "自适应解码"
  - "冻结骨干模型"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.29988</p>

# AutoCRAT: Within-trajectory Joint Control of Stochasticity and Compute for LLM Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Hanjun Luo, Qiushi Liu, Jingya Zhang, Haihong Pang, Jiaheng Wen, Yifei Ma, Yu Yao, Chengxi Zhang, Hanrong Zhang, Yankai Chen, Hanan Salam</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: New York University；Affiliation: New York University Abu Dhabi；Affiliation: University of Washington Seattle；Affiliation: Harvard University；Affiliation: Massachusetts Institute of Technology；Affiliation: University of Illinois Chicago；Affiliation: Mohamed bin Zayed University of Artificial Intelligence</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.29988v1) · [PDF 下载](https://arxiv.org/pdf/2608.29988v1) · **关键词** 大语言模型推理, 测试时计算, 解码随机性, 推理预算, 轨迹内联合控制, 自适应解码, 冻结骨干模型<br>


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

本文研究大语言模型推理阶段的动态控制。模型能力固定时，生成效果仍显著依赖两类推理时配置：一是采样随机性，即通过温度、top-p 等参数调节候选词分布，在探索多种思路与集中选择高概率答案之间取舍；二是推理计算量，即决定模型需要生成多少推理步骤、使用多长输出预算以及何时停止。传统方案通常在请求开始前设定一套全程不变的配置，但单条推理轨迹内部存在阶段差异：早期可能需要较强探索，后期则更需要收敛、核验并提交答案。因此，本文把问题定义为“轨迹内联合控制”：在模型生成尚未结束时，根据解码过程中可观察到的信号，同时调整随机性和计算预算，而非只控制其中一个维度或只在请求级做一次决策。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**解码随机性**

大语言模型每一步都会给出下一个词元的概率分布，温度和 top-p 等解码参数决定采样结果有多分散。随机性较高有利于探索不同推理方向，但也可能带来不稳定或错误；随机性较低更利于收敛，却可能过早锁定错误思路。

</div>
<div class="concept-item" markdown="1">

**测试时计算与推理预算**

测试时计算指模型在回答阶段投入的额外生成工作，例如更长的思维链、更多候选路径或额外的修正步骤；推理预算则限制这些工作的规模。增加预算并不总能提高正确率，因为答案可能已经收敛，继续生成反而会产生冗余或“过度思考”。

</div>
<div class="concept-item" markdown="1">

**轨迹内控制**

一条推理轨迹是模型从接收问题到产出最终答案的完整生成过程；轨迹内控制允许控制器在该过程的不同阶段重新选择配置。本文强调在句末或推理步骤标记等语义边界更新决策，以避免逐词元切换造成的剧烈波动。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是用户提出的数学、代码生成或复杂问答任务，以及一个参数冻结的大语言模型；系统不能修改骨干模型，也不依赖其隐藏状态，只能使用解码期间能够观察到的信号和控制器自身状态。控制器在单条生成轨迹进行期间，于自然语义边界从离散动作空间中选择控制动作，联合改变采样随机性与后续推理预算；输出仍是骨干模型生成的推理过程和最终答案。该设置的目标不是单纯最大化正确率或一味缩短输出，而是在答案质量与推理词元开销之间取得更好的权衡，并使同一控制机制能够迁移到不同模型接口和骨干模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **AdaReasoner（Wang et al., 2025a）**: 该方法会针对问题联合选择推理指令格式、温度和推理步数，因而已经涉及随机性与计算量的共同配置；但其决策主要发生在生成开始之前，完整轨迹随后沿用所选配置。AutoCRAT 与它的关键区别是把联合决策移入单条轨迹内部，使配置能够随推理阶段变化。
- **EcoTune（Xu et al., 2025）**: 该方法在任务层面联合优化温度、最大输出长度等推理超参数，说明两个控制维度可以共同调节；但它仍以请求级或任务级配置为主，不能依据一条轨迹已经取得的局部进展、置信变化或答案收敛状态持续干预。本文所针对的研究空缺正是这种细粒度的轨迹内联合控制。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

LLM 的推理质量不仅取决于模型本身，还取决于生成时如何配置解码随机性（如温度、$top\text{-}p$）和推理计算量（如推理深度、生成预算）。现实任务及同一条推理轨迹的不同阶段需求并不一致：早期可能需要更广泛地探索，后期则更需要收敛、核验并确定答案；但固定的生成配置难以适应这种变化，导致不必要的推理 token 消耗或推理不足。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **静态或按请求配置的方法**：在生成开始前，为整个请求预先设定解码随机性和推理计算预算，之后通常保持不变。这类方法实施简单，但不能根据推理过程中的实时状态调整策略。
- **单维度自适应方法**：一类方法在生成过程中动态调整解码随机性，例如温度或采样策略；另一类方法动态调整推理计算，例如思考长度、预算分配、提前停止或自我纠错。它们通常只控制其中一个维度。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有静态配置主要是请求级决策，无法响应同一条推理轨迹中不同阶段的需求，可能在需要探索时过早收敛，或在已经足够确定时继续消耗计算资源。
- 现有自适应方法通常将解码随机性和推理计算分开处理，忽略二者的交互关系；例如提高探索程度可能改变后续所需的推理预算，而缩短预算也可能影响是否需要继续探索。结果是无法形成统一的、轨迹内的协调控制。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未建立一种统一的轨迹内控制框架，在仅使用解码过程中可观察信号的前提下，同时决定“如何探索”（解码随机性）和“推理多久”（计算预算），并在推理状态变化时稳定地更新这两类决策。

</div>
<div markdown="1"><span>核心问题</span>

能否为冻结的 LLM 构建一个解码器侧控制器，仅依据生成过程中可获得的信号，在语义边界处联合调整解码随机性与推理预算，从而在不依赖模型隐藏状态或逐 token 频繁切换的情况下，取得更好的准确率—计算量权衡？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把推理看成一个会不断变化的过程，而不是一次性请求：控制器在句子结束或步骤标记等语义边界观察当前轨迹状态，再从离散的控制动作中选择下一阶段的随机性和预算。离散动作减少了连续参数微调带来的抖动，边界更新避免逐 token 切换造成的不稳定，同时仍比整条请求只设定一次配置更灵活。因此，控制器有机会在早期保留探索，在后期根据趋于确定的状态减少计算，从而兼顾推理质量与效率。

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

- 所给实验章节未提供具体消融表或逐项消融结果，因此无法从原文摘录并判断温度控制、预算控制、语义边界更新或离散动作空间各自的独立贡献；相关设计的因果作用仍需依赖完整论文的消融实验核查。
- 评测规模和覆盖范围有限：实验使用4个骨干、6个基准，并将AdaReasoner与Self-Consistency限制在非代码子集；数据划分、提示协议和解码参数虽保持一致，但原文未明确报告更广泛任务、更多随机种子结果的完整数值，因此跨领域稳健性仍不能充分确定。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。

**实验想回答的问题**

- 原文未明确报告。

**实验实现**

原文未明确报告。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：在单条推理轨迹内联合调节解码随机性与推理预算，同时提升推理准确率并减少推理 token。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`f400342872f70827f61498fcfa4f1a7025d3ed14f620c97c6f182c338b27f892`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
