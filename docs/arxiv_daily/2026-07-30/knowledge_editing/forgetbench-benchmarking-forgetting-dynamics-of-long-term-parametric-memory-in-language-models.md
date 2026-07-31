---
title: "[论文解读] ForgetBench: Benchmarking Forgetting Dynamics of Long-Term Parametric Memory in Language Models"
description: "[arXiv 2607.26455][知识编辑] ForgetBench把知识编辑从“一次修改后是否答对”的静态测试，扩展为“经历连续参数更新后能记多久、如何遗忘”的时间性评估。"
arxiv_id: "2607.26455"
announcement_date: "2026-07-30"
primary_category: "knowledge_editing"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.824667+00:00"
source_sha256: "df2f3295648ffe6c8fbc95d5a18ae4ecec61eaec3a86f033953765880b7e863a"
tags:
  - "知识编辑"
  - "LLM 评测"
  - "LLM 其他"
  - "大语言模型"
  - "长期参数记忆"
  - "持续知识编辑"
  - "灾难性遗忘"
  - "遗忘曲线"
  - "参数干扰"
  - "概念型问答"
  - "场景型问答"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">知识编辑 · arXiv 2607.26455</p>

# ForgetBench: Benchmarking Forgetting Dynamics of Long-Term Parametric Memory in Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Ruxi Gu, Zhenliang Zhang, Wei Wang</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26455v1) · [PDF 下载](https://arxiv.org/pdf/2607.26455v1) · **关键词** 大语言模型, 长期参数记忆, 持续知识编辑, 灾难性遗忘, 遗忘曲线, 参数干扰, 概念型问答, 场景型问答<br>


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

ForgetBench把知识编辑从“一次修改后是否答对”的静态测试，扩展为“经历连续参数更新后能记多久、如何遗忘”的时间性评估。

**不用术语来说**：语言模型上线后可能不断学到新事实，但一次更新成功并不意味着该事实能经受后续更新：新知识写入参数时，可能干扰甚至覆盖先前知识。现有测试通常只在修改后立即提问，因此难以判断模型是否真正形成了可长期保存的记忆，也无法观察遗忘发生的速度、程度及不同知识之间的差异。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出ForgetBench，以按时间排序的连续知识编辑流和多阶段重复评测，系统刻画大语言模型参数记忆的获得、保持、衰减与覆盖过程。
- 设计互补的概念型问答与场景型问答：前者隔离原子事实以分析参数干扰，后者利用多智能体交互图表示结构化关系知识，并据此评估保持强度、时间衰减和跨实例稳定性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型在持续知识编辑中的长期参数记忆。知识编辑是指不进行完整重训练，而通过修改模型参数写入或更新事实知识；以往评测通常只检查一次编辑后目标答案是否正确、改写问法能否泛化，以及无关知识是否保持不变。ForgetBench关注不同问题：当模型依次接受许多参数更新时，较早写入的知识能否在后续更新造成的参数干扰下继续存在。它将记忆寿命按后续编辑操作的数量计算，并通过多阶段重复测试形成遗忘曲线，从而区别于上下文窗口中的临时信息利用、检索增强生成以及依赖外部存储的交互式记忆。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**长期参数记忆**

指编码在模型参数中、在当前输入结束后仍可保留的知识。本文考察这种知识经过多轮参数更新后是否衰退，而不是模型能否从上下文或外部数据库中重新找到信息。

</div>
<div class="concept-item" markdown="1">

**知识编辑**

指在不完整重训模型的情况下，有针对性地改变某项事实关联，例如让模型对特定问题输出新的答案。编辑可以直接修改权重，也可以由辅助模型预测更新量或先定位关键组件再实施修改。

</div>
<div class="concept-item" markdown="1">

**遗忘曲线与参数干扰**

