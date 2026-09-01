---
title: "[论文解读] Test-Time Scaling for Scientific Equation Discovery"
description: "[arXiv 2608.28660][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.28660"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:42:52.889286+00:00"
source_sha256: "197ee42671c6ff9eb3abea0b2074d65b3eb42328ed6ec1d0bdc6f643081f948f"
tags:
  - "LLM Reasoning"
  - "测试时扩展"
  - "自动方程发现"
  - "符号回归"
  - "大语言模型搜索"
  - "外部验证器"
  - "探索—利用权衡"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.28660</p>

# Test-Time Scaling for Scientific Equation Discovery

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Haowei Lin, Hubert Lim, Xiangyu Wang, Letian Huang, Di He</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Peking University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28660v1) · [PDF 下载](https://arxiv.org/pdf/2608.28660v1) · **关键词** 测试时扩展, 自动方程发现, 符号回归, 大语言模型搜索, 外部验证器, 探索—利用权衡<br>


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

本文位于自动方程发现与测试时扩展（test-time scaling, TTS）的交叉领域。自动方程发现通常被视为符号回归：给定观测数据，系统搜索能够描述数据规律的数学方程或可执行程序，并在预测准确性与表达式简洁性之间取得平衡。TTS则是在不更新模型参数的情况下，于推理阶段增加计算量；本文具体研究外部TTS，即通过多次调用大语言模型生成、评价和筛选候选方程，而不是仅让一次回答使用更多推理标记。与数学答题或代码生成等具有明确标准答案的封闭任务不同，方程发现是开放式搜索问题，通常没有唯一目标字符串，候选解的进展由任务专用验证器根据观测数据进行评价。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**符号回归与方程发现**

符号回归从数据中搜索数学表达式，例如由变量、常数、运算符组成的方程，而不仅仅是拟合一个固定形式的模型。本文将大语言模型用作候选方程或程序的生成器，再由外部评价器判断候选结果。

</div>
<div class="concept-item" markdown="1">

**测试时扩展与搜索控制流**

测试时扩展是在模型参数保持不变时增加推理阶段计算，以获得更好的结果。控制流规定计算如何分配：可以并行生成许多候选，也可以逐步修改少量候选，或采用带分支和筛选的混合搜索。

</div>
<div class="concept-item" markdown="1">

**验证器与探索—利用权衡**

验证器是根据任务目标给候选方程打分或判断其质量的外部评价机制；在本文中，它使系统能够从生成结果中保留较优候选。探索是尝试更多样的新候选，利用则是围绕当前较优候选继续改进，二者需要在有限计算预算下分配。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个自动方程发现任务及其观测数据、任务描述和可调用的大语言模型；系统还获得一个固定的全局测试时计算预算$N$，并假设存在能够提供有信息反馈的任务专用验证器。输出是搜索过程中发现的候选数学方程或可执行程序，最终依据验证器分数选择较优解。论文把搜索表示为动态记忆状态$4mathcal{M}_t$4：在第$t$步，从已有候选中选择待扩展对象，生成新候选，评价其质量，再将新旧候选合并并剪枝；研究问题不是设计复杂的领域提示或变异规则，而是在预算固定时确定候选数量、扩展次数、保留规模和迭代轮数应如何组合。方程发现是开放式设置，因此“正确性”主要体现为验证器分数的改善，而不一定对应预先给定的唯一答案。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{M}_{t}$**

第$t$步的动态记忆状态，保存当前可用的候选方程或可执行程序。

</div>
<div class="notation-item" markdown="1">

**$q_{t}(\cdot\mid\mathcal{M}_{t})$**

在第$t$步根据当前记忆状态选择待扩展候选的策略；它可以是贪心的，也可以依据候选分数进行选择。

</div>
<div class="notation-item" markdown="1">

**$S_{t}=\{x_{t}^{(i)}\}_{i=1}^{n_{t}}$**

第$t$步被选中用于扩展的候选集合，其中$n_t$表示所选候选的数量。

</div>
<div class="notation-item" markdown="1">

**$G_{t}=\bigcup_{i=1}^{n_{t}}G_{t}^{(i)}$**

第$t$步生成的新候选总集合；$G_t^{(i)}$表示由第$i$个被选候选生成的候选集合，其大小由分支因子决定。

</div>

</div>

**直接相关的工作**

- **Best-of-N与外部测试时扩展**: Best-of-$N$通过并行生成多个候选，再用验证器选择结果，代表一次性扩大搜索宽度的控制流。本文将其与顺序改进、树搜索及演化式搜索统一到固定预算下的计算分配框架中，并比较不同分配方式而非复杂提示工程的作用。
- **LLM驱动的方程发现与演化式搜索系统**: 已有系统让大语言模型提出候选方程或程序，并借助外部目标函数反复评价、变异和筛选。本文认为这些系统通常同时包含专门提示、突变规则、模型集成和剪枝启发式，因此难以识别基本因素；本文以最小化的并行控制器作为受控研究对象，重点考察搜索宽度、种群规模与分支规模等计算分配决策。

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

该方法将大型语言模型驱动的科学方程发现形式化为固定测试时计算预算下的迭代搜索。给定观测数据和方程发现任务，模型反复从候选方程出发生成新候选，由验证器根据拟合参数、数值评估或候选程序执行结果计算分数，再依据控制器选择下一轮扩展对象并保留搜索记忆；核心研究变量是群体规模 $n$、每个父候选的分支数 $k$、分组数 $g$ 及其形成的单轮搜索宽度 $w=nk$。直观地说，方法不是继续训练模型，而是在推理时决定“同时尝试多少种方程、从哪些方程继续尝试，以及如何保留较好的候选”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始化候选搜索状态

将候选划分到 $g$ 个独立或半独立的搜索组中，并设定每组的局部群体规模为 $n/g$、局部预算为 $N/g$；每轮从当前状态选择候选进行扩展。

<div class="method-step__io" markdown="1">

**输入**：科学方程发现任务、观测数据、初始候选集合 $\mathcal{M}_0$、总测试时计算预算 $N$，以及控制参数 $n$、$k$、$g$。<br>
**输出**：各组的活动候选集合、历史记忆状态，以及每轮可生成的总候选数 $w=nk$。

</div>

**直观理解**：先把有限的尝试次数分配给若干个小搜索队伍，每个队伍维护一批当前候选。$n$ 决定同时保留多少个父候选，$k$ 决定每个父候选产生多少个后继。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 依据控制策略选择扩展对象

在 PBeam 中，选择每组完整的当前前沿 $S_t=\mathcal{M}_t$；在 PIE 中，将当前生成历史并入 $\mathcal{H}_{t+1}$，按照由温度参数 $\tau$ 控制的 softmax 概率从全部历史候选中抽取 $n/g$ 个候选。

<div class="method-step__io" markdown="1">

**输入**：当前候选状态、验证器分数 $f(x)$、选择策略 $q$，以及控制器的群体和分支参数。<br>
**输出**：下一轮待扩展的候选集合 $S_t$。

</div>

**直观理解**：PBeam 只从当前排名靠前的“前线队伍”继续探索，决策直接而集中；PIE 像保留一份完整档案，即使较早的候选暂时落后，也仍有机会凭概率再次被尝试。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 并行生成方程候选

语言模型为每个选中候选生成 $k$ 个方程或方程程序后继；每轮总生成量为 $w=nk$，并可按组并行提交候选验证任务。

<div class="method-step__io" markdown="1">

**输入**：选中的候选方程、原始任务提示、观测数据上下文和每个父候选的分支数 $k$。<br>
**输出**：新生成候选集合 $G_t$，其中 PBeam 每组产生 $w/g=(n/g)k$ 个候选。

</div>

**直观理解**：这一步相当于同时让多个研究者从若干条思路出发提出新公式。较大的 $w$ 提高探索范围，也增加可并行运行的验证任务数量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 验证、评分与状态更新

验证器计算每个候选的分数 $f(x)$；PBeam 将当前候选与新候选合并后只保留得分最高的 $n/g$ 个，PIE 则把新候选加入完整历史 $\mathcal{H}_{t+1}$，并将该历史作为下一轮记忆状态。

<div class="method-step__io" markdown="1">

**输入**：当前候选、生成集合 $G_t$、观测数据和验证器。<br>
**输出**：更新后的群体或历史状态 $\mathcal{M}_{t+1}$，以及最终从全部已验证候选中选出的方程。

</div>

**直观理解**：验证器像实验或测试仪器：它检查公式是否能解释数据。PBeam 严格保留当前最好的少数方案，PIE 则不彻底删除旧方案，以减少过早错过有潜力的搜索路径。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 总测试时计算预算约束

$$
\sum_{t=0}^{T-1}\sum_{i=1}^{n_t} k_t^{(i)}\leq N
$$

**符号说明**

- $T$：搜索迭代轮数。
- $t$：当前搜索轮次，取值为 $0$ 到 $T-1$。
- $n_t$：第 $t$ 轮被扩展的候选数量。
- $k_t^{(i)}$：第 $t$ 轮第 $i$ 个被扩展候选产生的后继数量。
- $N$：允许使用的总测试时计算预算，按生成或验证的候选数量计。

<div class="equation-explanation" markdown="1">

**直观理解**：该约束要求所有轮次、所有父候选产生的后继总数不能超过 $N$。因此不同控制器可以在相同资源下比较，差异主要来自它们把预算放在并行探索、连续扩展或候选保留的方式不同。<br>
**原文位置**：Appendix A；统一框架定义

</div>

</div>

<div class="equation-block" markdown="1">

#### PIE 的历史候选选择概率

$$
p_{t+1}(x)=\frac{\exp(f(x)/\tau)}{\sum_{x'\in\mathcal{H}_{t+1}}\exp(f(x')/\tau)}
$$

