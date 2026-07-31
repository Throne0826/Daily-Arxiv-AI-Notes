---
title: "[论文解读] RL$^2$-VLA: Adaptive RL Latent Compositional Steering with Test-Time Scaling for Vision-Language-Action Models"
description: "[arXiv 2607.26991][机器人 / 具身智能] 本文针对视觉-语言-动作模型在困难或分布外任务中容易失效、现有测试时干预又缺乏动作多样性与状态适应性的问题，提出根据失败预测选择性启用离线强化学习潜变量组合引导的框架 $RL^2$。"
arxiv_id: "2607.26991"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T05:30:51.322295+00:00"
source_sha256: "70340e267455516ca85f7211f2bdbd3eb31996029e102df9aef1c2f7d2bcdda4"
tags:
  - "机器人 / 具身智能"
  - "强化学习"
  - "视觉-语言-动作模型"
  - "分布外泛化"
  - "测试时引导"
  - "测试时扩展"
  - "流匹配"
  - "离线强化学习"
  - "动作多样性"
  - "失败检测"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2607.26991</p>

# RL$^2$-VLA: Adaptive RL Latent Compositional Steering with Test-Time Scaling for Vision-Language-Action Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Tan, Derek Ming Siang, Shailesh, Shailesh, Iyer, Srikrishna, Teo, William Wei Jie, Ju, Yuanliang, Gu, Qiao, Sartoretti, Guillaume</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> National University of Singapore；University of Toronto</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26991) · [PDF 下载](https://arxiv.org/pdf/2607.26991) · **关键词** 视觉-语言-动作模型, 分布外泛化, 测试时引导, 测试时扩展, 流匹配, 离线强化学习, 动作多样性, 失败检测<br>


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

本文针对视觉-语言-动作模型在困难或分布外任务中容易失效、现有测试时干预又缺乏动作多样性与状态适应性的问题，提出根据失败预测选择性启用离线强化学习潜变量组合引导的框架 $RL^2$。

**不用术语来说**：机器人原有策略在熟悉场景中可能已经能做出正确动作，但面对未见过的物体、指令或环境时，往往会反复尝试相似动作并以相似方式失败。现有部署期增强方法通常不判断机器人此刻是否真的需要帮助，而是在每个时间步统一干预；这既难以在失败时找到真正不同的解决方案，也可能在原动作正确时把它扰乱。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出一种组合引导思路：使用视觉-语言-动作模型动作专家的潜变量训练轻量级离线强化学习策略，并在推理时加权组合强化学习策略与冻结基础模型的流速度，从而将大规模模仿学习形成的行为先验与强化学习产生的高价值、多样化动作结合起来。
- 将测试时缩放分析分别用于基础策略的成功状态和失败状态，并据此引入失败检测器 SAFE：预测失败时启用组合引导，预测成功时退回基础视觉-语言-动作策略，形成自适应干预机制。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

视觉-语言-动作模型（Vision-Language-Action, VLA）把视觉观测、机器人本体状态和自然语言指令映射为连续控制动作，通常依靠大规模机器人示范进行模仿学习。此类模型在训练分布内已具备较强的通用操作能力，但面对未见指令、物体或环境时，成功率可能显著下降；测试时引导与测试时扩展因此尝试在不重新训练主模型的条件下，通过调整动作生成过程或采样多个候选动作来提高部署鲁棒性。本文关注带流匹配动作头的冻结 VLA：动作并非一次性回归得到，而是由速度场逐步将噪声变换成动作轨迹，这为推理阶段组合其他策略的速度场提供了接口。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉-语言-动作模型（VLA）**

VLA 是一种机器人策略，以图像、机器人本体状态和语言任务指令为条件，输出未来若干步组成的动作块。它通常从大量示范中学习，因此擅长复现训练数据中的行为模式，但不保证在分布外场景中仍能可靠执行。

</div>
<div class="concept-item" markdown="1">

**模仿学习与离线强化学习**

模仿学习通过最大化示范动作的似然来复现数据集中的行为；离线强化学习则只使用既有数据，根据奖励或回报判断行为价值并优化策略。前者提供稳定的行为先验，后者有机会偏离示范中的主导模式，发现回报更高的替代动作。

</div>
<div class="concept-item" markdown="1">

**流匹配与推理时引导**

