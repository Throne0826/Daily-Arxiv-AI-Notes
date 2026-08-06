---
title: "[论文解读] D$^2$F-ReAG: Dynamic Decomposition and Filtering for Multi-Hop Reasoning-Augmented Generation"
description: "[arXiv 2608.04444][LLM Reasoning] 本文针对多跳问答中固定分解与噪声累积的问题，提出依据当前推理可靠性按需分解问题、筛选可信子问题推理并回传修正根问题推理的框架。"
arxiv_id: "2608.04444"
announcement_date: "2026-08-06"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:59:57.884404+00:00"
source_sha256: "9a155165375d9dc81c9b96faae3d995d730d25785d6fd2751a50c487a2e0edc3"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "检索增强生成"
  - "多跳推理"
  - "动态问题分解"
  - "推理可靠性"
  - "证据过滤"
  - "跨文档问答"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.04444</p>

# D$^2$F-ReAG: Dynamic Decomposition and Filtering for Multi-Hop Reasoning-Augmented Generation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Jiaoyang Li, Junhao Ruan, Shengwei Tang, Kaiyan Chang, Zhengtao Yu, Tong Xiao, Jingbo Zhu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Northeastern University, Shenyang, China；Kunming University of Science and Technology, Kunming, China；NiuTrans Research, Shenyang, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04444v1) · [PDF 下载](https://arxiv.org/pdf/2608.04444v1) · **关键词** 检索增强生成, 多跳推理, 动态问题分解, 推理可靠性, 证据过滤, 跨文档问答<br>


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

本文针对多跳问答中固定分解与噪声累积的问题，提出依据当前推理可靠性按需分解问题、筛选可信子问题推理并回传修正根问题推理的框架。

**不用术语来说**：回答复杂问题时，所需事实往往分散在多篇文档中，模型必须先解决若干相互依赖的小问题，再把证据连接起来；但现有系统可能不分难易地执行固定轮数的拆解，也可能把错误或无关信息带入后续步骤，造成计算浪费并使早期错误逐步放大。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出以推理可靠性为控制信号的按需分解机制：根问题推理足够可靠时直接作答，否则继续生成逻辑子问题，并在根问题可可靠回答后提前停止，从而使分解深度适应问题难度。
- 提出可信推理回传与过滤机制：仅将置信度充分且与原问题相关的子问题推理路径向上传播，用其迭代更新和纠正根问题推理，以减少有用中间结论在有损压缩中丢失以及错误跨步骤累积。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于知识密集型问答中的检索增强生成与多跳推理研究。大语言模型的参数知识可能过时，并可能生成缺乏证据支持的内容；检索增强生成通过在回答时引入外部文档来改善事实性，但常规的一次检索更适合证据集中于单篇文档的简单问题。多跳问题则要求模型把分散在不同文档中的若干事实按逻辑顺序连接起来，例如先确定一个中间实体，再利用该实体检索最终答案。现有方案主要采用预构建知识图进行跨文档遍历，或将复杂问题拆成子问题并迭代检索；前者存在图结构不完整、构建维护成本高和知识更新困难等问题，后者可能因固定粒度的分解及迭代中的噪声累积而降低准确性与效率。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**检索增强生成（RAG）**

RAG先从外部语料中检索与问题相关的证据，再让语言模型结合问题和证据生成答案，从而减少仅依赖模型内部参数知识造成的事实错误。本文关注的难点不是单次检索本身，而是如何在多轮推理中持续获得并正确利用跨文档证据。

</div>
<div class="concept-item" markdown="1">

**多跳推理**

多跳推理是指答案不能由单条证据直接得到，而必须经过两个或更多相互依赖的推理步骤，把不同文档中的事实连接起来。前一步得到的中间结论通常会决定后一步需要检索什么，因此中间错误可能沿推理链传播。

</div>
<div class="concept-item" markdown="1">

**问题分解**

