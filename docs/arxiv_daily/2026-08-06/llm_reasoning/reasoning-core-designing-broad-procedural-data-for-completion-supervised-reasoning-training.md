---
title: "[论文解读] Reasoning Core: Designing Broad Procedural Data for Completion-Supervised Reasoning Training"
description: "[arXiv 2608.05148][LLM Reasoning] 本文研究如何把大规模、可验证的程序生成推理题设计成真正有效的补全式监督微调数据，并以 Reasoning Core 验证紧凑答案、难度控制和语义审计的重要性。"
arxiv_id: "2608.05148"
announcement_date: "2026-08-06"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:52:08.793190+00:00"
source_sha256: "63fa34c49da954a9f9669af94187f1990d618ce3a1aabff2d183f4a2e22013c7"
tags:
  - "LLM Reasoning"
  - "程序化数据生成"
  - "补全监督微调"
  - "语言模型推理"
  - "可验证推理"
  - "语义评分器"
  - "难度控制"
  - "训练效用"
  - "合成数据审计"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.05148</p>

# Reasoning Core: Designing Broad Procedural Data for Completion-Supervised Reasoning Training

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Damien Sileo, Valentin Lacombe, Dimitri Kachler</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Univ. Lille, Inria, CNRS, Centrale Lille, UMR 9189 - CRIStAL, F-59000 Lille, France</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.05148v1) · [PDF 下载](https://arxiv.org/pdf/2608.05148v1) · **关键词** 程序化数据生成, 补全监督微调, 语言模型推理, 可验证推理, 语义评分器, 难度控制, 训练效用, 合成数据审计<br>
**代码**: [https://github.com/sileod/reasoning-core](https://github.com/sileod/reasoning-core)

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

本文研究如何把大规模、可验证的程序生成推理题设计成真正有效的补全式监督微调数据，并以 Reasoning Core 验证紧凑答案、难度控制和语义审计的重要性。

**不用术语来说**：程序可以自动生成大量推理题，并同时算出或检查答案，但“答案可验证”不等于“适合拿来训练语言模型”：题面可能不足以唯一确定答案，答案格式可能过长或不稳定，题目可能太易或太难，不同任务混合后也可能互相稀释。论文要解决的是，在训练词元预算固定的情况下，怎样设计和表示这类数据，才能让模型从中获得可迁移的推理能力。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者构建 Reasoning Core：包含 50 个程序生成器，覆盖数学、逻辑、规划、状态跟踪、形式语言、结构化数据、游戏、因果和代码等领域，并统一提供语义评分器、难度控制以及面向监督微调、评测和强化学习的任务接口。
- 作者把“语义有效性”与“训练效用”明确区分，并通过受控集合比较及仓库级审计表明：生成题目具有正确、可识别的答案只是必要条件，紧凑的规范化目标、合适的难度范围以及生成、题面、目标与评分器之间的一致性同样决定监督训练价值。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于语言模型推理训练与合成数据设计研究。程序化生成器按照明确规则自动构造数学、逻辑、规划、状态跟踪、形式语言、结构化数据、游戏、因果和代码问题，并可同步计算或验证答案，因此能够低成本地产生大量新样本，还能直接调节题目结构与难度。已有广域程序化任务集主要被用作强化学习中的可验证环境，即根据最终答案是否正确提供结果奖励；但近期研究强调，强化学习的效果受其之前形成的能力和表示制约，因此本文转而考察更基础的监督数据层：在统一的补全监督微调条件和固定训练预算下，怎样设计、表示并混合程序化样本，才能为模型提供有效且可迁移的推理训练信号。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**程序化生成器**

由程序依据显式规则自动采样问题、生成标准答案并控制难度的系统。它可以持续产生新实例，但程序能够生成和判分并不意味着题面一定充分、答案表示一定适合学习。

</div>
<div class="concept-item" markdown="1">

**补全监督微调**

给定题面或提示，使用预先确定的目标文本训练语言模型继续生成正确补全，通常通过最大化目标序列的条件概率实现。本文比较的是这种监督训练用途，而不是各任务集原本可能采用的强化学习训练流程。

</div>
<div class="concept-item" markdown="1">

**语义有效性与训练效用**

语义有效性指渲染后的题目能够唯一或明确地确定一个正确目标，并且评分器能正确识别它；训练效用指在指定模型、训练目标、数据量和混合配置下，接触该数据能否改善下游表现。前者是必要的数据质量条件，但本文强调它并不足以保证后者。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是由多个程序化任务生成器组成的广域推理数据集。每个生成器接收任务配置及难度设置，输出自然语言或结构化的题目实例、用于补全监督的紧凑目标，以及能够按语义检查模型回答的评分机制；不同任务通过统一接口进入训练、评测或可验证强化学习流程。核心比较在匹配的补全监督协议下进行：控制基础模型设置、训练时长和训练预算，对 Reasoning Core、Procedural Warmup、Reasoning Gym、SynLogic 以及不加入程序化数据的条件进行比较，并用留出下游任务、自由生成、能力保持和仓库审计诊断训练效果与数据正确性。问题的关键假设是：程序上可验证的样本并不会自动成为优质监督数据，其价值还取决于题面是否充分决定答案、目标是否紧凑且一致、难度是否落在模型可学习的范围内，以及单项任务加入异质混合后是否仍能贡献有效信号。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Procedural Warmup**: 面向补全监督训练的直接相关基线，汇集 Dyck 任务等形式语言和抽象程序化序列，以紧凑的合成补全进行较早阶段的训练。Reasoning Core 将这一设定扩展到更异质的任务集合，并在匹配训练干预下考察生成器级设计差异。
- **Reasoning Gym 与 SynLogic**: 二者提供广泛或可扩展的算法、逻辑推理环境，主要服务于带可验证结果奖励的强化学习。本文将它们置于统一的补全监督协议中与 Reasoning Core 比较，用于检验原生面向强化学习设计的可验证任务是否同样适合作为监督微调数据。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

语言模型后续推理能力在很大程度上受监督阶段或更早训练分布的影响，而人工编写并核验大量多样化推理题成本较高。程序生成器能够按需产生新样本、直接计算或验证目标，并控制题目结构和难度，因此有望在固定词元预算内提供可扩展的推理监督；真正的需求是把这种生成能力转化为稳定、有效且可审计的补全式监督训练信号。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **窄域程序化预热**：Procedural Warmup 使用范围较窄的抽象程序序列进行训练预热，再继续常规语言模型训练；已有工作表明，这类预热可能改善后续训练，但它没有直接回答覆盖多种推理领域的程序数据应如何组织和表示。
- **面向结果奖励强化学习的可验证推理环境**：Reasoning Gym 和 SynLogic 提供较广泛的程序化推理任务，由验证器根据最终答案是否正确给出结果奖励，主要服务于强化学习。它们证明了程序任务适合可验证训练，但其设计目标并非在统一的补全监督协议下最大化监督微调收益。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有广域程序集合主要围绕验证器支持的强化学习构建，缺少在相同基础模型、训练目标、数据剂量和训练时长下，对其作为补全式监督微调数据的系统比较；因此无法判断哪类集合设计能够更好地强化后续训练的起点。
- 程序能够生成并验证答案，并不保证样本具有训练效用：题面可能无法唯一确定预期目标，目标表示可能冗长，难度可能偏离模型的可学习区间，生成逻辑、渲染文本、目标和评分器还可能存在细微错配。这些问题会浪费固定词元预算，甚至让形式上“正确”的任务难以产生下游迁移。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未建立一套面向广域补全式监督训练的程序数据设计与评估框架，尤其缺少对题面可判定性、目标表示、难度校准、异质任务混合效应和语义一致性的联合考察，也缺少多个程序集合在匹配训练条件下的直接证据。论文的实验范围最多覆盖 3B 参数模型，且未检验同一程序集合先用于监督微调、再用于强化学习的顺序训练，因此更大规模和跨训练阶段的结论仍属开放问题。

</div>
<div markdown="1"><span>核心问题</span>

在模型、训练目标、数据剂量和混合设置明确的条件下，广域可验证推理样本应当如何生成、表示、控制难度并接受审计，才能成为有效的补全式监督微调数据，而不只是形式上可由验证器判分的数据？

</div>
<div markdown="1"><span>作者直觉</span>

监督训练直接模仿给定目标，因此每个词元是否清楚表达应学习的决策非常关键。若题面唯一确定答案、输出采用紧凑且统一的规范形式、难度落在模型既不能轻易猜中又仍可学习的区间，那么有限预算会集中在核心推理映射上；再用语义评分和审计检查生成、展示、答案与判分是否一致，就能减少错误或含混监督。换言之，作者的切入点不是单纯增加题量，而是提高每个生成样本作为训练信号的密度与可靠性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Reasoning Core 是一个面向完成监督微调（SFT）的程序化推理数据集合与生成框架。每个生成器接收随机种子和难度配置，构造具有可验证语义的任务实例，随后将结构化实例渲染为零样本提示，并同时产出结构化参考答案、元数据和语义评分函数；训练时使用适合自回归预测的确定性规范答案，评估时则允许所有语义等价的答案。整体方法的重点不是只扩大题目数量，而是联合设计问题分布、难度控制、答案序列化、外部求解器和数据审计，使生成的样本既多样又适合完成监督训练。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多领域程序化生成

生成器根据任务特定的递归规则、语法规则、动作模式、状态转移规则、图结构或程序结构采样问题实例；可调参数包括推导深度、计划长度、变量数量、分支因子和符号结构规模。全局难度标量通过可覆盖的映射函数转换为这些参数，而不是只选择固定难度预设。

<div class="method-step__io" markdown="1">

**输入**：随机种子、任务生成器、任务类别和难度配置；当前版本包含数学、形式证明与符号操作、逻辑与概率推理、规划与游戏、状态与指称跟踪、图与约束、形式语言与转换、集合与结构化数据、代码九组共 $50$ 个生成器。<br>
**输出**：一个具有可复现实例定义的结构化任务对象，通常包含问题结构、可计算语义、难度元数据和用于复现的种子；实验清单还记录精确样本与行为哈希。

</div>

**直观理解**：可以把生成器理解为一套出题程序，而不是一批手工题目。调节难度时，程序会改变题目的实际结构，例如增加推理层数或变量数，而不只是把文字表面写得更复杂。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提示与规范答案构造

系统将问题元数据与提示渲染分离，生成不含少样本示例的零样本指令，以便把上下文和词元预算更多用于独立采样的问题。针对完成监督目标，系统选择确定性的规范答案序列化方式，例如对集合答案采用字典序，对规划、证明构造和程序综合避免由多个等价前缀引起的不一致后缀，并优先使用数字、标签、集合、表达式、证明行索引、计划或短程序等紧凑答案。

<div class="method-step__io" markdown="1">

**输入**：结构化任务对象、问题元数据和任务对应的参考语义。<br>
**输出**：用于训练的提示与单一规范完成目标，以及可供验证的结构化参考答案；规范目标负责稳定监督，结构化答案保留更完整的语义信息。

</div>

**直观理解**：同一道题可能有多个意思相同的正确写法，但模型训练需要一个明确的示范答案。这里先选定一种标准写法作为教学文本，同时不把其他等价写法误判为错误。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 语义评分与外部求解

评分函数不只比较字符串，而是按任务语义判断正确性：集合答案忽略顺序，lambda 项允许变量重命名，计划通过执行验证，证明候选通过编译检查，生成程序通过测试。外部工具通过统一集成层调用，并配合依赖固定、Docker 环境、执行隔离、缓存已接受实例和将验证器失败与模型答错分开处理。

<div class="method-step__io" markdown="1">

**输入**：模型生成的候选答案、结构化参考答案、任务语义和必要的外部求解器或运行时。<br>
**输出**：语义有效性评分、验证器状态和用于生成数据检查、自由生成评估或在线奖励的评分结果；验证器失败不会被当作模型获得正确答案。

</div>

**直观理解**：训练示范可以采用统一格式，但测试时要检查答案真正表达的内容。例如计划必须真的能执行，程序必须真的通过测试，不能因为文字看起来相似就算正确。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 仓库级审计与回归修正

系统结合模型辅助审查、人工裁决、手工复现、最小化案例和回归测试检查生成、渲染、目标与评分之间的一致性。模型判断不被视为事实依据；对奖励不为 $1$ 的案例进行裁决，并持续修复已确认问题，最终将问题加入回归测试，同时以相同流程回溯审计外部数据集合。

<div class="method-step__io" markdown="1">

**输入**：生成器源代码、渲染后的提示、参考目标、评分器、抽样实例和审计中发现的异常案例。<br>
**输出**：经过修正和回归测试覆盖的生成器、评分器与数据实例，以及记录审计范围和确认案例的材料。

</div>

**直观理解**：程序自动出题并不等于题目天然正确：可能是题面、标准答案或判分程序彼此不一致。因此，作者把发现的错误缩小成可重复的小案例，再加入自动测试，防止同一问题再次出现。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：论文方法章节将训练设定描述为完成监督微调：每个样本提供一个提示和一个规范完成目标，模型在教师强制条件下学习生成该目标。给定固定计算预算，单个训练样本通常只对应一次教师示范，因此作者通过宽问题分布和紧凑答案增加可覆盖的独立问题数量；语义评分主要用于数据验证、自由生成评估和在线奖励，而不是把所有语义等价答案都作为训练参考序列。所给章节未提供明确的损失函数或优化目标公式，因此不能进一步声称其采用了特定形式的交叉熵、奖励函数或多任务加权目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 宽覆盖生成器与难度控制**

Reasoning Core 通过 $50$ 个生成器覆盖九类任务，并强调改变语义结构而非仅改变表面文本。生成器可以暴露递归深度、计划长度、变量数、分支因子等任务相关控制量；全局难度值通过生成器可覆盖的函数映射到这些控制量，约定难度最高至 $5$ 时对所有生成器仍具有实际可行性。

> 直观理解：该模块决定“题目考什么”和“题目有多难”。它允许不同任务用不同方式增加难度，因此比所有任务共用固定的题目模板更能形成有结构的训练分布。

**2. 面向 SFT 的答案设计与语义评分器**

训练侧为适应单个教师强制完成目标，使用适合自回归预测的确定性规范答案，并偏好短答案以降低格式和偶然排序带来的监督成本。评估侧使用任务语义评分器接受等价答案，包括集合的顺序不变性、lambda 项的变量重命名等价、计划执行、证明编译和程序测试。

> 直观理解：这个模块把“教模型写哪一种答案”和“判断模型是否真正答对”分开。训练需要稳定、紧凑的示范，测试则不能因为模型采用另一种合理表达就误判。

**3. 可复现的工具集成与语义审计**

外部求解器和运行时通过公共集成层与 Docker 镜像接入，并固定依赖、隔离可执行任务、缓存可接受实例、区分验证器故障和答案错误。仓库验证结合已知案例测试、生成分布诊断、模型辅助审查、人工裁决、最小案例复现和回归测试；相同审计也应用于实验中的外部集合，但作者明确指出外部审计是回溯性的、非独立且非盲审的。

> 直观理解：程序化数据的可信度取决于整条链路，而不只是出题器。该模块让其他人能够复现实例和工具环境，也把“评分器出错”与“模型回答错误”区分开。

**训练与推理**

训练阶段首先从各生成器按记录的种子和难度配置采样实例，再将实例渲染为零样本提示，并以确定性规范答案作为完成监督目标。模型通过 SFT 学习从提示生成目标答案；在相同的训练协议下，不同程序化集合可以被匹配比较。推理或自由生成评估阶段，模型接收任务提示并输出候选完成，候选由对应语义评分器检查，而不是只与规范字符串进行精确匹配；计划、证明和程序等任务分别通过执行、编译或测试判断。生成器和评分器也可用于数据集验证与在线奖励，但所给章节未明确报告在线强化学习的具体训练流程。

**复现信息**

复现所需的关键工程约束包括：将生成器与评分器独立测试；记录精确样本、难度配置和行为哈希；对外部求解器固定依赖并使用 Docker 镜像；隔离不安全的可执行任务；缓存已接受实例；将超时、版本漂移、格式错误和主机不兼容等验证器失败单独记录，禁止其产生正确性得分。提示采用零样本指令，外部集合保留其原始渲染方式，因此不同集合的答案格式和对 SFT 的适配程度可能并不相同。审计中，模型辅助审查使用 GPT-5.5 High 及后续 GPT-5.6 High 检查代码、提示、目标和评分器，另用 Claude Haiku 4.5 在难度 $0$ 和 $1$ 的渲染样本上进行抽查；异常案例先由 Claude Opus 4.6、后续 Claude Opus 4.7 协助裁决，再经人工复核。原文强调，模型判断从未作为事实依据，确认的问题必须手工复现并由回归测试覆盖。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 训练主数据流：FineWeb-Edu 文本与 DOLCI 指令及对话数据等量混合。DOLCI 含逐步推理、工具使用和对话监督，因此 main-only 是经过整理的监督微调基线，而非未经训练的基座或纯原始文本基线。各程序化集合替换主数据流中 20% 的 prompt-plus-answer token，用于检验辅助程序化监督的边际作用。
- 主要推理评测：DROP、LogiQA、ARC-Challenge 与 BBH-test。DROP 侧重文本中的离散推理并以 F1 评价生成答案；LogiQA 与 ARC-Challenge 是选择题，分别测试逻辑阅读和科学推理；BBH-test 使用 BBH 中保留的算法型任务。四者还组成 Reasoning NLL compound，用于汇总域外答案预测迁移。BBH 的非算法型任务另作开发集，只用于任务开发和筛选，不计入正式 held-out 集合比较。
- 能力保持评测：MMLU-other 与 DOLCI。MMLU-other 是排除数学、形式逻辑和计算机科学后的 47 个 MMLU 学科宏平均，降低与程序化训练领域直接重合的程度；DOLCI 评估模型在原有指令训练分布上的答案 NLL。两者组成 Retention compound，用于判断推理收益是否以更广泛知识或指令能力退化为代价。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**相对答案 NLL 降幅 $\Delta_{\mathrm{NLL}}(A;E)$**

比较加入辅助集合 $A$ 的模型与配对 main-only 模型在评测分布 $E$ 上的答案负对数似然；其定义为 $100\left(1-\operatorname{NLL}_{E}(M_{\mathrm{main}+A})/\operatorname{NLL}_{E}(M_{\mathrm{main}})\right)$。NLL 衡量模型给正确答案分配的概率，尤其适合小模型准确率接近地板或选择题准确率变化仅约 1 至 2 个百分点时捕捉部分概率改善。 （越高越好；正值表示辅助数据使正确答案的 held-out NLL 低于匹配的 main-only 条件，即模型对正确答案赋予更高概率。）

</div>
<div class="metric-item" markdown="1">

**任务原生 F1 或准确率**

DROP 使用 F1 衡量预测答案与参考答案的词项重合；LogiQA、ARC-Challenge、BBH-test 和 MMLU-other 使用相应任务原生的准确率或评分。论文主要在 3B 模型上报告这些行为指标，因为此时它们比小模型上的近地板或近随机结果更有区分度。 （越高越好；它直接反映最终答案是否正确，但不能像 NLL 那样识别正确答案概率尚未跨过决策阈值的细微变化。）

</div>
<div class="metric-item" markdown="1">

**任务原生自由生成 reward**

在不提供目标答案的情况下，让模型自由生成并由任务专用 evaluator 或语义 scorer 评分，用于诊断训练后的可学性及零样本可解性。该指标与域外迁移不同：高 reward 可能仅表示模型掌握了狭窄输出空间，低 reward 也可能来自任务过难或数据问题。 （通常越高越好，因为它表示生成结果更符合任务判定标准；但论文强调 reward 饱和不等价于更强的域外推理迁移。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### SmolLM3-3B-Base，训练 2,400 步，20% 辅助 token，5 个种子；Reasoning Core 与配对 main-only 的任务原生行为指标比较。

<div class="result-value" markdown="1">

Reasoning Core 在四项 Reasoning 指标上均高于 main-only：DROP F1 从 $33.1\pm1.0$ 升至 $41.7\pm0.8$，LogiQA 准确率从 $46.8\pm0.6$ 升至 $47.8\pm0.7$，ARC-Challenge 从 $50.7\pm0.3$ 升至 $51.3\pm0.5$，BBH-test 从 $43.6\pm1.1$ 升至 $45.3\pm1.1$。

</div>

作者据此主张 Reasoning Core 的 NLL 改善能够转化为最终答案质量改善，而不只是概率校准变化。分析上，DROP 的提升最明显，其余任务的绝对增幅较小；该结果证明的是在指定 3B 基座、训练混合与 2,400 步预算下的配对增益，并不证明所有模型规模、训练时长或数据占比下都保持同一排序。

<div class="result-source" markdown="1">

来源：Section 5.1；具体数值见 Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At 3B and 2,400 updates, Reasoning Core improves all Reasoning metrics over the paired main-only continuation.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### SmolLM3-3B-Base，2,400 步、20% 辅助 token；四种程序化集合在各 held-out benchmark 上的配对相对答案 NLL 降幅。

<div class="result-value" markdown="1">

Reasoning Core 在 DROP、ARC-Challenge 和 MMLU-other 等多个数据集上取得较强且一致的正迁移，例如 DROP 为 $23.39\pm1.62$、ARC-Challenge 为 $9.21\pm0.84$、BBH-test 为 $29.17\pm2.42$、MMLU-other 为 $8.06\pm0.62$。相比之下，Procedural Warmup 在 DROP、ARC-E 和 ARC-Challenge 上分别为 $-1.41\pm0.83$、$-0.74\pm0.67$ 和 $-0.47\pm0.43$，显示程序化数据本身不保证广泛迁移。

</div>

作者的核心结论不是所有程序化任务都有效，而是集合设计会显著改变迁移方向与覆盖面。Reasoning Core 的优势跨越阅读、逻辑、科学推理和非形式学科保持指标，支持其广覆盖设计；但 Core/Gym 等量混合在 LogiQA 和 BBH-test 上更高，说明 Reasoning Core 并非每一个单项 benchmark 的绝对最优，也不能把集合级优势归因于某一个生成器。

<div class="result-source" markdown="1">

来源：Appendix Table 5，列顺序为 DROP、LogiQA、ARC-E、ARC-C、BBH-test、MMLU-other、DOLCI

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Reasoning Core 23.39 ± 1.62 4.40 ± 0.99 13.21 ± 1.17 9.21 ± 0.84 29.17 ± 2.42 8.06 ± 0.62 0.41 ± 0.08

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### SmolLM3-3B-Base，2,400 步、5 个种子；同时考察 Reasoning Core 的推理迁移与 DOLCI、MMLU-other 能力保持。

<div class="result-value" markdown="1">

Reasoning Core 的 MMLU-other 准确率为 $43.6\pm0.5$，高于 main-only 的 $42.9\pm0.2$；DOLCI 的表中 $\Delta$NLL 为 $-0.003\pm0.001$，变化幅度很小。附录按“相对 NLL 降幅越高越好”的定义报告 DOLCI 为 $0.41\pm0.08$，同样表示没有明显的训练分布保持损失。

</div>

这项控制针对一种替代解释：程序化训练可能只是让模型偏向短答案格式，并牺牲长篇指令能力。MMLU-other 和 DOLCI 没有显示相应退化，因此结果更符合“获得推理迁移而未明显遗忘主训练能力”的解释。不过 DOLCI 与主训练流直接相关，只能检验训练分布保持，不能代表所有开放式生成、安全性或现实知识能力。

<div class="result-source" markdown="1">

来源：Section 4.2；数值见 Table 2 与 Appendix Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Retention therefore asks whether procedural supervision is acquired at the expense of broader capability.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主结论来自固定的补全监督设置：辅助 token 占比主要采用 20%、最大长度为 1,024、训练最多 2,400 步，且只覆盖四个基座模型。集合排序会随模型与训练时长变化，因此不能直接外推到更大模型、强化学习、不同上下文长度或更长期训练。
- 任务设计分析主要是隔离任务运行上的观察性相关分析；中等 reward、长度、网格格式与迁移之间的关系即使经过标准化或长度控制，也可能受任务语义和难度等混杂因素影响。逐步 rationale 的负结果同样只覆盖解析与图路径等特定任务，不能推广为对所有思维链监督的否定。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Main-only：只使用相同主数据流继续训练，并与每个辅助条件共享随机种子、数据顺序、更新次数及优化配置；它是估计程序化辅助数据边际贡献的核心对照。
- Reasoning Gym：覆盖大量异质程序化任务，是规模较大且常用的程序化推理数据基线；论文还利用其 95 个任务的隔离训练面板分析可学性、长度和格式因素。
- SynLogic：以合成逻辑任务为主，与 Reasoning Core 的广领域设计形成对照，用于检验更集中于形式逻辑的集合能否产生同等广泛的迁移。
- Procedural Warmup：已有程序化预热方案的重实现版本；作者排除了属于纯续写而非 prompt-answer 任务的 cellular automata，以便统一转换为补全监督格式并进行公平比较。

**实验想回答的问题**

- 在总更新步数、主训练数据、辅助数据占比、随机种子和优化配置均匹配的补全监督协议下，Reasoning Core 是否比不加入程序化数据的 main-only 条件以及 Procedural Warmup、Reasoning Gym、SynLogic 三种程序化集合带来更强的域外推理迁移，同时不损害一般能力保持？
- 程序化任务的哪些属性决定训练效用：任务在训练中是否可学、目标是否紧凑、样例长度与辅助 token 剂量如何影响迁移，以及语义正确的逐步算法轨迹是否一定优于紧凑答案？

**实验实现**

实验使用 SmolLM2-135M、SmolLM2-360M、OLMo-1B 和 SmolLM3-3B-Base 四个基座，将四种程序化集合统一转换为 prompt-answer 样例并采用相同补全监督目标。主数据流与程序化数据按 token 混合，辅助数据占 prompt-plus-answer token 的 20%；该比例先在 Reasoning Gym 上以 10%、20%、40% 扫描，并依据 2,400 步时的 BBH 验证 NLL 确定。最大序列长度为 1,024，过长样例直接丢弃，以免截断末尾监督答案；任务在支持的难度级别间均匀采样并去重。实验覆盖 300 至 2,400 个更新步，所有条件采用配对种子，同一种子内共享数据顺序和优化配置，学习率经初步 Reasoning Gym 实验选定后对所有集合固定，不按集合单独调参。主要 3B、2,400 步结果汇总 5 个种子；迁移轨迹使用 3 个种子的均值及标准误。选择题按完整选项文本而非紧凑标签计算 NLL，以减弱短答案格式带来的虚假优势。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Reasoning Gym 全集合与按 BBH-development NLL 选出的 50 任务子集比较；SmolLM3-3B-Base，2,400 步、20% 辅助 token。 | 筛选子集将 LogiQA 的相对 NLL 降幅从 $2.57\pm0.89$ 提高到 $4.64\pm0.84$，但 DROP 从 $20.33\pm2.99$ 降至 $19.11\pm2.21$、ARC-Challenge 从 $3.54\pm1.12$ 降至 $2.08\pm1.00$、BBH-test 从 $23.89\pm2.50$ 降至 $23.40\pm1.97$、MMLU-other 从 $4.99\pm0.29$ 降至 $4.70\pm0.66$。 | 该消融隔离“按单一开发诊断筛任务”是否能提高整体迁移。结果只在 LogiQA 上改善，多数其他指标下降，说明开发集上的任务效用不能均匀外推，缩窄任务混合还可能损失互补性。它不意味着筛选一定无效，而是说明以 BBH-development NLL 单独排序并取前 50 个任务不足以优化多数据集平均迁移。 | Section 5.1；具体数值见 Appendix Table 5<br><span class="experiment-evidence">The subset improves LogiQA but degrades most other metrics relative to the full collection, suggesting that BBH-development utility does not transfer uniformly across evaluations and that narrowing the task mixture can reduce aggregate transfer.</span> |
| OLMo-1B 上 18 个相同 Reasoning Gym 任务的 300 步配对控制：按样例概率混合与按 token 份额匹配。样例匹配实际仅含 13.1% 辅助 token，token matching 将抽样概率从 $0.20$ 提高至 $0.293$，达到目标 20%。 | token matching 使 BBH 平均改善 $+1.77$ 个百分点，95% 区间为 $[1.15,2.48]$，且 18/18 个任务均改善；但 FineWeb 表现与样例长度的相关系数仍从 $-0.85$ 变为相近的 $-0.87$，没有消除长度关系。 | 该控制把“较长样例导致每次训练看到的辅助样例数更少”与“长格式本身代价更高”区分开。补足辅助 token 剂量普遍改善 BBH，说明预算不足确实会低估任务效用；然而长度与 FineWeb 保持的负相关几乎不变，说明长样例仍有独立成本。由于仅覆盖 18 个 OLMo-1B 任务和 300 步训练，该结论主要是机制诊断，而非所有集合的普遍因果定律。 | Appendix D.4，Token-matching control；数值汇总见 Table 8<br><span class="experiment-evidence">Token matching raises the example probability to .293 to obtain the intended 20% auxiliary-token share.</span> |

**定性案例**

- 逐步 rationale 的负面案例：解析任务把 Earley chart parser 的连续操作写成目标，图路径任务则逐步记录 BFS 或 Dijkstra 的前沿扩展、距离更新和前驱选择。虽然这些轨迹在语义上正确，但在 BBH-development 与 FineWeb NLL 上持续劣于紧凑答案；匹配训练预算、取消预算匹配以及缩短轨迹均未逆转排序。作者将其解释为：可迁移能力可能更接近对语法结构或可行路径整体形态的把握，而不是机械复现求解器账本。该案例只否定“正确算法轨迹必然是更好监督目标”，并不证明 rationale 监督普遍有害。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops and audits broad procedurally generated training data specifically for completion-supervised improvement of language-model reasoning.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`63fa34c49da954a9f9669af94187f1990d618ce3a1aabff2d183f4a2e22013c7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
