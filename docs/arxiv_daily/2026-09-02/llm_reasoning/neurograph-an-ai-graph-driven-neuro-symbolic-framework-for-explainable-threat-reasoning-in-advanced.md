---
title: "[论文解读] NeuroGraph: An AI Graph-Driven Neuro-Symbolic Framework for Explainable Threat Reasoning in Advanced Manufacturing"
description: "[arXiv 2609.00604][LLM Reasoning] 本文提出NeuroGraph及其GRICS架构，以“符号查询优先、语言模型生成受证据约束”的方式，在统一的工业安全知识图谱上实现跨信息技术与操作技术环境的可解释威胁推理。"
arxiv_id: "2609.00604"
announcement_date: "2026-09-02"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:48:54.124535+00:00"
source_sha256: "d3b1ed9d6177891b0869fa035edc0319f3cf487a8e1990041c18f436bf45e575"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "Explainable Artificial Intelligence"
  - "Large Language Models"
  - "Cybersecurity"
  - "Advanced Manufacturing"
  - "Knowledge Graphs"
  - "Neuro-symbolic"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.00604</p>

# NeuroGraph: An AI Graph-Driven Neuro-Symbolic Framework for Explainable Threat Reasoning in Advanced Manufacturing

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Padmeswari Nandiya, Ahmad Mohsin, Ahmed Ibrahim, Iqbal H. Sarker, Helge Janicke</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: School of Science (Computing & Security Discipline), Edith Cowan University, Perth, WA 6027, Australia；Affiliation: School of Science (Computing & Security Discipline)；Edith Cowan University, Perth, WA 6027, Australia</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00604v1) · [PDF 下载](https://arxiv.org/pdf/2609.00604v1) · **关键词** Explainable Artificial Intelligence, Large Language Models, Cybersecurity, Advanced Manufacturing, Knowledge Graphs, Neuro-symbolic<br>


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

本文提出NeuroGraph及其GRICS架构，以“符号查询优先、语言模型生成受证据约束”的方式，在统一的工业安全知识图谱上实现跨信息技术与操作技术环境的可解释威胁推理。

**不用术语来说**：先进制造系统把办公网络、工业设备和物理生产过程连接在一起，攻击者可能沿多个环节逐步扩散；安全分析人员因此需要把分散的漏洞、设备、攻击手法和事件信息串联起来。现有问答工具可能给出缺乏依据的答案，也往往不能清楚展示答案经过了哪些关系和证据，导致分析人员难以核验并据此处理可能产生物理后果的攻击。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出符号优先的神经—符号检索架构：第一阶段将分析人员的自然语言问题转换为受本体约束的可执行Cypher查询，并以知识图谱执行结果作为主要证据；仅在符号查询失败时使用向量检索寻找图锚点，而且锚点必须再次转化为符合本体的Cypher查询后才能进入回答阶段。
- 建立可审查的图证据推理流程：依托BRIDG-ICS本体统一连接资产、漏洞、弱点、攻击技术与对手行为，并向分析人员暴露生成的Cypher查询、检索到的图证据和最终自然语言回答，以支持跨IT与OT实体的多跳分析和逐阶段核验。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文面向先进制造与工业控制系统（ICS）的网络威胁情报（CTI）分析。现代工业环境连接信息技术（IT）、运营技术（OT）与物理过程，攻击者可沿资产、漏洞、弱点和攻击技术之间的关系实施多阶段攻击，并造成实际物理后果。传统检索增强生成（RAG）虽能让大语言模型查询外部情报，但文本检索难以稳定表达实体关系，且生成结果可能缺乏证据支持；Graph-RAG通过知识图谱组织关系，却仍可能缺少符合本体约束的多跳推理和可核查的证据轨迹。本文因此研究如何让分析员以自然语言提问，由系统在统一的工业网络安全知识图谱上执行结构化检索，并依据检索证据生成可解释答案。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**工业控制系统（ICS）**

ICS是监测和控制工业设备及生产过程的计算系统，广泛用于制造、能源和公共设施。其安全问题同时涉及IT网络、OT设备和物理过程，因此网络攻击可能造成停产、设备损坏等现实后果。

</div>
<div class="concept-item" markdown="1">

**知识图谱与网络安全本体**

知识图谱把资产、漏洞、弱点、攻击技术等对象表示为节点，并用边记录它们之间的明确关系；本体则规定允许出现的实体类型、关系及语义约束。沿图中关系连续遍历多个节点称为多跳推理，可用于追踪从受影响资产到漏洞及攻击行为的关联链。

</div>
<div class="concept-item" markdown="1">

**神经符号推理与Graph-RAG**

神经符号方法结合大语言模型的自然语言处理能力与符号程序的可执行、可检查推理；Graph-RAG则从知识图谱而非纯文本片段中获取回答上下文。本文采用“符号优先”方式：模型生成受本体约束的Cypher图查询，查询执行结果才可成为后续答案的证据。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是网络安全分析员针对先进制造环境提出的自然语言问题，目标输出是由图证据支撑的自然语言威胁分析，以及可供检查的Cypher查询和检索结果。系统运行于跨IT与OT领域的异构网络安全知识图谱之上，需要关联CVE、CWE、MITRE ATT&CK、CAPEC、资产清单和事件报告等知识，并支持跨资产、漏洞、弱点、攻击技术与对手行为的多跳检索。本文假设已有依据BRIDG-ICS本体整理完成的知识图谱，研究范围是图扎根威胁推理，而非本体构建与维护、自动化本体演化、持续CTI摄取或知识图谱实时同步。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **BRIDG-ICS ontology（Nandiya et al., 2026）**: 它是GRICS所依赖的既有网络安全本体，用统一知识图谱描述工业环境中的网络物理资产、漏洞、弱点、攻击技术和对手行为。本文假设该图谱已经过整理，并在其上研究图扎根推理，而不把本体构建作为贡献。
- **Graph Retrieval-Augmented Generation（Graph-RAG）**: 既有Graph-RAG利用知识图谱改善纯文本RAG的关系建模，但本文指出其常以嵌入相似度、图扩展、聚类或学习式图表示构造上下文，对异构工业网络安全知识的本体一致多跳推理和中间证据追踪支持有限。GRICS改以可执行Cypher作为主要证据检索机制，仅在符号查询失败时使用嵌入检索寻找图锚点，随后仍须重新生成符合本体的Cypher查询。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

工业控制系统广泛用于能源、制造和公共设施，其数字化与联网扩大了攻击面；攻击还可能从IT网络跨越到OT设备和物理过程，造成现实运行后果。面对这种多阶段、跨域攻击，分析人员必须联合理解CVE、CWE、MITRE ATT&CK、CAPEC、资产清单和事件报告等异构资料，但又不应被要求直接编写复杂的图查询，因此需要一种既便于自然语言交互、又能给出可验证证据链的辅助分析机制。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于大语言模型的文本检索增强生成**：先从外部网络安全文本中检索与问题相关的片段，再把片段作为上下文交给语言模型生成答案，从而补充模型参数中未包含或可能过时的威胁知识。
- **图检索增强生成**：将资产、漏洞、弱点和攻击模式表示为知识图谱中的节点与关系，再通过嵌入相似度、图扩展、聚类或学习到的图表示构造回答上下文，使模型能够利用实体之间的结构化联系。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 文本检索增强生成仍可能产生无证据支持的内容，而且对跨IT、OT和物理过程的关系链缺少显式结构化操作；其后果是模型难以稳定回答需要连接多个实体和多个步骤的威胁问题。
- 现有图检索增强方法往往只覆盖网络安全生态的一部分，或缺少受统一本体约束的多跳查询与中间证据展示；其后果是异构来源之间的关系可能不完整或不一致，分析人员也难以检查结论究竟由哪些图路径推导而来。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种面向工业网络安全的统一机制，能够让非图查询专家以自然语言提问，同时把每个问题编译为本体一致、可执行且可追踪的图查询；该机制还须保证下游回答只使用显式图执行返回的证据，并在符号查询失败时让神经检索仅辅助恢复图锚点，而不是绕过符号推理直接提供答案。

</div>
<div markdown="1"><span>核心问题</span>

在已有、经过整理的BRIDG-ICS网络安全知识图谱上，能否通过双大语言模型与符号优先检索相结合，把自然语言问题可靠地转换为可执行Cypher查询，并仅依据查询返回的图证据生成答案，从而支持跨IT与OT实体的多跳威胁推理、减少无依据生成并提供可核验的推理轨迹？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把语言模型擅长的“理解问题和组织语言”与知识图谱擅长的“按明确关系执行查询”分开：第一个模型只负责把问题翻译成受本体限制的程序，图数据库负责确定性地沿关系取证，第二个模型再把这些证据表述成人类可读答案。直观上，这相当于要求模型先提交可检查的检索步骤和证据，再允许它下结论；即使初始查询失败，向量检索也只负责找到重新进入图结构的位置，最终证据仍必须经过显式图查询获得。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

GRICS（Graph-Integrated Retrieval for Industry-Centric Security）是面向工业物联网、工业控制系统以及其他工业 $IT/OT$ 环境的领域专用知识图谱增强生成框架。其输入是分析人员的自然语言威胁问题 $q$，系统先利用受 $BRIDG\text{-}ICS$ 本体约束的第一个大语言模型生成可执行的 $Cypher$ 查询，再在 $Neo4j$ 知识图谱中检索节点、边和多跳路径，最后由第二个大语言模型仅依据检索到的证据生成答案。整体设计将自然语言理解、符号图遍历和语言生成分离：第一个模型负责“如何查”，图数据库负责“查到什么”，第二个模型负责“如何表述”。

知识图谱统一表示工业资产、软件、漏洞、弱点、攻击模式、$MITRE\ ATT\&CK$ 技术和运营区域等异构实体，并显式建模它们之间的语义关系与通信关系。因此，系统不仅能回答单个漏洞问题，还能沿着“工业资产 $\rightarrow$ $CVE$ $\rightarrow$ $CWE$ $\rightarrow$ $CAPEC$ $\rightarrow$ $MITRE\ ATT\&CK$”等链路分析攻击路径。嵌入检索不是独立的答案生成器，而只在符号查询失败时寻找图中的候选锚点，随后重新生成并执行符号查询，以保持最终证据的图结构可追溯性。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构建并规范化网络安全知识图谱

系统依次进行数据抽取、实体规范化、关系映射和图导入：使用规范标识符对漏洞、弱点、攻击模式、软件和攻击技术等实体去重，并依据 $BRIDG\text{-}ICS$ 建立类型化关系。结果以带标签属性图形式存入 $Neo4j$，其中实体是带标签节点，关系是带类型边，描述性字段是节点或关系属性。

<div class="method-step__io" markdown="1">

**输入**：来自 $CVE$、$CPE$、$CWE$、$CAPEC$、$MITRE\ ATT\&CK$ 以及真实工业互联网和 $OT$ 测试床的异构网络安全记录；$BRIDG\text{-}ICS$ 本体及其类别、属性和关系定义。<br>
**输出**：知识图谱 $\mathcal{G}=(\mathcal{V},\mathcal{E})$，包含网络资产、工业组件、漏洞及其语义和运营依赖关系；通信边还可携带 $pExploit$、$riskWeight$、$controlStrength$ 和 $costAttack$ 等风险属性。

</div>

**直观理解**：这一步像把多个安全资料库整理成一张统一的关系地图：同一个漏洞不会因来源不同而被重复记录，且每条连接都有明确含义。这样系统之后检索的不是互不相连的文本片段，而是可以沿关系逐步追踪的攻击路径。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 生成并执行本体约束的符号查询

第一个大语言模型 $\mathrm{LLM}_{\mathrm{cypher}}$ 根据紧凑本体、查询指令和用户问题生成一个或最多三个候选 $Cypher$ 查询；系统去重并进行语法验证，只执行符合图模式的查询。对长问题，系统可将问题拆分为不超过预设上限的语义片段，并使用 $CONTAINS$ 条件分别查询相关概念。

<div class="method-step__io" markdown="1">

**输入**：用户自然语言问题 $q$、知识图谱 $\mathcal{G}$ 和本体模式 $\mathcal{O}$，其中模式包含合法节点标签、关系类型和属性名。<br>
**输出**：若任一查询成功并返回非空结果，则得到证据集 $R$，其中包括本体一致的节点、边、节点属性以及可能的多跳路径；若查询语法错误、执行失败、引用无效模式或返回空结果，则进入回退机制。

</div>

**直观理解**：第一个模型不直接回答问题，而是把问题翻译成数据库能执行的查找指令。本体像一份“允许使用的词汇表和道路规则”，限制模型不能凭空创造图中不存在的实体或关系。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 失败时进行嵌入锚定并重新符号检索

系统将 $q$ 与每个节点编码到同一向量空间，以余弦相似度选取最高相似度的节点，或选取前 $k$ 个候选节点作为图锚点。随后把原问题、候选锚点和本体再次提供给 $\mathrm{LLM}_{\mathrm{cypher}}$，重新生成符合本体的 $Cypher$ 查询并在 $\mathcal{G}$ 上执行。

<div class="method-step__io" markdown="1">

**输入**：失败的原始查询、用户问题 $q$、所有图节点 $\mathcal{V}$ 及其向量表示；文中使用 $all\text{-}MiniLM\text{-}L6\text{-}v2$ 生成节点和问题嵌入。<br>
**输出**：成功时输出回退后的证据集 $R'$；该证据仍来自图中的显式节点、边和多跳遍历，而不是直接把相似向量对应的节点当作答案。若所有候选锚点都无法得到非空结果，算法返回空集。

</div>

**直观理解**：当模型没能写出可执行查询时，系统先用语义相似度猜测“可能相关的图中实体”，再让符号查询沿图继续查找。嵌入只负责找入口，不能替代后续的关系验证，因此它更像故障恢复用的导航，而不是最终证据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 基于图证据生成并展示答案

第二个大语言模型接收结构化子图作为上下文，并被明确要求只能依据检索到的图证据进行回答，不得引入未支持的外部知识。系统将生成的自然语言结果与可检查的图关系和检索过程一同呈现给分析人员，用于攻击分析、漏洞识别、风险理解和缓解规划。

<div class="method-step__io" markdown="1">

**输入**：成功检索得到的证据集 $R$ 或 $R'$，包括图路径、节点属性、关系信息、漏洞描述、严重性或 $CVSS$ 字段，以及用户原始问题。<br>
**输出**：面向分析人员的图依据威胁分析答案，包括漏洞解释、攻击路径、攻击技术归因、潜在影响或缓解建议；同时保留可追踪的图证据，使用户能够检查答案所依赖的节点和关系。

</div>

**直观理解**：第二个模型像一名只准查阅指定档案的报告撰写者：它负责把已验证的图证据组织成易读答案，但不能用自己的常识补写缺失事实。分析人员可以回看档案中的连接，判断答案是否确实由图中证据支持。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 网络安全知识图谱表示

$$
\mathcal{G}=(\mathcal{V},\mathcal{E},\mathcal{R})
$$

**符号说明**

- $\mathcal{G}$：整体网络安全知识图谱。
- $\mathcal{V}$：图中实体节点集合，例如工业资产、漏洞、弱点和攻击技术。
- $\mathcal{E}$：节点之间的关系边集合。
- $\mathcal{R}$：关系类型集合，用于区分漏洞关联、攻击技术使用、区域归属和通信等语义。

<div class="equation-explanation" markdown="1">

**直观理解**：该表示把安全知识拆成三部分：有哪些对象、对象如何连接以及连接分别代表什么。它是后续多跳查询和证据追踪的结构基础，而不是一个需要通过训练直接优化的预测公式。<br>
**原文位置**：第 2.1 节，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 嵌入相似度图锚点选择

$$
\hat{v}=\arg\max_{v^{\prime}\in\mathcal{V}}\mathrm{cosine}\left(f_{\mathrm{emb}}(q),f_{\mathrm{emb}}(v^{\prime})\right)
$$

**符号说明**

- $\hat{v}$：被选作回退检索入口的最高相似度图节点。
- $q$：用户提交的自然语言网络安全问题。
- $\mathcal{V}$：知识图谱中的节点集合。
- $f_{\mathrm{emb}}$：将问题或图节点映射到向量空间的嵌入函数。
- $\mathrm{cosine}(\cdot,\cdot)$：两个向量之间的余弦相似度，用于衡量语义接近程度。
- $v^{\prime}$：被比较的候选图节点。

<div class="equation-explanation" markdown="1">

**直观理解**：系统比较问题向量与每个节点向量，选择语义上最接近的节点作为重新生成符号查询的起点。这个公式只决定“从哪里开始查”，不直接决定最终答案，也不证明该节点与问题之间存在完整攻击关系。<br>
**原文位置**：第 5.3.1 节，公式（2）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：所给章节未明确给出统一的损失函数、优化目标或参数更新公式。文中说明第一个 $Cypher$ 生成模型采用提示工程、领域适配和进一步微调以提高本体一致查询生成，第二个答案生成模型“不进行微调”；但训练数据构造、监督信号、优化器、损失函数和训练轮数在所给内容中均为原文未明确报告。因此，能够确定的是：训练或适配目标是提高可执行且符合 $BRIDG\text{-}ICS$ 模式的 $Cypher$ 生成能力，而不是端到端直接优化最终答案指标；具体优化实现不能仅凭所给章节复现。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. BRIDG-ICS 网络安全知识图谱与本体层**

该模块将 $CVE$、$CPE$、$CWE$、$CAPEC$、$MITRE\ ATT\&CK$、工业资产、软件组件和运营区域映射到统一的 $BRIDG\text{-}ICS$ 类别体系。关系包括 $has\_Vulnerability$、$has\_CWE$、$use\_Technique$、$located\_In(Zone)$ 和 $Attack(Asset)$；通信关系 $COMMUNICATES\_WITH$ 可附带漏洞利用概率、风险权重、控制强度和攻击成本等属性。关系只有在来源映射或本体定义支持时才被实例化。

> 直观理解：它规定图中有哪些对象以及对象之间哪些连接是合法的，相当于安全领域的统一数据字典和关系地图。其价值在于把不同数据库中的记录放进同一套语义框架，支持跨漏洞、弱点、攻击模式和工业资产的多跳追踪。

**2. 双大语言模型的本体约束检索与回答架构**

第一个模型接收 $\mathcal{O}$ 和 $q$，生成并验证 $Cypher$ 查询，负责符号检索；第二个模型接收检索子图，负责受证据约束的答案合成，且不进行独立检索。该职责分离使查询生成错误可以单独检查，也避免回答模型在没有图证据时自由扩展事实。

> 直观理解：系统把“查资料”和“写报告”交给两个不同角色，而不是让一个模型同时搜索、推理和编造答案。这样分析人员能分别检查查询是否合法、图中查到了什么以及最终文字是否忠实于证据。

**3. 嵌入式故障回退与重新锚定机制**

节点记录使用 $all\text{-}MiniLM\text{-}L6\text{-}v2$ 转换为 $384$ 维向量，并以余弦相似度寻找语义候选节点。回退仅在 $Cypher$ 执行失败时启动；候选节点被重新交给查询生成模型，生成的查询仍需在知识图谱中执行，因而最终证据保持符号图基础。

> 直观理解：符号查询精确但可能因问题表达复杂而失败，向量相似度则提供较灵活的“找入口”能力。二者结合后，系统既能恢复部分失败查询，又不会把向量相似度本身误当成已经验证的攻击关系。

**训练与推理**

训练或离线准备阶段，系统从多个权威网络安全来源和工业 $IIoT/OT$ 测试床收集记录，将其转换为节点表和关系表，使用规范标识符进行实体归一化，并按照 $BRIDG\text{-}ICS$ 本体建立关系后导入 $Neo4j$。在固定的知识图谱快照上准备训练和评估数据；图节点记录另行编码为向量并存入向量数据库，以支持查询失败时的语义回退。文中仅说明第一个模型进行了与 $Cypher$ 生成有关的提示工程、领域适配和微调，未给出完整训练流程或目标函数。

推理时，用户提交自然语言问题 $q$。第一阶段由 $\mathrm{LLM}_{\mathrm{cypher}}$ 根据本体生成最多三个候选查询，去除重复和语法无效查询，并逐一在 $\mathcal{G}$ 上执行；第一个返回非空结果的查询产生证据集 $R$。若全部失败，系统将问题和图节点编码，按相似度取得前 $k$ 个候选锚点，再把原问题、锚点和本体交回查询模型重新生成查询；成功执行后得到 $R'$，否则返回空集。第二阶段把 $R$ 或 $R'$ 的节点、边、属性和多跳路径提供给第二个语言模型，该模型仅依据这些结构化证据合成答案，并向分析人员展示可检查的图关系和推理痕迹。

**复现信息**

知识图谱采用 $Neo4j$ 中的带标签属性图实现：节点表示网络安全实体，类型化边表示语义或运营关系，属性保存描述、严重性、$CVSS$ 指标及通信风险字段。节点嵌入使用 $all\text{-}MiniLM\text{-}L6\text{-}v2$，维度为 $384$；文中估计每个向量在 $32$ 位浮点存储下约占 $1.5\ \mathrm{KB}$，不含数据库和索引开销。长查询可按语义片段分解，片段以 $CONTAINS$ 过滤器参与查询；每个问题最多生成三个候选 $Cypher$ 查询，重复项和语法无效项会被丢弃。评估使用固定的 $BRIDG\text{-}ICS$ 图快照以保持训练与测试环境一致；图更新到评估环境之外时，会为新增或修改节点重新生成嵌入。所给章节未明确报告模型具体名称、微调数据规模、硬件、延迟设置、$k$ 的取值、图规模以及查询验证器的具体实现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- KG-RAG QA 数据集：从 BRIDG-ICS 知识图谱中选取 65 个真实世界 $CVE$，为其构造完整的 $CVE\rightarrow CWE\rightarrow CAPEC\rightarrow ATT\&CK$ 映射，并生成 450 个符合本体的问答样本。该数据集用于 Cypher-LLM 的参数高效微调，也覆盖实体关系、依赖推理、多跳遍历、攻击路径、缓解措施、IT–OT 关系和漏洞传播风险等威胁中心任务。样本通过改写问题和变换标识符来测试结构泛化，而非死记具体编号。
- CTIBench：公开的网络威胁情报基准。实验选取 CTI-RCM 2024、CTI-RCM 2021 和 CTI-ATE 三项任务；前两项根据 $CVE$ 描述识别对应的 $CWE$ 类别，并使用两个时间划分，后一项识别软件或恶意软件实体关联的 $MITRE\ ATT\&CK$ 技术。作者将原始提示改写为适合图检索的问题，用于评估从自然语言到结构化实体检索的正确性。
- BRIDG-ICS 知识图谱：作为符号检索和推理底座，而非独立的测试集。其本体、节点标签、关系类型和属性名称被注入 Cypher-LLM 提示词；生成的查询在该图上的 LPG 中进行语法检查、本体一致性检查和执行，以提供可追踪的实体、关系及多跳路径证据。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

预测实体与基准答案一致的样本比例；在本实验中主要反映自然语言问题能否被正确转换并通过图检索找到目标 $CWE$ 或 $ATT\&CK$ 技术。 （越高越好，因为它表示更多查询得到了正确的结构化实体。）

</div>
<div class="metric-item" markdown="1">

**F1-score**

Precision 与 Recall 的调和平均，用于综合衡量正确预测的可靠性和覆盖率；由于文中报告各配置的 Precision 均为 100%，差异主要来自 Recall 和未能解析的查询。 （越高越好，因为它要求正确性与覆盖率同时较高。）

</div>
<div class="metric-item" markdown="1">

**Hallucination Rate（HR）**

衡量生成答案中未被检索图证据支持的内容比例，用于检验 Answer-LLM 是否严格依据实体、关系和路径生成解释。 （越低越好，因为较低值表示较少出现脱离图证据的臆造内容；原文在所给片段中未报告具体 HR 数值。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Full GRICS 在 CTI-RCM 2024、CTI-RCM 2021 和 CTI-ATE 上的总体表现

<div class="result-value" markdown="1">

Full GRICS 在三项任务中均取得最高结果：CTI-RCM 2024 的 Accuracy 为 87.60%、F1 为 0.930；CTI-RCM 2021 的 Accuracy 为 90.40%、F1 为 0.949；CTI-ATE 的 Accuracy 为 77.15%、F1 为 0.871。作者同时报告其相对于已发表 Base LLM 在三项任务上均达到统计显著改进（$p<0.05$）。

</div>

这说明将本体约束的 Cypher 生成、知识图谱符号检索和嵌入回退结合起来，能够在漏洞分类和 ATT&CK 技术识别中更稳定地找到正确实体。CTI-ATE 仍明显更难，合理解释是其需要跨越软件、恶意软件、攻击模式、漏洞和技术之间的异质关系；该结果支持对多跳检索有效，但不能单独证明系统在所有真实工业场景中都可靠。

<div class="result-source" markdown="1">

来源：Section 6.2, Table 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Full GRICS achieves the highest performance on all three datasets, obtaining an accuracy of 87.60% and an F1 score of 0.930 on CTI-RCM 2024, an accuracy of 90.40% and an F1 score of 0.949 on CTI-RCM 2021, and an accuracy of 77.15% with an F1 score of 0.871 on CTI-ATE.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 不同配置在 CTI-RCM 2024 与 CTI-RCM 2021 上的比较

<div class="result-value" markdown="1">

在 CTI-RCM 2024 上，Accuracy 从 Base KG-RAG 的 62.80% 提升到 KG-RAG+FT 的 67.20%、KG-RAG+EF 的 85.70% 和 Full GRICS 的 87.60%；在 CTI-RCM 2021 上，Accuracy 分别为 66.50%、78.60%、88.20% 和 90.40%。两项任务中 Precision 均为 100%。

</div>

这些结果表明，单靠提示式 Cypher 和符号检索已经能完成一部分实体映射，但嵌入回退带来的提升大于单独微调，说明现实问题中查询失败或检索过窄是重要瓶颈；两者组合仍有小幅增益。100% Precision 不应理解为所有问题都答对，而是指已经产生有效预测的结果都对应正确实体，未解析或漏检的问题主要拖低 Accuracy 和 Recall。

<div class="result-source" markdown="1">

来源：Section 6.2, Table 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Full GRICS achieves the highest performance on all three datasets, obtaining an accuracy of 87.60% and an F1 score of 0.930 on CTI-RCM 2024, an accuracy of 90.40% and an F1 score of 0.949 on CTI-RCM 2021, and an accuracy of 77.15% with an F1 score of 0.871 on CTI-ATE.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### CTI-ATE 上的复杂关系推理

<div class="result-value" markdown="1">

CTI-ATE 的 Accuracy 从 Base KG-RAG 的 18.33% 提升至 KG-RAG+FT 的 64.72%、KG-RAG+EF 的 53.33% 和 Full GRICS 的 77.15%；对应 F1 分别为 0.309、0.786、0.695 和 0.871。

</div>

该任务最能区分组件对复杂关系检索的作用：Cypher 微调在没有回退时带来显著改善，而完整配置取得最高结果，说明更好的初始查询与失败后的恢复机制具有互补性。嵌入回退单独配置低于微调单独配置，表明语义锚点只能帮助恢复检索入口，不能替代高质量的本体查询生成；该结果仍不能证明每条多跳攻击路径都被完整恢复。

<div class="result-source" markdown="1">

来源：Section 6.2, Table 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The results show that GRICS performs strongly on the two vulnerability-to-weakness classification tasks, while the lower CTI-ATE performance reflects the greater relational complexity of ATT&CK technique identification across software, malware, attack patterns, vulnerabilities, and techniques.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评测依赖 BRIDG-ICS 知识图谱及其本体映射，且微调数据由 65 个 $CVE$ 生成 450 个样本；因此结果可能受图谱覆盖范围、映射完整性和改写样本分布限制，不能直接外推到未收录或本体不同的工业威胁情报。
- 所给实验片段没有提供运行时间、攻击成功率、每查询令牌数、幻觉率、查询违规率和模式一致性率的具体结果，也没有展示完整人工案例或跨图谱验证；因此关于交互式效率、低幻觉和可解释性的强度仍需依据完整论文或复现实验核查。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 已发表的 CTI-Benchmark LLM 基线：不使用知识图谱，代表纯提示式预测，用来估计图接地符号检索的独立贡献。
- Base KG-RAG：使用提示式 Cypher 生成和 BRIDG-ICS 上的符号检索，但不启用 Cypher 微调或嵌入回退，是最基本的图接地配置。
- KG-RAG+FT：在 Base KG-RAG 上加入 Cypher-LLM 的领域微调，用来测试查询生成质量和本体语义对齐的贡献。
- KG-RAG+EF：在 Base KG-RAG 上加入嵌入式回退，用来测试初始 Cypher 查询失败、过窄或无结果时的检索恢复能力。

**实验想回答的问题**

- 与不使用知识图谱的已发表基线及不同组件配置相比，$GRICS$ 能否提高漏洞到 $CWE$ 分类和软件或恶意软件到 $MITRE\ ATT\&CK$ 技术识别的准确性？
- Cypher 微调与嵌入回退机制是否分别改善查询生成、图检索覆盖率、复杂多跳推理和结果可解释性？

**实验实现**

评测统一使用相同的基准输入、提示词框架、推理设置和评价指标。Cypher-LLM 基于预训练的 Llama-3.1-8B Text2Cypher 模型，采用 Unsloth 和 LoRA 参数高效微调；训练使用 450 个 KG-RAG QA 样本，序列长度为 2048，实际批大小为 4。推理时，Cypher 提示词提供 BRIDG-ICS 本体、少样本示例和分析问题，并最多生成三个候选查询；候选按语法、本体一致性和图上可执行性顺序验证，选择首个能取得相关证据的查询。若符号检索失败，嵌入回退先寻找语义相关的图锚点，再交给 Cypher-LLM 重新生成仍须通过验证的本体合规查询。Answer-LLM 接收原问题和检索到的图证据，只负责将证据组织成人类可读的解释。基准分数主要评估 Cypher 生成和符号检索，因为基准答案是单一结构化实体，Answer-LLM 不改变该实体。文中还使用 McNemar 检验，以显著性水平 $\alpha=0.05$ 比较各配置与已发表 LLM 基线；运行时间、攻击成功率、每查询令牌数、查询违规率和模式一致性率被列为其他分析维度，但所给片段未提供其完整数值结果。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 已发表 CTI-Benchmark LLM 基线 versus Base KG-RAG | 作者将无知识图谱的已发表 LLM 基线与使用提示式 Cypher及 BRIDG-ICS 符号执行的 Base KG-RAG 进行比较，并报告 Base KG-RAG 在 CTI-RCM 2024、CTI-RCM 2021 和 CTI-ATE 上均显著优于 Base LLM（$p<0.05$）。 | 这是对“知识图谱接地是否有用”的外部对照。由于 Base KG-RAG 同时改变了回答机制和检索来源，结果支持图接地符号检索的总体价值，但不能把全部提升精确归因于某一个查询提示细节。 | Section 6.2, Statistical Significance; Section 6.2.1<br><span class="experiment-evidence">The results showed that Base KG-RAG significantly outperformed the Base LLM across CTI-RCM 2024, CTI-RCM 2021, and CTI-ATE (p<0.05), demonstrating the benefit of symbolic knowledge-graph retrieval.</span> |
| Base KG-RAG、KG-RAG+FT、KG-RAG+EF 与 Full GRICS 的逐步组件消融 | 在 CTI-ATE 上，Base KG-RAG、KG-RAG+FT、KG-RAG+EF 和 Full GRICS 的 Accuracy 分别为 18.33%、64.72%、53.33% 和 77.15%；在 CTI-RCM 2024 和 CTI-RCM 2021 上，Full GRICS 也分别达到 87.60% 和 90.40%。 | 该消融把微调和嵌入回退分别加入同一图检索框架：微调主要改善初始 Cypher 的语法有效性与语义对齐，回退主要处理初始查询无效、过窄或无结果的情况，组合后覆盖两类失败模式。由于图接地本身不能从可执行 KG-RAG 中直接删除，研究用外部无图 LLM 基线近似评估其贡献；因此这不是完全正交的因果消融。 | Section 6.2.1, Ablation Study; Table 4<br><span class="experiment-evidence">Full GRICS achieves the strongest performance across all three benchmark tasks, demonstrating that Cypher fine-tuning and embedding-based fallback address complementary limitations.</span> |

**定性案例**

- 原文未提供单个具体威胁事件的逐步定性案例；其可解释性分析以 Figure 4 的前 15 个 $CWE$ 类别热图和 Figure 5 的检索结果分布为代表，区分直接符号检索、嵌入回退后恢复和未解析查询。作者据此主张微调扩大语义覆盖并增加可直接追踪的图遍历，回退减少未解析结果；但所给片段未报告图中各类别或各结果分布的具体数值。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces an LLM-based neuro-symbolic framework for ontology-consistent multi-hop reasoning through executable knowledge-graph queries.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`d3b1ed9d6177891b0869fa035edc0319f3cf487a8e1990041c18f436bf45e575`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
