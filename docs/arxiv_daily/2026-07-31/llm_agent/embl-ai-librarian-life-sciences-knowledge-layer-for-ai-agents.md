---
title: "[论文解读] EMBL AI Librarian: Life-Sciences Knowledge Layer for AI Agents"
description: "[arXiv 2607.28229][LLM Agent] 本文研究如何在不自建稠密向量索引的前提下，把面向人类的 Europe PMC 文献搜索服务改造成面向 AI 智能体的生命科学知识层，使智能体能够用自然语言提问并直接获得紧凑、可引用的证据片段。"
arxiv_id: "2607.28229"
announcement_date: "2026-07-31"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.367180+00:00"
source_sha256: "29449d2f497299f5b598f5458eb8e83fd7ffc358f7f8d7c60b77396030cf0984"
tags:
  - "LLM Agent"
  - "生命科学文献检索"
  - "AI智能体"
  - "Europe PMC"
  - "检索增强生成"
  - "字段化查询"
  - "证据检索"
  - "大语言模型"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2607.28229</p>

# EMBL AI Librarian: Life-Sciences Knowledge Layer for AI Agents

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Sigillo, Luigi, Silvestri, Matteo, Tabaro, Francesco, Bhatnagar, Rajat, Mubashar, Syed Irtaza, Jeffryes, Matt, Nijjer, Daljit, Perera, Vittorio, Spjuth, Ola, Saez-Rodriguez, Julio, Harrison, Melissa, Petroni, Fabio</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.28229) · [PDF 下载](https://arxiv.org/pdf/2607.28229) · **关键词** 生命科学文献检索, AI智能体, Europe PMC, 检索增强生成, 字段化查询, 证据检索, 大语言模型<br>
**代码**: [https://github.com/petroni-lab/librarian](https://github.com/petroni-lab/librarian)

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

本文研究如何在不自建稠密向量索引的前提下，把面向人类的 Europe PMC 文献搜索服务改造成面向 AI 智能体的生命科学知识层，使智能体能够用自然语言提问并直接获得紧凑、可引用的证据片段。

**不用术语来说**：生命科学智能体需要依靠论文回答问题、核验主张或完成实验相关任务，但现有文献搜索工具通常要求它先把问题改写成关键词和复杂检索式，再从返回的整篇论文中自行寻找证据。生物实体往往还有多种名称，单次搜索容易漏掉相关文献；同时，逐篇阅读会迅速耗尽模型有限的上下文和计算预算。因此，真正缺少的不是更多论文，而是一个能把自然语言问题直接转化为少量可靠证据的中间层。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 EMBL AI Librarian：以单个大语言模型统筹检索规划和证据定位，在 Europe PMC 的实时搜索服务之上生成互补的关键词及字段化查询，并从检索到的论文中返回排序后的可引用证据，无需训练专用模型或维护自有向量索引。
- 提出一种可供不同 AI 智能体共享、且与底层大语言模型解耦的生命科学知识接口；论文通过文献综合、科学主张核验、开放式问答和生物学工作流四类任务检验这种知识层是否能改善下游表现。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

生命科学智能体正在承担文献综述、生物信息学工具编排、候选生物标志物筛选和假设生成等任务，这些任务都要求模型将回答或推理锚定在可核查的论文证据上。Europe PMC 是该领域的重要开放文献基础设施，原文称其收录约 1190 万篇全文、4070 万条 PubMed 摘要和 120 万条预印本，并支持按元数据、正文区段及基因、蛋白质、物种、化学物和疾病等实体标注进行检索；但其关键词语法、整篇文档输出和词法排序主要面向人类用户。论文因此研究一种面向智能体的“知识层”：在不另建全量向量索引的前提下，把自然语言问题转换为对 Europe PMC 实时搜索服务的多组互补查询，再从命中文献中提取少量、排序后的可引用证据片段。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**检索增强生成**

检索增强生成先从外部文献中找到相关材料，再让语言模型依据这些材料回答，从而降低仅依赖模型参数记忆所带来的事实错误。本文关注的核心不是最终文本生成器，而是为智能体提供可靠证据的检索知识层。

</div>
<div class="concept-item" markdown="1">

**稠密检索与词法检索**

稠密检索把问题和文段编码为向量并按向量距离寻找近邻；词法检索则依据关键词重合及其统计权重进行匹配，BM25 是常见方法。本文保留自然语言交互，但由大语言模型规划关键词及字段查询，并复用 Europe PMC 的实时词法搜索，而不是维护独立的稠密向量库。

</div>
<div class="concept-item" markdown="1">

**字段化查询与可引用证据**

字段化查询允许检索条件明确作用于基因、蛋白质、物种、疾病或正文区段等结构化字段，比把所有信息压入单一向量更容易控制和检查。可引用证据是带有来源元数据的相关原文片段，使下游智能体能够直接核查回答依据，而不必把整篇论文放入有限的上下文窗口。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是生命科学智能体以自然语言提出的问题，问题可能服务于跨论文综合、科学主张核验、开放式问答或实验流程任务。系统假设 Europe PMC 的实时索引及可访问论文内容能够作为外部知识源，并由一个可替换的大语言模型控制器理解问题、规划多组互补的关键词或字段化查询、筛选命中文献、将所选论文拆分为段落并按其对原问题的证据相关性评分；输出是一个紧凑、排序且附来源元数据的可引用证据片段集合，而非整篇论文或仅有文献列表。该设置还隐含两项现实约束：生物实体往往存在基因符号、蛋白质名称、疾病同义词和 MeSH 术语等别名，因此单次查询通常不足；智能体的上下文窗口与令牌预算有限，因此需要在检索层完成文献内证据定位。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Europe PMC**: 本文的底层生命科学文献搜索引擎与数据来源。EMBL AI Librarian 不复制或重建其索引，而是在其现有 API、丰富查询语法、正文区段和实体标注能力之上增加自然语言查询规划及段落级证据提取。
- **OpenScholar**: 代表基于稠密向量数据库的科学文献检索路线：论文指出其数据存储规模约为 744 GB，用以说明全量文献嵌入在索引和服务方面的基础设施成本。EMBL AI Librarian 试图保留自然语言输入与可引用文段输出的优点，同时避免维护自己的向量索引。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

AI 智能体正被用于生命科学文献综合、生物信息学工具编排、生物标志物筛选和假设生成，这些活动都要求其推理能够落到已发表证据上。与此同时，生命科学文献持续增长，而 Europe PMC 已包含大规模摘要、全文和预印本记录。现有接口却主要服务人类检索者：智能体必须掌握查询语法、处理基因或疾病等实体的别名、反复搜索，并阅读大量仅局部相关的全文。这使证据获取成为智能体工作流中的成本和可靠性瓶颈。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **Europe PMC 等字段化词法检索**：用户或智能体提交关键词以及针对标题、正文、方法、图表、基因、蛋白质、物种、化学物和疾病等字段的结构化条件，搜索引擎按词法相关性返回论文记录或全文。该方式能够利用数据库已有的显式元数据和专业标注，查询过程也较容易检查。
- **基于稠密向量数据库的文献检索**：系统预先将论文切分为段落，把每个段落编码为向量并建立近邻索引；收到自然语言问题后，再检索语义上最接近的段落。它比返回整篇论文更适合为智能体提供可引用材料，也不要求用户直接编写复杂关键词表达式。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 传统 Europe PMC 接口把查询规划和证据定位都留给每个下游智能体：词法查询难以自动覆盖生物实体的多种别名，通常需要多次互补搜索；返回结果又以整篇文献为主，相关信息可能只占很小一部分，导致遗漏证据或浪费有限的上下文窗口。
- 稠密检索虽然支持自然语言和段落级返回，但需要为整个文献库生成、更新并在线服务大规模嵌入，基础设施成本高；同时，向量表示会弱化数据库中原本明确的字段与实体标注，近邻匹配也不如字段化查询透明。论文还指出，随着大语言模型查询规划能力增强，稠密检索相对经过调优的词法检索所具有的优势正在缩小。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方案尚未同时满足四项需求：允许智能体以自然语言提问，自动形成覆盖别名和不同证据角度的互补查询，返回段落级且带来源的紧凑证据，并复用持续更新的权威实时文献基础设施而不另建昂贵索引。缺口因此不是新的通用搜索库，而是连接自然语言智能体与 Europe PMC 结构化检索能力的共享编排层。

</div>
<div markdown="1"><span>核心问题</span>

一个由单个大语言模型控制、直接调用 Europe PMC 实时字段化词法搜索并在所得全文中定位证据的知识层，能否在不训练专用模型和不维护稠密向量索引的情况下，为不同生命科学智能体提供足以改善多类下游任务的可引用证据？

</div>
<div markdown="1"><span>作者直觉</span>

Europe PMC 已经承担了文献收录、更新、字段索引和生命科学实体标注等最昂贵的基础工作，真正需要补上的，是对智能体友好的“翻译与筛选”环节。大语言模型适合把一个自然语言问题拆成若干互补检索意图，并把这些意图表达为可检查的关键词和字段条件；搜索引擎负责从最新文献库中高效召回，模型再只阅读候选论文、筛出与原问题直接相关的段落。这样把模型的语义规划能力与现有搜索基础设施的覆盖面、结构化信息和实时性结合起来，有望用较少上下文获得更集中且可追溯的证据。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

EMBL AI Librarian在Europe PMC之上增加面向AI智能体的生命科学知识层：输入是自然语言问题，输出不是整篇论文或普通搜索结果列表，而是一组能够直接支持回答、可追溯引用且较为紧凑的证据片段。端到端流程由单个、模型无关的大语言模型控制器统一编排；该控制器先规划彼此互补的子查询，调用实时Europe PMC搜索引擎检索文献，再阅读入选论文并定位相关证据。直观地说，系统把“设计检索式、反复搜索、通读论文和摘取证据”这些原本需要下游智能体自行完成的工作，封装成一次自然语言问答接口。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 接收自然语言问题

系统通过知识层接口接收问题，无需调用方掌握Europe PMC的字段、关键词组合或复杂查询语法。所给章节未说明是否还执行问题分类、实体识别或查询规范化。

<div class="method-step__io" markdown="1">

**输入**：生命科学智能体提交的自然语言问题。<br>
**输出**：供大语言模型控制器规划检索过程的用户问题。

</div>

**直观理解**：调用方只需说明自己想知道什么，不必先把问题翻译成数据库专用检索式。该接口将底层搜索复杂性与上层智能体隔离。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 规划互补子查询并实时检索

单个大语言模型控制器规划多个互补子查询，并将它们交给实时Europe PMC搜索引擎执行；系统复用Europe PMC经过整理的字段化生命科学检索基础设施。原文节选未给出子查询数量、查询生成提示词、候选合并方式及排序规则。

<div class="method-step__io" markdown="1">

**输入**：原始自然语言问题。<br>
**输出**：由一个或多个子查询召回的候选文献集合。

</div>

**直观理解**：复杂问题往往无法由一次关键词搜索覆盖，因此控制器从不同角度拆分并搜索。这里的大语言模型像检索员，Europe PMC则像持续更新且支持精细字段检索的生命科学目录。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 筛选论文并定位相关证据

控制器阅读选定论文，并在论文内容中定位与问题有关的证据。现有材料只明确说明系统会读取“selected papers”并寻找相关证据，未披露论文选择算法、全文获取范围、片段切分方式或相关性判定标准。

<div class="method-step__io" markdown="1">

**输入**：Europe PMC返回的候选文献以及原始问题。<br>
**输出**：与问题相关、来源于入选论文的候选证据片段。

</div>

**直观理解**：普通搜索通常把整篇论文交给智能体，而Librarian进一步完成“在哪一段能找到答案”的定位。这样可减少下游智能体读取大量无关文本的负担。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 返回紧凑且可引用的证据

知识层将相关内容组织为一组紧凑、可引用并能够支持回答的证据片段，返回给上层智能体。所给章节未明确报告片段去重、数量控制、引用元数据格式、答案生成方式或置信度估计方法。

<div class="method-step__io" markdown="1">

**输入**：已定位的候选证据片段。<br>
**输出**：面向下游智能体的可引用证据片段集合。

</div>

**直观理解**：最终产品是有出处的证据，而不是要求调用方自行阅读的论文清单。上层智能体可以据此回答问题、核验主张或执行后续生命科学任务。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用或原文未明确报告。所给方法章节节选把EMBL AI Librarian描述为由单个大语言模型控制器编排的检索与证据定位系统，没有给出专门训练该控制器的损失函数、监督数据、参数更新过程或强化学习目标，因此不能据此认定作者进行了额外模型训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 自然语言知识层接口**

该接口将自然语言问题映射到完整的文献检索与证据定位流程，并以紧凑、可引用的证据片段作为返回结果。它避免将Europe PMC的查询语法和整篇论文直接暴露给调用方。

> 直观理解：这一模块相当于统一服务台：智能体提交问题，系统负责完成后续检索工作并交付可用证据。它降低了不同智能体重复实现生命科学文献检索逻辑的成本。

**2. 单一且模型无关的大语言模型控制器**

一个大语言模型控制器统一编排子查询规划、实时检索以及入选论文中的证据定位。论文将其称为“model-agnostic”，表示架构原则上不绑定某个特定大语言模型；但所给材料未提供模型替换接口、提示词、上下文管理或工具调用协议。

> 直观理解：这里不是为每个阶段分别训练一个模型，而是由同一个控制器安排整个检索过程。模型无关设计意味着系统的工作流可以保留，同时替换负责决策的大语言模型。

**3. Europe PMC检索后端**

系统建立在Europe PMC之上，复用其经过整理的字段化生命科学搜索基础设施，并通过实时搜索引擎执行控制器生成的互补子查询。Europe PMC负责底层文献索引与检索，Librarian负责面向问题的规划和证据提取。

> 直观理解：该设计没有重新建设一个生命科学论文库，而是在成熟数据库上增加智能编排层。这样既利用现有索引和字段信息，也让返回结果更适合AI智能体直接使用。

**训练与推理**

现有材料仅支持描述推理阶段：调用方提交自然语言问题；控制器规划互补子查询；子查询由实时Europe PMC搜索引擎执行；控制器随后处理入选论文并定位相关证据；系统最终返回紧凑且可引用的证据片段。训练阶段、模型参数是否冻结、是否采用微调、检索失败后的重试机制、工具调用轮数以及停止条件均为原文未明确报告。

**复现信息**

公平解释该方法所必需的已知信息是：系统以Europe PMC作为实时文献检索后端，保留并利用其字段化生命科学搜索能力；整个流程由一个模型无关的大语言模型控制器编排；外部接口接收自然语言问题并返回证据片段，而非整篇论文。所给节选没有提供控制器所用具体模型、提示模板、子查询预算、候选文献规模、全文解析与片段化策略、排序或去重算法、上下文长度、运行成本和延迟，因此这些内容不能从当前材料中复现；作者声明代码公开于论文摘要所列GitHub仓库，但仍需结合完整论文与对应版本代码核验实现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ScholarQA-Bench：由博士级专家编写、需要综合多篇论文的宽泛问题。实验使用生物医学 Bio、神经科学 Neu，以及多学科 Multi 中归入 Bio 或 Neu 的子集，用于测试多文献综合和引文支撑能力；原文节选未给出各子集样本数。
- ProClaim-Eval：共 419 条声明，来自 SIGNOR 的蛋白质—蛋白质相互作用和 ConnectomeDB 的配体—受体相互作用；每条声明均有专家整理的 SUPPORT、REFUTE 或 UNCERTAIN 共识标签，用于测试代理能否从多篇文献中恢复科学共识。
- 开放式 LitQA2 与 LAB-Bench：开放式 LitQA2 保留 Europe PMC 中支持论文具有全文的 91 道困难事实题，答案不能仅由摘要得到；LAB-Bench 选用 DbQA、ProtocolQA、SeqQA 和 Cloning Scenarios 四类任务，分别考查数据库信息、实验方案排错、序列操作和分子克隆。前者主要隔离全文检索质量，后者检验知识层能否迁移到实际生命科学能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Citation F1**

引文精确率与召回率的调和平均。召回率检查应当有文献支撑的陈述是否得到适当引用，精确率检查已引用来源是否与对应陈述相关且确有必要。 （越高越好，因为它同时惩罚缺少关键引用和添加无关或不必要引用。）

</div>
<div class="metric-item" markdown="1">

**Agreement**

模型对科学声明给出的 SUPPORT、REFUTE 或 UNCERTAIN 裁决与专家共识标签一致的比例。 （越高越好，因为更高值表示模型更能依据文献恢复专家整理的共识；它不等同于证明专家标签本身绝对正确。）

</div>
<div class="metric-item" markdown="1">

**Coverage、Precision 与 Accuracy**

Coverage 是未弃答问题的比例；Precision 是已作答问题中正确答案的比例；Accuracy 是全部问题中答对的比例，弃答按错误计。LitQA2 的正确性由 GPT-4o 判断答案是否明确包含或无歧义地改写标准答案。 （三者通常越高越好，但需联合解释：Coverage 上升可能伴随猜测增多，Precision 上升也可能只是更频繁弃答；Accuracy 综合反映最终答对比例。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### ScholarQA-Bench：GLM-5 Synthesis Agent 使用 LIBRARIAN，而非 OSDS 上的 BM25

<div class="result-value" markdown="1">

在 Bio 和 Neu 上，LIBRARIAN 相对同一综合代理的 BM25 检索分别再提高 Citation F1 6.8 点和 10.9 点；在 Multi 上，作者报告 LLM 综合质量分数提高 20%。此外，使用 OSDS 的 GLM-5 代理已分别比 OpenScholar-70B 高 11.1 点和 5.4 点，说明模型规模与检索质量都可能贡献收益。

</div>

固定综合代理后，LIBRARIAN 相对 BM25 的提升较能支持“检索规划和证据定位更好”的解释；而 GLM-5 与 OpenScholar-70B 的比较同时改变模型规模，不能把差异完全归因于知识层。Multi 上仅扩大模型并未明显改善 LLM 评分，而换用 LIBRARIAN 后改善，进一步表明证据质量可能是关键因素，但 LLM-as-a-judge 仍可能带来评审偏差。

<div class="result-source" markdown="1">

来源：第 3.1 节 Findings，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The Synthesis Agent becomes even stronger when equipped with LIBRARIAN, with a further +6.8 on Bio and +10.9 on Neu over the BM25 index on OSDS.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### ProClaim-Eval：将原始 PubMed 与 Semantic Scholar 检索替换为 LIBRARIAN

<div class="result-value" markdown="1">

简单 Verifier Agent 的平均 Agreement 从 0.51 提高到 0.66，即增加 15 个百分点；完整 ProClaim 流水线从 0.75 提高到 0.80，即增加 5 个百分点。使用 LIBRARIAN 的 ProClaim 在 SIGNOR 和 ConnectomeDB 上分别为 0.78 和 0.81。

</div>

同一下游裁决代理换用 LIBRARIAN 后取得更高专家共识一致率，表明更直接、相关的证据能减少后续事实抽取与判断负担。简单单提示代理达到 0.66 也说明部分复杂工作已由检索层完成；但 LIBRARIAN 版本删除了原 ProClaim 的影响因子、引用量和全文自然语言推断特征，因此这不是只改一个接口、其他步骤完全不变的纯粹替换实验。

<div class="result-source" markdown="1">

来源：第 3.2 节 Findings，Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The same holds for ProClaim itself: switching its retriever to the LIBRARIAN knowledge layer yields +5 average agreement points (0.75→0.80), further supporting the hypothesis that LIBRARIAN provides better access to the underlying knowledge.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 开放式 LitQA2：固定 GPT-5.4 QA Agent，比较 Web-Search 与 LIBRARIAN

<div class="result-value" markdown="1">

Web-Search 的 Coverage、Precision 和 Accuracy 分别为 92.3、76.2 和 70.3；LIBRARIAN 分别达到 95.6、82.6 和 78.9，即 Precision 增加 6.4 点、Accuracy 增加 8.6 点，Coverage 增加 3.3 点。无检索条件虽有 100 Coverage，但 Precision 与 Accuracy 均仅为 17.6。

</div>

因为三种主要条件共享 GPT-5.4，结果较清楚地隔离了证据来源的作用：领域文献检索不仅让代理回答更多题，还让已作答答案更可靠。无检索时始终作答却大量出错，说明高 Coverage 本身不代表能力强。不过正确性由 GPT-4o 自动判定而非人工逐题复核，且仅评测 91 道具有 Europe PMC 全文的题目，外推范围有限。

<div class="result-source" markdown="1">

来源：第 3.3 节 Findings，Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Notably, replacing generic web search with LIBRARIAN improves both axes: precision rises by +6.4 points (to 82.6) and accuracy by +8.6 (to 78.9), while coverage also increases (92.3→95.6).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验没有报告 LIBRARIAN 内部组件的逐项消融，因此无法判断 $N=7$ 个子查询、每个子查询最多 $P=50$ 篇文章、全文段落筛选至 $k=16$ 段，以及最终证据定位分别贡献多少；现有对照主要验证整个知识层，而非其具体设计。
- 若干比较存在混杂或覆盖范围限制：ScholarQA-Bench 的部分基线使用约 70B 模型而综合代理使用约 700B 的 GLM-5；LitQA2 只有 91 道具备 Europe PMC 全文的问题且由 GPT-4o 自动判分；LAB-Bench 的 LIBRARIAN 结果来自约 80% 公开子集，而基线和人类结果来自完整数据集。此外，FigQA、TableQA 和 SuppQA 因系统尚不支持图、表及补充材料而被排除。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- OpenScholar 系列：在 ScholarQA-Bench 中与既有最佳代理比较，在 ProClaim-Eval 和 LitQA2 中作为外部参考。它代表依赖 Semantic Scholar 或 OpenScholar Data Store 的已发表学术检索代理，但部分比较同时改变了模型规模，因此不能全部视为纯检索器对照。
- OSDS 上的 BM25：与 LIBRARIAN 驱动的同一 GLM-5 Synthesis Agent 比较。BM25 是传统词项匹配检索器；固定生成代理后，该比较主要测试自然语言规划、全文阅读和证据定位是否优于关键词检索。
- ProClaim 原始检索器与简单 Verifier Agent：原始 ProClaim 使用 PubMed 和 Semantic Scholar，并包含检索、全文事实抽取和充分性判断循环；单提示 Verifier 则直接把证据映射为裁决。二者分别测试 LIBRARIAN 能否改善成熟多阶段流水线，以及高质量证据能否让简单下游代理也取得较强结果。
- 无检索与 Web-Search：在开放式 LitQA2 中固定 GPT-5.4，仅改变证据来源为参数知识、通用网页搜索或 LIBRARIAN。这是判断领域文献知识层是否优于不接地生成和通用搜索的最直接对照。

**实验想回答的问题**

- 在不同下游代理与任务中，将原有检索器或通用网页搜索替换为面向生命科学文献的 LIBRARIAN，是否能稳定提高引文支撑、科学共识判断和事实问答的正确性？
- 性能变化究竟来自更强的生成模型，还是来自检索层提供了更相关、可直接用于判断的全文证据；这种作用在文献驱动任务与数据库直查、序列操作等任务之间是否不同？

**实验实现**

LIBRARIAN 统一使用自托管 GLM-5，在 NVIDIA DGX B200 上通过 vLLM 服务；每次检索规划 $N=7$ 个子查询，每个子查询最多取回 $P=50$ 篇文章，对有全文的文章选取 $k=16$ 个段落进入后续证据阶段。ScholarQA-Bench 的综合代理由 GLM-5 单提示驱动；ProClaim-Eval 的各代理统一使用 Claude Sonnet 4.6；开放式 LitQA2 使用 GPT-5.4 作答、GPT-4o 判分。LAB-Bench 比较 GPT-4o 和 GPT-5.4 在无外部证据与加入 LIBRARIAN 两种条件下的表现，并列出 Claude 3.5 Sonnet 和人类专家作为参考。需要注意，LAB-Bench 的基线与人类结果来自完整数据集，而 LIBRARIAN 结果只来自约 80% 的公开子集，不能视为完全同样本的严格配对比较。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 开放式 LitQA2 的证据来源消融：Parametric、Web-Search 与 LIBRARIAN | 固定 GPT-5.4 后，无检索的 Accuracy 为 17.6，Web-Search 为 70.3，LIBRARIAN 为 78.9；对应 Precision 为 17.6、76.2 和 82.6。 | 该对照先隔离“是否检索”的作用，再隔离“通用搜索还是生命科学知识层”的作用。大幅从 17.6 升至 70.3 说明接地证据是主要增益来源，进一步升至 78.9 则支持领域专用证据筛选优于一般网页结果；它没有单独拆分 LIBRARIAN 内部的子查询规划、全文段落筛选和证据定位各自贡献。 | Table 3，列依次为 Cov、Prec、Acc<br><span class="experiment-evidence">QA Agent Parametric 100 17.6 17.6; QA Agent Web-Search 92.3 76.2 70.3; QA Agent LIBRARIAN 95.6 82.6 78.9.</span> |
| LAB-Bench 按模型强弱和任务类型比较 Base 与加入 LIBRARIAN | GPT-4o 的宏平均 Precision 从 49.0 升到 54.0，但 Coverage 从 70.2 降到 64.8，Accuracy 基本不变，为 35.2 到 35.3；GPT-5.4 的宏平均 Coverage 从 85.9 升到 92.7，Precision 保持 58.3，Accuracy 从 50.5 升到 54.6。GPT-5.4 的 SeqQA Accuracy 从 52.5 升到 63.8，而 DbQA 从 37.5 降到 36.2。 | 这一比较表明相同知识层会通过不同机制帮助不同能力的模型：较弱模型主要学会在证据不足时弃答，较强模型则利用新增证据扩大可正确回答的范围。SeqQA 与 DbQA 的反差还隔离出任务适配性：文献证据对序列相关问题有帮助，但对直接数据库查询可能增加噪声。由于 LIBRARIAN 条件只使用公开子集，而基线来自完整 LAB-Bench，该结果应视为支持性分析而非严格同样本消融。 | Table 4，Macro-avg 行<br><span class="experiment-evidence">Macro-avg Cov 88.0 56.7 70.2 64.8 (−5.4) 85.9 92.7 (+6.8); Prec 83.0 59.6 49.0 54.0 (+5.0) 58.3 58.3 (+0); Acc 73.2 35.1 35.2 35.3 (+0.1) 50.5 54.6 (+4.2).</span> |

**定性案例**

- SeqQA 是最清晰的任务级实例：GPT-5.4 加入 LIBRARIAN 后 Coverage 从 85.0 提高到 98.8，Precision 从 61.8 提高到 64.6，因而 Accuracy 从 52.5 提高到 63.8。作者据此解释，基础模型原先会因缺少证据而弃答，LIBRARIAN 补足证据后使其能够回答；这是按数据类别汇总的定量案例，而非展示具体问题与证据链的人工质性案例。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：构建由 LLM 规划检索子查询、阅读论文并定位证据的生命科学知识检索 Agent 层。; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`29449d2f497299f5b598f5458eb8e83fd7ffc358f7f8d7c60b77396030cf0984`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
