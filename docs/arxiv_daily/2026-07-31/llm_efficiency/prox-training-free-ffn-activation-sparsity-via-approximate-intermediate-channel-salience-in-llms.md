---
title: "[论文解读] Prox: Training-Free FFN Activation Sparsity via Approximate Intermediate-Channel Salience in LLMs"
description: "[arXiv 2607.27591][LLM 效率] Prox利用低成本代理值近似SwiGLU中间状态的幅值排序来选择通道，再对入选通道执行精确计算，从而在无需训练的条件下兼顾高FFN稀疏率、模型质量与推理加速。"
arxiv_id: "2607.27591"
announcement_date: "2026-07-31"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.074571+00:00"
source_sha256: "d7f4f0c124f863ffb956e83f1ad8ab0f29610f586d64a040feee29d302e4093c"
tags:
  - "LLM 效率"
  - "LLM 其他"
  - "大语言模型推理"
  - "SwiGLU 前馈网络"
  - "激活稀疏"
  - "通道显著性"
  - "训练无关稀疏化"
  - "内存带宽"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2607.27591</p>

# Prox: Training-Free FFN Activation Sparsity via Approximate Intermediate-Channel Salience in LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Liu, Jinyi, Chen, Wei, Chen, Pengyu, Yuan, Xinyi, Bai, Minghe, Wu, Guoquan, Wei, Jun</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27591) · [PDF 下载](https://arxiv.org/pdf/2607.27591) · **关键词** 大语言模型推理, SwiGLU 前馈网络, 激活稀疏, 通道显著性, 训练无关稀疏化, 内存带宽<br>


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

Prox利用低成本代理值近似SwiGLU中间状态的幅值排序来选择通道，再对入选通道执行精确计算，从而在无需训练的条件下兼顾高FFN稀疏率、模型质量与推理加速。

**不用术语来说**：大语言模型逐词生成文本时，需要频繁从显存读取前馈网络的大量权重，因而速度和能耗常受数据搬运限制。虽然跳过当前输入下不重要的计算通道可以降低开销，但系统必须先以较小代价准确判断哪些通道重要；如果判断错误，尤其在一次跳过多数通道时，模型输出质量会明显下降。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者识别出SwiGLU中间状态是有效的通道选择信号，并进一步指出稀疏执行只需要由该状态各项幅值排名决定的掩码，无需低成本代理复原其精确数值。
- 作者提出无需训练的两阶段Prox框架：第一阶段结合输入幅值稀疏化与量化代理权重生成共享通道掩码，第二阶段使用原始权重精确计算保留通道，并将同一掩码用于三个SwiGLU投影，以抑制代理误差累积并产生实际加速机会。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型自回归解码中的前馈网络（FFN）加速。现代模型常采用 SwiGLU FFN，其上投影、门控投影和下投影包含大量参数；在小批量解码时，权重从片外高带宽内存（HBM）搬运到片上存储往往主导延迟，因此减少实际访问的权重与乘加运算具有直接价值。激活稀疏通过按当前输入动态跳过低显著性通道来实现这一目标，它与量化、静态权重剪枝不同：模型权重本身可以保持不变，而每个 token 保留的通道集合可以不同。本文聚焦无需额外训练的原生 SwiGLU 稀疏化，即不修改网络结构，也不为每个模型和层训练专用预测器。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**SwiGLU 前馈网络**

SwiGLU 用两个并行投影产生上分支激活与门控激活，再逐元素相乘形成中间状态，最后经下投影返回模型维度。其计算为 $\mathrm{FFN}(\mathbf{x})=(\mathbf{x}W_{\mathrm{up}}\odot\mathrm{SiLU}(\mathbf{x}W_{\mathrm{gate}}))W_{\mathrm{down}}$，其中 $\mathrm{SiLU}$ 是平滑门控非线性函数。

</div>
<div class="concept-item" markdown="1">

**激活稀疏**

激活稀疏根据当前输入生成二值掩码，只计算被保留的输入或输出通道，并跳过相应权重访问和乘加操作。输入稀疏可省去权重矩阵的部分行，输出稀疏可只读取并计算部分列。

</div>
<div class="concept-item" markdown="1">

**通道显著性与掩码**

