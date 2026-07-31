---
title: "[论文解读] ReDiPPO: Reference-Guided Value Calibration and Discrepancy-Aware Token Reweighting for Mathematical Reasoning"
description: "[arXiv 2607.27631][对齐 / RLHF] ReDiPPO利用仅在训练期提供给评论器的参考答案校准中间状态价值，并依据参考引导评论器与标准评论器的分歧调整逐词元优势权重，以改善数学推理中的信用分配。"
arxiv_id: "2607.27631"
announcement_date: "2026-07-31"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.375368+00:00"
source_sha256: "e4da4136d4a22bfa15d4620c1e831f7933ae8a0649366a42ac6bcec7f84b2df5"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "强化学习"
  - "数学推理"
  - "可验证奖励强化学习"
  - "近端策略优化"
  - "价值估计"
  - "token级信用分配"
  - "稀疏终局奖励"
  - "参考答案特权信息"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2607.27631</p>

# ReDiPPO: Reference-Guided Value Calibration and Discrepancy-Aware Token Reweighting for Mathematical Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Zhang, Zhenrong, Wu, Fei, Du, Jun, Zhang, Jianshu, Wei, Si</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27631) · [PDF 下载](https://arxiv.org/pdf/2607.27631) · **关键词** 数学推理, 可验证奖励强化学习, 近端策略优化, 价值估计, token级信用分配, 稀疏终局奖励, 参考答案特权信息<br>
**代码**: [https://github.com/cii030/ReDiPPO](https://github.com/cii030/ReDiPPO)

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

ReDiPPO利用仅在训练期提供给评论器的参考答案校准中间状态价值，并依据参考引导评论器与标准评论器的分歧调整逐词元优势权重，以改善数学推理中的信用分配。

**不用术语来说**：数学推理模型通常要经过很多中间步骤才能得到最终答案，但训练系统往往只在最后判断答案是否正确，因此很难知道前面每一步究竟是有益还是有害。PPO虽能借助评论器逐步评价推理过程，但评论器只看到题目和尚未完成的解答，容易误判看似合理却最终错误的步骤，也可能低估尚未完成但方向正确的推导，进而向策略模型提供不可靠的学习信号。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出参考引导的价值校准：训练时让评论器同时观察题目、部分推理轨迹和参考答案，以更充分的信息估计中间状态能否导向正确结果；参考答案不提供给策略模型，因此不改变其仅根据题目作答的接口。
- 提出分歧感知的词元重加权：保留不看参考答案的标准评论器，将它与参考引导评论器在同一状态上的价值差异转化为有界的逐词元权重，用于调整PPO优势，从而重点处理参考盲评论器较可能误判的推理位置。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型的数学推理强化学习，具体处于“可验证奖励强化学习”（RLVR）场景：策略模型根据数学题生成包含多步推导的长回答，自动验证器将最终答案与参考答案比较，并给出稀疏的终局奖励。关键问题是如何把这个只在回答末尾出现的结果信号分配给前面各个生成步骤。无评论者方法如 GRPO、DAPO 和 GSPO 通常把同一个回答级优势信号广播给全部 token，简单但无法区分哪些中间步骤更有价值；PPO 则训练价值模型（评论者）估计各中间状态最终答对的可能性，从而提供依赖状态的 token 级信用分配。然而，标准评论者只能观察题目与尚未完成的部分回答：局部合理的推导可能最终出错，暂时不确定的推导也可能通向正确答案，因此在长推理轨迹和稀疏终局奖励下容易产生不准确的价值与优势估计。本文关注的背景矛盾是：参考答案已经被验证器用于确定终局奖励，却通常不提供给负责中间价值判断的评论者。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**可验证奖励强化学习（RLVR）**

策略模型生成数学解答后，由自动验证器比较最终答案和参考答案，得到客观、可扩展的结果奖励。该设置通常不直接标注每一步推导是否正确，因此监督信号稀疏。

</div>
<div class="concept-item" markdown="1">

**近端策略优化（PPO）与评论者**

PPO 同时使用生成回答的策略模型和预测未来回报的价值模型（评论者），并通过限制单次策略更新幅度来保持训练稳定。评论者对每个部分回答状态给出价值估计，使 PPO 原则上能够计算 token 级优势并判断某次生成动作应被鼓励还是抑制。

</div>
<div class="concept-item" markdown="1">

**token 级信用分配**

信用分配是把最终答对或答错的结果归因到生成序列中的具体决策；token 级分配意味着不同位置可以获得不同训练信号。若所有 token 共用同一回答级信号，模型便难以识别真正推动正确推理或导致错误的局部步骤。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是数学题目、训练数据附带的参考答案，以及策略模型基于题目生成的长推理回答；输出是经过强化学习更新、在推理时仅接收题目的数学推理策略。训练阶段假设最终答案能够被自动验证，并据此获得稀疏终局奖励；策略在训练和推理时均不读取参考答案。标准 PPO 评论者根据题目和部分回答估计中间状态价值，而本文额外允许参考引导评论者在训练时读取参考答案，将其视为“特权信息”，以更可靠地判断当前部分轨迹能否到达正确结果。两个评论者对同一 token 状态的估计差异还可用于识别参考盲评论者难以判断的状态；本文的背景任务因此不是增加过程级人工标注，而是在保持终局奖励设定的同时改善 token 级价值估计与信用分配。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入给策略模型的数学题目或提示。

</div>
<div class="notation-item" markdown="1">

**$y_{1:t}$**

策略已经生成到位置 $t$ 的部分回答，即当前中间推理状态。

</div>
<div class="notation-item" markdown="1">

**$y^{\mathrm{ref}}$**

训练样本附带的参考答案，仅供验证器和参考引导评论者使用，不输入策略模型。

</div>
<div class="notation-item" markdown="1">

**$V(x,y_{1:t})$**

评论者对题目 $x$ 和部分回答 $y_{1:t}$ 最终能够获得正确结果奖励的价值估计；此处是为说明问题设置而采用的通用记号，原文节选未明确规定其符号形式。

</div>

</div>

**直接相关的工作**

- **GRPO、DAPO 与 GSPO**: 这些无评论者方法不训练价值模型，而是构造回答级优势并将同一轨迹信号用于回答中的所有 token，从而避免价值估计误差，但不能显式区分同一推理轨迹内不同中间状态的贡献。ReDiPPO 与其主要区别是保留 PPO 评论者，以追求状态相关的 token 级信用分配。
- **Open-Reasoner-Zero、VAPO 与既有 PPO 改进**: 这些工作表明，在改进价值学习、价值校准或广义优势估计后，基于评论者的 PPO 在数学推理中仍有竞争力；VinePPO 等方法还可通过额外续写估计中间价值。本文所针对的剩余背景问题是：这些方法的标准评论者仍需在看不到参考答案的情况下评价部分解答，而 ReDiPPO 将参考答案作为训练期评论者特权信息，并保持策略的题目输入接口不变。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在基于可验证奖励的强化学习（RLVR）中，模型生成长篇数学推理后，自动验证器通常只根据最终答案是否匹配参考答案给出终局奖励。奖励稀疏且推理链较长，使训练系统难以把最终成败准确归因到具体词元；一旦中间状态评价失真，PPO优势的方向和幅度都会被扭曲，导致策略更新低效甚至错误。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **无评论器的GRPO、DAPO与GSPO类方法**：不训练价值模型，而是根据整条回答的结果构造回答级优势，并将同一个轨迹级信号分配给回答中的所有词元。这类方法实现简单且有效，但不能区分不同推理步骤对最终结果的具体作用。
- **基于标准评论器的PPO及其改进方法**：评论器依据题目和当前部分回答估计状态价值，再据此形成逐词元优势；已有工作通过评论器预训练、广义优势估计（GAE）变体或系统稳定化来改善训练，但评论器仍需在不知道目标答案的条件下判断未完成推理的前景。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 回答级方法把相同信号广播给全部词元，无法区分关键正确步骤、无效步骤与导致错误的步骤，因此牺牲了细粒度信用分配能力。
- 标准PPO评论器只观察题目和部分回答：局部合理的步骤可能最终走向错误，而暂未完成但有希望的推导可能显得不确定。此类价值误差会直接污染逐词元优势，使策略更新的方向或强度不准确。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有RLVR系统存在信息使用上的不对称：参考答案已被用于确定终局奖励，却没有提供给负责中间状态评价和逐词元信用分配的评论器。此前的价值学习改进主要优化训练方式或稳定性，尚未充分研究如何把参考答案作为训练期特权信息来校准评论器，并进一步利用“有参考”与“无参考”价值判断之间的差异识别困难状态。

</div>
<div markdown="1"><span>核心问题</span>

能否在不让策略模型访问参考答案、因而保持标准推理接口的前提下，让评论器在训练时利用参考答案获得更可靠的状态价值，并把参考引导评论器与标准评论器的逐词元分歧转化为有效的PPO更新权重？

</div>
<div markdown="1"><span>作者直觉</span>

参考答案相当于给评论器提供一个已知目的地：面对一段尚未完成的推理，它可以更准确地判断当前方向是否可能到达正确结果。与此同时，如果看过参考答案和没看过参考答案的两个评论器对某个状态判断差异很大，说明该位置仅凭局部轨迹较难评价，也更可能产生不可靠的信用信号；因此用这种分歧增强相应优势的作用，有望把学习重点放在真正困难且信息敏感的推理位置。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ReDiPPO在标准PPO的“策略模型加价值模型”结构上增加一个参考答案引导的价值模型，并明确分工：参考引导评论家$V_{\psi}^{\mathrm{ref}}$读取题目、当前部分解答和标准答案，用其价值预测构造逐词元优势；标准评论家$V_{\phi}^{\mathrm{std}}$只能读取题目和当前部分解答，用作无参考信息的对照。两个评论家对同一部分推理状态的预测差异，被视为该状态对普通评论家而言有多难判断，并转换为有上下界的逐词元权重。加权优势经过掩码白化后进入PPO裁剪目标，决定每个已采样词元对策略更新的相对贡献。
端到端看，策略始终只接收题目$x_i$并生成回答$y_i$；标准答案$z_i$仅在训练时提供给验证器和参考引导评论家，既不加入策略的生成上下文，也不改变终局奖励$G_i$。因此，该方法利用“训练时特权信息”改善信用分配，而不改变部署接口。直观地说，参考引导评论家像一位拿着答案批改草稿的教师，标准评论家像一位只看草稿的教师；两者分歧越大的推理位置越值得重点学习，但权重裁剪会防止少数位置支配整个更新。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 采样推理轨迹并取得可验证奖励

旧策略仅以$x_i$为条件自回归采样回答$y_i$，形成轨迹$\tau_i=(x_i,z_i,y_i,G_i)$；验证器比较回答中的最终答案与$z_i$，给出终局回报$G_i=\mathcal{R}(x_i,y_i,z_i)$。中间词元没有直接奖励。

<div class="method-step__io" markdown="1">

**输入**：从数据集$\mathcal{D}$采样的一批题目与参考答案$\{(x_i,z_i)\}_{i=1}^{B}$，以及旧策略$\pi_{\theta_{\mathrm{old}}}$和规则验证器$\mathcal{R}$。<br>
**输出**：包含题目、参考答案、完整回答和终局回报的训练轨迹，以及回答中所有有效词元位置的掩码$m_{i,t}$。

</div>

**直观理解**：模型先独立完成整道题，最后只得到“答对或答错”一类结果。后续步骤要把这个末端结果合理分配给此前的各个词元决策。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 双评论家对齐评估部分推理状态

标准分支计算$v_{i,t}^{\mathrm{std}}=V_{\phi}^{\mathrm{std}}(s_{i,t})$；参考分支把$z_i$按固定模板加入评论家上下文，计算$v_{i,t}^{\mathrm{ref}}=V_{\psi}^{\mathrm{ref}}(s_{i,t},z_i)$。两个分支评估完全相同的有效回答词元位置。

<div class="method-step__io" markdown="1">

**输入**：同一轨迹中的部分状态$s_{i,t}=(x_i,y_{i,<t})$、参考答案$z_i$，以及标准评论家$V_{\phi}^{\mathrm{std}}$和参考引导评论家$V_{\psi}^{\mathrm{ref}}$。<br>
**输出**：每个有效位置上的无参考价值预测$v_{i,t}^{\mathrm{std}}$与参考引导价值预测$v_{i,t}^{\mathrm{ref}}$。

</div>

**直观理解**：两名评审看同一份尚未完成的草稿，其中一名能查看标准答案，另一名不能。输入条件之外的因素保持一致，因而二者分歧可反映参考答案带来的判断变化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 构造参考引导优势与分歧权重

在$\gamma=\lambda=1$且仅有终局奖励时，先计算参考引导优势$\hat A_{i,t}^{\mathrm{ref}}=G_i-v_{i,t}^{\mathrm{ref}}$；再以$e_{i,t}=|v_{i,t}^{\mathrm{ref}}-v_{i,t}^{\mathrm{std}}|$度量分歧，将其在$\mathcal{M}$上标准化、以$1$为中心并裁剪到$[w_{\min},w_{\max}]$。

<div class="method-step__io" markdown="1">

**输入**：终局回报$G_i$、两组价值预测$v_{i,t}^{\mathrm{ref}}$和$v_{i,t}^{\mathrm{std}}$，以及批内有效位置集合$\mathcal{M}=\{(i,t):m_{i,t}=1\}$。<br>
**输出**：逐词元参考引导优势$\hat A_{i,t}^{\mathrm{ref}}$和有界正权重$w_{i,t}$。

</div>

**直观理解**：参考分支负责判断该词元相对预期是好是坏；双分支分歧负责判断这个位置对普通评论家是否难评。分歧只是困难度代理，并不等同于无法直接观测的真实价值误差。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 加权、白化并更新策略

先计算$w_{i,t}\hat A_{i,t}^{\mathrm{ref}}$，再在有效词元上减去掩码均值并除以掩码标准差，得到$\tilde A_{i,t}$；随后把它代入PPO裁剪代理目标更新$\pi_\theta$。评论家预测、权重和优势在演员更新时均停止梯度，因此策略梯度不会反向修改评论家。

<div class="method-step__io" markdown="1">

**输入**：逐词元优势$\hat A_{i,t}^{\mathrm{ref}}$、分歧权重$w_{i,t}$、有效位置掩码$m_{i,t}$和新旧策略的词元概率。<br>
**输出**：更新后的策略参数$\theta$，以及供下一轮采样使用的新旧策略同步结果$\theta_{\mathrm{old}}\leftarrow\theta$。

</div>

**直观理解**：高分歧位置在归一化前获得更大相对影响，但裁剪和白化共同限制更新尺度。PPO的概率比裁剪则避免策略一次偏离采样策略过远。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 分歧加权的参考引导优势

$$
\begin{aligned}
\hat{A}^{\mathrm{ref}}_{i,t} &= G_i-v^{\mathrm{ref}}_{i,t},\\
e_{i,t} &= \left|v^{\mathrm{ref}}_{i,t}-v^{\mathrm{std}}_{i,t}\right|,\\
\mu_e &= \frac{1}{|\mathcal{M}|}\sum_{(i,t)\in\mathcal{M}}e_{i,t},\qquad
\sigma_e^2 = \frac{1}{|\mathcal{M}|}\sum_{(i,t)\in\mathcal{M}}(e_{i,t}-\mu_e)^2,\\
w_{i,t} &= \mathrm{clip}\!\left(1+\frac{e_{i,t}-\mu_e}{\sigma_e+\epsilon_e},w_{\min},w_{\max}\right),\\
\tilde{A}_{i,t} &= \mathrm{Whiten}_m\!\left(w_{i,t}\hat{A}^{\mathrm{ref}}_{i,t}\right).
\end{aligned}
$$

**符号说明**

- $\hat{A}^{\mathrm{ref}}_{i,t}$：第$i$条回答在第$t$个词元处、以参考引导价值为基线的优势估计。
- $G_i$：验证器为第$i$条完整回答给出的终局回报。
- $v^{\mathrm{ref}}_{i,t}$：能观察参考答案的评论家对部分状态的价值预测。
- $v^{\mathrm{std}}_{i,t}$：不能观察参考答案的标准评论家对同一部分状态的价值预测。
- $e_{i,t}$：两个评论家在该词元状态上的绝对预测分歧。
- $\mathcal{M}$：当前批次内所有有效回答词元位置的集合。
- $\mu_e$：有效词元上分歧值的批内均值。
- $\sigma_e$：有效词元上分歧值的批内标准差。
- $\epsilon_e$：防止标准化时分母过小的数值稳定常数。
- $w_{i,t}$：以一为中心并经过上下界裁剪的逐词元分歧权重。
- $w_{\min},w_{\max}$：权重的正下界与上界。
- $\mathrm{Whiten}_m$：只在掩码标记的有效词元上执行减均值、除标准差的白化操作。
- $\tilde{A}_{i,t}$：供演员PPO目标使用的最终归一化加权优势。

<div class="equation-explanation" markdown="1">

**直观理解**：第一行用“实际终局结果减去参考引导评论家的预期”判断该词元所在状态优于还是劣于预期。其余各行把双评论家分歧转换成稳定的相对权重：高于批内平均分歧的位置通常被加强，低于平均的位置通常被减弱，但上下界限制极端权重；最后的白化保持PPO常用的归一化更新形式。<br>
**原文位置**：第3.3节公式(8)与第3.4节公式(9)–(13)

</div>

</div>

<div class="equation-block" markdown="1">

#### ReDiPPO演员裁剪目标

$$
\mathcal{L}_{\mathrm{ReDiPPO}}(\theta)=\mathrm{E}_{(i,t)\in\mathcal{M}}\left[\min\left(\rho_{i,t}\tilde{A}_{i,t},\bar{\rho}_{i,t}\tilde{A}_{i,t}\right)\right],\quad \rho_{i,t}=\frac{\pi_{\theta}(y_{i,t}\mid s_{i,t})}{\pi_{\theta_{\mathrm{old}}}(y_{i,t}\mid s_{i,t})},\quad \bar{\rho}_{i,t}=\mathrm{clip}(\rho_{i,t},1-\epsilon,1+\epsilon).
$$

**符号说明**

- $\mathcal{L}_{\mathrm{ReDiPPO}}(\theta)$：对策略参数进行最大化的ReDiPPO裁剪代理目标。
- $\theta$：当前待优化策略的参数。
- $\pi_{\theta}$：当前策略在部分状态下生成下一词元的条件概率分布。
- $\pi_{\theta_{\mathrm{old}}}$：采样当前训练轨迹时使用的旧策略。
- $s_{i,t}$：第$i$条轨迹在位置$t$的状态，即题目与此前已生成词元组成的上下文。
- $y_{i,t}$：第$i$条回答在位置$t$实际采样的词元。
- $\rho_{i,t}$：当前策略与旧策略对已采样词元所赋概率之比。
- $\bar{\rho}_{i,t}$：限制在区间$[1-\epsilon,1+\epsilon]$内的概率比。
- $\epsilon$：PPO策略概率比的裁剪半径。
- $\tilde{A}_{i,t}$：经分歧加权和掩码白化后的逐词元优势。
- $\mathcal{M}$：参与目标聚合的有效回答词元位置集合。

<div class="equation-explanation" markdown="1">

**直观理解**：目标根据$\tilde A_{i,t}$的正负提高或降低已采样词元的概率，同时取未裁剪项与裁剪项中的较小者，限制单次策略变化可获得的收益。ReDiPPO相对标准PPO的核心变化位于$\tilde A_{i,t}$的构造，演员目标本身仍保留PPO的保守更新机制。<br>
**原文位置**：第3.5节公式(14)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练包含三个相互配合但梯度彼此隔离的目标。演员最大化公式(14)的裁剪代理目标，其学习信号是由参考引导价值、双评论家分歧权重和掩码白化共同得到的$\tilde A_{i,t}$；更新演员时，价值预测、权重与优势均被分离出计算图。两个评论家则各自最小化PPO式裁剪价值损失：对分支$b\in\{\mathrm{std},\mathrm{ref}\}$，当前预测$v_{i,t}^{b}$先相对旧预测$v_{i,t}^{b,\mathrm{old}}$裁剪到宽度$\epsilon_v$的区间，损失取当前预测和裁剪预测相对共同目标$G_i$的平方误差较大者，并在有效词元上聚合。这样既让参考分支提供更有信息的演员基线，又让标准分支保持可比较的无参考判断；分歧只改变各词元策略梯度项的相对权重，不直接修改验证器奖励。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 参考引导价值校准**

参考引导评论家以$(s_{i,t},z_i)$为输入并预测$v_{i,t}^{\mathrm{ref}}$，该预测是演员优势的唯一价值基线；标准评论家的$v_{i,t}^{\mathrm{std}}$不直接构造演员优势。两者均以终局回报$G_i$为回归目标，并采用价值预测裁剪来限制单轮变化。

> 直观理解：部分推导即使表面合理，也可能已经偏离正确答案；反之，尚未完成的正确思路也可能显得不确定。允许评论家查看答案，有助于它判断当前草稿是否仍与正确终点相容，但策略本身看不到答案，因此不会形成训练与部署输入不一致的依赖。

**2. 参考—标准分歧感知重加权**

模块计算$e_{i,t}=|v_{i,t}^{\mathrm{ref}}-v_{i,t}^{\mathrm{std}}|$，在批内所有有效词元上用均值$\mu_e$和标准差$\sigma_e$标准化，再生成以$1$为中心并裁剪到$[w_{\min},w_{\max}]$的正权重$w_{i,t}$。约束$0<w_{\min}\leq1\leq w_{\max}$保留普通参考引导PPO作为名义更新，同时防止极端分歧造成不受控放大。

> 直观理解：若查看答案后对某一步的评价发生很大变化，说明仅凭部分草稿难以可靠判断该步，方法便提高该位置的训练关注度。这里采用相对分歧而非绝对阈值，使权重能适应不同批次和训练阶段的数值尺度。

**3. 逐词元PPO演员更新**

加权优势先在有效词元集合上进行掩码白化，得到$\tilde A_{i,t}$；演员随后以新旧策略概率比$\rho_{i,t}$及其裁剪版本$\bar\rho_{i,t}$优化逐词元PPO目标。优势符号控制已采样词元被鼓励或抑制，白化后的幅度控制该词元相对更新强度。

> 直观理解：方法没有替换PPO的稳定更新机制，而是改变PPO收到的逐词元学习信号。相比把同一个回答级分数广播给整段回答，它能区分同一推理链中不同位置的贡献。

**训练与推理**

训练前，作者针对每个策略骨干，用对应策略检查点为每道训练题采样八个回答，并由规则验证器赋予二元标签。由于初始策略准确率较高、错误回答不足，错误轨迹会被上采样，使正确与错误样本大致平衡；两个评论家均从与策略相同的检查点初始化，并在强化学习前进行两个训练轮次的价值预训练，以逐词元价值预测和验证器回报之间的均方误差为目标。标准分支读取题目与部分回答，参考分支额外读取参考答案。
强化学习阶段每轮依次执行：旧策略仅依据题目采样回答；验证器计算终局回报；两个评论家在对齐的有效词元状态上估值；参考分支形成逐词元优势；双分支分歧形成权重并产生白化优势；两个评论家以共同回报更新；演员以ReDiPPO裁剪目标更新；最后同步旧策略参数。推理阶段只保留并调用训练后的策略$\pi_\theta$，输入仍是普通题目$x$，不需要参考答案、验证器、标准评论家或参考引导评论家，因此参考答案属于纯训练期特权信息。

**复现信息**

复现和公平解释所需的关键设置包括：参考答案仅通过固定文本模板“The ground truth answer is {answer}.”加入参考评论家的上下文，绝不能加入策略输入；两评论家必须评估同一批轨迹中的同一组有效回答词元，否则逐位置分歧不可比较。方法采用终局奖励并设置$\gamma=\lambda=1$，因此参考优势简化为$G_i-v_{i,t}^{\mathrm{ref}}$；分歧统计、白化和损失聚合均只覆盖$m_{i,t}=1$的有效回答词元。权重须满足$0<w_{\min}\leq1\leq w_{\max}$，且在演员更新时评论家输出、权重和优势均需停止梯度。原文节选未给出$w_{\min}$、$w_{\max}$、$\epsilon$、$\epsilon_v$、$\epsilon_e$的具体数值，也未明确报告优化器、学习率、批大小和白化稳定常数；这些参数不能从所给章节推断。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- DAPO-17K：数学推理提示训练集，用于所有强化学习方法；原文未在所给章节中说明具体划分及本实验实际使用的样本数。其作用是提供可进行结果验证的训练问题。
- DeepMath-103K整数答案子集：包含40,188道最终答案为整数的问题，与DAPO-17K共同用于强化学习训练。整数答案允许通过规则验证器可靠地产生二元结果奖励；原文未明确报告训练、验证划分。
- 六项评测基准：AIME 2024、AIME 2025、AIME 2026、HMMT 2025、Minerva Math和OlympiadBench。前三项AIME与HMMT主要检验竞赛数学推理，后两项扩展到更广泛的数学问题；所有方法采用相同的答案抽取与验证流程。实验还在这六个测试集上分析评论家的分段解释方差，但所给章节未报告各基准样本规模。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**avg@32／avg@8**

对同一道题进行多次采样后计算平均正确率；AIME与HMMT报告avg@32，其余基准报告avg@8。表1中的数值均为百分比。该指标衡量策略在随机生成条件下产出可验证正确答案的平均能力，而非单次贪心解码准确率。 （越高越好，因为更高数值表示采样回答中正确结果所占比例更高；但不同采样次数下的数值不宜直接视为完全等价。）

</div>
<div class="metric-item" markdown="1">

**价值解释方差（EV）**

衡量评论家预测值$V_{i,t}$能够解释回报目标$R_{i,t}$变化的程度，定义为$1-\mathrm{Var}(R-V)/(\mathrm{Var}(R)+\epsilon)$，其中$(i,t)$遍历有效回答词元，$\epsilon$用于数值稳定。它直接检验价值估计是否贴近训练回报，而不是检验最终策略准确率。 （越高越好，因为残差方差相对回报方差越小，说明评论家校准越准确；低值或负值表示预测解释能力较弱。）

</div>
<div class="metric-item" markdown="1">

**路径选择准确率（PSA）**

先以回答内有效词元价值的均值$s_i$为每条推理路径打分，再检查同一提示的多条回答中，评论家评分最高者是否正确。只在同时包含正确与错误回答的提示组上计算，以避免全对或全错组掩盖区分能力。 （越高越好，因为这表示评论家更常把真正成功的推理路径排在首位；该指标反映排序能力，不等同于价值数值本身已经完全校准。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3-4B-Instruct-2507上的六基准平均表现

<div class="result-value" markdown="1">

ReDiPPO平均得分为56.03，高于最强对照GSPO的54.46，提升1.57个百分点；同时在六个单项基准上均取得该骨干下的最高分。相对严格匹配的PPO基线53.66，则提升2.37个百分点。

</div>

这说明在普通指令微调骨干上，完整方法的收益不仅来自“做过强化学习”，也超过了无评论家方法和共享训练条件的标准PPO。六项均领先增强了结果的一致性，但它仍只证明所测数学基准与采样协议下的优势，不能推出对其他任务或解码方式同样有效。

<div class="result-source" markdown="1">

来源：第4.2节 Overall Performance；表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Qwen3-4B-Instruct, it ranks first on every benchmark and improves the strongest baseline average from 54.46 to 56.03.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3-4B-Thinking-2507上的六基准平均表现

<div class="result-value" markdown="1">

ReDiPPO平均得分为73.90，高于最强基线GSPO的73.15，提升0.75个百分点；六项中领先五项，但AIME 2025上DAPO为76.88，略高于ReDiPPO的76.77。相对PPO的72.71，提升1.19个百分点。

</div>

在本身已具备较强推理能力的Thinking骨干上，增益较小但仍覆盖多数基准，表明该方法并非只对较弱的指令模型有效。不过，AIME 2025并未领先且平均优势有限；没有多次独立运行、方差或显著性检验时，不能判断小幅差异是否稳定超出训练随机性。

<div class="result-source" markdown="1">

来源：第4.2节 Overall Performance；表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Qwen3-4B-Thinking, ReDiPPO raises the best baseline average from 73.15 to 73.90 and leads on five of the six benchmarks, with DAPO slightly ahead on AIME 2025.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### OLMo3-7B-Instruct-DPO上的六基准平均表现

<div class="result-value" markdown="1">

ReDiPPO平均得分为41.13，高于最强基线DAPO的40.47，提升0.66个百分点，并在六项中的五项取得最高结果；相对PPO的39.51提升1.62个百分点。

</div>

跨到不同模型家族和7B规模后仍有平均收益，支持方法具有一定骨干可迁移性。它也表明ReDiPPO相对PPO的优势不是Qwen特有现象；但ReDiPPO在Minerva上的51.08低于DAPO的51.36，因此不能声称每个数据集都必然受益。

<div class="result-source" markdown="1">

来源：第4.2节 Overall Performance；表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ReDiPPO also improves the strongest OLMo3-7B-Instruct-DPO baseline from 40.47 to 41.13 and obtains the best result on five of the six benchmarks.

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

- Vanilla：强化学习前的初始策略检查点，用于衡量RLVR训练相对于原始模型究竟带来多少总体收益。
- DAPO：不使用评论家的RLVR基线，可检验ReDiPPO的收益是否超过强势的结果奖励策略优化方法，而非仅超过传统PPO。
- GSPO：另一种无评论家的策略优化基线，与DAPO共同覆盖不同的无价值网络训练方案，避免只选取单一对手。
- PPO：使用标准评论家，并与ReDiPPO共享价值预训练协议、训练数据、采样预算和评测过程。这是最关键的受控基线，用来隔离参考引导价值校准与差异感知词元重加权的总体贡献。

**实验想回答的问题**

- 在相同训练数据、采样预算和评测协议下，ReDiPPO能否在不同类型与规模的策略骨干上稳定超过初始模型、无评论家RLVR方法以及标准PPO？
- 参考答案引导的价值校准是否确实改善评论家的价值估计与推理路径选择能力，且这种改进能否与差异感知的词元级优势重加权互补，而不是仅通过生成更长回答获得收益？

**实验实现**

实验覆盖Qwen3-4B-Instruct-2507、Qwen3-4B-Thinking-2507和OLMo3-7B-Instruct-DPO三种策略骨干。评论家从对应策略检查点初始化，并按VAPO协议预训练两个周期。各方法使用全局批量512，每个提示采样8条回答；演员与评论家的学习率分别为$1\times10^{-6}$和$5\times10^{-6}$。由于奖励只在回答末尾给出，设置折扣因子与GAE参数$\gamma=\lambda=1$。PPO与ReDiPPO均使用非对称Clip-Higher，$\epsilon_{\mathrm{low}}=0.2$、$\epsilon_{\mathrm{high}}=0.28$，KL与熵损失系数均为0；ReDiPPO将差异权重裁剪到$[0.5,2.0]$。采样温度为1.0，指令模型最大回答长度为8192个词元，Qwen3-4B-Thinking为32768个词元。训练由VeRL实现。主表在AIME与HMMT上报告avg@32，在Minerva Math与OlympiadBench上报告avg@8；训练动态图中的AIME 2024使用avg@16，因此不能与主表数值直接混用。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 组件消融：PPO、仅加入参考引导评论家（+Ref.）与完整ReDiPPO | 仅加入参考引导价值校准后，Qwen3-Instruct、Qwen3-Think和OLMo-Inst的六基准平均准确率分别提高1.11、0.58和1.03个百分点；继续加入差异感知词元重加权，又分别提高1.26、0.61和0.59个百分点，使完整方法相对PPO的总提升达到2.37、1.19和1.62个百分点。 | 该消融先隔离“用参考答案改善评论家”，再测量“根据两类评论家的差异重加权词元优势”的增量，因此支持两个组件具有互补贡献，而非全部收益都来自额外评论家。不过这是顺序式消融：所给章节没有报告只启用重加权而不启用参考校准的独立条件，因而不能完整识别二者交互。 | 第4.3节 Component Contributions；图4<br><span class="experiment-evidence">Figure 4 shows that reference-guided value calibration consistently improves PPO, yielding gains of 1.11, 0.58, and 1.03 average-accuracy points on Qwen3-Inst., Qwen3-Think., and OLMo-Inst., respectively. Discrepancy-aware token reweighting provides a further 1.26, 0.61, and 0.59 points, increasing the total gains over PPO to 2.37, 1.19, and 1.62 points.</span> |
| 特权参考信息形式：简洁参考答案与预生成的较丰富参考解答 | 在最后五个共同的AIME 2024评测检查点上，答案版与解答版的avg@16分别为59.58和58.46，原文称答案版领先1.13个百分点。分段PSA上，解答版更常在回答中段领先，而答案版在最后20%区间的56个共同检查点中领先50次，解答版仅领先5次。 | 该实验检验更丰富的推导是否一定比最终答案更适合作为评论家特权信息。结果显示详细解答有助于判断中间进度，但简洁答案更利于末段路径选择，并在这次训练中带来更高下游准确率。由于每个变体只有一次训练，且解答来自单一生成流水线，这不能证明长参考普遍有害；它更可能说明单一路径解答会偏向特定推导。 | 附录D.1 Form of Privileged Reference Information；图8<br><span class="experiment-evidence">Averaged over the last five shared AIME 2024 evaluation checkpoints, the answer and solution variants obtain 59.58 and 58.46 avg@16, respectively, a 1.13-point advantage for the concise answer.</span> |

**定性案例**

- 参考—标准差异的响应级与位置级分析构成机制案例：高差异组同时呈现更长推理轨迹和更低成功率，说明差异可作为困难轨迹的经验指标；沿回答位置观察时，参考引导评论家的优势在后段扩大，说明同一回答中并非所有词元都同样需要参考信号。通俗地说，两位评论家“意见分歧”越大的位置，往往越可能是标准评论家难以判断的关键推理状态，因此对这些词元给予不同训练权重比整条回答统一加权更有针对性。该分析展示相关性与定位能力，但没有单独建立差异导致困难或性能提升的因果关系。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出用于提升LLM数学推理的PPO后训练方法，以参考引导价值估计和token级重加权改善信用分配。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`e4da4136d4a22bfa15d4620c1e831f7933ae8a0649366a42ac6bcec7f84b2df5`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
