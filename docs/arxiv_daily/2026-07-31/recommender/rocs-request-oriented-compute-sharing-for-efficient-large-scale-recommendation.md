---
title: "[论文解读] ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation"
description: "[arXiv 2607.27744][推荐系统] ROCS将推荐推理重构为“请求侧计算一次、候选侧按项计算”的非对称依赖模式，在保留中间请求—候选交互能力的同时减少同一请求内跨候选的重复计算。"
arxiv_id: "2607.27744"
announcement_date: "2026-07-31"
primary_category: "recommender"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.022196+00:00"
source_sha256: "d6db193d81aaeb2e3ec599f4e00931c5785ae7b17f381ee1a41aefe74dc5e85b"
tags:
  - "推荐系统"
  - "大规模推荐模型"
  - "请求级计算共享"
  - "请求—候选交互"
  - "候选隔离"
  - "特征交互"
  - "序列建模"
  - "推理效率"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">推荐系统 · arXiv 2607.27744</p>

# ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Chen, Yuxin, Luo, Liang, Zhang, Buyun, Jiao, Jian, Li, Boda, Wang, Haoyu, Tang, Tongyi, Cai, Ao, Shen, Zijian, Zhang, Zhengkai, Xie, Wenyi, Dick, Ryan, Liu, Han, Shi, Neng, Yu, Bin, Xiao, Jianbo, Bi, Shuyao, Yu, Hongtao, Fang, Yuanwei, Zhao, Zhuoran, Chen, Sijia, Chen, Yang, Yang, Shuqi, Li, Qianru, Liu, Zikun, Ling, Wei, Zeng, Sihan, Jin, Longhao, Lu, Jiaxin, Ma, Yinbin, Li, Jiawei, Ruan, Yichen, Lee, Yong Ler, Guan, Birmingham, Li, Zijian, Sun, Jianbo, Zhang, Zhengyu, Chen, Zeliang, Wei, Xiaohan, Hao, Yuchen, Musumeci, GP, Ranganathan, Venkatesh, Yao, Yantao, Tang, Chunqiang, Chen, Wenlin, Kolay, Santanu, Wen, Ellie Dingqiao</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27744) · [PDF 下载](https://arxiv.org/pdf/2607.27744) · **关键词** 大规模推荐模型, 请求级计算共享, 请求—候选交互, 候选隔离, 特征交互, 序列建模, 推理效率<br>


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

ROCS将推荐推理重构为“请求侧计算一次、候选侧按项计算”的非对称依赖模式，在保留中间请求—候选交互能力的同时减少同一请求内跨候选的重复计算。

**不用术语来说**：一次推荐请求通常需要给许多候选物品打分，其中用户画像、上下文和历史行为等输入对所有候选都相同；但常规模型很早就把这些信息与每个候选混合，导致后续的大量计算必须为每个候选重复执行。模型越大、用户序列越长，这种浪费越严重，而线上延迟和算力预算又限制了模型扩展。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出面向请求的计算共享范式ROCS：通过推迟候选信息进入共享表示的时机，维持候选无关的请求侧路径，同时允许候选表示在模型中持续读取请求侧信号，从而兼顾计算复用与中间交互表达能力。
- 作者将这一范式落实到实际推荐架构与GPU执行：GLM以算子级依赖约束隔离候选信息，DCA支持候选条件下对共享序列表示的深层检索，RRR将节省的算力重新投入模型容量，IKBO则避免显式物化广播数据。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大规模推荐模型根据请求上下文、用户行为序列和候选物品特征预测用户行为。稀疏特征通常先映射为嵌入，稠密特征经过变换，再由特征交互模块和序列模块联合建模；增加这些模块的计算量通常能提高预测质量，但线上延迟与硬件容量限制了每次请求的计算预算。本文关注推荐推理特有的“一次请求对应多个候选”结构：同一请求中的用户与上下文特征保持不变，只有候选特征变化，因此模型若能保持候选无关的请求侧表示，就可将一部分计算从“每个候选执行一次”改为“每个请求执行一次”。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**请求侧特征与候选侧特征**

