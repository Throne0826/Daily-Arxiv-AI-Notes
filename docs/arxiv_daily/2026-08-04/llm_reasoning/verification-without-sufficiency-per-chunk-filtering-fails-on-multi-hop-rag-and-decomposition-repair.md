---
title: "[论文解读] Verification Without Sufficiency: Per-Chunk Filtering Fails on Multi-Hop RAG, and Decomposition Repairs It"
description: "[arXiv 2608.00585][LLM Reasoning] 本文指出，多跳检索增强生成中的逐文本块验证隐含了“单个文本块足以回答原问题”的错误假设，并提出改用分解后的子问题验证相应证据。"
arxiv_id: "2608.00585"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T03:37:41.758923+00:00"
source_sha256: "646bf2d6eae5f889f7d4937f126d2b9cf81b3e91729cedd2531a4406e309bb45"
tags:
  - "LLM Reasoning"
  - "检索增强生成"
  - "多跳问答"
  - "逐块验证"
  - "自然语言推断"
  - "证据充分性"
  - "问题分解"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.00585</p>

# Verification Without Sufficiency: Per-Chunk Filtering Fails on Multi-Hop RAG, and Decomposition Repairs It

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Randhir Kumar</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.00585v1) · [PDF 下载](https://arxiv.org/pdf/2608.00585v1) · **关键词** 检索增强生成, 多跳问答, 逐块验证, 自然语言推断, 证据充分性, 问题分解<br>
**代码**: [https://github.com/iamhero2709/verification-without-sufficiency](https://github.com/iamhero2709/verification-without-sufficiency)

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

本文指出，多跳检索增强生成中的逐文本块验证隐含了“单个文本块足以回答原问题”的错误假设，并提出改用分解后的子问题验证相应证据。

**不用术语来说**：回答多跳问题往往需要把多个段落串联起来：前一个段落确定中间实体，后一个段落才给出最终答案。现有过滤器却让每个段落单独面对完整原问题，并删除看起来不能独立回答该问题的段落；这样一来，真正承载后续推理信息的关键段落反而容易被误删。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将逐文本块过滤失败归因于验证目标与多跳证据结构不匹配，而非简单归因于模型能力、检索器、阈值或提示设计：原问题通常只直接指向首跳证据，后续证据必须借助中间实体才能与问题建立联系。
- 作者提出以分解后的当前跳子问题替代完整原问题作为验证条件，使后续证据在与其真正对应的局部信息需求下接受判断，并通过黄金分解与现成分解器评估这一修复方向的潜力。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

检索增强生成（RAG）先从语料库中检索与问题相关的文本块，再让语言模型依据这些文本生成答案。由于检索器可能返回主题相近但事实无关的内容，常见系统会增加验证环节：分别评价每个文本块，并删除被判为错误或不相关的块。本文关注这一做法在多跳问答中的适用性：多跳问题需要串联多个段落中的事实，而单个段落通常不足以独立推出最终答案；尤其是后续跳所需的答案段落往往不会直接出现原问题中的实体或关系，因此，用原问题逐块验证可能恰好排除关键证据。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**检索增强生成（RAG）**

一种先检索外部文本、再将检索结果作为上下文交给语言模型生成答案的框架。它能够补充模型参数之外的知识，但答案质量依赖检索证据是否正确且充分。

</div>
<div class="concept-item" markdown="1">

**多跳问答**

需要依次组合两个或更多证据步骤才能回答的问题，例如先根据原问题确定一个中间实体，再查找该实体的属性。关键难点是后续证据可能只与中间结果直接相关，而与原问题的表面措辞并不相似。

</div>
<div class="concept-item" markdown="1">

**自然语言推断与蕴含**

自然语言推断判断一个前提是否足以支持某个假设，其中“蕴含”表示假设可由前提推出。在本文场景中，把单个检索段落作为前提进行蕴含评分，实际上隐含了该段落应能单独支持目标结论的假设。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究场景是面向单跳与多跳问答的RAG证据过滤。系统接收用户问题以及检索器返回的一组候选文本块，逐块计算嵌入相似度、自然语言推断蕴含度或基于全息约化表示的结构分数，再据此保留或丢弃文本块，最后将保留的上下文交给生成器回答。验证器的直接目标是区分金标准支持段落与干扰段落；本文考察的核心假设是：以原始问题为条件的逐块判断，是否能识别多跳推理中的关键证据。问题的结构性障碍在于，多跳任务只保证若干段落的组合足以回答问题，并不保证任一单独段落都是充分前提；因此，单块验证所采用的判断单位可能与任务所要求的证据单位不一致。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **CRAG**: CRAG训练检索评估器，对单个文本块给出正确、错误或模糊的判断，并据此选择生成分支。本文将其视为逐块验证范式的代表，并指出这种粒度主要在偏单跳任务上得到评估，未必能迁移到需要证据链的多跳场景。
- **Self-Ask与IRCoT**: 这类迭代检索方法会在不同推理跳之间重写或分解查询，因为第二跳证据通常无法直接通过原始问题检索到。本文把同一逻辑延伸到验证阶段：后续段落也应依据对应的分解子问题验证，而不应始终依据原始问题逐块判断。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

检索增强生成需要过滤检索结果中的无关段落，以免生成器利用主题相近但事实无关的内容。然而在多跳问答中，答案依赖一条跨段落证据链；若过滤阶段误删链条中的任一后续证据，即使检索器已经找到了所需材料，生成器仍无法完成推理，而且能力更强的生成器也无法弥补输入证据被提前移除的问题。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **逐文本块相关性或正确性过滤**：CRAG一类方法为每个检索文本块分别标注正确、错误或含糊，并仅保留高分内容；嵌入余弦相似度也可按原问题与文本块的语义接近程度排序。其共同特点是独立判断每个文本块，而不显式表示文本块之间的证据依赖。
- **蕴含与自反思式验证**：自然语言推断、RAGAS式忠实性指标或Self-RAG式反思机制，判断给定上下文是否支持待回答内容或生成结果。用于检索过滤时，它们通常仍以完整原问题为条件，对单个文本块进行支持性判断。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 逐块验证把每个文本块当作能够独立支持完整答案的充分前提，但多跳问题按定义需要组合多个证据；因此，单块低分可能只表示“证据尚不完整”，并不表示该文本块无关。将低分直接解释为应删除会破坏证据链。
- 完整原问题通常明确提到首跳实体，却不直接提到由首跳推导出的中间实体。于是验证器容易认可题面已经点名的首跳段落，却难以识别承载最终答案的后续段落；增强模型、修改阈值或更换检索器并未改变这种条件信息缺失。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有验证研究主要关注如何提高单个文本块的相关性、正确性或蕴含评分，却没有解决一个更基础的接口问题：在多跳检索中，验证器究竟应依据完整原问题，还是依据证据链当前一步的局部信息需求来判断文本块。与此同时，迭代检索系统可能已经生成子问题，却通常没有把这些中间结构继续用于验证。

</div>
<div markdown="1"><span>核心问题</span>

逐文本块验证在多跳检索增强生成中是否因“单块充分性”假设而系统性失败；若是，将验证条件从完整原问题改为分解后的当前跳子问题，能否恢复对后续关键证据的识别能力？

</div>
<div markdown="1"><span>作者直觉</span>

一个后续段落未必能单独回答完整问题，但通常能够直接回答某个明确的中间子问题。先把复杂问题拆成连续的小问题，再让每个文本块接受与其所在推理步骤相匹配的验证，相当于不再问“这个段落能否独自完成整道题”，而是问“它能否完成当前这一步”；这样可把证据链中的必要但不充分证据与真正的干扰项区分开。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文把多跳 RAG 的证据验证表述为“验证前提是否充分”的问题。输入是原始问题 $q$ 与候选段落集合 $\mathcal{C}$；传统逐块方法分别计算每个段落 $c_i$ 对整道问题的蕴含分数并据此保留或删除，但多跳问题通常需要多个段落联合推理，尤其是后续跳段落并不包含问题中直接出现的实体，因此单个段落无法蕴含完整答案。论文在相同模型下比较三种前提构造：逐块验证以单段为前提，集合级验证枚举段落对，条件式验证先固定第一跳锚点再寻找能补全推理链的段落。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选段落检索与第一跳锚定

用双编码器计算 $s_{\mathrm{emb}}(q,c)$，取分数最高的 $k$ 个段落组成 $\mathcal{T}$，再令 $c_1=\arg\max_{c\in\mathcal{T}}s_{\mathrm{emb}}(q,c)$。该锚点被视为问题直接指名、因而较容易通过语义相似度识别的第一跳证据。

<div class="method-step__io" markdown="1">

**输入**：原始问题 $q$、候选段落集合 $\mathcal{C}$ 和候选预算 $k$。<br>
**输出**：候选子集 $\mathcal{T}$ 与第一跳锚点 $c_1$。

</div>

**直观理解**：原问题通常直接提到第一跳实体，因此先找“最像问题”的段落较可靠；这相当于先抓住推理链中已露面的线索，而不是直接猜隐藏的答案段落。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造可供 NLI 检查的假设

规则算子 $\mathcal{H}$ 将疑问句转换为答案槽未指定的客体层陈述，例如把“Who directed Inception?”转换为“a person directed Inception.”。修复方案不再对完整问题应用 $\mathcal{H}$，而是先解析子问题中的占位符，再从当前跳子问题构造假设。

<div class="method-step__io" markdown="1">

**输入**：原始问题 $q$，或分解后针对某一跳的子问题。<br>
**输出**：用于自然语言推断的陈述式假设 $h$。

</div>

**直观理解**：NLI 模型擅长判断一条陈述能否由文本推出，而不擅长直接处理问句。关键不是换模型，而是让它检查“这个段落是否支持当前一步”，而不是要求单段回答整道多跳问题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 以充分前提寻找补全段落

对每个候选构造联合前提 $c_1\oplus c_j$，计算 $u_j=P(\text{entail}\mid c_1\oplus c_j,h)$，并选择 $c_2=\arg\max_j u_j$。该条件式搜索需要 $k-1$ 次蕴含调用，而盲目枚举所有段落对需要 $\binom{k}{2}$ 次。

<div class="method-step__io" markdown="1">

**输入**：锚点 $c_1$、其余候选 $c_j\in\mathcal{T}\setminus\{c_1\}$ 与假设 $h$。<br>
**输出**：条件式证据集合 $\{c_1,c_2\}$ 及其联合蕴含分数。

</div>

**直观理解**：单独看第二跳段落时，它可能与原问题不像，也不能推出完整答案；把已知第一跳与每个候选拼起来，验证器才有机会判断哪个候选真正补齐了推理链。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按分解子问题逐跳验证

对后续跳，将原问题假设替换为当前子问题假设，并对候选段落计算蕴含分数；论文分别使用 MuSiQue 的金标准分解和无需微调的 Qwen2.5-7B-Instruct 分解器进行检验。若系统本身采用 Self-Ask 或 IRCoT 一类迭代检索，可直接复用检索阶段已经生成的子问题。

<div class="method-step__io" markdown="1">

**输入**：问题分解产生的各跳子问题、此前跳的答案或锚点，以及同一批候选段落。<br>
**输出**：与每一跳语义范围一致的段落排序或筛选结果，供后续检索迭代或答案生成器使用。

</div>

**直观理解**：完整问题像一道需要两步以上完成的题，而子问题只要求检查当前一步；把检索时已经写出的“小问题”继续交给验证器，就能避免验证目标与单段证据能力不匹配。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 单段蕴含验证分数

$$
s_{\mathrm{ent}}(q,c)=P\!\left(\mathrm{entail}\mid c,\mathcal{H}(q)\right)
$$

**符号说明**

- $q$：输入问题。
- $c$：作为自然语言推断前提的单个候选段落。
- $\mathcal{H}$：把疑问句转换为答案槽未指定之陈述式假设的规则算子。
- $s_{\mathrm{ent}}(q,c)$：段落对问题假设的蕴含概率，即逐块验证使用的分数。
- $P(\mathrm{entail}\mid\cdot)$：NLI 交叉编码器输出的蕴含类别概率。

<div class="equation-explanation" markdown="1">

**直观理解**：该式询问“仅凭段落 $c$，能否推出由完整问题 $q$ 改写出的陈述”。论文指出，多跳场景下这一前提通常先天不充分，因此低分不等于段落无关，可能只是该段负责推理链中的一跳。<br>
**原文位置**：Section III-B, Entailment

</div>

</div>

<div class="equation-block" markdown="1">

#### 条件式证据补全选择

$$
u_j=P\!\left(\mathrm{entail}\mid c_1\oplus c_j,h\right),\qquad c_2=\underset{j}{\arg\max}\;u_j
$$

**符号说明**

- $c_1$：由问题—段落嵌入相似度确定的第一跳锚点。
- $c_j$：除锚点外的第 j 个候选段落。
- $\oplus$：按输入格式连接两个段落，使其共同构成 NLI 前提。
- $h$：由原问题或当前跳子问题构造的陈述式假设。
- $u_j$：锚点与候选段落联合后对假设的蕴含概率。
- $c_2$：使联合蕴含概率最大的补全段落。

<div class="equation-explanation" markdown="1">

**直观理解**：该选择不再问每段能否独自回答问题，而是固定较可靠的第一跳，再测试哪个候选与它组合后形成充分前提。它把盲目段落对搜索缩减为围绕单一锚点的线性搜索，但锚点错误仍会使后续选择失败。<br>
**原文位置**：Algorithm 1, lines 5–9; Section XI

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：论文没有提出新的参数训练目标，也未对嵌入器、NLI 模型或问题分解器进行微调。方法贡献是推理时改变验证前提与条件变量：从单段 $c_i$ 对完整问题的独立打分，改为锚点联合候选的充分性检查，进一步改为用当前跳子问题构造假设；因此优化表现为离散的排序与 $\arg\max$ 选择，而非反向传播。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 问题—段落嵌入锚定器**

使用 BAAI/bge-small-en-v1.5 双编码器 $E$ 分别编码问题与段落，以重缩放后的余弦相似度排序。该信号主要负责定位问题直接提及的第一跳，而不是独立识别未被问题命名的答案承载段落。

> 直观理解：语义相似度善于找问题中已经出现的人名或主题，因此适合确定起点；论文刻意不让它承担寻找隐藏第二跳的任务。

**2. 客体层假设与蕴含验证器**

规则算子 $\mathcal{H}$ 生成答案槽未指定的陈述，随后由 nli-deberta-v3-base 交叉编码器计算段落前提对该陈述的蕴含概率。论文还定义填入金标准答案的 oracle 假设作为信号上界，但可部署流程不使用金答案。

> 直观理解：“本文包含关于某问题的信息”容易让 NLI 退化为主题匹配；改写成现实世界中的具体陈述，才能让模型检查文本是否真正支持该事实。

**3. 分解条件验证器**

该模块将验证条件从原问题 $q$ 改为当前跳子问题，并可用已有第一跳段落作为分解器的锚定上下文。它与逐块方案可使用完全相同的 NLI 模型和候选段落，改变的核心仅是假设所对应的推理粒度。

> 直观理解：修复来自“问对问题”，而不是堆叠更大的验证模型：单段只需证明它负责的那一步，不必独自证明整条推理链。

**训练与推理**

全部核心流程均在推理阶段执行。条件式选择先以嵌入分数从 $\mathcal{C}$ 取得前 $k$ 个候选并确定 $c_1$，再把 $c_1$ 分别与其余 $k-1$ 个候选连接，由 NLI 模型评分并返回最高分补全段落；分解修复则用 MuSiQue 的金标准子问题分析上界，或让未微调的 Qwen2.5-7B-Instruct根据原问题及首个检索段落生成子问题，再用同一 NLI 模型验证当前跳。最终证据可送入固定生成器回答，论文没有用生成结果反向更新选择器。

**复现信息**

主要蕴含模型为 184M 参数的 nli-deberta-v3-base，并以 44M 的 xsmall 和 435M 的 DeBERTa-v3-large作容量控制；第一跳嵌入器默认采用 33M 参数的 BAAI/bge-small-en-v1.5。端到端条件式实验从检索排序前五段中选择证据，即 $k=5$，因此需要 $k-1=4$ 次 NLI 调用，而盲目段落对搜索需要 $\binom{5}{2}=10$ 次；生成实验采用 Qwen2.5-Instruct 系列与贪心解码。MuSiQue 的三跳和四跳问题不能由固定二段选择器完整覆盖，因此表中的二段端到端比较仅使用其二跳子集；分解验证实验则保留不同跳数，用来检验子问题条件化是否消除随推理深度增加的退化。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HotpotQA distractor：固定随机种子抽取500个问题，每题提供10个候选段落、平均2.0个金标准支持段落。它用于检验典型双跳场景，并区分问题直接点名的桥接段落与包含最终答案的段落。
- 2WikiMultihopQA：抽取500个问题，每题10个候选段落、平均2.5个金标准段落。它提供不同于HotpotQA的数据构造与关系组合，用于判断逐段验证失败是否只属于单一数据集。
- MuSiQue：抽取500个问题，每题20个候选段落、平均2.6个金标准段落，问题需要2、3或4跳推理。其金标准问题分解可直接用于比较原问题验证、金标准子问题验证和自动分解验证，并用于分析跳数增加的影响。另以300个SQuAD v1.1单跳问题作为任务结构控制，每题加入来自同一Wikipedia文章的9个困难负例。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**AUC**

把每个问题的金标准支持段落视为正例、干扰段落视为负例，衡量验证分数将正例排在负例之前的概率。它不依赖某个固定阈值；接近0.5表示接近随机排序。 （越高越好，因为更高的AUC表示验证信号更能把真正证据排在干扰信息之前。）

</div>
<div class="metric-item" markdown="1">

**Exact Match（EM）**

比较生成答案与标准答案经规范化后是否完全一致，用于衡量不同证据选择策略的端到端问答效果。表VIII主要报告逐段过滤或oracle相对最佳可部署选择器的EM点数差。 （越高越好；差值为负表示该选择器降低了最终答题正确率。）

</div>
<div class="metric-item" markdown="1">

**问题分层bootstrap置信区间**

以问题为分层单位进行1000次重采样，为AUC或配对提升估计不确定性，避免把同一问题下多个段落对误当作相互独立样本。 （它不是单调优劣指标；区间越窄表示估计越精确，而比较方法时需结合区间是否覆盖零或是否明显重叠。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三个多跳数据集上的逐段证据判别，并以单跳SQuAD作为任务结构控制

<div class="result-value" markdown="1">

可部署的逐段NLI蕴含评分在HotpotQA、2WikiMultihopQA和MuSiQue上的AUC分别为0.643、0.523和0.560，而相同流程在单跳SQuAD上达到0.951。嵌入相似度在三个多跳数据集上分别达到0.887、0.807和0.762，反而明显高于新增的NLI验证信号。

</div>

作者据此主张，失败并非NLI模型完全不会识别相关证据，而是原始多跳问题要求组合多个段落，单个金标准段落通常不能独立蕴含答案；因此以“单段能否支持完整问题答案”为判据会系统性错杀必要证据。SQuAD对照说明，同一流程在单跳、单段通常足够的条件下可以有效工作。不过，这些AUC结果只证明逐段分数难以区分金标准段落和干扰段落，不能单独证明所有形式的验证都无效，也不能说明嵌入相似度已足以解决端到端多跳问答。

<div class="result-source" markdown="1">

来源：摘要；第IV节表I与第VIII节单跳控制

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Entailment reaches 0.643, 0.523 and 0.560 AUC on HotpotQA, 2WikiMultihopQA and MuSiQue, against 0.951 on single-hop SQuAD.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 三个数据集、三种生成器规模和两个提示词下的端到端证据选择

<div class="result-value" markdown="1">

逐段过滤在所有实验单元中都显著差于完全不过滤；表VIII进一步显示，相对最佳可部署选择器，HotpotQA上的EM差距随生成器从0.5B增至3B而由-4.6扩大到-19.4，2Wiki由0.0扩大到-13.6，MuSiQue分别为-1.9、-11.2和-8.1。

</div>

这说明较弱的段落验证并非只是一个无害的预处理步骤：它会删除生成器完成多跳推理所需的中间证据。作者的解释是，更强的生成器原本更能利用多段证据，因此删证据造成的机会损失更大。该结果支持“不要在多跳RAG中按单段硬门控”的实践建议，但不能推出任何过滤都必然有害；重排序、条件选择和基于分解的验证仍可能有效。此外，0.5B模型的各方法区间高度重叠，低容量条件下的微小差异不宜作强结论。

<div class="result-source" markdown="1">

来源：摘要；第XI节端到端实验；第XIII节表VIII

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

End to end across three datasets, three generator sizes and two prompts, per-chunk gating is significantly worse than not filtering at all in every cell, and its penalty grows with generator capability.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### MuSiQue后续跳验证：原始问题、金标准分解子问题与自动分解子问题的比较

<div class="result-value" markdown="1">

将验证条件改为MuSiQue金标准分解中的后续跳子问题后，NLI AUC从接近随机的0.546升至0.840，配对提升为+0.355，bootstrap区间为[0.331, 0.382]。通用Qwen2.5-7B在同时看到原问题和首个检索段落时生成子问题，AUC达到0.637，约取得金标准分解可用提升的31%；不提供检索内容时仅为0.533。

</div>

核心修复不是换一个更大的验证器，而是让验证器回答范围更合适的问题：当前段落可能不足以支持完整答案，却足以支持某个局部子问题。金标准分解显示该设计存在很高上限；自动分解结果则说明部分收益可由现成模型获得，并且检索到的锚点段落对确定下一跳问题很重要。它尚未证明自动分解已达到实用最优，因为0.637与0.840之间仍有明显差距，而且金标准分解属于不可部署的oracle条件。

<div class="result-source" markdown="1">

来源：摘要；第XII节分解验证实验

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Using MuSiQue’s gold decomposition, entailment on a later hop rises from 0.546, which is chance, to 0.840, a paired lift of +0.355 with a bootstrap interval of [0.331, 0.382].

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

- 嵌入余弦相似度：衡量问题与段落的语义接近程度，也是检索器通常已经使用的信号。它回答新增验证模块是否提供了超出原检索排序的信息。
- 原问题条件下的逐段NLI蕴含评分：把单个段落作为前提，把由原问题构造的陈述作为假设；包括可部署的槽位模板版本和使用金标准答案的oracle版本。这是论文重点批判的标准逐段验证方式。
- 端到端不做过滤的检索结果：将检索到的上下文直接交给生成器。它是关键安全基线，因为一个有用的过滤器至少不应比保留全部证据更差。
- 替代证据选择器：端到端实验还比较重排序器、条件选择器和拥有金标准信息的oracle等，共形成七种选择策略。重排序器代表只改变证据优先级而不依赖逐段充分性判断；oracle给出理想证据选择的上界。原文节选未完整列出七种选择器的全部名称与定义。

**实验想回答的问题**

- 逐段验证器能否在多跳问答中把支持答案的金标准段落排在干扰段落之前，并据此安全地过滤检索结果？如果不能，失败究竟来自模型容量、阈值、文本长度或检索器等实现因素，还是来自“单段证据不足以回答原问题”这一结构性矛盾？
- 将验证条件从原始多跳问题改为与当前证据对应的分解子问题，能否恢复蕴含判断能力，并进一步改善端到端问答中的证据选择？

**实验实现**

所有候选段落均在每个问题内部评分，不建立全局语料索引；三个多跳数据集共形成20000个“问题—段落”对。默认NLI模型为184M参数的nli-deberta-v3-base，并以44M和435M版本做容量控制；作者先用两个无歧义NLI样例核验标签索引。端到端生成使用Qwen2.5-Instruct系列，考察0.5B、1.5B和3B三种规模、两个提示词，并采用贪心解码与随机种子1337。主分析以AUC衡量段落判别，以EM衡量最终问答；置信区间采用按问题分层的1000次bootstrap。单跳SQuAD控制使用同一Wikipedia文章内的段落作为困难负例，以避免负例过于容易。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| MuSiQue按所需推理跳数分组 | 嵌入相似度的AUC随跳数由2跳的0.819下降到4跳的0.677，对应区间分别为[0.802, 0.837]和[0.646, 0.709]；NLI曲线也下降，但区间重叠，因此作者只报告趋势而不宣称显著差异。4跳时可部署NLI与随机水平的距离不超过0.04。 | 该分组隔离了组合深度的影响：需要更多跳时，原问题与后续证据之间的直接词义和蕴含联系更弱，逐段验证因而进一步退化。嵌入曲线提供了显著的单调退化证据；NLI部分只能支持方向性观察，不能依据现有区间断言各跳数组之间均存在统计显著差异。 | 图2及其图注；第VI节<br><span class="experiment-evidence">Embedding similarity degrades significantly with hop count, from 0.819 [0.802, 0.837] at two hops to 0.677 [0.646, 0.709] at four.</span> |
| 充分性与前提长度控制：组合金标准段落，或把金标准段落与干扰段落配对 | 两个金标准段落合并后AUC达到0.881；金标准段落与干扰段落配对虽然前提更长，却只得到0.127，而对应比较值为0.540。 | 这一控制区分了“文本更长导致NLI退化”和“前提是否包含完整推理链”两种解释。如果长度是主因，更长的金标准组合不应显著改善；实际结果相反，只有共同提供充分证据的段落组合明显有效，而加入无关文本并不能修复判断。因而作者将根因归于充分性而非长度。不过，节选未完整展示0.127与0.540所对应条件的表头，具体列定义仍需对照原论文表格复核。 | 第I节实验概述；第VII节充分性与长度控制<br><span class="experiment-evidence">Both gold paragraphs together reach 0.881 AUC; a gold paired with a distractor scores 0.127 against 0.540, at greater length.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It analyzes multi-hop RAG verification failures and repairs them through question decomposition conditioned on intermediate reasoning hops.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`646bf2d6eae5f889f7d4937f126d2b9cf81b3e91729cedd2531a4406e309bb45`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