**符号说明**

- $p_{t+1}(x)$：候选 $x$ 在第 $t+1$ 轮被选作扩展对象的概率。
- $x$：历史候选方程。
- $\mathcal{H}_{t+1}$：截至第 $t+1$ 轮已经生成的全部候选历史集合。
- $f(x)$：验证器对候选方程 $x$ 给出的分数。
- $\tau$：softmax 温度参数，控制分数偏好与探索随机性之间的权衡。

<div class="equation-explanation" markdown="1">

**直观理解**：分数越高的历史候选，指数权重越大，因而更可能继续产生后继；但由于采用概率抽样，其他候选仍可能被重新探索。较小的 $\tau$ 更偏向高分候选，较大的 $\tau$ 通常带来更分散的选择。<br>
**原文位置**：第 2.2 节；Parallel Iterative Expansion（PIE）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未将该方法定义为需要更新语言模型参数的训练方法，也未给出新的参数优化损失。其优化对象是固定测试时计算预算 $N$ 下的搜索控制：通过选择 $n$、$k$、$g$、选择策略和剪枝策略，提高候选方程发现效果与验证效率；语言模型本身作为候选生成器使用。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 固定预算的统一控制框架**

每轮控制器由选择策略 $q_t$、扩展候选数 $n_t$、每个候选的分支数 $k_t^{(i)}$ 和剪枝算子 $\Pi_t$ 参数化，并满足总测试时计算约束 $\sum_{t=0}^{T-1}\sum_{i=1}^{n_t}k_t^{(i)}\leq N$。论文进一步采用时间齐次简化 $n_t\equiv n$、$k_t^{(i)}\equiv k$、$\Pi_t\equiv\Pi$，并定义搜索宽度 $w=nk$。

