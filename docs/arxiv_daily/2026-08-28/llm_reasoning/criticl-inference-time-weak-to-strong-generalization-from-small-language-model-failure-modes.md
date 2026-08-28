---
title: "[论文解读] CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes"
description: "[arXiv 2608.27455][LLM Reasoning] CritICL将小模型反复出现的结构化错误转化为可复用的批评式上下文示例，以较低推理开销帮助同一家族的更强模型规避常见推理陷阱。"
arxiv_id: "2608.27455"
announcement_date: "2026-08-28"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:34:56.377211+00:00"
source_sha256: "999f040c4d0c6165e5bbabcfde88aa756b46f05c98e179a98525f51146f38e44"
tags:
  - "LLM Reasoning"
  - "LLM 效率"
  - "LLM 其他"
  - "推理时扩展"
  - "弱到强泛化"
  - "失败模式"
  - "上下文学习"
  - "批评检索"
  - "大语言模型推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.27455</p>

# CritICL: Inference-Time Weak-to-Strong Generalization from Small Language Model Failure Modes

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Yufan Wu, Yinghui He, Zhengyi Hu, Lang Wei, Ruichen Li, Qifan Yang, Ting Zhu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: The Ohio State University；Affiliation: Princeton University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27455v1) · [PDF 下载](https://arxiv.org/pdf/2608.27455v1) · **关键词** 推理时扩展, 弱到强泛化, 失败模式, 上下文学习, 批评检索, 大语言模型推理<br>
**代码**: [https://github.com/umwyf/CRITICL](https://github.com/umwyf/CRITICL)

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

CritICL将小模型反复出现的结构化错误转化为可复用的批评式上下文示例，以较低推理开销帮助同一家族的更强模型规避常见推理陷阱。

**不用术语来说**：提高大语言模型推理能力通常需要让模型多次作答、反复修改，或调用另一个模型检查答案，这会增加生成次数、令牌消耗和计算成本。论文关注的是：能否预先整理较小模型经常犯什么错以及为什么错，再把这些经验作为提示提供给更强模型，使其一次或少数几次推理时就主动避开类似错误。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出以“失败模式”为弱到强迁移信号：作者观察到同一模型家族内，小模型与大模型的错误类型分布具有较强一致性，因此不再只利用弱模型给出的直接答案或在线指导，而是提取可跨模型规模复用的典型推理陷阱。
- 提出CritICL及其离线资源CritBank：CritBank记录问题、弱模型错误回答、失败模式标签和自然语言批评；推理时，动态版本按当前问题预测相关失败模式，静态版本按模型家族的整体失败画像检索批评示例，从而为目标模型提供失败感知的上下文指导。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型推理时增强与弱到强泛化的交叉方向。推理时增强是在不重新训练目标模型的前提下，通过提示、采样、批评或验证等操作提高其推理正确率；常见方法依赖多次生成、自我修正或外部验证器，因而增加推理调用与令牌成本。本文关注同一模型家族中不同规模模型可能共享的结构化错误模式，并尝试将小模型离线暴露出的常见推理陷阱转化为批评式上下文示例，以低额外成本指导更强模型。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**推理时扩展（inference-time scaling）**

在模型参数保持不变的情况下，为单个问题投入更多推理计算，例如重复采样、迭代修正或利用验证器筛选答案。它通常能提高准确率，但可能需要多次模型调用和较高令牌成本。

</div>
<div class="concept-item" markdown="1">

**弱到强泛化（weak-to-strong generalization）**

利用能力较弱模型提供的监督或指导来改善较强模型。本文不使用弱标签微调强模型，而是在推理阶段复用弱模型的失败信息。

</div>
<div class="concept-item" markdown="1">

**失败模式（failure mode）**

模型错误中反复出现、可归类且具有一定可预测性的推理缺陷，而非彼此无关的随机错误。本文假设同一家族的弱模型与强模型即使能力不同，也可能具有相近的失败模式分布。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个待求解问题、一个无需微调的目标大语言模型，以及离线构建的 CritBank，任务是在尽量减少额外生成和令牌消耗的条件下提高目标模型的推理表现。CritBank 的每条记录包含问题、弱模型的错误回答、失败模式标签和自然语言批评；推理时，系统依据当前输入可能触发的失败模式，或依据目标模型家族的全局失败模式画像，从 CritBank 选择批评式上下文示例，再让目标模型生成最终推理与答案。核心假设是：同一模型家族跨规模共享一定的结构化失败规律，因此小模型的错误可为大模型提供可迁移的避错信息；该设定属于纯推理时干预，不通过弱监督更新目标模型参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{B}_{\mathrm{crit}}$**

CritBank，即由弱模型错误、失败模式标签及相应批评组成的离线结构化资料库；该符号为便于说明而作的记号，原文节选未给出正式数学符号。

</div>
<div class="notation-item" markdown="1">

**$x$**

推理阶段输入目标模型的待求解问题；该符号为便于说明而作的记号，原文节选未给出正式数学符号。

</div>
<div class="notation-item" markdown="1">

**$f$**

与问题或模型家族相关的失败模式类别；该符号为便于说明而作的记号，原文节选未给出正式数学符号。

</div>
<div class="notation-item" markdown="1">

**$M_{\mathrm{target}}$**

接受检索到的批评式上下文并输出最终推理结果的目标强模型；该符号为便于说明而作的记号，原文节选未给出正式数学符号。

</div>

</div>

**直接相关的工作**

- **Self-Consistency（Wang et al., 2023）**: 代表通过多次采样并聚合候选解来提升推理表现的测试时扩展路线。它说明增加推理计算可以改善结果，也构成本文希望降低重复生成成本的直接参照。
- **Weak-to-Strong Generalization（Burns et al., 2024）**: 研究强模型能否从弱监督中获益，但主要面向训练时适配。CritICL 将问题改写为推理时弱到强迁移：不以弱标签微调目标模型，而把弱模型的结构化失败转化为可检索批评。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

推理时扩展虽然能提升大语言模型在数学等复杂任务上的表现，但通常需要重复采样、迭代修正或外部验证。其收益依赖额外模型调用与更长生成过程，因而在延迟、令牌成本或算力受限的应用中难以高效部署；研究需要一种能够复用既有错误知识、而不是为每个新问题持续增加生成次数的推理增强方式。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **传统推理时扩展**：对同一输入进行多次采样并聚合答案，要求模型反复自我改进，或借助外部验证器、评审模型判断候选答案，从额外计算中换取更可靠的推理结果。
- **弱模型在线指导强模型**：针对每个新输入调用较弱模型，让其即时生成监督信号、中间步骤或其他辅助信息，再将这些内容提供给较强模型，以实现推理阶段的弱到强泛化。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 传统推理时扩展往往要求模型自身或更强评审模型进行多次生成，直接增加推理延迟和令牌成本；因此，性能提升与计算开销紧密绑定。
- 已有弱到强推理方法通常为每个输入在线调用弱模型，并依赖其直接输出的质量；这既保留了额外推理开销，也没有充分利用弱模型错误中更稳定、更可迁移的结构化信息。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法尚未把弱模型的系统性失败整理成可离线构建、可重复检索的知识资源，也未充分回答这些失败模式能否跨同一家族的模型规模迁移，并以批评式上下文指导更强模型。缺少的是一种同时利用“弱模型如何失败”与低额外调用成本的推理机制。

</div>
<div markdown="1"><span>核心问题</span>

能否在仅增加很少推理成本的条件下，利用较弱模型的结构化失败模式，在推理时提升较强模型的推理表现？

</div>
<div markdown="1"><span>作者直觉</span>

模型的错误并非完全随机：同一家族模型即使参数规模和总体能力不同，也可能反复落入相似的推理陷阱。小模型更容易暴露这些陷阱，因此可被视为一种低成本的“错误探测器”。若预先用高能力模型把小模型错误归类并写成明确批评，再为新问题检索最相关的错误案例，强模型就能像阅读错题分析一样，在作答前获得针对性的避错提示，而不必依靠大量重复尝试。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CritICL是一种不更新目标大模型参数的推理时弱到强泛化方法。它先离线收集同一模型家族中多个小模型的错误推理，为每个错误归纳结构化的“失败模式”标签并生成自然语言批评，由此建立CritBank；面对新问题时，再按可能出现的失败模式检索至多五个带批评的错误示例，将其作为上下文交给更强的目标模型。输入是待解问题，核心操作是失败风险识别、按错误类型检索和批评式上下文学习，最终输出是目标模型的一次完整推理与答案，而不是对多个候选答案进行投票或外部验证。

该方法有动态与静态两个版本。CritICL-dynamic先让目标模型针对当前问题预测至多五种可能的失败模式，再据此检索，因此指导更具问题针对性，但需要一次额外模型调用；CritICL-static则根据同一家族弱模型的总体错误分布预先形成全局失败模式画像，直接检索相应示例，因而每题只需一次目标模型生成。直观地说，CritICL不是只展示“别人如何做对”，而是把弱模型反复犯过的典型错误及其纠正意见当作警示牌，让强模型在作答前知道哪些推理陷阱最值得避开。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 生成弱模型推理并筛选错误响应

对每个问题—模型组合$(q,m)\in\mathcal{Q}\times M$使用思维链提示生成五个包含中间推理和最终答案的响应，并通过正确性函数$\phi(q,r)\in\{0,1\}$划分正确与错误子集。后续只保留$R_{\text{incorrect}}(q,m)$中的响应，因为它们直接暴露模型的推理缺陷。

<div class="method-step__io" markdown="1">

**输入**：问题集合$\mathcal{Q}$，以及属于同一模型家族的小语言模型集合$M$。<br>
**输出**：带有来源问题与弱模型信息的错误推理集合，以及作为质量控制结果的正确／错误划分。

</div>

**直观理解**：这一步相当于让若干低年级学生反复解题，然后只收集其错题过程。方法关心的不只是错误答案，而是错误答案背后的推理路径。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 归纳失败模式并生成针对性批评

使用前沿语言模型为每个错误响应提出至多五个候选失败模式标签，再对语义相近或冗余标签进行聚类，得到代表性的错误类型；同时为$(q,r)$生成指出具体推理问题的自然语言批评$\mathcal{C}(q,r)$。除非另有说明，标签与批评均由gpt-4o-mini生成。

<div class="method-step__io" markdown="1">

**输入**：每个错误问题—响应对$(q,r)$，其中$r\in R_{\text{incorrect}}(q,m)$。<br>
**输出**：每个错误响应对应的失败模式集合$\mathcal{L}(q,r)$及结构化批评$\mathcal{C}(q,r)$。

</div>

**直观理解**：标签回答“这是哪一类错误”，批评回答“这道题具体错在哪里、应注意什么”。聚类则把措辞不同但实质相同的错误名称合并，避免检索索引过于零散。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 建立可按失败模式查询的CritBank

将四元组$(q,r,l,\mathcal{C}(q,r))$组织为CritBank，并建立标签的逆向索引$\mathcal{L}^{-1}(l)$，使系统能够由某个失败模式直接找到所有相关错误示例及批评。一个$(q,r)$可被赋予多个标签，因此也可能出现在多个标签的候选池中。

<div class="method-step__io" markdown="1">

**输入**：问题$q$、错误响应$r$、失败模式标签$l$和批评$\mathcal{C}(q,r)$。<br>
**输出**：结构化错误知识库CritBank，以及从失败模式标签到带批评示例的检索入口。

</div>

**直观理解**：CritBank类似按“错误原因”编目的错题本，而不是仅按题目主题分类。这样，新题即使表面内容不同，只要可能触发相同的推理缺陷，也能找到有用警示。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 为新问题确定失败模式并选择示例

动态版本让目标模型针对$q'$预测至多五个可能的失败模式；静态版本则使用由同一家族弱模型失败模式分布聚合得到的全局画像。两者随后通过Failure Mode-Based Sample Selection从相应标签的候选池中检索至多五个信息性示例。

<div class="method-step__io" markdown="1">

**输入**：未出现在建库问题集合中的新问题$q'$、CritBank，以及选定的动态或静态策略。<br>
**输出**：与当前问题风险或模型家族共性风险相匹配的一组错误响应—批评示例。

</div>

**直观理解**：动态版本像根据当前题目临时列出“本题易错点”，静态版本像随身携带该模型家族最常犯错误的固定清单。前者更有针对性但多一次调用，后者更稳定且成本更低。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### CritBank数据集定义

$$
\operatorname{CritBank}(\mathcal{Q},M)=\left\{(q,r,l,\mathcal{C}(q,r))\;\middle|\;q\in\mathcal{Q},\ m\in M,\ r\in R_{\mathrm{incorrect}}(q,m),\ l\in\mathcal{L}(q,r)\right\}
$$

**符号说明**

- $\mathcal{Q}$：用于离线建库的输入问题集合。
- $M$：用于暴露失败模式、且与目标模型属于同一家族的小语言模型集合。
- $q$：建库问题集合中的一个问题。
- $m$：弱模型集合中的一个模型。
- $r$：弱模型针对问题生成的、包含中间推理和最终答案的响应。
- $R_{\mathrm{incorrect}}(q,m)$：模型对问题生成的响应中，被正确性函数判定为错误的子集。
- $l$：赋给某个错误问题—响应对的代表性失败模式标签。
- $\mathcal{L}(q,r)$：标注函数，为问题—错误响应对返回一个失败模式标签子集。
- $\mathcal{C}(q,r)$：批评函数，为问题—错误响应对生成结构化自然语言反馈。

<div class="equation-explanation" markdown="1">

**直观理解**：该式规定CritBank中一条记录必须来自弱模型的错误响应，并同时带有一个失败模式标签和针对该错误过程的批评。若同一错误对应多个标签，它会与各标签分别形成可检索记录，从而支持一条错误经验被多个风险类别复用。<br>
**原文位置**：第2.1节“Final Dataset”

</div>

</div>

<div class="equation-block" markdown="1">

#### 失败模式标签的逆向检索映射

$$
\mathcal{L}^{-1}(l)=\left\{(q,r)\;\middle|\;l\in\mathcal{L}(q,r)\right\}
$$

**符号说明**

- $\mathcal{L}^{-1}(l)$：与失败模式标签相关联的全部问题—错误响应对集合；这里表示逆向索引，而非数值函数的普通倒数。
- $l$：作为检索键的失败模式标签。
- $q$：产生相关错误案例的原始问题。
- $r$：与原始问题对应的错误推理响应。
- $\mathcal{L}(q,r)$：问题—错误响应对所拥有的失败模式标签集合。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把“给案例贴标签”的正向过程反过来使用：给定一个预计会出现的错误类型，系统可直接找到所有体现该错误的历史案例，并进一步取出对应的$\mathcal{C}(q,r)$。它是动态和静态版本连接风险判断与上下文示例选择的关键接口。<br>
**原文位置**：第2.1节“Final Dataset”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。CritICL不是参数训练或微调方法，论文没有定义用于更新目标模型、弱模型或检索器参数的损失函数；其“弱到强泛化”发生在推理上下文层面。离线阶段调用弱模型产生错误响应，并调用gpt-4o-mini生成标签与批评；在线阶段仅通过提示、标签预测和示例检索改变目标模型所见上下文，因此CritBank构建式和逆向映射是数据组织与检索定义，而不是可微优化目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. CritBank结构化错误知识库**

CritBank仅收录满足$\phi(q,r)=0$的弱模型响应，并将每条记录表示为问题、错误推理、代表性失败模式标签和细粒度批评的组合。知识库由与目标模型同家族的较弱模型构建，使检索信号针对该模型家族共享的错误结构，而非抽象的通用错误列表。

> 直观理解：普通示例库通常保存正确解法；CritBank保存“典型错误及其诊断”。这种设计保留了错误发生的完整上下文，使目标模型既看到风险名称，也看到风险如何在真实推理中表现。

**2. Failure Mode-Based Sample Selection**

该模块以一个或多个失败模式标签$l$为检索条件，通过$\mathcal{L}^{-1}(l)$取得相关$(q,r)$及其批评，再选择至多五个上下文示例。正文节选没有公开该选择过程内部的排序公式或完整去重规则，具体提示与程序细节被指向附录G，因此不能将其等同于单纯的语义相似度检索。

> 直观理解：它优先寻找“会犯同一种错”的案例，而不只是寻找“题面看起来相似”的案例。论文消融中单独比较了随机、固定和语义选择，说明失败模式对齐是方法所要检验的关键变量。

**3. 动态与静态失败风险建模**

CritICL-dynamic使用目标模型从$q'$预测至多五个输入相关标签，随后检索对应批评，因此总计两次模型调用；CritICL-static从建库弱模型的标签分布聚合出模型家族级全局画像，并为每个问题复用该画像，因此只需一次目标模型答案生成。两种方案共享CritBank和样本选择机制，主要区别是失败模式查询来自当前输入还是离线总体分布。

> 直观理解：动态方案会为每道新题重新判断潜在风险，适合错误类型随输入明显变化的情况；静态方案利用家族中长期稳定的高频错误，省去在线预测步骤。二者体现的是针对性与调用成本之间的设计取舍，而不是两个独立训练出的模型。

**训练与推理**

离线构建阶段：对$\mathcal{Q}$中的每个问题和$M$中的每个弱模型进行思维链生成，每个$(q,m)$采样五个响应；依据$\phi(q,r)$保留错误响应，使用gpt-4o-mini为每条错误生成至多五个候选失败模式和一条细粒度批评，再聚类相近标签并建立CritBank及其逆向索引。该阶段可理解为制作可复用的模型家族错题库，不涉及目标模型参数更新。

在线推理阶段：对于$q'\notin\mathcal{Q}$，CritICL-dynamic先调用目标模型预测至多五个可能标签，然后检索至多五个批评式示例并再次调用目标模型作答；CritICL-static直接使用弱模型总体错误分布形成的全局失败模式画像检索示例，再进行一次答案生成。最终答案采用目标模型在批评式提示下的单次作答，不需要像Consistency@$k$那样反复生成并聚合多个候选，也不需要额外裁判模型选答案。

**复现信息**

复现时最关键的设置有四点。第一，CritBank与目标模型应来自同一模型家族：主实验面向Qwen2.5-32B/72B时，使用Qwen2.5-1.5B、3B和7B建库；LLaMA实验同样由较弱LLaMA模型提供错误案例。第二，每个问题—弱模型组合生成五个思维链响应，每条错误最多产生五个候选失败标签，在线阶段最多预测五个标签并检索五个示例。第三，除非另有说明，失败模式标签和批评由gpt-4o-mini生成，标签还需按论文采用的聚类程序合并语义重复项；具体提示模板位于附录G.1，而Failure Mode-Based Sample Selection的进一步细节位于附录G，当前节选未给出完整排序算法。第四，主实验使用温度$0$的贪心解码；成本核算应将动态版本的失败模式预测计为一次额外调用，因此静态版为一次生成、动态版为两次生成，不能只统计最终答案调用。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：小学数学文字题基准，含约 7.4k 个训练样本和 1.3k 个测试样本。训练集全部用于构建 CritBank，即诱导弱模型作答后生成失败模式标签与批评；完整测试集用于分布内评测。
- MATH：更高难度的数学推理基准，含约 7.5k 个训练样本和 5k 个测试样本。其训练集与 GSM8K 训练集合并形成约 15k 道题的 CritBank 来源，完整测试集用于分布内评测。
- AMC23、AIME24 与 AIME25：竞赛级数学题基准，不参与主要数学 CritBank 的构建，用于检验分布外泛化，尤其考察失败模式批评能否帮助模型处理更长、更精确的多步推理。附录还以 GPQA 检验数学与科学推理之间的跨领域迁移。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

最终答案正确的测试样本比例，是数学推理主结果、迁移实验和多数消融实验的核心指标。 （越高越好，因为它直接表示模型成功解出题目的频率。）

</div>
<div class="metric-item" markdown="1">

**Precision**

在失败模式检索或预测所判定的相关项目中，真正相关项目所占比例；正文称其用于比较不同示例选择策略，但所给节选未提供具体计算公式。 （越高越好，表示检索到的批评与目标失败模式更少出现无关匹配。）

</div>
<div class="metric-item" markdown="1">

**Recall**

真正相关的失败模式项目中被选择策略覆盖的比例；正文称其用于检索策略消融，但所给节选未给出具体计算公式。 （越高越好，表示策略遗漏的相关失败模式批评更少。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Llama 家族内弱到强迁移：以小型 Llama 模型构建 CritBank，在 Llama-3.1-70B-Instruct 上同时评测分布内和分布外任务。

<div class="result-value" markdown="1">

作者报告 CritICL-static 的总体准确率为 53.1，高于最强基线 Consistency@5 的 51.3，并且只需单次生成；这说明所提方法的收益并非只出现在 Qwen 家族。

</div>

这一结果的关键比较不是简单增加示例，而是“单次、失败模式指导的生成”与“多次采样后投票”的比较。2.0 个百分点的总体差距支持 CritICL 具有更好的效果—生成次数折中，但不能据此证明它在所有模型家族或所有推理任务上都优于测试时扩展，因为这里只展示了一个 Llama 目标模型，且节选未报告置信区间或重复运行波动。

<div class="result-source" markdown="1">

来源：Appendix E.1, Table 12 accompanying discussion

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Notably, CritICL-static improves the overall accuracy to 53.1, outperforming the strongest baseline (Consistency@5 at 51.3) by a clear margin.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨模型家族迁移：使用弱 Llama 模型构建的 CritBank 指导 Qwen2.5-72B，并与普通 5-shot ICL、密集正确示例检索及同家族 Qwen CritBank 比较。

<div class="result-value" markdown="1">

在 GSM8K、MATH、AMC23 的平均准确率上，跨家族 Llama CritBank 达到 70.3，高于普通 5-shot ICL 的 68.8 和正确示例检索的 69.3；同家族 Qwen CritBank 进一步达到 71.6。结果表明失败模式中既有跨家族可复用部分，也有明显的家族特异结构。

</div>

跨家族 CritBank 仍能超过普通正确示例，排除了方法必须共享完全相同模型家族才能产生任何收益的强假设；但同家族结果更高，说明实践中应把家族内弱到强迁移视为主要适用场景。该实验只涉及 Qwen 与 Llama，不能证明对任意架构组合都能迁移。

<div class="result-source" markdown="1">

来源：Appendix D.1, Table 10

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen2.5-72B | Llama CritBank, cross-family | 94.7 | 82.3 | 33.8 | 70.3

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 失败模式分布的一致性检验：比较同家族弱模型聚合画像与强模型画像，并设置跨家族画像作为对照。

<div class="result-value" markdown="1">

Qwen 聚合弱模型画像对 Qwen2.5-72B 的 Spearman 相关系数为 0.91、Top-10 重合为 9/10、JS 距离为 0.041；Llama 聚合画像对 Llama-3.1-70B 的对应 Spearman 相关系数为 0.88、Top-10 重合为 9/10、JS 距离为 0.047。相比之下，跨家族 Spearman 相关系数仅为 0.46 或 0.43，支持按同家族弱模型失败模式指导强模型的实验前提。

</div>

Spearman 和 Top-10 重合衡量主要错误类型及其排序是否相似，JS 距离衡量完整分布是否接近；因此这些数字说明错误画像随同家族模型规模变化仍较稳定。它们只证明统计相关和分布相似，不能证明共享架构或训练流程在因果上产生了相同内部错误机制。

<div class="result-source" markdown="1">

来源：Appendix B.1, Table 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen → Qwen2.5-72B | Qwen Aggregate | 0.91 | 0.76 | 9/10 | 0.041

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

- Zero-shot 与普通 few-shot ICL：前者不提供示例，后者随机或固定提供 1、3、5 个正确问答示例。它们分别衡量基础模型能力，以及性能提升是否仅由增加正确示范和上下文长度造成。
- Self-consistency：以温度 1.0 生成 3、5 或 7 条推理路径并对最终答案多数投票；它是典型测试时扩展方法，用于比较 CritICL 的单次生成是否能达到多次采样带来的收益。
- Self-reflection：让目标模型迭代批评并修正自己的输出，用于判断预先检索弱模型失败模式批评是否比目标模型即时产生自我反馈更有效。
- LLM-as-a-judge：生成五个候选回答，再由 GPT-4o-mini 判断并选择最终答案；该基线检验 CritICL 是否能在不依赖额外强评审模型和多候选生成的情况下取得竞争性表现。

**实验想回答的问题**

- 由同一模型家族中的小模型错误构建的 CritBank，能否在只进行一次确定性生成的条件下，提高大模型在分布内与竞赛级分布外数学推理任务上的准确率，并优于普通上下文学习和需要多次生成的测试时扩展方法？
- 性能增益是否确实来自“按失败模式对齐并检索批评示例”，以及这种失败模式信号在模型规模、模型家族和推理领域之间能够迁移到什么程度？

**实验实现**

Qwen 实验以 Qwen2.5-1.5B/3B/7B-Instruct 的回答构建 CritBank，并在 Qwen2.5-32B/72B-Instruct 上评测；Llama 实验以 Llama-3.2-1B/3B-Instruct 和 Llama-3.1-8B 的回答构建 CritBank，在 Llama-3.1-70B-Instruct 上评测。除 Self-consistency 等明确需要随机采样的测试时扩展基线外，实验采用温度 0.0 的贪心解码，以获得确定性输出；测试时扩展方法默认置于 5-shot 条件。CritICL 的关键对照是：普通 ICL只展示正确解答，而 CritICL 根据弱模型暴露出的结构化错误检索带批评的上下文示例。节选未完整给出主表中的提示模板、每次检索示例数、答案抽取规则及重复运行方差，因此这些实现细节仍需核对全文或代码。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 失败模式分类粒度消融：比较 8 类粗粒度、20 类默认细粒度和 45 类超细粒度分类体系。 | 20 类细粒度体系平均准确率为 59.9，高于 8 类粗粒度的 58.7 和 45 类超细粒度的 59.3；其 GSM8K、MATH、AMC23、AIME25 准确率分别为 95.4、84.0、35.4、24.6。 | 该消融隔离的是“错误标签应划分多细”。类别过粗会把不同推理缺陷混在一起，使批评不够针对；类别过细则会把 CritBank 切成过小的检索池，导致匹配稀疏和噪声上升。中等粒度最优支持检索需要在错误特异性与样本覆盖率之间折中，但不意味着 20 类对其他领域或更大 CritBank 仍是全局最优。 | Appendix B.4, Table 6<br><span class="experiment-evidence">Fine-grained \| 20 \| 95.4 \| 84.0 \| 35.4 \| 24.6 \| 59.9</span> |
| 示例选择与增益来源消融：将失败模式检索替换为随机选择、固定选择、语义相似检索，并进一步考察正确示例检索、通用 GPT 批评、仅弱模型错误回答及打乱失败标签。 | 作者报告 CritICL-dynamic 与 CritICL-static 在四个数学基准及所用指标上均优于替代选择策略；在更难的 AMC23 与 AIME 上，准确率优势达到 4–6 个百分点。附录的受控变体还显示，移除或打乱失败模式与批评之间的对应关系会削弱效果，但所给节选未包含 Table 7 的具体数值。 | 这组实验旨在排除三个替代解释：收益只是来自更多上下文、只是来自与题面相似的示例，或只是来自外部模型生成的任意批评。失败模式对齐策略更好，说明检索对象的“错误结构相关性”比表面语义相似更关键。不过由于节选缺少 Table 3 和 Table 7 的完整逐项数字，无法检查每个数据集上的差值及统计稳定性。 | Section 5.1, Table 3 accompanying discussion; Appendix C.1, Table 7<br><span class="experiment-evidence">The improvements are substantial, especially on more challenging benchmarks such as AMC23 and AIME, where gains of 4–6 points in accuracy are observed.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：利用弱模型的结构化失败模式构造批评式上下文示例，以较低生成和 token 成本增强推理。; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`999f040c4d0c6165e5bbabcfde88aa756b46f05c98e179a98525f51146f38e44`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