遗忘曲线记录一项已编辑知识的表现如何随后续编辑次数增加而变化；后续编辑次数在本文中相当于“记忆年龄”。参数干扰是指不同编辑共同作用于内部参数，使先前知识被削弱、破坏或覆盖。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个大语言模型、知识编辑方法以及按时间排序的知识流，系统依次把每项新知识写入模型参数，并在多个编辑阶段反复测试先前写入的知识。评测包含两种互补设置：概念型问答用于隔离原子事实更新，以便受控观察不同编辑之间的干扰；场景型问答通过多智能体交互图引入结构化关系知识，用于检验相互关联的信息能否整体保留。输出不是单次编辑成功与否，而是知识随编辑阶段变化的表现轨迹及遗忘曲线，据此分析保留强度、时间衰减和不同实例之间的稳定性。该设置假定知识通过参数修改获得，记忆年龄由该知识之后发生的编辑操作数定义，因此评测对象是模型内部参数记忆，而非上下文、检索系统或外部记忆模块。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **MEMIT（Meng et al., 2022b）与 AlphaEdit（Fang et al., 2024）**: 二者代表直接参数编辑方法：MEMIT支持大规模多事实编辑，AlphaEdit通过约束更新空间来减少对无关知识的干扰。它们说明事实可以被定向写入模型参数，但既有静态评测不足以揭示这些编辑在连续更新后的长期存活情况。
- **zsRE（Levy et al., 2017）、CounterFact（Meng et al., 2022a）与 UnKE（Deng et al., 2024）**: 这些知识编辑基准主要测量编辑成功、改写泛化以及非目标知识保持，并通常把每次编辑视为独立操作。ForgetBench在此基础上引入有时间顺序的连续编辑和跨阶段重复评测，以观察累积干扰、长期保留与遗忘动态。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

持续部署的语言模型需要反复吸收和更新知识。可靠适应不仅要求新知识能够被写入参数，还要求先前获得且仍然有效的知识在后续修改中不被意外破坏；否则，模型当前看似成功的更新可能导致长期事实可靠性下降。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **工作记忆与外部记忆评测**：长上下文推理、多跳问答主要测试模型在单次推理过程中处理临时信息的能力；多会话或智能体记忆基准则依靠检索机制、记忆组织和交互历史，在模型参数之外保存并调用信息。
- **静态知识编辑评测**：zsRE、UnKE等基准通常对单个事实实施参数编辑，再通过编辑准确率、泛化能力和局部性等指标检查目标知识是否立即生效、能否迁移到相关问法，以及是否影响无关知识。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 工作记忆和外部记忆评测关注单次上下文处理或参数外的信息存取，无法直接揭示知识写入模型参数后，因后续参数更新产生的累积干扰与遗忘。
- 传统知识编辑基准把各次编辑视为相互独立的操作，侧重编辑后的即时表现，忽略连续更新之间的时间交互；因此，一次编辑成功不能证明该知识在未来多轮修改后仍能保留。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一个面向内在参数记忆的统一时序基准：它应在受控的连续编辑过程中反复追踪同一批知识，同时区分孤立事实与结构化关系知识，从而比较不同模型和编辑方法的长期保持、衰减以及稳定性。

</div>
<div markdown="1"><span>核心问题</span>

在语言模型依次接受多轮知识编辑时，早期写入参数的知识能否经受后续修改；其保持与遗忘轨迹如何变化，并且现有编辑方法能否同时维持长期事实记忆和对不同问法的泛化能力？

</div>
<div markdown="1"><span>作者直觉</span>

若把连续编辑看成一条有时间顺序的知识流，并在每个编辑阶段回头测试先前知识，就能把“刚学会”与“长期记住”分开：概念型问答减少关系结构带来的混杂，便于观察单个事实之间的参数干扰；场景型问答再加入相互关联的知识，用来检验模型是否保存了整体关系，而不只是记住孤立答案。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ForgetBench不是一种新的模型训练或知识编辑算法，而是一套评测长期参数记忆的基准流程。它先用两种互补方式构造按时间排列的知识问答流：概念型QA把每条知识隔离为“主体—单一属性”，用于观察局部事实更新；场景型QA从模拟交互形成的异构知识图中抽取子图，再生成需要多跳关系推理的问题，用于观察结构化知识及实例间干扰。随后，待测编辑方法依次把正确答案写入模型，并按固定间隔回测当前与历史问题，形成二值正确性矩阵。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造概念型原子知识流

为每个主体分别采样编辑前属性值 $A^{wrong}$ 与独立的编辑后目标值 $A^{right}$，组成三元组 ($Q,A^{right},A^{wrong})$；不同主体之间不建立依赖关系。

<div class="method-step__io" markdown="1">

