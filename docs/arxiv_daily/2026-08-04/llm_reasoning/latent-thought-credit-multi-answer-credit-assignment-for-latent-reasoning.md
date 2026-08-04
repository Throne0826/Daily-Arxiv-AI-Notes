---
title: "[论文解读] Latent Thought Credit: Multi-Answer Credit Assignment for Latent Reasoning"
description: "[arXiv 2608.01593][LLM Reasoning] 本文将潜在推理的训练信号构造重新表述为潜在思维的期望下游奖励估计，并提出通过固定思维后的上下文、对多个答案奖励取平均来进行分层信用分配的LTC框架。"
arxiv_id: "2608.01593"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:02:51.600796+00:00"
source_sha256: "16b10867381c30a6e94f064e5251548caf079506d362f152dcd6e893bc8fc407"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "潜在推理"
  - "信用分配"
  - "可验证奖励强化学习"
  - "固定上下文"
  - "多答案采样"
  - "思维级期望奖励"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.01593</p>

# Latent Thought Credit: Multi-Answer Credit Assignment for Latent Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Xuyang Zhao, Liting Zhang, Zichen Xu, Yong Chen, Wenjia Zeng, Shiwan Zhao, Qicheng Li</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> TMCC, College of Computer Science, Nankai University, Tianjin, China；Lingxi (Beijing) Technology Co., Ltd</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01593v1) · [PDF 下载](https://arxiv.org/pdf/2608.01593v1) · **关键词** 潜在推理, 信用分配, 可验证奖励强化学习, 固定上下文, 多答案采样, 思维级期望奖励<br>


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

本文将潜在推理的训练信号构造重新表述为潜在思维的期望下游奖励估计，并提出通过固定思维后的上下文、对多个答案奖励取平均来进行分层信用分配的LTC框架。

**不用术语来说**：模型在内部形成一段不可直接阅读的连续表示后，还要随机生成最终答案；因此，一个错误答案既可能源于内部思考不佳，也可能只是答案生成时偶然选错。若仅凭一次作答的得分奖惩内部思考，训练就可能奖励坏思路或惩罚好思路，难以稳定提升推理能力。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出潜在思维信用LTC：对每个问题采样多个潜在思维，固定每个思维完成后的上下文，再从同一上下文生成多个答案，以平均答案奖励估计该思维的期望效用。
- 建立分层训练信号：分别用思维级优势和答案级优势优化潜在思维阶段与答案阶段，并以优势加权的思维匹配目标提高策略复现高信用潜在思维的能力。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型的潜在推理与可验证奖励强化学习交叉领域。传统链式思维把中间推理写成离散文本，因而可以直接对整段生成序列施加答案正确性奖励；潜在推理则把部分中间计算放在连续隐藏状态、软词元或文本与潜变量混合的表示中，以扩展模型表达和探索推理过程的方式。本文关注的核心不是如何构造潜在表示本身，而是如何依据最终答案奖励判断一段已采样潜在思维是否有用：同一潜在思维之后仍可能随机生成不同答案，因此单个答案的正确或错误同时受到思维质量与答案采样噪声影响，不能稳定代表该思维的预期效用。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**潜在推理**

模型不把全部中间推理写成可读文本，而是在连续隐藏状态、软词元或混合表示中完成部分计算。这里的“潜在思维”指一次完整采样得到、随后用于生成答案的内部推理表示。

</div>
<div class="concept-item" markdown="1">

**信用分配**

信用分配是根据最终奖励判断此前哪些决策应被鼓励或抑制。本文需要把答案正确性带来的奖励分别归因于潜在思维阶段和答案生成阶段。

</div>
<div class="concept-item" markdown="1">

**固定上下文期望奖励**

