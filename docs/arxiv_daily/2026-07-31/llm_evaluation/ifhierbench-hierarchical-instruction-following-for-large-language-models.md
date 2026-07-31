---
title: "[论文解读] IFHierBench: Hierarchical Instruction Following for Large Language Models"
description: "[arXiv 2607.27912][LLM 评测] 本文指出，现有基准因把输出约束视为作用于整段回答的扁平清单，无法评估大语言模型能否在正确的嵌套区域内满足约束，因此提出以分层作用域和确定性检查器测量这一能力的 IFHierBench。"
arxiv_id: "2607.27912"
announcement_date: "2026-07-31"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:48.964733+00:00"
source_sha256: "e14f2dd557bf9eff1b6cf6097f9014e7b99c8175fbcd0da9fe96f27082eae336"
tags:
  - "LLM 评测"
  - "LLM 其他"
  - "大语言模型"
  - "指令遵循"
  - "层次化约束"
  - "约束作用域"
  - "确定性检查器"
  - "基准评测"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2607.27912</p>

# IFHierBench: Hierarchical Instruction Following for Large Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Mao, Yuetian, Chen, Chunyang</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27912) · [PDF 下载](https://arxiv.org/pdf/2607.27912) · **关键词** 大语言模型, 指令遵循, 层次化约束, 约束作用域, 确定性检查器, 基准评测<br>
**代码**: [https://anonymous.4open.science/r/IFHierBench-0087](https://anonymous.4open.science/r/IFHierBench-0087)

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

本文指出，现有基准因把输出约束视为作用于整段回答的扁平清单，无法评估大语言模型能否在正确的嵌套区域内满足约束，因此提出以分层作用域和确定性检查器测量这一能力的 IFHierBench。

**不用术语来说**：现实中的一次模型调用常被要求生成完整的复杂产物，例如一份含多个章节、子章节和字段的报告，而且不同要求只适用于各自指定的部分。模型即使写出了要求的关键词或格式，也可能把它放错章节，甚至漏掉承载该内容的外层结构；传统测试往往只检查整篇回答中是否出现目标内容，因而会把这类结构性失败误判为成功。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 IFHierBench：包含 600 个提示，按约束树深度 $0$ 至 $3$ 分层，每个深度 150 个；基准覆盖 35 类可编程检查的约束，其中 10 类结构约束来自对 GitHub 上 1,232 个真实大语言模型应用提示的经验分析，另外 25 类内容约束取自 IFEval 和 ComplexBench。
- 构建从任务到分层约束树、自然语言提示和确定性分层检查器的数据合成流程，使每项约束都能在其指定输出区域内接受代码验证，而不依赖模型裁判。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型指令遵循评测领域。现实应用不仅要求模型生成语义正确、语言流畅的内容，还要求输出满足可客观核验的格式、结构、长度以及关键词等约束；例如，一份报告可能整体采用 Markdown，包含指定数量的二级标题，而某个二级标题下的特定子节又必须是一句话并包含指定词语。随着长上下文模型和智能体框架的发展，过去由多个短提示和外部程序分步完成的任务，越来越多地被合并为一次模型调用，因此约束会同时作用于完整输出、主要章节和嵌套字段。本文关注的核心场景正是这种具有不同作用域和多层嵌套关系的指令遵循，而不是仅检查整段回答是否满足一组扁平约束。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**输出约束**

输出约束是用户对模型回答施加的可检查要求，例如必须使用 JSON、包含三个章节、限制句子数量，或必须出现或禁止出现某个关键词。本文主要研究能够由确定性程序判断是否满足的约束，而非依赖主观质量评价的要求。

</div>
<div class="concept-item" markdown="1">

**约束作用域**

作用域指某项约束应当检查输出中的哪个区域：它可能作用于完整回答，也可能只作用于某个章节或嵌套字段。即使关键词出现在全文中，若它没有出现在指定子节内，对该子节的约束仍应判定为失败。

</div>
<div class="concept-item" markdown="1">

**层次化约束树**

层次化约束树用父子关系表示输出结构及其局部要求：父节点约束较大的输出区域，子节点约束其中更小的嵌套区域。树的深度反映约束嵌套程度，深层约束只有在对应的外层结构被正确生成后，才能在正确作用域内得到检查。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个自然语言提示，其中同时描述任务内容以及分布在完整输出、结构化章节和嵌套字段上的多层约束，模型需要通过一次调用生成完整回答。评测不仅检查回答中是否出现某种表面特征，还必须先定位每项约束对应的输出区域，再由确定性 Python 检查器判断该区域是否满足要求。IFHierBench据此构建了 600 个提示，按约束树深度 0 至 3 分层，每个深度包含 150 个提示，共覆盖 35 类约束，其中 10 类是面向 JSON、Markdown、列表和带标签章节的结构级约束，25 类是内容级约束；每个提示都配有沿约束树组合而成的层次化检查器。该设置假定约束具有可程序化判定标准，目标是测量模型能否同时生成正确的外层结构，并在每个指定局部作用域内满足相应内容要求。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **IFEval**: IFEval使用 25 类验证器模板，以确定性代码检查模型对输出约束的遵循情况，是本文内容级约束的重要来源之一。但其约束被视为作用于整段回答的独立扁平列表，无法区分关键词或格式要求应当在哪个嵌套章节中成立。
- **ComplexBench**: ComplexBench研究同一提示中多个约束之间的合取、链式和选择等逻辑关系，本文也从中引入部分内容级约束。它扩展的是约束间的逻辑组合，而不是输出区域之间的父子层次，因此仍不能把检查限定到某个嵌套子结构。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

随着模型容量、上下文窗口和智能体框架的发展，过去由多个短提示及外围代码拆分完成的任务，越来越多地被合并为一次大语言模型调用。一个长提示会同时规定整体产物的格式、主要章节的结构以及内部字段的内容，而下游程序只有在这些约束都于正确层级得到满足时才能可靠使用输出。论文还引用经验研究指出，真实开发者提示中超过 80% 的要求可以客观验证，例如必需字段、格式、长度以及必需或禁用关键词，这说明分层约束遵循既是实际部署需求，也是可进行确定测量的问题。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **扁平独立约束基准（IFEval、IFBench）**：把提示中的要求视为彼此独立的检查项，并使用代码对整段模型回答逐项检查；这种设计适合判断全局格式、长度或关键词要求，却不表达某项检查只应作用于特定章节或字段。
- **带逻辑关系的扁平约束基准（ComplexBench）**：在约束之间加入合取、链式或选择等逻辑关系，并采用规则与大语言模型相结合的验证方式；它提高了约束组合的复杂度，但仍未把输出表示为具有父子作用域的结构。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有基准统一在整段回答上执行检查，不能把要求限定到某个嵌套区域。其直接后果是作用域错误会被误判：例如要求 Highlights 子节包含“YoY”时，只要全文任意位置出现该词，扁平检查器就可能判定成功，即使应承载 Highlights 的 Executive Summary 外层章节根本没有生成。
- IFEval 等扁平基准已接近饱和，论文称包括不足 10B 参数的领先模型也能取得 80% 以上成绩；然而该成绩只说明模型较善于满足全局清单，不能推断其能够维持外层结构、定位内层区域并在正确位置执行嵌套约束，因此可能高估真实复杂产物生成中的可靠性。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究分别覆盖独立约束和约束间逻辑组合，却缺少一种同时具备三项性质的评测：显式表示约束的父子层级、在每项约束所属的局部输出区域进行检查，并以确定性代码而非模型裁判验证所有层级。因此，当前模型面对不同嵌套深度时的真实能力、失败位置及随深度变化的退化程度仍未被可靠测量。

</div>
<div markdown="1"><span>核心问题</span>

当前大语言模型能否在单次调用中可靠理解并执行分层输出规范，使整体回答、主要章节和嵌套字段分别在其正确作用域内满足约束；当约束树深度从 $0$ 增至 $3$ 时，这种能力如何变化？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把复杂提示理解为一棵约束树：父节点定义输出容器或结构，子节点定义只在该容器内部生效的要求。检查器沿树逐层定位对应区域后再验证局部约束，便能区分“内容出现了”和“内容在正确位置出现了”，同时暴露由外层结构缺失引起的连锁失败；按树深度分组则可把嵌套本身带来的难度从一般任务难度中更清楚地分离出来。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

IFHierBench 的构建方法把一个已有任务提示转化为“任务不变、约束重新分层生成”的可验证样本。端到端流程以 IFEval 种子提示为输入：先删除原有输出约束并保留任务与上下文，再挖掘任务相关词汇、判断任务体裁允许哪些根格式；随后从 JSON、Markdown、带标签章节、列表和字符串五类宿主格式出发，按目标深度递归生成约束树，在各作用域采样内容约束并求解参数；最后依据同一棵树同时生成自然语言提示和逐节点确定性检查器。输出样本因此包含任务提示、显式分层约束以及与各作用域一一对应的自动评分程序。

技术上的关键是把约束附着在树节点而非整个回答上：每个节点代表回答中的一个可定位区域，例如 JSON 键对应的值、列表中的元素或 Markdown 标题下的章节；结构约束规定容器形状，内容约束规定该区域的关键词、大小写或长度。通俗地说，该方法先画出回答应有的“目录和字段树”，再给每个局部区域分别写规则，并生成一个沿树逐层拆解回答的检查程序，从而避免把“标题不超过 60 字符”错误地应用到整篇回答。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 任务设置准备

使用 GPT-5.4 将提示解析为去除输出约束后的任务描述和保持原文不变的上下文，同时挖掘与任务相关的词汇池；模型还识别任务体裁，并从预定义格式中筛选可作为根节点的格式集合。作者对任务抽取、关键词挖掘和体裁—格式映射各随机抽查 $10\%$ 的输出，并报告每一步人工评估准确率均超过 $90\%$。

<div class="method-step__io" markdown="1">

**输入**：一个 IFEval 种子提示，其中包含原始任务、上下文以及可能已有的输出约束。<br>
**输出**：可供采样的任务设置，包括干净任务、原始上下文、任务词汇池、任务体裁和允许的根格式集合。

</div>

**直观理解**：这一步先把“要完成什么”与“回答必须长什么样”分开，再准备后续约束所需的词语素材。体裁过滤用于避免生成明显不自然的组合，例如强迫普通邮件套入 JSON 或项目符号列表。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分层约束树构造

采样器以深度优先方式选择根格式并递归扩展子作用域；每个节点先确定字符串、JSON 对象、列表、Markdown 文档或带标签章节等形状，再添加结构约束和内容约束。子节点类型由父节点类型、加权采样规则及剩余深度共同决定，到达最大深度时强制使用原子字符串；同一作用域中的内容约束须通过冲突矩阵检查。

<div class="method-step__io" markdown="1">

**输入**：准备后的任务、允许的根格式、目标树深度以及结构级和内容级约束模板库。<br>
**输出**：带唯一作用域别名、结构约束、内容约束和待定参数的约束树骨架。

</div>

**直观理解**：约束树类似一份带规则的输出蓝图：根节点规定整个回答的外壳，子节点规定字段或章节，叶节点规定最终文本。冲突矩阵则像预先列出的禁配表，可阻止同一文本同时被要求全部大写和全部小写。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 参数回填与可满足性求解

词汇参数从任务词汇池中选择，并保证必需词与禁用词不相同、互不构成子串，且关键词或标识符不在整棵树中重复；数量参数则维护字符、词、句和段落计数的上下界。求解器把固定词语等词汇承诺转换为计数下界，再迭代传播单位比例约束直至不动点；若任一计数出现 $X_{\min}>X_{\max}$，则拒绝该次采样，否则按段落到字符的由粗到细顺序确定具体值。

<div class="method-step__io" markdown="1">

**输入**：带待定参数的约束树，以及任务词汇池。<br>
**输出**：参数完全确定且通过启发式一致性检查的最终约束树。

</div>

**直观理解**：这一步检查随机生成的规则是否至少在长度上彼此兼容。例如标题必须包含两个指定词时，字符下限不能仍为零；若必需内容已经超过字符上限，就丢弃该组合并重新采样。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 检查器与自然语言提示生成

系统为每个节点绑定手写的确定性检查逻辑，并生成从父作用域中提取当前区域的解析器；随后用模板将各原子约束渲染成句子、解析跨作用域别名，并以 $0.8$ 的概率用预定义合并模板压缩匹配的同级约束句。任务、合并后的约束说明和上下文最终组成一个提示。

<div class="method-step__io" markdown="1">

**输入**：最终约束树、原始干净任务和上下文。<br>
**输出**：一个自然语言基准提示，以及与其约束树逐节点对应的确定性自动检查器。

</div>

**直观理解**：同一棵树同时产生“给模型看的要求”和“给评测程序用的答案规则”，可减少提示与评分标准错位。检查时先定位局部区域再判断规则；若 JSON、列表或章节无法解析，相关节点及其子树直接失败，而不会把规则错误地检查在其他文本上。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 词汇承诺诱导的字符与词数下界

$$
\begin{aligned} C_{\min} &\leftarrow \max\!\left(C_{\min},\sum_{t\in T}|t|\right),\\ W_{\min} &\leftarrow \max\!\left(W_{\min},\sum_{t\in T}\mathrm{wc}(t)\right). \end{aligned}
$$

**符号说明**

- $C_{\min}$：当前作用域允许的最少字符数。
- $W_{\min}$：当前作用域允许的最少词数。
- $T$：词汇约束强制出现的字面片段多重集合，包括必需关键词以及固定前缀、后缀或附言。
- $t$：集合 $T$ 中的一个强制字面片段。
- $|t|$：片段 $t$ 的字符数。
- $\mathrm{wc}(t)$：片段 $t$ 的词数。

<div class="equation-explanation" markdown="1">

**直观理解**：必需出现的文字本身就占用字符和词，因此输出长度下限至少要容纳这些片段。该更新能识别“必须包含很多词，但总长度上限过小”等直接矛盾；它按片段长度求和，是一种保守且易计算的一致性规则。<br>
**原文位置**：第 4.2 节 Hierarchical Sampling，Parameter Backfill，Quantitative resolution

</div>

</div>

<div class="equation-block" markdown="1">

#### 跨计数单位的可读性比例带与可行性条件

$$
1\leq \frac{S}{P}\leq 8,\qquad 3\leq \frac{W}{S}\leq 40,\qquad 3\leq \frac{C}{W}\leq 8,\qquad X_{\min}\leq X_{\max}\ \text{for all }X\in\{C,W,S,P\}
$$

**符号说明**

- $C$：某作用域最终实现的字符数。
- $W$：某作用域最终实现的词数。
- $S$：某作用域最终实现的句子数。
- $P$：某作用域最终实现的段落数。
- $X$：字符、词、句或段落计数中的任意一种，即 $X\in\{C,W,S,P\}$。
- $X_{\min}$：计数 $X$ 的当前下界。
- $X_{\max}$：计数 $X$ 的当前上界。

<div class="equation-explanation" markdown="1">

**直观理解**：三个比例带限制每段的句子数、每句的词数和每词对应的字符数，并据此在不同计数单位之间传播上下界；例如词数上限会限制字符数上限。传播达到不动点后，只要某个下界超过上界，该组约束就被视为不可行并拒绝采样；这些区间来自可读性启发式，而不是语言生成可满足性的充分证明。<br>
**原文位置**：第 4.2 节 Hierarchical Sampling，Parameter Backfill，Quantitative resolution

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。IFHierBench 是基准构建与确定性评测方法，不训练语言模型，也没有需要通过梯度优化的损失函数；文中的参数“求解”是对约束取值进行离散采样、上下界传播和冲突拒绝。最终优化目标可理解为构造结构有效、参数一致且可自动核验的测试样本，但原文没有把它定义为数值目标函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 作用域感知的约束树采样器**

树中每个节点表示一个可独立解析的输出作用域，并携带该作用域的格式、结构约束和内容约束。容器节点可以递归产生子节点，子格式不必与父格式相同；深度预算控制嵌套层数，唯一别名支持自然语言提示中的跨层定位。

> 直观理解：该模块使“规则属于回答的哪一部分”成为明确的数据结构，而不再只是扁平约束列表。这样可以表达“整个回答是 JSON，其中某个字段是三项列表，而每项不超过 15 个词”一类真实的嵌套要求。

**2. 冲突检测与参数一致性解析器**

冲突矩阵记录内容约束之间的成对互斥关系，采样器每次加入约束前都查询该矩阵；参数解析器进一步处理词汇碰撞、子串冲突、标识符重复以及字符、词、句、段落计数上下界。比例带被反复传播到各计数区间，直至达到不动点或发现区间为空。

> 直观理解：随机拼接规则容易产生无法完成的题目，因此该模块承担题目质量控制。不过，成对冲突矩阵和长度比例主要排除已编码的明显矛盾，并不等价于对所有自然语言约束进行完整的逻辑可满足性证明。

**3. 逐节点提取与确定性检查器**

检查器镜像约束树：节点先通过 JSON 解析、列表索引或标题区域提取等操作取得自己的文本切片，再运行对应约束类型的手写布尔谓词；容器节点仅在自身测试和全部子节点测试均通过时通过。提取失败会使该节点及整棵子树失败，从而保证约束只在预定作用域上评估。

> 直观理解：它像按目录逐层打开答案：先确认外层格式，再进入指定字段或章节检查局部规则。与在完整回答上搜索关键词相比，这种方式能区分“标题含有 policy”和“正文某处含有 policy”。

**训练与推理**

构建阶段先对种子提示运行 GPT-5.4，获得干净任务、上下文、词汇池和允许格式；再为指定深度采样约束树，用冲突矩阵过滤不兼容约束，并通过词汇解析和数量区间传播确定全部参数。最终树被分别编译为自然语言提示和确定性检查器，因此该流程生成的是固定评测数据，而非在线训练数据。

评测时，待测语言模型只接收最终自然语言提示并生成一次回答。检查器从根节点开始解析回答：根格式解析成功后，将对应字段、列表项或章节切片传给子节点；每个节点运行布尔测试，容器仅在全部后代约束均通过时通过。解析失败会让当前节点及其子树失败，这使结构错误与局部内容错误均可被定位，并支持按节点、作用域或整条提示汇总遵循情况。

**复现信息**

复现所需的核心资源包括：五种宿主格式及其递归规则、结构级与内容级约束模板、内容约束冲突矩阵、任务词汇池生成步骤、计数比例带、自然语言渲染与合并模板，以及每类约束对应的手写确定性谓词和作用域提取器。根格式必须受任务体裁允许集合约束；达到最大深度时子节点必须落为字符串，以避免产生没有可检查内容的空容器；每个作用域还需分配唯一别名，以便提示文本和检查器稳定地指向同一位置。

提示生成时，每个原子约束先单独模板化，再对匹配预定义组合的同级约束以 $0.8$ 的概率合并。原文给出了 JSON 解析、键集合包含、列表长度、子串包含和词数上限等检查示例，但所给章节未完整列出全部 35 类约束的模板、冲突矩阵内容、递归类型的具体采样权重以及参数区间的初始分布；因此仅凭本节摘录无法逐项复现完全相同的数据集，仍需使用作者发布的模板和检查器实现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- IFHierBench：本文提出的层次化指令遵循基准，共600个提示，覆盖4种约束树深度$d\in\{0,1,2,3\}$与35种不同约束；每个提示配有确定性的Python检查器，用于在对应作用域验证各项约束。实验按深度分层报告结果，作用是检验模型能否生成整体结构、局部章节及嵌套字段均符合要求的输出。原文节选未明确报告训练集、验证集或测试集划分，实验将该基准作为评测集使用。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**提示级严格准确率（Prompt-Level Accuracy）**

设基准含$N$个提示，第$i$个提示的约束集合为$C_i$，检查器通过指示量为$\mathbf{1}[c]$。指标为$\mathrm{Acc}_{\mathrm{prompt}}=\frac{1}{N}\sum_{i=1}^{N}\prod_{c\in C_i}\mathbf{1}[c]$：只有同一响应中的全部约束都通过，该提示才计为正确。它衡量端到端交付物是否完整合规，对任一局部错误都很敏感。 （越高越好，因为部署中的下游组件通常要求整份输出同时满足全部结构与内容约束。）

</div>
<div class="metric-item" markdown="1">

**指令级严格准确率（Instruction-Level Accuracy）**

指标为$\mathrm{Acc}_{\mathrm{inst}}=\frac{\sum_{i=1}^{N}\sum_{c\in C_i}\mathbf{1}[c]}{\sum_{i=1}^{N}|C_i|}$，即在所有提示的全部单项约束上计算平均通过率。它能区分“许多叶子约束分别能完成，但无法在一次响应中全部完成”与“整个约束子树均未正确构造”两类失败。 （越高越好，因为更高数值表示单项约束被正确执行的比例更大；但它不能替代提示级准确率，因为部分约束通过并不意味着最终输出可直接使用。）

</div>
<div class="metric-item" markdown="1">

**按约束类型汇总的通过率（Pooled Pass Rate）**

将七个模型在同一约束类型上的检查结果汇总，以识别最难满足的约束。表3重点比较精确字符数、精确词数、第$N$段首词、值域限制和精确句数五类约束，回答困难究竟集中在哪些操作上。 （越高越好，因为表示该类型约束更常被检查器判定为满足；这里主要利用低通过率定位共同失败点，而非形成单一总体排名。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### IFHierBench总体严格准确率及模型排名

<div class="result-value" markdown="1">

GPT-5.5取得53.7%的总体提示级准确率，Claude Opus 4.6为42.8%，Gemini-3-Flash为33.2%；其余四个模型均不超过19.8%。两种开启高thinking effort的模型在所有深度和两项指标上均领先。

</div>

作者据此认为，即使最强模型也只能让略多于一半的完整响应通过全部检查，层次化指令遵循仍存在明显缺口。该结果证明的是在IFHierBench确定性检查规则下的相对与绝对表现，并不能单独证明优势来自模型规模、训练数据或高thinking effort，因为这些因素没有通过受控实验分离。

<div class="result-source" markdown="1">

来源：第5.2.1节，表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GPT-5.5 and Claude Opus 4.6, both run with thinking effort set to high, top the table on every cell: 53.7% and 42.8% prompt-level overall, far ahead of Gemini-3-Flash at 33.2% and a tightly bunched cluster of Gemma-4-26B (19.8%), DeepSeek-R1 (15.5%), Qwen-3.6-35B (14.8%), and Kimi-K2.5 (14.7%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 提示级准确率随约束树深度$d$变化

<div class="result-value" markdown="1">

从$d=0$增加到$d=1$时，每个模型都下降37至53个百分点；GPT-5.5由86.7%降至49.3%，Claude Opus 4.6由78.7%降至42.0%。在$d=3$时，两者仍分别达到35.3%和22.7%，其他模型均为6.0%或以下。

</div>

最明显的性能断崖出现在第一次引入嵌套时，说明模型处理平面约束与处理带作用域的嵌套约束并非同一难度。作者进一步推测训练数据偏向平面结构，但实验没有直接检查训练语料，因此这是解释而非已验证因果结论。深度增长通常也会伴随更复杂的协调负担，故结果不能仅归因于树的形式深度。

<div class="result-source" markdown="1">

来源：第5.2.1节，表2及“Prompt-level accuracy decays steeply with depth”段落

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Every model loses between 37 and 53 absolute points from d=0 to d=1, including the strongest two (GPT-5.5 from 86.7% to 49.3%, Claude Opus 4.6 from 78.7% to 42.0%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 按约束类型汇总的失败分析

<div class="result-value" markdown="1">

七模型合并后最难的五类约束依次为精确字符数$string_length$（53.5%）、精确词数$num_words$（67.3%）、第$N$段首词$nth_paragraph_first_word$（73.2%）、允许值集合$value_in_set$（75.6%）和精确句数$num_sentences$（81.4%）。其中四类涉及计数或位置索引。

</div>

困难主要集中在要求模型精确计数和定位的位置约束，而不是所有语义或格式要求都同样困难。作者提出$string_length$缺少类似IFEval检查器所带来的训练信号，可能因此最难；但本文没有操纵训练数据或训练目标验证这一机制，汇总通过率也会受到各类型样本数量与分布影响。

<div class="result-source" markdown="1">

来源：第5.2.2节，表3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The five hardest types are string_length, which fixes the response to an exact character count (53.5%), num_words, which fixes the response to an exact word count (67.3%), nth_paragraph_first_word, which fixes the first word of the N-th paragraph (73.2%), value_in_set, which restricts a value to a fixed allowed set (75.6%), and num_sentences, which fixes the response to an exact sentence count (81.4%).

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

- GPT-5.5与Claude Opus 4.6：两种领先的闭源API模型，均将thinking effort设为high；它们构成强推理条件下的性能上界比较，也用于分析深度为$d=3$时的规划轨迹。
- Gemini-3-Flash：闭源API模型，在总体性能上处于两种最强模型与其余模型之间；其指令级准确率低于提示级准确率，因而是识别“外层结构整体失效”这一错误模式的重要对照。
- DeepSeek-R1与Kimi-K2.5：通过托管API调用的模型。它们用于检验具有不同训练与推理特征的现有模型是否同样受到层次深度影响；两者均表现出单项约束偶尔通过、整份响应难以全部通过的现象。
- Qwen3.6-35B-Instruct与Gemma-4-26B-it：在单张NVIDIA RTX 4090上通过Ollama v0.21.0本地运行的开放权重模型，使用默认4-bit量化。该组提供可本地部署模型与闭源API模型之间的比较；但模型规模、量化方式和推理设置并未受控，因此不能将差异单独归因于是否开放权重。

**实验想回答的问题**

- 当前代表性的闭源与开放权重模型能否同时满足同一提示中位于不同作用域的多条约束，以及这种严格遵循能力会如何随约束树深度$d$增加而变化？
- 模型失败主要来自无法构造外层结构、无法同时满足多个局部约束，还是特定约束类型本身较难；在深层提示上表现较好的模型又采用何种层次化规划方式？

**实验实现**

实验评测7个模型。GPT-5.5、Claude Opus 4.6、Gemini-3-Flash、DeepSeek-R1和Kimi-K2.5通过托管API调用；Qwen3.6-35B-Instruct与Gemma-4-26B-it在单张24 GB NVIDIA RTX 4090上借助Ollama v0.21.0运行，并采用其默认4-bit量化。GPT-5.5与Claude Opus 4.6的thinking effort设为high，且因接口不允许调整温度而保留服务商默认温度；其余模型以温度0解码，以提高输出确定性。每个响应由对应Python检查器逐项判定，并报告总体及$d=0$至$d=3$的提示级、指令级严格准确率。失败分析还汇总各约束类型的通过率，并对两个强模型在150个$d=3$提示上的推理轨迹进行遍历顺序分析；Claude轨迹开头对提示约束的逐字编号复述会先被剔除，再按约束特征短语的首次出现位置判断更接近深度优先还是广度优先。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 在150个$d=3$提示的推理轨迹中，研究者用每项约束的特征短语首次出现位置恢复规划次序；Claude Opus 4.6有67%的提示更符合深度优先遍历、33%更符合广度优先遍历，GPT-5.5则分别为62%和38%。Claude通常先逐字编号复述全部约束，因此分析前剔除了这段复述；GPT-5.5无需该预处理。这个案例说明两个强模型倾向先沿一个分支深入处理嵌套要求，但短语匹配只是规划顺序的代理指标，不能保证完整还原模型内部推理。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Presents a benchmark with deterministic scoped checkers for evaluating hierarchical instruction following in LLMs.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`e14f2dd557bf9eff1b6cf6097f9014e7b99c8175fbcd0da9fe96f27082eae336`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
