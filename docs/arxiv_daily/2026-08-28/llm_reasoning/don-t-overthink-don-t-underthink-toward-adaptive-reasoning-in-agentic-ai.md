---
title: "[论文解读] Don't Overthink, Don't Underthink: Toward Adaptive Reasoning in Agentic AI"
description: "[arXiv 2608.26442][LLM Reasoning] 本文将智能体人工智能中的过度推理与不足推理界定为推理资源错配的两类反复出现的失效模式，并通过实证分析说明未来系统需要根据任务执行过程中不断变化的需求，动态决定何时推理、何时行动以及何时停止。"
arxiv_id: "2608.26442"
announcement_date: "2026-08-28"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:37:38.681928+00:00"
source_sha256: "029c6726588c1bdb69241617a8b3bb562cd4edd441b936e81fa93cf88c2461e3"
tags:
  - "LLM Reasoning"
  - "LLM Agent"
  - "LLM 其他"
  - "智能体式人工智能"
  - "自适应推理"
  - "过度推理"
  - "推理不足"
  - "推理资源分配"
  - "推理时计算"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.26442</p>

# Don't Overthink, Don't Underthink: Toward Adaptive Reasoning in Agentic AI

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Md Jueal Mia, M. Hadi Amini</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Knight Foundation School of Computing and Information Sciences, Security, Optimization, and Learning for InterDependent Networks Laboratory (solid lab) Florida International University , Miami , Florida , USA；Knight Foundation School of Computing and Information Sciences, Security, Optimization, and Learning for InterDependent Networks Laboratory (solid lab) Florida International University；Affiliation: Knight Foundation School of Computing and Information Sciences；Security, Optimization, and Learning for InterDependent Networks Laboratory (solid lab)；Florida International University , Miami , Florida , USA</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26442v1) · [PDF 下载](https://arxiv.org/pdf/2608.26442v1) · **关键词** 智能体式人工智能, 自适应推理, 过度推理, 推理不足, 推理资源分配, 推理时计算<br>


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

本文将智能体人工智能中的过度推理与不足推理界定为推理资源错配的两类反复出现的失效模式，并通过实证分析说明未来系统需要根据任务执行过程中不断变化的需求，动态决定何时推理、何时行动以及何时停止。

**不用术语来说**：智能体不只是一次性回答问题，还会反复规划、调用工具、读取记忆并综合结果；如果它在简单步骤上想得太久，就会浪费时间和计算资源，甚至偏离原计划，而在真正困难的步骤上想得不够，又可能跳过必要工具或给出不完整答案。论文关注的不是让模型一味“多想”或“少想”，而是让推理投入与每一步实际需要相匹配。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 论文把过度推理和不足推理作为智能体推理资源错配的两类核心失效模式，并从冗余推理、薄弱推理、重复工具调用和跳过工具调用等可观察行为分析其成本与任务后果。
- 论文在基于 LangGraph 的固定智能体配置中，使用 MATH-500 与 GAIA 对代表性推理模型开展初步定量研究，并据此提出自适应推理应围绕“何时推理、何时行动、何时停止”建立机制与评价维度。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究智能体式人工智能中的推理资源分配问题。大语言模型可借助思维链进行逐步推理，而智能体系统还会把模型嵌入包含规划、工具调用、记忆检索、环境交互乃至多智能体协作的循环流程；因此，一次任务可能触发多个组件反复推理。推理越多并不必然越准确：过长的思考会增加生成令牌、延迟和计算成本，还可能引起重复调用工具或偏离任务目标；推理不足则可能导致证据收集不充分、漏掉必要步骤或过早结束。本文据此把核心问题界定为：智能体能否随任务需求的动态变化，在“继续推理、调用工具、采取行动、停止”之间合理分配推理资源，而不是统一采用固定推理长度。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大语言模型与大推理模型**

大语言模型通过预测后续令牌生成文本；大推理模型通常经过监督微调和人类反馈强化学习等训练，以产生更明确、较长的逐步推理轨迹。本文关注的不是模型是否能够推理，而是其在推理时投入了多少计算，以及这些投入是否与任务需要相称。

</div>
<div class="concept-item" markdown="1">

**思维链**

思维链是模型在给出最终答案前生成的中间推理步骤，可支持逻辑演绎、数学求解、规划与决策。更长的思维链通常消耗更多令牌和时间，但其长度与答案正确性并非线性关系。

</div>
<div class="concept-item" markdown="1">

**智能体式人工智能**

智能体式人工智能是能够围绕目标自主规划、调用外部工具、检索记忆、观察环境并进行多步决策的系统，既可由单个智能体构成，也可包含多个协作智能体。由于路由器、规划器和回答生成器等组件都可能调用模型，局部的冗余推理会在整条工作流中累积。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是完整智能体轨迹中的“推理错配”，而非孤立问答中的推理长度。系统输入为 MATH-500 数学题或 GAIA 通用智能体任务；LangGraph 工作流先由 Qwen3.5-4B 路由，再由 Qwen3.5-4B、Llama-3.1-8B-Instruct 或 Phi-4-reasoning 生成最终响应，并在需要时使用工具。实验采用确定性解码，最大生成长度为 $4096$ 个令牌，并记录工具使用、延迟、令牌消耗、触及令牌上限的情况以及完整交互轨迹。GPT-4.1 在不依据答案正确性的前提下，把每条轨迹独立标为推理不足、推理适当或过度推理；最终输出则另行标为正确、错误或不完整。概念上，推理不足指证据收集、验证或中间步骤少于完成任务所需；过度推理指在已足以解决任务后仍进行冗余思考、重复验证或不必要的工具操作；推理适当位于两者之间。该设置假定任务所需推理量会随规划、工具反馈和环境观察动态变化，因而不能仅由执行前的固定预算充分决定。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **ReAct（Yao et al., 2022）**: ReAct把语言推理与外部行动交替组织起来，是理解本文智能体循环中“何时思考、何时调用工具或行动”的直接技术背景；本文进一步关注这种循环内推理投入是否过多或不足。
- **Wang et al.（2025）**: 该工作指出，提高推理预算、增加规划步骤和采用复杂记忆机制往往只带来有限性能增益，却显著增加计算成本，为本文考察智能体工作流中的过度推理提供了直接依据；本文进一步以轨迹分类、成本和答案结果分析推理错配。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

显式思维链能够提高复杂任务的求解能力，但也会增加生成令牌、响应延迟和推理成本。在智能体工作流中，规划器、工具路由器和答案生成器等多个组件可能分别调用语言模型，因此单个环节中的少量冗余会沿多步流程累积；相反，某个关键环节推理不足又可能造成漏用工具、计划不完整或错误答案。这直接影响智能体的可扩展性、响应速度与真实部署可用性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **固定或预分配的推理控制**：在执行前为模型设置固定令牌预算，或先估计题目难度，再据此选择预定的推理强度。这类方法把推理资源主要视为可在任务开始前一次分配的预算。
- **模型内部推理调控与独立推理基准评测**：通过激活空间干预等方式改变模型内部的推理行为，并常在数学、逻辑等单次回答基准上评价效果；其重点通常是控制一次模型调用的推理量，而非追踪完整智能体循环中的规划、工具使用和环境反馈。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 固定预算或执行前难度估计假定任务所需推理量可以预先确定，但智能体在获得工具结果、检索记忆或与其他智能体交互后，局部难度和信息状态会持续变化；结果可能是在简单阶段过度计算，而在关键阶段预算不足。
- 面向单次模型回答或模型内部状态的控制，不能充分反映多组件智能体中的累积效应：不同组件可能重复分析、反复调用工具或跳过必要调用，从而产生额外延迟与令牌消耗，或者导致不完整解答。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚缺少一种面向完整智能体工作流的推理分配视角：既要识别推理投入相对当前任务需求何时过多或过少，也要把这种错配与延迟、令牌消耗、工具行为和答案完成度联系起来。本文首先提供初步经验性刻画，而不是宣称已经实现通用的自适应控制器；其结论也受固定 LangGraph 架构、固定工具路由模型、有限任务与模型范围的约束。

</div>
<div markdown="1"><span>核心问题</span>

在包含规划、工具调用和多步响应生成的智能体系统中，过度推理与不足推理如何表现，它们分别与计算成本和任务失败有何关联，以及这些现象对动态推理机制的设计提出了什么要求？

</div>
<div markdown="1"><span>作者直觉</span>

智能体执行任务类似于在途中不断获得新线索的决策过程：开始时无法准确知道每一步需要投入多少思考，但工具返回结果后可能立即变简单，也可能暴露新的困难。因此，更合理的入口是持续依据当前状态调整资源——信息充分时停止推理并作答，需要外部信息时及时行动，遇到关键不确定性时增加推理——而不是从任务开始到结束始终采用同一推理强度。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是提出并训练一种新的自适应推理算法，而是开展一项诊断性预实验：在统一的 LangGraph 智能体工作流中，用固定的路由模型处理工具决策，再分别调用三种最终回答模型完成任务；系统记录整条轨迹的时间、工具调用、令牌消耗和答案状态，随后由 GPT-4.1 在不参考答案正确性的前提下，将每条轨迹判为推理不足、推理适当或过度推理。最后，作者把这些推理类别与正确率、未完成回答、令牌上限触发和延迟联系起来，以检验智能体是否根据任务需求合理分配推理资源。

直观地说，该方法像给三位答题者安排同一名“工具调度员”，让他们完成数学题和需要外部信息的现实任务，并全程记录其思考时长、查工具次数和是否答完；再请独立裁判判断每位答题者是想得太少、恰到好处还是想得过多。需要特别注意的是，论文只用这一流程识别资源错配现象；第 6 节提出的自适应推理控制器只是未来研究设想，并未实现、训练或纳入实验。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 任务输入与统一智能体配置

将每个样本送入同一个基于 LangGraph 的智能体框架，并固定使用 Qwen3.5-4B 作为路由模型；最终回答模型分别配置为 Qwen3.5-4B、Llama-3.1-8B-Instruct 和 Phi-4-reasoning，以形成三个可比较的系统版本。

<div class="method-step__io" markdown="1">

**输入**：MATH-500 的全部 500 道测试题，以及 GAIA 公开验证集的 165 个任务。<br>
**输出**：共六个“数据集—最终模型”实验条件，以及每个条件下待执行的智能体任务。

</div>

**直观理解**：路由模型相当于统一的调度员，决定是否使用工具；三种最终模型则像不同的答题者。统一调度员有助于把最终回答阶段的差异主要归因于答题模型，但不能完全隔离框架和路由器本身的影响。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 路由决策与工具交互

Qwen3.5-4B 路由器在 LangGraph 工作流中作出工具使用决策；若调用工具，系统保存工具输入、工具输出、调用次数及相应耗时，并把观察结果加入后续上下文。

<div class="method-step__io" markdown="1">

**输入**：当前任务、智能体已有上下文，以及执行过程中获得的中间信息。<br>
**输出**：包含工具观察结果的轨迹上下文，以及工具调用次数、工具输入和输出令牌数、工具决策时间等记录。

</div>

**直观理解**：这一阶段模拟智能体边做题边决定是否“查资料”。它用于观察不同任务上工具分配是否合理，而不是证明工具调用本身必然提高正确率。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 最终回答生成与运行统计

三个最终模型分别以确定性解码生成答案，温度设为 $0.0$，最大生成长度为 $4096$ 个令牌；系统记录最终输出、生成时间、输出令牌数和是否触及令牌上限，对显式含有 `<think>` 与 `</think>` 的模型还统计标签内部的推理令牌。

<div class="method-step__io" markdown="1">

**输入**：原始任务与路由、工具阶段形成的完整上下文。<br>
**输出**：每个样本的最终答案、完整交互轨迹、时间与令牌成本，以及令牌上限触发状态。

</div>

**直观理解**：确定性解码减少了随机采样造成的波动，固定上限则提供统一预算。Llama-3.1-8B-Instruct 不公开显式思维轨迹，因此论文无法报告其推理令牌数，这不等于该模型没有进行内部推理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 独立轨迹分类与答案标注

GPT-4.1 独立把轨迹分类为过度推理、推理不足或推理适当；最终答案另行标注为正确、错误或未完成，并且推理类别不以答案是否正确为判定依据。

<div class="method-step__io" markdown="1">

**输入**：每个样本的完整智能体轨迹和最终回答。<br>
**输出**：每条轨迹的推理分配标签和答案质量标签。

</div>

**直观理解**：裁判先判断过程是否投入了合适的思考与验证，再单独判断结果是否正确，从设计上避免把“答错”直接等同于“想得太少”。不过，该分类依赖单一裁判模型及其提示词和量表，摘要所给章节未报告人工复核或裁判一致性。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文所述方法没有训练新模型、学习控制策略或定义可微优化目标；Qwen3.5-4B、Llama-3.1-8B-Instruct、Phi-4-reasoning 和 GPT-4.1 均作为现成模型使用。第 6 节提出未来可设计控制器，根据当前推理状态、任务需求和额外计算的预期收益，在继续推理、调用工具与输出答案之间动态选择，但原文没有给出该控制器的目标函数、训练数据、参数更新方法或实证结果。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. LangGraph 智能体执行框架**

该框架串联任务输入、Qwen3.5-4B 路由决策、工具调用、观察结果回填和最终答案生成，并保存完整交互轨迹。所有最终模型共享相同的工具代理模型，使工具侧统计在同一数据集内基本一致。

> 直观理解：它相当于实验流水线，确保三个最终模型经历相近的任务处理和工具调度过程。论文研究的是完整智能体工作流中的推理错配，而非只让模型离线回答一道孤立问题。

**2. 三类推理状态判别器**

GPT-4.1 根据完整轨迹，把推理不足定义为缺少必要中间步骤、证据收集或验证，或过早终止；把过度推理定义为超过任务所需的持续思考、重复验证或冗余推演；其余充分但不过量的过程归为推理适当。

> 直观理解：该模块把抽象的“想多了或想少了”转成可计数标签。它是论文分析的关键测量工具，但不是能够在线控制智能体推理量的控制器。

**3. 成本—质量联合测量模块**

系统同时测量总时间、工具决策时间、最终回答时间、工具调用与输入输出令牌、最终输出令牌、可见推理令牌、令牌上限命中及答案正确性；命中上限样本与未命中样本还分别计算准确率。

> 直观理解：只看正确率会掩盖“花费巨大但提升很小”的情况，因此论文把答案质量与时间、令牌和预算耗尽并列考察。该模块用于揭示效率权衡，并未把这些指标合成为一个经过优化的单一目标。

**训练与推理**

训练阶段：原文未进行额外训练或微调，也未报告提示优化、强化学习或控制器学习过程。推理阶段：对 MATH-500 的 500 个测试样本和 GAIA 的 165 个验证样本逐一运行 LangGraph 智能体；Qwen3.5-4B 统一承担路由与工具决策，三个候选最终模型分别生成答案。所有模型采用温度 $0.0$ 的确定性解码，最大输出长度为 $4096$ 个令牌；执行中保存工具使用、延迟、令牌量、预算命中和完整轨迹。运行结束后，GPT-4.1 对轨迹推理状态进行独立分类，答案另行判为正确、错误或未完成，再按数据集与模型汇总成本和质量指标。该流程是离线评估：推理类别在轨迹完成后产生，不会在当前执行中触发提前停止、追加推理或重新调用工具。

**复现信息**

实验运行于两张 NVIDIA RTX A6000 GPU，每张具有 48 GB 显存；LangGraph 框架通过兼容 vLLM 的 API 提供服务。路由器为 Hugging Face 模型 `Qwen/Qwen3.5-4B`，最终回答模型为该模型本身、`meta-llama/Llama-3.1-8B-Instruct` 与 `microsoft/Phi-4-reasoning`。推理令牌仅统计 `<think>` 与 `</think>` 标签之间的令牌；由于 Llama-3.1-8B-Instruct 不暴露这类轨迹，其该项结果记为 N/A。为支持复现，作者声明将发布框架源码、实验配置、提示词、GPT-4.1 裁判提示与分类量表、工具定义及逐样本输出，但所给章节只说明未来发布，未提供当前可访问的代码地址。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MATH-500：MATH 数学推理基准的 500 题评测子集，用于考察智能体在结构较明确、需要多步推导的数学问题上能否合理分配推理资源。原文未明确报告本实验是否使用其全部 500 题，也未在所给章节中说明难度分层或采样方式。
- GAIA public validation：面向通用 AI 助手的公开验证集，题目通常涉及信息检索、工具调用与多步任务执行；本文用它检验推理、行动和工具使用相互交织时的资源分配。原文未明确报告所用样本数、题目级别构成或是否排除特定题型。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**答案正确性**

衡量最终回答是否正确或完整，是判断推理投入是否真正转化为任务性能的核心效果指标；文中还据此分析过度推理是否带来成比例的准确率提升，以及推理不足是否对应错误或不完整答案。 （越高越好，因为它直接表示智能体成功完成任务的比例；但必须与成本指标联合解读，单独提高正确性不能说明推理资源分配高效。）

</div>
<div class="metric-item" markdown="1">

**Token 消耗与 token-limit exhaustion**

Token 消耗反映生成推理和答案所使用的文本计算量；token-limit exhaustion 表示生成达到固定最大长度限制，可能意味着推理冗长、未能及时停止，或复杂任务所需预算不足。两者共同刻画推理预算压力。 （在答案质量相当时越低越好；但不能脱离正确性机械地追求更少 token，因为过少的推理也可能造成错误或不完整解答。）

</div>
<div class="metric-item" markdown="1">

**工具决策延迟与工具使用行为**

工具决策延迟衡量智能体决定是否以及何时调用工具所需的时间；工具使用次数或行为用于识别重复调用、过量调用以及该调用时未调用等现象，从而考察推理与行动之间是否协调。 （在任务正确完成且工具需求相同的条件下，延迟和不必要调用越少越好；工具调用总数本身没有统一的单调优劣方向，因为复杂任务可能确实需要更多外部证据。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 被分类为过度推理的样本，跨 MATH-500 与 GAIA 的总体观察

<div class="result-value" markdown="1">

作者报告，过度推理样本与更高延迟、更多 token 消耗、更频繁的工具使用及更多触及 token 上限现象相关，但任务性能没有获得成比例提升。所给材料没有提供对应均值、准确率差、显著性检验或逐数据集数值。

</div>

这意味着“思考更多”并不自动等于“回答更好”：智能体可能重复规划、延迟行动或反复调用工具，最终只增加计算成本。该结果是相关性分析，不证明过度推理本身必然导致低准确率，也不能排除较难样本同时需要更多计算且更容易失败这一混杂因素。

<div class="result-source" markdown="1">

来源：Section 7, Conclusion

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Our findings suggest that cases classified as over-reasoning are associated with higher latency, greater token consumption, more frequent tool usage, and increased token-limit exhaustion without proportional improvements in task performance, whereas cases classified as under-reasoning are consistently associated with incorrect or incomplete solutions under our evaluation rubric.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 被分类为推理不足的样本，跨 MATH-500 与 GAIA 的总体观察

<div class="result-value" markdown="1">

作者报告，在其评测规则下，推理不足样本持续对应错误或不完整的最终解答。所给材料未报告错误率、与其他推理状态的差值或统计不确定性。

</div>

直观上，这类智能体过早作答，没有完成必要推导、证据收集、工具调用或验证。结果支持“仅压缩推理成本也会失败”，但由于论文没有进一步区分路由、检索、推理、答案合成和格式错误，不能认定所有错误都由思考时间不足直接造成。

<div class="result-source" markdown="1">

来源：Section 7, Conclusion

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Our findings suggest that cases classified as over-reasoning are associated with higher latency, greater token consumption, more frequent tool usage, and increased token-limit exhaustion without proportional improvements in task performance, whereas cases classified as under-reasoning are consistently associated with incorrect or incomplete solutions under our evaluation rubric.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### MATH-500 与 GAIA 的跨基准比较

<div class="result-value" markdown="1">

作者称两个基准呈现不同的主导失效模式，但共同表明固定智能体配置不能始终依据任务需求分配推理投入和工具使用。所给材料没有说明各基准具体由哪一种失效模式占主导，也没有提供类别比例。

</div>

数学题与通用助手任务对推导、检索和工具交互的要求不同，因此同一套控制策略可能在一个基准上偏向过度推理、在另一个基准上偏向推理不足。这一观察为动态控制提供动机，但尚未实验证明某种自适应控制器优于固定策略，因为本文没有实现并对照评测该控制器。

<div class="result-source" markdown="1">

来源：Section 7, Conclusion

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Although MATH-500 and GAIA exhibit different dominant failure modes, both benchmarks indicate that the evaluated agent configuration does not always allocate reasoning effort and tool usage according to task requirements.

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

- 原文未设置独立的无工具智能体基线，因此无法直接判断工具接入本身相对纯语言模型带来了多少准确率收益或额外开销。
- 原文未设置 standalone LLM 基线，因此不能把观察到的过度推理或推理不足明确归因于智能体编排，而非底层模型自身的推理行为。
- 原文未设置不同 token 预算的对照实验，因此固定最大生成长度下观察到的 token-limit exhaustion 不能揭示改变预算后准确率与成本如何变化。

**实验想回答的问题**

- 在基于 LangGraph 的智能体工作流中，推理投入是否会出现与任务需求不匹配的两类状态——过度推理与推理不足——以及它们分别如何影响答案正确性和推理成本？
- MATH-500 与 GAIA 这两类任务是否呈现不同的推理分配失效模式，从而说明仅依靠固定推理预算或固定工具策略不足以适应执行过程中不断变化的任务需求？

**实验实现**

实验采用基于 LangGraph 的固定智能体框架：Qwen3.5-4B 负责工具路由，另有三个最终响应模型生成答案，并在 MATH-500 与 GAIA public validation 上记录正确性、延迟、token 使用、工具行为和是否触及 token 上限。最大生成长度固定为 $4096$ token；推理状态按照作者给定的分类规则划分为过度推理或推理不足，并与答案正确性独立判定。所给材料未列出三个最终响应模型的名称、推理参数、运行硬件、各数据集实际样本数、重复运行次数、随机种子或置信区间，因此无法据此复现具体数值。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper studies adaptive inference-time reasoning allocation and its over- and under-reasoning failure modes within tool-using agentic workflows.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`029c6726588c1bdb69241617a8b3bb562cd4edd441b936e81fa93cf88c2461e3`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
