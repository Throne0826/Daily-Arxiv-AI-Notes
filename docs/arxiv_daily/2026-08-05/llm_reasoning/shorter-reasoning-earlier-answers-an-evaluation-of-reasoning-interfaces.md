---
title: "[论文解读] Shorter Reasoning, Earlier Answers? An Evaluation of Reasoning Interfaces"
description: "[arXiv 2608.03401][LLM Reasoning] 本文提出一种配对、等推理时点的评估框架，用以区分推理接口带来的真实早期答题改进与单纯提前结束生成，并分别考察限时正确完成、强制停止后的答案、双方均未完成时的差异及正确选项概率。"
arxiv_id: "2608.03401"
announcement_date: "2026-08-05"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:42:13.982767+00:00"
source_sha256: "7bdbddb5b92099c9617713c7f7642edd490530482eeef7f06f87515e3d3b4197"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "LLM 效率"
  - "LLM 其他"
  - "大语言模型"
  - "推理接口"
  - "推理预算"
  - "匹配推理时域"
  - "强制作答"
  - "早停"
  - "Qwen3"
  - "gpt-oss"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.03401</p>

# Shorter Reasoning, Earlier Answers? An Evaluation of Reasoning Interfaces

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Francesca Carlon, Vincent Ginis, Andres Algaba</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03401v1) · [PDF 下载](https://arxiv.org/pdf/2608.03401v1) · **关键词** 大语言模型, 推理接口, 推理预算, 匹配推理时域, 强制作答, 早停, Qwen3, gpt-oss<br>


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

本文提出一种配对、等推理时点的评估框架，用以区分推理接口带来的真实早期答题改进与单纯提前结束生成，并分别考察限时正确完成、强制停止后的答案、双方均未完成时的差异及正确选项概率。

**不用术语来说**：要求模型“少想一点”或选择较低推理强度，确实可能让它更快给出答案，但这不等于它在相同时间内想得更好：低强度运行可能已经交卷，而高强度运行仍在推理。若只比较两者最终答案和完整推理长度，就会把“更早停止”误判成“更高效地得到正确答案”。本文关注的是，在相同推理预算或相同停止时点下，不同推理接口究竟能否更早形成正确且可靠的答案。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 建立配对的等推理时点评估：对同一问题的不同运行施加相同外部停止点，并将“截止前正确完成”“停止时得到的答案”“双方均未完成时的答案差异”和“赋予正确选项的概率”分开报告，从而拆解提前完成与推理质量变化。
- 在Qwen3-14B的数值预算／简洁提示和早期可用答案指令，以及gpt-oss-20b／-120b的训练式推理强度设置上检验该框架，并通过已完成答案、同题控制、脚本化正对照和生成答案续写来验证强制答题测量。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大语言模型在回答高难度问题时，常先生成一段中间推理，再输出最终答案；增加测试时推理量有时能提高数学、科学和代码任务的准确率，但也会增加令牌成本、延迟和资源波动。本文关注“推理接口”的评估：提示词或模型内置档位可以改变推理长度，但常见的“完整推理长度—最终准确率”比较无法区分两种效应——干预究竟使模型在相同推理进度下更早形成了更好的答案，还是仅让模型更早停止。因此，论文在相同问题和匹配的推理时点上成对比较不同接口，并将按时完成、截断时答案、双方均未完成时的差异以及正确选项概率分开衡量。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**中间推理轨迹**

模型在最终作答前生成的逐步分析文本，也常称为思维链。轨迹长度通常以生成令牌数衡量，但更短并不自动表示推理效率或答案质量更高。

</div>
<div class="concept-item" markdown="1">

**推理控制与推理接口**

推理控制是改变模型输出多少中间推理的干预；推理接口则是用户施加该干预的方式，例如要求简洁作答的提示词，或模型训练得到的低、中、高推理强度设置。

</div>
<div class="concept-item" markdown="1">

**匹配推理时域与强制作答**

匹配推理时域是把同一问题的两次运行截取到相同或可比的推理进度；强制作答是在模型尚未自然结束时停止其推理并取得当时的候选答案。这样可以比较固定截止时间下“此刻会答什么”，而不只比较完整运行的最终结果。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是来自 GPQA Diamond 与 MMLU-Pro 的多项选择题，以及同一模型在不同推理接口下的成对运行：Qwen3-14B 比较普通生成与包含令牌限额或简洁要求的提示词，gpt-oss-20b/-120b 比较低、中、高推理强度。评估在外部设定的停止点 $B$，或较低强度运行自然结束的对应时点，观察每次运行是否已经完成且答对；若尚未完成，则截断推理并提取候选答案，同时考察双方均未完成时的答案差异和模型赋予正确选项的概率。核心假设是同题成对比较能够控制题目难度，而完成状态必须单独记录，否则“较早得到完整答案”会被误解为“相同推理进度下答案质量更高”。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$B$**

外部施加的推理停止点或令牌预算；Qwen 的不同提示条件在同一个 $B$ 上接受比较。

</div>

</div>

**直接相关的工作**

- **按完整轨迹长度绘制最终准确率的推理接口评估（引言引用文献[26]）**: 该范式衡量最终成本—准确率权衡，但不能判断控制方法是在固定推理时域内改善了答案，还是只促使模型更早停止；本文据此引入匹配时域和完成状态分解。
- **利用截断轨迹和强制作答研究答案稳定化与早停（引言引用文献[28–30]）**: 本文继承其在推理未完成时探测答案的思路，并进一步对同一问题的不同推理接口进行成对比较，同时分别报告完成正确性、截断答案、双方均未完成时的差异及正确答案概率。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

长推理会增加令牌成本和响应延迟，而且单次回答可能消耗数万令牌；模型事实上已经选定答案后，额外推理还可能收益很小。在有明确截止时间或算力预算的部署环境中，用户需要知道某种推理控制是否能提高截止前获得正确答案的机会，而不只是缩短最终输出记录。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **缩短或调节推理的接口**：通过偏好短推理的训练、模型内置的推理强度设置、生成过程引导，或要求简洁推理的提示词，改变模型在给出最终答案前产生的中间推理量。
- **完整轨迹的成本—准确率评估与轨迹截断研究**：常规评估将最终准确率对完整推理轨迹长度作图；相关早停研究则截断生成轨迹并要求模型给出答案，以分析答案何时稳定以及是否可以提前停止。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 仅按完整轨迹长度比较最终准确率，会混合两种不同效应：控制措施可能改善固定推理时点的答案，也可能只是促使模型更早停止。因此，这类结果无法判断未完成推理本身是否更优。
- 较早停止的运行已经有正式答案，而较高强度运行在同一时点可能仍未完成；若不单独记录完成状态、强制停止答案以及双方均未完成的情形，就会把状态不对称造成的部署优势误解为内在推理质量提升，也无法判断错误早期答案是否具有良好的概率质量。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚缺少一种在同一问题、同一推理时点上配对比较不同推理接口，并明确分离“提前完成的收益”与“未完成轨迹中的答案质量变化”的评估协议；同时也缺少对正确选项概率的独立检查，以识别模型是否只是更自信地提前给出错误答案。

</div>
<div markdown="1"><span>核心问题</span>

在匹配推理时点或外部令牌预算后，简洁提示、早期答案指令以及低／中推理强度是否真的让模型更早形成更正确、更可靠的答案，还是其表面优势主要来自运行更早结束；当允许高推理强度完整运行时，这种优势是否仍然存在？

</div>
<div markdown="1"><span>作者直觉</span>

把同一道题的两次运行放在相同“计时刻度”上，并标注它们是否已经结束，就像在同一考试时刻比较两名学生：既统计谁已经正确交卷，也让尚未交卷者立即写下当前答案，再只比较双方都仍在作答的样本。这样可以直接识别收益究竟来自更快交卷、较好的中途判断，还是更合理的概率分配，而不会用最终轨迹长度替代真正的限时表现。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文提出的不是新的推理模型或训练算法，而是一套“匹配推理时点”（matched-horizon）评估协议。核心输入是同一道选择题在不同推理控制条件下生成的成对轨迹：Qwen3-14B比较普通提示与数值/简洁提示，并另行测试要求尽早给出可用答案的简洁指令；gpt-oss-20b与gpt-oss-120b比较低、中、高推理努力设置。对于题目$i$、独立生成重复$r$和条件$z$，作者记录完整推理的终止长度$L_{ir}^{z}$，再在统一推理视界$B$处读取答案，而不是只比较各条件自然结束后的准确率。这样可以区分两种机制：控制条件究竟改善了同样计算量下已有的中间答案，还是仅让模型更早停止并提交答案。

在视界$B$处，若轨迹尚未结束，协议截断其推理前缀、关闭推理块，并要求模型从候选项中作答；若轨迹已经自然结束，则保留其自然终止答案。作者同时记录正确完成、截断后答案正确性、终止状态分层以及正确选项概率，并使用生成式答案续写等方式验证强制作答读出的可靠性。直观地说，该方法像在两名考生开考相同时间后同时收卷：既检查谁已经主动交卷，也检查尚未交卷者此刻被要求作答时会选什么，避免把“交卷更早”误解为“每一分钟都思考得更好”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造成对的推理控制轨迹

对每个题目$i$在各条件$z$下生成完整推理轨迹并记录终止长度$L_{ir}^{z}$。Qwen实验改变提示中的预算、简洁性或尽早作答要求，gpt-oss实验改变模型已训练的低、中、高努力设置；比较严格限制在同一模型家族内部。

<div class="method-step__io" markdown="1">

**输入**：同一批多项选择题、同一模型家族内的不同推理接口，以及独立生成重复$r$；主要题集为198道GPQA Diamond和按学科抽样的500道MMLU-Pro题目。<br>
**输出**：按题目与重复配对的完整轨迹、自然终止答案、推理长度和终止状态。

</div>

**直观理解**：先让同一道题在两种“思考方式”下各做一次，并保存全过程。配对能减少题目难度差异造成的干扰，但不能把提示控制与训练所得努力设置解释为可直接比较的因果处理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 在共同推理视界截断并读取答案

Qwen条件在相同外部停止点$B$接受评估；gpt-oss则在低或中努力轨迹自然结束的逐题视界上，重建高努力轨迹的对应前缀。对尚未结束的前缀使用标准化前缀探针读出$\rho=P$，对已经结束的轨迹使用自然终止读出$\rho=N$；另以生成式续写$\rho=C$作为验证性读出。

<div class="method-step__io" markdown="1">

**输入**：成对轨迹以及外部指定或由较低努力轨迹决定的视界$B$。<br>
**输出**：每个题目、重复、条件和视界对应的答案与二元正确性$Y_{ir}^{z,\rho}(B)$。

</div>

**直观理解**：比较不再发生在两条轨迹各自结束的时候，而发生在二者已经使用相同推理长度的时候。若一方还在思考，就暂时叫停并要求它立即选答案；若已经答完，则直接采用其原答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 分解停止时间与未完成前缀质量

作者把样本划分为双方均未结束、较低努力已结束而高努力仍活跃、双方均结束，以及高努力已结束而较低努力仍活跃等终止层，并计算各层对总体准确率差的贡献。另行报告截止时间前正确完成、停止未完成轨迹所得答案，以及双方均未完成时的条件差异。

<div class="method-step__io" markdown="1">

**输入**：视界$B$处每对轨迹的终止状态、强制或自然答案及其正确性。<br>
**输出**：按终止状态分解的准确率差及“更早停止”和“同视界答案变化”两类效应的诊断结果。

</div>

**直观理解**：如果较低努力模型领先只是因为它已经交卷，而高努力模型仍在草稿阶段，这种领先不等于其草稿本身更好。分层分析把“先交卷的收益”与“同样尚未交卷时答案更好”分开。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 评估答案选择、概率质量与统计不确定性

除准确率外，作者用Brier分数和条件对数损失检查概率预测质量，并考察正确选项概率的尾部；主分析先在题目内平均三个配对生成重复，再对题目进行10,000次bootstrap。九臂Qwen机制实验对500道题各使用八个题目特定重复，并采用嵌套配对bootstrap与同时区间控制同一组提示比较的不确定性。

<div class="method-step__io" markdown="1">

**输入**：候选项答案、正确选项概率、成对重复结果，以及前缀探针和自然答案之间的验证样本。<br>
**输出**：准确率、概率评分、置信区间、读出有效性诊断及对轨迹随机性的敏感性分析。

</div>

**直观理解**：选对答案只说明概率最高的候选项是否正确，不说明模型是否合理校准；一个错误答案也可能获得几乎全部概率。因此作者把“选了什么”和“对正确答案有多大信心”分别评估，并用成对重采样判断观察到的差异是否稳定。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 匹配视界正确性变量

$$
Y_{ir}^{z,\rho}(B) \in \{0,1\}
$$

**符号说明**

- $i$：题目索引。
- $r$：独立生成重复的索引。
- $z$：生成条件，例如普通提示、简洁提示，或低、中、高推理努力设置。
- $B$：评估推理视界，即允许使用的推理前缀长度或逐题匹配的停止点。
- $\rho$：答案读出方式；文中包括标准化前缀探针P、自然终止读出N和生成式答案续写C。
- $Y_{ir}^{z,\rho}(B)$：条件z在视界B处采用读出方式ρ所得答案的正确性；正确为1，错误为0。

<div class="equation-explanation" markdown="1">

**直观理解**：该变量把“哪道题、哪次随机生成、采用何种推理控制、何时停止、如何读取答案”全部显式写入评估对象。方法的关键不是公式复杂，而是保证不同条件的正确性在同一个$B$上比较，并把读出机制$\rho$与生成策略$z$分开。<br>
**原文位置**：第2节“Matched-horizon probes separate evaluation points from generation policies”，首段定义。

</div>

</div>

<div class="equation-block" markdown="1">

#### 条件轨迹的自然终止长度

$$
L_{ir}^{z}
$$

**符号说明**

- $L_{ir}^{z}$：题目i在重复r和条件z下自然结束时的推理长度。
- $i$：题目索引。
- $r$：生成重复索引。
- $z$：推理接口或生成条件。

<div class="equation-explanation" markdown="1">

**直观理解**：将$B$与$L_{ir}^{z}$比较即可判断该轨迹在评估时点是否已经完成：若自然终止长度不超过视界，就使用完成答案；否则只能读取被截断前缀。gpt-oss实验还用较低努力条件的$L_{ir}^{z}$作为与高努力前缀匹配的逐题视界。<br>
**原文位置**：第2节“Matched-horizon probes separate evaluation points from generation policies”，首段记号定义。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文提出的是推理接口的评估方法，没有训练新模型、微调参数或优化新的损失函数；Qwen的提示干预和gpt-oss已有的努力设置均在推理阶段使用。Brier分数与条件对数损失是评估概率质量的评分规则，不是本文用于更新模型参数的训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 匹配视界与逐题配对模块**

该模块以题目$i$和生成重复$r$为配对单位，在共同视界$B$比较条件$z$。Qwen使用相同的外部停止点；gpt-oss以每条低或中努力轨迹的实际终止长度作为逐题视界，并在该长度读取可重建的高努力前缀，从而使被比较答案对应相同的已用推理长度。

> 直观理解：传统的“最终准确率—最终长度”曲线把停止策略和中间推理质量混在一起。匹配视界相当于给两种条件相同的考试时间，再比较当时可用的答案。

**2. 多读出强制作答模块**

标准化前缀探针$\rho=P$关闭被截断的推理块，并在统一的最终作答上下文中读取候选项；自然终止读出$\rho=N$保留模型自行结束时给出的答案；生成式续写$\rho=C$则让截断前缀继续生成答案，用于检查候选项归一化或强制格式是否改变结论。作者还以完整答案回放、同题控制、脚本化正对照和答案续写验证该测量。

> 直观理解：未完成的草稿本来没有正式答案，因此必须设计一种公平的“现在就回答”接口。多种读出的一致性检查用于确认结果不是由特殊答题模板或候选项读取方式人为制造的。

**3. 终止状态与概率质量诊断模块**

终止状态分层把总体准确率差写成不同配对状态的贡献，以识别优势来自提前完成还是活跃前缀本身。概率层面分别报告Brier分数、条件对数损失和正确选项概率尾部，因为0/1准确率不会惩罚对错误选项的过度自信，而对数损失会强烈反映接近零的正确选项概率。

> 直观理解：“更早得到一个正确选项”和“更早形成可靠的概率判断”不是同一件事。该模块避免仅凭准确率就认定短推理在所有意义上更优。

**训练与推理**

完整过程均属于推理与离线评估。首先，在相同题目和配对随机重复上运行各推理接口，并保存完整推理轨迹、终止长度、最终答案以及可用于候选项概率读取的信息。Qwen3-14B的主要条件包括普通生成、宣布数值预算并要求简洁的提示，以及单独的“简洁推理并优先尽早给出可用答案”指令；九臂机制实验进一步区分隐藏视界、宣布512或2,048词元的数值/简洁提示、提前准确停止通知、通用有限预算措辞、仅数字措辞、尽早作答指令和无关数字安慰剂。gpt-oss-20b与gpt-oss-120b则分别生成低、中、高努力轨迹。

随后选择共同视界$B$：Qwen在预设检查点截断各条件，gpt-oss在较低努力轨迹自然结束的位置读取匹配的高努力前缀。已完成轨迹采用自然答案，未完成轨迹通过统一前缀探针强制作答；若高努力轨迹已在该视界前完成，则回放其完成推理块。最后按题目和重复形成成对差，分别分析总体正确性、双方均活跃时的前缀差异、各终止层贡献、Brier分数和条件对数损失，并通过自然完成答案、生成式答案续写及控制前缀检验强制读出的可信度。该流程估计的是特定模型家族与干预下的同视界差异，不支持把Qwen提示与gpt-oss训练式努力设置作跨家族因果比较。

**复现信息**

主要实验使用GPQA Diamond的198道题和跨学科抽样的500道MMLU-Pro题，主要模型为Qwen3-14B、gpt-oss-20b和gpt-oss-120b；Qwen3-4B与Qwen3-8B用于测量校准，Omni-MATH-2用于开放式数学扩展。主Qwen曲线和gpt-oss对比各使用三个独立的全局生成重复，条件在题目与重复内配对；先对每题的三个配对结果求平均，再以题目为单位进行10,000次bootstrap。由于只有三个全局重复，双向bootstrap、逐重复分析及题目—重复交叉随机截距仅作为对轨迹集合变化的敏感性诊断，不能提供精确的跨随机种子总体推断。

九臂Qwen机制实验在500道MMLU-Pro题上每题设置八个重复；题目标识、重复编号和基础种子的确定性哈希生成随机种子，同一题目—重复种子在九个提示臂间复用，以维持严格配对。其区间采用先重采样题目、再重采样题目内八个配对重复的嵌套bootstrap；同一提示—视界比较族使用最大绝对偏差构造同时区间。前缀探针需要可重建的轨迹；gpt-oss比较仅纳入可回放的匹配前缀，并用统一的中等努力最终作答上下文读取完成的低或中努力前缀及对应高努力前缀，以降低答案上下文本身不同造成的混杂。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GPQA Diamond：198道高难度研究生水平多项选择题。它用于检验短预算或低推理强度在困难科学推理上的效果；Qwen的字面“先限长推理、再作答”验证也覆盖全部198题。
- MMLU-Pro：主要分析使用500道多项选择题，并按原实验设计进行分层分析。它既用于Qwen3-14B的预算曲线，也用于九提示臂机制实验，从而区分数字、简洁措辞、提前通知和无关数字等提示因素。
- Omni-MATH-2：用于检查结论能否延伸到自由形式数学答案。Qwen分析采用200题子集；gpt-oss按原生难度信息抽取500题，最终模型特定配对样本为gpt-oss-20b的475题和gpt-oss-120b的490题。答案由指定的GPT-5 mini快照判定，因此该部分是补充性外部有效性检验，而非主要多项选择结论。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**配对准确率**

比较同一题、同一复现和同一推理截止长度下，候选字母预测或贪心最终回答是否正确。缺失或格式错误的选项字母按错误计，因此该指标同时反映截止前答案是否已经可用。 （越高越好，因为它表示在固定计算期限内能得到更多正确、可解析的答案。）

</div>
<div class="metric-item" markdown="1">

**条件对数损失**

先把所有有效单词元选项字母写法的概率聚合并归一化为$q_y$，再计算正确选项$y^\star$的$-\log q_{y^\star}$；它评价模型分配给正确答案的概率，而不只看最大概率选项。 （越低越好，因为较低值表示模型为正确选项分配了更高的条件概率。）

</div>
<div class="metric-item" markdown="1">

**终止感知答案可用性AUC**

在$0,64,\ldots,512$词元检查点读取正确答案对数优势，并对轨迹做词元归一化梯形积分；若轨迹提前自然终止，则把终止时的答案分布延续至后续检查点。它同时衡量证据形成速度和提前完成的实际收益。 （越高越好，因为它表示正确答案在推理过程更早、且更持续地可被读出。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3-14B：数字／简洁预算提示与普通生成，在匹配外部截止长度下比较

<div class="result-value" markdown="1">

作者报告该提示使推理轨迹缩短12%至17%，但在匹配词元上限后的准确率变化总体较小且方向不一致。

</div>

这说明“完整输出更短”不能自动推出“模型更早知道正确答案”。匹配$B$后，两组拥有相同的可观察推理长度，因此小而混合的准确率差异表明，数字预算提示的主要效果可能是改变停止行为，而非稳定地把正确推理前移。该结果仅适用于所测Qwen模型、提示和题集，不能证明所有简洁提示都无效。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The Qwen prompt shortens reasoning traces by 12-17%, while accuracy changes at matched token limits are small and mixed.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3-14B：MMLU-Pro上的简洁／尽早作答指令，在512词元截止处与普通生成比较

<div class="result-value" markdown="1">

该指令在512词元时将准确率提高3.8个百分点；即使只看两条轨迹都尚未完成的配对，仍提高2.7个百分点。到2048词元时，增益不确定。

</div>

512词元下的总体增益不完全由处理组更早结束解释，因为“双边均未完成”时仍存在较小优势；这为提示改变早期推理内容提供了证据。不过2048词元结论不稳定，说明优势依赖紧迫期限，不能解释为最终能力普遍提高，也不能据此断言更短推理始终更准确。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A concise/early-answer instruction raises MMLU-Pro accuracy by 3.8 percentage points at 512 tokens, including +2.7 points when both runs are unfinished.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### gpt-oss-20b与gpt-oss-120b：已完成的低／中强度轨迹对比匹配长度的高强度轨迹

<div class="result-value" markdown="1">

低强度和中强度已完成推理的候选对数几率答案，比同一截止长度下的高强度答案高14.5至26.3个百分点。

</div>

在严格截止期限内，较低强度策略往往已经结束并形成可读答案，而高强度策略可能仍在展开推理，因此前者具有显著的限时准确率优势。但作者进一步指出，512词元优势大多来自更早完成，未完成轨迹之间的差异更小且方向混合；所以该结果证明的是期限下的接口效用，而不是低强度推理在同等状态下具有更高的内在推理质量。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For gpt-oss, candidate-logit answers from completed low- and medium-effort reasoning are 14.5-26.3 points more accurate than matched-horizon high-effort answers.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主要推断只基于3组全局生成复现。题目bootstrap能描述当前已观察轨迹集合上的不确定性，但不足以精确估计随机种子总体差异；交叉随机效应和双向bootstrap也只能作为敏感性诊断。
- 结论受模型、提示、截止长度和读出方式限制。Omni-MATH-2部分仅每条件一次 rollout，并依赖外部模型判分；候选对数几率探测则是标准化前缀上的工具性读出，不等同于恢复原始生成时的完整内部状态或KV缓存。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Qwen3-14B普通生成／隐藏截止基线：生成时不出现数字预算或简洁指令，但在探测时施加与处理组完全相同的外部长度上限。该比较控制模型、题目和可见推理长度，用来判断提示是否改变了“答案出现的时间”，而非仅比较完整轨迹的长短。
- gpt-oss高推理强度基线：将低强度或中强度轨迹与同题、同复现、同匹配推理长度下的高强度轨迹比较。它直接检验紧迫截止下，更多预设推理投入是否反而延迟可用答案。
- 九臂提示机制对照：包括隐藏截止、宣告512或2048词元的数字／简洁提示、精确停止预告、一般有限预算措辞、仅数字措辞、简洁／尽早作答指令及无关数字安慰剂。它们用于拆分“数字匹配”“知道会被截断”和“要求尽早给出答案”三个可能机制。
- 随机、跨题交换与乱序前缀对照：分别保留长度和位置、保留连贯但与当前题无关的推理、以及保留原词元集合但破坏顺序。它们检验提前恢复的准确率是否依赖当前实例的有序推理内容，而非上下文长度或表面词元统计。

**实验想回答的问题**

- 在相同问题、相同模型和相同外部推理截止长度下，数字预算／简洁提示或模型内置的低、中、高推理强度，是否能让正确答案更早可用，而不只是让模型更早停止生成？
- 观察到的限时优势主要来自低强度轨迹更早完成，还是来自尚未完成的推理前缀本身更快形成正确判断；这种优势是否同时改善答案概率的校准质量？

**实验实现**

主要Qwen预算曲线和gpt-oss实验使用3组独立全局随机复现，条件在题目与复现内配对；计划的23034次生成全部存在。Qwen处理组在系统提示后追加所测指令，普通组不追加，探测时对两组施加相同外部推理长度$B$。gpt-oss通过聊天模板设置low、medium或high推理强度。主要候选对数几率读出使用本地Transformers／PyTorch前向传播：精确重放存储的前$B$个推理词元，关闭推理通道，在第一个答案位置提取全词表对数几率，并聚合所有受支持的单字母及带前导空格写法；这避免了解码再分词造成的前缀偏差。另以最多16个词元的确定性贪心续写作为行为读出。

统计上，主要分析先在每题内平均3个配对复现，再对题目进行10000次bootstrap；同时报告逐复现、题目×复现双向bootstrap和交叉随机截距敏感性分析。九臂Qwen机制实验在500道MMLU-Pro题上每题使用8个配对复现，共36000次生成与72000次策略上下文重放，并采用嵌套配对bootstrap及同时置信区间。作者还分别使用“策略上下文”和统一的“公共上下文”重放，以区分生成提示本身的直接影响与其所诱导推理前缀的影响。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 双方均未完成的活跃前缀子集 | MMLU-Pro在512词元处，简洁／尽早作答指令在双方都尚未完成时仍有2.7个百分点的准确率优势，小于包含已完成轨迹时的3.8个百分点总体优势。 | 该拆分隔离了自然终止带来的收益：总体优势与未完成子集优势之间的差距说明，部分收益确实来自更早完成；仍保留的2.7个百分点则与早期推理前缀发生变化相符。不过这是按“仍在推理”条件筛选后的比较，可能改变样本构成，不能当作完全独立识别的因果效应。 | 摘要<br><span class="experiment-evidence">A concise/early-answer instruction raises MMLU-Pro accuracy by 3.8 percentage points at 512 tokens, including +2.7 points when both runs are unfinished.</span> |
| 脚本化正控制：短策略立即暴露正确字母，长策略延后暴露 | 在64词元时，长策略准确率为25.0%，短策略为100.0%；到512词元时，两者均为100.0%。 | 这个人工构造实验验证了截断与候选字母读出确实能检测已知的“答案更早出现”：只有短策略在64词元前提供答案，因此出现75个百分点差距；当两条轨迹都已暴露答案后，差距消失。它只验证测量管线，不构成Qwen或gpt-oss会自发遵循精确数字预算的证据。 | 附录A.6，表A29<br><span class="experiment-evidence">Accuracy moves from 25.0% for the long policy to 100.0% for the short policy at B= 64 ; both reach 100.0% at B= 512 (Table A29).</span> |

**定性案例**

- 轨迹诊断显示，错误的早期答案有时仍把概率高度集中在所选错误选项上。其含义是：接口可以促使模型更早“承诺”一个答案，却未必更早积累了可靠证据；因此仅观察截止点准确率可能掩盖过度自信，需结合条件对数损失、Brier分数或正确答案概率分析。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Evaluates how concise prompts and trained effort settings affect reasoning length, early-answer accuracy, latency, and token-budget performance.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`7bdbddb5b92099c9617713c7f7642edd490530482eeef7f06f87515e3d3b4197`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
