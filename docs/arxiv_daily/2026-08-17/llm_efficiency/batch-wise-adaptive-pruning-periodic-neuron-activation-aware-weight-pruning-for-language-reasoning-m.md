---
title: "[论文解读] Batch-wise Adaptive Pruning: Periodic Neuron Activation-Aware Weight Pruning for Language Reasoning Model"
description: "[arXiv 2608.14003][LLM 效率] 本文研究如何在大推理模型的批量推理中，以无需训练和外部校准的方式动态剪枝，并通过周期性 top-$k$ 选择与激活记忆缓解共享掩码造成的稀疏率失控和推理精度下降。"
arxiv_id: "2608.14003"
announcement_date: "2026-08-17"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-17T02:01:46.018485+00:00"
source_sha256: "44f23b5ea52445c9424748ed83d419b22c915ff69bea1a8b397559eec78b2549"
tags:
  - "LLM 效率"
  - "LLM Reasoning"
  - "大型推理模型"
  - "批量推理"
  - "结构化神经元剪枝"
  - "自适应剪枝"
  - "top-$k$选择"
  - "激活记忆"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2608.14003</p>

# Batch-wise Adaptive Pruning: Periodic Neuron Activation-Aware Weight Pruning for Language Reasoning Model

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-17</span>
<span><strong>作者</strong> Yongmin Kim, Shota Takashiro, Yusuke Iwasawa, Takeshi Kojima, Yutaka Matsuo</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: The University of Tokyo</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.14003) · [PDF 下载](https://arxiv.org/pdf/2608.14003) · **关键词** 大型推理模型, 批量推理, 结构化神经元剪枝, 自适应剪枝, top-$k$选择, 激活记忆<br>
**代码**: [https://github.com/matsuolab/batch-wise-prune](https://github.com/matsuolab/batch-wise-prune)

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

本文研究如何在大推理模型的批量推理中，以无需训练和外部校准的方式动态剪枝，并通过周期性 top-$k$ 选择与激活记忆缓解共享掩码造成的稀疏率失控和推理精度下降。

**不用术语来说**：大推理模型需要生成很长的思考过程，推理成本很高；实际服务通常把多个请求合成一批处理以提高吞吐量，但一批请求在 GPU 上必须共用同一套被保留或跳过的神经元。不同请求的重要神经元并不完全相同，现有方法合并它们的激活后，原先设定的筛选标准便可能失效，导致跳过的计算量偏离预期，甚至误删完成推理所需的神经元。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者识别并实证分析了现有免训练剪枝在批量推理中的失效机制：静态剪枝无法跟踪长思维链中持续变化的激活，而基于离线阈值的自适应剪枝在跨样本聚合后会出现激活分布偏移，使实际稀疏率偏离目标。
- 作者提出面向批量推理的周期性 top-$k$ 剪枝，并加入跨更新阶段累积重要性的激活记忆：前者直接固定每次保留的神经元数量并降低频繁选择的开销，后者保留在长推理过程中周期性重新激活的神经元。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大型语言模型推理阶段的结构化神经元剪枝，重点关注大型推理模型（Large Reasoning Models, LRMs）在批量推理中的计算效率。LRMs通过生成较长的链式思维过程处理复杂任务，但生成步数增加了推理成本；批量推理将多个请求同时处理，以提高GPU吞吐量，却要求同一批样本共享一个剪枝掩码。本文的问题因此位于三个约束的交叉处：模型需要根据运行时激活动态选择神经元，选择结果需要适用于整个批次，还必须避免每个生成令牌都重新计算掩码所带来的额外开销。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**结构化神经元剪枝**

剪枝通过移除模型中被认为不重要的参数或神经元来减少计算量。本文采用结构化剪枝，即按完整神经元或相应矩阵列进行选择，因此可以使用标准矩阵运算获得加速，而不依赖专用稀疏硬件或额外训练。

</div>
<div class="concept-item" markdown="1">

**批量推理与共享掩码**

批量推理把多个输入样本作为一个批次同时送入模型，以提高服务吞吐量。由于GPU上的批量矩阵运算需要统一计算结构，批次内不同样本不能各自使用不同的神经元选择结果，通常必须共享一个剪枝掩码。

</div>
<div class="concept-item" markdown="1">

**静态剪枝与自适应剪枝**

静态剪枝在生成开始前确定神经元保留模式，并在整个推理过程中复用；自适应剪枝则依据生成期间实时出现的激活值动态更新模式。推理任务的激活模式会随长链式思维过程变化，因此静态模式可能过时，但自适应模式在批量场景下会遇到样本间选择不一致和更新开销问题。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定语言模型、输入请求批次及目标稀疏率，模型在自回归解码过程中为每个样本产生运行时激活，并据此评估前馈神经网络（FFN）中各神经元的重要性。由于批次中的所有样本必须使用一个共享掩码，方法先将样本级重要性分数聚合为单个神经元分数向量，再选择应保留的神经元，并输出后续生成所使用的稀疏计算结果。本文假设可以访问推理时的激活值，不进行额外训练；目标是在批量大小大于一、尤其是批量大小为四的推理设置下，使实际稀疏率接近目标值，同时尽量保持推理任务准确率和获得端到端加速。现有方法通常使用离线校准阈值，而本文关注聚合后激活分布发生变化导致阈值失配的问题。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathbf{Z}$**

FFN层中的激活矩阵；其行或列对应批次样本与神经元维度，具体排列方式由模型实现决定。论文用它展示神经元在长序列生成中的激活大小、重复激活现象及其周期性。

</div>
<div class="notation-item" markdown="1">

**$k$**

每次掩码更新时保留的神经元数量，通常由目标稀疏率和该层神经元总数共同决定。top-$k$选择保留聚合重要性分数最高的$k$个神经元。

</div>
<div class="notation-item" markdown="1">

**$s$**

目标稀疏率或实际稀疏率所对应的比例。目标稀疏率规定希望跳过的计算规模，实际稀疏率则表示运行中真正被剪去的计算比例；阈值分布漂移可能使二者不一致。

</div>
<div class="notation-item" markdown="1">

**$M$**

共享剪枝掩码，用于指示当前批次和更新阶段中哪些神经元被保留。它必须同时作用于批次内所有样本，并会按照周期性策略进行更新。

</div>

</div>

**直接相关的工作**

- **TEAL（Liu et al., 2025）**: TEAL是本文重点比较的训练无关自适应剪枝方法之一，依据运行时激活幅值和离线校准阈值动态选择神经元。本文指出，批量推理先聚合多个样本的激活后，聚合分布与离线校准分布不一致，导致实际稀疏率偏移并使推理准确率显著下降；本文以周期性top-$k$选择替代阈值选择，并加入激活记忆以适应长期生成。
- **CATS（Lee et al., 2024）**: CATS代表依据运行时激活动态选择神经元的自适应剪枝路线，能够利用输入相关的激活模式，但批量推理要求不同样本共享一个掩码，因此需要先聚合样本级重要性。本文将该类方法与静态剪枝区分开来，核心研究对象是自适应选择在共享掩码和长链式思维生成下的适配问题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大推理模型依靠较长的思维链处理复杂任务，生成长度使推理计算成本进一步上升；生产系统又必须采用批量推理来获得较高吞吐量。因此，所需方法不仅要减少前馈网络中的实际计算，还必须适应一批样本共享剪枝掩码的 GPU 执行方式，并在长时间生成期间保持推理所需的神经元。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **静态剪枝（如 Wanda、Griffin）**：在解码开始前，根据外部校准数据或当前提示确定固定剪枝模式，随后在整个生成过程中重复使用同一掩码。其优点是运行时无需反复选择神经元，但不能根据后续 token 的激活变化调整计算路径。
- **阈值式自适应剪枝（如 CATS、TEAL）**：根据运行时激活幅度动态判断神经元是否重要，并将重要性分数与预先在外部语料上校准的阈值比较；在批量推理中，需要先把多个样本的激活聚合为一个分数向量，再生成全批次共享的掩码。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 静态掩码在生成前即被固定，而推理任务的激活模式会随长思维链不断演化；因此早期选出的神经元集合会逐渐过时，无法持续覆盖后续推理阶段需要的计算路径。
- 现有自适应方法的阈值是针对未聚合或单样本激活分布离线校准的；批内聚合改变分数分布后，同一阈值不再对应预定稀疏率，导致实际剪枝比例漂移并损害准确率。若改为每个解码步执行 top-$k$ 选择，虽然能固定稀疏率，但选择开销又可能抵消剪枝带来的加速。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有方法没有同时满足三个条件：在批量共享掩码下精确控制稀疏率、跟踪长推理过程中不断变化且可能周期性重现的神经元重要性，以及把动态选择成本控制在足以获得实际推理加速的范围内。该缺口主要存在于高稀疏率的批量推理场景，而不是所有部署条件；原文指出低稀疏率或批大小为 $1$ 时，既有 TEAL 仍可能更合适。

</div>
<div markdown="1"><span>核心问题</span>

能否仅利用生成期间可访问的中间激活，在不训练模型、也不依赖外部校准语料的条件下，为一批推理请求周期性构造共享权重剪枝掩码，使实际稀疏率保持在指定目标附近，同时在选择开销、推理准确率和端到端速度之间取得可用平衡？

</div>
<div markdown="1"><span>作者直觉</span>

top-$k$ 选择关心的是聚合分数的相对排序，而不是其绝对数值是否仍匹配某个离线阈值，所以批内聚合即使改变分布尺度，也不会改变必须保留固定数量神经元这一约束；把选择操作改为每隔一段时间执行，则可摊薄排序成本。与此同时，长推理中的关键神经元可能暂时沉寂后再次激活，激活记忆把过去阶段的重要性带到下一次更新，相当于避免仅凭当前短窗口把反复参与推理的神经元过早删除。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法是一种面向批量自回归推理的、无需训练的结构化神经元剪枝方案，剪枝对象是 Transformer 中参数和计算量占比较高的门控多层感知机（gated MLP）。给定一个批次的提示词及随后生成的 token，方法先从各层中间激活估计每个前馈神经元对当前批次的重要性，再让整个批次共享同一个保留掩码。保留数量由目标稀疏率 $\rho$ 明确控制，因此选择依据是聚合分数的 top-$k$ 排名，而不是依赖预先校准且可能随批量分布变化而失效的固定阈值。

完整推理过程分为输入统计、初始稠密探索和周期性稀疏/稠密交替三个阶段。稠密阶段使用完整 MLP，并收集能够反映当前生成上下文的激活；稀疏阶段只加载和计算被掩码保留的权重行、列。跨阶段的激活记忆通过逐元素最大值保存曾经显著的神经元，随后周期性重算 top-$k$ 掩码，使方法既不会只依据提示词做一次静态判断，也能跟随长推理过程中神经元激活模式的变化。直观地说，它会定期短暂恢复完整模型来“侦察”当前需要哪些神经元，再用较小的 MLP 持续生成一段时间。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 门控 MLP 激活提取

对每个隐藏状态 $\mathbf{x}$ 计算门控分支 $\sigma(\mathbf{W}_g\mathbf{x})$ 与数值分支 $\mathbf{W}_1\mathbf{x}$ 的逐元素乘积，得到前馈激活 $\mathbf{z}\in\mathbb{R}^{D_{\mathrm{FF}}}$。批量处理整个序列后形成激活矩阵 $\mathbf{Z}\in\mathbb{R}^{T\times D_{\mathrm{FF}}}$。

<div class="method-step__io" markdown="1">

**输入**：当前 Transformer 层的隐藏状态序列 $\mathbf{X}\in\mathbb{R}^{T\times D}$；其中 $T$ 是有效 token 数，$D$ 是隐藏维度。<br>
**输出**：每层、每个有效 token 对应的前馈神经元激活矩阵 $\mathbf{Z}$。

</div>

**直观理解**：门控 MLP 可看成一组并行的中间神经元；这里先记录各神经元在当前文本上被使用的强弱，作为后续删减计算的依据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 样本级重要性评分

先对每个 token 的激活向量做行向 $\ell_2$ 归一化，再对每个神经元跨 token 的归一化激活做列向 $\ell_2$ 聚合，并除以 $\sqrt{T}$ 消除不同阶段 token 数量造成的长度偏差。由此得到阶段 $n$ 的样本级分数 $\mathbf{s}_n\in\mathbb{R}^{D_{\mathrm{FF}}}$。

<div class="method-step__io" markdown="1">

**输入**：单个样本在当前统计阶段收集的激活矩阵 $\mathbf{Z}$。<br>
**输出**：描述各神经元在当前样本和当前阶段中持续相对活跃程度的重要性向量 $\mathbf{s}_n$。

</div>

**直观理解**：先在每个 token 内比较神经元，而不是让整体激活特别大的 token 支配统计；随后寻找在多个 token 上反复活跃的神经元。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 批量聚合与 top-k 掩码生成

忽略 padding 和 EOS token；当 $B>1$ 时，对各样本分数做逐元素最大值聚合，使任一样本高度依赖的神经元不会被其他样本的低分直接稀释。之后用逐元素最大值将当前分数并入激活记忆，并选择记忆中分数最高的 $k=\lfloor(1-\rho)D_{\mathrm{FF}}\rfloor$ 个神经元构造共享二值掩码 $\mathbf{M}$。

<div class="method-step__io" markdown="1">

**输入**：批次中 $B$ 个样本的阶段分数 $\{\mathbf{s}_n^{(b)}\}_{b=1}^{B}$、目标稀疏率 $\rho$，以及来自先前阶段的激活记忆。<br>
**输出**：批次共享的激活记忆 $\mathbf{m}_n$ 与恰好保留约 $1-\rho$ 比例神经元的掩码 $\mathbf{M}_n$。

</div>

**直观理解**：同一批次必须使用相同形状的矩阵，因此要把多个样本的需求合成一份名单；最大值聚合相当于允许任一批次成员为自己关键的神经元提出保留请求。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 三阶段调度与周期更新

输入阶段从提示词激活计算 $\mathbf{s}_0$；随后执行 $T_{\mathrm{init}}$ 步完整 MLP，计算 $\mathbf{s}_1$ 并建立首个掩码。此后每个周期先执行 $T_p$ 步稀疏推理，再执行 $T_E$ 步稠密推理并收集新激活，按 $T_{\mathrm{trans}}=T_p+T_E$ 的间隔更新记忆和掩码。

<div class="method-step__io" markdown="1">

**输入**：提示词、初始分数 $\mathbf{s}_0$、初始稠密探索长度 $T_{\mathrm{init}}$、稀疏段长度 $T_p$ 和稠密探索段长度 $T_E$。<br>
**输出**：随生成上下文周期变化的一系列共享掩码 $\mathbf{M}_1,\mathbf{M}_2,\ldots$。

</div>

**直观理解**：方法不会生成一次掩码后永久不变，而是定期用完整网络观察需求是否变化；这对长链式推理中可能间歇性重新活跃的神经元尤其重要。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 阶段性神经元重要性评分

$$
[\overline{\mathbf{Z}}]_t=\frac{[\mathbf{Z}]_t}{\lVert[\mathbf{Z}]_t\rVert_2},\qquad \mathbf{s}_n=\operatorname{MS}(\mathbf{Z})=\frac{1}{\sqrt{T}}\left[\lVert[\overline{\mathbf{Z}}]_{\cdot,1}\rVert_2,\ldots,\lVert[\overline{\mathbf{Z}}]_{\cdot,D_{\mathrm{FF}}}\rVert_2\right]^{\top}
$$

**符号说明**

- $\mathbf{Z}\in\mathbb{R}^{T\times D_{\mathrm{FF}}}$：一个样本在当前阶段的前馈激活矩阵，行对应 token，列对应中间神经元
- $[\mathbf{Z}]_t$：第 t 个 token 的前馈激活向量
- $\overline{\mathbf{Z}}$：逐 token 做二范数归一化后的相对激活矩阵
- $T$：当前评分阶段纳入统计的有效 token 数
- $D_{\mathrm{FF}}$：门控 MLP 的中间神经元数量
- $\mathbf{s}_n$：阶段 n 的神经元重要性向量
- $\operatorname{MS}$：论文定义的批次内单样本评分函数

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分把每个 token 的激活缩放到相同总量，使分数表达神经元在该 token 内的相对份额；第二部分汇总每列在多个 token 上的活跃程度。除以 $\sqrt{T}$ 后，如果不同阶段具有相似的相对激活分布，其分数不会仅因阶段更长而系统性增大。<br>
**原文位置**：第3.2节，公式（2）；行归一化定义紧邻公式（2）之前

</div>

</div>

<div class="equation-block" markdown="1">

#### 掩码裁剪后的门控 MLP 前向

$$
\widehat{\mathbf{z}}=\sigma(\widehat{\mathbf{W}}_g\mathbf{x})\odot(\widehat{\mathbf{W}}_1\mathbf{x}),\qquad \mathbf{y}=\widehat{\mathbf{W}}_2\widehat{\mathbf{z}}
$$

**符号说明**

- $\mathbf{x}\in\mathbb{R}^{D}$：当前 token 输入门控 MLP 的隐藏状态
- $\widehat{\mathbf{W}}_g,\widehat{\mathbf{W}}_1\in\mathbb{R}^{k\times D}$：依据保留索引选取行后得到的门控投影与数值投影矩阵
- $\widehat{\mathbf{W}}_2\in\mathbb{R}^{D\times k}$：依据相同保留索引选取列后得到的输出投影矩阵
- $\sigma$：SiLU 激活函数
- $\odot$：逐元素乘法
- $\widehat{\mathbf{z}}\in\mathbb{R}^{k}$：仅包含保留神经元的紧凑中间激活
- $\mathbf{y}\in\mathbb{R}^{D}$：裁剪后 MLP 的输出，维度与原 Transformer 隐藏状态一致
- $k=\lfloor(1-\rho)D_{\mathrm{FF}}\rfloor$：由目标稀疏率决定的保留神经元数

<div class="equation-explanation" markdown="1">

**直观理解**：掩码先把三组相关权重裁剪成中间维度为 $k$ 的矩阵，再执行普通矩阵乘法；输入和输出仍保持 $D$ 维，因此无需改变 Transformer 其余模块。计算节省来自矩阵尺寸真实缩小，而不只是计算完整结果后再把部分值置零。<br>
**原文位置**：第3.3节 Phase 3，公式（4）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该方法没有新增损失函数、梯度优化或参数微调，原语言模型权重在整个过程中保持冻结；需要决定的只有推理时各阶段的激活统计、跨样本及跨阶段聚合、top-$k$ 掩码选择和裁剪后的前向计算。因此它优化的不是一个可微训练目标，而是在给定目标稀疏率 $\rho$ 和周期调度下，以启发式激活重要性尽量保留推理能力并减少 MLP 计算。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 长度校正的激活重要性评分器**

评分器对每个 token 的 $D_{\mathrm{FF}}$ 维激活先做 $\ell_2$ 归一化，再沿 token 维计算各神经元的 $\ell_2$ 范数，并用 $1/\sqrt{T}$ 校正阶段长度。它衡量的是神经元在一个阶段内持续具有较大相对激活的程度，而非单次激活峰值或权重静态幅值。

> 直观理解：归一化避免“某个 token 整体数值很大”被误认为许多神经元都重要，长度校正则使提示词阶段和较短探索阶段的分数可以公平合并。

**2. 共享掩码聚合与激活记忆**

批量聚合默认使用 $\bar{\mathbf{s}}_n=\max_b\mathbf{s}_n^{(b)}$；激活记忆递推为 $\mathbf{m}_n\leftarrow\max(\mathbf{m}_{n-1},\bar{\mathbf{s}}_n)$，初次更新相应地合并输入阶段与初始探索阶段。掩码始终由 $\operatorname{top-k}(\mathbf{m}_n,k)$ 产生，因此其稀疏率不依赖分数绝对尺度。

> 直观理解：批量最大值保护只对少数样本重要的神经元，跨阶段最大值则给曾经重要、以后可能重新激活的神经元留下位置；代价是记忆只增不减，可能更偏向历史重要性。

**3. 稀疏计算与稠密探索调度器**

调度器在初始稠密生成后，交替安排使用当前掩码的 $T_p$ 步结构化稀疏前向和用于重新估计分数的 $T_E$ 步完整前向。每次探索结束才更新掩码，从而把逐 token 自适应所需的额外统计和权重选择开销摊薄到整个周期。

> 直观理解：持续使用完整网络没有加速效果，而永久使用旧掩码又可能跟不上推理内容；周期调度是在计算节省与上下文适应之间取折中。

**训练与推理**

训练阶段完全沿用已有预训练或蒸馏语言模型，论文方法本身不进行训练。推理时，首先用完整模型处理提示词并按层记录有效 token 的门控 MLP 激活，得到输入阶段分数；接着以完整 MLP 生成 $T_{\mathrm{init}}$ 个 token，让统计包含生成上下文。批次内各样本的分数默认逐元素取最大值，再与先前分数逐元素取最大值形成激活记忆，由记忆的 top-$k$ 项生成首个共享掩码。

之后进入周期生成：连续 $T_p$ 步只使用掩码选出的紧凑权重进行结构化稀疏前向，再连续 $T_E$ 步恢复完整 MLP并收集激活；探索结束后计算新分数、更新记忆和掩码。该循环持续到所有样本结束生成；批次聚合时排除 padding 与 EOS token，而已完成样本不应通过这些占位位置影响剩余样本的神经元排序。

**复现信息**

复现时最关键的是在每个被剪枝的门控 MLP 层分别维护分数、记忆和掩码，并保证 $\mathbf{W}_g$、$\mathbf{W}_1$ 的保留行与 $\mathbf{W}_2$ 的保留列使用完全相同的索引。论文默认批次聚合为逐元素最大值，保留数使用 $k=\lfloor(1-\rho)D_{\mathrm{FF}}\rfloor$，选择采用 top-$k$ 排序；这使实际保留数量可控，也避免把在单样本分布上校准的阈值直接用于批量聚合后的不同分布。

周期长度定义为 $T_{\mathrm{trans}}=T_E+T_p$，论文设置 $T_{\mathrm{trans}}=20$，依据是重要神经元约每 $20$ 至 $23$ 个 token 再次激活的经验观察；但节选未给出 $T_{\mathrm{init}}$、$T_E$ 与 $T_p$ 的完整默认拆分，复现时需回查论文实验设置或附录。实现必须真的构造或高效访问尺寸为 $k\times D$、$D\times k$ 的紧凑权重，而非先运行完整 MLP 再乘二值掩码，否则无法获得该结构化剪枝所声称的计算优势。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- TinyGSM8K：GSM8K 的 100 个测试样本子集，用于低成本评估小学数学文字题；原文说明其目的是“reduce computational costs while maintaining evaluation reliability”。
- MATH500：测试集 500 个样本，用于评估竞赛级数学推理；该任务能检验剪枝是否破坏较长、较复杂的数学解题过程。
- GPQA-DIAMOND：测试集 198 个样本，用于评估研究生水平科学问答；它补充了数学任务之外的通用科学推理能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

模型在各基准测试中答对的比例；原文称四种模型均使用 accuracy 作为评估指标。 （越高越好，因为它直接表示推理答案的正确率。）

</div>
<div class="metric-item" markdown="1">

**Speed (token/sec)**

推理过程中每秒生成的 token 数，用于衡量剪枝带来的解码吞吐量。 （越高越好，表示单位时间内生成的推理文本更多。）

</div>
<div class="metric-item" markdown="1">

**Actual sparsity**

整个生成过程实际被剪去的参数比例；它不同于推理前指定的 target sparsity，因为所提方法会交替执行稠密步骤和稀疏步骤，且只剪枝 FFN 模块。 （在比较加速时，通常应在相同实际稀疏率下比较；更高的稀疏率一般意味着更少计算，但不能单独代表准确率更高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨模型的重要神经元周期性分析

<div class="result-value" markdown="1">

作者观察到重要神经元激活具有稳定的重复周期，并据此为不同模型设置状态更新周期：DS-R1-Qwen-7B、DS-R1-Llama-8B 和 Qwen3-8B 使用 $T_{\mathrm{trans}}=20$，Qwen3-1.7B 使用 $T_{\mathrm{trans}}=10$。表 14 报告的中位激活周期分别为 $22.8\pm1.9$、$20.8\pm2.9$、$11.8\pm0.8$ 和 $17.8\pm1.3$。

</div>

这项结果为“周期性更新剪枝掩码”提供了经验依据：模型并不需要在每个解码步骤都重新选择神经元。它支持更新周期应随模型激活动态调整，但不能单独证明所提方法一定优于所有基线，因为这里测量的是激活规律，不是端到端准确率或速度比较。

<div class="result-source" markdown="1">

来源：Appendix L, Table 14

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Based on the observed median activation periods, we set $T_{\text{trans}}=20$ for DS-R1-Qwen-7B, DS-R1-Llama-8B, and Qwen3-8B, and $T_{\text{trans}}=10$ for Qwen3-1.7B.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 激活记忆机制的跨模型平均结果，50% target sparsity、batch size 4

<div class="result-value" markdown="1">

在跨模型平均中，启用激活记忆的平均准确率为 $44.3$，关闭记忆为 $35.4$，相差 $8.9$ 个百分点；分模型时，DS-R1-Qwen-7B 为 $54.0$ 对 $45.3$，DS-R1-Llama-8B 为 $34.5$ 对 $25.5$。

</div>

激活记忆用于保留先前阶段识别出的重要神经元，因此可以缓解只依据当前批次或当前阶段选择神经元造成的遗漏。结果支持该组件对总体准确率有实质作用，但也说明记忆并非总是有益：在某些任务上它可能保留过早阶段的神经元，从而引入错误的偏置。

<div class="result-source" markdown="1">

来源：Appendix M, Table 15

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For activation memory, enabling memory consistently improves average accuracy by 8.7 points on DS-R1-Qwen-7B (54.0 vs. 45.3) and 9.0 points on DS-R1-Llama-8B (34.5 vs. 25.5).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### $T_{\mathrm{init}}$、$T_E$ 和 $T_{\mathrm{trans}}$ 的 MATH500 超参数实验

<div class="result-value" markdown="1">

在 DeepSeek-R1-Distill-Qwen-7B、batch size 4、NVIDIA H200 上，$T_{\mathrm{init}}$ 从 $0$ 增至 $128$ 时准确率由 $68.6$ 提升至 $71.4$，速度均为 $925.3$ token/sec；$T_E$ 从 $1$ 增至 $4$ 时准确率由 $67.4$ 升至 $77.2$，速度由 $941.0$ 降至 $896.8$ token/sec；$T_{\mathrm{trans}}$ 从 $10$ 增至 $30$ 时准确率由 $77.4$ 降至 $69.6$，速度由 $806.3$ 升至 $958.7$ token/sec。

</div>

$T_{\mathrm{init}}$ 控制开始剪枝前的稠密推理步数，主要帮助模型适应提示词之后的激活变化；$T_E$ 控制探索步数，增加它能获得更充分的当前激活信息，但会降低吞吐量；$T_{\mathrm{trans}}$ 控制重新计算剪枝掩码的间隔，间隔越长通常越快，却可能因掩码过时而损害准确率。因此，这些参数体现的是准确率和速度之间的部署取舍，而不是存在一个对所有任务都最优的固定组合。

<div class="result-source" markdown="1">

来源：Appendix N, Table 16

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Increasing $T_E$ (exploration steps) from 1 to 4 yields a 9.8 point accuracy gain but reduces throughput from 941.0 to 896.8 tokens/sec.

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

- Wanda：输入无关的训练免费剪枝方法，在 C4 校准后施加 $2{:}4$ 结构化稀疏，代表固定且不依赖当前推理状态的剪枝。
- Griffin：输入相关但静态的剪枝方法，在提示词阶段识别重要神经元，并在整个解码过程中复用同一组剪枝权重，代表只在推理初期适配一次的方法。
- TEAL：基于阈值的自适应方法，在 C4 上校准激活阈值，推理时剪去低于阈值的神经元，但在各层使用统一稀疏率，代表依赖离线校准分布的动态剪枝。

**实验想回答的问题**

- 在相同目标稀疏率下，批级自适应剪枝能否比 Wanda、Griffin 和 TEAL 更好地保留语言推理模型在数学与科学推理任务上的准确率，同时获得推理加速？
- 批内激活聚合方式、激活记忆机制以及 $T_{\mathrm{init}}$、$T_E$、$T_{\mathrm{trans}}$ 等控制剪枝时序的超参数，分别如何影响准确率与吞吐量？

**实验实现**

实验覆盖 DeepSeek-R1-Distill-Qwen-7B、DeepSeek-R1-Distill-Llama-8B，并在附录扩展到 Qwen3-1.7B 和 Qwen3-8B。DeepSeek 模型使用官方 DeepSeek-R1 chat template，Qwen3 模型使用 Qwen3 chat template 并设置 enable_thinking=True；所有模型采用 zero-shot、temperature $0$ 的贪心解码，最大生成长度为 16,000 tokens，准确率作为任务指标。批量评估时，基线和所提方法均在排除 padding 与 EOS token 后聚合批内激活；Dense 和 Wanda 的结果使用 batch size 4 报告。论文区分 target sparsity 与 actual sparsity，并指出第 4.3 节的吞吐量比较采用匹配的 actual sparsity，而 50% target sparsity 下的吞吐量放在附录 F。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 批内激活聚合：max 与 mean，50% target sparsity、batch size 4 | 跨模型平均中，max 的平均准确率为 $44.3$，mean 为 $43.1$；max 在 GSM8K 上为 $82.0$ 对 $73.5$、在 AMC23 上为 $37.5$ 对 $35.0$，mean 在 MATH500 上为 $58.1$ 对 $54.9$、在 GPQA-DIAMOND 上为 $27.8$ 对 $26.3$。 | 该消融只改变一个批次内如何合并不同样本的激活信号：max 更偏向保留任一样本强烈激活的神经元，mean 则反映批次的平均需求。两者在不同任务上各有优势，跨模型平均仅相差 $1.2$ 个百分点，因此不能据此断言 max 是普遍最优聚合算子。 | Appendix M, Table 15<br><span class="experiment-evidence">The cross-model averages differ by 1.2 points (44.3 vs 43.1), which we do not consider sufficient to claim that either operator is superior; the per-model winner is likewise split (Section 4.4).</span> |
| 超参数控制的准确率-吞吐量权衡，MATH500、batch size 4 | 增加探索步数 $T_E$ 从 $1$ 到 $4$，准确率提升 $9.8$ 个百分点，但吞吐量从 $941.0$ 降至 $896.8$ token/sec；将更新周期 $T_{\mathrm{trans}}$ 从 $10$ 延长到 $30$，准确率下降 $7.8$ 个百分点，但吞吐量从 $806.3$ 提升至 $958.7$ token/sec。将初始稠密步数 $T_{\mathrm{init}}$ 从 $0$ 增至 $128$，准确率提升 $2.8$ 个百分点，速度保持为 $925.3$ token/sec。 | 该消融检验三类时间控制参数是否分别承担不同功能。结果表明，$T_E$ 增大能用更多探索换取准确率，$T_{\mathrm{trans}}$ 增大能减少掩码更新开销但会降低适应性，$T_{\mathrm{init}}$ 主要帮助捕获提示词后的激活转移且几乎不牺牲速度。结论只在该模型、数据集和硬件设置下直接成立，不能自动推广到所有部署环境。 | Appendix N, Table 16<br><span class="experiment-evidence">Conversely, extending $T_{\text{trans}}$ (update period) from 10 to 30 degrades accuracy by 7.8 points while increasing throughput from 806.3 to 958.7 tokens/sec.</span> |

**定性案例**

- 在 DS-R1-Llama-8B 的 GPQA-DIAMOND 上，关闭激活记忆的准确率为 $29.3$，略高于启用记忆的 $21.7$；原文将其解释为累积激活记忆有时会过度保留早期阶段神经元。该案例说明记忆机制的总体正效应并不意味着它在每个任务和每个模型上都稳定有益。
- 证据引文："We note that on GPQA-DIAMOND, the no-memory variant slightly outperforms the memory variant on DS-R1-Llama-8B (29.3 vs. 21.7), suggesting that accumulated activation memory may occasionally over-retain neurons from earlier phases on certain tasks."

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出基于周期性神经元激活感知的批次自适应权重剪枝方法，以提升语言推理模型效率。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`44f23b5ea52445c9424748ed83d419b22c915ff69bea1a8b397559eec78b2549`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