流匹配策略使用随生成进度变化的速度场，把初始噪声连续运输为可执行的动作轨迹。推理时引导通过修改该速度场来改变生成方向，从而无需更新冻结主策略的参数，也能使候选动作更符合额外目标。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定离线示范数据集 $\mathcal{D}=\{o_i,a_i,\ell_i\}_{i=1}^{N}$，其中 $o_i$ 是视觉及可能包含的机器人本体观测，$a_i$ 是示范动作，$\ell_i$ 是语言指令；基础策略在时刻 $t$ 根据 $o_t$ 与 $\ell_t$ 生成长度由预测范围 $H$ 决定的动作块 $a_{t:t+H}$。部署时基础 VLA 保持冻结，研究场景同时包括训练分布内任务和具有未见指令、物体或环境的分布外任务。核心问题是：如何利用额外的测试时计算产生既高质量又不局限于基础策略主导行为模式的候选动作，以及何时应当介入生成过程；其隐含要求是，干预要能帮助基础策略可能失败的状态，同时避免扰动原本已经准确的动作。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{D}=\{o_i,a_i,\ell_i\}_{i=1}^{N}$**

包含 $N$ 个机器人示范样本的离线数据集，每个样本由观测、动作和语言指令组成。

</div>
<div class="notation-item" markdown="1">

**$\pi_{\theta}(a_{t:t+H}\mid o_t,\ell_t)$**

参数为 $\theta$ 的策略在当前观测与语言指令条件下，对未来动作块给出的条件分布。

</div>
<div class="notation-item" markdown="1">

**$v(o,a,\ell,k)$**

流匹配动作生成器的速度场；$k$ 表示生成进度，该速度场决定当前动作变量沿何种方向演化。

</div>
<div class="notation-item" markdown="1">

**$R=\mathbb{E}\left[\sum_{t=1}^{T}\gamma^{t-1}r^t\right]$**

强化学习所最大化的期望累计折扣回报，其中 $T$ 是任务时域，$r^t$ 是第 $t$ 步奖励，$\gamma$ 是折扣因子。

</div>

</div>

**直接相关的工作**

- **离散动作选择与测试时扩展方法 [19, 20, 29]**: 这些方法从同一 VLA 多次采样，或通过改写语言指令增加候选动作，再由外部验证器选择结果。它们保留基础策略的动作分布，但候选样本仍可能共享相关偏差与失败模式，因此难以充分覆盖分布外任务所需的替代行为。
- **SAFE [11]**: SAFE 是面向 VLA 的失败检测器。本文将其作为自适应决策组件：预测到失败时启用组合引导，预测成功时退回基础 VLA，从而区分需要探索替代动作与应当保留准确动作的状态。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

视觉-语言-动作模型依赖大规模机器人示范与视觉-语言模型先验，虽然在训练分布内的操作任务上表现较强，但在未见语言指令、物体或环境等分布外条件下，成功率会明显下降。重新收集大量机器人数据并训练模型成本高，因此需要一种可在部署时利用额外计算、无需大规模重训即可提高鲁棒性的方案。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **离散动作选择与测试时采样缩放**：从同一个预训练视觉-语言-动作策略反复采样多个候选动作，再由外部验证器选出最优候选；部分方法通过改写语言指令增加候选之间的差异。
- **可微分测试时引导**：利用视觉-语言模型给出的评分，或利用世界模型预测未来结果并计算可微指标，再通过梯度或连续引导信号调整动作生成，使候选动作能够偏离原策略的高概率区域。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 离散选择及现有采样缩放产生的候选最终仍来自同一基础策略，样本容易集中于相似行为并继承相关偏差和共同失败模式；即使改写指令，也未必能探索到示范数据主导模式之外的高价值动作。
- 可微分引导依赖预训练视觉-语言模型对物理交互的理解或世界模型的预测精度，而这些信号可能缺乏可靠的物理落地能力；同时，各类现有方法通常在每个时间步采用固定干预，无法避免在基础策略本已正确时引入不必要扰动。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作尚未同时解决两个彼此关联的问题：一是如何利用基础模型之外的学习信号产生可绕开主导失败模式、但仍保留可靠行为先验的动作候选；二是如何依据当前状态下基础策略的成功可能性决定是否进行这种引导。尤其缺少把成功状态与失败状态分开研究的测试时缩放规律，因此无法为干预时机提供有根据的决策规则。

</div>
<div markdown="1"><span>核心问题</span>

