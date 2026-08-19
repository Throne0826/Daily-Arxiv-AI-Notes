---
title: "[论文解读] ACTS-SQL: Agentic and Critic-Oriented Tree-Structured SQL Correctness with Large Language Models"
description: "[arXiv 2608.15145][LLM Agent] 原文未明确报告。"
arxiv_id: "2608.15145"
announcement_date: "2026-08-18"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:12:40.937855+00:00"
source_sha256: "2256406824fe8f2e47a218de057cc46604b8d1ca2b114f3bca9111bd8d95f7fd"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "LLM 其他"
  - "Text-to-SQL"
  - "SQL 自动纠错"
  - "大语言模型智能体"
  - "树结构推理"
  - "执行引导验证"
  - "语义歧义"
  - "分支与回溯"
  - "免训练方法"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.15145</p>

# ACTS-SQL: Agentic and Critic-Oriented Tree-Structured SQL Correctness with Large Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Xinmei Huang, Jie Song, Peng Li, Fuxin Jiang, Jing Zhang, Tieying Zhang, Jianjun Chen, Chenming Liu, Tao Yang, Maoyin Liu, Wenda Li, Hong Chen, Cuiping Li</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Renmin University of China；Renmin University of China；Affiliation: ByteDance Inc；ByteDance Inc</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.15145) · [PDF 下载](https://arxiv.org/pdf/2608.15145) · **关键词** Text-to-SQL, SQL 自动纠错, 大语言模型智能体, 树结构推理, 执行引导验证, 语义歧义, 分支与回溯, 免训练方法<br>


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

本文属于大语言模型驱动的文本到 SQL（Text-to-SQL）与 SQL 自动纠错领域。关系数据库以表、列及表间关系组织结构化数据，用户通过 SQL 表达连接、筛选、聚合等查询逻辑；Text-to-SQL 系统则把自然语言意图转换为 SQL。这里的关键困难不只是生成语法可执行的语句，还要保证连接路径、过滤条件、聚合方式和用户意图在语义上一致：SQL 即使成功执行，也可能悄然返回错误结果。真实工业环境进一步包含异构数据库、定制 SQL 方言和复杂数据格式，因此 SQL 纠错既用于清洗训练阶段由模型合成的数据，也用于在推理阶段修复候选 SQL 后再向用户返回结果。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**Text-to-SQL**

将用户的自然语言问题转换成可在关系数据库上执行的 SQL 查询。系统需要同时理解用户意图、数据库模式以及连接、过滤和聚合等查询语义。

</div>
<div class="concept-item" markdown="1">

**执行引导纠错**

运行候选 SQL，并利用语法错误、运行错误或查询结果等反馈继续修改 SQL。执行成功只能证明语句可运行，不能单独证明其结果符合用户意图。

</div>
<div class="concept-item" markdown="1">

**树结构调试**

把不同的语义解释或修改策略保留为不同分支，并在某条路径被判定错误时回退到较早节点。其核心机制是分支与回溯，用于避免一次早期误判锁定后续全部修改。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是用户的自然语言查询、一个存在语法或语义问题的 SQL，以及可用于检查模式和运行查询的数据库环境；输出是既可执行、又尽可能符合用户真实意图的修正 SQL。论文关注免训练设置，即不依赖针对特定数据库或 SQL 方言收集大规模监督数据并重新微调模型，而是在推理时由大语言模型规划和调用诊断、执行、模式检查及局部修复工具。问题允许用户意图存在歧义，也允许中间 SQL 因语法错误而暂时不可执行；因此系统必须区分“成功运行”和“语义正确”，保留多种合理解释，并能在发现不一致后回退。引言中的示例要求从形如 $M\times N$ 的文本描述中提取数值并识别产品类型，其中 $M$ 表示数字、$N$ 表示产品类型字符串；该例说明把关键词包含关系误解为精确匹配，会使单路径迭代不断叠加错误约束。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$M$**

引言示例中从文本模式提取的数值。

</div>
<div class="notation-item" markdown="1">

**$N$**

