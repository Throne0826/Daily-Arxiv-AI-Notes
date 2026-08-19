---
title: "[论文解读] VARM-Bench: Benchmarking Verifiable Structured Reasoning in Chinese Abusive Speech Moderation"
description: "[arXiv 2608.15600][LLM 评测] VARM-Bench旨在检验中文辱虐言论审核模型能否生成可被确定性解析和核验的结构化理由，从而揭示最终标签正确时仍可能存在的目标、立场与伤害类别判断错误。"
arxiv_id: "2608.15600"
announcement_date: "2026-08-18"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:18:42.982364+00:00"
source_sha256: "e48a7da9f00567da4f996810078d615c0e31acb66c84668b048b68fbf909770a"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "中文辱虐言论审核"
  - "可验证结构化推理"
  - "字段锚定思维链"
  - "确定性解析"
  - "目标识别"
  - "作者立场"
  - "细粒度有害类别"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.15600</p>

# VARM-Bench: Benchmarking Verifiable Structured Reasoning in Chinese Abusive Speech Moderation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Mingyu Yuan, Shengtao Wen, Lingbing Guo, Zhen Bi, Xiang Chen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> MIIT Key Laboratory of Pattern Analysis and Machine Intelligence；College of Computer Science and Technology；Nanjing University of Aeronautics and Astronautics；Nanjing University；College of Computer Science, Huzhou Normal University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.15600) · [PDF 下载](https://arxiv.org/pdf/2608.15600) · **关键词** 中文辱虐言论审核, 可验证结构化推理, 字段锚定思维链, 确定性解析, 目标识别, 作者立场, 细粒度有害类别<br>
**代码**: [https://github.com/NUAA-MMMI/VARM-Bench](https://github.com/NUAA-MMMI/VARM-Bench)

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

VARM-Bench旨在检验中文辱虐言论审核模型能否生成可被确定性解析和核验的结构化理由，从而揭示最终标签正确时仍可能存在的目标、立场与伤害类别判断错误。

**不用术语来说**：一条中文评论即使含有冒犯性词语，也不一定是在实施攻击：作者可能是在引用他人的话、反对辱骂，或只是中性提及某个群体。只检查模型最后给出的“有害/无害”标签，无法知道模型是否找对了被谈论的对象、理解了作者态度，并依据正确语境作出决定；这会让表面准确的审核系统隐藏实质性的判断错误。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出VARM-Bench，将目标、目标类型、目标是否明确、作者立场、伤害性标签和细粒度类别六项审核决定嵌入一段带显式锚点的自然语言理由，并从模型输出中确定性地重建完整审核记录。
- 建立区分最终决定、字段正确性、输出有效性和完整记录一致性的多层评测协议，并通过困难无害样本、隐藏记录错误和字段级瓶颈分析，检验模型是否依据正确对象与语境完成审核。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于中文辱虐言论审核与可验证自然语言推理的交叉研究。传统任务通常只判断文本是否有害，或进一步预测攻击类别和目标，但最终标签正确并不意味着判断依据正确：模型可能找错被指对象，把引用、反对或中性提及误判为作者攻击，仍偶然得到正确标签。中文社交媒体中的隐指、谐音替换、否定、引用和讽刺进一步放大了这一问题。VARM-Bench因此把审核结论表示为可从同一段自然语言解释中确定性恢复的六字段记录，使目标、作者立场与有害类别能够联合核验；这里的“可验证”仅指输出可被解析和对照标注检查，并不表示能够观察模型内部的真实推理过程。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**辱虐言论审核**

判断文本是否实施或认可针对某个对象的侮辱、歧视或其他攻击，并在需要时确定攻击目标及类别。仅看到冒犯性词语并不足以判定有害，还必须结合这些词由谁表达、指向谁以及作者持何种立场。

</div>
<div class="concept-item" markdown="1">

**字段锚定的思维链**

模型生成一段自然语言审核理由，并以固定锚点明确写出目标、目标类型、目标显隐性、作者立场、有害性标签和细粒度类别。锚点让程序能够提取关键结论，而锚点之间的文字保留面向人工审计的上下文依据。

</div>
<div class="concept-item" markdown="1">

**确定性验证**

使用固定规则解析模型输出并逐字段与参考记录比较，相同输出总会得到相同评分，不依赖另一个大语言模型充当裁判。它验证的是模型明确陈述的审核记录，而不是模型未显式呈现的内部计算。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

数据集中第$i$个样本由中文社交媒体文本$x_i$、六字段参考审核记录$z_i=(t_i,\tau_i,\epsilon_i,s_i,y_i,c_i)$及参考解释$r_i$组成。模型在只给定$x_i$的条件下生成一段解释$\hat r_i=f_\theta(x_i)$，并须依次使用`[T:]`、`[TY:]`、`[TT:]`、`[S:]`、`[L:]`和`[C:]`六个锚点；确定性解析器$\mathcal P$随后从$\hat r_i$恢复预测记录$\hat z_i$。六个输出分别表示主要判断所针对的最短稳定指称、指称范围、目标是否明示、作者对相关攻击命题的立场、文本是否实施或认可辱虐，以及审核类别；其中无害样本的类别统一为“非攻击”。任务假设所有字段预测都来自同一段解释，不额外生成独立字段元组，从而可以检查解释中陈述的目标、立场、标签和类别是否彼此一致并符合输入语境。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x_i$**

第$i$条待审核的中文社交媒体文本。

</div>
<div class="notation-item" markdown="1">

**$z_i=(t_i,\tau_i,\epsilon_i,s_i,y_i,c_i)$**

第$i$条样本的参考审核记录，依次包含目标、目标类型、目标显隐性、作者立场、有害性标签和细粒度类别。

</div>
<div class="notation-item" markdown="1">

**$\hat{r}_i=f_\theta(x_i)$**

参数为$\theta$的模型根据输入$x_i$生成的字段锚定自然语言解释。

</div>
<div class="notation-item" markdown="1">

**$\hat{z}_i=\mathcal{P}(\hat{r}_i)$**

确定性解析器$\mathcal P$从生成解释中恢复出的六字段预测审核记录。

</div>

</div>

**直接相关的工作**

- **ERASER: A Benchmark to Evaluate Rationalized NLP Models**: 该工作研究带理由的自然语言处理模型评估，为“除最终预测外还应检查解释依据”提供相关背景；VARM-Bench进一步针对中文辱虐审核，把六项审核决定嵌入固定锚点，使其能够恢复为完整结构化记录并进行确定性核验。
- **ROSCOE: A Suite of Metrics for Scoring Step-by-Step Reasoning**: 该工作关注分步推理文本的自动评分，与本文的解释质量评估问题直接相关；VARM-Bench的核心区别是使用领域字段锚点和确定性解析器检查审核决定，并明确不把生成解释视为模型内部推理的忠实记录。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

中文社交媒体中的隐含指代、谐音替换、否定、引用和讽刺会改变话语所指对象及其真实攻击性。审核模型若只碰巧给出正确标签，却误判攻击目标、作者立场或伤害类别，其决定便难以审计，也可能在引用辱语、反对攻击或中性身份提及等场景中造成不可靠的内容处置。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **标签分类与细粒度类别评测**：根据输入文本预测是否有害，或进一步预测冒犯、偏见、隐性毒性等细粒度类别，再以最终标签或类别是否匹配参考答案来评价模型。
- **目标感知结构化抽取与自由文本理由**：前者从文本中抽取攻击目标或输出若干结构化字段；后者让模型用自然语言解释审核决定，以表达目标、语境和立场之间的关系。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 最终标签或孤立字段不能验证审核决定的完整依据：模型可能找错指代对象、把被引用或被否定的辱骂当成作者立场，或者输出与目标和语境不一致的伤害类别，但仍获得正确的最终标签。
- 目标片段不能说明作者是在攻击、反对、引用还是中性提及该目标；自由文本理由虽能表达这些关系，其核心判断却难以稳定抽取和一致评分，因而通常无法进行可复现、无需大模型裁判的确定性核验。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有中文辱虐言论基准缺少一种统一表示：它既要保留自然语言理由以呈现语境关系，又要让目标、目标属性、作者立场、伤害性和类别等关键决定能够被明确恢复，并逐字段、逐记录地确定性验证。由此，标签级性能与完整审核记录可靠性之间的差距尚未被系统测量。

</div>
<div markdown="1"><span>核心问题</span>

在统一的结构化输出协议下，能否从中文辱虐言论审核模型生成的理由中确定性重建六字段完整记录，并据此判断模型不仅给出了正确的最终标签，而且对目标、立场、伤害性和细粒度类别形成了彼此一致、可追溯的判断？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是为自然语言理由加入显式字段锚点。这样，理由仍可描述“谁被谈论、作者持何态度、为何构成或不构成伤害”，解析器又能把其中六项决定机械地还原为固定记录，与人工参考逐项比较。通俗地说，这相当于要求模型在提交审核结论时同时填写一张可自动验收的依据表，从而把“答案碰巧正确”和“整套判断过程在可观察层面一致”区分开来；论文同时明确，这类生成理由只是可检查的说明，并不被视为模型内部推理的忠实记录。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

VARM-Bench把中文辱虐言论审核建模为“生成一段可解析、可审计的自然语言推理”，而不是只预测有害或无害标签。对每条输入文本$x_i$，模型$f_\theta$必须按固定顺序生成包含六个锚点的审核思维链$\hat r_i$：目标对象、目标类型、目标显式性、作者立场、有害性标签和细粒度类别；确定性解析器$\mathcal P$再从同一段文本中恢复六字段预测记录$\hat z_i$。评测一方面比较各字段及完整记录与参考记录$z_i$的一致性，另一方面保留锚点之间的解释文字，以便人工或后续审计检查模型是否引用了输入证据、正确处理上下文，并给出了足以支持结论的推断。

关键设计是让“机器可评分的结构化答案”和“人可阅读的输入特定解释”共用一个输出，而不让模型另行生成字段元组。直观地说，六个锚点类似审核表中的固定栏目，栏目之间的自然语言则相当于审核员填写的理由：解析器负责读取栏目答案，审计者负责判断理由是否真正说明了为何该对象受到何种表达、作者是否认同该表达，以及最终标签和类别为何成立。论文所称“可验证推理”仅指这种输出可被确定性解析和审核的操作属性，并不表示能够观察模型内部的潜在计算过程。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造带解释的参考审核样本

将样本表示为$(x_i,z_i,r_i)$，其中六字段记录为$z_i=(t_i,\tau_i,\epsilon_i,s_i,y_i,c_i)$，字段锚定的参考思维链$r_i$负责用输入证据解释这些决定；全部$N$条样本组成基准数据集$\mathcal D$。

<div class="method-step__io" markdown="1">

**输入**：第$i$条中文文本$x_i$及其人工审核信息。<br>
**输出**：包含输入文本、结构化参考记录和参考解释的数据集$\mathcal D$。

</div>

**直观理解**：这相当于同时保存审核题目、标准表格答案和审核理由，因此既能核对结论，也能检查结论是怎样从原文得到的。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成单一锚点式审核推理

模型$f_\theta$生成一段自然语言审核思维链$\hat r_i$，并严格按$\texttt{[T:]}\rightarrow\texttt{[TY:]}\rightarrow\texttt{[TT:]}\rightarrow\texttt{[S:]}\rightarrow\texttt{[L:]}\rightarrow\texttt{[C:]}$依次表达目标、目标类型、目标显式性、作者立场、有害性标签和类别。

<div class="method-step__io" markdown="1">

**输入**：仅输入待审核文本$x_i$，不向模型提供参考记录$z_i$或参考推理$r_i$。<br>
**输出**：兼具固定结构与自由解释文字的单一生成结果$\hat r_i$。

</div>

**直观理解**：模型不是只给“有害”二字，而是按固定栏目交代攻击谁、对象如何出现、作者是否赞同相关说法，以及据此作出的标签和分类。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 确定性解析与记录重建

确定性解析器$\mathcal P$读取六个锚点对应的值，重建$\hat z_i=(\hat t_i,\hat\tau_i,\hat\epsilon_i,\hat s_i,\hat y_i,\hat c_i)$；这些字段全部来自同一段$\hat r_i$，模型不再生成独立的字段元组。

<div class="method-step__io" markdown="1">

**输入**：模型生成的锚点式推理$\hat r_i$。<br>
**输出**：可用于字段级和联合评分的预测审核记录$\hat z_i$，以及原样保留的解释文本$\hat r_i$。

</div>

**直观理解**：解析器像读取格式固定的审核单，自动取出每个栏目的答案；由于表格答案与解释来自同一份输出，可以减少两套输出彼此矛盾的空间。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 结构评分与理由审计

自动评测比较六个字段各自及其联合结果是否与$z_i$一致，同时利用锚点之间保留的文字审计解释是否基于$x_i$中的具体证据、是否正确处理引述、否定或反对、隐式指代、讽刺和行为批评等语境现象，以及推断是否充分。

<div class="method-step__io" markdown="1">

**输入**：预测记录$\hat z_i$、参考记录$z_i$、生成解释$\hat r_i$及原输入$x_i$。<br>
**输出**：字段级与联合一致性结果，以及针对解释依据、语境正确性和推断充分性的可审计材料。

</div>

**直观理解**：结构评分检查“表填得对不对”，理由审计检查“是不是因为正确理解原文才填对”；这能识别标签碰巧正确但对象、立场或类别判断错误的情况。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 基准样本与六字段参考记录

$$
z_i=(t_i,\tau_i,\epsilon_i,s_i,y_i,c_i),\qquad \mathcal{D}=\left\{(x_i,z_i,r_i)\right\}_{i=1}^{N}
$$

**符号说明**

- $i$：样本索引。
- $N$：基准数据集中的样本总数。
- $x_i$：第$i$条待审核中文输入文本。
- $z_i$：第$i$条文本的六字段参考审核记录。
- $t_i$：主要审核命题的目标对象，即最短且稳定的相关指称。
- $\tau_i$：目标的指称范围类型，包括单一对象、群体对象或无明确对象。
- $\epsilon_i$：目标显式性，表示对象是直接表达、由语境推断，还是不存在明确对象。
- $s_i$：作者相对于相关辱虐命题的立场。
- $y_i$：有害性标签，取有害或无害。
- $c_i$：审核决定的主要细粒度类别。
- $r_i$：解释参考记录各字段决定的字段锚定自然语言思维链。
- $\mathcal{D}$：由$N$个输入、参考记录和参考推理三元组组成的基准数据集。

<div class="equation-explanation" markdown="1">

**直观理解**：该定义明确了基准的监督与评测单位：每条文本不仅对应一个最终标签，还对应五个补充判断和一段解释。六字段共同描述审核结论的逻辑结构，使评测能够发现“标签正确但目标、立场或类别错误”的样本。<br>
**原文位置**：Preliminaries，Task Definition，公式（1）和（2）

</div>

</div>

<div class="equation-block" markdown="1">

#### 锚点推理生成与结构化记录恢复

$$
\hat r_i=f_\theta(x_i),\qquad \hat z_i=\mathcal{P}(\hat r_i)=(\hat t_i,\hat\tau_i,\hat\epsilon_i,\hat s_i,\hat y_i,\hat c_i)
$$

**符号说明**

- $f_\theta$：参数为$\theta$的待评测生成模型。
- $\theta$：生成模型的参数；节选未说明其具体训练或优化方式。
- $\hat r_i$：模型根据$x_i$生成的单一自然语言审核思维链。
- $\mathcal{P}$：依据六个固定锚点抽取字段值的确定性解析器。
- $\hat z_i$：从$\hat r_i$重建的六字段预测审核记录。
- $\hat t_i$：预测的目标对象。
- $\hat\tau_i$：预测的目标类型。
- $\hat\epsilon_i$：预测的目标显式性。
- $\hat s_i$：预测的作者立场。
- $\hat y_i$：预测的有害性标签。
- $\hat c_i$：预测的细粒度类别。

<div class="equation-explanation" markdown="1">

**直观理解**：第一步让模型把审核判断和理由写进同一段带锚点的文本，第二步用固定规则把六项判断读回结构化记录。该设计的核心约束是“只生成一份答案”：自动评分所用字段必须来自被审计的那段解释，不能由另一条独立输出提供。<br>
**原文位置**：Preliminaries，Task Definition，公式（3）和（4）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用或原文节选未明确报告。所给章节定义的是基准任务、输出协议和评测接口，没有给出用于训练$f_\theta$的损失函数、优化器或参数更新规则，因此不能据此声称模型通过某种字段损失、语言建模损失或联合目标进行训练。公式$\hat r_i=f_\theta(x_i)$只规定模型在给定$x_i$时应生成什么形式的结果；$\hat z_i=\mathcal P(\hat r_i)$是确定性后处理，也不构成可微训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 六字段审核记录**

记录$z_i$包含六个相互关联的字段：$t_i$是主要审核命题中最短且稳定的指称对象，可为规范化自由文本或“no clear target”；$\tau_i$区分单一对象、群体对象和无明确对象；$\epsilon_i$区分显式、隐式和无明确对象；$s_i$区分攻击或赞同、反对攻击、引用或报道、中性提及；$y_i$区分有害与无害；$c_i$在一般辱虐、地域或族群、性别、性取向与性别认同、身份或职业、身体或健康、非攻击中选择主要依据，且所有无害样本统一使用非攻击类别。目标字段排除偶然出现的实体，同一命题中的并列指称合并为一个目标；对于被引用或遭作者反对的辱虐，目标仍是嵌入式辱虐命题所指的对象。

> 直观理解：这些字段把容易混淆的问题拆开：文本提到了谁，不等于作者正在攻击谁；出现辱虐说法，也不等于作者赞同它。只有先分清对象、指称方式和作者立场，最终的有害性及类别才具有可检查的依据。

**2. 字段锚定的自然语言思维链**

生成结果$\hat r_i$必须包含顺序固定的六个锚点，其中$\texttt{[T:]}$、$\texttt{[TY:]}$、$\texttt{[TT:]}$、$\texttt{[S:]}$、$\texttt{[L:]}$和$\texttt{[C:]}$分别承载目标、目标类型、目标显式性、立场、标签和类别。锚点之间的自由文本必须把输入中的具体证据与字段决定连接起来；仅罗列或换言复述字段值虽然可能满足格式，却不满足论文提出的理由要求。

> 直观理解：固定锚点保证不同模型的答案能被统一读取，自由文本则让模型说明证据和推断。二者结合，避免纯自由解释难以稳定抽取，也避免纯字段元组只有结论、没有语境依据。

**3. 确定性解析器与双层评测接口**

解析器$\mathcal P$不推测模型隐含意图，而是按照显式锚点从$\hat r_i$抽取字段并生成$\hat z_i$，从而支持字段级与六字段联合一致性评分；未被字段抽取消费的周边解释仍被保留，用于检查依据是否落在输入文本上、语境理解是否正确及推断是否足够。该框架所验证的是模型公开输出的操作性一致性，不声称验证模型内部推理轨迹。

> 直观理解：同一输出被分成两种用途：格式明确的部分交给程序打分，解释部分交给审计。这样既有可重复的自动评价，也不会把一个正确的最终标签误当成整个分析过程都正确。

**训练与推理**

训练流程在所给节选中未明确报告，包括是否使用$r_i$进行监督微调、如何划分数据以及如何提示模型，均不能从当前材料确定。可确认的推理流程是：向模型$f_\theta$仅提供$x_i$；模型生成一段按六锚点顺序组织的$\hat r_i$；$\mathcal P$从中抽取六项值形成$\hat z_i$；随后将$\hat z_i$与$z_i$进行字段级和联合比较，并保留$\hat r_i$以审计证据落地、语境理解和推断充分性。实际作答还需遵守字段语义，例如无害样本的$c_i$必须为“non-attack”，被引用或被反对的辱虐仍以嵌入命题的指称对象作为$t_i$，而作者是否实施或赞同辱虐则由$s_i$和$y_i$共同反映。

**复现信息**

公平复现所必需的接口约束包括：六个锚点必须存在且顺序固定；$t_i$允许规范化自由文本或“no clear target”，其余字段只能取章节列出的有限值；所有无害预测应配套“non-attack”类别；解析器必须直接处理同一段$\hat r_i$，不能接受模型另行输出的字段元组；锚点周围的自然语言必须保留，以免结构抽取后丢失理由审计材料。目标选择还应执行正文给出的规则：采用主决策命题中最短稳定的指称，排除偶然实体，合并同一命题下的并列对象，并在引用或反对辱虐时保留嵌入命题的目标。更细的冲突消解规则据称位于附录，但当前节选未提供；模型架构、解码参数、解析失败处理、提示模板、训练配置及具体评分实现也均为原文未明确报告，复现时需要回查完整论文。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- VARM-Bench 共含 8,000 条中文帖子或评论，来源为 Bilibili、知乎、百度贴吧和虎扑，按 5,600/800/1,600 划分为训练集、开发集和测试集，各划分保持 55/45 的有害—无害比例。训练集和开发集仅用于 CoT-SFT 适配与早停，所有系统最终在同一去重测试集上评估。数据包含六类有害内容以及 non-attack 类，并特意纳入引用辱骂、反对辱骂、中性身份提及等 1,440 条困难无害样本。
- 词汇线索挑战子集从测试集中构造，覆盖四组语义现象：人口身份、社会地位或角色、身体健康或残障、一般辱骂。每个子集约 100–200 条，按约 60:40 配置有害与无害样本，用于检验模型究竟理解作者立场和语境，还是仅被显著攻击词触发。
- CoT 人工审核样本由 300 个不放回随机抽取的共享测试输入组成；每个输入分别取得 Qwen2.5-7B CoT-SFT 与 DeepSeek-V4-Pro 零样本输出，共 600 条推理说明。该样本不测试分类分数，而测试解释能否支持实际人工复核。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**字段级 Macro-F1 与目标 T-F1**

五个离散字段使用 Macro-F1，使各类别获得同等权重；自由文本目标使用归一化字符重叠 F1，即 T-F1，以容忍部分边界重合。不可解析输出仍保留在分母中并记零，因此指标覆盖完整端到端流程。 （越高越好；高分分别表示离散字段分类更可靠，或预测目标与参考目标的字符范围更接近。）

</div>
<div class="metric-item" markdown="1">

**JREM**

完整记录联合精确匹配率。仅当输出可解析、目标 T-F1 不低于 $0.5$，且其余五个字段全部与冻结参考一致时，该样本才计为正确。它比标签分数更严格，用于判断一条审核记录能否作为整体被接受。 （越高越好；提高表示更多样本同时满足格式、目标定位和全部结构化决策，但不等于所有语义合理的替代表述都被接受。）

</div>
<div class="metric-item" markdown="1">

**HER-C 与 HER-L**

隐藏错误率，分别考察类别预测正确或有害标签预测正确的输出中，仍未达到完整记录正确标准的比例。解析失败会降低 JREM，但不进入 HER-C/HER-L 的分母。 （越低越好；较低值说明表面正确的类别或标签较少掩盖目标、显式性、立场等字段错误。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 高标签性能与完整记录质量的差距

<div class="result-value" markdown="1">

GPT-5.5 的标签 Macro-F1 为 97.6%，类别 Macro-F1 为 85.7%，但 JREM 仅为 55.4%，HER-C 为 38.1%。这直接表明，最终标签或类别正确并不能保证目标、目标属性和作者立场等字段共同正确。

</div>

作者据此主张传统标签级评估会高估结构化审核记录的可用性。分析上，这一结果支持使用联合指标，但 JREM 依赖单一冻结参考和目标 T-F1 阈值，因此 44.6% 的非联合匹配不能全部解释为无争议的语义错误。

<div class="result-source" markdown="1">

来源：Experiments, Main Results, Q1；Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 1 shows that GPT-5.5 achieves Label and Category Macro-F1 scores of 97.6% and 85.7%, but its JREM is only 55.4%; 38.1% of its category-correct outputs still contain a record error.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 显著词汇线索下的有害与无害语境

<div class="result-value" markdown="1">

四类挑战子集的 24 个“模型—子集”比较中，有害样本的 JREM 均高于无害样本，中位差距为 26.0 个百分点；一般辱骂线索的平均差距最大，为 38.1 个百分点。CoT-SFT 与 API 零样本系统在有害样本上的平均 JREM 接近，分别为 67.5% 和 66.4%，但在无害样本上分别为 45.8% 和 35.3%。

</div>

结果说明模型更容易在攻击词确实表达作者攻击时形成正确记录，而在引用、反驳或中性提及时容易把词面攻击性误当成作者立场。CoT-SFT 的主要优势集中于困难无害语境，但这些是按线索筛选的挑战子集，不能单独证明其对所有自然分布无害文本都有同等幅度的提升。

<div class="result-source" markdown="1">

来源：Experiments, Main Results, Q2；Figure 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

CoT-SFT and zero-shot API systems perform similarly on harmful cases, averaging 67.5% and 66.4% JREM, respectively. Their non-harmful JREM differs more clearly, reaching 45.8% for CoT-SFT and 35.3% for the API systems.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 完整记录的主要错误瓶颈与 CoT 可审核性

<div class="result-value" markdown="1">

字段分析显示所有系统中目标定位的失配率最高，其次是目标显式性；Shapley 分解将 Parse Success 与 JREM 之间差距的 76.6%–80.6% 归因于 Referent 组。另在 600 条 CoT 审核中，Qwen2.5-7B CoT-SFT 的 Groundedness、Adequacy、Coherence 分别为 91.3%、99.7%、99.7%，DeepSeek-V4-Pro 零样本则为 98.7%、22.8%、100.0%。

</div>

联合来看，系统最需要改进的不是输出格式，而是确定“攻击针对谁”并围绕该对象形成具体解释。零样本解释即使有依据且内部一致，也可能只是复述字段而缺乏样本特定理由；CoT-SFT 显著改善充分性，但其 groundedness 略低，且自动评审后仍需人工把关。这些审核分数衡量解释质量，不证明推理文本忠实呈现模型内部因果过程。

<div class="result-source" markdown="1">

来源：Experiments, Main Results, Q3–Q4；Figures 5 and 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

CoT-SFT obtains 91.3%, 99.7%, and 99.7% on the three dimensions, whereas Zero-Shot obtains 98.7%, 22.8%, and 100.0% (Figure 7).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- JREM 采用冻结单一参考记录，并要求目标 T-F1 至少为 $0.5$、其余五字段完全一致。论文的复标结果中 Target Explicitness 的 Krippendorff's $\alpha$ 为 0.671，目标字符 F1 一致性为 0.775，说明部分“错误”可能是合理的目标规范化或显式性分歧，而非明确的语义失败。
- 主要比较并非完全受控：CoT-SFT 同时改变训练方式、引入 5,600 条监督样本并监督解释，API 模型的规模和训练数据也不透明。因此结果可以支持“该配置在本基准上更有效”，但不能单独确定收益来自 CoT、结构字段监督、LoRA，或模型预训练差异。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 开放模型零样本：Qwen2.5-7B、Llama-3.1-8B 和 InternLM3-8B 直接按统一六锚点输出协议作答，用来衡量模型未经任务适配时的结构化审核能力。
- 分类体系引导零样本（+Taxonomy）：向上述三个开放模型补充任务分类体系，但不进行参数训练。它与普通零样本的比较用于隔离“提供明确标签定义和边界”本身的作用。
- CoT-SFT：对上述三个开放模型使用 5,600 条训练记录和 800 条开发记录进行带提示屏蔽的 LoRA 微调，同时监督六个结构化字段及连接它们的解释文本。与 +Taxonomy 相比，它检验样例级结构监督是否优于仅给规则。
- 闭源或 API 零样本系统：GPT-5.5、Qwen3.7-Max 和 DeepSeek-V4-Pro 在相同输入、解析器和指标下评估，作为高能力通用模型参照；由于模型规模、训练数据和接口条件并未对齐，该比较反映实际系统表现，不是严格的同规模架构对照。

**实验想回答的问题**

- 在相同测试集与输出约束下，标签或类别预测正确是否仍会掩盖目标、目标属性、作者立场等结构化字段的错误；不同提示或监督方式能否提高完整记录的联合正确率？
- 模型的完整记录错误主要来自哪些环节，尤其是显著辱骂词在引用、反驳和中性提及时是否会诱发误判；生成的推理说明是否足够有依据、具体且一致，因而可作为人工审核草稿？

**实验实现**

所有模型共享去重后的 1,600 条测试数据、六锚点输出契约、目标归一化规则、解析器和指标；测试集不参与适配或模型选择。CoT-SFT 使用提示部分不计损失的 LoRA，并按开发集损失早停，直接监督六个锚点及其连接文本。推理采用确定性解码，每个表格结果均从冻结的全测试集输出重新计算，不人工修复解析或字段错误。数据划分前实施 Unicode NFKC 规范化和去重，RapidFuzz 相似度达到 95% 的文本对被限制在同一划分，以降低泄漏风险。CoT 审核对每条解释执行三次盲化 GPT-5.5 评审，再由人工复查失败项、非一致项以及抽样的一致项。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 普通零样本 → +Taxonomy | 对三个开放模型，加入分类体系后类别 Macro-F1 提高 7.2–13.0 个百分点，但 HER-C 仍处于 51.7%–79.8%。例如 Qwen2.5-7B 的类别 Macro-F1 从 63.7% 升至 76.7%，JREM 仅从 31.9% 升至 36.4%，HER-C 基本不变，为 54.9% 对 54.8%。 | 该对照主要隔离显式任务定义和类别边界的作用。它能明显帮助模型选对类别，却没有同步解决目标、显式性或立场等联合字段，因此“知道分类体系”不足以生成可靠的完整记录。由于提示文本长度和内容也随条件变化，这不是对单一语义组件的参数级消融。 | Experiments, Main Results, Q1；Table 1<br><span class="experiment-evidence">For the three open models, taxonomy guidance raises Category Macro-F1 by 7.2–13.0 points, while HER-C remains at 51.7–79.8%.</span> |
| +Taxonomy/零样本 → CoT-SFT | 三个开放模型经 CoT-SFT 后，JREM 均达到 56.0%–59.5%，HER-C 降至 34.4%–37.2%，Parse Success 达到 99.3%–99.8%。以 InternLM3-8B 为例，JREM 从 +Taxonomy 的 12.7% 升至 59.5%，HER-C 从 79.8% 降至 34.5%。 | 该比较表明，样例级六字段与解释联合监督比仅提供体系规则更能改善整条记录，并基本消除格式解析问题。不过 CoT-SFT 同时引入训练数据、LoRA 参数更新和解释监督，无法进一步区分收益来自结构化字段监督、CoT 文本，还是一般的任务微调。 | Experiments, Main Results, Q1；Table 1<br><span class="experiment-evidence">CoT-SFT improves the complete record more consistently, raising JREM to 56.0–59.5% and lowering HER-C to 34.4–37.2%.</span> |

**定性案例**

- Figure 6 的 Case B 包含一条被作者引用后明确反对的地域刻板印象。只抽取攻击词或目标的表示可能把嵌入引语误当成作者本人立场，从而给出有害判断；VARM-Bench 则保留被引用群体为目标，同时记录作者持反对立场、文本无害且无有害类别。该案例说明目标抽取本身不能处理“谁说了什么、作者是否认同”的话语功能，必须联合建模目标、立场和最终决策；但单个案例只用于解释错误机制，不能估计该机制在总体数据中的频率。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出评测中文辱骂言论审核中可验证结构化推理能力的基准，兼具推理评测与任务验证重点。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`e48a7da9f00567da4f996810078d615c0e31acb66c84668b048b68fbf909770a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
