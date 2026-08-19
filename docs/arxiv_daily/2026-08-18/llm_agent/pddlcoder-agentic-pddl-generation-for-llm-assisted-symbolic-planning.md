---
title: "[论文解读] PDDLCoder: Agentic PDDL Generation for LLM-Assisted Symbolic Planning"
description: "[arXiv 2608.16637][LLM Agent] 原文未明确报告。"
arxiv_id: "2608.16637"
announcement_date: "2026-08-18"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:17:19.591383+00:00"
source_sha256: "2b7e9a3bdbf4bf864335f8f1b6b1dd97a5968d5876fb47115440a339d59347b1"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "自动规划"
  - "大语言模型"
  - "PDDL"
  - "符号规划"
  - "智能体式生成"
  - "计划适用性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.16637</p>

# PDDLCoder: Agentic PDDL Generation for LLM-Assisted Symbolic Planning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Veit Laule, Jiangtao Shuai, Manfred Hauswirth, Sonja Schimmler</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Technical University of Berlin；Affiliation: Fraunhofer FOKUS & Technical University of Berlin</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.16637) · [PDF 下载](https://arxiv.org/pdf/2608.16637) · **关键词** 自动规划, 大语言模型, PDDL, 符号规划, 智能体式生成, 计划适用性<br>
**代码**: [https://github.com/vDawgg/PDDLCoder](https://github.com/vDawgg/PDDLCoder)

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

自动规划研究如何找到一串动作，使环境从初始状态转变为满足目标条件的状态。由于每个动作都会改变后续动作所依赖的状态，长程规划不仅需要理解任务语义，还必须持续满足动作前置条件并正确推演效果。本文关注“大语言模型辅助的符号规划”：大语言模型不直接生成最终动作序列，而是把自然语言任务形式化为规划领域定义语言（PDDL）中的领域与问题文件，再交给 Fast Downward 等符号规划器搜索计划；所得计划还需在与原始任务对应的可执行环境中验证，以判断形式化模型和计划是否真正符合任务。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自动规划**

给定环境的初始状态、目标条件和可执行动作，自动规划器搜索一条能将初始状态推进到目标状态的动作序列。动作通常具有前置条件和效果：只有前置条件成立时才能执行，执行后会改变环境状态。

</div>
<div class="concept-item" markdown="1">

**规划领域定义语言（PDDL）**

PDDL 是描述符号规划任务的形式语言，通常将领域文件与问题文件分开：前者定义对象类型、谓词和动作模式，后者给出具体对象、初始状态与目标。其明确的形式结构允许解析器检查语法，并允许专用规划器执行可验证的搜索。

</div>
<div class="concept-item" markdown="1">

**计划适用性**

计划适用性是指动作序列能否从真实任务的初始状态开始逐步合法执行，并最终满足目标，而不只是文本格式正确或能被某个生成的 PDDL 模型接受。本文通过匹配的 pddlgym 可执行环境模拟动作，以检验计划相对于原始任务是否成立。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是自然语言形式的领域描述与具体问题描述，记为 $(D_{NL},P_{NL})$，并包含自然语言动作模式；系统不获得预定义的 PDDL 领域、问题、谓词、前置条件或效果，也不依赖生成过程中的人工反馈。目标是自动构造相互一致的 PDDL 领域文件和问题文件，调用符号规划器生成动作计划，再把该计划映射为仿真环境可执行的动作格式。最终输出不是仅通过语法检查的 PDDL，而是在对应 NL-pddlgym 环境中能够从初始状态执行至目标状态的适用计划；因此该设置同时考查自然语言语义形式化、形式规范一致性、符号搜索以及面向原始任务的执行验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D_{NL}$**

自然语言给出的规划领域描述，包括环境概念和动作模式。

</div>
<div class="notation-item" markdown="1">

**$P_{NL}$**

自然语言给出的具体规划问题描述，包括当前情境与目标。

</div>
<div class="notation-item" markdown="1">

**$(D_{NL},P_{NL})$**

PDDLCoder 接收的一组自然语言领域与问题输入。

</div>

</div>

**直接相关的工作**

- **NL2PDDL**: 同样从自然语言重建 PDDL，但为缓解上下文窗口压力而采用按动作拆分的固定生成流程。PDDLCoder所研究的差异在于让智能体依据工具反馈自主决定生成与修订步骤，而非预先规定完整的细化路径。
- **NL2Plan**: 能够从较少文本端到端生成 PDDL 领域和问题，但仍采用分阶段的信息抽取流程并只进行一次修复。它构成本文最直接的任务级参照之一，因为本文也要求同时生成领域与问题，但进一步强调自主迭代和可执行环境中的计划适用性验证。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

长时序规划要求系统先准确理解环境中的对象、动作及状态变化，再生成一串彼此衔接且最终满足目标的动作。直接让大型语言模型（LLM）从自然语言描述生成动作序列时，模型必须同时完成环境建模、长程推理和动作有效性维护，容易产生违反前置条件、无法执行或不能达到目标的计划。将自然语言转化为规划领域定义语言（PDDL），再交由符号规划器生成计划，可以把复杂推理交给形式化工具，并为计划验证提供明确依据；但这一方向仍需要一种能够从自然语言自动构造可靠规划模型、并以真实执行结果检验模型质量的方法。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **直接 LLM 规划器（LLM-Planners）**：系统直接输入自然语言任务描述，由 LLM 生成动作序列，通常不显式构造环境状态、动作前置条件和动作效果的形式化模型。其优点是流程简单、无需额外规划器，但模型需要在生成过程中自行保持每一步动作的合法性和长期目标的一致性。
- **LLM 形式化器（LLM-Formalizers）**：系统先让 LLM 将自然语言任务转写为 PDDL，包括对象、谓词、初始状态、目标、动作及其前置条件和效果；随后使用符号规划器（如 FD）在该形式化模型上搜索计划。符号规划器能够保证计划相对于所给 PDDL 模型是可行的，但最终结果仍取决于 LLM 是否准确表达了原始自然语言任务。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 许多 LLM 形式化方法依赖预先规定的生成流程和固定的细化步骤，模型只能按照设计好的阶段执行，难以根据当前错误类型自主决定下一步应检查或修改什么。这会限制其处理不同任务结构和复杂逻辑错误的能力；论文将 PDDLCoder 的设计对比为能够自主调用工具并迭代修改的编码代理。
- 部分方法依赖已有的部分形式化信息（例如预定义领域），或需要人工反馈来修正生成结果；这削弱了从自然语言零样本构建完整规划模型的实用性。与此同时，已有评估常停留在语法有效等中间属性，而没有直接检验生成的规格说明能否在原始任务环境中产生可执行计划，因此语法正确并不等于任务真正完成。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未充分解决这样一个完整闭环问题：在不提供预定义 PDDL 领域、谓词、动作前置条件或效果、也不依赖人工反馈的条件下，系统能否自主生成并反复修正完整规划规格说明，并通过外部工具和执行环境验证其计划确实适用于自然语言所描述的任务。更具体地说，研究缺少同时具备自主迭代形式化能力与自动执行验证机制的统一框架，也缺少能够跨领域、以计划适用性为最终标准的可复现实验基准。

</div>
<div markdown="1"><span>核心问题</span>

仅根据自然语言任务描述和动作模式，LLM 是否能够通过自主调用创建、读取、编辑、语法检查、规划求解及计划反馈等工具，迭代生成足以支持符号规划的完整 PDDL，并在未见领域上产出真正可执行且满足任务目标的计划？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把 PDDL 生成视为一种带工具反馈的结构化代码生成任务，而不是一次性文本翻译。LLM 先提出规划规格说明，再借助语法检查器和规划器发现形式错误或不可求解问题，并根据计划反馈继续读取、编辑和重写相关文件；当生成的计划被映射回可执行形式后，环境还能直接检查每个动作是否适用。这样的迭代过程相当于让模型在执行结果约束下逐步排除错误，降低一次生成必须同时完成建模与验证的压力。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PDDLCoder解决的是“从抽象自然语言联合生成PDDL领域文件与问题文件，并据此得到可执行计划”的任务。输入包括领域描述$D_{NL}$、问题描述$P_{NL}$、目标环境采用的最小动作模式集合$S$以及对象集合$O$；其中自然语言只说明任务背景、可用动作名称、对象、初始状态和目标，刻意隐藏谓词签名、动作参数、前置条件与效果。系统以ReAct智能体为控制器，在最多50轮交互中自主选择文件创建、读取、编辑、语法检查、规划和计划语义反馈等工具，逐步形成PDDL领域$D$与问题$P$。终止后，系统再次验证$D$和$P$并调用经典规划器生成原始计划$\pi$；若成功，再由MapAgent把它转换为符合环境接口的映射计划$\pi_m$，供最终执行评测。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造低规格形式化输入

将$D_{NL}$和$P_{NL}$作为PDDL生成的主要语义依据，其中只保留任务设定、动作名称、对象、初始状态和目标，不提供谓词、动作完整参数、前置条件或效果。$S$仅列出目标环境执行动作绝对必要的动作名和参数名，用于后续接口映射，而不是直接给出完整PDDL语义。

<div class="method-step__io" markdown="1">

**输入**：抽象领域描述$D_{NL}$、抽象问题描述$P_{NL}$、最小目标动作模式$S$与对象集合$O$。<br>
**输出**：供主智能体使用的自然语言形式化任务，以及供映射阶段使用的接口约束$S$和对象表$O$。

</div>

**直观理解**：系统拿到的是一份不完整的需求说明，而不是现成的逻辑模型；它必须自己推断“哪些事实需要记录”和“每个动作何时可做、做完改变什么”。$S$类似目标程序接口的最小函数签名，只保证最后生成的动作能够被环境接收。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 智能体迭代生成与编辑PDDL

DSPy实现的ReAct控制器根据当前文件和历次工具反馈，自主选择创建、读取或编辑操作；编辑先在内存中应用，再由VAL解析器验证，语法不合法时拒绝写入并返回诊断。循环持续到智能体显式宣布完成或达到50轮硬上限。

<div class="method-step__io" markdown="1">

**输入**：$D_{NL}$、$P_{NL}$、通用PDDL编写指南，以及当前工作区中的领域文件$D$和问题文件$P$。<br>
**输出**：不断修订的PDDL领域$D$和问题$P$，以及每次操作产生的结构化错误信息。

</div>

**直观理解**：这一阶段类似带编译检查的代码代理：模型不是一次性写完两个文件，而是观察当前版本、修改局部内容并根据报错继续处理。编辑前验证可避免一次错误修改直接破坏已经可解析的文件。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按失败状态调用符号反馈工具

智能体可调用VAL获得带行号和上下文的语法错误，也可调用Fast Downward的翻译阶段实施更严格的规划前检查；文件可用后，系统以Fast Downward的`lama-first`配置尝试生成$\pi$。若问题被判定不可解，工具提取可达实例化原子数、实例化动作数、因不可能前置条件或效果而删除的动作数，以及目标可满足性等可操作信息；超时或超内存则直接报告对应限制。

<div class="method-step__io" markdown="1">

**输入**：当前候选$D$与$P$，以及此前的语法错误、翻译结果或规划失败报告。<br>
**输出**：语法诊断、翻译诊断、规划失败摘要，或由符号规划器找到的原始计划$\pi$。

</div>

**直观理解**：不同失败需要不同工具：括号、类型或名称错误由解析器定位，逻辑上无解则由规划器解释搜索前处理发现的问题。控制器依据当前状态选择下一步，因此不必让每个实例都机械经历相同的固定修复顺序。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 映射计划并进行自然语言语义反馈

MapAgent根据$S$、$O$、$D$和$\pi$生成接口兼容的映射计划$\pi_m$；随后PlanAgent仅接收$D_{NL}$、$P_{NL}$、$S$和$\pi_m$，检查动作序列是否违反自然语言中显式或隐含的任务约束。PlanAgent被刻意隔离于生成的$D$和$P$之外，其反馈返回主智能体，后者可在总轮次预算内多次修订形式模型并重新规划。

<div class="method-step__io" markdown="1">

**输入**：已生成的原始计划$\pi$、领域文件$D$、最小动作模式$S$、对象集合$O$，以及自然语言描述$D_{NL}$和$P_{NL}$。<br>
**输出**：与目标执行接口一致的候选计划$\pi_m$，以及针对语义不可行步骤的可操作反馈。

</div>

**直观理解**：符号规划器只能保证计划符合模型自己写下的规则，却不能保证这些规则正确表达原任务；PlanAgent相当于独立审阅者，专门检查计划是否“合乎题意”。先映射再审阅还能让它看到环境实际会执行的动作形式，而非参数可能冗余的内部计划。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。原文方法章节没有提出可训练损失函数，也没有报告对主语言模型、MapAgent或PlanAgent进行参数更新；PDDLCoder属于推理时智能体编排方法，优化来自同一次任务内对文件、工具结果和反馈的迭代，而不是梯度下降。其操作目标可概括为获得语法有效、可由经典规划器求解且最终计划可在目标动力学中执行的$D$、$P$和$\pi_m$，但这只是系统成功条件，并非论文定义的数学训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. ReAct主控制器与CRU文件工具**

主控制器由DSPy中的ReAct实现，维护不断演化的工作区，并在创建、读取、编辑和各种反馈工具之间动态决策。CRU工具被限制为操作PDDL文件；其中编辑采用“内存修改、VAL验证、合法后返回”的事务式流程，非法编辑不会直接落入当前文件。

> 直观理解：该模块负责决定“现在最值得做什么”，使语法错误、模型不可解和计划语义错误能够走不同修复路径。受验证保护的编辑机制则相当于每次改代码前先做快速编译，降低连续修改造成的错误累积。

**2. VAL与Fast Downward符号反馈栈**

VAL提供带行号和文件上下文的PDDL解析诊断；Fast Downward同时承担更严格的翻译检查和计划生成，规划配置为`lama-first`，目标是快速返回第一条计划而非保证最优。单次规划运行限制为1分钟和4 GB内存，并将冗长的不可解输出压缩为可达原子、实例化动作、被删除动作及目标可满足性等摘要。

> 直观理解：VAL主要回答“文件写得是否合法”，Fast Downward进一步回答“这个逻辑模型能否真正产生计划”。这里追求的是高频、可解释的修复反馈，因此选择快速找到任意可行计划，而不是耗费更多资源寻找最短或成本最低计划。

**3. MapAgent与PlanAgent**

MapAgent接收$S$、$O$、生成的$D$和原始计划$\pi$，把生成PDDL中自行选择的动作参数投影为环境要求的最小接口，得到$\pi_m$。PlanAgent只依据$D_{NL}$、$P_{NL}$、$S$和$\pi_m$推断自然语言约束并定位不合理动作，不读取$D$与$P$，从而避免被待检查形式模型中的错误规则诱导。

> 直观理解：MapAgent解决“内部表示与外部执行接口不同”的问题，例如内部`move`可同时记录起点和终点，而环境可能只需要目标位置。PlanAgent解决“模型内部自洽但理解错题”的问题，例如PDDL漏写堆叠约束时，规划器可能允许移动被其他环压住的环，而语义审阅仍可指出这一物理冲突。

**训练与推理**

训练方面，原文未描述为PDDLCoder微调任何模型；NL-pddlgym的语言侧数据构造也不等于方法训练：作者人工撰写23个领域描述及每个领域2至3个种子问题描述，再用DeepSeek v4 Flash依照种子模式生成其余问题描述，同时要求保留源PDDL中的对象、初始状态和目标。数据集完整保留四个领域作为测试集，其余领域组成面向未来方法开发的训练与验证划分，测试领域不出现在这些划分中。

推理时，每个实例从$D_{NL}$、$P_{NL}$和通用PDDL指南开始，ReAct智能体在工作区中创建并迭代修改$D$和$P$。它可根据当前失败自主调用VAL、Fast Downward翻译、Fast Downward规划或计划反馈，不受预先固定的修复顺序约束；PlanAgent反馈可以在总预算内重复调用。达到显式完成信号或50轮上限后，系统执行统一语法验证和规划：若成功，则MapAgent利用$S$、$O$、$D$与$\pi$生成并保存$\pi_m$；若失败，则保留语法或规划失败状态。最后，评测器而非生成智能体在隐藏pddlgym环境中顺序执行$\pi_m$，以动作全部可应用且终态达成目标作为成功条件。

**复现信息**

复现时最关键的控制条件有四项。第一，主代理采用DSPy的ReAct实现，并设置最多50次工具交互，以限制上下文消耗；这一上限同时约束语法修复、规划尝试和PlanAgent的重复反馈。第二，语法反馈由VAL与Fast Downward翻译阶段共同提供：前者诊断细致，后者代表生成计划前必须通过的更严格检查。第三，计划生成使用Fast Downward的`lama-first`配置，每次运行最多1分钟、4 GB内存；因此实验衡量的是在受限反馈循环中能否找到一条计划，不应解释为最优规划能力比较。第四，MapAgent与PlanAgent的输入边界必须保持一致：MapAgent可见$S$、$O$、$D$和$\pi$，PlanAgent只可见$D_{NL}$、$P_{NL}$、$S$和$\pi_m$，而最终gym环境在生成阶段完全不可见。

任务范围限于完全可观测、确定性的经典规划，论文将概率领域及其他PDDL扩展留作未来工作。NL-pddlgym中的领域被限制在`typing`、`strips`、`disjunctive-preconditions`、`conditional-effects`、`negative-preconditions`和`equality`需求范围内。基准包含23个领域、711个问题，每个问题有3至310个对象；这些规模信息影响上下文长度、规划成本及计划长度，应在复现实验资源配置和失败分析中保留。最终评测只判断计划适用性，不声称生成PDDL与参考PDDL语义等价，因为隐藏谓词和动作细节允许同一自然语言任务存在多种有效形式化。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- NL-pddlgym测试集：包含训练及其他数据划分中未出现的4个领域，共106个问题变体；对象数量随问题变化，对应计划长度为2至557步。该测试集用于检验方法对未见领域的泛化，而不是对同领域新实例的拟合。
- 4个测试领域分别是经典规划领域Hanoi、Elevator和Satellite，以及作者为该数据集新建的Ring and Peg。分领域成功率用于观察方法是否只在少数领域有效，并揭示领域约束带来的差异，例如Hanoi要求移动动作的目的地必须是柱子。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**PDDL生成等级L0至L3**

分阶段衡量输出质量：L0表示没有语法有效的PDDL；L1表示PDDL语法有效但规划器找不到计划；L2表示获得了不可适用的计划；L3表示计划中的动作依次可执行，且终止动作执行后满足目标。对不生成PDDL的LLM-Planner，只使用L2和L3区分失败计划与成功计划。 （等级越高越好，其中L3是端到端成功标准；各等级计数还能定位失败发生在语法、可解性还是执行语义阶段。）

</div>
<div class="metric-item" markdown="1">

**Level-3成功率**

在全部问题或特定领域中达到L3的比例，即生成的最终计划可在相应环境中执行并解决问题。这是论文比较方法有效性的主要指标。 （越高越好，因为只有L3同时要求动作序列可适用并最终满足目标。）

</div>
<div class="metric-item" markdown="1">

**平均输入与输出Token数**

分别报告每个问题消耗的平均输入Token和输出Token，并附标准差，用于描述推理成本及波动。输入Token包含较长的工具输出、完整PDDL文件或计划，输出Token反映模型实际生成内容的规模。 （在成功率相近时越低通常越好；但输入与输出Token代表不同成本来源，不能脱离成功率单独判断方法优劣。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### PDDLCoder搭配6种开放权重模型，在NL-pddlgym全部106个测试问题上评估

<div class="result-value" markdown="1">

DeepSeek v4 Flash得到95个L3、9个L2、2个L1和0个L0，整体L3成功率为89.6%；分领域成功率为Elevator 90%、Hanoi 75%、Ring and Peg 93.3%、Satellite 94.4%。Gemma 4 31b和gpt-oss-120b分别得到65个与56个L3，而Llama 4 Scout没有问题达到L3。

</div>

结果说明PDDLCoder在能力较强的模型上可以覆盖多数未见领域问题，但并非与底层模型无关。较弱模型常在生成语法有效PDDL之前失败，另一些模型虽通过语法检查，却不能根据计划反馈修正语义错误。该单次运行比较支持“模型能力显著影响代理流程”的判断，但不能将差异明确归因于参数规模、训练数据或指令遵循能力。

<div class="result-source" markdown="1">

来源：表3，Results Across Models

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

DeepSeek v4 Flash | 0 | 2 | 9 | 95 | 90 | 75 | 93.3 | 94.4 | 172978.8 | 234922.6 | 32809.4 | 32990.4

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### PDDLCoder与LLM形式化基线NL2Plan、VML_PDDL，以及直接规划基线COT、ISR-LLM比较

<div class="result-value" markdown="1">

PDDLCoder的L3成功率为89.6%，高于NL2Plan的45.3%、VML_PDDL的34.9%、COT的74.5%和ISR-LLM的69.8%。相对最强对比方法COT，绝对提升为15.1个百分点。

</div>

该结果表明，在统一测试集和统一计划映射条件下，先生成并借助符号工具反复修正PDDL，比所测试的直接规划提示及既有形式化流程更容易得到可执行的成功计划。不过，VML_PDDL经过候选选择机制适配，各方法也只运行一次，所以这些数字不构成对原方法所有实现或随机运行分布的全面结论。

<div class="result-source" markdown="1">

来源：第4.2节 Comparison with Previous Approaches，表4相关正文

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

PDDLCoder achieves a level-3 success rate of 89.6%, compared with 45.3% for NL2Plan, 34.9% for VML_PDDL, 74.5% for COT, and 69.8% for ISR-LLM.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 使用NL-pddlgym真实PDDL文件生成的正确未映射计划，单独验证MapAgent

<div class="result-value" markdown="1">

在初始未映射计划正确的前提下，MapAgent映射后的计划有98.1%能在对应gym环境中成功解决问题。

</div>

这一控制实验说明计划映射通常可靠，因此主实验中的大量失败不太可能全部由动作名称映射造成；但98.1%并非100%，映射仍会给端到端成功率引入少量误差。该结果只验证“输入计划本身正确”时的映射，不代表MapAgent能够修复错误计划。

<div class="result-source" markdown="1">

来源：第4节 Evaluation，MapAgent独立验证段落

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

After applying each of the generated plans to the appropriate gym environments, we found that the mapped plans yielded a 98.1% success rate in solving the problem given a correct initial unmapped plan.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 每个模型、问题和配置仅评估一次，论文明确未量化不同采样运行之间的方差；模型排序、领域级反常变化及消融差值都可能包含随机性，尤其不宜据此作显著性判断。
- 比较并非完全原样复现所有基线：VML_PDDL因DeepSeek API限制改用LLM生成评分进行Best-of-N选择；同时刚性执行消融与代理式流程的交互预算未严格匹配，ISR-LLM又因日志限制缺少Token统计。因此成功率比较较有参考价值，但效率与机制归因仍需额外受控实验。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- NL2Plan：既有LLM-Formalizer方法，将自然语言任务转换为形式化规划表示；它是判断PDDLCoder的代理式反馈与修正机制是否优于既有PDDL生成流程的直接基线。
- VML_PDDL：另一种LLM-Formalizer方法。由于DeepSeek API限制，实验将原方法基于对数概率的Best-of-N候选选择改为LLM生成评分，因此比较对象是适配版本，不能完全等同于原论文实现。
- COT：使用思维链提示直接产生计划的LLM-Planner基线。它不生成PDDL，因而比较的是最终计划能否执行并达成目标，而不是形式化文件质量。
- ISR-LLM self-validator：带自验证机制的LLM-Planner基线，采用来自Blocksworld领域的少样本提示；它检验PDDLCoder的外部符号规划和工具反馈是否优于语言模型自行生成、检查计划。

**实验想回答的问题**

- PDDLCoder能否在不同开放权重大语言模型上稳定生成语法有效、可规划且最终可执行的PDDL，其主要性能瓶颈位于语法生成、规划可解性还是计划适用性？
- 与既有LLM形式化方法和直接规划方法相比，PDDLCoder是否提高了任务成功率；其计划反馈、计划映射和自适应工具选择分别贡献了多少？

**实验实现**

每个模型、问题和方法配置只运行一次，因此结果覆盖106个问题，但没有通过重复采样估计随机波动。对比方法采用原论文给出的最佳配置，包括原始提示、候选数量、迭代上限和停止条件，并统一使用PDDLCoder的计划映射方式，以减少自然语言动作到环境动作转换差异造成的不公平。DeepSeek v4 Flash通过OpenRouter运行，温度与Top-P均为1.0；其余模型在4张NVIDIA H100 GPU的服务器上通过vLLM本地部署，并采用各模型作者建议的采样参数。作者还用真实PDDL产生的计划单独测试MapAgent，以区分映射错误与PDDL生成错误。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Rigid Execution：保留相同代理与工具，但用预先规定的逐步流程和固定反馈循环替代自适应工具选择 | Rigid Execution仅有60个L3，而完整PDDLCoder有95个L3；其分领域成功率分别为50%、60%、46.7%和66.7%，均低于完整方法的90%、75%、93.3%和94.4%。刚性流程平均输出57247.8个Token，完整方法为32809.4个，即完整方法只消耗前者57.3%的平均输出Token。 | 该消融主要隔离执行方式：工具集合基本不变，但系统不能根据当前错误灵活决定下一步。结果支持自适应编排能减少无关的整文件重生成，并提高成功率。不过两种流程的交互预算并未严格匹配，作者也承认还可设计其他刚性流程，因此这只是自适应执行有效的初步证据。 | 表5，Rigid Execution消融<br><span class="experiment-evidence">Rigid Execution \| 19 \| 2 \| 25 \| 60 \| 50 \| 60 \| 46.7 \| 66.7 \| 39319.1 \| 31494.2 \| 57247.8 \| 43709.1</span> |
| Without PlanAgent：移除对映射后计划进行检查并生成反馈的PlanAgent | 移除PlanAgent后，L3数量由95降至73，L2由9升至28；Ring and Peg成功率从93.3%降至40%，Satellite从94.4%降至72.2%，但Hanoi从75%升至85%，Elevator保持90%。 | L2显著增加说明PlanAgent的核心价值是发现“规划器给出了计划，但该计划不能在目标环境中正确执行”的语义问题，并把问题反馈给PDDL修正过程。影响具有领域差异，尤其Ring and Peg依赖该反馈；Hanoi的反向变化提醒读者，单次随机运行和代理反馈本身的噪声可能导致局部领域并非单调改善。 | 表5，Without PlanAgent消融<br><span class="experiment-evidence">Without PlanAgent \| 3 \| 2 \| 28 \| 73 \| 90 \| 85 \| 40 \| 72.2 \| 74907.8 \| 65274.9 \| 15127.5 \| 11861.2</span> |

**定性案例**

- Hanoi领域暴露了语义对齐失败：自然语言描述要求move动作的目的地必须是柱子，但部分模型最初生成的PDDL不满足该约束，并在预算耗尽前始终未能修正。这个案例说明“语法有效”不等于“忠实表达自然语言领域规则”，也解释了为何需要规划与执行反馈共同检查生成结果。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops an agentic LLM method for generating PDDL representations to support symbolic planning.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`2b7e9a3bdbf4bf864335f8f1b6b1dd97a5968d5876fb47115440a339d59347b1`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
