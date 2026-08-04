---
title: "[论文解读] Prompt-Induced Waste in Large Reasoning Models: A Preregistered Two-Harness Benchmark of Coding Agents"
description: "[arXiv 2608.01347][LLM 效率] 本文通过预注册、配对控制的双代理框架基准，研究用户提示词措辞是否会在不提高编程任务正确率的情况下增加大型推理模型的推理、工具调用与交互成本。"
arxiv_id: "2608.01347"
announcement_date: "2026-08-04"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:01:23.633086+00:00"
source_sha256: "e3b352835efacafdc99a824dac9ea52d4c9ce75a41b2676d5b2d361a495995e5"
tags:
  - "LLM 效率"
  - "LLM 评测"
  - "LLM Reasoning"
  - "大型推理模型"
  - "编程智能体"
  - "提示措辞"
  - "推理词元"
  - "智能体框架"
  - "行为效率"
  - "计费效率"
  - "前缀缓存"
  - "因果基准"
  - "预注册实验"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2608.01347</p>

# Prompt-Induced Waste in Large Reasoning Models: A Preregistered Two-Harness Benchmark of Coding Agents

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Sarel Weinberger, Amir Hozez</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01347v1) · [PDF 下载](https://arxiv.org/pdf/2608.01347v1) · **关键词** 大型推理模型, 编程智能体, 提示措辞, 推理词元, 智能体框架, 行为效率, 计费效率, 前缀缓存, 因果基准, 预注册实验<br>


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

本文通过预注册、配对控制的双代理框架基准，研究用户提示词措辞是否会在不提高编程任务正确率的情况下增加大型推理模型的推理、工具调用与交互成本。

**不用术语来说**：同一个编程任务可以用不同措辞交给同一个模型，例如要求它“深入思考”或“比较多种方案”；这些措辞可能让编码代理思考更久、调用更多工具并进行更多轮交互，却未必更容易完成任务。由于代理框架本身会附加大量系统提示和工具说明，服务商还会使用缓存并以不同方式报告推理 token，因此仅比较提示词长度或账单金额，无法判断额外开销究竟由用户措辞、代理框架还是计费机制造成。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 建立可复用的预注册基准：在配对实验块内固定模型、任务及其他运行条件，仅改变用户提示词，并使用代理不可见的确定性测试判断任务是否成功，从而识别提示措辞对计算浪费的因果影响。
- 将行为效率与计费效率分开，并在两个真实代理框架中重复各条件；同时保留服务商报告的推理与缓存元数据，以分析框架固定前缀、交互轮数、缓存折扣及协议转换造成的混杂。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究以大型推理模型为核心的编程智能体成本。此类系统并非只生成一次答案，而是由智能体框架向模型附加系统提示与工具定义，再让模型在多轮循环中检查代码、调用工具、读取结果并继续推理；因此，实际开销同时来自隐藏或单独计量的推理词元、反复传输的输入前缀、工具调用和智能体轮次。论文关注的关键测量问题是：在模型、任务和框架保持不变时，仅改变用户提示的措辞，是否会增加这些计算与交互开销，以及增加的开销是否带来更高的任务成功率。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大型推理模型**

在给出最终回复或工具操作前进行额外内部推演的语言模型；论文将这部分计算对应的词元称为“推理词元”。由于推理词元可能按输出费率收费，提示语诱发的冗长思考会直接增加成本。

</div>
<div class="concept-item" markdown="1">

**编程智能体框架**

把模型、系统提示、工具模式和迭代执行逻辑组合起来的软件运行环境，文中称为 harness。它决定每轮向模型发送哪些固定内容、如何执行工具以及何时继续或停止，因此同一模型和提示在不同框架下可能产生显著不同的开销。

</div>
<div class="concept-item" markdown="1">

**前缀缓存与行为成本**

服务商可缓存反复出现的系统提示和工具定义，并对缓存输入给予计费折扣，但缓存通常不改变智能体实际执行的推理、调用和轮次。因而论文区分行为效率与计费效率，避免把账单下降误判为模型做了更少工作。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是在真实编程智能体框架中执行确定性编码任务的大型推理模型。每个实验条件的输入包括一个编码任务、某个冻结的用户提示版本、指定模型以及指定智能体框架；框架随后附加其系统提示和工具模式，并驱动模型进行多轮推理与工具执行。系统输出既包括最终代码修改，也包括推理词元数、工具调用数、智能体轮次、运行时间、缓存与非缓存输入及相应费用等过程记录；任务正确性由不会进入智能体工作区的隐藏确定性测试判定。为了识别提示措辞的因果影响，论文在配对实验块内固定模型、任务、框架和其他条件，只改变用户提示，并预注册假设、阈值及分析方案。该设定还明确处理三项混杂因素：框架每轮重传的大型固定前缀使提示长度不能代表总成本；服务商缓存使账单成本与实际行为工作量分离；协议转换层可能遗漏服务商报告的推理词元元数据。

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

大型推理模型作为编码代理时，每轮不仅生成最终回答，还可能消耗隐藏但按输出价格计费的推理 token，并产生工具调用和后续代理轮次。开发者经常加入“逐步思考”“深入思考”“比较多个方案”或顺带重构等指令，却缺少证据判断这些措辞带来的额外计算是否换来了更高的任务成功率，因此难以制定兼顾正确性和成本的提示规范。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **经验性提示技巧**：实践者依据经验在提示中加入深入推理、逐步分析、多方案比较或扩大任务范围等措辞，希望模型投入更多思考并提高解题质量；原文将这类做法概括为缺少受控证据支持的“prompt folklore”。
- **基于表面长度或账单成本的朴素评估**：这类评估直接以用户提示长度、服务商最终账单或单一路由返回的 token 统计近似代理工作量，而没有同时控制代理框架前缀、交互轮数、自动前缀缓存和协议层元数据保留情况。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 提示经验没有在真实代理循环中进行严格的配对控制，因此即使观察到成本或成功率变化，也难以排除任务、模型和运行条件差异，不能可靠回答某句提示是否因果性地增加无效推理。
- 表面成本指标混合了不同机制：代理框架会在每轮重传系统提示和工具模式形成大量固定输入，缓存会降低账单但不改变模型行为，而协议转换还可能静默丢失推理 token；其后果是提示长度、计费成本与实际行为工作量可能彼此背离。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有证据尚未在预先固定假设和判定阈值的条件下，跨多个大型推理模型、确定性编程任务及真实代理框架，隔离用户提示措辞对代理计算开销的因果影响；尤其缺少同时以隐藏测试控制任务质量、区分行为效率与计费效率，并检验提示效应是否随代理框架变化的系统研究。

</div>
<div markdown="1"><span>核心问题</span>

在模型、任务和运行条件保持不变时，仅改变用户提示的表达方式，会如何影响编码代理的推理 token、工具调用、交互轮数、运行时间与任务成功率；这种影响是否能够跨模型和代理框架复现，并且是否存在只增加成本而不提高正确率的提示形式？

</div>
<div markdown="1"><span>作者直觉</span>

若在同一配对实验块中只替换用户提示词，并用代理无法看到的确定性测试评价最终结果，那么成功率相同条件下出现的额外推理、工具调用或轮次就可以解释为提示诱发的浪费。再将相同的模型、任务和提示组合放入两个真实代理框架，并分别记录未受缓存折扣影响的行为指标与实际计费指标，就能进一步判断额外开销来自提示本身、框架设计还是服务商的计费与元数据机制。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是训练新模型，而是构建一个预注册、配对控制的编码代理基准，用于估计提示词措辞对推理开销的因果影响。实验对象包括推理模型、代理框架、确定性编码任务和提示词变体；在同一“模型－框架－任务”区组内，仅改变用户提示的措辞，并以精确基线提示为参照。代理在真实工具循环中检查文件、编辑代码并运行测试，最终由工作区外的隐藏确定性测试判定成功；与此同时，双侧日志系统记录供应商原始用量、工具调用、代理轮次、耗时、文件改动和缓存信息。这样，提示词导致的行为变化能够与任务差异、模型差异、框架固定前缀及缓存折扣区分开来。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 冻结假设、任务与分析协议

作者在查看基准结果前预注册假设、指标定义、浪费判定阈值和实验流程；进入留出集阶段前，又冻结各模型待验证的提示变体、任务、评估器与分析代码。Kimi-K3复现实验和Claude Sonnet 5跨供应商实验也分别在首次查看结果前冻结矩阵及差异阈值。

<div class="method-step__io" markdown="1">

**输入**：待检验的提示词效应假设，以及编码代理可能产生的推理开销、工具开销和范围违规问题。<br>
**输出**：不可根据观测结果事后调整的实验协议，以及彼此分离的开发集、冻结留出集和注册后复现实验。

</div>

**直观理解**：这相当于先写好判卷规则再考试，避免研究者看到某个偶然结果后改变指标或挑选最有利的任务。开发集负责发现候选效应，未见过的留出任务负责确认这些效应能否复现。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 构造任务与受控提示条件

每个任务由干净代码夹具、单一目标、明确验收标准、可见测试、工作区外隐藏测试、允许或禁止修改的路径以及专用评估器组成。模板生成器为任务渲染18种提示变体：主要变体保持目标、验收标准和测试命令逐字一致，只改变诸如深度思考、多方案比较、最大确定性、顺带清理或有界效率等措辞；故意破坏语义等价性的压力变体则单独分析。

<div class="method-step__io" markdown="1">

**输入**：24个小型确定性编码任务，其中16个属于开发集、8个属于留出集；任务覆盖Python、JavaScript和Go，并按低、中、高复杂度分层。<br>
**输出**：内容目标受控的主要提示矩阵，以及用于研究歧义、误导性提示、无关上下文和多轮拆分等输入缺陷的压力测试矩阵。

</div>

**直观理解**：主要实验像给同一道题换不同说法：要做的代码修改和通过标准不变，因此额外推理更可能来自措辞本身。压力实验则主动加入有缺陷的信息，用来回答错误线索与普通冗余是否具有不同代价。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 在两个真实代理框架中执行配对运行

PI.DEV通过OpenAI聊天补全接口直接调用模型；Claude Code通过固定版本的LiteLLM网关把Anthropic Messages协议转换为聊天补全协议。每个代理在真实的多轮工具循环中读取文件、搜索、修改代码和运行测试；同一区组中的基线与变体共享模型、框架和任务，只改变用户提示。

<div class="method-step__io" markdown="1">

**输入**：冻结的模型、任务、提示变体和代码夹具，以及PI.DEV与Claude Code两个代理框架。<br>
**输出**：每次运行的最终代码状态、代理轨迹、工具调用序列、轮次数、耗时及供应商用量记录。

</div>

**直观理解**：代理框架不只是一个聊天界面，它会附加系统提示和工具说明，并可能多次把上下文发送给模型。因此相同模型和任务在不同框架下可能产生完全不同的输入规模和循环次数，必须把框架作为实验因素而不是忽略掉。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 独立判定正确性并采集行为与计费指标

专用评估器同时运行可见测试和从未进入代理工作区的隐藏确定性测试，并依据允许路径检查越界修改。两个反向代理分别捕获协议网关两侧的数据，分析时采用供应商侧记录的推理令牌与缓存元数据，同时统计可见输出令牌、工具调用、轮次、重复读取或搜索、测试次数、首次编辑时间和墙钟时间。

<div class="method-step__io" markdown="1">

**输入**：代理完成后的代码、运行轨迹、版本差异和供应商返回的原始用量对象。<br>
**输出**：每次运行的任务成功、范围合规、行为开销、逻辑输入、实际账单成本与假设无缓存成本。

</div>

**直观理解**：隐藏测试防止代理仅针对已见测试“投机通过”；双侧抓包则防止协议转换层静默丢弃推理令牌、工具模式或缓存字段。实际账单会受缓存折扣影响，因此论文另外保留行为工作量和无缓存成本，避免把供应商优惠误当成模型更高效。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 配对推理比

$$
R_{m,h,t,v,r}=\frac{q_{m,h,t,v,r}}{\operatorname{median}_{r'\in\mathcal{B}_{m,h,t}}q_{m,h,t,b,r'}}
$$

**符号说明**

- $R_{m,h,t,v,r}$：模型m、框架h、任务t、提示变体v在第r次运行中的配对推理比
- $q_{m,h,t,v,r}$：该变体运行由供应商报告的推理令牌数
- $b$：精确基线提示条件
- $\mathcal{B}_{m,h,t}$：同一模型m、框架h和任务t区组中的基线重复运行集合
- $\operatorname{median}$：对基线重复运行取中位数，以降低异常运行的影响

<div class="equation-explanation" markdown="1">

**直观理解**：该比率把一次变体运行的推理量与完全匹配区组中的典型基线相比；$R_{m,h,t,v,r}=1$表示与基线相当，大于1表示消耗更多推理。论文再对任务聚类自助抽样得到95%区间，并依据预注册规则判断增加是否稳定且没有换来成功率收益。<br>
**原文位置**：第2.5节 Metrics；原文以文字定义“paired reasoning ratio”，未给出编号公式

</div>

</div>

<div class="equation-block" markdown="1">

#### 逻辑输入令牌

$$
I_{\mathrm{logical}}=I_{\mathrm{uncached}}+I_{\mathrm{cached}}
$$

**符号说明**

- $I_{\mathrm{logical}}$：模型在语义上接收的总输入令牌数，不考虑缓存折扣
- $I_{\mathrm{uncached}}$：按未缓存方式计量或计费的输入令牌数
- $I_{\mathrm{cached}}$：命中供应商前缀缓存的输入令牌数

<div class="equation-explanation" markdown="1">

**直观理解**：缓存只改变某部分输入的价格，不会删除模型收到的系统提示、工具模式或历史上下文。因此用$ I_{\mathrm{logical}} $描述实际传输的上下文规模，并把实际账单与估计无缓存成本分开，才能避免将缓存返利解释为行为效率提升。<br>
**原文位置**：第2.5节 Metrics

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文没有训练或微调模型，也不存在通过梯度下降优化的损失函数；其目标是通过预注册的受控实验估计提示措辞对代理推理和成本的因果效应。这里的“浪费”是分析阶段的分类：变体的配对推理比中位数须大于$1.5$，95%区间下界须大于$1.1$，不能带来实质成功率增益，而且效应须出现在多个任务上；这些阈值用于证据判定，不是模型训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 配对提示生成与冻结模块**

模板生成器从每个任务的固定目标、验收标准和测试命令生成主要提示变体，并自动验证这些关键字段保持逐字一致。18种变体中，9种主要变体用于近似隔离措辞的因果效应，目标简写与范围授权变体用于框架轴分析，7种压力变体因故意改变语义条件而单独统计。

> 直观理解：该模块保证实验真正比较“怎么说”，而不是悄悄改变“要做什么”。压力变体不能与语义等价提示混在一起，否则由错误信息导致的开销会被误归因于普通措辞。

**2. 双框架执行与双侧采集模块**

固定版本的PI.DEV和Claude Code执行相同任务；Claude Code经固定版本LiteLLM网关连接聊天补全接口。两个日志反向代理采集网关两侧协议数据并脱敏，使分析能够绕过网关丢失或重算的推理、缓存及成本字段，统一采用供应商侧原始用量对象。

> 直观理解：协议网关可能表面上返回文本，却丢掉工具定义、推理细节或正确价格，因此仅看代理界面不足以确认实验有效。双侧记录相当于同时检查发出和收到的“收据”，可以定位成本到底来自模型、框架还是协议转换。

**3. 隐藏评估与成本分解模块**

评估器在代理结束后运行可见测试和工作区外隐藏测试，并用版本差异与路径白名单检查范围合规。成本账本把行为指标与计费指标分开：前者包括推理令牌、工具调用、轮次和时间，后者区分未缓存输入、缓存输入、逻辑输入、实际成本和估计无缓存成本。

> 直观理解：正确性、代理实际做了多少工作、供应商最终收多少钱是三个不同问题。隐藏测试回答代码是否真的正确，行为指标回答代理是否浪费计算，而无缓存成本提供不受随机折扣干扰的经济比较。

**训练与推理**

全部过程属于推理时评测。首先冻结模型、框架版本、任务夹具、提示模板和评估协议；随后为每个任务建立干净工作区，由指定框架调用推理模型进入多轮工具循环，直至模型停止、满足框架终止条件或触及预算上限。运行期间记录模型响应、推理令牌、工具调用、轮次、文件访问、测试执行、时间和缓存字段；结束后再由外部评估器执行隐藏测试并检查修改范围。开发阶段用完整筛选矩阵寻找候选提示效应，留出阶段只在8个未见任务上运行预先选定并冻结的变体；注册后复现实验则将冻结协议迁移到Kimi-K3和第一方Anthropic API上的Claude Sonnet 5，以检查效应方向是否依赖原模型、供应商或协议网关。由于Anthropic API把思考令牌计入输出却不单独报告，Claude Sonnet 5实验使用相对自身基线的总输出令牌比，作者将其解释为推理效应的下界。

**复现信息**

公平复现所需的关键设置包括：24个任务按16个开发任务和8个留出任务划分，每个夹具在实验前验证为无法通过可见测试；任务覆盖9个Python、9个JavaScript和6个Go任务，并含低、中、高复杂度各8个。主要模型实验固定六个由Together AI提供的推理模型；框架固定为PI.DEV 0.82.1和Claude Code 2.1.220，协议转换固定为LiteLLM 1.93.0。网关必须先通过包含多步工具循环的能力测试，且分析必须使用供应商侧原始记录，因为论文观察到网关会丢弃推理细节、重算缓存字段，并可能使用不准确的模型价格表。

指标解释时必须保持三个边界。第一，提示长度不能替代输入成本，因为框架会在每轮重发系统提示和工具模式；应报告逻辑输入、轮次及工具行为。第二，实际账单受到概率性前缀缓存影响，应同时报告实际成本和按固定价格估计的无缓存成本，并且不能把缓存命中视为代理少做了工作。第三，不同模型家族的推理令牌语义和基线尺度不同，主要比较应在模型内部、框架内部和任务内部完成，同时并列检查绝对令牌数；跨供应商无法分离思考令牌时，则须明确改用总输出令牌指标，不能与可单独报告推理令牌的结果直接混同。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 核心任务集由24个确定性编码任务组成，按复杂度分为低、中、高三档，每档8题。任务通过隐藏评测器判断正确性，作用是避免模型针对公开测试直接优化，并在可重复条件下比较不同提示词和框架的成本。
- 开发与留出划分：作者先在开发任务上为每个模型选择三个最容易诱发浪费的提示变体，再冻结选择，并在8个未见留出任务上重新运行。留出阶段用于检验提示词效应是否能泛化，而不是只在用于选择提示词的任务上成立。
- 扩展验证包含筛选、压力测试、留出、复现和跨提供方研究；全文摘要报告共4,643次有效运行。Kimi-K3复现还在首次观察结果前冻结任务规则、实验矩阵和“实质差异”阈值，用于降低事后调整分析标准的风险。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**配对推理令牌比率**

对同一模型和任务，将某提示变体的推理令牌数与参照提示进行配对比较，并汇总其中位比率；该指标衡量提示措辞使内部推理成本放大或缩小的程度。 （在任务成功率不下降的前提下越低越好，因为更低表示完成相同任务消耗更少推理令牌。）

</div>
<div class="metric-item" markdown="1">

**任务成功率**

由确定性的隐藏评测器判断编码任务是否正确完成，用于检查额外推理支出是否转化为实际正确性收益。 （越高越好；但必须与成本联合解释，因为论文关注的是成本增加却没有正确性改善的浪费。）

</div>
<div class="metric-item" markdown="1">

**每次成功成本**

将推理令牌、静态输入和多轮代理交互等支出与成功任务数联系起来，衡量获得一次正确结果所需的资源。所给节选未提供其完整计算公式。 （越低越好，因为它直接反映代理系统取得有效结果的成本效率；提供方缓存造成的账单下降不能自动视为行为效率提升。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 要求模型提出并比较多种方案（mult._approaches）

<div class="result-value" markdown="1">

作者报告，该指令在所有受测模型上把推理令牌提高到参照条件的2.4至7.4倍，同时没有带来正确性改善，是跨模型最稳定的提示诱发浪费。

</div>

这意味着“先想出多个方案再比较”会让编码代理投入大量额外推理，即使任务最终答案并未更正确。它支持该提示在本任务集和实验框架下具有稳定成本副作用，但不能证明多方案比较在所有开放式软件工程任务中都无价值。

<div class="result-source" markdown="1">

来源：摘要；留出结果见第4.1节和表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Asking the model to develop and compare several approaches is the most consistently wasteful instruction, increasing reasoning tokens by 2.4-7.4x across all models.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 通用深入思考提示与有界效率模板

<div class="result-value" markdown="1">

作者报告，通用“think deeply”提示把推理量提高到1.6至2.2倍；相比之下，规定范围、验收标准和停止条件的bounded_eff.模板总体成本中性，并在部分条件下可将推理量减半。

</div>

结果表明，模糊地要求更深入思考容易延长 deliberation，而明确完成边界可能帮助模型及时停止。这里的“可减半”不是所有模型和任务上的统一保证；所给材料也未提供对应成功率、置信区间和逐模型表格行，不能据此断言该模板普遍提升准确率。

<div class="result-source" markdown="1">

来源：摘要；留出结果见第4.1节和表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Generic "think deeply" cues also increase deliberation by 1.6-2.2x, while a bounded-efficiency template specifying scope, acceptance criteria, and a stop condition is cost-neutral and can halve reasoning.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 固定模型、任务和提示词，对比Claude Code与PI.DEV框架

<div class="result-value" markdown="1">

作者报告，相同的模型—任务—提示组合在Claude Code下每次成功的成本是PI.DEV下的5至30倍，主要归因于更大的静态前缀和更多代理轮次。

</div>

该比较说明系统成本不只由模型或提示决定，代理框架注入的上下文和交互策略可能产生更大的开销。由于两个框架使用的协议路径不同，该结果反映的是完整框架配置的总体效应，不能仅归因于某一个组件，也不等同于Claude Code在功能或任务覆盖上整体更差。

<div class="result-source" markdown="1">

来源：摘要；跨框架实验的具体表格位置在所给节选中未明确报告

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Harness choice matters even more: identical model-task-prompt triples cost 5-30x more per success under Claude Code than under pi, mainly because of larger static prefixes and more turns.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 任务范围仅包含24个确定性编码任务，且每个复杂度档位只有8题。隐藏评测提高了客观性和可重复性，但对需求澄清、多人协作、长期代码维护及主观质量权衡等真实软件工程场景的外推能力有限。
- 框架比较估计的是PI.DEV与Claude Code完整配置的总体差异；静态前缀、协议转换、工具策略和轮次控制同时变化，因而不能从5至30倍结果中识别每个组件的独立因果贡献。此外，所给节选未展示置信区间、完整成功率表和逐任务分布，本分析仍需结合论文表格及代码仓库进行源文核验。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 中性或默认提示：作为提示措辞实验的参照条件，用于估计加入“深入思考”“比较多种方案”等指令后产生的额外推理成本。所给节选未列出该基线的完整原文模板。
- bounded_eff.（有界效率模板）：明确任务范围、验收标准和停止条件。它是有意义的效率基线，因为它不是简单要求模型少思考，而是为代理提供何时完成、何时停止的操作边界。
- PI.DEV框架：直接使用OpenAI Chat Completions协议，是与Claude Code比较代理框架开销时的参照框架。固定相同的模型、任务和提示词后，该比较主要检验静态前缀、交互轮次及框架协议带来的成本差异。
- 无关文本扰动：用于与误导性架构提示比较，从而区分“提示变长造成的成本”与“错误技术方向诱导模型进行无效探索造成的成本”。

**实验想回答的问题**

- 在真实编码代理中，仅改变提示词表述、保持模型与任务不变，是否会显著增加推理令牌、工具调用或代理轮次，却不提高隐藏评测器判定的任务成功率？
- 提示词效应能否跨模型、未见任务、代理框架和服务提供方复现；相较提示词，代理框架本身对每次成功所需成本的影响有多大？

**实验实现**

核心留出检验在PI.DEV上进行：每个模型仅依据开发数据选择三个最浪费的提示变体，随后在8个未见任务上各重复5次，因此每个实验单元为$n=40$。完整研究还包括压力测试、跨框架、跨提供方及Kimi-K3和Claude Sonnet 5复现。该设计有助于减少提示变体选择偏差，但所给节选没有展示随机种子、超时阈值、任务级失败处理及全部提示模板，相关实现仍需对照论文正文和仓库核验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 误导性架构提示与无关文本对照 | 作者报告，误导性的架构提示比无关文本造成的成本高得多。原文未明确报告该对照的具体倍率或绝对令牌差。 | 这一对照隔离了两种机制：无关文本主要增加输入长度，而误导性技术建议还可能把代理引向错误实现路线，触发额外检查、修改和工具调用。因此，观察到的浪费更可能来自错误搜索方向，而不只是提示更长；但缺少所给节选中的量化结果，效应大小仍需查表确认。 | 摘要；具体消融表格或章节位置原文未明确报告<br><span class="experiment-evidence">Misleading architectural hints are far costlier than irrelevant prose, and provider-side caching reduces billed cost without changing behavior, so it must not be treated as efficiency.</span> |
| 提供方缓存下的账单成本与实际模型行为对照 | 作者报告，提供方缓存会降低计费成本，但不会改变模型行为。原文未明确报告缓存带来的具体降幅。 | 该分析隔离“账单优化”和“计算行为优化”：缓存可能让重复前缀少收费，却不会减少代理实际生成的推理、工具调用或轮次。因此，若只看费用，会把基础设施折扣误判为模型或提示更高效。 | 摘要；具体消融表格或章节位置原文未明确报告<br><span class="experiment-evidence">Misleading architectural hints are far costlier than irrelevant prose, and provider-side caching reduces billed cost without changing behavior, so it must not be treated as efficiency.</span> |

**定性案例**

- 留出确认可视为选择偏差控制案例：作者只用开发数据挑选每个模型最浪费的三个提示变体，冻结后再到8个未见任务上检验，每个单元重复5次。主要效应在未见任务上仍被确认，说明结果并非完全由开发任务上的事后挑选造成；但所给节选没有提供逐任务失败轨迹，无法判断浪费主要来自过度规划、反复编辑还是工具调用循环。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces a benchmark measuring how prompts and agent harnesses affect reasoning-token, tool-use, and turn efficiency without improving coding success.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`e3b352835efacafdc99a824dac9ea52d4c9ce75a41b2676d5b2d361a495995e5`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
