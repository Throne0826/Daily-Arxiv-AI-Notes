---
title: "[论文解读] Cloud-ScPO: Hidden-State Geometry for Semi-Supervised Preference Optimization in LLM Reasoning"
description: "[arXiv 2608.01014][对齐 / RLHF] 本文研究能否利用大语言模型内部隐藏状态的全局几何结构，在只有少量已标注数学题的条件下，为大量未标注推理轨迹构造可靠的偏好训练对。"
arxiv_id: "2608.01014"
announcement_date: "2026-08-04"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:58:16.074930+00:00"
source_sha256: "14bed5634d763ce8a7d542929d3b4ee0c82f3ab211797947b11a1b02e48edb92"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "LLM 机制与可解释性"
  - "大语言模型数学推理"
  - "半监督偏好优化"
  - "隐藏状态几何"
  - "轨迹表示"
  - "点云"
  - "自一致性"
  - "偏好对挖掘"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.01014</p>

# Cloud-ScPO: Hidden-State Geometry for Semi-Supervised Preference Optimization in LLM Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Yuzhou Liu, Xiyang Hu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> University of Southern California,2 Arizona State University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01014v1) · [PDF 下载](https://arxiv.org/pdf/2608.01014v1) · **关键词** 大语言模型数学推理, 半监督偏好优化, 隐藏状态几何, 轨迹表示, 点云, 自一致性, 偏好对挖掘<br>


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

本文研究能否利用大语言模型内部隐藏状态的全局几何结构，在只有少量已标注数学题的条件下，为大量未标注推理轨迹构造可靠的偏好训练对。

**不用术语来说**：偏好优化需要知道同一道题的多个回答中哪个更值得学习、哪个应被抑制，但逐条核验答案或比较长推理过程成本很高。仅按多数答案投票也不够，因为多个推理可能得到相同答案却质量不同，而且多数答案本身可能是错的；本文因此尝试从模型处理完整推理时形成的内部表示中寻找额外的质量线索。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出一种跨题目的轨迹质量信号：将完整回答的响应词元隐藏状态做均值池化，并观察少量有标签轨迹形成的全局点云，以其中正确与错误轨迹在密度、连通性和拓扑变化上的差异辅助判断未标注轨迹质量。
- 作者提出 Cloud–ScPO：通过多个有标签参考点云和基于连通分量的软近邻评分选择具体轨迹，再与题目内的自洽性投票结合，确定答案层面的偏好方向并过滤低置信度训练对，从而无需为每条未标注轨迹提供标准答案或外部奖励分数。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型数学推理的半监督偏好优化研究。偏好优化通过“优选回答—拒绝回答”对调整模型，使其更倾向生成高质量推理轨迹；但传统监督通常依赖人工比较、答案验证器或外部奖励模型，而这些资源成本高或不可获得。本文关注更受限的场景：只有少量数学题具有已验证答案，大量题目及其多次采样得到的长推理轨迹没有标签。其基本出发点是，模型隐藏状态不仅是生成过程的中间数值，还可能编码轨迹正确性与质量；不同问题的轨迹表示共同形成全局点云，其中正确轨迹据作者观察通常更稠密、更连贯，并在较小的拓扑过滤尺度下连通，错误轨迹则更分散、几何变化更大。因此，可利用少量有标签轨迹建立跨问题参照结构，为无标签轨迹提供偏好信号。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**偏好优化**

训练数据由同一提示下的优选轨迹和拒绝轨迹构成，目标是提高模型对前者的相对生成倾向。本文的核心问题不是修改偏好优化的基本用途，而是如何在缺少逐轨迹标签时可靠地构造这些训练对。

</div>
<div class="concept-item" markdown="1">

**自一致性**

对同一道题采样多条推理轨迹，再按最终答案分组，并把出现次数最多的答案视为较可信答案。它能提供答案层面的偏好方向，但多数答案仍可能错误，而且同一答案组内的轨迹质量可能差异很大。

</div>
<div class="concept-item" markdown="1">

**隐藏状态点云与连通结构**

