---
title: "[论文解读] Locked at the Entrance, Open Inside: Where RLVR Narrows the Solution Space"
description: "[arXiv 2608.29188][对齐 / RLHF] 原文未明确报告。"
arxiv_id: "2608.29188"
announcement_date: "2026-09-01"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:38:16.662062+00:00"
source_sha256: "97a28e8e14b5822f09837e94413859bdfa03e5c4124341001ab21eff44ef2ff4"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "可验证奖励强化学习"
  - "推理解空间"
  - "入口族"
  - "访问与执行"
  - "探索坍缩"
  - "测试时扩展"
  - "Countdown任务"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.29188</p>

# Locked at the Entrance, Open Inside: Where RLVR Narrows the Solution Space

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Qiancheng Zhou, Ruizhe Li</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: School of Future Technology, Shanghai University；Affiliation: School of Computer Science, University of Birmingham</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.29188v1) · [PDF 下载](https://arxiv.org/pdf/2608.29188v1) · **关键词** 可验证奖励强化学习, 推理解空间, 入口族, 访问与执行, 探索坍缩, 测试时扩展, Countdown任务<br>
**代码**: [https://github.com/ershiyidian/early-branch-locking](https://github.com/ershiyidian/early-branch-locking)

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

本文处于大语言模型数学推理与强化学习交叉领域。可验证奖励强化学习（RLVR）使用答案正确性等可自动检查的信号训练模型，通常能显著提高单次生成正确率 $\mathrm{pass@1}$；测试时扩展则通过重复采样、自一致性或验证器引导搜索，从多个候选推理轨迹中寻找正确答案，因而依赖模型能够生成足够多样的候选路径。已有研究发现，RLVR在提高 $\mathrm{pass@1}$ 的同时可能使输出分布变尖、有效解的覆盖范围缩小，限制重复采样的边际收益。本文进一步把这种收缩定位到推理轨迹内部，区分模型是否会启动某类有效解（access）与启动后能否完成计算（execution）。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**可验证奖励强化学习（RLVR）**

一种用可自动判定的结果作为奖励来优化语言模型策略的训练范式，例如检查数学答案是否正确。其奖励可靠且易扩展，但反复强化常被采样到的成功路径，可能使其他有效路径越来越难被生成。

</div>
<div class="concept-item" markdown="1">

**测试时扩展（test-time scaling）**

在推理阶段投入更多计算，例如重复采样、自一致性投票或验证器引导搜索，以提高至少获得一个正确解的概率。它不仅取决于每次采样的准确率，也取决于底层策略能否覆盖不同且有效的推理轨迹。

</div>
<div class="concept-item" markdown="1">

**入口族（entrance family）**

在Countdown任务的完整解空间中，按照第一次使用的操作数和运算符对有效解进行分组；例如入口 $4\times$ 可包含以 $4\times7$ 或 $4\times9$ 开始的不同后续计算。入口族把早期路径选择离散化，使研究者能够分别测量某类解是否被启动以及启动后是否可完成。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

核心分析对象是Countdown算术任务：输入一组给定数字及目标值，例如 $\{4,5,7,9\}\to24$；输出是一条使用允许算术运算得到目标值的有效计算轨迹。该任务的关键条件是其全部有效解能够被穷举，并可按首个操作数与运算符划分为真实的入口族，因此不会像仅对采样轨迹聚类那样遗漏模型从未访问的有效分支。研究比较两条RLVR训练轨迹——Qwen2.5-3B上的PPO与Qwen2.5-3B-Instruct上的GRPO——并在不同检查点测量三类量：用自由生成的解族覆盖率表征入口访问，用给定最小入口前缀后的条件完成率表征下游执行能力，用 $\mathrm{pass@1}$ 表征单次采样正确率。分析隐含的区分是：若某入口在自由生成中很少出现，但强制提供该入口后模型仍可完成正确解，则损失主要发生在访问阶段，而不是模型已失去后续计算能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathrm{pass@1}$**

每个问题只采样一次时得到正确答案的比例，即单样本准确率。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{S}(x)$**

问题 $x$ 的全部有效解集合；这是依据正文所述“可穷举解空间”给出的便于说明的集合记号，原文节选未显式规定该符号。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{F}(x)$**

问题 $x$ 的入口族集合，每个族由初始操作数与运算符确定；原文节选未显式规定该符号。

</div>
<div class="notation-item" markdown="1">

**$\{4,5,7,9\}\to24$**

Countdown实例：使用给定数字构造算术表达式，使结果等于目标值 $24$。

</div>

</div>

**直接相关的工作**

- **RLVR中的分布锐化与探索坍缩研究（Mayilvahanan et al., 2026；Nguyen et al., 2025；Wu et al., 2025；Yue et al., 2025；Zhao et al., 2025）**: 这些工作指出在策略RLVR可能造成赢家通吃式的模式锐化和解覆盖率下降，但主要从提示级、最终答案级或整体分布层面衡量可达性。本文的区别是把收缩定位到单条推理轨迹内部，并明确分离早期入口访问失败与入口之后的执行失败。
- **语义分支与推理前缀研究（Saha et al., 2026；Macar et al., 2026；Zhang et al., 2025）**: 相关研究通过经验采样轨迹的语义聚类追踪策略分支，或使用推理前缀引导生成；但采样聚类看不到策略完全不访问的有效分支。本文依靠Countdown的可穷举真实解图定义入口族，并以最小入口前缀探测这些低访问乃至近乎消失分支仍具备的条件执行能力。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

可验证奖励强化学习（RLVR）能够提升大语言模型的单次解题准确率，但可能使策略集中于少数解题路径，从而削弱重复采样、自洽性推理和验证器引导搜索等测试时扩展方法的收益。实际问题在于：模型即使仍具备完成多种正确推理的能力，也可能很少主动尝试这些替代路径，导致解题系统的稳健性、候选解多样性和额外计算的利用效率下降。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **聚合式多样性评估与测试时扩展**：重复生成多条推理轨迹，再通过多数投票、自洽性判断或验证器筛选候选答案，以期利用不同解法提高最终准确率。这类方法通常依据最终答案数量或轨迹聚类来衡量解法多样性。
- **奖励或采样机制层面的多样性恢复**：通过奖励塑形、探索奖励、改变 rollout 目标、调整温度或采用提示词与算子引导等方式，鼓励策略生成更多不同轨迹，试图缓解 RLVR 训练后的解空间收缩。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有研究主要统计最终答案支持集或对完整轨迹聚类，无法区分模型是没有进入某个有效解法家族（access 失败），还是进入后无法完成后续计算（execution 失败）。这种混淆会直接影响干预设计：前者需要恢复开局分支选择，后者则需要改善后续推理能力。
- 现有缓解方法多在整体奖励、提示词或解码分布上进行调整，缺少对推理轨迹中具体损失位置的机制定位。因此，即使观察到解法多样性下降，也尚不清楚应在初始决策还是后续算术执行阶段恢复概率质量，导致干预可能牺牲 $pass@1$，或无法真正找回被遗忘的解法。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

未解决的关键空白是：缺少一种能够把可枚举解空间划分为离散入口家族，并分别测量入口访问与后续执行的分析框架；同时也缺少跨训练算法、模型规模和数学基准的证据，说明 RLVR 造成的解空间收缩究竟主要发生在何处，以及这种收缩是否是提升推理准确率的必然代价。本文利用 Countdown 中由首个操作数和运算符定义的入口家族填补这一空白，并进一步检验入口定向干预能否恢复多样性而不降低 $pass@1$。

</div>
<div markdown="1"><span>核心问题</span>

RLVR 训练后解法覆盖率下降，根本原因是策略无法访问原本有效的解法入口，还是已经进入这些入口却无法执行后续计算？如果主要是入口访问受限，那么针对早期分支的干预能否在保持单样本准确率的同时恢复解法覆盖率？

</div>
<div markdown="1"><span>作者直觉</span>

一条推理轨迹的开头决定模型首先选择哪一种解题家族；一旦概率质量在这一阶段集中到少数分支，后续即使仍能正确执行其他分支，也几乎不会主动到达它们。因而，若把一个未被策略选择的合法入口前缀直接提供给模型，并且模型随后仍能完成计算，就能说明能力尚未消失，问题主要是“没有开门”而不是“进门后不会走”。基于这一判断，在早期决策附近恢复或混合较早检查点的参数状态，可能比泛化地调整提示词或温度更有针对性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文的方法不是提出一个新的基础模型，而是建立一套用于定位 RLVR（具有可验证奖励的强化学习）造成的解空间收缩位置的分析与干预框架。输入包括 Countdown 算例、可穷举的全部合法解、不同训练阶段的模型策略，以及模型生成的推理轨迹；方法先把解按首个操作划分为入口族，再分别估计模型进入某入口的概率和进入后完成合法解的能力，最后通过受控入口、似然分段、结构多样性指标和参数插值检验收缩来源并尝试恢复多样性。直观地说，作者把解题过程看成“进门—房间内计算”：先判断模型是否还会选择某类开头，再判断它选定开头后是否仍能完成计算，从而区分“不会走这扇门”和“进门后不会走下去”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造可枚举的解空间与训练检查点

使用精确符号求解器枚举每个可解实例的全部合法算术表达式，并对加法和乘法按交换律、结合律进行规范化；同时过滤公开训练超集与评测集之间的输入—目标语义键，避免数据泄漏。把规范化合法表达式组成的集合记为 $\mathcal{S}(x)$，并将解空间表示为决策树，其中深度为一的分支对应首个算术决策。

<div class="method-step__io" markdown="1">

**输入**：Countdown 实例 $x$，包括目标整数和三或四个输入数；Qwen2.5-3B 的自训练 PPO 检查点，以及 Qwen2.5-3B-Instruct 经 TRL GRPO 训练的公开检查点。<br>
**输出**：每个实例的完整解集合、可行的入口族集合，以及一组从早期到后期的模型策略检查点。入口族 $b$ 由第一个操作数和第一个运算符 $(o_1,\odot_1)$ 决定；另有较粗粒度的首运算符类别划分。

</div>

**直观理解**：作者先把每道 Countdown 题所有可能的正确答案路径列出来，因而能够知道模型到底覆盖了多少种解，而不是只看是否答对。入口族就是“第一步怎么开始”，例如先算 $5-5$ 或先算 $7\times7$。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 测量总体解空间覆盖率

将每条生成轨迹解析为规范化合法解，并计算被至少一条轨迹发现的合法解占全部合法解的比例；再对评测实例求平均，得到语料级覆盖率。

<div class="method-step__io" markdown="1">

**输入**：实例 $x$ 的完整解集合 $\mathcal{S}(x)$，以及模型对该实例生成的 $n$ 条轨迹 $Y_{1:n}$。<br>
**输出**：实例级解空间覆盖率 $\mathrm{Cov}(x,Y_{1:n})$ 和平均覆盖率 $\overline{\mathrm{Cov}}(X)$，用于衡量测试时增加采样是否仍能发现多种有效路径。

</div>

**直观理解**：如果一道题有十种正确解，模型采样后找到了其中四种，覆盖率就是 $0.4$。这个指标与 pass@1 不同：pass@1 只问“第一条是否正确”，覆盖率问“模型能否探索到多少种正确路线”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 分解入口访问与后续执行

将经入口族 $b$ 得到合法解的概率分解为访问概率和条件执行概率。访问概率 $A_t(b\mid x)$ 由自由采样及教师强制前缀的对数概率估计；为测量“已经进入该入口后能否完成”，把生成过程固定到仅包含首个操作的合成前缀 $e_b$，再估计指定入口内的合法完成概率 $E_t^{\mathrm{do}}(b\mid x)$。

<div class="method-step__io" markdown="1">

**输入**：入口族 $b$、问题 $x$、自由采样轨迹，以及由求解器构造的入口前缀 $e_b$。<br>
**输出**：各训练阶段的入口选择分布、入口熵和集中度，以及在相同入口条件下的后续执行能力。该设计还使用中性问题重述、模型生成的失败前缀和互信息检验，排除合成前缀额外泄露后续答案信息的可能。

</div>

**直观理解**：实验不直接把完整思路提示给模型，只替它写到“第一步刚做完”就停下。这样比较的是：模型是否愿意走进这扇门，以及进门以后是否还能自己完成剩余计算。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 跨任务定位并实施入口干预

在 Countdown 中比较训练阶段的入口分布变化、条件执行变化和解叶 turnover；在 GSM8K、MATH500、Minerva Math、OlympiadBench、AMC23 与 AIME24 上，将轨迹划分为首次完整计算之前和之后，比较分段 token 对数似然、首个计算的类别熵和 distinct-trace rate。最后测试表面提示、早期检查点与后期检查点的晚层参数插值，以及多解 SFT 和分阶段 SFT—DPO—RLVR 训练是否保留入口多样性。

<div class="method-step__io" markdown="1">

**输入**：Countdown 中的入口访问—执行结果、标准数学基准上的推理轨迹，以及早期和后期模型参数。<br>
**输出**：入口收缩位置的定位证据、不同训练流程下的多样性对比，以及不牺牲单样本准确率而恢复解空间覆盖的入口定向干预方案。

</div>

**直观理解**：先在能完全列举答案的 Countdown 上找出问题发生在哪一步，再把同样的“首个计算熵下降”现象推广到开放式数学题。最后改变模型靠近后期策略的方式，检验是否能让它保留更多不同的开头。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 实例级与语料级解空间覆盖率

$$
\mathrm{Cov}(x,Y_{1:n})=\frac{\left|\left\{s\in\mathcal{S}(x)\mid s\text{ is the canonicalized solution of some }Y_i\in Y_{1:n}\right\}\right|}{|\mathcal{S}(x)|},\qquad \overline{\mathrm{Cov}}(X)=\frac{1}{|X|}\sum_{x\in X}\mathrm{Cov}(x,Y_{1:n})
$$

**符号说明**

- $x$：一个 Countdown 实例。
- $\mathcal{S}(x)$：实例 $x$ 的全部规范化合法解集合。
- $Y_{1:n}$：模型对 $x$ 生成的 $n$ 条独立轨迹。
- $s$：一个规范化后的合法解。
- $X$：评测实例集合。
- $|\cdot|$：集合的元素数量。

<div class="equation-explanation" markdown="1">

**直观理解**：第一式计算模型采样发现的不同合法解占全部合法解的比例；第二式再对所有实例取平均。它把“答对一次”扩展为“探索了多大的正确解空间”。<br>
**原文位置**：第 3 节“Solution space and coverage”，式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 入口访问与后续执行的概率分解

$$
\pi_{\theta}(\text{solve via }b\mid x)=\underbrace{\pi_{\theta}(B=b\mid x)}_{\text{access}}\cdot\underbrace{\pi_{\theta}(\text{valid completion}\mid x,B=b)}_{\text{execution}}
$$

**符号说明**

- $\pi_{\theta}$：参数为 $\theta$ 的模型策略，即生成轨迹的概率分布。
- $b$：入口族，由初始操作数和运算符确定。
- $x$：当前 Countdown 实例。
- $B=b$：模型选择了入口族 $b$。
- $\pi_{\theta}(B=b\mid x)$：给定问题后访问入口族 $b$ 的概率。
- $\pi_{\theta}(\text{valid completion}\mid x,B=b)$：已经选择入口族 $b$ 后完成合法解的条件概率。

<div class="equation-explanation" markdown="1">

**直观理解**：一条通过入口族 $b$ 的正确解，必须同时满足两件事：先选择这个入口，再把后面的计算做完。若强制给出入口后完成率仍高，说明训练主要删掉了“选择这条路”，而不是删掉了“执行这条路”的能力。<br>
**原文位置**：第 3 节“Entrance families: Decoupling access and execution”，式（2）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文的核心训练对象不是一个新损失函数，而是被分析的 RLVR 策略。PPO 和 GRPO 依据采样轨迹上的可验证奖励更新策略参数；由于策略梯度主要来自实际访问到的轨迹，早期较少被选中的入口会获得更少更新信号，进而形成入口选择概率进一步下降的自强化收缩。作者在附录中给出入口代理目标的理论分析，但所供章节未提供其完整公式，因此不在此臆造。作为对照，作者另行训练使用多解示范的 SFT 模型，并比较 SFT—DPO—RLVR 分阶段流程，以检验准确率提升是否必然要求牺牲入口多样性。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 可穷举解空间与入口族建模**

精确求解器生成规范化解集合 $\mathcal{S}(x)$，并把每个解映射到首个操作数—运算符元组 $b=(o_1,\odot_1)$。入口族固定第一项计算，但不限制后续算术步骤，因此可作为访问阶段与执行阶段之间的干预边界。

> 直观理解：只有在知道所有可能答案路径时，才能判断模型是少探索了，还是根本没有能力完成。入口族提供了一个足够早、又不会规定完整答案的切分点。

**2. 访问—执行解耦测量**

自由生成反映策略自身是否选择入口，合成入口前缀 $e_b$ 的条件生成反映被强制进入入口后的执行能力。作者特别区分 observational execution（自然选择入口后的执行项）与 designated-family completion（固定入口族内的完成概率），避免将入口选择偏差误判为计算能力下降。

> 直观理解：若自由采样几乎不出现某个开头，不能据此断定模型不会做这类题；把开头补上后再让模型继续，才能检验它是否只是“不再主动尝试”。

**3. 早期分布定位与多样性恢复**

对相同参考轨迹按首次完整计算边界切分 token 对数似然，比较早段与后段的分布漂移；对不可枚举任务使用首个计算的类别熵和 distinct-trace rate 作为结构代理。干预包括早期—后期检查点的晚层参数插值，以及使用多解示范的 SFT 或分阶段对齐流程。

> 直观理解：Countdown 能精确数答案，普通数学题不能，所以作者改为观察“第一笔计算有多少种写法”。恢复方法都针对入口分布，而不是简单增加提示词或强行指定完整推理。

**训练与推理**

训练分析覆盖两条 Countdown 流程：其一是遵循 TinyZero 框架、在 Qwen2.5-3B 上进行的 PPO，并保存从早期到后期的 actor 检查点；其二是直接评估 Qwen2.5-3B-Instruct 的公开 GRPO Countdown 系列。推理时首先对各检查点进行自由采样，统计 pass@1、pass@k、解覆盖率和入口分布；随后用求解器生成只到首个运算符结束的 $e_b$，固定入口后继续采样，以测量指定入口内的执行能力。对于普通数学基准，使用多条随机轨迹计算 pass@k、首个计算熵和 distinct-trace rate，并以相同参考轨迹的分段对数似然定位早期分布变化；干预阶段则比较表面提示、晚层参数插值及不同对齐流程的结果。

**复现信息**

Countdown 的 PPO 评测使用温度 $T=0.7$、top-$p=0.9$、最多 256 个 token、每题 320 条独立轨迹和 150 道留出可解题；GRPO 使用相同采样参数、最多 1,024 个 token、每题 320 条轨迹和 135 道去重后的评测题。普通数学基准包括 GSM8K、MATH500、Minerva Math、OlympiadBench、AMC23 和 AIME24；使用每题 64 条采样、$T=0.6$、top-$p=0.95$、最多 16,000 个 token，截断输出按错误计分。覆盖率依赖求解器完整性，作者报告独立枚举器在 500 道留出题上零差异；置信区间采用 bootstrap，但所供章节未给出入口参数插值的具体层数、系数或优化超参数。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Countdown：论文的核心分析任务；给定数字集合和目标值，要求通过算术运算得到目标。其有效解可以穷举，并按首个操作涉及的操作数与运算符划分为离散的入口族，用于分别测量入口访问与后续执行。论文还报告了 150 个问题的跨检查点评估、29 个问题的状态消融、184 个成功轨迹边界实例，以及一个 800 个问题且与训练集不重叠的池；这些子集的具体抽样细节并非全部在所给材料中明确报告。
- Jiayi-Pan/Countdown-Tasks-3to4：公共 GRPO 实验使用的数据集，配套模型为基于 Qwen2.5-3B-Instruct 训练的公开检查点系列。公共数据处理先以随机种子 42 打乱并取前 50,000 个样本，再划分训练集和测试集；由于发布代码无法重建精确划分，论文将全部 50,000 个样本视为训练超集，并按排序后的输入数字与目标值构造语义键，以排除评测重叠。
- 六个数学基准：用于检验早期步骤熵坍缩是否跨任务、跨模型规模复现。论文摘要明确报告使用 7B 和 14B 模型，但所给材料没有完整列出六个基准的名称、规模或划分，因此这些信息记为原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**$pass@1$**

单次采样得到正确答案的概率，反映单样本任务准确率，而不反映有效解族的多样性。 （越高越好；但单独升高不能证明策略仍保留了丰富的候选解。）

</div>
<div class="metric-item" markdown="1">

**solution-space coverage**

自由生成样本覆盖可枚举有效解空间或入口族的程度，主要衡量策略能访问多少不同的有效解分支。 （越高越好；它直接衡量测试时重复采样和搜索所依赖的解空间广度。）

</div>
<div class="metric-item" markdown="1">

**completion rate**

在指定入口前缀或入口族条件下，模型完成有效后续计算并得到正确解的比例，用于测量条件执行能力。 （越高越好；在入口被固定后，它更接近测量模型是否能执行该分支，而不是是否会主动选择该分支。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### PPO 与 GRPO 检查点上的训练过程

<div class="result-value" markdown="1">

RLVR 同时带来准确率上升和解空间收缩。PPO 中 `$pass@1$` 增长超过 50 倍，而整体覆盖率从 0.337 降至 0.111；GRPO 中准确率提升至原来的 3 倍，同时覆盖率下降 43%。在所有检查点都能解决的问题子集上，覆盖率仍然减半，说明收缩并非只由问题难度变化造成。

</div>

该结果支持准确率与候选解广度之间存在明显张力：模型更常生成某些可靠路径，却较少尝试其他仍然有效的路径。因此，重复采样的潜在收益会下降。但这只是总体相关性证据，单凭该结果尚不能定位收缩发生在入口还是后续计算。

<div class="result-source" markdown="1">

来源：Introduction, §4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

under PPO, pass@1 increases more than fiftyfold while overall solution coverage plummets from 0.337 to 0.111.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 入口访问与后续执行的定位实验

<div class="result-value" markdown="1">

训练造成的逐 token 似然变化主要集中在首次算术操作之前：PPO 的变化幅度是后续推理阶段的 16 倍，GRPO 是 11 倍。对低访问率族只提供未被策略选中的最小入口前缀后，PPO 下完成率从 0.018 升至 0.212；同时，匹配入口条件下的下游执行能力在训练中严格提升。

</div>

模型并非普遍失去计算这些解的能力，而是越来越少主动开启这些解族。换言之，问题更像是入口选择被锁定，而不是进入房间后无法完成计算；不过，入口前缀实验仍依赖特定的条件控制，不能直接证明所有未访问分支都同等容易恢复。

<div class="result-source" markdown="1">

来源：Introduction, §5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Supplying only a minimal, unselected entrance prefix restores completion rates in low-access families by over an order of magnitude (0.018 → 0.212 under PPO), while downstream execution capability on matched prefixes strictly improves during training.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 入口定向干预与跨任务复现

<div class="result-value" markdown="1">

表面提示无法恢复多样性，入口定向的后层参数与早期检查点插值使解空间覆盖率提高 37%，且 `$pass@1$` 不下降。早期步骤熵坍缩在 7B 和 14B 模型的六个数学基准上重复出现；但 SFT 对照保留了超过两倍的覆盖率，分阶段 SFT--DPO--RLVR 流程能够保留早期步骤熵。

</div>

这些结果把机制定位转化为干预证据：直接改变开端的模型状态比改变提示词或采样温度更有效，并且可以恢复候选解广度而不牺牲单样本准确率。跨任务结果表明现象并不限于 Countdown，但由于所给材料未列出六个基准的具体结果，不能据此判断各基准上的效果是否一致。

<div class="result-source" markdown="1">

来源：Abstract；Introduction, §6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

late-layer parameter interpolation with early checkpoints increases solution coverage by 37% at no loss in pass@1.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 核心机制证据主要来自可穷举的 Countdown 任务；虽然论文报告六个数学基准上的早期熵坍缩复现，但所给材料未明确列出基准名称、划分和逐基准数值，因此对一般数学推理乃至其他任务的外推仍有限。
- 入口前缀控制依赖求解器构造的族定义和可预测性门控；成功轨迹自然语言条件会泄露计划信息并未通过门控，说明条件执行率对前缀设计敏感。论文还未在所给材料中完整报告所有干预的数值、采样预算与统计不确定性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- PPO on Qwen2.5-3B：核心 RLVR 训练轨迹，用于观察训练过程中 `$pass@1$` 与解空间覆盖率的变化。
- GRPO on Qwen2.5-3B-Instruct：公共开源 GRPO 检查点系列，用于检验入口锁定现象是否依赖某一种 RL 算法或单一训练实现。
- SFT baseline：非 RLVR 的监督微调对照，用于判断早期熵坍缩是否是一般推理优化的必然结果，而不是 RLVR 特有现象。
- 表面提示、强制运算符偏移、温度缩放与入口感知参数干预：这些是恢复多样性的干预对照；前几者测试无需改变模型内部状态的恢复方式，后者直接测试入口定位分析所提出的机制性修复。各方法的完整名称和超参数在所给材料中未全部报告。

**实验想回答的问题**

- RLVR 训练后解空间覆盖率下降，主要源于策略无法进入某些有效入口族，还是源于进入后无法执行后续计算？
- 若多样性损失集中发生在推理开端，针对入口决策的干预能否在不降低 `$pass@1$` 的情况下恢复解空间覆盖率？

**实验实现**

论文在 Countdown 上将有效解穷举并按首个操作划分为入口族；自由生成时用族覆盖率估计 `$access$`，再以求解器指定的入口前缀约束生成、开放后续算术步骤，以估计 `$execution$`。训练过程中对 PPO 和 GRPO 的多个检查点同时跟踪 `$pass@1$` 与覆盖率，并在首次算术操作前后比较逐 token 的似然变化。入口干预包括表面提示、强制运算符变化、温度缩放，以及与早期检查点进行后层参数插值；跨基准实验进一步比较 7B、14B 模型和 SFT、分阶段 SFT--DPO--RLVR 等训练流程。所给材料未完整报告每项实验的采样预算、随机种子、置信区间计算方式和全部训练超参数。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 入口前缀与成功轨迹边界对照 | 在 184 个成功轨迹边界实例上，检查点 50 的“首次运算前”与“首次运算后”完成率分别为 0.145 和 0.914；检查点 275 分别为 0.617 和 0.999。附录表 16 还显示，状态只含数字多重集时完成率为 0.002，加入首个运算符标签后为 0.017，而成功的自然语言脚手架为 0.998，但后者未通过可预测性门控。 | 首次运算后提供了大量计算计划信息，因此完成率显著更高；这支持执行能力在后续阶段仍然存在。数字集合或裸运算符不足以复现成功轨迹，说明实验需要使用求解器构造且不泄露完整计划的入口，才能把入口访问与下游执行分开。 | Appendix C.7, Table 16, Panel B<br><span class="experiment-evidence">Before op 1 275 184 × 64 — 0.617</span> |
| 不同多样性恢复干预的比较 | 方法提示和强制运算符偏移未能恢复覆盖率，温度缩放会降低 `$pass@1$`；相反，与早期检查点进行后层参数插值使覆盖率提高 37%，且 `$pass@1$` 无损。论文未在所给材料中提供各失败干预的完整数值。 | 该消融隔离了“只改变输出表面或采样分布”与“直接恢复早期内部状态”的差别。结果说明入口锁定不是简单增加随机性即可解决的问题；但没有完整数值和统一预算时，不能精确比较每种干预的成本效益。 | Introduction, §6<br><span class="experiment-evidence">While method-prompting and forced operator shifts fail to recover coverage, and temperature scaling degrades pass@1, entrance-aware interventions succeed.</span> |

**定性案例**

- 在 150 个问题的入口族分析中，28 个族在后期 320 次自由采样中完全未出现，但提供最小入口后，在第 275 步的指定族完成率为 0.529；作为对照，仍保持访问率的族完成率为 0.658。该案例表明“未被访问”不等于“不可执行”，但恢复程度随访问尾部而变化：在更大、包含 276 个零访问族单元的 800 问题池中，平均入口供给完成率仅为 0.087，说明深层低概率分支并非都能同样容易重启。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper analyzes how RLVR changes LLM reasoning-solution diversity and proposes interventions to preserve coverage, directly concerning both reasoning optimization and RL-based alignment.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`97a28e8e14b5822f09837e94413859bdfa03e5c4124341001ab21eff44ef2ff4`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
