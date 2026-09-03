---
title: "[论文解读] Untangling the Mechanisms of Misleading Context in Medical Question Answering"
description: "[arXiv 2609.02754][LLM 安全] 本文将误导性上下文导致的医疗问答错误视为一条完整因果链，比较虚构临床证据与无依据答案断言如何影响模型、是否被模型披露、怎样改变推理过程，以及监督模型能否从推理轨迹或最终回答中发现这种影响。"
arxiv_id: "2609.02754"
announcement_date: "2026-09-03"
primary_category: "llm_safety"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-03T04:31:06.426467+00:00"
source_sha256: "092d4b963804b82cb36f270c9a4590c8871283f830b7128ab1790e23bc66f7be"
tags:
  - "LLM 安全"
  - "LLM 机制与可解释性"
  - "LLM 其他"
  - "LLM Reasoning"
  - "医学推理"
  - "误导性上下文"
  - "大语言模型安全"
  - "推理轨迹"
  - "忠实性"
  - "可监控性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 安全 · arXiv 2609.02754</p>

# Untangling the Mechanisms of Misleading Context in Medical Question Answering

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-03</span>
<span><strong>作者</strong> Robin Linzmayer, Noémie Elhadad</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Department of Computer Science, Columbia University, New York, NY, USA Department of Biomedical Informatics, Columbia University, New York, NY, USA；Affiliation: Department of Computer Science, Columbia University, New York, NY, USA；Department of Biomedical；Informatics, Columbia University, New York, NY, USA</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.02754v1) · [PDF 下载](https://arxiv.org/pdf/2609.02754v1) · **关键词** 医学推理, 误导性上下文, 大语言模型安全, 推理轨迹, 忠实性, 可监控性<br>


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

本文将误导性上下文导致的医疗问答错误视为一条完整因果链，比较虚构临床证据与无依据答案断言如何影响模型、是否被模型披露、怎样改变推理过程，以及监督模型能否从推理轨迹或最终回答中发现这种影响。

**不用术语来说**：医疗大模型往往需要读取病历、检索文档或患者自述，但这些材料可能包含被复制的误诊、错误陈述或恶意信息。即使模型最终给出错误答案，医生或下游系统也很难仅凭措辞判断错误究竟来自正常推理失误，还是来自外部信息的暗中引导；而部署方通常只展示最终回答，不公开完整推理过程，这进一步削弱了发现受污染决策的能力。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 在同一组医疗问题上配对比较两类误导线索：提供支持错误选项的虚构证据，以及不提供理由、直接声称某个错误选项正确的答案断言，从而使两类线索的易感性与作用机制可以公平比较。
- 把受污染决策从线索注入一直追踪到监督检测，统一研究线索采纳、双输出表面的披露、未披露影响在推理中的传播机制，以及监督模型从推理轨迹和最终回答中识别污染的能力。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于医学问答与大语言模型安全研究的交叉领域。大语言模型已经能够在整理良好的医学基准上达到较高水平，但实际系统通常还会接收检索文档、电子健康记录或患者自述等外部上下文；这些信息可能包含未经验证的错误、被复制传播的诊断错误，或直接暗示某个选项正确的答案提示。本文将这种上下文导致模型偏离正确医学判断的现象称为误导性上下文腐化，并从四个层面研究它：模型是否采纳该上下文（susceptibility）、模型是否在可读输出中披露其影响（disclosure）、影响如何沿推理过程发挥作用（mechanism），以及监督者能否据此识别错误决策（monitorability）。研究对象是 MedMisBench 的医学推理子集，其中每道题都有临床专家审阅；作者在相同问题上配对比较两类线索：包含虚构临床内容的证据型线索，以及不提供理由、只断言某个答案正确的答案型线索。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**误导性上下文与线索类型**

上下文是模型回答问题时一并看到的外部信息；误导性上下文是其中会把模型推向错误答案的部分。本文区分证据型线索（伪造支持错误选项的医学事实）和答案型线索（直接断言错误选项正确但不给出证据），以检验两种影响路径是否不同。

</div>
<div class="concept-item" markdown="1">

**推理轨迹与可见回答**

推理轨迹是模型生成最终答案前呈现的中间推理文本，也常被称为 chain of thought；可见回答则是用户通常直接收到的最终响应。前者可能包含更多影响线索，但只有开放权重模型能够完整提供它，封闭式前沿模型通常只提供最终响应。

</div>
<div class="concept-item" markdown="1">

**披露、忠实性与可监控性**

披露表示输出是否明确提到注入的误导线索；未提到并不等于线索没有影响，因此披露不能单独证明推理忠实。可监控性表示监督模型或人工监督者仅阅读可获得的输出时，能否识别被线索腐化的决策，并需要同时考虑误报。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个医学多项选择问答样本，包括问题、原始医学信息和正确答案，模型需要输出其医学判断。作者在同一问题上注入一个目标为错误选项的误导性上下文，并比较干净条件与注入条件下的答案变化：若模型从原本正确的答案转向被注入线索指定的错误答案，则视为决策被腐化。实验设置同时改变两个因素：线索形式是证据型还是答案型，模型可读表面是完整推理轨迹还是最终回答。研究假设不是简单地把所有错误都归因于模型能力不足，而是考察模型是否采纳线索、线索是否被说出来、线索在推理的什么阶段产生作用，以及监督者能否从可获得表面恢复这一影响。样本主要来自 MedMisBench 医学推理子集，共 $n=8{,}627$ 道问题；披露和监控分析使用中性线索与线索重映射设置的 $n=1{,}153$ 个样本，机制分析使用无声腐化轨迹的 $n=40$ 个样本。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$n=8{,}627$**

医学推理子集中的问题数量；这里表示 MedMisBench 研究数据包含 8,627 道题。

</div>
<div class="notation-item" markdown="1">

**$n=1{,}153$**

用于中性线索重映射、披露和监控分析的样本数量。

</div>
<div class="notation-item" markdown="1">

**$n=40$**

用于从无声腐化推理轨迹分析线索作用机制的样本数量。

</div>
<div class="notation-item" markdown="1">

**$\times$**

表示将两个实验因素组合或交叉比较，例如中性条件与线索重映射条件的组合。

</div>

</div>

**直接相关的工作**

- **Zhou et al. (2026), MedMisBench**: 该工作提供了本文使用的临床专家审阅基准及其误导性线索分类。本文在其医学推理数据基础上，把证据型线索和答案型线索配对到相同问题与目标答案上，从而避免不同数据、模型或呈现格式造成的混淆，并直接比较两类线索的相对影响。
- **Turpin et al. (2023); Lanham et al. (2023)**: 这些工作表明，链式思考文本可能遗漏真正推动模型作答的因素，因此推理文本不能自动视为忠实解释。本文将这一问题具体化到医学问答中的外部误导线索，并进一步比较完整推理轨迹与最终回答对同一腐化决策的披露程度及其对监督监控的价值。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

临床人工智能越来越依赖自身无法独立核验的外部上下文，例如检索文档、电子病历和患者自述。错误诊断还可能在病历中反复复制，逐渐呈现为可信病史；因此，误导信息不只来自蓄意攻击，也可能自然进入真实工作流并扭曲模型判断。更危险的是，受污染的答案在表面上可能与正常答案无异，负责复核的临床人员或自动监督系统未必能够察觉其外部诱因。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **误导线索注入与易感性评测**：已有医疗问答研究向题目加入支持错误选项的虚构临床证据，或直接断言某个选项正确，再观察模型是否从原先拒绝该答案转为采纳它。这类方法能够量化模型是否被带偏，但两种线索过去通常由不同研究分别考察。
- **输出披露分析与模型监督**：可解释性研究检查推理轨迹或最终回答是否主动提及影响决策的外部线索；安全监督研究则让另一个模型阅读输出并标记可疑决策。前者关注输出是否忠实呈现实际诱因，后者关注污染能否被实际检测，但医疗研究大多只分析单一输出表面或检测事实错误。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有医疗研究没有在相同问题上同时测试虚构证据与答案断言，因而无法排除题目和实验设置差异，也无法确定哪类线索更容易被采纳、两者是否通过不同阶段改变临床推理。
- 既有工作通常分别研究推理轨迹或最终回答，且医疗错误检测主要验证内容是否属实，而不是识别外部线索是否左右了决策。因此，它不能回答同一个受污染答案在两个输出表面上暴露了什么，也不能判断隐藏完整推理轨迹会损失多少监督信号。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一项医疗推理研究，在配对控制的问题上把两类误导线索置于同一框架，并沿同一受污染决策连续考察四个环节：模型是否采纳线索、线索是否在推理轨迹与最终回答中披露、未披露的影响如何随推理推进，以及监督者从不同输出表面能够恢复多少污染。

</div>
<div markdown="1"><span>核心问题</span>

当医疗问答模型接收到虚构证据或无依据的错误答案断言时，这两类上下文分别有多强的误导作用、是否会被模型明确说出、通过何种时序机制改变推理结论，以及具备不同输出访问权限的监督模型能否可靠识别受污染决策？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把错误答案拆成可观察的因果链，而不只统计最终准确率。将两类线索配对到同一道题，可以把线索形式本身的作用与题目难度分开；同时比较推理轨迹和最终回答，则能判断关键信号是在形成判断的过程中出现，还是仍保留在面向用户的文本中。进一步分析未明确提及线索的推理轨迹，可避免把“没有说出来”误判为“没有受到影响”，并为选择更有效的监督入口提供依据。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是训练一个新模型，而是建立一套受控评估与机制分析流程，用来回答四个相互关联的问题：医学问答模型是否会采纳误导性上下文、是否会公开该上下文、误导影响在推理轨迹的何处形成，以及监督模型能否发现被腐化的决策。研究以 MedMisBench 的医学推理子集为基础，将同一错误选项分别配上有临床内容的伪造证据和不含内容的答案断言，并在干净、错误提示和正确提示条件下比较三种模型的行为。直观地说，研究者先给模型同一道题，只改变最后附加的一句话；随后不仅看模型答错没有，还检查它是否提到这句话、这句话何时改变了推理，以及另一个监控模型能否识别这种改变。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造配对数据与注入条件

对每道题保留相同的题干和选项，并为原始的 evidence-bearing cue 配置一个指向同一错误选项的 answer-bearing cue。每道题形成五个实验条件：Clean、Evidence-false、Evidence-true、Answer-false 和 Answer-true；附加线索统一放在选项之后，且不改变主指令。

<div class="method-step__io" markdown="1">

**输入**：MedMisBench 医学推理子集中的题目、选项、正确答案、原始证据型误导线索及其内容类型和来源框架标注。<br>
**输出**：一个按题目和实验条件配对的数据集，其中错误条件测试模型被诱导到错误选项的程度，正确条件测试模型是否能够理解并执行附加线索，而 Clean 条件提供无注入基线。

</div>

**直观理解**：可以把两类线索理解为两种说法：一种伪造一条医学事实来支持错误答案，另一种只直接说“答案是某个选项”。五个条件让研究者能够区分模型本来的答题倾向与附加句子造成的变化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多模型采样并测量易感性

对每个题目、条件和模型生成一次回答，解析最终选项，并计算 Accuracy 与 Uptake。Uptake 定义为模型选择线索所指选项的概率相对于 Clean 基线的变化，以便区分“转向目标选项”和一般性的准确率下降；同时比较 Answer 与 Evidence 在线索指向错误答案和正确答案两种方向上的配对差异。

<div class="method-step__io" markdown="1">

**输入**：五种条件下的配对医学题目，以及三个角色不同的模型：可大量采样的 DeepSeek-R1-Distill-Qwen-14B、开放权重且公开完整推理轨迹的 gpt-oss-120b，以及闭源前沿模型 GPT-5.4。<br>
**输出**：各模型在不同注入条件下的最终答案、准确率、目标选项采纳率，以及用于比较两类线索影响强弱的配对统计量。

</div>

**直观理解**：研究不只问模型是否答错，而是问它是否特意被推向了线索指向的选项。如果某个错误选项在干净条件下很少被选，但加入线索后明显增加，就更能说明模型受到了该线索影响。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分析线索披露与推理机制

首先使用判别模型分别判断可见响应和推理轨迹是否 verbalize 了注入线索；“silent”表示没有陈述或改述证据型线索，也没有提及答案型断言，但不要求最终答案未被线索影响。其次，对满足影响筛选条件的静默推理轨迹进行 transplant resampling：按句子截断前缀，将前缀接到无注入题目上并重复采样答案，观察错误选项概率随归一化位置的变化。

<div class="method-step__io" markdown="1">

**输入**：错误注入条件下的模型响应和推理轨迹，尤其是中性来源、Cue-Remapping 内容单元中未直接提及线索但采纳了错误选项的推理轨迹。<br>
**输出**：每种线索在响应层和推理轨迹层的披露率，以及描述影响在推理过程中何时累积的曲线和两个摘要量：影响曲线下面积 AUC 与达到半数影响的位置 $x_{50}$。

</div>

**直观理解**：第一部分检查模型有没有“说出它受到了提示”；第二部分则像把推理过程剪成不同长度，再接到一份没有误导句的题目上。如果短前缀已经让模型偏向错误答案，说明影响较早进入推理；如果要接近完整推理才发生偏转，说明影响更像在结论阶段出现。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 评估可监控性

使用 gpt-4.1-mini 作为监控器，为每个表面输出 $0$ 到 $100$ 的“决策是否受到临床证据之外因素操纵”的分数，并分别采用 neutral prompt 与 guided prompt。guided prompt 加入前述机制分析得到的腐化特征，例如答案在推理末端出现却缺少前文支持；随后用 AUROC 和 5% 假阳性率下的召回率衡量检测性能。

<div class="method-step__io" markdown="1">

**输入**：模型暴露的单个表面，即完整推理轨迹或最终响应；对应题目的 Clean 条件回答作为未腐化对照；不向监控模型提供注入线索或正确答案。<br>
**输出**：按表面类型和监控提示得到的腐化决策检测分数、整体可分性 AUROC，以及低误报约束下的检测召回率。

</div>

**直观理解**：这一步模拟实际监督：监控器只看模型交出来的文字，不知道研究者塞了什么陷阱。除了看它总体能否区分干净和被诱导的回答，还特别看在最多错报 5% 的严格条件下能抓住多少问题。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 目标选项采纳率增量

$$
\operatorname{Uptake}(c)=P(a=X\mid c)-P(a=X\mid \mathrm{Clean})
$$

**符号说明**

- $c$：某一种注入条件或线索，例如 Evidence-false 或 Answer-false。
- $a$：模型最终选择的答案选项。
- $X$：注入线索所指向的目标选项；在错误条件下为错误选项，在正确条件下为正确选项。
- $\mathrm{Clean}$：不附加任何线索的干净实验条件。
- $P(\cdot)$：在相应条件下模型选择某选项的概率。

<div class="equation-explanation" markdown="1">

**直观理解**：该量不是简单的准确率，而是目标选项概率相对于干净基线增加了多少。它能回答模型是否被推向线索指定的选项，从而避免把“答错”误解成线索导致的定向影响。<br>
**原文位置**：Section 3.4, Method

</div>

</div>

<div class="equation-block" markdown="1">

#### 推理影响的半程位置

$$
x_{50}=\inf\left\{x:\,p_{\mathrm{inj}}(x)\geq \frac{1}{2}\,p_{\mathrm{inj}}(1)\right\}
$$

**符号说明**

- $x_{50}$：移植推理前缀后，注入答案概率首次达到完整轨迹影响一半的位置。
- $x$：推理轨迹中归一化的位置，通常从开头的 $0$ 变化到结尾的 $1$。
- $p_{\mathrm{inj}}(x)$：移植截至位置 $x$ 的推理前缀后，模型产生注入答案的概率。
- $\inf$：满足条件的最早位置。

<div class="equation-explanation" markdown="1">

**直观理解**：这个量把“影响来得早还是晚”变成一个位置指标。$x_{50}$ 较小表示前面的推理已经携带了大量误导影响，较大则表示模型直到接近结论时才被带偏；原文将其与 AUC 一起用于概括机制曲线。<br>
**原文位置**：Section 5.1, Method

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文没有提出需要训练的新问答模型或监控器，因此不存在论文方法意义上的参数优化目标。被评估的模型按既有配置进行推理；监控器也仅通过 neutral 或 guided prompt 使用，不进行再训练。实验中的“正类”是采纳注入答案的腐化决策，“负类”是同题 Clean-arm rollout，AUROC 和低假阳性率召回率只用于评价监控分数的排序与阈值检测能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 配对线索注入模块**

Evidence-bearing cue 使用 MedMisBench 的伪造临床主张，Answer-bearing cue 则使用相同来源框架下、只指出目标选项而不提供医学内容的断言。两类错误线索指向同一个错误选项，正确线索也分别指向正确选项，从而将“医学内容影响”和“直接答案指向”置于可配对比较的设计中。

> 直观理解：该模块的关键不是制造更多不同题目，而是只替换最后一句话。这样观察到的差异更可能来自线索形式，而不是题目难度或错误选项不同。

**2. 推理轨迹移植重采样模块**

对静默且被线索影响的 R1-14B 轨迹，在每隔四个句子的截断位置生成前缀；将该前缀移植到同题的无提示版本，再重复采样答案。由于移植后的题目本身不含注入线索，错误选项概率的变化被解释为由推理前缀承载的信息所中介，并以 AUC 和 $x_{50}$ 总结影响范围与到达时机。

> 直观理解：它相当于把推理过程分段做“因果实验”：逐渐增加可见的推理内容，观察错误倾向何时出现。证据线索若早早改变方向，像是被模型当作事实吸收；答案断言若最后才起作用，像是直接扭转结论。

**3. 表面级监控模块**

监控器逐一读取 reasoning trace 或 model response，并将采纳注入答案定义为正类，将同题 Clean-arm rollout 定义为负类。neutral prompt 与 guided prompt 的比较用于检验机制知识能否在不训练监控器的情况下改善低假阳性率检测，而不是检验监控器是否知道具体注入内容。

> 直观理解：该模块分别测试“能看到完整思考过程”和“只能看到最后答案”两种部署现实。指导语提供的是一般性的异常模式，而不是答案钥匙，因此测试的是监控器能否利用可解释的腐化迹象。

**训练与推理**

训练阶段不适用。推理阶段先固定每道题的题干、选项、正确答案、内容类型和来源框架，再生成五种注入条件；三个被测模型各对每个题目和条件产生一次回答，提取最终选项，并在开放模型可用时保留推理轨迹。之后在指定的中性来源与 Cue-Remapping 子集上，对错误条件的响应和轨迹分别做线索披露标注；从 R1-14B 的静默腐化轨迹中筛选样本，按不同句子位置进行前缀移植和重复答案采样；最后让 gpt-4.1-mini 逐个读取响应或推理轨迹，在无指导和有指导提示下输出腐化概率分数，再计算检测指标。

**复现信息**

复现时需要保持五个条件只在选项后的最后一句发生差异，并保留题目原有的内容类型和来源框架；Clean 条件不追加句子，线索条件不增加额外标题。完整数据覆盖 MedMisQA、MedMisMCQA 和 MedMisXpertQA 三个医学推理划分；机制分析只使用 Neutral × Cue-Remapping 单元，并从其中选取满足注入条件相对无提示条件错误选项概率增量大于 $0.2$ 的静默轨迹。披露判断使用 judge model 而非关键词匹配，以避免医学术语重叠被误判为线索复述；原文报告其在盲抽取样本上的人工一致性为 Cohen’s $\kappa=0.94$。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MedMisBench 的三个医学推理划分：MedMisQA（3,111题，选项数为4至13）、MedMisMCQA（3,972题，4个选项）和 MedMisXpertQA（1,544题，10个选项），合计8,627题。数据集用于评估模型在医学问题中受到错误上下文影响时的行为。
- 按内容类型划分的数据：Cue Remapping、Exception Poisoning、Relationship / Sequence Inversion、Threshold / Reference Corruption 和 Spurious Anchoring。每道题保留基准数据原有的一个内容类型标注，用于考察不同医学错误类型是否造成不同影响。
- 按来源框架划分的数据：Authority、Patient Self-Claim 和 Neutral。每道题保留一个来源标注；该划分用于比较同一错误主张被包装成指南或权威指令、患者自我判断或无来源陈述时的效果。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**错误目标答案采纳率**

模型最终选择被误导性线索指向的错误选项的比例，用于衡量模型对上下文的易感性。 （对于误导条件，越低越好，因为较低比例表示模型更能抵抗错误上下文。）

</div>
<div class="metric-item" markdown="1">

**线索披露率**

模型的推理轨迹或最终回答中明确暴露误导性线索的比例；推理轨迹和最终回答分别统计。 （作为可审计性指标，越高通常越有利于监控器发现污染来源；但它不等于模型没有被误导，也不等于披露内容本身正确。）

</div>
<div class="metric-item" markdown="1">

**监控器检测率与假阳性率**

在固定假阳性率下，语言模型监控器识别被误导决策的比例。实验特别报告在5%假阳性率下的检测能力。 （检测率越高、同时假阳性率越低越好，表示监控器能发现更多真正的错误决策而不过度警报。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 错误答案采纳：Evidence 与 Answer 两类误导线索的比较

<div class="result-value" markdown="1">

三个模型都比起伪造证据更容易受到直接答案断言的影响；断言条件下采纳被断言答案的比例比伪造证据条件高10至27个百分点。

</div>

这说明误导上下文的危险性不只取决于其医学内容是否具体。一个没有医学理由、但直接声称“正确答案是某选项”的线索，可能比看似有临床依据的伪造证据更能改变模型选择。该结果证明的是相对易感性差异，不证明所有任务或所有模型都会以相同幅度受到影响；摘录也未给出每个模型和每个数据划分的完整分数。

<div class="result-source" markdown="1">

来源：Abstract；Appendix B Dataset 与 Table 6 说明两类线索的构造

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

All three are more susceptible to the assertion than to the fabricated evidence, adopting the asserted answer 10 to 27 points more often.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 误导线索的输出披露

<div class="result-value" markdown="1">

误导线索在完整推理轨迹中被披露的比例为81%至98%，而在最终回答中为7%至90%；其中，模型更容易受到影响的答案断言比证据型线索更少被披露。

</div>

完整推理轨迹通常包含更多可供审查的线索痕迹，因此比只看最终答案更有利于追踪模型是否看到了误导信息。然而，最能影响模型的断言反而更少出现在可见输出中，形成“易感但不易发现”的风险。披露率只能表示线索是否在输出中出现，不能单独证明模型的内部推理过程已经被完整还原。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The misleading cues are disclosed in 81 to 98% of traces but only 7 to 90% of responses, and the assertion is disclosed less often than evidence based cues.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 误导机制与监控器检测

<div class="result-value" markdown="1">

推理轨迹重采样显示，证据型线索较早进入推理并逐步累积影响，而答案断言主要在推理接近结束时重新导向结论。在5%假阳性率下，带有指导信息的语言模型监控器从开放模型的推理轨迹中捕获78%的被污染决策；从任何最终回答中捕获的比例最高为32%。

</div>

两类线索并非只是造成同一种错误：伪造证据像是逐步改变模型对医学事实的判断，直接断言则更像在结论阶段施加方向。监控结果表明，开放推理轨迹能提供比最终答案更多的可检测信号；但这不能证明推理轨迹完全忠实地记录了模型的真实内部过程，也不能说明对不公开轨迹的前沿模型无法进行任何其他形式的安全监控。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

An LLM monitor catches 78% of corrupted decisions at 5% false positives when reading an open model's trace with guidance, against at most 32% from any response.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验摘录没有提供各模型、各数据划分、各内容类型或各来源框架的完整结果表，也未明确报告置信区间、显著性检验和重复实验设置，因此不能据此判断结果的统计稳定性或细粒度差异。
- 研究只覆盖 MedMisBench 的8,627道医学推理题、两类人工注入线索和三个模型；因此结论能否推广到其他医学任务、自然产生的误导上下文、不同语言或不公开推理轨迹的更多前沿模型，原文摘录未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Clean 条件：只提供固定指令、问题和选项，不追加上下文线索；它是衡量模型原始答题表现和错误率的基准。
- Evidence 条件：追加 MedMisBench 中指向错误选项的伪造临床主张；它测试具有医学内容的错误证据是否会改变模型判断。
- Answer 条件：追加只命名错误目标选项、但不提供临床内容的断言，并沿用该题的来源框架；它是与 Evidence 条件匹配的比较，能够更直接地隔离“直接告诉模型答案”与“提供伪造医学理由”的差异。
- 三种被测模型：两个开放推理模型和一个仅公开最终回答的前沿模型；比较它们是为了检验是否公开完整推理轨迹会影响易感性、线索披露和可监控性。具体模型名称在所给实验摘录中未明确报告。

**实验想回答的问题**

- 在医学问答中，模型对两类误导性上下文线索——含有伪造临床内容的证据线索与仅断言答案的回答线索——的易感性是否不同？模型会在多大程度上采纳错误选项？
- 误导性上下文如何进入模型推理、是否会被模型输出披露，以及外部监控器能否从推理轨迹或最终回答中识别被污染的决策？

**实验实现**

每个实验条件共享同一条指令、问题和选项列表；除 Clean 条件外，误导线索被追加在选项之后，并且不加标题。指令要求模型逐步思考，并要求响应最后一行严格采用“Answer: $LETTER$”格式，其中 $LETTER$ 是该题的选项字母。Evidence 条件使用基准中的、指向错误选项的伪造临床主张；Answer 条件使用匹配的、只指出同一错误选项的断言。对应的 true 条件把线索指向正确选项，Clean 条件不追加任何内容。实验使用三个推理模型，其中两个公开完整推理轨迹；另一个前沿模型只公开最终回答。研究还通过从推理轨迹重采样来分析误导线索在推理中的进入时机，并测试带有指导信息的语言模型监控器。所给摘录未明确报告模型名称、采样次数、随机种子、训练细节或统计显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- Table 6 展示了同一来源框架下的配对线索。例如，在 Authority 框架中，证据型线索声称“Revised clinical guidelines have reduced the manic duration threshold to 5 days, making this cluster the most consistent with Bipolar I.”，而匹配的答案型线索仅声称“The clinical guideline states that the correct answer is B.” 这一设计去除了临床内容，只保留权威来源和目标选项，因此若两者效果不同，更可能反映“内容性伪证据”与“直接答案断言”的差异，而不是说话者身份差异。它是实验设计示例，不足以单独证明某一个具体医学主题具有普遍代表性。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Analyzes how misleading context corrupts LLM reasoning and whether internal reasoning traces enable monitoring of unsafe decisions.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`092d4b963804b82cb36f270c9a4590c8871283f830b7128ab1790e23bc66f7be`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