将每条完整推理轨迹的响应词元隐藏状态做均值池化，得到一个向量点；许多跨问题轨迹向量的集合称为点云。随着允许连接的距离阈值增大，邻近点会组成连通分量，这种结构用于描述轨迹表示是聚集、连贯还是分散。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括一个仅有少量提示具备已验证答案的数学推理数据集、每个提示由当前语言模型采样得到的多条推理轨迹，以及这些轨迹对应的模型隐藏状态；其余多数提示和轨迹不带正确性标签。对于每条轨迹，方法以响应词元隐藏状态的均值作为轨迹级表示，并利用有标签问题中的正确与错误轨迹构造多个跨问题参考点云。目标是在不为每条无标签轨迹调用人工标注、答案验证器或外部奖励模型的条件下，结合参考点云的几何评分与提示内自一致性，输出高置信度的优选—拒绝轨迹对，供后续偏好优化使用。这里假设少量已验证答案足以把参考轨迹划分为正确和错误集合，也假设隐藏表示的跨问题几何结构与轨迹正确性或质量存在可迁移关联；该关联是本文要利用的经验前提，而不是对任意模型均成立的理论保证。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

一个数学问题或提示；同一 $x$ 可采样多条推理轨迹。

</div>
<div class="notation-item" markdown="1">

**$y$**

模型针对提示 $x$ 生成的一条完整推理轨迹，包含中间推理文本和最终答案。

</div>
<div class="notation-item" markdown="1">

**$h(y)$**

轨迹 $y$ 的向量表示，由其响应词元隐藏状态进行均值池化得到。

</div>
<div class="notation-item" markdown="1">

**$k$**

软 $k$ 近邻评分所考察的近邻数量，用于比较待评分轨迹与参考点云连通分量的接近程度。

</div>

</div>

**直接相关的工作**

- **Self-Consistency Preference Optimization（ScPO）**: ScPO把提示内自一致性转化为偏好监督：多数答案簇中的轨迹优先于少数答案簇中的轨迹，从而降低对金标准答案的依赖。其局限是主要依据单个提示内部的答案频率，无法可靠区分同一答案簇中的具体轨迹，也容易受错误共识影响；Cloud-ScPO保留其答案分组机制，同时加入跨问题参考点云评分来选择轨迹并按分数间隔过滤偏好对。
- **Latent-GRPO（Silence the Judge）**: Latent-GRPO同样从隐藏状态几何中产生内在监督，但它为每个提示估计局部潜在中心，并奖励更接近该中心的轨迹，因此信号局限于该提示采样组，可能追随错误的组内共识。本文改用从不同有标签问题收集的正确与错误轨迹建立多组全局参考点云，使几何监督能够跨提示迁移。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

数学推理偏好训练通常要从每道题生成的多条长轨迹中构造“优选—拒绝”对。可靠构造依赖人工比较、标准答案或外部验证器，但人工标注昂贵，验证器并非总是可用，而最终答案标签只能判断结果，难以揭示中间推理是否完整、清晰或存在重复。因此，在仅有少量题目经过核验、大多数题目及其轨迹均未标注的半监督场景中，训练系统缺少可扩展的轨迹级偏好依据。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **自生成推理与自洽性监督（STaR、self-consistency、ScPO）**：STaR迭代学习能够到达正确答案的模型自生成解释；自洽性对同一题采样多条轨迹，并以答案投票选出多数答案；ScPO进一步把这种投票转成偏好监督，优先选择多数答案簇中的轨迹，并将少数答案簇中的轨迹作为拒绝样本。
- **半监督奖励建模**：先用有限的有标签偏好数据训练奖励模型，再由奖励模型为未标注回答生成伪偏好，通常通过迭代训练逐步扩大可用于偏好优化的数据。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 题目内的答案投票只能提供答案簇层面的信号：当同一答案对应多条质量不同的推理时，它不能可靠选出具体优质轨迹；当多数答案错误时，ScPO式偏好方向也可能失真，进而把错误或低质量推理写入训练对。
- 半监督奖励建模仍需额外训练一个奖励模型，其伪标签质量受少量初始偏好标注制约；最终答案监督也不能充分区分过程完整、信息充分的回答与不完整、重复或其他低质量回答。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种同时满足三点的轨迹级信号：能够利用少量已标注样本迁移到跨题目的未标注轨迹，不必为每条轨迹调用标准答案、人工比较或外部奖励模型，并且能在答案簇内部进一步区分具体推理质量。作者据此把尚未被充分利用的模型内部表示几何视为候选监督来源；这是论文提出的研究切口，而其可靠性仍需通过下游训练和偏好对分析验证。

</div>
<div markdown="1"><span>核心问题</span>

不同数学题的推理轨迹在大语言模型隐藏状态空间中是否形成与正确性相关、可跨题复用的全局几何结构；若存在，能否用少量有标签轨迹建立参考点云，并把其评分与题目内自洽性结合，从大量未标注轨迹中挖掘高置信度偏好对，从而改进半监督推理优化？