在困难或分布外场景中，应当如何把预训练视觉-语言-动作模型引向更具多样性的候选动作，以及应当在何时启用这种引导，才能提升失败状态下的恢复能力而不破坏已经准确的动作？

</div>
<div markdown="1"><span>作者直觉</span>

基础视觉-语言-动作模型像一个从大量示范中学会常规做法的执行者，离线强化学习则能依据回报寻找示范主流之外但价值更高的替代动作；组合两者可兼顾动作可靠性与探索多样性。不过，多样性并非始终有益：当默认动作可能失败时，替代路线有机会避开共同失败模式；当默认动作已接近正确时，额外引导反而可能把动作推离正确解。因此，先预测是否会失败，再只在必要时组合强化学习引导，是该研究的核心切入点。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

RL$^2$是一个部署阶段的自适应动作引导框架，核心回答两个问题：如何让冻结的视觉-语言-动作模型（VLA）产生不同于其主导模仿模式、但仍有较高价值的动作，以及何时值得进行这种干预。离线阶段，作者从冻结VLA的动作专家中提取潜表示$e_t$，用带有这些潜表示的数据训练一个基于流匹配的强化学习策略$\pi_{\mathrm{RL}}(a_{t:t+H}\mid e_t)$；训练采用Q-learning with Adjoint Matching（QAM），以避免价值函数梯度穿过多步流生成过程时产生数值不稳定。在线阶段，系统同时利用$e_t$预测基础VLA是否可能失败；只有检测到失败时，才把RL策略提供的速度场$V_{\mathrm{RL}}$与VLA原有速度场$V_{\mathrm{VLA}}$组合起来，生成多个动作候选，否则直接保留基础VLA分布。最后由外部验证器为候选动作评分并选择执行动作。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造潜表示增强的离线数据

逐条将数据集观测和指令送入冻结VLA，从其动作专家提取嵌入$e_i$，形成增强数据集$\mathcal{D}=\{o_i,a_i,\ell_i,e_i\}_{i=1}^{N}$。这些潜表示压缩了与当前场景、指令和动作决策有关的内部信息。

<div class="method-step__io" markdown="1">

**输入**：BridgeV2或DROID中的观测$o_i$、动作$a_i$与语言指令$\ell_i$，以及一个冻结的预训练VLA。<br>
**输出**：供离线RL训练使用的潜表示增强数据集$\mathcal{D}$。

</div>

**直观理解**：不是让小型RL策略重新理解原始图像，而是把大模型已经提炼好的“决策摘要”交给它，从而降低训练难度并保留VLA的语义和控制知识。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 训练RL流匹配引导策略

训练条件策略$\pi_{\mathrm{RL}}(a_{t:t+H}\mid e_t)$；QAM先从终端动作$a_1$沿反向ODE计算伴随状态$\tilde{g}_t$，再令可学习速度场$f_\theta$通过逐时刻匹配损失跟随该价值引导。这样无需把$Q$的梯度直接反传穿过完整的多步流匹配采样器。

<div class="method-step__io" markdown="1">

**输入**：增强数据集$\mathcal{D}$、固定行为先验$f_\beta$、价值函数$Q(s,a)$和逆温度$\tau$。<br>
**输出**：能够依据VLA潜表示产生高价值、且不同于行为数据主导模式的RL速度场$V_{\mathrm{RL}}$。

</div>

**直观理解**：价值函数指出“哪些动作更好”，伴随状态把这一信号拆成每个生成步骤可学习的方向；RL策略因此学会在不完全抛弃示范经验的前提下探索替代动作。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提取在线状态并判断是否干预

将$e_t$并行送入RL引导策略和外部失败检测模块；失败检测模块根据潜表示判断基础VLA当前动作是否可能失败，并输出是否启用组合引导的触发信号。论文实验主要采用SAFE，并通过Conformal Prediction（CP，保形预测）阈值控制触发。

<div class="method-step__io" markdown="1">

**输入**：当前观测、语言指令，以及冻结VLA动作专家在当前时刻产生的潜表示$e_t$。<br>
**输出**：RL引导信息以及一个失败或成功状态的干预决策。

</div>

**直观理解**：系统先判断基础策略是否真的需要帮助：可能失败时增加动作多样性，已经可靠时则避免RL引导破坏原本正确的动作。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自适应组合动作生成

