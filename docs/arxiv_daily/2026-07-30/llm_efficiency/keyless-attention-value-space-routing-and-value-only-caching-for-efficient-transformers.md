---
title: "[论文解读] Keyless Attention: Value-Space Routing and Value-Only Caching for Efficient Transformers"
description: "[arXiv 2606.21848][LLM 效率] 本文研究能否用“价值空间路由”取代传统键投影，使Transformer在不缓存键表示的情况下保持模型能力，并将自回归推理的KV缓存及其访问开销减半。"
arxiv_id: "2606.21848"
announcement_date: "2026-07-30"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.675465+00:00"
source_sha256: "c8e690fa03abdbe36fca73fe3582fa363710b1966e0b9ad3a2676500f8aa3c01"
tags:
  - "LLM 效率"
  - "Keyless Attention"
  - "Value-Only Cache"
  - "值空间路由"
  - "KV缓存"
  - "自回归推理"
  - "注意力因子分解"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2606.21848</p>

# Keyless Attention: Value-Space Routing and Value-Only Caching for Efficient Transformers

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Xin Gao, Xingming Xu</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2606.21848v2) · [PDF 下载](https://arxiv.org/pdf/2606.21848v2) · **关键词** Keyless Attention, Value-Only Cache, 值空间路由, KV缓存, 自回归推理, 注意力因子分解<br>


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

本文研究能否用“价值空间路由”取代传统键投影，使Transformer在不缓存键表示的情况下保持模型能力，并将自回归推理的KV缓存及其访问开销减半。

**不用术语来说**：语言模型生成文本时，需要反复读取此前每个词留下的两份中间表示，即键和值；上下文越长、并发请求越多，这些数据占用的显存和搬运成本就越高，甚至可能超过模型参数本身。现有方法通常压缩、共享或筛除这些表示，但可能增加额外处理、丢失历史信息，或者虽然取消独立键投影，却没有专门机制承担键原本用于判断“当前查询应关注哪些历史词”的路由功能。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出Keyless Attention：取消键表示及键缓存，直接在查询与值之间计算注意力，并加入专用的价值空间路由投影来承担原键投影的令牌路由职责，从而形成Value-Only Cache。
- 从Depth-m Attention Factorization角度解释该设计，并采用m=3的实例，使投影矩阵数量与标准注意力一致；作者据此检验专用路由是否能在降低推理缓存成本的同时维持语言建模和下游任务表现。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究自回归语言模型的注意力与推理缓存效率。标准缩放点积注意力将每个词元的隐藏状态分别投影为查询（Q）、键（K）和值（V）：Q与历史K的相似度决定应从哪些位置读取信息，再对相应V加权求和。生成阶段若反复计算全部历史表示，代价很高，因此系统通常缓存各层历史词元的K和V；这样单个新词元的解码计算量相对上下文长度由二次增长降为线性增长，但缓存内存仍随序列长度、批量大小、网络层数和注意力头数线性增加。在长上下文、大批量部署中，KV缓存甚至可能超过模型参数所占内存，因而成为并发量与解码吞吐的主要限制。本文关注的核心问题不是管理或压缩现有KV缓存，而是重新设计注意力，使推理时只需保存V，同时保留原本由K承担的词元路由能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**缩放点积注意力（Scaled Dot-Product Attention）**

模型用查询Q与各位置的键K计算匹配分数，经归一化后作为权重，对值V进行加权汇总。直观地说，K负责判断“去哪里找”，V负责提供“取回什么内容”。

</div>
<div class="concept-item" markdown="1">

**自回归解码与KV缓存**

自回归模型每次根据已有词元生成下一个词元；KV缓存保存各层对历史词元已计算出的K和V，避免后续步骤重复计算。其代价是缓存容量随上下文、批量、层数和注意力头数量持续增长，并产生显著的内存访问开销。

</div>
<div class="concept-item" markdown="1">

**值空间路由（Value-Space Routing）**

本文提出以专门的路由投影替代传统键投影，使查询能够直接在值表示所在的空间中计算注意力分数。它不同于简单令K与V共享同一表示，因为仍保留一个明确负责路由的可学习变换。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是自回归Transformer在某一层的当前词元隐藏状态以及此前所有词元的历史表示；模型需要输出当前词元的注意力聚合结果，并继续完成下一词元预测。标准方案为当前词元构造Q，并从缓存读取历史K、V来计算注意力；本文设定是在保持常规语言模型训练方式和注意力表达能力的前提下，彻底取消独立K表示，以查询和历史V直接完成匹配与信息汇聚，使推理阶段仅缓存V。该设计针对长上下文推理，假设历史值表示可逐词元保存，而专门的值空间路由矩阵承担原键投影的词元选择功能。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$Q$**

查询表示，由当前词元的隐藏状态投影得到，用于发起对历史位置的信息检索。

</div>
<div class="notation-item" markdown="1">

**$K$**

标准注意力中的键表示，与Q计算匹配分数；Keyless Attention将其从注意力计算和缓存中取消。

</div>
<div class="notation-item" markdown="1">

**$V$**

值表示，承载被注意力权重汇总的内容；本文推理时只缓存该表示。

</div>
<div class="notation-item" markdown="1">

**$m$**

注意力双线性形式的因子分解深度；原文称标准注意力为深度2，而本文采用的Keyless Attention实例取m=3。

</div>

</div>

**直接相关的工作**

- **Multi-Query Attention（MQA）与Grouped-Query Attention（GQA）**: 二者通过让多个查询头共享键和值投影，减少跨注意力头的KV冗余，但仍需为每个历史词元保留K和V。本文进一步取消K缓存，因此解决的是表示种类而不仅是注意力头之间的重复。
- **KV-sharing方法（Edward, 2026；Kayyam et al., 2026；Team et al., 2026）**: 这类方法令K与V共享同一投影，可将KV缓存缩减50%，但原文指出其没有显式替代键的词元路由功能。Keyless Attention同样取消独立键投影，却额外引入专用的值空间路由矩阵，以区分“用于选择位置的变换”和“承载内容的值表示”。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

标准Transformer在自回归解码中缓存所有历史令牌的键和值，以避免重复计算；这把单步计算降为随上下文长度线性增长，却使缓存显存随序列长度、批量大小、层数和注意力头数共同增长。长上下文大模型中，KV缓存可能大于模型参数，并因持续读取历史缓存而成为推理并发度、吞吐量和可部署规模的主要约束。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **架构级共享或压缩方法**：MQA和GQA让多个查询头共享键、值投影，以减少头间冗余；MLA先把键和值压缩到低维潜在表示后再缓存；KV-sharing则让键和值使用同一投影，从而只保存一份表示。Slim Attention采取另一条路径：缓存键，并依据预训练权重之间的闭式变换精确恢复值。
- **缓存管理与内容压缩方法**：系统方法通过虚拟内存、动态物理内存分配和压缩感知调度提高缓存利用率与请求并发；算法方法则对KV缓存量化，或依据重要性剪除、仅保留部分历史令牌，以直接减少每个请求保存和读取的数据量。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 系统级管理主要改善既有KV缓存的放置、分配与调度，并未消除每层、每个历史令牌同时维护键和值这一结构性开销；共享或低维压缩虽然减少冗余，但通常仍围绕两类表示设计，不能从根本上得到仅含值的缓存。
- 量化和令牌筛选会引入额外的压缩、选择或调度复杂度，且删除历史令牌可能损害有用的长程依赖；已有KV-sharing虽能取消独立键投影并减半缓存，却没有显式替代键投影原本负责的内容路由功能，因此其表达能力与性能保持机制仍不充分。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种原生的注意力架构：它能完全移除键表示和键缓存，同时设置独立、可学习的机制来承担键空间中的路由职责，而不是简单地令键和值共用同一表示；该架构还应兼容常规大语言模型训练，并在不同模型家族上验证缓存收益不是以明显性能损失换来的。

</div>
<div markdown="1"><span>核心问题</span>

能否把注意力中的相关性判断改写为查询经专用价值空间路由后与值表示进行匹配，从而只缓存值，并在将KV缓存及访问开销降低50%的同时，达到与标准QKV注意力相当的语言建模和下游推理性能？

</div>
<div markdown="1"><span>作者直觉</span>

键本身不会作为注意力层的最终内容输出，它主要用于给历史令牌打分；真正被加权汇总并传递到后续网络的是值。因此，与其保存一份专门用于匹配的键，不如学习一个独立路由矩阵，把查询变换到适合与值比较的空间，再直接利用同一份值完成“选谁”和“取什么”。这保留了路由参数与内容参数之间的功能分工，又避免为每个历史令牌长期保存第二份表示。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Keyless Attention 将标准注意力中彼此独立的“键路由”和“值检索”改写为同一值空间内的路由与检索。给定隐藏状态 X，训练时先通过 $W^Q$ 和专用值路由矩阵 $W^R$ 得到与值空间兼容的查询，再以 XW^V 同时充当被匹配和被聚合的表示；因此不再生成 K=XW^K。自回归推理时将 $W^QW^R$ 预先合并为有效查询投影，只缓存历史值向量，输出仍是按注意力权重加权的值之和。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 输入表示与值投影

使用 $W^V$ 将每个位置映射为 V=XW^V，其中 d 为隐藏维度、n 为序列长度。V 不仅是最终聚合的内容，也直接参与注意力路由。

<div class="method-step__io" markdown="1">

**输入**：一层 Transformer 的序列隐藏状态 $X\in\mathbb{R}^{n\times d}$；自回归解码时可仅输入当前 token 的隐藏状态，并读取此前缓存。<br>
**输出**：值表示矩阵 V；解码时，当前值 $v_{n+1}$ 被追加到历史 Value-Only Cache。

</div>

**直观理解**：标准注意力为每个历史 token 保存“用于查找的键”和“真正取出的值”两份表示；这里让值同时承担被查找和被读取两种职责。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 查询到值空间的路由

训练时计算 $Q_R=XW^QW^R$，使查询进入与 V 可直接点积的空间。$W^R$ 替代原有 $W^K$ 的路由功能，但训练参数量仍保留三组投影 $W^Q$、$W^R$、$W^V$。

<div class="method-step__io" markdown="1">

**输入**：隐藏状态 X、查询投影 $W^Q$ 和值路由投影 $W^R$。<br>
**输出**：值空间兼容查询 $Q_R$。

</div>

**直观理解**：$W^R$ 像一个转接器：它不再为历史内容另做一套“索引卡”，而是把查询转换成能够直接搜索值向量的形式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 值空间打分与内容聚合

计算缩放点积 $Q_RV^\top/\sqrt{d_k}$，经 softmax 得到位置权重，再用这些权重聚合同一个 V。多头注意力中各头独立执行该过程并拼接输出；MQA 或 GQA 则让多个查询头共享一个值头或一组值头。

<div class="method-step__io" markdown="1">

**输入**：值空间查询 $Q_R$ 和值矩阵 V。<br>
**输出**：注意力层的上下文表示。

</div>

**直观理解**：模型根据“这个值本身与问题有多相关”决定读取比例，而不是先在独立键空间匹配、再转去读取另一份值表示。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 推理解耦与 Value-Only Cache

部署前预计算 $\tilde{W}^Q=W^QW^R$；每个解码步只生成当前有效查询和当前值，将当前值写入缓存，并令查询与全部缓存值计算注意力。由于历史键不再构造、存储或读取，缓存由 K、V 两部分缩减为 V 一部分。

<div class="method-step__io" markdown="1">

**输入**：训练完成的 $W^Q$、$W^R$、$W^V$，以及逐步增长的历史值缓存。<br>
**输出**：当前 token 的注意力输出和更新后的仅值缓存。

</div>

**直观理解**：训练阶段保留两层查询变换以学习更合适的路由，推理前把两层乘成一层，因此不会因额外因子分解而增加在线查询投影开销。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### Keyless Attention

$$
\mathrm{Attention}(X,W^Q,W^R,W^V)=\mathrm{softmax}\!\left(\frac{XW^QW^R(W^V)^\top X^\top}{\sqrt{d_k}}\right)XW^V
$$

**符号说明**

- $X\in\mathbb{R}^{n\times d}$：含 n 个 token、隐藏维度为 d 的输入序列表示。
- $W^Q$：查询投影矩阵，将隐藏状态映射到查询表示。
- $W^R$：值路由投影矩阵，将查询进一步映射到可与值直接匹配的空间。
- $W^V$：值投影矩阵；XW^V 既用于计算路由分数，也作为加权聚合的内容。
- $d_k=d/N_h$：每个注意力头的维度，$N_h$ 为注意力头数；平方根缩放用于控制点积幅度。
- $\mathrm{softmax}(\cdot)$：沿可被关注的位置将打分归一化为注意力权重；自回归模型中还需配合因果掩码。

<div class="equation-explanation" markdown="1">

**直观理解**：括号内先用转换后的查询与所有值计算相关性，softmax 把相关性变成读取比例，最后按比例汇总同一组值。相较 QKV 注意力，等式中没有 XW^K，因此历史 token 无须产生或缓存键。<br>
**原文位置**：第 2.1 节，公式 (2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 潜在 Value-Only Cache 注意力

$$
\mathrm{softmax}\!\left(\frac{Q_h^*(V^*)^\top}{\sqrt{r}}\right)V^*W^V_{h,\mathrm{post}},\qquad V^*=XW^V_{h,\mathrm{pre}},\quad Q_h^*=Q_h(W^V_{h,\mathrm{post}})^\top
$$

**符号说明**

- $h$：注意力头索引。
- $V^*$：需要实际写入缓存的 r 维潜在值表示。
- $W^V_{h,\mathrm{pre}}\in\mathbb{R}^{d\times r}$：将隐藏状态压缩到潜在维度 r 的值投影。
- $W^V_{h,\mathrm{post}}\in\mathbb{R}^{r\times d_k}$：将聚合后的潜在值扩展回每头维度 $d_k$ 的投影。
- $Q_h^*$：吸收值扩展矩阵后、可直接与潜在缓存 V^* 匹配的查询。
- $r$：潜在缓存维度；当 $r<d_k$ 时，缓存小于直接保存每头值向量。

<div class="equation-explanation" markdown="1">

**直观理解**：该式先在压缩空间中完成匹配和聚合，最后才把结果恢复到正常的头维度。它是基础 Value-Only Cache 的可选进一步压缩，而不是 Keyless Attention 成立所必需的步骤。<br>
**原文位置**：第 3 节“Multihead with Latent Value-only Cache”，公式 (15)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：节选未给出新的专用损失函数；Keyless Attention 作为注意力层替换件，仍由模型原有任务损失 $\mathcal{L}$ 端到端训练，因此不能据此补写具体语言建模交叉熵形式。其优化差异来自计算图：$W^R$ 的梯度通过 V=XW^V 依赖值投影，$W^V$ 的梯度则同时接收注意力打分路径和输出聚合路径的信号。作者据此提出隐式正则化假设，同时明确指出这种耦合可能减慢收敛。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 值空间路由投影**

核心双线性打分矩阵由标准注意力的 $\Omega=W^Q(W^K)^\top$ 改为 $\Omega=W^QW^R(W^V)^\top$，因子分解深度由 2 增至 3。$W^QW^R$ 的秩不超过 $d_k$；单头且 $W^V$ 满秩时，论文证明存在唯一有效查询投影可复现标准注意力的打分矩阵，多头情形则还要求每头标准打分矩阵的相应列空间包含于该头 $W^V$ 的列空间。

> 直观理解：额外的 $W^R$ 不是另一份需要缓存的 token 表示，而是模型权重中的查询变换。它保留专门学习“如何查找”的能力，同时把查找目标约束为真正要读取的值。

**2. 路由—检索梯度耦合**

由于 V=XW^V 同时进入注意力分数和输出聚合，$W^R$ 的梯度显式依赖 V，而 $W^V$ 的梯度又通过打分项依赖 $Q_R=XW^QW^R$。作者将这种相互依赖称为 gradient entanglement，并假设它可作为隐式正则化、减少路由对语料共现模式的独立特化，但也指出这会使优化更困难、收敛慢于常规注意力。

> 直观理解：路由器和内容表示不能各自独立学习：一方改变后，另一方下一步面对的目标也会改变。正面作用可能是限制过拟合，代价则是训练协调更困难；其中正则化解释是作者假设，而非形式化保证。

**3. 适配多头共享方式的仅值缓存**

MHA 为每个头保存独立 $V_h$；MQA 让所有查询头共享一个 V；GQA 让同组查询头共享 $V_g$。Keyless 机制只移除与相应值缓存配对的键缓存，因此可叠加在 MHA、MQA、GQA 以及潜在值压缩设计上。

> 直观理解：无论模型给每个头一份值，还是让若干头共享值，都可以只保存值而不保存键。具体总缓存大小仍取决于值头或值组的数量。

**训练与推理**

训练时，从随机初始化或目标架构的从头初始化配置出发，将每个标准键投影 $W^K$ 替换为权重矩阵 $W^R$；前向计算依次形成 XW^QW^R、XW^V、注意力权重和加权值输出，再由原任务损失联合更新 $W^Q$、$W^R$、$W^V$ 及模型其余参数。虽然不再产生键表示，但仍保留三组可学习投影，因此方法的重点是改变注意力因子化和缓存内容，而不是简单删去一组训练参数。

推理前把 $W^Q$ 与 $W^R$ 合并成 $\tilde{W}^Q=W^QW^R$。自回归第 n+1 步生成当前查询 $q_{n+1}$ 和值 $v_{n+1}$，把 $v_{n+1}$ 追加到由 $v_1,\ldots,v_n$ 构成的缓存；随后用 $q_{n+1}$ 与全部缓存值点积并 softmax，输出其加权和。由此无需构造、写入和读取历史键；论文声称相对对应的常规 KV 缓存，内存占用和内存访问开销均减少 50%，但这一比例针对移除键这一部分，若叠加 MQA、GQA 或潜在压缩，绝对缓存规模还取决于共享方式与潜在维度。

**复现信息**

公平实现的关键是保持原架构的头共享模式：普通 MHA 每头配置独立值缓存；Qwen2 1.5B 的 12 个查询头、2 个 KV 头采用 GQA，Keyless 版本使用 2 个值路由头，同时令相关查询侧投影按查询头独立；Llama 3.2 1B 的 32 个查询头、8 个 KV 头同样使用 8 个值路由头和按查询头独立的查询侧投影。这样做是为了在共享值表示时仍保留各查询头特有的路由能力，而不是把所有查询头也强制共享。

推理实现应在加载或部署阶段缓存合成矩阵 $\tilde{W}^Q$，避免每个 token 连续执行 $W^Q$ 与 $W^R$ 两次投影；缓存管理器只分配和追加 V 或可选的 V^*。潜在缓存中的压缩矩阵和扩展矩阵可以按头、按组或全头共享，复现时必须明确这一选择及 r，因为它们直接决定参数共享和缓存复杂度。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- WikiText-103：主要语言建模数据集。受 GPU 显存限制，实验使用其中 3000 万 token 的子集，从头训练五个模型；原文未明确报告训练集、验证集的具体 token 划分。它用于比较训练动态、最佳验证损失、困惑度、过拟合趋势及因子化深度消融。
- 五个零样本常识与问答基准：HellaSwag、ARC-Challenge、StoryCloze、SciQ 和 BoolQ，使用 36 层 GPT-2 模型评估准确率。它们分别覆盖常识续写、科学考试问答、故事结局、科学问答和布尔问答，用于检验语言建模结果能否迁移到下游任务；原文节选未明确报告各基准的样本规模。
- 推理效率测试工作负载：以 Qwen2-1.5B 的 GQA 架构为测试平台，设置 512、2048 和 8192 token 的 prefill 上下文，batch size 为 1，每次生成 256 token。它不是训练数据集，而是专门用于测量解码吞吐与缓存显存的标准化输入配置。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**验证损失与困惑度（PPL）**

验证损失衡量模型对未见文本赋予正确概率的能力；困惑度通常是平均交叉熵的指数形式，可理解为模型预测下一个 token 时的平均不确定性。最佳检查点比较主要能力，最佳点后的变化则反映过拟合稳健性。 （越低越好，因为较低值表示模型对真实后续 token 分配了更高概率。）

</div>
<div class="metric-item" markdown="1">

**零样本准确率**

不针对目标任务继续训练，直接计算五个下游基准中回答正确的比例，用于检验所学表示和语言能力能否迁移。 （越高越好，因为表示正确完成的测试样本比例更大。）

</div>
<div class="metric-item" markdown="1">

**解码吞吐与注意力缓存大小**

解码吞吐衡量单位时间内生成 token 的能力；缓存大小衡量自回归推理为历史 token 保存注意力状态所需的显存。两者共同测试 Keyless 是否带来实际推理收益，而不只是参数形式上的简化。 （吞吐越高越好，缓存越小越好；前者意味着生成更快，后者意味着可支持更长上下文或更大 batch。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 五种模型、四类架构上的语言建模表现

<div class="result-value" markdown="1">

Keyless 在五个模型中的四个达到或优于标准 QKV 的最佳困惑度：36 层 GPT-2 为 33.26 对 33.50；Pythia 410M 为 39.22 对 40.99；Qwen2 1.5B 为 33.79 对 34.38；Llama 3.2 1B 为 38.59 对 39.09。12 层 GPT-2 则略差，为 33.84 对 33.71。

</div>

作者结果表明，删除独立 key 表示并没有在所测架构上造成系统性的语言建模退化，而且较深 GPT-2 与三种外部架构均有小幅改善。分析上，这支持方法具有一定跨架构适用性，但改善幅度多数较小；除 GPT-2 外的跨架构结果未说明多随机种子显著性，因此不能据此断言 Keyless 普遍优于 QKV。

<div class="result-source" markdown="1">

来源：摘要；具体数值见第 5.1 节、图 2 与第 5.4 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Experiments across five models and four architectures show that Keyless Attention matches or outperforms standard QKV attention in perplexity on four of five models.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 36 层 GPT-2 的五项零样本下游评估

<div class="result-value" markdown="1">

QVV(3) 在 HellaSwag 和 StoryCloze 上显著优于 QKV，单侧 Welch t 检验分别为 p=0.004 和 p=0.007；ARC-Challenge 与 BoolQ 被作者判为可比，分别为 p=0.475 和 p=0.086；SciQ 上 QKV 更强，p<0.001。

</div>

该结果检验节省缓存是否以通用任务能力为代价。作者证据显示 Keyless 的影响取决于任务：两项显著改善、两项没有显著差异、一项显著较弱，因此更恰当的结论是总体具有竞争力，而不是全面提升。节选没有给出表 2 的准确率与方差，无法判断这些统计差异的实际效应大小。

<div class="result-source" markdown="1">

来源：第 5.2 节，表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A one-sided Welch’s t-test shows that QVV(3) significantly improves performance on HellaSwag (p=0.004) and StoryCloze (p=0.007), while achieving comparable performance on ARC-Challenge (p=0.475) and BoolQ (p=0.086).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen2-1.5B GQA 的自回归解码效率

<div class="result-value" markdown="1">

在 512、2048、8192 token 三种上下文长度下，Keyless 的解码吞吐均高于 QKV；其缓存始终减少 50%，其中 8192 token 时为 0.118 GB，而 QKV 为 0.236 GB。

</div>

缓存减半是结构上的直接结果：标准方法需要保存历史 key 和 value，Keyless 只保存 value。投影融合后也无需为路由额外执行一次查询投影，因此测试中吞吐有所提高。不过节选没有提供各长度的具体吞吐数值，且 batch size 固定为 1；作者关于更大 batch 会获得更明显加速的说法仍是预期，而非本实验直接证明。

<div class="result-source" markdown="1">

来源：第 5.5 节，图 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Figure 4 (right panel) shows the corresponding KV cache size: since Keyless stores only value states, it reduces cache memory by exactly 50% at every context length (e.g., 0.118 vs. 0.236 GB at 8192 tokens).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 训练数据仅为 WikiText-103 的 3000 万 token 子集，且所有模型均在单张 A100 上从头训练；这与现代大模型的训练数据规模、预训练时长和分布差异很大。因而实验能说明受控条件下的架构可行性，但不能直接证明替换成熟大模型中的 QKV 后仍可保持能力。
- 效率测试只覆盖 Qwen2-1.5B、batch size 1、三个上下文长度，并未报告完整吞吐数值、延迟、峰值显存、不同硬件或更大 batch 的结果。缓存减半可由结构严格推出，但更大 batch 下加速会显著增长只是作者预期，原文未明确报告实验证据。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 标准 QKV Attention，即分别投影 query、key、value，并在自回归推理中缓存 key 和 value。它是最直接的基线，因为实验让模型仅在注意力机制上不同，可以隔离删除 key 表示的影响。
- QVV(2)，即没有价值空间路由矩阵 $W^R$ 的 KV-sharing 方法，key 与 value 实际共享同一表示。它用于判断收益究竟来自简单共享，还是来自专门学习的价值空间路由。
- QKV(3)，即在标准 QKV 注意力的 query 路径中额外加入一个投影矩阵。它控制了投影深度与附加参数因素，用于判断 QVV 的表现是否仅由更深的线性因子化造成。
- QVV(4) 与 QVV(4ReLU)：前者比 QVV(3) 多一个线性权重矩阵，后者还插入 ReLU 非线性。二者用于检验继续加深因子化是否必要，以及线性结构本身是否重要。

**实验想回答的问题**

- 在训练数据、优化器和预处理保持一致时，以价值空间路由替代键投影的 Keyless Attention，能否在不同模型规模、位置编码、残差结构以及 MHA/GQA 配置下，保持或改善语言建模与零样本下游性能？
- 仅缓存 value、并在推理前融合连续查询投影，能否稳定减少缓存占用并提高解码吞吐；其中独立的价值空间路由矩阵是否确实优于简单的 key-value 表示共享？

**实验实现**

所有模型均通过 Hugging Face Transformers 实现，并在单张 NVIDIA A100-SXM4-80GB GPU 上从头训练；AdamW 学习率为 10^-4、weight decay 为 0.01。GPT-2 使用线性学习率衰减和 5% warmup，Pythia、Qwen2 与 Llama 使用余弦衰减和 5% 线性 warmup。主要 GPT-2 比较覆盖 12 层 280M 与 36 层 557M 模型，每个设置以三个随机种子训练 10 个 epoch，并报告均值和标准差；前者用 FP32、后者用 FP16。跨架构实验加入 Pythia 410M、Qwen2 1.5B 和 Llama 3.2 1B，覆盖 learned absolute、partial RoPE、full RoPE，顺序/并行残差以及 MHA/GQA。下游实验采用 36 层 GPT-2 做零样本评估，并以单侧 Welch t 检验比较方法。效率测试在 Qwen2-1.5B GQA 上进行，三个上下文长度均取三个随机种子的平均值；推理前将 Keyless 的连续查询投影 $W^Q$ 与 $W^R$ 融合，以避免额外查询投影开销。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 有无专用价值空间路由：QVV(2) 对比 QVV(3)/QVV(4)，12 层 GPT-2、WikiText-103 | 没有 $W^R$ 的 QVV(2) 验证损失劣于标准 QKV(2)；加入路由的 QVV(3) 和 QVV(4) 则在最佳验证损失上匹配 QKV(2) 与 QKV(3)，且最佳 epoch 后的过拟合较弱。 | 该对比隔离了专用价值空间路由，而不是笼统比较“无 key”与“有 key”。结果支持作者主张：仅让 key 和 value 共享表示会损失效果，路由矩阵能从 value 表示中学习适合注意力匹配的方向。不过节选没有报告消融的具体损失值或误差范围，效果大小需回查图 3。 | 第 5.3 节，图 3<br><span class="experiment-evidence">QVV(2) achieves worse validation loss than the QKV(2) baseline, while QVV(3) and QVV(4) match QKV(2) and QKV(3) at best validation loss.</span> |
| 线性因子化深度与非线性：QVV(3)、QVV(4)、QVV(4ReLU) | QVV(4ReLU) 表现最差；纯线性的 QVV(3) 与 QVV(4) 表现相近，而 QVV(4) 多需一个权重矩阵，因此作者选择 QVV(3) 作为最佳效率—性能折中。 | 该消融检验收益是否来自任意增加网络深度。ReLU 版本变差，说明路由路径并非越复杂越好；在本数据集上，额外线性层也没有带来清晰收益。作者将此解释为 ReLU 破坏线性因子化的隐式正则化，但实验只展示相关现象，尚未直接验证该因果机制。 | 第 5.3 节，图 3<br><span class="experiment-evidence">Since QVV(3) and QVV(4) perform comparably while QVV(4) requires one additional weight matrix, QVV(3) offers the best efficiency–performance trade-off for this dataset.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Proposes an attention architecture with value-only caching that halves cache memory and improves Transformer decoding efficiency.; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`c8e690fa03abdbe36fca73fe3582fa363710b1966e0b9ad3a2676500f8aa3c01`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