请求侧特征包括用户信息、时间、位置和用户行为序列，在同一次推荐请求的所有候选之间共享；候选侧特征描述具体物品，如类别或内容属性，会随候选变化。区分两者是判断中间表示能否跨候选复用的基础。

</div>
<div class="concept-item" markdown="1">

**特征交互与序列建模**

特征交互模块学习用户、上下文和物品属性之间的组合关系，序列模块则从用户历史行为中提取兴趣表示。若候选信号过早进入这些模块，后续表示都会依赖候选，整段计算便需要为每个候选重复执行。

</div>
<div class="concept-item" markdown="1">

**计算广播与摊销**

常规模型会把一份请求侧表示复制或逻辑广播到多个候选上，再逐候选执行后续网络；这会产生重复计算，并可能带来额外张量物化开销。若共享部分只计算一次，其成本可由同一请求的全部候选共同承担，即被摊销。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一批推荐请求；每个请求包含一组共享的请求侧特征，例如上下文、用户属性和行为序列，以及多个各自不同的候选侧特征。模型需要为每个请求与候选的配对输出行为预测分数，并满足线上吞吐量和延迟约束。关键假设是同一请求内的请求侧输入完全相同，因此任何不依赖候选的中间结果都可被精确复用；问题在于设计依赖关系，使候选侧表示可以持续读取请求侧信号，而候选信息不能反向污染可共享的请求侧路径，从而在保留中间交互能力的同时减少逐候选计算。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$r$**

一次用户推荐请求及其共享的请求侧特征；该符号是为概括原文问题设置而采用，原文节选未给出正式符号。

</div>
<div class="notation-item" markdown="1">

**$c_i$**

请求中的第 $i$ 个候选及其候选侧特征；原文节选未给出正式符号。

</div>
<div class="notation-item" markdown="1">

**$N_r$**

请求 $r$ 需要评估的候选数量；原文节选未给出正式符号。

</div>
<div class="notation-item" markdown="1">

**$h_r$**

仅依赖请求 $r$、因而能够在多个候选之间复用的中间表示；原文节选未给出正式符号。

</div>

</div>

**直接相关的工作**

- **Two-tower models（Covington et al., 2016）**: 双塔模型分别编码用户和物品，只在最终相似度函数中交互，因此最大化请求侧计算复用并适合高效检索；但它缺少网络中间层的请求—候选交互，表达能力受限，难以单独承担计算密集型排序。ROCS试图保留这种复用优势，同时允许候选侧表示在模型内部持续使用请求侧信号。
- **UGSEP（Lu et al., 2026）**: UGSEP通过面向RankMixer的掩码式令牌混合保留可复用的用户侧令牌，并补偿交互能力损失；其设计与特定架构绑定。ROCS将共享条件提升为可组合的算子级依赖不变量，目标是覆盖注意力、MLP、特征压缩及显式特征交互等异构组件。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

推荐模型可通过扩大特征交互模块和序列模块提升预测质量，但生产系统受到吞吐量、延迟与基础设施成本约束。由于一个请求对应多个候选，请求侧特征会被重复广播；一旦模型在早期融合请求与候选，原本相同的请求侧计算也会转化为逐候选计算，长序列中的高成本算子及其后续网络尤其容易成为实时服务瓶颈。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **系统级降本与知识迁移**：模型统一通过合并多个专用模型减少总体计算；知识迁移则把重计算放入异步流程，再将其知识蒸馏到较轻的在线模型中，以降低服务阶段的直接成本。
- **交互时机受限的共享架构**：双塔模型分别编码请求和候选，仅在最终评分时交互，以最大化请求表示复用；近期基于Transformer或特定骨干的掩码方案则允许部分中间交互，同时阻止候选信息污染可共享的请求表示。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 模型统一和知识迁移并未直接消除单次请求内部的逐候选冗余，并受到领域间干扰、蒸馏效率不足以及异步知识不够新鲜等约束，因此难以作为普适的模型扩展机制。
- 早融合架构保留了充分的交叉特征，却迫使高成本计算按候选重复；双塔将交互推迟到末端，又损失中间交互和表达能力。已有折中方案通常绑定特定模型结构，无法统一约束实际推荐模型中其他组件引入的候选依赖。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种可组合、跨特征交互与序列模块的通用依赖规则：它需要明确哪些中间表示必须保持候选无关，并让候选路径读取请求信号而不反向污染共享路径；同时还要让这种逻辑共享在GPU上转化为真实吞吐收益，而非被广播物化和数据搬运开销抵消。