通道显著性表示某个中间维度对当前 FFN 输出的重要程度，常以激活绝对值的排序近似。给定目标稀疏率后，算法保留排名靠前的通道并形成二值掩码；稀疏执行实际需要的是该索引集合，而不一定需要近似激活的精确数值。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是某一 Transformer 层 FFN 的 token 表示 $\mathbf{x}\in\mathbb{R}^{d_{\mathrm{model}}}$、预训练且保持不变的三组 SwiGLU 权重，以及指定的 FFN 稀疏预算。密集计算先得到上分支 $\mathbf{u}=\mathbf{x}W_{\mathrm{up}}$、门控分支 $\mathbf{h}=\mathrm{SiLU}(\mathbf{x}W_{\mathrm{gate}})$ 和联合中间状态 $\mathbf{s}=\mathbf{u}\odot\mathbf{h}$，再计算 $\mathbf{s}W_{\mathrm{down}}$；任务是在不训练额外预测器的条件下，提前找出 $\mathbf{s}$ 中最值得保留的中间通道，并仅对这些通道执行三次投影的必要运算。论文假设部署重点是内存带宽敏感的小批量自回归解码，并以保持原模型质量、降低 HBM 权重访问和乘加量为目标；关键难点是精确 $\mathbf{s}$ 本身需要先密集执行上投影和门控投影，因此不能直接作为低成本选择信号。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathbf{x}\in\mathbb{R}^{d_{\mathrm{model}}}$**

FFN 的输入 token 表示；$d_{\mathrm{model}}$ 是 Transformer 隐藏维度。

</div>
<div class="notation-item" markdown="1">

**$W_{\mathrm{up}},W_{\mathrm{gate}},W_{\mathrm{down}}$**

SwiGLU 的上投影、门控投影和下投影矩阵；前两者将模型维度映射到 $d_{\mathrm{ff}}$，下投影再映射回模型维度。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{u},\mathbf{h},\mathbf{s}$**

分别表示上分支激活、经 $\mathrm{SiLU}$ 的门控激活，以及二者逐元素乘积形成的 SwiGLU 中间状态。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{I}(\mathbf{m})=\{i\mid m_i=1\}$**

二值掩码 $\mathbf{m}$ 所保留的通道索引集合，用于只读取和计算相应的权重行或列。

</div>

</div>

**直接相关的工作**

- **CATS 与 COUNTDOWN**: 二者都是无需训练的原生 SwiGLU 稀疏方法，但分别仅依据密集计算得到的门控分支 $\mathbf{h}$ 或上分支 $\mathbf{u}$ 选择中间通道。由于单分支信号没有完整反映联合状态 $\mathbf{s}=\mathbf{u}\odot\mathbf{h}$，论文认为其在高稀疏率下更容易误排重要通道；同时，它们仍需密集执行其中一个投影分支。
- **TEAL**: TEAL 同时对上、门控投影的共享输入 $\mathbf{x}$ 和下投影的输入 $\mathbf{s}$ 应用输入稀疏。论文指出，第二次筛选建立在第一次稀疏化后已经近似的中间状态上，误差可能沿 FFN 累积；这与本文希望用低成本近似仅确定掩码、再对保留通道进行精确计算的设置形成直接对照。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在小批量自回归解码中，延迟主要来自将参数从片外高带宽显存搬运到片上存储。现代大语言模型的SwiGLU前馈网络含有三个大型投影矩阵，占据Transformer块的大部分参数、访存流量和乘加运算，因此，若能针对每个输入动态跳过低显著性中间通道及其关联权重和运算，就能直接缓解部署中的延迟、带宽与计算压力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于训练的激活稀疏预测器**：额外训练一个输入相关的预测模块，由它判断当前token应激活哪些FFN通道，再仅执行预测为重要的通道及相关乘加运算。
- **无需训练的激活稀疏启发式方法**：不修改或重新训练模型，而是依据激活幅值等现成统计信号直接构造通道掩码，以跳过低显著性通道；这类方法与量化、剪枝等静态压缩方向相互独立。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 基于训练的预测器必须针对每个模型分别训练，增加适配数据、训练成本和部署维护负担，难以直接扩展到不断变化的模型家族。
- 现有无需训练方法的通道选择信号在高稀疏率下不够可靠，容易错误删除重要通道并导致显著质量下降；而直接使用准确的SwiGLU中间状态虽然选择效果好，却必须先完成昂贵的稠密计算，抵消稀疏执行希望节省的访存与计算。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种无需逐模型训练、又不必先完整计算稠密SwiGLU中间状态的方法，能够以足够低的选择成本逼近精确中间状态产生的通道掩码，并让up、gate和down三个投影都真正受益于高比例稀疏化，同时避免将近似误差带入保留通道的最终数值。

</div>
<div markdown="1"><span>核心问题</span>

能否只近似SwiGLU中间状态的幅值排序而非精确数值，以低成本恢复接近精确状态的通道掩码，随后对入选通道使用原始权重精确计算，从而在无需训练的前提下实现高稀疏率、较小质量损失和端到端推理加速？

</div>
<div markdown="1"><span>作者直觉</span>

