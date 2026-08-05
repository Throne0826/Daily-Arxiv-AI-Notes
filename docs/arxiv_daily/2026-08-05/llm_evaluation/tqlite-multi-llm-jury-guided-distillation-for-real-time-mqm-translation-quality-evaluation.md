---
title: "[论文解读] TQLite: Multi-LLM Jury Guided Distillation for Real-time MQM Translation Quality Evaluation"
description: "[arXiv 2608.02975][LLM 评测] 本文针对基于MQM的翻译质量评估难以兼顾准确性、成本与开放性的问题，系统比较不同规模和推理模式的语言模型，并提出TQLite，将多模型评审团的聚合判断蒸馏到小型开源模型中。"
arxiv_id: "2608.02975"
announcement_date: "2026-08-05"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:42:48.486044+00:00"
source_sha256: "f507c2ef5a4b0c269b385631347d7d7f0e95e4d82d35e7949d4703a347e80291"
tags:
  - "LLM 评测"
  - "LLM 效率"
  - "LLM 其他"
  - "LLM Reasoning"
  - "机器翻译质量评估"
  - "多维质量指标"
  - "LLM-as-a-Judge"
  - "知识蒸馏"
  - "小语言模型"
  - "大推理模型"
  - "WMT22"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.02975</p>

# TQLite: Multi-LLM Jury Guided Distillation for Real-time MQM Translation Quality Evaluation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Bhavin Jawade, Cameron R. Wolfe</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.02975v1) · [PDF 下载](https://arxiv.org/pdf/2608.02975v1) · **关键词** 机器翻译质量评估, 多维质量指标, LLM-as-a-Judge, 知识蒸馏, 小语言模型, 大推理模型, WMT22<br>


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

本文针对基于MQM的翻译质量评估难以兼顾准确性、成本与开放性的问题，系统比较不同规模和推理模式的语言模型，并提出TQLite，将多模型评审团的聚合判断蒸馏到小型开源模型中。

**不用术语来说**：判断一段机器翻译好不好，不仅要看大意是否正确，还要识别错误的位置、类型和严重程度，因此比简单比较译文与参考答案更需要细致推理。强大的大模型能够较好地完成这种判断，但大规模使用时费用高、速度慢，而且许多领先模型并不开源；小模型虽然便宜且便于部署，却通常缺乏足够的评估能力。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者对标准大语言模型、具有显式推理能力的大型推理模型以及小型语言模型进行了覆盖模型规模、推理模式和开放程度的实证比较，用于厘清当前基于MQM的翻译质量评估能力，并指出提示设计和多模型评审会显著影响评估表现。
- 作者提出TQLite：由多个高性能大型推理模型或大语言模型组成评审团，通过多数投票和一致性筛选产生高质量合成监督数据，再将其评估能力蒸馏至小型开源模型，以获得更低成本、更高速度且可复现的翻译质量评估器。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究机器翻译质量评估（translation quality evaluation, TQ）：在不完全依赖人工逐句检查的情况下，判断机器译文相对于源文的质量。传统文本生成指标往往难以处理开放式表达，也可能与人工判断相关性较弱，因此近期方法常采用“LLM-as-a-Judge”，即向大语言模型提供源文、译文和评分规则，让模型模拟人工评审。本文具体采用多维质量指标（MQM）框架：评审者不直接给出笼统总分，而是定位译文中的错误片段，并标注错误类别及严重程度，再由这些标注推导质量分数。研究场景以 WMT22 metrics 测试集为主，覆盖中译英、英译德和英译俄，并同时考察系统级排序与句段级判断。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**LLM-as-a-Judge**

把能力较强的语言模型当作自动评审员，通过提示词向其说明评价标准、评分规则和输出格式，再让它评价给定文本。其目标是以自动化方式逼近人工质量判断，但成本、模型偏差与可复现性仍取决于所用评审模型。

</div>
<div class="concept-item" markdown="1">

**多维质量指标（MQM）**

MQM 是一种细粒度翻译评估框架，要求评审者定位具体错误片段，并为每个错误标注类别及 critical、major 或 minor 等严重程度。最终质量分数由这些错误标注自动推导，而不是由评审者直接给出一个整体印象分。