</div>
<div markdown="1"><span>核心问题</span>

能否通过模型与推理系统协同设计，把推荐网络中的请求侧计算系统性地暴露并保留下来，使其对同一请求只执行一次，同时继续支持模型深层的请求—候选交互，并在预测质量、吞吐量和模型容量之间获得更优折中？

</div>
<div markdown="1"><span>作者直觉</span>

关键在于利用依赖方向的不对称性：候选表示可以查询或消费已经算好的请求表示，但共享的请求表示不能吸收任何特定候选信息。这样，交互仍可在多层发生，却不会使整条请求路径变成候选专属计算。通俗地说，是先为用户准备一份可反复查阅的“公共资料”，每个候选只执行自己的增量分析，而不是为每个候选重新整理整份用户资料。该思路最适合每个请求候选较多且模型中候选无关计算占比较高的场景；候选数量较少时，可摊销的收益会下降。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ROCS把“同一请求要同时评估多个候选”这一推理结构直接写入模型：输入先按请求侧与候选侧分组，在特征交互网络中用广义层掩码（GLM）禁止候选信息反向污染请求侧表示；在行为序列网络中用深度交叉注意力（DCA）将昂贵的序列编码及键值投影改为每个请求计算一次，只保留较轻的候选条件检索逐候选执行。由此形成显式的共享请求子图和候选相关子图，前者的结果可广播给同一请求下的全部候选，后者继续建模请求—候选交互并输出各候选预测。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 输入分组与请求级共享准备

按照固定顺序把特征划分为请求组与候选组，并让序列流仅接收请求侧输入；这一分组同时确定后续算子的块下三角依赖关系。

<div class="method-step__io" markdown="1">

**输入**：一个请求的请求侧特征 $X^R$、用户行为序列 $S_0$，以及与该请求关联的候选特征集合 $\{X^{C_1},\ldots,X^{C_N}\}$。<br>
**输出**：候选无关的请求输入与序列输入，以及分别对应各候选的候选侧输入。

</div>

**直观理解**：先把一批候选共同拥有的信息和每个候选独有的信息分开，避免后续把本可复用的共同部分重复计算 $N$ 次。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. GLM 特征交互变换

逐算子实施 GLM 依赖约束：请求侧输出只能读取请求侧输入，候选侧输出可以读取请求与候选两侧输入；多个合规算子组合后仍保持该约束。

<div class="method-step__io" markdown="1">

**输入**：分组后的请求表示 $X^R$ 与候选表示 $X^C$，以及原推荐骨干中的线性层、线性压缩块、归一化、点运算和因子分解机等模块。<br>
**输出**：请求侧表示 $Y^R$ 和候选侧表示 $Y^C$，其中 $Y^R$ 对候选不变，而 $Y^C$ 保留请求—候选及候选内部交互。

</div>

**直观理解**：这相当于在网络内部设置单向阀门：公共信息可以流向候选分支，但候选信息不能倒流并改变公共分支。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. DCA 共享序列编码与分层检索

请求专属编码器逐层产生 $S_i=\operatorname{Enc}_i(S_{i-1})$，并共享其键和值投影；每个交互层再生成请求查询 $Q_i^R$ 与候选查询 $Q_i^C$，分别对同一层的 $S_i$ 做交叉注意力。

<div class="method-step__io" markdown="1">

**输入**：用户行为序列 $S_0$，以及每层 GLM 产生的请求侧和候选侧表示 $Y_{i-1}^R,Y_{i-1}^C$。<br>
**输出**：可复用的请求侧注意力结果 $A_i^R$、逐候选的注意力结果 $A_i^C$，以及供下一交互层使用的融合表示。

