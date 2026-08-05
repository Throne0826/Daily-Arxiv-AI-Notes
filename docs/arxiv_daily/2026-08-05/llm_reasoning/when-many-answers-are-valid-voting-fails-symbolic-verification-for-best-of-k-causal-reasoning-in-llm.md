---
title: "[论文解读] When Many Answers Are Valid, Voting Fails: Symbolic Verification for Best-of-K Causal Reasoning in LLMs"
description: "[arXiv 2608.03506][LLM Reasoning] 本文将多答案因果推理中的候选选择，从“哪个答案出现最多”改写为“哪个推理轨迹最符合可判定的因果图公理”，并提出无需训练的符号验证器 CALVER。"
arxiv_id: "2608.03506"
announcement_date: "2026-08-05"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:38:20.170964+00:00"
source_sha256: "cbff0b74f4d0e496eb8daf273c43c538a2a047e980a98fdf55963782030f2c91"
tags:
  - "LLM Reasoning"
  - "大语言模型"
  - "因果推理"
  - "测试时计算"
  - "Best-of-K选择"
  - "符号验证"
  - "自一致性"
  - "d-分离"
  - "后门准则"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.03506</p>

# When Many Answers Are Valid, Voting Fails: Symbolic Verification for Best-of-K Causal Reasoning in LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Omatharv Bharat Vaidya, Connor Thomas Jerzak, Zayne Rea Sprague, Fangcong Yin, Nhat Ho</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> The University of Texas at Austin；New York University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03506v1) · [PDF 下载](https://arxiv.org/pdf/2608.03506v1) · **关键词** 大语言模型, 因果推理, 测试时计算, Best-of-K选择, 符号验证, 自一致性, d-分离, 后门准则<br>


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

本文将多答案因果推理中的候选选择，从“哪个答案出现最多”改写为“哪个推理轨迹最符合可判定的因果图公理”，并提出无需训练的符号验证器 CALVER。

**不用术语来说**：面对一道可能有多个正确答案的因果题，语言模型反复作答后，正确答案往往分散成多种写法或不同集合，而某个常见但错误的答案反而可能出现得最频繁。因此，简单投票不一定能从已有回答中选出正确项，增加采样次数甚至会不断强化同一种错误。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者把具有多个合法答案的 best-of-$K$ 选择形式化为对“可判定有效性类别”的聚合：候选之间不必文字一致，只要分别满足题目要求的因果图条件，就应被视为有效。
- 作者提出 CALVER，将有向无环图和无环有向混合图上的祖先限制、$d$-分离、$m$-分离、干预图手术及后门准则编译为六槽推理轨迹的确定性评分规则；该验证器无需训练，也不依赖参考答案或特定采样模型。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型的测试时计算与因果图推理交叉领域。链式思维提示让模型输出显式推理轨迹；测试时方法通常从同一模型采样多条轨迹，再用自一致性（即答案多数投票）或评分器选出最终答案。这类聚合隐含假设是：正确轨迹比错误轨迹更集中于同一个答案。但在因果推理中，一个问题常有多个形式不同却同样满足图判据的答案，例如多个变量集合都能阻断指定路径或满足后门准则。因此，正确概率会分散到多个答案字符串上，而一种重复出现的错误可能成为相对多数。本文关注的核心背景不是如何生成更多推理，而是如何在固定候选池中依据可判定的因果有效性选择答案。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**因果图**

因果图用节点表示变量、用边表示变量间的因果或潜在混杂关系；有向无环图（DAG）只含有向边且不存在有向环，无环有向混合图（ADMG）还可用双向边表达未观测混杂。本文假设因果结构由题目直接提供，或可先从文本中构建。

</div>
<div class="concept-item" markdown="1">

**d-分离与m-分离**

$d$-分离是依据DAG中的路径结构和给定条件变量集合，判断两个变量是否被图结构所分离的规则；$m$-分离是其在ADMG上的扩展。它们把部分条件独立性判断转化为确定性的图算法，因此可以用来核验候选答案。