在某段潜在思维产生后固定其对应上下文，再从该上下文多次采样答案并平均奖励，可估计该思维的下游期望效用。通俗地说，它是在尽量保持“思考过程”不变的情况下重复作答，以区分思维质量与偶然答对或答错。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个待求解提示，任务覆盖数学推理与 STEM 多项选择等具有可验证答案的场景；模型先随机采样若干潜在思维，再从每段思维形成的固定后续上下文中随机生成多个答案，并依据答案是否满足可验证标准获得奖励。训练所需输出不是单一序列分数，而是两层信用信号：以同一潜在思维下多个答案的平均奖励估计思维级效用，用于优化潜在思维生成；同时利用具体答案之间的奖励差异优化答案生成。该设置假定答案奖励可计算，并且固定同一思维后的上下文、重复采样答案，能够近似分离潜在思维质量和答案生成随机性；本文比较的是完整潜在思维的下游效用，而不是为每个潜在推理步骤逐步分配奖励。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **GRPO-MA（Wang et al., 2026）**: 该方法从每个离散思维分支采样多个答案，并分别构造思维级与答案级优势，说明分支结构和多答案采样有助于信用估计；但其信用对象仍是离散或与词元锚定的推理分支，而本文将固定上下文下的多答案期望奖励用于连续潜在思维。
- **RLTT（Williams and Tureci, 2026）**: RLTT研究潜在轨迹中哪些步骤应获得奖励，关注轨迹内部的逐步信用分配；本文则把一段完整潜在思维视为比较单位，通过固定其后续上下文并平均多个答案奖励来评估整体思维效用。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

潜在推理把中间计算放在连续隐藏状态、软词元或混合表示中，扩展了模型表达和探索推理过程的空间，但这些内部状态通常无法像文本推理链那样被直接检查。训练时往往只能获得最终答案是否正确的可验证奖励，因此必须从下游结果反推某个潜在思维是否值得强化。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于可验证答案奖励的强化学习**：模型生成推理结果和最终答案，再依据答案能否被规则或标准答案验证来获得奖励；这类方法已被用于改进以文本思维链表示的数学推理。
- **连续或软表示的潜在推理方法**：模型不完全输出离散文本思维链，而是在连续隐藏状态、软词元或文本与潜变量的混合表示中完成中间计算，并可结合探索或测试时搜索获得答案。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单个潜在思维通常只通过一次随机生成的答案接受评价，而该答案的奖励同时受思维质量和答案采样随机性影响；因此，单次奖励是思维效用的高噪声估计，可能形成含糊甚至错误的信用排序。
- 现有潜在或软推理方法虽然提供了连续计算、探索和测试时搜索机制，但通常没有显式估计每个已采样潜在思维的期望下游奖励，因而缺少专门面向潜在思维阶段的可靠训练信号。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种面向潜在推理的信用分配机制，能够在保持同一潜在思维及其后续上下文不变的条件下，隔离答案生成的随机性，估计该思维本身的期望效用，并将这一估计与答案阶段的学习信号分开使用。

</div>
<div markdown="1"><span>核心问题</span>

对于只能从最终答案获得奖励的潜在推理模型，能否通过同一潜在思维下的多次答案采样构造更可靠的思维级信用，并据此分别优化潜在思维生成与答案生成？

</div>
<div markdown="1"><span>作者直觉</span>

把潜在思维看作一道题的内部解题方向，把后续答案看作沿该方向进行的多次作答。一次作答失败不足以证明方向错误；固定这个方向并重复作答后，平均得分更接近该方向通常能带来的真实收益。再用不同潜在思维之间的相对平均收益决定强化对象，就能减少偶然答案对内部思维奖惩的干扰。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

LTC（Latent Thought Credit）的输入是提示 $x$，输出是经过强化学习更新、能够进行连续潜在推理并生成离散答案的策略 $\pi_\theta$。一次训练 rollout 先从旧策略 $\pi_{\theta_{\mathrm{old}}}$ 采样 $K$ 条潜在思路：每一步不选择单个离散词元，而是通过 Gumbel-Softmax 得到词表上的软分布，再将词嵌入加权混合成连续向量。每条思路结束后保留其上下文 $s_i$，并在完全相同的 $s_i$ 下独立采样 $M$ 个答案。由此，同一思路对应多个答案奖励，而不是仅由一次可能带有采样偶然性的答案决定其好坏。
LTC随后进行分层信用分配：先用同一上下文下 $M$ 个答案奖励的均值 $\hat{\mu}_i$ 估计第 $i$ 条潜在思路的期望效用，再分别构造思路级优势 $A_i^{\mathrm{think}}$ 和答案级优势 $A_{ij}^{\mathrm{ans}}$。前者只更新潜在思路位置，后者只更新离散答案位置；此外，思路匹配辅助损失要求当前策略靠近旧策略探索到的高信用潜在向量。直观地说，LTC把“想法本身是否可靠”和“这一次答案采样是否碰巧正确”拆开评估，并让模型重点记住经多次作答验证过的好想法。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 连续潜在思路采样

