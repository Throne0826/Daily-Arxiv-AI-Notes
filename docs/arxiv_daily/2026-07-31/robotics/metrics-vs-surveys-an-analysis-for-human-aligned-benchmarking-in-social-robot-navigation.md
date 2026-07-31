---
title: "[论文解读] Metrics vs Surveys: An Analysis for Human-Aligned Benchmarking in Social Robot Navigation"
description: "[arXiv 2510.02941][机器人 / 具身智能] 本文研究社会机器人导航中的数值指标与人类问卷评价之间是否存在稳定关联，以筛选更接近人类感知的指标子集，作为正式用户调查之前的初步基准工具。"
arxiv_id: "2510.02941"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.352253+00:00"
source_sha256: "5bdfdff25077746c1d29e7dc0496ecfe68cd5341be9172d24a2520bc3abcc057"
tags:
  - "机器人 / 具身智能"
  - "社会导航"
  - "人本感知导航"
  - "定量评测指标"
  - "参与者问卷"
  - "人机评价对齐"
  - "相关性分析"
  - "移动机器人"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2510.02941</p>

# Metrics vs Surveys: An Analysis for Human-Aligned Benchmarking in Social Robot Navigation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Trepella, Stefano, Martini, Mauro, Pérez-Higueras, Noé, Ostuni, Andrea, Caballero, Fernando, Merino, Luis, Chiaberge, Marcello</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2510.02941) · [PDF 下载](https://arxiv.org/pdf/2510.02941) · **关键词** 社会导航, 人本感知导航, 定量评测指标, 参与者问卷, 人机评价对齐, 相关性分析, 移动机器人<br>
**代码**: [https://github.com/PIC4SeR/Social-Nav-Metrics-Matching](https://github.com/PIC4SeR/Social-Nav-Metrics-Matching)

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

本文研究社会机器人导航中的数值指标与人类问卷评价之间是否存在稳定关联，以筛选更接近人类感知的指标子集，作为正式用户调查之前的初步基准工具。

**不用术语来说**：机器人在人群中移动时，不仅要避免碰撞和快速到达目的地，还应让人感到舒适、行为容易预测，并尊重个人空间。运行时间、路径长度等数值容易自动计算，却未必能反映人的真实感受；问卷更能直接衡量这些感受，但组织真实参与者实验的成本高、耗时长，也难以在不同系统之间重复和比较。因此，需要判断自动计算的指标能否在一定程度上代替或补充人工评价。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出联合分析数值导航指标与人类问卷指标的框架，通过聚类和统计检验考察二者的关联，并筛选具有代表性的数值指标子集。
- 作者识别出更接近人类评价趋势的数值指标组合，并发布包含八类真实社会场景、机器人与行人轨迹、精确真值及问卷评价的数据集，为后续指标开发和基准测试提供资源。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

社会导航（亦称人本感知导航）研究移动机器人如何在人群环境中到达目标，同时避免碰撞并遵守人类对舒适性、可预测性、个人空间和社会可接受性的期待。其评估包含两类互补信号：一类是由机器人与行人轨迹计算的时间、路程、人际距离、社会力等定量指标，成本低、可重复且便于跨方法比较；另一类是参与者问卷给出的主观评价，更接近真实人类感受，但采集昂贵、耗时且难以规模化。当前关键问题不是缺少指标，而是缺少证据说明哪些定量指标确实与人类判断一致，以及能否用一组较小且有代表性的指标支持标准化初步评测。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**社会导航**

机器人不仅要高效、安全地移动，还要以人类容易理解和接受的方式与行人共享空间。例如，即使一条路线不会发生碰撞，若机器人过度靠近行人或运动难以预测，仍可能被认为不合适。

</div>
<div class="concept-item" markdown="1">

**近体学**

近体学研究人在社会互动中如何使用和感受空间距离；在机器人评测中，它常被转化为机器人与行人间距、侵入个人空间的时间或次数等指标。这类指标能描述物理接近程度，但未必完整反映舒适性和意图可读性。

</div>
<div class="concept-item" markdown="1">

**社会力模型**

社会力模型把行人的避让、趋向目标及相互排斥等行为抽象为类似“力”的数学量，并可据此计算机器人运动对人的社会影响。它综合位置、速度和运动方向，但这些模型量是否对应人的主观感受仍需通过问卷数据验证。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文考察真实机器人与人类参与者共同出现的八类社会场景。对每次实验，一方面从机器人和人员的真实轨迹中计算定量指标集合 $QM$，另一方面通过参与者问卷获得人类评价集合 $HM$；随后分析两类评价之间的相关关系，并寻找最具代表性的定量指标子集 $QM^*$。目标输出不是新的导航策略，而是一套联合分析框架及候选指标子集，用于判断现有客观指标能够解释哪些人类感受、遗漏哪些主观因素，并在无法开展大规模问卷时为人本一致的初步基准测试提供依据。该设定默认轨迹具有可靠真值、问卷能够表达参与者感受，且统计相关性用于揭示一致趋势，而不等同于证明定量指标与主观判断之间存在因果关系。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$QM$**

由机器人和人员轨迹计算得到的定量社会导航指标集合。

</div>
<div class="notation-item" markdown="1">

**$HM$**

由参与者问卷提供的人本或主观评价指标集合。

</div>
<div class="notation-item" markdown="1">

**$QM^*$**

通过聚类与统计分析筛选出的、与人类评价趋势最相关的代表性定量指标子集。

</div>

</div>

**直接相关的工作**

- **Gao and Huang [5]**: 该综述整理机器人遵守社会规范的量化方法，包括人际距离、对共处者造成的不适以及路径的社会可接受性，为本文所分析的定量指标类别提供直接背景；本文进一步检验这些客观量是否与问卷中的人类判断一致。
- **Mavrogiannis et al. [12]**: 该工作系统分析社会导航算法的评估挑战，说明仅考虑路径规划与避障不足以覆盖舒适性、可预测性等社会属性；本文针对其中的客观指标与主观评价对齐问题进行实证相关性分析。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

社会机器人导航的质量不能只由是否到达目标、耗时或路程决定，还涉及舒适度、可预测性、个人空间和行为可理解性等主观因素。部署方需要一种可重复、可扩展的评估方式，在大量算法或实验方案中先筛查明显不合适的系统，同时保留人类参与者调查作为最终验证手段。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **轨迹驱动的定量指标**：从机器人和行人的运动轨迹中计算时间、距离以及社会导航相关的数值量，再用这些指标比较不同导航方法。其优势是计算方便，尤其适合受控实验和批量评测。
- **基于参与者问卷的人类中心评价**：让真实参与者观察或经历机器人的导航行为，并通过问卷报告舒适、安全、可预测或易理解等主观感受。这类评价直接来源于人类判断，因此被作者视为最终验证的标准。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有定量指标数量多且可能给出相互对照甚至难以解释的信号，社区也尚未形成一组能够可靠刻画舒适度或行为可理解性等社会属性的标准指标；其后果是研究者难以仅凭完整指标集合清楚判断一次实验的总体质量。
- 问卷能够提供信息丰富的人类感知评价，但成本高、耗时、难以扩展，并且跨实验或跨系统的复现与比较较困难；其后果是问卷不适合作为大规模算法迭代和初步筛选的唯一评估方式。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未明确哪些可自动计算的社会导航指标与人类问卷判断存在足够稳定且可解释的对应关系，也缺少一种系统方法从众多指标中选出能代表人类评价趋势的紧凑子集。与此同时，现有数值指标仍不能充分表达复杂或部分可接受场景中的主观体验，因此这种对应关系的适用边界也需要被识别。

</div>
<div markdown="1"><span>核心问题</span>

在真实机器人和人类参与者实验中，能否通过数值导航指标与问卷评价的联合分析，找出一个代表性指标子集，使自动化评测的分组或评分趋势与人类判断一致到足以支持社会导航算法的初步基准筛选？

</div>
<div markdown="1"><span>作者直觉</span>

如果人类感到不舒适或认为机器人行为难以预测，这些感受往往会在轨迹中留下可测痕迹，例如机器人与人的相对运动关系或导航行为模式发生变化。作者因此先用聚类观察不同实验在数值指标空间中的自然分组，再用统计分析检查各指标与问卷评价的联系；筛除无关或重复指标后，保留下来的组合可能比把所有指标简单堆在一起更清楚地呈现接近人类判断的趋势。不过，这是作者用于构建辅助基准的出发点，并不意味着数值指标可以取代问卷。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是训练一个新的导航策略，而是建立一套“数值指标能否复现人类判断”的评估流程。输入是在真实实验室中采集的机器人—行人轨迹及参与者对同一批轨迹的问卷评分；作者先计算并归一化十一项定量指标（QM）和四项人本指标（HM），再分别在两个特征空间中对实验进行无监督 $K$-means 聚类，通过轮廓系数选择聚类数，并以调整兰德指数（ARI）衡量两种分组的一致性。作者还穷举非空 QM 子集，寻找最接近 HM 分组的指标组合，并用 Spearman、Kendall 与 Kruskal–Wallis 非参数检验验证单项指标与人类感知之间的关系。
直观地说，研究先让“仪器”和“人”分别给同一组机器人行为打分，再检查两者是否会把相似行为归到同一类，以及哪些机器指标最接近人的判断。其输出不是一个可部署的控制器，而是候选的人类对齐基准指标集合，以及对现有指标覆盖范围和缺口的诊断。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 采集真实社会导航轨迹

机器人在 VICON 覆盖的实验室中自主导航，系统同步记录机器人和行人的位置、速度与轨迹；每个场景执行三次采用不同控制设置的运行，以产生社会顺应程度不同的行为。机器人速度统一限制为线速度 $v\in[0.0,0.6]$ m/s、角速度 $\omega\in[-1.5,1.5]$ rad/s，部分控制器额外加入高斯行人代价图或社会功代价。

<div class="method-step__io" markdown="1">

**输入**：八类社会交互场景、Jackal 移动机器人、行人、四种实验地图以及不同配置的局部规划控制器。<br>
**输出**：覆盖 Passing、Overtaking、Crossing 1–3、Narrow turn、Mixed 和 Curious person 的 $24$ 次真实机器人实验轨迹。

</div>

**直观理解**：这一步有意让同一情境中的机器人表现得有好有坏，从而形成可被人和指标共同区分的测试样本。真实机器人和真实行人减少了纯仿真中运动过于理想化的问题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造定量指标与人本评分

从轨迹计算十一项 QM：到达时间、路径长度、累计航向变化、平均机器人线速度、社会功及其每秒值、距最近行人的平均最小距离，以及亲密、个人、社交、公共空间占用比例。与此同时，$70$ 名参与者使用五点 Likert 量表独立评价不打扰性、友好性、平滑性和预见避障能力；Curious person 场景因行人主动干扰机器人而不收集不打扰性评分。

<div class="method-step__io" markdown="1">

**输入**：机器人—行人轨迹，以及由这些轨迹生成的俯视二维动画。<br>
**输出**：同一批 $24$ 个实验对应的 QM 特征矩阵和 HM 特征矩阵。

</div>

**直观理解**：QM 是从运动数据自动算出的“机器视角”，HM 是观看相同行为后得到的“人类视角”。二维动画突出速度、相对距离和轨迹形状，但不能再现人与实体机器人共享空间时的心理压力。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 统一量纲并分别聚类

作者在每个场景内部把各 QM 线性缩放到 $[0,1]$，并根据指标语义统一“越好越接近 $1$”的方向；HM 通过除以 $5$ 缩放到 $[0,1]$。随后在 QM 与 HM 特征空间中分别执行无监督 $K$-means，并在 $K\in[2,5]$ 范围内使用轮廓系数考察组内紧密性和组间可分性。

<div class="method-step__io" markdown="1">

**输入**：量纲和取值方向不同的 QM，以及五点量表形式的 HM。<br>
**输出**：基于数值指标和基于人类评分的两套实验聚类标签，以及各候选 $K$ 的轮廓系数。

</div>

**直观理解**：归一化相当于先把秒、米、弧度和问卷分数换到同一把尺子上，否则数值范围大的指标可能不合理地主导聚类。分别聚类则避免直接用人类标签监督模型，使测试关注 QM 自身是否自然呈现出人类所见的行为结构。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 筛选并统计验证人类对齐指标

作者将 HM 聚类视为参照，以 ARI 比较 QM 与 HM 对同一批实验的分组，并对十一项 QM 的全部 $2^{11}-1=2047$ 个非空组合重复计算；每项指标的累计 ARI 是包含该指标的组合所获 ARI 之和。进一步使用 Spearman 秩相关和 Kendall 秩相关检查单项 QM 与 HM 的单调关联，再用 Kruskal–Wallis H 检验判断指标能否区分三种运行行为水平。

<div class="method-step__io" markdown="1">

**输入**：HM 聚类标签、QM 聚类标签、所有 QM 非空子集及逐实验的 QM/HM 数值。<br>
**输出**：高 ARI 的 QM 子集、各指标的累计 ARI 相关性排序、显著的 QM–HM 单项关联，以及对不充分指标的诊断。

</div>

**直观理解**：子集搜索回答“最少保留哪些机器指标，才能最像人的整体分组”；单项相关回答“哪个指标对应哪一种具体感受”；组间检验则回答“该指标能否稳定区分不同控制行为”。三类证据相互补充，避免只凭一次聚类结果决定基准。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 社会功

$$
SW = W_r + \sum_i W_{p,i}
$$

**符号说明**

- $SW$：机器人在一条实验轨迹上的总社会功，用于表征机器人自身受到的社会/障碍作用以及机器人对周围行人造成的社会影响。
- $W_r$：沿轨迹累积的机器人社会力与机器人障碍力模长之和；相应作用力来自社会力模型。
- $W_{p,i}$：机器人对第 i 名行人产生的社会力模长沿轨迹的累积值，仅考虑机器人周围最大 5 米范围内的行人。
- $i$：机器人附近行人的索引。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把“环境和他人对机器人造成的交互负担”与“机器人对每名行人造成的扰动”相加；数值越大，按社会力模型解释，机器人对原有人群运动的社会影响通常越强。论文同时使用整段轨迹的总量 $SW$ 和按时间平均的 $SW_s$，以区分总扰动与单位时间扰动。<br>
**原文位置**：Section III-C, Quantitative metrics

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文是数据采集与评估协议研究，没有可学习参数、损失函数或基于梯度的训练目标；$K$-means 仅在给定特征空间内最小化样本到所属簇中心的组内距离，用于发现结构，而不是训练导航控制器。指标选择的分析目标是提高 QM 聚类与 HM 聚类之间的 ARI，并通过秩相关和组间显著性检验确认这种一致性不是单一分析方法的产物。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双视角特征构造**

QM 同时覆盖传统导航效率、运动几何和社会交互：前者包括 $TTG$、$PL$、$CHC$ 和 $ARV$，后者包括 $SW$、$SW_s$、$AMD$ 及四个近体空间占用比例。HM 则将人类判断分解为 $UO$、$FL$、$SM$ 和 $AF$，使自动指标可以分别与不打扰性、友好性、平滑性和预见避障能力比较。

> 直观理解：只看是否快速到达会漏掉靠人太近或迫使行人让路等问题，而只看距离又可能漏掉效率和运动节奏，因此需要同时保留导航与社会两类描述。HM 的四个维度也防止把“人觉得好”压缩成一个含义不清的总分。

**2. 无监督聚类一致性分析**

作者在 QM 和 HM 空间独立执行 $K$-means，用轮廓系数评估每个空间内部的聚类结构，再以 ARI 比较两套标签；ARI 会校正随机一致性，因此比直接计算标签相等比例更适合比较编号任意的聚类。通过穷举 QM 子集并累计每项指标参与组合时的 ARI，方法既寻找最佳组合，也估计单项指标对人类式分组的总体贡献。

> 直观理解：聚类编号本身没有固定含义，例如机器的“第 1 类”可能对应人的“第 2 类”，ARI 关注的是哪些样本被放在一起而不是类别编号。穷举还能发现加入更多指标未必更好：无关或噪声指标可能掩盖真正与人类判断一致的结构。

**3. 非参数统计三角验证**

Spearman 的 $\rho$ 和 Kendall 的 $\tau$ 分别从秩次单调性与样本对次序一致性刻画 QM–HM 关联，适合五点 Likert 评分及不保证正态分布的小样本数据；作者仅保留同时满足 $|\rho|>0.4$、$p<0.05$ 与 $|\tau|>0.25$、$p<0.05$ 的关系。Kruskal–Wallis H 检验则比较 Run 1、2、3 的秩分布，检验指标区分行为等级的能力，而非只检查全体实验上的连续单调趋势。

> 直观理解：两种相关检验共同通过可减少某一种统计量偶然给出强关系的风险。Kruskal–Wallis 从另一个角度检查指标是否能把三档行为拉开，因此与聚类和逐项相关形成交叉验证。

**训练与推理**

无传统机器学习训练/推理划分。完整执行过程是：先运行不同控制器配置并采集 $24$ 条真实实验记录；从轨迹离线计算 QM，并从问卷汇总 HM；按场景归一化后，分别在两类特征空间运行 $K$-means；用 HM 产生的聚类标签作为比较参照，对全部 QM 非空子集重新聚类和计算 ARI；最后对原始的逐实验指标实施 Spearman、Kendall 和 Kruskal–Wallis 分析。若将该协议用于新系统，原则上需要采集同类轨迹并计算筛选后的 QM；但原文没有给出把新样本映射为最终社会质量分数的已训练预测器，因此不能把该流程理解为可直接输出人类评分的模型。

**复现信息**

实验使用 ClearPath Robotics Jackal 差速滑移转向平台和 VICON 跟踪系统，实验室有效区域为 $4.0\times5.0$ m；四张地图分别覆盖 $2.0\times5.0$ m、$2.0\times5.0$ m、$4.0\times3.0$ m 和 $3.0\times4.0$ m 的区域。前七个场景中行人以约 $0.4$ 至 $1$ m/s 行走，并主要为避免碰撞而调整轨迹；Curious person 场景中的行人会主动追随和阻挡机器人。问卷参与者来自意大利、西班牙和法国，独立评价各实验以避免跨场景相对排序偏差；这种设计有助于解释结果，但二维俯视动画缺少与实体机器人共处时的心理因素，且每个场景只有三次运行，因此所筛选指标在更大空间、更多文化群体和更多控制器上的泛化仍需另行验证。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 核心样本由24次社会导航实验组成，覆盖Passing、Overtaking、Crossing 1/2/3、Narrow Turn、Mixed和Curious共8种场景；每个场景包含3次运行，分别对应不同的机器人控制行为水平。原文未报告训练集、验证集或测试集划分，因为实验目标是相关性与聚类分析，而非训练预测模型。
- HM数据是参与者观看二维俯视动画后给出的5点Likert问卷评价，用于表示人类对机器人社会导航质量的感知。HM分数除以5缩放到$[0,1]$，并在聚类对齐分析中作为参照特征空间；原文节选未明确报告参与者人数、问卷样本量及人口统计信息。
- QM数据由同一批24次实验的11项自动计算指标构成，包含目标到达时间、平均机器人线速度、路径长度、社会功、人与机器人最小距离以及不同近体空间占用等效率、安全和社会距离信息。每项QM在同一场景的3次运行内线性缩放到$[0,1]$，最优运行赋值为1；不同指标依据其含义决定最大化或最小化。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**调整兰德指数（ARI）**

比较QM空间与HM空间的两套聚类划分是否把相同实验样本分到一起，并对随机一致性进行校正。文中把HM聚类标签作为参照，并遍历QM的所有非空子集以寻找高一致性组合。 （越高越好；较高ARI表示两种特征空间产生更相似的样本分组，但不等于单项QM能解释具体的人类感知维度。）

</div>
<div class="metric-item" markdown="1">

**轮廓系数（Silhouette score）**

衡量同一簇内样本是否紧密、不同簇之间是否分离，用于从$K\in[2,5]$中判断HM数据更自然的聚类数。 （越高越好；更高分数表示聚类内部更一致且簇间更容易区分。）

</div>
<div class="metric-item" markdown="1">

**Spearman相关与Kendall相关**

两种非参数秩相关指标分别衡量QM与HM之间的单调关系和排序一致性。作者要求同时满足$|\rho|>0.4$、$|\tau|>0.25$且两者$p<0.05$，才将关系视为稳定相关。 （相关强度的绝对值越大且$p$值越小越有力；正负号表示关系方向，不能简单理解为负相关一定更差，因为部分QM本来就是越小越好。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 验证HM能否作为区分机器人社会行为水平的人类参照

<div class="result-value" markdown="1">

Friedman检验显示8个场景的HM评分梯度均达到$p<0.01$；除Curious为$p=0.0025$外，其余场景均为$p<0.001$。Run 3与Run 1的Wilcoxon比较也全部显著，其中Narrow Turn为$p=0.0040$，其余场景为$p<0.001$。

</div>

作者据此主张，问卷并非完全由随机主观偏差构成，而能稳定区分三种控制行为，因此可作为QM对齐的参照。该结果只证明本实验刺激下评分存在统计差异，并不证明HM是普适、无偏或跨人群一致的绝对真值。

<div class="result-source" markdown="1">

来源：Section V-A, Table I

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

According to Friedman, the HM survey data maintains a statistically significant score gradient across all eight scenarios ($p<0.01$), establishing a robust ground truth.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 比较全部QM与筛选后QM组合对HM聚类的匹配程度，采用$K=2$

<div class="result-value" markdown="1">

全部11项QM的ARI仅为$-0.04$；最佳五指标组合——平均机器人线速度、社会功、亲密空间占用、个人空间占用和人与机器人平均最小距离——将ARI提高到$0.54$。其余三个最佳组合分别达到$0.42$、$0.42$和$0.31$。

</div>

这表明指标并非越多越好：同时保留运动效率、近体空间和人与机器人距离信息，比直接拼接全部指标更接近人类感知形成的二分结构。不过$0.54$只是中等程度的聚类一致性，而且结果来自24个样本，不能证明该组合能替代真实用户调查。

<div class="result-source" markdown="1">

来源：Section V-B, Table II

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The initial ARI of $-0.04$ across all 11 quantitative metrics was inadequate to establish a substantial correlation between the two clusters, as it was lower than 0.3.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 通过聚类、Spearman/Kendall相关和Kruskal–Wallis检验交叉识别最具人类对齐性的QM

<div class="result-value" markdown="1">

平均最小人距、亲密空间占用、社会空间占用、目标到达时间和平均机器人线速度是与HM关系最稳定的一组指标；作者只保留同时满足$|\rho|>0.4$、$|\tau|>0.25$且两种检验均有$p<0.05$的相关关系。社会功未进入强单项相关指标，平滑性也仅被现有指标较弱地表示。

</div>

距离与近体空间指标主要对应非干扰性、友好性和避障预见性，平均速度更偏向避障能力，目标到达时间可能混合反映多个导航方面。这说明当前QM能覆盖部分可观察行为，却不能充分表示平滑性等主观体验；相关关系也不说明这些QM造成了人类评价变化。

<div class="result-source" markdown="1">

来源：Section V-C, Figures 5 and 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The QM metrics with the highest correlation with a human criteria (HM) are: Avg-min-distance-person, Proxemics-Intimate-Space, Proxemics-Social-Space, Time-to-goal, and Avg-robot-linear-speed.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 调查使用二维俯视动画，使参与者容易观察速度、相对距离和路径平滑性，但缺少人与实体机器人共享空间时的临场压力、风险感和身体反应；因此所得HM及其与QM的相关性未必能直接迁移到真实人机共处环境。
- 分析仅含24次实验，却枚举2047个QM子集并选择最高ARI组合；原文节选未报告独立验证集、跨场景留出验证或多重比较校正。因而最佳组合可能对当前场景和样本敏感，相关性与聚类一致性也不能证明QM能够取代大规模人类调查。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 全部11项QM联合形成的特征空间：这是不做指标筛选的直接基线，用来检验“加入更多指标是否自然提高与人类分组的一致性”。其初始ARI为$-0.04$，显示冗余或不对齐的指标可能破坏聚类结构。
- HM特征空间上的K-means聚类：作者将其标签当作比较QM聚类的“ground truth”。这一基线并非客观真值，而是经过Friedman与Wilcoxon检验后建立的人类感知参照。
- 单项QM与单项HM的秩相关分析：Spearman相关和Kendall相关分别检验单调排序关系与成对排序一致性，用来与多指标聚类结果交叉验证。
- 按Run 1、Run 2和Run 3划分行为等级的Kruskal–Wallis检验：它不评价逐样本单调相关，而是检验某项QM能否区分三种行为水平，因此是对相关分析的补充比较。

**实验想回答的问题**

- 现有定量导航指标（QM）形成的实验分组，是否能与人类问卷指标（HM）反映的社会行为类别一致，从而支持低成本、可复现的“人类对齐”初步评测？
- 哪些单项或组合QM最能解释HM中的友好性、非干扰性、避障预见性和平滑性等主观判断，哪些人类感知因素仍未被现有指标充分表示？

**实验实现**

评测流程分为四步。第一，对每个场景内3次运行的QM按指标优劣方向线性归一化，使最佳运行取1，并把HM除以5缩放至$[0,1]$。第二，分别在QM与HM特征空间上执行无监督K-means；先用轮廓系数选择合适的$K$，再以ARI比较两套聚类。第三，枚举11项QM的全部非空子集，共$2^{11}-1=2047$种组合，计算每种组合的ARI，并通过累积ARI统计各指标在高一致性组合中的重要性。第四，使用Spearman、Kendall和Kruskal–Wallis从单指标相关、排序一致性和行为等级区分能力三个角度交叉验证。HM本身先以Friedman检验比较每个场景的3次运行，再用Wilcoxon符号秩检验比较预期最社会化的Run 3与最不社会化的Run 1。原文节选未明确报告K-means初始化次数、随机种子或缺失值处理方式。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| QM特征选择消融：全部11项指标对比最佳五指标子集 | 使用全部11项QM时ARI为$-0.04$；筛选为平均机器人线速度、社会功、亲密空间占用、个人空间占用和平均最小人距后，ARI达到$0.54$，绝对提高$0.58$。 | 该比较隔离了“指标子集选择”的作用：移除部分弱相关或噪声指标后，QM聚类明显更接近HM聚类。它不能确定每个被移除指标单独造成多少损害，也不能排除在仅24个样本上搜索2047种组合所产生的选择偏差。 | Section V-B, Table II<br><span class="experiment-evidence">These optimal QM sets significantly increase the ARI compared to using the entire QM set as the feature space.</span> |
| HM聚类数消融：比较$K=2$与$K=3$的内部可分性 | HM空间在$K=2$时轮廓系数为$0.548$，在$K=3$时为$0.435$，前者高$0.113$，因此作者认为二簇划分更容易区分。 | 这一比较检验结论是否依赖预设的行为类别数。结果表明，尽管实验有3个运行等级，HM数据在几何结构上更自然地形成两个群组，可能意味着参与者更容易区分较粗粒度的“较社会化/较不社会化”行为，而不是稳定恢复三个等级；轮廓系数本身不说明两个簇分别具有何种语义。 | Section V-B<br><span class="experiment-evidence">This internal cluster composition analysis yielded a silhouette score of 0.548 for $K=2$, while $K=3$ yielded 0.435, indicating that division into two clusters is more easily distinguishable.</span> |

**定性案例**

- Narrow Turn场景中，Run 3与Run 1的Wilcoxon检验仍显著，但$p=0.0040$，弱于多数场景的$p<0.001$。作者将其解释为参与者对高级或混合交互更难形成一致判断，并可能严厉评价仅部分符合社会规范的轨迹。该案例提示：复杂空间交互中的人类评价不确定性高于简单通过或超越场景，QM与HM的对应关系也可能随场景而变化。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper studies human-aligned evaluation metrics for socially aware mobile-robot navigation.; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`5bdfdff25077746c1d29e7dc0496ecfe68cd5341be9172d24a2520bc3abcc057`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
