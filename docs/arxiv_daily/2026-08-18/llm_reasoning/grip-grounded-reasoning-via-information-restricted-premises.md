---
title: "[论文解读] GRIP: Grounded Reasoning via Information-Restricted Premises"
description: "[arXiv 2608.16776][LLM Reasoning] 本文将检索增强生成中的“查询支配”视为表示容量分配问题，并提出让查询保留高容量通路、让证据经过低维随机瓶颈的 GRIP，以促使证据表示携带查询无法提供的剩余信息。"
arxiv_id: "2608.16776"
announcement_date: "2026-08-18"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:27:45.042948+00:00"
source_sha256: "7006908168963212b317949b7571cf16e98a7aadaac755c3aa13f7c37a0b78e8"
tags:
  - "LLM Reasoning"
  - "检索增强生成"
  - "信息瓶颈"
  - "有依据推理"
  - "查询主导"
  - "互信息"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.16776</p>

# GRIP: Grounded Reasoning via Information-Restricted Premises

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Lirui Teng</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of Waterloo, Waterloo, ON, Canada</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.16776) · [PDF 下载](https://arxiv.org/pdf/2608.16776) · **关键词** 检索增强生成, 信息瓶颈, 有依据推理, 查询主导, 互信息<br>


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

本文将检索增强生成中的“查询支配”视为表示容量分配问题，并提出让查询保留高容量通路、让证据经过低维随机瓶颈的 GRIP，以促使证据表示携带查询无法提供的剩余信息。

**不用术语来说**：检索增强生成本应根据外部材料回答问题，但模型即使拿到相关证据，也可能主要依赖问题本身和训练时记住的知识；一旦这些内部知识与证据冲突，模型便可能忽略证据并生成没有依据的答案。作者认为，问题不只是模型没有找对材料，而是问题文本在内部表示中占据了过多容量，使检索证据实际上难以影响最终推理。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将查询支配形式化为查询与证据表示之间的依赖问题，并提出查询—潜变量依赖指标，即互信息 $I(Q;z_k)$；其中 $Q$ 是查询，$z_k$ 是第 $k$ 个证据表示。该指标用于诊断证据通道是否退化成查询的压缩副本，而非真正补充查询缺失的信息。
- 作者提出 GRIP 的容量非对称设计：查询通过全维旁路直接送入解码器，检索证据则经过维度约为 $d_z\approx 4$ 的随机瓶颈。在严格容量预算下，与查询重复的信息缺乏保留价值，因而训练梯度被期望推动证据通道优先编码信息残差。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究检索增强生成（RAG）：语言模型先根据问题检索外部文本证据，再基于问题与证据生成答案，目标可表示为建模条件分布 $P(Y\mid Q,E)$。其中，$Q$ 是用户问题，$E$ 是检索到的证据，$Y$ 是输出答案。论文关注的核心背景问题是：即使检索证据与问题相关，模型仍可能主要依赖参数化知识和问题本身，而低估或忽略证据；因此，关键不只是检索哪些内容，也包括如何分配问题与证据在内部表示中的信息容量。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**检索增强生成（RAG）**

RAG 将外部检索文本作为生成模型的额外条件，使模型能够利用参数化知识之外的证据回答问题。理想情况下，答案应同时依赖问题 $Q$ 和证据 $E$，尤其应在二者冲突时以证据为依据。

</div>
<div class="concept-item" markdown="1">

**信息瓶颈**

信息瓶颈通过限制某个表示能够携带的信息量，迫使它保留对任务最有用的内容并丢弃冗余内容。本文将证据通道压缩并加入随机性，使证据表示不能完整复制问题，而需要传递问题未提供的补充信息。

</div>
<div class="concept-item" markdown="1">

**互信息与查询主导**

互信息 $I(Q;z_k)$ 衡量问题 $Q$ 与证据表示 $z_k$ 共享的信息量；数值较高意味着证据表示可能主要编码了问题中的信息。论文将这种证据表示被问题高容量路径压制、最终退化为问题副本的状态称为查询主导（query dominance）。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定问题 $Q$ 和由检索器提供的外部证据 $E$，模型需要输出答案 $Y$，即学习 $P(Y\mid Q,E)$。标准 RAG 通常把问题和证据送入共享的高维潜在表示，再由解码器生成答案；本文假设问题具有一条高容量路径，而证据与问题共享表示空间，因而模型可以在仅依赖 $P(Y\mid Q)$ 时获得较低训练损失。研究问题是：如何在不削弱解码器访问问题的情况下，限制证据表示的容量，使其主要编码相对于问题的残差信息，并提高生成结果对证据的依赖。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$Q$**

输入问题或查询。

</div>
<div class="notation-item" markdown="1">

**$E$**

从外部语料中检索得到的证据文本。

</div>
<div class="notation-item" markdown="1">

**$Y$**

模型生成的答案或目标输出。

</div>
<div class="notation-item" markdown="1">

**$z_k$**

第 $k$ 个位置或步骤上的证据潜在表示；论文用 $I(Q;z_k)$ 衡量它与问题之间的查询—潜在依赖。

</div>

</div>

**直接相关的工作**

- **Self-RAG**: Self-RAG 在生成过程中加入反思标记，用于评价是否需要检索以及检索内容是否有用。论文认为，这类方法主要在解码或检索批评层面干预，并未根本改变问题与证据在潜在表示中的容量分配，因此仍可能存在查询主导。
- **RAFT-style training**: RAFT 式训练通过训练模型识别并忽略干扰证据，改善证据使用能力。本文将其视为监督或训练策略层面的干预，并指出即使模型学会内容选择，高维表示仍可能优先分配容量给问题相关特征和参数化捷径；GRIP 则直接限制证据通道的表示容量。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

RAG 的目标是建模 $P(Y\mid Q,E)$，即依据查询 $Q$ 与外部证据 $E$ 生成答案 $Y$；但实际模型常退回到仅依赖查询和参数化知识的近似 $P(Y\mid Q)$。当模型记忆与检索证据不一致时，这种证据利用不足会直接造成无依据回答，也使增加检索文本未必能改善可靠性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **解码阶段的证据强化方法**：Self-RAG 通过反思标记让模型评价检索及其结果；上下文感知解码则重新调整输出词元概率，使生成更偏向检索内容。两者主要在生成决策阶段提高证据的显式影响。
- **监督训练与抗干扰方法**：RAFT 风格训练向模型提供包含干扰项的检索上下文，并监督模型识别有用证据、忽略无关材料，从内容选择层面提升面对噪声检索结果时的鲁棒性。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 上述方法主要干预解码规则或训练监督，却没有直接改变查询与证据融合时的潜在表示几何；证据仍可与查询共享高维空间，因此查询对内部状态的主导地位可能继续存在。
- 高维证据表示能够把大量容量分配给与查询一致的特征及参数化捷径，使检索内容只成为边缘修正。其后果是：即使检索结果相关、模型也接受了证据使用训练，证据通道仍可能退化为查询的压缩副本，而没有传递查询之外的信息。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种从表示容量层面强制证据发挥互补作用的机制，也缺少与该机制相匹配、可跨模型诊断查询支配程度的量化指标。尚未解决的关键是：如何在保留完整查询信息的同时，限制证据通道编码查询重复特征，并检验其是否转而承载条件于查询之后仍有用的信息残差。

</div>
<div markdown="1"><span>核心问题</span>

在查询仍可通过高带宽路径直接进入解码器的条件下，能否通过对证据表示同时施加极低维度与随机噪声约束，降低查询与证据潜变量之间的互信息 $I(Q;z_k)$，从而提高外部证据的实际利用程度并减少幻觉？

</div>
<div markdown="1"><span>作者直觉</span>

可以把查询通路看作已经完整提供“题目告诉模型的内容”，把受限证据通路看作只能传递少量补充信息的窄通道。由于重复传输查询信息既占容量又不能为解码器增加新信息，训练会倾向于保留查询中没有、但回答所需的证据特征。随机性进一步抑制脆弱的查询对齐编码；作者据此推测，低维限制与噪声的组合比单独使用任一约束更可能形成面向信息残差的证据表示。不过原文明确承认，这一条件残差化机制尚未得到形式化证明。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

GRIP将检索增强推理设计成一条逐步循环的非对称信息通路。给定查询$Q$、外部语料库$M_{\mathrm{ext}}$和当前推理上下文$C_k$，系统先检索候选段落并用下一步预测熵重排，再从最佳段落中抽取能够保持预测信息的最短前提$p_k$，通过自然语言推断验证其确实受原段落支持，随后把$p_k$压缩为仅四维且带高斯噪声的状态$z_k$；解码器同时接收完整维度的$Q$与$C_k$以及受限的$z_k$，生成当前推理步骤$i_k$。经验证的$p_k$和$i_k$随后写入$C_{k+1}$，循环直到生成答案标记或达到最大步数$K$。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 迭代检索与熵引导重排

稠密检索器先返回前$m$个候选段落$R_m^{(k)}$；系统再以候选段落条件下目标推理步骤$i_k$的预测熵为准，选择使$H_{\Theta}(i_k\mid r,C_k,Q)$最小的段落$r^{*(k)}$。该重排是依赖当前解码器状态的非可微选择，训练前五轮暂不启用。

<div class="method-step__io" markdown="1">

**输入**：查询$Q$、当前推理上下文$C_k$和外部语料库$M_{\mathrm{ext}}$。<br>
**输出**：当前步骤最有助于确定下一步推理的段落$r^{*(k)}$。

</div>

**直观理解**：稠密检索负责先找出主题相关的材料，熵重排再从中挑选让模型对“下一步该说什么”最确定的材料。它优化的是当前推理步骤的可预测性，而不只是查询与段落的表面相似度。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 预测性跨度抽取与蕴含验证

冻结的RoBERTa抽取器$\Theta_{\mathrm{ext}}$从$r^{*(k)}$中生成子跨度$p_k$，以跨度条件分布和完整段落条件分布之间的KL匹配保持预测作用，同时用长度稀疏惩罚压缩文本；冻结的DeBERTa-v3-large验证器仅接受满足$P_{\mathrm{NLI}}(\mathrm{entailment}\mid r^{*(k)},p_k)>0.75$的跨度。抽取器交叉注意力中的查询词元被遮蔽，避免前提表示直接依赖查询。

<div class="method-step__io" markdown="1">

**输入**：选中段落$r^{*(k)}$和当前上下文$C_k$。<br>
**输出**：短小且由原段落蕴含的已验证前提$p_k$；未通过验证时丢弃该步骤并保持上下文不变。

</div>

**直观理解**：这一阶段把整篇材料缩成真正支撑下一步推理的一小段，并检查该小段没有歪曲原文。遮蔽查询相当于要求抽取器依据证据本身选句，减少它把问题内容重新编码成所谓“证据”的机会。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 随机低维瓶颈

系统对$p_k$的词元表示做均值池化，再依次经过矩阵$W_1$、ReLU和矩阵$W_2$，最后加入方差为$1.0$的高斯噪声，得到四维状态$z_k$。低维投影、前提级文本压缩和随机噪声共同限制证据通道可传递的信息量。

<div class="method-step__io" markdown="1">

**输入**：已验证前提$p_k$。<br>
**输出**：受容量约束的证据状态$z_k\in\mathbb{R}^{4}$。

</div>

**直观理解**：可以把它理解为要求证据只能通过一张很窄且有噪声的纸条进入当前推理。纸条空间有限，模型更难复制问题中已有的信息，只能优先保留对答案真正有增量价值的证据特征。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 非对称解码与上下文更新

解码器把$Q$作为高带宽前缀输入，将$z_k$作为带可学习位置嵌入的单个特殊词元注入，并生成当前推理步骤$i_k$；随后按$C_{k+1}=C_k\oplus(p_k,i_k)$保存已验证跨度和本步推理。若$i_k$生成答案标记则提前返回，否则继续检索，达到$K$步后返回$i_K$。

<div class="method-step__io" markdown="1">

**输入**：完整维度的查询$Q$、历史上下文$C_k$以及受限证据状态$z_k$。<br>
**输出**：当前推理步骤$i_k$、更新后的上下文$C_{k+1}$，或最终答案$\hat{a}$。

</div>

**直观理解**：查询和既有推理可以完整进入解码器，但决定当前证据如何影响推理的即时信号必须经过四维瓶颈。前提文本只会在当前步骤完成后进入后续上下文，因此它能保留句子语义，却不能在同一步绕过瓶颈直接替代$z_k$。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 随机低维证据瓶颈

$$
z_{k}=W_{2}\,\sigma\!\left(W_{1}\cdot\operatorname{pool}(p_{k})\right)+\varepsilon_{k},\qquad \varepsilon_{k}\sim\mathcal{N}\!\left(0,\sigma^{2}I_{d_{z}}\right)
$$

**符号说明**

- $p_k$：第$k$步从检索段落中抽取并通过蕴含验证的前提跨度。
- $\operatorname{pool}(p_k)$：对前提$p_k$的词元表示进行均值池化所得的定长向量。
- $W_1,W_2$：随机瓶颈中可训练的第一层和第二层投影矩阵。
- $\sigma(\cdot)$：瓶颈投影中的ReLU非线性激活函数；这里的$\sigma(\cdot)$与噪声标准差$\sigma$同符号但含义不同。
- $z_k$：传给解码器的第$k$步低维证据状态，实现中维数为$d_z=4$。
- $\varepsilon_k$：加入瓶颈输出的零均值各向同性高斯噪声。
- $\sigma^2$：高斯噪声方差，实现中取$1.0$。
- $I_{d_z}$：$d_z$维单位矩阵，表示各维噪声相互独立且方差相同。

<div class="equation-explanation" markdown="1">

**直观理解**：该式先把一段自然语言证据压缩成极低维向量，再主动加入噪声。低维度限制可携带的特征数量，噪声削弱对脆弱相关模式的精确复制，两者共同使$z_k$更难充当第二份查询表示。<br>
**原文位置**：第4.3节，公式(7)

</div>

</div>

<div class="equation-block" markdown="1">

#### 逐步推理负对数似然目标

$$
\mathcal{L}_{\mathrm{task}}=-\sum_{k=1}^{K}\log P_{\Theta_{\mathrm{gen}}}\!\left(i_{k}\mid z_{k},C_{k},Q\right)
$$

**符号说明**

- $\mathcal{L}_{\mathrm{task}}$：训练时最小化的逐步推理负对数似然损失。
- $K$：一条训练样本中允许或标注的最大推理步数。
- $i_k$：第$k$步的目标推理文本或推理步骤。
- $P_{\Theta_{\mathrm{gen}}}$：由可训练生成参数$\Theta_{\mathrm{gen}}$定义的条件生成概率。
- $\Theta_{\mathrm{gen}}=\{W_1,W_2,\Theta_{\mathrm{dec}}\}$：参与优化的参数集合，包括瓶颈两层投影和解码器参数。
- $Q$：原始查询，以完整维度输入解码器。
- $C_k$：第$k$步之前累积的已验证前提与历史推理上下文。
- $z_k$：第$k$步经随机瓶颈得到的受限证据状态。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标要求模型在给定查询、历史上下文和受限证据状态时复现每一步正确推理。论文并未显式优化条件信息瓶颈目标；容量限制来自网络结构和噪声，而任务损失负责决定有限容量中哪些证据信息最有助于预测$i_k$。<br>
**原文位置**：第4.6节，公式(9)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练只最小化逐步目标推理的负对数似然$\mathcal{L}_{\mathrm{task}}$，梯度更新范围为$\Theta_{\mathrm{gen}}=\{W_1,W_2,\Theta_{\mathrm{dec}}\}$；稠密检索器、跨度抽取器和NLI验证器始终冻结。论文用条件信息瓶颈$-I(Z_k;Y\mid Q)+\beta I(Z_k;Q)$解释机制：理想上应保留给定$Q$后仍能预测目标$Y$的信息，并抑制与$Q$重复的信息，但作者明确说明GRIP没有直接优化这一互信息目标，也不主张二者形式等价。具体而言，$Q$已经通过完整维度旁路到达解码器，因此$z_k$中仅仅重复查询的特征通常不能进一步降低条件生成损失；在四维和噪声造成的紧张容量预算下，梯度更有压力把容量分配给证据带来的条件增量。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 预测性前提构造器**

该模块由冻结的RoBERTa跨度抽取器和冻结的DeBERTa-v3-large自然语言推断验证器组成。抽取器用预测分布KL匹配与长度稀疏约束寻找最短有效跨度，验证器以$0.75$的蕴含概率阈值过滤跨度；查询词元不参与抽取器的交叉注意力。

> 直观理解：它解决“什么内容有资格进入证据通道”的问题：材料既要足以保持下一步预测，又必须忠实于原段落。冻结模块还使实验中的主要学习变化集中在瓶颈和解码器，而不是让抽取器偷偷适应答案。

**2. 随机证据瓶颈**

瓶颈$B_{\theta}$采用两层投影、ReLU、均值池化和加性高斯噪声，将前提压缩到$d_z=4$，噪声方差为$\sigma^2=1.0$。在归一化后投影功率约为$P\approx1$的高斯信道近似下，作者将每步信息预算解释为约$2$至$4$比特。

> 直观理解：该模块不是单纯为了节省计算，而是人为制造证据与查询之间的容量不对称。由于查询已经完整提供，有限的证据容量若再次表示查询就是浪费，训练因而倾向于保留查询之外、对目标推理有帮助的信息。

**3. 非对称迭代解码器**

解码器以完整维度访问$Q$和$C_k$，但只能通过单个特殊词元访问四维噪声状态$z_k$，两条输入路径的容量相差约三个数量级。每步先由$z_k$参与生成$i_k$，再将文本前提$p_k$和$i_k$追加到下一步上下文。

> 直观理解：模块的关键不是删除查询，而是限制证据成为查询副本，同时保留多跳推理所需的历史文本。先生成、后写入前提的时间顺序，使当前步骤必须使用瓶颈信号，而后续步骤仍能读取必要的自然语言语义。

**训练与推理**

训练采用两阶段课程。第1阶段为第1至5轮，绕过熵重排，仅使用稠密检索排名最高的段落，让随机瓶颈和解码器先学会在稳定输入上生成目标步骤；第2阶段为第6至20轮，启用基于$H_{\Theta}(i_k\mid r,C_k,Q)$的熵引导候选选择，使检索段落与当前解码状态联动。两个阶段都冻结检索器、$\Theta_{\mathrm{ext}}$和NLI验证器，只训练瓶颈与解码器；熵选择本身是非可微决策，不通过该选择操作反向传播。

推理从$C_1=\emptyset$开始，并对$k=1,\ldots,K$重复四个阶段：根据$Q$和$C_k$检索前$m$个候选，以最低下一步预测熵选出$r^{*(k)}$，抽取$p_k$并检查其蕴含分数是否达到阈值$\tau$；验证失败则跳过本步且不改变上下文，验证成功则生成噪声状态$z_k$并解码$i_k$。之后以$C_{k+1}=C_k\oplus(p_k,i_k)$更新历史；若$i_k$含答案标记则提前输出，否则在达到$K$步时输出$i_K$。由于$p_k$在$i_k$生成后才被追加，当前步骤不能通过上下文直接读取该跨度，但后续步骤仍能利用其完整文本语义。

**复现信息**

公平解释该设计所需的核心配置是：证据状态维数$d_z=4$，加性高斯噪声方差$\sigma^2=1.0$，前提表示采用均值池化，瓶颈使用两层投影和ReLU；NLI验证器是冻结的DeBERTa-v3-large，蕴含概率阈值为$0.75$，跨度抽取器为冻结的RoBERTa模型。查询$Q$与上下文$C_k$按模型完整维度进入解码器，$z_k$则作为带可学习位置嵌入的单个特殊词元注入。

复现时还必须保留两个容易误读的顺序约束：熵重排只在课程训练第6轮后启用；每一步先用$z_k$生成$i_k$，再把$p_k$及$i_k$写入$C_{k+1}$。论文给出的高斯信道解释假设归一化后噪声前投影向量的平均功率约为$P\approx1$，由此估计每步容量约为$2$至$4$比特；这是基于信道近似的容量解释，不等于对实际神经表示互信息的精确测量。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HotpotQA：含干扰文档的多跳问答基准，是主实验和消融实验的核心数据集。它同时检验跨文档推理、答案 EM/F1、生成幻觉率以及查询与瓶颈表示之间的信息依赖。
- StrategyQA：需要隐式多步推理的二元问答基准，以准确率评价。它用于判断模型能否处理无法直接从单个文本片段抽取答案的推理任务。
- SQuAD 2.0：单跳抽取式问答基准，且包含不可回答问题。它用于检验复杂的迭代证据处理在不需要显式多跳分解时是否仍然有效，并暴露 Self-Ask 可能产生的分解开销。原文节选未提供各数据集规模、训练/验证/测试划分及具体评测 split。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**EM/Acc**

EM 要求预测答案与标准答案规范化后完全匹配；Acc 表示任务级正确率，其中 StrategyQA 使用 yes/no 准确率，ProofWriter 使用证明准确率。二者衡量最终任务是否答对。 （越高越好，因为更高数值表示更多样本得到完全正确的答案或证明。）

</div>
<div class="metric-item" markdown="1">

**F1**

衡量预测答案与标准答案之间 token 级精确率和召回率的调和平均，可对部分匹配给予分数；适用于 HotpotQA、2WikiMultihopQA 和 SQuAD 2.0。 （越高越好，因为它表示预测覆盖正确答案内容的程度更高。）

</div>
<div class="metric-item" markdown="1">

**Hall. (%)**

生成声明中不能由检索证据蕴含的比例。流水线内的 DeBERTa-v3 验证器既参与前提筛选，也用于主要评价，因此作者另用 MiniCheck 复核，以检查评价与训练选择信号共用验证器造成的循环性。 （越低越好，因为更低比例表示生成内容更受检索证据支持。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 五类推理任务上的总体任务性能

<div class="result-value" markdown="1">

作者报告 GRIP 在全部五个数据集上均超过最强的非 GRIP 基线，并在全部五项任务上超过架构匹配的 Llama-3 Iterative；其中 HotpotQA 的 EM 为 76.5、F1 为 80.3，StrategyQA 准确率为 73.4，2Wiki EM/F1 为 71.2/76.1，ProofWriter 准确率为 85.6，SQuAD 2.0 EM/F1 为 82.1/85.7。

</div>

作者的结论是，GRIP 的收益跨越了干扰型多跳、隐式推理、显式两跳、符号推理和单跳抽取等不同任务形态。分析上，这说明方法并非只适配一种多跳数据集；但除 HotpotQA 与 SQuAD 2.0 外，节选没有给出其余任务的显著性检验，因此不能仅凭均值断言所有任务上的优势都具有统计显著性，也不能据此证明对其他模型或检索索引普遍有效。

<div class="result-source" markdown="1">

来源：第 5.2 节，Table 1 及其后正文

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GRIP improves over the strongest non-GRIP baseline on every dataset, and outperforms the architecture-matched Llama-3 Iterative control on all five benchmarks—by +7.2 EM on HotpotQA and +4.1 accuracy points on StrategyQA—indicating that capacity asymmetry contributes beyond the iterative reasoning schedule.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 与架构匹配迭代对照的比较及显著性

<div class="result-value" markdown="1">

相对 Llama-3 Iterative，GRIP 在 HotpotQA 上将 EM 从 69.3 提升到 76.5，即增加 7.2 点；在 SQuAD 2.0 上将 EM 从 78.0 提升到 82.1，即增加 4.1 点。作者同时报告成对 bootstrap 比较在 HotpotQA 的 7.2 点提升和 SQuAD 2.0 的 3.7 点提升上均满足 $p<0.01$；节选中 SQuAD 的表格差值与正文所述 3.7 点存在不一致，需要核对原始论文。

</div>

该对照保持两步推理、检索、重排、抽取和 NLI 门控一致，因此比 Standard RAG 更能隔离随机信息瓶颈的增量贡献。它支持“容量受限的证据注入优于把验证前提作为全维文本注入”的解释，但仍不是严格的因果证明，因为瓶颈可能同时改变优化难度、表示尺度或解码器接收信息的形式。SQuAD 数值冲突也使其具体效应量需要源文复核。

<div class="result-source" markdown="1">

来源：第 5.2 节，Table 1 后正文

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Paired bootstrap comparisons are significant at p<0.01 on HotpotQA (+7.2) and SQuAD 2.0 (+3.7).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 证据忠实度及独立验证器复核

<div class="result-value" markdown="1">

在流水线内验证器下，HotpotQA 幻觉率由 Standard RAG 的 31.7% 降至 GRIP 的 8.6%，2Wiki 由 31.2% 降至 9.8%；在架构匹配比较中，HotpotQA 由 Llama-3 Iterative 的 28.7% 降至 8.6%。改用 MiniCheck 复核时，两种验证器的一致率为 89.0%，Cohen's $\kappa=0.77$，GRIP 的 HotpotQA 幻觉率由 8.6% 上升到 10.1%，但仍低于各基线。

</div>

作者据此提出较窄的结论：低幻觉结果并非只由原有 DeBERTa-v3 验证器的特殊偏好造成。独立验证器具有较高但非完美的一致性，而且复核后幻觉率有所上升，因此结果支持一定的稳健性，却不能证明评价完全无偏，更不能证明该机制对任意验证模型都成立。

<div class="result-source" markdown="1">

来源：第 5.2 节，Table 1 后正文

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

This grounding result is robust to the choice of verifier: rescoring with MiniCheck [20] yields 89.0% agreement with the in-pipeline verifier (Cohen’s κ=0.77), and the HotpotQA hallucination rate rises only from 8.6% to 10.1%, remaining well below every baseline—supporting the narrower claim that the gains are not specific to the original verifier, without establishing model-agnosticism.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验虽然覆盖五种推理形态，但所有系统共享同一个冻结 DPR-Wiki 检索底座，生成器也围绕 Llama-3-8B 设置；因此结果尚不能证明容量不对称机制能泛化到其他检索器、索引语料、生成模型规模或领域。作者对独立验证器结果也仅主张“不特定于原验证器”，明确没有建立 model-agnosticism。
- 节选未报告数据集规模、具体 split、完整检索与验证流水线统计或原子性分析；后三者被指向补充材料或附录。此外，SQuAD 2.0 的 Table 1 数值给出 GRIP 与 Llama-3 Iterative 的 EM 差为 4.1 点，而正文显著性句写为 3.7 点，属于需要查验原表、评测口径或勘误的内部不一致。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Standard RAG：使用 DPR 检索、直接拼接 passage，并由 Llama-3-8B 解码。它代表常规的“检索后把较完整证据交给生成器”方案，用于比较信息受限证据通道相对标准 RAG 的价值。
- Self-Ask：通过提示让模型迭代生成并回答子问题，但不改变证据进入解码器的路径。它检验性能是否仅靠显式问题分解即可获得。
- Llama-3-8B Iterative：最关键的架构匹配对照。它与 GRIP 使用相同的两步推理、检索器、熵重排、span 抽取、NLI 门控和解码超参数，但把验证后的前提 $p_k$ 作为普通全维文本送入解码器，而不经过随机瓶颈。因此，二者差异主要用于估计“容量不对称”本身的作用，而不是迭代流程或验证模块的作用。

**实验想回答的问题**

- 在相同检索底座、计算预算和两步推理流程下，GRIP 的信息受限随机瓶颈是否比标准 RAG、问题分解方法及架构匹配的迭代模型带来更高的任务正确率和更低的幻觉率？
- 性能提升是否确实来自容量不对称的证据通道；抽取、NLI 验证、瓶颈宽度与随机噪声分别如何影响任务信息保留、查询冗余和证据忠实度？

**实验实现**

所有系统共享冻结的 DPR-Wiki 索引、tokenization 和计算预算，但重排、抽取及 NLI 过滤后真正送达解码器的证据仍因方法而异。GRIP 每个样本执行 $K=2$ 个推理步骤，每步检索 $m=10$ 个 passage。可训练组件采用 AdamW，学习率为 $10^{-4}$、权重衰减为 $0.01$，线性 warmup 1,000 步后使用余弦衰减，并将梯度范数裁剪到 $1.0$；单设备 batch size 为 32、全局为 128。解码使用 nucleus sampling，参数为 $p=0.9$、$T=0.7$。模型在 4 张 A100 80GB GPU 上训练 20 个 epoch，报告三个随机种子的平均值；HotpotQA 上还报告了跨种子标准差。主结果使用成对 bootstrap 显著性检验，另以独立 MiniCheck 验证器复核幻觉判断。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除随机低维瓶颈 | 完整 GRIP 在 HotpotQA 上的 $I(Q;z_k)$ 为 0.47 bits、幻觉率为 8.6%、准确率为 76.5；移除瓶颈后分别变为 14.20 bits、24.3% 和 71.2，准确率下降 5.3 点。 | 该消融保留其他组件，却以 pooled premise embedding 替换低秩投影和噪声后的 $z_k$，因而直接检验限制证据通道容量是否必要。查询与表示的信息依赖大幅上升，并伴随幻觉增加和准确率下降，支持瓶颈是最关键组件；但这里的 $I(Q;z_k)$ 在“无瓶颈”条件下测量的是替代表示，与完整模型的低维随机变量并非完全同构，绝对值比较需谨慎。 | 第 5.3 节，Table 2，Component ablations<br><span class="experiment-evidence">No bottleneck \| 14.20 \| 24.3 \| 71.2 \| −5.3</span> |
| 瓶颈容量扫描 | 以 $d_z=4$ 的完整 GRIP 为参照，$d_z=2$ 时 $I(Q;z_k)=0.31$ bits、幻觉率为 9.2%、准确率为 74.2，下降 2.3 点；$d_z=16$ 时相应数值为 4.73 bits、11.5% 和 72.8，下降 3.7 点。 | 这一组实验隔离瓶颈宽度，在固定噪声方差 $\sigma^2=1.0$ 下检验容量与性能的关系。过窄通道最能压低查询依赖，却会丢失完成任务所需的证据；过宽通道虽然容量更大，却让查询冗余重新进入并提高幻觉。因而最优点是中等宽度 $d_z=4$，而非最小的信息通道。 | 第 5.3 节，Table 2 及其后正文<br><span class="experiment-evidence">The capacity sweep is non-monotonic. A very narrow bottleneck ($d_z=2)$ suppresses QL dependence most strongly but loses task-relevant evidence; a wider one ($d_z=16)$ restores capacity but allows query-redundant information to re-enter.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The title indicates a method for improving grounded reasoning by constraining the premises available to the model.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`7006908168963212b317949b7571cf16e98a7aadaac755c3aa13f7c37a0b78e8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
