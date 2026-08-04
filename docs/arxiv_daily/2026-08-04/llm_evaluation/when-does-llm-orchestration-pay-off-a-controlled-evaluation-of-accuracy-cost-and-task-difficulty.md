---
title: "[论文解读] When Does LLM Orchestration Pay Off? A Controlled Evaluation of Accuracy, Cost, and Task Difficulty"
description: "[arXiv 2608.00685][LLM 评测] 本文通过统一模型、解码、题目、评分规则与提示优化预算，检验大语言模型编排相对单次调用究竟能否以合理的推理资源成本换取更高准确率，以及这种收益是否随题目难度或底座模型而变化。"
arxiv_id: "2608.00685"
announcement_date: "2026-08-04"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:57:45.347143+00:00"
source_sha256: "59a1bcb0eecd5a0b2df02f15baa060cf40fbd06b4a61e327d49950368d5e02fd"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "大语言模型编排"
  - "推理时计算"
  - "Self-Refine"
  - "Best-of-N"
  - "多智能体辩论"
  - "思维链"
  - "准确率—成本权衡"
  - "任务难度"
  - "底层模型异质性"
  - "受控评估"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.00685</p>

# When Does LLM Orchestration Pay Off? A Controlled Evaluation of Accuracy, Cost, and Task Difficulty

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Nicolas Leins, Nico Pelleriti, Jana Gonnermann-Müller, Sebastian Pokutta</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Zuse Institute Berlin & TU Berlin, Berlin, Germany；Zuse Institute Berlin & Weizenbaum Institute Berlin, Berlin, Germany</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.00685v1) · [PDF 下载](https://arxiv.org/pdf/2608.00685v1) · **关键词** 大语言模型编排, 推理时计算, Self-Refine, Best-of-N, 多智能体辩论, 思维链, 准确率—成本权衡, 任务难度, 底层模型异质性, 受控评估<br>


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

本文通过统一模型、解码、题目、评分规则与提示优化预算，检验大语言模型编排相对单次调用究竟能否以合理的推理资源成本换取更高准确率，以及这种收益是否随题目难度或底座模型而变化。

**不用术语来说**：让大语言模型多生成几个答案、反复检查修改，或让多个模型实例互相讨论，有时能提高答题正确率，但也会消耗更多调用次数、令牌和时间。过去的比较往往同时更换模型、提示词和计算预算，因此即使复杂流程表现更好，也难以判断收益究竟来自编排结构，还是来自额外调优与计算。本文要解决的问题是：在尽量公平的条件下，这些复杂流程带来的准确率提升是否值得其额外成本。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 建立难度分层的完全配对评估：在五个大语言模型和三个推理领域中，将 Self-Refine、Best-of-$N$ 与 Debate 同任务直答、思维链单次调用进行比较，并固定底座模型、解码设置、测试题目和评分规则，同时用 GEPA 给予各方法相同的最大优化预算。
- 把“难题更容易做错”与“难题更值得采用编排”区分开来，同时联合考察准确率和推理资源；由此判断固定编排的相对收益究竟主要受题目难度影响，还是更依赖具体的底座模型与工作流组合。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型的推理时计算与编排评估研究。模型参数保持不变时，可以通过提示模型写出中间推理、并行生成多个候选答案、反复批评与修订，或让多个模型实例交换意见来增加推理时计算；这些做法可能提高正确率，也会增加模型调用次数、令牌消耗和延迟。论文关注的不是设计新的编排算法，而是在统一条件下比较三种固定的多调用编排与两种单调用基线，并同时考察正确率、实际资源消耗、题目难度及底层模型差异。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**推理时编排（inference-time orchestration）**

在不更新模型权重的情况下，用预先规定的多次调用流程组织模型完成任务。本文覆盖并行候选选择、迭代反馈修订和多实例辩论三类流程。

</div>
<div class="concept-item" markdown="1">

**思维链（Chain-of-Thought, CoT）**

通过提示要求模型在一次生成中给出中间推理步骤，再产生最终答案。本文把优化后的 CoT 作为单调用推理基线，以判断多调用结构是否带来超出一次结构化推理的收益。

</div>
<div class="concept-item" markdown="1">

**自然执行评估（natural-execution evaluation）**

固定每种工作流自身的执行规则，让其自然运行，并测量由此产生的调用与令牌消耗。它回答的是固定工作流所得正确率是否值得其实际成本，而不是在完全相同的推理令牌预算下比较方法。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是来自竞技编程、国际象棋谜题和数学三个领域、带有人类来源难度估计的同一组分层测试题，以及五种作为底层推理引擎的大语言模型。对每个“题目—底层模型”组合，系统运行任务直答、单调用 CoT、Self-Refine、Best-of-$N$ 或 Debate，并依据各领域统一的评分规则输出最终答案是否正确，同时记录完整工作流的令牌数与调用量。比较采用完全配对设置：各方法使用相同题目、底层模型、解码设置、停止规则和评分规则；其提示或协议均由 GEPA 在相同的最大离线优化预算下优化。这里的推理资源不强行匹配，而是按各固定流程的自然执行结果计量；题目难度用于分析绝对正确率以及编排相对收益是否随难度变化，底层模型则作为编排效果可能异质的重要条件。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$N$**

Best-of-$N$ 中为同一题目并行生成的候选答案数量。

</div>
<div class="notation-item" markdown="1">

**$x$**

一个待求解的基准测试题目。

</div>
<div class="notation-item" markdown="1">

**$d(x)$**

题目 $x$ 的人类来源难度估计；该符号用于概括论文的问题设置，并非原文在所给章节中明确规定的记号。

</div>
<div class="notation-item" markdown="1">

**$m$**

执行任务的底层大语言模型；该符号用于概括跨五种模型的配对比较，并非原文在所给章节中明确规定的记号。

</div>

</div>

**直接相关的工作**

- **Tran and Kiela (2026)**: 该研究在全局思考令牌预算固定的条件下比较工作流，并发现单智能体推理可匹配或超过若干多智能体结构；本文采用互补的自然执行设计，固定工作流规则后测量其实际令牌与调用消耗。
- **Smit et al. (2024)**: 该研究表明，多智能体辩论在考虑准确率、成本和延迟后未必优于集成式基线，而且协议调优会改变方法排名、超参数跨底层模型只能部分迁移；这些发现支持本文统一优化预算并分别分析不同底层模型。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型的推理效果不仅取决于预训练权重，也取决于推理阶段如何分配计算。增加候选生成、批评修订或多实例交互可以在不更新权重的情况下尝试提高正确率，但会增加模型调用、令牌消耗和延迟，并引入新的失败环节。实际部署因而面对准确率与资源消耗之间的选择：编排带来的增益必须足以补偿额外推理成本，而不能只看最终正确率。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **增加推理计算的固定编排**：Self-Refine 让模型先作答，再批评并修订自己的答案；Best-of-$N$ 生成多个候选并从中选择；Debate 让多个模型实例通过交互形成答案。三者都通过增加推理阶段的结构和计算来改善输出，而不修改模型权重。
- **难度感知的计算与工作流分配**：已有系统先估计任务复杂度，再据此选择模型能力、分配测试时计算量，或为每个查询构造不同工作流。其基本假设是更难的题目可能需要更强模型或更多推理资源。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 已有编排比较常把底座模型、提示词、停止条件、基准数据集和优化投入与工作流结构一起改变，导致结果存在混杂因素；复杂方法还可能因为组件更多而在开发中获得更多调优，从而使准确率差异不能被可靠归因于编排本身。
- 现有证据既缺少受控的准确率—资源联合比较，也没有证明固定编排相对简单推理的收益会随人类定义的题目难度单调增加。因此，难度能够预测绝对正确率下降，并不意味着它足以决定何时启用编排。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种研究设计，在同一批难度分层题目上，对常见固定编排和单次调用基线实施相同的优化预算，并保持底座模型、解码和评分条件一致，同时测量正确率与资源使用。尤其未解决的是：排除这些混杂因素后，编排的净收益是否稳定存在，以及人类难度能否预测其相对收益。

</div>
<div markdown="1"><span>核心问题</span>

在共同的提示优化协议下，Self-Refine、Best-of-$N$ 和 Debate 是否比任务直答或思维链单次调用获得更高准确率，它们需要付出多少额外推理资源，并且这种相对收益是否会随题目难度系统变化，或因底座模型不同而显著异质？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把各方法视为接受同等训练与考试条件的候选方案：先用共同预算优化，再在完全相同的题目上成对比较，并同时记录正确性和资源消耗。这样能较大程度隔离工作流结构本身的作用；进一步将绝对难度效应与“方法相对单次调用的增益”分开建模，则可避免把“难题普遍降低所有方法的准确率”误判为“难题更适合复杂编排”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文采用受控比较框架，评估额外推理时编排是否值得其成本。输入是来自 Codeforces、Lichess 和 AMC、按人类难度分层抽取的同一批题目；对每个题目，五个底座 LLM 分别运行任务提示单次调用、优化后的思维链单次调用，以及 Self-Refine、Best-of-$N$（BoN）和 Debate 三种编排方法。为减少“某种方法仅因提示词调得更充分而获胜”的混杂因素，作者使用 GEPA 在相同优化预算下优化各方法，再比较最终答案正确性、加权令牌成本及其随题目难度和底座模型发生的变化。
从流程上看，这不是训练一个新的语言模型，而是在固定底座 LLM 外增加推理控制结构：Self-Refine 让模型生成、反馈并修订；BoN 产生多个候选后选出一个结果；Debate 组织多次交互以形成最终答案。随后，作者以二元正确性为响应变量建立混合效应模型：先估计控制难度和底座模型后的平均方法效应，再检验“编排收益是否随难度上升”以及“编排收益是否依赖底座模型”。直观地说，实验同时控制题目、模型和调参投入，把问题拆成三层：多调用是否更准、额外准确率需要多少令牌、这种收益究竟由难题还是由模型适配性决定。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 统一题目与难度分层

在三个基准内按难度分层选取评测题目，并让所有方法和五个底座 LLM 处理相同题目；推断模型使用连续标准化难度，难度四分位仅用于保持 bootstrap 重采样的分层设计。

<div class="method-step__io" markdown="1">

**输入**：Codeforces 竞技编程题、Lichess 国际象棋谜题和 AMC 数学题，以及各题目的人类来源难度。<br>
**输出**：跨方法可直接配对比较、同时覆盖不同难度的统一评测项目集合。

</div>

**直观理解**：相当于让所有参赛方案做同一套、难易比例一致的试卷，避免某个方案因为抽到更简单的题而看起来更强。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 等预算方法优化

作者使用 GEPA 分别优化任务提示、CoT 提示及三种编排方法，并保持优化预算一致；原文节选未给出 GEPA 的搜索空间、迭代次数或具体目标函数。

<div class="method-step__io" markdown="1">

**输入**：任务格式、五类推理控制结构及相同的优化预算。<br>
**输出**：在调参投入上尽量可比的任务单调用、CoT 单调用、Self-Refine、BoN 与 Debate 配置。

</div>

**直观理解**：这里控制的是“赛前准备时间”：不能让编排方法经过大量调试，却拿未经调试的单次调用作对照。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行单调用与多调用推理

任务基线仅提交任务提示，CoT 基线提交任务加 CoT 系统提示，二者均调用一次 LLM；Self-Refine 按“生成→反馈→修订”运行，BoN 和 Debate 则通过多次模型调用形成最终候选或结论。节选仅明确 Self-Refine 的控制结构，未完整报告 BoN 的候选数、选择器和 Debate 的角色、轮数。

<div class="method-step__io" markdown="1">

**输入**：优化后的方法配置、一个基准题目和一个固定底座 LLM。<br>
**输出**：每个“题目—底座模型—方法”组合的最终答案、调用记录和总令牌消耗。

</div>

**直观理解**：单调用像一次作答后立即交卷；编排方法则允许复查、多写几份答案再选择，或让多个回答相互质疑，但会消耗更多推理资源。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 答案判定与成本汇总

将每次作答标记为二元变量 $\texttt{correct}$，并汇总包含失败尝试在内的加权令牌总量；成本进一步按正确答案数归一化，并与同一底座模型、同一基准的 task-only 单元比较。

<div class="method-step__io" markdown="1">

**输入**：最终答案、参考答案、所有尝试的令牌记录及失败记录。<br>
**输出**：准确率、整体项目 bootstrap 区间、每个正确答案的加权令牌成本及相对 task-only 成本。

</div>

**直观理解**：不仅看答对多少，还计算“得到一个正确答案平均烧掉多少令牌”；失败调用也计费，因此不会把不稳定方法的真实成本隐藏掉。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 平均方法效应的嵌套混合效应模型

$$
\begin{aligned} M_{0}:\quad &\texttt{correct}\sim\texttt{difficulty}+\texttt{LLM}+(1\mid\texttt{item})+(1\mid\texttt{item}:\texttt{LLM}),\\ M_{1}:\quad &\texttt{correct}\sim\texttt{method}+\texttt{difficulty}+\texttt{LLM}+(1\mid\texttt{item})+(1\mid\texttt{item}:\texttt{LLM}). \end{aligned}
$$

**符号说明**

- $M_0$：不包含方法固定效应的基准混合效应模型。
- $M_1$：在基准模型上加入方法固定效应的混合效应模型。
- $\texttt{correct}$：某次最终答案是否正确的二元响应变量。
- $\texttt{method}$：推理方法类别；计划对比以优化后的 CoT 为参照，比较 Self-Refine、BoN 和 Debate。
- $\texttt{difficulty}$：基准内部的连续标准化人类难度变量。
- $\texttt{LLM}$：五个底座语言模型的固定效应类别。
- $(1\mid\texttt{item})$：题目层面的随机截距，用于表示不同题目的基础正确率差异。
- $(1\mid\texttt{item}:\texttt{LLM})$：题目与底座 LLM 组合的随机项，用于处理同一题目在不同模型上的特异差异与重复观测结构。

<div class="equation-explanation" markdown="1">

**直观理解**：作者通过似然比检验比较 $M_0$ 和 $M_1$：若加入 $\texttt{method}$ 后拟合显著改善，就说明在控制难度、底座模型和题目差异后，方法总体上仍与准确率有关。随后从 $M_1$ 中提取三项计划对比，分别检验三种编排相对优化 CoT 的平均优势比。<br>
**原文位置**：方法章节，统计分析部分，模型 M0 与 M1

</div>

</div>

<div class="equation-block" markdown="1">

#### 方法异质性的交互模型

$$
\begin{aligned} M_{2}:\quad &\texttt{correct}\sim\texttt{method}*\texttt{difficulty}+\texttt{LLM}+(1\mid\texttt{item})+(1\mid\texttt{item}:\texttt{LLM}),\\ M_{3}:\quad &\texttt{correct}\sim\texttt{method}*\texttt{LLM}+\texttt{difficulty}+(1\mid\texttt{item})+(1\mid\texttt{item}:\texttt{LLM}). \end{aligned}
$$

**符号说明**

- $M_2$：允许不同方法具有不同难度斜率的计划交互模型。
- $M_3$：允许不同方法在不同底座 LLM 上具有不同效应的探索性模型。
- $\texttt{method}*\texttt{difficulty}$：方法主效应、难度主效应及方法与难度交互效应的联合表示。
- $\texttt{method}*\texttt{LLM}$：方法主效应、LLM 主效应及方法与 LLM 交互效应的联合表示。
- $\texttt{item}:\texttt{LLM}$：题目与 LLM 的组合层级。

<div class="equation-explanation" markdown="1">

**直观理解**：比较 $M_1$ 与 $M_2$ 回答“题目每增加一个标准差的难度，编排相对 CoT 的优势是否系统变化”；比较 $M_1$ 与 $M_3$ 则回答“同一种编排是否会因底座模型不同而表现不同”。前者是预先规划的难度检验，后者是作者根据描述性结果追加的探索性分析，两者证据地位不同。<br>
**原文位置**：方法章节，统计分析部分，模型 M2 与 M3

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用传统参数训练目标：论文不训练或微调五个底座 LLM，而是在相同预算下使用 GEPA 优化各方法的提示与推理配置。该优化阶段服务于公平比较，但所给节选没有明确报告 GEPA 的目标函数、候选表示、搜索轮数和选择准则，因此不能进一步断言它直接优化准确率、成本或二者的组合；评测阶段的混合效应模型属于统计推断工具，也不是语言模型训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 受控优化模块**

所有基线和编排方法均由 GEPA 在相同优化预算下分别优化，使比较对象是“经过同等优化的方法配置”。该设计控制优化投入，但节选未说明 GEPA 的内部优化目标和搜索过程。

> 直观理解：它用于排除调参不公平：观察到的差异应更多来自推理结构，而不是某一方法获得了更多人工或自动搜索机会。

**2. 推理编排模块**

该模块把固定底座 LLM 包装成不同调用图：task-only 与 CoT 各调用一次；Self-Refine 串联生成、反馈和修订；BoN 汇集多次候选；Debate 通过多次交互得到最终输出。编排增加的是推理时计算与信息流，不更新底座模型参数。

> 直观理解：它像在同一名解题者外增加不同工作流程，研究对象不是“换一个更强模型”，而是“让同一个模型多想、多选或相互审查是否划算”。

**3. 难度与模型异质性分析模块**

广义混合效应分析加入题目随机截距 $(1\mid\texttt{item})$ 和题目—LLM 随机项 $(1\mid\texttt{item}:\texttt{LLM})$，并以固定效应表示方法、连续难度和五个 LLM。计划模型 $M_2$ 检验方法特异的难度斜率，探索模型 $M_3$ 检验方法效应是否因底座 LLM 而异。

> 直观理解：同一道题可能天然更难，而且某道题可能恰好特别适合某个模型；随机效应用来吸收这些重复测量相关性，防止把题目差异误判成编排收益。

**训练与推理**

优化阶段对 task-only、CoT、Self-Refine、BoN 和 Debate 分别运行等预算 GEPA，得到各自配置；底座 LLM 参数保持不变。正式推理时，每个方法在同一批难度分层题目和同一组五个模型上执行：两个基线各进行一次调用，三种编排方法进行多阶段或多候选调用并输出唯一最终答案。评测器记录逐题正确性、所有调用及失败尝试的加权令牌，再按基准拟合 $M_0$ 至 $M_3$；平均效应和难度交互属于计划分析，方法与 LLM 交互属于探索性分析。

**复现信息**

公平解释结果所必需的实现信息包括：五个方法共享相同优化预算和相同评测题目；难度作为基准内部连续标准化预测量进入统计模型，而难度四分位只用于分层 bootstrap；置信区间采用整体题目重采样，以保留同一题目跨模型、跨方法的相关结构；加权令牌总量包含失败尝试；三个编排相对 CoT 的计划对比在每个基准内使用 Holm 多重比较校正。所给节选未明确报告 GEPA 的具体配置、BoN 的 $N$、候选选择机制、Debate 轮数与角色设置、令牌加权公式，以及各方法统一的生成超参数，这些信息需回查原文后才能完整复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Codeforces：Easy2Hard-Bench 中的竞技编程任务，难度来自参赛者记录推导的连续评分。作者使用独立训练集运行 GEPA 提示优化，并从不相交的评估集固定抽取 200 题；抽样同时按归一化难度分位数的十分位和评分不确定性的三分位分层。它主要检验代码推理、答案生成与自动判定条件下的准确率和资源成本。
- Lichess：Easy2Hard-Bench 中的国际象棋战术题，连续难度同样由玩家作答记录推导。实验使用专门的 GEPA 训练集和固定的 200 题评估子集，并保持与其他方法完全相同的题目集合。该数据集用于检验编排在状态理解、棋步搜索和高难度组合推理中的作用。
- AMC：Easy2Hard-Bench 中的数学竞赛题，题目难度通过基于人类作答统计的项目反应理论（IRT）估计。作者同样使用独立训练集优化提示，并从不相交评估集中分层固定抽取 200 题。该数据集检验数学推理场景中的平均准确率增益、难度交互和推理成本。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率及配对准确率差**

准确率是自动验证为正确的评估题比例；配对差在相同题目上计算编排方法与 task-only 或 CoT 的百分点差，并用整题 bootstrap 置信区间表达不确定性。 （越高越好；差值大于零表示编排在相同测试题上更准确，但置信区间包含零时不能据此确认稳定优势。）

</div>
<div class="metric-item" markdown="1">

**加权 token 数及每个正确答案的加权 token 数**

加权 token 数 $t_w$ 汇总一次评估消耗的推理资源；每个正确答案的加权 token 数进一步把总资源消耗除以正确答案数量，用于比较获得有效结果的成本。 （越低越好；在准确率相近时，更少的 $t_w$ 表示更高的推理效率。）

</div>
<div class="metric-item" markdown="1">

**混合效应模型检验**

似然比检验、AIC、优势比（OR）及其置信区间用于判断加入方法效应、方法与难度交互或方法与骨干模型交互后，是否能更好解释逐题正确与否。 （模型比较中，更低 AIC 和显著的似然比检验表示新增效应改善拟合；对方法优势而言，OR 大于 1 表示相对 CoT 的成功优势更高，但仍需结合置信区间和多重比较校正。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 五个骨干模型上的平均准确率：三种编排方法相对优化 CoT

<div class="result-value" markdown="1">

Codeforces 上 Self-Refine 和 BoN 相对 CoT 分别提高 4.6 和 4.2 个百分点，95% bootstrap 区间分别为 $[2.1,7.1]$ 和 $[1.8,6.5]$；AMC 上二者分别提高 1.9 和 2.6 个百分点，区间为 $[0.5,3.3]$ 和 $[1.3,4.0]$。Lichess 的所有方法对比均不显著，Debate 在三个基准上均未显著超过 CoT。

</div>

作者结果表明，多调用并非普遍无效，但稳定收益集中在 Self-Refine 和 BoN，且最大平均提升仅为中等幅度。区间排除零支持这些特定数据集上的平均优势，却不能证明所有模型或题目都受益；Debate 的复杂交互结构也没有显示出可靠的额外价值。

<div class="result-source" markdown="1">

来源：第 4.2 节，Figure 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The 95% whole-item bootstrap intervals excluded zero for Codeforces Self-Refine (+4.6 points, [2.1, 7.1]) and BoN (+4.2, [1.8, 6.5]), and for AMC Self-Refine (+1.9 points, [0.5, 3.3]) and BoN (+2.6, [1.3, 4.0]); the other CoT contrasts included zero.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 编排相对收益与人类题目难度的关系

<div class="result-value" markdown="1">

虽然难度与准确率在 Codeforces、Lichess 和 AMC 上分别呈 $\rho=-.533$、$-.660$ 和 $-.485$ 的负相关，但加入方法与连续难度交互的模型 $M_2$ 并未优于加性模型 $M_1$：三个基准的似然比检验分别为 $p=.688$、$.972$ 和 $.874$。九项预设斜率比检验的区间全部包含无效值 1，Holm 校正后的 $p$ 值均至少为 $.887$。

</div>

难题确实更容易答错，但“题目越难，编排相对 CoT 越有用”没有得到支持。描述性分组中个别难度区间可能出现较大收益，例如 Codeforces 的第三四分位，但这种波动没有形成跨难度水平的稳定单调趋势；因此不能把编排简单定位为专门解决最难题目的策略。

<div class="result-source" markdown="1">

来源：第 4.3 节，Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Compared with M1, M2 did not improve model fit for Codeforces (χ2(3)=1.47, p=.688), Lichess (χ2(3)=0.23, p=.972), or AMC (χ2(3)=0.70, p=.874).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 准确率收益、骨干模型异质性与推理资源成本

<div class="result-value" markdown="1">

方法与骨干模型的交互在 Codeforces、Lichess 和 AMC 上均显著，检验结果分别为 $\chi^2(12)=53.82$、30.68 和 87.68；模型特定的编排减 CoT 差值可从 Codeforces 的 -4.0 到 +18.0 个百分点、Lichess 的 -6.5 到 +12.0 个百分点以及 AMC 的 -9.5 到 +11.0 个百分点。同时，Self-Refine、BoN 和 Debate 的平均 $t_w$ 分别达到 CoT 的 1.82 至 2.13 倍、2.65 至 3.76 倍和 3.04 至 3.40 倍，具体范围随基准而变。

</div>

编排是否值得采用，主要取决于具体骨干模型和任务组合：同一种方法可能对一个模型明显增益，却使另一个模型退步。额外调用通常把资源消耗提高到 CoT 的约两至四倍，因此平均准确率略升并不等于成本效益更高；部署决策应比较具体模型单元格的准确率与成本，而非只采用跨模型均值。

<div class="result-source" markdown="1">

来源：第 4.4 至 4.5 节，Figures 3–4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Mean tw use for Self-Refine, BoN, and Debate was 2.12, 3.76, and 3.40 times CoT on Codeforces; 2.13, 2.65, and 3.04 times on Lichess; and 1.82, 3.25, and 3.08 times on AMC.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 每个基准只使用固定的 200 题评估子集，虽然分层抽样、共享题集和逐题配对设计降低了混杂并保留统计功效，但对完整 Easy2Hard-Bench、其他领域或不同难度分布的外推仍有限。
- 实验仅覆盖五个本地开放权重模型、三类编排结构和统一的 120,000-token 输出上限；模型与方法交互分析还是探索性的。此外，达到输出上限但未返回有效答案的尝试同时记零分并计入 token，这符合实际资源核算，却会使容易发生超长推理的模型在准确率和成本两方面同时受罚。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- task-only：仅提供任务指令的单次模型调用，是推理结构和额外调用最少的基准；它用于衡量编排相对于普通推理的绝对收益及额外 token 成本。
- GEPA-optimized CoT：通过 GEPA 在与编排方法相同的优化预算下得到的思维链单次调用基准。它是主要推断参照，因为它控制了提示优化投入，并检验多次调用的收益是否超出较强的单次调用推理。
- Self-Refine：先生成答案，再通过后续调用批评和修订同一答案。与 CoT 比较可检验迭代自我反馈本身是否带来收益。
- BoN 与 Debate：BoN 生成多个候选并选择最佳答案，检验采样多样性与选择机制；Debate 让多个推理角色交换意见后形成答案，检验交互式多代理结构。二者共同代表不同于顺序修订的多调用计算分配方式。

**实验想回答的问题**

- 在为所有方法提供相同提示优化预算、相同骨干模型和相同测试题目的受控条件下，Self-Refine、Best-of-$N$（BoN）和 Debate 是否比 task-only 与优化后的单次调用 CoT 获得足以抵偿额外推理成本的准确率提升？
- 编排方法的相对收益是否会随题目难度系统性增大，或者主要取决于所使用的骨干大语言模型？

**实验实现**

实验形成五个骨干模型、五种推理方法和三个基准的全交叉设计。五个本地开放权重模型为 DeepSeek V4 Flash、Gemma 4、GLM 4.7 Flash、Qwen 3.6 和 GPT-OSS Puzzle 88B；同一实验内，各方法共享骨干模型与解码设置。所有方法使用 120,000-token 输出上限，并通过 vLLM 以温度 1.0、top-$p$ 0.95 运行。每个数据集固定同一组 200 道分层抽样题，使模型或方法差异不会与测试子集选择混杂；GEPA 使用专门训练集，并对 CoT、Self-Refine、BoN 和 Debate施加相同优化预算。主要分析聚合五个模型，同时使用逐题配对差、整题 bootstrap 区间和混合效应模型；难度分析使用连续的人类难度估计，模型异质性分析则加入方法与骨干模型的交互。达到输出上限但未给出有效答案的尝试记为错误，其 token 仍计入资源总量。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 优化 CoT 与 task-only 的单次调用对照 | 跨五个模型，CoT 相对 task-only 在 Codeforces、Lichess 和 AMC 上分别变化 -0.1、+1.5 和 -1.4 个百分点，对应 95% 置信区间均包含零。 | 该对照隔离了“加入并优化思维链提示”本身，而不引入多次模型调用。结果说明，平均而言，优化 CoT 并未稳定超过最简单的 task-only；因此同时保留两种基准是必要的。不过模型特定差异较大，这也意味着总体均值不能解释每个骨干模型的行为。 | 第 4.1 节<br><span class="experiment-evidence">Across the five models, CoT differed from task-only by −0.1 percentage points on Codeforces (paired normal-approximation 95% CI [−2.8, 2.6]), +1.5 points on Lichess (95% CI [−1.0, 4.0]), and −1.4 points on AMC (95% CI [−2.9, 0.1]).</span> |
| 移除或加入方法与骨干模型交互项 | 加入方法与模型交互后，Codeforces、Lichess 和 AMC 的拟合改善检验分别为 $\chi^2(12)=53.82, p<.0001$、$\chi^2(12)=30.68, p=.0022$ 和 $\chi^2(12)=87.68, p<.0001$。 | 这一模型比较隔离了“所有骨干模型共享同一方法效应”的假设。显著改善说明平均方法效应掩盖了真实的模型差异，但该分析被作者标为探索性结果，适合生成模型选择假设，尚不能替代预先注册的逐模型确认实验。 | 第 4.4 节，Figure 3<br><span class="experiment-evidence">Exploratory likelihood-ratio tests indicated method-by-LLM heterogeneity on Codeforces (χ2(12)=53.82, p<.0001), Lichess (χ2(12)=30.68, p=.0022), and AMC (χ2(12)=87.68, p<.0001).</span> |

**定性案例**

- GPT-OSS 在 Codeforces 上由 task-only 的 58.0% 提升到 Debate 的 70.0%，但每个正确答案的加权 token 从 37,024 增至 130,888。这个单元格直观展示了论文的核心权衡：12 个百分点的准确率提升伴随约 3.5 倍的单位正确答案成本；它是说明性个案，不能代表 Debate 的总体效果，因为 Debate 在跨模型推断中并未显著优于 CoT。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper's central contribution is a controlled benchmark evaluation of LLM inference orchestration across accuracy, cost, difficulty, and model backbones.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`59a1bcb0eecd5a0b2df02f15baa060cf40fbd06b4a61e327d49950368d5e02fd`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
