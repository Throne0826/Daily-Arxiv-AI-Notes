---
title: "[论文解读] Enhancing Low-Resource Language Reasoning via High-Resource Language Feature Transfer"
description: "[arXiv 2608.30462][LLM 机制与可解释性] 原文未明确报告。"
arxiv_id: "2608.30462"
announcement_date: "2026-09-01"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:41:38.581228+00:00"
source_sha256: "87ff32f0527174b97db14c49874a6637983c777926c19d3e301fec3740f7ffce"
tags:
  - "LLM 机制与可解释性"
  - "LLM Reasoning"
  - "LLM 其他"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2608.30462</p>

# Enhancing Low-Resource Language Reasoning via High-Resource Language Feature Transfer

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Minju Song, Hyeon Hwang, Junhyun Lee, Jaewoo Kang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Korea University；Hankuk University of Foreign Studies</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30462v1) · [PDF 下载](https://arxiv.org/pdf/2608.30462v1) · **关键词** LLM 机制与可解释性<br>


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

原文未明确报告。

**不用术语来说**：原文未明确报告。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 原文未明确报告。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于多语言大语言模型与机制可解释性研究的交叉领域。研究对象是一个固定参数的自回归解码器语言模型 $M$，它能够用不同语言回答同一数学推理问题，但在高资源语言（HRL，如英语、西班牙语）和低资源语言（LRL，如泰语、韩语、越南语、斯瓦希里语）之间表现不一致。本文不把差异仅视为训练数据、分词方式或基准覆盖率造成的表面现象，而是考察语言是否会改变模型对潜在任务推理机制的激活程度。具体而言，模型在残差流中的内部激活被稀疏自编码器（SAE）分解为较易解释的潜在特征；研究者从成功的 HRL 推理轨迹中筛选与数学任务相关的特征，再将相应方向注入 LRL 推理过程，以检验这些特征是否参与了跨语言推理差距。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**残差流激活**

Transformer 每层会维护一个表示当前序列状态的向量，本文记作 $h$，它包含模型在某个生成位置上的综合内部信息。干预残差流，就是在模型继续计算前直接修改这个向量，而不是更新模型参数。

</div>
<div class="concept-item" markdown="1">

**稀疏自编码器（SAE）**

SAE 将高维残差流向量 $h
onothing$ 转换为通常只有少数非零分量的潜在表示 $z$，并尝试用这些分量重建原向量。每个潜在分量可理解为一种可能反复出现的内部特征，例如与某类任务计算或生成行为相关的方向。

</div>
<div class="concept-item" markdown="1">

**机制干预与特征转向**

机制干预不是只观察某个特征是否与正确答案同时出现，而是在前向计算中主动增强或抑制该特征对应的残差方向，再观察答案正确性或答案得分是否改变。若增强 HRL 特征能改善 LRL 推理、抑制这些特征又会损害 HRL 推理，则可获得该特征参与相关计算的干预性证据，但这不等同于严格的逻辑充分条件或必要条件。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

设 $M$ 为固定的解码器语言模型，$\ell$ 为选定的残差流层，$\mathcal{D}$ 为数学推理基准。对于问题 $i\in\mathcal{D}$ 和语言 $k\in\{a,b\}$，模型生成长度为 $T_i^{(k)}$ 的思维链轨迹 $r_i^{(k)}$；其中 $a$ 表示目标低资源语言，$b$ 表示参考高资源语言。在每个生成位置 $t$，记录层 $\ell$ 的残差激活 $h_{i,t}^{(k)}\in\mathbb{R}^{d}$，并通过预训练 SAE 得到 $z_{i,t}^{(k)}\in\mathbb{R}^{F}$。目标是从“参考语言回答正确、目标语言回答错误”的配对问题中，识别与成功 HRL 数学推理相关、但不只是语言身份或一般生成行为的潜在特征，并构造干预方向，在不翻译输入、不微调参数且保持用户使用 LRL 的条件下，提高目标语言的推理表现。该设定还要求通过抑制、随机特征和排除特征等对照，区分单纯相关性与特征参与机制的干预证据。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$M$**

固定参数的解码器式大语言模型。

</div>
<div class="notation-item" markdown="1">

**$\ell$**

进行 SAE 分析和残差流干预的模型层。

</div>
<div class="notation-item" markdown="1">

**$a,b$**

语言标记；$a$ 为目标低资源语言（LRL），$b$ 为参考高资源语言（HRL）。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{D}$**

数学推理问题集合或基准数据集。

</div>

</div>

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法在一个固定、已经训练好的解码器式语言模型 $M$ 的第 $\ell$ 层残差流上使用稀疏自编码器（SAE）分解激活。它首先从同一道题在高资源参考语言（HRL，记为 $b$）中答对、低资源目标语言（LRL，记为 $a$）中答错的配对样本中，寻找在参考语言推理轨迹中出现而在目标语言轨迹中未出现的稀疏特征；随后按照这些特征在两种语言成功推理轨迹中的平均激活差异构造残差流干预方向，并仅在目标语言生成阶段注入该方向。其核心不是翻译、微调或更换输出语言，而是测试：目标语言是否只是没有充分激活模型中已有的、跨语言共享的推理机制。

直观地说，SAE 将复杂的内部状态拆成许多相对可辨认的“内部开关”。方法先找出英语成功解题时被拨动、而目标语言失败时没有被拨动的开关，再在目标语言生成每个推理词时适度拨动这些开关；如果性能提高，同时反向关闭这些开关会损害参考语言性能，便说明这些方向可能参与了该模型的跨语言推理过程。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造跨语言配对对比集

只保留参考语言答对而目标语言答错的同题样本，形成 $\mathcal{P}_{b\to a}=\{i\mid r_i^{(b)}\text{ correct}\wedge r_i^{(a)}\text{ incorrect}\}$。对两种语言的每条轨迹，在每个生成位置选择 SAE 激活值最大的特征，并汇总为该轨迹的不同特征集合。

<div class="method-step__io" markdown="1">

**输入**：推理基准 $\mathcal{D}$、参考语言 $b$ 与目标语言 $a$，以及模型在每道题上的两条链式思维轨迹 $r_i^{(b)}$ 和 $r_i^{(a)}$。<br>
**输出**：配对对比集 $\mathcal{P}_{b\to a}$，以及每个样本、每种语言对应的轨迹特征集合 $\mathcal{F}_i^{(k)}$。

</div>

**直观理解**：同一道题被用作自身对照：这样可以尽量排除题目难度差异，只观察语言改变后哪些内部特征随成功或失败而变化。每个词位置只记录最活跃的特征，类似于记录当时最明显被打开的内部开关。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 识别并筛选候选稀疏特征

计算特征 $f$ 在参考侧和目标侧分别作为逐词最高激活特征出现的样本数 $c_f^{(b)}$ 与 $c_f^{(a)}$，保留满足 $c_f^{(b)}\ge 1$ 且 $c_f^{(a)}=0$ 的特征，得到候选池 $\mathcal{C}_{\mathrm{cand}}$。再按 $c_f^{(b)}$ 降序排列，并删除排名最前的高频特征，只保留预设排名窗口 $(s,n)$ 内的集合 $\mathcal{C}$。

<div class="method-step__io" markdown="1">

**输入**：两侧轨迹特征集合 $\mathcal{F}_i^{(a)}$、$\mathcal{F}_i^{(b)}$，以及候选特征的出现频数。<br>
**输出**：最终用于干预的特征集合 $\mathcal{C}$。

</div>

**直观理解**：第一轮筛选寻找“参考语言成功时出现、目标语言失败时没出现”的开关。排名窗口用于避开过于常见的生成模式，因为这些模式可能只是普遍语言或格式现象，不一定代表数学推理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 估计跨语言特征差异并生成残差方向

在每种语言的正确轨迹全部生成词上计算平均 SAE 激活向量 $\bar z^{(k)}$，并对每个 $f\in\mathcal{C}$ 定义系数 $w_f=\bar z_f^{(b)}-\bar z_f^{(a)}$。将这些系数施加到选中特征，再用 SAE 解码器把潜变量差异转换为残差流干预向量 $\Delta h$。

<div class="method-step__io" markdown="1">

**输入**：两种语言中答对题目的生成轨迹及其 SAE 表示 $z_{i,t}^{(k)}$，最终特征集合 $\mathcal{C}$。<br>
**输出**：由选中特征和其有符号激活差异共同决定的残差空间方向 $\Delta h$。

</div>

**直观理解**：这里不只是判断某个开关是否出现，还估计参考语言中它比目标语言强多少。差异越大，该方向在目标语言中的补偿幅度越大；正负号保留了“应该增强还是减弱”的信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 目标语言推理时进行因果干预

在目标语言前向生成的每个生成词位置，通过 SAE 编码并将选中特征替换为 $\tilde z_f=z_f+\alpha w_f$；等价地，将 $\Delta h=\alpha\sum_{f\in\mathcal{C}}w_fW_{\mathrm{dec}}[f]$ 加回第 $\ell$ 层残差流。干预只作用于生成阶段，提示词预填充阶段保持不变，并使用同一个方向贯穿所有生成步。

<div class="method-step__io" markdown="1">

**输入**：目标语言输入、模型第 $\ell$ 层每个生成位置的残差激活 $h$、干预强度 $\alpha>0$ 和方向 $\Delta h$。<br>
**输出**：保持目标语言输出形式的干预后推理轨迹和最终答案。

</div>

**直观理解**：模型仍然阅读并用目标语言回答，方法只在内部计算过程中持续施加一个小的提示。这样可以检验性能变化是否来自内部机制激活，而不是把答案偷偷改写成参考语言。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 配对对比集与候选特征集合

$$
\mathcal{P}_{b\to a}=\bigl\{i\mid r_i^{(b)}\text{ correct}\wedge r_i^{(a)}\text{ incorrect}\bigr\},\qquad \mathcal{C}_{\mathrm{cand}}=\bigl\{f\mid c_f^{(b)}\ge 1\wedge c_f^{(a)}=0\bigr\}
$$

**符号说明**

- $\mathcal{P}_{b\to a}$：参考语言答对而目标语言答错的同题样本集合。
- $r_i^{(b)},r_i^{(a)}$：题目 $i$ 在参考语言 $b$ 和目标语言 $a$ 中生成的推理轨迹。
- $\mathcal{C}_{\mathrm{cand}}$：候选稀疏特征集合。
- $c_f^{(b)},c_f^{(a)}$：特征 $f$ 在参考侧或目标侧轨迹中作为逐词最高激活特征出现的样本数。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分只比较同一道题的成败差异，第二部分保留只在参考成功轨迹中出现、却没有在对应目标失败轨迹中出现的特征。它把跨语言性能差距转换成可操作的内部特征候选。<br>
**原文位置**：式（3）、式（6），§3.1

</div>

</div>

<div class="equation-block" markdown="1">

#### 残差流干预方向

$$
\Delta h=\mathrm{Dec}(\tilde z)-\mathrm{Dec}(z)=\alpha\sum_{f\in\mathcal{C}}w_fW_{\mathrm{dec}}[f],\qquad w_f=\bar z_f^{(b)}-\bar z_f^{(a)}
$$

**符号说明**

- $\Delta h$：加入第 $\ell$ 层残差流的干预向量。
- $\alpha$：正的干预强度，控制整体转向幅度。
- $w_f$：选中特征 $f$ 在参考语言和目标语言正确推理轨迹中的平均激活差异。
- $\bar z^{(b)},\bar z^{(a)}$：分别在两种语言正确推理轨迹的全部生成词上计算的平均 SAE 激活向量。
- $W_{\mathrm{dec}}[f]$：SAE 解码器中对应特征 $f$ 的残差空间方向。
- $\mathcal{C}$：经过集合差分和排名窗口筛选后的最终特征集合。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把多个潜特征的语言间激活差异重新组合成一个可直接作用于模型隐藏状态的方向。由于解码器是线性的，潜空间中的逐特征增强可以等价地实现为残差流中的方向添加。<br>
**原文位置**：式（9）、式（11），§3.2

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文方法不训练新的语言模型，也不在推理阶段进行参数优化；其 SAE 使用预训练、公开的模型配套 SAE。方法阶段主要进行轨迹收集、正确性筛选、特征频数统计和平均激活估计，因此不存在本文提出的端到端训练损失或新的参数优化目标。SAE 本身的训练目标原文未明确报告，且不应据此臆造。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 稀疏自编码器表示**

SAE 将第 $\ell$ 层残差激活 $h\in\mathbb{R}^{d}$ 编码为稀疏潜表示 $z\in\mathbb{R}^{F}$，每个潜特征对应一个解码器方向 $w_{\mathrm{dec}}^{(f)}$。稀疏性使单个特征可以作为相对独立、可检查的内部变量，而不是直接解释混合了多种信息的稠密隐藏状态。

> 直观理解：原始隐藏状态像一段同时包含许多信息的混合信号，SAE 尝试把它拆成许多较少同时开启的成分。研究者因此能够单独挑选、增强或抑制某些成分。

**2. 对比式任务特征选择**

特征选择以同题的成功参考轨迹和失败目标轨迹为对照，依据逐词最高激活特征的样本级出现频数执行集合差分，再通过排名窗口去除最常见的候选特征。该步骤是观察性的，只能产生候选机制，不能单独证明因果关系。

> 直观理解：它先找“只在成功一侧反复出现”的内部模式，但不会把这种相关性直接当成原因。后续必须实际修改模型内部状态，才能检验这些模式是否真的有功能作用。

**3. 残差流特征转向与因果检验**

选中特征的干预系数等于正确推理轨迹中的参考语言平均激活减去目标语言平均激活，解码后形成残差流方向。作者用三类干预检验其解释：目标侧激活测试部分充分性，参考侧抑制测试功能必要性，随机特征、最高频特征和负方向测试特异性；这些术语仅表示在规定干预策略和评测分布下的操作性证据。

> 直观理解：如果增强该方向能帮目标语言、关闭它会伤害参考语言，而随机方向没有同样效果，就比单纯观察相关性更能支持“这些内部方向参与了推理”的解释。不过这仍不等于在所有反事实情形下它们是唯一或绝对必要的原因。

**训练与推理**

首先固定一个已训练的指令微调语言模型和其第 $\ell$ 层预训练 SAE。对每道推理题分别用参考语言和目标语言生成链式思维轨迹并评分，构造 $\mathcal{P}_{b\to a}$；编码对应残差激活，提取逐词最高激活特征，按 $c_f^{(b)}$ 与 $c_f^{(a)}$ 做集合差分和排名窗口筛选，得到 $\mathcal{C}$。随后在两种语言的正确轨迹上计算 $\bar z^{(b)}$ 与 $\bar z^{(a)}$，为每个选中特征计算 $w_f$，并在目标语言推理时通过前向钩子将 $\Delta h$ 加到第 $\ell$ 层每个生成位置；提示预填充不受干预。

因果解释通过同一固定模型中的对照干预完成：目标语言使用正向量测试激活是否提高正确率，参考语言使用反向或抑制干预测试性能是否下降，并与随机特征、未经过排名过滤的最高频特征及负向量比较。作者将正向改善称为操作性的“部分充分性”、源侧下降称为“功能必要性”证据，但这些结论限于指定模型、层、干预强度和评测分布。

**复现信息**

实验使用 Gemma-2-9B-it 与 Qwen2.5-7B-Instruct，所有干预均位于第 20 层残差流；Gemma 使用 Gemma Scope SAE，Qwen 使用其第 20 层 Matryoshka SAE。SAE 激活以 float32 计算，推理采用贪心解码，最多生成 $1{,}024$ 个新词；提示模板要求模型用相应语言逐步推理并把最终答案放入 $\boxed{\cdot}$。数学答案由 math_verify 评分，多项选择题通过解析 $\boxed{\cdot}$ 中的首字母并使用备用答案格式进行判定。

为公平解释结果，应注意干预向量在所有问题和所有生成步保持相同，且只改变内部残差状态，不改变用户可见的目标语言提示。实现所需的软件和硬件版本虽在附录中给出，但对理解算法不是关键；特征宽度、GPU 配置等常规复现细节原文已有报告，此处仅保留能影响干预位置、解码行为和评分方式的设置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MATH500：采用多语言 MMATH 基准中的 MATH500 划分，共 $N=311$ 道题，主要测试多步符号推理。实验覆盖英语或西班牙语参考语言以及泰语、韩语、越南语目标语言，用于检验干预能否迁移较复杂的数学推理机制。
- MGSM：共 $N=250$ 道多语言小学数学文字题，测试从自然语言条件中建立算式并完成逐步推理的能力。实验以英语或西班牙语为参考语言，并在泰语、韩语和斯瓦希里语上评价迁移效果。
- MMLU-ProX Psychology：共 $N=798$ 道本科心理学十选一题，测试知识调用和非数学领域的多步判断。实验覆盖英语或西班牙语参考语言以及泰语、韩语、斯瓦希里语和越南语，作用是判断方法能否超越纯数学任务。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

目标语言最终答案的正确比例。MATH500 与 MGSM 使用 $\texttt{math\_verify}$ 核验数学答案，MMLU-ProX 则匹配最终选择的答案选项。它直接衡量干预后是否完成任务，而不评价中间推理文本是否忠实或可解释。 （越高越好，因为更高数值表示正确完成的测试题比例更大。）

</div>
<div class="metric-item" markdown="1">

**Recovery Rate**

恢复率定义为 $\mathrm{Recovery}_{a\rightarrow b}=(\mathrm{acc}_{a\rightarrow b}-\mathrm{acc}_a)/(\mathrm{acc}_b-\mathrm{acc}_a)$，其中 $\mathrm{acc}_a$ 是目标语言 $a$ 的基线准确率，$\mathrm{acc}_b$ 是参考语言 $b$ 的基线准确率，$\mathrm{acc}_{a\rightarrow b}$ 是向目标语言施加 steering 后的准确率。该指标表示原有参考—目标语言差距中有多大比例被干预消除；例如正值意味着向参考语言成绩靠近。 （通常越高越好，因为它表示缩小了更多跨语言差距；但它依赖参考语言与目标语言的初始差距，不能脱离原始准确率单独比较实际收益。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Gemma-2-9B-it，以英语为参考语言；MATH500 的泰语、韩语和越南语目标语言

<div class="result-value" markdown="1">

Vanilla CoT 在英语上的准确率为 $56.91\%$，三个目标语言基线分别为 $48.23\%$、$49.20\%$ 和 $48.23\%$；steering 后分别达到 $49.20\%$、$52.41\%$ 和 $51.77\%$，对应恢复率为 $11\%$、$42\%$ 和 $41\%$。其中韩语和越南语的提升较明显，而泰语只恢复了较小部分差距。

</div>

作者报告的结果说明，从英语成功推理样本中筛出的特征可以提高 Gemma 在三种目标语言上的 MATH500 准确率，并非只对单个目标语言有效。直观上，这与“模型已有部分数学计算机制，但低资源语言没有充分激活它们”的解释一致。不过，该结果只能表明干预具有功能效果；由于这里没有给出随机方向、非任务特征或翻译方案的同表比较，不能仅凭这些数值排除一般性激活扰动或提示敏感性等替代解释。

<div class="result-source" markdown="1">

来源：表 1，上半部分“Reference language: English”，Gemma-2-9B 行；MATH500 列

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Gemma-2-9B Baseline 56.91 48.23 49.20 48.23 89.60 78.40 76.40 75.60 57.27 32.71 17.67 8.27 40.73; +Steering 49.20 52.41 51.77 82.40 78.40 79.20 33.30 23.31 10.30 42.36; Recovery +11% +42% +41% +36% +15% +26% +2% +14% +4% +10%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen2.5-7B-Instruct，以英语为参考语言；MGSM 的泰语、韩语和斯瓦希里语目标语言

<div class="result-value" markdown="1">

英语参考准确率为 $95.20\%$，泰语、韩语和斯瓦希里语的基线分别为 $80.40\%$、$79.60\%$ 和 $15.20\%$；steering 后分别为 $82.00\%$、$80.00\%$ 和 $19.60\%$，恢复率为 $11\%$、$3\%$ 和 $6\%$。绝对提升分别为 $1.60$、$0.40$ 和 $4.40$ 个百分点，显示不同语言上的收益差异很大。

</div>

该结果把验证扩展到第二个模型和数学文字题：所有三个目标语言的准确率均上升，因此效果并不局限于 Gemma 或 MATH500。但恢复率与绝对提升并不一致，例如斯瓦希里语因初始差距很大，提升 $4.40$ 个百分点仍只恢复 $6\%$ 的差距。这说明 steering 是部分补偿，而非消除语言资源差异，也不能据此断言不同语言共享完全相同的内部推理表示。

<div class="result-source" markdown="1">

来源：表 1，上半部分“Reference language: English”，Qwen2.5-7B 行；MGSM 列

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen2.5-7B Baseline 73.63 60.77 64.95 63.67 95.20 80.40 79.60 15.20 59.90 39.35 42.48 15.29 49.50; +Steering 63.70 66.60 66.56 82.00 80.00 19.60 41.60 44.11 17.42 53.13; Recovery +23% +19% +29% +11% +3% +6% +11% +9% +5% +35%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen2.5-7B-Instruct，以西班牙语为参考语言；MMLU-ProX Psychology 的泰语、韩语、斯瓦希里语和越南语目标语言

<div class="result-value" markdown="1">

西班牙语参考准确率为 $53.01\%$；泰语、韩语、斯瓦希里语和越南语基线分别为 $39.35\%$、$42.48\%$、$15.29\%$ 和 $49.50\%$，steering 后分别达到 $41.10\%$、$43.61\%$、$15.54\%$ 和 $51.38\%$，对应恢复率为 $13\%$、$11\%$、$1\%$ 和 $54\%$。越南语只提高 $1.88$ 个百分点，却因其初始差距仅为 $3.51$ 个百分点而得到较高恢复率。

</div>

该设置同时检验非英语参考语言与非数学专业知识任务。四种目标语言均有正向变化，支持特征迁移不只来自英语，也不只作用于算术或符号推理。与此同时，斯瓦希里语仅恢复 $1\%$ 的差距，表明方法在大幅落后的语言上可能很有限；越南语的 $54\%$ 恢复率则提醒读者，较高比例可能来自较小的初始分母，并不等同于巨大的绝对准确率提升。

<div class="result-source" markdown="1">

来源：表 1，下半部分“Reference language: Spanish”，Qwen2.5-7B 行；MMLU-ProX (psychology) 列

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen2.5-7B Baseline 67.85 60.77 64.95 63.67 84.00 80.40 79.60 15.20 53.01 39.35 42.48 15.29 49.50; +Steering 63.34 65.90 66.56 82.00 82.00 19.60 41.10 43.61 15.54 51.38; Recovery +36% +33% +69% +44% +55% +6% +13% +11% +1% +54%.

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

- Vanilla CoT：模型使用题目所在语言的原生思维链提示直接推理，不施加残差流干预。它是最直接的对照，用来测量模型原本的目标语言能力，并作为计算提升量和恢复率的起点。
- 高资源参考语言准确率：同一模型在英语或西班牙语题目上的 Vanilla CoT 成绩，被用作对应语言对的性能上限和跨语言差距终点；参考语言本身不接受 steering。该比较控制了模型和任务，仅改变语言，但这个“上限”只是实验定义的参照值，并非理论最优准确率。
- 跨模型对照：实验分别使用 Gemma-2-9B-it 与 Qwen2.5-7B-Instruct。两者不是额外训练出的竞争方法，而是用于检查结论是否依赖单一模型架构或单一 SAE 特征空间。
- 跨参考语言对照：分别从英语和西班牙语构造参考到目标语言的特征迁移。该设置检验有效特征是否只能由英语诱发，还是另一种高资源语言也能提供可迁移的任务相关机制。

**实验想回答的问题**

- 从高资源参考语言中筛出的任务相关稀疏特征，在注入低资源目标语言的生成过程后，能否提高数学推理与专业知识推理的准确率，并缩小同一模型内部的跨语言性能差距？
- 这种特征迁移是否能跨模型、跨参考语言及跨任务稳定生效，而不是只对某个特定模型、语言对或数学数据集有效？

**实验实现**

实验使用指令微调模型 Gemma-2-9B-it 和 Qwen2.5-7B-Instruct，并分别配对预训练的第 20 层稀疏自编码器：Gemma-Scope 的特征宽度为 $F=16{,}384$，Qwen 的 matryoshka SAE 为 $F=65{,}536$ 且每次保留 $k=100$ 个活跃特征；两者均采用 JumpReLU 架构。对每个“参考语言—目标语言—数据集”组合，候选池来自参考语言答对、目标语言答错的题目；按出现次数排序后丢弃前 $50\%$ 的候选，只保留第 50 至第 90 百分位的特征，以减少高频语言或通用生成特征的干扰。推理时在第 20 层残差流的每个生成步骤注入 steering 方向，但不改变提示预填充阶段的激活。所有题目均以单一语言呈现并使用该语言的思维链提示。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work uses sparse autoencoders and causal feature steering to analyze and transfer mechanisms underlying multilingual mathematical reasoning.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`87ff32f0527174b97db14c49874a6637983c777926c19d3e301fec3740f7ffce`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
