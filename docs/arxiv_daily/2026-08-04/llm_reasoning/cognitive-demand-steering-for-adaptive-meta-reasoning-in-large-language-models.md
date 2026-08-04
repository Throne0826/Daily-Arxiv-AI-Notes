---
title: "[论文解读] Cognitive Demand Steering for Adaptive Meta-Reasoning in Large Language Models"
description: "[arXiv 2608.01319][LLM Reasoning] 本文提出无需额外训练的认知需求引导框架 CDS，用多维“剩余认知需求”而非固定动作或对既有步骤的回顾性评分来控制大语言模型的推理、验证、算力分配与停止。"
arxiv_id: "2608.01319"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:57:19.585472+00:00"
source_sha256: "f3f776fd5044ca982f99ed65e4edbbccc1b86872f3f80841375bbddaab29defe"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "自适应推理"
  - "元推理"
  - "认知需求引导"
  - "残余需求评估"
  - "思维链"
  - "训练免费推理"
  - "自适应计算分配"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.01319</p>

# Cognitive Demand Steering for Adaptive Meta-Reasoning in Large Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> John Scoville, Shengzhuang Chen, Yejin Bang, Stefan Winzeck, Jonathan Richard Schwarz</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Thomson Reuters Foundational Research；Imperial College London</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01319v1) · [PDF 下载](https://arxiv.org/pdf/2608.01319v1) · **关键词** 大语言模型, 自适应推理, 元推理, 认知需求引导, 残余需求评估, 思维链, 训练免费推理, 自适应计算分配<br>


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

本文提出无需额外训练的认知需求引导框架 CDS，用多维“剩余认知需求”而非固定动作或对既有步骤的回顾性评分来控制大语言模型的推理、验证、算力分配与停止。

**不用术语来说**：大语言模型在难题上并不总是缺少推理长度，而是经常把力气用错地方：它可能写出看似合理的推导，却漏掉关键约束；在尚未核验边界情况时过早作答；或者问题已经解决后仍继续生成。实际需要的是一种过程控制机制，持续判断“距离正确答案还缺什么”，再让模型有针对性地补充推导、检查错误或及时停止。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 将自适应推理重新表述为需求跟踪：CDS先按认知科学启发的多个维度刻画任务需求，再在每轮推理后评估各项需求尚未满足的程度，以剩余需求作为控制器的核心状态。
- 构建无需训练且可组合的控制方式：系统依据剩余需求同时注入多类行为指导，动态生成验证目标，并据此决定后续动作、推理投入和停止时机，从而支持跨任务与跨模型的零样本使用。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型的自适应推理与元推理研究。普通思维链（Chain-of-Thought, CoT）让模型显式生成中间推理步骤，但复杂任务的关键不只是“生成更多步骤”，还在于判断当前解法遗漏了什么、下一步应采用何种认知操作，以及何时继续、验证、回退或停止。元推理因此在工作模型之外引入控制循环，根据任务、已有推理轨迹和进展评估来调整后续推理。本文关注的核心背景问题是：既有控制器往往直接从当前状态选择少量离散动作，或者依据已生成步骤的奖励进行事后评价，因而难以细致表示一个问题同时存在的逻辑、定量、信息筛选和验证需求，也不易根据尚未解决的困难合理分配推理计算量。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**思维链推理（Chain-of-Thought, CoT）**

模型在给出最终答案前生成一系列中间推理步骤，使多步演算或推导更容易完成。它提供了可继续检查和修正的推理轨迹，但本身不保证模型会关注正确约束，也不负责决定何时停止。

</div>
<div class="concept-item" markdown="1">

**元推理（meta-reasoning）**

元推理是在“执行推理”之上再进行控制：控制器观察任务和当前轨迹，决定下一步应继续推导、验证、回退、重启还是结束。本文中的工作模型负责产生具体推理内容，而元控制器负责规划和调整这一过程。

</div>
<div class="concept-item" markdown="1">

**认知需求与残余需求（cognitive demand and residual demand）**

