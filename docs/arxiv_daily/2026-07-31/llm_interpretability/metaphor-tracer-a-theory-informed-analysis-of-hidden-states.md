---
title: "[论文解读] Metaphor Tracer: A Theory-Informed Analysis of Hidden States"
description: "[arXiv 2607.28434][LLM 机制与可解释性] 本文尝试把关于“文本意义取决于符号在具体文本中的关系位置”的理论主张转化为可检验问题：能否从语言模型一次前向传播的隐藏状态几何中，无训练地识别某个位置对全文的聚合与对其他词元的隐喻式迁移。"
arxiv_id: "2607.28434"
announcement_date: "2026-07-31"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.082944+00:00"
source_sha256: "679382983a864521937aac952ce3f49737d4fb8333048168a12515903212ef35"
tags:
  - "LLM 机制与可解释性"
  - "隐藏状态可解释性"
  - "残差流"
  - "单文本关系结构"
  - "aggregator"
  - "differentiator"
  - "各向异性"
  - "缝合点"
  - "隐喻性迁移"
  - "训练免费分析"
  - "单次前向传播"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2607.28434</p>

# Metaphor Tracer: A Theory-Informed Analysis of Hidden States

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Heimann, Marc, Moghaddam, Roxana Assadi, Brovkina, Olga, Pettifor, Mark, Goetzmann, Lutz</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.28434) · [PDF 下载](https://arxiv.org/pdf/2607.28434) · **关键词** 隐藏状态可解释性, 残差流, 单文本关系结构, aggregator, differentiator, 各向异性, 缝合点, 隐喻性迁移, 训练免费分析, 单次前向传播<br>


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

本文尝试把关于“文本意义取决于符号在具体文本中的关系位置”的理论主张转化为可检验问题：能否从语言模型一次前向传播的隐藏状态几何中，无训练地识别某个位置对全文的聚合与对其他词元的隐喻式迁移。

**不用术语来说**：同一个词出现在不同文本甚至同一文本的不同位置时，可能承担完全不同的结构作用，例如标题、反复出现的名字或收束段落的句号可能成为组织全文的支点。常见分析往往关注模型最终输出、词本身的一般属性或跨语料平均规律，却不容易说明模型在阅读某一篇具体文本时如何形成其独有的内部组织。作者因此希望直接检查一次阅读过程中各词元位置之间形成的几何关系，并判断这种关系是否与事先独立给出的人类专家标注一致。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 将先前关于“缝合话语的锚点”和“隐喻式迁移”的理论解释首次操作化为可证伪的隐藏状态分析问题，并把已有几何分析工具组合成一个面向单篇文本、单次前向传播且无需训练的测量框架。
- 提出关系性的检验视角：不把结构价值视为某个词向量固有且可随词汇类型稳定迁移的属性，而考察它是否由词元在当前文本中的位置及其与其他词元的关系产生，并以工程构造和独立专家标注作为确认性依据。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型隐藏状态可解释性研究，但关注点不是解释模型为何生成某个答案，也不是从大规模语料中归纳一般性的语言特征，而是分析模型在一次前向传播中如何组织一篇具体文本。其基本立场是：同一个词在不同文本中的结构作用可能不同，因此研究对象应是词元在当前文本内部与其他词元形成的关系几何。作者把 Transformer 各层残差流中的隐藏状态视为这种“阅读结构”的载体，并借用拉康理论中的“缝合点”和“隐喻”概念，为可测量的两类结构现象提供解释框架。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**隐藏状态与残差流**

隐藏状态是模型处理每个词元时产生的向量表示；残差流则是在 Transformer 各层之间持续传递并更新这些表示的主通道。本文从一次前向传播产生的隐藏状态几何中读取文本内部的结构，而不分析最终生成结果。

</div>
<div class="concept-item" markdown="1">

**各向异性表示空间**

各向异性表示空间指隐藏向量并非均匀分布于所有方向，而是集中在某些共同方向或子空间中。因此，同一结构需要从不同几何视角观察，以免把空间的整体偏置误认为某个词元特有的文本作用。

</div>
<div class="concept-item" markdown="1">

**缝合点与隐喻性迁移**

拉康理论中的“缝合点”指能够回溯性固定话语意义、组织整段文本的关键能指；本文用 aggregator 通道操作化这种锚定作用。“隐喻”在其词源意义上被理解为搬运或迁移，本文用 differentiator 通道检测其他词元是否在阅读过程中暂时进入某个锚点的子空间。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一篇经过词元化的单独文本以及语言模型对该文本执行一次前向传播后得到的逐层隐藏状态。方法无需训练探针或微调模型，而是为每个词元位置计算两类分数：aggregator 判断该位置是否将全文关系汇聚为围绕一个锚点的稳定构型，differentiator 判断其他词元是否被暂时带入该锚点对应的子空间；两类通道均从各向异性空间的两个视角读取。研究假设隐藏状态中的结构价值是上下文关系属性，而非词汇类型或单个向量固有的属性；仪器常数仅在一篇发现文本上确定，此后的文本与模型用于确认性检验。输出不是生成决策的重要性解释，而是当前模型对这篇特定文本形成的逐位置、逐深度关系结构。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Heimann and Hübener (2024)**: 该理论工作比较拉康语言理论与 Transformer 的架构及数学原则，提出模型的“理解”可能具有可描述的话语结构，但当时没有相应测量工具；本文将其中的缝合点、隐喻性迁移等主张首次操作化并置于可证伪检验之下。
- **Heimann and Hübener (2025)**: 该工作进一步发展了前述理论解释，为本文把模型内部几何视为一种具体文本阅读结构提供概念基础；本文的新增部分是构造无需训练的测量仪器，并将理论命名的结构与工程化及专家标注的独立真值进行比较。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

这里的需求主要是科学解释而非直接应用：研究者需要描述语言模型如何在一次前向传播中组织一篇具体文本。目标对象不是模型最后作出的预测，也不是需要归因的某项决策，而是残差流中形成的、属于这一次阅读的内部参照结构。若缺少相应测量手段，就无法检验哪些词元位置成为统摄全文的锚点、哪些位置体现其他词元向其子空间的暂时迁移，也无法将这些内部结构与独立的人类阅读判断进行比较。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **面向输出决策的可解释人工智能方法**：这类方法通常从模型输出或某个具体决策出发，追查输入成分或内部表示对该结果的影响，以解释模型为何产生该预测。本文则把分析对象前移到模型阅读文本时形成的隐藏状态结构，而不要求先指定一个待解释的输出决策。
- **基于隐藏状态、嵌入或语料聚合统计的表示分析**：这类研究通过向量、注意力、隐藏状态几何或跨样本统计来刻画模型内部信息；其中词嵌入已体现符号由其与其他符号的相对位置来确定。作者希望进一步保留单篇文本内每个词元在空间与网络深度上的轨迹，而不是把个别阅读事件平均成语料层面的低分辨率规律。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 以最终输出或决策为中心的解释不能直接回答“模型如何把这一篇文本组织成一个独特整体”；其后果是文本内部的锚定、回溯性意义固定以及位置间迁移容易被当作中间噪声，而非独立研究对象。
- 既有理论工作只通过哲学原则、Transformer 架构与数学性质的比较，提出语言模型内部应存在可描述的话语结构，却没有测量装置；同时，依赖跨语料平均或词汇类型稳定属性的分析可能抹去词元在当前文本中的关系性价值，因此相关理论主张此前难以被确认或证伪。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究之间缺少一座可操作的桥梁：一端是关于锚点、隐喻迁移和符号关系位置的文本理论，另一端是Transformer隐藏状态的可观测几何。尚无经过冻结、无需额外训练的统一测量方案，能够在单篇文本的一次前向传播中逐位置读取这些结构，并用工程上已知的文本结构及事先独立形成的专家标注进行确认性检验。

</div>
<div markdown="1"><span>核心问题</span>

语言模型隐藏状态中是否存在可重复测量的两类关系结构——聚合全文的锚定作用与其他词元向锚点子空间的迁移作用——并且这些结构能否跨模型、文本和几何视图稳定出现，与独立专家判断对齐，同时表现为当前语篇中的位置属性而非词汇类型自身携带的固定属性？

</div>
<div markdown="1"><span>作者直觉</span>

Transformer在阅读时不断把上下文写入各位置的残差表示，因此某些位置若持续吸收并稳定全文关系，其周围几何应呈现“把文本收拢到一个配置中”的迹象；若其他词元在处理过程中短暂进入某个位置所张成的子空间，则几何轨迹应留下“被搬运过去”的迹象。与其询问单个向量本身含有什么，作者考察向量在当前文本全部位置和网络深度中的相对变化：就像一个词是否为文章支点不能只看词典释义，而要看全文如何围绕它重新组织。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Metaphor Tracer 是一种无需训练的单文本隐藏状态分析流程。给定文本和因果语言模型，它通过一次教师强制前向传播提取各层残差流状态，逐一把每个有效词元位置视为候选“锚点”，依据首层到末层的跨词元交互增长为该锚点选出专属核心子空间；随后沿网络深度追踪其他词元何时进入该子空间，并据此计算两个互补通道：区分器衡量阅读过程中发生的暂时性“运输”，聚合器衡量末层中该位置能否承载整篇文本的高秩稳定构型。输出是每个词元、每个视图下的原始通道分数、强锚点及其沿文本位置形成的结构图谱，而不是类别预测或生成结果。
技术上，该方法强调分数是关系性的：锚点的意义取决于它与当前文本全部词元的几何关系，而非其隐藏向量单独携带的固定属性。直观地说，系统先为每个位置找一组“最能体现它如何与全文共同变化的坐标”，再观察哪些词元曾被吸入这些坐标，以及最终全文能否在其中展开成丰富结构；前者像记录阅读途中发生过的临时结盟，后者像寻找能够把一段或整篇文本“钉住”的组织节点。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 提取逐层隐藏状态并建立词元池

在 float32 下执行一次无采样、教师强制的确定性前向传播，保存 $h\in\mathbb{R}^{L\times T\times d}$，其中 $h_\ell(t)$ 是词元 $t$ 经过第 $\ell$ 个 Transformer 块后的残差流状态。分析池排除特殊词元和纯分词器空格标记，但保留标点与分隔符。

<div class="method-step__io" markdown="1">

**输入**：一个已经分词的单篇文本、指定的因果 Transformer 模型，以及长度为 $T$ 的相同词元序列。<br>
**输出**：带模型与张量来源信息的逐层隐藏状态，以及可参与锚点统计的词元位置集合。

</div>

**直观理解**：这一步相当于拍下模型阅读文本时每一层的“内部快照”。保留标点很重要，因为段落末尾等分隔符可能正是模型汇聚片段结构的位置。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 为每个候选锚点构造核心子空间

对每个隐藏维度计算锚点与其他词元的逐元素乘积从首层到末层的中位增长 $\Delta_j(a)$，按增长降序排列；取覆盖正增长总质量 $\mu=0.7$ 的最短维度前缀作为 $\mathrm{dims}(a)$。只归一化正质量，以避免正负增长相互抵消而使子空间退化。

<div class="method-step__io" markdown="1">

**输入**：候选位置 $a$、池中其他词元的首层状态 $h_1(i)$ 与末层状态 $h_L(i)$。<br>
**输出**：每个位置专属的核心维度集合 $\mathrm{dims}(a)$ 及其大小 $k=|\mathrm{dims}(a)|$。

</div>

**直观理解**：不是给所有词元使用同一组坐标，而是为每个候选位置挑出最能描述“它与全文关系如何增强”的坐标。所需维度可多可少，因此 $k$ 本身也反映锚点结构的集中或分散程度。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 沿深度追踪招募并形成盆地

在 $\mathrm{dims}(a)$ 上计算每层中词元 $i$ 与锚点 $a$ 的余弦相似度，首次达到阈值 $\tau_\ell$ 时记录招募层，之后跌破阈值时记录丢失层；锚点盆地定义为任意深度曾越过阈值的全部词元。操作视图固定使用 $\tau=0.7$，安静维度视图则按层使用该层余弦分布的第 $95$ 百分位阈值。

<div class="method-step__io" markdown="1">

**输入**：锚点 $a$、其核心子空间 $\mathrm{dims}(a)$，以及所有池内词元在每一层的隐藏状态。<br>
**输出**：每个锚点的招募层、丢失层、逐层成员轨迹，以及“曾被招募”词元组成的盆地。

</div>

**直观理解**：盆地记录的是模型阅读途中曾与锚点短暂对齐的词元，而不要求这种关系一直保持到最后。它因此更像阅读过程的轨迹，而不是末层的一张静态合影。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 计算双通道分数与双几何视图

区分器比较盆地成员与非成员有多少深度位移能量落入锚点子空间，并乘以锚点自身的子空间位移比例；聚合器则计算末层词元在该子空间内、经词元中心化后的奇异值参与率，再除以隐藏维度 $d$。整套扫描分别在原始状态的操作视图和逐层逐维 z 标准化的安静维度视图中执行，并把两者差异作为结构信号而非误差。

<div class="method-step__io" markdown="1">

**输入**：每个锚点的核心子空间、盆地、首末层状态，以及末层全部池内词元的状态。<br>
**输出**：每个锚点在两个视图下的区分器与聚合器原始分数，以及各通道文本内前 $10\%$ 的强锚点并集。

</div>

**直观理解**：区分器问“哪些词元在阅读途中被明显带进了这个位置的领地”，聚合器问“全文最终能否在这个位置的领地中展开成丰富而稳定的形状”。双视图则分别保留模型实际使用的高方差方向和压低这些主导方向后的细微结构。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 锚点交互增长与核心子空间选择

$$
\Delta_j(a)=\operatorname*{median}_{i\in P,\,i\neq a}\left[h_L(i)_j h_L(a)_j-h_1(i)_j h_1(a)_j\right],\qquad \mathrm{dims}(a)=\operatorname*{argmin}_{S_m}\left\{m:\sum_{j\in S_m}\max(\Delta_j(a),0)\geq \mu\sum_{j=1}^{d}\max(\Delta_j(a),0)\right\}
$$

**符号说明**

- $a$：当前接受评估的候选锚点词元位置。
- $P$：排除特殊词元和纯空格标记后的分析词元池。
- $i$：词元池中除锚点外的其他词元位置。
- $j$：隐藏状态的第 $j$ 个维度。
- $h_\ell(i)_j$：词元 $i$ 在第 $\ell$ 个 Transformer 块后残差流状态的第 $j$ 维分量。
- $L$：模型 Transformer 块的总层数，因而 $h_L$ 表示末层状态。
- $\Delta_j(a)$：维度 $j$ 上，锚点与其他词元逐元素乘积从首层到末层的中位增长。
- $S_m$：将 $\Delta_j(a)$ 从大到小排序后取得的前 $m$ 个维度集合。
- $\mu$：正增长质量覆盖阈值，论文固定为 $0.7$。
- $\mathrm{dims}(a)$：覆盖至少 $\mu$ 比例正增长质量的最短排序前缀，即锚点核心子空间。
- $d$：模型隐藏状态的总维数。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分先看每个维度中，锚点和全文典型词元的共同激活是否从浅层到深层增强；使用中位数是为了描述典型关系而降低极端词元的影响。第二部分只累计正增长，并选择达到 $70\%$ 正质量所需的最少维度，使每个锚点获得大小可变、由当前文本决定的专属子空间。<br>
**原文位置**：Methods，Anchor construction

</div>

</div>

<div class="equation-block" markdown="1">

#### 区分器与聚合器双通道

$$
p_i(a)=\frac{\sum_{j\in\mathrm{dims}(a)}\left(h_L(i)_j-h_1(i)_j\right)^2}{\left\lVert h_L(i)-h_1(i)\right\rVert_2^2},\qquad D(a)=\max\left(0,\frac{1}{|B_a|}\sum_{i\in B_a}p_i(a)-\frac{1}{|P\setminus B_a|}\sum_{i\in P\setminus B_a}p_i(a)\right)p_a(a),\qquad A(a)=\frac{\left(\sum_r\sigma_r(X_a)\right)^2}{d\sum_r\sigma_r(X_a)^2}
$$

**符号说明**

- $p_i(a)$：词元 $i$ 从首层到末层的总位移能量中，落在锚点 $a$ 核心子空间内的比例。
- $B_a$：锚点 $a$ 的盆地，即在任意层曾达到招募阈值的池内词元集合。
- $P\setminus B_a$：词元池中从未被锚点 $a$ 招募的词元集合。
- $p_a(a)$：锚点自身的深度位移落入其核心子空间的比例。
- $D(a)$：锚点 $a$ 的区分器强度；若盆地或其补集为空，原文规定该分数置零。
- $X_a$：末层全部池内词元在 $\mathrm{dims}(a)$ 上的状态矩阵，并已沿词元维度中心化。
- $\sigma_r(X_a)$：中心化矩阵 $X_a$ 的第 $r$ 个奇异值。
- $A(a)$：锚点 $a$ 的聚合器强度，即奇异值参与率除以完整隐藏维度 $d$。
- $d$：模型隐藏维度，用于把聚合器有效秩归一化为容量份额。

<div class="equation-explanation" markdown="1">

**直观理解**：区分器先计算每个词元的深度变化有多少进入锚点子空间，再比较曾被招募者与未被招募者的平均比例；只有盆地成员更明显地进入该空间且锚点自身也沿该空间移动时，$D(a)$ 才高。聚合器用奇异值参与率估计末层全文在该子空间内占据多少彼此独立的方向：方向越丰富、越不被单一轴支配，$A(a)$ 越高，但论文也提醒它与子空间大小 $k$ 高度相关。<br>
**原文位置**：Methods，Two channels

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。Metaphor Tracer 不训练探针、不微调语言模型，也没有通过损失函数优化参数；模型权重、阈值规则和发现阶段冻结的常数均保持不变。这里的“分数”是对固定隐藏状态进行确定性几何计算的结果，不应被解释为模型学习目标、分类概率或因果效应。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 关系性锚点与自适应核心子空间**

每个词元位置都独立成为候选锚点，$\mathrm{dims}(a)$ 由该锚点与当前文本其他词元的首末层交互增长决定，而非使用固定探针、全语料主成分或预先指定维度。子空间大小 $k$ 不固定，并通过覆盖 $70\%$ 正增长质量的规则自适应确定。

> 直观理解：同一个词在不同文本位置可以得到不同子空间和分数，因为方法测量的是它在这篇文本中的组织作用。这正是作者所说的“关系性而非本质主义”设计。

**2. 招募盆地与处理／终态双通道**

盆地采用 ever-recruited 定义，把任何中间层曾达到相似度阈值的词元保留下来；区分器建立在这一跨层集合上，因此属于处理过程指标，而聚合器只使用末层中心化构型的有效秩，因此属于终态整合指标。两者不应合并为单一显著性分数。

> 直观理解：一个位置可能在阅读途中短暂吸引某些词元，却不负责最终整合全文；也可能很少产生这种临时吸引，却成为稳定的段落支点。两个通道分别保存这两种不同作用，避免把动态过程和最终结构混为一谈。

**3. 操作视图与安静维度视图**

操作视图直接使用原始残差流及固定阈值 $\tau=0.7$，保留 Transformer 实际计算所依赖的各向异性；安静维度视图先在每层按文本词元对各维做 z 标准化，再以该层余弦分布第 $95$ 百分位设定 $\tau_\ell$。作者不删除所谓异常高方差维度，而是报告每项发现由哪个视图承载，并把边界对齐反转等视图分歧视作信息。

> 直观理解：前一视图像在模型原本的声场中观察，响亮方向会主导结果；后一视图把每个方向音量拉齐，以便听见低方差的细节。两张地图回答不同问题，不能把其中一张简单称为去噪后的真相。

**训练与推理**

核心推理流程对每篇文本执行一次教师强制、无采样的状态提取，随后离线遍历全部有效词元作为候选锚点，构造核心子空间、追踪逐层招募并计算双通道。若需要预测熵和真实词元惊异度，则在完全相同且经过词表一致性检查的词元序列上进行第二次教师强制前向传播并启用语言模型头；注意力显著性控制另用第三次前向传播获取完整注意力张量，但不参与冻结的核心通道计算。
论文主体比较 phi-4、Qwen3-8B 与 Llama-3.1-8B，并以同谱系的 Llama-3.1-8B-Instruct 作为单独随访，用相同文本、常数和标注重新运行流程；随访结果不进入三模型的合并统计或复现计数。所有分数首先保留原始值，展示时才在单次运行的扫描词元内进行中位数映射为 $0$、第 $95$ 百分位映射为 $1$ 的截断对比归一化，且绝不跨模型归一化。

**复现信息**

主体模型为 microsoft/phi-4（14B，$L=40$，$d=5120$）、Qwen/Qwen3-8B（8B，$L=36$，$d=4096$）和 meta-llama/Llama-3.1-8B（8B，$L=32$，$d=4096$）；匹配谱系随访使用 meta-llama/Llama-3.1-8B-Instruct。嵌入层不计入层编号，$\ell=1$ 指第一个 Transformer 块输出，$\ell=L$ 指末层；核心默认值为质量阈值 $\mu=0.7$、操作视图招募阈值 $\tau=0.7$、强锚点通道分位数 $0.90$。
状态与地平线计算采用 float32；只有需要完整注意力张量的事后显著性控制因显存约束使用 bfloat16 和 eager attention。缓存按文本和模型标识，并在隐藏状态重新提取或聚合器定义标签不一致时拒绝复用；论文给出的公开代码仓库为 https://github.com/HermeneuticAI/MetaphorTracer，但该分析仍应结合原始代码与发布工件复核。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 工程化文本：由作者预先设计、结构边界已知的受控材料，用作可验证的结构真值。论文以文本、模型和几何视图组成的单元报告边界方向是否复现；所给节选明确报告相关结果覆盖 $6/6$ 个单元，但未完整列出文本名称、长度及划分。
- 临床访谈转录：由精神分析专家在该测量工具出现之前完成标记，用作独立专家真值，检验 aggregator 是否对应单篇临床话语中的结构位置。节选报告总体比较涉及 $36$ 个单元；患者数量、转录长度和训练、验证、测试划分原文未明确报告。
- 执行轨迹领域表格：由领域专家声明信息所在的列，用作不同于临床文本的第二类专家真值，检验方法能否在结构化技术材料中定位有组织作用的信息列。数据规模、具体表格数量及逐项结果在所给节选中原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**方向一致单元数**

在预先规定的文本、模型、几何视图组合中，统计效应方向与真值预测一致的单元数，例如 $6/6$ 或 $34/36$。论文强调按独立复现单元计数，而不是只报告汇总后的单个显著性值。 （越高越好，因为更多独立单元保持同一预期方向，意味着结论对模型、文本或视图变化更稳定；但它不等同于效应大小，也不能替代置信区间。）

</div>
<div class="metric-item" markdown="1">

**组间分数增量**

比较专家标记位置与词汇控制位置的 aggregator 分数，并考察标记强度是否对应分数的分级上升。它测试专家判断所包含的信息是否超出词本身可解释的部分。 （专家标记组相对控制组的正向增量越大、且随标记等级单调增加越好，因为这更符合结构性专家真值；所给节选未提供完整效应量定义。）

</div>
<div class="metric-item" markdown="1">

**跨语境迁移或稳定性**

比较相同词汇类型、原始隐藏状态或通道排序在文本编辑及语境变化后的相似程度，以区分表示本身的稳定性与从表示中读取的结构价值稳定性。 （该指标没有脱离对象的统一优劣方向：原始隐藏状态相似度高表示表示稳定，而 aggregator 的类型迁移较低、同时对当前文本真值拟合较高，才支持结构价值依赖具体语境的假设。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 已知边界的工程化文本

<div class="result-value" markdown="1">

作者报告 aggregator 在全部 $6/6$ 个评估单元中跟随工程化文本的 register 边界，说明预先规定的结构变化在所测模型和视图组合中方向一致。

</div>

通俗地说，文本在哪里被人为设计成换段、换语域或换组织方式，aggregator 就在相应位置表现出预期变化。这是受控条件下的结构恢复证据，但只证明该工具能识别这批预先设计的边界，不能单独证明它恢复了任意自然文本的完整意义结构。

<div class="result-source" markdown="1">

来源：Abstract；结果路线概述指向 Results §1–§4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

That this tracks a reading rests on independent ground truth: an engineered register the aggregator follows across its boundaries (6/6 cells), and a psychoanalyst’s marking of clinical transcripts, fixed before the instrument existed, in 34/36 cells, with a graded increment above lexical controls and dissociations no type-level measure reproduces.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 精神分析专家预先标记的临床访谈转录

<div class="result-value" markdown="1">

作者报告 aggregator 与专家标记在 $34/36$ 个评估单元中方向一致，并且相对于词汇控制呈分级增量。

</div>

这意味着分数与独立专家在具体话语中标出的结构位置高度一致，而且这种对应不能完全由被标记词汇本身解释。它支持该通道读取了语境关系，但不证明精神分析标注是唯一正确解释，也不证明跨专家一致性，因为节选说明该语料只有一名标注者。

<div class="result-source" markdown="1">

来源：Abstract；结果路线概述指向 Results §5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

That this tracks a reading rests on independent ground truth: an engineered register the aggregator follows across its boundaries (6/6 cells), and a psychoanalyst’s marking of clinical transcripts, fixed before the instrument existed, in 34/36 cells, with a graded increment above lexical controls and dissociations no type-level measure reproduces.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 三个模型上的重复词元、类型迁移及匹配的 base/instruct 模型比较

<div class="result-value" markdown="1">

作者报告重复出现时，词元的惊讶度与注意力下降而 aggregator 保持；同时，词元结构最容易随词汇类型迁移的模型，对单篇话语的拟合最差。在匹配的 base/instruct 模型对中，指令调优提高真值拟合，却没有改变类型迁移。

</div>

这些解离表明 aggregator 不只是难预测程度、注意力大小或词的固定标签。更合理的解释是，它描述词元在这篇文本关系网络中的位置。base/instruct 对照还提示，指令调优可能改善结构读取质量，而不必把结构变成更固定的词汇属性；但节选没有提供完整模型名和效应量，因此不能据此断言所有指令调优都会产生同样结果。

<div class="result-source" markdown="1">

来源：Abstract；结果路线概述指向 Results §6，重复词元及注意力控制另见 Results §5、§8

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A transfer test gives the result its shape: the model whose token structure travels with lexical type reads the singular discourse worst, and in a matched base/instruct pair tuning raises fidelity without moving type-transfer.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给 source excerpt 在后半部分存在大段字符转写损坏，且缺少完整表格、模型名称与统计检验，因此所有来自损坏段落的数值均需要对照论文 PDF 复核。
- 以上是需经原文核查的详细 AI 草稿；凡节选未明确提供的数据规模、效应量、置信区间或显著性检验，均未作推断。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 词汇类型层面的静态预测量或 lexical controls：检验高分是否只是某些词本身具有固定属性，而不是该词元在当前文本中的关系位置；这是临床专家标注比较所需的主要混淆控制。
- 词元惊讶度：衡量当前词元在其前缀条件下有多难预测，用于排除 aggregator 只是传统信息量或不可预测性的替代指标。
- 注意力量或 attention received：衡量词元吸收了多少注意力，用于排除 aggregator 只是显著性、注意力汇聚或 attention sink 的替代指标。
- 隐藏状态或词汇类型的跨文本迁移稳定性：比较原始表示、结构分数与词汇类型在语境变化后的保持程度，用于检验结构价值究竟随词本身迁移，还是依赖当前文本关系。

**实验想回答的问题**

- 在不训练探针、仅执行一次前向传播的条件下，aggregator 分数能否恢复单篇文本内部的组织结构，并与预先独立确定的人工结构或专家标注一致？
- aggregator 所测量的是词元在当前文本中的关系性位置，还是可由词汇类型、惊讶度、注意力或隐藏状态本身的跨语境稳定性解释的固有属性？

**实验实现**

作者在单篇发现文本上冻结常数，随后将其他材料作为验证性实验；每篇文本只做一次前向传播，不训练额外探针。系统从各层 residual stream 中为每个词元位置构造以该位置为 anchor 的子空间几何，并输出 aggregator 与 differentiator 两个通道；各通道又在保留各向异性的两种互补几何视图中评估。实验跨三个彼此无关的模型进行，并以模型、文本、视图组成的单元统计复现方向。全文共使用 $13$ 篇人工精选文本并生成超过 $40$ GB 的 float32 激活与逐 anchor 几何数据，但节选未提供模型名称、层选择、硬件、随机种子或完整统计检验细节。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 惊讶度与注意力残差控制 | 作者比较重复词元上的 aggregator、惊讶度和注意力，并进一步对注意力进行残差化；所给节选称惊讶度和注意力随重复衰减，而 aggregator 的对齐在控制注意力后仍保持，但完整数值与统计表原文未明确报告。 | 该控制隔离了“一个位置得分高只是因为模型更关注它或更难预测它”的解释。控制后仍有对齐，支持 aggregator 提供额外结构信号；但残差控制只能排除已建模的注意力成分，不能排除所有潜在混淆因素。 | Abstract；相关控制指向 Results §5、§8<br><span class="experiment-evidence">Across three unrelated models, as a signifier repeats, its surprisal and its attention drain while its aggregator score holds: the channel marks a token’s place in the text.</span> |
| 匹配的 base/instruct 模型对照 | 在架构匹配的基础模型与指令模型之间，作者报告指令调优提高了结构真值拟合，但没有改变词汇类型迁移。 | 这个对照尝试把指令调优的作用与架构差异分开：若拟合提高而类型迁移不变，则“读得更准”不等于“把结构更牢地绑定到词本身”。不过，节选没有给出模型名称、样本量和数值差异，因而目前只能接受方向性结论。 | Abstract；Results §6<br><span class="experiment-evidence">A transfer test gives the result its shape: the model whose token structure travels with lexical type reads the singular discourse worst, and in a matched base/instruct pair tuning raises fidelity without moving type-transfer.</span> |

**定性案例**

- 工程化异常段落被设计为高信息性但在篇章中没有稳定位置。作者报告该段的预测熵约为 $0.63$–$0.67$、词惊讶度约为 $0.63$–$0.65$，在三个模型中均高于机会水平，而 aggregator 仅约为 $0.17$–$0.32$、均低于机会水平；静态词汇预测量约为 $0.49$–$0.54$。其解释是：异常内容虽然出人意料，却没有被整合进文本结构，因此“信息多”与“组织地位高”发生分离。由于相应原文在所给节选中出现字符转写损坏，这些数值必须回查 Results §4 后方可正式引用。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper analyzes language-model hidden states with token-level measures intended to reveal text-specific structural representations.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`679382983a864521937aac952ce3f49737d4fb8333048168a12515903212ef35`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
