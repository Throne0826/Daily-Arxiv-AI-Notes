---
title: "[论文解读] AgentGUI: An Interface for Observing and Steering Long-Running AI Agents"
description: "[arXiv 2607.26300][LLM Agent] AgentGUI旨在通过本地化图形界面，把多个长时间运行的AI智能体的执行过程变得可观察、可人工干预且可自动纠偏，从而缩小智能体自主能力与人类监督能力之间的差距。"
arxiv_id: "2607.26300"
announcement_date: "2026-07-30"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.881384+00:00"
source_sha256: "0916db90a362e269563c406900c1de897a4e853647d5217d70627223b21865d7"
tags:
  - "LLM Agent"
  - "大语言模型智能体"
  - "长期运行智能体"
  - "人类监督"
  - "智能体轨迹可视化"
  - "运行时引导"
  - "多智能体会话"
  - "图形用户界面"
  - "智能体运行框架"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2607.26300</p>

# AgentGUI: An Interface for Observing and Steering Long-Running AI Agents

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Xuan Zhao, Jiwoong Sohn, Qinyue Zheng, Michael Moor</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26300v1) · [PDF 下载](https://arxiv.org/pdf/2607.26300v1) · **关键词** 大语言模型智能体, 长期运行智能体, 人类监督, 智能体轨迹可视化, 运行时引导, 多智能体会话, 图形用户界面, 智能体运行框架<br>
**代码**: [https://github.com/eth-medical-ai-lab/agent-gui](https://github.com/eth-medical-ai-lab/agent-gui)  **项目页**: [https://agent-gui-project.github.io/](https://agent-gui-project.github.io/)  

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

AgentGUI旨在通过本地化图形界面，把多个长时间运行的AI智能体的执行过程变得可观察、可人工干预且可自动纠偏，从而缩小智能体自主能力与人类监督能力之间的差距。

**不用术语来说**：AI智能体如今可以连续工作数小时甚至数天，但人类往往只能面对冗长、难以浏览的执行记录，因而不容易迅速判断智能体正在做什么、是否偏离目标，以及何时需要介入；当多个智能体同时运行时，这种监督负担会进一步加重。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出并开源AgentGUI：一个本地部署、面向多并发长时任务的图形界面，统一提供智能体轨迹可视化、手动与自动引导，以及不同开源和前沿智能体框架之间的集成与协调。
- 通过受控用户研究和初步自动纠偏实验验证该设计的潜在价值：作者报告，界面使用户从智能体轨迹中识别关键信息的时间缩短38%（p=0.023），自动防漂移功能在0.8B至9B的小型本地模型上最高提升34个百分点的任务完成率；但后者仅验证了受限条件下的定量完成情况。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型智能体与人机交互的交叉领域。工具调用型大语言模型智能体可在数小时乃至数天内持续推理、调用工具并执行代码，但其运行记录主要面向机器，人在同时监督多个长期会话时难以及时理解智能体正在做什么、是否偏离目标以及何时需要介入。AgentGUI针对这一监督接口问题，提供本地部署的图形界面，将多会话管理、智能体轨迹可视化、运行时干预，以及不同开源和前沿智能体框架之间的协调集中到同一界面中。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大语言模型智能体（LLM agent）**

以语言模型为决策核心、能够在多轮过程中进行推理、选择工具并执行动作的系统。它不同于一次性问答模型，会根据工具返回结果继续行动，形成较长的执行过程。

</div>
<div class="concept-item" markdown="1">

**智能体运行框架（agent harness）**

负责维护智能体上下文、连接工具、执行动作并支持长时运行的软件环境，例如SWE-agent、OpenHands、OpenClaw和Hermes。它决定了智能体如何组织消息、调用工具及保存运行状态。

</div>
<div class="concept-item" markdown="1">

**智能体轨迹与运行时引导（trajectory and runtime steering）**

轨迹是智能体在一次任务中产生的推理、消息、工具调用、代码执行及结果序列；运行时引导则指人在任务尚未结束时介入并纠正或重定向后续行为。前者解决“看清过程”，后者解决“及时改变过程”。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个或多个并发、长期运行的智能体会话及其持续产生的事件流，包括消息、工具/API调用、终端或代码执行、文件与时间信息；这些会话可能来自不同智能体框架。系统假设智能体能够暴露相应运行事件，并在本地GUI中将其组织为不同粒度的轨迹视图，同时允许人工或自动机制在运行期间实施引导。输出不是单一预测标签，而是可供用户监督的实时可视化状态、会话与共享文件视图、调试信息，以及作用于在途会话的干预或重定向指令；核心应用场景是用户同时观察和协调多个长时智能体任务。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Agent-flow与IBM Agent Trajectory Explorer**: 二者代表轨迹可视化方向：通过图形界面呈现工具调用、子智能体活动或执行历史，使机器导向的原始记录更易理解。论文指出，这类系统增强了可读性和诊断能力，但缺少对正在运行的会话进行介入或重定向的机制；AgentGUI试图把观察与引导统一起来。
- **AutoGen Studio、AGDebugger、Magentic-UI与ResearStudio**: 这些工作代表运行时引导方向，分别支持多智能体工作流构建与调试、消息编辑和重置、人机共同规划与执行，或对深度研究智能体的实时介入。论文认为此类界面通常绑定特定框架，而AgentGUI关注可观察性、运行时引导以及不同开放智能体框架协作三者的结合。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

工具调用型大语言模型智能体已经能够自主完成端到端软件工程等复杂任务，并持续运行数小时或数天。任务执行时间越长、并发会话越多，人类就越难持续阅读轨迹、核验中间产物并及时纠正错误；监督界面的发展因此落后于智能体自主能力，削弱了委托工作的可验证性与可信度。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于执行记录或转录文本的事后检查**：监督者通过智能体产生的消息、终端动作或API调用记录还原执行过程，再从中寻找关键步骤和异常。本文结论将这类记录概括为“opaque transcripts”；所给章节未明确报告具体系统名称或系统性对比。
- **各智能体框架内部分散的运行与控制方式**：开源或前沿智能体框架分别负责启动和运行智能体，用户在相应环境中查看或控制会话。根据作者对“integration with and coordination between”不同框架的强调，可以判断现有监督入口较为分散；但所给原文未明确列举具体框架及其既有界面功能。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 冗长而不透明的轨迹不便于快速定位关键事件，导致监督者理解智能体状态和发现偏离目标所需的时间较长，也难以有效覆盖持续数小时或数天的任务。
- 面对多个并发会话和不同智能体框架，缺少一个能够同时汇总状态、展示不同粒度细节并就地纠正行为的统一入口；其后果是观察、核验与干预彼此割裂。该判断与论文的问题设定一致，但所给节选未提供完整相关工作比较。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种以人为中心、可本地部署的统一界面，使监督者能够在多个并发、长时间运行且可能来自不同框架的智能体会话中，既看清执行轨迹和产物，又能直接实施人工引导或自动防漂移。尤其需要实证检验：更结构化的可观察性是否真的降低信息定位成本，以及自动引导是否能改善能力较弱的本地智能体的任务完成情况。

</div>
<div markdown="1"><span>核心问题</span>

能否通过一个统一的本地图形界面，将长时、多会话智能体的轨迹展示、人工干预、自动纠偏和跨框架协调整合起来，并由用户研究与初步实验验证其对监督效率和任务完成率的改善？

</div>
<div markdown="1"><span>作者直觉</span>

如果把原本散落在消息、终端动作、API调用和文件中的过程信息组织成分层、可视的会话视图，人类就不必逐行阅读完整记录，而能更快找到异常与关键产物；再把纠正入口放在同一界面中，并让自动管理机制在智能体漂移时及时介入，就可能在错误累积之前把执行拉回目标。换言之，AgentGUI并非单纯增强底层模型能力，而是通过让行为“看得懂、改得动”，提高人机协作的可控性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

AgentGUI不是新的智能体模型，而是一个面向长时、多会话智能体的本地人机协作界面。其端到端流程是：用户在统一仪表盘中配置任务、模型、工具和上下文文件；后端在相互隔离的持久化环境中运行一个或多个智能体，并把推理、工具调用、终端执行、文件变化和资源统计实时转换为分层轨迹；用户据此直接中断、修改任务或切换智能体配置，也可调用自动管理器审计任务是否偏离目标；最终，系统将会话标记为完成，或把带证据的纠偏意见反馈给智能体继续执行。
技术上，该系统把“可观察性、运行时干预和跨智能体协作”整合在同一控制平面中：FastAPI后端以独立工作进程执行智能体回合，通过WebSocket向React前端流式传送事件，每个工作桌面对应一个持久Docker沙箱。通俗地说，它类似一个面向AI员工的项目办公室：用户不仅能看见每个员工做了什么、花了多久、产出了哪些文件，还能在其走偏时立即改派任务，或请一个管理者自动检查并给出返工意见。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 创建会话并配置智能体

用户从仪表盘选择空闲工作桌面并提交任务；系统实例化对应智能体会话，主要支持Hermes，并实验性接入Claude Agent SDK。多个处理同一任务的智能体可被编为团队，并通过共享产物开展协作。

<div class="method-step__io" markdown="1">

**输入**：用户任务提示、可选上下文文件，以及智能体的记忆、系统提示、模型和工具配置。<br>
**输出**：具有明确任务定义、执行配置、工作目录和隔离运行环境的一个或多个智能体会话。

</div>

**直观理解**：这一步相当于给AI员工分配工位、工作说明和可用工具；若任务需要复核，还可以让较强模型检查本地小模型的成果。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 隔离执行并实时采集轨迹

后端在独立工作进程及每桌持久Docker沙箱中执行智能体回合，同时捕获推理或生成内容、工具请求与响应、代码和终端执行、文件访问、时间信息及token遥测；事件经WebSocket持续发送到前端。

<div class="method-step__io" markdown="1">

**输入**：已配置的会话、当前任务状态、工作区文件及智能体产生的模型响应和工具请求。<br>
**输出**：可实时消费的结构化事件流，以及可保存和恢复的完整轨迹与工作区快照。

</div>

**直观理解**：系统不是等任务结束后再给出一份长日志，而是像直播监控一样持续记录动作；沙箱则把各智能体与宿主机、其他智能体隔开，降低相互干扰和安全风险。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 分层呈现智能体状态

界面按信息粒度组织轨迹：活动流区分推理、生成和工具交互，概览图呈现各阶段墙钟时间，调试日志展示逐调用信息与token数据，轻量控制台突出代码执行；文件页支持产物预览，Hermes派生的子智能体则以可展开对象显示。

<div class="method-step__io" markdown="1">

**输入**：结构化轨迹事件、任务定义、工作区产物、子智能体信息和调试遥测。<br>
**输出**：覆盖任务活动、时间分配、终端行为、文件产物和底层调用的多层可视化视图。

</div>

**直观理解**：同一段运行记录可像“摘要—时间线—详细日志”那样逐层查看，用户不必从混杂的原始文本中手工寻找关键动作。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 人工或自动纠偏并闭环执行

人工通道允许用户中断并重定向当前回合、修改任务定义供下一回合读取，或在会话中切换模型与配置；自动通道先把任务拆成可验证标准，再从轨迹和文件中收集证据，逐项判断完成情况并生成审计报告。若标准满足则标记会话已解决，否则将审计意见作为纠偏反馈，提示智能体恢复执行。

<div class="method-step__io" markdown="1">

**输入**：当前轨迹、任务定义、工作区文件，以及用户输入或按需/定时触发的管理器审计请求。<br>
**输出**：已完成的会话，或携带具体审计反馈并继续运行的纠偏会话。

</div>

**直观理解**：人工方式像主管即时叫停并重新说明要求；自动管理器则像验收员，先列验收清单，再查日志和成果，合格就结案，不合格就指出问题并要求返工。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。AgentGUI是智能体编排、观察和转向系统，论文没有提出需要训练的新模型或优化目标；自动管理器通过调用已有LLM进行任务分解、证据审计和反馈生成，而不是通过本文定义的损失函数学习。附录B给出的置换检验公式属于用户研究的统计分析，不是系统方法的训练目标，因此未列入方法方程。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 多粒度轨迹观察模块**

该模块将交错的模型内容、工具调用、执行输出和文件活动组织为活动流、时间概览、逐调用调试日志及代码中心控制台，并同时提供工作区产物预览和子智能体轨迹入口。不同视图共享同一会话状态，但服务于快速浏览、耗时定位、底层调试和结果核验等不同监督需求。

> 直观理解：长时智能体的原始记录通常像把思考、命令和文件操作混在一起的聊天记录；分层展示让用户先看整体，再按需钻取细节，减少理解成本。

**2. 运行时转向模块**

系统提供三类人工控制：直接消息可中断并重定向当前回合；任务页修改会在当前回合结束后由智能体复查；运行中切换配置可让更强模型接管停滞任务，或让本地模型承担后续监控。该设计把干预作用于仍在执行的会话，而非仅在失败后离线分析。

> 直观理解：观察到错误后，用户无需终止全部工作并从头开始，而可以即时补充要求、修正目标或更换更合适的模型。

**3. 基于证据的自动管理器**

LLM管理器可由用户主动调用，也可在工作桌空闲且尚未标记完成时按可配置间隔触发。其审计链包括任务标准分解、从智能体文本轨迹与工作区文件取证、逐项判定和报告生成；报告随后控制“标记完成”或“带反馈恢复执行”的分支。

> 直观理解：管理器并非只凭最后一句自报完成来判断，而是先明确什么叫完成，再检查过程记录和真实文件，因此更适合发现智能体遗忘目标、过早停止或产物不符合要求等漂移。

**训练与推理**

系统没有独立训练阶段。运行时，用户先选择智能体框架与模型并提交任务；后端在隔离工作进程和持久Docker工作区内迭代执行“模型响应—工具或代码操作—环境返回”回合，同时将事件实时流式传给界面。用户可以只观察，也可在任意时点直接介入、更新任务或切换配置。自动管理器在人工请求或满足定时触发条件时读取任务、轨迹和文件，形成可验证标准及证据化审计结果；若判断任务完成，系统将会话标记为solved，否则把报告交给原智能体，使其依据纠偏意见继续推理和行动。多个智能体组成团队时，协作媒介主要是共享产物，系统同时保留各自独立的执行环境和轨迹。

**复现信息**

公平理解和复现该系统所需的关键实现包括：前端采用React，后端为本地托管的FastAPI服务，二者通过WebSocket传输实时事件；每个工作桌拥有继承自Hermes实现的持久Docker沙箱，并以独立工作进程执行回合，从而隔离宿主机及其他智能体；桌面可完整保存和恢复，包括轨迹与工作区快照。主要智能体集成对象是Hermes，Claude Agent SDK支持仍属实验性质；运行模型既可通过Ollama完全置于用户本地硬件，也可连接远程GPU或托管推理服务。原文没有在所给章节中明确报告自动管理器所用具体模型、审计提示模板、默认审计间隔或标准分解算法，因此这些部分不能据现有材料精确复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- OrganSMNIST：用户研究中的第一类研究任务，轨迹由基于 Qwen3.5-27B 的 Hermes agent 执行 CNN 训练任务产生，并由冻结评分器评估。论文为该任务生成两条 rollout；每条轨迹配有关于总体活动、耗时、输出文件、终端操作和调试过程的问题。原文未明确报告本实验使用的数据划分与样本规模。
- MedXpertQA：用户研究中的第二类研究任务，智能体通过迭代系统提示词来回答医学问答。论文同样生成两条 rollout，用于检验界面是否支持理解提示词优化类轨迹，而非只适用于模型训练轨迹。原文未明确报告所用题目数量、数据划分或具体子集。
- 合成患者病历工作区：自动转向实验使用的隐私友好型模拟任务，工作区包含 98 个文件，要求智能体完成 15 项数据聚合任务并生成 15 个交付物；每种 Qwen3.5 worker 规模运行 50 次。该设置用于制造长程文件检索与写入中的遗漏或偏航，并通过程序评分器检查交付物是否存在。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**每题完成时间**

参与者从轨迹中定位信息并回答问题所需的平均秒数，衡量界面对轨迹理解和信息检索效率的支持。 （越低越好，因为在答案质量不下降的前提下，更短时间意味着监督长程智能体所需的人力成本更低。）

</div>
<div class="metric-item" markdown="1">

**回答准确率**

每条 rollout 的问题中回答正确的比例，用于判断更快的信息查找是否仍能正确识别智能体行为、耗时、产物、终端操作和调试信息。 （越高越好，因为它表示用户对轨迹关键信息的理解更可靠。）

</div>
<div class="metric-item" markdown="1">

**任务完成率**

程序评分器判定 15 个要求交付物均被正确生成的运行比例；分别在管理器审计前和 worker 根据反馈修正后计算。 （越高越好，因为它表示智能体更完整地满足了多项数据聚合与文件交付要求。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 用户研究：AgentGUI 与 Hermes Dashboard 的总体答题速度比较，8 名参与者、被试内配对设计。

<div class="result-value" markdown="1">

AgentGUI 将平均每题用时从 145 秒降至 90 秒，即缩短 38%，配对置换检验得到 p=0.023。

</div>

作者结果表明，AgentGUI 的轨迹组织方式能显著缩短关键信息查找时间。由于两种界面展示相同类别的信息，这一差异更可能来自信息结构与交互设计，而不是 AgentGUI 获得了额外数据。不过，样本仅有 8 人，且任务与参与者群体较集中，因此不能据此断言相同幅度会推广到所有用户、智能体框架或真实生产环境。

<div class="result-source" markdown="1">

来源：第 4.1 节 Results；图 4；附录 B

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Participants completed questions 38% faster with AgentGUI than with the baseline interface, taking on average 90 s rather than 145 s per question (p = 0.023, Appendix B, Fig. 4).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 用户研究：AgentGUI 与 Hermes Dashboard 的总体回答准确率比较。

<div class="result-value" markdown="1">

平均准确率由基线界面的 80% 提升至 AgentGUI 的 93%，p=0.031。

</div>

该结果说明速度提升没有伴随总体准确率下降，反而观察到更高的正确率，因此不支持明显的速度—准确率权衡。但作者特别指出，一名参与者在基线界面仅取得 50%，可能放大总体差异；这意味着准确率提升的稳健性弱于单看平均数时的印象，仍需更大样本复现。

<div class="result-source" markdown="1">

来源：第 4.1 节 Results；图 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Accuracy improved to 93% from 80% (p = 0.031, Fig. 4), although this absolute increase could be impacted by one participant scoring a low (50%) score on the baseline interface.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 自动转向实验：一次 Qwen3.5-27B 管理器审计前后，比较四种 Qwen3.5 worker 规模的任务完成率；每种规模 50 次运行。

<div class="result-value" markdown="1">

完成率分别从 10% 提升至 26%（0.8B）、54% 提升至 70%（2B）、44% 提升至 78%（4B）以及 92% 提升至 98%（9B）；最大绝对增益为 4B worker 的 34 个百分点。

</div>

一次自动审计在所有模型规模上都提高了完成率，且对留下较多“部分成果”的中等规模 worker 帮助最大。这支持管理器可以发现遗漏并促使 worker 补写交付物，但它只是合成文件工作区上的概念验证：前后比较没有独立的随机化控制管理器，也不能区分收益究竟来自高质量审计、额外一次执行机会，还是二者共同作用。

<div class="result-source" markdown="1">

来源：第 4.2 节 Results；图 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The lift is largest where the worker leaves partial work, while saturating near weakest and strongest models: 10% → 26% (0.8B), 54% → 70% (2B), 44% → 78% (4B), and 92% → 98% (9B).

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

- Hermes Dashboard v0.16.0：Hermes Agent 自带的轨迹可视化工具，是用户研究中 AgentGUI 的直接界面基线。两种界面暴露相同的五类信息，但组织和呈现方式不同，因此比较主要测试界面设计对信息查找与轨迹理解的帮助，而不是信息量差异。
- 未经管理器审计的 Qwen3.5 worker：自动转向实验的自身对照。程序评分器先记录智能体独立执行后的完成情况，再由 Qwen3.5-27B 管理器审计遗漏并要求 worker 修正，因而前后差异用于估计一次自动审计与反馈的增量作用。

**实验想回答的问题**

- 与原生 Hermes Dashboard 相比，AgentGUI 能否帮助用户更快、更准确、且以更低主观负担理解长程智能体轨迹中的关键信息？
- 当本地小型智能体在复杂文件工作区中遗漏任务时，AgentGUI 的自动管理器审计与反馈能否提高任务完成率，并且这种收益能否跨不同模型规模成立？

**实验实现**

用户研究招募 8 名定量学科的硕士或博士生，采用被试内设计。每位参与者查看两条不同研究任务的轨迹，其中一条使用 AgentGUI、另一条使用 Hermes Dashboard，以避免同一轨迹在两个界面间产生记忆迁移；界面顺序和 rollout 分配被平衡，每条 rollout 在每个界面下恰由两名参与者查看。参与者先获得五分钟界面探索时间，随后回答每条轨迹的 14–15 个问题。统计分析以参与者在 AgentGUI 与 Dashboard 下的配对差值为单位，使用精确双侧符号翻转置换检验，并报告配对 t 置信区间。自动转向实验让 0.8B、2B、4B 和 9B 的 Qwen3.5 worker 分别独立处理合成病历工作区；若任务未完成，Qwen3.5-27B 管理器审计工作区并给出反馈，worker 修正后再次由同一程序评分器评分。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 4B worker 的初始完成率低于 2B 并非简单反映能力更弱。作者观察到，4B 模型倾向于用绝对路径写入输出，而沙箱写保护会拒绝该操作，导致部分交付物未落盘；管理器发现缺失并提示改用可接受方式重写后，完成率明显恢复。该案例说明自动审计不仅能纠正语义层面的任务偏航，也可能捕获模型与执行环境之间的操作规范冲突；但这是作者对特定异常模式的解释，不构成系统性的错误类型评估。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces an interface for monitoring and steering long-running AI agents and improving their task completion.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`0916db90a362e269563c406900c1de897a4e853647d5217d70627223b21865d7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
