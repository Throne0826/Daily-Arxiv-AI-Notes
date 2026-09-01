---
title: "[论文解读] Graph Evidence Is Not Enough: Diagnosing Native Decoder Use in Graph-Augmented LLMs"
description: "[arXiv 2608.30437][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.30437"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:51:47.797255+00:00"
source_sha256: "787e5a89d8fe52d7cd6b1b45cbacb8490868a2cdbd28e4f605add8dc8fbefe77"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "图增强大语言模型"
  - "图检索增强生成"
  - "最短跳数问答"
  - "图到解码器接口"
  - "原生解码器可用性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.30437</p>

# Graph Evidence Is Not Enough: Diagnosing Native Decoder Use in Graph-Augmented LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Xiaoyu Guo, Pengcheng Chen, Jiong Yu, Yi Lu, Yaohua Wang, Ziyang Li</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30437v1) · [PDF 下载](https://arxiv.org/pdf/2608.30437v1) · **关键词** 图增强大语言模型, 图检索增强生成, 最短跳数问答, 图到解码器接口, 原生解码器可用性<br>


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

本文位于图增强大语言模型（graph-augmented large language models）与图检索增强生成（GraphRAG）交叉领域。此类系统通常先通过图算法、检索器或图编码器提取与问题相关的节点、边或子图，再将这些信息以文本、图标记或其他输入表示提供给语言模型，最后由模型原生解码器生成答案。本文关注其中一个基础但常被混淆的接口问题：外部计算得到的图证据虽然已经被放入输入，解码器是否真的能够按照其结构读取并使用这些证据。为排除开放式生成和答案歧义的影响，论文采用纯拓扑、答案为小整数的最短跳数问答作为诊断任务。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**图与最短跳数**

图由节点和连接节点的边组成；两个节点之间的最短跳数，是从一个节点到另一个节点所需经过的最少边数。例如直接相连的两个节点距离为 $1$，中间还经过一个节点则距离为 $2$。

</div>
<div class="concept-item" markdown="1">

**图增强大语言模型**

图增强大语言模型先从图中检索或计算证据，再把证据转成模型输入，依靠语言模型生成最终答案。这里的关键不只是“是否提供了证据”，还包括证据的组织形式是否能让解码器识别节点之间的结构关系。

</div>
<div class="concept-item" markdown="1">

**原生解码器可用性**

原生解码器可用性指语言模型不依赖额外执行器、候选打分器或受限输出机制，仅凭输入中的图证据生成正确答案的能力。本文将图信号存在、图证据可见、图结构可读和解码器能够实际利用这些层次区分开来。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个图 $G$ 以及两个查询节点 $s$ 和 $t$，HopQA 要求模型输出节点对 $(s,t)$ 在图中的最短跳数 $d_G(s,t)$。输入可以包含由外部图计算或检索过程产生的相关图证据，输出则是一个严格匹配的整数答案。该设定假定图证据已经被转译到语言模型输入中，但不假定模型天然能够恢复证据中的拓扑关系；研究问题正是判断这种图到解码器的表示接口是否足以支持正确的原生生成。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$G$**

待查询的图，包含节点及其边结构。

</div>
<div class="notation-item" markdown="1">

**$s,t$**

最短路径查询中的起点节点和终点节点。

</div>
<div class="notation-item" markdown="1">

**$d_G(s,t)$**

图 $G$ 中从节点 $s$ 到节点 $t$ 的最短跳数，即最少需要经过的边数。

</div>
<div class="notation-item" markdown="1">

**$D_{\mathrm{task}}$**

任务相关的图证据或输入内容；本文的核心诊断是考察解码器能否从其中恢复与查询有关的拓扑信息。

</div>

</div>

**直接相关的工作**

- **G-Retriever**: G-Retriever 代表将紧凑的文本子图检索出来并置于生成模型输入中的方法，说明图结构可以通过文本证据暴露给语言模型。本文进一步追问：这种证据虽然可见，是否具有足够清晰的组织方式，使原生解码器能够准确使用其中的拓扑关系。
- **LLaGA**: LLaGA 将图表示投影到大语言模型的输入空间，代表学习式图—语言接口。本文与其关注点不同：本文不主要提出新的图表示投影，而是用受控的最短跳数诊断和不同证据排列条件，区分图证据是否存在、是否结构可读，以及是否真正被原生解码器利用。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

