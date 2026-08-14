---
title: "[论文解读] Unified Multi-Dimensional Benchmark for Complex Graph Reasoning in Large Language Models"
description: "[arXiv 2608.12391][LLM 评测] 本文提出半自动基准构建框架 GraphGym，通过系统扩展图规模、任务复杂度、任务描述、图加载方式和任务来源，并统一文本推理与代码推理评测，以更全面地暴露大语言模型在复杂图推理中的能力边界。"
arxiv_id: "2608.12391"
announcement_date: "2026-08-14"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T02:53:59.517427+00:00"
source_sha256: "0a6953aa34a11c610360257309f0fb0a91f9ae9c27aa383c74c9282b6d44fd70"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "图推理"
  - "复杂性维度"
  - "长上下文评测"
  - "文本式推理"
  - "代码式推理"
  - "半自动基准构建"
  - "数据污染"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.12391</p>

# Unified Multi-Dimensional Benchmark for Complex Graph Reasoning in Large Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Fali Wang, Ali Al-Lawati, Iliyas Bektas, Jinxuan Fang, Alek Melenski, Tianxiang Zhao, Yao Ma, Suhang Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> The Pennsylvania State University, University Park, PA, USA；Rensselaer Polytechnic Institute, Troy, NY, US</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12391v1) · [PDF 下载](https://arxiv.org/pdf/2608.12391v1) · **关键词** 大语言模型, 图推理, 复杂性维度, 长上下文评测, 文本式推理, 代码式推理, 半自动基准构建, 数据污染<br>


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

本文提出半自动基准构建框架 GraphGym，通过系统扩展图规模、任务复杂度、任务描述、图加载方式和任务来源，并统一文本推理与代码推理评测，以更全面地暴露大语言模型在复杂图推理中的能力边界。

**不用术语来说**：现有测试往往只让模型处理规模较小、表述直接、类型固定的图问题，而且通常只测试模型直接回答或编写代码中的一种方式。这类测试可能使模型依靠见过的题目、成熟图算法库或固定模板取得高分，却无法说明它能否理解陌生的现实情境、处理超长图数据、组合多个推理步骤，或在不同解题方式之间保持稳定表现。因此，需要一种能够持续生成新任务、控制难度并公平比较多种推理方式的统一测试体系。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出五阶段、基于大语言模型的半自动基准构建框架：自动生成任务定义、图实例、图加载脚本、参考解答、问题形式和评测脚本，同时在关键环节保留人工验证，以降低扩展和更新图推理基准的人工成本。
- 作者据此构建包含 $202$ 个任务的 GraphGym，从 Graph Size、Task Complexity、Task Description、Graph Loading 和 Task Source 五个维度控制复杂性，并为文本推理、代码推理及增强方法提供统一的自动化评测条件。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大语言模型的图推理评测把图结构及其问题转换为自然语言输入或编程任务，用来检验模型能否理解节点与边之间的关系，并完成连通性、遍历、最短路径、流等结构化多步推理。图实例可由程序随机生成，因而比固定的数学或代码题更容易控制难度、持续更新并降低训练数据污染风险；同时，增大节点数会自然拉长输入，例如原文指出稀疏图中约 $10$、$100$、$1{,}000$ 和 $10{,}000$ 个节点分别对应约 $200$、$1{,}000$、$9{,}000$ 和 $117{,}000$ 个 token，因此该领域也适合评测长上下文推理。本文关注的不是提出一种新的图算法，而是构建统一、可扩展的诊断性基准，以同时衡量模型在文本推理与代码推理中的能力边界。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**图推理**

图由节点及表示节点关系的边构成；图推理要求模型依据这些结构完成连通性判断、路径计算或多个图操作的组合。它既考查对输入结构的解析，也考查按算法步骤进行推断的能力。

</div>
<div class="concept-item" markdown="1">

**文本式与代码式推理**

文本式推理要求模型直接阅读文本化的图并给出答案，主要检验模型内部的结构理解与推演能力；代码式推理则要求模型生成并执行程序，还会检验问题建模、程序合成以及调用外部图工具的能力。两种模式的求解机制和错误来源不同，不能用其中一种完全代表另一种。

</div>
<div class="concept-item" markdown="1">

**数据污染**