</div>
<div class="concept-item" markdown="1">

**知识蒸馏**

知识蒸馏利用能力较强但成本较高的教师模型产生监督信号，再训练参数更少、推理更快的学生模型模仿教师。本文背景下，教师信号来自多个大型或推理模型组成的评审团，目标是让小语言模型以较低成本执行 MQM 翻译评估。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

基本输入是一条源语言句子及某个翻译系统生成的目标语言译文；采用参考型指标时还可使用人工参考译文，而参考无关型评估不依赖参考译文。评估器需要依据 MQM 规则识别译文中的错误片段、类别和严重程度，并据此生成可用于比较翻译质量的分数或判断。主要实验设置使用 WMT22 metrics 测试集：三个语言方向为中译英、英译德和英译俄，每个方向约含 $2{,}000$ 条源句，样本来自新闻、社交、对话和电子商务四类领域；54 个人工或机器翻译系统产生的候选译文合计构成 106,758 个待评估句段。人工 MQM 标注被视为金标准，评估性能分别在系统级和句段级衡量：前者检验评估器能否正确比较不同翻译系统的总体优劣，后者检验其能否正确比较具体句段，并对质量相同的情况进行校准。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

待翻译的源语言句子。

</div>
<div class="notation-item" markdown="1">

**$y$**

某个人工或机器翻译系统针对源句生成的候选译文。

</div>
<div class="notation-item" markdown="1">

**$m(x,y)$**

翻译质量评估器根据源句与候选译文给出的 MQM 派生质量分数或比较依据；该记号用于概括任务，原文节选未规定统一函数形式。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{acc}^{\star}$**

经过平局校准的句段级成对准确率，用于衡量评估器的句段级判断与人工 MQM 判断的一致程度。

</div>

</div>

**直接相关的工作**

- **Gemba-MQM**: 该方法将 LLM-as-a-Judge 用于 MQM 翻译评估，通过提示模型识别错误片段并据此评分；本文沿用其标准提示开展模型比较，并采用其评估代码以匹配 WMT22 官方计算流程。
- **AutoMQM**: 该工作系统比较现成及微调后的大语言模型在 MQM 翻译评估中的表现，并表明微调可缩小句段级评估差距；TQLite进一步关注如何把多个强模型的评审能力蒸馏到更高效的小语言模型中。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

基于多维质量指标MQM的翻译评估需要模型按照细化规范识别和权衡多种翻译错误，适合替代昂贵的人工作业，但实际评测可能涉及大量系统和文本片段。当前能力最强的评估器多为大型或闭源模型，逐条调用会带来较高的计算与货币成本，也使本地部署、审计和实验复现变得困难。因此，应用方需要一种能在系统级和片段级保持较强评估能力，同时支持低成本、低延迟和开放部署的模型。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **人工标签监督的学习型翻译指标**：使用人工评审给出的翻译质量标签或错误标注微调较小模型，使其在片段级给出质量判断，或在更细的文本跨度级定位翻译错误。这类方法推理较高效，但能力受人工标注数据的规模、成本和覆盖范围制约。
- **基于大模型评审的直接评分或MQM评估**：向强大语言模型提供源文、译文、评价标准、评分量表和输出格式，让模型像人工评审员一样直接打分；MQM方案进一步要求模型依据多维错误体系分析译文。大型推理模型还可投入更多推理计算，而多个模型组成的评审团可通过投票聚合判断。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有领先的大模型评审器主要依赖GPT-4、PaLM等大型闭源模型，虽然系统级效果强，但调用成本、计算开销和不可控的服务依赖使其难以大规模部署，也不利于完整复现；大型推理模型可能继续提高准确性，却会进一步扩大计算负担。
- 开源模型尤其是小型语言模型尚不能稳定完成MQM所需的复杂判断，与顶尖评审器存在明显能力差距；与此同时，大模型评审对提示设计敏感，单个模型的判断也可能带有自身偏差，因此仅缩小模型或直接采用单一教师都难以同时保证效率与监督质量。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究分别证明了大型模型可作为翻译评审员、微调能够改善片段级表现，也初步探索了较小开源模型，但尚缺少一种经过广泛基准比较验证的方案，能够把多个顶尖推理模型之间较可靠的共识转化为小型开源模型可学习的监督信号，从而系统地协调评估性能、推理成本与模型开放性。该缺口还包括一个实践判断：在模型规模、是否进行推理、提示设计以及单模型或多模型评审等选择之间，哪种配置最适合作为蒸馏教师。

