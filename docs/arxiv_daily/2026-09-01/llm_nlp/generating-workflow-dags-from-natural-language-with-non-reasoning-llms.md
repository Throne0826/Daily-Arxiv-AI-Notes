---
title: "[论文解读] Generating Workflow DAGs from Natural Language with Non-Reasoning LLMs"
description: "[arXiv 2608.30250][LLM 其他] 论文将自然语言路由规则的语义理解与工作流图的组合构造分离，使低成本、非推理型大语言模型只生成紧凑中间表示，再由确定性编译器生成可执行的工作流有向无环图。"
arxiv_id: "2608.30250"
announcement_date: "2026-09-01"
primary_category: "llm_nlp"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:47:52.654977+00:00"
source_sha256: "75aa2ba675dd3067480b43a1bcc047442a58fc3e0498d96de88b6c1d28fea239"
tags:
  - "LLM 其他"
  - "LLM Reasoning"
  - "自然语言到工作流 DAG"
  - "神经符号分解"
  - "非推理型大语言模型"
  - "中间表示编译"
  - "结构化生成"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 其他 · arXiv 2608.30250</p>

# Generating Workflow DAGs from Natural Language with Non-Reasoning LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Anand Iyer, Bhanu Khetharpal, Srinivas Upadhya, Ramkumar Rajagopal</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Microsoft</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30250v1) · [PDF 下载](https://arxiv.org/pdf/2608.30250v1) · **关键词** 自然语言到工作流 DAG, 神经符号分解, 非推理型大语言模型, 中间表示编译, 结构化生成<br>


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

论文将自然语言路由规则的语义理解与工作流图的组合构造分离，使低成本、非推理型大语言模型只生成紧凑中间表示，再由确定性编译器生成可执行的工作流有向无环图。

**不用术语来说**：企业联络中心需要把管理员写下的路由要求转换成平台可执行的 JSON 工作流，例如判断客户地区、周期性提高排队优先级，并在超时后结束会话。目标不是简单的动作清单，而是包含条件、并行分支、先命中先执行的回退链以及动作依赖关系的图；任何条件分组、属性值或连接关系错误都可能改变实际业务行为。人工编写要求熟悉平台且容易出错，而交互式产品又不能为每条规则长期承担高成本推理模型的延迟与令牌开销。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出“发射密度瓶颈”这一诊断：较强模型通常能够识别自然语言规则需要哪些节点，但在一次生成大量相互依赖节点时，容易遗漏或错配节点属性、依赖关系和布尔条件分组，因此主要故障位于复杂结构的输出阶段，而非规则理解阶段。
- 作者据此提出神经—符号分解架构：由学习式注册表选择器缩小当前规则所需的动作与条件词汇，由非推理型大语言模型生成紧凑中间表示，再由确定性编译器完成组合式图构造和 JSON 序列化；其目标是在保留少样本示例作用的同时，降低提示成本并保证结构可编译。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于自然语言到可执行结构的生成研究，具体聚焦企业联络中心中的工作流图生成。系统需要把业务管理员撰写的自然语言路由规则转换为商业路由平台可执行的 JSON 工作流；该工作流不是简单的动作列表，而是由条件、动作、执行顺序和并行分支共同构成的有向无环图（DAG）。因此，问题同时涉及语义解析、结构化输出、神经符号系统和程序编译：语言模型负责理解规则并提出结构化表示，确定性编译器负责把该表示稳定地转换为合法平台配置。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**有向无环图（DAG）**

DAG 是由节点和有向边组成、且沿边行进不会回到原节点的图。本文用节点表示触发器、条件或动作，用边表示条件门控、依赖关系和命中优先的执行顺序。

</div>
<div class="concept-item" markdown="1">

**神经符号分解**

神经符号分解把任务拆成两部分：语言模型处理自然语言中的含义，符号程序按照明确规则完成结构构造、执行或验证。这样可以避免让模型一次性生成所有相互依赖的图细节。