引言示例中与数值相连的产品类型字符串。

</div>

</div>

**直接相关的工作**

- **基于执行反馈的 SQL 迭代纠错**: 已有免训练方法通常根据运行错误或执行结果逐轮修改单个 SQL 候选。本文指出，这类线性过程依赖早期判断，而且执行成功不足以验证 SQL 是否符合用户语义。
- **智能体式 SQL 自调试**: 相关方法通过大语言模型的多轮交互进行诊断和修正，但通常仍沿单一路径推进。ACTS-SQL 将不同批评策略和语义假设显式组织成树，以分支保存备选方案，并以回溯放弃发生语义偏移的路径。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在真实的 Text-to-SQL 应用中，用户意图、数据库模式、表间连接关系和 SQL 方言往往具有高度异质性。LLM 一次生成的 SQL 即使能够通过语法解析或执行，也可能因连接条件、过滤位置、聚合逻辑或字符串匹配方式错误而产生语义不正确的结果。SQL 错误会同时影响在线查询服务的可靠性，以及由 LLM 生成或扩增训练数据时的数据质量，因此需要一种能够在多种数据库环境中稳定修正错误 SQL 的方法。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **一次性 Text-to-SQL 生成**：模型根据自然语言问题和数据库信息直接生成一条 SQL，随后将其作为最终查询。该路线能够降低人工编写 SQL 的负担，但通常难以在单次推理中同时正确处理复杂模式、连接、谓词和聚合语义。
- **基于执行反馈的训练无关智能体纠错**：LLM 先生成 SQL，再根据数据库执行结果、运行时错误或自我调试判断逐轮修改查询，直到得到看似可执行或更符合预期的版本。现有方法通常沿着单一路径逐步改写同一个 SQL 候选。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单路径逐轮改写容易受到早期隐含假设的支配。以“Electronics”筛选为例，模型若最初错误地将用户意图理解为精确字符串匹配，后续步骤就可能持续加强大小写归一化、去空格和正则精确匹配，而不会重新探索“包含该子串”这一合理解释，因而把错误假设固化为最终查询。
- 执行引导和整体式重生成难以同时保证语义稳定性与跨环境适应性。局部增加过滤条件或收紧谓词可能改变整个结果集，连续修改会造成错误累积和语义漂移；另一方面，依赖大规模领域微调需要昂贵的高质量监督数据，并可能在未见过的 SQL 方言上泛化不佳，因而难以满足真实工业系统的规模化部署需求。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作尚未充分解决这样一个具体问题：如何在无需依赖特定领域微调的前提下，使 SQL 纠错系统能够显式保留多种语义假设，基于数据库实例验证查询正确性，并在发现错误后回退到较早节点，而不是被迫沿单一、不可逆的修改轨迹继续推理。该缺口同时涉及候选路径生成、语义正确性判断和语法错误快速修复三种能力的协同。

</div>
<div markdown="1"><span>核心问题</span>

能否将 SQL 纠错建模为一种由计划引导的树结构调试过程，通过分支保留不同的修正策略和用户意图解释，通过回溯舍弃已经证伪的路径，并结合数据库交互与局部语法修复，在多种 SQL 方言和真实工业场景中获得更可靠、可扩展的纠错效果？

</div>
<div markdown="1"><span>作者直觉</span>

树结构的关键价值在于把不确定性显式化：当用户意图或修正方案存在多种合理解释时，系统暂时保留多个分支，而不是过早押注一个假设；当某条分支在执行结果、模式检查或语义评估中暴露问题时，系统可以回到之前的修改节点并尝试另一条路径。进一步地，直接运行 SQL 能以真实数据验证连接、过滤和聚合是否合理，按子句定位并修复语法错误则可以恢复可执行性，同时尽量不破坏已经确认的语义。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ACTS-SQL把SQL纠错建模为由修订计划驱动的树搜索过程。系统输入用户问题$U$、初始错误SQL $S_0$、数据库模式$D$、SQL方言以及已有执行结果，由Central Agent先生成树结构计划$T$；树中每个节点代表一次工具调用，边表示后续诊断或修复动作，分支则对应不同的错误解释或修复方向。系统沿树执行工具，根据数据库返回的证据动态扩展或选择分支，在叶节点生成候选SQL；若验证失败，便自底向上回滚并探索替代路径，直到返回通过检查的修正SQL $S^*$。

