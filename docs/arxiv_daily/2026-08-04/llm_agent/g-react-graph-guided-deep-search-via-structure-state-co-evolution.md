---
title: "[论文解读] G-ReAct: Graph-Guided Deep Search via Structure-State Co-Evolution"
description: "[arXiv 2608.01324][LLM Agent] G-ReAct针对长程、多跳的开放域深度搜索，将依赖自由文本历史的线性推理改造为固定拓扑查询图上的状态演化，使候选实体、已验证事实和约束满足情况能够持续参与后续搜索决策。"
arxiv_id: "2608.01324"
announcement_date: "2026-08-04"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:57:50.483436+00:00"
source_sha256: "b66d4558c00d64bef442b7913e58a38fa8ec52529b7fc4a027bb61c001035c32"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "LLM 其他"
  - "深度搜索"
  - "大语言模型智能体"
  - "图引导推理"
  - "状态演化"
  - "多跳检索"
  - "ReAct"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.01324</p>

# G-ReAct: Graph-Guided Deep Search via Structure-State Co-Evolution

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Shaoxiong Yang, Mengyuan Zhang, Shaojun Lin, Chao Li, Wei Liu, Kun Shao, Jian Luan</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> MiLM Plus, Xiaomi Inc；Huazhong University of Science and Technology；from one of the five universities in East China. A total of 43 references were included in this article, and the first reference was from neurlps 2020 and the fourth reference was from ICML 2020. Ask the name of this article</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01324v1) · [PDF 下载](https://arxiv.org/pdf/2608.01324v1) · **关键词** 深度搜索, 大语言模型智能体, 图引导推理, 状态演化, 多跳检索, ReAct<br>


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

G-ReAct针对长程、多跳的开放域深度搜索，将依赖自由文本历史的线性推理改造为固定拓扑查询图上的状态演化，使候选实体、已验证事实和约束满足情况能够持续参与后续搜索决策。

**不用术语来说**：面对答案不能通过一次检索直接获得的复杂问题，模型需要反复搜索网页、筛选候选对象、核对多个条件并拼接证据；但搜索过程一长，仅靠对话式文字记录很容易忘记先前条件、重复查找或偏离目标，因此需要一种能把“已确认什么、还缺什么、下一步该查什么”持续记录并用于决策的组织方式。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出G-ReAct，将深度搜索表述为固定拓扑查询图上的状态演化：稳定的结构层表示目标实体、关键概念及其依赖关系，动态的状态层记录候选实体、已验证事实和约束满足状态，并同时服务于训练轨迹构造与推理时搜索引导。
- 提出图与推理协同演化机制，以“检索—验证—图更新—决策引导”闭环把可靠的原子事实写回图状态，再由更新后的状态选择后续子目标和搜索方向；作者据此主张该机制可缓解冗余检索、约束丢失和推理漂移。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究面向大语言模型的开放域深度搜索：模型面对参数知识过时、事实幻觉以及问题所需信息不在上下文中的情况，需要反复调用搜索引擎或网页浏览器，逐步检索、核验并整合外部证据。与通常围绕一次或少数几次检索组织回答的检索增强生成不同，深度搜索问题往往包含多个未知实体、隐含关系、多跳依赖和模糊约束；模型不仅要使用工具，还要在较长交互过程中分解问题、规划查询、维护候选实体、核对跨步骤约束，并根据新证据调整后续搜索。本文据此把问题求解理解为固定查询图上的状态演化：图结构表达由题目约束决定的稳定逻辑骨架，节点和边上的动态状态记录候选实体、已核验事实及约束满足情况。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**深度搜索智能体（Deep Search Agent）**

一种由大语言模型驱动、能够多轮调用搜索引擎或浏览器的智能体。它在每轮中根据当前证据决定下一步检索、核验或推理操作，目标是完成无法依靠单次检索解决的开放域复杂任务。

</div>
<div class="concept-item" markdown="1">

**ReAct**

一种将“思考—行动—观察”交替组织起来的工具增强推理范式：模型先决定行动，再读取工具返回的观察并继续推理。传统 ReAct 主要把中间状态保存在自由文本历史中，因此在长轨迹中可能难以稳定维护多个候选项和约束。

</div>
<div class="concept-item" markdown="1">

**知识图谱与多跳推理**

知识图谱以实体为节点、关系为边表示结构化知识；多跳推理需要沿多个实体或关系连接逐步找到答案。本文借用图的结构表达任务依赖，但强调的不是静态知识存储，而是搜索过程中候选项、事实和约束状态的持续更新。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个开放域、网页密集型复杂问题，以及可调用的外部搜索或浏览工具；问题可能包含若干待确定实体、实体之间的依赖关系和需要同时满足的约束。求解过程假定题目可以抽取出相对稳定的任务逻辑结构，并且工具观察中能够获得可核验的原子事实；模型需在多轮交互中检索和验证证据，把可靠信息写入节点或边的状态，再依据当前图状态选择未解决子目标和下一搜索方向。最终输出是满足题目约束、具有外部证据支持的答案；训练场景还以该过程生成高质量监督微调轨迹，推理场景则直接使用图状态提供结构化指导，而不要求额外微调。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$G=(V,E)$**

任务特定的查询图；$V$ 表示目标实体或关键概念节点集合，$E$ 表示节点之间依赖关系的边集合。原文节选未给出该符号的正式定义，此处仅用通用图记号概括其文字设定。

</div>
<div class="notation-item" markdown="1">

**$V$**

查询图中的节点集合，每个节点对应问题中的目标实体或关键概念。

</div>
<div class="notation-item" markdown="1">

**$E$**

查询图中的边集合，用于表达实体、概念或子目标之间由题目约束产生的依赖关系。

</div>
<div class="notation-item" markdown="1">

**$S$**

附着于节点和边、随搜索推进而变化的图状态，可包含候选实体、已核验事实和约束满足情况。原文节选未指定正式符号，$S$ 是便于说明的概括性记号。

</div>

</div>

**直接相关的工作**

- **ReAct**: ReAct 提供通用的“thought–action–observation”工具交互范式，是现有深度搜索轨迹生成的常见基础；但其推理状态主要表现为自由文本历史，难以在长程搜索中持续保存多个候选实体、已验证事实和跨步骤约束。G-ReAct 在该交互循环之上加入显式查询图及动态状态，使后续行动同时受文本观察和结构化约束指导。
- **GraphRAG**: GraphRAG 使用图结构组织实体关联，以改善信息组织、检索和推理，体现了图结构对检索增强的价值。本文与其关键区别在于图的角色：相关工作主要把图作为静态知识资源或离线组织工具，G-ReAct 则在实际求解期间维护不断演化的图状态，并用该状态支持下一步搜索决策。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

开放域真实任务受到模型参数知识过时、事实幻觉以及外部信息利用不可靠等问题限制。深度搜索代理虽可调用搜索引擎和浏览器，但复杂任务通常包含多跳依赖、多个未知实体、隐含关系和模糊约束，要求模型在多轮交互中持续完成问题分解、规划、探索、证据验证、候选管理和信息整合，并在较长推理链上保持所有约束一致。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **检索增强生成与工具增强的深度搜索代理**：检索增强生成通常检索外部材料后据此生成答案；更复杂的深度搜索代理则让大语言模型调用搜索引擎或浏览器，通过多轮规划、检索、验证和推理逐步补齐信息。后者能够处理动态开放环境，但需要模型自行维护跨轮次的搜索进度与约束。
- **基于知识图谱出题与ReAct式轨迹生成**：已有工作利用知识图谱构造具有多跳依赖、歧义约束和可验证答案的困难问答，再由强推理模型按ReAct的“思考—行动—观察”模式生成工具交互轨迹，并通过答案校验、格式过滤和过程级验证筛选训练数据。知识图谱主要保证题目具有清晰的潜在推理路径，而实际求解状态仍主要保存在自由文本历史中。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 自由文本式ReAct历史缺少显式、持久的状态表示。长程搜索中，模型必须同时记住多个未知实体、候选集合、跨步骤约束、已验证事实和未完成子目标，信息容易在不断增长的上下文中被稀释，进而造成重复检索、约束遗忘和搜索方向漂移。
- 问题构造与问题求解之间存在结构不对称：知识图谱在出题阶段提供明确的逻辑骨架，但这一结构在轨迹构造和推理阶段常被弱化或丢弃，模型只能从线性交互记录中反复试错并重新发现潜在依赖关系。因此，仅增加题目难度、扩大轨迹数据量或加强事后过滤，并未直接解决搜索过程的状态组织问题。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法尚缺少一种贯穿训练轨迹生成与推理时搜索的统一结构化机制：它既要保留问题约束决定的稳定逻辑关系，又要随工具观察动态更新候选、事实和约束满足情况，并让这些显式状态直接约束下一步行动，而不是仅作为不断增长的文字记录被模型隐式记忆。

</div>
<div markdown="1"><span>核心问题</span>

能否把深度搜索建模为固定拓扑查询图上的状态演化，通过结构不变、状态更新以及图状态对决策的反馈，在不单纯依赖扩大训练数据的情况下，提高长程多跳搜索的连贯性、稳定性、可解释性与搜索效率，并使同一框架同时适用于监督微调轨迹构造和无需额外微调的推理时引导？

</div>
<div markdown="1"><span>作者直觉</span>

固定图结构相当于先为复杂问题画出一张不会随搜索过程丢失的“任务清单与依赖图”，动态状态则像在每个节点和关系旁持续标注候选对象、可靠证据、已满足条件和待解决事项。每轮检索后只把经过验证的原子事实写回对应位置，下一轮再优先处理尚未满足的节点或约束；这样，模型不必每次从整段历史中重新回忆当前进度，搜索方向也更容易受到显式问题结构约束。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

G-ReAct 将开放域深度搜索改写为“固定查询图约束下的结构化状态演化”。输入问题 $q$ 后，初始化器先用一次不调用工具的 LLM 推理生成查询图 $G_0$，把问题中的实体、待求变量及其关系显式化；图的拓扑随后保持不变。搜索代理在每轮仅依据 $G_0$、上一轮状态 $S_{i-1}$ 和本轮局部交互历史 $H_t^{(\mathrm{local})}$ 执行 Think–Act–Observe，调用搜索与网页访问工具收集证据。若本轮不能得出满足全部约束的答案，另一次不调用工具的 LLM 推理会从轨迹 $\tau_i$ 中抽取可追溯事实、更新候选实体及全局一致性状态，并把新状态 $S_i$ 注入下一轮；上一轮冗长的原始交互文本则被丢弃。

这一设计中的“结构—状态共演化”并不表示图结构也会变化：固定的 $G_0$ 始终充当问题约束清单，真正演化的是附着其上的事实、候选和一致性判断。直观地说，普通 ReAct 像不断续写一份越来越长的搜索聊天记录，而 G-ReAct 先画出一张不可随意改写的任务关系图，再在每轮结束时把搜索结果整理成结构化工作台；下一轮主要读取工作台，而不是重新翻阅全部历史。该框架既可用于生成带图和状态的监督微调轨迹，也可直接在推理时包裹现有 LLM，无需额外训练。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 查询图初始化

初始化器 $\phi$ 通过一次无工具 LLM 调用，将 $q$ 解析为固定拓扑图 $G_0=(V_0,E_0)$；节点分为原文命名实体和需要多跳求解的抽象槽位，边从预定义的 $21$ 类关系中选择。每个节点和边都必须锚定到 $q$ 的原文连续片段，禁止引入外部知识、同义改写或规范化结果。

<div class="method-step__io" markdown="1">

**输入**：自然语言问题 $q$。<br>
**输出**：作为全程约束骨架的查询图 $G_0$，以及空初始状态 $S_0=(\emptyset,\emptyset,\emptyset)$。

</div>

**直观理解**：这一步把题目拆成“要找哪些对象、对象之间必须满足什么关系”的检查表。原文锚定规则防止模型在尚未检索前就把自己的猜测写进题目结构。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 图与状态共同引导的工具探索

系统将进度摘要、每个抽象节点置信度最高的若干候选、累计验证事实和未满足约束序列化进新提示；代理随后执行 Think–Act–Observe，并调用 $\text{search}$ 或 $\text{visit}$。搜索方向按当前最佳候选的高、中、低置信度自适应选择：高置信度侧重补验剩余约束，中置信度先有限核验再扩展，低置信度则放弃当前候选并沿图寻找新方向。

<div class="method-step__io" markdown="1">

**输入**：固定查询图 $G_0$、上一轮结构化状态 $S_{i-1}$、问题 $q$，以及本轮局部历史 $H_t^{(\mathrm{local})}$。<br>
**输出**：本轮完整轨迹 $\tau_i=\{(r_{i,s},a_{i,s},o_{i,s})\}_{s=1}^{T_i}$，或已经满足图约束的最终答案。

</div>

**直观理解**：代理不是漫无目的地继续搜索，而是查看图上还缺哪条证据，并依据候选可靠程度决定“继续核验”还是“换方向”。本轮局部记录用于保持眼前操作连贯，但不会永久累积。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 证据驱动的状态更新

状态更新器 $\Psi$ 用一次无工具 LLM 调用依次完成四项工作：抽取单一命题且可定位到工具响应的原子事实；把事实映射到图节点并生成候选、支持约束、违反约束与置信度；检查跨节点候选组合是否满足全部边约束；生成下一轮应核验、消歧、优先或放弃的方向。更新后的状态包含累计事实 $F_{\leq i+1}$、节点候选域 $\mathcal{C}_{i+1}$ 和全局一致性状态 $\Sigma_{i+1}$。

<div class="method-step__io" markdown="1">

**输入**：旧状态 $S_i$、本轮轨迹 $\tau_i$ 和固定查询图 $G_0$。<br>
**输出**：新状态 $S_{i+1}=(F_{\leq i+1},\mathcal{C}_{i+1},\Sigma_{i+1})$，其中 $\Sigma_{i+1}$ 标记遗漏约束、当前最佳组合、跨节点组合及是否完全满足约束。

</div>

**直观理解**：这相当于把一轮杂乱的网页浏览整理成“已证实事实、可能答案、冲突和下一步待办”。只有能追溯到具体工具返回的事实才能进入长期状态，因此状态比原始长对话更适合作为跨轮记忆。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 单调合并、迭代与终止

事实采用只追加去重，重复候选合并支持证据并保留较高置信度，旧的高置信候选若本轮遗漏则重新注入；之后系统丢弃上一轮原始历史，仅把结构化状态渲染到下一轮。若发现满足全部图约束的候选便立即回答；若达到上下文、时间或调用限制则先更新状态，至多执行 $K$ 轮，仍未收敛时选择对 $G_0$ 约束满足度最高的候选组合输出。

<div class="method-step__io" markdown="1">

**输入**：新抽取事实和候选、旧状态、最大轮数 $K$、单轮调用及上下文预算。<br>
**输出**：满足全部约束的答案，或预算耗尽后的最佳努力答案；同时得到可用于监督微调的多轮深搜轨迹。

</div>

**直观理解**：单调合并避免后来一轮因摘要不完整而擦除早先的可靠发现。强制回答机制保证计算有上界，但预算耗尽时的输出不等同于已通过全部约束验证。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 查询图初始化与原文锚定约束

$$
G_{0}=\phi(q)=(V_{0},E_{0}),\qquad \forall x\in V_{0}\cup E_{0},\ \mathrm{anchor}(x)\subseteq\mathrm{span}(q)
$$

**符号说明**

- $q$：输入的自然语言问题。
- $\phi$：以一次无工具 LLM 调用实现的查询图初始化器。
- $G_0$：初始化后保持拓扑不变的查询图。
- $V_0$：实体节点与抽象推理槽位组成的节点集合。
- $E_0$：表达节点间关系和约束的边集合。
- $x$：查询图中的任意节点或边。
- $\mathrm{anchor}(x)$：图元素所对应的逐字原文锚点。
- $\mathrm{span}(q)$：问题文本中所有连续子串构成的范围。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分说明模型把问题转换成图，第二部分要求图中每个结构元素都能在问题原文中找到依据。该约束把图限定为题意的结构化表达，而不是允许初始化器偷偷补充检索知识；它是后续约束检查可信的前提，但不能保证模型选择的节点和关系一定完整。<br>
**原文位置**：第 3.1 节，公式（1）与公式（2）

</div>

</div>

<div class="equation-block" markdown="1">

#### 图条件决策与证据驱动状态转移

$$
a_t\sim\pi_{\mathrm{G\text{-}ReAct}}\!\left(\cdot\mid G_0,S_{i-1},H_t^{(\mathrm{local})}\right),\qquad S_{i+1}=\Psi(S_i,\tau_i)=(F_{\leq i+1},\mathcal{C}_{i+1},\Sigma_{i+1})
$$

**符号说明**

- $a_t$：当前步骤选择的工具动作或回答动作。
- $\pi_{\mathrm{G\text{-}ReAct}}$：由 LLM 实现的 G-ReAct 决策策略。
- $G_0$：固定查询图，提供全局问题结构与约束。
- $S_{i-1}$：进入第 i 轮时携带的上一轮结构化状态。
- $H_t^{(\mathrm{local})}$：当前轮截至步骤 t 的局部 Think–Act–Observe 交互历史。
- $\Psi$：从旧状态和本轮轨迹生成新状态的无工具 LLM 更新函数。
- $\tau_i$：第 i 轮的完整推理、动作和工具观察轨迹。
- $F_{\leq i+1}$：截至新一轮累计保存的可追溯验证事实集合。
- $\mathcal{C}_{i+1}$：更新后的逐节点候选域及其证据、违反约束和置信度。
- $\Sigma_{i+1}$：更新后的全局一致性、缺失约束、最佳组合和满足状态。

<div class="equation-explanation" markdown="1">

**直观理解**：左式规定每个动作同时参考固定任务结构、跨轮压缩记忆和当前轮短期历史；右式规定一轮结束后如何把原始轨迹压缩成下一轮可复用的状态。两式共同形成闭环：图告诉代理必须解决什么，状态告诉代理已经解决到哪里，本轮轨迹则提供新增证据。<br>
**原文位置**：第 3.2 节公式（4）与第 3.3 节公式（5）；状态分量依据第 3.2 节公式（3）及第 3.3 节定义

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：论文所述训练阶段是全参数监督微调：每个样本包含问题 $q$、查询图 $G_0$，以及交错排列的推理文本、工具调用、未压缩工具响应和最终答案，模型学习复现这些 G-ReAct 轨迹。所给章节没有写出独立的损失函数，也没有说明是否对工具响应或用户消息位置计算语言模型损失，因此只能确认采用监督微调，不能据此补写具体 token 级目标；训练明确未使用强化学习。

训练数据的关键变量不是额外奖励，而是轨迹如何携带状态：单轮样本从空状态开始并在一轮内完成，多轮续搜样本的首个用户回合包含先前由 $\Psi$ 生成的候选、满足状态和事实池。这样，微调同时教授模型从零构图搜索和从结构化中间状态继续搜索；推理时即使不微调，也可把相同的图构建、状态更新和提示渲染流程作为外部推理框架使用。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 原文锚定的固定查询图**

$G_0$ 的节点包括待求解的抽象节点和必须逐字匹配问题文本的实体节点；边表示组合、归属、用途和约束等关系，并保存关系类型、值描述和原文锚点。图初始化后不再改写，因此跨轮搜索始终面对同一套显式约束；不过作者也明确指出，单调状态保证并不能证明初始化器生成的 $G_0$ 本身正确。

> 直观理解：固定图的作用类似一张不会随搜索过程漂移的验收表：候选答案必须同时通过多项关系检查。它能抑制目标漂移，却仍可能继承最初拆题错误，因此原文锚定只能降低风险，不能消除风险。

**2. 事实—候选—一致性三层状态**

状态 $S_i=(F_{\leq i},\mathcal{C}_i,\Sigma_i)$ 分离三类信息：$F_{\leq i}$ 保存累计验证事实，$\mathcal{C}_i$ 为各抽象节点保存候选实体、支持或违反的图约束及离散置信度，$\Sigma_i$ 负责跨节点组合、遗漏约束、当前最佳赋值和完全满足标志。每轮提示仅注入这一压缩状态和本轮局部历史，使跨轮一致性不再依赖无限增长的平面文本历史。

> 直观理解：事实层回答“网页确实说了什么”，候选层回答“这些事实支持哪些可能对象”，一致性层回答“把对象组合起来后是否满足整道题”。分层后，模型可以定位缺口，而不必从长对话中重新辨认搜索进度。

**3. 抗退化状态合并**

更新器执行三项约束：已验证事实只追加且按事实内容去重；同一候选跨轮出现时取较高置信度并合并支持证据；任何旧的高置信候选都不能仅因新一轮未提及而消失。论文据此给出单调状态进展命题：事实集合不会缩小，共同出现候选的置信度不会降低，高置信候选会持续保留；在可验证事实有限且置信度取值有限时，状态最终到达不再变化的固定点。

> 直观理解：LLM 做摘要时可能漏掉早先内容，这个模块用显式合并规则保护已经获得的进展。这里保证的是记录不会倒退和最终稳定，不是保证一定找到正确答案，也不是保证错误的高置信候选会自动消失。

**训练与推理**

训练数据从 OpenSeeker-v1 抽取并经 G-ReAct 构造，共保留 $1{,}898$ 条轨迹，其中 $1{,}156$ 条为从空状态开始的单轮轨迹，$742$ 条为携带预计算状态的续搜轨迹。处理流程修复非标准的 think、tool_call、tool_response 和 answer 标签，删除错误标记、空工具返回及反映检索循环的连续重复查询，并把数据统一为仅保留 messages 字段的 JSON 数组。随后以 Qwen3-30B-A3B-Thinking-2507 为基座进行全参数监督微调，训练样本保留完整工具响应，使模型直接接触检索证据而非只学习摘要。

推理时，系统先生成 $G_0$ 并置 $S_0$ 为空；每轮渲染问题、图、进度、候选和事实，代理在调用上限内执行工具探索。若直接产生且验证出满足全部图约束的答案，则立即返回；否则在本轮显式终止、上下文达到状态更新阈值或调用预算耗尽时执行 $\Psi$，应用抗退化合并后开始新轮。最多运行 $K=5$ 轮；若一致性状态的完全满足标志始终为假，则根据累计事实与最终候选域选择图约束满足度最高的组合，输出最佳努力答案。由于图和状态通过提示提供，该推理流程也能用于未接受 G-ReAct 微调的现有 LLM。

**复现信息**

为公平复现，训练基座为 Qwen3-30B-A3B-Thinking-2507，其混合专家结构每次激活约 $3$B 参数；采用 BF16 的全参数监督微调，训练 $3$ 个 epoch，有效批量大小为 $32$，最大序列长度为 $128$k，AdamW 峰值学习率为 $1\times10^{-5}$ 并余弦衰减至 $1\times10^{-7}$。训练使用 $16$ 张 NVIDIA A100 80GB GPU；这些配置影响算力可比性，但论文方法本身并不依赖特定并行布局。

每个问题最多进行 $K=5$ 个精炼轮次，每轮最多 $N_{\max}=100$ 次 LLM 调用、最长 $20$ 分钟并使用 $128$k 上下文窗口；当上下文达到 $L_{\max}=64$k 时触发状态更新，为更新提示预留空间。$\text{search}$ 支持并行 Google 查询，每个查询返回前 $10$ 个结果并通过缓存去重；$\text{visit}$ 依次经过抓取、Jina 处理、LLM 摘要和 JSON 输出，返回 rational、evidence 与 summary。系统还检测连续两次相同工具调用并提示改变搜索方向，这属于避免检索循环的工程保护，解释效率结果时应与图状态机制区分。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- BrowseComp 与 BrowseComp-ZH：分别面向英文和中文的开放式网页浏览测试集，要求模型通过多轮搜索识别未知实体、解析隐含关系与歧义约束，并完成跨文档推理和事实核验。实验使用完整测试集；二者主要检验长程多跳搜索中约束保持和证据串联能力。
- XBench-DeepSearch（XBench-DS）：跨领域信息综合基准，要求模型从多个来源汇总并协调证据。实验使用完整测试集；它更侧重复杂信息聚合，因此适合检验查询图能否显式表示子问题及其依赖关系。
- GAIA：面向通用 AI 助手的异构工具使用与多步组合推理基准。论文仅采用包含 $103$ 个样本的纯文本验证子集，用于检查方法是否能迁移到网页深度搜索之外的综合工具推理场景。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**pass@1**

模型一次作答即通过判定的样本比例。论文以 GPT-4o-mini 作为 LLM 裁判，因此该指标衡量的是裁判认可的首答正确率，而不等同于人工核验准确率。 （越高越好，因为更高值表示无需多次采样即可成功回答的题目更多。）

</div>
<div class="metric-item" markdown="1">

**pass@3（p@3）**

在最多三次尝试中至少一次成功的比例，消融实验用它观察方法在多次采样条件下的潜在成功覆盖率。 （越高越好，因为它表示三次候选中出现正确答案的概率更大；但它不能替代单次作答能力。）

</div>
<div class="metric-item" markdown="1">

**Avg. Tool Calls**

每道题平均触发搜索等外部工具的次数，用来近似衡量搜索步骤与工具使用成本。 （在正确率不下降的前提下越低越好，因为更少调用意味着搜索路径更精简；单独降低该值并不代表答案质量更高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 监督微调后的总体性能：G-ReAct-OpenSeeker-v1 与同规模及更大模型比较

<div class="result-value" markdown="1">

G-ReAct-OpenSeeker-v1 使用约 $1.9\mathrm{K}$ 条轨迹，在 XBench-DS 上取得 $79.0\%$ pass@1，比 DeepSeek-V3.1-671B 的 $71.2\%$ 高 $7.8$ 个百分点；在 BrowseComp-ZH 和 BrowseComp 上分别达到 $52.6\%$ 与 $35.6\%$。

</div>

作者据此主张，合理组织搜索状态可以让约 $30\mathrm{B}$ 参数模型在部分深度搜索任务上超过远大于它的模型。分析上，这证明了 G-ReAct 在论文所列系统和评测协议中的竞争力，却不能单独证明结构设计普遍优于扩大参数规模：大模型基线并非统一工具、预算和推理配置下的受控实验，且 BrowseComp 上仍低于若干大型或闭源系统。

<div class="result-source" markdown="1">

来源：第 4.2 节“(1) Performance”及表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

G-ReAct-OpenSeeker-v1 achieves 79.0 on XBench-DS, establishing a new state of the art among our compared baselines and leading DeepSeek-V3.1-671B by 7.8 points. On BrowseComp-ZH, it achieves 52.6, surpassing GLM-4.6-357B (49.5). On BrowseComp, it reaches 35.6, the best result among ∼30B open-source deep-search models.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 同源问答池下的训练数据效率：G-ReAct 与 DeepDive、OpenSeeker-v1 对照

<div class="result-value" markdown="1">

在 DeepDive 同源比较中，G-ReAct-DeepDive 在 BrowseComp、BrowseComp-ZH 和 XBench-DS 上分别提高 $15.8$、$24.2$ 和 $26.0$ 个百分点；在 OpenSeeker-v1 同源比较中，G-ReAct 仅使用原训练轨迹数量的 $16\%$（约 $1.9\mathrm{K}$ 对 $11.7\mathrm{K}$），仍分别提高 $6.1$、$4.2$ 和 $5.0$ 个百分点。

</div>

这是支持“图结构轨迹具有更高监督效率”的核心受控证据：问题池来源相同，主要变化是轨迹被 G-ReAct 流程重新组织。它说明少量图结构轨迹可以优于更多线性轨迹，但尚不能把全部增益严格归因于图表示，因为重新生成过程还可能改变证据质量、推理长度或答案过滤质量。

<div class="result-source" markdown="1">

来源：第 4.2 节“(2) Data Efficiency”及表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In the same-source comparison, G-ReAct-DeepDive outperforms DeepDive-30B-A3B by 15.8, 24.2, and 26.0 points on BrowseComp, BrowseComp-ZH, and XBench-DS, respectively. Likewise, G-ReAct-OpenSeeker-v1 uses only 16% of the training trajectories (1.9K vs. 11.7K), yet still improves over OpenSeeker-v1-SFT by 6.1, 4.2, and 5.0 points on the same benchmarks.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### BrowseComp-ZH 上的免微调推理时指导：三个强模型启用 G-ReAct 前后比较

<div class="result-value" markdown="1">

启用 G-ReAct 后，doubao-seed-2.0-pro 的 pass@1 从 $64.71\%$ 升至 $71.28\%$，平均工具调用从 $19.72$ 降至 $18.62$；Claude-4.5-Sonnet 从 $39.10\%$ 升至 $43.94\%$，调用从 $24.32$ 降至 $22.91$；OpenAI-o3 从 $54.33\%$ 升至 $56.87\%$，调用从 $18.71$ 降至 $17.22$。

</div>

三种模型都同时提高正确率并减少工具调用，支持图状态能够把搜索集中到尚未解决的节点，而不是依靠更多试探换取正确率。该结果只在 BrowseComp-ZH 上报告，且未给出方差、置信区间或显著性检验，因此可以判断方向一致，不能据此确定增益在其他任务上同样稳定或具有统计显著性。

<div class="result-source" markdown="1">

来源：第 4.2 节“(3) Inference-Time Guidance”及表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 2 shows that, as a fine-tuning-free inference-time framework, G-ReAct consistently improves the performance of strong LLMs, boosting doubao-seed-2.0-pro by 6.57 points (64.71→71.28), Claude-Sonnet-4.5 by 4.84 points (39.10→43.94), and OpenAI-o3 by 2.54 points (54.33→56.87). More importantly, these improvements are accompanied with fewer tool calls—average reductions of 1.10, 1.41, and 1.49, respectively.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评测主要依赖 GPT-4o-mini 作为 LLM 裁判，原文未明确报告人工复核、裁判一致性或答案匹配误差；因此 pass@1 的变化可能同时包含真实能力变化与自动裁判偏差。
- 除同源轨迹实验外，多数基线来自官方报告或公开榜单，工具接口、搜索预算、上下文限制和运行时间可能不同；推理时实验也只报告 BrowseComp-ZH，且未提供置信区间或显著性检验，所以跨系统排名与泛化范围仍需统一协议复验。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- DeepDive-30B-A3B 与 OpenSeeker-v1-30B-A3B：最关键的同源受控基线。G-ReAct 分别从相同底层问答池抽取 $618$ 和 $1{,}898$ 个问答对，再重新生成图结构轨迹，因此比较主要隔离“轨迹结构”而非问题来源的影响；但样本抽取及重新生成仍可能引入其他差异。
- WebDancer、MiroThinker、WebSailor、WebSailor-V2、WebLeaper 与 Tongyi DeepResearch：约 $30\mathrm{B}$ 参数的开源深度搜索系统，覆盖 SFT、SFT+RL 以及 CPT+SFT+RL，并使用不同规模的数据。该组用于判断 G-ReAct 能否以更简单的训练配方和更少监督样本达到竞争性结果。
- Kimi-K2、DeepSeek-V3.1/V3.2、GLM-4.6/4.7 与 MiniMax-M2：参数规模约为 $230\mathrm{B}$ 至 $671\mathrm{B}$ 的开源大模型。该组检验结构化搜索组织是否能部分弥补模型规模差距，但并非严格控制主干、工具环境和推理预算的公平比较。
- Claude-4.5-Sonnet、Claude-4-Opus、OpenAI-o3、OpenAI Deep Research 与 GPT-5-Thinking-High：闭源强模型，用于提供前沿系统参照。其中 doubao-seed-2.0-pro、Claude-4.5-Sonnet 和 OpenAI-o3 还用于成对测试免微调的推理时 G-ReAct 指导。

**实验想回答的问题**

- 在仅使用监督微调的条件下，将搜索轨迹组织为“固定拓扑查询图上的状态演化”，能否比线性轨迹提供更有效、数据效率更高的训练监督，并使约 $30\mathrm{B}$ 参数模型在多跳检索与跨来源信息综合任务上超过同规模深度搜索模型？
- 在不额外微调被测模型时，G-ReAct 的图结构推理指导能否同时提高答案正确率并减少工具调用；查询图、状态演化和状态更新粒度是否确实是性能提升的关键因素？

**实验实现**

G-ReAct 以 Qwen3-30B-A3B-Thinking-2507 为主干，只进行 SFT；训练使用 $2\times8$ 张 A100 80GB GPU、Megatron 框架、$3$ 个 epoch、批大小 $32$、学习率 $10^{-5}$ 和 $128\mathrm{K}$ token 上下文窗口。评测除 GAIA 外使用各基准完整测试集，推理温度为 $0.6$、top-$p$ 为 $0.95$，所有主结果均报告由 GPT-4o-mini 判定的 pass@1。表 1 的非受控基线结果主要来自官方技术报告或公开榜单，因而模型接口、搜索工具、预算和评测时间未必完全一致；表 2 则在 BrowseComp-ZH 上比较同一模型启用与不启用 G-ReAct 的表现，更直接检验推理时指导。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 分别移除 Query Graph 或 State Evolution | 完整 G-ReAct 在 XBench 上的平均 p@1 为 $75.00\%$；移除 Query Graph 后降至 $67.00\%$，移除 State Evolution 后为 $69.67\%$。在 BrowseComp-ZH 上，完整模型为 $52.25\%$，两种移除版本分别降至 $48.44\%$ 和 $46.88\%$。 | 该实验分别隔离“显式子问题结构”和“依据新证据更新节点状态”两个组件。Query Graph 在 XBench 上造成更大降幅，支持它对复杂证据聚合的重要性；State Evolution 在两个基准上都下降，并在 BrowseComp-ZH 上影响更大，支持它帮助保存中间结论与约束。由于论文未报告误差条或显著性检验，组件间降幅大小应视为趋势而非精确排序。 | 第 4.3 节“Component Contribution Analysis”及表 3<br><span class="experiment-evidence">Removing the query graph causes a larger drop on XBench than on BrowseComp-ZH, indicating its importance for complex information aggregation tasks. Removing state evolution leads to consistent degradation on both benchmarks, highlighting its role in maintaining intermediate states and reducing reasoning drift during long-horizon search.</span> |
| 状态更新粒度：比较 $32\mathrm{K}$、$64\mathrm{K}$、$96\mathrm{K}$ 与 $128\mathrm{K}$ 滑动窗口 | $64\mathrm{K}$ 窗口在 XBench 上取得最高的平均 p@1、p@3 和回答率，分别为 $75.00\%$、$90.00\%$ 和 $98.33\%$；$32\mathrm{K}$、$96\mathrm{K}$、$128\mathrm{K}$ 的平均 p@1 分别为 $70.00\%$、$70.67\%$ 和 $67.67\%$。 | 窗口大小决定多久把累积文本压缩并写回图状态。结果支持一个中间粒度的折中：更新过频会切碎连续推理，更新过慢则可能在整理状态前已经发生上下文退化。不过该消融只在 XBench 上进行，不能证明 $64\mathrm{K}$ 是跨模型、跨任务的普适最优值。 | 第 4.3 节“Design Choice Analysis”及表 4<br><span class="experiment-evidence">For state-update granularity, we compare four sliding-window sizes (32K / 64K / 96K / 128K), with 64K achieving the best performance across all metrics (Table 4).</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It proposes a graph-state framework that guides long-horizon tool-based search and structured reasoning by LLM agents.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`b66d4558c00d64bef442b7913e58a38fa8ec52529b7fc4a027bb61c001035c32`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
