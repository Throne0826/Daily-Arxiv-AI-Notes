---
title: "[论文解读] Position: Reasoning is a Learnable Rule-Based Process"
description: "[arXiv 2608.12325][LLM Reasoning] 本文主张先以可操作定义明确“推理”这一研究对象，再将有效且可靠的推理界定为可学习的、基于精确规则应用的过程，从而使生成式人工智能的推理评测具备可检验的构念效度。"
arxiv_id: "2608.12325"
announcement_date: "2026-08-14"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T03:03:26.371744+00:00"
source_sha256: "66729d184e93ae6ba0fbe584fe3e5fb23b2c5164b704869e8148b8aec3f276e1"
tags:
  - "LLM Reasoning"
  - "人工智能推理"
  - "操作性定义"
  - "规则式过程"
  - "构念效度"
  - "大型推理模型"
  - "可信人工智能"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.12325</p>

# Position: Reasoning is a Learnable Rule-Based Process

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Rachel Lawrence, Jacqueline Maasch</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12325v1) · [PDF 下载](https://arxiv.org/pdf/2608.12325v1) · **关键词** 人工智能推理, 操作性定义, 规则式过程, 构念效度, 大型推理模型, 可信人工智能<br>
**代码**: [https://github.com/jmaasch/valid_reasoning](https://github.com/jmaasch/valid_reasoning)

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

本文主张先以可操作定义明确“推理”这一研究对象，再将有效且可靠的推理界定为可学习的、基于精确规则应用的过程，从而使生成式人工智能的推理评测具备可检验的构念效度。

**不用术语来说**：当前研究常根据模型是否答对题目来判断它是否会推理，但正确答案也可能来自记忆、猜测、数据污染或对表面模式的模仿。由于研究者尚未普遍说明“推理”究竟指什么、应观察什么证据，同一项结果可能被赋予不同含义，模型看起来像在推理，也无法证明其内部确实执行了可靠的推理过程。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 综合逻辑学、可验证自动推理与生成式人工智能文献，提出方法无关的操作性定义：推理是依据先前信念与当前证据，选择并精确应用规则序列以更新信念状态的过程；该定义可兼容符号、神经和混合方法。
- 提出面向人工智能推理研究的科学交流检查清单，要求研究者明确所研究的推理现象、说明评测代理指标与该定义之间的关系，并区分推理过程、规则选择和最终输出。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于生成式人工智能推理评估与可信人工智能的交叉领域。当前的大型推理模型（LRM）通常是在推理任务上微调的大语言模型（LLM），其能力主要通过问答准确率、静态基准和思维链文本来评价；但“推理”本身尚缺少被广泛采用的操作性定义。论文因此把研究焦点从模型是否给出正确答案，转向模型是否执行了可明确描述和检验的推理过程，并主张用兼容符号方法、神经方法与混合方法的定义来统一讨论。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**操作性定义（operational definition）**

把“推理”这类抽象概念转化为可观察、可测量和可复核的判定条件。它不要求整个领域接受唯一哲学定义，但要求每项研究说明自己测量的现象究竟是什么。

</div>
<div class="concept-item" markdown="1">

**构念效度（construct validity）**

指实验指标是否确实测到了研究声称关注的抽象构念。例如，问答准确率能测量答案是否正确，却不必然证明产生答案的内部过程属于推理。

</div>
<div class="concept-item" markdown="1">

**有效推理与可靠推理（valid and sound reasoning）**

本文将推理视为对规则的选择与精确应用，并把“有效性”归因于规则是否被准确执行，而不取决于规则如何被选中。可靠性还要求推理所依据的前提或信念具有适当保证，但所给节选尚未完整展开其形式条件。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文研究的不是一个给定数据集上的预测任务，而是生成式人工智能研究中“如何定义并测量推理”的元研究问题。分析对象是一个接收既有信念、当前证据或任务状态的系统；作者把推理非正式地定义为：系统选择并依次应用规则，使状态演化并得到有原则的信念更新或输出。这里的规则可以是定理、函数、策略，也可以包含随机性、不确定性和近似规则；关键假设是推理属于过程而非最终产物，且过程有效性来自规则的精确应用。因此，仅观察正确答案或流畅的思维链不能充分识别真实推理，因为模型也可能依靠记忆、猜测、数据污染或表面模仿得到相同输出。本文的目标输出是方法无关的操作性定义及科研交流检查清单，而不是新的模型、训练算法或推理基准；作者也明确不判断现有 LRM 能在多大程度上推理。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathrm{LRM}$**

大型推理模型，即针对推理任务进行微调的大语言模型。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{LLM}$**

大语言模型，是当前生成式人工智能系统的主要模型类型。

</div>
<div class="notation-item" markdown="1">

**$r\text{-}\mathrm{zombie}$**

“推理僵尸”：外在行为看似自主推理，但缺少有效内部推理机制的系统。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{CoT}$**

思维链，即模型用自然语言生成的中间步骤；本文强调它不一定忠实反映模型内部决策过程。

</div>

</div>

**直接相关的工作**

- **Huang and Chang (2023)**: 该工作被用于界定 LRM，并指出生成式人工智能中的推理“there is not a clear definition of what it entails”。本文以此作为定义缺乏共识的直接依据，进一步要求研究者先给出操作性定义，再论证评价指标的构念效度。
- **Chollet (2019)**: 该工作强调不能把智能过程与其产物混为一谈，并讨论通过大量先验经验获得的任务表现为何不足以证明推理。本文将这一观点具体化为“推理是过程而非输出”，据此质疑用问答准确率单独证明模型具有推理能力。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大型推理模型已被快速用于需要自主判断的场景，而其用户采用速度超过了可信推理证据的积累。与此同时，推理被视为实现通用人工智能的必要但非充分条件；若研究界不能可靠地识别和衡量推理，就既无法量化通向通用人工智能的进展，也无法判断现实应用究竟需要真正的推理机制，还是只需能产生推理式语言的系统。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **静态基准与问答正确率评测**：让模型在预先构造的推理任务或问答数据集上生成答案，再以最终答案是否正确衡量模型的推理能力；这种做法将可直接观测的任务表现作为抽象推理能力的代理指标。
- **生成式模型的行为表现与自然语言推理轨迹评估**：依据模型能否输出看似连贯的解释、步骤或推理式文本来判断其推理水平，通常关注外部行为，而不要求证明这些文本由有效的内部规则应用机制产生。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有研究经常缺少明确且统一的操作性定义，或使用含义宽泛、彼此错位的“推理”概念，导致评测指标究竟测到了什么无法验证，也使研究者能够移动评价目标，形成表面共识却难以比较真实进展。
- 最终答案正确或语言轨迹像推理，并不能识别答案的生成机制；模型可能依靠记忆、猜测、数据污染、基准过拟合或表面线索取得高分。因此，把推理过程与其输出产物混为一谈，会把“推理僵尸”误判为真正的自主推理系统。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一套可操作、可检验且与具体实现路线无关的框架，用来同时界定推理过程、区分规则选择与规则应用，并据此论证评测指标对“推理”这一抽象构念的效度。该框架还需能够连接符号推理的历史定义与神经生成模型的现代实践，而不预设必须采用符号、纯数据驱动或神经符号架构。

</div>
<div markdown="1"><span>核心问题</span>

如何给出一种适用于生成式人工智能、又兼容符号与神经方法的推理操作性定义，使研究者能够检验模型是否执行了有效的规则应用过程，并判断现有评测是否真正测量了所声称的推理能力？

</div>
<div markdown="1"><span>作者直觉</span>

如果把推理理解为“选择规则并精确执行规则”的过程，就可以把原本含混的能力声明拆成可检查的问题：系统使用了什么输入和规则、规则是否被正确应用、状态如何更新，以及结论是否由这些步骤得到。这样既允许规则通过数据学习，也允许规则表达随机性、不确定性和近似计算；关键不在规则是否由人手写，而在研究者能否说明并验证从输入到结论的过程。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是提出可训练模型或推理加速算法，而是建立一套用于定义、实现和审计“推理”的操作化框架。其核心观点是：推理应被刻画为一个过程，即系统在当前信念、外部证据与状态的约束下选择规则，并精确应用这些规则以更新信念或状态；规则可以由数据学习，因而“基于规则”不等于人工硬编码或传统专家系统。作者进一步区分规则选择与规则应用：规则可以选错，但只要所选规则被精确执行，该推理过程仍满足作者定义的有效性；若规则及初始前提还与目标语义或真实环境相符，则进一步涉及可靠性。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 界定领域中的推理现象

先给出形式化、可操作且与具体领域对应的推理定义，并将“推理过程”与答案、证明文本、思维链等过程产物分开。定义需要说明过程、规则、信念、证据和状态在该任务中分别指什么；若某个成分不存在，也应明确说明理由。

<div class="method-step__io" markdown="1">

**输入**：待研究的推理任务、系统行为以及研究者希望测量的能力。<br>
**输出**：可据以判断某次系统执行是否属于目标推理现象的操作化定义。

</div>

**直观理解**：这一步相当于先写清考试到底考什么，再设计题目和评分方式；答对一道题不能自动证明考生使用了指定的推理过程。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 表示初始信念、证据与规则

将任务输入映射为框架中的核心成分，并明确规则如何把推理输入变换为输出。规则可表示定理、函数、策略或包含随机性、不确定性与近似操作的映射，也可以通过机器学习获得，而不要求由人手工编写。

<div class="method-step__io" markdown="1">

**输入**：系统已有的信念、当前观测或新证据，以及可用规则或规则集合。<br>
**输出**：一个领域特定的推理状态及其可用规则空间。

</div>

**直观理解**：可以把信念理解为系统当前的“账本”，证据是新收到的信息，规则则规定哪些更新动作是允许的。规则可以是程序员写出的公式，也可以是模型从数据中学到的稳定变换。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 选择并精确应用规则

系统根据当前信息选择一个或一组规则，然后严格按照所选规则规定的映射执行更新。作者把有效性归因于精确的规则应用，而不把规则选择正确与否直接纳入有效性的定义。

<div class="method-step__io" markdown="1">

**输入**：当前状态、当前信念、新证据以及候选规则。<br>
**输出**：由规则产生的中间结论、动作或更新后的信念与状态。

</div>

**直观理解**：这里区分“选了哪条公式”和“有没有把公式算对”：选错公式属于决策问题，代入后没有照公式执行才破坏规则应用的有效性。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 迭代更新并产生推理结果

重复规则选择和精确应用，使信念随状态演化；不同领域可对更新方式施加不同约束，例如经典演绎通常只增加可推出的命题，而非单调逻辑允许有原则地撤回信念。迭代终止后，系统输出结论、证明、预测、动作或其他任务产物。

<div class="method-step__io" markdown="1">

**输入**：上一轮更新后的信念或状态，以及随后到达的证据。<br>
**输出**：最终信念状态与对应的任务输出，同时保留可供有效性审计的规则应用过程。

</div>

**直观理解**：它类似按明确规则逐步维护一份记录：每获得一条信息就更新一次，最后答案只是记录更新后的结果，不能替代对更新步骤本身的检查。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 贝叶斯规则作为迭代信念更新规则

$$
r_{\mathrm{bayes}} \coloneqq \left\{p(\theta\mid\mathcal{D})=\frac{p(\mathcal{D}\mid\theta)p(\theta)}{p(\mathcal{D})}\right\}
$$

**符号说明**

- $r_{\mathrm{bayes}}$：作为推理规则使用的贝叶斯更新规则
- $\theta$：需要推断的未知参数或假设
- $\mathcal{D}$：已经观测到的数据或证据
- $p(\theta\mid\mathcal{D})$：观察数据后关于参数的后验信念
- $p(\mathcal{D}\mid\theta)$：给定参数时观测到该数据的似然
- $p(\theta)$：观察当前数据前关于参数的先验信念
- $p(\mathcal{D})$：数据的边际概率，用于归一化后验分布

<div class="equation-explanation" markdown="1">

**直观理解**：该式不是整篇论文的训练目标，而是作者用来说明通用框架如何落到具体领域的实例：旧信念由先验 $p(\theta)$ 表示，新证据由数据 $\mathcal{D}$ 表示，精确应用贝叶斯规则后得到更新信念 $p(\theta\mid\mathcal{D})$。随着数据变化，系统可反复应用同一类规则进行有原则的信念修正。<br>
**原文位置**：§2.2，Example 2.2，Equation 1

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文是立场与概念框架论文，没有提出需要最小化或最大化的统一损失函数，也没有给出新的参数优化目标；“可学习”是对规则来源的兼容性主张，即规则可由机器学习获得，而不是一项具体训练算法。贝叶斯规则等公式用于展示领域映射，不应误读为本文所训练模型的目标函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 领域特定的操作化定义**

作者要求将抽象定义映射到具体问题中的过程、规则、信念、证据和状态，并把推理定义为规则作用下的状态或信念更新过程，而不是把最终答案或语言化轨迹直接等同于推理。该定义是方法无关的，可用于符号、神经和神经符号系统。

> 直观理解：它提供统一的检查模板，使不同技术路线可以在同一概念标准下比较，同时避免用“看起来会解释”代替“内部确实执行了所声明的推理”。

**2. 可学习的规则系统**

框架中的规则是从推理输入到输出的明确映射，可涵盖逻辑推理规则、概率更新公式、函数和强化学习策略，也允许处理随机性、不确定性与近似。规则允许从数据中学习，因此该模块不预设硬编码知识库，也不限定规则必须采用人类可读的符号形式。

> 直观理解：“基于规则”描述的是更新必须遵循某种确定下来的变换关系，并不表示所有规则都要由专家手写；神经网络学到的函数或策略也可能充当规则。

**3. 有效性与构念效度审计**

过程有效性检查所选规则是否被精确应用；评价层面的构念效度则检查数据集、指标和测试程序是否与论文声明的推理定义一致。该区分用于识别只产生合理答案或推理式语言、却无法证明内部机制符合定义的“推理僵尸”系统。

> 直观理解：一个系统可能猜中答案，也可能生成流畅的思维链，但这些现象本身不能说明它执行了目标规则；审计的作用是把结果正确、过程合规和测量合理三件事分开。

**训练与推理**

本文没有统一的模型训练流程。若将框架用于可学习系统，训练阶段的任务是从数据获得规则、规则集合或规则选择策略，并明确这些对象在领域定义中的含义；具体采用监督学习、强化学习或其他优化方式取决于实例，原文未规定。执行阶段则从初始信念和状态出发，接收当前证据，选择规则，精确应用规则产生更新，并根据后续证据反复迭代，最终输出结论或动作。对于经典自然演绎，初始输入是前提集合 $\Gamma$，规则集合固定，且各步没有新证据；若存在有限推导使结论 $\varphi$ 成立，则记为 $\Gamma\vdash\varphi$。对于贝叶斯推断，先验和观测数据随时间变化，系统重复应用贝叶斯规则更新后验。作者并未声称所有现有大语言模型都满足这一过程，也未提供提升大语言模型推理能力的具体实现。

**复现信息**

为使定义可操作，作者以自然语言、数学记号和 Algorithm 1 的伪代码表达框架，并提供简单、可编译的 Python 示例，用于展示各组成部分如何实例化以及有效性如何审计；代码仓库链接为 https://github.com/jmaasch/valid_reasoning。复现或采用该框架时，关键不是沿用某组超参数，而是完整记录具体任务中的规则、信念、证据、状态、规则选择方式、规则应用轨迹及其有效性检查。给定摘录未完整呈现 Definition 2.4 和 Algorithm 1 的正文，因此无法从现有材料可靠还原其全部形式化步骤或伪代码细节；原文也未报告模型规模、训练数据、优化器、推理采样参数或硬件配置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

原文未明确报告，或这里不需要额外前置概念。

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 本文未提供数据集实验、基线比较、统计检验或消融研究，因而不能据此判断所提操作性定义相较其他推理定义是否具有更高的预测效度、解释效度或实际评测效用。
- 原文提供的节选主要覆盖立场论证和研究规范，未给出对真实大型推理模型内部规则应用过程的可操作测量结果；因此，关于区分真实推理系统与仅产生推理式语言的系统是否在现实中普遍可行，仍属于作者主张，而非本文实验所证实的结论。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。

**实验想回答的问题**

- 原文未明确报告。

**实验实现**

本文是立场论文，不是提出并验证新模型的实证研究。原文明确说明，作者不试图刻画大型推理模型能够执行何种程度的推理，也不提出改善其推理能力的实际实现。因此，文中没有实验数据集、训练或测试划分、对照基线、定量指标、评测协议或可复现的模型实现细节。作者虽提到用简单的 Python 实现说明其操作性定义，并将定义应用于逻辑演绎、贝叶斯推断、强化学习和概率式下一词元预测等特殊情形，但这些内容属于概念示例，不构成模型性能实验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Develops operational definitions and research practices that frame AI reasoning as a learnable rule-based process.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`66729d184e93ae6ba0fbe584fe3e5fb23b2c5164b704869e8148b8aec3f276e1`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
