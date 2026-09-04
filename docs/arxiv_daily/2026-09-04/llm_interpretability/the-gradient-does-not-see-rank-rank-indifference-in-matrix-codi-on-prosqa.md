---
title: "[论文解读] The Gradient Does Not See Rank: Rank-Indifference in Matrix-CODI on ProsQA"
description: "[arXiv 2609.03090][LLM 机制与可解释性] 原文未明确报告。"
arxiv_id: "2609.03090"
announcement_date: "2026-09-04"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:36:17.906643+00:00"
source_sha256: "d7e6730564fd7b18bb466ab79a56ad60b4c2c43e182e1187d7e00bfd3914631a"
tags:
  - "LLM 机制与可解释性"
  - "LLM Reasoning"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2609.03090</p>

# The Gradient Does Not See Rank: Rank-Indifference in Matrix-CODI on ProsQA

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Samuel Larson</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Pebble ML</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03090v1) · [PDF 下载](https://arxiv.org/pdf/2609.03090v1) · **关键词** LLM 机制与可解释性<br>


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

本文位于连续思维链（continuous chain-of-thought, CoT）与机制可解释性研究的交叉领域。连续 CoT 不生成可读的逐步推理文本，而是把推理压缩为若干反馈到 Transformer 残差流中的连续潜在位置；CODI 通过教师模型的显式推理状态来蒸馏学生模型，使学生仅凭输入、连续潜在位置和答案完成任务。本文研究的是 matrix-CODI：每个潜在位置不直接沿普通向量通道反馈，而是先变换为矩阵潜变量 $Z$，再读回隐藏状态；矩阵的秩因此成为单个样本上可计算的结构指标。核心背景假设是：若不同奇异方向分别承载并行推理路径，那么保留低秩近似应破坏需要多条路径的推理，从而降低准确率。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**连续思维链与知识蒸馏**

连续思维链用不可直接阅读的向量或潜在位置表示推理步骤，而不是输出文字化的中间过程。知识蒸馏中，教师模型先看到提示、显式思维链和答案，学生模型再通过隐藏状态损失与答案预测损失学习教师状态。

</div>
<div class="concept-item" markdown="1">

**矩阵秩与奇异值分解**

矩阵的秩可理解为其中相互独立的方向数量；奇异值分解把矩阵写成若干方向及其强度的组合。秩-$k$ 截断只保留强度最大的 $k$ 个方向，因此可以检验模型是否真正使用了多个矩阵方向。

</div>
<div class="concept-item" markdown="1">

**消融实验与有效秩**

消融实验在推理时有意删除或替换某种结构，再观察性能是否下降，以判断该结构是否具有功能作用。有效秩不是稠密矩阵的严格数值秩，而是由归一化奇异值分布计算出的平滑指标，用来描述谱能量实际分布在多少个方向上。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是 GPT-2 small 上的 matrix-CODI 潜在推理系统，隐藏状态维度为 $D=768$，每个样本使用六个连续潜在位置，矩阵边长为 $d=16$。给定 ProsQA 的提示，学生模型将前一步隐藏状态 $h\in\mathbb{R}^{D}$ 映射为 $d\times d$ 矩阵 $Z$，再将其读回 $D$ 维状态并反馈为下一潜在位置，最终输出唯一正确答案。训练同时包含答案下一个词交叉熵损失和教师—学生隐藏状态的 $L_1$ 蒸馏损失；论文要检验的具体假设是：如果 $Z$ 的不同奇异方向表示并行推理路径，那么推理时把 $Z$ 截断到较低秩 $k$ 应在需要多个组成部分的任务上显著降低准确率。ProsQA 是一个合成蕴含任务：实体构成菱形有向无环图，问题询问哪个叶实体具有性质 $P$，每题有唯一正答案和一个干扰项。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$h\in\mathbb{R}^{D}$**

前一潜在步骤的 $D$ 维隐藏状态；本文中 $D=768$。

</div>
<div class="notation-item" markdown="1">

**$Z\in\mathbb{R}^{d\times d}$**

由隐藏状态升维并重排得到的矩阵潜变量；本文中 $d=16$。

</div>
<div class="notation-item" markdown="1">

**$Z_k$**

对 $Z$ 做奇异值分解后仅保留前 $k$ 个奇异方向得到的秩-$k$ 截断矩阵，用于推理时消融。

</div>
<div class="notation-item" markdown="1">

**$H_{\mathrm{eff}}(Z)$**

矩阵 $Z$ 的有效秩，即根据归一化奇异值分布计算的谱复杂度指标；数值越大表示谱能量越分散到更多方向。

</div>

</div>

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

连续思维链模型试图把显式文字推理压缩为少量连续潜在标记，以降低推理过程的表示和计算成本。矩阵化的连续思维链进一步把每个潜在标记表示为矩阵 $Z$，因此可以用奇异值分解得到的秩作为单样本结构指标。若矩阵中的不同奇异方向确实对应并行推理路径，那么理解秩是否承载推理功能，对于判断这类模型究竟是在并行组织推理，还是仅利用矩阵作为普通的中间参数，具有科学意义。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **连续思维链与潜在推理路径**：COCONUT 和 CODI 等方法不再把每一步推理输出为文字，而是将显式推理压缩为连续潜在标记，并把这些标记反馈到 Transformer 的残差流中，最后从模型状态预测答案。相关理论认为，多个推理路径可以以叠加形式存储在潜在表示中，从而在较短的连续序列中进行并行搜索。
- **矩阵瓶颈与秩消融分析**：matrix-CODI 将 $768$ 维潜在状态投影为 $d^2$ 个数，重排为矩阵 $Z\th-dimensional?{}$，再读回原维度并反馈给模型。研究者在推理时把 $Z$ 截断为秩 $k$ 的近似矩阵，观察准确率随 $k$ 的变化；如果较高秩代表更多必要的推理成分，降低 $k$ 应导致性能下降。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- “潜在表示包含并行推理路径”的理论解释并不自动意味着矩阵秩能够计数这些路径。只有当特征与 $Z$ 的奇异方向对齐，且训练目标奖励这种对齐时，秩才可能成为功能性指标；此外，彼此夹角较小的多个特征可以叠加而不必产生同等数量的秩。
- 既有证据主要依赖潜在标记是否存在或秩截断后准确率是否下降，难以区分“模型不使用秩”与“模型根本不依赖被干预的位置”。因此，即使秩消融曲线平坦，也不能单独证明秩对推理没有作用；同时，已有工作对连续思维链的“超位置性”提出了挑战，但尚未直接检验训练损失是否塑造了可被读取的秩结构。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚未解决的问题是：在矩阵瓶颈的实际训练中，秩是否被优化目标塑造成推理所依赖的功能变量，还是仅作为模型可以任意形成、却不会影响答案的结构属性。尤其缺少能够同时检验不同读出函数、不同随机种子以及位置相关负对照的直接证据。

</div>
<div markdown="1"><span>核心问题</span>

在 matrix-CODI 中，矩阵潜变量 $Z$ 的秩是否编码了答案预测所需的并行推理信息，以至于将 $Z$ 截断为较低秩会系统性降低任务准确率？

</div>
<div markdown="1"><span>作者直觉</span>

如果秩代表独立的推理成分，那么保留少数奇异方向应删除部分必要信息，准确率应随保留秩增加而上升；反之，若答案信息集中在少数与秩无关的方向，或读出过程对秩不敏感，秩截断曲线就会近似平坦。作者因此不仅改变秩，还比较非线性读出并观察不同种子是否形成不同秩，从而把“秩不重要”与“干预位置不重要”区分开来。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法将传统的连续思维链蒸馏扩展为矩阵瓶颈：模型把前一步隐藏状态 $h\in\mathbb{R}^{D}$ 映射为矩阵潜变量 $Z\in\mathbb{R}^{d\times d}$，再将 $Z$ 读出为下一步所需的隐藏状态。训练时同时使用教师隐藏状态蒸馏损失和答案的下一词元交叉熵；推理时对 $Z$ 做奇异值分解并保留前 $k$ 个奇异方向，以检验矩阵秩是否承载多个可用的推理成分。直观地说，模型先把连续思考写入一个小矩阵，再把矩阵还原成语言模型可继续处理的向量；研究者随后人为删掉矩阵中的低优先级方向，观察答案是否受损。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 教师轨迹与学生输入构造

教师前向计算在指定冒号词元位置产生参考隐藏状态；学生不读取显式链式思维，而是在每个连续潜在位置把前一步隐藏状态反馈为下一步输入嵌入。

<div class="method-step__io" markdown="1">

**输入**：教师侧的 prompt、显式链式思维和答案；学生侧的 prompt、固定数量的连续潜在位置和答案。<br>
**输出**：教师参考隐藏状态、学生的连续潜变量序列以及用于答案预测的学生隐藏状态。

</div>

**直观理解**：教师像先完整写出解题草稿，学生则把草稿压缩成若干不可直接阅读的连续记忆槽，再依次利用这些槽完成答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 矩阵瓶颈生成

先用 $W_{\mathrm{up}}\in\mathbb{R}^{d^{2}\times D}$ 将向量投影到 $d^{2}$ 维并重排为 $Z\in\mathbb{R}^{d\times d}$；可选的 thinker 对 $Z$ 做矩阵变换，随后通过读出函数得到 $h_{\mathrm{out}}=\operatorname{LayerNorm}(\phi(Z))$。默认读出为展平后线性投影 $\phi(Z)=W_{\mathrm{down}}\operatorname{vec}(Z)$。

<div class="method-step__io" markdown="1">

**输入**：前一步潜在隐藏状态 $h\in\mathbb{R}^{D}$，其中实验设定为 GPT-2 small 的 $D=768$。<br>
**输出**：下一步反馈使用的隐藏状态 $h_{\mathrm{out}}$，以及可被单独分析结构的矩阵潜变量 $Z$。

</div>

**直观理解**：这一步把一条向量记忆改造成一个方阵，使研究者能够讨论矩阵中有多少独立方向；读出阶段再把方阵恢复成语言模型熟悉的向量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 联合训练

优化总损失 $L=\gamma L_{\mathrm{kd}}+L_{\mathrm{ce}}$，其中 $L_{\mathrm{kd}}$ 对齐学生与教师的隐藏状态，$L_{\mathrm{ce}}$ 训练标准下一词元预测。

<div class="method-step__io" markdown="1">

**输入**：学生的答案预测、学生在答案冒号位置的隐藏状态，以及教师对应的参考隐藏状态。<br>
**输出**：训练完成的矩阵-CODI 模型及其在各潜在位置产生的矩阵 $Z$。

</div>

**直观理解**：优化同时要求学生的内部表示像教师，并且最终答案正确；因此矩阵不只是被迫模仿内部状态，也必须支持实际输出。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 秩干预与功能检验

计算 $Z=U\Sigma V^{\top}$，用前 $k$ 个奇异值及对应方向构造 $Z_k$，再将 $Z_k$ 而非原始 $Z$ 输入读出函数；比较不同 $k$ 下的答案准确率，并用有效秩 $H_{\mathrm{eff}}(Z)$ 描述训练过程中谱分布的平滑变化。

<div class="method-step__io" markdown="1">

**输入**：训练后推理过程中的矩阵 $Z$，以及候选秩 $k$。<br>
**输出**：秩截断准确率曲线、有效秩统计，以及关于秩是否具有功能作用的证据。

</div>

**直观理解**：相当于逐步关闭矩阵中的独立信息通道：如果高秩确实表示并行推理，保留很少方向应使准确率下降；若曲线平坦，则秩可能没有被模型使用，或该干预本身没有改变真正有用的位置。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 矩阵瓶颈与默认读出

$$
\begin{aligned}\operatorname{flat}&=W_{\mathrm{up}}h,\quad W_{\mathrm{up}}\in\mathbb{R}^{d^{2}\times D},\\Z&=\operatorname{reshape}(\operatorname{flat};d,d)\in\mathbb{R}^{d\times d},\\Z&\leftarrow (I+\Delta(Z))Z(I+\Gamma(Z))\quad\text{(optional thinker)},\\h_{\mathrm{out}}&=\operatorname{LayerNorm}(\phi(Z)),\quad \phi(Z)=W_{\mathrm{down}}\operatorname{vec}(Z),\quad W_{\mathrm{down}}\in\mathbb{R}^{D\times d^{2}}.\end{aligned}
$$

**符号说明**

- $h$：前一步的潜在隐藏状态，维度为 $D$。
- $D$：语言模型隐藏状态维度；本文 GPT-2 small 中为 $768$。
- $d$：矩阵边长；实验中固定为 $16$。
- $W_{\mathrm{up}}$：把 $D$ 维隐藏状态投影到 $d^{2}$ 维的上投影矩阵。
- $Z$：矩阵潜变量，承载一个连续潜在推理位置的信息。
- $\Delta,\Gamma$：可选 thinker 中对矩阵左右两侧进行调制的函数或变换；摘录未进一步说明其具体参数化。
- $\phi$：把矩阵潜变量读出为 $D$ 维向量的函数。
- $\operatorname{vec}(Z)$：将矩阵 $Z$ 展平为长度为 $d^{2}$ 的向量。
- $W_{\mathrm{down}}$：将展平矩阵投影回模型隐藏维度 $D$ 的下投影矩阵。

<div class="equation-explanation" markdown="1">

**直观理解**：这组变换定义了从普通隐藏状态到矩阵记忆、再回到语言模型隐藏状态的完整通路。矩阵结构的意义在于，它不仅保存数值内容，还允许用秩描述信息是否集中在少数独立方向上。<br>
**原文位置**：第 2.1 节“Matrix bottleneck”

</div>

</div>

<div class="equation-block" markdown="1">

#### 联合训练目标

$$
L=\gamma L_{\mathrm{kd}}+L_{\mathrm{ce}}
$$

**符号说明**

- $L$：训练时最小化的总损失。
- $\gamma$：隐藏状态蒸馏损失的权重。摘录未报告其具体数值。
- $L_{\mathrm{kd}}$：知识蒸馏损失；本文描述为学生与教师指定位置隐藏状态之间的 L1 损失。
- $L_{\mathrm{ce}}$：答案下一词元预测的标准交叉熵损失。

<div class="equation-explanation" markdown="1">

**直观理解**：目标函数把内部表示匹配和外部答案正确结合起来。前者使压缩后的学生思维接近教师状态，后者防止模型只学会表示相似而不会完成任务。<br>
**原文位置**：第 2.1 节“CODI distillation”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：模型通过最小化 $L=\gamma L_{\mathrm{kd}}+L_{\mathrm{ce}}$ 进行优化。$L_{\mathrm{kd}}$ 在答案冒号位置对齐教师与学生隐藏状态，摘录明确为隐藏状态的 L1 损失；$L_{\mathrm{ce}}$ 则训练学生生成正确答案。该设计使矩阵潜变量同时受到表示蒸馏和任务监督，但摘录未明确报告优化器、学习率、训练轮数或 $\gamma$ 的数值。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 矩阵潜变量瓶颈**

矩阵瓶颈把前一步隐藏状态 $h$ 映射为 $Z\in\mathbb{R}^{d\times d}$，实验固定 $d=16$。该矩阵位于显式链式思维反馈路径上，每个连续推理位置对应一个 $d\times d$ 思维矩阵，而不是普通向量潜变量。

> 直观理解：矩阵形式提供了一个单样本可观测的结构指标——秩，因此可以直接测试模型是否同时保留多个独立推理方向。

**2. 展平后投影读出**

默认读出先计算 $\operatorname{vec}(Z)$，再用 $W_{\mathrm{down}}\in\mathbb{R}^{D\times d^{2}}$ 投影回 $D$ 维，最后进行 LayerNorm。研究中还比较了双线性重参数化、含 GELU 的双线性读出、将奇异值送入 MLP 的 SVD 增强读出，以及基于 $ZZ^{\top}$ 的二次读出。

> 直观理解：读出器决定矩阵中的信息如何重新进入语言模型；增加非线性或显式奇异值通道，是为了检查秩不敏感是否只是默认展平线性读出的副作用。

**3. 秩截断探针**

对每个矩阵执行 SVD，并以 $Z_k=U_{:,1:k}\Sigma_{1:k,1:k}V_{:,1:k}^{\top}$ 替代原矩阵。硬截断使用实际前 $k$ 个奇异方向；有效秩则由归一化奇异值的谱熵指数化得到，用于描述谱能量分散程度，而不是替代干预本身。

> 直观理解：该模块把“秩是否重要”转化为可操作的因果式干预：只保留较少矩阵方向，再看模型是否还能答对。

**训练与推理**

训练阶段，教师输入为 prompt、显式链式思维和答案，学生输入为 prompt、固定数量连续潜在位置和答案；每个潜在位置由前一步隐藏状态反馈产生，矩阵瓶颈将该状态转换为 $Z$，再读出为下一步输入所需的隐藏状态。学生在答案冒号位置与教师状态计算 $L_{\mathrm{kd}}$，并对答案计算 $L_{\mathrm{ce}}$，联合更新模型。推理阶段不需要显式链式思维；模型按同一反馈路径生成答案。进行秩探针时，在读出前对每个 $Z$ 做 SVD，用 $Z_k$ 替换原矩阵，然后比较不同 $k$ 的答案准确率；有效秩仅用于谱结构统计，不能与硬秩截断混同。

**复现信息**

摘录中可确认的复现设定包括：骨干模型为 GPT-2 small，隐藏维度 $D=768$；矩阵边长为 $d=16$；默认读出为展平后线性投影并接 LayerNorm；秩干预采用 SVD 的硬前 $k$ 截断。有效秩使用归一化奇异值 $\tilde{\sigma}_i=\sigma_i/\sum_j\sigma_j$ 的谱熵指数化形式，但摘录未明确报告具体训练超参数、连续潜在位置数量、可选 thinker 是否启用、SVD 的数值阈值或答案解码策略，因此这些内容不应据此补写。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ProsQA：主要推理任务，用于三个训练条件、三随机种子复现及矩阵潜变量的秩投影评估。逐轮评估使用 COCONUT 测试文件前 128 个问题；线性探针使用完整的 500 题留出集。原文节选未进一步说明题目构成与数据划分方式。
- GSM8K-Aug：增强版数学推理任务，仅用于运行 R1。该模型处在约 6% 准确率、低于学习阈值的工作点，因此作者明确指出该运行不能单独支持关于秩的实质性结论。
- 500 题 COCONUT 测试文件：作为评估来源；常规逐轮实验取前 128 题，线性探针和无矩阵瓶颈的负对照使用完整 500 题。节选没有明确说明它与 ProsQA 命名之间的具体关系。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务准确率**

预测正确的题目比例；用于比较不同训练条件、不同保留秩 $k$、不同读出器以及负对照下的任务性能。 （越高越好，因为它直接反映目标任务上的预测正确率。）

</div>
<div class="metric-item" markdown="1">

**有效秩与秩投影曲线范围**

有效秩概括评估时 $16\times16$ 潜矩阵 $Z$ 的谱维度；曲线范围衡量 $k\in\{1,2,4,8,16\}$ 时最高与最低准确率之差。范围越小，表示性能对保留秩越不敏感。 （有效秩本身没有统一的优劣方向；若研究假设是秩承载必要推理成分，则更大的 $k$ 应带来更高准确率，而接近零的曲线范围反对这一预期。）

</div>
<div class="metric-item" markdown="1">

**Spearman 秩相关系数及其显著性**

样本级相关系数 $r_s$ 衡量潜矩阵有效秩与预测正确性之间是否存在单调关系；读出器实验中的 $p$ 值用于检验秩投影准确率是否呈显著单调趋势。 （不存在一般性的越高或越低越好；支持“秩有用”的证据应表现为稳定的非零相关或显著趋势，而接近零的 $r_s$ 或较大的 $p$ 值表示缺乏相应证据。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四种训练条件下，对矩阵潜变量 $Z$ 施加秩-$k$ 投影，其中 $k\in\{1,2,4,8,16\}$。

<div class="result-value" markdown="1">

四行实验的准确率曲线范围均不超过 0.6 个百分点。例如 ProsQA 的 R2 在 $k=1$ 与 $k=16$ 时均为 78.4%，R3a 为 76.8% 与 76.6%，R3b 为 72.6% 与 72.4%；相应样本级秩—正确性相关系数也接近零。

</div>

作者据此主张：模型的任务损失对潜矩阵保留多少秩基本不敏感。直观地说，即使把矩阵压到很低的秩，答案准确率也几乎不变，这不符合“较高秩保存多条必要并行推理路径”的直接预测。不过，该结果只说明这种秩投影没有造成可观测性能下降，不能单独证明矩阵中不存在分布式信息，也不能证明模型完全没有使用该潜位置。

<div class="result-source" markdown="1">

来源：表 1 标题说明

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Range across k∈{1,2,4,8,16} is ≤0.6 pp in every row.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### ProsQA 上进行三随机种子复现，并比较各次训练的最终有效秩与准确率。

<div class="result-value" markdown="1">

三种子平均准确率为 81.0 ± 2.0 个百分点，但最终有效秩横跨 $\{4,12,13\}$，即相近的任务表现可以伴随显著不同的潜矩阵秩。

</div>

作者将这种跨种子解耦解释为训练目标没有稳定奖励某个特定秩。关键不是某一次运行恰好得到低秩或高秩，而是不同秩都能达到相近准确率；因此最终秩不宜直接视为模型拥有多少条推理路径的指标。但只有三个种子，尚不足以刻画秩与性能之间所有较弱或非单调的关系。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A three-seed replication yields 81.0 +/- 2.0 percentage points accuracy while the final effective rank of Z spans {4, 12, 13}; the loss does not reward any particular rank.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 将原有读出方式替换为双线性、双线性加 GELU、SVD 增强和基于 $ZZ^T$ 的二次型读出器，再重复秩-$k$ 投影实验。

<div class="result-value" markdown="1">

四种读出器的秩投影曲线仍然平坦，Spearman 趋势检验的 $p$ 值依次为 0.63、0.14、0.82 和 0.46，均未显示显著的单调秩效应。

</div>

这排除了一个直接替代解释：平坦曲线并非仅由“先展平矩阵、再做线性投影”的读出器导致。尤其是对 $Z$ 非线性的 GELU 读出、显式读取奇异值的 SVD 读出以及依赖 $ZZ^T$ 的二次读出仍未产生秩敏感性。不过，不显著并不等于各种可能读出器都绝对与秩无关；结论只覆盖论文实际训练和测试的四种结构。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

All four rank-k curves remain flat (Spearman p-values 0.63, 0.14, 0.82, 0.46).

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

- 不同读出器结构：双线性重参数化、对 $Z$ 非线性的双线性加 GELU、将奇异值送入 MLP 的 SVD 增强读出器，以及基于 $ZZ^T$ 的二次型读出器。它们用于检验秩不敏感是否只是展平后线性投影读出器造成的结构性假象。
- 原始预训练隐藏状态：在线性探针实验中与矩阵潜变量 $Z$ 比较，用于判断 $Z$ 是否比模型未经矩阵瓶颈处理的隐藏表示更直接地编码目标答案。
- 普通 GPT-2 监督微调模型：不含矩阵瓶颈，也不存在原生的 $Z$，但接受相同形式的秩投影干预。该负对照用于判断平坦曲线是否为矩阵潜变量独有现象。
- 随机隐藏状态位置敏感性下界：以随机 $h$ 替换或干预相应位置并测量准确率，用于判断秩投影结果是否已落到“该位置本身不重要”的性能水平。

**实验想回答的问题**

- 矩阵式连续思维模型的潜变量 $Z$ 是否真正利用了矩阵秩来承载并行或可分解的推理成分；具体而言，将 $Z$ 投影为不同的低秩近似后，任务准确率是否随保留秩 $k$ 明显变化？
- 若秩不影响预测，这种现象究竟来自特定的展平后投影读出器，还是在非线性、显式奇异值感知及二次型读出器下仍然存在；同时，秩消融是否可能只是检测到了潜变量所在位置对模型不重要？

**实验实现**

矩阵-CODI 将每个连续思维潜 token 路由到一个 $d\times d$ 矩阵瓶颈；表 1 中实际评估的是 $16\times16$ 的矩阵潜变量 $Z$。核心干预先对每个样本的 $Z$ 做秩-$k$ 投影，再以 $k\in\{1,2,4,8,16\}$ 重新执行读出和任务预测，从而观察删除较小奇异方向是否损害准确率。常规结果来自每个 epoch 的 25 次评估，每次使用 500 题测试文件的前 128 题，单题对应约 0.78 个百分点的分辨率；线性探针和负对照改用完整 500 题留出集。论文还比较了 Thinker 开启或关闭、训练参数 $\gamma$ 取 1.0 或 0.0 的条件，并用三随机种子检查最终秩与准确率是否稳定对应。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 在完整 500 题留出集上，用线性探针分别从矩阵潜变量 $Z$ 和原始预训练隐藏状态预测目标。 | 从 $Z$ 读取目标的 AUC 为 0.673，低于原始预训练隐藏状态的 0.846。 | 该探针比较两种表示对目标答案的线性可解码程度，结果说明矩阵瓶颈没有让目标信息比原始隐藏状态更容易被线性读取。它支持“$Z$ 的秩不是清晰任务结构”的解释，但线性探针能力有限：较低 AUC 不代表 $Z$ 完全不含信息，也不能排除信息以非线性形式存在。 | 摘要<br><span class="experiment-evidence">A linear probe on Z underperforms a raw pretrained hidden state at target prediction (AUC 0.673 vs. 0.846).</span> |
| 对不含矩阵瓶颈和原生 $Z$ 的普通 GPT-2 监督微调模型执行相同秩投影范式，并加入随机隐藏状态位置敏感性下界。 | 三随机种子、500 个样本的负对照同样产生平坦曲线，汇总均值范围仅 0.20 个百分点；随机 $h$ 控制落在相同准确率水平。 | 这一控制隔离了“矩阵秩机制”与“干预位置无关”两种解释。连没有矩阵潜变量的模型也能出现相同曲线，且随机位置控制达到相同性能下界，说明平坦曲线可能只是因为被替换的位置对最终答案没有因果作用。因此，秩投影实验可证明缺少秩敏感性，却不能单凭自身证明模型梯度专门忽略了矩阵秩。 | 摘要<br><span class="experiment-evidence">A negative control on vanilla GPT-2 SFT (no matrix bottleneck, no Z, three seeds, n=500) reproduces a flat rank-k curve under the same intervention paradigm with pooled-mean range 0.20pp, and a random-h sensitivity floor lands at the same accuracy: the rank-k ablation alone conflates rank-blindness with position-irrelevance.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该工作通过干预和探针分析连续思维链模型中的潜在矩阵秩，核心贡献是研究语言模型内部表征与机制可解释性。; rule check: matched taxonomy keywords; top rule score=5.0
- 全文指纹：`d7e6730564fd7b18bb466ab79a56ad60b4c2c43e182e1187d7e00bfd3914631a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
