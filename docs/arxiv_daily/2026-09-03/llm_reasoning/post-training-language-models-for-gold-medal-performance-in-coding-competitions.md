---
title: "[论文解读] Post-Training Language Models for Gold-Medal Performance in Coding Competitions"
description: "[arXiv 2609.02849][LLM Reasoning] 本文旨在明确训练数据、监督微调、强化学习、模型规模与测试时计算各自如何推动大语言模型达到信息学竞赛金牌水平，并据此构建可在真实竞赛约束下运行的完整系统。"
arxiv_id: "2609.02849"
announcement_date: "2026-09-03"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-03T04:29:49.990133+00:00"
source_sha256: "de080edbe76aca6966341d9e83e84d92221660051b6bd11cf0e329417213e287"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "LLM 其他"
  - "竞赛编程"
  - "大语言模型"
  - "代码推理"
  - "合成推理数据"
  - "监督微调"
  - "强化学习"
  - "测试时计算"
  - "迭代代码修正"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.02849</p>

# Post-Training Language Models for Gold-Medal Performance in Coding Competitions

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-03</span>
<span><strong>作者</strong> Aleksander Ficek, Sean Narenthiran, Mehrzad Samadi, Somshubra Majumdar, Boris Ginsburg</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.02849v1) · [PDF 下载](https://arxiv.org/pdf/2609.02849v1) · **关键词** 竞赛编程, 大语言模型, 代码推理, 合成推理数据, 监督微调, 强化学习, 测试时计算, 迭代代码修正<br>
**代码**: [https://github.com/NVIDIA-NeMo/Skills](https://github.com/NVIDIA-NeMo/Skills)

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

本文旨在明确训练数据、监督微调、强化学习、模型规模与测试时计算各自如何推动大语言模型达到信息学竞赛金牌水平，并据此构建可在真实竞赛约束下运行的完整系统。

**不用术语来说**：信息学竞赛不仅要求模型写出能运行的程序，还要求它针对陌生题目设计新算法、处理复杂约束，并让代码通过隐藏测试。已有系统虽已取得金牌级成绩，但往往不公开，或同时改变模型、数据、训练和推理策略，因此难以判断成绩究竟来自哪里，也难以形成一套可复现、可诊断的开发方案。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出端到端竞赛编程专门化管线：从约 2.2 万道整理后的题目出发生成合成推理轨迹，再实施监督微调与可执行奖励驱动的强化学习，并通过排除和去重评测题降低训练数据泄漏风险。
- 提出 GenCorrect 闭环推理策略：在有限提交预算内生成多样化方案，利用评测器或先前提交的反馈迭代修正，并结合不同规模模型的实验，分析后训练、模型规模和测试时计算对竞赛成绩的相对作用。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型（LLM）代码推理与竞赛编程研究。竞赛编程不同于只要求生成可运行代码的常规代码基准：模型必须从题意和约束条件中设计新算法，完成实现，并使程序在隐藏测试、时间限制和内存限制下获得分数。国际信息学奥林匹克竞赛（IOI）等比赛因此同时检验算法推理、代码生成、调试以及有限提交预算下的解题策略；本文研究如何通过后训练和推理时计算，将通用语言模型专门化为竞赛编程系统。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**监督微调（SFT）**

SFT使用带有目标答案或推理过程的示例继续训练模型，使模型学习特定任务的输入—输出模式。本文中，目标是让模型更稳定地产生竞赛题的算法推理和代码。

</div>
<div class="concept-item" markdown="1">

**强化学习（RL）与可验证奖励**

RL通过奖励或惩罚调整模型生成行为，而不是只模仿固定答案。竞赛代码可以交给编译器和测试器执行，因此程序是否通过测试、获得多少分能够作为相对客观的奖励信号。

</div>
<div class="concept-item" markdown="1">

**测试时计算与反馈式迭代**

测试时计算是在模型部署或评测阶段额外生成、检查和筛选多个候选解，而不是只依赖一次生成。本文的GenCorrect利用提交结果等执行反馈，反复生成和改进方案，但必须遵守比赛的时间与提交次数限制。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定竞赛编程题目、输入输出说明、约束条件以及可用的编程环境，系统需要生成一个解决该题的程序，并在隐藏测试上取得尽可能高的分数。与普通代码生成不同，IOI类任务通常允许部分得分，系统可提交多个候选程序；每次提交会产生编译、测试通过情况或分数等反馈，系统需要在官方时间限制、互联网限制和提交预算下决定如何生成、评估、修改和选择解答。本文首先在排除评测题目的训练数据上进行专门化，再比较单次生成和多轮反馈式推理；论文还将通用模型结果与IOI 2025开发评测及IOI 2026的前瞻性、非官方评测区分开来。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D$**

经过筛选和去重的竞赛编程题目数据集；论文说明其规模为22,000道题，并排除了评测题目。

</div>
<div class="notation-item" markdown="1">

**$T$**

由教师模型生成的合成推理轨迹集合，用于SFT训练；论文分别为紧凑模型生成约120万条、较大模型生成477,642条。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{SFT}$**

监督微调阶段，用合成推理轨迹和竞赛题数据训练模型。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{RL}$**

强化学习阶段，利用可执行代码产生的奖励进一步优化紧凑模型。

</div>

</div>

**直接相关的工作**

- **AlphaCode与AlphaCode 2**: 这些工作将竞赛编程视为大规模候选代码生成与筛选问题，结合领域训练、采样、过滤、行为聚类和重排序。本文沿用生成—评估思想，但进一步把大规模题目整理、合成推理数据、SFT、可执行奖励RL以及反馈式测试时迭代连接为端到端流程。
- **OpenCodeReasoning与OpenCodeReasoning-II**: 相关工作表明，合成推理轨迹、自我批评和迭代改进能够提升竞赛编程能力。本文在此基础上研究更完整的后训练组合，并强调使用执行结果而非仅依赖模型自身判断的反馈式修正。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

IOI、ICPC 等竞赛构成了高难度、接近真实约束的程序推理场景：系统必须在规定时间、内存和提交次数内完成算法设计与正确实现，而一次生成常会因算法边界、复杂度或代码细节错误而丢分。研究者因此需要一种既能提高单次解题能力、又能利用有限反馈持续纠错的竞赛级系统。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **模型专门化与后训练**：利用竞赛题及其解题过程对基础语言模型进行监督微调，使模型学习算法推导和代码实现；部分系统进一步使用基于程序执行结果的强化学习，让通过测试的输出获得更高奖励。
- **扩大模型规模与测试时计算**：前者依靠更大模型容量提升复杂推理能力；后者在同一道题上生成多个候选答案，进行评估、选择或修正，以计算成本换取更高的最终通过率。本文所面对的已有金牌级系统通常综合采用这些手段。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 已有高水平系统常为闭源系统或依赖专用模型，训练数据、训练过程和推理流程缺乏充分透明度，导致其结果难以复现，也难以判断方法能否迁移到其他开放模型。
- 已有工作往往同时改变训练数据、后训练方式、模型规模和推理计算量，使各组件的独立贡献难以隔离；其后果是无法可靠回答应优先投入数据、强化学习、更大模型，还是更多提交与反馈迭代。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一套公开描述、端到端且经过组件化分析的竞赛编程方案，能够在严格排除评测题污染的前提下，系统比较合成数据、监督微调、强化学习、模型规模和反馈式测试时计算，并验证这些设计在真实竞赛时间、网络和提交限制下是否仍然有效。

</div>
<div markdown="1"><span>核心问题</span>

如何将数据整理与合成、监督微调、可执行奖励强化学习及有限预算下的迭代纠错组织成一个完整系统，并量化各环节对单次解题能力和最终竞赛成绩的作用，从而使模型达到乃至超过 IOI 金牌级表现？

</div>
<div markdown="1"><span>作者直觉</span>

竞赛程序失败通常不是单一原因造成的：模型既可能不会设计核心算法，也可能已找到正确思路却在边界条件或实现上出错。监督微调主要补充稳定的解题模式，强化学习用真实执行结果校准“什么代码才算正确”，而 GenCorrect 则把一次性作答变成“提出方案—接受反馈—定位错误—重新生成”的闭环；三者分别针对知识与推理、结果导向优化和临场纠错，因而可能形成互补。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法是一条从竞赛题数据到受反馈驱动的多轮解题系统的端到端专门化流水线。首先，作者整理约 $22{,}000$ 道竞赛题，并将题面、约束、测试、辅助文件和参考解封装成可执行环境；随后由 DeepSeek-V4-Flash 生成推理与自我改进轨迹，对 Nano 和 Ultra 模型进行监督微调；仅对 Nano 进一步使用可执行判题奖励开展 GRPO 强化学习。推理阶段，两种模型均使用 GenCorrect：每轮并行生成至多 $200$ 个候选程序，以行为相似度聚类，从中选出至多 $10$ 个代表提交判题，再把子任务反馈和互补参考解送入下一轮。

技术上，训练阶段解决“如何让模型掌握竞赛算法及迭代修正行为”，测试时计算则解决“单次生成不稳定、有限提交次数应如何分配”的问题。直观地说，系统先让模型大量学习高手的完整解题过程，再通过真实编译执行训练 Nano 区分可通过与不可通过的程序；正式答题时，它不押注一个答案，而是先广泛提出方案、保留差异最大的代表、实际试跑，再针对尚未通过的子任务继续修改。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 竞赛题整理与可执行环境构建

自动将每道题封装为包含题面、约束、测试用例、辅助文件和参考程序的可执行判题环境，并用参考解及生成解检查判定结果的一致性；删除不可靠环境，同时排除 IOI 2025、ICPC 2025 和 LiveCodeBench Pro，并针对这些评测集进行去重。

<div class="method-step__io" markdown="1">

**输入**：来自 $16$ 个地区性或国际竞赛系列、在线编程平台以及过去约二十年的原始题目、测试数据、辅助文件和参考解。<br>
**输出**：约 $22{,}000$ 道经筛选的训练题及其可执行环境，其中适合强化学习的部分进一步形成 $3{,}219$ 道题的数据集。

</div>

**直观理解**：这一步相当于把来源杂乱的题目改造成统一、可自动验收的练习册。严格排除目标评测题并去重，是为了避免模型因见过测试题而获得虚假的高分。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 合成推理轨迹与监督微调

教师模型为 Nano 生成 $1{,}200{,}000$ 条、为 Ultra 生成 $477{,}642$ 条推理轨迹，困难题获得更多采样；训练混合物还包括教师读取旧解并给出改进解的自我改进轨迹。Nano 训练 $3$ 个 epoch，Ultra 从 RLVR-teacher 检查点出发训练 $1$ 个 epoch。

<div class="method-step__io" markdown="1">

**输入**：整理后的竞赛题、基础模型 Nemotron-3-Nano-30B-A3B 与 NVIDIA-Nemotron-3-Ultra-550B-A55B，以及教师模型 DeepSeek-V4-Flash。<br>
**输出**：具备竞赛题分析、C++ 解法生成和根据旧解进行修正能力的 Nano-CC 与 Ultra-CC 监督微调模型。

</div>

**直观理解**：普通轨迹教模型从题目走到答案，自我改进轨迹则教它看懂一个已有方案为何不够好以及应如何修改。后者使训练时的行为与 GenCorrect 推理阶段的反复修正更加一致。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于可执行正确性的强化学习

使用 GRPO；每步对 $64$ 个提示各采样 $16$ 条 rollout，共 $1{,}024$ 个 C++17 程序，并进行编译和执行。程序获得满分时终局奖励为 $1$，否则为 $0$，随后优化无参考策略 KL 惩罚的逐 token 截断策略梯度目标，并按留出验证集表现选择检查点。

<div class="method-step__io" markdown="1">

**输入**：完成监督微调的 Nano-CC，以及按母题划分的 $2{,}847$ 道训练题和 $372$ 道验证题；同一题的不同子任务不会跨越训练集与验证集。<br>
**输出**：经执行反馈进一步优化的 Nemotron-3-Nano-CC；Ultra-CC 不经过这一强化学习阶段。

</div>

**直观理解**：监督微调主要模仿教师，而强化学习直接依据程序能否完全通过测试来调整 Nano。奖励虽然只有“全对或不全对”两档，但它与竞赛最终判定直接对齐。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### GenCorrect 多轮生成、筛选、执行与修正

每轮并行生成至多 $200$ 个候选并本地编译，过滤无效输出后，以局部质量启发式 $Q(c)$ 初始化中心，并用最远点规则选择至多 $K=10$ 个多样化中心；候选归入最相似的中心后，每簇选择 $Q(c)$ 最高者提交。系统累计各子任务历史最佳分数，并选择三个互补参考解，以保住已通过部分、针对未解决缺口并维持方案多样性，然后条件化生成下一轮。

<div class="method-step__io" markdown="1">

**输入**：一道待解题目、训练后的 Nano-CC 或 Ultra-CC，以及前几轮提交的程序和判题反馈。<br>
**输出**：在 IOI 中经过 $5$ 轮、每轮 $10$ 次且总计不超过官方每题 $50$ 次提交限制的最终解答集合；在 ICPC 中则持续迭代到题目通过或性能停滞。

</div>

**直观理解**：它像一个受提交次数约束的解题团队：先提出很多不同想法，但只让最有代表性的少数方案参加正式测试。判题结果告诉下一轮哪些子任务已经解决、哪些仍有漏洞，从而避免反复尝试近乎相同的程序。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 最远点多样性中心选择

$$
c_{\mathrm{next}}\in\arg\max_{c\notin C}\min_{z\in C}\left[1-\operatorname{sim}(c,z)\right]
$$

**符号说明**

- $c_{\mathrm{next}}$：下一名被加入中心集合的候选程序。
- $c$：尚未进入中心集合的候选程序。
- $C$：当前已选择的候选中心集合，最终至多包含十个中心。
- $z$：中心集合中的一个已有中心程序。
- $\operatorname{sim}(c,z)$：候选程序 $c$ 与中心程序 $z$ 的相似度分数。

<div class="equation-explanation" markdown="1">

**直观理解**：对每个尚未入选的候选，先看它与现有中心中最相近者仍有多大距离，再选取这一最小距离最大的候选。这样新增中心会尽量代表尚未覆盖的解法类型，而不是重复已有程序；随后所有候选被分配到最相似的中心，每个簇再以 $Q(c)$ 选出质量最高的代表。<br>
**原文位置**：第 3.4 节，公式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 跨轮次子任务最佳分数累计

$$
A_r(t)=\max\left(A_{r-1}(t),\max_{c\in S_r}s_t(c)\right),\qquad A_0(t)=0
$$

**符号说明**

- $A_r(t)$：完成第 $r$ 轮后，子任务 $t$ 在全部历史提交中达到的最高分。
- $A_{r-1}(t)$：进入第 $r$ 轮之前，子任务 $t$ 已累计的历史最高分。
- $S_r$：第 $r$ 轮实际提交给评测器的候选程序集合。
- $s_t(c)$：候选程序 $c$ 在子任务 $t$ 上获得的分数。
- $r$：GenCorrect 的轮次编号。
- $t$：IOI 题目中的一个子任务。

<div class="equation-explanation" markdown="1">

**直观理解**：系统把上一轮之前的历史最好成绩与本轮所有提交的最好成绩取最大值，因此已取得的子任务进展不会因后续某个较差程序而被覆盖。所得向量 $A_r$ 会作为下一轮提示的一部分，让模型明确哪些约束范围已经解决、哪些仍需改进。<br>
**原文位置**：第 3.4 节，公式 (2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：SFT 阶段通过教师生成的推理与程序轨迹进行标准序列监督，使模型学习在给定题目以及可选旧解的条件下生成改进后的完整解答；原文节选未给出其显式损失公式。Nano 的 RL 阶段把每个生成程序编译并执行，满分解获得奖励 $1$，其他解获得 $0$，再使用 GRPO 的逐 token 截断策略梯度提升相对高奖励 rollout 的概率；该目标不加入参考策略 KL 惩罚。最终模型检查点依据 $372$ 道留出验证题的表现选择，因而训练信号与“程序实际完全通过测试”直接对齐，但二元奖励不会显式区分部分正确方案之间的优劣。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 可执行竞赛环境与数据隔离**

每个环境统一提供题面、约束、测试、辅助文件和参考解，并要求参考程序与生成程序的判定保持一致；训练语料显式排除 IOI 2025、ICPC 2025 和 LiveCodeBench Pro，IOI 2026 则是在题目公开前运行的前瞻评测。

> 直观理解：可执行环境既是强化学习奖励和测试时反馈的来源，也是检查数据是否可靠的工具。数据隔离则确保评测主要反映迁移和推理能力，而不是记忆目标题目。

**2. SFT 与 GRPO 的分层后训练**

SFT 使用教师生成的完整推理轨迹和自我改进轨迹建立基础解题能力；Nano 随后采用 GRPO，以同一提示下的一组 rollout 作相对比较，并通过编译执行所得的二元终局奖励优化逐 token 截断策略梯度。Ultra 只进行 SFT，因此两种模型的训练路线并不相同。

> 直观理解：SFT 先告诉模型“好的解题过程长什么样”，RL 再用真实判题结果纠正只会模仿却不能通过测试的问题。只给 Nano 加 RL 也意味着不能把 Nano 与 Ultra 的差异简单归因于模型规模。

**3. GenCorrect 的多样性选择与反馈记忆**

GenCorrect 不直接提交所有采样结果，而是根据候选程序间的相似度进行行为聚类，再结合不读取当前轮判题分数的局部质量函数 $Q(c)$ 选取代表；提交后用累计向量 $A_r$ 保存各子任务迄今最高得分，并将其与三个功能互补的历史参考解共同用于后续生成。

> 直观理解：聚类减少把有限提交浪费在重复思路上的风险，累计反馈则防止后续修改忘掉已经通过的子任务。三个互补参考解不是只追随当前总分最高的单一程序，而是同时考虑保守、补缺和探索。

**训练与推理**

训练顺序为：构建并验证可执行题目环境；用教师模型按难度分配采样预算，生成普通推理轨迹和读取旧解后的自我改进轨迹；分别对 Nano 与 Ultra 进行 SFT；再仅对 Nano 使用 $2{,}847$ 道训练题开展执行驱动的 GRPO，并在按母题隔离的 $372$ 道验证题上选模。SFT 中 Nano 使用 $3$ 个 epoch，Ultra 使用 $1$ 个 epoch；Ultra 从 RLVR-teacher 检查点初始化，因此其最终能力也不能解释为仅来自本论文的 SFT。

推理时，第一轮只输入题面并生成候选；后续轮次额外输入历史解、评测反馈、累计子任务分数向量 $A_r$ 和三个互补参考解。每轮先生成并本地编译，随后在未观察本轮正式得分的前提下完成过滤、聚类和代表选择，再提交至评测器；这种次序避免用同一批提交的隐藏反馈反向挑选该批答案。IOI 使用固定的五轮方案以严格匹配每题 $50$ 次提交上限，ICPC 因只有通过或未通过的二元反馈，则在成功或表现停滞时终止。

**复现信息**

公平解释结果所需的关键配置包括：Nano 和 Ultra 的 SFT 全局批量均为 $64$，最长打包序列为 $262\mathrm{K}$ tokens；Nano 的学习率为 $5\times10^{-5}$ 且使用常数调度，Ultra 的峰值学习率为 $1.5\times10^{-5}$、使用余弦调度和 $0.1$ warmup 比例。RL 每步处理 $64$ 个提示，每个提示以温度 $1.0$ 生成 $16$ 条 rollout，共 $1{,}024$ 条，并统一生成、编译和执行 C++17 程序。GenCorrect 每轮至多生成 $200$ 个候选，但正式评测只提交至多 $10$ 个代表；$Q(c)$ 是不使用正式得分的本地启发式，完整过滤、排序、平局处理、跨轮保留规则和提示模板位于附录 C，当前节选未给出其具体定义。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- IOI 2025：国际信息学奥林匹克竞赛题集，满分为 600 分；用于测试带有子任务部分得分的复杂算法编程能力，并报告单样本 Score@1、并行采样 Score@200 及 GenCorrect 多轮结果。所有评测题均从 SFT 和 RL 数据中排除并去重。
- ICPC 2025：包含 12 道题的国际大学生程序设计竞赛题集；用于测试在整题通过标准下解决多道竞赛题的能力，报告 Pass@1 以及 GenCorrect 后平均解出的题数。评测题同样未用于训练。
- LiveCodeBench Pro（LCB Pro）：独立的代码生成评测集；用于检验方法是否超越 IOI、ICPC 的竞赛分布而迁移到另一组未见编程题，报告 Pass@1。原文未明确报告其题目规模、训练验证测试划分细节。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**IOI Score@1 与 Score@200**

Score@1 是单次生成解在 IOI 子任务和题目上的得分；Score@200 将生成结果分成独立运行组，对每个子任务保留该组中的最高分，再汇总并对运行组取平均。Score@1 反映一次生成能力，Score@200 反映并行候选搜索带来的上限。 （越高越好；IOI 结果可表示为 600 分原始分数或归一化百分比。）

</div>
<div class="metric-item" markdown="1">

**ICPC Pass@1**

对每道题仅采样一个解，统计被正确解决的题目比例；ICPC 主表中该比例以 12 道题为分母。GenCorrect 图中还报告平均解出的题目数。 （越高越好，因为它表示一次尝试能够通过完整题目测试的比例。）

</div>
<div class="metric-item" markdown="1">

**LCB Pro Pass@1**

单个采样解成功解决 LCB Pro 题目的比例，用于评估跨评测集的代码生成与算法解决能力。 （越高越好，表示更多独立题目被一次生成的程序正确解决。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 后训练模型在三类基准上的单样本表现（IOI 2025、ICPC 2025、LCB Pro）

<div class="result-value" markdown="1">

Nano-CC 相比基础 Nano 模型，IOI Score@1 从 21.7% 提升到 48.5%，ICPC Pass@1 从 16.9% 提升到 51.0%，LCB Pro Pass@1 从 17.6% 提升到 71.6%。Ultra-CC 相比基础 Ultra 模型分别从 45.5%、54.0%、72.6% 提升到 50.7%、57.4%、74.5%。在作者报告的模型中，Ultra-CC 三项均高于 Nano-CC；Nano-CC 在 LCB Pro 上也超过 gpt-oss-120b、Qwen3.6-35B-A3B、Nemotron-Cascade-2-30B-A3B 和 DeepSeek-V4-Flash。

</div>

该结果说明后训练不仅改善了训练目标附近的 IOI 表现，也迁移到 ICPC 和 LCB Pro。Ultra-CC 的提升幅度较小但绝对成绩更高，符合其基础模型更强的特点。它支持“后训练有效”和“强基础模型加少量 SFT 有竞争力”，但不能单独证明某个具体 SFT 数据组成或训练算法必然优于所有未列出的系统。

<div class="result-source" markdown="1">

来源：Section 4.2 Main Results；Figure 5；Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On IOI 2025, Nemotron-3-Nano-CC improves over its base model from 130 (21.7%) to 291 (48.5%) at Score@1 and from 272 to 461 at Score@200.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### GenCorrect 的多轮测试时计算（IOI 2025）

<div class="result-value" markdown="1">

Nano-CC 的 IOI 平均分从第一轮 360.6 提升到第五轮 468.2，增加 107.6 分；Ultra-CC 从 343.9 提升到 502.0，增加 158.1 分。Ultra-CC 在第五轮比 Nano-CC 高 33.8 分，并在第三轮后超过 IOI 2025 金牌线，而 Nano-CC 在第四轮后超过。

</div>

这表明反馈评估和迭代修正比单纯增加一次采样预算更能利用候选解，且 Ultra-CC 更能从测试时计算中获益。第一轮 Nano-CC 较高但后续被 Ultra-CC 反超，说明单样本或早期候选质量并不完全决定多轮搜索效果。该结果证明的是本文设置下的测试时增益，不等于对所有题集或无限计算预算都能持续线性提升。

<div class="result-source" markdown="1">

来源：Section 4.5 Effect of Test-Time Compute；Figure 8(a)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Nano-CC’s mean IOI 2025 score increases from 360.6 after the first round to 468.2 after five rounds, a gain of 107.6 points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 前瞻性 IOI 2026 竞赛评测

<div class="result-value" markdown="1">

作者摘要报告，面向竞赛专门构建的 Ultra-CC 系统在与人类选手相同的时间、联网和提交约束下取得 535.4/600，超过金牌线 361.12 以及最高人类得分 498.27。

</div>

这是最直接的外部验证：系统在新的 IOI 题集和受限竞赛环境中超过最高人类得分，说明方法不仅在离线基准上有效。由于本摘录的实验章节没有给出 IOI 2026 的完整运行次数、逐题得分、方差或对照系统，不能据此判断优势的统计稳定性，也不能把一次竞赛结果推广为所有编程任务上的人类替代能力。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under the same time, internet-access, and submission constraints as human contestants, it scores 535.4 out of 600, exceeding both the gold threshold of 361.12 and the top human score of 498.27.

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

- Nemotron-3-Nano-30B-A3B 与 Nemotron-3-Ultra-550B-A55B 基础模型：分别是 Nano-CC 和 Ultra-CC 的后训练前版本，用于隔离后训练带来的增益。
- Nemotron-Cascade-2-30B-A3B：与 Nano-CC 活跃参数规模相近的外部模型，用于比较同等计算规模下的竞争力。
- gpt-oss-120b、Qwen3.6-35B-A3B：代表其他大语言模型，其中前者在 LCB Pro 上表现较强，后者提供不同模型规模与训练路线的比较。
- DeepSeek-V4-Flash、DeepSeek-V4-Pro、GLM-5.2：高性能外部模型，用于检验 Nano-CC 和 Ultra-CC 是否达到当前评测模型的绝对性能水平；原文将其作为一组比较模型，但本文摘录未提供各模型的训练细节。

**实验想回答的问题**

- 后训练流水线中的监督微调（SFT）和强化学习（RL）分别能否提升模型在 IOI、ICPC 与 LCB Pro 上的编程表现，且提升是否能迁移到未见过的竞赛题？
- 并行采样与反馈驱动的测试时计算策略 GenCorrect 能否进一步提升模型表现，使其达到或超过竞赛奖牌分数线及顶尖人类选手水平？

**实验实现**

评测题均被排除并去重于 SFT 和 RL 数据。IOI 的 Score@k 通过独立运行组计算：每组在每个子任务上取最高分，汇总所有子任务和题目，再对运行组求平均；Score@1 使用单个样本，Score@200 使用 200 个并行样本。最终 IOI 与 ICPC 结果平均 1,000 次运行，中间训练检查点平均 50 次运行，Score@200 平均 5 次运行，LCB Pro 平均 8 次运行。检查点只依据留出的验证集选择。GenCorrect 每轮生成并评估候选解，再利用评测器反馈迭代修正，并将每轮 200 次生成集中为 10 次提交。竞赛结果均由本文评测框架重新获得，而非直接复制模型报告。IOI 与 ICPC 的最终竞赛结果还在与人类选手相同的时间、联网和提交限制下进行；原文摘录未明确报告各基线的统一提示词、解码参数及硬件配置。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 监督微调（SFT）消融与训练进程 | Nano-CC 经过三轮 SFT 后，IOI Score@1 从 21.7% 升至 47.3%，ICPC Pass@1 从 16.9% 升至 46.7%，LCB Pro Pass@1 从 17.6% 升至 70.7%；大部分增益发生在第一轮，第三轮开始趋于饱和。Ultra-CC 仅使用一个 SFT epoch 后，IOI、ICPC、LCB Pro 分别从 45.5%、54.0%、72.6% 升至 50.7%、57.4%、74.5%。 | 该对比把基础模型与逐步 SFT 检查点比较，主要测试监督示范数据是否是性能提升的核心来源，以及更强初始化是否降低继续训练的边际收益。结果支持 SFT 的关键作用，也显示 Nano-CC 的大幅提升不能简单归因于 RL。由于 Nano 与 Ultra 的规模、训练预算和 SFT 设置不同，这不是严格的同规模因果比较。 | Section 4.3 Effect of Supervised Fine-Tuning；Figure 6<br><span class="experiment-evidence">Figure 6 shows that SFT produces most of Nano-CC’s improvement.</span> |
| 强化学习（RL）及其初始化点消融 | 从第三轮 SFT 检查点开始进行 RL 后，Nano-CC 的 IOI Score@1 从 46.7% 升至 48.5%，ICPC Pass@1 从 47.3% 升至 51.0%，LCB Pro Pass@1 从 70.7% 升至 71.6%。从基础 Nano 直接开始 RL，IOI Score@1 在 30 步后从 21.7% 升至 24.9%；从第一、二、三轮 SFT 检查点初始化时，30 步后分别达到 43.0%、47.1%、48.7%。 | 该消融分别测试 RL 是否独立有效，以及 RL 是否依赖高质量 SFT 初始化。RL 从基础模型出发确实有可测增益，但远小于 SFT；从更晚的 SFT 检查点开始通常得到更高结果，说明 RL 更像是在已有能力前沿上进行局部优化，而不是替代监督学习。作者还指出二元执行奖励和长达 255K token 的轨迹造成稀疏奖励与长期信用分配困难，这为 RL 增益有限提供了机制解释。 | Section 4.4 Effect of Reinforcement Learning；Figure 7(b)<br><span class="experiment-evidence">Without SFT, RL improves IOI 2025 Score@1 from 21.7% to 24.9% after 30 steps, demonstrating that executable-reward RL can produce measurable gains directly from the base model.</span> |

**定性案例**

- IOI 与 ICPC 的 GenCorrect 曲线呈现不同的反馈利用模式：Ultra-CC 在 IOI 五轮后从 343.9 分升至 502.0 分，而在 ICPC 中从 9.0 道题升至 9.6 道题后基本维持不变。作者将其解释为 IOI 的子任务级分数提供了更细粒度反馈，ICPC 的二元通过反馈则较快失去继续修正所需的信息；这说明 GenCorrect 的效果不仅取决于生成模型，也取决于评测器反馈的细致程度。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该工作通过监督微调、强化学习和测试时迭代修正确立大语言模型在竞赛编程中的代码与复杂推理能力。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`de080edbe76aca6966341d9e83e84d92221660051b6bd11cf0e329417213e287`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