对流匹配VLA，若预测失败，则在每个流匹配步骤组合$V_{\mathrm{VLA}}$与$V_{\mathrm{RL}}$以产生多个动作块候选；若未预测失败，则从基础VLA动作分布生成候选。对于OpenVLA等自回归VLA，作者改用高斯扰动实现可组合的RL引导，但所给章节未给出组合系数的完整公式。

<div class="method-step__io" markdown="1">

**输入**：基础VLA速度场$V_{\mathrm{VLA}}$、RL速度场$V_{\mathrm{RL}}$和失败检测结果。<br>
**输出**：一组根据当前风险决定是否经过RL引导的候选动作。

</div>

**直观理解**：VLA提供熟练操作的基本方向，RL在失败风险较高时提供额外修正方向；这类似只在导航即将走错时启用绕行建议。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### QAM反向伴随状态方程

$$
\tilde{g}_{1}=-\tau\nabla_{a_{1}}Q(s,a_{1}),\qquad d\tilde{g}_{t}=-\nabla_{a_{t}}\left[2f_{\beta}(s,a_{t},t)-a_{t}/t\right]\tilde{g}_{t}\,dt
$$

**符号说明**

- $\tilde{g}_{t}$：流时间$t$上的伴随状态，即传递给策略速度场的时变价值引导信号。
- $a_t$：流匹配生成过程在时间$t$的中间动作变量；$a_1$是终端生成动作。
- $Q(s,a_1)$：评论家对状态$s$下终端动作$a_1$的长期回报估计。
- $\tau$：逆温度参数，控制价值引导相对于行为先验的强度。
- $f_\beta(s,a_t,t)$：固定行为先验在状态$s$、动作变量$a_t$和流时间$t$处的速度场。
- $\nabla_{a_t}$：对动作变量$a_t$求梯度。
- $t$：从噪声到动作的连续流时间。

<div class="equation-explanation" markdown="1">

**直观理解**：终端条件先用$Q$关于最终动作的梯度指出提高价值的方向，再沿行为先验定义的动力学反向传播该信息，得到每个流生成时刻的指导信号。它解决了价值梯度直接穿过多步流采样过程容易数值不稳定的问题。<br>
**原文位置**：第V-A节，公式(3)

</div>

</div>

<div class="equation-block" markdown="1">

#### Adjoint Matching策略损失

$$
L_{AM}(\theta)=\mathbb{E}_{s,\{a_t\}}\int_{0}^{1}\left\|\frac{2\left(f_{\theta}(s,a_t,t)-f_{\beta}(s,a_t,t)\right)}{\sigma_t}+\sigma_t\tilde{g}_t\right\|_{2}^{2}\,dt,\qquad \sigma_t=\sqrt{\frac{2(1-t)}{t}}
$$

**符号说明**

- $L_{AM}(\theta)$：用于优化策略参数$\theta$的伴随匹配损失。
- $f_\theta(s,a_t,t)$：待训练RL策略在状态$s$、中间动作$a_t$与流时间$t$处的速度场。
- $f_\beta(s,a_t,t)$：固定的行为先验速度场。
- $\tilde{g}_t$：由公式(3)反向计算的价值引导信号。
- $\sigma_t$：固定噪声调度，随流时间$t$调整速度偏移与价值引导的尺度。
- $\mathbb{E}_{s,\{a_t\}}$：对训练状态及其流轨迹中的中间动作取期望。
- $\|\cdot\|_2^2$：平方欧氏范数，用于惩罚速度修正与目标价值引导之间的不匹配。

<div class="equation-explanation" markdown="1">

**直观理解**：损失要求RL速度场相对行为先验的偏移，与伴随状态给出的价值改进方向相互抵消；当积分区间内该残差较小时，策略既靠近离线数据的行为分布，又偏向$Q$值更高的动作。作者指出这一一阶、逐时刻的匹配路径比直接通过完整流过程优化评论家目标更稳定。<br>
**原文位置**：第V-A节，公式(4)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练的直接目标是最小化$L_{AM}(\theta)$。QAM先固定行为先验$f_\beta$，利用评论家$Q(s,a)$和逆温度$\tau$构造伴随状态$\tilde{g}_t$，再更新$f_\theta$以匹配这一逐时刻引导；其理论目标是得到行为正则化分布$\pi(a\mid s)\propto\pi_\beta(a\mid s)\exp(\tau Q(s,a))$。其中$\pi_\beta$保留离线示范的动作先验，指数项提高高价值动作的概率，$\tau$决定策略偏离行为先验以追求高价值动作的程度。该RL目标训练的是独立轻量引导策略，基础VLA保持冻结；失败检测器和验证器分别负责决定何时使用该策略以及从其候选中选择什么，并不属于公式(4)的策略优化变量。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 潜表示条件的RL流匹配策略**