</div>

**直观理解**：系统只读一遍用户历史并制作可检索的“索引”，随后每个候选用自己的问题从该索引取回相关行为；在多层都检索，使后层能利用更丰富的请求—候选上下文。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 请求侧资源重分配与预测

通过请求侧资源重分配（RRR）扩大可共享请求路径的表示容量，以补偿固定容量下延迟候选交互可能造成的表达力下降；最终将请求表示广播并与各候选表示完成剩余计算，产生逐候选预测。

<div class="method-step__io" markdown="1">

**输入**：GLM 和 DCA 节省的请求级摊销计算预算、请求侧缩放比例 $r$，以及最终请求侧和候选侧表示。<br>
**输出**：每个候选的排序或检索分数，以及可在同一请求内复用的中间结果。

</div>

**直观理解**：ROCS不是简单删掉计算，而是把节省的预算优先投入只需计算一次的公共分支，因此可以较低的逐候选成本换取更大的模型容量。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### GLM 分组依赖不变量

$$
x^{(0:i)}=x^{\prime(0:i)}\Longrightarrow f^{(i)}(x)=f^{(i)}(x^{\prime});\qquad f(x^R,x^C)=\bigl(f^R(x^R),f^C(x^R,x^C)\bigr),\qquad M_{ij}=\mathbf{1}\{j\le i\}
$$

**符号说明**

- $x^{(i)}$：第 $i$ 个输入特征组。
- $x^{(0:i)}$：从第 $0$ 组到第 $i$ 组组成的输入前缀。
- $x^{\prime}$：用于检验依赖关系的另一组输入。
- $f^{(i)}(x)$：算子 $f$ 在输入 $x$ 上产生的第 $i$ 个输出组。
- $x^R,x^C$：两组情形下的请求侧输入和候选侧输入。
- $f^R,f^C$：请求侧输出函数与候选侧输出函数；前者只读取请求输入，后者可以读取两侧输入。
- $M_{ij}$：从输入组 $j$ 到输出组 $i$ 的许可掩码，值为 $1$ 表示允许依赖。
- $\mathbf{1}\{j\le i\}$：当 $j\le i$ 时取 $1$、否则取 $0$ 的指示函数。

<div class="equation-explanation" markdown="1">

**直观理解**：若两份输入在第 $0$ 至第 $i$ 组完全相同，则第 $i$ 个输出也必须相同；因此后面的候选组无法影响前面的请求组。在常用的两组设置中，这直接保证 $f^R(x^R)$ 能对同一请求的全部候选只计算一次，而候选分支仍可使用两侧信息完成交互。<br>
**原文位置**：第 3.1 节，公式（1）—（3）

</div>

</div>

<div class="equation-block" markdown="1">

#### DCA 查询生成与分组交叉注意力

$$
\begin{bmatrix}Q_i^R\\Q_i^C\end{bmatrix}=\operatorname{MLP}_i\!\left(\operatorname{LCB}_i\!\left(\begin{bmatrix}Y_{i-1}^R\\Y_{i-1}^C\end{bmatrix}\right)\right),\qquad A_i^R=\operatorname{Attn}\!\left(Q_i^R,S_iW_{K,i}^R,S_iW_{V,i}^R\right),\qquad A_i^C=\operatorname{Attn}\!\left(Q_i^C,S_iW_{K,i}^C,S_iW_{V,i}^C\right)
$$

**符号说明**

- $i$：当前交互层或序列编码深度。
- $Y_{i-1}^R,Y_{i-1}^C$：前一 GLM 层输出的请求侧表示与候选侧表示。
- $\operatorname{LCB}_i$：第 $i$ 层的 GLM 合规线性压缩块。
- $\operatorname{MLP}_i$：第 $i$ 层的 GLM 合规多层感知机。
- $Q_i^R,Q_i^C$：用于检索用户序列的请求侧查询与候选侧查询。
- $S_i$：请求专属序列编码器在第 $i$ 层产生的候选无关序列表示。
- $W_{K,i}^R,W_{V,i}^R$：请求侧注意力在第 $i$ 层使用的键和值投影矩阵。
- $W_{K,i}^C,W_{V,i}^C$：候选侧注意力在第 $i$ 层使用的键和值投影矩阵。
- $\operatorname{Attn}$：以查询、键和值为输入的交叉注意力运算。
- $A_i^R,A_i^C$：第 $i$ 层得到的请求侧与候选侧注意力输出。

