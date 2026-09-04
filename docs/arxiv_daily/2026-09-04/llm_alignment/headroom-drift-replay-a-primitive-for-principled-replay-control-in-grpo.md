---
title: "[论文解读] Headroom-Drift Replay: A Primitive for Principled Replay Control in GRPO"
description: "[arXiv 2609.03941][对齐 / RLHF] 原文未明确报告。"
arxiv_id: "2609.03941"
announcement_date: "2026-09-04"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:39:06.175671+00:00"
source_sha256: "4110c7be9501e0411496d523fdf4a7f752231b4f10ec7b3556d17a578c6b4d21"
tags:
  - "对齐 / RLHF"
  - "强化学习"
  - "LLM Reasoning"
  - "强化学习后训练"
  - "GRPO"
  - "经验回放"
  - "推理语言模型"
  - "Agentic Search"
  - "on-policy训练"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2609.03941</p>

# Headroom-Drift Replay: A Primitive for Principled Replay Control in GRPO

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Hyun Bin Park, Du-Seong Chang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Department of Artificial Intelligence, Sogang University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03941v1) · [PDF 下载](https://arxiv.org/pdf/2609.03941v1) · **关键词** 强化学习后训练, GRPO, 经验回放, 推理语言模型, Agentic Search, on-policy训练<br>


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

本文位于推理语言模型的强化学习后训练领域，重点研究组相对策略优化（GRPO）中的经验回放控制。GRPO通过对同一问题采样的一组回答进行组内比较来更新策略；经验回放则重复利用历史轨迹，以减少昂贵的新鲜 rollout 生成，尤其适用于需要外部环境交互的 Agentic Search。本文将回放视为独立的控制问题：在不改变新鲜 on-policy 数据流、也不增加额外训练机制的情况下，决定哪些历史组值得重用以及哪些仍与当前策略兼容。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**强化学习后训练与轨迹回放**

强化学习后训练通过与任务或环境交互获得轨迹，再依据奖励调整模型策略。轨迹回放把过去收集的轨迹再次用于训练，从而减少重复生成和环境交互的成本，但历史轨迹可能已经过时。

</div>
<div class="concept-item" markdown="1">

**GRPO与组级样本**

GRPO对同一个输入生成一组回答，并利用组内相对奖励或优势来判断哪些回答应被提高概率、哪些应被降低概率。本文以完整的回答组为回放单位，而不是拆开回放单个回答，以保留这种组内比较结构。

</div>
<div class="concept-item" markdown="1">

**On-policy与策略兼容性**

On-policy训练使用当前策略刚刚生成的数据；历史数据通常来自旧策略，因此可能与当前策略分布不一致。回放控制需要判断旧数据是否仍然适合当前策略，否则可能引入过时或不可靠的训练信号。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个正在进行 GRPO 训练的推理模型、当前策略以及由旧策略生成并存储的若干完整回答组，系统同时接收新鲜的 on-policy 组和候选历史回放组。目标是在保持新鲜数据流不变且不引入额外生成或辅助训练模块的前提下，筛选能够有效推动策略学习的历史组，并将其与新鲜组共同用于 GRPO 更新；输出是被准许进入当前训练步的回放组及更新后的策略。核心假设是，一个历史组的价值包含两个可分离方面：它是否仍有足够的学习空间，以及它是否仍与当前策略相容。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$G$**

一个完整的 GRPO 回答组，通常对应同一输入的多条回答及其奖励信息。

</div>
<div class="notation-item" markdown="1">

**$\pi_{\mathrm{cur}}$**

当前正在训练的策略。

</div>
<div class="notation-item" markdown="1">

**$\pi_{G}$**

生成回放组 $G$ 时所使用的行为策略或旧策略。

</div>
<div class="notation-item" markdown="1">

**$r$**

回答或轨迹获得的奖励，用于形成组内相对学习信号。

</div>

</div>

**直接相关的工作**

- **RePO**: RePO将经验回放纳入 GRPO 训练循环，说明在推理强化学习中重复利用历史数据能够提升样本效率。与本文不同，本文把重点收缩到回放选择本身，试图在不加入更大训练管线的情况下分别控制历史组的学习价值和策略兼容性。
- **EFRame**: EFRame将回放与探索、轨迹筛选等机制结合，以决定哪些轨迹被保留和重访。本文并非否定这类综合方法，而是提供一个可独立评估、可组合的回放控制原语，以隔离回放选择对 GRPO 训练的作用。

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

Headroom-Drift Replay 是一个面向 GRPO 的组级回放控制方法。每个训练步首先保持标准 GRPO 的新鲜在线采样不变，再对回放缓冲区中的完整响应组进行两阶段筛选：先用 Headroom 按剩余学习价值排序，再用 Policy Drift 检查该组与当前策略的兼容性；通过筛选的回放组与新鲜组混合后执行标准 GRPO 更新。直观地说，Headroom 负责回答“哪些旧经验仍值得学习”，Drift 负责回答“哪些旧经验已经过时到不应再用”。方法不增加新的自回归生成或环境交互，只增加固定轨迹上的教师强制重新评估。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 新鲜组生成与优势计算

当前策略为每个提示生成包含多个响应的组 $g=(Q,G_1,\ldots,G_n)$，随后按标准 GRPO 计算响应奖励和组相对优势 $A_i$。同时从新鲜组中识别奖励不完全相同的混合结果组，作为本步之后可进入缓冲区的候选。

<div class="method-step__io" markdown="1">

**输入**：当前策略 $\pi_{\theta_t}$、提示批次 $\mathcal{X}_t$。<br>
**输出**：新鲜在线组集合 $\mathcal{G}^{\mathrm{on}}_t$、每个响应及其优势 $A_i$、候选进入集合 $\mathcal{I}_t$。

</div>

**直观理解**：这一步完全沿用普通 GRPO：模型先自己尝试回答，再比较同一提示下不同回答的相对好坏。只有具有区分度的组才会被视为有价值的历史经验候选。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按 Headroom 排序历史组

根据组在生成时策略下计算并缓存的 $\mathrm{Headroom}(g;\pi_{\mathrm{gen}(g)})$，将缓冲区中的完整组按降序排列。回放单位是完整组而不是单个响应，以保留 GRPO 所需的组内相对比较结构。

<div class="method-step__io" markdown="1">

**输入**：训练前已存在的 FIFO 回放缓冲区 $\mathbf{B}_t$，其中每个组保存原生成策略、动作、原生成时对数概率和优势。<br>
**输出**：按学习价值优先级排列的历史组候选序列。

</div>

**直观理解**：Headroom 衡量旧回答还有多少“改进空间”：好的回答若当前概率还不够高，或坏的回答若当前概率还不够低，就更值得重新学习。完整保留一组回答，是为了不破坏 GRPO 通过组内比较获得训练信号的方式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 用 Policy Drift 进行兼容性筛选

对每个候选组的固定历史 token 序列进行一次教师强制前向计算，得到当前策略在这些已存动作上的对数概率；据此计算组级 $\mathrm{Drift}(g;\theta_t)$，仅接受满足 $\mathrm{Drift}(g;\theta_t)\leq\tau$ 的组。扫描在已接受组数达到 $K_{\mathrm{rep}}$ 或没有更多合格组时停止，并利用同一次前向结果刷新被重新检查组的 Headroom。

<div class="method-step__io" markdown="1">

**输入**：按 Headroom 排序的历史组、当前策略 $\pi_{\theta_t}$、漂移阈值 $\tau$、回放预算 $K_{\mathrm{rep}}$。<br>
**输出**：接受的回放组集合 $\mathcal{R}_t$，其规模不超过 $K_{\mathrm{rep}}$。

</div>

**直观理解**：即使某条旧经验看起来很有价值，如果当前模型已经和当时差异太大，直接使用可能不可靠。Drift 像一道安全门，先排除过时经验，再在剩余经验中优先选择 Headroom 较高者。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 混合更新与缓冲区维护

构造混合 actor 批次 $\mathcal{A}_t\leftarrow\mathcal{G}^{\mathrm{on}}_t\cup\mathcal{R}_t$，使用标准 GRPO 目标执行策略更新；更新完成后才把 $\mathcal{I}_t$ 写入缓冲区，从而禁止同一步生成、同一步回放。缓冲区超过容量时按 FIFO 规则驱逐最旧组。

<div class="method-step__io" markdown="1">

**输入**：新鲜组 $\mathcal{G}^{\mathrm{on}}_t$、接受的回放组 $\mathcal{R}_t$、候选进入集合 $\mathcal{I}_t$。<br>
**输出**：更新后的策略 $\pi_{\theta_{t+1}}$ 和维护后的回放缓冲区 $\mathbf{B}_{t+1}$。

</div>

**直观理解**：训练批次由“刚刚探索的经验”和“经过筛选的旧经验”组成，但新经验不能立即被重复使用。FIFO 规则使存储管理简单且可复现，而 Headroom 和 Drift 决定的是使用哪些旧经验，而不是改变新鲜探索过程。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 组级 Headroom

$$
\mathrm{Headroom}(g;\pi)=\frac{1}{|\mathcal{T}(g)|}\sum_{(i,j)\in\mathcal{T}(g)}h_{i,j}(\pi;g),\qquad h_{i,j}(\pi;g)=\begin{cases}1-\pi(a_{i,j}\mid s_{i,j}),&A_i>0,\\\pi(a_{i,j}\mid s_{i,j}),&A_i<0,\\0,&A_i=0.\end{cases}
$$

**符号说明**

- $g$：一个完整的提示及其多条响应组成的组。
- $\pi$：用于评估该组的策略；回放优先级通常在生成时策略上计算。
- $\mathcal{T}(g)$：组 $g$ 中所有生成 token 位置的集合。
- $a_{i,j}$：第 $i$ 条响应的第 $j$ 个生成动作或 token。
- $s_{i,j}$：生成 $a_{i,j}$ 时的条件上下文。
- $A_i$：第 $i$ 条响应的组相对优势；正值表示应提高该响应概率，负值表示应降低。
- $h_{i,j}$：单个 token 对学习方向的剩余概率修正空间。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把每个 token 的“还可以改多少”汇总成组级分数。正优势动作的概率越低，或负优势动作的概率越高，Headroom 就越大，说明该组仍可能带来较强的定向更新信号。<br>
**原文位置**：第 3.3 节，Headroom 定义

</div>

</div>

<div class="equation-block" markdown="1">

#### 组级 Policy Drift

$$
\Delta_{i,j}(g;\theta)=\log\pi_{\theta}(a_{i,j}\mid s_{i,j})-\log\pi_{\mathrm{gen}(g)}(a_{i,j}\mid s_{i,j}),\qquad \mathrm{Drift}(g;\theta)=\frac{1}{|\mathcal{T}(g)|}\sum_{(i,j)\in\mathcal{T}(g)}\Delta_{i,j}(g;\theta)^2
$$

**符号说明**

- $\Delta_{i,j}(g;\theta)$：当前策略与该组生成时策略在存储动作上的 token 级对数概率差。
- $\pi_{\theta}$：当前待更新策略。
- $\pi_{\mathrm{gen}(g)}$：生成并存储组 $g$ 时使用的冻结参考策略。
- $\mathrm{Drift}(g;\theta)$：组内 token 级漂移平方的平均值，用作回放兼容性分数。
- $\theta$：当前策略的参数。

<div class="equation-explanation" markdown="1">

**直观理解**：该式测量当前策略在整条旧轨迹上的行为变化幅度。漂移越小，旧轨迹越接近当前策略、重要性校正通常越稳定；算法因此只接受满足 $\mathrm{Drift}(g;\theta)\leq\tau$ 的组。<br>
**原文位置**：第 3.4 节，Policy Drift 定义

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：方法不提出新的优化目标；它在混合批次 $\mathcal{A}_t$ 上直接运行标准 GRPO 更新。对每个组，响应级优势 $A_i$ 被复制到该响应的所有 token 位置，并通过当前策略与生成时参考策略之间的比率 $r_{i,j}(\theta;g)$ 参与 GRPO 的策略优化；因此 Headroom 和 Drift 只控制哪些历史组进入批次，不改变 GRPO 的新鲜在线目标或其优势计算方式。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 组级 GRPO 回放状态**

每个组 $g=(Q,G_1,\ldots,G_n)$ 保存完整响应组、每个存储动作的生成时策略 $\pi_{\mathrm{gen}(g)}$ 下的对数概率、动作序列以及响应级优势 $A_i$。对任意 token 位置 $(i,j)\in\mathcal{T}(g)$，当前策略与生成策略之间的 GRPO 重要性比率为 $r_{i,j}(\theta;g)=\frac{\pi_\theta(a_{i,j}\mid s_{i,j})}{\pi_{\mathrm{gen}(g)}(a_{i,j}\mid s_{i,j})}$；因此新鲜组与回放组使用同一更新形式，区别仅在分母所对应的参考策略。

> 直观理解：回放数据必须记住“它当初是由哪个模型生成的”。这样当前模型重新使用旧回答时，才能正确判断策略变化造成的影响，而不是把旧回答误当成当前模型刚生成的回答。

**2. Headroom 学习价值排序**

对正优势响应，Headroom 使用 $1-\pi(a_{i,j}\mid s_{i,j})$ 表示该动作仍有多大概率上升空间；对负优势响应，使用 $\pi(a_{i,j}\mid s_{i,j})$ 表示该动作仍有多大概率下降空间；零优势位置贡献为零。各 token 贡献在组内平均，得到组级学习价值优先级，并首先在生成时策略下计算后缓存。

> 直观理解：它不是简单按新旧排序，而是寻找“方向正确但还没有学充分”的经验。一个好答案还没被模型充分偏好，或一个坏答案仍被模型赋予较高概率，都可能具有较高 Headroom。

**3. Policy Drift 兼容性门控**

对存储动作计算当前策略与生成策略的 token 级对数概率差，并在组内取平方平均作为 $\mathrm{Drift}(g;\theta)$。平方聚合避免正负偏差相互抵消，并对局部较大的策略变化施加更强惩罚；仅当该值不超过阈值 $\tau$ 时才允许回放，且最多接受 $K_{\mathrm{rep}}$ 个组。

> 直观理解：Drift 检查的是当前模型在旧轨迹上的行为是否仍相近。使用平方差是为了防止某些 token 变化很大、但被其他方向相反的变化平均抵消，从而错误地把过时轨迹放进训练批次。

**训练与推理**

训练时，每一步先由当前策略生成新鲜组并计算奖励、优势和回放进入候选，再从已有缓冲区按 Headroom 排序并用当前策略重新评估固定轨迹。通过 Drift 阈值的组与新鲜组混合执行标准 GRPO 更新，更新后才追加候选组并执行 FIFO 淘汰；回放阶段不需要新的自回归生成或环境交互。推理阶段原文未明确报告额外的推理流程或推理时回放，因此可合理理解为使用训练完成后的策略进行普通推理。

**复现信息**

复现时需要为每个组保存不可变的生成时参考状态，包括存储动作、生成时对数概率和优势；当前策略对固定轨迹采用并行教师强制前向计算，同时复用该次前向得到的对数概率刷新 Drift 和被访问组的 Headroom。缓冲区是固定容量 FIFO，扫描达到 $K_{\mathrm{rep}}$ 后停止；未扫描组的缓存 Headroom 可能变旧，但 Drift 门控仍负责阻止过度陈旧的组进入。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 数学推理：AIME24、AMC23、MATH500、Minerva 和 OlympiadBench，用于测试固定且可验证奖励下的 held-out 数学推理能力；完整比较结果见 Table 3，但原文未明确报告各数据集的样本规模与具体划分规模。
- Agentic Search：NQ、TriviaQA、PopQA、HotpotQA、2WikiMultiHopQA、Musique 和 Bamboogle，用于测试需要多轮工具调用和外部环境交互的搜索推理；Table 5 给出七个基准的结果，原文未明确报告各数据集的样本规模与具体划分规模。
- 多模态推理：Geometry3K（Geo3K）、MathVista 和 MathVision，用于测试方法能否迁移到图像与数学联合推理；采用三基准简化视图，结果见 Table 4，原文未明确报告各数据集的样本规模与具体划分规模。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Mean@32**

对每个输入的 $32$ 个样本分数取平均，再对输入取平均；Avg Mean@32 通常等同于各基准 Mean@32 的宏平均，用于衡量整体平均解题质量。 （越高越好，因为分数表示固定可验证奖励下的成功程度。）

</div>
<div class="metric-item" markdown="1">

**Best@32**

对每个输入的 $32$ 个样本取最高分，再对输入取平均；它衡量多次采样中能否产生至少一个高质量答案。 （越高越好；相较 Mean@32，它更关注轨迹质量的上尾，而不只是平均表现。）

</div>
<div class="metric-item" markdown="1">

**Weighted Mean@32**

按各基准的数据规模加权平均其 Mean@32，数据量更大的基准贡献更大，用于补充宏平均视角。 （越高越好，因为它表示按基准规模加权后的平均任务表现。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 数学推理：AIME24、AMC23、MATH500、Minerva 和 OlympiadBench 的跨基准比较

<div class="result-value" markdown="1">

作者报告 Headroom-Drift 在 Avg Mean@32 上超过所有列出的基线，包括匹配预算的纯在线训练、更大在线预算、匹配或更大规模的朴素回放，以及 DAPO、ExGRPO 和 BAPO。Table 3 的 Headroom-Drift 宏平均为 Mean@32 $0.3533$，高于 GRPO on-policy matched 的 $0.3356$、GRPO on-policy larger 的 $0.3344$、朴素回放 matched 的 $0.3117$ 和朴素回放 larger 的 $0.3053$；但其宏平均并未超过 DAPO 的 $0.3409$、ExGRPO 的 $0.3139$ 或 BAPO 的 $0.3469$ 以外的所有具体表中数值关系，原文的“surpassed on Avg Mean@32”与表格中 Headroom-Drift 的 $0.3533$ 一致地支持其超过这些基线。Headroom-Drift 使用 $1{,}843{,}200$ 个 fresh responses，而 GRPO on-policy larger 使用 $2{,}764{,}800$ 个。

</div>

这组实验最直接地测试方法是否比“只增加在线样本”或“把最近轨迹全部重放”更有效。结果支持：有选择地重放比单纯增加新数据或增加回放量更重要。不过它只说明在该实验协议和检查点上平均验证分数更高，不能单独证明 Headroom 和 Drift 各自的因果贡献，也不能说明所有数学任务都会受益。

<div class="result-source" markdown="1">

来源：Section 4.2.1；Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Headroom-Drift leads on Avg Mean@32 across all baselines.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 多模态推理：Geo3K、MathVista 和 MathVision 的三基准比较

<div class="result-value" markdown="1">

Headroom-Drift 的宏平均 Best@32 / Mean@32 为 $0.6017 / 0.4137$，高于 GRPO on-policy matched 的 $0.5732 / 0.3986$、GRPO on-policy larger 的 $0.5786 / 0.4005$ 和 DAPO 的 $0.5800 / 0.4056$；加权平均为 $0.5148 / 0.2883$，也高于三种比较方法的 $0.4839 / 0.2740$、$0.4945 / 0.2788$ 和 $0.4941 / 0.2793$。在单个任务上，Headroom-Drift 的 Geo3K 与 MathVision 两项 Mean@32 分别为 $0.5111$ 和 $0.1475$，均高于三种基线；MathVista 的 Mean@32 为 $0.5825$，低于 DAPO 的 $0.5860$。

</div>

这项结果检验回放控制是否只适用于纯文本数学推理。总体宏平均和加权平均都提升，说明方法在视觉信息参与的推理任务上仍有稳定的总体收益；但 MathVista 单项没有最好，表明收益并非每个数据集、每个指标都一致，不能据此宣称普遍领先。

<div class="result-source" markdown="1">

来源：Section 4.1；Table 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We report a compact three-benchmark view covering Geometry3K (Geo3K), MathVista, and MathVision.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Agentic Search：七个搜索问答基准及 7B 规模检查

<div class="result-value" markdown="1">

在主实验中，Headroom-Drift 的 Avg Mean@32 为 $0.3577$，略高于 GRPO + replay matched 的 $0.3548$，差值为 $0.0029$；Avg Best@32 则为 $0.4879$，高于朴素回放的 $0.4623$。在 7B Search-R1 检查中，Headroom-Drift 将 Avg Mean@4 从 $0.3737$ 提升到 $0.3955$，将 Weighted Mean@4 从 $0.4158$ 提升到 $0.4298$，并在七个基准中的六个领先；其 Avg Best@4 为 $0.5224$，高于朴素回放的 $0.5133$。作者还报告 Headroom-Drift 在包含回放选择开销时，每步时间低于更大在线训练基线；但所给摘录未提供 Table 1 的具体墙钟数值。

</div>

Agentic Search 的重点不是只追求最大平均分，而是检验昂贵环境交互下的成本—质量权衡。Mean@32 的主实验优势很小，可能处于噪声范围，因此不能把它解读为强平均性能提升；Best@32 和 7B 检查的改善更明显，提示选择机制可能更能提高产生优秀轨迹的概率。由于 7B 比较每种方法只有单次运行且使用 Mean@4，结果是有价值的规模信号，但不足以替代多次、统一采样数的稳健验证。

<div class="result-source" markdown="1">

来源：Section 4.2.2；Figure 1(b)；Tables 5–6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the headline Avg Mean@32, Headroom-Drift leads GRPO + replay matched by only 0.0029 (0.3577 vs. 0.3548), a gap within noise range.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前摘录未给出完整的成本表数值、各数据集规模与划分细节、随机种子及多数实验的重复运行信息；尤其 7B Agentic Search 检查明确只有每种方法一次运行，因此小幅提升的统计稳健性仍不清楚。
- 实验结果支持 Headroom-Drift 作为整体方法有效，但摘录未提供 Headroom 排序和 Policy Drift 门控分别移除或替换的严格组件消融，也未报告更多工具环境、模型规模或非固定奖励设置；因此尚不能确定两组件各自的必要性及方法对更广泛场景的泛化范围。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- GRPO on-policy matched：保持新鲜 rollout 预算与回放方法对齐，用来隔离回放复用本身的作用，而不是把更多新数据误认为回放收益。
- GRPO on-policy larger：使用更大的新鲜采样预算，用来检验 Headroom-Drift 的提升能否仅由增加在线数据解释。
- GRPO + replay matched/larger：只按最近保存的群组进行朴素回放，分别使用匹配或更大的回放规模，用来检验回放数量是否足够，还是需要 Headroom 排序与 Policy Drift 门控。
- DAPO，以及数学推理中可直接比较的 ExGRPO 和 BAPO：DAPO 是非回放强基线，ExGRPO 与 BAPO 代表更完整的回放或离线策略方法；Agentic Search 未纳入后两者，因为其公开实现面向 prompt-conditioned reasoning trajectories，而非外部交错工具调用轨迹，直接改造会破坏公平比较。

**实验想回答的问题**

- 在数学推理、智能体搜索和多模态推理中，仅加入 Headroom-Drift Replay 这一回放控制机制，是否能在相同或更少新鲜采样预算下超过纯在线训练、朴素回放及更复杂的回放方法？
- 在环境交互成本占主导的 Agentic Search 中，回放选择是否能在保持或提高 Mean@32 的同时降低训练墙钟时间，并且是否改善高质量轨迹的上界表现？

**实验实现**

实验在三类 GRPO 风格设置中进行，并以 Mean@32 作为跨领域主指标，同时结合 acquisition cost；Table 1 将每步平均墙钟时间作为主要成本指标。数学推理中使用完整基线集合，多模态推理采用三基准简化比较，Agentic Search 主要比较 GRPO on-policy matched、GRPO on-policy larger、GRPO + replay matched 和 DAPO。7B 规模检查使用 Search-R1 与 Qwen2.5-7B-Instruct；为适应计算预算，两种方法都使用 8-bit optimizer，并对每个输入采样四个答案，因此报告 Mean@4 和 Best@4。原文未明确报告统一的随机种子、重复运行次数以及所有设置的完整训练超参数；7B 检查明确为每种方法单次运行。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 数学推理中的预算与回放规模对照：在线训练 matched/larger，以及朴素回放 matched/larger | 相较 GRPO on-policy matched 的宏平均 Mean@32 $0.3356$，Headroom-Drift 为 $0.3533$；相较更大在线预算的 $0.3344$ 也更高。朴素回放 matched 和 larger 分别为 $0.3117$ 和 $0.3053$，均低于 Headroom-Drift。 | 这不是严格的单因素模块消融，而是针对两个替代解释的控制实验：如果提升只是来自更多 fresh responses，较大在线基线应能解释结果；如果只要增加 replay 数量就够，较大朴素回放应更强。结果反而支持“选择哪些群组”比“重放多少群组”更关键，但不同设置的总训练预算与数据组成仍可能存在其他差异。 | Section 4.2.1；Table 3<br><span class="experiment-evidence">Against GRPO + replay matched and GRPO + replay larger, the margin widens further, indicating that replay quality depends on principled subset selection rather than on replay volume.</span> |
| Agentic Search 的 7B 规模检查：Headroom-Drift 对比 GRPO + replay matched | 在相同配置、8-bit optimizer 和每个输入四个样本的条件下，Headroom-Drift 的 Avg Mean@4 为 $0.3955$，朴素回放为 $0.3737$；Weighted Mean@4 为 $0.4298$，朴素回放为 $0.4158$；Best@4 分别为 $0.5224$ 和 $0.5133$。 | 该检查主要隔离方法在较小模型和较少采样数下是否仍有效，而不是检验 @32 性能。它显示收益没有完全依赖大模型或大量样本，但每种方法只有一次运行，且降低采样数会改变 Best 与 Mean 的统计性质，因此应视为支持性证据而非最终结论。 | Appendix B, Table 6<br><span class="experiment-evidence">The controlled comparison is based on one run per method with four samples per input.</span> |

**定性案例**

- 训练动态案例：数学推理的 Figure 4 显示，回放训练曲线在较宽的中后期区间高于 GRPO on-policy matched，并在相当长一段区间高于 GRPO on-policy larger；附录的 training-score-matched 分析进一步称回放延迟进入低熵区间。这可解释为回放可能让模型在相近训练分数下保持更久的探索，但原文摘录没有给出曲线的具体数值或独立统计检验。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出用于 GRPO 后训练的原则性轨迹重放控制方法，核心涉及推理模型的强化学习训练效率与经验复用。; rule check: matched taxonomy keywords; top rule score=5.0
- 全文指纹：`4110c7be9501e0411496d523fdf4a7f752231b4f10ec7b3556d17a578c6b4d21`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