S²GE（Sampling-First Structured Graph Encoding）是一种面向原生语言模型解码器的“采样优先”图接口。输入是图 $G=(V,E,X)$、查询端点 $q=(s,t)$ 和节点预算 $B$；系统先构造有界子图 $G_{\mathrm{sub}}=S_B(G,q)$，再依据节点相对查询端点的角色与距离排序、投影为图令牌，并以邻接对齐损失约束投影空间，最终让解码器直接生成最短跳数 $y=d_G(s,t)\in\{1,2,3,4,5\}$。其设计依次处理三个接口瓶颈：查询相关证据是否进入预算、源点和目标点等角色是否可读、投影后的令牌是否仍保留局部邻接关系。

直观地说，方法并不期待语言模型从一堆无序图令牌中自行恢复图结构，而是先选出与问题最有关的局部地图，再给地图中的起点、终点和沿途节点设置清楚的路标，最后要求相邻地点在表示空间中仍然彼此接近。训练同时优化答案生成和结构保持；推理时无需外部最短路执行器，模型通过普通自回归解码输出一个整数答案。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造HopQA实例与有界接口

将任务限定为五分类式生成问题，其中 $y\in\mathcal{A}$ 且 $\mathcal{A}=\{1,2,3,4,5\}$；接口最多容纳 $B$ 个采样节点。模型只能通过该有界接口观察图，因此采样阶段丢失的信息不能由更大的解码器事后恢复。

<div class="method-step__io" markdown="1">

**输入**：图 $G=(V,E,X)$、查询 $q=(s,t)$、节点预算 $B$，以及训练时的真实答案 $y=d_G(s,t)$。<br>
**输出**：一个待采样的端点条件查询，以及明确的接口预算和目标跳数。

</div>

**直观理解**：这一步把开放式图推理压缩成一个答案范围很小、可严格判分的问题。它相当于规定模型只能查看一张尺寸有限的局部地图，然后回答起点到终点最少经过几条边。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 查询感知子图采样

采样器优先把可用的源点与目标点放入种子集合，并围绕端点相关节点和高阶节点进行局部扩展，随后截断为 $G_{\mathrm{sub}}=S_B(G,q)$。该步骤针对局部证据条件 $C_{\mathrm{local}}(q)$，决定哪些路径或邻域信息能够进入解码器视野。

<div class="method-step__io" markdown="1">

**输入**：完整图 $G$、查询端点 $s,t$ 和节点预算 $B$。<br>
**输出**：节点数受 $B$ 约束、以查询端点为中心的采样子图 $G_{\mathrm{sub}}$。

</div>

**直观理解**：预算有限时，随机装入许多节点可能恰好漏掉起点、终点或连接路径。查询感知采样先保住解题最需要的区域，类似先把地图裁剪到起终点附近，而不是平均保留整座城市的信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 基于角色的感知与序列化

为节点赋予源点、目标点、端点邻近节点或上下文节点等查询条件角色，并按角色 $r(v)$、到两端点的采样子图距离 $d_s(v),d_t(v)$、负度数 $-\deg(v)$ 和稳定遍历索引 $b(v)$ 排序。排序后的节点被投影为序列 $T(q)=(z_{\pi(1)},\ldots,z_{\pi(m)})$，并与角色、局部度数和排序键等可计算注释共同形成接口 $I_B(G,q)$。

<div class="method-step__io" markdown="1">

**输入**：采样子图 $G_{\mathrm{sub}}$ 及其中各节点相对 $s,t$ 的局部属性。<br>
**输出**：角色可辨、顺序稳定的投影图令牌及其接口注释。

</div>

**直观理解**：单纯给出节点向量并不会告诉语言模型哪个是起点、哪个是终点。该步骤相当于为节点贴上“起点”“终点”“附近节点”“背景节点”标签，并按与问题的相关程度排队。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 邻接对齐、联合训练与原生生成

训练时，一方面以语言模型负对数似然学习自回归生成答案，另一方面使令牌两两余弦相似度矩阵逼近加自环并归一化后的采样邻接矩阵；两项损失按固定权重联合优化。推理时仅构造同样的可读接口，由原生解码器自由生成，并以严格精确匹配检查是否输出正确跳数。

<div class="method-step__io" markdown="1">

