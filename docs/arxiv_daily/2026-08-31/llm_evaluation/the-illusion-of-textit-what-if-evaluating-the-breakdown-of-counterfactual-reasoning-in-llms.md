---
title: "[论文解读] The Illusion of $\\textit{What If}$: Evaluating the Breakdown of Counterfactual Reasoning in LLMs"
description: "[arXiv 2608.27953][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.27953"
announcement_date: "2026-08-31"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:35:34.013456+00:00"
source_sha256: "5f266b365cc6d8963dfd0197de5f5437ac0faf9b8a1fb719646595f2035b9eff"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "反事实推理"
  - "大语言模型"
  - "因果推理"
  - "开放域评测"
  - "长时程推理"
  - "因果图"
  - "WhatIfBench"
  - "PRISM"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.27953</p>

# The Illusion of $\textit{What If}$: Evaluating the Breakdown of Counterfactual Reasoning in LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Yucheng Wang, Yuetian Du, Zhengyi Liu, Rongyu Zhang, Bing Zhao, Boyu Yang, Ming Kong, Lin Qu, Hu Wei, Jie Liu, Qiang Zhu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Zhejiang University Alibaba Group City University of Hong Kong[1mm]</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27953v1) · [PDF 下载](https://arxiv.org/pdf/2608.27953v1) · **关键词** 反事实推理, 大语言模型, 因果推理, 开放域评测, 长时程推理, 因果图, WhatIfBench, PRISM<br>
**代码**: [https://github.com/zju-gt/WhatIfBench](https://github.com/zju-gt/WhatIfBench) · **项目页**: [https://github.com/zju-gt/WhatIfBench](https://github.com/zju-gt/WhatIfBench)

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

反事实推理研究模型在改变现实前提后，能否推断“如果情况不同会怎样”，并解释变化如何沿着事件、状态与机制逐步传播。与只要求预测一个固定答案的任务不同，开放领域、开放形式、长时程反事实问题通常允许多个合理结果，因此评价重点应从最终结论扩展到前提是否保持、因果方向是否正确、关键机制是否完整以及整条因果过程是否连贯。本文将这一问题用于检验大语言模型是否真正形成了连贯的因果解释，而不只是生成符合常识、但缺少因果支撑的流畅叙述。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**反事实推理**

反事实推理是在一个假设前提下推演未实际发生的情形，例如先接受“智能手机从未广泛普及”，再分析其对移动互联网和社会协作的影响。模型不能简单恢复现实世界事实，而要坚持该假设并追踪由它引起的后续变化。

</div>
<div class="concept-item" markdown="1">

**因果过程与因果图**

因果过程强调一个结果是如何由中间事件、状态和机制逐步产生的，而不是只判断结果对不对。因果图用节点表示事件或状态、用有向边表示因果影响；本文将模型的自然语言回答转换为响应派生语义因果图，并检查边的有效性、方向和整体连续性。

</div>
<div class="concept-item" markdown="1">

**开放域、开放形式、长时程设定**

开放域表示问题可能涉及科学技术、人文社会或跨领域系统，题目不预先列出全部变量和关系；开放形式表示模型可以自由组织答案，而不是从固定选项中作答。长时程表示干预的影响要经过多个中间环节传播，因此单一最终答案或短答案匹配不足以评价推理质量。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是一道开放形式的 what-if 问题及其反事实前提，例如询问某项技术从未被广泛采用会产生什么后果；模型输出是一段自由形式的因果解释，而非固定格式的答案或预定义变量赋值。WhatIfBench 包含 220 道 STEM、HSS 和 Hybrid 问题：前者侧重自然与技术约束，HSS 侧重历史、制度与社会动力，Hybrid 涉及跨领域传播。由于同一问题可以有多个合理轨迹，评价不假设唯一金标准结果，而是要求回答忠实于反事实前提、覆盖重要机制、遵守领域约束、适当处理不确定性，并呈现方向正确且连续的因果链。PRISM 将回答转化为响应派生语义因果图，再结合过程层面的因果有效性和答案层面的解释充分性进行评估。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D_{\mathrm{task}}$**

本文的反事实评测数据集；具体对应 WhatIfBench 中的问题集合。

</div>
<div class="notation-item" markdown="1">

**$x$**

输入的开放形式反事实问题或其反事实前提。

</div>
<div class="notation-item" markdown="1">

**$y$**

大语言模型针对问题 $x$ 生成的自由形式自然语言回答。

</div>
<div class="notation-item" markdown="1">

**$G=(V,E)$**

由回答 $y$ 派生的语义因果图；$V$ 是事件、状态和机制等节点集合，$E$ 是节点之间的有向因果关系集合。

</div>

</div>

**直接相关的工作**

- **CRASS**: CRASS 将反事实条件句转换为问答实例，适合检验模型是否能在较短、较受约束的任务中处理反事实前提；本文认为这类设置通常依赖答案级比较，未充分覆盖开放域长时程回答中的机制传播和因果过程。
- **IfQA**: IfQA 将反事实预设引入开放域问答，并使用 Exact Match 与 token-level F1 等参考答案指标；本文继承其对开放域反事实问题的关注，但进一步针对没有唯一答案的自由形式解释，采用因果图过程评价与问题特定评分规约相结合的方式。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现实中的“如果……会怎样”问题通常涉及历史、社会、科学或技术系统的长期连锁变化。模型不仅要给出一个听起来合理的结论，还要说明改变的前提如何通过多个中间事件、状态和机制影响后续结果。若只依据语言流畅度或最终答案是否匹配来评价，就可能把缺少因果依据的叙述误判为可靠推理。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **有界的反事实问答基准**：这类方法将反事实条件转化为问答任务，要求模型识别假设前提并回答一个局部问题。例如，CRASS处理反事实条件句，IfQA处理带有反事实预设的开放域问答。它们主要检验模型能否在较短范围内应用给定假设。
- **基于形式变量或因果结构的干预式评测**：这类方法预先规定变量、因果结构和目标结果，再要求模型模拟某个变量被干预后的影响。由于问题结构和可能答案通常受到明确约束，因此可以使用固定答案或相对清晰的结果标准进行评价。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有基准大多依赖固定变量、明确因果结构或单一目标结果，难以覆盖真实开放域问题中隐含的关键机制、跨领域影响和长时间跨度。其直接后果是：模型可能只需完成局部条件匹配，而不必展示从反事实前提到最终后果的完整因果过程。
- 当一个问题存在多个合理结果时，最终结论匹配无法区分可靠解释与流畅但脆弱的叙述。模型可能遗漏必要机制、改变原始前提、倒置因果方向，或在推理中重新使用现实世界假设，却仍然得到表面上可信的答案。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种面向开放域、开放形式、长时程反事实问题的评测方法：它既允许不同答案基于同一前提提出多种合理结果，又能检查回答内部的事件链、状态变化和因果机制是否连续，并同时判断回答是否忠实于前提、覆盖关键机制、遵守领域约束以及适当地表达不确定性。

</div>
<div markdown="1"><span>核心问题</span>

在不存在唯一标准结果的开放域反事实问题中，如何把模型的自由文本解释转化为可检查的因果过程，并据此区分真正连贯、前提一致的反事实推理与仅仅语言流畅的叙述？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把评价对象从“最后说了什么”转向“回答是怎样推到这个结果的”。具体而言，可从模型回答中抽取事件、状态和机制，组成回答衍生的语义因果图，再分别检查图中因果边和整体拓扑是否连贯，以及回答是否满足问题特定的解释标准。这样，即使不同回答提出不同但合理的结果，也可以依据其因果过程和解释质量进行比较；用通俗的话说，就是不只看模型的结论像不像正确答案，还要沿着它的推理链逐步检查每一跳是否站得住。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法由基准任务与评估器两部分组成。首先，给定包含问题语境和明确反事实干预的实例 $x_i=(q_i,I_i)$，被测大语言模型生成开放式自然语言解释 $y_i$；随后，PRISM 将解释转换为响应派生语义因果图，并结合过程指标与量规指标评价其因果过程有效性和解释充分性。直观地说，WhatIfBench 不要求模型复述唯一标准答案，而是检查模型能否从“如果条件改变”出发，沿着合理的中间机制持续推导后果，同时不偏离原始前提。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造反事实任务实例

筛选具有明确反事实前提、充分语境和非平凡因果传播要求的问题，将其改写为规范化查询 $q_i$，并标注干预 $I_i$、领域类别 $d_i$ 与问题级量规 $\mathcal{R}_i$。

<div class="method-step__io" markdown="1">

**输入**：候选 what-if 问题及其背景材料。<br>
**输出**：WhatIfBench 实例 $x_i=(q_i,I_i)$ 及其领域标签和评估要求。

</div>

**直观理解**：这一步先把模糊的“假如发生某事会怎样”整理成可评估的问题，但不强行规定只有一个正确结论，而是明确应当考虑哪些机制和后果。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 生成开放式反事实解释

模型根据问题语境和反事实干预生成自由格式解释 $y_i$，要求解释忠实于 $I_i$，补充相关中间机制，并将影响传播到下游结果。

<div class="method-step__io" markdown="1">

**输入**：实例 $x_i=(q_i,I_i)$ 与待测模型 $M$。<br>
**输出**：模型对该反事实问题的自然语言回答 $y_i$。

</div>

**直观理解**：模型不能只给出一句“结果会改变”，而应说明改变从哪里开始、经过哪些环节、最终可能造成什么影响。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 将回答解析为语义因果图

解析器先抽取基本话语单元（EDU）及其带标签的语义关系，构造支持—核心结构，再将关系投影为 EDU 级有向边，去除重复边，得到 $\mathcal{G}_{y_i}=(\mathcal{V}_{y_i},\mathcal{E}_{y_i})$。若解析失败或没有有效 EDU，则把回答按句子切分，并用相邻句之间的 $\mathrm{SEQUENCE}$ 边构造保守的启发式图。

<div class="method-step__io" markdown="1">

**输入**：回答 $y_i$、解析器 $p_{\theta}$、关系标签集合 $\mathcal{L}$ 和预算 $B$。<br>
**输出**：与回答文本对应的响应派生语义因果图 $\mathcal{G}_{y_i}$。

</div>

**直观理解**：评估器把一段长文字转换成“事件或状态节点”和“它们之间如何关联的箭头”，这样就能检查推理链是否断裂，而不只看语言是否流畅。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 联合计算 PRISM 分数

过程指标（Process Metric，PM）在图层面评价因果关系、传播过程和整体结构的有效性；量规指标（Rubric Metric，RM）依据问题级量规评价回答是否覆盖必要内容、解释是否充分。两者共同形成最终 PRISM 分数，用于总体和 STEM、HSS、Hybrid 类别诊断。

<div class="method-step__io" markdown="1">

**输入**：反事实实例 $x_i$、回答图 $\mathcal{G}_{y_i}$、量规 $\mathcal{R}_i$ 以及模型回答文本 $y_i$。<br>
**输出**：PM、RM 及其组合后的 PRISM 最终分数和错误分析结果。

</div>

**直观理解**：PM 类似检查推理路线是否走得通，RM 类似检查答案是否把题目要求讲完整；两者结合可区分“过程错了”和“过程尚可但解释不够”的情况。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 反事实解释生成任务

$$
x_i=(q_i,I_i),\qquad x_i\xrightarrow{M}y_i
$$

**符号说明**

- $x_i$：第 $i$ 个 what-if 实例，由问题语境和反事实干预组成。
- $q_i$：第 $i$ 个实例的规范化问题或上下文。
- $I_i$：明确指定的反事实前提或干预。
- $M$：被评估的大语言模型。
- $y_i$：模型针对该实例生成的自由格式自然语言解释。

<div class="equation-explanation" markdown="1">

**直观理解**：该表达式定义了基准的输入和输出：模型接收原问题及被改变的条件，然后生成解释。关键要求不是只预测结果，而是让 $y_i$ 忠实于 $I_i$，并说明中间机制如何把改变传递到下游后果。<br>
**原文位置**：第 3.1 节，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 响应派生语义因果图

$$
\mathcal{G}_{y}=(\mathcal{V}_{y},\mathcal{E}_{y})
$$

**符号说明**

- $\mathcal{G}_{y}$：由回答 $y$ 解析得到的语义因果图。
- $\mathcal{V}_{y}$：图中的节点集合，每个节点对应一个抽取出的 EDU 及其文本。
- $\mathcal{E}_{y}$：图中的有向边集合，每条边表示经归一化的语义关系。
- $y$：待解析的模型自然语言回答。

<div class="equation-explanation" markdown="1">

**直观理解**：这个图把回答中的基本陈述作为节点，把陈述之间的因果或语义联系作为箭头。PM 可以据此检查回答是否形成连贯的因果拓扑，而不是由互不相连的流畅句子拼成表面故事。<br>
**原文位置**：附录 E“Response-to-Graph Parsing Algorithm”，算法 1 第 2 行

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文方法主要是基准与推理时评估框架，而非训练一个用于回答反事实问题的新模型；所给章节未定义被测大语言模型或 PRISM 解析器的可优化训练损失，因此训练目标为不适用，原文未明确报告相关优化目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. WhatIfBench 任务与量规**

基准包含 220 个开放式、长时程反事实问题，覆盖 STEM、HSS 和 Hybrid 三类场景。每个实例具有规范化查询 $q_i$、明确干预 $I_i$、类别 $d_i$ 和问题级量规 $\mathcal{R}_i$；量规描述可接受的推理空间、约束、机制及解释要求，而不是指定唯一 gold conclusion。

> 直观理解：量规的作用是规定“一个好答案至少应讨论什么”，同时允许多个合理的未来路径，因此更适合开放领域的反事实问题。

**2. 响应到图的解析器**

解析流程使用解析器模型 $p_{\theta}$ 从回答中抽取 EDU、语义关系和支持—核心结构；每个关系记录表示源节点、目标节点、关系标签及结构类型，其中结构类型属于 $\{\mathrm{SN},\mathrm{NS},\mathrm{NN}\}$。解析结果经关系归一化、引用解析、重复边删除后映射为 EDU 级有向图；若无有效解析，则使用句子级顺序边作为 fallback。

> 直观理解：该模块把“先发生什么、导致什么、支持什么”显式化，避免评估器只凭表面措辞给分；fallback 则保证异常回答仍能进入统一评估流程。

**3. PRISM 双指标评估**

PRISM 联合使用图级 PM 与答案级 RM。PM 关注响应派生图的因果有效性，RM 依据 $\mathcal{R}_i$ 检查解释的内容覆盖和说明充分性；二者互补，使评估同时考虑因果拓扑与最终答案质量。

> 直观理解：只看最终结论可能漏掉中间推理错误，只看图结构又可能忽略答案是否真正回应问题；双指标分别检查这两方面。

**训练与推理**

WhatIfBench 的构建包括候选问题收集、筛选、规范化改写、领域标注、量规编写以及问题级和量规级质量审查。推理时，对每个 $x_i$ 运行被测模型得到 $y_i$，再以温度 $\tau=0$、解析预算 $B$ 和关系标签集 $\mathcal{L}$ 调用解析器 $p_{\theta}$；解析得到有效 EDU 和关系后生成 $\mathcal{G}_{y_i}$，否则使用句子切分与 $\mathrm{SEQUENCE}$ 边的启发式图，最后计算 PM、RM 和最终 PRISM 分数。给定章节没有说明被测模型或解析器是否在该基准上进行微调，因此应将其理解为独立评估流程，而非端到端联合训练。

**复现信息**

复现评估所必需的流程细节包括：关系记录写作 $\mathcal{R}=\{(s_j,t_j,\ell_j,\nu_j)\}_{j=1}^{m}$，其中 $\ell_j\in\mathcal{L}$、$\nu_j\in\{\mathrm{SN},\mathrm{NS},\mathrm{NN}\}$；解析器输出后先抽取 EDU，再构造支持—核心结构，建立结构节点到 EDU 的引用映射，归一化关系标签并解析源、目标 EDU，最后去重并排除自环。若解析输出为空、没有 EDU 或没有关系但 EDU 数量大于 1，则按算法规定分别回退到句子级顺序图或平坦顺序结构；这些设计保证不同长度和不同格式的回答都能获得统一的图表示。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- WhatIfBench：包含 220 个 what-if 问题，划分为 STEM、HSS 和 Hybrid 三类，用于测试模型在开放域、开放形式和长时程反事实场景中的因果解释能力；实验使用固定测试集。
- IfQA：作为外部反事实推理基准，用于与 WhatIfBench 比较模型排名和任务难度。原文未明确报告本实验所使用的 IfQA 样本规模与具体划分。
- CounterBench：作为另一项外部反事实推理基准，用于检验 WhatIfBench 的模型排序是否与既有基准一致。原文未明确报告本实验所使用的 CounterBench 样本规模与具体划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Process Metric (PM)**

在响应派生语义因果图中，检查每条因果相关边是否有文本支持、关系类型是否匹配、方向是否正确且机制上可解释；它衡量局部因果转移的有效性，而不是直接判断现实世界因果模型的真实性。 （越高越好，因为更高表示更多因果相关边得到严格支持；但它不能单独证明解释已经覆盖所有必要机制或下游后果。）

</div>
<div class="metric-item" markdown="1">

**Rubric Metric (RM)**

依据每道问题的冻结问题级量规，评价答案是否覆盖前提忠实性、机制、下游后果、领域约束、不确定性处理和解释完整性等要求；每个量规标准按 1 至 10 分评分后归一化。 （越高越好，因为更高表示答案满足更多问题特定的解释要求；它是答案层面的充分性指标，不等同于每一条因果边都在局部上有效。）

</div>
<div class="metric-item" markdown="1">

**Final Score**

将所有样本上的平均 PM 与平均 RM 等权平均，即同时汇总因果过程有效性和解释层面的覆盖度。 （越高越好；它便于总体比较，但可能掩盖 PM 与 RM 之间的权衡，因此实验同时报告二者。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### WhatIfBench 总体难度：六个前沿模型的 Final Score

<div class="result-value" markdown="1">

GPT-5.5 得分最高，为 64.62；Claude-Opus-4.7 为 59.11，其余模型均低于 57。该结果说明即使是最强模型也未接近满分，开放域、开放形式、长时程反事实因果推理仍然困难。

</div>

作者据此主张 WhatIfBench 尚未饱和。其合理含义是模型生成流畅文本并不等于能够可靠地从反事实前提连续传播因果后果；但该结果不能证明模型在所有反事实任务或现实因果推理中都普遍失败，因为测试集规模和领域范围仍由 WhatIfBench 的设计限定。

<div class="result-source" markdown="1">

来源：第 5.2 节 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Even the strongest model, GPT-5.5, achieves a final score of only 64.62, followed by Claude-Opus-4.7 with 59.11.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 领域分组：STEM、HSS 与 Hybrid 的 PM/RM 差异

<div class="result-value" markdown="1">

各模型总体上在 STEM 上表现较好，HSS 通常更困难；Hybrid 并非对所有模型都最难，但表现波动更大。以 GPT-5.5 为例，STEM 的 PM/RM 为 72.77/64.00，HSS 为 57.38/61.98，Hybrid 为 65.32/64.80。

</div>

作者将 STEM 的相对优势解释为科学或技术机制通常更稳定，而 HSS 需要处理路径依赖、制度动态和多主体社会后果。该结果主要支持“领域会改变失败类型和难度”的诊断性结论，不能单独证明 HSS 问题在客观上更复杂，因为不同类别的问题内容、约束和量规也可能不同。

<div class="result-source" markdown="1">

来源：第 5.2 节 Finding 2；GPT-5.5 数值见表 2 Main results on WhatIfBench

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Models perform consistently better on STEM scenarios, where counterfactual consequences are often governed by more stable scientific or technical mechanisms.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 过程有效性与解释充分性的互补性：总体 PM 与 RM

<div class="result-value" markdown="1">

所有模型的总体 PM 均高于总体 RM；Qwen3-Max 的总体 PM 为 58.07，但总体 RM 仅为 46.45。GPT-5.5 和 Claude-Opus-4.7 在 PM 与 RM 两项上均排名前两位，最终分数分别为 64.62 和 59.11。

</div>

这表明答案可能包含若干局部上合理的因果转移，却没有完整覆盖问题要求的机制、约束或下游后果；因此只看局部因果边会高估解释质量。作者据此支持 PRISM 将 PM 与 RM 联合报告的设计，但相关性不是因果证明，且 PM/RM 的分离仍依赖自动解析和 GPT-5.4 评估器。

<div class="result-source" markdown="1">

来源：第 5.2 节 Finding 3；总体数值见表 2 Main results on WhatIfBench

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For example, Qwen3-Max achieves a relatively strong overall PM of 58.07 but a much lower overall RM of 46.45, suggesting that locally plausible causal transitions do not necessarily yield a complete or well-grounded explanation.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验只评估六个前沿模型，并在一个包含 220 道题的 WhatIfBench 固定测试集上进行；因此结论首先适用于该基准的题目构成，不能直接推广到所有反事实任务、模型家族或真实世界因果决策。
- PRISM 的自动解析与判分统一使用 GPT-5.4，且 PM 和 RM 都依赖响应文本、解析模式和问题级量规；虽然人工审查与人工相关性结果提供了支持，但 Edge Validity 低于节点和图结构有效性，RM 的 Spearman 相关也低于其 Pearson 相关，说明边级解析和排序一致性仍存在误差。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- IfQA：提供外部基准比较，可检验 WhatIfBench 与较传统反事实问答评价之间的差异；其报告指标为 EM。
- CounterBench：提供另一种反事实推理比较，可检验模型在不同任务定义下的排名稳定性；其报告指标为 Acc。
- Human–Human agreement：不是模型基线，而是人工一致性上限，用于判断 PRISM 与人工评分的接近程度。
- 人工审查的图解析结果：不是竞争模型基线，而是对响应到图解析质量的参照，用于检验 PRISM 中间表示是否可靠。

**实验想回答的问题**

- 在固定生成协议下，当前前沿大语言模型能否在 WhatIfBench 的开放域、开放形式、长时程反事实因果推理中，同时维持因果过程有效性与解释覆盖度？
- PRISM 的过程指标、量规指标及其响应派生语义因果图，能否揭示模型的因果断裂、前提漂移和拓扑碎片化，并与人工判断保持一致？

**实验实现**

实验评估六个前沿大语言模型：GLM-5.1、DeepSeek-V4-Pro、Qwen3-Max、Gemini-3.1-Pro-Preview、Claude-Opus-4.7 和 GPT-5.5。所有模型使用同一回答生成模板，在固定 WhatIfBench 测试集上生成回答，模型侧温度为 $\tau=0.6$、生成预算为 4,096 tokens；回答原样送入 PRISM，不使用模型专属提示、答案归一化或事后修正。PRISM 使用统一的 GPT-5.4 进行解析与判分，评估器温度为 $\tau=0.0$，并对所有模型采用相同提示和解码设置。结果按 STEM、HSS、Hybrid 分组报告，同时报告总体 PM、总体 RM 和等权 Final Score。弱回答分析选取 Final Score 低于 60 的回答，五类失败标签允许重叠。另以三组人工审查检验节点、边、图结构和因果关系解析质量，并以人工—人工一致性作为 PRISM—人工相关性的参照。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未提供单个回答级别的具体定性案例或逐步对照案例；实验主要通过总体分数、失败模式标签、响应派生图的节点数与最长路径，以及人工相关性分析进行定量诊断，因此不能据此补写某一具体问题的因果链。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：构建开放域反事实因果推理基准及语义因果图评测方法，核心是评估LLM的反事实推理能力。; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`5f266b365cc6d8963dfd0197de5f5437ac0faf9b8a1fb719646595f2035b9eff`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