通道筛选本质上是一个排序后取舍的问题：系统只需知道哪些中间项排在前面，并不需要在筛选阶段知道每一项的精确值。因此，可用稀疏输入和低比特代理权重快速得到一个粗略中间状态；只要它大体保持真实幅值次序，就能生成相近的掩码。代理值仅负责“选谁”，入选通道再由原始权重负责“算准”，于是选择阶段可以便宜，最终保留值又不会持续携带代理近似误差。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Prox 是面向 SwiGLU 前馈网络（FFN）的免训练两阶段稀疏推理框架。输入为某层隐藏状态 $\mathbf{x}\in\mathbb{R}^{d_{\mathrm{model}}}$；第一阶段仅用保留大幅值输入坐标的稀疏向量和 INT4 代理权重，近似计算中间信号 $\tilde{\mathbf{s}}$，再按其幅值产生共享通道掩码 $\mathbf{m}_{\mathbf{s}}$；第二阶段使用原始全精度权重，只对掩码选中的中间通道精确执行 up、gate 和 down 三个投影，输出 $\mathbf{y}$。代理值不会作为激活传给后续层，因此其数值误差只可能通过“选错通道”影响结果，而不会直接累积到网络输出。

核心依据是：SwiGLU 的中间状态 $\mathbf{s}$ 同时对应 up 与 gate 投影的输出通道，以及 down 投影的输入通道；故一个共享掩码就能统一稀疏化三个投影。Prox 不试图低成本重建 $\mathbf{s}$ 的精确数值，只要求代理 $\tilde{\mathbf{s}}$ 尽量保持各通道绝对值的相对排序。通俗地说，它先用廉价草稿判断“哪些通道值得算”，再只为入选通道做原模型的精确计算。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 第一步：按幅值稀疏化层输入

构造 $[\mathbf{m}_{\mathbf{x}}]_i=\mathbf{1}[|x_i|\geq\tau_{\mathbf{x},\ell}^{s_1}]$，仅保留掩码为 $1$ 的输入坐标；阈值在标定数据上选取，使实际稀疏率近似 $s_1$。保留最大幅值坐标可在给定非零坐标数下最小化被丢弃残差的 $\ell_2$ 范数，并通过 $\|\mathbf{x}W-\mathbf{x}_{\mathrm{sp}}W\|_2\leq\|\mathbf{x}-\mathbf{x}_{\mathrm{sp}}\|_2\|W\|_2$ 控制投影扰动。

<div class="method-step__io" markdown="1">

**输入**：FFN 层 $\ell$ 的输入 $\mathbf{x}$、目标第一阶段稀疏率 $s_1$，以及离线标定的层级阈值 $\tau_{\mathbf{x},\ell}^{s_1}$。<br>
**输出**：输入掩码 $\mathbf{m}_{\mathbf{x}}$ 及隐式的稀疏输入 $\mathbf{x}_{\mathrm{sp}}=\mathbf{x}\odot\mathbf{m}_{\mathbf{x}}$。

</div>

**直观理解**：这一步优先留下绝对值大的输入分量，因为它们通常携带更多信号能量。它不是删除输出通道，而是用更少输入坐标粗略估计所有中间通道的重要性。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 第二步：构造低成本中间状态代理

仅沿 $\mathbf{m}_{\mathbf{x}}$ 保留的输入坐标执行两个代理投影，得到 $\tilde{\mathbf{u}}$ 与经 SiLU 激活的 $\tilde{\mathbf{h}}$，随后计算 $\tilde{\mathbf{s}}=\tilde{\mathbf{u}}\odot\tilde{\mathbf{h}}$。代理路径同时利用输入稀疏性和低比特权重，且不把 $\tilde{\mathbf{s}}$ 作为真实 FFN 激活向下传播。

<div class="method-step__io" markdown="1">

**输入**：原始输入 $\mathbf{x}$、输入掩码 $\mathbf{m}_{\mathbf{x}}$，以及由原 up、gate 权重生成的量化代理权重 $\widetilde W_{\mathrm{up}}$ 和 $\widetilde W_{\mathrm{gate}}$。<br>
**输出**：覆盖全部 $d_{\mathrm{ff}}$ 个中间通道的近似重要性信号 $\tilde{\mathbf{s}}$。

</div>

**直观理解**：代理计算像低清预览：数值不必精确，只要大致排对哪些通道更重要。由于预览结果只用于做选择，量化误差和输入截断误差不会直接成为下一层的输入。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 第三步：生成共享中间通道掩码

按 $[\mathbf{m}_{\mathbf{s}}]_j=\mathbf{1}[|\tilde{s}_j|\geq\tau_{\mathbf{s},\ell}^{s_2}]$ 选择活跃中间通道，阈值在标定数据上固定，以近似达到 $s_2$。同一 $\mathbf{m}_{\mathbf{s}}$ 同时约束 up、gate 的输出通道和 down 的输入通道。

