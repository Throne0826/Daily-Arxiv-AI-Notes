---
title: "[论文解读] Beyond the Mean: Multi-Moment Policy Optimization for LLM Reasoning"
description: "[arXiv 2608.02149][对齐 / RLHF] 本文将不同数学题上的失败概率视为取值于$[0,1]$的随机变量，从“只优化一个矩”转向联合优化多个矩，以更完整地控制模型在不同难度问题上的推理表现。"
arxiv_id: "2608.02149"
announcement_date: "2026-08-04"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:01:34.706268+00:00"
source_sha256: "6d4d1e58e8752fa0688361aec997feffe04500824990303f913352a1c6c9a96a"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "强化学习"
  - "大语言模型推理"
  - "可验证奖励强化学习"
  - "策略优化"
  - "失败概率分布"
  - "矩优化"
  - "Pass@$K$"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.02149</p>

# Beyond the Mean: Multi-Moment Policy Optimization for LLM Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Yijun Zhang, Yule Xie, Jiaxin Ding, Xin Ding, Fan Xu, Haoxiang Zhang, Luoyi Fu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Shanghai Jiao Tong University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.02149v1) · [PDF 下载](https://arxiv.org/pdf/2608.02149v1) · **关键词** 大语言模型推理, 可验证奖励强化学习, 策略优化, 失败概率分布, 矩优化, Pass@$K$<br>
**代码**: [https://github.com/e3trange/MMPO](https://github.com/e3trange/MMPO)

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

本文将不同数学题上的失败概率视为取值于$[0,1]$的随机变量，从“只优化一个矩”转向联合优化多个矩，以更完整地控制模型在不同难度问题上的推理表现。

**不用术语来说**：经过强化学习训练后，模型可能在多数简单题上表现很好，却仍频繁答错少数困难题；若训练目标只看所有题的平均失败率，这种差异会被平均值掩盖。论文要解决的问题是：如何设计一个目标，使训练不仅降低整体失败水平，还能利用失败概率分布的更多信息，对较难问题给予适度关注，同时避免只追逐某一项局部统计量。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出失败概率分布的矩视角，并据此构造多矩策略优化方法MMPO，同时最小化多个阶次的矩；该目标还可解释为最小化“在有限次尝试内获得首次正确回答所需尝试次数”的期望。
- 作者提出广义矩变换框架，将REINFORCE式目标、Pass@$K$训练和MaxRL置于统一视角下，并声称该目标族具有严格Schur凸性，因而偏好让不同问题的成功概率更加均衡。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究面向大语言模型数学推理的可验证奖励强化学习（RLVR）。在这一设置中，模型策略针对每道题生成回答，规则验证器依据最终答案是否正确给出二元奖励；因此，对任意题目重复采样时，策略都对应一个成功概率和失败概率，而题目难度差异进一步形成跨题目的失败概率分布。传统策略梯度方法主要提高平均奖励，等价于降低该分布的一阶矩；本文则借助概率分布的矩来描述不同目标究竟关注平均失败、难题失败还是更完整的分布结构。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**可验证奖励强化学习（RLVR）**

RLVR使用规则程序或答案检查器判断模型输出是否正确，从而提供可靠的结果级奖励。在本文的数学推理场景中，每个回答只获得成功或失败的二元反馈。

</div>
<div class="concept-item" markdown="1">

**失败概率随机变量及其矩**

从题目分布中随机抽取问题后，该题在当前策略下的失败概率也成为随机变量$F_\theta\in[0,1]$；其第$i$阶矩为$\mathbb{E}[F_\theta^i]$。一阶矩反映平均失败率，较高阶矩会相对放大高失败概率题目的影响。

</div>
<div class="concept-item" markdown="1">

**Pass@$K$**

Pass@$K$表示对同一道题独立生成$K$个回答时，至少一个回答正确的概率；若单次失败概率为$f$，则$K$次全部失败的概率为$f^K$。因此，优化跨题目的Pass@$K$可被理解为降低失败概率分布的单个$K$阶矩。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是从数学题目分布中采样的问题，以及由参数为$\theta$的大语言模型策略生成的一个或多个推理回答；规则验证器将每个回答映射为成功或失败。对每道题，策略诱导一个单次回答失败概率；随机抽题后得到跨题目的失败概率随机变量$F_\theta$。训练目标是在仅有结果级二元监督、同题回答可重复采样的设置下调整$\theta$，以降低整体失败风险。本文所依赖的关键假设是$F_\theta$的取值位于$[0,1]$：根据Hausdorff矩定理，该区间上分布的完整矩序列能够唯一确定分布，因此只优化$\mathbb{E}[F_\theta]$或某个$\mathbb{E}[F_\theta^K]$只能约束分布的一个侧面，不能完整刻画不同难度题目上的失败结构。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\theta$**

大语言模型策略的可训练参数。

</div>
<div class="notation-item" markdown="1">

**$F_\theta$**

从问题分布随机抽题时，该题在策略参数$\theta$下的单次回答失败概率所形成的随机变量，取值属于$[0,1]$。

</div>
<div class="notation-item" markdown="1">

**$\mathbb{E}[F_\theta^i]$**

失败概率随机变量$F_\theta$的第$i$阶矩，即跨问题平均后的$i$次方失败概率。

</div>
<div class="notation-item" markdown="1">

**$K$**

对同一道问题独立采样回答的次数；在Pass@$K$目标中也对应所优化的失败概率矩阶数。

</div>

</div>

**直接相关的工作**

- **REINFORCE、GRPO与DAPO**: 这些方法以期望奖励为核心：REINFORCE提供基本策略梯度形式，GRPO和DAPO通过组内优势估计等机制改善训练效率与稳定性。按照本文的矩视角，它们仍主要对应降低$F_\theta$的一阶矩，因而主要反映平均失败水平。
- **Pass@$K$ training与MaxRL**: Pass@$K$训练最大化$K$次采样中至少一次成功的概率，在本文框架下等价于优化单个更高阶矩$\mathbb{E}[F_\theta^K]$；MaxRL通过最大化期望对数成功概率建立似然导向目标，本文将其解释为优化变换后随机变量的多个加权矩。二者说明现有非期望奖励目标已隐含分布偏好，但此前缺少统一的矩刻画。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在带可验证奖励的强化学习中，数学推理答案可由规则验证器赋予成功或失败的二元奖励，因此一项策略会为每道题诱导一个失败概率。实际训练既需要降低跨问题的总体失败水平，也需要改善那些需要多次采样才可能答对的困难题；否则，平均成绩的提升可能主要来自本来就容易的问题。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **期望奖励与探索增强方法**：REINFORCE以期望奖励为基本目标；GRPO和DAPO在这一训练范式上加入稳定化改进。相关探索方法还使用熵正则化或分布匹配，促使策略保持输出多样性。按本文的矩视角，REINFORCE式方法实质上主要优化失败概率随机变量$F_\theta$的一阶矩$\mathbb{E}[F_\theta]$，即平均失败概率。
- **直接基于失败分布构造的目标**：Pass@$K$训练关注同一问题经过$K$次采样后至少成功一次的概率，因此对应于优化失败概率的某个单一高阶矩，倾向于改善困难问题的多次尝试成功率；MaxRL则从似然角度连接强化学习与最大似然学习，本文将其重新解释为优化经变换分布的矩。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有目标虽然出发点不同，但缺少统一的分布层面刻画，因而难以明确比较它们究竟强调平均表现、困难问题，还是问题间表现均衡性；这也使目标函数设计较依赖局部直觉。
- 一阶矩方法和Pass@$K$训练分别只约束一个矩。由于$[0,1]$上的分布需要完整矩序列才能唯一确定，单个矩只能反映失败概率分布的一个侧面，无法刻画其更广泛的结构；结果是相同或接近的目标值可能对应明显不同的跨题失败模式。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未显式建立一个面向LLM推理策略优化的多矩框架：既能联合利用失败概率分布的多个统计层次，又能为这种联合目标给出清晰的操作含义，并统一解释若干已有目标之间的关系。

</div>
<div markdown="1"><span>核心问题</span>

能否从失败概率随机变量$F_\theta$的矩出发，构造一个可训练的策略优化目标，使其同时最小化多个矩，并在平均性能、困难题关注程度与跨问题成功概率均衡性之间形成有理论依据的权衡？

</div>
<div markdown="1"><span>作者直觉</span>

平均失败率只回答“随机抽一道题，模型平均多容易失败”，而高阶矩会放大接近$1$的失败概率，因此对持续答错的困难题更敏感。将多个阶次合并，相当于同时从多个尺度观察失败分布：低阶矩维持整体改善，高阶矩增加对高失败概率问题的压力。作者进一步把这一组合解释为缩短有限次重复尝试下的首次成功时间，使抽象的多矩目标对应到“尽快得到第一个正确答案”这一实际需求。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MMPO（Multi-Moment Policy Optimization，多矩策略优化）把“一个随机题目上的失败概率”视为随机变量，而不只优化所有题目的平均失败率。给定题目分布 $\mathcal{D}$、策略 $\pi_\theta$ 和二值验证器 $r(x,y)$，单次回答的成功概率为 $s_\theta(x)$，失败概率为 $f_\theta(x)=1-s_\theta(x)$；当随机题目 $X\sim\mathcal{D}$ 时，$F_\theta=f_\theta(X)$ 描述模型在不同题目上的失败率分布。REINFORCE、GRPO 一类目标主要降低一阶矩 $\mathbb{E}[F_\theta]$，MMPO 则最小化前 $T$ 个原始矩之和 $\sum_{k=1}^{T}\mathbb{E}[F_\theta^k]$。高阶矩会相对突出失败概率大的困难题，因此该目标同时关注整体准确率和困难题长尾，而不是只提高已经较容易解出的题目。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立题目级失败概率模型

策略生成回答 $y\sim\pi_\theta(\cdot\mid x)$，并定义 $s_\theta(x)=\mathbb{E}[r(x,y)]$ 与 $f_\theta(x)=1-s_\theta(x)$；令 $X\sim\mathcal{D}$，得到跨题目随机变量 $F_\theta=f_\theta(X)$。

<div class="method-step__io" markdown="1">

**输入**：题目分布 $\mathcal{D}$、从中抽取的题目 $x$、当前策略 $\pi_\theta(\cdot\mid x)$，以及输出二值奖励的验证器 $r(x,y)\in\{0,1\}$。<br>
**输出**：当前策略在题目分布上的失败概率分布，以及它的矩 $\mu_k(\theta)=\mathbb{E}[F_\theta^k]$。

</div>

**直观理解**：不再只问“模型平均能答对多少”，而是记录每道题各自有多难。这样可以区分“多数题都略有失败”和“少数题几乎永远失败”这两种平均值相同、训练意义却不同的情况。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造多矩总体目标

将前 $T$ 个原始矩等权相加，最小化 $\mathcal{J}_T(\theta)=\sum_{k=1}^{T}\mathbb{E}[F_\theta^k]$。该目标与最小化首次成功所需尝试次数的截断期望仅相差与参数无关的常数项。

<div class="method-step__io" markdown="1">

**输入**：失败概率随机变量 $F_\theta$ 与截断阶数 $T$。<br>
**输出**：一个兼顾平均失败率和困难题高失败率的总体优化准则 $\mathcal{J}_T(\theta)$。

</div>

**直观理解**：如果一道题连续多次都失败，它会同时影响多个矩，因而得到更强的训练关注。$T$ 可以理解为关心“在有限次尝试内尽快首次答对”的最大观察范围。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按题目组采样并估计优势

对每道题 $x_i$ 独立采样 $G$ 个回答 $y_{i,j}$ 并计算奖励；可用组内成功率 $\widehat{s}_i$ 构造插件式权重 $\widehat{w}_i$ 和有偏优势，也可在 $T\leq G$ 时利用排除第 $j$ 个回答的留一法统计量构造无偏梯度优势。

<div class="method-step__io" markdown="1">

**输入**：冻结的旧策略 $\pi_{\theta_{\mathrm{old}}}$、一个含 $B$ 道题的批次，以及每题的组大小 $G$。<br>
**输出**：每个回答对应的实现优势 $\widehat{A}_{i,j}$，其中题目难度权重和回答相对组内基线的好坏被合并。

</div>

**直观理解**：同一道题一次生成多个答案，用这组答案估计它当前有多难，再决定该题的训练信号应放大多少。有偏版本简单且作者称经验上有效，无偏版本更严格，但需要足够多的组内样本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行裁剪策略更新

最大化 PPO 风格的裁剪代理目标，在未裁剪项 $\rho_{i,j}(\theta)\widehat{A}_{i,j}$ 与裁剪项之间取较保守者；完成一轮更新后，将当前策略作为下一轮采样所用的旧策略。

<div class="method-step__io" markdown="1">

**输入**：回答样本 $y_{i,j}$、优势 $\widehat{A}_{i,j}$、新旧策略概率比 $\rho_{i,j}(\theta)$ 和裁剪阈值 $\epsilon$。<br>
**输出**：更新后的策略参数 $\theta$，以及下一轮迭代使用的策略 $\pi_\theta$。

</div>

**直观理解**：多矩目标决定“哪些题和回答更值得学习”，PPO 裁剪则限制单次参数更新幅度，避免新策略相对采样策略变化过猛。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### MMPO 多矩总体目标及首次成功解释

$$
\min_{\theta}\ \mathcal{J}_{T}(\theta),\qquad \mathcal{J}_{T}(\theta)=\sum_{k=1}^{T}\mathbb{E}\!\left[F_{\theta}^{k}\right];\qquad \mathbb{E}\!\left[\min\{S_{\theta}(X),T+1\}\mid X=x\right]=\sum_{k=0}^{T}f_{\theta}(x)^{k}.
$$

**符号说明**

- $\theta$：策略模型参数。
- $\mathcal{J}_{T}(\theta)$：MMPO 在截断阶数为 $T$ 时的总体损失。
- $T$：纳入目标的最高矩阶数，也是首次成功时间解释中的有限截断范围。
- $X\sim\mathcal{D}$：从题目分布 $\mathcal{D}$ 随机抽取的问题实例。
- $F_{\theta}=f_{\theta}(X)$：随机题目在当前策略下的失败概率随机变量。
- $f_{\theta}(x)=1-s_{\theta}(x)$：固定题目 $x$ 的单次生成失败概率。
- $S_{\theta}(x)$：对题目 $x$ 独立重复生成时，第一次产生正确回答的尝试编号。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分把失败概率的前 $T$ 个矩等权相加；因为 $F_\theta$ 位于 $[0,1]$，高阶项会更集中地惩罚失败概率接近 $1$ 的题目。第二部分说明该和式比截断首次成功时间的期望少常数 $1$，所以两者对 $\theta$ 有相同的最优解和梯度方向；MMPO由此获得“减少有限预算内首次成功所需尝试次数”的操作性含义。<br>
**原文位置**：第3.2节 Population Objective，式(3)与式(5)

</div>

</div>

<div class="equation-block" markdown="1">

#### 问题级权重与裁剪代理目标

$$
w_{T,\theta}(x)=\sum_{k=1}^{T}k f_{\theta}(x)^{k-1},\qquad \mathcal{L}_{\mathrm{MMPO}}(\theta)=\frac{1}{BG}\sum_{i=1}^{B}\sum_{j=1}^{G}\min\!\left(\rho_{i,j}(\theta)\widehat{A}_{i,j},\operatorname{clip}(\rho_{i,j}(\theta),1-\epsilon,1+\epsilon)\widehat{A}_{i,j}\right).
$$

**符号说明**

- $w_{T,\theta}(x)$：由多矩目标导出的题目级梯度权重；它随题目失败概率变化。
- $B$：每个训练批次中的题目数。
- $G$：每道题从旧策略采样的回答数。
- $\widehat{A}_{i,j}$：第 $i$ 道题第 $j$ 个回答的实现优势，可采用插件式有偏估计或留一法无偏估计。
- $\rho_{i,j}(\theta)$：重要性比率 $\pi_\theta(y_{i,j}\mid x_i)/\pi_{\theta_{\mathrm{old}}}(y_{i,j}\mid x_i)$。
- $\epsilon$：PPO 风格代理目标的概率比裁剪阈值。
- $\pi_{\theta_{\mathrm{old}}}$：生成当前训练样本时冻结使用的旧策略。

<div class="equation-explanation" markdown="1">

**直观理解**：权重式把总体多矩目标转换成可在每道题上实施的训练强度：失败率高的题会获得更强信号。裁剪目标再用新旧策略概率比修正离策略更新，并限制比率偏离 $1$ 的幅度，从而把新的题目重加权机制接入成熟的 PPO 更新流程。<br>
**原文位置**：第3.2节 Surrogate Objective，式(7)与式(13)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：总体上最小化 $\mathcal{J}_T(\theta)=\sum_{k=1}^{T}\mathbb{E}[F_\theta^k]$，实践中则最大化由该目标梯度导出的 PPO 裁剪代理函数。目标求导后，标准的成功奖励梯度被题目级系数 $w_{T,\theta}(x)$ 调整；再减去成功概率基线，可写成 $w_{T,\theta}(x)(r(x,y)-s_\theta(x))\nabla_\theta\log\pi_\theta(y\mid x)$ 的期望。该基线不改变期望梯度，但使单个回答相对于同题平均成功水平产生正或负优势。

MMPO 与对照目标的区别在于矩系数：REINFORCE 风格方法只优化 $\mathbb{E}[F_\theta]$，Pass@$K$ 只优化 $\mathbb{E}[F_\theta^K]$，MaxRL 使用 $\sum_{k=1}^{T}\mathbb{E}[F_\theta^k]/k$，而 MMPO 对前 $T$ 阶矩赋相同系数。作者从理论上将 MaxRL 解释为优化变换变量 $U_\lambda F_\theta$ 的矩，其中 $U_\lambda\sim\operatorname{Beta}(\lambda,1)$；MMPO 则对应退化选择 $U\equiv1$，直接优化 $F_\theta$ 的矩。论文进一步证明这类广义矩目标在 $T\geq2$ 时严格 Schur-凸，即平均失败率相同的两个题目集合中，失败率越不均衡者目标值越高；直观上，它反对只在容易题上集中取得收益，并偏好把改进更均匀地分配到不同题目。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 失败概率矩表征**

核心状态量是 $F_\theta=f_\theta(X)\in[0,1]$，其第 $k$ 阶原始矩为 $\mu_k(\theta)=\mathbb{E}[F_\theta^k]$。一阶矩对应平均失败率，较高阶矩对接近 $1$ 的失败概率更敏感；理论上，$[0,1]$ 上随机变量的完整矩序列可唯一决定其分布，但有限个矩只能提供部分表征。

> 直观理解：均值只给出一张总成绩单，多阶矩则补充模型是否存在一批长期答不出的题。论文没有声称有限的 $T$ 个矩能完整恢复失败率分布，而是用它们提供互补的优化信号。

**2. 首次成功时间与困难题重加权**

对固定题目独立重复采样时，首次成功时间 $S_\theta(x)$服从成功概率为 $s_\theta(x)$ 的几何分布，且 $\mathbb{E}[\min\{S_\theta(X),T+1\}\mid X=x]=\sum_{k=0}^{T}f_\theta(x)^k$。对多矩目标求导得到题目级权重 $w_{T,\theta}(x)=\sum_{k=1}^{T}k f_\theta(x)^{k-1}$，因此失败概率越高的题通常权重越大；相较只优化 $\mathbb{E}[F_\theta^T]$ 的 Pass@$T$，它通过汇总从一阶到 $T$ 阶信号来避免只由最高阶矩实施过激重权。

> 直观理解：该模块把抽象的矩目标解释成“在有限预算内尽快第一次答对”。困难题往往需要更多次尝试，所以目标会自然提高其训练优先级，但仍保留低阶矩对整体平均表现的约束。

**3. 组内优势估计与 PPO 接口**

插件式估计先计算 $\widehat{s}_i=G^{-1}\sum_{j=1}^{G}r(x_i,y_{i,j})$，再令 $\widehat{w}_i=\sum_{k=1}^{T}k(1-\widehat{s}_i)^{k-1}$ 和 $\widehat{A}_{i,j}^{\mathrm{bias}}=\widehat{w}_i(r(x_i,y_{i,j})-\widehat{s}_i)$。论文还给出基于 $M_{i,-j}$ 的留一法无偏优势；两种优势均可直接代入 PPO 风格的裁剪代理目标。

> 直观理解：这使 MMPO 无需改变语言模型结构：相对于常见的组式策略优化，主要新增的是按组内成功情况计算题目权重。工程上可以在简单但有偏的估计与条件更严格的无偏估计之间选择。

**训练与推理**

训练开始时以初始语言模型作为 $\pi_\theta$。每轮先复制参数得到采样策略 $\pi_{\theta_{\mathrm{old}}}$，从 $\mathcal{D}$ 抽取 $B$ 道题，并对每题生成 $G$ 个回答；验证器计算二值正确性后，按所选估计器得到 $\widehat{A}_{i,j}$。插件式版本复用同一组样本估计成功率、题目权重与基线，因此一般有偏；当 $T\leq G$ 时，可用其余 $G-1$ 个回答的失败计数 $M_{i,-j}$ 构造留一法优势，使策略梯度方向无偏。随后在这些固定样本上最大化裁剪代理目标，更新 $\theta$，并重复采样和优化直至收敛，最终返回 $\pi_\theta$。

推理阶段不需要计算 $F_\theta$ 的矩、题目权重或组内优势，也不需要额外的判别网络；输入题目后直接由训练后的策略生成回答。首次成功时间是目标的训练解释，而不是强制要求部署时必须执行到成功为止：实际推理可按评测或应用预算采用单次生成，也可进行多次独立采样。

**复现信息**

复现方法所必需的结构性超参数是截断阶数 $T$、批大小 $B$、每题采样数 $G$、PPO 裁剪阈值 $\epsilon$，以及优势估计器的选择。使用无偏估计时必须满足 $T\leq G$；若取 $T=G$，论文给出了仅依赖组内成功数 $N_i$ 与当前回答奖励的简化闭式优势。插件式估计不需要该留一组合统计，计算更直接，但其偏差意味着它并非总体目标梯度的严格无偏估计。

从算法改动看，MMPO主要是在组式策略优化上增加题目级权重，而不是修改模型架构。给定组内成功率，$\widehat{w}_i=\sum_{k=1}^{T}k(1-\widehat{s}_i)^{k-1}$ 可直接计算；较大的 $G$ 不仅降低采样噪声，还允许估计更宽的矩范围。所给节选仅明确初始模型采用 Qwen3-1.7B/4B-Base，并称训练使用 verl；学习率、生成长度、具体 $T$、$G$、$B$、$\epsilon$、优化轮数及采用有偏还是无偏优势等数值配置在当前节选中未完整报告，因此不能据此补全。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MATH/MATH500：MATH共含12,500道竞赛数学题，其中7,500道训练题全部用于强化学习；MATH500是从原测试集抽取的500题代表性子集，用于评测。训练题与评测题不重叠，因此该设置主要检验方法对同类但未见问题的泛化能力。
- OlymMATH：包含200道人工作答与筛选的奥林匹克级数学题，覆盖四个主要数学领域，并划分为简单、困难子集；实验使用英文版本进行评测。它比常规竞赛题更难，主要用于观察方法是否改善高失败概率问题。
- AMC23与AIME24/AIME25：AMC23含40道2023年AMC 12A/12B题，用于检验高中竞赛数学能力；AIME24和AIME25各含30道题，覆盖代数、几何、数论和组合数学，其中AIME答案为0至999的整数。三者强调近期、较难且分布不同的竞赛问题。除MATH7.5K训练集外，这些基准与MATH500、OlymMATH共同组成统一验证集。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率**

衡量模型在评测题上生成正确最终答案的比例。实验定期评估各训练检查点，并在统一验证集上按准确率选择最佳检查点；它直接反映单次作答的总体正确性，但不能单独说明正确率是否集中在少数容易题上。 （越高越好，因为更高值表示更多问题被正确解决。）

</div>
<div class="metric-item" markdown="1">

**Gini系数**

衡量逐题成功概率的离散程度。在平均成功率相同的前提下，较低的Gini系数表示性能更均匀地分布于不同问题，而不是主要集中在少数题目上。该指标用于检验多矩目标是否改善问题之间的表现均衡性。 （越低越好，但这一判断以平均成功率可比为前提；若均值不同，不能只凭Gini系数判定方法整体更强。）

</div>
<div class="metric-item" markdown="1">

**Lorenz曲线**

将问题按逐题成功概率排序后，绘制累计问题比例与累计成功概率质量之间的关系。它是分布均衡性的图形化指标，可显示成功是否主要来自一小部分容易题。 （越接近45度平等线越好，因为这表示成功概率在问题之间分布得更均衡。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 五个数学推理基准与不同模型规模上的总体比较

<div class="result-value" markdown="1">

作者声称MMPO在全部实验设置中持续优于强基线，但所给章节没有提供对应表格、具体基线名称、各数据集准确率、提升幅度或统计不确定性。

</div>

这一结果若由完整结果表支持，说明联合优化多个失败概率矩在不同题集和模型规模下具有一致收益，而不是只在单一基准偶然有效。不过，仅凭当前定性陈述不能判断增益大小、训练成本、统计显著性，也不能确认每个单独数据集上是否都领先。

<div class="result-source" markdown="1">

来源：Abstract；所给摘录未包含Section 4.2的结果表

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Experiments across five mathematical reasoning benchmarks and models of different scales demonstrate that MMPO consistently outperforms strong baselines.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 附录B.1双策略玩具例子：仅比较第一矩与第四矩

<div class="result-value" markdown="1">

策略$\theta_2$的平均失败概率为$1/3$，低于$\theta_1$的$2/5$，因此第一矩偏好$\theta_2$；但$\theta_2$的第四矩为$1/9$，高于$\theta_1$的$1441/50000$，因此第四矩偏好$\theta_1$。这表明不同阶矩可对同一对策略给出相反排序。

</div>

第一矩只反映平均失败水平，高阶矩则对接近1的较大失败概率更敏感。该例说明只看平均值会忽略少数特别困难问题形成的上尾风险，但它是人为构造的分布示例，不是模型在真实基准上的性能证据。

<div class="result-source" markdown="1">

来源：Appendix B.1，Equation (69)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In contrast, their fourth moments satisfy $\mathbb{E}\!\left[F_{\theta_{1}}^{4}\right]=\frac{1441}{50000}<\frac{1}{9}=\mathbb{E}\!\left[F_{\theta_{2}}^{4}\right]$.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 附录B.1双策略玩具例子：联合前四阶矩

<div class="result-value" markdown="1">

前四阶失败概率矩之和在$\theta_1$上为$99023/150000$，小于$\theta_2$的$248/315$，因此MMPO式多矩目标偏好平均失败概率略高、但高阶矩和困难问题上尾更小的$\theta_1$。

</div>

该结果直观展示了MMPO的决策规则：它不只追求平均失败率最低，还会对少数问题上的持续失败施加更大压力。它证明了目标函数能够改变策略排序，但不能证明这种偏好必然提高真实测试准确率；真实收益仍需Section 4.2的完整实验数据验证。

<div class="result-source" markdown="1">

来源：Appendix B.1，Equation (70)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

When jointly considering the first four moments, the MMPO objective favors $\theta_{1}$, since $\sum_{k=1}^{4}\mathbb{E}\!\left[F_{\theta_{1}}^{k}\right]=\frac{99023}{150000}<\frac{248}{315}=\sum_{k=1}^{4}\mathbb{E}\!\left[F_{\theta_{2}}^{k}\right]$.

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

- GRPO：原文明确将其与MMPO用于逐题成功概率、Gini系数和Lorenz曲线的受控比较。它是有意义的比较对象，因为两种方法均属于面向大语言模型推理的策略优化方法，而MMPO的关键差别是显式联合处理失败概率的多个矩。
- 一阶矩方法：附录将其作为概念性对照，代表主要降低平均失败概率、但不直接约束失败概率分布高阶结构的方法。原文在所给章节中未列出该类别包含的全部具体算法。
- 不同矩变换目标：第4节说明实验会分析“transformation family”，用于比较不同矩权重或矩轮廓所诱导的策略目标。所给原文未包含具体变换名称及其逐项结果。
- 不同截断阶数的MMPO：通过改变联合纳入的矩的最高阶数，检验性能改善是否依赖高阶矩以及继续增加阶数是否仍然有益。所给原文未提供具体候选阶数和结果表。

**实验想回答的问题**

- MMPO在不同模型规模和五个数学推理基准上，能否比强基线取得更高的答案准确率，从而支持“联合优化多个失败概率矩比仅优化单一矩更有效”的核心主张？
- MMPO的收益是否确实来自高阶矩、截断阶数与矩变换族所形成的目标差异，以及这种目标是否能让成功概率更均匀地分布在不同难度的问题上？

**实验实现**

训练使用MATH的7,500题训练划分；MATH500、OlymMATH、AMC23、AIME24和AIME25合并为统一验证集。各方法采用相同评估频率，并报告该统一集合上准确率最高的检查点，以控制检查点选择造成的不公平。分析逐题分布时，MMPO和GRPO均对每道题独立采样16个回答，以正确性指示量$r_{i,j}^{(m)}$计算经验成功概率$\widehat{s}_{i}^{(m)}=\frac{1}{16}\sum_{j=1}^{16}r_{i,j}^{(m)}$。随后按共同阈值$\alpha$保留两种方法面对的同一组中等难度问题，避免极易题或两者均无法解决的极难题主导Gini与Lorenz比较。所给原文未报告模型名称、模型规模、优化器、训练步数、采样温度、主要结果表和随机种子。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 截断阶数分析 | 作者说明Section 4.3分析截断阶数，但所给原文未明确报告候选阶数、准确率变化或最佳阶数。 | 该消融应隔离“纳入多少阶失败概率矩”的作用：若从一阶增加到多阶后改善，才能直接支持高阶矩有用；若阶数过高后收益饱和或下降，则说明目标权重、估计方差或优化难度存在折中。由于结果缺失，当前不能判断上述趋势是否出现。 | Section 4 Experiments；Section 4.3具体内容未包含在所给摘录中<br><span class="experiment-evidence">Section 4.2 reports the overall performance, Section 4.3 analyzes the truncation order and transformation family, and Section 4.4 further examines the properties of the moment-based objective family.</span> |
| 矩变换族分析 | 作者说明Section 4.3比较不同变换族，Section 4.4进一步研究矩目标族的性质；所给原文未明确报告具体变换、数值结果或哪一种变换最优。 | 这一比较旨在判断收益是否只来自MMPO的某个固定公式，还是来自更一般的矩轮廓设计。若多个合理变换都优于一阶目标，可增强矩视角的普适性；若只有单一设置有效，则结论更可能依赖特定权重。当前摘录不足以作出判断。 | Section 4 Experiments；Sections 4.3-4.4具体内容未包含在所给摘录中<br><span class="experiment-evidence">Section 4.2 reports the overall performance, Section 4.3 analyzes the truncation order and transformation family, and Section 4.4 further examines the properties of the moment-based objective family.</span> |

**定性案例**

- 附录B.1构造$F_{\theta_1}\sim\operatorname{Unif}(0.3,0.5)$与$F_{\theta_2}\sim\operatorname{Beta}(1/2,1)$：$\theta_2$在零附近有更多概率质量，因而平均失败率更低，但同时具有更重的高失败率上尾；$\theta_1$的失败概率则更均匀。该案例直观说明MMPO可能牺牲少量平均指标来减少特别困难问题上的持续失败，不过作者称真实实验最终也改善了第一矩，这一后续主张在当前摘录中没有对应数值。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It proposes a policy-optimization objective trained with reinforcement learning to improve LLM mathematical reasoning.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`6d4d1e58e8752fa0688361aec997feffe04500824990303f913352a1c6c9a96a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
