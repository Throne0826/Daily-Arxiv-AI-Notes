---
title: "[论文解读] Trace as State: Reasoning Traces as Conditional States for Long-Context Transformers"
description: "[arXiv 2609.02702][LLM Reasoning] 本文研究如何把首轮生成的推理轨迹作为任务状态，在新一轮因果处理开始前置于长上下文之前，使模型能够带着已发现的目标、搜索线索或排除信息重新阅读上下文。"
arxiv_id: "2609.02702"
announcement_date: "2026-09-03"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-03T04:31:58.299913+00:00"
source_sha256: "df75f50bf50b81fa89480d77c5982436e0bb720ec9836812cfb5254c5731062b"
tags:
  - "LLM Reasoning"
  - "长上下文推理"
  - "因果注意力"
  - "推理轨迹"
  - "文本状态"
  - "重新读取"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.02702</p>

# Trace as State: Reasoning Traces as Conditional States for Long-Context Transformers

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-03</span>
<span><strong>作者</strong> Xu Zou, Jie Tang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Tsinghua University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.02702v1) · [PDF 下载](https://arxiv.org/pdf/2609.02702v1) · **关键词** 长上下文推理, 因果注意力, 推理轨迹, 文本状态, 重新读取<br>


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

本文研究如何把首轮生成的推理轨迹作为任务状态，在新一轮因果处理开始前置于长上下文之前，使模型能够带着已发现的目标、搜索线索或排除信息重新阅读上下文。

**不用术语来说**：长上下文模型虽然能读入大量文本，但只能从前向后处理：如果模型直到文本后部或首轮推理结束时才弄清楚“应该找什么”，这个新认识就无法反过来影响前面内容在同一轮中的处理。模型可能因此读过了关键信息，却没有按照后来形成的目标来组织和利用它。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出“条件状态更新任务”抽象，并给出定性理论依据：对于单遍读取的确定性因果处理器，若条件先于信息序列给出，只需持续维护实际条件对应的状态；若条件最后才出现，最坏情况下可能需要保存该序列对所有潜在条件的作用，二者可产生指数级工作内存差距。
- 作者提出 Trace as State：收集模型首轮生成的一条或多条推理轨迹，将其序列化为文本状态代理 $T$，并在新一轮推理中放到原长上下文之前；同时设计 Trace Append 作为严格位置对照，以区分“拥有相同轨迹文本”的收益与“轨迹在重读上下文前已经可用”的收益。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于长上下文语言模型与因果推理的交叉领域。长上下文模型能够接收数十万乃至百万级词元，但标准自回归 Transformer 仍采用因果注意力：某个位置的表示只能利用该位置及其之前的内容，后文信息无法回溯并修改已经形成的前文表示。因此，模型虽然可以在后文生成答案时看到先前内容，却可能在读取长上下文早期部分时尚不知道后来才确定的目标、搜索状态或候选假设。本文关注的核心背景是：如何在不改变单次传递中的因果结构前提下，让后续获得的任务相关状态影响下一次对长上下文的读取。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**因果注意力**

在自回归 Transformer 中，位置 $i$ 的表示只能关注位置 $i$ 及其前缀，不能直接使用后面的词元。这样保证了逐词生成的因果性，但也使后文发现的信息无法回溯影响前文表示。

</div>
<div class="concept-item" markdown="1">

**长上下文推理**

长上下文推理是指模型需要在很长的输入中定位证据，并对分散的信息执行组合、搜索或多步判断。难点不只是把文本放进窗口，还包括模型能否在读取不同位置时维持正确的任务状态并整合证据。

</div>
<div class="concept-item" markdown="1">

**条件状态更新任务**

这类抽象任务从一个由条件确定的初始状态开始，再依次读取信息序列并更新状态。若条件先给出，处理器只需维护当前真实状态；若条件后给出，则可能需要保留该序列对许多潜在条件的作用，因而需要更多工作记忆。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文把长上下文推理抽象为一个因果状态处理问题：输入包含一个长信息序列，以及可能在序列之前或之后出现的任务条件；处理器逐步读取输入并维护一个运行状态，最终输出任务答案。关键比较不是改变信息内容，而是改变任务相关状态相对于长上下文的出现顺序。条件先出现时，处理器可在读取每个项目时直接更新已确定的状态；条件后出现时，早先的读取阶段尚不知道应当保留哪一种状态轨迹。论文进一步把模型在第一次推理中生成的文本推理轨迹视为任务状态的可观察代理，并研究将其放在第二次长上下文读取之前是否能改善答案。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$T$**

收集并序列化的推理轨迹文本；它不是隐状态，而是模型第一次推理后生成、可在下一次输入中显式提供的文本状态代理。

</div>
<div class="notation-item" markdown="1">

**$x_{1:n}$**

长度为 $n$ 的长上下文信息序列，表示模型需要重新读取和处理的输入内容。

</div>
<div class="notation-item" markdown="1">

**$s$**

因果处理器在读取输入过程中的运行状态，例如当前目标、搜索前沿或已排除的假设集合。

</div>
<div class="notation-item" markdown="1">

**$y$**

模型针对给定长上下文和任务条件生成的最终答案或评测输出。

</div>

</div>

**直接相关的工作**

- **Ok and Lee (2026)**: 该工作说明因果注意力会造成提示中选项顺序导致的性能差异，并发现将选项在上下文之后重复可以部分缩小差距。它与本文共同揭示了输入顺序对因果模型推理的影响，但本文进一步把顺序问题解释为任务状态何时可用，并将第一次生成的推理轨迹放到第二次读取长上下文之前。
- **Re2（Xu et al., 2024）**: Re2 通过在同一提示中重复问题提供直接的重新阅读基线，说明重复任务信息可能有助于推理。本文的区别在于重复的不是固定问题文本，而是第一次推理后收集的、可能包含中间计算信息的文本状态，并专门比较其位于长上下文之前或之后的效果。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在图搜索、多目标信息检索等长上下文任务中，模型需要维护活动目标、搜索前沿或已排除假设等任务状态。然而，这些状态往往只有在读到后文或完成部分推理后才会形成。受因果注意力约束，后形成的状态只能影响后续推理和答案生成，不能修改同一遍处理中较早位置已经形成的表示，因此名义上更长的上下文窗口并不自动解决信息利用顺序不匹配的问题。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **扩大长上下文处理能力的模型架构**：稀疏、压缩或混合序列建模等架构扩大模型可接收的上下文长度，使模型能够在一次调用中处理数十万乃至更多词元；但其自回归 Transformer 通常仍采用因果注意力，位置较后的信息不能回流到较早位置。
- **推理轨迹与轨迹后置复用**：推理模型在给出可见答案前生成文本化的中间推理，这些轨迹能够携带部分计算结果。轨迹可以用于后续推理；本文特别以 Trace Append 表示一种位置控制：第二轮仍提供相同的轨迹文本，但把它放在长上下文之后，使其只能指导之后的推理与答案生成。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单纯扩大上下文窗口解决的是“能否读入”，而非“何时获得任务状态”。当关键条件出现得较晚时，单遍因果处理器无法用该条件重新解释先前内容；在作者构造的条件状态更新问题中，条件后置最坏可能要求记住信息序列对大量潜在条件的不同作用，从而带来指数级内存需求。
- 仅在上下文之后附加推理轨迹虽然让答案阶段获得了中间信息，却不能让轨迹影响此前长上下文表示的形成。因此，它无法判断收益究竟来自通用的推理脚手架，还是来自在重读期间提前提供任务状态；此外，轨迹本身可能不完整或包含错误，不能被等同于真实、无误的内部状态。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作已表明信息的相对呈现顺序会影响推理，也表明生成式推理文本能够承载中间计算，但尚缺少一种保持每一轮内部仍为标准因果处理、同时把上一轮晚发现的任务状态前移到下一轮上下文处理之前的通用推理方案；也缺少使用完全相同轨迹、仅改变放置位置的对照来验证“状态先于上下文”是否是关键因素。

</div>
<div markdown="1"><span>核心问题</span>

对于长上下文因果 Transformer，把首轮推理轨迹作为任务状态代理并置于第二轮长上下文之前，是否会比将同一轨迹置于上下文之后更有效；这种位置优势能否由条件状态更新中的先条件、后条件内存差异来解释？

</div>
<div markdown="1"><span>作者直觉</span>

可以把首轮推理看成一次侦察：模型读完后才知道真正的目标、可疑路径和已排除选项。Trace as State 不要求改变 Transformer 的因果结构，而是把侦察笔记 $T$ 放到新一轮输入最前面，让模型带着这些线索重新阅读。这样，处理每一段上下文时都能围绕当前已知目标更新一个实际状态，而不必在条件尚不明确时同时保留许多可能解释；相比之下，把笔记放在上下文末尾，只能帮助最后作答，不能指导重读过程中的信息筛选与表示形成。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法先用“条件状态更新任务”解释长上下文推理中的顺序问题：因果处理器只能按输入顺序读取信息；若决定如何解释上下文的条件在上下文之后才出现，处理器可能需要同时保留大量候选状态路径。最坏情况下，状态空间大小为 $|\mathcal{S}|=2^b$ 时，条件后置需要约 $b2^b$ 比特，而条件前置只需约 $b$ 比特。作者据此提出一个顺序原则：指导信息处理的任务状态，应尽可能在被指导的信息之前提供。

实际任务中并不存在可直接读取的精确状态 $z$，因此方法先让同一个因果模型对长上下文 $x$ 推理若干次，收集推理轨迹 $r_1,\ldots,r_{n_{\mathrm{tr}}}$，再用固定序列化器 $\pi$ 将其组成文本状态代理 $T$。随后开启一次全新的因果前向过程，将输入排列为 $[T,x]$，让模型带着先前发现的目标、指代关系或搜索进度重新阅读上下文并生成答案；匹配对照 Trace Append 则输入 $[x,T]$。两者使用完全相同的模型、上下文和轨迹文本，仅改变 $T$ 的位置，因而可直接检验“状态是否在重读上下文时已经可用”这一设计因素。通俗地说，Trace as State 类似于先把第一次解题得到的草稿放在题目前，再从头读题；Trace Append 则是在读完整道题后才看到同一份草稿。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始长上下文推理与轨迹采集

独立运行模型 $n_{\mathrm{tr}}$ 次；第 $j$ 次运行从条件分布 $\mathcal{M}(\cdot\mid x)$ 中产生推理轨迹 $r_j$ 和单独的可见答案 $a_j$。该阶段使用轨迹作为后续状态信息来源，而不是直接将首轮答案视为最终输出。

<div class="method-step__io" markdown="1">

**输入**：同一长上下文问题 $x$、因果推理模型 $\mathcal{M}$，以及预设运行次数 $n_{\mathrm{tr}}$。<br>
**输出**：轨迹集合 $(r_1,\ldots,r_{n_{\mathrm{tr}}})$，以及对应的初始可见答案 $(a_1,\ldots,a_{n_{\mathrm{tr}}})$。

</div>

**直观理解**：模型先尝试解题并留下若干份“思考草稿”；这些草稿可能记录当前目标、已经消解的指代或搜索到的位置。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造文本状态代理

计算 $T=\pi(r_1,\ldots,r_{n_{\mathrm{tr}}})$；序列化器保留被纳入轨迹的原始顺序，并添加固定标签和分隔符。在不同放置条件之间使用完全相同的 $\pi$ 和 $T$。

<div class="method-step__io" markdown="1">

**输入**：采集到的推理轨迹 $r_1,\ldots,r_{n_{\mathrm{tr}}}$ 与任务对应的固定序列化器 $\pi$。<br>
**输出**：序列化文本 $T$，即对任务状态的可观察文本代理。

</div>

**直观理解**：这一步把多份草稿整理成统一格式的备忘录；它不保证正确或完整，也不等同于模型隐藏层中的真实内部状态。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### Trace as State 条件前置重读

启动一次新的因果前向过程，以 $[T,x]$ 为输入，再生成推理轨迹 $r'_{\mathrm{Tas}}$ 和可见答案 $a'_{\mathrm{Tas}}$。由于 $T$ 位于前方，模型处理每个上下文位置时都可因果地利用其中的状态线索。

<div class="method-step__io" markdown="1">

**输入**：文本状态代理 $T$、原始长上下文 $x$ 和同一模型 $\mathcal{M}$。<br>
**输出**：Trace as State 的新推理轨迹 $r'_{\mathrm{Tas}}$ 与最终可见答案 $a'_{\mathrm{Tas}}$。

</div>

**直观理解**：模型先查看第一次解题留下的备忘录，再从头阅读材料，因此可用已经发现的线索选择重点、解释指代或延续搜索。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### Trace Append 匹配对照

在新的因果前向过程中改用 $[x,T]$，生成 $r'_{\mathrm{Tap}}$ 和 $a'_{\mathrm{Tap}}$。该设置允许 $T$ 影响后续推理与答案，但不能回溯改变模型先前处理上下文词元时形成的表示。

<div class="method-step__io" markdown="1">

**输入**：与 Trace as State 完全相同的 $T$、$x$ 和模型 $\mathcal{M}$。<br>
**输出**：Trace Append 的新推理轨迹 $r'_{\mathrm{Tap}}$ 与可见答案 $a'_{\mathrm{Tap}}$，用于和前置结果比较。

</div>

**直观理解**：这相当于读完材料后才拿到备忘录：它仍可帮助作答，却无法指导刚才那一遍阅读。因为两组输入仅顺序不同，该对照隔离了“轨迹前置”本身的作用。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 因果状态递推与顺序相关的最坏情况内存

$$
\begin{aligned}
s_i &= U(s_{i-1},c_i),\qquad i=1,\ldots,n,\\
s_0 &= z,\qquad b=\log_2|\mathcal{S}|,\\
M_{[z,C]} &\le \lceil b\rceil,\\
M_{[C,z]} &\ge \left\lceil\log_2|\mathcal{S}|^{|\mathcal{S}|}\right\rceil
=\left\lceil|\mathcal{S}|\log_2|\mathcal{S}|\right\rceil
=\lceil b2^b\rceil\quad\text{(worst case)}.
\end{aligned}
$$

**符号说明**

- $C=(c_1,\ldots,c_n)$：由 $n$ 个信息单元组成的有序输入序列。
- $c_i$：序列中的第 $i$ 个信息单元。
- $s_i$：处理完 $c_1$ 至 $c_i$ 后的任务状态。
- $U$：根据当前状态与新信息单元产生下一状态的固定更新规则。
- $\mathcal{S}$：有限任务状态空间。
- $z$：任务条件，同时作为初始任务状态 $s_0$。
- $b=\log_2|\mathcal{S}|$：表示一个状态所需的信息量尺度。
- $M_{[z,C]}$：先输入条件、后输入信息序列时所需的工作内存。
- $M_{[C,z]}$：先输入信息序列、最后才输入条件时所需的工作内存。

<div class="equation-explanation" markdown="1">

**直观理解**：递推式表示处理器每次只能依据已有状态和当前输入向前更新。条件先到时，处理器知道要沿哪条状态路径计算，只需保存当前状态；条件后到时，为保证能响应任意 $z$，最坏情况下必须区分从每个可能初态到终态的完整函数，共有 $|\mathcal{S}|^{|\mathcal{S}|}$ 种，因此内存下界从约 $b$ 增至约 $b2^b$ 比特。该结论是最坏情况理论动机，并不声称真实 Transformer 在所有任务上都会达到此下界。<br>
**原文位置**：第3.1节，公式(1)与公式(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 轨迹采集、序列化与两种放置条件

$$
\begin{aligned}
(r_j,a_j)&\sim\mathcal{M}(\cdot\mid x),\qquad j=1,\ldots,n_{\mathrm{tr}},\\
T&=\pi(r_1,\ldots,r_{n_{\mathrm{tr}}}),\\
(r'_{\mathrm{Tap}},a'_{\mathrm{Tap}})&\sim\mathcal{M}(\cdot\mid[x,T]),\\
(r'_{\mathrm{Tas}},a'_{\mathrm{Tas}})&\sim\mathcal{M}(\cdot\mid[T,x]).
\end{aligned}
$$

**符号说明**

- $\mathcal{M}$：执行初始推理和后续重读的因果推理模型。
- $x$：包含问题在内的长上下文输入。
- $n_{\mathrm{tr}}$：用于收集推理轨迹的源模型运行次数。
- $r_j$：第 $j$ 次初始运行产生的推理轨迹。
- $a_j$：第 $j$ 次初始运行产生的独立可见答案。
- $\pi$：跨放置条件保持固定的轨迹序列化器。
- $T$：由多个推理轨迹组成的序列化文本状态代理。
- $r'_{\mathrm{Tap}},a'_{\mathrm{Tap}}$：输入顺序为 $[x,T]$ 时，新一轮产生的轨迹和可见答案。
- $r'_{\mathrm{Tas}},a'_{\mathrm{Tas}}$：输入顺序为 $[T,x]$ 时，新一轮产生的轨迹和可见答案。

<div class="equation-explanation" markdown="1">

**直观理解**：模型先从原始上下文中产生轨迹，再把轨迹整理成同一份 $T$。实验方法只交换 $T$ 与 $x$ 的顺序：Trace Append 在读完上下文后提供轨迹，Trace as State 则先提供轨迹再让模型重读上下文，因此两者的差异可归因于状态代理何时进入因果计算。<br>
**原文位置**：第3.2节公式(3)、公式(4)，第3.3节公式(5)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。原文方法未提出新的训练损失、参数优化过程或模型微调；它是推理时的多次调用与提示顺序重排方法。初始运行负责生成文本状态代理，新的前向过程负责在 $[T,x]$ 条件下重新推理，最终比较的是生成答案而非某个新增训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 条件状态更新模型**

处理器维护有限状态空间 $\mathcal{S}$ 中的任务状态 $s_i$，并按输入顺序用固定规则 $U$ 更新。条件 $z\in\mathcal{S}$ 决定初始状态 $s_0=z$；比较 $[z,C]$ 与 $[C,z]$ 可得到最坏情况下的顺序相关内存差异。

> 直观理解：该模块不是一个新增神经网络层，而是解释方法的理论抽象：先知道任务条件时只需沿一条路径处理信息，最后才知道条件时则可能必须为许多候选路径保留结果。

**2. 推理轨迹序列化器**

固定映射 $\pi$ 将一个或多个推理轨迹按来源顺序组成 $T$，并添加固定标签与分隔符。作者将 $T$ 定义为任务状态的文本代理，而非精确条件 $z$ 或模型的特权内部状态。

> 直观理解：它负责把非结构化思考过程整理成模型可再次读取的文本，同时保证前置与后置实验使用的是同一份内容，避免把内容差异误认为顺序效果。

**3. 状态前置的新因果前向过程**

Trace as State 在新一轮推理中输入 $[T,x]$；匹配控制 Trace Append 输入 $[x,T]$。二者不修改因果 Transformer 的注意力方向，而是通过重新排列已有文本，使状态代理在上下文重处理期间可用。

> 直观理解：方法的核心不是让模型向后看，也不是更新参数，而是让模型带着先前形成的提示重新读一遍上下文，从输入顺序上绕开“关键信息发现得太晚”的问题。

**训练与推理**

整个流程发生在推理阶段。首先对同一输入 $x$ 调用模型 $n_{\mathrm{tr}}$ 次，分别保留推理轨迹 $r_j$ 与可见答案 $a_j$；随后用固定序列化器 $\pi$ 合并轨迹得到 $T$。最后必须开启新的因果前向过程：主方法输入 $[T,x]$ 并输出 $a'_{\mathrm{Tas}}$，对照方法输入 $[x,T]$ 并输出 $a'_{\mathrm{Tap}}$。这里的“fresh pass”很关键，因为主方法需要模型在已经看到 $T$ 的条件下重新处理整个 $x$，而不是简单延续初始生成或仅在末尾追加文本。原文节选未说明额外训练，也未说明利用首轮答案投票或选择最终答案。

**复现信息**

公平解释结果所需的关键控制有三点：第一，Trace as State 与 Trace Append 使用同一个长上下文 $x$ 和完全相同的序列化轨迹 $T$，唯一实验变量是二者的排列顺序；第二，序列化器 $\pi$ 在两种放置条件间固定，保留所含推理文本的来源顺序，并只增加固定标签和分隔符；第三，轨迹只是可能不完整、有损或错误的文本代理，不能解释为精确形式条件 $z$ 或模型内部隐藏状态。所给方法章节未明确报告采样温度、解码策略、具体 $n_{\mathrm{tr}}$、轨迹截断规则、提示模板全文或上下文超限处理方式，复现时仍需回查论文其他章节或代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GraphWalks：要求模型在长边列表中维护图状态并完成图遍历推理；实验使用最长且不超过模型输入上限的 $256K$ bin，用于测试长上下文中的状态累积与检索。
- MRCRv2 8-needle：要求模型把最终请求绑定到此前正确的请求—响应实例；实验使用 $256K$ 和 $512K$ bins，用于测试长文本中的多项信息定位与绑定。由于不同模型的分词器不同，原文指出若干 $1M$ bin 问题无法公平测试。
- NUB-1M：包含约 $400$K–$700$K token 新小说的长篇阅读理解基准；使用 season 2，报告 $20$ 个问题在 $5$ 次重复实验上的平均准确率，用于测试对超长连续文本的理解。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Exact match**

预测答案必须与标准答案完全匹配，适合衡量离散答案任务中的最终正确率。 （越高越好；更高表示模型给出完全正确答案的比例更大。）

</div>
<div class="metric-item" markdown="1">

**Accuracy**

题目层面的答对比例；NUB-1M 报告的是 $20$ 个问题在 $5$ 次重复上的平均准确率。 （越高越好；更高表示整体阅读理解或推理判断更可靠。）

</div>
<div class="metric-item" markdown="1">

**Reported task metric**

各数据集原有的任务评测指标；所给实验摘录没有逐一列出 MRCRv2 和全部任务的具体指标名称。 （原文摘录未明确说明所有指标的方向；通常应依据数据集定义判断，且不能仅凭摘要补充未报告的指标。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三模型、三数据集及全部报告的模型—任务—指标组合

<div class="result-value" markdown="1">

Trace as State 在 $27$ 个报告组合中的 $26$ 个超过 Trace Append。

</div>

这说明轨迹放在长上下文之前具有很强的跨模型和跨任务稳定性，且优势不能简单归因于使用了更多 token 或使用了第二遍推理，因为 Trace Append 共享相同的轨迹代理和大体流程。但该结果并不证明每一个任务、每一个指标或任意轨迹质量下都必然有效；摘要明确保留了至少一个未胜出的组合。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across three models and three long-context datasets, Trace as State outperforms Trace Append in 26 of 27 reported combinations of model, task, and metric.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### GraphWalks Parents，DeepSeek V4 Pro Preview，exact match

<div class="result-value" markdown="1">

初始单次通过率为 $29.2\%$，Trace Append 为 $43.0\%$，Trace as State 提升至 $81.8\%$。

</div>

在该图状态维护任务中，先读出的轨迹若位于上下文之前，模型重新阅读边列表时更可能按照已有状态线索进行检索和推理。相较单次基线，Trace as State 的提升显示两遍处理有帮助；相较 Trace Append 的进一步提升则更直接支持“前置位置”而非仅仅“增加轨迹”的解释。但这是一个模型—任务组合，不能单独代表所有设置。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On GraphWalks Parents, exact match lifts DeepSeek V4 Pro Preview from 29.2% on the initial pass and 43.0% with Trace Appendto 81.8% with Trace as State,

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### GraphWalks Parents，GLM-5.2，exact match

<div class="result-value" markdown="1">

初始单次通过率为 $66.4\%$，Trace Append 为 $83.2\%$，Trace as State 达到 $100.0\%$。

</div>

GLM-5.2 在该设置下已经具有较高的初始性能，但前置轨迹仍消除了剩余错误，达到全部题目正确。结果表明方法不只对低基线模型有效；不过满分只说明该特定数据集和实验样本上的 exact match，不等于模型获得了普遍可靠的长上下文推理能力。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

and from 66.4% and 83.2% to 100.0% for GLM-5.2.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 证据摘录没有提供完整结果表、各数据集逐项分数、置信区间或统计显著性；因此 $26/27$ 的汇总不能替代对效应大小和方差的核查。
- 实验依赖三个能够暴露并重新输入自身推理轨迹的前沿模型、固定文本序列化器以及最多前 $50{,}000$ 个字符的轨迹截断；原文未明确报告在不暴露轨迹的模型、不同序列化器、不同截断长度或训练适配模型上的结果。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 单次前向基线 $\mathcal{M}([x,q])$：模型只读取长上下文 $x$ 和问题 $q$，衡量不使用额外推理轨迹时的原始能力。
- Trace as State：先在第一遍产生推理轨迹 $T$，第二遍按 $[T,x,q]$ 输入；它检验把先前得到的任务状态置于长上下文之前，是否能引导模型重新读取上下文。
- Trace Append：第二遍按 $[x,T,q]$ 输入；它使用与 Trace as State 相同的轨迹代理和两遍流程，但把轨迹放在上下文之后，因此是位置匹配控制，而非普通的无轨迹对照。

**实验想回答的问题**

- 在相同任务状态代理和模型条件下，将推理轨迹置于长上下文之前的 Trace as State，是否比置于上下文之后的 Trace Append 更能提升长上下文推理性能？
- 这种位置效应是否跨越不同模型、任务领域、上下文长度和评测指标稳定存在，而不是某一个模型或数据集的偶然现象？

**实验实现**

每个模型和任务均比较单次输入 $[x,q]$、Trace as State 输入 $[T,x,q]$ 和 Trace Append 输入 $[x,T,q]$。其中 $x$ 是长上下文，$q$ 是问题，$T$ 是模型第一遍生成并保留的推理轨迹，$\mathcal{M}$ 表示待评测模型。实验使用 Qwen 3.7 Max、DeepSeek V4 Pro Preview 和 GLM-5.2，并采用各模型可用的最高推理强度：DeepSeek V4 Pro 和 GLM-5.2 使用 max，Qwen 3.7 Max 使用官方 xhigh 系统提示。固定序列化器只加入必要分隔符，例如 <trace_start> 和 <trace_end>；过长轨迹截断到前 $50{,}000$ 个字符。为使模型集中处理问题，所有输入都把 $q$ 放在末尾。由于追加轨迹会增加输入长度，数据集选择最长但仍低于约 $1M$ token 容量的 bins。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 初始单次通过 vs. Trace Append vs. Trace as State | 在 GraphWalks Parents 的 DeepSeek V4 Pro Preview 上，三者 exact match 分别为 $29.2\%$、$43.0\%$ 和 $81.8\%$；在 GLM-5.2 上分别为 $66.4\%$、$83.2\%$ 和 $100.0\%$。 | 这不是删除某个网络模块的传统结构消融，而是逐步增加并改变轨迹的使用方式。单次通过到 Trace Append 的变化估计“第二遍加轨迹”的收益；Trace Append 到 Trace as State 的变化隔离“轨迹放在前面”的收益。由于两种 trace 条件复用了模型自身第一遍轨迹，该比较仍无法完全排除轨迹内容与第二遍输入长度的交互影响。 | Abstract<br><span class="experiment-evidence">On GraphWalks Parents, exact match lifts DeepSeek V4 Pro Preview from 29.2% on the initial pass and 43.0% with Trace Appendto 81.8% with Trace as State, and from 66.4% and 83.2% to 100.0% for GLM-5.2.</span> |
| Trace as State 与 Trace Append 的配对位置对照 | Trace as State 在 $27$ 个报告的模型—任务—指标组合中有 $26$ 个优于 Trace Append。 | 该配对对照直接检验核心设计变量，即把同类文本状态放在长上下文之前还是之后。广泛胜出支持位置效应具有普遍性，但原文摘录未报告每个组合的数值差距，因此不能据此判断优势是否在所有数据集上都同样大。 | Abstract<br><span class="experiment-evidence">Across three models and three long-context datasets, Trace as State outperforms Trace Append in 26 of 27 reported combinations of model, task, and metric.</span> |

**定性案例**

- GraphWalks Parents 的结果是一个定量案例：DeepSeek V4 Pro Preview 从单次的 $29.2\%$、Trace Append 的 $43.0\%$ 上升到 Trace as State 的 $81.8\%$，GLM-5.2 则从 $66.4\%$、$83.2\%$ 上升到 $100.0\%$。它说明前置轨迹可能帮助模型在重新扫描边列表前先形成任务相关状态；但所给摘录没有展示具体生成轨迹、错误样例或逐步推理内容，因此不能进一步断言模型内部确实执行了某种特定图算法。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过将推理轨迹作为前置条件状态来改善长上下文 Transformer 的信息整合与推理性能。; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`df75f50bf50b81fa89480d77c5982436e0bb720ec9836812cfb5254c5731062b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
