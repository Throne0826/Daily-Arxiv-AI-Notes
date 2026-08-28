---
title: "[论文解读] RuleWeaver: Benchmarking Rule-Centered Scenario Reasoning for Large Language Models"
description: "[arXiv 2608.26832][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.26832"
announcement_date: "2026-08-28"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:33:20.612060+00:00"
source_sha256: "ab288abbaa17acafc13b8ef1d6d34a5edfc010569944a7fbf83789370f982e1a"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大型语言模型"
  - "规则中心场景推理"
  - "复杂规则"
  - "规则依赖链"
  - "过程级评测"
  - "基准构建"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.26832</p>

# RuleWeaver: Benchmarking Rule-Centered Scenario Reasoning for Large Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Bohan Yu, Shi-Yang Li, Pengfei Cao, Jun Zhao, Kang Liu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: School of Advanced Interdisciplinary Sciences, University of Chinese Academy of Sciences；Affiliation: The Key Laboratory of Cognition and Decision Intelligence for Complex SystemsInstitute of Automation, Chinese Academy of Sciences；Affiliation: School of Artificial Intelligence, University of Chinese Academy of Sciences</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26832v1) · [PDF 下载](https://arxiv.org/pdf/2608.26832v1) · **关键词** 大型语言模型, 规则中心场景推理, 复杂规则, 规则依赖链, 过程级评测, 基准构建<br>
**代码**: [https://github.com/SharkSpicy-NLP/RuleWeaver](https://github.com/SharkSpicy-NLP/RuleWeaver)

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

RuleWeaver位于大型语言模型的规则推理评测领域，关注模型能否在具体自然语言情境中识别、解释并组合领域规则，而不只是遵守输出格式或完成抽象逻辑题。论文将基础规则统一表示为语料中抽取的“如果条件成立，则产生结果”的IF-THEN元规则，再通过抽象化、附加条件、语义否定、例外、冲突和强制优先级六类语义增强构造复杂规则；其中前三类主要改变规则的粒度、范围或极性，后三类进一步改变规则是否适用、规则结论是否兼容以及冲突时谁优先。评测重点因此包括三个可分离的能力：找到情境相关规则、沿依赖链正确应用规则，以及据此形成完整答案。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**IF-THEN元规则（Meta Rule）**

一种原子化条件规则：IF部分描述触发条件，THEN部分描述条件满足后可推出的结果。RuleWeaver从真实语料抽取这类规则，并把它们作为后续复杂化和场景构造的基本单元。

</div>
<div class="concept-item" markdown="1">

**规则依赖链**

若一条规则产生的中间结论被另一条规则当作触发依据，两次规则应用之间就存在依赖。多个依赖步骤组成有向推理结构，可表现为顺序传递、分支、汇合或多层聚合。

</div>
<div class="concept-item" markdown="1">

**过程级评测**

除判断最终答案是否正确外，还检查模型找到了哪些规则、这些规则是否用对，以及中间推理是否满足实例专属评分标准。它用于区分“偶然答对”与“依据正确规则和依赖关系答对”。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

每个评测实例向模型提供一个自然语言场景、一个最终问题，以及同时含相关规则与干扰规则的可见规则池。五条相关复杂规则来自互不相同的规则组，以避免同一元规则的近似变体同时进入实例；同源设置从一个来源语料抽取这些规则，跨源设置则跨四个来源组合。问题覆盖多事项综合、确定性结论推导、事件预测、优先级裁决、特殊情形判断、反事实修改和行动建议七类。模型需要输出最终答案及其引用或应用的规则标识；评测分别考察实例专属量规下的答案质量、相关规则召回情况和已引用规则的正确应用情况。该设定假定场景中嵌入了触发规则所需的事实，但不会直接泄露规则标识、隐藏子问题或中间结论。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{R}=\{r_1,\ldots,r_5\}$**

单个场景实例使用的五条相关复杂规则集合，其中每条规则来自不同规则组。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{G}$**

参考标注中的相关规则标识集合，即模型原则上应识别的规则。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{C}$**

模型在答案中引用或声称应用的规则标识集合。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{A}$**

模型所引用规则中，经参考答案判定为应用正确的规则应用集合。

</div>

</div>

**直接相关的工作**

- **IFEval（Zhou et al., 2023）**: 论文将其归为指令遵循基准：主要检查模型输出是否满足显式约束，而非围绕语料来源规则构造场景、追踪多步规则依赖并评价规则应用过程。表1据此将其列出的四项核心维度均标为不支持。
- **RuleArena（Zhou et al., 2025）**: 这是表1中与RuleWeaver最接近的逻辑推理基准：支持语料衍生规则和规则中心场景问答，并部分支持多来源或跨领域组合；但论文标示其不支持细粒度语义规则类型。RuleWeaver试图同时覆盖语料衍生规则、语义规则类型、规则中心场景问答和跨来源组合四个维度。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在政策、流程、合同和叙事等专业场景中，模型不能只生成表面上合理的答案，还必须从具体情境中找出相关规则，区分条件、禁止、例外、冲突和优先级等不同作用，并按照规则之间的依赖关系作出决定和解释。若模型遗漏关键规则或错误处理规则之间的关系，其回答即使语言流畅，也可能导致不可靠的判断。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **指令遵循基准**：这类基准主要检查模型是否遵守自然语言指令中的输出格式、内容范围和表达风格等约束。它们关注的是模型最终应当以什么形式回答，而不是模型如何识别并运用情境中的规则来完成判断。
- **逻辑推理基准**：这类基准通常预先提供一组规则和事实，要求模型依据它们推出结论。它们能够测试从规则到结论的演绎能力，但通常不充分模拟现实场景中规则的识别、角色区分、例外处理、冲突解决和依赖追踪。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 指令遵循基准把重点放在输出层面的约束，难以判断模型是否在具体场景中找到了真正相关的规则并据此进行决策；因此，模型可能形式上完全遵循指令，却没有完成可靠的规则中心推理。
- 现有逻辑推理基准多在相关规则已经明确给出的条件下评估结论是否正确，且没有充分区分规则的不同语义作用及其相互依赖；因此，它们难以揭示模型是否遗漏规则、误用规则，或错误处理例外、冲突与优先级。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有评测缺少一种面向真实文本规则的统一框架：该框架既要把语料中的自然规则构造成具有不同语义角色的复杂规则，又要将这些规则嵌入需要主动识别和组合规则的具体情境，还要超越最终答案正确性，分别评估规则找全了没有、应用是否正确以及整体推理过程的质量。

</div>
<div markdown="1"><span>核心问题</span>

如何构建并验证一个规则中心的情境推理基准，使其能够系统评估大语言模型在复杂场景中识别相关规则、理解规则角色及依赖关系、正确应用规则并给出有依据回答的能力？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是先从真实语料中提取单一条件到单一结果的基础规则，再通过语义增强生成包含补充条件、语义反转、例外、冲突和优先级等变化的复杂规则，最后把这些规则组合进需要多步判断的情境问答中。这样，测试难点不再只是记住或套用一条显式规则，而是要求模型像处理现实政策或合同一样，先找出相关规则，再判断它们如何共同决定答案；同时保留规则应用标注和针对实例的评分标准，也能区分“答案碰巧正确”与“推理过程真正可靠”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

RuleWeaver 是一个用于评估大语言模型规则中心场景推理能力的可追溯基准构建框架。它先从真实语料中抽取原子化的 IF-THEN Meta Rule，再通过六类语义增强逐步生成复杂规则，随后把五条彼此独立的相关规则组织成具有显式依赖链的场景问答实例。模型评测时接收场景、问题以及包含相关规则和干扰规则的可见规则池，输出最终答案和所引用或应用的规则标识；系统分别计算基于量规的答案质量、规则召回率和规则精确率，从而区分“答得对不对”“找全规则没有”以及“找到的规则用对没有”。直观地说，该方法不是只检查模型最后写出的结论，而是像检查一份解题过程：既看答案，也看模型是否找到了正确的依据并沿着正确的依赖关系使用它。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### Meta Rule 抽取与筛选

系统从四类语料中抽取具有单一触发条件和单一结果的原子 IF-THEN 规则，并依据格式有效性、原子性、语义清晰度以及是否依赖外部背景知识进行筛选；随后通过代表性聚类和人工检查减少重复、提升来源与表达多样性。

<div class="method-step__io" markdown="1">

**输入**：来自 GovReport、WikiHow、CUAD 和 BookSum 的文档，分别对应政策报告、操作指南、合同条款和叙事语境。<br>
**输出**：初始抽取得到 11,145 条 Meta Rules，质量筛选后保留 200 条高质量 Meta Rules。每条规则都保持清晰的 IF-THEN 结构，并保留其语料来源信息。

</div>

**直观理解**：先从真实文本中找出最小的“如果满足某条件，就产生某结果”的规则，再把含糊、重复或必须依赖常识才能理解的规则删掉。这样做相当于先准备一批可靠的积木，而不是直接凭空编写复杂题目。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 渐进式复杂规则构造

对每条 Meta Rule 执行五轮渐进式增强。前四轮从 ABSTRACT、ADDITIVE 和 NEGATE 中采样一种中等强度增强，并作用于 IF 侧、THEN 侧或两侧；第五轮进一步分支，引入一种中等增强或 EXCEPTION、CONFLICT、IRONCLAD 之一，并记录增强类型、修改位置和逻辑组合方式（AND、OR 或 NOT）。

<div class="method-step__io" markdown="1">

**输入**：200 条经过筛选的 Meta Rules。<br>
**输出**：形成 200 个复杂规则组；每个规则组的变体都能追溯到初始 Meta Rule、增强轮次、修改位置和逻辑组合，同时覆盖六种语义类型。

</div>

**直观理解**：复杂规则不是一次性写成，而是像逐层改写同一条规则：可以补充条件、缩小或扩展范围、反转语义，也可以加入例外、冲突和优先级。每次修改都留下记录，因此之后能判断模型究竟在哪一种规则变化上出错。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 依赖驱动的场景问答生成

生成器先制定规则依赖计划，规定每个推理步骤应用哪条规则以及中间结论如何支持后续步骤；再为每一步生成包含触发事实的局部子场景，并在最终合成时将其整合为连贯场景、问题、规则应用标注、规则逻辑链和实例专属量规。实例支持 same-source 设置（五条规则来自同一数据集）和 cross-source 设置（规则跨四个数据集采样）。

<div class="method-step__io" markdown="1">

**输入**：复杂规则组；每个实例从不同规则组中采样五条规则，组成规则集合 $\mathcal{R}=\{r_1,\ldots,r_5\}$；目标问题类型从七类中选择，包括多问题综合、确定性结论推导、事件预测、优先级仲裁、特殊情形判断、反事实修改和行动处方。<br>
**输出**：得到规则中心场景 QA 实例。论文总体构建了 96 个实例，且每个实例附带用于追踪规则依赖和评分的参考输出、规则逻辑链及量规。

</div>

**直观理解**：先画一张“解题路线图”，再按路线图逐步写出局部事实，最后把这些局部片段拼成一个自然故事。场景不会直接告诉模型规则文本、规则编号或隐藏小问题，模型必须从情境中的事实自己找出哪些规则被触发，以及前一步结论怎样影响后一步。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 质量审查与过程级评分

候选实例通常经过约五轮质量控制：启发式检查 JSON 格式和直接使用规则的覆盖情况，基于大语言模型的评审检查依赖结构、规则覆盖、信息泄漏和依赖传递，超过 80 分质量阈值的实例再接受人工检查。评测时分别计算量规答案质量、规则召回率和规则精确率。

<div class="method-step__io" markdown="1">

**输入**：候选场景 QA、其规则依赖计划、规则标注、逻辑链和量规；评测阶段还输入模型生成的最终答案与规则标识集合。<br>
**输出**：输出经过筛选的基准实例，以及模型层面的 $S_{\mathrm{rubric}}$、$S_{\mathrm{recall}}$ 和 $S_{\mathrm{precision}}$ 三类分数；三者分别对应答案维度满足情况、相关规则找回程度和所引用规则的正确应用程度。

</div>

**直观理解**：这一阶段既检查题目本身是否能正常使用，也检查模型的过程表现。它避免只用最终答案“一票判定”：模型可能碰巧答对但没有找到全部规则，也可能找到很多规则却错误地应用它们，这些情况会被分开记录。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 量规答案质量分数

$$
S_{\mathrm{rubric}}=\sum_{i\in\mathcal{I}}w_i b_i
$$

**符号说明**

- $\mathcal{I}$：实例专属量规的评分维度集合。
- $w_i$：第 $i$ 个评分维度的分值，且所有维度分值之和为 100。
- $b_i$：二值指示变量；当模型答案满足第 $i$ 个维度时为 1，否则为 0。
- $S_{\mathrm{rubric}}$：模型答案获得的量规总分。

<div class="equation-explanation" markdown="1">

**直观理解**：每个量规维度只有“满足”或“不满足”两种状态：满足就拿到该维度全部分值，否则得零分。该设计强调关键推理要求是否完整实现，而不是用部分正确的模糊平均替代结构性判断。<br>
**原文位置**：第 3.4 节 Scoring Design

</div>

</div>

<div class="equation-block" markdown="1">

#### 规则召回率与规则精确率

$$
S_{\mathrm{recall}}=\frac{|\mathcal{C}\cap\mathcal{G}|}{|\mathcal{G}|},\qquad S_{\mathrm{precision}}=\frac{|\mathcal{A}|}{|\mathcal{C}|}
$$

**符号说明**

- $\mathcal{G}$：参考答案中所有相关规则标识组成的集合。
- $\mathcal{C}$：模型引用或声称应用的规则标识集合。
- $\mathcal{A}$：模型所引用且相对于参考答案被判定为正确的规则应用集合。
- $S_{\mathrm{recall}}$：模型找回的相关规则占全部金标准相关规则的比例。
- $S_{\mathrm{precision}}$：模型引用的规则应用中被判定正确的比例；若模型未引用规则，该分数设为零。

<div class="equation-explanation" markdown="1">

**直观理解**：召回率回答“该找的规则找全了吗”，所以分母是全部相关规则；精确率回答“你说用到的规则有多少真的用对了”，所以分母是模型引用的规则。把两者分开后，可以区分漏掉依据和乱用依据这两类错误。<br>
**原文位置**：第 3.4 节 Scoring Design

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。RuleWeaver 是基准构建与评测框架，而不是提出需要训练的新模型；文中没有定义用于优化模型参数的训练损失。生成规则、场景和质量反馈依赖 DeepSeek-V4-Pro，但这些生成过程属于数据构建流程，不等同于被评测模型的参数训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 可追溯的规则增强模块**

每次增强由语义增强类型、修改位置和逻辑组合方法三个属性描述。六类增强为 ABSTRACT、ADDITIVE、NEGATE、EXCEPTION、CONFLICT 和 IRONCLAD；其中前三类主要改变规则的粒度、范围或极性，后三类主要改变适用性、兼容性或优先级。

> 直观理解：模块把“规则变复杂”的方式拆成明确类别，而不是笼统地增加难度。研究者因此可以知道题目要求的是处理例外、解决冲突，还是识别优先级，而模型错误也更容易定位。

**2. 规则依赖计划与逻辑链模块**

依赖计划是规则应用步骤上的有向结构，支持独立根规则、顺序依赖传递、分支、多个结论汇合和多层聚合。最终规则逻辑链为每一步记录规则标识、依赖关系、触发事实、中间结论及其对下游步骤的贡献。

> 直观理解：它相当于在题目生成前先画出一张推理流程图。模型不仅要判断某条规则是否适用，还要保留中间结果，并把它正确传给后续规则；因此测试的是链式推理，而不只是单条规则匹配。

**3. 过程级评分模块**

模型看到最终场景、问题和同时包含相关规则与干扰规则的规则池，并返回答案及其引用或应用的规则标识。答案质量使用实例专属的 100 分全有或全无量规；规则检索和应用则分别由规则召回率与规则精确率衡量，未引用任何规则时规则精确率设为零。

> 直观理解：规则池中的干扰项迫使模型进行选择，而不是默认所有规则都相关。三种分数像三道检查：是否满足关键答题要求、是否找到了该找的规则、是否把声称使用的规则真正用正确。

**训练与推理**

数据构建阶段，先从四个语料库抽取并筛选 Meta Rules，再经过五轮增强得到复杂规则组。之后对每个实例采样五条不同规则组中的规则，选择七类问题之一，生成依赖计划和局部子场景，合成最终场景及其参考标注；候选实例经过启发式检查、基于大语言模型的多轮审查和人工质量保证后纳入基准。推理阶段，向待测 LLM 提供最终场景、问题和含相关规则及干扰规则的可见规则池；模型输出最终答案以及引用或应用的规则标识，评测器据此计算量规分数、规则召回率和规则精确率。论文未描述被测模型需要额外训练、微调或使用检索增强。

**复现信息**

复现或公平解读时，关键设置包括：规则来自 GovReport、WikiHow、CUAD 和 BookSum；每个 QA 实例使用五条来自不同规则组的相关复杂规则，以避免同一 Meta Rule 的兄弟变体同时出现；same-source 与 cross-source 分别表示规则来自单一数据集或跨四个数据集。场景生成的四个阶段均使用 DeepSeek-V4-Pro；质量审查通常运行五轮，候选实例需超过 80 分质量阈值后再进行人工检查。基准规模为 200 个复杂规则组和 96 个场景 QA 实例；规则增强类型、依赖计划、规则逻辑链及实例专属量规共同提供了过程可追踪性。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- RuleWeaver 的主评测集包含 96 个复杂场景问答实例，每个实例有 5 条金标准规则。主实验为每题提供包含 200 条复杂规则的候选池，用于同时测试从干扰规则中检索相关规则及正确应用规则的能力。
- 同源组成子集包含 48 个对齐实例，场景所需规则来自相同来源；其作用是提供相对受控的规则组合条件，并作为跨来源实验的比较基准。
- 跨来源组成子集包含 48 个对齐实例，组合来自不同来源的规则；其作用是测试模型面对异质规则表达、语义和潜在交互时的迁移与整合能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**规则召回率（Rule Recall）**

从回答中检测模型明确引用的规则标识符，再与该题所需的金标准规则集合比较；衡量模型找全必要规则的程度。它不直接判断规则是否被正确解释或应用。 （越高越好，因为漏掉必要规则通常会破坏后续推理链。）

</div>
<div class="metric-item" markdown="1">

**规则精确率（Rule Precision）**

衡量模型所引用规则中有多少被正确选择并应用，侧重排除无关引用或错误用法；它与召回率互补，高精确率不等于找全了规则。 （越高越好，因为这表示模型较少引用或使用不恰当的规则。）

</div>
<div class="metric-item" markdown="1">

**Rubric 综合评分**

由评判模型依据细粒度评分规约评价答案，覆盖问题理解、议题分解、规则支撑、依赖链对齐、例外或冲突处理、中间结论、最终一致性等维度，并归一到 0–100 分。该指标用于评价推理过程与答案质量，而不只是最终答案是否碰巧正确。 （越高越好，因为更高分表示答案在规则依据、多步推理和最终综合方面更完整；但其可靠性仍依赖自动评判与规约质量。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 200 条复杂规则下的同源与跨来源主评测

<div class="result-value" markdown="1">

同源条件下，GPT-5.5 的 Rubric 分数最高，为 53.83，同时规则精确率最高，为 74.58%；Kimi-K2.6 的规则召回率最高，为 72.92%。跨来源条件下，Claude-Opus-4.6 的 Rubric 分数和召回率最高，分别为 50.27 与 62.50%，而 GPT-5.4 的精确率最高，为 78.64%。

</div>

没有模型同时在所有维度和来源设置上占优，说明“找全规则”“少用错规则”和“把规则组织成正确答案”是不同能力。最高 Rubric 分数仅略高于满分的一半，表明即使领先通用模型也未解决复杂规则场景推理。该结果只比较了所选 96 个实例、指定提示与解码设置，不能证明某模型在所有专业领域或所有规则任务中普遍最强。

<div class="result-source" markdown="1">

来源：第 4.3 节 Overall Performance，表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under same-source composition, GPT-5.5 obtains the highest rubric score (53.83) and rule precision (74.58), while Kimi-K2.6 achieves the highest rule recall (72.92). Under cross-source composition, Claude-Opus-4.6 is strongest in both rubric score (50.27) and rule recall (62.50), whereas GPT-5.4 obtains the highest rule precision (78.64).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨来源规则相对于同源规则的总体影响

<div class="result-value" markdown="1">

在 11 个模型上取平均后，跨来源组成使规则召回率下降 11.93 个百分点、Rubric 分数下降 4.05 分，但规则精确率反而上升 2.42 个百分点。

</div>

跨来源规则主要使模型更难找全并综合所有必要规则，而不是简单导致更多错误引用。精确率小幅上升可能意味着模型在困难条件下引用得更保守，不能据此判断其整体推理变好；召回和综合评分的下降恰好表明这种保守策略可能漏掉关键规则。该比较揭示相关性，但没有单独控制规则措辞、领域差异等所有潜在因素。

<div class="result-source" markdown="1">

来源：第 4.3 节 Overall Performance，表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Averaged over the 11 models, cross-source evaluation reduces recall by 11.93 points and rubric score by 4.05 points, while precision increases slightly by 2.42 points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 200 条规则条件下的评分维度与错误类型诊断

<div class="result-value" markdown="1">

模型在“不使用外部事实”和“引用格式合规”上分别达到约 91.2% 和 82.8%，但依赖链对齐仅为 14.2%，中间结论质量为 21.0%，议题分解为 28.4%，例外或冲突处理为 30.4%。错误分析中，多步整合错误最常见，占 86.7%；即使只看规则全部召回的回答，多步整合错误仍有 74.9%，已引用规则的应用错误仍有 65.6%。

</div>

主要困难不是遵守输出格式或避免外部知识，而是维护跨步骤的规则依赖：模型可能已经找到规则，却无法正确生成、复用和连接中间结论。全召回子集仍有大量应用与整合错误，因而仅改进检索不足以解决任务。错误类别允许同一回答同时被计入多类，所以这些比例不能相加解释为互斥的失败分布。

<div class="result-source" markdown="1">

来源：第 4.3 节 Rubric-Dimension Performance 的表 3；第 4.4 节 Error Type Analysis 的表 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 4, the most frequent error is multi-step integration (86.7%), followed by rule selection (72.2%) and rule interaction (69.5%). In the full-recall subset, multi-step integration errors (74.9%) and cited-rule application errors (65.6%) remain frequent, suggesting that models often fail not only by missing relevant rules, but also by misusing retrieved rules or failing to connect intermediate conclusions.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主评测只有 96 个实例，每个来源设置为 48 个实例，因此部分领先模型之间的差异不稳定。配对 bootstrap 中，同源 GPT-5.5 相对 GPT-5.4 和 Claude-Opus-4.6、跨来源 Claude-Opus-4.6 相对 GPT-5.4 和 GPT-5.5 的 95% 置信区间均跨越 0，不能据此断言这些相近模型存在显著且可泛化的优劣次序。
- Rubric 分数主要由 DeepSeek-V4-Flash 自动生成。尽管人工审计和替代评判器显示较高相关性，评判器—人工相关仍低于人工—人工相关，说明评分可能保留系统性偏差；此外，非统一的推理模式与温度设置，尤其 Kimi-K2.6 使用温度 0.6，也会削弱模型间完全受控比较的程度。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Claude 系列：Claude-Opus-4.6 与 Claude-Sonnet-4.6。它们是主要闭源模型家族之一，可检验高性能通用模型在规则检索和长链整合上的上限。
- OpenAI 系列：GPT-5.4 与 GPT-5.5。GPT-5.5取得同源条件下最高综合评分，因此也是判断其他模型与领先水平差距的重要参照。
- Gemini-3.1-Pro-Preview 与 Deepseek-V4-Pro：代表另外两个模型家族，可用于观察结果是否只属于单一供应商或模型谱系。
- Qwen3.5-Plus、Doubao-Seed-2.0-pro、GLM-5、Kimi-K2.6 与 MiniMax-M2.7：扩展模型覆盖面，用于比较不同系统在规则召回、引用精度和最终推理质量之间的取舍。

**实验想回答的问题**

- 在包含大量候选复杂规则的具体场景中，当前代表性大语言模型能否完整找出所需规则、正确使用这些规则，并据此形成高质量的多步答案？
- 规则来源异质性、推理链结构与候选规则池规模如何影响模型表现，主要瓶颈究竟来自规则检索，还是来自规则交互和中间结论的多步整合？

**实验实现**

共评测 11 个模型。可配置时关闭推理模式，并将解码温度设为 0，以减少随机性；Kimi-K2.6 的非思考模式因 API 限制使用温度 0.6，Gemini-3.1-Pro-Preview 使用 low thinking 配置。DeepSeek-V4-Flash 作为主要自动评判模型，温度为 0。主结果采用 200 条复杂规则条件；每个来源设置包含 48 个对齐问答实例。作者还以 20,000 次有放回 bootstrap 构造 95% 置信区间，并通过人工审计及 Grok-4.3、Gemini-3-Flash 替代评判器检查自动评分的可靠性与模型家族偏差。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 场景推理链复杂度：推理深度、依赖负载与结构分支 | 平均 Rubric 分数随推理深度从 2 增至 4 而由 68.1 降至 40.0、再降至 31.2；依赖负载从没有依赖规则步骤增至 3 个时，分数由 68.1 降至 28.0。相比之下，无分支与单分支场景的平均分相近。 | 这一分析区分了“链更长”“更多规则依赖先前结论”和“一个节点通向多个后续步骤”三类结构复杂度。结果表明，顺序推理深度及中间结论复用比简单分支更能解释性能下降。不过这些实例并非随机控制实验，不同复杂度组可能还同时存在语义或题型差异，因此结果更适合视为结构难度信号，而不是严格因果效应。 | 第 4.4 节 Scenario Complexity Analysis，图 3(a)<br><span class="experiment-evidence">Mean score decreases from 68.1 at depth 2 to 40.0 at depth 3 and 31.2 at depth 4, indicating that longer rule chains are substantially harder for current models. Dependency load shows a similar trend: scores decline from 68.1 with no dependent rule step to 28.0 with three dependent rule steps.</span> |
| 候选规则池规模：仅提供金标准规则、100 条规则与 200 条规则 | 随着规则池扩大，三个受测模型总体表现下降。MiniMax-M2.7 的退化最明显：召回率从 84.8% 降至 58.5%，精确率从 56.2% 降至 45.3%，Rubric 分数从 40.5 降至 25.4。 | 该对照主要隔离候选干扰规则数量的影响：仅提供金标准规则时几乎不需要检索，而 100 或 200 条规则要求模型从更多候选项中筛选。召回、精确率和综合分共同下降，说明规则池扩大不仅增加漏检，还会影响规则应用与最终整合。但该实验只报告 MiniMax-M2.7、Kimi-K2.6 和 Claude-Sonnet-4.6 三个模型，不能直接假定所有模型具有相同降幅。 | 第 4.4 节 Rule-Pool Size Sensitivity，图 3(b)<br><span class="experiment-evidence">MiniMax-M2.7 shows the clearest degradation, with recall dropping from 84.8 to 58.5, precision from 56.2 to 45.3, and rubric score from 40.5 to 25.4.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces a benchmark and process-level metrics specifically for evaluating LLM reasoning over complex rules.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`ab288abbaa17acafc13b8ef1d6d34a5edfc010569944a7fbf83789370f982e1a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