**输入**：独立采样的主体、预定义属性值分布和固定属性查询模板。<br>
**输出**：由相互独立的原子事实组成、具有时间顺序的概念型QA序列。

</div>

**直观理解**：它类似于逐个修改互不相关的个人档案，例如把某人的年龄从79改为22。这样可以把遗忘归因于连续编辑本身，而不是复杂关系推理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造场景型结构化知识流

在 K 轮模拟中增删智能体并生成智能体—物品交互，得到异构知识图；从中抽取 N 个具有受控重叠的 L 大小子图，将其规则化改写为自然语言上下文，再由生成模型产生每题一个正确答案和三个干扰项，并随机选取一个干扰项作为 $A^{wrong}$。

<div class="method-step__io" markdown="1">

**输入**：模拟轮数 K、子图规模 L、子图数 N、每个子图的问题数 t，以及初始智能体集合。<br>
**输出**：长度 $T=N\times t$ 的场景型QA序列 $\mathcal{D}$，其中每项为 ($Q_{ij},A_{ij}^{right},A_{ij}^{wrong})$。

</div>

**直观理解**：它先搭建一个包含人物、物品和互动关系的小世界，再询问必须沿多条关系才能回答的问题。子图重叠会使不同知识共享上下文，因此可检验编辑一处时是否影响相关知识。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行顺序知识编辑与周期性回测

按序将各QA目标答案持续写入模型，并在每完成 k 次编辑后，对截至当前已经编辑的所有知识共同测试；同时改变总序列长度 $t_n=nk$，以覆盖不同时间跨度。

<div class="method-step__io" markdown="1">

**输入**：概念型或场景型QA序列、待测语言模型、外部知识编辑方法、最大编辑长度 T 和评测间隔 k。<br>
**输出**：各编辑阶段的模型状态，以及每条知识在多个后续阶段上的预测结果。

</div>

**直观理解**：这不是只在修改后立刻考试，而是每学一批新知识就把旧知识重新考一遍。因而可以看到某条记忆刚写入时是否成功，以及它在后续修改中何时消失或重新出现。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立时空正确性矩阵

将第 t 个评测轮次对第 i 次编辑知识的正确性记为 $\mathcal{Z}[t,i]\in\{0,1\}$，其中 $i\leq tk$；横向按记忆年龄 $\Delta=tk-i$ 聚合，纵向跟踪同一知识跨轮次的状态。

<div class="method-step__io" markdown="1">

**输入**：每个评测轮次对当前及历史问题的回答。<br>
**输出**：具有三角形观测范围的二值矩阵 $\mathcal{Z}$，即后续遗忘量化的统一数据表示。

</div>

**直观理解**：矩阵的一行相当于某次阶段考试，一列相当于同一道旧题在多次考试中的成绩。沿不同方向读取它，分别能观察记忆随年龄衰减和单条记忆是否反复波动。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 即时编辑成功率与历史保留率

$$
\text{ES}=\frac{k}{T}\sum_{t=1}^{T/k}\mathcal{Z}_{t,tk},\quad \text{Ret}=\frac{k}{T}\sum_{t=1}^{T/k}\left(\frac{1}{tk-1}\sum_{i=1}^{tk-1}\mathcal{Z}_{t,i}\right)
$$

**符号说明**

- $\text{ES}$：Edit Success，即每个评测轮次中最新编辑知识的平均正确率。
- $\text{Ret}$：Retention，即各评测轮次中此前所有已编辑知识的平均保留正确率。
- $T$：最大顺序编辑长度。
- $k$：相邻两次评测之间执行的编辑步数。
- $t$：评测轮次索引，共有 T/k 轮。
- $i$：知识编辑项的顺序索引。
- $\mathcal{Z}_{t,i}$：第 t 个评测轮次对第 i 个知识项的二值正确性，正确为1、错误为0。

<div class="equation-explanation" markdown="1">

**直观理解**：ES只取矩阵中每轮最新写入知识对应的位置，回答“刚编辑完是否学会”；Ret则在每轮排除最新项后平均所有旧知识，回答“过去写入的内容还剩多少”。两者必须同时观察，因为一个方法可能容易写入新事实，却会严重覆盖旧事实。<br>
**原文位置**：第4.1节，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 按记忆年龄定义的遗忘曲线