> 直观理解：该框架把 Best-of-N、顺序改写、树搜索和进化式搜索都看成“如何花费有限尝试次数”的不同方案，从而能够单独研究计算分配，而不是把复杂提示词或工程技巧的影响混在一起。

**2. Parallel Beam Search（PBeam）**

PBeam 将群体和预算平均划分到 $g$ 个组；每组选择全部当前前沿，生成 $k$ 个后继，并执行 $\mathcal{M}_{t+1}=\operatorname{Top}_{n/g}(\mathcal{M}_t\cup G_t;f)$。其中 $\operatorname{Top}_{m}(A;f)$ 表示按验证器分数 $f$ 从集合 $A$ 中保留得分最高的 $m$ 个元素。

> 直观理解：它是并行化的束搜索：每组同时扩展若干条当前最佳路径，然后只留下最好的固定数量。这样能控制候选规模并保持较强的利用已有高分结果的倾向。

**3. Parallel Iterative Expansion（PIE）**

PIE 不将未入选候选永久截断，而是维护历史集合 $\mathcal{H}_{t+1}=\mathcal{H}_t\cup G_t$，并以 $p_{t+1}(x)=\exp(f(x)/\tau)/\sum_{x'\in\mathcal{H}_{t+1}}\exp(f(x')/\tau)$ 对历史候选抽样下一轮扩展对象；其记忆状态更新为 $\mathcal{M}_{t+1}=\mathcal{H}_{t+1}$。