<div class="method-step__io" markdown="1">

**输入**：代理中间状态 $\tilde{\mathbf{s}}$、目标第二阶段稀疏率 $s_2$，以及离线标定的阈值 $\tau_{\mathbf{s},\ell}^{s_2}$。<br>
**输出**：共享二值掩码 $\mathbf{m}_{\mathbf{s}}\in\{0,1\}^{d_{\mathrm{ff}}}$。

</div>

**直观理解**：这里真正需要的是“入选名单”，而不是代理激活的精确值。共享名单保证三个投影在同一组中间坐标上工作，避免各自选择导致维度不一致。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 第四步：对入选通道执行精确稀疏 SwiGLU

使用原始权重仅计算 $\mathbf{m}_{\mathbf{s}}$ 选中的 up 与 gate 输出，形成精确稀疏中间状态 $\mathbf{s}_{\mathrm{sp}}$；随后仅从 $W_{\mathrm{down}}$ 读取相应行并完成输入稀疏投影。未选通道不产生乘加和权重访存。

<div class="method-step__io" markdown="1">

**输入**：原输入 $\mathbf{x}$、共享掩码 $\mathbf{m}_{\mathbf{s}}$，以及原模型的 $W_{\mathrm{up}}$、$W_{\mathrm{gate}}$ 和 $W_{\mathrm{down}}$。<br>
**输出**：FFN 输出 $\mathbf{y}$；其保留通道上的激活由原模型权重精确计算。

</div>

**直观理解**：廉价阶段只决定算谁，昂贵阶段则把入选者算准。这样既避免完整计算全部中间通道，也避免把近似激活直接送入模型所造成的误差传播。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 两阶段代理选择与精确稀疏执行

$$
\begin{aligned}
\tilde{\mathbf{u}}&=\Pi^{\mathrm{in}}(\mathbf{x},\widetilde W_{\mathrm{up}},\mathbf{m}_{\mathbf{x}}),\\
\tilde{\mathbf{h}}&=\mathrm{SiLU}\!\left(\Pi^{\mathrm{in}}(\mathbf{x},\widetilde W_{\mathrm{gate}},\mathbf{m}_{\mathbf{x}})\right),\\
\tilde{\mathbf{s}}&=\tilde{\mathbf{u}}\odot\tilde{\mathbf{h}},\qquad
[\mathbf{m}_{\mathbf{s}}]_j=\mathbf{1}\!\left[|\tilde{s}_j|\geq\tau_{\mathbf{s},\ell}^{s_2}\right],\\
\mathbf{u}_{\mathrm{sp}}&=\Pi^{\mathrm{out}}(\mathbf{x},W_{\mathrm{up}},\mathbf{m}_{\mathbf{s}}),\\
\mathbf{h}_{\mathrm{sp}}&=\mathrm{SiLU}\!\left(\Pi^{\mathrm{out}}(\mathbf{x},W_{\mathrm{gate}},\mathbf{m}_{\mathbf{s}})\right),\\
\mathbf{s}_{\mathrm{sp}}&=\mathbf{u}_{\mathrm{sp}}\odot\mathbf{h}_{\mathrm{sp}},\qquad
\mathbf{y}=\Pi^{\mathrm{in}}(\mathbf{s}_{\mathrm{sp}},W_{\mathrm{down}},\mathbf{m}_{\mathbf{s}}).
\end{aligned}
$$

**符号说明**

- $\mathbf{x}$：当前 FFN 层的输入隐藏状态。
- $\mathbf{m}_{\mathbf{x}}$：按输入绝对值阈值产生的二值输入坐标掩码。
- $\widetilde W_{\mathrm{up}},\widetilde W_{\mathrm{gate}}$：第一阶段使用的量化 up 与 gate 代理权重。
- $\Pi^{\mathrm{in}}$：按给定掩码跳过输入坐标的输入稀疏投影算子。
- $\Pi^{\mathrm{out}}$：只计算给定掩码所指定输出通道的输出稀疏投影算子。
- $\tilde{\mathbf{u}},\tilde{\mathbf{h}},\tilde{\mathbf{s}}$：代理 up 激活、代理 gate 激活及其逐元素乘积形成的代理中间状态。
- $\mathrm{SiLU}$：SwiGLU gate 分支使用的 SiLU 非线性激活函数。
- $\odot$：逐元素乘法。
- $\mathbf{m}_{\mathbf{s}}$：根据代理中间状态幅值选出的共享中间通道掩码。
- $\tau_{\mathbf{s},\ell}^{s_2}$：层 $\ell$ 在目标第二阶段稀疏率 $s_2$ 下离线标定的中间状态阈值。
- $j$：中间通道索引，取值从 1 到 $d_{\mathrm{ff}}$。
- $\mathbf{1}[\cdot]$：条件成立时为 1、否则为 0 的指示函数。
- $W_{\mathrm{up}},W_{\mathrm{gate}},W_{\mathrm{down}}$：原模型用于第二阶段精确计算的 up、gate 和 down 权重。
- $\mathbf{u}_{\mathrm{sp}},\mathbf{h}_{\mathrm{sp}},\mathbf{s}_{\mathrm{sp}}$：仅在入选中间通道上精确计算的 up 激活、gate 激活和 SwiGLU 中间状态。
- $\mathbf{y}$：稀疏 FFN 的最终输出。

