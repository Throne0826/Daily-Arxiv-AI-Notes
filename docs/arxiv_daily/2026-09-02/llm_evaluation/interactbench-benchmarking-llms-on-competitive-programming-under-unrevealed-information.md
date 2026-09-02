---
title: "[论文解读] InteractBench: Benchmarking LLMs on Competitive Programming under Unrevealed Information"
description: "[arXiv 2608.29632][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.29632"
announcement_date: "2026-09-02"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:38:45.268893+00:00"
source_sha256: "1fe4211fdaa80c85378f50cda023dc7f584810c1870a624193e2fdaaf4152a8f"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "代码生成"
  - "竞技编程"
  - "交互式问题"
  - "本地交互器"
  - "离线评测"
  - "查询预算"
  - "协议感知诊断"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.29632</p>

# InteractBench: Benchmarking LLMs on Competitive Programming under Unrevealed Information

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Jiaze Li, Aocheng Shen, Bing Liu, Boyu Zhang, Xiaoxuan Fan, Qiankun Zhang, Xianjun Deng</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: School of Cyber Science and Engineering, Huazhong University of Science and Technology, Wuhan, China；Affiliation: Key Laboratory of Cyberspace Security, Ministry of Education, Zhengzhou, China；Affiliation: Hubei Key Laboratory of Distributed System Security, Wuhan, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.29632v1) · [PDF 下载](https://arxiv.org/pdf/2608.29632v1) · **关键词** 大语言模型, 代码生成, 竞技编程, 交互式问题, 本地交互器, 离线评测, 查询预算, 协议感知诊断<br>
**代码**: [https://github.com/kmsgk0/InteractBench](https://github.com/kmsgk0/InteractBench)

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

大语言模型的代码能力通常通过执行生成程序并检查结果是否正确来评估。HumanEval、MBPP及多数竞技编程基准采用批处理式任务：程序启动时即可获得完整且静态的输入，因此主要考查算法设计和代码实现。本文关注其中尚未被充分覆盖的交互式竞技编程：关键数据由裁判程序隐藏，参赛程序必须在运行期间依照指定协议发起多轮查询，根据返回信息动态维护状态，并在有限查询次数以及时间、内存约束下给出最终答案。这一设置不仅要求算法逻辑正确，也要求生成代码能够正确管理输入输出时序、查询预算和交互状态。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**批处理式问题（batch-style problem）**

程序开始运行时一次性获得完整输入，且输入内容不会随程序行为改变。程序通常完成计算后直接输出答案，不需要在运行中向裁判索取新信息。

</div>
<div class="concept-item" markdown="1">

**交互式问题（interactive problem）**

关键输入由交互器隐藏，求解程序需要通过多轮查询逐步获得信息，再提交最终答案。每轮消息的格式与顺序必须符合协议，而且通常存在严格的查询次数上限。

</div>
<div class="concept-item" markdown="1">

**本地交互器（local interactor）**

交互器是模拟在线裁判、保存隐藏实例并回应程序查询的可执行组件。本地交互器使程序与裁判的完整通信可在离线环境中复现，无需向外部在线评测系统提交代码。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

InteractBench评估的是大语言模型一次性生成的自包含程序，而不是模型反复运行、观察测试反馈并修改代码的开发代理。对每道题，程序只能先读取题目允许公开的信息；隐藏实例保存在本地交互器中。运行时，程序按照题目规定的标准输入输出接口或 grader-linked 接口发送查询，交互器依据隐藏实例返回响应，每次查询消耗相应预算；程序需要综合多轮响应更新内部状态，并在预算、协议、时间和内存限制内输出最终答案。评测输出不仅包括程序是否通过，还区分普通算法错误与交互特有故障，如协议违规、查询预算超限、死锁或超时。基准包含来自 Codeforces、AtCoder、IOI 和 ICPC 的 322 道交互题，并为每题提供可执行的本地交互器，以支持完全离线且可重复的评估。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **LiveCodeBench Pro**: 该竞技编程基准提供自包含评测、标签和难度信息，但原文表1显示其584道题中仅21道支持交互；InteractBench则将322道题全部设为交互题，集中测量隐藏信息条件下的运行时查询能力。
- **LiveOIBench**: 该基准同时支持标准输入输出和 grader-linked 接口，也包含交互题，但原文表1显示其403道题中仅23道为交互题。InteractBench在接口覆盖相近的基础上提供完整的交互题集合、本地可执行交互器及协议感知的失败诊断。

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

InteractBench 的目标不是训练模型，而是构建一个可离线执行、能忠实模拟在线交互判题的基准。对每个交互式编程任务，系统把求解器 $S$、隐藏测试用例 $x$、本地交互器 $J$、交互协议 $\Pi$ 和查询预算 $B$ 封装到沙箱中；求解器根据历史对话逐轮提出查询并读取响应，最终输出答案，评测器据此判定 Accepted 或 Rejected，同时记录完整交互轨迹和结构化失败原因。直观地说，它把原本依赖竞赛平台的“向裁判提问并逐步获得信息”的任务，改造成一套可重复运行的本地实验装置。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 任务筛选与标注

仅保留具有多轮交互、明确消息格式与终止条件、以及可监控或强制执行查询预算的任务；排除本质上是单次调用的批处理式接口，并为任务标注 Easy、Medium、Hard 难度和 Graph、Search、Greedy、Bit、Data Structures、Math、Game 七类中的一个或多个类别。

<div class="method-step__io" markdown="1">

**输入**：来自 Codeforces、AtCoder、IOI 和 ICPC 的候选交互式编程题。<br>
**输出**：满足交互条件并带有难度、类别元数据的任务集合，最终基准包含 322 道题。

</div>

**直观理解**：这一步先确认题目确实要求程序“边问边解”，而不是把完整输入一次性读入。类别和难度标签用于描述测试覆盖面，而不是改变题目的判定规则。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成本地评测器

通过 execution-driven propose–validate–adjudicate 循环生成测试用例生成器和交互器：提议模型先拟定候选生成器，随后拟定交互器；根据题目是否允许交互器依赖历史，选择自适应或非自适应模式。每题生成固定随机种子的 100 个测试用例，并将求解器与交互器包装为通过标准输入输出通信的两个隔离进程。

<div class="method-step__io" markdown="1">

**输入**：筛选后的题面、原始接口规范、隐藏数据格式以及题目的官方评测信息。<br>
**输出**：包含测试生成器、本地交互器、沙箱配置和协议检查逻辑的离线评测器工件。

</div>

**直观理解**：可以把交互器理解为本地裁判：它保存隐藏信息，只在程序提问后按题目规则回答。固定种子使不同模型面对同一组实验条件，双进程结构则模拟真实比赛中的程序—裁判通信。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行验证与人工裁决

每题使用 15 个官方结果为 Accepted 的提交、15 个官方判为 Rejected 的人工提交和 15 个通过轻微变异得到的拒绝探针进行验证；检查离线判定是否与官方结果一致，并测试协议、格式和查询预算违规能否被拒绝。失败候选获得基于交互轨迹的反馈并重新生成，最多迭代三轮，仍有歧义的案例交由专家修订。

<div class="method-step__io" markdown="1">

**输入**：候选离线评测器、每题验证池，以及待检查的求解器提交。<br>
**输出**：经执行验证和必要人工审计后确认的本地评测器，以及每次执行的轨迹、终止信号和结构化拒绝原因；共有 31 道题需要专家介入。

</div>

**直观理解**：不是只检查裁判代码能否运行，而是用已知正确和已知错误的程序反向测试裁判是否可靠。若自动生成的裁判与官方判题不一致，系统根据“程序在哪里、为何失败”的轨迹改写它，必要时由竞赛专家处理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 模型解答与一致性审计

在资源受限沙箱中运行程序；程序在第 $t$ 轮依据此前的交互前缀产生查询，交互器返回响应，系统更新 transcript 并计数查询或轮次。程序结束后，评测器同时检查协议合规、预算不超限和最终答案正确性；在允许的题目上，再从每题抽取 5 个提交到官方接口，比较线上与离线的 Accepted/Rejected 结果。

<div class="method-step__io" markdown="1">

**输入**：模型生成的参赛程序、本地隐藏测试用例、交互器、协议 $\Pi$ 和查询预算 $B$。<br>
**输出**：每次提交的最终判定、完整交互 transcript、终止信号和失败类型；另得到有限规模的线上—线下一致性审计结果。

</div>

**直观理解**：模型不能偷看隐藏信息，只能通过合法提问逐步推断。即使答案算法本身正确，只要输出格式错、没有及时刷新、超出提问次数或最终答案错，也会被判为失败。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 交互过程与最终判定

$$
q_t=S_{\mathrm{qry}}(\tau_{<t}),\quad r_t=J(x,\tau_{<t},q_t),\quad \tau_t=\tau_{<t}\circ(q_t,r_t),\quad t=1,\ldots,T;\quad \tau=\tau_T,\quad a=S_{\mathrm{out}}(\tau),\quad v=\mathrm{Eval}(a,\tau,x;\Pi,B)\in\{\mathrm{Accepted},\mathrm{Rejected}\}
$$

**符号说明**

- $S$：求解器，即待评测的程序或模型生成代码。
- $S_{\mathrm{qry}}$：求解器根据已有交互历史生成下一次查询的部分。
- $S_{\mathrm{out}}$：求解器依据完整交互轨迹生成最终答案的部分。
- $J$：交互器或本地裁判。
- $x$：隐藏测试用例或隐藏状态。
- $q_t$：第 $t$ 轮求解器发出的查询。
- $r_t$：第 $t$ 轮交互器返回的响应。
- $\tau_t$：完成前 $t$ 轮后的交互 transcript。
- $\tau_{<t}$：第 $t$ 轮之前的 transcript 前缀，即 $\tau_{t-1}$。
- $\circ$：把新的查询—响应对追加到 transcript 的连接操作。
- $T$：本次执行终止前的交互轮数。
- $a$：求解器根据完整 transcript 产生的最终输出。
- $\Pi$：规定消息格式、合法交互和终止条件的协议。
- $B$：允许的查询、轮次或裁判调用预算。
- $v$：评测结果，取 Accepted 或 Rejected。

<div class="equation-explanation" markdown="1">

**直观理解**：公式把一次交互看成一个闭环：程序根据已有信息提问，裁判回答，历史继续增长，直到程序输出答案。评测器只有在整个 transcript 符合协议、预算未超限且答案对隐藏用例正确时，才返回 Accepted。<br>
**原文位置**：Section 3.1, Problem Definition

</div>

</div>

<div class="equation-block" markdown="1">

#### 离线接受条件

$$
v=\mathrm{Accepted}\iff \tau\ \text{conforms to}\ \Pi\ \land\ Q_{\Pi}(\tau)\leq B\ \land\ a\ \text{is correct for}\ x;\quad \text{otherwise }v=\mathrm{Rejected}
$$

**符号说明**

- $Q_{\Pi}(\tau)$：在协议 $\Pi$ 下，从 transcript $\tau$ 统计出的查询、轮次或裁判调用次数。
- $\mathrm{Accepted}$：程序遵守协议、未超预算且最终答案正确。
- $\mathrm{Rejected}$：至少有一项协议、预算或正确性条件不满足。

<div class="equation-explanation" markdown="1">

**直观理解**：这个条件说明交互题不是“答案对了就行”。程序必须同时做到会提问、按格式通信、控制提问次数，并在获得有限信息后给出正确答案。<br>
**原文位置**：Section 3.1, Problem Definition

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。InteractBench 是评测基准和离线评测器构建方法，不提出用于训练语言模型的损失函数或参数优化目标。提议模型参与的是测试生成器和交互器的构造，而不是学习被评测模型的求解策略；候选工件依据执行结果与官方判定的一致性接受。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 交互式任务形式化与判定器**

任务由求解器 $S$、交互器 $J$、隐藏测试用例 $x$、协议 $\Pi$ 和预算 $B$ 构成。第 $t$ 轮中，求解器根据历史前缀 $\tau_{<t}$ 产生查询 $q_t$，交互器依据 $x$、历史和查询产生响应 $r_t$；系统把二者追加为完整轨迹，并由 $\mathrm{Eval}$ 检查协议、预算和最终输出。

> 直观理解：该模块明确区分“程序主动问了什么”“裁判回答了什么”和“程序最后提交了什么”，因此能够识别普通逻辑错误之外的交互错误。

**2. 生成器—交互器构造与验证循环**

GPT-5.2 和 Gemini-3-Pro-Preview 提议候选测试生成器与交互器，GPT-5.2 还作为面向代码的裁决模型；但候选是否接受由实际执行验证决定。验证池覆盖正确提交、人工错误提交和变异拒绝探针，失败候选接收 trace-grounded feedback，最多三轮后升级人工专家。

> 直观理解：语言模型负责提出裁判实现，运行结果负责决定实现是否可信；这种安排降低了“看起来合理但实际判错”的风险。

**3. 离线沙箱与诊断记录**

求解器和本地交互器作为两个隔离进程经标准流通信，沙箱施加每进程时间和内存限制；显式计数器监控查询、轮次或 grader call，日志保存 transcript、终止信号和统一失败原因。交互器按原题规则分为固定隐藏状态的非自适应模式和可依据历史选择合法回复的自适应模式。

> 直观理解：它把线上裁判的关键行为搬到本地，同时保留通信、超时、超预算和协议违规等信息，便于重复实验和定位模型失败原因。

**训练与推理**

论文所给方法没有针对被测 LLM 的训练阶段。推理时，LLM 先生成交互式编程题的求解代码；本地沙箱启动该代码和对应交互器，代码在每轮读取当前响应、发出下一次查询，并在结束时输出答案；评测器记录 transcript、协议和预算状态，随后根据隐藏用例检查最终正确性并返回 Accepted 或 Rejected。交互器若面对允许历史依赖的题目，则可在与既有 transcript 一致的合法回复中自适应选择；否则在交互开始前固定隐藏测试用例和回复行为。构建评测器时，候选生成器和交互器经历提议、验证、基于轨迹反馈的再提议及最多三轮后的人工审计；此外，在允许官方提交的场景中，每题最多抽取 5 个模型提交进行线上—线下结果核对。

**复现信息**

复现实验必须准备每题的题面、隐藏测试用例生成器、本地交互器、协议解析与终止检查、查询或轮次计数器，以及求解器和交互器的双进程沙箱。论文明确说明每题生成固定随机种子的 100 个测试用例，验证池包含 15 个 Accepted 提交、15 个官方 Rejected 的人工提交和 15 个变异拒绝探针；沙箱默认遵循原题的时间和内存预算，并通过标准流通信，因此跨语言运行的关键是遵守协议并在查询后显式刷新输出。候选工件最多自动迭代三轮，仍有歧义时由有交互式判题经验的竞赛专家根据轨迹修改。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- InteractBench：包含322道来自Codeforces、ICPC、AtCoder和IOI的高质量交互式题目；每题配有可执行的本地交互器，用于离线编译、运行和验证。题目按Easy、Medium、Hard分层，并标注Graph、Search、Greedy、Bit、Data Structures、Math、Game等可多选类别。其作用是测试程序在信息不完全公开时的查询、推理和状态维护能力。原文报告的难度分布为Easy 85、Medium 162、Hard 75；来源分布为Codeforces 220、ICPC 61、AtCoder 17、IOI 24（Table 6）。
- 150道与交互式版本匹配的问题：用于批处理对照实验。Batch设置直接向程序提供隐藏测试数据，但保留相同的最终答案验证逻辑；Interactive设置要求程序通过查询从本地交互器获取信息。该匹配设计主要隔离“信息是否预先揭示”这一因素（Table 9，Section C.1）。
- 时间切分子集：仅使用具有已知发布日期的问题，按切分年份$Y$划分为$P_{<Y}$和$P_{\geq Y}$，并在后者上计算平均$\mathrm{pass}@1$。该设置用于诊断潜在的时间性数据污染，而不是用于比较模型总体能力（Figure 3，Section C.3）。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**$\mathrm{pass}@1$**

单次生成程序在编译、交互执行、协议和最终答案验证全部通过的比例；Interactive设置下还要求程序正确获取并维护隐藏信息。 （越高越好，因为它表示更多程序能够端到端解决题目。）

</div>
<div class="metric-item" markdown="1">

**$\mathrm{pass}@5$或$\mathrm{refine}@5$**

$\mathrm{pass}@5$表示五次独立生成中至少一次通过，$\mathrm{refine}@5$表示五轮基于失败反馈的累计通过率；二者分别衡量候选多样性和连续修正的效果。 （越高越好，但两者不是完全相同的计算过程，不能直接视为同一指标。）

</div>
<div class="metric-item" markdown="1">

**失败类型比例**

在未成功执行中统计WA、PE、QLE、IDLE、CE、RE、TLE和MLE等错误类型的占比：WA为错误答案，PE为协议错误，QLE为查询预算超限，CE为编译错误，其他缩写分别表示空闲、运行时、超时和内存相关失败。 （对某一错误类型而言通常越低越好；重点不是单个比例的绝对大小，而是识别性能瓶颈属于算法推理还是交互执行。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Batch与Interactive对照（150道匹配题，Table 9）

<div class="result-value" markdown="1">

向程序预先揭示隐藏数据后，所有测试模型的$\mathrm{pass}@1$都提高；但批处理并未消除错误答案，说明交互信息获取是额外困难来源，而不是全部算法困难的唯一来源。

</div>

该结果支持“未揭示信息造成独立交互鸿沟”的作者解释：模型不仅要想出算法，还要决定问什么、何时问以及如何根据回复更新状态。不过，Batch仍会失败，因此不能据此断言模型只是不擅长协议；部分失败来自题目本身的算法推理。

<div class="result-source" markdown="1">

来源：Table 9，Section C.1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 9 shows that revealing the hidden test data improves pass@1 for every tested configuration.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 交互失败构成及迭代修正（Table 11）

<div class="result-value" markdown="1">

迭代反馈能够降低部分编译和协议层面的执行错误，但修正后WA仍是五种代表性模型配置中的主要残余失败类型；因此，简单地让模型根据运行反馈改代码，不能充分解决部分可观测交互推理问题。

</div>

这一区分很重要：如果失败主要是CE或PE，增加模板和反馈可能有效；如果主要是WA，则模型需要改进隐藏状态推断、查询规划和算法不变量，而不是只修复代码格式或刷新操作。

<div class="result-source" markdown="1">

来源：Table 11，Section C.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At the same time, WA remains the dominant residual failure type after refinement for all five configurations.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 时间切分污染诊断（Figure 3）

<div class="result-value" markdown="1">

在不同切分年份$Y$下，六种代表性模型在发布日期不早于$Y$的问题上的平均$\mathrm{pass}@1$曲线均未出现明显断崖，而是逐步变化。

</div>

作者据此认为没有观察到由某个单一时间窗口主导的明显记忆泄漏迹象。这只是诊断性证据，不能证明不存在训练数据污染，也不能替代对题目来源、发布日期和模型训练数据的直接审计。

<div class="result-source" markdown="1">

来源：Figure 3，Section C.3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across the sweep, we do not observe a cliff-like discontinuity as the cut year advances; instead, the curves change gradually for all models.

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

- Batch评测：将隐藏测试数据提前提供给模型生成的程序，是Interactive评测的关键对照，用于衡量去除信息获取和交互协议负担后，算法核心本身仍有多大难度。
- Independent resampling：对同一模型和题目独立生成多次程序，并以$\mathrm{pass}@5$统计五次尝试内是否至少成功一次，用于比较增加独立候选程序的收益。
- Few-shot prompting：在提示中加入一个已解决的交互式题目示例，用于测试显式示范是否能改善协议遵循和交互式解题。
- Iterative refinement：将失败执行反馈返回模型并让其逐轮修改程序，以$\mathrm{refine}@5$统计五轮内的累计成功率，用于测试反馈驱动修正是否优于独立重新采样。

**实验想回答的问题**

- 在隐藏信息必须通过多轮查询获得的交互式编程环境中，LLM生成程序的成功率如何随题目难度、信息获取类别和动态状态跟踪要求变化？
- 交互式评测中的失败主要来自算法逻辑错误，还是来自协议违规、查询预算超限等交互执行问题；在批处理输入、提示示例和迭代修正等设置下，这些失败是否能够缓解？

**实验实现**

所有Inter­actBench任务均在本地评测框架中运行，并使用随题目提供的可执行交互器。模型采用统一的零样本代码生成包装提示，要求生成单文件程序、遵守标准输入输出、每次查询后刷新输出、遇到无效响应立即终止且不向标准输出打印调试信息；程序随后被编译并与交互器执行，正确性由完整交互记录和最终验证共同判定（Appendix B.3）。模型覆盖闭源与开源配置，包括GPT-5.2、GPT-4.1、Gemini系列、Claude-Opus-4.5、DeepSeek系列和Qwen3系列。主实验按难度和类别报告结果；补充实验比较Batch与Interactive、独立重采样、少样本提示、迭代修正、时间切分以及多语言输入输出模板。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Batch输入相对于Interactive输入（Table 9） | 所有测试配置在Batch下的$\mathrm{pass}@1$高于Interactive；同时，Batch显著减少协议错误和查询预算超限，但错误答案仍是未成功运行中的主要失败类型。 | 该对照隔离了“隐藏数据是否提前给出”这一设计因素。性能提升说明查询过程本身确实造成负担；错误答案仍占主导则说明去掉交互后，题目的算法核心依然具有挑战。 | Table 9，Section C.1<br><span class="experiment-evidence">Batch evaluation also substantially reduces protocol errors and query-budget overruns, but wrong answers remain the dominant failure type among unsuccessful runs.</span> |
| 独立重采样、少样本提示与迭代修正（Table 10） | 少样本提示的效果通常接近独立重采样，并在多数配置上略高；迭代修正对较强模型相对于单次尝试有改善，但最终仍低于独立重采样和少样本提示。以GPT-5.2为例，五轮迭代累计成功率为$0.677$，而独立重采样和少样本提示分别为$0.705$和$0.714$。 | 该实验比较三种测试时增强方式：增加独立候选、提供交互范例、利用失败反馈连续改写。结果更支持“范例或多次独立尝试能提高找到正确方案的机会”，而不是认为当前反馈迭代机制已经能可靠完成深层交互推理。 | Table 10，Section C.2<br><span class="experiment-evidence">Iterative refinement improves over a single attempt for stronger models, but its final scores remain below those of independent resampling and few-shot prompting.</span> |

**定性案例**

- Qwen3-14B的两种推理配置出现设置相关的排序反转：NonThinking版本在Batch评测中高于Thinking版本，但在Interactive评测中低于Thinking版本。原文将其作为交互环境可能改变模型相对表现的现象报告；这提示不能仅依据完整信息任务中的模型排名推断其在交互任务中的排名，但该现象本身不足以解释具体原因。证据：“A rank reversal appears for the two Qwen3-14B variants: Qwen3-14B-NonThinking is higher in batch evaluation (0.180 vs. 0.093), but lower in interactive evaluation (0.011 vs. 0.056).”（Table 9，Section C.1）

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces a benchmark for evaluating LLM algorithmic and code reasoning on interactive competitive-programming problems.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`1fe4211fdaa80c85378f50cda023dc7f584810c1870a624193e2fdaaf4152a8f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
