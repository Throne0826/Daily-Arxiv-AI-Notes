---
title: "[论文解读] Beyond Uncertainty: Multi-Solver Disagreement Rewards for Self-Evolving Reasoning Curricula"
description: "[arXiv 2608.30035][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.30035"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:47:19.410960+00:00"
source_sha256: "518ca9606055dcaa15ddd9b0bd7c7682e9c1c763256bf19f57008ccc1415b29e"
tags:
  - "LLM Reasoning"
  - "无数据自进化"
  - "Challenger–Solver"
  - "多 Solver 分歧"
  - "自适应课程"
  - "奖励坍缩"
  - "群组相对策略优化"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.30035</p>

# Beyond Uncertainty: Multi-Solver Disagreement Rewards for Self-Evolving Reasoning Curricula

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Vinoth Selvendran, Zhanming Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30035v1) · [PDF 下载](https://arxiv.org/pdf/2608.30035v1) · **关键词** 无数据自进化, Challenger–Solver, 多 Solver 分歧, 自适应课程, 奖励坍缩, 群组相对策略优化<br>


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

本文研究面向大语言模型推理训练的“无数据自进化”框架。其核心是 Challenger–Solver（出题者—解题者）交替优化：Challenger 自动生成问题，Solver 尝试求解，再由 Solver 的表现构造奖励以更新 Challenger，从而形成随能力变化的训练课程，无需人工标注。既有 R-Zero 主要以同一 Solver 多次采样答案的不一致程度衡量问题难度；本文关注的背景性矛盾是，这种单模型内部不确定性会随答案趋同而消失，而且无法判断低不确定性究竟表示问题真正简单，还是问题恰好符合该模型的固有偏差。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**Challenger–Solver 协同进化**

Challenger 负责生成能够暴露 Solver 能力缺口的问题，Solver 则利用这些问题继续训练。两者交替冻结与更新，使训练数据的难度随 Solver 的能力动态变化。

</div>
<div class="concept-item" markdown="1">

**采样不确定性与模型间分歧**

采样不确定性考察同一模型对同一问题多次回答是否一致；模型间分歧则考察多个异构 Solver 的代表答案是否冲突。前者可能因单个模型变得自洽而坍缩，后者可揭示不同模型能力或偏差之间的差异。

</div>
<div class="concept-item" markdown="1">

**多数答案、伪标签与香农熵**

多数答案是从多次采样中出现最频繁的等价答案，跨样本多数投票得到的答案可作为无人工标注条件下的伪标签。香农熵衡量答案类别分布的分散程度：多个 Solver 越倾向于给出不同答案，熵越高。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

设参数为 $\theta$ 的 Challenger $Q_\theta$ 生成问题 $q$，异构 Solver 集成 $\mathcal{E}=\{S_1,\ldots,S_N\}$ 对该问题作答；每个 $S_i$ 独立采样 $k$ 次，并通过符号等价匹配和多数投票形成该变体的代表答案 $a_i$。系统在 Challenger 训练阶段冻结 Solver，根据池化采样不确定性、跨 Solver 分歧以及重复惩罚构造问题奖励并用 GRPO 更新 Challenger；随后冻结 Challenger，用筛选后的生成问题及多数投票伪标签训练 Solver。该设定假定无需人工训练数据或人工偏好标签，并通过模型容量和采样温度不同的 Solver 变体提供异质性；目标不是从固定题库挑选样本，而是直接引导生成器产生处于真实能力边界附近、能够支持稳健推理学习的问题。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$Q_{\theta}$**

参数为 $\theta$ 的 Challenger 模型，负责生成训练问题。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{E}=\{S_1,\ldots,S_N\}$**

由 $N$ 个 Solver 变体构成的异构集成。

</div>
<div class="notation-item" markdown="1">

**$a_i$**

Solver 变体 $S_i$ 对问题进行 $k$ 次采样后，经多数投票与符号等价匹配得到的代表答案。

</div>
<div class="notation-item" markdown="1">

**$\hat{p}$**

池化答案集合相对于多数投票伪标签 $\tilde{y}$ 的经验正确率，用于描述单模型式采样不确定性。

</div>

</div>

**直接相关的工作**

- **R-Zero（Huang et al., 2025）**: 本文直接扩展的 Challenger–Solver 框架。R-Zero 用单一 Solver 的多次采样不一致性奖励 Challenger；本文保留其交替训练结构和数据流程，但以异构多 Solver 的答案分歧补充奖励信号，以缓解答案趋同造成的奖励坍缩。
- **Query-by-Committee（Seung et al., 1992）**: 提供“委员会分歧代表样本信息量”的相关思想。区别在于传统方法通常从固定数据池中选择分歧较大的样本，而本文把分歧直接用作生成式强化学习课程的奖励，主动改变 Challenger 将生成的问题分布。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

自演化推理系统希望在不依赖人工标注数据的情况下，自动生成能够推动模型进步的训练题目。其核心需求是可靠地判断一道题是否真正位于 Solver 的能力边界：题目过易不能带来有效学习，题目过难又可能难以产生可信的训练信号。若题目难度判断失真，Challenger 生成的课程就会偏离 Solver 的实际能力，限制持续自我改进。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于单 Solver 采样不确定性的自演化方法（以 R-Zero 为代表）**：Challenger 生成题目后，让同一个 Solver 独立采样多次，并根据答案是否一致计算采样不确定性。若 Solver 对同一道题大约一半答对、另一半答错，即 $4\hat{p}\approx 0.5$4，通常被视为题目接近其能力边界，Challenger 因而获得较高奖励；Solver 再利用筛选后的题目和多数投票伪标签进行训练。
- **Challenger–Solver 协同进化课程生成**：系统把题目生成者 Challenger 与解题者 Solver 放入循环：Challenger 产生针对 Solver 弱点的问题，Solver 学习解决这些问题，更新后的 Solver 再为下一轮题目生成提供反馈。该范式试图用模型间的自动交互替代人工课程设计和大规模人工数据整理。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单 Solver 的采样不确定性会随着 Solver 适应 Challenger 的题目分布而塌缩：多个采样答案逐渐趋于一致，奖励接近零，Challenger 因而缺乏继续发现有价值题目的学习信号。换言之，奖励下降可能只表示模型在当前分布上形成了稳定反应，并不一定表示题目已经充分覆盖真实能力边界。
- 该信号把模型自身的不确定性误当作普遍难度，无法区分“对某个模型容易但对其他模型困难”的题目。原文指出，R-Zero 的伪标签准确率在三轮迭代中从 79% 降至 63%，并报告“model performance degrading after iteration 3”（Introduction，引用 Huang et al. (2025) 的 Section 4.4、Table 5），说明单模型不确定性可能逐渐成为不可靠的难度代理；其后果是课程可能被模型偏见或既有解题模式牵引，而非针对可迁移的推理能力。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有方法主要利用单个 Solver 的模型内采样差异来评价题目，却缺少一种能够衡量不同模型之间能力边界差异、同时又能直接接入现有 Challenger 训练流程的奖励信号。因此，尚未解决的问题是：如何在不增加人工数据、也不改动底层强化学习框架的前提下，使 Challenger 发现那些能暴露真实且具有迁移价值的推理弱点的题目。

</div>
<div markdown="1"><span>核心问题</span>

与单 Solver 的采样不确定性相比，基于异质 Solver 集成的跨模型答案分歧，能否提供更稳定、更有区分度的 Challenger 奖励，从而生成更有效的自演化推理课程并提升下游 Solver 的泛化能力？

</div>
<div markdown="1"><span>作者直觉</span>

如果多个能力和采样温度不同的 Solver 对同一道题给出不同的多数答案，这种分歧更可能反映题目触及了模型之间真实的能力边界，而不只是某一个模型的随机采样波动。作者因此用各 Solver 的多数答案分布计算归一化 Shannon 熵：答案越分散，熵越高，Challenger 获得的 disagreement reward 越大。直观地说，单模型信号问的是“这个模型自己是否犹豫”，多模型信号问的是“不同模型是否在这道题上出现系统性分歧”；后者有望减少单一模型偏见，并把课程推向适中的、能够促进稳健推理学习的难度区域。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

方法将原有基于单个 Solver 采样不确定性的 Challenger 奖励，扩展为结合单模型不确定性与多 Solver 分歧的复合奖励。给定 Challenger 生成的问题 $q$，系统把它并行发送给三个具有不同温度或模型架构的 Solver 变体，分别聚合答案、计算答案分布的不确定性与变体间的答案分歧，最后扣除问题重复惩罚并将所得奖励用于 Challenger 的 GRPO 训练。直观地说，系统不再只观察一个学生是否“答得摇摆”，还观察不同学生是否对同一道题得出不同结论，因此能发现单一模型已经自信但仍可能存在能力边界的问题。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 交替生成问题与固定模型

Challenger 生成问题及其参考答案；在 Challenger 训练阶段冻结 Solver，在 Solver 训练阶段冻结 Challenger，并通过 GRPO 交替更新两者参数。

<div class="method-step__io" markdown="1">

**输入**：当前 Challenger $Q_{\theta}$、当前 Solver 以及自演化训练框架中的问题生成 rollout。<br>
**输出**：待评估的问题 $q$，以及用于后续奖励计算的固定 Solver 集合 $\mathcal{E}$。

</div>

**直观理解**：可以把它看成出题者和答题者轮流升级：先固定答题者来评价新题，再固定出题者来训练答题者，避免双方同时变化导致奖励含义不稳定。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多 Solver 并行采样与答案归并

每个变体独立生成 $k=10$ 个答案；利用符号等价检查、数值容差 $\epsilon=10^{-6}$ 和 Union-Find 将数学上等价的答案聚类，并选取最大等价类的代表作为该变体的 plurality answer $a_i$。

<div class="method-step__io" markdown="1">

**输入**：有效问题 $q$ 与三个 Solver 变体 $S_a$、$S_b$、$S_c$。<br>
**输出**：每个 Solver 的代表答案 $a_i$，以及全部变体答案组成的池化答案集合。

</div>

**直观理解**：同一个 Solver 先作答多次，再把只是写法不同但数学意义相同的答案视为同一答案；这样奖励比较的是解答结论，而不是字符串表面差异。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算不确定性与跨模型分歧

根据最大答案等价类的经验比例 $\hat{p}$ 计算单模型不确定性 $r_{\mathrm{unc}}$；再根据三个代表答案的等价类分布计算归一化 Shannon 熵 $r_{\mathrm{dis}}$。

<div class="method-step__io" markdown="1">

**输入**：池化后的全部答案、三个变体的代表答案，以及多数投票伪标签 $\tilde{y}$。<br>
**输出**：问题级不确定性奖励 $r_{\mathrm{unc}}(q)$ 与多 Solver 分歧奖励 $r_{\mathrm{dis}}(q)$。

</div>

**直观理解**：前一个信号问“所有回答混在一起是否摇摆”，后一个信号问“不同类型的答题者是否意见不一致”；后者能够捕捉每个模型内部都很自信、但模型之间结论不同的题目。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 合成奖励与 Challenger 更新

按 $r(q)=\alpha r_{\mathrm{unc}}(q)+\beta r_{\mathrm{dis}}(q)-r_{\mathrm{rep}}(q)$ 合成奖励，其中默认 $\alpha=1.0$、$\beta=0.5$；随后将该奖励输入 GRPO 以更新 Challenger。

<div class="method-step__io" markdown="1">

**输入**：$r_{\mathrm{unc}}(q)$、$r_{\mathrm{dis}}(q)$、批内重复惩罚 $r_{\mathrm{rep}}(q)$ 以及 Challenger 生成的 rollout。<br>
**输出**：偏向高不确定性、高跨 Solver 分歧且低重复度问题的新 Challenger 策略，进而形成更具挑战性的训练课程。

</div>

**直观理解**：出题者会得到三方面反馈：题目是否让答题者犹豫、不同答题者是否冲突、题目是否只是重复旧题；综合反馈指导它逐渐生成更能暴露真实能力缺口的问题。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 单 Solver 不确定性奖励

$$
\hat{p}=\frac{1}{m}\sum_{j=1}^{m}\mathbf{1}[y_j=\tilde{y}],\qquad r_{\mathrm{unc}}(q)=\min(\hat{p},1-\hat{p})
$$

**符号说明**

- $q$：Challenger 生成的问题。
- $S_{\phi}$：参数为 $\phi$ 的 Solver。
- $m$：单个 Solver 对问题 $q$ 生成的答案数量。
- $y_j$：第 $j$ 个采样答案。
- $\tilde{y}$：对采样答案进行多数投票得到的伪标签。
- $\mathbf{1}[\cdot]$：条件成立时取 $1$、否则取 $0$ 的指示函数。
- $\hat{p}$：等于多数投票伪标签的答案比例。
- $r_{\mathrm{unc}}(q)$：问题 $q$ 的单 Solver 采样不确定性奖励。

<div class="equation-explanation" markdown="1">

**直观理解**：当答案大致一半支持伪标签、另一半不支持时，$\hat{p}$ 接近 $0.5$，奖励最大；当 Solver 几乎总是给出同一答案时，奖励趋近于零。这正是该信号在 Solver 变得自信后会失去训练梯度的原因。<br>
**原文位置**：第 4.1 节，公式 (1)–(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 多 Solver 分歧奖励与复合奖励

$$
r_{\mathrm{dis}}(q)=\frac{H(a_{S_a},a_{S_b},a_{S_c})}{\log|\mathcal{E}|},\qquad r(q)=\alpha r_{\mathrm{unc}}(q)+\beta r_{\mathrm{dis}}(q)-r_{\mathrm{rep}}(q)
$$

**符号说明**

- $\mathcal{E}$：Solver 变体集合，本文为 $\{S_a,S_b,S_c\}$。
- $a_{S_i}$：Solver 变体 $S_i$ 的 $k$ 次采样答案经等价聚类后选出的最大类代表答案。
- $H(\cdot)$：在代表答案等价类分布上计算的 Shannon 熵，使用自然对数。
- $|\mathcal{E}|$：Solver 变体数量，用于熵归一化。
- $r_{\mathrm{dis}}(q)$：不同 Solver 对问题 $q$ 给出不同代表答案时产生的归一化分歧奖励。
- $\alpha$：单 Solver 不确定性项的权重，本文默认取 $1.0$。
- $\beta$：多 Solver 分歧项的权重，本文默认取 $0.5$。
- $r_{\mathrm{rep}}(q)$：基于批内 BLEU 聚类计算的问题重复惩罚。
- $r(q)$：用于 Challenger 优化的最终问题级奖励。

<div class="equation-explanation" markdown="1">

**直观理解**：归一化熵衡量三个 Solver 的结论是否分散：一致回答时为零，答案越分裂则越大。复合式奖励把这种跨模型冲突作为补充信号，同时压低重复问题，使 Challenger 更可能生成能揭示真实推理差异的新题。<br>
**原文位置**：第 4.2–4.3 节，公式 (3)–(4)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：该方法本身不改变 R-Zero 的优化器或训练框架，而是替换 Challenger 的奖励函数。Challenger 通过 GRPO 最大化其生成 rollout 所获得的组相对奖励；Solver 则在 Challenger 冻结时，使用生成的问题进行 GRPO 训练。默认目标奖励由 $r_{\mathrm{unc}}$、$r_{\mathrm{dis}}$ 和 $r_{\mathrm{rep}}$ 组成，解析失败的输出获得固定负奖励 $-1$，以惩罚无法提取有效 $\backslash\mathrm{boxed{} }$ 内容的生成结果。其核心优化含义是：提高 Challenger 生成高信息量、低重复度问题的概率，而不是直接用分歧熵训练 Solver 的答案生成器。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 异构 Solver 集合**

集合定义为 $\mathcal{E}=\{S_a,S_b,S_c\}$：$S_a$ 是经过 GRPO 训练的 Qwen3-4B Solver v1，在温度 $T=0.7$ 下采样；$S_b$ 使用相同权重但温度 $T=1.0$，提供采样多样性；$S_c$ 是温度 $T=0.7$ 的 Llama-3.2-3B-Instruct，提供架构差异。因此，集合同时覆盖同架构的采样敏感性和跨架构的模型分歧。

> 直观理解：如果只用一个模型，模型可能对自己熟悉的错误模式也很自信。让不同温度和不同架构的“答题者”共同作答，可以更容易发现模型之间的能力边界。

**2. 答案等价类与分歧熵**

每个变体的 $k$ 个答案先通过数学等价检查聚类，再以最大等价类代表 $a_i$ 参与跨变体比较。分歧奖励在三个代表答案的等价类分布上计算 Shannon 熵，并除以 $\log|\mathcal{E}|$，从而将奖励归一化到 $[0,1]$；三个变体一致时为 $0$，三个答案互异时为 $1$。

> 直观理解：“$1/2$”和“$0.5$”应被视为同一个答案，否则系统会把表达方式差异误判为推理分歧。归一化熵则把意见越分散的问题赋予越高分。

**3. 复合奖励与鲁棒边界处理**

复合奖励保留原有单 Solver 不确定性，并以较小权重加入分歧项，同时减去批级 BLEU 聚类得到的重复惩罚。解析失败的输出直接获得 $r(q)=-1$；若部分 Solver 超时，则仅用实际返回的变体计算分歧熵，并相应使用响应变体数进行归一化。

> 直观理解：新信号是对旧信号的补充而不是完全替代，因此训练仍保留原框架的行为；格式错误、重复出题和服务超时也不会被误当成有价值的困难题。

**训练与推理**

训练时，Challenger rollout 首先被解析为问题和参考答案；有效问题并行发送到三个独立推理引擎，每个引擎生成 $10$ 个答案。系统完成答案等价聚类、池化答案的不确定性计算、三个代表答案的分歧熵计算和批级重复惩罚后，返回 $r(q)$；该奖励用于更新 Challenger，随后固定更新后的 Challenger 来训练 Solver，循环进行。推理或评估阶段则使用训练后的 Solver 在目标数学基准上作答；给定章节没有说明评估阶段继续使用该奖励系统。

**复现信息**

实现采用三个独立 GPU 推理引擎，并通过轻量 HTTP 接口和线程池并发调用；每个引擎设置每题 30 秒超时。数学答案使用 `mathruler.grade_answer` 进行符号化简和容差比较，再以 Union-Find 合并等价类；批内重复问题仅对成功解析的问题进行 BLEU 聚类。相较单 Solver 评价，每个 batch 的墙钟时间约增加 8 分钟，总 GPU 小时开销约为约 3 倍；这些开销是该方法获得跨模型分歧信号所需的代价。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MATH-500：竞赛数学评测集，用于测试 Solver 在具有多步推理要求的数学问题上的 pass@1 准确率；原文未明确报告其训练、验证和测试划分规模。
- AMC：美国数学竞赛类评测集，用于检验方法在竞赛级数学题上的迁移表现；原文未明确报告具体题目数量及划分方式。
- Olympiad：奥林匹克数学类评测集，用于测试更高难度竞赛数学推理；原文未明确报告具体题目数量及划分方式。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**pass@1 accuracy**

模型仅生成一次答案时答案正确的比例，用于衡量最终 Solver 的直接解题能力。 （越高越好，因为更高数值表示更多题目被一次性正确解决。）

</div>
<div class="metric-item" markdown="1">

**R-Zero 与 Ours 的准确率差值**

本文重点关注的相对改变量，用于比较多求解器分歧课程相对于单求解器不确定性课程的增益。 （对 Ours 而言差值越高越好；它比绝对分数更适合控制不同答案验证流程造成的整体分数偏移。）

</div>
<div class="metric-item" markdown="1">

**批次奖励均值及标准差**

在 Challenger 训练日志中统计 $r_{\mathrm{dis}}$ 与 $r_{\mathrm{unc}}$ 的平均水平和波动程度，用于观察奖励是否提供持续、可区分的训练信号。 （分歧奖励均值提高且标准差降低通常更有利，表示信号增强并趋于稳定；不应单独把奖励绝对值等同于最终解题能力。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 竞赛数学综合表现：比较 R-Zero 与 Ours 在 MATH-500、AMC 和 Olympiad 上的 Comp. Avg pass@1。

<div class="result-value" markdown="1">

Ours 的竞赛数学平均准确率为 45.69%，高于 R-Zero 的 44.35%，提升 1.34 个百分点。

</div>

这支持作者关于多求解器分歧课程能够把训练信号更有效地集中到竞赛数学能力上的主张。由于两者使用相同评测流程，该差值具有较好的内部可比性；但它不能证明方法在所有数学或非数学任务上都普遍更强，也不能排除一次额外 Challenger 迭代或课程规模等因素的影响。

<div class="result-source" markdown="1">

来源：Table 1, Section 5.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Comp. Avg 33.41 36.38 44.35 45.69

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 分项竞赛数学结果：分别比较 MATH-500、AMC 和 Olympiad 上的 R-Zero 与 Ours。

<div class="result-value" markdown="1">

Ours 相比 R-Zero 在 MATH-500、AMC 和 Olympiad 上分别提高 1.20、1.32 和 1.48 个百分点，三个竞赛数学数据集均有提升。

</div>

提升覆盖不同难度和题型范围的竞赛数学评测，而不是只由单一数据集驱动，因此与“课程更关注能力边界”的解释相一致。不过，原文只报告最终准确率，没有提供题目级显著性检验、方差或多次随机种子结果，所以提升的统计稳定性仍需进一步验证。

<div class="result-source" markdown="1">

来源：Section 5.2, immediately after Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The disagreement-Challenger curriculum produces consistent improvements on competition-level math: +1.20 on MATH-500, +1.32 on AMC, and +1.48 on Olympiad (average +1.34 points over R-Zero).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 非竞赛数学对照：比较 GSM8K 上的 R-Zero 与 Ours，以观察竞赛数学增益是否伴随一般小学数学任务的退化。

<div class="result-value" markdown="1">

Ours 在 GSM8K 上为 89.39%，低于 R-Zero 的 89.99%，下降 0.60 个百分点。

</div>

该结果表明方法的收益并非所有评测任务上的全面提升，可能存在课程容量或训练分布向竞赛数学倾斜的权衡。作者将其归因于“reduced curriculum size”，但该解释在当前材料中没有通过额外控制实验得到验证，因此应视为作者的归因而非已经证实的机制。

<div class="result-source" markdown="1">

来源：Table 1, Section 5.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GSM8K 78.32 89.76 89.99 89.39

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

- Base：未进行后训练的 Qwen3-4B-Base，用于提供初始能力参照。
- Post-tr.：Qwen3-4B 后训练模型，用于区分一般后训练收益与自演化课程收益。
- R-Zero：采用标准 R-Zero 第一次迭代、单求解器不确定性奖励训练的 Solver，是最关键的直接基线，因为它与本文方法共享 R-Zero 框架，仅替换 Challenger 的奖励信号。
- Ours：采用多求解器分歧奖励生成课程后训练的 Solver，用于检验所提出奖励替换的效果。

**实验想回答的问题**

- 与标准 R-Zero 的单求解器不确定性奖励相比，多求解器分歧奖励能否生成更有效的 Challenger 课程，并提升 Solver 在竞赛数学任务上的最终能力？
- 多求解器分歧奖励在 Challenger 训练期间是否能够保持并增强学习信号，而不是像单模型采样不确定性那样趋近于零？

**实验实现**

实验基于 R-Zero，主干模型为 Qwen3-4B-Base，并使用官方 GRPO 超参数：batch size 为 16、Questioner 训练 6 步、Solver 训练 20 步、每题采样 $m=10$ 个答案。硬件为 8 张 NVIDIA H100-80GB，其中 4 张用于 FSDP trainer，3 张用于集成模型推理服务。$S_a$ 与 $S_b$ 共享 Solver v1 checkpoint，但采样温度分别为 0.7 和 1.0；$S_c$ 为温度 0.7 的 Llama-3.2-3B-Instruct，从而形成不同模型容量与采样温度的异质求解器集成。实验先运行标准 R-Zero 的一次迭代作为基线，再额外运行一次使用分歧奖励的 Challenger 迭代，最后用生成的课程训练 Solver 并评测。每次 Challenger 迭代约耗时 14 个 GPU-小时。所有模型均采用同一评测流程和 mathruler 进行答案判定，并使用符号等价检查及 Claude Sonnet 4.6 复核；作者指出，这一流程不同于原 R-Zero 使用 GPT-4o 判定的流程，因此本文主要比较相同流程下的相对差值，而非跨论文比较绝对分数。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 奖励信号对照：单求解器不确定性奖励 $r_{\mathrm{unc}}$ 与多求解器分歧奖励 $r_{\mathrm{dis}}$ 的训练动态比较。 | $r_{\mathrm{dis}}$ 从 0.609 增至 0.718，端到端提升 18%，其标准差从 0.336 降至 0.278；$r_{\mathrm{unc}}$ 在训练期间保持稳定。 | 这一对照隔离了奖励定义的差异，显示分歧奖励没有像论文所担忧的单模型奖励那样失去变化，反而在 Challenger 训练中保留了增长的优化信号。它是奖励层面的消融，而不是完整的模型架构消融；因此不能单独证明奖励动态一定导致了最终准确率提升。 | Table 2, Section 5.3<br><span class="experiment-evidence">$r_dis$ trends upward (+18% end-to-end) with decreasing variance; $r_unc$ remains stable.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper proposes a multi-solver disagreement reward for generating adaptive curricula that improve LLM mathematical reasoning.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`518ca9606055dcaa15ddd9b0bd7c7682e9c1c763256bf19f57008ccc1415b29e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