<div class="equation-explanation" markdown="1">

**直观理解**：等式前半部分以便宜的稀疏、量化计算生成通道名单，后半部分则丢弃代理数值，改用原权重精确重算名单内的通道。其关键不是让 $\tilde{\mathbf{s}}$ 接近 $\mathbf{s}$ 的每个数值，而是让由二者幅值排序产生的高重要性通道集合尽量一致。<br>
**原文位置**：第 4.1 节“Two-Stage Sparse Inference”；代理计算、通道阈值公式及 Stage 2 精确稀疏计算公式。

</div>

</div>

<div class="equation-block" markdown="1">

#### 两阶段归一化成本与有效稀疏率

$$
\begin{aligned}
C_{\mathrm{Dense}}&=3,\\
C_{\mathrm{Prox}}&=2\alpha(1-s_1)+3(1-s_2),\\
e&=1-\frac{C_{\mathrm{Prox}}}{C_{\mathrm{Dense}}}=s_2-\frac{2\alpha(1-s_1)}{3}.
\end{aligned}
$$

**符号说明**

- $C_{\mathrm{Dense}}$：稠密 SwiGLU FFN 的归一化成本；up、gate、down 三个投影各计一个单位，因此总计 3。
- $C_{\mathrm{Prox}}$：Prox 两阶段合计的归一化计算成本。
- $\alpha$：一次量化代理投影相对于一次完整全精度稠密投影的单位成本比例。
- $s_1$：第一阶段输入坐标稀疏率，故代理投影处理的输入比例为 $1-s_1$。
- $s_2$：第二阶段中间通道稀疏率，故三个精确投影处理的通道比例为 $1-s_2$。
- $e$：相对于稠密 FFN 总成本定义的目标有效稀疏率。

<div class="equation-explanation" markdown="1">

**直观理解**：第一阶段有两个低成本代理投影，第二阶段有三个按通道缩减的全精度投影，因此不能把 $s_2$ 直接视为整个 FFN 的实际节省比例；代理筛选本身也消耗计算。该关系把代理开销纳入统一预算，使不同 $(s_1,s_2)$ 组合能在相同目标 $e$ 下公平比较。<br>
**原文位置**：第 4.2 节“Sparsity Allocation between Two Stages”，归一化成本和有效稀疏率公式。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：Prox 是 training-free 方法，不更新原模型参数，也没有通过梯度最小化的训练损失。离线过程仅在标定数据上确定各层输入阈值 $\tau_{\mathbf{x},\ell}^{s_1}$ 和中间代理阈值 $\tau_{\mathbf{s},\ell}^{s_2}$，并从原 FP16 权重构造量化代理；这些步骤属于推理配置与统计标定，而非模型训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 排序保持型代理路径**

代理路径组合幅值输入稀疏和对称逐行 INT4 权重量化，计算 $\tilde{\mathbf{s}}$ 仅用于估计 $|\mathbf{s}|$ 的通道排序。若代理扰动只改变远离选择阈值的数值而不跨越阈值，最终掩码不变，模型输出也不会受到该代理误差影响。

> 直观理解：该模块的目标不是模仿每个真实激活值，而是尽可能选出相同的高重要性通道。因而它可以比普通近似推理更激进地压缩计算和权重。

**2. 共享中间通道掩码与误差隔离**

SwiGLU 中 $\mathbf{s}=\mathbf{u}\odot\mathbf{h}$ 的第 $j$ 项是 down 投影第 $j$ 行的系数，因此 $|s_j|$ 可作为该通道输出贡献的自然指标。Prox 用代理产生的单个 $\mathbf{m}_{\mathbf{s}}$ 同时制造 up、gate 的输出稀疏和 down 的输入稀疏，并在第二阶段重新计算精确激活。

