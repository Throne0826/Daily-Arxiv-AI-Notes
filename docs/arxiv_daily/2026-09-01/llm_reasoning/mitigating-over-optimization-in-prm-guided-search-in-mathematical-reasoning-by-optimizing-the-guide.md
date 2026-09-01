---
title: "[论文解读] Mitigating Over-Optimization in PRM-Guided Search in Mathematical Reasoning by Optimizing the Guide"
description: "[arXiv 2608.30051][LLM Reasoning] 本文将不可靠过程奖励模型引导的数学推理搜索重新表述为奖励不确定性下的鲁棒决策问题，以无需训练的 maximin 选择机制降低搜索对虚高过程分数的过度优化。"
arxiv_id: "2608.30051"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:32:41.244473+00:00"
source_sha256: "146c3881eb3796ea32a39f5c8a90892985598327f7d4a6e1a108c7d447c3f678"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "过程奖励模型"
  - "数学推理"
  - "推理时搜索"
  - "步骤级监督"
  - "奖励过度优化"
  - "奖励黑客"
  - "稳健优化"
  - "maximin搜索"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.30051</p>

# Mitigating Over-Optimization in PRM-Guided Search in Mathematical Reasoning by Optimizing the Guide

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Taejong Joo, Diego Klabjan</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Department of Industrial Engineering & Management Sciences；Affiliation: Northwestern University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30051v1) · [PDF 下载](https://arxiv.org/pdf/2608.30051v1) · **关键词** 过程奖励模型, 数学推理, 推理时搜索, 步骤级监督, 奖励过度优化, 奖励黑客, 稳健优化, maximin搜索<br>
**代码**: [https://github.com/tjoo512/maximin-search](https://github.com/tjoo512/maximin-search)

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

本文将不可靠过程奖励模型引导的数学推理搜索重新表述为奖励不确定性下的鲁棒决策问题，以无需训练的 maximin 选择机制降低搜索对虚高过程分数的过度优化。

**不用术语来说**：在数学推理搜索中，系统会生成多条尚未完成的解题路线，并用评分器决定哪些路线值得继续。但评分器可能把错误路线打成高分，或把正确路线打成低分；搜索越深、候选越多，就越容易偶然遇到一个分数极高但实际错误的候选。一旦系统盲目追逐最高分，正确路线可能被永久删除，有限的推理预算反而被浪费在错误方向上。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者从理论上刻画了 PRM 过度优化的具体机制：对含噪步骤分数反复取最大值会产生极值效应，使不可行前缀随推理深度增加而更可能凭偶然虚高分数被选中；分析还指出该风险与验证器不确定性、前缀可分性、生成器覆盖率、搜索宽度和推理深度有关。
- 作者把 PRM 引导搜索建模为可信奖励扰动集合上的鲁棒优化，并据此提出无需微调或在线适配的 maximin 搜索插件：选择在可能评分扰动下仍有竞争力、同时具有一定多样性的前缀，以减少对异常高分的敏感性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型的搜索式数学推理。在这类系统中，大语言模型先生成多条由中间步骤组成的候选推理轨迹，搜索算法再把有限的推理时计算分配给较有希望的分支。过程奖励模型（PRM）为每个中间步骤或部分轨迹打分，比只评价最终答案的结果奖励模型提供更密集的控制信号，因而可以及早剪除低分分支。然而，PRM只是潜在推理质量的学习代理，其评分会受到监督不足、模型设定偏差和分布偏移影响；搜索又会反复选择评分最高的候选，使偶然高分的错误前缀被扩展、实际可行但被低估的前缀被永久剪除。本文所处的核心问题因此不是单纯提高生成量，而是在固定生成器和固定PRM的条件下，如何对不确定的步骤评分作出稳健的保留与剪枝决策。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**过程奖励模型（Process Reward Model, PRM）**

PRM对尚未完成的推理前缀或其中的步骤进行评价，用分数估计该前缀继续得到正确解答的潜力。它能在最终答案出现前指导搜索，但分数并不等同于真实推理质量。

</div>
<div class="concept-item" markdown="1">

**搜索式推理与剪枝**

模型在每一轮生成多个候选推理前缀，搜索算法只保留其中一部分继续扩展，这一淘汰过程称为剪枝。剪枝节省计算，但一旦误删可行分支，后续搜索通常无法恢复该分支。

</div>
<div class="concept-item" markdown="1">

**奖励过度优化（reward over-optimization）**

当算法持续最大化一个存在误差的代理奖励时，选出的候选可能只是利用了评分器的误差，而不是真实质量更高。本文关注其步骤级形式：噪声评分会同时影响候选选择和后续计算资源的分配。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一道数学问题、一个固定的大语言模型生成器、一个固定的PRM以及有限的推理时搜索预算。搜索在多个深度上迭代进行：生成器从当前前缀产生候选后续步骤，PRM对候选前缀给出步骤级分数，选择器保留至多$m$个前缀并继续扩展，最终输出完整推理轨迹及答案。基本假设是PRM分数带有不确定性，因而高分不必然代表前缀可继续得到正确答案；随着推理深度和候选数量增加，在大量错误前缀中出现异常高分的机会也会上升。论文据此把搜索决策理解为奖励扰动下的稳健优化：不把观测到的PRM分数视为精确真值，而是在一组合理的评分变化下保留仍具竞争力的候选，并利用RBF核$K$表达候选之间的相似性，以避免搜索预算集中于一组相似且可能由评分噪声抬高的轨迹。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$m$**

每次剪枝后保留并继续扩展的推理前缀数量，即搜索宽度。

</div>
<div class="notation-item" markdown="1">

**$K$**

用于衡量候选推理前缀之间相似性的径向基函数（RBF）核；文中稳健选择器据此兼顾PRM高分与候选多样性。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{PRM}$**

过程奖励模型，对中间推理步骤或部分轨迹提供步骤级评价。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{BoN}$**

Best-of-N结果级解码：生成多个完整答案，再依据结果评分选择其中一个；它不在中间步骤上分配搜索资源。

</div>

</div>

**直接相关的工作**

- **Tree of Thoughts（Yao et al., 2023）**: 该方法通过显式搜索部分推理状态并从低潜力分支回退，说明推理时计算可以通过结构化搜索提升效果。本文继承“对中间状态进行搜索和剪枝”的设置，但进一步研究指导剪枝的PRM存在噪声时，搜索为何会过度优化错误评分。
- **ReST-MCTS*、V-STaR与PRIME**: 这些自改进方法通过迭代更新策略、价值模型、验证器或奖励来缓解搜索与评价之间的不匹配，但通常需要额外训练、较高计算开销，部分方法还依赖结果监督或标准答案。本文采取不同路线：保持生成器与PRM固定，在推理阶段直接改造选择规则，以稳健决策而非在线修复评分器来处理奖励不确定性。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

推理时搜索能否有效利用额外计算，取决于系统是否能在早期正确保留有希望的部分解。PRM 虽提供逐步评分，但它只是潜在推理质量的学习代理，会因监督不足、模型设定偏差或分布漂移而出错。搜索又会主动把候选分布推向评分器偏好的区域，因此一次假阴性可能永久剪掉正确分支，一次假阳性则可能让大量预算持续扩展伪解，导致增加推理计算并不必然提高真实解题能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **直接最大化 PRM 分数的引导搜索**：语言模型在每轮生成若干推理前缀，PRM 对中间步骤评分，搜索算法优先保留最高分候选并剪除其余分支。该方式利用密集的步骤级信号进行早期筛选，比只在完整答案处评分更容易控制多步搜索。
- **测试时训练或在线适配评分器**：系统在推理阶段继续更新或修正奖励模型，希望评分器适应当前题目与搜索产生的新分布，再用更新后的分数指导候选扩展和剪枝。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 直接按 PRM 分数取最大值默认预测值足够可信，但搜索会系统性放大评分噪声：候选数量和推理深度增加时，不可行前缀更可能因极值效应获得偶然高分。后果是伪轨迹被持续扩展，而仍可导向正确答案的轨迹被过早删除。
- 测试时训练或在线适配把重点放在修复评分器，不仅将额外优化引入推理关键路径、增加计算与实现负担，其稳定性还依赖低信号且分布外的数据环境；这并未直接解决评分器无法被完全校准时，搜索算法应如何稳健行动的问题。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有方法缺少一种面向决策层的机制：在不假定 PRM 分数精确、也不额外训练验证器的条件下，显式考虑合理的奖励扰动，并据此决定应保留哪些部分推理轨迹。尤其需要解释含噪评分为何会随搜索深入而恶化，并把这一失败机制转化为可直接接入现有解码流程的鲁棒选择规则。

</div>
<div markdown="1"><span>核心问题</span>

当步骤级验证器存在不可避免的评分噪声时，能否把 PRM 引导搜索构造成奖励不确定性下的鲁棒优化，使算法无需微调或在线适配，仍能避免追逐偶然的高分异常值，并保留真正有希望的推理前缀？

</div>
<div markdown="1"><span>作者直觉</span>

单纯保留当前最高分候选，相当于把评分器的一次预测当成确定事实；maximin 思路则询问：如果分数在合理范围内发生不利扰动，哪些候选仍值得保留？再结合由 RBF 核 $K$ 表示的候选相似性，选择 $m$ 个兼顾较高评分与多样性的前缀，可以避免搜索预算集中到一组彼此相似、仅因同类评分误差而虚高的路线。通俗地说，它不把所有筹码押在评分器眼下最喜欢的一条路上，而是保留若干在评分偏差存在时仍可能成功的备选路线。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法是一种无需训练的稳健推理时搜索策略，目标是在固定过程奖励模型（process reward model，PRM）可能含噪的情况下，减少对异常高分前缀的过度优化。给定问题 $x$、基础推理模型策略 $\pi$ 和固定的 PRM $\widehat{V}$，方法先生成多个候选推理前缀，再不直接依据单一 PRM 分数选取候选，而是通过带有核函数惩罚的 maximin 稳健目标选择一组较可靠且不过度集中的轨迹，持续扩展直到得到答案。直观地说，普通搜索会把所有计算押在“当前分数最高”的路径上；Maximin 则会考虑奖励估计可能出错，并保留具有互补性的候选路径，从而降低错误高分导致的过早剪枝。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 初始化问题与推理状态

将部分推理表示为轨迹 $\tau^{(t)}=(x,s_1,\ldots,s_t)$，其中每个 $s_i$ 是一个语义连贯的推理片段；在深度 $t$ 维护活动候选集合（beam）$\mathcal{B}_t$，初始状态为问题本身 $\tau^{(0)}=x$。

<div class="method-step__io" markdown="1">

**输入**：输入数学问题 $x$、基础生成模型的思想级策略 $\pi(s\mid\tau^{(t)})$、最大推理深度 $T_{\max}$、候选总预算 $N$ 以及搜索宽度 $w_t$。<br>
**输出**：当前深度的活动轨迹集合 $\mathcal{B}_t$ 及其搜索状态。

</div>

**直观理解**：可以把每条轨迹看作一条正在书写的解题草稿。$\mathcal{B}_t$ 是当前保留下来的若干份草稿，而不是只保留一份答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 扩展活动轨迹并形成候选集

对每条活动轨迹，从 $\pi(\cdot\mid\tau_i^{(t)})$ 采样或枚举后续思想，并通过前缀扩展 $\tau_i^{(t)}\oplus s$ 形成候选集合 $\mathcal{C}_{t+1}$；其规模不超过 $N$，每条活动轨迹的分支数为 $b_t=\lfloor N/w_t\rfloor$。

<div class="method-step__io" markdown="1">

**输入**：活动轨迹集合 $\mathcal{B}_t=\{\tau_i^{(t)}\}_{i=1}^{w_t}$ 以及生成策略 $\pi$。<br>
**输出**：下一深度的候选前缀集合 $\mathcal{C}_{t+1}$。

</div>

**直观理解**：这一步相当于让每份草稿各自尝试若干种下一步写法。这样搜索预算被分配到多条可能的解题路线，而不是只沿着模型最常见的下一步继续。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 计算过程奖励与表示几何

PRM 为每个中间轨迹输出标量分数 $\widehat{V}(\tau)$，该分数被解释为从当前前缀继续推理后获得高效用的估计；Maximin 使用经过 $\ell_2$ 归一化的 PRM 表示计算基于角度距离的 RBF 核，以刻画候选轨迹之间的相似性或集中程度。

<div class="method-step__io" markdown="1">

**输入**：候选前缀 $\tau\in\mathcal{C}_{t+1}$、固定 PRM $\widehat{V}$ 及其内部表示。<br>
**输出**：每个候选前缀的过程奖励估计，以及候选之间的核相似性结构。

</div>

**直观理解**：PRM 不仅告诉系统“哪份草稿看起来好”，还提供表示信息来判断几份草稿是否其实非常相似。若所有候选都挤在同一种路线中，系统会更警惕这种集中。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 以稳健目标选择下一轮轨迹

先进行随机贪心选择，再通过 $1$-swap 局部改进进一步优化 maximin 稳健目标；该目标在可能的奖励扰动下权衡候选的预测效用与候选集合的集中风险，而不是简单选择 PRM 分数最高的前缀。外层辅助变量 $\eta$ 通过由 $\xi$ 控制分辨率的乘法网格 $G_\xi$ 搜索。

<div class="method-step__io" markdown="1">

**输入**：候选集合 $\mathcal{C}_{t+1}$、PRM 分数、核矩阵、样本相关的不确定性半径 $\widetilde{B}$ 以及网格参数 $\xi$。<br>
**输出**：下一活动集合 $\mathcal{B}_{t+1}\subseteq\mathcal{C}_{t+1}$，且 $|\mathcal{B}_{t+1}|=w_{t+1}$。

</div>

**直观理解**：普通 beam search 像按分数排序后直接取前几名；这里则像在问：“即使分数有一定误差，这组选出的草稿是否仍然可靠？”$1$-swap 就是尝试用一份未入选草稿替换已入选草稿，看整体稳健性是否提高。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 自适应 RKHS 不确定性半径

$$
\widetilde{B}=\sqrt{\nu^{\top}K^{\dagger}\nu}
$$

**符号说明**

- $\widetilde{B}$：样本相关的 RKHS 半径代理，用于刻画奖励函数可能存在的不确定性尺度。
- $\nu$：由轨迹内过程奖励的最大变化构成的向量，用于反映局部奖励变化。
- $K$：由候选轨迹的 PRM 表示和 RBF 核构成的核矩阵。
- $K^{\dagger}$：核矩阵 $K$ 的 Moore–Penrose 伪逆。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把当前候选轨迹的奖励变化与表示空间几何结合起来，估计本次搜索应当容忍多大的奖励不确定性。它使算法在局部奖励变化大或几何结构不同的样本上采用不同程度的保守性，而不是依赖一个全局固定超参数。<br>
**原文位置**：第 6.3 节“自适应不确定性尺度”

</div>

</div>

<div class="equation-block" markdown="1">

#### 基础模型的轨迹概率分解

$$
\pi(\tau^{(T)})=\prod_{t=1}^{T}\pi(s_t\mid\tau^{(t-1)})
$$

**符号说明**

- $\pi(\tau^{(T)})$：基础推理策略生成完整轨迹 $\tau^{(T)}$ 的概率。
- $s_t$：第 $t$ 个推理思想或推理片段。
- $\tau^{(t-1)}$：生成第 $t$ 个思想之前的部分轨迹。
- $T$：该完整轨迹的终止长度。

<div class="equation-explanation" markdown="1">

**直观理解**：完整解题过程的概率等于每一步在已有历史条件下生成下一段思想的概率之积。该分解说明候选轨迹由生成模型提出，而 Maximin 主要改变的是候选保留和计算分配方式。<br>
**原文位置**：第 3 节“Reasoning Models”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文方法不引入新的参数训练目标，也不对基础生成模型或 PRM 进行微调。其核心是推理时的稳健优化：在固定的 $\widehat{V}$ 分数和候选轨迹表示上，选择对可能奖励扰动更不敏感的候选集合；因此，$1$-swap 局部改进优化的是搜索选择目标，而不是更新神经网络参数。原文所给出的选段未包含该 maximin 目标的完整公式及其编号，因此不能据此补写具体目标函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 固定 PRM 引导模块**

PRM $\widehat{V}$ 为部分轨迹 $\tau^{(t)}$ 输出标量过程奖励，基础模型策略 $\pi$ 负责提出后续思想，二者分工明确：$\pi$ 决定候选从哪里来，$\widehat{V}$ 决定有限计算预算分配给哪些候选。该框架可退化为多种搜索：当 $b_t=1$ 时对应 outcome-level 的 Best-of-$N$ 选择，当 $w_t=1$ 时对应 step-level greedy decoding。

> 直观理解：生成模型负责“提出解法”，PRM 负责“检查中间过程是否有希望”。论文不在搜索过程中重新训练或在线修正 PRM，而是研究如何更安全地使用这个可能不完美的检查器。

**2. Maximin 稳健选择模块**

该模块把 PRM 引导搜索表述为对可能奖励扰动的稳健优化，并加入二次核惩罚以降低候选选择对 PRM 异常高分的敏感性。候选选择由随机贪心初始化，并用 $1$-swap 局部搜索继续优化稳健目标；因此，额外优化针对的是稳健目标，而非未经修正的 PRM 分数。

> 直观理解：论文的核心改变不是换一个更强的生成器，而是改变“怎样利用评分”。它允许保留若干不完全相同的路线，避免一条被误打高分的错误路线挤掉所有可行路线。

**3. 自适应不确定性与表示核模块**

方法使用样本相关的 RKHS 半径代理 $\widetilde{B}=\sqrt{\nu^{\top}K^{\dagger}\nu}$，其中 $\nu$ 描述轨迹内过程奖励的最大变化，$K^{\dagger}$ 是核矩阵 $K$ 的伪逆。RBF 核在 PRM 表示经 $\ell_2$ 归一化后计算，使距离主要反映角度而不是原始特征范数；网格参数 $\xi$ 控制辅助变量 $\eta$ 的乘法网格分辨率。

> 直观理解：不确定性尺度不是对所有题目和深度使用同一个固定旋钮，而是根据当前样本的奖励变化和表示几何自动调整。归一化则避免模型表示的向量长度差异被误当成语义差异。

**训练与推理**

训练阶段不适用：实验直接使用现成的基础生成器和现成 PRM，不进行 fine-tuning、在线适应或搜索中的奖励模型更新。推理阶段从问题 $x$ 开始，依据 $\pi$ 生成候选思想，用 $\widehat{V}$ 和表示核计算候选质量及相似性，再通过 maximin 稳健选择保留下一轮轨迹；该过程重复至 $\mathrm{EOS}$ 或 $T_{\max}$，最后由 $\mathrm{ans}$ 提取答案。与普通 step-level beam search 相比，额外计算主要来自核相关的稳健选择和网格搜索，而不是额外生成模型训练。

**复现信息**

复现所必需的关键设置包括：候选总预算使用 $N=16$ 或 $N=64$；不确定性半径默认采用样本相关估计 $\widetilde{B}$；候选表示先作 $\ell_2$ 归一化，再使用 RBF 核；稳健选择包含随机贪心初始化和 $1$-swap 局部改进；辅助变量使用由 $\xi$ 控制的乘法网格，默认 $\xi=0.05$。选段报告 $\xi=0.05$ 时相对 SBS 的运行时间开销为 $0.26\%$，但未给出完整算法伪代码、RBF 核带宽、PRM 表示提取层、候选采样温度的默认值，或 maximin 目标的完整计算式；这些内容原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：小学数学应用题基准，用于检验方法在相对基础、通常需要多步算术推理的任务上的表现。实验报告准确率；所给章节未明确说明使用的样本规模与数据划分。
- MATH-500：从 MATH 数学问题体系构成的评测集，用于测试比 GSM8K 更复杂的数学推理。实验报告准确率；所给章节未进一步说明具体划分或采样流程。
- AIME’24 与 AIME’25：竞赛级数学问题基准，用于测试高难度推理。原文称每个 AIME 数据集仅含 30 个样本，因此采用三个不同随机种子运行并报告平均准确率，以降低小样本评测的随机波动。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率**

最终答案正确的问题占全部评测问题的比例，直接衡量数学题求解成功率。AIME’24 和 AIME’25 的准确率取三个随机种子结果的平均值。 （越高越好，因为更高数值表示在相同数据集上正确解决了更多问题。）

</div>
<div class="metric-item" markdown="1">

**相对平均改进幅度**

作者用百分比概括 maximin 搜索相对于普通 PRM 引导搜索的平均性能提升；所给材料未给出该百分比的逐项计算公式或完整表格数值。 （越高越好，因为它表示鲁棒搜索相对直接使用 PRM 分数取得更大的准确率收益，但不能脱离基线绝对准确率单独判断实际效果。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨数学基准、生成器与推理预算的总体比较

<div class="result-value" markdown="1">

作者声称，在不进行微调或在线适应的条件下，maximin 搜索相对于普通 PRM 引导搜索取得了平均 17%–35% 的一致改进。

</div>

这一结果支持本文的核心判断：直接追逐最高 PRM 分数可能放大评分噪声，而针对奖励扰动进行保守选择能够改善最终正确率。17%–35% 是作者给出的总体相对改进范围；由于所给节选缺少表 1 的具体数值，无法核验各数据集上的绝对准确率、改进计算方式以及哪些设置对应区间两端。

<div class="result-source" markdown="1">

来源：摘要；具体分设置结果据称位于表 1，但所给节选未包含表格数据行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Without fine-tuning or online adaptation, maximin search consistently improves the PRM-guided search by 17-35\% on average, outperforming outcome- and step-level baselines in 14 out of 16 settings.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 与结果级和步骤级监督基线的跨设置胜负比较

<div class="result-value" markdown="1">

作者报告，maximin 搜索在 16 个生成器—数据集—预算设置中的 14 个设置里优于结果级与步骤级基线。

</div>

14/16 的覆盖率说明优势并非仅由某一个数据集或预算上的极端增益造成，并且比较对象包含 BoN、MBR-BoN 与 SBS 等不同监督粒度的方法。不过，这一统计不表示 14 个设置中每个差距都具有统计显著性；节选也没有提供剩余两个设置的具体失败幅度。

<div class="result-source" markdown="1">

来源：摘要；具体分设置结果据称位于表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Without fine-tuning or online adaptation, maximin search consistently improves the PRM-guided search by 17-35\% on average, outperforming outcome- and step-level baselines in 14 out of 16 settings.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 训练自由条件下的通用性检验

<div class="result-value" markdown="1">

作者声称上述改进是在不微调、不在线适应且不进行任务专用训练的条件下获得，并覆盖两个不同生成器家族及 $N=16$、$N=64$ 两种推理预算。

</div>

该设置表明收益被归因于搜索时如何利用 PRM，而不是额外训练生成器或奖励模型，因此部署成本相对较低。跨两个生成器也降低了方法只适配某一模型家族的可能性；但仅测试两个小型生成器和一个 PRM，不能证明其对更大模型、其他奖励模型或域外任务普遍有效。

<div class="result-source" markdown="1">

来源：第 6 节 Experiments，Base models and configuration

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

All models are used without fine-tuning, online adaptation, or task-specific training.

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

- Beam search：不使用外部奖励模型，按生成模型自身的序列概率保留并扩展前 $N$ 条部分轨迹。它检验性能提升是否只是来自维护多条候选路径，而不是来自鲁棒的 PRM 引导。
- Best-of-$N$（BoN）：独立采样 $N$ 条完整轨迹，再选取估计结果分数最高者。它代表只在完整答案层面使用监督的常见推理时扩展方法，用于比较“生成后筛选”与“生成过程中逐步引导”。
- MBR-BoN：在 BoN 的价值估计上加入候选答案间的语义相似度项，在高奖励与候选共识之间折中。它是更强的结果级监督基线，可检验 maximin 搜索的收益是否超过简单的多样本共识选择。
- SBS：标准 PRM 引导的步骤级 beam search，每轮按 PRM 分数保留前 $m$ 条部分轨迹。它与本文方法使用相同类型的步骤奖励，因而是最直接的比较对象：两者差异主要反映是否对 PRM 噪声和异常高分进行鲁棒处理。

**实验想回答的问题**

- 在相同推理预算下，maximin PRM 引导搜索能否比无外部监督、结果级监督和标准步骤级 PRM 搜索更准确地解决不同难度的数学推理题？
- 这种改进能否跨生成器家族、数据集难度与推理预算保持一致，从而说明方法并非只适用于某个特定基础模型或单一搜索规模？

**实验实现**

实验使用 Qwen2.5-Math-1.5B 与 Phi-3.5-mini-instruct 作为现成生成器，并统一使用 Skywork o1-PRM-1.5B 提供步骤奖励；所有模型均不进行微调、在线适应或任务专用训练。对轨迹 $\tau$，作者将各推理步骤的 PRM 奖励取平均，作为轨迹价值估计 $\hat{V}(\tau)$。生成器采用零样本思维链提示。主要比较预算为 $N\in\{16,64\}$：beam search 的宽度和 Best-of-$N$ 的样本量均按 $N$ 设置；PRM 引导搜索固定分支因子为 4，并令搜索宽度 $m=\lfloor N/4\rfloor$，使其最多维护或扩展的并行轨迹预算与其他方法尽量匹配。贪心解码使用 $N=1$，但由于预算不同，主要用于提供单路径参考，而不是完全同预算的公平对照。MBR-BoN 按 $\hat{V}(\tau)+0.1\cdot\frac{1}{N}\sum_{i=1}^{N}U(\tau,\tau_i)$ 选择轨迹，其中 $U$ 是两条轨迹嵌入的余弦相似度。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文针对数学推理中的 PRM 引导搜索提出鲁棒的推理期搜索方法，以缓解过程奖励过优化。; rule check: matched taxonomy keywords; top rule score=6.0
- 全文指纹：`146c3881eb3796ea32a39f5c8a90892985598327f7d4a6e1a108c7d447c3f678`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
