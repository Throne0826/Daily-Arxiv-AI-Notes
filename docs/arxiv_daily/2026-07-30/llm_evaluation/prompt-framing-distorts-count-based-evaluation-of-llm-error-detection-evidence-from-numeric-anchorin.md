---
title: "[论文解读] Prompt Framing Distorts Count Based Evaluation of LLM Error Detection: Evidence from Numeric Anchoring"
description: "[arXiv 2607.01240][LLM 评测] 本文指出：当提示词预先给出预期错误数时，大模型可能仅通过迎合该数字提高基于计数的F1，而没有更准确地定位具体错误，因此计数分数会夸大真实的错误检测能力。"
arxiv_id: "2607.01240"
announcement_date: "2026-07-30"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:25.245130+00:00"
source_sha256: "36b3bcd9709126104af7545fe0e8b0691aaae7abb3ae34a7a17b63d8c25f6408"
tags:
  - "LLM 评测"
  - "大语言模型评测"
  - "错误检测"
  - "Count-F1"
  - "计数—跨度差距"
  - "数字锚定"
  - "提示敏感性"
  - "语法错误纠正"
  - "评测污染"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2607.01240</p>

# Prompt Framing Distorts Count Based Evaluation of LLM Error Detection: Evidence from Numeric Anchoring

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Dekun Yang</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.01240v2) · [PDF 下载](https://arxiv.org/pdf/2607.01240v2) · **关键词** 大语言模型评测, 错误检测, Count-F1, 计数—跨度差距, 数字锚定, 提示敏感性, 语法错误纠正, 评测污染  


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

本文指出：当提示词预先给出预期错误数时，大模型可能仅通过迎合该数字提高基于计数的F1，而没有更准确地定位具体错误，因此计数分数会夸大真实的错误检测能力。

**不用术语来说**：校对系统不仅要说出一段文字里有多少处错误，更要找对错误在哪里、错了什么。然而，一些评测只比较模型报告的错误总数与参考总数；如果提示词又提前透露了参考数量，模型即使指出了错误的位置，也可能仅因报出相近数量而获得高分。这会使评测结果看起来很好，却不能证明系统真的更会校对。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出ErrorBench这一受控压力测试协议：保持文本与任务不变，只改变提示词中给出的错误数量，从而直接检验计数线索是否会改变模型的报告数量，并比较不同模型家族的响应差异。
- 作者将Count-F1与基于编辑或跨度匹配的定位指标并列比较，显示“提示真实错误数”带来的计数得分提升并不伴随同等幅度的编辑定位改善，据此提出评测应避免预填错误数，并同时报告跨度感知指标。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型评测与语法错误检测的交叉领域。LLM可被用作校对器、代码审查器或事实核查器，但其检测质量不能只由“报告的错误数量是否等于参考数量”衡量：模型可能猜对总数，却标错具体位置或错误类型。论文关注一种评测污染现象——提示词预先给出期望错误数，而计数指标又以该数为评分目标；此时高分可能主要反映模型遵循提示中的数字，而非真正提升错误定位能力。研究以CoNLL-2014语法纠错文本为受控材料，通过改变提示中的数字线索，考察计数结果与编辑或跨度级结果之间是否出现系统性分离。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**Count-F1（计数F1）**

一种把模型报告的错误总数与参考错误总数进行比较的评分方式，强调数量是否一致。它不充分检查模型指出的是不是正确错误，因此可能在定位很差时仍取得高分。

</div>
<div class="conceptitem" markdown="1">

**跨度或编辑感知评测**

这类评测不仅比较错误数量，还检查原文中的具体错误位置及其修改内容；文中涉及M2风格诊断与ERRANT提取出的编辑级 F_{0.5}。相比纯计数指标，它更能反映模型是否真正找到了并修正了错误。

</div>
<div class="conceptitem" markdown="1">

**数字锚定（numeric anchoring）**

提示中出现的显著数字可能成为模型作答时的参照，使报告数量向该数字移动。本文只把“锚定”作为行为描述，并不声称已经区分了心理式锚定、输出模仿、迎合或一般指令遵循等内部机制。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一段包含若干语法错误的CoNLL-2014文本，LLM需要识别并描述错误，输出中可进一步得到其报告的错误数量、错误位置或对应修改。实验保持文本与任务不变，只改变提示条件：既包括不提供错误数的Blind条件，也包括提供某个预期数量的锚定条件，并可用相互冲突的偏低与偏高数字线索进行压力测试。核心比较是：提示数字是否显著改变模型报告的错误数，以及Count-F1的提升是否远大于编辑级或跨度级质量的提升。其基本假设是，如果提示给出的数字同时接近计数指标的目标，那么模型仅通过服从该数字就可能获得较高Count-F1；因此计数一致不能单独作为定位能力改善的证据。论文将ErrorBench定位为评测协议审计，而非模型排行榜或模型内部机制检验。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$N$**

给定文本的参考错误数量，即锚定提示构造时所依据的目标计数。

</div>
<div class="notationitem" markdown="1">

**$N-2$**

偏低的错误数提示，比参考数量少2，用于测试模型输出是否随低锚点移动。

</div>
<div class="notationitem" markdown="1">

**$N+2$**

偏高的错误数提示，比参考数量多2；它与 N-2 相差4个错误。

</div>
<div class="notationitem" markdown="1">

**$F_{0.5}$**

编辑级F分数，其中精确率的权重高于召回率；本文用ERRANT提取编辑并结合两个CoNLL-2014参考答案计算，以衡量实际修改质量。

</div>

</div>

**直接相关的工作**

- **CoNLL-2014语法错误纠正评测（Ng et al., 2014）及相关GEC研究**: 为本文提供文本、人工参考修改及编辑级评测背景，并说明仅比较错误数量不足以代表语法纠错质量。
- **Perez et al. (2023) 关于LLM迎合行为的研究**: 既有研究发现模型可能顺从用户陈述，即使该陈述错误；本文把这一问题收窄到提示提供具体错误数、模型再估计错误数量的场景。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大模型正被用于文本校对、代码审查和事实核查，实际价值取决于能否准确指出具体错误。但若评测把复杂的检测任务压缩为“报告数量是否等于参考数量”，提示词中泄露的数量信息就可能直接影响得分，导致研究者或使用者误判系统的定位能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于错误数量的F1评测**：将模型报告的错误总数与人工参考总数进行比较，并据此计算Count-F1。该方法简洁，适合快速判断数量是否一致，但不检查模型指出的错误位置或编辑内容是否正确。
- **带计数或位置提示的下游纠错**：任务说明或上游模块先向模型提供约束信息，例如文本含有一个或零个错误，或直接给出预测的错误跨度；下游模型据此生成检测或纠正结果。这类提示可以服务特定工作流，但若评测目标与提示信息重合，分数会同时反映检测能力和指令服从。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 计数指标忽略“错误在哪里”这一核心信息，因此模型可能报对总数却找错具体错误；其后果是接近满分的Count-F1也不能证明错误定位质量较高。
- 当提示词暴露预期错误数，而评测又奖励与该数量一致时，评测输入与评分目标发生信息泄漏；由此得到的提升可能来自数字模仿、指令服从或锚定反应，而非检测能力改善。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有实践表明计数或位置线索会被放入纠错提示，也有研究讨论人类及大模型的锚定效应，但尚缺少一种受控、面向评测有效性的审计：只改变提示中的数字，在其他条件不变时，系统测量计数得分的变化是否显著大于真实编辑或跨度定位质量的变化。作者强调，该缺口关乎评测协议是否可信，而不是判定某个模型家族优劣或识别模型内部的认知机制。

</div>
<div markdown="1"><span>核心问题</span>

在同一文本和同一检测任务下，提示词给出的错误数量是否会系统性改变模型报告的错误数，并使从Blind提示切换到真实数量提示时Count-F1的增幅大于编辑或跨度感知指标的增幅；这种响应在不同模型家族间是否存在描述性差异？

</div>
<div markdown="1"><span>作者直觉</span>

如果提示中出现一个醒目的错误数，善于遵循指令的模型可能把它当作输出规模的目标：数字偏高时多列错误，数字偏低时少列错误。这样做很容易改善“数量是否相等”，却不会自动告诉模型哪些词句真的有错。因此，将提示数字作为唯一操纵变量，并分别观察报告数量与位置匹配质量，就能识别计数分数究竟是在测检测能力，还是在奖励对提示数字的迎合。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ErrorBench不是训练新模型的方法，而是一套受控压力测试协议：它固定文本、模型、输出格式和解码设置，只改变提示中关于错误数量的先验信息，以测量大语言模型报告的错误数是否会被数字锚点牵引，以及这种计数变化是否真正对应更准确的错误定位。输入是从CoNLL-2014构造的四句文本窗口及其人工标注错误，经过五种提示条件调用六个模型，再分别进行计数解析、描述到文本跨度的定位，以及基于纠正文段的ERRANT复核，输出Count Bias、Anchoring Sensitivity Index（ASI）、Count-F1和编辑级微平均F0.5等指标。
技术上的核心对照是：Blind不提供数量，Anchored提供真实错误数，Mislead-Over与Mislead-Under分别提供比真实值高2和低2的数量。若提示数字显著改变模型报告数，却没有带来相称的跨度或编辑匹配提升，就说明仅按“找出了多少个错误”计算的Count-F1可能被提示框架抬高；通俗地说，模型可能只是把答案条目数凑到提示给出的数字，而不是真的更会找错。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造并审计ErrorBench文本单元

将连续句子划分为互不重叠的四句窗口，按Annotator 0的真实错误数N分层抽取原含3至7个错误的143个窗口；随后依据官方SGML文档边界审计并删除20个跨作文边界的窗口，形成123篇主分析文本。纠正文段复现实验对应的初始100篇子集经同类审计后保留83篇。

<div class="method-step__io" markdown="1">

**输入**：CoNLL-2014 Shared Task数据中的连续句子、Annotator 0的M2编辑标注，以及用于敏感性分析的Annotator 1标注。  
**输出**：每篇包含原始文本、Annotator-0错误总数、M2类别和词元索引标注的主数据集，以及用于ERRANT复核的83篇子集。

</div>

**直观理解**：每个样本相当于一小段四句话的作文，并附有人工答案。边界审计避免把两篇不同作文的句子错误拼成同一段，从而让提示与评分使用合法的文本单元。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 施加五种错误数量提示框架

在相同系统提示和结构化输出要求下设置Blind、Informed、Anchored、Mislead-Over和Mislead-Under五个条件；后三类数量提示分别给出N、N+2和max(1,N-2)。所有条件都要求模型按“ERROR N: [description]”逐项回答，并以“TOTAL ERRORS FOUND: N”结束。

<div class="method-step__io" markdown="1">

**输入**：每篇文本及其真实错误数N。  
**输出**：同一文本在无数量信息、仅告知存在错误、真实数量锚定、过高数量误导和过低数量误导下的可比较请求。

</div>

**直观理解**：实验只改变模型事先看到的错误数量线索，其他要求保持一致，因此可以把输出差异主要归因于提示框架。高报和低报条件像是在答题前故意告诉学生一个偏大或偏小的“标准答案数”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 调用六个模型并解析结构化回答

以温度0执行完整的123×6×5实验网格，按固定格式解析各回答中的错误描述和总错误数；重试采用keep-last-success规则。无法解析的计数在Count-F1中记为0，而Count Bias及成对计数分析只使用两条件均可解析的样本并报告有效样本量。

<div class="method-step__io" markdown="1">

**输入**：123篇文本与五种提示条件构成的请求，以及GPT-4o、GPT-5.4、Claude Haiku 4.5、Claude Sonnet 4.6、Gemini 2.5 Flash和Gemini 3.1 Pro Preview。  
**输出**：共3690个审计后主实验单元的模型回答、报告错误数、错误描述及解析状态。

</div>

**直观理解**：让每个模型对每篇文章都经历全部五种提示，形成配对比较，避免把文章难度或模型差异误当成锚定效应。温度0用于减少随机波动，但作者明确指出远程模型调用仍不保证完全确定。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算计数敏感性与描述派生的跨度指标

先计算Count Bias、ASI和不要求跨度匹配的篇章级Count-F1；再从描述中提取被引用的原文片段与纠正片段，将其定位到文章，并构造(sentence,start,end,correction)编辑元组。主分析把无法定位的描述视为假阳性，并以仓库内的strict、detection和overlap匹配规则计算语料级微平均F0.5。

<div class="method-step__io" markdown="1">

**输入**：模型报告数、人工参考数，以及每条结构化错误描述。  
**输出**：提示对报告数量的影响，以及错误是否真正落到正确文本位置并给出相应修改的跨度级诊断结果。

</div>

**直观理解**：计数指标只检查“说了几个”，跨度指标则检查“具体指出哪里错、怎样改”。二者并列可以识别模型为了迎合提示数字而增加条目、但没有提高实际定位质量的情况。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### Count Bias与锚定敏感性指数

$$
\mathrm{CB}_{i}=\hat{N}_{i}-N_{i},\qquad \mathrm{ASI}_{i}(c)=\frac{\left|\mathrm{CB}_{i}(c)-\mathrm{CB}_{i}(\mathrm{Blind})\right|}{N_{i}}
$$

**符号说明**

- $i$：篇章索引。
- $\hat{N}_{i}$：模型在篇章i上报告的错误数量。
- $N_{i}$：篇章i的人工参考错误数量。
- $\mathrm{CB}_{i}$：Count Bias；正值表示模型高报错误，负值表示低报。
- $c$：被评估的提示条件，如Anchored、Mislead-Over或Mislead-Under。
- $\mathrm{Blind}$：不提供任何错误数量信息的基线提示条件。
- $\mathrm{ASI}_{i}(c)$：条件c相对Blind造成的计数偏差变化绝对值，并用真实错误数归一化。

<div class="equation-explanation" markdown="1">

**直观理解**：CB回答模型比人工答案多报或少报了几个错误；ASI不判断偏移方向，而是测量换成某种提示后，报告数量相对Blind移动了多大。除以真实错误数后，不同错误密度的文章更便于比较，但该指标只描述提示响应，不证明模型内部存在特定心理或因果机制。  
**原文位置**：第3.4节 Evaluation Metrics

</div>

</div>

<div class="equation-block" markdown="1">

#### Count-F1的计数重叠构造

$$
\mathrm{TP}_{i}=\min(\hat{N}_{i},N_{i}),\qquad \mathrm{FP}_{i}=\max(0,\hat{N}_{i}-N_{i}),\qquad \mathrm{FN}_{i}=\max(0,N_{i}-\hat{N}_{i})
$$

**符号说明**

- $\hat{N}_{i}$：模型在篇章i上报告的错误数量。
- $N_{i}$：篇章i的参考错误数量。
- $\mathrm{TP}_{i}$：仅按预测数与参考数的数量重叠定义的真阳性数。
- $\mathrm{FP}_{i}$：模型报告数超过参考数的部分。
- $\mathrm{FN}_{i}$：模型报告数少于参考数的部分。

<div class="equation-explanation" markdown="1">

**直观理解**：该构造只比较两个数量：例如模型报告5个、参考也是5个，就会得到5个计数意义上的真阳性，即使这5条都没有指向正确位置。因此它正是论文要压力测试的薄弱点；作者在篇章层面计算Count-F1后再取平均，无法解析的计数记为0。  
**原文位置**：第3.4节 Evaluation Metrics

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。ErrorBench是黑盒推理评测协议，不训练或微调六个受测模型，也没有通过损失函数优化参数；这里的“目标”是比较同一模型、同一文本在不同提示数量线索下的计数指标变化与跨度/编辑指标变化是否一致。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 提示数量操控模块**

以真实错误数N为基准构造五个提示条件；Anchored提供N，Mislead-Over提供N+2，Mislead-Under提供max(1,N-2)。保留样本均满足N≥3，因此两个误导条件给出的数值相差固定的4。

> 直观理解：该模块建立实验中的自变量：既测试真实数量能否抬高计数分数，也用方向相反的错误数字检验模型报告是否会随锚点系统性移动。

**2. 计数评分与锚定敏感性模块**

Count-F1将预测数与参考数的重叠min(预测数,参考数)视为真阳性，不要求任何错误跨度匹配；Count Bias衡量高报或低报，ASI则衡量某提示相对Blind造成的归一化偏移幅度。

> 直观理解：Count-F1容易因“数量接近答案”而变高，即使列出的错误位置完全不对；CB和ASI用于直接观察模型是否被提示中的数字带偏。

**3. 跨度定位与ERRANT双路径验证模块**

主路径从错误描述抽取原文/纠正片段并定位为(sentence,start,end,correction)元组，按strict、detection和overlap规则计算微平均F0.5；复核路径使用ERRANT 3.0.0从完整纠正文本抽取编辑，并进行精确元组及双参考评分。

> 直观理解：两条路径分别检查自然语言错误说明和实际纠正文段，目的是证明计数变化是否对应真实可定位、可匹配的编辑，而不是评分器只看条目数所产生的表面进步。

**训练与推理**

整个流程只有推理与离线评分。主实验对123篇文章、6个模型和5种提示执行完整配对调用；模型在固定系统提示下输出逐条错误描述及总数，随后解析计数并从描述定位编辑跨度。独立复核要求模型生成完整纠正文本，再由ERRANT 3.0.0抽取预测编辑，与Annotator 0进行精确匹配，并通过Annotator 0和1实施双参考敏感性规则。跨模型比较仅作描述性解释，因为模型标签来自OpenAI兼容代理所请求的标识符。

**复现信息**

主实验温度固定为0，输出上限为800 tokens；纠正文段复现实验上限为1400 tokens。审计后主网格为123×6×5=3690个单元，重试使用keep-last-success规则。Count-F1对不可解析计数记0，CB和成对分析只使用可解析配对并报告有效样本量；描述无法定位时在主跨度分析中记为假阳性，缺失纠正文本在ERRANT复核中记为空预测。主描述评分是仓库内实现的M2-style诊断，并非官方M2 scorer；作者声明代码、提示和原始输出将在论文发表后通过匿名研究仓库发布。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- 主实验使用 CoNLL-2014 语法纠错语料中的 123 个篇章。每个篇章分别在五种提示条件下交给六个模型，共形成 123×5×6=3,690 个模型—条件响应；它用于测量数量偏差、提示锚定敏感性以及由错误描述恢复出的编辑定位质量。
- 纠正文段复现实验使用其中 83 个篇章，要求模型输出完整纠正后的文本，再由 ERRANT 抽取编辑并与 CoNLL 的两位标注者比较。每个模型—条件单元均覆盖全部 83 个篇章；缺失调用、缺失纠正文段和不可解析数量按失败处理。
- CoNLL-2014 的人工参考编辑既提供每篇文章的真实错误数量，也提供编辑位置与改法。主路径采用描述派生的 M2 风格匹配；复现路径采用 ERRANT 提取精确编辑元组，并逐句选择两条参考中 F0.5 较高者。作者明确指出，后一规则不是官方 M2 max-match 评分器。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**Count Bias（CB）与 Anchoring Sensitivity Index（ASI）**

CB 是模型报告错误数相对真实错误数的有符号偏差：正值表示多报，负值表示少报；ASI 比较带数字提示的条件与 Blind 条件，衡量模型报告数量随提示数字移动的程度。二者衡量数量行为，而不是错误位置是否正确。 （CB 的绝对值越接近 0，数量越接近参考；ASI 没有可直接解释为“越高越好”的方向，高值表示更受数字线索影响，低值也可能只是持续少报而非真正抗锚定。）

</div>
<div class="metricitem" markdown="1">

**Count-F1**

仅根据预测错误总数与参考错误总数的重合程度计算篇章级 F1；主实验对不可解析数量赋 0。它能测量数量一致性，但不检查模型是否找到了正确的错误跨度或提出了正确修改。 （数值越高表示预测数量与参考数量越一致；但在提示已经提供目标数量时，高分不能单独证明错误检测或定位能力更强。）

</div>
<div class="metricitem" markdown="1">

**跨度／编辑感知 F0.5（描述派生 M2-style 与多参考 ERRANT）**

M2-style F0.5 将模型的错误描述转换为编辑，并在 Strict、Detection 或 Overlap 规则下与人工编辑匹配；ERRANT F0.5 则从完整纠正文段抽取精确编辑元组并与两条人工参考比较。F0.5 对精确率的权重高于召回率，更关注模型提出的修改是否可靠。 （越高表示模型更准确地定位并修正了参考错误。相较 Count-F1，它更接近实际校对质量，但结果仍依赖编辑抽取、匹配规则和参考标注。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 真实数量锚定：比较 Blind 与 Anchored 下的 Count-F1 和描述派生 M2-style overlap F0.5

<div class="result-value" markdown="1">

六个模型平均而言，Blind→Anchored 使 Count-F1 增加 0.163，而跨度感知的 overlap F0.5 只增加 0.059。GPT-5.4 的 Count-F1 从 0.582 跃升至 0.988，但 overlap F0.5 几乎不变，仅从 0.201 到 0.202；其 Anchored 条件下两指标差为 0.786。

</div>

作者据此主张存在 F1 Inflation：当提示直接泄露目标错误数时，模型可以让“报了几个”接近正确，却不必更准确地回答“错误在哪里、如何修改”。GPT-5.4 是最清楚的例子，因为数量分数提高 0.406，而编辑重合只提高 0.001。该结果证明 Count-F1 可被提示框架严重扭曲，但不能证明锚定对所有模型的真实编辑能力都毫无影响；例如 Claude S.4.6 的 overlap F0.5 仍有明显增长。

<div class="result-source" markdown="1">

来源：第4.5节；表4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">For GPT-5.4, Count-F1 changes from 0.582 to 0.988 while overlap F0.5 stays near 0.20.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 冲突数字线索：Mislead-Under 与 Mislead-Over 的配对比较

<div class="result-value" markdown="1">

两种提示仅将所给数量提高四个错误，GPT-4o、GPT-5.4、Claude H.4.5 和 Claude S.4.6 的平均报告数分别随之提高 3.740、3.285、3.610 和 3.537，即达到提示差异的 82%–94%；Gemini 2.5 和 Gemini 3.1 仅提高 0.211 和 0.144。六个变化经 BH 校正后均异于 0（q<.01），但 Gemini 的效应很小。

</div>

由于两个条件除数字外相同，这一比较比“Blind 对真实 Anchored”更直接地证明输出计数会跟随任意数字线索。GPT/Claude 几乎复制提示给出的数量，而 Gemini 在该协议下维持少报倾向。作者特别警告：Gemini 的低响应不能直接解释为更强的普遍鲁棒性，因为它也可能来自难以改变的系统性少报先验。

<div class="result-source" markdown="1">

来源：第4.2节；图3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">The mean reported-count shift is 3.740 for GPT-4o, 3.285 for GPT-5.4, 3.610 for Claude H.4.5, and 3.537 for Claude S.4.6 (Figure 3).</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 完整纠正文段复现：83 篇文章上的 Blind→Anchored Count-F1 与两参考 ERRANT F0.5

<div class="result-value" markdown="1">

跨六个模型平均，Anchored 相对 Blind 使 corpus Count-F1 增加 0.218，而两参考编辑 F0.5 仅增加 0.042。两种增量之差在 GPT-4o、GPT-5.4、两个 Claude 模型和 Gemini 2.5 上的 95% bootstrap 区间均高于 0；Gemini 3.1 的点估计为 +0.072，但区间为[-0.018,+0.161]，跨越 0。

</div>

该复现不依赖模型自行描述错误，而是从完整改写文本中用 ERRANT 抽取编辑，因此降低了“描述解析方式制造差距”的疑虑。五个模型仍显示数量分数增幅显著大于真实编辑分数增幅，支持核心现象具有一定评估路径稳健性；但 Gemini 3.1 的区间跨 0，不能声称六个模型都达到统计显著。

<div class="result-source" markdown="1">

来源：第4.6节；图5、表12

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Across models, Blind→Anchored raises corpus Count-F1 by 0.218 on average and two-reference edit F0.5 by 0.042.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主实验只有 123 篇、纠正文段复现只有 83 篇，且均来自 CoNLL-2014 英语语法纠错数据；实验能支持该受控压力测试中的提示锚定效应，但不能直接外推到其他语言、开放域事实核查、代码审查或长文档校对。
- 描述派生 M2 分数依赖把自然语言说明转换成编辑的覆盖率和匹配规则；ERRANT 复现虽缓解这一问题，但其逐句选择较高 F0.5 参考的规则不是官方 M2 max-match。不同输出缺失模式也可能影响模型比较，因此作者关于模型家族“更顺从”或“更少响应”的结论应限定在当前协议内。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Blind：不向模型提供错误数量，是判断模型自然报告倾向以及衡量 Blind→Anchored 变化的核心基线。
- Informed：告知任务或错误信息但不预填目标数量，用于区分一般任务说明的影响与具体数字线索的影响。
- Anchored：提示中直接给出真实错误数量。它是压力测试条件而非公平的能力基线，用于检验 Count-F1 是否会因答案数量已被泄露而接近满分。
- Mislead-Over 与 Mislead-Under：分别提供偏高和偏低的错误数量，两者相差四个错误而其他提示内容相同。其配对对比可排除“只有真实数字才有效”的解释，直接隔离冲突数字线索对输出数量的因果影响。

**实验想回答的问题**

- 在模型实际定位语法错误的能力基本不变时，提示词中预先给出的错误数量是否会系统性改变模型报告的错误数，并由此人为抬高仅比较数量的 Count-F1？
- 这种“数量得分上涨、编辑定位改善有限”的现象能否跨六个模型成立，并在更严格的描述派生编辑匹配、完整纠正文段与多参考 ERRANT 评分下复现？

**实验实现**

实验比较 GPT-4o、GPT-5.4、Claude H.4.5、Claude S.4.6、Gemini 2.5 和 Gemini 3.1，并对每篇文章施加 Blind、Informed、Anchored、Mislead-Over、Mislead-Under 五种提示。主分析集包含 123 篇；Count-F1 对所有篇章计算，不可解析计数记为 0，而 CB 只在可解析响应上计算。条件相对 Blind 的差异采用篇章级配对 t 检验，并对 24 次检验统一进行 Benjamini–Hochberg 校正；Mislead-Over 与 Mislead-Under 的六个模型配对检验另行进行 BH 校正。纠正文段路径对 83 篇文章进行 1,000 次配对篇章 bootstrap（seed 42），报告 Blind→Anchored 的 Count-F1 变化与两参考 ERRANT F0.5 变化之差及其 95% 百分位区间。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除“数字正确性”因素：仅比较相差四个错误的 Mislead-Under 与 Mislead-Over | GPT/Claude 的计数移动达到所给数字差的 82%–94%，且高数字被精确重复于 93%–100% 的输出；Gemini 精确重复率为 0%。 | 这项控制只改变提示中的数字，因而隔离了数字线索本身，而不是正确答案泄露或其他措辞变化。结果说明高 Count-F1 并非只能由模型识别真实错误产生，模型也可能先接受提示数量，再生成足量错误描述。不过，精确重复提示数仍不等同于每条错误都是虚构的，需结合跨度匹配和案例分析判断内容质量。 | 第4.2节；图3<br><span class="experiment-evidence">The high count is repeated exactly in 93–100% of GPT/Claude outputs and 0% of Gemini outputs.</span> |
| 更换输出与评分管线：由错误描述派生 M2 编辑，改为完整纠正文段经 ERRANT 抽取并进行两参考评分 | 配对 bootstrap 中，Count-F1 增量减 ERRANT F0.5 增量的差值分别为 GPT-4o +0.224 [0.100,0.416]、GPT-5.4 +0.348 [0.286,0.413]、Claude H.4.5 +0.115 [0.065,0.166]、Claude S.4.6 +0.132 [0.075,0.185]、Gemini 2.5 +0.156 [0.080,0.240]、Gemini 3.1 +0.072 [-0.018,0.161]。 | 该消融检验核心结论是否只是“从自然语言错误描述恢复编辑”这一中间步骤的产物。改用完整纠正文段和 ERRANT 后，五个模型的区间仍完全高于 0，说明数量膨胀并不依赖单一解析管线；Gemini 3.1 未达到 95% 显著水平，提示现象强度具有模型差异。此外，这里采用逐句选择较高 F0.5 参考的局部规则，并非官方 M2 max-match，故不应把数值视为官方 CoNLL 排名。 | 附录B.3，表12<br><span class="experiment-evidence">The contrast is positive at the 95% level for five of six models.</span> |

**定性案例**

- 在 conll_0238（真实错误数 N=4）上，GPT-4o 在 Blind 条件只报告了有效的 theirselves→themselves；当 Mislead-Over 提供 M=6 时，它保留该修改并新增五个无依据的错误，包括四个并不存在的标点前空格和 depression 前不必要的冠词。作者将其解释为模型为了达到提示数量而“发明”错误，而非找回其余三个金标准编辑。该案例直观展示了数量吻合如何与定位质量脱钩，但单个案例不能估计这种失败在全部数据中的发生率。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Presents a benchmark showing that prompt-induced numeric anchoring can distort metrics used to evaluate LLM error detection.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`36b3bcd9709126104af7545fe0e8b0691aaae7abb3ae34a7a17b63d8c25f6408`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
