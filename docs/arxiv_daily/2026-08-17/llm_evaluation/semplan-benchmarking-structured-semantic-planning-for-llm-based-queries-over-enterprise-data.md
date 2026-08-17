---
title: "[论文解读] SemPlan: Benchmarking Structured Semantic Planning for LLM-Based Queries over Enterprise Data"
description: "[arXiv 2608.13612][LLM 评测] SemPlan通过固定模型、数据、样例与评测规则，对比不同结构化约束程度的企业数据问答架构，以判断约束如何改变正确性、策略合规、失败类型、成本与稳定性之间的权衡。"
arxiv_id: "2608.13612"
announcement_date: "2026-08-17"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-17T02:00:38.758062+00:00"
source_sha256: "fbd4f594a3dfa94b3de4b8abe11db796477e87089df065ac566e7fedb37a1269"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "企业数据自然语言查询"
  - "结构化语义规划"
  - "文本到 SQL"
  - "LLM 架构评测"
  - "数据库治理"
  - "对话式澄清"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.13612</p>

# SemPlan: Benchmarking Structured Semantic Planning for LLM-Based Queries over Enterprise Data

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-17</span>
<span><strong>作者</strong> Bruno Santos Teixeira</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13612) · [PDF 下载](https://arxiv.org/pdf/2608.13612) · **关键词** 企业数据自然语言查询, 结构化语义规划, 文本到 SQL, LLM 架构评测, 数据库治理, 对话式澄清<br>


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

SemPlan通过固定模型、数据、样例与评测规则，对比不同结构化约束程度的企业数据问答架构，以判断约束如何改变正确性、策略合规、失败类型、成本与稳定性之间的权衡。

**不用术语来说**：用户用自然语言查询企业数据时，往往不会完整说明指标口径、时间范围、分组维度、权限边界或上下文。系统即使生成了语法正确的查询，也可能误解业务含义、违反访问策略、执行不受支持的操作，或在重复运行和多轮对话中给出不一致结果。因此，真正的问题不是单纯“能否生成 SQL”，而是怎样在语言模型与确定性软件之间合理分配理解、规划、校验和执行责任。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 构建一个确定生成的英⽂与巴西葡萄牙文合成企业数据问答基准，使多种系统架构能够在相同模型配置、数据库快照和评测规则下接受受控比较。
- 将直接生成 SQL、受限工具智能体、结构化语义请求加确定性规划，以及支持澄清与状态管理的语义规划纳入统一实验，系统考察正确性、策略行为、失败模式、成本、歧义处理、多轮状态一致性与重复运行稳定性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究的是面向企业结构化数据的自然语言查询系统。用户以自然语言提出涉及业务指标、维度、时间范围、权限边界或会话上下文的问题，系统需要将其转化为可执行且符合治理要求的行为。与仅生成语法正确的 SQL 不同，企业场景还要求结果在语义、权限、操作有效性、成本和稳定性方面正确；因此，本文将 LLM（大语言模型）与确定性规划、工具调用及执行组件之间的职责分配作为主要研究对象，并在固定模型、数据快照、测试案例和评测规则下比较不同架构。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**文本到 SQL**

文本到 SQL 是把自然语言问题转换为数据库查询语句的任务。SQL 语法正确并不保证查询使用了正确的业务指标、筛选条件或权限范围。

</div>
<div class="concept-item" markdown="1">

**结构化语义请求**

结构化语义请求是介于自然语言和 SQL 之间的、具有预定义字段和类型的中间表示，例如明确指定指标、维度、时间范围和操作类型。它把用户意图写成机器可检查的数据结构，使后续规划器能够按照固定规则生成查询或拒绝不支持的请求。

</div>
<div class="concept-item" markdown="1">

**确定性规划与治理**

确定性规划是指给定同一个结构化请求时，由规则或固定程序产生一致的查询计划，而不是让模型自由决定每一步。治理包括权限检查、禁止操作检查、输入验证、成本控制和可解释的失败分类，用于防止系统执行不安全或无效的行为。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定企业数据的数据库快照、自然语言查询以及在部分架构中提供的会话历史，系统需要输出查询答案、拒绝或澄清结果，并在允许时执行相应的数据访问行为。本文使用独立生成的合成企业领域和英葡双语案例，在相同模型配置与评测规则下比较四种端到端架构：直接生成 SQL、受限工具代理、生成结构化语义请求后进行确定性规划与执行，以及加入澄清和有状态语义计划的变体。问题的核心不是单一查询的语法转换，而是在请求可能含糊、越权、不可执行或需要多轮上下文时，同时满足答案正确性、政策行为、失败类型、成本和重复稳定性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D$**

企业数据库快照；它表示系统可以访问的结构化数据及其模式。

</div>
<div class="notation-item" markdown="1">

**$x$**

用户输入的自然语言查询，可能包含省略、歧义、时间范围或不被支持的操作。

</div>
<div class="notation-item" markdown="1">

**$r$**

系统生成的结构化语义请求或语义计划；它承载从 $x$ 中解析出的指标、维度、过滤条件、时间范围及所需操作。

</div>
<div class="notation-item" markdown="1">

**$y$**

系统最终返回的答案、澄清请求、拒绝结果或其他可评测输出。

</div>

</div>

**直接相关的工作**

- **Spider、SParC、CoSQL 与 BIRD**: 这些基准分别强调跨数据库模式泛化、上下文交互、对话式澄清与不可回答请求，以及大规模数据库内容、外部知识和效率问题。SemPlan 借鉴其数据库问答和对话评测方向，但进一步把企业治理、政策行为、成本、失败模式和重复稳定性纳入同一架构比较。
- **IRNet 与 PICARD**: IRNet 通过模式链接和 SemQL 中间表示，再确定性地推导 SQL；PICARD 在生成过程中逐步拒绝不符合语法约束的 token。它们共同支持使用中间结构或形式约束减少无效输出，但并不能直接证明约束越多，端到端答案正确率就一定越高。SemPlan 将这一问题扩展为 LLM 与确定性软件组件之间不同职责分配的比较。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

企业分析问题同时包含自然语言歧义、业务指标定义、隐含维度、时间范围、授权边界和会话上下文。只检查查询是否可执行，无法保证答案在业务语义和治理规则上正确；一旦系统误解请求，还可能产生错误结果、策略违规、无效操作、额外调用成本或不稳定输出。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **直接 SQL 生成**：语言模型直接把用户问题翻译成 SQL，再交给数据库执行。该路线把语义理解、字段选择、过滤条件和查询结构的大部分决策集中交给模型。
- **受约束的中间层方法**：系统让模型选择有限工具，或先输出带类型的语义表示，再由确定性程序完成规范化、规划、策略检查和执行；更进一步的方案还会通过澄清问题和显式状态处理歧义及多轮上下文。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- SQL 语法正确不等于业务语义正确或策略合规；直接生成路线缺少稳定的中间契约，模型对指标、时间范围或权限的误判可能直接进入执行阶段。
- 增加工具边界、类型约束、确定性规划或会话状态并不必然提升整体正确性：这些机制可能减少某类错误，却引入契约失败、错误澄清或状态不一致，而且已有讨论常把架构选择视为工程偏好，缺少控制其他变量后的多维实证比较。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作尚未充分回答：在保持语言模型、测试问题、数据库快照和评分规则一致时，不同程度的结构化约束究竟改善哪些行为、恶化哪些行为，以及这些变化是否值得其成本。尤其缺少同时覆盖答案正确性、策略行为、细分失败结果、歧义、多轮状态和重复性，并能将架构影响与模型差异区分开的受控基准。

</div>
<div markdown="1"><span>核心问题</span>

在基于语言模型的企业数据查询中，不同形式与不同程度的结构化约束，会如何权衡答案正确性、策略行为、失败模式、调用成本和重复运行稳定性？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把语言模型擅长但不稳定的自然语言理解，与规则明确、结果可复现的确定性软件分工：模型先表达用户想查什么，后续程序再按固定契约规划、校验并执行。通过逐步增加这种结构，并固定其余实验条件，可以观察约束是在阻止错误传播，还是仅把错误从 SQL 生成阶段转移到语义契约、澄清或状态管理阶段；因此研究目标是识别可解释的架构权衡，而不是预设“结构越多越好”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文不是提出并训练一个新的语言模型，而是在相同底座模型、输入语境和企业数据治理条件下，对四种“自然语言问题如何转成可执行分析”的系统架构进行受控比较。输入是双语企业分析问题以及区域设置、参考日期、受治理的数据视图和指标定义；核心自变量是结构化约束进入处理链的位置：A1由大语言模型直接生成SQL，A2让模型调用有类型约束的分析工具，A3让模型生成声明式的语义请求，再由确定性程序规范化并执行，A4则在A3基础上加入结构化会话状态、澄清结果和显式的PATCH/REPLACE更新语义。除A1外，模型都不能直接编写任意SQL；A3和A4中的SQL即使存在，也由应用程序根据已验证的语义计划生成。
端到端看，系统先把用户话语及必要上下文交给同一模型，再依据所属方案得到SQL、工具调用或$SemanticRequest$；随后由安全守卫、类型验证器或语义规范化器检查中间表示，确定性执行器才访问数据库并形成最终回答。该设计把“模型是否理解问题”与“谁负责生成可执行查询”分开考察：直观地说，A1让模型直接写查询，A2让模型使用限定功能的计算器，A3让模型填写一张结构化分析申请单，A4还让这张申请单能够在多轮对话中被澄清和局部修改。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造统一的模型输入

系统按方案使用各自独立冻结的提示词，但所有方案共享同一配置模型$gpt\text{-}5.6\text{-}luna$。输入只提供完成任务所需的目录、模式和语义上下文，不向A1泄露金标准SQL、计划或答案。

<div class="method-step__io" markdown="1">

**输入**：用户的企业分析问题；A1还明确接收区域设置、参考日期、紧凑的受治理视图模式和相关指标定义，A4额外接收先前的结构化状态。<br>
**输出**：一个面向对应方案的模型调用上下文。

</div>

**直观理解**：这一步相当于给四位受试者相同能力的语言模型和同一业务问题，但为其配备不同形式的操作规程。这样，结果差异主要反映接口与执行架构，而不是底座模型不同。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 生成受方案约束的中间表示

A1输出包含SQL或类型化拒答的严格JSON；A2输出受严格参数模式和规范目录标识符约束的有限工具调用；A3输出包含操作、指标、维度、过滤器、时间粒度、排序、数量上限、比较字段、澄清字段和置信度的严格$SemanticRequest$；A4输出语义请求、澄清结果或带PATCH/REPLACE语义的状态操作。

<div class="method-step__io" markdown="1">

**输入**：统一上下文以及用户话语；A4同时读取既有结构化会话状态。<br>
**输出**：模型生成的SQL、类型化工具调用、语义请求，或拒答/澄清/状态更新结果。

</div>

**直观理解**：四种方案的关键区别不是模型是否参与，而是模型被允许写到哪一层。结构越强，模型越像是在填写预定义表单，而不是自行决定数据库查询的完整写法。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 验证、规范化与状态处理

A1的SQL必须通过解析、抽象语法树允许列表、复杂度限制、只读授权、语句超时和行数限制；A2检查工具名、调用数量及参数模式；A3/A4验证标识符和类型、解析文档化语义规则，并把请求编译为可执行语义计划。A4还按兼容性规则处理PATCH/REPLACE：PATCH只修改显式指定字段，REPLACE替换状态，超出范围的轮次在未重置时保留原状态。

<div class="method-step__io" markdown="1">

**输入**：上一步产生的方案特定中间表示，以及受治理的模式、目录、类型规则和A4历史状态。<br>
**输出**：获准执行的SQL、合法工具操作或经过规范化的语义计划；不合法输入则形成错误、拒答或澄清结果。

</div>

**直观理解**：这一层是模型与数据库之间的检查站：它把自由文本决定转成可检查的结构，并阻止越权、类型错误或过于复杂的操作。A4的PATCH类似只改申请单中点名的栏目，避免一次追问意外擦除其他条件。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 确定性编译、执行与返回

A1执行通过守卫的模型生成SQL；A2由确定性执行器实现聚合、排名、期间比较、预算比较、合同状态和字段描述等工具操作；A3/A4由受治理软件把语义计划编译为参数化SQL或等价的确定性算子调用，再访问数据库。执行结果随后用于生成最终回答，同时记录无效、执行失败、拒答、澄清和政策相关结局。

<div class="method-step__io" markdown="1">

**输入**：通过检查的查询或计划，以及企业数据库。<br>
**输出**：最终分析回答，或明确的拒答、澄清、越界及执行错误状态。

</div>

**直观理解**：A3和A4中，模型决定“想分析什么”，程序决定“具体怎样查数据库”。这种职责分离旨在让查询生成更可控，但它本身并不保证模型选择的指标、过滤条件或澄清行为一定正确。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。原文所述方法没有训练或微调新模型，也未给出可优化的中心损失函数；四种方案均调用同一个已配置模型，研究对象是推理时接口、约束、规范化和执行责任的分配。论文预先冻结研究问题与方向性假设，并在隐藏评测后保留混合或负面发现，但这些假设属于实验检验标准，不是梯度优化目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 方案特定的模型接口层**

A1、A2、A3和A4分别把模型输出空间限制为严格JSON SQL/拒答、类型化工具调用、$SemanticRequest$以及带澄清和状态操作的扩展语义请求。各方案提示词独立冻结，并以SHA-256标识固定版本，从而减少评测后调整提示词造成的比较偏差。

> 直观理解：该模块决定模型能用什么“语言”表达意图。直接SQL最自由，工具和语义请求更受约束；论文正是通过改变这一接口来检验结构化规划是否比直接生成查询更可靠。

**2. 确定性验证与执行层**

A1采用SQL解析与安全守卫；A2将合法工具调用映射到预实现的分析操作；A3/A4执行标识符和类型验证、语义规则解析、计划编译以及参数化SQL或等价算子执行。该层不再让语言模型自由改写执行逻辑，因此相同合法计划应对应可重复的数据库操作。

> 直观理解：它把概率性的语言模型与真实数据库隔开，类似先审核申请单，再由固定业务程序办理。这样能减少任意SQL带来的直接风险，也便于定位错误究竟出在意图理解、结构验证还是数据库执行。

**3. A4澄清与结构化状态管理器**

A4在A3接口上增加先前状态、类型化澄清结局以及显式PATCH/REPLACE操作，并通过兼容性规则控制字段更新。PATCH仅更新模型明确改变的字段，越界轮次默认保留状态，只有REPLACE或重置才进行整体替换或清除。

> 直观理解：该模块试图解决多轮提问中的条件继承问题，例如用户说“再按地区拆分”时，应保留原指标和时间范围，只新增地区维度。它是待检验的结构设计，不应仅凭架构描述推断其实际澄清或多轮正确率更高。

**训练与推理**

训练阶段不适用：节选没有报告针对A1–A4的数据训练、参数更新或偏好优化。推理时，每个问题进入对应方案的冻结提示词；模型以低推理强度运行，并在1,200个输出词元上限内生成方案规定的中间表示。A1随后由SQL守卫审核模型SQL；A2把有限且类型正确的工具调用交给确定性执行器；A3验证并规范化$SemanticRequest$，再编译为参数化SQL或确定性算子；A4除执行A3流程外，还根据既有状态决定请求、澄清、PATCH或REPLACE，并在状态规范化后执行。所有数据库访问都经过受治理的软件边界，但不同方案可能在模型生成、验证、澄清或执行阶段产生拒答、越界和错误。

**复现信息**

为保证架构比较可解释，四种方案统一使用$gpt\text{-}5.6\text{-}luna$、提供方中立的OpenAI适配器、低推理强度和1,200词元输出上限；提示词按方案独立冻结，原文还报告了各方案的SHA-256摘要以确认版本。A1必须实施SQL解析、抽象语法树允许列表、复杂度限制、只读授权、语句超时和行数限制；A2必须限制可用工具、工具参数及最多可组合的调用次数；A3/A4必须使用规范目录标识符、严格类型模式、文档化语义规则和确定性编译器。节选未明确给出具体数据库引擎、超时数值、行数上限、工具调用上限、完整$SemanticRequest$模式或状态兼容规则，因此仅凭所给章节不能完整复现这些底层配置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Northstar Commerce 合成企业分析域：包含客户、产品、订单、支付、费用、预算、供应商、合同和日历维度；数据由确定性种子和已记录不变量生成，参考环境使用受治理的 PostgreSQL 视图与只读执行策略。其作用是提供可重复、可审计的企业查询数据库。
- SemPlan Benchmark 1.0.0-rc.2：共 1,800 个案例，其中 en-US 900 个、pt-BR 900 个；划分为 development 300、validation 300、public test 500、hidden test 300、multi-turn 200 和 adversarial 200。案例覆盖查找、分组聚合、排名、比较、方差、趋势、份额或比率、过滤、合同状态、歧义、范围外、多轮和对抗性查询。
- 冻结科学评测子集：由 public test、hidden test、multi-turn 和 adversarial 组成，共 1,200 个案例。development 与 validation 不参与主要科学比较；每个案例在 A1–A4 下各运行一次，形成 4,800 条主要记录，另从中确定性抽取 150 个案例并为每种方法额外重复两次，形成 1,200 条稳定性记录。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**绝对正确性**

衡量每个案例是否得到正确的最终结果；原文说明该指标在成对显著性检验之前报告。 （越高越好，因为它直接表示正确完成企业查询的比例。）

</div>
<div class="metric-item" markdown="1">

**终止 ERROR 结果与类型化失败**

ERROR 表示案例未成功完成；类型化失败进一步区分 EXECUTION_FAILED、OUTPUT_SCHEMA_INVALID、POLICY_VIOLATION、CATALOG_UNKNOWN_ID 和 CFG_INVALID 等失败面。 （ERROR 和失败计数越低通常越好，但必须结合失败类型解释；某种方法可能减少总体错误，却增加另一类契约或执行失败。）

</div>
<div class="metric-item" markdown="1">

**平均 API 成本**

衡量每条主要记录的提供商 API 费用；它由提供商使用量与价格表记录得到，不等于总拥有成本。 （越低越好，但不能据此推断基础设施、工程时间或未来价格下的总成本。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四种方法在冻结科学子集上的总体终止结果

<div class="result-value" markdown="1">

A1 产生 372 个主要 ERROR 结果，A2 产生 747 个，A3 产生 727 个，A4 产生 769 个。就总体终止错误数量而言，A1 最少，但该结果不能单独说明 A1 的查询正确性最高，因为错误数量与拒答、错误答案和其他终止状态的组成需要分开分析。

</div>

这项比较测试四种方法完成请求的总体稳定程度。A1 的 ERROR 较少，说明它在该冻结设置下较少进入记录为 ERROR 的终止状态；但作者明确将不同失败面视为科学结果，因此不能把较少 ERROR 直接解释为方法全面优越，也不能据此判断每次非 ERROR 都是正确答案。

<div class="result-source" markdown="1">

来源：第 8 节 Failure Analysis

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A1 produced 372 primary ERROR outcomes, compared with 747 for A2, 727 for A3, and 769 for A4.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 失败类型与错误迁移

<div class="result-value" markdown="1">

在全部 6,000 条科学记录中，EXECUTION_FAILED 为 1,762，OUTPUT_SCHEMA_INVALID 为 1,051，POLICY_VIOLATION 为 368，CATALOG_UNKNOWN_ID 为 78，CFG_INVALID 为 24；主要 4,800 条记录中的对应数量分别为 1,402、845、287、65 和 16。

</div>

这项结果测试方法是否只是把错误从一种形式转移到另一种形式。执行失败表示请求到达受治理执行层后违反数据库或执行规则；输出模式失败表示没有满足严格输出契约；政策违反表示被保护层拒绝。因而总体错误数的变化必须结合错误类别阅读，不能简单称为“错误消失”。原文也指出，汇总结果不足以证明某一错误代码由某个具体模块单独造成。

<div class="result-source" markdown="1">

来源：第 8 节 Failure Analysis，Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across all 6,000 scientific records, the recorded error codes are EXECUTION_FAILED (1,762), OUTPUT_SCHEMA_INVALID (1,051), POLICY_VIOLATION (368), CATALOG_UNKNOWN_ID (78), and CFG_INVALID (24).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 正确性与 API 成本的权衡

<div class="result-value" markdown="1">

A3 被作者描述为正确性最高，A4 被描述为平均 API 成本最低；A1、A2、A3、A4 的每条主要记录平均成本分别为 USD 0.000918、0.000927、0.000512 和 0.000469。A3 相对 A2 的配对平均成本差为 -USD 0.000415，A4 相对 A2 为 -USD 0.000459。

</div>

该结果说明更低成本与更高正确性并不必然由同一种方法同时实现：A3 在正确性上占优，A4 在冻结模型和价格表下最省 API 费用。它只支持当前模型、提示词、案例和价格配置下的观测性比较，不足以推出长期总成本、其他模型上的表现，或正确性与成本之间的普遍因果关系。

<div class="result-source" markdown="1">

来源：第 10 节 Cost and Operational Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Mean cost per primary record is USD 0.000918 for A1, 0.000927 for A2, 0.000512 for A3, and 0.000469 for A4.

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

- A1：实验中的第一种完整方法。原文所给摘录未明确报告其方法名称或具体组件，因此这里只能将其作为固定实验条件下的比较参照。
- A2：实验中的第二种完整方法。原文所给摘录未明确报告其方法名称或具体组件。
- A3：实验中的第三种完整方法。原文所给摘录未明确报告其方法名称或具体组件；结果部分指出它具有最高正确性。
- A4：实验中的第四种完整方法。原文所给摘录未明确报告其方法名称或具体组件；结果部分指出它的平均 API 成本最低。

**实验想回答的问题**

- 在固定的企业数据、模型配置和提示词条件下，四种方法 A1–A4 在 1,200 个科学评测案例上的正确性、政策合规性与终止结果是否存在差异？
- 增加结构化语义或工具接口是否改变系统的失败类型、重复可复现性与 API 成本，而不仅仅是改变总体错误数量？

**实验实现**

所有主要比较使用相同的 benchmark 版本、案例集合、数据库快照、模型配置和各方法冻结提示词。模型为 gpt-5.6-luna，推理级别为 low，最大输出为 1,200；主要设计是每种方法处理 1,200 个案例各一次。二元结果使用按案例对齐的 McNemar 检验和带 95% 置信区间的配对风险差，并对预先指定的主要比较族进行 Holm–Bonferroni 校正；偏态连续结果（例如 API 成本）使用配对自助法对比。实验区分提供商、传输、基础设施和模型质量失败。模型质量失败在系统提供足以分类的证据时保留为科学结果，而不是当作缺失值。延迟虽预先指定，但因捕获的类型化失败记录为零延迟且在方法间分布不均，被排除在主要结论之外；重复运行只用于评估方法内重复性，不增加主要样本量。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 重复运行稳定性分析：从 1,200 个案例中确定性抽取 150 个案例，每种方法额外运行两次 | 共产生 1,200 条稳定性记录，用于分析方法内重复性；原文所给摘录未明确报告各方法的稳定性数值或显著性结果。 | 该设计隔离模型或系统重复运行时的波动，测试同一方法在相同案例上的结果是否可复现。由于重复记录不计入主要样本，它不会人为扩大主要比较的样本量；但没有具体稳定性统计量，无法判断哪种方法最稳定。 | 第 6 节 Experimental Setup<br><span class="experiment-evidence">A deterministic stratified subset of 150 cases is then executed two additional times per approach, producing 1,200 stability records.</span> |
| 延迟结果的审计性排除 | 延迟被预先指定但未纳入主要结论，因为捕获的类型化失败记录为零延迟，且这些失败在不同方法间分布不均；原文未提供可用于公平比较的延迟数值。 | 这不是改变模型组件的传统消融，而是对一个实验变量进行有效性检查。若失败请求被记录为零延迟，直接计算中位延迟会系统性偏低，并且不同方法的失败比例不同，比较就不再代表完整端到端延迟。排除延迟提高了解释的谨慎性，但也意味着实验没有给出主要延迟结论。 | 第 6 节 Experimental Setup<br><span class="experiment-evidence">Consequently, the resulting medians are not comparable as a clean end-to-end latency measure.</span> |

**定性案例**

- 原文给出一个双语示例而非结果性案例研究：英文查询“What was net revenue for consumer customers in the North region through the online channel in January 2022?”与巴西葡萄牙语查询表达相同语义，规范请求识别 net_revenue、地区、渠道、客户细分过滤条件和时间窗口。它主要测试跨语言表面表达能否映射到同一规范语义请求；原文明确说明主要评测使用冻结案例工件，而不是手工改写的示例，因此不能把该示例当作定量性能结果。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces a benchmark for evaluating structured semantic planning by LLMs over enterprise data.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`fbd4f594a3dfa94b3de4b8abe11db796477e87089df065ac566e7fedb37a1269`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
