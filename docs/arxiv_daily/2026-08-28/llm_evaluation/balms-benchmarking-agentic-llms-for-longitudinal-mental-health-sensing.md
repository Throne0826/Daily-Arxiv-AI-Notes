---
title: "[论文解读] BALMS: Benchmarking Agentic LLMs for Longitudinal Mental Health Sensing"
description: "[arXiv 2608.27219][LLM 评测] BALMS建立了一个纵向心理健康感知基准，用于检验不同大语言模型智能体能否从长期可穿戴与手机传感数据中预测可验证的心理健康分数，并生成有时间与数值证据支撑的解释。"
arxiv_id: "2608.27219"
announcement_date: "2026-08-28"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:31:08.789172+00:00"
source_sha256: "a128552ea7468d4e1f680668949fcc69df70ac7d00711b07ca574c4138ced536"
tags:
  - "LLM 评测"
  - "LLM Agent"
  - "LLM Reasoning"
  - "纵向心理健康感知"
  - "大语言模型智能体"
  - "可穿戴传感数据"
  - "幸福感评分预测"
  - "证据落地解释"
  - "外部记忆"
  - "工具调用"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.27219</p>

# BALMS: Benchmarking Agentic LLMs for Longitudinal Mental Health Sensing

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Yu Yvonne Wu, Arvind Pillai, Yuliang Chen, Yuwei Zhang, Sudarshan Regmi, Tess Z. Griffin, Michael V. Heinz, Lisa A. Marsch, Nicholas C. Jacobson, Andrew Campbell</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Dartmouth College；Affiliation: University of Cambridge</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27219v1) · [PDF 下载](https://arxiv.org/pdf/2608.27219v1) · **关键词** 纵向心理健康感知, 大语言模型智能体, 可穿戴传感数据, 幸福感评分预测, 证据落地解释, 外部记忆, 工具调用<br>


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

BALMS建立了一个纵向心理健康感知基准，用于检验不同大语言模型智能体能否从长期可穿戴与手机传感数据中预测可验证的心理健康分数，并生成有时间与数值证据支撑的解释。

**不用术语来说**：心理健康通常靠偶尔就诊或填写问卷来评估，只能看到少数时间点的状态；可穿戴设备虽然能连续记录睡眠、活动和心率等信息，但记录既长又杂，模型很难从中找出真正相关的变化，并据此可靠地判断压力、焦虑或抑郁程度。研究需要回答的不是模型能否查出某周最高步数，而是它能否综合数周乃至更久的个人历史，给出可信的心理状态预测并说明依据。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 将纵向心理健康感知形式化为统一的智能体评测问题，同时要求系统输出可核验的数值型健康分数和基于长期传感证据的自然语言解释，从而把预测正确性与解释可信度绑定起来。
- 在三个真实纵向数据集上，以五种开源或闭源大语言模型为骨干，统一比较提示式、工具式和记忆式三类智能体范式，并据此分析选择性记忆、特征语义、推理提示及历史长度对系统表现的影响。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

纵向心理健康感知旨在利用可穿戴设备和智能手机长期、被动采集的睡眠、活动量、心率等多通道行为与生理信号，辅助评估抑郁、焦虑和压力等心理状态。传统临床访谈与自评量表只能提供间隔较长的主观快照，而连续传感数据能够呈现跨周、跨月乃至跨年的变化；但这些记录通常篇幅长、数值密集且来源异构，既可能超过大语言模型的上下文窗口，也会暴露其长序列数值计算不可靠的问题。因此，本文关注由检索、外部记忆、可执行工具和语言推理共同构成的智能体，使模型能够选择相关历史、执行必要计算，并给出可核查的心理健康评分及其依据。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**纵向心理健康感知**

根据同一个人在较长时间内持续积累的行为和生理记录推断其心理健康状态，而不是只分析某一天或一次问卷。关键在于识别睡眠、活动、心率等信号随时间形成的模式。

</div>
<div class="concept-item" markdown="1">

**基于大语言模型的智能体**

以大语言模型为推理核心，同时允许其调用检索、外部记忆或计算工具的系统。相较于把全部传感记录直接塞入提示词，智能体可以筛选历史、委托精确计算，并组织自然语言解释。

</div>
<div class="concept-item" markdown="1">

**证据落地的解释**

生成的理由必须指向用户记录中真实存在的时间段、数值或变化趋势，并能够支持对应的心理健康预测。它不同于听起来合理但没有传感数据依据的泛化叙述。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一名用户跨较长观察期积累的多通道可穿戴设备或手机感知记录，以及关于其心理健康状况的查询，智能体需要联合完成两类输出：一是预测可验证的数值型幸福感或心理健康量表得分，二是生成由记录中的时间模式和数值证据支撑的自然语言理由。该设置假定传感历史可能跨越数周至数年，数据通道、特征格式和观察长度会因数据集而异，并且完整文本化记录可能超过模型上下文限制；因此系统需要借助提示、工具或记忆等智能体范式处理信息选择与数值推理。BALMS所评估的不是“某周最高步数”一类短窗口事实检索，而是能否从长期行为模式推断心理状态，并让解释与具体评分相互对应。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **MedAgentBench**: 该基准在交互式FHIR电子健康记录环境中评估医疗智能体，主要考察工具使用、规划和交互能力；它不覆盖BALMS所强调的多周至多年可穿戴历史推理、时间数值证据落地，以及心理健康评分与解释的联合评价。
- **现有可穿戴与移动感知LLM智能体**: Kim等、Merrill等、Choube等、Heydari等及Wu等的相关系统使智能体能够查询个人传感记录，但现有任务主要是短固定窗口内的事实查找或算术，如查询一周最高步数或一月平均静息心率；部分系统提供开放式洞察或个案展示，却缺少与解释配对的具体幸福感评分，因而难以验证解释是否真正支持预测。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

临床访问和自评问卷成本较高且采样稀疏，容易错过心理状态随时间发生的变化；手机与可穿戴设备则可低负担地连续采集睡眠、活动、心率等多通道信号。实际需求是把这些长期、异构且因人而异的记录转化为可审查的心理健康评估，但直接文本化长期高频数据会迅速消耗上下文窗口，而且心理状态并不是某个传感数值的简单映射，需要识别跨时间的行为模式并完成可靠的数值推断。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **短窗口可穿戴数据问答智能体**：把一周或一个月等固定窗口内的传感记录交给大语言模型或配套工具，回答最高步数、平均静息心率等事实检索与算术问题，主要测试模型能否定位数值并执行简单计算。
- **开放式健康洞察与文本临床智能体**：一类系统根据个人数据生成定性总结或个案式健康洞察；另一类系统通过检索、记忆或工具完成诊断问答、证据搜索和多轮临床对话，但其主要信息来源仍是文本，而非长期多通道传感序列。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 固定短窗口任务主要衡量事实查找和局部算术，不能检验智能体是否能从长期行为与生理变化中推断心理健康状态；当记录跨越多月且包含多个通道时，直接输入还可能超过模型上下文限制，并放大大语言模型处理长数值序列时的不可靠性。
- 定性洞察或开放式解释通常没有与明确的心理健康分数成对出现，因此难以判断解释是否真正支持预测；同时，不同数据集的传感器类型、特征格式和观察周期差异很大，单一数据集上手工设计的方案未必能够迁移。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有工作缺少一个跨真实纵向数据集、模型骨干与智能体范式的标准化评测框架，无法系统比较提示、外部计算工具和选择性记忆在长时间跨度心理健康推断中的作用，也无法同时核验最终分数以及解释中的时间依据、数值正确性和证据一致性。

</div>
<div markdown="1"><span>核心问题</span>

在不进行特定任务训练的条件下，提示式、工具式和记忆式大语言模型智能体中，哪类设计最能从不同格式和时间跨度的被动传感历史中预测心理健康分数并生成证据充分的解释；这种能力又如何受到模型骨干、特征语义、推理提示、传感通道数量和历史长度的影响？

</div>
<div markdown="1"><span>作者直觉</span>

智能体化的关键不在于把更多原始记录塞进模型，而在于合理分工：记忆或检索模块先从漫长历史中挑出相关片段，工具负责模型不擅长的精确数值计算，大语言模型再利用具有明确含义的行为特征组织跨时间推理并生成解释。这样既能缓解上下文容量和长序列计算问题，也使预测依据更容易被检查；BALMS通过统一任务与评测来验证这种设计直觉，而不是预先假定某一种智能体必然最佳。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

BALMS将纵向可穿戴与移动感知记录组织为“目标日前历史窗口”，要求基于大语言模型的健康代理完成两类任务：一是预测目标日的整数自报告心理健康分数，二是生成能够引用时间变化和传感证据的解释。所有代理在相同目标日划分与相同输入窗口上进行零样本推理；研究比较Health-LLM、分块RAG、RAPTOR和PHIA四种系统，并分别搭配五种开源或闭源语言模型骨干，同时考察直接提示与思维链提示的差异。

从流程上看，系统先接收一段按时间排列的行为和生理信号，再以直接上下文、检索记忆、层次记忆或ReAct式工具交互的方式选择并组织历史证据，最后输出心理健康量表分数及解释。通俗地说，这不是让模型查找“某周最高步数”这样的单条事实，而是让它像阅读一份长期健康日记一样，判断活动、睡眠等信号如何随时间变化，并据此估计当天的情绪、压力或焦虑水平。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造纵向感知窗口与预测目标

按照统一的目标日划分提取历史感知窗口，并保留记录的时间顺序；不同数据集分别以情绪、压力或焦虑自报告分数作为预测标签。公平比较时，各系统使用完全相同的目标日和输入窗口。

<div class="method-step__io" markdown="1">

**输入**：真实世界纵向数据集中的目标日、该目标日前的传感记录，以及对应任务所使用的原生Likert量表。<br>
**输出**：一个按时间组织的感知窗口，以及待预测的目标日与量表定义。

</div>

**直观理解**：可以把它理解为给所有代理同一份截止到目标日前的健康日志，避免某个方法因看到更多历史或不同测试日期而占优。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 组织或检索历史证据

Health-LLM按照其官方实现处理健康感知上下文；分块RAG使用LangChain实现从切分后的历史记录中检索相关内容；RAPTOR将日内记录和每日摘要构造成两层记忆树；PHIA按照官方实现以ReAct方式迭代调用可用信息，最多执行10轮。

<div class="method-step__io" markdown="1">

**输入**：目标日前的纵向传感窗口，以及用户提出的心理健康预测请求。<br>
**输出**：供语言模型推理的感知上下文、检索片段、层次摘要或工具交互轨迹。

</div>

**直观理解**：历史记录可能太长，不能简单全部塞给模型，因此不同代理采用不同的“翻日志”方式：直接阅读、查找相关片段、先看摘要树，或边思考边调用工具。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于语言模型进行零样本纵向推理

代理调用Qwen2.5-7B-Instruct、Mistral-7B-Instruct-v0.3、Qwen2.5-14B-Instruct、DeepSeek-R1-Distill-Qwen-14B或Claude-Haiku-4.5之一进行零样本推理；实验分别采用无思维链和加入CoT提示的设置。

<div class="method-step__io" markdown="1">

**输入**：整理后的历史证据、目标日查询、量表要求，以及可选的思维链提示。<br>
**输出**：目标日的整数自报告分数预测，以及开放式的证据化解释。

</div>

**直观理解**：模型既要给出一个与原量表一致的整数答案，也要说明哪些时间变化支持该答案；CoT只是鼓励模型展示分步推理，并不保证其引用的时间或数值一定正确。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分别评估数值预测与解释质量

封闭式预测按所有留出目标日上的平均绝对误差评估；开放式解释由单一Llama-3.3-70B-Instruct裁判同时检查时间推理操作和一般解释质量，裁判可见感知窗口、金标准分数、代理预测与解释。

<div class="method-step__io" markdown="1">

**输入**：代理预测分数、金标准自报告分数、生成的解释，以及原始感知窗口。<br>
**输出**：数值误差，以及时间维度的调用率、条件正确率、覆盖率和一般质量评分。

</div>

**直观理解**：第一部分检查“猜得离真实分数有多远”，第二部分检查“理由是否真的能从日志中核实”，从而避免只奖励语言流畅但没有证据的解释。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。BALMS在所给节选中是零样本代理评测框架，而不是通过监督学习训练新模型的方法；各语言模型骨干与代理实现直接用于推理，未报告针对三个心理健康数据集进行参数更新，也未定义新的训练损失。平均绝对误差属于封闭式任务的评估指标，而非用于优化模型参数的训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 纵向记忆与检索模块**

基准覆盖多种历史组织机制：分块RAG基于LangChain从切分记录中检索；RAPTOR把日内记录和每日摘要组织为两层记忆树；Health-LLM与PHIA沿用各自官方实现，其中PHIA允许最多10轮ReAct迭代。原文节选未进一步给出切块大小、检索数量、嵌入模型或具体工具接口。

> 直观理解：这个模块解决“长期记录太多、哪些信息值得看”的问题。平铺检索适合找局部证据，层次记忆先看摘要再定位细节，而迭代式代理可以根据中间判断继续查询。

**2. 分数预测与证据化解释模块**

每个代理以零样本方式输出数据集原生Likert量表上的整数自报告预测，并生成解释其判断的自然语言理由。可选CoT提示用于诱导显式分步推理，但方法并未额外训练专用预测头，也未宣称CoT本身能够保证时间依据或数值一致性。

> 直观理解：输出不只是一个心理健康分数，还必须给出“为什么”。这使基准能够区分偶然猜对的模型与真正利用长期行为变化作出判断的模型。

**3. 两层LLM-as-Judge解释评估器**

Llama-3.3-70B-Instruct裁判的第一层改编自TemporalBench，检查六类纵向操作：C1时间条件与字段对齐、C2时间片比较、C3相对变化判断、C4滞后效应、C5峰谷或变化点结构、C6跨通道交互；每项标记为正确、错误或未调用，并汇总调用率、调用条件下正确率与正确覆盖率。第二层改编自PHIA专家量规，以1至5级评分检查Faithfulness、Evidence Grounding、Domain Knowledge、Safety、Clarity和总体质量。

> 直观理解：裁判先判断解释有没有正确处理“何时变化、前后差多少、是否延迟、多个传感器是否共同变化”等时间问题，再判断理由是否可核验、清楚且安全。“未调用”选项避免因解释没有使用不必要的复杂操作而被扣分。

**训练与推理**

推理时，研究者首先为每个留出目标日提供相同的历史感知窗口，并根据代理范式直接组织上下文、执行分块检索、遍历两层RAPTOR记忆，或运行最多10轮PHIA ReAct交互。随后，代理使用指定骨干模型，在无CoT和有CoT两种提示条件下分别生成原生Likert量表上的整数预测及其理由；五个骨干包括四个本地部署的开源模型和Claude-Haiku-4.5。

评估阶段不再训练代理。封闭式输出与金标准自报告标签计算MAE，且在全部留出目标日上取平均；开放式理由交给固定的Llama-3.3-70B-Instruct裁判，裁判同时读取输入窗口、金标准分数、代理预测和理由，以判断解释是否符合预测、事实是否可从窗口验证，以及是否正确执行必要的时间推理。由于裁判可见金标准，其角色是离线评估器，而不是代理推理时可访问的辅助模型。

**复现信息**

为保证横向比较，各系统共享目标日划分、输入窗口、提示格式和解码设置。开源骨干通过vLLM在4张A6000 GPU上本地运行；Claude-Haiku-4.5通过Anthropic API调用。Health-LLM与PHIA遵循官方实现，PHIA的最大ReAct迭代次数设为10；分块RAG采用官方LangChain实现，RAPTOR在日内记录与每日摘要之上建立两层记忆树。

传感器敏感性实验还在GLOBEM上比较完整的移动端加智能手表信号与仅保留Fitbit信号的输入配置，用于判断信息量更大的原始多源记录是否一定优于较紧凑、语义更明确的可穿戴特征。所给节选没有报告具体历史窗口长度、切块参数、检索条数、采样温度、随机种子或裁判重复运行策略，因此不能据此完整复现这些设置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- DiversityOne：真实世界纵向被动感知数据集，用于情绪预测；输入以较原始的移动感知流为主，因此重点检验智能体处理复杂模式和子日级数据的能力。原文节选未明确报告样本规模、时间跨度及训练集、验证集、测试集的具体划分。
- PMData：包含Fitbit风格行为聚合特征的纵向数据集，用于压力预测。其特征更紧凑且具有直接语义，可检验LLM是否更容易利用步数、睡眠等高层行为指标。原文节选未明确报告样本规模和正式数据划分；附录的PHIA分析涉及$1463$个留出窗口，但不能据此推断完整数据集规模。
- GLOBEM：包含较稀疏的被动感知特征与原始移动数据流，用于PHQ-4焦虑等心理健康标签预测，同时承担解释质量、时间推理、传感器敏感性和长窗口扩展实验。原文节选未明确报告完整规模和正式划分；附录的PHIA分析涉及$1640$个留出窗口。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**平均绝对误差（MAE）**

计算预测分数与真实自报告分数之间绝对差的平均值，用于闭式心理健康分数预测任务T1。它直接反映分数偏差，但不能判断预测理由是否真实使用了传感器证据。 （越低越好，因为预测分数越接近对应的自报告标签。）

</div>
<div class="metric-item" markdown="1">

**LLM-as-a-Judge分层解释评分**

由裁判LLM依据量表评价开放式解释任务T2，包括一般解释质量以及时间推理维度，例如跨感知流对齐C1和结构调用C5。一般质量总分GQ被缩放到$[0,1]$以便比较。该指标测试解释是否流畅、完整且有时间证据，而非只测试最终数值。 （越高越好，因为高分表示解释更符合评分量表；但自动裁判分数仍不等同于临床有效性。）

</div>
<div class="metric-item" markdown="1">

**单样本平均延迟**

记录每个样本从智能体推理到产生结果的平均运行时间，用于比较直接提示、检索和多步代码执行的计算开销。 （越低越好，因为连续监测系统需要及时、低成本地返回反馈；不过低延迟本身不代表预测准确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 零样本T1预测：Claude-Haiku-4.5驱动Health-LLM，在DiversityOne上与训练集均值预测器比较

<div class="result-value" markdown="1">

Health-LLM取得$0.42$ MAE，优于均值预测器的$0.58$；说明较强闭源骨干在该设置下能够从纵向记录提取超过标签均值先验的信息。整体趋势仍是多数零样本智能体很少稳定超过均值基线，较小的Mistral-7B尤其容易落后。

</div>

这一比较的重要性不只是误差下降$0.16$，而是复杂系统终于超过了“不看传感器、只猜平均值”的最低参照。然而，它只证明特定骨干、范式和数据集组合有效，并不表示零样本智能体普遍可靠，也不能说明其解释已在时间上正确扎根。

<div class="result-source" markdown="1">

来源：第4.1节，Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For example, Claude-Haiku-4.5 with Health-LLM achieves 0.42 MAE on DiversityOne, outperforming the 0.58 mean baseline, while PHIA reaches 0.54 MAE on PMData, close to the 0.48 baseline.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### GLOBEM上的T2解释质量与时间推理：三个智能体范式跨不同LLM骨干比较

<div class="result-value" markdown="1">

Claude-Haiku-4.5是唯一同时缩小总体解释质量差距与时间证据扎根差距的骨干；开放式指令骨干通常能生成流畅文本，却很少可靠执行跨时间序列对齐C1或跨感知流结构分析C5。

</div>

结果区分了“解释写得像推理”和“解释确实依据时间序列做过运算”。语言流畅不能证明模型正确切分历史窗口、比较个人基线或追踪不同传感器之间的关系。该结论来自自动裁判量表，表明相对差异而非临床解释的最终可信度。

<div class="result-source" markdown="1">

来源：Figure 4图注及第4.2节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Only Claude-Haiku-4.5 closes both the rationale-quality and temporal-grounding gaps, while open-source instruct backbones produce fluent rationales but struggle with temporal reasoning and rarely invoke alignment (C1) or structure (C5).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### PHIA工具型智能体的执行轨迹诊断：Qwen2.5-14B-Instruct、随机种子0、三个数据集

<div class="result-value" markdown="1">

PHIA在GLOBEM的$85.9\%$窗口中输出模态标签$2$，MAE为$1.52$；在PMData中有$77.4\%$输出标签$3$，MAE为$0.57$；在DiversityOne中$99.5\%$的窗口没有可解析答案，MAE为$2.11$。这表明其PMData上的表面竞争力主要来自固定标签恰好接近数据集均值，而非针对个人历史进行有效计算。

</div>

工具调用并不会自动带来可靠数值推理。代码无输出、跨步骤状态丢失、强制结束时编造理由、凭空设置阈值和对原始流进行错误聚合，会让智能体对不同用户重复同一答案。因此，PMData上的接近基线不能被解释为真正理解了可穿戴记录；同时，这一诊断只直接覆盖指定骨干与种子。

<div class="result-source" markdown="1">

来源：Appendix B.1，Table 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On PMData the modal label (3) is close to the dataset’s mean stress, so MAE remains competitive (0.57 vs. mean predictor 0.48); on GLOBEM the modal label (2) is far from the low-skewed PHQ-4 anxiety distribution and MAE doubles (1.52 vs. 0.80); on DiversityOne the agent fails to parse a valid answer in almost every window.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验以自报告量表为目标，并通过LLM自动裁判解释；它评估的是与自报告的一致性及对感知窗口的可验证性，而非临床诊断准确性、治疗效果或真实部署中的安全性。论文也明确将BALMS定位为临床访视之间的低负担反馈系统，而不是诊断工具。
- 部分强结论具有配置依赖性：长窗口实验只使用Qwen2.5-14B-Instruct，PHIA详细失败分析只直接报告随机种子$0$，且GLOBEM与DiversityOne的原始或稀疏模式会显著影响工具执行。因而不能把某一范式的排名无条件推广到其他骨干、数据模式、心理量表或人群。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 均值预测器：始终输出训练集标签均值，不读取任何感知输入。它衡量仅利用数据集标签先验即可达到的误差；若复杂智能体不能超过它，就不能证明纵向传感器记录提供了额外预测价值。
- Health-LLM：基于提示的范式，将纵向感知记录文本化后直接交给LLM。它检验模型能否在单次上下文中阅读和综合完整历史，也暴露长上下文造成证据稀释与数值推理困难的问题。
- RAG：基于记忆或检索增强生成的范式，先从长期历史中选择相关记录，再由LLM预测并解释。它与直接提示的比较用于判断选择性检索能否控制上下文长度并利用更长历史。
- PHIA：工具型智能体，通过生成并执行代码操作预加载的DataFrame。它检验显式计算工具是否优于纯文本推理，以及工具接口与数据模式不匹配时是否会产生执行失败、标签坍缩和额外延迟。

**实验想回答的问题**

- 在不进行任务特定训练的条件下，现有智能体能否利用数月至数年的可穿戴设备与手机被动感知历史，准确预测每日心理健康或幸福感自评分数，并生成可由原始时间窗口验证的解释？
- 智能体范式、LLM骨干、思维链、回看窗口长度和传感器表示方式分别如何影响预测误差、时间证据扎根、推理质量与运行效率？

**实验实现**

实验覆盖三个真实世界纵向数据集、两个任务族、三种智能体范式和五个骨干：Qwen2.5-7B-Instruct、Qwen2.5-14B-Instruct、Mistral-7B-Instruct-v0.3、DeepSeek-R1-Distill-Qwen-14B及Claude-Haiku-4.5。T1在无任务特定训练的零样本条件下预测每日自报告分数，并以均值预测器为参照；T2生成依据感知窗口的解释，由LLM裁判按分层量表自动评分。论文还比较无思维链与加入思维链的提示，在PMData和GLOBEM上固定目标日、改变回看窗口，并在GLOBEM上比较完整多模态输入与仅Fitbit输入。长窗口实验使用Qwen2.5-14B-Instruct；PHIA附录故障统计使用该骨干和随机种子$0$。原文节选没有给出通用采样策略、所有随机种子、裁判模型身份、标签归一化方法或正式数据划分细节，因此这些信息需回查全文。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 思维链消融：在相同智能体配置中比较不使用与使用CoT提示 | CoT主要改善DeepSeek和Claude等推理导向骨干，在多数配置中降低MAE，最高相对改进达到$41.4\%$；普通指令骨干没有表现出同等稳定的收益。 | 该实验隔离了显式推理提示的作用：当骨干本身擅长组织中间推理时，先整理时间证据再给分可能减少误差；但CoT不是独立的可靠性机制，不能据此认定生成的步骤真实执行了时间序列运算，也不能推断所有模型都会获益。 | 第4.2节，Table 3<br><span class="experiment-evidence">With DeepSeek and Claude architectures, +CoT consistently reduces MAE across most configurations, yielding improvements up to 41.4%.</span> |
| 回看窗口长度消融：固定目标日，使用Qwen2.5-14B-Instruct改变PMData与GLOBEM的历史长度 | 随着可检索历史增加，RAG在PMData上的MAE约下降$29\%$，在GLOBEM上约下降$9\%$；Health-LLM反而随窗口增长而退化，PHIA在PMData较稳定但在GLOBEM仍较弱且波动较大。 | 该实验隔离了“更多历史”与“如何暴露历史”的影响。RAG的改进说明选择性检索可从长期记录中找到有用证据，而直接把全部记录文本化可能淹没目标日信息。两个数据集收益不同，提示检索价值依赖特征密度与语义质量，并不能证明任意增加历史都会提高预测。 | 第4.3节，Figure 5<br><span class="experiment-evidence">RAG benefits more consistently from longer histories, especially on PMData, where MAE decreases ∼29% as more historical records become available for retrieval. The gain is smaller on GLOBEM (∼9%), likely because its sparser passive-sensing features provide less informative retrieved evidence than PMData’s Fitbit-style aggregates.</span> |

**定性案例**

- 论文在附录D.1选取一个GLOBEM时间窗口，对两个骨干生成的推理轨迹逐项标注Tier-1与Tier-2维度，用于展示流畅解释与真实时间扎根之间的差别。当前节选未提供案例原文、预测值或逐项评分，因此不能进一步判断具体哪条证据被正确或错误使用。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出用于评测 LLM 智能体长期时序感知、预测和证据化推理能力的基准，智能体评测是核心贡献。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`a128552ea7468d4e1f680668949fcc69df70ac7d00711b07ca574c4138ced536`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