问题分解把一个复杂问题改写为若干更容易检索和回答的子问题，并将子问题结论组合为最终答案。分解过深会产生冗余检索和计算，分解不足则无法显式解决必要的中间关系，因此分解深度需要适应问题难度。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是一个需要跨文档证据才能回答的多跳问题，以及可供检索的外部知识源；系统输出是由检索证据支持的最终答案。基本设定是：证据可能散布于多篇文档，根问题的初始推理可能可靠也可能包含错误，而且复杂度因问题而异。本文据此把关键决策定义为是否继续分解当前问题：若根层推理已足够可靠，则直接回答并提前停止；若不可靠，则生成逻辑相关的子问题，检索并验证其推理结果，再把可靠且相关的子问题推理路径向上传递，用于修正根问题推理。该设定不要求预先构建知识图，但依赖模型能够评估当前推理的可靠性与子问题结果的相关性；节选未给出这些判断的形式化阈值或概率假设。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathrm{RAG}$**

检索增强生成，即结合外部知识检索与语言模型生成的问答范式。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{D^2F\text{-}ReAG}$**

本文提出的动态分解与过滤多跳推理增强生成框架。

</div>

</div>

**直接相关的工作**

- **GraphRAG**: 代表基于图结构的多跳检索路线：通过局部与全局查询进行层次化社区搜索，使系统能沿知识单元之间的连接寻找跨文档证据。它说明结构化关系有助于多跳推理，但本文指出预构建图可能不完整，且在大规模或知识频繁更新时构建与维护成本较高，因此本文转向无需显式预构建图的动态分解方案。
- **LogicRAG**: 与本文最直接相关的问题分解方法：它把复杂查询拆成逻辑子问题，并将多轮检索证据压缩到文档级记忆中，以支持无显式知识图的多跳推理。本文认为其不足在于压缩不能彻底过滤冗余或错误内容，噪声可能迭代累积；同时分解粒度较固定，可能对简单问题过度分解、对复杂问题分解不足，因而留下了按当前推理可靠性动态控制分解深度并验证中间推理的研究空缺。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型依赖可能过时的参数知识，容易产生缺乏事实支持的答案；常规检索增强生成虽然能引入外部知识，但多跳问题的证据通常分散在不同文档中，需要跨文档组合多个中间结论。若系统无法控制推理展开程度并判断中间信息是否可信，就会同时面临答案不可靠和计算成本偏高的问题。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于图的检索增强生成（Graph RAG）**：预先把事实及其关系组织成图结构，回答问题时沿相互连接的知识单元遍历和检索，从而取得跨文档、多跳证据。
- **问题分解与迭代记忆方法（以 LogicRAG 为例）**：将复杂查询拆成子问题，逐步检索相关材料，并把每轮证据压缩进文档级记忆；后续步骤依赖该记忆继续检索和推理，无需显式构建知识图。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 预构建知识图难以覆盖全部相关关系，且大规模构建和维护成本高；当知识频繁更新时，图容易过时或不完整，进而限制多跳证据遍历的有效性。
- 迭代记忆的压缩不能充分排除冗余或错误内容，噪声会随轮次累积并误导后续推理；同时，固定或僵化的分解粒度会让简单问题被过度拆分、复杂问题又拆分不足，因而同时损害效率与准确性。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有无图多跳方法尚缺少一个统一的闭环控制机制，能够根据当前推理是否可靠来决定要不要继续分解，并在利用中间结果前同时验证其可信度与相关性，再将有效推理完整地反馈给根问题，而非仅保留可能有损的压缩记忆。

</div>
<div markdown="1"><span>核心问题</span>

能否以当前推理可靠性作为动态控制信号，自适应决定多跳问题的分解深度和停止时机，并通过筛选、回传可信子问题推理来纠正根问题推理，从而减少错误传播与不必要计算？

</div>
<div markdown="1"><span>作者直觉</span>

