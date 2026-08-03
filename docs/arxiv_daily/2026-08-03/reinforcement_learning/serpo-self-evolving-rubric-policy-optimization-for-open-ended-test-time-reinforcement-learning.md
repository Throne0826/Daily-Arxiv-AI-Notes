---
title: "[论文解读] SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning"
description: "[arXiv 2607.26873][强化学习] SERPO旨在让语言模型在没有参考答案、人工反馈、外部奖励模型或更强评审器的开放式测试场景中，通过共同演化响应档案、查询专属评分准则与策略参数，自主构造持续有效的强化学习奖励。"
arxiv_id: "2607.26873"
announcement_date: "2026-08-03"
primary_category: "reinforcement_learning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-03T02:16:23.472577+00:00"
source_sha256: "2f1992274882b069d80f79fca2ba603a260785ff23360b48de0c14bdd24c81d8"
tags:
  - "强化学习"
  - "LLM Reasoning"
  - "测试时强化学习"
  - "开放式生成"
  - "传导式适应"
  - "伪奖励"
  - "查询特定量规"
  - "组相对策略优化"
  - "自演化"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">强化学习 · arXiv 2607.26873</p>

# SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-03</span>
<span><strong>作者</strong> Jianze Wang, Kunwang Zheng, Ying Liu, Yu Cao, Qilong Zhang, Jinlong Chen, Hua Yang, Qianglong Chen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> School of Artificial Intelligence and Automation, Huazhong University of Science and Technology</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26873) · [PDF 下载](https://arxiv.org/pdf/2607.26873) · **关键词** 测试时强化学习, 开放式生成, 传导式适应, 伪奖励, 查询特定量规, 组相对策略优化, 自演化<br>


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

SERPO旨在让语言模型在没有参考答案、人工反馈、外部奖励模型或更强评审器的开放式测试场景中，通过共同演化响应档案、查询专属评分准则与策略参数，自主构造持续有效的强化学习奖励。

**不用术语来说**：模型部署后可能需要根据一批真实测试问题继续提升，但开放式问题往往有多种同样合理的回答，无法像选择题那样通过“多数答案一致”判断优劣。例如，两份医疗建议可能结论相同，却在禁忌事项、风险说明和就医升级建议上质量不同。因此，关键困难不是生成更多答案，而是在没有标准答案和外部专家的条件下，让模型从自己的回答中辨别细粒度质量差异，并据此可靠地改进自身。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将固定提示集、无标签信息预算下的测试时强化学习扩展到开放式生成，并提出SERPO闭环：为每个查询维护按优劣组织的Good–Normal–Bad响应档案，从响应对比中演化查询专属准则，再用所得奖励更新共享策略。
- 作者提出概率化准则奖励接口：利用模型推理后对Pass/Fail判定词的概率表示满足每条准则的置信度，而非只采用离散裁决；准则还会按区分能力被保留、合并或删除，以适应策略生成质量的变化。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究开放式生成中的测试时强化学习（Test-Time Reinforcement Learning, TTRL）。其核心目标是：部署后的语言模型在没有参考答案、人工反馈、外部奖励模型或更强裁判的条件下，仅利用测试提示及自身生成的回答构造伪奖励，并据此更新策略。传统 TTRL 通常从同一提示采样多个回答，经答案抽取和多数投票得到伪标签；这适合选择题、符号推理等具有规范答案的任务，却不适合医疗建议或研究问答等开放式任务，因为多个有效回答可能措辞不同，而表面结论相同的回答也可能在事实性、完整性和安全性上存在关键差异。本文因此保留“用自生成反馈优化策略”的 TTRL 框架，但把答案一致性替换为针对每个查询的细粒度准则验证。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**固定集合、传导式测试时强化学习**

模型在适应阶段可以反复使用同一组无标签测试提示及其自行采样的回答，并直接更新参数；“传导式”表示这些待适应提示在训练式更新前已经可见。隐藏评分器只用于事后报告，不得参与奖励构造。

</div>
<div class="concept-item" markdown="1">

**量规与原子准则**

量规把开放式回答的整体质量拆成可分别判断的自然语言要求，例如事实正确、覆盖关键风险或避免危险建议；每一项原子准则应尽量只检查一个性质。裁判输出回答满足各准则的概率，再将其聚合为标量奖励。

</div>
<div class="concept-item" markdown="1">

**组相对策略优化（GRPO）**

GRPO 对同一提示的一组回答进行相对比较，将各回答奖励按组均值和标准差标准化为优势，而不另行训练价值评论器。本文沿用其策略更新机制，改变的是奖励来源。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定无标签适应集 $\mathcal{D}_{\mathrm{adapt}}=\{x_n\}_{n=1}^{N}$，在全局步骤 $t$，当前策略 $\pi_{\theta_t}$ 从小批量 $\mathcal{X}_t\subset\mathcal{D}_{\mathrm{adapt}}$ 中取提示，并为每个提示 $x$ 采样 $G$ 个回答，形成 rollout 组 $\mathcal{O}_t(x)$。算法只能使用原始提示、自生成回答以及由这些信息计算的统计量；不能访问参考答案、官方量规、人工或外部评价反馈、辅助语料、外部任务奖励，也不能借助评分器挑选提示。辅助模型如被调用，必须保持冻结且不可访问评测资源。由于真实质量 $r^{\star}(x,o)$ 不可见，学习目标是构造随适应过程更新的伪奖励 $\hat r_t(x,o)$，并提高策略回答的期望伪奖励；每次 actor 更新内部的奖励规则保持固定。适应完成后，隐藏评分器在原适应提示上评估新生成回答，而与其不相交的 $\mathcal{D}_{\mathrm{eval}}$ 用于测量迁移能力。传统答案级 TTRL 以抽取答案是否等于投票伪标签作为二元奖励；本文的问题则是在不存在可靠规范答案时，如何仅依靠模型自身输出建立能够区分事实性、完整性与安全性差异，并可随策略进步持续更新的查询特定奖励。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{D}_{\mathrm{adapt}}=\{x_n\}_{n=1}^{N}$**

适应阶段可见的固定无标签提示集合，其中 $N$ 是提示数量。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{O}_t(x)=\{o_{t,i}\}_{i=1}^{G}$**

步骤 $t$ 时策略针对提示 $x$ 采样的回答组，$G$ 为组大小，$o_{t,i}$ 为第 $i$ 个回答。

</div>
<div class="notation-item" markdown="1">

**$\hat r_t(x,o)$**

在步骤 $t$ 根据允许信息构造的伪奖励，用来替代不可观测的真实质量 $r^{\star}(x,o)$。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{R}=\{(c_m,\rho_m,w_m)\}_{m=1}^{M}$**

由 $M$ 个原子准则组成的量规；$c_m$ 是准则文本，$\rho_m\in\{+1,-1\}$ 表示正向要求或负向失败项，$w_m\geq 0$ 是其权重。

</div>

</div>

**直接相关的工作**

- **基于多数投票或自一致性的答案级 TTRL（Wang et al., 2023；Zuo et al., 2025）**: 这些方法从多个回答中抽取可比较答案，以多数结果作为伪标签，并奖励与其一致的回答。它们构成本文的直接对照，但依赖答案抽取和任务特定的等价关系，无法可靠处理不存在规范答案的开放式生成。
- **策略—量规协同演化方法（RLCER、EvoRubrics、EvoLM、EvoRubric、DynamicRubric）**: 这些方法表明量规可用于开放式回答评价或策略训练，但通常允许结果监督、整理后的量规、更强裁判、可训练的量规或评价模块，或额外语料与生成任务。本文关注更受限的固定集合 TTRL：评价角色保持冻结，奖励只能来自原始提示和模型自生成回答。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

测试时强化学习要求已部署模型只利用原始测试提示及自身采样回答，在同一提示集上反复构造奖励并更新参数。对开放式任务而言，合格回答可能措辞、详略和论证路径不同，而重要质量又体现为事实性、完整性、指令遵循与安全性等多个维度；若没有参考答案、人工反馈、官方评分准则、外部奖励模型或更强评审器，系统仍需产生能随策略演化而保持信息量的奖励信号。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于答案投票或伪标签的测试时强化学习**：对同一问题采样多个解答，以多数投票或自洽聚合选出伪标签，再奖励与该伪标签一致的响应；后续方法通过自我反思、熵置信度或针对多数投票失效的修正来提高伪标签可靠性。
- **基于评分准则的奖励与自演化方法**：把回答拆解为事实性、完整性、安全性等要求并逐项评价。既有研究通常采用基准自带准则、冻结模型给出的准则反馈，或借助结果监督、对抗训练、元验证及响应集合条件化来联合训练策略与准则生成器或评估器；另一些自演化方法还会从预训练文本或源文档生成新任务、提示或课程变体。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 答案投票预设不同响应可以归约为同一个可比较的规范答案，这对选择题、符号推理或可标准化任务较合适，却不适用于存在多种有效表达的开放式生成。它可能奖励多个回答共同遗漏的关键信息，也可能把内容正确但表述不同的答案判为不一致，因而无法提供可靠的优化目标。
- 现有准则奖励或自演化方案往往依赖官方准则、外部数据、结果监督、额外任务生成或更宽松的后训练预算；固定提示集的无标签测试时场景无法使用这些资源。此外，固定准则与离散判定难以保留细微置信度，也未必能在策略能力变化后继续区分新产生的回答。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种适用于开放式生成的固定集测试时强化学习机制：它必须仅从原始查询和当前模型生成的响应中形成查询级评价依据，不把多样回答强行压缩为单一答案，同时使评分准则随策略更新而调整，并将评审的不确定性转化为足够细致、可用于策略优化的奖励。

</div>
<div markdown="1"><span>核心问题</span>

在完全没有标签、外部奖励模型、官方准则或更强评审器的条件下，能否让同一个语言模型利用自身回答之间的质量对比，自主演化出具有区分力的查询专属准则和概率奖励，并由此持续提升开放式生成策略及其跨基准迁移能力？

</div>
<div markdown="1"><span>作者直觉</span>

开放式回答虽然未必共享同一最终措辞，却仍可通过具体质量要求进行相对比较。若先把差异最大的回答组织成好、一般、差三个有序档案，就能从它们的对照中发现“什么特征真正区分质量”；只保留能够稳定拉开这些档案的原子准则，再用Pass/Fail概率表达每条准则的满足程度，可获得比硬投票更细腻的奖励。策略改善后，新回答会暴露旧准则的不足或产生新的区分维度，因而同步刷新档案与准则有望避免奖励迅速失效，形成响应、准则和策略相互推动的闭环。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SERPO 是面向开放式提示的闭环测试时强化学习（TTRL）框架。对每个查询 $x$，系统维护查询局部的 Good–Normal–Bad（G-N-B）响应档案 $\mathcal{E}_t(x)$ 与动态评分准则池 $\mathcal{R}_t(x)$，同时在不同查询之间共享并更新策略模型参数 $\theta_t$。每次遇到查询时，演员模型生成一组回答；固定 judge 将每条准则的布尔判定转成连续满足概率；现有 rubric 先为回答排序并选出差异最大的 G-N-B 三元组；固定 rubric generator 再依据累积档案提出、合并或删除准则；最后利用更新后的准则效用、G-N-B 校准分数构造标量奖励，并通过 GRPO 更新演员模型。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 初始化查询状态并采样回答

首次遇到 $x$ 时，固定 rubric generator 生成非空的查询专属原子准则集合，并以相等权重初始化 $\mathcal{R}_t(x)$。随后演员模型针对 $x$ 采样大小为 $G$ 的 rollout 组 $\{o_{t,i}\}_{i=1}^{G}$。

<div class="method-step__io" markdown="1">

**输入**：当前开放式查询 $x$、共享演员参数 $\theta_t$；若首次遇到该查询，则没有历史档案与 rubric。<br>
**输出**：候选回答组、当前准则池，以及已有或新建的查询局部状态。

</div>

**直观理解**：系统先为当前问题建立一张可修改的评分表，再让正在学习的模型一次写出多个答案。评分表属于该问题，但答题模型在所有问题之间共享学习成果。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 连续准则评分与临时排序

固定 judge 对每个回答—准则对进行推理，并从正、负 verdict token 的概率得到满足概率 $q_J(x,o,c_m)$；负向准则通过取补值统一成“越大越好”的分数 $z_{m,t}(o)$。系统按当前权重聚合这些分数，得到仅用于档案排序的临时分数 $r^{\mathrm{arc}}_{t,i}$，且缓存判定结果供后续效用估计、校准和奖励计算复用。

<div class="method-step__io" markdown="1">

**输入**：查询 $x$、回答 $o_{t,i}$、当前准则 $c_m$ 及其极性 $\rho_m$。<br>
**输出**：每个 rollout 的逐准则连续分数与临时档案排序分数。

</div>

**直观理解**：judge 不只给“通过/不通过”，而是保留判断有多确定，从而避免大量答案同分。正向要求和禁止事项都被转换到同一方向，便于统一加权。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 更新 G-N-B 对比档案

SERPO 在所有满足 Good 分数不低于 Normal、Normal 不低于 Bad 的不同回答三元组中，最大化三段分差的乘积，选出最具区分度的 G-N-B 三元组。若最大分离度为零则不更新，否则把三条回答分别追加到容量受限的 FIFO 档案，得到 $\mathcal{E}_{t+1}(x)$。

<div class="method-step__io" markdown="1">

**输入**：同一 rollout 组的临时分数 $r^{\mathrm{arc}}_{t,i}$ 与查询 $x$ 的历史档案 $\mathcal{E}_t(x)$。<br>
**输出**：按质量层次组织、同时保持明显差异的更新档案 $\mathcal{E}_{t+1}(x)$。

</div>

**直观理解**：系统不是只保存最好和最差答案，而是保存“好、一般、差”三个清晰层次。这样 rubric generator 能看到具体差别，判断哪些要求真正区分回答质量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 自演化 rubric 与准则筛选

到达刷新间隔时，固定 rubric generator 根据强弱回答对比提出原子准则，并与旧池合并：重复要求映射到同一稳定标识，相关但不同的要求保持分离。系统以分数方差和 G-N-B 顺序一致性之积计算准则效用；低效用准则连续三轮处于淘汰区才删除，离开淘汰区则风险计数重置。

<div class="method-step__io" markdown="1">

**输入**：查询 $x$、当前 rubric $\mathcal{R}_t(x)$、更新后的 G-N-B 档案 $\mathcal{E}_{t+1}(x)$。<br>
**输出**：幸存的活动准则集合 $\mathcal{M}_{t+1}(x)$、准则效用 $d_{m,t+1}$ 及更新后的 rubric。

</div>

**直观理解**：新评分项必须既能让不同答案得到不同分数，又应当把 Good 排在 Normal 和 Bad 前面。连续多轮无用才删除，使 rubric 能纠错而不会因一次噪声频繁震荡。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 连续准则满足概率与极性统一

$$
q_J(x,o,c_m)=\frac{\exp \ell_{\mathrm{T}}^{(m)}}{\exp \ell_{\mathrm{T}}^{(m)}+\exp \ell_{\mathrm{F}}^{(m)}},\qquad z_{m,t}(o)=\begin{cases}q_J(x,o,c_m),&\rho_m=+1,\\1-q_J(x,o,c_m),&\rho_m=-1.\end{cases}
$$

**符号说明**

- $x$：当前开放式输入查询。
- $o$：演员模型生成的一个回答。
- $c_m$：索引为 m 的原子评分准则。
- $\ell_{\mathrm{T}}^{(m)},\ell_{\mathrm{F}}^{(m)}$：judge 在完成推理后，对准则 m 的正向与负向 verdict token 分配的对数概率。
- $q_J(x,o,c_m)$：judge 认为回答 o 满足准则 $c_m$ 的概率，取值位于零到一之间。
- $\rho_m$：准则极性；正一表示应满足的正向要求，负一表示应避免的负向要求。
- $z_{m,t}(o)$：第 t 次遇到查询时的极性统一准则分数，数值越大始终表示回答越好。

<div class="equation-explanation" markdown="1">

**直观理解**：该式先把 judge 的二元 verdict 转为连续置信度，保留“明确满足”和“勉强满足”的差异；再对负向准则取补值，使所有评分都遵循越大越好的方向。相比硬判定，这能减少组内奖励并列，为 GRPO 保留更细的优势信号。<br>
**原文位置**：第 4 节“Criterion Scoring and Reward Interface”，式（3）与式（4）。

</div>

</div>

<div class="equation-block" markdown="1">

#### 经效用加权和 G-N-B 校准的最终奖励

$$
r_{t,i}\!\left(o_{t,i},\mathcal{R}_{t+1}\right)=\frac{1}{Z_{t+1}^{\mathrm{rew}}}\sum_{m\in\mathcal{M}_{t+1}}w_{m,t+1}^{\mathrm{rew}}\widetilde{z}_{m,t+1}(o_{t,i}),\quad w_{m,t+1}^{\mathrm{rew}}=\max(\epsilon_u,d_{m,t+1}),\quad \eta_{m,t+1}(o)=\frac{z_{m,t+1}(o)-\mu_{m,t+1}^{B}}{\Delta\mu_{m,t+1}},\quad \widetilde{z}_{m,t+1}(o)=\begin{cases}\operatorname{clip}_{[0,1]}\!\left(\eta_{m,t+1}(o)\right),&\Delta\mu_{m,t+1}\geq\delta,\\z_{m,t+1}(o),&\text{otherwise},\end{cases}\quad \Delta\mu_{m,t+1}=\mu_{m,t+1}^{G}-\mu_{m,t+1}^{B}
$$

**符号说明**

- $r_{t,i}$：第 t 次遇到查询时，第 i 个 rollout 交给 GRPO 的最终标量奖励。
- $\mathcal{R}_{t+1}$：完成本轮准则合并、效用更新和淘汰后的 rubric 状态。
- $\mathcal{M}_{t+1}$：rubric 更新后幸存的活动准则索引集合。
- $d_{m,t+1}$：准则 m 的区分效用，由响应分数方差与 G-N-B 顺序一致性相乘得到。
- $\epsilon_u$：准则奖励权重的正下界，避免幸存准则权重完全为零。
- $w_{m,t+1}^{\mathrm{rew}}$：准则 m 在最终奖励中的效用导出权重。
- $Z_{t+1}^{\mathrm{rew}}$：所有幸存准则奖励权重之和，用于归一化加权平均。
- $\mu_{m,t+1}^{G},\mu_{m,t+1}^{B}$：准则 m 在 Good 档案与 Bad 档案上的平均极性统一分数。
- $\Delta\mu_{m,t+1}$：Good 与 Bad 档案在准则 m 上的平均分差。
- $\delta$：允许进行 G-N-B 校准所需的最小 Good–Bad 分差阈值。
- $\widetilde{z}_{m,t+1}(o)$：经过 G-N-B 区间校准或回退处理后的准则分数。

<div class="equation-explanation" markdown="1">

**直观理解**：最终奖励只使用 rubric 更新后仍然存活的准则，并让更能区分 G-N-B 的准则占更大权重。若某准则确实能拉开 Good 与 Bad，系统以两类档案均值作为动态零点和单位尺度；若分差太小，则不强行放大噪声，而退回原始分数。<br>
**原文位置**：第 4 节“Policy Evolution”，式（8）及其紧随定义。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：SERPO 的直接优化对象是共享演员策略：更新后的 rubric 为同一查询的一组 rollout 产生最终标量奖励 $r_{t,i}$，GRPO 在组内对奖励进行归一化，并依据相对优势更新演员参数 $\theta_t$。原文节选未给出完整 GRPO 损失公式，因此不能进一步写出剪切项、KL 项或优化超参数；方法上的关键区别是，式（5）的 $r^{\mathrm{arc}}_{t,i}$ 仅用于选择档案样本，真正进入策略优化的是 rubric 更新后由式（8）计算的奖励。rubric generator 和 judge 不参与梯度更新，它们只提供固定参考下的准则生成与评分。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 固定的 rubric generator 与 judge**

演员、rubric generator 和 judge 均从部署模型初始化，但只有演员被优化；后两者保留初始权重。rubric generator 根据查询、旧 rubric 和 G-N-B 对比证据提出原子准则，judge 则输出正负 verdict token 的对数概率并形成连续满足分数。

> 直观理解：若负责出评分表或打分的模型也跟着奖励一起训练，评分尺度可能随策略漂移，形成自我迎合。固定两个评价角色相当于保留稳定的尺子，而动态变化的是尺子上的评分项目及其权重。

**2. 查询局部的 G-N-B 档案**

每个查询维护三个容量受限的 FIFO 档案 $\mathcal{A}^{G}_t(x)$、$\mathcal{A}^{N}_t(x)$ 和 $\mathcal{A}^{B}_t(x)$。更新时选择分离度最大的有序三元组，而非简单保存当前最高分和最低分；若所有候选三元组的分离度均为零，则保持档案不变。

> 直观理解：三个档案提供持续更新的“好例、普通例、反例”，使准则生成不依赖外部标签。选择差异明显的三层样本也能减少近似重复回答对 rubric 刷新的干扰。

**3. 可恢复淘汰与 G-N-B 奖励校准**

准则效用同时要求档案内分数有方差，并与 G-N-B 顺序一致；当候选池至少含四项时，效用最低的一定比例进入风险区，连续三轮处于该区才被删除。幸存准则按 $\max(\epsilon_u,d_{m,t+1})$ 加权，并在 Good–Bad 均值差不小于阈值 $\delta$ 时进行区间校准。

> 直观理解：只会给所有答案相同分数，或把坏答案排在好答案前面的准则没有训练价值。延迟删除允许暂时失效的准则恢复，而校准则让不同准则的奖励尺度更可比较。

**训练与推理**

该方法属于测试时在线适应，而不是先离线训练一个独立奖励模型。处理每个查询时，系统依次执行 rollout 采样、固定 judge 连续评分、G-N-B 档案更新、按计划刷新 rubric、计算准则效用与风险计数、生成最终奖励并执行 GRPO；更新后的演员继续服务后续查询，而档案与 rubric 按查询分别保存。因而推断与学习交织进行：当前回答既是用户输出候选，也是下一轮 rubric 和策略更新的数据；演员变化会改变未来回答，未来回答再改变档案、准则、权重与校准范围，从而闭合响应—rubric—策略循环。

**复现信息**

公平复现需要保留三类状态：每个查询的有界 FIFO G-N-B 档案、带稳定标识和连续低效用计数器的查询专属准则池，以及跨查询共享的演员参数。所有已判定的回答—准则元组应缓存并复用于档案排序、效用估计、校准和奖励构造；只需对尚未评分的档案—准则对调用 judge。准则池不足四项时不启用淘汰区；达到四项后，最低 $K_{t+1}=\max\{1,\lfloor\zeta|\widetilde{\mathcal{M}}_{t+1}(x)|\rfloor\}$ 项进入风险区，并在连续三轮处于风险区后删除。原文节选没有明确报告 rollout 组大小 $G$、档案容量、刷新间隔、淘汰比例 $\zeta$、顺序比较边界 $\tau$、校准阈值 $\delta$、权重下界 $\epsilon_u$、GRPO 超参数及具体提示模板，这些数值需查阅论文附录后才能完整复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HealthBench：采用官方HealthBench-500子集，测试安全敏感的医疗建议。它既是一个域内演化基准，也使用官方评估协议进行最终报告；适应期间只能访问提示、模型采样、自生成准则及其统计量，不能访问官方准则、参考答案或最终评估反馈。
- ResearchQA：测试需要证据支撑的长篇科学回答，使用官方评估或验证划分独立进行演化，并作为第二个域内开放式任务。顺序适应实验先在HealthBench训练30个epoch，再切换到ResearchQA训练30个epoch。
- 域外迁移套件：HealthBench演化后的策略直接评测MedQA与LLMEval-Med；ResearchQA演化后的策略直接评测GPQA-Diamond与RaR-Science，不进行额外适应。前两组分别检验医疗与科学领域内，模型能否把从开放式提示中学到的策略迁移到未用于演化的任务。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**官方协议下的0–100评分**

HealthBench、ResearchQA、LLMEval-Med与RaR-Science由GPT-5.1按照各数据集官方准则或协议评分，衡量开放式回答在正确性、覆盖度、安全性或证据质量等任务要求上的总体表现。 （越高越好，因为更高分表示回答更符合数据集规定的质量准则；但该分数依赖自动评估器，不能直接等同于人工确认的真实质量。）

</div>
<div class="metric-item" markdown="1">

**Accuracy**

MedQA与GPQA-Diamond通过直接抽取最终答案计算0–100准确率，用于检验演化后的模型在有明确答案的域外任务上是否答对。 （越高越好，因为它表示正确答案所占比例更高；该指标不评估开放式解释的完整性或安全性。）

</div>
<div class="metric-item" markdown="1">

**Six-benchmark Avg.**

六个基准分数的无权算术平均，用于概括域内与域外任务的整体表现，避免只依据单一数据集下结论。 （越高越好，因为它表示跨基准平均性能更强；无权平均会掩盖任务难度、样本规模和指标语义的差异。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 两个演员骨干在HealthBench与ResearchQA上的30-epoch域内演化

<div class="result-value" markdown="1">

所给节选说明Figure 2比较了四种“模型—基准”域内配置，并在SERPO柱上标注相对Base的增益，但没有提供各配置的具体分数或完整柱状图，因此无法从当前材料核验SERPO的平均提升幅度、显著性或是否在四个配置中全部领先。

</div>

该实验原本回答SERPO能否在不同模型规模与两类开放式任务上普遍改进，而不是只对单一医疗数据集有效。当前节选只交代了比较方式，没有给出数值结果；因此不能把论文设计的研究问题本身当成已证实的结论。

<div class="result-source" markdown="1">

来源：Figure 2说明文字

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Error bars show the standard deviation across three evaluation runs; percentages above the SERPO bars report relative gains over Base, and the break indicates a truncated y-axis.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### HealthBench或ResearchQA演化后，零额外适应迁移到四个域外基准

<div class="result-value" markdown="1">

实验协议明确设置了MedQA、LLMEval-Med、GPQA-Diamond与RaR-Science四个留出基准，但所给节选没有包含Table 1的结果行，因此SERPO是否提高域外平均分、哪些任务受益或是否存在负迁移均为原文未明确报告。

</div>

这个设置比域内提升更能检验模型学到的是一般回答策略还是对固定提示集合的过拟合。由于缺少实际分数，只能确认论文进行了无额外适应的迁移评测，不能确认迁移收益的方向和大小。

<div class="result-source" markdown="1">

来源：Appendix D.1, Evaluation Protocol

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Without further adaptation, HealthBench-evolved policies are evaluated on MedQA and LLMEval-Med, while ResearchQA-evolved policies are evaluated on GPQA-Diamond and RaR-Science.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen3-4B在HealthBench上的45-epoch长程演化

<div class="result-value" markdown="1">

作者报告SERPO在第30个epoch之后仍继续改善，而其他比较方法采用共同的30-epoch预算；节选未提供第30与第45个epoch的具体分数或方差，因此无法量化后续收益。图中的epoch-99结果只是依据epoch 40–45平均斜率外推的描述性预测，并非真实训练观测。

</div>

该结果表明SERPO至少在观察到的45个epoch范围内没有明显在30个epoch处停止进步，支持研究更长适应周期的必要性。不过，由于基线没有同样训练到45个epoch，这不能单独证明SERPO在等长长期预算下优于所有方法；更不能把外推到epoch 99的虚线当作实验成绩。

<div class="result-source" markdown="1">

来源：Figure 2(b)说明文字；长程轨迹的详细协议见Appendix D.1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

SERPO runs for 45 epochs and continues to improve after epoch 30, while all comparison methods use the common 30-epoch budget.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给材料缺少核心结果表与完整消融表，无法报告或核验各模型—基准组合的具体分数、相对增益、标准差及组件移除后的变化；因此上述结论必须结合Table 1、Table 4、Table 5及相应消融结果进行源文复核。
- 最终开放式评分依赖GPT-5.1按官方准则自动评审，且每个请求只生成一次评审结果。三个报告种子可以衡量评估运行波动，但不能消除评估器偏差；此外，只有SERPO延长到45个epoch，长期比较并非所有方法在完全相同训练时长下的对照。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Base：未经测试时强化学习更新的初始模型，用来判断任何性能变化是否确实来自适应过程；图中相对增益也以Base为参照。
- 开放式投票基线：包括Response vote与更强的Claim consensus。前者把每个回答压缩为核心建议并按Jaccard词集相似度聚类，以最大簇成员作为正奖励；后者抽取可核验主张，以至少一半采样都支持的主张构成共识奖励。两者都使用冻结的初始模型自评，且每个提示采样16个回答，而SERPO只采样8个，因此比较并未在采样预算上偏向SERPO。
- RGSD式准则引导测试时扩展：演员模型保持冻结，仅让准则指导生成。静态版本固定初始准则，增强版本允许使用SERPO的准则演化、G-N-B档案和准则池维护，用于区分“改进推理时引导”与“真正更新策略参数”的作用。
- Privileged Policy-Evolution Reference：保持SERPO的采样、GRPO优化器和30-epoch预算，但在适应期间向固定的Qwen3.6-27B评估器暴露数据集官方准则，只演化策略而不演化准则。它不是无标签方法，而是用于估计获得特权监督时策略演化可达到的参考水平。

**实验想回答的问题**

- SERPO在HealthBench与ResearchQA上进行无参考答案的测试时强化学习后，能否稳定提高域内开放式回答质量，并把提升迁移到未参与适应的域外基准？
- 动态准则演化与策略参数更新是否互补，以及准则池、G-N-B档案、评估器设计和更长训练周期分别如何影响性能？

**实验实现**

演员骨干为Qwen3-4B-Instruct-2507和Qwen3.5-9B，均以非思考模式运行；演员通过GRPO更新，准则生成器与概率评审器则是冻结的初始权重副本。SERPO每个提示采样组大小为8，默认演化30个epoch；Qwen3-4B在HealthBench上的长程实验延长至45个epoch，顺序实验则在HealthBench与ResearchQA上各运行30个epoch。演员学习率为$10^{-6}$，训练批量为48个提示，PPO小批量为24个提示，提示与回答的最大长度分别为2048和4096 token。最终报告使用评估种子40、41、42的算术平均，Table 4另报告标准差；这些评估结果不参与奖励、早停、提示选择或检查点选择。GPT-5.1和官方准则只用于最终报告，除明确标记的特权参考外，适应阶段不接收参考答案、官方评分、隐藏评估反馈、人类反馈或外部奖励模型分数。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- Figure 2给出的准则级示例指出，Claim consensus可能保留“高频但不完整”的建议，因为它奖励多个回答反复提到的主张，而不直接判断遗漏了哪些任务要求；SERPO则利用随查询演化的准则和Good–Normal–Bad证据档案比较不同质量层级。这个案例解释了准则演化为何可能比多数共识更适合开放式任务，但它属于机制示意，不能替代跨数据集的定量消融。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Develops a self-evolving rubric-based policy optimization method for open-ended test-time reinforcement learning.; rule check: matched taxonomy keywords; top rule score=6.0
- 全文指纹：`2f1992274882b069d80f79fca2ba603a260785ff23360b48de0c14bdd24c81d8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
