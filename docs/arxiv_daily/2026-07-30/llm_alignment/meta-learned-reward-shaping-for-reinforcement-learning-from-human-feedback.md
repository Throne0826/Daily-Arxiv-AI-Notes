---
title: "[论文解读] Meta-Learned Reward Shaping for Reinforcement Learning from Human Feedback"
description: "[arXiv 2607.26094][对齐 / RLHF] 本文提出 MeRLa：在正式 RLHF 训练前，利用多个辅助任务元学习任务感知的奖励塑形函数，以补充静态奖励模型的信号，同时通过基于势函数的约束尽量保持原有最优策略不变。"
arxiv_id: "2607.26094"
announcement_date: "2026-07-30"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.665492+00:00"
source_sha256: "d9a72645821981870eb5095b9d31e84c037b920cf3396d387f26d0b12106813c"
tags:
  - "对齐 / RLHF"
  - "LLM 其他"
  - "强化学习"
  - "基于人类反馈的强化学习"
  - "大语言模型对齐"
  - "奖励塑形"
  - "元学习"
  - "势函数塑形"
  - "策略不变性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2607.26094</p>

# Meta-Learned Reward Shaping for Reinforcement Learning from Human Feedback

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Yunpeng Chu</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26094v1) · [PDF 下载](https://arxiv.org/pdf/2607.26094v1) · **关键词** 基于人类反馈的强化学习, 大语言模型对齐, 奖励塑形, 元学习, 势函数塑形, 策略不变性<br>


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

本文提出 MeRLa：在正式 RLHF 训练前，利用多个辅助任务元学习任务感知的奖励塑形函数，以补充静态奖励模型的信号，同时通过基于势函数的约束尽量保持原有最优策略不变。

**不用术语来说**：同一个通用奖励模型需要评价推理、创作、安全和事实准确性等差异很大的回答，但它往往无法识别细微而又与任务相关的质量差别，导致许多回答得到近似分数；模型因此缺少清晰的改进方向，甚至可能学会钻奖励模型的漏洞。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出面向 RLHF 的元学习奖励塑形框架 MeRLa，从辅助任务经验中学习任务感知函数 Φ(x,y;φ)，无需为每个目标任务重新手工设计奖励或增加人工偏好标签。
- 将任务区分、熵正则化与基于势函数的守恒约束组合为元目标，并围绕策略不变性、表示漂移敏感性和熵最大化造成的激励错位给出理论分析。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型的偏好对齐研究。标准的基于人类反馈的强化学习（RLHF）先用成对偏好数据训练奖励模型，再把语言模型视为策略，使用 PPO、GRPO 等强化学习算法提高生成回答的奖励，同时通过 KL 散度约束模型不要过度偏离监督微调后的参考策略。本文关注这一流程中的奖励信号：同一个静态、任务无关的奖励模型需要评价推理、创作、安全与事实性等差异很大的提示，因而可能无法区分细微质量差异，并可能诱发对奖励模型漏洞的利用。其理论基础是势函数奖励塑形，即在基础奖励上加入具有特定差分形式的辅助奖励，以改善学习信号而不改变原问题的最优策略。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**基于人类反馈的强化学习（RLHF）**

RLHF利用人类对回答的偏好训练奖励模型，再优化语言模型，使其生成更符合这些偏好的回答。训练通常还加入相对参考策略的 KL 惩罚，以限制模型行为发生过大偏移。

</div>
<div class="concept-item" markdown="1">

**奖励塑形（Reward Shaping）**

奖励塑形是在原始奖励之外加入辅助信号，使策略更容易判断哪些行为值得鼓励。若辅助项设计不当，它也可能改变模型真正追求的目标，因此需要结构性约束。

</div>
<div class="concept-item" markdown="1">

**势函数奖励塑形（Potential-Based Reward Shaping）**

该方法把辅助奖励写成相邻状态势值之差：\(\Phi(s,s')=\gamma\phi(s')-\phi(s)\)。在经典强化学习条件下，这种形式可保持最优策略不变，直观上只是重新分配学习过程中的奖励，而不是更换最终目标。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括提示分布中的提示 \(x\)、语言模型按自回归方式生成的回答 \(y\)，以及由偏好数据训练得到的基础奖励模型 \(R_{\mathrm{base},\psi}(x,y)\)。策略 \(\pi_\theta\) 的输出是回答上的条件概率分布；标准目标最大化生成回答的期望基础奖励，同时用系数 \(\beta\) 加权的 KL 散度约束其接近监督微调参考策略 \(\pi_{\mathrm{ref}}\)。本文所处的问题设置是在正式 RLHF 训练前利用辅助任务学习任务感知的塑形函数 \(\Phi(x,y;\phi)\)，随后将其与基础奖励组合，为不同任务提供更细致的训练信号；关键假设是塑形项受到势函数形式约束，从而在改善优化过程的同时保持基础奖励所诱导的最优策略。原文指出辅助任务经验无需额外人类标签，但所给节选未明确说明辅助任务的具体构造。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\pi_\theta(y\mid x)=\prod_{t=1}^{|y|}\pi_\theta(y_t\mid x,y_{<t})$**

参数为 \(\theta\) 的自回归语言模型策略；给定提示 \(x\) 后，完整回答 \(y\) 的概率等于各位置词元条件概率的乘积。

</div>
<div class="notation-item" markdown="1">

**$R_{\mathrm{base},\psi}(x,y)$**

参数为 \(\psi\) 的基础奖励模型，对提示 \(x\) 与回答 \(y\) 的匹配质量给出标量评价。

</div>
<div class="notation-item" markdown="1">

**$\max_\theta\mathbb{E}_{x\sim D,\,y\sim\pi_\theta(\cdot\mid x)}\left[R_{\mathrm{base}}(x,y)-\beta\,\mathrm{KL}(\pi_\theta\|\pi_{\mathrm{ref}})\right]$**

标准 RLHF 优化目标：提高期望基础奖励，同时以强度 \(\beta\) 惩罚当前策略与参考策略之间的 KL 偏离；来源为 Preliminaries 的公式（1）。

</div>
<div class="notation-item" markdown="1">

**$\Phi(s,s')=\gamma\phi(s')-\phi(s)$**

势函数塑形项；\(s,s'\) 是相邻状态，\(\phi:S\to\mathbb{R}\) 为状态势函数，\(\gamma\) 为折扣因子。将其加入原奖励得到 \(R'=R+\Phi\)，可在经典条件下保持最优策略不变。

</div>

</div>

**直接相关的工作**

- **Ng, Harada, and Russell (1999), Policy Invariance under Reward Transformations: Theory and Application to Reward Shaping**: 提供势函数奖励塑形及策略不变性的理论基础。本文据此约束学习到的塑形信号，避免辅助奖励改变基础奖励对应的最优策略。
- **Zou et al. (2019), Reward Shaping via Meta-Learning**: 与本文最直接相关的是利用元学习获得奖励塑形函数；本文将这一思想用于大语言模型 RLHF，并针对任务感知奖励、策略不变性及稳定训练提出相应设计。所给节选未提供两者在算法细节上的完整比较。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

标准 RLHF 先用成对偏好数据训练奖励模型 R_ψ，再通过 PPO、GRPO 或 DPO 等方法优化语言模型策略。由于 R_ψ 通常来自静态、任务无关的数据，它对不同类型提示使用相对固定的评价信号，难以持续提供细粒度、任务适配的学习反馈。这会降低对齐效率，并可能使进一步优化损害模型原有的通用能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **静态奖励模型驱动的 RLHF 或偏好优化**：先从成对偏好数据学习一个固定奖励模型，再用 PPO、GRPO 等强化学习算法最大化该奖励；DPO 则直接利用偏好对优化策略。它们的共同基础是已有偏好信号能够充分表达目标行为。
- **人工、学习式或模型生成的奖励塑形**：在基础奖励之外加入辅助奖励，引导策略更快识别优质输出。人工方法按任务编写规则；学习式方法从数据中拟合塑形信号；自奖励与 AI 反馈方法则让模型或外部模型产生评价。基于势函数的塑形还可在满足特定形式时保持最优策略不变。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 静态、任务无关的奖励模型无法充分分辨跨任务的细微质量差异，容易产生奖励稀疏；持续针对这一窄信号优化还可能导致奖励过度优化，即策略利用评分盲点，以及“对齐税”，即通用能力因过度迎合奖励而下降。
- 现有奖励塑形存在安全性与成本权衡：人工设计依赖逐任务专业知识；不受约束的学习式塑形可能改变原奖励所诱导的最优策略；自奖励或 AI 生成奖励又可能依赖有缺陷的自我判断，并增加推理成本。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚缺少一种可在正式 RLHF 之前从多个辅助任务自动提炼奖励知识、对新任务提供细粒度塑形信号，并同时以明确约束控制策略偏移的统一方案。尤其需要兼顾任务适应性、无需额外人工标签以及近似保持原始优化目标这三项要求。

</div>
<div markdown="1"><span>核心问题</span>

能否元学习一个以提示 x、回答 y 和参数 φ 为输入的任务感知塑形函数 Φ(x,y;φ)，使其在增强 RLHF 学习信号和训练稳定性的同时，通过基于势函数的守恒约束保持策略最优性，并避免熵激励或表示漂移引入不可控偏差？

</div>
<div markdown="1"><span>作者直觉</span>

多个辅助任务反复呈现了“什么样的奖励能有效区分回答并推动策略改进”的共同结构。与其为每个任务手工写规则，不如先让塑形网络从这些任务中学会生成有辨别力的补充信号；再用守恒约束限制它只能改变学习路径而非最终目标。直观地说，基础奖励决定模型应到达哪里，元学习塑形则提供更密集、因任务而异的路标。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MeRLa 是一个先学习奖励塑形、再执行常规 RLHF 的两阶段框架。第一阶段从多个辅助任务的偏好对中训练轻量塑形函数，使其既能区分优劣回答、提供较丰富的奖励信号，又尽量符合基于势函数的奖励塑形形式；第二阶段冻结该函数，将其输出与基础奖励模型相加，再用 GRPO、PPO 或 DAPO 等算法更新语言模型策略。塑形函数的输入表示始终由冻结的参考模型提取，以避免策略训练期间表示空间变化造成奖励漂移。
直观上，基础奖励模型只给出一个较笼统的“总分”，MeRLa 学习一个面向任务的“附加评分提示”，让策略更容易判断改进方向。这个附加信号受到势函数约束，目标是改变学习过程的难易和稳定性，而不是改变原基础奖励所定义的最优答案；但原文实际使用的是保守损失所实现的近似约束，因此严格的策略不变性只对完全满足势函数分解的情形成立。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造跨任务元学习样本

对每个辅助任务采样提示和回答偏好对，并用冻结参考模型的倒数第二层提取提示嵌入 $h_x$ 与回答嵌入 $h_y$。基础奖励模型同时为回答提供原始质量信号。

<div class="method-step__io" markdown="1">

**输入**：辅助任务分布 $\mathcal{T}=\{\tau_1,\ldots,\tau_M\}$、各任务提示 x、偏好回答 $y^{+}$ 与拒绝回答 $y^{-}$、基础奖励模型 $R_{\mathrm{base},\psi}$ 及参考策略 $\pi_{\mathrm{ref}}$。<br>
**输出**：表示稳定的跨任务训练批次，以及每个回答对应的基础奖励。

</div>

**直观理解**：这一步准备多种任务上的“好回答—差回答”示例，并用一把训练期间不变化的尺子表示文本，避免后续评分器面对不断移动的特征坐标系。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算任务感知的复合奖励

将 $h_x$、$h_y$ 和差分 $h_y-h_x$ 拼接后输入两层 MLP，得到标量塑形值 $\Phi(x,y;\phi)$，再按权重 $\alpha$ 加到基础奖励上。塑形还可按生成前缀分解为逐词势差，以对应潜在函数奖励塑形。

<div class="method-step__io" markdown="1">

**输入**：冻结编码器产生的 $h_x$、$h_y$，以及基础奖励 $R_{\mathrm{base},\psi}(x,y)$。<br>
**输出**：复合奖励 $\hat{R}(x,y;\phi,\psi)$。

</div>

**直观理解**：MLP 不直接替换原评分器，而是在原分数上增加一个小的任务相关修正；提示与回答的差分帮助它描述回答相对问题语境发生了什么变化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 元学习塑形函数

联合最小化任务判别损失、负熵正则和保守损失，并通过梯度下降更新塑形参数 $\phi$。任务损失要求偏好回答得分更高，熵项防止奖励退化为常数，保守项惩罚其偏离势函数形式。

<div class="method-step__io" markdown="1">

**输入**：各辅助任务中的复合奖励、偏好标签，以及逐词势函数投影 $\Phi_{\mathrm{pb}}$。<br>
**输出**：跨辅助任务学习得到并随后冻结的参数 $\phi^{*}$。

</div>

**直观理解**：训练同时要求附加评分“有区分度”和“不过界”：既不能所有回答都给同一分，也不能为了拉开分数而任意改写原来的优劣排序。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 使用元塑形奖励执行 RLHF

当前策略生成回答后，系统计算基础奖励与塑形奖励之和，并加入相对参考策略的 KL 惩罚；随后用 GRPO、PPO 或 DAPO 等在线 RLHF 优化器更新 $\theta$，而不再更新 $\phi^{*}$。

<div class="method-step__io" markdown="1">

**输入**：目标训练提示集 D、当前策略 $\pi_\theta$、冻结参考策略 $\pi_{\mathrm{ref}}$、基础奖励模型和冻结塑形函数 $\Phi(\cdot;\phi^{*})$。<br>
**输出**：在复合奖励指导下训练完成的对齐策略 $\pi_\theta$。

</div>

**直观理解**：部署阶段把学到的附加评分器当作固定教练，策略根据更细致的反馈改进；KL 惩罚则限制模型不要为了追逐奖励而偏离原参考模型过远。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 跨任务元学习目标

$$
\min_{\phi}\mathcal{L}_{\mathrm{meta}}(\phi)=\sum_{i=1}^{M}\left[\mathcal{L}_{\mathrm{task}}^{(i)}(\phi)+\lambda_{1}\mathcal{L}_{\mathrm{ent}}(\phi)+\lambda_{2}\mathcal{L}_{\mathrm{con}}(\phi)\right]
$$

**符号说明**

- $\phi$：奖励塑形网络的可学习参数。
- $\mathcal{L}_{\mathrm{meta}}$：汇总全部辅助任务及正则项的元学习总损失。
- $M$：辅助任务的数量。
- $i$：辅助任务索引。
- $\mathcal{L}_{\mathrm{task}}^{(i)}$：第 i 个任务上的偏好判别损失，促使复合奖励给予 $y^{+}$ 高于 $y^{-}$ 的分数。
- $\mathcal{L}_{\mathrm{ent}}$：负熵正则项；最小化它等价于提高批内复合奖励分布的熵，防止输出坍缩为常数。
- $\mathcal{L}_{\mathrm{con}}$：保守损失，度量塑形输出与基于势函数的投影之间的平方偏差。
- $\lambda_1$：熵正则的权重。
- $\lambda_2$：保守损失的权重。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标在三个要求之间折中：能识别每个任务中的优劣回答、产生非退化且信息丰富的奖励、同时不要明显偏离保证策略不变性的势函数结构。它是第一阶段唯一更新 $\phi$ 的总目标，得到的 $\phi^{*}$ 在部署阶段保持冻结。<br>
**原文位置**：Method，Meta-Learning Objective，Equation (5)

</div>

</div>

<div class="equation-block" markdown="1">

#### 带元塑形奖励的 RLHF 目标

$$
\max_{\theta}\mathbb{E}_{x\sim D,\,y\sim\pi_{\theta}(\cdot\mid x)}\left[R_{\mathrm{base},\psi}(x,y)+\alpha\Phi(x,y;\phi^{*})-\beta\,\mathrm{KL}(\pi_{\theta}\|\pi_{\mathrm{ref}})\right]
$$

**符号说明**

- $\theta$：部署阶段需要优化的语言模型策略参数。
- $\mathbb{E}$：对训练提示及当前策略采样回答所取的期望。
- $D$：部署阶段 RLHF 使用的目标提示数据分布。
- $x$：输入提示。
- $y$：当前策略针对提示生成的回答。
- $\pi_{\theta}(\cdot\mid x)$：给定提示 x 时当前自回归语言模型的回答分布。
- $R_{\mathrm{base},\psi}$：参数为 $\psi$ 的基础奖励模型。
- $\alpha$：塑形奖励强度，原文规定 $\alpha\in[0,1]$。
- $\Phi$：任务感知的奖励塑形函数。
- $\phi^{*}$：元学习结束后冻结的塑形参数。
- $\beta$：KL 偏离惩罚的权重。
- $\mathrm{KL}(\pi_{\theta}\|\pi_{\mathrm{ref}})$：当前策略相对于监督微调参考策略的 KL 散度惩罚。
- $\pi_{\mathrm{ref}}$：冻结的监督微调参考策略，也用于提供稳定文本嵌入。

<div class="equation-explanation" markdown="1">

**直观理解**：部署时，策略最大化“基础奖励＋任务塑形奖励”，同时因偏离参考模型而付出 KL 代价。塑形项提供更密集或更有区分度的学习方向，KL 项限制过度偏移；若 $\Phi$ 严格采用势函数形式，则理论上只改变学习路径而不改变基础奖励定义的最优策略。<br>
**原文位置**：由 Method 的 Equation (2) 代入 Deployment: RLHF with Meta-Shaped Rewards 的 Equation (9)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：第一阶段固定基础奖励模型和参考编码器，仅对塑形参数 $\phi$ 做梯度下降。每个辅助任务的判别损失采用二选一的 softmax 交叉熵，要求偏好回答 $y^{+}$ 的复合奖励高于拒绝回答 $y^{-}$；负熵项扩大批内奖励分布的有效区分度；保守项通过与逐词势函数分解的最小二乘投影比较，限制塑形信号改变原奖励排序的能力。原文理论保证针对严格满足势函数分解的 $\Phi$，而实际网络通过 $\mathcal{L}_{\mathrm{con}}$ 近似该条件，因此应将实际方法理解为受控近似，而非无条件的严格策略不变。
第二阶段冻结 $\phi^{*}$，只优化策略参数 $\theta$。每轮从 D 采样提示，由 $\pi_\theta$ 生成回答，计算复合奖励和 KL 惩罚，再交给 GRPO、PPO 或 DAPO 更新策略；其中 GRPO 是论文主要采用的骨干优化器。原文还提到谱归一化和梯度范数形式的漂移正则用于控制塑形网络敏感度，但它们没有出现在给出的 Equation (5) 总目标中，二者如何与元目标合并的细节原文摘录未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 轻量奖励塑形网络**

塑形函数采用 $\Phi(x,y;\phi)=\mathrm{MLP}_{\phi}(h_x\oplus h_y\oplus(h_y-h_x))$。网络是隐藏维度为 256、使用 SiLU 激活的两层 MLP，参数量少于 1M；输入来自基础 LLM 倒数第二层，输出为一个标量。

> 直观理解：该模块学习基础奖励没有表达充分的任务相关差异。拼接提示、回答及二者差分，使它既能看到各自内容，也能判断回答相对提示的偏移。

**2. 冻结参考编码器与漂移控制**

$h_x$ 和 $h_y$ 由冻结的 $\pi_{\mathrm{ref}}$ 提取，而不是由持续更新的 $\pi_\theta$ 提取；塑形 MLP 还采用谱归一化以限制其 Lipschitz 常数。固定编码器使同一输入的表示漂移为零，并将塑形学习与策略更新解耦。

> 直观理解：如果用正在训练的策略提取特征，同一句话在不同训练阶段可能得到不同坐标，固定塑形器的输出便会无故变化。冻结编码器相当于固定评分标尺，使奖励变化主要反映回答变化，而非内部表示漂移。

**3. 近似势函数约束**

回答级塑形被表示或投影为 $\Phi(x,y;\phi)=\sum_{t=1}^{|y|}[\gamma\varphi_\phi(x,y_{\le t})-\varphi_\phi(x,y_{<t})]$，并通过最小二乘得到势函数空间中的投影 $\Phi_{\mathrm{pb}}$；保守损失惩罚 $\Phi$ 与该投影之间的平方偏差。若分解被严格满足，逐步势差会望远镜式相消，从而保持基础奖励对应的最优策略；实际训练只保证近似满足，因此仍可能存在残差偏差。

> 直观理解：这项设计让附加奖励更像沿途路标：它可以告诉模型下一步是否更接近目标，却原则上不应换掉终点。保守损失就是防止路标本身变成一个新的、可能被钻空子的目标。

**训练与推理**

完整训练分为两个阶段。元学习阶段遍历 M 个辅助任务：采样 x 和 ($y^{+},y^{-})$，由冻结参考模型提取 $h_x$、$h_y$，计算基础奖励与塑形奖励，累计任务判别、熵和保守损失，然后以学习率 $\eta_\phi$ 更新 $\phi$；完成 $T_{\mathrm{meta}}$ 个周期后得到并冻结 $\phi^{*}$。RLHF 部署阶段进行 $T_{\mathrm{rl}}$ 个周期：从目标分布 D 采样提示，当前策略自回归生成回答，固定塑形器与基础奖励模型共同给出复合奖励，再通过选定的在线 RLHF 算法更新 $\theta$。
最终推理时仅需使用训练完成的策略 $\pi_\theta$ 生成回答；塑形网络服务于训练奖励计算，而不是文本生成过程本身。原文算法返回的是 aligned policy $\pi_\theta$，未说明推理阶段必须继续运行基础奖励模型或塑形网络。

**复现信息**

塑形网络为两层 MLP，隐藏维度 256，激活函数为 SiLU，新增参数少于 1M；输入是冻结参考模型倒数第二层产生的提示嵌入、回答嵌入及二者差分。参考模型本来就用于标准 RLHF 的 KL 惩罚，因此作者称冻结编码器不增加额外模型内存；但提取塑形输入及运行 MLP 仍涉及计算开销，摘录未给出具体吞吐量。
塑形强度满足 $\alpha\in[0,1]$，网络采用谱归一化限制 Lipschitz 常数；势函数投影通过对逐词势差分解做最小二乘获得。主要部署优化器为 GRPO，方法也声明兼容 PPO 和 DAPO。元学习任务组成、$\alpha$、$\beta$、$\lambda_1$、$\lambda_2$、学习率、批量大小、训练周期、势函数投影的具体求解过程，以及提示与回答嵌入的池化方式在所给摘录中均未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- UltraFeedback：用于训练显式奖励模型，并作为各比较方法共享的偏好数据来源；采用何种划分、样本规模及辅助元任务的具体构造，所给原文未明确报告。
- AlpacaEval 2.0：测试单轮指令遵循能力；使用 GPT-4-Turbo 作为裁判，报告长度控制胜率，以降低较长回答天然占优造成的偏差。评测样本规模和划分在所给原文中未明确报告。
- MT-Bench、MATH 与 IFEval：分别测试多轮对话、数学推理和具有可验证约束的指令遵循。受列表数量限制合并列示；三者的评测规模、划分及 MATH/IFEval 的具体评分协议在所给原文中未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**AlpacaEval 2.0 长度控制胜率（LC win rate）**

由 GPT-4-Turbo 比较模型回答并进行长度校正后，模型回答胜出的比例；主要衡量开放式指令遵循质量，同时减少回答长度对裁判偏好的干扰。 （越高越好，因为更高比例表示在长度因素受控后，回答更常被裁判偏好。）

</div>
<div class="metric-item" markdown="1">

**MT-Bench 分数**

基于模型裁判的多轮对话质量评分，用于考察回答质量及跨轮次保持上下文和完成任务的能力。 （越高越好，因为更高分表示多轮对话的综合质量更优。）

</div>
<div class="metric-item" markdown="1">

**训练奖励方差**

衡量不同训练过程或训练阶段中所得奖励的波动程度，正文以相对降幅描述 MeRLa 的训练稳定性。 （通常越低越好，因为较小波动意味着优化过程更稳定；但它不能单独证明最终任务质量更高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### LLaMA-3-8B-Instruct 上，以 GRPO 为骨干的 MeRLa 与 DAPO 等方法进行四基准综合比较。

<div class="result-value" markdown="1">

作者报告 MeRLa 在 AlpacaEval 2.0 达到 90.8% 的长度控制胜率，较 DAPO 高 3.9 个百分点；相对比较对象还在 MT-Bench、MATH 和 IFEval 上分别提高 0.33 分、5.6% 和 3.9%，且配对 t 检验均达到 p<0.05。

</div>

结果表明，元学习奖励塑形的收益并未局限于开放式指令评测，而是覆盖多轮对话、数学推理和可验证指令遵循。由于 MeRLa 使用 GRPO 骨干，最有辨识力的比较应是 MeRLa 与未塑形 GRPO；但所给节选只明确给出了相对 DAPO 的差值，且未提供 Table 1 的完整逐项数值，因此无法核验各基线上的绝对优势。这些结果支持跨任务有效性，但不能证明在其他模型规模、奖励模型或人工裁判下同样成立。

<div class="result-source" markdown="1">

来源：Experiments—Main Results，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MeRLa (GRPO backbone) achieves 90.8% LC win rate on AlpacaEval 2.0, outperforming DAPO by 3.9 points. Gains are consistent across all benchmarks: +0.33 on MT-Bench, +5.6% on MATH, and +3.9% on IFEval, all statistically significant (p < 0.05, paired t-test).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### RLHF 训练过程中的收敛速度与奖励波动比较，主要对照 MeRLa、DAPO 和 PPO。

<div class="result-value" markdown="1">

MeRLa 在前 150 个训练步骤内达到最终奖励的 90%，DAPO 需要 250 步，PPO 则需要至少 350 步；同时，MeRLa 的奖励方差低 41%。

</div>

该结果测试 MeRLa 是否提供了更稠密、更容易优化的学习信号：更早达到最终奖励的 90% 表示样本或更新效率更高，方差下降则表示训练波动较小。不过，这里的“最终奖励”由实验奖励体系定义，未必等价于真实人类偏好；41% 的方差降幅也没有在节选中给出误差条或显著性检验。

<div class="result-source" markdown="1">

来源：Analysis—Reward Signal Quality，Figure 5(a)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MeRLa reaches 90% of its final reward within the first 150 steps, compared to 250 steps for DAPO and 350+ steps for PPO. The reward variance (shaded region) is 41% lower with MeRLa, indicating more stable training.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 在 2,000 个留出偏好对上，对基础奖励模型、人工设计奖励塑形和 MeRLa 的奖励分布进行比较。

<div class="result-value" markdown="1">

作者报告基础奖励模型的奖励标准差为 0.80；MeRLa 的平均奖励为 1.1，而对照值为 0.8，标准差降至 0.35，并称其对高、低质量回答的分离更好。

</div>

该分析试图说明 MeRLa 不只是整体抬高奖励，而是将信号变得更集中并增强质量区分，从而可能形成更平滑的优化目标。不过，均值更高和方差更低本身不必然代表奖励更准确；真正关键的是与人类质量排序的一致性，而节选没有给出排序相关性、校准误差或分离度的定量指标。

<div class="result-source" markdown="1">

来源：Analysis—Reward Signal Quality，Figure 4(a)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The base reward model produces a wide, bimodal distribution with high variance (σ=0.80). Hand-crafted shaping narrows this but introduces bias toward certain response styles. MeRLa achieves the most desirable distribution: higher mean (μ=1.1 vs. 0.8), lower variance (σ=0.35), and better separation between high and low-quality responses.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给节选缺少 Table 1 的完整分数、标准差或置信区间，也未说明 MATH 与 IFEval 上百分比增益是绝对百分点还是相对增幅；虽然作者报告配对 t 检验 p<0.05，但样本配对方式和多重比较处理未明确，主要数值仍需回查原表。
- 实验仅明确覆盖 LLaMA-3-8B-Instruct、一个共享奖励模型及以自动裁判为主的评测；GPT-4-Turbo 裁判可能带有风格偏好，奖励分布和 t-SNE 景观又是代理分析，因此尚不能据此确认 MeRLa 在更大模型、不同奖励模型或真实人工偏好评测中保持相同优势。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- PPO：经典的基于显式奖励模型和策略梯度的 RLHF 方法，用于判断奖励塑形相对标准 RLHF 流程是否有效。
- DPO：不显式训练在线强化学习策略、直接从偏好对优化策略的方法，用于比较 MeRLa 与另一类主流对齐范式。
- GRPO：MeRLa 实验所采用的 RLHF 骨干；比较原始 GRPO 与加入 MeRLa 的 GRPO，可以较直接地识别奖励塑形带来的增益。
- DAPO：较强的策略优化基线，也是正文中用于报告主要差值和收敛速度的直接竞争方法。所有方法共享基础模型与偏好数据；需要显式奖励模型的方法还共享同一奖励模型检查点。

**实验想回答的问题**

- 在相同基础模型与偏好数据下，加入元学习奖励塑形的 MeRLa，是否能比主流 RLHF 与直接偏好优化方法更好地提升指令遵循、对话和推理能力？
- MeRLa 的收益是否来自更有信息量且更稳定的奖励信号，以及冻结编码器、势函数约束等关键设计是否确实有助于稳定训练并避免改变原奖励的偏好排序？

**实验实现**

基础策略为 LLaMA-3-8B-Instruct；奖励模型在 UltraFeedback 上训练，并使用秩为 16 的 LoRA。MeRLa 的塑形网络是带 SiLU 激活和谱归一化的两层 MLP，隐藏维度为 256；设置 64 个元任务，塑形强度 α=0.3，两个目标权重 λ1=0.05、λ2=0.1。RLHF 阶段使用 GRPO，组大小为 8、KL 系数 β=0.004、学习率为 10^-6，共训练 20 个 epoch，硬件为 8 张 A100-80GB。AlpacaEval 2.0 使用 GPT-4-Turbo、标准贪心裁判模板和温度 0；模型回答也通过贪心解码生成，最大长度为 2048 tokens，并对三个随机种子取平均。除 AlpacaEval 外，其余基准的解码、重复次数及统计检验细节在所给原文中未完整说明。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 冻结参考编码器与使用持续更新的策略编码器计算提示和回答表示。 | 在 1,000 个训练步骤中，冻结编码器时塑形输出方差为 0.002，使用演化编码器时为 0.087，即增加 43 倍；AlpacaEval 2.0 最终胜率也从 90.8% 降至 87.1%。 | 该消融隔离了“表示漂移”的影响：塑形函数在元学习后固定时，若输入表示随策略更新而改变，同一类文本可能得到不稳定的塑形奖励。方差显著上升并伴随胜率下降，支持冻结编码器这一设计。不过该比较同时改变了表示来源，尚不能区分漂移幅度、编码器质量和其他训练交互各自的贡献。 | Theoretical Analysis—Representation Drift Sensitivity—Empirical Validation<br><span class="experiment-evidence">With the frozen encoder, the shaping output variance across 1,000 training steps is 0.002 (negligible). With the evolving encoder, the variance is 0.087 — a 43× increase. The final AlpacaEval 2.0 win rate drops from 90.8% (frozen) to 87.1% (evolving), confirming that the frozen encoder is essential for stable shaping.</span> |

**定性案例**

- Figure 5(b) 的 t-SNE 二维投影显示，基础奖励景观存在多个局部极大值，而 MeRLa 的等高线更平滑并呈现通往全局最优点的清晰路径。该图可直观解释更快收敛，但 t-SNE 会扭曲高维距离，因此它只能作为定性示意，不能独立证明真实参数空间中的局部最优确实减少。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出用于 LLM RLHF 的元学习任务感知奖励塑形方法，核心贡献属于奖励建模与对齐后训练。; rule check: matched taxonomy keywords; top rule score=12.0
- 全文指纹：`d9a72645821981870eb5095b9d31e84c037b920cf3396d387f26d0b12106813c`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
