---
title: "[论文解读] Soft Guidance Starts to Outperform CoT Prompting as LLMs Improve"
description: "[arXiv 2608.03550][LLM Reasoning] 本文重新检验现代大语言模型的推理评测范式，发现对于已具备原生逐步推理能力的模型，少样本思维链提示可能因额外约束而降低数学解题表现，简洁的零样本提示反而更能反映模型能力。"
arxiv_id: "2608.03550"
announcement_date: "2026-08-05"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:37:47.259784+00:00"
source_sha256: "a70a9cb264b46b1d9ab0bd739044aee0b1530d8f3bff6d1a37337144e6b93ae6"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "数学推理"
  - "思维链提示"
  - "少样本提示"
  - "零样本提示"
  - "上下文学习"
  - "指导—干扰权衡"
  - "推理评测"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.03550</p>

# Soft Guidance Starts to Outperform CoT Prompting as LLMs Improve

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Denys Pushkin, Albert Q. Jiang, Aryo Lotfi, Colin Sandon, Emmanuel Abbé</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> EPFL, Apple；Apple</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03550v1) · [PDF 下载](https://arxiv.org/pdf/2608.03550v1) · **关键词** 大语言模型, 数学推理, 思维链提示, 少样本提示, 零样本提示, 上下文学习, 指导—干扰权衡, 推理评测<br>


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

本文重新检验现代大语言模型的推理评测范式，发现对于已具备原生逐步推理能力的模型，少样本思维链提示可能因额外约束而降低数学解题表现，简洁的零样本提示反而更能反映模型能力。

**不用术语来说**：传统评测常先给模型看几道带详细解题过程的示例，再让它模仿这种方式回答新题；但现代推理模型本来就会自行展开推理，示例可能不再提供必要帮助，反而迫使模型兼顾示例的写法、答案格式和上下文关系。本文要判断：继续使用这种标准提示，究竟是在帮助模型思考，还是在干扰模型解决问题。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者挑战了将少样本思维链作为现代推理模型默认基线的惯例，并提出“引导—干扰权衡”：示例既能诱导分步推理，也会带来风格适配、格式遵循和上下文整合负担；当模型已能原生推理时，后者可能超过前者。
- 作者主张以约束更少的零样本生成作为推理专用模型更具竞争力、也更忠实的评测起点，以避免低估模型真实能力，并避免夸大相对于弱化基线的新方法增益。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型数学推理评测研究，关注提示方式是否能真实反映模型能力。传统少样本思维链提示会在输入中提供若干带逐步推导的人工示例，使模型模仿其推理和作答格式；零样本思维链则不提供示例，只加入“Let’s think step by step”等简短指令。由于现代推理专用模型已通过包含多步推理轨迹的数据训练，面对数学题时往往能自然生成分步解答，因此原本用于诱导推理的少样本思维链可能不再是中性的评测条件：它既提供解题指导，也要求模型适应示例的表达风格、输出格式和上下文，从而可能干扰模型原生的推理过程。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**思维链提示（Chain-of-Thought prompting, CoT）**

通过展示或要求生成中间推理步骤，引导模型先分解问题、再给出答案。本文主要区分含人工示范的少样本 CoT 与仅加入简短分步思考指令的零样本 CoT。

</div>
<div class="concept-item" markdown="1">

**上下文学习（In-Context Learning, ICL）**

模型不更新参数，而是根据当前提示中的示例临时推断任务规则和输出形式。示例不仅传递解题方法，也可能迫使模型模仿特定措辞、推导风格与答案格式。

</div>
<div class="concept-item" markdown="1">

**推理专用大语言模型**

指训练过程中特别强化数学或多步推理能力、能够原生输出 CoT 风格解答的模型。与通用模型相比，这类模型可能更少依赖外部示范来启动逐步推理。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究在数学文字题评测中比较不同提示条件：输入是待求解题目 $x$，可选地附加人工或模型生成的带推理示例，或者加入零样本 CoT 指令；模型输出自由形式解答及最终答案 $\hat{y}$，再与标准答案 $y$ 比较。核心设置包括无示例的自由生成、零样本 CoT，以及随机选取示例的少样本 CoT；随机选择用于尽量隔离“示例格式与指导方式”的影响，而不是研究复杂的示例检索策略。论文的问题不是 CoT 能否让早期模型产生推理步骤，而是对于已经能够自然分步推理的现代模型，少样本 CoT 是否仍是可靠且有竞争力的评测基线。其基本假设是提示存在“指导—干扰”权衡：示例可能提供有效解题线索，但风格适配、格式遵循和非必要上下文化也会占用模型的生成能力，甚至诱发过度续写或错误修正；图 1 所示案例正用于说明自由生成过程中模型可能已得到正确中间结果，却继续生成并重新确认错误答案。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入的数学问题。

</div>
<div class="notation-item" markdown="1">

**$y$**

数据集给出的标准最终答案。

</div>
<div class="notation-item" markdown="1">

**$\hat{y}$**

模型在特定提示条件下生成的最终答案。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{E}$**

少样本提示中提供的上下文示例集合；无示例设置下可视为空集。

</div>

</div>

**直接相关的工作**

- **Wei et al. (2022) 与 Kojima et al. (2022)**: 前者建立了使用人工分步示例的传统少样本 CoT，后者提出通过“Let’s think step by step”触发推理的零样本 CoT；二者构成本文重新比较自由零样本生成、零样本 CoT 和少样本 CoT 的直接基础。
- **Auto-CoT、Active-Prompt 与 AlignedCoT**: 这些方法使用模型生成并可经后处理的上下文示例，以降低人工示例与模型原生表达方式之间的风格错配。本文与其互补：它进一步检验即使示例由模型生成、格式更贴近模型自身，基于示例的 CoT 是否仍可能弱于无示例基线。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

模型能力和新推理方法通常依赖基准评测来比较，而提示方式本身会改变测得的性能。如果评测仍默认采用可能压制现代模型的少样本思维链，那么模型发布者和研究者可能得到失真的能力排序，并把相对于该受损基线的提升误判为方法本身的真实收益，因此需要重新确认这种基线是否仍然公平有效。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **少样本思维链提示**：在待解问题之前放入若干人工编写、通常取自同一数据集的示例，每个示例展示从题目到中间推理步骤再到最终答案的完整过程，使模型通过上下文学习模仿分步求解。这一方法最初用于改变倾向于直接回答的模型之输出行为，后来成为推理评测的标准基线。
- **零样本思维链提示**：不提供解题示例，只在问题后加入类似“Let’s think step by step”的简短指令，促使模型展开逐步推理。它比少样本方案减少了示例选择与模仿负担，但仍以人工设计的语言明确规定模型应采用的推理方式。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 少样本思维链不仅传递解题思路，还要求模型适应示例风格、遵守输出格式并把示例与当前问题整合起来。对于已经接受多步推理轨迹训练、能够自然生成思维链的模型，这些附加要求可能占用注意力并诱发不必要的情境化，从而使评测提示由帮助变成干扰。
- 把少样本思维链固定为默认基线隐含了“模型仍需示例才能展开推理”的旧假设，却没有充分检验该假设对现代推理专用模型是否成立；零样本思维链虽然约束较轻，其人工提示带来的边际帮助也可能随着模型增强而递减。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有惯例已证明思维链提示对早期、倾向直接输出答案的模型有效，但尚缺少针对现代中等规模模型的对照检验，以区分分步推理引导带来的收益与示例模仿、格式遵循及上下文整合造成的损失；尤其不清楚推理专用模型在无示例自由生成、零样本思维链和标准少样本思维链之间应以哪一种设置作为可信基线。

</div>
<div markdown="1"><span>核心问题</span>

当模型已经因专门训练而能够原生生成逐步推理时，标准少样本思维链提示是否仍能提高数学解题能力，还是简洁的零样本生成会表现更好；这种关系是否也适用于通用模型，并会如何影响推理评测基线的选择？

</div>
<div markdown="1"><span>作者直觉</span>

提示可以类比为给解题者提供脚手架：能力较弱时，示例能提醒其拆分步骤；能力较强时，过细的范例却可能迫使其一边解题，一边模仿他人的措辞和版式。作者因此从减少外部约束入手，让推理专用模型采用训练中已形成的自然求解策略；如果模型本来就知道如何展开推理，移除冗余示例应能降低认知式干扰，而一句简短的逐步思考提示最多只会再提供有限增益。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是提出新的模型结构或训练算法，而是设计一项受控的提示策略比较实验，用于检验传统思维链（Chain-of-Thought, CoT）提示的核心假设：向模型注入示范性的中间推理结构，是否仍能提升现代大语言模型的数学解题表现。研究以数学问题和现代中等规模语言模型为输入，在不更新模型参数的条件下，分别采用仅提供题目的零样本提示，以及若干包含推理示例的 CoT 提示变体，再比较模型生成答案的效果。为避免示例检索算法本身成为混杂因素，CoT 示例采用随机选择，而非根据测试题相似度进行检索。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造数学推理输入

对同一数学任务保留一致的问题主体，并准备零样本条件与多个 CoT 提示条件。研究同时考察通用模型和推理专门化模型，以判断提示效果是否依赖模型自身已经具备的推理倾向。

<div class="method-step__io" markdown="1">

**输入**：数学问题、候选大语言模型，以及可用于构造 CoT 提示的带逐步推理示例。<br>
**输出**：可在不同模型和提示条件之间进行受控比较的测试输入集合。

</div>

**直观理解**：这一步相当于给不同学生安排同一类试题，但分别测试“只看题目”和“先看带解题过程的例题”两种条件。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成零样本基线提示

仅向模型提供问题陈述，不加入人工设计的逐步推理示范，让模型按其原生输出风格生成解答。该条件用于观察模型是否已经能够自行产生 CoT 风格的多步推理。

<div class="method-step__io" markdown="1">

**输入**：单个数学问题。<br>
**输出**：零样本条件下的模型推理文本与最终答案。

</div>

**直观理解**：这里不给模型规定解题模板，目的是看它在没有外部示范时会自然采用什么推理方式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造并执行 CoT 提示变体

从示例池中随机选择示例并注入提示上下文，形成多个 CoT 提示变体，再由模型生成目标问题的推理过程和答案。随机选择用于排除相似度检索、示例排序优化等策略带来的额外收益，使比较更集中于“注入中间推理结构”本身。

<div class="method-step__io" markdown="1">

**输入**：数学问题、带中间推理过程的示例池，以及待比较的 CoT 提示策略。<br>
**输出**：各 CoT 提示条件下的模型推理文本与最终答案。

</div>

**直观理解**：研究者给模型展示若干完整例题，但不刻意挑选最像当前题目的例子，从而避免把“选例技巧好”误认为“CoT 本身有效”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 跨提示与跨模型比较

比较同一模型在不同提示策略下的数学解题表现，并进一步比较通用模型与推理专门化模型的变化方向。分析重点是 CoT 提供的推理指导收益，是否会被风格适配、格式遵循和无关上下文化造成的干扰抵消。

<div class="method-step__io" markdown="1">

**输入**：各模型在零样本条件和 CoT 提示变体下生成的答案。<br>
**输出**：关于不同模型类型是否仍应使用传统 CoT 提示的受控实验结论。

</div>

**直观理解**：最终不是只问哪种提示分数最高，还要判断：模型越会自主推理时，照着外部示范写答案是否反而会分散注意力。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。所给章节描述的是提示层面的受控推理评测，没有提出新的损失函数，也没有对模型参数进行优化；研究变量是推理时采用的提示形式，而不是训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 零样本原生推理条件**

该条件只输入问题陈述，不显式要求模型模仿少样本 CoT 示例，用于测量现代指令微调模型自行生成逐步推理的能力。它也是判断 CoT 示例究竟提供必要指导还是额外干扰的核心对照组。

> 直观理解：如果模型本来就会逐步解题，那么不提供例题不等于不进行推理；它反而可能让模型使用自己最熟悉的解题方式。

**2. 随机示例 CoT 条件**

CoT 条件向上下文注入带中间推理步骤的示例，但示例通过随机方式选择。该设计削弱了检索质量这一混杂变量，使结果更接近对传统 CoT 提示机制本身的检验。

> 直观理解：若专门挑选与测试题高度相似的例题，性能提升可能来自“碰巧看过类似题”；随机选例能让比较更公平，但仍可能受到具体随机样本的影响。

**3. 指导—干扰权衡分析**

作者将 CoT 的作用拆分为两面：它可以提供中间推理结构，但也要求模型适应示例的语言风格、输出格式和上下文框架。对已经能自然生成完整推理的专门化模型，后一类约束可能与模型偏好的推理模式冲突。

> 直观理解：例题既可能像脚手架一样帮助不会解题的模型，也可能像多余模板一样束缚已经会解题的模型；实验要判断哪一面占主导。

**训练与推理**

本文方法发生在推理阶段。对每个数学问题，研究者分别构造仅含题目的零样本输入，以及由随机示例组成的多个 CoT 提示输入；随后将这些输入交给固定的现代中等规模语言模型生成解答，并在相同任务上比较不同提示条件。通用模型与推理专门化模型被分别考察，因为前者可能仍需要显式推理指导，后者则可能已从训练数据中习得稳定的逐步推理行为。所给章节未说明任何额外微调、梯度更新或参数适配过程。

**复现信息**

公平解释结果所需的关键实现设计是：CoT 示例采用随机选择，以尽量排除检索策略造成的混杂；零样本条件仅提供问题陈述，从而保留模型的原生推理风格；比较覆盖多个 CoT 变体、零样本基线以及不同类型的现代中等规模模型。所给章节未明确列出各提示模板的完整文本、每个变体的示例数量、随机种子、解码参数、重复运行次数或答案判定程序，因此仅凭该摘录无法完整复现实验。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：小学水平数学文字题基准，包含约 7.5K 个训练样本和 1.3K 个测试样本。训练集仅用于随机抽取上下文示例，或让待测模型生成 Self-CoT 示例；最终准确率在测试集上计算。由于实验只使用一个数学数据集，结论直接对应算术文字题场景，不能自动推广到其他推理任务。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（Accuracy, Acc）**

测试题中最终数值答案正确的比例，用于衡量端到端数学解题表现；该指标同时受推理正确性和答案能否被正确抽取影响。 （越高越好，因为正确回答的测试题比例更大。）

</div>
<div class="metric-item" markdown="1">

**无效答案率（Invalid Answer Rate, Inv Ans）**

因缺少最终答案、未按要求给出单一数值等格式问题而无法有效抽取答案的比例。它帮助判断准确率变化来自真实推理能力，还是仅来自格式服从。 （越低越好，因为更少回答因输出格式而被判为无效。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 推理专用或推理较强模型：DS-CoT 与零样本自由生成对比

<div class="result-value" markdown="1">

Mathstral 的 DS-CoT 系列最高仅为 74.1%，低于零样本自由生成的 83.8%，差 9.7 个百分点；Qwen 的 DS-CoT 系列最高为 83.4%，也低于零样本自由生成的 88.6%，差 5.2 个百分点。

</div>

作者据此主张，固定的人类推理示例会妨碍这两类较强模型发挥原生推理能力，传统少样本 CoT 因而可能成为被削弱的评测基线。更朴素地说，强模型本来已经知道怎样展开解题，额外要求它模仿数据集的措辞和格式反而可能分散注意力。不过，该比较只能说明所测模型、GSM8K 和随机示例协议下的端到端准确率下降，不能单独证明模型内部推理确实受到干扰，也不能排除示例质量、上下文构成等其他机制。

<div class="result-source" markdown="1">

来源：第 5.1 节；表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Specifically, we obtain at most 74.1% accuracy with DS-CoT-style prompting for Mathstral, compared to 83.8% for the zero-shot baseline. Similarly, for Qwen, DS-CoT variants achieve no more than 83.4%, while zero-shot prompting yields 88.6%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 模型生成示例与对应零样本基线对比

<div class="result-value" markdown="1">

Self-CoT 系列并未普遍超过零样本基线：Mathstral 的最佳 Self-CoT+0shot 为 85.5%，仍低于其零样本 CoT 的 86.1%；Qwen 的最佳 Self-CoT+0shot 为 91.6%，仅比零样本 CoT 的 90.9%高 0.7 个百分点。

</div>

结果说明，让模型自己编写示例可以减少人类示例带来的风格错配，但完整少样本脚手架对已经擅长结构化推理的模型未必有额外价值。作者将 Mathstral 的现象解释为其更擅长自然生成连贯推理轨迹；这是机制性推测，而非实验直接测量。Qwen 的小幅提升也不意味着 Self-CoT 普遍有效，因为这里只覆盖单一数据集和随机示例设置。

<div class="result-source" markdown="1">

来源：第 5.2 节；具体数值见表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

When comparing Self-CoT (free-form) and Self-CoT+0shot to their respective baselines—zero-shot free-form and zero-shot CoT—we find that these strategies yield only marginal improvements for the Qwen model, and fail to outperform the baseline for Mathstral.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 所有提示变体中比较 Self-CoT+0shot 的整体表现

<div class="result-value" markdown="1">

Self-CoT+0shot 是三种模型上整体最强的少样本格式：Qwen 最高达到 91.6%，超过其零样本 CoT 的 90.9%；Llama 在 16-shot 时达到 84.4%，超过其零样本 CoT 的 81.4%；Mathstral 最高为 85.5%，略低于零样本 CoT 的 86.1%。

</div>

这一结果支持“软引导”观点：先用很短的逐步思考提示让模型生成符合自身习惯的示例，再把这些示例用于上下文学习，比直接复制数据集中的人类解答更兼容模型的原生输出方式。它并不表示示例越多越好：最佳 shot 数随模型而异，且 Mathstral 仍以无示例的零样本 CoT 更强。因此，更准确的结论是 Self-CoT+0shot 是所测少样本方案中伤害最小、总体最有效的格式，而不是无条件优于零样本。

<div class="result-source" markdown="1">

来源：第 5.3 节；具体数值见表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Among all the prompting variants we evaluated, Self-CoT+0shot (see column 6 in Table 1) consistently yields the strongest performance across models. It even outperforms the zero-shot CoT baseline for Qwen and Llama, and underperforms it only slightly for Mathstral.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 外部有效性有限：实验只有 GSM8K 一个小学数学文字题数据集和三个约 7B–8B 的模型，没有覆盖更复杂数学、符号推理、代码、常识推理或更大规模模型。因此，“模型越强，标准 CoT 越像干扰”仍是由有限横截面对发展趋势作出的解释，尚非受控的模型规模或训练阶段研究。
- 机制证据有限：实验测量的是最终准确率与格式无效率，并未直接观测内部推理过程。作者提出的“guidance-distraction”权衡、风格适配负担和原生推理受干扰是对结果的合理解释，但随机示例质量、上下文长度、示例难度及模型生成示例池构成也可能影响结果；同时，简单清洗无效不能排除更精细筛选或检索策略带来收益。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 零样本自由生成（zero-shot free form）：只提供题目，让模型以自身习惯的格式作答。它是判断少样本示例究竟提供帮助还是构成干扰的核心基线。
- 零样本 CoT：在回答前加入“Let’s think step by step”这一轻量引导，但不提供完整示例。它用于区分“只提醒模型逐步思考”的收益与“要求模型模仿少样本推理轨迹”的额外影响。
- DS-CoT／DS-CoT+Instr：从 GSM8K 训练集随机抽取人类编写的推理示例，后者再加入答案格式指令；两者均分别搭配规则抽取和提示式抽取。该组代表常见的标准少样本 CoT 评测协议。
- Self-CoT／Self-CoT+0shot：由同一个待测模型分别在自由生成或零样本 CoT 引导下为训练题生成解答，仅保留最终答案正确的示例，再将其用于上下文学习。它们用于检验与模型原生表达风格更一致的示例能否减轻 DS-CoT 的风格适配负担。

**实验想回答的问题**

- 对于已能自然生成逐步推理过程的现代中型语言模型，随机选取的人类编写少样本思维链示例是否仍优于不给示例的零样本提示，还是会因风格模仿、格式服从和额外上下文而妨碍推理？
- 若少样本示例改由模型自身生成，示例的生成方式、答案抽取方式以及示例清洗会如何影响性能；这些因素究竟改善了数学推理，还是只改善了输出格式？

**实验实现**

实验评估 Mathstral-7B、Qwen2.5-7B-Instruct 和 Llama-3.1-8B-Instruct，分别覆盖专门面向多步数学推理、具备较强推理表现的通用指令模型，以及未专门优化推理的通用指令模型。少样本规模为 1、2、4、8、16；所有示例均随机选择，以避免高级示例检索策略成为混杂因素。DS-CoT 同时测试规则抽取与提示式抽取：前者寻找最后一个“#### <number>”模式，后者要求模型只返回单一数值。Self-CoT 系列统一采用提示式抽取。构建模型生成示例时，作者先为全部约 7.5K 道训练题生成解答，只保留最终答案正确者；清洗变体还会截断解答后的续写，并过滤可能推理不完整的示例。全部生成采用贪心解码，各项结果在 10 个不同随机种子的示例采样运行上取平均。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 答案抽取消融：DS-CoT+Rule 与 DS-CoT+Prompt 使用完全相同的推理解答，仅改变最终答案抽取方式 | 小样本时，规则抽取造成大量格式失败。例如 Qwen 1-shot 的 DS-CoT+Rule 准确率仅 3.0%、无效答案率 96.5%，改用提示式抽取后准确率为 86.9%、无效答案率仅 0.1%；Llama 1-shot 也从 10.6%准确率和 87.3%无效率变为 78.0%准确率和 0.1%无效率。 | 该消融隔离了“答案如何被读出”这一因素，因为两种设置的上下文解答相同。巨大差距表明，DS-CoT+Rule 在示例较少时的低分主要是模型没有模仿“#### 数值”格式，而不一定是不会解题；更多示例带来的表面提升也可能只是格式学习。提示式抽取则用明确指令要求单一数值，使准确率更接近推理解答本身的质量。 | 表 2，Qwen2.5-7B-Instruct 的 1-shot 完整数据行；列依次为 DS-CoT+Rule、DS-CoT+Prompt、DS-CoT+Instr+Rule、DS-CoT+Instr+Prompt 的 Acc 与 Inv Ans<br><span class="experiment-evidence">1-shot \| 3.0 \| 96.5 \| 86.9 \| 0.1 \| 83.3 \| 0.7 \| 83.4 \| 0.2</span> |
| 模型生成示例的清洗消融：比较未经处理与经过“截断续写＋过滤不完整推理”两阶段处理的 Self-CoT 和 Self-CoT+0shot | 清洗没有稳定改善 Self-CoT+0shot：例如 16-shot 时，Mathstral 变化为 +0.0、Qwen 为 +0.0、Llama 为 -0.4 个百分点。较一致的收益只出现在 Llama 的自由生成 Self-CoT 上，其 1、2、4、8、16-shot 分别提高 1.5、1.4、0.7、1.2、2.2 个百分点。 | 该消融检验模型生成示例中的对话续写或不完整论证是否是主要性能瓶颈。对 Self-CoT+0shot 几乎无收益，说明轻量 CoT 前缀已能让这些模型生成足够规整的示例，简单清洗的边际价值有限；Llama 自由生成 Self-CoT 的持续改善则与其未专门训练推理轨迹的设定一致。但清洗方法本身较简单，因此不能推出更强的质量筛选方法也无效。 | 表 3，16-shot 完整数据行；每个模型依次报告 Self-CoT 未清洗准确率及清洗变化、Self-CoT+0shot 未清洗准确率及清洗变化<br><span class="experiment-evidence">16-shot \| 83.6 \| +0.1 \| 85.2 \| +0.0 \| 89.6 \| +0.2 \| 91.6 \| +0.0 \| 72.8 \| +2.2 \| 84.4 \| -0.4</span> |

**定性案例**

- 作者人工检查模型生成示例后发现两类污染：Llama 和 Qwen 有时在给出正确解答后继续生成对话；另一些回答虽然最终数值正确，却没有给出逻辑完整的论证。这一观察解释了清洗流程为何同时包含“在完整解答后截断”和“过滤疑似不完整推理”，但原文没有提供具体样例或错误类别频率，因而只能作为流程设计依据，不能量化其普遍程度。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：研究比较软引导、零样本与少样本 CoT 提示对现代 LLM 数学推理表现的影响。; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`a70a9cb264b46b1d9ab0bd739044aee0b1530d8f3bff6d1a37337144e6b93ae6`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
