---
title: "[论文解读] Baikal: Structured Search for Deep Research over Data Lakes"
description: "[arXiv 2607.27726][LLM Agent] Baikal 将异构数据湖上的深度研究重新表述为固定预算下的结构化搜索：先把表格与文本组织成语义区域，再依据已获得发现的质量，在区域之间自适应地平衡探索与利用。"
arxiv_id: "2607.27726"
announcement_date: "2026-07-31"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.152880+00:00"
source_sha256: "74396e8e18123c0bbdd760f66e705f1afd2e9138fd6fa4e4b5b37fc5a5ded3a9"
tags:
  - "LLM Agent"
  - "数据湖深度研究"
  - "大语言模型智能体"
  - "异构表格与文本"
  - "语义区域"
  - "预算搜索"
  - "探索—利用权衡"
  - "多臂老虎机"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2607.27726</p>

# Baikal: Structured Search for Deep Research over Data Lakes

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Agarwal, Dhruv, Mohan, Rishitha Guttapalle, Kumari, Aarti, Sinha, Ashi, Anil, Athulya, Srinivas, Kavitha, Samulowitz, Horst, McCallum, Andrew</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27726) · [PDF 下载](https://arxiv.org/pdf/2607.27726) · **关键词** 数据湖深度研究, 大语言模型智能体, 异构表格与文本, 语义区域, 预算搜索, 探索—利用权衡, 多臂老虎机<br>


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

Baikal 将异构数据湖上的深度研究重新表述为固定预算下的结构化搜索：先把表格与文本组织成语义区域，再依据已获得发现的质量，在区域之间自适应地平衡探索与利用。

**不用术语来说**：面对包含成千上万张表格和大量文本的数据湖，研究代理不仅要找到与问题直接相关的材料，还要主动发现问题的不同侧面，并最终写出有证据支撑的综合报告。可用的调查次数通常有限；如果代理一直沿着最先找到的线索继续追问，就可能反复收集相似信息，而遗漏其他重要主题。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者把数据湖深度研究形式化为预算受限的搜索问题，明确将“覆盖新主题”与“深入高价值线索”之间的取舍作为核心决策，而不再仅让不断累积的上下文隐式决定下一步调查方向。
- 作者提出 Baikal：将表格和段落联合嵌入并聚类为语义区域，以区域为搜索单位生成和回答有依据的子问题，再把发现的有据性、相关性、差异性和效用评分作为反馈，更新区域价值并指导后续选择。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究“数据湖上的深度研究”：大语言模型智能体面对由数千张关系表和大量文本段落组成的异构证据集合，需要把开放式分析请求拆成若干子问题，检索并处理相关证据，最后生成带有来源依据的长篇报告。该任务不仅要求跨表格与文本进行检索和推理，还要求在有限调查预算内覆盖查询的多个重要方面；已有文本到 SQL 和编码智能体主要增强了证据处理能力，而本文聚焦尚未被充分解决的“下一步应去哪里查”这一搜索决策问题。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**数据湖**

数据湖是集中保存大量异构数据的集合；在本文中，它同时包含关系表和描述性文本段落。智能体必须先从整个湖中定位相关材料，而不能假定目标数据集已经给定。

</div>
<div class="concept-item" markdown="1">

**语义区域**

语义区域是把表达相近主题的表格和段落联合嵌入后聚类形成的证据组。它把逐条材料的巨大搜索空间压缩成较有组织的主题空间，使一次命中可以带入同一区域内的其他相关证据。

</div>
<div class="concept-item" markdown="1">

**探索—利用权衡**

“利用”是继续调查当前看来高价值的区域，“探索”是尝试尚不确定但可能提供新观点的区域。固定预算下只做利用容易重复局部证据，只做探索又可能浪费步骤，因此本文把区域选择建模为预算受限的多臂老虎机式序贯决策。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括一个开放式分析查询，以及由大量关系表和非结构化段落构成的数据湖；不同证据可能在格式、主题和粒度上差异显著。系统先将全湖证据组织成语义区域；对每个查询，再保留包含 top-$k$ 初始检索结果的候选区域，并在总计 $B$ 个调查步骤内反复选择区域、提出由该区域支撑的子问题、通过区域范围内的 SQL 与文本分析形成发现。每项发现按事实依据性、相关性、差异性和实用性评分，该评分作为后续区域选择的反馈；最终输出是综合全部发现并将论断归因到证据来源的长篇研究报告。核心假设是调查预算有限，因此系统不能穷举整个数据湖，必须显式决定如何在不同语义区域之间分配搜索机会。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$B$**

单个研究查询允许执行的调查或子问题步骤总预算。

</div>
<div class="notation-item" markdown="1">

**$k$**

初始检索中用于确定候选语义区域的 top-k 结果数量；包含任一命中项的区域都会被保留。

</div>
<div class="notation-item" markdown="1">

**$\epsilon$**

贝叶斯 epsilon-greedy 区域选择策略中的探索参数，用于控制随机探索与选择当前高价值区域之间的比例。

</div>

</div>

**直接相关的工作**

- **DeepSearcher**: 代表按步骤交替执行检索与生成的深度研究系统；其后续调查方向主要由累积上下文推动，而本文将“选择下一处证据区域”改写为显式的预算搜索决策。
- **HybridQA 与 TAT-QA**: 二者原本提供表格—文本混合问答数据；本文据此构建包含大量表格与配套段落的数据湖测试环境，用于研究开放式、长报告式的深度研究，而非仅回答单个封闭问题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

组织内部的证据常存放在异构数据湖中，包括大量关系表以及解释这些表的非结构化文本。开放式分析请求往往涉及多个概念和证据来源，代理必须在有限的子问题预算内完成检索、数据处理、跨来源推理和报告综合；真正困难的不只是找到一条相关证据，而是系统覆盖查询的多个显著方面，同时保证结论可追溯到来源。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **迭代检索—生成式深度研究系统**：DeepSearcher 等方法循环执行检索、阅读和生成，让当前已积累的上下文改变模型对问题的理解，并据此决定下一轮搜索或子问题。该范式能够逐步深化已有线索，但搜索策略通常没有显式维护不同主题区域的价值与覆盖状态。
- **通用编码代理及其检索或聚类增强变体**：OpenCode 类代理利用代码、SQL 和文本检索工具分析数据；聚类变体还会把相近证据组织在一起，以便代理访问相关材料。不过，仅把聚类结果交给代理，并不等于建立了跨区域的顺序搜索机制，代理仍可能缺少根据调查反馈分配后续预算的明确策略。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 由累积上下文隐式驱动下一步调查容易产生局部过度利用：早期看似有希望的证据会持续吸引搜索预算，导致最终报告对查询的重要侧面覆盖不足。作者在引言中将其概括为“overexploiting locally-promising evidence”，并指出其表现是覆盖较差的低质量报告。
- 现有进展主要改善异构证据检索以及借助 SQL、代码代理处理证据，却没有充分解决固定预算下应当依次调查哪些语义方向的问题。即使预先对证据聚类，如果没有把发现质量反馈给区域选择策略，结构本身也难以保证多样且有用的调查结果；作者明确声称，把相同区域交给强编码代理并不能复现 Baikal 的收益。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种面向异构数据湖的显式搜索框架：它应把庞大的表格—文本集合转化为可管理的语义搜索空间，以区域为单位记录调查价值，并根据每轮发现的质量动态分配有限预算，从而同时控制主题覆盖与线索深挖。换言之，缺口不在于单次检索或单次推理能力，而在于如何对一系列研究行动进行结构化、可反馈的全局调度。

</div>
<div markdown="1"><span>核心问题</span>

在子问题数量固定的条件下，能否通过构建语义证据区域，并使用随机、LLM 引导、贝叶斯 $\epsilon$-greedy 或 Bayes-UCB 等区域选择策略，根据已有发现的质量连续更新搜索方向，从而比上下文驱动的迭代方法和仅使用聚类的编码代理生成更有据、覆盖更广且更有用的研究报告？

</div>
<div markdown="1"><span>作者直觉</span>

语义聚类先把原本扁平、庞杂的数据湖变成一张由若干主题区域组成的“地图”：一次检索命中某个条目时，代理也能看到同一区域内语义相近的表格和段落。随后，区域级策略像在有限次数内勘探多个地点：既会回到已经产出高质量发现的区域，也会为尚未充分调查的区域保留机会。以发现质量作为奖励，可使搜索方向由实际证据产出而非仅由模型当前上下文决定，因此更可能避免围绕单一线索反复追问。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Baikal把异构数据湖上的深度研究建模为有限预算下的结构化搜索。输入是研究问题$q$以及由关系表集合$\mathcal{T}$和文本段落集合$\mathcal{P}$组成的数据湖$\mathcal{L}=\mathcal{T}\cup\mathcal{P}$；系统先把两类证据编码到同一向量空间并聚成语义区域，再通过查询检索激活候选区域。在最多$B$个步骤中，区域选择策略反复选择一个候选区域，由LLM提出区域内可回答且不重复的子问题，研究代理用区域内SQL表和段落调查该问题，产生带引用的finding，并由LLM裁判给出质量奖励$r_t$以更新区域价值；最后只依据有效findings合成报告。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建查询无关的语义区域

使用同一个文本编码器将表与段落映射到共享向量空间，再由BERTopic依次执行UMAP降维和HDBSCAN密度聚类；噪声项及过小簇被丢弃，过大簇则用$k$-means拆分。每个保留区域$c$包含表集合$\mathcal{T}_c$、段落集合$\mathcal{P}_c$和由代表词生成的简短描述。

<div class="method-step__io" markdown="1">

**输入**：数据湖$\mathcal{L}=\mathcal{T}\cup\mathcal{P}$，其中每张表包含标题、列名和模式描述，每个段落包含标题和正文。<br>
**输出**：可复用的语义区域集合$\mathcal{R}$，满足$|\mathcal{R}|\ll|\mathcal{L}|$，且每个区域规模可放入代理上下文。

</div>

**直观理解**：这一步相当于先给大型仓库按主题分区，把讨论同一主题的表格和文字放在一起。之后搜索策略只需选择主题区，而不必直接在数十万条证据之间决策。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按查询激活候选区域

编码$q$后，分别按余弦相似度检索前$k$张表和前$k$个段落；只要区域$c$与任一检索结果重叠，就将其加入候选集$\mathcal{C}(q)$。一个高排名证据项可以激活其整个区域，因此同区域中低于Top-$k$截断线的相关证据也进入后续调查范围。

<div class="method-step__io" markdown="1">

**输入**：研究问题$q$、语义区域集合$\mathcal{R}$及全部证据的向量表示。<br>
**输出**：与$q$初步相关、供预算搜索使用的候选区域集合$\mathcal{C}(q)$。

</div>

**直观理解**：检索在这里不是直接决定最终证据，而是决定哪些主题区有资格被调查。这能扩大单条检索命中的作用，但检索未触达、被聚类判为噪声或因簇过小被删除的证据仍不可达。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 选择区域并生成区域内子问题

策略$\pi$从$\mathcal{C}(q)$选择区域$c$；若$S_c$为空，LLM依据$q$、$\mathcal{T}_c\cup\mathcal{P}_c$及该区域已问过的问题生成至多$K$个涵盖计数、比较、趋势或分布等角度的子问题，并过滤重复项。若仍无可用问题，则执行区域淘汰，将$c$移出候选集并在同一步重新选择；否则随机或通过LLM subquestion selection选出一个$s_t$。

<div class="method-step__io" markdown="1">

**输入**：候选集$\mathcal{C}(q)$、预算状态、各区域历史访问次数与奖励，以及区域尚未使用的子问题池$S_c$。<br>
**输出**：当前步骤待调查的区域$c$和单个子问题$s_t$，或经淘汰后缩小的候选集。

</div>

**直观理解**：策略先决定“去哪个主题区”，再决定“在该区问什么”。子问题池会跨访问保留，避免每次重访都重复规划；完全提不出相关问题的区域会被移除，而且不会白白消耗一个finding名额。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 区域约束调查与奖励反馈

研究代理在区域范围内执行SQL、阅读段落并返回带表或段落标识符引用的答案；可选的区域扩展根据$s_t$生成关键词，在全湖段落索引中用grep匹配少量补充段落并合并到$c$。LLM裁判依据证据扎根性、与$q$的相关性、相对既有findings的差异性和报告效用，为$f_t$给出$r_t\in[0,1]$，策略据此更新区域价值。

<div class="method-step__io" markdown="1">

**输入**：区域$c$、子问题$s_t$、区域内表和段落，以及此前findings $f_{1:t-1}$。<br>
**输出**：单个带证据引用的finding $f_t$、奖励$r_t$及更新后的搜索策略状态。

</div>

**直观理解**：选区之后，代理像被限制在一个专题资料夹中完成一次小型调查；区域扩展只补入子问题揭示出的缺失文本。奖励不仅判断答案是否正确相关，还会惩罚与先前内容重复的发现，因此已被充分挖掘的区域会逐渐失去吸引力。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 预算归一化的报告质量目标

$$
\max\;\frac{1}{B}\sum_{t=1}^{B}\rho\bigl(f_t\mid q,f_{1:t-1}\bigr)
$$

**符号说明**

- $B$：允许执行的调查步骤总预算；每一步至多产生一个finding。
- $t$：当前调查步骤的索引。
- $q$：用户给出的研究问题。
- $f_t$：第t步产生的finding，由子问题、答案及支持该答案的数据湖证据组成。
- $f_{1:t-1}$：第t步之前已获得的全部findings。
- $\rho(f_t\mid q,f_{1:t-1})$：取值位于[0,1]的finding质量函数，综合衡量证据扎根性、查询相关性、相对既有发现的差异性及报告效用。

<div class="equation-explanation" markdown="1">

**直观理解**：系统希望在固定$B$步内最大化每一步发现质量的平均值，而不是只追求某一次特别好的答案。由于$\rho$显式依赖$f_{1:t-1}$，同一区域反复提供相似内容时奖励会下降，搜索环境因此是非平稳的，并自然推动策略转向尚未覆盖的语义区域。<br>
**原文位置**：式(1)，第3.1节 Problem Formulation

</div>

</div>

<div class="equation-block" markdown="1">

#### Beta区域价值的软伪计数更新

$$
\alpha_c\leftarrow\alpha_c+w\,r_t,\qquad \beta_c\leftarrow\beta_c+w\,(1-r_t)
$$

**符号说明**

- $c$：当前被调查的候选语义区域。
- $\alpha_c$：区域c的Beta价值分布中的软成功参数。
- $\beta_c$：区域c的Beta价值分布中的软失败参数。
- $r_t$：第t步finding的LLM质量奖励，取值位于[0,1]。
- $w$：本次观测加入后验时采用的证据权重。
- $\mu_c=\alpha_c/(\alpha_c+\beta_c)$：区域c的Beta后验均值，用作其预期finding质量的估计。

<div class="equation-explanation" markdown="1">

**直观理解**：高奖励$r_t$主要增加$\alpha_c$，低奖励则主要增加$\beta_c$，从而改变区域$c$的预期价值和不确定性。论文明确说明这不是连续奖励下的严格共轭贝叶斯更新，而是把评分看成软Bernoulli证据的伪计数方案，供Bayes $\epsilon$-greedy和Bayes-UCB控制下一步搜索。<br>
**原文位置**：式(3)，第3.4节 Search via Region Selection

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：Baikal没有报告对编码器、研究代理或区域选择器进行端到端参数训练；式(1)是推理时的预算搜索目标和评价定义，而不是通过反向传播优化的训练损失。在线优化发生在单个查询的搜索过程中：LLM裁判计算$r_t=\rho(f_t\mid q,f_{1:t-1})$，Random策略忽略奖励，LLM策略把历史统计放入提示词，贝叶斯策略则按式(3)更新区域的Beta价值分布，并据此选择后续区域。这里的“学习”是有限预算内更新决策状态，不是跨数据集训练模型权重。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 异构证据区域化与候选前端**

表和段落由同一编码器联合嵌入与聚类，使同主题的结构化、非结构化证据落入同一区域；查询阶段通过表、段落各自的Top-$k$检索激活区域。区域构建与查询无关，因此每个数据湖只需预计算一次，但候选可达性同时受检索深度、噪声过滤和最小簇阈值限制。

> 直观理解：该模块把无法直接搜索的海量证据压缩为数量较少、带主题含义的“搜索臂”。其关键取舍是效率与召回率：候选区越少，搜索越便宜，但前端遗漏的证据不可能被后面的聪明策略补救。

**2. 区域调查代理**

LLM为当前区域维护去重后的子问题池，执行器仅访问该区域的SQLite表和段落，并必须返回所用证据标识符；完整配置采用OpenCode类编码代理，以支持SQL生成、执行错误修正和证据阅读。区域扩展允许依据具体子问题检索少量新段落，缓解静态聚类无法表达查询细微语义的问题。

> 直观理解：区域只规定“到哪里找”，调查代理才真正完成“问什么、怎么算、引用什么”。限制访问范围减少了上下文负担，而区域扩展提供了一条受控的补漏路径。

**3. 奖励驱动的区域选择策略**

每次选择区域相当于拉动多臂老虎机的一条臂，观察值是finding质量$r_t$；论文比较均匀Random、直接由LLM选择、带LLM先验的Bayes $\epsilon$-greedy和Bayes-UCB。贝叶斯策略先将LLM对每个区域的$n$次类别判断转成Beta参数$(\alpha_c,\beta_c)$，再用连续奖励进行软伪计数更新；$\epsilon$-greedy大多选择后验均值最大的区域，探索时从$\Pr(c)\propto\exp(\tau\mu_c)$采样，而Bayes-UCB选择最高后验上分位数的区域。

> 直观理解：这一模块解决固定预算应如何在“继续深挖看起来有价值的区域”和“尝试尚未充分调查的区域”之间分配。因为$B$与候选区域数可能同量级，仅靠在线试错来不及判断区域优劣，所以LLM先验用于在第一次调查前拉开区域价值估计。

**训练与推理**

离线预处理阶段，系统将全部表转换为标题、列名和模式描述文本，将段落转换为标题和正文文本，用共享编码器生成向量，并联合聚类为$\mathcal{R}$；该结果按数据湖缓存并复用于不同查询。在线推理时，系统检索$q$最相似的前$k$张表与前$k$个段落，构造$\mathcal{C}(q)$；若采用贝叶斯策略，还需让LLM对每个候选区域给出$n$个类别信念，并将其映射为$(\alpha_c,\beta_c)$。随后最多迭代$B$次：策略选区、维护或补充$S_c$、淘汰无法生成问题的区域、取出一个$s_t$、由区域约束代理调查得到$f_t$、由LLM裁判计算$r_t$并更新策略。最终在预算耗尽或候选集为空后，仅用有效$f_{1:B}$合成带证据归因的报告。

**复现信息**

论文实验中的共享嵌入器为Qwen3-Embedding-0.6B，语义区域由BERTopic、UMAP、HDBSCAN以及用于拆分过大簇的$k$-means构建；默认检索深度为$k=100$。区域内表被置于区域范围的SQLite数据库中，完整配置使用OpenCode类研究代理执行SQL和阅读段落，并可通过关键词加grep进行区域扩展。搜索预算为$B=50$个子问题findings，实验中每个查询平均约有$|\mathcal{C}(q)|\approx43$个候选区域；这一接近一比一的预算规模解释了为什么无先验的经典UCB会近似逐个访问未探索区域，也解释了贝叶斯策略需要查询条件化LLM先验。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HybridQA数据湖：从HybridQA构造的异构研究环境，包含10,993张表，并与约227K篇Wikipedia段落共同组成大规模证据湖；实验抽取15个查询。它主要检验系统能否在表格与百科文本并存、候选证据数量远超预算的条件下发现并整合相关证据。原文节选未明确报告查询抽样方式、训练/验证/测试划分及是否沿用HybridQA原始划分。
- TAT-QA数据湖：从TAT-QA构造的金融领域异构环境，包含2,757张表以及约13K篇金融报告段落；实验同样使用15个查询。它用于检验方法能否迁移到数值推理和财务文本占主导、规模小于HybridQA但证据类型不同的数据湖。原文节选未明确报告查询抽样与数据划分。
- 长预算补充评测集：从HybridQA查询中选择覆盖率处于低、中、高三个层次的3个查询，把预算从主实验的$B=50$扩展至$B=200$。该小规模设置专门测试区域策略在获得重复访问和利用区域的机会后能否真正拉开差距，而不是用于估计整体数据集上的平均性能。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**报告总分（report score）**

汇总整份报告质量的核心指标；原文指出该分数采用乘法组合，因此某一维度很高不能补偿另一维度很低。例如，高相关但缺乏数据湖证据支持的报告仍会得到较低总分。节选未给出完整计算公式和取值范围。 （越高越好，因为它要求报告同时满足多个质量条件，而不是仅优化表面相关性。）

</div>
<div class="metric-item" markdown="1">

**发现质量量规：groundedness、relevance、distinctness与utility**

GPT-5-mini逐项评价发现是否由数据湖证据支持、是否直接回答研究问题、是否提供区别于既有发现的新信息，以及是否值得写入最终研究报告。该组维度用于解释总分变化来自证据可靠性、主题贴合度、覆盖多样性还是实际用途。 （各维度均越高越好；但应联合阅读，因为实验显示检索—生成方法可能具有很高的相关性，却在证据支持和信息 distinctness 上较弱。）

</div>
<div class="metric-item" markdown="1">

**证据覆盖、累计发现分与成本**

gold表格/段落召回率衡量运行结束时触及了多少查询所需证据；累计发现分衡量每一步产生的有效研究价值并展示搜索轨迹；每查询成本及每个有效发现的成本衡量质量提升的资源代价。三者共同用于验证改进是否源于更合理的预算投放，而非只来自最终综合。 （证据召回率和累计发现分越高越好；在质量相当时成本越低越好，而每个有效发现的成本更适合判断额外支出是否真正换来了可用证据。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 两个数据湖、主预算$B=50$下的最终报告总分

<div class="result-value" markdown="1">

最佳Baikal在HybridQA上由Bayes-UCB取得0.46，相对该湖最强基线提升28%；在TAT-QA上由random与Bayesian $\epsilon$-greedy并列取得0.45，相对最强基线提升36%。四种策略中有三种在两个数据湖上都超过全部基线，但LLM-guided在HybridQA仅为0.35。

</div>

作者据此主张，显式探索语义区域在两种不同数据湖上都优于强检索代理，而且提升并非只由某一个精细策略产生。分析上，这支持“区域结构加预算循环”具有普遍价值；但每湖只有15个查询，且全部结果依赖自动评分，因此不能据此断言在所有数据湖、人工评审或其他模型上仍有相同比例的提升。LLM-guided的失败也表明，让LLM直接挑选看似安全的区域可能牺牲覆盖率。

<div class="result-source" markdown="1">

来源：第5.1节，Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The best Baikal configuration reaches a report score of 0.46 on HybridQA (Bayes-UCB) and 0.45 on TAT-QA (random and Bayes ε-greedy), improving on the strongest baseline for each lake by 28% and 36% respectively (Table 2).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 质量维度分解以及向OpenCode提供相同聚类结构的控制实验

<div class="result-value" markdown="1">

在HybridQA上，较强Baikal策略把groundedness提高到0.92，而OpenCode变体为0.72–0.73、DeepSearcher为0.31；distinctness提高到0.86，而OpenCode变体为0.62–0.67。与此同时，DeepSearcher在两个数据湖的relevance均为0.97，HybridQA上的OpenCode + Clustering相关性也高于Baikal，即0.81对0.73。相同结构使OpenCode在HybridQA从0.29升至0.36，却使其在TAT-QA从0.32降至0.27。

</div>

收益主要来自更可靠且彼此不同的证据，而不是让报告在措辞上更贴近查询。控制实验进一步说明，聚类产物并非可即插即用的充分条件：OpenCode拿到同样结构后表现不稳定，因此Baikal的顺序区域调查方式更可能是关键。不过，这仍是系统级对照，不能完全排除提示词、执行流程或其他未展示实现差异的影响。

<div class="result-source" markdown="1">

来源：第5.1节，Table 2；OpenCode结构控制结果见第5.1节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On HybridQA, the strongest Baikal policies raise groundedness from 0.72–0.73 for the OpenCode variants and 0.31 for DeepSearcher to 0.92, and distinctness from 0.62–0.67 to 0.86.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 搜索轨迹、证据覆盖与成本—质量分析

<div class="result-value" markdown="1">

Baikal在前10步内即与所有基线拉开累计发现分差距；在HybridQA上触及0.32–0.35的gold表格，而OpenCode变体为0.14–0.18、DeepSearcher为0.03。50步中，Baikal平均产生44.6个正量规得分发现，OpenCode为30.9、DeepSearcher为15.2。其每查询成本为$0.84–$1.41，高于基线的$0.33–$0.73$；但按有效发现归一化后，random Baikal为$0.019$，基线为$0.017–$0.022$。

</div>

这些结果把最终分数提升与搜索过程联系起来：Baikal更早把步骤投向有用区域，覆盖更多gold证据，并产出更多可用发现。它不是绝对更便宜，而是以较高总花费完成了更多有效调查；单位有效发现成本大致相当。因此适合将结论表述为“预算使用更有效且产量更高”，而不是“运行成本更低”。

<div class="result-source" markdown="1">

来源：第5.2节；Figure 2；补充材料Table 6与Table 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Out of 50 steps on HybridQA, Baikal yields 44.6 findings with a positive rubric score, against 30.9 for OpenCode and 15.2 for DeepSearcher (Table 7 in supplementary), and the baselines are far more variable across queries (±3.8–7.4 versus ±1.3–2.8).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- DeepSearcher：代表典型的迭代检索—生成式深度研究方法，由累积上下文决定后续调查方向。它是关键对照，因为论文的核心主张正是显式区域搜索能缓解此类方法贴近当前局部证据、但覆盖不足的问题。
- OpenCode研究代理：具备检索能力的通用研究代理，用来判断Baikal是否只是受益于更强的子问题执行代理，而非其区域化预算分配机制。
- OpenCode + Clustering：向OpenCode提供与Baikal相同的检索和聚类产物。该对照控制了语义区域结构本身，从而检验仅把聚类结果交给代理是否足以复现Baikal的提升。
- Baikal内部区域选择策略：random、LLM-guided、Bayesian $\epsilon$-greedy和Bayes-UCB并非外部基线，而是同一框架下的策略对照。它们分别测试无学习选择、LLM直接判断、带随机探索的贝叶斯价值利用以及对高不确定性区域保持乐观探索的效果。

**实验想回答的问题**

- 在相同子问题预算下，把异构证据组织成语义区域并显式分配区域搜索预算，是否比迭代式检索—生成代理产生更高质量、更有依据且覆盖面更广的研究报告？
- Baikal的收益究竟来自预先提供的聚类结构，还是来自在语义区域之间进行顺序预算分配；不同区域选择策略的优势又会如何随搜索预算变化？

**实验实现**

主评测在两个数据湖上各使用15个查询，并把研究预算固定为$B=50$步，以比较Baikal各区域策略、DeepSearcher和OpenCode变体。报告及中间发现由GPT-5-mini依据四维量规评分；均值的不确定性以查询级bootstrap的95%置信区间报告，消融表采用10,000次配对重采样，并给出置信区间半宽。为检查自动裁判的可复现性，作者按得分分层抽取80条发现，交由独立的Claude Opus 4.6重新评分；groundedness使用Gwet’s $AC_1$，有序维度使用二次加权$AC_2$。此外，作者在3个覆盖层次不同的HybridQA查询上把预算扩展至$B=200$，并比较Bayes-UCB与随机搜索。节选未明确报告生成模型的完整配置、检索参数、重复运行次数和硬件环境。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 从random Baikal完整栈中依次移除研究代理（RA）、区域扩展（RE）和LLM子问题选择（LSS） | 完整系统在HybridQA/TAT-QA上的报告分分别为0.44/0.45；移除RA后为0.40/0.39，再移除RE后为0.37/0.36，最后移除LSS后为0.36/0.35。对应地，RA分别贡献0.04和0.06，RE再贡献0.03和0.03，LSS最后仅贡献0.01和0.01。 | 这是累积移除而非每个组件独立移除，因此差值反映组件在当前剩余栈中的边际作用，不能简单视为可加且无交互的因果贡献。结果显示RA与动态补充段落都有稳定作用，但只保留语义区域和随机子问题选择的基础版本仍接近或达到最强基线，说明区域化搜索是性能地基，附加模块主要提供增量改进。 | Appendix A，Table 4<br><span class="experiment-evidence">Removing the research agent costs 0.04 and 0.06 report score on HybridQA and TAT-QA, region expansion a further 0.03 on both, and LLM subquestion selection a final 0.01 (Table 4); what remains—regions with random selection—still scores 0.36 and 0.35, so the rest of the stack adds 0.08–0.10 on top of a foundation already as strong as the best baseline.</span> |
| 将搜索预算从$B=50$扩展到$B=200$，在3个不同覆盖层次的HybridQA查询上比较Bayes-UCB与random | 在$B=200$时，Bayes-UCB相对random的累计发现分平均增加5.61点，即8.8%；而在主实验$B=50$时，多种Baikal策略较难区分。 | 该实验隔离了“策略是否需要足够预算才能利用历史奖励”的问题。较大预算允许算法重复访问高价值区域，因此不确定性驱动的Bayes-UCB开始优于均匀随机选择。这说明$B=50$下策略接近不代表策略无效，但结论仅来自3个特意覆盖低、中、高覆盖率的查询，证据强度低于完整主实验。 | 第5.2节，Figure 3<br><span class="experiment-evidence">Extending the budget to 200 on three HybridQA queries spanning the coverage strata does separate them: Bayes-UCB gains 5.61 points (8.8%) in cumulative finding score over random (Figure 3), so the comparison at B=50 understates rather than flatters the value of optimistic region selection.</span> |

**定性案例**

- Figure 3可视为搜索行为案例：作者选择3个分别代表低、中、高证据覆盖率的HybridQA查询，绘制Bayes-UCB相对random在预算推进过程中的配对累计发现分差。到$B=200$时平均优势为5.61点（8.8%），支持“乐观区域选择需要多次访问机会才会显效”的机制解释；但节选未提供每个查询的主题、逐步选择了哪些区域或具体发现内容，因此它是轨迹级案例而非可审查的语义级案例。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出面向异构数据湖深度研究智能体的预算化结构搜索框架，以区域级探索利用策略指导检索和报告生成。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`74396e8e18123c0bbdd760f66e705f1afd2e9138fd6fa4e4b5b37fc5a5ded3a9`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