</div>
<div class="concept-item" markdown="1">

**后门准则与干预**

后门准则判断一个调整变量集合能否阻断处理变量与结果变量之间由共同原因造成的非因果关联，从而识别因果效应。干预通常通过图手术表示，例如对变量实施干预时删除所有指向该变量的入边，再在修改后的图上检查相关关系。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个因果推理问题、相应的因果结构，以及语言模型独立采样得到的$K$条结构化推理轨迹，任务是在不查询参考答案、也不重新训练生成模型的条件下，从同一冻结候选池中选择一个最终答案。问题包括寻找任一满足指定图谓词的变量集合，例如满足后门准则的调整集或使变量$d$-分离的条件集；此时正确输出并不唯一。本文的设定要求相关有效性能够通过祖先子图限制、$d$-分离或$m$-分离、干预图手术和后门检验等标准图计算来判定。CALVER把每条候选轨迹解析为六个有类型的槽位，对各槽位执行确定性检查并计算分数，最后选择最早出现的最高分轨迹并返回其抽取答案。该设定覆盖DAG与ADMG，也讨论阈值化平均处理效应决策；其关键前提是存在可用的因果结构，而该结构可以直接给出或由文本构建。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$K$**

测试时从语言模型采样并参与选择的候选推理轨迹数量。

</div>
<div class="notation-item" markdown="1">

**$X$**

因果查询中的处理变量或干预变量。

</div>
<div class="notation-item" markdown="1">

**$Y$**

因果查询中的结果变量。

</div>
<div class="notation-item" markdown="1">

**$\varnothing$**

空变量集合；在示例中表示不使用任何调整变量，可能成为高频但无效的候选答案。

</div>

</div>

**直接相关的工作**

- **Wang et al. (2023), Self-consistency improves chain of thought reasoning in language models**: 该工作通过采样多条链式思维轨迹并返回最频繁答案进行测试时聚合，是本文直接质疑的基线范式。本文指出，当多个有效答案分裂选票时，精确字符串多数投票可能选择高频错误答案。
- **Chen et al. (2024), CLEAR: can language models really understand causal graphs?**: CLEAR提供本文使用的因果图推理场景，尤其包含只需找出任一有效答案的查询；这类查询可能同时接受多个调整集或分离集，直接体现答案多重性问题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型常通过增加推理时计算来提升复杂推理能力，即采样 $K$ 条思维链后再选择答案。因果推理却经常要求“找出任意一个满足条件的集合”，例如多个调整集都可能满足后门准则。此时系统需要从一批表达不同、质量不一的轨迹中识别任何真正符合因果条件的候选，而不能把字符串共识误当成正确性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **自一致性与精确多数投票**：从模型采样多条推理轨迹，抽取最终答案，并返回出现次数最多的答案；其隐含前提是正确推理会比错误推理更集中地指向同一个输出。
- **通用候选评分或直接形式化求解**：前者利用模型置信度、学习式奖励模型或大语言模型裁判对固定候选池排序；后者先从文本构造一个因果图等形式对象，再调用图算法精确求解，而不在原候选池中进行选择。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 精确投票无法合并语义上不同但分别合法的答案：有效概率会分散到多个答案字符串上，而重复出现的同一种混杂错误可能成为最大单一众数。因此，更大的 $K$ 不保证纠正错误，反而可能更稳定地选中该错误众数。
- 通用评分器没有把 Pearl 因果准则直接作为判定依据，因而可能偏好措辞可信但图结构上无效的轨迹；直接求解则依赖一次性构造出足够可靠的形式图，当不同轨迹对文本中的因果关系有不同但局部有用的解释时，单图抽取可能丢失候选级信息。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有推理时选择方法缺少一种面向多合法答案的机制：它应在不查询基准参考答案、不重新训练模型的条件下，依据题目给定或由文本构造的因果结构，逐候选判断其是否属于同一合法答案类别，并保留不同轨迹中分别正确的局部因果解释。

