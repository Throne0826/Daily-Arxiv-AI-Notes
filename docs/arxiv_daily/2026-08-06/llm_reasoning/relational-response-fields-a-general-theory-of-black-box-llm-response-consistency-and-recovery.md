---
title: "[论文解读] Relational Response Fields: A General Theory of Black-Box LLM Response Consistency and Recovery"
description: "[arXiv 2608.04552][LLM Reasoning] 本文把多个经变换查询所得的黑盒大模型回答组织为“关系响应场”，并提出关系—锚点裕量 $\\gamma_k(D,A)$，用于判断至多 $k$ 个回答节点遭到破坏时是否能够恢复，以及恢复问题在噪声下有多困难。"
arxiv_id: "2608.04552"
announcement_date: "2026-08-06"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T07:06:26.848712+00:00"
source_sha256: "f08f377005b4a386e5f13fff523a95c025cab6f3d6ab5b4e7a81461d91e8802f"
tags:
  - "LLM Reasoning"
  - "幻觉检测"
  - "黑盒大语言模型"
  - "关系响应场"
  - "响应一致性"
  - "组稀疏恢复"
  - "关系缺陷算子"
  - "锚点"
  - "可辨识性"
  - "受限最小奇异值"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.04552</p>

# Relational Response Fields: A General Theory of Black-Box LLM Response Consistency and Recovery

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Song Zichen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Sungkyunkwan University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04552v1) · [PDF 下载](https://arxiv.org/pdf/2608.04552v1) · **关键词** 黑盒大语言模型, 关系响应场, 响应一致性, 组稀疏恢复, 关系缺陷算子, 锚点, 可辨识性, 受限最小奇异值<br>


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

本文把多个经变换查询所得的黑盒大模型回答组织为“关系响应场”，并提出关系—锚点裕量 $\gamma_k(D,A)$，用于判断至多 $k$ 个回答节点遭到破坏时是否能够恢复，以及恢复问题在噪声下有多困难。

**不用术语来说**：面对无法查看参数或重新训练的黑盒大模型，人们常通过改写问题、多次采样、投票或验证来提高可靠性，但收集更多回答并不意味着一定能找回正确答案：多个回答可能彼此完全一致，却共同包含同一种错误。本文要解决的基础问题是，在采用任何具体修复算法之前，如何根据回答之间的已知关系和少量可信证据，判断正确回答是否原则上可辨认、可稳定恢复。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将释义、单位缩放、任务分解、代码重构等查询变换统一表示为关系响应场：节点保存解析后的回答，边上的类型化传输规定有效回答应如何随查询变换，外部执行结果、验证器或人工标签则作为可信锚点。由此，不同的黑盒可靠性操作被转化为同一个结构化逆问题。
- 作者提出受限可观测裕量 $\gamma_k(D,A)$，并声称其正值恰好对应所有至多 $k$ 节点破坏的一致可识别性，恢复误差的最优最坏情形尺度由 $1/\gamma_k(D,A)$ 控制；同时区分信息论上的可识别性与可计算群 $\ell_1$ 解码器所需的更强零空间条件。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究黑盒大语言模型的响应可靠性：模型只能通过接口查询，无法检查参数、计算梯度或重新训练，因此可靠性方法通常在推理阶段生成多个相关回答，再利用投票、自我修订、验证器或输入变换进行检查。论文把这些回答统一表示为“关系响应场”（Relational Response Field, RRF）：对同一任务施加释义、缩放、分解、代码重构等有已知语义关系的变换，以图节点表示变换后的查询及其响应，以边上的传输规则约束正确响应应如何随变换而变化；执行结果、人工标签或外部验证器则提供独立可信的锚点。由此，可靠性问题被表述为一个带组稀疏错误的黑盒逆问题：关键不只是回答是否彼此一致，而是关系与锚点能否唯一辨认真值并定位少量受损节点。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**黑盒模型**

只能提交查询并观察输出，不能访问模型内部参数、隐藏状态或梯度。本文因此仅使用解析后的响应、响应之间的已知关系以及外部可信证据进行恢复。

</div>
<div class="concept-item" markdown="1">

**组稀疏恢复**

假设错误只出现在少数响应节点，但一个节点内部可以包含多个同时变化的数值或结构化坐标，因此按节点而非按单个坐标统计稀疏度。本文假设至多有 $k$ 个响应节点被破坏。

</div>
<div class="concept-item" markdown="1">

**受限最小奇异值**

它衡量一个线性算子在指定稀疏方向上区分非零扰动的最弱能力；值越接近零，就越容易出现不同候选响应场产生几乎相同观测的情况。本文的 $\gamma_k(D,A)$ 将这一思想用于关系与锚点组成的实例级算子。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定由变换后查询构成的图 $G=(V,E)$，黑盒模型在节点 $i$ 上的原始输出经解析器映射为结构化响应 $z_i$，全部节点的响应组成场 $z=(z_i)_{i\in V}$。每条边 $e=(i,j)$ 带有已知类型的传输 $T_e$，用于描述有效响应应满足的关系 $z_j=T_ez_i$；将各边残差 $z_j-T_ez_i$ 堆叠后得到关系缺陷算子 $D$，可信执行结果、约束、验证器或人工标签则构成锚点算子 $A$。论文考虑至多 $k$ 个节点被任意破坏的情形，目标是从关系缺陷和锚点证据中识别并恢复真实响应场。基本假设是传输关系及锚点本身已知且可计算，而响应生成模型保持黑盒；关系一致性并不自动等于正确性，因为任何位于 $\ker D$ 中的共同偏移都不会改变关系缺陷，只有适当锚点才能消除这类不可观测方向。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$G=(V,E)$**

变换查询图；$V$ 是响应节点集合，$E$ 是带类型关系的边集合。

</div>
<div class="notation-item" markdown="1">

**$z=(z_i)_{i\in V}$**

关系响应场，即所有节点上经黑盒解析器结构化后的模型响应。

</div>
<div class="notation-item" markdown="1">

**$D,\ A$**

$D$ 是堆叠边关系残差的关系缺陷算子；$A$ 是编码执行、约束、验证器或人工标签等可信证据的锚点算子。

</div>
<div class="notation-item" markdown="1">

**$\gamma_k(D,A)$**

关系—锚点算子在不超过 $2k$ 个节点的组稀疏方向上的最小增益，用于刻画至多 $k$ 个节点受损时的可辨识性与稳定性；其为正当且仅当所有此类破坏都可被统一识别。

</div>

</div>

**直接相关的工作**

- **Metamorphic testing（蜕变测试）**: 该类方法在缺少标准答案时变换输入，并检查不同输出是否满足预先知道的关系；本文将这些输入变换、输出关系和其他推理时方法共同表示为RRF中的节点、边与传输。
- **Group-sparse recovery（组稀疏恢复）**: 该领域提供按组建模少量受损单元、受限奇异值及零空间条件等数学工具；本文把它们用于黑盒LLM响应节点，同时强调信息论上的可辨识性与可计算的组 $\ell_1$ 解码保证需要不同条件。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

黑盒大模型只能通过输入输出接口访问，不能检查内部状态、求梯度或直接再训练，因此可靠性改进通常发生在推理阶段。实际系统可以生成同一问题的释义版本、缩放版本、分解子问题或语义等价代码，并获得一组相互关联的回答；然而系统仍需知道：当其中少量回答错误且观测含噪时，这些关系和有限的可信验证信息是否足以定位错误并恢复正确回答。若缺少这种事前判断，增加采样、关系检查或修复迭代可能只会提高表面一致性，而不能提高真实性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **多样化生成与回答级修正**：通过提示改写、多条推理链采样与投票、自我批评、迭代修订或推理树搜索，为单个问题产生多个候选答案，再依据频率、模型判断或搜索过程选择结果。这类方法主要把可靠性视为候选生成和选择问题。
- **验证器与变形关系检查**：可执行验证器、学习式验证器或人工约束为回答提供外部证据；变形测试则先对输入实施保持任务语义或具有已知输出变换规律的操作，再检查各输出是否满足预定关系。它们实际上共同产生了一组由关系连接、并可能带有可信锚点的回答。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有方法通常评价某个回答、投票规则或修复启发式是否有效，却没有给出与具体算法无关的可恢复性判据。因此，即使增加回答数量或关系边，也无法据此判断所有至多 $k$ 节点错误是否可唯一识别，或噪声会被放大到何种程度。
- 仅检查关系一致性不能认证真实性。若误差方向 $h$ 位于关系算子零空间 $\ker D$ 中，则字段 $z$ 与 $z+h$ 具有相同的关系缺陷；换言之，同一种幻觉可以在所有释义或变换版本中被一致传播。重复的同类关系还可能只增加冗余，无法消除这种不可观测方向。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一个统一且实例相关的理论量，把查询变换形成的类型化关系、外部可信锚点和节点级稀疏错误共同纳入分析，并同时回答三件事：错误是否可识别、恢复对噪声有多敏感，以及困难究竟来自观测设计本身还是某个具体算法。现有的稀疏恢复、图信号和变形测试理论提供了相关工具，但原文主张此前并未将关系—锚点受限裕量明确建立为黑盒大模型回答恢复的基本难度量。

</div>
<div markdown="1"><span>核心问题</span>

给定关系缺陷算子 $D$、锚点算子 $A$，并假设至多有 $k$ 个回答节点被破坏，什么条件能够精确判定任意此类破坏是否都可辨认，并刻画所有估计器在观测噪声下不可避免的最坏恢复误差尺度？

</div>
<div markdown="1"><span>作者直觉</span>

把每个变换后的查询看作一个节点，把“正确回答应如何随变换而变化”写成边约束后，恢复问题就类似于利用一组联立方程寻找被少量节点错误污染的隐藏字段。关系只能看到违反关系的变化，看不到落在 $\ker D$ 中、会让所有回答同步偏移的变化；可信锚点的作用正是观测并固定这些方向。因而关键不在关系或回答的数量，而在组合算子是否能在所有至多 $2k$ 节点支撑的非零差异上产生足够大的可观测信号：两个各含至多 $k$ 个错误的候选字段之差最多涉及 $2k$ 个节点。$\gamma_k(D,A)$ 越大，这些候选越容易区分；若其为零，则至少存在两个不同候选产生完全相同的关系与锚点观测，任何修复算法都无法保证选出真值。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把黑盒大语言模型对同一问题及其变换版本产生的回答，组织成关系响应场（RRF）。每个节点对应一个经过解析的回答向量 $z_i$，有向边通过已知传输算子 $T_e$ 表示释义、缩放、分解或代码重构等变换下回答应满足的关系，外部锚点通过 $Az\approx b$ 注入标签、执行结果、检索证据或验证器等独立信息。给定观测回答 $y$、关系算子 $D$、锚点算子 $A$、关系目标 $q$ 和锚点目标 $b$，方法先构造联合观测矩阵 $B=[D;A]$ 及残差 $s=[Dy-q;Ay-b]$，再估计节点级稀疏错误 $e^{\star}$，最后输出修复场 $\widehat z=y-\widehat e$。其核心不是训练或更新语言模型，而是分析并修复已经采样和解析的黑盒响应。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建响应场

外部解析器 $\phi_i$ 将每个文本映射为有限维实希尔伯特空间中的向量 $z_i=\phi_i(y_i)\in\mathcal H_i$，并把所有节点组成 $z=(z_1,\ldots,z_n)\in\mathcal H=\bigoplus_i\mathcal H_i$。解析器可以提取数值、结构化答案、执行签名或兼容的程序块，但不能访问模型的 logits、梯度、隐藏状态或参数。

<div class="method-step__io" markdown="1">

**输入**：一组经过类型化变换的查询 $x_i$，以及黑盒模型对各查询生成的文本回答 $y_i\sim P_\theta(\cdot\mid x_i)$。<br>
**输出**：解析后的观测场 $y$ 或其向量表示，以及节点分组稀疏结构。

</div>

**直观理解**：先把不同形式的模型回答翻译成可比较的表示。例如，代码回答可以被表示为测试执行签名，数学回答可以被表示为数值或符号结构。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 编码关系与锚点

对每条边计算加权关系缺陷 $(Dz)_e=\sqrt{w_e}(z_j-T_ez_i)$，并将关系算子与锚点算子堆叠为 $B=[D;A]$。在存在关系目标 $q$ 和锚点目标 $b$ 时，构造残差 $s=[Dy-q;Ay-b]$；观测模型为 $s=Be^{\star}+\xi$，其中 $e^{\star}$ 在至多 $k$ 个节点上非零，$\xi$ 表示锚点或其他测量噪声。

<div class="method-step__io" markdown="1">

**输入**：响应节点表示、带类型的边 $e=(i,j,t)$、传输算子 $T_e:\mathcal H_i\to\mathcal H_j$、关系权重 $w_e$，以及外部约束 $Az\approx b$。<br>
**输出**：联合线性逆问题的矩阵 $B$ 与观测残差 $s$。

</div>

**直观理解**：边约束回答之间应该怎样变化，锚点则提供独立的“外部参照”。只依赖边约束可能只能得到彼此一致的错误，因此需要锚点打破这种不可辨识方向。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 评估实例可恢复性

计算关系可观测裕度 $\gamma_k(D,A)$，即所有至多 $2k$ 个节点支撑上的限制矩阵最小奇异值的最小值。若 $\gamma_k>0$，任意至多 $k$ 节点错误在理论上都能被唯一识别；若 $\gamma_k=0$，存在两个不同的稀疏错误产生相同观测，因而无法保证统一恢复。

<div class="method-step__io" markdown="1">

**输入**：联合矩阵 $B$、节点级错误预算 $k$ 和噪声半径 $\epsilon$。<br>
**输出**：实例级恢复证书 $\gamma_k$，以及在噪声下的理论误差尺度 $2\epsilon/\gamma_k$。

</div>

**直观理解**：该裕度衡量最难区分的稀疏错误方向有多明显。裕度越小，两个候选修复越接近、越容易被噪声混淆；它描述的是问题本身的难度，不是某个算法的分数。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 估计稀疏错误并修复

小规模场使用节点支撑枚举求解组稀疏的理想解；连续表示的大规模场使用组范数约束或惩罚的凸松弛，并通过近端梯度进行优化。离散输出则保留模型采样得到的候选答案，经过边传输后直接在候选场上最小化关系能量与锚点能量。

<div class="method-step__io" markdown="1">

**输入**：残差 $s$、矩阵 $B$、错误预算或噪声半径，以及可选的离散候选集合。<br>
**输出**：错误估计 $\widehat e$、修复场 $\widehat z=y-\widehat e$，以及残差 $\|B\widehat e-s\|$ 和实例裕度 $\gamma_k$。

</div>

**直观理解**：系统只修改被判定为异常的回答节点，不改动模型参数。连续优化适合数值向量，离散候选搜索则避免把两个整数或两个程序错误地平均成一个不存在的答案。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 关系可观测裕度

$$
\gamma_{k}(D,A):=\min_{\substack{h\in\mathcal{H}\setminus\{0\}\\\|h\|_{0,\mathrm{g}}\leq 2k}}\frac{\|Bh\|_{2}}{\|h\|_{2}}=\min_{1\leq |S|\leq 2k}\sigma_{\min}(B_{S})
$$

**符号说明**

- $\gamma_k(D,A)$：错误预算为 $k$ 时，关系与锚点联合系统的实例级可观测裕度。
- $D$：由类型化边传输关系构成的关系算子。
- $A$：由外部证据或验证约束构成的锚点算子。
- $B=[D;A]$：把关系约束和锚点约束纵向堆叠得到的联合算子。
- $h$：候选差异方向，即两个可能错误场之差。
- $\|h\|_{0,\mathrm{g}}$：非零节点的数量，而不是非零坐标的数量。
- $S$：包含至多 $2k$ 个节点的支撑集合。
- $\sigma_{\min}(B_S)$：将 $B$ 限制到节点集合 $S$ 后所得矩阵的最小奇异值。

<div class="equation-explanation" markdown="1">

**直观理解**：该式寻找最难被关系和锚点区分的稀疏方向。若结果为正，则任意两个至多 $k$ 节点错误的观测都不同；结果越小，噪声造成的修复误差上限越大。<br>
**原文位置**：第 2 节 Definition 1，式（5）

</div>

</div>

<div class="equation-block" markdown="1">

#### 组稀疏修复目标

$$
\widehat{e}_{1}\in\operatorname*{arg\,min}_{e}\sum_{i\in V}\omega_i\|e_i\|_2\quad\text{s.t.}\quad\|Be-s\|_2\leq\epsilon
$$

**符号说明**

- $\widehat e_1$：凸松弛得到的节点级错误估计。
- $e_i$：第 $i$ 个响应节点的修改向量。
- $\omega_i$：节点级组稀疏惩罚权重。
- $s$：由观测场、关系目标和锚点目标构成的残差向量。
- $\epsilon$：允许的联合观测误差半径。
- $\|e\|_{2,1}$：各节点错误向量二范数之和，用于鼓励只有少数节点被修改。

<div class="equation-explanation" markdown="1">

**直观理解**：目标在两个要求之间权衡：修改的节点尽量少，同时修复误差要与关系和锚点观测一致。它是对直接枚举错误节点的可计算近似，但还需要比 $\gamma_k>0$ 更强的零空间条件才能保证凸算法统一成功。<br>
**原文位置**：第 4 节，式（9）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：该方法没有模型训练目标，也不进行语言模型参数更新。其优化对象是已解析回答场中的错误变量 $e$：小规模问题直接最小化组级非零节点数，大规模连续问题最小化加权组范数并满足 $\|Be-s\|_2\leq\epsilon$，或使用等价的惩罚目标 $\frac{1}{2}\|Be-s\|_2^2+\tau\sum_i\omega_i\|e_i\|_2$；输出的是修复后的响应，而不是新的模型参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 关系响应场表示**

有限有向多重图 $G=(V,E)$ 的节点保存变换查询及其解析表示，边类型决定传输算子 $T_e$，关系权重在同一关系族内归一化。权重采用复制不变的约定：将一个观测复制为 $m$ 份时，每份权重变为 $w/m$，从而避免单纯增加重复查询数量而虚假提高信息量。

> 直观理解：该模块把“不同问题之间应该如何对应”明确写出来，并防止重复抄写同一条证据被错误地当成更多独立证据。

**2. 关系可观测裕度**

$\gamma_k(D,A)$ 在所有至多 $2k$ 个节点支撑上寻找最小的限制最小奇异值；它等价于联合矩阵 $B$ 的组 spark 大于 $2k$。因此 $\gamma_k>0$ 是给定稀疏错误模型下统一精确可辨识的充要条件，而不仅是某个算法的充分条件。

> 直观理解：关系约束和锚点共同决定回答错误能否被唯一定位。关系一致但整体偏移的共享幻觉可能位于 $\ker D$ 中，只有足够有效的锚点才能消除这种盲区。

**3. 稀疏修复解码器**

理想解码器最小化组级非零节点数并限制联合残差；大规模连续场使用 $\sum_i\omega_i\|e_i\|_2$ 的组稀疏凸松弛或其带参数 $\tau$ 的惩罚形式。正的 $\gamma_k$ 保证信息论可恢复性，但凸松弛还需要组鲁棒零空间性质，因此实例可辨识并不自动意味着该近似算法成功。

> 直观理解：算法倾向于只编辑少数节点，同时让修复后的整体回答满足关系和外部证据。理论上能恢复与实际使用的快速优化器能恢复，是两个需要分别检验的问题。

**训练与推理**

完整推理流程为：对变换查询采样黑盒模型回答；用外部解析器得到节点表示；依据任务语义建立有向边、传输算子、关系权重及外部锚点；构造 $B=[D;A]$ 与 $s=[Dy-q;Ay-b]$；根据规模和表示类型选择精确支撑搜索、连续组稀疏凸优化或离散候选场搜索；得到 $\widehat e$ 后返回 $\widehat z=y-\widehat e$，并报告 $\gamma_k$ 与联合残差作为证书。理论上，若 $\gamma_k>0$ 且观测噪声满足 $\|\xi\|_2\leq\epsilon$，任意满足相同稀疏预算和残差约束的估计具有误差界 $\|\widehat e-e^{\star}\|_2\leq 2\epsilon/\gamma_k(D,A)$；但凸松弛的统一保证还要求组鲁棒零空间性质。

**复现信息**

小型响应场可枚举所有至多 $2k$ 节点支撑并计算限制矩阵的最小奇异值，从而精确计算 $\gamma_k$；大规模连续场采用组近端梯度求解凸目标，步长需小于 $\|B\|_{2\to2}^{-2}$，而加速更新分别对应标准的 $O(1/t)$ 与 $O(1/t^2)$ 目标间隙收敛阶。离散任务不能直接对答案取连续平均，因此应为每个节点保留由模型采样提取的有限候选集，在传输后的候选之间联合最小化关系和锚点能量。复现实验时必须明确解析器、节点分组、边类型与传输算子、关系权重归一化方式、锚点构造、错误预算 $k$ 和噪声半径，因为这些因素共同决定实例的 $\gamma_k$。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 合成定理验证场：每个响应场包含 $d=4$ 个有类型的纤维，传输算子按 $T_{ij}=M_jM_i^{-1}$ 构造；实验完全掌握真值 $z^\star$、破坏算子 $B$、错误支持集及 $\gamma_k$。其作用是直接检验理论后果，并通过枚举大小不超过 $2k$ 的全部节点支持精确计算 margin，而非采用谱代理量。
- 自然黑盒模型日志：数学部分含 128 个整数表达式题，使用恒等、缩放和平移变换，以精确答案准确率评价；代码部分含 64 个整数函数任务，使用参数重命名、等价题述和分解提示，并配置 8 个公开测试及 16 个隐藏测试，以隐藏测试 pass@1 评价。每题生成 4 个确定性变换响应，同时记录自一致性与反思调用。该数据用于考察自然条件下的候选生成，但可能包含正确候选缺失、共享错误或多节点错误。
- 真实错误回放场：从自然日志中抽取模型实际产生的错误，将每个合格样本控制为 3 个正确响应节点和 1 个不同的真实错误节点，即严格满足 $k=1$；代码错误还要求错误程序与正确程序的公开执行签名不同。每个样本在 10 种预先规定的关系—锚点设计上重复评估，且响应内容保持不变。该数据把真实错误内容与算子设计分离，用于检验 $\gamma_1(D,A)$ 的跨模型、跨任务预测能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务正确率**

数学使用精确答案准确率，代码使用隐藏测试 pass@1，衡量最终候选是否真正解决原任务。自然日志中的 candidate recall 则表示候选集合是否至少包含正确答案，用来区分“修复器选错”与“根本没有正确候选”。 （越高越好，因为它直接表示正确回答或通过隐藏测试的比例；但 candidate recall 只是可选上限，不等同于部署时能够识别正确候选。）

</div>
<div class="metric-item" markdown="1">

**全场重构误差**

衡量修复后的整个响应场与受控正确场之间的偏差，是错误回放实验的主要恢复指标；它不仅检查单个最终答案，还检查所有变换节点能否被一致地重建。 （越低越好，因为较小误差表示关系与锚点算子能够更稳定地定位并修复受损节点。）

</div>
<div class="metric-item" markdown="1">

**预测关联与判别指标**

Spearman $\rho$ 衡量 $\gamma_1(D,A)$ 对不同算子设计恢复难度的秩排序能力；分组逻辑模型的 held-out AUC 衡量加入 $\gamma_1$ 后对恢复结果的样本外判别能力，置换检验 $p$ 值用于判断这种增益是否可能由组内随机对应造成。 （Spearman $\rho$ 和 AUC 越高越好，说明 $\gamma_1$ 更能预测恢复次序或成功概率；置换检验 $p$ 值越低，说明观察到的对应关系越难由随机排列解释。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 合成场中的一致性—真实性分离

<div class="result-value" markdown="1">

向关系算子的零空间加入共享传输偏移后，关系缺陷仅为 $2.5\times10^{-16}$，但相对真值的误差仍为 $0.877$。

</div>

作者据此主张“关系一致”并不推出“回答真实”：如果所有节点沿着关系算子不可见的同一方向共同偏移，节点之间仍近乎完美一致，关系检查却无法发现共享幻觉。分析上，这验证的是零空间盲区这一受控构造，而不是自然模型共享幻觉的实际发生率，也不能单独证明某种修复算法优于其他算法。

<div class="result-source" markdown="1">

来源：图 1及表 1；具体数值见表 1 的“Consistency ≠ truth”行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A shared transported hallucination has virtually zero defect despite large truth error (left).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 自然数学与代码日志中的候选生成

<div class="result-value" markdown="1">

外部 verifier 在所列各模型—任务组合上达到与 candidate recall 相同的成绩；例如 Qwen2.5-0.5B 的数学结果为 $22.7\%$，代码结果为 $75.0\%$。相比之下，关系多数在该模型上分别为 $18.0\%$ 和 $68.8\%$，说明外部可验证证据在这些日志中能更充分利用已有正确候选。

</div>

这些结果检验实际黑盒输出中不同候选生成或选择机制的表现，并显示主要瓶颈常常是候选集合是否含有正确答案。作者没有把它解释为公平的算法排行榜，因为各方法查询预算不相等，而且自然场可能违反 $k=1$ 假设；因此该表不能直接证明 verifier 在等计算量下普遍更优，也不能用自然场中的失败反驳或支持 $\gamma_k$ 理论。

<div class="result-source" markdown="1">

来源：表 2及第 5.2 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Methods have disclosed but unequal query budgets, so this table characterizes candidate generation rather than a compute-matched leaderboard.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨模型、跨任务的真实错误回放

<div class="result-value" markdown="1">

合并 3660 个回放场后，$\gamma_1(D,A)$ 与恢复表现的秩关联为 $0.449$，cluster-bootstrap 的 $95\%$ 区间为 $[0.417,0.481]$；在控制检查点、任务、原始错误、关系数和锚点数后，加入标准化 $\gamma_1$ 使 held-out AUC 提升 $0.033$，其逻辑模型系数为 $3.653$，2000 次题内置换检验得到 $p=0.00050$。

</div>

作者据此认为，同一个修复前算子量能够在两类任务、多个检查点和不同响应空间中按预期排序恢复难度；正系数和样本外 AUC 增益还表明该信息不能完全由关系数量、锚点数量或模型身份解释。分析上，这提供的是跨分层的中等强度预测证据，而非普适定律：回放场由正确性标签构造且严格限定为单节点错误，不能直接充当部署时的答案选择器。

<div class="result-source" markdown="1">

来源：第 5.3 节；表 3与图 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Pooled rank association is 0.449 with cluster-bootstrap 95% interval [0.417,0.481]. A grouped logistic model controls for checkpoint, task, raw error, relation count, and anchor count; adding standardized γ1 improves held-out AUC by 0.033 and has coefficient 3.653. A 2,000-draw within-item permutation test gives p=0.00050.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 真实错误回放依赖正确性标签来挑选 3 个正确节点和 1 个错误节点，因此是评估用压力测试，不是可部署的无标签选择方法；它也排除了多节点错误、共享幻觉、解析器碰撞和正确候选缺失等自然失败类型。
- 跨模型、跨任务证据仅覆盖两个模型家族及数学、代码两个领域，不能推出适用于所有大语言模型和任务的普遍缩放规律；自然日志中的方法查询预算又不相等，表 2不能支持计算量匹配的优劣结论。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Raw：直接使用原始模型回答，不进行额外聚合或修复；它给出模型自身能力与后处理收益的参照点。
- Self-consistency：利用重复采样结果进行自一致性选择，是黑盒推理中常见的投票式基线，用于比较关系约束是否比仅依赖答案频率更有效。
- Relational majority：依据变换后回答之间的关系一致性进行多数选择，直接代表“仅靠一致性”的关系式方法，可检验一致性是否足以保证真实。
- Reflect 与 Verifier：Reflect 让模型根据反思日志修订答案，代表迭代自我修正；Verifier 使用独立验证证据选择候选，代表带可信锚点的方案。二者分别检验语言模型自审与外部可验证信号的价值。

**实验想回答的问题**

- 理论定义的恢复难度 $\gamma_k(D,A)$ 是否准确刻画关系响应场在至多 $k$ 个节点受损时的可识别性与修复难度，包括“一致但不真实”、锚点引发的可恢复性相变以及重复关系的收益饱和？
- 在模型、任务和响应空间发生变化后，修复前计算的 $\gamma_1(D,A)$ 是否仍能预测真实模型错误的恢复结果，而不只是拟合 Sparse-RRF 这一特定算法的事后分数？

**实验实现**

实验分成三层：先在合成场中精确验证理论预言，再在自然模型日志上比较候选生成方法，最后把真实错误放入严格受控的 $k=1$ 回放场中做因果更清晰的算子干预。自然实验只使用解析后的输出，不访问 logits 或模型内部状态；所列检查点包括 Qwen2.5-0.5B-Instruct、Phi-3-mini-4k-instruct、Qwen2.5-7B 和 Qwen2.5-14B。回放实验对同一题目的响应固定不变，仅切换 10 种关系—锚点设计，并将同一题目的全部设计置于同一推断组；另以 3 个关系数和锚点数匹配的 triangle/isolate 设计区分“约束数量”与“实际可观测性”。作者明确指出自然日志各方法查询预算不相等，因此表 2 是候选生成特征比较，不是计算量匹配的排行榜。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 锚点相变：对 6 个双节点连通分量加入锚点 | 加入这些锚点后，$\gamma_1$ 从 $0$ 上升至 $0.524$，并从此开始精确恢复。 | 该干预隔离了可信外部证据对可识别性的作用：锚点并非仅让误差逐渐变小，而是在消除最后一个允许的稀疏零方向时触发从不可识别到可恢复的相变。由于这是合成场中的受控结果，它验证理论机制，但不说明自然任务需要固定数量的 6 个锚点。 | 图 1及表 1；具体数值见表 1 的“Anchor transition”行<br><span class="experiment-evidence">Recovery changes when anchors remove the final admissible sparse null direction (right).</span> |
| 重复饱和：把每条关系原样重复 $1$ 至 $16$ 次 | 虽然关系副本数增加到原来的 $16$ 倍，归一化 $\gamma_2$ 始终保持 $0.309$。 | 该消融隔离了“约束的独立信息”与“观测次数”两个因素。完全相同的关系副本不会改变归一化 Gram 算子，因此不会改善确定性的可识别性；独立重复调用仍可能通过平均降低随机噪声，但那属于方差缩减，不能视为新增结构信息。 | 第 5.1 节及表 1 的“Duplicate saturation”行<br><span class="experiment-evidence">Duplicate saturation distinguishes deterministic information from variance reduction: independent repeated calls may reduce observation noise, but literal copies do not alter the normalized Gram operator.</span> |

**定性案例**

- 图 1左侧的共享传输幻觉是关键反例：所有变换节点共同沿关系零空间偏移，因而节点间缺陷近乎为零，但整体远离真值。它直观说明，仅观察答案之间“互相说得通”无法排除它们以同一种方式共同出错；需要独立锚点或其他能覆盖该零方向的证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops a theory and repair algorithms for recovering reliable math and code answers from relational consistency and trusted anchors, including shared-hallucination failure modes.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`f08f377005b4a386e5f13fff523a95c025cab6f3d6ab5b4e7a81461d91e8802f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
