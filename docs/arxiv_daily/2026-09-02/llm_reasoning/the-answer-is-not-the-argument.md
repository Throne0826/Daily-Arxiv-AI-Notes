---
title: "[论文解读] The Answer Is Not the Argument"
description: "[arXiv 2609.00264][LLM Reasoning] 本文检验可信参考答案究竟帮助大语言模型监控器验证推理过程，还是仅帮助其发现结论不一致，并指出依赖参考答案的汇总成绩可能高估过程监督能力。"
arxiv_id: "2609.00264"
announcement_date: "2026-09-02"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:39:40.205989+00:00"
source_sha256: "02acccaf387f3bca1954168f7e25594c8d20b15783a24d6eba763b53766a07f5"
tags:
  - "LLM Reasoning"
  - "LLM 安全"
  - "LLM 评测"
  - "大语言模型"
  - "思维链监控"
  - "推理验证"
  - "过程监督"
  - "首错定位"
  - "参考答案依赖"
  - "人工智能监督"
  - "Humanity’s Last Exam"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.00264</p>

# The Answer Is Not the Argument

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Will Yeadon, Sergio Juárez, Paul Mackay, T. J. Dowling, Elise Agra, Oto-obong Inyang, Arin Mizouri, Craig P. Testrow</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: 1 Department of Physics, Durham University, Durham DH1 3LE, UK；Affiliation: 2 Escuela de Ingeniería de Telecomunicación, Department of Signal Theory and Communications, University of Vigo, Vigo E-36310, Spain；Department of Physics, Durham University, Durham DH1 3LE, UK；Escuela de Ingeniería de Telecomunicación, Department of Signal Theory and Communications, University of Vigo, Vigo E-36310, Spain</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00264v1) · [PDF 下载](https://arxiv.org/pdf/2609.00264v1) · **关键词** 大语言模型, 思维链监控, 推理验证, 过程监督, 首错定位, 参考答案依赖, 人工智能监督, Humanity’s Last Exam<br>


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

本文检验可信参考答案究竟帮助大语言模型监控器验证推理过程，还是仅帮助其发现结论不一致，并指出依赖参考答案的汇总成绩可能高估过程监督能力。

**不用术语来说**：让一个模型检查另一个模型写出的解题过程时，直接告诉检查者标准答案通常会让评分变好，但这不等于它真正看懂并核验了推理：它可能只是在比较最终结论。真正关键的是，即使答案正确，推导中也可能存在事实或逻辑错误；若监控器放过这类过程，就无法可靠识别“结果看似合格、产生结果的过程却不可靠”的情况。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者把“验证论证”与“核对答案”拆分为可区分的能力：固定同一条自然生成的物理解题轨迹，仅改变监控器获得的参考答案信息，并分别考察错误检测与首个错误步骤定位。
- 作者将最终答案错误的轨迹与“答案正确但推理确有错误”的关键轨迹分开分析，从而检验参考答案带来的性能提升是否真正覆盖结论无法暴露的过程错误。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型监督与推理过程评估研究。大语言模型常输出思维链，即以自然语言写出的分步推理；链式思维监控则让另一个模型阅读这些步骤，判断论证是否存在错误。此类监控可能成为高级人工智能监督体系的一层，但其有效性必须在接近真实部署的条件下衡量。关键问题是：评测若向监控模型提供可信参考答案，模型可能只需比较最终结论便能发现答案错误，而不必真正核验中间论证。本文因此把“论证是否成立”与“结论是否正确”分开，重点考察最终答案正确但推理中确有错误的轨迹，因为这类样本无法仅凭答案暴露问题，并在结构上类似于“输出可接受、生成过程却不可靠”的奖励黑客现象。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**思维链监控**

由一个监控模型检查另一个模型写出的分步推理，并判断整条推理是否错误以及首个错误出现在哪一步。它评估的是外显文本论证，而不保证这些文字忠实反映被监控模型内部实际完成的计算。

</div>
<div class="concept-item" markdown="1">

**结果监督与过程监督**

结果监督只依据最终答案是否正确进行评价；过程监督则检查中间步骤，能够发现“答案碰巧正确但论证无效”的情况。本文关注的监控任务可视为一种过程层面的验证。

</div>
<div class="concept-item" markdown="1">

**首错定位**

首错定位要求指出推理轨迹中第一个实质性错误步骤，而不只是判断整条解答对错。它比结论一致性检查更能检验监控模型是否真正阅读并验证了论证。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是三个前沿模型针对 Humanity’s Last Exam 物理题自然生成的分步解答，错误并非人工插入。数据包含 79 道题的 237 条带步骤编号的推理轨迹；每条轨迹分别标注最终答案是否正确，以及若论证有误时第一个错误步骤的位置。参考标准综合物理学专家标注、独立的大语言模型辩论和隐去生成来源后的裁决。八个监控模型在保持题目与推理轨迹不变的情况下接受不同信息条件：看不到参考答案、看到但未获认证的答案、看到被明确认证为正确的答案，或先在盲测条件下作出判断再获得答案。监控输出包括整条轨迹是否有错及首错位置；核心比较对象是错误答案轨迹与“最终答案正确但推理存在真实错误”的关键轨迹，从而判断参考答案访问究竟提升了独立论证验证，还是主要增强了结论一致性检查。该设置只评估外显推理文本的正确性，不主张该文本必然忠实呈现模型的内部推理过程；同时，样本中的错误主要是普通且多为非承重错误，而非刻意规避监控的对抗性行为。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **MonitorBench**: 该工作发现，可监控性取决于决策关键信息是否被结构性地纳入中间推理：只影响最终回答的注入答案线索，比会改变中间推理的附加条件更难监控。本文研究互补的读取端效应——生成时不提供参考答案，只在监控阶段改变答案的可得性与可信状态，以检验答案访问对真实推理错误检测的影响。
- **大语言模型作为物理作业评判者的参考答案依赖研究**: 既有研究表明，评判模型面对故意错误的参考解答时，可能把正确作答误判为错误，说明参考信息会重塑判断并引发依赖。本文把问题推进到参考答案真实可信的情形，考察这种依赖是否会让监控评测高估模型核验论证的能力。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

思维链监控被设想为人工智能监督体系中的一层：由一个大语言模型阅读另一个模型公开的推理并标记错误。然而，部署这类机制前必须知道它实际能够承担多少监督责任。尤其在奖励投机等安全风险中，系统可能给出可接受的输出，却通过不可靠甚至有问题的过程得到它；如果监控器只能判断输出是否符合预期，而不能独立检查论证，它就会漏掉最需要过程监督发现的风险。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **带可信参考答案的思维链监控评测**：向监控模型提供题目、待检查的推理轨迹以及经过认证的正确答案，再让它判断轨迹是否有错或定位错误。这种设置便于提高判断准确率，但同时允许监控器通过比较最终答案来推断整条轨迹是否可靠。
- **结果监督与既有可监控性评测**：结果监督用最终答案是否正确作为主要信号；既有可监控性研究则比较不同推理信息、提示可见性、阅读模型强度或注入线索位置下的预测能力。这些研究说明可见信息会改变监控表现，但未直接隔离监控阶段的答案访问对独立推理核验能力的影响。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 提供可信答案会混合两种不同能力：逐步检查论证是否成立，以及查看结论是否与标准答案一致。因此，参考答案条件下更高的汇总检测成绩不能直接证明监控器验证了推理过程，并可能夸大其过程监督能力。
- 仅按最终答案正确与否评测，会掩盖“正确答案由错误推理得到”的关键样本；跨题预测还可能利用题目难度等旁路线索。其后果是评测无法确定监控器能否发现不影响结论、被抵消或由猜测掩盖的真实推理错误。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚缺少一种受控评测：对同一批未经人工植入错误、且由专家独立裁定首个错误步骤的自然推理轨迹，只改变参考答案在监控阶段是否可见及是否被认证，并专门测量正确结论所掩盖的过程错误。因而，人们尚不能判断可信答案带来的性能增益究竟来自论证核验，还是来自结论一致性检查。

</div>
<div markdown="1"><span>核心问题</span>

当大语言模型监控器获得可信参考答案时，它是否更能发现并定位独立裁定的推理错误，特别是最终答案正确却包含真实错误的轨迹；还是主要更容易识别最终答案错误的轨迹，从而使评测成绩虚高？

</div>
<div markdown="1"><span>作者直觉</span>

若参考答案真正增强了推理核验，那么它对不同最终结论类型的错误轨迹都应有帮助，尤其不应削弱对“答案正确但过程错误”轨迹的识别。反之，若增益主要来自答案比对，提升就会集中在最终答案错误的轨迹，而正确答案会反过来使监控器更愿意放过其中的过程错误。通过固定轨迹、只改变答案信息，并比较这两类轨迹的召回与首错定位，便可区分两种机制。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是训练新模型，而是构建一个用于检验链式思维监控能力的评估流程。流程以经过筛选的物理题和三个生成模型产生的编号解答为输入，先独立标注最终答案是否正确以及推理中最早的错误步骤，再让八个监控模型在不同答案可见性条件下判断是否存在错误并定位错误步骤，最后比较检测与定位指标。技术上，研究将“结论错误”和“论证错误”分开：正确答案但含有错误推理的 $24$ 条关键轨迹用于测试监控器是否真的检查论证，而不是仅核对结论；直观地说，研究不是问“答案对不对”，而是问“解题过程是否每一步都站得住”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 题目筛选与解答生成

依次保留文本题、精确匹配题和确实需要多步物理推理的题目，并剔除物理设定不适定、参考答案错误或存在多个合理答案的题目。三个生成模型各对每道保留题目生成一份按步骤编号的解答，并将最终答案放入方框。

<div class="method-step__io" markdown="1">

**输入**：Humanity's Last Exam 中物理类别的题目，以及三个前沿生成模型 GPT-5.5、Claude Opus 4.7 和 Gemini 3.1 Pro。<br>
**输出**：来自 $79$ 道题的 $237$ 条解答轨迹，每道题对应三个生成模型的轨迹。

</div>

**直观理解**：先把题目筛成适合公平核验的版本，再让不同模型各自完整作答；这样后续监控器看到的是自然产生的推理错误，而不是研究者故意植入的错误。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 参考标准构建

对每条轨迹分别判断最终答案是否正确，并寻找第一个作出虚假断言的步骤；探索性尝试本身不算错误，但错误的物理、数学、数值或关于此前推理的断言算错误。物理学家标注了 $174$ 条轨迹，独立的五轮语言模型辩论覆盖全部轨迹，主作者在隐藏标注来源后裁决分歧，形成最终参考标准。

<div class="method-step__io" markdown="1">

**输入**：$237$ 条带有编号步骤的解答轨迹，以及物理学家标注和独立多轮语言模型辩论标注。<br>
**输出**：三类轨迹：$130$ 条答案正确且推理无错误，$83$ 条答案错误，$24$ 条答案正确但推理含有错误；全部 $107$ 条错误轨迹同时具有错误存在标签和最早错误步骤标签。

</div>

**直观理解**：答案正确与推理正确是两道独立的问题。研究者不追问哪一步最影响最后结果，而只记录论证第一次变假的地方，从而避免把“最早失效点”和“最后导致错答的地方”混为一谈。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 监控条件设计与推理核验

八个监控模型分别在四级信息条件下工作：$BLIND$ 只看题目和轨迹；$HINT$ 额外看到被称为“不可信候选”的答案；$CERT$ 看到被声明为正确的答案，并被明确提醒正确答案不代表推理可靠；$REVISE$ 先作出盲判，再看到认证答案并允许修改。另设 $RCTRL$ 以区分“再次思考”的影响，并设逐步暴露且隐藏后续步骤的 $STEP$ 条件作为独立复合干预。

<div class="method-step__io" markdown="1">

**输入**：题目、完整编号轨迹、参考答案，以及监控器在前一条件下的判断（仅在需要时提供）。<br>
**输出**：每条完整轨迹的 $has\_error$、$first\_error\_step$ 和 $error\_confidence$；在 $STEP$ 下则得到各前缀的 $step\_has\_error$，任一步为正即判定整条轨迹有错。

</div>

**直观理解**：这相当于逐渐给检查员更多线索：先不给答案，再给一个未认证答案，最后告诉它答案确定正确。若性能只在最终答案错误时提升，就说明检查员主要是在对答案，而不是在读证明。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 指标计算与不确定性分析

主要计算平衡准确率，即错误轨迹召回率与干净轨迹特异性的平均值；同时计算精确定位 $L_0$，要求监控器既标记轨迹有错，又准确指出最早错误步骤。对错误轨迹进一步划分为提前、精确、滞后和漏检，并在错答轨迹与正确答案但错误推理的关键轨迹上分别计算召回率。

<div class="method-step__io" markdown="1">

**输入**：监控器的错误标记、错误步骤预测、置信度，以及参考标准中的三类轨迹标签。<br>
**输出**：各信息条件、各监控器及各轨迹类别上的检测与定位结果；通过按题目而非按轨迹进行的 $2000$ 次聚类自助法得到置信区间，并用八个监控器上的精确符号检验考察方向一致性。

</div>

**直观理解**：只看“报出了多少错误”会奖励一个凡事报警的监控器，因此研究同时要求它少误报，并检查它是否找到了真正的第一处错误。统计时把同一道题的三个解答绑在一起重采样，避免把它们错误地当成完全独立的数据。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文没有训练新的监控器或优化参数，而是对固定的八个监控模型进行提示式推理评估。模型在温度设为 $0$ 的条件下运行，Kimi K3 受其 API 限制使用温度 $1.0$ 且低思考强度；这些设置影响推理采样方式，但不是本文提出的训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双轴参考标注**

参考标准将最终答案正确性与推理错误定位作为两个独立标签。最早错误步骤定义为首次对题目、物理或数学、数值结果，或轨迹自身此前推理作出虚假断言的编号步骤；未证明但尚未被证明为假的合理断言不自动计错，探索后被放弃的方法也不自动计错。

> 直观理解：该模块防止把“最终答案错误”当成“推理中唯一的问题”。尤其是关键轨迹中，答案表面正确但中间已经出现错误，正是测试独立过程核验的核心材料。

**2. 四级答案信息阶梯**

$BLIND$、$HINT$、$CERT$ 和 $REVISE$ 构成逐级增加答案信息的条件链。$HINT$ 与 $CERT$ 的区别在于答案的认识论状态：前者要求监控器不信任答案，后者声明答案正确；$REVISE$ 进一步测量监控器在盲判后获得答案时的修订行为。

> 直观理解：把“看到答案”和“相信答案”分开，才能判断性能提升究竟来自答案本身，还是来自答案被赋予了可信身份。再次作答的控制条件则排除了单纯多想一次造成的提升。

**3. 检测—定位分离评估**

监控器输出二元的 $has\_error$ 和离散的 $first\_error\_step$，因此“正确报警”不等于“正确定位”。主要检测指标平衡准确率同时考虑 sensitivity 与 specificity；主要过程指标 $L_0$ 只有在报警且步骤完全正确时才计为成功，错误轨迹还按 early、exact、late、missed 四类分解。

> 直观理解：一个检查员可能知道“这份证明有问题”，却不知道问题从哪一步开始。分开报告这两种能力，可以避免把发现结论矛盾误报成真正的推理审计。

**训练与推理**

研究首先离线生成并标注解答轨迹，然后在推理阶段将相同题目与轨迹按条件提供给八个监控模型。完整轨迹条件要求模型以 JSON 返回 $has\_error$、$first\_error\_step$ 和 $error\_confidence$；$REVISE$ 会把该模型先前的盲判一并回放，再揭示认证答案并允许修改；$STEP$ 则逐步输入前缀，任一前缀被判错便标记整条轨迹，并以最早阳性前缀作为定位结果。所有有效解析结果按固定条件计算指标，跨条件的召回率比较使用四个条件均有有效输出的共同子集。

**复现信息**

数据构建从 $228$ 个物理细分类别题目开始，因图像接口限制仅保留文本题，再保留精确匹配题和需要多步推理的题目；经过试评估和标注阶段排除后得到 $79$ 道题。参考标准包含物理学家与独立语言模型辩论两条标注路径，来源隐藏后由主作者裁决；八个监控器排除了参与 AI 辩论标注的 GPT-5.5 和 Claude Opus 4.8，并额外保留完全留出的 Kimi K3。统计不确定性按 $79$ 道题进行聚类自助重采样，每次携带该题的全部三条轨迹，重复 $2000$ 次；因此置信区间反映题目抽样误差，不代表从所有可能监控模型中抽样所得的总体不确定性。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 物理题解轨迹数据：来自 $79$ 道 Humanity's Last Exam 物理题的 $237$ 条带有步骤编号的解答，由 $3$ 个前沿模型生成；数据中没有人为插入错误，用于检验真实模型推理中的自然错误。
- 关键轨迹子集：经物理学家标注、独立 LLM 辩论以及隐藏答案来源的裁决共同建立参考标准后，得到 $24$ 条“最终答案正确但轨迹含有真实错误”的轨迹，用于直接测试监控器是否能发现不影响最终答案的推理错误。
- 答案正确性与首个错误步骤标注：每条轨迹均独立标注最终答案是否正确以及第一个错误步骤的位置；该标注既支持错误检测，也支持更严格的错误定位评估。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**平衡准确率（balanced accuracy）**

对正确与错误类别分别计算召回率后取平均，用于避免类别不均衡时只偏向多数类。 （越高越好，表示监控器同时识别正确轨迹与错误轨迹的能力更强。）

</div>
<div class="metric-item" markdown="1">

**错误轨迹召回率（recall）**

在真实含有错误的轨迹中，被监控器标记为错误的比例；研究分别考察错误答案轨迹与关键轨迹。 （越高越好，但必须结合轨迹类型解释；关键轨迹上的高召回尤其代表发现不影响最终答案的过程错误。）

</div>
<div class="metric-item" markdown="1">

**首个错误精确定位率（exact first-error localization）**

监控器指出的首个错误步骤与参考标准中的第一个错误步骤完全一致的比例。 （越高越好；它比仅判断轨迹有无错误要求更精确，反映监控器是否真正定位了问题来源。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 从未核验答案到已认证答案的信息阶梯

<div class="result-value" markdown="1">

平均平衡准确率由 $0.637$ 升至 $0.796$，首个错误精确定位率由 $0.261$ 升至 $0.379$。

</div>

看到可信最终答案确实让监控器整体更容易判断轨迹是否有问题，也稍微提升了指出具体首个错误步骤的能力。但这两个总体指标不能单独证明监控器获得了更强的独立过程验证能力，因为答案本身可能直接提供了结论一致性线索。

<div class="result-source" markdown="1">

来源：Abstract；Section III Results, subsection III.1 Overview

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Certification raised mean balanced accuracy from 0.637 to 0.796, while exact first-error localization rose from 0.261 to 0.379.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 已认证答案对错误答案轨迹与关键轨迹的影响

<div class="result-value" markdown="1">

在错误答案轨迹上，错误召回率由 $0.653$ 升至 $0.951$；在关键轨迹上，错误召回率反而由 $0.521$ 降至 $0.438$。这一方向对全部 $8$ 个监控器都成立，问题自助抽样的 $95\%$ 置信区间为 $[+0.256,+0.506]$。

</div>

答案认证主要帮助监控器发现“结论明显错误”的轨迹，却没有帮助它发现“结论正确但论证错误”的轨迹，甚至使后者更难被标记。因而总体准确率上升不能解释为论证核查能力全面提升；更合理的解释是监控器在进行答案与推理结论的一致性检查。

<div class="result-source" markdown="1">

来源：Abstract；Section III Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Certification changed recall (the fraction of error traces flagged as erroneous) from 0.653 to 0.951 on wrong-answer traces but from 0.521 to 0.438 on critical traces; the contrast had the same direction for all 8 monitors (question-bootstrap 95% CI [+0.256, +0.506]).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 盲承诺后重新显示答案

<div class="result-value" markdown="1">

在此前被监控器放过的错误答案轨迹中，看到答案后有 $93.8\%$ 被新标记为错误；在此前被放过的关键轨迹中，只有 $18.0\%$ 被新标记为错误。

</div>

答案信息能强烈纠正“最终答案错误但先前未被发现”的漏检，因为答案与轨迹结论之间存在直接冲突；但它很少揭示最终答案正确时隐藏的论证错误。该结果进一步支持答案访问主要增强结论一致性检查，而非独立验证支持论证是否可靠。

<div class="result-source" markdown="1">

来源：Abstract；Section III Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

After blind commitment, monitors shown the answer newly flagged 93.8% of previously passed wrong-answer traces as erroneous, but only 18.0% of critical traces.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 样本范围有限：数据来自 $79$ 道 Humanity's Last Exam 物理题、$237$ 条轨迹和 $3$ 个前沿模型，其中关键轨迹只有 $24$ 条；因此结果能否推广到其他学科、任务、模型或更大规模的错误分布，原文未明确报告。
- 错误主要是普通且多数不影响最终结论的错误，而不是专门设计的对抗性或奖励劫持错误；因此研究支持“可信答案可能高估监控能力”的风险警示，但不能直接证明监控器在所有恶意、战略性或高负荷错误上都会表现相同。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 未核验答案条件：监控器只能依据题目与推理轨迹判断，用作近似独立过程验证的基线。
- 已认证答案条件：监控器可看到经过核验的最终答案，用于测量可信答案信息带来的性能变化。
- 盲承诺后再显示答案条件：监控器先在不知道答案时作出判断，随后获得答案并重新判断，用于区分答案信息带来的真正新发现与事后确认。
- 八个 LLM 监控器之间的横向比较：所有监控器在相同信息条件下评估轨迹，用于检验观察到的效应是否依赖单一监控模型。

**实验想回答的问题**

- 在监控模型获得未经核验、已认证或经盲承诺后揭示的最终答案时，答案信息是否提升其对推理过程的独立验证能力，还是主要帮助其检查推理结论是否与答案一致？
- 答案认证对错误答案轨迹与“答案正确但推理含有错误”的关键轨迹，是否产生不同的检测与首个错误定位效果？

**实验实现**

研究收集三类信息条件下的监控判断：答案未核验、答案已认证，以及监控器先盲目承诺判断后再看到答案。共有 $8$ 个 LLM 监控器对轨迹进行盲评或答案辅助评估。参考标准不直接依赖待测监控器，而是综合物理学家标注、独立 LLM 辩论和答案来源被隐藏后的裁决。实验重点比较信息阶梯上的总体识别能力、不同轨迹类型的错误召回，以及首个错误步骤的精确定位；原文未明确报告各监控器的具体模型名称、提示词和完整训练或推理配置。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 答案信息条件的逐级消融：未核验答案、已认证答案、盲承诺后显示答案 | 信息条件从无答案到认证答案时，平均平衡准确率为 $0.637\rightarrow0.796$，首个错误精确定位率为 $0.261\rightarrow0.379$；盲承诺设计进一步测量答案出现后对原判断的增量改变。 | 该设计隔离了“是否获得最终答案”这一核心变量，而不是简单比较不同模型。它表明答案在判断后出现时仍能改变大量对错误答案轨迹的判断，但对关键轨迹的改变很小，因此总体增益不能直接归因于更好的过程推理审查。 | Section III Results, subsection III.1 Overview；但所提供原文摘录为截断句，完整数值句见 Abstract<br><span class="experiment-evidence">Mean balanced accuracy rises monotonically along the information ladder, from</span> |
| 错误答案轨迹与关键轨迹的分层分析 | 认证条件下，两类轨迹的错误召回率分别为 $0.951$ 与 $0.438$；盲承诺后重新看到答案时，两类此前漏检轨迹的新标记比例分别为 $93.8\%$ 与 $18.0\%$。 | 这是对总体结果的决定性拆分：如果答案访问真正改善了过程验证，两类含错轨迹都应普遍受益；实际效果只集中在错误最终答案上，说明答案信息更像一个结论校验信号，而不是论证可靠性的独立证据。 | Abstract；Section III Results<br><span class="experiment-evidence">Certification changed recall (the fraction of error traces flagged as erroneous) from 0.653 to 0.951 on wrong-answer traces but from 0.521 to 0.438 on critical traces; the contrast had the same direction for all 8 monitors (question-bootstrap 95% CI [+0.256, +0.506]).</span> |

**定性案例**

- 关键轨迹的定性作用是展示“答案正确但推理不健全”的具体风险类别：监控器在看到正确答案后往往不会重新指出其中的普通、非承重错误。原文所提供材料未给出某一道题的完整逐步案例，因此不能据此概括某个具体物理错误或监控器的具体解释。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Evaluates LLM chain-of-thought monitors and shows that trusted answers improve conclusion checking rather than reliable verification of reasoning, with direct implications for AI oversight.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`02acccaf387f3bca1954168f7e25594c8d20b15783a24d6eba763b53766a07f5`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