> 直观理解：PIE 像带有记忆的概率搜索：高分公式更容易再次被扩展，但低分公式并非完全消失。温度 $\tau$ 控制“偏向已知好方案”和“继续尝试较少探索方案”之间的平衡。

**训练与推理**

这是推理时搜索流程，而非模型训练流程。推理阶段输入科学任务、观测数据和初始候选，控制器循环执行候选选择、语言模型生成、验证器评分及状态更新，直到耗尽预算 $N$ 或完成预定迭代轮数 $T$，最后输出验证器评分最高或被保留的方程；给定摘录未说明初始候选的具体构造、提示模板、验证器分数的具体形式或最终候选的额外人工筛选步骤。

**复现信息**

复现实验所必需的抽象配置包括总预算 $N$、群体规模 $n$、分支数 $k$、分组数 $g$、搜索宽度 $w=nk$、PIE 温度 $\tau$、组内预算 $N/g$ 及并行提交验证任务的机制。PBeam 要求 $n/g$ 和相关预算能够按组分配；PIE 需要保存完整历史集合，因此其存储和验证管理不同于只保留前沿的 PBeam。摘录未明确报告模型、提示词、验证器实现、初始种子、具体超参数取值或停止条件，不能据此补充这些细节。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- LLM-SRBench 的 LSR-Synth Biology（Bio）域，共 24 个种群动力学任务。每个任务由 5,000 个合成样本生成，本地实现公开 4,000 个训练样本，其余用于留出测试；输入为时间与种群规模 $(t,P)$，输出为增长率 $dP/dt$。搜索只读取任务描述和训练集，Bio 是使用 gpt-oss-20b 开展主宽度—深度研究的核心数据集。
- LLM-SRBench 的 LSR-Synth Material Science（Material）域，共 25 个应力—应变任务。每个任务同样公开 4,000 个训练点，输入为应变与温度 $(\epsilon,T)$，输出为应力 $\sigma$；其隐藏符号定律与数值范围随任务变化。该域主要用于检验从 Bio 得到的计算分配规律能否跨科学领域泛化。
- 两个领域合计 49 个任务。每个任务包含自然语言说明、变量定义、可执行程序框架、训练集以及留出测试集；本地数据还含 $ood\_test$，但后者从不用于模型选择。模型需要生成 Python 程序，同时给出方程的函数形式和自由参数拟合器，而不是从一个封闭答案集合中选择结果。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**训练集 $\operatorname{Acc}_{0.1}$**

搜索过程唯一使用的适应度与父节点选择目标，衡量预测落入基准所定义的 $0.1$ 容差范围内的比例。它回答候选方程对已观察数据拟合得多好，并向搜索控制器提供反馈。 （越高越好，因为更高值表示更多训练点满足误差容差；但它不是符号结构完全恢复的直接证明，也不能单独保证留出集泛化。）

</div>
<div class="metric-item" markdown="1">

**留出测试集 $\operatorname{Acc}_{0.1}$**