**输入**：投影令牌矩阵 $Z\in\mathbb{R}^{m\times d}$、采样子图邻接矩阵 $A_B$、接口 $I_B(G,q)$ 和训练答案序列 $y$。<br>
**输出**：训练后可从图令牌接口直接生成单个最短跳数的语言模型。

</div>

**直观理解**：角色标签说明“谁是谁”，邻接对齐进一步说明“谁和谁直接相连”。训练完成后不再调用外部最短路算法，而是检验普通解码过程能否真正读懂这些结构化证据。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 采样邻接对齐损失

$$
\tilde{A}_B=A_B+I,\qquad \hat{A}_B=\tilde{D}^{-1/2}\tilde{A}_B\tilde{D}^{-1/2},\qquad \mathcal{L}_{\mathrm{align}}=\left\|\operatorname{norm}(Z)\operatorname{norm}(Z)^{\top}-\hat{A}_B\right\|_F^2
$$

**符号说明**

- $A_B$：采样子图的邻接矩阵。
- $I$：单位矩阵；加入它等价于为每个采样节点添加自环。
- $\tilde{A}_B$：加入自环后的采样邻接矩阵。
- $\tilde{D}$：由加入自环后的邻接矩阵计算得到的度矩阵。
- $\hat{A}_B$：对称归一化后的邻接目标。
- $Z\in\mathbb{R}^{m\times d}$：由 $m$ 个采样节点的 $d$ 维投影图令牌按行组成的矩阵。
- $\operatorname{norm}(Z)$：对 $Z$ 的每一行执行 $\ell_2$ 归一化后的矩阵。
- $\|\cdot\|_F^2$：Frobenius范数的平方，用于累计两个矩阵对应元素之间的平方误差。

<div class="equation-explanation" markdown="1">

**直观理解**：行归一化令牌的内积是节点令牌之间的余弦相似度，因此左侧矩阵描述投影空间中的两两接近程度；损失要求它接近采样子图的归一化邻接结构。这样做并不直接计算最短路，而是减少投影过程中局部边关系被抹去的风险。<br>
**原文位置**：第3.1节“Adjacency-based alignment”

</div>

</div>

<div class="equation-block" markdown="1">

#### 联合训练目标

$$
\mathcal{L}=\mathcal{L}_{\mathrm{LM}}+\lambda\mathcal{L}_{\mathrm{align}},\qquad \mathcal{L}_{\mathrm{LM}}=-\sum_{j=1}^{|y|}\log p_{\theta}\!\left(y_j\mid y_{<j},I_B(G,q)\right)
$$

**符号说明**

- $\mathcal{L}$：S²GE的总训练损失。
- $\mathcal{L}_{\mathrm{LM}}$：目标答案序列的逐令牌负对数似然。
- $\mathcal{L}_{\mathrm{align}}$：保持采样子图邻接关系的对齐损失。
- $\lambda$：邻接对齐项的权重；论文通过验证固定为 $0.25$。
- $y_j$：真实答案序列中的第 $j$ 个令牌。
- $y_{<j}$：第 $j$ 个位置之前的真实答案令牌前缀。
- $I_B(G,q)$：由预算为 $B$ 的采样子图构造、提供给语言模型的图接口。
- $p_\theta$：参数为 $\theta$ 的解码器给出的条件令牌概率。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项要求模型生成正确的跳数答案，第二项要求输入模型的图令牌仍能反映局部边关系。二者联合优化把“答对问题”和“不要在投影时破坏证据结构”连接起来，避免只训练输出格式而忽略图拓扑。<br>
**原文位置**：第3.2节“Training Objective and Diagnostics”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练采用教师强制式自回归学习：在每个答案位置，以真实前缀 $y_{<j}$ 和图接口 $I_B(G,q)$ 为条件，提高真实令牌 $y_j$ 的概率。同时计算采样子图的归一化邻接目标，并以 $\lambda=0.25$ 加权邻接对齐损失；因此梯度同时更新答案生成路径和图令牌投影，使模型既学会输出合法跳数，也保留支撑该答案的局部拓扑。该权重由验证确定，所给正文未说明搜索范围。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 查询感知采样器**

该模块实现接口的第一道门控：在预算 $B$ 内强制优先纳入查询端点，并围绕端点相关节点和高阶节点扩展，得到 $G_{\mathrm{sub}}$。论文用端点覆盖率和路径召回率审计其对应的 $C_{\mathrm{local}}(q)$，但所给正文未提供更细的打分函数或并列节点处理规则。

