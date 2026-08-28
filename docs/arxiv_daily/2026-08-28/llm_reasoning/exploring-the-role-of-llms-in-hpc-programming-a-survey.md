---
title: "[论文解读] Exploring the Role of LLMs in HPC Programming: A Survey"
description: "[arXiv 2608.26110][LLM Reasoning] 本文系统梳理大语言模型在高性能计算编程中的应用，重点判断其在代码生成、并行化与优化等任务上何时有效、为何失效，以及距离可靠的生产级协作工具还缺少哪些关键条件。"
arxiv_id: "2608.26110"
announcement_date: "2026-08-28"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:45:54.595615+00:00"
source_sha256: "e58a76032011f245260229b46128052c4c43a0dc327199883b151a74f9ccf4a6"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "高性能计算"
  - "大型语言模型"
  - "并行编程"
  - "代码大模型"
  - "MPI"
  - "OpenMP"
  - "CUDA"
  - "领域专用 LLM"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.26110</p>

# Exploring the Role of LLMs in HPC Programming: A Survey

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Strahinja Ljaljevic, Josep Jorba, Sergio Iserte</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> bBarcelona Supercomputing Center (BSC), Barcelona, Spain</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26110v1) · [PDF 下载](https://arxiv.org/pdf/2608.26110v1) · **关键词** 高性能计算, 大型语言模型, 并行编程, 代码大模型, MPI, OpenMP, CUDA, 领域专用 LLM<br>


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

本文系统梳理大语言模型在高性能计算编程中的应用，重点判断其在代码生成、并行化与优化等任务上何时有效、为何失效，以及距离可靠的生产级协作工具还缺少哪些关键条件。

**不用术语来说**：高性能计算程序需要把计算任务正确而高效地分配到多核处理器、多个计算节点及加速器上，开发者不仅要写出能运行的代码，还要同时保证结果正确、执行速度快，并能随硬件规模扩大而保持效率。大语言模型能够帮助生成和修改代码，但一段看似合理的回答可能包含并行错误，或只在小例子上有效，因此需要系统评估它究竟能承担哪些工作、现有证据是否充分。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 将现有大语言模型辅助高性能计算的研究组织为代码生成、并行化与优化、框架与体系结构、评测与基准，以及挑战与整体格局五类，从而建立可比较的研究版图。
- 综合分析通用模型与高性能计算领域专用模型的能力边界，并据此归纳训练数据、模型设计、可用性和评测方面的缺口，提出加强领域数据、性能工具与调度器集成、严格评测及可信治理等研究方向。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

高性能计算（HPC）通过多核处理器、计算集群及 GPU 等异构硬件并行执行大规模科学计算，但开发者必须同时处理任务划分、线程或进程协作、数据移动、硬件差异以及性能扩展等问题。本文关注大型语言模型（LLM）能否作为 HPC 编程助手：它们从自然语言、程序代码和相关文档中学习上下文，可辅助生成、解释、调试、优化和迁移并行程序。论文将相关研究归入代码生成、并行化与优化、框架与架构、评测与基准、挑战与研究版图五类，核心应用覆盖 OpenMP 共享内存编程、MPI 分布式内存编程、CUDA GPU 编程，以及面向异构平台的混合并行工作流。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大型语言模型（LLM）与代码大模型（Code LLM）**

LLM 通常基于 Transformer，通过学习词元序列的概率分布，根据已有上下文预测并生成后续内容。Code LLM 在源代码、技术文档和自然语言描述上训练，因此能够在自然语言需求与 C、C++、Python、Fortran 等程序之间建立联系。

</div>
<div class="concept-item" markdown="1">

**并行编程模型**

并行编程模型规定多个计算单元如何分工和交换数据：OpenMP 主要面向同一节点内的共享内存线程，MPI 主要通过消息传递协调分布式进程，CUDA 则用于在 NVIDIA GPU 上组织大规模并行计算。实际 HPC 程序常组合多种模型，例如用 MPI 连接节点、用 OpenMP 使用节点内 CPU 核心。

</div>
<div class="concept-item" markdown="1">

**性能正确性与可扩展性**

HPC 程序不仅要产生正确结果，还要避免数据竞争、死锁及错误通信，并在增加处理器或问题规模后获得合理的加速。因而“代码可以编译或通过小样例”不足以证明其适合生产环境，还需检查通信开销、内存局部性、负载均衡和跨平台性能。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文不是提出单一生成算法，而是对 LLM 与 HPC 编程交叉领域进行结构化综述。其输入是从 IEEE Xplore、ACM Digital Library、arXiv 和 SpringerLink 等来源检索到的研究，检索主题包括“LLM for HPC”“parallel programming”和“code generation”；筛选侧重 2023 年以来、与 LLM-HPC 集成直接相关且具有技术深度的同行评审论文或高质量预印本，并排除缺乏 HPC 场景的通用 AI 研究及非技术性材料。分析对象包括通用 LLM、代码大模型及 HPC 专用模型在并行代码生成、性能优化、调试重构、文档教育、遗留代码迁移、作业脚本与环境配置等任务中的表现。输出是一套按五个主题组织的研究版图，以及对模型适用范围、正确性、性能可移植性、扩展能力、数据和评测缺口的综合判断；其默认场景是 LLM 辅助而非取代 HPC 专家，生成结果仍需编译、测试、性能分析和人工审查。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Godoy et al.（2024）的 LLM 并行编程助手研究**: 该工作代表将现有 LLM 助手用于编写 MPI、OpenMP 和 CUDA 代码的实践路径，为本文讨论 LLM 如何嵌入 IDE 或开发工作流提供直接案例。所给原文节选未提供该文的完整题名及具体评测结果。
- **chatHPC（Yin et al., 2024）**: chatHPC 代表部署在 HPC 中心门户中的领域化聊天助手，可帮助用户生成作业脚本或配置软件环境；它对应本文所讨论的检索增强和领域知识注入路线，也说明 LLM 的作用可以从代码生成延伸到系统使用支持。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

高性能计算编程横跨共享内存、分布式内存和异构硬件等环境，开发者需要掌握 OpenMP、MPI、CUDA 等不同并行范式，并处理内存局部性、节点间通信和可扩展性问题。这种工作专业门槛高、代码改造成本大；如果大语言模型能够生成并行内核、调整集群作业脚本或建议优化变换，就可能降低入门门槛、减少重复劳动并加快科学程序原型开发，但错误建议也可能直接破坏计算正确性或性能。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **通用大语言模型辅助编程**：利用主要在通用文本和代码上训练的模型，根据自然语言指令生成、解释或改写程序，并尝试补充 OpenMP 等并行指令、进行循环变换或给出平台相关的优化建议。
- **高性能计算领域专用大语言模型**：以 HPC-Coder、HPC-GPT、chatHPC 等系统为代表，通过领域数据微调、整理过的专用数据集或检索增强生成，将高性能计算代码、文档和系统知识引入回答过程，以提高领域任务上的准确性与相关性。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 通用模型在串行代码和类似 OpenMP 的共享内存任务上尚能取得一定效果，但在 MPI 等分布式范式中表现不足；这类任务对通信语义、正确性和跨节点扩展尤为敏感，因此“代码能够生成”并不等于能够安全用于实际集群。
- 领域专用模型虽可借助微调、精选数据和检索增强生成提高准确性，但适用范围仍较窄，现有验证又多局限于标准基准或微内核；再加上上下文长度限制、输出质量不稳定和缺乏 HPC 专用统一基准，其结果难以证明模型能可靠处理大型生产软件。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作分别展示了若干代码生成或优化能力，却缺少一个面向高性能计算完整开发流程的系统综合：尚不清楚不同模型和技术分别适用于哪些并行范式，其证据是否覆盖正确性、性能可移植性与规模扩展，以及从小型基准走向生产环境还需要补齐哪些数据、工具集成、评测和治理条件。

</div>
<div markdown="1"><span>核心问题</span>

现有大语言模型在高性能计算的代码生成、并行化与优化、框架支持和系统级指导中已经取得了什么能力、存在哪些可验证的边界，并应沿哪些方向发展，才能成为可信的高性能计算开发协作者？

</div>
<div markdown="1"><span>作者直觉</span>

作者选择结构化文献筛选与主题分类，而不是用单个基准给整个领域下结论，因为高性能计算中的“有效”包含多个层面：生成语法正确的代码、保持并行语义、获得实际加速以及扩展到更多节点并非同一件事。把研究按任务与技术层次归类，再比较通用模型和领域专用模型的证据，可以揭示局部成功是否依赖特定数据、范式或小规模测试，并据此区分真正可迁移的能力与尚未被生产场景验证的能力。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是提出或训练一个新的大语言模型，而是采用结构化文献综述方法，系统整理大语言模型在高性能计算（HPC）编程中的应用。完整流程是：在多个学术数据库中以通用词和领域词组合检索文献，依据时间范围、主题相关性、技术深度与可复现性进行筛选，再从模型类型、目标并行编程模型、评估策略和工作流集成深度四个维度编码，最后围绕七个研究问题，将证据归纳为代码生成、并行化与优化、框架与架构、评估与基准以及挑战与整体格局五类主题。

直观地说，作者先建立一份可追溯的“候选论文清单”，再用统一准则去除与 HPC 无关、缺少实证或内容重复的工作，随后给每篇论文贴上可比较的标签，最终横向判断不同方法能做什么、怎样发挥作用、效果如何、用什么标准测试，以及还存在哪些研究空白。该方法的产出是领域证据地图和批判性综合，而不是一个可直接执行的代码生成器或新的训练模型。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 确定综述范围与研究问题

作者将目标具体化为七个研究问题，分别覆盖既有用途、使用技术与交互模式、并行编程效果、指标和基准、与人工代码的比较、主要挑战及未来研究缺口。研究范围主要聚焦 2023 年以来明确处理 HPC 特有问题的同行评审论文，并为时效性和相关性纳入部分近期预印本。

<div class="method-step__io" markdown="1">

**输入**：LLM 辅助 HPC 编程这一研究主题，以及作者希望比较的应用、技术、效果、评估、人类基线、局限与研究空白。<br>
**输出**：一套约束后续检索、筛选和综合的分析问题，以及明确的时间与主题边界。

</div>

**直观理解**：这一步相当于在查资料前先写好七个必须回答的问题，避免最后只堆砌论文摘要。把范围限定在 HPC 特有任务，也能防止普通代码生成研究稀释结论。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多源检索与候选语料汇编

作者在五个来源中组合检索通用术语和领域术语，包括“Large Language Models”“High Performance Computing”“Parallel Programming”“LLM for HPC”和“Parallel Code Generation”等。由于缩写与全称返回的结果量可能明显不同，检索同时使用 LLM/HPC 及其完整写法，以降低措辞造成的漏检风险。

<div class="method-step__io" markdown="1">

**输入**：Google Scholar、IEEE Xplore、ACM Digital Library、arXiv 和 SpringerLink，以及由 LLM、HPC、并行编程、代码生成和自动化等概念组成的关键词集合。<br>
**输出**：可供筛选的候选文献语料，并通过公开代码仓库保存综述语料以支持复查和扩展。

</div>

**直观理解**：同一主题可能被作者写成缩写或全称，只搜索一种表达会漏掉论文。因此这里像用多组同义词在多个图书馆交叉查找，再把找到的记录集中到一份清单中。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 依据纳入与排除标准筛选文献

纳入工作必须明确研究 LLM 与 HPC 工作流的结合，并通过基准、实现细节或案例研究提供技术证据；优先考虑 2023 年以来的同行评审成果，也允许相关且近期的预印本。作者排除不涉及 HPC 或并行计算的一般 AI 论文、缺少实证和可复现信息的非技术或轶事性材料，以及与已有工作高度重叠且没有新增见解的派生论文。

<div class="method-step__io" markdown="1">

**输入**：检索得到的候选论文，以及表 2 和表 3 给出的纳入、排除标准。<br>
**输出**：主题相关、具有一定技术深度且重复度受控的最终评审文献集合。

</div>

**直观理解**：这一步不是按论文声称的效果挑选“好结果”，而是先检查它是否真正研究 HPC、是否拿出可检验的技术证据。重复或只有观点而没有实验支撑的材料不会成为核心证据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 统一编码、主题归类与跨论文综合

每篇论文按四个维度检查：所用模型属于通用 LLM 还是代码或 HPC 专用模型；面向 OpenMP、MPI、CUDA、HIP、OpenCL、SYCL、任务式或混合并行中的哪类编程模型；采用编译、语义正确性、运行时间、加速比、效率、扩展性、单元测试或专家验证等何种评价；以及系统被集成到 IDE 助手、独立框架、对话门户还是多智能体系统的何种深度。随后作者将证据组织到五个主题区域，并用这些横向维度回答研究问题、识别一致结论与方法缺口。

<div class="method-step__io" markdown="1">

**输入**：通过筛选的论文全文，以及七个研究问题。<br>
**输出**：关于 LLM 在 HPC 编程中的用途、实现方式、实证效果、评估惯例、工作流集成和未解决问题的结构化证据综合。

</div>

**直观理解**：作者不是逐篇复述，而是给所有论文使用同一张“信息表”。这样可以比较不同系统究竟测试了哪种并行范式、是否只会编译还是也能扩展，以及离真实 HPC 工作流还有多远。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文是结构化综述，不提出需要参数优化的模型、损失函数或训练目标；其方法目标是通过可追溯的检索、筛选、编码和主题综合，形成对 LLM-HPC 研究现状及缺口的证据地图。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 检索与筛选协议**

该模块由五类学术信息源、通用与 HPC 专用关键词、2023 年以来的主要时间窗口，以及显式纳入和排除标准构成。它要求候选工作明确涉及 LLM 对 HPC 工作流的支持，并具有基准、实现细节或案例证据，同时剔除一般 AI、非技术材料和无新增见解的重复研究。

> 直观理解：它决定哪些论文有资格成为证据，是综述可重复性的入口。如果检索词或筛选规则不透明，读者就无法判断结论来自完整证据，还是来自作者随意选择的少量论文。

**2. 四维文献编码框架**

作者从模型类型、目标编程模型、评价策略和 HPC 工作流集成深度四个维度分析每篇论文。该框架把模型能力与具体并行环境及验证方式对应起来，避免仅用“能否生成代码”这一宽泛标签评价系统。

> 直观理解：一段代码能够生成或通过编译，不等于它在 MPI 多节点环境中正确、高效且可扩展。四维编码迫使综述同时询问“谁生成、生成什么、怎样测、在哪里使用”。

**3. 研究问题驱动的主题综合**

七个研究问题提供分析主线，最终证据被整理为代码生成、并行化与优化、框架与架构、评估与基准、挑战与整体格局五类。该设计既描述现有系统，也要求比较效果、人类代码基线、评价覆盖和研究空白。

> 直观理解：主题分类负责把相近工作放在一起，研究问题则规定比较时必须回答什么。两者结合可避免综述退化为模型和工具名单。

**训练与推理**

不适用传统意义上的模型训练或推理流程。综述的“执行过程”是人工或研究团队层面的文献处理：先围绕七个研究问题确定范围，在五个信息源中用多种关键词表达检索，从候选结果中按表 2 和表 3 筛选，再按四个统一维度抽取信息，最后在五个主题下进行跨论文比较。原文未说明使用自动文献分类器、双人独立筛选、分歧仲裁、质量评分量表或统计元分析，因此不能把这些程序视为本文已经实施的方法。

**复现信息**

复现时需要保留的关键信息包括：检索来源为 Google Scholar、IEEE Xplore、ACM Digital Library、arXiv 和 SpringerLink；关键词同时覆盖 LLM/HPC 的缩写、全称及并行编程、代码生成和自动化等组合；主要关注 2023 年以来的研究；筛选规则见表 2 和表 3；公开语料仓库为 https://github.com/sljaljevic/llm-hpc-survey。公平解释结论时还应注意，节选原文没有报告各数据库的具体检索日期、完整查询字符串、初始命中数、去重后数量、最终纳入数量、审稿人数量或一致性统计，因此该流程具有公开框架和可扩展语料，但尚不足以仅凭当前章节逐条重建完整的系统综述筛选轨迹。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ParEval：包含 420 个并行计算任务，覆盖 12 类计算问题和 7 种编程模型，包括 OpenMP、MPI 与 CUDA。它主要用于函数级、短上下文条件下的代码生成评测，能够横向比较模型在多种并行范式中的语法、语义、运行性能和扩展能力；但其任务粒度可能低估真实代码库中的跨文件协调、构建系统和依赖管理难度。
- ParEval-Repo：面向真实代码仓库的串行到并行翻译基准，覆盖多种编程模型与真实仓库。它通过单元测试、集成测试、运行性能和专家审查考察长上下文、跨文件依赖、接口一致性以及构建系统处理能力，因此比函数级基准更接近软件现代化场景。原文未明确报告其仓库数量、数据划分或各子集规模。
- chatHPC 的合成评测数据：用于评估面向 HPC 的微调、服务与输出可靠性流程，并配合词法、语义和幻觉检测指标。该数据能够验证框架内部设计，但原文指出其主要依赖合成数据，且缺乏广泛的外部研究和跨计算中心部署，因而不能充分代表不同调度器、软件模块和安全策略下的生产环境。原文未明确报告数据规模与训练、验证、测试划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**$pass@k$**

在模型生成的前 $k$ 个候选程序中，至少有一个候选通过正确性测试的概率或比例。它比单次生成成功率更能反映采样多个候选时找到可运行解的机会，但仍依赖测试集是否充分覆盖并发错误和边界情况。 （越高越好，因为更高值表示在给定候选预算内更可能得到通过测试的程序；它不自动意味着程序具备良好运行性能或多节点扩展性。）

</div>
<div class="metric-item" markdown="1">

**运行效率**

衡量生成代码的执行时间、加速效果或相对参考实现的性能，用于区分“能够运行”与“适合 HPC 使用”。具体计时方式和归一化公式因被综述研究而异，原文未给出统一定义。 （通常执行时间越低或加速比越高越好，因为 HPC 代码不仅要正确，还需有效利用计算资源；跨硬件或不同测量协议的数值不能直接比较。）

</div>
<div class="metric-item" markdown="1">

**可扩展性**

考察程序在增加线程、进程、GPU 或计算节点后能否继续获得性能收益，反映通信、同步和负载均衡是否合理。该指标尤其适合发现只在小规模输入或单节点上有效的生成代码。 （在资源增加时保持更好的加速与效率通常更好；但原文未规定统一的强扩展或弱扩展计算公式，因此需要结合各被综述论文的实验协议解释。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### ParEval 的多范式函数级评测

<div class="result-value" markdown="1">

ParEval 提供 420 个任务，覆盖 12 类计算问题和 7 种编程模型；综述据此认为，通用 LLM 在顺序代码上表现较强，但处理并行编程复杂性时经常遇到困难。

</div>

该结果说明评测范围不只限于一种 API，而是同时检查 OpenMP、MPI、CUDA 等不同执行模型，因此能够暴露并行语义方面的系统性弱点。它并不证明所有通用模型在所有并行任务上都失败，也不代表函数级成功能迁移到完整应用；相反，短上下文任务可能高估模型面对真实仓库时的能力。

<div class="result-source" markdown="1">

来源：第 4.4 节 Evaluation and Benchmarking，Table 4 的相关讨论

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The ParEval benchmark introduced by Nichols et al. provides a comprehensive framework for assessing LLM performance on 420 parallel computing tasks across 12 computational problem types and seven programming models (including OpenMP, MPI, and CUDA).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### ParEval-Repo 的仓库级串行到并行翻译

<div class="result-value" markdown="1">

仓库级评测显示，模型在较大代码库上的成功并不稳定，反复出现构建系统生成、依赖连接和接口一致性问题。

</div>

这比单个函数是否通过测试更接近真实 HPC 软件现代化：模型必须同步修改多个文件，并保持构建脚本、依赖和接口彼此一致。结果表明，局部代码生成能力尚未转化为可靠的端到端工程能力；但原文没有给出统一成功率，因此只能得出定性结论，不能量化某个模型落后多少。

<div class="result-source" markdown="1">

来源：第 4.4 节 Evaluation and Benchmarking，ParEval-Repo 讨论

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

While ParEval-Repo addresses long context realism, success remains uneven on larger repos, with recurring issues in build system generation, dependency wiring and interface consistency—indicating current LLMs still struggle with end-to-end software modernization at scale.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 领域专用模型与通用模型的综合比较

<div class="result-value" markdown="1">

HPC-Coder、HPC-GPT 和 chatHPC 等经过领域微调、专门数据训练或检索增强的系统总体表现更好，并更接近 HPC 对可扩展性和资源效率的要求；但验证范围通常局限于受控基准或较小代码内核。

</div>

作者的综合判断是，高质量并行代码和针对性训练能够减少语法与领域知识错误，说明专业化具有实际价值。分析上，这些结果尚不能证明模型可稳定处理遗留代码、异构硬件、多节点通信和计算中心特定配置，因为现有测试分布较窄，也缺少大规模跨站点部署证据。

<div class="result-source" markdown="1">

来源：第 5.1 节对领域专用模型和评测证据的综合讨论

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Fine-tuned and domain-specific LLMs, such as HPC-Coder, HPC-GPT and chatHPC demonstrate improved performance, particularly when augmented with targeted instruction tuning, domain-specific datasets and RAG mechanisms.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 本文是综述，未在统一硬件、统一提示、统一模型版本和统一测试集上复现实验。不同论文的任务难度、代码粒度和指标定义并不一致，因此“领域模型更好”与“通用模型在 MPI 上较弱”等结论主要是作者对文献的综合判断，而不是严格受控的统计比较。
- 所给原文没有完整呈现 Table 4 的分模型数值，也未明确报告多数基准的数据划分、方差、显著性检验和失败率；同时存在训练数据与基准重叠的风险。故当前证据适合识别能力边界和研究方向，不足以据此选择生产模型或断言其在真实多节点 HPC 系统中的可靠性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 通用 LLM：作为领域专用系统的基本对照，用于检验仅依靠通用代码能力能否处理并行语义。该比较有意义，因为综述认为通用模型擅长顺序代码，却常在 MPI 等要求通信正确性和可扩展性的任务中失效。
- HPC-Coder：经过 HPC 代码或指令数据微调的领域模型，用来检验领域数据和专门训练是否改善并行代码生成的准确性及性能目标对齐。
- HPC-GPT：面向 HPC 场景的专用模型，与通用 LLM 对比可评估领域适配的收益；但综述同时强调，其证据多来自受控基准或小型内核，不能直接外推到完整生产应用。
- chatHPC：结合微调、部署、评测及检索增强生成的 HPC 框架，用来检验窄域知识、内部部署和可靠性检测是否优于普通提示式调用；其主要限制是合成数据和框架内部指标占比较高。

**实验想回答的问题**

- 现有评测是否表明，通用大语言模型能够正确生成、翻译或优化不同并行编程范式下的 HPC 代码，尤其是 OpenMP、MPI 与 CUDA 代码？
- 领域专用模型、仓库级基准和多维指标能否弥补传统函数级任务与文本相似度指标的不足，并可靠预测模型在真实 HPC 软件中的正确性、性能和可扩展性？

**实验实现**

本文是文献综述而非提出新模型的实验论文，因此没有统一训练配置、硬件平台、随机种子或数据划分。作者通过 IEEE Xplore、ACM Digital Library、arXiv 和 SpringerLink，以“LLM for HPC”“parallel programming”“code generation”等关键词筛选文献，重点关注 2023 年以来、与 LLM-HPC 结合相关且具有技术深度的同行评审论文和高质量预印本，并排除缺乏 HPC 语境的通用 AI 研究。实验结论来自对既有研究的综合：函数级 ParEval 使用多编程模型任务及正确性、性能和扩展指标；ParEval-Repo 使用单元测试、集成测试、运行性能与专家审查；chatHPC 使用词法、语义及幻觉检测。由于各研究的数据、硬件和评测协议不同，综述提供的是跨论文定性判断，而非受控条件下的统一排行榜。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- chatHPC 可视为部署型案例：它把领域微调、本地服务、词法与语义评测以及幻觉检测组织成完整流程，并强调在 HPC 环境中采用本地部署以满足安全和性能约束。该案例说明可靠性不能只依靠生成模型本身，还需要检索、检测和部署控制；但其评测主要使用合成数据和框架内部指标，缺少跨计算中心验证，因而尚不能证明它能适应不同调度器、模块系统和安全政策。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The survey primarily reviews LLM code generation, parallelization, optimization, and correctness for HPC programming.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`e58a76032011f245260229b46128052c4c43a0dc327199883b151a74f9ccf4a6`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
