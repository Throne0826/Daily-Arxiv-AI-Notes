---
title: "[论文解读] CMT-RAG: Complementary Memory Traces for Multi-turn Multi-hop RAG"
description: "[arXiv 2607.26470][LLM Agent] 本文针对多轮对话中需要跨轮复用中间推理与证据的多跳问答，提出以“子问题级推理轨迹”而非原始对话历史作为检索记忆，并通过 CMT-RAG 与 MuMu-QA 分别提供实现框架和评测基准。"
arxiv_id: "2607.26470"
announcement_date: "2026-08-03"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-03T02:15:54.788858+00:00"
source_sha256: "7c1beb058fee03bdb7c03762fa8e2155053f68cf6d5775fd4140a4f117c73c99"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "检索增强生成"
  - "多轮多跳问答"
  - "跨轮子问题依赖"
  - "互补记忆轨迹"
  - "轨迹有向无环图"
  - "MuMu-QA"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2607.26470</p>

# CMT-RAG: Complementary Memory Traces for Multi-turn Multi-hop RAG

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-03</span>
<span><strong>作者</strong> Lang Zhou, Yingjian Chen, Shuxuan Li, Kun-Yu Lin, Zhilin Zhao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Sun Yat-sen University；The University of Hong Kong</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26470) · [PDF 下载](https://arxiv.org/pdf/2607.26470) · **关键词** 检索增强生成, 多轮多跳问答, 跨轮子问题依赖, 互补记忆轨迹, 轨迹有向无环图, MuMu-QA<br>


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

本文针对多轮对话中需要跨轮复用中间推理与证据的多跳问答，提出以“子问题级推理轨迹”而非原始对话历史作为检索记忆，并通过 CMT-RAG 与 MuMu-QA 分别提供实现框架和评测基准。

**不用术语来说**：用户连续提问时，后续问题常省略已经说过的实体，或要求在前面答案的基础上继续查询另一种属性；而一个问题本身还可能需要查找多段材料才能回答。现有系统通常只保留整段聊天记录、改写后的单个问题或粗略摘要，因此难以准确定位“前面哪一步推理、哪个实体以及哪段证据”应当被当前问题复用。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 CMT-RAG：将每个历史推理步骤保存为可寻址的互补记忆轨迹，轨迹绑定已解析的子问题、跨轨迹依赖、检索关键词、支持证据与子答案；同时以循环状态维持局部对话连续性，以会话级有向无环图保存长期依赖，使无状态阅读器只接收当前所需的子问题和证据。
- 构建 MuMu-QA：把多跳问题重组为具有跨轮依赖的对话，并提供对话范围的子问题标识、轨迹关键词、依赖边、支持段落标识和完整轨迹图监督，以直接评测跨轮子问题依赖恢复，尤其覆盖长对话条件。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

检索增强生成（RAG）先从非结构化语料库中寻找证据，再让语言模型依据证据回答问题。本文关注更困难的多轮、多跳会话场景：用户会省略已出现的实体，并基于先前答案继续追问；与此同时，一个问题可能需要拆成多个相互依赖的子问题，经若干次检索才能回答。传统系统通常把记忆保存为完整对话、查询改写结果或非结构化摘要，但检索实际需要的是某个先前子问题得到的实体、推理依赖及其证据，因此本文将任务重新表述为会话级“推理轨迹有向无环图”的增量构建。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多跳检索与推理**

单次检索不足以直接回答问题，系统必须先解决中间子问题，再利用中间答案检索后续证据。例如先确定某作品的作者，再查询该作者的出生地。

</div>
<div class="concept-item" markdown="1">

**跨轮依赖**

当前问题的缺失实体或检索目标需要由较早轮次中的推理结果补全。本文区分谓词扩展（查询先前目标的新属性或关系）与实体引用（直接复用先前引入的实体）两类典型依赖。

</div>
<div class="concept-item" markdown="1">

**轨迹有向无环图**

系统把每个可检索的子问题及其关键词、前置依赖和证据保存为一个轨迹节点，并用有向边表示节点间的依赖关系。图中不允许形成环，因此后生成的轨迹只能依赖此前已有的轨迹。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定非结构化语料库 $\mathcal{C}$ 和按时间排列的用户查询序列 $\mathcal{D}=\langle q_1,q_2,\ldots,q_T\rangle$，系统需要在每一轮 $t$ 输出由语料证据支撑的答案 $a_t$。一个查询可以包含多个检索相关子问题，并依赖较早轮次解析出的主体或实体；系统因而需要把当前查询分解成轨迹草稿，根据已有图 $\mathcal{G}_{<t}$ 解析跨轮依赖、检索支持段落，并将完成的轨迹增量 $\Delta\mathcal{G}_t$ 写入会话级图。每个轨迹将自然语言子问题、用于历史查找的关键词、前置轨迹编号和直接检索到的段落编号绑定起来，使后续轮次能够选择特定历史推理步骤并复用其证据，而不必重新解释全部对话历史。MuMu-QA 是该问题设定的基准实例，由 MuSiQue 的子问题分解、中间答案与支持段落构造，并额外提供跨轮子问题依赖及完整轨迹图监督。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{C}$**

供系统检索证据的非结构化语料库。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{D}=\langle q_1,q_2,\ldots,q_T\rangle$**

包含 $T$ 个用户轮次的有序对话，其中 $q_t$ 是第 $t$ 轮查询。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{G}=(\mathcal{V},\mathcal{E}_{\mathcal{G}})$**

会话级轨迹有向无环图；$\mathcal{V}$ 是轨迹及其答案构成的节点集合，$\mathcal{E}_{\mathcal{G}}$ 是跨轨迹依赖边集合。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{T}_k=(q_k^{\mathrm{sub}},kw_k,\mathrm{deps}(k),\mathrm{para\_ids}_k)$**

第 $k$ 条检索级记忆轨迹，依次包含子问题、查找关键词、前置轨迹集合和直接检索到的段落编号。

</div>

</div>

**直接相关的工作**

- **MuSiQue（Trivedi et al., 2022）**: MuMu-QA 的构造来源；本文利用 MuSiQue 已有的多跳问题分解、中间答案和支持段落，进一步合成具有显式跨轮依赖的会话。
- **查询改写式会话检索（Anantha et al., 2021；Mo et al., 2023；Zhu et al., 2025a）**: 这类方法把依赖上下文的追问改写为独立查询，适合处理局部指代，但会把多步依赖压缩进单个查询，不能显式保存可供后续检索复用的中间目标、依赖关系与证据。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

扩展式信息检索对话同时包含两种困难：用户会省略重复实体或在先前结果上继续追问，形成跨轮依赖；回答当前问题又可能需要把任务拆成多个相互依赖的子问题并检索多段证据。系统因而不仅要理解当前轮，还必须找到某个历史推理步骤中已经确定的对象或实体，并复用当时支撑该结论的证据。若只能重新解释全部对话历史，长对话中的依赖定位与证据恢复就会变得低效且不稳定。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **查询改写与当前轮查询分解**：查询改写把依赖上下文的当前问题补全为可独立检索的查询，适合解决局部指代；查询分解则把复杂问题拆成若干子问题，按子问题之间的关系执行多跳检索。两者主要围绕当前查询构造检索请求。
- **对话记忆与对话图建模**：记忆式系统保存原始历史、摘要或向量表示，以便后续轮次读取上下文；对话图方法显式表示话语之间的关系。它们通常把整轮话语或整段对话作为记忆单位，而不是保存一次检索推理所对应的子问题、依赖对象和支持证据。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 查询改写会把跨轮依赖链压缩进一个独立查询，导致中间检索目标不可见；查询分解虽然暴露当前轮的多跳结构，却通常假设问题自包含、依赖仅发生在当前轮内。因此，当后续问题扩展或复用先前子问题的实体时，系统难以明确指出应连接哪个历史推理节点。
- 历史、摘要、嵌入和话语级图主要提供轮次级上下文，没有显式编码检索所需的子问题级跨轮依赖，也未将历史结论与其支持证据绑定。其后果是检索器需要的记忆粒度与系统实际保存的记忆粒度不一致，只能从全局历史中再次推断相关步骤，且现有多轮 RAG 基准也缺少相应的依赖标注来直接评测这一能力。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种与检索过程同粒度的对话记忆表示：它应把历史子问题变成可寻址对象，明确记录当前子问题依赖哪个先前步骤，并保留该步骤成立所依据的证据；同时还需要一个具有子问题级跨轮依赖监督和长对话划分的基准，以区分真正的长期依赖恢复与简单的短历史重放。

</div>
<div markdown="1"><span>核心问题</span>

能否把多轮对话记忆组织成带依赖边和证据绑定的子问题级推理轨迹，并结合维护近期语境的循环状态，使系统在不把完整历史交给阅读器的情况下，准确恢复跨轮先决步骤、组装新旧证据并提高多跳问答准确率？

</div>
<div markdown="1"><span>作者直觉</span>

检索实际处理的是具体子问题，而不是抽象的整轮对话，因此记忆也应采用相同粒度。若把一次历史推理封装为包含“问了什么、依赖谁、用过什么证据”的轨迹，后续追问就不必重新理解全部聊天记录，只需沿依赖边或关键词找到相关轨迹，再把其中的历史证据与当前新检索证据临时组合。循环状态负责最近几轮的语境衔接，持久轨迹图负责较远的显式依赖，两种记忆各自处理不同时间尺度。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CMT-RAG将多轮、多跳对话检索建模为“轨迹有向无环图”持续归纳：系统不把整段历史反复交给回答模型，而是将当前问题拆成若干结构化记忆轨迹；每条轨迹包含子问题、检索关键词、对既有轨迹的依赖以及证据段落标识。轻量级状态空间模型在轮次间传递循环状态，用于生成轨迹草稿；系统再通过持久化轨迹图消解跨轮引用、复用远距离证据，并为每个已消解子问题检索新段落。完成的轨迹写回图中，最后由无状态阅读器仅依据已消解子问题和合并后的证据生成当前轮答案。
直观而言，该方法把对话记忆分成两种互补渠道：循环状态像“工作记忆”，压缩近期对话并帮助理解当前问题；轨迹图像“可检索笔记本”，长期保存已经解决的子问题及其证据。前者避免每轮重读全部历史，后者避免仅靠压缩状态而遗忘早期实体和材料。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 轨迹草稿生成

基于Mamba-2状态空间模型更新跨轮循环状态，并将$q_t$分解为有序的结构化轨迹草稿；每个草稿至少预测自然语言子问题$q_k^{\text{sub}}$、关键词$kw_k$和对先前轨迹的依赖$\mathrm{deps}(k)$。

<div class="method-step__io" markdown="1">

**输入**：当前轮查询$q_t$、上一轮状态空间模型的循环状态$h_{t-1}$，以及生成器已接收的会话信息。<br>
**输出**：当前轮的一组有序轨迹草稿及更新后的循环状态。

</div>

**直观理解**：生成器先判断当前问题包含几个需要分别检索的小问题，并写下每个小问题可能依赖哪条旧结论。循环状态相当于随对话更新的简短工作记忆。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 依赖引用消解与轨迹图访问

系统把草稿中预测的依赖链接到既有轨迹节点，以取得依赖节点所引入的实体或主题；除显式依赖访问外，还可根据轨迹关键词重叠额外查找至多一条相关旧轨迹。

<div class="method-step__io" markdown="1">

**输入**：当前轮轨迹草稿，以及此前累积的轨迹有向无环图$\mathcal{G}_{<t}$。<br>
**输出**：依赖已消解的子问题，以及从旧轨迹中复用的答案、关键词和支持段落。

</div>

**直观理解**：如果新问题说“该公司”或需要上一轮的中间答案，系统会沿图中的边找到它真正指向的实体。关键词查找则像翻阅旧笔记的索引，用于找回并非紧邻当前轮但仍有用的材料。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 新证据检索与轨迹补全

系统以每个已消解子问题为检索单元，默认使用DRAGON检索$k_{\mathrm{local}}=5$个新段落；随后合并新检索证据与旧轨迹证据、去重，并把实际使用的段落标识写入$\mathrm{para\_ids}_k$。

<div class="method-step__io" markdown="1">

**输入**：依赖已消解的子问题、DRAGON语料索引、依赖轨迹或关键词命中轨迹中保存的证据。<br>
**输出**：包含子问题、关键词、依赖和段落标识的完整轨迹，以及供阅读器使用的去重证据集合。

</div>

**直观理解**：系统既查找解决当前小问题的新资料，也重复利用旧笔记里已经验证过的资料。这样无需把固定数量的大段历史全部塞给阅读器。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 无状态阅读与记忆写回

无状态阅读器不重放完整对话历史，而仅使用已消解子问题和检索证据回答各子问题并形成最终答案$a_t$；完成的轨迹及其答案作为$\Delta\mathcal{G}_t$追加到持久化轨迹图。

<div class="method-step__io" markdown="1">

**输入**：依赖已消解的子问题、合并去重后的证据段落，以及当前轮全部完整轨迹。<br>
**输出**：当前轮最终答案$a_t$和更新后的会话级轨迹图$\mathcal{G}_{\le t}$。

</div>

**直观理解**：大型阅读器只处理当前真正需要的问题和证据，长期记忆管理交给更轻量的生成器与图结构。新得到的中间结论随后变成可供未来轮次调用的笔记。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 会话级轨迹有向无环图

$$
\mathcal{G}=(\mathcal{V},\mathcal{E}_{\mathcal{G}})
$$

**符号说明**

- $\mathcal{G}$：整个会话持续构建的轨迹有向无环图。
- $\mathcal{V}$：节点集合；每个节点由一条轨迹及其答案$(\mathcal{T}_k,a_k)$组成。
- $\mathcal{E}_{\mathcal{G}}$：依赖边集合；边$(\mathcal{T}_j,\mathcal{T}_i)$表示轨迹$\mathcal{T}_i$依赖轨迹$\mathcal{T}_j$引入的实体或主题。
- $\mathcal{T}_k$：第$k$个子问题对应的结构化记忆轨迹。
- $a_k$：轨迹$\mathcal{T}_k$对应的答案或中间结论。

<div class="equation-explanation" markdown="1">

**直观理解**：该式规定长期记忆不是一串原始对话，而是一张保存推理依赖的图。图结构使系统能够沿依赖边定位前置结论，并在相隔很多轮后再次取回相应证据。<br>
**原文位置**：第2.1节，公式(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 结构化记忆轨迹

$$
\mathcal{T}_{k}=\bigl(q_{k}^{\text{sub}},\ kw_{k},\ \mathrm{deps}(k),\ \mathrm{para\_ids}_{k}\bigr)
$$

**符号说明**

- $\mathcal{T}_k$：第$k$条可被生成、检索、链接和写回的记忆单元。
- $q_k^{\text{sub}}$：交给检索器和阅读器处理的自然语言子问题。
- $kw_k$：用于轨迹图关键词查找的检索锚点。
- $\mathrm{deps}(k)$：前置轨迹编号集合，满足$\mathrm{deps}(k)\subseteq\{1,\ldots,k-1\}$。
- $\mathrm{para\_ids}_k$：为该子问题直接检索并保存的语料段落标识集合。

<div class="equation-explanation" markdown="1">

**直观理解**：一条轨迹同时回答四个操作问题：要检索什么、用什么词查旧记忆、依赖哪些旧结论、证据存在哪里。因此它比整轮话语或无结构摘要更容易被后续检索与回答流程直接使用。<br>
**原文位置**：第2.1节，公式(3)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文节选未给出三阶段监督微调或直接偏好优化的完整损失公式，因此不应补造目标函数。已明确的信息是：生成器先以线性化的金标准轨迹为自回归目标进行三阶段监督微调，阶段2和阶段3检查点仅按轨迹目标上的自回归验证损失选择；随后进行一个预先设定轮数的、面向具体阅读器的直接偏好优化，奖励权重为$\gamma=0.2$。两种阅读器分别使用由对应阅读器生成的偏好对训练适配器，所以实验检验的是对不同阅读器的兼容性，而不是未经适配的零样本阅读器替换。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 循环式SSM轨迹生成器**

生成器以Mamba-2-2.7B为初始化骨干，在轮次间保留循环状态$h_t$，并自回归生成统一格式的轨迹草稿。训练采用三阶段监督微调课程，之后针对具体阅读器进行直接偏好优化；其职责是对话解析、子问题分解和依赖预测，而不是直接承担最终证据阅读。

> 直观理解：状态空间模型无需每轮重新编码全部历史，因而适合维护随轮次更新的短期语义状态。它负责把含糊的对话问题整理成可检索任务，让昂贵的阅读器专注于依据证据回答。

**2. 持久化轨迹DAG**

轨迹图$\mathcal{G}=(\mathcal{V},\mathcal{E}_{\mathcal{G}})$以“轨迹及其答案”为节点，并以有向边表达后续轨迹对先前实体或主题的依赖。图支持显式依赖访问和基于$kw_k$的关键词重叠查找，节点还保存$\mathrm{para\_ids}_k$以便直接复用历史证据。

> 直观理解：单一压缩状态可能在长对话中遗失细节，轨迹图则把重要中间问题、答案和来源显式保存。图中的边说明结论之间如何相接，因此系统能准确回到早期证据，而不是只依赖模糊的对话摘要。

**3. 检索—阅读解耦模块**

DRAGON以已完成引用消解的$q_k^{\text{sub}}$为查询，从共享非结构化语料$\mathcal{C}$检索段落；系统将这些新段落与DAG返回的历史证据合并去重，再交给Qwen3-32B或Llama-3.3-70B-Instruct等无状态阅读器。最终阅读器上下文不要求包含累计问答历史。

> 直观理解：先把代词和依赖实体弄清楚，再检索，通常比直接拿含糊的当前问句搜索更有针对性。阅读器看到的是整理后的问题与证据，而不是冗长且可能分散注意力的完整聊天记录。

**训练与推理**

训练时，方法以Mamba-2-2.7B初始化轨迹生成器，并通过LoRA适配器学习将对话输入线性化为结构化轨迹。监督来自MuMu-QA：该数据利用MuSiQue已有的子问题分解、中间答案和支持段落，并通过“子问题迁移”制造跨轮依赖、通过“图拼接”连接两条推理链；短对话和长对话划分用于训练。三阶段监督微调后，再以对应最终阅读器产生的偏好数据执行直接偏好优化；检查点选择不使用最终问答的EM/F1、GoldCtx或效率指标。
推理时，第$t$轮首先将$q_t$与$h_{t-1}$输入SSM生成轨迹草稿，再针对$\mathcal{G}_{<t}$消解依赖并进行关键词DAG查找。系统对每个已消解子问题执行局部检索，合并新证据和历史轨迹证据、去重并补全轨迹；无状态阅读器在不重放完整对话的条件下生成$a_t$，随后把完整轨迹和答案追加到图中，并将更新后的SSM状态传给下一轮。该流程中SSM状态主要承担连续语义记忆，DAG主要承担可寻址、可复用的长期证据记忆。

**复现信息**

公平解释结果所需的默认配置为：局部检索器采用共享DRAGON索引，每个已消解子问题固定检索$k_{\mathrm{local}}=5$个段落，并通过关键词重叠最多额外访问一条轨迹；合并证据后去重，因此每轮实际阅读上下文大小取决于生成的子问题数量，而不等于单次检索深度。MuMu-QA实验使用贪心轨迹生成、跨轮SSM状态传递和依赖式DAG访问。CMT-RAG及Oracle轨迹版本不在开发集上搜索$k_{\mathrm{local}}$，而基线会在$k\in\{5,10,20\}$中按长对话开发集F1选择检索深度。
长对话划分包含548个对话、5396轮，并参与轨迹检查点选择，因此相应结果应视为开发集比较，而非独立同分布测试集估计。33–67轮的超长划分不参与训练、检查点选择或检索深度选择，专用于长度外推。延迟统计包含轨迹或计划生成、检索、中间阅读器调用和最终答案生成，但排除一次性的模型与索引初始化。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MuMu-QA：用于多轮、多跳检索增强问答评测。每个解析后的子问题通过 DRAGON 稠密检索器取得排名前 $5$ 的支持段落，再与依赖轨迹和关键词匹配所复用的历史段落合并、去重。所给节选未报告数据集规模、训练/验证/测试划分及具体样本统计。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

原文未明确报告，或这里不需要额外前置概念。

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给节选未包含第 4 节实验正文中的数据表、基线、评价指标和得分，也没有报告方差、置信区间或显著性检验；因此主结果与消融结果均不能从现有材料可靠重建，任何性能优越性结论都需要回查完整论文。
- 远距离轨迹查找采用固定的词面集合相似度和阈值 $s>0.05$，且最多保留一个候选，不进行词干化、语义匹配或频率加权。这种设计实现简单，但可能漏掉同义改写，也可能因少量共有词引入无关历史证据；节选没有提供阈值敏感性、候选数量或词法匹配组件的消融结果。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。

**实验想回答的问题**

- 在多轮、多跳问答中，将显式跨轮依赖解析与基于关键词的远距离历史轨迹查找结合起来，能否恢复相关历史证据，并为无状态阅读器构造有效上下文？
- 状态空间模型式的有状态轨迹生成能否在不重放完整对话历史的条件下逐轮处理当前输入，从而支持更高效的多会话推理？

**实验实现**

推理时先读取生成轨迹中保存的依赖标识符，从会话有向无环图中取回被引用轨迹，并把其中间答案代入占位符，得到解析后的子问题。除显式依赖外，系统还在同一对话中搜索早于最近十轮窗口的已完成轨迹：关键词被转为小写，并以 Unicode 正则表达式“$\w+$”分词成集合；候选相似度采用二元余弦，即 Ochiai 系数。系统不做词干化、额外停用词删除或词频加权，并排除已经通过近期显式依赖访问的轨迹；候选按相似度降序排列，同分时按整数轨迹标识符升序打破平局，仅保留满足严格阈值 $s>0.05$ 的最高排名候选。其历史段落与 DRAGON 返回段落按段落标识符合并去重，再交给无状态阅读器。阅读器只能依据给定证据输出最短答案片段或 yes/no；最终答案仅使用当前轮用户问题和当前轮推理步骤聚合。默认批大小为 $8$、并发请求上限为 $32$、最大生成长度为 $512$ 个 token；支持显式思考模式的模型在子问题回答和最终生成阶段均关闭该模式。有状态轨迹生成采用 BF16、贪心解码和每轮最多 $512$ 个生成 token，保留跨轮循环状态；多会话服务最多批处理 $16$ 个并发会话，并使用打包循环缓存、GPU 常驻解码缓冲区和 CUDA Graph。所给节选没有提供评价指标、比较模型配置或统计显著性协议。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 图 7 展示了一个 MuMu-QA 实例：当前轮首先被分解为带显式依赖和关键词的结构化轨迹，系统同时解析预测依赖并通过关键词恢复会话有向无环图中的历史轨迹节点，随后汇总新检索与复用证据，由无状态阅读器生成答案。原文表述为：“A real evaluation example from MuMu-QA. The current dialogue turn is first decomposed into structured traces with explicit dependencies and keywords. Dependency resolution combines the predicted dependency with a keyword-recovered historical trace node from the DAG, enabling evidence reuse across distant turns. The retrieved and reused evidence is then aggregated and passed to the stateless reader to produce the final answer.”该案例说明完整机制能够在单个实例中运行，但不能证明其普遍准确性，也不能替代定量结果或消融实验。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper proposes a memory-based RAG mechanism for retrieval across multi-turn interactions and multi-hop reasoning.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`7c1beb058fee03bdb7c03762fa8e2155053f68cf6d5775fd4140a4f117c73c99`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