从直观上看，该方法不是要求大模型一次猜出答案，而是让它像数据分析师一样先列出排查计划，再查看真实列值、运行中间查询、拆解语法错误并逐步收集证据。树结构保存了尚未尝试的解释，因此某条路线失败后可以退回分叉点继续排查；这尤其适合处理“SQL能够执行但语义不符合用户意图”的情况，因为仅靠语法检查或最终执行成功无法识别此类错误。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成树结构修订计划

Central Agent生成初始计划$T$，指定根诊断操作和主要修复分支；每个节点以JSON字典表示，包含唯一标识、描述、工具名、工具输入和子节点列表，并由全局$cursor$指示当前执行节点。

<div class="method-step__io" markdown="1">

**输入**：用户问题$U$、初始错误SQL $S_0$、数据库模式$D$、SQL方言及$S_0$的执行结果。<br>
**输出**：可执行的初始修订树$T$及指向根节点的$cursor$。

</div>

**直观理解**：这一步相当于先制作排错流程图，而不是立即重写SQL；流程图明确下一步要检查什么，以及不同检查结果分别通向哪条路线。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行诊断并动态扩展计划

系统调用当前节点对应的工具；若Detect Ambiguities发现含义不明确的短语，就产生2至3个基于数据库模式的解释，并把这些解释扩展为新的语义分支。

<div class="method-step__io" markdown="1">

**输入**：当前节点、节点指定的工具输入、数据库模式、用户问题及此前节点的执行历史。<br>
**输出**：工具结果、附有执行证据的节点，以及必要时扩展后的计划树$T$。

</div>

**直观理解**：例如“活跃用户”可能指发帖者或回答者，系统会把这些理解分别列为候选路线，避免把大模型最先想到的解释直接当成事实。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于数据库证据选择与验证分支

Central Agent依据中间执行结果选择最可信的下一节点，并可运行任意子查询或抽样查看列值，以检验语义假设、匹配谓词和中间关系是否符合用户目标。

<div class="method-step__io" markdown="1">

**输入**：当前节点的多个子分支、Run SQL或Inspect Column Format返回的结果，以及完整交互历史。<br>
**输出**：更新后的$cursor$、被选中的推理路径及沿途积累的数据库证据。

</div>

**直观理解**：这类似于用数据库中的真实数据做实验：系统不是只看表名和列名推测，而是查看列值或中间结果，判断哪种解释更有证据支持。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成候选SQL并修复语法问题

Generate SQL要求大模型在证据约束下尽量少改原查询并生成候选SQL；若出现语法错误，Split and Fix Syntax Error SQL将其分解为无嵌套的单层$SELECT$关系单元，借助临时空表并行检查后，再由大模型综合子查询及错误信息重建SQL。

<div class="method-step__io" markdown="1">

**输入**：用户意图、数据库模式、原始SQL、当前路径上的诊断信号与执行反馈。<br>
**输出**：候选修正SQL及其自动执行结果，必要时还包括子SQL级语法诊断。

</div>

**直观理解**：语义已经基本确定后，系统才完成整条SQL；如果长查询报错，就先把它拆成投影、过滤、连接或聚合等小块，定位具体坏掉的子句后再拼回去。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。所给章节没有提出参数训练、微调损失或奖励函数，ACTS-SQL描述的是推理阶段的代理式编排框架：它通过提示词、工具调用、数据库执行反馈和树搜索控制现有大模型，而不是通过一个可学习目标优化模型参数。Central Agent对分支可信度和SQL正确性的判断由提示上下文驱动，原文未给出可计算的评分函数、阈值或形式化最优化目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Central Agent与JSON计划控制器**

