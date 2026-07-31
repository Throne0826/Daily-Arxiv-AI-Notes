---
title: "[论文解读] Towards Transfer-Efficient Multi-modal Sequential Recommendation with State Space Duality"
description: "[arXiv 2506.02916][推荐系统] 本文针对可迁移多模态序列推荐微调收敛慢的问题，探索以符合序列推荐先验的代数结构约束替代复杂训练策略，并通过序列级对齐、时序衰减与跨模态融合兼顾推荐精度和迁移效率。"
arxiv_id: "2506.02916"
announcement_date: "2026-07-31"
primary_category: "recommender"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.118597+00:00"
source_sha256: "e62b06b014c368ec26db4c376d85f2f57a63773148841a68edad9ea7cf47610f"
tags:
  - "推荐系统"
  - "序列推荐"
  - "多模态推荐"
  - "迁移学习"
  - "状态空间对偶"
  - "跨模态对齐"
  - "时间建模"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">推荐系统 · arXiv 2506.02916</p>

# Towards Transfer-Efficient Multi-modal Sequential Recommendation with State Space Duality

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Fan, Hao, Liu, Qingyang, Liu, Hongjiu, Hu, Yanrong, Fang, Kai</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2506.02916) · [PDF 下载](https://arxiv.org/pdf/2506.02916) · **关键词** 序列推荐, 多模态推荐, 迁移学习, 状态空间对偶, 跨模态对齐, 时间建模<br>
**代码**: [https://github.com/AlwaysFHao/MMM4Rec](https://github.com/AlwaysFHao/MMM4Rec)

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

本文针对可迁移多模态序列推荐微调收敛慢的问题，探索以符合序列推荐先验的代数结构约束替代复杂训练策略，并通过序列级对齐、时序衰减与跨模态融合兼顾推荐精度和迁移效率。

**不用术语来说**：推荐系统需要根据用户依次点击或购买的商品预测下一项行为；商品的文本和图像比平台内部编号包含更通用的语义，因此有望把一个数据集上学到的知识迁移到另一个数据集。然而，同一商品的图像或文本在不同用户、不同时间上下文中的作用并不相同，而且越接近当前时刻的交互通常越能反映用户的最新兴趣。现有模型往往需要复杂的对比学习、负样本设计或额外聚类才能处理这些问题，使预训练模型在新数据上适配较慢，甚至可能因不合适的知识迁移而降低效果。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出以“先对齐、后融合”为核心的可迁移多模态序列推荐框架：通过共享参数的模态投影在序列层面对齐文本、图像与推荐语义，再利用 Time-aware Cross-SSD 和双通道傅里叶自适应滤波建模跨模态时序关系，以减少语义不一致和噪声传播。
- 作者把状态空间对偶性（SSD）的状态转移衰减、全局时间感知及跨模态权重共享组织为符合序列推荐先验的代数约束，使预训练和下游微调可以统一采用简单的交叉熵目标；其目标是在保持多模态检索能力的同时，降低迁移所需的优化复杂度并加快收敛。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

序列推荐（Sequential Recommendation, SR）根据用户按时间排列的历史交互预测下一件物品。传统方法主要以物品ID作为特征，但ID依赖特定平台的交互记录：数据稀疏或新物品缺少交互时难以学习可靠表示，不同平台的ID空间也没有共享语义，因而不利于跨域迁移。多模态序列推荐进一步利用物品的文本、图像等通用内容特征，并通过大规模数据预训练、下游数据微调，使内容语义适配推荐任务；其核心前提是不能直接把静态多模态特征当作用户兴趣，而要结合交互序列的时间上下文，将其转换为与推荐语义一致的动态表示。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多模态序列推荐**

在按时间预测下一物品的基础上，同时使用物品的文本、图像等内容信息。不同模态对用户当前兴趣的作用会随交互上下文变化，因此模型既要对齐模态语义，也要进行序列级融合。

</div>
<div class="concept-item" markdown="1">

**预训练—迁移范式**

模型先在大规模推荐数据上学习如何把通用内容特征转换为推荐相关表示，再在目标数据集上微调。该范式不要求源域和目标域拥有重叠物品，但需要避免源域知识损害目标域表现的负迁移。

</div>
<div class="concept-item" markdown="1">

**状态空间对偶（SSD）**

SSD是结构化状态空间序列模型的一种表述，可利用状态转移随时间衰减的性质建模历史信息。本文关注这一归纳偏置与序列推荐先验的契合：通常较近的交互更能反映用户当前兴趣，因此不同时间位置不应被同等对待。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是用户按时间排列的物品交互序列，以及各物品预先提取的文本、视觉等多模态特征；模型需要从序列上下文中学习用户兴趣表示，并预测下一件可能交互的物品。研究采用先预训练、后迁移微调的设置，假定多模态内容具有跨数据集可复用的通用语义，但这些原始语义尚未与推荐空间对齐。建模时还需处理两项结构性问题：同一物品的模态贡献会因用户及时间上下文而改变，且序列中较近物品通常比早期物品更能代表当前偏好。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **MISSRec**: 与本文最直接相关的可迁移多模态序列推荐方法。它在候选物品侧使用用户特定的模态融合系数，并通过多模态聚类过滤冗余信息；原文认为其不足是忽略用户侧序列级兴趣表示的学习，而且聚类属于启发式、非端到端处理，可能限制微调收敛效率。
- **MMSRec**: 使用自监督对比学习处理视觉与文本之间的跨模态对齐，代表依靠额外训练目标约束多模态推荐表示的路线。原文指出，这类方法计算开销较大，负样本策略难以针对推荐语义设计，且人工构造的复杂优化过程可能减慢新领域上的微调收敛。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在电商和社交平台中，交互稀疏与新商品冷启动会削弱仅依赖商品 ID 的序列推荐模型；不同平台又使用彼此不兼容的 ID 映射，使表示难以跨域复用。文本和图像具有较通用的语义，可缓解这些问题，但工程上仍需让大规模数据预训练得到的多模态推荐器快速适配下游数据，并避免无关或冲突知识造成负迁移。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **跨模态对比学习与复杂约束优化**：这类方法在推荐语义空间中拉近相互匹配的模态或序列表示、推远负样本，并通过额外训练目标约束表示的学习轨迹，以促使通用视觉和文本特征适配推荐任务，同时抑制负迁移与不同模态此消彼长的“跷跷板现象”。
- **MISSRec 的候选侧模态加权与多模态聚类**：MISSRec 在候选商品侧学习用户特定的模态融合系数，并通过多模态聚类去除冗余信息、突出关键商品特征，从而改善模态对齐和有效信息筛选。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 对比学习依赖适合推荐语义的负样本设计，并引入多个约束目标和繁琐优化步骤；作者认为这种人工设计、非端到端的训练范式提高了模型复杂度，限制了预训练模型在下游任务上的快速收敛。
- 现有设计未同时解决序列上下文中的动态模态贡献和交互位置贡献不均：MISSRec 的候选侧融合忽略了从用户交互序列学习兴趣表示的过程，其聚类又割裂端到端训练；Transformer 虽有位置编码，却在初始处理时平等看待各商品的多模态特征，未显式优先保留通常更能代表当前兴趣的近期交互信息。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作尚缺少一种统一、端到端且结构上符合序列推荐规律的机制：它既要在用户序列层面随上下文调整各模态的重要性，又要显式体现近期交互通常更关键的时间偏置，同时不依赖复杂对比目标、负采样或离线聚类，使同一套简单训练目标能够贯通预训练与下游微调。

</div>
<div markdown="1"><span>核心问题</span>

能否把跨模态共享、状态空间模型的时间衰减和全局时序相关性编码为专门的代数结构约束，从而让多模态序列推荐器仅用一致的交叉熵训练，就能有效学习推荐对齐的多模态表示，并在迁移到下游数据时兼顾准确性、抗负迁移能力与快速收敛？

</div>
<div markdown="1"><span>作者直觉</span>

共享投影可把文本和图像先送入同一表示坐标系，减少各模态独立映射造成的语义漂移；随后再做序列级融合，模型便可依据完整交互上下文决定当前更应相信哪种模态。SSD 的状态转移衰减天然让较早信息随时间逐步减弱，符合近期行为通常更能反映当前兴趣的先验；全局时间感知和频域过滤则补充跨较长时间范围的相关性并抑制重复、噪声成分。换言之，作者把原本需要额外损失函数和训练技巧表达的偏好直接写入网络结构，使优化过程更简单，也更可能在下游微调时迅速找到有效表示。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MMM4Rec以用户按时间排序的交互序列、每个物品的图像与文本以及相邻交互时间差为输入，输出下一物品的多模态匹配分数。端到端流程是：先用冻结的ViT与BERT离线提取视觉、文本特征，并以轻量适配器统一到维度$N$；再让两个模态通过参数共享的时间感知状态空间对偶模块TiSSD分别编码，从而在序列层面对齐到推荐语义空间；随后对两路时间信号进行双通道傅里叶滤波，并由交叉模态TiCoSSD融合视觉、文本和时间信息；最后取序列末位置隐状态作为当前用户兴趣，与候选物品的两种模态表示分别做内积并求和。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多模态特征预提取与适配

冻结视觉编码器$\Phi^v$和文本编码器$\Phi^t$，得到特征序列$\boldsymbol{F}^v\in\mathbb{R}^{L\times D_p^v}$与$\boldsymbol{F}^t\in\mathbb{R}^{L\times D_p^t}$；再用模态专属线性适配器$\Psi^v$、$\Psi^t$投影为统一维度的$\boldsymbol{X}^v,\boldsymbol{X}^t\in\mathbb{R}^{L\times N}$。

<div class="method-step__io" markdown="1">

**输入**：交互序列中各物品的原始图像$i_l^v$与文本$i_l^t$。<br>
**输出**：维度一致但尚未直接融合的视觉序列$\boldsymbol{X}^v$和文本序列$\boldsymbol{X}^t$。

</div>

**直观理解**：大编码器负责把图片和文字转成通用语义向量，小适配器只学习如何把这些通用语义改造成适合当前推荐任务的表示。冻结大编码器可以减少迁移时需要更新的参数，而暂不做早期融合可避免一个模态的噪声立即污染另一个模态。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 时间感知的序列级跨模态对齐

两种模态分别进入同一组共享参数的TiSSD；模块把内容生成的步长$\Delta$与经过全局门控、因果卷积增强的时间差$\widehat{\mathcal{D}}$结合，构造具有因果性和状态衰减的结构化掩码$\boldsymbol{L}$，随后通过残差连接、层归一化和各自的前馈网络得到$\boldsymbol{P}^v$与$\boldsymbol{P}^t$。

<div class="method-step__io" markdown="1">

**输入**：两路适配后序列$\boldsymbol{X}^v$、$\boldsymbol{X}^t$，以及由时间戳$\mathcal{T}^{u_k}$计算并归一化的时间差序列$\mathcal{D}$。<br>
**输出**：推荐语义对齐后的视觉序列$\boldsymbol{P}^v$、文本序列$\boldsymbol{P}^t$，以及两路增强时间信号$\widehat{\mathcal{D}}^v$、$\widehat{\mathcal{D}}^t$。

</div>

**直观理解**：共享TiSSD相当于要求图像和文本用同一套“阅读交互历史”的规则，从而减少两种模态各自漂移到不同语义空间的可能。衰减掩码默认更重视近期行为，而真实时间间隔又能保留某些虽较早但时间模式重要的交互。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 双通道时间频谱融合

先用一维FFT将两路信号变换为频谱$\widetilde{\mathcal{D}}^v$和$\widetilde{\mathcal{D}}^t$，分别通过复数值自适应核重加权频率分量；再把两路过滤频谱相加，经可学习复数线性变换和逆FFT得到统一时间信号$\widehat{\mathcal{D}}^f$。

<div class="method-step__io" markdown="1">

**输入**：视觉和文本分支输出的时间信号$\widehat{\mathcal{D}}^v$与$\widehat{\mathcal{D}}^t$。<br>
**输出**：供跨模态状态转移使用的融合时间差表示$\widehat{\mathcal{D}}^f$。

</div>

**直观理解**：频域处理把交互节奏拆成不同快慢的周期成分，使模型能够分别削弱噪声频率、保留两种模态共同支持的时间规律。它融合的是“行为发生节奏”，而不是过早把图像和文本内容简单相加。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### TiCoSSD跨模态融合与兴趣编码

TiCoSSD从视觉分支生成$\boldsymbol{C}$，从文本分支生成$\boldsymbol{B}$、值序列$\boldsymbol{X}$和步长$\Delta$，再以$\widehat{\mathcal{D}}^f$修正状态转移掩码并计算跨模态序列$\boldsymbol{M}$；$\boldsymbol{M}$与两路输入残差相加，经过层归一化和前馈网络形成$\boldsymbol{Y}\in\mathbb{R}^{L\times N}$。

<div class="method-step__io" markdown="1">

**输入**：对齐后的$\boldsymbol{P}^v$、$\boldsymbol{P}^t$和融合时间信号$\widehat{\mathcal{D}}^f$。<br>
**输出**：每个序列位置的统一用户兴趣表示$\boldsymbol{Y}$，其中末位置向量$y_L$作为当前用户表示$u_k$。

</div>

**直观理解**：该结构类似交叉注意力：视觉信息决定“查询什么”，文本信息提供“可匹配的线索和值”，时间掩码限制历史信息如何向后传播。残差连接保留原始两模态信息，避免融合模块覆盖掉已经对齐的有效特征。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### TiSSD时间感知状态空间映射

$$
\widetilde{\boldsymbol{X}},\widehat{\mathcal{D}}=TiSSD\left(\boldsymbol{X},\mathcal{D}\right)\coloneqq\left(\boldsymbol{L}\circ\boldsymbol{C}\overline{\boldsymbol{B}}^{\top}\right)\boldsymbol{X},\qquad \hat{\Delta}=Softplus\left(\Delta\cdot\widehat{\mathcal{D}}\right)+b^{\Delta},\qquad \overline{\boldsymbol{B}}=\hat{\Delta}\cdot\boldsymbol{B}
$$

**符号说明**

- $\boldsymbol{X}\in\mathbb{R}^{L\times N}$：长度为$L$、特征维度为$N$的输入序列
- $\mathcal{D}\in\mathbb{R}^{L}$：由相邻交互时间间隔构造并归一化的原始时间差序列
- $\widehat{\mathcal{D}}$：经过全局门控和局部因果卷积增强的时间信号
- $\Delta,\hat{\Delta}$：内容生成的原始离散化步长及注入时间信息后的步长
- $\boldsymbol{C},\boldsymbol{B}$：SSD中由输入投影产生的状态读取矩阵和状态写入矩阵，可类比为注意力的查询与键
- $\overline{\boldsymbol{B}}$：经时间感知步长离散化后的状态写入矩阵
- $\boldsymbol{L}$：由状态衰减系数和时间感知步长构造的下三角结构化因果掩码
- $\circ$：逐元素乘法，用结构化掩码调制位置间的关联强度
- $\widetilde{\boldsymbol{X}}$：聚合历史信息后的时间感知序列表示

<div class="equation-explanation" markdown="1">

**直观理解**：核心计算先形成类似线性注意力的内容关联$\boldsymbol{C}\overline{\boldsymbol{B}}^{\top}$，再由$\boldsymbol{L}$限制哪些过去位置能够影响当前位置以及影响衰减多少。真实时间间隔通过$\hat{\Delta}$改变状态写入和掩码，因此两个序列位置即使索引距离相同，也可因实际间隔不同而具有不同传播强度；本文随后对视觉和文本调用共享参数的这一映射，以实现序列级语义对齐。<br>
**原文位置**：第3.3.1节，式(6)至式(10)，核心输出为式(10)

</div>

</div>

<div class="equation-block" markdown="1">

#### 统一的预训练与微调交叉熵目标

$$
\ell_{u_k}=-\log\frac{\exp\left(\langle u_k,i_{L_{u_k}+1}\rangle/\tau\right)}{\sum_{i\in\mathcal{C}}\exp\left(\langle u_k,i\rangle/\tau\right)},\qquad \mathcal{C}=\begin{cases}\mathcal{C}_{\mathrm{batch}},&\text{pre-training},\\ \mathcal{I},&\text{fine-tuning}.\end{cases}
$$

**符号说明**

- $u_k=y_L$：用户$u_k$的当前兴趣表示，即融合序列最后一个位置的隐状态
- $i_{L_{u_k}+1}$：用户历史序列之后的真实下一交互物品
- $\langle u_k,i\rangle$：用户表示与候选物品视觉、文本适配表示的两个内积之和
- $\tau>0$：控制softmax分布尖锐程度的温度参数
- $\mathcal{C}_{\mathrm{batch}}$：预训练时由同一小批量中的目标物品组成的候选集合
- $\mathcal{I}$：下游领域的完整物品集合

<div class="equation-explanation" markdown="1">

**直观理解**：该目标提高真实下一物品相对于候选负例的得分。预训练和微调保持相同的交叉熵形式，只改变分母中的候选集合：大规模预训练使用批内负例控制计算成本，小规模下游微调使用全物品集合逼近完整检索；这里的统一写法忠实概括式(22)与式(23)的训练意图，但原文式(22)和式(23)的分母索引记法分别写成用户索引形式，存在候选物品归属不够清晰的问题，复现时应结合实现核对。<br>
**原文位置**：第3.5.1至3.5.3节，候选得分式(21)、预训练目标式(22)、微调目标式(23)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：优化目标只包含下一物品分类交叉熵，不增加跨模态对比损失、重建损失或其他辅助任务。作者的设计逻辑是把推荐先验直接编码进结构约束：共享TiSSD收紧两种模态的语义空间，状态衰减与时间掩码约束历史贡献，TiCoSSD规定跨模态交互方式；因此训练目标只需推动真实下一物品得分超过负例，避免多目标权重平衡造成额外的迁移优化负担。预训练阶段以批内下一物品作为负例集合，微调阶段改为全物品softmax；两阶段均通过温度$\tau$缩放分数。需要注意，原文宣称这种简化目标有助于快速收敛，但仅从方法章节不能单独确认速度增益来自目标、结构约束还是二者共同作用。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 共享参数的时间感知SSD对齐器**

TiSSD将SSD解释为带结构化衰减掩码的线性注意力：$\boldsymbol{C}$、$\overline{\boldsymbol{B}}$和$\boldsymbol{X}$分别对应查询、键和值，$\boldsymbol{L}$控制历史位置之间的因果传播。模型进一步把实际时间差注入离散化步长$\hat{\Delta}$，并让视觉与文本分支共享TiSSD参数；共享约束作用于整个序列编码过程，而非只约束单个物品表示。

> 直观理解：普通参数独立的双分支可能各自学到一套不兼容的推荐规则，后续融合还要重新弥合差异。权重共享直接缩小可选解空间，使两种模态从一开始就按同样的近期偏好和时间间隔规则组织信息，因此作者将其作为加速迁移优化的代数约束。

**2. 双通道傅里叶自适应过滤器**

模块分别对$\widehat{\mathcal{D}}^v$和$\widehat{\mathcal{D}}^t$执行FFT，并通过由输入频谱生成的复数核$\boldsymbol{K}^v$、$\boldsymbol{K}^t$进行逐元素过滤；两路频谱相加后再经过可学习复数变换和逆FFT，输出$\widehat{\mathcal{D}}^f$。复数线性层在实现时拆成实部和虚部的块矩阵运算。

> 直观理解：两种模态对同一段历史可能产生不同的时间信号，直接平均会把规律和噪声一并混合。自适应频率权重让模型先判断每一路中哪些快慢变化值得保留，再生成供融合状态空间模型使用的统一节奏。

**3. 时间感知交叉SSD**

TiCoSSD打破普通TiSSD中$\boldsymbol{C}$、$\boldsymbol{B}$和$\boldsymbol{X}$均由同一输入产生的设置：$\boldsymbol{C}=\boldsymbol{P}^vW_2+b_2$来自视觉序列，而$[\boldsymbol{B},\boldsymbol{X},\Delta]=\boldsymbol{P}^tW_3+b_3$来自文本序列，并以融合时间信号调制状态转移。最终输出再与$\boldsymbol{P}^v$、$\boldsymbol{P}^t$做残差融合。

> 直观理解：结构分工迫使视觉和文本在每个历史位置发生条件化交互，而不是把两个向量机械拼接。SSD掩码同时加入先后顺序、近期偏置和真实时间间隔，使跨模态信息只沿符合序列推荐语义的路径传播。

**训练与推理**

预训练时，先离线使用冻结的$\Phi^v$和$\Phi^t$生成候选物品基础特征，训练轻量适配器、共享TiSSD、傅里叶过滤器、TiCoSSD及打分相关参数。每个用户序列以前缀预测下一物品，末位置$y_L$作为$u_k$，真实下一物品为正例，同批其他目标物品提供负例，并最小化式(22)对应的交叉熵。可选的模态门控物品偏置$\mathbf{E}^v,\mathbf{E}^t\in\mathbb{R}^{|\mathcal{I}|\times N}$可加入相应模态表示，以学习领域内静态物品先验。

迁移到新领域时，保留可迁移的多模态序列建模参数；由于$\mathbf{E}^v$与$\mathbf{E}^t$绑定原领域物品集合，若启用则必须丢弃并在新领域重新学习。微调仍执行相同前向流程，但对完整物品集合计算softmax交叉熵。推理时，对给定用户历史及时间戳计算$u_k=y_L$，将其分别与每个候选物品的视觉适配表示和文本适配表示做内积并求和，再按总分从高到低返回候选；候选的冻结编码器特征可预先离线缓存，在线阶段无需重复运行BERT或ViT。

**复现信息**

复现时最关键的结构条件有四项：视觉与文本编码器使用跨模态预训练版本的ViT和BERT并保持冻结；两个模态先经独立线性适配器统一到维度$N$，但对齐阶段的TiSSD参数必须共享；TiSSD需要以归一化相邻时间差修正离散化步长和结构化因果掩码；TiCoSSD必须由视觉序列生成$\boldsymbol{C}$、由文本序列生成$\boldsymbol{B}$、$\boldsymbol{X}$与$\Delta$，并使用双通道频域模块产生的$\widehat{\mathcal{D}}^f$。SSD可根据序列长度$L$和特征维度$N$选择线性注意力形式或数学等价的平方注意力核：原文给出的复杂度分别为$O(LN^2)$与传统注意力的$O(L^2N)$，但本节未给出具体切换阈值。

源码核对还应关注两处记法问题。第一，式(2)左侧文字说明文本适配器处理$\boldsymbol{F}^t$，右侧最终乘法也使用$\boldsymbol{F}^tW_a^t$，但函数参数被写成$\Psi^t(\boldsymbol{F}^v)$，按上下文应疑似为排版错误，不能据此把视觉特征送入文本适配器。第二，式(9)、式(10)与式(19)的矩阵括号和逐元素乘法排版较含混，特别是$\boldsymbol{L}\circ\boldsymbol{C}\boldsymbol{B}^{\top}(\hat{\Delta}^{\top}\boldsymbol{X})$的维度解释应以作者代码为准；此外式(17)把逆FFT结果标为$\mathbb{C}^L$，而后续时间步长通常应使用实值信号，原文未明确报告是否取实部或利用共轭对称保证实值输出。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 预训练数据来自Amazon Reviews的Food、Home、CDs、Kindle和Movies五个领域，合计1,361,408名用户、446,975个物品和14,029,229次交互，平均序列长度为13.51。它们用于学习可跨领域迁移的多模态序列表示。所有数据经过5-core过滤，即每名用户和每个物品至少保留5次相关交互；文本元数据包括标题、类别和品牌。图像覆盖率仅为21.06%，其中Kindle为0%，因此该设置同时检验模型处理严重模态缺失的能力。
- 下游迁移数据为Scientific、Pantry、Instruments、Arts和Office五个Amazon领域，规模从Scientific的8,442名用户、4,385个物品和59,427次交互，到Office的87,436名用户、25,986个物品和684,837次交互。模型在这些目标领域微调并评估，以检验跨领域迁移质量及收敛效率。作者保留图像缺失物品，与既有工作保持一致；因此主实验更接近不完整多模态数据，而非所有商品都具有图像的理想条件。
- 附录还构造Office完整模态子集：删除图像缺失的物品后重新比较UniSRec、MMSRec、MISSRec、ATHWE和MMM4Rec。该子集专门检验主实验中的性能是否受到低图像覆盖率限制，以及视觉信息完整时多模态迁移是否更有价值；原文未明确报告该子集的用户数、物品数、交互数及具体划分规模。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Recall@$K$，其中$K\in\{10,50\}$**

检查真实下一物品是否出现在模型排名前$K$的候选中，衡量候选集的命中能力。Recall@50比Recall@10允许更宽的推荐列表，因此更侧重模型能否把目标物品召回，而Recall@10要求目标进入更靠前的短列表。 （越高越好，因为更高的值表示真实下一物品更频繁地进入前$K$名。）

</div>
<div class="metric-item" markdown="1">

**NDCG@$K$，其中$K\in\{10,50\}$**

归一化折损累积增益不仅判断是否命中，还按目标物品在前$K$名中的位置给予折损权重；目标排名越靠前，得分越高。因此它比Recall@$K$更敏感于推荐列表内部的排序质量。 （越高越好，因为这表示模型既能召回真实物品，又能将其排在更靠前的位置。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 含ID的多模态迁移：Pantry数据集，MMM4Rec与表2中最佳基线比较。

<div class="result-value" markdown="1">

MMM4Rec在Pantry上取得R@10为0.0984、R@50为0.2127、N@10为0.0481、N@50为0.0729；相对各指标的最佳基线分别提高26.32%、13.44%、31.78%和21.91%。其中N@10从MISSRec的0.0365提升到0.0481，是作者强调的最大代表性增益。

</div>

Pantry具有93.65%的高图像覆盖率，这组结果说明当文本、图像和ID都较充分时，MMM4Rec尤其能改善短推荐列表中的命中与排序。作者将其归因于更完整的多模态偏好建模、序列级语义对齐和时间感知状态空间动态。分析上，高视觉覆盖率与大幅提升同时出现，支持视觉模态可能有帮助，但单个领域的比较不能单独证明图像覆盖率就是增益原因，也不能把收益唯一归因于某个模块。

<div class="result-source" markdown="1">

来源：表2，Pantry四个指标行；第4.2节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Pantry R@10 0.0501 0.0487 0.0504 0.0531 0.0395 0.0444 0.0693 0.0779 0.0495 0.0437 0.0573 0.0984 26.32%; R@50 0.1322 0.1377 0.1360 0.1408 0.1151 0.1315 0.1827 0.1875 0.1407 0.1156 0.1414 0.2127 13.44%; N@10 0.0218 0.0223 0.0229 0.0234 0.0209 0.0214 0.0311 0.0365 0.0222 0.0232 0.0314 0.0481 31.78%; N@50 0.0394 0.0415 0.0411 0.0423 0.0370 0.0400 0.0556 0.0598 0.0418 0.0388 0.0494 0.0729 21.91%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 移除ID的内容迁移：五个下游领域仅使用文本与图像，避免模型依赖目标领域物品ID。

<div class="result-value" markdown="1">

MMM4Rec在表3的20个“数据集-指标”组合中有18个取得严格最优，Scientific的R@10与MISSRec并列；唯一未最优的是Office的N@10，MMM4Rec为0.0859，略低于MMSRec的0.0864。代表性地，在Instruments上，MMM4Rec的R@10、R@50、N@10和N@50分别为0.1293、0.2426、0.0847和0.1092，相对最佳基线提高5.81%、3.54%、9.86%和8.98%。

</div>

不提供ID后，模型不能直接记忆目标领域物品标识，必须依靠可跨领域复用的文本和视觉语义。结果因而更直接地支持MMM4Rec具有内容检索与冷启动式迁移能力，而优势并非完全来自ID嵌入。不过这仍不是严格的新物品冷启动实验：节选没有说明测试物品是否从未出现在微调训练中，而且Office的N@10表明其并非在所有排序指标上都占优。

<div class="result-source" markdown="1">

来源：表3，Instruments四个指标行；第4.2节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Instruments R@10 0.1127 0.1170 0.1150 0.0783 0.1189 0.1222 0.1119 0.1201 0.1293 5.81%; R@50 0.2104 0.2040 0.2084 0.1387 0.2255 0.2343 0.2219 0.2218 0.2426 3.54%; N@10 0.0661 0.0769 0.0741 0.0497 0.0680 0.0758 0.0732 0.0771 0.0847 9.86%; N@50 0.0873 0.0988 0.0940 0.0627 0.0912 0.1002 0.0970 0.0988 0.1092 8.98%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 迁移效率：MMM4Rec与可迁移多模态模型MMSRec、MISSRec在五个下游领域上的早停轮数和每轮耗时比较。

<div class="result-value" markdown="1">

MMM4Rec在五个领域都以最少轮数停止：Scientific、Pantry、Instruments、Arts和Office分别需要13、10、7、5和5轮，而MISSRec分别需要76、32、65、166和153轮。按五个领域简单平均，MMM4Rec约需8轮，MISSRec约需98.4轮，相差约12.3倍；MMM4Rec的单轮耗时也均最低，例如Arts为14.92秒，而MMSRec和MISSRec分别为33.81秒和25.15秒。

</div>

该结果说明MMM4Rec的优势不只是每轮计算更快，更主要来自达到早停条件所需的微调轮数显著减少。作者认为原因是共享权重对齐不需要对比学习目标，时间感知掩码也不需要聚类。这里的“收敛”由早停轮数体现，不能直接等同于达到相同训练损失的理论收敛速度；此外，原文没有给出硬件、批大小、重复运行方差或早停时各模型的验证分数，因此绝对耗时和“约10倍”结论仍需复核。

<div class="result-source" markdown="1">

来源：表4；第4.3节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Scientific epochs 25 76 13; s / epoch 2.72 2.21 2.07; Pantry epochs 20 32 10; s / epoch 6.43 5.97 5.58; Instruments epochs 50 65 7; s / epoch 12.25 10.55 9.08; Arts epochs 67 166 5; s / epoch 33.81 25.15 14.92; Office epochs 52 153 5; s / epoch 33.57 41.06 27.93.

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

- SASRec代表基于Transformer自注意力的经典ID序列推荐器；作者还为其构造文本增强版本。它用于判断性能提升究竟来自多模态迁移设计，还是普通注意力序列建模及加入文本已经足够。
- Mamba4Rec代表基于Mamba状态空间模型的ID序列推荐器，并另有文本增强版本。与它比较可区分“采用Mamba类骨干”本身的收益和MMM4Rec特有的跨模态对齐、时间融合及预训练机制的收益。
- VQRec代表不使用ID、依靠文本语义并支持迁移的推荐器。它是移除ID实验中的关键对照，用于检验MMM4Rec能否仅凭内容模态形成可迁移的物品表示，而不是依赖目标领域的物品ID记忆。
- MISSRec代表可迁移的多模态序列推荐器，是与MMM4Rec输入能力最接近的核心基线；MMSRec还用于迁移效率比较。二者共同检验MMM4Rec提出的共享权重对齐、状态空间时间约束和频域融合是否能同时改善检索质量与微调成本。

**实验想回答的问题**

- RQ1：在五个下游领域中，MMM4Rec相较于利用ID、文本或图像信息的先进序列推荐模型，能否取得更好的下一物品检索效果；这种优势在包含ID和移除ID的公平输入条件下是否都成立？
- RQ2：从预训练模型迁移到下游领域时，MMM4Rec能否用更少的微调轮数和更短的单轮时间收敛，同时保持较高的推荐准确率？

**实验实现**

统一使用SigLip-B/16提取图像与文本特征，再由模态适配器投影到256维潜在空间。MMM4Rec以NAdam优化，学习率为$10^{-4}$，预训练40轮；下游微调采用耐心值为10的早停。Mamba骨干的状态因子为64，一维因果卷积核大小为4，块扩展因子为2；dropout为0.4，时间相关超参数$\tau=0.8$，TiSSD和TiCoSSD均默认堆叠一层。主结果分别在含ID的$T+V+ID$条件和不含ID的$T+V$条件下比较；对原本不使用ID的VQRec、MMSRec等，作者专门移除MMM4Rec的ID相关模态偏置以保持输入一致。表2中的相对提升声称通过$t$检验达到$p<0.05$，但节选未说明随机种子数量、均值与方差、负采样或全量排序方式，也未给出具体数据划分比例。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 组件消融：在Scientific和Office上分别移除预训练、时间感知增强、跨模态共享权重、可学习滤波器或自适应滤波器，并测试两层TiSSD/TiCoSSD。 | 移除预训练造成最稳定且幅度最大的下降：Scientific的R@10由0.1348降至0.1257、N@50由0.1002降至0.0896；Office的R@10由0.1337降至0.1178、N@50由0.1080降至0.0901。移除时间增强、共享权重或任一频域滤波器也普遍降低指标。堆叠两层则在Scientific上退化，但在更大的Office上四项指标均提高，例如N@10由0.0906升至0.0926。 | “w/o PT”直接隔离跨领域预训练的贡献，结果表明预训练是迁移性能的主要来源，而其余变体检验时间先验、跨模态约束和双阶段频域融合是否各有增量价值。两层模型在小型Scientific上变差、在大型Office上变好，支持作者关于数据规模与过拟合的解释，但只有两个领域，尚不能确立一般性的深度选择规律。各消融一次只移除一个设计，却未报告多组件联合消融，因此不能判断模块之间是否存在替代或协同效应。 | 表5；第4.4节<br><span class="experiment-evidence">(0) MMM4Rec 0.1348 0.2627 0.0724 0.1002 0.1337 0.2132 0.0906 0.1080; (1) - w/o PT 0.1257 0.2399 0.0647 0.0896 0.1178 0.1868 0.0751 0.0901; (2) - w/o Time 0.1328 0.2559 0.0696 0.0965 0.1329 0.2128 0.0895 0.1069; (3) - w/o Shared 0.1294 0.2521 0.0685 0.0955 0.1331 0.2124 0.0897 0.1069; (4) - w/o LF 0.1303 0.2592 0.0685 0.0968 0.1314 0.2090 0.0886 0.1056; (5) - w/o AF 0.1317 0.2517 0.0687 0.0949 0.1310 0.2083 0.0891 0.1060; (6) - 2L 0.1309 0.2544 0.0698 0.0969 0.1343 0.2140 0.0926 0.1101.</span> |
| 受控注意力替换：保留原有投影、对齐和融合流程，仅用标准自注意力替换TiSSD、用交叉注意力替换TiCoSSD，并以注意力掩码取代状态空间衰减和时间感知掩码。 | 原模型在Scientific、Office、Instruments和Arts的全部16个“数据集-指标”组合上都优于注意力替换版。差距在Arts最明显：R@10从0.1307降至0.1109，R@50从0.2486降至0.2062，N@10从0.0777降至0.0662，N@50从0.1034降至0.0869；Instruments的R@50也从0.2525降至0.2233。 | 该实验控制了外围投影与融合结构，因此比简单删除模块更能检验收益是否来自状态空间时间约束本身。结果支持TiSSD/TiCoSSD中的近期行为衰减、远距离重要行为时间修正和跨模态时间结构并非可由标准注意力直接等价替代。不过替换版的参数量、计算量和调参预算未报告，故仍不能完全排除模型容量或优化适配差异。 | 附录C，表7<br><span class="experiment-evidence">Scientific MMM4Rec 0.1348 0.2627 0.0724 0.1002; Attention replacement 0.1310 0.2503 0.0695 0.0955; Office MMM4Rec 0.1337 0.2132 0.0906 0.1080; Attention replacement 0.1236 0.1959 0.0851 0.1009; Instruments MMM4Rec 0.1330 0.2525 0.0822 0.1082; Attention replacement 0.1209 0.2233 0.0751 0.0976; Arts MMM4Rec 0.1307 0.2486 0.0777 0.1034; Attention replacement 0.1109 0.2062 0.0662 0.0869.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The central contribution is a transfer-efficient multimodal architecture for sequential recommendation.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`e62b06b014c368ec26db4c376d85f2f57a63773148841a68edad9ea7cf47610f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