每个同步迭代后仅用于记录当前历史最优节点的域内泛化表现，绝不反馈给搜索。它用于区分训练适应度提升与真正的未见样本预测改善。 （越高越好，因为表示候选方程在未参与搜索的数据上仍有更多预测满足容差。）

</div>
<div class="metric-item" markdown="1">

**NMSE、$R^2$ 与 combined_score**

评估器额外报告的诊断指标：NMSE 表示归一化均方误差，$R^2$ 表示解释输出变异的程度，combined_score 是基准特定的综合分数。原文摘录未给出 combined_score 的精确定义，且明确说明这些指标不作为搜索目标。 （NMSE 越低越好；$R^2$ 与 combined_score 通常越高越好。由于搜索始终优化训练集 $\operatorname{Acc}_{0.1}$，这些指标只能作为补充评价。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 在 LLM-SRBench 上固定预算并扫描不同宽度—深度分配

<div class="result-value" markdown="1">

作者报告搜索宽度 $w=nk$ 是主要的计算分配参数；相较之下，把预算分配给更深的连续改写并非实验中最关键的决定。所给摘录没有包含对应结果表、具体均值、标准差或显著性检验，因此无法量化宽度优势。

</div>

直观上，在验证器能可靠评价候选方程时，同一轮尝试更多彼此不同的方程，通常比只沿少数候选反复修改更有价值。这支持“探索—利用分配”是方程发现测试时扩展的核心问题，但并不证明宽搜索对所有预算、任务或验证器都必然最优。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On LLM-SRBench equation-discovery tasks, we find that search width is the dominant allocation parameter: the best width in our sweep generally increases with the compute budget, while the population--branching split and controller choice matter less.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 预算 $N$ 从 1 增至 128 时比较最优宽度

<div class="result-value" markdown="1">

作者报告扫描范围内的最佳宽度通常随计算预算增加而增大。原文使用“generally”而非无例外结论，且当前摘录未给出每个预算对应的最优 $w$，因此不能据此推出固定比例规律或精确的宽度选择公式。

</div>

增加预算后，不应默认把额外调用全部用于延长搜索链；实验趋势表明，较大预算也需要扩大并行探索面。这里得到的是经验性的配置规律，不是对任意模型、任意数据或超过 128 次预算的理论保证。

<div class="result-source" markdown="1">

来源：摘要；预算网格见附录 B.4 表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On LLM-SRBench equation-discovery tasks, we find that search width is the dominant allocation parameter: the best width in our sweep generally increases with the compute budget, while the population--branching split and controller choice matter less.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 比较不同宽度配置的实际运行效率

<div class="result-value" markdown="1">

作者声称适当选择搜索宽度还能通过提高并行度改善墙钟时间效率。所给摘录没有报告具体耗时、加速比、硬件配置或成本归一化结果，因而只能确认方向性结论。

</div>

总模型调用量相近时，更宽的配置可同时派发更多生成和评估任务，从而减少等待连续迭代的时间。不过，这种收益依赖 128 路模型调用和评估并发等运行环境；它不表示总计算量、API 成本或能耗下降。

<div class="result-source" markdown="1">

来源：摘要；异步执行与并发设置见附录 B.3、B.4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Appropriate width selection also improves wall-clock efficiency by increasing parallelism.

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

- 共享仿射初始化：所有 49 个任务和所有搜索组都从同一个最小二乘仿射模型开始。它是刻意设置的弱、领域无关起点，用于减少高质量人工初始方程对搜索比较的干扰。
- PBeam：按训练集 $\operatorname{Acc}_{0.1}$ 选择每组得分最高的有效节点，并在旧记忆与新子节点的并集中保留前 $s=n/g$ 个节点。它代表确定性的利用优先策略，适合检验集中追踪当前最优候选是否优于随机化探索。
- PIE：对截断到 $[-10,10]$ 的搜索分数做单位温度 softmax，并无放回地抽取父节点；记忆中保留更多历史候选。它代表随机化、探索性更强的控制器，与 PBeam 的比较用于判断控制器选择是否比宽度分配更重要。
- 固定预算下的不同 $(n,k)$ 配置：主扫描令 $g=1$，枚举满足 $nk\leq128$ 的二次幂组合，并从一次最大预算运行的检查点恢复 $N\in\{1,2,4,8,16,32,64,128\}$ 的结果。由于 $w=nk$ 决定每轮并行扩展数，而 $T$ 约随 $N/w$ 变化，这组比较直接构成宽搜索与深搜索的对照。

