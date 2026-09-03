---
title: "[论文解读] Large Language Models (LLMs) for Telecom Root Cause Analysis (RCA): A Structured Reasoning Framework for Evidence-Grounded Diagnosis"
description: "[arXiv 2609.02805][LLM Reasoning] 本文针对通用大语言模型在电信根因分析中推理不稳定、证据对齐不足和易产生幻觉的问题，提出将异构遥测、分阶段诊断路径、根因标签与可追溯解释联合起来的结构化微调框架 SEKA-FT。"
arxiv_id: "2609.02805"
announcement_date: "2026-09-03"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-03T04:28:40.775311+00:00"
source_sha256: "743811a3640cbb70364540f7a7998dad624e98aac82f6ef2f401b58fb83119aa"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大型语言模型（LLM）"
  - "根因分析（RCA）"
  - "电信网络"
  - "结构化推理"
  - "证据对齐"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.02805</p>

# Large Language Models (LLMs) for Telecom Root Cause Analysis (RCA): A Structured Reasoning Framework for Evidence-Grounded Diagnosis

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-03</span>
<span><strong>作者</strong> Hao Zhou, Mandar Kulkarni, Hao Chen, Yan Xin, Charlie, Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Jianzhong</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.02805v1) · [PDF 下载](https://arxiv.org/pdf/2609.02805v1) · **关键词** 大型语言模型（LLM）, 根因分析（RCA）, 电信网络, 结构化推理, 证据对齐<br>


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

本文针对通用大语言模型在电信根因分析中推理不稳定、证据对齐不足和易产生幻觉的问题，提出将异构遥测、分阶段诊断路径、根因标签与可追溯解释联合起来的结构化微调框架 SEKA-FT。

**不用术语来说**：现代移动网络由无线接入、传输和核心网等相互依赖的部分组成；当业务质量下降时，同一异常可能由覆盖、移动性、资源调度、邻区关系或配置等多种因素引起。运维人员不仅需要判断“故障是什么”，还需要确认该结论是否由实际指标支持。普通预测模型或直接调用大语言模型可能给出看似合理却缺少证据、前后不一致的答案，因此难以用于高风险的真实网络运维。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将电信根因分析重新表述为“证据—路径—决策”的结构化推理问题，而非仅从输入直接预测故障标签；其目标是让模型依次检查相关证据、排除不受支持的假设，再作出根因判断。
- 作者提出 SEKA-FT，将规范化后的异构网络证据、中间诊断检查、最终根因标签和证据化解释纳入统一微调监督，使诊断结论能够对应具体 KPI、拓扑关系、移动性统计及工程参数。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

电信网络根因分析（Root Cause Analysis, RCA）旨在根据网络运行数据定位导致性能下降或服务故障的最可能根本原因。5G及新兴6G网络同时包含无线接入、传输和核心网等异构层级，故障影响会跨越多个网络组件；传统规则系统依赖预设告警模式或KPI阈值，机器学习方法主要学习统计相关性，而大型语言模型（LLM）能够整合跨域知识并生成解释，但其诊断结果仍可能出现推理不稳定、证据对齐不足和幻觉等问题。本文将电信RCA建模为一种结构化推理任务，而不是简单的输入到标签预测任务。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**根因分析（RCA）**

RCA是从告警、性能指标、拓扑关系和配置参数等观测证据出发，判断造成当前故障或性能退化的根本原因。它不仅要求给出故障类别，还要求诊断过程能够被证据支持和解释。

</div>
<div class="concept-item" markdown="1">

**电信遥测与KPI**

遥测是网络设备和系统持续产生的运行观测数据，KPI则是衡量网络性能的关键指标，例如服务质量、资源使用或移动性相关指标。本文特别关注来自不同网络层级、具有不同结构的异构证据。

</div>
<div class="concept-item" markdown="1">

**结构化推理**

结构化推理把诊断拆分为有顺序的检查步骤，使模型先核对相关证据、排除缺乏支持的假设，再作出根因决定。本文将这种过程组织为“证据—决策路径—最终决定”，以提高诊断一致性和可追溯性。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定电信网络中的异构故障排查输入，包括用户面KPI、移动性统计、邻区关系、工程参数以及其他跨层遥测，模型需要输出根因诊断标签，并生成与具体网络证据和领域知识相对应的中间决策路径及可追溯解释。本文假设诊断不能只依赖表面统计相关性，而应逐步检查与候选根因相关的证据；实验设置聚焦于5G RCA数据集TeleLogs和TelecomTS，并考察不同证据表示和诊断特征下的方法表现。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

一次RCA样本的异构网络观测输入，例如KPI、移动性统计、邻区关系和工程参数。

</div>
<div class="notation-item" markdown="1">

**$y$**

样本对应的最终根因诊断标签或故障类别。

</div>
<div class="notation-item" markdown="1">

**$p$**

从证据检查到根因判断的中间诊断决策路径，用于表示分阶段的排查过程。

</div>
<div class="notation-item" markdown="1">

**$e$**

用于支持诊断的具体网络证据及其对应的领域知识。

</div>

</div>

**直接相关的工作**

- **基于规则的电信RCA方法**: 这类方法依据预定义告警模式或KPI阈值触发固定排障流程，具有明确规则但难以覆盖复杂、跨层和未见过的故障。本文不再把RCA限定为固定规则匹配，而是引入可学习的证据到决策路径监督。
- **数据驱动的机器学习RCA方法**: 机器学习方法能够处理大量遥测并进行故障检测或分类，但主要学习统计模式，面对未见故障通常需要重新训练，且缺少显式的多步诊断和可追溯解释。本文提出的SEKA-FT通过结构化证据、决策路径、根因标签和证据解释的联合监督来弥补这一不足。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

5G-Advanced及未来6G网络规模大、组件异构，并存在跨无线接入网、传输网和核心网的复杂依赖。一次性能退化往往需要同时核查用户面 KPI、移动性行为、资源调度、覆盖几何、邻区关系和配置参数；若根因识别错误或延迟，可能扩大通信中断并影响应急呼叫、支付、交通和医疗等关键服务。因此，实际运维需要一种既能综合跨层证据，又能给出稳定、可核验诊断依据的自动化 RCA 方法。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **规则系统与数据驱动机器学习**：规则系统依据预先定义的告警组合、KPI 阈值和排障流程匹配根因；机器学习方法则从大量遥测样本中学习统计模式，用于检测或分类潜在故障。前者把专家经验固化为确定性逻辑，后者通过数据拟合提高批量处理和模式识别能力。
- **直接使用通用大语言模型或常规微调**：这类方法把遥测描述、告警或排障问题直接交给大语言模型，由模型利用已有知识和多步生成能力输出根因及自然语言解释；常规监督微调通常更侧重从输入映射到最终标签或答案，但未必显式约束模型必须按照电信诊断依赖逐项验证证据。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 规则方法依赖人工穷举模式，难以覆盖复杂或新型故障；机器学习方法主要学习统计相关性而非显式诊断过程，面对未见故障模式时通常需要大量新数据和重新训练，也难以说明多层指标如何共同导向根因。
- 通用大语言模型即使具备跨域推理和解释能力，也可能对相似测量采用不一致的推理路径；若缺少遥测结构与诊断步骤约束，模型容易依赖表面相关性，甚至在没有 KPI、拓扑或配置证据时猜测原因，导致结论不可追溯且不适合直接支持高风险运维决策。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法尚未解决如何在同一个训练框架中，按照电信 RCA 的真实诊断依赖，同时对齐异构结构化证据、中间排查路径、最终根因标签和可追溯解释。缺少这种联合约束时，模型可能得到正确标签却使用错误理由，也可能生成流畅解释但无法由网络观测验证。

</div>
<div markdown="1"><span>核心问题</span>

能否通过面向电信领域的结构化微调，把 RCA 从直接的“输入到标签”预测改造成受控的“证据到诊断路径再到决策”推理，使大语言模型在不同 5G 数据表示和故障场景下同时提高根因识别准确性、决策一致性与解释可信度？

</div>
<div markdown="1"><span>作者直觉</span>

根因诊断更像按检查表排障，而不是看到若干异常后立即猜标签。若先把来源不同的网络信息整理为固定语义的上下文块，再要求模型依次检查覆盖、移动性、资源和配置等候选因素，并让每个判断引用可观察证据，模型就更难跳过关键步骤或凭空补充原因。把这些中间检查与最终答案一起用于训练，还能让模型学习“什么证据支持或排除什么假设”，从而使结果比只监督最终标签更稳定、可审计。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SEKA-FT（Structured Evidence- and Knowledge-Aligned Fine-Tuning）把电信根因分析从“输入遥测、直接预测标签”改造成统一的“证据→诊断路径→根因决策”生成任务。输入是用户面 KPI、控制面日志、邻区关系、终端状态和小区工程参数等异构信息；框架先将其整理为固定语义槽位，再要求模型生成可核查的中间诊断检查，依据检查结果排除缺乏证据的候选原因，最后输出由观测证据和领域知识共同支持的解释与根因标签。训练时，提示部分不计入损失，模型只对包含中间检查、假设收缩、解释和最终决策的结构化目标序列计算逐词元因果语言建模损失。
直观地说，该方法不是让模型“看完数据就猜答案”，而是把工程师的排障流程写进训练答案：先把杂乱数据填入统一表格，再逐项检查速度、资源、切换和覆盖距离等条件，排除不成立的原因，最后检查剩余候选是否与天线配置等工程知识一致。这种设计主要约束模型采用何种证据和推理顺序，而不是单纯依赖扩大模型或增加一段自由文本解释。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 异构故障上下文采集与任务定义

将一次 RCA 样本定义为条件生成任务：模型需要依据当前网络证据，从候选原因中识别最可能的根因，并生成对应的诊断说明。原始监督可能只有类似 $M3$ 的根因标签，因此尚不能直接表达证据如何导向决策。

<div class="method-step__io" markdown="1">

**输入**：原始电信排障输入，包括用户面性能指标、控制面信令或日志、服务小区与邻区关系、终端全局状态、轨迹事件、工程参数，以及预先给定的候选根因集合。<br>
**输出**：待标准化的故障上下文、候选根因及其监督标签。

</div>

**直观理解**：这一阶段相当于收集一张故障工单涉及的所有材料，并明确允许选择哪些故障原因；它还没有开始推理，只是确定问题和可用证据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 规范化上下文对齐

把证据归一化到固定语义块和稳定槽位，例如 Bottleneck Snapshot、UE Global State、Trajectory-Level Events 与 Serving Cell Engineering Parameters；同时删除与诊断无关的冗余片段，但保留具有因果判别价值的 KPI 和配置。相同概念在不同样本中始终出现在可比较的位置，使 Scheduled RBs、Serving SS-RSRP 等数值不再被当作脱离上下文的孤立词元。

<div class="method-step__io" markdown="1">

**输入**：格式松散、来源各异的遥测、日志、拓扑关系与配置记录。<br>
**输出**：结构一致、噪声受控的规范化 RCA 上下文。

</div>

**直观理解**：这类似于把不同厂商、不同工单格式的数据都填进同一张标准检查表。模型因而更容易知道一个数字代表什么，而不是被字段顺序或文本写法的变化干扰。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 中间检查与决策路径控制

模型先生成紧凑、可解释的诊断检查，例如 Speed_check、Low RB_check、Handover_check 和 Distance_check，并用这些检查判断移动速度、调度资源、切换稳定性和覆盖距离是否支持相应故障假设。检查结果随后用于逐步排除不受证据支持的候选原因；若某个异常已经具有决定性，也可以提前收缩推理范围。

<div class="method-step__io" markdown="1">

**输入**：规范化上下文、候选根因，以及由领域规则确定的检查维度。<br>
**输出**：一组证据派生的检查结果，以及经过剪枝的候选根因空间。

</div>

**直观理解**：它相当于先做排障清单，而不是马上选答案：车速未超阈值，就不应把高速移动作为主因；资源块充足，就应排除资源不足。这样可以降低模型凭表面关键词走捷径的概率。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 知识约束的解释生成与最终决策

第二层推理以检查结果为条件，对剩余假设进行知识驱动的细化，并生成明确引用观测指标或工程参数的解释；随后输出规定格式的最终根因标签。训练目标把检查、假设排除、解释和标签串成同一目标序列，以保留从证据到路径再到决策的依赖关系。

<div class="method-step__io" markdown="1">

**输入**：规范化证据、中间检查结果、剩余候选根因及电信工程知识。<br>
**输出**：可追溯的诊断解释和最终根因决策，例如 $M3$。

</div>

**直观理解**：当前几项常见原因被证据排除后，模型才查看剩余线索，例如机械下倾角、数字倾角和天线高度是否共同指向边缘覆盖损失。最终答案因此不仅给出“是什么”，也说明“哪些事实排除了其他答案、哪些事实支持当前答案”。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文在第 IV-D 节说明，SEKA-FT 使用逐词元因果语言建模目标训练结构化目标序列，并屏蔽提示词元，使损失只作用于模型应生成的部分。目标序列联合包含中间诊断检查、基于证据的候选排除、知识约束的假设细化和最终根因标签；因此优化并非分别训练分类器与解释器，而是让模型学习条件依赖链 $\text{evidence}\rightarrow\text{path}\rightarrow\text{decision}$。原文未给出该损失的显式公式、各部分权重或额外辅助损失，故不应补写未报告的数学形式。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Canonical Context Structuring**

该模块在输入层建立统一证据接口，将用户面指标、控制面事件、拓扑关系、移动状态和工程配置映射到固定语义块及固定槽位。其作用不是重新估计 KPI，而是控制表示方式、保留诊断信号并减少冗余，使语义等价的证据在各样本中具有一致表示。

> 直观理解：如果同一种证据每次都以不同字段名、顺序或文本形式出现，模型可能学习格式而非故障规律；标准化上下文相当于先统一工单模板。

**2. CoT-enabled Decision-Path Control**

该模块把思维链（Chain-of-Thought, CoT）用作微调监督，而不只是推理时的提示技巧。模型必须先从结构化输入生成布尔式或紧凑的诊断检查，再据此剪除高速移动、资源不足、频繁切换、过覆盖等不成立的候选假设，最后才允许产生根因标签。

> 直观理解：普通分类训练只告诉模型正确选项，不能保证它用了正确理由；决策路径监督则像要求学生写出关键判定步骤，使错误关联更容易受到约束。

**3. Evidence- and Knowledge-Anchored Explanation**

该模块将结构化目标分为两层：第一层把遥测转换为可验证的证据检查，第二层根据检查结果和领域约束细化剩余假设。解释必须锚定可观察指标、配置或事件，并与最终标签联合生成，从而提高监督密度和决策可追溯性。

> 直观理解：仅增加自由形式解释可能让模型写出听起来合理但没有数据支持的故事；该模块要求解释沿着已检查的证据展开，因此解释本身也成为训练信号。

**训练与推理**

训练阶段先把每个原始样本转换为规范化上下文，并依据可观测指标和电信知识构造两层结构化答案：第一层给出诊断检查，第二层根据检查结果排除假设、组织解释并输出标签。将规范化输入及任务指令作为提示，将完整推理与最终决策作为目标序列；微调小型 LLM 时屏蔽提示词元，只对目标词元执行自回归预测和参数更新。
推理阶段对新故障样本采用同一输入模板：首先填充瓶颈快照、终端状态、轨迹事件、邻区关系和工程参数等槽位；随后模型按训练得到的顺序生成检查结果、收缩候选集合、形成证据锚定的解释并输出规定格式的根因编号。该流程的可靠性依赖训练与推理使用一致的字段语义和候选原因定义；文中介绍的 RAG、智能体工具调用和 RLVR 是相关发展范式，但并未被描述为当前 SEKA-FT 实验流水线的组成部分。

**复现信息**

公平理解该方法所需的关键实现信息是：输入必须采用固定证据块；输出必须同时包含中间检查、知识驱动的第二步解释和最终标签；训练时提示词元应被掩蔽。示例中的检查涉及速度、调度 RB、切换次数和 UE 到服务小区的距离，并利用机械下倾角、数字倾角和天线高度等配置完成剩余假设判断。所给章节未明确报告基础模型名称、参数规模、优化器、学习率、批量大小、训练轮数、上下文长度、数据划分、检查阈值的统一构造规则或解码配置，因此无法仅凭该摘录完整复现；这些信息需要回查论文其余实验与实现章节。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- TeleLogs：论文将其作为主要评测基准，并说明每个样本包含用户面关键绩效指标、移动性统计、服务小区工程参数及对应根因标签。它主要测试模型对路测测量、邻区关系和工程配置的联合推理能力。数据集规模、训练集/验证集/测试集划分未在所给原文中明确报告。
- TelecomTS：源自实验室部署的测试床，在真实应用流量下从基站和用户设备采集高分辨率、多通道关键绩效指标。它用于检验方法在测试床时序观测和多样网络条件下的迁移表现。数据集规模与具体划分未在所给原文中明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

所有样本中最终根因标签预测正确的比例，衡量总体分类正确性。 （越高越好；它直接反映整体诊断命中率，但在类别不均衡时可能掩盖少数根因类别的表现。）

</div>
<div class="metric-item" markdown="1">

**Macro-F1**

先分别计算各根因类别的 $F1$，再对类别做等权平均；$F1$ 综合了精确率与召回率。 （越高越好；它比 Accuracy 更能反映各根因类别是否都得到较均衡的识别。）

</div>
<div class="metric-item" markdown="1">

**RCA decision-path consistency accuracy**

模型生成的中间诊断路径是否与由根因定义和确定性证据检查得到的正确检查结果一致，例如高移动速度或资源块不足。 （越高越好；它评价推理过程是否稳定、可验证，而不只是最终标签是否碰巧正确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### TeleLogs 上不同训练策略的总体诊断性能

<div class="result-value" markdown="1">

SEKA-FT 达到 Accuracy $0.942\pm0.006$ 和 Macro-F1 $0.937\pm0.007$，高于 SFT + Structured Input 的 Accuracy $0.256\pm0.018$、Macro-F1 $0.234\pm0.016$，也高于 LSTM 的 Accuracy $0.132\pm0.012$、Macro-F1 $0.090\pm0.011$。

</div>

该结果支持作者关于“结构化证据对齐加决策路径控制”有效的主张：完整方法不仅预测最终标签，也学习了中间诊断逻辑。它不能单独证明每个模块都必要，因为不同方法还可能在目标序列和监督信息上存在整体差异；此外，原文未在所给摘录中报告完整统计显著性 $p$ 值。

<div class="result-source" markdown="1">

来源：V-B Experiment Results on TeleLogs；Fig. 5(a)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

SEKA-FT achieves the best performance, reaching 0.942 ± 0.006 Accuracy and 0.937 ± 0.007 Macro-F1.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### TeleLogs 上模型规模与常规上下文学习的比较

<div class="result-value" markdown="1">

在 Regular ICL 条件下，即使使用 Qwen3-32B，Accuracy 也只有 $0.126\pm0.010$，Macro-F1 只有 $0.109\pm0.009$；作者报告轻量级 Qwen2.5-1.5B 的 SEKA-FT 明显优于所有 ICL 基线。

</div>

这表明对该任务而言，单纯增加模型参数并不能替代任务特定的结构化微调；模型需要被训练为按电信证据和诊断路径组织判断。该比较只针对 ICL，不等价于证明 $1.5$B 模型在所有任务或所有微调设置下都优于更大的模型。

<div class="result-source" markdown="1">

来源：V-B Experiment Results on TeleLogs；Fig. 5(c)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen3-32B reaches only 0.126 ± 0.010 Accuracy and 0.109 ± 0.009 Macro-F1.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### TeleLogs 上顺序诊断检查对候选根因空间的影响

<div class="result-value" markdown="1">

模型依次执行四个中间检查；在均匀根因分布假设下，候选集平均大小从初始的 $8$ 个依次降为 $6.25$、$4.75$、$3.5$ 和 $2.5$ 个。

</div>

该分析说明结构化检查可以在最终分类前逐步排除不符合证据的假设，从而降低决策复杂度。它是基于候选空间的机制性分析，不是独立的准确率证明；其中“均匀根因分布”是解释平均候选数的假设，实际数据分布下的收益可能不同。

<div class="result-source" markdown="1">

来源：V-B Experiment Results on TeleLogs；Fig. 5(f)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under a uniform root-cause distribution, the average candidate-set size decreases from 8 to 6.25, 4.75, 3.5, and 2.5 after the first through fourth checks, respectively.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验摘录没有报告 TeleLogs 和 TelecomTS 的样本规模、训练/验证/测试划分，也没有给出 TelecomTS 的具体主结果，因此跨数据集泛化能力无法从当前证据中独立核查。
- 结果主要来自两个 $5G$ 根因分析基准和 Qwen 系列模型；虽然报告了多随机种子、置信区间及显著性检验方案，但原文摘录未提供完整检验结果、各类别样本分布或真实运营网络部署评估，因此不能直接推断对其他厂商、网络制式或线上故障场景同样有效。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Regular ICL：不进行监督微调，直接通过上下文示例提示模型；用于检验仅扩大模型或提供上下文是否足以完成电信根因分析。
- LSTM：非大语言模型的序列分类基线；用于比较传统时序建模方法与语言模型方法在该任务上的差异。
- Vanilla SFT：使用 TeleLogs 原始输入输出进行监督微调；用于隔离“直接把原始数据用于微调”这一朴素方案的效果。
- SFT + Structured Input：在监督微调中加入规范化、结构化输入；用于检验统一网络上下文表示本身的作用。

**实验想回答的问题**

- 在 TeleLogs 与 TelecomTS 两个具有不同证据形态的 $5G$ 根因分析数据集上，SEKA-FT 是否比直接上下文学习、序列分类和不同形式的监督微调获得更高的诊断准确性与宏平均 $F1$？
- 将规范化网络上下文、诊断路径和证据支撑解释联合纳入训练，是否能改善中间决策路径的一致性，并降低最终根因判断的候选空间？

**实验实现**

主模型为 Qwen2.5-1.5B-Instruct；另用 Qwen2.5-7B-Instruct 与 Qwen3-32B 检验模型规模影响。SEKA-FT 的监督目标由原始根因标签、基准定义的诊断检查和自动生成的证据支撑解释构成，目标序列包含中间诊断路径、假设细化解释和最终根因决策。适用时，各监督微调方法使用 SFT；LoRA 作用于最后四个 Transformer 模块，训练采用因果语言模型损失并屏蔽提示词标记，学习率为 $1\mathrm{e}{-5}$，训练 $12$ 个 epoch，批大小为 $2$，最大序列长度为 $2048$，使用梯度裁剪和 bf16 混合精度，并在 Nvidia RTX 6000 Ada 上实现。所有结果均为不同随机种子的 $10$ 次独立运行平均值，并报告 $95\%$ 置信区间；置信区间基于样本均值和标准差的 Student $t$ 区间。Accuracy 使用精确 McNemar 检验，Macro-F1 使用配对置换检验，多重比较通过 Holm–Bonferroni 校正。所给原文未提供 TeleLogs 与 TelecomTS 的具体样本数量、数据划分、完整表格数值及 TelecomTS 的分数据集结果。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 去除结构化输入：Vanilla SFT 对比 SFT + Structured Input | Vanilla SFT 的 Accuracy 为 $0.007\pm0.003$、Macro-F1 为 $0.013\pm0.004$；SFT + Structured Input 分别提高到 $0.256\pm0.018$ 和 $0.234\pm0.016$。 | 这一对比主要隔离规范化网络上下文的作用。性能提升说明把异构遥测整理为统一、可解释的上下文，有助于模型识别跨层证据；但由于这是训练方案整体变化，不能把增益严格归因于某一个具体字段或单一格式设计。 | V-B Experiment Results on TeleLogs；Fig. 5(a)<br><span class="experiment-evidence">SFT + Structured Input improves performance to 0.256 ± 0.018 Accuracy and 0.234 ± 0.016 Macro-F1, confirming the benefit of canonical context structuring, but remains substantially below SEKA-FT.</span> |
| 去除完整决策路径控制：SFT + Structured Input 对比 SEKA-FT | SFT + Structured Input 的 Accuracy 为 $0.256\pm0.018$、Macro-F1 为 $0.234\pm0.016$；加入完整 SEKA-FT 设计后分别达到 $0.942\pm0.006$ 和 $0.937\pm0.007$。 | 该比较说明仅提供结构化输入仍不足以获得稳定诊断，显式训练中间检查、假设细化和最终决策的联合序列可能是关键补充。由于摘录未给出逐模块消融，例如分别去除解释监督或路径控制，因此不能确定完整模型增益由哪一个内部组件单独贡献。 | V-B Experiment Results on TeleLogs；Fig. 5(a)<br><span class="experiment-evidence">SEKA-FT achieves the best performance, reaching 0.942 ± 0.006 Accuracy and 0.937 ± 0.007 Macro-F1.</span> |

**定性案例**

- 按根因类别的分析显示，覆盖与邻区相关故障最容易混淆：过度下倾、较强邻区选择和覆盖重叠可能共同产生相似的 $RSRP/SINR$ 与邻区观测。该案例说明剩余错误具有明确的电信语义，反映的是证据模式重叠，而不是完全随机的分类失败。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper proposes a structured, evidence-grounded reasoning framework that improves LLM diagnostic accuracy and consistency in telecom root-cause analysis.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`743811a3640cbb70364540f7a7998dad624e98aac82f6ef2f401b58fb83119aa`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
