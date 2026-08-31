---
title: "[论文解读] VISTA: Verifier-Informed Student-to-Teacher Adaptation for On-Policy Self-Distillation"
description: "[arXiv 2608.28306][对齐 / RLHF] 原文未明确报告。"
arxiv_id: "2608.28306"
announcement_date: "2026-08-31"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:42:17.838559+00:00"
source_sha256: "e9e86bc99793fec3d67a3a09aa680867a301032967d98fd761095ebdd3f07a73"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "on-policy self-distillation"
  - "privileged information distillation"
  - "student-to-teacher adaptation"
  - "outcome verification"
  - "KL-guided selective supervision"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.28306</p>

# VISTA: Verifier-Informed Student-to-Teacher Adaptation for On-Policy Self-Distillation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Zewen Ding, Zezhong Wu, Zhou Tao, Shida Wang, Shizhuo Hou, YongXiang Hua, Haoyu Cao, Linli Xu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> State Key Laboratory of Cognitive Intelligence</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28306v1) · [PDF 下载](https://arxiv.org/pdf/2608.28306v1) · **关键词** on-policy self-distillation, privileged information distillation, student-to-teacher adaptation, outcome verification, KL-guided selective supervision<br>


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

本文位于推理模型后训练与知识蒸馏交叉领域，核心 setting 是带特权信息的 on-policy self-distillation（OPSD）。训练时，problem-only student 仅依据推理阶段可获得的问题生成自己的 rollout；privileged teacher 额外读取 reference solution，并在该 rollout 的每个 token 位置提供稠密的概率分布监督。这样既使训练数据分布贴近学生实际推理行为，又比只使用最终答案提供更细粒度的学习信号。本文关注的特殊点是：teacher 的特权信息并不保证其在每个位置都比 student 更适合作为 problem-only 推理的目标，因此需要研究如何利用已验证的学生行为修正 teacher。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**知识蒸馏与特权信息蒸馏**

知识蒸馏让 student 学习 teacher 的输出概率分布，而不仅是最终标签。特权信息蒸馏允许 teacher 使用训练阶段可见、推理阶段不可见的额外信息，例如 reference solution，再把这种信息转化为对 student 的监督。

</div>
<div class="concept-item" markdown="1">

**On-policy self-distillation（OPSD）**

on-policy 指训练样本由当前 student 自己生成，而不是完全来自固定数据集；self-distillation 指 student 学习与自身任务相关的 teacher 分布。在本文中，student 只看问题生成 rollout，teacher 看问题和参考解，并沿 student 的实际生成轨迹提供逐 token 监督。

</div>
<div class="concept-item" markdown="1">

**结果验证器与 token-level 分布**

结果验证器检查一条完整 rollout 的最终答案是否正确，提供便宜的序列级信号，但不必标注每一步推理。token-level 分布是模型在每个位置对下一 token 的概率分布，本文用 teacher 与 student 分布的 KL divergence 衡量两者在该位置的分歧。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定数学竞赛问题 $x$ 与训练阶段可用的参考解 $r$，problem-only student 根据 $x$ 采样一条 rollout $y=(y_1,y_T)$；在第 $t$ 个位置，student 产生条件分布 $p_S(\text{token}\text{|}x,y_{<t})$，privileged teacher 则利用 $x$ 和 $r$ 产生分布 $p_T(\text{token}\text{|}x,r,y_{<t})$。标准 OPSD 在所有 rollout 位置把 teacher 分布作为 student 的稠密目标，只更新 student；VISTA 保留这一 student 更新，同时要求结果验证器判定 rollout 是否正确，只有通过验证的 rollout 才用于 teacher 向 student 分布靠拢，并且只在 teacher 与 student 分歧最大的 top-$k$ 个位置进行该适应。目标是在不让推理阶段访问 $r$ 的前提下，提高 student 的有效推理能力，并避免 teacher 的特权条件诱导出不适合 problem-only 推理的目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入的数学竞赛问题。

</div>
<div class="notation-item" markdown="1">

