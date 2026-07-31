---
title: "[论文解读] SciSchema.org: A Multidisciplinary Collection of Schemas for Structured Scientific Process Descriptions"
description: "[arXiv 2607.27955][LLM 其他] 本文发布 SciSchema.org：一个覆盖五类学科领域、包含 16 个专家标注科学过程模式的多学科资源，旨在把散落于论文不同载体中的过程信息转化为可复用的结构化描述。"
arxiv_id: "2607.27955"
announcement_date: "2026-07-31"
primary_category: "llm_nlp"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T05:30:51.542778+00:00"
source_sha256: "15016eadc0d3d6056ba7150bd32ca285a035399da8fb00614228a93394d988f7"
tags:
  - "LLM 其他"
  - "模式挖掘"
  - "科学过程模式"
  - "大语言模型"
  - "符号化科学知识结构"
  - "科学知识图谱"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 其他 · arXiv 2607.27955</p>

# SciSchema.org: A Multidisciplinary Collection of Schemas for Structured Scientific Process Descriptions

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> D'Souza, Jennifer, Sadruddin, Sameer, Rula, Anisa, Bossler, Ana, Fullana, Andrés, Bas, Enric, Ather, Syed, Circi, Defne, Chen, Anlan, Brinson, L. Catherine, Columbus, Alyssa, Demetriou, George, Jeong, Dongjun, Kumar, Tarun, Krüger, Frank, Genehr, Sascha, Budde-Sagert, Kai, Leonescu, Anamaria, Lodola, Francesco, Florindi, Chiara, Murthy, Gagana Balasubramanya, Olagbile, Samson Oluwapelumi, Riasat, Nazia, Sha, Yan, Shen, Kevin, Yang, Shaokai</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> TIB Leibniz Information Centre for Science and Technology, Hannover, Germany；University of Brescia, Brescia, Italy；University of Alicante, Alicante, Spain；Georgia Institute of Technology, Atlanta, United States；Duke University, Durham, United States；Johns Hopkins University, Baltimore, United States；University of Manchester, Manchester, United Kingdom；Wismar University of Applied Sciences, Wismar, Germany；University of Rostock, Rostock, Germany；University College London, London, United Kingdom；University of Milano-Bicocca, Milan, Italy；Cambridge Institute of Technology, Bengaluru, India</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27955) · [PDF 下载](https://arxiv.org/pdf/2607.27955) · **关键词** 模式挖掘, 科学过程模式, 大语言模型, 符号化科学知识结构, 科学知识图谱<br>


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

本文发布 SciSchema.org：一个覆盖五类学科领域、包含 16 个专家标注科学过程模式的多学科资源，旨在把散落于论文不同载体中的过程信息转化为可复用的结构化描述。

**不用术语来说**：一项科学实验或分析过程通常没有被完整地写在一个位置：所用材料可能出现在表格中，仪器参数写在正文里，操作步骤放在补充文件中，测量结果又通过图形呈现。人和计算机因此难以快速拼合出完整过程，也难以可靠地比较不同研究、复现实验或复用已有方法。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 发布首版 SciSchema.org，提供横跨生物与生物技术、材料与化学、成像与测量、物理和心理学的 16 个专家标注模式；这些模式以可复用字段统一表示过程的输入、输出、材料、工具、参数、条件、步骤、测量及来源信息。
- 构建并公开一套人机协同的模式挖掘资源链：大语言模型依据过程规范、科学论文和专家反馈生成候选结构，再由领域专家形成最终主模式；数据同时包含 JSON Schema、SHACL、模型中间结果、专家反馈、来源论文元数据、社区开发材料和分析脚本。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于科学知识表示与科学信息抽取的交叉领域。其核心背景是：论文中的实验或分析过程通常没有统一的机器可读结构，关键细节分散在正文、表格、图、实验协议和补充材料中，使跨论文比较、复现实验、复用流程及自动处理变得困难。SciSchema.org试图用跨学科的“过程模式”统一描述这些信息：每个模式预先规定某类科学过程应包含哪些可复用字段，例如输入、输出、材料、仪器或软件、参数、条件、操作步骤、测量结果及来源信息；首个版本包含16个经专家标注的模式，覆盖生物与生物技术、材料与化学、成像与测量、物理学和心理学。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**科学过程模式（scientific process schema）**

一种规定科学过程记录应包含哪些字段、字段具有何种结构的可复用模板。它描述的是一类过程的通用信息框架，而不是某一次实验的具体数值。

</div>
<div class="concept-item" markdown="1">

**JSON Schema与SHACL**