可以把整个过程理解为有条件展开的推理树：先尝试直接解决根问题，只有当这次推理不可信时才向下拆分；子问题得到可靠且相关的结论后，不只留下简短摘要，而是把经过验证的推理依据送回上层。这样，容易的问题走短路径，困难的问题获得更多推理步骤，而可疑的中间信息不会轻易成为后续推理的基础。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

D2F-ReAG 是一个面向多跳问答的动态推理增强生成框架。输入为根问题 $q_{root}$ 和文档语料库 $\mathcal{C}$；系统先检索与问题最相关的前 $k$ 篇文档 $D(q_{root})$，据此生成根推理 $r(q_{root})$，再由一个基于大语言模型的评判器给出可靠性分数 $s_r(q_{root})\in[0,10]$。若分数高于阈值 $\theta$，系统直接从已验证的根推理产生答案；否则，它把当前问题分解为更小的子问题，逐个执行检索、推理与可靠性判断，并利用已经验证的中间结论改写后续相关子问题。可靠且与根问题相关的子推理会被合并回根推理，随后重新判断根推理，直到其分数超过阈值并提前停止。

该方法的核心不是无条件构造一条很长的推理链，而是先尝试用一次检索解决问题，只在证据或逻辑不足时增加推理深度。通俗地说，它像一名先尝试直接作答、再检查解题过程的学生：简单题通过检查后立即交卷；复杂题才拆成若干小题，并且只把经过核验、确实有助于原题的解题结果写回总答案，从而兼顾准确性、检索针对性和计算成本。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 检索与根推理生成

稠密检索器从 $\mathcal{C}$ 中选取与 $q_{root}$ 最相关的前 $k$ 篇文档，组成 $D(q_{root})$；生成器以问题和文档为条件产生详细根推理 $r(q_{root})=\mathrm{Generator}(q_{root},D(q_{root}))$。检索证据用于约束推理，使模型更多依赖外部事实而非仅依赖参数记忆。

<div class="method-step__io" markdown="1">

**输入**：根问题 $q_{root}$ 与外部语料库 $\mathcal{C}$。<br>
**输出**：带有检索证据支持的初始根推理 $r(q_{root})$。

</div>

**直观理解**：系统先查资料再写解题过程。这里生成的不是最终答案，而是一份随后需要检查的候选推理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 可靠性评判与动态路由

基于大语言模型的评判器按照证据支撑、逻辑一致性和答案完整性等维度计算 $s_r(q)$，并与阈值 $\theta$ 比较。实验中设置 $\theta=7$；只有满足 $s_r(q)>\theta$ 的推理才被视为可靠，否则进入分解流程。

<div class="method-step__io" markdown="1">

**输入**：当前问题 $q$ 及其推理 $r(q)$，其中 $q$ 可以是根问题或任一子问题。<br>
**输出**：“已解决”或“需要分解”的路由结果，以及可供后续过滤使用的可靠性分数 $s_r(q)$。

</div>

**直观理解**：这一步相当于检查解题过程是否有证据、是否自洽、是否足以回答问题。阈值控制系统何时停止，也决定哪些问题值得投入额外计算。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 递归分解与上下文改写

系统通过提示工程执行 $sub(q)=\mathrm{Decompose}(q)$，把问题拆成聚焦单个推理跳或较窄信息需求的子问题，并按顺序解决。某个子问题可靠解决后，系统以其推理 $r_q$ 改写相关的待处理子问题集合 $\mathcal{S}_i$，得到 $\mathcal{S}'_i=\{\mathrm{Rewrite}(q,r_q)\mid q\in\mathcal{S}_i\}$，再对改写后的问题进行下一轮检索与生成。

<div class="method-step__io" markdown="1">

**输入**：未通过可靠性阈值的当前问题 $q$，以及此前已可靠解决的子问题推理。<br>
**输出**：更明确、可独立检索的子问题，以及每个子问题对应的候选推理和可靠性判断。

</div>

**直观理解**：复杂问题被拆成依赖关系更清楚的小问题；前面已经确认的答案还会补进后续问题，消除代词、缺失实体或模糊条件。这样后续检索更像搜索具体事实，而不是用含糊问题反复碰运气。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 相关性过滤、根推理更新与终止