</div>
<div markdown="1"><span>核心问题</span>

当因果题允许多个图上合法答案时，能否把标准因果图判据编译为一个训练无关的 best-of-$K$ 验证与选择规则，使其在同一冻结候选池上比投票和通用评分器更可靠；同时，候选级验证在什么条件下应优于“先构造一个图、再精确求解”的架构？

</div>
<div markdown="1"><span>作者直觉</span>

造成答案多样性的因果性质本身也提供了检验答案的规则。例如，一个候选调整集是否阻断所有相关后门路径，可以通过图算法确定，而不需要观察它是否与其他候选写得一样。CALVER 因而不统计“有多少人给出同一个答案”，而是分别检查每条轨迹是否正确描述变量、关系、条件集合与干预，并选择满足最多因果约束的候选。通俗地说，它把选举改成了逐份验算：多个不同答案只要各自通过规则检查，就不会因分票而受到惩罚。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CALVER（Causal Axiom-Level VERification）把 best-of-$K$ 从“统计哪个答案出现最多”改为“逐条检查哪份推理最符合可执行的因果规则”。输入是查询 $q$、$K$ 条独立采样的结构化推理轨迹，以及题目直接提供或轨迹自行构造的图；验证器不读取标准答案，而是检查每条轨迹的图、查询、策略、推导记录、计算结果和最终答案，得到六位证书分数 $S_i$，最后返回最高分轨迹的答案。在 ATE 任务中，它还依据观测分布 $P$ 独立重算调整公式，并检查阈值决策是否与数值结果一致。

该方法的关键是让“多个表述不同但都有效的答案”不再彼此分票：CALVER 比较的是候选是否满足因果公理，而不是答案字符串的频率。若题目给出真实图，则所有候选在同一图 $G^{\star}$ 上验证；若结构只能从文本推断，则第 $i$ 条轨迹提交自己的图 $\widehat{G}_i$，验证器只检查其内部一致性，隐藏的源图 $G^{\star}$ 仅在选定候选后用于最终评分。因此，构图模式能防止选择器偷看标签，但其可靠性也取决于候选图是否保留了与查询有关的混杂、后代和分离关系。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成并解析候选池

策略模型独立生成 $K$ 条轨迹 $r_1,\ldots,r_K$，并从每条轨迹提取答案 $a_i=a(r_i)$。每条轨迹按类型化契约填写 graph、query、strategy、derivation record、computed result 和 answer 六个槽位，缺失或重复槽位会使相应检查失败。

<div class="method-step__io" markdown="1">

**输入**：查询 $q$，题目给出的因果图或图的文本描述；ATE 题还包括观测分布 $P$ 与阈值 $\tau$。<br>
**输出**：冻结的候选池 $\{r_i,a_i\}_{i=1}^{K}$，以及可供程序解析的中间因果声明。

</div>

**直观理解**：模型不是只交一个简短答案，而是同时提交一份格式固定、可以逐项验算的“解题单”。冻结候选池保证 CALVER、投票或其他选择器比较的是完全相同的模型输出。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 确定逐候选验证图

在 supplied-graph 模式中令 $G_i^{\mathrm{ver}}=G^{\star}$；在 constructed-graph 模式中，轨迹从文本构造 $\widehat{G}_i$，并令 $G_i^{\mathrm{ver}}=\widehat{G}_i$。后一模式在选择完成前不向任何选择器暴露 $G^{\star}$。

<div class="method-step__io" markdown="1">

**输入**：第 $i$ 条轨迹、题目格式，以及可能直接提供的源图 $G^{\star}$。<br>
**输出**：每条轨迹对应的验证图 $G_i^{\mathrm{ver}}$。

</div>

**直观理解**：有现成图时，所有考生用同一张题图验算；只有文字时，每个考生先画自己的图，再检查其答案是否由这张图推出。隐藏真实图避免验证器间接使用标准答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行六项因果证书检查