数据污染是指公开测试题进入模型的训练或开发流程，使高分可能来自记忆而非真实推理。程序化生成新图实例与标签可以减少测试实例同训练材料重合，并支持持续刷新评测内容。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文要解决的是复杂图推理基准的构建与统一评测问题。一个任务以图问题定义为核心，可来自经典图算法或在线编程测评风格的问题；框架据此生成任务描述、图实例、图加载脚本、参考解、问题形式和自动评测脚本，并在人为质量检查后形成可执行样例。模型输入包含任务描述与图数据：描述可以显式使用图论术语，也可以把图关系隐藏在现实场景中；图数据可以直接写入提示，也可以存放在本地文件中供代码加载。模型输出则随设置变化：文本模式直接产生答案，代码模式生成可执行程序，再由对应评测器判断正确性。

基准将难度组织为五个维度：图规模、任务复杂度、任务描述、图加载方式和任务来源。图规模最高达到 $10{,}000$ 个节点；任务复杂度通过组合多个种子任务形成复合任务；每个任务具有两种描述、三种“推理方式与加载方式”场景以及四种图规模，理论上最多形成 $24$ 个实例。该设置隐含的基本假设是：参考程序能够为生成图实例提供可信标签，自动评测器能够判定模型输出，而关键阶段的人类验证用于控制由大语言模型自动生成任务材料时产生的质量风险。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$G=(V,E)$**

用于概括本文图推理输入的通用记号；$G$ 表示图，$V$ 表示节点集合，$E$ 表示边集合。该记号是为解释问题设置所作的标准化概括，原文节选未显式给出这一公式。

</div>
<div class="notation-item" markdown="1">

**$|V|$**

图中的节点数量，对应本文“Graph Size”维度；基准覆盖的最大规模为 $10{,}000$ 个节点。

</div>
<div class="notation-item" markdown="1">

**$k$**

复合任务包含的种子任务数量，即原文所称 combo size；它用于刻画“Task Complexity”，但原文节选未为其指定正式符号。

</div>
<div class="notation-item" markdown="1">

**$T$**

一个图推理任务，可包含任务定义、描述、图实例、参考解、加载脚本、问题形式和评测脚本；该符号是便于说明而引入的概括，原文节选未显式定义。

</div>

</div>

**直接相关的工作**

- **GraphInstruct**: 经典图任务方向的代表性基准与指令微调工作之一，使用 Erdős–Rényi 等生成器采样随机图，体现了图数据可程序化生成的优势。本文以其为既有文本式图推理研究的例子，同时指出图任务上的指令微调通常存在跨任务迁移能力有限的问题。
- **GraphEval36K**: 代码式图推理基准的代表，从 LeetCode 等在线测评来源选择图问题，并配套参考解和评测脚本。它代表以编程题为中心的单一推理模式，而本文试图在同一基准内统一比较文本式与代码式推理，并进一步扩展图规模、复合任务、隐式描述和文件加载等复杂性维度。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型的强推理表现需要通过不易被训练数据污染、能够按需刷新且足以测试长上下文的任务来验证。传统数学、代码和逻辑基准通常题目固定且输入较短，一旦进入训练语料，高分可能来自记忆而非真实推理；重新人工编题成本又很高。图任务可以程序化生成结构与答案，并通过增加节点数自然拉长输入，因此适合作为可控的结构化多步推理测试，但前提是基准本身能覆盖真实而多样的难度来源。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **经典图问题型文本推理基准**：以连通性、遍历、最短路或流等预定义任务为核心，程序生成图实例及答案，再使用模板把任务描述和图数据直接放入提示中，让模型输出自然语言形式的答案。NLGraph、GraphQA、GraphInstruct 和 GrAlgoBench 属于这一思路的代表。
- **在线测评题型代码推理基准**：从 LeetCode 等在线测评平台收集图相关编程题，为题目配套参考程序和评测脚本，要求模型理解题意并生成可执行代码，再通过测试用例判断正确性；GraphEval36K 是文中给出的代表。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 复杂性覆盖不足：既有基准很少包含 $1\mathrm{K}$ 或 $10\mathrm{K}$ 节点的长上下文实例，通常聚焦单一任务、显式图论表述和提示内直接加载数据，也大多局限于经典图问题。其后果是无法系统测试任务组合、隐式现实场景、文件加载和超长输入；在代码模式下，模型还可能直接调用 NetworkX 等成熟库，使经典任务接近饱和，掩盖真正的建模与推理困难。
- 构建与评测机制割裂：现有流程通常需要人工设计任务、编写图生成程序、实现参考解和制作评测脚本，难以低成本持续扩展；同时，多数基准只覆盖文本推理或代码推理之一，无法在同一任务体系下区分模型内部推理能力与题意理解、计算建模、代码生成及工具使用能力。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作尚未提供一种可扩展的统一机制，在有限人工审核下自动构造并持续更新复杂图任务，同时沿多个可控维度制造难度，并让同一基准兼容文本回答、代码求解和增强方法评测。缺少这一机制意味着研究者既难以判断模型性能下降究竟来自图规模、组合复杂度、描述隐含性、数据加载还是任务来源，也难以公平比较不同推理模式及改进方法。

