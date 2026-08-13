---
title: "[论文解读] Reinforcing Step-level Reasoning for Effective Self-Correction in LLMs"
description: "[arXiv 2608.11573][LLM Reasoning] 本文提出两阶段框架 SFS-DPO：先强化小型大语言模型的逐步推理能力，再训练其在推理过程中识别并改正错误步骤，从而提升数学推理的可靠性。"
arxiv_id: "2608.11573"
announcement_date: "2026-08-13"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-13T02:53:00.404690+00:00"
source_sha256: "c9f746e8804ecfae2f7679bcb398addeb9a738279fde6a0c5477e798e72e0ce6"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "LLM 其他"
  - "大语言模型"
  - "数学推理"
  - "步骤级推理"
  - "偏好优化"
  - "信用分配"
  - "自验证"
  - "自纠错"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.11573</p>

# Reinforcing Step-level Reasoning for Effective Self-Correction in LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-13</span>
<span><strong>作者</strong> Vu Duc Anh, Nhat M. Hoang, Do Xuan Long, Cong-Duy Nguyen, Ponhvoan Srey, Luu Anh Tuan</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Nanyang Technological University, Singapore；Affiliation: National University of Singapore, VinUniversity, Vietnam, Institute for Infocomm Research (IR), A*STAR, {vuducanh001, hoangmin003, ponhvoan002；Affiliation: National University of Singapore；Institute for Infocomm Research (IR), A*STAR, {vuducanh001, hoangmin003, ponhvoan002</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.11573v1) · [PDF 下载](https://arxiv.org/pdf/2608.11573v1) · **关键词** 大语言模型, 数学推理, 步骤级推理, 偏好优化, 信用分配, 自验证, 自纠错<br>


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

本文提出两阶段框架 SFS-DPO：先强化小型大语言模型的逐步推理能力，再训练其在推理过程中识别并改正错误步骤，从而提升数学推理的可靠性。

**不用术语来说**：小型大语言模型解决复杂数学题时，前面某一步一旦出错，后续计算往往会沿着错误方向继续展开。现有训练方法通常只教模型在多个后续推理方向中偏好较好的一个，却没有充分教会模型回头检查已经写出的错误步骤并进行修改，因此模型即使知道什么样的续写更好，也未必能在实际推理时有效地自我纠错。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 SFS-DPO 两阶段框架：第一阶段通过逐步偏好优化增强局部推理能力，第二阶段针对错误步骤训练显式的自我验证与自我纠正，把“偏好正确续写”进一步转化为“发现并修复既有错误”的能力。
- 提出教师辅助变体 SFS-DPO-R，引入更强模型生成的错误验证解释，为模型提供更明确的纠错信号；作者同时指出，该设计会带来教师依赖，并可能传播教师的偏差或错误。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型的数学推理与内在自纠错研究。复杂数学解答通常由连续推理步骤组成，小型大语言模型一旦在较早步骤出错，错误便可能沿后续推导传播；而仅依据完整答案优劣进行训练，难以判断具体是哪一步造成失败。为提供更精确的学习信号，相关研究转向步骤级目标：在正确推理前缀之后比较候选下一步，使模型学习偏好正确延续。本文进一步关注一个不同但紧密相关的问题：模型不仅要在生成前偏好正确步骤，还要能检查自己已经生成的错误步骤、将其改写为更合理的步骤，并基于修正结果继续推理。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**步骤级偏好优化**

在相同且正确的推理前缀下，将较好的下一步与较差的下一步配对训练，使模型提高前者的相对偏好。它把完整解答提供的粗粒度反馈定位到局部步骤，从而改善复杂推理中的信用分配。

</div>
<div class="concept-item" markdown="1">

**自验证与自纠错**

自验证是模型判断自身中间推理是否存在错误，自纠错则是在发现错误后生成修订步骤并继续求解。本文所说的内在自纠错强调由同一模型完成检查和修改，而非只依赖外部验证器在最终输出后给出评价。

</div>
<div class="concept-item" markdown="1">

**信用分配**

信用分配是确定最终成功或失败应归因于哪些生成决策的问题。数学解答可能包含很长的正确前缀，因此只看最终答案会给前面各步提供含糊信号，而步骤级监督能更直接地指向首个错误及其候选替代步骤。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务设置是让大语言模型对复杂数学问题生成多步解答，并在推理过程中处理自身错误。给定题目以及截至当前步骤的推理前缀，模型首先需要选择合理的下一步；若已经生成错误步骤，则还需验证该步骤、将其修订为更优的延续，并从修正后的轨迹继续推导至答案。论文假设局部步骤质量会影响整条推理链，尤其是早期错误可向后传播；因此训练既要强化正确前缀条件下的步骤偏好，也要显式学习“发现错误、改写错误、继续推理”的行为。研究重点是小型大语言模型的数学推理，并同时考察域内和域外设置下这种能力能否保持稳健。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Step-DPO**: 它在正确推理前缀条件下比较下一步候选，并明确针对轨迹中的首个错误步骤，以局部偏好信号改善信用分配。本文将这类步骤级偏好优化用作第一阶段初始化，但进一步加入显式自验证和自纠错训练，以弥补其只偏好更好延续、却不修订已生成错误的不足。
- **SCoRe**: 它通过基于模型自生成数据的多轮在线策略强化学习训练内在自纠错，并指出离线纠错训练可能面临分布偏移与行为坍塌。本文同样研究模型自身纠错，但采用“步骤级强化学习偏好初始化，再训练步骤级纠错”的两阶段路径；原文作者称该初始化比从零开始或监督微调带来更稳健的下游自纠错。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在复杂数学推理中，答案由一系列相互依赖的中间步骤构成；较早出现的局部错误可能持续影响后续步骤，最终导致整条解题过程失败。对参数规模较小的模型而言，仅提升最终答案正确率不足以解决这一问题，实际需要模型在生成过程中检查当前步骤，并在错误继续扩散之前主动修正。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **逐步训练目标**：与只依据最终答案提供监督相比，这类方法把学习信号定位到中间推理步骤，使模型能够区分局部步骤或局部续写的质量，从而获得更细粒度的推理反馈。
- **逐步偏好优化**：给定同一推理上下文，该方法让模型提高正确或更优续写的相对偏好，并降低错误续写的偏好。其重点是选择接下来应当生成的较好推理方向，而不是显式回看和改写模型已经生成的错误步骤。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有逐步方法主要优化“正确续写优于错误续写”的相对偏好，却没有直接训练模型验证已经生成的步骤；因此，局部偏好能力不一定会自然转化为推理时的错误检测能力。
- 即使模型能够识别较优的后续方向，若训练过程没有展示如何从一个具体错误步骤退回并改写为正确步骤，模型仍可能沿着原有错误继续推理，使早期错误传播到整个解答。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究提供了细粒度的步骤级偏好信号，但“评价哪个续写更好”与“在实际生成中识别、解释并修复自己已经犯下的错误”之间仍存在训练目标上的缺口。尚需一种机制，将局部步骤偏好系统地转化为可执行的多步自我纠错行为，并检验这种能力能否跨模型骨干以及分布内、分布外数学任务稳定生效。

</div>
<div markdown="1"><span>核心问题</span>

在逐步偏好学习的基础上，显式加入针对错误步骤的自我验证与修正训练，是否能使中等规模的大语言模型在推理时更有效地发现并纠正自身错误，从而获得比既有步骤级训练方法更稳健的数学推理表现？

</div>
<div markdown="1"><span>作者直觉</span>

逐步偏好训练可以先让模型形成局部判断标准，即知道在当前上下文中哪一种推理延续更合理；随后再用包含“发现错误、改写错误、继续求解”的训练轨迹，教模型把这种判断标准用于自身输出。直观地说，第一阶段训练模型辨别哪一步更好，第二阶段训练模型在自己走错时真正停下来换路；教师生成的解释则进一步说明错误在哪里以及为何需要修改，使纠错信号更具体。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SFS-DPO把自我纠错建模为带显式“发现错误—修复错误”动作的多步生成过程。给定问题$x$，策略模型$\pi_\theta$自回归地产生轨迹$(s_1,\ldots,s_M,\hat y)$；其中一个步骤既可以是普通解题步骤，也可以是指出前一步有误的检测步骤，或替换错误推理的修复步骤。方法不直接联合学习所有能力，而是采用两阶段训练：先通过步骤级偏好优化提高模型区分正确与错误中间步骤的能力，再通过自我纠错偏好优化，使模型在已经生成错误步骤后更倾向于检测并修复错误，而不是沿错误路径继续生成。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造步骤级初始化偏好样本

把共享同一问题和推理前缀的$s_k^+$与$s_k^-$组成步骤级偏好对，并规定$s_k^+\succ s_k^-$。这种局部比较控制了上下文差异，使训练信号集中于第$k$步本身是否合理。

<div class="method-step__io" markdown="1">

**输入**：输入问题$x$、错误发生前的正确前缀$\{s_i\}_{i=1}^{k-1}$、候选正确步骤$s_k^+$和候选错误步骤$s_k^-$。<br>
**输出**：步骤级偏好数据集$\mathcal D$，用于初始化阶段的策略优化。

</div>

**直观理解**：可以把它理解为在同一道题、同一段已有解法之后，要求模型从两个“下一步”中选出正确者，而不是只看整份答案最后是否正确。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤级偏好初始化

最小化$\mathcal L_{\mathrm{Pre}}(\theta)$，提高正确步骤$s_k^+$的条件对数概率并压低错误步骤$s_k^-$的条件对数概率；偏好差经系数$\beta$缩放后送入逻辑函数$\sigma$。作者采用文献[13]的步骤级偏好优化框架实现该阶段。

<div class="method-step__io" markdown="1">

**输入**：待训练策略$\pi_\theta$与步骤级偏好数据集$\mathcal D$。<br>
**输出**：具有较强局部步骤判断与生成能力的初始化策略模型。

</div>

**直观理解**：这一阶段先训练模型把每一步走稳，为后续同时执行“找错”和“改错”提供基础，减少两个困难任务一起学习时相互放大的噪声。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造自我纠错偏好对

在共同上下文$(x,\{s_i\}_{i=1}^{k-1},s_k^-)$下构造优选续写$c_k^+$和拒选续写$s_{k+1}^-$。SFS-DPO令$c_k^+=\{d_{k-1},s_k^+\}$；SFS-DPO-R则令$c_k^+=\{d_{k-1},r_{k-1},s_k^+\}$，额外加入教师生成的错误解释$r_{k-1}$。

<div class="method-step__io" markdown="1">

**输入**：问题$x$、正确前缀$\{s_i\}_{i=1}^{k-1}$、已出现的错误步骤$s_k^-$、错误未被处理时的后续步骤$s_{k+1}^-$，以及正确修复步骤$s_k^+$。<br>
**输出**：自我纠错偏好数据集$\mathcal D_{\mathrm{SC}}$，其中优选项显式检测并修复错误，拒选项沿错误轨迹继续。

</div>

**直观理解**：模型看到自己已经走错一步后，需要在“承认并改正”和“装作没错继续推”之间作选择；带R版本还提供教师解释，告诉模型错在哪里。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自我纠错偏好优化

最小化$\mathcal L_{\mathrm{SC}}(\theta)$，增大优选纠错续写$c_k^+$相对于参考模型的对数概率比，并减小未处理错误的续写$s_{k+1}^-$对应的对数概率比。冻结的$\pi_{\mathrm{ref}}$约束策略不要为了满足偏好而无界偏离初始化模型。

<div class="method-step__io" markdown="1">

**输入**：初始化后的策略$\pi_\theta$、冻结参考模型$\pi_{\mathrm{ref}}$以及$\mathcal D_{\mathrm{SC}}$。<br>
**输出**：SFS-DPO或SFS-DPO-R模型，能够在多步推理中生成显式错误检测与针对性修复。

</div>

**直观理解**：训练奖励“停下来检查并改正”的续写，同时惩罚“顺着错误继续写”的续写；参考模型相当于锚点，用来限制训练造成的行为漂移。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 初始化阶段的步骤级偏好目标

$$
\mathcal{L}_{\mathrm{Pre}}(\theta)=-\mathbb{E}_{(x,\{s_i\}_{i=1}^{k-1},s_k^+,s_k^-)\sim\mathcal{D}}\left[\log\sigma\left(\beta\left(\log\pi_\theta(s_k^+\mid x,\{s_i\}_{i=1}^{k-1})-\log\pi_\theta(s_k^-\mid x,\{s_i\}_{i=1}^{k-1})\right)\right)\right]
$$

**符号说明**

- $\mathcal{L}_{\mathrm{Pre}}(\theta)$：初始化阶段需要最小化的步骤级偏好损失。
- $\theta$：待优化语言模型的参数。
- $x$：输入问题。
- $\{s_i\}_{i=1}^{k-1}$：第k步之前的正确推理前缀。
- $s_k^+$：在给定前缀之后应被偏好的正确第k步。
- $s_k^-$：在相同前缀之后应被拒绝的错误第k步。
- $\pi_\theta$：正在优化的策略语言模型。
- $\mathcal D$：由问题、前缀、正确步骤和错误步骤组成的步骤级偏好数据集。
- $\beta$：控制偏好差缩放强度的超参数。
- $\sigma$：逻辑函数，把正确与错误步骤的对数概率差映射为偏好概率。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标要求正确步骤的条件概率高于错误步骤；两者差距越大，损失越小。它先把模型训练成更可靠的“局部下一步选择器”，从而降低后续错误检测和修复联合学习时的复合误差。<br>
**原文位置**：第3.1节 Initialization Stage

</div>

</div>

<div class="equation-block" markdown="1">

#### 步骤式自我纠错偏好目标

$$
\mathcal{L}_{\mathrm{SC}}(\theta)=-\mathbb{E}_{(x,\{s_i\}_{i=1}^{k-1},s_k^-,c_k^+,s_{k+1}^-)\sim\mathcal{D}_{\mathrm{SC}}}\left[\log\sigma\left(\beta\log\frac{\pi_\theta(c_k^+\mid x,\{s_i\}_{i=1}^{k-1},s_k^-)}{\pi_{\mathrm{ref}}(c_k^+\mid x,\{s_i\}_{i=1}^{k-1},s_k^-)}-\beta\log\frac{\pi_\theta(s_{k+1}^-\mid x,\{s_i\}_{i=1}^{k-1},s_k^-)}{\pi_{\mathrm{ref}}(s_{k+1}^-\mid x,\{s_i\}_{i=1}^{k-1},s_k^-)}\right)\right]
$$

**符号说明**

- $\mathcal{L}_{\mathrm{SC}}(\theta)$：第二阶段需要最小化的步骤式自我纠错偏好损失。
- $s_k^-$：已经出现在推理轨迹中的错误第k步，也是两个候选续写共享的条件。
- $c_k^+$：优选的自我纠错续写；SFS-DPO中为检测信号与修复步骤，SFS-DPO-R中还包含教师错误解释。
- $s_{k+1}^-$：错误未被检测和处理时产生的后续错误步骤。
- $\pi_{\mathrm{ref}}$：冻结的参考模型，用于衡量策略相对原模型的概率变化。
- $\mathcal D_{\mathrm{SC}}$：包含错误上下文、优选纠错续写和拒选错误续写的自我纠错偏好数据集。
- $d_{k-1}$：显式指出上一错误步骤存在问题的检测信号。
- $r_{k-1}$：SFS-DPO-R中由外部教师生成的错误原因说明。
- $s_k^+$：用于替换错误步骤的正确推理步骤。
- $\beta$：缩放策略相对参考模型之偏好差的系数。

<div class="equation-explanation" markdown="1">

**直观理解**：公式比较策略模型相对参考模型对两类续写增加了多少偏好：训练希望纠错续写$c_k^+$的相对增幅更大，同时抑制继续犯错的$s_{k+1}^-$。因此模型学习的不是一般意义上的正确续写，而是在明确看到自身错误后选择检测、解释并修复的行为。<br>
**原文位置**：第3.2节 Step-wise Self-Correction；纠错续写定义见第3.2.1节和第3.2.2节

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：总训练过程是顺序执行而非把两个损失简单相加：先用$\mathcal L_{\mathrm{Pre}}$初始化$\pi_\theta$，使其在相同前缀下偏好正确中间步骤；随后以该模型为起点，用$\mathcal L_{\mathrm{SC}}$学习错误发生后的恢复行为。第二阶段采用相对于冻结模型$\pi_{\mathrm{ref}}$的概率比进行偏好优化，使$c_k^+$优于$s_{k+1}^-$；SFS-DPO与SFS-DPO-R使用相同目标，仅在$c_k^+$是否包含教师理由$r_{k-1}$上不同。作者的核心主张是，这种先增强步骤级推理、再训练自我纠错的分解能减少错误判断与错误修订同时学习造成的噪声和误差累积。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 步骤级偏好初始化模块**

该模块在相同上下文$(x,\{s_i\}_{i=1}^{k-1})$下比较$s_k^+$和$s_k^-$，直接优化局部中间步骤的相对概率。它针对的是后续自我纠错所依赖的步骤级判断基础，而不是仅用模板化监督让模型模仿某种纠错输出格式。

> 直观理解：如果模型连当前一步是否合理都分不清，就很难稳定地指出错误并生成正确替代方案；因此作者先单独补强这一基础能力。

**2. 纠错续写偏好模块**

该模块把已出现的$s_k^-$保留在条件上下文中，比较显式纠错续写$c_k^+$与未检测错误时的续写$s_{k+1}^-$。这种构造训练的是错误发生之后的恢复决策，而非重新从无错误前缀直接生成正确步骤。

> 直观理解：关键不只是让模型知道正确答案，而是让它在已经犯错的现实条件下学会回头修正；这更贴近实际自我纠错。

**3. 双变体纠错信号构造**

SFS-DPO使用检测信号$d_{k-1}$与修复步骤$s_k^+$组成$c_k^+$，不依赖外部教师解释；SFS-DPO-R在二者之间加入教师生成的理由$r_{k-1}$，明确说明$s_k^-$为何错误。两者共享同一偏好目标，区别只在优选纠错续写所包含的监督信息。

> 直观理解：基础版本只示范“这里错了，应该这样改”；带R版本还解释“为什么错”，信号更丰富，但训练数据依赖更强的外部模型。

**训练与推理**

训练时，首先从步骤级数据中抽取共享问题与正确前缀的正负下一步，形成$\mathcal D$并完成初始化偏好优化；然后在正确前缀后放入错误步骤$s_k^-$，分别构造纠错续写$c_k^+$和未处理错误的续写$s_{k+1}^-$，形成$\mathcal D_{\mathrm{SC}}$并进行第二阶段优化。SFS-DPO的$c_k^+$只含显式检测信号和正确替代步骤，SFS-DPO-R还调用强教师生成错误理由。推理时不再执行偏好比较或参数更新，训练后的单一策略从$x$开始自回归生成；普通步骤推进解题，检测步骤标记前一步错误，随后修复步骤替换错误推理，最终由修正后的终端轨迹产生$\hat y$。

**复现信息**

与复现和公平解释直接相关的设计包括：两阶段都使用步骤级强化学习式偏好优化，初始化数据规模为$10\mathrm{K}$，自我纠错阶段数据规模为$8.4\mathrm{K}$；第二阶段需要冻结参考模型$\pi_{\mathrm{ref}}$。SFS-DPO不使用外部教师提供错误解释，SFS-DPO-R则需要强教师生成$r_{k-1}$，因此两者比较同时反映纠错信号质量与外部依赖之间的权衡。所给章节未明确报告$\beta$取值、教师模型名称、样本生成与过滤流程、轨迹中步骤的具体切分规则、解码参数以及检测标记的确切文本格式，这些信息仍需结合论文其他章节和代码核查。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 域内评测由 GSM8K 与 MATH 构成，测试集分别含 1,319 和 5,000 道题。二者的训练集还用于构造与 Step-DPO 相同的 10K 样本初始化数据，因此这里的“域内”表示训练监督和测试任务来自相同数据来源，而非测试题参与训练。
- GaoKao2023（GK2023）包含 385 道取自 2023 年中国高考的竞赛级数学问题，作为分布外评测，检验方法能否从 GSM8K/MATH 的训练监督迁移到不同题型与考试分布。
- OCWCourses（OCW）包含 272 道需要多步推理的本科 STEM 问题，作为另一项分布外评测。纠错阶段的数据来自原 Step-DPO 10K 数据：SFS-DPO 构造出 8,416 个无需外部教师的偏好样本；SFS-DPO-R 则在纠错信号与正确步骤之间插入 GPT-4o 生成的错误解释。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**答案准确率（Accuracy）**

四个基准上最终答案正确的题目比例；主表使用贪心解码。该指标评价完整推理的任务结果，但不能单独判断模型是否真的检测并修复了中间错误。 （越高越好，因为表示更多问题得到正确最终答案。）

</div>
<div class="metric-item" markdown="1">

**自我纠错率（Self-correction rate）**

原文在实验设置中将其定义为：在模型决定执行自我纠错的生成解答中，最终正确解答所占比例。不过附录表 6 将其用于描述模型纠错行为的频率，节选没有进一步澄清两处口径是否完全一致，因此相关数字需要回查原文定义与计算代码。 （不能简单判定越高越好；作者的附录分析表明，触发得更多不一定带来更高任务准确率，关键在纠错的选择性与有效性。）

</div>
<div class="metric-item" markdown="1">

**错误召回率（Error Recall）**

错误推理步骤中，被模型通过自我纠错信号标记出来的比例，用于衡量模型发现中间错误的覆盖程度。 （通常越高越好，因为表示漏检的错误步骤更少；但若缺少误报率或精确率，高召回并不能证明错误判断足够准确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 七个骨干模型在两个域内基准上的总体比较

<div class="result-value" markdown="1">

作者报告，SFS-DPO 和 SFS-DPO-R 相对各自基础模型在全部域内设置中均有提升，并分别在 14 个“骨干模型×域内数据集”设置中的 11 个和 12 个超过 Step-DPO；相比之下，Step-DPO 的改进较小且不稳定。

</div>

这说明在相同类型的步骤级监督基础上，明确教模型何时发出纠错信号以及如何改写错误步骤，比只偏好正确步骤更稳定。该结果支持“显式纠错训练有效”的作者主张，但不是严格的单因素因果证明，因为 SFS 方法的第二阶段数据结构和训练过程均与 Step-DPO 不同。

<div class="result-source" markdown="1">

来源：第 4.2 节 In-Domain Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In contrast, SFS-DPO and SFS-DPO-R learn explicit self-correction and achieve larger gains than Step-DPO, outperforming it in 11/14 and 12/14 settings, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen2-7B-Instruct 上的域内结果

<div class="result-value" markdown="1">

Qwen2-7B-Instruct 的基础准确率为 MATH 55.7、GSM8K 85.0；SFS-DPO-R 分别达到 59.1 和 86.0，即绝对提高 3.4 和 1.0 个百分点，平均分由 50.2 提至 53.0。MATH 上 59.1 的结果相对 Step-DPO 具有统计显著性。

</div>

这是节选中最明显的域内增益：教师辅助纠错训练对原先纠错行为较弱的指令模型尤其有效。不过，该行同时包含分布外结果，平均分是四个基准的平均值；而且 GSM8K 上 SFS-DPO-R 的 86.0 低于 SFS-DPO 的 86.6，所以不能据此声称教师解释在每个任务上都更优。

<div class="result-source" markdown="1">

来源：表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen2-7B-Instruct | + SFS-DPO-R | 59.1* (+3.4) | 86.0 (+1.0) | 44.7 (+5.0) | 22.1 (+1.9) | 53.0 (+2.8)

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 数学专用 Qwen2.5-Math-7B-Instruct 上的域内与分布外泛化

<div class="result-value" markdown="1">

SFS-DPO-R 将 MATH、GSM8K、GK2023 和 OCW 的准确率分别从 83.6、95.2、57.4、23.9 提高至 85.0、96.0、67.8、32.7，对应绝对增益 1.4、0.8、10.4 和 8.8 个百分点；四项平均分从 65.0 升至 70.4，即提高 5.4 个百分点。

</div>

分布外两项的增益明显大于域内两项，说明纠错训练可能提升了跨题型迁移，而不只是记住训练分布中的答题模式。它仍不能证明对任意分布外任务都有效：这里只评测了两个规模较小的 OOD 基准，且节选仅对域内结果标注统计显著性。

<div class="result-source" markdown="1">

来源：表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen2.5-Math-7B-Instruct | + SFS-DPO-R | 85.0* (+1.4) | 96.0 (+0.8) | 67.8 (+10.4) | 32.7 (+8.8) | 70.4 (+5.4)

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 分布外结论只来自 GK2023 的 385 题和 OCW 的 272 题，且表 2 的显著性标记仅适用于域内基准；节选也未报告多随机种子均值、方差或置信区间。因此，OOD 大幅增益具有启发性，但其统计稳定性和对更多推理领域的可推广性仍需验证。
- SFS-DPO-R 依赖 GPT-4o 生成错误解释，增加了外部教师成本，也可能引入教师偏差。实验没有提供等 token、等数据量或不同解释质量的受控对照；此外，自我纠错率在实验设置与附录叙述中的口径存在潜在歧义，相关行为结论需要结合完整论文和代码复核。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 未经本研究训练的对应骨干模型，包括 DeepSeekMath-7B-SFT、Qwen2-7B-SFT、Qwen2-7B-Instruct、Qwen2.5-Math-7B-Instruct、Qwen3-8B、Llama-3.1-8B-Instruct 和 Qwen2.5-14B-Instruct。它们给出每种模型原有推理与自发纠错能力的参照点。
- Step-DPO：直接且最关键的训练方法基线。它使用步骤级偏好优化增强推理，但没有像 SFS-DPO 那样显式训练模型识别错误并修正后续步骤，因而能够检验收益是否来自“显式自我纠错”而不只是步骤级偏好学习。
- SFS-DPO：资源无关的两阶段方法版本。它先进行步骤级推理初始化，再使用带错误前缀、纠错信号和正确步骤的偏好数据训练自我纠错；它也是判断教师解释是否必要时的直接对照。
- SFS-DPO-R：教师辅助版本，在 SFS-DPO 的纠错信号后加入 GPT-4o 生成的错误原因解释。与 SFS-DPO 的比较主要检验显式解释能否形成更强的纠错监督，但两者之间的小幅差异不能自动归因于解释质量。

**实验想回答的问题**

- 在七种通用或数学专用骨干模型上，显式训练逐步自我验证与自我纠错的 SFS-DPO、SFS-DPO-R，是否比基础模型和仅优化步骤偏好的 Step-DPO 更稳定地提高域内数学推理准确率，并能否泛化到分布外问题？
- 性能变化究竟来自模型更频繁地触发纠错，还是来自更有选择性、更准确的纠错；加入由教师模型生成的错误解释后，是否能提供更强的纠错信号？

**实验实现**

评测覆盖七个骨干模型，并在 MATH、GSM8K、GK2023 和 OCW 上采用贪心解码与答案准确率。表 2 括号内数字是相对对应基础骨干的绝对准确率变化；域内结果的星号表示相对 Step-DPO 通过单侧 McNemar 检验，显著性阈值为 $p<0.05$。训练分两阶段：初始化阶段沿用 Step-DPO 的 10K 样本数据，训练 3 个 epoch、批量大小为 4；纠错阶段使用 8,416 个 SFS 偏好样本训练 4 个 epoch、批量大小为 8。所有阶段均采用 AdamW，预热比例为 $0.02$，学习率为 $5\times10^{-7}$。这些统一设置支持方法间比较，但节选未报告随机种子、多次运行方差或分布外结果的显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 教师错误解释的作用：SFS-DPO-R 对比 SFS-DPO，以 Qwen3-8B 为例 | Qwen3-8B 使用 SFS-DPO 时四项平均准确率为 64.5、相对基础模型提高 0.6 个百分点；加入教师错误解释的 SFS-DPO-R 达到 65.2、提高 1.3 个百分点，即相对 SFS-DPO 再增加 0.7 个百分点。其自我纠错率也由基础模型的 35.8 降至 SFS-DPO 的 26.9，并在 SFS-DPO-R 下回升至 28.8。 | 两种方法的核心差别是 SFS-DPO-R 在纠错信号与正确步骤之间插入 GPT-4o 生成的错误解释，因此该比较近似隔离“解释性纠错信号”的作用。结果表明解释可改善该模型的总体准确率，但纠错率仍低于基础模型，进一步说明收益来自更有效或更有选择性的修正，而非单纯增加触发次数。由于训练样本内容随解释加入而改变，这不是完全受控的参数级消融。 | 表 6；准确率数字见表 2<br><span class="experiment-evidence">Qwen3-8B \| 35.8 \| 26.9 \| 28.8</span> |
| 训练后纠错频率与效果是否同步：Llama-3.1-8B-Instruct | Llama-3.1-8B-Instruct 的自我纠错率从基础模型的 37.0 降至 SFS-DPO 的 28.8，并进一步降至 SFS-DPO-R 的 23.9；与此同时，表 2 的四项平均准确率由 50.0 提高到 52.0 和 52.3。 | 这项分析隔离的不是某个网络组件，而是检验“更高纠错频率是否解释准确率提升”。两项指标反向变化，否定了这种简单解释，并支持作者关于选择性纠错更重要的判断。不过，节选没有提供纠错触发的逐题配对分析，因而无法确定下降来自减少误纠错、减少无效纠错，还是信号识别规则的变化。 | 表 6；平均准确率数字见表 2<br><span class="experiment-evidence">Llama-3.1-8B-Instruct \| 37.0 \| 28.8 \| 23.9</span> |

**定性案例**

- 附录图 5 给出按 epoch 的行为分析：作者称 DeepSeekMath-7B-SFT 的自我纠错率和任务准确率都在第 2 个 epoch 达到峰值，而 Qwen2-7B-SFT 的纠错率相对稳定、准确率仅小幅波动。前者显示纠错行为与性能可能同步，后者则说明原始纠错频率不足以预测有效性。节选没有提供图中各 epoch 的完整数值，因此不能进一步量化相关程度。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper uses step-level preference optimization to train LLM self-verification and self-correction, centrally contributing to both reasoning and preference-based post-training.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`c9f746e8804ecfae2f7679bcb398addeb9a738279fde6a0c5477e798e72e0ce6`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
