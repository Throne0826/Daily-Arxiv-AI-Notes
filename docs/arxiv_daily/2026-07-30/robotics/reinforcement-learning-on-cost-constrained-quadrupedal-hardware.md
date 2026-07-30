---
title: "[论文解读] Reinforcement Learning on Cost-Constrained Quadrupedal Hardware"
description: "[arXiv 2607.26434][机器人 / 具身智能] 本文研究低成本四足机器人因执行器通信延迟、反馈缺失与噪声而产生的仿真到现实鸿沟，并比较手工延迟补偿与时间感知神经网络两条解决路径。"
arxiv_id: "2607.26434"
announcement_date: "2026-07-30"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:25.672220+00:00"
source_sha256: "f9e63aa03f2c82d9fa73eeeb40b05835409b91d4f4d08f2d74f1cc388a59a982"
tags:
  - "机器人 / 具身智能"
  - "强化学习"
  - "低成本四足机器人"
  - "强化学习控制"
  - "仿真到现实迁移"
  - "执行器延迟"
  - "部分可观测马尔可夫决策过程"
  - "时间感知网络"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2607.26434</p>

# Reinforcement Learning on Cost-Constrained Quadrupedal Hardware

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Javier C. Weddington, Bence P. Ölveczky, Stephen A. Baccus</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26434v1) · [PDF 下载](https://arxiv.org/pdf/2607.26434v1) · **关键词** 低成本四足机器人, 强化学习控制, 仿真到现实迁移, 执行器延迟, 部分可观测马尔可夫决策过程, 时间感知网络  


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

本文研究低成本四足机器人因执行器通信延迟、反馈缺失与噪声而产生的仿真到现实鸿沟，并比较手工延迟补偿与时间感知神经网络两条解决路径。

**不用术语来说**：低价四足机器人的电机收到指令后不会立即动作，而且控制器通常只能读到不够准确的关节位置，无法直接获得速度和力矩；因此，机器人根据旧信息作出的纠正动作到达电机时，身体状态可能已经改变，使仿真中学会的步态在真机上失效。本文要判断：应当为普通策略人工搭建复杂的补偿环节，还是让带记忆的网络自己学习这些延迟规律。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将低成本四足机器人的极端执行延迟明确建模为部分可观测决策问题，并把研究焦点从一般的模型误差转向通信延迟、缺失状态与随机反馈共同造成的部署困难。
- 作者在相同训练条件与校准后的延迟执行器模型下比较前馈网络和多种时间感知网络，以检验网络内部记忆能否替代手工构造的观测与控制补偿；其进一步关注时间感知策略是否会形成类似中央模式发生器的自主节律。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究低成本四足机器人上的强化学习步态控制及其仿真到现实迁移。高端平台通常采用低延迟、高频率且可反馈位置、速度或力矩的准直驱/弹性执行器；相比之下，Mini Pupper 2 使用廉价有刷直流位置舵机，仅提供位置反馈，并经 ESP32 串行链路产生实测 76 ms 传输延迟，3 Hz 以上的跟踪能力还会明显下降。动作延迟、反馈噪声和状态缺失使控制器看到的信息不能完整代表机器人当前状态，因此标准马尔可夫决策过程假设不再成立，需要按部分可观测控制问题理解。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**仿真到现实迁移（sim-to-real transfer）**

先在仿真器中训练控制策略，再部署到真实机器人。若仿真没有准确覆盖真实执行器的延迟、噪声和响应带宽，策略在仿真中学到的动作时序可能在硬件上失效。

</div>
<div class="conceptitem" markdown="1">

**部分可观测马尔可夫决策过程（POMDP）**

控制器不能直接获得决定未来演化所需的完整当前状态，只能依据不完整或滞后的观测选择动作。本文中，缺少速度与力矩反馈、位置量化以及随机执行延迟共同造成部分可观测性。

</div>
<div class="conceptitem" markdown="1">

**时间感知网络（time-aware network）**

能够利用跨时间信息形成内部记忆或动态状态的策略网络，而不是仅根据当前一帧观测独立决策。它可能在内部推断尚未执行的历史命令及缺失状态，从而适应变化的延迟。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是约 300 美元的 Mini Pupper 2 四足机器人，其位置舵机存在实测 76 ms 传输延迟，只返回带噪、量化的位置，而不提供速度和力矩。策略在每个时刻接收不完整且可能过时的机器人观测，并输出关节位置命令；命令经过约 k 个控制步后才作用于执行器。论文要判断这种低成本硬件的 sim-to-real 瓶颈应主要通过哪类方案解决：为简单前馈策略构造合成比例—微分反馈等模型化“观测桥”，还是使用时间感知网络，在内部学习延迟与缺失状态的动态规律。若延迟固定且完整状态可见，可将尚未执行的历史动作并入状态以恢复马尔可夫性；但本文硬件同时具有随机延迟和不完整反馈，因而被建模为带随机动作缓冲区的 POMDP。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$s_t$**

时刻 t 的系统状态；在真实低成本硬件上，该状态不能被策略完整观测。

</div>
<div class="notationitem" markdown="1">

**$a_t$**

策略在时刻 t 发出的动作，即关节位置命令；若延迟为 k 个时间步，该动作到 t+k 才生效。

</div>
<div class="notationitem" markdown="1">

**$k$**

动作从发出到实际生效所经历的时间步数；真实系统中可能随机变化。

</div>
<div class="notationitem" markdown="1">

**$\tilde{s}_t=(s_t,a_{t-1},a_{t-2},\ldots,a_{t-k})$**

固定延迟条件下的增广状态，由当前状态和此前已发出但可能尚未执行的动作缓冲区组成，用于恢复马尔可夫性（第 I-A 节，式（1））。

</div>

</div>

**直接相关的工作**

- **显式执行器延迟建模方法 [18]**: 已有研究指出显式建模执行器延迟是 sim-to-real 迁移所必需的，但主要面向高频、低延迟的无刷执行器系统，不能直接回答超过 50 ms 延迟且反馈缺失时应如何选择策略架构。
- **基于动作历史或扰动感知表示的延迟强化学习方法 [20]**: 这类方法通过历史动作或延迟相关表示缓解部分可观测性，与本文的问题形式直接相关；本文进一步比较神经网络架构自身处理极端硬件延迟的能力与手工部署补偿是否足够。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

高性能四足平台通常依靠低延迟、高控制频率且可反馈位置、速度和力矩的昂贵执行器，而 Mini Pupper 2 一类低成本平台采用有刷位置舵机，论文测得其通信传输延迟为 76 ms，并且只有位置反馈。长延迟使传感信息到达控制器时已经过时，控制命令到达关节时也可能不再适合当前姿态，普通闭环纠错因而失效；这既阻碍强化学习策略从仿真迁移到真机，也提高了低成本机器人部署所需的人工调试负担。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **模型化延迟与手工观测桥接**：在训练环境中显式加入平均执行器延迟，并在部署时为简单的前馈策略构造合成比例—微分反馈等补偿模块，用估计的状态变化弥补真机缺少速度、力矩反馈的问题。其基本思路是由工程人员在网络外部恢复一个更接近训练条件的观测与控制回路。
- **基于历史信息的时间感知策略**：使用动作历史、扰动感知表示或循环神经网络，让策略根据一段时间内的观测和动作推断当前隐含状态。对于延迟为若干控制步的系统，过去已经发出但尚未执行的动作也属于有效状态；带记忆的网络可在内部追踪这些信息，而不只依赖当前时刻的观测。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有显式延迟建模工作主要面向高频无刷执行器，其最大延迟往往不超过一个控制周期，不能直接说明在超过 50 ms、反馈不完整且延迟具有随机性的低成本硬件上何种方案仍然有效。
- 前馈策略依赖手工设计的部署补偿，可能需要较多参数和逐机调试；但采用更复杂的循环或注意力架构也会增加训练与部署成本，而且此前尚不清楚不同时间感知架构是否真的能够内化延迟动力学，而非仍需外部工程补偿。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究没有在统一训练条件下系统回答：当仿真到现实差距主要由极端通信延迟和缺失状态而非精细动力学误差主导时，不同神经网络架构本身管理部分可观测性的能力如何，以及这种内部时间建模能否实质性减少低成本真机部署所需的手工补偿。

</div>
<div markdown="1"><span>核心问题</span>

对于成本受限的四足硬件，解决仿真到现实瓶颈更应依靠哪条路径：为简单前馈策略构建合成 PD 反馈等模型化观测桥，还是训练能够在内部学习执行延迟与缺失状态动力学的时间感知网络？

</div>
<div markdown="1"><span>作者直觉</span>

延迟使“当前观测”不足以判断机器人真正处于什么状态，因为近期命令中有些仍在传输或尚未完全执行。带有持续记忆通路的网络可以把过去的观测和动作压缩成内部时间状态，进而预测身体节律并提前发出协调命令；如果网络进一步形成自维持的周期性步态，它就不必等待每次迟到且嘈杂的反馈再纠错，因而可能像生物中央模式发生器一样，以自主节律抵抗长延迟。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把低成本四足机器人上的控制视为部分可观测决策问题：舵机存在约 76 ms 的传输与到位延迟，且硬件只能可靠提供少量惯性测量，关节速度和力矩反馈近似为零或噪声很大。作者先在 Isaac Lab 中显式模拟延迟舵机，用 PPO 端到端训练时间感知的 LSTM 策略；部署时再用按关节学习的无状态 MLP 舵机模型，根据动作预测关节位置，并将预测值作为策略的合成反馈。最终形成两层控制器：LSTM 负责较长时间尺度的延迟补偿、步态节律和方向控制，舵机 MLP 负责较短时间尺度的执行器状态预测。

直观地说，策略不再等待廉价舵机返回迟到且不可信的反馈，而是依靠内部记忆持续产生稳定步态，并用一个小型预测器估计“各关节此刻大概走到了哪里”。这种分工使上层控制器可以维持节奏，下层预测器则修正仿真舵机模型与真实舵机之间的差异；作者认为 LSTM 在训练约束下自发形成了类似生物中央模式发生器（CPG）的稳定周期动力学，但这一点属于对隐藏状态、动作轨迹和开环行为的实验性解释，而非预先写入网络的振荡器结构。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 建立延迟执行器仿真与部分观测任务

在 Isaac Lab 中使用校准的延迟 PD 执行器，将传输延迟设为 500 Hz 物理仿真下的 33–43 个步，并构造 60 维观测：机体线速度、角速度、投影重力、速度指令、12 个关节的位置、速度、力矩和上一动作。策略输出 12 维关节目标动作，动作缩放系数为 0.5。

<div class="method-step__io" markdown="1">

**输入**：Mini Pupper 2 的舵机延迟和幅值测量，以及速度指令、机体状态、关节状态和上一时刻动作。  
**输出**：包含真实平台主要延迟与执行器限制的并行四足运动训练环境。

</div>

**直观理解**：这里先让仿真机器人经历与廉价硬件相近的“命令发出后很久才执行”问题，使策略不能依赖即时反馈。60 维观测相当于把机器人自身状态、用户指令和近期控制命令统一交给控制器。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 用 PPO 训练时间感知运动策略

使用 PPO 优化策略和价值网络；时间架构先把观测映射为 128 维时序表征，再接入共享规格的 actor/critic MLP。作者在相同环境和奖励条件下比较 MLP、LSTM、GRU 与 Transformer，其中 LSTM 无需课程学习即可收敛，而 MLP 需要逐步增加延迟、惩罚权重和动作尺度的多阶段课程。

<div class="method-step__io" markdown="1">

**输入**：延迟环境产生的 60 维观测、速度命令、奖励与终止信号。  
**输出**：将当前观测及内部时序状态映射为 12 维关节目标的 LSTM 策略，以及用于对照的其他架构策略。

</div>

**直观理解**：PPO通过反复试走和奖励更新网络；LSTM 的记忆让它能够保存此前动作和状态，从而推断当前反馈对应的是哪个较早时刻。与只看当前输入的 MLP 相比，它更容易在反馈延迟时保持连续节奏。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 学习每个关节的短时舵机预测器

为每个关节训练独立的无状态 MLP，用动作命令预测实际舵机位置，以替代训练时使用但与硬件偏差较大的解析 PD 模型。预测器不保留跨时刻隐藏状态，从而避免一次预测误差在自回归反馈环中持续累积。

<div class="method-step__io" markdown="1">

**输入**：真实机器人进行 3 轮开环动作回放所得数据，每个关节 390 个样本，以及策略发出的舵机命令。  
**输出**：可在部署阶段生成平滑合成关节位置的逐关节舵机模型。

</div>

**直观理解**：同一型号的廉价舵机也可能因关节和运动阶段不同而反应不一，因此不能只用一套固定物理参数。小 MLP 像是每个关节各自的“到位估计器”，而无记忆设计可防止估错一次后越错越远。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 两层控制器开环部署

LSTM 策略在硬件上以 25 Hz 运行，不采用真实编码器闭环反馈；60 维输入中仅 6 维来自真实 IMU，关节力矩和机体线速度置零，关节相关通道主要由舵机 MLP 补全。策略动作经过 8 Hz Butterworth 低通滤波和约 0.60–0.75 的硬件缩放后发送给舵机。

<div class="method-step__io" markdown="1">

**输入**：25 Hz 下的速度命令、IMU 角速度与投影重力，以及舵机 MLP 根据策略动作生成的合成关节位置。  
**输出**：可执行前进、后退、横移和偏航命令的真实四足步态，以及持续更新的预测关节状态。

</div>

**直观理解**：上层 LSTM 像掌握整体节拍的步态中枢，下层 MLP 像预测舵机实际动作的快速观察器。降低控制频率并平滑命令，是为了给慢速舵机足够时间接近目标，避免新命令不断覆盖尚未完成的旧命令。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### PD 执行器力矩

$$
\tau = K_p\left(q_{\mathrm{target}}-q\right)-K_d\dot{q}
$$

**符号说明**

- $\tau$：施加到关节上的控制力矩。
- $K_p$：比例增益，决定目标位置误差产生多大的恢复力矩；训练配置中取 70。
- $q_{\mathrm{target}}$：策略动作指定的目标关节位置。
- $q$：当前或模型预测的关节位置。
- $K_d$：微分或阻尼增益，用于抑制过快运动和振荡；训练配置中取 1.2。
- $\dot{q}$：关节角速度。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项根据目标位置与当前位置之差推动关节到位，第二项根据速度提供阻尼。该式既说明训练中的解析执行器如何把位置命令变成力矩，也说明传统 MLP 部署方案为何需要合成位置、速度和力矩；不过真实舵机的响应随关节和步态阶段变化，因此最终 LSTM 部署改用学习到的逐关节 MLP预测位置。  
**原文位置**：Section II-C Deployment，第 2 项“PD dynamics are simulated”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：策略采用 rsl_rl 的 PPO 实现，直接最大化由标准运动任务奖励塑造的期望累计回报；原文没有给出完整 PPO 损失方程，因此不应据此重构或发明目标公式。奖励重点包括线速度和角速度命令跟踪，并对足端滑移、偏离关节位置、关节力矩、动作不平滑和机体姿态偏差施加惩罚；跟踪标准差设为 \(\sigma_{\mathrm{lin}}=0.1\) 和 \(\sigma_{\mathrm{ang}}=0.2\)。CPG、正弦波形或极限环均未作为显式奖励或结构约束，而是 LSTM 在延迟和不可靠反馈条件下优化运动回报后出现的策略动力学。逐关节舵机 MLP 的具体监督损失函数在所给章节中原文未明确报告，只说明其利用开环回放数据学习动作到舵机位置的预测关系。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 时间感知 LSTM 策略**

LSTM 时序模块把观测编码为 128 维表示，再输入 actor 的 [512, 256, 128] ELU MLP 产生动作；critic 使用同规格 [512, 256, 128] MLP。其 cell state 提供较直接的跨时间信息通路，作者将其解释为适合保存固定延迟所需历史信息的“移位寄存器式”归纳偏置，并在训练后观察到稳定极限环和自主节律。

> 直观理解：延迟意味着当前看到的关节状态可能对应过去的命令，控制器必须记住历史才能正确配对。LSTM 不仅完成这种延迟补偿，还学会在反馈不足时依靠内部状态维持周期步态；CPG 是训练后涌现的行为，而不是人工规定的正弦振荡。

**2. 校准的延迟 PD 执行器仿真**

训练环境使用 DelayedPDActuatorCfg：比例增益 70、微分增益 1.2、摩擦 0.03、armature 0.005、力矩上限 5.0 Nm、仿真速度上限 10.5 rad/s，并加入 33–43 个 500 Hz 物理步的传输延迟。该模块在策略学习阶段近似真实舵机的延迟、幅值和动力学约束。

> 直观理解：如果训练中的关节能瞬间响应，而真实舵机需要几十毫秒，策略到硬件上就会失效。延迟执行器模型故意让仿真也变慢，使策略在训练时学会提前量和节奏控制。

**3. 逐关节无状态 MLP 舵机模型**

部署端为每个关节分别训练 MLP，以策略命令预测关节位置并填充合成观测；原文报告其将关节预测误差由解析 PD 仿真的 0.1–1.8 rad 降至 0.003–0.03 rad。作者选择无状态模型而非舵机 LSTM，是因为每关节仅 390 个训练样本时，循环模型容易过拟合并产生隐藏状态漂移，且其误差会通过策略—预测器反馈环继续放大。

> 直观理解：长期运动规律交给数据充足的策略 LSTM，而少量硬件数据只用于学习“命令到位置”的局部映射。短时预测器每一步重新计算，不把上一步的错误记入内部记忆，因此更适合当前的小数据部署条件。

**训练与推理**

训练阶段在单张 RTX 4090 上运行 4098 个并行环境。每个策略更新由每环境 24 个仿真步组成，PPO 每次更新执行 5 个学习 epoch；折扣因子为 0.99，GAE 参数为 0.95，裁剪比为 0.2，熵系数为 0.005，目标 KL 为 0.01，自适应学习率初值为 1×10^-3。所有候选架构使用相同奖励和环境先直接训练：LSTM 得到稳定步态，MLP 只有在逐步增加延迟、惩罚权重和动作尺度的课程下才达到多方向命令跟踪，GRU 与 Transformer 在训练预算内未收敛。这里的比较用于隔离时序架构归纳偏置，而不是通过不同超参数为某一模型提供额外优势。

部署阶段先采集少量真实舵机开环回放数据，训练每个关节的无状态 MLP 位置预测器；随后以 25 Hz 循环运行 LSTM。每一步将真实 IMU 的角速度和投影重力、运动命令、上一动作及舵机 MLP 生成的合成关节信息组装为策略观测，速度与力矩等不可信通道按文中设置置零；LSTM 更新隐藏状态并输出 12 个关节目标，动作经 8 Hz 低通滤波和硬件比例缩放后发送给舵机，同时作为下一步舵机预测和策略历史输入。所谓“开环”主要指不依赖真实关节编码器闭环确认，并不表示完全没有传感器输入，因为 IMU 仍用于平衡和地形姿态调制。

**复现信息**

公平复现最关键的是同时匹配延迟、控制频率、观测可用性和两层模型的时间尺度。训练物理频率为 500 Hz，延迟为 33–43 个物理步；原文在 Section II-C 的传统 MLP 部署描述中又提到仿真策略为 50 Hz、每策略步含 4 个子步，而硬件部署为 25 Hz，因此实现时应明确区分训练策略频率、物理子步和硬件命令频率，不能把它们视为同一参数。60 维观测由机体线速度 3、角速度 3、投影重力 3、速度命令 3、关节位置 12、关节速度 12、关节力矩 12、上一动作 12 组成；真实 LSTM 部署仅有 6 维直接来自 IMU，其余关节信息依靠模型生成或置零。

动作输出需使用 8 Hz Butterworth 低通滤波，并根据硬件使用约 0.60–0.75 的命令增益；Section II-C 前文称实践中硬件 scale 设为 0.75，后文给出部署范围 0.60–0.75，两者应按具体实验条件核对。逐关节舵机 MLP 使用 3 轮开环回放、每关节 390 个样本；其网络层数、宽度、激活函数、训练损失和优化器在所给原文中未明确报告。作者还描述了传统 MLP 策略的替代部署方案：25 Hz 下设置 5 步、即 200 ms 的动作延迟缓冲，并用解析 PD 动力学重建关节状态；该方案需要至少 6 个手调参数，而最终推荐的 LSTM–MLP 两层方案主要调节硬件缩放系数。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- 强化学习仿真环境：用于以 PPO 端到端训练四足运动策略，并评估额外观测延迟、关节状态噪声以及分布外山坡和凹地地形。原文节选未明确报告环境数量、训练步数及训练/测试划分。
- Mini Pupper 2 真实硬件评测：用于验证开环策略的步态、方向服从性和执行器噪声条件下的 sim-to-real 迁移。评测覆盖前进、后退、横移和偏航指令，但原文未明确报告重复试验次数、路线长度或成功率统计。
- 真实伺服器开环回放数据：每个关节由 3 轮回放、390 个样本组成，用于训练按关节的 MLP 伺服预测器；原文未明确报告训练集与测试集的具体划分。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**单频正弦拟合决定系数 R²**

衡量 12 个关节动作能被单一周期正弦波解释的程度，用来判断步态是否呈现规则、自持的节律结构；R² 越接近 1，单频振荡解释的波形方差越多。 （更高通常表示更规则的周期节律，但不能单独证明该节律由内部 CPG 产生，也不等同于更高的行走成功率。）

</div>
<div class="metricitem" markdown="1">

**延迟扰动下的动作振幅、频率与抖动**

在训练基线延迟之上继续注入观测延迟，检查关节命令是否仍保持原有振幅、稳定频率和光滑波形；振幅塌缩或频率漂移意味着策略过度依赖过时反馈。 （振幅和频率越接近无额外延迟条件、抖动越低越好；振幅本身并非越大越好。）

</div>
<div class="metricitem" markdown="1">

**相对完整观测步态的相关系数**

比较加入关节状态高斯噪声或完全清零关节状态后，所得步态与完整观测基准步态的一致程度，用于确定噪声反馈何时比不使用反馈更有害。 （相关系数越高，说明步态波形越接近完整观测基准；它衡量波形保持程度，不直接衡量位移速度、能耗或跌倒率。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### LSTM 在仿真和真实 Mini Pupper 2 上的自主节律与 CPG 结构

<div class="result-value" markdown="1">

12 个关节的单频正弦拟合平均 R² 在仿真中为 0.40、硬件上为 0.77；真实硬件关节振荡约为 2.8 Hz。作者据此结合隐藏状态极限环、去反馈后节律持续以及 IMU 调制现象，将该策略解释为端到端学习出的 CPG。

</div>

硬件上的动作比仿真动作更接近规则单频振荡，可能因为低通滤波、较低控制频率和开环部署滤除了高频修正。该结果支持“策略内部形成稳定节律”的解释，但 R² 较高本身不能证明生物学机制等价；CPG 判断还依赖隐藏状态极限环和反馈独立性等诊断。

<div class="result-source" markdown="1">

来源：Section III-A, Figure 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Sinusoidal fit (R² to a single-frequency sine) across all 12 joints yields mean R² = 0.40 in simulation (complex multi-frequency waveform with corrections, foot placement, contact responses) and mean R² = 0.77 on hardware. The Butterworth low-pass filter, 25 Hz control rate, and open-loop deployment removes the high-frequency corrective behaviors; and the CPG oscillation remained robust at 2.8 Hz, uniform across all joints.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 在训练时 76 ms 基线延迟之外加入最高 320 ms 观测延迟，对比 LSTM 与 MLP

<div class="result-value" markdown="1">

在额外 320 ms 延迟下，LSTM 的动作振幅仍为 0.49，而 MLP 降至 0.16；PCA 中 LSTM 的椭圆动作轨道在各延迟条件下保持，MLP 轨道则塌缩为近似水平带。

</div>

LSTM 即使收到严重滞后的关节信息，仍可依靠内部循环状态维持周期动作；MLP 更像由当前输入驱动，延迟增大后失去振荡结构。这证明了所测条件下的延迟鲁棒性差异，但没有给出跌倒率、移动距离或统计置信区间，因此不能据此量化完整任务成功率。

<div class="result-source" markdown="1">

来源：Figure 6; Section III-B

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">LSTM (solid) maintains amplitude and waveform across all conditions (amp = 0.49 at +320 ms). MLP (dashed) amplitude collapses to 0.16 at +320 ms.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 同一 LSTM 策略从仿真直接部署到真实 Mini Pupper 2

<div class="result-value" markdown="1">

策略仅以硬件尺度或命令增益作为调节参数，即在仿真和真实机器人上完成前进、后退、横移和偏航方向的服从性运动；真实部署采用 0.60–0.75 的单一命令增益和 8 Hz 动作低通滤波。

</div>

结果说明该策略能够在低成本硬件上产生与指令方向一致的运动，而不需要显式运动学规则。它不是严格的轨迹跟踪或导航成功率证明：原文只报告方向服从性，并指出前进时因髋部不对称和陀螺仪噪声存在轻微顺时针弧线。

<div class="result-source" markdown="1">

来源：Section III-C, Figure 7(b)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">The LSTM policy deployed open-loop with a single command gain of 0.60–0.75 with a Butterworth low-pass filter at 8 Hz on action output. Directional compliance was confirmed in all commanded directions (forward, backward, strafe, yaw) in both simulation and on the real Mini Pupper 2.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验主要报告波形、相关性、PCA 轨道和方向服从性，未明确提供硬件跌倒率、行走速度、能耗、跟踪误差、重复次数、置信区间或显著性检验，因此难以判断鲁棒性增益在完整任务层面的大小和可重复性。
- 硬件结论来自单一低成本平台 Mini Pupper 2，且部署仍使用命令增益、低通滤波和按关节伺服预测器；GRU、Transformer 及四种策略的完整定量对比在所给节选中缺失，CPG 与跨平台泛化结论仍需更多机器人、负载和地形验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- MLP 策略：无循环记忆，主要依赖当前观测，是检验时间记忆和自主振荡是否必要的核心对照。
- GRU 策略：具有门控循环状态，用于比较不同循环架构的训练、部署和延迟鲁棒性；但所给结果节选未提供其定量成绩。
- Transformer 策略：用注意力处理时间信息，是另一种时间感知架构对照；但所给结果节选未提供其定量成绩。
- 解析 PD 伺服仿真与循环 LSTM 伺服模型：前者检验简单动力学模型是否足以模拟真实舵机，后者与无状态 MLP 伺服预测器比较自回归误差累积风险。

**实验想回答的问题**

- 在低成本四足机器人存在显著执行器传输延迟与噪声反馈时，LSTM、MLP、GRU 和 Transformer 中哪类策略能够训练收敛、部署到真实硬件，并在额外观测延迟下保持稳定步态？
- LSTM 的鲁棒性是否来自自主生成的中央模式发生器（CPG）式极限环，而非依赖实时关节反馈；按关节学习的无状态伺服预测模型能否进一步缩小仿真与真实执行器之间的差异？

**实验实现**

作者沿三条轴线比较 MLP、LSTM、GRU 和 Transformer：训练收敛及课程需求、真实硬件部署复杂度、延迟扰动鲁棒性。核心诊断在策略自身训练环境中开环执行，并仅对关节状态通道（索引 12–48）注入额外延迟或高斯噪声。极限环分析将 LSTM 的 128 维内部状态及 12 维动作联合投影到 PCA 空间，以相同主轴比较不同延迟条件。真实部署以 25 Hz 控制，动作输出经过 8 Hz Butterworth 低通滤波，并将速度和力矩反馈清零；LSTM 使用同一训练网络，仅调节 0.60–0.75 的命令增益。另以每关节 390 个开环回放样本训练无状态 MLP 伺服预测器，为策略生成预计关节观测。节选没有提供随机种子、置信区间、显著性检验、硬件试验重复次数或统一任务成功率。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 向关节状态观测加入递增高斯噪声，并与完全清零关节状态通道比较 | LSTM 与 MLP 均在噪声标准差约 0.2 rad 处出现交叉：超过该水平时，完全不使用关节状态比使用噪声关节状态更能保持步态。清零关节状态时，LSTM 与完整观测基准的步态相关系数为 0.826，MLP 为 0.698；实测位置噪声为 0.101 rad，而由 25 Hz 有限差分得到的速度噪声为 3.17 rad/s。 | 该消融隔离了实时本体感觉的价值：适度准确的位置反馈仍有帮助，但严重污染的速度反馈会破坏控制回路。LSTM 在清零后仍保持较高相关性，支持其节律主要由内部状态产生；不过位置噪声和速度噪声量纲不同，约 0.2 rad 的交叉点不能直接作为速度通道的同量纲阈值。 | Figure 7(a); Section III-C<br><span class="experiment-evidence">Both LSTM (corr = 0.826 when zeroed) and MLP (corr = 0.698) cross over at σ ≈ 0.2 rad: noise beyond this level degrades the gait more than having no joint state at all. Measured hardware noise levels (position σ = 0.101 rad, velocity σ = 3.17 rad/s from finite differencing at 25 Hz) are shown as vertical bands.</span> |
| 以按关节无状态 MLP 伺服预测器替换解析 PD 伺服仿真 | 使用每关节 3 轮、390 个开环回放样本训练后，关节预测误差由解析 PD 仿真的 0.1–1.8 rad 降至 0.003–0.03 rad。 | 该比较隔离了真实舵机动力学建模的作用：单一解析 PD 模型无法表达不同关节和步态阶段的响应差异，而小型按关节 MLP 能明显改善下一步关节位置预测。误差下降支持它作为策略观测生成器的用途，但节选未说明误差统计方式、独立测试划分或置信区间，因而不能排除对有限回放轨迹的过拟合。 | Section III-C<br><span class="experiment-evidence">A learned per-joint MLP servo model, trained on 3 loops of open-loop playback data (390 samples per joint), replaced the analytic PD simulation for observation generation. The learned servo model reduced the joint prediction error from 0.1–1.8 rad (PD sim) to 0.003–0.03 rad, allowing the individual hardware servo position to have smooth and sustainable locomotion sequences.</span> |

**定性案例**

- 分布外地形测试中，仿真 LSTM 无需重新训练即可在山坡和凹地上调节同一基础节律；作者解释为 IMU 重力向量随坡度旋转，从而调制内部 CPG。该案例说明节律可接受姿态输入进行连续调节，但节选没有给出坡度范围、成功率或与基线的定量比较。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work develops reinforcement-learned quadruped locomotion with delay-aware modeling for robust sim-to-real deployment on low-cost hardware.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`f9e63aa03f2c82d9fa73eeeb40b05835409b91d4f4d08f2d74f1cc388a59a982`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
