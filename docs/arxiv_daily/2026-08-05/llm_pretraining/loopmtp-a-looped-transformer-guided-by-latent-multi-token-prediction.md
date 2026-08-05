---
title: "[论文解读] LoopMTP: A looped transformer guided by latent multi-token prediction"
description: "[arXiv 2608.03624][预训练] 本文研究如何用潜在空间中的多词元预测监督和可学习的状态聚合，引导循环 Transformer 在固定参数量下进行更有效、更稳定的多轮推理。"
arxiv_id: "2608.03624"
announcement_date: "2026-08-05"
primary_category: "llm_pretraining"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:43:23.688827+00:00"
source_sha256: "515dab404aa5f13e6c3b1d5811ec63cecc0190d30435e017525ebf17cacc7a01"
tags:
  - "预训练"
  - "LLM Reasoning"
  - "循环 Transformer"
  - "潜在推理"
  - "多词元预测"
  - "参数高效推理"
  - "隐藏状态对齐"
  - "表示聚合"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">预训练 · arXiv 2608.03624</p>

# LoopMTP: A looped transformer guided by latent multi-token prediction

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Behzad Shomali, Markus Frey, David Berghaus, Joachim Koehler, Mehdi Ali</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Lamarr Institute；University of Bonn</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03624v1) · [PDF 下载](https://arxiv.org/pdf/2608.03624v1) · **关键词** 循环 Transformer, 潜在推理, 多词元预测, 参数高效推理, 隐藏状态对齐, 表示聚合<br>


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

本文研究如何用潜在空间中的多词元预测监督和可学习的状态聚合，引导循环 Transformer 在固定参数量下进行更有效、更稳定的多轮推理。

**不用术语来说**：小型语言模型通常难以完成需要多步思考的任务；虽然反复使用同一组网络层可以在不增加参数的情况下延长计算过程，但模型每轮究竟应推进什么并没有明确指导，继续计算反而可能改坏原本正确的答案，或只是在重复相似工作。本文要解决的就是：怎样让每一轮计算都有不同且有用的目标，同时保留此前已经形成的有效信息。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 LoopMTP，将第 $t$ 次循环的隐藏状态与当前位置之后第 $t$ 个词元的嵌入进行软对齐，使不同循环分别获得面向不同未来位置的监督，从结构上把 $T$ 次循环与预测未来 $T$ 个词元联系起来。
- 引入轻量级可学习门控来聚合历次状态，避免新一轮表示无条件覆盖旧信息；作者还系统考察了多词元对齐目标与聚合机制，并将该架构用于训练小型领域专家模型。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型的参数高效推理研究方向。标准 Transformer 通常通过堆叠更多不同参数的层来增加计算深度，但这会扩大模型规模；垂直循环 Transformer 则让同一组层对隐藏表示重复执行 $T$ 次，在参数量基本不变的情况下获得更大的“有效深度”。这类模型把多步计算放在连续隐藏空间中，最终才输出离散词元，因此属于潜在推理。与之互补，多词元预测（MTP）要求模型在当前位置同时关注后续多个词元，为隐藏表示提供比单一下一词元预测更密集、具有前瞻性的训练信号。本文研究的核心背景是：如何用低开销的潜在 MTP 信号引导每次循环，使小型循环模型的迭代真正承担不同阶段的前瞻计算，而不是反复改写或重复同一表示。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**垂直循环 Transformer**

同一组 Transformer 层被连续复用 $T$ 次，每次接收并更新上一轮的隐藏表示，因此增加的是计算次数和有效深度，而非参数量。它不同于沿序列加入潜在词元的水平循环。

</div>
<div class="concept-item" markdown="1">

**潜在推理**

模型在输出下一个离散词元之前，先在连续向量表示上执行多步更新。循环次数可视为内部推理步数，但中间步骤通常没有可直接观察的文字输出。

</div>
<div class="concept-item" markdown="1">

**多词元预测（MTP）**

传统下一词元预测只监督紧邻的一个未来词元，而 MTP 让当前位置同时预测未来 $k$ 个词元，以鼓励规划和长程依赖建模。本文不在每轮计算完整词表分布，而是在潜在空间中将循环表示与特定未来词元的嵌入进行软对齐。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一段已词元化的文本及其后续真实词元，模型首先把当前位置的上下文编码为隐藏表示，再让共享的 Transformer 层栈循环运行 $T$ 次。第 $t$ 次循环不仅参与最终的下一词元建模，还被训练为在潜在空间中朝向当前位置之后第 $t$ 个真实词元的嵌入；各轮表示通过轻量门控进行保留与聚合，以避免后轮直接覆盖前轮已有的有效信息。模型的最终输出仍是语言模型所需的词元概率或预测词元；基本设定是假定训练时可取得未来真实词元作为监督，并以增加循环计算量、但不随 $T$ 增加主干参数量的方式换取推理能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$T$**

共享 Transformer 层栈的总循环次数，也对应模型拟对齐或前瞻的未来词元范围。

</div>
<div class="notation-item" markdown="1">

**$t$**

循环索引；第 $t$ 轮隐藏状态对应当前位置之后第 $t$ 个词元的潜在监督。

</div>
<div class="notation-item" markdown="1">

**$k$**

一般 MTP 目标中同时预测的未来词元数量。

</div>

</div>

**直接相关的工作**

- **Fu et al. (2026) 的循环 Transformer 研究**: 该工作表明，复用同一组参数进行多次前向迭代，可以在固定参数量下模拟更深模型并获得较强推理能力，为本文采用垂直循环提供直接基础；本文进一步处理循环过程中表示覆盖、潜在过度思考和迭代计算趋同的问题。
- **Noci et al. (2026) 的 MTP 与潜在推理结合方法**: 该方法在选定位置进行隐藏空间多步前瞻，并通过完整词表上的交叉熵监督未来真实词元。本文改用循环隐藏状态与未来词元嵌入之间的余弦相似度作为软引导，避免每轮都执行一次完整词表投影，从而更适合循环次数较多的参数高效模型。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

数学、代码生成等任务需要较多顺序计算，传统做法通常通过堆叠更多 Transformer 层获得更强推理能力，但这会显著增大参数量与部署成本。许多机构只能通过 API 使用前沿模型，也难以在本地承载有竞争力的开放权重模型；医疗等场景又要求敏感数据留在本地，因此迫切需要能够在有限硬件和固定参数预算下运行的强推理模型。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **循环 Transformer**：它不继续增加不同的网络层，而是让输入表示反复通过同一组 Transformer 块，共执行 $T$ 次迭代。这样能以参数共享的方式获得近似更深网络的顺序计算量，并在输出词元前于潜在表示中进行多轮修正。
- **多词元预测（MTP）**：它用同时预测未来 $k$ 个词元的训练目标替代或补充单一的下一词元预测，迫使模型提前编码后续信息。已有研究表明这种“向前看”的监督有助于推理，但论文指出，此前收益主要在较大规模模型上得到验证，尚未与循环计算的中间状态形成直接对应。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有循环模型常让每次迭代的新隐藏表示直接替换旧表示，可能丢弃早期循环中仍然有用的信息，进而产生“潜在过度思考”：某个答案在较早轮次已经正确，却在继续循环后被改成错误答案。
- 不同循环缺少明确且有差异的中间监督。随着循环次数增加，各轮隐藏表示可能越来越相似，形成“无差别计算”，即后续轮次重复近似操作，消耗额外算力却没有带来相应的信息推进；同时，已有 MTP 工作尚未解决如何将其前瞻监督施加到循环模型的逐轮潜在状态上。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究分别证明了参数共享的循环深度和面向未来的 MTP 目标具有价值，但缺少一种统一机制：在不增加完整网络深度的前提下，为每个循环分配与其轮次对应的前瞻目标，并让模型有选择地继承先前状态。尤其尚不清楚，这种机制能否同时缓解过度修正与重复计算，并在较多循环及小型领域模型训练中保持稳定有效。

</div>
<div markdown="1"><span>核心问题</span>

能否把 $T$ 次循环与未来 $T$ 个词元建立潜在空间中的结构对应，使第 $t$ 轮表示受到第 $t$ 步未来信息的引导，再通过可学习聚合保留已有有效状态，从而在参数量基本不变时优于普通非循环模型及既有循环 Transformer？

</div>
<div markdown="1"><span>作者直觉</span>

如果所有循环只面对最终的下一词元损失，各轮就像一群没有分工的人反复修改同一份答案；若让第 $t$ 轮表示靠近未来第 $t$ 个词元的语义，每一轮便获得不同的“前瞻里程碑”，更可能逐步扩展上下文中的计划，而非原地重复。与此同时，门控聚合类似于允许模型决定保留多少旧草稿、吸收多少新修改，因此有机会避免后续循环覆盖已经正确的信息。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

LoopMTP以长度为$S$的词元序列$\mathbf{u}$为输入，先得到初始嵌入$\mathbf{x}^{(0)}$，再把同一个含$L$层Transformer的骨干网络重复使用$T$次。每轮不仅读取上一轮状态$\mathbf{x}^{(t-1)}$，还重新注入固定的词元嵌入，并显式加入归一化轮次编号；由此，同一组参数可以形成相当于更深网络的迭代计算。训练时，第$t$轮隐状态被软性引导去接近位置$i+t$处未来词元的输出嵌入，但$t=1$不加该约束，以保留一个可供后续轮次继续加工的通用表示。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 词元嵌入与循环状态初始化

通过嵌入层得到$\mathbf{x}^{(0)}=\mathrm{Embed}(\mathbf{u})\in\mathbb{R}^{S\times d}$，并将其同时作为初始循环状态和所有轮次都可访问的固定词元信息。

<div class="method-step__io" markdown="1">

**输入**：词元序列$\mathbf{u}=(u_1,\ldots,u_S)\in\mathcal{V}^S$，其中$\mathcal{V}$是词表。<br>
**输出**：初始表示矩阵$\mathbf{x}^{(0)}$，每个位置对应一个$d$维向量。

</div>

**直观理解**：模型先把离散词元变成连续向量；后续每轮都能重新查看这些原始向量，避免迭代过程中把输入内容完全覆盖。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造轮次感知的循环输入

模型把归一化轮次编号$(t-1)/T$拼接到上一轮状态，并用该轮专属的LayerNorm处理；初始嵌入则经共享的词元LayerNorm处理。两路结果沿特征维拼接，再经线性投影$\mathrm{P}$恢复到$d$维，得到$\mathbf{y}^{(t)}$。

<div class="method-step__io" markdown="1">

**输入**：上一轮输出$\mathbf{x}^{(t-1)}$、初始嵌入$\mathbf{x}^{(0)}$、当前轮次$t$和总轮数$T$。<br>
**输出**：同时包含原始词元信息、上一轮推理结果和当前轮次标识的融合表示$\mathbf{y}^{(t)}\in\mathbb{R}^{S\times d}$。

</div>

**直观理解**：这一步相当于在每轮开始时告诉模型“原题是什么、上一轮想到什么、现在是第几轮”，使共享骨干不必对所有轮次执行完全相同的变换。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 共享骨干的稳定循环计算

同一个含$L$层的Transformer骨干$f_\theta$被重复调用，产生$\mathbf{x}^{(t)}=f_\theta(\mathbf{y}^{(t)})$。每个注意力和前馈残差分支在RMSNorm后乘固定因子$1/T$，即Loop-LNS，以限制重复展开时残差更新的规模。

<div class="method-step__io" markdown="1">

**输入**：第$t$轮融合表示$\mathbf{y}^{(t)}$。<br>
**输出**：全部轮次的隐藏表示集合$\{\mathbf{x}^{(t)}\}_{t=1}^{T}$。

</div>

**直观理解**：模型像反复修改同一份草稿一样复用参数；固定缩放避免循环次数增加后每次修改累积得过猛，同时又不会让后期轮次因缩放过小而几乎学不到东西。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 内容条件门控聚合

共享线性门$W_g$结合每轮偏置$\beta_t$，为每个词元、每个特征维计算非负权重；权重在轮次维归一化后，对各轮表示逐元素加权求和，得到$\mathbf{z}$。

<div class="method-step__io" markdown="1">

**输入**：各轮隐藏表示$\{\mathbf{x}^{(t)}\}_{t=1}^{T}$。<br>
**输出**：融合了不同计算轮次信息的最终表示$\mathbf{z}\in\mathbb{R}^{S\times d}$，随后送入归一化层和语言模型头。

</div>

**直观理解**：模型不强迫最后一轮覆盖前面所有结果，而是针对不同词元和特征，自行决定保留哪一轮的信息；这类似把多版草稿按内容选择性合并。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 逐词元门控聚合

$$
\begin{aligned} \mathbf{g}^{(t)}_i &= \operatorname{softplus}\!\left(W_g\mathbf{x}^{(t)}_i+\beta_t\mathbf{1}_d\right),\\ \tilde{\mathbf{g}}^{(t)}_i &= \frac{\mathbf{g}^{(t)}_i}{\sum_{s=1}^{T}\mathbf{g}^{(s)}_i+\varepsilon},\\ \mathbf{z}_i &= \sum_{t=1}^{T}\tilde{\mathbf{g}}^{(t)}_i\odot\mathbf{x}^{(t)}_i. \end{aligned}
$$

**符号说明**

- $\mathbf{x}^{(t)}_i$：第$t$轮在序列位置$i$产生的$d$维隐藏向量。
- $W_g$：所有轮次共享的$d\times d$线性门控矩阵。
- $\beta_t$：第$t$轮的可学习标量偏置。
- $\mathbf{1}_d$：长度为$d$的全一向量，用于把标量偏置加到每个特征维。
- $\mathbf{g}^{(t)}_i$：softplus变换后得到的非负、未归一化门值。
- $\tilde{\mathbf{g}}^{(t)}_i$：在全部$T$个轮次之间归一化后的逐特征门权重。
- $T$：共享Transformer骨干的总循环次数。
- $s$：归一化分母中遍历所有循环轮次的索引。
- $\varepsilon$：防止除零的常数，原文设为$10^{-8}$。
- $\odot$：逐元素乘法。
- $\mathbf{z}_i$：位置$i$聚合所有轮次后得到的最终$d$维表示。
- $d$：模型隐藏表示的维度。
- $i$：序列中的词元位置索引。
- $t$：当前循环轮次索引。

<div class="equation-explanation" markdown="1">

**直观理解**：第一式根据当前内容和轮次偏置生成门值，第二式使同一特征在各轮上的权重近似归一化，第三式按这些权重融合表示。其核心作用是防止最后一轮无条件覆盖早期结果，并允许不同词元、不同特征使用不同的有效计算深度。<br>
**原文位置**：第3.3节，公式(9)–(11)

</div>

</div>

<div class="equation-block" markdown="1">

#### NTP、潜空间MTP对齐与ponder正则的联合目标

$$
\begin{aligned} \mathcal{L}_{\mathrm{NTP}} &= -\frac{1}{S-1}\sum_{i=1}^{S-1}\log \mathbf{p}^{\mathrm{agg}}_i[u_{i+1}],\\ \mathcal{L}^{(t)}_{\mathrm{align}} &= \frac{1}{S-t}\sum_{i=1}^{S-t}\left(1-\cos\!\left(\mathbf{x}^{(t)}_i,\operatorname{sg}[E_{u_{i+t}}]\right)\right),\\ \mathcal{L}_{\mathrm{align}} &= \frac{1}{T-1}\sum_{t=2}^{T}\mathcal{L}^{(t)}_{\mathrm{align}},\\ G_i(t) &= \frac{1}{d}\sum_k\tilde{\mathbf{g}}^{(t)}_{i,k},\qquad Q=(1/T,\ldots,1/T),\\ \mathcal{L}_{\mathrm{ponder}} &= \frac{1}{S}\sum_{i=1}^{S}\operatorname{KL}(G_i\|Q),\\ \mathcal{L} &= \mathcal{L}_{\mathrm{NTP}}+\lambda_{\mathrm{align}}\mathcal{L}_{\mathrm{align}}+\lambda_{\mathrm{ponder}}\mathcal{L}_{\mathrm{ponder}}. \end{aligned}
$$

**符号说明**

- $\mathcal{L}_{\mathrm{NTP}}$：基于聚合表示的标准下一词元交叉熵损失。
- $S$：输入序列长度。
- $\mathbf{p}^{\mathrm{agg}}_i$：语言模型头根据聚合表示在位置$i$输出的词表概率分布。
- $u_{i+1}$：位置$i$之后的真实下一词元。
- $\mathcal{L}^{(t)}_{\mathrm{align}}$：第$t$轮针对$t$步之后词元计算的隐藏状态对齐损失，仅用于$t=2,\ldots,T$。
- $\mathbf{x}^{(t)}_i$：第$t$轮在位置$i$的隐藏表示。
- $\cos(\cdot,\cdot)$：两个向量之间的余弦相似度。
- $\operatorname{sg}[\cdot]$：停止梯度算子，使目标输出嵌入不通过该对齐项被更新。
- $E$：形状为$|\mathcal{V}|\times d$的输出嵌入或unembedding矩阵。
- $E_{u_{i+t}}$：真实未来词元$u_{i+t}$对应的$d$维输出嵌入。
- $\mathcal{L}_{\mathrm{align}}$：对第$2$至第$T$轮对齐损失取平均得到的软MTP正则项。
- $T$：总循环次数，也对应软MTP监督覆盖的最大前瞻距离。
- $G_i(t)$：位置$i$上第$t$轮门权重对$d$个特征维取平均后得到的轮次概率质量。
- $\tilde{\mathbf{g}}^{(t)}_{i,k}$：位置$i$、第$t$轮、第$k$个特征维的归一化门权重。
- $k$：隐藏表示的特征维索引。
- $d$：隐藏表示维度。
- $Q$：在$T$个轮次上均匀分配质量的先验分布。
- $\operatorname{KL}(G_i\|Q)$：位置$i$的门控轮次分布相对于均匀先验的Kullback–Leibler散度。
- $\mathcal{L}_{\mathrm{ponder}}$：对所有位置的门控KL散度取平均所得的正则项。
- $\lambda_{\mathrm{align}}$：控制软MTP对齐强度的超参数。
- $\lambda_{\mathrm{ponder}}$：控制门控分布正则强度的超参数。
- $\mathcal{L}$：用于端到端反向传播的最终训练损失。
- $i$：序列位置索引。
- $t$：循环轮次及其对应未来词元偏移量。

<div class="equation-explanation" markdown="1">

**直观理解**：下一词元损失负责最终语言建模能力；软MTP项不要求每轮输出完整词表分布，而只把第$t$轮表示推向$t$步之后词元的嵌入方向，因此是一种较轻的表示级监督。ponder项把平均门权重拉向均匀先验，用来抑制所有权重长期集中于单一轮次，但最终是否采用某轮仍由内容条件门控决定。<br>
**原文位置**：第3.4节，公式(12)–(16)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练优化的主目标是聚合表示上的下一词元预测，即模型最终仍按普通自回归语言模型学习。$\lambda_{\mathrm{align}}\mathcal{L}_{\mathrm{align}}$是表示级辅助项：它让第$t$轮获得与$t$步未来相关的功能分工，同时通过停止梯度把输出嵌入当作固定目标，避免模型仅靠移动目标向量来降低余弦距离；第1轮无对齐损失，以便形成可供后续多轮读取的丰富基础状态。$\lambda_{\mathrm{ponder}}\mathcal{L}_{\mathrm{ponder}}$则正则化门控的总体轮次使用，降低门控塌缩风险。三项联合优化把“预测正确”“各轮计算有所区分”和“保留多轮有用信息”分别编码进同一训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. MTP引导的循环Transformer块**

完整的$L$层骨干而非单层被循环复用；第$t$轮输入由初始嵌入、上一轮状态和轮次编号共同构成，并使用轮次专属的$\mathrm{LN}^{\mathrm{prev}}_t$适配不同迭代阶段的统计分布。骨干内部采用Loop-LNS，在每个注意力和FFN分支的归一化输出上统一乘$1/T$。

> 直观理解：共享参数节省了模型容量，但共享也可能让每轮做相似的事；轮次信号和独立归一化让同一骨干知道自己处于哪个推理阶段，Loop-LNS则负责让多轮展开不至于数值失稳。

**2. 潜空间软MTP对齐**

第$t$轮位置$i$的隐藏向量$\mathbf{x}^{(t)}_i$通过余弦相似度对齐到未来词元$u_{i+t}$在输出矩阵$E$中的嵌入；目标嵌入使用停止梯度，且$t=1$不施加对齐监督。该设计不为每轮计算全词表概率分布，因此不同于传统多词元预测头。

> 直观理解：它不是要求每一轮直接说出未来词，而是给隐藏状态一个方向提示：第二轮应包含两步之后的信息，第三轮应包含三步之后的信息。这样能减少各轮表示高度相似的“无差别计算”，同时避免多个全词表输出头带来的开销和过强约束。

**3. 逐词元、逐特征的学习式聚合门**

单个共享矩阵$W_g\in\mathbb{R}^{d\times d}$和$T$个标量偏置生成各轮门值，经softplus保证非负，再在轮次维归一化。门的初始化强烈偏向第一轮：$\beta_1$取中等正值，其余偏置取较大负值，使训练初期近似普通非循环Transformer，之后再逐步启用后续轮次；该模块在文中模型上增加少于$0.5\%$的参数。

> 直观理解：循环模型若只使用最后一轮，早期形成的有用信息可能被覆盖；固定平均又不能适应不同词元。学习式门控让模型从易训练的单轮行为起步，再按内容逐渐决定哪些后续计算值得采用。

**训练与推理**

训练时，对每个序列先计算一次$\mathbf{x}^{(0)}$，再顺序展开$T$轮共享骨干并保存全部$\mathbf{x}^{(t)}$；每轮输入都重新融合$\mathbf{x}^{(0)}$和$\mathbf{x}^{(t-1)}$。随后门控聚合全部轮次，语言模型头从$\mathbf{z}$产生下一词元分布；同时，第$2$至第$T$轮分别与偏移$2$至$T$的真实未来词元嵌入计算软对齐损失，门值计算ponder正则，最后对总损失反向传播。推理时不需要真实未来词元，也不计算对齐损失或ponder损失；模型仍执行预设的$T$轮循环，经同一门控模块聚合各轮状态，再由语言模型头自回归地产生下一个词元。

**复现信息**

实验模型采用GPT-2式仅解码器架构，循环的是完整$L=12$层骨干，隐藏维度为$d=1024$，注意力头数为32，名义FFN维度为4096；使用旋转位置编码、注意力前的查询/键RMSNorm和SwiGLU。循环稳定性的关键实现不是普通深度缩放，而是在所有轮次、所有注意力与FFN子块中固定使用$1/T$的Loop-LNS；作者称按累计有效深度逐渐减小缩放会使后期轮次因因子过小而几乎失去梯度贡献。门控仅增加一个$d\times d$线性层和$T$个偏置，文中规模下额外参数少于$0.5\%$；其偏置初始化先偏向第1轮，使训练初期近似非循环模型。主实验在Nemotron-CC-v2高质量子集和Nemotron-CC-Math-v1上训练$6.8$B词元；优化使用Muon与AdamW，峰值学习率为$1.9\times10^{-3}$。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 通用与问答任务集合：包括 ARC-Challenge（ARC-C）、ARC-Easy（ARC-E）、HellaSwag（HS）、Winogrande（WG）、Social IQA（SIQA）、PIQA 和 LAMBADA（LB）。表 5 用准确率评估答题或续写正确性，表 6 用 BPB 评估模型对相同任务文本的概率建模质量；原文节选未报告各数据集规模、数据划分或具体评测 split。
- 数学与推理任务集合：按 algebra、counting & probability、geometry、intermediate algebra、number theory、prealgebra 和 precalculus 七个类别汇总，并用 BPB 比较模型的预测质量。原文节选未给出数据集名称、样本规模及训练集与测试集划分。
- 代码任务集合：包括 MBPP、Codex 和 HumanEval，以 BPB 衡量代码序列建模能力。这里测试的是模型给参考代码分配概率的能力，而不是常见的程序执行通过率；原文节选未报告样本规模、划分或生成与执行协议。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

通用与问答任务上预测正确样本所占比例；它直接反映离散答案是否正确，但不显示错误预测的置信程度。 （越高越好，因为更高值表示更多样本被正确回答。）

</div>
<div class="metric-item" markdown="1">

**BPB（bits per byte）**

按字节归一化的负对数似然，衡量模型为真实文本或代码序列分配概率的质量；归一化后可在不同分词方式或序列长度下进行较公平的比较。它不是数学答案正确率，也不是代码执行通过率。 （越低越好，因为较低 BPB 表示模型给真实序列分配了更高概率、预测不确定性更小。）

</div>
<div class="metric-item" markdown="1">

**STD（跨随机种子的标准差）**

同一配置在不同随机种子下结果的离散程度，用于观察训练和评测稳定性；标准差必须结合均值理解，较小波动本身不保证模型性能较高。 （通常越低越稳定，但只有在平均性能不下降时，较低 STD 才构成明确优势。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 通用与问答任务准确率：LoopMTP 在 $T=9$ 时与非循环基线及 LoopFormer 对比

<div class="result-value" markdown="1">

LoopMTP 在 $T=9$ 时七项任务平均准确率为 $50.02\pm0.16$，高于非循环基线的 $46.28\pm0.28$，也高于 LoopFormer 在其最佳所列循环次数 $T=5$ 时的 $47.88\pm0.49$。按均值计算，LoopMTP 相对非循环基线提高约 $8.1\%$，绝对提高 3.74 个百分点。

</div>

作者数据表明，带潜在多词元指导的循环计算在通用与问答任务上能将额外计算转化为更高平均正确率，而且结果波动较小。该结论覆盖七项任务的宏观平均，但不意味着每个任务和每个循环数都占优：正文明确指出唯一例外是 $T=3$ 时的 Winogrande；同时，这些结果不能证明收益必然来自某一个单独组件。

<div class="result-source" markdown="1">

来源：附录 E，表 5（General & QA Tasks, Accuracy）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Non-looped 31.60 1.16 59.90 0.54 38.48 0.04 50.96 0.27 44.85 0.27 65.98 0.24 32.16 0.89 46.28 0.28
LoopFormer Loops=5 35.24 1.40 59.65 0.98 41.61 0.86 52.35 0.84 45.87 0.23 65.29 0.56 35.13 0.62 47.88 0.49
LoopMTP (ours) Loops=9 36.01 0.39 63.71 0.53 44.64 0.16 52.70 0.35 47.78 0.16 67.86 0.33 37.47 1.46 50.02 0.16

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 数学与推理任务：七类数学题上的平均 BPB

<div class="result-value" markdown="1">

LoopMTP 在 $T=7$ 时取得最低平均 BPB $0.6575\pm0.0021$，优于非循环基线的 $0.7114\pm0.0024$，也优于 LoopFormer 的最佳所列结果 $0.6898\pm0.0116$（$T=5$）。LoopMTP 从 $T=3$ 到 $T=9$ 的平均 BPB 均低于非循环基线。

</div>

这说明 LoopMTP 更擅长为数学与推理文本中的真实后续序列分配概率，并且优势覆盖七个数学类别。需要注意，BPB 改善不等同于最终数学答案准确率提升；节选没有提供基于答案匹配、推理步骤正确性或执行验证的指标。

<div class="result-source" markdown="1">

来源：附录 E，表 7（Math & Reasoning Tasks, BPB）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Non-looped 0.7015 0.0029 0.6839 0.0023 0.7696 0.0032 0.7321 0.0047 0.7661 0.0009 0.6696 0.0019 0.6572 0.0028 0.7114 0.0024
LoopFormer Loops=5 0.6789 0.0133 0.6604 0.0113 0.7543 0.0095 0.7053 0.0116 0.7461 0.0127 0.6490 0.0129 0.6348 0.0108 0.6898 0.0116
LoopMTP (ours) Loops=7 0.6414 0.0030 0.6306 0.0017 0.7179 0.0013 0.6771 0.0035 0.7100 0.0023 0.6153 0.0025 0.6101 0.0021 0.6575 0.0021

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 代码任务：MBPP、Codex 与 HumanEval 上的平均 BPB

<div class="result-value" markdown="1">

LoopMTP 在 $T=7$ 时取得最低平均代码 BPB $0.7822\pm0.0019$，优于非循环基线的 $0.8624\pm0.0040$，也优于 LoopFormer 的最佳所列结果 $0.8348\pm0.0163$（$T=5$）。在该配置下，MBPP 和 Codex 的 BPB 分别为 $0.8812\pm0.0053$ 与 $0.6832\pm0.0017$。

</div>

结果支持 LoopMTP 改善代码序列概率建模，并显示 $T=7$ 是所列配置中的最佳点；继续增加到 $T=9$ 后平均 BPB 回升，说明更多循环并非单调带来收益。由于没有报告 pass@k 或实际执行测试，这不能直接证明模型生成了更多功能正确的程序。

<div class="result-source" markdown="1">

来源：附录 E，表 8（Coding Tasks, BPB）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Non-looped 0.9710 0.0033 0.7538 0.0048 0.8624 0.0040
LoopFormer Loops=5 0.9320 0.0153 0.7375 0.0186 0.8348 0.0163
LoopMTP (ours) Loops=7 0.8812 0.0053 0.6832 0.0017 0.7822 0.0019

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验节选主要报告聚合均值、标准差和循环次数扫描，没有提供逐样本定性案例、统计显著性检验、相同训练与推理计算预算的核算，或潜在 MTP 与轻量门控的独立去除实验，因此可以确认整体方法有效，但难以精确分解各组件的因果贡献。
- 数学、推理和代码任务仅报告 BPB；该指标衡量真实序列的概率建模质量，却不能直接验证最终数学答案或程序执行是否正确。此外，节选只展示到 $T=9$，不能据此验证摘要所称更高循环次数下的稳定性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Non-looped：不重复使用 Transformer 层栈的基线，用于判断循环计算及其监督是否确实优于常规固定深度模型。
- LoopFormer：同样复用层栈、但不采用 LoopMTP 潜在多词元指导的循环基线，用于区分收益究竟来自“增加循环计算”，还是来自 LoopMTP 对中间循环状态的监督与信息保留设计。该基线在每个循环次数下分别搜索学习率、权重衰减和 warmup ratio，因此是经过专门调参的强对照。
- LoopMTP 的不同循环次数配置（$T=3,5,7,9$）：用于检验增加有效计算深度后性能与稳定性的变化，不是独立模型家族。

**实验想回答的问题**

- 在参数共享的循环 Transformer 中，LoopMTP 能否相较非循环模型和未使用潜在多词元预测指导的 LoopFormer，提高通用问答、数学推理与代码任务的性能？
- 随着循环次数 $T$ 从 3 增至 9，LoopMTP 是否仍能稳定训练并持续受益，而不是出现性能退化、随机种子间剧烈波动或训练发散？

**实验实现**

附录 E 报告各配置跨 3 个随机种子的平均值和标准差，除非另有说明。LoopFormer 的 $T=3$ 配置有一次训练发散，因此该行只汇总 2 个随机种子；此外，LoopFormer 针对每个循环次数分别搜索学习率、权重衰减和 warmup ratio。实验比较 $T=3,5,7,9$，并分别报告通用问答准确率、通用问答 BPB、数学推理 BPB 和代码 BPB。节选未提供模型参数量、训练语料、训练步数、计算预算、解码策略或显著性检验，因而不能从这些表单独判断训练成本是否相同。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| LoopMTP 的循环次数扫描：代码任务上比较 $T=3,5,7,9$ | 平均代码 BPB 随循环次数由 $T=3$ 的 $0.8071\pm0.0083$ 降至 $T=5$ 的 $0.7921\pm0.0037$，再降至 $T=7$ 的 $0.7822\pm0.0019$；到 $T=9$ 时回升为 $0.8003\pm0.0101$。 | 该扫描隔离的是推理循环次数对同一方法的影响。结果显示适量增加循环可改善代码建模，但超过任务的有效计算需求后会出现回报递减甚至退化；因此，LoopMTP 缓解了循环不稳定问题，却没有证明无限增加循环都有效。 | 附录 E，表 8（Coding Tasks, BPB）<br><span class="experiment-evidence">LoopMTP (ours) Loops=3 0.9072 0.0113 0.7070 0.0107 0.8071 0.0083
Loops=5 0.8876 0.0042 0.6965 0.0062 0.7921 0.0037
Loops=7 0.8812 0.0053 0.6832 0.0017 0.7822 0.0019
Loops=9 0.8942 0.0115 0.7064 0.0087 0.8003 0.0101</span> |
| 循环监督设计对稳定性的对照：LoopFormer 与 LoopMTP 在高循环次数下的数学 BPB | 在 $T=7$ 时，LoopFormer 的平均数学 BPB 为 $1.7259\pm1.3763$，而 LoopMTP 为 $0.6575\pm0.0021$；在 $T=9$ 时，两者分别为 $1.6034\pm1.3039$ 和 $0.6586\pm0.0049$。LoopFormer 的均值明显恶化且跨种子波动极大，LoopMTP 则保持接近其最佳值。 | 这一对照主要检验：仅增加循环是否足够，还是循环中的潜在前瞻监督与门控信息保留对稳定训练至关重要。结果支持后者，但这不是严格的单组件消融，因为 LoopMTP 与 LoopFormer 可能同时存在多处设计差异；若要分别归因于潜在 MTP 和门控机制，还需要去除其中单个组件的实验。 | 附录 E，表 7（Math & Reasoning Tasks, BPB）<br><span class="experiment-evidence">LoopFormer Loops=7 1.7655 1.4466 1.5079 1.1230 1.8546 1.4597 1.8537 1.5247 1.7187 1.2894 1.5966 1.2564 1.7844 1.5343 1.7259 1.3763
Loops=9 1.6296 1.3613 1.4130 1.0741 1.7195 1.3811 1.7134 1.4341 1.6130 1.2377 1.4812 1.1884 1.6545 1.4508 1.6034 1.3039
LoopMTP (ours) Loops=7 0.6414 0.0030 0.6306 0.0017 0.7179 0.0013 0.6771 0.0035 0.7100 0.0023 0.6153 0.0025 0.6101 0.0021 0.6575 0.0021
Loops=9 0.6410 0.0040 0.6322 0.0024 0.7180 0.0061 0.6819 0.0073 0.7132 0.0045 0.6137 0.0032 0.6103 0.0071 0.6586 0.0049</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出以潜在多token预测监督循环Transformer的新架构与训练目标，旨在以固定参数量增强推理能力。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`515dab404aa5f13e6c3b1d5811ec63cecc0190d30435e017525ebf17cacc7a01`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
