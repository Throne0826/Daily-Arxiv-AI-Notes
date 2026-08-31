---
title: "[论文解读] MAIL: Memory-driven, Adaptive, Incremental, and Literature-grounded Framework for Hypothesis Generation in Chemistry"
description: "[arXiv 2608.28315][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.28315"
announcement_date: "2026-08-31"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:41:14.091463+00:00"
source_sha256: "f45efba3efc12c4b90de06bf812425c1f411eaf6122afef94d2b669a677ba3fe"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "假设生成"
  - "大型语言模型"
  - "化学假设"
  - "文献驱动推理"
  - "时间推理"
  - "迭代检索"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.28315</p>

# MAIL: Memory-driven, Adaptive, Incremental, and Literature-grounded Framework for Hypothesis Generation in Chemistry

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Mahdi Babaei, Xueshen Li, Yutao Kuang, Jolene P. Reid, Yu Gan</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Biomedical Engineering, Stevens Institute of Technology, Hoboken, NJ 07030, USA；Affiliation: Department of Chemistry, University of British Columbia, Vancouver, BC V6T 1Z1, Canada；Affiliation: Department of Bioengineering, University of Maryland, College Park, MD 20742, USA；Affiliation: Artificial Intelligence Interdisciplinary Institute at MarylandUniversity of Maryland, College Park, MD 20742, USA * Corresponding authors；Affiliation: Artificial Intelligence Interdisciplinary Institute at MarylandUniversity of Maryland, College Park, MD 20742, USA</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28315v1) · [PDF 下载](https://arxiv.org/pdf/2608.28315v1) · **关键词** 假设生成, 大型语言模型, 化学假设, 文献驱动推理, 时间推理, 迭代检索<br>


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

本文研究化学科学假设生成，即利用大型语言模型（LLM）从已有化学文献和研究背景中提出可检验、具有新颖性且符合化学机理的研究假设。与一般文本生成不同，化学假设不仅要表达一个新的研究方向，还应说明研究对象、预期现象或结果以及可能的作用机制，并尽量具备实验可行性。MAIL将这一任务视为文献驱动的时间推理过程：系统按时间检索先前文献，在多轮生成中保留和压缩已有信息，并依据模型对当前假设的反馈持续修订。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大型语言模型（LLM）**

LLM是从大规模文本中学习语言规律和知识表达的模型，可根据给定背景、文献和提示生成或评价科学文本。本文将其用作文献综合、机理推理和假设修订的核心推理器。

</div>
<div class="concept-item" markdown="1">

**文献驱动假设生成**

该任务要求系统从科学文献中抽取概念、方法和机制，再组合成尚未被直接提出但具有科学依据的新假设。高质量输出应同时满足概念新颖性、化学合理性、机制清晰性和实验可检验性。

</div>
<div class="concept-item" markdown="1">

**时间接地的迭代推理**

时间接地表示检索和使用文献时考虑其先后顺序，使生成的假设建立在目标时间点之前可获得的知识上。迭代推理则表示假设不是一次生成，而是在多轮新文献和反馈作用下逐步更新。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定研究问题或研究背景、截至相应时间的化学文献以及当前假设和其反馈，系统需要输出一个新的、可检验的化学研究假设。MAIL的设定不依赖推理阶段的人类逐轮评价：在第$t$轮，系统利用背景和检索文献生成当前假设$h_t$，再由LLM产生内部反馈$f_t$；下一轮根据$f_t$、当前假设和新检索文献继续生成$h_{t+1}$。文献检索应随假设和反馈变化，而不是固定使用一个预先整理的灵感语料库；最终目标是生成结构连贯、机理上可信并具有科学价值的假设。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$h_t$**

第$t$轮生成的当前研究假设。

</div>
<div class="notation-item" markdown="1">

**$f_t$**

LLM在第$t$轮对假设$h_t$产生的内部反馈，用于指出问题并指导后续修订。

</div>
<div class="notation-item" markdown="1">

**$I^{(t+1)}$**

第$t+1$轮检索到的新文献或文献信息集合，其内容会受到前一轮假设和反馈的影响。

</div>
<div class="notation-item" markdown="1">

**$t$**

迭代轮次，表示假设生成、内部评价和文献更新所处的时间步骤。

</div>

</div>

**直接相关的工作**

- **MOOSE-Chem**: MOOSE-Chem通过多阶段灵感检索与组合构造化学假设，说明检索和概念组合对化学假设生成的重要性；但本文指出，这类方法主要依赖预定义或相对静态的文献语料，未充分实现根据当前假设和反馈动态改变后续检索。MAIL试图以跨轮次的查询依赖检索、压缩记忆和反馈驱动修订弥补这一不足。
- **SciMON与Scideator**: SciMON和Scideator通过重组概念或科学要素支持假设生成，代表组合式和交互式科学创意发现方法。相较之下，MAIL将假设形成组织为连续的时间推理轨迹：每轮保留当前假设、生成内部反馈并检索新的时间先前文献，从而减少对人工交互、手工启发式分解和人工排序规则的依赖。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

化学文献持续增长，蕴含了大量可用于科学发现的知识，但研究者和自动化系统难以高效追踪思想如何随时间演化，并将分散的文献证据转化为具有机制解释和实验可行性的全新假设。化学假设不仅要有新颖性，还必须符合化学原理、明确预期机制与结果，因此单纯生成语言上合理的文本并不足以支持后续研究。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **静态文献检索与概念组合方法**：这类方法从预先选定的文献语料库中检索启发材料，再通过多阶段检索、概念重组或科学要素组合生成假设。例如，MOOSE-Chem进行多阶段灵感检索与组合，SciMON和Scideator则重组不同概念或科学侧面。
- **时间演化、迭代搜索与约束引导方法**：这类方法建模科学实体和关系的时间变化，或通过多轮搜索、层次化扩展、领域反馈和约束逐步构造假设。例如，时间知识图谱追踪知识演化，ChemReasoner使用量子化学反馈优化催化剂设计，其他方法则采用目标驱动或约束引导的智能体。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 许多方法依赖静态或人工预先筛选的启发语料库、固定启发式规则或手工设计的排序流程，检索内容不能根据当前假设及其推理状态动态变化，因而可能限制可探索的文献范围与假设新颖性。
- 已有工作通常只解决知识演化建模、预定义语料组合、交互式概念重组、层次化细化或特定领域优化中的某一部分，尚未充分整合跨多个科学数据库、按时间区间进行的查询相关检索，以及跨轮次压缩记忆和反馈驱动的自然语言修订；部分流程还依赖人工参与，削弱了大规模自动化能力。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种能够将多源科学数据库中的查询相关文献检索、时间约束、跨轮次压缩记忆和反馈驱动假设修订统一起来的自动化框架。具体而言，系统需要让后续轮次的检索响应前一轮生成的假设及其反馈，而不是始终从固定语料或固定规则中获取灵感；同时还应在没有推理阶段人工评价的情况下，持续提高假设的新颖性、机制深度和领域一致性。

</div>
<div markdown="1"><span>核心问题</span>

能否将化学假设生成建模为一个以时间为基础、由记忆驱动并由文献支撑的多轮推理过程，使大型语言模型根据当前假设、内部反馈和新检索文献，自动生成更加新颖、机制上可信且具有实验意义的后续假设？

</div>
<div markdown="1"><span>作者直觉</span>

科学假设通常不是一次性从文献中直接抽取的结论，而是在已有背景、逐步获得的新证据和对当前想法的反思之间不断演化。MAIL的切入点是保留当前假设及其压缩记忆，让模型在下一轮根据自身反馈重新检索时间上相关的文献，再进行综合与修订。直观地说，当前假设会反过来决定下一步应寻找什么证据，而新证据又会改变假设的方向；这种闭环有望比一次性生成或固定语料组合更充分地探索化学机制与潜在研究路径。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MAIL将化学假设生成建模为一个由文献与记忆驱动的迭代推理过程，而不是一次性生成。系统以研究问题和时间上可用的先前文献为输入，先生成候选假设，再通过结构化评价发现其有效性、新颖性、具体性和科学意义方面的不足，随后检索能够弥补这些不足的启发文献，并据此反复修订，最后从不同轮次的候选假设中选择最有潜力者。直观地说，MAIL像一名会持续读新论文、记录批评意见并修改研究构想的研究者：每一轮都不是简单重写，而是根据问题缺口补充机制、方法或实验设计。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 研究问题与初始文献驱动的假设生成

模型根据研究问题和文献内容提出初始研究假设，并将已有知识组织为后续推理可使用的概念路径与记忆。该过程强调从时间上较早的文献出发，以模拟历史上基于先前知识形成新研究方向的情境。

<div class="method-step__io" markdown="1">

**输入**：研究问题、时间上可用的化学文献及其检索结果，以及基础生成模型。<br>
**输出**：一个或多个初始化学研究假设，以及与其相关的文献、概念和推理记忆。

</div>

**直观理解**：系统先像研究者做文献综述一样理解问题，再提出一个可检验的研究猜想，而不是凭空写出新颖句子。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 结构化反馈与假设缺陷诊断

模型从有效性、新颖性、具体性和意义等维度审查当前假设，识别其机制不清、实验结构不足、与背景问题不一致或科学可行性较弱等缺陷。反馈结果被累积到记忆中，作为下一轮检索和修订的条件。

<div class="method-step__io" markdown="1">

**输入**：当前假设、研究问题、相关背景及评价提示。<br>
**输出**：针对当前假设的结构化反馈、需要修复的具体弱点，以及保留的有效内容。

</div>

**直观理解**：这一步相当于请评审先指出“哪里不够好、为什么不够好”，让后续修改有明确目标，而不是盲目润色。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 上下文感知的启发文献选择

模型选择恰好能够修复已识别弱点的启发论文，优先考虑能提供机制、方法或概念，并能提升假设新颖性、具体性或合理性的文献。该选择不是固定使用同一静态灵感语料库，而是随当前假设和反馈动态改变；每个查询使用的论文数量$K$可调节。

<div class="method-step__io" markdown="1">

**输入**：当前假设、上一轮反馈、已有记忆和候选文献集合。<br>
**输出**：用于下一轮修订的相关启发论文及其选择理由。

</div>

**直观理解**：如果评审说假设缺少反应机制，系统就专门寻找能补充该机制的论文，而不是每次随机推荐相同的参考文献。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 反馈约束下的迭代假设修订

模型整合至少一个与当前缺陷相关的机制或方法，保留上一版本的有效部分，并生成更具体、具有机制解释且可实验检验的假设。该过程重复多个轮次；文中图3考察了从第1轮到第3轮的性能变化，最终从不同轮次产生的候选中进行选择。

<div class="method-step__io" markdown="1">

**输入**：上一轮假设、结构化反馈、新选定的启发论文和累积记忆。<br>
**输出**：逐轮改进的假设序列，以及供最终决策比较的候选假设。

</div>

**直观理解**：每一轮都像“提出方案—接受批评—查找针对性证据—修改方案”，复杂科学构想因此逐步形成，而非依赖单次生成。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告MAIL是否进行新的参数训练、专门的损失函数或端到端优化目标。根据所给章节，MAIL主要表现为基于提示、检索、记忆、反馈和迭代推理的框架；因此不能据此推断存在参数级训练目标。实验中使用相同的底层生成器和自动评价器进行主要比较，以减少框架差异之外的影响。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 动态上下文感知检索与记忆**

MAIL维护随迭代更新的概念路径和累积记忆，并根据当前假设及反馈动态选择相关文献。与依赖静态启发语料库的方法不同，检索上下文会随假设缺陷、已有知识和新文献持续变化，从而为下一轮推理提供针对性材料。

> 直观理解：它不仅记住读过什么，还记住当前假设缺什么，并据此改变下一次查文献的方向。

**2. 反馈驱动的多阶段精炼**

系统将假设评价、缺陷识别、启发论文选择和假设重写组织成循环，并要求修订结果回应反馈、吸收新文献中的至少一个相关机制或方法，同时保留先前版本的有效内容。实验中的消融分别移除迭代精炼和反馈推理，用于检验这种循环是否真正贡献性能。

> 直观理解：该模块把“生成”变成有检查、有证据补充和有目标修改的过程，因此更适合需要机制与实验设计的化学假设。

**3. 结构化提示与候选决策**

不同阶段使用专门的提示约束输出格式和决策标准：评价阶段按有效性、新颖性、意义和潜力审查；文献选择阶段要求论文直接帮助修复弱点；修订阶段要求生成简洁、机制清楚且可测试的假设；最终选择阶段综合研究问题匹配、经验支持和科学价值。提示优化作为独立组件在消融实验中被移除，以评估其作用。

> 直观理解：提示不是泛泛地要求模型“想一个好点子”，而是把每个阶段的任务、输入和判断规则写清楚，减少输出跑题或过于笼统。

**训练与推理**

所给章节未说明MAIL的独立训练流程、训练数据划分、参数更新方式或优化器设置。推理时，系统输入研究问题及时间上可用的文献，生成初始假设；随后循环执行结构化反馈、针对性启发文献选择和假设修订，并利用累积记忆保持跨轮次的信息连续性，最后选择整体质量最优的候选假设。

**复现信息**

为公平解释结果，应注意主要比较使用相同的底层生成器和自动评价器；开放权重模型实验则在每个模型系列内部比较MAIL与MOOSE-Chem，因此不应把不同模型系列的绝对分数直接混为一谈。文中在TOMATO-Chem上测试每次查询检索$K\in\{1,3,5,10\}$篇论文，$K=5$取得所报告的最佳结果；不过所给章节未明确报告检索器、记忆的数据结构、提示模板全文、候选数量、轮次外的生成参数或人工筛选流程。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- TOMATO-Chem：公开基准数据集，包含51篇论文，覆盖有机化学、聚合物化学等领域。每个样本提供背景问题、背景综述、两篇带有启发理由的论文标题、目标假设及其主要要点；背景和启发材料经过整理以避免目标泄漏。其作用是模拟研究者先给出问题和简要综述、再要求模型提出假设的协作场景。来源：第4.1节。
- HN-NS：作者新整理的高新颖性数据集，包含50篇近期发表于Nature和Science的化学研究论文，覆盖电化学、生物催化和材料科学。该数据集针对概念关系稀疏、科学理论快速演化以及摘要中不显著的副反应或次要观察等困难，测试模型能否超越常见文献模式进行跨领域推理。每个样本具有与TOMATO-Chem相同的结构化标注。来源：第4.1节。
- 专家评价子集：从每个数据集各抽取25个假设，共进行50次博士级有机化学家评审；评审比较MAIL与MOOSE-Chem的输出，并采用双盲方式。该子集不是新的生成数据集，而是用于检验化学合理性、可行性、新颖性、完整性、科学影响和广泛用途的人工评价设置。来源：第4.2节和第5节。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**MIOS（Main Idea Overlap Score）**

衡量生成假设与历史目标假设在核心科学主张和机制上的重合程度，不评价文风、篇幅或表达质量；它主要回答模型是否恢复了目标发现的中心思想。 （越高越好，因为更高分表示与目标假设的核心思想和机制更一致；但它衡量的是历史思想恢复能力，不等同于独立原创性。）

</div>
<div class="metric-item" markdown="1">

**MPOS（Main Points Overlap Score）**

衡量生成假设覆盖目标假设中预先定义的方法学要点的程度，主要反映输入、条件、方法和可观测结果等关键要素是否被涵盖。 （越高越好，因为更高分表示覆盖了更多目标方法要点；但它不单独证明生成方案已经完成实验验证。）

</div>
<div class="metric-item" markdown="1">

**专家综合评价分**

由博士级有机化学家依据表1的七个维度进行评价：化学合理性、物理可行性、技术新颖性、概念新颖性、完整性、科学影响和广泛用途；各维度采用0—2分量表并汇总为总体分数。 （越高越好，因为它表示专家认为假设更合理、更可实施、更完整且更具潜在影响；不过样本量有限，且专家评价不能替代真实实验验证。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### TOMATO-Chem上的专家评价

<div class="result-value" markdown="1">

MAIL的总体专家评价分为10.80，高于MOOSE-Chem的10.32；MAIL在化学合理性、物理可行性、概念新颖性、完整性、科学影响和广泛用途上更高，但MOOSE-Chem的技术新颖性更高（1.64对1.56），MAIL的概念新颖性为1.36对1.28。

</div>

这表明在专家看来，MAIL生成的假设整体上更合理、可实施且更有科学价值，优势并不来自所有新颖性维度：MOOSE-Chem在技术层面的新催化剂、底物、条件或材料创新上略占优。该结果不能证明MAIL的假设已经通过实验，也不能排除单一专家和有限样本带来的评价不确定性。

<div class="result-source" markdown="1">

来源：第5节“Expert Evaluation”，Table 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On TOMATO-Chem (Table 4), MAIL achieves a higher overall expert-evaluation score than MOOSE-Chem (10.80 versus 10.32), with stronger scores in chemical plausibility, physical feasibility, conceptual novelty, completeness, scientific impact, and broader utility.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### MAIL温度敏感性实验

<div class="result-value" markdown="1">

在所报告的温度设置中，温度0.7取得最高平均MIOS 3.69和最高平均MPOS 2.38；温度1.0的Top MIOS为4.29，高于0.7的4.27，但其平均MIOS降至3.48、平均MPOS降至2.09。

</div>

结果支持将0.7作为在新颖性与具体性之间的折中：较高温度可能偶尔产生更接近目标的单个候选，却会降低多次运行的平均稳定性和方法要点覆盖。该实验只说明参数在当前GPT-4o、数据和评价协议下的影响，不能推出对其他模型或任务普遍成立的最优温度。

<div class="result-source" markdown="1">

来源：Table 6，第5节“Expert Evaluation”及第6节“Parameter Sensitivity Analysis”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

0.7 | 4.27 | 3.69 | 3.91 | 2.38

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### HN-NS上的跨数据集泛化

<div class="result-value" markdown="1">

在包含Nature和Science高新颖性论文的HN-NS数据集上，作者报告MAIL保持了稳健的MIOS表现；专家评价中所有方法的总分均因数据集更难而下降，但作者称MAIL仍能合成非显然的机制路径。

</div>

这说明MAIL在概念关系稀疏、理论演化较快且关键信息可能隐含于副反应或次要观察中的场景下，仍能进行一定程度的跨文献综合。由于所提供章节未给出Table 7和Table 8的具体数值，也未明确列出MAIL与各基线的完整数值差异，因此这里只能支持定性结论，不能据此精确判断提升幅度或统计显著性。

<div class="result-source" markdown="1">

来源：第7节“Experiments on HN-NS Dataset”，Table 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The evaluation on our HN-NS dataset (Table 7) demonstrates that MAIL maintains a robust Main Idea Overlap Score even on a more challenging benchmark.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 核心自动指标是对历史目标假设的恢复度，而非前瞻性实验验证或完全独立的原创性；作者也承认MIOS和MPOS衡量的是参考思想恢复。实际化学可行性仍需实验检验。
- 专家评价证据规模有限：每个数据集仅评审25个假设，由一名博士级有机化学家完成；HN-NS的完整表格数值、其他基线的名称与具体比较结果在所提供章节中未明确报告，因此部分泛化和优越性结论仍需完整原文核查。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- MOOSE-Chem：多轮候选搜索框架，使用束搜索、假设排序和演化式细化，是最有意义的端到端比较对象，因为它同样针对化学假设生成并进行多候选探索与迭代改进。专家评价也直接比较MAIL与MOOSE-Chem。来源：第4.2—4.3节。
- 其他基线：原文提到主比较包含多个已发布实现，但所提供章节未列出其名称、具体配置或完整结果，不能据此补充具体方法。

**实验想回答的问题**

- 在时间截断且避免目标论文泄漏的条件下，MAIL能否比现有方法更准确地恢复历史化学假设的核心思想与方法要点，并生成化学上合理、可检验的假设？
- MAIL在较高概念新颖性的数据集上是否仍具有泛化能力，以及检索数量和生成温度等关键参数如何影响假设质量？

**实验实现**

所有生成均调用GPT-4o API，温度设为0.7。每个背景执行三轮迭代细化，每轮生成8—10个候选，单次MAIL执行共生成24—30个候选并约调用35—40次LLM。文献检索使用PubMed、Semantic Scholar和CrossRef，并按2015年以前、2015—2020年、2021—2023年分组；所有检索记录限制在2023年底以前，且排除与目标论文同标题或同持久标识符的记录，但保留相关的先前研究。每轮每个查询检索深度为5，并选择两篇启发论文；三种来源每轮均查询，因此每次执行有9次来源级检索请求，不含分页和失败重试。每种方法在每个背景上独立运行10次，报告10个最终输出的平均分，并额外报告这10次中的事后最高分Top；Top只用于评价，不反馈给生成、细化或选择过程。候选缩减和最终选择由预定义提示自动完成，不访问目标假设、MIOS或MPOS。自动评价在生成和最终选择完成后才调用，所有输出去除方法标识并使用固定评分规则。由于两个数据集的论文均晚于GPT-4o截至2023年10月的知识截止时间，作者将该设置用于降低数据污染风险。专家评价采用双盲协议；相关性分析使用Pearson相关系数，并针对每个数据集的21个两两比较采用Benjamini—Hochberg校正。完整方法之间的比较不应解释为每次调用、令牌数、运行时间或API成本的效率比较。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 检索论文数量$K$的敏感性 | 作者报告适中的检索数量带来更好的假设质量，而过少或过多的启发论文都会降低表现；所提供章节未给出Table 5的具体$K$值、MIOS或MPOS数值。 | 该实验主要隔离检索上下文规模的作用。结果支持MAIL需要受控的启发多样性：材料太少会限制概念连接，材料太多则可能引入无关信息并增加模型负担。由于缺乏具体表格行，不能判断最佳$K$或下降幅度。 | 第6节“Parameter Sensitivity Analysis”，Table 5<br><span class="experiment-evidence">The results indicate that a moderate number of retrieved papers leads to better hypothesis quality, while both too few and too many inspirations reduce performance.</span> |
| 生成温度$T$的敏感性 | Table 6报告：$T=0.0$时Top MIOS、平均MIOS、Top MPOS、平均MPOS分别为3.85、1.85、3.01、1.93；$T=0.3$时为3.88、3.34、3.27、2.02；$T=0.5$时为4.04、3.32、3.93、2.28；$T=0.7$时为4.27、3.69、3.91、2.38；$T=1.0$时为4.29、3.48、3.35、2.09。 | 该消融隔离随机性和探索强度对输出的影响。$T=0.7$的平均指标最好，说明它在重复运行中的稳定性和目标要点覆盖之间取得较好折中；$T=1.0$虽有最高Top MIOS，却平均表现下降，说明单次最佳结果不能代表典型输出质量。 | Table 6，第6节“Parameter Sensitivity Analysis”<br><span class="experiment-evidence">0.7 \| 4.27 \| 3.69 \| 3.91 \| 2.38</span> |

**定性案例**

- HN-NS中的定性案例结论是，MAIL能够在高概念新颖性主题中合成“non-obvious mechanistic pathways”。其解释是：迭代细化与记忆驱动推理帮助模型连接相距较远的启发材料。不过所提供章节没有给出具体论文、输入文献、生成假设或逐案专家评分，因此不能进一步验证该机制路径是否真正对应目标发现或已具备实验可行性。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出基于记忆、增量更新和文献 grounding 的 LLM 科学假设生成与推理框架。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`f45efba3efc12c4b90de06bf812425c1f411eaf6122afef94d2b669a677ba3fe`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