系统先用 $\mathrm{Check}(q_i,q_{root})$ 判断子问题是否与根问题相关；仅当子推理同时可靠且相关时，才通过 $\mathrm{Update}$ 将其整合进根推理。更新后的根推理再次接受可靠性评判，一旦分数超过 $\theta$，系统停止处理剩余子问题并由 $\mathrm{Answer}$ 生成最终答案。

<div class="method-step__io" markdown="1">

**输入**：可靠子推理 $r(q_i)$、子问题 $q_i$、根问题 $q_{root}$ 和当前根推理 $r(q_{root})$。<br>
**输出**：逐步增强的根推理 $r'(q_{root})$，以及达到可靠性条件后生成的最终答案 $a_{root}$。

</div>

**直观理解**：不是所有小题结果都写入总解答：系统会丢弃跑题内容，只保留可信且有用的信息。根推理一旦已经足够好就提前结束，以减少过度分解带来的时间、令牌消耗和噪声。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 可靠性评分与动态分解判定

$$
\begin{aligned}
s_r(q)&=\operatorname{Score}(q,r(q)),\\
\operatorname{Judge}(q)&=\begin{cases}
\text{Solved},&\text{if }s_r(q)>\theta,\\
\text{Decompose},&\text{if }s_r(q)\leq\theta.
\end{cases}
\end{aligned}
$$

**符号说明**

- $q$：当前接受判断的问题，可以是根问题或某个子问题。
- $r(q)$：生成器依据问题及其检索文档得到的推理过程。
- $s_r(q)$：推理可靠性分数，取值范围为零到十，数值越高表示越可靠。
- $\operatorname{Score}$：基于大语言模型的评分函数，按照预定义规则综合考察证据支撑、逻辑一致性和答案完整性。
- $\theta$：可靠性判定阈值；论文实验中设为七，并采用严格大于关系判定已解决。
- $\operatorname{Judge}(q)$：动态控制结果，决定当前问题终止还是继续分解。

<div class="equation-explanation" markdown="1">

**直观理解**：该式是动态推理深度的控制核心：系统先评价当前推理，而不是预先规定所有问题必须执行相同数量的步骤。分数超过阈值时停止扩展；否则将问题拆小并继续检索，因此额外计算主要用于当前证据和推理确实不足的问题。<br>
**原文位置**：第 3.2 节，公式（2）和公式（3）

</div>

</div>

<div class="equation-block" markdown="1">

#### 可靠子推理增强根推理

$$
r^{\prime}(q_{root})=\operatorname{Update}\bigl(r(q_{root}),r(q_i)\bigr)
$$

**符号说明**

- $q_{root}$：用户最初提出、最终需要回答的根问题。
- $q_i$：由根问题或其他未解决问题分解得到的第 i 个子问题。
- $r(q_{root})$：更新前的根问题推理。
- $r(q_i)$：已经通过可靠性判断且经相关性检查确认有助于根问题的子问题推理。
- $\operatorname{Update}$：将新验证的证据和中间结论整合进现有根推理的操作。
- $r^{\prime}(q_{root})$：吸收可靠且相关的子推理之后得到的新版根推理。

<div class="equation-explanation" markdown="1">

**直观理解**：该式描述 ReAG 的信息回流：子问题不是单独回答后即被丢弃，而是把经过验证的中间结论补充到原问题的推理中。更新后再次评分，使系统形成“发现缺口、拆分求解、回填证据、重新检查”的闭环；原文同时明确，只有通过相关性检查的子推理才执行该更新。<br>
**原文位置**：第 3.4 节，公式（8）；相关性前置条件见公式（7）及其后文字

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。所给方法章节没有提出新的参数训练损失、监督目标或端到端优化过程；D2F-ReAG 是一个以提示工程、检索、生成、评分、改写和状态更新组成的推理时框架。文中的 $\mathrm{Score}$、$\mathrm{Decompose}$、$\mathrm{Rewrite}$、$\mathrm{Check}$ 与 $\mathrm{Update}$ 表示由模型执行的推理操作或控制函数，而不是用于反向传播的可微目标，因此不能把可靠性分数误解为训练奖励或损失函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 基于证据的检索生成模块**

