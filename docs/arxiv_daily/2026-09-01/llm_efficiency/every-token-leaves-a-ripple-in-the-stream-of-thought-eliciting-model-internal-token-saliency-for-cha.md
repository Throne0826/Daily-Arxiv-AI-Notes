---
title: "[论文解读] Every Token Leaves a Ripple in the Stream of Thought: Eliciting Model-Internal Token Saliency for Chain-of-Thought Compression"
description: "[arXiv 2608.31066][LLM 效率] 原文未明确报告。"
arxiv_id: "2608.31066"
announcement_date: "2026-09-01"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:41:24.574560+00:00"
source_sha256: "faf575a57aabf3d4228c29a93a89cc5628abc71025bd21117048157d2c91ceda"
tags:
  - "LLM 效率"
  - "LLM Reasoning"
  - "LLM 机制与可解释性"
  - "链式思维压缩"
  - "词元级剪枝"
  - "模型内部显著性"
  - "残差流干预"
  - "大语言模型推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2608.31066</p>

# Every Token Leaves a Ripple in the Stream of Thought: Eliciting Model-Internal Token Saliency for Chain-of-Thought Compression

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Tianyi Zhao, Yinhan He, Wendy Zheng, Chen Chen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of Virginia</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.31066v1) · [PDF 下载](https://arxiv.org/pdf/2608.31066v1) · **关键词** 链式思维压缩, 词元级剪枝, 模型内部显著性, 残差流干预, 大语言模型推理<br>


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

本文研究大语言模型的链式思维（Chain-of-Thought，CoT）压缩，具体聚焦于从完整推理链中删除部分推理词元，同时尽量保持模型的答案能力。CoT能够提升多步问题求解效果，但较长的中间推理会增加推理延迟、显存占用和服务成本；词元级压缩因此需要在给定保留预算$\gamma$下，判断完整推理链中哪些词元对目标模型最终答案的计算最重要。本文将这一选择问题表述为模型内部显著性分析：不依赖外部评分器，而是观察词元在残差流中的内部表示对正确答案似然的影响。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**链式思维（CoT）**

CoT是模型在给出最终答案前生成的一串中间推理步骤或文字。它通过显式展开推理过程帮助模型处理多步问题，但也会使输出变长、推理成本上升。

</div>
<div class="concept-item" markdown="1">

**残差流（residual stream）**

残差流是Transformer各层之间持续传递和累积信息的内部表示通道。本文把某个推理词元在残差流中的状态看作该词元向后续答案计算传递的信息，并通过干预这一状态来评估词元作用。

</div>
<div class="concept-item" markdown="1">

**词元级CoT压缩**

该任务从一条完整推理链中保留部分词元，形成较短的推理监督信号或推理轨迹。核心不是重新生成更短的答案，而是依据词元重要性在保留预算内选择应留下的内容。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个问题及其完整CoT推理链，设推理链长度为$T$，目标是在保留比例或保留预算$\gamma$下选择其中一部分推理词元，输出压缩后的CoT轨迹，并用这些轨迹适配模型以生成更短的推理链。本文假设目标模型自身的残差流包含与答案计算相关的信息；因此，对每个词元的内部残差状态进行移除或注入，可以近似衡量该词元对正确答案的贡献。重要性由两个互补问题刻画：移除该词元会使正确答案似然下降多少（必要性），以及只提供该词元的信息时能够恢复多少正确答案信号（充分性）。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$T$**

一条完整推理链中的词元数量。

</div>
<div class="notation-item" markdown="1">

**$\gamma$**

压缩时的保留预算或保留比例，用于约束最终保留的推理词元数量。

</div>
<div class="notation-item" markdown="1">

**$O(T)$**

若逐个词元进行残差干预并重新计算答案，计算成本随推理链长度$T$线性增长。

</div>
<div class="notation-item" markdown="1">

**$\rho$**

Spearman秩相关系数，用于衡量必要性排序与充分性排序之间的一致程度。

</div>

</div>

**直接相关的工作**

- **TokenSkip**: TokenSkip在词元级CoT剪枝中使用辅助的LLMLingua风格词元评分器来构造压缩推理监督。本文认为，这类外部评分的排序依赖评分器自身的训练目标、监督信号和领域假设，未必直接反映目标模型内部的答案计算，因此提出从目标模型残差流中直接评估词元重要性。
- **GoGI-Skip**: GoGI-Skip通过中间表示的梯度范数对推理内容进行评分，属于更接近模型内部的剪枝方法。本文进一步使用残差流干预定义必要性与充分性两个互补维度，并将其合并为统一排序，以避免单一启发式信号可能造成的偏差。

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

MIST（Model-Internal Saliency for Token-level CoT Compression）面向给定查询 $x$、目标模型 $M$ 生成的推理链 $c=(t_1,[0m\ldots,t_T)$ 及其答案 $a$，从模型残差流中估计每个推理词元对答案计算的内部贡献。它分别计算删除某词元内部状态后答案似然下降的必要性，以及只注入该词元内部状态后答案似然上升的充分性；随后利用层权重聚合两类信号并形成统一分数 $S_i^{\mathrm{MIST}}$，保留最高分词元构造压缩链，最后用这些压缩链通过 LoRA 适配目标模型。直观地说，MIST 不问某个词元在表面文本中“看起来是否重要”，而是观察模型自己的隐藏状态：拿走它会损失多少信息，单独提供它又能恢复多少答案信息。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成并筛选原始推理链

目标模型对每个查询生成推理链 $c=(t_1,\ldots,t_T)$ 和答案 $a$，仅保留抽取答案与金标准标签一致的链。

<div class="method-step__io" markdown="1">

**输入**：训练集查询 $x$、目标模型 $M$ 及对应金标准答案。<br>
**输出**：由正确自生成样本组成的训练链集合，每条样本包含查询、完整推理链和答案。

</div>

**直观理解**：先让待适配模型自己展示解题过程，再去掉最终答案错误的过程，避免压缩器学习错误推理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提取模型内部的双轴词元重要性

在完整链前向过程中，通过一次关于答案对数似然的反向传播计算各词元、各层的梯度与激活；在无链输入上再进行一次反向传播，分别用一阶泰勒近似估计将词元状态置零的必要性和把词元状态注入目标最终位置的充分性。

<div class="method-step__io" markdown="1">

**输入**：一条筛选后的完整链 $(x,c,a)$，以及模型各层各位置的残差流状态 $h_i^{(l)}$。<br>
**输出**：每个词元 $i$ 的逐层必要性估计 $\widehat{\phi}_i^{(l)}$ 与逐层充分性估计 $\widehat{\psi}_i^{(l)}$。

</div>

**直观理解**：同一条链只需两次反向传播，就能同时回答两个问题：删掉这个词元模型会损失什么，以及只给模型这个词元它能获得什么。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 跨层聚合并排序筛选

用各层残差更新在答案词元输出方向上的投影计算 $\bar c_l$，再对两条重要性轴进行加权聚合和归一化，按 $S_i^{\mathrm{MIST}}$ 降序排列并保留前 $\lceil\gamma T\rceil$ 个词元。

<div class="method-step__io" markdown="1">

**输入**：逐层双轴分数、各层的答案方向权重 $\bar c_l$ 和保留比例 $\gamma$。<br>
**输出**：每条原始推理链对应的压缩推理链，作为后续监督微调数据。

</div>

**直观理解**：不同网络层对答案的作用不同，因此先估计哪些层更朝向正确答案，再综合“删不得”和“单独有用”两种证据挑选词元。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### LoRA 适配与压缩推理生成

将多种 $\gamma$ 的压缩链混合为监督数据，通过 LoRA 微调目标模型；推理时加载同一个适配器，并使用与目标压缩率对应的指令控制生成长度。

<div class="method-step__io" markdown="1">

**输入**：不同保留预算下的压缩链集合、目标模型 $M$ 及训练配置。<br>
**输出**：能够生成较短推理链的适配模型及其在测试集上的答案和生成词元数。

</div>

**直观理解**：压缩器只负责制作高价值的短示范，LoRA 再教模型模仿这些示范；部署时模型可以在尽量少写步骤的同时继续解题。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 固定保留预算下的理想压缩目标

$$
c_{\gamma}^{\star}=\arg\max_{c^{\prime}\subseteq c,\ |c^{\prime}|=\lceil\gamma T\rceil}\log p_{M}(a\mid x,c^{\prime})
$$

**符号说明**

- $c_{\gamma}^{\star}$：在保留预算 $\gamma$ 下，使目标模型正确答案对数似然最大的理想压缩链。
- $c$：完整推理链，由词元 $t_1,\ldots,t_T$ 构成。
- $c^{\prime}$：从完整链中选择出的候选词元子集或压缩链。
- $\gamma$：保留比例，取值为 $(0,1]$。
- $T$：完整推理链的词元数。
- $p_M(a\mid x,c^{\prime})$：模型 $M$ 在查询 $x$ 和候选压缩链 $c^{\prime}$ 条件下生成答案 $a$ 的概率。

<div class="equation-explanation" markdown="1">

**直观理解**：这个目标直接寻找“在固定长度下仍最支持正确答案”的词元组合，但枚举所有子集的计算量呈组合爆炸。因此 MIST 用每个词元的内部显著性分数近似这个难以直接求解的全局选择问题。<br>
**原文位置**：第 3.1 节，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 统一 MIST 词元分数

$$
S^{\textsc{MIST}}_{i}=\alpha\cdot\widehat{\phi}_{i}+(1-\alpha)\cdot\widehat{\psi}_{i},\quad \alpha\in[0,1]
$$

**符号说明**

- $S^{\textsc{MIST}}_{i}$：第 $i$ 个推理词元的最终 MIST 显著性分数。
- $\widehat{\phi}_{i}$：第 $i$ 个词元聚合后的必要性显著性，反映移除其内部贡献造成的答案信息损失。
- $\widehat{\psi}_{i}$：第 $i$ 个词元聚合后的充分性显著性，反映单独提供其内部状态带来的答案似然增益。
- $\alpha$：必要性与充分性之间的权衡超参数。

<div class="equation-explanation" markdown="1">

**直观理解**：分数将两个互补指标合成一个可排序的数：$\alpha$ 较大时更重视完整推理中不可缺少的词元，较小时更重视单个词元本身能携带的答案相关信息。论文说明两种排名相关性较弱，因此合并比只使用任一轴更完整。<br>
**原文位置**：第 3.3 节，公式（8）；逐层聚合见公式（7）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：压缩阶段的理想目标是最大化 $\log p_M(a\mid x,c^{\prime})$，即在固定保留预算下保留最能支持目标模型正确答案的词元；实际算法不直接优化所有词元子集，而是以残差流干预得到的 $S_i^{\mathrm{MIST}}$ 进行排序。得到压缩链后，训练阶段采用监督微调：目标模型学习在查询和压缩推理示范条件下生成推理链及答案。具体优化器损失的逐项形式原文未明确报告；论文明确说明使用 LoRA 适配器，并在多个保留预算的压缩链混合数据上训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 残差流干预与双轴显著性**

残差流被视为模型内部的信息传递载体。必要性通过将完整链中第 $i$ 个词元在各层的源状态 $h_i^{(l),\mathrm{src}}$ 置零来定义；充分性则把该源状态与无链前向在最终位置的目标状态 $h_{\mathrm{final}}^{(l),\mathrm{tgt}}$ 之间的差异注入目标位置。两种干预均以答案对数似然为行为读出，并用梯度与干预方向的内积作一阶近似。

> 直观理解：残差流可以理解为模型逐层传递和改写的工作记忆。必要性检查“拿走后会不会变差”，充分性检查“单独给它能不能帮上忙”；两者互补，避免只奖励某一种类型的词元。

**2. Logit-lens 层加权聚合**

对每层 $l$，计算该层残差更新 $h_t^{(l)}-h_t^{(l-1)}$ 与答案词元对应反嵌入行 $W_U[a]$ 的平均内积 $\bar c_l$，以此衡量该层更新将链表示推向答案的程度。随后分别按 $\bar c_l$ 聚合 $|\widehat{\phi}_i^{(l)}|$ 和 $|\widehat{\psi}_i^{(l)}|$，而不是简单平均所有层。

> 直观理解：有些层主要处理低层语言形式，有些层更直接参与答案形成。这个权重让更贴近答案方向的层对词元评分影响更大。

**3. 统一分数与预算化保留**

分别聚合并归一化必要性和充分性后，用超参数 $\alpha\in[0,1]$ 对两轴线性组合得到 $S_i^{\mathrm{MIST}}$。给定预算 $\gamma\in(0,1]$，算法按统一分数选择恰好 $\lceil\gamma T\rceil$ 个词元；论文给出的压缩链定义为从完整链中选取固定数量词元的最优子集近似。

> 直观理解：最终排名像一个同时看“不可删性”和“独立信息量”的投票器。预算决定保留多少词元，MIST 决定具体保留哪些词元。

**训练与推理**

训练过程分为三阶段。首先，对每个模型与数据集组合在训练查询上贪心自生成 CoT，并筛选答案正确的链；其次，对每条保留链执行 MIST 评分：完整链前向及答案对数似然反向传播提供源激活和必要性梯度，无链输入的答案对数似然反向传播提供目标最终位置梯度，随后计算逐层双轴分数、层权重和统一词元排名；最后，对 $\gamma\in\{0.5,0.6,0.7,0.8,0.9,1.0\}$ 的压缩链进行混合，训练一个 LoRA 适配器。

推理时不重新为测试样本逐词元计算 MIST 分数，而是加载已训练适配器，在测试查询上贪心生成。通过前置“Please reduce $(1-\gamma)\times100\%$ of the words in your CoT”指令控制期望压缩程度；同一适配器在不同预算下复用。训练时的链保留比例 $\gamma$ 与最终生成词元相对于完整链基线的实际压缩率并不必然相同，因为适配器会学习自己的长度策略。

**复现信息**

为复现核心方法，需要保留以下与结果解释直接相关的设置：每条链的 MIST 评分使用两次反向传播，因梯度可同时暴露所有词元和层的位置，所以评分开销不随链长 $T$ 线性增加额外前向次数。完整链评分使用源答案对数似然 $\log p_M(a\mid x,c)$，无链评分使用 $\log p_M(a\mid x,\emptyset)$；源激活和层权重均来自同一次完整链前向。

为保证比较公平，所有评分器复用同一组一次性自生成且答案正确的推理链，差异主要归因于词元选择阶段。LoRA 训练覆盖全部线性投影，并使用固定的统一训练流程；推理和自生成均采用贪心解码。需要注意，MIST 的理论干预是将隐藏状态置零或补丁注入，而实际大规模评分采用相应的梯度—激活一阶线性近似；论文将完整泰勒展开和余项界放在附录 D。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：小学数学文字题，使用标准训练集和测试集；规模为训练 7,473、测试 1,319。它主要检验方法在相对规则的算术多步推理上的压缩能力。原文说明："We use the standard train and test splits from the GSM8K release without further filtering."（Appendix A，GSM8K）
- MATH：更具挑战性的竞赛数学题；训练集由 Hendrycks 的七个学科合并而成，测试集使用 MATH-500，规模为训练 7,500、测试 500。它用于检验方法对较长、较复杂数学推理链的适应性。原文说明："The training set is the concatenation of the seven Hendrycks subjects; the test set is the canonical MATH-500 subset."（Appendix A，MATH）
- MMLU-Pro 与 BBH-MC：前者是多学科专业知识与推理任务，原始数据没有标准训练集，作者将 12,032 个测试样本随机划分为训练 10,501、评估 1,531；后者选用 BIG-Bench Hard 中 17 个字母式多选子任务，将 4,074 个样本按 80/20 划分为训练 3,258、评估 816。两者共同检验方法跨学科、常识和逻辑多选推理的泛化能力。由于任务限制最多列出三个数据集，此处将 MMLU-Pro 与 BBH-MC 合并描述。原文说明："We therefore randomly partition the 12,032 examples into 10,501 training and 1,531 evaluation examples."（Appendix A，MMLU-Pro）；"we randomly partition the available examples into 3,258 training and 816 evaluation examples (80/20 split)."（Appendix A，BBH-MC）

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

模型在测试集上给出正确答案的比例，用于衡量压缩后推理能力是否保持。 （越高越好；在相同压缩率下更高表示保留 token 更有助于正确求解。）

</div>
<div class="metric-item" markdown="1">

**Compression rate**

相对于完整 CoT LoRA 基线，微调适配器在推理时生成 token 总量的相对减少比例。它衡量推理成本节约，而不是训练数据中直接保留的 token 比例。 （越高越节省推理 token；但必须结合 Accuracy 解读，单独提高压缩率可能意味着能力损失。）

</div>
<div class="metric-item" markdown="1">

**Per-batch wall-clock decoding time**

测试集生成阶段每个 batch 的实际解码耗时，用于把 token 数量压缩转化为可观察的推理时间成本。 （越低越好；它受硬件、批大小和实现影响，因此不能完全等同于理论 token 节省。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Full-chain：保留完整 CoT，不进行 token 选择；LoRA 在未修改的自生成链上微调。它提供性能上限，用于判断压缩是否造成损失。No-chain：只保留最终答案、完全移除推理链；它提供极端压缩对照，用于判断中间推理 token 是否有实际价值。
- Uniform：在每个保留率 $\gamma$ 下随机保留 $\lceil\gamma T\rceil$ 个 token。它检验 MIST 的收益是否只是来自保留了相同数量的 token，而不是来自更准确的选择。
- TokenSkip：使用预训练 LLMLingua-2 分类器作为外部 token 重要性评分器，并保留得分最高的 $\lceil\gamma T\rceil$ 个 token。它是与 MIST 最直接的外部评分比较，检验模型内部信号是否优于外部压缩器。
- GoGI-$\ell_1$、Perplexity、Attention rollout 与 H2O：这些方法分别代表单层梯度范数、自信息、跨层注意力传播和回答位置接收的累计注意力。它们覆盖梯度、语言模型不确定性和注意力启发式信号；原文共比较九个 baseline，但此处合并列出其余四类以满足最多四项比较项。

**实验想回答的问题**

- 在相同自生成推理链、微调配方和评测协议下，基于模型内部显著性的 MIST 是否比外部分类器、梯度、注意力或启发式打分方法更有效地选择应保留的 CoT token？
- 在不同推理数据集、目标模型和 token 保留率下，MIST 能否在降低推理 token 成本的同时维持任务准确率，并且其 necessity 与 sufficiency 设计是否确实有助于压缩效果？

**实验实现**

实验采用三阶段流程。第一阶段，对每个模型—数据集组合在训练集上贪心生成 CoT，仅保留抽取答案与金标准一致的链；同一批自生成链被所有评分器复用，以隔离评分方法的影响。第二阶段，对每条保留链用 MIST 或 baseline 计算 token 分数，并在 $\gamma\in\{0.5,0.6,0.7,0.8,0.9\}$ 下保留每条链的前 $\lceil\gamma T\rceil$ 个 token。第三阶段，在压缩链上用 LoRA 微调目标模型，并在测试集上贪心解码。训练时实际混合 $\gamma\in\{0.5,0.6,0.7,0.8,0.9,1.0\}$ 的样本；推理时通过统一的 Please reduce 指令控制目标长度，而不是为每个 $\gamma$ 单独训练适配器。LoRA 使用秩 $r=8$、缩放 $\alpha=16$、学习率 $5\times10^{-5}$、3 个 epoch、有效 batch size 8 和上下文长度 2,048。自生成与评测使用贪心解码、temperature 0、top-p 1.0；自生成和评测采用 bfloat16 与 SDPA，MIST 评分阶段改用 eager attention 和 float32 以保持梯度稳定。所有实验运行在 2 张 NVIDIA A100 80GB GPU 上。需要区分：训练保留率 $\gamma$ 是构造监督数据时保留的 CoT 比例，报告的 inference compression rate 是相对完整链适配器的实际生成长度下降，两者不必相等。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：MIST uses residual-stream saliency to identify and prune reasoning tokens, centrally combining efficient CoT inference, reasoning-trace compression, and internal attribution.; rule check: matched taxonomy keywords; top rule score=6.0
- 全文指纹：`faf575a57aabf3d4228c29a93a89cc5628abc71025bd21117048157d2c91ceda`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