<div class="equation-explanation" markdown="1">

**直观理解**：查询生成器遵循 GLM，因此请求查询和对应注意力结果可按请求共享，候选查询则继续携带候选上下文。两类查询检索同一份共享序列表示，但使用各自的键值投影，从而同时实现昂贵序列编码的复用和候选相关的信息选择。<br>
**原文位置**：第 3.2 节，公式（12）—（13）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：所给章节没有提出新的损失函数，也未明确报告 ROCS 对原推荐任务训练目标的修改；其核心是计算图依赖约束、序列结构拆分和容量分配。因此训练时应沿用具体推荐骨干原有的监督目标，并通过该目标联合优化 GLM、DCA、序列编码器及最终预测层参数；关于损失形式、负采样或多任务权重，原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 广义层掩码（GLM）**

GLM规定函数级不变量：第 $i$ 个输出组只能依赖输入组 $0$ 到 $i$。线性层和线性压缩块把权重改成块下三角结构；归一化改为组内统计；多输入点运算按对应组执行；因子分解机仅保留允许的组间交互。由于该性质对函数复合封闭，整个 MLP 或特征交互堆栈都能维持请求侧对候选不变。需要注意，这不是假定两类特征统计独立，而是主动限制计算图中的信息流方向。

> 直观理解：仅在算子输出后遮挡是不够的，因为请求表示可能已经在算子内部混入候选信息。GLM必须改造每类算子的内部依赖，才能保证缓存的请求结果与当前候选无关，并且与对同一 ROCS 化模型进行广播执行时的确定性结果一致。

**2. 深度交叉注意力（DCA）**

DCA把候选感知的序列建模拆成请求专属序列编码和候选条件检索。序列表示 $S_i$ 及其键、值投影每个请求只计算一次；GLM 合规的查询生成器保证 $Q_i^R$ 仅依赖请求，而 $Q_i^C$ 可依赖请求和候选。交叉注意力设置在每个交互层，而非只在末端检索，使不同深度的查询可以从对应深度的序列表示中提取互补信息。

> 直观理解：若一开始就把候选注入用户序列，整条昂贵序列网络都要为每个候选重跑；若完全推迟交互，又可能损失候选相关性。DCA共享昂贵的“理解历史”过程，同时保留每层按候选检索历史的能力。

**3. 请求侧资源重分配（RRR）**

直接 ROCS 化并不保证在固定容量下保持表达力，因为常规模块可将全部输出维度用于候选相关表示，而 ROCS 模块必须预留一部分给可复用请求表示。RRR用缩放比例 $r$ 控制各 ROCS 模块的请求侧容量，并把计算共享产生的预算节省重新投入请求路径；原文称默认在所有 ROCS 模块中使用相同的 $r$。

> 直观理解：请求路径扩大一次即可服务多个候选，所以增加它的容量比等量扩大逐候选路径便宜。该设计负责把“更省算力”转化为更好的质量—效率折中，而不是把结构约束带来的容量损失留给模型自行承担。

**训练与推理**

训练阶段，以请求—候选样本及用户行为序列为输入，在每个被 ROCS 化的算子内部执行 GLM 约束，并通过 DCA 生成共享序列表示和分组注意力结果；整个网络仍可端到端反向传播。RRR通过请求侧缩放比例 $r$ 调整共享分支容量，但所给章节未说明 $r$ 是搜索所得还是固定超参数，也未说明训练批次是否显式按请求聚合。

推理阶段，对一个请求先计算一次请求侧特征子图、各层序列表示 $S_i$、共享键值投影以及请求侧注意力；随后将这些结果提供给该请求的 $N$ 个候选，仅执行候选侧查询、候选相关交互与预测头。由 GLM 的复合封闭性，同一请求下所有候选的请求侧结果满足 $[F(X^R,X^{C_1})]^R=\cdots=[F(X^R,X^{C_N})]^R=F^R(X^R)$，所以缓存或广播不会改变同一个 ROCS 化模块在确定性前向传播下的语义结果。