策略$\pi_{\mathrm{RL}}(a_{t:t+H}\mid e_t)$以冻结VLA动作专家的潜表示$e_t$为条件，并利用QAM学习相对于固定行为先验$f_\beta$的价值导向速度修正。其目标分布满足行为正则化形式$\pi(a\mid s)\propto\pi_\beta(a\mid s)\exp(\tau Q(s,a))$，其中$\tau$控制价值偏好相对于行为先验的强度。

> 直观理解：该模块借用VLA已经学到的场景理解，再利用RL寻找示范数据主导动作之外的高价值方案；行为先验则约束它不要为了追求价值而产生完全脱离数据分布的动作。

**2. 自适应失败检测与触发模块**

失败检测器读取动作专家潜表示$e_t$，判断当前基础VLA是否可能失败；实验中SAFE结合CP置信带产生触发决策，并通过显著性水平$\alpha$调节触发范围。该模块与动作候选生成并行运行，只控制是否组合速度场，不改动冻结VLA。

> 直观理解：动作多样性并非始终有益：基础动作已经准确时，额外引导可能把它推离正确解。因此该模块把计算和干预集中在真正可能失败的时刻。

**3. 组合生成与验证器**

检测到失败时，系统在流匹配采样的各步骤组合$V_{\mathrm{VLA}}$和$V_{\mathrm{RL}}$；否则使用原始VLA分布。生成的候选最终由CoVer等验证器评分和筛选，使VLA行为先验、RL引入的分布扩展以及测试时多样本选择形成闭环。

> 直观理解：组合生成负责提出既像熟练示范、又包含恢复可能性的候选；验证器负责从中做最终决策，避免把“更不同”误当成“必然更好”。

**训练与推理**

训练阶段包括三部分。第一，冻结预训练VLA并遍历BridgeV2、DROID等离线数据，从动作专家提取每个样本的潜表示$e_i$。第二，以$e_i$为条件训练流匹配RL策略：评论家提供$Q(s,a)$，QAM通过公式(3)生成$\tilde{g}_t$，并用公式(4)更新$f_\theta$；对OpenVLA等非流匹配设置，框架可接入以CQL训练、且可与VLA动作组合的策略。第三，为具体部署环境准备失败检测器及其CP触发阈值；验证器作为候选评分器使用。

推理时，当前观测和指令先进入冻结VLA，得到基础动作生成信息及动作专家潜表示$e_t$。SAFE等模块根据$e_t$检测风险：若预测成功，直接保持基础VLA候选；若预测失败，RL策略依据$e_t$产生$V_{\mathrm{RL}}$，并在每个流匹配步骤与$V_{\mathrm{VLA}}$组合以扩展候选动作分布。系统对多个候选重复采样，由CoVer等验证器选择最佳动作执行，再根据下一时刻的新观测重新判断。因而该方法的自适应性发生在每个决策时刻，而不是为整条轨迹预先固定“始终引导”或“从不引导”。

**复现信息**