Central Agent统一承担三类控制任务：生成初始树结构计划、在多分支节点选择下一节点、在叶节点判断候选SQL是接受还是回滚。其提示上下文包含任务规则、可用工具及输入输出规范、SQL方言、模式、用户问题、错误SQL、执行结果、当前JSON计划和全部节点历史；通过修改全局$cursor$实现有状态的非线性遍历。

> 直观理解：它相当于排错负责人：工具负责执行具体检查，Central Agent负责决定检查顺序、解释检查结果并维护进度。显式JSON状态使已经尝试的路线、工具结果和备用分支能够被追踪，减少多轮推理中遗忘上下文的风险。

**2. 语义诊断与数据库执行工具**

Detect Ambiguities利用大模型识别用户请求中未充分说明的短语，并为每处歧义给出2至3个由数据库模式约束的解释；Run SQL执行任意SQL并以列表返回元组，Inspect Column Format则把指定表名和列名填入固定查询模板，返回该列的样本值。这些工具将自然语言假设转化为可由真实数据库行为支持或反驳的诊断信号。

> 直观理解：SQL语法正确时，错误常来自对用户措辞或数据格式的误解，例如把日期文本、类别编码或“重叠”概念理解错。该模块让系统先提出有限的解释，再查看真实数据验证，从而避免只凭语言模型常识修复SQL。

**3. 语法分解修复与受约束SQL生成**

Split and Fix Syntax Error SQL把无效查询重写为最小、可独立执行且仅含一个平坦$SELECT$的关系单元，并显式保留单元间依赖；若子SQL $B$依赖子SQL $A$，系统创建输出模式与$A$一致的空临时表，使二者可独立并行接受语法检查。随后，大模型结合各子SQL及其错误信号合成修正版；Generate SQL则使用根节点至当前节点的全部证据生成尽量少改动、避免无依据假设的最终候选，并自动执行。

> 直观理解：长SQL中的多个错误会互相遮蔽，数据库通常只先报告其中一个；拆成小单元后可以同时发现不同子句的问题。空临时表只模拟依赖结果的结构，不要求先算出上游数据，因此能把“语法是否成立”和“查询最终返回什么”分开检查。

**训练与推理**

原文所述流程属于推理阶段。初始化时，系统将$U$、$S_0$、$D$、SQL方言和初始执行结果交给Central Agent，生成计划$T$并把$cursor$置于根节点；随后循环执行当前节点。如果当前工具发现歧义，系统将候选解释扩展为子节点；若当前节点有多个子节点，Central Agent依据工具结果选择下一节点，若只有一个子节点则直接前进。Run SQL和Inspect Column Format在遍历过程中提供数据库行为与列值证据，Split and Fix Syntax Error SQL负责细粒度语法定位，Generate SQL在叶节点综合完整路径上下文生成并执行候选SQL。

候选SQL通过Central Agent的正确性检查后，系统输出$S^*$并终止；若未通过，则在$T$中回滚到可继续探索的位置，更新$cursor$后重复诊断、生成和验证。原文称系统可回滚到计划中的任意节点，但未明确给出回滚节点排序、搜索预算、最大迭代次数、超时策略，或在所有分支都失败时的返回规则；因此不能把该过程理解为具有完备性保证的确定性搜索算法。

**复现信息**

复现该方法所需的核心接口包括：支持节点增删和$cursor$更新的JSON计划表示；能够接收任务说明、工具规范、输出格式及完整历史的Central Agent提示；五类工具，即Detect Ambiguities、Run SQL、Inspect Column Format、Split and Fix Syntax Error SQL与Generate SQL；以及可执行目标SQL方言、返回查询结果并创建临时空表的数据库环境。Generate SQL应获得用户意图、模式、原SQL、执行反馈和当前路径的全部诊断信号，并被要求最小化无必要改写、避免推测性假设、严格依据已有证据。

