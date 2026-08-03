---
title: "[论文解读] When Iterative RAG Beats Ideal Evidence: A Diagnostic Study in Scientific Multi-hop Question Answering"
description: "[arXiv 2601.19827][LLM Reasoning] 本文通过统一控制的诊断实验，研究科学多跳问答中同步交替的检索与推理为何以及何时能够优于一次性提供全部标注证据的 Gold Context。"
arxiv_id: "2601.19827"
announcement_date: "2026-08-03"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-03T02:17:35.855619+00:00"
source_sha256: "eb7f3e04600e371ef4952157c8a3f991243d0cd3ff1768318ac4aa1420659b57"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "科学多跳问答"
  - "检索增强生成"
  - "迭代 RAG"
  - "Gold Context"
  - "化学问答"
  - "检索—推理同步"
  - "机制级诊断"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2601.19827</p>

# When Iterative RAG Beats Ideal Evidence: A Diagnostic Study in Scientific Multi-hop Question Answering

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-03</span>
<span><strong>作者</strong> Mahdi Astaraki, Mohammad Arshi Saloot, Ali Shiraee Kasmaee, Hamidreza Mahyar, Soheila Samiee</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Faculty of Engineering, McMaster University, Canada；BASF Canada Inc., Canada</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2601.19827) · [PDF 下载](https://arxiv.org/pdf/2601.19827) · **关键词** 科学多跳问答, 检索增强生成, 迭代 RAG, Gold Context, 化学问答, 检索—推理同步, 机制级诊断<br>


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

本文通过统一控制的诊断实验，研究科学多跳问答中同步交替的检索与推理为何以及何时能够优于一次性提供全部标注证据的 Gold Context。

**不用术语来说**：回答复杂的化学问题往往需要把分散在多个来源中的事实按顺序连接起来；即使系统一开始就拿到所有正确证据，模型也可能因信息过载、证据顺序与自身思路不匹配，或不会组合多个事实而答错。因此，关键问题不只是“是否找到了证据”，还包括“何时检索什么、怎样依据中间结论继续检索，以及何时停止”。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 建立统一的受控比较框架，在相同检索接口和编排约束下，对十一种语言模型比较 No Context、Gold Context 与 Iterative RAG，从而同时区分参数记忆、静态理想证据和同步检索—推理过程的作用。
- 将评价从最终准确率扩展到机制层诊断，考察逐跳证据覆盖、锚点传播、查询质量、证据组合、停止校准、干扰项锁定与程序遵从，以解释迭代检索成功或失败的具体原因。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究科学领域的多跳问答与检索增强生成。多跳问答要求模型把分散在多个来源、多个推理步骤中的证据串联起来；在化学等专业领域，相关知识较稀疏，通用大语言模型的参数记忆覆盖有限，且中间结论需要进一步组合才能得到最终答案。传统静态 RAG 通常先一次性检索并固定上下文，再让模型完成生成；迭代 RAG 则在回答过程中交替进行检索、假设更新与停止判断，使后续检索能够依据当前推理状态调整。本文关心的核心不是提出新的 RAG 算法，而是在统一控制条件下诊断：这种同步的检索—推理过程能否比一次性提供全部标注证据的 Gold Context 更有效，以及模型架构、问题跳数和证据利用行为如何影响这一比较。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多跳问答（Multi-hop QA）**

答案不能由单条事实直接得到，而要先找到若干中间事实，再按依赖关系逐步组合。例如，前一跳确定某个化合物，后一跳再查询该化合物的性质。

</div>
<div class="concept-item" markdown="1">

**检索增强生成（RAG）**

模型生成答案前或生成过程中，从外部知识源检索相关证据，以减少仅依赖参数记忆造成的知识缺失或幻觉。静态 RAG 固定一次性上下文，迭代 RAG 则让检索结果随推理进展动态变化。

</div>
<div class="concept-item" markdown="1">

**Gold Context（理想证据上下文）**

由数据集标注提供的 oracle 证据；本文将每一跳的标注证据一次性作为段落交给生成模型，形成理想化的静态 RAG 基线。它代表证据选择近乎完美，但不必然是实际性能上界，因为长上下文可能带来干扰，证据顺序也可能与模型的推理轨迹不一致。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务是在以化学为重点的 ChemKGMultiHopQA 上回答需要跨多跳证据组合的问题。研究先用 No Context 条件筛除仅凭模型内部参数知识即可回答的样本，从而把分析集中于真正依赖外部检索的问题；随后在相同问题上比较三种条件：No Context 只允许参数记忆，Gold Context 一次性提供各跳的 oracle 证据，Iterative RAG 则在统一控制器下交替执行检索、假设修正和基于证据的停止。输入包括问题以及相应条件允许访问的证据源或标注上下文，输出是最终答案；比较对象为十一种推理型与非推理型大语言模型。研究假设统一检索接口、将分块和重排序与生成解耦，并对所有模型采用相同编排约束，以尽量把性能差异归因于证据提供过程及模型利用机制，而不是检索配置差异。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Lewis et al. (2020)**: 被本文用作 RAG 的基础背景：通过外部检索为生成模型提供依据，降低对参数记忆的依赖；本文进一步比较静态证据供给与迭代检索—推理。
- **Nahid and Rafiei (2025)**: 相关研究通常把 Gold Context 视为检索系统试图接近的理想上界；本文强调它并非必然的操作性上界，并直接检验迭代 RAG 是否能够超过该静态基线。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

科学多跳问答要求模型跨多个步骤整合稀疏且异构的领域知识。化学等专业领域在通用模型训练数据中的覆盖有限，中间结论通常还必须转化为下一步检索线索；若后续一跳缺少证据，或模型不能把已获得的事实组合起来，整条答案链就会失败。这使可靠的外部检索及其与推理过程的协调成为实际需求。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **静态 RAG 与 Gold Context**：系统先进行一次检索，再让模型基于固定上下文一次性生成答案；Gold Context 是其理想化版本，即把数据集标注的每一跳预言机证据同时作为上下文交给生成模型，通常被用作静态检索条件的强基线或近似上界。
- **迭代或动态 RAG**：系统在多个步骤中交替执行检索和推理：模型依据当前证据形成或修正中间假设，再用该假设生成下一次查询，并通过显式步骤分配和停止判断决定是否继续。它同时利用推理改善检索，也利用新证据推进推理。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有比较通常只以单步检索为基线，结果容易受到文本解析、切块、向量表示与重排序配置差异的影响，因而难以判断提升究竟来自迭代机制，还是来自更有利的检索实现。
- 相关研究往往只考察“推理增强检索”或“检索增强推理”的一侧，且常缺少 No Context 与 Gold Context 的联合对照、只测试少量模型；因此无法系统判断静态理想证据是否真是有效上界，也难以解释模型架构、跳数和过程控制如何影响结果。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

在专业科学领域中，尚缺少一种跨多类语言模型、统一检索与编排条件的机制级研究，用来检验迭代检索—推理是否能超过 Gold Context，并把性能差异进一步归因于逐跳覆盖、自我纠错、证据组合、干扰路径或停止策略，而非检索配置差异。

</div>
<div markdown="1"><span>核心问题</span>

对于真正依赖外部证据的化学多跳问题，同步的迭代检索—推理能否稳定优于一次性提供全部预言机证据的 Gold Context；若能，这种优势在什么模型类型和跳数条件下出现，又由哪些过程机制与失败模式决定？

</div>
<div markdown="1"><span>作者直觉</span>

一次性给出全部正确证据并不等于模型能够正确使用它们。分阶段检索可以让每一步只围绕当前中间结论取得更相关的信息，把上一跳得到的关键实体作为下一跳的“锚点”，并在发现方向错误时及时改写查询。这样既能降低长上下文中的干扰与认知负担，也能使证据出现的顺序更贴合模型的推理轨迹；不过其收益仍取决于系统能否覆盖最后几跳、避免被无关事实带偏，并正确判断何时停止。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文提出的不是一个需要训练的新模型，而是一套用于科学多跳问答的无训练迭代式检索增强生成框架及其诊断协议。给定化学问题，系统先强制执行一次检索，再让同一个被测语言模型依据当前证据形成“部分答案”，判断信息是否充分；若仍有缺口，模型生成只针对下一推理跳的子查询并再次检索，否则从已收集证据中生成带引用的最终答案。整个循环最多允许 $5$ 次检索，每次保留当前轮的完整 top-$10$ 段落，同时从每个历史轮次中最多保留 $2$ 个最佳段落，以在证据连续性与上下文噪声之间折中。

该框架的核心实验意义是把三个因素分开考察：无上下文条件测参数记忆，Gold Context 条件用构造问题时的全部真值段落模拟无检索噪声的理想静态 RAG，Iterative RAG 条件则测试检索、规划和证据综合能否在推理过程中协同工作。通俗地说，Gold Context 是一次性把所有正确材料放到桌上，而迭代框架像逐步查资料：先确认当前知道什么，再只搜索下一块缺失信息，并在资料足够时停止。作者还利用数据集提供的逐跳真值路径审计查询、检索、停止决策和最终综合，从而避免只看答案对错却无法定位失败原因。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 语料预处理与化学领域索引

系统对文本执行 Unicode 规范化和空白清理，再切分为长度 $220$ 词、相邻块重叠 $50$ 词的文本块；随后使用化学专用句向量编码器 BASF-AI/ChEmbed 将文本块编码并建立可检索索引。该窗口旨在容纳完整定义或性质描述，同时避免过长文本稀释与查询相关的信号。

<div class="method-step__io" markdown="1">

**输入**：ChemKGMultiHopQA 配套语料，来源包括 ChemRxiv、PubChem 和 Wikipedia。<br>
**输出**：由化学语义向量表示的重叠文本块索引。

</div>

**直观理解**：这一步相当于把不同来源的化学资料整理成大小适中的卡片，并按化学语义建立目录。专用编码器有助于识别化学名称、分子式和专业术语之间的关联，而不只依赖字面相同。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 强制首轮检索

系统以原始问题作为首轮查询，执行一次不可跳过的检索，并返回相关性最高的 top-$10$ 段落。论文把一次独立检索动作定义为一个步骤，因此若模型在第 $1$ 步后立即结束，该次运行总共只包含一次查询。

<div class="method-step__io" markdown="1">

**输入**：用户的原始多跳化学问题和已建立的语料索引。<br>
**输出**：第 $1$ 轮的 top-$10$ 候选证据及原始问题状态。

</div>

**直观理解**：无论模型自认为是否知道答案，都必须先查一次资料。这样既保证迭代条件确实使用外部证据，也为后续判断“还缺什么”提供起点。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 部分答案更新与证据视图构造

模型阅读第 $K$ 轮查询和检索段落后生成“第 $K$ 步部分答案”，明确记录目前已确认的事实或暂定假设。为限制上下文膨胀，规划器完整接收当前轮 top-$10$ 段落，但对此前每一轮仅接收最多 $2$ 个最佳段落；达到最大预算时，总证据视图约为 $18$ 个段落。

<div class="method-step__io" markdown="1">

**输入**：原始问题、当前步编号、当前轮 top-$10$ 段落、历史查询与部分答案，以及经过筛选的历史证据。<br>
**输出**：更新后的部分答案，以及供控制器作下一步决策的紧凑证据状态。

</div>

**直观理解**：部分答案类似研究笔记：它不是最终作答，而是把刚查到的可靠信息写下来，防止下一轮忘记关键实体。历史资料只保留精华，避免所有旧段落堆在一起分散模型注意力。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 检索或终止的控制决策

规划器必须在两个动作中选择一个：若仍存在知识缺口，则生成针对下一逻辑跳的原子化子查询并执行第 $K+1$ 次检索；若证据已充分，则选择 Finalize。该循环受最多 $5$ 次检索的固定预算约束，新增查询应利用已确认的中间实体推进，而不是重复原问题或同时混合多个推理跳。

<div class="method-step__io" markdown="1">

**输入**：紧凑证据视图、部分答案、原始问题、历史查询及当前检索步数。<br>
**输出**：下一轮检索查询及其候选证据，或者终止信号。

</div>

**直观理解**：控制器像查资料时的导航员：每轮只决定“下一件最需要查清的事”，或者确认材料已经够用。固定预算防止无休止搜索，部分答案则帮助查询携带上一跳得到的化合物、性质或关系。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该方法是 training-free 的测试时控制与评估框架，不更新语言模型、检索编码器或答案裁判的参数，也没有论文所定义的训练损失函数。优化发生在推理流程层面：通过显式部分答案、针对下一推理跳的查询改写、历史证据筛选和停止决策，在固定检索预算内提高证据覆盖与多跳综合质量；这些设计是控制策略，而非通过梯度下降学习的目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 检索—规划—编排控制器**

控制器协调 Retrieval、Planning 与 Orchestration 三项职责：检索器从化学索引返回证据，规划器依据当前部分答案识别下一知识缺口，编排器维护步骤、历史状态和最多 $5$ 次检索的预算。第 $1$ 次检索是强制的，此后每轮只能选择 Retrieve 或 Finalize，因而将开放式思考约束为可审计的离散动作序列。

> 直观理解：该模块把“思考”和“查资料”交替安排，而不是一次检索后直接作答。它需要解决的不只是找到相关文本，还要决定下一步查什么以及什么时候停止。

**2. 部分答案与紧凑上下文管理**

部分答案是模型观察第 $K$ 轮查询与证据后形成的显式知识状态，并连同历史查询、原问题和步编号传入下一轮。上下文管理器保留当前轮全部 top-$10$ 段落，并从每个先前步骤最多挑选 $2$ 个最佳段落，使后续规划既能访问最新证据，也能携带跨跳所需的关键事实。

> 直观理解：多跳检索容易在后续轮次忘记上一轮找到的实体，也容易被大量旧文本淹没。显式笔记负责维持推理链，精选历史段落负责控制噪声，两者共同降低推理漂移。

**3. 机制级诊断与答案验证**

诊断套件利用 ChemKGMultiHopQA 提供的真值推理跳、逐跳上下文和检索日志，将失败分为证据获取、策略控制和信息综合三类。具体检查包括逐跳检索覆盖缺口，Vague、Over-Broad、Fusion、Off-Topic 四类查询质量标记，Anchor Carry–Drop、置信度失准、流程遵循率、干扰项锁定，以及证据充分时仍答错的 Composition Failure 和句子级 Sufficiency Score；所有诊断判断仅依据问题、真值路径与日志，不引入外部知识。

> 直观理解：最终答错可能是没搜到、搜索方向跑偏、过早停止，或明明有证据却组合错误。该模块沿整个过程逐项检查，因此能解释迭代 RAG 为什么成功或失败，而不是只给出一个准确率。

**训练与推理**

训练阶段不存在额外训练。实验先离线规范化并切分 ChemKGMultiHopQA 语料，再使用现成的 BASF-AI/ChEmbed 构建化学文本块索引；被测语言模型、嵌入模型和 GPT-5-mini 裁判均按现成能力使用。

推理时分别运行三种配置以隔离不同能力来源。No Context 只给问题，不提供外部段落，用于观察参数记忆；Gold Context 一次性提供生成该问题所依据的全部真值支持段落，并禁止后续检索，用于近似检索精度完美、无无关干扰的静态 RAG；Iterative RAG 则先按原问题强制检索 top-$10$，生成部分答案并判断信息充分性，随后反复生成下一跳子查询、更新证据和部分答案，或在充分时终止，最多执行 $5$ 次检索。终止后由保守综合器依据已提供证据生成带引用答案，再由 GPT-5-mini 按化学实体语义等价规则判断正确性。与此同时，诊断器把每轮查询、命中证据、实体锚点传递、停止行为和最终综合与数据集的真值跳路径对齐，以区分检索失败、控制失败和综合失败。

**复现信息**

复现与公平解释所需的关键设置如下：数据集采用 ChemKGMultiHopQA，因为它包含一至四跳的跨文档化学短答案问题，并提供子问题、中间答案、显式跳间连接和真值支持段落；语料块长度为 $220$ 词、重叠 $50$ 词，嵌入器为 BASF-AI/ChEmbed。每次检索返回 top-$10$ 段落，当前轮段落全部进入规划上下文，每个历史轮次最多保留 $2$ 个最佳段落，检索预算上限为 $5$ 步。

Gold Context 使用构造问题时的最小真值支持段落且不允许再检索，因此它测试静态证据利用和多跳组合，而不是检索能力；Iterative RAG 则同时受实际检索质量和控制策略影响。答案不能仅用精确字符串匹配评判，裁判需接受别名、同义词、分子式与 IUPAC 名称等价。难度分层基于 $11$ 个被测模型的错误数量：错误模型不超过 $2$ 个为 Easy，错误 $5$ 至 $7$ 个为 Medium，错误 $9$ 至 $11$ 个为 Hard；该分层反映模型群体的经验难度，并非依据问题跳数直接定义。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 实验使用一个包含 1 至 4 跳问题的科学多跳问答评测集，同一批问题在 No Context、Gold Context 与 Iterative RAG 条件下接受测试。Gold Context 提供完整的预设正确证据，用于近似理想静态检索；Iterative RAG 则允许模型根据当前推理状态逐步检索。所给章节未明确报告数据集名称、总规模、来源及训练—验证—测试划分，因此不能据此判断结果对其他科学领域或开放域问答的泛化性。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

最终答案正确的题目比例；论文按模型和运行条件报告百分比，并以跨模型均值及标准差概括总体趋势。 （越高越好，因为它直接衡量科学多跳问题的最终作答成功率；但单一准确率会掩盖从 Gold Context 切换到 Iterative RAG 后不同题目上的恢复与回退。）

</div>
<div class="metric-item" markdown="1">

**Average Output Tokens**

每次回答平均生成的输出 token 数；Iterative RAG 的输出包括检索查询、部分答案和跨步骤状态，因此该指标近似反映生成成本与测试时计算量，而不是检索系统的全部延迟或货币成本。 （在准确率相近时越低通常越好，因为生成开销较小；不能脱离准确率单独比较，也不能把 token 数直接等同于完整部署成本。）

</div>
<div class="metric-item" markdown="1">

**Parametric Suppression Rate（PSR）**

在 No Context 下原本回答正确、但启用 Iterative RAG 后转为错误的题目，占 No Context 正确题目的比例，即 $PSR=|Q_{correct}^{NoCtx}\cap Q_{incorrect}^{IterRAG}|/|Q_{correct}^{NoCtx}|$。它衡量检索对模型既有正确参数知识的破坏程度。 （越低越好；较低的 $PSR$ 表示模型更能在检索片段与内部知识冲突时过滤噪声并保留原有正确判断。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三种证据条件的跨模型总体准确率

<div class="result-value" markdown="1">

11 个模型的平均准确率由 No Context 的 $37.16\pm5.54\%$ 上升到 Gold Context 的 $69.14\pm7.22\%$，再上升到 Iterative RAG 的 $80.89\pm5.08\%$；图 2 的成对检验表明这种总体排序在模型间具有一致性。

</div>

作者的结果表明，正确静态证据已经带来大幅收益，但把检索动作与当前推理状态同步，仍能进一步提高最终准确率。直观上，一次性给出所有正确段落并不保证模型能发现正确的证据使用顺序；迭代过程会先形成中间结论，再据此缩小下一步搜索范围。不过，该比较不能单独证明提升完全由“同步”机制产生，因为三种条件的提示格式、输出长度和交互过程也不同，需结合 Gold+CoT 消融理解。

<div class="result-source" markdown="1">

来源：第 4 节，表 1 与图 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Performance is weak in the No-Context condition (37.16 ± 5.54%). Providing Gold Context substantially improves accuracy (69.14 ± 7.22%). Iterative RAG, which couples retrieval with stepwise reasoning, yields further gains: (80.89 ± 5.08%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 模型级别的 Iterative RAG 收益与最佳表现

<div class="result-value" markdown="1">

所有表 1 中的模型在 Iterative RAG 下均高于各自的 Gold Context 准确率；Claude Sonnet 4.5 从 $73.85\%$ 提升到 $87.68\%$，增加 $13.83$ 个百分点，并取得最高 Iterative RAG 准确率。GPT-4o 的变化更大，从 No Context 的 $32.29\%$ 提升到 Iterative RAG 的 $81.96\%$。

</div>

这说明收益不是只发生在能力较弱或没有推理优化的模型上：强推理模型也能从按步骤获取证据中受益。与此同时，不同模型的边际收益差异很大，意味着 Iterative RAG 并非与底座模型无关的固定增益；模型对静态长上下文的利用能力、查询生成质量以及对检索噪声的抵抗力都会影响结果。这里展示的是同一评测集上的相关表现，不能据此断言所有科学任务都能获得相同幅度的提升。

<div class="result-source" markdown="1">

来源：第 4 节，表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For instance, GPT-4o jumps from 32.29% (No Context) to 81.96% (Iterative RAG), a massive 49.67 pp gain, significantly exceeding the 24.03 pp gain achieved by providing Gold Context. Similarly, Claude Sonnet 4.5 sees its performance more than double, rising from 40.02% to 87.68%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 所有模型共同无法回答的问题及其跳数分布

<div class="result-value" markdown="1">

被全部 11 个模型答错的问题数从 No Context 的 $356$ 道降到 Gold Context 的 $73$ 道，再降到 Iterative RAG 的 $21$ 道。按 1 至 4 跳分解，三种条件下的共同未解决数依次为 $76\rightarrow8\rightarrow0$、$93\rightarrow21\rightarrow4$、$85\rightarrow15\rightarrow4$ 和 $102\rightarrow29\rightarrow13$。

</div>

Iterative RAG 不只是提高个别模型的平均分，还显著压缩了所有模型都无法解决的共同失败集合，并完全消除了该集合中的 1 跳问题。失败并未随跳数简单单调增长：2 跳和 4 跳问题更集中，提示难度可能来自特定桥接关系或长链组合，而非仅由跳数决定。不过，“所有模型共同答错”的数量不等于每个模型的错误数，也不能据此识别具体失败原因。

<div class="result-source" markdown="1">

来源：第 4.5 节，图 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Totals drop sharply from 356 in No Context to 73 in Gold Context and to 21 in Iterative RAG. However, Iterative RAG eliminates a large share of these challenging items: unanswered counts fall from 76 → 8 → 0 (1 hop), 93 → 21 → 4 (2 hops), 85 → 15 → 4 (3 hops), and 102 → 29 → 13 (4 hops) across No Context, Gold, and Iterative RAG, respectively—evidence that stepwise retrieval with partial-answer state resolves both mid-chain gaps (hop 2) and deeper chains (hop 4).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验章节未明确报告数据集名称、总题量与划分、检索语料和检索器、解码设置、重复运行次数及答案判定规则。因而难以复现实验，也无法判断显著性检验是否充分处理了同一题目和同一模型之间的配对结构；所有结论仍需结合论文其余章节核验。
- Gold+CoT 只覆盖三个代表模型，且 Iterative RAG 同时改变检索次数、证据出现顺序、提示结构和状态维护方式，因此只能削弱“收益纯粹来自更多 token”的解释，尚不能定量归因于查询生成、部分答案状态或证据空间缩减中的某一个组件。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- No Context：不给外部证据，仅依赖模型参数中储存的知识。它衡量模型本身能回答多少问题，并为分析检索是否反而破坏原有正确知识提供参照。
- Gold Context：一次性向模型提供全部 oracle evidence，即预先确定的完整正确支持段落，不允许后续检索。它是关键的强静态基线，用来区分“拥有正确证据”与“能否按推理进度组织和利用证据”。
- Gold+CoT：仍一次性提供与 Gold Context 相同的 oracle evidence，但显式要求逐步推理，并禁止额外检索。该对照增加静态条件下的推理预算，用于检验 Iterative RAG 的提升是否只是输出更长或计算更多。

**实验想回答的问题**

- 在科学多跳问答中，将检索与逐步推理同步进行的 Iterative RAG，是否能稳定优于仅依赖参数记忆的 No Context，以及一次性提供完整正确证据的 Gold Context？
- Iterative RAG 的收益究竟来自更长的测试时计算，还是来自分阶段检索、维护部分答案状态并据此更新后续查询；同时，这种动态过程会带来哪些回退与参数记忆抑制风险？

**实验实现**

论文在 11 个模型上比较三种核心条件：No Context、一次性输入全部 oracle evidence 的 Gold Context，以及同步检索与推理的 Iterative RAG。Iterative RAG 最多允许五次检索，每一步生成查询和部分答案，并将部分答案作为跨步骤状态供后续检索与推理使用。除总体准确率和平均输出 token 外，作者还按题目划分参数记忆成功、仅静态理想证据成功、仅迭代检索成功和所有条件均失败四类，并统计 Gold 到 Iterative 的 recoveries 与 regressions。所给章节仅说明图 2 使用跨模型配对 $t$ 检验并标注显著性水平，未明确报告重复运行次数、解码参数、检索器及语料库配置、答案匹配规则或置信区间计算方式。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Gold+CoT：增加静态 oracle evidence 条件下的逐步推理预算，但不允许追加检索 | Gold+CoT 在三个代表模型上都优于普通 Gold Context，但仍低于 Iterative RAG。GPT-4o 的准确率为 $56.32\%\rightarrow78.08\%\rightarrow81.96\%$；Claude 3.7 Sonnet Standard 为 $68.13\%\rightarrow81.45\%\rightarrow84.49\%$。后者在 Gold+CoT 中平均生成 $909.96$ tokens，高于 Iterative RAG 的 $714.73$ tokens，却仍少 $3.04$ 个百分点。 | 该消融隔离了“更多推理计算”这一替代解释。Gold+CoT 大幅缩小差距，说明额外测试时推理本身确实重要；但即使静态条件生成更多 token，准确率仍未追上 Iterative RAG，支持作者关于“计算如何组织”比单纯延长生成更关键的主张。它仍不是完全严格的因果隔离，因为两种条件的交互结构和可见信息时间顺序不同，且只测试了三个模型。 | 第 4.1 节，表 2<br><span class="experiment-evidence">For GPT-4o, Gold+CoT increases accuracy from 56.32% to 78.08%, but Iterative RAG further improves performance to 81.96%. A similar pattern holds for Claude 3.7 Sonnet (Standard), where Gold+CoT reaches 81.45%, while Iterative RAG reaches 84.49%. Importantly, this improvement cannot be explained by token count alone: Claude 3.7 Sonnet (Standard) uses more output tokens in Gold+CoT than in Iterative RAG (909.96 vs. 714.73), yet still performs worse.</span> |
| 参数记忆抑制分析：比较 No Context 正确但 Iterative RAG 错误的题目 | 跨模型平均 $PSR$ 为 $6.7\%$；Mistral Large 2402 和 Llama 3.3 70B 的抑制率最高，分别为 $14.1\%$ 和 $11.7\%$，Claude 3.7 Sonnet 与 Claude Sonnet 4.5 最低，分别为 $2.7\%$ 和 $3.4\%$。 | 该分析检验引入检索是否会破坏模型原本正确的参数知识，而不是检验某个单独模块的移除效果。较高的 $PSR$ 表示模型更容易服从误导性检索片段或因早期错误证据偏离正确路径；较低的 $PSR$ 则表明冲突解决较稳健。由于论文未对检索噪声类型进行受控干预，权威偏差、噪声不确定性和推理中断仍是作者提出的解释性假设。 | 第 4.4 节，图 5<br><span class="experiment-evidence">As illustrated in Figure 5, the average suppression rate across models is 6.7%. However, the variance is significant: Mistral Large 2402 and Llama 3.3 70B show the highest vulnerability, with suppression rates of 14.1% and 11.7% respectively. Conversely, the Claude family demonstrates exceptional stability, with Claude 3.7 Sonnet achieving the lowest PSR of 2.7%, followed closely by Claude Sonnet 4.5 at 3.4%.</span> |

**定性案例**

- Mistral Large 2402 展示了净准确率可能掩盖逐题波动：Iterative RAG 能解决一批 Gold Context 下失败的困难问题，但也会丢失一批原本可由静态正确证据解决的问题。因此，其较小净增益并不表示迭代过程没有新增能力，而是新增成功与回退相互抵消。这个案例说明评估动态 RAG 时应同时报告 recoveries、regressions 和净变化，而不能只比较两个总体准确率。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Diagnostically evaluates iterative retrieval-augmented reasoning on scientific multi-hop question answering.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`eb7f3e04600e371ef4952157c8a3f991243d0cd3ff1768318ac4aa1420659b57`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