</div>
<div markdown="1"><span>核心问题</span>

能否先通过统一实验确定最可靠的大模型翻译评估配置，再利用多模型评审团的投票结果和一致性筛选构造合成训练数据，将其MQM评估能力蒸馏到小型开源模型，使学生模型在系统级与片段级接近先进大型推理评审器，同时显著降低推理成本并提高可部署性？

</div>
<div markdown="1"><span>作者直觉</span>

不同强模型可能各自在某些错误类型或语言现象上出错，但它们对同一译文形成一致判断时，该判断通常比任一单模型输出更适合作为训练标签。多数投票可削弱个别教师的偶然错误，一致性筛选则避免让学生学习争议过大的样本；随后，小模型把昂贵评审团逐例完成的判断模式压缩进参数中，部署时只需运行一次小模型推理。直观而言，这是用高成本评审团离线“编写教材”，再让低成本学生在线独立答题，而不是在每次评估时重新召集评审团。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

TQLite 的目标是把大型推理模型在 MQM 翻译质量评估中的能力蒸馏到小语言模型。根据摘要，训练端先由多个大型推理模型组成“评审团”，分别评价翻译样本，再通过数据筛选和响应聚合形成高质量合成监督数据，最后用这些数据训练小语言模型；部署时，小模型直接对新翻译执行 MQM 风格评估，以降低大规模评测的计算成本。技术上，MQM 不要求直接猜测一个总体质量分，而是先识别译文中的错误片段，并为错误分配类别和严重程度，再从这些结构化错误推导最终分数。

直观地说，该方法让多个能力较强但昂贵的“教师评委”共同制作训练题与参考答案，再让便宜的小模型学习这些判断。需要注意，所给章节仅完整描述了数据、MQM 评估框架、指标和基线；并未给出教师模型名单、评审响应的具体聚合算法、数据筛选阈值、小模型训练损失或提示模板，因此下述流程只能忠实概括摘要明确披露的端到端设计，不能据此复现全部训练细节。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造待评估翻译样本

从翻译评测数据中整理可供教师模型判断的样本，并通过作者所称的 practical data curation techniques 进行数据筛选或整理。所给材料未说明筛选规则、采样比例以及是否对语言对、领域或翻译系统进行均衡。

<div class="method-step__io" markdown="1">

**输入**：包含源句、候选译文以及在参考型设置下可能使用的参考译文的翻译质量评估样本。<br>
**输出**：提交给多模型评审团的候选训练样本集合。

</div>

**直观理解**：这一步相当于先整理教师要批改的试卷，并尽量排除不适合教学或质量可疑的题目。具体如何挑题，当前摘录没有交代。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多大型推理模型独立进行 MQM 评价

不同教师模型对同一候选译文生成 MQM 风格的评价响应，原则上识别错误片段，并标注错误类别及 critical、major 或 minor 严重程度。所给章节说明最终 MQM 分数可由这些错误标注自动推导，但未给出 TQLite 使用的错误权重和分数计算细节。

<div class="method-step__io" markdown="1">

**输入**：每个候选样本及其评估提示；摘要表明教师端由多个大型推理模型组成，但未披露具体模型和提示内容。<br>
**输出**：同一样本对应的多个教师评价响应。

</div>

**直观理解**：不是让一名教师决定答案，而是让多名强模型分别批改同一译文。这样可以利用模型间的互补判断，减少依赖单个教师偶然出错的风险。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 聚合评审响应并生成合成监督数据

对多模型响应进行 aggregation，形成用于蒸馏的统一监督信号，并与筛选后的输入样本配对构成合成训练集。摘要明确存在跨模型响应聚合，但所给材料未说明采用投票、分数平均、错误片段合并、置信度加权还是其他一致性规则。

<div class="method-step__io" markdown="1">

