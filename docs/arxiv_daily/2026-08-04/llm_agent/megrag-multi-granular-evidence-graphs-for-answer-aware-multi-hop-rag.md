---
title: "[论文解读] MEGRAG: Multi-Granular Evidence Graphs for Answer-Aware Multi-Hop RAG"
description: "[arXiv 2608.02195][LLM Agent] MEGRAG通过按需组合三元组、句子和段落级证据，并利用每一步的中间答案判断继续检索还是停止，旨在减少多跳问答中的上下文噪声、冗余证据与误差累积。"
arxiv_id: "2608.02195"
announcement_date: "2026-08-04"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:05:11.843591+00:00"
source_sha256: "0fe7ebc047e8e750c3e05f13484d16f53173f103c6a1ca9352eb6cb5df61a937"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "检索增强生成"
  - "多跳问答"
  - "迭代式 RAG"
  - "多粒度证据"
  - "跨粒度索引"
  - "证据图"
  - "答案感知推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.02195</p>

# MEGRAG: Multi-Granular Evidence Graphs for Answer-Aware Multi-Hop RAG

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Weidong Bao, Yingying Sun, Jun Yang, Yilin Wang, Zili Wei, Yubin Bao, Fangling Leng, Minghe Yu, Tiancheng Zhang, Ge Yu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Northeastern University, Shenyang, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.02195v1) · [PDF 下载](https://arxiv.org/pdf/2608.02195v1) · **关键词** 检索增强生成, 多跳问答, 迭代式 RAG, 多粒度证据, 跨粒度索引, 证据图, 答案感知推理<br>


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

MEGRAG通过按需组合三元组、句子和段落级证据，并利用每一步的中间答案判断继续检索还是停止，旨在减少多跳问答中的上下文噪声、冗余证据与误差累积。

**不用术语来说**：复杂问题的答案往往不能从一段文本中直接找到，而要先找到一个线索，再用它定位下一条信息，最后把多处证据连接起来。现有系统通常在每一步只使用一种大小的文本片段：片段太短可能缺少必要背景，太长又会混入无关内容；同时，系统常常要等所有检索步骤结束后才尝试回答原问题，因而可能继续搜集已经不需要的信息，并把早期检索错误带到最终答案中。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出跨粒度证据组织与选择机制：离线建立段落、句子和三元组之间的索引，在线从紧凑的三元组开始，根据当前问题的证据充分性按需扩展到对应句子或段落，从而使不同问题和不同推理步骤可以采用不同证据粒度。
- 提出答案感知的迭代推理策略：每一步先回答当前查询，再结合中间答案与既有推理判断初始问题是否已经解决；若仍缺信息，则明确知识缺口并生成更聚焦的下一查询，否则立即停止，整个过程形成面向当前问题的路径式证据图。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

检索增强生成（RAG）先从外部语料中检索证据，再由语言模型依据证据回答问题。本文关注其中的多跳问答：答案所需信息分散在多个来源，后续证据的相关性往往只有在获得前序线索后才显现，因此仅按初始问题执行一次检索容易找到局部线索，却遗漏中间证据。迭代式 RAG（iRAG）通过交替进行检索、推理和查询改写来逐步补齐信息；相关研究还利用图、超图或证据链连接分散证据，并通过不同粒度的信息单元兼顾精确性与上下文完整性。MEGRAG 所处的具体问题是：如何在每一跳动态选择三元组、句子或段落级证据，并依据当前中间答案判断原始问题是否已经解决。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**检索增强生成（RAG）**

RAG 将语言模型与外部检索器结合：检索器从语料库找出相关文本，生成模型再依据这些文本作答。它使答案能够利用模型参数之外的知识，但效果取决于检索证据是否相关且充分。

</div>
<div class="concept-item" markdown="1">

**多跳问答与迭代式 RAG（iRAG）**

多跳问答要求把分散在多个来源中的线索按依赖关系组合起来，通常不能通过一次检索直接得到答案。iRAG 在每轮推理后根据已知信息改写查询并继续检索，使后续检索能够针对当前仍缺失的线索。

</div>
<div class="concept-item" markdown="1">

**多粒度证据**

同一来源可以表示为段落、句子和关系三元组等不同粒度：细粒度单元更紧凑，但可能缺少语境；粗粒度单元上下文更完整，却可能带来无关噪声。本文所说的跨粒度索引，是把同一段落及其句子和抽取出的三元组对应起来，以便推理时按需扩展证据。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个需要多步推理的初始自然语言问题和可检索的文本语料库，系统需要在开放式检索环境中逐轮寻找证据，并最终输出问题答案。每一轮以当前查询为输入，先检索候选段落，再从相互对齐的三元组、句子和段落视图中选择足以回答当前查询的证据，产生中间答案；系统随后结合既往推理判断该中间答案是否已经解决初始问题。若信息仍不充分，则识别尚缺的事实并形成下一轮聚焦查询；若已充分，则停止检索并返回答案。其基本假设是，多跳所需事实存在于语料库的不同文本单元中，而且证据的适宜粒度会随问题和推理步骤变化。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Trivedi et al. (2023), Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions**: 代表迭代式 RAG 路线，通过交替执行检索与链式推理，让中间推理结果引导后续证据获取；它构成本文多轮检索设定的直接基础。MEGRAG 进一步强调每一轮的多粒度证据选择，以及利用中间答案判断继续检索或停止。
- **Hu et al. (2026), Iterative Multi-Granular RAG with Contextual Hierarchical Graph**: 直接相关的多粒度 RAG 工作，利用层次化结构平衡聚焦证据与上下文完整性。本文据引言所述进一步针对两个缺口：推理步骤仍可能依赖固定或单一粒度证据，以及仅在多轮证据汇总后回答原始问题所造成的冗余与错误累积。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

多跳问答需要从分散来源中逐步发现并整合证据。只依据初始问题执行一次检索，通常只能找到与问题表面直接相关的局部线索，而后续证据的相关性往往要在获得中间结论后才显现。因此，系统既要随着推理进展更新检索目标，也要控制每一步提供给生成模型的证据是否足够且不过量。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **迭代式检索增强生成**：在检索与推理之间循环：系统根据已获得的证据诊断尚缺的信息、改写查询，再检索下一跳证据；通常在完成若干轮检索并汇总各轮材料后，才回答最初的问题。
- **结构感知与多粒度检索**：结构感知方法借助图、超图或证据链连接分散信息；多粒度方法则使用较细单元进行排序，或从局部证据向更大上下文扩展，以提高检索精度并兼顾语境完整性。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 多数方法在单个推理步骤内仍以固定的单一粒度提供证据，无法同时兼顾信息密度与上下文完整性：三元组或短片段虽然集中，却可能缺少解释答案所需的语境；完整段落虽然信息较全，却可能引入无关内容并干扰推理。
- 多数迭代方法把“检索过程”与“回答初始问题”顺序分离，往往完成多轮检索后才统一作答；系统因而不能利用中间答案及时判断证据是否已经充分，容易继续检索冗余材料，并使中间步骤的检索错误逐轮累积，最终降低答案质量。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究分别增强了查询改写、证据结构化和粒度调节，但仍缺少一个统一机制：它应在每个推理步骤内依据当前查询动态选择最低但充分的证据粒度，同时把该步形成的答案直接用于判断初始问题是否已解决、识别剩余知识缺口并控制检索终止。

</div>
<div markdown="1"><span>核心问题</span>

能否构建一种面向多跳问答的迭代式RAG框架，使其在每一步从三元组、句子和段落中按充分性选择证据，并以中间答案为反馈，自适应决定生成下一条聚焦查询或立即返回最终答案？

</div>
<div markdown="1"><span>作者直觉</span>

人的信息搜寻通常以“足够支持当前判断”为停止标准：先查看最简洁的事实，只有事实缺少语境时才阅读更完整的句子或段落；得到阶段性结论后，再判断原问题是否已经能回答。将这一过程计算化，可以让紧凑证据承担主要推理，必要时才补充上下文，并让中间答案成为下一步行动的依据，从源头减少无效检索和错误传播。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MEGRAG 将多跳问答建模为一个随检索过程在线增长的、问题特定的路径式证据图。输入是初始问题 $x$ 与语料库 $\mathcal{D}=\{d_j\}_{j=1}^{N}$；离线阶段把每篇段落组织为段落、句子和关系三元组三种粒度，并用跨粒度索引 $\mathcal{I}$ 保持细粒度证据与来源段落之间的对应关系。在线阶段从 $q_1=x$ 开始，每轮先按当前查询 $q_i$ 检索段落，再收集这些段落内部的句子和三元组；策略 $\pi$ 按“三元组、三元组加句子、再加段落”的由细到粗顺序选择首个足够回答当前查询的证据组合 $Z_i$，生成中间答案 $b_i$，并结合既有推理历史判断初始问题是否已经解决。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 离线构建多粒度证据空间

系统保存段落视图 $\mathcal{E}^{P}$，切分得到句子视图 $\mathcal{E}^{S}$，并用大语言模型从段落中抽取关系三元组形成 $\mathcal{E}^{T}$；跨粒度索引 $\mathcal{I}$ 将每条句子和三元组映射回其来源段落。只为段落建立稠密向量检索入口，句子和三元组不在全语料范围内独立检索。

<div class="method-step__io" markdown="1">

**输入**：语料库 $\mathcal{D}=\{d_j\}_{j=1}^{N}$，其中每个 $d_j$ 是一个可检索段落。<br>
**输出**：多粒度证据空间 $\mathcal{E}=\{\mathcal{E}^{P},\mathcal{E}^{S},\mathcal{E}^{T},\mathcal{I}\}$，其中三种视图共享明确的来源对应关系。

</div>

**直观理解**：同一份资料被做成“全文段落、关键句、事实卡片”三种版本，并用目录记录它们属于哪篇原文。这样既能用短事实快速作答，也能在事实不够明确时返回原句或完整上下文。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按当前信息缺口收集对齐候选证据

系统编码 $q_i$ 并按向量相似度排序全部段落，取前 $N_P$ 个形成 $C_i^{P}$；随后依照段落检索次序，通过 $\mathcal{I}$ 收集其关联句子和三元组，去重后分别保留至多 $N_S$ 个句子和 $N_T$ 个三元组。由此得到候选集合 $C_i=\{C_i^{P},C_i^{S},C_i^{T}\}$，三种粒度均来自同一批已检索段落。

<div class="method-step__io" markdown="1">

**输入**：当前查询 $q_i$、段落向量索引和跨粒度索引 $\mathcal{I}$。<br>
**输出**：与 $q_i$ 相关且跨粒度对齐的段落、句子和三元组候选集合 $C_i$。

</div>

**直观理解**：系统先找到可能相关的几篇文章，再只查看这些文章里的句子和事实卡片。这个局部化过程避免在整个知识库中分别搜索三种材料而造成来源错配或搜索成本膨胀。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自适应选择证据并构造推理节点

策略 $\pi$ 依次检查 $C_i^{T}$、$C_i^{T}\cup C_i^{S}$ 和 $C_i^{T}\cup C_i^{S}\cup C_i^{P}$，在首个足以支持当前回答的粒度停止扩充，并形成 $Z_i=(T_i,S_i,P_i)$。策略基于该证据生成当前查询的中间答案 $b_i$，更新已解决路径 $h_i$，记录剩余信息需求 $m_i$，并联合预测停止标志 $s_i$、初始问题答案 $y_i$、下一查询 $q_{i+1}$ 和转移关系 $r_i$。

<div class="method-step__io" markdown="1">

**输入**：初始问题 $x$、当前查询 $q_i$、候选证据 $C_i$，以及由先前证据图 $G^{(i-1)}$ 压缩得到的结构化历史 $H_i$。<br>
**输出**：推理节点 $v_i=(q_i,Z_i,b_i,h_i,m_i,y_i,s_i)$，以及继续检索时所需的 $q_{i+1}$ 和 $r_i$。

</div>

**直观理解**：系统先尝试只看最简洁的事实；若事实缺少限定条件，就补充原句，再不够才读取整段。它不仅回答眼前的小问题，还明确记下“已经知道什么、仍缺什么”，从而让下一轮检索围绕缺口展开。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 更新路径、答案感知停止并输出

若 $s_i=0$，系统要求 $y_i=\emptyset$ 且 $m_i\neq\mathrm{none}$，添加继续边 $e_i^{\mathrm{cont}}=(v_i,r_i,v_{i+1})$，并用 $q_{i+1}$ 开始下一轮；若 $s_i=1$，则要求 $m_i=\mathrm{none}$、$y_i\neq\emptyset$ 和 $q_{i+1}=\emptyset$，添加终止边并返回 $\hat{a}=y_i$ 及其证据轨迹。若达到 $i=B$ 仍未停止，最终解析器仅使用按顺序选中的 $(Z_1,\ldots,Z_B)$，并把 $b_B$ 作为候选线索生成预测，同时将轨迹标为预算耗尽。

<div class="method-step__io" markdown="1">

**输入**：当前节点 $v_i$、停止决策 $s_i$、下一查询 $q_{i+1}$、转移关系 $r_i$ 和最大步骤预算 $B$。<br>
**输出**：最终答案 $\hat{a}$、可追踪的推理路径 $P_{\hat{a}}$，或带有预算耗尽标记的最终解析结果。

</div>

**直观理解**：每轮结束后，系统直接检查原始问题是否已经被完整回答，而不是机械地运行固定轮数。若尚未解决，它只围绕明确的信息缺口提出一个新问题；若已经解决，则立即停止并保留从查询、证据到答案的完整记录。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 单步图构建策略

$$
o_i=(Z_i,b_i,y_i,s_i,q_{i+1},h_i,m_i,r_i)=\pi(x,q_i,H_i,C_i)
$$

**符号说明**

- $x$：需要最终回答的初始问题。
- $q_i$：第 i 轮用于检索和局部作答的当前查询。
- $H_i$：先前证据图的结构化摘要，包含已有查询、证据、中间答案、已解决路径、信息缺口和转移关系。
- $C_i$：第 i 轮对齐的段落、句子和三元组候选集合。
- $\pi$：负责证据选择、回答、缺口识别、停止判断和下一查询生成的图构建策略。
- $Z_i$：策略从多粒度候选中选出的证据组合。
- $b_i$：由所选证据支持的当前查询中间答案。
- $y_i$：停止时给出的初始问题答案；继续时为空。
- $s_i$：二值停止决策，1 表示初始问题已经解决，0 表示仍需检索。
- $q_{i+1}$：针对剩余信息需求生成的下一轮查询；停止时为空。
- $h_i$：截至当前步骤已经解决的推理路径。
- $m_i$：回答初始问题仍缺少的信息；完成时为 none。
- $r_i$：说明下一查询如何朝初始问题目标推进的转移关系。
- $o_i$：策略在第 i 轮联合生成的完整结构化决策。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把通常分散实现的多个动作统一为一次条件决策：系统既选择证据和生成局部答案，也显式判断原问题是否完成，并在未完成时描述缺口和产生下一查询。联合输出使“检索什么、为什么继续、何时停止”共享同一份问题目标和历史状态。<br>
**原文位置**：Methodology，Path-structured Question-specific Evidence Graph Construction，公式 (6)

</div>

</div>

<div class="equation-block" markdown="1">

#### 图构建蒸馏目标

$$
\mathcal{L}_{\mathrm{GCD}}=-\sum_{\xi}\sum_{i=1}^{L_{\xi}}\log p_{\theta}(o_i\mid x,q_i,H_i,C_i)
$$

**符号说明**

- $\mathcal{L}_{\mathrm{GCD}}$：图构建蒸馏的负对数似然损失。
- $\xi$：教师针对一个训练问题生成的完整决策轨迹。
- $L_{\xi}$：轨迹 xi 包含的决策步骤数。
- $i$：轨迹中的步骤下标。
- $p_{\theta}$：参数为 theta 的学生策略所定义的条件输出概率。
- $o_i$：教师在第 i 步给出的完整目标决策，包括证据、回答、停止状态、缺口和下一查询等字段。
- $(x,q_i,H_i,C_i)$：学生预测第 i 步决策时使用的初始问题、当前查询、结构化历史与候选证据。

<div class="equation-explanation" markdown="1">

**直观理解**：训练最小化教师完整决策的负对数概率，即要求学生在每个状态下尽可能复现教师的整个结构化输出。它监督的是逐步控制策略，而不只是最终答案，因此证据选择错误、错误停止或偏离信息缺口的下一查询都会受到训练约束。<br>
**原文位置**：Methodology，Graph Construction Distillation，公式 (9)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标是最小化 $\mathcal{L}_{\mathrm{GCD}}$，等价于最大化学生策略在每个教师状态下生成目标决策 $o_i$ 的条件似然。教师先执行完整的多轮图构建过程并产出逐步轨迹，学生以监督微调方式学习所有输出字段；因此优化同时覆盖多粒度证据选择、中间答案、已解决路径、剩余信息需求、停止判断、最终答案、下一查询和转移关系。继续节点与终止节点具有不同的一致性约束：前者应输出 $s_i=0$、非空缺口和下一查询，后者应输出 $s_i=1$、$m_i=\mathrm{none}$、非空最终答案及空的下一查询。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 跨粒度证据空间与索引**

证据空间同时包含段落视图 $\mathcal{E}^{P}$、句子视图 $\mathcal{E}^{S}$ 和三元组视图 $\mathcal{E}^{T}$；索引 $\mathcal{I}$ 把句子、三元组与来源段落连接起来。段落承担语义检索入口，细粒度单元只在已检索段落内部被收集，因此系统并不依赖全语料知识图谱遍历。

> 直观理解：三元组信息密度高，但可能丢失否定、时间、别名或比较条件；句子保留局部限定，段落则提供消歧和跨句背景。来源对齐保证补充上下文时取回的是同一事实的原文，而不是语义相似但出处无关的材料。

**2. 路径式问题特定证据图与结构化历史**

第 $i$ 步的图为 $G^{(i)}=(V^{(i)},E^{(i)})$，每个节点保存查询、已选证据、中间答案、已解决路径、剩余需求、最终答案和停止状态。由于每个节点至多产生一个 $q_{i+1}$，该图实际是一条有向路径；历史摘要 $H_i=\mathrm{GraphSummary}(G^{(i-1)})$ 还保留目标条件化的转移关系 $r_i$，说明下一次检索如何补足初始问题 $x$。

> 直观理解：这里的“图”主要不是用来搜索复杂分支，而是把每轮决策组织成可审计的推理链。相较于只累计证据文本，结构化历史能区分已解决结论、当前缺口和下一步目的，减少重复检索以及前序错误的无条件累积。

**3. 图构建策略蒸馏**

教师策略对每个训练问题运行完整流程，生成轨迹 $\xi=\{(x,q_i,H_i,C_i,o_i)\}_{i=1}^{L_\xi}$；学生策略学习复现完整决策 $o_i=(Z_i,b_i,y_i,s_i,q_{i+1},h_i,m_i,r_i)$，而非只学习最终答案。终止样本还联合监督 $s_i=1$、有效答案 $y_i$、$m_i=\mathrm{none}$ 和 $q_{i+1}=\emptyset$，图的确定性更新规则本身不参与学习。

> 直观理解：教师展示的不只是答案，还展示每一步选什么证据、当前能回答什么、何时停止以及下一步问什么。学生因此学习的是完整的检索控制行为，使较轻量模型也能执行结构化决策。

**训练与推理**

训练时，教师对每个问题从 $q_1=x$ 开始，重复执行候选收集、自适应证据选择、局部作答、缺口判断和图更新，得到长度为 $L_\xi$ 的轨迹；学生在相同的 $(x,q_i,H_i,C_i)$ 条件下，通过教师强制学习复现 $o_i$。推理时无需教师：学生策略从初始问题出发，每轮检索段落并经 $\mathcal{I}$ 取得对齐的句子和三元组，选择首个充分的证据粒度，生成节点并判断是否停止；若继续，则以针对 $m_i$ 的 $q_{i+1}$ 进入下一轮，若停止，则返回 $y_i$ 与轨迹。达到预算 $B$ 仍未解决时，最终解析器只汇总已选择证据而不重新引入未选候选，从而限制噪声继续累积。

**复现信息**

复现时最关键的约束有四项。第一，检索只对段落向量执行，句子和三元组必须通过 $\mathcal{I}$ 从前 $N_P$ 个段落中收集，否则会改变方法所依赖的跨粒度对齐条件。第二，候选生成按段落排名和段内原始顺序遍历，去重后截断到 $N_S$ 和 $N_T$；证据选择则固定采用从三元组到句子再到段落的细到粗充分性判断。第三，历史 $H_i$ 不只是证据拼接，还应包含先前查询、中间答案、已解决路径、剩余需求和转移关系；每个节点最多生成一个下一查询，因此在线图保持为有向路径。第四，需要同时实现答案感知停止、最大步骤预算 $B$ 和预算耗尽后的最终解析器，并保存每轮查询、所选证据、局部答案、缺口和转移关系，以便得到与论文定义一致的可追踪输出。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 2WikiMultiHopQA：多跳问答基准。实验从该基准中以随机种子42无放回抽取1,000个问题，作为评估不同系统整合分散证据能力的测试集；原文节选未进一步说明所用官方划分。
- HotpotQA：要求联合多个证据回答问题的多跳问答基准。实验同样使用固定的1,000题子集，用来检验方法在另一种常用多跳问题分布上的泛化表现；原文节选未明确说明是否使用支持事实标注或何种官方划分。
- MuSiQue：强调组合式、多步推理的问答基准，同样评测固定的1,000题子集。作者指出其问题通常需要更长的组合链，因此该数据集既用于主结果比较，也用于目标条件化转移关系的集中消融。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Token-level F1**

根据预测答案与标准答案之间的词元级精确率和召回率计算调和平均值，允许答案部分匹配，因而能衡量预测覆盖正确答案内容的程度。 （越高越好，因为更高的F1表示预测与标准答案在词元层面具有更充分且更精确的重合。）

</div>
<div class="metric-item" markdown="1">

**Exact Match（EM）**

衡量规范化后的预测答案是否与标准答案完全一致，比词元级F1更严格，不为部分正确答案提供分数。 （越高越好，因为更高的EM表示更多问题被完整、精确地回答。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3-8B，2WikiMultiHopQA

<div class="result-value" markdown="1">

MEGRAG相对该数据集最强基线的F1和EM分别提高5.84点和7.50点，并在对应比较中取得最高观测值。

</div>

该结果表明，在固定评测子集和共享骨干下，MEGRAG的完整系统比参评基线更准确，且严格完全匹配指标的提升更明显。但各系统沿用各自发表时的训练方案，因此不能把全部差距都归因于多粒度证据图或某个单独模块；原文还指出配对自助法区间支持Qwen3-8B比较，但相关区间未出现在当前节选中。

<div class="result-source" markdown="1">

来源：Table 1；Main Results on Multi-hop QA

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

With Qwen3-8B, its F1/EM margins over the strongest per-dataset baseline are 5.84/7.50, 2.90/2.70, and 8.34/9.10 on 2WikiMultiHopQA, HotpotQA, and MuSiQue.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3-8B，HotpotQA与MuSiQue

<div class="result-value" markdown="1">

在HotpotQA上，MEGRAG相对最强基线的F1/EM优势为2.90/2.70点；在MuSiQue上优势扩大到8.34/9.10点。

</div>

跨数据集均为正的优势说明改进并非只出现在单一问题分布上。MuSiQue上的增益最大，与作者关于“更长组合链更需要持续跟踪未解决目标”的解释一致，但这只是由数据集特性和结果模式支持的分析，不能单凭分数证明长链推理就是增益的唯一原因。

<div class="result-source" markdown="1">

来源：Table 1；Main Results on Multi-hop QA

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

With Qwen3-8B, its F1/EM margins over the strongest per-dataset baseline are 5.84/7.50, 2.90/2.70, and 8.34/9.10 on 2WikiMultiHopQA, HotpotQA, and MuSiQue.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 提示式Qwen3-Max，不使用轨迹蒸馏

<div class="result-value" markdown="1">

MEGRAG相对各数据集最强基线的F1/EM优势依次为：2WikiMultiHopQA上1.92/1.10点、HotpotQA上3.34/1.20点、MuSiQue上5.21/6.30点。

</div>

在不对Qwen3-Max进行轨迹微调、仅通过提示执行MEGRAG推理流程时，三个基准仍出现正向观测增益，说明效果并非完全由Qwen3-8B的轨迹蒸馏造成。不过作者明确限制了显著性结论：全部F1增益和MuSiQue的两项增益显著，而前两个数据集的EM增益不显著，因此不能声称所有指标都稳定优于基线。

<div class="result-source" markdown="1">

来源：Table 1；Main Results on Multi-hop QA

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

With prompt-only Qwen3-Max, the respective margins remain 1.92/1.10, 3.34/1.20, and 5.21/6.30, showing that the inference procedure remains effective without trajectory distillation.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前节选虽声明实验覆盖自适应证据粒度与检索深度、停止效率、证据充分性审计和失败分析，但除转移关系外未给出这些实验的完整数值或案例。因此无法从所供材料核验图3中的LLM调用节省、词元节省、F1变化，也不能判断所选证据是否总能独立复现答案。
- 每个基准仅评测固定随机种子42抽取的1,000题，且Qwen3-8B主比较允许各基线采用其原生训练制度。固定子集有利于公平复现，但单次抽样可能限制对完整测试分布的代表性；训练监督不匹配则使主结果更适合作为端到端系统比较，而非严格的架构归因实验。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Direct Model与NativeRAG：前者检验不依赖外部检索时生成骨干自身的问答能力，后者代表一次性检索增强生成；它们共同构成判断多步检索是否必要的基础参照。
- MetaRAG、DualRAG与CIRAG：代表迭代式或自适应式RAG，用于比较MEGRAG的中间回答、缺失信息识别和动态继续检索机制是否优于已有多步检索流程。
- HippoRAG 2、NeocorRAG、HGRAG、LogicRAG与QAFD-RAG：作者将其归为结构感知方法，用于判断路径化多粒度证据图相对其他结构化证据或推理组织方式是否更有效。节选未逐一解释这些基线的内部机制。
- MGranRAG：多粒度RAG基线，是检验MEGRAG收益是否仅来自同时使用不同证据粒度的最直接对照；两者的差异还涉及证据对齐、目标条件化状态转移和答案感知停止。

**实验想回答的问题**

- RQ1：在统一评测子集、检索语料和生成骨干的条件下，MEGRAG能否比直接生成、常规RAG、迭代或自适应RAG、结构感知RAG及多粒度RAG取得更高的多跳问答准确率？同时，提示式Qwen3-Max实验用于检验这种收益是否在没有轨迹蒸馏时仍然存在。
- RQ2：MEGRAG的关键设计是否真正发挥作用？重点考察目标条件化的转移关系是否帮助模型跟踪跨跳推理中尚未解决的信息，并结合原文规划的粒度适应、检索深度和停止效率分析评估系统为何有效。当前节选仅提供了转移关系消融的完整数值，未提供粒度、深度及停止效率的具体结果。

**实验实现**

所有方法在两个骨干设置内共享相同的推理与回答模型，并使用同一随机种子42抽取的每基准1,000题子集、相同检索语料、预处理和评测脚本。默认检索器为NV-Embed-v2，稳健性研究另用BGE-small-en-v1.5；查询和段落由检索器编码，句子与三元组候选则从已检索段落通过跨粒度对齐索引取得，而非独立向量检索。迭代方法每步检索10个段落，最多进行4步；MEGRAG设置$N_P=10$，句子和三元组候选预算为$N_S=N_T=30$。Qwen3-Max还负责离线开放信息抽取和生成蒸馏轨迹：作者从官方训练集的3,000个、与评测不重叠的问题生成轨迹，并在单张H800上用LoRA微调Qwen3-8B。需要注意，Qwen3-8B主表比较的是遵循各自原生训练方案的完整系统，而不是监督条件完全匹配的纯架构比较；Qwen3-Max则以提示方式运行相同推理流程，用于削弱蒸馏带来的混杂。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 提示式Qwen3-Max在MuSiQue上移除目标条件化转移关系$ r_i $ | 移除$ r_i $后，F1由62.01降至60.40，EM由51.80降至50.20，即分别下降1.61和1.60点。 | 该变体保留其他推理状态字段、检索器、候选预算、停止策略和推理预算，只删除表示当前推理目标如何转向下一缺失信息的$ r_i $，因此较集中地检验“显式转移关系是否有用”。下降说明模型受益于这一字段；由于所有变体均为提示式运行，差异不能归因于轨迹微调。 | Table 2；Goal-conditioned Transition Analysis<br><span class="experiment-evidence">The F1/EM losses are 1.61/1.60 and 2.91/3.20, respectively.</span> |
| 提示式Qwen3-Max在MuSiQue上将目标条件化转移关系$ r_i $替换为无关关系 | 打乱关系后F1为59.10、EM为48.60，相对完整MEGRAG的62.01/51.80分别下降2.91和3.20点。 | 该实验不删除关系字段，而是提供内容无关的关系。其损失大于直接移除，表明后续决策依赖关系所表达的具体目标内容，而非仅从“存在一个额外字段”中获益；无关信息还可能误导后续查询与停止判断。该结论只在MuSiQue和Qwen3-Max提示设置上得到直接验证。 | Table 2；Goal-conditioned Transition Analysis<br><span class="experiment-evidence">Shuffled Transition Relation \| 59.10 \| 48.60 \| −2.91</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出面向多跳问答的迭代式 RAG 框架，通过多粒度证据图、缺失信息判断和自适应检索支持逐步推理。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`0fe7ebc047e8e750c3e05f13484d16f53173f103c6a1ca9352eb6cb5df61a937`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