JSON Schema用于声明并验证JSON数据的字段、类型和结构；SHACL用于约束RDF知识图中的节点、属性及其取值。本文同时提供两种格式，使模式既能服务普通结构化数据，也能用于语义网和科学知识图谱。

</div>
<div class="concept-item" markdown="1">

**人在回路的模式挖掘（human-in-the-loop schema mining）**

先由大语言模型从过程说明、科学论文和专家反馈中生成候选结构，再由领域专家审查、修改并构建最终主模式。模型负责扩大候选结构的覆盖面，专家负责保证领域含义和最终结构的可靠性。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入包括科学过程规范、相关科学论文以及领域专家反馈；论文设定的应用环境是多个学科中过程描述分散、表达方式异构且缺乏统一字段的科学文献。处理目标不是直接抽取某篇论文的完整实验记录，而是通过大语言模型辅助产生候选模式，并由领域专家整合为可复用的最终主模式。输出是一套包含16个专家标注模式的多学科数据资源，最终模式以JSON Schema和SHACL两种机器可读格式发布，同时保留模型生成的中间模式、专家反馈记录、源论文元数据、社区开发材料与分析脚本。该设置默认不同过程虽然具有领域差异，但仍可通过输入、输出、材料、工具、参数、条件、步骤、测量和来源等字段形成可复用的结构化描述。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

科学过程的关键细节分散在正文、表格、图片、实验规程和补充文件中，而且不同学科采用不同的叙述方式。缺少统一结构会提高信息搜集与核对成本，并直接妨碍跨研究比较、实验复现、方法复用以及面向计算机的自动处理。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于文章话语的非结构化过程描述**：研究者使用自然语言正文，并结合表格、图形、规程和补充材料记录实验或分析过程；读者需要跨载体查找信息并自行还原各要素之间的关系。
- **大语言模型辅助的候选模式生成**：模型从过程规范、科学文章和专家反馈中归纳可能的字段与层级，形成候选结构，作为专家构建最终主模式的起点。该方式在本文中属于待整合进人机协同流程的技术入口，而不是被单独证明足以替代专家的方法。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 异构、分散的文章描述没有把输入、条件、步骤、测量和来源等信息组织成统一字段，导致过程实例难以被机器稳定读取，也难以直接开展跨论文比较。
- 仅依赖自动生成的候选结构无法从所给摘要中确认其领域正确性、完整性与复用能力；若缺少领域专家整理，模型输出可能不足以成为最终的权威主模式。原文未明确报告与其他自动模式挖掘方法的定量比较。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有科学文献表达与自动候选结构之间，仍缺少一个由领域专家定稿、同时覆盖多个学科并提供标准机器可读格式及完整开发记录的科学过程模式集合；这使结构化标注、知识图谱构建和语义出版缺乏可共同复用的过程描述基础。

</div>
<div markdown="1"><span>核心问题</span>

能否通过大语言模型生成候选结构、专家反馈和领域专家最终构建相结合的人机协同流程，形成一套跨学科、可复用且符合 JSON Schema 与 SHACL 表达要求的科学过程模式资源？

</div>
<div markdown="1"><span>作者直觉</span>

模型适合快速阅读多份过程规范和论文并提出字段草案，专家则能够判断某个字段在本领域是否准确、必要以及应如何组织。把前者的归纳效率与后者的专业判断结合起来，有望降低从零设计模式的成本，同时保留最终结构的学科可信度；再用标准格式发布，便于后续标注工具和知识图谱系统直接采用。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文的方法不是训练一个新的预测模型，而是构建一套“机器生成候选、专家持续纠偏、专家最终定稿”的人在回路（human-in-the-loop, HITL）科学过程模式挖掘流程。对每一种科学过程，研究者先收集领域说明、约 10 篇精心筛选的论文和约 50 篇或更多的扩展论文；随后让 12 个大语言模型各自沿三阶段轨迹迭代生成 JSON Schema 候选结构，并在阶段间注入领域专家对属性合并、分组、缺失项和描述质量的反馈；最后由专家比较至多 12 个候选，选择、编辑或融合它们，形成主模式，再由协调团队检查结构与格式并发布 JSON Schema、SHACL 及适用的 ORKG 模板。
直观地说，该流程把模式设计看成逐步整理“科学实验表格”的过程：先依据专家列出的关键项目搭出空表，再用少量高质量论文校准栏目，继而用大规模文献补全长尾细节，最后由真正理解该科学过程的专家决定哪些栏目应保留、如何嵌套以及应使用什么术语。大语言模型负责高通量地发现和组织候选字段，但不直接决定最终标准。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 科学过程筛选与输入材料准备