该模块对根问题和每个子问题统一执行“稠密检索加条件生成”：对任意 $q\in\{q_{root},q_1,\ldots,q_n\}$，先从 $\mathcal{C}$ 检索 $D(q)$，再由生成器产生 $r(q)$。因此，根层和子问题层共享同一种证据获取与推理接口，区别只在于问题粒度及其所处的递归阶段。

> 直观理解：多跳问题失败的一个原因是单次检索难以同时命中分散在不同文档中的全部事实。把大问题拆小后重新检索，可以让每次搜索只负责寻找一个较明确的中间事实。

**2. 可靠性驱动的动态分解模块**

评判器并不把生成的推理默认视为正确，而是输出 $s_r(q)$ 并通过阈值 $\theta$ 决定停止或继续分解。该控制同时作用于根问题和子问题：简单根问题可直接结束，困难问题才增加深度，而不可靠的子推理不会直接参与根推理更新。

> 直观理解：固定分解会让简单问题也经历昂贵的多步流程，还可能引入额外错误；完全不分解又难以处理真正需要跨文档连接证据的问题。动态门控的作用是在两者之间按题目难度分配计算。

**3. 改写与双重过滤的 ReAG 模块**

ReAG 即推理增强生成。系统先以已验证推理改写相关待处理子问题，再通过“可靠性”和“与根问题的相关性”两道条件筛选中间推理，最后利用 $\mathrm{Update}(r(q_{root}),r(q_i))$ 更新全局推理状态，并重新评估根推理是否足以作答。

> 直观理解：改写负责把已经查明的信息传给下一步，过滤负责阻止错误或跑题内容进入总解答。两者结合后，根推理得到的是经过核验的中间结论，而不是所有子问题输出的简单拼接。

**训练与推理**

原文未描述专门训练阶段，完整流程应理解为推理时编排。给定 $q_{root}$，系统检索 $D(q_{root})$ 并生成 $r(q_{root})$；随后计算 $s_r(q_{root})$。若 $s_r(q_{root})>\theta$，则直接执行 $a_{root}=\mathrm{Answer}(r(q_{root}))$；否则，对未解决问题执行 $sub(q)=\mathrm{Decompose}(q)$，按顺序处理其子问题。每个子问题都重复检索、生成和可靠性判断；可靠解决后，其推理用于改写相关的后续子问题，以便把已确认的实体或条件带入下一轮检索。

对子问题推理，系统先检查其与 $q_{root}$ 的相关性；只有同时满足可靠和相关两个条件的 $r(q_i)$ 才被合并进 $r(q_{root})$。每次更新后重新评估根推理，一旦其分数超过 $\theta$，便跳过剩余子问题并生成答案。若当前子问题仍不可靠，则继续对它进行逻辑分解，因而形成按需递归的求解过程；不过，所给章节没有明确报告最大递归深度、循环次数上限、无法达到阈值时的回退策略或并列子问题的具体调度细则。

**复现信息**

公平复现所必需且原文明确给出的设置包括：使用稠密检索器从语料库 $\mathcal{C}$ 返回前 $k$ 篇相关文档；生成器同时接收问题 $q$ 与其证据集合 $D(q)$；可靠性分数范围为 $[0,10]$；阈值设为 $\theta=7$，并且停止条件是严格的 $s_r(q)>\theta$，所以得分恰为七仍需分解。评判规则综合考察证据支撑、逻辑一致性和回答完整性，子问题通过提示工程进行逻辑分解与改写，并按顺序求解。

