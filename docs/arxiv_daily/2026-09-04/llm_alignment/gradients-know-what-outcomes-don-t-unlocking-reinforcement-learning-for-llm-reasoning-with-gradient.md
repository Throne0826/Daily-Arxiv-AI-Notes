---
title: "[论文解读] Gradients Know What Outcomes Don't: Unlocking Reinforcement Learning for LLM Reasoning with Gradient-Aligned Rewards"
description: "[arXiv 2609.03342][对齐 / RLHF] 原文未明确报告。"
arxiv_id: "2609.03342"
announcement_date: "2026-09-04"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:36:26.781604+00:00"
source_sha256: "bff3a7cb85cb660061e24f9fd6089e9d1bd392923e27e8581cece1691149afd1"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "强化学习从可验证奖励（RLVR）"
  - "大语言模型推理"
  - "链式思维"
  - "信用分配"
  - "梯度对齐奖励（GAR）"
  - "过程级奖励"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2609.03342</p>

# Gradients Know What Outcomes Don't: Unlocking Reinforcement Learning for LLM Reasoning with Gradient-Aligned Rewards

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Leqi Zheng, Jinbo Su, Fang Niu, Chaokun Wang, Weiping Wang, Jiajun Zhang, Shannan Yan, Jie Wu, Zhaolu Kang, Rong Fu, Hang Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Tsinghua University；Affiliation: Renmin University of China；Affiliation: Institute of Information Engineering, CAS；Affiliation: The Australian National University；Affiliation: Peking University；Affiliation: University of Macau</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03342v1) · [PDF 下载](https://arxiv.org/pdf/2609.03342v1) · **关键词** 强化学习从可验证奖励（RLVR）, 大语言模型推理, 链式思维, 信用分配, 梯度对齐奖励（GAR）, 过程级奖励<br>
**代码**: [https://github.com/LQgdwind/GAR](https://github.com/LQgdwind/GAR)

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

本文位于大语言模型推理强化学习领域，重点讨论如何为链式思维生成提供比最终答案正确性更细致的奖励信号。强化学习从可验证奖励（RLVR）通常让策略模型生成推理轨迹，并由规则或验证器检查最终答案：答案正确得到正奖励，答案错误得到零奖励。该设定能够诱导模型形成结构化推理，但二元结果奖励无法区分多个都答对的问题解法，因此正确轨迹之间缺少进一步的优化方向。本文研究的基本背景是：在不依赖额外在线评审器或大规模离线步骤标注的条件下，如何利用训练语料中已有的专家链式思维，为当前策略产生更有区分度的奖励。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**强化学习从可验证奖励（RLVR）**

RLVR让语言模型生成回答，再用能够自动检查最终答案的验证器提供奖励，而不是依赖人工逐步评价。本文中该奖励主要是二元的：最终答案正确或错误。

</div>
<div class="concept-item" markdown="1">

**信用分配问题**

信用分配问题是指最终结果已知，但难以判断生成过程中的哪些动作或推理步骤真正促成了结果。若多个轨迹都获得相同正确奖励，策略梯度就难以优先强化其中质量更高的轨迹。

</div>
<div class="concept-item" markdown="1">

**过程级奖励与策略梯度**

过程级奖励在生成过程中提供比最终答案更细的反馈，例如评价推理步骤或整条轨迹的质量。策略梯度则根据奖励调整模型参数，使高奖励轨迹在未来更可能被生成；本文进一步比较轨迹对应的梯度方向与专家参考梯度的接近程度。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个数学或知识推理问题、一个正在优化的语言模型策略，以及训练语料中与该问题配套的专家链式思维解答，模型首先按当前策略生成若干候选推理轨迹。最终答案验证器输出结果正确性，作为基本的结果门控；对于正确轨迹，本文方法进一步利用策略在输出投影层产生的截断反向传播梯度，与专家解答产生的锚点梯度进行比较，从而形成稠密的、推理感知的奖励；错误轨迹无论其梯度方向如何都被门控为零。训练目标仍是在线强化学习：输入是问题和专家参考解答，输出是带有结果正确性约束及梯度对齐信号的轨迹奖励，并据此更新策略。其关键假设是，专家解答在模型自身梯度空间中能够提供有用的参考方向，而不必把专家解答直接当作固定的蒸馏目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathbf{v}_{a}$**

专家锚点梯度向量，即专家链式思维经过模型输出投影层反向传播后得到的参考梯度方向。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{v}$**

某条候选生成轨迹对应的梯度向量，用于与专家锚点梯度进行方向比较。

</div>
<div class="notation-item" markdown="1">

**$r$**

一条候选轨迹获得的奖励；在本文设定中，错误轨迹被结果门控为零，正确轨迹还可依据梯度与专家锚点的对齐程度获得额外信号。

</div>
<div class="notation-item" markdown="1">

**$\cos(\mathbf{v},\mathbf{v}_{a})$**

候选轨迹梯度与专家锚点梯度之间的余弦相似度，衡量两者方向的接近程度；数值越高表示梯度更新方向越一致。

</div>

</div>

**直接相关的工作**

- **RLVR与GRPO等结果奖励方法**: 这类方法证明仅凭最终答案的可验证奖励也能诱导大语言模型产生链式思维，但二元奖励会让所有正确轨迹获得相同反馈，使正确轨迹之间的组内优势趋近于零。GAR保留结果验证这一可靠门控，同时在正确轨迹之间加入梯度对齐信号。
- **过程奖励模型（PRM）**: PRM通过步骤级反馈提供更稠密的监督，但通常需要大规模专家步骤标注，或依赖在固定数据分布上离线训练的独立验证器。GAR不训练外部评审模型，而是使用训练语料已有的专家链式思维作为梯度空间锚点，并直接在当前策略的在线生成循环中计算奖励。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在利用可验证奖励进行大语言模型推理训练时，系统通常只检查最终答案是否正确，并据此给予二元奖励。这样可以推动模型产生较长的思维链，却无法区分多个同样答对的问题解答：有的解答推理清晰、步骤可靠，有的解答可能依赖偶然猜测或包含脆弱的中间过程。结果是，训练信号难以进一步把策略引向更高质量、更可复用的推理轨迹，形成典型的信用分配问题。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **结果奖励与基于表面规则的奖励塑形**：结果奖励只根据最终答案是否正确赋予二元信号；规则塑形则额外利用长度、格式等可观察特征调整奖励。这些方法实现简单，并且不需要逐步标注，但前者把所有正确轨迹视为等价，后者主要判断输出的外在形式，而不是思维链是否真正使用了任务所需的推理结构。
- **过程奖励模型（PRM）及其自动化变体**：过程奖励模型尝试对思维链中的中间步骤提供逐步反馈，以此改善信用分配；自动化变体则用程序或模型生成过程标签，减少人工标注。这类方法原则上能够提供比最终结果更细粒度的监督，但通常依赖大量专家过程标注，或在离线、固定的数据分布上训练一个独立的奖励模型。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 结果奖励的正确子集内部没有区分度：当多个采样轨迹都得到正确答案时，它们的奖励相同，因而组内相对优势趋近于零，策略梯度缺少选择更优推理过程的依据。与此同时，数学训练语料中已经存在的专家思维链没有被转化为奖励信号。
- 过程级替代方案在成本或适应性上存在缺陷：人工过程奖励模型需要昂贵的大规模专家标注，自动化方案又通常基于固定分布离线训练，可能与训练过程中持续变化的策略分布不一致；表面启发式方法虽然便宜，却不能可靠衡量真实推理质量。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚未解决的空白是：如何在不依赖昂贵离线过程标注的前提下，直接利用训练语料中已有的专家思维链，为当前策略生成的每条轨迹提供能够区分推理质量的稠密、过程感知奖励，并使该信号适应策略本身的变化。关键缺口不只是增加奖励密度，而是找到一种既使用专家信息、又与策略更新机制处于同一表示空间的评价方式。

</div>
<div markdown="1"><span>核心问题</span>

能否把专家思维链转化为策略梯度空间中的参考方向，再用当前策略对候选轨迹产生的梯度与该参考方向之间的对齐程度，构造一种低额外成本且能够区分正确推理轨迹质量的奖励？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把“这条轨迹应当如何改变模型”作为质量线索，而不只看它最终是否答对。对专家解答和模型 rollout 分别计算输出投影层的截断梯度，可以得到它们对模型参数更新的方向；如果某条正确轨迹诱导的更新方向与专家轨迹相近，说明二者在预测误差和激活模式上可能具有相似的推理结构，因此应获得更高奖励。用余弦相似度比较方向还能削弱梯度绝对规模差异的影响；再对错误答案进行结果正确性门控，则可避免一条方向上看似相似但最终错误的轨迹获得奖励。直观地说，该方法不是询问“答案对不对”或“文字像不像好解答”，而是询问“这条轨迹会把模型往专家解答所代表的学习方向推动多少”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

GAR（Gradient-Aligned Reward，梯度对齐奖励）是嵌入 GRPO 或 REINFORCE++ 训练步骤中的在线奖励塑形机制。对每个提示 $x$，策略 $pi_{\theta}$ 生成 $K$ 条候选回答；结果验证器先筛出答案正确且格式有效的回答。GAR 随后以教师强制方式分别处理这些回答和数据集自带的专家思维链 $a(x)$，冻结 Transformer 主体，只在输出投影层边界计算截断梯度，并将梯度与隐藏激活逐元素相乘、跨 token 平均和归一化，得到紧凑向量 $\mathbf{v}_i$ 与锚点向量 $\mathbf{v}_a$。二者的余弦相似度经过正确回答组内中心化、非负裁剪和缩放后叠加到二元正确性奖励上，再由原有强化学习优化器计算优势并更新策略。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选生成与结果门控

策略为每个提示采样 $K$ 条回答 $\{y_1,\ldots,y_K\}$，验证器依据最终答案与格式将其划分为正确子集 $\mathcal{P}(x)$ 和未通过子集。未通过回答不执行梯度提取，只获得格式惩罚 $p(y_i)$。

<div class="method-step__io" markdown="1">

**输入**：当前策略 $\pi_{\theta}$、提示 $x$、每个提示对应的专家思维链 $a(x)$，以及结果验证器。<br>
**输出**：通过验证的候选回答集合 $\mathcal{P}(x)$，以及未通过回答的低奖励。

</div>

**直观理解**：验证器相当于第一道硬门槛：GAR 只在“答案已经正确”的解法之间比较推理质量，而不会奖励答案错误但梯度偶然相似的轨迹。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 截断反向传播与梯度—激活表征

模型以教师强制方式前向计算，在输出投影层输入处截取并停止梯度传播的隐藏状态 $\widetilde{\mathbf{h}}_t$；仅通过语言模型头计算交叉熵对该隐藏状态的梯度 $\mathbf{G}_t$。将 $\mathbf{G}_t$ 与 $\widetilde{\mathbf{h}}_t$ 逐元素相乘，随后跨位置平均并作 $L_2$ 归一化。

<div class="method-step__io" markdown="1">

**输入**：一个通过验证的回答 $y_i$、其响应或显式思考区间 $\mathcal{T}_{y_i}$，以及当前模型的输出投影参数 $W_o,\mathbf{b}_o$。<br>
**输出**：每条正确回答对应的 $d$ 维单位向量 $\mathbf{v}_i$。

</div>

**直观理解**：该步骤不追踪整个模型如何变化，只观察输出层附近哪些隐藏维度既被强烈激活、又会显著影响预测损失，因此比完整反向传播便宜，也比只看措辞更接近模型内部的计算模式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 专家锚点构建与缓存

对 $a(x)$ 执行与候选回答完全相同的教师强制、截断梯度和梯度—激活聚合流程，得到单位向量 $\mathbf{v}_a$。锚点向量在该提示的 rollout 组内缓存，供全部 $K$ 条候选共享。

<div class="method-step__io" markdown="1">

**输入**：同一提示的数据集专家思维链 $a(x)$ 和当前策略参数。<br>
**输出**：提示级专家梯度锚点 $\mathbf{v}_a$。

</div>

**直观理解**：专家解答被转换为模型自身坐标系中的参考方向；缓存意味着同一道题的参考答案只计算一次，而不必为每条候选重复计算。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 梯度对齐评分与奖励塑形

以单位向量内积 $b(y_i)=\mathbf{v}_i^{\top}\mathbf{v}_a$ 计算余弦对齐度，再减去正确子集中的平均对齐度；仅保留非负部分并乘以 $\beta$，叠加到基础正确性奖励上。

<div class="method-step__io" markdown="1">

**输入**：正确候选向量 $\mathbf{v}_i$、专家锚点 $\mathbf{v}_a$、基础正确性奖励 $r_{\mathrm{base}}$、权重 $\beta$ 和格式惩罚 $p(y_i)$。<br>
**输出**：每条 rollout 的最终奖励 $r_{\mathrm{GAR}}(x,y_i)$。

</div>

**直观理解**：所有正确答案仍有相同的及格分，但比同组其他正确解法更接近专家内部方向的回答会获得额外加分；低于组内平均值的正确回答不会被扣到二元奖励基线以下。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 截断梯度—激活向量

$$
\mathcal{L}_{\mathrm{tr}}(x,y)=\frac{1}{|\mathcal{T}_{y}|}\sum_{t\in\mathcal{T}_{y}}\ell\!\left(W_o\widetilde{\mathbf{h}}_t+\mathbf{b}_o,\,y_{t+1}\right),\quad \mathbf{G}_t=\frac{\partial\mathcal{L}_{\mathrm{tr}}}{\partial\widetilde{\mathbf{h}}_t},\quad \mathbf{S}_t=\mathbf{G}_t\odot\widetilde{\mathbf{h}}_t,\quad \bar{\mathbf{s}}=\frac{1}{|\mathcal{T}_{y}|}\sum_{t\in\mathcal{T}_{y}}\mathbf{S}_t,\quad \mathbf{v}=\frac{\bar{\mathbf{s}}}{\|\bar{\mathbf{s}}\|_2}
$$

**符号说明**

- $\mathcal{L}_{\mathrm{tr}}$：仅通过输出投影层计算的教师强制平均交叉熵损失。
- $\mathcal{T}_{y}$：回答 $y$ 的响应 token 区间；若文本显式分隔思考部分，则可指思考区间。
- $\widetilde{\mathbf{h}}_t$：位置 $t$ 处从 Transformer 主体截取并停止梯度传播的 $d$ 维隐藏状态。
- $W_o,\mathbf{b}_o$：语言模型输出投影层的权重和偏置。
- $y_{t+1}$：位置 $t$ 所预测的下一 token 目标。
- $\mathbf{G}_t$：截断损失相对于隐藏状态 $\widetilde{\mathbf{h}}_t$ 的梯度，即局部损失敏感度。
- $\odot$：逐元素乘法。
- $\mathbf{S}_t$：位置 $t$ 的梯度—激活信号。
- $\bar{\mathbf{s}},\mathbf{v}$：分别表示跨 token 平均后的信号及其 $L_2$ 归一化单位向量。

<div class="equation-explanation" markdown="1">

**直观理解**：该式先计算每个响应 token 的预测误差如何影响输出层输入，再用隐藏激活对梯度逐维加权，最后将整条回答压缩为一个方向向量。跨位置平均减少长度差异，归一化消除尺度漂移，使不同回答之间可以直接用余弦比较。<br>
**原文位置**：第 2.2 节，式（2）—（4）；梯度—激活定义见式（3），向量聚合见式（4）

</div>

</div>

<div class="equation-block" markdown="1">

#### 门控、中心化和非负裁剪的 GAR 奖励

$$
b(y_i)=\mathbf{v}_i^{\top}\mathbf{v}_a,\quad \widehat{b}(y_i)=b(y_i)-\frac{1}{|\mathcal{P}(x)|}\sum_{y_j\in\mathcal{P}(x)}b(y_j),\quad r_{\mathrm{GAR}}(x,y_i)=\begin{cases}r_{\mathrm{base}}+\beta\max\!\left(0,\widehat{b}(y_i)\right)+p(y_i),&r_{\mathrm{raw}}(x,y_i)>0,\\p(y_i),&\text{otherwise.}\end{cases}
$$

**符号说明**

- $\mathbf{v}_i$：第 $i$ 条通过验证的候选回答的归一化梯度—激活向量。
- $\mathbf{v}_a$：同一提示对应专家思维链的归一化梯度—激活锚点。
- $b(y_i)$：候选与专家锚点的余弦对齐分数；因两向量均已归一化，它等于内积。
- $\mathcal{P}(x)$：提示 $x$ 的 rollout 组中通过结果验证的正确回答子集。
- $\widehat{b}(y_i)$：候选对齐分数减去正确子集平均分所得的组内相对对齐度。
- $r_{\mathrm{raw}}$：结果验证器给出的二元正确性奖励。
- $r_{\mathrm{base}}$：正确回答的基础奖励，文中默认值为 $1.0$。
- $\beta$：梯度对齐奖励的缩放系数，文中默认值为 $0.5$。
- $p(y_i)$：违反规定思考/答案格式时施加的非正惩罚。

<div class="equation-explanation" markdown="1">

**直观理解**：该奖励先保留结果正确性这一硬条件，再只给对齐度高于同题正确回答平均值的轨迹增加奖励。中心化制造了正确轨迹之间原本缺失的组内差异，非负裁剪则保证对齐项不会把任何正确轨迹压到仅使用结果奖励时的基线以下。<br>
**原文位置**：第 2.3 节，式（5）—（6）；完整在线流程见附录 B 算法 1

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：GAR 本身不是新的策略梯度目标，而是替换或扩充优化器输入的标量奖励。标准二元验证中，同一组内所有正确回答都获得相同奖励，当正确数量 $K_c$ 接近 rollout 数 $K$ 时，GRPO 难以从正确轨迹之间形成有信息量的相对优势；GAR 用 $\beta\max(0,\widehat{b}(y_i))$ 引入组内差异，使与专家梯度方向更一致的正确轨迹获得更大的优势。随后仍由 GRPO 或 REINFORCE++ 按其原有目标计算优势、重要性比率或策略梯度并更新 $\theta$，因此 GAR 改变的是“学习信号偏好什么”，而不是“优化器如何执行更新”。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 结果验证器门控**

二元奖励定义为 $r_{\mathrm{raw}}(x,y)=\mathbf{1}[\operatorname{Verify}(x,y)]$。只有 $r_{\mathrm{raw}}>0$ 且格式有效的回答进入梯度对齐计算，错误或格式异常回答直接获得 $p(y)\leq 0$；这既阻止策略利用无意义梯度方向骗取奖励，也把额外计算限制在正确轨迹上。

> 直观理解：梯度相似只能回答“像不像专家”，不能保证答案正确，因此验证器负责真实性，GAR 只负责对已经正确的解法进行细分。

**2. 输出层截断梯度—激活编码器**

该模块通过 forward pre-hook 捕获 $\mathbf{H}\in\mathbb{R}^{n\times d}$，将其 detach 后只经过 $W_o$ 与 $\mathbf{b}_o$ 计算损失；对每个位置形成 $\mathbf{S}_t=\mathbf{G}_t\odot\widetilde{\mathbf{h}}_t$，再平均和归一化为 $\mathbf{v}\in\mathbb{R}^{d}$。作者以“损失敏感度乘激活强度”刻画各隐藏维度对当前序列预测的局部贡献，并用截断计算代替维度为 $|\theta|$ 的完整参数梯度。

> 直观理解：原始梯度只说明改变某一维会怎样，激活只说明某一维用了多少；两者相乘保留“既被使用又影响预测”的维度，从而降低表面措辞和无关噪声的影响。

**3. 专家锚点对齐与组内奖励塑形**

候选与专家向量均经 $L_2$ 归一化，因此内积就是余弦相似度。GAR 在同一提示的正确子集 $\mathcal{P}(x)$ 内对该分数中心化，并通过 $\max(0,\cdot)$ 只奖励高于正确组平均水平的轨迹；专家锚点按提示缓存，无需额外标注或外部奖励网络。

> 直观理解：绝对余弦值可能随题目难度和模型状态变化，组内中心化改为比较同一道题中谁更接近专家；非负裁剪则使奖励塑形只增加优质正确解法的奖励，而不削弱其他正确解法原有的正确性奖励。

**训练与推理**

训练时，从基础模型直接进行全参数强化学习，不要求先做监督微调。每一步先为每个提示生成 $K$ 条 rollout，执行答案与格式验证；对通过者提取候选梯度—激活向量，并按需计算和缓存该提示的专家锚点，随后生成组内中心化的 GAR 奖励并交给 GRPO 或 REINFORCE++ 更新模型。由于锚点来自训练语料已有的思维链，GAR 不训练额外的 Judge 或过程奖励模型；锚点只在当前 rollout 组内缓存，因为模型参数更新后其梯度表征也可能变化。推理时无需验证器、专家锚点、梯度提取或 GAR 奖励，训练后的语言模型按普通自回归方式直接生成答案，因此 GAR 不增加部署阶段的模型结构或推理计算。

**复现信息**

论文在 SLIME/Megatron 训练栈中将 GAR 实现为 GRPO 优势计算前的在线 reward hook，并在 Qwen3-4B-Base 与 Qwen3-8B-Base 上从基础检查点进行全参数强化学习。训练使用约 $10{,}000$ 个 NuminaMath-CoT 问题，每题自带的思维链作为 $a(x)$；共训练 $400$ 步，批大小为 $128$，每题采样 $K=16$ 条轨迹，即门控前每步有 $2{,}048$ 条候选。默认设置为 $\beta=0.5$、最大 GAR 处理跨度 $L=768$ token、激活阈值 $\tau_a=0.05$ 和锚点过滤参数 $p_f=0.7$。复现时最关键的公平性条件是：候选与锚点必须使用同一当前策略、同一截断梯度流程和相同 token 区间规则；隐藏状态须在输出投影边界 detach，错误回答须在梯度计算前过滤，且同题锚点应在 rollout 组内复用。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 竞赛数学基准组：IMO-AnswerBench、HMMT 2026、HMMT 2025 与 AIME 2026，用于检验模型在高难度数学推理上的分布内效果。原文节选未给出各基准的题目规模、数据划分及是否存在训练集重叠，因此这些信息仍需核对全文。
- GPQA Diamond：高难度科学问答基准。模型仅使用数学数据训练后进行零样本评测，用于判断 GAR 学到的能力是否能从数学推理迁移到科学推理；原文节选未报告样本规模或具体分数。
- MMLU-Pro：覆盖多学科知识与推理的综合基准。这里同样采用仅在数学数据上训练、随后零样本评测的设置，用于检验跨领域迁移；原文节选未报告样本规模或具体分数。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Pass@$k$**

对每道题采样 $k$ 个回答，只要至少一个回答正确，该题就计为成功。Pass@1 更接近单次生成的实际正确率；较大的 $k$ 更强调候选集合对正确解法的覆盖能力。 （越高越好，因为它表示在给定采样预算内找到至少一个正确答案的概率更大。）

</div>
<div class="metric-item" markdown="1">

**Maj@16**

从 16 个采样回答中按答案多数投票得到最终预测，再计算其正确率；GPQA Diamond 使用该指标衡量多次采样后的集成稳定性。 （越高越好，因为多数投票后的最终答案更常正确。）

</div>
<div class="metric-item" markdown="1">

**微平均 Pass@1**

MMLU-Pro 上按所有样本汇总计算单次生成正确率，而不是先对不同类别分别求平均；它反映整体样本层面的零样本准确性。 （越高越好，因为单次回答正确的总体比例更高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3-4B 与 Qwen3-8B，在四个竞赛数学基准上将 GAR 叠加到对应基础优化器。

<div class="result-value" markdown="1">

作者报告，GAR 在所有“基准—模型”组合上都优于对应基础优化器；最大 Pass@1 相对增益为 52.4%，出现在 Qwen3-4B 的 HMMT 2025 设置。由于节选没有给出表 2 的完整逐项数值，无法据此复核所有组合的绝对提升幅度。

</div>

这说明 GAR 的收益并非只出现在某一个数据集或模型规模上，而且低 $k$ 下的改善意味着正确解答被分配了更高生成概率，而不只是偶然增加了少量可被大规模采样发现的正确路径。不过，“所有组合均改善”仍局限于文中选择的两个 Qwen3 规模和四个数学基准，不能直接推出对其他模型家族也普遍有效。

<div class="result-source" markdown="1">

来源：第 5.1 节 Main Results，表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GAR improves over the corresponding base optimizer on every benchmark–model combination, with relative gains of up to 52.4% at pass@1 (HMMT 2025, 4B).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### GAR-GRPO 对比 GRPO，分别使用 Qwen3-4B 与 Qwen3-8B，在 HMMT 2026 和 HMMT 2025 上评测 Pass@1。

<div class="result-value" markdown="1">

在 4B 模型上，HMMT 2026 的 Pass@1 从 2.42 提高到 3.18，HMMT 2025 从 3.83 提高到 5.00，相对提升分别为 31.4% 和 30.5%；在 8B 模型上，相应比较从 4.24 提高到 5.15、从 4.50 提高到 6.00。

</div>

这组直接配对结果表明，GAR 在更大模型上仍有正收益，不是仅对容量较小的模型有效。它还说明增益来自同一优化器上的奖励替换或增强，而不是更换了训练算法。但这些绝对准确率仍然较低，因此结果支持“稳定改善”，并不意味着模型已经解决了这些高难度竞赛任务。

<div class="result-source" markdown="1">

来源：第 5.1 节 Main Results，表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For GAR-GRPO at the 4B scale, pass@1 increases from 2.42 to 3.18 on HMMT 2026 and from 3.83 to 5.00 on HMMT 2025, corresponding to relative gains of 31.4% and 30.5%, respectively. The same comparisons at the 8B scale increase from 4.24 to 5.15 and from 4.50 to 6.00, showing that the benefit persists as model capacity grows.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 将 GAR 叠加到 REINFORCE++，并与原始 REINFORCE++ 比较；重点观察 Qwen3-4B 在 HMMT 2025 上的 Pass@1。

<div class="result-value" markdown="1">

GAR-REINFORCE++ 在该设置下将 Pass@1 从 3.17 提高到 4.83；作者称这是所报告结果中的最大相对增益，并认为 GAR 在 REINFORCE++ 上取得了与 GAR-GRPO 相近的改善。

</div>

这一结果用于检验 GAR 与策略优化器是否可分离：同一种梯度对齐奖励在 GRPO 之外仍然有效，支持其作为奖励层组件的定位。它不能单独证明 GAR 对任意强化学习优化器都有效，因为节选只明确展示了 GRPO 和 REINFORCE++ 两类优化器。

<div class="result-source" markdown="1">

来源：第 5.1 节 Main Results，表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The largest relative gain occurs for GAR-REINFORCE++ on HMMT 2025 at the 4B scale, where pass@1 rises from 3.17 to 4.83.

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

- GRPO：GAR-GRPO 的直接基础优化器。比较 GRPO 与 GAR-GRPO 可以隔离奖励信号的影响，因为二者使用相同基础模型、训练数据和计算预算。
- REINFORCE++：另一种策略梯度优化器。比较 REINFORCE++ 与 GAR-REINFORCE++，用于判断 GAR 是否只是依赖 GRPO，还是能够作为通用奖励塑形方式叠加到不同优化器上。
- Grad2Reward 与 G2RL：均属于利用梯度信息构造学习信号的竞争方法。它们是最直接的方法类别对照，用于检验 GAR 的优势是否来自其特定的“候选轨迹—专家锚点”梯度对齐设计，而非泛泛地使用梯度。
- MASPO：基于优化或奖励改进的竞争方案。其作用是比较 GAR 与非 GAR 的增强型训练方法相对普通 GRPO 能带来多大增益。

**实验想回答的问题**

- 在相同训练数据与计算预算下，GAR 是否能稳定提高 Qwen3-4B 和 Qwen3-8B 在竞赛数学任务上的推理正确率，并且相较普通结果奖励，是否主要提升低采样预算下生成正确答案的概率？
- GAR 的收益是否独立于具体策略优化器，并能否优于其他基于梯度或奖励塑形的竞争方法，同时保持高采样预算下正确推理路径的覆盖能力？

**实验实现**

实验从 Qwen3-4B-Base 与 Qwen3-8B-Base 检查点直接开始强化学习，不使用监督微调预热；各方法使用相同训练数据和计算预算。竞赛数学结果在 10 次独立运行上取平均，表 2 同时报告标准差，并对 GAR 与其对应基础优化器之间的差异进行跨运行配对 $t$ 检验，作者报告所有比较均达到 $p<0.05$。迁移实验使用 Qwen3-4B-Base，各方法只在数学数据上训练，再对 GPQA Diamond 和 MMLU-Pro 做零样本评测。节选未提供生成温度、每题采样细节、训练步数及完整硬件配置。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 作者在六个训练题上挑选了可明确区分解题方法的正确 rollout，并观察到与专家采用相同方法的轨迹获得更高余弦对齐分数，而采用不同但仍正确方法的轨迹得分较低。该案例支持 GAR 信号能够区分内部推导策略，而不只是答案是否正确或文本表面形式；但样本仅有六题，且方法类别需要人工识别，因此它更适合作为机制示例，不能替代大规模因果验证。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper proposes a dense gradient-aligned reward for RLVR post-training that improves chain-of-thought reasoning in LLMs.; rule check: matched taxonomy keywords; top rule score=11.0
- 全文指纹：`bff3a7cb85cb660061e24f9fd6089e9d1bd392923e27e8581cece1691149afd1`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