认知需求表示解决任务所需的能力组合，例如信息识别、逻辑推导、定量计算、抽象和知识检索；本文使用受认知科学启发的16个维度刻画它。残余需求是经过若干推理步骤后仍未满足的那部分需求，用来描述“离可靠解答还缺什么”，而非只评价上一段推理写得好不好。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个待解决的推理任务以及可调用的大语言模型，系统首先在16个认知维度上评估任务的初始需求，并识别其中活跃的维度；初始时尚无进展，因此残余需求等于完整的初始需求。随后，训练免费的元控制循环反复读取任务、累计推理轨迹、当前进展、残余需求及辅助风险信号，据此规划投入力度，注入与活跃维度相匹配的通用示例或行为指导，并选择自由形式的下一步动作；工作模型执行该计划并追加一段推理。进展评估器在每轮判断各项需求已被满足到何种程度，并列出缺失信息、待验证结果或边界条件；当任务被判定完成时输出最终答案，否则继续迭代，直至达到最大轮数。该设定不训练额外控制器，也不要求针对新模型或新任务进行适配；其目标是在数学、科学问答和代码生成等任务上，以剩余认知困难而非固定动作类别作为控制状态，使推理策略和计算量随未解决需求变化。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$d$**

认知需求维度；本文共使用16个受认知科学启发的维度。

</div>
<div class="notation-item" markdown="1">

**$D^{(0)}$**

任务开始时评估得到的初始认知需求剖面；该符号是对原文文字描述的概括，所给章节未规定正式记号。

</div>
<div class="notation-item" markdown="1">

**$R^{(t)}$**

第$t$轮评估后的残余认知需求，即各活跃维度中尚未被当前推理覆盖的需求；该符号是便于说明而作的概括，所给章节未规定正式记号。

</div>
<div class="notation-item" markdown="1">

**$t$**

元推理控制循环的轮次索引。

</div>

</div>

**直接相关的工作**

- **Chain-of-Thought（CoT）**: CoT通过提示模型生成中间步骤，为本文的迭代推理轨迹提供基础，但它通常没有显式控制器来诊断尚未满足的认知需求。CDS在CoT式生成外增加进展评估和控制循环，使后续推理能够根据残余需求被定向调整。
- **Tree-of-Thought（ToT）**: ToT通过生成、评价和搜索多个候选思路扩展推理，但其典型控制更侧重分支、选择和剪枝等搜索动作。本文将这类直接选择离散干预的方案概括为“动作中心控制”，并以多维、可组合的残余需求剖面替代固定动作或模式作为核心控制状态。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

复杂数学、科学问答和代码生成任务通常同时要求识别相关信息、抽象建模、逻辑演绎、定量核验、知识检索与边界条件检查。模型若不能在推理过程中识别哪些要求仍未完成，就容易让早期错误向后传播、遗漏决定性约束，或在低价值路径上浪费推理计算。因此，实际需求不是统一增加思维链长度，而是让推理投入随当前未解决问题动态变化。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **结构化推理与搜索方法**：思维链、自一致性、由简到繁和思维树等方法通过显式生成中间步骤、采样多条答案路径、分解问题或搜索分支来提高推理质量；部分推理模型还通过强化学习形成内部思维链。它们主要改变推理轨迹的生成或搜索方式。
- **动作中心式元推理控制**：控制器读取任务上下文和当前推理状态，然后从预设的离散干预中选择下一步，例如切换推理策略或认知模式、剪枝、回溯、重启或终止。有些系统依赖回顾性奖励判断上一阶段表现，有些则需要多样本监督来训练额外控制器。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 固定且较小的动作集合只能粗粒度地选择一种策略或模式，难以显式表示并同时组合抽象、演绎、计算和验证等相互作用的需求；结果是控制器可能选择一个大致合适的模式，却仍无法针对任务中真正缺失的认知操作。
- 回顾性评分、表面轨迹模式或启发式搜索策略侧重判断已经生成的内容，而没有结构化估计尚未解决的困难；这会削弱继续、验证、分支和停止决策的依据，并可能造成错误累积或无效计算。额外训练控制器还带来监督数据与迁移成本。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种统一、细粒度且无需训练的控制状态：它既要面向未来地描述当前解答距离完成任务还缺哪些认知工作，又要支持多种需求的组合，并把该描述直接转化为验证目标、推理策略和计算预算。换言之，尚不清楚“剩余认知需求”能否替代离散动作或单一奖励，成为可跨模型、跨任务迁移的元推理信号。

