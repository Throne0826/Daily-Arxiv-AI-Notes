---
title: "[论文解读] Language-encoded network topology enables large language models to reason about complex networks"
description: "[arXiv 2609.03229][LLM Reasoning] BioGlyph将图算法提取的枢纽、割点、桥和跨社区连接者等拓扑角色转写为可解释的自然语言，使冻结的大语言模型无需从原始连接中自行重建复杂结构，也能回答网络连通性、重要性与扰动后果问题。"
arxiv_id: "2609.03229"
announcement_date: "2026-09-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:40:03.510795+00:00"
source_sha256: "a36bce9443f984ba464b04c900e6f8174ce048919817140ad7380eab0bf475d0"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "复杂网络"
  - "大语言模型"
  - "图结构推理"
  - "网络拓扑"
  - "结构角色"
  - "社群结构"
  - "扰动分析"
  - "可解释表示"
  - "BioGlyph"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.03229</p>

# Language-encoded network topology enables large language models to reason about complex networks

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Ucchwas Talukder Utsha, Sakib Mostafa, James Zou, Md Tauhidul Islam</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Department of Radiation Oncology, Stanford University, Stanford, California, USA；Affiliation: Department of Electrical Engineering, Stanford University, Stanford, California, USA；Affiliation: Department of Biomedical Data Science, Stanford University School of Medicine, Stanford, California, USA；Affiliation: Department of Computer Science, Stanford University, Stanford, California, USA</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03229v1) · [PDF 下载](https://arxiv.org/pdf/2609.03229v1) · **关键词** 复杂网络, 大语言模型, 图结构推理, 网络拓扑, 结构角色, 社群结构, 扰动分析, 可解释表示, BioGlyph<br>


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

BioGlyph将图算法提取的枢纽、割点、桥和跨社区连接者等拓扑角色转写为可解释的自然语言，使冻结的大语言模型无需从原始连接中自行重建复杂结构，也能回答网络连通性、重要性与扰动后果问题。

**不用术语来说**：许多生物与工程问题不只关心“谁与谁相连”，还关心某个节点为何重要、删除一条连接是否会使系统断裂，以及哪个组成部分维系着不同区域。边列表虽然完整记录了连接，却没有直接说明这些连接的整体含义；大语言模型因而需要先在文本中还原网络结构，再进行推理，容易在复杂或密集网络上出错。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出BioGlyph：利用经典网络分析算法和固定规则，将仅由拓扑确定的结构属性编译成统一、可读的角色描述；每项描述同时给出角色、支持该判断的结构证据，并在适用时说明删除节点或边的后果。
- 确立一种“改变网络信息的表达、而非修改网络或语言模型”的研究路线，并检验所得角色词汇是否既能支持大语言模型的结构推理，又能揭示酵母蛋白互作网络中与基因必需性相关的生物组织。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于网络科学与大语言模型推理的交叉领域。复杂系统可抽象为图 $G=(V,E)$：节点表示蛋白质、基因、用户或基础设施组件，边表示相互作用或连接；研究重点不仅是查询某条边是否存在，还包括识别枢纽、跨社群连接者、割点和桥，以及判断删除节点或边后连通性如何变化。经典图算法可以精确计算这些结构性质，但大语言模型面对边列表、连接关系句子或数值测量表时，必须先从文本中重建拓扑，因而容易在连通性与扰动问题上出错；BioGlyph所处的问题背景正是如何把算法得到的网络结构转换为模型和研究者都能直接理解的语言表示。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**图与连通性**

图由节点集合 $V$ 和边集合 $E$ 构成；若两个节点之间存在一条由若干边组成的路径，则它们相互可达。删除节点或边后检查可达关系是否改变，是本文扰动推理任务的基础。

</div>
<div class="concept-item" markdown="1">

**社群结构**

社群是图中内部连接较密、与外部连接相对较少的一组节点。位于社群核心的节点维持局部组织，而跨社群连接者负责连接不同功能区域。

</div>
<div class="concept-item" markdown="1">

**结构角色**

结构角色是根据节点或边在整体拓扑中的位置赋予的可解释类别，例如枢纽、割点、桥、社群核心和跨社群连接者。角色关注连接所产生的系统意义，而不只记录节点度数或一串难以解释的向量。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个仅包含拓扑信息的网络 $G=(V,E)$，不依赖节点标签、生物学注释或任务专用训练；同一个冻结的大语言模型需要回答网络连通性、组件重要性以及删除某个节点或边后的结构后果等问题。传统输入形式包括边列表、自然语言连接描述、网络测量值或学习得到的数值表示；本文背景下的目标输出则是能够支撑正确答案的、人类可读的结构信息，例如某节点是否为枢纽或割点、连接了哪些社群，以及删除后是否会使网络分裂。核心比较条件是保持原始网络和语言模型不变，只改变网络信息提供给模型的表示方式。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$G=(V,E)$**

网络或图，其中 $V$ 是节点集合，$E$ 是节点之间的边集合。

</div>
<div class="notation-item" markdown="1">

**$V$**

系统中的元素集合，例如蛋白质、基因、用户或基础设施组件。

</div>
<div class="notation-item" markdown="1">

**$E$**

元素之间的关系集合，例如蛋白质相互作用或社会连接。

</div>
<div class="notation-item" markdown="1">

**$G\setminus x$**

从图 $G$ 中删除节点或边 $x$ 后得到的扰动网络，用于分析删除操作对连通性和网络分裂的影响。

</div>

</div>

**直接相关的工作**

- **Girvan and Newman (2002), Community structure in social and biological networks**: 为识别网络社群及其跨区域连接关系提供经典网络科学背景；BioGlyph需要利用图划分结果区分社群核心和跨社群连接者，再把这些算法结构翻译成语言。
- **Chen et al. (2024), LLaGA: Large Language and Graph Assistant**: 代表将学习得到的图表示提供给语言模型的路线。论文指出这类数值表示能够编码复杂模式，但通常难以直接说明节点为何重要、连接了哪些区域，以及删除后会发生什么；BioGlyph转而使用固定规则生成可解释的结构角色描述。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

蛋白互作、基因调控、脑连接、交通和电网等系统的功能与脆弱性取决于全局连接方式。实际分析常需判断某个蛋白是否连接两个生物过程、某个节点失效后其他节点是否仍可到达，或哪条边被删除时破坏最大；单独罗列局部交互无法直接回答这些涉及全局位置和扰动后果的问题。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **连接显式编码**：把网络表示为边列表、结构化数据，或逐句描述节点之间的连接，再把这些原始连接提供给大语言模型，由模型在回答问题时自行推断社区、桥、割点及删除后的连通性。
- **学习式数值表示**：通过图表示学习把节点或局部网络压缩为数值向量，再将向量接入语言模型，以隐式承载复杂拓扑模式，而不是明确陈述节点承担的结构角色。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 显式连接表示虽然保留原网络，但没有预先提炼结构含义；语言模型必须先从大量局部连接恢复全局拓扑，再完成任务推理，因此即使标准图算法可以精确求解，也可能在桥接关系、断连效应和重要性判断上出错，密集且社区交织的网络尤其困难。
- 学习式数值表示能够捕获复杂模式，却难以向研究者说明某个节点为何重要、连接了哪些网络区域，以及删除后可能产生什么后果；这种不可解释性限制了表示在需要科学证据和机制说明的生物医学推理中的用途。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法在“保留原始连接但让模型承担结构解析”与“压缩拓扑但牺牲可解释性”之间存在缺口：尚缺少一种不依赖节点标签、生物注释或任务专门训练，且无需改动大语言模型，就能把经典图分析得到的全局结构知识直接表达为模型与研究者共同可读语言的通用表示。

</div>
<div markdown="1"><span>核心问题</span>

网络拓扑能否被确定性地翻译成带有结构证据和扰动含义的自然语言角色，从而在网络与大语言模型均保持不变的条件下，提高模型对连通性、结构重要性和节点或边删除后果的推理能力，并保留可供科学解释的意义？

</div>
<div markdown="1"><span>作者直觉</span>

大语言模型擅长处理语义明确的文字，却不擅长在长连接清单中稳定执行隐含的图算法。若先由可靠的网络分析程序计算“这是枢纽”“它连接两个社区”“删除它会把网络分开”等事实，再用固定词汇把结果写成带证据的描述，模型便可直接围绕这些结构结论进行语言推理。通俗地说，BioGlyph不是让模型自己从线路表中寻找关键枢纽，而是先生成一份可核查的“网络角色说明书”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

BioGlyph 是一个无需训练、也不修改图或语言模型的确定性“图结构编译器”。对每个问题，它先围绕题目点名的节点检索局部子图，再计算连通性、中心性、社区结构和核分解等经典图信号；随后用固定规则把这些数值或拓扑性质映射为 11 类可读角色，例如枢纽、割点、桥、跨社区连接者和社区核心。每条角色描述同时包含触发该角色的证据及其结构后果，最终与题目和统一的全图目标节点事实一起输入冻结的语言模型，由精确图算法而非另一个语言模型提供标准答案。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 按问题检索局部网络区域

基础设置从目标节点扩展两层广度优先搜索，并将区域限制为 120 个节点；较大设置允许 300 个节点，并按问题类型选择两层邻域或与反事实可达性有关的路径。目标节点优先保留；部分问题还可进行至多两轮补充扩展，以尽量纳入完整目标邻域或删除指定节点后仍存在的连接路径。

<div class="method-step__io" markdown="1">

**输入**：完整网络 $G=(V,E)$、问题中出现的一个或多个目标节点，以及检索节点上限。<br>
**输出**：包含目标节点及其相关局部结构的检索子图；若目标标识符在完整网络中不存在，则在调用语言模型前直接标记为不可回答。

</div>

**直观理解**：这一步类似先从一张过大的地图中裁出与问题相关的街区，避免把整个网络塞入上下文。所有表示方法使用同一块裁剪区域，因此比较的是“怎样描述图”，而不是“看到了哪部分图”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 计算结构信号与社区划分

在 $\widetilde{G}$ 上计算连通分量、割点、桥、$k$-core 核数及 Leiden 社区；在 $G$ 上计算度、PageRank、节点介数和边介数，并进一步得到参与系数 $P(v)$ 与社区内度 $k^{\mathrm{int}}(v)$。实验网络按无向图处理，因此其中 $G=\widetilde{G}$。

<div class="method-step__io" markdown="1">

**输入**：检索得到的区域图 $G$，以及去除自环并忽略方向后得到的简单无向视图 $\widetilde{G}$。<br>
**输出**：统一的结构信号记录，包括节点、边和社区层面的拓扑测量，以及介数采用精确计算还是采样估计的标记。

</div>

**直观理解**：这些信号分别回答“连接是否很多”“是否卡在许多最短路径上”“邻居是否跨越多个群体”以及“移除后会不会断开”等问题。BioGlyph 不要求语言模型自行从边表中推导这些性质，而是先由可靠的图算法算出它们。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 将结构信号编译为语义角色

编译器在节点、边和社区三个层级分配 11 类角色：割点与桥由精确连通性分解直接确定；枢纽、权威节点、瓶颈边、跨社区连接者、边界节点和社区核心依据区域内或社区内的均值加若干标准差触发；孤立点、外围节点和脆弱社区使用固定结构条件。每个已分配角色附带触发测量和简短结构后果，并按层级、角色名及目标排序。

<div class="method-step__io" markdown="1">

**输入**：结构信号记录、固定角色阈值 $\{\sigma_X\}$ 和确定性的社区划分。<br>
**输出**：结构角色集合 $\mathcal{G}$，可渲染为仅角色名、角色名加证据，或包含证据与结构后果的完整 BioGlyph 描述。

</div>

**直观理解**：这相当于把难读的数字翻译成稳定的结构词汇，例如把“介数异常高且连接多个社区”写成“跨社区连接者”。规则固定且可检查，因此角色不是语言模型凭感觉生成的标签。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 构造提示并由冻结语言模型作答

系统将网络区域描述、共享事实块和问题拼接成提示，要求模型推理并以 `ANSWER: <answer>` 结束；同一检索区域也可分别渲染为无图、边表、邻接句子、原始测量表或学习角色，以形成受控比较。Qwen3-8B 与 Llama-3.1-8B-Instruct 均保持冻结，输出由确定性规则解析，并与完整网络上的精确图算法答案做精确匹配。

<div class="method-step__io" markdown="1">

**输入**：渲染后的 BioGlyph 描述、问题文本，以及所有表示共享的目标节点存在性和全图度数事实。<br>
**输出**：问题的可解析最终答案及其正确性；超出提示预算、无法解析或与图算法答案不符均计为错误。

</div>

**直观理解**：BioGlyph 本身负责把图变成语言，语言模型只负责阅读这些结构说明并回答问题。由于标准答案由图算法计算，评测不会出现“一个模型给另一个模型打分”的循环。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 参与系数

$$
P(v)=1-\sum_{m\in\mathcal{M}}\left(\frac{k_{v,m}}{d(v)}\right)^2,\qquad k_{v,m}=\left|\left\{u\in N(v):C(u)=m\right\}\right|
$$

**符号说明**

- $v$：待描述的节点。
- $\mathcal{M}$：Leiden 算法得到的社区集合。
- $N(v)$：节点 $v$ 的邻居集合。
- $C(u)$：节点 $u$ 所属的社区。
- $k_{v,m}$：节点 $v$ 在社区 $m$ 中拥有的邻居数。
- $d(v)$：节点 $v$ 的度，即邻居总数。
- $P(v)$：节点 $v$ 的参与系数；当 $d(v)=0$ 时按定义设为 0。

<div class="equation-explanation" markdown="1">

**直观理解**：该式衡量一个节点的邻居是否分散在多个社区：若邻居几乎都属于同一社区，平方占比之和接近 1，故 $P(v)$ 接近 0；若邻居较均匀地分布在多个社区，$P(v)$ 会更大。BioGlyph 用它识别社区边界节点，而不是仅凭总连接数判断节点是否跨群体。<br>
**原文位置**：Methods，Structural signals，公式 (1)–(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 异常结构值的角色触发规则

$$
X(u)>\mu_X+\sigma_X s_X
$$

**符号说明**

- $u$：接受判断的节点、边或其他结构元素。
- $X(u)$：元素 $u$ 在结构量 $X$ 上的取值，例如度、介数、PageRank、参与系数或社区内度。
- $\mu_X$：相关比较集合中结构量 $X$ 的均值。
- $s_X$：相关比较集合中结构量 $X$ 的标准差。
- $\sigma_X$：针对具体角色预先固定的标准差倍数。

<div class="equation-explanation" markdown="1">

**直观理解**：元素只有在某项结构量显著高于其比较群体时才获得相应角色；若 $s_X=0$，该阈值角色不分配。除社区核心在各社区内部比较外，默认比较分布来自当前检索区域，因此角色表达的是该问题区域中的相对异常，而不一定是全图中的绝对异常。<br>
**原文位置**：Methods，The BioGlyph compiler，公式 (4)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：BioGlyph 主方法没有可学习参数，也没有训练目标：角色阈值、连通性条件和文字模板均预先固定，语言模型在推理时保持冻结。只有对照方法“学习角色”需要训练：它使用 Deep Graph Infomax，让真实节点嵌入与全图摘要相互匹配、让经特征行置换得到的损坏嵌入与摘要不匹配；训练后的嵌入再以 $K=8$ 的 $k$-means++ 聚类成离散角色。该目标仅用于构造 R4 基线，不参与 BioGlyph 的角色生成，也不使用 benchmark 的任务标签。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 三层结构角色编译器**

编译器包含 8 个节点角色、2 个边角色和 1 个社区角色。`CUT_NODE` 与 `BRIDGE_EDGE` 分别对应割点和桥；`HUB`、`AUTHORITY`、`BOTTLENECK_LINK`、`CROSS_COMMUNITY_CONNECTOR`、`BOUNDARY_NODE`、`COMMUNITY_CORE` 使用异常高值规则，其中标准差倍数依次为 2.0、2.0、2.0、2.0、1.5、1.0；`ISOLATE`、`PERIPHERAL` 和 `FRAGILE_REGION` 则分别依据单节点分量、核数 $c(v)\leq 1$、社区边连通度 $\lambda\leq 1$ 判定。`AUTHORITY` 仅为有向网络定义，本文报告的无向实验不使用它；社区核心只在至少含 3 个节点的社区内比较，脆弱社区只对规模为 3 至 1,500 的社区计算。

> 直观理解：单个数值往往不能直接告诉模型其结构含义，角色编译器把测量组合成可解释判断。例如高介数并不自动意味着跨社区连接者，还必须确实接触至少两个社区，从而让标签更贴近其语义。

**2. 证据化与闭世界渲染**

完整渲染为每个角色输出角色名称、触发它的测量和对应的结构后果，并明确声明区域中的全部割点与桥均已列出。因此，区域内某节点若没有 `CUT_NODE` 条目，可以反向推断它不是该区域的割点；同时渲染会声明区域内所有节点，包括未获得任何角色的节点。论文还设计了将语义名称替换为无意义 token 的 opaque 控制，以及逐步加入证据和结构后果的多种渲染，以区分角色划分本身与可解释词义的作用。

> 直观理解：只列出“重要节点”通常会产生歧义：没有出现究竟表示“不重要”，还是“系统漏写”？闭世界声明消除了这种歧义，而证据和后果则告诉模型标签为何成立、能支持什么推论。

**3. 检索充分性与双重精确预言机**

完整网络预言机计算用于评分的真实答案，区域预言机在检索子图上计算同一问题；仅当两者答案一致时，区域才被称为充分。反事实可达性的自适应停止条件直接检查删除节点后的连通谓词，因而使用了特权信息；作者另设基于个性化 PageRank、且不运行该循环的无预言机检索对照，以区分表示能力和检索辅助带来的影响。

> 直观理解：局部区域可能天然缺少答题所需的边，所以答错不一定是语言模型推理失败。两个预言机分别判断“全图正确答案是什么”和“裁出的区域是否足以得到该答案”，从而把检索失败与表示、推理失败区分开。

**训练与推理**

推理前，系统以固定随机种子完成社区划分及必要的近似计算；对每道题独立检索区域并生成同一份结构信号记录。R5 将记录编译为 BioGlyph，R3 则直接打印其中的数值，以保证两者接触相同底层信息；R0–R4 分别提供无图、边表、自然语言邻接句、原始测量和无监督学习角色。随后将选定表示、统一的目标事实块与问题输入冻结的 Qwen3-8B 或 Llama-3.1-8B-Instruct，解析最终 `ANSWER:` 后的内容，并使用完整网络上的精确图算法进行精确匹配评分。

作为 R4 基线，GCN、GraphSAGE、GAT 或 GIN 在完整网络上运行两层消息传递，使用 11 维节点特征生成 32 维嵌入；经 200 个 epoch 的无监督训练后，将节点分到 8 个聚类，并在检索区域中显示其全图聚类角色。BioGlyph 与该基线的关键区别不是是否拥有图统计量，而是 BioGlyph 显式计算割点、桥、社区和移除后连通性等任务相关结构，再以有语义且可验证的固定角色表达它们。

**复现信息**

图量由 NetworkX 计算，节点与边介数使用 Brandes 算法：当节点数 $n\leq 5{,}000$ 时精确计算，更大图使用固定种子 0 选择的 1,000 个枢轴估计；$k$-core 使用标准核分解。社区划分采用以模块度为目标的 Leiden 算法和种子 0，社区按规模递减重编号，并以最小节点标识符打破平局；检索也按距离和节点标识符确定性排序，从而提高复现性。

两个语言模型均以 40,960 token 上下文运行；主 benchmark 为生成预留 16,384 token，因此提示预算为 24,576 token，超预算提示不发送且计为错误。Qwen3-8B 使用 thinking 模式和温度 0.6，Llama-3.1-8B-Instruct 使用贪心解码；所有随机步骤使用种子 0。R4 学习角色基线使用两层、隐藏宽度 64、输出维度 32 的消息传递网络和 PReLU，以 Adam、学习率 0.01 训练 200 个 epoch，再进行带种子的 $k$-means++ 聚类。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- STRING-Yeast：包含 3,384 个蛋白质和 43,030 条物理相互作用；使用 156 道问题评估蛋白质网络推理，并用独立的 SGD 基因必需性注释检验结构角色的生物学关联。原文没有给出传统意义上的训练集、验证集和测试集划分；实验使用检索到的局部网络区域及其问题进行评测。
- ChCh-Miner：BioSNAP 药物相互作用网络，包含 1,514 种药物和 48,514 条相互作用，平均度约为 64，是基准中最稠密的网络；使用 156 道问题评估稠密网络上的结构推理。原文未明确报告数据集划分。
- Reactome：功能相互作用网络，包含 10,022 个蛋白质和 194,494 条相互作用；一项分析筛选最大连通分量中的割点及其删除后导致的分离规模，另一项用 60 个模块、共 120 次回答评估模型估计删除影响的能力，并以 DepMap 24Q4 依赖性注释作外部关联验证。原文未明确报告训练、验证和测试划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**system accuracy**

模型回答与精确图算法输出一致的题目比例；还包括网络中不存在目标节点时正确声明无法回答的情形。 （越高越好，因为它直接衡量结构问题的最终答对率。）

</div>
<div class="metric-item" markdown="1">

**95% bootstrap confidence interval**

对系统准确率进行自助法重采样得到的不确定性区间，用于表示估计结果的统计波动。 （区间本身不是越高越好；比较方法时应同时看准确率差异及区间宽度和重叠情况。）

</div>
<div class="metric-item" markdown="1">

**median absolute error**

模型估计删除节点后分离蛋白质数量时，预测值与精确数量之差的绝对值的中位数。 （越低越好，因为它表示典型回答离精确图算法结果更近。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### STRING-Yeast 上的总体结构推理

<div class="result-value" markdown="1">

在两个冻结模型合并后，BioGlyph 准确率为 75.6%，高于无网络信息的 47.3%；边列表、句子、原始图测量表和 GraphSAGE 角色分别为 40.1%、37.5%、36.1% 和 49.2%。在双方均未超出上下文窗口的配对子集上，BioGlyph 仍分别以 79.5% 对 73.7%、74.6% 对 57.8%、75.0% 对 53.1% 和 78.1% 对 47.1% 优于原始测量表、句子、边列表和 GraphSAGE。

</div>

这说明优势不只是因为其他表示过长而被截断：即使比较双方都完整可读的问题，BioGlyph 仍更能把局部连接组织成可用于推理的结构概念。结果支持其对该基准的表示优势，但不能单独证明它在所有模型、网络规模或未覆盖的问题类型上都同样有效。

<div class="result-source" markdown="1">

来源：Results；Figure 3a–b

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across both models, BioGlyph yielded an accuracy of 75.6% on the yeast benchmark (95% confidence interval (CI), 72.3–78.9%), compared with 47.3% without network information (Fig. 3a).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### ChCh-Miner 稠密药物网络上的结构推理

<div class="result-value" markdown="1">

在平均度约为 64 的稠密药物网络上，BioGlyph 准确率为 77.7%，高于无网络信息的 50.8%、GraphSAGE 的 51.4%、边列表的 41.7%、句子的 38.3% 和原始测量表的 25.3%。在双方都能完整输入的配对子集上，BioGlyph 对原始测量表、句子、边列表和 GraphSAGE 的准确率分别为 72.4% 对 59.2%、75.9% 对 60.5%、72.8% 对 55.0% 和 79.4% 对 49.7%。

</div>

该结果检验了 BioGlyph 在高连接密度、潜在提示很长的网络中是否仍然有效。总体结果包含上下文窗口因素，但配对子集仍保持优势，因此作者的解释是：结构角色的语义压缩和明确后果有助于推理，而不仅是减少输入长度。它并未说明所有稠密网络都具有相同幅度的提升。

<div class="result-source" markdown="1">

来源：Results；Figure 4a–b

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across both models, BioGlyph achieved 77.7% system accuracy (95% confidence interval (CI), 74.5–80.9%; Fig. 4a), compared with 50.8% without network information.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Reactome 删除扰动推理与外部生物学验证

<div class="result-value" markdown="1">

在 60 个 Reactome 模块的 120 次回答中，BioGlyph 对“删除某蛋白质后会分离多少蛋白质”的估计准确率为 42.5%，中位绝对误差为 1；句子、边列表和原始测量表的准确率分别为 24.2%、11.7% 和 1.7%，中位误差分别为 7、13 和 27。结构角色还与独立功能有关：STRING-Yeast 中跨社区连接者的必需基因比例为 57.6%，而外围蛋白质为 12.9%，网络总体为 30.9%。

</div>

Reactome 结果表明 BioGlyph 不仅帮助模型回答分类式结构问题，也能近似估计节点删除造成的连通性损失；其定性结构判断的正确率也高于其他表示。Yeast 的必需性关联则是外部有效性证据，说明纯拓扑角色可能对应生物功能，但这是相关关系，不是证明跨社区连接者导致基因必需，也不代表每个连接者都必需。

<div class="result-source" markdown="1">

来源：Results；Figure 5d

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across 120 responses, BioGlyph yielded 42.5% accuracy and a median absolute error of one protein.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验摘录没有报告训练、验证和测试划分，也未完整提供 Section S1 中其他网络、模型家族和控制实验的结果；因此对跨模型、跨领域泛化能力的判断受到信息范围限制。
- 主要准确率受 24,576-token 上下文窗口影响，部分边列表、句子和原始测量提示无法输入模型；虽然作者用完整可读问题的配对分析进行控制，但这不能完全分离表示质量、提示长度与信息内容差异。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 无网络信息（R0）：不向模型提供图结构，用来测量模型仅凭问题和名称所能达到的背景准确率。
- 边列表（R1）与句子化边列表（R2）：分别直接列出连接关系或将边改写为自然语言，用来检验模型能否从低层邻接事实自行恢复全局结构。
- 原始图测量表（R3）：提供节点的数值图测量值，用来检验显式数值信息是否足以支持结构推理，同时反映长提示和数值语义不直观的影响。
- GraphSAGE 学习型角色（R4）：用图神经网络学习节点表示或角色，再转写给语言模型；它是论文所比较的四种图编码器中表现最强者，用来检验固定、可解释的 BioGlyph 角色是否优于学习型结构编码。

**实验想回答的问题**

- 在网络以自然语言可读的结构角色形式呈现时，冻结的大语言模型能否比使用无网络信息、边列表、句子、原始图测量值或学习型结构表示更准确地回答节点重要性、连通性与删除扰动问题？
- BioGlyph 表示中的角色名称、支持性图测量和结构后果分别贡献多少；其识别出的跨社区连接者或割点是否与独立的生物学功能和依赖性指标相关？

**实验实现**

每个问题先检索以指定节点为中心的网络区域，再分别用 BioGlyph、R0、R1、R2、R3 和 R4 表示；所有表示输入相同的两个冻结模型 Qwen3-8B 与 Llama-3.1-8B。模型不更新参数，结果跨两个模型汇总。答案由精确图算法输出评分，而不是由另一个语言模型判分。BioGlyph 将图划分与结构测量结合，为每个节点生成结构角色、支持该角色的证据及其语义后果；在所报告的主要实验中，所有 BioGlyph 描述均适配 24,576-token 上下文窗口。为区分表示能力与提示截断，作者另行只比较两种表示都能完整输入且都产生回答的问题。Reactome 的删除影响实验直接逐一移除节点并计算从最大剩余连通分量分离的蛋白质数；生物学关联分析使用未提供给 BioGlyph 编译器和语言模型的 SGD 或 DepMap 注释。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| STRING-Yeast：逐步移除 BioGlyph 描述成分 | 在所有消融版本都可读的问题共同子集上，仅保留角色名称的准确率为 69.9%；加入支持性图测量后为 68.8%；进一步加入每种角色的结构后果后升至 82.7%。 | 该消融区分了三类信息的作用。单独角色名称已经提供有用的结构先验，数值证据在此设置下没有带来增益，甚至略降；明确说明“该角色被移除后会造成什么结构影响”带来最大提升，说明模型更容易使用已经翻译成语言后果的结构信息，而不是自行从数字重建后果。 | Results；Figure 3c<br><span class="experiment-evidence">Adding the graph measurements supporting each assignment yielded 68.8%, whereas additionally stating the structural consequence of each role increased accuracy to 82.7%.</span> |
| ChCh-Miner：将语义角色名称替换为无意义标记 | 保持角色分配及其他提示内容不变，仅把角色名称替换为无意义 token 后，总体准确率从 66.8% 降至 55.1%。 | 这一控制实验隔离了角色词汇的语义可解释性：模型看到的结构分配并未改变，改变的是名称是否携带“枢纽”“跨社区连接者”等可理解含义。因此下降支持作者关于语义词汇本身参与推理的主张，但由于这是提示替换实验，仍不能完全排除词形、标记分布或语言先验等非语义因素。 | Results；Figure 4c<br><span class="experiment-evidence">This substitution reduced overall system accuracy from 66.8% to 55.1%.</span> |

**定性案例**

- 在 STRING-Yeast 一个包含 120 个蛋白质和 781 条连接的区域中，BioGlyph 描述只提供一次，Qwen3-8B 随后进行多轮推理：模型判断移除 ACT1 会造成最大破坏，并依据其移除后留下八个连通分量的后果识别 ACT1 为跨社区连接者；面对“CBF5 更具破坏性”的反驳时仍保持原答案。该例说明 BioGlyph 可支持跨轮次复用同一结构描述、同时结合角色与明确后果进行一致推理；ACT1 的必需性来自独立 SGD 标注，模型本身并未看到该标注。原文证据为：“Qwen3-8B identified ACT1 as the protein whose removal would cause the greatest disruption, citing the stated consequence that its removal leaves eight connected components.”（Figure 2）

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces a language-based graph representation specifically designed to improve LLM structural reasoning over complex networks.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`a36bce9443f984ba464b04c900e6f8174ce048919817140ad7380eab0bf475d0`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
