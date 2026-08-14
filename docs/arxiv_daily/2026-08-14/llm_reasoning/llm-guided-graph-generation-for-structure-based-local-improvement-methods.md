---
title: "[论文解读] LLM-Guided Graph Generation for Structure-Based Local Improvement Methods"
description: "[arXiv 2608.13333][LLM Reasoning] 本文研究如何借助大语言模型自动把不同 MiniZinc 约束优化问题转换为统一的加权图，使结构化局部改进方法能够跨问题选择搜索邻域和算法配置，减少对领域专家手工设计的依赖。"
arxiv_id: "2608.13333"
announcement_date: "2026-08-14"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T03:04:30.385968+00:00"
source_sha256: "b0cb8b199facc536cf383990d61ad811408c395d6b80445fbc373748e59ec136"
tags:
  - "LLM Reasoning"
  - "大邻域搜索"
  - "结构化局部改进"
  - "MiniZinc"
  - "约束优化"
  - "加权变量关系图"
  - "大语言模型"
  - "算法选择"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.13333</p>

# LLM-Guided Graph Generation for Structure-Based Local Improvement Methods

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Hai Xia, Vaidyanathan Peruvemba Ramaswamy, Stefan Szeider</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13333v1) · [PDF 下载](https://arxiv.org/pdf/2608.13333v1) · **关键词** 大邻域搜索, 结构化局部改进, MiniZinc, 约束优化, 加权变量关系图, 大语言模型, 算法选择<br>


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

本文研究如何借助大语言模型自动把不同 MiniZinc 约束优化问题转换为统一的加权图，使结构化局部改进方法能够跨问题选择搜索邻域和算法配置，减少对领域专家手工设计的依赖。

**不用术语来说**：大型组合优化问题通常难以一次求到高质量解，因此可以反复挑选一部分变量，让精确求解器只重新优化这一小部分；但挑哪些变量直接决定搜索效率。随机挑选虽然简单，却可能把关系很弱的变量放在一起，浪费求解时间；依据问题结构挑选通常更有效，但不同问题表达变量关系的方式不同，过去需要专家逐类分析约束、设计邻域和特征，难以形成可复用的自动流程。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出由大语言模型根据 MiniZinc 模型和语义指南生成并验证图生成器，将同一问题类型的任意实例转换为统一加权图；图节点对应决策变量，边及其权重表示变量之间的约束关系与耦合强度。
- 利用统一图表示构建跨问题的结构化局部改进流程：一方面通过通用图搜索策略选择紧密关联的变量邻域，另一方面从图中提取通用特征，为不同实例自动选择合适的搜索配置。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究约束组合优化中的大邻域搜索（Large Neighborhood Search, LNS）。给定一个由决策变量、变量取值域、约束和优化目标组成的 MiniZinc 模型，LNS 从当前完整解出发，每轮固定大部分变量，只释放一个变量子集并交给精确求解器重新优化，再将更优的局部结果合并回全局解；因此，所选变量是否形成有意义且耦合紧密的邻域，会直接影响有限求解时间的利用效率。结构化局部改进方法（Structure-Based Local Improvement Methods, SLIM）进一步利用变量之间的结构关系选择邻域，但以往通常需要专家针对树宽、图着色或最大可满足性等单一问题设计结构表示与选取规则。本文所处的技术背景是：MiniZinc 提供统一、求解器无关的约束建模入口，而图表示可将异构约束实例转换为节点与边，从而让通用邻域提取和跨问题配置选择在同一表示空间中运行。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大邻域搜索（LNS）**

一种迭代元启发式方法：每轮释放当前解中的一部分决策变量，由精确求解器在其余变量固定的条件下重新求解。与只改变少量变量的普通局部搜索相比，它能探索更大的局部区域，但效果高度依赖释放哪些变量。

</div>
<div class="concept-item" markdown="1">

**结构化局部改进方法（SLIM）**

SLIM 根据变量之间的结构联系构造局部子问题，而不是均匀随机选变量；本文采用基于广度优先搜索和加权随机采样的通用提取方式。直观上，它希望一次共同重优化彼此强相关的变量，避免把求解预算浪费在联系松散的变量组合上。

</div>
<div class="concept-item" markdown="1">

**变量关系加权图**

图中节点对应决策变量，并携带权重和取值域大小；边表示变量因约束而产生的关系，边权刻画耦合强度。该图抹去具体问题的领域名称，却保留求解所需的语义结构，使不同 MiniZinc 问题能够共享图算法和图特征。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一类 MiniZinc 约束优化问题的模型，以及该问题类型下的具体实例；MiniZinc 被假定为统一的、与底层求解器无关的建模格式。离线阶段，大语言模型依据作者给出的语义指南读取约束模型并生成一个经过验证的确定性 Python 图生成器；该生成器应能把同一问题类型的任意实例映射为统一格式的加权图 $G=(V,E)$，其中每个节点 $v\in V$ 对应一个决策变量，每条边 $e\in E$ 表示变量间的约束关系。在线求解阶段，SLIM 从该图中提取结构相关的变量子集作为 LNS 邻域，由精确求解器执行局部优化；同时，从统一图中抽取拓扑与统计特征，为来自不同问题类型的实例选择合适的 SLIM 配置。最终输出包括可复用的图生成器、每个实例的通用加权图、每轮待重新优化的变量邻域，以及跨问题配置选择结果；大语言模型在这里充当一次性的离线“编译器”，并不在每轮搜索中直接求解实例。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$G=(V,E)$**

由图生成器产生的统一加权图；$V$ 是节点集合，$E$ 是边集合。

</div>
<div class="notation-item" markdown="1">

**$v\in V$**

一个图节点，对应 MiniZinc 实例中的一个决策变量，并可携带变量权重与取值域大小。

</div>
<div class="notation-item" markdown="1">

**$e\in E$**

连接相关决策变量的边，表示它们之间存在约束关系，并可携带语义耦合强度。

</div>
<div class="notation-item" markdown="1">

**$N\subseteq V$**

一次 LNS 或 SLIM 迭代中被释放并交给精确求解器重新优化的变量邻域；该符号是为清晰描述问题设置而作的概括，原文节选未给出专门符号。

</div>

</div>

**直接相关的工作**

- **Shaw（1998）的结构感知大邻域搜索**: 该工作在车辆路径问题中表明，利用结构的破坏或变量释放策略优于随机选择，构成本文结构化邻域选择的直接背景；但其设计面向特定问题，而本文试图让统一图生成与邻域提取适用于任意 MiniZinc 问题。
- **Fichte et al.（2017）的 SLIM**: 该工作首先将 SLIM 用于树宽计算，后续研究又将同类思想分别扩展到分支宽度、树深度、贝叶斯网络学习、图着色、决策树优化和最大可满足性。本文继承“按结构选取局部变量”的框架，但将以往针对每个领域人工构造结构和策略的步骤，改为由大语言模型离线生成统一、确定且可审计的图生成器。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

结构化局部改进方法的效果高度依赖邻域选择：每轮只有被选中的变量会交给精确求解器重新优化，因此，若邻域不能覆盖彼此紧密关联且有改进潜力的变量，有限的求解预算就会消耗在低价值子问题上。实际需求是在面对多种 MiniZinc 约束优化问题时，快速得到可用的结构感知搜索策略，而不必为每个领域重新组织专家团队、手工实现算法并长期调参。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **随机大型邻域搜索**：每轮随机选取一部分决策变量，将其余变量固定，再由精确求解器优化所选局部子问题；该方法计算开销低，也不要求理解问题语义。
- **问题专用的结构化局部改进与配置选择**：领域专家分析特定问题中的变量关系和约束结构，据此设计能够形成紧耦合邻域的选择规则；进一步使用算法配置器搜索参数，或提取该领域专用的实例特征，在算法组合中选择配置。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 随机选择忽略实例特征和约束结构，可能反复生成变量联系松散的局部子问题，导致精确求解器的时间没有用于最有希望的联合改进。
- 现有结构化方法的邻域构造、变量选择规则和实例特征通常绑定具体问题领域，需要大量专家知识和数月工程工作；配置器还可能要求很高的计算预算，因而难以扩展到大量异构问题。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作尚未提供一种面向不同 MiniZinc 问题的统一机制，能够自动从约束模型中提取足以支持邻域构造的语义结构，同时产生可跨问题比较的实例特征。缺少这一中间表示，使结构化搜索策略和配置选择仍然依赖问题专用设计。

</div>
<div markdown="1"><span>核心问题</span>

能否让大语言模型依据 MiniZinc 模型合成可靠的图生成程序，把不同问题实例映射为统一的加权变量关系图，并使同一套通用局部搜索与配置选择机制在多个问题类型上有效工作？

</div>
<div markdown="1"><span>作者直觉</span>

MiniZinc 模型已经显式描述了决策变量、变量取值范围以及约束中的共同出现和作用关系，只是这些信息采用不同领域的建模方式表达。大语言模型可以解释模型中的语义并生成相应的转换程序，把领域化表达压缩成统一图结构；随后，图上的广度优先搜索或加权采样便可优先聚集联系紧密的变量，而拓扑与权重统计又可作为跨问题共享的配置选择依据。直观地说，大语言模型负责把不同问题“翻译”为同一种关系地图，后续算法只需在这张标准化地图上工作。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把大语言模型用作一次性的“语义编译器”，而不是直接让它求解约束优化问题。对每一种 MiniZinc 问题类型，LLM 读取模型文件与人工制定的语义权重指南，生成一个 Python 图生成器；随后，该程序可将该类型的任意实例转换为统一加权图。图中节点对应决策变量，记录目标相关重要性权重与变量域大小；边对应变量之间的约束关系，边权表示耦合强度。统一图同时服务于两个环节：SLIM 根据图结构选择每轮要重新优化的变量邻域，算法选择器则根据图特征为当前实例挑选合适的 SLIM 配置。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按问题类型合成图生成器

LLM 分析模型中的决策变量、目标函数和约束语义，生成可执行的 Python 程序 `generator.py`。该步骤每个问题类型只执行一次，生成器随后可复用于该类型的不同实例。

<div class="method-step__io" markdown="1">

**输入**：某一问题类型的 MiniZinc 模型文件 `.mzn`，以及规定节点权重、约束耦合权重和图连通性的语义指南。<br>
**输出**：理解该问题类型语义结构的图生成器 `generator.py`。

</div>

**直观理解**：LLM 不负责直接给出解，而是为每类问题编写一个“翻译器”，将领域特有的约束模型翻译成后续算法都能读取的图。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 实例解析与统一加权图构造

变量提取器解析决策变量的名称、数组索引和取值域，产生 `variables.json`；图生成器结合实例参数建立加权图，并按照语义指南设置节点与边的属性。节点权重位于 $[0,1]$，节点域大小属于 $\mathbb{N}$，边权也位于 $[0,1]$。

<div class="method-step__io" markdown="1">

**输入**：实例的 `.mzn` 与 `.dzn` 文件、变量提取器，以及对应问题类型的 `generator.py`。<br>
**输出**：变量描述文件 `variables.json` 和统一格式的加权图 `graph.json`。

</div>

**直观理解**：不同领域的调度、路径规划或资源分配实例都会被压缩成同一种语言：哪些变量重要、每个变量有多少种可能取值，以及哪些变量因约束而紧密关联。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提取图特征并选择 SLIM 配置

系统从图中计算统一的 $54$ 维特征，包括拓扑统计、节点与边权分布、变量域统计及相关性、变量元数据和数值型实例参数；选择模型据此预测 $30$ 个候选 SLIM 配置中适合当前实例的配置。配置描述邻域预算 $b$、单轮求解时限 $t$、BFS 或 LNS 提取策略及冻结方式等。

<div class="method-step__io" markdown="1">

**输入**：当前实例的统一加权图，以及训练阶段得到的算法选择模型。<br>
**输出**：当前实例采用的 SLIM 配置。

</div>

**直观理解**：图特征相当于实例的统一体检报告；选择器不需要知道它原本属于哪个领域，只根据报告判断应当采用多大的局部搜索范围、搜索多久以及如何挑选变量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造局部邻域与约束子问题

BFS 提取按节点权重随机选择起点，再沿高权边优先扩展，以获得结构连通的变量邻域；LNS 提取则按节点权重随机收集变量，不要求变量在图上相邻。提取在域大小感知的预算 $b$ 达到阈值时停止，邻域外变量通常固定为当前值，也可通过冻结模式 $f$ 反向指定要冻结的变量。

<div class="method-step__io" markdown="1">

**输入**：统一加权图、所选配置、当前解 $s^*$ 和提取方法 $\mathcal{E}$。<br>
**输出**：待重新优化的变量集合 $N$，以及由原 MiniZinc 模型、冻结约束和目标界共同构成的局部子问题。

</div>

**直观理解**：每轮只松开一小部分变量，其余变量暂时保持不动；BFS 倾向于一起修改相互影响较强的一组变量，而 LNS 用作不强调局部连通性的随机对照策略。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 重复约束的有界边权聚合

$$
W=1-\prod_i(1-w_i)
$$

**符号说明**

- $W$：同一对决策变量在汇总所有相关约束后得到的最终边权。
- $w_i$：第 $i$ 个约束为该变量对贡献的耦合权重，取值位于 $[0,1]$。
- $i$：连接同一变量对的约束索引。

<div class="equation-explanation" markdown="1">

**直观理解**：公式先把每个约束“未产生耦合”的比例 $1-w_i$ 相乘，再用 $1$ 减去该乘积。更多或更强的共同约束会提高最终边权，但结果始终不超过 $1$，从而让不同问题生成的图保持统一尺度。<br>
**原文位置**：第 3.2.2 节 Generation Guidelines，第 4 条 Bounded weights

</div>

</div>

<div class="equation-block" markdown="1">

#### 局部子问题的非劣化目标界

$$
\operatorname{obj}(s')\leq\operatorname{obj}(s^*)\quad\text{(minimization)};\qquad \operatorname{obj}(s')\geq\operatorname{obj}(s^*)\quad\text{(maximization)}
$$

**符号说明**

- $\operatorname{obj}(\cdot)$：原约束优化问题的目标函数。
- $s'$：当前一轮局部子问题产生的候选可行解。
- $s^*$：进入当前迭代时保存的全局当前解。

<div class="equation-explanation" markdown="1">

**直观理解**：最小化时只允许候选解的目标值不高于当前值，最大化时方向相反。等号被保留，因此算法可以接受质量相同但变量赋值不同的解，在不降低当前目标质量的前提下移动到新的搜索位置。<br>
**原文位置**：第 3.3.1 节 Extraction Methods，SLIM working loop 描述

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：图生成器本身不是通过论文数据端到端训练的模型，而是由通用 LLM 按语义指南一次性合成程序，因此不存在针对图生成器的梯度训练目标。算法选择阶段才进行监督学习：对实例 $i$ 提取图特征向量 $\mathbf{x}_i$，并构造多配置目标向量 $\mathbf{y}_i$；其中每一维表示相应 SLIM 配置取得的改进幅度与一次性求解基线改进幅度之差。代表性的多输出随机森林回归器学习从 $\mathbf{x}_i$ 到 $\mathbf{y}_i$ 的映射，使推理时可以选择预测相对改进最大的配置；其他四类选择器遵循相同的数据流程，但采用不同损失目标或预测对象。SLIM 的实际优化目标仍是原 MiniZinc 模型的目标函数，算法选择目标只是间接学习哪种搜索配置更可能改善该目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. LLM 引导的语义图生成**

节点表示决策变量，节点属性包括目标重要性权重 $w\in[0,1]$ 和域大小 $d\in\mathbb{N}$；边表示共同约束产生的耦合关系，边权 $w\in[0,1]$。指南要求目标相关成分通常赋予至少 $0.6$ 的较高权重；含 $n>10$ 个变量的大型全局约束采用 $\max(0.1,1/n)$ 的较弱耦合，含 $n\leq5$ 个变量的小约束保留至少 $0.8$ 的强耦合，并要求图中不存在孤立节点。多个约束重复连接同一对变量时，使用有界聚合公式合并边权，避免总权重超过 $1$。

> 直观理解：该模块将“变量是否直接影响目标”和“变量是否必须协同改变”编码成权重。削弱大型全局约束尤其重要，因为把一个大规模 `alldifferent` 约束展开成高权完全图会淹没更有区分力的局部关系，使几乎所有变量看起来同样相关。

**2. 通用结构化局部改进框架 SLIM**

SLIM 从通常由启发式方法或短时求解获得的次优初始解 $s_0$ 出发，每轮以 $\mathcal{E}\in\{\mathrm{BFS},\mathrm{LNS}\}$ 从图中提取邻域 $N$。预算采用域大小感知的度量，而不是只计算变量个数，因为取值域更大的变量通常带来更大的局部搜索空间；冻结模式 $f$ 决定提取集合是被优化还是被固定，并通过目标界阻止局部求解器返回更差的解。

> 直观理解：SLIM 的核心不是替换底层约束求解器，而是控制每轮让求解器重新考虑哪些变量。图权重提供重要性，图边提供结构关联，域大小则估计放开这些变量后子问题会有多难。

**3. 跨问题算法配置选择**

作者把每个实例表示为同一套 $54$ 维图特征，并以各配置相对一次性求解基线的改进差值作为学习目标；代表性选择器是多输出随机森林回归，同时还构造了 ensemble、binary、classification 和 two-stage 等选择方式。训练样本按问题类型加权，使每种问题对训练和测试评价的贡献相同；候选组合来自不同预算、单轮时限、提取策略与冻结方式，共形成 $30$ 个配置。

> 直观理解：不存在对所有实例都最好的局部搜索参数，因此选择器学习“什么样的图适合什么样的配置”。问题加权用于避免实例数量特别多的类型主导模型，例如原文指出 RCPSP 单独占数据集的 $38\%$。

**训练与推理**

训练阶段首先对各训练实例运行全部候选 SLIM 配置并记录相对一次性求解基线的改进，再从每个实例的统一图中提取 $54$ 维特征。由于各问题类型的实例数量严重不均衡，作者采用按问题加权的样本权重，使每种问题在训练及最终测试评价中贡献相同；模型经交叉验证后，在完整训练集上重新训练。配置与特征消融采用贪心反向消除：先删除那些移除后能改善交叉验证表现的配置，再在缩减后的配置集合上继续删除特征。

推理阶段不再调用 LLM：变量提取器与预先合成的 `generator.py` 将新实例转换为图，系统计算同一组图特征，并由训练好的选择器给出配置。SLIM 随后从 $s_0$ 开始，按所选提取方法、预算 $b$、冻结方式 $f$ 和时限 $t$ 循环建立并求解局部子问题；可行且不劣的候选解替换当前解，最终输出总时间预算内得到的最好当前解。

**复现信息**

论文在问题特定阶段使用 Claude Opus 4.5 读取 `.mzn` 模型和语义指南并生成 Python 图生成器；单个问题类型的合成通常在数分钟内完成，且生成器可用于该类型来自不同年份竞赛的实例。可复现时需要保留模型文件、提示中的完整语义指南、生成的 `generator.py`、变量解析规则及统一 `graph.json` 格式，因为图生成程序的差异会直接改变后续邻域与特征。

作者评估的配置空间包含预算 $b\in\{10,20,50,70,100,200\}$、单轮时限 $t\in\{20,30,45,60\}$ 秒及不同提取和冻结策略，组合后使用 $30$ 个配置；原文节选未给出所有组合的逐项清单，也未完整定义域大小感知预算的计算式与五种选择器的具体损失，这些内容被指向补充材料。公平复现还需固定初始解生成过程、总运行时限、最大迭代次数、底层局部求解器及随机种子；当前节选仅展示种子 $51$、$52$、$53$ 的部分选择结果，未完整报告上述运行设置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 实验数据来自2008—2025年MiniZinc竞赛，覆盖20种约束优化问题。筛选条件是：Gurobi能在10分钟内找到可行解，但在60分钟内不能证明最优；同时每种问题至少保留5个合格实例。这一筛选使评测集中于“可求得可行解、但在给定预算内仍有改进空间”的较难实例，而不是所有MiniZinc实例。
- 算法选择实验按问题类型进行分层，将实例以70:30划分为训练集和测试集。训练集用于学习从通用图特征到SLIM配置的映射，测试集用于评估该映射对未参与训练实例的泛化能力。原文未在所给章节中报告训练集、测试集及各问题类型的具体实例数量。
- 同一训练集与测试集划分分别在随机种子51、52、53下评测五种算法选择方法。多种子实验用于检查结果是否依赖某次随机运行，但由于原文表述为每个种子使用相同的训练／测试实例分布，它主要反映选择器训练或搜索过程的随机波动，而不是多次重新采样数据划分的波动。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**问题加权胜率（problem-weighted win rate）**

比较SLIM与基线的目标值，并先在每种问题类型内部计算胜出比例，再以问题类型为单位汇总，从而避免实例较多的问题类型主导总体结果。该指标回答方法在不同问题类型上是否广泛有效；原文未在所给章节中给出其精确计算公式。 （越高越好，因为它表示SLIM得到严格优于比较对象的目标值的比例更高；但必须结合平局率和负率判断，低于50%并不必然表示总体较差。）

</div>
<div class="metric-item" markdown="1">

**胜／平／负比例（win/tie/loss percentages）**

按目标值将每个实例的比较结果记为SLIM优于、等于或劣于基线，用于展示胜率之外的完整结果分布。它尤其能区分“没有获胜但多数打平”和“经常得到更差解”两种情况。 （胜率和并列率越高、负率越低越好；其中胜率体现严格改进，并列率体现至少保持基线质量。）

</div>
<div class="metric-item" markdown="1">

**净胜分（win minus loss）**

以问题加权胜率减去问题加权负率，衡量严格改进相对于严格退步的净优势。它补充了单独胜率无法表达的风险信息。 （越高越好；正值表示严格胜出的比例超过严格失败的比例。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 整体算法选择效果：按实例选择SLIM配置，对比one-shot Gurobi和最佳单一配置。

<div class="result-value" markdown="1">

作者在摘要中报告，算法选择相对one-shot Gurobi取得39.5%的平均问题加权胜率，而最佳单一配置为19.3%，即算法选择的胜率超过后者两倍。

</div>

这说明固定一种搜索策略会损失大量跨实例适应性，而根据通用图特征选择配置能更充分利用配置组合。39.5%低于50%不能直接解释为“多数情况下更差”，因为严格胜率不包含大量目标值相同的实例；同时该比较只证明在所选20类、经过难度筛选的MiniZinc实例和60分钟预算下有效，不能证明对任意约束优化问题或其他预算同样有效。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We evaluated our pipeline on instances across 20 MiniZinc competition problems, finding that algorithm selection achieves a 39.5% average problem-weighted win rate against a one-shot Gurobi baseline, more than doubling the best single configuration (19.3%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 五种算法选择方法在随机种子51、52、53上的表现，对比最佳单一配置。

<div class="result-value" markdown="1">

最佳单一配置在不同种子上的问题加权胜率为17.8%—22.3%，而五种选择方法在每个种子上都超过31%；每个种子中表现最好的选择器达到37.9%—40.6%，净胜分为14.8%—24.5%。

</div>

这一结果直接检验了“按实例选配置”是否优于“一套配置用于所有实例”：所有五种方法均跨种子超过固定配置，说明收益并非只来自某一种选择器。正净胜分进一步说明严格改进多于严格退步。不过，所给Table 1正文只提供范围，没有逐方法、逐种子的完整表格行，因此不能据此确定每种选择器的精确排名或显著性大小。

<div class="result-source" markdown="1">

来源：Section 4.3, Table 1 discussion

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In general, for the best-performing approach on each seed, the problem-weighted win rates are tightly clustered (37.9–40.6%) with positive net scores (win minus loss of 14.8–24.5%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 每种问题类型采用其最佳SLIM配置，与相同预算的one-shot Gurobi比较。

<div class="result-value" markdown="1">

在tdtsp、spot5、community-detection、triangular和opd五类问题上，SLIM在超过75%的实例中胜过one-shot Gurobi；20类问题中，仅rectangle-packing和VRP两类在超过50%的实例上得到更差解。

</div>

该结果表明结构引导的局部改进在若干问题类型上具有很强潜力，同时效果明显依赖问题类型。由于这里为每种问题类型选择其最佳配置，并且每个实例运行了30种配置，这更接近配置池能力分析，而不是未知实例上的可部署性能；真正的自动化泛化能力应以训练后算法选择器的测试结果为准。

<div class="result-source" markdown="1">

来源：Section 4.2, Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On problems including tdtsp, spot5, community-detection, triangular, and opd, SLIM can win over 75% of the instances.

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

- One-shot Gurobi：直接在原始MiniZinc实例上运行Gurobi，使用与SLIM相同的60分钟总预算。它是有意义的强基线，因为比较的是“将预算一次性交给成熟商业求解器”与“把Gurobi作为子求解器进行结构引导的迭代局部改进”两种预算使用方式。
- Best single configuration：在全部实例上固定使用表现最好的一个SLIM配置。它检验算法选择器的收益是否真正来自按实例调整配置，而不是仅仅因为配置池中存在一个普遍较强的配置。
- Virtual best：对每个测试实例事后选择配置池中表现最好的配置，是依赖真实测试结果的理想上界，不能作为可部署算法。它用于衡量配置池的潜在空间，以及实际算法选择器距离完美选配仍有多远。
- 随机变量抽取的SLIM／标准大邻域搜索：当变量抽取是随机的且不使用统一图权重时，使用Gurobi子求解器的SLIM退化为标准大邻域搜索。它在概念上用于区分结构引导选择与随机选择，但所给实验章节未报告其独立汇总分数。

**实验想回答的问题**

- 在相同的60分钟总预算下，由统一加权图引导变量选择的、问题无关的SLIM，能否比直接在原始MiniZinc实例上运行一次Gurobi得到更好的目标值？
- 利用实例的通用图特征为每个实例自动选择SLIM配置，是否能超过对所有实例固定使用同一个最佳配置；不同算法选择器的效果和稳定性如何？

**实验实现**

所有实验在Sun Grid Engine集群上运行，共20个Ubuntu 18.04 LTS节点；每个节点配备两颗Intel Xeon E5-2640 v4 2.40 GHz CPU和160 GB内存，SLIM及相关程序使用Python 3.6.9。SLIM与one-shot Gurobi采用相同的60分钟总预算；比较目标值时，SLIM在每个实例上运行30种配置，Figure 2使用每种问题类型上表现最好的配置，并对3个随机种子取平均。算法选择实验评估五种选择方法，并使用随机种子51、52、53及相同的训练／测试实例分布。作者提供了Zenodo复现材料，地址为https://doi.org/10.5281/zenodo.21910103。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 配置与图特征消融后的组合调整。 | 摘要报告该消融将问题加权胜率进一步提高到44.0%，相对完整算法选择结果39.5%提高4.5个百分点。 | 按作者表述，这项实验用于检查配置集合和输入图特征中是否含有无效或有害成分；删减后反而提升，说明更大的配置池或特征集并不必然更好，冗余信息可能增加选择难度。然而所给章节没有提供被移除的具体配置、特征、独立消融顺序或逐项结果，因此无法判断4.5个百分点主要来自配置裁剪、特征裁剪还是二者交互，也无法评估统计稳定性。 | Abstract；所给Section 4.1—4.3未包含详细消融表<br><span class="experiment-evidence">Configuration and feature ablation boost the performance further to 44.0%, demonstrating that LLM-based semantic generation enables effective automated structure extraction and feature extraction for constraint optimization.</span> |

**定性案例**

- filters与grid-coloring构成一个有解释价值的边界案例：SLIM没有在任何实例上严格超过one-shot Gurobi，但所有实例都取得相同质量的解。这表明零胜率不等于方法失败，而可能意味着基线已达到相同的可达解质量；相反，rectangle-packing和VRP在超过半数实例上更差，才更直接暴露结构表示、配置选择或局部搜索机制对特定问题类型的不适配。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The central method uses an LLM to synthesize graph-generator code that extracts optimization-problem structure for local improvement and configuration selection.; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`b0cb8b199facc536cf383990d61ad811408c395d6b80445fbc373748e59ec136`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
