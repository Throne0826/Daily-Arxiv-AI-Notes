---
title: "[论文解读] C-Unseen: Weak Signal Detection in Dynamic Temporal Knowledge Graphs via LLM Reasoning"
description: "[arXiv 2608.26870][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.26870"
announcement_date: "2026-08-28"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:46:18.253796+00:00"
source_sha256: "137037b2d7fa5e0c75cf55dfe193369dd2a902f160b8d9b75d4547bcda299ba1"
tags:
  - "LLM Reasoning"
  - "弱信号检测"
  - "动态时间知识图谱"
  - "时间知识图谱"
  - "大型语言模型"
  - "罕见子图"
  - "跨时间佐证"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.26870</p>

# C-Unseen: Weak Signal Detection in Dynamic Temporal Knowledge Graphs via LLM Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Yassir Lairgi, Ludovic Moncla, Khalid Benabdeslem, Rémy Cazabet, Pierre Cléau</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: INSA Lyon, CNRS, UCBL, LIRIS, UMR5205, 69621 Villeurbanne, France</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26870v1) · [PDF 下载](https://arxiv.org/pdf/2608.26870v1) · **关键词** 弱信号检测, 动态时间知识图谱, 时间知识图谱, 大型语言模型, 罕见子图, 跨时间佐证<br>
**代码**: [https://github.com/AuvaLab/itext2kg](https://github.com/AuvaLab/itext2kg)

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

弱信号检测面向战略监测场景，目标是在重大变化得到明确确认之前，从零散、低可见度的信息中识别其早期迹象。传统关键词频率与主题模型主要衡量词项或主题的统计变化，难以表示“谁与谁发生了何种关系”；无类型时序图虽能追踪局部连接模式，却缺少实体类别和关系语义。时间知识图谱将文本表示为带时间信息的实体—关系事实，例如“WHO—发布警报—猴痘”，从而同时保留语义结构与时间线索。本文进一步采用动态时间知识图谱，使监测系统能够随新文档到达而形成连续快照，并区分事实被系统观察到的时间与事实自身的有效时期；在此背景下，弱信号被定义为最初罕见、语义一致，并在连续快照中得到重复出现或其他事实佐证的子图，而不是单个突增词项。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**时间知识图谱（Temporal Knowledge Graph, TKG）**

以实体和有类型关系构成图，并为事实附加时间信息；一个事实可理解为“主语—关系—宾语—时间”。它比词频或主题分布更适合表达事件涉及的对象、关系及发生时间。

</div>
<div class="concept-item" markdown="1">

**动态时间知识图谱（Dynamic Temporal Knowledge Graph, DTKG）**

由随数据到达而更新的一系列知识图谱快照组成，并通过双时间建模区分事实的观察时间与有效时期。这样既能保存“何时看到该事实”，也能在文本明确给出时间范围时记录“该事实何时成立”。

</div>
<div class="concept-item" markdown="1">

**弱信号与强信号**

弱信号是重大变化尚未确立时出现的低可见度、碎片化先兆，其意义通常依赖后续事实的佐证；强信号则是变化已经公开确认、可明确判断的锚点事件。本文关注的不是一般异常，而是能够在强信号之前形成连贯证据链的罕见子图。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是从持续变化的文本来源构建的动态时间知识图谱，可视为按观察时间排列的快照序列；每个快照包含实体、带类型的关系及相应时间信息。任务是在不能借助未来强信号确认信息的监测条件下，先找出与当前快照主导叙事存在语义张力的罕见且连贯的子图，再跨连续时间步追踪它们是否持续出现或获得佐证。输出是被判定为真实弱信号的子图及其时间轨迹；核心假设是，有意义的早期迹象不仅具有低可见度，还会通过后续相关事实逐渐“增殖”，而一次性噪声不会形成同样的跨快照证据链。本文的数据语境还区分背景事实、弱信号、弱信号的前置信息佐证以及强信号，强信号之后的事实不属于可评分的前兆集合。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$t_{obs}$**

观察时间，即某条事实被文档报告并进入动态知识图谱的时间；它不一定等于事实实际开始成立的时间。

</div>
<div class="notation-item" markdown="1">

**$t^{\text{weak}}_{s}$**

与强信号事件 $s$ 对应的最早已标注前兆日期。

</div>
<div class="notation-item" markdown="1">

**$t^{\text{strong}}_{s}$**

强信号事件 $s$ 被公开确认或确立的日期。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{A}(s)$**

强信号 $s$ 的锚词集合，用于判断检测结果与该强信号是否具有足够的共享语义线索。

</div>

</div>

**直接相关的工作**

- **Yoon 等人的关键词频率方法**: 以文档中词项的分布变化区分弱、潜在或强信号，是本文所针对的统计型路线；它无法显式建模实体间的有类型关系，而且单词级检测在要求多个共享锚词时受到结构性限制。
- **基于 graphlet 的时序交互网络弱信号检测**: 通过小型局部子图模式刻画网络结构随时间的演化，为本文利用子图追踪信号提供了直接背景；但其图是简单、无类型的，不能保存命名实体、关系类型及知识演化的语义上下文。

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

C-Unseen把动态时间知识图谱（DTKG）视为可持续更新的记忆，并在每个观测时刻$t$执行“先找异常、再查延续”的两阶段推理。输入是当前快照$\mathcal{G}_s^t$及记忆中保留的历史连接子图；模块1先让大语言模型概括当前快照的主导叙事，再找出与该叙事存在语义张力、但并非标签错误等图谱伪影的稀有五元组，随后用实体间最短路径补足这些五元组的结构语境。模块2把当前连接子图与历时连接子图逐一比较：只有当前内容延续并推进了较早时刻已经出现的张力，相关子图才被标注为弱信号并写回DTKG；完成匹配的信号及相关连接子图随后退出后续提示，避免重复报警。

技术上，该方法没有训练新的预测器，也没有通过一个数值异常分数直接设阈值，而是以提示驱动的链式思维（CoT）完成语义判断。直观地说，系统先为每一期材料写出“这一期主要在讲什么”，再圈出“不太符合主旋律但可能有意义的线索”；单期异动不会立即报警，只有后续时期出现能接续同一故事线的新证据时，早期异动才被回溯性确认为先兆。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 读取并文本化当前DTKG快照

系统从DTKG记忆读取当前快照，把每个事实按带索引的“主体名称与类型$\longrightarrow$关系及有效期$\longrightarrow$客体名称与类型”格式转成文本，并整体提供给LLM。观测时间$t$与事实自身的有效期$(t_{start},t_{end})$被分别保留。

<div class="method-step__io" markdown="1">

**输入**：观测时刻$t$的快照$\mathcal{G}_s^t=(\mathcal{E}^t,\mathcal{R}^t,\mathcal{T}_{start}^t,\mathcal{T}_{end}^t,\mathcal{F}^t)$，其中$\mathcal{F}^t$包含带实体类型和有效期的事实五元组。<br>
**输出**：可由LLM读取的当前快照五元组列表，以及每条事实对应的索引、实体类型、关系类型和时间边界。

</div>

**直观理解**：这一步相当于把机器中的图结构翻译成一份结构化事件清单，同时区分“系统何时看到它”和“这件事在现实中何时有效”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立主导叙事并抽取稀有子图

模块1采用两步CoT：先概括快照的主导叙事，再逐条比较五元组与该叙事，识别内容上存在张力的集合$\mathcal{S}^t\subseteq\mathcal{F}^t$。仅由标签不一致等TKG构建伪影造成、而语义仍符合主叙事的偏差会被明确排除。

<div class="method-step__io" markdown="1">

**输入**：当前快照的完整文本化五元组列表。<br>
**输出**：一个或多个当前时刻的稀有子图$\mathcal{S}^t$；若不存在可信偏离，则稀有子图集合为空。

</div>

**直观理解**：系统不是简单寻找低频词，而是先理解本期材料的共同主题，再找“与整体走向不一致但语义上说得通”的事实。这样可把真正的新动向与数据清洗问题区分开。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造并保存连接子图

在快照的实体级邻接图上用广度优先搜索计算$\mathcal{E}(\mathcal{S}^t)$中每对实体之间的最短路径，并取这些路径的并集形成$\mathcal{C}^t$。系统仅保留稀有五元组及连接它们所需的结构上下文，丢弃快照的其余部分，并将结果作为历史证据写入记忆。

<div class="method-step__io" markdown="1">

**输入**：稀有子图$\mathcal{S}^t$、其中出现的实体集合$\mathcal{E}(\mathcal{S}^t)$以及完整快照$\mathcal{G}_s^t$。<br>
**输出**：当前连接子图$\mathcal{C}^t$及其中被突出标记的稀有五元组；若没有稀有子图，则$\mathcal{C}^t$为空。

</div>

**直观理解**：孤立异常往往难以解释，因此系统补上连接异常实体的最短“关系链”。它像从一张大地图中裁出异常地点及其必要道路，既保留来龙去脉，又减少无关信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 跨快照核验并触发弱信号

模块2先让LLM分别说明每个历史连接子图的主要内容及其稀有五元组所暗示的方向，再把$\mathcal{C}^t$中的每个五元组与这些历史暗示比较。若当前内容延续并推进某个较早张力，系统便把对应子图标注为弱信号；已匹配的弱信号及相关连接子图在下一时刻不再输入模型。

<div class="method-step__io" markdown="1">

**输入**：当前连接子图$\mathcal{C}^t$以及DTKG记忆中的所有先前连接子图$\{\mathcal{C}^{t'}:t'<t\}$；若$\mathcal{C}^t$为空则跳过此步。<br>
**输出**：带自然语言跨期解释的弱信号子图，以及写回DTKG记忆的弱信号标注；未获得后续印证的当前偏离仍只作为候选证据。

</div>

**直观理解**：一次反常可能只是噪声，所以系统会等待后续证据。若后来事实沿着同一矛盾方向发展，早先线索才会被认定为前兆，而已报警故事线会从待检队列移除以防重复。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 动态时间知识图谱快照定义

$$
\mathcal{G}_{s}^{t}=\left(\mathcal{E}^{t},\,\mathcal{R}^{t},\,\mathcal{T}_{start}^{t},\,\mathcal{T}_{end}^{t},\,\mathcal{F}^{t}\right),\qquad \mathcal{F}^{t}\ni(e_s,r,e_o,t_{start},t_{end})
$$

**符号说明**

- $\mathcal{G}_{s}^{t}$：观测时刻$t$的时间知识图谱快照。
- $t$：系统获得或观察该快照的时间，属于有序观测时间集合。
- $\mathcal{E}^{t}$：快照$t$中的带类型实体集合。
- $\mathcal{R}^{t}$：快照$t$中的带类型关系集合。
- $\mathcal{T}_{start}^{t}$：快照中事实可使用的有效期起点集合。
- $\mathcal{T}_{end}^{t}$：快照中事实可使用的有效期终点集合。
- $\mathcal{F}^{t}$：快照$t$中的事实五元组集合。
- $e_s$：事实的主体实体，属于$\mathcal{E}^{t}$。
- $r$：主体与客体之间的类型化关系，属于$\mathcal{R}^{t}$。
- $e_o$：事实的客体实体，属于$\mathcal{E}^{t}$。
- $t_{start}$：该事实自身有效期的起点；底层事实无明确时间边界时可以未定义。
- $t_{end}$：该事实自身有效期的终点；底层事实无明确时间边界时可以未定义。

<div class="equation-explanation" markdown="1">

**直观理解**：该定义把“何时观察到事实”与“事实描述的关系何时有效”分开。例如系统可能在较晚的观测时刻$t$读到一条有效期更早的事实；这种双时间表示可防止把知识进入系统的时间误当成事件发生时间。<br>
**原文位置**：第3.1节“Dynamic Temporal Knowledge Graph”

</div>

</div>

<div class="equation-block" markdown="1">

#### 稀有子图、连接子图与弱信号的判定关系

$$
\mathcal{S}^{t}\subseteq\mathcal{F}^{t},\qquad \mathcal{C}^{t}=\bigcup_{\{u,v\}\subseteq\mathcal{E}(\mathcal{S}^{t})}\operatorname{SP}_{\mathcal{G}_{s}^{t}}(u,v),\qquad \operatorname{WeakSignal}(\mathcal{S}^{t})\iff \operatorname{Rare}(\mathcal{S}^{t},\mathcal{G}_{s}^{t})\land\exists t'<t:\operatorname{Advance}(\mathcal{S}^{t},\mathcal{S}^{t'})
$$