团队依据过程是否已有通常超过 15 年的稳定文献、是否具备足量可访问全文、以及论文中是否反复报告足够细致且相互关联的过程属性进行筛选；16 个最终确认的过程分别由专家编写含简述和 5–15 个初始属性的规格说明，并收集约 10 篇精心筛选论文及约 50 篇或更多的扩展论文。

<div class="method-step__io" markdown="1">

**输入**：社区提交的 29 个候选科学过程，以及每项提案的领域、过程名称、通俗说明和两篇代表性论文。<br>
**输出**：按过程组织的三类输入：领域规格说明、小型受控论文集和扩展全文语料库。

</div>

**直观理解**：并非任何研究主题都适合建立细粒度模式：如果论文只共享“数据准备—特征提取—分类”等宽泛阶段，最终只能得到浅层框架。该步骤优先选择拥有大量重复变量、人工逐篇归纳较困难的成熟过程。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段 1：依据领域规格生成初始模式

使用 schema-miner 的过程无关提示模板，要求 12 个大语言模型分别扮演模式设计者并独立输出带类型约束的 JSON Schema；此阶段不输入论文证据，专家随后审阅每个初始候选。

<div class="method-step__io" markdown="1">

**输入**：某一过程的名称、简短说明及专家给出的 5–15 个初始属性。<br>
**输出**：每个过程最多得到 12 个彼此独立的初始候选模式，以及供下一阶段使用的专家反馈。

</div>

**直观理解**：这一步先画出多个版本的“栏目草图”，以便观察不同模型如何扩展专家给出的少量关键属性。由于尚未读取文献，这些结果只是起点，不被视为可靠的最终模式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段 2：受控论文证据与周期性专家纠偏

精选论文被分成两个批次，在每条模型轨迹中顺序处理；每次迭代向模型提供下一篇论文、上一轮模式及最近一次可用反馈，批次 1 使用阶段 1 反馈，专家复审后再以新反馈驱动批次 2。

<div class="method-step__io" markdown="1">

**输入**：阶段 1 候选模式、每个过程约 10 篇人工精选论文，以及关于属性合并、分组、遗漏和描述质量的专家反馈。<br>
**输出**：经高相关文献证据校准的第二阶段模式，以及用于启动阶段 3 的第二轮专家意见。

</div>

**直观理解**：精选论文类似少量高质量样例，帮助模型确认哪些栏目确实在文献中出现。分批审阅则像在长任务中设置检查点，既让专家及时纠偏，又避免要求专家在每篇论文后都进行评审。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段 3：扩展语料迭代精炼

扩展语料同样分为两个批次，沿各模型既有轨迹持续更新模式：批次 1 从阶段 2 结果和反馈开始，专家复审后以新反馈处理批次 2；模型若因累积模式与论文输入超出上下文处理能力而无法返回有效结构，则该轨迹不产生最终候选。

<div class="method-step__io" markdown="1">

**输入**：阶段 2 的模式、对应专家反馈，以及每个过程约 50 篇或更多的扩展全文论文。<br>
**输出**：每个科学过程至多 12 个最终的模型生成候选模式。

</div>

**直观理解**：这一阶段用更大的文献覆盖面寻找精选样例未包含的字段和变体，相当于对栏目表做覆盖面压力测试。输出仍只是候选，因为文献中频繁出现的写法不一定等于科学上最合理的组织方式。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文是数据集与模式构建工作，没有提出需要通过损失函数优化的新模型，也未对所用大语言模型进行参数训练或微调；schema-miner 通过提示调用现有模型生成和修订候选 JSON Schema，真正被持续更新的是外部模式文件，而不是模型权重。最终质量控制依赖领域专家反馈、候选比较和主模式编辑，而非一个自动优化目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 多模型独立模式轨迹**

每个过程同时运行 12 条互不合并的三阶段轨迹，模型覆盖指令微调型与推理导向型，并同时包含不超过 80 亿参数的小模型和更大模型；每条轨迹始终继承自身上一轮模式，从而保留可追踪的演化链。

> 直观理解：不同模型可能擅长发现不同字段或组织方式，独立运行可提供多样化候选，避免最终设计过度依赖单一模型。这里的模型比较主要服务于候选生成与专家选择，而不是通过投票自动产生最终模式。

**2. 论文驱动的迭代模式更新器**

schema-miner 版本 3.2.5 将过程规格、逐篇论文、前序 JSON Schema 和最近的专家反馈组合为模型输入，使模式随证据逐轮扩展或修订；小型精选集和大型扩展集分别承担高相关性校准与覆盖面扩展的作用。