> 直观理解：同一个中间索引贯穿三个投影，所以一张名单即可同时减少三处工作量。重新精算入选通道把近似误差限制在“是否入选”这一处，而不是让近似数值贯穿网络。

**3. 面向解码的融合稀疏内核**

第一阶段使用融合 split-$N$ CUDA 内核共同计算 up 与 gate 代理投影，共享隐藏状态读取，在寄存器中解包 INT4，并直接形成和阈值化 $\tilde{\mathbf{s}}$，避免存储两份独立 FP16 代理向量。第二阶段用融合输出稀疏内核完成精确 up、gate 与 SwiGLU，再以输入稀疏 GEMV 完成 down 投影，掩码检查位于主计算循环内。

> 直观理解：算法上的零值只有在硬件真正跳过权重读取和乘加时才会带来速度收益。融合内核还减少了中间张量写回和重复读取，适配单批次自回归解码这一通常受内存带宽限制的场景。

**训练与推理**

部署前，首先由原始 $W_{\mathrm{up}}$ 和 $W_{\mathrm{gate}}$ 构造对称逐行 INT4 代理权重，并在标定数据上为各层及各目标稀疏工作点确定输入和中间通道阈值。随后根据目标有效稀疏率 $e$ 分配 $(s_1,s_2)$：以 $s_2=0.7$ 为初始锚点，由成本模型求 $s_1$，将其限制在 $[0,0.7]$ 内，必要时调整 $s_2$；阈值和代理权重在在线推理期间保持固定。

逐 token 解码时，每个 FFN 层先阈值化 $\mathbf{x}$，用稀疏输入和 INT4 代理权重生成 $\tilde{\mathbf{s}}$，再阈值化得到 $\mathbf{m}_{\mathbf{s}}$。之后立即丢弃代理激活，使用原模型权重精确计算入选的 up、gate 通道及对应 down 投影，得到 $\mathbf{y}$；因此原模型无需微调，代理权重也不替代第二阶段的正式权重。

**复现信息**

公平解释性能时需注意，Prox 的速度收益不仅来自逻辑稀疏率，还依赖专用内核是否真正减少权重访存和乘加。文中面向单批次自回归解码实现 CUDA 与 Triton 内核：第一阶段融合 up、gate 代理投影，INT4 在寄存器中解包，局部和以 FP32 归约，并直接完成 SwiGLU、幅值阈值化与掩码生成；第二阶段融合精确 up、gate 和 SwiGLU，再以输入稀疏 GEMV 执行 down 投影。代理权重常驻 GPU 显存，内核启动形状和归约策略会针对 GPU 架构、矩阵形状与稀疏区间自动调优；这些设计是把算法稀疏转化为实际解码加速所必需的，而非改变模型质量的训练技巧。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 下游能力评测由 EleutherAI LM Harness 执行，包含六项任务：8-shot GSM8K 测试数学推理，5-shot MMLU 测试多学科知识，10-shot HellaSwag 测试常识补全，zero-shot ARC-Easy、25-shot ARC-Challenge 测试科学问答，zero-shot PIQA 测试物理常识。实验覆盖 Qwen3、Qwen3.5、Ministral、Mistral、Llama-3 和 Gemma-3 的十个模型；前五类主要检验 SwiGLU FFN，Gemma-3 用于检验向 GeGLU FFN 的泛化。具体数据划分与样本数原文未明确报告。
- WikiText 用于测量量化 Qwen3-8B 在不同 FFN 稀疏率下的困惑度，覆盖 AWQ、FP8、W4A16 和 W8A8 四种量化配置。它检验 Prox 与低比特模型权重结合后是否仍能保持语言建模质量；具体 WikiText 版本、划分和样本规模原文未明确报告。
- LongBench 与 RULER 用于测试 Qwen3-8B 在 16K 和 32K 上下文长度下的长上下文准确率。实验将 $60\%$ FFN 稀疏的 Prox 分别接入 RocketKV 和 HShare，考察 FFN 稀疏与稀疏注意力的兼容性；具体任务子集、样本数及聚合方式原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**六项下游任务聚合分数**

汇总 GSM8K、MMLU、HellaSwag、ARC-Easy、ARC-Challenge 和 PIQA 的任务表现，用于衡量稀疏化后的综合能力保持程度。原文未明确说明具体归一化或聚合公式。 （越高越好，因为更高分数表示稀疏推理后保留了更多下游任务能力。）

</div>
<div class="metric-item" markdown="1">

**困惑度**

衡量模型对 WikiText 文本序列的预测不确定性，用于检测量化与 FFN 稀疏叠加后的语言建模退化。 （越低越好，因为较低困惑度表示模型为真实文本赋予了更高概率。）

</div>
<div class="metric-item" markdown="1">

**解码吞吐量与相对加速比**

