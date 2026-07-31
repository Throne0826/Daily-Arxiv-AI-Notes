---
title: "[论文解读] HANDBOOK.md: A Benchmark for Long-Context Agentic Instruction Following"
description: "[arXiv 2607.25398][LLM 评测] HANDBOOK.md构建了一个面向企业代理的基准，用于检验语言模型代理能否在长周期、多工具操作中持续遵守冗长且具有约束力的规章，而不只是完成用户表面的任务请求。"
arxiv_id: "2607.25398"
announcement_date: "2026-07-29"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.342030+00:00"
source_sha256: "4238394d666a78e0e49b8283a001473c2fb6461c062eaa8deb6b20c73f0ebe70"
tags:
  - "LLM 评测"
  - "LLM Agent"
  - "语言模型智能体"
  - "常设指令"
  - "长上下文"
  - "政策遵循"
  - "工具调用"
  - "标准操作程序"
  - "程序化评测"
  - "长程一致性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2607.25398</p>

# HANDBOOK.md: A Benchmark for Long-Context Agentic Instruction Following

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-29</span>
<span><strong>作者</strong> Liudas Panavas, Sebastian Minus, Bradley Monton, Derek Ray, Suhaas Garre, Sushant Mehta, Edwin Chen</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.25398v1) · [PDF 下载](https://arxiv.org/pdf/2607.25398v1) · **关键词** 语言模型智能体, 常设指令, 长上下文, 政策遵循, 工具调用, 标准操作程序, 程序化评测, 长程一致性<br>
**代码**: [https://github.com/surge-ai/handbook](https://github.com/surge-ai/handbook)  

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

HANDBOOK.md构建了一个面向企业代理的基准，用于检验语言模型代理能否在长周期、多工具操作中持续遵守冗长且具有约束力的规章，而不只是完成用户表面的任务请求。

**不用术语来说**：企业中的任务请求并不总能直接执行：例如，邮件可能要求立即解雇员工，但公司手册可能规定必须先取得特定人员批准。语言模型代理同样会同时面对即时请求和长期有效的政策文件；真正的问题是，它能否在查阅文件、调用多个工具并执行许多步骤之后，仍准确记住并服从政策，包括在必要时拒绝或停止操作。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出HANDBOOK.md基准，以65个相互独立的企业任务直接测量长篇常设指令对代理行为的持续约束力；任务覆盖五个业务领域，并使用20至124页、按任务修改关键规则与阈值的专家编写操作手册，降低依靠记忆固定政策或模式匹配完成任务的可能性。
- 建立确定性且双向的评测机制：共824项程序化标准既检查政策要求的动作是否完成，也检查被禁止的动作和非预期副作用是否发生，从而把“完成工作”与“合规完成工作”区分开来。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于语言模型智能体、长上下文理解与指令遵循的交叉领域。现实中的智能体不仅要根据即时请求完成任务，还常被系统提示、政策文件或技能文档等“常设指令”持续约束；因此，关键能力不是单纯读懂长文或达成目标，而是在多步推理和多次工具调用中始终识别适用条款，并在请求与政策冲突时服从政策。既有智能体基准多考查交互环境中的目标完成率，长上下文基准则多考查检索和阅读，较少直接测量长篇约束文档能否持续、可靠地支配智能体的实际行动。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**常设指令（standing instructions）**

在单次工作请求之外预先给定、并对后续所有行动持续有效的规则，例如系统提示、公司手册或标准操作程序。即时邮件即使要求执行某项操作，智能体仍须先判断该操作是否被常设指令允许。

</div>
<div class="concept-item" markdown="1">

**智能体式任务（agentic task）**

模型不是一次性生成答案，而是在有状态环境中反复推理、读取文件并调用邮件、日历、工单或商务服务等工具。先前操作会改变环境状态，因此漏做、误做和额外副作用都可能影响最终判定。

</div>
<div class="concept-item" markdown="1">

**模型上下文协议（Model Context Protocol, MCP）**

一种向模型智能体统一暴露外部工具与服务的接口协议。本文通过 MCP 提供模拟邮件、聊天、日历、问题追踪和商务服务，使评测对象能够像企业员工一样操作多个系统。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

HANDBOOK.md 将智能体置于一个自包含、可重置的虚构公司环境中。输入包括一项日常工作请求、一份20至124页（约8K至79K token）的任务专属标准操作程序，以及由电子表格、PDF、Office 文档和多个 MCP 服务组成的有状态工作空间；65项任务覆盖财务、医疗账单、保险、物流和人力资源五个领域、十家虚构公司。智能体需要在平均约17个推理步骤和30次工具调用的执行过程中定位并保留相关规则，完成政策要求的操作，同时拒绝或停止政策禁止的操作。输出不是单一文本答案，而是执行后的完整环境状态及工具操作轨迹，例如修改后的表格、创建的工单、发出的邮件，以及应当被正确扣留而未发送的操作。每项任务均由基础手册变体生成，关键权限主体、阈值和流程细节不同，以降低记忆固定政策带来的捷径；评测使用程序化标准同时检查必需行为和禁止行为，不使用大模型裁判。严格判定要求该次试验满足全部标准，因而衡量的是长政策对端到端行动的实际约束力，而非一般任务完成质量。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\tau\text{-bench}$**

一个显式评测工具型智能体政策遵循能力的既有基准；其领域政策较短，且同一领域内各任务共享政策。

</div>
<div class="notation-item" markdown="1">

**$\tau^{2}\text{-bench}$**

对 τ-bench 设置的扩展，引入双控制电信领域，但并未把重点转向更长且逐任务变化的政策文档。

</div>

</div>

**直接相关的工作**

- **τ-bench**: 它同样把政策遵循作为明确评测目标，并根据最终数据库状态评分；但政策只有数页且在领域内跨任务共享，模型可能通过重复接触吸收规则。HANDBOOK.md 将政策扩展到20至124页，并让每项任务拥有独特变体，从而更直接检验现场阅读和长程执行。
- **SOP-Bench**: 它也评测智能体执行工业标准操作程序，并使用合成工具 API；区别在于其程序本身就是任务规格，而 HANDBOOK.md 将独立工作请求与上层治理手册分开，因此能够检验智能体是否会因政策要求而拒绝、暂停或限制看似合理的请求。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

企业正把系统提示、政策文件或技能文档作为长期有效的“常设指令”交给语言模型代理，并让代理在邮件、聊天、日历、工单和商务系统之间自主操作。此类部署默认代理会让政策持续支配后续行为，但现实任务往往包含与政策冲突的合理即时请求；一旦代理遗漏审批条件、忽略检查结果或执行被禁止的动作，即使大部分流程正确，也可能造成严重的合规与业务风险。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **目标完成型语言代理基准**：向代理提供一个明确目标，例如解决工单、浏览网站或完成工作流，再依据任务是否完成来评分；评测重点通常是代理能否规划并调用工具达到目标。
- **短政策、跨任务共享的政策遵循评测**：给代理提供较短且在多个任务中重复使用的规则，并检查其行为是否符合这些规则；这种设置可以测量基本规则遵循能力，但代理也可能通过反复接触记住政策模式，而非真正读取当前文档。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 目标完成型基准主要奖励是否达到用户请求的结果，较少检查代理是否因上位政策而拒绝某个动作，也往往不系统检测禁止行为；因此，一个完成了表面任务却违反公司规定的代理仍可能获得较高评价。
- 已有政策遵循设置中的规则通常较短并在任务间共享，难以反映20至124页政策文件、约17个推理步骤和30次工具调用所带来的检索、记忆与持续执行压力，也无法排除模型凭熟悉模式作答。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有评测缺少一种接近真实企业部署、同时具备任务级唯一长政策、原生多工具环境以及确定性双向验收标准的测量工具，因而无法可靠判断代理是否真正读取眼前的规则，并在长操作链中让这些规则持续约束每一个动作。

</div>
<div markdown="1"><span>核心问题</span>

当每项任务都配有一份独特、冗长且具有约束力的企业操作手册时，当前语言模型代理能否在延伸的多工具工作流中正确定位适用条款、保留关键细节、服从检查结果，并同时完成所有必需动作与避免所有禁止动作？

</div>
<div markdown="1"><span>作者直觉</span>

作者把任务提示设计得相对日常，把真正难度放在每个环境独有的手册中，并修改决定评分的审批人、阈值和流程细节。这样，代理不能只凭任务表述或固定政策模板行动，而必须查阅当前文件。再通过程序同时检查最终环境状态、外部服务记录和禁止副作用，评测便能识别“看起来完成了工作”与“确实按政策完成了工作”之间的差别。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

HANDBOOK.md不是一种需要训练的新模型，而是一套评测长上下文智能体能否持续遵守“常驻政策”的基准。每个任务将普通工作请求、独有的20至124页标准操作程序（SOP）以及可交互的虚构公司环境交给智能体；智能体必须从政策中定位适用规则，跨多轮推理和工具调用执行允许或要求的操作，并拒绝政策禁止的操作。执行结束后，程序化评分器检查工作区及所有外部服务的最终状态和副作用，只有全部准则均满足时才判定严格通过。
直观地说，该基准不只问智能体“有没有把事情办完”，而是问它是否像可靠员工一样，在处理邮件、表格和业务系统时始终按公司手册办事。任务故意让环境内的具体请求可能与手册冲突，并为每项任务改变关键阈值、授权人和流程细节，从而测试智能体是否真正阅读当前手册，而不是依靠记忆或常见业务惯例猜测规则。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造任务专属政策与工作请求

研究者对基础手册进行任务级变体化，改变决定评分结果的授权主体、数值阈值和程序细节，使65项任务各自拥有不同政策；手册以PDF、Word或HTML形式提供，长度为20至124页。

<div class="method-step__io" markdown="1">

**输入**：十份由领域专家撰写的基础手册，覆盖金融、医疗账单、保险、物流和人力资源五个领域，以及相应的日常专业工作请求。<br>
**输出**：一份独有的长篇SOP及一个独立于SOP表述的工作目标，例如按照SOP处理当天未读邮件。

</div>

**直观理解**：同类任务虽然使用相似公司的规章框架，但真正决定能否操作的规则会变化。因此，智能体不能背诵一套固定答案，必须查看眼前这份手册。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始化可重置的公司环境

系统在容器化Harbor环境中建立电子表格、PDF和Office文档工作区，并通过模型上下文协议（MCP）暴露模拟的电子邮件、聊天、日历、问题跟踪及商务服务；每次试验从规定的初始状态启动。

<div class="method-step__io" markdown="1">

**输入**：任务专属SOP、初始业务数据、文件工作区和待处理请求。<br>
**输出**：一个自包含、可交互且可在试验后检查完整状态的虚构公司环境。

</div>

**直观理解**：这不是让模型阅读一段静态对话，而是给它一个能操作文件和业务软件的“公司沙盒”。重置机制保证不同模型面对相同起点，因而结果可以公平比较。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 智能体检索规则并执行工作流

在统一的OpenHands智能体框架下，模型读取相关材料、识别适用条款和指令优先级，并通过多轮推理与工具调用完成检查、审批、更新或通信；若政策条件不成立，则应停止或拒绝相应动作。

<div class="method-step__io" markdown="1">

**输入**：用户工作请求、长篇SOP、环境中的消息与业务记录，以及可调用的MCP工具。<br>
**输出**：修改后的文件和服务状态、完整工具调用轨迹，以及智能体的最终回复。

</div>

**直观理解**：关键难点不是生成一段看似合理的答复，而是在较长操作过程中一直记住规则，并让后续行动服从检查结果。例如，即使邮件要求立即执行某操作，只要手册规定授权不足，智能体就应停下。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 双向程序化评分

每项任务使用预先编写的确定性评分准则：Expected-Output准则检查政策要求的动作是否发生，Incorrect-Behavior准则检查禁止动作是否未发生，并可通过精确计数不变量发现额外或重复操作；全基准共有824条准则，整个过程不使用大语言模型裁判。

<div class="method-step__io" markdown="1">

**输入**：试验结束后的工作区、各外部服务的最终状态和执行过程中产生的副作用。<br>
**输出**：每条准则的满足情况，以及该试验的严格通过或失败判定；论文还比较了允许恰好一条准则失败的近失判定。

</div>

**直观理解**：评分同时检查“该做的做了没有”和“不该做的有没有偷偷发生”。严格评分类似合规审计：即使大部分流程正确，只要漏掉一项要求或多做一次被禁止的操作，整项任务仍不通过。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。HANDBOOK.md是评测基准和可交互环境，论文没有提出待优化的新模型、训练损失或强化学习目标；其容器化环境可以用于未来的强化学习，但本文方法本身只进行模型配置评测。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 任务级政策变体化**

基准由十份基础手册扩展为65份任务专属政策，系统性修改命名授权人、审批阈值和关键程序细节；政策长度约为8K至79K tokens，且不存在两项任务共享完全相同政策的情况。

> 直观理解：该设计把“会不会背熟经常出现的规则”与“能不能阅读并执行当前规则”区分开。模型若凭常识套用旧阈值或旧授权关系，就会在确定性评分中失败。

**2. MCP公司工具环境**

环境将本地文档工作区与模拟邮件、Slack、日历、Jira和Shopify等服务组合起来，并通过MCP向智能体提供工具接口；任务采用容器化、可重置的Harbor格式。

> 直观理解：政策是否被遵守最终体现在真实动作上，而不只是模型口头声称合规。通过记录和检查多个服务的状态，基准能够发现发错消息、错误更新记录或产生未请求副作用等问题。

**3. 确定性双向合规评分器**

评分器以程序化rubric直接检查环境状态，分别编码必需结果与禁止行为；严格pass@1要求单次试验满足该任务的全部准则，不引入LLM裁判的主观判断。

> 直观理解：只看目标完成会把“事情做成但违反规定”误判为成功。双向评分把业务完成度和政策边界同时纳入，并能精确定位智能体是遗漏必要步骤，还是执行了本应阻止的操作。

**训练与推理**

评测时，研究者将任务请求、任务专属长篇SOP及环境工具交给待测模型，并使用统一的OpenHands框架驱动智能体进行推理和工具调用。智能体自行决定读取哪些文档、调用哪些服务以及何时停止；论文描述的任务平均约经历17个推理步骤和30次工具调用。试验结束后不依据最终文字回答人工打分，而是运行任务rubric检查文件系统及所有模拟服务的最终状态，并据全部准则是否满足生成严格pass@1结果。论文共比较30种模型配置、涉及11家提供商；不同推理努力设置被视为不同配置，以检验增加推理预算是否改善政策遵守。

**复现信息**

复现所需的核心组件是公开发布的65项任务、任务专属SOP、初始环境状态、824条程序化评分准则、Harbor容器配置及统一评测工具链；论文给出的代码与环境地址为https://github.com/surge-ai/handbook。公平解释结果时需要保留每项任务独有的政策变体和完全相同的可重置初始状态，并同时检查Expected-Output与Incorrect-Behavior准则；若只判断最终答复是否合理，或使用LLM裁判代替状态检查，就不再等价于论文的严格评测。源节选未明确给出模型采样温度、最大上下文设置、重复试验次数及所有工具级超参数，因此这些细节应标记为“原文未明确报告”，不能据此自行补全。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HANDBOOK.md：包含65个任务，覆盖财务与会计12项、HR 13项、保险13项、物流12项、医疗账单15项，来自10家虚构公司。每项任务由短工作请求、独立容器化环境、经定向变异的企业手册和程序化评分规则组成；手册为PDF、Word或HTML格式，共25/20/20项，长度中位数37页、范围20至124页，提取文本中位数14.9K tokens、范围8.3K至79.4K。每个任务使用不同政策版本，以检验模型是否读取当前规则而非依赖记忆。原文未明确报告训练集、验证集或测试集划分；该数据集在实验中整体充当评测集。
- 任务环境与工具状态：每项任务包含文件工作区以及按需配置的模拟Gmail、Slack、Google Calendar、Jira和Shopify服务。65项任务中，邮件与Slack各出现于62项，日历40项、Jira 14项、Shopify 4项；任务通常混有无关文件、旧版本和通信噪声。这部分不是独立数据集，而是用于检验智能体能否跨文件与服务搜集证据、执行操作并留下可验证的最终状态。
- 程序化评分规则集：65项任务共有824条验收标准，每项3至27条、平均12.7条。其中592条Expected-Output规则检查必需结果，232条Incorrect-Behavior规则检查禁止行为或越界修改。它不是训练标签，而是确定性评测器集合，用于同时衡量“该做的是否完成”和“不该做的是否避免”。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Strict pass@1**

一次试验只有在该任务的全部程序化规则均通过时才记为成功，然后对任务及每任务四次运行的结果取平均。它把任何一个必要输出缺失或任何一个禁止行为发生都视为完整工作流失败，是论文的主要排名指标。 （越高越好，因为更高表示智能体更常在一次执行中同时满足所有操作要求与政策控制。）

</div>
<div class="metric-item" markdown="1">

**pass@1 (N−1)**

每次试验允许恰好一条规则失败，其余规则必须通过。该指标用于区分“只差一个条件的近失误”和存在多个错误的全面失败，不作为主要排名标准。 （越高越好，但其合规含义弱于Strict pass@1；分数上升可能只是评分允许忽略一个关键控制，并不等价于安全部署。）

</div>
<div class="metric-item" markdown="1">

**平均逐规则得分**

计算一次试验中通过的规则所占比例，用于分析任务完成的细粒度程度，而不是决定排行榜名次。 （越高越好，因为表示满足的独立要求更多；但它可能掩盖单条高风险禁止行为，因此不能替代严格成功率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 30种模型配置的Strict pass@1总体比较

<div class="result-value" markdown="1">

排名第一的Claude Fable 5（adaptive/max）取得36.2%，第二名Claude Fable 5默认配置为34.2%；最佳非Anthropic配置GPT-5.6 Sol（max）为23.5%。

</div>

作者据此认为，即使最强配置也仍在接近三分之二的试验中至少违反一条规则，长手册约束下的端到端可靠性仍有很大提升空间。36.2%衡量的是极严格的整项任务成功率，而不是模型平均只完成了约三分之一的规则，也不能单独证明失败均由长上下文遗忘造成。

<div class="result-source" markdown="1">

来源：第5.1节 Main results；表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The subsequently released Claude Fable 5 raised the ceiling to 36.2%, 12.7 points clear of the strongest configuration from any other provider, but still fails nearly two of every three tasks under strict grading.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 前沿以下各模型配置的性能分布

<div class="result-value" markdown="1">

中间一组模型大致落在5%至16%的Strict pass@1区间，表2最低配置Grok 4.3为0.8%；最高36.2%与最低0.8%相差约45倍。

</div>

这说明该基准没有出现大多数模型都接近满分的饱和现象，并能拉开不同配置的端到端合规能力。它不表示分数低的模型完全无法完成子步骤，因为严格指标会把只错一条规则的试验也记为失败。

<div class="result-source" markdown="1">

来源：第5.1节 Main results；表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The spread is wide relative to many saturating benchmarks: the top and bottom of the table differ by a factor of 45, and configurations of the same model at different reasoning-effort settings differ by up to three points (Opus 4.8) or 2.7 points (Sonnet 4.6, where the adaptive/max setting is worth a 35% relative improvement).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 严格评分与允许一条规则失败的近失误评分比较

<div class="result-value" markdown="1">

在pass@1 (N−1)下，Claude Opus 4.8（max）约由21.9%升至46%，默认Opus 4.8约由18.9%升至41%，GPT-5.5约由21.5%升至32%。

</div>

不少严格失败轨迹实际上只差一条规则，说明模型常能完成工作流的大部分内容；但被遗漏的规则可能正是审批门槛、暂停条件或作用域边界，因此近失误分数不能被解释为可接受的实际合规率。不同模型的相对排序也会变化，表明模型不仅在失败频率上不同，在一次失败涉及多少规则方面也不同。

<div class="result-source" markdown="1">

来源：第5.3节 Strict versus near-miss grading；图3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under pass@1 (N−1), Opus 4.8 (max) rises from 21.9% to roughly 46%, Opus 4.8 (default) from 18.9% to about 41%, and GPT-5.5 from 21.5% to about 32%; across the frontier the relaxation roughly doubles scores.

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

- Claude系列配置，包括Claude Fable 5、Claude Opus 4.8和Claude Sonnet 4.6及其更高推理强度版本；它们构成主要前沿参照，并可比较同一模型默认与adaptive/max设置。
- OpenAI系列配置，包括GPT-5.6 Sol与GPT-5.5及其高推理设置；它们用于与排名最高的Claude配置比较，也用于观察增加推理强度是否稳定提升政策遵循。
- 其他供应商的中高端模型，包括Grok、Gemini、GLM、Kimi、DeepSeek、Qwen和Muse等；这些模型用于判断结果是否只反映单一模型家族，并刻画中间性能区间。
- 效率层与低分配置，如Gemini 3.5 Flash-Lite、Nemotron 3 Ultra、Inkling和Grok 4.3；它们提供性能、生成token量和成本维度的低端参照。论文共评测20个模型、30种配置，来自11家供应商，并非针对某一专门训练方法设置的传统消融基线。

**实验想回答的问题**

- 当前语言模型智能体能否在长达20至124页、规则相互关联且需要持续调用工具的企业工作流中，始终让手册中的常设政策约束其行为，并同时完成所有必需操作、避免所有禁止操作？
- 模型能力、推理强度以及评分严格程度如何影响政策遵循表现；失败主要体现为整体不会完成任务，还是仅违反少量但可能关键的控制条件？

**实验实现**

所有配置使用基于OpenHands agent SDK的统一智能体框架，在任务Docker容器内运行，并通过单一MCP端点访问文件系统及模拟服务。模型原样接收任务系统提示和用户指令，此后自主行动；环境不提供模拟用户，模型也被要求不要请求澄清。每次试验最多200次工具调用、最长1小时，单次工具调用超时300秒；不超过1 MB的工具观察不截断，另设上下文溢出时的摘要压缩器，但原文称实际评测中未触发。每个模型配置对全部65项任务各运行4次，即每配置260次试验；供应商或传输错误导致的中止会排除并重跑，而非计为失败。完成的试验平均约17个智能体步骤、30次工具调用。试验结束后，评分器在容器中读取最终工作区和服务状态，以Python验证器确定每条规则的通过或失败。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 同一模型默认推理强度与更高推理强度对比 | 提高推理强度使Opus 4.8提升3.0个百分点、Sonnet 4.6提升2.7个百分点、Fable 5提升2.0个百分点；GPT-5.5保持21.5%不变，GLM 5.2反而下降2.7个百分点。 | 该对比近似隔离了额外推理预算的作用：收益并不稳定，说明主要瓶颈不只是“思考不够久”。若错误源自漏读或错误采用规则，更多推理可能围绕错误前提展开，甚至推翻先前正确判断。由于各供应商的推理强度控制方式并不相同，这不是完全统一计算预算下的严格因果消融。 | 第5.1节 Main results；表2<br><span class="experiment-evidence">Raising effort improves Opus 4.8 (+3.0), Sonnet 4.6 (+2.7), and Fable 5 (+2.0), leaves GPT-5.5 unchanged (21.5% at both settings), and hurts GLM 5.2 (−2.7).</span> |
| 评分容错消融：Strict pass@1与允许失败一条规则的pass@1 (N−1)对比 | 前沿配置在容许一条规则失败后，分数总体约翻倍；例如Opus 4.8（max）从21.9%升至约46%，GPT-5.5从21.5%升至约32%。 | 这不是模型组件消融，而是评分定义的敏感性分析。它隔离了“最后一条失败规则”对整项成功判定的影响，证明严格低分中包含大量近失误；同时，由于那一条可能是关键合规控制，不能据此断言模型已基本适合无监督部署。 | 第5.3节 Strict versus near-miss grading；图3<br><span class="experiment-evidence">Under pass@1 (N−1), Opus 4.8 (max) rises from 21.9% to roughly 46%, Opus 4.8 (default) from 18.9% to about 41%, and GPT-5.5 from 21.5% to about 32%; across the frontier the relaxation roughly doubles scores.</span> |

**定性案例**

- Crestwood University的HR任务展示了基准如何检验跨来源规则整合：智能体需从41页SOP、SOP作者的邮件修订、员工约束、Jira离职工单以及已有283个事件的日历中，判断应为哪些人安排何时的离职面谈。正确结果只新增3个会议，使日历最终恰有286个事件，同时不得改动原有7封邮件、Jira事项或相关员工表格行。该案例说明评分不仅检查最终会议是否创建，还通过精确状态不变量检查智能体是否越界修改环境；但原文节选未给出具体模型在该案例上的运行结果。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：reused verified category during targeted regeneration
- 全文指纹：`4238394d666a78e0e49b8283a001473c2fb6461c062eaa8deb6b20c73f0ebe70`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