</div>
<div markdown="1"><span>核心问题</span>

能否在不训练额外控制器的条件下，先建立任务的多维认知需求画像，再逐轮估计部分解答尚未覆盖的需求，并利用这一需求缺口自适应地选择组合式干预、安排验证与推理投入，以及决定何时停止？

</div>
<div markdown="1"><span>作者直觉</span>

把解题过程类比为逐项清理一张动态待办清单：初始画像说明题目可能需要哪些能力，每轮评估则标记哪些工作已经完成、哪些信息仍缺失、哪些结论风险较高。控制器不必从少数笼统模式中猜选一个，而可以针对仍未完成的项目同时提供相应指导；待办项多且风险高时继续投入，关键结论存疑时安排定向检查，需求基本清零时停止。这样，计算量和推理行为都由“还差什么”驱动，而不是由“刚才看起来做得怎样”驱动。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

认知需求引导（Cognitive Demand Steering, CDS）是在未修改的工作模型外部运行的、无需训练的元推理控制循环。给定任务 $q$，系统先沿 16 个认知与知识维度评估初始难度，并保留得分最高的 4 个维度作为活动工作集 $\mathcal{A}$；随后每轮依次判断当前推理是否完成、估计尚未满足的认知需求、安排计算强度、生成下一步自然语言干预，再让工作模型执行该干预。新生成的推理片段被追加到轨迹 $\mathcal{T}_t$，循环直至进度评估器判定任务已解决或达到最大轮数，最终输出可抽取的答案。
该设计的关键不是给已经生成的步骤打一个事后奖励，而是询问“要解决问题还缺什么”。残余需求画像 $D_t$ 为控制器提供前瞻信号，例如当前瓶颈究竟是定量推导、关键信息识别还是验证；努力调度器再依据瓶颈、平均剩余需求、不确定性和推理失稳风险决定下一轮应投入多少推理与验证。通俗地说，CDS 像一名持续检查解题进度的指导教师：先判断学生还欠缺哪种思考，再明确布置下一步，而不是只笼统评价上一行答案好不好。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始认知需求画像与活动维度选择

需求画像器调用通用 LLM，为每个维度给出 $0$ 至 $5$ 的整数需求分数，形成初始画像 $D_0$；实验中取最高分的 $k=4$ 个维度构成活动工作集 $\mathcal{A}$，并用这些分数初始化残余需求。

<div class="method-step__io" markdown="1">

**输入**：任务实例 $q$、包含 16 个认知与知识维度的需求分类 $\mathcal{D}$。<br>
**输出**：初始需求画像 $D_0$、活动工作集 $\mathcal{A}$、初始努力等级以及初始残余需求向量。

</div>

**直观理解**：系统先判断这道题主要难在什么地方，而不要求后续控制器同时关注全部 16 个方面。只保留最相关的 4 项可以让诊断与提示集中在真正可能限制解题的能力上。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 进度评估与停止判断

进度评估器 $\mathcal{E}$ 生成状态 $P_t$，概括当前进展并估计矛盾风险 $c_t$、循环风险 $l_t$、不确定性 $u_t$、验证目标 $v_t$、缺失信息 $m_t$ 及任务是否已解决；若已解决，则在调用下一次工作模型前提前终止并整理最终答案。

<div class="method-step__io" markdown="1">

**输入**：任务 $q$、当前累计推理轨迹 $\mathcal{T}_t$、初始画像和活动工作集 $\mathcal{A}$。<br>
**输出**：结构化进度状态 $P_t$，或在任务已完成时输出最终答案。

</div>

**直观理解**：这一阶段既检查“做完没有”，也记录哪里可能自相矛盾、原地打转，以及下一步需要验证什么。它避免系统在答案已经充分时继续消耗计算，也避免只凭流畅文本误判进度。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 残余需求诊断、指导检索与努力调度