验证器依次产生六个二值结果 $b_{ij}$：图能否解析并绑定实例、查询是否匹配、所提策略是否图上有效、推导记录是否使用声明的类型化操作、计算值能否被独立重算、最终答案是否由重算结果推出。不同任务调用预先固定的检查器，例如后门调整使用切断 $X$ 出边后的 $d$-分离，ADMG 使用类型化 $m$-分离，ATE 则重算调整泛函。

<div class="method-step__io" markdown="1">

**输入**：轨迹 $r_i$、验证图 $G_i^{\mathrm{ver}}$ 与查询 $q$；数值 ATE 任务还输入 $P$、$\tau$ 和预先声明的容差 $\varepsilon$。<br>
**输出**：六位检查向量 $(b_{i1},\ldots,b_{i6})$ 及总分 $S_i$；$S_i=6$ 表示六项部署检查全部通过。

</div>

**直观理解**：这相当于检查一条证明的六个环节，而不是只看最后一句。即使答案碰巧正确，只要图、策略或中间计算无法支撑它，也不会获得完整证书。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 确定性选择与最终输出

选择分数最大的候选；若并列，则固定选择最早出现的轨迹。正确性字段和基准参考答案在打分前由机械隔离层移除，只有选定索引后才重新接入并用于外部评测。

<div class="method-step__io" markdown="1">

**输入**：所有候选的分数 $S_1,\ldots,S_K$ 及其答案。<br>
**输出**：索引 $i^{\star}$ 与最终答案 $a_{i^{\star}}$。

</div>

**直观理解**：CALVER 选的是“因果证明最完整”的候选，而不是“说得最多”的答案。固定并列规则与标签隔离使选择过程可复现，并排除利用标准答案打分的可能。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 六位证书评分与确定性选择

$$
b_{ij}=b_j(r_i;G_i^{\mathrm{ver}},q)\in\{0,1\},\qquad S_i=\sum_{j=1}^{6}b_{ij},\qquad i^{\star}=\min\!\left(\operatorname*{arg\,max}_{1\le i\le K}S_i\right)
$$

**符号说明**

- $r_i$：候选池中的第 i 条结构化推理轨迹
- $G_i^{\mathrm{ver}}$：第 i 条轨迹所使用的验证图；可为源图或该轨迹自行构造的图
- $q$：题目要求回答的因果查询
- $b_{ij}$：第 i 条轨迹在第 j 项契约检查上的二值通过标记
- $S_i$：第 i 条轨迹通过的检查总数，最大部署分数为 6
- $K$：同一问题独立采样的候选轨迹数量
- $i^{\star}$：最终选中的候选索引；最高分并列时取最小索引

<div class="equation-explanation" markdown="1">

**直观理解**：每条轨迹要过六道可执行检查，每过一项得一分；选择器取总分最高者，并用最早出现作为固定的并列决策。该式正式定义了 CALVER 如何聚合候选，整个过程只依赖轨迹、查询和验证图，不依赖目标标签。<br>
**原文位置**：Method，Graph-dependent verification；Table 1

</div>

</div>

<div class="equation-block" markdown="1">

#### ATE 后门调整重算与严格决策条件

$$
\psi(P;X,Y,Z)=\sum_z\Bigl[P(Y=1\mid X=1,Z=z)-P(Y=1\mid X=0,Z=z)\Bigr]P(Z=z),\qquad |\widehat{\theta}_i-\psi(P;X,Y,Z)|\le\varepsilon;\quad Z\cap\bigl(\{X,Y\}\cup\operatorname{De}_G(X)\bigr)=\varnothing,\quad X\perp_d Y\mid Z\ \text{in }G_{\underline X},\quad |\psi(P;X,Y,Z)-\tau|>\varepsilon
$$

**符号说明**