语法分解工具需要把查询转换成投影、过滤、连接或聚合等单层$SELECT$单元，并依据上游输出列建立模式匹配的临时表，以便独立或并行进行语法检查。所给章节未明确报告所用基础大模型及版本、生成参数、提示词全文、上下文长度、数据库采样数量、候选分支选择温度、验证检查的精确定义、搜索上限、并行执行配置或失败恢复细节；这些缺失会影响运行成本、确定性和复现公平性，实施时不应自行视为论文既定设置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- BIRD-CRITIC-Open：由真实用户报告的 SQL 错误构建的公开 SQL 调试基准中的多方言子集，覆盖 PostgreSQL、MySQL、SQL Server 和 Oracle。实验用它检验系统处理不同语法规则与错误模式时的迁移能力。原文未明确报告该子集的样本数及数据划分。
- BIRD-CRITIC-PG：BIRD-CRITIC 的 PostgreSQL 子集，任务输入是需要诊断和修复的错误 SQL，而非从自然语言直接生成 SQL。它用于比较不同修复方法在统一数据库方言下的整体效果，并承载规划结构及关键工具的消融实验。原文未明确报告样本数及数据划分。
- TLS：来自工业日志分析服务的真实 Text-to-SQL 类数据集，其中目标语言是面向大规模日志分析的非标准 SQL 类领域专用语言 TLS。数据包含真实用户自然语言请求及在生产系统中执行的标准 TLS 查询，覆盖 288 个主题（表），每表平均 21.33 列。该数据不提供错误 SQL，方法必须先从自然语言生成 TLS，再由 critic 依据执行反馈进行修正，因此用于检验实际部署中的生成后纠错能力。原文未明确报告查询总数及训练、验证、测试划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**执行正确率**

在 BIRD-CRITIC 中，预测 SQL 在目标数据库上的执行结果与标准 SQL 相同即判为正确；在 TLS 中，生成或修正后的 TLS 执行结果与标准 TLS 相同即判为正确。该指标重视查询结果语义，而不要求 SQL 字符串完全一致。 （越高越好，因为更高比例表示更多查询产生了与标准查询相同的执行结果。）

</div>
<div class="metric-item" markdown="1">

**端到端延迟（Lat., 秒）**

TLS 实验中从初始生成到 critic 完成全部诊断、执行和细化过程的平均运行时间，用于衡量纠错模块的实际响应成本。 （越低越好，因为在准确率相近时，更短延迟更适合在线生产服务；但该指标必须与准确率联合判断，不能单独代表方法质量。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### BIRD-CRITIC-Open 与 BIRD-CRITIC-PG 总体比较

<div class="result-value" markdown="1">

ACTS-SQL 在 Open 和 PG 上分别达到 58.70% 与 64.29%。表中最强非 ACTS-SQL 方法 XiYan Model 分别为 49.28% 与 45.92%；最强 raw model 在 Open 上为 GPT-o3 的 41.30%，在 PG 上为 DeepSeek-R1 的 38.78%。

</div>

该结果支持作者关于结构化、执行引导修复优于直接模型调用和既有修复代理的主张。尤其是 PG 上的优势说明提升并非只来自混合方言样本。不过，这只是同一基准上的执行正确率比较，不能独立证明每个增益均由树规划造成；该因果判断还需要结合消融实验。

<div class="result-source" markdown="1">

来源：表 1（Main results on the BIRD-CRITIC benchmark）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ACTS-SQL 58.70% 64.29% 53.06% 33.67% 45.85%

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### BIRD-CRITIC-Open 的四种数据库方言

<div class="result-value" markdown="1">

ACTS-SQL 在 PostgreSQL、MySQL、SQLServer 和 Oracle 上分别取得 53.06%、33.67%、45.85% 和 58.70% 的结果；对应的 XiYan Model 为 43.88%、28.57%、44.53% 和 49.28%。

</div>

四个方言上均高于该微调模型，支持作者所称的跨方言一致性，也说明仅依赖以生成任务为主的微调不一定适合错误诊断。需要注意，MySQL 的绝对正确率仍只有 33.67%，SQLServer 相对 XiYan Model 的差距也较小，因此结果显示的是相对优势，而不是所有方言上的问题已经解决。