</div>
<div markdown="1"><span>核心问题</span>

论文集中回答两个相互衔接的问题：GraphGym 所定义的五个数据复杂性维度分别如何影响大语言模型的图推理表现；面对这些复杂任务，指令微调和检索增强等方法能否在文本推理与代码推理场景中稳定提升性能并泛化到新任务？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把基准构建看作一条可生成、可审核的生产流程，并把笼统的“题目更难”拆成五个可独立调节的因素。大语言模型负责批量生成彼此配套的题目、数据、参考解和评测程序，人工只检查关键质量节点，因而能够降低扩展成本；同一任务再被转换为不同描述、规模和加载形式，并分别要求直接作答或编写代码，就像给模型做受控变量实验，可以更清楚地定位失败来自长上下文、任务组合、问题识别还是工具化求解。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

GraphGym同时指一个半自动基准构建框架及其产出的图推理数据集。框架以人工整理的原子图任务、预定义组合模式和目标图规模为起点，使用DeepSeek-V3作为数据生成器，依次完成任务组合与图生成、参考求解与标签生成、任务描述和问题生成、评测脚本生成、质量过滤，最终形成可同时支持文本推理与代码推理的统一评测单元。每个单元不仅包含问题和图实例，还配套参考解、图加载脚本及任务专用评测脚本，因此能够从数据构造一直覆盖到自动评分。

其核心设计是把图推理难度拆成五个可控制维度：Graph Size控制节点数和输入长度；Task Complexity用组合任务所含原子任务数衡量；Task Description控制问题是否明确使用图术语；Graph Loading区分图数据直接写入提示与从本地文件读取；Task Source区分经典图算法与在线编程评测风格任务。通俗地说，该框架类似一条带人工质检的自动出题流水线：模型负责组合题型、造图、写标准答案和判题器，人工只在关键节点检查生成物是否正确、可执行且相互一致。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 预备阶段：定义种子任务与组合模式

构建包含$40$个经典图任务和$60$个在线评测风格任务的种子任务池，并预定义sequential、constrained、hierarchical、counterfactual、map-reduce、aggregate和logical-comparative共$7$种组合模式。经典任务保证与既有基准可比较，在线评测任务则减少代码推理仅调用成熟图算法库即可解题的问题。

<div class="method-step__io" markdown="1">

**输入**：已有图推理基准覆盖的经典任务、LeetCode中的开放式图问题，以及人工规定的任务组合规则。<br>
**输出**：共$100$个可作为原子单元的种子任务，以及$7$种用于生成复合任务的结构模板。

</div>

**直观理解**：种子任务相当于基本积木，组合模式规定积木如何连接；两者共同决定后续能生成哪些单任务或多步骤复合题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段1：任务组合与图实例生成

LLM数据生成器选择合适的组合模式，产生新的任务定义和与该任务适配的图生成代码；执行代码后，分别生成节点数为$10$、$100$、$1{,}000$和$10{,}000$的图实例。$k=1$被视为复合任务的退化情形，框架本身可以扩展到更大的$k$。

<div class="method-step__io" markdown="1">

**输入**：指定的组合规模$k\in\{1,2,3,4\}$、从任务池抽取的$k$个种子任务、$7$种候选组合模式，以及目标节点规模。<br>
**输出**：具有明确语义的单一或复合图任务、可执行的图生成程序，以及四种规模的对应图实例。

</div>

**直观理解**：模型先决定几道基础题应怎样串成一道新题，再编写造图程序；改变$k$是在增加推理链条，改变节点数则是在增加需要读取和处理的数据量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段2：参考求解器生成与标签标注

LLM数据生成器为新任务生成参考求解代码，并通过执行求解器为图实例计算参考答案。该阶段把自然语言任务落实为可执行的解题过程，使后续评测拥有程序化标签来源。

<div class="method-step__io" markdown="1">

