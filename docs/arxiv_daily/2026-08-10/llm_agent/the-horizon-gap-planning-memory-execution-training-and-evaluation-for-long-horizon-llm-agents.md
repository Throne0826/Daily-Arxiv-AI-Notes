---
title: "[论文解读] The Horizon Gap: Planning, Memory, Execution, Training, and Evaluation for Long-Horizon LLM Agents"
description: "[arXiv 2608.06663][LLM Agent] 本文提出“视野鸿沟”这一诊断框架，系统梳理长时程大语言模型智能体为何会在多步骤任务中失去可靠性，以及研究界如何以更密集的过程信号应对该问题。"
arxiv_id: "2608.06663"
announcement_date: "2026-08-10"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-10T02:38:20.885383+00:00"
source_sha256: "29847547def327b579fbf007e4d5f43c98b668a06339e4ec4786d358f0db4ca9"
tags:
  - "LLM Agent"
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "长时域大语言模型智能体"
  - "horizon gap"
  - "长期记忆"
  - "轨迹级评估"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.06663</p>

# The Horizon Gap: Planning, Memory, Execution, Training, and Evaluation for Long-Horizon LLM Agents

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-10</span>
<span><strong>作者</strong> Mingguang Chen, Licheng Wang, Bo Qu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.06663v1) · [PDF 下载](https://arxiv.org/pdf/2608.06663v1) · **关键词** 长时域大语言模型智能体, horizon gap, 长期记忆, 轨迹级评估<br>


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

本文提出“视野鸿沟”这一诊断框架，系统梳理长时程大语言模型智能体为何会在多步骤任务中失去可靠性，以及研究界如何以更密集的过程信号应对该问题。

**不用术语来说**：一个模型即使能独立答对复杂问题，也不代表它能持续数小时完成真实任务。任务变长后，它可能忘记早先决定、误以为工作已经完成，或逐步偏离最初目标；而普通的一次性对错测试往往看不出这些失败。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 明确区分长时程、长上下文和长期记忆：前者描述任务需要多少步骤，后两者分别描述模型单次可处理的文本容量与系统能否跨步骤或跨会话保存信息，避免将三者混为同一能力。
- 以规划、记忆、执行、训练、评估及基础与安全六类工作组织文献，并提出跨类别判断：随着任务时程增长，单一终局奖励或通过/失败信号会失去诊断力，研究需要构造步骤级过程信号。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究长时域大语言模型智能体，即由语言模型、工具调用、记忆机制和控制循环组成的系统，如何在需要持续数分钟至数小时、包含大量连续步骤的任务中保持目标一致并可靠完成工作。单步推理能力与多步任务可靠完成能力之间的差距被称为“horizon gap”。理解这一问题需要区分任务所要求的步骤数量、模型一次能够处理的令牌数量，以及系统能否跨步骤或跨会话保存信息；三者分别对应长时域、长上下文和长期记忆，并不是同一个属性。本文是系统性综述，收集并筛选了 $1{,}547$ 篇 $2024$ 至 $2026$ 年的 arXiv 论文，按照任务生命周期将研究组织为规划与分解、记忆与上下文管理、执行控制与恢复、长时域训练、评估与测量，以及基础理论、局限性与安全六类。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**长时域任务**

长时域描述的是任务本身：任务需要多少个相互依赖的步骤才能完成，而不是模型能读多少文本。例如一个持续数小时的软件工程任务，其最终结果依赖许多中间决策和操作。

</div>
<div class="concept-item" markdown="1">

**长上下文**

长上下文描述模型在一次输入中能够同时关注的令牌数量。它可以帮助模型看到更长的历史，但并不保证模型会正确提取早期决定、维持目标或可靠执行后续步骤。

</div>
<div class="concept-item" markdown="1">

**长期记忆**

长期记忆描述智能体系统是否能把信息保存到当前上下文之外，并在后续步骤、任务或会话中再次使用。它是系统设计属性，不能仅由模型的上下文窗口长度推出。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文将问题抽象为：给定一个需要连续执行多个步骤的任务、初始目标、可用环境或工具，以及由大语言模型驱动的智能体系统，系统需要生成并执行一条跨越较长时间的行动轨迹，最终输出满足任务要求的结果。系统还必须处理历史信息、计划变化、执行失败和中间状态；其可靠性不能只由最终成功或失败判断，因为随着步骤数量增加，单个最终信号越来越难以说明错误发生在哪里。综述关注的核心设定是模型嵌入智能体循环后，在上下文容量有限、任务状态持续变化、工具可能失败且评估信息不完整的条件下，如何实现可持续的目标跟踪和任务完成。文献还将“承载时域”的位置作为第二个组织轴：时域可以位于单一上下文内、由超出上下文窗口的任务级控制框架承载，或通过持久化机制跨任务与会话承载。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$H$**

任务的时域，可理解为完成任务所需的步骤数量或持续时间；原文主要以自然语言定义该概念，未给出统一的形式化符号。

</div>
<div class="notation-item" markdown="1">

**$C$**

模型一次可处理的上下文容量，通常以令牌数量衡量；原文未明确规定统一符号，此处用于说明长上下文与任务时域的区别。

</div>
<div class="notation-item" markdown="1">

**$M$**

系统的长期记忆状态，用于表示跨步骤或跨会话保存并重新取用的信息；原文未给出统一数学记号。

</div>
<div class="notation-item" markdown="1">

**$\tau_{1:T}$**

从第 $1$ 步到第 $T$ 步的任务执行轨迹，包括中间行动、观测和状态变化；原文未给出该统一记号，但轨迹级诊断是其讨论的核心对象。

</div>

</div>

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现实部署需要智能体在软件工程等持续数小时的任务中稳定推进，而非只在单轮推理中给出正确答案。长任务中，模型能力之外的任务编排系统、状态管理和错误累积都会使最终交付不可靠，阻碍无人值守或长期运行的应用。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **单步能力评测与结果导向监督**：用单次回答是否正确、最终任务是否通过，或一个终局奖励来衡量和训练模型；该做法将整段轨迹压缩为单一结果信号。
- **长上下文与记忆增强型智能体系统**：通过扩大模型一次可注意的文本范围，或在步骤和会话之间保存、检索历史信息，帮助智能体维持任务状态并继续执行。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单步基准不能暴露跨步骤失忆、过早宣告完成和目标漂移等失败模式；即使模型单步表现很强，也无法据此推断长任务是否可靠完成。
- 终局通过/失败或单一奖励会随任务长度增加而变得稀疏且信息不足，既难定位哪一步导致失败，也难为训练中的信用分配和评估中的过程诊断提供依据。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究常把任务所需步骤数、模型上下文容量和系统持久记忆混称为“长时程”，同时缺少一个贯穿规划、记忆、执行、训练与评估的统一视角来解释：长任务可靠性究竟由模型本体还是外围编排系统决定，以及怎样获得可诊断的过程级证据。

</div>
<div markdown="1"><span>核心问题</span>

面对不断延长的智能体任务，研究界已采用哪些规划、记忆、执行控制、训练和评估手段来缩小单步能力与长任务可靠完成之间的“视野鸿沟”，这些手段共同依赖什么类型的监督与测量信号？

</div>
<div markdown="1"><span>作者直觉</span>

将长任务看成一条可逐步检查的执行轨迹，而不是只看最后成败，可以在错误发生附近观察进展、偏离和恢复过程。再按“时程由模型上下文承载、由任务内编排承载，还是跨任务持久承载”分类，便能比较不同方案真正解决的是信息容量、状态延续还是执行可靠性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<p class="paper-minor-label">关键流程</p>

原文未明确报告完整流程。

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

原文未明确报告。

**训练与推理**

原文未明确报告。

**复现信息**

原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- SWE-bench及其扩展数据集：任务是给定完整代码仓库后解决真实GitHub问题；SWE-bench-java、Multi-SWE-bench、SWE-bench Multimodal和SWE-Bench Pro分别扩展编程语言、模态或任务规模，作用是测试覆盖范围与更长的软件工程任务。
- WebArena、OSWorld、AgentBench、GAIA及其扩展：分别覆盖网页操作、完整桌面操作、多个智能体环境和通用助理任务，作用是测试智能体在真实环境中执行工具调用与多步交互的能力；OS-Harm和AndroidControl-Curated进一步检验安全性及基准噪声。
- SWE-Bench-CL、ELL和EvoAgentBench：将任务组织为按时间或过程关联的序列，测试智能体是否能跨任务积累经验、迁移程序性策略并避免灾难性遗忘，而不是只在相互独立的任务实例上取得高分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务解决率或Pass@1**

衡量一次运行中任务是否被判定为成功，例如补丁是否通过测试或界面任务是否达到目标。 （通常越高越好，但只有在测试、任务定义和数据污染得到控制时，较高分才具有可信的能力含义。）

</div>
<div class="metric-item" markdown="1">

**重复试验可靠性**

在相同任务重复运行时，衡量智能体能否稳定重现成功，而不是偶然成功一次。 （越高越好；该指标把执行随机性、任务描述歧义和智能体行为波动纳入评价。）

</div>
<div class="metric-item" markdown="1">

**人类完成时间对应的时间跨度**

估计智能体在给定成功率下能够完成多长的人类工作时长任务，用于直接描述可承载的任务跨度。 （在任务定义和跨模型时代可比性成立时，越高表示可完成的任务跨度越长；原文强调其增长趋势只是“measured and reported”，并非已证实的普遍定律。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### SWE-bench及其有效性审计

<div class="result-value" markdown="1">

SWE-bench+的人工检查发现，成功补丁中32.67%涉及解法泄漏，另有31.08%仅因测试套件过弱而通过；同时过滤两类样本后，一个排行榜领先系统的解决率从12.47%降至3.97%。

</div>

最终测试通过率可能显著高估真实问题解决能力。该结果支持进行数据去污染和测试质量审计，但不能推出所有SWE-bench结果都无效，也不能直接比较未采用相同过滤规则的系统。

<div class="result-source" markdown="1">

来源：§7 Evaluation & Measurement，SWE-bench案例研究段落

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

SWE-bench+ manually inspects successful patches and finds 32.67% involve solution leakage (the fix was already present in the issue report or comments) and a further 31.08% pass only because the test suite is too weak to verify correctness — filtering both out drops one leaderboard-topping system’s resolution rate from 12.47% to 3.97%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 轨迹级软件工程诊断

<div class="result-value" markdown="1">

TRAJEVAL显示，某些能力较强的模型即使定位到了正确代码，仍会在后续执行阶段失败；这种“coherence collapse”表明Pass@1不能充分解释剩余约30%至35%的未解决问题。

</div>

模型找到故障位置并不等于能够保持连贯计划、修改代码、验证结果并完成任务。轨迹级诊断能区分定位失败与后续执行失败，但该结果本身不提供一种普遍适用于所有智能体的失败分类理论。

<div class="result-source" markdown="1">

来源：§7 Evaluation & Measurement，SWE-bench案例研究段落

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Most recently, a trajectory-level diagnostic (TRAJEVAL) shows that even where capable models localize the right code, they still fail after reaching it — “coherence collapse” — meaning Pass@1 alone actively misdiagnoses why the remaining 30–35% of issues go unsolved.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 人类时间跨度与跨任务评估

<div class="result-value" markdown="1">

论文核查约十五个知名智能体基准后发现，只有GAIA报告了清晰的分级人类完成时间统计；SWE-bench、WebArena和OSWorld的原论文均未报告人类时间基线。与此同时，SWE-Bench-CL、ELL和EvoAgentBench开始将任务组织为序列，以测量经验积累、知识迁移、程序性能力和灾难性遗忘。

</div>

领域已经提出直接测量任务跨度的思路，但多数基准缺少该指标，因此不同基准之间不能据此稳健比较“能工作多久”。跨任务基准则补足了独立任务评估的盲点，不过原文只说明这类研究正在出现，并未给出统一的性能提升结论。

<div class="result-source" markdown="1">

来源：§7 Evaluation & Measurement，Measuring horizon directly: time-horizon metrics

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Figure 5 makes a point about the field’s measurement maturity by its own sparseness: of the roughly fifteen well-known agentic benchmarks we checked against their own papers, only GAIA reports a clean, level-by-level human-time-to-complete statistic; METR’s own composite task suite states the band over which model success degrades rather than the suite’s literal range; and SWE-Bench Pro states only a qualitative “hours to days.”

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

- 固定任务上的最终结果评估，例如代码补丁是否通过测试或智能体是否到达目标界面；它是传统比较基线，但无法定位长轨迹中的失败原因。
- 单次运行成功率或Pass@1：用于比较不同系统在同一任务上的表面完成能力，但不能反映重复运行时的可靠性。
- 仅扩大基准覆盖范围的后续版本，例如SWE-bench-java、Multi-SWE-bench和WebArena等；它们可检验跨语言、跨模态和跨环境泛化，但不自动解决污染与有效性问题。
- 数据清洗、泄漏审计与轨迹级诊断方法：它们不是统一的模型基线，而是用于检验原始排行榜分数是否由真实问题解决、测试套件缺陷或记忆造成的评估对照。

**实验想回答的问题**

- 现有长时程智能体基准是否真正测量了持续完成复杂任务的能力，而不是记忆、数据泄漏、弱测试或执行随机性？
- 随着任务时长和所需步骤增加，单一最终成功率是否足以反映智能体的能力、失败位置与跨任务持续改进？

**实验实现**

论文是综述和评估方法论分析，而非提出统一模型并在统一训练集上进行受控实验。作者系统整理了1,547篇arXiv论文，并将文献按规划、记忆、执行、训练、评估、基础与安全六类组织；本节重点综合各基准原论文、数据清洗研究、排行榜审计、重复运行研究和轨迹诊断研究。所有基准数值按首次引用时记录，因为公开排行榜会随时间变化。作者特别比较最终结果指标与过程级证据：前者只判断是否成功，后者检查泄漏、测试充分性、失败轨迹、重复运行稳定性和跨任务迁移。对于人类时间跨度，作者核查约十五个知名智能体基准的原论文，但指出只有GAIA报告了清晰的分级人类完成时间统计；SWE-bench、WebArena和OSWorld的原论文没有报告人类时间基线。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| SWE-bench+过滤解法泄漏与弱测试样本 | 同时移除解法泄漏和测试套件不足以验证正确性的样本后，一个排行榜领先系统的解决率由12.47%降至3.97%。 | 这是对评估数据有效性的敏感性分析：它隔离了数据污染和判定规则对排行榜分数的影响。分数的大幅下降说明原始成功率不能直接当作真实能力，但由于只报告了一个系统，不能将降幅普遍外推到所有系统。 | §7 Evaluation & Measurement，SWE-bench案例研究段落<br><span class="experiment-evidence">filtering both out drops one leaderboard-topping system’s resolution rate from 12.47% to 3.97%.</span> |
| 单次成功率与重复运行可靠性对照 | 原文未明确报告统一数值对照；相关研究将不一致归因于执行随机性、任务规格歧义和智能体自身的运行间行为差异。 | 该对照检验的是评价协议是否稳定，而不是某个模型组件的消融。它说明单次Pass@1可能把偶然成功当成能力，因此重复试验应作为补充；但原文没有给出统一数据集上的具体提升或下降幅度。 | §7 Evaluation & Measurement，GUI和computer-use基准段落<br><span class="experiment-evidence">reliability, in other words, is not purely a property of the model, but of execution, task specification, and agent behavior jointly</span> |

**定性案例**

- SWE-bench的演化展示了评估从扩大覆盖范围转向检验有效性的过程：后续工作先扩展语言、模态和企业级任务，随后通过SWE-bench+、行为正确性研究、动态更新基准、记忆与泄漏研究以及TRAJEVAL，分别检查解法泄漏、弱测试、数据污染、排行榜可比性和轨迹连贯性。其核心解释是：一个补丁通过测试并不必然表示真正解决了问题，智能体还可能在定位正确代码后于后续执行阶段失去连贯性。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：This survey centers on the planning, memory, execution, training, and evaluation challenges of long-horizon LLM agents.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`29847547def327b579fbf007e4d5f43c98b668a06339e4ec4786d358f0db4ca9`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