**复现信息**

公平实现的关键不是在普通算子输出端简单置零，而是分别改造算子内部：线性层和线性压缩块使用块下三角权重，归一化按组计算统计量，残差与其他点运算按对齐分组执行，拼接和形状变换必须保留组标签，因子分解机屏蔽从后组流向前组的交互。DCA 的序列流必须排除候选输入，才能让 $S_i$ 及其键值投影真正按请求缓存。

GPU 推理还采用内核内广播优化（IKBO），避免显式物化请求结果到所有候选的广播副本；线性压缩块中的请求贡献 $W_{CR}X^R$ 可由 IKBO直接提供。所给节选没有给出 IKBO 的完整内核算法、硬件配置或通用复现参数，因此不能据此补充线程布局、精度格式或融合策略；已明确的实现原则是把请求级广播与后续候选计算融合，以减少额外内存读写和中间张量。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- KuaiRand：公开多反馈推荐数据集，含1,000名用户、4,369,953个物品和11,713,045次交互，提供30个用户特征、62个物品特征以及点击、点赞、关注标签。它具有明确且丰富的请求侧与候选侧特征，用于检验ROCS在请求侧计算占比较高场景中的质量—效率权衡。原文未明确报告训练、验证和测试划分比例。
- KuaiVideo：公开多反馈视频推荐数据集，含10,000名用户、3,239,534个物品和13,661,383次交互，提供5个用户特征、2个物品特征以及点击、点赞、关注标签。它用于检验ROCS在请求侧特征较少、但每个请求仍需评价多个候选的视频推荐场景中的泛化能力。原文未明确报告数据划分比例。
- KKBox：公开音乐推荐数据集，含7,377,418次交互、7个用户特征和12个物品特征，以是否重复播放为单一反馈；用户数和物品数在表中未给出。它与两个多反馈数据集互补，用于检验ROCS在单任务推荐上的有效性。原文未明确报告数据划分比例。另有三个内部生产工作负载——广告检索、短视频排序和广告排序——每个均超过1,000亿训练样本，但因数据不公开，原文未提供更细的数据统计或划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**AUC**

ROC曲线下面积，衡量正样本得分高于负样本的排序能力。多反馈数据集分别报告点击、点赞、关注AUC，并以宏平均AUC概括整体质量；KKBox报告重复播放AUC。 （越高越好，因为更高的AUC表示模型区分正负反馈的能力更强。）

</div>
<div class="metric-item" markdown="1">

**摊销FLOPs与MFLOPs/候选**

硬件无关的算法计算复杂度。若请求侧计算量为$C_R$、每候选计算量为$C_C$、每请求候选数为$N$，则每候选摊销成本为$C_{\mathrm{amort}}(N)=C_C+C_R/N$；公开实验报告$N\in\{1,100\}$，生产实验报告每候选MFLOPs。 （越低越好，因为相同预测质量下，更少的浮点运算意味着更高的理论推理效率；但它不包含内存访问、内核调度等系统开销。）

</div>
<div class="metric-item" markdown="1">

**相对LogLoss与相对QPS**

生产实验以相对LogLoss衡量概率预测误差，以每秒处理请求数QPS衡量H100服务器上回放生产流量时的端到端吞吐。广告与自然内容工作负载中，作者分别将0.02%和0.1%的RLL改善视为具有实践意义。 （相对LogLoss越低越好，表示预测概率更准确；QPS越高越好，表示同一服务环境单位时间可处理更多请求。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三个公开数据集、三种骨干上的ROCS-Base效率结果

<div class="result-value" markdown="1">

在$N=100$时，ROCS-Base相对对应Vanilla显著减少摊销FLOPs：表1给出的降幅覆盖30.1%至90.6%。例如，DCNv2在KuaiVideo上从1.49降至0.14 FLOPs单位，减少90.6%；Wukong在KuaiRand上从9.92降至5.47，减少45.1%。与此同时，Base配置有时出现小幅AUC下降，符合候选相关通路容量被压缩的预期。