**输入**：阶段1产生的任务定义、图实例及其数据格式。<br>
**输出**：任务对应的参考求解程序，以及各图实例的参考答案或标签。

</div>

**直观理解**：这一步相当于先编写标准解法，再用它批量算出标准答案；参考标签不是仅凭语言模型直接猜测得到，而是由生成的程序执行产生。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段3至4：描述、问题、图加载与评测接口生成

框架生成任务描述、具体问题形式和图加载脚本，并为任务生成专用评测脚本；图既可直接序列化到提示中，也可由模型生成的代码从本地文件加载。由此，同一任务能够被包装为直接输出答案的文本推理问题，或生成并执行程序的代码推理问题。

<div class="method-step__io" markdown="1">

**输入**：经过求解的任务定义、图实例、参考答案，以及文本推理和代码推理两种目标评测方式。<br>
**输出**：文本式与代码式问题提示、内联或文件式图加载组件，以及可自动判断模型输出的任务专用评测脚本。

</div>

**直观理解**：同一道图题可以变成“读完图后直接回答”，也可以变成“写程序读取图并计算”；配套判题器使这两类回答能够在统一框架内评分。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。GraphGym是一套基准构建与评测框架，而不是通过损失函数训练参数化模型的方法；文中使用LLM作为数据生成器，并未在所给方法章节中提出新的训练目标或优化方程。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 多源种子任务与组合任务模块**

该模块把$40$个经典图任务与$60$个在线评测风格任务统一为原子任务，并使用$7$种组合模式构造包含$1$至$4$个种子任务的新任务。组合规模直接控制模型需要解决、保存并合并多少个子问题的结果。

> 直观理解：只扩大图的节点数主要增加阅读和计算负担，而组合多个任务会改变推理结构；该模块因此能够分别测试“输入很长”和“步骤很复杂”两类困难。

**2. LLM数据生成器**

框架使用DeepSeek-V3生成任务定义、任务自适应图生成代码、参考求解代码、任务描述、问题形式、图加载脚本和评测脚本。生成器贯穿五阶段，但关键产物仍需人工验证，因此该方法被定义为半自动而非全自动。

> 直观理解：同一个生成模型承担出题、造数据、写标准解和写判题器等工作，可显著减少逐题手工制作成本；人工检查用于限制模型生成错误在流水线中继续传播。

**3. 双推理模式与双图加载模块**

框架同时构造文本推理和代码推理接口：前者把图结构序列化为文本并要求模型直接推断答案，后者要求模型生成可执行代码。Graph Loading进一步支持将图直接放入提示或通过本地文件加载，从而覆盖提示内数据处理与外部数据读取两种条件。

> 直观理解：该模块避免把“会读文字化的图”和“会编程求解图问题”混为一种能力，也能检验模型在图数据不直接出现在提示中时是否仍能正确加载和处理输入。

**训练与推理**

构建阶段先由人工确定种子任务和组合模式，再向DeepSeek-V3提供种子任务定义、候选组合模式及规定输出格式。生成器根据组合规模创建任务和图生成代码，执行该代码得到不同节点规模的实例；随后生成并执行参考求解器以获得标签，再生成任务描述、问题、图加载脚本和任务专用评测脚本，最后通过有限人工验证过滤低质量样本。

评测时，文本推理模式把任务描述与序列化图数据放入提示，模型直接生成答案，再与参考标签进行任务相关的自动比较；代码推理模式让模型生成程序，程序读取内联图或本地图文件并输出结果，再由评测脚本判定。该流程还可承载微调模型或检索增强方法，但这些属于受测增强设置，不是GraphGym自身的训练过程。

**复现信息**