**实验想回答的问题**

- 在固定测试时计算预算 $N$ 下，如何在搜索宽度 $w=nk$ 与同步搜索深度 $T=\max(1,\lfloor N/(nk)\rfloor)$ 之间分配计算，才能更有效地发现可泛化的科学方程？
- 当总宽度相同或接近时，种群规模 $n$、分支因子 $k$、分组数 $g$ 以及控制器类型 PBeam/PIE 是否会显著改变结果；结论能否跨科学领域与语言模型骨干保持一致？

**实验实现**

主实验对每个模型—领域—随机种子组合运行固定的计算分配网格。PBeam 枚举 36 个满足 $nk\leq128$ 的二次幂 $(n,k)$ 配置；PIE 排除退化的 $(1,1)$ 及 $nk=128$ 的单步设置后使用 27 个配置。每次运行先执行到最大预算 128，再依据累计 $budget\_used\leq N$ 的最后检查点恢复较小预算结果。每个领域先对任务取平均，再对三个随机种子 $\{0,1,2\}$ 报告均值与标准差。主设置为 Bio 上的 gpt-oss-20b；Material 上的同一模型检验跨数据域泛化，Bio 上的 Qwen3-30B-A3B-Thinking-2507 检验跨模型泛化。解码温度为 0.7，最大生成长度为 16,384 token；模型调用与评估异步执行，全局并发上限均为 128。每个候选程序在独立 Python 子进程中运行，超时为 600 秒，且只允许 numpy、scipy 与 scikit-learn。测试集只用于日志，$ood\_test$ 不参与模型选择。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 固定总宽度后改变种群—分支拆分 $(n,k)$ | 作者声称，相比总宽度 $w=nk$，将相同宽度拆为较大种群、较小分支，或较小种群、较大分支，影响较弱。摘录只给出扫描设计，没有提供各配置的具体分数或差值。 | 该消融隔离了“同时保留多少父候选”与“每个父候选生成多少子节点”的作用。如果总宽度相近时结果也相近，就说明系统首先关心每轮总共尝试多少候选，而不是这些候选按何种家族结构产生；但缺少数值结果意味着无法判断差异是否统计上可忽略。 | 摘要；$(n,k)$ 扫描网格见附录 B.4 表 2<br><span class="experiment-evidence">On LLM-SRBench equation-discovery tasks, we find that search width is the dominant allocation parameter: the best width in our sweep generally increases with the compute budget, while the population--branching split and controller choice matter less.</span> |
| 固定 $N=128$，在竞争性宽度切片上改变分组数 $g$ | 分组消融覆盖宽度 32 的 $(32,1)$、$(16,2)$、$(8,4)$ 与宽度 16 的 $(16,1)$、$(8,2)$，并测试 $n$ 在 $\{1,2,4,8,16,32\}$ 中所有可行约数作为 $g$；每种算法形成 24 个配置。所给摘录没有报告分组对最终指标的方向或幅度，因此不能断言分组有效或无效。 | 分组把总种群划成若干相对独立的搜索子群，意图避免所有候选过早集中到同一路径。该设计控制了预算和高层宽度，用来检验“维持多个独立搜索盆地”是否带来额外收益；由于结果章节缺失，目前只能说明它测试什么，不能给出效果结论。 | 附录 B.4 表 2，G assignment<br><span class="experiment-evidence">Grouping ablation, performed only for gpt-oss-20b on Bio and Material.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work studies test-time compute allocation and verifier-guided search strategies for LLM-based scientific equation reasoning and discovery.; rule check: matched taxonomy keywords; top rule score=5.0
- 全文指纹：`197ee42671c6ff9eb3abea0b2074d65b3eb42328ed6ec1d0bdc6f643081f948f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
