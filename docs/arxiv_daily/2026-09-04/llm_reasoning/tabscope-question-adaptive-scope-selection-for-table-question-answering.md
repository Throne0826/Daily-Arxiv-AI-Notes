---
title: "[论文解读] TabScope: Question-Adaptive Scope Selection for Table Question Answering"
description: "[arXiv 2609.03395][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2609.03395"
announcement_date: "2026-09-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:39:28.743024+00:00"
source_sha256: "99213696685fd699594319bd841868ad6f237d355d948b0f0ce3a54bc3a54940"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "表格问答（TableQA）"
  - "大语言模型（LLM）"
  - "长表格推理"
  - "证据定位"
  - "问题自适应范围选择"
  - "表格分解"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.03395</p>

# TabScope: Question-Adaptive Scope Selection for Table Question Answering

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Yuxiang Wang, Junhao Gan, Jianzhong Qi</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: The University of Melbourne</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03395v1) · [PDF 下载](https://arxiv.org/pdf/2609.03395v1) · **关键词** 表格问答（TableQA）, 大语言模型（LLM）, 长表格推理, 证据定位, 问题自适应范围选择, 表格分解<br>


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

表格问答（Table Question Answering，TableQA）研究让模型根据自然语言问题，从给定表格中推断并生成答案。近年来，大语言模型（LLM）结合链式思维提示在该任务上表现较强，但表格变长后，模型需要从大量无关行列中识别少量支持证据，推理准确率通常下降。本文关注的核心背景问题是：表格范围不应始终固定为全表，而应根据问题所需的证据范围，在完整表格与问题相关的局部子表之间进行选择。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**表格问答（TableQA）**

输入是一张表格和一个自然语言问题，输出是由表格内容推导出的答案。问题可能要求查找单元格、比较若干实体、执行聚合，或综合分散在多行中的信息。

</div>
<div class="concept-item" markdown="1">

**证据定位与子表**

证据定位是从原始表格中找出支持答案的相关行和列；由这些行列组成的较小表格称为子表。局部化可以减少无关内容，但如果删去了问题需要的行列，也会造成检索或推理错误。

</div>
<div class="concept-item" markdown="1">

**操作感知的表格分解**

表格分解不是只依据词语相似度检索内容，而是结合问题隐含的操作需求来选择行列，例如查找、局部比较或聚合。其目标是生成既足够小、又保留完成答案所需信息的子表。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定原始表格 $T$ 与自然语言问题 $q$，系统需要输出答案 $a$，并在两种推理范围之间作出选择：直接使用完整表格 $T$，或先根据 $q$ 从 $T$ 中构造问题相关的子表 $T_q$，再基于 $T_q$ 推理。本文假设不同问题对证据范围的需求不同：依赖少量局部区域的问题适合局部化，而需要完整比较集合、较大聚合范围或分散信息的问题可能更适合保留全表。研究设置特别关注长表格，因为其中无关内容更多，固定采用全表或固定采用分解都可能失效。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$T$**

输入的原始表格。

</div>
<div class="notation-item" markdown="1">

**$q$**

输入的自然语言问题。

</div>
<div class="notation-item" markdown="1">

**$T_q$**

针对问题 $q$ 从原始表格 $T$ 中选择并细化得到的问题相关子表。

</div>
<div class="notation-item" markdown="1">

**$a$**

模型根据表格和问题生成的最终答案。

</div>

</div>

**直接相关的工作**

- **DATER（Ye et al., 2023）**: DATER 使用大语言模型同时分解表格和问题，并选择相关行列后进行下游推理，代表了通过证据定位降低长表格推理负担的路线。TabScope 与其相似之处在于都构造局部证据，但进一步强调证据选择应感知问题所需的操作，并先判断当前问题是否适合局部化。
- **Chain-of-Table（Wang et al., 2024）**: Chain-of-Table 在推理过程中迭代表格变换，把中间表格作为不断演化的推理状态；其他程序引导方法也可能使用 SQL 或 Python 执行完整操作链。TabScope 不要求生成完整的可执行操作程序，而是在必要时进行操作感知的表格分解，并在不适合局部化时直接保留全表。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在表格问答中，大语言模型需要从表格里找到支持答案的行和列，再完成查找、比较或聚合等推理。随着表格变长，大量无关内容会干扰证据识别并降低答案准确率；但简单地缩小表格也不总是安全，因为涉及大范围比较、完整聚合或分散证据的问题可能需要保留整张表。因此，系统必须针对每个问题控制送入推理模型的表格范围。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **全表推理**：将完整表格与问题一起交给大语言模型，通常配合思维链提示生成答案。该方式保留全部上下文，适合需要遍历许多行、比较多个实体或在完整取值域上聚合的问题。
- **固定式表格分解或局部化**：在回答前检索或筛选与问题相关的行和列，形成较小的子表，再让模型基于子表推理。其目的在于减少长表中的无关内容，使模型更容易聚焦于局部证据。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 两种固定策略都无法适配不同问题的证据范围：全表推理在长表上容易受到无关内容干扰，而一律局部化又可能删去大范围比较、完整聚合或跨多行推理所必需的信息，并额外引入检索错误。
- 现有评测条件不足以研究局部化是否正确：WikiTableQuestions等数据集通常只有表格、问题和最终答案，缺少支持答案的子表标注，难以直接衡量中间证据选择质量；同时，多数基准中的表格相对较小，对真实长表场景覆盖有限。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究主要关注如何对表格做分解，却没有充分解决局部化是否应当应用于当前问题这一上游决策，也缺少能够分别检验子表证据质量和长表问答能力的评测资源。论文因而聚焦于问题自适应的表格范围选择，并以银标参考子表和长表基准补足相应评估条件。

</div>
<div markdown="1"><span>核心问题</span>

对于给定的表格问答实例，模型应当何时先定位紧凑子表再推理，何时应保留完整表格进行推理？

</div>
<div markdown="1"><span>作者直觉</span>

问题本身能够暗示所需证据的覆盖范围：面向单个实体的查找或局部关系推理通常只依赖少量行列，删去其余内容可以降低干扰；涉及许多实体、全局比较或完整聚合的问题则需要更广覆盖。先依据问题类型选择推理范围，再仅在适合时进行面向操作的行列分解，有望同时获得局部化的聚焦优势和全表推理的上下文完整性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

TabScope的输入是表格$T$、问题$q$以及待生成的答案。系统先由基于大语言模型的分类器$C_{\theta}$预测问题类型，再由固定策略$\pi$结合问题类型和表格规模决定采用局部推理或全表推理；若选择局部推理，系统通过面向操作的检索、证据聚合和子表精炼构造问题相关子表$T^{\prime}$，最后由答案模型$M$基于$(q,T^{\prime})$或$(q,T)$生成答案。直观而言，TabScope不是一律“缩小表格”，而是先判断问题需要放大镜还是全景图，再选择相应的信息范围。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 问题类型与推理范围选择

分类器$C_{\theta}(q,T)$预测预定义问题类型$\hat{\tau}$，策略$\pi(\hat{\tau},s(T))$结合类型和表格规模状态$s(T)$选择$z\in\{\mathrm{local},\mathrm{full}\}$。

<div class="method-step__io" markdown="1">

**输入**：原始问题$q$和表格$T$。<br>
**输出**：局部推理或全表推理的范围决策$z$。

</div>

**直观理解**：系统先判断问题是查找少数记录，还是需要扫描大量记录。这个决策避免了把所有问题都强行压缩成小表，也避免让简单局部问题暴露于过多无关内容。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 面向操作的证据检索

分解器先识别问题所需的操作，如查找、过滤、比较或计数，再分别检索完成该操作所需的行集合和列集合；默认对同一问题采样$K=4$次检索结果。

<div class="method-step__io" markdown="1">

**输入**：问题$q$、完整表格$T$，以及局部推理决策$z=\mathrm{local}$。<br>
**输出**：多个候选行集合与列集合，以及每个候选的可靠性分数$s(c)$。

</div>

**直观理解**：它不只寻找和问题字面相似的单元格，而是思考“要完成这个问题必须做什么”。例如计数问题不仅需要最终计数，还要保留用于筛选和核验的条件列及相关记录。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 证据聚合与候选子表构造

将规范化后相同的行集或列集合并为候选组，以支持权重衡量重复出现和置信度；对高权重组逐步求并，枚举行列组合，并依据证据支持度与子表紧凑性选择得分最高的组合。

<div class="method-step__io" markdown="1">

**输入**：多次检索得到的候选行集、列集及可靠性分数。<br>
**输出**：候选行$R^{\prime}$、列$C^{\prime}$及初始子表$T^{\prime}=T[R^{\prime},C^{\prime}]$。

</div>

**直观理解**：一次检索可能漏掉证据或选入噪声，因此系统让多次检索“投票”。反复被选中的行列更可信，同时评分会惩罚过大的子表，使结果尽量小但不能牺牲必要证据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 子表精炼与答案生成

验证器检查$T^{\prime}$是否缺少回答所需的行、列或二者，并默认进行一轮补充；答案模型$M$随后根据$(q,T^{\prime})$或$(q,T)$生成答案。

<div class="method-step__io" markdown="1">

**输入**：问题$q$、完整表$T$和初始子表$T^{\prime}$；若选择全表推理，则直接使用$T$。<br>
**输出**：最终答案$\hat{a}$。

</div>

**直观理解**：精炼步骤像交卷前的证据核对：如果缩小后的表遗漏了关键记录，就把缺失内容补回。全表模式则跳过压缩，直接让答案模型在原表上推理。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 问题类型到推理范围的自适应选择

$$
\hat{\tau}=C_{\theta}(q,T),\qquad z=\pi\bigl(\hat{\tau},s(T)\bigr),\qquad z\in\{\mathrm{local},\mathrm{full}\}
$$

**符号说明**

- $\hat{\tau}$：分类器预测的问题类型。
- $C_{\theta}$：参数为$\theta$的基于大语言模型的问题类型分类器。
- $q$：输入问题。
- $T$：原始表格。
- $z$：最终推理范围，取局部$\mathrm{local}$或全表$\mathrm{full}$。
- $\pi$：根据问题类型和表格规模选择推理范围的固定策略。
- $s(T)$：表格规模状态或规模区间。

<div class="equation-explanation" markdown="1">

**直观理解**：该公式把两个决策分开：分类器回答“这是什么类型的问题”，固定策略回答“这种类型在当前表格规模下应看多大范围”。它的核心作用是让局部化成为按问题触发的选择，而不是所有样本都执行的固定操作。<br>
**原文位置**：第3.3节，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 候选子表的支持度与紧凑性评分

$$
S(R^{\prime},C^{\prime})=\frac{\mathrm{Support}(R^{\prime},C^{\prime})}{\rho(R^{\prime},C^{\prime})^{\alpha}},\qquad \rho(R^{\prime},C^{\prime})=\frac{|R^{\prime}|\cdot|C^{\prime}|}{|R|\cdot|H|}
$$

**符号说明**

- $S(R^{\prime},C^{\prime})$：候选行列组合的最终评分。
- $\mathrm{Support}(R^{\prime},C^{\prime})$：候选子表覆盖多次检索所支持行组和列组的程度；原文定义为$\sqrt{\mathrm{RowScore}(R^{\prime})\cdot\mathrm{ColScore}(C^{\prime})}$。
- $\rho(R^{\prime},C^{\prime})$：候选子表保留单元格数占原表单元格数的比例。
- $\alpha$：子表规模惩罚系数，原文给定范围为$[0.1,0.3]$。
- $R^{\prime},C^{\prime}$：候选选中行集合和列集合。
- $R,H$：原表的行集合和列标题集合。
- $|\cdot|$：集合中元素的数量。

<div class="equation-explanation" markdown="1">

**直观理解**：评分在“证据覆盖充分”和“表格足够紧凑”之间折中：反复被检索支持的行列会提高分数，而保留过多单元格会受到惩罚。系统选择$S$最高的行列组合形成最终分解表。<br>
**原文位置**：第3.4节，公式(5)；其中支持度定义见公式(4)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告TabScope是否对分类器、分解器或答案模型进行新的端到端参数训练，也未给出相应的损失函数或优化目标。方法描述表明，推理时使用基于大语言模型的分类、检索、验证和答案生成，并通过验证集离线分析确定固定策略$\pi$；因此能够确认的是策略选择过程，而不是一个明确的联合梯度优化过程。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 问题自适应范围选择器**

该模块由问题类型分类器$C_{\theta}$和固定类型到范围策略$\pi$组成。策略在验证集离线比较各问题类型上的局部与全表推理表现，并在表格规模改变时考虑首选范围是否发生变化；推理时模型只需预测$\hat{\tau}$，最终范围由$\pi$确定。

> 直观理解：把“是否缩小表格”从答案模型的临时判断变成显式决策。这样可以针对查找、排序等局部问题缩小范围，同时为全局计数或多实体比较保留完整表格。

**2. 面向操作的表格分解器**

分解器围绕问题所需操作联合检索行和列，而非仅依赖词汇重叠；随后分别聚合行组和列组，构造行列组合，并通过支持度与紧凑性评分选出子表。最终还由验证器检查并补充缺失证据。

> 直观理解：问题的答案形式不一定说明全部证据。例如“有多少支澳大利亚球队得分超过10分”需要国家、得分和球队标识列，以及所有满足条件的行，因此分解必须服务于过滤和计数过程。

**3. 多样本证据聚合与答案模型**

每次候选检索输出包含行集或列集，并可带有基于平均token对数概率计算的可靠性分数；相同规范化集合被合并后按支持权重排序。选择范围后，答案模型$M$只接收问题与选定表格输入，生成最终答案$\hat{a}$。

> 直观理解：多次检索相当于让几名检索员独立找证据，再根据一致性和置信度汇总。答案模型因此面对更稳定、与任务相关的输入，而不是一次可能不完整的检索结果。

**训练与推理**

在离线阶段，作者根据验证集上不同问题类型和表格规模下的局部推理与全表推理结果确定策略$\pi$。在推理阶段，给定$q$和$T$后，分类器预测$\hat{\tau}$并由策略决定范围；局部模式执行操作识别、$K=4$次候选检索、行列分别聚合、候选子表评分和默认一轮精炼，再由答案模型$M$生成$\hat{a}$；全表模式跳过分解和精炼，直接以$(q,T)$生成答案。

**复现信息**

表格表示为$T=(H,R)$，其中$H=\{h_1,\ldots,h_m\}$是列标题集合，$R=\{r_1,\ldots,r_n\}$是行集合，子表表示为$T^{\prime}=T[R^{\prime},C^{\prime}]$，其中$R^{\prime}\subseteq R$且$C^{\prime}\subseteq H$。证据聚合默认采样$K=4$个检索输出；若LLM提供生成置信度，则候选可靠性分数$s(c)$由平均token对数概率计算，否则设为$0$并退化为基于频次的投票。候选行列组合按支持度和紧凑性评分选择，规模惩罚系数$\alpha$的范围为$[0.1,0.3]$；这些设置足以解释复现实验中的检索稳定性、子表压缩程度和精炼行为。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- WikiTQ：标准表格问答基准，平均每个问题对应的表格含 6.4 列、25.4 行和 662.6 个序列化 token；训练集、验证集和测试集分别有 11,321、2,831 和 4,344 个问答对。论文用它进行常规问答评测、按表格大小分析以及按问题类型分析推理范围。
- SLQA：作者从 Spider 中序列化长度超过 4,096 token 的真实长表构建的新基准，平均含 11.0 列、733.8 行和 9,786.2 个 token；训练集、验证集和测试集分别有 1,324、239 和 1,110 个问答对。问题通过单元格、行、列或子表四种证据范围自适应生成，并经人工检查，用于专门检验长表条件下的问答能力。
- WTQ-SubTab：面向全部 4,344 个 WikiTQ 测试问题构建的银标子表资源，平均含 1.8 列、6.5 行和 104.8 个 token。它不向 TabScope 推理过程提供参考答案或银标证据，只用于离线评价行、列及单元格证据选择。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**问答准确率**

衡量模型最终答案正确的比例；论文用局部化准确率减去完整表 CoT 准确率得到差值，正值表示局部化更优。 （越高越好，因为它直接反映最终问答正确性；两种范围的差值则应结合问题类型判断，而非假定始终越大越好。）

</div>
<div class="metric-item" markdown="1">

**单元格级 F1、精确率、召回率与完全匹配率**

将预测子表与人工标注证据按单元格比较。精确率衡量所选内容中有多少确属必要证据，召回率衡量必要证据被覆盖多少，F1 平衡二者，完全匹配率要求预测范围与标注范围整体一致。 （均为越高越好；高精确率表示子表更紧凑，高召回率表示证据更充分，而完全匹配是最严格的范围一致性标准。）

</div>
<div class="metric-item" markdown="1">

**行 F1 与列 F1**

分别比较预测行集合、预测列集合与人工证据标注的重合程度，用于定位分解错误主要来自行筛选还是列筛选。 （越高越好，因为更高的 F1 表示在遗漏必要行列与保留冗余行列之间取得了更好的平衡。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### RQ1：在人工标注证据子集上比较三种银标子表构造方法

<div class="result-value" markdown="1">

直接生成并加入验证器修复后，单元格 F1 为 74.67%，单元格精确率为 85.58%，单元格召回率为 77.48%，单元格完全匹配率为 44.67%，行 F1 为 82.90%，列 F1 为 90.15%，六项指标均高于基于模式构造和未经修复的直接生成。

</div>

这一结果支持作者采用“直接选择行列，再由验证器检查并修复”的方式构造 WTQ-SubTab：它既减少无关证据，也提高必要证据覆盖率。需要注意，这里评估的是银标参考子表的构造质量，而不是 TabScope 在未知答案条件下的在线证据选择能力；构造过程可以访问参考答案，因此不能把这些分数直接视为实际推理时的检索性能。

<div class="result-source" markdown="1">

来源：表 10，Appendix E.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Direct Generation + Refinement | 74.67 | 85.58 | 77.48 | 44.67 | 82.90 | 90.15

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### RQ2：WikiTQ 验证集上按问题类型比较局部化推理与完整表 CoT

<div class="result-value" markdown="1">

局部化在查找、排序/最高最低、局部推理和计数差问题上分别领先 1.17、1.01、3.33 和 2.13 个百分点；完整表 CoT 则在一般计数、频次计数和比较问题上分别领先 2.40、2.68 和 1.24 个百分点。

</div>

结果表明表格变长并不意味着所有问题都应先截取子表。答案证据集中在少量记录附近时，局部化能够降低无关内容干扰；需要遍历大量记录、统计全局频次或跨实体比较时，过早裁剪反而可能遗漏证据。该比较说明“何时局部化”取决于推理操作，但逐类型差异只有约 1 至 3 个百分点，仍需结合样本量和统计不确定性审慎解释。

<div class="result-source" markdown="1">

来源：表 7，Appendix B

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Lookup | 86.51% | 85.34% | +1.17; Order/Superlative | 85.01% | 84.00% | +1.01; Local Reasoning | 69.90% | 66.67% | +3.33; Count-Diff | 76.60% | 74.47% | +2.13; Count-General | 79.78% | 82.18% | -2.40; Count-Frequency | 82.14% | 84.82% | -2.68; Compare | 67.90% | 69.14% | -1.24

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### RQ3：依据预测问题类型在局部子表与完整表之间自适应选择

<div class="result-value" markdown="1">

作者报告，自适应选择取得最佳总体表现；但所给节选未包含相应主结果表、具体数据集分数、提升幅度或显著性检验。

</div>

该结论与逐类型实验一致：固定全表会使局部问题暴露于过多无关内容，固定局部化又可能破坏全局计数和比较所需的覆盖范围，因此按问题类型切换具有合理性。不过，在缺少总体结果数值和与固定策略的完整对照时，只能将其视为作者的定性结论，不能据此判断优势大小、跨模型稳定性或统计可靠性。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Experiments on WikiTQ and SLQA show that localization is particularly effective for lookup and local reasoning questions, while adaptive selection between localized and full-table reasoning achieves the best overall performance.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给节选没有包含 TabScope 在 WikiTQ 和 SLQA 上的完整主结果表，因此无法核验“自适应选择取得最佳总体表现”的具体分数、相对提升、不同基础模型的一致性或统计显著性。
- 原文存在需要回查的内部不一致：Appendix E.2 正文称随机抽取 150 个 WikiTableQuestions 问答对进行人工标注，而表 10 标题称为 200 个；Appendix B 正文先称表 8 是 WikiTQ 的大表验证子集，表 8 标题却写作 SLQA。上述样本来源与规模会影响消融结论的可复现性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 完整表 CoT：把完整表格交给模型并进行思维链推理，是判断局部化是否真正减少长表干扰的直接对照；它也保留了全局计数和跨区域比较所需的完整证据。
- 局部化推理：先选出问题相关子表，再仅在该范围内回答。与完整表 CoT 的逐类型比较用于确定哪些问题适合缩小证据范围。
- 基于模式的银标构造：先生成与问题相关的模式元素和值，再据此检索原表中的行列，用于检验直接预测证据范围是否优于传统的两阶段模式检索。
- 直接生成银标子表：模型根据问题、参考答案和原表直接预测目标行列；与加入验证器修复的版本比较，可以隔离验证与修复步骤的贡献。

**实验想回答的问题**

- 操作感知的表格分解能否选出既紧凑又充分的证据，并在行、列和单元格层面接近人工标注的证据范围？
- 在长表问答中，局部化推理能否缓解无关内容造成的性能下降，以及按问题类型在局部子表与完整表之间自适应选择，是否优于固定使用单一范围？

**实验实现**

基础模型为 LLaMA-3.3-70B 和 GPT-5-mini，覆盖开源与闭源模型设置。开源模型通过基于 swift.llm 的本地后端和 HuggingFace 权重运行，GPT-5-mini 使用 OpenAI Chat Completions API。问答解码最多生成 2,048 个新 token，并使用模型默认输入预算；检索采样温度为 0.5，其余组件温度为 0。范围策略由 WikiTQ 验证集上的离线逐类型比较导出：查找、排序/最高最低、局部推理和计数差默认使用局部子表，一般计数、频次计数和比较默认使用完整表；对于大表，频次计数改用局部范围。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除或加入银标构造中的验证器引导修复 | 在直接生成基础上加入验证器修复后，单元格 F1 从 71.58% 提升至 74.67%，列 F1 从 84.55% 提升至 90.15%；同时，单元格精确率、召回率、完全匹配率和行 F1 也分别从 80.59%、75.25%、42.67% 和 80.38% 提升至 85.58%、77.48%、44.67% 和 82.90%。 | 该对照隔离了验证器的作用：验证器检查无效索引、证据缺失和冗余内容，再通过修复提示增删行列。六项指标同步上升，说明收益不是单纯扩大子表以换取召回，而是同时改善紧凑性和覆盖率。不过，这是离线银标构造组件的消融，不能证明在线 TabScope 使用同类验证器也会获得相同幅度的最终问答提升。 | 表 10，Appendix E.2<br><span class="experiment-evidence">Table 10 shows that direct generation substantially improves over schema-based construction. Verifier-guided refinement further increases all six metrics, raising cell F1 from 71.58% to 74.67% and column F1 from 84.55% to 90.15%.</span> |
| 在大表子集上重新检验问题类型与范围偏好的交互 | 查找和排序/最高最低仍偏向局部化，分别领先 1.39 和 0.53 个百分点；一般计数仍偏向完整表，局部化低 2.34 个百分点。频次计数则从总体验证集上局部化低 2.68 个百分点，转为大表子集上局部化高 2.22 个百分点。 | 这项分析隔离了表格规模对范围策略的影响。多数类型的偏好保持稳定，但频次计数发生反转，说明在极长表中，全表噪声或上下文负担可能超过局部化遗漏证据的风险，因此论文为大表频次计数单独指定局部范围。该结果只覆盖样本量足够的四类问题，不能外推到被省略的问题类型。 | 表 8，Appendix B<br><span class="experiment-evidence">Lookup \| 70.68% \| 69.29% \| +1.39; Order/Superlative \| 77.66% \| 77.13% \| +0.53; Count-General \| 76.83% \| 79.17% \| -2.34; Count-Frequency \| 84.44% \| 82.22% \| +2.22</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It proposes question-adaptive evidence scope selection to improve LLM reasoning over large tables.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`99213696685fd699594319bd841868ad6f237d355d948b0f0ce3a54bc3a54940`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
