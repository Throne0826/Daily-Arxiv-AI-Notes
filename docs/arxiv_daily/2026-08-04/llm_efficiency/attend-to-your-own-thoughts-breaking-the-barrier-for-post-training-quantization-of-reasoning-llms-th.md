---
title: "[论文解读] Attend to Your Own Thoughts: Breaking the Barrier for Post-Training Quantization of Reasoning LLMs through the Lens of 1.58-Bit Quantization"
description: "[arXiv 2608.01078][LLM 效率] 本文将推理模型自身生成的思维链与答案用于量化校准，以弥补常规语料缺少显式推理模式的问题，从而探索无需重新训练、可扩展到不同架构和规模的三值推理大模型构建方法。"
arxiv_id: "2608.01078"
announcement_date: "2026-08-04"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:58:21.345244+00:00"
source_sha256: "939d4aa7b1a95a7fd6dc22952c4250acbafd1de28f676d4edf97f1163d0935c0"
tags:
  - "LLM 效率"
  - "LLM Reasoning"
  - "大语言模型"
  - "训练后量化"
  - "三值量化"
  - "1.58-bit 量化"
  - "思维链"
  - "校准数据"
  - "推理模型"
  - "可微量化"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2608.01078</p>

# Attend to Your Own Thoughts: Breaking the Barrier for Post-Training Quantization of Reasoning LLMs through the Lens of 1.58-Bit Quantization

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Shigeng Wang, Chao Li, Yangyuxuan Kang, Jiawei Fan, Anbang Yao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01078v1) · [PDF 下载](https://arxiv.org/pdf/2608.01078v1) · **关键词** 大语言模型, 训练后量化, 三值量化, 1.58-bit 量化, 思维链, 校准数据, 推理模型, 可微量化<br>
**代码**: [https://github.com/IntelChina-AI/BitTern](https://github.com/IntelChina-AI/BitTern) · **项目页**: [https://github.com/IntelChina-AI/BitTern](https://github.com/IntelChina-AI/BitTern)

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

本文将推理模型自身生成的思维链与答案用于量化校准，以弥补常规语料缺少显式推理模式的问题，从而探索无需重新训练、可扩展到不同架构和规模的三值推理大模型构建方法。

**不用术语来说**：推理大模型虽然能解决数学和编程问题，但保存和运行成本很高；把模型权重压缩为三种取值可以大幅降低成本，却也容易破坏模型逐步推理所依赖的信息。现有压缩方法通常用普通网页文本来判断压缩前后模型是否一致，这些文本很少展示完整的解题步骤，因此校准过程可能保住一般语言能力，却无法保住复杂推理能力。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者通过数学与代码任务上的经验研究，将可微三值量化后性能崩溃的关键原因定位为校准方案：常规网页语料与目标推理行为不匹配，且三值表示的信息容量过低，难以容忍这种校准偏差。
- 作者提出 AYOT，让待量化的高精度目标模型针对校准问题自行生成推理轨迹和最终答案，再将问题、轨迹与答案共同用于 CAT-Q 的量化校准，形成面向推理大模型的 ScaleQ-1.58 框架。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大语言模型依靠思维链推理处理数学、代码等需要多步逻辑的任务，但高精度模型的权重存储与矩阵计算成本较高，因而难以部署到资源受限平台。训练后量化是在不重新进行完整预训练的前提下降低模型数值精度；本文关注其中最激进的三值量化，即用集合 $\{-1,0,1\}$ 中的值近似原始高精度权重，使每个权重平均只需约 $\log_2 3\approx1.58$ bit，并将大量浮点乘法转化为更低成本的加减运算。已有训练后量化主要研究 8-bit 或 4-bit 模型以及常识、基础语言生成任务，而本文研究能否仅用少量校准数据，将已经具备思维链能力的高精度推理模型直接转换为可完成复杂数学与代码任务的 1.58-bit 模型。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**训练后量化（Post-Training Quantization, PTQ）**

在模型完成预训练后压缩其权重或激活，通常借助少量校准样本估计量化参数，无需从头训练模型。本文采用逐层或逐块重构语境下的 PTQ，目标是让量化模块的输出尽量接近高精度模块。

</div>
<div class="concept-item" markdown="1">

**三值量化（Ternary Quantization）**

用缩放后的三值权重 $\alpha T$ 近似高精度权重 $W$，其中 $T_i\in\{-1,0,1\}$，因此也称 1.58-bit 量化。其压缩和推理加速潜力很高，但相较 8-bit 或 4-bit 量化会损失更多信息，更容易破坏复杂推理能力。

</div>
<div class="concept-item" markdown="1">

**思维链与校准数据（Chain-of-Thought and Calibration Data）**

思维链是模型从问题到答案之间生成的一系列中间推理步骤；校准数据则用于观测模型内部输出分布并确定量化方式。本文的关键背景假设是：通用网页文本主要呈现局部词语关系，而目标模型自己生成的推理轨迹更能代表数学和代码任务实际需要保留的计算模式。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个已经过预训练、具有思维链推理能力的高精度目标大语言模型，以及规模远小于原始训练语料的校准问题集合，任务是在 PTQ 设置下把线性层高精度权重 $W$ 近似为 $\alpha T$，其中三值矩阵 $T$ 的元素由阈值 $\Delta$ 映射到 $\{-1,0,1\}$。输入包括目标模型、校准问题以及可作为校准上下文的文本；输出是保持原模型架构但权重被三值化的 1.58-bit 推理模型。本文考察的设置覆盖稠密模型和混合专家模型、$1.7$B 至 $235$B 参数规模，以及数学、代码等复杂推理任务；其基本约束是不进行从头量化感知预训练，而是通过少量校准数据学习分组缩放因子和权重阈值。传统校准通常从 C4、WikiText2 等通用网页语料抽样，并隐含量化方法对校准数据变化较稳健的假设；本文指出该假设在信息损失更严重的三值量化中可能不成立，尤其无法充分覆盖推理模型运行时产生的多步逻辑模式。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$W$**

线性层的高精度权重矩阵。

</div>
<div class="notation-item" markdown="1">

**$T$**

与 $W$ 对应的三值权重矩阵，其元素属于 $\{-1,0,1\}$。

</div>
<div class="notation-item" markdown="1">

**$\alpha$**

用于恢复三值权重量级的缩放因子；CAT-Q 按权重组学习该参数。

</div>
<div class="notation-item" markdown="1">

**$\Delta$**

决定高精度权重映射为 $-1$、$0$ 或 $1$ 的阈值；CAT-Q 按权重组学习该参数。

</div>

</div>

**直接相关的工作**

- **BitNet b1.58 2B4T**: 此前面向复杂推理的代表性 1.58-bit 模型，拥有 20 亿参数，并通过包含文本、数学、代码和对话数据的 4 万亿 token 从头训练，再经历监督微调和直接偏好优化。它说明三值模型可以获得推理能力，但训练流程昂贵且复杂，难以直接扩展到更大模型；本文将其作为量化感知训练路线的关键参照。
- **CAT-Q**: 首个可微三值化方法，使用软三值化函数为预训练模型学习分组缩放因子与权重阈值，并已展示扩展到百亿乃至千亿级参数的潜力。本文以 CAT-Q 为直接技术基础，但关注其此前未充分验证的数学和代码推理场景，并研究校准内容是否是其在复杂任务上发生性能崩溃的关键因素。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

数学、代码等复杂任务依赖大模型的思维链推理能力，但高精度模型具有较大的显存占用和计算开销，难以部署到资源受限的平台。三值量化把权重限制为集合 $\{1,0,-1\}$，可用较低成本的整数加减替代大量浮点乘法，但极端压缩也更容易造成信息丢失，因此需要一种成本明显低于从头训练、同时能够保存复杂推理能力的量化途径。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于量化感知训练或知识蒸馏的三值模型**：这类方法在训练或微调期间模拟三值化，并通过量化感知训练或教师模型监督来适应离散权重。BitNet b1.58、TriLM 和 Tequila 等模型采用这一思路；BitNet b1.58 2B4T 还通过大规模预训练、监督微调和偏好优化获得复杂推理能力。
- **基于校准重构的训练后量化与 CAT-Q**：训练后量化不重新进行完整预训练，而是从 C4、WikiText2 等语料抽取少量校准数据，逐层或逐块重构高精度模型的输出分布。CAT-Q 进一步采用可微的软三值化，学习分组缩放因子与权重阈值，使三值量化能够扩展到更大的预训练模型。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 量化感知训练和从头训练能够缓解三值化损失，但需要海量训练词元、GPU 集群以及复杂的训练流程；资源需求还会随模型规模和架构复杂度增长，因此既有三值模型主要局限于较小的稠密架构，难以经济地扩展到超大模型或混合专家模型。
- 常规训练后量化默认不同校准语料之间的差异不会显著影响结果，这一假设在 8 位或 4 位量化下可能尚可接受，却不适合信息损失更严重的 1.58 位三值量化。网页文本主要体现局部词语关系，缺少数学和代码解题所需的显式中间逻辑；因此即使 CAT-Q 能学习量化参数，用此类语料校准仍可能使复杂推理性能崩溃。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未提供一种可扩展的三值训练后量化方法，能够在不进行昂贵从头训练的条件下，为不同规模、稠密或混合专家架构的预训练推理模型保留数学与编程等复杂推理能力。更具体地说，已有方法改善了三值参数的优化方式，却没有解决校准上下文与目标模型实际推理过程不一致的问题。

</div>
<div markdown="1"><span>核心问题</span>

在训练后量化场景中，三值量化能否跨越复杂推理任务、不同模型架构和更大参数规模而保持有效；若常规方法不能做到，性能瓶颈是否来自校准方案，以及把目标模型自身的推理轨迹纳入校准能否突破该瓶颈？

</div>
<div markdown="1"><span>作者直觉</span>

量化校准相当于告诉低精度模型哪些行为必须在压缩后尽量保持。普通网页文本只让模型复现一般续写行为，而数学和代码任务真正依赖的是从问题到中间推理步骤、再到最终答案的完整计算路径。AYOT 让高精度目标模型先对合适的校准问题生成自己的思维链和答案，再用这些内容校准三值模型；这样校准信号更接近该模型实际解决推理任务时的内部工作分布，有限的三值表示能力便可优先用于保留关键推理模式。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ScaleQ-1.58 是一个面向推理大语言模型的三值后训练量化框架，目标是在不重新训练或微调模型的条件下，将高精度权重压缩为近似 1.58-bit 的三值权重，同时尽量保留思维链推理能力。其完整流程是：先从数学与代码领域数据中抽取问题，让待量化的高精度目标模型亲自生成推理轨迹和最终答案；再把“问题、推理轨迹、答案”组成校准上下文；最后用 CAT-Q 的可微软三值化和跨层输出重构优化量化参数，并将软权重固化为取值属于 $\{-1,0,1\}$ 的三值权重。ScaleQ-1.58 本身并未提出新的三值化算子，而是将新的校准策略 AYOT 与已有 CAT-Q 量化算法结合。

关键设计是让校准输入覆盖模型实际执行复杂推理时产生的中间状态。普通网页文本主要提供一般语言共现关系，简单的领域问答对虽包含数学或代码知识，却没有呈现目标模型逐步求解时的激活模式；使用更强但架构和规模不同的外部模型生成思维链，也可能与待量化模型自身的计算路径不匹配。AYOT 因而使用目标模型自己的推理轨迹，相当于在压缩模型前先记录它“思考时内部各层如何响应”，再要求量化模型在这些代表性输入上复现高精度模型的跨层输出。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建领域相关的问题集合

默认从 MetaMathQA 和 OpenCodeInstruct 各随机抽取 1024 个样本，并确认校准样本不与相应测试集重叠。任务特定设置通过替换部分默认数学或代码样本，引入与目标任务更接近的训练数据。

<div class="method-step__io" markdown="1">

**输入**：数学领域的 MetaMathQA 与代码领域的 OpenCodeInstruct；任务特定实验还可加入 GSM8K、MBPP 或 ProofWriter 的训练样本。<br>
**输出**：由 2048 个领域问题组成、覆盖约 4M token 校准预算的问题集合。

</div>

**直观理解**：量化时看到的数据决定模型要优先保住哪些行为；因此数学和代码模型不能只用随机网页段落校准。该步骤先保证校准问题与测试领域相关，同时避免直接用测试样本造成数据泄漏。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成目标模型自身的思维链

将每个问题输入目标模型，由该模型生成逐步推理轨迹和最终答案，再组成“问题、推理轨迹、生成答案”三元组。这里的生成器必须是待量化目标模型本身，而不是 DeepSeek-R1-671B 等外部强模型。

<div class="method-step__io" markdown="1">

**输入**：领域问题集合与尚未量化的高精度目标大语言模型。<br>
**输出**：CoT-aware、self-generated 的 AYOT 校准语料。

</div>

**直观理解**：不同模型即使回答同一道题，也可能采用不同的中间计算路径。让模型展示自己的解题过程，可以使后续量化直接保护该模型真正使用的推理模式，而不是模仿另一个模型的思考方式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行可微软三值化与跨层重构

先用 $\hat{\mathbf{W}}=(\mathbf{W}-\mu)/\alpha$ 重分布权重，再随归一化校准时间 $t$ 增大，通过软三值函数把连续权重平滑推向 $[-1,1]$ 内的三个离散状态。优化采用滑动窗口上的跨层输出重构，使量化窗口的输出逼近原高精度模型在同一 AYOT 上下文中的输出。

<div class="method-step__io" markdown="1">

**输入**：高精度权重 $\mathbf{W}$、AYOT 校准上下文，以及 CAT-Q 的可学习重分布参数 $\mu$、$\alpha$ 和三值阈值 $\Delta$。<br>
**输出**：经过校准的三值表示、缩放因子及其他量化参数。

</div>

**直观理解**：直接把连续权重四舍五入成三个值会产生不可导的突变，有限校准数据很难补救。CAT-Q 先把硬切换变成逐渐收紧的软过程，并一次对一段相邻层校准，从而保护跨层传播后的整体行为。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 固化三值模型并执行推理

将权重重构为 $\mathbf{W}\approx\alpha\mathbf{T}$，其中 $\mathbf{T}$ 为三值张量，并丢弃仅用于重分布的均值 $\mu$。对 MoE 模型保留路由器层的全精度表示，其余模块进行三值量化。

<div class="method-step__io" markdown="1">

**输入**：校准完成的软三值权重、学习到的尺度 $\alpha$，以及原模型结构。<br>
**输出**：权重格式为 W1.58A16 的推理模型，即权重采用约 1.58-bit 三值表示而激活保持 16-bit。

</div>

**直观理解**：最终部署时只需保存三个可能的权重状态及对应尺度，不再保留校准阶段的软函数和均值偏移。MoE 路由器决定每个 token 被送往哪些专家，错误路由影响较大，因此作者没有量化该部分。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### CAT-Q 可微软三值化函数

$$
T_i=f(\hat{W}_i;s,t,\Delta)=\frac{\tanh\!\left(ts(\hat{W}_i-\Delta)\right)+\tanh\!\left(ts(\hat{W}_i+\Delta)\right)}{2\tanh(ts)}
$$

**符号说明**

- $T_i$：第 $i$ 个权重对应的软三值化输出；校准后趋向负值、零或正值三个状态。
- $\hat{W}_i$：重分布权重 $\hat{\mathbf{W}}$ 的第 $i$ 个元素，由原权重经均值平移和尺度缩放得到。
- $f(\cdot)$：随校准进程逐渐从近似连续映射转为三值映射的可微函数。
- $s$：固定的锐度因子，控制双曲正切曲线向离散阶跃过渡的陡峭程度。
- $t$：归一化到 $[0,1]$ 的当前校准时间步；其增大使输出逐渐被限制到三值形态。
- $\Delta$：权重阈值，决定映射到零值区域的宽度。

<div class="equation-explanation" markdown="1">

**直观理解**：两个平移后的双曲正切项共同形成三个区域：较小的负权重趋向负状态，中间权重趋向零，较大的正权重趋向正状态。分母用于规范输出曲线；随着 $t$ 增大，映射越来越接近硬三值化，但在校准过程中仍保持可微，因此可以通过输出重构误差更新量化参数。<br>
**原文位置**：第 2.1 节，公式 (2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 权重重分布与最终三值重构

$$
\hat{\mathbf{W}}=\frac{\mathbf{W}-\mu}{\alpha},\qquad \mathbf{W}\approx\alpha\mathbf{T},\qquad \mathbf{T}\in\{-1,0,1\}^{\operatorname{shape}(\mathbf{W})}
$$

**符号说明**

- $\mathbf{W}$：待量化层的原始高精度权重张量。
- $\hat{\mathbf{W}}$：供软三值化函数处理的重分布权重张量。
- $\mu$：可学习权重均值，仅在校准时调整权重分布，最终权重重构时被丢弃。
- $\alpha$：可学习缩放因子；最终把无量纲三值张量映射回原权重的数值尺度。
- $\mathbf{T}$：与 $\mathbf{W}$ 形状相同、元素属于 $\{-1,0,1\}$ 的最终三值张量。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分先将权重居中并缩放，使三值阈值更容易把权重合理分组；第二部分是实际部署格式，只用尺度 $\alpha$ 乘三值张量 $\mathbf{T}$ 近似原权重。因为最终不加入 $\mu$，模型仍保持 TWN 式硬件友好三值表示，而 $\mu$ 只是优化过程中的辅助变量。<br>
**原文位置**：第 2.1 节的权重重分布定义；附录 C.2 的三值重构公式

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：ScaleQ-1.58 属于后训练量化，不进行预训练、监督微调或参数高效微调；其优化对象是量化相关参数，而不是用新任务标签继续训练全部模型参数。AYOT 三元组被送入高精度参考模型和当前软三值模型，CAT-Q 通过滑动窗口跨层输出重构，使量化窗口输出逼近参考输出，并在校准时间 $t$ 从 $0$ 向 $1$ 推进时逐渐强化三值约束。原文节选没有给出重构损失的明确数学形式、各损失项权重或具体优化器，因此不能进一步断言其采用均方误差、KL 散度或其他目标；能够确定的是，AYOT 改变了重构所依据的输入分布，而 CAT-Q 负责可微量化参数优化。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. AYOT 自生成思维链校准**

AYOT 遵循两个原则：校准问题来自目标领域，并由待量化的高精度目标模型为每个问题生成推理轨迹和最终答案。生成后的 $[\text{question},\text{reasoning traces},\text{generated answer}]$ 序列整体作为量化重构的上下文，而不是只输入普通网页文本或 $[\text{question},\text{answer}]$ 对。

> 直观理解：AYOT 不改变模型结构或三值编码，而是改变校准算法所观察的数据。其作用类似于在压缩一套解题程序前，不仅记录输入和最终输出，还记录这套程序自己产生的完整执行过程。

**2. CAT-Q 软三值化与权重重分布**

CAT-Q 用可学习均值 $\mu$ 和尺度 $\alpha$ 将原权重变换为 $\hat{\mathbf{W}}=(\mathbf{W}-\mu)/\alpha$，再通过由时间 $t$ 控制的双曲正切函数逐步逼近三值映射。$\mu$ 只帮助校准阶段重新排列权重相对阈值的位置，最终重构不包含该均值，以保持标准三值权重格式。

> 直观理解：权重重分布先把连续权重调整到更容易分成负、零、正三组的位置；软三值化则让这一分组逐渐发生，使梯度优化仍可工作。最终移除均值，是为了不让部署格式额外承担一个不符合标准三值计算的偏移项。

**3. 滑动窗口跨层输出重构**

ScaleQ-1.58 沿用 CAT-Q 的跨层输出重构：以滑动窗口包含若干相邻层，在 AYOT 校准序列上联合调整窗口内量化参数，使窗口末端输出接近对应高精度网络输出。原文节选未给出该重构损失的显式公式，也未说明窗口宽度。

> 直观理解：逐层单独拟合可能让每层的小误差在深层网络中累积；窗口重构直接观察多层组合后的结果，因此能让相邻层彼此补偿。它保护的是一段计算链的整体输出，而不只是每一层孤立的权重数值。

**训练与推理**

校准前保留一份高精度目标模型，并从 MetaMathQA 与 OpenCodeInstruct 抽取领域问题。先由该目标模型以常规自回归方式生成自己的思维链和答案，将完整三元组截断或填充到固定长度；随后按组处理模型权重，在 AYOT 序列上运行高精度模型与软三值模型，使用 CAT-Q 的滑动窗口跨层重构学习 $\mu$、$\alpha$、$\Delta$ 等量化参数，并通过时间变量 $t$ 将连续代理逐步收紧为三值表示。该过程只需要有限校准数据，不更新模型以学习新的问答知识。

校准结束后，将每个权重组固化为 $\alpha\mathbf{T}$ 并删除辅助均值 $\mu$；推理时不再需要 AYOT 数据、思维链生成器或软三值函数。部署模型按原有自回归流程接收用户问题并生成推理过程与答案，只是大部分矩阵权重已替换为三值表示；激活仍为 16-bit。对于 MoE 架构，专家及其他非路由模块被量化，而负责专家选择的路由器保持全精度。

**复现信息**

默认校准集含 2048 个样本，每个样本截断或填充到 2048 token，其中 MetaMathQA 与 OpenCodeInstruct 各 1024 个，对应约 4M 校准 token。默认校准运行 60 个 epoch，batch size 为 3；除 AYOT 数据构造外，其余超参数沿用 CAT-Q。权重采用 group-wise 量化，固定组大小为 $g=128$；最终格式为 W1.58A16。对 MoE 模型，路由器层维持全精度，其余模块量化。

任务特定校准实验中，作者分别用 GSM8K 训练集样本替换八分之一数学样本，用 MBPP 训练集样本替换八分之一代码样本；MBPP 训练样本与 MBPP+ 测试集不重叠。加入 ProofWriter 时，也分别替换八分之一数学样本和八分之一代码样本。原文节选未明确报告生成思维链时的解码温度、采样策略、最大生成长度、跨层窗口宽度、优化器、学习率、校准硬件与运行时间，这些因素仍需结合代码或完整论文核查后才能完全复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 数学与代码评测套件：MATH-500包含500道竞赛级数学题；GSM8K包含8792道小学数学文字题，其中7473道训练题、1319道测试题；Omni-MATH包含4428道奥赛级题目。代码侧采用HumanEval+的164道函数生成题和约378道MBPP+ Python题。它们分别覆盖基础算术、竞赛数学、困难多步数学、函数正确性和基础编程，用于检验量化后推理能力是否保留。
- 跨领域评测套件：ProofWriter用带真、假或未知标签的合成事实、规则和假设测试多步演绎，并按推理深度报告结果；WikiText2与C4以困惑度测试基础语言建模；PIQA、ARC-e、ARC-c、HellaSwag和Winogrande的平均准确率用于测试物理、科学及一般常识推理。这组数据检验方法是否只对数学和代码有效。
- 校准数据：默认从MetaMathQA和OpenCodeInstruct抽取提示，让待量化的高精度模型自行生成推理轨迹与答案，再将问题、轨迹和答案拼成校准上下文，默认总预算为$4\mathrm{M}$词元。消融还引入WikiText2、C4、GSM8K、MBPP及256条ProofWriter训练样本，以区分通用文本、领域相关数据和目标任务数据的作用。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务准确率**

用于MATH-500、GSM8K、Omni-MATH、ProofWriter及常识选择题，表示最终答案或类别判断正确的样本比例；论文还对若干任务或ProofWriter深度取平均。 （越高越好，因为正确完成推理任务的样本更多。）

</div>
<div class="metric-item" markdown="1">

**代码功能正确率**

HumanEval+和MBPP+通过扩展测试用例判断生成代码是否实现题目要求；摘录将其作为百分数报告，但未进一步明确具体统计名称或采样协议。 （越高越好，因为通过测试用例的代码任务更多。）

</div>
<div class="metric-item" markdown="1">

**困惑度**

在WikiText2和C4上衡量模型对真实文本序列的预测不确定性，论文报告两个数据集的平均困惑度。 （越低越好，因为模型给观测文本分配的概率通常更高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 与既有1.58比特推理模型比较：默认$4\mathrm{M}$校准词元下的三值Qwen3-1.7B和Qwen3-4B，对照使用$4\mathrm{T}$词元的BitNet b1.58 2B4T。

<div class="result-value" markdown="1">

作者报告，三值Qwen3-1.7B在四个数学与代码任务上的平均成绩达到BitNet b1.58 2B4T的90.52%以上，而量化所需词元少$1{,}000{,}000$倍；三值Qwen3-4B相对该基线取得8.97个百分点的绝对增益。

</div>

这说明AYOT结合CAT-Q能以很小的后训练校准预算得到可用的三值推理模型，并且4B版本在作者选定的四任务平均值上超过已有1.58比特模型。不过，这不是严格同构比较：模型规模、基础模型、预训练数据和“从头训练”与“后训练量化”的流程均不同，因而不能把全部差异归因于AYOT。

<div class="result-source" markdown="1">

来源：第3.2节，Scaling across Models and Tasks；相关逐模型结果位于表1，但所给摘录未包含表1数值行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Notably, compared to the best prior 1.58-bit reasoning LLM, BitNet b1.58 2B4T [39], our ternary Qwen3-1.7B achieves competitive performance (over 90.52% of the average score of BitNet b1.58 2B4T on four math/coding tasks) while using 1,000,000× fewer tokens for quantization. Moreover, our ternary Qwen3-4B surpasses BitNet b1.58 2B4T by an absolute 8.97%, highlighting the extreme efficiency of ScaleQ-1.58 in terms of the calibration token count for quantization.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3-4B在$W1.58A16$下将校准预算从$256\mathrm{K}$逐步增加至$16\mathrm{M}$，epoch数和其他超参数保持一致。

<div class="result-value" markdown="1">

五项任务均随预算增加而改善：例如MATH-500从20.90升至66.20，GSM8K从15.84升至70.96，HumanEval+从27.44升至58.45；默认$4\mathrm{M}$时五项结果依次为58.40、61.56、14.93、53.98和39.15。

</div>

一致的上升趋势表明，三值PTQ对校准数据覆盖度高度敏感，$4\mathrm{M}$并非已饱和的最佳预算。由于该实验固定epoch而增加数据量，总数据处理量也随之增加；论文随后用固定迭代次数的消融进一步区分数据多样性和计算量，但这里本身不能单独证明增益完全来自数据多样性。

<div class="result-source" markdown="1">

来源：表2；图4展示准确率随校准词元数变化的趋势

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

W1.58A16 | 256K | 20.90 | 15.84 | 7.90 | 27.44 | 30.95
W1.58A16 | 4M | 58.40 | 61.56 | 14.93 | 53.98 | 39.15
W1.58A16 | 16M | 66.20 | 70.96 | 16.80 | 58.45 | 47.35

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen3-4B三值模型使用不同领域组成的$4\mathrm{M}$词元校准集，并在数学、代码、语言建模、常识和ProofWriter上联合评测。

<div class="result-value" markdown="1">

仅用数学与代码校准时，五项数学/代码成绩为58.40、61.56、14.93、53.98和39.15，但ProofWriter平均仅39.50；加入科学逻辑和任务特定数据后，五项成绩变为59.10、70.36、16.71、54.27和42.06，ProofWriter平均达到83.54。相应语言建模平均困惑度为33.14、常识平均准确率为52.81。

</div>

结果显示校准数据的领域组成会直接塑造量化模型保留哪类能力：数学/代码轨迹并不会自动保住科学演绎能力，而加入对应数据可显著修复目标领域。混合校准因此更适合通用部署，但语言建模困惑度和常识成绩并未随领域增加而单调改善，说明固定预算下存在数据配比权衡，不能据此宣称所有能力同时最优。

<div class="result-source" markdown="1">

来源：表8，四类校准数据均启用的最后一行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

✓ | ✓ | ✓ | ✓ | 59.10 | 70.36 | 16.71 | 54.27 | 42.06 | 33.14 | 52.81 | 83.54

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

- 全精度Qwen3 $W16A16$：给出同一基础模型未量化时的性能上界，用于衡量三值权重量化造成的绝对损失；它不是同等存储或计算成本下的竞争方法。
- BitNet b1.58 2B4T：已有的1.58比特推理模型，使用约$4\mathrm{T}$训练词元；与它比较可判断ScaleQ-1.58能否用后训练量化和远少于从头训练的词元预算获得有竞争力的结果，但二者基础模型与训练过程并不完全相同。
- CAT-Q配合思维链无关校准：分别使用WikiText2、C4或领域数据，是最直接的三值量化校准对照，用来判断性能提升是否来自AYOT的自生成推理上下文，而不只是CAT-Q优化器本身。
- SliderQuant配合C4校准：用于$W2A16$和$W4A16$设置；将其与AYOT+SliderQuant比较，可以把AYOT视为可替换的校准策略，检验其是否超越1.58比特和CAT-Q这一特定组合。

**实验想回答的问题**

- 在默认仅使用$4\mathrm{M}$校准词元的条件下，ScaleQ-1.58能否把不同规模、不同架构的推理大模型压缩到$W1.58A16$，同时在数学、代码和科学逻辑推理任务上避免传统校准导致的性能崩溃？
- ScaleQ-1.58的效果究竟来自校准词元数量、优化迭代次数，还是AYOT所强调的自生成思维链、任务相关数据与长上下文；这些校准原则能否推广到$W2A16$和$W4A16$？

**实验实现**

核心实验覆盖Qwen3稠密模型1.7B、4B、8B、14B和32B，MoE模型Qwen3-30B-A3B与Qwen3-235B-A22B，以及DeepSeek-R1-Distill-Llama-70B。除非另行说明，均采用权重三值、激活16比特的$W1.58A16$设置，默认校准预算为$4\mathrm{M}$词元。主要消融固定在Qwen3-4B上；词元扩展实验保持epoch数和其他超参数一致，迭代次数消融则显式控制优化步数。序列长度比较$2048$与$4096$，其他位宽实验把AYOT接入SliderQuant。摘录未明确报告解码温度、采样次数、随机种子、置信区间及显著性检验，因此表中差异应视为点估计。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 控制优化迭代数，比较校准词元规模与训练步数：Qwen3-4B、$W1.58A16$，分别使用$256\mathrm{K}$或$2\mathrm{M}$词元，并在2560、5120和10240步下评测。 | 作者计算称，在$256\mathrm{K}$词元下把迭代数从2560增至10240，五任务平均准确率提高5.49个百分点；固定为10240步时，把校准数据从$256\mathrm{K}$增至$2\mathrm{M}$，平均提高13.86个百分点。 | 该消融把“看过更多不同词元”与“对同一批数据优化更多次”分开。两者都能提升性能，但固定步数后扩大数据规模的收益更大，支持多样化校准样本覆盖更多推理状态这一解释。它仍未报告多次随机实验，因此不能判断差异的统计稳定性。 | 第3.3节Calibration Set Size vs. Quantization Budget；表3<br><span class="experiment-evidence">For 256K tokens, raising the number of optimization iterations from 2560 to 10240 improves the average accuracy across the five tasks by 5.49%. Yet under the same 10240 optimization iterations, scaling the calibration token count from 256K to 2M tokens produces a much larger gain of 13.86% on average.</span> |
| 固定Qwen3-4B与CAT-Q，比较WikiText2、C4、领域数据、强模型生成思维链，以及待量化模型自行生成思维链的AYOT校准。 | C4校准在五项任务上仅得到0.00、14.48、2.71、0.00和0.00；领域相关但无思维链的校准提高到24.20、28.65、5.04、17.88和11.38；AYOT进一步达到58.40、61.56、14.93、53.98和39.15，并明显超过强模型生成思维链的31.80、30.78、6.98、16.46和14.29。 | 该比较同时检验两条设计原则：校准文本应与目标推理领域匹配，并应来自待量化模型自身。强模型生成的轨迹不如自生成轨迹，说明“答案质量更高”不等于“更适合重现目标模型内部激活分布”。不过，不同生成来源的长度、风格和难度是否完全匹配，摘录没有说明，因此机制解释仍需进一步控制实验。 | 表4<br><span class="experiment-evidence">CoT-agnostic: generic-text (C4) \| 0.00 \| 14.48 \| 2.71 \| 0.00 \| 0.00
CoT-agnostic: domain-specific \| 24.20 \| 28.65 \| 5.04 \| 17.88 \| 11.38
CoT-aware: stronger-LLM-generated \| 31.80 \| 30.78 \| 6.98 \| 16.46 \| 14.29
AYOT (CoT-aware: self-generated) \| 58.40 \| 61.56 \| 14.93 \| 53.98 \| 39.15</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces a reasoning-aware post-training quantization framework that compresses LLMs to ternary weights while preserving reasoning performance.; rule check: matched taxonomy keywords; top rule score=5.0
- 全文指纹：`939d4aa7b1a95a7fd6dc22952c4250acbafd1de28f676d4edf97f1163d0935c0`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