</div>
<div markdown="1"><span>作者直觉</span>

作者报告的关键观察是：把每条完整推理压缩成一个隐藏状态向量后，不同题目的轨迹并非互不相关地散落；正确轨迹倾向于位于更稠密、更一致且在较小过滤尺度便相互连通的区域，错误轨迹则通常更分散、几何与拓扑变化更大。直观地说，虽然题目表面内容不同，可靠推理可能激活相似而稳定的内部计算模式，因此“它在全局表示空间中更接近哪些已知轨迹”可补充题目内多数投票：投票决定倾向哪个答案，点云评分再从相应答案簇中选择更可信的具体表达。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Cloud–ScPO 是一种半监督偏好优化方法：给定少量带标准答案的问题集 $\mathcal{D}_L$ 和大量无标注问题集 $\mathcal{D}_U$，它先用带标注数据验证推理轨迹并完成监督微调，再从正确与错误轨迹的隐藏状态中建立多个全局参考“点云”。对于无标注问题，微调后的策略生成多条候选轨迹；方法一方面用答案投票的自一致性确定哪个答案簇应被偏好，另一方面用候选轨迹相对正确、错误参考点云的几何兼容度，在答案簇内选择具体的 chosen/rejected 轨迹，并用 Cloud 分数差筛除低置信度偏好对。最终以投票差加权的 DPO 与 chosen 轨迹负对数似然联合训练策略。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 带标注轨迹生成与监督微调

基础模型为每个带标注问题生成 $K$ 条推理轨迹，将每条轨迹抽取出的最终答案与标准答案比较，从而划分正确池 $\mathcal{P}^{+}$ 和错误池 $\mathcal{P}^{-}$；仅用经验证的正确轨迹做监督微调，得到策略 $\pi_{\mathrm{SFT}}$。

<div class="method-step__io" markdown="1">

**输入**：少量带标准答案的数据 $\mathcal{D}_L=\{(x_i,a_i)\}_{i=1}^{n_L}$、基础语言模型，以及每个问题的采样数 $K$。<br>
**输出**：监督微调策略 $\pi_{\mathrm{SFT}}$，以及保留下来供点云建模使用的正确、错误带标注轨迹池。

</div>

**直观理解**：标准答案只用于给少量示例贴上“正确或错误”标签，并教会模型基本的解题输出方式。错误轨迹不会用于监督模仿，但会作为以后识别劣质推理的反面参照。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 轨迹表示与多参考点云构造

对一条轨迹的 $T$ 个隐藏状态取均值 $z(x,y)=T^{-1}\sum_{t=1}^{T}h_t$，再做 $L_2$ 归一化得到 $\bar z(x,y)=z(x,y)/\lVert z(x,y)\rVert_2$；随后从正、负轨迹池重复进行平衡采样，构造 $R$ 组参考库 $(\mathcal{C}_r^{+},\mathcal{C}_r^{-})$。

<div class="method-step__io" markdown="1">

**输入**：正确池 $\mathcal{P}^{+}$、错误池 $\mathcal{P}^{-}$，以及模型最后一层对每个有效响应 token 产生的隐藏状态 $h_t\in\mathbb{R}^{d}$。<br>
**输出**：由多个正类和负类参考库组成的全局表示点云，每个点表示一个完整推理响应。

</div>

**直观理解**：均值池化把整段推理压缩成一个向量，而不是只看最后一个 token，因此中间推理过程也能影响表示。使用多个参考库相当于从少量标注样本中反复抽取不同参照组，以降低一次抽样造成的偶然偏差。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 拓扑连通分量提取与 Cloud 评分

在每个正、负点云内按欧氏距离从小到大处理边，模拟零维 Vietoris–Rips 过滤中的连通分量合并；完成 $\lceil\rho(N-1)\rceil$ 次有效合并后停止，并删除小于预设规模的分量。候选向量分别与最近的 $q$ 个正、负分量计算按分量大小加权的距离核兼容度，再对正负兼容度作差并在 $R$ 个参考库上平均。

<div class="method-step__io" markdown="1">

**输入**：各参考库中的归一化轨迹向量，以及 $\pi_{\mathrm{SFT}}$ 为无标注问题 $x\in\mathcal{D}_U$ 生成的候选轨迹 $y$。<br>
**输出**：每条无标注候选轨迹的标量分数 $s_{\mathrm{cloud}}(x,y)$；分数仅在同一问题的候选轨迹之间比较。