</div>

这说明只改变计算组织方式、把可共享部分移到请求侧执行一次，就能在多候选推理中削减大量重复计算，而且候选越多，请求侧成本越容易被摊薄。不过，结果并不表示Base配置必然保持质量：它刻意不把节省的预算重新投入容量，因此部分任务的AUC会下降；FLOPs下降也不等价于实际QPS按同比例上升。

<div class="result-source" markdown="1">

来源：第5.1.3节，表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under the base configuration, ROCS substantially reduces amortized FLOPs at N=100 across all evaluated ROCS backbones.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 公开数据集上ROCS-Scaled与相应Vanilla骨干的等预算比较

<div class="result-value" markdown="1">

在约相同的$N=100$摊销预算下，ROCS-Scaled的宏平均AUC均高于对应Vanilla：例如DCNv2在KKBox上由0.8287升至0.8330，FinalMLP在KuaiRand上由0.8661升至0.8700，Wukong在KuaiVideo上由0.7972升至0.7980。表1中的九个“数据集—骨干”组合均呈现宏平均AUC提升。

</div>

结果支持作者的资源再分配主张：共享省下的计算若用于扩大每请求只运行一次的网络，可在近似相同的多候选计算预算下提高质量。它证明的是所测试预算和骨干上的经验优势，并不单独证明所有容量都应放在请求侧，也不能排除超参数搜索或离散维度造成的轻微预算差异。

<div class="result-source" markdown="1">

来源：第5.1.3节，表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ROCS–Scaled reinvests the saved computation into additional request-side capacity and improves the aggregate AUC of the corresponding Vanilla backbone under a comparable N=100 amortized budget.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 三个生产级工作负载上的端到端部署评估

<div class="result-value" markdown="1">

ROCS在广告检索、短视频自然内容排序和广告排序中分别获得196%、47%和62%的相对QPS提升；广告检索与广告排序的LogLoss质量持平，短视频排序的相对LogLoss改善0.5%。三个数据集均超过1,000亿训练样本，模型复杂度约跨两个数量级。

</div>

该结果表明ROCS的算法节省可在真实H100服务栈中转化为吞吐收益，而不只是纸面FLOPs下降。广告检索候选数量约为$O(10{,}000)$，其增益最大，与请求侧成本被更多候选摊销的机制一致；短视频排序则把部分预算重新投入容量，兼得质量和吞吐。不过这些是内部数据与回放流量结果，缺少公开复现条件，也未报告置信区间或在线业务指标的具体数值。

<div class="result-source" markdown="1">

来源：第5.2.2节，表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ROCS matches or improves model quality while increasing replay QPS by 47–196% across retrieval and ranking models spanning approximately two orders of magnitude in inference complexity.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 公开实验未报告数据划分、重复运行次数、随机种子、误差范围或统计显著性；部分AUC差异仅在千分位量级，因此难以判断小幅提升是否对随机初始化和数据切分稳健。
- 最强的QPS与LogLoss结论来自不可公开的内部数据和特定H100服务环境。公开基准主要报告硬件无关FLOPs，因而外部读者无法完整复现生产吞吐，也不能直接推断其他GPU、候选规模或低请求侧计算工作负载上的收益。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Vanilla骨干：原始DCNv2、FinalMLP或Wukong在较早阶段混合请求侧和候选侧特征，因此完整网络需对每个候选重复执行。它是最直接的对照，用于判断把同一骨干改造成ROCS后，质量和计算成本如何变化。
- ROCS-Base：将$N=1$时的推理FLOPs尽量匹配相应Vanilla模型，不把多候选共享产生的节省重新投入模型容量。该配置主要检验直接进行候选隔离和请求侧共享能节省多少计算，以及是否因候选相关通路容量缩小而损失质量。
- ROCS-Scaled：扩大请求侧模型容量，使$N=100$时的摊销FLOPs尽量不超过相应Vanilla预算。该配置检验“请求导向资源再分配”：不是单纯削减成本，而是把共享节省的预算投入只执行一次的请求侧网络。
- RankMixer with UGSEP：面向请求共享的专用架构基线，分别报告UGSEP@1和UGSEP@100。它用于判断ROCS是否不仅优于未共享的骨干，而且能与已有架构特定的请求共享方案形成有竞争力的质量—效率前沿。