基础VLA在训练和部署中均保持冻结；离线RL策略以动作专家潜表示而非原始图像为主要条件，这是理解训练可行性和消融结果的关键。作者报告RL策略使用两张NVIDIA L40s训练约$500\mathrm{k}$至$1\mathrm{M}$步，但所给章节没有完整列出网络宽度、优化器、学习率、速度场组合系数或潜表示聚合细节，因此复现时需核对附录第VI节及正式代码。流匹配VLA通过速度场组合实现引导，自回归OpenVLA则使用高斯扰动实现兼容的组合引导；两种实现不应视为完全相同的采样器。部署端还需为目标环境校准失败检测：真实机器人实验中，仿真轨迹训练的SAFE不能直接良好泛化，作者重新收集真实环境滚动数据，这说明失败触发器存在环境依赖，而RL策略和基础VLA权重可继续沿用。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- SIMPLER（Original）：模拟大规模示范数据采集场景的机器人操作基准。实验选取 BridgeV2 中使用 WidowX 机器人的四个标准域内任务及原始提示词，以 OpenVLA 为基础策略；该设置主要检验方法在 VLA 已见任务和标准语言指令下是否仍能带来增益。RL 引导策略为经 CQL 训练、来自 V-GPS 的策略，验证器为 RoboMonkey。原文未明确报告训练集、验证集与测试集划分。
- SIMPLER（OOD）：一部分实验保留四个域内任务，但将基础指令替换为具有挑战性的 red-teaming 分布外提示；另一部分加入 Interleave-VLA 提供的四个分布外环境，改变背景、目标物体并加入干扰物。基础模型为 $\pi_0$，RL 流引导策略为 QAM，候选动作验证器为 CoVer。前者测试语言鲁棒性，后者进一步测试视觉环境和物体配置变化下的泛化；原文未明确报告数据划分。
- PolaRiS（OOD）：基于高保真 Gaussian-splat 场景和 Franka Emika Panda 机器人的模拟基准。实验使用三个由 DROID 改编的任务，并配置分布外 red-teaming 指令及多个干扰物；任务包括 Move Latte Cup、Tape into Container 和 Pan Cleaning。基础模型为 $\pi_{0.5}$，QAM 负责 RL 流引导，CoVer 负责候选动作选择。该设置同时检验最终成功和部分任务进展；原文未明确报告数据划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**成功率 $S$**

在重复执行中完整完成机器人操作任务的比例，直接衡量端到端任务可靠性。 （越高越好，因为更高比例表示策略更经常达到任务终止目标。）

</div>
<div class="metric-item" markdown="1">

**进展率 $P$**

衡量任务即使未完全成功时完成了多少阶段或取得了多少进展；本文在 PolaRiS 中同时报告该指标，以区分完全失败与部分完成。 （越高越好，因为它表示策略更接近完整完成任务；但它不能替代最终成功率。原文节选未给出其具体计算公式。）

</div>
<div class="metric-item" markdown="1">

**跨任务平均表现及随机种子标准差**

对多个任务的成功率或进展率取平均，并以三个随机种子的标准差表示结果波动。 （平均值越高越好；在平均值相近时，标准差越小通常表示结果更稳定，但本文没有进行统计显著性检验。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### OpenVLA 在 SIMPLER 四个域内任务及原始提示词上的评估

<div class="result-value" markdown="1">

作者报告，自适应 $RL^2$ 相对最强 Repeated 基线的跨任务平均成功率提高 7.5 个百分点，单任务最大提高 19.4 个百分点。

</div>

这说明即使任务和指令处于基础 VLA 熟悉的分布内，RL 组合式引导仍可能提供重复采样没有覆盖到的有效动作，而自适应介入可将这些动作纳入候选集合。该比较支持方法对标准任务有效，但节选未给出 Fig. 6 的逐任务原始数值，因此无法核验增益来自哪些任务，也不能据此证明提升具有统计显著性。

<div class="result-source" markdown="1">

来源：Section VI-B.1，Fig. 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For OpenVLA, adaptive RL2 achieves an average performance gain of +7.5% (task-wise +19.4%) over the strongest Repeated baseline across SIMPLER in-domain tasks.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### $\pi_0$ 在四个新增 SIMPLER 分布外环境及分布外语言提示上的评估

<div class="result-value" markdown="1">

作者报告，自适应 $RL^2$ 相对最强 Rephrase 基线平均提高 8.5 个百分点；在 Spoon on Towel - Google 任务上最大提高 14.6 个百分点。

</div>

新增环境同时改变背景、目标物体并可能加入干扰物，因此该结果比单纯改写语言更直接地测试视觉环境泛化。平均增益表明，RL 引导产生的候选动作可能补充由不同提示词生成但仍高度相关的 VLA 动作。它仍不能证明方法对所有未见环境普遍有效，因为这里只覆盖四个新增任务，且没有报告显著性检验。

<div class="result-source" markdown="1">

来源：Section VI-B.2，Fig. 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We benchmark using π0 across these SIMPLER tasks under OOD language prompts, and observe an average performance gain of +8.5% over the strongest Rephrase baseline, with up to +14.6% gain for the highest performing task (Spoon on Towel - Google).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### $\pi_{0.5}$ 在 PolaRiS 三个任务及分布外语言提示上的评估

<div class="result-value" markdown="1">

