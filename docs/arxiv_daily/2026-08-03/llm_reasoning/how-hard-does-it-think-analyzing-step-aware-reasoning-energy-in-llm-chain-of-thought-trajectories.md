---
title: "[论文解读] How Hard Does It Think? Analyzing Step-Aware Reasoning Energy in LLM Chain-of-Thought Trajectories"
description: "[arXiv 2607.28674][LLM Reasoning] 本文提出步感知推理能量（SARE），通过比较相邻 Transformer 层中思维链步骤的词元关系几何变化，刻画模型在每个推理步骤投入的内部计算努力，并研究该信号与语义阶段及推理失败的关系。"
arxiv_id: "2607.28674"
announcement_date: "2026-08-03"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-03T02:16:23.657510+00:00"
source_sha256: "c2c40caa1eadfcc9727047d101f5f1217bf030c896fde53eb42567c441529034"
tags:
  - "LLM Reasoning"
  - "LLM 机制与可解释性"
  - "大语言模型"
  - "思维链推理"
  - "步骤级推理能量"
  - "居中核对齐"
  - "Gram矩阵"
  - "隐藏状态"
  - "语义状态聚类"
  - "马尔可夫状态转移"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2607.28674</p>

# How Hard Does It Think? Analyzing Step-Aware Reasoning Energy in LLM Chain-of-Thought Trajectories

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-03</span>
<span><strong>作者</strong> Hui Wei, Junda Wu, Sheldon Yu, Sizhe Zhou, Yizhu Jiao, Ming Zhong, Bowen Jin, Tong Yu, Shijia Pan, Jiawei Han, Julian McAuley</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Adobe Research</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.28674) · [PDF 下载](https://arxiv.org/pdf/2607.28674) · **关键词** 大语言模型, 思维链推理, 步骤级推理能量, 居中核对齐, Gram矩阵, 隐藏状态, 语义状态聚类, 马尔可夫状态转移<br>


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

本文提出步感知推理能量（SARE），通过比较相邻 Transformer 层中思维链步骤的词元关系几何变化，刻画模型在每个推理步骤投入的内部计算努力，并研究该信号与语义阶段及推理失败的关系。

**不用术语来说**：思维链虽然把中间推理写了出来，却没有直接说明模型在哪些步骤真正进行了复杂加工、在哪些步骤只是沿用已有表示，也无法仅凭文字可靠判断错误从何处开始。研究者因此需要一种观察模型内部状态的方法，将计算努力定位到具体步骤，并检验关键步骤中的异常加工模式能否预示最终回答错误。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 SARE：在每个思维链步骤内，由词元隐藏状态构造 Gram 矩阵，并用中心核对齐（CKA）衡量相邻层之间词元关系结构的重组程度，从而获得保留词元间关系的步骤级计算努力指标。
- 将步骤级能量与无监督发现的潜在语义状态结合，以分析能量沿推理链的阶段性变化，以及正确和错误轨迹在关键语义节点上的差异；同时将这些动态特征用于离线推理失败检测。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大语言模型可通过思维链（Chain-of-Thought, CoT）把复杂问题拆成连续的文本推理步骤，但步骤可见并不等于内部计算过程透明：输出概率只能描述模型最终“说得多自信”，难以判断每一步在 Transformer 各层中经历了多少表征重组。本文研究步骤级推理能量，即利用相邻层之间词元关系几何的变化，估计模型对单个推理步骤投入的内部计算努力；同时把步骤归入潜在语义状态，以分析能量如何随问题设定、事实检索、组合推理和最终验证等语义功能而变化。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**思维链推理**

模型在给出最终答案前生成若干中间推理步骤，例如列式、检索事实或验证结论。本文把完整轨迹切分为$T$个离散步骤，而不是把整段推理视为一个不可分割的文本序列。

</div>
<div class="concept-item" markdown="1">

**Gram矩阵与居中核对齐**

步骤中各词元的隐藏向量可组成矩阵，其Gram矩阵记录任意两个词元表征的相似关系；居中核对齐（CKA）用于比较两层Gram矩阵所描述的关系结构是否一致。相邻层CKA较低意味着词元间关系仍在明显重组，可被解释为该步骤需要更深的内部处理。

</div>
<div class="concept-item" markdown="1">

**潜在语义状态与一阶马尔可夫链**

潜在语义状态是通过无监督聚类得到的步骤类型，每一类可对应问题设定、事实检索或最终验证等功能。本文进一步假设下一步骤的状态主要依赖当前状态，用转移概率$P_{ij}$描述从状态$C_i$转向$C_j$的经验规律。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一条由开放权重大语言模型生成的CoT轨迹$\mathcal{T}=[s_1,\ldots,s_T]$，其中步骤$s_t$含$n_t$个词元；分析还需要取得这些词元在各Transformer层的隐藏状态。对每个步骤和层$l$，隐藏状态矩阵$\mathbf{H}_t^{(l)}\in\mathbb{R}^{n_t\times d}$被转换为Gram矩阵$\mathbf{G}_t^{(l)}=\mathbf{H}_t^{(l)}(\mathbf{H}_t^{(l)})^\top$，以保留步骤内部的词元关系；相邻层关系几何的变化随后用于刻画步骤级推理能量。另一方面，系统根据最后一层隐藏状态的累积Gram矩阵谱构造步骤嵌入，经$K$-Means得到宏观语义状态$C_1,\ldots,C_K$，从而输出每一步的能量、语义状态序列及跨步骤能量动态。该设置采用一阶马尔可夫近似分析状态转移，并把“持续跨层重组”解释为较高计算努力；这种能量是内部表征变化的操作性指标，不等同于实际硬件功耗，也不直接证明模型执行了人类式思考。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{T}=[s_1,\ldots,s_T]$**

由$T$个离散文本步骤构成的完整CoT推理轨迹，其中$s_t$表示第$t$步。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{H}_t^{(l)}\in\mathbb{R}^{n_t\times d}$**

步骤$s_t$在第$l$层的词元隐藏状态矩阵；$n_t$是该步骤的词元数，$d$是隐藏维度。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{G}_t^{(l)}=\mathbf{H}_t^{(l)}(\mathbf{H}_t^{(l)})^\top$**

步骤$s_t$在第$l$层的Gram矩阵，元素表示步骤内部词元隐藏表征之间的两两内积关系。

</div>
<div class="notation-item" markdown="1">

**$P_{ij}=P(s_{t+1}=C_j\mid s_t=C_i)$**

一阶马尔可夫状态转移概率，即当前步骤属于$C_i$时，下一步骤进入$C_j$的概率。

</div>

</div>

**直接相关的工作**

- **Deep Thinking Ratio（Chen et al., 2026）**: 同样尝试通过跨层行为衡量推理努力，但其依据词元级预测稳定性，并把处理深度汇总成单个轨迹级标量；本文认为这会丢失单步差异以及步骤内部词元之间的关系结构。
- **Tuned Lens（Belrose et al., 2023）**: 该类方法把中间层隐藏状态映射到最终词表预测，用于观察模型预测如何逐层形成；本文不以单个词元的预测为中心，而比较完整推理步骤在相邻层中的关系几何，以连接步骤语义功能与内部计算变化。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

CoT 提示能提升数学、常识和多跳推理表现，但其可读文本只展示模型生成了什么，不能揭示生成每一步时内部表征经历了多少加工。缺少步骤级诊断信号，会使研究者难以识别计算资源集中于何处、错误是否在最终答案之前已经出现，也难以据此设计有针对性的重采样、搜索扩展或训练监督。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **输出层面的置信度与文本分析**：利用生成词元的对数概率、熵或困惑度评估回答置信度，或者在完整推理轨迹文本上训练分类器来预测正确性。这类方法容易获取，但主要观察模型最终呈现的表面信号，并不直接描述 Transformer 各层如何加工某个推理步骤。
- **内部表征探测与深度思考比率（DTR）**：一般内部探测方法分析单个词元或聚合后的隐藏表示；DTR 则依据词元在不同层上的预测稳定性估计推理努力，并将深度信息汇总为整条轨迹的一个标量。它们开始利用模型内部计算，但分析粒度或结构表达仍不足以刻画完整步骤的动态。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 输出置信度和轨迹文本分类器把模型内部计算视为黑箱，因此即使能够判断某条轨迹可能错误，也难以定位哪一个语义步骤缺少充分加工，更不能区分表面上相似但内部处理强度不同的步骤。
- 词元级探测或 DTR 要么独立处理词元，要么把层间变化压缩为轨迹级标量，因而丢失同一步骤内词元之间的关系结构，并掩盖不同语义阶段可能出现的局部能量跃迁和关键失败节点。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种同时满足三项要求的诊断框架：以单个 CoT 步骤为分析单位，直接利用跨层隐藏状态衡量内部加工，并保留步骤内词元之间的关系几何；此外，该内部信号尚未被系统地放入推理链的语义进程中，以解释不同语义角色的能量差异及其与错误轨迹的联系。

</div>
<div markdown="1"><span>核心问题</span>

论文集中回答两个相互衔接的问题：不同潜在语义状态是否具有可区分的步骤级推理能量模式，且这些模式在正确与错误轨迹之间是否不同；在不知道真实答案标签的诊断场景下，步骤能量随推理进程的动态能否提供超越输出置信度的失败预测信息？

</div>
<div markdown="1"><span>作者直觉</span>

如果一个步骤仍在进行实质性推理，其词元彼此之间的相似关系应当随着信息穿过多层 Transformer 而持续重组；若这些关系很早便稳定，模型可能只进行了较浅的加工。CKA 可以直接比较相邻层的整体关系结构，而无需逐一对齐特征方向或语义簇。再把这种重组强度按步骤的语义角色排列，就可能看见整条轨迹平均值会掩盖的局部变化，并发现模型在验证、组合等关键节点是否投入了异常少的计算努力。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把一条思维链轨迹先切分为离散推理步骤，再从大语言模型各层的隐藏状态中提取每一步的“令牌关系几何”。对步骤 $s_t$，作者用 Gram 矩阵描述该步骤内部任意两个令牌表示之间的相似关系，并以中心化核对齐（Centered Kernel Alignment, CKA）比较相邻层的关系几何；各层差异累加后得到步骤感知推理能量 $E_t$。与此同时，方法根据最后一层隐藏状态构造步骤的谱嵌入，并通过 $K$-Means 将步骤归入潜在语义宏状态，以一阶马尔可夫链表示推理状态的跨步骤转移。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 思维链步骤切分与隐藏状态提取

将轨迹切分为 $\mathcal{T}=[s_1,\ldots,s_T]$；对含有 $n_t$ 个令牌的步骤 $s_t$，收集第 $l$ 层隐藏状态矩阵 $\bm{H}_t^{(l)}\in\mathbb{R}^{n_t\times d}$。

<div class="method-step__io" markdown="1">

**输入**：一条思维链文本轨迹 $\mathcal{T}$，以及模型在各 Transformer 层产生的令牌隐藏状态。<br>
**输出**：按步骤和网络层组织的隐藏状态矩阵集合。

</div>

**直观理解**：方法不是给整段回答一个总分，而是先把推理拆成若干步，再查看模型在每一步、每一层内部如何表示这些词。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 令牌关系几何构造与中心化

计算 Gram 矩阵 $\bm{G}_t^{(l)}=\bm{H}_t^{(l)}(\bm{H}_t^{(l)})^\top$，再用中心化矩阵 $\bm{M}_{n_t}=\bm{I}_{n_t}-\frac{1}{n_t}\mathbf{1}\mathbf{1}^\top$ 得到 $\tilde{\bm{G}}_t^{(l)}=\bm{M}_{n_t}\bm{G}_t^{(l)}\bm{M}_{n_t}$。

<div class="method-step__io" markdown="1">

**输入**：步骤 $s_t$ 在第 $l$ 层的隐藏状态矩阵 $\bm{H}_t^{(l)}$。<br>
**输出**：每个步骤在每一层的中心化令牌关系矩阵 $\tilde{\bm{G}}_t^{(l)}$。

</div>

**直观理解**：Gram 矩阵可看作一张“词与词之间有多相似”的关系表；中心化会去除整体偏移，使后续比较更关注关系结构本身。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 相邻层几何差异与步骤能量计算

用 CKA 比较第 $l$ 层与第 $l+1$ 层的令牌关系结构，并定义差异 $D_t^{(l)}=1-\mathrm{CKA}(\tilde{\bm{G}}_t^{(l)},\tilde{\bm{G}}_t^{(l+1)})$；随后将全部 $L-1$ 次层间差异求和得到 $E_t$。

<div class="method-step__io" markdown="1">

**输入**：步骤 $s_t$ 在所有相邻层上的中心化 Gram 矩阵。<br>
**输出**：深度差异曲线 $\bm{D}_t=[D_t^{(1)},\ldots,D_t^{(L-1)}]$ 和步骤感知推理能量 $E_t$。

</div>

**直观理解**：若一个步骤的词间关系在多层中持续被重组，模型就像一直在“修改内部理解”，因而能量较高；若关系很早稳定，能量就较低。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 语义状态聚类与轨迹转移建模

从 Gram 矩阵的特征值谱构造步骤级谱嵌入，通过 $K$-Means 得到硬聚类标签 $C_i$，再将标签序列建模为一阶马尔可夫链；跨步骤能量变化进一步由波动性、峰值和谷值等轨迹统计量表征。

<div class="method-step__io" markdown="1">

**输入**：各步骤最后一层隐藏状态形成的累积令牌 Gram 矩阵，以及步骤能量序列 $[E_1,\ldots,E_T]$。<br>
**输出**：语义宏状态序列、状态转移概率矩阵 $P$，以及反映跨步骤能量动态的轨迹级特征。

</div>

**直观理解**：聚类用于判断每一步大致承担何种概念功能，马尔可夫链则记录推理如何从一种功能切换到下一种功能；能量统计补充说明切换前后模型的内部计算强度如何变化。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 相邻层 CKA 几何差异

$$
D_t^{(l)}=1-\mathrm{CKA}\!\left(\tilde{\bm{G}}_t^{(l)},\tilde{\bm{G}}_t^{(l+1)}\right)=1-\frac{\mathrm{tr}\!\left(\tilde{\bm{G}}_t^{(l)}\tilde{\bm{G}}_t^{(l+1)}\right)}{\left\|\tilde{\bm{G}}_t^{(l)}\right\|_F\left\|\tilde{\bm{G}}_t^{(l+1)}\right\|_F},\quad l=1,\ldots,L-1
$$

**符号说明**

- $D_t^{(l)}$：步骤 $s_t$ 从第 $l$ 层到第 $l+1$ 层的令牌关系几何差异。
- $\tilde{\bm{G}}_t^{(l)}$：步骤 $s_t$ 在第 $l$ 层的中心化 Gram 矩阵，其中 $\tilde{\bm{G}}_t^{(l)}=\bm{M}_{n_t}\bm{G}_t^{(l)}\bm{M}_{n_t}$。
- $\mathrm{tr}(\cdot)$：矩阵的迹；此处用于计算两个中心化关系矩阵的内积。
- $\|\cdot\|_F$：Frobenius 范数，用于归一化矩阵内积，使比较不受整体尺度影响。
- $L$：参与分析的模型层数，因此共有 $L-1$ 个相邻层转移。

<div class="equation-explanation" markdown="1">

**直观理解**：CKA 越高，说明相邻两层中的令牌关系越相似；用 $1-\mathrm{CKA}$ 后，数值越大就表示该层间发生了越显著的内部结构重组。该量是作者把“模型是否仍在处理这一步”转化为可计算信号的核心。<br>
**原文位置**：第 4.1 节，公式（2）与公式（3）

</div>

</div>

<div class="equation-block" markdown="1">

#### 步骤感知推理能量

$$
E_t=\sum_{l=1}^{L-1}D_t^{(l)}
$$

**符号说明**

- $E_t$：推理步骤 $s_t$ 的步骤感知推理能量。
- $D_t^{(l)}$：步骤 $s_t$ 在相邻层 $l$ 与 $l+1$ 之间的 CKA 几何差异。
- $l$：Transformer 层索引。
- $L$：参与计算的总层数。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把一个步骤在整次前向传播中经历的所有层间几何变化累加起来。高 $E_t$ 表示内部令牌关系经过持续调整，作者将其解释为较大的计算努力；低 $E_t$ 表示结构较早稳定，但它不是硬件功耗或物理能耗的直接测量。<br>
**原文位置**：第 4.1 节，公式（4）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。原文所述方法不是通过新增损失函数训练模型，而是对既有大语言模型生成思维链时产生的隐藏状态进行事后表征分析；$E_t$ 是分析指标，不是用于反向传播的优化目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 步骤级令牌关系几何**

模块以 $\bm{G}_t^{(l)}=\bm{H}_t^{(l)}(\bm{H}_t^{(l)})^\top$ 编码步骤内所有令牌对的相似关系，而不是独立考察每个令牌的下一词分布；中心化后的矩阵用于消除均值成分。

> 直观理解：单独观察每个词会丢失“这些词如何共同构成当前推理”的信息，关系矩阵则保留了整步内部的集体语义结构。

**2. 基于 CKA 的层间差异模块**

CKA 直接比较相邻层中对应令牌对的 Gram 矩阵项，并对隐藏表示的正交变换和各向同性缩放保持不变。相比直接比较特征值，它不要求跨层特征向量对齐；相比令牌级 Jensen-Shannon 散度，它保留令牌间依赖；相比跨层软聚类分布，它不需要求解聚类标签对应关系。

> 直观理解：不同网络层可能把同一语义空间旋转或整体缩放，直接比较向量容易把这种无关变化误当成推理变化；CKA 更关注词间关系是否真正被重新组织。

**3. 潜在语义状态与马尔可夫转移模块**

模块从各步骤最后一层累积 Gram 矩阵的特征值谱获得谱嵌入，以 $K$-Means 推断 $K$ 个宏状态；步骤标签序列采用一阶条件概率 $P_{ij}=P(s_{t+1}=C_j\mid s_t=C_i)$ 描述。

> 直观理解：能量回答“模型在这一步内部改动了多少”，状态聚类回答“这一步可能在做哪类工作”；二者结合后，可以研究不同推理功能之间切换时计算强度如何起伏。

**训练与推理**

推理阶段先让既有模型产生思维链，并保存各步骤令牌在各层的隐藏状态。分析阶段对每个步骤构造并中心化 Gram 矩阵，计算全部相邻层的 CKA 差异并累加为 $E_t$；另以最后一层表示产生谱嵌入、执行 $K$-Means 聚类，随后从步骤标签序列估计一阶状态转移概率，并结合相邻步骤能量变化形成轨迹级统计特征。所给章节未描述模型参数更新、聚类中心如何跨数据划分拟合，或下游特征的完整训练流程。

**复现信息**

复现所必需的结构性设定包括：思维链必须被切分为 $T$ 个离散文本步骤；每一步需保留所有参与分析层的令牌隐藏状态；几何比较应使用中心化 Gram 矩阵和相邻层 CKA；语义状态聚类使用最后一层隐藏状态对应的累积 Gram 矩阵特征值谱及 $K$-Means。具体步骤切分规则、谱嵌入维度、聚类数 $K$、累积 Gram 矩阵的实现方式及聚类初始化等细节在所给摘录中未明确报告，原文仅指向附录 A.1。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 数学推理：GSM8K考查小学应用题中的多步数值推理，MATH考查更高难度的数学问题。每个模型在每个数据集上抽取800个样本，二者均来自标准测试集；该组用于检验SARE能否刻画从题意解析、计算到答案形成的不同阶段。
- 常识推理：CSQA要求结合隐含常识进行选择与推断，StrategyQA主要是需要策略性推理的二元真假问答。CSQA从验证集抽取800例；StrategyQA使用完整测试集，共687例。后者特别用于检验概率置信度在短答案、二元输出场景中是否会失效。
- 多跳问答：HotpotQA与MuSiQue要求围绕文本证据完成多步事实组合，均从验证集为每个模型抽取800例。该组用于考查能量信号能否反映证据检索、中间比较与最终综合等功能阶段，以及是否有助于发现多跳推理失败。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**F1-score**

错误轨迹检测的精确率与召回率的调和平均，用于同时惩罚漏检错误和误报错误。分类阈值在验证集上以最大化F1为目标进行选择，再在独立测试集上报告。 （越高越好，因为这表示对错误轨迹的识别在精确率和召回率之间取得更好的平衡。）

</div>
<div class="metric-item" markdown="1">

**AUPRC**

精确率—召回率曲线下面积，衡量模型在不同分类阈值下识别错误轨迹的整体排序能力；相较单一阈值的F1，它更能反映类别不平衡条件下的稳定性。正文未给出具体数值，仅说明附录表8—10呈现相同总体趋势。 （越高越好，因为这意味着错误样本在置信排序中更稳定地位于正确样本之前。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### StrategyQA上的跨模型错误检测，比较SARE、Token Count与四种概率置信度基线

<div class="result-value" markdown="1">

四种概率基线在三个模型上均得到F1为0；SARE仍达到0.459—0.526，Token Count达到0.460—0.580。具体而言，LLaMA-3.2-3B、Gemma-3-4B和Phi-4-mini的SARE分别为0.491、0.459和0.526；Token Count分别为0.580、0.460和0.514。

</div>

作者将概率基线的崩溃解释为二元真假任务中词元概率在不同轨迹间过于接近，阈值调优最终退化为把所有轨迹判为正确；SARE和长度则利用完整推理过程，因此仍保留区分信号。分析上，这说明最终词元概率不是此类任务中可靠的错误探测器，但不能据此断言SARE普遍优于长度：在LLaMA-3.2-3B和Gemma-3-4B上，Token Count分别高出0.089和0.001，短轨迹的长度已解释了相当多信息。

<div class="result-source" markdown="1">

来源：Section 5.3, Empirical Findings (F1 Performance); Tables 1–3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A notable pattern is that four probabilistic baselines (Mean Log-Probability, Negative Entropy, Negative Perplexity, and Self-Certainty) report F1 = 0 on StrategyQA across all three models, which is not an implementation error, but a fundamental limitation of output-based confidence for binary True/False tasks, where token-level probability distributions are near-uniform across trajectories regardless of correctness and threshold tuning collapses to predicting all trajectories correct. Neither SARE nor Token Count exhibits this failure, retaining F1 of 0.46–0.53 and 0.46–0.58 respectively, as both operate on full trajectory features rather than final-token probabilities.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Gemma-3-4B在GSM8K上的错误轨迹检测

<div class="result-value" markdown="1">

SARE取得0.293的F1，高于Token Count的0.200、Mean Log-Probability的0.237、Negative Entropy的0.262、Negative Perplexity的0.236和Self-Certainty的0.282；相对最强基线Self-Certainty提高0.011。

</div>

这一行是SARE在数学推理上具有额外判别信息的清晰实例：跨层能量和状态结构与轨迹长度、平均输出概率相比都更有效。不过绝对F1仍低于0.3，表明该设置中的错误识别依然困难；0.011的领先幅度也不足以单独证明稳定优势，因为原文没有在所给章节中报告多次运行方差或显著性检验。

<div class="result-source" markdown="1">

来源：Table 2, F1 Comparison: SARE vs. All Baselines for Gemma-3-4B

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GSM8K 0.293 0.200 0.237 0.262 0.236 0.282

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### LLaMA-3.2-3B在MuSiQue多跳问答上的错误轨迹检测

<div class="result-value" markdown="1">

SARE取得0.958的F1，高于Token Count与Self-Certainty的0.947，也略高于Mean Log-Probability、Negative Entropy和Negative Perplexity的0.954。

</div>

该结果显示，在需要组合多步事实的任务中，各类信号本身都很强，而SARE只取得小幅领先。这支持内部动态可提供补充信息，但不能说明性能主要来自SARE：最强概率基线仅落后0.004，且主版本的SARE已经加入Token Count，因此应结合去除长度的消融来判断内部能量的独立贡献。

<div class="result-source" markdown="1">

来源：Table 1, F1 Comparison: SARE vs. All Baselines for LLaMA-3.2-3B

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MuSiQue 0.958 0.947 0.954 0.954 0.954 0.947

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验是离线错误检测：分类器使用完整思维链汇总特征，并以最终答案正确性构造标签。它验证的是轨迹结束后的失败识别能力，不等同于生成过程中实时预警、定位首个错误步骤或主动修正推理。
- 能量与错误之间仅是相关关系，且能量尺度明显依赖模型架构，不能直接跨模型比较绝对值。主结果缺少所给章节中的置信区间、多次随机划分方差或显著性检验；同时主SARE包含Token Count，因此小幅领先应结合去长度消融谨慎解释。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Token Count：思维链的总词元数，是最直接的表面长度启发式。它用于判断SARE的效果是否只是因为错误与正确轨迹长度不同；论文也将其加入SARE轨迹特征，以测试内部动态与长度是否互补。
- Mean Log-Probability：生成词元平均对数似然，代表模型对自身输出的平均概率置信度。与SARE比较可判断跨层隐藏状态的几何变化是否提供了最终输出概率之外的信息。
- Negative Entropy与Negative Perplexity：前者是词元分布平均香农熵的相反数，后者定义为$-\exp(-\text{mean log-likelihood})$；二者都经过符号调整，使较大值表示较高置信度。它们测试常见的不确定性指标能否替代内部推理动态。
- Self-Certainty：词元概率分布与均匀分布之间的KL散度，用于衡量模型内部置信程度。它是比单纯最大概率更结构化的输出分布基线，但仍主要依赖词元层概率，而非完整轨迹中的跨层表示变化。

**实验想回答的问题**

- RQ1：聚类得到的不同推理状态是否具有可区分的步骤感知推理能量（SARE）分布；在同一状态内，正确与错误思维链的能量分布是否存在系统差异？
- RQ2：将逐步能量变化与状态转移结构汇总为轨迹特征后，能否在不知道最终答案是否正确的前提下离线识别失败的推理轨迹，并优于长度或输出概率等常见置信度信号？

**实验实现**

实验使用LLaMA-3.2-3B、Phi-4-mini和Gemma-3-4B生成思维链并提取内部隐藏状态。RQ1将每个模型产生的全部推理步骤聚为$K=7$个状态，按状态在轨迹中的常见位置排序，以箱线图比较各状态的SARE分布，并以小提琴图比较同一状态中正确与错误轨迹。RQ2把一条轨迹压缩为12维特征：7项能量强度统计量，包括均值、中位数、标准差、范围、波动性、峰和谷；以及5项状态拓扑统计量，包括聚类熵、状态重访次数、不同转移数、转移多样性和最高频状态占比。波动性、峰和谷用于概括相邻步骤能量变化$\Delta E(s_i\to s_{i+1})$。主结果再将Token Count与该向量结合。数据按最终答案正确性分层划分为70%训练、10%验证和20%测试；采用带$\ell_2$正则的逻辑回归，在验证集上选择使F1最大的阈值，并仅在留出的测试集上报告最终表现。所有基线使用相同阈值调优流程，以降低比较协议造成的偏差。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 从SARE错误检测特征中移除Token Count，仅保留能量强度与状态拓扑信息 | 原文称绝对性能略有下降，但总体趋势保持一致；所给正文未提供附录表5—7的具体数值，因此无法量化每个模型和数据集的下降幅度。 | 该消融隔离了表面轨迹长度的贡献。性能下降说明长度与内部动态确实互补；趋势仍保持则支持SARE并非只是Token Count的复杂替代品。不过缺少具体分数、方差和显著性结果，无法判断独立增益究竟有多大或在哪些数据集上最可靠。 | Section 5.3, Reasoning Energy and Token Count as Complementary Signals; Appendix Tables 5–7<br><span class="experiment-evidence">Although absolute performance slightly decreases, the overall trends remain consistent with the results presented here (see Appendix Table 5-7).</span> |

**定性案例**

- 代表性可视化比较了Phi-4-mini/GSM8K、Gemma-3-4B/HotpotQA和LLaMA-3.2-3B/StrategyQA。Phi-4-mini在GSM8K中的错误轨迹于最终推理状态明显偏向较低SARE；LLaMA-3.2-3B在StrategyQA中则是早期检索状态大体重叠，到后期量化与组合状态才分离。该案例说明错误信号具有“状态局部性”，但图形只揭示相关关系，不能确定低能量是错误的原因、结果，还是两者共同受其他因素影响。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper analyzes reasoning effort across individual steps of LLM chain-of-thought trajectories.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`c2c40caa1eadfcc9727047d101f5f1217bf030c896fde53eb42567c441529034`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
