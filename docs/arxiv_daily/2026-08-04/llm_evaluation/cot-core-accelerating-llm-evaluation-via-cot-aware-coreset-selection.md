---
title: "[论文解读] CoT-Core: Accelerating LLM Evaluation via CoT-Aware Coreset Selection"
description: "[arXiv 2608.00014][LLM 评测] CoT-Core通过将问题的零样本思维链推理过程嵌入潜在空间并选择代表性样本，在不依赖历史模型答题日志的条件下压缩评测集，以降低大语言模型持续评测的成本。"
arxiv_id: "2608.00014"
announcement_date: "2026-08-04"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:56:54.056754+00:00"
source_sha256: "4fa05303c3a5d8fada20a9adc6887fa216cff56257437d4ed6ed2f609963cf25"
tags:
  - "LLM 评测"
  - "LLM 其他"
  - "LLM Reasoning"
  - "大语言模型评测"
  - "核心集选择"
  - "思维链"
  - "推理轨迹嵌入"
  - "训练自由方法"
  - "评测数据冗余"
  - "冷启动"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.00014</p>

# CoT-Core: Accelerating LLM Evaluation via CoT-Aware Coreset Selection

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Qihua Pan, Zhenheng Tang, Peijie Dong, Xiang Liu, Huacan Wang, Bo Li, Xiaowen Chu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Nanjing University；The Hong Kong University of Science and Technology；The Hong Kong University of Science and Technology (Guangzhou)</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.00014v1) · [PDF 下载](https://arxiv.org/pdf/2608.00014v1) · **关键词** 大语言模型评测, 核心集选择, 思维链, 推理轨迹嵌入, 训练自由方法, 评测数据冗余, 冷启动<br>


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

CoT-Core通过将问题的零样本思维链推理过程嵌入潜在空间并选择代表性样本，在不依赖历史模型答题日志的条件下压缩评测集，以降低大语言模型持续评测的成本。

**不用术语来说**：大语言模型在预训练、对齐和微调期间需要反复接受评测，而完整运行包含成千上万道题的基准会消耗大量算力和资金。理想方案是只测试少量具有代表性的题目，再据此估计模型在完整基准上的表现；困难在于，代表性不能只按题目措辞判断，因为表面上完全不同的题目可能实际考查同一种解题逻辑。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出无需训练且不依赖历史答题记录的CoT-Core：先展开题目的零样本思维链，再按推理轨迹的表示选择核心问题，旨在绕开文本表面相似性造成的“词汇陷阱”。
- 明确推理感知式评测集压缩的适用边界：作者声称其收益受任务复杂度制约，在基础算术任务上存在“简单度下限”，而在专家级基准上可获得更大的信息收益；同时指出表示质量需要在冗长回答引入的对话噪声与过度压缩造成的学科语义缺失之间权衡。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大语言模型评测通常在包含大量测试题的基准上运行模型，再依据答题正确率等指标估计其能力。由于模型开发需要在持续预训练、对齐和微调期间反复评测多个检查点，全量测试会产生显著的计算与经济成本；与此同时，现有基准内部常含能力或结构相近的冗余题目。因此，本研究关注评测核心集选择：从完整基准中挑选一个规模较小但具有代表性的题目子集，用其评测结果近似完整基准得分。该问题的关键并非简单删除文字相似的题目，而是保留不同的推理结构、能力要求与难度，使子集上的模型表现仍能可靠反映全量表现。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**核心集选择（coreset selection）**

从完整数据集中选出一个较小且具有代表性的子集，使在该子集上得到的评测结论尽可能接近全量数据结果。这里的目标是降低重复评测成本，同时避免因删题而扭曲模型能力估计。

</div>
<div class="concept-item" markdown="1">

**思维链（Chain-of-Thought, CoT）轨迹**

模型在给出最终答案前生成的分步推理过程，可视为从题目到答案的一系列中间认知操作。论文将这种轨迹作为题目表示，试图识别措辞不同但解题逻辑相同的问题。

</div>
<div class="concept-item" markdown="1">

**潜在推理流形（reasoning manifold）**

指题目背后由推理模式、逻辑结构和认知操作形成的隐含组织空间，而非原始文本的字词相似性。将推理轨迹映射为稠密向量后，具有同构推理结构的题目应在该空间中更接近。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个待评测的大语言模型基准，其中每道题包含原始问题文本，但在新建、私有或新兴基准场景下，不假设拥有大量模型在这些题目上的历史作答记录。目标是在不训练额外选择模型的条件下，从完整题集选出规模受限的代表性核心题集，并用核心集上的模型表现近似完整基准得分。论文所针对的主要设置是模型开发过程中的重复评测：同一核心集可用于多个模型或检查点，以减少推理调用和费用；选择依据需要覆盖题目的潜在逻辑与推理结构，而不能仅依赖表层词汇重合。作者进一步假设，零样本思维链能够显式展开部分潜在推理过程，且其向量表示比原始问题文本更适合衡量题目之间的结构相似性；这一假设的适用程度可能受到任务复杂度约束。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **TinyBenchmarks（Polo et al., 2024）**: 该工作使用项目反应理论，根据大量模型的历史正确性响应矩阵估计题目特征并构造小型评测集。它能够利用经验表现刻画题目难度，但依赖预先积累的大规模评测日志，因此在新建或私有基准上存在冷启动限制；这构成 CoT-Core 强调无历史数据、免训练选择的直接背景。
- **k-center greedy（Sener & Savarese, 2017）**: 该几何方法通过选择空间中的代表点来扩大核心集对数据分布的覆盖范围，并且不要求历史作答记录。论文指出，将它直接用于原始题目文本嵌入时容易受表层词汇相似性影响；CoT-Core 保留几何选择思路，但将表示空间改为由思维链推理轨迹形成的潜在空间。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型开发不是一次训练、一次验收，而是需要在多个检查点上持续评测，以监控预训练、对齐和微调的进展。若每次都运行完整基准，数以万计的测试样例会被重复推理，形成难以承受的计算与经济开销；而基准内部又存在冗余，因此需要用一个尽可能小但仍能重建完整评测分数的核心子集来替代穷举评测。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于项目反应理论的心理测量方法**：项目反应理论（Item Response Theory，IRT）利用许多历史模型在各道题上的正确与错误记录，估计题目的难度、区分度等参数，再据此挑选或加权少量题目，以推断待测模型在完整评测集上的能力。
- **基于文本嵌入的几何核心集方法**：这类方法先用稠密编码器把题面映射为向量，再采用$k$-center greedy等几何算法选择覆盖向量空间的代表性样本。其计算较高效，也不必建立复杂的能力模型，但代表性主要由题面嵌入空间中的距离决定。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- IRT类方法严重依赖大量预先积累的模型答题日志。新建基准、私有数据集或尚未被大量模型测试的数据没有足够记录来校准题目参数，因而出现“冷启动”问题，甚至无法直接应用。
- 文本嵌入方法容易受词汇重合和表面语义支配，不能可靠识别题目背后的潜在推理结构。其后果是：使用不同叙述或学科语境、但解题逻辑等价的问题可能被误判为相距很远，核心集因而重复覆盖某些逻辑模式并遗漏其他模式。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法尚未同时满足三个要求：不依赖跨模型历史正确率记录、能够识别跨越题面词汇差异的逻辑等价性，并能据此构造足以高保真估计完整基准分数的小型评测子集。进一步地，原有研究也未充分说明这种推理感知压缩在何种任务复杂度下真正优于浅层文本表示。

</div>
<div markdown="1"><span>核心问题</span>

能否直接利用大语言模型为每道题生成的零样本思维链作为推理结构的可观察代理，在无需训练和历史答题日志的前提下选择代表性核心题目，并使该子集在不同复杂度基准上仍能准确代理完整评测结果？

</div>
<div markdown="1"><span>作者直觉</span>

题面描述更像问题的“外壳”，思维链则把求解所需的中间操作展开出来。例如，两道题可能分别谈论购物和行程，普通文本表示会因名词不同而将其分开，但若二者都需要建立相同关系并执行同一组运算，其推理轨迹就可能更接近。将这些轨迹嵌入后再聚类，有望让每个被选问题代表一种解题逻辑，而不是仅代表一组相似措辞；不过，当任务本身过于简单、可区分的推理结构很少时，这种额外表示带来的收益也会受到限制。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CoT-Core是一个无需历史作答日志、无需参数训练的评测核心集选择框架。输入是完整评测集$\mathcal{D}=\{(q_i,a_i)\}_{i=1}^{N}$和核心集预算$B$；框架先让生成模型$\mathcal{M}_{gen}$为每道题展开零样本思维链轨迹$t_i$，再将原问题$q_i$与轨迹$t_i$拼接后交给预训练稠密编码器$\mathcal{E}$，得到推理特征$\mathbf e_i\in\mathbb R^d$，最后在特征空间中执行$k$-means并令$k=B$，从每个簇选择距质心最近的实例，输出大小为$B$的核心集$\mathcal S$。被测模型$\mathcal M$只需回答$\mathcal S$中的问题，其表现再由标准聚合或GP-IRT等估计器$f_{est}$映射为完整数据集得分$\hat S_{\mathcal D}(\mathcal M)$。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 零样本CoT轨迹生成

将$q_i$与$p_{cot}$进行字符串拼接，并输入指令微调生成模型$\mathcal M_{gen}$，产生逐步推理文本$t_i=\mathcal M_{gen}(q_i\oplus p_{cot})$。无论最终答案是否正确，轨迹$t_i$都被保留，因为方法假设推理尝试仍能暴露问题要求的运算、知识调用和逻辑步骤。

<div class="method-step__io" markdown="1">

**输入**：完整评测集中的每个问题$q_i$，以及固定的CoT触发提示$p_{cot}$。<br>
**输出**：与全部$N$个问题一一对应的推理轨迹集合$\{t_i\}_{i=1}^{N}$。

</div>

**直观理解**：这一步不是让生成模型替代被测模型答题，而是让它把每道题可能需要的“解题路线”写出来。即使路线最后走错，它尝试使用哪类公式、比较哪些选项或进行何种推导，仍可能比题面词汇更能表示题目的推理类型。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 上下文化轨迹嵌入

构造结构化文本$s_i=\text{``Question: ''}\oplus q_i\oplus\text{`` Reason: ''}\oplus t_i$，再由预训练稠密检索编码器$\mathcal E$映射为向量$\mathbf e_i=\mathcal E(s_i)$。全部向量组成矩阵$\mathbf E\in\mathbb R^{N\times d}$，其中$d$是嵌入维数。

<div class="method-step__io" markdown="1">

**输入**：原问题$q_i$及其生成轨迹$t_i$。<br>
**输出**：包含题面语境与推理路径的特征矩阵$\mathbf E$。

</div>

**直观理解**：只编码题面容易把共享专业词汇的题误判为相似，也可能把措辞不同但解法相同的题判得很远。把题面和解题路线一起编码，相当于同时保留“题目在讲什么”和“题目要怎样解决”，避免孤立轨迹失去原始语境。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 同构聚类与代表实例选择

对$N$个向量执行$k$-means聚类并设置$k=B$；在每个簇中，选取到该簇几何质心距离最近的题目作为代表。所选实例的并集构成$\mathcal S\subset\mathcal D$且$|\mathcal S|=B\ll N$。

<div class="method-step__io" markdown="1">

**输入**：推理特征矩阵$\mathbf E$和核心集预算$B$。<br>
**输出**：覆盖不同潜在推理结构的核心评测集$\mathcal S$。

</div>

**直观理解**：每个簇可理解为一种常见的解题结构，距质心最近的题是该结构的典型样本。每簇取一道题，可以减少重复考查同类能力，同时尽量避免漏掉较少见的推理模式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 子集作答与全量性能估计

仅在$\mathcal S$上运行被测模型$\mathcal M$并计算实例得分，再由$f_{est}(\mathcal M,\mathcal S)$估计完整数据集性能。框架将选择器与估计器解耦：无历史数据时可采用标准聚合，有历史响应数据时也可接入GP-IRT等参数化估计器。

<div class="method-step__io" markdown="1">

**输入**：核心集$\mathcal S$、待评测模型$\mathcal M$和选定的估计器$f_{est}$。<br>
**输出**：完整基准得分的代理估计$\hat S_{\mathcal D}(\mathcal M)$，而无需在全部$N$道题上运行$\mathcal M$。

</div>

**直观理解**：昂贵环节是让许多待测模型回答完整题库；CoT轨迹通常只需在建核心集时预先生成一次。之后每个新模型只回答少量代表题，再通过统一的计分规则推测其全量表现。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 完整评测得分与核心集估计目标

$$
S_{\mathcal D}(\mathcal M)=\frac{1}{N}\sum_{i=1}^{N}m\!\left(\mathcal M(q_i),a_i\right),\qquad \hat S_{\mathcal D}(\mathcal M)=f_{est}(\mathcal M,\mathcal S)\approx S_{\mathcal D}(\mathcal M),\quad \mathcal S\subset\mathcal D,\ |\mathcal S|=B\ll N
$$

**符号说明**

- $\mathcal D=\{(q_i,a_i)\}_{i=1}^{N}$：包含$N$个测试实例的完整评测集；$q_i$是第$i$个问题，$a_i$是其参考答案。
- $\mathcal M$：需要评测的未知大语言模型。
- $m(\cdot,\cdot)$：比较模型输出与参考答案的实例级评价函数，原文以精确匹配准确率为例。
- $S_{\mathcal D}(\mathcal M)$：模型$\mathcal M$在完整数据集$\mathcal D$上的真实平均性能。
- $\mathcal S$：从$\mathcal D$中选出的代表性核心集。
- $B$：核心集预算，即允许保留并实际评测的实例数，且远小于$N$。
- $f_{est}$：根据模型在核心集上的响应估计全量性能的代理计分函数。
- $\hat S_{\mathcal D}(\mathcal M)$：由核心集响应得到的完整数据集性能估计值。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分给出昂贵的真实评测：让模型回答全部$N$道题后取平均。第二部分规定核心集方法的目标：只评测$B$道代表题，但让估计值尽可能接近全量得分；CoT-Core主要优化其中的子集$\mathcal S$，而不限定$f_{est}$的具体形式。<br>
**原文位置**：第3.1节，公式(1)与公式(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### CoT上下文化表示构造

$$
t_i=\mathcal M_{gen}(q_i\oplus p_{cot}),\qquad s_i=\text{``Question: ''}\oplus q_i\oplus\text{`` Reason: ''}\oplus t_i,\qquad \mathbf e_i=\mathcal E(s_i),\quad \mathbf E\in\mathbb R^{N\times d}
$$

**符号说明**

- $\mathcal M_{gen}$：用于展开推理轨迹的指令微调生成模型，不是当前被评测的模型$\mathcal M$。
- $p_{cot}$：引导模型逐步思考的固定CoT提示，例如原文所述的“Let’s think step by step”。
- $\oplus$：字符串拼接操作。
- $t_i$：生成器针对问题$q_i$产生的逐步推理轨迹。
- $s_i$：将原问题与其推理轨迹按固定字段拼接得到的上下文化输入序列。
- $\mathcal E$：预训练稠密检索编码器。
- $\mathbf e_i$：问题$i$的$d$维上下文化推理向量。
- $\mathbf E$：由全部$N$个推理向量组成的特征矩阵。
- $d$：稠密编码器输出向量的维数。

<div class="equation-explanation" markdown="1">

**直观理解**：该式概括了方法最关键的表示变换：先把题目展开为解题轨迹，再把题目和轨迹共同压缩成可计算距离的向量。后续聚类比较的因此不只是题面用词，而是包含问题语境的推理路径相似性。<br>
**原文位置**：第3.3节公式(3)与第3.4节公式(4)、公式(5)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：CoT-Core本身没有可训练参数，也没有通过梯度下降优化的损失函数。其“优化目标”是组合式的核心集构造目标，即在$|\mathcal S|=B$约束下让$\hat S_{\mathcal D}(\mathcal M)$接近$S_{\mathcal D}(\mathcal M)$；实际选择阶段用$k$-means的几何划分和最近质心代表实现覆盖，而论文节选未给出一个联合优化选择误差与估计误差的显式损失。若下游采用GP-IRT等参数化估计器，其训练属于估计器本身，并非CoT-Core选择器的训练过程。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 推理轨迹外显器**

该模块由指令微调生成模型$\mathcal M_{gen}$和固定提示$p_{cot}$组成，以零样本方式将隐含解题过程展开为文本轨迹$t_i$。方法不按最终答案正确性筛除轨迹，核心假设是“轨迹结构”比“轨迹结论”更直接地反映题目要求的推理能力；生成器因此不是监督标签来源，也不参与下游被测模型评分。

> 直观理解：它的作用类似于为题目生成一份解题思路草稿。论文消融表明，大模型写得更长并不必然更适合聚类，因为大量通用套话可能使本来不同的题在文本表示上显得相似。

**2. 上下文化推理表示器**

该模块使用预训练稠密编码器$\mathcal E$编码“Question + Reason”序列，而不是单独编码$q_i$或$t_i$。题面提供学科实体和问题条件等语义锚点，轨迹提供操作顺序、公式调用、因果关系与选项排除过程；二者共同决定向量$\mathbf e_i$在潜在推理流形中的位置。

> 直观理解：轨迹若脱离题面，抽象步骤可能过于通用；题面若没有轨迹，又容易受词汇重合支配。联合表示是在表面语义与逻辑结构之间取平衡，论文的清洗消融也说明：去除套话可能有益，但删掉所有数字、实体和领域信息会造成“语义饥饿”。

**3. 预算约束的几何选择器**

选择器在$\mathbf E$上使用无需训练的$k$-means，并令簇数等于预算$B$；每簇选择距离质心最近的真实实例，而非生成一个不可直接评测的合成质心。该模块仅决定$\mathcal S$，不绑定标准聚合、IRT或GP-IRT等$f_{est}$，因此可以独立替换评分估计器。

> 直观理解：聚类解决“应该保留哪些题”，估计器解决“怎样由这些题推断总分”，二者是不同问题。这样的解耦使同一核心集既能在完全零历史数据条件下直接求均值，也能在获得历史日志后配合更复杂的统计模型。

**训练与推理**

离线构建阶段，对固定基准中的全部$q_i$运行一次$\mathcal M_{gen}$，得到$t_i$；随后构造$s_i$，由冻结的$\mathcal E$批量计算$\mathbf E$，再以$k=B$运行$k$-means并从每簇取最近质心实例，形成可复用的$\mathcal S$。这一阶段不需要任何被测模型的历史正确率矩阵，也不更新$\mathcal M_{gen}$或$\mathcal E$。在线评测阶段，对每个新模型$\mathcal M$仅提交$\mathcal S$中的问题，依据参考答案$a_i$获得子集实例分数，再用$f_{est}$输出$\hat S_{\mathcal D}(\mathcal M)$；无历史数据时采用标准聚合，有历史日志时可接入GP-IRT等估计器。需要注意，生成CoT是核心集的一次性预处理成本，真正被持续节省的是每个后续模型在完整基准上的推理成本。

**复现信息**

论文使用预训练稠密编码器（示例为BGE-M3）表示上下文化轨迹；CoT生成温度设为$T=0.7$，最大生成长度为$1024$个token。标准生成方式是在$q_i$后追加固定$p_{cot}$；层次清洗消融中，初始生成和后续清洗均使用Phi-4，以控制模型差异这一混杂因素。原始方法保留未改写的CoT；Cleaned CoT删除自我修正、死路、犹豫和会话套话，但保留必要计算、实体及核心步骤；Abstract CoT进一步删除具体数值与实体，只保留元操作序列。后两者属于机制消融而非默认流水线。复现时还应明确生成器版本、编码器版本、预算$B$或采样比例、$k$-means初始化与随机种子；其中后两项在所给原文节选中未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：数学文字题推理基准，用于检验基于零样本思维链轨迹的选题方式能否识别共享的数学推理结构。所给节选未明确报告数据规模、实际评测样本数或是否使用官方测试划分。
- MMLU 与 MMLU-Pro：跨学科选择题基准；前者覆盖一般知识与推理任务，后者提高了题目难度，用于比较任务复杂度变化时推理感知剪枝的适用边界。所给节选未报告各自使用的样本规模及具体学科划分。
- GPQA Diamond：高难度研究生水平科学问答子集，用于测试方法在复杂科学推理任务上的表现。由于该数据集较小，$1\%$ 预算只对应一个样本，论文因此不报告该设置。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Mean Absolute Error（MAE）**

计算子集代理分数与完整数据集真实分数之间绝对误差的平均值，直接衡量压缩评测后的分数估计保真度。 （越低越好，因为误差越小说明用少量题目得到的模型分数越接近全量评测结果。）

</div>
<div class="metric-item" markdown="1">

**Ranking Similarity（Sim）**

衡量子集评测产生的模型排序与完整数据集排序的一致程度。所给节选未给出该相似度的具体数学定义。 （越高越好，因为更高的一致性表示压缩评测更能保持模型之间的相对优劣关系。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Random：按预算随机抽取题目，是不利用内容或历史信息的最低参照；它检验复杂选题策略是否真正优于抽样波动。论文对该基线运行 $20$ 次独立试验。
- Question-Emb K-Means：对原始问题文本的嵌入进行 K-Means 聚类，再据此选择代表题；它是最直接的训练自由语义聚类基线，用于检验 CoT 推理轨迹是否比表层问题文本提供更有效的代表性。
- $k$-Center Greedy：在特征空间中贪心选择样本，使未选样本到最近中心的最大距离尽量小；它代表强调全局覆盖而非平均聚类误差的训练自由方法。
- Correctness K-Means 与 IRT：前者聚类历史二元正确性响应矩阵，后者利用项目反应理论从历史评测日志拟合题目及模型的潜在参数。两者代表依赖历史模型答题记录的方法；在主实验中只使用互不重叠的 $N=25$ 个训练模型拟合，并作为参考与无训练方法比较。

**实验想回答的问题**

- 在仅保留原测试集 $1\%$、$5\%$、$10\%$、$15\%$ 或 $20\%$ 样本的条件下，CoT-Core 能否比随机抽样、原始问题文本聚类和覆盖式选择更准确地估计模型在完整数据集上的分数与排名？
- CoT-Core 的无训练、推理轨迹感知选择机制，能否在只有 $N=25$ 个历史模型的低资源条件下，与依赖历史答题日志的 Correctness K-Means 和 IRT 方法形成有竞争力的替代方案，并能否推广到未参与拟合的 $100$ 个模型？

**实验实现**

CoT-Core 的轨迹生成模型 $\mathcal{M}_{gen}$ 使用开源权重 Phi-4，并通过 OpenCompass 运行以统一评测流程；生成的上下文化推理轨迹由 BGE-M3 编码器 $\mathcal{E}$ 映射到连续特征空间。实验分别在完整数据集的 $1\%$、$5\%$、$10\%$、$15\%$ 和 $20\%$ 预算下抽取核心集，其中 GPQA 不报告 $1\%$ 预算。评测日志来自 TinyBenchmarks 和 Open LLM Leaderboard；作者划出 $100$ 个互不重叠的模型作为测试集，并仅以另一组 $N=25$ 个模型训练历史依赖方法，较大的 $N\in\{50,100,200\}$ 被放入附录 C。每个子集分别配合 Standard Aggregation（SA）和 GP-IRT 两种解耦估计器，以区分选题质量与后续分数聚合器的影响；SA 使用选择方法给出的样本权重，或退化为无权经验均值。除 Random 运行 $20$ 次外，其余算法方法报告 $5$ 个独立随机种子的均值。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper proposes a chain-of-thought-aware coreset selection method that reduces the cost of LLM benchmark evaluation while preserving score estimates.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`4fa05303c3a5d8fada20a9adc6887fa216cff56257437d4ed6ed2f609963cf25`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