- $\psi(P;X,Y,Z)$：依据观测分布和调整集计算的后门调整泛函
- $P$：题目提供的观测联合分布
- $X$：二元处理变量
- $Y$：二元结果变量
- $Z$：候选后门调整变量集合
- $\widehat{\theta}_i$：第 i 条轨迹在 computed-result 槽位报告的 ATE
- $\varepsilon$：评测前声明的数值容差
- $\operatorname{De}_G(X)$：图 G 中处理变量 X 的严格后代集合
- $G_{\underline X}$：删除所有从 X 发出之箭头后的图
- $\tau$：用于判断 ATE 是否足够大的题目阈值

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分按每个协变量取值分层，计算处理组与对照组的结果概率差，再按该层在人群中的概率加权。严格证书不仅要求模型报告值与重算值接近，还要求 $Z$ 不包含处理、结果或处理的后代，确实阻断后门路径，并让效应与阈值保持超过误差容限的距离；在图与分布正确且满足正值性时，这些条件可保证最终阈值判断正确。<br>
**原文位置**：Method，Graph-dependent verification，公式 (1)、公式 (2)；Theory，Theorem 1

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。CALVER 是无需训练的符号选择器，没有参数学习、梯度更新或额外监督目标；语言模型只负责生成冻结候选，CALVER 在推理阶段用预先规定的离散检查和确定性规则评分。因此，证书分数 $S_i$ 是候选选择准则，而不是用于反向传播的训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 类型化轨迹契约**

契约把自然语言推理映射为六个机器可读槽位：graph、query、strategy、derivation record、computed result 和 answer。推导记录只检查来源与格式，其余五项承担主要语义验证；缺失或重复字段直接使对应位为零。

> 直观理解：纯自然语言很难可靠验算，因此方法要求模型把关键主张放进固定表格。它不限制外围解释怎么写，但确保图、方法、数值和答案可以分别核对。

**2. 图依赖的因果检查器**

检查器按任务族预先固定，包括后门调整、带类型的条件独立、媒介变量见证、干预可达性和数值 ATE。以后门为例，候选调整集 $Z$ 必须在删除 $X$ 所有出边的图 $(G_i^{\mathrm{ver}})_{\underline{X}}$ 中使 $X\perp_d Y\mid Z$；对于含双向边的 ADMG，则使用 $m$-分离。

> 直观理解：检查器把 Pearl 因果准则变成可执行程序，用图上的路径关系判断候选是否真正阻断了混杂。这样做不需要知道基准列出的答案，因为同一道题可能存在多个有效调整集。

**3. ATE 独立重算与严格证书**

对于二元处理 $X$ 和结果 $Y$，验证器用候选调整集 $Z$ 与观测分布 $P$ 重算 $\psi(P;X,Y,Z)$，要求轨迹报告值 $\widehat{\theta}_i$ 与其误差不超过 $\varepsilon$，并检查最终判断是否等于 $\mathbf{1}\{\widehat{\theta}_i>\tau\}$。严格 ATE 证书还排除 $X$、$Y$ 及 $X$ 的后代进入 $Z$，要求后门 $d$-分离成立，并要求重算效应距阈值超过 $\varepsilon$。

> 直观理解：模型不能只声称某个调整集和数值正确，验证器会自己重新计算。额外的阈值间隔保证小数值误差不会把“超过阈值”和“未超过阈值”翻转。

**训练与推理**

训练阶段：原文方法不训练 CALVER，也不为特定基准微调验证器；各任务族的有效性检查、数值容差 $\varepsilon$、并列规则和字段隔离规则在评测前固定。推理阶段：策略模型针对每题独立采样 $K$ 条符合轨迹契约的候选；系统按题目格式为每条候选指定 $G_i^{\mathrm{ver}}$，执行六项检查并求得 $S_i$；ATE 候选还由程序从 $P$ 独立重算调整泛函。最后按 $i^{\star}=\min(\arg\max_i S_i)$ 选择答案，之后才恢复隐藏的正确性与参考答案字段进行外部评分。constructed-graph 模式中的最终正确性仍相对于隐藏源图 $G^{\star}$ 判断，而 CALVER 的选择分数仅表示候选相对于其自建图 $\widehat{G}_i$ 的有效性与内部一致性。