残余需求评估器 $\mathcal{R}$ 将每个活动维度尚需投入的程度更新为 $D_t$，分数限制在 $[0,5]$；系统选取残余需求最高的 3 个维度，从静态字典 $\mathcal{G}$ 检索相应通用示例，并综合需求、不确定性及风险计算离散努力等级 $\ell_t\in\{1,\ldots,5\}$。

<div class="method-step__io" markdown="1">

**输入**：任务 $q$、初始画像 $D_0$、进度状态 $P_t$、上一轮残余需求及活动工作集 $\mathcal{A}$。<br>
**输出**：残余需求画像 $D_t$、最高需求维度子集 $\mathcal{A}^{\star}$、通用指导示例集合和当前努力预算。

</div>

**直观理解**：初始难点不等于当前难点：某项需求可能已经解决，另一项则可能成为新瓶颈。该步骤会把注意力转向尚未解决且最紧迫的三项，并决定下一步是简短推进，还是需要分解、复核或尝试替代路径。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自由形式控制与工作模型执行

控制器 $\mathcal{C}$ 通过一次 LLM 查询生成自由形式自然语言动作 $A_t$，其中可指定下一推导、需补足的信息、检查项目和推理风格；工作模型 $\mathcal{M}$ 根据 $A_t$ 与努力预算生成一个新的推理片段 $s_t$，而非一次性重做完整答案。

<div class="method-step__io" markdown="1">

**输入**：任务 $q$、进度状态 $P_t$、残余需求 $D_t$、活动维度 $\mathcal{A}^{\star}$、检索示例、努力等级以及既有推理轨迹。<br>
**输出**：需求引导的下一段推理 $s_t$，并将其追加为更新后的轨迹 $\mathcal{T}_{t+1}=\mathcal{T}_t\Vert s_t$。

</div>

**直观理解**：控制器不从少量固定动作中选标签，而是可以针对当前题目写出具体指令，例如要求代入某个关系、检查单位或验证边界情况。工作模型只执行这一阶段性指令，随后系统重新诊断，从而形成可纠偏的闭环。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 逐轮残余需求画像

$$
D_t=\mathcal{R}(q,P_t,D_0),\qquad D_t=\left\{d_t^{(i)}\right\}_{i\in\mathcal{A}}
$$

**符号说明**

- $D_t$：第 t 轮各活动维度的残余需求画像。
- $\mathcal{R}$：由通用 LLM 提示实现的残余需求评估器。
- $q$：待解决的任务实例。
- $P_t$：第 t 轮进度状态，包含完成标记、风险、不确定性、验证目标和缺失信息。
- $D_0$：任务开始前得到的初始认知需求画像。
- $d_t^{(i)}$：第 t 轮在第 i 个活动维度上尚未满足的需求分数，取值限制为 0 至 5。
- $\mathcal{A}$：从 16 个维度中选出的活动工作集，实验中初始大小为 4。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把固定的初始难度参照与当前进度结合起来，重新估计每种能力还需要投入多少。分数随需求被满足而趋近于零，因此控制器依据的是当前剩余问题，而不是题目一开始的静态难度。<br>
**原文位置**：第 3.5 节，公式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 自适应努力分数

$$
E_t=\alpha_0\max_{i\in\mathcal{A}}d_t^{(i)}+\alpha_1\overline{D}_t+\alpha_2\cdot5u_t+\alpha_3\cdot5r_t,\qquad \overline{D}_t=\frac{1}{|\mathcal{A}|}\sum_{i\in\mathcal{A}}d_t^{(i)}
$$

**符号说明**

- $E_t$：第 t 轮的连续努力分数，范围为 0 至 5，随后映射为 1 至 5 级离散预算。
- $d_t^{(i)}$：活动维度 i 在第 t 轮的残余需求分数。
- $\overline{D}_t$：所有活动维度残余需求的算术平均值。
- $u_t$：进度评估器给出的不确定性，范围为 0 至 1。
- $r_t$：由矛盾风险与循环风险导出的推理失稳分数，范围为 0 至 1；算法伪代码以二者最大值构造该项。
- $\alpha_0,\alpha_1,\alpha_2,\alpha_3$：四项权重；评测采用 0.45、0.25、0.15、0.15。
- $\mathcal{A}$：当前参与跟踪的认知需求维度集合。