旧策略输出干净 logits $\ell_{\theta_{\mathrm{old}}}(h_{i,t})$，加入 Gumbel 噪声 $g_{i,t}$ 后经温度缩放和 softmax 得到 $q_{i,t}$；随后以 $q_{i,t}$ 对词嵌入 $E_v$ 加权并归一化，形成连续潜在词元 $z_{i,t}$。重复该过程得到 $K$ 条潜在思路 $\tau_i^{\mathrm{think}}$，并保留每条思路结束后的上下文 $s_i$。

<div class="method-step__io" markdown="1">

**输入**：提示 $x$、旧策略 $\pi_{\theta_{\mathrm{old}}}$、思路采样温度 $\tau_{\mathrm{think}}$，以及每个潜在步骤的当前状态 $h_{i,t}$。<br>
**输出**：$K$ 条由连续嵌入组成的潜在思路及其固定的思路后上下文 $\{s_i\}_{i=1}^{K}$。

</div>

**直观理解**：普通生成每一步必须选定一个词，而这里允许模型使用多个词嵌入的连续混合表示一个内部想法。Gumbel 噪声使不同 rollout 探索不同方向，固定 $s_i$ 则保证后续多次作答都从同一个想法起点出发。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 固定上下文的多答案评估

对每个 $s_i$ 独立采样 $M$ 个离散答案 $y_{ij}$，计算奖励 $r_{ij}=R(x,y_{ij})$，并以均值 $\hat{\mu}_i=M^{-1}\sum_j r_{ij}$ 估计该思路在答案采样分布下的期望奖励。评估期间上下文 $s_i$ 不变，因此奖励差异来自答案采样，而不同 $\hat{\mu}_i$ 的差异更能反映潜在思路质量。

<div class="method-step__io" markdown="1">

**输入**：提示 $x$、每条潜在思路对应的固定上下文 $s_i$、旧策略的答案分布 $\pi_{\theta_{\mathrm{old}}}^{\mathrm{ans}}$ 和奖励函数 $R$。<br>
**输出**：每条思路的效用估计 $\hat{\mu}_i$，以及全部 $KM$ 个答案及其奖励 $r_{ij}$。

</div>

**直观理解**：一次错误答案不一定说明前面的想法错误，也可能只是表达或采样失误。让同一想法回答多次并取平均，相当于用重复试验降低偶然噪声。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分层优势构造与位置级信用分配

在 $K$ 条思路之间标准化 $\hat{\mu}_i$ 得到 $A_i^{\mathrm{think}}$，并在全部 $KM$ 个答案之间标准化 $r_{ij}$ 得到 $A_{ij}^{\mathrm{ans}}$。完整 rollout 中，潜在思路位置统一使用对应的 $A_i^{\mathrm{think}}$，答案位置使用各自的 $A_{ij}^{\mathrm{ans}}$。

<div class="method-step__io" markdown="1">

**输入**：思路效用估计 $\{\hat{\mu}_i\}_{i=1}^{K}$ 和同一提示下的全部答案奖励 $\{r_{ij}\}$。<br>
**输出**：分别面向潜在思路阶段和答案阶段的两组优势权重。

</div>

**直观理解**：思路要与其他思路比较，答案要与同题的其他答案比较。这样可避免把某个答案的偶然成败原封不动地归因给整条内部思路。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分层策略更新与高信用思路匹配

以 REINFORCE 风格损失更新策略：思路位置最大化由 $A_i^{\mathrm{think}}$ 加权的潜在策略代理项，答案位置最大化由 $A_{ij}^{\mathrm{ans}}$ 加权的词元对数概率。同时从当前策略干净 logits 的 top-$k$ 支持集构造预测嵌入 $\hat z_{i,t}$，并按思路优势的 softmax 权重拟合旧策略采得的潜在向量。

<div class="method-step__io" markdown="1">

**输入**：带优势权重的完整 rollout、当前策略 $\pi_\theta$、旧策略产生的潜在向量 $z_{i,t}^{\mathrm{roll}}$，以及匹配权重 $\lambda$。<br>
**输出**：更新后的参数 $\theta$；训练后模型可先生成连续潜在思路，再从相应上下文生成最终离散答案。

</div>

**直观理解**：策略梯度负责增加高回报行为再次出现的概率，匹配损失则直接教模型复现高分思路在嵌入空间中的形状。后者为连续内部表示提供了比单纯奖励更直接的学习信号。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 多答案思路效用估计与分层优势

