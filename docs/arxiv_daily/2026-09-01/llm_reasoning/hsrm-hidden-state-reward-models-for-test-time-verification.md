---
title: "[论文解读] HSRM: Hidden-State Reward Models for Test-Time Verification"
description: "[arXiv 2608.30841][LLM Reasoning] HSRM利用生成模型在解题时已经计算出的隐藏状态，以约200万参数的轻量级Transformer对候选数学解答进行排序，从而避免大型文本验证器重新读取完整解答所带来的额外推理成本。"
arxiv_id: "2608.30841"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:31:48.766074+00:00"
source_sha256: "73537b2e140583f04c8638301352c534d493cbfe1d5fc9a99def5691bccb8f1b"
tags:
  - "LLM Reasoning"
  - "LLM 效率"
  - "LLM 其他"
  - "LLM 机制与可解释性"
  - "隐藏状态奖励模型"
  - "测试时验证"
  - "best-of-N 推理"
  - "数学推理"
  - "结果级监督"
  - "候选排序"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.30841</p>

# HSRM: Hidden-State Reward Models for Test-Time Verification

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Xianzhi Li, Xiaodan Zhu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Department of Electrical and Computer Engineering & Ingenuity Labs Research InstituteQueen’s University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30841v1) · [PDF 下载](https://arxiv.org/pdf/2608.30841v1) · **关键词** 隐藏状态奖励模型, 测试时验证, best-of-N 推理, 数学推理, 结果级监督, 候选排序<br>
**代码**: [https://github.com/JXL884/HSRM](https://github.com/JXL884/HSRM)

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

HSRM利用生成模型在解题时已经计算出的隐藏状态，以约200万参数的轻量级Transformer对候选数学解答进行排序，从而避免大型文本验证器重新读取完整解答所带来的额外推理成本。

**不用术语来说**：面对一道数学题，语言模型通常可以生成多份看似合理的解答，但其中可能只有部分正确；系统因此需要从这些候选中选出最可信的一份。传统做法是让另一个模型把每份答案重新读一遍并打分，这相当于在生成之后又进行一次昂贵的文本处理。本文要解决的是：能否直接利用生成过程中已经产生的内部计算结果来判断答案，而不再让大型验证模型重复阅读文本。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出隐藏状态奖励模型HSRM：在冻结生成器参数的前提下，提取推理步骤边界处的隐藏状态，并用小型Transformer编码器为完整候选解答输出标量分数，以支持best-of-$N$候选选择。
- 提出一种低监督成本的适配方式：直接采样生成器自己的解题轨迹，依据最终答案是否正确赋予结果标签，并学习将正确候选排在错误候选之前；该方法不需要人工编写的逐步过程监督，也不依赖预先构建的大型验证器语料。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型的测试时推理与答案验证研究。基本场景是：生成器针对同一道数学题采样多个看似合理的推理轨迹，再由验证器为候选解评分并选出最可信者；这种 best-of-$N$ 策略能以额外推理计算换取更高准确率，但效果取决于验证器的排序质量与成本。传统文本验证器需要在候选生成完毕后重新读取、编码整段推理文本，较大的过程奖励模型甚至本身也是语言模型，因此验证可能占据显著推理开销。本文所依赖的关键事实是，生成器在解码时形成的隐藏状态可能已经编码答案正确性、事实性或错误风险等信息，因而可将这些内部表示直接作为验证输入，避免另一模型重复处理文本。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**best-of-N 推理**

对同一问题随机生成 $N$ 个候选解，并用验证器评分后返回最高分候选。它不是让模型只生成一次，而是通过增加测试时采样量提高找到正确解的机会。

</div>
<div class="concept-item" markdown="1">

**隐藏状态**

隐藏状态是语言模型处理上下文并生成每个词元时产生的内部向量表示，其中可能包含语义、推理进度及正确性相关信号。HSRM读取这些已在生成过程中算出的向量，而不是仅观察最终输出文字。

</div>
<div class="concept-item" markdown="1">

**结果奖励模型与过程奖励模型**

结果奖励模型依据完整解答或最终答案是否正确来学习评分；过程奖励模型则对中间推理步骤提供监督或分数。本文采用候选轨迹的最终正确性标签训练排序器，不要求人工撰写逐步过程监督。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一道目标领域的数学问题，以及冻结生成器为该问题采样得到的 $N$ 条候选推理轨迹；生成过程中同时保留各词元对应的末层隐藏状态。HSRM在推理步骤边界抽取隐藏状态，将每条候选压缩成步骤级向量序列，再输出一个标量奖励分数，用于把正确候选排在错误候选之前并选出最终答案。该设定假定候选的最终答案可以获得结果级正确性标签，以便从生成器自身采样的轨迹训练验证器；它不依赖人工过程标注或既有的大型验证器语料，并且生成器参数保持冻结。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$N$**

同一道问题在 best-of-N 推理中采样的候选解数量。

</div>
<div class="notation-item" markdown="1">

**$T_{s,n}$**

图1中第 $s$ 个推理步骤内第 $n$ 个位置的生成词元。

</div>
<div class="notation-item" markdown="1">

**$H_{s,n}$**

冻结生成器生成词元 $T_{s,n}$ 时产生的末层隐藏状态。

</div>
<div class="notation-item" markdown="1">

**$[S]$**

从推理步骤边界抽取隐藏状态后形成的紧凑步骤级序列；相较完整的词元级序列，它只保留每步的代表性内部表示。

</div>

</div>

**直接相关的工作**

- **EORM（Jiang et al., 2025）**: EORM以紧凑能量模型为思维链文本评分，代表降低文本验证器规模的路线；但它仍需重新编码每条候选文本。HSRM改为复用生成器解码时已经计算的隐藏状态，研究重点由“缩小文本验证模型”转向“消除重复文本编码”。
- **SWIFT/ELHSR（Guo et al., 2025）与 ReProbe（Ni et al., 2026）**: 两者均直接利用模型内部特征进行推理验证：SWIFT/ELHSR在词元级隐藏状态上应用轻量奖励头，ReProbe则用轻量 Transformer 探针处理词元级特征并在步骤内聚合。HSRM与其方向互补，但直接在推理步骤边界取样，将输入构造成更短的步骤级序列，而非先处理完整词元级表示。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

测试时扩展推理通常对同一道题采样多个候选解答，再依靠验证器选择最优候选。该流程能否提高准确率，不仅取决于生成器是否产生了正确解，还取决于验证器能否可靠且低成本地识别它。随着候选数量$N$增加，每份解答都要接受验证，验证成本可能成为整个推理流程的重要负担。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **结果奖励模型**：验证器将候选解答作为文本重新编码，并根据最终答案或整条解题轨迹输出一个总体分数；best-of-$N$流程随后选择得分最高的候选。它只需要结果层面的正确性标签，但其判断依据仍主要来自重新读取候选文本。
- **过程奖励模型**：验证器逐步阅读推理文本，并对中间步骤分别评估或打分，以便发现局部推理错误。较新的过程奖励模型本身往往也是大型语言模型，并且训练时通常需要更细粒度的过程监督。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 文本验证器忽略了生成阶段已经计算出的内部表示：生成器完成候选解答后，独立验证模型还必须再次编码相同文本。当候选较多或验证器本身较大时，这种重复计算会使验证成为总推理成本的重要组成部分。
- 过程级验证虽然提供更细粒度的判断，却可能依赖人工编写或标注的中间步骤监督，并需要较大的预训练验证模型；这提高了数据构建和部署门槛，也不利于快速适配新的目标领域。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究表明，语言模型的隐藏表示能够编码其答案是否可能正确、内容是否真实等信号，但这些发现尚未充分转化为数学推理中的实用候选排序机制。具体缺口是：能否把生成器解码时自然产生的隐藏状态压缩为低成本的解答级验证信号，并仅依靠自生成轨迹及最终结果标签完成训练，同时保持与更大文本验证器相当的选择能力。

</div>
<div markdown="1"><span>核心问题</span>

冻结的数学推理生成器在推理步骤边界处产生的隐藏状态，是否足以支持一个轻量级奖励模型可靠地排序正确与错误候选，从而替代需要重新编码完整解答文本的大型验证器？

</div>
<div markdown="1"><span>作者直觉</span>

生成器写出每一步推理时，其隐藏状态不仅表示即将输出的词，还汇集了当前问题、既有推理链和模型内部置信信息。若正确与错误轨迹在这些内部表示中留下可分辨的模式，小型模型就不必重新理解整段文字，只需读取若干步骤边界的状态并综合判断。通俗地说，HSRM不是请另一位“大模型阅卷”，而是读取原生成器解题过程中留下的内部工作痕迹，再学习哪些痕迹更常对应正确答案。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

HSRM（Hidden-State Reward Model）是一个用于最佳候选选择（Best-of-$N$，即从同一题生成 $N$ 个答案后选一个）的轻量级验证器。给定冻结的生成器 $p_{\theta}$、题目 $x$ 和候选解答集合 $\{y_i\}_{i=1}^{N}$，HSRM不重新读取候选文本，而是在生成过程中提取生成器已经计算出的推理步骤边界隐藏状态，经线性投影、小型Transformer编码器和候选级读出层得到分数 $f_{\phi}(x,y_i)$，最后选择得分最高的候选。直观地说，它像是读取生成器在“写答案时留下的内部笔记”，而不是让另一个模型再次通读完整答案，因此可以减少验证阶段的重复计算。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选解答生成

生成器对每道题采样 $N$ 个候选解答 $\{y_i\}_{i=1}^{N}$，其中每个候选解答表示为 token 序列 $y=(y_1,\ldots,y_T)$。生成过程中同时保存各 token 位置和生成器层的隐藏状态。

<div class="method-step__io" markdown="1">

**输入**：题目提示 $x$、冻结的生成器 $p_{\theta}$ 和候选数量 $N$。<br>
**输出**：候选解答集合 $\{y_i\}_{i=1}^{N}$ 及其生成时产生的隐藏状态张量。

</div>

**直观理解**：先让同一个语言模型独立解题多次，得到若干可能正确、也可能错误的答案；验证器使用生成时已经产生的内部表示，避免之后再次编码答案文本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 推理步骤边界抽取

利用常见的步骤终止分隔符定位推理步骤边界，取每个边界之前的 token 位置 $t_1<t_2<\cdots<t_S\leq T$，并构造 $H^{\ell}(y)=[h_{t_1}^{\ell};\ldots;h_{t_S}^{\ell}]\in\mathbb{R}^{S\times d_{\mathrm{gen}}}$。默认使用生成器最后一层 $\ell=L$，且包含最终生成 token 的表示。

<div class="method-step__io" markdown="1">

**输入**：单个候选解答 $y$ 的 token 级隐藏状态 $\{h_t^{\ell}\}_{t=1}^{T}$。<br>
**输出**：长度为推理步骤数 $S$ 的隐藏状态序列 $H^{\ell}(y)$。

</div>

**直观理解**：模型不必逐字检查答案，只在每个推理步骤结束的位置取一个“摘要式内部状态”；因此验证器看到的是步骤级序列，而不是很长的完整 token 序列。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 隐藏状态编码与候选打分

先对每个步骤状态进行线性投影 $z_s^{(0)}=W_{\mathrm{in}}h_{t_s}^{\ell}+b_{\mathrm{in}}$，再通过小型Transformer编码器建模不同推理步骤之间的关系。对未填充的步骤表示进行均值池化和层归一化，得到候选表示 $z$，随后由线性读出层计算 $f_{\phi}(x,y)=w^{\top}z+b$。

<div class="method-step__io" markdown="1">

**输入**：步骤级隐藏状态序列 $H\in\mathbb{R}^{S\times d_{\mathrm{gen}}}$。<br>
**输出**：每个候选解答的标量验证分数 $s_i=f_{\phi}(x,y_i)$。

</div>

**直观理解**：线性层先把生成器的内部表示转换为验证器能处理的宽度，Transformer再判断各步骤组合起来是否像一个正确解答，最后把整条推理压缩成一个分数。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 最佳候选选择

在同一道题的候选集合中执行Best-of-$N$选择：$\hat{y}=y_{\arg\max_i f_{\phi}(x,y_i)}$。

<div class="method-step__io" markdown="1">

**输入**：$N$ 个候选解答及其验证分数 $\{f_{\phi}(x,y_i)\}_{i=1}^{N}$。<br>
**输出**：最终返回的候选解答 $\hat{y}$。

</div>

**直观理解**：验证器不负责重新生成答案，只负责在已有候选中挑出最可信的一个；最高分被解释为最可能正确。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 步骤边界隐藏状态序列

$$
H^{\ell}(y)=\left[h_{t_{1}}^{\ell};h_{t_{2}}^{\ell};\ldots;h_{t_{S}}^{\ell}\right]\in\mathbb{R}^{S\times d_{\mathrm{gen}}}
$$

**符号说明**

- $y=(y_1,\ldots,y_T)$：候选解答的 token 序列，$T$ 为 token 总数。
- $h_t^{\ell}$：生成器在 token 位置 $t$、层 $\ell$ 的隐藏状态，维度为 $d_{\mathrm{gen}}$。
- $t_1<\cdots<t_S\leq T$：推理步骤边界之前的 token 位置，$S$ 为步骤边界数量。
- $H^{\ell}(y)$：由步骤边界隐藏状态组成的矩阵，作为HSRM的输入。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把逐 token 的内部表示筛选成逐推理步骤的表示。这样既保留了生成器在步骤结束时对当前推理的总结，又减少了验证器需要处理的序列长度。<br>
**原文位置**：第3.1节，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 同题候选的安全成对排序损失

$$
\mathcal{L}_{\mathrm{rank}}=\frac{1}{|\mathcal{P}||\mathcal{N}|}\sum_{i\in\mathcal{P}}\sum_{j\in\mathcal{N}}\log\!\left(1+e^{-(s_i-s_j)}\right)
$$

**符号说明**

- $\mathcal{P}=\{i:c_i=1\}$：同一道训练题中被标记为正确的候选索引集合。
- $\mathcal{N}=\{j:c_j=0\}$：同一道训练题中被标记为错误的候选索引集合。
- $c_i\in\{0,1\}$：候选解答 $y_i$ 的二元正确性标签。
- $s_i=f_{\phi}(x,y_i)$：HSRM对题目 $x$ 和候选解答 $y_i$ 输出的验证分数。
- $|\mathcal{P}|,|\mathcal{N}|$：该问题中正确候选和错误候选的数量。

<div class="equation-explanation" markdown="1">

**直观理解**：损失函数逐一惩罚“错误候选分数不低于正确候选”的情况；当正确候选分数高出错误候选时，损失变小。由于只比较正确与错误两类，不会强迫多个正确答案形成任意的内部排序。<br>
**原文位置**：第3.3节，公式(6)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标是在同一道题内部让所有正确候选的分数高于错误候选。对每个正确索引 $i\in\mathcal{P}$ 和错误索引 $j\in\mathcal{N}$，排序损失惩罚分数差 $s_i-s_j$ 不足；正确候选之间不产生排序约束，因此适合一题有多个正确解答的情形。若某道题没有正确候选或没有错误候选，即 $|\mathcal{P}|=0$ 或 $|\mathcal{N}|=0$，则该题不提供同题排序信号，并从训练损失中省略。论文还说明会将该目标与点式BCE和ListMLE比较，但本方法默认采用公式(6)的tie-safe pairwise ranking loss。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 步骤边界隐藏状态提取器**

生成器在 token 位置 $t$、层 $\ell$ 的残差流表示为 $h_t^{\ell}\in\mathbb{R}^{d_{\mathrm{gen}}}$。HSRM只保留步骤边界位置的表示，形成 $S\times d_{\mathrm{gen}}$ 的输入，而不是处理全部 $T$ 个 token；这些表示在生成阶段已经计算完成，因此无需额外的生成器前向传播。

> 直观理解：该模块利用生成器已有的中间结果，并把长文本压缩为较短的步骤序列，是HSRM降低验证成本的关键。

**2. 步骤级Transformer验证器**

输入投影 $W_{\mathrm{in}}$ 将生成器宽度 $d_{\mathrm{gen}}$ 映射到验证器宽度 $d_{\mathrm{model}}$；默认验证器使用两层Transformer、四个注意力头、前馈层宽度为 $4d_{\mathrm{model}}$，其中 $d_{\mathrm{model}}=256$。Transformer在步骤维度上交互，使某一步的表示能够结合其他步骤判断整体推理是否一致。

> 直观理解：单独看某个推理步骤可能无法判断对错，Transformer让验证器能够观察步骤之间的依赖，例如前面的设定是否支持后面的计算。

**3. 候选级读出与排名机制**

编码后的步骤表示先在未填充位置上均值池化，再经过层归一化，最后由线性层输出标量分数。训练时采用同一问题内的正确—错误候选成对排序，而不是强迫多个正确候选彼此排序。

> 直观理解：模块把整条推理汇总为一个可比较的分数；只要求正确答案胜过错误答案，避免把同样正确但写法不同的答案人为排出高低。

**训练与推理**

训练阶段先运行冻结生成器，为训练问题采样候选解答、获得答案正确性标签，并缓存步骤边界隐藏状态；随后只优化HSRM参数 $\phi$，不再调用生成器。默认使用AdamW、学习率 $1\times10^{-4}$、问题批大小8、1000个梯度步、0.20的问题级验证划分和0.1 dropout；这些设置来自附录C，但核心训练流程是基于缓存表示学习同题候选排序。推理阶段对每道题采样 $N$ 个候选，缓存相同类型的步骤边界表示，在一个批量验证器前向过程中计算所有候选分数，并返回 $\arg\max_i f_{\phi}(x,y_i)$ 对应的候选。由于隐藏状态由生成器生成时已经得到，新增成本主要是小型HSRM对步骤表示的一次前向计算，而不是对每个候选文本再次进行生成器或文本验证器编码。

**复现信息**

默认模型使用最终生成器层的隐藏状态、$d_{\mathrm{model}}=256$、两层Transformer、四个注意力头和宽度为 $4d_{\mathrm{model}}$ 的前馈层，约有2M参数；实际参数量随生成器隐藏维度变化，附录表4报告Qwen3-1.7B、4B、8B和14B对应约2.12M、2.25M、2.65M和3.4M参数。输入按步骤终止分隔符切分，包括换行、句号换行和冒号换行等模式；池化时忽略填充位置。生成器保持冻结，缓存表示使用float16；训练和推理都复用同一抽取方式，以保证训练输入与实际验证输入一致。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：以小学到中学层级的多步文字算术题检验较容易、接近饱和条件下的候选筛选能力。训练池对每道训练题采样 $64$ 个解答，评测时在问题级不重叠的划分上从 $8$ 个候选中选择一个；正文未在所给片段中列出具体题目数量和索引。
- MATH-500：覆盖更复杂的竞赛式数学问题，用于检验验证器能否区分形式上相似但数学正确性不同的推理。训练和评测同样采用每题 $64$ 个训练候选与 best-of-$8$ 评测；附录明确说明 Table 7 的 MATH-500 行使用较早划分，只用于观察随候选数变化的趋势，因此不应与主实验数值直接混用。
- AIME：代表低正确率、高难度竞赛数学环境，主要检验当正确候选稀少时，隐藏状态排序是否仍优于文本验证器或简单置信度启发式。它也是压力测试：较小的绝对差异可能来自候选池中本来就很少出现正确答案，而不一定表示排序器没有信号。论文还评测 OlympiadBench，但受字段数量限制未在此单列。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Verifier-best accuracy at $N=8$**

对每道题采样 $8$ 个候选，由验证器选择得分最高者；若其最终答案正确，则该题计为正确。它直接对应论文的部署目标，但同时受候选生成质量约束：候选池没有正确答案时，再好的验证器也无法成功。 （越高越好，因为它表示验证器最终选中正确答案的问题比例更高。）

</div>
<div class="metric-item" markdown="1">

**Within-problem AUROC**

在同一道题的候选池内部，用验证器分数区分正确与错误候选，随后仅对可定义 AUROC 的题目求平均。它比最终 top-$1$ 选择更全面地衡量排序质量，但不会直接等同于 best-of-$8$ 的实际准确率。 （越高越好；$0.5$ 附近相当于随机区分，而更高值表示正确候选通常获得更高分。）

</div>
<div class="metric-item" markdown="1">

**Oracle pass@$N$**

检查每题的 $N$ 个采样候选中是否至少存在一个正确答案，不考察验证器能否识别它。该指标刻画候选池所允许的理论上限，并用于判断继续扩大候选池或改进排序器可能还有多少空间。 （越高表示生成阶段更常覆盖正确答案；它是上限指标，不是可部署验证器本身的成绩。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四种 Qwen3 规模与四个数学基准上的 HSRM 对 EORM 主比较

<div class="result-value" markdown="1">

作者报告，HSRM 在 $16$ 个生成器—数据集组合中的 $15$ 个达到或超过 55M 参数文本 EORM，而 HSRM 仅约 2M 参数。正文进一步称 GSM8K 的四种生成器规模上 HSRM 均优于 EORM；在 MATH-500、AIME 和 OlympiadBench 上通常也保持领先，但所给 Figure 2 文本没有给出各单元的精确分数。

</div>

这支持“生成过程中已有的内部表征足以承担轻量候选验证”这一主要经验结论：HSRM 不必重新读取整段文本，也能在多数设置中优于更大的文本验证器。它并不证明隐藏状态验证在所有模型、任务或解码策略上都占优，因为生成器仅来自同一 Qwen3 系列，且主要实验关闭 thinking mode；“达到或超过”也没有说明每个单元的差异是否具有统计显著性。

<div class="result-source" markdown="1">

来源：摘要；主趋势见 Figure 2 与 Section 5.1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across four mathematical reasoning benchmarks, HSRM matches or outperforms a 55M-parameter text-only energy verifier in 15 of 16 generator--dataset settings while using only about 2M parameters, providing an efficient alternative to text-only verification by reusing representations already computed during generation.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### HSRM 对每个单元事后选出的最佳廉价启发式，覆盖四个数据集和四种生成器规模

<div class="result-value" markdown="1">

HSRM 在 $16$ 个单元中胜出 $12$ 个、持平 $2$ 个、落后 $2$ 个。优势在 GSM8K 和 OlympiadBench 的所有生成器规模上保持一致；两个明确落后单元是 MATH-500 4B 的 $85.8\%$ 对 $86.2\%$，以及 AIME 8B 的 $17.7\%$ 对 $19.3\%$。

</div>

由于基线可以针对每个单元事后挑选最有利的概率、熵或长度规则，这比实际部署时预先固定一个启发式更苛刻。多数单元仍由 HSRM 胜出，说明其排序信号通常不只是长度或置信度的简单复刻；但 AIME 和部分接近饱和的 MATH-500 单元显示，低信号或边际空间很小时，学习型验证器未必优于廉价规则。

<div class="result-source" markdown="1">

来源：Appendix D，Table 8 及“Cheap scorers”小节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Even under this favorable comparison, HSRM outperforms the best cheap scorer in 12 of 16 settings, ties in 2, and underperforms in only 2.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 验证器参数量、权重内存、输入形式和额外生成器调用成本

<div class="result-value" markdown="1">

默认 HSRM 约为 $2.1$–$3.4$M 参数、float16 权重约 $4$–$7$MB，读取至多 $100$ 个步骤隐藏状态，并且额外生成器前向次数为 $0$。作为对照，EORM 为 $53.4$M 参数、约 $107$MB，需重新编码文本；Qwen2.5-Math-PRM-7B 约 $7.6$B 参数、约 $15$GB，并进行生成器规模的文本重编码。

</div>

该结果说明 HSRM 的主要工程价值来自复用生成时已经计算的表征：候选生成完毕后，小编码器直接处理少量步骤向量。这里给出的是模型权重和额外重编码方式，而不是完整端到端延迟、缓存隐藏状态所需显存、吞吐量或能耗，因此不能仅凭参数和权重内存断言实际系统一定按相同比例加速。

<div class="result-source" markdown="1">

来源：Appendix D，Table 11，HSRM 行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

HSRM (ours) | 2.1–3.4M | ∼4–7MB | S≤100 hidden states | 0

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主实验集中于同一 Qwen3 模型家族、数学推理任务和 non-thinking mode，因此尚不能由这些结果推出 HSRM 能迁移到其他生成器架构、开放式任务或显式长思考模式。候选标签还依赖答案归一化规则及带标准答案上下文的 LLM judge，潜在标签误差可能影响训练和评测。
- 效率证据主要是参数量、float16 权重内存、输入长度形式和额外生成器调用次数；原文片段未明确报告端到端延迟、吞吐量、隐藏状态缓存开销或总能耗。此外，多处结果接近 oracle 上限或处于 AIME 的低准确率区间，较小分差不应被解释为普遍而显著的实际优势。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- EORM 55M：主要容量对照。它是约 55M 参数的文本能量验证器，以 Transformer 重新编码完整思维链，并用 Bradley–Terry 排序目标训练。该比较直接检验复用生成器隐藏状态，是否能用显著更小的验证器替代文本重编码。
- Qwen2.5-Math-PRM-7B：约 7B 参数、使用 MATH 风格过程监督训练的现成过程奖励模型。它代表强大的外部领域专用验证器，但既不与 HSRM 容量匹配，也不控制训练数据和监督来源，因此适合提供性能参照，不适合单独归因隐藏状态设计的优劣。
- 单次生成与 oracle pass@$N$：前者不执行候选重排，是验证器所带来增益的下界参照；后者只要候选池中存在正确答案就计为成功，是固定采样池对任何选择器施加的上限。两者共同区分“生成器没有产生正确解”与“已经产生但验证器没有选中”。
- 廉价内部启发式：包括累积或平均对数概率、负平均熵、负 varentropy、回答长度、推理步骤数等。Table 8 甚至为每个数据集—生成器单元事后选取其中最好的启发式，形成偏向启发式的乐观包络，用于检验 HSRM 是否只是学习了置信度或长度代理。

**实验想回答的问题**

- 在冻结不同规模的 Qwen3 生成器后，仅利用生成过程中已经产生的推理步骤边界隐藏状态，约 2M 参数的 HSRM 能否在数学推理的 best-of-$8$ 候选选择中，达到或超过需要重新读取完整文本的 55M 参数 EORM，并缩小与 7B 过程奖励模型之间的差距？
- HSRM 的收益是否来自真正具有判别力的内部表征，而非候选长度、生成概率或熵等廉价代理信号；其训练目标和编码器容量分别对候选排序质量有何影响？

**实验实现**

实验使用 Qwen3-1.7B、4B、8B 和 14B 四种生成器；主实验均关闭 thinking mode，并在训练和评测期间冻结生成器，只训练 HSRM 或可学习基线。所有生成器以 float16、温度 $0.7$、top-$p=0.9$ 采样；训练时每题生成 $64$ 个候选，评测时使用相互独立的问题划分和 $8$ 个候选。候选最终答案先按数据集规则抽取并归一化常见格式及符号等价形式，仍有歧义时由能看到标准答案的 LLM judge 判定。该后处理提高了标签可用性，但也把规则和裁判模型引入监督链条。

默认 HSRM 是隐藏宽度 $256$、4 个注意力头、dropout $0.1$ 的两层 Transformer，输入为冻结生成器最后一层在推理步骤边界处的隐藏状态。隐藏状态和候选池只生成并缓存一次，此后训练验证器无需再次调用生成器。可学习验证器使用五个随机种子和问题级验证集早停；分布内结果报告五次运行的均值与标准差。零样本迁移则在源数据集训练后直接评测目标数据集，不做目标域验证器训练，但所给片段未提供其具体结果。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 训练目标消融：在相同 Qwen3-1.7B 候选池和相同 HSRM 架构下，对比 tie-safe Bradley–Terry、ListMLE 与二元交叉熵 | 在 GSM8K 上，Bradley–Terry 的 best-of-$8$ 准确率为 $85.93\%\pm0.56$、within-problem AUROC 为 $0.718\pm0.007$，高于 ListMLE 的 $84.59\%\pm1.41$、$0.694\pm0.027$ 和 BCE 的 $83.91\%\pm0.45$、$0.687\pm0.006$。MATH-500 上相同目标也以 $66.91\%\pm0.89$ 和 $0.620\pm0.014$ 取得三者最佳结果。 | 该消融只改变损失函数，因此较直接地检验训练目标与推理需求是否对齐。Bradley–Terry 只要求同一题中的正确候选分数高于错误候选，不强迫多个同标签候选互相排序；BCE 把候选独立分类，ListMLE 则要求完整次序。结果支持“保留同标签并列关系的成对排序更适合 best-of-$N$”这一解释，但只在两个数据集和 1.7B 生成器上验证，不能保证结论对所有规模都成立。 | Appendix D，Table 9；解释见 Appendix E“Training Objective”<br><span class="experiment-evidence">GSM8K \| Bradley–Terry (Eq. (6)) \| 85.93 ± 0.56 \| 0.718 ± 0.007</span> |
| 编码器架构消融：DeepSet $d=128$、Transformer $d=128$ 与默认 Transformer $d=256$ | 三种编码器总体成绩接近，默认宽 Transformer 并未全面取胜。例如 GSM8K 8B 上，默认模型为 $94.99\%\pm0.22$、AUROC $0.682\pm0.029$，高于两个较小编码器的 AUROC；但 MATH-500 14B 上，$d=128$ Transformer 达到 $89.10\%\pm1.12$，而默认 $d=256$ Transformer为 $87.90\%\pm0.78$。 | 该实验固定输入隐藏状态、损失、学习率、训练步数、批量大小和验证划分，主要隔离聚合器容量与结构。没有架构在所有单元占优，说明有效信号很可能已经存在于步骤边界隐藏状态中，而不是由高容量 Transformer 凭空构造；默认 $d=256$ 模型是稳定的折中方案，却不是每个数据集和生成器组合的最优选择。 | Appendix D，Table 10，MATH-500 14B 行；解释见 Appendix E“Encoder architecture”<br><span class="experiment-evidence">MATH-500 \| 14B \| 87.90 ± 0.46 / 0.568 ± 0.021 \| 89.10 ± 1.12 / 0.571 ± 0.034 \| 87.90 ± 0.78 / 0.537 ± 0.022</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该工作针对数学推理候选答案进行测试时验证，并通过复用生成器隐藏状态显著降低验证参数量与推理开销。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`73537b2e140583f04c8638301352c534d493cbfe1d5fc9a99def5691bccb8f1b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
