---
title: "[论文解读] When Text Misleads: Inconsistent-Aware Reasoning for Audio-Grounded Dialogue"
description: "[arXiv 2608.27176][LLM 评测] 本文以“文本含义与语音表达相冲突”为切入点，构建可区分跨模态冲突与一致情形的口语对话评测，并探索用显式、可检查的声学证据纠正文本捷径。"
arxiv_id: "2608.27176"
announcement_date: "2026-08-28"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:42:44.478776+00:00"
source_sha256: "f45104f72bf5a068dd7ce256ac8037f155a6cc090b632c03c8719bfd4c95fb2c"
tags:
  - "LLM 评测"
  - "LLM 其他"
  - "LLM Reasoning"
  - "口语对话理解"
  - "跨模态分歧"
  - "语音落地"
  - "模态捷径"
  - "副语言声学线索"
  - "ContraTalk"
  - "Audio Twin"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.27176</p>

# When Text Misleads: Inconsistent-Aware Reasoning for Audio-Grounded Dialogue

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Yen-Ju Lu, Yuzhe Wang, Yaohan Guan, Xiluo He, Jiarui Hai, Mingrui Liang, Kaavya Chaparala, Thomas Thebaud, Laureano Moro-Velazquez, Najim Dehak, Jesus Villalba</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Center for Language and Speech Processing, Johns Hopkins University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27176v1) · [PDF 下载](https://arxiv.org/pdf/2608.27176v1) · **关键词** 口语对话理解, 跨模态分歧, 语音落地, 模态捷径, 副语言声学线索, ContraTalk, Audio Twin<br>


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

本文以“文本含义与语音表达相冲突”为切入点，构建可区分跨模态冲突与一致情形的口语对话评测，并探索用显式、可检查的声学证据纠正文本捷径。

**不用术语来说**：同一句话写成文字后可能显得礼貌、自信或赞同，但说话人的语调、停顿、情绪和表达方式却可能透露出不满、犹豫或反对。现有系统即使回答正确，也可能只是猜中了文字表面意思，并未真正听懂声音；因此，需要一种评测来判断模型何时应相信文本、何时应依据语音修正文本，以及在两者一致时能否避免被不必要的声学分析带偏。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将“跨模态分歧”明确为口语对话理解中的关键失效场景，并提出 ContraTalk：从文本表面解释与语音落地解释的分歧区域构造受控问答，同时保留二者一致的样例，以分别检验模型纠正文本误导和维持正确文本判断的能力。
- 作者提出 Audio Twin 推理框架，把局部韵律、情感、时序及说话行为等语音线索转换为可供语言模型读取、检索和比较的文本化证据，使模型能够显式决定这些证据应确认还是推翻转写文本所暗示的解释。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于口语对话理解与多模态推理研究。系统不仅要利用转写文本中的词汇和语义，还要结合音频中的副语言信息，例如韵律、情绪、停顿、说话方式和互动节奏，以判断说话者的真实状态与意图。现有评测常可仅凭文本或某一种模态完成，导致模型学习“模态捷径”：即使任务名义上包含音频，模型也可能忽略声音证据。本文关注更严格的情形——文本给出的表层解释看似合理，却与音频支持的解释不一致；此时系统必须比较两类证据，而不能默认文本正确。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**副语言声学线索**

指不等同于词语内容、但能通过声音传递信息的特征，如音高、语速、音量、停顿、情绪色彩和说话风格。它们可揭示犹豫、讽刺、压抑的不满或会话意图，而这些信息通常无法从逐字转写中恢复。

</div>
<div class="concept-item" markdown="1">

**模态捷径与模态坍缩**

模态捷径是模型依赖最容易预测答案的单一信息源，而非真正整合文本与音频；当另一模态在功能上被忽略时，本文称其为模态坍缩。口语任务中常见的情况是文本语义过强，使模型几乎不使用声学证据。

</div>
<div class="concept-item" markdown="1">

**跨模态分歧**

指转写文本支持的表层解释与音频中的韵律、情感或互动线索支持的解释不同。本文将这种分歧视为检验真实语音落地能力的核心条件，因为正确作答需要用声音证据修正、细化或否定文本推断。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是一段带有转写文本的口语对话以及关于该对话的问题，输出是对互动行为、情绪状态、对话行为、社会立场或会话意图的正确判断。评测同时包含两种受控设置：在“冲突样例”中，文本会诱导出合理但错误的陷阱解释，正确答案必须依据音频或互动线索确定；在“一致样例”中，文本解释与语音落地解释相符，用于检查模型是否能在没有冲突时保留有效的文本推理，而不是机械地反对文本。该设置的关键假设是，获得音频输入并不等于真正使用音频：模型只有在跨模态分歧出现时避开文本偏置陷阱，才能体现可验证的语音落地推理能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **视觉问答中的语言先验研究（Goyal et al., 2017）**: 该研究表明，多模态模型可能利用语言先验而非视觉证据作答，为本文所讨论的“名义上多模态、实际上依赖单一模态”的评测缺陷提供了直接类比。本文将这一问题具体化到口语对话中的转写文本捷径。
- **AIR-Bench、AudioBench 与 MMAU 等音频语言评测**: 这些基准评估音频语言理解、组合推理或指令遵循，但原文认为其模态通常是合作、互补或各自可提供答案的。ContraTalk 的区别在于刻意构造文本与语音证据发生冲突的对话问题，以检验模型能否在二者之间进行证据仲裁。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

口语对话的真实含义同时依赖词汇内容和副语言声学信号。反讽、克制的不满、犹豫、礼貌包装下的拒绝等现象往往无法从转写文本恢复；若系统只依赖文字，就可能在情绪状态、社会立场、对话行为和交际意图上作出表面合理但实际错误的判断。这会使高基准分数掩盖模型没有真正依据语音进行推理的事实，也降低系统在真实交互中的可靠性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **以转写文本或单模态特征为主的评测与建模**：模型主要从词汇和语义模式预测答案，或利用数据集中与标签相关的单一声学线索；如果仅凭一种模态即可完成任务，模型就不必比较文本与语音证据。此类设置容易产生“模态坍缩”，即名义上的多模态系统实际上忽略了另一模态。
- **直接音频语言模型的隐式多模态融合**：模型同时接收语音及文本相关信息，并在内部表示中融合两类信号。它具备访问音频的能力，但声学线索如何被定位、选择以及用于修正文本解释通常不可见，也缺少显式机制来判断当前样例是否真的需要以音频推翻文字表面含义。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 许多既有基准允许模型依靠语言先验、词汇相关性或数据集偏差获得正确答案，因而无法区分“真正基于语音理解”与“利用转写文本走捷径”；结果是总体准确率可能高估模型处理跨模态冲突的能力。
- 仅把音频提供给模型并不保证有效落地：隐式融合仍可能选择文本诱导的错误解释，而且在文本与语音一致时，噪声声学线索还可能破坏原本正确的文本判断。因此，系统既要知道何时修正，也要知道何时不修正。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种受控而可扩展的评测框架，能够把“文本表面解释合理但被声学证据否定”的冲突样例与“文本和语音支持同一答案”的一致样例明确分开。相应地，也缺少一种可审计的推理接口，用于展示模型提取了哪些局部声学证据、如何比较竞争解释，以及这些证据为何足以确认或推翻文本判断。

</div>
<div markdown="1"><span>核心问题</span>

在口语对话问答中，能否通过显式识别文本—语音分歧并聚合可读的局部声学证据，使模型在冲突情形下减少文本捷径、依据语音修正答案，同时在一致情形下保持校准而不过度使用音频？

</div>
<div markdown="1"><span>作者直觉</span>

作者的直觉是：最能暴露模型是否真正“听懂”的，不是文本与音频都指向同一答案的普通样例，而是二者给出竞争解释的边界情形。进一步地，与其让推理模型面对不透明的整段音频并期待其自动融合，不如先把语调、停顿、情感和互动行为定位并整理成 Audio Twin，再让模型像核对证词一样比较这些证据与文本表面解释。这样既能追踪模型为何改判，也能在证据不足时保留原有文本判断。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文的方法包含相互配合的两部分。第一部分构建诊断基准 ContraTalk：从带音频、时间戳转写和说话者状态提示的 Seamless Interaction Dataset 出发，分别生成“仅看文字时最自然的表层解释”和“结合语音线索后的落地解释”；若二者不同，则把前者设置为具有迷惑性的文本偏置选项，形成 conflict 样例，若二者一致，则形成 consistent 样例。说话者提示只用于数据构造，不会在评测时提供给模型；最终样例还经过自动检查和针对性人工复核。
第二部分是用于回答这些问题的 Audio Twin 推理框架。系统先从音频中提取韵律、情感、流利度、时序及重叠说话等特征，并按说话者和对话轮次与转写对齐，转换为可由语言模型读取的结构化文本证据 $E_{\mathrm{AT}}$。面对具体问题时，系统先规划需要哪些声学证据，再从转写中定位相关轮次，检索对应的 Audio Twin 条目，最后让推理模型联合完整转写 $T$、检索证据 $E_q$、问题 $q$ 和候选集 $\mathcal{C}$ 选择答案。通俗地说，它不是要求语言模型直接从一段不透明的音频中自行发现所有线索，而是先把“怎么说的”整理成带位置标签的证据卡，再与“说了什么”进行显式比较。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造跨模态解释与评测区域

分别提出转写驱动的表层解释 $\hat{y}_T$ 与结合音频的语音落地解释 $\hat{y}_{TA}$；根据二者是否相等，将候选样例划入 conflict 或 consistent 区域。

<div class="method-step__io" markdown="1">

**输入**：Seamless Interaction Dataset 中的 spoken dialogue、时间戳转写 $T$、音频 $A$，以及仅在构造阶段使用的说话者提示。<br>
**输出**：带有跨模态关系标签的候选解释，以及后续生成选择题所需的正确答案和潜在干扰项。

</div>

**直观理解**：先分别问“只读字幕会怎么理解”和“真正听过语音后会怎么理解”。两种理解不同的地方正是检验模型是否会被文字误导的关键区域。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成并验证 ContraTalk 问答样例

将 conflict 区域的文本表层解释放入选项，作为合理但错误的 text-biased distractor，并以语音落地解释为正确答案；consistent 区域不定义单独的误导选项，随后执行自动检查、泄漏过滤、修订和针对性人工复核。

<div class="method-step__io" markdown="1">

**输入**：候选解释、原始对话证据，以及 interaction behavior、emotion state、dialogue act、social stance、conversational intent 五类话语维度。<br>
**输出**：包含 501 道多项选择题的 ContraTalk，其中 conflict 为 333 题、consistent 为 168 题。

</div>

**直观理解**：冲突题有意保留一个“只看字幕很容易选中”的陷阱；一致题则检查系统在无需用音频纠正文字时，是否仍能稳定作答而不过度纠正。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立问题无关的 Audio Twin

Audio Twin 构建器以 $T$ 和 $F$ 为输入，将韵律、情感、流利度、说话时序、重叠及必要的说话者相对基线转换为结构化、文本可读且与轮次和说话者绑定的证据。

<div class="method-step__io" markdown="1">

**输入**：对话 $D=(T,A)$，其中 $T$ 是带时间信息的转写，$A$ 是对应音频；语音前端从 $A$ 提取并与转写轮次对齐的特征 $F$。<br>
**输出**：问题无关的完整证据结构 $E_{\mathrm{AT}}$。

</div>

**直观理解**：这一步像为整段对话制作一套索引化证据卡，例如标出某轮“比该说话者平时更快、更响、明显犹豫”或“两人发生重叠”。它把难以直接检查的声波变成语言模型能够比较和引用的文字证据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 规划问题所需证据并定位转写锚点

问题条件化的证据计划 $\pi_q$ 指定应检索的声学证据类型，transcript locator 据此从 $U$ 中选择少量相关锚点 $S_q$，但此阶段不选择答案。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、目标话语维度、完整转写所诱导的轮次集合 $U=\{u_i\}_{i=1}^{N}$。<br>
**输出**：证据计划 $\pi_q$ 与相关轮次集合 $S_q\subseteq U$。

</div>

**直观理解**：系统先决定应该听什么、去哪里找，而不是边看字幕边猜答案。例如情绪题优先查语调和强度，打断题则优先查轮次边界与重叠。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 跨模态分歧与一致性定义

$$
\hat{y}_{T}=f_{T}(T,q,\mathcal{C}),\qquad \hat{y}_{TA}=f_{TA}(T,A,q,\mathcal{C});\qquad \text{conflict: }\hat{y}_{T}\neq\hat{y}_{TA},\ y^{\star}=\hat{y}_{TA},\qquad \text{consistent: }\hat{y}_{T}=\hat{y}_{TA}=y^{\star}.
$$

**符号说明**

- $T$：对话转写，主要承载词汇和句面内容。
- $A$：与转写对应的音频，包含韵律、情感和互动方式等副语言信息。
- $q$：针对该对话提出的问题。
- $\mathcal{C}=\{c_1,\ldots,c_K\}$：由 K 个候选答案组成的集合。
- $f_T$：只使用转写进行回答的推断函数。
- $f_{TA}$：联合使用转写与音频进行回答的推断函数。
- $\hat{y}_T$：仅由转写诱导的表层答案。
- $\hat{y}_{TA}$：结合完整口语对话证据后得到的语音落地答案。
- $y^{\star}$：评测使用的正确答案。

<div class="equation-explanation" markdown="1">

**直观理解**：该定义决定样例究竟测试“纠错”还是“保持”。若只看字幕与听过音频后的答案不同，正确答案取后者，前者可成为文本偏置陷阱；若二者相同，则模型不应为了表现出使用音频而无端改答案。<br>
**原文位置**：第 3.1 节 Problem Formulation

</div>

</div>

<div class="equation-block" markdown="1">

#### Audio Twin 构建、检索与回答

$$
E_{\mathrm{AT}}=\phi_{\mathrm{AT}}(T,F),\qquad S_q=\pi_q(U,q),\ S_q\subseteq U,\qquad E_q=\mathcal{R}(E_{\mathrm{AT}},S_q,\pi_q),\qquad \hat{y}=f(T,E_q,q,\mathcal{C}).
$$

**符号说明**

- $F$：语音前端提取并与转写轮次对齐的声学及副语言特征。
- $\phi_{\mathrm{AT}}$：把转写和对齐语音特征转换为 Audio Twin 的构建函数。
- $E_{\mathrm{AT}}$：覆盖整段对话、与问题无关的结构化 Audio Twin 证据。
- $U=\{u_i\}_{i=1}^{N}$：由转写划分出的 N 个对话轮次集合。
- $\pi_q$：根据问题制定证据类型并选择相关轮次的证据计划。
- $S_q$：由证据计划选出的相关转写锚点集合。
- $\mathcal{R}$：依据锚点和计划从 Audio Twin 中取回证据的检索函数。
- $E_q$：与当前问题相关、且与转写对齐的声学证据子集。
- $f$：联合完整转写、检索证据、问题和候选答案执行选择的推理函数。
- $\hat{y}$：系统最终预测的候选答案。

<div class="equation-explanation" markdown="1">

**直观理解**：方程描述了完整的信息流：先把整段语音变成可查询的证据库，再由问题决定关注哪些轮次和证据类型，最后把取回的“怎么说”与完整的“说了什么”交给回答模型。关键设计是 $E_{\mathrm{AT}}$ 在看到具体问题前就建立，而 $E_q$ 才是面向问题筛选出的子集，从而将证据生成和答案选择分开。<br>
**原文位置**：第 4.1 节 Overview、第 4.2 节 Audio Twin Representation 与第 4.3 节 Agentic-style Evidence Retrieval

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。所给章节把 Audio Twin 描述为 agentic-style 推理框架，没有给出参数训练、监督损失或端到端优化目标；核心函数 $\phi_{\mathrm{AT}}$、$\pi_q$、$\mathcal{R}$ 和 $f$ 表示构建与推理流程，而不是文中声明的可微联合训练目标。ContraTalk 的 conflict/consistent 定义也是数据构造和评测规则，不能当作训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Audio Twin 构建器**

语音前端先产生声学与副语言特征 $F$，再按时间戳将其对齐到转写轮次和说话者；构建器 $\phi_{\mathrm{AT}}$ 将这些特征文本化为结构化证据 $E_{\mathrm{AT}}$。证据覆盖韵律、情感、流利度、时序和重叠，适用时还使用说话者自身基线表达相对的音量、语速或犹豫程度。

> 直观理解：该模块解决“语言模型看到字幕后忽略音频”以及“音频对模型而言过于不透明”的问题。相对说话者基线尤其重要，因为同样的绝对语速对不同说话者未必表示同一种状态。

**2. 证据计划与转写定位器**

证据计划 $\pi_q$ 由问题及目标话语维度决定需要的证据类别，并从轮次集合 $U$ 中产生锚点 $S_q$；定位过程与最终答案选择分离，以减少先猜选项、再选择性寻找支持证据的风险。

> 直观理解：它相当于先列出检查清单并圈定录音片段，而不是把整套声学描述一次性塞给模型。这样既降低无关信息干扰，也让检索过程更便于诊断。

**3. 检索与跨模态比较推理器**

检索器根据 $E_{\mathrm{AT}}$、$S_q$ 和 $\pi_q$ 形成问题相关证据 $E_q$；回答函数 $f$ 同时读取完整转写 $T$ 与 $E_q$，在候选集 $\mathcal{C}$ 中选择最受证据支持的答案。$E_q$ 不是外部知识，而是与当前对话转写对齐的语音证据。

> 直观理解：该模块不假定音频永远推翻字幕，也不假定字幕永远可靠，而是比较两者。因而它既能在 conflict 样例中纠正文字陷阱，也应在 consistent 样例中保留原本正确的文字解释。

**训练与推理**

数据构造阶段，作者利用 Seamless Interaction Dataset 的音频、转写和说话者提示提出转写表层解释与语音落地解释，并据其一致性生成 conflict 或 consistent 多项选择题；提示仅作为构造时信号，不向受评模型开放。候选样例经过自动检查及定向人工审查：互补系统产生分歧的样例被优先复核，系统一致的样例则抽样审计；审查者在不知道说话者提示的条件下听音频，并检查转写、问题、选项和答案。
推理阶段不需要访问构造时提示。系统首先由 $T$ 和音频特征 $F$ 一次性建立问题无关的 $E_{\mathrm{AT}}$；随后针对每个 $q$ 形成 $\pi_q$，在不提前选择答案的情况下定位 $S_q$，再检索得到 $E_q$。最终模型联合完整词汇上下文 $T$ 与局部语音证据 $E_q$，从 $\mathcal{C}$ 中输出 $\hat{y}$。这一设计的判断标准不是“是否总使用音频推翻文字”，而是 conflict 时根据音频纠正表层解释、consistent 时保持已由两种模态共同支持的答案。

**复现信息**

公平解释该方法至少需要保留三点。第一，Audio Twin 的输入是带时间戳的转写与对齐语音特征，证据必须绑定对话轮次和说话者；否则无法复现基于锚点的检索。第二，证据应覆盖韵律、情感、流利度、时序和重叠，并在有意义时提供说话者特定基线，因为框架依赖相对变化而不只是绝对声学值。第三，回答时向模型提供完整转写，但只提供由计划和锚点检索出的相关 Audio Twin 证据；这一区分是控制上下文噪声并诊断跨模态推理的关键。
所给正文没有明确报告具体语音前端、证据卡字段格式、对齐可靠性算法、特征文本化模板、推理模型提示词或模型参数；原文将这些内容分别指向附录 F 和附录 G，因此不能仅凭当前节选补造。基准方面可确认其使用 Seamless Interaction 的全部 117 个带标签测试对话生成 501 题，并对其中 350 题由七名审查者进行人工复核；这些数字描述数据覆盖与质量控制，而不是模型训练规模。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ContraTalk：受控的音频落地对话理解基准，共含 501 道多项选择题。每个实例由对话音频 $A$、转写 $T$、问题 $q$ 和候选集合 $\mathcal{C}=\{c_1,\ldots,c_K\}$ 构成，覆盖交互行为（IB）、情绪状态（ES）、会话意图（CI）、对话行为（DA）和社会立场（SS）五个维度。
- 冲突样本：文本表面解释与经人工核验的语音落地解释不一致、信息不足或具有误导性。正确答案对应实际说话方式所支持的解释，另设一个在仅看转写时仍很合理的文本偏置干扰项，用于诊断模型是否真正使用韵律、情绪或说话风格等声学证据。
- 一致样本：转写解释与语音落地解释相符，正确答案同时受文本和语音支持。该划分不是为了测试音频纠错，而是检查音频模型或代理式推理系统是否会在原本可由文本正确解决的问题上引入新的错误。原文节选未给出冲突与一致样本各自的具体数量。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（Accuracy）**

模型选择金标准答案的比例；在冲突样本上反映能否依据声学信息纠正文本表面解释，在一致样本上反映能否保留文本与语音共同支持的答案。论文按五个话语维度及总体结果报告。 （越高越好，因为更高值表示更多问题被正确回答；但仅凭一致样本的高准确率不能证明模型真正利用了音频。）

</div>
<div class="metric-item" markdown="1">

**误导率（Mislead Rate）**

模型选择文本偏置表面干扰项的比例，只适用于定义了该结构化陷阱的冲突样本。它比一般错误率更具体地区分“被转写误导”与其他类型的错误。 （越低越好，因为较低值表示模型较少沿用与声学证据冲突的文本表面解释。）

</div>
<div class="metric-item" markdown="1">

**按类别结果（IB、ES、CI、DA、SS）**

分别报告五种话语维度上的准确率和误导率，用于判断系统改善是否集中于某类线索，例如情绪状态或会话意图，而非只看总体平均值。 （准确率越高、误导率越低越好；类别分解还能揭示相同总体分数背后的能力差异。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 文本-only 模型在冲突样本上的捷径暴露

<div class="result-value" markdown="1">

五个文本-only 模型的总体准确率仅为 33.0%—47.7%，总体误导率为 34.5%—45.0%。其中表现最好的 Sonnet 4.5 达到 47.7% 准确率，但仍有 34.5% 的样本选择文本偏置干扰项；Haiku 4.5 的准确率最低，为 33.0%，误导率最高，为 45.0%。

</div>

作者结果支持 ContraTalk 确实能暴露转写捷径：即便是强文本模型，也会把语义上合理但与实际说话方式冲突的选项当成答案。分析上，低准确率和高误导率共同说明问题不只是一般知识不足，而是模型受到文本表面解释系统性牵引。不过，这些结果只针对构造出的冲突区域，不能直接推出模型在所有真实语音对话任务上都同样失败。

<div class="result-source" markdown="1">

来源：表 2（Shortcut diagnostic），Text-only LLMs；数字顺序依次为五类及总体准确率、五类及总体误导率

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Haiku 4.5 36.8 26.7 28.4 44.6 31.3 33.0 47.1 53.3 50.7 37.5 34.3 45.0
Sonnet 4.5 57.4 40.0 47.8 50.0 44.8 47.7 29.4 41.3 38.8 32.1 29.9 34.5

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 直接 Audio-LLM 在冲突样本上的音频落地能力

<div class="result-value" markdown="1">

直接 Audio-LLM 的总体准确率介于 33.6% 和 46.8% 之间，总体误导率介于 29.7% 和 39.9% 之间。StepAudio-R1 获得该组最高总体准确率 46.8%，但仍有 32.1% 的总体误导率；StepAudio-2 的误导率最低，为 29.7%，但准确率仅为 39.3%。

</div>

直接输入音频并未稳定解决跨模态冲突：某些模型减少了文本陷阱选择，却没有同步提高正确率，说明它们可能只是转向其他错误，而非准确提取并推理声学证据。该结果证明“具有音频接口”不等于“可靠落地于音频”；但由于不同 Audio-LLM 的模型规模、训练数据和架构并不完全受控，不能把所有差异仅归因于输入模态。

<div class="result-source" markdown="1">

来源：表 2（Shortcut diagnostic），Audio-LLMs；数字顺序依次为五类及总体准确率、五类及总体误导率

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

StepAudio-R1 42.6 45.3 47.8 50.0 49.3 46.8 36.8 30.7 35.8 30.4 26.9 32.1
StepAudio-2 44.1 38.7 37.3 35.7 40.3 39.3 22.1 34.7 32.8 39.3 20.9 29.7

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Audio Twin 与匹配文本骨干的冲突样本比较

<div class="result-value" markdown="1">

Sonnet 4.5 加入 Audio Twin 后，总体准确率由 47.7% 提升到 50.5%，增加 2.8 个百分点；总体误导率由 34.5% 降至 29.4%，下降 5.1 个百分点。其 CI 准确率由 47.8% 提升到 55.2%，DA 准确率由 50.0% 提升到 55.4%。

</div>

这是最清晰的配对改善：显式把声学线索整理成文本可读证据，既提高了正确答案选择率，也降低了文本陷阱选择率，说明 Audio Twin 不只是改变答案分布，而是在该骨干上改善了音频落地。然而提升依赖骨干，不能据此断言所有模型都会获益；其他配对结果并非全面优于原文本模型。

<div class="result-source" markdown="1">

来源：表 2（Shortcut diagnostic），Text-only LLMs 与 Audio Twin Reasoning；数字顺序依次为五类及总体准确率、五类及总体误导率

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Sonnet 4.5 57.4 40.0 47.8 50.0 44.8 47.7 29.4 41.3 38.8 32.1 29.9 34.5
Sonnet 4.5 + AT 50.0 46.7 55.2 55.4 46.3 50.5 27.9 37.3 28.4 26.8 25.4 29.4

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

- 文本-only LLM：DeepSeek V3.1、Nova 2 Lite、Claude Haiku 4.5、Sonnet 4.5 和 Opus 4.7。它们仅根据转写作答，是测量“文本捷径”强度的关键对照；若其频繁选择预设的表面干扰项，就说明问题确实要求超越词面内容。
- 直接 Audio-LLM：包括 AudioFlamingoNext、StepAudio-R1、StepAudio-2、MIMOAudio、Qwen2.5-Omni、KimiAudio、Qwen3-Omni 和 GPT-4o-Audio-Mini。它们直接接收语音，用来检验“可访问音频”是否自然等价于“有效利用声学证据”。
- Audio Twin 推理系统：分别以 Haiku 4.5、Sonnet 4.5 和 Opus 4.7 为推理骨干，将局部声学线索转成模型可阅读的结构化文本表示后再推理。与相应文本-only 骨干的配对比较，主要用于判断显式汇总声学证据是否优于仅依赖转写。
- QA-only 质量控制基线：模型只接收问题和候选答案，不接收转写或音频。若仍能根据题面形式或选项关系推出答案，实例会被重写并复测，仍存在捷径者被删除；该基线用于控制数据伪影，而非与最终系统竞争性能。

**实验想回答的问题**

- ContraTalk 的冲突样本能否揭示“转写文本捷径”：当文本表面含义与声学线索冲突时，仅看转写的模型是否会选择专门设计的文本偏置干扰项，以及直接接收音频能否消除这一偏差？
- 显式 Audio Twin 声学证据推理相较文本推理和直接音频推理，能否提高冲突样本准确率、降低误导率，同时在无需音频纠正的一致样本上保留原有能力？

**实验实现**

评测采用多项选择协议：模型基于可用输入，从候选集合 $\mathcal{C}$ 中选择答案。三种输入与推理方式分别是仅转写、直接语音，以及先将局部声学线索转成 Audio Twin 再交给文本推理骨干。冲突样本同时报告准确率与误导率，一致样本只报告准确率；结果按五类话语现象和总体汇总。论文说明采用对话级 bootstrap 计算 95% 置信区间，但所给节选未包含具体区间。基准构建还经过 QA-only 自动筛查和人工核验：冲突样本优先人工检查两个自动验证器意见不一致的项目，一致样本则采用随机抽样质检。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Haiku 4.5：加入 Audio Twin 前后 | 加入 Audio Twin 后，总体准确率从 33.0% 升至 43.2%，增加 10.2 个百分点；总体误导率从 45.0% 降至 30.9%，下降 14.1 个百分点。五类准确率中，CI 从 28.4% 升至 46.3%，ES 从 26.7% 升至 37.3%，但 IB 从 36.8% 升至 39.7%，改善较小。 | 这一配对近似隔离了“显式声学证据表示”的作用：推理骨干名称保持一致，变化来自加入 Audio Twin 流程。大幅下降的误导率说明结构化声学线索尤其能抑制弱骨干沿用文本陷阱；但论文节选未说明调用配置是否完全一致，因此它仍不是严格的单变量实验。 | 表 2（Shortcut diagnostic），Haiku 4.5 与 Haiku 4.5 + AT<br><span class="experiment-evidence">Haiku 4.5 36.8 26.7 28.4 44.6 31.3 33.0 47.1 53.3 50.7 37.5 34.3 45.0
Haiku 4.5 + AT 39.7 37.3 46.3 51.8 43.3 43.2 22.1 38.7 35.8 26.8 29.9 30.9</span> |
| Opus 4.7：加入 Audio Twin 前后 | 加入 Audio Twin 后，总体准确率由 45.3% 小幅升至 46.8%，增加 1.5 个百分点；总体误导率却由 36.9% 降至 34.8%，仅下降 2.1 个百分点。类别变化不一致：CI 准确率从 40.3% 升至 52.2%，但 IB 从 61.8% 降至 51.5%，ES 从 40.0% 降至 36.0%。 | 该对照揭示 Audio Twin 并非普遍增益组件：它可能帮助模型处理需要声学意图解释的类别，同时损害原本依靠文本即可较好判断的类别。因而总体平均值会掩盖证据注入带来的能力重分配，也支持作者关于一致样本表现依赖骨干的判断。 | 表 2（Shortcut diagnostic），Opus 4.7 与 Opus 4.7 + AT<br><span class="experiment-evidence">Opus 4.7 61.8 40.0 40.3 48.2 37.3 45.3 20.6 46.7 44.8 32.1 38.8 36.9
Opus 4.7 + AT 51.5 36.0 52.2 51.8 44.8 46.8 36.8 38.7 32.8 26.8 37.3 34.8</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces a controlled benchmark for transcript-shortcut failures and an acoustic-evidence framework for improving speech-grounded LLM reasoning.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`f45104f72bf5a068dd7ce256ac8037f155a6cc090b632c03c8719bfd4c95fb2c`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
