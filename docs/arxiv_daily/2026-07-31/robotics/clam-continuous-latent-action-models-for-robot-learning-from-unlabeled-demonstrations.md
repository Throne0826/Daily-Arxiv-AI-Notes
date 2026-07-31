---
title: "[论文解读] CLAM: Continuous Latent Action Models for Robot Learning from Unlabeled Demonstrations"
description: "[arXiv 2505.04999][机器人 / 具身智能] CLAM旨在用少量带动作的任务无关玩耍数据，将大量无动作标签的机器人专家视频转化为可执行的连续控制策略，从而减少对昂贵专家遥操作数据的依赖。"
arxiv_id: "2505.04999"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:48.974368+00:00"
source_sha256: "e6ca0da979464ef4d47ac3e8722f4fcd7f0d96f87fd0140f70ea04abd7277fca"
tags:
  - "机器人 / 具身智能"
  - "仅观测模仿"
  - "连续潜在动作"
  - "逆动力学模型"
  - "前向动力学模型"
  - "任务无关探索数据"
  - "连续机器人控制"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2505.04999</p>

# CLAM: Continuous Latent Action Models for Robot Learning from Unlabeled Demonstrations

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Liang, Anthony, Czempin, Pavel, Hong, Matthew M., Zhou, Yutai, Wang, Jingzhen, Biyik, Erdem, Tu, Stephen</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2505.04999) · [PDF 下载](https://arxiv.org/pdf/2505.04999) · **关键词** 仅观测模仿, 连续潜在动作, 逆动力学模型, 前向动力学模型, 任务无关探索数据, 连续机器人控制<br>
**项目页**: [https://clamrobot.github.io/](https://clamrobot.github.io/)

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

CLAM旨在用少量带动作的任务无关玩耍数据，将大量无动作标签的机器人专家视频转化为可执行的连续控制策略，从而减少对昂贵专家遥操作数据的依赖。

**不用术语来说**：机器人通常要看着专家操作记录及其对应的电机指令，才能学会一项任务，但逐步记录这类指令需要人工遥操作，成本高且难以扩展。现实中更容易获得的往往只有展示机器人如何运动的视频，而没有每一时刻的控制指令；本文要解决的就是如何利用这些只有画面的示范，让机器人最终输出真实、连续的电机命令。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出CLAM，以连续潜在动作表示相邻观测之间的行为变化，并通过预测下一观测进行自监督学习；同时联合训练动作解码器，使潜在动作能够映射为真实机器人控制信号。
- 作者提出用少量任务无关玩耍数据完成潜在动作的控制落地，而不需要为每个新任务采集带动作标签的专家示范；作者进一步在真实WidowX机器人四项操作任务上验证了这一设定。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于机器人“仅观测模仿”（imitation from observation, IfO）研究：目标是从没有控制指令标签的专家观测序列中学习可执行策略。标准模仿学习通常需要由遥操作同步采集的“观测—动作”专家数据，但遥操作成本高，也难以覆盖大量任务与真实环境变化；相比之下，机器人视频、经视角与形态转换的人类视频以及缺少兼容动作格式的历史日志更容易获得。本文聚焦完全离线的连续控制场景：专家数据只提供机器人视角下的连续观测，而少量带动作数据来自与具体任务无关的自由探索。核心问题是先用自监督动力学预测发现能够描述相邻观测变化的连续潜在动作，再将该表示落地为真实电机指令，从而绕过对带动作专家示范的依赖。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**仅观测模仿（Imitation from Observation, IfO）**

示范仅包含观测序列，不提供产生这些状态变化的真实动作，学习器需要据此恢复或绕过缺失的动作信息。与标准模仿学习相比，其关键困难是无法直接监督策略输出机器人控制指令。

</div>
<div class="concept-item" markdown="1">

**逆动力学与前向动力学**

逆动力学模型根据相邻观测推断促成状态变化的动作；前向动力学模型则根据当前观测和动作预测下一观测。CLAM让二者形成自监督闭环，以“能否重建未来观测”约束潜在动作所表达的行为变化。

</div>
<div class="concept-item" markdown="1">

**潜在动作与动作落地**

潜在动作是在模型内部学习的低维行为表示，不必直接等同于机器人的关节或末端执行器命令；动作落地是使用动作解码器将该表示映射为真实、可执行的连续控制量。本文采用连续潜在空间，并用少量任务无关的带动作探索数据约束其可解码性。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入由两类离线数据组成：第一类是目标任务的无动作专家示范，只含连续观测序列；第二类是少量任务无关的 play data，其中观测与真实机器人动作成对记录。本文假设无动作示范已经呈现为与机器人形态和视角兼容的观测，因此不直接解决人类视频到机器人观测的转换问题，也不依赖在线环境交互或外部现成视觉模型。学习系统首先利用相邻观测训练潜在逆动力学模型 $f_{\phi}$，推断解释观测变化的连续潜在动作；潜在前向动力学模型 $g_{\psi}$ 根据观测历史和该潜在动作预测未来观测，以重建目标提供自监督信号。同时，系统用带动作 play data 联合训练动作解码器，使潜在动作能够映射为真实连续控制命令。训练完成后，$f_{\phi}$ 为无动作专家轨迹生成伪动作标签，标准模仿学习策略再从这些重标注轨迹中学习；部署时，策略预测潜在动作，动作解码器输出可直接执行的电机命令。最终输出是一个能够完成目标任务的机器人控制策略，而训练过程不需要任何带真实动作标签的目标任务专家示范。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$f_{\phi}$**

参数为 $\phi$ 的潜在逆动力学模型，根据连续观测推断两者之间的连续潜在动作。

</div>
<div class="notation-item" markdown="1">

**$g_{\psi}$**

参数为 $\psi$ 的潜在前向动力学模型，根据观测历史与潜在动作预测未来观测。

</div>

</div>

**直接相关的工作**

- **LAPO / Genie**: 同样利用潜在逆动力学模型为无动作轨迹生成标签，但原文指出这类方法主要研究具有小型离散动作空间的视频游戏，并常以向量量化构造离散潜在动作；CLAM针对高维、完全连续的机器人控制改用连续潜在动作与联合动作落地。
- **LAOM**: LAOM表明少量动作标签监督有助于潜在动作在存在干扰因素时用于下游任务，但其监督模块是测试时丢弃的单层线性层；CLAM使用训练与推理阶段共享的动作解码器进行联合监督，并将研究重点放在仿真及真实机器人操控。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大规模机器人模仿学习受制于数据采集：传统示范需要专家通过遥操作同步提供观测与动作，但遥操作昂贵、耗时，而且普通用户难以针对不同现场环境和新任务反复完成高质量控制。相比之下，无动作标签的机器人视角视频更容易获得，例如由人类视频转换出的机器人视角观测、互联网行为视频，以及动作格式缺失或不兼容的既有机器人日志。研究需求因此不是继续增加专家遥操作，而是从这些廉价的观测序列中恢复可供策略学习的控制信息。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **标准模仿学习与行为克隆**：使用机器人自身视角的专家观测—动作对，直接监督训练策略，使策略根据当前观测预测专家控制命令。其优势是学习目标明确，但前提是每段专家示范都有与机器人控制接口兼容的真实动作标签。
- **视频转换与既有潜在动作学习**：视频转换方法借助手部跟踪、图像修补等技术，把人类示范转换成更接近目标机器人视角和外观的观测；潜在动作方法则从连续观测之间的变化推断隐藏行为，并以这种表示替代缺失的真实动作来标注示范。两类方法分别缓解视觉或表示问题，但仍需解决隐藏行为如何稳定对应连续电机命令的问题。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 标准模仿学习依赖带动作标签的专家机器人示范；即使人类视频已被转换为机器人兼容的画面，转换过程也不会产生真实机器人控制信号，因此这些数据仍不能直接用于常规行为克隆。
- 既有潜在动作范式尚未充分解决高维连续控制中的可执行性：若潜在空间的学习与真实动作映射彼此分离，表示可能有助于重建画面，却不一定能被稳定解码成连续控制命令。其后果是观测层面的变化表示与机器人实际可执行动作之间存在断层。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究之间缺少一个完整接口：它既要在不使用专家动作标签的情况下，从机器人观测序列中学习描述相邻状态变化的动作表示，又要仅依靠少量、无需针对目标任务收集的带动作数据，把该表示约束为能够解码到真实连续控制空间。尤其缺乏对这种方案能否支持高维连续控制并部署到物理机器人的验证。

</div>
<div markdown="1"><span>核心问题</span>

能否通过连续潜在动作和联合动作落地，从无动作标签的专家机器人视频中生成可靠伪动作，再利用少量任务无关玩耍数据把伪动作映射为可执行电机命令，使机器人在未采集任何带动作标签专家示范的前提下学会新任务？

</div>
<div markdown="1"><span>作者直觉</span>

相邻两帧观测之间发生了什么变化，通常隐含着导致该变化的动作。CLAM让逆动力学模型把这种变化压缩为连续潜在动作，再让前向动力学模型检查该潜在动作能否解释下一帧；这形成了无需动作标签的自监督信号。与此同时，少量玩耍数据提供真实动作作为“坐标锚点”，联合训练动作解码器会反过来约束潜在空间，使其中的变化方向不仅能解释视频，还能对应机器人可执行的连续命令。这样，任务知识主要来自廉价的无标签专家视频，而控制接口知识可由跨任务复用的玩耍数据提供。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CLAM把“从无动作标签的专家视频学习控制”拆成两个阶段。第一阶段在大规模无标签观测集$\mathcal{D}_{\mathrm{unlabeled}}$上，通过预测下一帧学习连续潜动作$z_t$：逆动力学模型根据相邻观测推断$z_t$，前向动力学模型再用当前观测与$z_t$重建$o_{t+1}$；同时利用少量带动作的任务无关数据$\mathcal{D}_{\mathrm{labeled}}$，联合训练动作解码器把$z_t$映射为可执行动作$a_t$。第二阶段用已训练的逆动力学模型为无动作标签的任务专家演示$\mathcal{D}_{\mathrm{unlabeled-expert}}$生成潜动作伪标签，再以模仿学习训练策略$\pi_\theta(z_t\mid o_t)$。部署时，策略先从当前观测预测潜动作，动作解码器随后输出机器人命令。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 连续潜动作的自监督学习

逆动力学模型$f_\phi$由上下文与下一观测推断连续潜动作$z_t$，前向动力学模型$g_\psi$根据$o_{t-H},\ldots,o_t$和$z_t$预测$\hat{o}_{t+1}$，并以未来观测重建误差更新二者。编码器—解码器的信息瓶颈限制$z_t$的容量，使其优先记录解释当前转移所需的信息。

<div class="method-step__io" markdown="1">

**输入**：无动作标签的观测轨迹$\mathcal{D}_{\mathrm{unlabeled}}$，其中每条轨迹提供连续观测$o_{t-H},\ldots,o_t,o_{t+1}$。<br>
**输出**：可从观测转移推断低层连续潜动作的逆动力学模型$f_\phi$，以及仅在预训练阶段提供监督信号的前向动力学模型$g_\psi$。

</div>

**直观理解**：模型先猜测“相邻两帧之间发生了什么动作”，再检查这个猜测能否解释下一帧；如果解释不好，就同时修正猜动作和预测未来的两个模型。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 潜动作与真实控制命令联合对齐

用$f_\phi$产生$z_t$，再由不接收观测的动作解码器$p_\omega(a_t\mid z_t)$预测$\hat a_t$；其动作均方误差同时更新$p_\omega$和$f_\phi$。训练过程交替使用无标签批次优化重建项，以及每隔$K$次更新使用带标签批次优化动作解码项。

<div class="method-step__io" markdown="1">

**输入**：少量带标签转移$\mathcal{D}_{\mathrm{labeled}}$，每个样本包含观测转移及真实环境动作$a_t$；该数据可以来自随机策略或任务无关的玩耍行为。<br>
**输出**：与机器人真实动作空间对齐的潜动作表示，以及可将$z_t$转换为可执行动作$a_t$的解码器$p_\omega$。

</div>

**直观理解**：少量带动作数据相当于一本“潜在动作语言到电机命令”的词典；联合更新还会反过来整理这门潜在语言，使相近代码具有稳定、可执行的控制含义。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 专家演示重标注与潜策略学习

对专家轨迹中的每个相邻观测对推断$z_t$，构造重标注数据$\mathcal{D}_{\mathrm{relabeled-expert}}$；随后以均方误差训练潜动作策略$\pi_\theta(z_t\mid o_t)$复现这些伪标签。前向动力学模型$g_\psi$在此阶段被丢弃，而逆动力学模型的图像编码特征可以迁移给策略。

<div class="method-step__io" markdown="1">

**输入**：无动作标签的任务专家演示$\mathcal{D}_{\mathrm{unlabeled-expert}}$和预训练逆动力学模型$f_\phi$。<br>
**输出**：给定当前观测即可预测专家式连续潜动作的策略$\pi_\theta$。

</div>

**直观理解**：系统先给没有动作记录的专家视频自动补上“动作字幕”，再像普通行为克隆一样训练策略模仿这些字幕。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 闭环部署

策略先计算$z_t\sim\pi_\theta(\cdot\mid o_t)$，动作解码器再计算$a_t\sim p_\omega(\cdot\mid z_t)$，并将$a_t$发送给环境；获得新观测后重复该过程直至任务结束。

<div class="method-step__io" markdown="1">

**输入**：环境当前观测$o_t$、训练后的潜动作策略$\pi_\theta$和动作解码器$p_\omega$。<br>
**输出**：机器人可直接执行的连续控制序列$a_1,a_2,\ldots$。

</div>

**直观理解**：运行时形成“看图—决定潜动作—翻译成电机命令—再次观察”的闭环，不需要未来帧或专家动作标签。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### CLAM第一阶段联合目标

$$
\mathcal{L}_{\mathrm{CLAM}}=\mathcal{L}_{\mathrm{recon}}+\beta\mathcal{L}_{\mathrm{action-decoder}}=\operatorname{MSE}(\hat{o}_{t+1},o_{t+1})+\beta\operatorname{MSE}(\hat{a}_t,a_t)
$$

**符号说明**

- $\mathcal{L}_{\mathrm{CLAM}}$：第一阶段用于训练连续潜动作模型与动作解码器的总损失
- $\mathcal{L}_{\mathrm{recon}}$：前向动力学模型的下一观测重建损失
- $\mathcal{L}_{\mathrm{action-decoder}}$：动作解码器预测真实环境动作的监督损失
- $\hat{o}_{t+1}$：前向动力学模型依据观测上下文和潜动作预测的下一观测
- $o_{t+1}$：数据中实际出现的下一观测
- $\hat{a}_t$：动作解码器根据潜动作预测的环境动作
- $a_t$：带标签数据中记录的真实环境动作
- $\beta$：平衡观测重建监督与动作落地监督的超参数
- $\operatorname{MSE}$：均方误差，即预测值与目标值逐维平方差的平均

<div class="equation-explanation" markdown="1">

**直观理解**：第一项要求潜动作足以解释“画面怎样变化”，让模型能从海量无标签视频学习；第二项要求同一潜动作能被翻译成正确的机器人命令。二者联合优化把可预测未来的表示与可执行控制对齐，而$\beta$决定少量动作监督对潜空间施加多强的约束。<br>
**原文位置**：Section IV-A, “Latent Action Decoder”与该节末尾的最终训练目标

</div>

</div>

<div class="equation-block" markdown="1">

#### 潜动作策略模仿目标

$$
\mathcal{L}_{\pi}=\operatorname{MSE}(\hat{z}_t,z_t)
$$

**符号说明**

- $\mathcal{L}_{\pi}$：第二阶段训练潜动作策略的模仿损失
- $\hat{z}_t$：策略根据当前观测$o_t$预测的连续潜动作
- $z_t$：预训练逆动力学模型根据专家观测转移生成的潜动作伪标签
- $\operatorname{MSE}$：预测潜动作与伪标签之间的均方误差

<div class="equation-explanation" markdown="1">

**直观理解**：该目标让策略在只看到当前观测时复现专家轨迹对应的潜动作。它把原本缺少真实动作标签的问题转化为对自动生成的连续伪动作进行行为克隆。<br>
**原文位置**：Section IV-B, “Latent Action Policy Training”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：第一阶段包含两种交替的梯度更新：在$\mathcal{D}_{\mathrm{unlabeled}}$上通过$\mathcal{L}_{\mathrm{recon}}$更新$f_\phi$与$g_\psi$，使$z_t$保留预测下一观测所需的转移信息；每隔$K$步在$\mathcal{D}_{\mathrm{labeled}}$上通过$\mathcal{L}_{\mathrm{action-decoder}}$更新$p_\omega$与$f_\phi$，使潜动作能够对应真实控制。因而所谓联合目标在算法实现上并不要求每个批次同时含有两类数据，而是通过交替采样实现加权联合优化。第二阶段固定预训练的潜动作标注机制，用$f_\phi$生成专家伪标签，并仅以$\mathcal{L}_\pi$训练$\pi_\theta$；$g_\psi$完成提供自监督信号的作用后不参与策略训练或部署。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 连续潜动作模型**

该模块由逆动力学模型$f_\phi(z_t\mid o_{t-H},\ldots,o_t,o_{t+1})$与前向动力学模型$g_\psi(o_{t+1}\mid o_{t-H},\ldots,o_t,z_t)$组成。与采用向量量化得到离散代码的既有方法不同，CLAM直接学习连续$z_t$；额外的$H$步历史用于缓解图像观测无法完整反映环境状态的问题。

> 直观理解：连续机器人控制包含方向、速度和力度等细微变化，有限的离散代码容易把不同动作挤到同一类别；连续潜空间能保留这些渐变。历史帧则帮助模型从运动趋势判断速度或隐藏状态，而不只依赖单张图片。

**2. 无观测条件的动作解码器**

动作解码器建模$p_\omega(a_t\mid z_t)$，只接收潜动作而不接收$o_t$，并在第一阶段与$f_\phi$联合训练。带标签数据只负责把潜动作落地到环境动作，不要求来自目标任务专家。

> 直观理解：禁止解码器查看图像，可以避免它绕过$z_t$、直接从场景猜动作，从而迫使潜代码本身表达低层控制。联合训练比事后单独拟合转换器更能保证潜空间可被真实机器人稳定解码。

**3. 潜动作策略**

策略$\pi_\theta(z_t\mid o_t)$在重标注专家数据上进行模仿学习，学习从单个当前观测预测$f_\phi$生成的专家潜动作。其输出不直接作用于环境，而由$p_\omega$转换为$a_t$。

> 直观理解：该策略学习的是专家“想实施的低层变化”，而不是昂贵的原始动作标签；因此专家只需展示任务过程，少量通用带动作数据便可承担控制接口校准。

**训练与推理**

训练时，先初始化$f_\phi$、$g_\psi$和$p_\omega$。在共$N_C$次第一阶段更新中，每次从$\mathcal{D}_{\mathrm{unlabeled}}$取观测序列，计算$z_t=f_\phi(o_{t-H},\ldots,o_t,o_{t+1})$与$\hat{o}_{t+1}=g_\psi(o_{t-H},\ldots,o_t,z_t)$并优化重建损失；当迭代次数满足间隔$K$时，再从$\mathcal{D}_{\mathrm{labeled}}$取样，经过$f_\phi$和$p_\omega$预测$\hat a_t$并优化动作解码损失。随后用$f_\phi$逐转移标注$\mathcal{D}_{\mathrm{unlabeled-expert}}$，得到包含$o_t$与$z_t$的$\mathcal{D}_{\mathrm{relabeled-expert}}$，再进行$N_P$次更新以训练$\pi_\theta$。推理时不再需要$f_\phi$、$g_\psi$、专家未来观测或任何标签；在每个时间步，$\pi_\theta$由$o_t$预测$z_t$，$p_\omega$将其解码为$a_t$，环境执行动作并返回下一观测。

**复现信息**

公平解释该方法需要注意三项设计。第一，输入可包含额外$H$步历史上下文，这是针对视觉观测部分可观测性的处理，但部署算法中的策略仍按原文写作$\pi_\theta(z_t\mid o_t)$。第二，潜动作采用连续表示，并通过编码器—解码器信息瓶颈抑制直接复制观测等捷径；摘录未给出网络层数、潜空间维度、$H$、$K$或$\beta$的具体取值，原文未明确报告。第三，动作解码器刻意不以观测为条件，且其监督可来自随机策略或任务无关玩耍数据；这一区别决定了方法是否真正依靠$z_t$承载可执行动作信息。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- DMControl：包含Hopper与HalfCheetah两个连续 locomotion 任务。CLAM预训练使用D4RL的medium-expert轨迹；小规模有标签集合$\mathcal{D}_{\mathrm{labeled}}$只从次优轨迹中抽取，用来检验模型能否借助无标签数据弥补动作监督质量不足。该组实验报告归一化回报。
- MetaWorld：包含Assembly、Bin Picking、Peg Insert和Shelf Place四个困难操作任务。作者训练单任务强化学习智能体并收集其回放缓冲区作为预训练数据，另留出random-medium数据构成$\mathcal{D}_{\mathrm{labeled}}$。它同时用于状态输入和图像输入实验，主要检验潜在动作学习在高维连续机械臂控制中的有效性。
- 真实WidowX机械臂：包含Reach Block、Push Button、Close Microwave以及Put Object in Pot and Slide Pot四项任务；最后一项在$5\,\mathrm{Hz}$控制频率下超过150步。任务无关play数据约含5万次转移，其中约5000次转移带动作标签；每项任务另收集约30条没有动作标签的专家示范，用来检验方法能否从少量真实动作监督中完成潜在动作到电机命令的落地。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**DMControl归一化回报**

将策略在Hopper和HalfCheetah中的累计环境回报归一化，用于衡量 locomotion 控制质量；摘录未说明具体归一化公式。 （越高越好，因为更高回报表示策略更有效地完成环境定义的控制目标。）

</div>
<div class="metric-item" markdown="1">

**MetaWorld平均任务成功率**

统计评估回合中完成指定操作任务的比例；图像实验对3个随机种子、每个种子50次评估rollout取平均。 （越高越好，因为它直接表示策略成功完成装配、抓取、插入或放置任务的频率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### DMControl与MetaWorld状态输入的六任务总体比较

<div class="result-value" markdown="1">

Transformer-CLAM在HalfCheetah、Hopper、Assembly、Bin Picking、Peg Insert和Shelf Place上的结果依次为$0.72\pm0.04$、$0.81\pm0.05$、$0.91\pm0.03$、$0.82\pm0.03$、$0.79\pm0.07$和$0.93\pm0.02$，六任务简单平均为$0.83$。它高于最佳非CLAM基线VPT的平均$0.28$，约为后者的$2.96$倍，也高于MLP-CLAM的$0.63$。

</div>

该结果表明，在同一组状态控制任务上，连续潜在动作与Transformer时序建模的组合明显优于小数据行为克隆、监督式动作伪标注和已有潜在动作方法；优势并非仅由某一个任务贡献，因为Transformer-CLAM在六列中都高于非特权基线。不过，表格把DMControl归一化回报与MetaWorld成功率直接做简单平均，这个平均值适合概括相对趋势，却不是具有统一物理含义的跨基准指标。

<div class="result-source" markdown="1">

来源：Table I，列顺序为HalfCheetah、Hopper、Assembly、Bin Picking、Peg Insert、Shelf Place、Average

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Transformer-CLAM∗ | 0.72 ± 0.04 | 0.81 ± 0.05 | 0.91 ± 0.03 | 0.82 ± 0.03 | 0.79 ± 0.07 | 0.93 ± 0.02 | 0.83

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 与使用专家真实动作标签的特权行为克隆比较

<div class="result-value" markdown="1">

Transformer-CLAM的六任务平均值为$0.83$，接近BC-Expert的$0.87$；分任务看，它在HalfCheetah和Hopper上分别以$0.72$和$0.81$超过BC-Expert的$0.68$和$0.76$，在Shelf Place上与BC-Expert同为$0.93$，但在Assembly、Bin Picking和Peg Insert上仍分别落后$0.09$、$0.12$和$0.12$。

</div>

这说明无动作标签专家示范配合少量任务无关动作数据，可以恢复接近全监督专家行为克隆的总体性能，支持CLAM减少专家遥操作标注需求的核心主张。但BC-Expert使用了其他方法不可见的真实专家动作，且两者在部分任务仍有明显差距；个别任务上CLAM超过BC-Expert也不能证明潜在动作监督普遍优于真实动作监督，因为训练数据分布、优化误差和评估方差都可能影响比较。

<div class="result-source" markdown="1">

来源：Table I，列顺序为HalfCheetah、Hopper、Assembly、Bin Picking、Peg Insert、Shelf Place、Average；CLAM数值见同表Transformer-CLAM行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

BC-Expert | 0.68 ± 0.02 | 0.76 ± 0.04 | 1.00 ± 0.00 | 0.94 ± 0.05 | 0.91 ± 0.03 | 0.93 ± 0.00 | 0.87

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### MetaWorld图像输入、统一使用100条动作标注轨迹

<div class="result-value" markdown="1">

在所有方法使用相同数量的100条动作标注轨迹时，MLP-CLAM与Transformer-CLAM相对最佳基线最高可取得$3\times$的任务成功率提升。

</div>

该实验测试高维视觉输入下的核心难点：少量带动作数据并非纯专家数据时，直接行为克隆或仅靠监督逆动力学补标签会受到明显限制，而CLAM可利用无标签序列学习动作相关的动态变化。这里的“最高$3\times$”是某些任务上的相对提升，不代表所有任务、所有随机种子或绝对成功率都提升三倍；摘录也未给出Figure 2各任务的完整数值。

<div class="result-source" markdown="1">

来源：Figure 2说明，MetaWorld Image-Based Experiments

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Because 𝒟 labeled is not solely expert data, baselines struggle to learn a performant downstream policy, whereas MLP-CLAM and Transformer-CLAM achieve up to a 3 × improvement over the best baseline.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验摘录没有包含真实WidowX任务的定量结果，也没有给出Figure 2的逐任务数值，因而无法独立核验论文摘要中“跨真实机器人任务提升$2$至$3$倍”的范围、统计显著性和具体失败情形。
- 摘录未提供专门的组件消融表，无法严格隔离连续相对离散潜在空间、联合训练相对分阶段训练、不同潜在维度或动作标注规模各自的因果贡献。MLP-CLAM与Transformer-CLAM的差异同时改变模型参数化和时序建模能力，只能视为架构比较，不能替代完整消融。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- BC-AL：只在小规模、并非完全由专家构成的$\mathcal{D}_{\mathrm{labeled}}$上进行行为克隆。它直接衡量仅依赖现有动作标签、不利用无标签数据时能够达到的水平。
- VPT：只用$\mathcal{D}_{\mathrm{labeled}}$监督训练逆动力学模型，再为无动作标签的专家示范预测环境动作，最后在伪标注数据上训练行为克隆策略。它是与CLAM最直接的“先补动作标签、再克隆”比较，但其动作推断器没有从大规模无标签数据中学习动力学。
- LAPO与LAPA：LAPO采用向量量化的离散潜在动作；LAPA在潜在动作模型预训练后，把逆动力学模型末层替换为动作头，并在非专家$\mathcal{D}_{\mathrm{labeled}}$上端到端微调。二者用于比较离散潜在动作及传统分阶段动作落地方案与CLAM连续潜在动作方案的差异。
- BC-Expert：在无标签专家示范对应的真实专家动作上训练的特权行为克隆参考。其他方法不能访问这些动作标签，因此它不是公平的数据条件基线，而是用于估计“若昂贵的专家动作标签可用”时的性能上界。

**实验想回答的问题**

- 在专家示范只有观测、没有动作标签，而动作标签仅来自少量任务无关或次优数据的条件下，CLAM能否比行为克隆、动作伪标注、离散潜在动作和纯表征预训练方法学到更有效的连续控制策略？
- 连续潜在动作方法能否跨越状态输入、图像输入、模拟 locomotion、模拟机械臂操作和真实机器人长时程任务，并接近使用专家真实动作标签训练的特权上界$BC\text{-}Expert$？

**实验实现**

作者尽量在CLAM与各基线之间复用相同的逆动力学模型、前向动力学模型、动作解码器或动作头，以及Transformer行为克隆策略，并在算法适用时提供相同数据。图像实验统一使用100条带动作轨迹，以减少监督量差异造成的混淆。图像CLAM把$64\times64\times3$图像切成边长16的patch，共16个patch，并以Space-Time注意力处理空间与时间信息；潜在策略使用预训练ResNet18产生$7\times7$、通道维度为$d_v=512$的视觉token，再由因果Transformer通过交叉注意力预测动作。策略每个时刻输出5个动作组成的chunk，对应1秒执行。所有直接预测环境动作的方法均使用各基准原生的连续动作空间。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 真实WidowX实验覆盖触达、按钮按压、关微波炉以及“把物体放入锅中并滑动锅”的长时程任务，最后一项超过150个控制步，说明评估并不限于短时单动作技能。然而所给摘录只描述任务与数据规模，没有提供每项真实任务的成功率、失败模式或与基线的定量差异，因此不能据此判断真实部署提升幅度。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops latent-action learning for robot control from observation-only demonstrations and limited action-labeled play data.; rule check: matched taxonomy keywords; top rule score=5.0
- 全文指纹：`e6ca0da979464ef4d47ac3e8722f4fcd7f0d96f87fd0140f70ea04abd7277fca`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