**输入**：多个大型推理模型对同一样本给出的 MQM 评价响应。<br>
**输出**：由输入样本和聚合 MQM 标签或评价响应组成的高质量合成训练数据。

</div>

**直观理解**：这一步类似汇总多名评委的意见，制作一份较稳定的参考答案。聚合是 TQLite 区别于单教师蒸馏的关键环节，但当前摘录不足以判断它如何解决评委意见冲突。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 训练并部署小语言模型评估器

使用合成数据训练小语言模型，使其学习教师评审团的 MQM 判断能力；推理时，小模型直接处理新的翻译样本并输出 MQM 风格评价或由错误标注推导的质量分数。所给材料未报告训练损失、参数更新方式、输出格式约束以及推理阶段是否需要参考译文。

<div class="method-step__io" markdown="1">

**输入**：经过数据整理和多模型响应聚合得到的合成监督数据，以及待蒸馏的小语言模型。<br>
**输出**：可用于实时或大规模翻译质量评价的轻量级 MQM 评估器及其预测结果。

</div>

**直观理解**：昂贵的教师模型只在制作训练数据时使用，线上评估则交给成本更低的小模型。这样把计算开销从每次请求都调用大模型，转变为一次性教师标注加持续的小模型推理。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：所给材料没有给出 TQLite 的显式训练目标、损失函数或优化公式，因此不能确认其采用标准自回归监督微调、分数回归、分类损失、排序损失，还是这些目标的组合。可以确定的只有优化方向：让小语言模型学习由多大型推理模型评审团生成并聚合后的 MQM 监督信号，从而改善其翻译质量评估能力；任何更具体的目标函数均需查阅论文方法章节后才能确认。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 多大型推理模型评审团**

该模块使用一组具有差异性的模型对相同翻译样本生成多个评价响应，以替代单一教师产生蒸馏标签。摘要将其描述为 multi-LRM jury，并强调评审模型具有多样性；当前材料没有提供评审团规模、模型身份或独立采样次数。

> 直观理解：不同强模型可能擅长发现不同类型的翻译错误。让它们共同参与，可以避免小模型只模仿某一个教师的系统性偏差。

**2. 数据整理与评审聚合**

该模块将 practical data curation techniques 与跨模型评价响应聚合结合，用于生成质量较高的合成训练监督。它决定哪些样本进入训练集以及教师意见如何合并，但摘录未披露过滤条件、冲突处理规则或聚合算法。

> 直观理解：多教师并不自动等于高质量数据：低质量题目和互相矛盾的答案仍需处理。该模块相当于训练数据的编辑与审校环节，是蒸馏是否可靠的核心。

**3. MQM 风格小模型评估器**

学生端是面向翻译质量评价的小语言模型，通过合成监督学习 MQM 所要求的错误定位、错误分类和严重程度判断，并据此产生可比较的评价结果。现有摘录未明确学生模型结构、参数规模、是否输出完整错误跨度，以及最终分数的具体计算规则。

> 直观理解：学生模型学习的不是简单词面相似度，而是像人工评审一样分析译文哪里错、错得多严重。其价值在于以较低推理成本逼近大型推理模型评估器的判断能力。

**训练与推理**

训练阶段包括四个逻辑环节：准备翻译评价样本；让多个大型推理模型分别生成 MQM 风格响应；通过数据整理和跨模型聚合构造合成监督集；用该监督集蒸馏小语言模型。摘要声称这种训练可使小模型接近最佳大型推理模型评估器的 MQM 表现，但当前摘录没有提供训练轮数、数据规模、教师调用策略、标签格式或模型选择规则。

推理阶段不再需要完整的多模型评审团，而是由训练后的小模型直接评价候选译文。按照所给 MQM 预备知识，合理的评估接口应围绕错误片段、错误类别和严重程度组织，并从这些信息获得最终质量判断；然而，原文摘录没有明确 TQLite 在推理时输出结构化错误列表还是仅输出分数，也没有说明参考译文是否必需，因而不能进一步断言。

**复现信息**

