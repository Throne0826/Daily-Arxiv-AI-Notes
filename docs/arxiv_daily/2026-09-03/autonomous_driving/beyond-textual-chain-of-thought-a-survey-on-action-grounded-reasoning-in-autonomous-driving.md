---
title: "[论文解读] Beyond Textual Chain-of-Thought: A Survey on Action-Grounded Reasoning in Autonomous Driving"
description: "[arXiv 2609.01659][自动驾驶] 本文综述将自动驾驶中的思维链从文字推理重新界定为“动作落地的推理表示”，并以观测与驾驶输出之间的中间表示形式为主轴，统一梳理语言、视觉空间、潜在动态和外部化推理。"
arxiv_id: "2609.01659"
announcement_date: "2026-09-03"
primary_category: "autonomous_driving"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-03T04:33:01.757972+00:00"
source_sha256: "f1c9494008fdabc2a76237a1d17e040e6c8b6d766acec39a548fc37ae56f658c"
tags:
  - "自动驾驶"
  - "VLM Reasoning"
  - "LLM Reasoning"
  - "动作扎根推理"
  - "思维链"
  - "视觉语言动作模型"
  - "中间表示"
  - "闭环可靠性"
  - "安全验证"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">自动驾驶 · arXiv 2609.01659</p>

# Beyond Textual Chain-of-Thought: A Survey on Action-Grounded Reasoning in Autonomous Driving

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-03</span>
<span><strong>作者</strong> Zhengxu Tang, Xiaozhou Zhang, Guofeng Cui, Ziyu Gong, Zi Wang, Yunfei Shi, Ruifeng Deng, Chengzhi Qi, Ke Chen, Sachin Patil, Tianjun Xiao, Langechuan Liu, Pichao Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> NVIDIA</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.01659v1) · [PDF 下载](https://arxiv.org/pdf/2609.01659v1) · **关键词** 自动驾驶, 动作扎根推理, 思维链, 视觉语言动作模型, 中间表示, 闭环可靠性, 安全验证<br>
**项目页**: [https://github.com/tangzhengxu/awesome-av-cot](https://github.com/tangzhengxu/awesome-av-cot)

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

本文综述将自动驾驶中的思维链从文字推理重新界定为“动作落地的推理表示”，并以观测与驾驶输出之间的中间表示形式为主轴，统一梳理语言、视觉空间、潜在动态和外部化推理。

**不用术语来说**：自动驾驶模型不能只把场景“说得有道理”，还必须及时生成安全、连续且符合真实道路几何与运动规律的动作；因此，关键问题不在于生成更长的文字解释，而在于模型采取行动前应使用什么样的中间信息，以及如何判断这些信息确实影响并改善了驾驶决策。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出以中间表示为中心的统一框架：把“观测与驾驶相关输出之间可识别、可用于决策的结构”作为比较单位，将130篇方法论文归入语言、视觉空间、潜在动态和外部化四类表示及13个子类型，从而能够在同一框架下比较文本链、想象的未来状态、潜在空间推演、检索轨迹、工具调用和多智能体消息。
- 综合已有基准证据并明确研究前沿：归纳不同表示在可解释性、现实落地、动作耦合、延迟与闭环可靠性上的取舍，将忠实的动作耦合、感知落地、自适应推理成本、闭环可靠性和安全验证识别为核心挑战；同时明确本文只做语料层面的综合，不声称任何表示类别具有因果上的优越性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于自动驾驶与多模态推理交叉领域。自动驾驶系统需要从摄像头等传感器获得的场景观察出发，理解道路结构、交通参与者及其交互，并生成车辆未来的连续动作或轨迹。随着大语言模型（LLM）、视觉语言模型（VLM）和视觉—语言—动作模型（VLA）被用于场景理解、决策解释和动作生成，研究重点从单纯的端到端映射逐渐转向在观察与动作之间加入可分析的推理层。本文将这一推理层中的中间结构称为动作扎根推理表示：它们不仅描述或压缩信息，还应当与驾驶几何、运动、交通规则及最终动作发生实际联系。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**思维链（Chain-of-Thought，CoT）**

CoT 是模型在给出最终答案前显式生成的逐步中间推理过程。在语言任务中，中间过程通常是文字；在自动驾驶中，中间过程还可能是未来视觉状态、占用结构、潜变量、工具输出或多智能体消息。

</div>
<div class="concept-item" markdown="1">

**动作扎根推理表示**

它指位于场景观察与驾驶决策之间、能够组织驾驶相关信息的可识别中间结构。这里的“扎根”意味着该结构应与真实世界中的位置、几何关系、运动、交通规则或可执行轨迹相联系，而不是仅作为无法解释的通用特征。

</div>
<div class="concept-item" markdown="1">

**闭环驾驶与连续动作**

连续动作是随时间变化的控制输出，例如车辆未来的轨迹或驾驶控制量，而不是一次性的文字答案。闭环系统会把当前动作对环境造成的后果重新作为后续观察，因此推理延迟、错误累积和不稳定中间过程都会直接影响后续决策与安全性。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文不是提出一个新的驾驶模型，而是界定并整理一类研究问题：给定自动驾驶车辆对当前环境的多模态观察，模型应先形成某种决策相关的中间推理表示，再输出未来驾驶动作或轨迹。该表示可以是语言、视觉—空间结构、潜在动力学状态，或由检索、工具、规则和多智能体交互产生的外部化信息。纳入范围要求中间结构在观察与动作之间承担明确的推理作用：它可以被生成或监督，也可以作为决策相关状态被检查、干预、检索、压缩、提炼、修订或通信；普通感知、预测或规划模块若没有可识别的推理中间过程，则不纳入。问题的关键约束是中间表示必须同时考虑世界扎根、动作耦合、实时运行、闭环可靠性和安全验证，而不能只追求文字解释的完整性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{O}$**

车辆在当前时刻获得的多模态环境观察，例如视觉输入及其中包含的道路、车辆和交通参与者信息。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{R}$**

观察与最终驾驶决策之间的动作扎根推理表示；它是本文比较不同方法时的核心中间对象。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{A}$**

驾驶系统输出的动作或未来轨迹；与语言问答中的离散答案不同，它具有连续的时空结构。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{CoT}$**

思维链（Chain-of-Thought）的缩写，表示模型在最终输出前产生的中间推理步骤。本文研究其从文本形式扩展到语言、视觉—空间、潜在动力学和外部化表示的过程。

</div>

</div>

**直接相关的工作**

- **Cui et al. (2025), Chain-of-Thought for Autonomous Driving**: 该工作直接聚焦自动驾驶中的 CoT 方法，主要按照 CoT 范式、方法和任务组织文献。本文与其研究范围最接近，但进一步把比较单位统一为观察与驾驶输出之间的中间表示形式，而不局限于文本 CoT 方法。
- **Cui et al. (2026), LLM4AD**: 该综述从 LLM 在自动驾驶中的角色、任务、基准和流水线集成等角度组织研究，将推理视为多种能力之一。本文则只考察决策相关的中间推理结构，并比较其如何连接观察、动作和安全验证。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

自动驾驶基础模型需要在复杂、持续变化的道路环境中，把场景理解转化为连续轨迹。这个过程既要依赖几何位置、物体运动和交通规则，又受实时延迟与闭环反馈约束；一旦中间推理冗长、不稳定或与实际动作脱节，误差便可能随车辆连续执行而累积。因此，系统需要一种既能连接感知与轨迹生成，又便于监督、检查和安全审计的推理层。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **文本思维链与语言式驾驶推理**：模型先用逐步文字描述场景、识别关键交通参与者、推断交互并形成驾驶计划，再据此生成最终决策。其优势是过程容易阅读和检查，也可通过分阶段计划、反思修正或压缩文本轨迹来组织推理。
- **既有自动驾驶基础模型与推理综述框架**：既有综述通常按大语言模型的角色与任务、思维链方法范式、视觉—语言—动作架构、端到端系统演化，或认知能力与系统挑战组织文献；这些视角能够说明模型或流水线如何构成，但一般不把观测与动作之间出现的中间产物作为跨方法统一比较的基本单位。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 普通文本思维链与连续驾驶动作具有不同的表示和相似性结构，文字上合理的推理未必对应正确轨迹；它还可能缺少对道路几何、运动状态和交通规则的直接落地。在实时闭环中，冗长或不稳定的文本轨迹会增加延迟，并可能放大而非减少执行误差。
- 按模型、任务、流水线或能力组织的既有综述难以统一比较文本链、未来视觉状态、占用结构、潜在动态推演、检索记录、工具输出和智能体消息，也较难系统追问这些中间表示是否真正连接下游动作，以及需要什么证据验证其动作忠实性与安全可靠性。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有文献缺少一个以“决策相关的中间产物”为共同分析单位的系统框架，因而尚不能清晰刻画不同推理表示如何在可解释性、物理世界落地、动作耦合、计算延迟和闭环可靠性之间取舍。尤其缺少对纳入边界和证据标准的统一规定：哪些中间状态属于显式推理，而非普通感知、预测或规划特征；又应如何证明它们可被检查、干预、压缩、检索、修正或通信，并确实参与决策。

</div>
<div markdown="1"><span>核心问题</span>

在自动驾驶中，模型应以何种可识别的中间形式组织行动前的推理，使其能够同时连接真实场景与连续驾驶输出，并接受统一分类和证据评估？

</div>
<div markdown="1"><span>作者直觉</span>

与其按模型名称或任务阶段分类，不如直接观察“感知输入和驾驶输出之间留下了什么”。中间产物的形式往往决定了系统最容易获得的性质：语言便于人工检查，视觉空间结构更贴近道路几何，潜在动态表示更容易与预测和控制相连，检索、工具及多智能体消息则可引入外部知识与协作。以这些产物为主轴，可以把架构差异很大的方法放到同一组决策标准下比较，同时也揭示没有单一表示能够兼顾所有需求，未来更可能需要可落地、与行为存在因果联系、计算高效且能在闭环中受监控的混合表示。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是提出一个可训练的自动驾驶模型，而是提出一套“以中间表示为中心”的综述分析方法。其分析对象是观察到动作之间的决策相关中间产物：只要某种表示实际连接感知与轨迹、控制指令、机动决策或规划器干预，就被视为驾驶推理载体，而不要求它必须是自然语言。作者据此将所收集的工作划分为语言型、视觉—空间型、潜在—动态型和外部化型四大家族，并进一步细分为13个子类型，用来比较不同设计在可解释性、物理世界落地、动作耦合、实时效率、外部知识访问与多智能体协作方面的取舍。

分类的关键不在中间信息“看起来像什么”或“从哪里产生”，而在推理到输出的接口处，下游模块以什么形式消费该信息。例如，坐标若仍作为文本词元参与语言推理，则归为语言型；若被解析为边界框、对象状态、占据元素或航点并直接用于预测或规划，则归为视觉—空间型。工具来源仅作为附加属性记录，不自动决定主类别。直观地说，本文不是按模型名称或骨干网络整理文献，而是追问：车辆在采取动作之前，真正拿什么作为自己的‘思考草稿’？

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 界定动作落地的驾驶推理

判断方法是否形成了连接观察与动作的决策相关中间结构，而不是仅生成语言上连贯的解释。评价重点从文本链的可读性转向该中间结构是否承载几何、运动、交互意图、交通规则等会影响驾驶安全的变量。

<div class="method-step__io" markdown="1">

**输入**：自动驾驶方法中的场景观测、中间计算过程，以及最终的轨迹、控制命令、机动决策或规划器干预。<br>
**输出**：一个扩展后的驾驶推理定义，可同时容纳文本推理、空间证据、未来状态、潜在动态、检索记忆和工具返回结果。

</div>

**直观理解**：普通问答中的思考最终产生一句答案，而驾驶中的思考必须促成车辆下一步怎么走。即使内部表示无法被人直接阅读，只要它确实改善轨迹选择或控制，就属于本文研究的推理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 识别决策相关的中间产物

定位在“推理到输出”接口处被下游预测器、规划器或动作头实际消费的中间产物，并区分其表示形式、功能和来源。仅用于展示、事后解释或与动作生成相互独立的文本，不足以证明动作落地。

<div class="method-step__io" markdown="1">

**输入**：每篇方法论文所描述的模型结构、推理过程，以及中间模块与最终动作输出之间的连接方式。<br>
**输出**：每种方法的核心中间产物描述，例如场景说明、未来占据状态、潜在展开、优化中的轨迹状态、检索经验、规则约束、工具结果或协作消息。

</div>

**直观理解**：这一步相当于沿着模型的数据流寻找真正进入决策环节的信息，而不是只看论文展示了什么解释。若一段说明没有改变规划器，它更像旁白；若一个潜在状态直接决定轨迹，它才是决策过程的一部分。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按消费形式分配主类别与子类型

首先将方法归入语言型、视觉—空间型、潜在—动态型或外部化型，再依据具体机制分配到13个子类型之一。主标签由中间产物的消费形式决定；工具来源、知识来源或混合属性可作为次级标签记录，以处理跨类别方法。

<div class="method-step__io" markdown="1">

**输入**：已识别的决策相关中间产物及其被下游模块消费的形式。<br>
**输出**：四级家族和13个子类型构成的表示中心分类体系，以及每篇方法的主要归属。

</div>

**直观理解**：同一份坐标可以写成一句话，也可以变成规划器使用的边界框；内容相同不代表推理形式相同。作者因此看下游怎样使用它，而不是依据文件格式、表面措辞或生成它的工具来分类。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在相容协议内综合证据与权衡

作者为每个子类型选择一个中间产物清晰且具有文档化研究内比较的代表方法，并保留原论文的模型配置、数据划分、预测时域、输入和指标定义。不同实验协议下的分数不进行跨行排名，综合重点是表示设计分别测试了何种能力及其典型失效模式。

<div class="method-step__io" markdown="1">

**输入**：各论文报告的骨干模型、任务、数据集或基准、指标、代表性中间产物，以及同一研究中的对照结果。<br>
**输出**：按子类型组织的代表性比较表与完整论文清单，以及关于可解释性、落地性、动作耦合、效率、可靠性和可验证性的结构化结论。

</div>

**直观理解**：不同驾驶论文即使都报告一个“分数”，测试环境也可能完全不同，因此不能把数字直接排成排行榜。本文把研究内对照当作较可靠证据，用它说明某种中间表示在自己的实验条件下解决了什么问题。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文是综述与分类体系论文，没有提出统一的模型损失函数、参数优化目标或训练算法；不同被综述方法各自使用轨迹监督、未来场景重建、动作预测、语言监督、强化微调或扩散式轨迹优化等目标，但节选没有给出可作为本文统一目标的公式，因此不应人为合并或补造方程。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 语言型表示**

该家族把场景描述、对象分析、风险解释、分阶段计划、自我批评或压缩文本轨迹作为中间产物，分为描述型、程序型、反思型和压缩型。描述型强调可检查的语义与理由；程序型按感知、预测、规划和控制等阶段组织信息；反思型增加批评、修订或回滚；压缩型通过蒸馏、内化或按需激活减少推理时延。

> 直观理解：语言便于人类查看、监督并与交通规则对齐，但它只能间接表达距离、遮挡和运动。其主要风险是模型可能把正确动作事后包装成合理解释，或者描述正确却仍输出错误轨迹；固定流程和多轮反思还可能不适应场景复杂度或违反实时要求。

**2. 视觉—空间型与潜在—动态型表示**

视觉—空间型将未来图像、占据结构、对象裁剪、掩码、边界框、深度特征或轨迹草图作为推理载体，包括预测型与动作落地型。潜在—动态型则以潜在世界模型展开、显式监督的离散或连续动态词元、扩散或其他迭代优化状态承载推理，包括展开型、词元化型和优化型；它们通常比像素生成更紧凑，也更便于规划器直接使用。

> 直观理解：视觉—空间表示像是在行动前标出危险对象或预演未来场景，能保留文本容易丢失的几何关系，但选错关键区域或生成一个看似真实却对规划无用的未来都会造成误导。潜在表示更像机器内部的压缩沙盘，运行可能更快、动作联系更强，却难以让人确认其中究竟编码了风险、意图还是数据捷径。

**3. 外部化表示**

该家族把部分推理移出模型参数，分为检索增强、知识落地、工具介导和协作四类。相应中间产物分别是被检索的案例或经验、规则与地图或场景图等结构化先验、规划器或模拟器等工具的调用与返回值，以及车辆、智能体或基础设施之间交换的消息。

> 直观理解：外部系统可以补充罕见规则、历史经验、专用计算能力和其他车辆看见的信息，因此适合长尾场景和模块化部署。但它也引入新的安全边界：检索内容可能过时，工具可能调用失败，通信可能延迟或遭到伪造，系统必须验证来源并在外部信息缺失时安全退化。

**训练与推理**

本文自身没有模型训练和在线推理流程，其“运行过程”是文献编码与证据综合：先把驾驶推理定义为观察和动作之间的决策相关结构，再从各方法中定位该结构，随后依据其在推理到输出接口处的消费形式分配主类别和子类型，最后在保留原研究实验条件的前提下整理研究内证据。对于混合系统，主类别由真正进入下游预测或规划环节的表示决定，检索、工具或知识来源可另作次级属性。

从被综述系统的共同视角看，训练阶段可能利用显式文本推理、未来状态、重建任务或结构化知识来监督中间表示；推理阶段则必须在闭环与实时约束下把该表示转化为轨迹或控制。论文特别强调，冗长推理并非默认更好：显式文本可仅作为训练脚手架并在部署时被蒸馏或内化，昂贵的反思或工具调用也可只在高风险、不确定场景触发。不过这些是跨论文归纳出的设计模式，而不是本文实现并验证的一套统一训练方案。

**复现信息**

语料规模为171篇论文，其中130篇是方法论文，另有41篇基准、数据集、综述与分析论文；节选未给出检索数据库、查询式、纳入与排除标准、去重流程、标注人员数量、标注一致性或争议仲裁程序，因此无法仅凭所给章节完整复现语料收集和分类标注。分类体系包含四个主类别和13个子类型：语言型4类、视觉—空间型2类、潜在—动态型3类、外部化型4类。

表2每个子类型只展示一个代表方法，选择依据是中间产物定义清晰并存在可记录的研究内比较，而非该方法取得最高分。表中结果保留来源论文各自的模型配置、数据划分、预测时域、输入和指标定义；由于这些协议并不统一，不应把不同数据集或不同设置下的分数作横向排名。附录B被说明为完整论文级清单并包含骨干模型、基准和子类型，但当前节选没有提供该附录内容；因此这里能够复现的是分类判据和代表性组织原则，而不是完整的文献编码表。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 问答与显式推理数据集：用于测试模型是否能够描述驾驶场景、回答问题并生成结构化推理轨迹；原文未明确报告统一的数据集规模、训练验证测试划分或单一主数据集。
- 空间定位与鲁棒性基准：用于测试目标定位、空间关系理解以及在扰动下维持稳定性的能力；原文未明确报告统一的数据集规模和划分。
- 规划与闭环驾驶基准：规划基准测试运动决策、避碰、路线和行驶进度，闭环基准进一步测试动作会改变后续观测时推理是否仍然可靠；原文未明确报告统一的数据集规模、划分和具体实验协议。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Exact-match 或 multiple-choice accuracy**

衡量最终答案是否与标准答案完全一致或选项是否正确，主要反映显式问答的结果正确性。 （越高越好；但高分不能证明答案具有视觉 grounding、推理过程忠实，或确实影响了规划动作。）

</div>
<div class="metric-item" markdown="1">

**Trajectory displacement metrics**

比较模型预测轨迹与日志中未来轨迹之间的位移差异，反映预测轨迹与示范轨迹的接近程度。 （通常越低越好；但更接近日志轨迹不必然意味着更安全，因为其他合理且安全的驾驶行为也可能因此受到惩罚。）

</div>
<div class="metric-item" markdown="1">

**Open-loop collision estimates 与 closed-loop/composite scores**

开环碰撞估计在固定的车身占用范围、预测时域、目标外推方式和碰撞协议下估计风险；闭环或综合分数则在交互环境中汇总更广泛的驾驶表现。 （碰撞估计通常越低越好，闭环或综合分数通常越高越好；但开环估计不建模其他交通参与者如何响应自车，闭环分数也受模拟器、场景和聚合规则影响。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 不同类型驾驶推理基准的覆盖范围

<div class="result-value" markdown="1">

评测体系呈碎片化：问答基准主要检验描述和回答，空间基准检验定位与关系，规划基准检验动作决策，闭环基准检验动作影响未来观测后的可靠性；它们尚未共同覆盖从中间推理到动作后果的完整链路。

</div>

这说明一个模型可能会正确描述场景，却未必能据此产生安全动作；也可能规划表现不错，却没有可检查的推理证据。因此，单项基准的高分不能代表完整的行动化推理能力。

<div class="result-source" markdown="1">

来源：第5节“Evaluation Landscape”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Despite this progress, evaluation remains fragmented: QA benchmarks rarely test action consequences, planning benchmarks rarely inspect intermediate reasoning, and closed-loop benchmarks rarely evaluate reasoning faithfulness or evidence reliability (details in Appendix C).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 问答正确率与规划、动作可靠性的关系

<div class="result-value" markdown="1">

Exact-match 或 multiple-choice accuracy 能衡量最终答案正确性，但不能证明答案具有视觉 grounding，也不能证明答案被规划器使用；轨迹位移指标能衡量预测轨迹与日志未来的差异，但可能惩罚其他安全驾驶行为。

</div>

这些指标分别回答“答对了吗”和“像不像记录轨迹”，却没有直接回答“证据是否来自当前场景”以及“推理是否促成了安全动作”。因此，改善某个指标不等于整体推理质量改善。

<div class="result-source" markdown="1">

来源：第5节“Evaluation Landscape”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Exact-match or multiple-choice accuracy measures final-answer correctness, but does not show whether the answer is visually grounded or used by the planner.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 开环与闭环驾驶评测的可比性和局限

<div class="result-value" markdown="1">

开环碰撞估计依赖车身占用范围、预测时域、目标外推和碰撞协议，且不建模其他交通参与者对自车的响应；闭环和综合分数覆盖更多驾驶因素，但依赖具体模拟器、基准版本、场景集合和聚合规则，因此应作为来源特定的证据，而非可直接比较的推理质量分数。

</div>

同一个模型在不同模拟器或碰撞协议下可能得到不同结论。开环结果更容易测量但忽略交互，闭环结果更接近真实驾驶但环境依赖更强；两者都不能单独证明中间推理是忠实且安全的。

<div class="result-source" markdown="1">

来源：第5节“Evaluation Landscape”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We therefore report these metrics as source-specific evidence rather than treating them as directly comparable measures of reasoning quality.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文提供的是评测景观与方法论综合，而非统一控制变量下的模型实验；因此没有报告可用于直接比较的统一数据集规模、数据划分、基线分数、统计显著性或消融结果。
- 本文明确指出现有评测仍然碎片化，且开环碰撞估计、轨迹位移、闭环分数分别受协议、交互建模和模拟环境影响；因此文中结论不能被解释为某一类推理方法在真实部署安全性上必然优于其他类别。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- QA或显式推理评测：以最终答案正确性为主要比较对象，适合衡量可表达的场景理解，但不能说明答案是否真正被规划器使用。
- 空间定位与鲁棒性评测：比较目标定位、关系理解和扰动稳定性，适合检验中间视觉空间表示的 grounding 能力。
- 开环规划评测：比较预测轨迹与记录的未来轨迹，并估计碰撞风险，适合衡量运动决策，但可能惩罚其他同样安全的行为。
- 闭环或综合驾驶评测：在动作影响未来观测的环境中比较驾驶表现，覆盖面更广，但结果依赖具体模拟器、基准版本、场景集合和分数聚合规则。原文未明确报告一个统一的模型基线表。

**实验想回答的问题**

- 现有自动驾驶推理基准分别评估场景问答、空间定位、规划和闭环行为时，是否覆盖了从中间推理表示到最终动作的完整链路？
- 不同评价指标分别测量哪些能力，以及为什么不能把问答正确率、轨迹误差、碰撞估计和闭环综合分数直接视为可互换的推理质量指标？

**实验实现**

本文是综述而非提出单一模型的对照实验，因此实验设置主要是对既有评测体系进行分类和方法论分析。作者将评测划分为问答与显式推理、空间 grounding 与鲁棒性、规划以及闭环评测，并强调这些基准分别覆盖推理系统的不同片段。原文未明确报告统一的训练流程、硬件、随机种子、模型超参数、数据规模汇总或可复现实验脚本。本文的核心评估结论是：应联合报告 grounding、动作忠实性、推理成本和闭环安全，而不是只依赖单一问答或轨迹指标。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 综述给出的代表性设计分析是“解释性—动作耦合”的权衡：文本链条便于人检查，但可能与最终轨迹联系松散；潜在 rollout 和优化状态能直接影响规划，却难以检查；视觉裁剪、掩码、检索案例和工具输出处于中间位置，但仍需验证最终动作确实依赖这些中间产物。作者据此提出未来系统可能需要双重表示，即用于控制的紧凑内部表示加上用于监控和解释的忠实外部轨迹。该内容是跨类别综合分析，不是单个数据集上的定量案例实验。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：综述自动驾驶中从文本思维链转向视觉空间、潜在动态及动作落地中间表示的推理方法。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`f1c9494008fdabc2a76237a1d17e040e6c8b6d766acec39a548fc37ae56f658c`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