</div>
<div class="concept-item" markdown="1">

**中间表示（IR）**

中间表示是连接模型输出和最终平台格式的紧凑、受约束表示。模型只需描述规则中涉及的对象和关系，编译器再依据固定规则生成完整工作流 JSON，从而把容易出错的组合式图构造移出语言模型。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是业务管理员用自然语言描述的联络中心路由规则，例如指定客户区域、等待条件、优先级变化、计时器和未解决时的终止动作。输出是商业路由平台 JSON 方言中的可执行工作流 DAG；图中包含条件动作、并行分支、命中优先的后备链以及每个分支上的布尔谓词。典型规则可能要求在队列等待期间反复提高优先级，并在达到时间阈值后结束会话，因此输出必须同时正确表达节点、属性、布尔分组和依赖边。任务假设平台的动作与条件词汇由注册表定义，且生成结果在部署前仍由人工审核和验证；研究目标是在保证结构合法性的同时，提高复杂规则的一次生成准确率，并控制交互式应用中的每条规则提示词成本。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D$**

目标工作流有向无环图，由节点集合和有向边集合组成。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{DAG}$**

有向无环图（directed acyclic graph）的缩写，表示工作流中不存在循环依赖。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{IR}$**

中间表示（intermediate representation），是语言模型输出与最终平台 JSON 之间的紧凑结构化接口。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{JSON}$**

最终工作流所采用的结构化数据格式；本文特指商业路由平台使用的 JSON 方言。

</div>

</div>

**直接相关的工作**

- **语义解析与自然语言到结构化输出（以 text-to-SQL 为代表）**: 这类研究同样把自然语言映射为可执行或严格结构化的对象，通常重视精确匹配和跨模式泛化。本文继承其结构化生成目标，但将输出对象扩展为包含并行分支、条件门控和依赖关系的工作流 DAG，并通过后端确定性编译保证格式有效。
- **神经符号生成与 LLM 驱动的工作流生成**: 相关方法通常让语言模型提出符号表示，再由执行器或验证器处理；本文具体采用 `$\mathrm{IR}\rightarrow\mathrm{JSON}$` 的编译分工。与从已有结构化计划开始的工作流系统不同，本文将自然语言到图结构的解析作为核心难点，并使用不会失败的确定性编译器，而不是反复生成、验证和重生成。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现有商业联络中心的路由规则最终必须落实为可执行 JSON 图，其中节点表示转移队列、提高优先级、通知主管或提供回呼等动作，边表示条件门控和执行依赖。生产规则可能组合多达 15 个条件分支，而且单个分支还可触发多个动作，形成高密度分支网格。由于一次错误的属性、条件分组或遗漏分支就会改变工作流行为，生成结果仍需人工审核；因此，提高首次生成正确率可直接减少修订与重新生成次数。同时，该转换器位于交互式创作流程中，必须控制模型推理成本和每条规则的提示长度。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **单体提示生成**：把平台支持的动作、条件、输出模式以及各类少样本示例集中放入一个大型提示，让大语言模型从结构化模板规则直接一次性生成完整 JSON 工作流图。论文指出，少样本示例是该方案准确率的重要来源，但模型也必须同时承担语义解释、节点选择、属性填写、布尔分组、边连接和 JSON 序列化。
- **直接使用扩展推理模型**：依靠能力更强、会执行较长内部推理的模型处理复杂条件和图依赖，以提升完整工作流的生成质量。该路线主要通过增加模型能力缓解结构生成错误，而不是改变任务分工或把图构造交给确定性程序。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单体提示难以随平台词汇持续扩展：每增加一种业务场景，就要加入新的动作、条件和场景示例，并在每次请求中携带大量与当前规则无关的上下文。这既增加令牌成本，也会分散模型对相关定义与示例的注意力；更关键的是，模型在同一轮中输出的相互依赖节点越多，就越容易错配属性或破坏布尔结构。
- 扩展推理模型虽可提供更高质量，但其成本和延迟不适合大规模、交互式的企业规则创作。作者还强调，单纯扩大模型并未直接针对故障机制：问题并非模型普遍读不懂规则，而是它在一次性发射高密度结构时容易丢失细节，因此仅依赖更昂贵模型不能形成经济且可扩展的工程方案。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种面向自然语言到工作流图的架构，能够先区分“理解规则”与“发射复杂图结构”两类能力，再把容易遗漏、但可由规则程序完成的组合式图构造移出模型；该架构还需随平台动作和条件词汇增长而保持提示聚焦，并在不依赖昂贵扩展推理的前提下达到生产相关的语义质量与结构有效性。