实验主要采用 WMT22 metrics task 测试集：覆盖 zh-en、en-de 和 en-ru 三个语言对，每个语言对约有 2,000 个句子，句子来自新闻、社交、对话和电子商务四类领域；候选译文由 54 个人工或机器翻译系统生成，总计 106,758 个待评估片段。人类标注的 MQM 结果被用作金标准，其中标注者识别单个错误片段并赋予错误类别及 critical、major 或 minor 严重程度，最终分数由这些标注推导。

公平解释结果时，应注意作者使用 WMT22 官方评估脚本，并具体采用 Gemba-MQM 仓库中的评估代码以保持一致；评价指标是系统级成对准确率和带平局校准的片段级成对准确率 $\texttt{acc}^{\star}$。作者明确避免报告系统级和片段级相关性指标，理由是其容易受到小样本和离群值影响。当前材料没有给出 TQLite 的教师与学生模型配置、合成训练集规模、超参数、硬件、提示模板、解码设置或响应聚合实现，因此这些均属于复现所缺失的关键信息。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- WMT22 metrics test set：用于所有评审模型、提示格式和 TQLite 学生模型的最终比较，覆盖英德、英俄和中英三个语言方向。实验采用无参考设置，即评审器只读取源句与候选译文，不使用人工参考译文；同一测试集同时报告系统级及句段级准确率。
- 约 300 万条源句—译文候选池：从 OPUS-100、OPUS Books、Europarl、OPUS TED Talks、Tanzil、Wikipedia、Tatoeba，以及 WMT 2015、2017、2019 汇集而成，覆盖西班牙语、俄语、德语、中文、英语、日语和印地语。它不是最终测试集，而是供 LRM 生成 MQM 错误跨度、类别和严重程度标注的合成训练数据来源。
- Perfect-Agreement 合成训练子集：经过多 LRM 评审及一致度过滤后保留 99,214 条、约 10 万条高质量样本，作为论文默认的微调数据。另用 2 万条规模的子集比较不同一致度阈值与 LoRA 秩，并用从 5 千条到约 9.9 万条的规模序列研究数据量效应。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**系统级准确率（System-Level Accuracy）**

衡量评估器在翻译系统整体质量比较或排序上与 WMT22 人工判断的一致程度。它主要回答评估器能否选出整体更好的翻译系统；原文节选未给出该指标的完整计算公式。 （越高越好，因为更高数值表示系统层面的判断更符合人工评估。）

</div>
<div class="metric-item" markdown="1">

**句段级准确率（Segment-Level Acc*）**

衡量评估器对单个源句—译文实例的质量判断与人工标注的一致程度，分别报告英德、英俄、中英及三者平均值。它比系统级指标更直接检验细粒度错误识别能力；星号所对应的精确定义在所给节选中未展开。 （越高越好，因为模型需要在单句层面更稳定地区分译文质量。）

</div>
<div class="metric-item" markdown="1">

**准确率—推理时间权衡**

Figure 7 将平均句段级准确率与推理时间联合考察，用于比较评审质量和部署速度，而不是只比较准确率。论文还使用“accuracy × inference time”这一表述，但所给节选未明确给出其公式、单位或具体数值。 （理想情况是准确率更高且推理时间更低；由于原文未明确该复合量的方向和公式，不宜仅凭乘积名称判断越高或越低越好。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### TQLite 蒸馏后的 Gemma-3-12B-it 与其预训练版本及开放 LRM 基线比较

<div class="result-value" markdown="1">

蒸馏模型的三语言平均句段级准确率达到 55.03%，并被作者报告为同时改善句段级与系统级表现。按 Table 2 的数值，它高于 Qwen-3-8B-thinking 的 50.57%、Qwen-3-32B-thinking 的 52.74%、DeepSeek-R1-Distill-Llama-8B 的 48.41%和 70B 的 51.73%，但仍低于最佳闭源 LRM。

</div>

作者据此主张，多 LRM 教师生成并经一致度筛选的监督信号可以显著增强小型开放模型，使 12B 学生超过所测开放推理模型。分析上，这说明专门任务蒸馏可以比直接依赖通用推理能力更有效；但它不证明学生在所有语言、其他年份 WMT 数据或不同 MQM 规范下都优于开放 LRM，因为最终比较集中在 WMT22 和三个语言方向，而且节选未提供统计显著性。