$$
\begin{aligned}\mu_i&=\mathbb{E}_{y\sim\pi_{\theta_{\mathrm{old}}}^{\mathrm{ans}}(\cdot\mid x,s_i)}[R(x,y)],\\ \hat{\mu}_i&=\frac{1}{M}\sum_{j=1}^{M}r_{ij},\qquad r_{ij}=R(x,y_{ij}),\\ A_i^{\mathrm{think}}&=\frac{\hat{\mu}_i-\operatorname{mean}_{i'}(\hat{\mu}_{i'})}{\operatorname{std}_{i'}(\hat{\mu}_{i'})+\epsilon},\\ A_{ij}^{\mathrm{ans}}&=\frac{r_{ij}-\operatorname{mean}_{i',j'}(r_{i'j'})}{\operatorname{std}_{i',j'}(r_{i'j'})+\epsilon}.\end{aligned}
$$

**符号说明**

- $x$：当前训练提示。
- $i,i'$：潜在思路索引；统计量中的索引遍历同一提示采样的全部思路。
- $j,j'$：固定思路上下文下的答案索引；联合统计量遍历同一提示的全部答案。
- $s_i$：第 i 条潜在思路结束后被保留并固定的上下文。
- $\pi_{\theta_{\mathrm{old}}}^{\mathrm{ans}}$：参数为旧参数的答案生成策略。
- $y,y_{ij}$：离散答案；其中 $y_{ij}$ 是从第 i 个固定上下文采样的第 j 个答案。
- $R(x,y)$：根据提示和答案返回标量奖励的函数。
- $r_{ij}$：第 i 条思路下第 j 个答案的实际奖励。
- $\mu_i$：固定第 i 条思路上下文时，对答案采样随机性取期望后的真实思路效用。
- $\hat{\mu}_i$：由有限个答案奖励均值获得的思路效用估计。
- $M$：每条潜在思路对应的答案采样数。
- $A_i^{\mathrm{think}}$：第 i 条潜在思路在同题思路组内标准化后的优势。
- $A_{ij}^{\mathrm{ans}}$：第 i 条思路下第 j 个答案在同题全部答案内标准化后的优势。
- $\operatorname{mean},\operatorname{std}$：分别表示指定索引范围内的均值和标准差。
- $\epsilon$：防止标准差过小导致除零或数值不稳定的常数。

<div class="equation-explanation" markdown="1">

**直观理解**：第一、二行把思路质量定义为“固定该思路后，多次生成答案所得奖励的期望”，并以样本平均近似。后两行分别回答两个不同问题：一条思路相对其他思路是否更可靠，以及一次具体作答相对同题其他答案是否更好；这是分层信用成立的核心。<br>
**原文位置**：Thought-Level Reward Estimation，公式（3）—（4）；Hierarchical Credit Construction，公式（5）及其后续答案优势定义。

</div>

</div>

<div class="equation-block" markdown="1">

#### 分层策略损失、思路匹配与总目标

$$
\begin{aligned}\mathcal{L}_{\mathrm{think}}&=-\frac{1}{K}\sum_{i=1}^{K}\frac{1}{T_i}\sum_{t\in\mathcal{P}_i^{\mathrm{think}}}\operatorname{sg}(A_i^{\mathrm{think}})\ell_{i,t}^{\mathrm{think}}(\theta),\\ \mathcal{L}_{\mathrm{ans}}&=-\frac{1}{KM}\sum_{i=1}^{K}\sum_{j=1}^{M}\frac{1}{U_{ij}}\sum_{t\in\mathcal{P}_{ij}^{\mathrm{ans}}}\operatorname{sg}(A_{ij}^{\mathrm{ans}})\ell_{ij,t}^{\mathrm{ans}}(\theta),\\ D_i^{\mathrm{match}}&=\frac{1}{|\mathcal{T}_i|}\sum_{t\in\mathcal{T}_i}\frac{\|\hat z_{i,t}-\operatorname{sg}(z_{i,t}^{\mathrm{roll}})\|_2^2}{d_{\mathrm{model}}},\\ \omega_i&=\frac{\exp(A_i^{\mathrm{think}})}{\sum_{i'=1}^{K}\exp(A_{i'}^{\mathrm{think}})},\qquad \mathcal{L}_{\mathrm{match}}=\sum_{i=1}^{K}\omega_iD_i^{\mathrm{match}},\\ \mathcal{L}&=\mathcal{L}_{\mathrm{think}}+\mathcal{L}_{\mathrm{ans}}+\lambda\mathcal{L}_{\mathrm{match}}.\end{aligned}
$$