</div>
<div markdown="1"><span>核心问题</span>

能否通过学习式词汇筛选、紧凑中间表示和确定性编译，将低成本非推理型大语言模型限制在其擅长的自然语言解释与必要元素选择上，从而可靠生成包含并行分支、回退链、布尔谓词和动作依赖的可执行工作流有向无环图，并缩小其与强推理模型之间的质量差距？

</div>
<div markdown="1"><span>作者直觉</span>

如果模型已经能正确判断规则需要哪些动作和条件，那么继续要求它逐节点填写重复属性、保持跨节点引用一致、正确嵌套布尔表达式并输出合法 JSON，相当于让语言模型兼任脆弱的图编译器。更稳妥的分工是让模型只写一份短而语义明确的“施工说明”，再由确定性程序按固定规则展开节点、连接边并序列化；注册表选择器则像先从庞大的零件库中取出本次真正需要的零件，使模型仍能看到相关定义和示例，而不必每次阅读整个平台词汇。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法将自然语言路由规则转换为可执行的工作流有向无环图（DAG）。系统采用“学习式注册表选择器 + 非推理型大语言模型生成中间表示（IR）+ 确定性编译器”的分工：模型负责理解规则意图、识别分支和值，编译器负责把组合扩展、依赖连接、布尔结构和目标 JSON 的序列化交给精确的程序处理。直观地说，模型先回答“需要哪些零件、它们表达什么”，再用一种较简单的草稿格式描述流程，最后由编译器按照平台规则组装成不会出现语法错误的正式工作流。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 注册表检索与选择

前端大语言模型读取规则，从注册表中选择所需的事件、动作、条件和示例 ID，并输出一个小型 JSON 选择结果；注册表中的消歧元数据用于区分容易混淆的条件。选择结果再用于构造后续生成提示。

<div class="method-step__io" markdown="1">

**输入**：一条自然语言规则，以及包含事件类型、动作类型、条件类型、数据类型、运算符和示例 JSON 的版本化注册表。<br>
**输出**：与当前规则相关的精简注册表子集和对应示例集合。

</div>

**直观理解**：这一步像先从大型零件库中挑出本题真正会用到的零件，避免每次都把整个目录塞给模型。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自然语言到中间表示生成

非推理型大语言模型识别触发事件、分支、动作、条件值及依赖关系，并将其写成低语法负担的 IR，而不是直接生成最终平台 JSON。IR 表达工作流 DAG 的节点、条件和分支关系，同时尽量让模型只写一次值列表。

<div class="method-step__io" markdown="1">

**输入**：原始自然语言规则、选择器返回的注册表子集及示例，以及用于描述工作流的 YAML 风格中间表示（IR）提示。<br>
**输出**：描述目标工作流意图和图结构的 IR 文本。

</div>

**直观理解**：模型先写一份结构较简单的流程草稿；相比直接手写大量带括号和引号的 JSON，这更像填写清晰的表格，减少格式性出错。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### IR 到目标工作流编译

确定性编译器解析 IR，执行交叉乘积、命中优先链、残余分支处理，以及集合条件的布尔展开，并生成平台所需的触发器、动作、谓词和依赖边。编译器将命中优先分支编码为 skip-on-match 依赖，将并行分支保持为独立路径，并为“其他所有情况”分支保留空谓词。

<div class="method-step__io" markdown="1">

