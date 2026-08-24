---
title: "[论文解读] Causal Modeling of Adverse Pregnancy Outcomes via Adaptive LLM Proposals"
description: "[arXiv 2608.21079][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.21079"
announcement_date: "2026-08-24"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-24T02:12:43.977582+00:00"
source_sha256: "6faa9ecf0d9a73bcc753f28fdf5e6cec8e4656de9913471d2bf77f3869f7f4a3"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "因果发现"
  - "不良妊娠结局"
  - "大语言模型"
  - "因果贝叶斯网络"
  - "估计分布算法"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.21079</p>

# Causal Modeling of Adverse Pregnancy Outcomes via Adaptive LLM Proposals

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Kavimayil P. Komarasamy, Saurabh Mathur, Ameet Soni, David M. Haas, Kristian Kersting, Sriraam Natarajan</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: 2 The University of Texas at Dallas；Affiliation: 3 Technical University of Darmstadt；Affiliation: 4 Swarthmore College；Affiliation: 5 Indiana University School of Medicine；Affiliation: 6 Hessian Center for Artificial Intelligence (hessian.ai)；Affiliation: 7 German Research Center for AI (DFKI)；The University of Texas at Dallas；Technical University of Darmstadt；Swarthmore College；Indiana University School of Medicine；Hessian Center for Artificial Intelligence (hessian.ai)；German Research Center for AI (DFKI)</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.21079v1) · [PDF 下载](https://arxiv.org/pdf/2608.21079v1) · **关键词** 因果发现, 不良妊娠结局, 大语言模型, 因果贝叶斯网络, 估计分布算法<br>


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

原文未明确报告。

**不用术语来说**：原文未明确报告。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 原文未明确报告。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于临床因果发现与神经符号人工智能的交叉领域，关注如何从有限且噪声较大的产科数据和不完整的医学知识中构建不良妊娠结局（Adverse Pregnancy Outcomes，APOs）的因果模型。APOs包括早产、先兆子痫和妊娠期糖尿病等，其风险因素涉及孕妇人口学特征、家族史、既往疾病和生活方式。论文采用因果贝叶斯网络（Causal Bayesian Network，CBN）表示变量之间的有向因果关系，并将大语言模型（Large Language Model，LLM）的领域先验知识与数据上的经验评分结合起来，以生成和筛选合理的因果图。这里的目标不是仅拟合变量相关性，而是得到能够支持医学干预推理的候选因果结构。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**因果贝叶斯网络与因果有向无环图**

因果贝叶斯网络用有向无环图表示变量之间的直接因果关系；若存在边 $X_i\rightarrow X_j$，表示 $X_i$ 被假设为 $X_j$ 的直接原因。它不仅描述统计依赖，还可用于回答“主动改变某个变量会怎样”的干预问题，因此比普通贝叶斯网络更适合临床决策。

</div>
<div class="concept-item" markdown="1">

**理论精炼与结构评分**

理论精炼从一个已有的、通常不完整的因果图出发，通过增加、删除或反转边，逐步寻找数据拟合更好的图。贝叶斯狄利克雷（BD）分数或贝叶斯信息准则（BIC）等结构评分可衡量候选图对观测数据的解释程度，但这种局部爬山搜索容易受初始图影响并陷入局部最优。

</div>
<div class="concept-item" markdown="1">

**估计分布算法与MIMIC循环**

估计分布算法不只保留一个候选解，而是反复执行“采样—评估—更新”，利用高分候选解的共同特征来指导后续搜索。本文借鉴互信息最大化输入聚类（MIMIC）的思想，但不显式学习图结构的概率分布，而是让LLM根据高分图作为上下文示例来产生下一批候选图。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定临床数据集中的变量集合、禁止出现的边集合以及由LLM提供的医学先验，任务是生成一个或多个表示变量因果关系的候选有向无环图。每轮生成的图都要在数据上接受经验结构评分，再选出得分最高的若干图，作为下一轮LLM提示上下文的一部分；最终输出是高评分的候选因果图及其边集合，而不是单纯的预测标签。该设定面向小样本、观测数据和不完整领域知识，因而不能假定所有相关变量都被充分测量，也不能依靠孕妇人群中难以实施的随机干预实验直接确认全部因果边。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\bm{X}=\{X_1,X_2,\dots,X_n\}$**

研究中考虑的全部变量集合，例如孕妇特征、既往疾病、生活方式因素和不良妊娠结局。

</div>
<div class="notation-item" markdown="1">

**$G=(\bm{X},E)$**

因果图；节点是变量集合 $\bm{X}$，边集合 $E$ 包含被假设存在的有向因果关系。

</div>
<div class="notation-item" markdown="1">

**$X_i\rightarrow X_j\in E$**

表示变量 $X_i$ 被建模为变量 $X_j$ 的直接原因。

</div>

</div>

**直接相关的工作**

- **数据驱动因果发现方法：PC、FCI与GES**: 这些方法主要从观测数据中的条件独立关系或评分信号学习因果结构，并依赖因果马尔可夫条件、忠实性和因果充分性等结构假设。论文指出，产科临床数据通常规模小、噪声大且变量观测不充分，因此仅依赖统计信号可能无法恢复合理的临床因果图。
- **LLM增强的理论精炼**: 相关方法使用LLM生成初始因果图，再通过局部增加、删除或反转边来改善数据结构评分。本文将其作为重要背景，但认为单个LLM初始图会使局部搜索高度依赖起点；因此本文改用多轮候选生成和高分图上下文更新，以扩大搜索范围并降低陷入局部最优的风险。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

不良妊娠结局（Adverse Pregnancy Outcomes，$APOs$）包括子痫前期、妊娠糖尿病和早产等，可能对母亲及子女产生长期影响。临床上需要可靠的因果模型来识别风险因素及其作用关系，从而支持风险评估和有针对性的干预；但产科领域的数据量有限、数据质量不稳定，而且对孕妇开展干预性研究存在较大伦理与实践困难，因此许多$APOs$的整体因果机制仍不清楚。原文依据：Introduction：“data-driven causal discovery is limited by the paucity of high-quality obstetric data and the extreme difficulty of performing interventional studies in pregnant populations.”

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **纯数据驱动的因果发现**：这类方法主要从观测数据中的统计依赖关系出发，搜索能够解释数据的因果图，而较少依赖医学先验知识。其优势是流程较自动化，但在产科小样本和复杂变量关系下，数据本身通常不足以稳定地区分因果关系与相关关系。
- **基于大语言模型（$LLM$）的因果假设生成与理论修正**：$LLM$利用训练语料中的医学知识提出可能的因果边，或从一个初始因果图出发，通过局部增删和修改边来提高图与数据的拟合程度。前者能够提供广泛先验，后者则尝试用经验数据约束假设。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 纯数据驱动方法受到产科高质量数据稀缺的直接限制，难以可靠恢复完整的因果结构；而$LLM$虽然能提出许多候选关系，却不能稳定地区分真正的因果关系和单纯相关关系，其输出还会对提示词敏感，可能产生相互矛盾且缺乏数据依据的因果图。原文依据：Introduction：“LLMs can suggest causal links based on their vast training corpora, they cannot reason causally; they fail to distinguish genuine causation from mere association”；以及：“their outputs are highly sensitive to prompts and can result in contradictory graphs that lack grounding in empirical evidence.”
- 现有理论修正方法通常从一个初始假设出发，仅通过局部编辑逐步改善其数据拟合度，因此结果依赖初始图的质量，容易陷入由起点决定的局部最优解。其后果是，即使数据和领域知识中存在更有价值的因果结构，搜索过程也可能无法到达。原文依据：Introduction：“these methods are sensitive to their starting points, often becoming trapped in local optima that depend entirely on the quality of the initial hypothesis.”

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种能够同时利用$LLM$广泛医学先验和有限临床数据、又不被单个初始因果图或一次性模型输出限制的因果假设生成机制。具体而言，已有工作没有充分解决如何让候选因果图在多轮搜索中依据经验数据持续筛选和改进，从而降低$LLM$输出的随机性、矛盾性及脱离数据的问题。

</div>
<div markdown="1"><span>核心问题</span>

在产科数据稀缺且医学因果知识不完整的条件下，能否把$LLM$作为候选因果图的自适应提议分布，并通过“生成—经验评价—上下文更新”的迭代过程，使后续假设逐步集中到更有数据支持、同时具有医学合理性的因果结构区域？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把$LLM$看作负责扩大搜索范围的知识提议器，而不是直接判定因果关系的最终裁判：模型先生成多个候选图，数据评分器再检验这些图是否与观测证据相符，表现较好的图被放回后续上下文，帮助模型减少重复生成低质量或矛盾结构。直观地说，这种循环让$LLM$负责“提出可能性”，让数据负责“筛选可信度”，并通过保留高分历史候选逐步修正搜索方向；因此它有望同时缓解小数据导致的搜索不足和单次$LLM$输出不稳定的问题。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CLARA（Causal Learning via Adaptive Resampling and Aggregation）面向数据稀疏、领域知识不完整的因果发现任务，将预训练大语言模型（LLM）视为因果图的自适应提议分布。给定变量集合 $\bm{X}$、小型临床数据集和部分先验知识，系统反复执行“生成—评估—更新”：LLM生成多个候选因果有向无环图（DAG），候选图依据经验数据评分，再把高分图或其共同边作为下一轮提示上下文，从而逐步把生成概率集中到更有希望的因果结构区域。直观地说，LLM负责提供广泛但可能不稳定的医学知识，数据评分负责筛选这些知识，迭代提示则让后续生成参考先前表现较好的方案；该过程不是直接训练一个新的因果模型，而是搜索和聚合候选因果假设。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 定义变量与先验约束

把变量表示为因果图 $G=(\bm{X},E)$ 中的节点，把候选有向边表示为潜在直接因果关系；在真实的 nuMoM2b 实验中，数据驱动基线还获得了相同的禁止边集合 $\mathbf{F}$。

<div class="method-step__io" markdown="1">

**输入**：临床变量集合 $\bm{X}=\{X_1,X_2,\ldots,X_n\}$、小型观测数据集，以及不完整的专家知识和允许或禁止的边集合。<br>
**输出**：候选因果图的搜索问题、变量表示和初始提示所需的领域约束。

</div>

**直观理解**：这一步先确定“有哪些因素”和“哪些方向明显不应考虑”，相当于给搜索划定地图，而不是让模型在所有可能的医学变量之间任意连线。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 由 LLM 生成候选因果图

LLM依据提示生成多个多样化的因果结构假设，将其作为候选 DAG 集合；CLARA不依赖单个LLM输出，而是把LLM整体视为随上下文变化的采样分布。

<div class="method-step__io" markdown="1">

**输入**：变量清单、领域问题描述、先验约束，以及初始或上一轮更新后的提示上下文。<br>
**输出**：本轮候选因果图集合及其结构表示。

</div>

**直观理解**：LLM像一个能提出多种医学解释的顾问：它的知识覆盖面广，但单次回答可能矛盾，因此系统保留多个方案而不是只采信一个答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 用经验数据评估候选图

对每个候选图计算经验结构评分，并据此排序；随后选取高分候选图用于下一轮上下文更新。论文摘录未明确给出该经验评分的具体公式或所用评分函数名称。

<div class="method-step__io" markdown="1">

**输入**：候选因果图集合和临床或合成数据。<br>
**输出**：按数据一致性排序的候选图，以及其中的 top-$K$ 高分图。

</div>

**直观理解**：这一步检查“提出的因果关系是否能解释实际数据”，但数据评分只是证据，不等于单独证明医学因果关系。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 更新提示并迭代搜索

将高分图加入或替换后续生成的上下文，使下一轮LLM生成向高分结构区域移动；共同边变体用高分图之间的结构摘要替代完整 DAG，以减少提示长度。重复生成、评估和更新，直到达到预设迭代次数或完成搜索。

<div class="method-step__io" markdown="1">

**输入**：top-$K$ 高分候选图，或这些图中反复出现的共同结构，以及当前提示上下文。<br>
**输出**：最终候选因果图、稳定出现的因果边和可供领域专家审查的新增假设。

</div>

**直观理解**：系统像“筛选—复盘—再提案”：每轮留下较好的方案作为范例，让模型下一轮少走明显无效的方向，同时保留多个可能性以降低局部最优风险。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 因果贝叶斯网络的联合分布分解

$$
P(\bm{x})=\prod_i P_i\bigl(X_i\mid \mathrm{Pa}_i(\bm{x})\bigr)
$$

**符号说明**

- $\bm{X}$：变量集合 $\{X_1,X_2,\ldots,X_n\}$。
- $\bm{x}$：变量集合 $\bm{X}$ 的一个具体取值或观测赋值。
- $P(\bm{x})$：整个变量赋值 $\bm{x}$ 的联合概率。
- $P_i$：变量 $X_i$ 在给定其父节点后的局部条件概率分布。
- $\mathrm{Pa}_i(\bm{x})$：因果图中 $X_i$ 的父节点在赋值 $\bm{x}$ 下的取值。

<div class="equation-explanation" markdown="1">

**直观理解**：该式说明一个因果贝叶斯网络如何由图结构和局部条件分布共同表示整体概率分布。它是背景定义而非CLARA专门优化的目标；CLARA主要搜索图结构 $G$，再用经验数据评价候选结构。<br>
**原文位置**：II-A Causal Bayesian Networks

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告一个需要梯度训练的新模型目标，也未给出候选图经验评分的具体数学形式。CLARA的优化对象是候选因果图的经验得分：生成多个图、选择高分图，并通过更新LLM上下文使后续提议偏向高分结构；因此这里更准确地说是基于评估的迭代搜索，而不是对LLM参数进行端到端训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. LLM自适应提议分布**

与一次性生成单个初始图不同，CLARA通过提示上下文控制LLM对候选因果结构的生成分布。高分图被用作后续 in-context examples；因此提议分布不是显式参数化的概率模型，而是由LLM及其动态上下文隐式定义。

> 直观理解：LLM不是最终裁判，而是不断提出候选方案的“提议者”；系统根据历史得分告诉它下一轮应重点参考哪些结构。

**2. Generate-Evaluate-Update 搜索循环**

CLARA将估计分布算法中的 Sample-Evaluate-Update 思路改写为 Generate-Evaluate-Update。它不显式学习 top-$K$ 图上的结构分布并从该分布采样，而是用LLM生成新样本，并通过替换或更新提示中的高分样例完成分布调整。

> 直观理解：传统方法可能直接拟合一个新的采样器；CLARA则利用提示示例间接改变LLM的采样倾向，借此结合大规模先验知识与小数据集证据。

**3. 高分图聚合与共同边摘要**

完整 CLARA 将 top-$K$ 高分因果图作为后续上下文；共同边变体提取这些高分图中反复出现的边，以结构摘要替代完整图。后者旨在降低提示 token 数，同时尽量保留高分候选之间的稳定信息。

> 直观理解：如果多个好方案都包含同一条边，就把它看作较稳定的线索；只传递这些共同线索可减少模型需要阅读的内容，但可能丢失完整图中的组合关系。

**训练与推理**

论文摘录描述的是推理时搜索流程。首先固定变量、数据和约束，使用LLM生成候选因果图；然后在数据上评分并选出 top-$K$ 图，更新提示后重复该过程，最终输出高分候选结构及其聚合边。实验中还报告了使用 GPT-5.2 或 Llama-3.3-70B-Instruct 作为提议LLM，并将迭代次数记为 $T$、保留图数量记为 $K$；在图3的敏感性实验中，GPT-5.2 使用 $K=7$、$T=5$。论文摘录未明确报告停止准则、候选图的精确编码格式、经验评分公式以及LLM调用的随机采样参数，因此这些内容不能据此复现。

**复现信息**

为公平解释结果，应区分三类方法：PC和FCI是主要依靠条件独立性等统计信号的数据驱动因果发现方法；“LLM（One-shot）”只使用一次LLM生成；“LLM + Theory Refinement”从LLM图出发，用逐边添加、删除或反转的局部贪心搜索进行理论修正；MIMIC使用类似迭代重采样结构但没有LLM提供的先验。CLARA的共同边变体以 top-$K$ 图的结构摘要替代完整图，论文报告其提示长度最多可减少约三倍；不过摘录未明确报告完整的提示模板、每轮候选数量、评分函数、图合法性校验和最终图的汇聚规则。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ALARM 合成数据集：基于包含 37 个节点和 46 条边的 ALARM 贝叶斯网络生成 3,000 个观测；真实因果图和条件概率表来自 bnlearn。每个离散变量以 0.2 的概率被随机替换为该变量的另一个有效状态，从而模拟 20% 的逐项分类噪声。其作用是提供已知真值图，检验方法在可控噪声环境下的结构恢复能力。
- nuMoM2b 真实临床数据：来自初产单胎孕妇的纵向研究，仅使用首次产检时收集的变量，包含 9 个早孕风险因素和 4 个不良妊娠结局，即先兆子痫、新发高血压、妊娠期糖尿病和早产。排除既往糖尿病受试者及含缺失值的样本后，保留 3,856 个样本；其作用是检验方法在真实、稀疏且具有临床约束的数据上的实用性。
- 专家参考图与额外边分析：在 nuMoM2b 上，使用产科专家依据当前医学共识构建的因果图作为结构参照，并分析模型超出该图所发现的边是否具有潜在临床意义。该参照图代表专家当前已知关系，而不应被解释为绝对完备的真实因果图。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Structural Intervention Distance (SID)**

衡量学习图与参考图在干预推理和调整集方面的差异，关注图是否支持正确的干预效果估计，而不只是边是否逐条相同。 （越低越好；在临床干预场景中，较低 SID 表示模型更可能为干预提供可靠的因果调整方案。论文将其作为主要指标。）

</div>
<div class="metric-item" markdown="1">

**Structural Hamming Distance (SHD)**

统计学习图相对于参考图的边添加、删除和方向反转错误，并将这些错误视为同等代价。 （越低越好；但较低 SHD 不必然意味着干预推理正确，因为该指标不区分一条边是否会改变所需调整集。论文将其作为次要指标。）

</div>
<div class="metric-item" markdown="1">

**Recall 与 Precision**

Recall 衡量参考图中的因果关系被恢复的比例，Precision 衡量模型预测的边中与参考图一致的比例；二者共同描述拓扑结构与专家图的对齐程度。 （越高越好；Recall 高表示漏边少，Precision 高表示误报边少，但二者都不能单独保证干预推理可靠。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### nuMoM2b 真实产科数据上的专家图对齐

<div class="result-value" markdown="1">

作者报告 CLARA 恢复了专家验证的全部因果边，并在专家参考图之外发现了额外的、具有潜在临床合理性的关系；但所给原文摘录没有提供表 II 中对应的具体 SID、SHD、Recall 或 Precision 数值。

</div>

这说明 CLARA 至少没有遗漏专家已认可的关系，并能提出供专家进一步审查的新假设。它不等于额外边已经被临床或实验研究证实，也不能仅凭该结论断言模型在所有指标上都优于每个基线。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Our method recovers all expert-validated edges and identifies additional plausible causal relations not previously listed by experts, potentially providing new insights for targeted interventions.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### ALARM 含 20% 逐项分类噪声的合成数据

<div class="result-value" markdown="1">

实验将 CLARA 与已知生成图的 ALARM 真值进行比较，以检验其在噪声观测下恢复因果结构的能力；所给摘录仅说明该数据和评估设计，未报告表 II 的具体结果数值或明确的胜负排序。

</div>

ALARM 的价值在于真值图已知，因此可以直接评价结构错误，而不必把专家判断当作唯一标准。但当前材料不足以证明 CLARA 在 ALARM 上相对 PC、FCI 或其他基线的具体改进幅度。

<div class="result-source" markdown="1">

来源：Section IV-A, Dataset Description

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We sampled 3,000 observations from this network based on the provided probability tables and introduced 20% entry-wise categorical noise, where each variable value is independently replaced with a randomly selected valid state with probability 0.2 to simulate imperfect observational conditions.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 结构摘要与完整 DAG 的表示比较

<div class="result-value" markdown="1">

作者把完整图排序版本与只在 top-$K$ 图中保留共同直接邻接边的 Common edges 版本进行比较，并以结构摘要能否在减少提示词规模的同时维持性能为实验目标；所给摘录没有报告提示词长度、性能变化或显著性数值。

</div>

该比较测试的是信息压缩是否损害搜索质量：摘要只传递多个高分图一致同意的邻接关系，因此可能减少冗余，但也可能丢失方向或不确定结构。没有具体结果时，不能判断压缩是否确实无损。

<div class="result-source" markdown="1">

来源：Section IV-B, Method and Baselines

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A common edge is included in the structural summary representation only if it appears in all top-K scoring graphs to reflect full agreement across the top-K set.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给原文摘录缺少表 II 和表 IV 的具体数值，因此无法核查 CLARA 相对各基线在 SID、SHD、Recall、Precision 上的实际优势、误差范围及统计显著性。
- nuMoM2b 的专家图只编码临床专家依据当前知识认可的关系，且研究使用首次产检观测数据并删除缺失值；因此额外边仍需外部数据、纵向分析或临床研究验证，结果不能自动推广为完整或已确认的产科因果图。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- PC 算法：基于条件独立性检验从观测数据中发现因果结构，代表经典的纯数据驱动方法；用于检验 LLM 先验是否能弥补数据稀缺和噪声造成的信息不足。
- FCI 算法：同样使用数据驱动的条件独立性检验，但面向可能存在未观测混杂的因果发现问题；用于与另一种标准观测因果发现程序比较。
- 纯一次性 LLM 生成：直接让 GPT-5.2 或 Llama-3.3-70B-Instruct 生成因果图，不利用 CLARA 的迭代经验反馈；用于隔离 LLM 先验本身与自适应搜索机制的贡献。
- MIMIC 与 LLM 增强的理论修正方法：MIMIC 作为非 LLM 的探索性数据分析消融，主要隔离 CLARA 的迭代搜索环路；LLM 增强理论修正则代表使用 LLM 进行理论初始化或修正、但不完整复现 CLARA 自适应提议过程的方法。

**实验想回答的问题**

- 在合成的、含噪且数据稀缺的环境中，CLARA 将 LLM 先验与迭代结构搜索结合后，是否比纯 LLM 生成、纯结构搜索以及 LLM 初始化的局部搜索产生更好的因果假设？
- 在真实产科数据中，CLARA 是否能比数据驱动因果发现方法更好地恢复接近临床专家知识的因果结构，同时通过结构摘要减少提示词长度而保持性能？

**实验实现**

数据驱动方法 PC 和 FCI 使用离散变量的卡方条件独立性检验，显著性水平为 $\alpha=0.05$。LLM 方法使用 GPT-5.2 和 Llama-3.3-70B-Instruct，温度设为 0.7；Llama 的最大 token 数为 8192，其他模型参数使用默认值。为降低采样方差，每个候选图由 5 次独立采样响应的并集构成；若并集产生环，则删除 5 次响应中出现频率最低的边，频率相同则按字典序处理。nuMoM2b 所有方法均可使用编码时间顺序约束的不允许边集合 $\mathbf{F}$，而 ALARM 不使用黑名单边。CLARA 的完整版本以 BIC 分数对完整图排序，结构摘要版本只保留所有 top-$K$ 图共同包含的直接邻接边。统一设置批大小 $K=7$、迭代次数 $T=5$；LLM 方法独立运行 5 次并报告均值和标准差，PC 与 FCI 为确定性方法并报告单次结果。原文所给摘录未包含表 II 的具体 SHD、SID、Recall 或 Precision 数值，因此不能据此补充数值比较。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| CLARA 完整图版本 vs. Common edges 结构摘要版本 | 完整版本使用 BIC 排序的完整图，Common edges 版本仅将所有 top-$K$ 图共有的直接邻接边放入上下文；实验目标是测试减少 prompt 大小后是否维持性能，但所给摘录未报告两者的具体分数或压缩比例。 | 该消融主要隔离表示方式，而不是检验 LLM 先验或迭代搜索是否存在。若两者性能接近，说明跨高分候选图的一致邻接信息已足够；若性能下降，则表示被摘要丢弃的方向或不一致信息仍然有用。 | Section IV-A, Dataset Description<br><span class="experiment-evidence">We consider 4 adverse pregnancy outcomes: preeclampsia, new hypertension, gestational diabetes, and preterm birth (both spontaneous and medically indicated).</span> |
| 迭代次数与搜索环路敏感性 | 作者固定批大小 $K=7$ 和迭代次数 $T=5$，并报告该配置在敏感性分析中取得最低 SID；同时称继续增加迭代次数没有带来额外改进。摘录未给出不同 $K$、$T$ 配置的 SID 数值。 | 这项分析测试搜索是否在有限轮次后已经收敛，以及继续向 LLM 提供反馈是否仍有收益。结论支持采用 5 轮作为实验配置，但没有说明不同设置的方差、运行成本或统计显著性。 | Section IV-B, Method and Baselines; Table IV<br><span class="experiment-evidence">For all experiments, we set the batch size K=7 and the number of iterations T=5, as this configuration achieves the lowest Structural Intervention Distance (SID) in the sensitivity analysis (Table IV), with no additional improvements observed from further iterations.</span> |

**定性案例**

- 产科案例分析使用 Fig. 2 展示专家构建的因果图及 CLARA 发现的额外边，并按人口统计学、家族史、既往疾病、生活方式和妊娠结局区分节点类型。该展示用于说明模型输出可能超出既有专家清单并产生可供临床审查的新假设；但所给摘录未列出额外边的具体端点、方向或逐条医学验证结果，因此不能把图中新增关系直接解释为已证实因果关系。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The central contribution is a neurosymbolic iterative reasoning framework that uses an LLM to propose and refine causal hypotheses based on empirical scores.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`6faa9ecf0d9a73bcc753f28fdf5e6cec8e4656de9913471d2bf77f3869f7f4a3`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
