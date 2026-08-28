---
title: "[论文解读] From Atomic to Agentic: Towards Interpretable Evaluation of LLMs' Agentic Mathematical Capabilities"
description: "[arXiv 2608.26950][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.26950"
announcement_date: "2026-08-28"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:41:16.571912+00:00"
source_sha256: "ebb563f2ee32a26a843eed1654c01a396cabfac5d65a45e3d52922ab210b38f0"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM Agent"
  - "LLM 其他"
  - "大语言模型"
  - "数学推理"
  - "智能体能力"
  - "过程级评测"
  - "数学原子能力"
  - "可解释评测"
  - "多模态数学"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.26950</p>

# From Atomic to Agentic: Towards Interpretable Evaluation of LLMs' Agentic Mathematical Capabilities

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Jiayi Kuang, Yinghui Li, Yunze Song, Keyu Chen, Zhifeng Shen, Yangning Li, Yidong Wang, Di Yin, Ruizhi Qiao, Xing Sun, Kai Jin, Ying Shen, Liang Lin, Philip S. Yu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Sun Yat-sen University；Affiliation: Tencent Youtu Lab；Affiliation: University of Illinois Chicago；Affiliation: Pengcheng Laboratory</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26950v1) · [PDF 下载](https://arxiv.org/pdf/2608.26950v1) · **关键词** 大语言模型, 数学推理, 智能体能力, 过程级评测, 数学原子能力, 可解释评测, 多模态数学<br>
**代码**: [https://github.com/Eternity-gaga/Agentic-Math-Bench](https://github.com/Eternity-gaga/Agentic-Math-Bench)

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

本研究位于大语言模型数学推理与智能体评测的交叉领域。传统数学基准通常给模型一道文本或含图题目，再依据最终答案是否正确计算总体准确率；这种结果级评测能反映解题成功率，却难以判断失败发生在理解图形、制定计划、执行计算还是检查修正等环节。与此同时，数学智能体开始通过规划、行动执行、自我反思以及工具调用来组织多步推理，因此评测对象也应从“是否答对”扩展为“模型在解题过程中具备哪些可复用的智能体能力”。本文据此把数学解题过程拆成原子能力，并将其与规划、行动和反馈三类智能体行为对齐，以形成可解释的过程级能力画像。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**智能体推理**

指模型不只直接生成答案，而是围绕目标动态执行规划、具体操作和结果反思等步骤。这里关注的是基础大语言模型自身是否具备支撑这些步骤的内在能力，而非某个外部智能体系统的整体性能。

</div>
<div class="concept-item" markdown="1">

**数学原子能力**

指复杂数学解题过程中可分离、可复用的基本能力单元，例如从图形提取变量的空间感知、选择解题策略的建模以及执行计算。原子化分析使评测能够定位具体能力瓶颈，而不只记录整道题是否做对。

</div>
<div class="concept-item" markdown="1">

**过程级评测**

指直接考查或标注推理过程中的局部步骤与行为，而非仅核对最终答案。其目标是区分计划错误、执行错误和反馈失效，并检查推理逻辑是否可靠。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文提出 AgenticMathBench，用于评估大语言模型在数学推理中的内在智能体能力。评测输入是覆盖纯文本与多模态情境的数学问题及其过程级任务；任务按照规划、行动和反馈三类智能体功能组织，并进一步对应结构化的数学原子能力。模型需要完成相应的局部判断、生成或执行任务，评测输出不是单一的最终答案准确率，而是按行为与原子能力划分的细粒度能力表现，从而比较即使端到端正确率相近的模型是否具有不同的智能体能力结构。该设置默认复杂数学解题可以分解为多个可复用步骤，而且这些步骤能够与智能体行为建立有意义的对应关系。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **GAUSS**: GAUSS沿结构化技能维度组织数学评测，可生成比总体准确率更具解释性的能力画像；但原文指出此类评测仍主要由整题驱动，对原子技能在何处失败及其如何交互的可见性有限。AgenticMathBench进一步把数学原子能力操作化，并与智能体行为建立对应。
- **Math-Shepherd 与 PRM800K 风格的过程奖励模型**: 这类方法对单个推理步骤评分，可用于候选答案重排、强化学习或多智能体讨论，说明过程信号对数学推理有价值；本文所针对的缺口则是缺少一个统一基准，专门以细粒度过程指标评估规划、行动和反馈三类能力。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型正从直接生成数学答案转向能够规划步骤、执行操作并根据反馈修正方案的智能体式推理。然而，在把基础模型嵌入复杂智能体系统之前，研究者需要判断模型是否真正具备这些内在能力，以及失败发生在规划、执行还是反思环节。若只检查最终答案，即使模型碰巧答对，也无法确认其推理逻辑是否可靠；答错时也难以定位应改进的具体能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **终局答案导向的数学基准**：向模型提供完整数学问题，并主要依据最终答案是否正确来计算总体表现。这类评测适合衡量端到端解题成功率，但通常把中间推理过程视为不可分解的整体。
- **数学技能分解型评测**：将数学问题按若干技能或能力类别组织，以观察模型在不同类型任务上的表现。部分数据集尝试覆盖更多细粒度技能，但原文指出，它们往往只涉及较窄的能力集合，或缺少大规模、系统化的测量框架。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 最终正确率无法可靠区分“严密推理后得出答案”与“过程存在错误但偶然答对”，也不能在失败时定位具体步骤，因此对模型诊断和智能体能力改进的指导价值有限。
- 已有技能评测很少把数学中的原子能力与智能体的原子行为建立系统对应关系，因而难以判断瓶颈究竟属于规划、动作执行还是反馈修正，也不足以比较端到端准确率相近模型的真实智能体能力结构。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种面向数学推理过程、同时覆盖文本与多模态情境的可解释评测框架：该框架应把可复用的数学原子能力映射到规划、行动和反馈等核心智能体功能，并通过细粒度任务形成可比较的能力画像，而非只给出单一的最终正确率。

</div>
<div markdown="1"><span>核心问题</span>

基础大语言模型是否具备参与数学智能体框架所需的内在规划、行动与反馈能力，以及如何通过过程级评测识别不同模型在这些能力上的优势和瓶颈？

</div>
<div markdown="1"><span>作者直觉</span>

复杂数学解题与智能体工作流都可以拆成较小、可重复使用的步骤。例如，几何题可能依次要求从图形提取关系、选择建模策略并完成计算，这分别体现不同阶段的能力。因而，与其只看最后答案，不如逐步检查模型能否制定方案、正确执行并发现或修复错误；这种“原子能力—智能体行为”对齐有望把笼统的成败转化为可解释、可干预的诊断结果。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

AgenticMathBench（AMB）不是直接根据最终答案判断数学能力，而是把数学求解过程拆成可复用的原子能力，并将这些能力与智能体的三类功能——规划、行动、反馈——交叉组织。给定数学问题、可选的图像信息或部分求解轨迹，AMB分别要求模型选择并排序所需能力、执行单一原子子任务、判断和修正已有轨迹，输出能力集合、步骤计划、计算或形式化结果、错误诊断及修复建议等过程级结果。其核心设计是将“会不会做出最终答案”转化为“是否知道下一步该做什么、能否完成该步、能否发现并修正错误”，从而隔离诊断不同的 agentic 数学能力。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 统一数学原子能力体系

研究者先汇总并比较已有能力定义，再进行合并、细分和筛除，并经数学专家咨询后形成三级能力体系：基础概念与计算、高级推理与应用、数学元认知。体系包含符号识别、概念理解、计算、空间感知、形式化、演绎与归纳推理、数学建模、定理应用和自我反思；“新知识学习”虽被列出，但因单次测试难以评估而暂未纳入。

<div class="method-step__io" markdown="1">

**输入**：既有数学基准、数学解题数据，以及关于基础计算、几何、证明、建模和元认知能力的文献定义。<br>
**输出**：一个用于标注数据和组织任务的数学原子能力集合，以及每个问题对应的多标签能力描述。

</div>

**直观理解**：这一步像把一道复杂数学题拆成“读懂符号、列式、计算、证明、检查”等可单独测试的小技能。这样后续不只知道模型答错了，还能定位它缺的是哪一种能力。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 收集、规范化与生成过程数据

研究者从大量数学基准中筛选覆盖不同能力的数据，统一输入与目标格式，并执行过滤、去重、下采样和多标签能力标注。对于规划和反馈所需的动态过程，系统采用规范的“计划—行动—反馈”范式合成轨迹：先生成全局计划，再逐步执行原子能力、验证中间结果，并依据反馈调整后续行动，随后进行最终答案检查、人工过程质量筛选和能力覆盖多样性筛选。

<div class="method-step__io" markdown="1">

**输入**：覆盖手写符号、初等和高级解题、几何、定理证明、竞赛和奥林匹克数学的既有数据集，以及原始解答或问题图像。<br>
**输出**：单原子 Action 任务、文本与多模态数学轨迹，以及从轨迹中抽取的能力集合、完整计划、截断后的下一步目标、错误步骤和修复目标。

</div>

**直观理解**：原始数据通常只有题目和答案，不能直接说明模型怎样思考。作者因此把它们改造成统一的“小任务”，并额外生成带有中间步骤和检查过程的解题记录，像为每道题制作可逐步回放的实验录像。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造规划、行动与反馈任务

规划任务包括能力规划、解题规划和下一步规划：模型分别选择所需能力集合、生成有序的能力—子目标序列，或根据当前状态预测下一步。行动任务把单一原子能力从完整解题中解耦出来，要求模型独立完成符号识别、概念理解、计算、空间感知、形式化、演绎与归纳推理、数学建模或定理应用；反馈任务则要求模型判断轨迹正误、定位最早错误及错误类型，并提出与正确修复策略一致的下一步。

<div class="method-step__io" markdown="1">

**输入**：统一后的数学问题、原子能力标签、合成或筛选后的参考轨迹，以及部分截断轨迹。<br>
**输出**：规划输出为能力集合、完整有序计划或下一步 $(a_{t+1},g_{t+1})$；行动输出为规范化数学表达式、概念或关系集合、数值结果、Lean4 定理声明、证明提纲、建模要素或定理应用轨迹；反馈输出为正确性标签、错误位置与类型、以及修复动作和理由。

</div>

**直观理解**：三类任务分别对应智能体的“先安排工作”“实际完成一件工作”“检查并纠错”。它们被分开测试，因此模型即使最终答案相近，也可能暴露出规划混乱、某个基础技能薄弱或不会纠错等差异。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按目标类型进行过程级评测

对集合或分类目标使用精确匹配、准确率、精确率、召回率和 F1；对数值计算使用数值精确匹配，对符号计算使用计算机代数系统等价性；对形式化结果检查 Lean 编译和语义对齐；对完整计划、证明提纲、建模约束目标、定理应用轨迹和修复理由，在规则难以可靠判定等价性时使用 LLM 评审覆盖性、一致性或对齐程度。规划的下一步同时评估能力准确率和子目标语义相似度。

<div class="method-step__io" markdown="1">

**输入**：模型对上述文本或多模态任务的预测结果，以及参考能力标签、参考轨迹和可执行形式化结果。<br>
**输出**：各原子能力、各 agentic 功能及其交叉任务的细粒度分数和能力画像，而非单一最终答案正确率。

</div>

**直观理解**：不同答案不能用同一把尺子衡量：数字可直接比对，Lean 定理可尝试编译，开放式证明步骤则需要判断是否覆盖关键内容。最后得到的是一张能力体检表，而不是一个只说明“答对或答错”的总分。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 有序解题计划

$$
\pi=\big[(a_{1},g_{1}),(a_{2},g_{2}),\dots,(a_{T},g_{T})\big]
$$

**符号说明**

- $\pi$：模型生成的有序解题计划。
- $a_t\in\mathcal{A}$：第 $t$ 步选择的数学原子能力；$\mathcal{A}$ 是全部原子能力集合。
- $g_t$：第 $t$ 步需要完成的具体子目标。
- $t$：计划中的步骤索引。
- $T$：计划总步骤数。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把一个解题计划表示为有序的“能力—子目标”对。它不仅要求模型说出要用哪些技能，还要求决定先后顺序和每一步要完成什么；因此可以检验规划是否符合数学上的依赖关系，而不把实际计算错误混入规划能力。<br>
**原文位置**：第 2.1.2 节 Planning，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 反馈函数

$$
f:(\text{problem},\tau_{\leq t})\rightarrow\{\text{status},\text{type},\text{sugg}\}
$$

**符号说明**

- $f$：反馈函数，将问题及其已有轨迹映射为诊断结果。
- $\text{problem}$：待解决的数学问题。
- $\tau_{\leq t}$：截至第 $t$ 步的部分或完整求解轨迹。
- $\text{status}$：轨迹或当前状态的正确性状态。
- $\text{type}$：检测到的错误类型。
- $\text{sugg}$：建议采取的修复动作或后续步骤。

<div class="equation-explanation" markdown="1">

**直观理解**：该式将反馈明确为一个输入—输出过程：模型读取题目和目前已经发生的步骤，先判断是否正确，再指出错误属于什么类型，并给出如何继续或修复的建议。它把“检查答案”扩展为对过程的监控和纠错。<br>
**原文位置**：第 2.1.2 节 Feedback，公式（2）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文将 AMB 定义为评测基准和数据构造框架，没有给出用于训练模型的统一参数优化目标、损失函数或反向传播过程。因此训练目标为“不适用”；论文的核心是对现有模型进行推理时评测，而不是训练一个新的基础模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 原子能力—智能体功能交叉建模**

AMB 沿两个轴组织评测：数学原子能力轴与 agentic 功能轴。规划被定义为能力选择、排序和下一步决策，行动被定义为单一原子能力的隔离执行，反馈被定义为对已有轨迹进行状态监控、错误定位和修正；因此评测的是两个轴的交集，而不是简单给数学技能重新命名。基础与高级能力主要支撑行动，元认知能力主要支撑反馈，而规划在全局上协调多种能力。

> 直观理解：同一个技能在不同阶段扮演的作用不同。例如“定理应用”可以是执行某一步，也可以在检查时帮助判断原步骤是否合理。把“技能是什么”和“智能体何时使用它”分开，才能测出模型的过程组织能力。

**2. 计划—行动—反馈轨迹生成器**

给定问题，规范轨迹首先生成包含所需原子能力、具体子任务和执行顺序的全局计划；随后逐步执行选定能力，验证中间结果，并根据反馈动态调整后续动作。完整轨迹经过自动最终答案检查、人工推理质量筛选以及覆盖步骤和能力多样性筛选；原始过程还被截断于不同完成比例，用于构造下一步规划和反馈样本。

> 直观理解：该模块模拟一个会做计划、会执行、会检查的数学智能体，但评测时又把三种行为拆开。这样既能产生有上下文的过程样本，也能单独询问模型某一个关键决策。

**3. 异构目标评估器**

评估器根据目标结构选择不同判定机制：集合目标使用集合匹配指标，数值和符号表达式使用精确匹配或 CAS 等价性，形式化目标使用 Lean 编译与语义对齐，开放式过程目标使用 LLM-as-judge 评估覆盖性、一致性和对齐性。反馈评估分别计算正确性判断、错误步骤定位、错误类型分类，以及修复理由和修复动作与参考策略的一致性；论文还报告了针对评审模型的稳健性检查和人工验证。

> 直观理解：评估器不会强行把所有过程答案转成字符串比较，而是根据答案性质选择合适的验证方式。对于机器难以自动判定的证明或修复建议，则让评审模型检查是否覆盖关键内容、逻辑是否一致。

**训练与推理**

数据构造阶段先统一既有数据格式并标注原子能力；对规划和反馈，按照规范的计划—行动—反馈范式合成数学轨迹，再进行自动答案检查、人工过程质量筛选和多样性筛选。对部分过程结构化目标，原文说明使用 GPT-4o 将原始解答改写为中间表示，并进行规范化和过程检查。推理阶段，模型接收问题、文本或图像输入，或接收被截断的已有轨迹，分别生成能力集合、完整计划、下一步、单原子任务答案、正确性判断、错误定位或修复建议；随后由对应的自动指标、Lean/CAS 工具或 LLM 评审器评分。

**复现信息**

为保证公平解释，AMB 将文本和多模态输入纳入同一任务组织方式，并把不同目标转换为统一的任务—输入—目标输出—指标模式。规划中的完整计划由 LLM 评审其步骤覆盖、子目标质量和逻辑一致性，下一步规划则在轨迹完成比例为 $20\%$、$50\%$ 和 $80\%$ 的截断点上测试；行动不评估自我反思，因为论文将其归入反馈。原文未明确报告统一的模型训练超参数、训练轮数、优化器或生成解码设置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 论文提出的过程级数学智能体基准：包含文本与多模态任务，并按规划、反馈、动作三大类组织。规划考查完整解法规划、下一步规划等能力；反馈考查结果判断、错误定位和修复建议；动作进一步覆盖计算、概念理解、形式语言、前向推理、数学建模与定理使用等原子能力。当前节选未给出样本规模、训练/验证/测试划分及各子任务题量，因而无法判断置信区间或类别均衡性。
- MATH：作为端到端数学解题基准，与过程级智能体得分并列用于检验“最终答案正确率是否代表智能体能力”。当前节选未说明采用的具体划分、提示方式或评测样本数。
- AIME25：作为较高难度的端到端数学解题基准，与规划、反馈和动作得分对照。它在本实验中的作用不是训练数据，而是提供传统结果导向能力的参照；当前节选未明确报告具体题目范围、评测协议或是否允许工具调用。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（Accuracy/Acc）与精确率（Precision/Prec.）**

准确率衡量结果判断、分类或任务完成正确的样本比例；精确率衡量模型给出的正类判断中有多少正确。不同动作子任务使用的具体指标并不完全相同，不能在缺少任务定义时将各列直接视为同一种百分比。 （越高越好，因为更高值表示更多样本被正确判断或更少产生错误的正类预测。）

</div>
<div class="metric-item" markdown="1">

**F1 与集合 F1（Set-F1、Var-F1）**

F1 是精确率和召回率的调和平均，用于同时惩罚漏检与误检；集合 F1 比较预测元素集合与标准集合，变量 F1 则用于数学建模中的变量识别。规划任务也报告 F1，以评价预测规划内容与标注之间的综合匹配程度。 （越高越好，因为只有精确率与召回率都较好时，F1 才会较高。）

</div>
<div class="metric-item" markdown="1">

**完全匹配、编译/对齐和 Pass@k（EM、Compile、Align、Pass@k）**

EM 要求输出与标准答案完全一致；Compile 检验形式化输出能否通过编译或解析；Align 检验形式表达与目标语义或结构是否一致；Pass@k 表示至多考察 $k$ 个候选时至少一个通过测试的概率。当前节选未给出各指标的完整判定细则及 $k$ 的取值。 （均为越高越好，分别表示严格匹配、形式有效、结构或语义一致，以及候选中出现有效解的可能性更高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 端到端数学成绩与过程级智能体能力的对照

<div class="result-value" markdown="1">

Table 5 显示，GPT-5.2 与 Gemini-3-Pro 的 MATH 都为 $100.0$，但规划得分分别为 $41.0$ 与 $34.2$，反馈得分分别为 $53.7$ 与 $48.3$，动作得分分别为 $89.3$ 与 $80.6$。另一个更明显的例子是 GLM-4.7：MATH 为 $98.8$、AIME25 为 $95.7$，但规划、反馈和动作仅为 $29.0$、$29.7$ 和 $64.5$。作者据此主张，接近或很高的最终答题成绩不能唯一决定过程级能力画像。

</div>

这项比较直接回答了基准的核心问题：只看最终答案会把“怎样得到答案、能否发现错误、能否精确执行结构化步骤”压缩成一个结果分数。相同的 MATH 成绩仍可对应不同的规划、反馈和动作表现，因此过程级测评具有额外诊断价值。不过，这只是跨模型的描述性比较，不能单独证明某种训练方式导致了能力下降，也不能排除提示、模型接口或评审器偏好造成的影响。

<div class="result-source" markdown="1">

来源：Table 5；Section 4.1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GPT-5.2 | 100.0 | 99.0 | 41.0 | 53.7 | 89.3
Gemini-3-Pro | 100.0 | 95.7 | 34.2 | 48.3 | 80.6
GLM-4.7 | 98.8 | 95.7 | 29.0 | 29.7 | 64.5

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 反馈能力：结果判断、错误定位与修复建议

<div class="result-value" markdown="1">

作者报告，即使商业模型在区分正确与错误推理轨迹时也低于 $65\%$ 准确率；错误定位比结果判断更难，而最高层次的修复建议表现进一步下降。文中没有在当前节选中给出 Table 3 的逐模型完整数值，因此不能确定哪一模型在各反馈子任务上最佳。

</div>

反馈不是简单判断最终答案对错，而是要从复杂轨迹中找出导致失败的具体步骤和原因，再给出可执行的下一步修复。模型可能会说“这里需要修改”，却无法把诊断转化为明确操作，这说明语言解释看似合理不等于具备闭环纠错能力。低于 $65\%$ 的结果支持该任务具有挑战性的作者判断，但在缺少人类基线、评审一致性和完整分项数据时，不能把全部误差都归因于模型推理缺陷。

<div class="result-source" markdown="1">

来源：Section 3.3；完整分数据称见 Table 3，但当前节选未提供

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Most models achieve moderate accuracy in distinguishing correct from incorrect trajectories. Even commercial models remain below 65% accuracy, indicating that outcome assessment is non-trivial when reasoning traces are complex.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 动作能力：从计算到形式化、建模和定理使用的结构化执行

<div class="result-value" markdown="1">

Table 4 表明，商业模型整体较强且相对均衡，但没有单一模型在所有列上都占优。例如 Gemini-3-Pro 的计算列为 $88.7$、概念列为 $56.0$、前向推理准确率为 $100.0$、定理 Pass@k 为 $99.0$；DeepSeek-V3.2 的对应计算与概念列为 $84.7$ 和 $52.4$，同时在形式语言、前向推理及定理任务上达到 $97.7$、$99.4$ 和 $100.0$。数学专用模型也并非必然稳健：Qwen2.5-Math-72B-Instruct 在计算和概念列仅为 $6.0$ 与 $6.2$。

</div>

动作评测关注模型能否把计划准确落实成数学操作，而不只是能否描述思路。结果显示，一些强模型在形式化和推理执行上接近满分，但概念理解仍是共同短板；数学专门化标签也不保证在该基准的动作格式下表现良好。该结果支持“能力画像不均衡”的结论，但不同列使用 EM、F1、准确率、编译率或 Pass@k 等不同指标，不能把各列数值直接当作同尺度难度比较；Qwen2.5-Math 的异常低分也需要结合输出格式兼容性进一步核查。

<div class="result-source" markdown="1">

来源：Table 4；Sections 3.4 and 4.3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Gemini-3-Pro | 88.7 | 56.0 | 72.0 | 100.0 | 93.7 | 94.7 | 92.2 | 84.7 | 99.7 | 99.0
DeepSeek-V3.2 | 84.7 | 52.4 | 97.7 | 99.4 | 91.4 | 93.1 | 88.3 | 83.0 | 99.0 | 100.0
Qwen2.5-Math-72B-Instruct | 6.0 | 6.2 | 48.9 | 2.5 | 2.0 | 7.8 | 36.0 | 23.1 | 90.8 | 5.3

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前节选未报告过程级数据集规模、子任务分布、数据划分、人工基线、置信区间或显著性检验，也未完整展示 Planning 的 Table 2、Feedback 的 Table 3 和多模态的 Table 17。因此，结果能够支持模型间的描述性差异，但不足以判断差异是否具有统计稳健性，或是否受任务样本构成影响。
- 开放式任务依赖 DeepSeek-V3 充当评审器。温度设为 $0$ 只能降低随机性，不能消除评审模型的系统偏好、与被评模型的家族相关性或对特定表达风格的偏爱。当前节选还未完整给出人工一致性验证及评审器敏感性分析，因而尤其需要复核异常低分和模型间的小幅差异。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 通用开源模型，包括 Llama-4、DeepSeek-V3.2、Qwen3 和 GLM-4.7 等。该组用于考查通用指令或推理训练能否自然迁移到数学智能体的过程能力，并比较不同规模和推理增强策略产生的能力画像。
- 多模态开源模型，包括 Qwen3-VL、InternVL3.5 和 DeepSeek-VL2。它们是文本与视觉数学任务上的参照，用于判断过程级能力是否能跨模态保持；但当前节选未提供对应的 Table 17 数值。
- 数学专用开源模型，包括 Qwen2.5-Math-72B-Instruct 和 DeepSeek-Math-V2。该组是关键对照，因为它能检验面向数学最终答案或解题轨迹的专门训练是否足以形成规划、反馈和结构化执行能力。
- 商业模型，包括 GPT-5.2、Claude-Sonnet-4.5-thinking 和 Gemini-3-Pro-Preview。它们代表较强的闭源系统，用于估计当前高性能模型的能力上界，并与强开源模型比较能力的均衡性。

**实验想回答的问题**

- 现有模型在数学智能体的规划、反馈与动作执行三类过程能力上分别表现如何；不同能力维度是否会呈现可区分、非均衡的能力画像？
- 端到端数学正确率能否可靠代表过程级智能体能力，还是相近的最终答题成绩可能掩盖显著不同的规划、反馈和执行缺陷？

**实验实现**

实验覆盖通用开源、数学专用开源和商业模型，并对多模态模型另行评测。过程开放、可能存在多条合理路径的任务使用 LLM-as-a-judge：论文明确以 DeepSeek-V3 作为评审模型，并将温度固定为 $0$，以减少随机性。作者认为，完整解法规划和修复建议不适合仅用字符串匹配，因为不同但正确的推理路径可能被误罚。当前节选只显示评审流程说明的一部分，未完整提供评审提示、防护措施、人工一致性验证、解码配置、重复运行次数与统计显著性检验；实现细节被指向 Appendix G.1。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- Figure 5 与 Appendix G.3/G.4 的案例分析显示，一些端到端成绩很强的模型会把多步推理直接压缩为最终答案，并表现出较弱的状态跟踪；在反馈任务中，它们可能标出错误附近的步骤，却没有追溯到造成后续失败的因果源头。作者通过 case card 公布输入题目、展示给模型的轨迹、期望格式、原始输出和诊断结果，以提高质性分析的可审计性。该案例能说明典型失败模式，但单个案例不能估计该错误在整个数据集中的发生频率。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces a process-level benchmark for evaluating LLM mathematical reasoning through agentic planning, action, and feedback capabilities.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`ebb563f2ee32a26a843eed1654c01a396cabfac5d65a45e3d52922ab210b38f0`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