**复现信息**

公平比较需要复用同一批冻结候选，且所有选择器在运行前都不能访问正确性标签或基准参考答案。图、查询和六个槽位必须采用可确定解析的类型化表示；任务对应的后门、$d$-分离、$m$-分离、干预可达性或真值表检查器应在评测前固定。复现 ATE 部分还必须预先声明 $\varepsilon$，实现对 $\psi(P;X,Y,Z)$ 的独立计算，并区分普通六位满分与加入处理排除、后门分离和决策间隔条件的严格 ATE 证书。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 主要数据集是 CLEAR 的 find-one-valid 任务之“typed clean core”：原始 480 道题中，有 126 道同时满足“公开任务允许多个有效对象”以及“论文实现了与该图类型兼容的判定谓词”。筛选规则在生成候选之前固定；只要所选对象满足谓词，即使不同于数据集列出的示例答案也算正确。supplied-graph 设置直接给出因果图，主要用于隔离并检验候选选择能力。
- 外部因果迁移使用 bnlearn 仓库中的 10 个已发表贝叶斯网络。实验既直接提供 DAG，也把网络改写为三个文本难度：L1 明示每条边，L2 明确描述机制，L3 使用含干扰信息的自然叙事。其作用是分别测试新图结构上的零样本迁移，以及当模型必须先从文本恢复图时，候选级验证能否继续优于投票。
- 跨领域迁移使用动态生成的 K&K 骑士与无赖逻辑谜题，每种 3、4、5 人规模均有 180 个 problem-seed 单元。模型输出命题形式化，选择器以真值表一致性替代因果图谓词，用于检验“按可执行有效性选择”是否是超越因果推理的通用机制。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**选择准确率**

在 problem-seed 层面，选择器最终挑出的对象满足任务判定谓词的比例；CLEAR 允许任何图上有效对象，而不要求与数据集示例逐字一致。 （越高越好，因为它直接衡量在固定候选池中找到有效答案的能力。）

</div>
<div class="metric-item" markdown="1">

**相对基线的百分点增益及配对 95% 置信区间**

CALVER 准确率减去同一 problem-seed 单元上基线准确率，以百分点表示；区间通过按源问题聚类的配对 bootstrap 得到。 （增益越大越好；若置信区间不跨 0，说明观察到的优势在该重采样分析下较稳定。）

</div>
<div class="metric-item" markdown="1">

**精确图恢复率**

在 graph-from-text 设置中，从文本重建出的完整图与源图完全一致的比例，用于刻画文本到图转写的难度，而不是直接作为最终答案准确率。 （越高表示完整结构抽取越可靠；较低时 CALVER 仍可能依靠与当前查询有关的局部关系验证候选。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### CLEAR clean core 的八种策略，固定 $K=8$，CALVER 对比集合 Jaccard medoid

<div class="result-value" markdown="1">

CALVER 在八种策略上都提高了点估计；其中七种策略相对 set medoid 的 95% 置信区间不跨 0。增益随策略而异，例如 Qwen 7B SFT 从 31.6% 提升到 43.8%，Mistral NeMo 12B 从 28.3% 提升到 47.4%，Qwen 14B 从 44.4% 提升到 68.5%；唯一统计证据较弱的是 Qwen 7B base，其增益为 4.4 个百分点、区间为 $[-0.8,9.7]$。

</div>

这说明收益并不局限于单一模型规模、微调方式或量化配置：当候选遵循可解析的结构化轨迹时，检查因果有效性通常比寻找池内最具代表性的答案更可靠。不过，不同策略提供的可用验证信号不同，且 Qwen 7B base 的区间跨 0，因此不能声称每个策略上都已得到确定优势。

<div class="result-source" markdown="1">

来源：“Many-satisfier queries across policies”节，Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Relative to this stronger voting baseline, seven of eight confidence intervals exclude zero.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 1,111 个所有选择器分数均齐全的冻结 CLEAR problem-seed 单元，CALVER 对比通用非 oracle 评分器