<div class="result-source" markdown="1">

来源：表 1（列顺序为 Bird-critic Open、Bird-critic PG、PostgreSQL、MySQL、SQLServer、Oracle）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ACTS-SQL 58.70% 64.29% 53.06% 33.67% 45.85%

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 工业 TLS 数据集上的跨基础模型 critic 比较

<div class="result-value" markdown="1">

ACTS-SQL 在 GPT-5、GPT-o3、DeepSeek-R1 和 XiYan 四个基础模型上分别达到 53.61%、56.36%、23.85% 和 13.75%的最高准确率，对应平均延迟为 218.91、277.41、38.65 和 42.56 秒。无 critic 时的准确率分别为 36.77%、40.55%、22.68% 和 13.40%。

</div>

控制初始生成器后，ACTS-SQL 在四种骨干上均提高最终准确率，因而支持纠错机制不依赖单一模型的主张；GPT-5 与 GPT-o3 上提升最明显，而 DeepSeek-R1 与 XiYan 上提升有限。与此同时，ACTS-SQL 在前两个强模型上的延迟远高于 No Critic 和 LLM Critic，因此作者所称“适度且可用于生产”的开销需要结合具体服务时限审慎判断，表中数据并不证明其在所有在线场景都满足延迟要求。

<div class="result-source" markdown="1">

来源：表 3（Performance of different critic strategies on the TLS dataset）；其余基础模型结果见同表

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GPT-5 (9) 36.77% 6.31 47.42% 26.52 37.74% 72.51 46.83% 15.51 53.61% 218.91

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验报告缺少样本总数、测试划分细节、硬件、调用成本、重复运行、方差、置信区间和显著性检验，因此难以判断较小差距是否稳定，也无法完整复现实验或评估生产成本。TLS 数据来自单一工业日志分析服务，且没有说明能否公开，外部研究者可能无法独立验证其结果。
- 效率结论需要谨慎解读：表 3 中 ACTS-SQL 在 GPT-5 和 GPT-o3 上的平均延迟分别为 218.91 秒和 277.41 秒，显著高于对应 No Critic 的 6.31 秒和 18.17 秒。原文称额外延迟“moderate and comparable”，但未提供线上延迟预算、吞吐量、并发测试或成本数据；同时，表 2 未说明各消融变体是否具有相同推理、token 和工具调用预算。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Raw Models：包括 GPT-o3、GPT-5、DeepSeek-R1，另在主表中报告 grok-4。它们在没有额外训练或外部工具的情况下直接修复 SQL，用于判断结构化代理是否优于强基础模型的一次性端到端推理。
- SQL Correction Agents：SQLFixAgent、DAC、RepairAgent 和 MapleRepair 代表已有代理式或免训练 SQL 修复方法。重点对照 DAC 与 MapleRepair，因为它们同样利用诊断或执行相关机制，但主要采用线性细化过程，可检验 ACTS-SQL 的树分支与回退设计是否带来额外价值。
- XiYan-SQL：经过多任务微调的 Text-to-SQL 模型，覆盖多种 SQL 格式和数据库方言。该比较用于检验面向 SQL 生成的监督微调能否直接迁移到真实报错修复及非标准 TLS；它与训练免调、推理时执行引导的 ACTS-SQL 形成方法路线上的对照。
- TLS critic 策略：在同一 GPT-5、GPT-o3、DeepSeek-R1 或 XiYan 初始生成器上分别配置 No Critic、通用 LLM Critic、DAC、MapleRepair 和 ACTS-SQL。控制基础生成模型后进行比较，可以把最终变化主要归因于纠错模块，而不是初始生成器能力。

**实验想回答的问题**

- 在面向真实报错的 SQL 修复任务中，ACTS-SQL 是否比直接调用大语言模型、线性修复代理和经过微调的 Text-to-SQL 模型具有更高的执行正确率，并且能否跨 PostgreSQL、MySQL、SQL Server 和 Oracle 方言保持这一优势？
- 性能提升是否确实来自树结构规划、执行反馈和歧义检测；当系统迁移到工业 Text-to-TLS 生成任务时，这些机制能否跨不同基础模型提高准确率，同时保持可接受的端到端延迟？