**输入**：模型生成的 IR、完整或筛选后的注册表，以及平台要求的目标 JSON schema。<br>
**输出**：语法有效且符合平台方言的工作流 JSON，其中包含事件触发块、动作 DAG、每个动作的布尔谓词和依赖边。

</div>

**直观理解**：编译器像一台严格的装配机：模型给出意图和零件清单后，程序负责按固定规则复制组合、连接分支并补齐平台格式，因此不会要求模型手工完成所有机械性展开。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 验证与部署推理

对编译结果进行格式和结构检查，然后将其交付平台执行或部署；由于最终 JSON 由确定性编译器生成，系统把主要剩余风险集中在语义完整性、属性值精确性和注册表选择召回，而不是 JSON 语法。

<div class="method-step__io" markdown="1">

**输入**：编译得到的工作流 JSON，以及目标平台的 schema 或部署接口。<br>
**输出**：可部署的工作流配置，或带有语义错误信息的待修订结果。

</div>

**直观理解**：最后像上线前的自动验收：程序先确认文件格式和连接方式正确，再交给平台；若仍有问题，主要是模型理解或填写内容不完整，而不是括号、字段排列等低层错误。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确给出统一的参数化训练目标或损失函数。方法依赖现成的非推理型大语言模型进行提示式生成；选择器与 IR 生成器的具体训练数据、参数更新目标和优化算法在所给章节中未明确报告，因此不能据此补写监督损失或强化学习目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 版本化注册表与学习式选择器**

注册表是事件、动作、条件、数据类型、运算符及场景示例的单一事实来源。选择器以规则为输入，输出相关条目和示例 ID；其提示还可由未来的相似度候选生成器预筛选，以便在注册表扩大时控制选择器输入规模。

> 直观理解：注册表把平台词汇和示例集中管理，新增能力时主要增加条目而不是修改代码；选择器只取当前规则需要的知识，使后续模型面对较小、较相关的上下文。

**2. 低语法负担的 IR 生成器**

系统将模型任务定义为自然语言到 YAML 实例化的 IR，而不是自然语言到最终 JSON。该表示保留工作流意图、节点、条件和依赖信息，并把可由程序确定的组合扩展留给后续编译阶段。

> 直观理解：模型擅长理解文字，但不一定擅长一次性准确写出许多相互依赖的结构；IR 让它少写格式，多表达意思。

**3. 目标无关的确定性编译器**

编译器将 IR 翻译为平台特定的工作流 JSON，并执行交叉乘积、命中优先链、残余分支和列表条件的确定性展开。它通过固定规则处理布尔集合展开，例如将排除多个值的条件转换为相应的合取结构，从而避免模型重复书写同一列表和复杂依赖。

> 直观理解：编译器把容易机械出错、但规则明确的工作交给程序完成；同时，目标无关设计使更换工作流类型或 JSON 方言时主要调整编译器和注册表，而不必重新设计模型提示。

**训练与推理**

推理时，系统先向选择器提供自然语言规则和注册表，使其返回相关事件、动作、条件及示例；随后将筛选后的注册表内容与规则共同放入 IR 生成提示，由大语言模型产生 YAML 风格 IR。确定性编译器再读取 IR，完成分支组合、依赖连接、布尔条件展开和目标 JSON 序列化，最后进行平台层面的格式或结构验证。论文还定义了不使用选择器和编译器的单体基线、只使用选择器直接生成 JSON 的配置、只使用 IR 与编译器的配置，以及同时使用两者的完整系统；这些配置用于区分上下文缩减和确定性编译各自的作用。

**复现信息**

