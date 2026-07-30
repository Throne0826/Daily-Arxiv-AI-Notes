---
title: "[论文解读] SimpleWikiSearch: A Clean Offline Wikipedia Environment for Agentic Search"
description: "[arXiv 2607.26070][LLM Agent] 本文不提出新的智能体算法，而是构建一个将维基百科语料、检索服务、工具接口与评测协议完整固定并公开的离线环境，使基于大语言模型的智能体搜索结果更容易复现和公平比较。"
arxiv_id: "2607.26070"
announcement_date: "2026-07-30"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T07:32:04.945284+00:00"
source_sha256: "af2c646abaee88d4df26b69ec79ec51bd3988c1bef5cea4895de9f957f11d972"
tags:
  - "LLM Agent"
  - "LLM 评测"
  - "LLM 其他"
  - "智能体搜索"
  - "开放域问答"
  - "离线维基百科"
  - "可复现评测"
  - "文本分块"
  - "关键词检索"
  - "稠密检索"
  - "工具调用"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2607.26070</p>

# SimpleWikiSearch: A Clean Offline Wikipedia Environment for Agentic Search

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Guanming Xiong, Penghui Zhang</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26070v1) · [PDF 下载](https://arxiv.org/pdf/2607.26070v1) · **关键词** 智能体搜索, 开放域问答, 离线维基百科, 可复现评测, 文本分块, 关键词检索, 稠密检索, 工具调用  
**代码**: [https://github.com/JimXiongGM/simple_wiki_search](https://github.com/JimXiongGM/simple_wiki_search)  

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

本文不提出新的智能体算法，而是构建一个将维基百科语料、检索服务、工具接口与评测协议完整固定并公开的离线环境，使基于大语言模型的智能体搜索结果更容易复现和公平比较。

**不用术语来说**：评测一个会搜索维基百科并回答问题的智能体时，最终得分并不只由大语言模型决定：使用哪个版本的维基百科、网页如何清洗和切分、搜索结果如何返回、上下文在哪里截断，以及答案如何提交，都会影响结果。以往论文常省略这些设置，因此即使使用相同模型和数据集，也可能无法重现分数，更难判断性能差异究竟来自模型还是搜索环境。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者规定并实现了一个端到端的离线维基百科智能体搜索环境，明确覆盖语料快照与清洗、按章节切块、关键词和稠密检索索引、工具定义、观测格式、智能体交互循环及评测协议。
- 作者配套提供六个问答数据集上的基线评测设计与可复现分析资产，包括开源模型的完整测试集和随机300题结果、商业闭源模型的随机300题结果，以及推理轨迹、工具观测、预测、评测字段和统计脚本。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于开放域问答、信息检索与大语言模型智能体评测的交叉领域。典型系统让大语言模型围绕用户问题反复调用搜索工具、阅读返回内容并提交答案；因此，最终得分不仅取决于模型本身，也受维基百科版本、页面清洗方式、文本切分粒度、检索索引、工具接口、观察内容格式及答案提交规则影响。本文把这些通常被当作外围实现细节的因素视为需要控制和公开的实验环境，目标是在固定的离线英文维基百科上建立可运行、可复现的智能体搜索基准，而不是提出新的智能体算法。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**智能体搜索（agentic search）**

指大语言模型不直接一次性回答问题，而是根据当前信息决定是否调用搜索、打开页面等工具，并经过多轮交互后提交答案。模型的推理策略与工具环境共同决定最终表现。

</div>
<div class="conceptitem" markdown="1">

**检索单元与文本分块（retrieval unit / chunking）**

检索系统通常不直接搜索整篇文章，而是先把文章切成可建立索引的文本块，再返回与查询最相关的块。块过短可能丢失章节或文档级上下文，块过长则可能包含更多无关信息并增加模型阅读成本。

</div>
<div class="conceptitem" markdown="1">

**关键词检索与稠密检索（keyword / dense retrieval）**

关键词检索主要依据查询与文档中的词项匹配，稠密检索则把查询和文本编码成向量，并按语义相似度查找内容。SimpleWikiSearch同时构建两类索引，使检索后端成为明确且可复现的环境组成部分。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是来自开放域问答数据集的自然语言问题，以及由指定英文维基百科快照经过清洗和按章节切分后形成的离线语料库。大语言模型智能体在统一协议下调用三个工具：用 search 检索候选内容，用 open_url 打开对应页面或结果，用 submit_answer 提交最终答案；系统输出答案以及可保存的消息轨迹、工具观察和评测字段。该设置假定智能体获取事实信息的主要外部渠道是受控的离线维基百科环境，并通过固定语料、索引、工具模式、观察格式和评测协议，减少不同实验中外围配置差异造成的不可比性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **KILT**: KILT为多种知识密集型任务提供共享知识源，使用2019年8月1日的英文维基百科快照，包含590万篇文章。本文将其作为广泛复用的维基百科评测设置示例，同时指出仅说明采用KILT式知识源仍不足以完整规定面向工具智能体的清洗、分块、观察和交互协议。
- **DPR**: DPR使用2018年12月20日英文维基百科转储，移除表格、信息框、列表和消歧义页等半结构化内容，并把文章切成互不重叠的100词段落，形成21,015,324个段落。本文借此说明传统短段落构造是为段落检索器和短上下文阅读器设计的，并非现代大语言模型智能体的中性默认选择。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

开放域问答和智能体搜索通常依据最终答案分数比较系统，但搜索环境很少被当作需要控制的实验变量。语料时间点、文档预处理、检索粒度、索引后端和工具交互规则均会改变智能体能看到的证据及其推理过程；若这些条件没有明确记录和可执行实现，研究者便难以复现实验，也无法把性能差异可靠地归因于语言模型或智能体设计。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **KILT/DPR式离线维基百科 passage 检索环境**：这类设置先固定一个英文维基百科快照，移除表格、信息框、列表等半结构化内容，再把文章切成互不重叠的约100词短段落，以段落作为索引和检索单位。KILT使用2019年8月1日快照并包含约590万篇文章；DPR使用2018年12月20日快照，其语料包含21,015,324个段落。
- **既有基于大语言模型的维基百科搜索智能体**：智能体通过搜索或打开页面等工具迭代获取维基百科证据，再由语言模型综合观察结果并提交答案；相关工作通常重点报告模型、智能体策略和最终答案分数，而将底层维基百科数据库及工具运行细节视为附属配置。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 传统100词短段落是为段落检索器和短上下文阅读器设计的，并非现代工具型智能体的中性默认值：短块可能因截断而语义不完整，也可能隐藏跨段落的文档级信息，迫使检索器在超大语料中寻找孤立的证据片段。
- 既有智能体搜索研究常未说明维基百科快照、页面清洗与切分方式、结果格式、观测截断规则，以及单步能否调用多个工具。由于这些因素会同时改变检索和推理行为，仅比较最终得分可能混入环境差异，导致基线难以复现且跨论文比较失真。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一个面向现代大语言模型工具调用智能体、可离线运行且端到端充分规定的维基百科参考环境；该环境需要把知识快照、语料构建、检索后端、工具契约、观测呈现、答案提交和评测记录统一为可执行协议，而不是只给出一个模糊的“可搜索维基百科”能力。

</div>
<div markdown="1"><span>核心问题</span>

在不提出新智能体算法的前提下，能否通过固定并公开离线维基百科搜索的全部关键环境变量，建立一个可运行的参考基线，使不同语言模型和智能体系统的问答结果能够被复现、审计并在相同条件下比较？

</div>
<div markdown="1"><span>作者直觉</span>

把搜索环境视为实验装置而非隐藏实现细节，可以减少比较中的混杂变量：所有系统面对同一份语料、相同切块和索引，并遵守一致的搜索、打开页面与提交答案规则后，结果差异就更可能反映模型或智能体本身。保存完整交互轨迹和工具观测还使研究者能够定位错误究竟发生在检索、证据呈现、推理还是答案提交阶段。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SimpleWikiSearch不是新的智能体算法，而是一套可复现的离线维基百科搜索环境。其端到端流程是：从固定版本的英文维基百科转储中清洗文章，按语义结构和分词后长度切块，为同一批文本块建立关键词索引与稠密向量索引，再向大语言模型仅暴露 search、open_url 和 submit_answer 三个工具；模型通过多轮检索、阅读和答案提交完成问答。环境固定了语料快照、文本预处理、切块、索引、URL、观察格式与终止规则，从而减少不同实验因底层搜索设施不一致而产生的混杂因素。
直观地说，该方法把“让模型上网查资料”改造成一个版本锁定、接口统一的离线图书馆：所有模型面对同一批书、同一种目录和相同的借阅规则，因此所得差异更能反映模型的检索与推理能力，而不是搜索引擎或网页版本的差异。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 固定并清洗维基百科语料

将 wikitext 转换为清洗后的纯文本表示，保留轻量 Markdown 形式的章节标题和可用表格结构，同时移除显式链接标记；发布索引覆盖 7,189,602 篇文章。

<div class="method-step__io" markdown="1">

**输入**：官方英文维基百科转储 enwiki-20260601，其中包含原始 wikitext、页面结构、链接及表格等内容。  
**输出**：具有稳定页面标识、标题和章节结构的离线英文维基百科文本集合。

</div>

**直观理解**：这一步相当于把固定日期的百科全书排版成统一、易读的版本。它既避免实时网页随后变化，也防止原始维基标记干扰模型阅读。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按结构和 token 长度构造文本块

按分词后的 token 数而非固定词数切分，并尽量合并章节至 1536 token 的目标长度，允许 20% 浮动且保留句子边界；最终生成 10,837,506 个文本块。每块保存页面 id、标题、块 id、内部块序号、总块数和正文。

<div class="method-step__io" markdown="1">

**输入**：清洗后的文章、文章章节边界，以及 Qwen3-Embedding-0.6B 分词器。  
**输出**：统一块标识空间中的结构化长文本块，以及形如 /wiki/<pageid>#chunk-N 的稳定离线 URL。

</div>

**直观理解**：它不像传统的固定 100 词短段落那样机械截断，而是尽量把同一章节和完整句子放在一起。这样智能体一次看到的上下文更完整，同时每段内容仍能被精确定位和打开。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立关键词与稠密向量检索

使用 Tantivy 为块正文和标题建立关键词索引；同时用 Qwen3-Embedding-0.6B 将每块编码成 1024 维向量，并以 fp16 形式存入 FAISS HNSW 索引。向量检索先返回块 id，再由 Tantivy 块存储解析对应标题和正文；默认采用倒数排名融合 RRF 合并关键词与向量候选。

<div class="method-step__io" markdown="1">

**输入**：全部文本块、标题和共享块 id。  
**输出**：支持 rrf、keywords 和 vector 三种模式的离线检索后端，返回排序后的标题、块 URL 和文本摘要。

</div>

**直观理解**：关键词检索擅长找完全相同的人名或术语，向量检索擅长找表达不同但意思相近的内容；RRF 把两份排名综合起来。两个索引共用块 id，可避免向量命中与实际展示文本错位。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 通过最小工具接口执行智能体搜索

模型可调用 search 发起查询并选择检索模式、用 open_url 打开某个块或整篇文章，最后调用 submit_answer 提交短字符串或题目要求的一张 Markdown 表格。search 返回排序命中的标题、可打开 URL 和摘要，而 open_url 根据有无 #chunk-N 分别返回指定块或全文。

<div class="method-step__io" markdown="1">

**输入**：用户问题、对话历史、三项 OpenAI 风格函数工具的 JSON schema，以及离线检索后端。  
**输出**：由工具观察不断扩展的对话轨迹，以及显式终止该轮任务的最终答案。

</div>

**直观理解**：模型只能做三件事：查目录、翻开资料、交答案。有限且明确的工具减少了不同智能体框架在接口能力上的隐性差别。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

这篇论文不以中心数学公式展开，或全文中未提取到可靠的关键公式。

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该论文贡献的是固定语料、检索后端、工具接口和运行协议，不训练新的智能体模型，也未给出需要优化的新损失函数；Qwen3-Embedding-0.6B 仅作为既有分词器和文本编码器使用，基线大语言模型通过兼容 OpenAI 的服务执行推理。原文在所给方法章节中没有提供 RRF 的具体数学公式，因此不应补写未报告的融合参数或目标函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 共享标识的双路检索栈**

Tantivy 同时承担关键词搜索、标题查找、URL 解析和文本存储；FAISS HNSW 保存由 Qwen3-Embedding-0.6B 生成的 1024 维 fp16 向量，并通过侧表将向量行号映射到共享块 id。默认 RRF 融合关键词与向量排名，也保留单路模式以进行受控比较。

> 直观理解：双路检索让系统同时利用字面匹配和语义相似性，而共享 id 保证两个检索器谈论的是同一段百科文本。保留单路开关还可以判断性能究竟来自关键词、语义检索还是二者融合。

**2. 离线稳定的文本与 URL 层**

每个文本块绑定 page id、chunk id 和块位置；外部显示使用 en.wikipedia.org 主机以提高可读性，但实际由离线索引解析。带 #chunk-N 的 URL 打开指定块，不带该后缀的页面 URL打开全文，其中内部块序号从零计数，暴露 URL 中的 N 从一计数。

> 直观理解：URL 看起来像普通维基百科链接，但不会访问实时网站，因此同一链接在不同运行中仍指向同一份内容。块级与全文级打开方式兼顾快速定位和补充上下文。

**3. 三工具智能体契约**

search 接收 query，并可设置 top_k、only_title 及 rrf、keywords、vector 三种 method；open_url 接收 URL；submit_answer 只接收最终答案并立即终止 episode。所有输入、输出和终止方式均以明确的函数 schema 传给模型。

> 直观理解：工具契约把智能体能够采取的行动压缩为固定菜单，避免某些实验额外提供浏览器、引用工具或特殊答案解析器。这样评测主要考察模型如何规划查询、选择证据和形成答案。

**训练与推理**

语料准备阶段是一次性的离线构建过程：下载 enwiki-20260601，清洗 wikitext，按章节、句界和 1536-token 目标长度构造文本块，随后建立 Tantivy 关键词索引，并为所有块计算 Qwen3-Embedding-0.6B 向量以建立 FAISS HNSW 索引。该过程不涉及对问答模型的微调。
推理时，运行器把问题、历史消息和三项工具 schema 发送给 OpenAI 兼容的聊天补全服务。模型可先用 search 查询；系统依据指定 method 执行关键词搜索、向量搜索或默认 RRF 融合并返回标题、URL 与摘要；模型再用 open_url 阅读目标块或全文，并可根据证据继续改写查询。模型最终必须调用 submit_answer，提交短答案或题目要求的单张 Markdown 表格；运行器随后结束 episode。全过程受 20 个模型轮次及每个 assistant 步骤最多五次工具调用的统一限制。

**复现信息**

公平复现所需的关键配置包括：语料快照为 enwiki-20260601；索引覆盖 7,189,602 篇文章和 10,837,506 个文本块；切块使用 Qwen3-Embedding-0.6B 分词器，以 1536 token 为目标、20% 为容差，并保持句子边界。关键词后端为 Tantivy；稠密编码器为 Qwen3-Embedding-0.6B，输出 1024 维向量；向量后端为 FAISS HNSW，每块保存一个 fp16 向量。默认检索模式为 RRF，keywords 与 vector 模式需继续暴露以支持消融或受控比较。
工具观察必须保持一致：search 返回排序后的标题、离线可打开 URL 和摘要；open_url 对块 URL 返回带标题及位置的指定块，对无块后缀的页面 URL 返回全文；submit_answer 仅接受最终答案且无解释。运行预算固定为最多 20 轮，每个 assistant 步骤最多五个工具调用；若该步无工具调用，运行器追加继续检索或正式提交答案的提醒。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- MuSiQue：开发集，共 2,417 个样本，问题平均 18.1 个词，28.1% 的样本提供至少一个答案别名。它主要检验需要组合多条证据的多跳问答能力，也是分析高交互成本与预算耗尽问题的代表性困难数据集。
- FRAMES：使用全部 824 个样本，问题平均 27.6 个词，不提供答案别名。它用于检验较长问题下的多步搜索与推理，并可观察词面 F1 在缺少别名时是否低估语义正确但表述不同的答案。
- HotpotQA：使用 dev-fullwiki 划分，共 7,405 个样本，问题平均 15.7 个词，不提供答案别名。它用于测试全 Wikipedia 环境中的多跳检索，并构成模型规模增大后并非所有数据集都提升的反例。实验还评测了 2WikiMultiHopQA、PopQA 和 Bamboogle，但受字段数量限制不逐项展开。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**Token-level F1**

对预测答案与主答案及其别名分别做开放域问答的标准规范化，包括转为小写、去除标点和冠词，再计算词元级精确率与召回率的调和平均，并取所有可接受答案中的最大值。它主要衡量预测与标准答案的词面重合程度。 （越高越好，因为更高表示预测包含更多正确答案词元且无关词元更少；但正确的改写或较长回答可能因词面差异而得分偏低。）

</div>
<div class="metricitem" markdown="1">

**LLM-judged accuracy**

由 gpt-5.4-mini-2026-03-17 按固定二元提示判断预测是否在事实意义上正确，允许释义、日期或姓名变体，以及嵌入较长文本中的正确答案。 （越高越好，因为它表示被判定为事实正确的样本比例更大；但该指标依赖特定裁判模型及提示词，不能视为完全客观的人工准确率。）

</div>
<div class="metricitem" markdown="1">

**交互轨迹统计**

包括每题平均模型轮数、search 调用数、open 调用数、成功 submit 比例、提示与生成的总令牌数，以及墙钟运行时间。它不直接衡量答案正确性，而是揭示智能体如何使用环境及其资源成本。 （没有统一的单调方向：在正确率相当时，轮数、调用数、令牌数和时间通常越低越高效，成功提交率越高越好；更多交互也可能是解决困难多跳问题所必需的。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 完整测试集上的 Qwen3.5-4B 与 Qwen3.5-9B 最终回答比较

<div class="result-value" markdown="1">

按作者对表 3 的总结，Qwen3.5-9B 在多数数据集上的 LLM 裁判准确率高于 Qwen3.5-4B，增益在 MuSiQue、FRAMES 和 Bamboogle 上最明显；HotpotQA 是例外，9B 略低。由于给定章节未包含表 3 的具体分数，不能据此量化提升幅度。

</div>

这说明在同一检索环境和工具协议下，较大的开源模型通常更能完成搜索与多步推理，但参数规模增加并不保证每个数据集都改善。该结果支持的是环境内的经验比较，不证明 9B 模型在其他语料快照、检索后端、提示词或随机种子下必然更好。

<div class="result-source" markdown="1">

来源：第 4 节 Results，对表 3 的文字总结

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Under the LLM-judged metric, the open-source 9B model improves over the 4B model on most datasets, with the largest gains on MuSiQue, FRAMES, and Bamboogle; HotpotQA is an exception, where 9B is slightly lower.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 困难多跳数据集与较简单数据集的交互轨迹比较

<div class="result-value" markdown="1">

作者报告，MuSiQue 和 FRAMES 所需的交互轮数与搜索调用数大约是 2Wiki 或 PopQA 的两倍，成功提交率降至 66%—73%。这表明不少失败并非明确提交了错误答案，而是智能体在完成提交前触及 20 轮上限。

</div>

最终准确率无法区分“检索到错误证据”“推理失败”和“尚未完成就耗尽预算”。轨迹统计显示，困难任务同时要求更长的搜索链并更容易超时，因此改进模型推理、检索质量、工具策略或交互预算都可能提升结果。不过，这个观察不能单独判断增加轮数是否最有效，因为更多轮数也会增加令牌和时间成本。

<div class="result-source" markdown="1">

来源：第 5 节 Analysis，对表 5 和表 6 的综合分析

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Harder multi-hop datasets such as MuSiQue and FRAMES require roughly twice as many rounds and search calls as 2Wiki or PopQA, and their successful submission rates drop into the 66–73% range, indicating that many episodes end by hitting the round budget rather than by a successful answer submission.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### FRAMES 完整测试集上两种开源模型的工具使用与成本

<div class="result-value" markdown="1">

在 FRAMES 的 824 个样本上，Qwen3.5-4B 平均运行 11.68 轮、调用 search 9.46 次、open 1.50 次，成功提交率为 66.26%，每题使用 114,771 个总令牌并耗时 39.8 秒；Qwen3.5-9B 相应为 11.29 轮、8.89 次 search、1.43 次 open、71.00% 成功提交率、119,330 个令牌和 65.6 秒。

</div>

较大的 9B 模型以略少的轮数和工具调用获得更高的成功提交率，但单题令牌数略增，墙钟时间也明显更长。这揭示了模型容量、交互效率和推理成本之间的权衡；成功提交率提高只表示更多回合按协议提交了答案，并不等同于这些答案全部正确。

<div class="result-source" markdown="1">

来源：表 5（Qwen3.5-4B）与表 6（Qwen3.5-9B）的 FRAMES 行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">FRAMES 824 11.68 9.46 1.50 66.26 114,771 39.8
FRAMES 824 11.29 8.89 1.43 71.00 119,330 65.6</span>

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

- Qwen3.5-4B：本地部署的较小开源 LLM 基线，用于衡量在统一搜索环境下、较低模型容量时的回答质量与工具使用行为。
- Qwen3.5-9B：本地部署的较大开源 LLM，与 4B 版本形成主要受控比较，用于考察模型容量增加是否改善问答正确率、提交成功率和搜索效率。
- deepseek-v4-pro：仅在每个数据集随机抽取 300 个样本的设置中评测的闭源商业模型，用于提供商业系统参照；Bamboogle 因总共只有 125 个样本而使用全部样本。
- gpt-5.4-2026-03-05：同样只用于 random-300 设置的闭源商业模型，作用是比较开源本地模型与商业模型在相同子集和工具协议下的表现。

**实验想回答的问题**

- 在固定的离线 Wikipedia 语料、检索工具接口和回答规则下，不同规模及来源的 LLM 作为搜索智能体时，在六个问答数据集上的最终回答质量如何？
- 最终回答分数背后，智能体的交互轮数、检索与页面打开次数、成功提交率、令牌消耗和运行时间如何随模型及任务难度变化？

**实验实现**

完整测试设置在每个数据集上评测可获得标准答案的划分；random-300 设置则每个数据集随机评测 300 个样本，但 Bamboogle 仅有 125 个样本。除非另有说明，智能体使用默认的 RRF（Reciprocal Rank Fusion，倒数排名融合）搜索，将多种检索结果按排名合并；采样温度为 0.7，top-p 为 0.95，每题最多运行 20 轮，每次助手响应最多调用 5 次工具。Qwen 开源模型通过 SGLang 在单张 NVIDIA A100 80GB GPU、CUDA 13.0 环境中本地推理，因此时间结果只代表该硬件与服务栈。最终答案同时报告词面 F1 和 LLM 语义裁判准确率，以避免单一指标掩盖改写答案或冗长答案的情况。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces a reproducible tool-based search environment and evaluation protocol for benchmarking LLM search agents.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`af2c646abaee88d4df26b69ec79ec51bd3988c1bef5cea4895de9f957f11d972`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