<div class="result-source" markdown="1">

来源：Section 6.2, “Comparison against larger models”; 开放 LRM 对照数值见 Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For gemma-12b-it, we observe that distillation consistently improves both segment-level and system-level performance over its pretrained counterpart, achieving an average segment-level accuracy of 55.03%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 闭源 LRM 在 WMT22 系统级和句段级评估中的性能上界

<div class="result-value" markdown="1">

OpenAI o3-high 获得最高的系统级准确率 92.34%；Gemini-2.5-Pro-thinking 获得最高的单模型平均句段级准确率 57.06%。这表明系统级最强模型与句段级最强模型并不相同。

</div>

作者的结论是 LRM 整体上构成最强评审器，其中额外推理尤其有利于系统级判断。更谨慎的解释是，不同粒度的指标考查不同能力：系统汇总可能抵消单句噪声，因此系统级领先不能自动推出错误跨度识别也最佳；同时，部分开放 LRM 明显落后，说明“采用推理模型”本身并不是充分条件。

<div class="result-source" markdown="1">

来源：Table 2 and Section 4, “Reasoning models”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In particular, o3 with high reasoning effort achieves a state-of-the-art system-level accuracy of 92.34%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 不同 LRM 组成的三模型评审团与单模型、同模型多输出聚合比较

<div class="result-value" markdown="1">

由 o4-mini-high、o3-high 和 o1-high 组成的多 LRM 评审团取得 89.78% 系统级准确率和 57.07% 平均句段级准确率；后者略高于最佳单模型 Gemini-2.5-Pro-thinking 的 57.06%。同一 o4-mini-high 重复三次的聚合结果为 87.96% 和 56.29%，说明异构教师的收益主要体现在句段级且比同模型重复采样更稳定。

</div>

该结果支持用多样化教师产生蒸馏标签：不同模型的错误倾向可以相互抵消，而不只是通过重复采样降低随机性。不过，多 LRM 评审团的系统级结果仍低于 o3-high 的 92.34%，所以集成不是所有指标上都占优；57.07% 相对 57.06% 的优势也极小，不能在缺少置信区间时解读为确定的统计提升。

<div class="result-source" markdown="1">

来源：Table 2 and Figure 3; Section 4, “Multi-LRM jury”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Aggregating over outputs from different LRMs yields a more consistent performance improvement compared to aggregating over several outputs from the same LRM.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主要准确率结论来自 WMT22 的英德、英俄和中英方向；尽管合成训练池覆盖七种语言，所给实验没有展示西班牙语、日语、印地语或其他领域上的独立测试，因此跨语言和跨领域泛化仍需验证。
- 节选未报告置信区间、统计显著性、人工错误分析、完整成本数字或 Figure 7 的推理时间数值；此外，多教师一致可能形成共同偏差。因此，诸如 57.07% 对 57.06% 的微小差距以及“最佳成本—性能权衡”都应在复核原始图表和运行条件后再作强结论。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 传统或专门训练的翻译质量指标：BLEURT-20、COMET-22、MetricX-XXL-MQM-2020、COMET-QE 和 COMET-Kiwi。它们提供非通用生成式评审器的参照，其中 MetricX-XXL-MQM-2020 是较强句段级基线。
- 通用 LLM/SLM 评审器：包括 GPT-4、GPT-4o、GPT-4o-mini、Gemma-3-27B-it 和 Gemma-3-4B-it 等。该组用于判断模型规模、开放或闭源属性以及提示设计对 MQM 评估能力的影响；未微调的 Gemma 模型也是衡量蒸馏增益的直接起点。
- 单个 LRM：包括 Qwen-3-thinking、DeepSeek-R1-Distill、OpenAI o1/o3/o4-mini 和 Gemini-2.5-thinking。它们代表计算成本较高但推理能力更强的教师及性能上界，用于检验 TQLite 是否能以小模型逼近强推理评审器。
- 多输出与多 LRM 评审团：前者对同一 LRM 的多个输出求平均，后者对不同 LRM 的输出求平均。二者用于区分重复采样带来的方差降低与模型多样性带来的互补收益，并为合成标注和蒸馏提供教师信号。

