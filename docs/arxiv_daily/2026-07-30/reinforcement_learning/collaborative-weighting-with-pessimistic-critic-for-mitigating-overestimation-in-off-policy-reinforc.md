---
title: "[论文解读] Collaborative Weighting with Pessimistic Critic for Mitigating Overestimation in Off-Policy Reinforcement Learning"
description: "[arXiv 2607.26509][强化学习] 本文针对离策略连续控制中价值高估与训练不稳定问题，提出CWAC，通过联合校准TD误差与预测不确定性，并以随机悲观价值替代直接最大化期望Q值，减少不可靠样本更新和贪心策略改进造成的误差放大。"
arxiv_id: "2607.26509"
announcement_date: "2026-07-30"
primary_category: "reinforcement_learning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.617083+00:00"
source_sha256: "abfde6cbcf203876f732d98c6deb68875e70c406acedbed1773e52334fbce96e"
tags:
  - "强化学习"
  - "离策略强化学习"
  - "连续控制"
  - "过估计偏差"
  - "分布式评论家"
  - "协同加权"
  - "随机悲观价值估计"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">强化学习 · arXiv 2607.26509</p>

# Collaborative Weighting with Pessimistic Critic for Mitigating Overestimation in Off-Policy Reinforcement Learning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Gong Gao, Xiao Lai, Ziqi Xie, Guojie Chen, Xianhui Liu, Weidong Zhao</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26509v1) · [PDF 下载](https://arxiv.org/pdf/2607.26509v1) · **关键词** 离策略强化学习, 连续控制, 过估计偏差, 分布式评论家, 协同加权, 随机悲观价值估计<br>
**代码**: [https://anonymous.4open.science/r/CWAC-348E](https://anonymous.4open.science/r/CWAC-348E)  

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

本文针对离策略连续控制中价值高估与训练不稳定问题，提出CWAC，通过联合校准TD误差与预测不确定性，并以随机悲观价值替代直接最大化期望Q值，减少不可靠样本更新和贪心策略改进造成的误差放大。

**不用术语来说**：离策略强化学习会反复利用历史交互数据，并根据当前模型预测哪些动作更好；但这些预测在训练早期往往不准确。若算法总是选择预测值最高的动作，就容易把偶然偏高的估计误当成真正优势，并在后续更新中不断强化这一错误。同时，预测误差较大的样本未必更有学习价值，它也可能只是数据不足或自举目标噪声造成的异常样本，因此盲目强调此类样本会使训练更加不稳定。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出协同加权机制，将TD误差与由回报分布得到的预测不确定性联合用于调整样本影响：不确定性用于抑制不可靠的高误差信号，TD误差反过来帮助校准不确定性相关的权重。
- 作者提出基于分布式评论家的随机悲观价值估计，从预测的回报分布中采样来执行策略改进，而非直接最大化期望Q值，以降低贪心选择对正向估计噪声的偏好，同时保留一定探索空间。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究连续控制中的深度离策略强化学习。智能体把历史交互转移存入经验回放缓冲区，并利用这些可重复采样的数据训练动作价值函数，再由价值估计指导策略改进；这种做法样本效率较高，但神经网络近似、时序差分自举目标以及策略对高估动作的偏好会形成反馈回路：带正向估计噪声的动作更容易被选中，其误差又进入后续目标，最终造成持续的价值过估计和训练不稳定。本文所需的直接背景是最大熵演员—评论家学习与加权Q学习：前者交替进行策略评估和策略改进，后者通过样本权重控制不同转移对评论家更新的影响。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**离策略演员—评论家（off-policy actor-critic）**

演员表示策略，即在状态下如何选择动作；评论家用Q函数估计某个状态—动作对的长期折扣回报。离策略表示训练数据可以来自旧策略或其他行为策略，因此经验回放中的历史数据能够被反复使用。

</div>
<div class="concept-item" markdown="1">

**时序差分学习与自举（TD learning and bootstrapping）**

TD学习用即时奖励加上下一个状态的当前价值估计构造监督目标，而不必等待完整轨迹结束。由于目标本身依赖尚不准确且持续变化的网络估计，近似误差会递归传播。

</div>
<div class="concept-item" markdown="1">

**过估计偏差与预测不确定性**

当策略倾向选择当前估值最高的动作时，带有正向噪声的动作会被系统性偏好，从而使Q值高于真实回报。预测不确定性描述价值预测的可信程度；数据覆盖不足或自举误差较大时，不确定性通常更高。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

环境被建模为马尔可夫决策过程，状态为输入，策略输出连续动作；环境随后给出奖励和下一状态，所得转移被存入经验回放缓冲区。评论家从缓冲区采样状态—动作数据，以软Bellman目标执行TD更新；演员则依据评论家的价值估计改进策略。研究假设价值函数由神经网络近似，训练采用离策略数据和自举目标，因此估计噪声、数据覆盖不足及目标非平稳性不可避免。本文聚焦的问题是：如何利用价值预测的不确定性调节不同样本的学习贡献，并避免策略改进直接偏好被偶然高估的动作，从而在不过度牺牲在线探索的前提下缓解过估计、提高样本效率与训练稳定性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{M}=\langle\mathcal{S},\mathcal{A},\mathcal{P},\mathcal{R},\gamma\rangle$**

马尔可夫决策过程；其中\(\mathcal{S}\)是状态空间，\(\mathcal{A}\)是动作空间，\(\mathcal{P}\)是状态转移规律，\(\mathcal{R}\)是奖励函数，\(\gamma\)是折扣因子。

</div>
<div class="notation-item" markdown="1">

**$\pi_{\phi}(a\mid s)$**

参数为\(\phi\)的策略；在状态\(s\)下给动作\(a\)分配概率或概率密度，文中预备知识部分采用高斯策略。

</div>
<div class="notation-item" markdown="1">

**$Q_{\theta}(s,a)$**

参数为\(\theta\)的评论家网络，对状态\(s\)下执行动作\(a\)后的长期折扣回报进行估计。

</div>
<div class="notation-item" markdown="1">

**$\omega(s,a)$**

加权Q学习中的状态—动作相关权重，用于调节单个转移的Bellman残差对评论家参数更新的贡献。

</div>

</div>

**直接相关的工作**

- **悲观价值估计**: 这类方法通过惩罚高不确定性动作来抑制价值过估计，是本文处理策略改进偏差的直接参照；原文同时指出，在线学习中过强的悲观性可能阻碍探索并导致次优表现。
- **自适应样本加权（包括优先经验回放与不确定性感知加权学习）**: 这类方法依据TD误差或不确定性改变样本对价值更新的贡献。本文指出，大TD误差可能与高不确定性纠缠，若直接强调这些转移，可能放大噪声交互并引入有偏更新。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

SAC、TD3和DDPG等离策略演员—评论家算法依赖神经网络Q函数和TD自举目标来学习长期回报。近似目标中的噪声会使优化信号持续变化，而策略改进又倾向于选择当前估值最高的动作；两者结合后，早期的正向估计误差会被递归传播并自我强化，形成系统性价值高估，最终损害连续控制中的样本效率、策略质量和训练稳定性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **悲观价值估计**：对高不确定性动作的价值施加惩罚，或采用更保守的价值作为策略优化依据，从而降低被高估动作进入自举目标和策略更新的概率。
- **基于TD误差的自适应样本加权或优先采样**：依据转移样本的TD误差调整训练权重，通常让TD误差较大的样本更频繁或更强地参与更新，以集中修正当前价值函数预测不一致之处。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 悲观价值估计虽然能够抑制高估，但在线学习中过强的保守性会压低潜在优质动作的价值，阻碍有效探索并可能导致次优策略；因此，固定或过度的悲观程度难以兼顾稳健性与探索。
- 大TD误差并不必然表示样本信息量高，它可能源于数据覆盖不足、自举误差或随机交互噪声。只按TD误差提高样本权重，会把高不确定性噪声当作重要学习信号，进而产生有偏更新并放大价值误差。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法通常分别处理价值高估或样本重要性，尚缺少一种轻量、可嵌入主流离策略算法的统一机制：既显式估计回报预测的不确定性，又让不确定性与TD误差相互校准样本权重，并在策略改进阶段自适应地引入适度悲观，以同时避免噪声样本主导学习和贪心最大化放大正向误差。

</div>
<div markdown="1"><span>核心问题</span>

能否利用分布式价值函数提供的回报不确定性，联合调节评论家更新中的TD误差信号，并通过从回报分布中随机取得偏悲观的价值来指导策略改进，从而在不过度牺牲探索的前提下减少离策略演员—评论家算法的价值高估、误差传播和训练波动？

</div>
<div markdown="1"><span>作者直觉</span>

如果两个样本具有同样大的TD误差，其中一个预测分布集中、另一个预测分布很宽，那么前者更可能反映可修正的系统性偏差，后者则更可能是模型尚无把握的噪声；因此应用不确定性降低后者的更新影响。策略更新时也不直接相信回报分布的均值或最高估计，而是从该分布中随机采样一个偏保守的价值：这相当于避免每次都追逐最乐观的偶然误差，同时随机性又使算法不像固定下界那样始终极端保守。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CWAC是在连续控制的离策略 actor-critic 框架上加入“分布式评论家、协同加权、随机悲观策略改进”的统一方法。评论家不只输出动作价值均值 Q，还输出回报分布的标准差 σ，后者被视为预测不确定性。训练时，算法从经验回放池均匀抽取转移，以目标评论家的悲观价值构造自举目标：先从高斯分布采样非负扰动幅度，再按不确定性大小从 Q 中扣除该幅度。评论家使用 Huber 损失拟合该目标，同时用不确定性权重 ω 降低高不确定样本对价值拟合的影响，并用 TD 误差权重 ξ 调节对不确定性的直接惩罚。actor 则最大化悲观价值与熵奖励之和，从而避免策略专门追逐偶然被高估的动作。

直观地说，CWAC给每个价值预测同时附上一条“误差带”：误差带宽时，不急着相信该样本的 Q 值；但也不把误差带强行压到很窄，以免模型在尚未学好的区域假装自信。随机悲观扣减进一步避免固定强度的保守惩罚：它通常压低不可靠动作的价值，却保留一定随机变化，以在抑制过估计和维持探索之间取得折中。该机制不改变经验回放的采样分布，可作为 SAC、TD3 或 DDPG 一类离策略算法的附加价值学习机制；所给算法流程具体采用双评论家、目标网络及带熵项的随机策略形式。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 环境交互与均匀经验回放

从 π_φ(·|s) 采样动作 a，与环境交互得到奖励 r 和下一状态 s′，并将转移 (s,a,r,s′) 存入 B；更新时从 B 抽取小批量，而非按 TD 误差进行优先采样。

<div class="method-step__io" markdown="1">

**输入**：当前状态 s、参数为 φ 的随机策略 π_φ，以及经验回放池 B。<br>
**输出**：用于离策略更新的小批量转移，以及持续扩充的经验回放池 B。

</div>

**直观理解**：经验池相当于打乱后的历史练习册；CWAC不让“看起来错误最大”的题被反复抽中，而是在取出题目后再判断其答案是否可靠。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 分布式价值估计与随机悲观采样

采样 ε∼N(0,μI)，计算悲观价值 Z_θ(s,a)=Q_θ(s,a)−|ε|σ_θ(s,a)；对下一状态从当前策略采样 a′，再取两个目标评论家悲观值的较小者并加入奖励、折扣和熵项，形成自举目标 y。

<div class="method-step__io" markdown="1">

**输入**：批量中的状态—动作对、两个评论家及其目标网络；每个评论家给出价值均值 Q_θ(s,a) 和标准差 σ_θ(s,a)。<br>
**输出**：当前或候选动作的悲观价值 Z，以及供评论家学习的目标 y。

</div>

**直观理解**：如果预测的误差带更宽，就从名义分数中扣得更多；双评论家的最小值又增加一道保险，降低偶然高估被写入后续目标并递归传播的概率。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 协同加权评论家更新

按 ω=(E[σ_θ]/(σ_θ+c))^{β_ω} 缩放 Huber 价值损失，并按 ξ=(E[|δ|]/(|δ|+c))^{β_ξ} 缩放不确定性惩罚 ξσ；通过梯度下降联合优化评论家输出的均值与不确定性。

<div class="method-step__io" markdown="1">

**输入**：预测均值 Q_θ、标准差 σ_θ、目标 y，以及 TD 误差 δ=Q_θ−y。<br>
**输出**：更新后的分布式评论家，其价值面较少受高不确定目标支配，同时保留与学习误差相适应的不确定性。

</div>

**直观理解**：ω回答“这条价值标签值得信多少”：越不确定，价值拟合力度越小；ξ回答“现在是否该把误差带收紧”：TD 误差很大时先少收紧，防止模型在尚未学会时过早变得自信。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 悲观策略改进与目标网络更新

actor 通过梯度上升最大化 E[Z_θ(s,a)−αlogπ_φ(a|s)]，即用悲观价值而非原始 Q 指导动作选择；随后以 θ′_i←τθ_i+(1−τ)θ′_i 对两个目标评论家进行软更新。

<div class="method-step__io" markdown="1">

**输入**：更新后的评论家、回放状态 s、策略生成的动作 a，以及熵系数 α。<br>
**输出**：不易追逐高估动作的策略 π_φ，以及缓慢跟随在线评论家的目标网络。

</div>

**直观理解**：策略不仅看动作的预测收益，还考虑预测是否可靠并保留熵探索；目标网络缓慢移动，使下一轮学习所用的“参考答案”不会剧烈变化。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 随机悲观价值采样

$$
\mathcal{Z}_{\theta}(s,a)=Q_{\theta}(s,a)-b\!\left(\sigma_{\theta}(s,a)\right),\qquad b(\sigma)=|\epsilon|\sigma,\qquad \epsilon\sim\mathcal{N}(0,\mu I)
$$

**符号说明**

- $\mathcal{Z}_{\theta}(s,a)$：状态 s 下执行动作 a 的随机悲观价值估计。
- $Q_{\theta}(s,a)$：参数为 θ 的分布式评论家所预测的回报均值。
- $\sigma_{\theta}(s,a)$：评论家所预测回报分布的标准差，用作该状态—动作对的预测不确定性。
- $b(\sigma)$：依赖不确定性的非负随机扣减量。
- $\epsilon$：从零均值高斯分布采样的随机扰动；取绝对值后保证扣减方向为悲观方向。
- $\mu$：高斯扰动协方差的尺度，控制随机悲观扰动的总体强度。
- $I$：单位矩阵。
- $s,a$：MDP中的状态与动作。
- $\theta$：评论家网络参数。

<div class="equation-explanation" markdown="1">

**直观理解**：该式从名义 Q 值中扣除“随机系数×预测标准差”。不确定性越大，平均扣减越大，因此策略和自举目标较少采用证据不足却偶然很高的价值；随机系数则避免所有状态都受到固定强度的保守惩罚。<br>
**原文位置**：第4.1节，定义1，公式(4)

</div>

</div>

<div class="equation-block" markdown="1">

#### 协同加权评论家目标、悲观自举目标与双权重

$$
\begin{aligned}\mathcal{L}_{\mathcal{Z}}^{\omega,\xi}(\theta)&=\mathbb{E}_{(s,a)\sim\mathcal{B},\,s'\sim\rho_{\pi},\,a'\sim\pi_{\phi}}\!\left[\omega(s,a)\,\mathrm{Huber}\!\left(Q_{\theta}(s,a)-y\right)+\xi(s,a)\,\sigma_{\theta}(s,a)\right],\\ y&=r+\gamma\left[\min_{i=1,2}\mathcal{Z}_{\theta_i'}(s',a')-\alpha\log\pi_{\phi}(a'\mid s')\right],\qquad a'\sim\pi_{\phi}(\cdot\mid s'),\\ \delta(s,a)&=Q_{\theta}(s,a)-y,\\ \omega(s,a)&=\left(\frac{\mathbb{E}[\sigma_{\theta}(s,a)]}{\sigma_{\theta}(s,a)+c}\right)^{\beta_{\omega}},\qquad \xi(s,a)=\left(\frac{\mathbb{E}[|\delta(s,a)|]}{|\delta(s,a)|+c}\right)^{\beta_{\xi}}.\end{aligned}
$$

**符号说明**

- $\mathcal{L}_{\mathcal{Z}}^{\omega,\xi}(\theta)$：用于训练分布式评论家的协同加权损失。
- $\mathcal{B}$：存放历史转移的经验回放池。
- $\rho_{\pi}$：策略 π 诱导的状态分布。
- $\pi_{\phi}$：参数为 φ 的随机 actor 策略。
- $\mathrm{Huber}(\cdot)$：Huber 损失；小残差区域近似平方损失，大残差区域近似绝对值损失，以降低异常目标的影响。
- $y$：由即时奖励和下一状态悲观价值组成的自举学习目标。
- $r$：当前转移的即时奖励。
- $\gamma$：未来回报的折扣因子。
- $\mathcal{Z}_{\theta_i'}$：第 i 个目标评论家的随机悲观价值；$θ_i$′为其目标网络参数。
- $\min_{i=1,2}$：在两个目标评论家的悲观估计中取较小值，以进一步抑制正向估计误差。
- $\alpha$：最大熵强化学习中的熵系数。
- $-\alpha\log\pi_{\phi}(a'\mid s')$：目标中的熵奖励项，用于避免策略过早退化为确定性选择。
- $\delta(s,a)$：当前价值预测与自举目标之间的 TD 误差。
- $\omega(s,a)$：不确定性感知的价值损失权重；σ较大时该权重较小。
- $\xi(s,a)$：由 TD 误差控制的不确定性正则权重；|δ|较大时该权重较小。
- $\mathbb{E}[\sigma_{\theta}(s,a)]$：预测标准差的期望，用于给单个样本的不确定性提供相对参照尺度。
- $\mathbb{E}[|\delta(s,a)|]$：绝对 TD 误差的期望，用于给单个样本残差提供相对参照尺度。
- $\beta_{\omega},\beta_{\xi}$：分别控制不确定性权重和 TD 误差权重变化尖锐程度的指数。
- $c$：防止分母过小并提高数值稳定性的小常数。
- $s',a'$：下一状态及从当前策略在该状态采样的下一动作。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项负责把 Q 均值拟合到悲观自举目标，但 ω会降低高不确定样本的发言权；第二项倾向于缩小预测标准差，但 ξ在 TD 误差很大时会减弱这种压力，避免评论家尚未拟合好就出现不确定性坍缩。两条调节路径形成互补：一条阻止噪声目标推高价值，另一条阻止过强悲观和虚假自信压制潜在探索。<br>
**原文位置**：第4.2节，定义2，公式(5)、(6)、(7)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：评论家通过梯度下降最小化协同加权损失：Huber 项学习价值均值，ω根据预测标准差降低不可靠转移的影响；线性不确定性项 ξσ推动模型在证据充分时收紧回报分布，而 ξ根据绝对 TD 误差避免在大残差区域过早压低 σ。这里的关键不是简单偏爱大 TD 误差样本，而是区分“有用的 Bellman 学习信号”和“由有限覆盖、函数逼近或自举造成的噪声”。目标 y使用双目标评论家的最小悲观值，使过估计不易沿 Bellman 自举链条向前传播。

actor 通过梯度上升最大化 $J_π(φ)=E_{s∼B,a∼π_φ}[Z_θ(s,a)−αlogπ_φ(a|s)]$。因此，策略改进偏向悲观调整后仍然较优的动作，同时熵项维持随机探索；这与评论家端的悲观目标保持一致，避免 actor 利用原始 Q 中的正向误差。在线评论家更新后，目标评论家以软更新缓慢跟随，以降低目标非平稳性。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 分布式评论家与随机悲观价值**

评论家用 Q_θ(s,a) 表示回报分布的均值，用 σ_θ(s,a) 表示标准差，并以 |ε|σ_θ 作为随机、非负的不确定性扣减。随机扰动尺度由 μ 控制，因此悲观程度同时依赖局部预测不确定性和每次采样的扰动。

> 直观理解：普通评论家只报一个分数，无法区分“高价值且可靠”和“高价值但没把握”；该模块同时报告分数与可信程度，并用可信程度修正决策分数。

**2. TD 误差—不确定性协同加权**

ω随 σ 增大而减小，用于抑制高不确定样本的价值拟合梯度；ξ随 |δ| 增大而减小，用于减弱大残差区域中的 σ 收缩。两个权重由批量或采样分布上的 E[σ]、E[|δ|]作相对尺度归一化，β_ω、β_ξ控制权重变化的尖锐程度。

> 直观理解：只按大 TD 误差加权会把噪声误认成重要学习信号；CWAC让“误差大小”和“预测可信度”相互制约，既不追着噪声更新，也不在证据不足时强迫模型过度自信。

**3. 悲观目标与悲观 actor 更新**

评论家目标使用两个目标评论家悲观估计的最小值，actor 也直接优化悲观价值 Z，并在最大熵框架下保留 −αlogπ_φ(a|s) 项。因而悲观性同时进入策略评估和策略改进，而不是只在评论家损失中作局部正则化。

> 直观理解：若只修正评论家的训练，却仍让策略追逐原始 Q 的最大值，高估仍可能在动作选择时被放大；该模块让训练目标和实际选动作遵循同一套谨慎标准。

**训练与推理**

训练阶段首先随机初始化两个评论家 $Q_{θ_1}$、$Q_{θ_2}$和 actor π_φ，并复制得到两个目标评论家；智能体循环从策略采样动作、执行环境转移并写入经验池。每次更新从经验池抽取小批量，对下一状态采样 a′，由目标评论家的均值和标准差生成随机悲观值，取双评论家较小值构造 y；随后计算 δ、ω和 ξ，最小化协同加权 Huber—不确定性损失。完成评论家更新后，重新以悲观价值指导 actor 最大化带熵目标，最后用系数 τ对目标评论家进行软更新。随机悲观样本会进入评论家目标和 actor 更新，但经验池本身仍采用普通抽样。

推断或部署阶段以训练后的 π_φ根据当前状态产生动作并与环境交互；原文节选没有明确说明评估时采用随机动作、分布均值动作还是其他确定化规则。若部署仍需按论文目标评估候选动作，则可使用评论家的悲观价值而非原始 Q，但算法主体已经把这种偏好蒸馏进 actor；原文未明确报告额外的推断期优化或搜索步骤。

**复现信息**

复现方法所必需的结构性细节包括：两个在线评论家及对应目标网络；评论家必须同时提供回报均值 Q和标准差 σ；悲观扰动满足 ε∼N(0,μI)并使用 |ε|保证只向下修正；目标值取两个目标评论家悲观估计的最小值；评论家采用 Huber 而非均方误差；经验回放不使用按历史 TD 误差的优先采样；目标网络按 $θ_i$′←τθ_i+(1−τ)θ_i′更新。μ、β_ω、β_ξ、c、τ及 α分别控制悲观扰动、两类加权、数值稳定、目标网络跟随速度和熵强度；这些参数的具体数值、σ的网络参数化方式、期望项的批量估计方式以及与 TD3/DDPG 集成时对熵项和随机策略的具体改写，在所给章节中原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- OpenAI Gym连续控制基准：6个任务，包括HalfCheetah、Ant、Hopper、Walker2d、Humanoid和BipedalWalker；状态维度为11至376，动作维度为3至17。其作用是检验标准机器人运动控制任务上的最终回报、收敛速度和跨任务一致性。原文未给出训练集、验证集或测试集划分，因为强化学习评测通过智能体与模拟环境在线交互完成。
- PyBullet连续控制基准：4个任务，包括HalfCheetahBulletEnv、AntBulletEnv、HopperBulletEnv和Walker2DBulletEnv；状态维度为15至28，动作维度为3至8。作者将其视为环境动力学噪声更强的测试平台，用于检验CWAC对噪声及价值估计误差的鲁棒性。
- DeepMind Control Suite（DMC）：12个任务，覆盖reacher、walker、hopper、fish、swimmer、pendulum、cheetah、quadruped和finger等控制问题；状态维度为3至78，动作维度为1至12。其作用是在较短的500K交互预算下检验样本效率、任务多样性和跨控制场景的泛化表现。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**最终平均评估回报**

Gym报告10个随机种子上最后10次评估分数的平均回报；PyBullet和DMC报告10个随机种子上最后10个评估episode的平均回报。它衡量训练结束时策略获得的累计奖励，但不同任务间的绝对回报尺度并不统一。 （通常越高越好，因为更高累计奖励表示策略更好地完成环境目标。）

</div>
<div class="metric-item" markdown="1">

**跨任务平均回报（Avg.）**

将同一基准中各任务的最终平均回报再作算术平均，用于给出总体比较。由于各任务奖励尺度不同，该指标适合做本文表内的粗略汇总，不应被解释为严格归一化的跨任务综合能力。 （在同一张表和相同任务集合内越高越好，但会受到高回报尺度任务的较大影响。）

</div>
<div class="metric-item" markdown="1">

**Q值估计误差**

定义为Q(s,a)-G^π(s,a)，其中Q(s,a)是critic对状态动作对的估计，G^π(s,a)是策略π下的经验回报；正值对应过估计，负值对应低估，接近零且波动较小表示价值学习更准确、稳定。 （绝对值越小且时间曲线越平稳越好，因为这意味着价值预测更接近经验回报，并减少错误向策略更新传播。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 6个Gym连续控制任务上的总体比较

<div class="result-value" markdown="1">

CWAC在表2的6个任务中均取得最高平均回报，跨任务Avg.为5792；VIAC、ALH、LAP、SAC和TD3分别为5022、4403、4472、4127和4358。作者据此计算CWAC相对这些方法的平均指标提升分别为15.3%、31.5%、29.5%、40.3%和32.9%。

</div>

这说明在本文采用的Gym任务、训练预算和评测协议下，CWAC的优势不是由单一任务拉动：它在运动类型、状态维度和动作维度不同的6项任务中都取得表内最佳最终均值。尤其是相对直接骨架SAC的提升支持新增机制有效，而不只是SAC本身的能力。不过，跨任务Avg.没有做奖励尺度归一化，不能作为跨基准的绝对综合能力分数；10个种子的均值与标准差也不能替代显著性检验。

<div class="result-source" markdown="1">

来源：第5.3节，表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 2, CWAC achieves the best overall performance among all benchmark methods, including VIAC, ALH, LAP, SAC, and TD3, with relative improvements of 15.3%, 31.5%, 29.5%, 40.3%, and 32.9%, respectively, in average evaluation metrics.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 4个动力学噪声较强的PyBullet任务上的比较

<div class="result-value" markdown="1">

CWAC在4个任务中均取得最高平均回报，跨任务Avg.为2680；VIAC、ALH、LAP、SAC和TD3分别为2465、123、2482、1947和2036。作者报告CWAC相对SAC的平均回报提升为37.6%，且每个算法均训练2M交互步、使用10个随机种子。

</div>

PyBullet用于测试在更强环境噪声下，按预测不确定性抑制不可靠更新是否仍然有益。CWAC在全部4项任务领先，且优于只按TD误差优先采样的LAP，结果与论文关于“高TD误差可能来自噪声、不能简单放大”的动机一致。但实验只提供最终回报和曲线，不能单凭这些结果确定增益究竟分别来自不确定性加权、悲观采样还是其他实现交互；因果归因仍需组件消融。

<div class="result-source" markdown="1">

来源：第5.4节，表3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Specifically, CWAC, VIAC, and LAP improve the average return over SAC by 37.6%, 26.6%, and 27.5%, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 12个DMC任务、每项500K环境步下的样本效率与广泛性比较

<div class="result-value" markdown="1">

CWAC的跨任务Avg.为698，高于VIAC的548、ALH的383、LAP的576、SAC的456和TD3的479；作者称CWAC在12项任务中的8项达到表内最佳结果。它并非每项都领先，例如walker-walk、cheetah-run、walker-run和quadruped-run由其他方法取得更高均值。

</div>

在比PyBullet更短的500K步预算下取得最高总体均值，支持CWAC具有较好的样本效率和跨任务适用性；同时，只有8项任务最佳表明该方法并非普遍支配所有价值学习策略。该结果展示的是所选任务和超参数下的经验优势，不证明对DMC之外环境或更长训练预算也保持相同排序。

<div class="result-source" markdown="1">

来源：第5.5节，表4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across the 12 evaluated tasks, CWAC achieves the SOTA performance on 8 tasks, highlighting its robustness and effectiveness in diverse continuous control scenarios.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 核心组件消融和超参数敏感性主要只在Walker2d上进行，且节选没有提供去除协同加权、仅保留TD误差加权、仅保留不确定性加权、去除悲观采样等完整因子组合的数值表，因此难以精确分解各组件及其交互作用的贡献。
- 实验报告10个随机种子的均值和标准差，但未报告置信区间、显著性检验或归一化跨任务指标；此外，第5.1节给出的默认β_ω=2、β_ξ=1与第5.7节悲观系数分析中所称默认β_ω=1、β_ξ=2不一致，DMC描述还误称采用“四个任务”却实际列出12项，均需结合原论文和代码进一步核查。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- SAC：最大熵随机策略actor-critic，也是本文主要CWAC实现所依附的标准骨架；与SAC比较可直接判断新增协同加权和悲观估计相对原始骨架的增益。
- TD3：采用确定性策略和双critic抑制过估计的经典离策略算法；它提供不同于SAC的价值估计与策略更新机制，也用于检验CWAC能否迁移到非最大熵框架。
- LAP：基于TD误差的优先采样方法，是检验本文核心主张的重要对照，即单纯强调大TD误差样本是否可能同时放大噪声，而联合考虑不确定性能否更稳健。
- VIAC：使用更积极的价值改进与价值引导优化，代表直接强化价值改进的路线；与其比较主要检验CWAC的悲观、可靠样本优先策略是否比激进价值更新更稳定。

**实验想回答的问题**

- CWAC能否在Gym、PyBullet和DMC等动力学特性不同的连续控制环境中，相比代表性离策略actor-critic方法获得一致、稳定且可迁移到不同算法骨架的性能提升？
- 协同加权与随机悲观价值估计是否确实改善Bellman误差最小化和价值学习稳定性，并在超参数变化及非平稳扰动下保持有效？

**实验实现**

主要实验采用标准SAC网络设计，并在未特别说明时固定悲观系数μ=0.8、不确定性加权指数β_ω=2、TD误差重加权指数β_ξ=1。Gym结果基于10个随机种子，学习曲线阴影表示评估结果的半个标准差；PyBullet中每个算法训练2M环境交互步并运行10个随机种子；DMC中每个算法训练500K步并运行10个随机种子。表格中的“±”是跨试验标准差，曲线仅为可视化进行了统一平滑。算法扩展实验还把CWAC接入TD3和DDPG，并在6个Gym任务、统一超参数和相同实验条件下各运行10次。原文节选未明确说明评估频率、每次评估的episode数、环境版本之外的终止规则、统计显著性检验或模型选择流程。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Walker2d上改变随机悲观系数μ；每种配置训练2M步并使用10个随机种子，μ=0表示关闭随机悲观采样 | 当μ处于[0.6,1.2]时，CWAC在不同取值下均表现出稳定改进；μ=1.4时训练变得不稳定。该实验表明适度悲观具有较宽容的有效区间，但悲观程度过强可能引入额外估计偏差。 | 这一消融主要隔离随机悲观价值估计的强度：μ=0提供关闭该机制的参照，较大的μ会更偏向保守价值。有效区间说明结果不依赖一个极窄的精确取值，但μ=1.4的退化提醒悲观估计并非越强越好。原文未给出各μ配置的最终回报数值，因此不能量化每个取值相对μ=0的增益。 | 第5.7节，图6左<br><span class="experiment-evidence">When μ lies within the interval [0.6,1.2], CWAC demonstrates consistently stable performance improvements across different choices of μ, as shown in Figure 6 (left).</span> |
| Walker2d上改变不确定性加权指数β_ω；β_ω=0表示不使用不确定性加权 | β_ω=0相较β_ω∈[0.5,2]出现明显性能下降；随着β_ω增大，高不确定性样本的TD误差被更强地下调，但β_ω=4会放大TD误差整体波动并导致性能不稳定。 | 该对比隔离了“根据预测不确定性调整样本贡献”这一核心组件。关闭加权后的退化支持不确定性信息有独立价值，而β_ω=4的退化说明过度压低高不确定样本会改变误差分布并造成振荡。由于只有Walker2d上的曲线且无精确表格数值，这一结论尚不能保证在全部22个主实验任务上具有相同敏感性。 | 第5.7节，图6中<br><span class="experiment-evidence">When βω=0, no uncertainty weighting is applied, resulting in a notable performance drop compared to settings with βω∈[0.5,2], as shown in Figure 6 (center).</span> |

**定性案例**

- 价值估计误差图提供了与最终回报互补的诊断：VIAC在Ant上的TD误差出现明显波动，并与约1.5M步后的性能下降相伴；ALH则在Hopper和BipedalWalker上表现出较明显的价值低估。作者分别将其归因于VIAC过于激进的价值改进和ALH在TD3价值平滑之上进一步增强保守性。更谨慎的解释是，这些曲线揭示了不同方法的失败模式，但尚未通过受控干预证明所述机制就是唯一原因。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper proposes an uncertainty-aware off-policy actor-critic algorithm to mitigate value overestimation.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`abfde6cbcf203876f732d98c6deb68875e70c406acedbed1773e52334fbce96e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
