---
title: "[论文解读] CoVA-SFT: A Large-Scale Dataset for Chain of Visual Abstractions"
description: "[arXiv 2608.28958][VLM Reasoning] 本文以 CoVA-SFT 填补“从纯文本问题出发、通过多步且可自校正的视觉抽象进行推理”所需的大规模训练数据与统一评测基准空缺。"
arxiv_id: "2608.28958"
announcement_date: "2026-09-01"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:37:26.851807+00:00"
source_sha256: "5e060a5ab4852c155b829906959e8131d65c5299e35db80d6a09370da3251c11"
tags:
  - "VLM Reasoning"
  - "LLM 其他"
  - "LLM Reasoning"
  - "链式思维"
  - "多模态语言模型"
  - "链式视觉抽象"
  - "视觉工作区"
  - "交错视觉—语言推理"
  - "监督微调数据集"
  - "结构化推理"
  - "CoVA-SFT"
  - "CoVA-Bench"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.28958</p>

# CoVA-SFT: A Large-Scale Dataset for Chain of Visual Abstractions

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Tsung-Han Wu, Heekyung Lee, Anya Ji, Haoming Chen, Trevor Darrell, Joseph E. Gonzalez, David M. Chan</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28958v1) · [PDF 下载](https://arxiv.org/pdf/2608.28958v1) · **关键词** 链式思维, 多模态语言模型, 链式视觉抽象, 视觉工作区, 交错视觉—语言推理, 监督微调数据集, 结构化推理, CoVA-SFT, CoVA-Bench<br>


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

本文以 CoVA-SFT 填补“从纯文本问题出发、通过多步且可自校正的视觉抽象进行推理”所需的大规模训练数据与统一评测基准空缺。

**不用术语来说**：许多推理题的关键状态更适合画出来，而不是写成长篇文字，例如用棋盘记录棋局、用表格整理排程约束、用家谱表示亲属关系。现有模型通常被迫把这些二维结构逐项翻译成线性文字，不仅冗长，而且容易在多步更新中遗漏位置、连接或约束。论文希望让多模态模型在处理纯文本题目时，能够像人使用草稿纸一样主动创建、检查并持续更新视觉化的中间工作区。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者发布 CoVA-SFT：一种面向文本输入推理的结构化监督微调数据集，其轨迹显式包含选择视觉表示的理由、由智能体执行的渲染过程以及验证与自我修正环节，用于训练模型交替使用文字和视觉抽象。
- 作者同时发布覆盖相同任务范围的留出评测集 CoVA-Bench，并提供微调验证基线，用来检验模型是否真正学会利用内部视觉工作区，而不只是处理题目中原本已有的图像。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型推理与多模态推理交叉领域。链式思维（Chain-of-Thought，CoT）让模型先生成若干中间步骤，再给出最终答案，因此适合数学、编程和复杂逻辑任务；但当中间状态本质上是棋盘、关系图、几何图或排列表格时，仅用文字描述会把二维或结构化信息强行串行化。本文关注一种更适合这类问题的推理形式：模型在处理纯文本题目时，动态构造并维护视觉工作区，使文本推理与图像、表格或其他视觉抽象交替出现。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**链式思维（CoT）**

CoT 是让模型显式写出从题目到答案的中间推理步骤，而不是只输出最终结果。它有助于分解复杂任务，但传统 CoT 通常把所有中间状态都表示成文字。

</div>
<div class="concept-item" markdown="1">

**多模态语言模型**

多模态语言模型能够处理文字与图像等不同类型的信息，并在它们之间进行推理。本文利用这一能力，使模型不仅阅读文本，还能在推理过程中使用生成的视觉表示。

</div>
<div class="concept-item" markdown="1">

**视觉抽象与视觉工作区**

视觉抽象是把问题中的结构转化为表格、家谱图、关系图、棋盘或几何图等可视化表示。视觉工作区则是模型在解题过程中构造、更新和检查这些表示的中间空间，类似人类在纸上打草稿。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文研究纯文本输入下的结构化推理任务：输入是一道以文字描述的问题，例如排课约束、亲属关系、图关系、棋局、迷宫、数独或几何题；输出是任务要求的答案，如配置、关系、路径、棋步或数值。与依赖题目原始图像的视觉问答不同，输入本身不提供视觉状态，模型需要先根据文本理解问题，再在多步推理中选择合适的视觉抽象、生成或更新该抽象，并最终返回答案。论文的训练设置以监督微调数据为核心，目标是让多模态模型学会交替使用文字推理和视觉中间表示；评测则使用独立保留的测试样本，检验这种能力是否能跨越不同任务和布局类型。论文将数据组织为 $5$ 类布局族和 $17$ 个复杂任务，但所给章节未完整列出全部任务定义或统一的形式化输入输出符号。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Zebra-CoT**: Zebra-CoT 属于交错视觉—语言推理数据集，将推理建立在已有输入图像的视觉观察上；CoVA-SFT 的区别在于题目是纯文本输入，模型需要在推理过程中从头构造视觉工作区。
- **Math-VR**: Math-VR 将数学推理与文字、图像或数学图表结合，说明视觉表示可以辅助特定数学任务；CoVA-SFT 进一步扩展到游戏、图、布局、表格和数学等五类布局族及十七类任务，并强调多步生成与自我验证。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

空间、结构和关系推理往往要求模型在较长过程中保存并更新复杂状态，例如棋子位置、图节点关系、排程约束或几何构型。标准文本思维链只能按顺序生成词元，因此必须把天然具有二维结构的状态序列化为 prose；随着推理步数增加，这种表示会变得低效，也更难维持全局一致性。实际需求不是简单地让模型“看图”，而是让它面对纯文本问题时主动构造合适的图、表或布局，并把这些表示作为可持续更新的推理草稿。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **文本思维链**：模型先生成一系列自然语言中间步骤，再据此给出最终答案。这种方式适合证明、计算说明等中间状态本来就容易用语言表达的任务，但对棋盘、图结构和空间布局等状态，只能将其压缩成线性的文字描述。
- **视觉—语言交错推理与视觉草稿方法**：相关工作会在推理轨迹中加入草图、生成图像、代码绘制的图表或连续视觉表示；Mirage、CoVT 等潜在词元方法主要把输入图像的特征融入中间推理，Zebra-CoT 等数据则提供基于已有图像的视觉—语言交错轨迹。另一些方法允许模型根据文本绘制图形或执行绘图代码，将结果作为外部草稿。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 多数既有视觉推理资源以题目中已经存在的图像为依据，训练目标主要是观察、对齐或利用输入视觉信息；它们没有系统解决模型如何从纯文本描述中自行选择表示形式、从零构造视觉工作区并在连续步骤中维护其结构一致性。
- 已有资源在数据规模、任务领域覆盖或连续推理深度上受到限制，因此难以同时支持长程结构跟踪的监督训练和跨任务、可复现的统一验证；结果是研究者缺少能够判断视觉中间表示是否真正有助于纯文本推理的综合性数据基础。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺一种同时满足四项条件的资源：输入本身是纯文本；轨迹包含多步视觉状态而非单次插图；生成过程具有结构验证和自我修正；训练集与留出基准覆盖多类结构化任务。这个空缺使模型即使具备视觉架构，也缺少明确监督来学习何时建立何种视觉抽象、如何随推理更新它，以及如何发现并修复前一步造成的结构错误。

</div>
<div markdown="1"><span>核心问题</span>

能否通过一套大规模、跨任务、带验证闭环的交错视觉推理轨迹，教会多模态语言模型针对纯文本问题自主建立并维护视觉中间工作区，并用统一留出基准确认这种能力确实可学习、可评测？

</div>
<div markdown="1"><span>作者直觉</span>

人的草稿并不是对题目进行装饰，而是把难以记忆的关系外化：表格让冲突一眼可见，图让连接关系可追踪，棋盘或布局图让位置更新不必反复转述。作者据此把监督信号从“最终答案”扩展为“为什么需要某种图示—如何画出它—画完后怎样检查—发现问题后如何重画”的完整过程。这样，模型学习的不是固定图片模板，而是一种使用视觉表示管理中间状态的程序性习惯；自我检查环节则有望减少错误视觉状态在后续步骤中不断累积。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CoVA-SFT 是一个用于监督微调的多模态推理数据集，目标是让视觉语言模型在处理原本以文本呈现的复杂逻辑题时，主动建立、读取并维护中间视觉工作空间。其端到端流程以文本问题为输入，先由生成模型判断视觉抽象是否有用并设计结构化表示，再通过 Matplotlib 等工具将表示渲染成图像，随后进行一致性检查和必要的重绘，最后保存交错的文本推理、结构化工件、视觉图像与答案。数据集共包含 51,904 个样本和 222,046 个多模态推理步骤，覆盖 Table、Graph、Layout、Game、Math 五类抽象族及 17 项任务。直观地说，模型不是把所有视觉信息硬翻译成文字，而是在推理过程中画一张可反复查看和修改的草图，并把这张草图作为后续思考的外部工作台。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 问题分析与理由及问答构造

Claude 4.5 Sonnet 首先说明为什么该任务需要视觉工作空间，确定应当渲染的对象或关系，并生成相应的问答对和推理计划。

<div class="method-step__io" markdown="1">

**输入**：文本推理问题及其任务类型。<br>
**输出**：包含视觉抽象理由、待渲染内容、问题、答案以及后续推理所需结构的初始样本。

</div>

**直观理解**：这一步先回答“为什么要画图”和“应该画什么”，相当于解题者在动笔前决定使用路线图、表格、棋盘还是参数平面。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 交错推理与程序化渲染

生成模型逐步产生文本推理，并调用 Matplotlib 等工具编写程序，将表格、图、布局、游戏状态或数学区域渲染为视觉工作空间；生成的图像随后被反馈给模型，作为下一步推理的上下文。

<div class="method-step__io" markdown="1">

**输入**：初始文本推理、结构化中间工件和待生成的下一步推理。<br>
**输出**：由文本步骤、工具调用、结构化表示和对应图像组成的交错推理轨迹。

</div>

**直观理解**：模型每走一步就把当前状态画出来，再看着这张图继续推理；这类似人在纸上画草图、检查草图后再继续计算。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 视觉一致性验证与自我纠错

模型检查图像是否忠实表达题目中的结构、数量、连接关系和状态；若发现结构不一致或绘制错误，则重新进入渲染循环并重绘工作空间。

<div class="method-step__io" markdown="1">

**输入**：已渲染的视觉工作空间、原始问题和当前推理轨迹。<br>
**输出**：经过验证的视觉工件及修正后的完整推理轨迹。

</div>

**直观理解**：这一步像在交卷前核对草图：如果少画一个节点、连错一条边或标错区域，就先改图，而不是让错误继续污染后面的推理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 数据集整理与划分

将样本按五类视觉抽象族和 17 项任务组织为训练语料 CoVA-SFT，并从相同任务与抽象族中保留独立测试样本，构成 CoVA-Bench。

<div class="method-step__io" markdown="1">

**输入**：通过验证的多模态推理轨迹及其答案。<br>
**输出**：51,904 个训练样本、222,046 个多模态推理步骤，以及包含 1,700 个测试样本的评测基准。

</div>

**直观理解**：最终得到的不只是答案集合，而是大量“问题—中间文字—图像—检查—答案”的完整示范；测试集则用于检验模型是否能把这种工作方式迁移到未见样本。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文所给章节将 CoVA-SFT 定义为用于监督微调的多模态推理语料，但未明确给出训练损失、参数化目标或优化公式。根据现有材料，训练时应以数据中的文本推理、工具调用、视觉中间工件、验证步骤和最终答案作为监督信号；具体采用何种语言建模损失、图像编码目标或多模态联合目标，原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 结构化视觉抽象**

数据覆盖 Table、Graph、Layout、Game 和 Math 五个抽象族，使用表格、图结构、空间布局、游戏状态和数学图形等中间表示承载文本问题中的关系与状态。结构化工件使视觉内容可由程序生成，也便于在推理过程中更新。

> 直观理解：它把抽象关系转换成适合观察和操作的对象：例如把“哪些节点相连”变成图，把“参数满足哪些条件”变成平面区域。这样模型可以直接检查结构，而不必只依靠长篇文字记忆。

**2. 工具驱动的交错推理**

生成模型通过 Matplotlib 工具调用逐步创建视觉工作空间，并在每次渲染后接收图像作为新的上下文，从而形成文本推理与视觉状态交替出现的轨迹，而不是一次性生成静态插图。

> 直观理解：图像不是答案后的装饰，而是推理过程中的“可读写记忆”。模型可以根据当前计算结果更新图，再用更新后的图指导下一步。

**3. 验证反馈循环**

生成流程包含对渲染结果的结构一致性检查；检测到与题目不符的内容后，模型重新执行渲染并继续下游推理。该循环显式记录了自我检查和纠错行为。

> 直观理解：模型被要求先确认自己的图是否正确，再继续解题，类似把“画图”和“验图”分成两个环节，以降低错误状态被持续使用的风险。

**训练与推理**

训练阶段，模型使用 CoVA-SFT 中的完整交错轨迹进行监督学习，学习从文本问题出发生成视觉抽象、调用渲染工具、读取生成图像、执行一致性验证并输出答案。推理阶段，模型应接收新的文本问题，依次构造视觉工作空间、生成或更新图像、将图像反馈到上下文中并继续推理；若发现渲染结果不一致，则重新绘制后再继续。现有章节未明确报告推理时是否强制执行固定次数的验证、是否使用外部工具以外的搜索策略，或最终答案是否必须经过独立验证器确认。

**复现信息**

已知的关键实现信息是：数据由 Claude 4.5 Sonnet 作为代理式生成器分三阶段构造，视觉工作空间通过 Matplotlib 工具调用以程序化方式渲染，并在验证失败时进入重绘循环。数据组织为五类抽象族、17 项任务；CoVA-Bench 与 CoVA-SFT 使用相同的任务和抽象族，但包含训练阶段保留的 1,700 个测试样本，每项任务 100 个。原文摘录未明确报告模型架构、视觉编码器、提示模板、优化器、学习率、批大小、训练轮数、图像分辨率、工具沙箱配置或数据去重细节，因此这些因素不能据此复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- CoVA-Bench：包含 $1{,}700$ 个留出测试样本，覆盖与训练数据相同的 $17$ 个任务；其作用是评估模型对 CoVA-SFT 所覆盖任务的域内泛化能力。原文未明确报告各任务的具体划分比例或测试样本是否按任务均衡。
- CoVA-SFT：用于微调 Qwen3-VL-8B-Thinking 的训练语料，原文摘要报告包含 $51.9$K 个样本和超过 $222$K 个多模态推理步骤，覆盖 $5$ 类布局和 $17$ 个复杂任务；其作用是训练模型生成最终文本答案以及中间的潜在视觉轨迹。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**各任务及 Avg 的百分比得分**

表 2 报告 Table、Layout、Graph、Game、Math 五类任务以及 Avg 的数值，用于比较不同方法在各任务和总体上的表现。原文未明确给出该百分比得分的正式名称、计算公式或是否为准确率。 （越高越好，因为它表示任务评测得分更高；但在缺少正式指标定义时，不应将其进一步解释为某一种特定准确率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### CoVA-SFT 与交错式 CoT 基线的总体比较

<div class="result-value" markdown="1">

CoVA-SFT 的平均得分为 $38.2$，高于交错式基线 MathCanvas 的 $16.8$；表中其余交错方法的平均得分为 CodePlot-CoT $12.9$、TwGI $0.9$、Zebra-CoT $11.2$。

</div>

这说明在本文的域内留出测试集上，经过 CoVA-SFT 训练的模型比依赖外部程序渲染视觉工件的交错式方法表现更好。作者将差异归因于视觉工作区被内部化，因而避免外部执行边界以及渲染错误向后续推理传播。不过，该结果只能证明在本实验设置和这些基线上的相对优势，不能单独证明潜在视觉轨迹在所有任务或分布外数据上都更有效。

<div class="result-source" markdown="1">

来源：Table 2: Dataset Validation Baseline

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Latent TokensCoV A-SFT Baseline (Ours) 47.2 53.4 62.0 20.08.538.2

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### CoVA-SFT 与纯文本 CoT 基线的任务级比较

<div class="result-value" markdown="1">

CoVA-SFT 在 Graph 上得分为 $62.0$，高于最佳纯文本基线 Qwen3-VL-Thinking 的 $57.0$；但在 Table、Layout 和 Math 上分别为 $47.2$、$53.4$ 和 $8.5$，低于 Qwen3-VL-Thinking 的 $80.3$、$76.3$ 和 $27.3$。

</div>

结果表明，交错视觉表示的收益并非普遍存在，而主要出现在图关系推理这一类任务。作者的解释是，图中的节点、边和可达性关系用文字维护成本较高，而视觉工作区能持续承载这些结构；相反，数学推理已经有成熟的符号文本表示，额外引入潜在视觉 token 可能形成负担。因此，CoVA-SFT 不是对纯文本 CoT 的全面替代，而是对特定结构化视觉推理需求的补充。

<div class="result-source" markdown="1">

来源：Table 2: Dataset Validation Baseline；Section 3, Results and Analysis

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Latent TokensCoV A-SFT Baseline (Ours) 47.2 53.4 62.0 20.08.538.2
Text-Only
VLM Qwen3-VL-Thinking 80.3 76.3 46.5 25.5 27.3 51.2

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 不同任务类别上的方法行为

<div class="result-value" markdown="1">

CoVA-SFT 在 Math 上得分为 $8.5$，低于 MathCanvas 的 $12.3$，也低于 Qwen3-VL-Thinking 的 $27.3$；在 Graph 上则达到 $62.0$，高于 Qwen3-VL-Thinking 的 $46.5$ 和 MathCanvas 的 $20.2$。

</div>

该结果进一步定位了方法的适用边界：视觉工作区对图结构关系的保持可能有帮助，但对已经适合符号化表达的数学问题可能造成表示错配。MathCanvas 在 Math 上优于 CoVA-SFT，说明内部潜在视觉轨迹并不自动优于所有外部工具方案。由于实验没有提供逐步推理质量、错误类型或统计显著性分析，这些数字不能确定性能差异究竟来自表示形式、训练数据、提示方式还是实现细节。

<div class="result-source" markdown="1">

来源：Section 3, Results and Analysis

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

CoV A-SFT achieves the highest average score among in-terleaved CoT baselines by a substantial margin (38.2% vs. 16.8% for the next-best baseline, Math-Canvas), although MathCanvas performs better on Math.

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

- Qwen3-Think：纯语言模型的文本 CoT 基线，用于衡量不具备视觉输入能力、仅将问题序列化为文字时的表现。
- Qwen3-VL-Thinking：视觉语言模型在纯文本模式下的强基线，用于区分模型本身的推理能力与交错视觉表示带来的收益。
- MathCanvas：通过外部工具生成视觉工作区并将其反馈给推理链的交错式 CoT 方法，是表中交错基线的最佳平均表现者之一，可检验内部潜在视觉状态是否优于外部渲染流程。
- CoVA-SFT Baseline (Ours)：在 Qwen3-VL-8B-Thinking 上使用 CoVA-SFT 微调的模型，是本文方法；与上述基线比较可检验数据集和训练目标的整体效果。

**实验想回答的问题**

- 在相同约 $7$–$8$B 参数规模下，使用 CoVA-SFT 微调的模型能否学习并利用交错的视觉推理轨迹，从而在 CoVA-Bench 上优于现有交错式 CoT 方法？
- 内部化的视觉工作区相对于纯文本 CoT 的优势是否依赖任务类型，尤其是否更适合图结构等难以用文字持续维护的视觉关系推理？

**实验实现**

实验在零样本评测条件下进行：模型只接收文本形式的问题陈述。研究者将 Qwen3-VL-8B-Thinking 用 CoVA-SFT 微调，使模型除了生成最终文本答案，还生成支撑推理的交错潜在视觉轨迹；每张交错图像使用固定的 $128$ 个视觉 token。训练采用文本自回归交叉熵损失与视觉 token 余弦相似度损失的联合目标，视觉部分对齐预测的潜在视觉 token 与目标嵌入。原文未明确报告训练轮数、学习率、批大小、随机种子及各基线的具体推理提示。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces a dataset and benchmark for training multimodal models to perform multi-step reasoning through interleaved textual and visual abstractions.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`5e060a5ab4852c155b829906959e8131d65c5299e35db80d6a09370da3251c11`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