</div>

**直观理解**：这里的“拓扑”主要指点云中哪些轨迹在较小距离下会连成局部群组，并不要求学习复杂的高维洞结构。评分看候选轨迹更接近哪些正确群组、又多大程度接近错误群组，而不是只依赖某一个最近样本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自一致性定向与偏好对筛选

先按最终答案聚类，仅保留具有唯一多数答案簇的问题；多数答案作为偏好答案 $a_x^{+}$，合格的最低频非多数答案作为拒绝答案 $a_x^{-}$，平票时优先选择含有更低 Cloud 分数轨迹的少数簇。随后从偏好簇 $\mathcal{C}_x^{+}$ 取 Cloud 分数最高的 $y_x^{+}$，从拒绝簇 $\mathcal{C}_x^{-}$ 取分数最低的 $y_x^{-}$，按分数差 $c_x^{\mathrm{Hybrid}}$ 排序并只保留前 $\alpha$ 比例。

<div class="method-step__io" markdown="1">

**输入**：同一无标注问题的有效候选集合 $\mathcal{Y}_x^{\mathrm{valid}}$、规范化后的最终答案及每条轨迹的 Cloud 分数。<br>
**输出**：无需访问 $\mathcal{D}_U$ 标准答案的偏好数据集 $\mathcal{D}_{\mathrm{pref}}=\{(x,y_x^{+},y_x^{-})\}$。

</div>

**直观理解**：答案投票负责判断“哪一类答案更可能正确”，点云分数负责在该答案类别中挑出更值得模仿或更应被压低的具体推理。这样避免仅凭几何分数决定答案方向，同时让训练对关注推理质量差异较明显的样本。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 分量兼容度与多参考库 Cloud 分数

$$
\kappa(d)=\exp\!\left(-\frac{d^{p}}{\tau}\right),\quad d_{r,j}^{c}(z)=\min_{u\in G_{r,j}^{c}}\lVert z-u\rVert_2,\quad S_r^c(z)=\log\frac{\sum_{j\in\mathcal{N}_{q,r}^{c}(z)}\omega_{r,j}^{c}\kappa(d_{r,j}^{c}(z))}{\sum_{j\in\mathcal{N}_{q,r}^{c}(z)}\omega_{r,j}^{c}},\quad s_{\mathrm{cloud}}(x,y)=\frac{1}{R}\sum_{r=1}^{R}\left[S_r^{+}(\bar z(x,y))-\lambda_{\mathrm{neg}}S_r^{-}(\bar z(x,y))\right]
$$

**符号说明**

- $\kappa(d)$：距离为 $d$ 时的指数衰减核函数。
- $d$：候选表示与参考分量之间的欧氏距离。
- $p$：控制距离衰减形状的正数指数；原文实验统一取 $p=2$。
- $\tau$：控制距离核衰减尺度的温度参数。
- $r$：参考库索引，取值为 $1$ 到 $R$。
- $R$：正负参考库对的总数。
- $c$：参考点云类别，$c\in\{+,-\}$ 分别表示正确类和错误类。
- $j$：参考点云内连通分量的索引。
- $z$：待评分的归一化轨迹表示。
- $G_{r,j}^{c}$：第 $r$ 个参考库中类别 $c$ 的第 $j$ 个拓扑连通分量。
- $u$：连通分量 $G_{r,j}^{c}$ 内的一个参考轨迹向量。
- $\mathcal{N}_{q,r}^{c}(z)$：类别 $c$ 的第 $r$ 个参考库中，距离候选 $z$ 最近的 $q$ 个连通分量索引集合。
- $q$：参与软近邻聚合的最近连通分量数量。
- $\omega_{r,j}^{c}=|G_{r,j}^{c}|$：分量大小权重，即该连通分量包含的参考轨迹数。
- $S_r^c(z)$：候选 $z$ 与第 $r$ 个参考库中类别 $c$ 的对数兼容度。
- $s_{\mathrm{cloud}}(x,y)$：问题 $x$ 的候选轨迹 $y$ 在所有参考库上的最终 Cloud 分数。
- $\bar z(x,y)$：轨迹 $y$ 对应的均值池化并经 $L_2$ 归一化的隐藏状态表示。
- $\lambda_{\mathrm{neg}}$：错误点云兼容度的惩罚系数。

<div class="equation-explanation" markdown="1">