> 直观理解：它解决的不是模型会不会推理，而是模型有没有看到足够的解题证据；若连接路径在采样时已经被删除，任何后续解码能力都无法恢复它。

**2. 角色感知排序与图令牌接口**

节点顺序定义为 $\pi=\operatorname{sort}(V_B;r(v),d_s(v),d_t(v),-\deg(v),b(v))$，其中角色优先区分源点、目标点、端点邻近节点和上下文节点，局部距离与度数进一步表达端点接近性和邻域显著性，稳定索引保证序列化可复现。该模块对应角色可读性 $S_{\mathrm{role}}(q)$，并通过角色消融和查询消融检验。

> 直观理解：图本身没有天然的文本阅读顺序；若节点无标识地排列，解码器很难知道查询指向谁。固定角色和次序把无序局部图改造成更适合语言模型逐令牌读取的证据列表。

**3. 邻接保持投影**

投影后令牌组成 $Z\in\mathbb{R}^{m\times d}$，模块将行归一化后的令牌内积与归一化邻接目标 $\hat A_B$ 对齐，使直接相邻节点在令牌空间中具有较高相似性。它对应邻接可恢复性 $A_{\mathrm{adj}}(q)$，论文使用冻结邻接探针检查结构在投影后是否仍可读。

> 直观理解：投影可能把原图中的边关系冲淡，使解码器只看到彼此无关的向量。该约束像是在编码后继续把原本相邻的节点绑在一起，降低结构信息在进入语言模型前的损失。

**训练与推理**

训练阶段：对每个 $(G,q,y)$ 实例，先按预算 $B$ 进行查询感知采样，再计算节点角色、端点局部距离、度数和稳定遍历索引，按照 $\pi$ 排序并投影为图令牌；随后把图令牌及其注释输入语言模型，联合最小化 $\mathcal{L}_{\mathrm{LM}}$ 与 $\mathcal{L}_{\mathrm{align}}$。推理阶段沿用同一采样、排序和投影流程，但不需要真实答案，也不执行损失计算；原生解码器根据 $I_B(G,q)$ 自由生成答案。HopQA要求生成 $d_G(s,t)\in\{1,2,3,4,5\}$，主要判定采用严格精确匹配，因此带有额外文字、格式错误或错误整数的输出均不能视为严格正确。

**复现信息**

正文明确给出的关键设置包括：图接口采用固定节点预算，图2示例为 $B=32$；主实验使用LLaMA-3-8B-Instruct作为单一解码骨干，因此结果不能直接证明跨模型规模的收益；邻接对齐权重固定为 $\lambda=0.25$。节点排序依次利用角色、到源点和目标点的采样子图局部距离、负度数和稳定遍历索引。所给章节未明确报告采样扩展的精确伪代码、图投影层结构、优化器、学习率、批大小、训练轮数及解码参数，复现时需要进一步核对附录C。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Core-HopQA：从GRBench构造DBLP、Biomedical和GoodReads三个域，分别代表引文图、生物医学关系图和推荐图；所有域采用平衡的五标签协议，因此随机预测和多数类预测的期望准确率均为$20\%$。其作用是检验原生跳数生成能否跨越不同图类型使用拓扑证据。
- Core-HopQA中的PubMed域：数据来自Planetoid/PubMed，代表另一类引文图。它与DBLP共同用于比较图令牌干预和接口消融，但两者呈现不同的打乱敏感性。
- PubMed path-witness诊断：除预测标量跳数外，还要求模型给出局部有效的第一跳见证；该设置用于区分只输出正确数字与实际形成局部拓扑推理之间的差异。原文未明确报告该诊断的独立训练、测试规模和划分细节。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**StrictEM**

严格精确匹配，计算预测字符串与正确答案完全相同的样本比例：$\mathrm{StrictEM}=\frac{1}{n}\sum_i\mathbf{1}\{\mathrm{exact}(\hat y_i)=y_i\}$。它是主要的原生可用性指标，要求模型不仅得到正确数字，还要以严格规定的形式输出。 （越高越好，因为它同时反映答案正确性和原生输出表面是否符合评测要求。）

</div>
<div class="metric-item" markdown="1">

**ParsedEM**

