---
title: "[论文解读] GoT-CD: Graph-of-Thoughts Causal Discovery and the Fragility of Post-hoc Path-Specific Fairness Audits"
description: "[arXiv 2608.02877][LLM Reasoning] 本文追问：当因果发现得到的图被用于路径特定公平性审计时，整体结构指标看似良好是否仍可能遗漏审计所依赖的关键因果路径，并探索以完整候选图为推理单元的图式思维能否同时改善有向无环图的有效性与关键路径恢复。"
arxiv_id: "2608.02877"
announcement_date: "2026-08-05"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:42:35.935668+00:00"
source_sha256: "aa7702260e4ac112777b2fb30eb2903fa0aff8984933041c9d6638ec9f8935d7"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "因果发现"
  - "有向无环图"
  - "大语言模型"
  - "Graph of Thoughts"
  - "路径特定公平性"
  - "反事实公平性"
  - "临床决策支持"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.02877</p>

# GoT-CD: Graph-of-Thoughts Causal Discovery and the Fragility of Post-hoc Path-Specific Fairness Audits

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Nitish Nagesh, Elahe Khatibi, Thomas Dean Hughes, Mahdi Bagheri, Pratik Gajane, Amir M. Rahmani</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Department of Computer Science, University of California, Irvine, Irvine, CA, USA</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.02877v1) · [PDF 下载](https://arxiv.org/pdf/2608.02877v1) · **关键词** 因果发现, 有向无环图, 大语言模型, Graph of Thoughts, 路径特定公平性, 反事实公平性, 临床决策支持<br>


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

本文追问：当因果发现得到的图被用于路径特定公平性审计时，整体结构指标看似良好是否仍可能遗漏审计所依赖的关键因果路径，并探索以完整候选图为推理单元的图式思维能否同时改善有向无环图的有效性与关键路径恢复。

**不用术语来说**：临床研究常先根据观察数据推断变量之间的因果关系，再利用推断出的关系图检查性别等敏感属性是否通过不合理的中间机制影响预测结果。问题在于，公平性结论完全依赖前一步得到的图：如果算法恰好漏掉从敏感属性到结果的关键路径，后续审计就可能把“没有找到路径”误当成“没有不公平影响”。因此，一张在整体边预测上得分不错的图，也可能给出具有误导性的公平证明。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将因果发现的评价目标从单纯的全图结构一致性推进到下游审计相关的路径保真度，指出应同时报告敏感属性至结果的关键路径是否被恢复，而不能只报告对所有边等权汇总的结构指标。
- 作者提出 GoT-CD：并行生成多个完整候选边集，以确定性的有效性函数评分，在禁止引入候选图之外新边的硬并集约束下合并，并通过贪心投影在最终提交前保证输出为有向无环图；该设计旨在克服局部、不可回溯的 LLM 因果发现过程。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

因果发现旨在从观测数据中恢复变量之间的有向因果结构；在难以开展随机试验的临床与生物医学场景中，所得图可用于机制推理、选择因果效应估计所需的调整变量，以及审计预测模型是否存在不公平影响。传统方法主要依赖条件独立性检验或参数化评分，但在小样本条件下可能统计功效不足；大语言模型方法则尝试利用预训练获得的领域知识补充数据证据。本文进一步关注“发现图—公平审计”串联流程：路径特定反事实公平性以给定因果图为定义基础，因此即使发现图的整体结构指标较好，只要敏感属性到结果变量的关键路径被遗漏，后续审计仍可能错误地给出无不公平影响的结论。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**有向无环图（DAG）**

DAG用节点表示变量、用有向边表示假定的直接因果关系，并禁止形成沿箭头方向返回起点的环。无环性使变量能够按因果先后排列，也是本文判定发现结果是否为有效因果图的基本条件。

</div>
<div class="concept-item" markdown="1">

**因果发现**

因果发现根据观测样本推断变量间的边及其方向，而不是在已知因果图上只估计某个效应。由于仅靠观测分布通常不能无条件识别唯一因果图，算法需要依赖统计假设、结构评分或外部领域知识。

</div>
<div class="concept-item" markdown="1">

**路径特定反事实公平性**

该概念区分敏感属性影响结果的不同因果路径，并检验被认定为不正当的路径所传递的效应。其估计依赖输入因果图：若图中缺失关键的敏感属性到结果路径，审计可能将路径特定效应报告为零，而这并不等同于真实公平。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是在固定变量集合上采集的观测数据；论文报告的核心设置采用小样本协议 $n=100$，并允许大语言模型利用变量语义和预训练领域知识进行结构推理。因果发现阶段输出这些变量上的有向图，目标是得到有效DAG并尽可能恢复真实的边与方向；下游阶段再以该图为依据，审计敏感属性 $S$ 是否通过特定中介路径影响结果 $Y$。问题的关键不只是提高全图层面的结构一致性，还要确认公平估计所依赖的 $S\to Y$ 路径是否被恢复：一旦该路径缺失，审计可能输出零路径特定效应，从而形成与真实公平难以区分的“错误清白”结果。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$n$**

用于因果发现的观测样本数；本文摘要所述锁定实验协议取100。

</div>
<div class="notation-item" markdown="1">

**$S$**

受保护或敏感属性，例如阿尔茨海默病基准中的性别。

</div>
<div class="notation-item" markdown="1">

**$Y$**

公平审计关注的结果变量，例如认知评估结果。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{PSE}_{|\cdot|}$**

论文报告的路径特定效应绝对量，用于衡量指定因果路径上传递的影响大小。

</div>

</div>

**直接相关的工作**

- **PC、GES、NOTEARS与DAGMA等经典因果发现方法**: 这些方法分别以条件独立性检验、离散结构评分搜索或连续优化为主要依据，是本文比较和定位LLM因果发现的统计学习背景；原文指出，它们所依赖的检验或参数化评分面在小样本下可能统计功效不足。
- **基于LLM的成对查询与广度优先遍历式因果发现**: 成对方法逐一询问变量 $A$ 是否导致变量 $B$，查询规模随变量数呈二次增长，且模型看不到逐步形成的全局结构；遍历方法在每个节点询问其直接结果变量，但会不可逆地提交局部决定，使早期错误传播。本文以完整候选边集作为推理单位，正是针对这两类局部推理限制。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在临床与生物医学场景中，随机实验往往不可行，研究者因而使用观察数据恢复因果图，并据此开展机制解释、效应估计和模型公平性审计。路径特定反事实公平性尤其关注敏感属性是否沿不应被允许的中介路径影响结果，但其估计对象由输入的因果图定义；一旦发现阶段漏边、错向或破坏关键路径，审计数值便可能不再对应真实的不公平机制，甚至产生与真正公平无法从输出上区分的“错误清白证明”。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **经典统计因果发现方法**：PC 等约束型方法通过条件独立检验删边并确定方向，GES 等评分型方法搜索使统计评分更优的图，NOTEARS 与 DAGMA 等连续松弛方法则把离散图搜索转化为带无环约束的连续优化。这些方法主要从观测数据中的统计关系恢复结构。
- **基于 LLM 的局部因果发现**：成对询问方法逐一判断变量 $A$ 是否导致变量 $B$，再把所有局部答案拼成图；遍历式方法按广度优先顺序处理节点，并询问当前节点直接导致哪些变量。两者试图利用 LLM 预训练所得的领域知识，补充小样本条件下统计证据不足的问题。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 经典统计方法依赖条件独立检验或参数化评分曲面，在样本量较小时可能统计功效不足；其后果是关键因果边可能因证据弱而被遗漏，从而使依赖这些边的机制分析或公平性审计失真。
- 现有 LLM 方法以局部判断为主：成对询问的查询量随变量数呈二次增长，而且模型看不到正在形成的全局结构；遍历式方法虽然提供部分局部上下文，却会不可撤销地提交每次扩展，早期错误可持续传播。与此同时，常用整体结构指标对所有边等权计分，无法说明下游公平审计所依赖的特定路径是否仍然存在。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少一种把“图在形式上有效、整体结构恢复较好”与“图保留了下游公平审计所需关键路径”联系起来的评价框架，也缺少能够让 LLM 在提交局部边之前比较、合并和修正完整候选图的发现机制。因此，结构分数与审计可靠性之间的断层尚未被系统检验：当敏感属性到结果的路径消失时，路径特定审计究竟会报告什么，也没有成为标准评测问题。

</div>
<div markdown="1"><span>核心问题</span>

完整图级的 Graph-of-Thoughts 因果发现能否在稳定输出有效有向无环图的同时，达到有竞争力的结构恢复质量；更关键的是，整体结构质量能否保证敏感属性至结果的审计相关路径被恢复，若该路径被遗漏，事后路径特定公平性审计是否会错误地给出零效应或“公平”结论？

</div>
<div markdown="1"><span>作者直觉</span>

局部逐边决策像是在没有总图的情况下逐段修路，一次错误连接便可能影响后续方向，而且难以返工。GoT-CD 改为让模型先提出多张完整候选图，使每个方案都能在全局结构中接受检查，再仅从候选边中合并较可信的部分，并在最终输出前消除环。这样既保留了不同推理方案可能共同支持的因果关系，又限制合并过程凭空创造新边；而单独检查审计关键路径，则能揭示整体平均分掩盖的、对公平结论具有决定意义的局部错误。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

GoT-CD 将因果发现建模为“完整候选图”层面的 Graph-of-Thoughts 推理，而不是逐变量对或逐节点决定边。输入是观测数据的变量名称、变量描述与领域提示；模型并行生成 $k$ 个完整候选边集，确定性评分器筛除格式或结构较差的候选，再在候选边并集约束下聚合、改进，并通过贪心无环投影输出有向无环图（DAG）。所得邻接矩阵首先与参考图比较边级结构指标；在阿尔茨海默病案例中，还要基于发现图重新拟合线性结构方程，枚举从敏感属性 $S$ 到结果 $Y$ 的路径并计算路径特定效应。

核心设计意图是把全局结构一致性纳入一次推理：模型提出的是整张图，因而可同时考虑多条边之间的方向与环路关系；硬并集约束又防止聚合阶段凭空增加未被任何分支支持的边。通俗地说，系统先让多个“专家”各画一张完整因果图，再用可复现的规则选图、合图和去环；最后不仅检查整张图像不像参考图，还检查公平性审计真正依赖的特定路径是否仍然存在。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 完整候选图生成

执行 $\textsc{Generate}(k)$：以一次提示要求 LLM 返回 $k$ 个彼此不同的完整候选边集，并将文本响应解析为有向边列表；多词变量名采用最长优先匹配，避免将 $\mathrm{Brain\ Volume}$ 等名称截断。

<div class="method-step__io" markdown="1">

**输入**：数据集中全部变量的名称与描述、领域前言，以及分支数 $k$。<br>
**输出**：$k$ 个覆盖完整变量集合的候选有向图。

</div>

**直观理解**：不是对每一对变量单独提问，而是让模型一次画出若干张完整图。这样模型能够在判断一条边时同时顾及整张图的方向和结构。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 确定性评分与候选保留

对每张图应用固定局部评分：未声明变量的边每条罚 $-5$，自环每条罚 $-3$，合法边数量获得奖励；无环图加 $3$，有环图罚 $-4$，并以软密度先验抑制边数少于 $0.5n$ 或多于 $2.5n$ 的图，其中 $n$ 是变量数。随后执行 $\textsc{KeepBestN}(\min(2,k))$。

<div class="method-step__io" markdown="1">

**输入**：$k$ 个候选图及声明的变量集合。<br>
**输出**：至多两个得分最高的完整候选图。

</div>

**直观理解**：评分器只检查边是否合法、图是否无环以及密度是否过于极端，并不利用参考答案判断因果正确性。固定规则使候选排序可复现，也不需要额外调用模型。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 受约束聚合与改进

$\textsc{Aggregate}$ 要求模型合并候选图，但输出边必须属于输入候选边的并集，解析器还会再次执行该过滤；$\textsc{Improve}$ 随后细化合并图，是唯一可提出并集外新边的操作，新边仅在不会与已接受核心构成有向环时逐条接纳。若改进结果为空，则回退到最高分生成候选的并集。

<div class="method-step__io" markdown="1">

**输入**：保留候选图的边集及其并集。<br>
**输出**：受候选证据约束、可能包含少量安全改进边的合并图。

</div>

**直观理解**：聚合阶段只能从多个草图中“选边”，不能临时编造新边；改进阶段虽可补边，但每条补边都必须通过无环检查。这在保留修正能力的同时限制了模型凭常识随意扩张图结构。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 无环投影与结构输出

按列表顺序遍历所有边，仅保留不会与当前已接受边形成有向环的边，完成贪心 DAG 投影；最终图按数据框列顺序转成邻接矩阵，并计算边级精确率、召回率、$F_1$、预测边数及 DAG 有效性。

<div class="method-step__io" markdown="1">

**输入**：聚合并改进后的有序边列表。<br>
**输出**：保证无环的发现图及与参考图对齐的邻接矩阵。

</div>

**直观理解**：系统像按顺序往图里放边：如果新边会把已有路径首尾相接成环，就丢弃它。该方法保证输出可用于后续因果路径分析，但环中哪条边被删除取决于输出顺序，而不一定取决于证据强弱。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### GoT-CD 操作图

$$
\begin{split}\textsc{Generate}(k)\to\textsc{Score}\to\textsc{KeepBestN}(\min(2,k))\to\\ \textsc{Aggregate}\to\textsc{Improve}\to\textsc{Score}\to\textsc{KeepBestN}(1)\end{split}
$$

**符号说明**

- $k$：生成阶段并行提出的完整候选图数量，即分支因子。
- $\textsc{Generate}(k)$：根据变量名称、描述和领域提示生成多个完整候选边集。
- $\textsc{Score}$：用固定的结构有效性规则为候选图评分，不调用语言模型。
- $\textsc{KeepBestN}(m)$：保留评分最高的 m 个候选；第一次至多保留两个，最后保留一个。
- $\textsc{Aggregate}$：在保留候选边集的硬并集约束下生成合并图。
- $\textsc{Improve}$：细化合并图，并在逐边无环检查下允许有限的并集外新增边。

<div class="equation-explanation" markdown="1">

**直观理解**：该式定义方法的端到端推理顺序，而不是需要梯度最小化的损失函数。其关键是先保留少量较可靠的完整图，再受约束地合并和修正，最后重新评分并选出唯一结果。<br>
**原文位置**：第 3.2 节，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 单条有向路径的线性路径特定效应

$$
\mathrm{PSE}(\pi)=\prod_{l=0}^{L-1}B_{v_l,v_{l+1}}
$$

**符号说明**

- $\pi=\langle S=v_0,v_1,\ldots,v_L=Y\rangle$：从敏感属性 S 出发、经过若干中间变量并到达结果 Y 的一条简单有向路径。
- $S$：受保护或敏感属性；阿尔茨海默病案例中为 Sex。
- $Y$：审计结果变量；阿尔茨海默病案例中为 MOCA Score。
- $v_l$：路径上的第 l 个变量节点。
- $L$：路径所含有向边的数量。
- $B_{v_l,v_{l+1}}$：在线性结构方程中，从节点 $v_l$ 指向节点 $v_{l+1}$ 的回归系数。
- $\mathrm{PSE}(\pi)$：沿指定路径 π 传递的线性效应。

<div class="equation-explanation" markdown="1">

**直观理解**：在线性模型中，上游变量的单位变化会依次乘上每条边的回归系数，因此整条路径的作用是这些系数的乘积。将所有路径的 $\mathrm{PSE}(\pi)$ 相加得到总线性效应；将其绝对值相加得到 $\mathrm{PSE}_{|\cdot|}$，可避免正负路径相互抵消后看似没有影响。<br>
**原文位置**：第 3.5 节，公式（2）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。GoT-CD 不是通过论文数据重新训练或微调语言模型，而是在固定预训练 LLM 上执行提示驱动的推理流程；确定性结构评分只用于候选排序，并非可微训练损失。公平性阶段的普通最小二乘和逻辑回归分别拟合发现图上的局部结构方程与二值化中介模型，但它们属于事后参数估计，不会反向更新 GoT-CD 或其 LLM 主干。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 完整图级 Graph-of-Thoughts 控制流**

单次操作图为 $\textsc{Generate}(k)\to\textsc{Score}\to\textsc{KeepBestN}(\min(2,k))\to\textsc{Aggregate}\to\textsc{Improve}\to\textsc{Score}\to\textsc{KeepBestN}(1)$，其中每个 thought 表示完整候选边集。它区别于逐变量对判断以及 BFS 中按节点逐步扩展的局部表示。

> 直观理解：完整图是推理的基本单位，使每个分支都能表达一种全局因果解释。与逐边拼图相比，这更容易在生成时顾及边之间的兼容性，但也要求模型在一次响应中输出完整边表。

**2. 硬并集约束与确定性有效性评分**

评分不调用 LLM，而依据非法变量、自环、合法边数、无环性和图密度进行固定计算；聚合结果必须属于保留候选边集的并集，并由解析器强制过滤。只有后续 $\textsc{Improve}$ 能提出并集外边，且这些边须逐条通过环检测。

> 直观理解：评分器解决“如何稳定选候选”，并集约束解决“合并时是否会凭空造边”。两者都不是因果正确性的证明，而是控制输出格式、结构有效性和模型自由度的护栏。

**3. DAG 投影与路径审计接口**

最终贪心投影保证 GoT-CD 输出 DAG，使 $(I-B)^{-1}$ 与有向路径枚举可直接使用。对其他方法产生的循环图，论文在审计前反复删除检测到的环上一条边，但明确说明这不是最小反馈边集，而是额外的建模选择。

> 直观理解：路径特定公平性需要方向明确且无环的因果图；否则路径和效应定义会受到如何断环的影响。因此“始终输出 DAG”不仅是格式要求，也减少了公平性审计前人为删边带来的不确定性。

**训练与推理**

推理时，系统先向固定 LLM 提供全部变量名称、变量描述和领域前言，要求一次生成 $k$ 张完整候选图。候选图经过解析和确定性评分后保留至多两张；聚合提示在硬并集约束下生成合并图，解析器再次删除并集外边；改进操作可提出新边，但后处理仅接纳不会成环的新增边。改进结果若为空则回退到高分候选并集，随后对全部边执行顺序敏感的贪心无环投影，输出与数据列顺序对齐的邻接矩阵。

结构评估完成后，在每个发现图上单独估计审计参数：每个节点对其图中父节点进行普通最小二乘回归以形成 $B$，然后枚举 $S\to Y$ 简单有向路径并计算路径效应。离散审计则按中位数二值化相关变量并拟合逻辑回归。若输入方法产生循环图，必须先用启发式反馈边删除程序断环；这一步会改变审计所依据的图，因此其结果不能与原生 DAG 输出完全等同解释。

**复现信息**

报告实验采用 $gpt\text{-}4o\text{-}mini$，温度为 $0.7$，主设置分支因子为 $k=3$，每次响应上限为 $2048$ token，以容纳完整边列表；分支消融另考察 $k\in\{1,3,5\}$。所有方法使用同一批 $n=100$ 的观测数据与固定随机种子 $0$；这一小样本锁定协议便于方法间比较，但结论仅覆盖论文报告的五个基准。

复现时必须保留三项会实质影响结果的处理：多词变量名采用最长优先解析；聚合结果由程序而非仅靠提示强制限制在候选并集中；最终边按模型输出顺序进行贪心投影。最后一项意味着同一循环中的保留边由列表位置决定，而非统计证据或因果置信度，这是解释结果和设计改进版本时的重要限制。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 五个报告的基准包括 Asia、Child、Alzheimer’s Disease、COVID-Respiratory 和 Sweden-Traffic。它们用于评估因果图的结构恢复质量；原文未明确报告每个数据集的变量规模、具体训练/测试划分或完整样本构造方式。
- Alzheimer’s Disease 基准包含一个由专家给出的 $19$ 条边的参考图，用于结构一致性评估；同一基准还用于公平性审计，其中敏感属性为 $S=\mathrm{Sex}$，结果变量为 $Y=\mathrm{MOCA\ Score}$，已知的不公平路径为 $S\rightarrow\mathrm{Brain\ Volume}\rightarrow Y$。
- 每个报告的发现运行使用 $n=100$ 个观测样本。COVID-Complications、Neuropathic 以及统计量增强的 LLM 变体被排除在报告表格之外，因此不能据此推断它们的完整性能。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Precision**

预测边中属于参考图的比例，衡量发现图加入错误边的程度。 （越高越好，因为较高值表示较少的假阳性边。）

</div>
<div class="metric-item" markdown="1">

**Recall**

参考图中的真实边被发现图恢复的比例，衡量漏掉真实因果关系的程度。 （越高越好，因为较高值表示遗漏的真实边更少。）

</div>
<div class="metric-item" markdown="1">

**$F_1$**

Precision 与 Recall 的调和平均，用一个指标平衡错误加入边和遗漏边两类误差；原文还报告预测边数、真实边数和 DAG validity，但本输出优先保留三项结构质量指标。 （越高越好，因为它要求精确率和召回率同时较高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Alzheimer’s Disease 的结构恢复

<div class="result-value" markdown="1">

在包含 $19$ 条专家参考边的 Alzheimer’s 基准上，GoT-CD 的 $F_1$ 为 $0.757$，Precision 为 $0.778$，Recall 为 $0.737$；其表现高于最强经典基线 GES 的 $F_1=0.650$，也高于 LLM-BFS 的 $F_1=0.649$。

</div>

这说明在该基准上，GoT-CD 同时较好地控制了错误边和漏边，并在边级结构指标上优于所报告的经典与 LLM 基线。但这一结果只说明边集合与参考图较接近，不等于所有关键因果路径都被恢复，也不等于后续公平性审计一定正确。

<div class="result-source" markdown="1">

来源：Section 4.1, Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GoT-CD attains the highest F1 (0.757) with balanced precision (0.778) and recall (0.737), outperforming every classical baseline (strongest: GES, F1 = 0.650) and every LLM baseline, including LLM-BFS (F1 = 0.649).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 五个报告基准上的 DAG 有效性

<div class="result-value" markdown="1">

论文摘要声称 GoT-CD 在五个报告基准上都返回有效 DAG，并在 Asia、Alzheimer’s 和 COVID-Respiratory 上取得 LLM 方法中最好的 DAG-valid $F_1$。

</div>

DAG 有效性表示输出图没有有向环，是进行标准因果解释和许多下游计算的必要结构条件。该结果支持 GoT-CD 的输出可用性和结构竞争力，但“有效 DAG”本身不保证边方向正确，也不保证关键公平路径被保留。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GoT-CD returns a valid DAG on all five reported benchmarks and achieves the best DAG-valid F1 score among LLM methods on Asia, Alzheimer's, and COVID-Respiratory datasets.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Alzheimer’s 上的路径特定公平性审计

<div class="result-value" markdown="1">

在存在已知不公平路径 $S\rightarrow\mathrm{Brain\ Volume}\rightarrow Y$ 的 Alzheimer’s 基准上，$8$ 个发现图中有 $5$ 个没有恢复从敏感属性到结果的路径，因此报告零总体效应；然而中介效应仍然存在。

</div>

该结果直接揭示了结构指标与公平性审计之间的断裂：如果发现图漏掉敏感属性到结果的关键路径，后续审计可能把真实存在的总体影响误判为零。它并非证明 GoT-CD 的所有发现图都不适合公平性分析，而是说明必须在结构发现之后额外检查审计所依赖的具体路径。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On an Alzheimer's benchmark with known unfair path, a post-hoc path-specific audit shows that five of eight discovered graphs recover no path from the sensitive attribute to the outcome and therefore report a null overall effect while mediated effects persist, necessitating downstream path-specific fairness analysis along with structural discovery.

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

- GES：经典基于评分的因果发现方法，用于检验 GoT-CD 相对于传统结构搜索的改进。
- PC：经典基于条件独立性检验的方法，用于比较另一类主流因果发现范式；原文指出其在 Alzheimer’s 结果中未返回 DAG。
- NOTEARS 与 DAGMA-linear：连续优化型因果发现基线，用于比较不同的 DAG 约束优化策略。
- LLM-BFS、LLM-pairwise 与 GoT-CD-BFS：大语言模型或搜索策略相关比较方法，用于区分完整图级推理、逐边推理和搜索过程的影响；受列表限制，这些方法作为一组 LLM/搜索基线理解。

**实验想回答的问题**

- GoT-CD 能否在多个基准上恢复与专家或真实结构一致、且满足有向无环图约束的因果图，并与经典因果发现方法及大语言模型基线竞争？
- 即使发现图的整体结构指标较好，图中与路径特定公平性审计有关的敏感属性到结果变量的关键路径是否仍可能缺失，从而改变审计结论？

**实验实现**

所有发现运行使用 $\mathrm{gpt\text{-}4o\text{-}mini}$ 作为 LLM 主干，温度为 $0.7$，随机种子为 $0$，GoT 分支因子为 $k=3$；Asia 和 Child 使用锁定的观测抽样，其余基准使用固定的线性 CSV 文件。GoT-CD 以完整候选边集作为推理单元，并行生成多个候选图，由确定性的有效性函数评分，在禁止发明候选边的硬联合约束下合并，再通过贪心投影确保提交结果为 DAG。实验先计算结构一致性，再在 Alzheimer’s 图上进行路径特定公平性审计。该审计检查敏感属性 $S$ 到结果 $Y$ 的路径是否被发现图保留；其作用不是重新发现因果图，而是测试结构错误会不会改变后续公平性结论。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- Alzheimer’s 公平性案例以 $S=\mathrm{Sex}$ 为敏感属性、$Y=\mathrm{MOCA\ Score}$ 为结果，并考察已知不公平路径 $S\rightarrow\mathrm{Brain\ Volume}\rightarrow Y$。$8$ 个发现图中有 $5$ 个未恢复任何从 $S$ 到 $Y$ 的路径，却仍存在中介效应；该案例说明，审计系统若只依赖发现图中的总体路径，可能将路径缺失误读为不存在不公平影响。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It develops a Graph-of-Thoughts reasoning procedure that generates, scores, merges, and validates candidate causal graphs.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`aa7702260e4ac112777b2fb30eb2903fa0aff8984933041c9d6638ec9f8935d7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