**实验想回答的问题**

- 不同规模与类型的评审模型——小语言模型（SLM）、通用大语言模型（LLM）和具备显式推理能力的大推理模型（LRM）——在无参考 MQM 翻译质量评估中分别能达到怎样的系统级与句段级表现？提示格式、推理强度及多模型集成会如何影响结果？
- 能否用多 LRM 评审团生成并筛选合成 MQM 错误标注，再将其蒸馏到较小的开放模型中，使学生模型以更低推理成本接近强 LRM 的评估能力？训练数据的评审团一致度、样本量和可训练参数量是否决定蒸馏效果？

**实验实现**

基准阶段固定采用 Gemba-MQM 的三个少样本示例和无参考评估设置，在 WMT22 上逐步比较模型选择、自由文本或结构化文本或 JSON 输出、多轮或单轮提示、零样本思维链、推理强度及评审团聚合。后续实验采用单轮 TQLite-ST 提示和结构化文本输出，因为它能减少依赖脆弱解析启发式的格式错误，同时相较 JSON 的性能损失较小。评审团的最终句段分数通过平均多个输出的 MQM 分数获得。合成数据阶段以约 300 万个源句—译文对为候选，教师集合使用 OpenAI o1 与 o3，GPT-4.1-mini 充当元评审器以聚合错误跨度；默认只保留 Perfect-Agreement 样本。学生模型为 Gemma-3-12B-it 和 Gemma-3-4B-it，采用监督微调及 LoRA 参数高效适配，默认 LoRA 秩为 256。速度实验通过 OpenAI API 运行闭源模型，并以 vLLM 在 4 张 A100 40GB GPU 上运行 Gemma-3-12B-it；原文节选未报告解码参数、重复运行次数或显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 固定 Gemma-3-12B-it 和 2 万条训练样本，逐步放宽评审团一致度过滤：Perfect、Perfect + High、加入 Moderate、再加入 Low | 只使用 Perfect-Agreement 数据时平均句段级准确率最高，为 53.54%；加入 High 后为 53.44%，再加入 Moderate 后降至 52.21%，加入 Low 后进一步降至 51.24%。从最严格到包含 Low 的设置下降 2.30 个百分点。 | 该消融主要隔离合成标签质量，而不是学生架构或基本训练算法。结果说明高一致度是有效的数据质量代理：在样本预算相近的比较意图下，低一致度教师标注带来的噪声超过了新增样本的收益。不过，一致度只表示教师彼此相同，不保证教师共同结论一定符合人工 MQM 标注，因此它是过滤启发式而非真实正确率证明。 | Figure 6 and Section 6.2, “Impact of varying Data Quality”<br><span class="experiment-evidence">Training with only Perfect-Agreement data yields the highest accuracy (53.54%), closely followed by Perfect + High agreement (53.44%). Performance declines as lower-agreement samples are introduced, dropping to 52.21% with Moderate and 51.24% when Low agreement data is included.</span> |
| 固定 Gemma-3-12B-it 与 2 万条训练数据，改变 LoRA 秩以调整可训练参数量 | 句段级准确率从 LoRA 秩 16 时的 52.91%上升到秩 128 时的峰值 53.80%，秩 256 时出现轻微回落；节选未明确给出秩 256 的具体准确率。 | 该实验隔离参数高效微调容量的影响。中等 LoRA 秩已足以适配 MQM 判断任务，继续增加可训练参数并不保证更好。作者将秩 256 的回落解释为 2 万条数据不足及可能的轻度过拟合，但这是推测而非由训练—验证曲线或独立过拟合检验直接证明的因果结论。 | Figure 5 and Section 6.2, “Number of training parameters”<br><span class="experiment-evidence">Accuracy rises steadily from rank 16 (52.91%) to a peak at rank 128 (53.80%), indicating that moderate capacity yields the best adaptation in this setting.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：系统评测不同规模模型的翻译质量评估能力，并以多模型评审蒸馏出可实时部署的小型评估器。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`f507c2ef5a4b0c269b385631347d7d7f0e95e4d82d35e7949d4703a347e80291`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