解析精确匹配，先从生成结果中提取第一个整数，再比较提取值与标签：$\mathrm{ParsedEM}=\frac{1}{n}\sum_i\mathbf{1}\{\mathrm{extract}(\hat y_i)=y_i\}$。它审计模型是否留下正确的数值痕迹，但放宽了严格格式要求。 （越高越好；但它不能单独证明模型真正使用了图证据，因为正确整数可能来自任务先验或非结构性线索。）

</div>
<div class="metric-item" markdown="1">

**$\Delta^+_{\mathrm{su}}$**

正信号使用差距，定义为$\Delta^+_{\mathrm{su}}(m)=\max\left(0,\max_{c\in C_{\mathrm{graph}}}\mathrm{EM}(c)-\mathrm{EM}(m_{\mathrm{nat}})\right)$，其中$C_{\mathrm{graph}}$是图控制条件集合，$m_{\mathrm{nat}}$是原生生成模型。它衡量图控制决策表面是否显著优于原生生成。 （从诊断角度，差距越小越好：较大的正差距表示原生生成没有把图证据转化为可用输出；不过该指标本身不是模型准确率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Core-HopQA上的原生生成主结果

<div class="result-value" markdown="1">

G-Retriever在四个域上的StrictEM均为$0.0\pm0.0\%$，LLaGA也接近零；S$^2$GE在DBLP、Biomedical、GoodReads和PubMed上的StrictEM分别为$36.5\%$、$57.8\%$、$76.6\%$和$52.0\%$。相对$20\%$随机基线，S$^2$GE的增益分别为$+16.5$、$+37.8$、$+56.6$和$+32.0$个百分点。

</div>

在答案空间很小且任务只要求拓扑跳数的条件下，已有原生图增强基线仍几乎不能严格生成正确标签，而S$^2$GE达到明显高于随机的结果。这支持作者关于“提供图证据不等于原生解码器能使用图证据”的诊断，但不能单独证明S$^2$GE在每个样本上都执行了可靠的显式路径推理；任务先验和输出形式仍可能影响结果。

<div class="result-source" markdown="1">

来源：第4.2节，Table 1及其正文

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 1 shows that G-Retriever obtains 0.0±0.0% strict EM across Core-HopQA, while LLaGA stays near zero. S2GE reaches 36.5–76.6% strict EM, corresponding to ∆Chance gains of +16.5, +37.8, +56.6, and +32.0 on DBLP, Biomedical, GoodReads, and PubMed.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 图令牌干预三角：可读、无图与打乱图

<div class="result-value" markdown="1">

单个代表性种子的StrictEM为：DBLP可读图$34.0\%$、无图$15.0\%$、打乱图$6.0\%$；Biomedical为$57.8\%$、$57.1\%$、$52.7\%$；GoodReads为$76.6\%$、$9.8\%$、$34.2\%$；PubMed为$52.0\%$、$19.5\%$、$51.3\%$。

</div>

三种条件将“是否包含证据”“证据是否保持可读组织”和“模型是否真正依赖拓扑”分开。DBLP中打乱后低于无图，说明顺序破坏会造成有害干扰；PubMed中打乱几乎不影响可读条件，说明该域对组织顺序鲁棒；Biomedical中无图几乎达到可读图，表明任务先验已经足以产生较高分数，即无图饱和。由于这些是单个代表性种子结果，不能替代多种子主结果。

<div class="result-source" markdown="1">

来源：第4.3节，Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 3: Graph-token interventions. Values are StrictEM percentages from a single representative seed; Table 1 reports the multi-seed main results.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### PubMed path-witness诊断

<div class="result-value" markdown="1">

Pure GNN的答案准确率为$48.4\pm0.8\%$、第一跳联合准确率为$40.4\pm2.3\%$；S$^2$GE分别为$96.6\pm1.4\%$和$59.8\pm0.4\%$。第一跳联合准确率要求同时给出正确答案和有效的第一跳见证。

</div>

S$^2$GE不仅在标量答案上明显高于Pure GNN，也更常能满足答案加局部第一跳见证这一更严格条件。不过联合指标明显低于答案准确率，说明得到正确跳数并不等价于稳定地产生可验证的局部路径证据；该诊断支持作者对“图证据使用”和“输出形式”同时造成差距的判断。

<div class="result-source" markdown="1">

来源：第4.2节，Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 2: PubMed path-witness diagnostic. Values are percentages. Answer accuracy measures the path-existence answer. First-hop joint accuracy requires both the correct answer and a valid first-hop witness.

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