复现框架时最关键的配置包括：数据生成器采用DeepSeek-V3；种子任务由$40$个经典任务和$60$个LeetCode风格开放任务组成；组合规模取$k\in\{1,2,3,4\}$；候选组合模式共$7$种；每个任务生成$10$、$100$、$1{,}000$和$10{,}000$节点规模的实例；最终基准包含$202$个任务。还需保留任务自适应图生成代码、参考求解器、两类图加载方式及任务专用评测脚本，否则无法复现其多维控制和端到端自动评分能力。原文所给节选未明确报告生成温度、采样次数、失败重试策略、人工标注人数与一致性标准，也未完整列出质量过滤规则；这些信息需要结合附录D及待发布代码进一步核验。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GraphGym：作者通过半自动五阶段框架构建的图推理基准，共含 $202$ 个任务；其设计角色是统一评测文本推理、代码推理及增强推理。摘录说明任务可采用显式或隐式描述、内联或文件图加载、经典或在线测评风格来源，并支持最高 $10{,}000$ 个节点，但未提供实验划分、每类样本数或模型评测实例总数。
- 内联图序列化分析数据：针对 tree、sparse、medium、BA、RGG、ER、dense 和 complete 八类图分布，根据节点数与期望边数生成边记录，并用 `cl100k_base` 实际分词，估计完整提示的 token 数。该数据用于测试不同图密度下的上下文可扩展性，不是模型推理准确率数据集。
- 代表性基准元数据集合：作者汇总 NLGraph、GPT4Graph、GraphQA、LLM4DyG、GraphInstruct、GraphEval36K、GraphArena、ProGraph、GraphPattern、GraphOmni、GraphAlgorithm、GrAlgoBench 等基准，并按五维规则比较覆盖范围。它用于定位 GraphGym 的设计覆盖缺口，而不是在统一样本上直接比较模型性能。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**提示 token 长度 $T_{\mathrm{prompt}}$**

使用 `cl100k_base` 对完整提示实际分词后的 token 数，由固定模板、节点列表和边列表三部分相加得到。它衡量图序列化带来的上下文成本，并可与 $8$k、$32$k、$128$k 和 $1$M 等上下文窗口比较。 （在表达同一任务与图实例时越低越好，因为较短提示更不容易被上下文窗口截断；但该指标不衡量答案正确率，也不能单独说明模型推理能力。）

</div>
<div class="metric-item" markdown="1">

**五维基准覆盖得分**

分别评估 Graph Size、Task Complexity、Task Description、Graph Loading 和 Task Source，每维归一化到 $[0,100]$。其中图规模按最大节点数 $n_{\max}$ 的十进制对数计分，其余维度依据是否覆盖复合任务、隐式描述、文件加载及混合任务来源分档。 （越高表示基准覆盖的复杂设置越多；它是作者提出的设计覆盖度量，并非模型性能指标，高分不自动意味着样本质量更高或任务更难被模型解决。）

</div>
<div class="metric-item" markdown="1">

**最大节点规模 $n_{\max}$**

基准明确支持的最大图节点数，也是 NodeScaleScore 的输入。作者将其上限截断为 $10{,}000$，使 $10$、$100$、$1{,}000$ 和 $10{,}000$ 个节点分别对应 $25$、$50$、$75$ 和 $100$ 分。 （作为压力测试覆盖指标通常越高越好，因为更大图更能检验长上下文或文件加载能力；但节点数没有同时反映边密度，完整图的 token 成本可能远高于同节点数的树。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 五维基准覆盖比较

<div class="result-value" markdown="1">

作者报告 GraphGym 的最大图规模达到 $n_{\max}=10{,}000$，并在五个维度上均取得 $100$ 分；该结果支持其覆盖范围比所列既有基准更全面的主张。

</div>

这意味着 GraphGym 的设计同时纳入大图、复合任务、显式与隐式描述、内联与文件加载以及混合任务来源。它证明的是作者评分规则下的功能覆盖，不证明 GraphGym 的每个样本都更困难，也不证明模型在该基准上的性能更低。

<div class="result-source" markdown="1">

来源：Appendix B, Comparative results；Figure 9

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Second, no prior benchmark simultaneously attains high scores on all dimensions, leaving a gap that our benchmark is designed to close: it offers composite tasks, both explicit and implicit descriptions, both inline and file-based graph loading, mixed task sources, and graph sizes up to $n_{\max}=10{,}000$, achieving the maximum score on every axis.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 稀疏图与中等稠密图的内联提示扩展

<div class="result-value" markdown="1">

在 $N=1{,}000$ 时，tree、sparse、medium 和 BA($m=3$) 的估计提示长度分别为 $9{,}129$、$9{,}135$、$15{,}135$ 和 $21{,}081$ tokens，均低于 $32$k；但 ER($p=0.05$) 已达到 $152{,}978$ tokens，超过 $128$k。

</div>

同样的节点数并不对应相同的上下文压力，边数随 $N$ 线性增长的图仍可内联，而边数近似二次增长的 ER 图会迅速超出常见窗口。因此，评测大图时必须同时控制图分布或边密度。该结果只估计输入能否装入上下文，并未测试模型即使读入完整图后能否正确推理。

<div class="result-source" markdown="1">