> 直观理解：模型不是一次读完全部论文后直接给答案，而是边读边维护一份不断更新的结构化草稿。这使新增字段能够联系到具体文献阶段，也让专家有机会在错误累积前进行干预。

**3. 分层专家控制与来源记录**

迭代阶段的反馈表关注属性合并、属性分组、缺失属性、描述充分性及可选 JSON 直接修改；最终阶段另设五点评分和主模式构建表，要求专家说明采用了哪些模型候选以及最终结构各部分如何形成。

> 直观理解：该模块把专家角色从简单打分者提升为模式作者：专家既能在中途指出问题，也拥有最终编辑权。来源记录则帮助使用者区分模型建议、专家修订和最终发布结构，提高数据集的可审查性。

**训练与推理**

整个流程属于现有大语言模型的推理调用与人工编纂，不包含本文自有模型的训练阶段。对每个过程，12 个模型首先仅根据规格说明生成初稿；随后在精选论文的两个批次中，模型反复接收“下一篇论文、上一轮模式、最近专家反馈”并输出更新模式；再以相同机制处理扩展语料的两个批次。专家在阶段 1 后、阶段 2 的两个批次后以及阶段 3 批次 1 后提供阶段性意见，并在阶段 3 批次 2 后对最终候选进行五点评分和融合编辑；若某模型无法在累积上下文中输出有效模式，该轨迹可能缺失，因此每个过程的候选数是“至多 12 个”而非固定 12 个。

**复现信息**

复现核心流程需要 schema-miner 版本 3.2.5；源码以 MIT License 发布于 https://github.com/sciknoworg/schema-miner，并可通过 PyPI 安装。模型和服务提供商通过命令行参数或环境配置文件指定，过程名称、说明和规格属性则作为过程无关提示模板的参数，因此更换过程、模型或提供商通常不需要修改代码。公平解释结果时需注意三点：各过程的大型语料规模会随全文可访问性而变化；专家并非每处理一篇论文就反馈，而是在预设批次边界集中评审；上下文容量不足可能导致某些模型轨迹没有有效最终候选。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 核心评估对象是 SciSchema.org 首个版本：包含 16 个由专家标注的科学过程模式，覆盖 Biology & Biotechnology、Materials & Chemistry、Imaging & Measurement、Physics 和 Psychology 五类学科领域。每个模式描述过程实例应记录的字段，如输入、输出、材料、仪器或软件、参数、条件、步骤、测量和来源信息。它是模式集合，不是已填充的文章级过程实例数据集；原文未报告训练集、验证集或测试集划分。
- 模式开发的候选池包含 29 个被提议的科学过程，横跨分子生物学、神经科学、心理学、粒子物理、天文学、化学、材料科学、工程、人工智能、计算成像和医学等领域。该候选池用于筛选适合建立模式的成熟过程，筛选依据包括文献成熟度、可访问全文规模以及过程属性是否稳定且反复出现；它不是模型性能测试集。
- 发布包还包含中间模型生成模式、专家反馈记录、源论文元数据、社区开发材料和分析脚本。其作用是支持开发过程追踪、专家审查与可复现检查；所给原文没有明确报告各子集的文件数、文章数、字段总数或固定划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**模式结构检查**

检查最终模式是否具有可用于描述科学过程的组织结构和字段设计。所给原文只说明进行了该项技术验证，没有给出量化定义、通过阈值或聚合得分。 （原文未定义数值方向；若按合格性检查理解，满足预定结构要求优于不满足，但不能据此推断模式的语义完整性。）

</div>
<div class="metric-item" markdown="1">

**开发来源与专家审查检查**

检查候选模式如何由过程说明、科学论文、模型输出和专家反馈逐步形成，并确认领域专家参与最终主模式构建。原文未给出专家间一致性、覆盖率或审查通过率。 （原文未定义数值方向；来源记录更完整、专家审查更充分通常更可信，但本文节选没有提供可比较的量化尺度。）

</div>
<div class="metric-item" markdown="1">

**JSON Schema 与 SHACL 语法符合性**

检查两种机器可处理表示能否满足相应格式或验证工具的语法约束。该指标主要发现格式错误，并不直接衡量字段是否科学正确、是否覆盖全部重要过程信息。 （若以验证通过情况计，更多模式通过或更少语法错误更好；所给原文未报告具体通过数、错误数或比例。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 首个版本的跨学科覆盖与资源规模

<div class="result-value" markdown="1">

作者报告发布了 16 个专家标注模式，覆盖五个宽泛学科类别。这是资源规模和覆盖面的描述性结果，并非与其他模式库比较后得到的性能提升。

</div>

