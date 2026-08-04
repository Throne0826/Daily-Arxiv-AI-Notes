---
title: "[论文解读] PICTURE: Enhancing Theory-of-Mind in Large Language Models by Revealing, Not Hiding, Characters' Lack of Knowledge"
description: "[arXiv 2608.01598][LLM Reasoning] 本文针对大语言模型在错误信念任务中容易依据客观事实、而非角色所知信息作答的问题，提出让模型在自由形式思维链中显式生成角色“不知道什么”，以减少严格事件隐藏格式造成的推理性能损失。"
arxiv_id: "2608.01598"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:00:44.733294+00:00"
source_sha256: "679ac87976b6f7a093a17cb74c72057b38ad36033a5a63838632cddeb6028578"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "心智理论"
  - "大语言模型"
  - "错误信念"
  - "视角采择"
  - "事件隐藏"
  - "反应抑制"
  - "缺失知识"
  - "思维链提示"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.01598</p>

# PICTURE: Enhancing Theory-of-Mind in Large Language Models by Revealing, Not Hiding, Characters' Lack of Knowledge

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Eojin Jeon, SangKeun Lee</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Department of Artificial Intelligence, Korea University, Seoul, Republic of Korea；Department of Computer Science and Engineering, Korea University, Seoul, Republic of Korea</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01598v1) · [PDF 下载](https://arxiv.org/pdf/2608.01598v1) · **关键词** 心智理论, 大语言模型, 错误信念, 视角采择, 事件隐藏, 反应抑制, 缺失知识, 思维链提示<br>
**代码**: [https://github.com/jej127/PICTURE](https://github.com/jej127/PICTURE)

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

本文针对大语言模型在错误信念任务中容易依据客观事实、而非角色所知信息作答的问题，提出让模型在自由形式思维链中显式生成角色“不知道什么”，以减少严格事件隐藏格式造成的推理性能损失。

**不用术语来说**：故事中的角色可能没有看到某件事，因此其信念会与真实情况不同；但大语言模型读到了完整故事，常直接用自己看到的事实回答，而不能按角色有限的信息判断。已有方法先删掉角色不知道的事件，却要求模型严格输出特定结构，一旦删错或格式约束干扰推理，最终答案也会受到影响。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出并通过初步实验检验一个行为层面的假设：在推理过程中明确写出角色对哪些事件缺乏知识，可以提示大语言模型抑制这些事件对答案的影响。这里的“抑制”仅指模型在提示中仍能看到角色未知事件时依然正确作答，不涉及对模型内部神经机制的主张。
- 作者据此提出 PICTURE：不删除完整故事中的事件，而是要求模型在自由形式思维链中推断角色知道和不知道的内容，再继续逐步推理，从而将视角采择与较少受格式限制的推理结合起来。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型在文本心智理论任务中的推理能力。心智理论要求模型根据故事中角色实际观察到的信息，推断该角色的信念，而不能直接用全知视角下的客观事实作答；其中，错误信念任务尤其关键，因为角色的认知状态与现实状态存在冲突。已有方法通常先执行“视角采择”：删除目标角色未感知的事件，再让模型依据过滤后的故事回答问题。该流程绕开了模型对未知事件进行反应抑制的需要，但事件删除往往要求模型严格输出故事子集、JSON 或图结构，格式约束可能干扰原本的推理。本文关注一种不同设定：保留完整故事和所有事件，以自由形式表达角色视角，并显式指出角色“不知道什么”，从而帮助模型在仍能看到未知事件的情况下依据角色信念作答。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**心智理论（Theory of Mind, ToM）**

指把信念、知识等心理状态归因于他人，并据此预测其判断或行为的能力。在本文的文本任务中，模型需要区分故事的客观现实与特定角色所拥有的信息。

</div>
<div class="concept-item" markdown="1">

**错误信念任务（false-belief task）**

目标角色因未观察到某个事件而持有与现实不一致的信念，模型必须按角色的错误认知回答，而不是按最新事实回答。与之对应的真实信念任务中，角色信念和现实状态一致，通常不产生这种视角冲突。

</div>
<div class="concept-item" markdown="1">

**反应抑制（inhibition）**

本文将其定义为行为层面的能力：即使提示中包含目标角色不知道的事件，模型仍能正确回答心智理论问题。该定义不声称模型内部存在与人类相同的神经或认知抑制机制。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一段包含多个角色及一系列事件的自然语言故事、一个目标角色，以及关于该角色信念或知识状态的问题；故事可能包含目标角色没有感知、因而不知道的事件。输出是从该角色自身视角得到的答案，必要时还包括通向答案的自由形式思维链解释。核心假设是：故事文本对模型保持完整可见，不通过事件隐藏预先删除角色未知的信息；因此模型必须先判断目标角色知道和不知道哪些事件，再抑制未知事件对最终答案的影响。本文讨论的“抑制”仅由最终行为是否正确界定，而不涉及模型内部机制。初步研究还借助 Percept-ToMi 提供的事件感知者信息，把角色未感知的事件显式改写为“该角色不知道该事件”，用于检验显式缺失知识能否改善错误信念推理。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **SimToM**: SimToM 采用两阶段提示，先从故事中筛除目标角色未观察到的事件，再基于过滤后的故事回答问题，是本文所概括的事件隐藏式视角采择代表。它降低了回答阶段的抑制要求，但需要生成正确的故事子集；本文则保留完整故事，使模型在未知事件仍然可见时进行推理。
- **PercepToM**: PercepToM 同样通过两阶段提示实现事件过滤，并提出本文初步研究所使用的 Percept-ToMi 数据集；该数据集提供每个事件的感知者信息，使作者能够确定目标角色未感知哪些事件。本文利用这些标注显式加入角色的“缺失知识”，检验这种提示是否能帮助模型抑制客观事实的干扰。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

心智理论任务要求模型根据他人的信念、知识等心理状态进行判断。在错误信念场景中，角色没有观察到某些事件，其主观认知因而不同于客观现实；大语言模型却能读到完整故事，容易受角色未知事件影响并依据真实状态作答。这种无法稳定区分“模型知道的事实”和“角色知道的事实”的现象，是模拟类人心智理论能力的关键障碍。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **零样本思维链提示**：向模型提供完整故事，并通过“Think step by step”等触发语让其自由生成逐步解释后回答问题。该方法输出限制较少，但没有专门机制隔离角色未知的事件。
- **基于事件隐藏的视角采择**：先让模型从故事中移除角色不知道的事件，再仅依据过滤后的故事回答；为确保未知事件与角色视角被清楚分开，既有工作通常要求输出 JSON、图结构或原故事的事件子集。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 一般的自由形式思维链会持续暴露完整故事，模型容易让角色未见的事件进入后续推理，最终以客观现实代替角色视角作答。
- 事件隐藏虽然绕开了上述抑制要求，却依赖严格的结构或事件子集格式；格式遵循与推理表现之间可能存在权衡，而且错误删除本应保留的事件会破坏角色视角，使后续回答建立在不完整或错误的故事上。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究主要通过物理删除角色未知事件来实现视角采择，尚未充分研究一个更少受格式约束的替代路径：保留完整故事并采用自由形式解释时，怎样让模型主动识别角色缺失的知识，同时避免这些仍可见的事件支配最终答案。

</div>
<div markdown="1"><span>核心问题</span>

当角色未知事件始终保留在输入和推理上下文中时，显式表述角色对这些事件的“不知情”，能否作为有效提示，使大语言模型按角色信念而非客观现实完成心智理论推理？

</div>
<div markdown="1"><span>作者直觉</span>

仅让模型“站在角色角度思考”仍较抽象；若明确生成“角色不知道某事件”，就相当于给该事件加上一个不可用于代表角色信念的标记。模型无需先把事件从故事中精确删除，也能在后续推理时把它视为与该角色答案无关的信息，从而兼顾完整上下文与自由形式推理。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PICTURE 是一种仅在推理阶段使用的提示方法，目标是在不执行“事件隐藏”的情况下完成心智理论推理。输入是包含多个角色及事件的完整故事和一个关于目标角色心理状态的问题；模型先以自由形式的思维链梳理目标角色知道与不知道哪些事件，再保留完整故事作为后续推理上下文，最后根据显式形成的知识状态回答问题。其关键机制是把“角色缺乏某项知识”直接写进推理过程，从而触发抑制控制：虽然模型仍能看到角色未观察到的事件，但回答时应避免把这些事件错误地归入该角色的信念。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 确定目标角色与待判断心理状态

模型读取未经删减的故事，并根据问题确定需要采用谁的视角，以及最终需要判断的信念、知识、态度、意图或其他心理状态。该步骤保留角色可知和不可知的全部事件，尚不回答最终问题。

<div class="method-step__io" markdown="1">

**输入**：完整故事、问题及其指定或隐含的目标角色。<br>
**输出**：目标角色、问题所要求的心理状态，以及供后续推理使用的完整事件上下文。

</div>

**直观理解**：先弄清楚“要站在谁的立场回答什么问题”。故事仍完整摆在模型面前，以免删减过程本身造成信息遗漏或错误。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自由形式视角采择

PICTURE 使用类似“目标角色知道和不知道哪些事件？”的指令，并结合“Think step by step”式思维链提示，让模型用不受固定格式约束的自然语言重建角色视角。输出不必是故事事件的严格子集，也不要求复制、删除或重新排列原文句子。

<div class="method-step__io" markdown="1">

**输入**：目标角色和完整事件上下文。<br>
**输出**：描述目标角色知识状态的自由形式思维链。

</div>

**直观理解**：模型不是像编辑文本那样删掉角色没看见的句子，而是像解释剧情一样说清楚：这个角色经历了什么，又错过了什么。自由表达降低了生成严格事件子集时的格式负担。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 显式生成知识缺失

模型在思维链中不仅陈述目标角色已知的事件，还明确生成其不知道、未观察到或未获知的事件。论文把这种显式知识缺失视为抑制控制的触发因素，使模型在仍可读取完整故事的条件下，区分事实世界与角色信念世界。

<div class="method-step__io" markdown="1">

**输入**：自由形式视角采择过程及故事中的观察、进入、离开、物体移动等事件线索。<br>
**输出**：同时包含“已知事件”和“未知事件”的角色知识状态表示。

</div>

**直观理解**：仅说“角色知道什么”容易让模型被完整故事中的真实事实带偏；补上一句“角色不知道后来发生了什么”，相当于给回答过程设置明确的认知边界。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于角色知识状态完成回答

模型依据已形成的角色视角继续进行任务所需的组合推理，并生成最终答案；对于错误信念问题，它需要抑制使用角色未知的真实事件。PICTURE 不在视角采择之后增加事件隐藏或格式转换步骤。

<div class="method-step__io" markdown="1">

**输入**：完整故事、问题，以及显式包含知识缺失的自由形式思维链。<br>
**输出**：从目标角色视角得到的最终心智理论问题答案。

</div>

**直观理解**：最后回答时，模型可以知道故事真相，但必须按角色实际掌握的信息作答。它像一名读者区分“我知道的结局”和“故事人物此刻以为的情况”，而不是先把书页剪掉再判断。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。原文将 PICTURE 描述为提示方法，所给章节未提出新的参数训练目标、损失函数或针对该方法的微调过程；方法效果来自推理时提示所诱发的知识状态表达与抑制行为，而不是通过反向传播优化一个新增模块。因此不能把实验使用的准确率或 F1 分数解释为训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 知识状态显式化提示**

PICTURE 新增的核心指令要求模型同时推理目标角色知道与不知道的事件，例如原文给出的“What events does and does not {character} know about?”。提示的作用对象是角色知识状态，而不是直接要求模型输出一个错误信念答案；附录 B.7 的不同措辞实验进一步表明，关键条件是明确鼓励这种知识状态推理。

> 直观理解：这个模块把通常隐含的“角色没看到什么”变成必须说出来的中间结论。它让模型有机会在最终回答前主动标记哪些真实信息不能算作角色的知识。

**2. 无事件隐藏的自由形式思维链**

该模块以自然语言解释承载视角采择结果，不要求输出仅由角色已知事件组成的严格故事子集。与 SimToM 一类方法不同，PICTURE 始终保留完整上下文；与“PICTURE w/ Event Hiding”变体不同，它也不在自由推理后把解释转换成经过过滤的事件集合。

> 直观理解：传统方案让模型同时完成推理和精确删句，删错一条事件就会污染后续答案。PICTURE 允许模型按自然语言习惯解释人物视角，以减少严格格式转换带来的额外错误。

**3. 基于知识缺失的抑制控制**

这里的抑制控制不是独立训练的分类器或额外神经网络模块，而是由提示诱发的推理行为：当思维链明确指出某事件不为目标角色所知时，模型应在推断该角色的信念时抑制该事件。该机制对位置变化等错误信念问题最直接，但面对多跳推理或多个角色的高阶信念时，仍需额外的组合推理。

> 直观理解：模型看到了全部事实，却不能把所有事实都塞进角色脑中。显式写出“角色不知道这件事”就像给该事实贴上“读者可用、角色不可用”的标签。

**训练与推理**

PICTURE 不需要专门训练。推理时，向现有大语言模型提供完整故事、心智理论问题、自由形式思维链指令，以及要求说明目标角色知道和不知道哪些事件的知识状态指令；模型先生成角色视角解释，再在不删除任何故事事件的前提下生成最终答案。核心流程可概括为“完整上下文输入 → 显式推理已知与未知 → 依据角色视角回答”。附录中的“PICTURE w/ Event Hiding”不是正式方法，而是用于检验机制的变体：它在自由形式视角推理后额外删除未知事件，再仅依据保留事件回答；正式 PICTURE 明确省略这一转换。原文案例主要展示 GPT-3.5-Turbo 的输出，并补充检查了 Llama2-7B-chat，但这不意味着方法依赖特定模型架构。

**复现信息**

公平复现时最重要的是保留三项条件。第一，输入必须保持完整，不应预先移除目标角色未知的事件；否则无法检验显式知识缺失能否在信息暴露条件下触发抑制。第二，视角采择输出应允许自由自然语言，不应强制模型返回故事子集、事件编号或其他固定模式。第三，提示必须明确要求同时讨论目标角色“知道”和“不知道”的事件，并使用思维链提示引出逐步解释。论文消融中的 SimToM + CoT 保持思维链因素但仍执行事件隐藏，用于区分收益是否仅来自 CoT；PICTURE w/ Event Hiding 则在自由解释后重新加入事件过滤，用于检验隐藏步骤本身是否引入错误。所给章节未明确报告正式提示的全部模板、解码参数、采样次数或推理温度，复现这些细节时仍需核对论文其他章节或附录。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- BigToM：使用其中 800 个问题。该基准包含较自然、结构化程度较低的叙事，用于检验方法面对接近自然语言的故事时，能否根据角色实际接触的信息推断其错误信念；原文未明确报告这 800 个问题的训练、验证和测试划分。
- ToMi：使用 Wilf 等人（2024）所采用的 1,000 个问题。故事由模板生成、结构较规则，作用是测试模型在受控情节和明确事件链中进行错误信念推理的能力；原文未明确报告具体数据划分。
- FANToM：使用 1,540 个信念问题。该基准由多人对话构成，特定说话者会离开并重新加入，因此可测试模型能否追踪不同参与者分别见证了哪些对话内容；原文未明确报告具体数据划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（Accuracy）**

正确回答的问题数占全部被评估问题数的比例，分别用于三个心智理论基准。 （越高越好，因为更高的准确率表示模型更常依据角色拥有的信息，而非完整故事中的全知信息作答。）

</div>
<div class="metric-item" markdown="1">

**False Belief 准确率**

仅在角色信念与现实状态不一致的错误信念问题上计算准确率，重点测量模型能否抑制角色未见事件所提供的信息。 （越高越好；这类问题最直接暴露模型是否把自身看到的完整叙事错误地当成角色知识。）

</div>
<div class="metric-item" markdown="1">

**All 准确率**

在完整问题集合上计算准确率，并与 False Belief 子集结果并列报告，用于观察方法的总体表现。 （越高越好，但必须结合 False Belief 准确率解释，因为总体分数可能受到较容易或不要求知识抑制的问题影响。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三个心智理论数据集与主实验所用骨干模型上的总体比较

<div class="result-value" markdown="1">

作者报告 PICTURE 在所有数据集和骨干大语言模型上均超过全部基线；所给节选没有表 1 的逐数据集、逐模型分数，因此无法核对每个比较的绝对差值。

</div>

该结果说明收益并非只出现在某一种故事结构中：ToMi 的模板故事、BigToM 的自然叙事和 FANToM 的多人对话均呈现一致方向。不过，这是作者对表 1 的汇总结论；缺少具体分数和显著性检验时，不能据此判断每个设置中的优势大小、方差或统计可靠性。

<div class="result-source" markdown="1">

来源：第 6.1 节 Main Results，表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Picture outperforms all baselines across datasets and backbone LLMs.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 错误信念问题上的核心结果

<div class="result-value" markdown="1">

PICTURE 在错误信念问题上取得平均 7.3% 的提升。原文使用“7.3%”而未在所给节选中说明这是绝对准确率百分点还是相对提升，因此不应擅自转换为“提高 7.3 个百分点”。

</div>

错误信念题要求模型忽略自己在完整故事中看到、但目标角色没有看到的事件，因此该提升直接支持 PICTURE 改善知识抑制的主张。它仍不能单独证明模型形成了类人的心智理论表征：准确率提升也可能部分来自提示措辞、额外推理步骤或输出分布变化。

<div class="result-source" markdown="1">

来源：第 6.1 节 Main Results，表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In particular, it achieves an average improvement of 7.3% on false-belief questions.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 较新骨干模型 Llama3.1-8B-Instruct、Qwen3-8B 与 Gemma3-12B-Instruct 上的扩展评估

<div class="result-value" markdown="1">

作者称 PICTURE 在三种较新大语言模型上相对竞争方法均获得一致改进；所给节选未包含表 5 的具体数值。

</div>

这一结果测试方法是否只对较早模型有效，观察到的一致方向支持其跨模型代际的可迁移性。但由于缺少每个数据集和模型的分数，无法判断改进是否在所有单项设置中都成立、提升幅度是否稳定，也不能排除提示模板与特定模型对齐方式的影响。

<div class="result-source" markdown="1">

来源：附录 B.1 Results on More Recent LLMs，表 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Overall, Picture achieves consistent improvements over the competitive methods across all three LLMs.

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

- Vanilla：直接提示模型回答问题，不加入显式视角采择步骤。它衡量骨干模型原有的心智理论能力，并用于判断 PICTURE 的收益是否只是来自模型自身知识。
- CoT：要求模型生成自由形式思维链，但不专门要求指出角色不知道什么。它是最关键的非视角采择对照，用于区分“一般性增加推理文本”与“明确表述知识缺失”带来的效果。
- SimToM：先通过视角采择隐藏目标角色未观察到的事件，再基于过滤后的故事回答问题。该比较用于判断 PICTURE 在不删除事件、因而仍需主动抑制无关信息的条件下，能否超过传统事件隐藏范式。
- PercepToM：采用感知推断和事件隐藏，并要求生成严格格式的中间输出。它检验 PICTURE 的自由形式解释能否避免结构化中间结果带来的格式失败，同时保持或提升视角采择效果。

**实验想回答的问题**

- RQ1/RQ2：与不显式进行视角采择的提示方法以及基于事件隐藏的视角采择方法相比，PICTURE 是否能让大语言模型更有效地抑制对角色未知事件的利用，并因此更准确地回答错误信念问题？
- RQ3/RQ4/RQ5：PICTURE 是否会按设计在自由形式思维链中明确生成角色的知识缺失，这一机制能否推广到不同类型的心智理论问题，以及加入思维链后，事件隐藏方法能否达到与 PICTURE 相当的表现？

**实验实现**

主实验在三个基准及多个骨干大语言模型上比较 PICTURE 与各类提示方法，并依照 Wilf 等人（2024）分别报告错误信念问题（False Belief）和完整问题集（All）的结果。每个结果使用随机种子 $\{0,111,222,333\}$ 独立运行四次后取平均。Llama2-7B-chat 搭配 PercepToM 的结果未被报告，因为该模型在 PercepToM 的感知推断阶段对超过 95% 的问题反复无法生成有效 JSON 数组；这既体现严格中间格式的实际失败模式，也意味着该模型上的 PICTURE 与 PercepToM 缺少可直接比较的数值。附录 B.1 进一步在 Llama3.1-8B-Instruct、Qwen3-8B 和 Gemma3-12B-Instruct 上采用与第 5.1 节相同的基准进行评估。所给节选未包含表 1、表 5 的具体逐项分数，也未交代解码参数、提示示例数量或统计显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The contribution is a chain-of-thought prompting method that improves Theory-of-Mind reasoning by explicitly representing characters' missing knowledge.; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`679ac87976b6f7a093a17cb74c72057b38ad36033a5a63838632cddeb6028578`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
