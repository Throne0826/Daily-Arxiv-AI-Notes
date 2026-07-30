---
title: "[论文解读] Position: Evaluation Scores Are Perishable Knowledge Claims"
description: "[arXiv 2607.26191][LLM 评测] 本文主张将语言模型评测分数视为具有证据强度、适用范围和有效期限的知识主张，并通过显式元数据与可调悲观程度的聚合方式抑制平均分造成的“信任膨胀”。"
arxiv_id: "2607.26191"
announcement_date: "2026-07-30"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:25.016416+00:00"
source_sha256: "6560492fd1c1d08bf66ad1d687c98bebfedaf6d048a5ad74fa504479a84ecec6"
tags:
  - "LLM 评测"
  - "语言模型评估"
  - "信任膨胀"
  - "知识主张"
  - "评估聚合"
  - "LLM-as-judge"
  - "基准污染"
  - "适用范围"
  - "有效期"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2607.26191</p>

# Position: Evaluation Scores Are Perishable Knowledge Claims

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Sankalp Gilda, Shlok Gilda</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26191v1) · [PDF 下载](https://arxiv.org/pdf/2607.26191v1) · **关键词** 语言模型评估, 信任膨胀, 知识主张, 评估聚合, LLM-as-judge, 基准污染, 适用范围, 有效期  


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

本文主张将语言模型评测分数视为具有证据强度、适用范围和有效期限的知识主张，并通过显式元数据与可调悲观程度的聚合方式抑制平均分造成的“信任膨胀”。

**不用术语来说**：当前评测常把自动指标、LLM裁判、人工评价和多个基准成绩合成一个平均分，但这些证据的可靠性、适用对象和产生时间并不相同。一个模型即使在多数项目上表现良好，也可能在关键项目上很差；平均值会掩盖这种短板。此外，旧基准可能因训练数据污染或任务分布变化而失效，但排行榜仍可能将其与新结果并列展示，使一个看似精确的分数传达出超出证据实际支持程度的信心。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出“评测中的信任膨胀”这一统一问题表述：平均聚合可能让总体结论的可信度超过其中最弱评测信号的可靠性，并将提示敏感性、不可复现、基准污染和LLM裁判偏差解释为评测知识主张所依赖假设未被显式表达的不同表现。
- 作者提出为评测结果附加三类元数据——形式化等级、适用范围声明和有效期限——并以最弱环节聚合及其可调悲观程度的算子族作为理论入口；同时明确该方案是立场性框架，尚缺少大规模实证验证。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文讨论语言模型评估的可信度问题。当前评估通常同时使用自动指标、LLM-as-judge 评分、人工评价和多个基准测试，并通过平均值等方式汇总为单一分数或排名。然而，各类证据的可靠性并不相同：提示格式的细微变化可能显著改变准确率，人工自然语言生成评价常难以复现，静态测试集会因训练数据污染和分布变化而失效，LLM 裁判还可能受到文本风格、长度、答案位置及模型家族关系的系统性影响。本文因此不把评估分数视为固定的“真实质量”，而将其视为带有证据强度、适用边界和时间限制的知识主张。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**信任膨胀（trust inflation in evaluation）**

指多个质量不一或彼此相关的评估信号经平均后，汇总结果看起来比其中最不可靠的证据更可信。其关键风险是平均值能够掩盖模型在某些场景中的明显弱点，也可能把并不独立的重复评分误当成额外证据。

</div>
<div class="conceptitem" markdown="1">

**知识主张（epistemic claim）**

评估分数不是脱离条件、永久成立的事实，而是在特定证据和假设下对系统质量作出的断言。判断该断言是否可信，需要同时检查证据如何获得、适用于什么数据，以及在什么时间范围内仍然有效。

</div>
<div class="conceptitem" markdown="1">

**评估元数据：形式性、范围与有效期**

形式性层级描述证据强度，例如人工评价通常比单一自动指标提供更强证据；范围声明限定结论只适用于被测试的任务或数据分布。有效期表示结果会随测试集污染和数据分布变化而过时，超过期限后应重新评估。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是由多个异质信号构成的语言模型评估：输入可以包括自动指标、LLM-as-judge 评分、人工评价，以及不同基准场景的测试结果；常规系统把这些信号平均后输出总分或排行榜。本文考察这种汇总是否会隐藏最弱证据或最差场景，并主张输出不应只有一个无条件分数，而应附带形式性层级、适用范围和过期时间等元数据。其基本假设是评估证据可能不独立、可靠性不同，并且只在特定测试分布和时间窗口内支持结论；因此，评估结果应被理解为有条件且会过期的知识主张，而非模型能力的普遍真值。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$\rho$**

系统排名之间的相关系数；引言引用的复现研究用它衡量原始人工评价与复现实验所得排名的一致程度。

</div>

</div>

**直接相关的工作**

- **Belz et al. (2023)**: 该复现研究汇总多年人工自然语言生成评价，指出多数评价未能稳定复现，且原始实验与复现实验的系统排名相关性经常低于 \(\rho=0.8\)。本文以此说明人工评价本身也具有有限可靠性，不能被无条件视为永久真值。
- **Gu et al. (2024)**: 该工作综述 LLM-as-judge 研究及其系统性失效模式。本文据此把风格偏好、长度与位置效应，以及裁判和被评模型同属一个模型家族时的性能退化，视为评估信号需要明确证据强度与适用条件的背景依据。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

模型选择、排行榜比较和安全部署都依赖评测结果，但现实中的证据来源高度异质：自动指标、同一模型家族产生的多个裁判评分、人工评价和静态基准并不具有相同的证据强度，也未必相互独立。与此同时，分数只对被测试的数据分布成立，并会随着测试集污染和任务分布迁移而过时。若这些条件不随结果一起记录，使用者就可能把局部、脆弱或已经失效的证据误解为对模型整体能力的稳定证明。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **分项修复与校准方法**：既有研究通常分别处理污染检测、人工标注质量、自动指标鲁棒性和LLM裁判校准等问题，例如检查训练数据与测试集重叠、提高标注一致性，或测量裁判的长度、位置及风格偏差。此类方法主要改善单个评测环节。
- **均值式多信号聚合**：常见排行榜或评测套件将不同场景、指标或裁判给出的分数平均，得到便于排序和比较的单一总分；其隐含做法是让一个维度上的高分补偿另一个维度上的低分，并通常不在总分中表达证据依赖性、适用边界或时效性。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 分项修复把提示敏感、复现失败、污染和裁判偏差视为彼此独立的技术故障，缺少一个统一机制来说明最终分数究竟支持多强、覆盖多大范围以及持续多久，因此即使单项质量有所改善，综合结论的认识论边界仍然不透明。
- 均值聚合允许强信号补偿弱信号，也可能把相关而非独立的证据当作可累加证据；结果是关键短板被隐藏，旧结果与新结果被无条件并列，总体可信度高于最脆弱环节所能支撑的程度。作者将这一后果称为“信任膨胀”。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有评测体系缺少一种面向最终知识主张的统一表示与聚合框架：它不仅要给出性能数值，还要显式说明该数值基于何种强度的证据、仅适用于什么测试范围、何时需要重新验证，以及聚合时愿意在多大程度上容忍短板。论文试图填补的是这一结果层面的透明度与治理缺口，而不是再提出一个新的单项性能指标。

</div>
<div markdown="1"><span>核心问题</span>

如何把语言模型评测结果从无条件的固定分数改造为带有形式化等级、适用范围和有效期限的可审查知识主张，并用显式声明悲观程度的聚合规则，避免综合评价对证据可靠性的系统性高估？

</div>
<div markdown="1"><span>作者直觉</span>

一条综合结论好比由多节链条共同承载：若部署成功要求各关键条件同时成立，最薄弱的一节会限制整条链的可信程度，其他项目的高分不能自动消除这一风险。因此，先标明每条证据“有多正式、能说明哪里、有效到何时”，再根据应用风险选择从平均到最弱环节之间的聚合强度，可以让总分表达真实的证据边界。对安全关键场景应更偏向最弱环节；对一般比较则可采用较温和的悲观程度，但该选择必须公开，而不应隐藏在一个平均数中。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文是立场论文而非新的模型训练算法。其方法把语言模型评测结果重新表示为带有“认识论状态”的知识声明：输入包括各维度得分、证据来源、适用条件和评测时间；随后为证据标注形式化等级、适用范围和有效期，再使用显式声明的有序加权平均（OWA）算子聚合，最终输出既含综合分数、又含可信度边界与元数据的评测记录。技术核心是用悲观参数控制聚合策略：安全关键场景默认接近最弱环节，即综合判断不能掩盖任何关键维度的低分。

直观而言，作者反对只给出一个脱离上下文的平均分。新的记录方式更像食品标签：不仅显示一个数值，还说明证据有多可靠、适用于什么环境、何时需要重新检验；聚合时也必须公开究竟更看重平均表现还是最差表现。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 收集并结构化评测证据

将每项结果表示为独立证据信号，并保存其评测配置、数据分布、语言、模型范围和评测日期；同一模型家族生成并裁判的结果应标记为自我评估，而非独立证据。

<div class="method-step__io" markdown="1">

**输入**：模型在多个任务、子任务或质量维度上的得分，以及自动指标、LLM-as-judge、众包标注、受控人工实验或形式证明等证据来源。  
**输出**：一组可追踪来源和条件的证据记录，而不是已经平均化的单一排行榜分数。

</div>

**直观理解**：先保留每张“成绩单”的来源和考试条件，避免把不同可靠程度、不同适用范围的分数直接混在一起。尤其不能让系统用与自身高度相关的裁判给自己背书。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 标注形式化等级、范围与有效期

按证据类型赋予F0至F3形式化等级及可靠性上限，并显式声明任务领域、语言、模型规模范围、评测日期等适用范围；同时设置有效窗口，过期后将可靠性降至表示“尚不确定、而非已被否定”的下限值。

<div class="method-step__io" markdown="1">

**输入**：结构化的单项证据记录。  
**输出**：带有证据强度上限、适用边界和到期状态的评测声明。

</div>

**直观理解**：一个分数不能因为样本很多就突破其测量方法本身的可信度，也不能从英语通用任务自动推广到其他语言或专业场景。过期结果不会被判成错误，但不能继续被当作新鲜证据使用。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 选择并公开校准聚合策略

将分数降序排列后使用OWA加权聚合，并通过悲观参数ρ公开控制算子；ρ=1对应最小值、ρ=0.5对应算术平均、ρ=0对应最大值，安全关键场景建议默认采用最弱环节端点。

<div class="method-step__io" markdown="1">

**输入**：各证据或评测维度的分数，以及部署场景对漏报风险和保守程度的要求。  
**输出**：带有明确聚合算子、权重和悲观程度的综合结果。

</div>

**直观理解**：这相当于公开成绩单的计分规则：可以看平均分，也可以要求任何关键科目都不能不及格。作者并未要求所有场景一律取最低分，而是要求不能把平均规则隐藏成理所当然。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 输出可审计并可更新的评测结果

生成机器可读的评测记录，在样本量不足、归一化方式不同或证据过期时发出警告；当数据污染、分布变化、模型更新或有效期届满时触发重新评测，而不是继续沿用旧分数。

<div class="method-step__io" markdown="1">

**输入**：聚合结果、形式化等级、范围声明、有效窗口和完整评测配置。  
**输出**：可供排行榜、部署审查或后续统计分析使用的有时效、有限定范围且可追溯的评测声明。

</div>

**直观理解**：最终产物不是永久有效的冠军名次，而是一张能说明“为什么可信、在哪可信、可信到何时”的凭证。条件改变后，应更新凭证而不是只复制旧成绩。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 有序加权平均聚合

$$
\operatorname{OWA}(s;w)=\sum_{i=1}^{n} w_i s_{(i)},\qquad s_{(1)}\geq\cdots\geq s_{(n)},\quad w_i\geq0,\quad\sum_{i=1}^{n}w_i=1
$$

**符号说明**

- $s=\{s_1,\ldots,s_n\}$：待聚合的n个证据分数或评测维度得分。
- $s_{(i)}$：所有分数按降序排列后的第i个分数；s_{(1)}为最高分，s_{(n)}为最低分。
- $w_i$：分配给第i个排序位置的非负权重，所有权重之和为1。
- $n$：参与聚合的证据或评测维度数量。
- $\operatorname{OWA}(s;w)$：在给定排序位置权重w时得到的综合评测值。

<div class="equation-explanation" markdown="1">

**直观理解**：OWA不是按指标名称固定加权，而是先按得分高低排序，再决定更重视高分端还是低分端。把全部权重放在最低分位置就得到最弱环节，把权重均匀分配则得到算术平均，因此它能够统一表达不同风险偏好。  
**原文位置**：第2节“Trust inflation in evaluation”，小节“Weakest-Link as the Conservative Endpoint”

</div>

</div>

<div class="equation-block" markdown="1">

#### OWA悲观参数

$$
\beta(w)=\frac{1}{n-1}\sum_{i=1}^{n}(n-i)w_i,\qquad \rho=1-\beta(w)\in[0,1]
$$

**符号说明**

- $\beta(w)$：Yager定义的orness，表示权重偏向较高分位置的程度。
- $\rho$：论文采用的悲观参数，是orness的反向量；数值越大，聚合越强调低分和最弱环节。
- $w_i$：OWA中第i个排序位置的权重。
- $i$：降序排列后的位置索引。
- $n$：被聚合分数的数量；该公式要求n大于1。

<div class="equation-explanation" markdown="1">

**直观理解**：ρ把聚合规则压缩成一个可报告的风险偏好参数：ρ=1得到最小值，ρ=0.5对应算术平均，ρ=0得到最大值。关键主张不是永远选择ρ=1，而是根据场景校准并公开ρ，避免默认平均值悄悄掩盖关键短板。  
**原文位置**：第2节“Trust inflation in evaluation”，小节“Weakest-Link as the Conservative Endpoint”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文不提出需要梯度优化、参数学习或微调的新模型；OWA是评测结果的决策级聚合算子，形式化等级、范围和有效期也是评测元数据。权重w、悲观参数ρ、等级上限及有效窗口应依据风险和应用场景由评测者声明或校准，但原文没有给出从数据中自动学习这些量的优化目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 认识论元数据模块**

每项评测结果附带三类元数据：形式化等级衡量证据类型能够支持的最高可靠性，范围声明限定结论适用的数据分布与配置，有效窗口表示结论的时间边界。作者提出F0至F3四级默认体系：F0为LLM-as-judge或众包标注、上限0.70；F1为结构化量表或自动指标、上限0.85；F2为受控人工评测或A/B测试、上限0.95；F3为数学证明或形式性质、上限1.00。

> 直观理解：该模块防止低质量证据通过增加数量或与高质量证据求平均而显得异常可靠。文中的具体上限是作者提出、仍需社区校准的默认值，不应理解为已经大规模实证验证的固定常数。

**2. 最弱环节与OWA聚合模块**

当评测维度具有串行依赖关系，例如事实正确是语言流畅有意义的前提时，保守可靠性由最弱维度限制。OWA把最小值、平均值和最大值放入同一参数化算子族，通过权重及悲观参数ρ选择聚合位置，并要求报告该选择。

> 直观理解：如果一个系统表达流畅但事实错误，其他高分不应自动抵消事实性短板。OWA仍允许普通场景采用中间程度的折中，但让决策者看见为这种折中承担了多少“信任膨胀”风险。

**3. 可审计评测工具链**

作者以一个用于比较智能体式AI在机器学习研究任务上表现的评测工具为工程依据；该工具采用Docker隔离、受控A/B方法、结构化错误分类和配对统计分析，并强调模式版本、机器可读警告及归一化差异披露。

> 直观理解：该模块负责让不同运行真正可比较，并保存后来分析所需的信息。它是论文主张的工程案例而非跨系统的大规模验证，因此能说明设计需求，却不能单独证明所有建议普遍有效。

**训练与推理**

训练阶段不适用；论文不改变被评模型的训练过程。评测执行阶段先在明确的数据、提示、环境和时间条件下运行模型并收集各维度证据，再判断评测者是否独立、为每项证据附加形式化等级及可靠性上限、适用范围和有效窗口；之后根据使用场景选择OWA权重与ρ，对排序后的分数进行聚合，并同时输出单项得分、综合值和元数据。若任务具有安全关键的串行依赖，作者建议以ρ=1的最小值作为默认；若采用中间ρ，则应明确披露由此接受的信任膨胀风险。证据到期、评测分布改变、基准污染或模型更新后，应重新运行评测，而不能把旧结论无条件外推。

**复现信息**

论文报告的工程案例是约3,700行的智能体式AI评测工具，用于机器学习研究任务上的受控A/B比较，采用Docker隔离、结构化错误分类和配对统计分析。作者还报告该工具的输出模式在五周内、两种输出格式之间经历13次修订，用以说明模式版本化和预先保存分析字段的重要性。除此之外，原文节选未明确给出OWA权重的具体校准算法、各类证据有效窗口的精确时长、过期后可靠性下限的数值，也没有提供可直接复现的完整代码与配置；因此该方法目前更接近评测协议与报告规范，而非已经标准化的软件算法。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- 公开 HELM 排行榜：覆盖 54 个前沿模型和 10 个评测场景，用于比较按场景算术平均分与最弱项分数得到的模型排名。原文节选未明确报告具体 HELM 版本、场景名称、数据划分及抓取日期。
- 面向机器学习研究任务的智能体 AI 评测记录：由作者构建的评测框架产生，用于总结评测基础设施中的模式变更、跨边界错误和评分饱和问题。原文未明确报告任务数量、样本规模、训练或测试划分以及被比较的智能体名称。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**算术平均分**

对多个任务或能力维度的分数等权求平均，衡量总体平均表现，但可能让高分维度抵消低分维度。 （通常越高越好，但只有在各维度可以相互补偿且权重合理时，较高平均分才可解释为更强的整体表现。）

</div>
<div class="metricitem" markdown="1">

**最弱项分数**

取所有评测维度中的最低分，衡量系统最薄弱能力所形成的性能或可靠性上限。 （越高越好，因为最低分提高意味着最明显的能力短板得到改善；该指标尤其适合各能力存在串行依赖或安全关键约束的场景。）

</div>
<div class="metricitem" markdown="1">

**可靠性乘数**

对不同严格程度的评测信号赋予相对可信权重；作者的框架将样本式评分设为完整评测的 0.7 倍，以避免把快速、局部评测与完整评测视为同等证据。 （它不是直接追求越高或越低的性能指标；数值越高表示该评测证据相对于完整评测越可靠，而不是模型能力本身越强。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 公开 HELM 排行榜上，对 54 个前沿模型的 10 个场景分别采用算术平均和最弱项规则进行排名。

<div class="result-value" markdown="1">

按平均分得到的前五名与按最弱项得到的前五名完全不重合。

</div>

这表明聚合规则并非无关紧要的展示选择：允许强项补偿弱项的平均分，与强调最低能力的保守规则，可能推荐完全不同的一组模型。该结果支持作者关于“应公开聚合算子”的主张，但不能单独证明最弱项排名必然更符合所有部署目标，也不能证明平均分排名中的模型总体质量较差；哪种规则合理仍取决于任务是否允许能力之间相互补偿。

<div class="result-source" markdown="1">

来源：摘要；相关图表在所给节选中未展示

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">We illustrate the cost of mean aggregation on the public HELM leaderboard: across 54 frontier models on ten scenarios, the top-five models ranked by mean score and by weakest-link are completely disjoint.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 作者在五周内开发和使用智能体 AI 评测框架，维护逐次运行与跨运行比较两种输出格式。

<div class="result-value" markdown="1">

输出模式在五周内经历 13 次修订；每次修订都源于事后分析需要原设计没有记录的字段。

</div>

这一结果说明，评测结果是否可解释不仅取决于模型分数，还取决于评测记录是否保存了足够且版本一致的上下文。若模式没有显式版本号，分析程序可能把不同评测制度下的结果直接比较。它是一个工程观察，不等同于统计证明所有评测框架都会以类似频率修改，也没有量化这些修改对最终模型排名造成了多大影响。

<div class="result-source" markdown="1">

来源：第 4 节，Schema Volatility

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Our evaluation output schema required 13 revisions across two output formats (per-run and cross-run comparison) in five weeks, each triggered by discovering that post-hoc analysis required fields absent from the original design.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 检查 Python 评测客户端与 Go 后端之间的跨语言结果传递和失败判定。

<div class="result-value" markdown="1">

一个参数默认值导致所有脚本失败被静默记录为成功；常规单元测试、集成测试和输出检查均未发现该问题，最终通过数据库取证分析定位。

</div>

该案例表明，测量基础设施本身可能系统性地抬高成功率：后端已经计算出的失败判定，在跨语言接口处被默认参数覆盖。它直接支持“分数可信度不能高于测量过程可信度”的论点，但原文没有报告受影响的运行数量、修复前后的分数变化或错误发生概率，因此不能据此估算此类缺陷的一般流行程度。

<div class="result-source" markdown="1">

来源：第 4 节，Cross-Boundary Semantic Bugs

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">A semantic mismatch between our Python evaluation client and Go backend caused all script failures to be silently recorded as successes.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 上述分析仅依据所提供的相关章节和摘要；HELM 对应的完整表格、图、场景名称及智能体评测的原始运行记录未包含在节选中，数值和实验配置仍需对照论文全文核查。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 算术平均聚合：常见的排行榜汇总方式，允许一个维度的高分补偿另一个维度的低分；它是论文批评的默认方案，也是检验“信任膨胀”的主要比较对象。
- 最弱项聚合（minimum/weakest-link）：取各评测维度中的最低分，不允许强项掩盖关键弱项；它代表作者所讨论的保守聚合端点。
- 完整评测：在作者的分层评测框架中作为较高可靠性的参照，用于比较速度更快但证据较弱的样本式评分。
- 样本式评分：只使用部分样本进行评估，并相对于完整评测施加 0.7 倍可靠性权重；该比较用于说明评测成本与证据可靠性应被显式区分。

**实验想回答的问题**

- 在多场景模型评测中，按算术平均分聚合与按最弱项聚合是否会产生实质不同的模型排名，从而揭示平均聚合造成的“信任膨胀”？
- 真实的智能体 AI 评测基础设施中，输出模式变更、跨语言语义错误和评分上限等问题，是否会使报告分数偏离系统的实际能力或不同版本间的可比性？

**实验实现**

论文的实证内容分为排行榜重聚合和评测框架经验总结两部分。排行榜分析对公开 HELM 中 54 个前沿模型在 10 个场景上的结果分别采用算术平均和最弱项规则排序，并比较两种规则的前五名集合。评测框架部分来自一个约 3,700 行、面向机器学习研究任务的智能体 AI 评测系统；系统采用 Docker 隔离、受控 A/B 比较、结构化错误分类和配对统计分析，并提供语法检查、样本式评分、完整评测和不评测四个层级。节选未给出 HELM 数据预处理、缺失值处理、统计显著性检验，也未说明智能体任务的样本规模和重复运行次数，因此该部分更接近工程经验报告，而非完整的受控基准实验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 评分饱和案例：框架长期观察到分数停留在 SOTA 的 90.5%，起初怀疑是评测框架造成的上限，后续发现它是智能体持续选择的嵌入模型所具有的确定性限制。该案例说明，相同的分数天花板既可能来自被测系统，也可能来自测量工具，必须通过组件级排查区分原因；不过原文没有给出替换嵌入模型后的对照成绩，因此它属于定性诊断而非正式消融。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Proposes an epistemic framework for aggregating, qualifying, and expiring language-model evaluation scores.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`6560492fd1c1d08bf66ad1d687c98bebfedaf6d048a5ad74fa504479a84ecec6`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
