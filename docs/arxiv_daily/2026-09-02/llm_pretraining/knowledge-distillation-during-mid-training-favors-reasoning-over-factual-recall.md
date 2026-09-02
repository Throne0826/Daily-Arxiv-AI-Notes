---
title: "[论文解读] Knowledge Distillation During Mid-Training Favors Reasoning over Factual Recall"
description: "[arXiv 2609.01532][预训练] 本文发现标准前向 KL 知识蒸馏在中期训练中会形成“推理提升、事实回忆变慢”的权衡，并据此提出按教师预测熵在蒸馏与下一词预测之间逐词切换的 Switch Distillation。"
arxiv_id: "2609.01532"
announcement_date: "2026-09-02"
primary_category: "llm_pretraining"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:43:25.180646+00:00"
source_sha256: "73e8a52f0400a93bdb5f9cf64040be3b8d4fd5110284b9b48e191702557ee4b8"
tags:
  - "预训练"
  - "LLM Reasoning"
  - "语言模型中期训练"
  - "知识蒸馏"
  - "下一词元预测"
  - "前向KL散度"
  - "反向KL散度"
  - "教师预测熵"
  - "推理—事实回忆权衡"
  - "OLMo-2"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">预训练 · arXiv 2609.01532</p>

# Knowledge Distillation During Mid-Training Favors Reasoning over Factual Recall

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Jacqueline He, Howard Yen, Shuyue Stella Li, Margaret Li, Hanqing Zeng, Yinglong Xia, Benyu Zhang, Zhuokai Zhao, Qiang Zhang, Pang Wei Koh, Luke Zettlemoyer, Wen-tau Yih</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Meta AI；Affiliation: University of Washington；Affiliation: Princeton University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.01532v1) · [PDF 下载](https://arxiv.org/pdf/2609.01532v1) · **关键词** 语言模型中期训练, 知识蒸馏, 下一词元预测, 前向KL散度, 反向KL散度, 教师预测熵, 推理—事实回忆权衡, OLMo-2<br>
**代码**: [https://github.com/facebookresearch/midtraining-distillation](https://github.com/facebookresearch/midtraining-distillation)

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

本文发现标准前向 KL 知识蒸馏在中期训练中会形成“推理提升、事实回忆变慢”的权衡，并据此提出按教师预测熵在蒸馏与下一词预测之间逐词切换的 Switch Distillation。

**不用术语来说**：语言模型完成大规模预训练后，常用规模更小但质量更高的数据继续学习，以加强推理、事实性和指令遵循；由于这一阶段可用词元较少，每个词元的训练信号尤其宝贵。强教师虽然能提供比唯一正确答案更丰富的概率分布，但教师对不同内容的把握并不相同：它往往更擅长程序化的推理步骤，却对某些知识密集型文本不够确定。若不加区分地模仿教师，学生可能更快学会推理，却更慢记住训练数据中的新事实。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者通过受控实验揭示了中期训练特有且跨教师规模、KL 方向和插值系数均较稳健的“推理—回忆权衡”，并将其解释为教师置信度、学生已有知识状态与蒸馏目标三者的相互作用。
- 作者提出 Switch Distillation：利用教师预测熵作为轻量路由信号，在教师有把握的词元上执行知识蒸馏，在教师不确定的词元上退回标准下一词预测，从而缓解推理收益与事实学习之间的冲突。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究自回归语言模型在“中期训练”阶段的知识蒸馏。语言模型通常先在海量文本上预训练，再通过较小但经过筛选的高质量语料继续进行自监督中期训练，以强化事实性、推理、代码和指令理解，最后接受面向交互或对齐的后训练。中期训练所用词元远少于预训练，因此需要从每个词元提取更丰富的监督信号；知识蒸馏为此引入一个能力更强的教师模型，让学生不仅学习语料中实际出现的下一词元，还学习教师对整个词表的概率分布。既有蒸馏研究主要覆盖预训练和后训练，本文所关注的基础问题是：这种监督在学生已经拥有大量知识的中期训练阶段，是否仍会均衡地促进推理能力与事实记忆。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**下一词元预测与交叉熵**

给定前文$x_{<n}$，自回归语言模型预测下一个词元$x_n$，标准训练以交叉熵损失$-\log p_\theta(x_n\mid x_{<n})$提高真实词元的概率。它只把观测到的目标词元作为直接监督，不显式提供其他候选词元之间的相对合理性。

</div>
<div class="concept-item" markdown="1">

**基于logit的知识蒸馏**

教师模型把下一词元的完整预测分布提供给较小的学生模型，学生通过匹配该分布获得比单一正确词元更丰富的监督。本文用$\alpha\in[0,1]$在标准交叉熵与蒸馏损失之间插值，$\alpha=0$即普通下一词元预测，较大的$\alpha$表示更依赖教师。

</div>
<div class="concept-item" markdown="1">

**KL散度与预测熵**

KL散度衡量两个概率分布的差异：前向KL以教师分布加权，要求学生覆盖教师认为可能的候选；反向KL以学生分布加权，更强地抑制教师低概率区域。预测熵概括教师分布的不确定性，熵低表示概率集中、教师更有信心，熵高表示教师在多个候选间犹豫。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是词表兼容的教师—学生语言模型：输入为来自Dolmino Mix 1124的词元序列$\mathbf{x}=(x_1,\ldots,x_N)$及每个位置的前缀$x_{<n}$，学生输出下一词元分布$p_S^\tau(\cdot\mid x_{<n})$，教师输出对应分布$p_T^\tau(\cdot\mid x_{<n})$。标准基线仅最小化真实下一词元的交叉熵；蒸馏训练则以权重$\alpha$混合交叉熵和前向或反向KL散度，并用温度$\tau>0$调节分布平滑程度。实验比较两个训练起点：预训练学生从随机参数开始并训练100B词元；中期训练学生从已在4T词元上预训练的OLMo-2 1B Stage 1检查点继续训练60B词元。教师为后训练过的OLMo-2 1B、7B或13B Instruct模型；核心比较是在控制学生、数据和训练设置后，考察蒸馏相对普通下一词元预测对生成式推理、生成式事实回忆、知识与常识选择题以及后训练后指令遵循的影响，其中阶段差异分析主要聚焦推理与事实回忆。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathbf{x}=(x_1,\ldots,x_N)$**

包含$N$个词元的训练序列，其中$x_n$是位置$n$的目标词元。

</div>
<div class="notation-item" markdown="1">

**$p_\theta(x_n\mid x_{<n})$**

参数为$\theta$的自回归语言模型在前缀$x_{<n}$下赋予真实下一词元$x_n$的概率。

</div>
<div class="notation-item" markdown="1">

**$p_T^\tau(\cdot\mid x_{<n}),\ p_S^\tau(\cdot\mid x_{<n})$**

经温度$\tau$缩放后，教师$T$与学生$S$在给定前缀时对整个词表的下一词元预测分布。

</div>
<div class="notation-item" markdown="1">

**$\alpha\in[0,1]$**

蒸馏强度，即混合目标中KL蒸馏损失的权重；交叉熵权重为$1-\alpha$。

</div>

</div>

**直接相关的工作**

- **Hinton et al. (2015), logit-based knowledge distillation**: 提供本文采用的教师—学生分布匹配范式：学生在真实标签监督之外匹配教师的软预测分布。本文将这一范式放入研究较少的语言模型中期训练阶段，检验其收益是否与预训练阶段一致。
- **Walsh et al. (2025), OLMo-2 ecosystem**: 提供开放的多规模模型、中间检查点、训练配方以及Dolmino训练语料，使本文能够在相同生态内控制学生初始化、教师规模与训练阶段，并直接比较预训练和中期训练中的蒸馏行为。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

中期训练位于预训练与后训练之间，使用较少的精选语料继续进行自监督学习，目标是高效增强事实性、推理、编程和指令遵循等能力。由于其训练词元预算远小于预训练，训练者希望借助更强教师提高单位词元的信息量；然而，如果蒸馏信号妨碍学生从精选语料中吸收尚未掌握的事实，中期训练作为后续对齐基础的价值就会受到削弱。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **标准下一词预测（NTP）**：把语料中的真实下一个词元作为监督目标，以交叉熵训练学生。它直接强化观测到的正确词元，因此适合记忆新事实，但不能利用教师对其他候选词元所提供的相对偏好和结构化知识。
- **基于 logits 的知识蒸馏（前向 KL 蒸馏）**：让学生的预测分布逼近强教师的完整预测分布，通常最小化从教师分布到学生分布的前向 KL 散度，并可用蒸馏强度 $\alpha$ 与 NTP 插值。相较仅监督真实词元，该方法向学生传递教师对整个词表的概率判断。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有语言模型蒸馏研究主要集中于预训练和后训练，因而默认蒸馏在不同训练阶段具有相近作用；本文观察到这一假设不成立：前向 KL 蒸馏在预训练中可同时改善推理与事实回忆，但在中期训练中继续提高推理时会减慢事实获取。
- 统一蒸馏没有区分教师监督质量。教师在数学、指令遵循等程序化数据上的预测熵较低，而在一般网页文本等非结构化、知识密集内容上的预测熵较高；随着教师熵升高，蒸馏相对 NTP 更会削弱真实词元的学习信号，导致中期训练开始时尚未掌握的事实尤其难以被学生吸收。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚不清楚知识蒸馏在中期训练这一独立阶段是否仍能同时促进不同能力，也缺少一种针对学生已有知识状态和教师分域置信度进行自适应选择、并能避免牺牲事实回忆的中期训练目标。

</div>
<div markdown="1"><span>核心问题</span>

在中期训练中，标准知识蒸馏为何会偏向提升推理而抑制新事实的获取，以及能否利用教师预测熵识别可靠监督，在保留推理收益的同时恢复真实词元对事实学习的作用？

</div>
<div markdown="1"><span>作者直觉</span>

教师预测熵可以理解为教师对下一个词元有多犹豫：熵低时，概率集中于少数候选，教师的完整分布通常能提供有价值的额外结构，适合让学生模仿；熵高时，教师本身不确定，继续拟合其分散分布可能冲淡语料中真实词元的信号。因而逐词选择“有把握时蒸馏、没把握时直接学答案”，可以把教师知识主要用于其优势区域，同时让学生仍能从文本中学习教师未可靠掌握的新事实。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Switch Distillation 面向已经完成大规模预训练、正在进行自监督 mid-training 的语言模型。输入是固定语料中的 token 序列、学生模型与后训练教师模型在各位置的下一 token 分布；方法先计算教师分布熵，再将每个 batch 中熵最低的 $q$% token 路由到反向 KL 蒸馏，其余 token 保留标准交叉熵训练，最终得到兼顾推理、知识与事实回忆的 mid-trained 学生模型。作者选择 $q=20\%$，并在后续后训练中继续使用该模型而不再蒸馏。直观地说，教师只在自己最确定、最可能教对的 token 上“授课”，而在不确定的位置让语料本身监督学生，从而避免教师干扰学生已经能够较好吸收的事实知识。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造训练状态与教师监督

在 mid-training 中从 OLMo-2 1B Stage 1 checkpoint 初始化学生，该 checkpoint 已在 4T tokens 上预训练；随后对每个训练序列和 token 位置 $n$，分别执行学生与教师的自回归前向计算，得到下一 token 分布 $p_{\mathrm{S},n}^{(\tau)}$ 和 $p_{\mathrm{T},n}^{(\tau)}$。训练持续 60B tokens；教师提供软标签，语料真实下一个 token 提供交叉熵监督。

<div class="method-step__io" markdown="1">

**输入**：Dolmino Mix 1124 语料、学生语言模型 $S$、词表 $\mathcal{V}$，以及 OLMo-2 1B、7B 或 13B Instruct 教师模型 $T$。<br>
**输出**：每个 token 位置的学生分布、教师分布、真实目标 token，以及可供路由的教师不确定性信号。

</div>

**直观理解**：学生继续阅读经过筛选的混合语料，教师同时对每个位置给出一个完整的概率答案，而不是只给出一个词。这样方法可以逐 token 判断教师是否足够可靠。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算教师熵并选择蒸馏位置

计算教师在位置 $n$ 的预测熵 $H_n$，并在当前 batch 的所有 token 中取熵最低的 $q$% 组成集合 $\mathcal{S}_q=\{n:H_n\leq\operatorname{Quantile}_q(\{H_n\})\}$。实验通过路由比例扫描后选定 $q=20\%$；低熵表示教师的概率质量更集中，通常意味着其 top-1 预测更可能与真实 token 一致。

<div class="method-step__io" markdown="1">

**输入**：每个位置的教师温度缩放分布 $p_{\mathrm{T}}^{(\tau)}(v\mid x_{<n})$。<br>
**输出**：蒸馏 token 集合 $\mathcal{S}_q$ 及其补集 $\bar{\mathcal{S}}_q$，分别对应教师监督和语料监督。

</div>

**直观理解**：把教师最有把握的 20% 题目挑出来让教师教，其余题目仍以原始课本答案为准。熵在这里像一个“教师自信度”分数，但它不需要额外的模型或人工标注。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按 token 路由两种监督

对 $n\in\mathcal{S}_q$ 使用反向 KL，即以学生分布为权重匹配教师分布；对 $n\notin\mathcal{S}_q$ 使用真实 token 的交叉熵。两部分分别归一化，因此 $q$ 只改变哪些 token 接受教师监督，不直接改变蒸馏损失的整体权重。

<div class="method-step__io" markdown="1">

**输入**：蒸馏集合 $\mathcal{S}_q$、补集 $\bar{\mathcal{S}}_q$、学生分布、教师分布和真实目标 token。<br>
**输出**：每个训练 batch 的 Switch Distillation 损失。

</div>

**直观理解**：教师擅长的局部位置使用软概率教学，教师不确定的位置则让学生直接学习语料答案。分开归一化可以避免仅仅因为选中的 token 数量变化，就意外改变训练强度。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 优化学生并进行下游后训练

通过梯度下降最小化路由后的联合目标，得到 mid-trained checkpoint；随后对各方法的 checkpoint 统一执行 OLMo-2 1B 的四阶段后训练流程：监督微调（SFT）、直接偏好优化（DPO）以及两轮带可验证奖励的强化学习（RLVR1、RLVR2），后训练阶段不再继续蒸馏。

<div class="method-step__io" markdown="1">

**输入**：Switch Distillation 损失及 mid-training 中更新后的学生参数。<br>
**输出**：可用于推理、事实回忆、知识与常识以及指令遵循评测的最终模型。

</div>

**直观理解**：先在持续预训练阶段选择性吸收教师能力，再用同一套对齐流程把所有模型训练成可交互助手。这样可以检验方法的收益是否只是训练中暂时存在，还是会保留到最终模型。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 教师预测熵与路由集合

$$
H_n=-\sum_{v\in\mathcal{V}}p_{\mathrm{T}}^{(\tau)}(v\mid x_{<n})\log p_{\mathrm{T}}^{(\tau)}(v\mid x_{<n}),\qquad \mathcal{S}_{q}=\left\{n:H_n\leq\operatorname{Quantile}_{q}(\{H_n\})\right\}
$$

**符号说明**

- $H_n$：教师在 token 位置 $n$ 的预测熵，数值越低表示教师分布越集中、相对越有把握。
- $p_{\mathrm{T}}^{(\tau)}(v\mid x_{<n})$：教师在给定前缀 $x_{<n}$ 时，对词表 token $v$ 的温度缩放概率；$\tau$ 是温度参数。
- $\mathcal{V}$：语言模型词表。
- $\mathcal{S}_q$：被路由到教师蒸馏的 token 位置集合，包含当前 batch 中熵最低的 $q$% token。
- $\operatorname{Quantile}_q(\{H_n\})$：所有位置熵值的 $q$ 分位数阈值。

<div class="equation-explanation" markdown="1">

**直观理解**：该式先把教师对一个位置的概率答案压缩成一个不确定性分数，再按分数排序。熵低于 batch 分位数的位置交给教师，其他位置交给语料监督；因此路由依据的是教师信心，而不是预先固定的领域标签。<br>
**原文位置**：第 5 节，公式（5）及 Switch Distillation 定义

</div>

</div>

<div class="equation-block" markdown="1">

#### Switch Distillation 联合目标

$$
\mathcal{L}^{\mathrm{SwitchDist}}=\tau^{2}\frac{1}{|\mathcal{S}_{q}|}\sum_{n\in\mathcal{S}_{q}}\mathrm{RKL}\!\left(p_{\mathrm{S},n}^{(\tau)}\,\|\,p_{\mathrm{T},n}^{(\tau)}\right)+\frac{1}{|\bar{\mathcal{S}}_{q}|}\sum_{n\notin\mathcal{S}_{q}}\mathcal{L}_{\mathrm{CE},n}
$$

**符号说明**

- $\mathcal{L}^{\mathrm{SwitchDist}}$：Switch Distillation 的训练损失。
- $\tau^{2}$：温度缩放产生的损失因子，用于保持蒸馏梯度尺度。
- $\mathrm{RKL}(p_{\mathrm{S},n}^{(\tau)}\|p_{\mathrm{T},n}^{(\tau)})$：位置 $n$ 上学生分布相对教师分布的反向 KL 散度。
- $\mathcal{L}_{\mathrm{CE},n}$：位置 $n$ 以真实下一个 token 为目标的交叉熵损失。
- $|\mathcal{S}_q|,|\bar{\mathcal{S}}_q|$：蒸馏集合及其补集中的 token 数量，用于分别归一化两项损失。

<div class="equation-explanation" markdown="1">

**直观理解**：目标函数把一个 batch 分成两部分：可靠位置平均计算 RKL，不可靠位置平均计算 CE。两部分各自平均后相加，所以改变 $q$ 主要改变监督来源的覆盖范围，而不是简单地把教师损失放大或缩小。<br>
**原文位置**：第 5 节，公式（6）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：学生通过最小化上述联合目标更新参数。对最低熵的 $q$% token，RKL 使学生分布集中到教师偏好的高概率区域；对剩余 token，CE 使学生拟合语料中的真实下一 token。与统一的 forward-KL KD 不同，该目标显式利用教师不确定性决定监督来源；与普通混合目标不同，RKL 和 CE 在各自 token 子集上分别归一化，因此 $q$ 表示路由比例而非额外的全局蒸馏权重。作者的设计依据是 mid-training 中教师对程序性数据更自信，而学生较早获得低熵事实知识；统一蒸馏可能减慢事实回忆获取，选择性蒸馏则试图保留两类监督的优势。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 教师预测熵路由**

教师在每个 token 位置计算温度为 $\tau$ 的预测熵，并以 batch 内熵的分位数为阈值选择最低熵的 $q$% 位置。实验报告采用 $q=20\%$；在 7B 教师上，$q=10\%$、$20\%$、$30\%$ 的 mid-training Reasoning macro-average 分别为 40.6、44.7、43.9，说明中等稀疏度在所测设置中最好；13B 教师对应数值为 38.5、42.1、41.6（Table/节 6.4 附近的 routing-ratio ablation）。

> 直观理解：模型不假设教师对所有内容同样可靠，而是动态挑选教师最确定的位置。程序性内容通常更容易让教师形成尖锐分布，事实性 payload 则可能让教师分布更分散，因此这种选择能减少错误或不必要的教师干预。

**2. 低熵位置的反向 KL 蒸馏**

在 $\mathcal{S}_q$ 上使用 RKL，而不是标准 forward KL。RKL 的 mode-seeking 特性会强化教师偏好的高概率延续；低熵筛选使这一性质更适合可靠、集中的教师分布，同时避免把教师低概率尾部的分布质量广泛传播给学生。

> 直观理解：当教师非常确定时，学生应更集中地学习教师最推荐的延续，而不是平均照顾教师几乎不认可的许多候选词。该设计将“什么时候蒸馏”和“用什么散度蒸馏”配合起来。

**3. 剩余 token 的交叉熵回退**

在 $\bar{\mathcal{S}}_q$ 上保留真实语料 token 的 CE，而不是强迫学生匹配高熵教师。该回退机制使语料监督继续负责事实知识获取，并且不增加模型参数或额外模型前向次数；相较标准在线 KD，额外开销主要是熵和分位数计算。

> 直观理解：教师没把握时不必硬听教师，而应回到训练数据中的实际答案。它相当于给系统设置了一个安全模式，保护学生对事实内容的正常学习。

**训练与推理**

训练阶段使用固定的 Dolmino Mix 1124 语料进行自回归 mid-training；该混合数据包括过滤后的 DCLM web text、FLAN instruction-following data、Dolmino Math、peS2o、Wikipedia（含 Wikibooks）和 Stack Exchange。教师与学生对同一前缀进行在线前向计算，教师熵在每个 batch 内计算并产生路由掩码，学生随后反向传播 Switch Distillation 损失；推理时不需要教师、熵计算或路由，直接使用训练后的学生模型生成文本。实验还把 mid-trained checkpoint 统一送入 SFT、DPO、RLVR1 和 RLVR2 后训练，以测试 mid-training 获得的能力是否能保留到最终模型。

**复现信息**

复现实验所需的关键设置是：学生为 OLMo-2 1B，mid-training 从已预训练 4T tokens 的 OLMo-2 1B Stage 1 checkpoint 开始并继续 60B tokens；教师使用 OLMo-2 1B、7B 或 13B Instruct，词表需与学生兼容。路由比例通过 $q=10\%$、$20\%$、$30\%$ 扫描，主实验选 $q=20\%$；方法不增加参数或额外模型前向，仅增加熵与分位数计算。比较或解释结果时应注意，研究还测试了 FKL、教师 top-1 正确性、程序性领域标签、随机等稀疏路由，以及始终 CE 和教师 top-1 硬标签等替代设计；完整优化器、学习率、batch size 与温度具体数值在所给摘录中原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 中期训练语料：用于按照论文第 2.2 节相同的中期训练设置训练学生模型；所给摘录未明确报告该语料的名称、规模或划分。
- 下游 Reasoning 基准集合：用于评估数学、逻辑或其他推理能力；摘录仅说明表 1 使用了缩写后的基准名称，并未列出完整任务名、规模或划分。
- Factual Recall 以及 Knowledge & Commonsense 基准集合：前者检验事实信息回忆，后者检验知识与常识应用；摘录未明确报告各基准的完整名称、规模或划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Reasoning**

多个推理下游任务的宏平均性能，用于衡量模型解决需要程序性推导或多步判断的问题的能力。 （越高越好，因为高分表示推理任务的平均表现更强。）

</div>
<div class="metric-item" markdown="1">

**Factual Recall**

事实回忆能力，衡量模型是否能够保留或提取训练中获得的低熵事实知识。 （越高越好；本实验尤其关注蒸馏提升推理时是否牺牲该指标。）

</div>
<div class="metric-item" markdown="1">

**Knowledge & Commonsense**

知识与常识任务的综合性能，衡量模型对一般知识和日常常识的理解与应用能力。 （越高越好，因为高分表示知识和常识相关下游任务表现更强。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 推理能力：Switch Distillation 与 $\mathrm{NTP}$ 及其他蒸馏基线比较

<div class="result-value" markdown="1">

在 7B 和 13B 教师条件下，Switch Distillation 的 Reasoning 宏平均分别为 44.7% 和 42.1%，高于 $\mathrm{NTP}$ 的 26.1%，并且是两种教师规模下最强的推理方法。

</div>

这表明按教师置信度选择蒸馏或交叉熵，能够显著增强学生处理推理任务的能力。它只说明在论文所用中期训练设置和下游基准上平均表现更好，不能单独证明该方法在所有推理类型、所有训练阶段或未报告的数据分布上都普遍优越。

<div class="result-source" markdown="1">

来源：第 6.2 节，表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across both teacher sizes, Switch Distillation achieves the strongest Reasoning, improving the macro-average from 26.1% under NTP to 44.7%/42.1% with the 7B and 13B teachers, while remaining the KD baseline closest to NTP on Factual Recall (29.3%/29.3% vs. 30.3%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 事实回忆：保持原有知识的能力

<div class="result-value" markdown="1">

Switch Distillation 在 7B 和 13B 教师下的 Factual Recall 均为 29.3%，接近 $\mathrm{NTP}$ 的 30.3%，并且是知识蒸馏基线中最接近 $\mathrm{NTP}$ 的方法。

</div>

该结果支持方法缓解推理增强通常伴随的事实回忆下降：它没有达到 $\mathrm{NTP}$ 的事实回忆分数，但损失相对较小。这里的“保持”是相对于其他蒸馏基线而言的近似保持，不应解读为完全消除了事实回忆差距。

<div class="result-source" markdown="1">

来源：第 6.2 节，表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across both teacher sizes, Switch Distillation achieves the strongest Reasoning, improving the macro-average from 26.1% under NTP to 44.7%/42.1% with the 7B and 13B teachers, while remaining the KD baseline closest to NTP on Factual Recall (29.3%/29.3% vs. 30.3%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 知识与常识：不同教师规模下的综合能力

<div class="result-value" markdown="1">

Switch Distillation 在 7B 和 13B 教师下的 Knowledge & Commonsense 分别为 49.3% 和 46.5%，并在该指标上取得最强表现；论文同时观察到 7B 教师通常优于 13B 教师。

</div>

结果说明更大的教师并不必然带来更好的蒸馏结果；在学生能力固定时，教师与学生之间过大的容量差距可能使教师分布不易被学生有效模仿。这个解释是论文结合既有工作的分析，当前摘录没有提供控制教师质量、训练计算量或具体任务难度后的因果验证。

<div class="result-source" markdown="1">

来源：第 6.2 节，表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Switch Distillation also achieves the strongest Knowledge & Commonsense performance (49.3%/46.5%). We further note that distillation with the 7B teacher generally outperforms the 13B teacher.

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

- 标准下一词预测（$\mathrm{NTP}$）：没有教师，作为共享参考点，用于衡量蒸馏相对于普通语言模型训练的收益或代价。
- 正向知识蒸馏（$\mathrm{FKD}$）：在 $\alpha=0.5$ 下使用标准正向 KL 蒸馏，是论文比较的主要知识蒸馏基线。
- 反向知识蒸馏（$\mathrm{RKD}$）：同样在 $\alpha=0.5$ 下运行，用于检验改变 KL 方向后，性能是否改善事实回忆与推理之间的权衡。
- Token-routing 知识蒸馏（$\mathrm{TRKD}$）：在高教师熵 token 上进行正向 KL 蒸馏、其他 token 保留交叉熵（$\mathrm{CE}$），用于比较另一种基于 token 路由的蒸馏策略。

**实验想回答的问题**

- 在中期训练阶段，与标准下一词预测（$\mathrm{NTP}$）、正向知识蒸馏（$\mathrm{FKD}$）、反向知识蒸馏（$\mathrm{RKD}$）和 token-routing 知识蒸馏（$\mathrm{TRKD}$）相比，Switch Distillation 是否能同时提升推理与知识、常识能力，并尽量保持事实回忆能力？
- 该方法在不同教师模型规模下是否稳定有效，以及其表现是否受到教师与学生之间容量差距的影响？

**实验实现**

实验沿用第 2.2 节的中期训练设置，学生模型分别接受 OLMo-2 7B Instruct 或 13B Instruct 教师的监督；同时与无教师的 $\mathrm{NTP}$ 比较。$\mathrm{FKD}$ 和 $\mathrm{RKD}$ 均采用 $\alpha=0.5$，该值据论文称在事实回忆与推理之间提供了经验上最好的平衡。Switch Distillation 使用教师预测熵作为轻量路由信号：教师低熵、即更有把握的 token 使用反向 KL 蒸馏，否则使用交叉熵；这与 $\mathrm{TRKD}$ 在高熵 token 上使用正向 KL 的策略不同。训练使用开源 lingua 框架；教师模型的蒸馏温度为 $\tau=2$，7B 和 13B 教师以 FP8 加载。下游结果在中期训练后评估，表 1 还说明使用成对 bootstrap 检验统计显著性，显著性阈值为 $p<0.05$。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper proposes a mid-training distillation objective and measures its effects on language-model reasoning and factual knowledge acquisition.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`73e8a52f0400a93bdb5f9cf64040be3b8d4fd5110284b9b48e191702557ee4b8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
