---
title: "[论文解读] IFCMemoryBench: Evaluating Long-Term Memory of LLM-Based Agents in BIM Information Retrieval"
description: "[arXiv 2607.26072][LLM 评测] 本文提出 IFCMemoryBench，用于检验大语言模型智能体能否在多会话 BIM 工作流中保存并调用历史项目知识，再将其与实时 IFC 模型查询结果结合起来回答问题。"
arxiv_id: "2607.26072"
announcement_date: "2026-07-30"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:25.832201+00:00"
source_sha256: "364b406abeb13c165612f930e01dd6ae298c5760d0bb4287235b01bcc1c68279"
tags:
  - "LLM 评测"
  - "LLM Agent"
  - "大语言模型智能体"
  - "长期记忆"
  - "建筑信息模型"
  - "IFC"
  - "多会话评测"
  - "工具增强信息检索"
  - "开放世界问答"
  - "IFCMemoryBench"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2607.26072</p>

# IFCMemoryBench: Evaluating Long-Term Memory of LLM-Based Agents in BIM Information Retrieval

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Changyu Du, Alexander Vosseler, Filippo Mazza, André Borrmann</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26072v1) · [PDF 下载](https://arxiv.org/pdf/2607.26072v1) · **关键词** 大语言模型智能体, 长期记忆, 建筑信息模型, IFC, 多会话评测, 工具增强信息检索, 开放世界问答, IFCMemoryBench  


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

本文提出 IFCMemoryBench，用于检验大语言模型智能体能否在多会话 BIM 工作流中保存并调用历史项目知识，再将其与实时 IFC 模型查询结果结合起来回答问题。

**不用术语来说**：工程人员可能在早先对话中确定材料参数、成本假设或客户要求，而这些信息并未写入建筑模型；数周后再次提问时，智能体既要记得这些决定，又要查询当前模型中的构件和数量。现有评测通常只检查智能体能否复述旧对话，无法判断它是否能把历史信息真正用于专业工程分析。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出把 IFC-Bench v2 中信息不完整的问题转换为多会话记忆任务的方法：将回答所缺少的项目背景分散植入历史会话，再要求智能体结合这些记忆与实时 IFC 查询完成后续探测问题。
- 构建 IFCMemoryBench，并以摄取、检索和利用三个环节分析代表性的向量式、图式与文件式记忆系统，从而揭示通用记忆系统迁移到 IFC 驱动的专业检索任务时存在明显能力缺口。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于“大语言模型智能体长期记忆”与“建筑信息模型（BIM）信息检索”的交叉领域。BIM以结构化数字模型描述墙、梁、房间、系统、材料、工程量及其关系，IFC是其主要交换格式；近期检索系统通常让智能体通过ReAct式工具调用或执行Python代码来查询IFC。既有任务大多是封闭世界、无状态的单次问答，即答案完全存在于当前IFC中；本文关注更贴近工程实践的开放世界、多会话情形：项目规范、客户决定、修正记录或计算假设可能只在先前对话中出现，智能体必须长期保存这些信息，并在之后将其与实时IFC查询结果结合。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**长期记忆（long-term memory）**

指智能体跨会话持久保存并复用信息的能力，区别于当前任务中的工作记忆和单次会话内的短期记忆。本文主要涉及项目事实、约束等语义式记忆，以及先前更正或决定等情景式记忆，不评估技能与流程层面的程序性记忆。

</div>
<div class="conceptitem" markdown="1">

**IFC与BIM信息检索**

BIM是建筑项目的结构化数字表示，IFC则是包含对象类型、属性和对象关系的语义丰富、面向对象交换模式。LLM智能体可通过工具查询或代码执行读取IFC中的构件属性、空间关系与工程量，而不是仅依赖语言模型自身知识作答。

</div>
<div class="conceptitem" markdown="1">

**开放世界、工具落地的多会话问答**

开放世界问题无法仅凭IFC回答，还需要模型外的项目规范、设计意图、排放因子或修正记录；“工具落地”表示答案还必须受实时IFC查询结果约束。多会话设置进一步要求这些外部信息来自较早会话，而非直接放入当前提示。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

IFCMemoryBench把IFC-Bench v2中因信息不完整而无法仅靠IFC回答的问题转换为多会话记忆任务。每个任务的输入由某一项目的若干先前聊天会话、当前探测问题以及可通过工具实时查询的IFC模型组成；先前会话分散植入IFC中缺失的项目上下文，当前问题原则上只有在恢复该上下文并取得相关IFC数据后才能回答。智能体需要依次完成记忆摄取、记忆检索和信息利用：把历史会话写成可复用记忆，在探测时找回所需事实，再把这些事实与IFC查询结果组合为最终答案。该设置覆盖143个记忆依赖任务、19个项目、23个IFC模型和共4,016个先前会话；核心假设是关键外部上下文不会在当前问题中重复提供，也未完整写入IFC。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$\mathcal{S}_{<t}$**

当前探测时刻之前的多轮或多次历史会话；这是便于说明任务的概念性记号，原文未给出正式符号。

</div>
<div class="notationitem" markdown="1">

**$\mathcal{M}$**

智能体从历史会话中建立并跨会话保存的长期记忆；具体实现可以是向量库、知识图谱或持久文件，原文未给出正式符号。

</div>
<div class="notationitem" markdown="1">

**$\mathcal{I}$**

当前项目的IFC结构化模型及其可查询内容；原文未给出正式符号。

</div>
<div class="notationitem" markdown="1">

**$q \rightarrow y$**

智能体针对当前探测问题q，结合从长期记忆取回的上下文与IFC实时查询结果生成最终答案y；原文未给出正式公式。

</div>

</div>

**直接相关的工作**

- **IFC-Bench v2（Hellin et al., 2026）**: 它评估智能体通过自适应探索和代码执行查询IFC的能力，并为本文的任务构造提供不完整信息问题来源；但原基准以彼此独立的问答为主，未直接检验跨会话长期记忆。
- **LongMemEval（Wu et al., 2025a）**: 它是面向聊天助手长期交互记忆的通用基准，可检验跨对话事实恢复；与本文不同，它并非针对BIM工程场景，也不直接要求将记忆内容同实时、结构化的IFC工具查询结合。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

真实 BIM 项目持续数周或数月，规格确认、客户决定、修正意见、排放因子和工程惯例等关键信息常存在于对话中，而不在 IFC 模型内。后续问题又可能同时依赖这些历史知识和 IFC 中的实时对象、关系及数量；若智能体遗忘、误记或错误拼接信息，就可能给出不完整甚至误导性的工程结论。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **无状态的 LLM-BIM 信息检索与 IFC 问答基准**：智能体通过 ReAct 式工具调用检查 IFC 文件，并针对彼此独立的自然语言问题生成答案；这类系统通常假设所需证据都能从当前 IFC 模型中取得。
- **通用长期记忆系统及对话记忆基准**：记忆系统通常利用向量存储、知识图谱或持久化文件保存跨会话信息；LongMemEval、MemoryAgentBench 和 MemoryArena 等基准主要在开放域或角色设定对话中检查事实、偏好和历史事件的记忆能力。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 无状态 BIM 基准忽略跨会话形成但未写入 IFC 的项目知识，因此无法测试智能体能否在长期项目中延续需求、假设和决策，也无法覆盖“历史上下文加实时模型证据”这一真实回答条件。
- 通用对话记忆评测侧重找回语义相关内容，却不直接检验专业工具环境中的证据整合；在 BIM 中，仅主题相关并不够，记忆还必须完整保留精确事实、单位、实体指代、工程假设及其与 IFC 对象的联系，否则检索结果即使相关也可能无法用于可靠计算或判断。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种工具落地、领域特定且真正依赖跨会话信息的评测设置，能够区分失败究竟发生在历史信息写入、所需证据检索，还是记忆与结构化 IFC 数据的联合使用阶段，并同时评价最终答案和记忆内容本身的质量。

</div>
<div markdown="1"><span>核心问题</span>

代表性的通用长期记忆系统能否在多会话 BIM 信息检索中，可靠保存项目知识、按需取回完整证据，并将其与实时 IFC 查询结果结合，从而正确回答仅靠对话记忆或仅靠模型数据都无法回答的问题？

</div>
<div markdown="1"><span>作者直觉</span>

把原本因缺少外部背景而无法仅凭 IFC 回答的问题改造成多会话任务，可以人为控制“必须记住什么”和“必须查询什么”：历史会话提供规格、假设或修正，IFC 工具提供对象与数量，最终问题迫使智能体合并两类证据。再把过程拆成摄取、检索和利用三个环节，就能定位通用记忆系统究竟是没有形成完整项目知识、没有找到它，还是找到后不会与模型证据共同推理。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法不是训练一种新的记忆模型，而是构建并运行一个面向BIM信息检索的长期记忆评测流程。每个任务先把IFC模型中缺失的项目知识分散到25至40个历史会话中；被测记忆系统按时间顺序吸收这些会话并形成记忆库。探测阶段，统一的ReAct式代理接收最终问题，可访问记忆层和只读IFCQuery工具，将历史项目知识与实时IFC查询结果结合为答案；随后两个经专家抽样验证的LLM裁判分别评估答案质量与记忆质量。直观地说，系统不仅要“记得以前说过什么”，还要知道此刻该找哪段记忆，并把它与建筑模型里的实时数据正确拼接起来。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造记忆依赖任务

三个高性能IFC信息检索系统分别执行原问题，LLM交叉分析其轨迹以确定模型能够提供的实体、属性集、数量和空间包含信息；另一LLM将问题标为not_in_ifc、needs_external_info或partially_answerable_from_ifc，并剔除仅凭IFC即可完整回答的样本。

<div class="method-step__io" markdown="1">

**输入**：IFC-Bench v2中第4类不完整信息问题、对应IFC模型及原始标准答案。  
**输出**：确实依赖模型外知识的问题，以及每题可由IFC提供的信息边界和记忆依赖类型。

</div>

**直观理解**：这一步先划清“模型里有什么、模型外还缺什么”，避免把普通IFC查询误当作长期记忆任务。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成缺失知识、标准答案与历史会话

具备网页搜索和代码解释器的生成代理补充标准、排放因子、成本等外部事实，并合成无法公开查得的项目规范或进度信息，再将其与IFC信息组合成标准答案；随后把关键知识以顺带说明、用户纠正或背景条件等形式分散到每题25至40个历史会话中，并使用仅能访问当前会话和IFC工具的ReAct代理回放成完整对话。

<div class="method-step__io" markdown="1">

**输入**：保留的问题、其记忆依赖标签以及已提取的IFC侧信息。  
**输出**：143个多会话任务，包括4,016个历史会话、隐藏的目标记忆内容、探测问题和标准答案。

</div>

**直观理解**：需要记住的线索不会集中写成一张答案卡，而是像真实项目沟通一样散落在大量日常对话中；隔离式回放可防止标准答案或其他会话的信息泄漏。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 顺序写入长期记忆

被测系统逐会话更新状态：向量方案抽取独立文本事实并嵌入存储，时序图方案抽取实体、关系和有效时间，文件方案由写入代理持续更新memory.md；系统需要自行决定保留、概括、覆盖或丢弃哪些内容。

<div class="method-step__io" markdown="1">

**输入**：按时间排列的历史会话S_1至S_{t-1}及初始记忆库M_0。  
**输出**：探测前的累积记忆库M_{t-1}，其具体形式可以是向量条目、时序知识图或Markdown项目摘要。

</div>

**直观理解**：这不是把全部聊天原样塞进搜索库，而是边读边整理项目笔记；一旦写入时漏掉或错误压缩关键条件，后续检索通常无法补救。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 动态检索并联合IFC推理

探测代理自行决定发出多少个记忆查询及其措辞，合并各次检索结果形成R_t；随后通过ReAct过程查询实时IFC模型，并结合Q_t、R_t和工具结果生成最终答案A_t。文件记忆直接注入系统提示，向量和图记忆则通过统一的search_project_memory接口访问。

<div class="method-step__io" markdown="1">

**输入**：探测问题Q_t、累积记忆M_{t-1}以及只读IFCQuery工具T_{\mathrm{IFC}}。  
**输出**：最终回答、实际取回的记忆内容以及IFC工具调用轨迹。

</div>

**直观理解**：代理必须一边翻项目笔记、一边查建筑模型：历史对话可能给出规范或单价，IFC则给出构件和工程量，二者缺一不可。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 顺序、在线且有状态的记忆写入

$$
M_i=f_{\mathrm{ingest}}(M_{i-1},S_i),\quad i=1,\dots,t-1
$$

**符号说明**

- $S_i$：探测前第i个历史聊天会话。
- $M_{i-1}$：处理第i个会话之前已经累积的记忆库。
- $f_{\mathrm{ingest}}$：记忆系统的写入函数，负责抽取、合并、概括、覆盖或丢弃会话内容。
- $M_i$：吸收会话S_i之后更新得到的记忆库。
- $t$：最终探测发生的时间索引，因此共有t-1个先前会话。

<div class="equation-explanation" markdown="1">

**直观理解**：每段新会话都不是独立存档，而是与当前项目记忆共同决定下一版记忆。这体现了长期记忆与普通追加式RAG索引的差别：写入阶段已经发生选择和状态更新，关键事实可能被整合，也可能在此处丢失。  
**原文位置**：第3.1节，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 代理驱动的记忆检索与答案生成

$$
\begin{aligned}R_t&=\bigcup_{j=1}^{k}f_{\mathrm{retrieve}}(q_j,M_{t-1})\subseteq M_{t-1},\\A_t&=\mathrm{LLM}(Q_t,R_t,T_{\mathrm{IFC}}).\end{aligned}
$$

**符号说明**

- $M_{t-1}$：所有探测前会话处理完毕后的累积记忆库。
- $q_j$：探测代理自行构造的第j个记忆查询。
- $k$：代理在本题中决定发出的记忆查询次数。
- $f_{\mathrm{retrieve}}$：记忆系统提供的检索函数，针对一个查询返回记忆库的固定子集。
- $R_t$：k次查询结果的并集，即探测时实际提供给代理的记忆。
- $Q_t$：最终的记忆依赖探测问题。
- $T_{\mathrm{IFC}}$：用于读取实时IFC模型信息的查询工具。
- $A_t$：语言模型结合问题、检索记忆和IFC工具结果生成的最终答案。
- $\mathrm{LLM}$：执行ReAct式推理、工具调用和答案生成的探测语言模型代理。

<div class="equation-explanation" markdown="1">

**直观理解**：检索覆盖面既受底层搜索能力影响，也受代理是否提出正确查询影响；多次结果合并后，代理还必须把记忆中的项目约定与IFC中的结构化事实联合使用。该分解使研究者能分别定位系统侧检索、代理侧查询和答案利用阶段的失败。  
**原文位置**：第3.1节，公式(2)与公式(3)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文提出的是基准构造与评测方法，没有报告针对IFCMemoryBench训练或微调被测记忆系统，也没有定义可优化的损失函数；公式描述的是会话写入、检索和推理过程，而非梯度训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 可替换长期记忆层**

评测固定探测代理与IFC工具，仅替换记忆层。Mem0式向量记忆将抽取出的文本事实嵌入后执行top-k语义搜索；Graphiti式时序图把会话保存为带时间戳的episode，并建立实体、事实关系及有效时间，再以语义和关键词混合搜索返回关系、实体摘要和时间信息；DeepAgents式文件记忆则由代理顺序维护紧凑的memory.md。

> 直观理解：统一外围代理后，性能差异更能归因于“项目知识怎样被写下和取回”，而不是不同IFC工具或答题代理造成的混杂。三类方案分别近似可搜索卡片、带关系的项目知识网和人工维护的项目笔记。

**2. 统一的ReAct式BIM探测代理**

所有条件使用相同提示策略和代理框架，并拥有对IFCQuery命令行工具的只读访问。向量与图方案通过search_project_memory(query, limit)暴露记忆；文件方案把memory.md作为只读项目上下文直接注入系统提示，带引用版本还可依据[S003-M02]等标识在prior_sessions.json中用grep或read_file核验原消息。

> 直观理解：ReAct表示代理可交替进行推理和工具调用，而不是只生成一次文本。统一接口保证比较基本公平；引用机制则让摘要中的事实能够回到原对话核查，降低压缩笔记造成的失真风险。

**3. 双裁判诊断模块**

两个LLM裁判使用探测问题、标准答案、植入知识、系统答案和检索记忆进行二元维度判定。作者用同一随机40题样本进行专家复标：答案正确性标签一致38题，原始一致率95%、Cohen's κ为0.90；记忆正确性标签40题全部一致。

> 直观理解：只看最终答案无法判断错误来自写入、检索还是使用，因此需要单独检查记忆链路。专家抽样验证说明裁判与领域人员在该样本上高度一致，但它仍属于有限样本上的有效性证据，而不是人工全面复核。

**训练与推理**

数据构造阶段使用多个LLM代理完成IFC轨迹交叉分析、可回答性筛选、外部知识补全、标准答案合成、历史会话生成和隔离式回放，并由人工审查剔除答案错误、植入知识与IFC冲突或探测问题有歧义的样本。评测阶段不进行任务内训练：每个记忆系统先按顺序摄取该任务的全部历史会话，再由统一探测代理访问其记忆层和IFCQuery回答问题，最后由双LLM裁判评分。无记忆条件直接丢弃历史会话，作为判断问题是否真正依赖记忆的下界。

**复现信息**

公平比较的关键控制项是：所有系统共用同一ReAct式BIM代理、固定提示策略和只读IFCQuery，仅改变记忆的写入、检索与暴露方式；不同任务通过元数据隔离，防止跨项目记忆污染。向量记忆保存抽取后的独立文本条目并执行top-k相似度搜索；时序图保存带时间戳的会话来源、实体与关系，并采用语义和关键词混合搜索；文件记忆逐会话更新单个紧凑Markdown文件，分为无引用和带稳定消息引用两种形式。原文节选未明确报告嵌入模型、top-k具体取值、LLM型号、提示全文及裁判解码参数，复现时需进一步核对论文其余章节或代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- IFCMemoryBench：由IFC-Bench v2中的信息不完整问题构造，包含143个多会话任务、19个项目、23个公开IFC模型和4,016个先前会话，覆盖建筑、结构、机电、给排水、通风与城市等专业。每个任务把IFC模型中缺失但回答所必需的项目背景植入先前对话，随后要求代理结合该记忆与实时IFC查询回答探测问题。全基准共有95,003条消息，其中用户消息9,488条、助手消息45,983条、工具消息39,532条；平均每个任务28个先前会话。原文节选未报告训练、验证、测试划分，实验角色是统一的最终评测集。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**答案准确率（Ans-acc.）**

由答案评审器分别判断正确性（Corr.）、完整性（Cmp.）和相关性（Rel.）；只有三项均为“是”的任务才计为答案准确。该严格合取指标防止把主题相关但遗漏关键条件的答案算作成功。 （越高越好，因为它表示更多任务同时满足事实正确、信息充分且回答对象无偏离。）

</div>
<div class="metricitem" markdown="1">

**记忆准确率（Mem-acc.）**

由记忆评审器判断检索内容是否相关（R-rel.）、是否覆盖回答所需关键事实（R-cov.），以及最终答案是否正确使用这些记忆（A-mem.）；三项同时成立才计为成功。评审时将代理轨迹中的记忆内容与隐藏目标记忆事实比较，而不是评价整体答案文风。 （越高越好，因为它衡量从找到合适记忆到实际使用记忆的完整链路是否成功。）

</div>
<div class="metricitem" markdown="1">

**Wilson 95%置信区间**

针对143个任务上的二项成功率给出不确定性范围，用于判断观察到的系统差距是否可能只是有限样本波动；它不是独立的质量分数。 （不存在单调的越高或越低越好；区间越窄表示成功率估计越精确，而比较系统时应结合区间重叠情况，不能只看点估计排名。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 无长期记忆下界，固定Grok-4.3探测代理

<div class="result-value" markdown="1">

No memory的正确性为22.4%、完整性为3.5%、相关性为92.3%，但严格答案准确率为0.0%（95% CI：[0.0, 2.6]）。作者据此认为，没有任何任务在同时满足正确、完整和相关三项要求时成功，说明该基准确实要求跨会话信息。

</div>

高相关性但零严格准确率意味着代理通常理解了问题主题，也可能从IFC中得到部分信息，却无法补齐只存在于旧会话中的项目事实。这支持基准的记忆必要性，但不表示无记忆代理的每个局部陈述都错误，也不能单凭该结果区分缺失记忆与工具使用不足各自造成的影响。

<div class="result-source" markdown="1">

来源：表2，No memory行；第4.3节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">No memory | 22.4 [16.3, 29.9] | 3.5 [1.5, 7.9] | 92.3 [86.8, 95.7] | 0.0 [0.0, 2.6] | — | — | — | —</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 部署现实写入范围下的最佳系统：Mem0向量记忆，固定Grok-4.3探测代理

<div class="result-value" markdown="1">

Mem0取得44.4%正确性、33.1%完整性、100.0%相关性和32.4%答案准确率（95% CI：[25.2, 40.5]）；其记忆相关率为90.1%、关键事实覆盖率为49.3%、答案使用记忆率为82.4%，严格记忆准确率为47.2%。它是该固定代理主比较中表现最好的系统，但仍有超过三分之二任务未达到严格答案准确标准。

</div>

Mem0通常能找到同项目、同主题的内容，而且当有用内容出现时代理往往会采用；真正明显的断点是只有约一半任务检索到了全部关键事实。因此，结果更支持“记忆表示或访问不完整”是当前主要瓶颈，而不是“代理完全不会使用记忆”。不过，这只是受控设置中的关联性诊断，不能证明向量架构在所有模型、领域或写入策略下都优于图和文件记忆。

<div class="result-source" markdown="1">

来源：表2，Mem0 (vector)行；第4.3节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Mem0 (vector) | 44.4 [36.4, 52.6] | 33.1 [25.9, 41.2] | 100.0 [97.4, 100.0] | 32.4 [25.2, 40.5] | 90.1 [84.1, 94.0] | 49.3 [41.2, 57.4] | 82.4 [75.3, 87.8] | 47.2 [39.2, 55.4]</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 图式记忆Graphiti，固定Grok-4.3探测代理

<div class="result-value" markdown="1">

Graphiti的答案准确率为21.0%（95% CI：[15.1, 28.4]），记忆相关率达到81.8%，但关键事实覆盖率仅27.3%，严格记忆准确率为25.9%。其答案相关性为99.3%，而完整性只有22.4%。

</div>

图检索经常能返回主题相关记录，却没有把回答所需的规格级事实作为连贯证据一并提供。作者将这种相关性与覆盖率的落差解释为事实可能分散在不同节点和边上；从实验设计上看，这一结果揭示的是默认Graphiti表示及检索配置在该任务上的问题，并不能证明知识图谱原则上不适合BIM记忆。

<div class="result-source" markdown="1">

来源：表2，Graphiti (graph)行；第4.3节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Graphiti (graph) | 32.2 [25.1, 40.2] | 22.4 [16.3, 29.9] | 99.3 [96.1, 99.9] | 21.0 [15.1, 28.4] | 81.8 [74.7, 87.3] | 27.3 [20.6, 35.1] | 74.1 [66.4, 80.6] | 25.9 [19.4, 33.6]</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 基准的持久事实只植入用户消息，因此“仅用户消息”写入条件天然占优，写入范围消融不能直接代表真实部署中事实可能来自助手、工具或外部文档的情况；主实验虽采用更现实的“用户消息加最终答案”，仍是合成或公开来源派生的上下文。
- 主结果只覆盖143个任务，并统一使用Grok-4.3作为探测代理、评审器及系统内部LLM组件；若干置信区间重叠，细小排名差异不稳健。LLM评审虽经专家验证，仍不能替代跨模型、跨评审器及更大规模真实工程项目上的复核。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- No memory：不给代理跨会话记忆，仅允许其依靠当前任务和IFC查询。它是必要的下界，用于验证任务是否确实无法仅凭模型内信息完成。
- Mem0（向量记忆）：将抽取出的记忆项存入Qdrant，并使用默认嵌入模型进行语义检索。它代表以稠密向量相似度为核心的通用记忆架构。
- Graphiti（图记忆）：以Neo4j保存图结构，采用默认图模式，并通过RRF融合BM25词法候选与稠密语义候选。它检验实体—关系表示是否比独立记忆片段更适合保存项目知识。
- Markdown文件记忆：使用DeepAgents MemoryMiddleware，在每一步从磁盘重新载入memory.md；实验包含保留引用的cited版本与不保留引用的uncited版本。两者共享存储和注入机制，因此其差异主要反映写入内容是否可追溯、是否形成自包含事实。

**实验想回答的问题**

- 在必须结合跨会话项目知识与实时IFC模型查询的专业任务中，向量式、图式和文件式长期记忆系统能否让固定的探测代理准确回答问题；性能瓶颈主要位于记忆写入、检索覆盖还是答案利用环节？
- 当存储与检索机制保持不变时，写入记忆的会话范围如何影响性能；当已存记忆保持不变时，探测大模型的能力又如何影响代理侧的记忆搜索与使用？

**实验实现**

主实验固定同一个基于DeepAgents实现的ReAct探测代理，只替换记忆层，以尽量把差异归因于记忆架构。代理仅配备bash工具来运行ifcquery，其他无关DeepAgents工具被移除；它可通过命令检查IFC概要、选择实体、读取属性与关系等。Grok-4.3同时用于探测代理、LLM评审器以及各记忆系统内部的LLM组件，温度设为0；各系统除文中注明之处外使用默认配置。主比较采用“用户消息加助手最终答案”的写入范围，因为部署中的记忆系统无法预先知道哪些轮次含有持久事实；仅写入用户消息被视为接近预筛选 oracle 的条件。每个二元评审维度按任务统计阳性比例，并报告Wilson 95%置信区间。需要注意，同一模型兼任代理、系统组件和评审器有利于控制变量，但不能证明结果可直接推广到其他模型或人工评测协议。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 写入范围消融：仅用户消息、用户消息加助手最终答案、完整轮次；保持存储、检索和探测代理不变 | 三个被测系统均在仅写入用户消息时取得最佳结果；扩大到助手答案、推理过程、工具调用及输出后性能下降。所给节选未包含表3的具体分数，因此无法可靠报告变化幅度。 | 该消融隔离了“写什么进记忆”的影响。由于基准构造时持久事实只被植入用户消息，用户消息-only条件相当于提前知道事实所在位置的近似oracle；更宽范围主要增加干扰文本。因此结果证明这些系统对写入噪声敏感，但不能据此一般化为真实项目中永远不应保存助手或工具信息，因为真实工作流中的新事实也可能由这些来源产生。 | 第4.4节，表3（具体数值未出现在所给节选中）<br><span class="experiment-evidence">Across all three systems, the best results come from ingesting only user messages (Table 3).</span> |
| Markdown记忆质量消融：cited与uncited共享相同文件存储及注入机制 | cited版本的答案准确率为24.5%、关键事实覆盖率为43.4%、严格记忆准确率为38.5%；uncited版本对应为17.6%、24.6%和24.6%。观察差值分别为+6.9、+18.8和+13.9个百分点。 | 由于两种版本共享存储与注入方式，这一对照主要隔离写入内容是否保留出处并形成自包含事实。最大的提升出现在关键事实覆盖率，支持“可追溯、完整的事实单元比压缩摘要更容易复用”的解释；但原文仅称其为提示性结果，不能排除两种写入文本在长度、措辞或信息量上的伴随差异。 | 第4.3节；数值来自表2的Markdown cited与Markdown uncited两行<br><span class="experiment-evidence">The cited variant has higher observed scores than the uncited one, suggesting that memory should preserve traceable, self-contained project facts rather than compressed session summaries.</span> |

**定性案例**

- Graphiti构成机制层面的定性案例：检索结果可与正确项目和主题相关，但规格级事实可能被拆散到多个节点与边中，未以完整证据包返回给代理。作者用这一现象解释其81.8%的检索相关率与27.3%的关键事实覆盖率之间的明显落差。该案例提示，专业BIM记忆不仅需要实体关系，还需要把来源、限定条件、数量、单位和适用范围组织成可一次取回的事实结构。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It presents a benchmark that evaluates long-term memory ingestion, retrieval, and use by LLM agents operating over structured BIM environments.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`364b406abeb13c165612f930e01dd6ae298c5760d0bb4287235b01bcc1c68279`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
