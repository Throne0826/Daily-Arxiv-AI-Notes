---
title: "[论文解读] SHAPE of Chain-of-Thought in Math Reasoning"
description: "[arXiv 2608.28600][LLM Reasoning] 本文提出以“语义空间”和“启发式动作”刻画数学思维链的 SHAPE 框架，旨在揭示模型如何组织解题过程、诊断后训练造成的策略集中，并将诊断所得的启发式信息用于改进强化学习训练。"
arxiv_id: "2608.28600"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:35:56.356794+00:00"
source_sha256: "eb017fd596c1a1f07dbd59db7690aae331a0adea43676e3cf54e0277c6e5712f"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型数学推理"
  - "思维链分析"
  - "语义空间"
  - "数学启发式"
  - "强化学习后训练"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.28600</p>

# SHAPE of Chain-of-Thought in Math Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Jonghyun Song, Sangjun Song, Minjae Oh, Haesung Pyun, Sungsik Lee, Yohan Jo</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28600v1) · [PDF 下载](https://arxiv.org/pdf/2608.28600v1) · **关键词** 大语言模型数学推理, 思维链分析, 语义空间, 数学启发式, 强化学习后训练<br>
**代码**: [https://github.com/holi-lab/SHAPE-of-CoT](https://github.com/holi-lab/SHAPE-of-CoT)

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

本文提出以“语义空间”和“启发式动作”刻画数学思维链的 SHAPE 框架，旨在揭示模型如何组织解题过程、诊断后训练造成的策略集中，并将诊断所得的启发式信息用于改进强化学习训练。

**不用术语来说**：数学大模型即使答对同一道题，也可能采用完全不同的思路；只检查答案或统计推理文本有多长，无法判断模型是否真正形成了合适且连贯的解题策略，也难以解释它为何失败。本文要解决的问题，是把一段冗长的解题文字转化为可分析的数学过程：模型当前从什么角度理解问题、采取了什么有目的的操作，以及何时放弃或重新采用某种思路。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 SHAPE 诊断框架，将思维链表示为语义空间及其内部启发式动作的演化序列，并通过自动分段、启发式标注和空间状态跟踪，将这一数学教育理论视角扩展到大规模模型轨迹分析。
- 把过程诊断与训练连接起来：作者据此考察后训练是否带来新的数学能力，指出强化学习会使成功轨迹的启发式使用趋于集中，并进一步在带可验证奖励的强化学习中引入启发式规划，以改善任务表现。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型数学推理与思维链分析交叉领域。数学推理模型通常输入一道数学问题，生成包含中间步骤的思维链（Chain-of-Thought，简称 CoT），再输出最终答案；但仅依据答案是否正确，难以判断模型究竟采用了什么数学理解和策略。本文借鉴数学教育研究，将一条 CoT 表示为随推理推进而变化的语义空间序列，并记录每个空间中的启发式行动，从而分析模型如何解释问题、选择策略、转换思路以及最终解决问题。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**思维链（Chain-of-Thought, CoT）**

CoT 是模型在最终答案之前生成的逐步文字推理过程，通常包括建模、计算、检验和修正等步骤。本文把这条文本轨迹作为分析模型数学行为的基本输入。

</div>
<div class="concept-item" markdown="1">

**语义空间（semantic space）**

语义空间是模型当前用于理解和解决问题的一种具体数学解释，由它采用的对象、目标和约束共同定义。例如，同一道题可以先被解释为代数方程组，再被解释为试值或计数问题。模型可以维持当前空间、进入新空间，或返回先前使用过的空间。

</div>
<div class="concept-item" markdown="1">

**启发式（heuristic）**

启发式是语义空间中的、有目的的数学行动，例如引入表示、化简问题、探索特定情形或逆向工作。它不同于单纯陈述答案等非启发式步骤；本文用启发式的类型和分布刻画模型实际采取了哪些数学策略。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定数学问题及模型生成的思维链轨迹，SHAPE（Semantic-space and Heuristic Analysis for Problem-solving Evolution）需要将轨迹划分为承载启发式的内容单元，为各单元标注一个或多个启发式，并追踪模型数学解释的变化。其输出不是新的数学答案，而是对推理过程的结构化表示：每个局部步骤对应的启发式标签、当前语义空间，以及语义空间之间的转移状态。基于这些标注，研究进一步计算启发式活动在语义空间中的分布和空间转移频率，并分析它们与最终答案正确性及后训练效果的关系。问题设定默认 CoT 可以被有意义地分段和解释，但文段未声称文字化 CoT 必然忠实反映模型内部计算；相关研究反而指出，CoT 可能包含事后补充或装饰性步骤。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\texttt{SHAPE}$**

Semantic-space and Heuristic Analysis for Problem-solving Evolution，即本文提出的语义空间—启发式分析框架。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{CoT}$**

Chain-of-Thought，模型生成的逐步思维链轨迹。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{Maintain}$**

语义空间状态，表示当前步骤继续使用原有的数学解释。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{New}/\mathrm{Return}$**

语义空间转移状态；$\mathrm{New}$ 表示进入此前未使用的新解释，$\mathrm{Return}$ 表示回到先前访问过的解释。

</div>

</div>

**直接相关的工作**

- **既有思维链分析方法**: 既有工作主要分析 CoT 的表面或整体结构，例如长度、“wait”或“aha”等自我修正标记、规划与验证等宽泛推理片段，以及图或树形式的结构。这些方法有助于描述模型如何组织文本，但通常不追踪每个局部行动所依据的具体数学解释；SHAPE 因而转向语义空间和启发式两个数学问题求解概念。
- **强化学习与可验证奖励后训练（RLVR）**: RLVR 通过最终答案是否正确的结果级信号改进数学推理，但相关研究提示，它可能主要提高采样效率而未扩展模型的推理策略 repertoire，并可能造成推理多样性坍缩或启发式的 mode-seeking。SHAPE 从语义空间组织和启发式使用方式出发补充这一研究方向，而不只比较准确率或输出表面多样性。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型在数学基准上取得较高最终答案准确率，并生成越来越长的思维链，但准确率不能说明模型如何组织解法，也不能区分稳定的数学能力与偶然得到正确答案。若缺少过程层面的诊断工具，研究者便难以定位失败来自错误的问题表述、无效的操作，还是在多个思路之间反复切换；同样也无法判断后训练究竟教会了模型新的解题方式，还是仅强化了原有的高频策略。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **表层思维链特征分析**：通过轨迹长度、“wait”或“aha”等自我修正词汇，以及规划、验证等宽泛阶段标签概括推理过程，再分析这些特征与答案正确性的关系。
- **思维链结构表示**：把推理步骤组织为图或树，以描述步骤之间的连接、分支和回溯等结构模式，但通常不进一步识别每个分支所采用的具体数学解释与操作。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 长度、词汇标记和宽泛阶段主要反映文本形式或一般认知活动，不能追踪模型当前是在代数、几何或数值试验等哪一种数学解释下工作；因此，即使两条轨迹具有相似长度和验证结构，也可能对应实质不同的数学能力。
- 图或树能够呈现分支与回退，却不能说明模型为何切换思路、切换后执行了什么数学动作。这使既有表示难以判断失败是合理探索还是注意力分散，也难以为后训练提供直接、具有数学含义的控制信号。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种有数学教育理论依据、可自动扩展到大量轨迹的过程表示，能够同时刻画模型采用的数学解释、解释内部的具体启发式动作，以及解释之间的维持、新建和返回关系；因而尚不能系统检验这些过程特征是否比传统思维链特征更能解释正确性，也不能据此辨别强化学习是否扩展了模型的解题策略范围。

</div>
<div markdown="1"><span>核心问题</span>

能否把大语言模型的数学思维链表示为“语义空间—启发式动作”的动态序列，并利用该表示回答三个相互衔接的问题：哪些数学过程特征与正确答案最相关，后训练如何改变模型的解题组织方式，以及显式鼓励启发式规划能否反过来提升训练效果？

</div>
<div markdown="1"><span>作者直觉</span>

解题并非单纯生成更多文字，而是在某种问题表述中执行有目的的数学动作。例如，模型可以先建立方程，转而枚举特例，再返回方程求解；这里“建立方程所处的代数解释”和“枚举所处的试验解释”是不同语义空间，而建立表示、简化、逆向推导或考察特例是启发式动作。分别记录“在哪种理解框架中思考”和“具体做了什么”，就能区分围绕少数有效思路持续推进与在许多不相干思路间游移；这些标签也比长度或关键词更接近可被训练直接鼓励的数学行为。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SHAPE（Semantic-space and Heuristic Analysis for Problem-solving Evolution）将大型语言模型生成的思维链（Chain-of-Thought，CoT）视为可观察的解题记录，而不是只检查最终答案。它先把文本轨迹切分为可解释的内容单元，再为每个单元标注一个或多个数学启发式，并依据会改变问题表示或解释的启发式追踪语义空间的切换、保持与返回，最终输出结构化的语义空间序列与启发式序列。基于这两层标注，方法计算启发式在语义空间及其连续片段中的分布，并用有效数量等指标刻画推理努力是集中于少数解释框架，还是分散于多个框架。直观地说，SHAPE不仅问模型“答案对不对”，还问它“采用了什么数学动作、从什么角度理解问题，以及是否在不同角度之间来回切换”。该框架既用于分析模型行为和后训练造成的策略变化，也用于在强化学习训练的提示中加入数学启发式。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建人工共识金标准并选择标注模型

四位作者对轨迹进行内容单元切分和多标签启发式标注，并通过讨论解决分歧，形成包含 $1{,}598$ 个内容单元、$8{,}334$ 个句子的共识集合；随后以加权 $F1$ 评估单元级一致性、以宏平均 $F1$ 评估类别级一致性，比较候选标注模型。

<div class="method-step__io" markdown="1">

**输入**：来自 $\mathrm{MATH\text{-}Perturb}$ 的 $48$ 条 CoT 轨迹，分别由 Qwen3-30B-A3B-Instruct、Qwen3-30B-A3B-Thinking、Qwen3-8B 和 Nemotron-Cascade-8B 生成。<br>
**输出**：人工标注的金标准，以及被选为主要自动标注器的 Grok-4.1-Fast 和 Qwen3.5-27B；除非另有说明，后续 SHAPE 标注使用 Qwen3.5-27B。

</div>

**直观理解**：先由人建立一小批“标准答案”，再选择最接近人工判断的模型来批量阅读 CoT。这样可以避免直接假定任意标注模型都能正确识别数学策略。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 内容单元切分

将轨迹划分为能够被连贯地赋予启发式标签的最小文本跨度。每个单元保留其在原始推理中的顺序，以便之后建立逐步的结构化轨迹。

<div class="method-step__io" markdown="1">

**输入**：一条原始 CoT 文本轨迹。<br>
**输出**：有序内容单元序列 $c_1,c_2,\ldots,c_T$，其中 $T$ 是该轨迹的单元数。

</div>

**直观理解**：类似把一篇解题草稿切成一句句或一小段段“可判断的动作”，例如“设未知数”“分类讨论”或“代回验证”，而不是把整篇草稿当成一个标签。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 启发式多标签标注

标注模型依据统一启发式分类体系，为第 $t$ 个单元分配启发式集合 $H_t\subseteq\mathcal{H}$；分类可包括简化问题、逆向工作、引入辅助对象、改变表示、分类讨论和反证等。一个单元可以同时具有多个启发式，因此该阶段不被限制为单标签分类。

<div class="method-step__io" markdown="1">

**输入**：内容单元序列 $c_1,c_2,\ldots,c_T$。<br>
**输出**：启发式序列 $\mathbf{H}=(H_1,H_2,\ldots,H_T)$，其中 $\mathcal{H}$ 是完整启发式分类体系。

</div>

**直观理解**：模型不只给每段文字贴一个标签，因为一个数学动作可能同时“改变表示”并“形式化结构”。多标签设计更接近真实解题过程，但也意味着标注本身带有解释性。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 语义空间追踪与结构化输出

对包含表示变化型启发式的单元，追踪模型选择 $\mathrm{New}$、$\mathrm{Maintain}$ 或 $\mathrm{Return}$：$\mathrm{New}$ 开启新语义空间，$\mathrm{Maintain}$ 延续当前空间，$\mathrm{Return}$ 从记忆缓冲区中联合确定要返回的目标空间；其他单元默认留在当前空间。

<div class="method-step__io" markdown="1">

**输入**：带有启发式集合的内容单元序列，以及用于记录已见语义空间的记忆缓冲区 $\mathcal{M}$。<br>
**输出**：语义空间序列 $\mathbf{S}=(s_1,s_2,\ldots,s_T)$，以及与其对齐的 $\mathbf{H}$，共同构成结构化 SHAPE 轨迹。

</div>

**直观理解**：语义空间表示模型正在用哪种数学视角理解问题，例如代数约束或试探计数。追踪器像一个书签系统：模型可以继续当前视角、开一个新视角，或回到以前的视角。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 语义空间启发式活动的有效数量

$$
N_{\text{space}}^{\text{eff}}=\exp\!\left(-\sum_{i\in\mathcal{I}}q(i)\log q(i)\right)
$$

**符号说明**

- $N_{\text{space}}^{\text{eff}}$：按语义空间合并后，启发式活动所对应的有效语义空间数量。
- $q(i)$：语义空间 ID $i$ 获得的启发式计数占全部启发式计数的比例。
- $\mathcal{I}=\{1,\ldots,M\}$：该轨迹中观察到的不同语义空间 ID 集合，$M$ 是空间数量。
- $\exp$：指数函数；将熵转换为更直观的有效数量。
- $\log$：对数函数，用于计算分布熵。

<div class="equation-explanation" markdown="1">

**直观理解**：该式先计算启发式活动分布的熵，再取其指数。若活动几乎集中在一个空间，结果接近 $1$；若较均匀地分布在多个空间，结果更高，因此可把它理解为模型实际上动用了多少个重要解题视角。<br>
**原文位置**：§2.3，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 连续语义空间片段的有效数量

$$
N_{\text{trans}}^{\text{eff}}=\exp\!\left(-\sum_{k=1}^{K}p(k)\log p(k)\right)-1
$$

**符号说明**

- $N_{\text{trans}}^{\text{eff}}$：按连续语义空间片段统计后得到的有效片段数量减一，用于刻画语义空间转移结构。
- $p(k)$：第 $k$ 个最大连续语义空间片段获得的启发式计数占全部启发式计数的比例。
- $R_k$：语义空间序列中第 $k$ 个最大连续片段所包含的内容单元索引集合。
- $K$：该轨迹中的连续语义空间片段总数。

<div class="equation-explanation" markdown="1">

**直观理解**：该式不把同一空间的多次访问合并，而是分别看每次连续停留。减去 $1$ 是论文定义的一部分；数值较高通常表示启发式活动分散在更多片段中，也就是推理过程中发生了更多或更明显的空间转移。<br>
**原文位置**：§2.3，公式（2）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：SHAPE 本身是分析与标注框架，不是一个独立的语言模型训练目标，因此所给章节没有定义新的 SHAPE 损失函数。启发式增强实验使用基于 Group Relative Policy Optimization（GRPO）的 Plan-GRPO 与 HA-Plan-GRPO；两者共享奖励函数、验证器、优化器和评估提示，仅改变训练 rollout 提示，HA-Plan-GRPO 在规划阶段额外提供十一种数学启发式。原文未明确报告该章节中的完整 GRPO 数学目标或具体优化公式，因此不能据此补写损失函数。研究逻辑是：用奖励信号优化模型生成可验证的数学答案，同时检验在 rollout 中显式提供启发式是否改变最终准确率。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 统一启发式分类器**

SHAPE 将数学教育研究中的策略、战术和局部操作整合为适合自动标注 CoT 的统一分类体系。标注结果为 $H_t\subseteq\mathcal{H}$ 的多标签集合；表示变化型启发式包括改变符号表示、认知再解释、引入符号表示或形式化、简化问题、类比以及验证和回顾等。

> 直观理解：该模块回答“模型在这一小段具体做了什么”。它把自然语言推理转换成数学上有含义的动作，而不是只依赖文本长度、句法形式或表面相似度。

**2. 语义空间追踪器与记忆缓冲区**

语义空间不是直接从 CoT 中显式读取，而是根据启发式动作序列推断模型当前考虑的约束、目标和可用操作。追踪器对表示变化型单元预测 $\mathrm{New}$、$\mathrm{Maintain}$ 或 $\mathrm{Return}$，并在返回时从记忆缓冲区 $\mathcal{M}$ 中确定目标空间 ID。

> 直观理解：同一种数学视角可能被暂时离开后再次使用，因此不能只统计“出现过多少种空间”。记忆缓冲区让系统区分“真正开辟新视角”和“回到旧视角”。

**3. 深度—广度分布度量**

系统由 $\mathbf{S}$ 和 $\mathbf{H}$ 构造两类分布：$q(i)$ 将启发式计数按语义空间 ID 合并，$p(k)$ 将计数按连续语义空间片段分别统计；同时计算启发式频率 $u(h)$。$N_{\mathrm{space}}^{\mathrm{eff}}$ 衡量启发式活动有效地使用了多少个空间，$N_{\mathrm{trans}}^{\mathrm{eff}}$ 则反映连续片段层面的转移程度。

> 直观理解：如果模型多次回到同一空间，空间分布会把这些访问合并，说明它仍可能围绕一个核心解释深入；片段分布则保留每次离开和返回，因此能揭示来回切换。

**训练与推理**

在纯分析流程中，训练输入是人工标注的 CoT 金标准，作用是选择可靠的自动标注模型；推理时输入一条原始 CoT，标注模型依次完成内容单元切分、启发式多标签预测和语义空间追踪，输出对齐的 $\mathbf{S}$ 与 $\mathbf{H}$，再计算分布和有效数量。后训练效果分析收集四个模型在 MATH-Perturb 原题、保持解法的简单扰动题和改变解法的困难扰动题上的 CoT，并比较其 SHAPE 结构变化。启发式增强训练则以 Qwen3-1.7B-Base 为基础，在 MATH 训练集上分别训练 Plan-GRPO 和 HA-Plan-GRPO，随后在 MATH-Perturb 测试集上用相同评估设置比较。

**复现信息**

可复现所必需的核心设置包括：金标准含 $48$ 条轨迹、$1{,}598$ 个内容单元和 $8{,}334$ 个句子；主要自动标注器默认是 Qwen3.5-27B，另以 Grok-4.1-Fast 进行模型选择和部分分析；语义空间追踪仅对包含表示变化型启发式的单元显式预测 $\mathrm{New}$、$\mathrm{Maintain}$ 或 $\mathrm{Return}$，其余单元沿用当前空间。后训练策略分布的 Density/Coverage 使用 $k=3$ 个近邻和余弦距离，且仅统计两模型都正确的问题上的成功轨迹；HA-Plan-GRPO 与 Plan-GRPO 只在 rollout 提示上不同。完整提示、算法和训练细节位于论文附录 D 与附录 F，所给章节未提供更多可直接复现的优化超参数。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Omni-MATH 的 100 题子集：沿用 ThinkARM 的实验子集，包含 15 个模型生成的思维链轨迹。它用于两项诊断实验：以轨迹特征预测最终答案正确性，以及比较正确、错误轨迹的有效语义空间数、有效转移数和转移比。
- MATH-Perturb 的 115 题测试集：每个原始题均来自 level-5 MATH，并配有简单扰动和困难扰动。简单扰动保留解法与结构，困难扰动以最小文字变化改变所需解法，因此该数据用于区分模型是在复用原策略，还是能根据数学要求重组推理。
- MATH-Perturb 上的共同成功轨迹与 GRPO 评测轨迹：前者对每道双方均答对的题最多汇总五条成功轨迹，用于比较基础模型和后训练模型的启发式分布；后者用于初步评估 Qwen3-1.7B-Base、Plan-GRPO 与 HA-Plan-GRPO 在原始、简单和困难题上的生成质量与多次采样成功率。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**AUROC**

衡量逻辑回归依据轨迹特征区分正确与错误答案的排序能力；$0.5$ 近似随机，越接近 $1$ 区分能力越强。实验使用分层五折外层交叉验证，并在内层五折中选择 $\ell_1$ 或 $\ell_2$ 正则化及其超参数。 （越高越好，因为更高值表示相应轨迹表征携带更稳定的答案正确性信号。）

</div>
<div class="metric-item" markdown="1">

**Pass@1、Avg@64 与 Pass@64**

Pass@1 检验单次生成能否答对，用于观察扰动造成的直接性能变化；Avg@64 表示多次采样下的平均正确表现，Pass@64 表示 64 次采样中至少出现一次正确解的能力。两类指标分别反映典型生成质量与策略支持范围。 （均为越高越好；但 Pass@64 较高不代表单次输出稳定，因为它只要求多次尝试中至少成功一次。）

</div>
<div class="metric-item" markdown="1">

**SHAPE 分布与语义空间指标**

启发式频率分布的 Jensen–Shannon 散度 $D_{JS}^{\mathrm{freq}}$ 衡量原题与扰动题所用数学动作的变化；有效语义空间数 $N_{\mathrm{space}}^{\mathrm{eff}}$ 衡量推理集中于多少种数学解释；转移比 $\rho=N_{\mathrm{trans}}^{\mathrm{eff}}/N_{\mathrm{space}}^{\mathrm{eff}}$ 衡量每个语义空间上的平均切换强度。后训练分析另以 Density 衡量轨迹是否集中于基础分布的高密度核心，以 Coverage 衡量基础模型策略区域被覆盖的比例。 （这些诊断量没有统一的单调优劣：较大的 $D_{JS}^{\mathrm{freq}}$ 或 $N_{\mathrm{space}}^{\mathrm{eff}}$ 可表示适应性增强，也可能表示无效搜索；较大的 $\rho$ 可能意味着反复切换而未取得进展。对于后训练分布，Density 高于 $1$ 且 Coverage 较低共同指向模式寻优和策略收缩，而非更优本身。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Omni-MATH 100 题、15 个模型轨迹上的答案正确性预测

<div class="result-value" markdown="1">

SHAPE 的 11 类启发式频率达到 AUROC $0.653\pm0.02$；加入非启发式类别后达到最高的 $0.664\pm0.02$。相比之下，长度为 $0.504\pm0.03$，长度加推理词元特征为 $0.503\pm0.03$，自我修正和 ThinkARM 均约为 $0.618$。

</div>

作者据此主张：模型采取了哪些数学动作，比轨迹有多长、出现多少“思考”词元或处于何种一般推理阶段，更能解释最终是否答对。分析上，这验证了 SHAPE 作为诊断表征的增量价值，但 AUROC 仍远低于完美预测，而且观察性分类不能证明某一启发式会因果地提升正确率。

<div class="result-source" markdown="1">

来源：第 3.1 节 Results，表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Notably, SHAPE frequency features achieve the best AUROC (0.664 ± 0.02), outperforming all baselines.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### MATH-Perturb 原题、简单扰动与改变必要解法的困难扰动

<div class="result-value" markdown="1">

四个模型在困难扰动下的 Pass@1 均明显下降，例如 Qwen3-8B 从原题 $0.96$ 降至 $0.84$，Qwen3-32B 从 $0.92$ 降至 $0.76$，Nemotron-Cascade-8B 从 $0.92$ 降至 $0.71$，Olmo-3-7B-Think-RLVR 从 $0.97$ 降至 $0.76$。同时，困难扰动相较简单扰动产生更大的启发式分布变化、更多有效语义空间和更高转移比，且表中相应比较达到单侧配对检验的 $p<.05$。

</div>

作者的结论不是模型机械复制了原解，而是模型识别到问题结构已变并改变了局部数学动作与全局语义遍历；问题在于这种适应表现为开辟更多解释后反复切换，未能收敛到正确方案。该实验支持“适应但失败”，却不能单凭这些聚合指标确定每次切换的具体错误原因。

<div class="result-source" markdown="1">

来源：第 4.1 节 Results，表 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 3 shows substantial Pass@1 drops under hard perturbation across all four models.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 基础模型与 RL/GRPO 后训练模型在成功轨迹启发式频率空间中的分布比较

<div class="result-value" markdown="1">

三个基础—后训练配对的 Density 均高于 $1$：Qwen3-1.7B-GRPO 为 $1.220$，Olmo-3-7B-Think-RL-Zero 为 $1.250$，Olmo-3-7B-Think-RLVR 为 $1.032$；对应 Coverage 分别为 $0.871$、$0.707$、$0.531$。无关模型对照仅有 Density $0.520$、Coverage $0.437$。

</div>

作者将“Density 高于 $1$ 且 Coverage 低于 $1$”解释为后训练把成功轨迹集中到基础模型原本已有的高密度策略核心，同时放弃部分低频启发式模式，即启发式层面的模式寻优。该结果表明策略分布收窄，但不等于后训练没有提升准确率，也不能证明被舍弃的模式一定有用；分析还仅覆盖双方都成功的轨迹。

<div class="result-source" markdown="1">

来源：第 4.2 节 Results，表 4；图 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Every post-trained model exhibits Density above 1.0, indicating concentration in the dense core of the base distribution rather than spreading widely.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 正确性预测与语义空间统计主要基于 Omni-MATH 的 100 题子集；扰动实验也只有 MATH-Perturb 的 115 题和四个后训练模型。题目规模、数学领域及模型覆盖有限，结论是否适用于更广泛难度、证明题或其他模型家族仍需验证。
- SHAPE 标签由 Grok-4.1-Fast 自动生成，而节选未报告人工标注一致性或标注误差敏感性；后训练分布分析又只保留基础模型与后训练模型都成功的轨迹。因此，启发式类别噪声和成功样本选择都可能影响 Density、Coverage 及语义空间结论。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 表层思维链特征：包括 CoT 长度、推理词元数量与比例，以及由“wait”“aha”“verify”等词汇标记构造的自我修正次数、比例和是否出现。该组对照检验性能是否仅来自轨迹长度或可见的反思措辞。
- ThinkARM：以 Read、Analyze、Plan、Implement、Explore、Verify、Answer、Monitor 八类阶段标签的词元比例表示思维链。它是比长度特征更具结构性的基线，用于判断数学启发式标签是否比一般推理阶段标签包含更多正确性信息。
- 简单扰动与困难扰动对照：两者均尽量保持题面接近原题，但只有困难扰动改变必要解法。该控制比较可将一般措辞变化与真正要求策略切换的变化区分开。
- 基础模型及跨模型分布对照：Olmo-3-7B、Qwen3-1.7B-Base 分别作为对应后训练模型的参考分布；Olmo-3-7B 对 Qwen3-1.7B-Base 的无关模型配对用于判断高密度、部分覆盖是否只是任意两个模型之间都会出现的现象。

**实验想回答的问题**

- 与长度、推理词元比例、自我修正标记和阶段标签等传统思维链表征相比，SHAPE 的数学启发式特征能否更有效地预测答案正确性；其语义空间指标能否揭示正确与错误轨迹在推理组织方式上的差异？
- 当题目仅作轻微文字改动但所需解法发生变化时，模型是否会真正调整启发式与语义解释；强化学习后训练是否会压缩启发式策略空间，以及显式鼓励启发式规划能否改善数学推理表现？

**实验实现**

正确性预测以每条 CoT 的特征向量为输入、最终答案是否正确为标签，训练带 $\ell_1$ 或 $\ell_2$ 正则的逻辑回归；正则类型和超参数由内层五折 AUROC 选择，结果以分层五折交叉验证报告。扰动实验从 Qwen3-8B、Qwen3-32B、Nemotron-Cascade-8B 和 Olmo-3-7B-Think-RLVR 收集原题、简单扰动题和困难扰动题轨迹，并由 Grok-4.1-Fast 执行 SHAPE 标注；困难与简单扰动的差异以单侧配对 Wilcoxon 符号秩检验判断，$p<.05$ 标星。后训练分布比较在启发式频率向量 $\nu(h)$ 上使用余弦距离和 $k=3$ 近邻计算 Density、Coverage，仅保留基础模型与后训练模型都答对的问题。GRPO 训练使用两张 NVIDIA B200；Plan-GRPO要求先列目标与子目标，HA-Plan-GRPO进一步在每个主要步骤选择并解释一种数学启发式。原文节选未给出训练集规模、训练步数及全部超参数。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| SHAPE 特征中仅使用 11 类启发式 $H$，与加入非启发式类别 $N$ 的 $H+N$ 对照 | AUROC 从仅用 $H$ 的 $0.653\pm0.02$ 提升到 $H+N$ 的 $0.664\pm0.02$，特征数从 11 增至 12。 | 该对照隔离了“未执行明确数学启发式”的内容比例是否有额外信息。小幅提升说明非启发式内容也与成败相关，但主要预测力仍来自启发式分布；原文未报告该差异的显著性检验，因此不能断言增益稳定显著。 | 表 1<br><span class="experiment-evidence">SHAPE (H+N) 0.664 ± 0.02 12</span> |
| Qwen3-1.7B 上基础模型、仅增加规划格式的 Plan-GRPO、以及加入 11 类数学启发式的 HA-Plan-GRPO | 在原题、简单扰动和困难扰动上，HA-Plan-GRPO 的 Avg@64 分别为 $36.80$、$35.80$、$17.72$，均高于 Plan-GRPO 的 $30.00$、$29.86$、$14.52$ 和基础模型的 $23.54$、$23.10$、$11.84$。其 Pass@64 分别为 $80.00$、$79.13$、$62.61$；相较 Plan-GRPO 的 $80.00$、$78.26$、$61.74$，提升较小。 | Plan-GRPO 控制了“仅要求先规划”带来的收益，因此额外差异更接近启发式信息与启发式引导 rollout 的贡献。Avg@64 的一致提升表明典型采样质量改善，而 Pass@64 只小幅变化，意味着方法更可能重分配正确解的生成概率，而非大幅扩展模型能解决的问题集合。该表被作者标为初步结果，且原文未报告方差或显著性。 | 表 5<br><span class="experiment-evidence">+ HA-Plan-GRPO (ours) 36.80 80.00 35.80 79.13 17.72 62.61</span> |

**定性案例**

- 图 3 将 Olmo-3-7B-Base 与 Olmo-3-7B-Think-RLVR 的成功轨迹投影到启发式频率空间的第一主成分。后训练模型集中在基础分布峰值附近，同时未覆盖左侧尾部；这一可视化与表 4 的高 Density、较低 Coverage 相互印证，直观展示了“强化已有主导策略而舍弃部分少见策略”的模式。不过，一维主成分投影会压缩高维结构，不能单独作为分布收缩的充分证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文系统分析数学思维链中的语义空间和启发式，并通过多样化推理启发式改进数学推理能力。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`eb017fd596c1a1f07dbd59db7690aae331a0adea43676e3cf54e0277c6e5712f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