<div class="result-value" markdown="1">

CALVER 达到 42.1%，最接近的通用比较器为 30.5%。相对奖励模型、LLM judge、模型自置信度和精确多数投票，CALVER 分别领先 11.6、14.8、12.1 和 11.3 个百分点，四个配对置信区间均不跨 0；把 LLM judge 扩大到 Qwen2.5-72B 后仍只与多数投票基本持平。

</div>

固定候选池和输入后，差距更可能来自评分准则：CALVER 执行明确的因果谓词，而通用神经评分器可能偏好流畅、常见或看似可信的轨迹。该结果支持“符号有效性提供了通用评分器未捕捉的信号”，但不证明 CALVER 能改善候选生成本身，也不代表它适用于没有可用因果结构或不可形式化的任务。

<div class="result-source" markdown="1">

来源：“Does the advantage survive matched pools and larger K?”节，Figure 2 左图

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

CALVER reaches 42.1% (Figure 2); the closest generic comparator reaches 30.5%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen 7B SFT 的冻结 $K=32$ CLEAR 候选池，以前缀方式考察采样预算扩展

<div class="result-value" markdown="1">

CALVER 从 $K=1$ 时的 20.6% 上升到 $K=32$ 时的 57.9%；精确多数投票在 $K=32$ 时为 32.5%，且从 $K=16$ 到 $K=32$ 没有改善。两者差距由 $K=2$ 的 7.7 个百分点扩大到 $K=32$ 的 25.4 个百分点，后者 95% 置信区间为 $[18.3,32.3]$。verifier-GRPO 与未适配 base 策略也呈相同定性趋势。

</div>

更多采样提高了“池中至少存在一个有效候选”的机会，但票数可能继续分散到多个不同的有效答案；CALVER 能直接识别这些答案的共同有效性，因此更能利用额外预算。结果建立在冻结池的前缀比较上，控制了不同 $K$ 重新采样造成的混杂，但只覆盖论文测试的模型、任务与最大预算，不能推出无限增大 $K$ 时仍会持续改善。

<div class="result-source" markdown="1">

来源：“Does the advantage survive matched pools and larger K?”节，Figure 2 中图与右图

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The gap therefore grows from 7.7 percentage points at K=2 to 25.4 points at K=32 [18.3, 32.3].

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- supplied-graph CLEAR 中，验证器与评分标准按设计使用同一谓词，因此该设置强力检验选择机制，却可能高估现实任务中的表现；graph-from-text、DoVerifier、K&K 和精确 ATE 实验提供了验证器与评价器分离的补充证据，但节选未给出所有补充实验的完整逐项结果。
- CALVER 依赖可获得或可从文本构造的因果结构，并要求任务性质能够编写成正确的可执行谓词。若图结构严重缺失、文本歧义无法保留查询所需关系，或目标依赖不可形式化的常识，验证器可能没有可靠信号；此外，提示词、种子、模型修订与完整运行清单尚待作者公开代码数据包，当前结论仍需源文件和复现实验核验。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 精确多数投票（exact plurality）：选择候选池中出现频率最高的答案，是论文所针对的 self-consistency 标准做法；它能直接检验多个有效答案分散票数时是否会让重复出现的无效答案获胜。
- 集合 Jaccard medoid：选择与池内其他候选集合平均重叠最大的候选，比逐字符串计票更能容忍集合答案的表述差异，因此是 CLEAR 多答案场景中更强、更公平的投票基线。
- Skywork Reward V2 8B：对每条候选轨迹给出标量分数的通用奖励模型。它用于比较领域无关的学习式质量评分与执行 Pearl 因果准则的专用符号验证。
- 参考答案不可见的 LLM judge：接收与 CALVER 相同的图、问题和轨迹；论文还测试 Qwen2.5-72B 裁判。该基线检验性能差距是否仅来自 CALVER 拥有更多输入，或是否可通过扩大通用裁判模型弥补。