该结果表明资源不是围绕单一实验技术建立，而是尝试验证同一套过程描述思想能否跨学科使用。它不证明 16 个模式足以代表这些学科，也不证明字段覆盖完整、专家之间一致或下游任务性能更高。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We present the first release of SciSchema.org, a multidisciplinary collection of 16 expert-annotated schemas spanning Biology & Biotechnology, Materials & Chemistry, Imaging & Measurement, Physics, and Psychology.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 候选过程筛选

<div class="result-value" markdown="1">

社区征集形成了 29 个候选过程，随后依据过程成熟度、可访问文献规模和过程信息粒度进行内部筛选。该数字反映筛选入口的广度，而不是最终模式的准确率或召回率。

</div>

先从较广的候选池选择文献稳定、属性丰富的过程，有助于避免为新颖但资料稀少的技术构建脆弱模式。不过，内部筛选没有外部基准或盲审对照，因此不能据此判断未入选过程不适合结构化，也无法量化选择偏差。

<div class="result-source" markdown="1">

来源：Methods — Community formation and process selection — Process screening and selection

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The resulting submissions formed a candidate pool of 29 proposed processes spanning molecular biology, neuroscience, psychology, particle physics, astronomy, chemistry, materials science, engineering, artificial intelligence, computational imaging, and medicine.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 发布格式与技术验证范围

<div class="result-value" markdown="1">

最终模式同时以 JSON Schema 和 SHACL/Notation3 发布，两种表示编码相同内容；作者称技术验证检查了模式结构、开发来源、专家审查和语法符合性。所给原文未明确报告逐模式通过数、失败数或验证比例。

</div>

双格式发布分别服务于普通文档或软件系统以及 RDF 知识图谱，说明成果重视互操作性。语法符合性只能证明文件可被相应生态解析或验证，不能证明模式在科学上完备，也不能证明信息抽取、检索或跨研究比较等下游应用已经获得性能收益。

<div class="result-source" markdown="1">

来源：Background & Summary

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

They are released as JSON Schema for document- and software-oriented reuse and SHACL/Notation3 for RDF and knowledge-graph reuse, with both representations encoding the same content.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给原文没有提供技术验证的逐模式结果、验证通过率、错误类型、专家一致性或字段覆盖率，也没有与既有模式库、纯人工设计、纯大语言模型生成等基线比较。因此目前可以确认资源的规模、表示形式和验证维度，却不能定量判断模式质量优于其他方案。
- 过程筛选偏向拥有长期、稳定且可访问文献，并具有大量重复过程变量的成熟领域；这种策略有利于构建内容丰富的模式，但可能降低对新兴技术、文献稀少领域、受限访问文献和结构较简单计算流程的代表性。本文发布的是过程类及字段定义，而不是已填充的文章级执行记录，所以下游抽取准确性、复现成功率和跨研究比较收益仍需另行验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。

**实验想回答的问题**

- 首个版本的数据资源是否覆盖多个学科，并以可复用、机器可处理的形式提供科学过程模式，而不是仅提供文章级过程实例？
- 所采用的人机协同模式挖掘与技术验证流程，是否能够产出经过领域专家审查且在 JSON Schema 与 SHACL 表示上符合语法要求的最终模式？

**实验实现**

评估属于数据集技术验证，而不是预测模型的训练—测试实验。整体流程先公开征集领域专家提出过程及代表性论文，再从 29 个候选过程中筛选具有成熟文献、足够可访问全文和丰富重复属性的过程；随后由大语言模型依据过程说明、科学论文与专家反馈生成候选结构，最终由领域专家构建主模式。发布时将相同模式内容编码为面向文档和软件复用的 JSON Schema，以及面向 RDF 与知识图谱复用的 SHACL/Notation3。原文概述的验证维度包括模式结构、开发来源、专家审查和语法符合性，但所给章节未明确报告所用模型的完整配置、文章采样规模、验证命令、错误判定规则、人工评审协议或逐模式统计结果，因此无法复现为标准化的量化基准实验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原子层沉积示例展示了模式驱动比较的潜在用途：ORKG 中的说明性比较覆盖 200 多篇研究论文，并用七个模式属性组织报告值。该案例说明结构化字段可能让过程特定检索直接呈现跨论文比较，而不只返回全文列表；但它采用的是一个简单的说明性模式，且原文没有设置无模式检索对照、用户研究或检索指标，因此只能视为应用演示，不能作为 SciSchema.org 整体有效性的定量证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The main contribution is a collection of scientific process schemas, while LLMs are only used within the dataset-construction workflow.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`15016eadc0d3d6056ba7150bd32ca285a035399da8fb00614228a93394d988f7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
