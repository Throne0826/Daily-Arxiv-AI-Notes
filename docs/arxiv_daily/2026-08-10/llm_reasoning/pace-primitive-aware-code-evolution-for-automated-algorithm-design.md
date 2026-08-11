---
title: "[论文解读] PACE: Primitive-Aware Code Evolution for Automated Algorithm Design"
description: "[arXiv 2608.07395][LLM Reasoning] PACE 将自动算法设计中原本随完整程序一同淘汰的局部代码逻辑，表示为可持续复用的可执行算法原语，并通过受约束的代码演化与自适应选择促进其跨程序迁移。"
arxiv_id: "2608.07395"
announcement_date: "2026-08-10"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-11T02:33:07.992255+00:00"
source_sha256: "c64efea3aa3d54a95593ade9159568e22f83f3a9aeb83531617ffcade78a383f"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "自动算法设计"
  - "程序演化"
  - "可执行算法原语"
  - "Thompson采样"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.07395</p>

# PACE: Primitive-Aware Code Evolution for Automated Algorithm Design

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-10</span>
<span><strong>作者</strong> Zhuoliang Xie, Ruihao Zheng, Xiang Xu, Genghui Li, Zhengkun Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Southern University of Science and Technology；Shenzhen University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.07395v1) · [PDF 下载](https://arxiv.org/pdf/2608.07395v1) · **关键词** 大语言模型, 自动算法设计, 程序演化, 可执行算法原语, Thompson采样<br>


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

PACE 将自动算法设计中原本随完整程序一同淘汰的局部代码逻辑，表示为可持续复用的可执行算法原语，并通过受约束的代码演化与自适应选择促进其跨程序迁移。

**不用术语来说**：用大语言模型自动设计程序时，系统通常生成、测试并筛选整段算法代码；一段程序即使总体表现不好，其中某个局部函数也可能很有价值，但它会和整段程序一起被丢弃。后续搜索因此可能反复寻找已经出现过的有效思路，消耗有限的程序评估预算。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出“可执行算法原语”（EAP）：把算法中的局部逻辑实现为具有稳定身份、可被后续候选程序调用的函数，从而使其不依附于首次出现的宿主程序而持续保留。
- 提出 PACE：利用原语感知的变异操作保证原语保留与跨程序组合，并依据子代相对父代的改进，以 Thompson sampling 动态决定哪些原语更值得暴露给后续生成步骤，且不需要额外验证集或评估预算。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于基于大语言模型（LLM）的自动算法设计（AAD）领域。AAD将算法搜索表示为一个闭环：LLM生成或修改可执行程序，程序评估器根据任务性能给出反馈，系统再据此产生后续候选算法。现有方法通常把完整算法程序作为最小演化单位，因此一个程序被淘汰时，其中可能有价值的局部逻辑也会随之丢失。PACE关注的核心问题是：如何在保持完整算法搜索能力的同时，将有用的局部代码从一个宿主程序中抽取出来，并持久地转移到后续程序中。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**基于LLM的自动算法设计（LLM-based AAD）**

LLM根据算法描述、已有程序和评估反馈生成或修改可执行算法。程序运行结果充当搜索反馈，使系统能够在较少人工领域知识的情况下迭代改进算法。

</div>
<div class="concept-item" markdown="1">

**程序演化与变异算子**

程序演化把候选算法视为可被反复修改的个体，变异算子则规定如何从已有程序产生新程序。传统AAD中的交叉和变异通常直接处理完整父程序，LLM可以对其中任意代码进行修改，缺少明确的局部组件边界。

</div>
<div class="concept-item" markdown="1">

**可执行算法原语（Executable Algorithmic Primitive，EAP）**

EAP是实现为可调用函数的局部算法逻辑，并具有跨宿主算法保持不变的身份。PACE将有潜力的EAP保存到持续更新的集合中，使后续候选算法可以重新调用或组合它，即使包含它的原算法已经被淘汰。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个算法设计任务及其程序评估器，系统需要从候选程序空间中搜索性能较高的可执行算法。每个候选算法都可以看作一个完整程序，其中部分局部逻辑被表示为可调用的EAP；算法评估器为程序提供任务性能反馈。PACE的设定假定程序可以运行并接受统一的任务评价，而且局部逻辑能够以函数形式抽取、保存和再次调用。搜索目标是在固定或相同的评估预算下发现竞争力强的算法，同时保留能够跨程序复用的有效组件；根据给定章节，方法不依赖额外验证集或额外评估预算。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$A$**

一个完整的候选算法或宿主程序。

</div>
<div class="notation-item" markdown="1">

**$e$**

一个可执行算法原语，即具有稳定身份并能被算法调用的局部函数逻辑。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{E}$**

动态EAP集合，用于保存并管理在算法演化过程中提取的原语。

</div>
<div class="notation-item" markdown="1">

**$\Delta$**

相对于父算法的性能改进量；PACE用子代相对父代是否改进来为参与转移的EAP积累反馈。给定章节未明确报告其具体数值定义或完整公式。

</div>

</div>

**直接相关的工作**

- **Evolution of Heuristics（EoH，Liu et al., 2024）**: EoH代表将LLM代码生成与程序评估结合的自动启发式算法设计方法。PACE沿用这种闭环搜索范式，但针对完整程序作为演化单位所造成的局部逻辑丢失问题，引入具有持久身份的EAP及面向原语的代码演化机制。
- **EvoLattice（Yuksel, 2025）**: 原文将EvoLattice作为认识到直接编辑完整算法存在局限的近期工作。PACE进一步把局部算法组件明确建模为可执行且可跨程序转移的EAP，并通过原语级操作和基于父代相对改进的Thompson采样来选择后续要暴露给LLM的原语。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

自动算法设计（AAD）希望在缺少人工领域专家持续编写启发式规则的条件下，借助大语言模型生成可执行程序、由任务评估器反馈性能并迭代改进。这类过程的关键资源是候选算法的评估次数：若有用的局部逻辑无法积累和迁移，搜索会把预算花在重复发现相似代码上，难以稳定组合不同候选中已经验证过的有效部分。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于大语言模型的整程序演化式 AAD**：FunSearch、EoH 及其后续方法将完整可执行算法作为搜索个体：大语言模型根据父代程序及其评估结果生成或修改代码，评估器为完整程序打分，再保留高分程序并淘汰低分程序。反思、树搜索和种群管理等机制改进了候选程序的生成或调度，但基本评价和存活单位仍是完整算法。
- **整程序交叉与变异**：现有变异或交叉通常将一个或多个父代完整程序放入大语言模型上下文，由模型自由重写、组合或修改代码。这样可以探索较大范围的算法变化，但代码中哪些局部函数、规则或计算步骤应被保留，并没有显式结构约束或独立归因机制。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 完整程序是最小存活单位，导致低分程序被淘汰时，其内部可能对另一种算法有用的局部逻辑也被一并删除。原文指出："eliminating a low-performing algorithm entails discarding all of its local logic, including components that could be valuable in a different algorithm"（Introduction，Figure 1(a) 说明）。结果是有用逻辑可能被反复丢弃和重新发现，浪费搜索预算。
- 自由编辑完整代码不能可靠地区分局部逻辑的正负贡献，也不能把一次子代改进明确归因给某个可复用组件。即便某段代码曾参与高分候选，其价值仍与宿主程序、其他改动及提示上下文耦合；因此系统缺少一种能跨宿主程序积累证据、并据此优先复用局部组件的机制。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有方法已能以完整程序为对象进行生成、评估和进化，但尚未在代码层面提供一种同时满足三项条件的机制：局部算法组件可脱离原宿主持续存在、其跨程序使用受到可追踪的结构性约束、以及其效用可仅利用既有任务评估反馈被自适应估计。

</div>
<div markdown="1"><span>核心问题</span>

在不增加辅助验证数据和额外算法评估预算的前提下，如何把自动算法设计中的局部代码逻辑变成可持久复用、可跨程序转移且可按实际收益优先选择的搜索对象，从而提高有限预算下发现高性能算法的效率？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把一段值得保留的局部逻辑封装成可调用函数，而不是把它视为一次性完整程序的内部文本。这样，原程序即使总体失败，该函数仍可被保存并插入或替换到后续候选中；若带有该函数的子代相对其父代经常改进，就提高其被再次选中的机会，反之降低。通俗地说，系统不再只记住“哪份完整作业得分高”，还会保留并检验“作业中哪种可复用解题步骤值得带到下一份作业”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PACE将自动化算法设计从“只进化完整程序”扩展为“同时维护完整算法与可复用局部函数”。系统输入任务定义、算法搜索空间$\mathcal{A}$、完整算法评价器$J$和有限评价预算$B$；搜索状态由完整算法种群$\mathcal{P}_t$、持久化EAP集合$\mathcal{E}_t$以及迁移证据$\mathcal{H}_t$组成。EAP（Executable Algorithmic Primitive，可执行算法原语）是搜索过程中生成或从已评价程序中提取的可调用函数$e=(\sigma_e,\phi_e)$：$\sigma_e$描述其用途，$\phi_e$给出固定的可执行实现。完整算法仍是唯一接受任务评价的对象，EAP不单独获得任务分数；系统通过EAP被迁移前后子代相对父代的性能变化，间接判断它是否值得继续复用。

端到端地看，每轮搜索先选择父程序，再从动态EAP集合中选择可迁移原语，并通过Insert、Replace、Refine或Crossover产生候选程序；随后调用$J$评价完整候选，更新算法种群，并在适用的单原语迁移操作中把“相对父代是否改进”写入$\mathcal{H}_t$，供Thompson sampling调整后续EAP选择。与此同时，系统可以生成新EAP或从已评价算法中提取局部函数，且一经接纳便不会因其来源程序被淘汰而删除。通俗地说，普通方法淘汰一个方案时会连同其中有用的小技巧一起丢弃；PACE把这些小技巧保存成带接口的函数零件，使其能够装入未来产生的其他方案。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始化双层搜索状态

构造状态$S_t=(\mathcal{P}_t,\mathcal{E}_t,\mathcal{H}_t)$，其中$\mathcal{P}_t$存放可被选择和淘汰的完整算法，$\mathcal{E}_t$存放独立持久化的EAP，$\mathcal{H}_t$记录EAP跨程序迁移后的效果证据。评价器只作用于完整算法，评价调用总数$N_J$不得超过$B$。

<div class="method-step__io" markdown="1">

**输入**：AAD任务、算法空间$\mathcal{A}$、完整程序评价器$J:\mathcal{A}\rightarrow\mathbb{R}$、评价预算$B$，以及初始完整算法。<br>
**输出**：可同步演化完整程序和可复用局部函数的初始搜索状态。

</div>

**直观理解**：系统维护两个不同寿命的仓库：完整方案参加竞争，函数零件则长期留存。这样即使某个完整方案后来被淘汰，它贡献过的局部实现仍可继续参与搜索。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 发现并接纳EAP

PACE通过EAP Generation直接提出新函数，或通过EAP Extraction从已评价算法中识别可独立调用的局部逻辑；接纳后的原语表示为$e=(\sigma_e,\phi_e)$。其中实现$\phi_e$在迁移时保持不变，若修改其实现，则应视为不同EAP；每代至多提出$1$个生成或提取候选。

<div class="method-step__io" markdown="1">

**输入**：任务描述、当前或历史上已评价的完整算法，以及当前EAP集合$\mathcal{E}_t$。<br>
**输出**：更新后的持久EAP集合$\mathcal{E}_{t+1}$，其中原有已接纳EAP继续保留。

</div>

**直观理解**：生成相当于专门设计一个新零件，提取则相当于把完整程序中已经出现的有效片段拆成标准零件。固定函数实现保证系统评价的是同一个零件在不同宿主中的迁移效果，而不是名称相同但内容不断变化的代码。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 选择父程序、EAP与结构化变异操作

系统选择父算法，并利用基于父代相对性能改进的Thompson sampling从$\mathcal{E}_t$选择待迁移EAP；随后应用四类原语感知操作：Insert和Replace引入一个焦点EAP，Refine和Crossover复用既有EAP结构。前两类操作在结构上明确单个焦点EAP，因此可产生针对该EAP的迁移证据；后两类操作不把结果归功于某一个EAP。

<div class="method-step__io" markdown="1">

**输入**：完整算法种群$\mathcal{P}_t$、EAP集合$\mathcal{E}_t$、迁移证据$\mathcal{H}_t$以及每个算法最多包含$k$个EAP的约束。<br>
**输出**：显式调用零个或多个EAP、且可由评价器执行的候选完整算法。

</div>

**直观理解**：Thompson sampling在“继续使用看起来有效的零件”和“尝试证据不足的零件”之间进行概率化权衡。Insert与Replace像给一个方案装入指定零件，便于判断该零件是否有帮助；Refine与Crossover同时改动的因素更多，因此不强行把成败记到单一零件名下。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 评价、信用更新与种群更新

调用$J$得到候选完整算法的任务分数，并按既有进化循环更新$\mathcal{P}_t$；当候选来自Insert或Replace时，将候选相对父代的性能改进转化为该焦点EAP的迁移证据并写入$\mathcal{H}_{t+1}$。被种群选择淘汰的完整算法从$\mathcal{P}_t$消失，但其已接纳EAP仍保留在$\mathcal{E}_{t+1}$。

<div class="method-step__io" markdown="1">

**输入**：候选完整算法、对应父算法、所用操作、焦点EAP以及评价器$J$。<br>
**输出**：新的状态$S_{t+1}=(\mathcal{P}_{t+1},\mathcal{E}_{t+1},\mathcal{H}_{t+1})$以及截至当前评价预算内发现的最佳完整算法。

</div>

**直观理解**：系统不为零件额外建立测试集，也不单独运行零件，而是观察装入该零件后的完整方案是否优于父方案。这样可在同一任务预算中积累复用证据，同时避免把宿主程序本来就很强误当成零件本身的贡献。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 有限评价预算下的AAD目标

$$
A^{\star}=\arg\max_{A\in\mathcal{A}}J(A),\qquad N_J\leq B
$$

**符号说明**

- $A^{\star}$：在给定评价预算内搜索到的最佳完整算法
- $\mathcal{A}$：任务允许的完整算法空间
- $A$：一个可执行的完整候选算法
- $J$：从完整算法映射到实数分数的任务评价器，文中约定分数越大越好
- $N_J$：搜索过程中对评价器的累计调用次数
- $B$：允许使用的有限评价预算

<div class="equation-explanation" markdown="1">

**直观理解**：PACE没有改变自动化算法设计最终要优化的对象：目标仍是在有限次完整程序评价中找到最高分算法。它改变的是搜索过程内部保存什么信息、如何产生候选以及如何复用局部代码，而不是给EAP另设一个可直接优化的任务分数。<br>
**原文位置**：Primitive-Aware Automated Algorithm Design，公式(3)

</div>

</div>

<div class="equation-block" markdown="1">

#### PACE扩展搜索状态

$$
S_t=(\mathcal{P}_t,\mathcal{E}_t,\mathcal{H}_t)
$$

**符号说明**

- $S_t$：搜索步骤t时PACE的完整内部状态
- $t$：当前搜索步骤
- $\mathcal{P}_t$：步骤t时参与选择、变异和淘汰的完整算法种群
- $\mathcal{E}_t$：步骤t时已经接纳并可供迁移的持久EAP集合
- $\mathcal{H}_t$：截至步骤t从EAP跨算法迁移中积累的效果证据

<div class="equation-explanation" markdown="1">

**直观理解**：标准进化搜索主要围绕完整程序种群运行；该式表明PACE额外把可复用函数和迁移证据提升为显式搜索状态。三部分分别回答“当前有哪些完整方案”“有哪些长期可复用零件”以及“过去迁移这些零件是否有效”，从而支持后续的原语选择和结构化变异。<br>
**原文位置**：Primitive-Aware Automated Algorithm Design，公式(4)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：PACE不是通过梯度下降训练一个参数化模型，其外层优化仍是有限预算下最大化完整算法得分$J(A)$。EAP没有独立任务目标，也不额外使用评价数据集；其信用来自Insert或Replace所生成子代相对父代的性能变化，并通过$\mathcal{H}_t$影响Thompson sampling的后续选择概率。因此，这里的“学习”发生在搜索策略层面：完整程序分数决定种群更新，父代相对改进决定哪些EAP更值得迁移。原文节选没有给出Thompson sampling的具体概率模型和更新公式，不能据此补写似然、先验或奖励二值化规则。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 持久化EAP表示与发现模块**

每个EAP写作$e=(\sigma_e,\phi_e)$，由文本描述$\sigma_e$与可执行函数$\phi_e$组成；算法$A$对当前EAP集合的实际使用由调用集$\mathcal{C}(A;\mathcal{E}_t)$区分。EAP可由生成模块直接提出，也可由提取模块从已评价算法中获得，并满足接纳后的单调持久性：来源算法退出种群不会删除该EAP。

> 直观理解：“集合中可用”不等于“当前程序正在使用”：只有程序显式调用函数，EAP才参与该程序执行。这种分离使局部知识不再依附于某个完整程序的生存状态，是跨代和跨程序迁移成立的基础。

**2. 原语感知变异操作模块**

PACE使用P1至P4四类操作，对应文中Insert、Replace、Refine和Crossover。Insert与Replace各自引入一个焦点EAP，并把候选相对父代的变化用于该EAP的信用评估；Refine和Crossover保持或重组现有EAP调用结构，但由于变化不能唯一归因于单个EAP，系统不向某一个EAP分配信用。

> 直观理解：普通代码生成可能在改写程序时无意删除有价值的函数；这些操作把EAP的保留或转移变成结构约束。它们既负责实际复用代码，也规定什么情况下可以合理判断某个零件带来了改进。

**3. 基于迁移证据的Thompson sampling**

模块读取$\mathcal{H}_t$中由单焦点EAP操作产生的父代相对改进证据，以Thompson sampling决定后续优先暴露和迁移哪些EAP。所给章节未提供其先验、后验更新或成功事件定义的完整公式，因此不能据此进一步指定分布参数。

> 直观理解：仅永久保存大量函数会让选择越来越困难，因此系统还需学习哪些函数更可能在新宿主中有效。使用相对父代的变化，是为了评价“装入这个函数后是否变好”，而不是简单偏爱曾经出现在高分程序中的函数。

**训练与推理**

搜索阶段从初始完整算法种群开始，循环执行父代选择、EAP选择、原语感知候选生成、完整算法评价和种群更新，直到评价器调用达到预算$B$。每轮还允许至多提出$1$个EAP Generation或Extraction候选；已接纳EAP独立留存在$\mathcal{E}_t$中。候选程序若通过Insert或Replace引入单个焦点EAP，系统将其相对父代的改进写入迁移历史；若通过Refine或Crossover生成，则复用EAP结构但不把结果归因给单个EAP。最终输出评价预算内得分最优的完整可执行算法，而不是EAP集合本身。

部署或测试时，使用搜索阶段选出的完整程序直接在任务环境中执行；EAP只是该程序内部显式调用的固定函数，并非需要另行训练或预测的模型。论文实验中的“training”指算法在训练实例或固定训练种子上的搜索与选择，“test”则指将训练阶段选出的最佳程序直接用于未参与搜索的环境种子或更大TSP规模；因此测试过程不再更新$\mathcal{P}_t$、$\mathcal{E}_t$或$\mathcal{H}_t$，其目的在于检验所发现程序的零样本泛化。

**复现信息**

复现实验时最关键的统一设置是：完整算法种群规模为$20$，参数$k=3$同时限制单个算法最多包含的EAP数和结构化生成的最大尝试次数，每代最多进行$1$个EAP Generation或Extraction提案。搜索预算方面，正文的收敛实验按$1000$次评价展示；但所给节选对“评价器调用”和个别基线的“模型调用”分别表述，复现时应核对完整论文中的统一预算口径，避免把LLM调用数与任务评价数直接等同。

方法解释还需保留两项边界条件。第一，EAP的实现$\phi_e$在迁移时固定，修改实现即产生新EAP，否则迁移证据无法对应稳定对象。第二，EAP集合具有持久性，但完整程序仍可被种群机制淘汰；PACE由此增加了可用代码上下文和选择负担，$k$正是控制单个程序组合复杂度的主要参数。所给节选没有完整披露EAP接纳判据、去重机制、Thompson sampling后验细节以及四种操作的精确提示模板，这些内容均应在源码或论文未截取部分中进一步核验。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 连续控制环境：包括OpenAI Gym中的Racing Car与Bipedal Walker。Racing Car以视觉输入为主，Bipedal Walker以状态输入为主，用于检验PACE生成的程序化连续控制策略能否跨不同输入模态和控制问题发挥作用。给定摘录仅说明环境种子固定，未完整报告训练与测试种子数量及具体划分规模。
- TSP：旅行商问题实例，目标是在复杂组合搜索空间中进化能改善最终路径质量的算法。训练实例、测试实例数量及节点规模在给定摘录中未完整展示；训练实例用于搜索和选择程序，测试实例仅用于评估训练阶段选出的最佳程序。
- TSP-ACO：由蚁群优化框架引导的旅行商问题，PACE负责进化其中的算法逻辑，以检验EAP机制能否改进既有组合优化框架。该设置同时允许与DeepACO等神经方法及传统ACO进行比较；实例规模和完整数据生成参数在给定摘录中未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**最佳训练分数**

每次搜索在1000次评估内找到的最佳程序在训练评估器上的得分，并在三次独立运行之间报告均值和标准差；它主要衡量搜索效率、最终训练质量和运行稳定性。 （依任务表格中的箭头解释。给定摘录明确显示Racing Car与Bipedal Walker为越高越好，因为更高回报表示控制策略完成任务的质量更好；TSP与TSP-ACO的具体分数定义和方向在摘录中未完整展示。）

</div>
<div class="metric-item" markdown="1">

**测试分数**

搜索结束后，仅将训练评估器选出的最佳程序放到测试实例或测试环境上评估，用于衡量该程序对未参与搜索选择的数据或环境的泛化表现。 （依具体任务的评价定义而定；控制任务表中为越高越好，路由任务的方向在给定摘录中未明确报告。）

</div>
<div class="metric-item" markdown="1">

**收敛曲线**

展示搜索过程中最佳性能随评估次数变化的轨迹，用于比较不同方法找到高质量算法的速度和最终收敛水平。图3覆盖Racing Car、Bipedal Walker和TSP-ACO。 （在同一评估次数下达到更优任务分数更好；曲线更早达到较优水平通常表示样本或评估效率更高，但给定摘录没有提供曲线数值。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四项任务的总体比较

<div class="result-value" markdown="1">

作者声称PACE在四项任务上能够发现具有竞争力的算法，并在进化过程中从结构上保留有价值的算法组件；但给定摘录没有包含表1及其他结果表的完整数据，因此无法核验PACE相对各基线的具体优势、排名、均值或标准差。

</div>

这项总体结论说明PACE至少被作者认为能够同时适用于连续控制和组合优化，而不是只针对单一任务设计。它支持的是方法的跨任务可用性及组件保留目标，不足以单独证明PACE在每个任务上都显著优于所有LLM、神经和经典基线，也不能据此判断提升是否具有统计显著性。

<div class="result-source" markdown="1">

来源：Abstract；具体数值表在给定摘录中未完整提供

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Experiments on four tasks demonstrate that PACE effectively discovers competitive algorithms while structurally preserving valuable algorithmic components.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Racing Car、Bipedal Walker与TSP-ACO的搜索过程

<div class="result-value" markdown="1">

图3报告了三项任务的收敛曲线，但给定文本没有提供曲线数值或作者对曲线差异的完整文字结论，因而无法可靠量化PACE的收敛速度及最终优势。

</div>

这组实验原本用于观察PACE是否在固定1000次评估预算内更快找到较优算法，并检验这种搜索行为能否跨视觉控制、状态控制和组合优化保持一致。仅知道存在收敛图并不能证明PACE收敛更快，因为还需要读取曲线位置、误差范围以及各基线轨迹。

<div class="result-source" markdown="1">

来源：Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Figure 3: Convergence curves on three diverse tasks.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 训练选择后的测试泛化

<div class="result-value" markdown="1">

实验对训练阶段选出的最佳程序进行测试集评估，但给定摘录未包含任何完整测试分数，因此无法判断PACE的测试优势是否与训练优势一致，也无法量化泛化差距。

</div>

这一协议把“搜索时见过的数据上的表现”和“搜索完成后的泛化表现”分开，可以减少直接用测试集指导程序进化造成的信息泄漏。不过，固定实例及单次最佳程序选择仍可能带来选择偏差；必须结合完整测试表和多次运行波动才能评价泛化可靠性。

<div class="result-source" markdown="1">

来源：Details of Evaluations & Experiments；Table 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Test instances are evaluated only after the search selects the best-performing algorithm from the training performance.

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

- LLM整程序及反思式进化基线：EoH代表标准算法进化，ReEvo代表利用反思反馈的进化。它们用于判断PACE把局部逻辑拆成持久EAP并进行跨程序迁移，是否优于主要以完整程序为搜索单位的方法。
- LLM搜索与多样性基线：MCTS-AHD代表树搜索式自动算法设计，HSEvo代表强调混合多样性的进化方法。二者用于区分PACE的收益究竟来自更一般的搜索增强，还是来自原语保留、迁移与选择机制。
- 任务专用LLM基线MLES：用于多模态连续控制算法进化。实验仅采用其冷启动模式，因为带种子的模式会引入外部程序先验；该比较用于检验PACE在不借助额外程序知识时能否与专门面向控制任务的方法竞争。
- 非LLM基线：控制任务采用PPO，组合优化采用DeepACO，TSP-ACO还采用传统ACO。它们分别代表神经强化学习、神经组合优化和经典非学习启发式方法，用于判断自动生成程序相对于不同技术路线的实际竞争力。

**实验想回答的问题**

- PACE能否在连续控制与组合优化两类差异明显的任务上，通过保留并迁移可执行算法原语（EAP），发现具有竞争力的程序化算法？
- PACE在相同大语言模型、评估预算和训练后测试协议下，相比整程序进化、反思式进化、树搜索、神经方法及经典启发式方法是否更有效？

**实验实现**

PACE在这些实验中仅设置参数$k=3$，但给定摘录没有重新定义$k$的具体语义。所有基于大语言模型的自动算法设计方法统一使用GPT-4o-mini生成算法，每种方法执行3次独立运行，每次最多进行1000次评估；训练结果报告最佳训练分数的均值与标准差。测试阶段不继续搜索，而是把训练评估器选出的全程最佳程序放到测试集上评估。对于同一任务，各方法共享相同评估器和固定实例；PPO配置直接沿用MLES以提高比较公平性，MLES仅使用冷启动模式。全部实验运行于Intel Xeon Gold 6348 CPU。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Its central contribution is LLM-based automated code and algorithm evolution that discovers and transfers reusable algorithmic components.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`c64efea3aa3d54a95593ade9159568e22f83f3a9aeb83531617ffcade78a383f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