**$r$**

训练阶段 teacher 可访问的 reference solution；student 在推理时不可访问。

</div>
<div class="notation-item" markdown="1">

**$y=(y_1,\ldots,y_T)$**

student 从问题 $x$ 出发生成的 rollout，$y_t$ 是第 $t$ 个 token，$T$ 是 rollout 长度。

</div>
<div class="notation-item" markdown="1">

**$p_S(\cdot\mid x,y_{<t})\text{ 与 }p_T(\cdot\mid x,r,y_{<t})$**

第 $t$ 个位置的 student 与 privileged teacher 下一 token 概率分布；其中 $y_{<t}$ 表示此前已经生成的 token。

</div>

</div>

**直接相关的工作**

- **On-policy self-distillation（OPSD；Zhao et al. 2026）**: OPSD 是本文直接继承的训练框架：student 在自己的 rollout 上学习 privileged teacher 的逐 token 分布。其关键限制是固定 teacher 目标并只沿 teacher-to-student 方向更新，因此默认 teacher 在每个位置都优于 problem-only student；VISTA 保留标准 student 更新，但增加由结果验证器门控、由 top-$k$ KL 位置选择的 student-to-teacher 适应。
- **RLSD、TRACE 与 DemoPSD**: 这些方法从 student 侧缓解 teacher 目标失配：RLSD 依据验证器奖励调整更新方向，TRACE 只在选定推理片段上蒸馏，DemoPSD 在 teacher 与 student 分歧处提高 student 侧的权重。它们仍把 privileged teacher 视为固定目标；VISTA 的研究缺口在于利用已验证的 student rollout 反向修正 teacher，同时以稀疏位置选择避免无条件采用 student 分布。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

VISTA（Verifier-Informed Student-to-Teacher Adaptation）是在在线自蒸馏（OPSD）框架上加入选择性教师适应的训练方法。给定问题及参考解答，问题专用学生策略 $\pi_S(\cdot\mid x)$ 只接收问题 $x$，特权教师策略 $\pi_T(\cdot\mid x,y^{\star})$ 同时接收问题和参考解答 $y^{\star}$。训练时先由当前学生生成轨迹，再让学生沿自身轨迹匹配教师分布；如果轨迹通过确定性结果验证器，则只在教师与学生分歧最大的至多 $k$ 个位置上，用学生分布反向更新教师。这样既保留了 OPSD 的密集学生监督，又避免把未经验证的学生错误和所有位置的分歧直接传给教师。

直观地说，教师原本像一名只给学生批改意见、自己却不修改答案的导师；VISTA 允许导师从“最终确实做对”的学生解题过程学习，但只采纳最值得检查的若干步骤。训练结束后，部署时只使用问题专用学生，不需要参考解答、验证器或教师。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造问题—参考解答训练样本

学生仅以 $x$ 为条件，教师以 $(x,y^{\star})$ 为条件。对每个训练问题，从当前学生采样一条在线轨迹 $y\sim\pi_S(\cdot\mid x)$，并在该轨迹的每个前缀 $y_{<t}$ 上计算 $P_t^S=\pi_S(\cdot\mid x,y_{<t})$ 与 $P_t^T=\pi_T(\cdot\mid x,y^{\star},y_{<t})$。

<div class="method-step__io" markdown="1">

**输入**：训练集 $\mathcal{S}=\{(x_i,y_i^{\star})\}_{i=1}^{N}$，其中 $x_i$ 是问题，$y_i^{\star}$ 是参考解答；学生策略 $\pi_S$ 和教师策略 $\pi_T$。<br>
**输出**：一条由学生生成的轨迹，以及每个位置成对的学生、教师下一词分布。

</div>

**直观理解**：学生先独立解题，教师再观察学生已经写出的部分，并针对同一个下一步给出分布式建议，而不是只比较最终答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 保留 OPSD 的学生更新