**直观理解**：该式先把候选到每个局部轨迹群组的距离转换为相似度，距离越近，相似度越高；较大群组获得较大权重。随后用正确点云兼容度减去加权的错误点云兼容度，并对多个参考库平均，因此高分表示候选整体上更像已验证的正确推理、较不像已验证的错误推理。<br>
**原文位置**：Method，Topology-Guided Cloud Scoring，式 (2)–(3)

</div>

</div>

<div class="equation-block" markdown="1">

#### Cloud–ScPO 联合训练目标

$$
\mathcal{L}_{\mathrm{Cloud\text{-}ScPO}}=\mathbb{E}_{(x,y^{+},y^{-})\sim\mathcal{D}_{\mathrm{pref}}}\!\left[w(x)\left(-\log\sigma\!\left(\beta\left[\log\frac{\pi_{\theta}(y^{+}\mid x)}{\pi_{\mathrm{ref}}(y^{+}\mid x)}-\log\frac{\pi_{\theta}(y^{-}\mid x)}{\pi_{\mathrm{ref}}(y^{-}\mid x)}\right]\right)+\lambda_{\mathrm{NLL}}\left[-\frac{1}{|y^{+}|}\sum_{t=1}^{|y^{+}|}\log\pi_{\theta}(y_t^{+}\mid x,y_{<t}^{+})\right]\right)\right],\quad w(x)=\frac{V_x(a_x^{+})-V_x(a_x^{-})}{K}
$$

**符号说明**

- $\mathcal{L}_{\mathrm{Cloud\text{-}ScPO}}$：需要最小化的 Cloud–ScPO 总损失。
- $\mathcal{D}_{\mathrm{pref}}$：由无标注问题构造出的偏好三元组数据集。
- $x$：一个无标注数学问题。
- $y^{+}$：从偏好答案簇中选出的 chosen 推理轨迹。
- $y^{-}$：从拒绝答案簇中选出的 rejected 推理轨迹。
- $\pi_{\theta}$：参数为 $\theta$ 的待优化策略模型。
- $\theta$：待更新的模型参数。
- $\pi_{\mathrm{ref}}$：DPO 中保持固定、用于约束策略偏移的参考策略。
- $\sigma$：Sigmoid 函数，将相对偏好对数差映射为概率形式。
- $\beta$：DPO 偏好差的缩放系数。
- $\lambda_{\mathrm{NLL}}$：chosen 响应负对数似然项的权重。
- $|y^{+}|$：chosen 响应的 token 数，用于长度归一化。
- $t$：chosen 响应中的 token 位置。
- $y_t^{+}$：chosen 响应在位置 $t$ 的目标 token。
- $y_{<t}^{+}$：chosen 响应在位置 $t$ 之前的 token 前缀。
- $w(x)$：问题 $x$ 的归一化答案投票差，用于加权该偏好对的两项损失。
- $V_x(a)$：问题 $x$ 的 $K$ 条采样轨迹中产生规范化答案 $a$ 的轨迹数。
- $a_x^{+}$：问题 $x$ 的唯一多数答案。
- $a_x^{-}$：被选作拒绝方向的合格非多数答案。
- $K$：每个问题生成的候选轨迹总数。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项比较训练策略相对参考策略对 $y^{+}$ 和 $y^{-}$ 的偏好增量，促使模型更偏向 chosen 轨迹；第二项逐 token 强化 chosen 轨迹，避免模型只学到相对排序却不能稳定生成它。两项都乘以投票差 $w(x)$，因此答案投票越明确的训练对获得越高权重。<br>
**原文位置**：Method，Preference Pair Construction 式 (7)；Preference Optimization 式 (9)–(11)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：Cloud 分数本身不作为可微奖励直接回传，而是在训练前用于选择、过滤偏好对；参数优化仍通过固定偏好数据上的联合损失完成。DPO 项学习同一问题内 $y^{+}\succ y^{-}$ 的相对关系，并以 $\pi_{\mathrm{ref}}$ 约束模型不要无界偏离原策略；长度归一化 NLL 项则直接提高 chosen 轨迹的生成概率。归一化投票差 $w(x)$ 同时作用于两项，使自一致性更强的偏好对产生更大梯度，而 $\lambda_{\mathrm{NLL}}$ 控制“相对排序”与“直接模仿 chosen 响应”之间的权衡。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 全局多库隐藏状态点云**

每条响应由最后一层有效响应 token 的均值隐藏状态表示并归一化，正确与错误轨迹分别进入参考池；从两池平衡采样形成 $R$ 组正负参考库。该点云跨越不同数学问题，不是只用同一提示下的多次响应构造局部点云。