**符号说明**

- $\mathcal{L}_{\mathrm{think}}$：潜在思路位置上的优势加权策略损失。
- $\mathcal{L}_{\mathrm{ans}}$：离散答案位置上的优势加权策略损失。
- $\mathcal{L}_{\mathrm{match}}$：使当前策略复现高信用 rollout 潜在向量的辅助损失。
- $\mathcal{L}$：用于更新当前策略参数的最终训练目标。
- $K,M$：分别为每个提示采样的潜在思路数和每条思路采样的答案数。
- $\mathcal{P}_i^{\mathrm{think}},\mathcal{P}_{ij}^{\mathrm{ans}}$：分别表示第 i 条思路的潜在位置集合和第 (i,j) 条完整 rollout 的答案位置集合。
- $T_i,U_{ij}$：分别为上述潜在思路位置数和答案位置数，用于长度归一化。
- $t$：思路或答案序列中的位置索引。
- $\ell_{i,t}^{\mathrm{think}}(\theta),\ell_{ij,t}^{\mathrm{ans}}(\theta)$：当前参数下思路位置的 Gumbel-Softmax 策略代理项，以及答案词元的对数概率项。
- $\theta$：待优化的当前策略参数。
- $\operatorname{sg}$：停止梯度算子，使优势和 rollout 目标仅作为固定监督信号。
- $D_i^{\mathrm{match}}$：第 i 条思路的平均归一化嵌入匹配距离。
- $\mathcal{T}_i$：第 i 条潜在思路所含步骤的集合。
- $\hat z_{i,t}$：由当前策略干净 logits 的 top-k 候选词嵌入加权得到的预测向量。
- $z_{i,t}^{\mathrm{roll}}$：旧 rollout 策略在相同步骤采样到的潜在思路向量。
- $d_{\mathrm{model}}$：模型隐藏维度，用于归一化平方欧氏距离。
- $\omega_i$：由思路优势经过跨思路 softmax 得到的非负匹配权重。
- $A_i^{\mathrm{think}},A_{ij}^{\mathrm{ans}}$：分别为思路级优势和答案级优势。
- $\lambda$：控制思路匹配辅助项相对强度的超参数。

<div class="equation-explanation" markdown="1">

**直观理解**：前两行把不同层级的信用送到正确的位置：思路平均表现决定潜在向量更新，具体答案表现决定答案词元更新。后两行让高优势思路获得更大的模仿权重，最终目标则在奖励驱动的策略优化与连续表示的直接匹配之间取得平衡。<br>
**原文位置**：Hierarchical Policy Objective，公式（7）—（8）及答案损失；Thought Matching Auxiliary，公式（10）—（12）；Overall Objective and Training Procedure，公式（13）。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：优化时最小化 $\mathcal{L}=\mathcal{L}_{\mathrm{policy}}+\lambda\mathcal{L}_{\mathrm{match}}$，其中 $\mathcal{L}_{\mathrm{policy}}=\mathcal{L}_{\mathrm{think}}+\mathcal{L}_{\mathrm{ans}}$。$\mathcal{L}_{\mathrm{think}}$ 将同一潜在思路的 $A_i^{\mathrm{think}}$ 广播到该思路的全部潜在位置，$\mathcal{L}_{\mathrm{ans}}$ 则将 $A_{ij}^{\mathrm{ans}}$ 作用于对应答案的全部离散词元；两者都对序列长度取平均，并对优势停止梯度。论文明确指出，底层更新仍是简单的 REINFORCE 风格形式，LTC的实质变化不是发明新的策略梯度，而是重新估计并分配潜在推理信用。
辅助项 $\mathcal{L}_{\mathrm{match}}$ 使用当前策略的干净 logits 预测潜在嵌入，以 rollout 策略产生且停止梯度的 $z_{i,t}^{\mathrm{roll}}$ 为目标。由于权重 $\omega_i$ 随 $A_i^{\mathrm{think}}$ 增大，优化主要模仿多答案评估确认的高信用思路，而不是无差别复制所有随机探索结果；$\lambda$ 决定这种直接表示监督相对于策略损失的强度。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Gumbel-Softmax 潜在思路生成器**