所给章节没有明确报告稠密检索器名称、$k$ 的具体取值、生成器与评判器所用模型、提示模板、评分采样设置、最大分解深度、相关性判定阈值、更新提示或答案解码参数；这些缺失会影响严格复现。作者对设计的解释是，按需分解可跳过简单问题的额外步骤，可靠性与相关性过滤可降低错误或离题推理污染根状态的风险，而根推理达标后的提前停止可避免过度推理；这些是方法设计主张，并不等同于对所有模型和数据集均成立的理论保证。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HotpotQA：标准跨文档多跳问答基准。实验从其验证集随机抽取1,000个问题，并沿用HippoRAG 2所使用的检索语料；它主要检验方法能否组合多个文档中的证据。
- 2WikiMultiHopQA：基于Wikipedia的多跳问答基准。实验从验证集随机抽取1,000个问题，使用与HippoRAG 2一致的检索语料；论文将其视为较需要深层多跳推理的场景，也是D²F-ReAG取得最大相对增益的数据集。
- MuSiQue：强调可组合、多步推理的问答基准。实验同样从验证集随机抽取1,000个问题并采用统一检索语料；它用于测试图结构或迭代检索方法在较难、多跳关系可能未被充分覆盖时的表现。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Str-Acc**

对预测答案与标准答案进行常规规范化后检查是否完全匹配，衡量严格的词面正确性。该指标会把语义正确但措辞不同的答案判为错误。 （越高越好，因为更高表示更多预测能与标准答案严格匹配。）

</div>
<div class="metric-item" markdown="1">

**LLM-Acc**

使用强LLM作为自动评审者，判断预测与参考答案是否语义等价，允许释义和表面形式差异。它补充Str-Acc，但结果也可能受自动评审模型偏差影响。 （越高越好，因为更高表示更多预测在语义上被判断为正确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 2WikiMultiHopQA上的总体准确率

<div class="result-value" markdown="1">

D²F-ReAG取得70.3的Str-Acc和68.9的LLM-Acc，两项指标均超过全部基线。

</div>

这说明在论文认为深层多跳推理需求较强的2WikiMultiHopQA上，动态决定是否分解并利用经过验证的子问题推理，既提高了与标准答案的严格匹配，也提高了语义正确性。由于各方法采用统一生成模型和检索配置，该差异更可能来自推理与检索策略；但这里只报告最佳运行结果，不能据此确认平均增益或统计显著性。

<div class="result-source" markdown="1">

来源：第4.4节 Main Results，Table 1的正文解读

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

D2F-ReAG consistently outperforms all baselines on 2Wiki (70.3 / 68.9) and MuSiQue (32.2 / 37.9), and achieves the highest LLM-Acc on HotpotQA (63.4), with the largest gains on 2WikiMultiHopQA where deep multi-hop reasoning is most needed.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### MuSiQue上的总体准确率

<div class="result-value" markdown="1">

D²F-ReAG取得32.2的Str-Acc和37.9的LLM-Acc，并在这两项指标上超过所列基线。

</div>

MuSiQue用于检验较困难的组合式多跳推理。两项指标同时领先，表明方法的优势并非仅来自输出形式更接近标准答案，也覆盖了语义层面的正确性。不过绝对准确率仍明显低于2WikiMultiHopQA，说明动态分解与过滤并未解决该数据集上的大部分问题，也不能单凭这些分数确定错误来自检索、分解还是最终生成。

<div class="result-source" markdown="1">

来源：第4.4节 Main Results，Table 1的正文解读

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

D2F-ReAG consistently outperforms all baselines on 2Wiki (70.3 / 68.9) and MuSiQue (32.2 / 37.9), and achieves the highest LLM-Acc on HotpotQA (63.4), with the largest gains on 2WikiMultiHopQA where deep multi-hop reasoning is most needed.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 与最强提示式基线LogicRAG的比较

<div class="result-value" markdown="1">

在2WikiMultiHopQA上，D²F-ReAG相对LogicRAG最多提高5.4个百分点Str-Acc和6.4个百分点LLM-Acc；此外，其HotpotQA LLM-Acc达到63.4，而正文给出的最佳基线LogicRAG为62.5。