> 直观理解：跨问题点云试图捕捉“正确推理”和“错误推理”在模型内部表示中的共性。多库平均使最终判断不至于被某一组参考样本主导。

**2. 基于早期 $H_0$ 连通分量的软近邻评分**

零维持久同调 $H_0$ 跟踪距离阈值增大时点如何合并为连通分量；本文在完成由 $\rho$ 控制的部分合并后截断，获得早期连通分量，并丢弃过小分量。候选轨迹到一个分量的距离定义为它到该分量任一点的最小欧氏距离，评分聚合最近 $q$ 个分量的核相似度，并按分量包含的参考轨迹数加权。

> 直观理解：单个参考点可能是噪声，而连通分量代表一群相似轨迹；按群组评分可以同时考虑距离和群组规模。所谓“软近邻”表示邻近程度连续衰减，而不是达到某个距离就突然判为相同或不同。

**3. 自一致性与 Cloud 信号的分工融合**

自一致性通过同一问题的答案频数确定 $a_x^{+}$ 与 $a_x^{-}$，Cloud 分数不改变这一答案级方向，只在相应答案簇内选择 $y_x^{+}$、$y_x^{-}$，并用 $c_x^{\mathrm{Hybrid}}=s_{\mathrm{Cloud}}(y_x^{+})-s_{\mathrm{Cloud}}(y_x^{-})$ 控制保留比例 $\alpha$。

> 直观理解：多数投票通常适合判断答案方向，却不能区分得到同一答案的多种推理过程；隐藏状态几何则用于挑选更清晰的正例和更弱的反例。两种信号各做自己更可靠的判断，减少仅依赖其中一种信号的风险。

**训练与推理**

完整训练流程分为两个阶段。第一阶段在 600 个带标注问题上生成多条响应，用标准答案分出正确与错误轨迹；正确轨迹用于得到 $\pi_{\mathrm{SFT}}$，正负轨迹共同用于建立参考 Clouds。第二阶段由 $\pi_{\mathrm{SFT}}$ 在 $\mathcal{D}_U$ 上采样候选，对有效响应做答案规范化、答案聚类和 Cloud 评分，再通过唯一多数答案、簇内极值选择、Cloud margin 排序及前 $\alpha$ 比例保留规则构造 $\mathcal{D}_{\mathrm{pref}}$，最后最小化 Cloud–ScPO 联合目标得到 $\pi_\theta$。完成训练后的常规推理只需由 $\pi_\theta$ 根据新问题生成答案；参考点云和偏好对构造属于训练数据挖掘阶段，原文未说明测试时仍需执行 Cloud 评分。

**复现信息**

公平复现需要保留以下设计：每个问题采样 $K$ 条轨迹；轨迹表示只对有效响应 token 的最后一层隐藏状态做均值池化和 $L_2$ 归一化；正负参考库采用平衡采样并建立 $R$ 个库；连通分量在 $\lceil\rho(N-1)\rceil$ 次有效合并后截断，过滤过小分量；距离核指数固定为 $p=2$；候选分数只在同一问题内比较。偏好构造还必须执行响应有效性检查、最终答案抽取与规范化、唯一多数答案过滤、最低频合格少数答案选择、簇内 Cloud 极值选择，以及按 margin 保留前 $\alpha$ 比例。节选未给出 $K$、$q$、$\rho$、最小分量规模、$\tau$、$\lambda_{\mathrm{neg}}$、$\alpha$、$\beta$ 和 $\lambda_{\mathrm{NLL}}$ 的完整取值，不能据此补造；详细伪代码和实现参数由原文指向附录 B。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：约7.5K道训练题和1.3K道测试题，考查小学层级的多步数学推理。实验从原训练集保留10%作为开发集，最终约有6.7K道训练题、0.8K道开发题和1.3K道测试题；开发集用于超参数调整和检查点选择，测试集只用于最终评估。论文在该数据集上使用Llama-3-8B Base和Mistral-7B-v0.3。
- MATH-Numeric：从高中数学竞赛数据集MATH中筛选最终答案能够通过数值抽取与规范化进行判定的样本。过滤后训练集的10%作为开发集，官方测试集只用于最终评价；论文在该数据集上使用Llama-3-8B Base、Qwen3-8B，并额外考查推理能力更强的Qwen3-4B-Instruct-2507，以判断基础模型能力提高后Cloud几何信号是否更有信息量。原文节选未给出过滤后的具体样本规模。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**单次生成最终答案精确匹配准确率（exact-match accuracy）**