**实验想回答的问题**

- 在完全相同、预先冻结的候选池上，不使用参考答案的因果符号验证器 CALVER，能否比精确多数投票、集合中位候选、奖励模型、LLM 裁判和模型自置信度更可靠地选出满足图谓词的答案？
- CALVER 的优势是否会随采样预算 $K$ 增大，并能否迁移到外部贝叶斯网络、由文本重建因果图的场景，以及使用真值表验证的形式逻辑任务？

**实验实现**

默认以温度 0.8 采样 $K=8$ 条轨迹；除特别说明外，置信区间采用按源问题聚类的配对 bootstrap。主要比较在冻结的相同候选池上进行，避免不同选择器因候选质量不同而不可比；标量评分器在最高分并列时选择最早候选，投票与集合中位候选使用预先声明的答案级平局规则。实验覆盖 Qwen2.5 7B、14B、32B，7B/32B 的 4-bit NF4 版本及 Mistral NeMo 12B；另含遵循六槽轨迹格式的 7B SFT 和 verifier-GRPO 策略。外部图与逻辑谜题相对训练生成器均为零样本。作者称精确模型与适配器版本、NF4 配置、提示词、随机种子和运行清单将随代码数据包发布，因此当前节选尚不足以完全独立复现。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除语义因果有效性，仅保留解析、变量绑定和格式检查的 structure-only selector | 在 1,111 个匹配 CLEAR 单元上，structure-only 选择器准确率为 23.5%，CALVER 高出 18.6 个百分点，95% 置信区间为 $[15.6,21.7]$。 | 该消融隔离了“能否解析结构化轨迹”与“是否真正执行因果谓词”。准确率大幅下降说明主要信号来自 $d$-分离、后门准则和干预等语义检查，而不是格式规范、字段齐全或绑定成功本身。由于完整 Table 4 未包含在节选中，无法进一步核对各类图破坏消融的具体数值。 | “Does the advantage survive matched pools and larger K?”节；相关机制汇总见 Table 4<br><span class="experiment-evidence">The 18.6-point difference [15.6, 21.7] attributes the gain to the executable causal predicate: checking format alone confers no advantage.</span> |
| 文本给图时，对比“先抽取一个共识图再精确求解”与“逐候选验证”，限于每个表达层级共同可执行的 153 个单元 | L1 与 L2 中，extract-then-solve 分别达到 92.8% 和 96.7%，高于 candidate-wise verification 的 83.7% 和 82.4%；L3 中两者接近，分别为 83.7% 和 85.6%。 | 这项对照界定了 CALVER 的适用条件，而非证明逐候选验证始终最优：文本接近边列表或机制描述、能够可靠转写时，抽取一次并调用精确求解器更好；自然叙事导致候选对图的理解分歧时，逐候选验证可避免把所有决策绑定到单次错误抽取。共同可执行子集本身经过可解析性筛选，不能代表全部文本输入上的绝对表现。 | “When should one extract a single graph instead?”节，Figure 3<br><span class="experiment-evidence">On the common 153-unit executable stratum, where recovery is necessarily higher because parseability is a precondition, extraction followed by exact solving reaches 92.8% and 96.7% at L1 and L2, compared with 83.7% and 82.4% for candidate-wise verification.</span> |

**定性案例**

- 在人工审计的 clean-core 子集中，CALVER 选出的 21 个图上有效答案中有 11 个（52.4%）不同于数据集列出的示例，但仍满足题目谓词。这个案例直接展示了精确匹配投票的盲点：多个不同对象都可能正确，投票会把它们拆成不同模式，而谓词验证会把它们统一视为有效。该审计支持论文关于基准答案不完备的解释，但样本仅有 21 个，不能据此估计整个数据集的标注问题比例。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The core contribution is a symbolic causal and logical verifier for selecting valid LLM reasoning traces during best-of-K inference.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`cbff0b74f4d0e496eb8daf273c43c538a2a047e980a98fdf55963782030f2c91`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