来源：Appendix A.4, Table 2；列顺序为 tree、sparse、medium、BA($m=3$)、ER($0.05$)、ER($0.20$)、dense、complete

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

1000 | 9,129 | 9,135 | 15,135 | 21,081 | 152,978 | 602,503 | 752,344 | 2,999,969

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 稠密图和完全图的内联提示成本

<div class="result-value" markdown="1">

在 $N=1{,}000$ 时，dense 图约需 $752{,}344$ tokens，complete 图约需 $2{,}999{,}969$ tokens；即使是 $1$M 上下文也无法完整容纳后者。

</div>

该结果说明仅提高模型上下文上限不足以覆盖所有大图：完全图的边数为 $O(N^2)$，序列化成本会快速膨胀，因而文件加载和代码访问机制具有实际必要性。不过，表中边记录由简化的随机生成与字符串格式构成，具体 token 数会随 tokenizer、编号形式和序列化格式变化。

<div class="result-source" markdown="1">

来源：Appendix A.4, Table 2；列顺序为 tree、sparse、medium、BA($m=3$)、ER($0.05$)、ER($0.20$)、dense、complete

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

1000 | 9,129 | 9,135 | 15,135 | 21,081 | 152,978 | 602,503 | 752,344 | 2,999,969

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

- NLGraph：典型文本图推理评测基准，含 $8$ 个经典任务，图规模不超过 $35$ 个节点，仅采用显式描述和提示内图加载；它代表已有小规模、以内联输入为主的文本评测设置。
- GraphArena：同时覆盖多项 P 类和 NP 类图问题，因而是检验 GraphGym 是否真正扩展任务难度而非仅增加任务数量的有意义参照；但其图规模为 $4$ 至 $50$，且只支持显式描述和提示内加载。
- GraphEval36K：由 $40$ 个 LeetCode 图问题构成的代码推理评测，支持文件加载、显式与隐式描述，图规模为 $20$ 至 $200$；它是比较 GraphGym 跨描述形式和代码执行场景覆盖能力的重要基线。
- GraphAlgorithm：包含来自 Codeforces、AtCoder、CodeChef 和 Kattis 的 $239$ 个图问题，代表在线测评风格的代码推理基准；它具有较宽的任务来源，但图通常只有约 $10$ 个节点且采用提示内加载，可用于区分“任务数量多”和“输入规模及加载方式丰富”两种能力。

**实验想回答的问题**

- 内联图序列化的提示长度如何随节点数 $N$、边数 $M$ 和图分布 $\mathcal{D}$ 增长，以及常见上下文窗口能够容纳多大规模的图？
- 与已有图推理基准相比，GraphGym 是否同时覆盖图规模、任务复杂度、任务描述、图加载方式和任务来源五个复杂度维度？当前摘录未包含模型性能实验章节，因此无法核验摘要所称的文本推理、代码推理、微调模型和检索增强方法的具体效果。

**实验实现**

提示长度实验统一使用显式任务描述模板，将提示分解为固定文本、节点列表和边列表；默认采用 GPT-4/GPT-4o 系列对应的 `cl100k_base` tokenizer，并设 $T_{\mathrm{fixed}}=135$。边记录的端点从 $\{0,\ldots,N-1\}^{2}$ 中均匀抽取；加权图的权重独立取自 $\{1,\ldots,10\}$。各分布先以期望边数 $M_{\mathcal{D}}(N)$ 确定规模，再计算序列化 token 数。基准比较则使用作者定义的五维 $[0,100]$ 评分规则，并依据各基准公开的任务数量、图规模、描述形式、加载方式、复杂度和任务来源制作雷达图。当前摘录未给出被测 LLM、解码参数、重复次数、准确率判定流程、训练/测试划分或显著性检验，因而不能完整复现实质性的模型性能实验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 可将 $N=1{,}000$ 的 tree 与 complete 图视为一个诊断案例：两者节点数相同，但提示长度分别为 $9{,}129$ 和 $2{,}999{,}969$ tokens，相差约 $329$ 倍。该案例直观说明，按节点数分桶会掩盖真正的输入成本，文件加载设置主要隔离的是图序列化瓶颈，而不只是扩大名义节点规模。证据见 Appendix A.4 的 Table 2。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The central contribution is a multidimensional benchmark and evaluation framework targeting LLM graph-reasoning capabilities.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`0a6953aa34a11c610360257309f0fb0a91f9ae9c27aa383c74c9282b6d44fd70`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