在潜在步骤 $t$，模型将加入 Gumbel 噪声的 logits 转换为软分布 $q_{i,t}$，再生成归一化嵌入混合 $z_{i,t}=\sum_v q_{i,t}(v)E_v/\lVert q_{i,t}\rVert$。因此潜在思路是连续向量序列，而非可直接阅读的离散思维链。

> 直观理解：该模块既保留可微的软表示，又通过随机扰动产生思路多样性；没有多样思路，就无法在同一提示内比较哪种内部推理更有价值。

**2. 固定上下文多答案信用估计器**

其目标是估计 $\mu_i=\mathbb{E}_{y\sim\pi_{\theta_{\mathrm{old}}}^{\mathrm{ans}}(\cdot\mid x,s_i)}[R(x,y)]$，实际使用同一 $s_i$ 下 $M$ 个奖励的样本均值 $\hat\mu_i$。思路优势在 $K$ 个 $\hat\mu_i$ 上归一化，而答案优势在同一提示的 $KM$ 个原始奖励上归一化。

> 直观理解：这是LTC区别于把整条 rollout 只配一个优势值的关键设计。它估计的是“从这个想法继续作答，平均能有多好”，因而更接近应归给潜在思路的信用。

**3. 优势加权思路匹配器**

当前策略仅在干净 logits 的 top-$k$ 词元集合 $S_{i,t}$ 上归一化概率，并据此形成预测嵌入 $\hat z_{i,t}$；它与停止梯度后的 rollout 向量 $z_{i,t}^{\mathrm{roll}}$ 计算按隐藏维度归一化的均方距离。各思路距离由 $\omega_i=\operatorname{softmax}_i(A_i^{\mathrm{think}})$ 加权，使高优势思路对辅助损失贡献更大。

> 直观理解：策略梯度只告诉模型某条思路总体上应增加还是减少，匹配器进一步给出“应靠近哪个连续向量”的方向。top-$k$ 限制让匹配集中在模型最可能的候选嵌入上。

**训练与推理**

训练阶段按提示进行 on-policy 式循环：先用 $\theta_{\mathrm{old}}$ 和 Gumbel 扰动生成 $K$ 条连续潜在思路；保存各自的 $s_i$ 后，每条思路生成 $M$ 个答案并由 $R$ 打分；计算 $\hat\mu_i$、$A_i^{\mathrm{think}}$ 和 $A_{ij}^{\mathrm{ans}}$；再以完整 rollout 计算分层策略损失和思路匹配损失，更新 $\theta$，随后将更新后的策略用于后续 rollout。因为每条思路被复制到 $M$ 个答案分支，训练计算预算随 $KM$ 增长，$K$ 控制思路探索广度，$M$ 控制单条思路效用估计的重复精度。
推理阶段不需要多答案信用估计、优势标准化或思路匹配监督；这些是训练信用分配机制。模型先执行已学习的连续潜在思路阶段，得到思路后的内部上下文，再由答案策略生成可观察的离散答案。所给原文没有进一步明确报告推理时是否固定使用随机 Gumbel 噪声、具体解码温度或生成多个候选，因此这些设置不能由方法章节推断。

**复现信息**

公平复现所必需的结构性参数包括每题思路数 $K$、每条思路答案数 $M$、潜在采样温度 $\tau_{\mathrm{think}}$、思路匹配 top-$k$ 支持大小以及辅助权重 $\lambda$。主实验采用的配置可由所给消融文字确认包含 $(K,M)=(2,4)$，即每个提示形成 $KM=8$ 个答案 rollout；但优化器、学习率、批量大小、潜在思路长度控制、Gumbel 噪声尺度细节及奖励函数实现未在所给方法摘录中明确报告，复现时必须回查论文其他章节。
还需保留两个容易改变方法含义的实现约束：第一，$M$ 个答案必须从完全相同的思路后上下文 $s_i$ 采样，否则其均值不再是固定思路的效用估计；第二，匹配目标 $z_{i,t}^{\mathrm{roll}}$ 和优势权重在相应损失中应停止梯度，避免模型通过修改信用或目标向量来降低损失。思路侧的 $\ell_{i,t}^{\mathrm{think}}$ 是 Gumbel-Softmax 潜在策略代理项，不能误实现为离散词元对数概率；答案侧才使用标准自回归词元对数概率。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：基础数学文字题数据集，用于训练并评估短链算术推理；固定上下文诊断另外抽取 256 个测试提示，以测量答案采样噪声、奖励估计误差和信用排序可靠性。原文未明确报告主实验所用训练集与测试集的具体样本数。
- MATH 与 MATH500：前者的训练集用于较困难的数学推理训练，MATH/MATH500 用于评估复杂数学推理及留出数据上的泛化。原文没有在所给节选中明确各自的评测规模或主结果。
- MMLU-STEM 与 ARC-Challenge：用于检验 STEM 多项选择理解、知识推理和任务迁移；训练使用由 MMLU 与 ARC-C 样本构成的多项选择集合。原文未明确该混合训练集的规模与配比。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率**