<div class="equation-explanation" markdown="1">

**直观理解**：公式同时考虑最严重的单项瓶颈、整体剩余工作量、主观不确定性和推理是否失稳，并将后两项乘以 5 统一量纲。最大需求项权重最高，所以即使多数方面已解决，只要仍有一个关键难点，系统也不会过早降低推理强度。<br>
**原文位置**：第 3.6 节，公式 (2)；具体风险构造另见算法 2 的 ScheduleEffort

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。CDS 没有可学习参数、奖励函数或任务专用优化目标，也不对需求画像器、评估器、控制器或工作模型进行梯度更新；各模块均通过提示调用通用 LLM。论文所称“training-free”指控制逻辑在推理时组合初始画像、残余需求、静态通用示例和自然语言动作，因此无需多样本监督或针对任务、模型进行适配；公式 (1) 与公式 (2) 是状态更新和计算预算规则，不是训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 进度评估器与残余需求评估器**

进度评估器把轨迹转换为结构化状态 $P_t$，其中完成标记控制提前停止，$c_t$、$l_t$ 和 $u_t$ 描述推理稳定性，$v_t$ 与 $m_t$ 为控制器提供验证目标和缺失信息。残余需求评估器再以 $q$、$P_t$ 和 $D_0$ 为条件，在固定活动轴上生成 $D_t$；它预测完成任务仍需满足的需求，而不是对上一段文本计算奖励。

> 直观理解：进度评估回答“目前发生了什么”，残余需求评估回答“接下来还需要什么”。二者分开后，系统既能发现当前错误，也能把下一轮行动对准尚未解决的瓶颈。

**2. 努力调度器**

调度器将最大残余需求、活动维度上的平均残余需求、不确定性，以及由矛盾和循环风险形成的失稳分数组合为 $E_t$，再四舍五入并截断为 $1$ 至 $5$ 级努力等级。高等级提示控制器和工作模型增加问题分解、验证及替代路径；论文评测中同一测试只使用一个模型，通过改变推理预算实现自适应计算，而未实际按等级路由到更强模型。

> 直观理解：最大需求项保证单个严重瓶颈不会被其他低分项平均掉，平均需求则反映整体剩余工作量。风险和不确定性高时提高预算，使系统更谨慎；问题接近解决时降低预算，减少无效推理。

**3. 自由形式控制器与工作模型**

控制器以任务、$P_t$、$D_t$、努力等级和按维度检索的通用示例为上下文，零样本生成动作 $A_t$；其动作空间是开放的自然语言，而非预定义策略集合。工作模型接收任务、完整轨迹、$A_t$ 和努力等级，仅生成下一推理片段，并由外部循环负责后续评估、纠偏与终止。

> 直观理解：细粒度诊断只有转化成可执行指令才有价值；开放式动作能明确到当前题目的具体运算或检查，而不只是“继续”“回溯”等粗粒度命令。工作模型本身无需改参数，因此同一套控制方式原则上可以套在不同基础模型和任务上。

**训练与推理**

训练阶段不存在。推理时，系统首先对输入任务做一次 16 维画像并选择 4 个活动维度，初始化空推理轨迹与残余需求；在每轮中，进度评估器读取任务和累计轨迹，若判定已解决便提前整理答案，否则努力调度器确定预算，系统选择残余需求最高的 3 个维度并检索静态通用指导，控制器生成下一步动作，工作模型再生成一个受引导的推理片段。该片段被追加到轨迹，残余需求被重新评估，随后进入下一轮；若一直未被判定为解决，则达到最大轮数后返回累计轨迹或其中可抽取的最终答案。
所有评估与控制都采用自然语言 LLM 查询，因而可以在不修改工作模型的条件下迁移到不同任务和骨干模型。需要注意，架构允许按照努力等级选择不同的工作后端 $M_\tau$，但论文实验固定每个测试所用模型，仅自适应改变步骤、分支与验证预算；因此实验验证的主要是自适应推理过程，而不是强弱模型路由带来的收益。

