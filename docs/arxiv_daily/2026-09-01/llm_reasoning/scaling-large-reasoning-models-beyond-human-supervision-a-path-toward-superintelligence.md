---
title: "[论文解读] Scaling Large Reasoning Models beyond Human Supervision: A Path toward Superintelligence"
description: "[arXiv 2608.31075][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.31075"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:44:04.352129+00:00"
source_sha256: "784f144930a28618ded5898c64312b544608e1c841c1907d125dcd8a02050cd0"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "大推理模型"
  - "强化学习与可验证奖励"
  - "超越人类监督"
  - "奖励轴"
  - "经验轴"
  - "自主课程与环境生成"
  - "奖励欺骗"
  - "反馈保真度"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.31075</p>

# Scaling Large Reasoning Models beyond Human Supervision: A Path toward Superintelligence

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Zhiqin Yang, Jingwen Fu, Yuhan Liu, Hengyu Liu, Yonggang Zhang, Kainan Cao, Zizhuo Zhang, Chenxin Li, Ruibin Yuan, Jiahao Pan, Jiankai Sun, Zhenyuan Zhang, Yibo Li, Yunlong Lin, Jing Xiong, Sida Lin, Bo Han, Wei Xue, Yike Guo</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> The Hong Kong University of Science and Technology2 Zhongguancun Academy；Xi’an Jiaotong University4 The Chinese University of Hong Kong；The University of Hong Kong6 Hong Kong Baptist University；Hunyuan Tencent8 National University of Singapore9 Xiamen University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.31075v1) · [PDF 下载](https://arxiv.org/pdf/2608.31075v1) · **关键词** 大推理模型, 强化学习与可验证奖励, 超越人类监督, 奖励轴, 经验轴, 自主课程与环境生成, 奖励欺骗, 反馈保真度<br>
**代码**: [https://github.com/visitworld123/Awesome-Scaling-LRM-Beyond-Human-Supervision](https://github.com/visitworld123/Awesome-Scaling-LRM-Beyond-Human-Supervision) · **项目页**: [https://github.com/visitworld123/Awesome-Scaling-LRM-Beyond-Human-Supervision](https://github.com/visitworld123/Awesome-Scaling-LRM-Beyond-Human-Supervision)

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

本文位于大推理模型（large reasoning models, LRMs）与强化学习交叉领域，关注模型如何通过生成并学习交互经验来提升数学、代码及开放式智能体任务的能力。当前可扩展的基础是带可验证奖励的强化学习（RLVR）：数学答案可与标准答案比较，代码可编译并执行测试，因此大量模型轨迹无需逐条人工检查即可获得训练信号。但在创作、开放式问答和长期智能体交互中，任务通常没有唯一正确答案，反馈依赖语境、偏好或长期后果；因此论文研究当人工监督逐渐退出后，奖励如何获得、任务与环境如何产生，以及这些过程能否持续支持模型改进。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大推理模型（LRM）**

LRM 是通过大规模预训练、强化学习和更多推理时计算来解决复杂问题的语言模型。它们不仅直接给出答案，还会生成较长的推理轨迹或执行多步行动。

</div>
<div class="concept-item" markdown="1">

**强化学习与轨迹**

强化学习让模型根据反馈调整行为：模型接收任务或环境状态，生成一系列动作或回答，形成一条轨迹，再依据奖励更新策略。奖励越能准确反映任务目标，训练越可能推动真正有用的能力，而不是只优化表面分数。

</div>
<div class="concept-item" markdown="1">

**可验证奖励（RLVR）**

RLVR 使用能够自动检查的结果提供奖励，例如比较数学答案或执行生成的程序。它减少了逐条人工评价的需要，但只适用于正确性能够被可靠、自动判定的任务；开放式任务中的自动评分通常只是目标的代理信号。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文将“超越人类监督”定义为：在人类目标、初始数据、工具、环境、安全约束和独立审计仍可能存在的前提下，学习过程中需要人持续提供的操作性劳动逐渐减少。模型从任务或环境中生成轨迹，奖励机制对行为进行评价，学习算法据此更新策略；论文分别考察奖励轴与经验轴。奖励轴研究反馈证据如何从逐实例人工判断转向可复用验证器、奖励模型或无人工反馈的信号；经验轴研究任务和环境如何从人工设计逐渐转向模型生成，并最终形成策略、奖励、任务与环境共同演化的学习循环。该问题的核心不是单纯降低标注成本，而是在人工无法覆盖全部高难度、长时程经验时，仍获得真实、稳定且可持续的能力提升。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$L0\text{--}L4$**

从 L0 到 L4 的递减监督阶梯，用于标记学习过程中哪些组成部分仍需要持续的人类提供；它不是能力、可靠性、对齐程度或人类知识总量的指标。

</div>
<div class="notation-item" markdown="1">

**$\text{reward axis}$**

奖励轴，表示用于评价模型行为的证据及其来源，从逐实例人工判断逐步扩展到可验证或更自主获得的反馈。

</div>
<div class="notation-item" markdown="1">

**$\text{experience axis}$**

经验轴，表示产生训练轨迹的任务与环境如何从人工策划逐步转向模型生成、环境构造及自主共演化。

</div>
<div class="notation-item" markdown="1">

**$\text{policy capability}$**

策略能力，指模型在任务上的实际完成能力；它与反馈是否准确、训练经验是否高质量是不同的评价对象。

</div>

</div>

**直接相关的工作**

- **DeepSeek-R1（Guo et al., 2025a；Shao et al., 2024）**: 论文将其作为大推理模型发展的代表案例，说明结合大规模预训练、强化学习和推理时计算后，模型在数学与代码生成等可验证任务上取得了强能力；它构成本文讨论“从可验证反馈走向更开放任务”的现实背景，而不是本文提出的方法。
- **Silver & Sutton（2025）提出的“Experience Era”视角**: 该工作为论文强调经验在能力改进中的重要性提供概念背景。本文进一步把经验生成与奖励获取连接起来，提出奖励轴和经验轴，以及描述持续人类供给逐步减少的 L0–L4 监督阶梯。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大推理模型已经能够在数学和代码等结果可自动检查的任务上通过强化学习持续提升，但现实中的开放式问答、创意写作和复杂智能体交互通常没有唯一正确答案，质量还取决于语境、偏好和长期后果。随着推理轨迹变长、交互步骤增多以及任务难度接近或超过专家水平，人工逐条评价和设计训练任务的成本与速度都难以匹配模型产生经验的规模。论文因此关注一个实际而基础的问题：如何让模型在人工监督逐渐减少时仍能获得有意义的反馈、接触有价值的经验并持续改进。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **可验证奖励强化学习**：在数学任务中将模型答案与已知解比较，在代码任务中编译并执行程序，再依据结果直接产生奖励。由于正确性可以自动检查，大量模型生成轨迹无需人工逐条审阅即可用于强化学习。
- **学习型评价与自动经验生成**：对于缺乏确定答案的任务，使用奖励模型、评价准则或语言模型裁判近似人类判断；同时让模型生成推理轨迹、合成指令、调节任务难度，甚至构造可执行环境，以扩大训练经验并形成动态课程。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 可验证奖励主要适用于答案或执行结果能够明确核验的任务，难以覆盖开放式输出和长期智能体行为；学习型奖励虽然扩大了适用范围，却只是目标的代理信号，可能出现校准不足、相关性错误和奖励投机，模型优化的分数未必代表真实质量。
- 自动生成经验并不等于获得有效学习材料。模型生成的任务和环境可能缺乏多样性、难度不合适、不可解，或不能保持目标领域中的真实动态与后果；当策略、任务生成器和评价器共同适应时，还可能形成课程坍缩或相互强化的错误，使表面性能提升而独立标准下的能力停滞甚至下降。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究分别推进了奖励自动化或经验自动生成，但缺少一个统一框架来说明：在人类持续供给逐步退出后，学习过程中的哪些环节仍依赖人类，奖励如何获得可靠依据，经验如何保持有效，以及两者如何共同演化。更具体地说，尚未充分解决一个系统性缺口：如何同时评估模型自身能力、反馈信号对真实目标的忠实程度，以及自动生成经验的质量与可持续性，并据此判断模型是否真正实现了超越人工监督带宽的持续学习，而不是仅在代理指标上取得进步。

</div>
<div markdown="1"><span>核心问题</span>

当人类无法继续评价和设计模型产生的全部学习经验时，大型推理模型如何依靠逐渐自动化的奖励获取、任务与环境生成，以及二者的协同演化，仍然实现可靠、持续且可扩展的能力提升？

</div>
<div markdown="1"><span>作者直觉</span>

论文的切入点是把学习循环拆成相互连接的两个维度：奖励维度考察行为依据什么证据被评价，经验维度考察模型从哪些任务和环境中学习。只要反馈足够可信，新的经验能够暴露当前策略的弱点，策略进步又能推动生成更具挑战性的任务，学习循环就可能逐步摆脱人工逐例干预。为避免把自动化程度误认为真正进步，论文进一步将评价对象分为策略能力、反馈忠实度和经验质量：前者检验模型是否会做，后两者检验模型为何得到奖励以及训练材料是否值得学习。这个框架也使奖励欺骗、反馈漂移、课程坍缩和环境错误等失效路径能够被单独识别，而不是被一个总体性能分数掩盖。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是提出一个需要训练的新模型，而是对“大推理模型如何逐步脱离人类监督继续学习”进行结构化分析。其方法将学习过程拆成两个相互连接的维度：奖励轴描述反馈从逐样本人工判断，经过可复用验证器，走向无需即时人类反馈的自动奖励；经验轴描述数据和交互环境从人工策划，逐步走向模型自生成课程、环境以及主体之间的共同演化。作者据此构造 $L0$ 至 $L4$ 的五级阶梯，标记学习环节中仍由人类直接控制的部分，并用策略能力、反馈保真度和经验质量三个对象评估自动化学习是否真正有效。直观地说，本文分析的不是“怎样把一个模型训练得更强”的单一算法，而是“谁提供任务、谁提供反馈、谁检查反馈，以及这些环节能否可靠闭环”的系统路线图。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 界定学习闭环与监督来源

将学习闭环分解为奖励轴和经验轴：前者追踪奖励由人工判断向可复用验证器及无人工反馈信号的迁移，后者追踪经验由人工任务和环境向自生成课程、构造环境与自主共演化的迁移。

<div class="method-step__io" markdown="1">

**输入**：大推理模型的任务、推理轨迹、最终答案、奖励信号、训练经验以及人与环境提供的反馈。<br>
**输出**：一个用于定位不同研究工作的二维监督来源框架。

</div>

**直观理解**：先分别问两个问题：模型得到的分数是谁给的，以及模型练习的题目和环境是谁准备的。这样可以避免把“自动评分”和“自动出题”误认为同一件事。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按人类控制程度组织方法

依据学习过程中仍由人类持续控制的环节，将方法归入 $L0$ 至 $L4$ 五个层级，并同时考察奖励自动化与经验自动化的进展，而不是只依据是否使用强化学习进行分类。

<div class="method-step__io" markdown="1">

**输入**：不同研究中的奖励机制、任务来源、环境来源、验证器更新方式和训练闭环。<br>
**输出**：从高人类介入到趋向自主学习的分层梯子，以及各方法在梯子上的位置。

</div>

**直观理解**：这类似给“自动驾驶程度”分级：不能只看车辆会不会自己转向，还要看路线、规则、故障判断和训练场景是否仍由人类控制。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分类和分析奖励信号

按照证据来源，将奖励归为人类基础、模型派生、参考锚定和环境锚定等类型，并分析奖励如何作用于推理轨迹 $\bm{z}$、答案 $\bm{y}$ 或交互结果。重点区分“环境被用于提供信息”和“环境结果真正决定奖励”。

<div class="method-step__io" markdown="1">

**输入**：人工评估、模型派生信号、参考答案、可执行程序测试、游戏结果、形式化证明内核以及重建或循环一致性信号。<br>
**输出**：奖励来源、可扩展性、外部证据强度及潜在失真的系统比较。

</div>

**直观理解**：模型可以调用工具，但工具输出不一定就是评分标准；只有程序是否通过测试、定理是否被内核接受等外部结果真正决定分数时，才算环境提供了奖励证据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分析经验生成与学习闭环

考察经验是否由模型自行提出、筛选和迭代，并分析自生成课程、环境构造及策略—验证器共演化如何连接奖励轴。随后检查闭环中的错误是否会被重复利用或放大。

<div class="method-step__io" markdown="1">

**输入**：人工策划任务、模型生成任务、自动构造测试或环境、自博弈轨迹、工具交互记录以及策略和验证器的更新过程。<br>
**输出**：对自主经验扩展能力及其闭环稳定性的定性结论。

</div>

**直观理解**：如果模型既出题、又做题、还自己判分，它确实可以无限练习，但也可能把错误题目和错误标准一起循环放大。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文作为综述与分析论文，没有提出统一的可直接执行训练目标，因此不存在一个属于本文方法的单一损失函数。文中讨论的代表性训练形式通常以策略梯度更新模型参数 $\theta$，并根据奖励分别强化推理轨迹 $\bm{z}$ 和答案 $\bm{y}$；参考锚定方法还可最大化目标答案 $\bm{y}^{*}$ 在给定问题 $\bm{q}$ 与推理轨迹条件下的概率，环境锚定方法则将执行成功、游戏胜负或形式化内核接受等结果作为奖励。其核心分析结论是：优化目标的可计算性不等于目标语义的可靠性，奖励上升也不等于通用能力必然扩展。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 奖励轴与证据来源分类**

奖励机制按其外部证据来源组织为人工基础、模型派生、参考锚定和环境锚定信号。参考锚定方法利用已有目标答案 $\bm{y}^{*}$ 评估采样推理 $\bm{z}$ 对答案概率、困惑度、重建或参考指标的影响；环境锚定方法则依据执行测试、游戏规则、交互状态或形式化内核的结果评分。

> 直观理解：该模块回答“分数凭什么可信”。越依赖独立于策略本身的外部结果，越能减少模型自我确认，但测试不完整、规则有漏洞或形式化目标写错时，外部奖励仍可能被利用。

**2. 经验轴与自主学习梯子**

经验轴从人工策划任务和环境，延伸到模型生成课程、任务和测试，再到自博弈、环境构造以及策略与验证器的共同演化。$L0$ 至 $L4$ 用于标记这些学习环节仍处于人类控制、部分自动化或趋向自主的程度。

> 直观理解：该模块回答“模型练什么以及在哪里练”。模型能自己产生更多练习材料并不意味着材料有价值，因此经验生成必须和任务难度、可学习性、环境正确性一起检查。

**3. 失效模式与三对象评估**

分析围绕策略能力、反馈保真度和经验质量展开，并重点检查 reward hacking、feedback drift、curriculum collapse 和 environment errors。论文还区分奖励优化与能力扩展：强化学习可能提高采样效率，却缩窄策略支持集、形成模板化行为，或只改善与验证器直接相关的任务。

> 直观理解：自动学习的风险不只是“奖励噪声”，还包括模型学会骗验证器、验证器逐渐偏离真实目标、课程变得单一，以及环境本身包含错误。三类评估对象能帮助判断问题到底出在模型、评分标准还是练习材料。

**训练与推理**

本文本身不训练或部署一个新模型，而是对已有方法的端到端学习闭环进行归纳。一般闭环从问题 $\bm{q}$ 或环境状态开始，由策略 $\pi_{\theta}$ 生成推理轨迹 $\bm{z}$、答案 $\bm{y}$ 或动作序列；随后由人工评估器、模型评估器、参考目标或外部环境产生奖励，算法据此更新策略，并将成功或失败轨迹重新纳入后续经验。随着监督减少，任务、测试、环境和验证器也可能由模型生成或更新，形成自生成课程、自博弈或策略—评估器共演化。推理阶段则执行相同的生成过程，并通过目标匹配、模型评分、程序执行、游戏结果或形式化验证判断输出；若没有独立可靠的验证器，推理时的高置信度不能视为正确性证明。

**复现信息**

要复现或公平理解本文的分析，关键不是某个统一超参数，而是明确每项工作的监督边界和证据链：记录任务由谁提供、奖励由谁计算、验证器是否独立于策略、环境是否由模型构造、失败样本是否进入下一轮课程，以及策略和验证器是否同时更新。对代码任务，应区分工具执行仅为模型提供信息与测试结果真正决定奖励；对形式化证明，应同时固定定理陈述、形式化环境和资源预算，因为内核接受并不保证自然语言目标形式化正确。对自动生成经验，应检查任务可学习性、测试覆盖率、环境实现正确性和课程多样性；对最终结果，应同时报告策略能力、反馈保真度和经验质量，而不能只报告代理奖励或单次任务准确率。原文未明确报告一个统一的实现配置、训练数据规模、硬件设置或通用推理流程。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

原文未明确报告，或这里不需要额外前置概念。

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。

**实验想回答的问题**

- 原文是否通过受控实验检验了在减少人类监督后，大型推理模型能否持续提升能力？
- 不同奖励来源、评估器和经验生成机制是否经过统一数据集、基线与指标的定量比较？

**实验实现**

所提供原文节选属于综述性分析，主要按奖励来源和经验来源构建从 $L0$ 到 $L4$ 的概念阶梯，并讨论奖励欺骗、反馈漂移、课程坍缩和环境错误等风险；未提供独立实验的任务数据集、训练集或测试集划分、基线系统、评价指标、运行次数、统计显著性或复现实验协议。原文明确区分在线优化与离线优化：二者描述反馈如何被使用，而不决定评价标准最初来自哪里。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文系统分析大语言模型推理能力如何通过RLVR、自主经验生成和逐步减少人类监督进行扩展，兼具推理与对齐训练主题。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`784f144930a28618ded5898c64312b544608e1c841c1907d125dcd8a02050cd0`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
