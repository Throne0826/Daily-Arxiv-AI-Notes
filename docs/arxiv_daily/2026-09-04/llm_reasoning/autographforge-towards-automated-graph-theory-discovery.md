---
title: "[论文解读] AutoGraphForge: Towards Automated Graph Theory Discovery"
description: "[arXiv 2609.03478][LLM Reasoning] AutoGraphForge旨在把图论猜想的生成、反例搜索、形式化与机器证明连接成统一流水线，并通过反例反馈和新颖性检查减少错误、已知或过拟合的候选结论。"
arxiv_id: "2609.03478"
announcement_date: "2026-09-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:40:30.026189+00:00"
source_sha256: "0982992bdea3cea2d4ef5160e71423fb9b240bc771dd9d96a264c764673f228f"
tags:
  - "LLM Reasoning"
  - "自动猜想生成"
  - "自动定理证明"
  - "计算机辅助图论"
  - "反例搜索"
  - "高性能计算"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.03478</p>

# AutoGraphForge: Towards Automated Graph Theory Discovery

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Ján Pastorek</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Department of Applied Informatics, Comenius University in Bratislava, Bratislava, Slovakia</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03478v1) · [PDF 下载](https://arxiv.org/pdf/2609.03478v1) · **关键词** 自动猜想生成, 自动定理证明, 计算机辅助图论, 反例搜索, 高性能计算<br>
**代码**: [https://github.com/JanPastorek/AutoGraphForge](https://github.com/JanPastorek/AutoGraphForge)

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

AutoGraphForge旨在把图论猜想的生成、反例搜索、形式化与机器证明连接成统一流水线，并通过反例反馈和新颖性检查减少错误、已知或过拟合的候选结论。

**不用术语来说**：计算机可以从有限图样本中归纳看似成立的规律，但“在样本上没出错”既不代表规律普遍正确，也不代表它是新的或值得研究的；即便得到有意义的猜想，还需要把它准确写成形式语言并获得可由可信内核检查的证明。因此，真正困难的不是大量生成公式，而是让生成、淘汰、修正和验证形成连贯且可信的发现过程。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者构建了AutoGraphForge的首个版本，将多轮猜想生成、反例驱动的数据更新、已知关系过滤、Lean 4形式化和神经定理证明器接入同一计算流程；但作者明确说明，证明阶段目前仅完成实现与初步健全性检查，尚未对存活猜想开展受控评测。
- 作者为降低伪发现与重复发现的概率，引入由经典、民间及平凡关系组成的新颖性过滤器，并结合大规模、多来源图数据与主动反例搜索，使候选猜想不仅接受静态样本检验，还会受到针对性搜索的持续攻击。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于计算机辅助图论、自动猜想生成与自动定理证明的交叉领域。图论研究有限简单图的结构及其可计算性质；图不变量则把一个图映射为整数或其他数值，例如独立数、匹配数和边覆盖数。AutoGraphForge 的目标不是直接枚举所有定理，而是建立一个从图数据和不变量出发，依次生成候选关系、寻找反例、排除已知结果、形式化命题并尝试证明的自动化闭环；其中最终的正确性由 Lean 4 的内核检查，而不是由神经网络单独保证。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**有限简单图与图不变量**

有限简单图 $G$ 由顶点集合 $V(G)$ 和边集合 $E(G)$ 构成，且没有环或重边；顶点数称为阶，边数称为大小。图不变量是只由图的结构决定、在图同构下保持不变的量，例如独立数 $\alpha$、匹配数 $\nu$ 和顶点覆盖数 $\tau$。

</div>
<div class="concept-item" markdown="1">

**反例引导的猜想生成**

系统先根据已有图样本提出候选关系，再用图数据或搜索算法寻找违反该关系的图。找到的反例会加入后续样本，使下一轮生成器能够避开已知错误模式；因此它是逐轮收紧候选空间，而不是一次性从全部图中学习。

</div>
<div class="concept-item" markdown="1">

**形式化证明与内核验证**

形式化证明把数学命题翻译成 Lean 4 可检查的类型化语句和证明项。神经证明器可以提出证明，但最终必须由固定版本的 mathlib4 和 Lean 内核独立验证，从而将“模型认为正确”与“形式系统确认正确”区分开。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一组有限简单图及其计算得到的图不变量表 $T$，以及包含经典关系、图族和搜索程序的知识与测试资源；管线计算的总不变量数为 $59$。系统在每轮中使用 Graffiti3 基于规模较小且会被反例扩充的表 $T$ 生成候选关系，先通过包含 $559$ 条经典或民间关系的创新性过滤器判断候选是否已由已知结果推出，再在约 $348{,}000$ 个图组成的反驳数据集和主动反例搜索上测试；未被淘汰的关系输出为待证明猜想，并被确定性地转换为 Lean 4 命题骨架，随后交由神经证明器提出候选证明、由 Lean 内核验证。论文的假设是：图不变量能够可靠计算，数据集与主动搜索能够发现相当一部分反例，但未被发现并不等于数学上已经证明；因此系统产出的主要中间结果是“尚未被现有测试反驳且未被过滤器判定为已知”的候选猜想，而不是自动保证为真的定理。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$G$**

研究对象，即一个有限简单图。

</div>
<div class="notation-item" markdown="1">

**$V(G),E(G)$**

分别表示图 $G$ 的顶点集合和边集合。

</div>
<div class="notation-item" markdown="1">

**$n=|V(G)|,m=|E(G)|$**

$n$ 是图的阶，即顶点数；$m$ 是图的大小，即边数。

</div>
<div class="notation-item" markdown="1">

**$T$**

快照表，记录少量图及其已计算的不变量，并在发现反例后扩充。

</div>

</div>

**直接相关的工作**

- **Graffiti3**: 本文将 Graffiti3 作为候选图论关系的生成器；它在系统中负责从演化的快照表 $T$ 提出猜想，而不是负责最终证明。
- **GraphCalc（Davila，2025）**: 论文依赖 GraphCalc 文档给出全部 $59$ 个图不变量的精确定义；正文只详细定义与主要论证直接相关的不变量，因此 GraphCalc 构成其不变量计算与术语说明的基础。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

自动图论发现面临一条完整的可信性链条：系统必须提出可能有价值的图不变量关系，发现有限数据未覆盖的反例，排除文献中已知或可由已有关系直接推出的结论，再把剩余猜想转成可机械检查的形式陈述并尝试证明。任何环节孤立运行都会留下明显风险，例如错误的不变量计算可能制造假反例，有限样本可能支持错误规律，而未经内核验证的自然语言证明又可能包含隐蔽缺口。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **自动猜想生成方法**：既有系统主要采用两类互补思路：一类用代数表达式树组合图不变量及算术运算并搜索候选关系；另一类使用线性或混合整数规划，或把每个图映射为不变量空间中的点并读取凸包面，从有限表格中寻找紧的线性不等式。它们擅长提出和排序候选猜想，但候选通常首先只是对当前数据的拟合。
- **反例搜索与形式证明工具**：反例发现可依靠穷举、分支定界、随机搜索、启发式搜索或深度强化学习，主动寻找违反候选关系的图；在验证端，Lean 4等证明助理把定义、陈述和证明表示为形式对象，由小型可信内核逐步核验，神经证明器则负责提出候选证明而不负责最终裁决。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 有限图表上的成立容易造成过拟合：数据可能缺少破坏不等式的特殊结构，生成器还可能堆叠过多项和常数形成“怪物猜想”。其后果是候选看似紧致或复杂，实际上可能为假，或者只是在记忆当前样本。
- 已有工具大多分别处理猜想、反驳、形式化或证明，且生成系统还会反复产出已知、平凡或可由既有关系推出的结果。缺少跨阶段反馈意味着反例不能系统地改进下一轮候选，存活猜想也未必能顺畅进入独立、内核级的证明检查。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

据作者所知，图论领域尚无一个把自动猜想、主动反例搜索、形式化和自动证明整合为闭环发现流程的现成系统。尤其缺少这样的机制：只把针对当前猜想发现的反例加入后续生成数据，以持续修正搜索空间；同时用可推导性而非简单字符串匹配判断候选是否已被知识库蕴含；最后将真正存活的候选确定性地导出到证明助理。

</div>
<div markdown="1"><span>核心问题</span>

能否构建并实际运行一条可扩展的图论自动发现流水线，使候选猜想在多轮生成过程中同时接受已知知识、新颖性推理、大规模异质图数据和主动反例搜索的筛选，并进一步被可靠地翻译为Lean 4目标、交由自动证明器尝试证明和内核核验？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点类似“出题者与找错者对抗学习”：生成器先从较小的图表中提出简洁关系，反例搜索器专门寻找其薄弱处，找到的反例再进入下一轮数据，使后续候选必须解释此前失败的结构。与此同时，新颖性过滤器先消除可由已有关系推得的候选，避免把计算资源浪费在重复结论上；最后以Lean内核作为独立裁判，把“模型认为证明成功”与“形式系统确认正确”区分开来。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

AutoGraphForge 是一个“猜想生成—新颖性筛选—反例证伪—形式化与证明”的闭环系统。输入是当前快照表 $T$、图不变量、图类谓词和已知定理库；系统在小规模且不断被反例更新的 $T$ 上生成候选猜想，再用大规模图数据集、参数化图族、随机图和专门搜索算法寻找反例。只有通过新颖性筛选并在反例搜索中存活的候选，才会被确定性地翻译为 Lean 4 命题，并交给神经证明器生成证明，最后由 Lean 内核独立核验。直观地说，$T$ 像一个不断加入“失败样例”的训练草稿本，而反例搜索器像主动找漏洞的审稿人；证明器只负责提出证明，真正决定证明是否有效的是内核。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构建知识库与计算图不变量

系统用 GraphCalc 为每个图计算精确不变量值，超时值留空，并用 networkx 交叉检查；这些图及其不变量组成快照表 $T$，其数值列把图表示为 $\\mathbb{R}^{k}$ 中的点，其中 $k$ 是不变量数量。

<div class="method-step__io" markdown="1">

**输入**：输入为初始的 TxGraffiti expressive graphs、后续发现的反例、图类标签以及需要计算的图不变量。<br>
**输出**：输出是供猜想生成使用的小型、会随反例增长的快照表 $T$，以及供后续证伪使用的更大静态图数据资源。

</div>

**直观理解**：系统不会一开始就在全部图上生成猜想，而是先保留一个较小的代表性样本。每当某个猜想被找到反例，反例就加入样本，使下一轮生成自动避开已经暴露的错误模式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 生成、排序并筛选候选猜想

Graffiti3 在当前 $T$ 上生成线性半空间、不等式的比值或乘积变体，以及 Sophie 产生的充分或必要条件。随后使用 Dalmatian、Morgan 和 Touch 启发式去除被更强界支配、仅在较小图类中成立但在更大类中也成立、或在数据中不够紧的候选；对线性候选，线性规划检验其是否可由已知关系的凸组合和合法不变量下界推出。

<div class="method-step__io" markdown="1">

**输入**：输入为快照表 $T$、其中的数值不变量、布尔图类谓词，以及包含经典定理和民间结果的已知关系库。<br>
**输出**：输出是按优先级排列且未被已知理论蕴含的候选猜想；被判定为已知结果的候选会被排除，但保留作新颖性筛选的校验样例。

</div>

**直观理解**：这一阶段同时回答两个问题：候选是否足够有信息量，以及它是否只是旧定理的重新拼接。Touch 偏好“贴着数据边界”的猜想，而线性规划则像一个可检查的代数审计器，避免把已知结论误报为新发现。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 多层反例搜索与反例驱动迭代

系统先在约 $348{,}207$ 个图上批量检查候选，再测试 barbells、lollipops、spiders、$k$-trees、line graphs 等参数化族和随机图模型；若仍未找到反例，则调用 SMT、线性交叉熵、变量邻域搜索、蒙特卡洛树搜索、模拟退火或深度强化学习后端，最大化候选的违反幅度。

<div class="method-step__io" markdown="1">

**输入**：输入为通过新颖性筛选的候选猜想，以及静态数据集、参数化图族、随机图模型和可主动构造图的搜索后端。<br>
**输出**：若发现图 $G$ 使候选失败，则将 $G$ 及其不变量加入 $T$，进入下一轮候选生成；若候选在所有启用的反例搜索中均未被推翻，则送入形式化与证明阶段。

</div>

**直观理解**：“在已有数据上为真”并不等于对所有有限图都为真，因此系统先用现成图库广泛筛查，再让搜索器主动制造可能违反猜想的图。一个反例不仅淘汰当前猜想，还会改变下一轮系统看到的样本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 确定性形式化、神经证明与内核核验

lean_export.py 将每个不变量映射为 Lean 名称，将图类条件映射为前置假设，并把关系两侧转换到 $\mathbb{R}$；随后 DeepSeek-Prover-V2-671B 与 OProver-32B 以单轮或带编译器反馈的多轮模式生成证明。每个证明都由固定版本的 mathlib4、GraphInvariants 前置定义和 Lean 内核独立检查，并保存为可再次验证的 `.lean` 文件。

<div class="method-step__io" markdown="1">

**输入**：输入为存活的 TxGraffiti 猜想、其图不变量和图类谓词，以及 Lean 4、mathlib4 和 GraphInvariants 前置定义。<br>
**输出**：输出包括 Lean 中类型正确但尚未证明的 `sorry` 命题骨架，以及经内核通过的完整证明文件；未被形式化支持的不变量或图类条件会被跳过。

</div>

**直观理解**：形式化翻译像把自然语言猜想改写成机器能精确阅读的合同，神经模型只是尝试填写证明内容。即使模型“自信地”给出错误证明，Lean 内核也不会接受，因此可信性不依赖模型自身的判断。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 线性规划新颖性过滤的非负性证书

$$
R(g)-\sum_{j}w_{j}B_{j}(g)=\sum_{i}s_{i}(g_{i}-L_{i})+\sum_{k}\mu_{k}E_{k}(g)+t
$$

**符号说明**

- $R(g)$：候选猜想右侧的线性函数，候选形式为 $f\leq R(g)$。
- $f$：候选猜想左侧的目标图不变量。
- $g=(g_1,\ldots,g_n)$：候选右侧使用的 $n$ 个图不变量组成的向量。
- $B_j(g)$：已知定理库中关于目标不变量 $f$ 的第 $j$ 个线性上界。
- $w_j$：第 $j$ 个已知上界的凸组合权重，要求 $w_j\geq0$ 且 $\sum_jw_j=1$。
- $s_i$：对应安全下界 $g_i\geq L_i$ 的非负乘子，要求 $s_i\geq0$。
- $L_i$：不变量 $g_i$ 的已知合法下界。
- $\mu_k$：图类恒等式 $E_k(g)=0$ 的自由乘子，可以取任意实数。
- $E_k(g)$：在候选所量化的整个图类上恒等为零的线性结构关系。
- $t$：非负常数松弛项，用于吸收剩余常数，要求 $t\geq0$。

<div class="equation-explanation" markdown="1">

**直观理解**：如果线性规划能找到这些权重、乘子和松弛量，就说明候选与已知定理之差处处非负，因此候选并没有超出已知理论。关键的安全条件是每个下界和恒等式必须在候选的整个假设类上成立，而不能只在有限数据表中碰巧成立。<br>
**原文位置**：第 3.3 节“ The non-negativity certificate ”

</div>

</div>

<div class="equation-block" markdown="1">

#### 候选猜想的反例违反幅度

$$
\mathrm{margin}(G)=f(G)-R(g)(G)
$$

**符号说明**

- $\mathrm{margin}(G)$：图 $G$ 对不等式候选的违反幅度。
- $G$：待检验或由搜索器构造的图。
- $f(G)$：目标不变量 $f$ 在图 $G$ 上的取值。
- $R(g)(G)$：由其他不变量计算出的候选右侧在图 $G$ 上的值。

<div class="equation-explanation" markdown="1">

**直观理解**：当 $\mathrm{margin}(G)>0$ 时，图 $G$ 就满足 $f(G)>R(g)(G)$，因而是候选不等式的反例；幅度越大，说明反例越有说服力。对 Sophie 的蕴含候选，系统同样把“满足前提但违反结论”定义为正的违反信号。<br>
**原文位置**：第 3.4.2 节“ Counterexample-search algorithms ”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：系统的核心生成—证伪循环不是端到端梯度训练，而是以反例驱动的迭代优化为主：Graffiti3 根据快照表 $T$ 选择满足当前样本的候选，反例搜索器最大化 $\mathrm{margin}(G)$，找到反例后扩大 $T$ 并重新生成。线性交叉熵后端更新图的边包含概率，使其趋向高违反幅度样本；深度强化学习后端则训练边选择策略以提高基于违反幅度的奖励。形式化阶段使用的两个神经证明器承担证明搜索，不改变 Lean 命题的语义；其输出必须通过内核检查，因此论文没有把“模型生成证明”本身当作可信目标。对于证明器的完整训练数据、损失函数或在本项目上的再训练过程，原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Graffiti3 猜想生成与启发式选择**

线性猜想采用形如 $\sum_i a_i f_i(G)\leq c$ 的半空间语法，其中 $f_i$ 是图不变量，$a_i,c\in\mathbb{R}$。系统关注当前快照表点云凸包的有效边界；Dalmatian 删除被更强猜想支配的界，Morgan 删除在更宽图类中同样成立的受限界，Touch 按候选在数据图上达到紧性的次数排序。Sophie 则从布尔谓词集合 $\mathcal{P}$ 中搜索合取条件 $H=\bigwedge_{i\in Q}P_i$，生成 $H\Rightarrow I$ 形式的充分条件，也处理必要条件及其逆否表达。

> 直观理解：数值模式可以理解为寻找包住数据点的最紧直线或平面，布尔模式则是在问“哪些图类条件足以保证某性质”。这些规则减少大量重复、过弱或只因样本有限而显得成立的候选。

**2. 线性规划新颖性过滤器**

对于候选 $f\leq R(g)$，系统从已知的 $f\leq B_j(g)$ 中选择非负权重 $w_j$，要求权重和为 $1$，并检查候选与已知界的差能否表示为合法非负项、图类恒等式和常数松弛的和。只有在每个已知界和恒等式都对候选的整个假设类有效时，才允许将其纳入推导，从而避免把只在数据集上成立的关系当作定理。

> 直观理解：过滤器不是简单地比较数值，而是要求给出一张代数“证明收据”：候选界必须能由旧定理按合法方式混合得到。找不到这张收据时，系统暂时把候选视为可能新颖，而不是直接断言它一定是定理。

**3. 统一违反幅度的反例搜索后端**

所有搜索器共享违反幅度接口。对于不等式 $f(G)\leq R(g)(G)$，违反幅度为 $f(G)-R(g)(G)$；对于 $H\Rightarrow I$，仅当图满足 $H$ 且不满足 $I$ 时取正值。SMT 将边表示为布尔变量并编码不变量约束；交叉熵方法更新边生成概率；变量邻域搜索、蒙特卡洛树搜索和模拟退火探索边增删；深度强化学习训练边选择策略以提高该幅度。

> 直观理解：不同算法虽然找图的方式不同，但都在优化同一个目标：找到一个让猜想“错得最明显”的图。统一接口使系统可以替换或组合搜索器，而不必为每种算法重写整个证伪流程。

**训练与推理**

推理流程从当前 $T$ 开始：Graffiti3 生成候选，启发式和线性规划过滤器删除低价值或可由已知理论推出的关系；剩余候选依次经过静态图集、特殊图族、随机模型和主动反例搜索。发现反例时，系统把反例加入 $T$ 并进入下一轮；没有发现反例的候选在达到规定存活轮数后进入 Lean 导出。Lean 导出是确定性的：不变量、图类谓词和关系被映射为固定名称、假设和实数不等式，先产生带 `sorry` 的类型正确目标，再由 DeepSeek-Prover-V2-671B 和 OProver-32B 以单次或编译器反馈的多轮模式尝试闭合目标。最终由固定版本的 mathlib4、GraphInvariants 前置定义和独立 Lean 内核复核；通过的证明保存为自包含 `.lean` 文件。现阶段完整证明阶段尚未对全部存活猜想运行，论文仅报告了初步端到端检查。

**复现信息**

为保证结果可复核，图不变量由 GraphCalc 精确计算，超时值保留为空；networkx 仅作独立交叉检查，GraphCalc 与 HoG 共享不变量的抽查结果没有发现不匹配。静态反例资源由 HoG、至多九个顶点的连通图穷举表和若干特殊图族合并而成，包含数值不变量与布尔图类谓词；这些大数据只用于证伪，不用于直接生成猜想。反例搜索可从随机图开始，也可从已有图初始化。形式化支持范围受 GraphInvariants 前置表限制，未被形式化的不变量或图类会跳过；证明器运行环境包括 vLLM 和多 GPU 服务，但完整证明吞吐量、成功率及端到端运行时间原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 猜想生成快照表 $T$：初始核心来自 337 个 TxGraffiti expressive graphs；在早期开发运行中，$T$ 仅通过加入系统自身猜想的反例增长，到正式实验开始前达到 2,860 个图。它只用于 Graffiti3 生成候选猜想，而不是最终验证集；这种设计测试“小型、经反例强化的核心表”是否足以驱动迭代生成。
- 静态反驳数据集：共 348,207 个图，约含 348,000 个样本，合并完整 House of Graphs 不变量导出、所有至多 9 个顶点的连通图穷举，以及强正则图、极小 Ramsey 图、Cayley 图、cage、barbell、lollipop、spider 等结构化或极值族。每个图计算 59 个属性，其中 45 个为可作为不等式左端目标的数值不变量，14 个为图类布尔谓词；另加入 $n\geq 3$ 与 $n\geq 4$ 两个派生条件。该集合专用于发现有限样本上的反例，不承担生成任务。
- 参数族、随机模型与主动搜索产生的图：参数族包括 barbell、lollipop、spider、$k$-tree、线图、Delaunay 图和满足 $\alpha=2$ 的补图等；随机部分包括随机正则图、Erdős–Rényi $G(n,p)$、随机树和随机二分图；主动搜索在 $n=10$ 到 $n=100$ 的多个阶数上运行。其作用是补充固定数据库偏向小图或已收录结构的问题，并针对每个候选最大化违反裕量，而非提供普遍正确性的证明。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**最终存活猜想数**

统计同时通过静态反驳数据集、559 条已知关系及其闭包构成的新颖性过滤器、以及全部启用的主动反例搜索后仍未被淘汰的候选数。数量较大表示流程有较高发现产出，但不等同于这些猜想均为真、重要或非平凡。 （在筛选强度和候选质量可比时越高越好；若缺少人工审查或正式证明，单纯增大该数也可能意味着残留冗余与平凡猜想更多。）

</div>
<div class="metric-item" markdown="1">

**固定点收敛与墙钟时间**

观察每个目标不变量分区是否停止产生新的可加入快照表的反例，以及达到固定点所需轮数和时间。它衡量反例反馈循环的终止行为与工程效率，而不是猜想真值。 （在得到相同质量输出时，达到固定点的时间和轮数越低越好；但过早收敛也可能来自搜索能力不足。）

</div>
<div class="metric-item" markdown="1">

**Lean 内核验证结果**

检查确定性导出的 Lean 陈述是否类型正确，以及神经证明器产生的证明是否被独立内核接受。内核通过是形式证明正确性的硬判据，但当前节选只报告了平凡不等式上的初步健全性检查。 （通过率越高越好，因为只有内核接受的证明才被系统视为有效；不过必须结合题目难度和测试集规模解读。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 完整多轮猜想生成、559 条关系的新颖性过滤、约 348,000 图的静态反驳，以及全部启用的主动反例搜索

<div class="result-value" markdown="1">

流程最终保留 6,522 个候选猜想；这些候选没有在现有反驳资源中发现反例，也未被新颖性过滤器标记为可由已知关系推出。其中包含关于二分图和正则图的 annihilation number 与 edge-cover number 的非平凡关系，作者称已给出手工证明。

</div>

作者的结果表明该流水线能够产生规模可观、且比“仅在生成表上成立”更经得起反驳的候选集合。这里的“存活”只是截至本次有限数据库和有限预算搜索均未被推翻，并不构成全称命题的证明；同样，新颖性过滤只覆盖所编码的 559 条关系及其闭包，不能保证文献意义上的绝对新颖。手工证明的少数关系提供了更强的有效性案例，但不能自动推广到全部 6,522 个候选。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Run for several rounds on an HPC cluster, the loop yields 6,522 surviving conjectures that no graph in the refutation dataset, which were not flagged as known by the novelty filter, and no active-search run eliminated—among them nontrivial relations between the annihilation number and the edge-cover number for bipartite graphs and regular graphs which we were able to prove by hand.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 5 个目标不变量分区的 HPC 多轮生成—反驳实验，每个分区最多运行 29 小时

<div class="result-value" markdown="1">

5 个分区均在时间上限前达到固定点；每轮约需 20–40 分钟，运行 5 轮的分区约需 2 小时，运行 9 轮的分区约需 4.5 小时。生成—反驳循环约消耗 3,200 核时，即约 0.37 CPU 年。

</div>

这说明在作者当前的数据、搜索预算和目标划分下，反例反馈循环可以工程上收敛，而不是持续无限扩张快照表。固定点仅表示当前生成器与反驳器之间不再产生新反馈，并不意味着搜索空间已穷尽；不同生成规则、更强反例后端或更大的图阶仍可能打破该固定点。

<div class="result-source" markdown="1">

来源：实验计算成本段，目标不变量分区说明之前

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The generate–refute experiment was a SLURM array of five independent partitions, each on a full 256-core node, run to a fixed point or a 29 h wall-clock cap; no partition hit the cap—all five terminated at a fixed point.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 存活猜想的确定性 Lean 4 导出，以及 DeepSeek-Prover-V2-671B、OProver-32B 后接独立内核检查的形式化与证明阶段

<div class="result-value" markdown="1">

端到端形式化阶段已经实现并通过初步健全性检查：确定性导出可产生类型正确的 Lean 陈述，两种证明器生成的平凡不等式证明可被内核独立验证；完整流水线当时仍在集群运行，因此没有报告对 6,522 个候选的总体证明率。

</div>

该结果验证的是接口和可信链路能够工作：自然语言之外的结构化猜想可以落到 Lean 类型系统中，模型输出也不会绕过内核。它尚不能证明系统已自动解决非平凡的新猜想，因为已报告的检查对象只是平凡不等式，且完整批量实验没有结束。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

This stage is implemented end-to-end and passes initial sanity checks—the deterministic export yields type-correct Lean statements and the provers independently kernel-verify trivial inequalities—with the full pipeline currently running on the cluster.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 论文报告的是进行中的系统。全部 6,522 个存活猜想并未被形式证明，完整神经证明实验仍在集群运行；当前形式化证据只覆盖类型正确导出和平凡不等式的内核验证，不能据此估计非平凡猜想的自动证明成功率。
- 节选没有给出单遍基线与多轮反例引导流程的定量对照，也没有分别统计静态图库、新颖性过滤器和各主动搜索后端淘汰的候选数，因此无法通过消融判断每个组件的独立贡献。有限图库和有时限的搜索还意味着“未找到反例”不能被解释为“猜想为真”。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 单遍生成与筛选基线：论文说明计算总成本包含第 4.1 节的 single-pass baseline run，用于与多轮反例引导流程比较；但所给节选没有提供该基线的具体配置、候选数量或对比结果，因此无法据此量化迭代反馈的净增益。
- 固定静态数据反驳：候选先在约 348,000 个预计算图上测试，这是主动搜索之前的基础验证方式。它是有意义的参照，因为可区分“数据库中已有反例”和“必须通过候选定向搜索才能找到的反例”，但节选未分项报告两者分别淘汰了多少猜想。
- 两种神经证明器 DeepSeek-Prover-V2-671B 与 OProver-32B：它们是并列的证明后端而非严格意义上的无模型基线。二者生成的候选证明均须经过同一套固定版本 mathlib4、自定义不变量前言和 Lean 内核检查，因此可在统一可信判据下比较；原文节选尚未给出各自的证明成功率。

**实验想回答的问题**

- 反例引导的多轮“生成—新颖性筛选—静态反驳—主动反例搜索”流程，能否在不让猜想生成器直接访问完整图库的条件下，稳定收敛并产出一批尚未被已知关系推出、且未被现有反驳手段击败的图论猜想？
- 从生成阶段存活的猜想能否被确定性地翻译为类型正确的 Lean 4 陈述，并使神经证明器提交的证明始终接受独立 Lean 内核检查，从而形成端到端的形式化验证链路？

**实验实现**

实验将 45 个数值目标不变量按 GraphCalc 标识符字母序切成 5 个连续分区，每区 9 个目标；这一划分用于确定性负载均衡，不代表语义分组。5 个 SLURM 数组任务分别占用一台 256 核 AMD EPYC 9745 节点，运行至固定点或 29 小时上限。候选首先由 Graffiti3 在小型快照表 $T$ 上生成，再经由 559 条经典或民间关系构成的新颖性过滤器判断是否可由已知关系线性推出，随后经过静态与随机图数据反驳，并由 Z3、交叉熵、变邻域搜索、蒙特卡洛树搜索、模拟退火和强化学习图搜索等后端最大化违反裕量。所有主动搜索后端采用统一默认参数、没有针对单个猜想调参，并受每候选墙钟预算约束。形式化阶段将存活猜想确定性导出为 Lean 4 陈述骨架，DeepSeek-Prover-V2-671B 与 OProver-32B 仅负责提出证明，最终由固定版本 mathlib4 环境中的 Lean 内核独立判定。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 案例研究是 annihilation number 与 edge-cover number 在二分图和正则图上的关系：它们通过自动生成、新颖性过滤、静态与主动反驳后存活，并由作者手工证明。该案例说明流水线至少能把注意力引向可证明的非平凡关系；但所给节选没有列出具体不等式、证明内容或与既有定理的细粒度比较，因而仍需核对正文相应定理。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops an automated mathematical discovery pipeline for conjecturing, refuting, formalizing, and kernel-verifying graph-theory proofs with neural theorem provers.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`0982992bdea3cea2d4ef5160e71423fb9b240bc771dd9d96a264c764673f228f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