**实验实现**

BIRD-CRITIC 上所有方法采用相同实验设置；代理基线遵循作者公开的官方实现与配置。Raw Model 通过官方推理 API 调用，温度为 0.1、$top-p$ 为 0.95、最大输入长度为 8K tokens；原文同时说明除非另有指定，大语言模型采用确定性解码以降低随机性，但没有进一步解释该表述与上述采样参数如何协调。XiYan-SQL 使用 BIRD-CRITIC 排行榜评估 raw model 的同一提示协议。BIRD-CRITIC 以执行结果等价判定正确性。TLS 则先让每个基础模型根据自然语言生成初始查询，再执行查询；启用 critic 时，系统根据执行反馈迭代诊断和修改，并同时报告最终准确率与完整细化延迟。原文未明确报告硬件、重复运行次数、随机种子、置信区间或显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 将树结构细化计划替换为单一路径线性计划 | 完整方法在 BIRD-CRITIC-Open 和 PG 上为 58.70% 与 64.29%，线性计划变体降至 45.81% 与 36.93%；其 PostgreSQL、MySQL、SQLServer、Oracle 结果分别为 38.88%、20.47%、36.56% 和 45.81%。 | 该变体保留逐步调用工具和生成 SQL 的流程，但禁止分支与回退，因此主要隔离树结构规划的作用。PG 上明显下降支持这样的解释：线性方法一旦过早接受错误语义假设，后续修改只能沿错误路径累积；树结构则可并行保留候选解释并从失败分支回退。不过，原文没有报告 token 或工具调用预算是否严格匹配，所以不能排除树方法使用更多推理资源也是部分增益来源。 | 表 2（Ablation study of ACTS-SQL on the BIRD-CRITIC benchmark）<br><span class="experiment-evidence">w/ Linear Plan 45.81% 36.93% 38.88% 20.47% 36.56%</span> |
| 移除执行工具或用户查询歧义检测工具 | 移除执行工具后，Open 与 PG 分别降至 39.84% 和 32.66%；移除歧义检测后分别为 43.89% 和 27.37%，均低于完整方法的 58.70% 和 64.29%。按 Open 结果看执行工具影响更大，按 PG 结果看歧义检测变体更低，因此不能笼统断言执行工具在所有设置上都造成最大降幅。 | 执行工具消融检验运行 SQL、检查列和观察中间结果是否为分支选择与回退提供必要证据；歧义检测消融检验系统在修复开始前澄清用户意图的价值。二者都重要，但作用阶段不同：执行反馈主要验证候选 SQL 的行为，歧义检测主要减少一开始选错语义解释的概率。原文关于“移除执行工具导致更大下降”的概括与 PG 列的数值并不完全一致，复核论文时应特别检查表格或文字是否存在口径差异。 | 表 2；歧义检测变体同表为“w/o Ambiguity Detection 43.89% 27.37% 31.28% 25.67% 38.45%”<br><span class="experiment-evidence">w/o Execution Tool 39.84% 32.66% 29.85% 21.48% 37.92%</span> |

**定性案例**

- 图 4 讨论“2022 年各产品类别中月销售额最高的前三个产品”。“月销售额”可能指逐月排名，也可能被错误理解为全年汇总后排名。基础模型先采用全年聚合，线性代理即使看到错误执行结果，也只在该固定语义下继续局部修改；ACTS-SQL 则为不同解释建立分支、分别执行验证，并从无效路径回退。该案例直观展示了树规划如何处理语义歧义，但它只是代表性个案，不能替代总体准确率或按错误类型统计。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops an LLM-based agentic and critic-guided tree search system for verifying and correcting SQL, making tool-like task execution and reasoning central.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`2256406824fe8f2e47a218de057cc46604b8d1ca2b114f3bca9111bd8d95f7fd`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
