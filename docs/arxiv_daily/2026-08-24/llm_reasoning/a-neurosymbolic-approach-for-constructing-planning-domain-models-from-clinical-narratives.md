---
title: "[论文解读] A Neurosymbolic Approach for Constructing Planning Domain Models from Clinical Narratives"
description: "[arXiv 2608.21186][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.21186"
announcement_date: "2026-08-24"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-24T02:08:47.176884+00:00"
source_sha256: "b7eb7c1c471004d84b23c9f33d4097037346cef16d203a9e562db4d411ce21f8"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "临床叙述"
  - "手术流程建模"
  - "自动规划"
  - "PPDDL"
  - "神经符号人工智能"
  - "大语言模型"
  - "概率动作模型"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.21186</p>

# A Neurosymbolic Approach for Constructing Planning Domain Models from Clinical Narratives

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Ranveer Singh, Saurabh Mathur, Michael Skinner, Prasad Tadepalli, Kristian Kersting, Sriraam Natarajan</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> The University of Texas at Dallas, Richardson, TX, USA；Technical University of Darmstadt, Darmstadt, Germany；Oregon State University, Corvallis, OR, USA；Hessian Center for Artificial Intelligence (hessian.ai), Darmstadt, Germany；German Research Center for AI (DFKI)</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.21186v1) · [PDF 下载](https://arxiv.org/pdf/2608.21186v1) · **关键词** 临床叙述, 手术流程建模, 自动规划, PPDDL, 神经符号人工智能, 大语言模型, 概率动作模型<br>


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

本文位于临床文本信息抽取、神经符号人工智能与自动规划的交叉领域。临床手术记录包含患者状况、外科医生实施的动作及其结果，但这些信息通常以非结构化叙述形式存在，且部分动作只被间接暗示。论文关注如何把这些叙述转换为可解释的概率规划领域模型，使模型能够表示手术流程中动作的前置条件、可能效果及其不确定性，并支持临床验证、手术培训、病历审查和质量改进等决策支持任务。其核心表示采用基于状态谓词和参数化动作模式的规划语言，再结合大语言模型对文本中隐含事件进行补全。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自动规划与规划领域模型**

自动规划研究如何根据当前状态和目标生成一系列动作。规划领域模型规定有哪些动作、动作何时可执行，以及执行后状态如何变化；在本文中，它对应对手术流程的形式化描述。

</div>
<div class="concept-item" markdown="1">

**PDDL 与 PPDDL**

PDDL 是自动规划中描述领域的形式语言，通常用状态谓词表达事实，用参数化动作模式表达可复用的操作。PPDDL 在此基础上允许动作具有概率效果，因此可以表示同一手术动作可能产生不同结果的情况。

</div>
<div class="concept-item" markdown="1">

**神经符号方法**

神经方法擅长从自然语言中识别和补全信息，符号方法则擅长用明确、可检查的规则表示知识。神经符号方法将两者结合：本文使用预训练大语言模型处理临床叙述，再用符号规划模型组织和验证动作知识。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一组关于同一类手术的非结构化临床记录，本文以腹腔镜阑尾切除术记录为具体场景，目标是学习一个概率规划领域模型。输入包括手术叙述及其中显式或隐含的临床事件；输出包括结构化事件序列、动作模式及其前置条件和概率效果。模型应尽量概括不同患者病例和不同外科医生的共同流程，同时保留并表达罕见并发症等不确定情况，并且其符号知识需要能够由临床专家理解和核验。论文将手术记录中的每个病例视为对潜在动作轨迹的部分观察，而不是假设原始文本已经提供完整、准确且结构化的事件日志。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D$**

临床手术记录数据集；本文实验中包含腹腔镜阑尾切除术记录。

</div>
<div class="notation-item" markdown="1">

**$x$**

一份原始临床叙述或手术记录文本。

</div>
<div class="notation-item" markdown="1">

**$s$**

从文本中抽取或补全的结构化状态、谓词或事件序列，用于描述手术过程中的事实变化。

</div>
<div class="notation-item" markdown="1">

**$a$**

规划模型中的参数化动作，例如放置穿刺器；动作具有可执行的前置条件及执行后的效果。

</div>

</div>

**直接相关的工作**

- **Ghallab、Nau 与 Traverso（2004），Automated planning: theory and practice**: 该工作提供自动规划和规划领域模型的基础背景，帮助定义本文所使用的状态、动作、前置条件与效果等形式化概念。本文将这些规划表示用于临床手术流程建模，而不是仅在传统人工定义的规划领域中进行规划。
- **Younes 与 Littman（2004），PPDDL1.0: an extension to PDDL for expressing planning domains with probabilistic effects**: 该工作定义了能够表达概率效果的 PPDDL 形式化基础。本文采用这一类概率规划表示来刻画手术动作结果的不确定性，例如同一动作在不同病例中可能导致不同状态变化。

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

NSPIN将一组无结构的手术叙述输入预训练大型语言模型（LLM），先建立描述手术对象、观察谓词和动作的形式化词汇，再从每份病历中抽取显式事件并补全被省略的隐含事件，形成结构化动作—观察序列。随后，系统利用这些序列进行符号化的概率规划域归纳，学习动作的前置条件与随机观察效果，并用LLM提出的语义修订结合经验数据验证来调整前置条件，最终输出可用于动作预测、计划生成和叙述合成的概率规划域模型$\mathcal{P}$。直观地说，LLM负责“读懂病历并补齐常识”，符号归纳负责“检查这些步骤能否组成一致的流程”，二者共同避免单独使用任一方法的缺陷。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 形式化模式创建

LLM根据领域描述生成初始规划模式$\mathcal{P}_0$，其中规定类型化对象类别、观察谓词以及用于表示动作和转移的形式化模板。观察谓词属于有限的一阶逻辑谓词集合$\mathcal{F}$，用于描述器械、解剖结构、位置及其关系。

<div class="method-step__io" markdown="1">

**输入**：自然语言的手术领域描述，包括手术规则、约束和相关对象类型。<br>
**输出**：初始领域词汇和模式$\mathcal{P}_0$，包括对象集合$O$、谓词集合$\mathcal{F}$以及动作表示所需的结构。

</div>

**直观理解**：这一步先建立统一的“手术语言”：例如把地点、器械和解剖结构分成不同类别，并规定“切口已建立”或“阑尾已固定”应如何写成机器可检查的事实。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 病历事件抽取与隐含事件补全

LLM将不同医生使用的缩写、术语和叙述风格映射到统一的动作与观察谓词，抽取文本中明确出现的事件；随后根据部分事件序列、临床常识和动作可行性推断病历中未明确写出的中间动作或状态。该阶段同时承担信息抽取和序列插补，使输出不再只是病历字面上出现的稀疏事件。

<div class="method-step__io" markdown="1">

**输入**：病历数据库$\mathcal{D}=\{x^{(i)}\}_{i=1}^{N}$，其中每个$x^{(i)}$是一例手术的非结构化叙述，以及初始模式$\mathcal{P}_0$。<br>
**输出**：用于归纳的结构化动作—观察序列，包括显式事件、被补全的隐含事件及其顺序信息。

</div>

**直观理解**：病历常写“结果”而省略医生认为显而易见的步骤；LLM先把不同写法翻译成同一种符号，再依据上下文补出例如固定阑尾基底后才能切断阑尾这类必要环节。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 概率动作—观察模型归纳

符号归纳方法从序列中聚合跨病例的动作转移，学习每个参数化动作的前置条件、动作执行后可能产生的观察及其概率，并将结果表示为PPDDL域模型。前置条件约束某动作在什么状态下可执行，概率效果则表示同一动作在不同病例中可能出现的随机结果或观察。

<div class="method-step__io" markdown="1">

**输入**：由多份病历得到的结构化动作—观察序列，以及模式中的对象和谓词定义。<br>
**输出**：初步概率规划域模型，包括动作模式、前置条件、随机效果及其概率分布。

</div>

**直观理解**：系统不把一份病历当成唯一标准答案，而是比较很多病例：哪些事实通常必须先成立，某动作之后哪些观察经常出现，以及这些观察各自有多大可能。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### LLM语义修订与经验验证

LLM检查符号归纳出的前置条件，提出删除虚假相关条件、保留真正流程依赖关系的修订；系统再用病例中的动作转移进行经验验证，评估修订后模型对观察和下一动作的预测，并以预测表现和真实动作不可用率指导最终选择。该过程重点解决数据驱动归纳可能把偶然共现误当作动作必要条件的问题。

<div class="method-step__io" markdown="1">

**输入**：初步PPDDL模型、抽取和插补后的病例序列，以及LLM对动作语义和临床流程的知识。<br>
**输出**：经过验证的NSPIN概率规划域模型，可作为下一动作预测的约束，也可用于采样动作序列和生成手术叙述。

</div>

**直观理解**：如果模型错误地认为某个描述性发现是动作必需条件，很多真实病例就会被挡住；LLM提出更符合语义的修改，数据验证则检查这种修改是否真的能解释未见病例。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 经典规划问题的形式化定义

$$
\langle\mathcal{P},s_{0},G\rangle,\quad \mathcal{P}=\langle\mathcal{F},O,\mathcal{A}\rangle
$$

**符号说明**

- $\mathcal{P}$：规划域，包含对象、谓词和参数化动作模式。
- $s_{0}$：初始状态，即规划开始时成立的事实集合。
- $G$：目标条件，用于判断某个状态是否完成任务。
- $\mathcal{F}$：有限的一阶逻辑谓词符号集合，用于表示对象属性及对象之间的关系。
- $O$：有限对象集合，例如手术地点、器械和解剖结构。
- $\mathcal{A}$：参数化动作模式集合，例如放置端口或切断阑尾。

<div class="equation-explanation" markdown="1">

**直观理解**：该定义把一个规划任务拆成三部分：从什么状态开始、允许使用哪些动作和事实、最终要满足什么目标。NSPIN的任务不是直接为每份病历生成文字，而是从病历数据库中归纳出这样的可复用规划域。<br>
**原文位置**：Background > Planning Domain Models

</div>

</div>

<div class="equation-block" markdown="1">

#### 概率动作效果的表示

$$
\{(p_{1},\operatorname{add}_{1}(a),\operatorname{del}_{1}(a)),\dots,(p_{k},\operatorname{add}_{k}(a),\operatorname{del}_{k}(a))\},\quad \sum_{i=1}^{k}p_{i}=1
$$

**符号说明**

- $a$：一个动作或动作模式。
- $p_i$：执行动作$a$时第$i$种结果发生的概率。
- $\operatorname{add}_{i}(a)$：第$i$种结果使其变为真的事实集合。
- $\operatorname{del}_{i}(a)$：第$i$种结果使其变为假的事实集合。
- $k$：该动作可能结果的数量。

<div class="equation-explanation" markdown="1">

**直观理解**：与确定性规划中“一个动作必然得到一个结果”不同，PPDDL允许同一动作在不同病例中产生不同观察或状态变化。概率总和为$1$保证这些结果覆盖该动作的全部可能性，因而模型可以表达临床流程中的随机性。<br>
**原文位置**：Background > Planning Domain Models

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确给出一个统一的可微训练损失或参数优化公式。根据方法和实验描述，NSPIN的优化目标是经验上获得能够解释病例序列的概率动作—观察模型：提高观察集合和下一动作的Top-1、Top-3预测准确率，降低平均负对数似然，并降低真实动作不可用率（TADR）；LLM前置条件修订则通过这些留出数据指标验证其是否减少过强约束。这里的“训练”主要是从结构化病例序列进行符号动作模型归纳和概率估计，而不是端到端更新LLM参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. LLM抽取与序列插补模块**

该模块利用预训练LLM的语言表示能力处理非标准缩写、术语变体和不同医生的写作风格，将文本映射到模式中的动作和观察谓词。除抽取显式信息外，LLM还根据临床叙述中的上下文与隐含可供性补全潜在事件，以缓解原始病历的稀疏性和不完整性。

> 直观理解：它相当于一个能够理解临床简称的记录整理员，但不仅抄写原文，还会根据前后步骤补出医生没有写明的常规动作。

**2. 符号化PPDDL归纳模块**

该模块将结构化序列转换为参数化动作模型，学习动作前置条件和观察效果；概率效果表示动作执行后多种可能结果的分布。符号结构提供明确的状态、动作可执行性和逻辑关系，使模型能够跨病例聚合并对未见病历进行预测，而不是只生成单份文本对应的流程。

> 直观理解：它像一套流程规则检查器：只有满足必要条件的动作才允许发生，并记录动作之后可能出现的多种结果及其频率。

**3. 基于LLM提议和数据验证的前置条件修订模块**

系统对符号归纳出的前置条件进行一次语义层面的LLM修订，重点去除由病例共现造成的过强或无关条件，同时保留核心程序依赖；随后通过观察集合预测、下一动作预测、平均负对数似然和真实动作不可用率进行验证。论文示例中，该模块移除了“与阑尾相关的病理描述”等非核心条件，但保留了标本必须先取回这一流程要求。

> 直观理解：统计数据有时会把“经常一起出现”误认为“必须先发生”；修订模块区分真正的因果前提和只是常见伴随信息，再用留出的病例检验判断是否改对。

**训练与推理**

训练或模型构建阶段首先从领域描述生成$\mathcal{P}_0$，再对数据库$\mathcal{D}$中的每份病历抽取并插补动作—观察序列；符号归纳器根据这些序列学习动作前置条件和概率观察效果，之后由LLM提出前置条件修订，并用经验转移验证修订结果。论文未明确报告符号归纳器的具体搜索算法、概率估计公式或是否使用独立验证集选择修订版本，因此不能进一步断言其内部优化过程。推理阶段给定新的部分病例序列或当前状态，模型使用已学习的前置条件筛选可执行的候选动作，并依据动作—观察转移模型预测后续观察或采样下一动作；连续采样即可生成部分手术序列，再结合谓词模板、序列和生成规则合成手术叙述。PPDDL前置条件充当动作选择的逻辑门，概率效果则提供后续观察的不确定性。

**复现信息**

复现或公平解释结果所需的关键信息是：数据来源为2,660份腹腔镜阑尾切除术病历，记录来自9名外科医生；模型比较包含NSPIN、去掉前置条件修订的NSPIN、带示例的LLM基线和仅使用LLM的基线。论文片段明确说明，观察预测在执行动作条件下评估，因此前置条件修订主要影响下一动作预测而不直接影响观察预测；序列生成时使用PPDDL前置条件限制可执行动作，并由转移模型发射相应观察。其余关键实现信息，如所用LLM名称与版本、提示词、符号归纳算法、训练—测试划分、随机种子、具体PPDDL编码和概率估计细节，原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 临床叙事数据集：包含 2,660 份腹腔镜阑尾切除术记录，由 9 名外科医生撰写，来自美国得克萨斯州达拉斯儿童医疗中心。数据用于从非结构化文本抽取和补全手术步骤，并进行跨医生泛化评估。
- Imputed 数据：每份手术记录经模型抽取隐含步骤并补全，形成结构化谓词序列；用于检验隐含信息补全是否改善模型学习。原文未明确报告该子集的独立样本数。
- Non-Imputed 数据：不进行隐含步骤补全的结构化序列，用作与 Imputed 数据的对照；原文未明确报告该子集的独立样本数。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Top-1/Top-3 accuracy**

衡量模型预测的真实目标是否分别位于第一名或前三名；在 observation set prediction 中，目标是动作与下一动作之间实际出现的观察集合，在 next-action prediction 中，目标是后续动作。 （越高越好，因为这表示真实观察集合或后续动作更常被排在前面。）

</div>
<div class="metric-item" markdown="1">

**Average negative log-likelihood（Avg NLL）**

衡量模型为真实观察集合或动作分配的概率质量，并反映概率预测的校准程度。 （越低越好，因为较低的负对数似然表示模型给真实结果分配了更高且更合理的概率。）

</div>
<div class="metric-item" markdown="1">

**True action disallowed rate（TADR）**

衡量学习到的前条件错误排除真实后续动作的比例，即符号层面的适用性约束与实际工作流不兼容的程度。 （越低越好，因为较低的 TADR 表示模型较少错误地禁止临床记录中确实发生的动作。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 隐含步骤补全：Imputed 与 Non-Imputed 数据上的 action set prediction

<div class="result-value" markdown="1">

Imputed 数据的 Top-1 accuracy 为 $0.32\pm0.07$，Top-3 accuracy 为 $0.51\pm0.10$，Avg NLL 为 $9.33\pm2.35$；Non-Imputed 数据分别为 $0.24\pm0.09$、$0.39\pm0.12$ 和 $11.85\pm2.85$。

</div>

补全隐含步骤后，模型更常把真实观察集合排在前列，并为真实结果分配更高概率，说明临床叙事中的隐含动作确实影响概率效果学习。该结果支持补全步骤的必要性，但只直接比较了 Imputed 与 Non-Imputed 数据，不能单独证明完整 NSPIN 一定优于所有 LLM 基线。

<div class="result-source" markdown="1">

来源：Table 1, Empirical Evaluation—Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Imputed 0.32 ± 0.07 0.51 ± 0.10 9.33 ± 2.35; Non-Imputed 0.24 ± 0.09 0.39 ± 0.12 11.85 ± 2.85

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 模型规模与评估覆盖范围：生成的腹腔镜阑尾切除术规划模式

<div class="result-value" markdown="1">

NSPIN 生成的模式包含 63 个谓词，其中 34 个为观察谓词、26 个为动作谓词、3 个为关系谓词，并包含 58 类带类型参数和 322 个枚举 grounding 值。

</div>

该结果表明方法能够把较复杂的手术流程编码为具有观察、动作和关系结构的 PPDDL 模式，而不是只生成少量孤立动作。它说明表达能力和覆盖范围，但这些规模数字本身不代表模型正确性，也不等价于临床可部署性。

<div class="result-source" markdown="1">

来源：Empirical Evaluation—Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The generated appendectomy schema comprises 63 predicates in total, including 34 observation predicates, 26 action predicates, and 3 relational predicates, along with 58 typed argument categories and 322 enumerated grounding values.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨医生泛化与统计比较

<div class="result-value" markdown="1">

实验采用 9 折留一医生交叉验证，并报告所有比较均具有统计显著性；具体比较对应的各方法完整分数在所给摘录中未明确报告。

</div>

留出整名医生而不是随机留出单条记录，可以更严格地测试模型能否迁移到不同医生的书写习惯。统计显著性说明报告的比较不太可能只是抽样波动，但由于当前材料缺少 Tables 2 和 3 的具体数值，无法判断各方法提升幅度、效应大小或临床实际重要性。

<div class="result-source" markdown="1">

来源：Empirical Evaluation—Metrics

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We compute these metrics for each method using 9-fold cross-validation, where the PPDDLs are learnt from predicate sequences of all but one surgeon, and evaluated on the held-out surgeon’s predicate sequences.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前所给实验摘录只包含 Table 1 的具体数值，没有 Tables 2 和 3 中 LLM-only、LLM-Example、完整 NSPIN 及预条件精炼消融的完整结果，因此无法严格核验论文关于方法间优劣的全部数值结论。
- 数据来自单一医院的 9 名医生，且仅覆盖腹腔镜阑尾切除术；留一医生交叉验证能测试一定的书写者泛化，但不能证明模型已泛化到其他医院、术式、语言风格或真实临床决策环境。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- LLM-only：向 LLM 提供域描述和谓词模板，要求其零样本直接生成 PPDDL 模型，用于检验仅依赖语言模型先验能否构造可用规划模型。
- LLM-Example：除域描述和谓词模板外，再提供数据集中的一个谓词序列作为上下文示例，用于检验少量示例 grounding 是否能弥补零样本生成的不足。
- NSPIN without final LLM-based precondition refinement：移除 NSPIN 最后的 LLM 预条件精炼步骤，用于隔离该组件对最终规划模型质量的贡献。

**实验想回答的问题**

- LLM 对临床叙事中隐含步骤的补全，是否能提高诱导规划域模型的准确性？
- LLM 预条件精炼是否能改善 NSPIN 生成的概率规划模型，并使其优于仅依赖 LLM 的方法？

**实验实现**

采用 9 折交叉验证：每一折使用除一名医生外其余 8 名医生的谓词序列学习 PPDDL 模型，再在留出的医生记录上评估，以测试跨医生泛化。为保护临床隐私，原文描述采用混合 LLM 策略：本地、医学调优的 Medgemma-27b 负责从原始叙事抽取和补全程序轨迹，Claude Sonnet 4.6 负责高层模式构建和符号精炼；但原文同时写道“All LLM-based generations and refinement use Claude Sonnet”，两处关于生成模型的表述存在需要核查的歧义。每份手术记录进行 5 次抽取，每个抽取序列独立补全，并用 Clingo ASP 求解器依据约束合并每名患者的 5 条谓词序列。数据驱动的 PPDDL 构造对窗口大小 $w\inightarrow\text{?}$、最小效果概率阈值和最小前条件支持阈值进行网格搜索；原文明确报告最终选择 $w=3$、$\tau_{\mathrm{prob}}=0.01$ 和 $\tau_{\mathrm{obs}}=0.8$，但窗口集合在所给文本中存在排版损坏。生成的阑尾切除术模式包含 63 个谓词、58 类带类型参数和 322 个枚举 grounding 值。统计检验采用显著性水平 $\alpha=0.05$ 的 Wilcoxon signed-rank test。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 去除最终 LLM 预条件精炼 | 原文将“不含最终 LLM-based precondition refinement”的 NSPIN 变体列为比较方法，但所给摘录未提供该消融的具体分数或变化幅度。 | 该消融试图隔离预条件精炼的作用：前面的轨迹抽取、隐含步骤补全和数据驱动 PPDDL 构造保持不变，只移除根据 LLM 建议修订前条件的步骤。若完整结果中该变体的 TADR 或预测指标变差，才能说明精炼改善了动作适用性；当前材料不足以作出这一数值结论。 | Empirical Evaluation—Methods<br><span class="experiment-evidence">Additionally, we also evaluate a variant of NSPIN without the final LLM-based precondition refinement.</span> |
| Imputed 与 Non-Imputed 数据对照 | Imputed 的 Top-1 accuracy 为 $0.32\pm0.07$，Non-Imputed 为 $0.24\pm0.09$；Imputed 的 Top-3 accuracy 为 $0.51\pm0.10$，Non-Imputed 为 $0.39\pm0.12$；Imputed 的 Avg NLL 为 $9.33\pm2.35$，Non-Imputed 为 $11.85\pm2.85$。 | 该对照直接移除隐含信息补全这一组件，显示补全对观察集合预测有一致帮助。由于对照可能同时改变输入序列的完整性和统计分布，结果支持组件有效，但不能排除数据表示变化带来的部分影响。 | Table 1, Empirical Evaluation—Results<br><span class="experiment-evidence">Imputed 0.32 ± 0.07 0.51 ± 0.10 9.33 ± 2.35; Non-Imputed 0.24 ± 0.09 0.39 ± 0.12 11.85 ± 2.85</span> |

**定性案例**

- 原文提出 Q4 以临床知识和实践为标准，评估 NSPIN 补全的步骤、诱导的前条件及生成叙事的一致性，并声称专家临床审查显示其诱导知识“大体符合”手术实践；但所给摘录没有具体病例、专家人数、审查协议或逐项错误示例，因此不能据此判断哪些临床步骤最可靠或哪些前条件仍存在风险。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper uses an LLM within a neurosymbolic framework to extract, validate, and refine formal probabilistic planning models from clinical narratives.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`b7eb7c1c471004d84b23c9f33d4097037346cef16d203a9e562db4d411ce21f8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