</div>

与同样依赖问题分解的LogicRAG相比，这一差距更直接支持论文的核心判断：仅进行逻辑分解还不够，分解应由根推理可靠性按需触发，并应过滤或验证中间推理。HotpotQA上的LLM-Acc提升为0.9个百分点，幅度较小；且缺少方差和显著性检验，不能断言该小幅差异稳定存在。2WikiMultiHopQA上的较大提升也只是与特定基线和配置的比较，不能单独证明每个内部组件都必要。

<div class="result-source" markdown="1">

来源：第4.4节 Main Results，Table 1的正文解读

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Against the strongest prompt-based baseline LogicRAG, it yields up to 5.4-point Str-Acc and 6.4-point LLM-Acc improvements on 2Wiki, showing that on-demand decomposition and reliability-guided reasoning mitigate the over- or under-decomposition of fixed-depth methods.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 消融证据不完整：来源只给出Figure 2中“with vs. without decomposition”的若干图形文本以及Table 2标题，没有明确映射每个数值对应的数据集、指标和实验条件，也未提供完整表格行。因此不能可靠量化分解模块的独立贡献，更无法分别隔离可靠性判断、动态深度控制和过滤机制。
- 实验报告各次运行中的最佳分数，却未说明运行次数、随机种子、均值、方差、置信区间或统计显著性；同时LLM-Acc依赖自动评审模型，但节选未交代评审模型、提示词和一致性验证。这限制了结果的可复现性，也使小幅领先尤其是HotpotQA上的差异需要谨慎解释。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 零样本LLM，包括LLaMA3（8B/13B）、gpt-3.5-turbo和gpt-4o-mini：不访问外部检索语料，用于衡量语言模型仅依靠参数知识和内在推理能力所能达到的水平。
- HippoRAG 2：论文所列图结构RAG方法中的最强代表，通过预构建图结构支持多跳检索；它用于判断动态推理与过滤能否优于显式知识关联结构。
- ChainRAG：基于提示的RAG代表，采用子问题分解和句子图检索，在2WikiMultiHopQA上表现较好；与它比较可检验D²F-ReAG的动态分解是否优于预设式分解流程。
- LogicRAG：最关键的提示式RAG比较对象，通过逻辑分解交替执行推理与检索，并取得HotpotQA上最高的基线LLM-Acc；它直接对应论文希望解决的固定分解深度及迭代噪声问题。

**实验想回答的问题**

- 在统一检索器、相同检索篇章数和相同生成模型的条件下，D²F-ReAG能否在不同类型的多跳问答数据集上同时提高严格字符串正确率与语义正确率？
- 相较于零样本推理、图结构RAG和基于提示的迭代RAG，按根节点推理可靠性决定是否分解问题的动态策略，是否更适合需要跨文档、多步推理的任务？

**实验实现**

实验遵循HippoRAG 2的语料设置，从三个验证集各随机抽取1,000题。所有方法统一使用sentence-transformers/all-MiniLM-L6-v2生成稠密检索向量，将检索篇章数固定为$k=3$，并以gpt-4o-mini作为答案生成骨干模型，使比较主要反映检索和推理策略差异。实验在单张NVIDIA RTX 3090 GPU上运行。论文报告多次运行中的最佳分数，但所给章节没有说明运行次数、随机种子、方差、置信区间或显著性检验，因此结果能够支持最佳观测性能比较，却不足以判断性能提升的稳定性。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 第4.4节称附录6提供了一个案例，展示D²F-ReAG如何借助可靠的子问题推理纠正中间错误；但本次提供的来源节选不包含案例的问题、检索证据、推理轨迹或最终答案，因此无法核查纠错发生在哪一步，也无法判断该案例是否具有代表性。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces adaptive question decomposition and filtering to improve cross-document multi-hop reasoning in retrieval-augmented LLM generation.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`9a155165375d9dc81c9b96faae3d995d730d25785d6fd2751a50c487a2e0edc3`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