衡量最终答案正确的样本比例，是数学推理与 STEM 多项选择任务的主要效果指标。所给节选声称 LTC 的平均准确率最佳，但没有提供逐数据集数值。 （越高越好，因为它直接表示模型完成任务的成功率。）

</div>
<div class="metric-item" markdown="1">

**MAE 与 MSE**

分别计算低预算估计 $\hat{\mu}_i(m)$ 与留出参考均值 $\mu_i^{\mathrm{ref}}$ 之间的平均绝对误差和均方误差。MAE反映典型偏差大小，MSE对较大的估计错误施加更重惩罚。 （越低越好，因为较小误差意味着少量答案得到的思维期望奖励更接近留出答案池给出的参考值。）

</div>
<div class="metric-item" markdown="1">

**成对排序错误与 regret**

成对排序错误对反序记 1、估计侧并列记 0.5，用于衡量思维优劣关系是否错误或含糊；regret 是所选思维与候选集中参考最优思维之间的留出奖励差，用于衡量噪声选择造成的实际效用损失。 （二者均越低越好：前者降低表示思维排序更可靠，后者降低表示即使发生选择误差，其效用代价也更小。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 主任务总体比较：数学推理与 STEM 多项选择任务

<div class="result-value" markdown="1">

作者声称 LTC 在所比较方法中取得最高的平均准确率；但所给节选省略了主结果表，因此无法核对各数据集分数、平均提升幅度、模型规模、重复次数或显著性。

</div>

这一结论表明 LTC 的完整训练方案可能比 HRPO、GRPO 和 GRPO-MA 更有效，但当前材料不足以判断优势是否稳定地覆盖所有数据集，也不能区分提升主要来自多答案估计、分层优势还是思维匹配目标。它同样不证明 LTC 在不同模型族或更大 rollout 预算下仍然占优。

<div class="result-source" markdown="1">

来源：Abstract；所给 Experiments 节选未包含主结果表

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

LTC achieves the best average accuracy among the compared methods, while ablations and fixed-context diagnostics show that multi-answer estimation reduces reward-estimation error and mitigates ambiguous or incorrect thought-level credit.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 固定上下文方差诊断：初始策略、最终 LTC 策略及高 $K$ 候选池

<div class="result-value" markdown="1">

在初始策略中，思维内答案方差为 0.0376，超过思维间期望奖励方差 0.0244，噪声信号比为 1.54；最终策略对应数值为 0.0568、0.0043 和 13.10。扩大到 $K=32$、$M=64$ 后，比值仍为 8.99。

</div>

固定 $s_i$ 后仍然出现较大的正确性波动，说明单个最终答案不是潜在思维质量的稳定观测。最终策略的候选思维平均效用更接近，使思维间信号更弱，而答案采样噪声仍较大，因此单答案信用尤其容易误判。高 $K$ 结果说明这一现象并非只由四个候选思维造成；不过方差比较是诊断性证据，不直接证明多答案训练必然提高最终准确率。

<div class="result-source" markdown="1">

来源：Table 4；Analysis and Discussion / Variance Evidence and Budget Sensitivity

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For the initial policy, the noise-to-signal ratio is 1.54, showing that answer-sampling noise already exceeds thought-level variation before RL training. Compared with the initial policy, the final policy has lower between-thought variance (0.0043 vs. 0.0244) while retaining substantial within-thought variance (0.0568 vs. 0.0376), yielding a ratio of 13.10.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 固定上下文低预算奖励估计：将每个思维的答案数从 $m=1$ 增至 $m=8$

<div class="result-value" markdown="1">

初始策略的 MAE 从 0.0785 降至 0.0349，MSE 从 0.0412 降至 0.0068；最终策略的 MAE 从 0.1148 降至 0.0490，MSE 从 0.0581 降至 0.0093。