**符号说明**

- $\mathcal{S}^{t}$：时刻$t$从当前事实集合中抽出的稀有子图，其内容与当前快照的主导叙事存在张力。
- $\mathcal{E}(\mathcal{S}^{t})$：稀有子图$\mathcal{S}^{t}$涉及的实体集合。
- $\mathcal{C}^{t}$：连接稀有实体的结构上下文，即所有实体对最短路径的并集。
- $\operatorname{SP}_{\mathcal{G}_{s}^{t}}(u,v)$：在快照$\mathcal{G}_{s}^{t}$的实体级邻接结构中，由广度优先搜索得到的实体$u$与$v$之间的最短路径。
- $\operatorname{Rare}(\mathcal{S}^{t},\mathcal{G}_{s}^{t})$：表示$\mathcal{S}^{t}$相对当前快照主导叙事是稀有且语义连贯的；这是LLM作出的语义判断，不是论文给出的数值函数。
- $t'$：早于当前时刻$t$的历史观测时刻。
- $\operatorname{Advance}(\mathcal{S}^{t},\mathcal{S}^{t'})$：表示当前子图内容延续并推进了历史稀有子图中已经出现的张力；这是对论文文字判据的逻辑记述。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分规定候选线索必须来自当前事实；第二部分用最短路径补齐这些线索之间的关系背景；第三部分表达核心判据：当前稀有还不够，必须存在更早的同线程张力并被当前证据推进。最后一个双条件是对原文定义的忠实逻辑化表达，并非作者提出的可微损失函数。<br>
**原文位置**：第3.1节“Rare Subgraph”“Connecting Subgraph”和“Weak Signal”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。原文所述C-Unseen没有训练专用模型、参数优化目标或可微损失函数；其关键决策由预训练LLM在提示中执行两步CoT推理，并结合确定性的最短路径搜索与DTKG记忆更新完成。因此，稀有性和跨期“推进张力”是语义判据，而不是通过标注数据拟合的数值评分函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 稀有子图抽取器（Rare Subgraphs Extractor）**

该模块对当前快照执行“主导叙事$\rightarrow$偏离判断”的两步CoT，将稀有性定义为相对当前语境的语义张力，而非单纯的出现频率。抽取后，它通过广度优先搜索得到稀有实体两两最短路径的并集$\mathcal{C}^t$，从而把语义偏离与图中的关系结构结合起来。

> 直观理解：它解决“什么算异常”和“异常之间如何相关”两个问题：LLM负责理解语义，最短路径负责提供可核查的关系上下文。相比把完整图直接交给模型，选择性保留异常及必要路径能减少主流事实对微弱线索的淹没。

**2. 弱信号告警器（Weak Signal Alerter）**

该模块不把单个$\mathcal{C}^t$直接视作弱信号，而是检索所有较早连接子图并执行两步CoT：先总结历史子图及其暗示，再判断当前五元组是否延续同一线程。判定条件强调“推进既有张力”，因此只共享实体或主题、却没有语义发展关系的子图不应自动匹配。

> 直观理解：该模块相当于时间上的复核员：早期异常先进入观察名单，后期出现连贯证据时才报警。它用跨期印证降低对偶发噪声的误判，并以历史到当前的自然语言解释说明报警依据。

**3. DTKG记忆与状态更新**

DTKG不仅存储五元组，还承载可更新属性，包括稀有子图、连接子图和弱信号标注。每个时刻完成检测后，新证据被写回；已确认为同一弱信号的子图及其关联历史证据在下一轮被丢弃，不再重复展示给LLM。

> 直观理解：记忆机制让模型无需每次从头阅读全部历史，同时保存跨期判断所需的证据链。消费掉已经报警的线索，则使系统关注尚未解决的新故事线。

**训练与推理**

该框架是逐快照的推理流程，而非训练流程。初始化时，DTKG按有序观测时间保存快照$\{\mathcal{G}_s^t\}_{t\in\mathcal{T}_{obs}}$；到达时刻$t$后，系统文本化$\mathcal{F}^t$并运行模块1，得到$\mathcal{S}^t$和$\mathcal{C}^t$。若$\mathcal{C}^t$为空，当期告警模块被跳过；否则，系统取回当前及全部历史连接子图，运行模块2的“解释历史暗示$\rightarrow$比较当前延续性”推理。被认定为弱信号的子图连同解释和标注写回记忆，已完成匹配的弱信号及相关连接子图在下一时刻从提示上下文中移除；随后对下一个快照重复同样过程。

**复现信息**

公平复现所必需的设计包括：保留实体与关系类型，并以五元组$(e_s,r,e_o,t_{start},t_{end})$呈现事实；区分观测时间$t$和事实有效期，其中有效期可缺失；模块1必须使用“先总结主导叙事、再检测偏离”的两步提示，并排除标签错配等图谱伪影；连接子图须在实体级邻接上以广度优先搜索求稀有实体两两最短路径并取并集；模块2必须访问历史连接子图而非仅访问当前快照，并采用“先解释历史暗示、再判断当前推进”的两步提示。所给方法章节未明确报告具体LLM型号、解码参数、提示全文、上下文截断策略或最短路径多解时的选择规则，这些项目不能从当前材料补写，复现时仍需核查论文其余章节或代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Wiki-OpenAI：作者为弱信号检测构建的企业领域基准。数据来自OpenAI维基百科页面在2015年1月至2025年12月间的全部月度编辑，并使用ATOM抽取原子事实。事实按源事件年份归入2015—2025年的11个DTKG时间快照；去重后有757条维基百科事实，另补充16条来自《纽约时报》等成熟新闻媒体的事实，共773条。基准标注了5个最终成为强信号的事件，并为每个信号给出弱信号最早出现时间$t_s^{\mathrm{weak}}$与强信号形成时间$t_s^{\mathrm{strong}}$。该数据集同时承担检测准确率、提前量和解释性评估；原文未明确报告训练集、验证集与测试集划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Precision、Recall与$F_1$**

检测结果$(\hat{s},t)$只有同时满足两项条件才算真阳性：描述$\hat{s}$与某个真实信号$s$的锚词集合$\mathcal{A}(s)$至少共享$k$个不同词，且检测时间$t$落在窗口$\mathcal{W}_s=[t_s^{\mathrm{weak}},t_s^{\mathrm{strong}}]$内。作者分别在$k\in\{1,2,3\}$下评估；$k$越大，匹配越严格。Precision衡量所有输出中正确检测的比例，Recall衡量5个真实强信号中有多少至少被及时命中一次，$F_1$是二者的调和平均。需要注意，输出总数$|\mathcal{D}_M|$不随$k$变化，因此严格度提高只会减少可计为真阳性的检测。 （越高越好；Precision高表示误报较少，Recall高表示漏报较少，$F_1$高表示二者平衡较好。）

</div>
<div class="metric-item" markdown="1">

**Mean Lead Time**

对已被方法$M$正确识别的信号$s$，提前量定义为$\mathrm{LeadTime}_M(s,k)=t_s^{\mathrm{strong}}-t_{M,s}^{\mathrm{det}}(k)$，即强信号形成时间减去最早有效检测时间；随后仅在被成功检测的信号集合$\mathcal{S}_M^+(k)$上求均值，并同时查看逐信号分布。该指标补充了准确率，因为临近强信号形成才发出的正确警报，实际预警价值可能很低。 （越高越好，表示在强信号正式确立前更早发出警报；但该均值只覆盖成功检测的信号，必须结合Recall解读，以免漏掉大量信号的方法因少数早期命中而显得优秀。）

</div>
<div class="metric-item" markdown="1">

**Interpretability qualitative comparison**

在同一事件上并列比较各方法的输出形式：关键词、主题词袋、graphlet实体集合，以及C-Unseen的类型化五元组和自然语言解释。它检验输出能否说明弱信号涉及哪些实体、关系和时间背景，而不只是给出难以追溯的词项。 （没有数值化方向；解释越能由具体上下文和图事实支撑、越便于人工核查越好。所给章节未报告人工评分量表、评审人数或一致性指标。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### C-Unseen与关键词、主题及图方法的总体比较

<div class="result-value" markdown="1">

作者声称C-Unseen优于三类基线，但所给实验章节没有提供对应分数、表格、逐严格度结果或统计检验，因而无法量化优势大小，也无法确认优势主要来自Precision、Recall、$F_1$还是提前量。

</div>

这项结论支持“结合语义关系、稀有子图与跨时间持续性可能比单纯词频、主题词或无类型拓扑更有效”的作者主张。然而，在缺少结果表的情况下，它不能证明改进幅度、跨严格度稳定性或统计显著性，也不能排除人工补充事实和锚词匹配规则对C-Unseen更有利的可能性。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Experimental results demonstrate that C-Unseen outperforms keyword-, topic-, and graph-based baselines.

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

- 关键词方法：以单个关键词作为检测输出，用于检验仅依赖词频或词项突增、而不显式建模语义关系的方法能否捕获早期信号。所给章节未列出具体算法名称和参数。
- 主题方法：输出一组主题词，用于比较基于主题建模的语义聚合与C-Unseen关系化、类型化子图表示之间的差异。所给章节未列出具体主题模型名称。
- 图方法：从无类型图结构或graphlet中收集实体作为检测结果，用于判断仅利用拓扑模式、但缺少关系类型和自然语言解释的方案是否足够。所给章节未列出具体图基线名称。

**实验想回答的问题**

- RQ1/RQ2：与关键词、主题和图结构方法相比，C-Unseen能否更准确地识别弱信号，并在信号正式成为强信号之前提供更长的预警时间？
- RQ3/RQ4：C-Unseen生成的解释是否具有上下文依据和可理解性，以及框架中的哪些组件带来了检测性能？

**实验实现**

评估以5个已确立的强信号为参照。每个真实信号$s$具有检测窗口$\mathcal{W}_s$和由先兆事实提取的区分性锚词集合$\mathcal{A}(s)$；各方法产生检测集合$\mathcal{D}_M=\{(\hat{s},t)\}$。统一评测器通过锚词重合数处理不同输出粒度，并在$k=1,2,3$三种严格度下判断是否命中。若同一信号被多次命中，Recall只按该信号至少成功一次计算，提前量则采用最早的有效检测时间。数据方面，由于维基百科无法完整记录现实中的全部先兆历史，作者人工补入16条有新闻来源的原子事实。所给章节没有报告模型版本、提示模板、解码设置、随机种子、运行次数、显著性检验或计算成本，因此无法据此判断结果对LLM采样和提示变化是否稳健。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Uses chain-of-thought LLM reasoning to identify semantically rare subgraphs in dynamic temporal knowledge graphs for weak-signal detection.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`137037b2d7fa5e0c75cf55dfe193369dd2a902f160b8d9b75d4547bcda299ba1`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
