---
title: "[论文解读] WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning"
description: "[arXiv 2607.28418][LLM 效率] WIDE旨在通过逐词元动态选择注意力头组和FFN通道组，并将这种细粒度剪枝与GPU内核协同设计，在更好保留大模型能力的同时，为预填充与解码阶段带来可落地的端到端加速。"
arxiv_id: "2607.28418"
announcement_date: "2026-07-31"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.109763+00:00"
source_sha256: "e3cec44c8e21636f10f1c297d033bf1505b8623376c0aa7c901c6a0587012477"
tags:
  - "LLM 效率"
  - "大语言模型推理"
  - "动态结构化剪枝"
  - "token 级路由"
  - "宽度剪枝"
  - "注意力头组"
  - "FFN 通道组"
  - "GPU 稀疏执行"
  - "预填充与解码"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2607.28418</p>

# WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Hu, Haozhe, Wu, Hao, Yin, Peiran, Han, Chao, Ma, Yunpu, Shen, Xiaoyu</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.28418) · [PDF 下载](https://arxiv.org/pdf/2607.28418) · **关键词** 大语言模型推理, 动态结构化剪枝, token 级路由, 宽度剪枝, 注意力头组, FFN 通道组, GPU 稀疏执行, 预填充与解码<br>
**代码**: [https://github.com/EIT-NLP/LLM-Pruning/tree/main/WIDE](https://github.com/EIT-NLP/LLM-Pruning/tree/main/WIDE)

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

WIDE旨在通过逐词元动态选择注意力头组和FFN通道组，并将这种细粒度剪枝与GPU内核协同设计，在更好保留大模型能力的同时，为预填充与解码阶段带来可落地的端到端加速。

**不用术语来说**：大语言模型处理不同词元时，实际需要的计算量并不相同：简单词元可能只需模型的一部分能力，困难词元则需要更多计算。现有方法要么对所有输入永久删除同一批结构，容易损害困难任务的准确性；要么按输入动态跳过整层或整个子模块，调节尺度又过于粗糙。即使进一步做到更细的动态选择，不规则的计算布局也可能让GPU忙于整理数据而非执行有效运算，导致理论上的计算量下降无法转化为真实速度提升。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出端到端、逐词元的动态宽度剪枝框架WIDE：轻量级路由器为每个词元独立选择与分组查询注意力对齐的注意力头组以及可配置的FFN通道组，将动态结构剪枝从整层或子层跳过推进到层内神经元块级计算分配。
- 作者提出剪枝—内核协同设计：先通过掩码重排把任意逐词元路由模式转换为适合GPU执行的规则布局，再以块级跳过和硬件相关的块内跳过逐步消除无效计算，从而同时覆盖预填充与解码场景。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大语言模型推理的主要成本来自逐层执行 Transformer 中的注意力与前馈网络（FFN）计算。模型剪枝通过跳过或移除冗余结构来降低计算量：静态结构化剪枝为所有输入固定删除相同的层、注意力头或通道，便于现有硬件执行，但无法按输入难度分配算力；动态剪枝则在推理时用轻量路由器决定当前 token 执行哪些结构，适应性更强。现有动态方法主要沿深度维度跳过整层或整个子模块，而本文关注更细的宽度维度，即让每个 token 在层内选择注意力头组和 FFN 通道组，同时要求这种不规则选择能够在 GPU 上转化为实际加速。论文同时覆盖预填充与解码：前者并行处理输入序列，后者在已有 KV 缓存的基础上逐 token 生成。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**结构化剪枝**

以完整层、注意力头、矩阵行列或通道组等规则结构为单位减少计算。与任意删除单个权重相比，这类规则结构更容易映射到 GPU 内核并获得实际吞吐提升。

</div>
<div class="concept-item" markdown="1">

**动态深度剪枝与动态宽度剪枝**

动态深度剪枝决定某个 token 是否执行整层或整个注意力、FFN 子模块；动态宽度剪枝保留该层，但只执行其中一部分注意力头或 FFN 通道。后者的分配粒度更细，却会产生随 token 改变的不规则执行模式。

</div>
<div class="concept-item" markdown="1">

**预填充与解码**

预填充（prefill）一次处理提示词中的多个 token，并建立注意力所需的 KV 缓存；解码（decode）利用该缓存逐步生成新 token。两阶段的并行度和硬件瓶颈不同，因此剪枝方案需要分别支持并验证。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个预训练 Transformer 大语言模型、输入 token 序列以及目标稀疏率，目标是在不永久采用统一静态掩码的前提下，为每层中的每个 token 生成动态路由决策：分别选择要执行的 GQA 对齐注意力头组和可配置大小的 FFN 通道组。被选中的组参与矩阵计算，未选中的组应被 GPU 内核有效跳过；系统输出仍是标准语言模型的隐藏状态或下一 token 概率。问题同时假设路由开销与稀疏执行的不规则性必须受到控制，因为理论计算量下降并不自动等于端到端延迟下降；因此评价对象既包括模型质量保持，也包括预填充和解码场景中的实际执行效率。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathbf{W}_{q}$**

注意力查询投影矩阵；论文沿输出特征维（N 轴）对其进行分组剪枝。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{W}_{o}$**

注意力输出投影矩阵；论文沿输入特征维（K 轴）跳过与被裁剪注意力头组对应的计算。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{W}_{\mathrm{up}},\mathbf{W}_{\mathrm{gate}},\mathbf{W}_{\mathrm{down}}$**

FFN 的上投影、门控投影和下投影矩阵；前两者沿输出特征维分组，后者沿输入特征维与相同通道组对齐。

</div>
<div class="notation-item" markdown="1">

**$N_G$**

一个模块中的路由组数量；图 1 说明路由器输出特征数设为其两倍，以配合 Gumbel-Softmax 形式的组级选择。

</div>

</div>

**直接相关的工作**

- **Mixture-of-Depths（MoD）**: 代表性的 token 级动态深度路由方法：在固定计算预算下，仅让得分最高的 $k$ 个 token 通过每个 Transformer 层。它说明了按 token 自适应分配计算的可行性，但决策单位是整层，无法让只需要部分层内容量的 token 选择细粒度头组或通道组。
- **PolarSparse 与 FastForward**: 二者已探索动态宽度剪枝，但原文将其适用范围概括为仅面向批量解码或预填充等特定场景。WIDE 的问题设置进一步要求统一覆盖预填充和解码，并把 token 级宽度路由与面向 GPU 的块跳过机制共同设计。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

随着模型规模和智能体系统复杂度增长，大语言模型服务的算力与时延成本持续上升。模型剪枝虽然可以减少参数和计算，但部署真正需要的不只是较低的理论计算量：方法还必须在较高稀疏率下维持任务质量，并让减少的运算在现代GPU、高吞吐推理和CUDA Graph执行环境中转化为实际端到端加速。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **静态结构化剪枝**：先用校准数据确定可删除结构，再永久移除整层、注意力或FFN子层、权重矩阵的行列或单个神经元；推理时所有输入共享同一剪枝后网络。其结构固定且规则，因而容易接入现有硬件后端并获得实际吞吐收益。
- **动态深度剪枝**：加入轻量级路由器，根据各个词元的状态决定是否执行或跳过整层、注意力子模块或FFN子模块，使不同输入获得不同计算预算，因此比输入无关的静态剪枝更有机会保留模型质量。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 静态剪枝对每个输入采用完全相同的删除方案，无法利用不同输入乃至不同词元之间的难度差异；在较激进的稀疏率下，困难词元所需的模型容量也会被永久移除，因而容易出现显著准确率下降。
- 现有动态方法主要在深度方向做整层或整子模块的二元决策。若一个词元只需要层内部分注意力头或FFN通道，跳过整个模块会损失仍然有用的计算，而完整执行又浪费预算；进一步采用细粒度逐词元选择时，还会产生不规则掩码、同步的掩码到索引转换以及低效的聚集—分散操作，使理论稀疏性难以形成真实推理加速。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作尚未同时解决模型侧与系统侧的缺口：模型侧缺少能够在每个Transformer块内部按词元分配注意力头组和FFN通道组的可训练结构化剪枝；系统侧缺少一种统一执行机制，能把这种不规则的细粒度路由转换为GPU友好的规则工作布局，并同时服务于计算特征不同的预填充和逐词元解码阶段。

</div>
<div markdown="1"><span>核心问题</span>

能否构建一种端到端可微的逐词元动态宽度剪枝方法，使每个词元在层内只调用所需的注意力头组与FFN通道组，并通过配套GPU内核把细粒度稀疏性转化为预填充和解码中的真实端到端速度收益？

</div>
<div markdown="1"><span>作者直觉</span>

关键思路是把“删掉哪些固定结构”改为“当前词元需要哪些成组能力”：组级选择比跳过整层更精细，又比任意单神经元稀疏更规则，可在质量与硬件效率之间形成可控折中。随后不直接为每个词元构造零散的稀疏张量，而是按路由掩码重排并打包活跃词元，使同一路由组的有效工作形成与GPU计算块对齐的连续前缀；内核便可先跳过完全无效的计算块，再跳过块内无效的数据加载和张量核片段。直观地说，WIDE先让模型按需“选部件”，再把零散选择整理成GPU擅长批量处理的形状。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

WIDE把标准Transformer层的注意力与前馈网络（FFN）按“宽度”切成可跳过的连续计算组，并为每个token单独预测哪些组执行。输入为隐藏表示$\mathbf{X}\in\mathbb{R}^{B\times T\times D}$；轻量瓶颈路由器输出注意力头组与FFN通道组的二元掩码，掩码分别控制注意力输出头组以及FFN中间维度上的计算。训练采用两阶段方案：先冻结原模型、只用校准数据训练路由器，再可选地通过LoRA微调线性层；语言建模损失负责维持任务能力，稀疏度损失使实际跳过比例接近预算$S$。

推理时，WIDE没有直接为每个token收集不同的权重子集，因为这会产生庞大的中间张量并破坏CUDA Graph。它改为按每个计算组对token掩码排序，把需要同一组计算的token聚集为连续区间，再在定制GEMM和FlashAttention内核中分三级跳过：先跳过完全无效的CTA块，再跳过无效的激活加载包，最后跳过无效的MMA矩阵乘片段。直观地说，模型先为每个词挑选必要的“注意力头和神经元块”，随后把选择相同模块的词临时排到一起，使GPU仍能进行规则的分块计算，而不是处理大量零散的小任务。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 划分可剪枝的原子计算组

注意力侧以兼容GQA的查询头组为原子，令每个键值头对应的组宽为$G=D/H_k=(H_q/H_k)d$；FFN侧沿中间维度$D'$把Up、Gate和Down投影共同划分为连续的$G$通道组。一个组的掩码同时作用于相关联的算子，注意力掩码只门控注意力输出及后续输出投影，不剪除$\mathbf{W}_k$和$\mathbf{W}_v$，以避免破坏KV缓存。

<div class="method-step__io" markdown="1">

**输入**：每层隐藏表示$\mathbf{X}\in\mathbb{R}^{B\times T\times D}$、注意力投影和FFN投影参数，以及组大小$G$。<br>
**输出**：注意力组掩码$\mathcal{M}_{\mathrm{attn}}\in\{0,1\}^{B\times T_q\times H_k}$和FFN组掩码$\mathcal{M}_{\mathrm{ffn}}\in\{0,1\}^{B\times T\times D'/G}$所对应的结构化执行单元。

</div>

**直观理解**：这一步先规定“最小能关掉多大一块计算”：注意力按共享同一KV头的查询头成组，FFN按连续神经元通道成组。组越小，选择越精细但调度成本越高；组越大，更容易获得GPU加速但可能误删更多有用计算。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 逐token生成动态路由掩码

瓶颈路由器先用$\mathbf{W}_1\in\mathbb{R}^{D\times r}$降维，再用$\mathbf{W}_2\in\mathbb{R}^{r\times 2N_G}$为每组产生“执行/跳过”两个logit。训练时用硬Gumbel-Softmax得到可反向传播的近似二元决策，推理时直接取两类logit的最大值，其中类别$0$表示执行、类别$1$表示跳过。

<div class="method-step__io" markdown="1">

**输入**：当前层每个token的隐藏向量$\mathbf{X}$以及注意力或FFN的组数$N_G$。<br>
**输出**：针对每个token、每一层和每个宽度组的二元掩码$\mathcal{M}$。

</div>

**直观理解**：路由器相当于每层前的轻量开关面板：它查看当前词的表示，再决定哪些注意力头组或FFN通道组值得计算。瓶颈结构把判断成本压低，使节省的主体计算不至于被路由开销抵消。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 两阶段恢复模型质量并约束稀疏度

第一阶段冻结原模型全部参数，仅优化路由器；第二阶段为可选步骤，在各层线性模块中加入LoRA低秩增量并继续调优。两个阶段都联合最小化语言建模损失$\mathcal{L}_{\mathrm{LM}}$与全层平均稀疏率偏离目标$S$的惩罚。

<div class="method-step__io" markdown="1">

**输入**：预训练模型、校准数据、目标稀疏率$S$以及路由掩码。<br>
**输出**：满足目标计算预算、且尽量保持原模型预测能力的路由器；可选LoRA阶段还输出适应剪枝模式的低秩参数。

</div>

**直观理解**：先只训练“开关”，可以低成本学会把计算分给不同token；若质量仍不足，再让LoRA小幅调整原网络对新执行模式的适应性。稀疏度惩罚防止路由器为了降低语言建模损失而把所有组都打开。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按组重排掩码与token行

对每个组$g$，沿token行维度$M$对$\mathcal{M}_{:,g}$降序排序，得到活动项集中在前缀的$\widetilde{\mathcal{M}}_{:,g}$及行索引$\mathcal{I}_{:,g}$；索引用于融合地收集输入行并将输出散射回原顺序。排序后除至多一个边界tile外，每个CTA行tile都变为全活动或全不活动。

<div class="method-step__io" markdown="1">

**输入**：展平后的token行、二元路由矩阵$\mathcal{M}\in\{0,1\}^{M\times N_G}$以及每组的剪枝宽度$G$。<br>
**输出**：规则化的分组掩码$\widetilde{\mathcal{M}}$、重排索引$\mathcal{I}$以及适合tile化GPU内核处理的token布局。

</div>

**直观理解**：不同token原本会打开不同模块，访问模式十分零散；排序把需要同一模块的token排到连续位置。这样GPU看到的是少量整齐的连续计算块，而不是为每个token单独复制权重和启动小算子。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 逐token路由及训练/推理二元化

$$
\mathcal{R}=\operatorname{reshape}(\mathbf{X}\mathbf{W}_{1}\mathbf{W}_{2})\in\mathbb{R}^{B\times T\times N_G\times 2},\qquad \mathcal{M}=\begin{cases}\mathbf{1}\!\left[\arg\max_{c\in\{0,1\}}\mathcal{R}_{\ldots,c}=0\right],&\text{inference},\\ \operatorname{GumbelSoftmax}_{\tau}^{\mathrm{hard}}(\mathcal{R})_{\ldots,0},&\text{training}.\end{cases}
$$

**符号说明**

- $\mathbf{X}$：当前Transformer层的输入隐藏表示，形状为$B\times T\times D$。
- $\mathbf{W}_{1}$：路由器降维矩阵，形状为$D\times r$。
- $\mathbf{W}_{2}$：路由器输出矩阵，形状为$r\times 2N_G$，为每组产生两个类别logit。
- $\mathcal{R}$：逐批次、逐token、逐组的二分类路由logit张量。
- $N_G$：每个算子中的候选计算组数；注意力为$D/G$，FFN为$D'/G$。
- $r$：路由器瓶颈维度，远小于模型隐藏维度$D$。
- $\mathcal{M}$：二元执行掩码；值$1$对应类别$0$，表示执行该组，值$0$表示跳过。
- $\tau$：硬Gumbel-Softmax的温度，用于控制训练时采样分布的尖锐程度。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分以低秩瓶颈为每个token的每个计算组产生“执行”和“跳过”分数。第二部分规定训练时使用具有离散前向结果、但仍可近似传递梯度的硬Gumbel-Softmax，推理时则直接选择分数更高的类别，从而把可训练路由转换为真实二元开关。<br>
**原文位置**：第3.1节，公式(4)与公式(5)

</div>

</div>

<div class="equation-block" markdown="1">

#### 语言建模与目标稀疏度联合目标

$$
\mathcal{L}=\mathcal{L}_{\mathrm{LM}}+\alpha\left\lvert S-\frac{1}{2N}\sum_{i=1}^{N}\left[\left(1-\frac{1}{\lvert\mathcal{M}_{\mathrm{attn}}^{i}\rvert}\sum\mathcal{M}_{\mathrm{attn}}^{i}\right)+\left(1-\frac{1}{\lvert\mathcal{M}_{\mathrm{ffn}}^{i}\rvert}\sum\mathcal{M}_{\mathrm{ffn}}^{i}\right)\right]\right\rvert
$$

**符号说明**

- $\mathcal{L}$：两阶段训练所最小化的总损失。
- $\mathcal{L}_{\mathrm{LM}}$：标准语言建模损失，用于保持模型的token预测能力。
- $\alpha$：稀疏度约束的权重超参数。
- $S$：预先指定的目标稀疏率，即希望跳过的平均计算比例。
- $N$：Transformer层数。
- $\mathcal{M}_{\mathrm{attn}}^{i}$：第$i$层注意力组的二元执行掩码，其中均值表示执行比例。
- $\mathcal{M}_{\mathrm{ffn}}^{i}$：第$i$层FFN组的二元执行掩码，其中均值表示执行比例。
- $\lvert\mathcal{M}\rvert$：相应掩码包含的元素总数。

<div class="equation-explanation" markdown="1">

**直观理解**：掩码均值是组的平均执行率，因此$1$减去该均值就是平均跳过率；公式先在每层汇总注意力与FFN的跳过率，再与预算$S$比较。绝对值惩罚只约束全模型平均稀疏率，这给路由器留下了跨token、跨层和跨模块重新分配计算的空间，而语言建模损失决定这种分配是否保留预测能力。<br>
**原文位置**：第3.2节，公式(6)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：总目标同时解决两个可能冲突的问题：$\mathcal{L}_{\mathrm{LM}}$要求稀疏模型继续预测正确，稀疏项则要求注意力与FFN的全层平均跳过率接近预算$S$。第一阶段只有路由器参数接收更新，因此优化的核心是学习“对什么token打开什么组”；可选第二阶段固定同一目标，但允许LoRA低秩参数调整各线性模块，使基座模型适应路由造成的激活分布和可用通道变化。该约束针对平均预算，而不是强迫每个token具有相同活动组数，这正是WIDE能进行自适应计算分配的前提。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 硬件对齐的注意力与FFN剪枝单元**

注意力采用头作为最小原子，并在GQA中按$H_q/H_k$个查询头组成一组，使$\mathcal{M}_{\mathrm{attn}}$能与现有解码优化及KV缓存兼容。FFN沿$D'$使用属于$\mathcal{T}=\{2^k\mid k\in\mathbb{Z}_{\geq 4}\}$的连续组宽$G$，同一掩码贯穿Up/Gate输出与Down输入，避免不同投影产生不一致的稀疏结构。

> 直观理解：动态剪枝只有在“关闭的部分”恰好对应GPU可跳过的规则计算块时才可能真正加速。该模块因此不是任意删神经元，而是把模型结构、GQA/KV缓存约束和矩阵乘分块方式同时纳入组设计。

**2. 瓶颈式逐token路由器**

每层路由器通过两层线性映射把维度$D$的隐藏状态变成$N_G$组二分类logit，瓶颈维度满足$r\ll D$；训练与推理共享同一决策语义，但分别使用硬Gumbel-Softmax和argmax。注意力取$N_G=D/G$，FFN取$N_G=D'/G$。

> 直观理解：该模块把统一的静态剪枝比例改成依赖token内容的计算分配：简单token可以少用一些组，困难token可以保留更相关的组。训练阶段的连续近似解决了离散开关通常无法直接用梯度学习的问题。

**3. 掩码重排与多层级跳过内核**

对每个路由组独立排序token行，使活动行形成连续前缀，并通过索引$\mathcal{I}$完成融合收集和回写；内核随后在$S_0=BM$、$S_1=S_{\mathrm{ld}}$和$S_2=S_{\mathrm{mma}}$三种粒度上计算是否执行。$S_0$提供与硬件无关的CTA早退，$S_1$和$S_2$分别适配具体GPU的加载机制与MMA指令。

> 直观理解：朴素方案会给每个token显式收集不同权重子集，产生规模约为$O(pMNK)$的中间存储并损害权重复用。重排方案只改变token处理顺序，不复制token专属权重，因此能够保留接近稠密内核的规则主循环。

**训练与推理**

训练阶段首先从预训练Transformer出发，在每层注意力和FFN前接入瓶颈路由器，并根据组宽$G$确定$N_G$。路由器阶段冻结基座模型，使用校准数据和硬Gumbel-Softmax联合优化语言建模损失与稀疏约束；之后可选地向所有基座线性模块加入LoRA，在保留动态路由的条件下继续恢复质量。原文称第二阶段为可选，因此仅使用校准数据时的核心产物是路由器，而非完整模型权重重训练。

推理同时覆盖prefill和逐token decode。每层先用argmax产生注意力与FFN掩码，再对每个组的token行排序；融合内核依据排序索引读取激活、共享原始权重tile，并按CTA、加载和MMA三级谓词跳过无效工作，最后散射回原token顺序。注意力路由不移除$\mathbf{W}_k$或$\mathbf{W}_v$对应的KV缓存内容，因此不会因后续token可能需要某个组而发生缓存逐出；GEMM-MN、GEMM-K和Attention三类内核共同覆盖Q/Up/Gate、O/Down和FlashAttention计算。

**复现信息**

公平复现需要保留三项关键设计。第一，注意力组宽必须遵循GQA共享关系$G=D/H_k=(H_q/H_k)d$，而FFN的$G$应选自矩阵乘常用tile宽集合$\mathcal{T}$；较小$G$提高路由灵活性，较大$G$更利于硬件跳过。第二，路由器使用$r\ll D$的瓶颈，原文给出的典型候选为$r\in\{16,32\}$，训练类别约定必须保持类别$0$为执行、类别$1$为跳过。

第三，实际加速依赖掩码重排与融合内核，不能把逐token掩码简单实现为PyTorch gather-scatter。后者在N轴或K轴宽度剪枝中会物化token专属权重子集$\mathbf{B}_{\mathrm{sub}}$，中间存储的主导项达到$O(pMNK)$；WIDE通过排序后的共享权重tile和融合回写避免该张量。CTA粒度$S_0=BM$与硬件无关，而加载粒度$S_{\mathrm{ld}}$和MMA粒度$S_{\mathrm{mma}}$必须针对目标GPU的加载及矩阵乘指令实现；因此算法掩码相同并不意味着不同硬件上的内核细节或收益完全相同。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- RedPajama-1T 的一个子集：同时作为路由器校准语料和 LoRA 恢复语料。原文未说明该子集的样本数、token 数或具体划分，因此无法判断训练数据规模及是否存在评测数据污染。
- WikiText2：用于报告困惑度，主要检验剪枝后模型对连续自然语言的概率建模能力；评测最大上下文长度为 4096。原文未明确报告所用 split。
- 七项零样本分类基准的集合：ARC-Easy、ARC-Challenge、BoolQ、WinoGrande、PIQA、OpenBookQA 和 HellaSwag。实验报告七项任务的平均准确率及相对稠密模型的性能保留率，用于综合考察常识推理、问答和文本续写等能力；各任务样本规模与 split 在节选中未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**WikiText2 困惑度（PPL）**

衡量模型给真实文本分配概率的能力；困惑度越低，说明模型对下一个 token 的预测越可靠。该指标对模型退化较敏感，但不能直接代表问答或推理能力。 （越低越好，因为较低困惑度表示真实文本在模型下具有更高的平均预测概率。）

</div>
<div class="metric-item" markdown="1">

**七项零样本任务平均准确率及性能保留率**

平均准确率是七个分类基准准确率的算术汇总；性能保留率将剪枝模型平均准确率与原始稠密模型比较，用于消除不同骨干模型绝对能力的部分差异。平均值可能掩盖单项任务上的明显退化。 （越高越好；准确率越高表示答对的样本比例越大，保留率越接近 $100\%$ 表示越接近稠密模型。）

</div>
<div class="metric-item" markdown="1">

**推理加速比与吞吐量**

算子级实验在 CUDA Graph replay 下报告 TFLOPs 或相对稠密算子的速度；端到端实验测量单步首 token 时间（TTFT）和每输出 token 时间（TPOT），并换算为预填充和解码加速比。前者检验稀疏内核本身，后者包含路由、内核初始化、KV 投影和图启动等固定开销。 （加速比和吞吐量越高越好；加速比大于 $1$ 才表示相对稠密基线真正缩短了运行时间。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 仅校准、Llama3.1-8B、目标稀疏率 $50\%$

<div class="result-value" markdown="1">

WIDE（$G=32$）取得 61.84 的七任务平均准确率和 $86.42\%$ 的性能保留率，WikiText2 困惑度为 14.15；最强非 WIDE 基线 DDP 的平均准确率为 53.04，因此 WIDE 高出 8.80 个百分点。与动态深度基线 SkipGPT 的 42.51 相比，差距为 19.33 个百分点。

</div>

这说明在不进行 LoRA 权重恢复时，把动态决策细化到注意力头组和 FFN 通道组，比固定宽度剪枝或跳过整层更能承受激进剪枝。它支持“动态宽度粒度更合适”的解释，但不能单独证明收益全部来自 token 级路由，因为 WIDE 与各基线的路由结构、优化目标和内核设计并未逐项控制。

<div class="result-source" markdown="1">

来源：第 4.2 节 Calibration-only Results，表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Llama3.1-8B, WIDE improves over the strongest non-WIDE baseline by 8.80 average-accuracy points (61.84 vs. 53.04).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 统一 LoRA 恢复、两种骨干模型、目标稀疏率 $50\%$

<div class="result-value" markdown="1">

WIDE 的最佳配置在 Llama3.1-8B 上达到 64.82 平均准确率，在 Llama3.2-3B 上达到 58.77；相对 SkipGPT 分别提高 3.22 和 4.44 个百分点，相对 DDP 分别提高 10.19 和 9.89 个百分点。对应性能保留率均约为 $90\%$。

</div>

共同的 LoRA 恢复会缩小不同剪枝方法之间的差距，但 WIDE 仍领先，说明结果不只来自恢复训练能修补其误差。这里的结论限定于给定 RedPajama 恢复语料和 LoRA 预算，不能推出在完整微调、其他模型家族或不同数据域中仍保持相同优势。

<div class="result-source" markdown="1">

来源：第 4.2 节 LoRA Results，表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Its best configurations reach 64.82 average accuracy on Llama3.1-8B and 58.77 on Llama3.2-3B, improving over SkipGPT by 3.22 and 4.44 points, and over DDP by 10.19 and 9.89 points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### NVIDIA RTX 5090 上的端到端推理，Llama3.1-8B，目标稀疏率 $50\%$

<div class="result-value" markdown="1">

最佳配置相对稠密模型实现 $1.68\times$ 的预填充加速和 $1.55\times$ 的解码加速；在 $0\%$ 稀疏率下，$G\leq128$ 的最佳设置仍保留稠密吞吐量的 $98.60\%$。

</div>

这验证了逐 token 路由不仅减少理论 FLOPs，也能在单一高端 GPU 和所测工作负载上转化为端到端时延收益；接近稠密的 $0\%$ 稀疏吞吐量还表明路由与定制内核的基本开销较小。不过，该结果不是跨硬件、跨批大小或跨服务并发度的普遍吞吐结论，而且端到端加速明显低于仅看稀疏计算量时的理想上界。

<div class="result-source" markdown="1">

来源：第 4.3 节 Performance over Sparsity，图 8

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At 50% sparsity, the best configuration accelerates prefill by 1.68× and decode by 1.55×.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 硬件结论主要来自 NVIDIA RTX 5090（sm120），且端到端实验节选未系统列出不同批大小、输入与输出长度、并发请求及其他 GPU 架构的结果。WIDE 依赖 CuTe/CUTLASS、定制 JIT 和细粒度跳过能力，因此所报 $1.68\times$ 与 $1.55\times$ 加速不能直接外推到数据中心 GPU、通用推理框架或生产服务负载。
- 质量实验只覆盖 Llama3.1-8B、Llama3.2-3B、一个未说明规模的 RedPajama 子集以及七项零样本分类任务。各方法虽共享恢复配置，但校准阶段沿用各自原始训练预算，计算成本并非严格等量；同时，平均准确率会隐藏单任务退化，节选也未提供方差、重复运行或显著性检验。因此结果支持所测设置下的优势，但不足以证明跨模型规模、长上下文、生成质量和其他领域的普遍有效性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Shortened LLaMA 与 CoopPruner：代表静态深度剪枝，即对所有输入固定删除部分层；它们用于判断 WIDE 的收益是否来自避免输入无关的整层裁剪。
- SliceGPT、Týr-the-Pruner 与 DDP：代表静态宽度剪枝，即固定裁剪隐藏维度、注意力或 FFN 宽度。其中 DDP 是表中最强的静态宽度对照，适合检验逐 token 动态分配是否优于固定宽度结构。
- D-LLM：动态剪枝对照，用于比较 WIDE 与已有输入自适应方法的质量保持能力；表中结果也显示，具有“动态”性质本身并不足以保证高稀疏率下的稳定性。
- SkipGPT：代表逐输入或逐 token 的动态深度路由，通过跳过层减少计算。作者还增大其路由器秩 $r$ 以匹配 WIDE 的路由容量，因此它是区分“动态深度选择”与“动态宽度选择”的关键对照。

**实验想回答的问题**

- 在相同目标稀疏率、骨干模型和恢复训练条件下，细粒度的逐 token 动态宽度剪枝是否比静态深度剪枝、静态宽度剪枝和动态深度剪枝更能保持语言建模能力与下游零样本准确率？
- WIDE 的质量与实际加速如何随目标稀疏率和剪枝组大小 $G$ 变化，并且其路由、稀疏算子及固定开销能否在预填充和解码阶段转化为端到端收益？

**实验实现**

骨干模型为 Llama3.1-8B 和 Llama3.2-3B。路由器校准与 LoRA 恢复各训练 10000 步，批大小为 16，最大序列长度为 4096，使用 4 张 NVIDIA A100-SXM4-40G；路由阶段将 Gumbel-Softmax 温度从 5 线性退火至 0.5，并设稀疏约束权重 $\alpha=20$。LoRA 使用秩 $r=16$、缩放参数 $\alpha=32$ 和 0.1 dropout。所有方法共享 RedPajama 子集和 LoRA 配置，但校准阶段沿用各方法原始训练预算，因此校准计算量并非完全一致。质量评测由 lm-evaluation-harness 完成，最大上下文长度为 4096。

推理主要在 sm120 架构的 NVIDIA RTX 5090 上评测。算子级测试使用 Triton benchmark 接口和 CUDA Graph replay；端到端测试采用 ELANA 风格分析工具测量 TTFT 与 TPOT。WIDE 分别实现 Triton、Tilelang 和基于 CUTLASS CuTe、TVM-FFI JIT 的内核，其中 CuTe 能在矩阵 $\mathbf{A}$ 加载和 MMA 执行时进行块内跳过，较粗粒度 DSL 只能按 CTA 跳过。因而实验同时检查“理论上少算了多少”和“硬件实际能否跳过这些计算”。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Llama3.1-8B、$50\%$ 稀疏率，固定注意力组大小 $G_{attn}=512$，改变 FFN 组大小 $G_{ffn}$ | 仅校准时，将 $G_{ffn}$ 从 16 增至 256，平均准确率从 62.89 降至 60.27，即下降 2.62 个百分点；LoRA 后将 $G_{ffn}$ 从 16 增至 512，平均准确率从 64.92 降至 63.79，即下降 1.13 个百分点。 | 该实验隔离了 FFN 路由粒度：较小组能按 token 更精细地保留通道，因此校准阶段质量通常更高；LoRA 可补偿较粗分组造成的大部分损失。它同时揭示实际设计取舍，因为后续内核结果表明过小的组难以摊薄 GPU 流水线开销，所以最高准确率配置未必是最高速度配置。 | 第 4.3 节 Effects of Pruning Group，图 5（正文称 Table 5）<br><span class="experiment-evidence">Table 5 shows that quality is robust across G, where increasing Gffn from 16 to 256 at 50% sparsity decreases average accuracy by 2.62 points, and changing Gffn from 16 to 512 after LoRA tuning only lowers accuracy by 1.13 points, with similar trends at Table 2 and attention side.</span> |
| Llama3.1-8B、$50\%$ 目标稀疏率、$G=128$ 的层级时延分解，预填充长度 $T=16384$、批大小 $B=1$ | 可加速算子路径的平均加速为预填充 $1.82\times$、解码 $1.92\times$；不可消除或尚未加速的部分约占预填充总时延的 $16.7\%$、解码总时延的 $29.1\%$。 | 该分析隔离了稀疏内核本身与模型其余部分，解释为什么减少约一半目标计算并不会自动产生完整的 $2\times$ 端到端加速。解码固定开销比例更高，因此即使稀疏算子接近理想速度，整体收益仍被 KV 投影、逐元素操作、图启动和路由成本限制。这是时延归因分析，而不是移除某个模型组件后重新测量质量的传统消融。 | 第 4.3 节 The Upper Bound of Speedup，图 4<br><span class="experiment-evidence">These components account for about 16.7% of total prefill latency and 29.1% of total decoding latency, which explains why the layer-wise speedup remains below the theoretical speedup.</span> |

**定性案例**

- 在一个 HellaSwag 样例中，FFN 路由器倾向于保留“boy”“running”“track”等语义内容词，而更常跳过“A”“a”“the”等冠词，尤其发生在平均 FFN 稀疏率较高的第 9 至 11 层。该可视化与“路由具有语义感知性”的作者解释一致，但它只展示代表性个案，不能证明词类与计算分配之间存在稳定因果关系；层级统计还显示总体稀疏率为 $47.3\%$ 时，注意力和 FFN 的稀疏率分别为 $66.2\%$ 与 $28.5\%$，说明模型学习了明显不均匀的模块预算。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces token-level dynamic width pruning and kernel co-design to accelerate LLM prefill and decoding.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`e3cec44c8e21636f10f1c297d033bf1505b8623376c0aa7c901c6a0587012477`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