计算每个位置的点式截断全词表前向 KL 损失，并在教师分布一侧使用停止梯度 $\operatorname{sg}[P_t^T]$，从而只更新学生。损失对轨迹长度 $|y|$ 的所有位置取平均，保持标准 OPSD 的在线、逐词监督方式。

<div class="method-step__io" markdown="1">

**输入**：学生轨迹 $y$、各位置的教师分布 $P_t^T$ 和学生分布 $P_t^S$。<br>
**输出**：学生损失 $\mathcal{L}_S$ 及其对应的学生参数更新方向。

</div>

**直观理解**：教师仍然是学生的主要逐步参照物；停止梯度意味着这一步只要求学生靠近教师，不会顺便改变教师。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 对学生轨迹进行结果验证

使用确定性验证器检查最终结果：数学任务采用规则化答案检查，代码任务采用沙箱测试执行。定义结果门控 $\gamma^{\mathrm{out}}(x,y)$：验证通过为 $1$，否则为 $0$。

<div class="method-step__io" markdown="1">

**输入**：已完成的学生轨迹 $y$ 及其问题 $x$。<br>
**输出**：轨迹级资格标记 $\gamma^{\mathrm{out}}$，决定该轨迹是否可以提供教师监督。

</div>

**直观理解**：验证器通常只能说明整条解答最后对不对，不能指出错误发生在哪一步；因此 VISTA 只把最终确定正确的轨迹交给教师学习，避免把潜在错误扩散给教师。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 选择最有信息量的轨迹位置

在每个位置计算未截断的教师到学生 KL 分数 $d_t=D_{\mathcal{V}}(P_t^T\|P_t^S)$，再选出分数最高的至多 $k$ 个位置组成集合 $\mathcal{I}_k$。位置门控为 $\gamma_t^{\mathrm{pos}}=\mathbb{I}[t\in\mathcal{I}_k]$，并与结果门控相乘得到 $\gamma_t=\gamma^{\mathrm{out}}\gamma_t^{\mathrm{pos}}$。

<div class="method-step__io" markdown="1">

**输入**：通过结果验证的学生轨迹，以及每个位置的 $P_t^T$ 和 $P_t^S$。<br>
**输出**：逐位置教师更新掩码 $\gamma_t\in\{0,1\}$。

</div>

**直观理解**：不是让教师重写整条解题过程，而是优先检查教师和学生意见差距最大的步骤；这些步骤最可能暴露教师对问题专用推理的不匹配。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### VISTA 总训练目标