复现或公平解读时，关键设定包括：注册表必须同时保存平台词汇及与场景对应的示例 JSON；输入规则可能包含拼写错误和非英语实体值，但完整工作流结构由模板生成并具有确定真值；规则覆盖七类结构，分支数为每条规则一到十五个，数据集共六百三十五条规则。编译器需要支持触发器、动作节点、每动作布尔谓词、依赖边、skip-on-match 命中优先链、并行分支和空谓词残余分支；原文未明确报告选择器或 IR 生成器的具体训练样本构造、参数、优化器和解码超参数。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 制造的合成规则基准：共 $635$ 条业务路由规则；每条规则对应一个目标工作流 DAG，包含条件动作、并行分支、命中优先的回退链以及分支级布尔谓词。该数据集用于统一比较所有模型和配置，所有结果均覆盖全部 $635$ 条规则。
- 训练或调参数据：原文未明确报告独立训练集、验证集或测试集划分。选择器的调优方式仅明确为：Selector→JSON 使用了与 Selector+IR 独立调优的选择器，并在选择时传入更完整的注册表。
- 密度诊断数据或划分：原文仅说明第 5.3 节包含 density curve，并且条件准确率由程序直接依据真实工作流计算；原文未明确报告该曲线是否使用独立数据划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Cond%（exact-match condition accuracy）**

程序将生成的工作流条件树与真实工作流逐条比较，只有条件树完全匹配才算正确；该指标不依赖 LLM 判断，重点衡量布尔条件及其分组是否被准确配置。 （越高越好，因为更高表示生成的条件逻辑与目标工作流完全一致。）

</div>
<div class="metric-item" markdown="1">

**AI%（LLM-as-judge validity）**

由 Claude Opus 4.6 在固定规则书下判断生成工作流的语义有效性；同一规则书和评审模型用于所有配置。 （越高越好，表示从整体语义和业务可执行性看，生成结果更符合目标规则。它可能受评审模型偏好影响，因此不能替代程序化指标。）

</div>
<div class="metric-item" markdown="1">

**JSON validity**

程序检查输出是否为可解析且符合目标格式的 JSON；它只检验形式合法性，不等于节点、参数或条件语义正确。 （越高越好，因为无效 JSON 无法直接交给后续工作流平台执行；但接近 $100\%$ 也不能证明工作流内容正确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四种配置在四个模型上的总体比较，重点看 GPT-5.3-chat 与完整 Selector+IR 流程。

<div class="result-value" markdown="1">

Selector+IR 在 GPT-5.3-chat 上达到 Cond% $82.2$、AI% $80.6$，相较 Monolithic 的 Cond% $56.5$、AI% $56.4$，分别提高 $25.7$ 和 $24.2$ 个百分点。该配置也在 GPT-4.1 上取得 Cond% $78.1$、AI% $64.6$，在 GPT-5.2 上取得 $89.6$、$84.1$，在 Opus 4.6 上取得 $88.0$、$88.8$。

</div>

这说明把相关注册表筛选与 IR—编译器式流程结合起来，能够显著缓解非推理模型在一次输出大量相互依赖节点时的结构配置困难。GPT-5.3-chat 的提升主要证明该方法对原本容易漏生成动作的模型有效；它不证明非推理模型在所有任务上都超过推理模型，因为 GPT-5.2 和 Opus 4.6 在部分配置下仍有更高的条件或评审分数。

<div class="result-source" markdown="1">

来源：Table 1, Section 5.1；表头为“Cond% / AI%”，列依次为 GPT-4.1、GPT-5.3-chat、GPT-5.2、Opus 4.6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Selector+IR 78.1 / 64.6 82.2 / 80.6 89.6 / 84.1 88.0 / 88.8

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 非推理方法与推理模型参考线的桥接比较。

<div class="result-value" markdown="1">

GPT-5.3-chat 使用 Selector+IR 时 AI% 为 $80.6$，GPT-5.2 使用 Monolithic 时 AI% 为 $79.8$；两者差异为 $0.8$ 个百分点。原文摘要进一步声称，GPT-5.3-chat 的改进在评审有效性上达到与推理模型开箱即用质量的统计等价，但仍存在约 $8$ 个百分点的 frontier gap。

</div>