吞吐量以 tokens/s 表示，相对加速比以稠密模型为 $1.00\times$，衡量单批次自回归解码的端到端效率；长上下文实验同时报告 LongBench/RULER 准确率，以检查速度提升对应的质量代价。 （吞吐量和加速比越高越好，但必须结合准确率或下游分数判断，避免把严重质量退化误认为有效加速。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 十个模型、六项下游任务，比较 Prox 与 TEAL 在 $50\%$、$60\%$ 和 $70\%$ FFN 模块级稀疏率下的聚合分数。

<div class="result-value" markdown="1">

作者报告：在 $50\%$ 稀疏率下，Prox 在十个模型中的八个上超过 TEAL；在 $60\%$ 和 $70\%$ 下，Prox 在全部十个模型上均超过 TEAL。表 1 还显示，Prox 在 Qwen3-8B 上从稠密分数 76.1 降至 $70\%$ 稀疏时的 68.6，而 TEAL 为 63.3；在 Gemma3-12B 上，Prox 在 $70\%$ 时为 74.8，TEAL 为 62.0。

</div>

该结果直接支持 Prox 的核心质量主张：高稀疏率下，仅用低成本代理确定掩码、再精确计算入选通道，比把代理激活直接用于 FFN 输出更稳健；Gemma-3 的结果也说明这种策略并非只适用于 SwiGLU。不过，聚合分数会掩盖单项任务差异，且实验只覆盖指定的十个模型，不能证明对所有模型架构或任务都成立。

<div class="result-source" markdown="1">

来源：第 5.1 节“Downstream accuracy”及表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Specifically, Prox surpasses TEAL on 8 out of 10 evaluated models at 50% sparsity and consistently outperforms it across all 10 models at 60% and 70% sparsity.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### NVIDIA A6000 上的单批次端到端自回归解码，FFN 稀疏率为 $60\%$ 至 $70\%$。

<div class="result-value" markdown="1">

Prox 在该区间取得 $1.51\times$ 至 $1.99\times$ 的端到端加速。在 $70\%$ 稀疏率下，Prox 与 TEAL 的吞吐量差距在所有受测模型上不超过 $2.9\%$，但 Prox 的平均下游任务表现高出 $14.4\%$。

</div>

这说明 Prox 的第二阶段精确重算并未抵消稀疏计算带来的系统收益：其速度与更激进复用近似激活的 TEAL 基本接近，但质量明显更高。该结果只证明特定内核、单 batch 和所测 GPU 上的解码收益；不能直接外推到大批量服务、训练、提示预填充或其他硬件。

<div class="result-source" markdown="1">

来源：第 5.1 节“End-to-end decoding speedup”及图 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At 70% sparsity, Prox differs from TEAL in throughput by no more than 2.9% across all evaluated models and improves the average downstream task performance by 14.4%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen3-8B 在 16K 和 32K 上下文中，将 $60\%$ FFN 稀疏的 Prox 与 RocketKV 稀疏注意力组合。

<div class="result-value" markdown="1">

RocketKV 单独使用时，16K/32K 吞吐量分别为 40.7/41.0 tokens/s，即 $1.23\times$/$1.72\times$；加入 Prox 后提高到 63.6/62.5 tokens/s，即 $1.92\times$/$2.62\times$。LongBench/RULER 的相对准确率由 100.0/100.0 变为 96.6/98.0。

</div>

该组合结果表明 FFN 稀疏与注意力稀疏可作用于不同模块，因而能够叠加节省计算；在 32K 上下文中组合加速尤其明显。与此同时，LongBench 和 RULER 分别出现 $3.4$ 与 $2.0$ 个相对点的下降，因此“兼容”应理解为速度收益较大且质量大体保留，而不是完全无损；单一模型和两个后端也不足以证明普遍兼容。

<div class="result-source" markdown="1">

来源：表 2，RocketKV + Prox 行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

RocketKV + Prox 63.6 (1.92×) 62.5 (2.62×) 96.6 / 98.0

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前实现面向延迟敏感的单批次自回归解码，尚不支持高效的大批量服务；因此图 5 的端到端加速不能直接代表数据中心常见的多请求批处理吞吐量。
- Stage 1 的 INT4 代理权重需要常驻 GPU 显存，带来约 $12\%$ 的权重存储开销。作者提出未来可按 Transformer 层采用滑动窗口式加载与驱逐，但本文尚未验证该方案的延迟、带宽和质量影响。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Dense：不进行 FFN 稀疏化的原模型，提供质量和吞吐量参考点，用于判断加速来自多少精度代价。
- CATS：无需训练的激活稀疏方法，只对部分 FFN 投影进行稀疏化。它代表依据较简化通道信号进行选择的方法，可检验 Prox 在高稀疏率下是否具有更稳健的通道筛选能力。
- M-COUNTDOWN：作者采用的 COUNTDOWN 变体，因为其在实际推理条件下的平均下游分数高于 D-COUNTDOWN。它同样属于无需训练的 FFN 激活稀疏基线，但受限于仅稀疏两个 FFN 矩阵。
- TEAL：对三个 FFN 投影进行稀疏化，并直接复用稀疏近似的中间状态参与后续计算。它与 Prox 最接近，关键差异是 TEAL 让代理误差进入最终激活，而 Prox 仅用代理值选通道，再精确重算入选通道。