- G-Retriever：原生生成基线，使用其公开实现和检查点；它直接检验已有图增强方法能否让原生解码器生成正确标签。
- LLaGA：另一种原生生成图语言模型基线，与G-Retriever共同构成主要的原生解码比较。
- Pure GNN：仅使用图神经网络的图控制模型，用于判断图结构本身是否足以支持答案，而不要求语言模型进行原生生成。
- SubgraphRAG：检索—执行控制方法，将图子结构检索后交给执行式流程；它用于比较“检索后显式执行”与“把证据交给原生解码器”这两种决策表面。

**实验想回答的问题**

- 在答案是有限五分类整数、且任务只依赖图拓扑的情况下，外部提供的图证据是否真的能被原生解码器读取并用于生成正确的跳数标签，而不是仅仅被放入输入上下文？
- S$^2$GE中的查询感知采样、端点与邻近性排序、角色感知组织和结构保持对齐，分别是否改善了图证据的可用性；不同图域是否会呈现有害打乱、打乱鲁棒或无图饱和等不同状态？

**实验实现**

实验分为Core-HopQA原生跳数标签生成和Auxiliary Graph Diagnostics辅助诊断两部分，后者覆盖信号提取、路径证据、图令牌干预和邻接迁移。所有可训练的S$^2$GE实验使用最多12个epoch、早停耐心值6和三个随机种子；G-Retriever与LLaGA使用公开实现、检查点及各自方法的优化设置。主实验约使用400 GPU小时；原文还报告了5090 GPUs，但未明确该表述对应的具体GPU数量或配置。图令牌干预比较可读图、无图和打乱图三种匹配条件：可读条件保留图内容及组织顺序，无图条件移除证据，打乱条件保留令牌内容但破坏顺序。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| PubMed接口消融：查询感知采样、角色感知、距离/度数线索和对齐 | 完整S$^2$GE的StrictEM为$52.0\pm3.4\%$；移除查询感知采样后为$25.0\pm1.1\%$，下降$27.0$个百分点；移除角色感知后为$47.0\pm2.3\%$，下降$5.0$个百分点；移除距离/度数线索后为$45.9\pm2.7\%$，下降$6.1$个百分点；移除对齐后为$52.0\pm3.7\%$，报告为不变。 | PubMed属于打乱鲁棒域，主要瓶颈是是否采到与查询相关的证据，而不是令牌顺序，因此查询感知采样的移除造成最大损失。角色、距离和度数线索有中等作用；对齐在该域没有可见主结果收益，但“不变”不能证明对齐普遍无效，因为它可能依赖域或随机波动。 | 第4.4节，Table 4；完整模型行见同表<br><span class="experiment-evidence">no query-aware sampling25.0±1.1−27.0</span> |
| DBLP接口消融：查询语法、度数线索、角色感知与随机排序 | 完整S$^2$GE的StrictEM为$36.5\pm1.6\%$；移除查询语法后为$24.1\pm5.2\%$，下降$12.4$个百分点；移除度数线索后为$22.8\pm3.7\%$，下降$13.7$个百分点；移除角色感知后为$32.0\pm2.3\%$，下降$4.5$个百分点；随机排序诊断为$33.8\pm5.0\%$，下降$2.7$个百分点。 | DBLP属于有害打乱域，结果显示查询语法和度数线索比角色感知更关键，说明该域需要更明确的端点和局部结构信号。随机排序的平均下降较小且方差较大，不能据此断言排序不重要；它更适合作为诊断，结合Table 3中打乱图从可读图的下降来理解组织破坏的风险。 | 第4.4节，Table 4；完整消融结果见同表<br><span class="experiment-evidence">no degree cues22.8±3.7−13.7</span> |

**定性案例**

- 作者将DBLP和PubMed作为代表性域：DBLP满足$S_\kappa<N_\kappa<R_\kappa$，即打乱图低于无图且无图低于可读图，属于有害打乱；PubMed满足$S_\kappa\approx R_\kappa$，属于打乱鲁棒。直观上，同样的图令牌干预在不同域触发了不同输出状态，说明接口设计不能只按证据数量评价，还必须检查局部结构是否能被解码器利用。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文诊断图增强 LLM 对拓扑图证据的可用性，并通过结构化证据接口提升多跳图推理性能。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`787e5a89d8fe52d7cd6b1b45cbacb8490868a2cdbd28e4f605add8dc8fbefe77`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
