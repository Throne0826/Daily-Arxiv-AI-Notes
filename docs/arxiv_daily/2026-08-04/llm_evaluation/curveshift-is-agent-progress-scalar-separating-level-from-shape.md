---
title: "[论文解读] CurveShift: Is Agent Progress Scalar? Separating Level from Shape"
description: "[arXiv 2608.00355][LLM 评测] 本文质疑用单一分数概括大模型进步的充分性，并研究在扣除整体能力上升后，新模型是否仍对高难度任务表现出额外增益。"
arxiv_id: "2608.00355"
announcement_date: "2026-08-04"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:57:52.036105+00:00"
source_sha256: "64816e72b7443c9b55c5f77f838cf550bd722d12d867cb59d2d7c290f334d635"
tags:
  - "LLM 评测"
  - "LLM 其他"
  - "LLM Reasoning"
  - "项目反应理论"
  - "差异项目功能"
  - "语言模型评测"
  - "难度—成功率曲线"
  - "基准饱和"
  - "支架混杂"
  - "外生难度锚定"
  - "竞争性编程"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.00355</p>

# CurveShift: Is Agent Progress Scalar? Separating Level from Shape

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Hanwen Xing, Pengyun Wang, BingXu Meng, Kumail Alhamoud, Xiang Li, Jicheng Wang, Xin Yu, Xinyang Han, Xiaomin Li, Philip Torr, Yuexing Hao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> University of Southern California；University of Chicago；University of California, Berkeley；Massachusetts Institute of Technology；Stanford University；University of California, Davis；Pennsylvania State University；Harvard University；University of Oxford</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.00355v1) · [PDF 下载](https://arxiv.org/pdf/2608.00355v1) · **关键词** 项目反应理论, 差异项目功能, 语言模型评测, 难度—成功率曲线, 基准饱和, 支架混杂, 外生难度锚定, 竞争性编程<br>
**代码**: [https://github.com/harvenstar/CurveShift](https://github.com/harvenstar/CurveShift)

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

本文质疑用单一分数概括大模型进步的充分性，并研究在扣除整体能力上升后，新模型是否仍对高难度任务表现出额外增益。

**不用术语来说**：当新一代模型在困难题上的进步看起来比简单题更明显时，这不一定意味着模型获得了专门解决难题的新能力：简单题可能早已接近满分，继续提升的空间很小，而同样的整体能力增长自然会更多地反映在困难题上。研究者因此需要区分两种情况：整条表现曲线只是整体上移，还是曲线形状确实发生变化，使模型在困难题上的表现超过其简单题和中等题成绩所能预测的水平。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将“整体能力水平上升”与“难度—表现曲线的形状变化”明确分离，并指出既有观察中大部分所谓向困难任务迁移的增益，可以由单一潜在能力上升以及天花板效应、题目区分度差异解释，无须假定能力结构发生质变。
- 作者提出利用无智能体脚手架且具有外生难度排序的 LiveCodeBench 识别残余的困难题效应，从而避免模型版本与脚手架版本同步更新造成的归因混淆；同时将结论严格限定为竞争性编程中的短推理任务，而不外推到长时程自主智能体能力。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型能力评测与心理测量学交叉研究。现有排行榜平均解题率、METR 时间跨度以及统一潜在能力曲线通常把模型进步压缩成一个标量，但同样的总分增长可能来自两种不同变化：其一是所有难度上的整体能力水平上升，其二是增益特别集中于困难任务，使“难度—成功率曲线”的形状发生变化。本文借助项目反应理论比较这两者，并强调评测设计必须处理两个关键问题：难度最好由独立于待测模型的外部信息确定；在智能体基准中，模型与智能体支架往往同时更新，因而观测到的进步未必能归因于模型本身。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**项目反应理论（Item Response Theory, IRT）**

IRT 用潜在能力和题目属性解释答题成功概率，从而把模型总体水平与题目难度放在同一统计框架中。本文关心的不是只估计一个更高的能力值，而是检验能力与难度之间的关系是否随模型时代改变。

</div>
<div class="concept-item" markdown="1">

**Rasch 模型与二参数逻辑模型（2PL）**

Rasch 模型假设成功概率由模型能力与题目难度之差决定，并默认各题区分不同能力水平的方式相同；2PL 进一步允许题目的区分度不同。二者可作为“只有总体能力上升、曲线形状不变”的标量基准，并帮助判断表面的困难题增益能否由天花板效应和区分度解释。

</div>
<div class="concept-item" markdown="1">

**差异项目功能（Differential Item Functioning, DIF）**

DIF 指在控制总体能力后，同一类题目对不同群体或时代仍表现出系统性难易差异。本文采用广义的时代 DIF，检验 2024 年 9 月之后的模型是否在困难题上获得超出其简单题和中等题表现所预测的额外优势。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是跨发布日期模型在不同难度任务上的成败记录、模型所属时代，以及独立的任务难度排序；研究场景包括存在智能体支架的纵向评测和无支架的 LiveCodeBench 竞赛编程评测。输出是对两类变化的区分：总体潜在能力的标量上移，以及集中在困难题上的时代效应 $4\delta$4，即控制总体能力后难度—成功率曲线是否仍发生形状变化。基本假设是题目难度具有可比较的外部锚点；LiveCodeBench 的难度来自人类竞赛、先于模型评测确定，且模型直接根据题面生成代码，不经过工具调用循环或多步智能体支架。对于 METR 或 SWE-bench 一类智能体轨迹，模型时代与支架时代近乎共线，因此数据只能描述部署系统的变化，不能可靠地把困难任务上的额外收益分别归因于模型或支架；无支架基准用于消除这一混杂，但其结论范围仅覆盖竞争性编程和较短推理任务，不能直接推广到长时程自主智能体能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\theta_m$**

模型 $m$ 的潜在总体能力；其随模型代际上升表示难度—成功率曲线整体平移。

</div>
<div class="notation-item" markdown="1">

**$b_i$**

题目 $i$ 的难度；本文强调应尽可能使用独立于待测模型的外生难度排序。

</div>
<div class="notation-item" markdown="1">

**$a_i$**

题目 $i$ 的区分度，即该题对能力变化的敏感程度；Rasch 模型通常固定该项，而 2PL 允许其因题而异。

</div>
<div class="notation-item" markdown="1">

**$\delta$**

困难题上的时代效应：在控制总体能力水平后，后期模型相对早期模型在困难题上的额外对数优势，用于表示残余的曲线形状变化。

</div>

</div>

**直接相关的工作**

- **Kwa et al. (2025) 的 METR time-horizon metric**: 该工作以单一时间跨度及其倍增时间概括智能体能力的纵向进步，但不检验增益是否均匀分布于不同任务难度。本文将这种标量趋势作为待拆解对象，区分纯粹的能力水平上移与困难任务上的额外形状变化。
- **Schaeffer et al. (2023) 关于 emergent abilities 的度量分析**: 该工作指出所谓能力“涌现”的突跃可能由非线性或不连续指标造成，而非模型本身出现定性变化。本文把相同的测量批判应用于难度轴：先检验困难任务增益迁移能否由标量能力、天花板效应和题目区分度重现，再寻找控制这些因素后仍存在的残余效应。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

排行榜平均通过率、METR 时间跨度以及潜在能力估计通常把模型进步压缩为一个标量。这类指标便于比较和预测，却无法判断新增能力究竟均匀分布于各难度，还是主要集中在最困难任务上。该区别直接影响对能力前沿、突现能力和风险趋势的解释：若困难题增益只是简单题饱和后的统计现象，就不应被视为模型能力结构发生了质变；若扣除整体提升后仍存在稳定的困难题额外增益，则单一标量不足以描述模型进展。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **标量进展指标**：用平均解题率、时间跨度或随模型代际上升的单一潜在能力值概括总体表现。这些方法适合形成简洁的排行榜或增长趋势，但把不同难度题目上的表现变化汇总到同一个数值中。
- **项目反应理论模型**：Rasch 模型用模型的单一潜在能力与题目固定难度之间的差异预测成功概率；二参数逻辑模型进一步允许不同题目具有不同区分度。差异项目功能分析则检验在控制总体能力后，题目表现与难度之间的关系是否随模型时代改变。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 仅观察困难任务获得更大绝对增益，不能证明难度—表现曲线发生了形状变化。简单任务接近满分后存在天花板效应，因此单一能力水平上升也会产生“增益向困难题迁移”的外观；若不建立标量零假设，研究者容易把度量方式造成的现象误判为新能力。
- 在 METR、SWE-bench 等智能体评测中，新模型通常与新脚手架共同出现，而脚手架选择对成绩的影响可能与模型选择相当。模型时代与脚手架时代近乎共线，使困难题上的额外增益无法可靠归因于模型本身，也无法用这些轨迹单独识别模型原生能力的曲线形状变化。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种可识别的纵向设计，能够同时控制总体能力上升、题目难度和区分度，并排除智能体脚手架升级的影响，从而估计模型时代是否对困难题产生独立的额外作用。理想证据需要逐题结果、带日期的模型、独立于模型的难度排序以及无脚手架执行环境；公开基准很少同时满足这些条件。

</div>
<div markdown="1"><span>核心问题</span>

在以单一潜在能力上升作为零假设，并控制题目难度与区分度之后，2024 年 9 月以后发布的模型是否仍在最困难的竞争性编程题目上表现得显著优于其简单题和中等题成绩所能预测的水平？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是先用 Rasch 模型回答“仅靠整体能力上升会看到什么”，再把真实数据超过该预测的困难题表现视为候选的曲线形状变化。LiveCodeBench 要求模型直接根据完整题面生成代码，没有工具调用循环或多步脚手架，其竞赛来源又提供了不依赖任何被测模型的难度顺序。因此，简单题和中等题可以校准总体能力，最困难题相对该能力基线的剩余增益则更接近模型原生的难度特异效应，而不是评测基础设施同步升级的结果。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CurveShift是一套用于区分“能力水平整体上升”与“进步在困难任务上重新分布”的统计分析流程。输入是逐模型、逐题目的成功结果，以及独立于被评估模型给出的题目难度标签和模型发布日期；方法先用简单题与中等题估计每个模型的一维能力$\hat{\theta}_m$，再冻结该能力，仅在困难题上估计后推理时代带来的额外成功对数优势$\delta$。为避免困难题区分度与时代效应相互替代，困难题区分度$\alpha_{\mathrm{hard}}$不从同一批数据中自由拟合，而是在预设网格上固定，并通过按题目、竞赛或模型聚类的bootstrap评估不确定性。

直观地说，作者先根据简单题和中等题判断每个模型“总体有多强”，随后询问：若两个时代的模型具有相同的这项总体能力，新时代模型是否仍会在困难题上表现得更好？因此，$\delta$不是总分增长，也不是困难题原始正确率之差，而是扣除总体能力、逐题固有难度和假定区分度后，困难题响应曲线形状的剩余时代变化。该识别主要依赖无智能体脚手架的LiveCodeBench；METR与SWE-bench Verified中模型年代和脚手架年代同步变化，不能把困难任务收益明确归因于基础模型本身。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造带外生难度的逐题结果面板

将模型$m$与题目$i$组成结果矩阵，并以2024年9月发布的o1-preview为固定断点，定义$\mathit{post}_m$；同时根据人工标签定义困难题指示量$\mathit{hard}_i$。难度必须由人类完成时间、修复时间或竞赛难度预先给出，不能从同一批待评估模型的表现反推。

<div class="method-step__io" markdown="1">

**输入**：METR、SWE-bench Verified和LiveCodeBench的逐模型逐题结果，人工难度标签，以及模型发布日期；LiveCodeBench单元格还包含成功次数$k_{mi}$与尝试次数$n_{mi}$。<br>
**输出**：包含结果、尝试次数、外生难度、模型日期和时代标签的分析面板。

</div>

**直观理解**：这一步相当于先用与参赛模型无关的标准给题目分档，避免因为新模型做不出的题被自动称为“难题”而形成循环论证。固定历史断点则使问题成为对特定时代转变的回顾性比较。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 用非困难题估计并冻结能力水平

基于二项似然拟合项目反应模型，得到每个模型的能力估计$\hat{\theta}_m$，随后将其作为固定offset带入困难题分析。由于困难题不参与该估计，困难题中的时代残差不能再通过上调或下调$\theta_m$被吸收。

<div class="method-step__io" markdown="1">

**输入**：简单题和中等题上的$k_{mi}$、$n_{mi}$及逐题结果，不使用任何困难题结果。<br>
**输出**：仅由简单题和中等题确定的冻结能力向量$\{\hat{\theta}_m\}$。

</div>

**直观理解**：可以把简单题和中等题看作一把统一的“总体能力尺子”。先把尺子读数锁定，再观察困难题是否偏离这把尺子的预测。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在困难题上估计形状变化

仅对困难题拟合带逐题固定效应$c_i$的二项logistic模型，以$\delta$作为唯一自由的时代系数；分别在$\alpha_{\mathrm{hard}}\in\{0.55,0.83,1.00\}$下重复估计。$c_i$吸收每道题自身的难度，固定$\alpha_{\mathrm{hard}}$阻止区分度与$\delta$在似然中相互替代。

<div class="method-step__io" markdown="1">

**输入**：冻结的$\hat{\theta}_m$、困难题结果、后时代指示量$\mathit{post}_m$以及预先固定的困难题区分度$\alpha_{\mathrm{hard}}$。<br>
**输出**：每个固定区分度假设下的困难题时代效应$\hat{\delta}$。

</div>

**直观理解**：这一步比较的是总体能力相同时，新旧时代模型在同一道困难题上的系统差异。多组$\alpha_{\mathrm{hard}}$相当于主动改变对困难题“多能拉开强弱差距”的假设，检查结论是否依赖某个难以识别的设定。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 校准偏差并量化不确定性

对第一阶段估计能力所造成的小幅生成回归量偏差进行模拟校准，并使用1,500次聚类bootstrap构造区间；聚类单位依次包括题目、竞赛和模型，模型家族聚类则作为簇数很少时的更严格敏感性分析。不同聚类层级分别对应向新题目、新竞赛、新模型检查点或新模型家族推广时的不确定性。

<div class="method-step__io" markdown="1">

**输入**：各区分度设定下的原始$\hat{\delta}$、面板的聚类结构，以及第一阶段生成的能力回归量$\hat{\theta}_m$。<br>
**输出**：经校准的$\hat{\delta}$、聚类置信区间，以及针对不同推广目标的稳健性判断。

</div>

**直观理解**：同一道题或同一家族中的观测并非完全独立，普通标准误会显得过于确定。聚类重采样把相关观测成组移动，用来检验估计是否只是少数题目、竞赛或模型造成的。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 时代差异项目功能模型

$$
\operatorname{logit}p_{mi}=\theta_m-b_i+\delta\,\mathit{post}_m\mathit{hard}_i
$$

**符号说明**

- $p_{mi}$：模型$m$成功解决题目$i$的概率
- $\operatorname{logit}(p)$：成功概率$p$的对数优势，即$\log\!\left(p/(1-p)\right)$
- $\theta_m$：模型$m$的一维总体能力
- $b_i$：题目$i$的潜在难度；值越大，基准成功概率越低
- $\mathit{post}_m$：模型$m$是否在2024年9月断点当日或之后发布的二元指示量
- $\mathit{hard}_i$：题目$i$是否属于困难档的二元指示量
- $\delta$：后时代模型在困难题上的额外成功对数优势，即扣除总体能力与题目难度后的形状效应

<div class="equation-explanation" markdown="1">

**直观理解**：基础项$\theta_m-b_i$表达“模型越强、题目越容易，成功率越高”。交互项只在模型属于后时代且题目属于困难档时生效，因此$\delta>0$表示后时代模型对困难题的提升超过其总体能力所能解释的水平；但该式若直接联合估计，仍可能把困难题信息吸收到能力中，所以作者进一步采用锚定流程。<br>
**原文位置**：第3.2节，公式(2)，Era-DIF model

</div>

</div>

<div class="equation-block" markdown="1">

#### 冻结能力的锚定困难题模型

$$
\operatorname{logit}p_{mi}=\alpha_{\mathrm{hard}}\hat{\theta}_m+c_i+\delta\,\mathit{post}_m
$$

**符号说明**

- $p_{mi}$：模型$m$在困难题$i$上的成功概率
- $\hat{\theta}_m$：仅用简单题和中等题估计并随后冻结的模型$m$能力
- $\alpha_{\mathrm{hard}}$：困难题对能力差异的区分度缩放系数，在拟合前固定而非由该模型估计
- $c_i$：困难题$i$的逐题固定效应，用于吸收其独有的基础难度
- $\mathit{post}_m$：模型$m$是否属于固定断点后的时代
- $\delta$：给定冻结能力、固定区分度和同一道题后，后时代相对于前时代的困难题对数优势

<div class="equation-explanation" markdown="1">

**直观理解**：这是CurveShift最终用于识别形状效应的核心模型。$\hat{\theta}_m$已经由非困难题确定，$c_i$让比较发生在同一道题内，$\alpha_{\mathrm{hard}}$又被外部固定，所以剩余的系统性时代差异集中到$\delta$；通俗地说，它是在锁住“模型有多强”“题本身多难”和“困难题多会区分强弱”之后，再比较新旧时代。<br>
**原文位置**：第3.2节，公式(3)，anchored 2PL sensitivity design的Step 2

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文不是训练语言模型，而是对既有模型评测结果进行统计估计。第一阶段在简单题和中等题上最大化连续二项似然：每个单元格将成功次数$k_{mi}$视为$n_{mi}$次尝试中的二项计数，由此估计能力$\hat{\theta}_m$及相应题目参数；第二阶段把$\hat{\theta}_m$作为固定offset，在困难题上、给定$\alpha_{\mathrm{hard}}$时最大化同类二项似然，估计逐题固定效应$c_i$和时代系数$\delta$。使用$n_{mi}$保留了不同单元格的已知采样精度；作者没有把多次尝试简单二值化为pass@1，因为困难题低基准成功率下的二值化会压低测得的区分度。这里的优化目标是获得可解释的结构参数与不确定性，而非通过反向传播更新被评估模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 外生难度与无脚手架识别模块**

方法要求题目难度排序在被评估模型之外形成，并优先使用直接代码生成、没有智能体脚手架的LiveCodeBench。METR和SWE-bench Verified可展示不同难度段的表面趋势，但由于较新模型通常搭配较新脚手架，时代效应同时混合了基础模型和执行系统变化，不能作为核心因果归属依据。

> 直观理解：若模型和辅助工具同时升级，困难任务变好后无法知道是谁起作用。LiveCodeBench让所有模型直接生成代码，因此至少移除了“新版模型配新版工具”这一关键混杂。

**2. 水平与形状分解模块**

“水平”由简单题和中等题估计的标量能力$\hat{\theta}_m$表示；“形状”由冻结该能力后，后时代模型在困难题上的额外对数优势$\delta$表示。逐题固定效应$c_i$进一步控制同一困难档内部各题的固有难度差异。

> 直观理解：总能力提高会自然地让更多困难题越过可解阈值，看起来像进步偏向困难题。先固定总体能力后仍存在的困难题差异，才是本文所称的曲线形状变化。

**3. 锚定区分度敏感性模块**

自由二参数logistic模型中的题目区分度和时代差异项在当前数据上近似混叠，联合极大似然会随初始化改变并可能使$\delta$反号。因此作者不报告自由2PL控制，而固定$\alpha_{\mathrm{hard}}$并在$0.55$、$0.83$和$1.00$上重估，其中$1.00$表示困难题与其他题具有相同区分度。

> 直观理解：区分度和时代效应都能让强模型在困难题上显得更突出，数据不足以可靠判断应把变化分给哪一个。作者把区分度当作外部假设逐项扫描，使读者能够看到时代效应在不同假设下如何变化。

**训练与推理**

完整估计程序如下：先以模型发布日期生成$\mathit{post}_m$，以人工标签生成难度分组；随后排除困难题，仅用简单题和中等题的二项结果拟合能力$\hat{\theta}_m$。接着只保留困难题，在一个给定的$\alpha_{\mathrm{hard}}$下，将$\alpha_{\mathrm{hard}}\hat{\theta}_m$作为固定预测项，联合估计$c_i$与$\delta$；对区分度网格逐点重复这一过程，并对生成回归量偏差作校准。最后按目标推广单位进行聚类bootstrap，并通过替代锚点、家族控制、日期与断点扰动、连续时间、竞赛来源拆分及污染过滤等规格重新估计。

对新数据应用时，需要同样具备逐题结果、模型日期和独立难度标签，并保证用于能力锚定的简单与中等题覆盖足够多的模型。输出不是单个模型的预测标签，而是一条敏感性曲线$\hat{\delta}(\alpha_{\mathrm{hard}})$及其区间：它说明在不同困难题区分度假设下，后时代是否存在无法由总体能力上升解释的额外困难题收益。

**复现信息**

公平复现所需的关键数据设置是：LiveCodeBench面板包含66个有日期的模型和1,055道题，按人工标签分为322道简单题、383道中等题和350道困难题；每个单元格记录$k_{mi}$与$n_{mi}$，多数普通模型每题尝试10次，而多数推理模型仅尝试1次。该尝试次数与时代相关，因此必须采用计数二项似然并在真实$n_{mi}$结构上检查估计偏差，不能把等权拟合或单次抽样直接当作无偏对照。时代断点固定为十进制年份2024.70，即2024年9月的o1-preview发布时点。

核心规格应逐点固定$\alpha_{\mathrm{hard}}\in\{0.55,0.83,1.00\}$，而不是自由联合估计2PL区分度；主文把$\alpha_{\mathrm{hard}}=1.00$作为等区分度的保守设定，$0.83$对应连续似然下经去偏的区分度估计，$0.55$对应困难题二值化可能产生的区分度压低情形。不确定性使用1,500次聚类bootstrap；题目、竞赛、模型和模型家族聚类回答不同的总体推广问题，尤其家族层面只有11个簇，区间应解释为低功效的敏感性结果。原文还说明第一阶段能力是生成回归量，会带来小幅正偏，因此主估计需要按附录A.4所述模拟校准；仅凭当前节选无法完整复现该校准模拟的生成参数与计算细节，必须回查附录和公开代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- METR TH1.0 时间跨度数据：任务来自 HCAST、RE-Bench 和 SWAA，由人类专家按预计完成时间划分难度区间。实验把完成时间桶作为外生难度变量，用于检验“能力提升似乎更偏向困难任务”的现象能否仅由统一的 Rasch 难度—能力模型和容易任务的天花板效应解释。原文节选未给出该版本的任务总数、模型数及各难度区间规模。
- SWE-bench Verified：包含 $500$ 个软件工程实例，人工修复时长分为少于 $15$ 分钟、$15$ 至 $60$ 分钟、$1$ 至 $4$ 小时和超过 $4$ 小时四档；作者从公开实验仓库收集 $134$ 个模型提交的逐实例解决结果，并由提交目录恢复模型日期。它用于检查困难任务效应能否在另一项智能体软件工程基准中复现，同时展示脚手架年代与模型年代共线、困难样本尾部较薄所造成的识别限制。
- LiveCodeBench Difficulty Panel：作者整理 $66$ 个有发布日期的模型在 $1{,}055$ 道竞赛编程题上的逐题结果，其中容易、中等、困难题分别为 $322$、$383$、$350$ 道，汇总通过率分别为 $0.83$、$0.45$、$0.18$。每个模型—题目单元记录成功次数 $k_{mi}$、尝试次数 $n_{mi}$、人工难度标签和模型发布日期；多数模型每题尝试 $10$ 次，推理模型尝试 $1$ 次。该基准直接生成代码且不使用智能体脚手架，题目原始竞赛日期还提供一定的抗污染性，因此是区分模型能力变化与脚手架升级的核心识别数据。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**困难题额外效应（logit）**

衡量在总体能力以及容易、中等题表现已经被模型解释后，推理时代之后的模型在困难题上的额外对数胜算增量；$0$ 表示没有曲线形状变化，正值表示困难题表现高于统一能力提升所预测的水平。 （若研究目标是寻找困难任务上的额外进步，则数值越高表示该效应越强；但它不是综合性能分数，也不能脱离不确定性和识别假设单独解释。）

</div>
<div class="metric-item" markdown="1">

**题目通过率**

模型在给定难度题目上的成功比例；LiveCodeBench 的单元结果来自成功次数 $k_{mi}$ 与尝试次数 $n_{mi}$。论文用困难题通过率的变化把 logit 效应转换成更直观的实际成功概率。 （越高表示在该难度组中成功生成正确程序的概率越大，但容易题接近上限时，该指标可能因天花板效应而低估进一步能力增长。）

</div>
<div class="metric-item" markdown="1">

**困难题残差或年代交互效应**

比较困难题实际结果与仅由总体能力、题目难度及非困难题表现所预测结果之间的差异，用来检测难度—表现曲线是否改变形状，而不只是整体水平平移。 （显著为正且在合理控制下保持稳定，才支持困难题存在额外增益；接近 $0$ 则更符合统一标量能力增长。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### METR TH1.0：用形状固定、仅能力水平上升的单一 Rasch 模型解释分难度增益

<div class="result-value" markdown="1">

作者报告，原本看似“进步转向更困难任务”的主要部分，可由统一 Rasch 模型重现，因此大体来自容易任务的天花板效应，而不要求假设能力曲线发生质变。

</div>

这说明按难度直接比较通过率增量容易产生错觉：容易题已经接近满分时，新能力没有足够空间表现，而困难题仍有提升空间。该结果否定的是把全部困难题增益都解释成新型能力的做法，并不否定后续可能存在较小的真实曲线形状变化。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On METR time-horizon data, a single Rasch model with rising ability reproduces this pattern, so it is largely explained by ceiling effects rather than a qualitative change in capability.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### LiveCodeBench：控制总体能力后比较 $2024$ 年 $9$ 月之后模型的困难题表现

<div class="result-value" markdown="1">

在作者称为最保守的假设下，后期模型仍有约 $+0.40$ logit 的困难题额外效应，对应困难题通过率约从 $18\%$ 提升到 $25\%$。

</div>

容易题和中等题所反映的整体能力增长不足以完全预测困难题提升，因此数据支持竞争性编程中的难度—表现曲线存在小幅但实质性的形状变化。该数值只识别 LiveCodeBench 上部署模型能力的变化，不能直接推广到所有推理、数学或长时自主任务。

<div class="result-source" markdown="1">

来源：摘要；正文第 5 节结果由第 6 节引用

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

After accounting for the rise in overall ability, models released after September 2024 still gain on the hardest problems beyond what their easy and medium performance predicts, by about +0.40 logits under our most conservative assumption, raising the hard-problem solve rate from roughly 18% to 25%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 无脚手架的 LiveCodeBench 与存在年代共线性的 METR、SWE-bench Verified 对照

<div class="result-value" markdown="1">

LiveCodeBench 通过取消智能体脚手架，使困难题年代效应能够归因于部署模型能力，包括模型原生的推理时计算，而不是外部执行框架升级。

</div>

这一结果主要解决因果归因而非效应大小问题：在智能体基准上，即使困难题效应方向相同，也无法判断收益来自模型还是工具链；LiveCodeBench 排除了这一特定混杂因素。不过，它仍不能排除训练数据、模型家族构成或其他随年代变化的模型侧因素。

<div class="result-source" markdown="1">

来源：第 6 节“Only a no-scaffold benchmark separates capability from scaffold”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The hard-item era effect on LiveCodeBench isolates deployed model capability, including native inference-time reasoning, from the contribution of any harness.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 干净识别主要依赖单一竞争性编程基准 LiveCodeBench。作者明确把结论限定在竞争性编程，不能据此断言数学推理、通用智能体能力或长时自主任务也出现同样的曲线形状变化。
- 智能体基准中较新模型几乎总与较新脚手架绑定，缺乏跨年代、同脚手架的充分重叠；SWE-bench 还存在困难样本尾部较薄的问题。因此这些数据只能说明方向相似，无法独立确认模型能力的因果贡献。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 单一 Rasch 模型：仅允许模型能力随年代上升，同时保持共同的难度—响应曲线形状不变。它是关键零假设，因为若该模型已能重现“增益向困难任务移动”的表象，就说明该表象可能只是容易任务接近满分后的天花板效应，而非能力结构发生变化。
- 由容易题和中等题表现预测困难题表现：先用非困难题刻画总体能力水平，再考察困难题的实际表现是否高于该预测。这个比较直接对应论文所称的困难题残差，可把“整体都变强”与“困难题额外变强”分开。
- METR 与 SWE-bench Verified 的智能体评测结果：两者用于比较困难题效应的方向是否跨基准一致，但不能作为干净的模型能力归因基线，因为较新的模型通常同时配有较新的执行脚手架。
- 推理时代之前与之后的模型年代分组：论文以 $2024$ 年 $9$ 月为断点比较两个时期。在控制总体能力后，年代项是否仍能解释困难题表现，是判断曲线形状是否改变的核心比较。

**实验想回答的问题**

- 在控制模型总体能力水平上升后，不同年代模型的难度—表现曲线是否仍发生形状变化，即新模型是否在困难任务上获得超出容易、中等任务所能预测的额外增益？
- 观察到的困难任务额外增益究竟来自模型自身能力，包括模型原生的推理时计算，还是来自随模型年代同步升级的智能体脚手架或评测流程？

**实验实现**

评测以逐模型、逐题或逐难度桶结果为基础，而不是只比较单个总分。METR 分析先用能力上升但曲线形状固定的 Rasch 模型检验天花板效应；SWE-bench Verified 按人工修复时长分层；LiveCodeBench 则利用外生的容易、中等、困难标签，并根据每个单元的 $k_{mi}/n_{mi}$ 建模。核心比较是在控制总体能力后，估计 $2024$ 年 $9$ 月之后模型的困难题额外效应。识别上，作者把无智能体脚手架的 LiveCodeBench 作为主证据，因为 METR 和 SWE-bench 中模型年代与脚手架年代同步变化。节选未提供完整回归式、置信区间计算方式、优化器、软件版本或随机种子，因此这些实现细节需回查原文与代码。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 在 METR 最困难难度带中，仅保留跨越两个年代、使用同一脚手架的运行结果 | 限制到同一脚手架后只剩 $1$ 个推理时代之后的模型，而且该模型本身并未接受推理训练，样本不足以区分模型年代效应与脚手架年代效应。 | 这个限制性分析试图固定脚手架，从而单独观察模型升级；但固定后几乎没有跨年代覆盖，说明智能体数据缺乏所需的重叠支持。它不是“没有模型效应”的证据，而是表明 METR 无法可靠识别效应来源。 | 第 6 节“Only a no-scaffold benchmark separates capability from scaffold”<br><span class="experiment-evidence">In the hardest band, if we restrict to a single scaffold that spans both eras, only one post-era model remains, and that model is not itself trained for reasoning.</span> |
| 将困难题效应从 METR 扩展到 SWE-bench Verified | SWE-bench Verified 上的困难题效应方向为正，但未达到统计显著；同时受到困难题尾部样本较少以及脚手架年代共线的影响。 | 该对照检验效应方向是否跨智能体软件工程基准复现。正方向提供弱一致性，但不显著且识别条件较差，不能作为独立确认，更不能把效应明确归因于模型自身。 | 第 6 节“Only a no-scaffold benchmark separates capability from scaffold”<br><span class="experiment-evidence">Its directional hard-item effect is positive but not statistically significant, and it suffers from both a thin hard tail and its own scaffold era collinearity, especially because agentic and agentless solution procedures can themselves change SWE-bench outcomes (Yang et al., 2024; Xia et al., 2025).</span> |

**定性案例**

- 论文比较了不同候选基准为何不能替代 LiveCodeBench：CodeElo 与其共享 Codeforces 来源，LiveBench 缺乏干净的外生逐题难度，BigCodeBench 缺少同样的有日期、无脚手架面板，Omni-MATH 则未公开跨有日期模型的逐题矩阵。这个案例说明识别曲线形状变化需要同时具备模型日期、逐题结果、外生难度和无智能体脚手架四项条件，而不只是另找一个高难度基准。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops an evaluation analysis that separates overall model ability from changes in performance across task difficulty and releases a dated coding-benchmark panel.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`64816e72b7443c9b55c5f77f838cf550bd722d12d867cb59d2d7c290f334d635`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
