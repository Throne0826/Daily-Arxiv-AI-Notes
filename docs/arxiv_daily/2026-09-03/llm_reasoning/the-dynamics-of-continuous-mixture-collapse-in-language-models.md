---
title: "[论文解读] The Dynamics of Continuous Mixture Collapse in Language Models"
description: "[arXiv 2609.02049][LLM Reasoning] 本文追问连续推理状态为何会在预训练语言模型中坍缩，并将原因区分为架构引入的几何失真、训练放大的失真，以及即使在线性传输下仍会发生的软最大值—自回归反馈动力学。"
arxiv_id: "2609.02049"
announcement_date: "2026-09-03"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-03T04:28:40.157681+00:00"
source_sha256: "3931099d71950d093d8da49c1850da047b4b2e7a32a7b2539f0d05caba1b1412"
tags:
  - "LLM Reasoning"
  - "LLM 机制与可解释性"
  - "连续推理"
  - "连续链式思维"
  - "混合状态坍缩"
  - "Transformer"
  - "自回归反馈"
  - "Softmax动力学"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.02049</p>

# The Dynamics of Continuous Mixture Collapse in Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-03</span>
<span><strong>作者</strong> Ali Backour</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Massachusetts Institute of Technology</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.02049v1) · [PDF 下载](https://arxiv.org/pdf/2609.02049v1) · **关键词** 连续推理, 连续链式思维, 混合状态坍缩, Transformer, 自回归反馈, Softmax动力学<br>


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

本文追问连续推理状态为何会在预训练语言模型中坍缩，并将原因区分为架构引入的几何失真、训练放大的失真，以及即使在线性传输下仍会发生的软最大值—自回归反馈动力学。

**不用术语来说**：普通链式思维每一步都必须选定一个词，因此会丢掉其他可能的推理方向；连续推理试图把多个候选按概率混合后继续计算，但实际模型往往不能让这些候选长期共存：某个候选可能迅速占据全部权重，也可能让原本不同的混合状态逐渐变得无法区分。若不知道这种变化来自网络结构、训练所得参数，还是生成反馈机制本身，就难以判断仅靠微调、修改表示或调整解码能否真正解决问题。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者把连续混合坍缩分解为三个可独立致败的来源：Transformer 架构本身会扭曲混合几何关系，训练会显著放大这种扭曲，而软最大值读出与自回归反馈即使在模型完美线性传输混合时也能单独破坏混合。
- 作者提出从二元混合动力学到 $K$ 分量混合的统一分析视角，指出系统会随分量下一步偏好的差异进入放大或收缩状态，并进一步论证精确保留一般需要依赖上下文的校正，其所需信息维数可能随分量数增加。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大型语言模型中的连续推理，即用连续向量或多个候选词表示的加权混合状态替代传统链式思维中的离散中间词。传统自回归生成在每一步从词表分布中选定一个词，从而丢弃其他候选路径；连续推理试图保留这些路径并在后续计算中共同传播，以提高推理状态的压缩能力和探索能力。本文关注的核心背景问题是：理想的混合状态在预训练Transformer模型中能否被稳定保留，而不是在层变换或逐步反馈过程中发生坍缩。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**链式思维推理（Chain-of-Thought, CoT）**

模型通过连续生成自然语言中间步骤来解决问题，而不是直接输出最终答案。每一步通常提交一个离散词，因此其他可能的推理方向不会继续保留。

</div>
<div class="concept-item" markdown="1">

**连续推理状态**

连续推理状态是用于表示中间推理过程的向量或隐状态，不必对应一个可读的自然语言词。它可以在同一状态中保留多个候选推理方向，随后直接作为下一步模型计算的输入。

</div>
<div class="concept-item" markdown="1">

**加权词嵌入混合**

给定词表中各词的嵌入向量，将词概率作为权重进行求和，例如 $e(p)=\sum_i p_i e_i$。直观地说，它把多个候选词的信息压缩为一个连续向量，而不是只选概率最高的词。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

设模型在某一步对词表产生概率分布 $p$，并通过加权词嵌入或其他连续表示形成中间状态，再将该状态反馈给模型以生成后续推理。理想目标是：不同候选成分及其权重能够在模型层变换、softmax读出和自回归反馈后继续对应并保持；实际研究问题则是识别哪些机制会使混合状态退化为单一主导成分，或使不同混合状态变得无法区分。本文考察预训练模型及匹配的随机初始化模型，并进一步讨论包含多个成分的混合，而不是只假设模型始终能线性、无损地传输混合状态。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$p$**

模型在当前推理步骤对词表给出的概率分布或混合权重。

</div>
<div class="notation-item" markdown="1">

**$p_i$**

概率分布 $p$ 中对应第 $i$ 个词或第 $i$ 个混合成分的权重。

</div>
<div class="notation-item" markdown="1">

**$e_i$**

词表中第 $i$ 个词的嵌入向量。

</div>
<div class="notation-item" markdown="1">

**$e(p)$**

由概率分布 $p$ 加权得到的连续推理状态，即各词嵌入的加权和。

</div>

</div>

**直接相关的工作**

- **Soft Thinking**: 该方法把推理状态构造为词嵌入的概率加权混合，并将连续表示反馈到下一步模型计算中，是本文所分析的混合状态机制的直接代表。本文进一步研究这种表示为何在预训练模型中不能稳定保持。
- **Coconut**: 该方法直接把模型最后的隐状态作为下一步输入嵌入，代表不依赖显式离散中间词的连续推理路线。它说明连续推理不局限于词嵌入混合，但本文的核心分析集中在混合状态的几何失真、softmax读出与自回归反馈。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

连续状态推理希望同时保留并传播多个候选推理轨迹，从而减少离散中间词造成的信息丢失，并可能用较少计算表示多条推理路径。然而，预训练模型中的混合状态经常在连续回馈后失效：要么最高概率分量形成贪心反馈并压制其他路径，要么模型根本不利用连续状态。这使连续推理所承诺的并行探索与压缩优势缺乏可靠基础。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于词嵌入混合的训练无关连续推理**：Soft Thinking 将词表分布中的各词嵌入按概率加权求和，形成连续状态 $e(p)=\sum_i p_i e_i$，再把该状态作为下一推理步的输入；Mixture of Inputs 也保留原本会被采样丢弃的分布信息，并反馈与采样词及其来源分布有关的贝叶斯后验。
- **基于隐状态的学习式连续推理**：Coconut 直接把模型上一时刻的最后隐状态作为下一步输入嵌入；CODI 则通过蒸馏显式链式思维，把离散推理过程压缩到连续隐状态链中。两者都试图绕过必须生成可读中间词的离散瓶颈。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 已有实证研究发现，Soft Thinking 的解码容易被最高概率分量主导，形成不断强化当前优势分量的反馈回路，因而不能稳定保留备选推理路径。
- 训练无关或微调式潜在推理中，连续状态可能坍缩或被模型忽略；只有从头使用潜在思维训练的模型才显示出部分连续状态迹象。现有观察说明现象存在，却未区分失败究竟由架构、训练还是反馈动力学造成，也因此不能明确应在何处干预。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前工作主要报告连续状态“坍缩”或“未被使用”的现象，但缺少一个因果层次清晰的解释：尚不清楚未训练的 Transformer 是否已会破坏混合、预训练额外增加了多少失真，以及在排除表示传输误差后，软最大值读出和自回归反馈是否仍足以导致失败。对于多于两个分量的情形，精确保留需要何种校正、校正复杂度如何随 $K$ 增长，也没有得到一般性刻画。

</div>
<div markdown="1"><span>核心问题</span>

连续混合状态在语言模型的逐步生成中为什么无法被稳定保存；架构、学习所得权重与软最大值—自回归动力学分别扮演什么角色；系统在何种条件下会放大微小差异直至单一分量占优，又在何种条件下会收缩不同混合使其不可辨别；这一结论如何推广到 $K$ 分量？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是逐层剥离可能原因，而不是把所有失真都归因于“模型不适合连续推理”。先用参数规模和结构匹配的随机初始化模型作为控制，可把架构固有失真与训练后新增失真区分开；再假设中间网络能完美线性传输混合，单独研究输出概率和下一步反馈，就能判断坍缩是否是生成机制本身的必然动力学结果。直观上，若两个分量偏好的后续词差异很大，轻微权重优势会在反馈中反复加强；若偏好相近，反馈又会抹平不同初始混合之间的差别。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文采用“表示层探针—理想化动力系统—受控自回归验证—多分量推广”的分析路线，将连续混合坍缩拆成三个彼此独立的来源。首先，把两个或三个词元嵌入按给定权重线性组合并注入提示内部，比较混合输入经过不同网络深度后的位置是否仍等于端点隐藏状态的线性插值；再用同架构随机初始化网络作为控制，以区分架构固有非线性与训练权重造成的额外失真。其次，作者假设Transformer能够完美线性传输混合，只保留线性输出头、softmax和自回归反馈，由此推导混合偏向量的递推式，并证明耦合强度以 $L=2$ 为临界点：超临界时微小多数被放大，亚临界时不同混合被压缩到不可区分。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造并注入连续混合状态

构造 $e(p)=\sum_i p_i e_i$，用这一连续向量替换提示内部的普通词元嵌入；二元实验以权重 $w\in[0,1]$ 插值两个端点，三元实验则扫描三角单纯形中的权重格点。

<div class="method-step__io" markdown="1">

**输入**：若干词元嵌入 $e_i\in\mathbb{R}^d$、位于概率单纯形上的权重 $p$，以及要求模型根据该槽位回答问题的文本上下文。<br>
**输出**：每个请求权重对应的逐层隐藏状态和最终下一词元分布。

</div>

**直观理解**：这相当于把多个候选词压成一个“混合词”放进句子，再检查模型是否仍把它理解成按原比例混合的多个可能性。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 测量表示几何的保持程度

将 $h(w)-h(0)$ 投影到端点方向 $h(1)-h(0)$，得到恢复权重 $\alpha(w)$；再以请求权重与恢复权重的平均绝对偏差构造CALIB，其中精确线性保持得分为 $1$，在 $w=0.5$ 处硬切换到某一端点得分为 $0$。

<div class="method-step__io" markdown="1">

**输入**：混合输入产生的隐藏状态 $h(w)$，以及两个纯端点产生的隐藏状态 $h(0)$ 和 $h(1)$。<br>
**输出**：各网络深度的 $\alpha(w)$ 曲线和CALIB分数，用于判断混合是否逐层变成阶跃式、近乎纯端点的表示。

</div>

**直观理解**：若混合比例是七三，理想情况下隐藏状态也应落在两个端点连线的七三位置；投影和CALIB就是检查模型把这个点推偏了多少。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 用匹配的未训练网络分离架构效应与训练效应

对训练模型和随机控制执行完全相同的混合注入与逐层测量；随机控制保留深度、注意力、归一化和非线性模块，但去掉学习所得参数的影响。

<div class="method-step__io" markdown="1">

**输入**：Qwen3.5和Gemma 4系列预训练模型，以及每个模型对应的五个同架构随机初始化网络。<br>
**输出**：架构本身造成的基准失真，以及预训练在此基础上增加的失真，可通过逐层及最终层CALIB差异加以比较。

</div>

**直观理解**：随机网络像一组“只有机器结构、没有学习经验”的对照组；若训练模型坍缩明显更强，就不能把全部问题归因于Transformer结构本身。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 隔离递归softmax并执行二分量动力学滚动

分别运行 $M(c_t\Vert A_t)$ 和 $M(c_t\Vert B_t)$，用各自贪心预测更新端点，再仅在线性logit空间按 $w_t$ 插值并经过softmax；将混合分布赋给两个新端点的条件概率重新归一化，作为 $w_{t+1}$，同时逐步重测耦合 $L_t$ 和场 $b_t$。

<div class="method-step__io" markdown="1">

**输入**：上下文 $c_t$、两个当前纯分支词元 $A_t$ 与 $B_t$、混合权重 $w_t$，以及模型在两个纯分支上的输出logits。<br>
**输出**：长度为 $50$ 步的权重轨迹 $w_t$、中心化轨迹 $u_t=2w_t-1$，以及随上下文变化的 $L_t$ 和 $b_t$。

</div>

**直观理解**：这里故意不让混合向量经过Transformer内部，只混合两个纯分支的最终logits，因此一旦仍发生坍缩，原因就可定位到softmax和“把输出再喂回模型”的反馈环。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 二分量递归softmax动力学

$$
u_{t+1}=\tanh\!\left(\frac{b_t+L_tu_t}{2}\right)
$$

**符号说明**

- $u_t$：第 $t$ 步中心化后的混合偏向，定义为 $u_t=2w_t-1$；$-1$、$0$、$1$ 分别对应纯 $B$、均衡混合和纯 $A$。
- $w_t$：第 $t$ 步分配给分量 $A$ 的概率权重，取值位于 $[0,1]$。
- $L_t$：第 $t$ 步耦合，$L_t=(\Delta_{A,t}-\Delta_{B,t})/2$，表示两个纯分支对候选 $A$ 与 $B$ 的相对排序差异。
- $b_t$：第 $t$ 步外场，$b_t=(\Delta_{A,t}+\Delta_{B,t})/2$，表示两个分支log-odds中的共同偏置。
- $\Delta_{A,t}$：纯分支 $A$ 的log-odds，定义为 $\log(q_t^A(A)/q_t^A(B))$。
- $\Delta_{B,t}$：纯分支 $B$ 的log-odds，定义为 $\log(q_t^B(A)/q_t^B(B))$。
- $t$：自回归滚动的时间步索引。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把线性logit插值、softmax和反馈合并成一个递推映射。忽略共同偏置并令耦合固定时，均衡状态在 $L<2$ 时稳定，所有初始差异被收缩；在 $L>2$ 时不稳定，任意微小多数都会向同号的极化固定点发展，因此阈值两侧分别对应“洗掉差异”和“赢家通吃”两种信息损失。<br>
**原文位置**：式(7)，第3.1节；临界稳定性分析见第3.2节及式(8)至式(10)

</div>

</div>

<div class="equation-block" markdown="1">

#### 多分量校正所需上下文维数下界

$$
m\geq\operatorname{rank}D_x\Phi\!\left(x_0,f(\bar a,r(x_0))\right);\qquad \operatorname{rank}D_x\Phi=K-1\ \Longrightarrow\ m\geq K-1
$$

**符号说明**

- $m$：提供给校正器的上下文相关表示 $r(x)$ 的维数。
- $D_x\Phi$：一步混合传播映射 $\Phi$ 关于连续上下文表示 $x$ 的雅可比矩阵，描述局部上下文变化会沿多少个独立方向改变输出混合。
- $\Phi$：模型在给定上下文和混合状态下的一步传播映射，使 $a_{t+1}=\Phi(x_t,a_t)$。
- $x_0$：分析局部校正条件时选定的参考上下文表示。
- $f$：在模型传播前调整混合坐标的校正函数。
- $\bar a$：要求在参考上下文附近保持不变的一个内部目标混合状态。
- $r$：从上下文表示中提取供校正器使用的信息映射，满足 $r(x)\in\mathbb{R}^m$。
- $K$：混合中的分量数；其独立比例自由度为 $K-1$。
- $\operatorname{rank}$：矩阵的秩，即局部上下文扰动能够独立影响输出混合的方向数。

<div class="equation-explanation" markdown="1">

**直观理解**：若上下文的小变化能够沿许多独立方向改变模型输出，校正器就必须获得至少同样多维的上下文信息，否则无法同时抵消这些变化。特别地，当上下文影响覆盖全部 $K-1$ 个混合方向时，精确局部保持至少需要 $K-1$ 维上下文条件信号，这排除了单个全局温度作为一般解法。<br>
**原文位置**：定理3，式(18)与式(19)，第5节

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文不是提出并训练一个新语言模型或校正器，而是对既有预训练模型进行表示探针、随机初始化对照、理论推导和受控滚动实验；文中的 $f$ 与 $r$ 是用于证明校正复杂度下界的一般函数，并未给出需要优化的具体损失函数，也未实际训练该校正器。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 隐藏状态几何探针与CALIB**

二元混合的恢复权重定义为 $\alpha(w)=\langle h(w)-h(0),h(1)-h(0)\rangle/\lVert h(1)-h(0)\rVert^2$，即混合隐藏状态在两个端点连线方向上的坐标。CALIB对 $|\alpha(w)-w|$ 求平均并经常数 $Z$ 归一化，以便把精确保持和硬阈值坍缩分别标定为 $1$ 与 $0$。

> 直观理解：该探针不要求隐藏状态完全位于端点连线上，而只读取与混合比例直接相关的轴向位置，因此适合判断模型是否保留了“多少属于每个端点”这一核心信息。CALIB越低，说明请求的连续比例越容易被改写成接近离散选择的表示。

**2. 线性logit传输下的递归softmax系统**

即使最终隐藏状态和输出头都线性，$z(w)=wz_A+(1-w)z_B$ 经softmax后也产生几何概率混合 $q_w(y)\propto q_A(y)^wq_B(y)^{1-w}$，而不是所期望的算术混合 $wq_A+(1-w)q_B$。作者以两个分支对候选 $A,B$ 的log-odds构造耦合 $L_t$ 和场 $b_t$，将反馈压缩为一维非自治递推；其中 $L_t$ 衡量两分支对后继的相对偏好差异，$b_t$ 表示二者共有的偏向。

> 直观理解：线性混合logits并不等于线性混合概率，softmax会改变比例；当改变后的比例被连续反馈时，小偏差会重复累积。耦合量描述两个分支是否在“各自支持不同后继”：差异越强，当前多数越容易在下一步得到额外优势。

**3. 上下文条件的多分量校正器**

对 $K$ 分量权重 $p$，作者采用 $a_i=\log(p_i/p_K)$ 的 $K-1$ 维无约束坐标，并把模型的一步传播表示为 $\Phi(x_t,a_t)$。候选校正器先根据上下文摘要 $r(x_t)\in\mathbb{R}^m$ 把目标状态改写为 $\widetilde a_t=f(a_t,r(x_t))$，再要求 $\Phi(x_t,\widetilde a_t)=a_t$；链式法则给出所需上下文信息维数的秩下界。

> 直观理解：同一混合比例在不同句子里可能受到不同方向、不同强度的扭曲，所以固定温度或固定重加权通常无法普遍抵消误差。若上下文能沿 $K-1$ 个独立比例方向改变输出，校正器就至少要接收同样多的独立上下文信号。

**训练与推理**

训练方面，作者不修改预训练模型参数；为建立控制组，每种架构生成五个随机初始化实例，而非用任务数据训练这些实例。表示探针阶段在提示内部注入连续嵌入，分别记录纯端点和混合输入的逐层隐藏状态，再计算恢复权重与CALIB。递归softmax阶段仅让两个纯分支正常经过模型：每一步对两个分支分别前向计算并贪心选取下一端点，将端点logits按当前权重线性插值，经过softmax后只在两个新端点上重新归一化概率以更新权重，并更新上下文继续滚动。阈值实验不改变模型或分支轨迹，而是用温度 $\tau$ 将已测耦合改为 $L_t/\tau$，从两个对称初态重放递推，以检验收缩—放大转变是否出现在理论阈值附近。

**复现信息**

公平解释结果所需的关键信息包括：表示保持实验使用附录A所述的同一套 $1000$ 项基准；三元可视化扫描包含 $325$ 个单纯形格点。随机控制与对应预训练模型具有完全相同的架构，每个未训练结果取五次随机初始化的均值并报告标准差。主要模型族为Qwen3.5和Gemma 4，深度分析重点展示Qwen3.5-4B与Gemma-4-E4B-it，并在更广的八模型规模梯度上比较最终层CALIB。递归实验对每项滚动 $50$ 步，图中轨迹及耦合统计使用项目中位数；这种汇总反映典型行为，但不会展示项目间分布的全部尾部差异。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 连续混合物基准：共 $1000$ 个二元混合项目，覆盖颜色、温度、大小、速度、硬度、重量和亮度七类语义属性。每个项目包含一个带注入槽的提示词、两个组件词和两个对应答案词；在混合权重 $p$ 下，将注入向量设为 $e(p)=p e_1+(1-p)e_2$。该基准用于测试模型在下一词位置对连续嵌入混合的答案概率是否随混合权重保持合理变化。原文未报告独立训练集、验证集或测试集划分；该基准整体用于评估。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**两个答案词的相对下一词概率**

测量模型在答案位置为两个候选答案分配的概率相对关系，并考察该关系如何随混合权重 $p$ 变化。 （原文未明确给出统一的高低方向或汇总评分；若用于检验混合保真度，则应关注概率关系是否与两个端点及混合权重保持一致，而不是简单追求概率越高越好。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验章节仅包含基准构造与代表性项目，未提供主结果、消融结果、数值表格或图表，因此不能支持关于模型性能、训练影响或理论预测的定量结论。
- 项目要求组件词和答案词在两个模型族中均为单词元，并要求端点答案概率至少为 $0.5$；这提高了评测可比性和题目有效性，但可能限制基准对复杂分词、困难问题及端点本身不可靠情形的覆盖。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 随机初始化控制模型：与训练模型匹配，用于判断观察到的混合行为是否来自预训练，而不是仅来自模型架构或随机参数。
- 混合物的两个端点 $p=1$ 和 $p=0$：分别对应两个真实组件词，是评估中间混合状态的参照，而非独立模型基线。

**实验想回答的问题**

- 所构造的混合物评测是否能够在统一的下一词预测任务中检验模型对连续嵌入混合的保真度？
- 不同模型族及其训练模型与随机初始化控制模型是否可以在同一批经过端点质量筛选的项目上进行可比评估？

**实验实现**

每个项目只保留满足以下条件的样本：两个组件词和两个答案词在两个模型族的分词器下均为单个词元；并且训练模型在两个端点处对相应答案词至少分配 $0.5$ 的概率。随后跨模型族取交集，形成供所有训练模型及其匹配随机初始化控制模型共同使用的 $1000$ 项基准。提示采用聊天模板，并在答案位置前关闭推理块，使下一词概率集中于要求的一词答案。注入槽填入的是两个组件嵌入的凸组合，而不是真实词元。原文未明确报告模型族名称、模型规模、采样次数、随机种子、具体概率汇总方式或统计显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 表 $2$ 给出十个代表性项目，按七个语义类别先各出现一次，再进行第二轮排列。例如，`sun / pit` 对应 `bright / dark`，`granite / cotton` 对应 `hard / soft`。这些例子说明基准覆盖的是简单、可解释的二元属性；它们是项目示例而非定性结果，原文未报告单个案例的模型输出或错误模式。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：从理论和实验上分析语言模型连续潜状态推理中混合表示坍缩的内部动力学机制。; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`3931099d71950d093d8da49c1850da047b4b2e7a32a7b2539f0d05caba1b1412`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