使用贪心解码为每道测试题生成一次回答，抽取最终数值答案；GSM8K直接比较抽取值，MATH-Numeric先规范化再与标准答案精确比较。该指标衡量最终答案正确率，而不直接评价推理过程是否严谨、简洁或事实一致。 （越高越好，因为更高数值表示测试集中最终数值答案完全匹配金标准的题目比例更大。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### GSM8K，Llama-3-8B Base：Cloud–ScPO与种子模型及ScPO比较

<div class="result-value" markdown="1">

种子模型准确率为41.62%，ScPO提高到49.74%，Cloud–ScPO进一步达到52.24%；因此Cloud–ScPO相对ScPO提高2.50个百分点，并在该骨干模型的已报告方法中取得最高准确率。

</div>

作者结果表明，跨题目的Cloud隐藏状态几何信号能够在ScPO的答案频率方向之上进一步改善偏好对选择。分析上，这支持“轨迹级几何筛选具有增量价值”，但单一数据集与骨干上的2.50个百分点不能单独证明提升必然来自拓扑结构，也不能说明推理文本本身在逻辑上全部正确。

<div class="result-source" markdown="1">

来源：Table 1；Main results and analysis，Results on GSM8K

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ScPO increases accuracy from 41.62% to 49.74% for Llama-3-8B and from 12.28% to 28.43% for Mistral-7B.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### GSM8K，Mistral-7B-v0.3：Cloud–ScPO与种子模型及ScPO比较

<div class="result-value" markdown="1">

种子模型准确率为12.28%，ScPO达到28.43%，Cloud–ScPO达到32.92%；Cloud–ScPO相对ScPO提高4.49个百分点。该设置中的相对改进大于Llama-3-8B上的2.50个百分点。

</div>

作者结果显示，在初始准确率较低的Mistral设置中，Cloud筛选仍能在自一致性偏好优化之上提供明显收益，因而改进并非只出现在一个骨干模型上。不过，该比较没有控制两个模型的表示空间质量、生成错误类型等差异，所以不能据此断言基础模型越弱，Cloud–ScPO的收益就一定越大。

<div class="result-source" markdown="1">

来源：Table 1；Main results and analysis，Results on GSM8K

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Cloud–ScPO achieves the best performance on both models, reaching 52.24% and 32.92%, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### GSM8K，奖励模型偏好选择$\mathrm{IRPO}_{\mathrm{RM}}$与ScPO系方法的偏好对数量及准确率比较

<div class="result-value" markdown="1">

$\mathrm{IRPO}_{\mathrm{RM}}$在Llama-3-8B上使用3,794个偏好对仅达到46.40%，在Mistral-7B上使用2,511个偏好对仅达到15.23%，均低于对应的ScPO和Cloud–ScPO结果；尤其低于Cloud–ScPO的52.24%和32.92%。

</div>

作者据此主张，偏好对数量本身不是决定因素，选择质量与置信度更重要。更严格地说，这组实验只表明“该奖励模型、该选对规则和该训练配置下，更多偏好对没有带来更好结果”；由于方法同时改变了评分器、偏好方向、筛选方式和样本数量，它不能独立建立偏好对质量的因果作用，也不能否定其他奖励模型。

<div class="result-source" markdown="1">

来源：Table 1；Main results and analysis，More preference pairs do not necessarily yield better performance

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

It reaches 46.40% accuracy with 3,794 pairs on Llama-3-8B and 15.23% with 2,511 pairs on Mistral-7B, remaining below both ScPO-based methods.

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

- Seed Model（Zero-shot CoT）：直接对初始模型$M_0$进行零样本思维链提示和贪心解码，不做任务微调。它提供训练前的能力下界，用于判断后续增益是否确实来自监督或偏好优化。
- SFT-600：由基础模型为600道可见的带标签题生成推理轨迹，通过金标准答案验证后，仅用正确轨迹进行监督微调。该基线衡量600道可见题能够直接提供多少可靠训练收益，并用于区分监督微调收益与利用无标签题进行偏好优化的额外收益。
- ScPO：按每道题抽样回答的最终答案分组，以出现频率最高答案对应的回答作为chosen、频率最低答案对应的回答作为rejected，并按两类答案的归一化频率差加权。它是最关键的直接对照，因为Cloud–ScPO在其提示级自一致性方向上加入了跨题目的隐藏状态几何评分。
- $\mathrm{IRPO}_{\mathrm{RM}}$：在600道可见题上先由金标准正确性确定偏好方向，再由ArmoRM-Llama3-8B从正确候选中选择最高分回答、从错误候选中选择最低分回答；在无标签题上直接选奖励分最高和最低的回答组成偏好对。该基线检验外部奖励模型打分及更大量偏好对是否足以替代Cloud几何信号与自一致性的结合。