在固定 Opus 评审规则下，结构化流程让较便宜的非推理模型达到与 GPT-5.2 单体提示接近的语义有效性，支持“把组合工作移出模型”这一设计判断。这里的“统计等价”不是说两者完全相同，也不表示 Selector+IR 已达到最强模型的上限；摘要明确保留了约 $8$ 个百分点的前沿差距。该结果还应结合不同模型价格、延迟和提示长度，而不能只按单一 AI% 排名。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On GPT-5.3-chat, the method improves judge validity by 24 percentage points and achieves statistical equivalence to a reasoning model's out-of-the-box quality, although an approximately 8-point frontier gap remains.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 条件逻辑的独立验证与生成密度诊断。

<div class="result-value" markdown="1">

实验将 Cond% 定义为完全匹配条件树的程序化指标，并报告所有配置均覆盖 $635$ 条规则；摘要指出，模型通常能高准确率选择正确图节点，但随着一次输出中相互依赖节点数量增加，属性和布尔分组错误会增加。因而，条件逻辑的主要瓶颈被定位为 emission density，而不是单纯的节点识别。

</div>

该结果把“模型知道应该有哪些节点”和“模型能在一个长输出中正确连接并配置这些节点”区分开来。它支持使用紧凑 IR 和确定性编译器承接组合式图构造：模型只需提出结构化意图，编译器再按规则生成最终 DAG。由于所给摘录没有列出第 5.3 节 density curve 的具体数值或图表行，不能据此声称误差随节点数呈某个精确函数关系。

<div class="result-source" markdown="1">

来源：Abstract；相关条件精确率定义和程序化评估见 Section 5.1，密度曲线见 Section 5.3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

our central diagnostic is an emission-density bottleneck: on a 635-rule benchmark of manufactured synthetic data, models select the correct graph nodes with high accuracy but increasingly misconfigure attributes and Boolean grouping as the number of interdependent nodes emitted in one pass grows.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 数据集是制造的合成基准，虽然包含复杂 DAG 结构，但原文未证明该分布足以代表真实企业联络中心中所有自然语言写法、异常规则和平台迁移场景；真实部署效果仍需外部数据验证。
- 核心 AI% 依赖 Claude Opus 4.6 评审，存在 LLM-as-judge 的模型偏好风险；作者通过 GPT-5.3-chat 与 GPT-5.2 的桥接比较、程序化 Cond% 以及附录论证缓解该问题，但评审指标仍不等同于真实生产执行成功率。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Monolithic：模型直接根据完整的单体提示生成最终工作流 JSON，是传统端到端生成基线，用于测量不拆分图构造时的性能和提示成本。
- Selector→JSON：先由选择器缩小相关注册表词汇，再让模型直接生成 JSON；它检验仅减少候选词汇、但仍把最终图结构组合交给模型是否足够。
- IR-only：使用中间表示承载结构化生成过程，但不结合本文最终的 Selector+IR 选择器配置；它用于判断 IR 编译思路本身的作用。
- GPT-5.2 与 Claude Opus 4.6：推理类模型参考线，用于比较非推理模型方案与更昂贵的扩展推理模型的质量。它们不是同一模型架构下的严格成本对照，主要承担质量上界或参考水平的角色。

**实验想回答的问题**

- 在涵盖 $635$ 条规则的合成基准上，选择器与中间表示（IR）驱动的神经符号流程，是否能提升非推理模型生成工作流的条件正确性与语义有效性，并达到推理模型的可比质量？
- 性能提升究竟来自哪一部分设计：缩小注册表词汇范围的选择器，还是把组合式图构造交给确定性编译器的 IR 流程？同时，模型一次生成的节点数量是否会造成属性配置和布尔条件分组的密度瓶颈？

**实验实现**