</div>

从同一潜在思维上下文采样更多答案并平均，可以更接近由 32 个留出答案形成的参考均值，而且这一趋势在训练前后都成立。这直接支持 LTC 的多答案估计动机，但参考均值仍是有限样本近似，并非真实期望奖励；该诊断也没有单独测量估计误差降低能带来多少任务准确率提升。

<div class="result-source" markdown="1">

来源：Table 5；Analysis and Discussion / Estimator Error

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

From m=1 to m=8, MAE decreases from 0.0785 to 0.0349 for the initial policy and from 0.1148 to 0.0490 for the final policy. The corresponding MSE values decrease from 0.0412 to 0.0068 and from 0.0581 to 0.0093, respectively.

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

- HRPO：用于控制潜在推理架构本身带来的影响。它是关键对照，因为 LTC 若优于 HRPO，更可能说明收益来自信用分配机制，而不只是采用了连续潜在思维。
- GRPO：在相同 rollout 预算下进行平坦的组相对策略优化，不显式区分思维阶段和答案阶段。该比较检验分层信用分配是否优于直接用最终答案奖励更新整个生成过程。
- GRPO-MA：从每个离散文本思维前缀继续采样多个答案，以前缀平均奖励构造思维级优势，并在同一提示的全部答案间归一化答案级优势。它是最接近的多答案基线，用于区分 LTC 的收益究竟来自多答案平均本身，还是来自潜在思维上的分层训练设计。

**实验想回答的问题**

- 在相同模型、提示格式、奖励计算、采样温度和 rollout 预算下，LTC 是否能比潜在推理基线、平坦的组相对策略优化以及离散思维上的多答案信用分配获得更高的数学与 STEM 任务准确率？
- 固定某个潜在思维产生的后思维上下文 $s_i$ 后，多次采样答案并取平均，能否降低期望奖励 $mu_i$ 的估计误差，并减少潜在思维排序错误及选择后悔？

**实验实现**

实验基于 Qwen2.5-Instruct 模型族和 GRPO 风格的在线策略训练框架。公平性控制包括相同模型、提示格式、奖励计算、采样温度及 rollout 预算；LTC 默认总预算为 $B=K\times M=8$，主设置为 $(K,M)=(2,4)$，即每个提示采样 2 个潜在思维，并从每个固定的后思维上下文采样 4 个答案。正式评测采用贪心解码。

固定上下文诊断不参与训练：对每个提示采样 $K$ 个潜在思维，冻结各自的上下文 $s_i$，再从同一上下文生成 $M$ 个答案。主诊断使用 256 个 GSM8K 测试提示、$K=4$ 和 $M=40$；编号 0 至 7 的答案组成低预算探测池，编号 8 至 39 的答案组成留出参考池，并考察 $m\in\{1,2,4,8\}$。初始策略和最终 LTC 策略采用相同的连续潜在思维 rollout 与 Gumbel 探索设置。另设高候选量诊断，使用 $K=32$、$M=64$，检查结论是否只在较小候选池中成立。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 多答案预算敏感性：固定上下文下令 $m\in\{1,2,4,8\}$ | 初始策略的成对排序错误从 0.3840 降至 0.2621，regret 从 0.0406 降至 0.0166；最终策略的成对排序错误从 0.4728 降至 0.4380，regret 从 0.0320 降至 0.0254。 | 该预算变化隔离了“每个固定思维上下文采样多少答案”的作用：更多答案减少了错误或含糊的思维排序，并降低选错思维的效用损失。初始策略改善更明显，而最终策略排序错误仍高，说明当候选思维的真实效用差距很小时，增加到 8 个答案仍不足以获得稳定排序。该实验是离线诊断，不等价于重新训练不同 $M$ 的 LTC。 | Table 6；Analysis and Discussion / Credit Assignment Consequence<br><span class="experiment-evidence">For the initial policy, pairwise error decreases from 0.3840 to 0.2621 and regret decreases from 0.0406 to 0.0166. For the final policy, pairwise error remains higher but decreases from 0.4728 to 0.4380, while regret decreases from 0.0320 to 0.0254.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It proposes an RL credit-assignment framework for training continuous latent reasoning using thought- and answer-level advantages.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`16b10867381c30a6e94f064e5251548caf079506d362f152dcd6e893bc8fc407`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