**复现信息**

复现方法时需要保留以下影响方法含义的设置：认知分类包含 $K=16$ 个维度，每维按 $0$ 至 $5$ 评分；实验经超参数搜索固定初始活动维度数为 $k=4$，控制前选取残余需求最高的 3 项检索指导，且维度指导来自预先编写的静态字典 $\mathcal{G}$。首轮轨迹为空，进度状态以 $u_1=0.5$、其余风险为 0 初始化；残余分数截断至 $[0,5]$，努力权重为 $(0.45,0.25,0.15,0.15)$，连续分数经四舍五入并截断到 $1$ 至 $5$ 级。
论文评测最多运行 12 轮且不允许使用外部工具。工作模型被要求显式输出可供外部评估器读取的推理过程，每轮只生成下一片段；终止条件是进度评估器判定已解决或达到轮数上限。文中一处说明“每步省略活动集中最低需求维度”，而算法同时保留初始 4 维并在控制阶段取最高 3 维；复现时应结合作者代码或提示模板核对该维度更新细节。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- LiveCodeBench（LCB）：代码生成基准，按 Easy、Medium、Hard 三种难度报告结果，用于检验方法在不同代码任务难度下进行算法设计与代码合成的能力。原文节选未明确报告数据规模、版本、数据划分或具体评测样本数。
- 数学推理基准：用于检验数学演绎与定量推理能力。原文称总评测覆盖六个推理基准，但节选未给出数学数据集名称、规模与划分。
- 科学知识整合类基准：用于检验模型结合领域知识完成多步推理的能力。原文节选未给出数据集名称、规模与划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率或百分比任务得分**

衡量模型在各推理基准上给出正确答案或通过任务判定的比例。表 2 和表 3 均以百分数报告，但节选未说明不同数据集是否使用完全相同的判分规则。 （越高越好，因为更高得分表示更多测试问题被正确解决。）

</div>
<div class="metric-item" markdown="1">

**跨模型、跨基准平均提升**

将三个前沿大语言模型和六个推理基准上的表现汇总，用于判断 CDS 的总体收益是否具有跨模型与跨任务一致性。 （越高越好，但平均值可能掩盖具体模型或数据集上的下降，因此必须结合逐项结果检查。）

</div>
<div class="metric-item" markdown="1">

**Token 效率**

比较不同推理方法取得结果时消耗的生成 token 或推理预算，用于判断准确率提升是否仅来自更多计算。原文说明会考察该指标，但所给节选未报告定义、数值或统计方式。 （在准确率相当时 token 消耗越低越好；在预算相当时准确率越高越好。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三个前沿大语言模型、六个推理基准的总体平均结果：CDS 对比直接调用

<div class="result-value" markdown="1">

作者报告 CDS 的平均准确率相对直接调用提高 $21.9\%$。

</div>

这一汇总结果表明，加入迭代元控制和认知需求驱动干预后，模型总体上比不进行测试时推理控制更准确。这里的 $21.9\%$ 应按原文表述理解为“improves accuracy by”的提升值；节选没有说明它是绝对百分点还是相对增幅，也没有给出逐数据集分布和统计显著性，因此不能据此断言每个模型、每个任务都获得同等幅度的提升。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Averaged across three frontier LLMs and six reasoning benchmarks, CDS improves accuracy by $21.9\%$ over direct calls and $9\%$ over standard CoT reasoning, with the largest gains on difficult mathematics and coding tasks.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 三个前沿大语言模型、六个推理基准的总体平均结果：CDS 对比标准 CoT

<div class="result-value" markdown="1">

作者报告 CDS 的平均准确率相对标准 CoT 推理提高 $9\%$。

</div>

该比较比直接调用基线更关键，因为它控制了“生成逐步推理”这一常见增强因素，说明作者观察到的收益不只是来自要求模型思考更多步骤，而与 CDS 的迭代评估和干预有关。不过，完整 CDS 同时包含多个机制，单凭这一结果无法把 $9\%$ 的收益全部归因于剩余需求跟踪；这一因果问题需要结合需求消融实验判断。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Averaged across three frontier LLMs and six reasoning benchmarks, CDS improves accuracy by $21.9\%$ over direct calls and $9\%$ over standard CoT reasoning, with the largest gains on difficult mathematics and coding tasks.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 按任务难度比较 CDS 的收益

