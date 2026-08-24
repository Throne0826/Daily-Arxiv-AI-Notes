---
title: "[论文解读] DirEAG: Dirichlet Evidence Aggregation for Calibrating Verbalized Confidence in Mathematical Reasoning"
description: "[arXiv 2608.20717][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.20717"
announcement_date: "2026-08-24"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-24T02:09:15.725036+00:00"
source_sha256: "5e8faa53c7f90dee526b2c385437719e8f29561b68a5d0851dde05a668f6e83f"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型数学推理"
  - "黑盒置信度"
  - "verbalized confidence"
  - "置信度校准"
  - "多提示观测"
  - "Dirichlet 证据聚合"
  - "候选答案"
  - "空状态"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.20717</p>

# DirEAG: Dirichlet Evidence Aggregation for Calibrating Verbalized Confidence in Mathematical Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Haorui Xu, Yuzhou Zhu, Liyuan Gao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.20717v1) · [PDF 下载](https://arxiv.org/pdf/2608.20717v1) · **关键词** 大语言模型数学推理, 黑盒置信度, verbalized confidence, 置信度校准, 多提示观测, Dirichlet 证据聚合, 候选答案, 空状态<br>
**代码**: [https://github.com/horacehsugithub/DirEAG](https://github.com/horacehsugithub/DirEAG)

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

本文位于大语言模型数学推理与黑盒置信度校准的交叉领域。数学推理任务要求模型针对一道题生成答案，并说明该答案是否可信；由于数学答案通常是离散的、可由外部规则检查的结果，因此可以直接将模型报告的置信度与答案是否正确进行比较。本文关注一种黑盒设定：研究者无法使用模型内部的条件词概率，只能通过提示词获得模型生成的答案及其 verbalized confidence（口头化置信度，即模型用数值或语言表达的自我信心）。同一道题在多个 confidence-steering prompts（置信度引导提示）下会产生多组“答案—置信度”观测；这些观测既包含答案之间的一致或冲突，也包含模型对不同答案报告的数值信号。核心背景问题是：这些自我报告的置信度通常具有一定的排序或相对可信信息，但其数值尺度可能随提示层级、模型和数据集变化，因而不能直接当作真实正确概率。置信度校准的目标，是使预测概率与大量样本上的经验正确率相匹配；本文进一步把多次观测整合为候选答案层面的概率，并保留“所有候选答案都错误”的可能性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**黑盒 verbalized confidence 与置信度校准**

黑盒表示只能访问模型的输入输出，不能读取内部 logits 或条件词概率；verbalized confidence 是模型针对自己答案报告的信心数值。置信度校准要求预测的概率与答案实际正确的频率相符，例如被模型报告为约 $0.8$ 可信的一组答案应大致有 $80\%$ 正确。

</div>
<div class="concept-item" markdown="1">

**多观测不确定性估计**

对同一道题重复采样或改变提示词，可以得到多个答案，用答案一致性、样本分布或语义差异来估计不确定性。本文的观测更丰富，因为每个输出同时包含候选答案和模型报告的置信度，而不是只有答案是否重复。

</div>
<div class="concept-item" markdown="1">

**Dirichlet 分布与软证据**

Dirichlet 分布是定义在多个离散类别概率上的分布，可用一组证据参数表示各类别获得了多少支持。DirEAG 将每个答案—置信度观测转换为对候选答案类别及额外空状态的软证据，再累积这些证据，从而避免把单次自我报告直接等同于真实概率。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

对于每道数学题，固定的黑盒大语言模型在多个置信度引导提示下生成若干答案—置信度观测。设不同观测中出现的答案构成有限候选集合；系统需要利用这些观测及校准数据，输出最终被选答案的正确概率，同时尽可能保持合理的答案选择能力。该设定允许不同提示产生不同的置信度尺度，也允许多个观测给出冲突答案。重要假设是：自我报告的置信度可能不是可直接解释的概率，但仍可能携带与正确性相关的有效信息。为处理候选集合不完备的情况，方法增加一个 null state（空状态），表示“生成的所有候选答案都不正确”；否则，仅在候选答案之间聚合会被迫把概率分配给至少一个错误候选。本文是后处理方法，不修改或微调产生观测的基础模型；其输入是已有的多组答案—置信度观测及校准样例，输出是候选答案的聚合评分、选定答案以及经最终二元校准后的答案置信度。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

一道待解的数学问题。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{A}(x)$**

问题 $x$ 的候选答案集合，由多个置信度引导提示产生的答案去重得到。

</div>
<div class="notation-item" markdown="1">

**$a_i$**

候选答案集合中的第 $i$ 个离散答案状态。

</div>
<div class="notation-item" markdown="1">

**$a_\varnothing$**

额外的空状态，表示所有已生成候选答案均不正确；它不是某个具体数值答案。

</div>

</div>

**直接相关的工作**

- **SteerConf**: SteerConf 通过对同一道题使用不同的置信度引导提示，获得多组答案—置信度观测，再进行聚合；它直接启发了本文的多提示设定。区别在于，本文将聚合明确建模为校准问题，用校准样例学习不同提示和任务条件下的报告偏差，并以 Dirichlet 证据处理候选答案及空状态，而不是仅依赖描述性统计或启发式规则。
- **Self-consistency、sample consistency 与 semantic entropy**: 这些多观测方法主要依据多次生成的答案一致性、样本分布或语义多样性估计不确定性，因此能够反映输出变化。本文认为它们通常没有直接建模自我报告置信度的数值含义；DirEAG 保留每个观测中的答案和置信度，并学习如何将置信度转换为候选答案层面的证据。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在数学推理中，系统不仅要给出答案，还应说明该答案是否可信。若模型对错误答案给出高置信度，使用者可能受到误导；若置信度不能反映答案正确性，也就难以据此筛选、复核或部署模型。黑盒设置下通常无法直接取得可靠的内部概率，因此研究需要利用模型自行报告的置信度来估计答案级可信度。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **答案一致性、采样一致性与熵类方法**：通过多次生成答案，观察答案是否一致，或根据输出分布的熵衡量不确定性。这类方法主要利用输出之间的变化程度来判断模型是否稳定。
- **多提示置信度询问与启发式聚合**：在不同的置信度引导提示下多次询问模型，使其生成答案及口头报告的置信度，再使用直接平均、描述性统计或类似 SteerConf 的规则合并这些分数。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 一致性、采样变化和熵主要描述不同输出之间是否相同，却没有直接学习口头置信度数值对应实际正确率的含义；因此可能忽略有用的数值信息，或把输出稳定性误当作答案可信度。
- 直接平均或启发式合并默认不同提示、模型和数据集中的置信度具有可直接比较的尺度，无法处理模型报告偏差随提示条件和任务变化而改变的情况；其后果是聚合结果未必经过校准，即报告为较高的置信度不一定对应相称的正确概率。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未充分解决这样一个黑盒校准问题：如何利用多个提示下的、具有尺度偏移的口头置信度报告，将它们学习性地转换为候选答案层面的正确概率，同时保留模型报告中的有效排序信息，并表示“所有生成候选答案都错误”的情况。

</div>
<div markdown="1"><span>核心问题</span>

给定同一道数学题在多个置信度引导提示下产生的答案—置信度观测，能否通过少量校准参数学习每类报告对候选答案的证据贡献，并结合显式的空状态，得到比直接平均和启发式聚合更可靠的答案选择与置信度？

</div>
<div markdown="1"><span>作者直觉</span>

口头置信度不宜被直接当作概率，但也不应完全丢弃。更合理的做法是把每次报告看作对某个候选答案的软证据，利用校准样例学习不同提示层级的证据强度，再在候选答案和“无候选答案正确”的空状态之间累积这些证据。这样既能利用报告所包含的相对信息，又能允许其数值尺度存在偏差；随后再对最终选中答案的概率进行二元校准，以修正聚合证据与实际正确率之间的剩余尺度差异。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

DirEAG处理同一道数学题在五种置信度引导提示下产生的答案—置信度观测。它先用带提示级偏置的单调校准将原始自报置信度映射到可比较尺度，再把校准后的置信度作为对候选答案的软证据，联合一个表示“正确答案不在候选集合中”的空状态进行Dirichlet证据聚合，最后将所选答案的后验质量转换为跨样本可解释的正确概率。直观而言，该方法不是简单平均五次置信度，而是同时考虑答案是否重复、不同提示的可靠性、低置信度所暗示的候选缺失，以及最终概率是否符合真实正确率。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多提示置信度 elicitation

使用从谨慎到自信的五个confidence-steering prompts分别查询黑盒语言模型，得到$L=5$个答案—置信度观测$D_i=\{(a_{i\ell},q_{i\ell})\}_{\ell=1}^{L}$，其中$a_{i\ell}$是第$\ell$个答案，$q_{i\ell}$是模型口头报告的置信度。

<div class="method-step__io" markdown="1">

**输入**：数学问题 $x_i$。<br>
**输出**：同一问题的多次观测$D_i$，以及由不同观测答案构成的候选集合$A_i=\{a_{i\ell}:\ell=1,\ldots,L\}$。

</div>

**直观理解**：可以把五种提示看作让同一个模型以五种不同的“自信语气”回答。这样获得的不是五个独立问题答案，而是对同一答案空间的多份、可能带有不同尺度偏差的证词。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提示级置信度校准

先将边界值裁剪到$(\epsilon,1-\epsilon)$，再使用带提示级偏置$b_\ell$和共享正斜率$s=\operatorname{softplus}(r)>0$的Platt-style单调变换，得到校准置信度$\widetilde q_{i\ell}$。偏置允许不同提示的报告基准移动，共享斜率限制参数规模并保持置信度排序不被反转。

<div class="method-step__io" markdown="1">

**输入**：原始置信度$q_{i\ell}\in[0,1]$及提示级参数。<br>
**输出**：处于对齐尺度上的校准观测$\{(a_{i\ell},\widetilde q_{i\ell})\}_{\ell=1}^{L}$。

</div>

**直观理解**：如果“谨慎提示”通常只报0.6而“自信提示”通常报0.9，这两个数字不能直接比较；该步骤像给不同温度计分别调零和调刻度，但仍保持同一提示内部高分高于低分。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 扩展候选空间中的Dirichlet证据聚合

构造扩展状态空间$S_i=A_i\cup\{\varnothing\}$，其中$\varnothing$表示正确答案不在生成候选中；对每个候选答案累积由$w_\ell\widetilde q_{i\ell}$加权的证据，对空状态累积基础项和$w_\ell(1-\widetilde q_{i\ell})$表示的低置信度证据。将Dirichlet浓度参数归一化为后验均值$P_i(a\mid D_i)$，并在生成候选中选择后验最高者$\hat a_i$。

<div class="method-step__io" markdown="1">

**输入**：候选集合$A_i$、校准置信度$\widetilde q_{i\ell}$和学习到的提示可靠性权重$w_\ell$。<br>
**输出**：候选答案及空状态的后验分布、所选答案$\hat a_i$和其原始聚合置信度$\hat c_i=P_i(\hat a_i\mid D_i)$。

</div>

**直观理解**：重复且高置信度的答案会获得更多支持，但不可靠提示的支持会被降权；如果所有回答都不够可信，证据可以流向“候选集合可能漏掉正确答案”的空状态，而不是被迫支持某个错误数字。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 类别训练与最终二元校准

若$y_i\in A_i$，将目标状态设为$y_i$；否则设为$\varnothing$，并最小化目标状态的分类负对数似然以学习$w_\ell,b_\ell,s,\eta,\beta_0,\gamma$。随后在独立的held-out calibration split上，用二参数Platt变换将$\hat c_i$映射为最终正确概率$\hat c_i^{\mathrm{cal}}$。

<div class="method-step__io" markdown="1">

**输入**：带金标准答案$y_i$的校准数据、聚合后的状态分布和所选答案质量$\hat c_i$。<br>
**输出**：最终答案$\hat a_i$和用于ECE、Brier score等二元校准指标的概率$\hat c_i^{\mathrm{cal}}$。

</div>

**直观理解**：Dirichlet聚合回答的是“在这道题的候选和空状态中，哪个状态得到多少支持”；最终校准再回答“长期来看，报出这个分数的答案有多大比例正确”。两者分别处理候选内部比较和跨题目的概率可信度。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 提示级Platt-style置信度校准

$$
\widetilde q_{i\ell}=\sigma\left(b_\ell+s\operatorname{logit}(q_{i\ell}^{\epsilon})\right),\qquad s=\operatorname{softplus}(r)>0,\qquad q_{i\ell}^{\epsilon}=\operatorname{clip}(q_{i\ell},\epsilon,1-\epsilon),\quad 0<\epsilon<\frac{1}{2}
$$

**符号说明**

- $q_{i\ell}$：问题$i$在第$\ell$个提示下得到的原始自报置信度。
- $q_{i\ell}^{\epsilon}$：裁剪到开区间$(\epsilon,1-\epsilon)$后的置信度，避免$\operatorname{logit}$在0或1处无定义。
- $\widetilde q_{i\ell}$：校准后的置信度。
- $b_\ell$：第$\ell$个confidence-steering prompt的提示级偏置。
- $s$：所有提示共享的正斜率，保证变换单调不减。
- $\sigma$：logistic sigmoid函数。
- $r$：用于通过softplus产生正斜率$s$的无约束参数。

<div class="equation-explanation" markdown="1">

**直观理解**：公式将每个提示产生的置信度转换到共同概率尺度。$b_\ell$纠正某种提示一贯偏高或偏低的报告习惯，正的共享$s$保证原来更自信的报告不会被校准成更低的报告。<br>
**原文位置**：第3.1节，式(1)–(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### Dirichlet浓度与聚合目标

$$
\alpha_i(a)=\frac{\eta}{|A_i|+1}+\sum_{\ell:a_{i\ell}=a}w_\ell\widetilde q_{i\ell},\quad a\in A_i;\qquad \alpha_i(\varnothing)=\frac{\eta}{|A_i|+1}+\beta_0+\gamma\sum_{\ell=1}^{L}w_\ell(1-\widetilde q_{i\ell});\qquad P_i(a\mid D_i)=\frac{\alpha_i(a)}{\alpha_i(\varnothing)+\sum_{b\in A_i}\alpha_i(b)};\qquad \mathcal L(\theta)=-\sum_i\log P_i(t_i\mid D_i;\theta)+\lambda\lVert\theta\rVert_2^2
$$

**符号说明**

- $\alpha_i(a)$：问题$i$的候选答案$a$对应的Dirichlet浓度，也就是未归一化证据量。
- $\alpha_i(\varnothing)$：空状态的浓度，表示正确答案可能不在候选集合中的证据。
- $\eta$：分配给所有状态的对称先验总强度。
- $A_i$：问题$i$的不同生成候选答案集合。
- $w_\ell$：第$\ell$个提示的学习得到的可靠性权重，且非负。
- $\beta_0$：空状态的基础浓度。
- $\gamma$：低校准置信度转化为空状态证据的强度。
- $P_i(a\mid D_i)$：在观测$D_i$下状态$a$的Dirichlet后验均值。
- $t_i$：训练目标状态：若金标准答案出现在$A_i$中则为该答案，否则为$\varnothing$。
- $\theta$：待学习参数集合，包括$w_\ell,b_\ell,s,\eta,\beta_0,\gamma$。
- $\lambda$：L2正则化系数。

<div class="equation-explanation" markdown="1">

**直观理解**：前半部分把每次观测转成可累加的证据，再在候选答案和空状态之间归一化为概率。训练时提高真实目标状态的后验概率，并用正则项抑制参数过度拟合；因此模型学习的是哪些提示更可靠、置信度如何影响证据，以及何时应相信空状态。<br>
**原文位置**：第3.2节式(5)–(7)，第3.3节式(10)–(12)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练分为两部分。第一部分在校准数据上最小化类别负对数似然$\mathcal L(\theta)=-\sum_i\log P_i(t_i\mid D_i;\theta)+\lambda\lVert\theta\rVert_2^2$，目标状态$t_i$在金标准答案出现于候选集合时为该答案，否则为空状态；非负参数通过softplus等正参数化实现。第二部分冻结或使用已得到的聚合分数，在held-out calibration split上拟合$\hat c_i^{\mathrm{cal}}=\sigma(a+b\operatorname{logit}(\hat c_i))$，使最终分数对应跨样本的经验正确率。前者学习候选级证据结构，后者学习二元正确性概率的最终尺度。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 提示依赖的单调置信度校准**

对裁剪后的$q_{i\ell}$应用$\widetilde q_{i\ell}=\sigma(b_\ell+s\operatorname{logit}(q_{i\ell}^{\epsilon}))$，其中$b_\ell$是第$\ell$个提示的偏置，$s>0$是共享斜率，$\sigma$是logistic sigmoid。该设计使用较少参数刻画不同confidence-steering levels的尺度偏移，同时不破坏每个提示内部的置信度顺序。

> 直观理解：它只校正不同提示“报分偏高或偏低”的系统差异，不试图重新生成答案，因此适合黑盒模型。

**2. 带空状态的加权Dirichlet证据聚合**

状态空间为$S_i=A_i\cup\{\varnothing\}$。候选答案的浓度参数由对相同答案的$w_\ell\widetilde q_{i\ell}$加权累积，空状态则由基础浓度$\beta_0$和低置信度证据$\gamma\sum_\ell w_\ell(1-\widetilde q_{i\ell})$增强；$\eta$提供对各状态的对称先验强度。

> 直观理解：该模块把多次回答当作可加权的“证据”，而不是把分数机械平均；空状态使系统能够明确表达“所有生成答案都可能不对”。

**3. 最终二元Platt校准**

对最大后验候选的聚合质量$\hat c_i$应用$\hat c_i^{\mathrm{cal}}=\sigma(a+b\operatorname{logit}(\hat c_i))$，其中$a,b$在保留校准集上拟合。该步骤不改变候选选择或Dirichlet证据，只修正所选答案分数到真实正确概率的映射。

> 直观理解：即使候选之间的相对支持判断合理，分数0.8也未必对应80%的真实正确率；这个模块专门修正这种整体概率刻度误差。

**训练与推理**

训练时，对每个校准样本保存五个提示产生的$D_i$及金标准答案$y_i$；先拟合提示级偏置、共享斜率、提示可靠性权重、Dirichlet先验和空状态参数，再在独立保留集上拟合最终二元Platt参数。推理时，对新问题执行同样的五提示查询和置信度校准，构造$A_i$与$S_i$，计算各状态的Dirichlet后验均值，选择$\arg\max_{a\in A_i}P_i(a\mid D_i)$，并将所选答案的后验质量输入最终校准器，输出答案和校准正确概率。

**复现信息**

方法依赖五级confidence-steering elicitation设计；提示从谨慎到高度自信，具体提示文本在所给方法摘录中未完整呈现。候选集合按生成答案去重，空状态与候选答案共享同一归一化状态空间；可靠性权重和其他非负浓度相关参数采用正参数化。实现和实验所需的完整超参数、数据划分、优化器、训练轮数及裁剪阈值在所给章节摘录中原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：数学文字题基准，使用官方训练集—测试集划分；用于检验常规小学数学推理场景下的答案选择与置信度校准。
- SVAMP：数学文字题基准，采用 $5$ 折交叉拟合；用于检验模型在题目结构变化下的泛化能力。原文未明确报告样本规模。
- GSM-Hard：更具挑战性的数学推理基准，采用 $5$ 折交叉拟合；用于检验方法在模型准确率较低、置信度失真更明显的困难场景中的表现。原文未明确报告样本规模。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy (Acc)**

所选最终答案与标准答案相符的比例，衡量答案选择能力。 （越高越好；但它不评价置信度数值是否与真实正确概率匹配。）

</div>
<div class="metric-item" markdown="1">

**ECE 与 Brier score**

ECE 将预测置信度按 $10$ 个等宽区间分箱，比较置信度与实际正确率的差异；Brier score 衡量概率预测与正确性标签之间的平方误差，二者都评价概率校准。 （越低越好；较低表示置信度的数值尺度更接近实际正确概率。）

</div>
<div class="metric-item" markdown="1">

**AUROC、PR-P 与 PR-N**

这些指标评价置信度对正确与错误样本的排序能力；AUROC 衡量区分正确和错误预测的总体排序，PR-P 将正确预测作为正类，PR-N 将错误预测作为正类。 （越高越好；它们主要衡量能否优先识别可靠答案或潜在错误，而不是概率值本身是否校准。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 主比较：Qwen2.5-7B、Mistral-7B 和 Gemma-2-9B-it 在 GSM8K、SVAMP、GSM-Hard 上的端到端结果

<div class="result-value" markdown="1">

作者报告 DirEAG 在多数模型—数据集组合上取得更低的 ECE，并在若干设置中同时改善答案选择；例如 Qwen GSM8K 的 DirEAG 为 Acc $0.8908$、ECE $0.0280$、Brier $0.0736$，而 Mean confidence 为 Acc $0.8992$、ECE $0.1049$、Brier $0.0840$；Mistral GSM8K 的 DirEAG 为 Acc $0.6308$、ECE $0.0585$、Brier $0.1486$，优于 SteerConf 的 Acc $0.5102$、ECE $0.0837$、Brier $0.1647$。

</div>

这表明 DirEAG 的主要优势是把置信度报告校准到更合理的概率尺度，而不是在所有任务上都提高最终答案准确率。Qwen GSM8K 中 Mean confidence 的准确率略高，因此不能据此声称 DirEAG 始终选择最佳答案；更稳妥的结论是，学习式证据聚合通常比直接平均或启发式聚合更能控制置信度偏差。

<div class="result-source" markdown="1">

来源：Table 1，Model: Qwen2.5-7B，GSM8K；对应列为 Acc、ECE、Brier、AUROC、PR-P、PR-N

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

DirEAG 0.8908 0.0280 0.0736 0.8621 0.9744 0.5136

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 校准与错误排序的区分：agreement-based 基线和置信度聚合基线

<div class="result-value" markdown="1">

答案一致性方法在答案选择和错误排序上仍然很强，但不保证概率尺度校准。例如 Qwen GSM8K 的 Self-consistency 达到 Acc $0.9265$、ECE $0.0170$、AUROC $0.8542$，而 DirEAG 为 Acc $0.8908$、ECE $0.0280$、AUROC $0.8621$；在 Gemma GSM-Hard 上，SteerConf 的 ECE 为 $0.0844$、AUROC 为 $0.8394$，DirEAG 的 ECE 为 $0.0432$、AUROC 为 $0.8274$。

</div>

实验说明“能否排序出可能错误的样本”和“置信度是否等于真实正确概率”是两个不同目标。Self-consistency 可能依靠答案重复性获得较高准确率和较好校准，SteerConf 也可能在错误排序上占优；DirEAG 的价值主要在于综合答案身份与 verbalized confidence，并使概率数值更可解释。因此不能仅凭单一指标判断方法优劣。

<div class="result-source" markdown="1">

来源：Section 4.2 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Overall, these results show that multi-output structure is useful, but directly using agreement or reported scores does not consistently yield calibrated probabilities.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 实例级信息诊断：DirEAG 与模型—数据集常数准确率预测器的比较

<div class="result-value" markdown="1">

在全部九个模型—数据集组合中，DirEAG 的 Brier score 都低于常数 base-rate 诊断，绝对降低幅度为 $0.021$ 至 $0.086$；其 AUROC 相对常数预测器的提升为 $0.229$ 至 $0.362$。常数预测器的 AUROC 固定为 $0.5$，因为它不能区分容易和困难的实例。

</div>

该诊断检验 DirEAG 是否只是恢复每个模型和数据集的平均成功率。结果支持作者的解释：DirEAG 能依据每个实例的答案—置信度观测给出不同的不确定性，从而识别更可能出错的题目。不过，base-rate 使用评估集经验准确率，属于有利但不可部署的参照，所以它适合做诊断，不适合被当作实际系统基线。

<div class="result-source" markdown="1">

来源：Section 4.4 Diagnostic Analysis of Learned Uncertainty，Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Figure 2 shows that DirEAG obtains lower Brier score than the constant diagnostic in all nine model–dataset settings, with absolute reductions ranging from 0.021 to 0.086.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验只覆盖三个数学推理数据集、三个开放权重模型和五个答案—置信度观测；因此对其他任务、闭源模型、不同提示设计以及不同观测数量的可迁移性，原文未明确报告。
- 主实验使用了最终 Platt calibration，且 base-rate 诊断明确使用评估集经验准确率；尽管论文说明被评估样本排除在拟合之外，实际部署中的跨分布校准稳定性、校准数据需求和成本仍缺少实验验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Vanilla：使用中性置信度提示产生单次答案—置信度输出，是直接 verbalized confidence 的基础参照，用来衡量提示引导和聚合是否带来收益。
- Mean confidence：对五次置信度报告直接求平均；检验简单平均能否处理不同提示水平带来的尺度偏移。
- Self-consistency 与 answer entropy：分别利用五个普通采样答案的一致性或答案分布熵作为不确定性信号；二者合并为一类 agreement-based 对照，检验答案变化本身是否已经足够。
- SteerConf 与 Top-K：SteerConf 使用原始置信度引导聚合规则，直接对比启发式聚合；Top-K 一次产生五个候选答案，作为单响应、多候选输出基线，检验多候选提示但无 DirEAG 学习聚合时的效果。

**实验想回答的问题**

- 在不同模型与数学数据集上，DirEAG 是否能将多次提示得到的答案—置信度观测转化为更可靠的概率置信度，同时保持具有竞争力的答案选择能力？
- DirEAG 的性能来自哪些部分：答案计数、不同置信度提示的可靠性建模、置信度证据聚合，还是最终的二元概率校准？

**实验实现**

实验使用 Qwen2.5-7B-Instruct、Mistral-7B-Instruct-v0.3 和 Gemma-2-9B-it 三个指令微调开放权重模型。DirEAG、Mean confidence 和 SteerConf 尽可能共享五个答案—置信度观测；Self-consistency 和 answer entropy 使用五个普通采样；Top-K 一次提示模型产生五个候选答案。GSM8K 使用官方划分，SVAMP 与 GSM-Hard 使用 $5$ 折交叉拟合。被评估样本同时排除在 DirEAG 参数拟合和最终 Platt calibration 之外，模型—数据集组合之间固定优化设置；完整实现细节由代码提供。实验还将 DirEAG 与一个常数 base-rate 诊断比较：该诊断给每个样本赋予同一置信度，即对应模型—数据集组合的经验准确率。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 答案计数与提示级可靠性：Count-only + Cal. 对比 + Level Reliability | 加入 level reliability 后变化很小。例如 Qwen GSM8K 的 Count-only + Cal. 为 Acc $0.8863$、ECE $0.0366$、Brier $0.0751$，加入后为 Acc $0.8863$、ECE $0.0393$、Brier $0.0755$；Mistral SVAMP 的 ECE 从 $0.0491$ 变为 $0.0488$，准确率均为 $0.7380$。 | 该消融隔离不同置信度 steering level 是否需要单独学习可靠性权重。结果支持作者的判断：答案出现次数本身已经是强信号，提示级可靠性权重不是主要收益来源；但这只说明在当前数据、模型和拟合协议下增益有限，不能证明该模块在所有提示设计中都无用。 | Table 2，Model: Qwen2.5-7B，GSM8K；另见相邻的 + Level Reliability 行<br><span class="experiment-evidence">GSM8K Count-only + Cal. 0.8863 0.0366 0.0751 0.8572 0.9710 0.5607</span> |
| 置信度证据与最终二元校准：+ Conf. evidence 对比 Full DirEAG | 去掉最终二元校准时，置信度证据能够改变候选评分并有时提高准确率，但原始 posterior mass 的尺度严重失准；例如 Qwen GSM8K 的 + Conf. evidence 为 Acc $0.8908$、ECE $0.4276$、Brier $0.2619$，Full DirEAG 在准确率不变的情况下将 ECE 和 Brier 降至 $0.0280$ 和 $0.0736$。Mistral GSM-Hard 中，ECE 由 $0.1006$ 降至 $0.0387$，Brier 由 $0.1405$ 降至 $0.1245$。 | 该结果把两个作用分开：Dirichlet evidence aggregation 负责在候选答案层面利用置信度并可能改变答案选择，最终 binary calibration 负责把被选答案的概率质量重新映射到可信尺度。由于校准器是单调的且只在选定答案之后应用，它不会改变候选排序；因此准确率差异主要来自证据聚合，而 ECE、Brier 的改善主要来自最终概率尺度修正。 | Section 4.3 Internal Ablation；数值见 Table 2，Model: Qwen2.5-7B，GSM8K<br><span class="experiment-evidence">Full DirEAG preserves the candidate-level effects of confidence evidence while applying final binary calibration to correct the selected-answer probability scale.</span> |

**定性案例**

- null state 诊断：Figure 3 比较正确预测与“标准答案不在生成候选集”时的平均 null-state probability，结果显示后者持续更高。它支持 DirEAG 能识别“候选答案集合可能整体不包含正确答案”的情况，但该图提供的是分组平均趋势而非具体题目的逐例解释，不能单独证明 null state 对每个错误实例都有效。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The core contribution is calibrated confidence estimation for LLM mathematical reasoning through Dirichlet evidence aggregation.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`5e8faa53c7f90dee526b2c385437719e8f29561b68a5d0851dde05a668f6e83f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
