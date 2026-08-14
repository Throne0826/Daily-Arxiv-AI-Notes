---
title: "[论文解读] Thought-Aware KV Cache Compaction for Reasoning via Adaptive Attention Matching"
description: "[arXiv 2608.12331][LLM 效率] 本文提出思维感知注意力匹配（TAM），利用思维链内部不同推理步骤的重要性差异，自适应地压缩解码过程中生成词元的键值缓存。"
arxiv_id: "2608.12331"
announcement_date: "2026-08-14"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T02:54:33.312021+00:00"
source_sha256: "8aa443afd00fc6d7800c22095ef6c29595a58d225ac0384dafef4274b9b96612"
tags:
  - "LLM 效率"
  - "LLM Reasoning"
  - "推理型语言模型"
  - "链式思维"
  - "KV 缓存压缩"
  - "轨迹中途压缩"
  - "注意力匹配"
  - "结构感知预算分配"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2608.12331</p>

# Thought-Aware KV Cache Compaction for Reasoning via Adaptive Attention Matching

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Yang Liu, Bin Chong, Chongyang Zhang, Hao Zheng, Jiayu Liang, Xu Kefu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Tsinghua University；Peking University；Soochow University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12331v1) · [PDF 下载](https://arxiv.org/pdf/2608.12331v1) · **关键词** 推理型语言模型, 链式思维, KV 缓存压缩, 轨迹中途压缩, 注意力匹配, 结构感知预算分配<br>


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

本文提出思维感知注意力匹配（TAM），利用思维链内部不同推理步骤的重要性差异，自适应地压缩解码过程中生成词元的键值缓存。

**不用术语来说**：推理模型在回答复杂问题时会生成很长的中间推理过程，并保存此前每个词元的注意力状态，因此占用的显存会随推理长度持续增加。若简单地等比例删除或压缩所有历史内容，模型可能丢失题目条件、关键中间结论等仍会影响后续推理的信息；研究需要在严格的显存预算下，区分应重点保留和可大幅压缩的推理内容。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出面向生成中途压缩的TAM框架：先把推理轨迹划分为思维块，再依据各块的重要性与规模分配不同压缩预算，并保护受到较高注意力的关键词元，从而将统一压缩改为结构感知压缩。
- 为上述设计提供理论依据：作者声称自适应预算分配在凸误差模型下最优，关键词元保护能够降低近似误差，而且连续多次压缩产生的累计误差保持有界。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究推理型语言模型在自回归解码过程中的键值缓存压缩。Transformer 每生成一个新词元，都会把该词元在各注意力层产生的键和值加入 KV 缓存，使缓存规模随上下文长度 $T$ 线性增长；而链式思维推理通常包含较长的中间推导，因此显存占用会持续上升。已有工作多面向预填充阶段的长输入，或把已生成的推理轨迹视为同等重要的平坦词元序列；本文关注更具体的“轨迹中途压缩”问题，即在推理尚未结束时周期性压缩已生成词元的 KV 状态，同时尽可能保持后续注意力计算和最终推理能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**键值缓存（KV cache）**

自回归语言模型会保存历史词元对应的键向量和值向量，后续生成时直接复用，从而避免重复计算整个前缀。其代价是缓存随历史长度 $T$ 增长，长链式思维会因此形成显存瓶颈。

</div>
<div class="concept-item" markdown="1">

**缩放点积注意力与注意力质量**

注意力先用查询与各键的缩放点积计算权重，再对值向量做加权求和；某个 KV 块的“注意力质量”是该块所有未归一化指数权重之和。压缩时不仅要近似块内的加权输出，还要保持其注意力质量，否则该块与未来新增词元共同参与全局 softmax 时，其相对贡献会失真。

</div>
<div class="concept-item" markdown="1">

**注意力匹配（Attention Matching, AM）**

AM 用较短的紧凑键、紧凑值和逐位置偏置替换原 KV 缓存，并针对一组参考查询拟合原缓存的局部注意力输出及注意力质量。它把压缩转化为可闭式或标准数值方法求解的子问题，但原始设定主要针对固定上下文的一次性预填充压缩。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定推理模型在解码中已经生成的长度为 $T$ 的前缀、其逐层键矩阵 $\mathbf{K}$ 与值矩阵 $\mathbf{V}$，以及由近期查询构成的参考查询集合，任务是在推理继续进行前把原缓存替换为长度 $t$ 且 $t\ll T$ 的紧凑表示 $(\mathbf{C}_k,\bm{\beta},\mathbf{C}_v)$。紧凑缓存应在规定的内存预算内，近似原缓存对参考查询产生的局部注意力输出和注意力质量，并能与后续生成词元的 KV 状态共同参与注意力计算。本文所依据的结构假设是：链式思维可以划分为若干语义连贯的推理段，而且不同段对未来生成的重要性并不相同，因此压缩预算不应在全部词元或推理段之间均匀分配。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathbf{Q}\in\mathbb{R}^{n\times d}$**

参考查询矩阵；$n$ 是查询数量，$d$ 是每个注意力头中查询、键和值向量的维度。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{K},\mathbf{V}\in\mathbb{R}^{T\times d}$**

待压缩的原始键矩阵和值矩阵；$T$ 是当前缓存中的上下文词元数。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{C}_k,\mathbf{C}_v\in\mathbb{R}^{t\times d}$**

压缩后的键矩阵和值矩阵；$t$ 是紧凑缓存长度，通常满足 $t\ll T$。

</div>
<div class="notation-item" markdown="1">

**$\boldsymbol{\beta}\in\mathbb{R}^{t}$**

紧凑键的逐位置标量偏置，用于校准压缩后各位置的未归一化注意力权重并匹配原缓存的注意力质量。

</div>

</div>

**直接相关的工作**

- **Attention Matching（AM；Zweiger et al., 2026）**: AM 通过紧凑键值、偏置和参考查询匹配原缓存的注意力输出与注意力质量，为本文采用的潜在空间压缩原语提供基础；但其面向固定上下文的预填充场景，并对整个上下文统一压缩，未利用推理步骤之间的重要性差异。
- **Reasoning Path Compression（RPC；Song et al., 2025）**: RPC 与本文同样处理解码过程中的周期性轨迹压缩，并使用近期查询形成选择器窗口；区别在于 RPC 直接驱逐词元且使用统一保留规则，而本文拟在推理段之间自适应分配预算，并通过注意力匹配构造紧凑表示。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

推理语言模型会在解码阶段生成较长的思维链，键值缓存必须保存所有历史词元的注意力状态，其显存占用随序列长度线性增长。这不仅提高峰值显存，还会降低解码吞吐量，使长程推理难以部署在资源受限设备上；因此，需求重点是压缩已经生成的推理轨迹，而不只是压缩推理开始前的输入提示。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **注意力匹配（Attention Matching，AM）**：AM通过闭式优化构造数量更少的键和值，使压缩后的注意力输出及注意力质量尽量接近原缓存；它使用固定上下文上的自学习查询作为匹配参照，适合进行幅度较大的一次性压缩。
- **推理路径压缩（Reasoning Path Compression，RPC）**：RPC面向生成过程中的周期性压缩，使用近期查询组成选择器窗口，估计历史词元是否仍然重要，并通过逐出低优先级词元缩小键值缓存。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- AM主要针对预填充阶段，并假设可在固定上下文上获得自学习查询，未直接解决推理轨迹持续增长时的中途、连续压缩需求。
- RPC采用简单词元逐出，在高压缩率下会系统性低估注意力质量；同时，AM与RPC都把推理轨迹视为扁平词元序列并统一分配压缩资源，因而可能对已失效的探索过程保留过多内容，却对题目定义、关键中间结果等长期有用信息压缩过度。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究分别探索了“逐出还是优化”这一压缩操作选择，以及“自学习查询还是近期选择器窗口”这一查询来源选择，但尚未系统利用思维链的层次结构来决定不同推理步骤应获得多少缓存预算。尤其缺少一种可在解码中途反复运行、同时结合分块预算分配与关键推理锚点保护的方案。

</div>
<div markdown="1"><span>核心问题</span>

在给定键值缓存预算下，能否依据各思维块的规模和对后续生成的重要性进行非均匀压缩，并保护块内关键词元，使模型在连续的中途压缩过程中比统一压缩或简单逐出更好地保留推理能力？

</div>
<div markdown="1"><span>作者直觉</span>

思维链中的信息价值并不均匀：探索性死路通常会随推理推进而失去作用，而题目条件、关键计算结果和阶段性结论可能持续影响后续生成。因此，可把有限缓存视为需要分配给不同推理步骤的资源：重要且信息量较大的思维块获得更多压缩后表示，次要块被更激进地压缩；再单独保留高注意力词元，可避免整体近似时抹去少量但关键的推理支点。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

TAM（Thought-Aware Attention Matching，思维感知注意力匹配）是一种仅用于推理阶段的 KV 缓存压缩方法。输入是语言模型当前已经生成的提示词与推理轨迹，以及各层、各 KV 头对应的键值缓存 $(\mathbf{K},\mathbf{V})$；输出是由少量压缩键、标量偏置、压缩值和未压缩保护尾部组成的新缓存。其端到端流程是：从最近的推理位置提取参考查询，按思维步骤切分可压缩前缀，以注意力衡量各步骤和各 token 的当前重要性，保护关键 token，并将有限的保留名额自适应分配给不同步骤；随后在每个步骤内部选择代表键，最后在整个前缀范围内拟合注意力质量与注意力输出。

技术上，TAM建立在注意力匹配（AM）之上。普通删除方法只保留原始 KV 条目的一个子集，会不可避免地减少被压缩前缀在 softmax 分母中的总质量，使未来 token 获得偏高的相对注意力；AM则为压缩键增加偏置 $\bm{\beta}$，同时近似原缓存的局部注意力输出和注意力质量。TAM没有改变这一全局拟合目标，而是改进“哪些键应被保留”：它不把长推理链视为重要性均匀的平坦序列，而是让较重要、较长的推理步骤获得更多名额，并原样保留持续受到高注意力的推理锚点。直观地说，TAM先按解题步骤整理草稿，再决定每一步应留下多少内容，最后校准摘要，使模型读取摘要时尽量产生与读取完整草稿相同的注意力结果。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提取选择器窗口查询并划定压缩区域

直接保留最后 $\tau$ 个 token 的 KV 状态，并对最近 $R$ 个位置执行一次带前向钩子的前向计算，取得逐层、逐头的参考查询 $\mathbf{Q}_{\mathrm{ref}}\in\mathbb{R}^{R\times d}$。每个 KV 头使用与自己对应的参考查询，前缀 $[0,L-\tau]$ 进入后续压缩。

<div class="method-step__io" markdown="1">

**输入**：长度为 $L$ 的当前 token 序列及其 KV 缓存 $(\mathbf{K},\mathbf{V})$，选择器窗口大小 $R$、尾部保护长度 $\tau$ 和目标缓存大小 $t$。<br>
**输出**：受保护尾部 $(\mathbf{K}_p,\mathbf{V}_p)$、可压缩前缀，以及表示当前推理前沿的参考查询 $\mathbf{Q}_{\mathrm{ref}}$。

</div>

**直观理解**：最近生成的 token 最能反映模型当前正在思考什么，因此可用其查询向量估计旧内容接下来是否仍有用。尾部不压缩，是为了避免破坏最新且通常最直接相关的上下文。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 切分思维步骤并计算重要性

默认以双换行检测推理步骤边界，将前缀切成 $\{S_1,\ldots,S_m\}$，并合并长度小于 $\ell_{\min}$ 的相邻短段；备选方案根据相邻位置平均注意力的梯度突变划界。对每段 $S_i$，计算其从 $\mathbf{Q}_{\mathrm{ref}}$ 接收的平均注意力质量 $w_i$，并记录段长 $n_i$。

<div class="method-step__io" markdown="1">

**输入**：可压缩前缀、解码后的 token 文本和参考查询 $\mathbf{Q}_{\mathrm{ref}}$。<br>
**输出**：带有段长 $n_i$ 和重要性 $w_i$ 的思维分段集合 $\{S_i\}_{i=1}^{m}$。

</div>

**直观理解**：一段长推理通常由多个功能不同的步骤组成，例如设变量、推导和核验；把它们分开后，系统才能避免给无关步骤和关键步骤分配相同比例的空间。双换行规则利用模型已有的书写结构，不需要额外训练一个边界识别器。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 保护关键 token 并自适应分配预算

计算每个可压缩 token 从选择器窗口获得的平均注意力；若其得分超过全前缀平均值的 $c$ 倍，则加入关键集合 $\mathcal{P}$ 并原样保留。扣除这些 token 占用的名额后，以 $\sqrt{w_i n_i}$ 为权重向各段分配 $t_i$ 个键名额，每段至少一个，舍入余量交给小数余项最大的段。

<div class="method-step__io" markdown="1">

**输入**：各段 $S_i$、段长 $n_i$、段重要性 $w_i$、参考查询 $\mathbf{Q}_{\mathrm{ref}}$、目标大小 $t$ 和阈值倍数 $c$。<br>
**输出**：关键 token 集合 $\mathcal{P}$、剩余预算 $t'=t-|\mathcal{P}|$，以及各思维段的保留预算 $\{t_i\}$。

</div>

**直观理解**：关键 token 类似草稿中的题目常数、关键中间结论或定义，若让压缩算法重新合成它们，误差可能被后续推理放大。预算同时考虑“这一段多重要”和“这一段有多长”：重要且长的步骤获得更多位置，低相关步骤只留下最低限度的代表。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分段选键、全局拟合并组装缓存

在每个 $S_i\setminus\mathcal{P}$ 中按参考查询下的聚合注意力选出 $t_i$ 个键，再合并所有分段结果与关键键形成 $\mathbf{C}_k$；随后全局使用非负最小二乘拟合偏置 $\bm{\beta}$ 以匹配注意力质量，并用普通最小二乘拟合 $\mathbf{C}_v$ 以匹配注意力输出。关键键的偏置固定为 $\beta_j=0$，最后将 $(\mathbf{C}_k,\bm{\beta},\mathbf{C}_v)$ 与尾部 $(\mathbf{K}_p,\mathbf{V}_p)$ 拼接。

<div class="method-step__io" markdown="1">

**输入**：关键集合 $\mathcal{P}$、各段预算 $t_i$、原始前缀 KV、参考查询 $\mathbf{Q}_{\mathrm{ref}}$ 和受保护尾部。<br>
**输出**：供后续自回归解码直接使用的紧凑 KV 缓存；若启用周期模式，缓存长度在约 $t$ 与 $t+P$ 之间变化。

</div>

**直观理解**：分段选键保证每个推理步骤都有与其价值相称的代表，全局拟合则让这些代表共同模拟完整前缀，而不是分别生成彼此不协调的局部摘要。偏置可以补回删除键造成的注意力总量缺口，值向量拟合则校准最终被读取出的信息。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 注意力输出与注意力质量的联合匹配条件

$$
\frac{\exp(\mathbf{q}_{i}\mathbf{K}^{\top}/\sqrt{d})\mathbf{V}}{\sum_{j=1}^{T}\exp(\mathbf{q}_{i}\mathbf{K}_{j}^{\top}/\sqrt{d})}\approx\frac{\exp(\mathbf{q}_{i}\mathbf{C}_{k}^{\top}/\sqrt{d}+\bm{\beta})\mathbf{C}_{v}}{\sum_{j=1}^{t}\exp(\mathbf{q}_{i}(\mathbf{C}_{k})_{j}^{\top}/\sqrt{d}+\beta_{j})},\qquad \sum_{j=1}^{T}\exp(\mathbf{q}_{i}\mathbf{K}_{j}^{\top}/\sqrt{d})\approx\sum_{j=1}^{t}\exp(\mathbf{q}_{i}(\mathbf{C}_{k})_{j}^{\top}/\sqrt{d}+\beta_{j})
$$

**符号说明**

- $\mathbf{q}_{i}$：第 $i$ 个参考查询向量，来自选择器窗口中的某个位置。
- $\mathbf{K},\mathbf{V}$：压缩前的键矩阵和值矩阵，分别包含 $T$ 个 KV 条目。
- $\mathbf{C}_{k},\mathbf{C}_{v}$：压缩后的键矩阵和值矩阵，分别包含 $t$ 个条目，且 $t\ll T$。
- $\bm{\beta}$：压缩键对应的逐条目标量偏置，用于校正删除原键后产生的注意力质量缺口。
- $d$：每个注意力头的键与查询维度；$\sqrt{d}$ 用于缩放点积。
- $T,t$：原始缓存条目数与压缩缓存条目数。

<div class="equation-explanation" markdown="1">

**直观理解**：第一个近似要求：对关心的参考查询，读取紧凑缓存所得的加权值应接近读取完整缓存的结果；第二个近似要求：紧凑前缀在 softmax 中占据的未归一化总质量也应接近原前缀。第二项很关键，因为即使前缀内部的归一化输出相似，若总质量偏小，当前缀与未来 KV 拼接后，模型仍会错误地把更多注意力转移给未来 token。<br>
**原文位置**：第 3.2 节，式 (3) 与式 (4)

</div>

</div>

<div class="equation-block" markdown="1">

#### 思维段自适应预算分配

$$
t_{i}=\max\!\left(1,\;\left\lfloor t^{\prime}\cdot\frac{\sqrt{w_{i}n_{i}}}{\sum_{j=1}^{m}\sqrt{w_{j}n_{j}}}\right\rfloor\right),\qquad t^{\prime}=t-|\mathcal{P}|
$$

**符号说明**

- $t_i$：分配给第 $i$ 个思维段的非关键压缩键数量。
- $t$：可压缩前缀的目标键预算。
- $t^{\prime}$：为关键 token 预留位置后剩余的预算。
- $\mathcal{P}$：需要原样保留的关键 token 集合。
- $w_i$：第 $i$ 个思维段从选择器窗口查询获得的平均注意力质量，即该段当前的重要性。
- $n_i$：第 $i$ 个思维段的 token 数量。
- $m$：可压缩前缀中的思维段总数。

<div class="equation-explanation" markdown="1">

**直观理解**：预算份额与重要性和段长乘积的平方根成正比，因此一个段只有在既重要又需要覆盖较多内容时才会得到较多键；外层最大值保证每段至少有一个代表。论文作者声称，在每段误差是局部压缩率的凸函数且采用线性误差模型时，该规则最小化总加权近似误差；实际整数预算还需通过向下取整和最大余数分配满足总预算约束。<br>
**原文位置**：第 4.4 节，式 (6)；理论依据见命题 C.1，证明指向附录 D

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：TAM不是训练模型或微调参数的方法，而是冻结语言模型后的推理期缓存优化。每次压缩中的“优化目标”是让紧凑缓存针对 $\mathbf{Q}_{\mathrm{ref}}$ 同时复现原缓存的注意力质量与注意力输出：固定所选 $\mathbf{C}_k$ 后，以 $u_j=\exp(\beta_j)\geq0$ 将质量匹配写成非负最小二乘并求得 $\bm{\beta}$，再在给定 $\mathbf{C}_k$ 和 $\bm{\beta}$ 的条件下用普通最小二乘求 $\mathbf{C}_v$。这两个闭式或数值拟合步骤只生成当前缓存的压缩表示，不更新 Qwen3-4B 等基础模型的权重。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 思维分段与参考查询模块**

默认分段器在解码文本中扫描双换行边界，时间复杂度为 $O(L)$，并合并不足 $\ell_{\min}$ 个 token 的短段；选择器窗口从最近 $R$ 个位置提取逐层、逐头查询，用这些查询计算分段重要性和 token 重要性。论文还提供注意力分段替代方案：若相邻位置平均注意力差的绝对值超过该差值中位数的两倍，则设置边界。

> 直观理解：该模块定义了压缩决策的两个坐标：文本结构说明“哪些 token 属于同一步”，最近查询说明“当前推理还在关注哪些内容”。两者结合后，压缩依据不再只是 token 的先后位置。

**2. 自适应预算与关键 token 保护模块**

对每个段使用完整前缀上归一化的注意力质量 $w_i$ 衡量重要性，并依据 $t_i\propto\sqrt{w_i n_i}$ 分配非关键键预算；同时把平均注意力高于 $c\,\bar{\alpha}_{\mathrm{mean}}$ 的位置纳入 $\mathcal{P}$。关键 token 的原始键和值被直接保留，且拟合时固定其 $\beta_j=0$，从而保持原始注意力 logit 不变。

> 直观理解：只按段长分配会浪费空间在长但无关的步骤上，只按注意力分配又可能把很长的重要步骤压得过狠。平方根分配在这两个因素之间折中，而直接保护少量异常重要的 token，可避免关键事实被近似过程冲淡。

**3. 全局注意力匹配与周期触发模块**

选键在各段内部独立进行，但 $\bm{\beta}$ 和 $\mathbf{C}_v$ 在所有已选键上统一拟合：令 $u_j=\exp(\beta_j)\geq0$ 后，注意力质量拟合成为非负最小二乘问题，值拟合成为普通最小二乘问题。周期模式每生成 $P$ 个新 token 或达到最大长度时重新切分、评分、选键和拟合；旧的关键 token 在下一轮不享有永久保护，而是按最新注意力重新竞争。

> 直观理解：局部选代表解决“每一步留下什么”，全局拟合解决“合起来读是否仍像原文”。周期触发则把一次性降低稳态内存扩展为全程限制峰值内存，但更小的 $P$ 意味着更频繁的压缩计算和更多轮近似误差。

**训练与推理**

训练阶段无需修改基础模型，也不需要为分段、重要性预测或关键 token 检测训练额外网络。推理时先按常规自回归方式生成并积累 KV；达到触发条件后，保留最近 $\tau$ 个 token，从最近 $R$ 个位置提取 $\mathbf{Q}_{\mathrm{ref}}$，按文本边界重建思维段，对每个 KV 头独立计算注意力、关键集合和分段预算，再完成分段选键与全局 NNLS/OLS 拟合。各头得到的压缩表示与未压缩尾部拼接后继续参与正常注意力计算。

一次性模式只在缓存达到最大序列长度时执行压缩，因而降低压缩后的稳态占用，但生成早期仍可能达到未压缩峰值。周期模式还在每新增 $P$ 个 token 后重复完整流程，使缓存大致在 $t$ 与 $t+P$ 之间波动；每轮都会根据最新文本和查询重新计算边界、重要性与关键集合。该设计适应推理焦点随生成过程变化的事实，但重复压缩增加计算成本，而且论文仅说明累积误差有理论界，不能据此认为多轮压缩完全无损。

**复现信息**

公平复现需要明确以下决定：压缩以每层、每个 KV 头为单位处理；默认分段依据双换行，并合并少于 $\ell_{\min}$ 个 token 的短段；关键阈值为 $\delta=c\,\bar{\alpha}_{\mathrm{mean}}$，原文默认 $c=3$；选择器窗口默认 $R=64$。段内候选在算法描述中按 $\mathbf{Q}_{\mathrm{ref}}$ 下的最高聚合注意力选择，关键 token 不参与普通段内选键；所有已选键合并后才执行全局质量与值拟合，且关键键固定 $\beta_j=0$。

目标大小 $t$ 应理解为压缩前缀预算，最终可用缓存还包括最后 $\tau$ 个未压缩 token；整数 $t_i$ 向下取整后，余量分给小数余项最大的段。周期版本默认使用 $P=1024$，但 $P$ 是内存、压缩频率和近似误差之间的控制量，不是模型参数。原文给出的约四千 token 单步时间分解中，主要开销来自分段选键、NNLS 和 OLS，而思维分段、重要性计算及关键 token 识别只是叠加在既有 AM 流程上的轻量步骤；不过具体硬件、$\tau$、$\ell_{\min}$ 及数值求解器容差在所给章节中未明确报告，复现时仍需核对完整论文与代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- AIME 2024：包含AIME I与AIME II共30道竞赛数学题，用于测试多步、长轨迹推理；生成序列中位长度约为$4\mathrm{k}$个令牌，因此尤其适合检验KV缓存压缩在长链式思维中的影响。原文未说明另行划分训练集或验证集，实验角色是小规模高难度推理评测。
- MATH-500：MATH测试集的500题子集，覆盖代数、几何、数论和组合数学。它提供比AIME 2024更大的样本量，用于降低仅在30题上比较准确率所带来的统计波动，并检验方法能否跨数学题型工作。每题具有确定答案，原文未说明进一步的数据划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Exact-match pass@1准确率**

在贪心解码下，每道题只生成一次答案，并统计最终答案与确定性标准答案完全匹配的比例；它测量压缩后模型能否保持端到端数学求解正确性。 （越高越好，因为更高比例表示压缩造成的推理或答案恢复损失更小。）

</div>
<div class="metric-item" markdown="1">

**峰值显存占用**

测量解码期间模型权重、KV缓存及相关运行状态造成的最高GPU显存需求，主要用于判断周期压缩是否真正限制长序列生成的内存峰值。 （在准确率可接受的前提下越低越好，因为较低峰值允许在固定硬件上生成更长序列或服务更多请求。）

</div>
<div class="metric-item" markdown="1">

**压缩时间**

测量执行KV缓存压缩操作所需的时间，用于评估节省显存是否引入过大的额外计算开销。 （越低越好，因为压缩时间会直接增加推理解码延迟；但原文节选未给出具体计时结果。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### AIME 2024与MATH-500，相同KV保留比例下比较TAM和均匀压缩

<div class="result-value" markdown="1">

作者报告，TAM在相同内存占用下比均匀压缩获得更高准确率，说明按推理段分配预算并保护关键令牌可以改善压缩后的任务表现；但所给节选没有提供各保留比例、各数据集对应的完整分数，因此无法判断提升幅度及统计稳定性。

</div>

这一结果支持“不同推理内容不应被等比例压缩”的核心主张：同样只留下固定数量的KV条目，把更多容量留给重要推理段通常比平均分配更有效。它不能单独证明三个组件各自都必要，也不能证明TAM优于所有长上下文压缩方法，因为比较范围主要是均匀注意力匹配和适配后的驱逐基线。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Experiments on AIME 2024 and MATH-500 with Qwen3-4B show that TAM improves accuracy over uniform compaction at the same memory footprint, with periodic compaction bounding peak memory to 3.1--3.2\,GB (a 65\% reduction) while maintaining competitive accuracy.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### TAM周期压缩，触发间隔$P=1024$个令牌

<div class="result-value" markdown="1">

作者报告，周期TAM把峰值显存限制在3.1至3.2GB，相比参照配置降低65%，同时维持有竞争力的准确率。该结果直接测试周期触发是否能避免KV缓存随生成长度持续增长。

</div>

一次性压缩只有在到达触发长度后才释放缓存，触发前仍可能出现较高显存峰值；周期压缩则不断把旧缓存压回目标规模，因此更适合受显存上限约束的长推理解码。不过“有竞争力”不是等同于“无准确率损失”，而且节选没有给出65%所对应参照配置的逐项显存值、压缩时间或置信区间。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Experiments on AIME 2024 and MATH-500 with Qwen3-4B show that TAM improves accuracy over uniform compaction at the same memory footprint, with periodic compaction bounding peak memory to 3.1--3.2\,GB (a 65\% reduction) while maintaining competitive accuracy.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### MATH-500，TAM保留比例为0.1，与完整KV缓存比较

<div class="result-value" markdown="1">

TAM取得67.8%准确率，完整缓存为71.2%，绝对差距为3.4个百分点。作者的错误分析指出，差距主要集中在超过6000个令牌的长推理链，以及后期回溯并重新使用早期推理段的问题。

</div>

只保留10% KV条目时仍接近完整缓存，表明压缩保留了大部分端到端解题能力，但性能并未完全恢复。失败分布还揭示了当前重要性估计的时间局限：早期看似无关的内容可能在后续修正中重新变得重要。这里的“集中”来自作者的事后分析，节选没有给出各失败类型的题目数量或显著性检验，因而不能量化两类原因各自贡献了多少误差。

<div class="result-source" markdown="1">

来源：Appendix B, Error analysis

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On MATH-500, the accuracy gap (67.8% vs. 71.2%) concentrates on problems with two characteristics: (i) very long reasoning chains (>6k tokens) that produce many segments with complex non-local dependencies between distant reasoning steps, and (ii) problems where the model’s reasoning path undergoes a late-stage correction that revisits earlier segments.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验节选缺少完整主结果表、组件消融表和压缩时间数值。因而只能确认作者报告的总体趋势、周期显存结果及MATH-500的一个准确率对比，无法核验不同保留比例下的逐项收益，也无法分别归因于思维分段、自适应预算和关键令牌保护；因此消融列表保持为空。
- 评测只使用Qwen3-4B、两个数学数据集和贪心解码。AIME 2024仅有30题，且方法在超过6000令牌、存在远距离依赖或后期回溯的轨迹上更易失败；现有证据不足以证明结论可推广到其他模型规模、采样策略、非数学任务或需要频繁修正早期推理的场景。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- No Compaction：保留完整KV缓存，作为不受压缩误差影响的准确率参照。它并非同显存预算下的竞争方法，而是用于衡量压缩方案相对完整缓存损失了多少任务性能。
- Eviction (Selector Window)：根据选择器窗口产生的注意力分数保留高注意力键并删除其余条目，将H2O、SnapKV一类基于注意力的令牌选择思想适配到生成中途。该基线用于区分TAM的注意力匹配式压缩与直接删除KV条目的差异。
- AM + Repeat：在达到最大长度时执行一次注意力匹配，并使用重复预填充查询。它代表已有注意力匹配方案，用于检验TAM的思维结构建模是否比一般的匹配式压缩更有效。
- PAM (Uniform)：使用选择器窗口查询执行注意力匹配，但采用均匀预算，且不使用思维分段和关键令牌保护；只在最大长度处压缩一次，即$P=\infty$。这是最直接的同类对照，用于判断TAM的结构感知设计是否优于把推理轨迹视为平坦令牌序列。

**实验想回答的问题**

- 在保留相同比例KV条目的条件下，利用思维分段、按段自适应预算和关键令牌保护的TAM，是否比均匀压缩、直接驱逐及已有注意力匹配方案更能保持数学推理的答案准确率？
- 周期性执行TAM能否在长链式思维生成过程中限制峰值显存，同时保持有竞争力的准确率；其优势是否与不同推理段的重要性差异有关？

**实验实现**

基础模型为Qwen3-4B，使用GPTQ-Int4四比特量化，在单张80GB NVIDIA A100上运行。所有题目采用温度为0的贪心解码，最大生成长度为8192个令牌。目标保留比例遍历$\{0.05,0.1,0.2\}$，分别只保留原KV条目的5%、10%或20%；最近$\tau=20$个令牌始终受到保护，选择器窗口长度为$R=64$，关键令牌阈值乘子为$c=3$。默认以双换行启发式切分思维段，最短段长为$\ell_{\min}=32$，并按最高注意力分数选择键。一次性TAM在最大长度处压缩，即$P=\infty$；周期版本每生成$P=1024$个令牌触发一次压缩。该协议同时改变压缩比例和触发方式，用于观察准确率、峰值显存及压缩代价之间的权衡。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 作者人工检查$c=3$时识别出的关键令牌，发现它们主要是题目中的数值常量、推导得到的方程或变量绑定，以及“Therefore”“=”等维系推理结构的令牌。该观察说明高注意力令牌在语义上确实可能充当后续推理反复依赖的锚点，但这是定性检查；原文节选未报告标注标准、样本数量或人工一致性，因此不能据此量化关键令牌检测的准确性。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：核心贡献是利用思维链结构进行自适应 KV Cache 压缩，以降低推理内存并保持推理准确率。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`8aa443afd00fc6d7800c22095ef6c29595a58d225ac0384dafef4274b9b96612`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
