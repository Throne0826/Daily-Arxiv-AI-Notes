---
title: "[论文解读] IterCOMP: Reasoning-aware Adaptive Prompt Compression for Multi-hop Question Answering"
description: "[arXiv 2608.13588][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.13588"
announcement_date: "2026-08-17"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-18T02:04:41.205605+00:00"
source_sha256: "1f1f076fa344a6cb666ac9bb9f43b1cf7b3cc3d57727a9a4fec82842516bce38"
tags:
  - "LLM Reasoning"
  - "LLM 效率"
  - "多跳问答"
  - "检索增强生成"
  - "提示压缩"
  - "查询感知压缩"
  - "迭代推理"
  - "后续问题生成"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.13588</p>

# IterCOMP: Reasoning-aware Adaptive Prompt Compression for Multi-hop Question Answering

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-17</span>
<span><strong>作者</strong> JungMin Yun, YoungBin Kim</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Department of Artificial Intelligence, Chung-Ang University；Graduate School of Advanced Imaging Sciences, Multimedia and Film, Chung-Ang University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13588) · [PDF 下载](https://arxiv.org/pdf/2608.13588) · **关键词** 多跳问答, 检索增强生成, 提示压缩, 查询感知压缩, 迭代推理, 后续问题生成<br>


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

本文研究检索增强生成（Retrieval-Augmented Generation, RAG）环境下的多跳问答与提示压缩。RAG先从外部知识源检索文档，再将问题和检索结果一并输入大语言模型，从而弥补静态预训练知识覆盖不足的问题；但检索文档会带来较长且含噪的上下文，增加推理延迟、计算量和商业API成本，并可能因无关信息及“中间位置遗忘”现象降低回答准确性。该矛盾在多跳问答中更突出，因为模型必须把分散在多个文档中的证据按依赖关系连接起来，其中某些中间线索并未直接出现在初始问题中。因此，本文关注的不是单纯缩短输入，而是在较小词元预算下保留完成整条推理链所必需的证据。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**检索增强生成（RAG）**

RAG在回答问题前从外部来源检索相关文档，并把这些文档作为上下文交给大语言模型。它能引入动态知识，但检索内容过多时会提高成本并混入干扰信息。

</div>
<div class="concept-item" markdown="1">

**多跳问答（Multi-hop QA）**

多跳问答要求模型依次组合多个证据片段才能得到答案，而不是从单个句子直接抽取答案。不同证据通常分散在多篇文档中，后续需要寻找什么信息还可能取决于前一步发现的中间线索。

</div>
<div class="concept-item" markdown="1">

**硬提示压缩（Hard Prompt Compression）**

硬提示压缩通过抽取关键句或生成简短摘要，将原始文本压缩为仍可直接阅读的离散文本。与依赖模型内部连续向量的软提示不同，它更适合无法访问模型参数或隐藏状态的商业API环境。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入包括一个需要跨文档推理的自然语言问题，以及RAG系统检索得到的多个文档或证据片段；这些候选内容可能冗长、重复、与问题无关，也可能只在与其他片段组合后才显现价值。目标是生成一个更短、面向推理的文本提示：它应删除干扰内容，同时保留足以回答原问题的跨文档证据及其关键关联，随后供大语言模型生成最终答案。本文所针对的设置允许在压缩过程中调用大语言模型判断现有证据是否充分，并在证据不足时提出有针对性的后续问题；根据摘要和引言，IterCOMP是统一且无需训练的框架，但所给章节未给出形式化输入输出符号、压缩率约束或检索器假设。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **LongLLMLingua**: 代表查询感知的硬提示压缩：先依据查询条件下的困惑度估计文档级重要性，再细化到词元选择。它能保留与初始查询直接相关的内容，但论文指出，这类单查询与单文档或句子的匹配范式难以表示多跳问答中的跨文档依赖和隐式中间线索。
- **Self-Ask**: 通过让大语言模型生成并回答子问题来分解复杂查询，为组合推理提供逐步的信息需求。IterCOMP借鉴这种后续提问能力，但将其置于提示压缩循环中：后续问题用于识别当前证据缺口并指导关键证据的迭代整合，而不只是展开答案推理。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

多跳问答要求模型把分散在多个文档或证据片段中的信息连接起来，才能得到最终答案。检索增强生成（RAG）虽然能够补充模型预训练数据之外的知识，但通常会把大量检索结果直接放入上下文，导致输入变长、推理延迟和调用成本上升；无关内容还可能分散模型注意力，使模型难以完成跨文档的信息整合。这个问题在多跳问答中更严重，因为有效证据往往不是由初始问题直接指出，而是需要通过中间推理逐步发现。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **检索增强生成（RAG）**：RAG先根据问题从外部语料库检索相关文档，再将检索结果与原问题一起提供给大语言模型，由模型生成基于外部证据的答案。它能够弥补模型静态预训练知识覆盖不足的问题，但如果检索结果未经充分筛选，输入中仍会包含大量冗余或干扰信息。
- **查询导向的提示压缩**：这类方法依据单个用户查询与文档内容之间的相关性，删除不重要的词句、片段或文档，或者把长文本压缩成更短的表示，从而降低上下文长度。其核心判断通常是初始查询是否直接与某段内容相关。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有提示压缩方法大多采用单查询、单轮筛选范式，只依据初始问题判断文档相关性，难以识别多跳问答中需要经过中间线索才能发现的证据。结果是某些当前看似不相关、但对后续推理必不可少的片段可能被提前删除，造成证据链断裂和答案信息不完整。
- 直接扩大RAG上下文或使用一次性压缩，无法充分处理多个证据片段之间的顺序依赖与相互补充关系。输入越长，推理计算和API调用成本越高，同时无关内容及其位置偏差可能降低模型的准确性；而迭代压缩若缺少对当前证据是否足以回答问题的判断，又可能过早停止或累积错误证据。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未充分解决这样的问题：如何在不进行额外训练的条件下，把多跳推理过程直接纳入提示压缩，使压缩器能够根据当前已保留的证据判断答案是否可得，并在不足时主动确定下一步需要寻找的信息。缺少这一机制时，压缩目标只是缩短文本，而不是在降低上下文开销的同时保持完整的多跳证据链。

</div>
<div markdown="1"><span>核心问题</span>

能否构建一种训练无关且适用于不同大语言模型的自适应压缩框架，使其通过反复判断当前证据的可回答性、发现信息缺口并生成针对性的后续问题，逐步保留完成多跳问答所必需的证据，同时减少最终提示中的令牌数量？

</div>
<div markdown="1"><span>作者直觉</span>

多跳问答的关键证据往往要沿着推理路径逐步显现，因此压缩过程不应只问“这段内容是否直接匹配原问题”，还应问“在当前推理状态下，已有证据是否足够；如果不足，下一步缺什么”。IterCOMP的切入点是让大语言模型参与这一循环：先筛选候选证据，再判断能否回答；若不能回答，则根据已知信息提出有明确目标的后续问题，用新获得的证据补足推理链。直观地说，这种方法把一次性的文本删减改成面向解题过程的逐步取舍，因而有机会同时减少冗余上下文并保留跨文档推理所需的信息。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

IterCOMP 将多跳问答中的提示压缩建模为一个由“证据筛选—充分性判断—缺口追问—再次筛选”构成的闭环。输入是原始问题 $q^{(0)}$ 与检索文档集合 $D=\{d_1,\ldots,d_N\}$；系统先把文档拆成句子级证据片段，再以语义相似度和词汇相似度联合打分，按全局分数分位数保留候选证据 $E_{\mathrm{cand}}^{(h)}$。随后，LLM 判断当前证据能否回答原问题：若可以，就将其定为压缩提示 $P_{\mathrm{comp}}$ 并交给阅读器 $M$ 生成答案；若不可以，LLM 则指出缺失信息并生成后续问题 $q^{(h)}$，系统据此重新筛选并累积证据，直到证据充分或达到最大迭代次数。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 文档分解

将每篇文档 $d_i$ 按句子切分为 $E_i=\{e_{i,1},\ldots,e_{i,R_i}\}$，其中 $R_i$ 是文档 $d_i$ 的句子数；所有句子片段与当前查询共同送入证据筛选模块。句子级粒度在保留局部语义的同时，使系统能够删除文档内部无关内容，而不必整篇保留或丢弃。

<div class="method-step__io" markdown="1">

**输入**：原始问题 $q^{(0)}$ 与检索文档集合 $D=\{d_1,\ldots,d_N\}$。<br>
**输出**：全体候选证据片段 $\bigcup_i E_i$。

</div>

**直观理解**：这一步相当于把长文档拆成可独立挑选的句子，使压缩器能够只留下推理真正需要的部分。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 双视角相关性筛选

使用冻结的 bge-m3 分别计算查询与片段的稠密语义相似度和加权词汇重合度，再由权重 $\lambda$ 合成为双视角分数 $S_{\mathrm{dual}}$。系统在所有片段的全局分数分布上计算第 $k$ 百分位阈值，只保留分数不低于该阈值的片段。

<div class="method-step__io" markdown="1">

**输入**：当前查询 $q^{(h)}$ 与全部证据片段 $e_{i,j}$；第一次迭代时使用原始问题 $q^{(0)}$。<br>
**输出**：本轮筛选并累积得到的候选证据集合 $E_{\mathrm{cand}}^{(h)}$。

</div>

**直观理解**：语义分数寻找“意思相近”的句子，词汇分数保住实体名、关键词等精确线索；分位数阈值则根据当前材料的相对分布自适应决定保留范围。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 可回答性判断与缺口定位

LLM 作为二分类推理控制器，判断当前证据是否足以推出原问题答案。若判断为不可回答，LLM 进一步明确缺失信息，并把该知识缺口改写为有针对性的后续问题 $q^{(h)}$。

<div class="method-step__io" markdown="1">

**输入**：原始问题 $q^{(0)}$ 和当前累计证据 $E_{\mathrm{cand}}^{(h)}$。<br>
**输出**：“可回答/不可回答”判定；不可回答时还输出后续问题 $q^{(h)}$。

</div>

**直观理解**：控制器不是只问哪些句子看起来像原问题，而是检查现有线索能否连成完整推理链；缺哪一环，就生成专门寻找那一环的新问题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 迭代积累、停止与答案生成

若证据充分，系统提前停止并令 $P_{\mathrm{comp}}=E_{\mathrm{cand}}^{(h)}$；若证据不足且仍有迭代预算，则以 $q^{(h)}$ 重新执行相关性筛选，得到并累积 $E_{\mathrm{cand}}^{(h+1)}$。循环在证据充分或达到最大跳数时结束，最终由阅读器生成 $y=M(P_{\mathrm{comp}},q^{(0)})$。

<div class="method-step__io" markdown="1">

**输入**：充分性判定、后续问题 $q^{(h)}$、候选证据 $E_{\mathrm{cand}}^{(h)}$ 及预设最大迭代次数。<br>
**输出**：压缩提示 $P_{\mathrm{comp}}$ 与最终答案 $y$。

</div>

**直观理解**：系统会边推理边补材料，而不是一次性压缩；证据够用就立即作答，证据不够才继续寻找，并用迭代上限避免无休止追问和噪声累积。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 提示压缩任务目标与阅读器输出

$$
D=\{d_1,\ldots,d_N\},\qquad L(P_{\mathrm{comp}})\ll\sum_{i=1}^{N}L(d_i),\qquad y=M(P_{\mathrm{comp}},q)
$$

**符号说明**

- $q$：待回答的原始问题。
- $D$：初始检索得到的文档集合。
- $d_i$：检索集合中的第 i 篇文档。
- $N$：检索文档总数。
- $P_{\mathrm{comp}}$：从检索文档中合成的简洁但信息充分的压缩提示。
- $L(\cdot)$：输入文本的词元长度。
- $M$：读取压缩提示和问题并生成答案的下游阅读器模型。
- $y$：阅读器生成的最终答案。

<div class="equation-explanation" markdown="1">

**直观理解**：该形式化没有给出一个可训练的标量损失，而是规定方法应同时满足两个目标：压缩提示远短于全部原始文档，同时仍保留足够的推理证据，让阅读器产生高保真答案。IterCOMP 用相关性筛选控制长度，用可回答性判断约束信息充分性。<br>
**原文位置**：第 4.1 节 Problem Formulation

</div>

</div>

<div class="equation-block" markdown="1">

#### 双视角相关性评分与百分位筛选

$$
\begin{aligned}S_{\mathrm{sem}}(q,e_{i,j})&=E(q)^{\top}E(e_{i,j}),\\ w_t^x&=\operatorname{ReLU}(\mathbf{w}_{\mathrm{lex}}^{\top}E_x(t)),\quad x\in\{q,e_{i,j}\},\\ S_{\mathrm{lex}}(q,e_{i,j})&=\sum_{t\in q\cap e_{i,j}}w_t^q w_t^{e_{i,j}},\\ S_{\mathrm{dual}}(q,e_{i,j})&=\lambda S_{\mathrm{sem}}(q,e_{i,j})+(1-\lambda)S_{\mathrm{lex}}(q,e_{i,j}),\\ \mathcal{S}&=\{S_{\mathrm{dual}}(q,e_{i,j})\mid\forall i,j\},\\ E_{\mathrm{cand}}&=\{e_{i,j}\mid S_{\mathrm{dual}}(q,e_{i,j})\geq\operatorname{Percentile}(\mathcal{S},k)\}.\end{aligned}
$$

**符号说明**

- $e_{i,j}$：第 i 篇文档中的第 j 个句子级证据片段。
- $E(\cdot)$：bge-m3 提供的冻结文本编码器；用于产生查询、句子或上下文化词元表示。
- $S_{\mathrm{sem}}$：查询与证据片段稠密向量的内积，即语义相似度。
- $t$：查询或证据片段中的词元。
- $\mathbf{w}_{\mathrm{lex}}$：把上下文化词元表示投影为标量重要性分数的预训练向量。
- $w_t^x$：词元 t 在文本 x 的上下文中的非负词汇重要性权重。
- $S_{\mathrm{lex}}$：查询与证据共有词元的重要性乘积之和，即加权稀疏词汇相似度。
- $\lambda$：位于区间 [0,1] 的权重，用于平衡语义信号与词汇信号。
- $S_{\mathrm{dual}}$：融合语义与词汇相关性的最终证据分数。
- $\mathcal{S}$：当前所有候选片段的双视角相关性分数多重集合。
- $k$：用于确定动态截断位置的百分位参数。
- $E_{\mathrm{cand}}$：分数达到或超过第 k 百分位阈值的候选证据集合。

<div class="equation-explanation" markdown="1">

**直观理解**：前四行分别衡量“整体含义是否相近”和“重要共有词是否匹配”，再将两者合并。最后两行不设固定绝对分数，而是在当前全部片段中保留相对高分者，使筛选阈值能随不同问题和检索上下文的分数尺度变化；迭代时只需把 $q$ 换成新生成的后续问题即可重新聚焦。<br>
**原文位置**：第 4.2.2 节，公式（1）至（5）；为呈现完整筛选规则而合并书写

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：IterCOMP 是训练-free 方法，没有为压缩器定义或优化额外的训练损失。文本编码器及词汇投影向量直接采用预训练 bge-m3，并在整个流程中冻结；LLM 通过提示执行可回答性分类、缺失信息识别和后续问题生成，阅读器负责最终答案生成。因此，第 4.1 节的长度约束与答案保真要求属于任务目标，而不是通过梯度下降直接优化的目标函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双视角证据相关性模块**

该模块以冻结的 bge-m3 同时提供句子级稠密表示和词元重要性表示。稠密内积 $S_{\mathrm{sem}}$ 捕捉上下文语义对应关系；稀疏分数 $S_{\mathrm{lex}}$ 只在查询与证据共有词元上累加双方的上下文化重要性乘积，再以 $\lambda$ 加权融合并进行百分位筛选。

> 直观理解：仅靠语义匹配可能漏掉名称、数字或专有词等精确线索，仅靠关键词又可能无法识别改写和隐含关系；两种信号结合，是为了兼顾“意思相关”和“关键字确实对得上”。

**2. 可回答性推理控制器**

在第 $h$ 轮，LLM 联合读取原问题 $q^{(0)}$ 与累计证据 $E_{\mathrm{cand}}^{(h)}$，执行证据充分性的二元判断。它决定是否将当前集合直接固化为 $P_{\mathrm{comp}}$，因此把压缩停止条件从固定长度或固定轮数改为由推理需求驱动的动态条件。

> 直观理解：普通压缩器通常只判断文本是否相关，却不检查线索是否足以完成整条推理链；该控制器负责回答更关键的问题，即“现在的信息是否已经够用”。

**3. 缺失信息识别与查询反馈模块**

当 $E_{\mathrm{cand}}^{(h)}$ 不充分时，同一类 LLM 推理能力被用于定位阻断答案推导的知识缺口，并生成目标明确的后续问题 $q^{(h)}$。该问题返回证据筛选模块，使下一轮排序不再只围绕原问题的表面措辞，而能寻找中间推理节点所需的补充事实。

> 直观理解：多跳问题常把中间问题隐藏起来，例如先要确定人物身份，才能查询其出生地；该模块会主动提出这个中间问题，从文档中补齐缺失的一跳。

**训练与推理**

训练阶段不存在面向 IterCOMP 的参数更新。推理开始时，系统输入 $q^{(0)}$ 与 $D$，完成句子级分解，并以 $q^{(0)}$ 计算双视角相关性和百分位阈值，形成首轮证据 $E_{\mathrm{cand}}^{(0)}$。LLM 随后判断这些证据是否足以回答 $q^{(0)}$：若充分，立即令 $P_{\mathrm{comp}}=E_{\mathrm{cand}}^{(0)}$；若不足，则描述缺失信息并生成后续问题。第 $h$ 轮产生的 $q^{(h)}$ 被用来重新评价文档片段，新增相关证据被纳入下一轮累计集合 $E_{\mathrm{cand}}^{(h+1)}$，再接受同样的充分性检查。循环在 LLM 判断可回答时提前终止，或在达到预定义最大跳数时强制结束；最终把压缩提示和原问题送入阅读器，得到 $y=M(P_{\mathrm{comp}},q^{(0)})$。需要注意，后续问题用于寻找中间证据，最终回答的目标始终是原问题 $q^{(0)}$。

**复现信息**

复现方法结构所必需的设置包括：以句子作为证据分解单位；以未经额外微调且全程冻结的 bge-m3 同时提供稠密编码器和词汇重要性投影；用超参数 $\lambda$ 混合语义与词汇分数；在全部候选片段的全局分数分布上采用第 $k$ 百分位阈值；并为迭代证据积累设置最大跳数，以限制错误的“不可回答”判断引发的无效循环和噪声传播。所给章节没有明确报告 $\lambda$、$k$、最大迭代次数、具体控制器 LLM、阅读器模型、解码参数或提示模板的最终实验取值，因此仅凭当前摘录不能完整复现实验配置，不应自行补全这些参数。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MuSiQue：包含需要二至四跳推理的问题。主实验使用仅含可回答问题的$musique\_ans\_v1.0\_dev$子集；它也是消融、推理复杂度分析和API效率分析的主要数据集。预备实验按二跳、三跳、四跳分别随机抽取400个问答对，用于检验模型能否判断证据是否充分并识别缺失信息。
- 2WikiMultiHopQA：在开发集上进行零样本评测，用于检验压缩方法能否泛化到基于多个维基百科事实连接的多跳问答；原文节选未提供该开发集的具体样本数。
- HotpotQA：在开发集上进行零样本评测，并通过与Raw Documents和Oracle的差距比较，检验IterCOMP能否从长上下文中保留支持多跳推理的关键信息；原文节选未提供该开发集的具体样本数。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Exact Match（EM）**

预测答案与标准答案在规范化后完全一致的比例，衡量严格的答案正确性；近义表达或格式差异也可能被判错。 （越高越好，因为完全匹配的测试样本更多。）

</div>
<div class="metric-item" markdown="1">

**F1**

根据预测答案与标准答案之间的词元重叠计算精确率和召回率的调和平均，是主问答质量指标；相比EM，它允许答案部分匹配。预备实验还报告答案可判定性分类的总体F1，但该数值与问答答案F1属于不同任务，不能直接横向比较。 （越高越好，因为预测答案覆盖标准答案内容的同时包含更少错误内容。）

</div>
<div class="metric-item" markdown="1">

**Compression Ratio（Ratio）**

压缩后提示相对于原始上下文的长度比例，用于衡量保留了多少输入；例如$0.14$表示压缩提示约为原输入的14%。 （在问答质量相近时越低越好，因为输入更短、推理成本通常更低；但比例过低可能删除完成推理链所需的补充证据。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### MuSiQue主结果：IterCOMP对比Raw Documents与最强已报告压缩基线R2C

<div class="result-value" markdown="1">

IterCOMP取得$27.36$的F1；Raw Documents为$19.92$，因此提高$7.44$点；相对次优R2C高$4.92$点。作者还报告MuSiQue输入长度约缩短至原来的七分之一。

</div>

结果表明，在固定LLaMA-3-8B阅读器下，选择并迭代补充证据比直接输入所有文档更准确，也优于作者纳入比较的现有压缩方法。合理解释是无关上下文会干扰多跳证据连接，而IterCOMP保留了更集中的推理线索。不过，这只是开发集上的方法级比较，不能证明增益完全来自某一个模块，也不能证明对其他阅读器、测试集或真实检索错误同样成立。

<div class="result-source" markdown="1">

来源：第5.2节Main Results；Table 3（表格本体未包含在节选中）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Compared to existing compression methods, IterCOMP demonstrates notable performance gains. On MuSiQue, it attains an F1 score of 27.36, surpassing the second-best method, R2C, by 4.92 points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### HotpotQA主结果：缩小Raw Documents与Oracle之间的性能差距

<div class="result-value" markdown="1">

Raw Documents与Oracle的F1差距为$15.32$点，IterCOMP取得$51.79$的F1，并按作者计算弥合其中$53.2\%$。同一节前文把该F1写为$51.78$，存在$0.01$的文本不一致，需回查Table 3。

</div>

Oracle使用真实支持文档，代表理想文档选择；因此“弥合差距”比只与无压缩方法比较更能说明证据筛选质量。IterCOMP恢复了约一半由冗余上下文造成的潜在损失，但仍未达到Oracle，说明自动过滤仍会漏掉证据或保留噪声。Oracle只是文档级上界，并非整个问答系统的理论上界。

<div class="result-source" markdown="1">

来源：第5.2节Main Results；Table 3（表格本体未包含在节选中）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On HotpotQA, the performance gap between Raw Documents and Oracle is 15.32 points. IterCOMP attains an F1 score of 51.79, effectively closing 53.2% of this gap.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### MuSiQue推理复杂度分析：二跳至四跳

<div class="result-value" markdown="1">

二跳、三跳、四跳的F1依次为$30.19$、$26.16$、$20.72$；平均迭代次数依次为$1.98$、$2.45$、$3.08$，压缩提示长度依次为$228$、$348$、$403$个词元。

</div>

随着推理链变长，系统自动执行更多证据补全轮次并保留更长上下文，说明它不是固定长度的一次性过滤器，而会根据问题难度调整计算量和证据量。但F1仍明显下降，表明增加迭代只能部分应对复杂度，无法消除长链证据连接和阅读器推理能力带来的困难。该分析展示的是相关趋势，并未通过控制变量证明跳数本身是性能下降的唯一原因。

<div class="result-source" markdown="1">

来源：Table 4；第5.2节Reasoning Complexity

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

2-hop 19.33 30.19 1.98 228; 3-hop 14.87 26.16 2.45 348; 4-hop 11.60 20.72 3.08 403.

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

- Raw Documents：直接拼接数据集中的全部文档，不进行过滤。它回答“压缩是否比把所有上下文交给阅读器更好”，并暴露无关文本对推理的干扰及输入成本。
- Oracle：只向阅读器提供金标准支持文档，作为文档级压缩的理想选择上界。它用于衡量IterCOMP距离完美文档筛选还有多大差距，但并不是现实可部署的方法，因为测试时通常不知道金标准文档。
- LLMLingua、LongLLMLingua与LLMLingua-2：代表已有提示压缩方法，用于比较IterCOMP的推理感知迭代机制与通用提示压缩策略。原文节选未分别解释三者的实现差异。
- RECOMP、Selective-Context与R2C：代表与本文最相关的抽取式或硬压缩策略；其中R2C是MuSiQue上作者报告的次优方法，因此是判断IterCOMP增益是否超过强竞争方法的关键参照。

**实验想回答的问题**

- IterCOMP能否在零样本多跳问答中，以明显更短的输入上下文获得优于无压缩输入和现有硬压缩、抽取式压缩方法的回答准确率？
- 迭代证据补全、答案可判定性判断和双重相关性过滤是否分别有效，以及IterCOMP能否随推理跳数增加而自适应地增加迭代次数与保留证据量？

**实验实现**

所有主实验均在三个数据集的开发集上采用零样本设置，并统一使用LLaMA-3-8B作为阅读器，以减少阅读模型差异对压缩方法比较的干扰。IterCOMP最多执行5轮迭代；融合语义与词汇相关性信号的权重设为$\lambda=0.6$。相关性过滤使用百分位阈值$k$：MuSiQue和HotpotQA取$k=90$，2WikiMultiHopQA取$k=85$；作者称其与Oracle压缩设置对齐以提高比较公平性。除EM、F1和压缩比外，复杂度分析还记录平均迭代次数与压缩后词元数，API效率实验则在MuSiQue随机500个样本上测量最终阅读器问答步骤的成本和延迟。预备实验使用GPT-4o依据数据集分解标注生成子问题—子答案，并比较LLaMA-3.1-8B-Instruct、Mistral-7B-Instruct、GPT-3.5-Turbo和GPT-4o的证据充分性判断及缺失信息识别能力。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除迭代细化（Iterative Refinement） | 完整IterCOMP的EM、F1和Ratio分别为$16.67$、$27.36$和$0.14$；移除迭代细化后分别变为$8.50$、$17.39$和$0.06$，F1下降$9.97$点，是表中最大的性能降幅。 | 该消融隔离了“发现证据不足后生成后续问题并继续累积证据”的作用。更低的Ratio说明一次过滤确实更短，但大幅下降的F1表明它经常缺少后续推理跳所需信息；因此迭代带来的额外词元不是单纯冗余，而是在准确率和压缩强度之间交换必要证据。不过，移除模块也同时改变了输入长度，不能把全部差值严格归因于推理过程本身。 | Table 5；第5.3节Ablation Study & Analysis<br><span class="experiment-evidence">Iterative Refinement 8.50 17.39 0.06.</span> |
| 相关性过滤阈值$k$的敏感性分析 | MuSiQue上的F1随$k$增大而上升，在$k=90$时达到峰值$27.36$，但在$k=95$时下降；当$k\geq90$时，压缩提示比Oracle设置还短。 | 较大的$k$意味着过滤更严格：先去除更多噪声会帮助阅读器，但阈值过高又会删掉完成多跳链所需的辅助证据。这验证了压缩存在非单调权衡，并为主实验选择$k=90$提供经验依据；同时也说明结果依赖数据集上的阈值调节，不能假定同一阈值天然适用于所有分布。 | Figure 3（左）；第5.3节Ablation Study & Analysis<br><span class="experiment-evidence">The F1 score increases steadily with larger k, peaking at 27.36 when k=90. This indicates that a stricter relevance threshold effectively isolates salient information and reduces noise, thereby enhancing the reader model’s reasoning. However, performance drops at k=95, suggesting that an overly stringent cutoff discards supplementary evidence necessary for completing the reasoning chain.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出面向多跳问答推理的自适应提示压缩方法，同时核心涉及推理能力与上下文效率。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`1f1f076fa344a6cb666ac9bb9f43b1cf7b3cc3d57727a9a4fec82842516bce38`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