**实验想回答的问题**

- 在公开数据集和不同特征交互骨干上，ROCS能否稳定改善预测质量与推理计算量之间的权衡，并在候选数从$N=1$增至$N=100$时通过请求侧计算复用获得更大收益？
- 在生产级检索与排序系统中，ROCS的算法级FLOPs节省能否转化为端到端QPS提升；DCA的候选隔离设计以及IKBO的算子优化分别贡献了什么？

**实验实现**

公开实验按RecZoo提供的预处理和数据格式进行，所有模型以PyTorch实现并在单张96 GB NVIDIA H100上训练。每个“模型—数据集”组合从给定网格抽取20组配置，在单样本前向成本约10 MFLOPs的预算内选择验证AUC最高者；统一采用Adam、学习率$10^{-3}$、批量大小65,536、最多100轮训练和耐心值5的早停。ROCS-Base沿用对应Vanilla超参数，ROCS-Scaled逐步扩大网络宽度等容量，直至$N=100$时的摊销成本不超过Vanilla预算。生产实验固定Wukong骨干，并在相同数据、特征、训练流程和服务环境下比较Vanilla与ROCS；QPS由H100服务器回放生产流量测得。该协议控制了大部分训练与部署变量，但公开摘录没有给出随机种子、重复运行次数、方差或显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| DCA关键设计消融：候选隔离、逐层交叉注意力和请求侧交叉注意力 | 以DCA为基准，改用会使序列处理栈产生候选依赖的Interformer时，质量持平但相对QPS下降36%；将交叉注意力限制为单一深度时，相对LogLoss恶化0.05%，但QPS提高5%；移除请求侧交叉注意力时，相对LogLoss同样恶化0.05%，QPS持平。 | Interformer对照隔离了“序列主干是否保持候选无关”这一因素：质量相近而吞吐明显下降，说明延迟引入请求—候选交互是共享效率的关键。两个0.05%的质量回退分别支持逐层检索和请求侧检索的作用，但幅度较小，且原文没有方差或显著性检验，因此不能确定其统计稳定性。 | 第5.2.4节，表3<br><span class="experiment-evidence">Replacing DCA with Interformer, which introduces candidate dependence into the sequence-processing stack, achieves comparable quality but reduces QPS by 36%.</span> |
| IKBO-LCB内核的递增优化消融 | 内核延迟从原始1.944 ms依次降至：分解后1.389 ms（降低28.5%）、内存对齐后0.798 ms（降低58.9%）、广播融合后0.580 ms（降低70.2%），最终通过GEMM与广播流水化并融合请求/候选计算降至0.482 ms（降低75.2%）。 | 该消融逐步加入系统优化，说明收益并非仅来自模型结构：避免显式广播、改善内存对齐和重叠计算均有增量贡献。最终数字是特定IKBO-LCB算子的延迟，而不是完整推荐模型的端到端延迟，因此不能直接解释为整套服务加速75.2%。 | 第5.2.5节，表4<br><span class="experiment-evidence">Pipelining GEMM with broadcast + fusing request/candidate compute \| 0.482 \| −75.2%</span> |

**定性案例**

- 请求侧扩展实验固定候选侧容量，仅逐步提高请求侧与候选侧FLOPs之比；图4显示两个生产模型的RLL随请求侧计算增加而持续改善。该趋势支持“把共享节省的预算投入请求侧”的设计逻辑，但摘录未给出各点的精确数值、误差条或模型身份，因此只能作为趋势证据，不能量化边际收益。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：核心贡献是通过请求级计算共享改进大规模推荐模型的检索与排序效率。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`d6db193d81aaeb2e3ec599f4e00931c5785ae7b17f381ee1a41aefe74dc5e85b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