实验覆盖 GPT-4.1、GPT-5.3-chat 两个非推理模型，以及 GPT-5.2、Claude Opus 4.6 两个推理类参考模型。全部 $16$ 个模型—配置单元均采用贪心解码（temperature $=0$），因此基本没有解码随机性；不确定性通过重采样而不是重复生成来估计。所有指标均在 $635$ 条规则上计算。AI% 固定由 Claude Opus 4.6 按同一规则书评审；Cond%、JSON 有效性、事件/节点集合匹配和节点精确率均由程序直接对照真实工作流计算。作者特别说明，Opus 生成结果由 Opus 评审可能存在自偏好，但主要比较 GPT-5.3-chat 与 GPT-5.2，不涉及 Opus 生成，因此该比较中的自偏好因素会抵消；此外，条件精确率仍提供独立于评审模型的检验。统计上，温度为 $0$ 时单次运行适合使用配对 McNemar 检验，场景聚类 bootstrap 置信区间用于反映逐规则比例的不确定性。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Selector→JSON 与 Selector+IR 的对比：两者都使用选择器，但前者仍直接输出 JSON，后者将结果交给 IR 流程。 | GPT-5.3-chat 的 Selector→JSON 为 Cond% $75.1$、AI% $75.3$，Selector+IR 为 $82.2$、$80.6$，分别提高 $7.1$ 和 $5.3$ 个百分点；GPT-4.1 则为 $79.7$、$71.5$ 对比 $78.1$、$64.6$。 | 在 GPT-5.3-chat 上，加入 IR 后的增益支持“确定性编译器承担组合式图构造”是关键因素，而不只是减少注册表候选项。可是该对比并非完全纯粹的单变量实验：原文明确说 Selector→JSON 使用独立调优的选择器，并在选择时通过更完整的注册表，因此不能把所有差异严格归因于 IR。 | Table 1, Section 5.1；表中每项为“Cond% / AI%”<br><span class="experiment-evidence">Selector → JSON 79.7 / 71.5 75.1 / 75.3 87.4 / 84.3 78.6 / 80.5
IR-only 78.3 / 65.2 79.4 / 77.2 91.0 / 82.4 83.0 / 88.8
Selector+IR 78.1 / 64.6 82.2 / 80.6 89.6 / 84.1 88.0 / 88.8</span> |
| Monolithic 与 IR-only 的对比：检验从完整单体提示转向 IR 流程的独立影响。 | GPT-5.3-chat 的 Monolithic 为 Cond% $56.5$、AI% $56.4$，IR-only 为 $79.4$、$77.2$，分别提高 $22.9$ 和 $20.8$ 个百分点；GPT-4.1 的对应结果为 $70.1$、$66.8$ 与 $78.3$、$65.2$。 | 对 GPT-5.3-chat 而言，即使不加入最终 Selector，IR-only 也大幅改善条件匹配和评审有效性，说明把复杂图构造从一次性 JSON 发射中移出模型本身具有决定性价值。GPT-4.1 的 AI% 几乎没有改善，提醒我们 IR 并不能消除所有模型能力差异；同时，IR-only 与 Monolithic 的提示内容和生成路径可能不止一个变量不同，因此它更适合证明总体设计方向，而非精确分解每个实现细节的因果贡献。 | Table 1, Section 5.1；表中每项为“Cond% / AI%”<br><span class="experiment-evidence">Monolithic 70.1 / 66.8 56.5 / 56.4 87.2 / 79.8 87.2 / 84.1
IR-only 78.3 / 65.2 79.4 / 77.2 91.0 / 82.4 83.0 / 88.8</span> |

**定性案例**

- 密度诊断是最具解释性的定性结果：模型能够选出正确节点，却在一次生成多个相互依赖节点时错误配置属性或布尔分组。这表明失败不是简单的词汇检索问题，而是长结构化输出中的组合一致性问题；因此，IR 将模型输出限制为紧凑意图，随后由确定性编译器展开为 DAG，正好针对该失败模式。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文研究利用非推理型大语言模型与确定性编译器将自然语言转换为结构化工作流 DAG，核心是 LLM 结构化生成方法。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`75aa2ba675dd3067480b43a1bcc047442a58fc3e0498d96de88b6c1d28fea239`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
