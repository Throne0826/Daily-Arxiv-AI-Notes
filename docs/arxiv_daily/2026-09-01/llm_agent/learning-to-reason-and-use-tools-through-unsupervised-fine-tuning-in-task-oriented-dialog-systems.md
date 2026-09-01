---
title: "[论文解读] Learning to Reason and Use Tools through Unsupervised Fine-Tuning in Task-Oriented Dialog Systems"
description: "[arXiv 2608.30426][LLM Agent] 原文未明确报告。"
arxiv_id: "2608.30426"
announcement_date: "2026-09-01"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:40:12.073831+00:00"
source_sha256: "e99b9df5846bd8c8aafa7b1f167afc27046c643bcb2b41d36561181f9408ae62"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "LLM 其他"
  - "任务型对话"
  - "大语言模型"
  - "ReAct"
  - "工具调用"
  - "无监督微调"
  - "上下文学习"
  - "推理轨迹"
  - "SIMMC"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.30426</p>

# Learning to Reason and Use Tools through Unsupervised Fine-Tuning in Task-Oriented Dialog Systems

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Markel Ferro, Oier Lopez de Lacalle</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: HiTZ Center - Ixa, University of the Basque Country UPV/EHU</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30426v1) · [PDF 下载](https://arxiv.org/pdf/2608.30426v1) · **关键词** 任务型对话, 大语言模型, ReAct, 工具调用, 无监督微调, 上下文学习, 推理轨迹, SIMMC<br>


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

本文研究面向任务型对话（Task-oriented Dialogue，TOD）的智能体系统。TOD系统的目标是通过多轮自然语言交互完成预定义任务，例如检索商品信息或进行预订。传统TOD通常采用模块化架构，将自然语言理解（NLU）、对话状态跟踪（DST）和自然语言生成（NLG）等功能分开处理；这种设计较易定位模块功能，但模块间错误会逐步传播，且各模块需要独立训练。近年来，大语言模型（LLM）被用于构建端到端TOD系统，但其主要依赖训练阶段获得的静态参数知识，难以动态查询外部信息，因此可能产生事实错误。本文将ReAct式的推理与工具调用机制引入TOD，使模型能够在对话过程中交替生成思考、调用工具并读取观察结果，再据此生成最终回答。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**任务型对话（TOD）**

TOD是围绕明确任务展开的多轮对话系统，例如根据用户约束检索合适商品。系统不仅要生成自然语言，还要正确识别用户需求、维护对话状态，并返回与任务相关的实体或属性。

</div>
<div class="concept-item" markdown="1">

**ReAct与工具调用**

ReAct是一种让LLM交替执行思考（thought）、行动（action）和观察（observation）的智能体框架。行动通常是调用数据库、API或程序，观察则是工具返回的信息；这种机制使模型不必只依赖自身记忆，而能通过外部信息完成推理。

</div>
<div class="concept-item" markdown="1">

**无监督微调与上下文学习**

上下文学习（ICL）是指模型不更新参数，仅依据提示中的示例完成新输入。本文利用ICL生成包含推理和工具调用的轨迹，再筛选高质量轨迹作为训练数据，对模型进行无人工标注的微调；因此这里的“无监督”主要指不依赖人工编写的推理轨迹。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定指令提示、对话历史和当前用户查询，系统需要在任务型对话环境中生成正确、事实一致的最终回答。与只根据输入上下文直接作答的提示方法不同，本文假设系统可以访问为任务设计的外部工具，并允许模型先将问题分解为若干子问题，再执行工具调用、读取返回结果并继续推理。训练阶段没有人工提供的推理轨迹：模型首先通过ICL推理产生候选轨迹，随后由LLM评判器筛选高质量样本，形成微调数据；微调后的模型还会继续生成更优轨迹，用于后续迭代。实验设置聚焦于SIMMC中的商店场景对话，并分别考察服装和家具领域，以及通过加入合成对象构造的更高场景复杂度。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

系统输入，包括指令提示、对话历史和用户查询的组合。

</div>
<div class="notation-item" markdown="1">

**$T$**

ReAct推理轨迹，由依次产生的思考、行动和观察步骤组成。

</div>
<div class="notation-item" markdown="1">

**$a_t$**

第$t$步行动，例如调用外部API、数据库或其他程序工具。

</div>
<div class="notation-item" markdown="1">

**$o_t$**

第$t$步行动得到的观察结果，即外部工具返回并供模型继续推理的信息。

</div>

</div>

**直接相关的工作**

- **ReAct框架**: ReAct为本文的核心方法基础：它通过交替生成思考、行动和观察，使LLM能够进行分步推理并访问外部知识。本文关注的是如何将该框架适配到结构化且受约束的TOD环境，并通过无监督微调缓解少样例提示容易模仿示例、推理不一致的问题。
- **SIMMC数据集**: SIMMC是本文的主要实验平台，包含围绕商店环境中对象展开的多轮对话。本文利用其服装和家具领域检验推理与工具调用，并通过跨领域测试和增加合成对象分析模型对场景复杂度变化的适应能力。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

任务型对话系统需要根据商店库存、商品属性等不断变化的外部信息回答用户，但通用大语言模型主要依赖训练时获得的知识，无法可靠地动态查询当前环境，因此即使回答流畅，也可能捏造事实或给出错误信息。实际部署需要一种既能检索外部知识、又能正确规划查询步骤的对话代理，同时还应避免依赖昂贵的人工推理标注和超大模型。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **模块化任务型对话系统**：将自然语言理解、对话状态跟踪和自然语言生成等功能拆成独立模块，分别训练并按流水线连接，以识别用户意图、维护任务状态并生成回复。
- **端到端大语言模型与提示式 ReAct**：端到端方法直接让通用大语言模型根据对话上下文生成回答；ReAct 则进一步要求模型反复产生“思考—动作—观察”：先分解问题，再调用外部 API 或程序，读取工具返回的信息，最后形成有事实依据的回答。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 模块化系统结构复杂，各模块需要单独训练；上游识别或状态跟踪产生的错误还会传递到后续模块，降低最终任务完成的可靠性。
- 普通端到端模型缺少动态信息访问机制，容易产生事实幻觉；而仅靠上下文提示将 ReAct 用于任务型对话也并不直接，因为必须针对场景设计可用工具和提示，并使模型学会合理分解任务、选择工具。提示式方法在对象数量较多的复杂场景中还可能更快退化。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究表明推理与工具调用能够连接外部知识，但尚缺少一种面向任务型对话的完整适配方案：它应能在没有人工反馈或人工推理轨迹标注的条件下，自动获得并筛选高质量的推理—工具使用轨迹，再用这些轨迹稳定训练较小模型；同时还需验证这种训练能否抵抗场景复杂度上升，并避免只记住训练领域而无法迁移。

</div>
<div markdown="1"><span>核心问题</span>

能否将 ReAct 有效适配到任务型对话，并通过“上下文学习生成轨迹—大模型裁判筛选—迭代微调与自我改进”的无监督流程，使较小的大语言模型学会可靠推理和工具调用，从而在准确性、复杂场景鲁棒性及跨领域泛化方面达到或超过依赖提示的更大模型？

</div>
<div markdown="1"><span>作者直觉</span>

与其要求模型把所有动态事实都记在参数中，不如让它把复杂请求拆成若干可执行步骤，并在需要时查询环境；工具返回的观察结果相当于可核验的事实依据。初始模型虽然会生成一些错误或冗长轨迹，但大模型裁判可以保留较可靠的样本用于微调；改进后的检查点又能产生更好的下一轮轨迹，由此形成自举式提升。训练目标因而不是记忆某个领域的固定答案，而是学习可复用的“何时查询、查询什么、如何利用结果”的过程。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法将任务型对话建模为一个可调用外部工具的 ReAct 智能体。输入包括对话历史、当前用户查询以及场景中物体的多模态元数据；模型通过反复生成“思考—行动—观察”轨迹，使用针对场景信息检索设计的工具，最后生成回答。训练阶段不依赖人工标注的推理轨迹，而是先用上下文学习生成候选轨迹，再由 Prometheus 2 评价最终回答并筛选高质量样本，随后使用 LoRA 监督微调 Llama 8B，并通过多轮自训练持续扩充训练数据，得到 USI ReAct 8B。直观地说，模型先学会查找与问题有关的商品信息，再从自己的高质量解题过程里反复学习，而不是只凭参数记忆直接回答。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造场景化 ReAct 推理与工具调用

将原始 ReAct 提示适配到自动响应生成任务，使 LLM 迭代生成思考、行动和观察三元组。行动可调用 $Look[]$、$Search[query]$ 或 $Finish[answer]$；其中 $Look[]$ 获取场景内全部物体的视觉元数据，$Search[query]$ 按约束检索非视觉元数据，$Finish[answer]$ 终止推理并输出最终回答。

<div class="method-step__io" markdown="1">

**输入**：SIMMC 2.1 中的对话历史、当前用户查询以及当前场景的物体元数据；系统不使用真实标注答案或其他真实任务标注。<br>
**输出**：一个包含工具调用、工具观察结果和最终回答的完整推理轨迹；初始系统称为 ReAct ICL 70B。

</div>

**直观理解**：模型像一名购物助手：先查看场景中的商品，再按“价格便宜”或“评分较高”等条件搜索，最后把查到的信息组织成回答。这样可以只访问与问题有关的信息，减少凭空编造和无关检索。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自动生成候选训练轨迹

让系统在没有人工推理轨迹监督的情况下，为数据中的任务生成思考—行动—观察轨迹及其最终回答，并将能够导向正确回答的轨迹视为潜在有效的训练实例。

<div class="method-step__io" markdown="1">

**输入**：由上下文学习运行的 ReAct 系统、场景输入和对话查询。<br>
**输出**：候选轨迹数据集，包含模型生成的推理过程、工具观察和最终响应。

</div>

**直观理解**：先让一个较强的模型示范如何查资料和回答，把这些示范暂存为后续训练材料；关键困难是其中可能混有错误示范，因此不能直接全部用于微调。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于 LLM 评审的轨迹过滤

使用 Prometheus 2 作为自动评审器，评价最终回答的事实准确性；仅保留在 Likert 量表上获得满分 5 的轨迹，阈值来自初步实验并可视为任务相关超参数。

<div class="method-step__io" markdown="1">

**输入**：候选推理轨迹及其最终回答。<br>
**输出**：高质量、可用于微调的轨迹训练集。

</div>

**直观理解**：这一步像自动质检：评审器只留下事实完全可靠的回答对应的完整解题过程，避免模型把错误的查找步骤也学进去。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### LoRA 微调与自我改进迭代

使用 LoRA 对模型进行监督微调，并依据验证集上的 Prometheus 评价选择最佳检查点，得到第一轮模型 ReAct FT。随后用改进后的模型生成更好的轨迹，将新增高质量轨迹并入训练集合，再继续微调 Llama 8B；当 Prometheus 不再检测到性能提升时停止迭代。

<div class="method-step__io" markdown="1">

**输入**：筛选后的高质量轨迹、Llama 8B 基础模型以及验证集。<br>
**输出**：最终的 Unsupervised Self-Improving ReAct 8B 模型及其可调用工具的推理能力。

</div>

**直观理解**：模型先用第一批可靠示范学习，再用变强后的自己产生更好的示范，循环进行直到效果不再提高。LoRA 只训练较小的附加参数，目的是在资源有限时完成适配。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未给出显式的损失函数或数学优化目标。方法层面上，训练目标是对筛选后的正确思考—行动—观察轨迹进行监督微调，使模型学习从对话输入出发进行工具调用并生成最终回答；优化通过 LoRA 实现。每轮训练后，使用验证集上的 Prometheus 评价选择最佳检查点，并在检测不到进一步性能提升时终止自我改进。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 面向任务型对话的 ReAct 智能体**

LLM 接收指令提示、对话历史和当前用户查询，交替生成思考、行动和观察，直到产生 $Finish[answer]$。该实现将原始 ReAct 框架改造成适用于 SIMMC 场景元数据检索的对话系统。

> 直观理解：普通模型可能直接凭记忆回答；该模块要求它先说明要查什么、实际调用工具取得什么，再基于观察结果作答，因此回答有可追溯的信息依据。

**2. 场景信息检索工具集**

$Look[]$ 返回场景内所有物体的视觉元数据；$Search[query]$ 根据查询条件返回满足约束的物体非视觉元数据，例如按 $customerRating>3$ 筛选；$Finish[answer]$ 标记最终回答并停止后续行动。

> 直观理解：三个工具分别对应“看全景”“按条件查资料”和“提交答案”。它们把场景中的视觉和文本商品信息变成模型可以逐步使用的外部证据。

**3. Prometheus 2 驱动的无监督自训练**

Prometheus 2 对候选轨迹的最终回答进行事实准确性评价，仅保留得分为 5 的实例；筛选集用于 LoRA 监督微调，验证集上的 Prometheus 结果用于检查点选择和迭代停止判断。

> 直观理解：模型不需要人工逐条写出推理过程，但需要一个自动裁判来筛选可靠答案。随着模型变强，它又能产生更好的训练材料，从而形成自我改进闭环。

**训练与推理**

训练流程从 Llama 8B 基础模型和 ReAct ICL 生成的候选轨迹开始。系统首先在 SIMMC 2.1 的场景和对话输入上生成工具使用轨迹，然后由 Prometheus 2 评价最终回答并保留得分为 5 的样本；接着使用这些样本进行 LoRA 监督微调，利用验证集上的 Prometheus 分数选择最佳检查点，得到 ReAct FT。之后，改进后的模型继续生成候选轨迹，新的高质量轨迹被加入训练集合并触发下一轮微调，循环直到性能不再提升，最终得到 USI ReAct 8B。

推理时，模型只观察对话历史、当前查询和当前场景元数据，不读取真实任务标注。它根据当前问题决定是否调用 $Look[]$ 获取视觉信息、调用 $Search[query]$ 筛选非视觉信息，并根据工具观察结果继续推理；执行 $Finish[answer]$ 后，将其中的回答作为系统响应。

**复现信息**

复现或公平解读该方法所需的关键设定包括：任务限定为 SIMMC 2.1 的自动响应生成，不涉及该基准中的共指消解和对话状态跟踪；工具分别处理视觉元数据、约束条件下的非视觉元数据和最终回答；轨迹过滤阈值为 Prometheus 2 Likert 量表的满分 5；微调采用 LoRA，基础模型为 Llama 8B，并使用验证集进行检查点选择。原文选段未明确报告 LoRA 的秩、学习率、批大小、训练轮数、候选轨迹数量、每轮迭代次数或停止时的具体数值，因此这些细节不能据此补充。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- SIMMC 2.1：包含 11,244 个任务型对话和 117,236 条话语，覆盖 fashion 与 furniture 两个领域。模型根据对话历史和场景元数据生成回复，每次输入使用前两个对话轮次；原始视觉场景被转换为文本元数据，以便使用单模态语言模型。fashion 场景平均包含 30 个对象、每个对象有 11 个属性，furniture 场景平均包含 8.9 个对象、每个对象有 7 个属性，因此前者用于体现更高的场景复杂度。
- SIMMC 2.1 的 fashion 域验证集扩展版本：向场景元数据中加入合成对象，将每个场景的对象数量设置在 20 至 150 之间，用于测试对象数量增加时模型的上下文处理能力和复杂场景鲁棒性。
- SIMMC 2.1 的跨域训练—测试设置：分别只在 fashion 或 furniture 域训练，再在两个域上测试，用于检验微调模型是否记忆特定领域的对象属性，以及其跨域迁移能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**人工准确率**

盲评者判断生成回复是否正确的比例；每个领域随机抽取 100 个实例，并对所有系统使用相同实例。该指标直接关注回复是否事实正确，而不是与参考答案的字面重合程度。 （越高越好，因为更高比例表示回复正确的实例更多。）

</div>
<div class="metric-item" markdown="1">

**Prometheus 评分**

LLM 评审器对回复或推理轨迹质量给出的自动评分，主要用于无监督筛选和自我改进过程，也在部分必须自动评估的实验中作为信号。 （越高越好，但只能谨慎解释，因为论文指出该评审器会高估基线并产生假阳性，不能替代最终人工评估。）

</div>
<div class="metric-item" markdown="1">

**平均推理三元组数量**

每个系统生成的 thought–action–observation 推理单元平均数量，用于衡量推理轨迹是否冗长或包含低效步骤。 （越低越好，前提是回复正确性不下降；数量减少可表示噪声动作和重复工具调用减少，但单独不能证明推理质量更高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 完整 SIMMC 2.1 评测：比较 Blind、All-in-context、ReAct ICL、ReAct FT 和 USI ReAct。

<div class="result-value" markdown="1">

USI ReAct 8B 在 fashion 与 furniture 上分别达到 67% 和 82%，是表中 8B 系统的最佳结果，并超过 ReAct ICL 70B 的 60% 和 80%。

</div>

这说明自我改进能够使较小模型有效吸收推理与工具使用轨迹，在本文设置下达到或超过更大模型的上下文学习表现。但它不能证明 8B 模型在所有任务或所有数据分布上都优于 70B 模型，因为比较局限于 SIMMC 2.1 及其指定评估协议。

<div class="result-source" markdown="1">

来源：Table 1, Section 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

USI ReAct 8B | 67% | 82%

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 模型规模与训练方式比较：ReAct FT 8B 对比 ReAct ICL 70B，重点观察 fashion 域。

<div class="result-value" markdown="1">

ReAct FT 8B 在 fashion 域达到 65%，高于 ReAct ICL 70B 的 60%；在 furniture 域则为 75%，低于 ReAct ICL 70B 的 80%。

</div>

结果支持微调能显著改变小模型的任务能力，尤其在复杂的 fashion 场景中，训练后的 8B 模型可以超过仅通过上下文示例使用的 70B 模型。但该优势并非所有领域都成立，furniture 域的结果表明更大模型仍可能在较简单场景中占优。

<div class="result-source" markdown="1">

来源：Table 1, Section 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ReAct FT 8B | 65% | 75%

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 场景复杂度分析：逐步增加 fashion 场景中的对象数量，比较 ReAct ICL 70B 与 All-in-context。

<div class="result-value" markdown="1">

随着场景对象数量增加，All-in-context 基线性能显著下降，而 ReAct ICL 70B 表现出更强的鲁棒性。

</div>

该结果表明显式推理和工具化访问可能比把全部元数据一次性塞入上下文更能应对宽上下文和高信息密度场景。由于分析使用合成对象扩展验证集，且原文未给出图中的具体数值，结论主要支持相对趋势，不能据此确定具体性能下降幅度。

<div class="result-source" markdown="1">

来源：Section 7.3, Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Notably, as the number of objects increases, the performance of the All-in-context baseline degrades substantially. In contrast, ReAct ICL 70B exhibits greater robustness under complex conditions.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 最终人工评估每个领域只随机抽取 100 个实例，样本规模有限；同时，自动 Prometheus 评审器会高估基线并产生假阳性，因此自我改进和跨域实验中的自动分数需要结合人工结果谨慎解读。
- 场景复杂度实验通过插入合成对象构造 20 至 150 个对象的场景，未必完全代表真实对话中的复杂场景；此外，自我改进趋势的 Prometheus 分析只在 fashion 验证集上进行，跨到 furniture 的泛化仍未被同等严格地验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Blind baseline：使用 Llama 3.3 70B Instruct，但完全移除对象相关信息；它检验模型仅凭对话上下文能达到的性能下限。
- All-in-context baseline：使用 Llama 3.3 70B Instruct，并将完整对象元数据放入输入；它检验直接提供全部外部信息、但不进行显式工具化推理时的效果。
- ReAct ICL：使用五条人工整理的推理轨迹作为上下文学习示例，比较仅靠提示学习与后续微调的差异；8B 和 70B 版本分别采用对应规模的 Llama Instruct 模型。
- BART：跨域实验中的已有任务型对话架构基线，用于比较 ReAct 微调方法与更容易针对数据集训练的模型在跨域泛化上的差异。

**实验想回答的问题**

- ReAct 的显式推理与工具调用能否在动态场景信息检索任务中提升任务型对话的事实准确性，并超过不使用对象信息或直接将全部元数据放入上下文的基线？
- 无监督微调、自我改进和轨迹清洗是否能够提升较小模型的性能、复杂场景鲁棒性与跨域泛化能力？

**实验实现**

主干模型为 Llama 3.3 70B Instruct 和 Llama 3.1 8B Instruct，分别用于 70B 与 8B 系统。ReAct 系统通过生成推理轨迹、调用外部场景信息工具并产生最终回复来完成任务；无监督微调数据由上下文学习推理生成，再由 Prometheus 过滤高质量样本。自我改进循环使用改进后的检查点继续生成和筛选轨迹，随后进行下一轮微调。资源受限时采用秩为 32 的 LoRA。最终评估采用盲人工标注，而非 BLEU 或 BERTScore；意图分析使用 SIMMC 2.1 的意图标签进行事后分组，不将意图标签输入模型。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 无监督自我改进迭代：比较初始轨迹集与连续五轮筛选、微调和再生成的结果。 | 验证集 Prometheus 平均分从初始的 2.77 提升到第五轮的 3.67；第六轮降至 3.63，因此作者停止继续训练。fashion 中评分为 5 的训练话语从 5,492 增至 11,073，furniture 中从 2,342 增至 4,408。 | 该消融检验的是自我改进循环是否能逐步扩大高质量训练数据并提高生成轨迹质量。第一轮收益最大、后续收益递减，说明初次微调是关键；第六轮下降还提示继续迭代可能引入退化。不过这些趋势主要基于 fashion 验证集上的 Prometheus 评估，不能独立等同于人工准确率提升。 | Section 7.2, Table 3<br><span class="experiment-evidence">In terms of the Prometheus score, the model improves from an initial value of 2.77 to 3.67 after five iterations.</span> |
| 推理三元组清洗：比较使用过滤器清除 malformed actions、无效查询和连续重复 Look[] 调用，与不进行过滤的训练数据。 | 过滤后 ReAct FT 8B 的结果为 70%，未过滤为 62.5%，提升 7.5 个百分点；ReAct FT 70B 为 72% 对 74%，USI ReAct 8B 为 74.5% 对 73.5%。同时，过滤后平均三元组数量分别为 2.7906、2.8951 和 2.4974。 | 该消融说明清洗推理轨迹对 8B 基础微调模型尤其重要，能够减少低效或错误动作并提高评估表现；但对 70B 模型，过滤反而使结果下降，说明统一的启发式过滤器并非普遍有效。USI 模型差异很小，也暗示自我学习过程可能已经隐式抑制了部分噪声。 | Table 5, Section 7.4<br><span class="experiment-evidence">ReAct FT 8B \| 70% \| 62.5%</span> |

**定性案例**

- 意图分组显示，USI ReAct 8B 在 INFORM:DISAMBIGUATE、INFORM:GET、INFORM:REFINE 和 REQUEST:ADD_TO_CART 等类别上表现突出，例如 REQUEST:ADD_TO_CART 达到 95%，但 ASK:GET 降至 41%；这说明自我改进模型更擅长结合场景信息发现或操作相关对象，却可能没有同样稳定地回答直接的属性查询。该结论来自按意图汇总的人工正确率，不能解释单个对话中的具体错误原因。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该工作通过ReAct、外部工具调用和自监督轨迹微调提升任务型对话中的LLM推理与工具使用能力。; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`e99b9df5846bd8c8aafa7b1f167afc27046c643bcb2b41d36561181f9408ae62`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