<div class="result-value" markdown="1">

作者称最大收益出现在困难数学任务和困难代码任务上；所给节选未报告相应的逐项分数或提升幅度。

</div>

这一现象与 CDS 的设计目标一致：当问题仍有较高剩余认知需求时，控制器应继续投入推理并选择更针对性的干预，因此复杂任务可能比简单任务更受益。但节选只提供作者的汇总结论，没有给出难度分组的完整数据，也未排除困难任务因基线较弱而具有更大提升空间的解释。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Averaged across three frontier LLMs and six reasoning benchmarks, CDS improves accuracy by $21.9\%$ over direct calls and $9\%$ over standard CoT reasoning, with the largest gains on difficult mathematics and coding tasks.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Direct inference（直接推理）：直接调用骨干模型回答问题，不增加显式思维链或元推理控制。该基线用于衡量 CDS 相对原始模型能力带来的净提升。
- Standard CoT reasoning（标准思维链推理）：让模型生成逐步推理过程，但不使用 CDS 的剩余需求评估与干预机制。该比较用于判断收益是否超出一般的逐步推理提示。
- Meta-Reasoner-S（Meta Reasoner Static）：采用静态元推理策略的比较方法。它用于检验固定控制策略与 CDS 动态需求驱动控制之间的差异；节选未明确报告其具体配置。
- Meta-Reasoner-D（Meta Reasoner Dynamic）：采用动态元推理策略的比较方法。它是更接近 CDS 的强基线，可用于判断仅有动态控制是否足够，还是还需要显式的剩余需求表征；节选未明确报告其具体实现与训练条件。

**实验想回答的问题**

- CDS 是否能在数学推演、算法执行、科学知识整合和代码生成等推理任务上，稳定优于直接推理与标准测试时推理方法？
- 显式跟踪剩余认知需求是否具有独立价值，以及随着推理轮数增加，CDS 是否能把额外计算更有效地分配给困难任务？

**实验实现**

实验覆盖三个前沿大语言模型和六个推理基准，任务需求包括数学演绎、算法执行、科学知识整合与代码生成。表 2 按“模型 × 基准 × 推理方法”报告百分比得分，并标出每个模型、每个基准上的最佳与次佳结果。实验还考察推理轮数增加时推理轨迹预测能力的变化，以及不同方法的 token 效率。消融实验保留自适应进展评估、努力程度调度和控制器—工作模型迭代，只移除认知需求相关信息，并将努力等级固定为最高的 $5$。原文节选未明确报告样本量、提示模板、最大轮数、解码参数、随机种子、重复实验次数、显著性检验或 token 效率的具体计算方法。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 完整 CDS 对比需求消融版本：移除初始需求画像、剩余需求画像、上下文中的需求信息以及需求条件化示例，并将努力等级固定为最高的 $5$ | 作者报告完整 CDS 在六个数据集的平均结果上优于需求消融版本；表 3 的具体百分比未包含在所给节选中。 | 该消融试图隔离“显式需求跟踪”的贡献。消融版本仍保留自适应进展评估、努力调度及控制器—工作模型迭代，因此比较并不是完整 CDS 与普通单次推理之间的差异。尤其重要的是，消融版本每一步都采用最高努力等级，而完整 CDS 根据任务需求动态调整；完整方法仍然更好，支持“诊断需要何种推理”比单纯最大化推理努力更重要。不过，该消融同时删除了需求画像、需求注入和需求条件化示例，无法进一步区分这些子组件各自的贡献。 | Section 5.1, Table 3<br><span class="experiment-evidence">This is in spite of the fact that the ablated variant applies maximum reasoning effort at each step while CDS dynamically adjusts effort based on task demands.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出无需训练的元推理控制框架，根据剩余认知需求动态选择干预以改进数学和代码推理。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`f3f776fd5044ca982f99ed65e4edbbccc1b86872f3f80841375bbddaab29defe`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