$$
\mathcal{F}(\Delta)=\mathbb{E}\left[\mathcal{Z}[t,i]\mid tk-i=\Delta\right]
$$

**符号说明**

- $\mathcal{F}(\Delta)$：记忆年龄为 $\Delta$ 时的平均知识保留率。
- $\Delta$：记忆年龄，即某知识写入后经历的后续编辑次数。
- $t$：评测轮次索引。
- $k$：每个评测间隔包含的编辑步数。
- $i$：知识项被编辑时的顺序索引。
- $\mathcal{Z}[t,i]$：第 t 轮评测时第 i 个知识项是否回答正确。
- $\mathbb{E}[\cdot]$：对所有满足相同记忆年龄条件的观测取平均。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把写入时间不同、但都经历了相同数量后续编辑的知识放在一起求平均，从而分离“知识有多老”与“它在序列中的绝对位置”。曲线下降表示随编辑累积发生遗忘；论文还由此计算半衰期、AUF和局部Speed，但这些是该核心曲线的派生统计量。<br>
**原文位置**：第4.2节，公式(2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。ForgetBench是评测基准，不提出需要优化的新损失函数；知识写入由被测的外部编辑方法完成，基准只规定QA流、顺序编辑和回测方式。ES、Ret、遗忘曲线、TC、Gen与Flu均为评价量，而非反向传播目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双范式QA生成模块**

概念型QA通过独立主体和单属性替换消除实例间依赖；场景型QA由动态智能体—物品知识图、受控重叠子图、规则化上下文及生成模型产生的多项选择题构成。二者分别控制事实粒度与关系结构。

> 直观理解：两个测试集回答不同问题：前者测试一条孤立事实能记多久，后者测试相互关联的知识能否整体保存。若只使用其中一种，就难以判断遗忘来自编辑冲突还是关系结构。

**2. 顺序编辑与评测矩阵模块**

知识按时间顺序注入，每 k 次编辑执行一次历史知识联合回测，并用 $\mathcal{Z}[t,i]$ 表示第 t 轮对第 i 个知识项的正确性。记忆年龄定义为 $\Delta=tk-i$，使不同写入时刻的知识可以按经历过的后续编辑次数对齐。

> 直观理解：这一步把连续编辑过程变成可分析的时间记录。按记忆年龄对齐后，早写入和晚写入的知识可以在相同“经历了多少次干扰”的条件下公平比较。

**3. 多维遗忘量化模块**

ES与Ret分别衡量写入瞬间和历史知识总体正确率；遗忘曲线及其半衰期、AUF和Speed描述随记忆年龄变化的保留水平；TC按各知识轨迹的0/1状态转换率衡量稳定性。Gen与Flu进一步排除仅记住原始措辞或累积编辑导致语言退化的情况。

> 直观理解：高稳定性不必然表示记得好：模型也可能稳定地一直答错。因此TC必须和Ret、遗忘曲线联合解读，而泛化与流畅性则防止把机械背题或模型损坏误认为成功记忆。

**训练与推理**

评测前先生成概念型和场景型QA序列。运行时，从未编辑或相应起始模型出发，使用待测知识编辑方法按序把每个 $A^{right}$ 作为目标知识注入模型；每完成 k 个编辑步骤，对当前为止的全部问题执行推理，并将回答是否匹配目标答案写入 $\mathcal{Z}$。随后在不同总序列长度上重复该流程，从 $\mathcal{Z}$ 计算即时写入、历史保留、年龄衰减和单实例状态转换指标；再用查询改写版本测试泛化，以生成文本中的有效词法token比例检查流畅性。原文节选未明确给出具体被测编辑算法的优化步骤、答案匹配规则或模型解码配置，因此不能把这些实现归属于ForgetBench本身。

**复现信息**

场景型生成的关键规模关系为 $T=N\times t$：先运行 K 轮交互模拟，再从完整知识图抽取 N 个大小为 L 的子图，每个子图生成 t 道题；每题包含一个正确选项和三个错误候选，并从错误候选中抽取 $A^{wrong}$。评测每隔 k 次编辑进行一次，且考察长度集合 \{$t_n\}_{n=0}^{T/k}$，其中 $t_n=nk$。半衰期计算前对遗忘曲线做轻量平滑，并在线性插值下估计首次跌至 $\mathcal{F}(0)/2$ 的位置；图4仅为可视化采用bin size为10的均值聚合，不应与核心原始正确性矩阵混淆。K、L、N、t、T和k的具体数值在所给章节中原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ForgetBench概念型问答：人物档案从包含2500个不同档案的名称池中随机抽样，用于尽量隔离上下文关系，测试编辑知识本身是否被写入参数并在后续编辑后保留。原文未明确报告该部分单独的问题数量及训练、验证、测试划分。
- ForgetBench场景型问答：由20个Qwen2.5-32B代理进行超过50轮交互，形成含56,095个节点和96,082条边的交互图；从中随机抽取2500个约含20个节点、任意两者最大重叠率为20%的子图，再交给专门代理生成问题。其作用是测试关系结构和语境线索能否帮助长期记忆检索。
- 完整ForgetBench共包含6431个问题实例。实验把连续编辑序列按时间排列，在多个编辑阶段重复测量知识表现；原文未明确报告概念型与场景型实例的具体分配，也未明确给出常规训练集、验证集和测试集划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**ES与Ret**

ES衡量目标知识在编辑后是否成功获得，Ret衡量该知识经过后续连续编辑后仍能被正确召回的程度。两者分别对应“写进去”和“过一段编辑序列后还记得”，不能只凭ES判断长期记忆。 （越高越好；高ES表示即时编辑有效，高Ret表示对后续参数干扰更稳健。）

</div>
<div class="metric-item" markdown="1">

**遗忘动态指标（$Δ_{1/2}$、AUF与Speed）**

$Δ_{1/2}$表示记忆表现衰减到指定半值所经历的编辑跨度；AUF概括整个时间区间内遗忘曲线下的总体保持水平；Speed刻画随连续编辑发生的变化速率。三者用于区分瞬时崩溃、平稳衰减、长期平台和异常回升等动态，而不仅是比较最终时刻。 （$Δ_{1/2}$和AUF越高通常越好；Speed越接近0表示记忆随时间更稳定。负Speed可能对应后期回升，并不自动证明形成了可靠记忆。）

</div>
<div class="metric-item" markdown="1">

**Gen**

衡量编辑知识能否迁移到释义、改写或关联表达，而非只对原始编辑提示作出机械回答。负值表示相对参照出现泛化损害。 （越高越好；接近或高于0通常表示编辑没有明显破坏相关泛化，显著负值说明保持可能依赖死记目标形式。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 概念型问答中的AlphaEdit：DeepSeek-R1 7B与Qwen-2.5 7B

<div class="result-value" markdown="1">

AlphaEdit在保持指标上最强，但出现最严重的保持—泛化冲突：DeepSeek-R1上的Ret为0.979、Gen为-0.930；Qwen-2.5上的Ret为0.885、Gen为-0.559。作者据此认为，零空间投影用刚性正交约束保护历史参数时，也严重限制了可用于融合新知识的更新方向。

</div>

这表示模型能够长期回答训练时的目标事实，却难以处理同一知识的改写问法，因而更接近保存固定答案而不是把知识接入原有语义网络。该相关性支持“强保持可能牺牲泛化”的诊断，但仅凭这些结果不能证明零空间约束是唯一因果来源，也不能推广到未测试的模型、方法或超过500步的序列。

<div class="result-source" markdown="1">

来源：第5.2节，Evaluation on the Concept-based Test；表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

This trade-off is most severe in high-capacity models: on DeepSeek-R1, AlphaEdit’s peak Ret (0.979) directly corresponds to a devastating Gen score of -0.930, and on Qwen-2.5, its strong Ret (0.885) is accompanied by a Gen of -0.559.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 场景型问答相对于概念型问答：AlphaEdit在DeepSeek-R1 7B上的泛化变化

<div class="result-value" markdown="1">

加入结构化场景后，AlphaEdit在DeepSeek-R1上的Gen由概念型测试的-0.930改善到场景型测试的-0.327；作者同时报告各基线的ES和Ret总体上升，并将其解释为关系结构提供了语义支架。

</div>

上下文中的人物、事件和关系可成为检索线索，使原本难以直接召回的知识重新可见，因此场景测试缓解了表面上的保持—泛化矛盾。但Gen仍为负值，而且可观察召回改善不等于知识已稳定固化在参数中；结果也可能部分反映模型利用当前语境推断答案。

<div class="result-source" markdown="1">

来源：第5.2节，Evaluation on the Scenario-based Test；表1与表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The relational density narrows the performance gap between AlphaEdit and UltraEdit, while also alleviating AlphaEdit’s catastrophic generalization drop (e.g., its Gen score on DeepSeek-R1 improves from -0.930 to -0.327).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 场景型问答中的WISE：Llama-3.1 8B

<div class="result-value" markdown="1">

WISE在该设置下达到Flu 0.999且Gen约为0，但作者认为其实际长期保持仍有限；表2中相应Ret为0.258。它体现了输出自然、泛化损害较小与参数记忆牢固并非同一性质。

</div>

路由机制可以让回答保持通顺并避免明显破坏原能力，却不保证新知识被稳定写入基础模型参数。因此，不能把流畅回答或接近零的Gen单独视为长期记忆成功。该结果只说明WISE在此模型和协议下偏向保守，不表示其在所有编辑规模或任务上都无法保持知识。

<div class="result-source" markdown="1">

来源：第5.2节，Evaluation on the Scenario-based Test；表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Conversely, WISE achieves near-perfect fluency (Flu: 0.999) and generalization (Gen ≈ 0) but limited actual retention, proving that fluent generation does not equate to genuine memory preservation.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文节选未提供随机种子、重复实验次数、置信区间或显著性检验，因而无法判断方法间较小差异是否稳定；场景数据由同一种Qwen2.5-32B代理生成互动和问题，也可能带来生成模型特有的语言与关系模式偏差。
- 所有实验把序列长度限制为500，且只覆盖四个约7B至8B级模型和四种参数编辑方法；场景中的高召回还可能混合参数保存与上下文推断。因此，结果不能直接证明超过500次更新、更大模型、其他编辑机制或真实世界持续学习环境中的长期记忆性质。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- MEMIT：代表直接修改模型参数以批量写入事实的编辑方法，可检验缺少显式干扰控制时，连续参数更新是否会覆盖旧知识。
- WISE：通过路由等机制管理编辑知识，属于较保守的比较对象；它可检验维持输出流畅性和近似不损害泛化，是否等同于知识真正进入并长期保存在基础参数中。
- AlphaEdit：采用零空间投影与正交约束来减少新编辑对历史参数的干扰，是保持导向的代表方法；它用于检验强保护旧知识是否会压缩有效更新方向并损害改写泛化。
- UltraEdit：代表具有较强单步编辑能力的优化方法，用来检验单次写入成功能否自然扩展为数百次更新后的长期稳定记忆。

**实验想回答的问题**

- 在最多500次连续知识编辑中，不同语言模型与编辑方法能否同时实现新知识写入、长期保持和对改写问题的泛化，还是会出现保持—泛化权衡？
- 孤立事实问答与包含实体关系和上下文线索的场景问答，是否会呈现不同的遗忘曲线与可观察召回能力？

**实验实现**

实验覆盖Llama-3 8B、Llama-3.1 8B、Qwen-2.5 7B和DeepSeek-R1 7B，并在每个模型上比较四种编辑方法。实现和超参数采用EasyEdit2提供的默认配置。由于预实验显示两类问答中多数模型与方法在序列长度超过500后ES和Ret均明显下降，正式实验统一令最大连续编辑长度T=500，并每隔k=10个编辑阶段评估一次，以兼顾时间分辨率与计算成本。全部实验运行于4张各24 GB显存的NVIDIA GeForce RTX 4090。该协议比较的是反复修改后的记忆轨迹，不是单次编辑准确率。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 遗忘曲线的定性对照显示，概念型测试中MEMIT可迅速降到零，而AlphaEdit可能维持近乎平坦的轨迹；场景型曲线更平滑但伴随不规则波动和负Speed。该现象说明相同终点Ret可能来自不同过程：稳定保存、早期崩溃、上下文辅助恢复或后续关联编辑强化，因此必须结合整条时间曲线解释长期记忆。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces a benchmark and evaluation framework for measuring long-term forgetting under sequential LLM knowledge edits.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`df2f3295648ffe6c8fbc95d5a18ae4ecec61eaec3a86f033953765880b7e863a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