自适应 $RL^2$ 的平均成功率为 $42.7\%\pm2.3\%$，高于 Rephrase 的 $31.8\%\pm3.4\%$，即提高 10.9 个百分点；平均进展率由 $55.2\%\pm1.4\%$ 提高到 $63.0\%\pm3.4\%$，即提高 7.8 个百分点。Move Latte Cup 的成功率由 48.7% 提高到 66.0%，增幅为 17.3 个百分点。

</div>

成功率与进展率同时上升，说明改进并非只让失败轨迹略微靠近目标，而是更经常完成整个任务。自适应版本也高于 Compose-Always 的平均成功率 33.8%，与“成功可能性较高时不应无条件扰动基础动作”的设计动机一致。不过该表只能建立组件组合与性能之间的实验关联，不能单独证明 SAFE 判断或动作多样性是增益的唯一原因。

<div class="result-source" markdown="1">

来源：Table I：PolaRiS OOD Prompt Evaluation

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Average | S(%) | 14.3 (± 2.0) | 31.8 (± 3.4) | 33.8 (± 1.7) | 42.7 (± 2.3); P(%) | 40.0 (± 0.7) | 55.2 (± 1.4) | 55.8 (± 1.2) | 63.0 (± 3.4).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给节选在 Table II 的表头后截断，未提供 latent 表征、RL 训练等消融的完整配置和数值，因此无法可靠填写带数值证据的消融结果；论文关于这些组件重要性的主张仍需对照完整表格核验。
- 实验主要基于 SIMPLER 与 PolaRiS 模拟环境，任务数分别有限；节选虽提到真实世界实验，但没有提供其设置和结果。与此同时，实验未报告统计显著性检验，且未明确 50 次运行如何分配到三个随机种子，因此均值差异的统计可靠性仍需进一步核查。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Vanilla：直接使用未加测试时引导的 OpenVLA、$\pi_0$ 或 $\pi_{0.5}$。它给出基础策略本身的能力下界，用于判断增益是否确实来自额外采样与组合式引导。
- Repeated/Rephrase：Repeated 从同一 VLA 重复采样动作；Rephrase 使用 VLM 生成的多种指令改写来采样动作。该基线代表已有测试时扩展方法，可检验仅增加候选数量或语言多样性是否足以解决相关失败模式。
- $RL^2$（Compose-Always）：对多个 VLA 动作始终应用 RL 组合式引导。它与自适应版本共享引导机制，但不判断当前是否可能失败，因此用于检验“仅在失败时介入”是否必要。
- $RL^2$（Compose-Adaptive）：SAFE 预测基础 VLA 将失败时启用组合式引导，否则退回 Repeated 或 Rephrase。它是完整方法，比较重点是选择性干预能否既利用失败状态下的动作多样性，又避免扰动本来正确的动作。

**实验想回答的问题**

- 组合式引导是否能在无需重新训练基础视觉—语言—动作模型（VLA）的情况下，提高标准任务、分布外语言指令以及分布外环境中的任务成功率？
- 自适应策略是否能根据基础 VLA 的预测失败状态选择性启用强化学习引导，并比始终引导或仅增加 VLA 动作采样获得更好的测试时扩展效果？

**实验实现**

所有实验各运行 50 次，并报告三个随机种子的均值与标准差。OpenVLA 设置遵循既有方法：先对 9 个来自 VLA 或组合策略的动作样本拟合高斯分布，再重采样 32 个动作；$\pi_0$ 与 $\pi_{0.5}$ 设置使用 8 个指令改写，每个改写生成 5 个动作样本。候选动作最终由 RoboMonkey 或 CoVer 验证器选择；自适应版本额外使用 SAFE 判断基础策略当前是否可能失败。原文节选没有说明 50 次运行与三个种子之间的具体分配，也未报告置信区间或显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- Spoon on Towel 的动作可视化显示：使用指令改写时，$\pi_0$ 的动作样本大多朝错误方向或错误干扰物集中，执行中会在勺子上方振荡；RL 引导后的候选更分散，其中出现朝向正确目标的高质量动作，并由 CoVer 选中，最终形成更准确、果断的抓取。该案例直观解释了组合式引导如何打破相关失败模式，但属于单个轨迹的定性证据，不能替代总体统计结果。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过轻量级离线强化学习策略对 VLA 潜变量进行自适应测试时引导，以提升机器人任务成功率。; rule check: matched taxonomy keywords; top rule score=6.0
- 全文指纹：`70340e267455516ca85f7211f2bdbd3eb31996029e102df9aef1c2f7d2bcdda4`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