**实验想回答的问题**

- 在相同的 FFN 模块级稀疏预算下，Prox 能否比 CATS、COUNTDOWN 和 TEAL 更可靠地保留多种大语言模型的下游任务能力，尤其是在 $60\%$ 至 $70\%$ 的高稀疏区间？
- Prox 的质量优势能否转化为真实的端到端解码加速，并与模型量化、RocketKV 或 HShare 等稀疏注意力技术组合，而不造成不可接受的困惑度或长上下文准确率损失？

**实验实现**

公平性方面，所有方法仅应用于 FFN 投影，并统一报告 FFN 模块级有效稀疏率。CATS 与 COUNTDOWN 的投影级稀疏率 $k$ 被换算为模块级有效稀疏率 $2k/3$；TEAL 取三个 FFN 投影稀疏率的平均值；Prox 按论文第 4.2 节的成本模型换算。Stage 1 的 INT4 与 FP16 GEMV 成本系数设为 $\alpha=1/3$，这是依据三种 GPU、四种 Qwen3 规模上的实测延迟比范围选取的统一近似值，而不是仅按位宽采用理论值 $0.25$。对似然型任务，作者在完整序列上启用稀疏化，使隐藏状态全程受到稀疏计算影响；对 GSM8K 等生成任务，提示预填充保持稠密，仅稀疏解码阶段。端到端速度采用 NVIDIA A6000、batch size 为 1 的解码测试；附录另报告 A100 与 RTX 3090。量化兼容性在 Qwen3-8B 上测试 AWQ、FP8、W4A16 和 W8A8；稀疏注意力兼容性在 Qwen3-8B、16K/32K 上测试 RocketKV 与 HShare。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| A1 将 Stage 1 的 INT4 代理权重替换为 FP16，并在相同目标计算预算下重新分配两阶段计算量。 | A1 在八个模型—稀疏率设置中均低于 Prox；在 $70\%$ 稀疏率下，Qwen3-8B 和 Qwen3-14B 分别落后 9.0 与 4.7 分。表 3 中对应分数为：Qwen3-8B 的 Prox/A1 为 68.6/59.6，Qwen3-14B 为 74.8/70.1。 | 该消融隔离的是代理权重精度与预算分配之间的权衡。FP16 代理的单次估计可能更精确，但成本更高，固定总预算下会挤压候选覆盖或精确计算，因此整体质量反而下降。它支持使用 INT4 代理的工程选择，但不能推出低精度在任何预算或硬件上都必然更优。 | 第 5.2 节“A1: Effect of proxy-weight precision”及表 3<br><span class="experiment-evidence">As Table 3 shows, A1 consistently underperforms Prox across all eight settings, with performance deficits reaching 9.0 and 4.7 points at 70% sparsity on Qwen3-8B and Qwen3-14B, respectively.</span> |
| A3 保留 Prox 的其余设置，但删除 Stage 2 的精确计算，直接将入选通道的量化代理值送入下投影。 | Prox 在全部设置中均超过 A3；在 $70\%$ 稀疏率下，Qwen3-8B 与 Qwen3-14B 的差距分别达到 24.3 和 18.1 分。表 3 中 Prox/A3 分别为 68.6/44.3 和 74.8/56.7。 | 这是最直接验证核心机制的消融：通道集合保持由代理选出，只改变入选通道最终使用代理值还是精确值。巨大差距说明代理值适合做相对重要性排序，却不足以替代真实激活参与输出计算；因此 Stage 2 不是可有可无的精度修补，而是高稀疏率稳定性的关键来源。 | 第 5.2 节“A3: Necessity of exact computation”及表 3<br><span class="experiment-evidence">Prox outperforms A3 across all settings, with performance gaps reaching 24.3 points on Qwen3-8B and 18.1 points on Qwen3-14B at 70% sparsity.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Proposes training-free FFN activation sparsification to accelerate LLM decoding while preserving model quality.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`d7f4f0c124f863ffb956e83f1ad8ab0f29610f586d64a040feee29d302e4093c`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
