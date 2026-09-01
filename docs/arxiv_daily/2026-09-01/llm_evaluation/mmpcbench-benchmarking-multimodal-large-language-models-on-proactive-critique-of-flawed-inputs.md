---
title: "[论文解读] MMPCBench: Benchmarking Multimodal Large Language Models on Proactive Critique of Flawed Inputs"
description: "[arXiv 2608.29286][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.29286"
announcement_date: "2026-09-01"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:33:45.654180+00:00"
source_sha256: "1b96d97ce8a4b7c5fdcb478315f9076483beaae4c482f3ee65f056c350c9168b"
tags:
  - "LLM 评测"
  - "LLM 其他"
  - "LLM Reasoning"
  - "多模态大语言模型"
  - "主动批评"
  - "有缺陷输入"
  - "视觉前提"
  - "错误检测"
  - "错误诊断"
  - "推理—回答一致性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.29286</p>

# MMPCBench: Benchmarking Multimodal Large Language Models on Proactive Critique of Flawed Inputs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Jinzhe Li, Gengxu Li, Jinnan Li, Yuan Wu, Yi Chang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: School of Artificial Intelligence, Jilin University；Affiliation: International Center of Future Science, Jilin University{jinzhe25, gxli25；Affiliation: Engineering Research Center of Knowledge-Driven Human-Machine Intelligence, MOE, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.29286v1) · [PDF 下载](https://arxiv.org/pdf/2608.29286v1) · **关键词** 多模态大语言模型, 主动批评, 有缺陷输入, 视觉前提, 错误检测, 错误诊断, 推理—回答一致性<br>
**代码**: [https://github.com/ALIENS32/MMPCBench](https://github.com/ALIENS32/MMPCBench)

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

多模态大语言模型（MLLM）同时处理文本、图像等信息，并被用于问答、对话和智能代理。传统评测通常假设用户输入完整、正确且语义明确，但真实输入可能包含错误前提、歧义、文本与图像不一致，或因视觉信息缺失而无法回答。因此，本论文关注一种面向可靠交互的能力：模型在没有额外提示的情况下，主动检查用户输入，识别问题，解释错误原因，并通过纠正、澄清或拒答等方式给出合适响应。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多模态大语言模型（MLLM）**

能够联合理解文本和图像等多种模态信息，并生成自然语言回答的模型。它不仅要理解文字指令，还要判断文字描述是否与图像内容相符。

</div>
<div class="concept-item" markdown="1">

**主动批评（Proactive Critique）**

指模型不需要用户明确要求“检查错误”，就能自主发现输入中的无效前提、歧义或不可回答部分，并采取纠正、澄清或拒答等补救行动。直观地说，模型不能只服从问题，还要先判断这个问题本身是否成立。

</div>
<div class="concept-item" markdown="1">

**内部推理与最终回答的一致性**

该概念考察模型在内部推理中识别出的错误，是否也被反映在最终输出中。若模型内部已经发现问题，却在最终回答中继续顺从错误前提，就出现论文所称的“consistency gap”，即推理—回答一致性缺口。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文将主动批评形式化为对有缺陷用户输入的端到端处理任务。输入包括用户文本查询及可选的视觉内容，其中缺陷可能表现为前提矛盾、缺失前提、歧义、不可回答条件或细微视觉异常；模型需要在没有显式错误检测指令的情况下，输出能够处理该缺陷的响应。评测不仅判断模型是否发现错误，还判断其是否准确诊断根因、是否选择有效的补救策略，以及最终回答是否与内部推理保持逻辑一致。MMPCBench将缺陷组织为4类主要错误和12个子类别，并在多模态交互场景中考察纠正、澄清和拒答等响应方式。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$MLLM$**

多模态大语言模型（Multimodal Large Language Model）。

</div>
<div class="notation-item" markdown="1">

**$Proactive\ Critique$**

主动批评能力，即自主发现、分析并修复有缺陷用户输入的能力。

</div>
<div class="notation-item" markdown="1">

**$Detect$**

错误检测能力，判断输入是否存在缺陷。

</div>
<div class="notation-item" markdown="1">

**$Diag.$**

错误诊断能力，定位错误的具体原因或根本类型。

</div>

</div>

**直接相关的工作**

- **Mis-prompt 与 PCBench**: 这两项工作研究文本输入中的错误指令或误导性前提，为主动输入批评提供了先例；但它们限于文本模态，不能系统评估图像与文本之间的矛盾或视觉异常。
- **MoHoBench 与 ISEVAL**: 这两项工作将输入缺陷处理扩展到多模态场景，例如不可回答的视觉问题和文本—图像矛盾；但已有评测主要集中于拒答或有限的补救行为，未覆盖纠正、澄清、拒答等多种策略，也没有充分评估内部推理与最终回答之间的一致性。

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

MMPCBench不是一个训练新模型的方法，而是一个用于评估多模态大语言模型（MLLM）主动批判能力的基准框架。其输入被形式化为三元组 $I=\{T,V,Q\}$：$T$ 是文本上下文，$V$ 是图像或图表等视觉信息，$Q$ 是待执行的任务指令；其中 $T$ 与 $V$ 构成推理依据，$Q$ 定义任务目标。框架先按照四类、12个子类构造带缺陷的多模态输入，再通过分层评价衡量模型能否发现错误、解释错误并修正最终回答，同时检查内部推理与外部回答是否一致。直观地说，该方法不只问模型“能否完成任务”，还问它“发现题目有问题时，能否主动指出问题并给出合理处理”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 定义多模态任务与缺陷标签

将输入中的缺陷按四个主类进行归类：表达错误、前提矛盾、前提缺失和超出能力范围，共12个子类别。表达错误包括歧义和意图不清；前提矛盾包括跨模态矛盾、视觉间矛盾和文本内矛盾；前提缺失包括不同程度的视觉信息缺失、缺失图像、缺失指令和语义错配；超出能力范围表示仅凭给定证据无法客观推出答案。

<div class="method-step__io" markdown="1">

**输入**：由文本上下文 $T$、视觉信息 $V$ 和查询指令 $Q$ 组成的多模态输入 $I$。<br>
**输出**：带有错误类型、子类型及相应任务目标的缺陷输入样本。

</div>

**直观理解**：先把“题目为什么有问题”分门别类。例如，文字说图中有红色物体但图中没有，是跨模态矛盾；图像被遮挡到关键证据消失，则属于视觉前提缺失。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 构造基准数据

构建流程包括多源数据采样、多模型错误注入和自动/人工筛选；图2说明错误注入阶段形成约12,000个样本，随后过滤样本质量与缺陷有效性。

<div class="method-step__io" markdown="1">

**输入**：来自多种来源的原始多模态任务，以及需要植入的错误类型。<br>
**输出**：用于测试主动批判能力的带缺陷多模态基准集及其标注。

</div>

**直观理解**：可以把它理解为给原本正常的题目故意加入不同种类的“陷阱”，再由自动程序和人工检查，避免陷阱不成立或题目本身无法理解。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 让MLLM处理缺陷输入

模型在不获得额外提示的条件下生成回答；评价其是否检测到缺陷、是否正确诊断缺陷原因，以及是否采取澄清、拒答、修正任务或给出条件化答案等合理解决方式。给定节选未明确报告模型架构改造或额外训练过程。

<div class="method-step__io" markdown="1">

**输入**：MMPCBench中的带缺陷输入 $I=\{T,V,Q\}$，以及待测MLLM。<br>
**输出**：模型的最终回答，以及在适用模型或设置下可用于对齐分析的内部推理信息。

</div>

**直观理解**：测试重点不是强迫模型拒绝所有可疑问题，而是观察它能否先判断证据是否可靠，再决定回答、说明限制或要求补充信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 分层评价与综合比较

按照错误检测、错误诊断和错误解决三个层次进行评价，并结合对齐感知指标分析推理过程与最终回答是否一致；图2将相关指标记为 $EDA$、$DP$ 和 $SE$，并由LLM评审面板整合为综合 $PCQ$ 分数。

<div class="method-step__io" markdown="1">

**输入**：模型输出、缺陷标签，以及模型内部推理与最终回答（若评价设置提供）。<br>
**输出**：各模型在主动批判能力上的分项结果、综合分数及一致性分析。

</div>

**直观理解**：评价像检查医生诊断：先看是否发现病症，再看病因判断是否正确，最后看是否给出合适处理；如果模型内部已经发现问题却在最终回答中装作题目正常，还会被单独识别。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 多模态输入定义

$$
I=\{T,V,Q\}
$$

**符号说明**

- $I$：MLLM接收的完整多模态输入。
- $T$：文本上下文，包含核心概念和技术术语。
- $V$：视觉信息，例如图像或图表，提供空间或视觉证据。
- $Q$：查询或任务指令，规定模型需要完成的目标。

<div class="equation-explanation" markdown="1">

**直观理解**：该定义把任务拆成证据和目标两部分：$T$ 与 $V$ 共同提供模型应依据的前提，$Q$ 则说明要完成什么任务。主动批判的关键，就是检查这些前提是否足以支持该目标，以及彼此之间是否一致。<br>
**原文位置**：第3节“Task Formulation and Error Taxonomy”，公式(1)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：该论文提供的节选描述的是基准构造与评价方法，而不是用于训练MLLM的新损失函数或优化目标。原文未明确报告是否对被测模型进行基准特定的微调，因此不能据此推断存在训练阶段；基准的核心目标是测量模型在推理时的错误检测、诊断和解决能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 四类十二子类错误分类体系**

错误按缺陷所在的输入组成部分及其逻辑性质划分。表达错误处理文本不可确定解释的问题；前提矛盾处理 $T$、$V$ 内部或跨模态的互斥证据；前提缺失处理解决任务所需信息不存在、损坏或不相关的情况；超出能力范围处理即使拥有当前证据也无法逻辑推出的目标。

> 直观理解：该模块把笼统的“输入有问题”拆成可诊断的故障类型，使模型能力差异能够被具体定位，而不是只得到一个总体正确率。

**2. 多阶段缺陷数据构造与筛选**

数据构造采用多源采样、基于多个模型的错误注入以及自动和人工过滤三阶段流程，形成约12,000个候选样本。视觉前提缺失还按约30%、50%和80%的缺失程度区分轻度、中度和重度情形。

> 直观理解：不同缺失程度用于测试问题难度：遮掉少量信息可能仍可回答，遮掉大部分关键信息则应触发更谨慎的处理。

**3. 分层且对齐感知的评价框架**

框架分别考察错误检测、诊断和解决，并使用 $EDA$、$DP$、$SE$ 等指标构成综合 $PCQ$ 评价；同时通过LLM-as-a-Judge评审面板分析内部推理与最终响应的连贯性。给定节选未定义这些缩写的完整公式、具体判分规则或评审面板配置。

> 直观理解：单看最后答案可能掩盖模型已经意识到问题但没有说出来的情况，因此该模块把“想到了什么”和“最后说了什么”之间的落差也纳入评价。

**训练与推理**

从给定材料可确定的流程是：构造带标签的缺陷输入，直接将其提供给待测MLLM，收集最终回答，并在评价设置允许时比较内部推理与最终回答。随后使用分层评价考察检测、诊断和解决表现，再以 $PCQ$ 等综合结果进行模型间比较；原文节选未明确报告具体推理提示、输出格式、是否要求模型显式分步作答或各指标的精确计算流程。

**复现信息**

复现实验至少需要按照四类、12个子类重建缺陷样本，保留视觉缺失约30%、50%和80%的分级，并执行多源采样、模型错误注入及自动/人工筛选三阶段流程。图2报告错误注入阶段为约12,000个样本；但给定节选未明确报告各类别样本数量、数据划分、注入模型、筛选标准、被测模型推理参数、$EDA$、$DP$、$SE$ 与 $PCQ$ 的具体定义，以及LLM评审面板的模型和提示词，因此这些细节不能据此补全。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MMPCBench：最终包含 $3,146$ 个经过筛选的错误输入实例，覆盖四类主要错误和十二个子类别；其作用是系统测试 MLLM 对不可回答或有缺陷多模态输入的主动批判能力。原文报告数据由约 $12,000$ 个候选样本经模型核验和人工复审后得到，最终样本分布见 Table 4。
- 源数据池：OlympiadBench、MMMU-Pro、EMMA、MathVista 和 MATH-Vision；这些数据集提供原始学科问题，研究者在保持学科主题的同时改写问题和上下文，再注入错误。原文未明确报告各源数据集的单独样本数量或训练、验证、测试划分。
- 一致性分析子集：对五个模型同时检查内部推理链和最终回答，用于比较 $EDA^{R}$ 与 $EDA^{F}$，并计算检测丢失率和诊断质量下降。原文未明确报告该分析所使用的样本数量或独立数据划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Error Detection Accuracy（EDA）**

对每个错误输入，只有当最终回答明确指出输入不合理或存在错误时才记为检测成功。若模型照常执行错误指令、给出肯定性幻觉回答，或只进行无声修正，均视为未检测。形式为 $\mathrm{EDA}=\frac{1}{N}\sum_{i=1}^{N}d_i$，其中 $N$ 是错误输入数量，$d_i\in\{0,1\}$ 表示第 $i$ 个样本是否被明确检测；后续诊断和处理评价仅在成功检测集合 $\mathcal{H}=\{i\mid d_i=1\}$ 上进行。 （越高越好，因为它直接衡量模型是否主动把错误说出来；该指标主要反映主动性，不等于模型已经正确解释或修复了错误。）

</div>
<div class="metric-item" markdown="1">

**Diagnostic Precision（DP）**

在模型已检测出错误的样本上，评价模型是否准确说明错误的根本原因。摘录章节只给出了评分变量 $s_i^{\mathrm{diag}}\in\{0,1,2\}$ 的定义起始部分，完整分级规则在所供原文中未明确报告。 （越高越好，因为它衡量批判是否不仅停留在“有问题”的表面判断，而是指出了正确的错误机制。）

</div>
<div class="metric-item" markdown="1">

**Strategic Effectiveness（SE）**

在模型检测并诊断错误后，评价其采取的处理策略是否有效，例如纠正、澄清或拒答。摘录章节未给出 SE 的完整计算公式和分级细则。 （越高越好，因为有效的主动批判应当帮助用户纠正输入、澄清必要信息或避免基于错误前提继续作答。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 14 个 MLLM 在 MMPCBench 上的总体主动批判表现

<div class="result-value" markdown="1">

作者报告平均 PCQ 为 $26.1$，平均 EDA 为 $33.2\%$，意味着约三分之二的错误输入场景没有得到模型明确的批判；模型家族大致呈现 Qwen3-VL 领先、主流闭源模型居中、Gemma-3、GLM-4.6V 和 Doubao-Seed-1.6-vision 居后的分层。证据中的 PCQ 是综合主动批判质量指标，但所供章节未给出其完整公式。

</div>

核心结论是模型通常会继续完成用户任务，而不是先验证输入是否合理。该结果支持“主动发现错误仍是普遍短板”的作者主张，但不能单独证明某一模型在所有任务或真实部署环境中都更可靠，因为数据由特定错误注入流程构造，且摘录未提供完整 Table 2 数值、置信区间或统计显著性分析。

<div class="result-source" markdown="1">

来源：Section 6.2，Proactive Critique Is Widely Deficient；Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 2, proactive critique remains a systematic weakness across current MLLMs: the average PCQ is only 26.1 and the average EDA is 33.2%, indicating that models fail to produce any critical response in approximately two-thirds of erroneous-input scenarios, instead defaulting to sycophantic task completion.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 模型规模、模型家族与错误类别的影响

<div class="result-value" markdown="1">

在 Qwen3-VL 家族内，PCQ 从 $8$B 模型的 $38.7$ 提升至 $235$B 模型的 $47.4$；相反，Gemma-3 随规模扩大近乎停滞甚至轻微下降。类别平均 PCQ 从 Expression Error 的 $12.9$、Premise Contradiction 的 $21.0$、Missing Premise 的 $26.4$ 到 Beyond Capability 的 $65.4$，表现出明显难度梯度。

</div>

规模并非自动带来主动批判能力：只有当训练范式支持这种行为时，扩大规模才可能有效。直接妨碍任务完成的错误较容易被发现，而表达歧义、矛盾前提和细微视觉缺失需要模型主动核查，因此更难。类别结果适合解释 benchmark 的诊断性，但不能把 PCQ 差异完全归因于错误本身，因为各类别样本量、注入方式和视觉复杂度可能同时影响结果。

<div class="result-source" markdown="1">

来源：Section 6.2，Proactive Critique Is Widely Deficient

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Within Qwen3-VL, PCQ improves consistently with scale, from 38.7 (8B) to 47.4 (235B). In contrast, Gemma-3 shows near-stagnation or even slight regression.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 内部推理与最终回答的一致性

<div class="result-value" markdown="1">

在表中五个模型的平均结果为 $EDA^{R}=0.47$、$EDA^{F}=0.28$、DDR $=0.46$、DQD $=0.20$；其中 DDR 表示内部推理检测到、但最终回答未呈现的错误比例，DQD 表示两者都检测到时诊断精度的平均下降。作者据此认为，模型并非完全无法在推理阶段识别错误，而是经常在生成最终回答时抑制这些发现。

</div>

这一区分了“模型能否看出问题”和“模型是否把问题告诉用户”。平均 DDR 为 $0.46$ 表明内部批判约有近一半没有传递到最终输出，且平均诊断下降 $0.20$（满分范围为 $0$ 到 $2$）说明即使最终提及错误，解释也可能变弱。该分析支持一致性缺口这一作者主张，但只覆盖表中五个模型，不能直接推广到全部 $14$ 个模型；此外，内部推理的可观测性和评判方式也可能影响该结论。

<div class="result-source" markdown="1">

来源：Section 6.3；Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 3 reveals a systematic gap across all five models: EDA^R exceeds EDA^F by 19 percentage points on average, and DDR shows that 46% of reasoning-level critique findings are absent from the final response.

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

- Qwen3-VL 系列：包括 $8$B、$30$B 和 $235$B 规模模型，用于观察同一模型家族内的规模变化以及开放模型与其他模型家族的差异。
- 主流闭源 MLLM：包括 GPT-5.1 (high)、GPT-5.2、GPT-5-mini、Claude-Sonnet-4.5 (Thinking)、Gemini-3-Pro 和 Gemini-3-Flash，用于检验商业模型在主动批判任务上的表现及其推理—回答一致性。
- 其他开放模型：包括 GLM-4.6V 以及 Gemma-3-4B-it、Gemma-3-12B-it 和 Gemma-3-27B-it，用于比较不同开放模型家族和模型规模。
- Doubao-Seed-1.6-vision：作为另一种闭源视觉语言模型参与横向比较，用于考察模型家族和训练范式差异，而不是作为传统的单一算法基线。

**实验想回答的问题**

- 当前多模态大语言模型（MLLM）能否在没有额外提示的情况下，主动检测错误输入，并进一步诊断错误原因、采取有效处理策略？
- 模型的内部推理与最终回答之间是否存在一致性缺口，以及模型规模、模型家族和错误类别如何影响主动批判能力？

**实验实现**

数据构造包括数据采样、错误注入和质量筛选。研究者使用 GPT-5.1 (high)、Gemini-3-Pro 和 Doubao-Seed-1.6-vision 改写样本；视觉错误通过梯度引导退化移除关键语义区域，或使用生成式编辑合成视觉矛盾；文本和逻辑错误通过少样本提示改写查询或插入矛盾前提；结构错误通过打乱或删除数据组件生成。两个未参与生成该样本的模型进行独立二元核验，任一检查失败即淘汰；剩余样本由三名研究生复审，每个样本由两人评估、分歧由第三人裁决，最终得到高质量集合。模型评测使用原始图像，不额外缩放或预处理；图像分辨率采用各模型默认 API 配置。开放模型的主要设置包括 Qwen3-VL 使用 $T=0.7$、$top\_p=0.7$ 和 presence penalty $1.5$，GLM-4.6V 使用 $T=0.7$、$top\_p=0.7$，Gemma-3 使用 $T=1.0$、$top\_p=0.7$。原文未明确报告统一的提示模板、重复运行次数、随机种子、显著性检验或完整 DP/SE 评分规则。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 策略分布提供了一个定性的行为案例：Qwen3-VL-235B-A22B-Instruct 主要采取 Correction，在声明假设后把图文不一致视为可修复的用户疏漏；Claude-Sonnet-4.5 (Thinking) 主要采取 Clarification，引导用户先明确歧义而不贸然猜测。该对比说明“主动批判”不只有一个理想输出形式：直接修正强调即时可用性，澄清则强调降低未经验证的推断风险；但摘录未提供具体输入—输出样例，因此不能据此判断哪种策略在每个错误类别上都更优。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出评测多模态大模型主动发现、诊断和修复错误输入能力的基准与分层评价协议。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`1b96d97ce8a4b7c5fdcb478315f9076483beaae4c482f3ee65f056c350c9168b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