$$
\mathcal{L}_{\mathrm{total}}=\mathbb{E}_{\substack{(x,y^{\star})\sim\mathcal{S}\\ y\sim\pi_S(\cdot\mid x)}\left[\mathcal{L}_S(x,y,y^{\star})+\lambda\mathcal{L}_T(x,y,y^{\star})\right]
$$

**符号说明**

- $\mathcal{L}_{\mathrm{total}}$：VISTA 需要最小化的期望总损失。
- $\mathcal{L}_S$：学生损失，沿学生在线轨迹使学生分布匹配教师分布。
- $\mathcal{L}_T$：教师适应损失，只在门控选中的位置使教师分布匹配学生分布。
- $\lambda$：正的教师适应权重，控制教师损失相对于学生损失的影响。
- $\mathcal{S}$：由问题和参考解答组成的训练集。
- $x$：输入问题。
- $y^{\star}$：参考解答，教师可见而学生在部署时不可见。
- $y$：从当前学生策略采样得到的在线推理轨迹。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标把两个方向的学习放在同一轮训练中：第一项保持 OPSD 的教师到学生监督，第二项让教师在可靠且被选中的位置吸收学生信息。期望表示训练要对训练样本和学生实际生成的轨迹求平均，而不是只在参考解答上训练。<br>
**原文位置**：第 3.3 节，式（5）

</div>

</div>

<div class="equation-block" markdown="1">

#### 教师更新位置掩码

$$
\gamma_t(x,y,y^{\star})=\gamma^{\mathrm{out}}(x,y)\,\gamma^{\mathrm{pos}}_t(x,y,y^{\star}),\qquad \gamma^{\mathrm{pos}}_t(x,y,y^{\star})=\mathbb{I}\!\left[t\in\mathcal{I}_k(x,y,y^{\star})\right],\qquad \mathcal{I}_k(x,y,y^{\star})=\operatorname{TopK}^{\min(k,|y|)}_{j\in\{1,\ldots,|y|\}}d_j(x,y,y^{\star}),\quad d_t(x,y,y^{\star})=D_{\mathcal{V}}(P_t^T\|P_t^S)
$$

**符号说明**

- $\gamma_t$：位置 $t$ 是否执行教师更新的二值掩码。
- $\gamma^{\mathrm{out}}$：轨迹级结果门控；验证通过为 $1$，否则为 $0$。
- $\gamma^{\mathrm{pos}}_t$：位置级门控；位置属于 Top-$k$ 分歧集合时为 $1$。
- $\mathcal{I}_k$：按分歧分数从高到低选出的至多 $k$ 个轨迹位置。
- $d_t$：位置 $t$ 的教师到学生全词表 KL 分歧分数。
- $k$：每条轨迹最多用于教师适应的位置数。
- $|y|$：学生轨迹的长度。

<div class="equation-explanation" markdown="1">

**直观理解**：教师只有在整条轨迹结果正确，并且当前位置属于分歧最大的至多 $k$ 个位置时才更新。这个公式把“学生是否可靠”和“哪一步最值得学习”分开处理，避免用错误轨迹或大量低信息位置稀释教师适应。<br>
**原文位置**：第 3.4 节，式（6）—（8）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练以问题—参考解答对 $(x,y^{\star})$ 为条件，并从当前问题专用学生采样 $y$，因此保持 OPSD 的 on-policy 特性。学生轨迹上的 $\mathcal{L}_S$ 使用 $\operatorname{sg}[P_t^T]$，阻断教师梯度并仅优化学生；教师项 $\mathcal{L}_T$ 使用 $\operatorname{sg}[P_t^S]$，阻断学生梯度并仅优化教师，而且只对 $\gamma_t=1$ 的位置生效。两项均从同一更新前策略快照计算，轨迹和掩码在该次更新中固定；优化完成后再重新采样轨迹并重复流程。教师项中的教师分布位于 KL 的第一参数，因而属于反向 KL 形式，倾向于从学生支持的备选中集中概率；学生项中的学生分布位于第二参数，保持前向 KL 的覆盖性。VISTA 不引入额外采样循环、独立奖励目标或学习型奖励模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 在线自蒸馏与截断前向 KL**

学生轨迹由当前学生在线采样，而不是由固定数据中的参考解答直接提供。标准 OPSD 在每个前缀计算教师到学生的点式截断前向 KL，使学生学习教师支持的多个可能下一词；截断阈值为 $\tau$，词表为 $\mathcal{V}$。

> 直观理解：学生必须面对自己实际会走到的推理状态，教师则在这些真实状态上逐词提供密集反馈；截断项限制异常大的单词级损失，避免个别概率比值主导训练。

**2. 结果门控的学生到教师适应**

教师适应损失只在验证器接受的完整轨迹上启用，因为结果验证提供了“从问题本身能够得到正确答案”的外部证据。教师更新采用 $D^{\mathrm{clip}}_{\mathcal{V},\tau}(P_t^T\|\operatorname{sg}[P_t^S])$，优化 KL 的第一参数，因此具有反向 KL 的模式寻求倾向；其强度由 $\lambda>0$ 控制。

> 直观理解：结果门控并不声称学生每个中间步骤都正确，而是使用最终正确性作为廉价的可靠性筛选器；它比让教师学习所有学生轨迹更不容易强化错误。

**3. 基于教师—学生分歧的 Top-$k$ 位置选择**

对每条合格轨迹，以 $d_t=D_{\mathcal{V}}(P_t^T\|P_t^S)$ 衡量位置分歧，并选择最高的至多 $k$ 个位置。最终掩码同时要求轨迹通过结果验证且位置属于 $\mathcal{I}_k$，因此教师适应既有轨迹级过滤，也有位置级稀疏化。

> 直观理解：如果教师和学生本来意见一致，更新教师的信息量有限；优先处理高分歧位置可以减少教师过快变成学生、进而失去独立指导能力的风险。

**训练与推理**

完整训练过程为：从训练集取 $(x,y^{\star})$；由学生仅根据 $x$ 生成 $y$；在每个前缀上计算 $P_t^S$ 和 $P_t^T$；用确定性验证器决定 $\gamma^{\mathrm{out}}$；计算各位置的教师—学生 KL 分数并形成 Top-$k$ 集合；计算并联合优化 $\mathcal{L}_S+\lambda\mathcal{L}_T$；随后进入下一轮在线采样。训练时教师需要参考解答，学生在训练中也通过教师分布获得特权信息的密集监督，但学生自身的输入始终不含 $y^{\star}$。

推理时只保留训练后的问题专用学生 $\pi_S$：输入新问题 $x$，按学生策略逐步生成答案。推理阶段不需要参考解答、教师、结果验证器或额外的教师适应步骤；$\operatorname{Avg@12}$ 等评估则基于多次生成的结果进行统计。

**复现信息**

为复现实验或公平解读结果，需保留以下方法相关设置：教师更新使用与学生轨迹相同的前缀和同一更新前策略快照；教师适应位置最多为 $k$ 个，短于 $k$ 的轨迹只选至多 $|y|$ 个位置；分歧选择使用未截断的全词表 KL，而训练损失使用点式截断全词表 KL。结果门控依赖任务可执行的确定性验证：数学使用规则化答案检查，代码使用沙箱测试；因此方法的适用性依赖于是否存在可靠的结果验证器。训练不需要额外采样、单独奖励优化或过程级人工标注。原文节选未明确报告学生和教师的具体优化器、学习率、批大小、$\lambda$ 与 $k$ 的统一默认值；其中消融明确考察 $k\in\{8,16,32,64\}$ 及 All 设置，并显示 $k=16$ 的结果最好。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- OpenThoughts mathematical-reasoning corpus：用于训练，沿用 OPSD 的数据、100 步 on-policy 蒸馏预算和学生训练协议；实验使用 Qwen3-1.7B、Qwen3-4B 与 Qwen3-8B。
- AIME 2024 与 AIME 2025：竞赛级数学推理评测集，用于测试模型在不同年份 AIME 题目上的泛化性能；位置预算扫描仅记录这两个数据集的结果。
- HMMT 2025：竞赛级数学推理评测集，与两套 AIME 数据共同构成主评测，用于检验方法在另一数学竞赛来源上的有效性。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Avg@12**

对每道题采样 12 个完整答案后计算平均准确率，衡量模型通过多次采样得到正确解的总体能力。 （越高越好，因为更高表示 12 次采样中正确答案的平均比例更大。）

</div>
<div class="metric-item" markdown="1">

**验证器接受率**

学生 rollout $y$ 在问题 $x$ 上被确定性结果验证器判定为正确并接受的比例，即 $V(x,y)=1$ 的比例；它决定多少轨迹会触发教师更新。 （它不是直接的性能指标；在本实验中主要用于解释训练期间的 outcome gate 覆盖率。）

</div>
<div class="metric-item" markdown="1">

**教师侧 token-level 支持统计**

在固定的、已人工检查为有效的学生轨迹上，统计教师赋予概率不超过 $0.05$ 的 token 数量，并分析教师是否显式提及 privileged reference；这些指标检验教师是否更支持有效的 problem-only 推理及是否减少参考答案泄漏。 （低概率 token 数与显式 reference attribution 轨迹数越少，通常越符合作者对教师适配的解释；它们不是最终数学准确率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨模型规模与三套竞赛数学评测的总体结果

<div class="result-value" markdown="1">

作者称 VISTA 在 Qwen3-1.7B、4B、8B 三种规模上均取得最高 Avg@12；相对 OPSD 的提升分别为 $0.6$、$0.7$ 和 $2.1$ 个百分点。

</div>

这说明学生到教师适配在小、中、大模型上都具有正向结果，而且较大模型上的增益更明显。该结果支持方法的跨规模有效性，但不能单独证明 outcome gate 或 top-$k$ mask 各自是必要的，因为这里比较的是完整 VISTA 与整体基线。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across AIME24, AIME25, and HMMT25 with Qwen3 models at 1.7B, 4B, and 8B, VISTA achieves the highest Avg@12 at every scale, improving over OPSD by $0.6$, $0.7$, and $2.1$ points, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3-8B VISTA 学生的训练过程稳定性

<div class="result-value" markdown="1">

在第 25、50、75、100 步，AIME24 Avg@12 分别为 $74.4$、$76.9$、$78.6$、$76.4$；AIME25 分别为 $71.9$、$69.4$、$71.9$、$71.1$；HMMT25 分别为 $43.1$、$43.9$、$45.6$、$48.3$。

</div>

训练期间没有出现突然崩溃：HMMT25 持续提高，而两个 AIME 指标在相近范围内波动。这支持训练过程总体稳定，但也表明单一 checkpoint 未必在所有数据集上同时最优；它不能证明每一步都带来提升。

<div class="result-source" markdown="1">

来源：附录 D.1，表 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The scores fluctuate only modestly, with no abrupt collapse: HMMT25 improves steadily, while AIME24 and AIME25 remain within comparable ranges.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 稀疏 top-$16$ 更新与 all-position 更新的学生适配规模

<div class="result-value" markdown="1">

Qwen3-8B 在第 100 步的学生有效权重全局二范数 $D^{(2)}$ 为 top-$16$ 的 $1.624$、all-position 的 $1.404$；相对差异为 $15.7\%$。同一步的学生/教师更新规模比为 $\rho_{16}=1.42$ 与 $\rho_{\mathrm{all}}=1.31$。

</div>

在教师只更新高 KL 位置时，后续学生相对于冻结基础模型累积了更大的有效变化，且相对于教师移动幅度的比例也更高。作者据此解释：all-position 教师更新可能过度改变教师，使学生随后获得的有效适配不足。不过这些权重尺度是机制诊断，不是直接的准确率证明。

<div class="result-source" markdown="1">

来源：附录 D.2，图 9；相关定义见附录 D.2，式 (13)--(17)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Figure 9 shows that the top-16 student has larger $D^{(2)}$ at every checkpoint, with its advantage growing from $3.2\%$ at step 25 ($0.637$ versus $0.617$) to $15.7\%$ at step 100 ($1.624$ versus $1.404$).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验摘录没有包含主结果表的逐数据集、逐模型数值，也没有给出 outcome gate 和位置选择消融的 Avg@12 数值；因此对具体变体优劣及各数据集增益的判断仍需核对论文完整表格。
- 评测主要集中于三个竞赛数学数据集，并使用 Qwen3 及单一的 100-step 训练预算；摘录未报告非数学任务、更多模型家族、不同训练预算或不同验证器上的结果，故跨领域与跨验证器可迁移性尚未由这些实验充分建立。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Base model：未经过该训练流程的 Qwen3 模型，用于衡量训练方法相对于初始能力的增益。
- SFT：监督微调基线，用于比较常规的参考答案监督是否足以达到 VISTA 的效果。
- GRPO：基于群体相对奖励的强化学习方法，用于比较另一类结果级数学推理训练方案。
- 标准 OPSD 与 SDPO：OPSD 是最直接的对照，因为 VISTA 保留其学生更新、仅增加教师适配；SDPO 则在相同协议下重新训练，用于比较另一种自蒸馏方法。

**实验想回答的问题**

- 在相同的训练预算与学生训练流程下，VISTA 的学生到教师适配是否能在不同模型规模上稳定优于标准 OPSD 及其他基线？
- 结果提升主要来自哪两个设计：仅在验证器接受的学生轨迹上更新教师，以及仅选择教师—学生 KL 散度最大的少量位置进行更新？

**实验实现**

训练使用 instruct-tuned Qwen3-1.7B、Qwen3-4B 和 Qwen3-8B；沿用 OPSD 的 100-step on-policy distillation budget 与 student-training protocol，仅改变学生学习率。评测在 AIME24、AIME25 和 HMMT25 上报告 Avg@12，并将 VISTA 与 Base、SFT、GRPO、标准 OPSD 的已发表结果比较，同时在相同协议下训练和评测 SDPO。教师适配实验主要改变教师损失权重 $\lambda$ 与位置预算 $k$；作者报告 $\lambda\geq0.75$ 且 $k\in[16,32]$ 是较强、可迁移的工作区间。控制实验固定使用 Qwen3-8B；位置选择比较固定 $k=16$，候选位置限制为 rollout 前 $1{,}024$ 个 token。教师侧分析使用初始教师及第 25、50、75、100 步 checkpoint；有效轨迹库含 100 条经自动验证并人工复核的学生轨迹，reference attribution 分析对 100 个问题各采样一条 privileged-teacher 响应，能力探针使用 30 个验证问题、每题 12 条 privileged-teacher 响应。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Outcome gate：all-rollout、random、reverse 与 VISTA | 控制实验固定使用 Qwen3-8B。all-rollout 在所有 rollout 上启用教师更新；random 对每条轨迹以 $r\sim\operatorname{Bernoulli}(0.6)$ 随机启用；reverse 只在验证器拒绝轨迹上启用；VISTA 只在接受轨迹上启用。随机概率 $0.6$ 根据训练期间约 $60\%$ 的接受率设定。 | 该设计将“更新多少条轨迹”与“更新哪些轨迹”尽量分开：random 匹配大致更新比例，reverse 检验错误轨迹是否适合作为教师监督来源，all-rollout 检验不做 outcome 筛选的效果。给定摘录未提供这些变体的最终 Avg@12 数值，因此只能说明其因果对照意图，不能据此声称某变体的准确率高低。 | 附录 C.1，Outcome gate<br><span class="experiment-evidence">The reverse control enables the update only on verifier-rejected rollouts, while VISTA enables it only on verifier-accepted rollouts.</span> |
| Position selection 与位置预算 $k$ | 位置选择比较固定 $k=16$，包括 first-$k$、last-$k$、random-$k$ 和 KL control；KL control 选择教师到学生方向的 raw KL 分数最高的 $m=\min(k,\|y\|)$ 个位置。位置预算扫描为 $k\in\{8,16,32,64\}$ 及 all-position，所有候选位置均限于 rollout 前 $1{,}024$ 个 token。 | 该消融检验收益是否来自特定的 token 位置，以及稀疏程度是否重要。first/last/random 是位置选择对照，KL control 则直接测试“教师与学生分歧最大处最值得适配”的假设。摘录未报告各变体的准确率表或数值，因此不能将实验设置误写成已证实的性能排序。 | 附录 C.1，Position selection；位置预算扫描见附录 C.1，Position budget<br><span class="experiment-evidence">The KL control ranks all rollout positions by $d_t$ and uses the $m$ positions with the largest scores.</span> |

**定性案例**

- 教师优势并非在每个 token 位置都成立：图 12 展示 privileged teacher 过度支持显式依赖 reference 的 continuation，而 problem-only student 依靠自身推导走出有效路径；图 13 则展示教师低估学生一个局部连贯且最终正确的 problem-only 下一步。该定性证据解释了为什么仅把教师分布作为固定目标可能把参考答案依赖或不必要的路径抑制传给学生，也说明 VISTA 的目标是选择性修正教师，而不是假定教师逐 token 永远优于学生。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该工作通过结果验证的 rollout 改进教师与学生之间的自蒸馏监督，属于面向推理能力的验证驱动后训练方法。; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`e9e86bc99793fec3d67a3a09aa680867a301032967d98fd761095ebdd3f07a73`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