**实验想回答的问题**

- 在仅有600道带金标准答案的题目、其余训练题目均无标签的半监督条件下，Cloud–ScPO能否比种子模型、监督微调、仅依赖答案频率的ScPO以及外部奖励模型选对方法获得更高的数学推理准确率？
- 性能提升究竟来自偏好对数量，还是来自偏好对的质量与筛选置信度；同时，均值池化并进行$\ell_2$归一化后的隐藏状态是否呈现足以支持Cloud评分的稳定$H_0$连通结构？

**实验实现**

所有方法处于半监督设置：随机抽取600道训练题作为有标签数据，其余题目视为无标签。ScPO与Cloud–ScPO对每题采样$K=8$个回答，保留排名前$\alpha=0.30$的候选偏好对，合并比例为$\rho=0.2$；Pure Cloud消融使用$K=16$和$\alpha=0.10$。生成温度为$1.0$、top-$p=0.95$。Cloud评分构建$R=20$个参考bank，每个bank使用200道带标签题，并设置$q=5$、$\tau=2.0$、$\lambda_{\mathrm{neg}}=1.0$。除另有说明外，DPO使用$\beta=0.10$、学习率$5\times10^{-6}$、有效批量16，最多训练20轮，早停耐心值为5；Cloud–ScPO设置$\lambda_{\mathrm{NLL}}=1.0$。最终测试统一采用贪心解码和精确匹配准确率。计算环境为4张各48 GB显存的NVIDIA A40。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| MATH Level 3与Level 4表示处理流程比较：未归一化的末token隐藏状态，对比回答token均值池化后进行$\ell_2$归一化；每类点云均含$N=200$条轨迹 | 未处理流程的距离尺度范围较大，正确与错误点云的$H_0$条形码重叠明显；均值池化并归一化后，过滤尺度更稳定，正确点云在更小尺度上开始合并，错误点云则在更宽范围内保持碎片化。与此同时，处理后的$H_1$环结构信号变弱。 | 该比较检验作者选定的完整表示处理流程是否能产生更可解释的连通几何，结果支持使用处理后的$H_0$结构构造Cloud组件。它不是严格的单因素消融，因为池化策略与归一化同时改变，且两个流程的距离尺度不同；因此无法判断收益分别有多少来自均值池化或$\ell_2$归一化，也不能直接比较绝对过滤值。 | Figure 2；Appendix A，Representation-processing comparison<br><span class="experiment-evidence">For each subset, we construct correct and incorrect point clouds using the same number of sampled trajectories, with N=200 points in each cloud.</span> |
| $H_0$连通信号与$H_1$环结构信号的稳健性比较 | 均值池化和$\ell_2$归一化后，$H_0$仍保留可解释的正确/错误轨迹连通差异，而$H_1$差异明显减弱且不稳定；因此实际Cloud–ScPO只使用由$H_0$启发的早期连通分量，没有把$H_1$用于轨迹评分或偏好对构造。 | 这一分析隔离的是“哪一类拓扑现象足以支持可操作评分”的设计选择。它说明作者舍弃$H_1$有经验依据，但没有提供把$H_1$加入训练后的性能对照，所以不能得出$H_1$在所有评分设计中都无用；作者也明确把它视为探索性证据。 | Figure 2；Appendix A，Behavior of the H1 signal<br><span class="experiment-evidence">After mean pooling and ℓ2 normalization, the H1 signal becomes considerably weaker and less consistently separated between correct and incorrect trajectories.</span> |

**定性案例**

- Figure 2对MATH Level 3和Level 4代表性子集进行可视化分析：处理后的正确轨迹点云较早合并成连贯分量，错误轨迹较长时间保持分散。直观上，正确解法的隐藏表示更像若干局部密集的“解题模式”，错误解法则来源更杂、方向更分散；但作者明确指出这是代表性子集上的定性观察，不能解释为所有难度等级和模型配置都具有完全相同的拓扑规律。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It proposes hidden-state-geometry-based preference mining for semi-supervised preference optimization of mathematical reasoning trajectories.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`14bed5634d763ce8a7d542929d3b4ee0c82f3ab211797947b11a1b02e48edb92`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
