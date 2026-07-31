---
title: "[论文解读] REFINE-DP: Diffusion Policy Fine-tuning for Humanoid Loco-manipulation via Reinforcement Learning"
description: "[arXiv 2603.13707][机器人 / 具身智能] REFINE-DP通过强化学习联合微调扩散策略运动规划器与人形机器人全身控制器，使二者在交互中共同适应，从而缓解离线模仿学习的分布偏移和规划—控制失配。"
arxiv_id: "2603.13707"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.250436+00:00"
source_sha256: "cd5473701090856875ba84f9e6f513509832804f056e5a21bb2ecf6aeba7bf0e"
tags:
  - "机器人 / 具身智能"
  - "强化学习"
  - "人形机器人"
  - "移动操作"
  - "扩散策略"
  - "强化学习微调"
  - "分层规划与控制"
  - "模仿学习"
  - "仿真到现实"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2603.13707</p>

# REFINE-DP: Diffusion Policy Fine-tuning for Humanoid Loco-manipulation via Reinforcement Learning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Gu, Zhaoyuan, Chen, Yipu, Chai, Zimeng, Cueva, Alfred, Nguyen, Thong, Wu, Yifan, Xue, Huishu, Kim, Minji, Legene, Isaac, Liu, Fukang, Kim, KyoungMok, Barula, Ayan, Chen, Yongxin, Zhao, Ye</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2603.13707) · [PDF 下载](https://arxiv.org/pdf/2603.13707) · **关键词** 人形机器人, 移动操作, 扩散策略, 强化学习微调, 分层规划与控制, 模仿学习, 仿真到现实<br>
**项目页**: [https://refine-dp.github.io/REFINE-DP/](https://refine-dp.github.io/REFINE-DP/)

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

REFINE-DP通过强化学习联合微调扩散策略运动规划器与人形机器人全身控制器，使二者在交互中共同适应，从而缓解离线模仿学习的分布偏移和规划—控制失配。

**不用术语来说**：人形机器人开门、搬箱等任务既要决定身体和双手下一步怎样移动，又要在接触、摩擦和物体位置存在误差时稳定执行。仅从示范中学习的规划器一旦给出机器人难以准确完成的动作，后续观察就会偏离训练数据，错误还会在长任务中不断累积；而为所有可能情况采集大量人形机器人示范，成本又过高。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出分层的人形移动操作架构：扩散策略在较低维的笛卡尔空间生成动作片段，包括基座速度和手部 $SE(3)$ 位姿轨迹；强化学习控制器再将这些命令转换为全身关节位置参考，在缩小规划器动作空间的同时保留稳定移动与精确操作能力。
- 提出规划器—控制器联合微调方案：利用仿真交互和策略梯度更新扩散策略以提高任务成功率，同时更新移动操作控制器以跟踪规划器不断变化的命令分布，避免只优化单个模块所造成的接口失配。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

人形机器人移动操作（loco-manipulation）要求机器人在行走保持平衡的同时，用手与门、箱子等物体发生接触并完成长时序任务。本文采用分层规划—控制设定：上层扩散策略从专家示范中学习任务级运动规划，生成紧凑、具有物理意义的笛卡尔动作块；下层强化学习控制器将这些命令转换为全身关节位置参考，并负责稳定行走与准确操作。该设定既避免上层直接处理高维全身关节空间，也使任务规划和复杂机器人动力学控制能够分工，但两层之间的命令分布是否匹配会直接影响执行可靠性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**扩散策略（Diffusion Policy, DP）**

一种从专家示范学习动作分布的行为克隆方法，通过逐步去噪生成一段动作序列，适合表示同一状态下可能存在的多种合理行为。本文让它充当上层运动规划器，而不是直接输出全身关节控制量。

</div>
<div class="concept-item" markdown="1">

**移动操作（Loco-manipulation）**

指机器人同时协调移动与物体操作，例如边行走边开门或搬运箱子。对人形机器人而言，这类任务同时涉及欠驱动平衡、接触不确定性、高维全身动力学和长时序误差累积。

</div>
<div class="concept-item" markdown="1">

**强化学习微调（RLFT）**

先用离线示范预训练策略，再让策略在仿真环境中交互，并依据任务奖励继续更新。它可探索示范数据未覆盖的状态—动作组合，从而缓解纯行为克隆遇到分布外状态后不断累积错误的问题。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

目标是在 T1 人形机器人上自主完成开门穿行、长时序物体运输以及登上高台取物等移动操作任务。系统先在源环境中使用冻结的强化学习移动操作控制器采集人类遥操作示范，再由示范数据预训练扩散策略；随后在目标仿真环境中联合更新上层规划器与下层控制器。运行时，上层根据任务与环境观测生成包含基座速度和手部 $SE(3)$ 位姿轨迹的笛卡尔动作块，下层将其转换为关节位置参考并执行；联合优化的关键假设是，规划器输出分布会在微调中变化，因此控制器也必须同步适应该分布，才能同时改善命令跟踪和任务成功率。真实部署还要求系统可依靠机载 RGB 信息估计物体位姿，而不依赖特权状态。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$SE(3)$**

三维刚体位姿空间，同时描述手部在三维空间中的位置与旋转姿态。

</div>
<div class="notation-item" markdown="1">

**$\pi_{RL}$**

强化学习策略；在本文语境中主要指接收基座速度和手部位姿命令、输出关节位置参考的移动操作控制器。

</div>

</div>

**直接相关的工作**

- **Diffusion Policy（DP）**: 为本文提供从专家示范学习多模态动作生成模型的基础；其离线行为克隆属性也带来分布偏移和长时序累积误差，构成本文需要解决的核心背景问题。
- **Diffusion Policy Policy Optimization（DPPO）**: 将 PPO 改造为可直接微调预训练扩散策略，以提高任务成功率；REFINE-DP以此类扩散策略梯度为基础，但进一步联合更新规划器和人形机器人移动操作控制器，而非只优化单个规划策略。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

人形移动操作涉及长时序决策、高维全身运动以及物体接触。模型误差、接触不确定性和跟踪偏差可能使一次局部执行误差演变为后续规划失败，因此机器人需要的不只是复现参考动作，还要能在真实执行产生偏差后继续完成任务。这直接关系到开门通行、长距离搬运和登台取物等任务能否摆脱人工监督或启发式规划。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于示范的扩散策略与行为克隆**：从离线专家示范中学习条件动作生成分布，利用扩散模型表达复杂、可能多峰的专家行为；部署时根据当前状态生成一段未来动作。常见改进方式是扩大示范数据和模型容量，以增加状态—动作空间的覆盖范围。
- **分层运动规划与强化学习全身控制**：高层规划器输出基座速度和手部 $SE(3)$ 位姿轨迹等笛卡尔命令，低层强化学习控制器负责把它们转换为关节位置参考并维持平衡。该分工避免高层策略直接处理完整的全身关节空间，但通常分别训练两个模块。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 离线行为克隆只能学习示范数据覆盖的分布；部署中的微小执行误差会把机器人带到未见状态，规划器随后生成更不可靠的动作，形成逐步累积的分布偏移。长时序、高维且包含接触的人形任务会进一步放大这一问题。
- 单纯扩大离线示范集对人形系统需要昂贵的遥操作采集和训练计算，而且不能直接修复规划器与控制器的耦合问题：离线训练的规划器可能输出低层控制器跟踪不准的命令；若只微调规划器或控制器之一，另一模块仍面向旧的输入或执行分布。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方案缺少一种数据成本可控的闭环适应机制，能够让离线预训练的扩散规划器通过任务交互探索未见状态，同时让全身控制器同步适应规划器更新后的命令分布。待解决的关键不是单独提升高层生成能力或低层跟踪能力，而是在保持低维、直观规划接口的前提下维持两个层级之间的分布一致性。

</div>
<div markdown="1"><span>核心问题</span>

能否以少量人类示范预训练扩散策略，再利用仿真中的稀疏任务奖励，通过基于 PPO 的扩散策略梯度联合更新高层运动规划器和低层移动操作控制器，从而同时提高任务成功率、命令跟踪质量以及对预训练分布外场景的适应能力？

</div>
<div markdown="1"><span>作者直觉</span>

高层规划器像是给出一串身体与双手的路线指令，低层控制器则负责真正把这些指令做出来。若只训练前者，它可能逐渐提出后者做不到的动作；若只训练后者，它只能更好地执行原有规划，却无法纠正规划本身。让二者在同一批任务交互中共同更新，相当于规划器学习提出更有利于成功且可执行的命令，控制器也同步练习这些新命令，因此能够减少接口处的误差并阻止误差沿长任务持续放大。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

REFINE-DP 是一个“高层运动规划器 + 低层全身控制器”的分层框架。输入是机器人及物体的观测历史，高层扩散策略生成一段动作指令，包括期望双手位姿、夹爪状态和基座速度；速度到落脚点规划器再把基座速度转换为离散足步目标，低层强化学习控制器据此输出腿部与手臂的关节位置偏移，最终由比例-微分控制器驱动机器人。训练分三阶段：先获得成功的专家轨迹，再用去噪目标预训练扩散策略，最后在仿真环境中用基于 PPO 的 DPPO 微调扩散规划器，并可同步更新低层控制器。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 专家数据采集与动作接口构造

操作者通过 VR 设备或启发式规划器给出运动指令，由 $\pi_{\text{loco\_manip}}$ 在 IsaacLab 中执行；只保留成功轨迹，并记录观测与动作对。观测包含身体坐标系中的手脚位姿、夹爪状态和物体信息，动作包含期望手部位姿、夹爪状态与基座速度。

<div class="method-step__io" markdown="1">

**输入**：任务相关的初始机器人状态、物体配置、遥操作指令或按任务阶段设计的启发式规划器，以及预训练低层策略 $\pi_{\text{loco\_manip}}$。<br>
**输出**：由成功状态—动作序列组成的离线数据集 $\mathcal{D}$；文中以 50 条遥操作轨迹提供核心行为与恢复模式，再用启发式轨迹扩充到 1000 条。

</div>

**直观理解**：遥操作数据像少量高质量示范，能展示人在偏离计划后如何恢复；启发式规划器则像自动化脚本，用较低成本覆盖更多初始位置和运动时序。两者结合是在行为丰富性与数据规模之间折中。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 低层行走—操作控制器训练

分别用强化学习训练下肢策略 $\pi_{\rm lower}$ 和上肢策略 $\pi_{\rm upper}$：前者模仿参考运动并跟踪下一步落脚位置，后者跟踪左右手的位置与姿态；训练中随机化手臂构型、载荷和外力，使两个子策略能承受彼此产生的扰动。两者输出拼接为 26 维关节位置偏移 $\mathbf{a}_{t}=[\mathbf{a}^{\rm lower}_{t};\mathbf{a}^{\rm upper}_{t}]$。

<div class="method-step__io" markdown="1">

**输入**：下肢参考运动、离散落脚点命令 $\mathbf{g}^{\rm lower}_{t}$、双手的 $SE(3)$ 位姿目标 $\mathbf{g}^{\rm upper}_{t}$，以及机器人本体感知状态。<br>
**输出**：低层策略 $\pi_{\text{loco\_manip}}(\mathbf{a}_{t}\mid\mathbf{s}_{t},\mathbf{g}_{t})$，其中 12 维输出控制腿部、14 维输出控制手臂；目标关节位置为 $\mathbf{q}_{\rm target}=\mathbf{q}_{\rm def}+\mathbf{a}_{t}$，并交由比例-微分控制器跟踪。

</div>

**直观理解**：高层规划器只说明“手要到哪里、身体要怎样移动”，低层控制器负责把这些意图变成保持平衡的具体关节动作。直接指定落脚点比只跟踪速度更适合频繁启停和精细调整，因为它能直接约束脚最终落在哪里。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 扩散运动规划器离线预训练

对动作片段逐级加入高斯噪声，得到第 $k$ 个扩散步的 $\mathbf{A}^{k}_{t}$；训练噪声预测网络 $\epsilon_{\theta}$ 根据 $\mathbf{A}^{k}_{t}$、观测片段 $\mathbf{S}_{t}$ 和扩散步 $k$ 预测所加噪声。部署时从高斯噪声动作开始执行 $K$ 次反向去噪，形成条件动作分布 $p_{\theta}(\mathbf{A}^{0:K}_{t}\mid\mathbf{S}_{t})$。

<div class="method-step__io" markdown="1">

**输入**：成功示范数据集 $\mathcal{D}=\{(\mathbf{S}_{i},\mathbf{A}^{0}_{i})\}_{i=1}^{N}$，其中 $\mathbf{S}_{i}$ 是观测片段，$\mathbf{A}^{0}_{i}$ 是对应的无噪动作片段。<br>
**输出**：预训练扩散策略 $\bar{\pi}_{\theta}$，可根据当前观测生成包含基座速度、双手位姿和夹爪状态的连续动作片段。

</div>

**直观理解**：模型不是一次直接回归唯一动作，而是从随机动作逐步擦除噪声，因此能够表示示范中多种合理的操作路径。不过，这一阶段只模仿成功数据，并未直接检验生成指令经过真实闭环动力学执行后是否仍能成功。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于增广 MDP 的扩散策略强化学习微调

方法把每个环境时刻内部的 $K$ 次去噪都展开为增广马尔可夫决策过程 $\mathcal{M}_{\rm DP}$ 中的决策步，使每一步反向去噪的高斯转移概率可以显式计算。随后从回放缓冲区计算广义优势估计，并用 DPPO 的 PPO 风格策略梯度更新扩散策略参数。

<div class="method-step__io" markdown="1">

**输入**：预训练策略 $\bar{\pi}_{\theta}$、目标仿真环境、低层控制器，以及环境奖励 $R_{t}$。<br>
**输出**：适应目标环境动力学、执行误差和随机化条件的扩散规划器；它不再只追求复现示范，而是通过仿真试错直接提高累计回报与任务成功率。

</div>

**直观理解**：普通 PPO 需要知道“策略生成这个动作的概率”，但完整扩散策略的最终动作概率难以直接求出。DPPO 将一次复杂的生成过程拆成多次概率已知的高斯去噪动作，因此可以对每个中间选择应用 PPO。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 扩散策略噪声预测损失

$$
\mathcal{L}_{\text{diff}}(\theta)=\mathbb{E}_{\mathbf{A}_{t}^{0},\mathbf{S}_{t},k,\epsilon}\Big[\|\epsilon-\epsilon_{\theta}(\mathbf{A}_{t}^{k},\mathbf{S}_{t},k)\|^{2}\Big],\qquad \epsilon\sim\mathcal{N}(0,\mathbf{I})
$$

**符号说明**

- $\mathcal{L}_{\text{diff}}(\theta)$：参数为 θ 的扩散策略预训练损失。
- $\mathbf{A}_{t}^{0}$：环境时刻 t 对应的无噪专家动作片段。
- $\mathbf{A}_{t}^{k}$：对无噪动作片段执行前向扩散后，在第 k 个去噪层级得到的含噪动作片段。
- $\mathbf{S}_{t}$：环境时刻 t 的条件观测片段。
- $k$：扩散或反向去噪的时间步索引。
- $\epsilon$：从标准高斯分布采样并加入动作的目标噪声。
- $\epsilon_{\theta}$：根据含噪动作、观测和扩散步预测噪声的神经网络。
- $\mathbf{I}$：与动作维度匹配的单位协方差矩阵。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标让网络从含噪动作中识别被加入的高斯噪声；反复减去预测噪声，就能把随机样本逐步还原为符合当前观测的动作序列。它负责把专家轨迹中的行为分布压入初始规划器，但本身不包含环境回报，因此不能直接修正闭环执行中的累计误差。<br>
**原文位置**：第 III-B 节，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 去噪过程增广 MDP 的转移与奖励

$$
\bar{P}\!\left(\bar{s}_{\bar{t}+1}\mid\bar{s}_{\bar{t}},\bar{a}_{\bar{t}}\right)=\left\{\begin{array}{ll}(\mathbf{S}_{t},\mathbf{A}_{t}^{k})\sim\bm{\delta}_{\mathbf{S}_{t},\mathbf{A}_{t}^{k}},&k>0\\[4pt](\mathbf{S}_{t+1},\mathbf{A}_{t+1}^{K})\sim P(\mathbf{S}_{t+1}\mid\mathbf{S}_{t},\mathbf{A}_{t}^{0})\otimes\mathcal{N}(0,\mathbf{I}),&k=0\end{array}\right.,\qquad \bar{R}_{\bar{t}(t,k)}=\left\{\begin{array}{ll}0,&k>0\\R_{t}(\mathbf{S}_{t},\mathbf{A}_{t}^{0}),&k=0\end{array}\right.
$$

**符号说明**

- $\bar{s}_{\bar{t}}$：增广 MDP 的状态，由环境观测与当前去噪层级的动作变量共同构成。
- $\bar{a}_{\bar{t}}$：增广 MDP 中一次反向去噪所产生的下一层动作变量。
- $\bar{P}$：同时覆盖内部去噪转移和真实环境转移的增广状态转移分布。
- $\bm{\delta}_{\mathbf{S}_{t},\mathbf{A}_{t}^{k}}$：狄拉克分布，表示中间去噪步只确定性地更新动作层级，环境观测保持不变。
- $P(\mathbf{S}_{t+1}\mid\mathbf{S}_{t},\mathbf{A}_{t}^{0})$：最终动作进入机器人与环境后产生下一观测的环境动力学。
- $\mathbf{A}_{t+1}^{K}$：下一环境时刻用于启动新一轮反向扩散的高斯噪声动作。
- $\bar{R}_{\bar{t}(t,k)}$：增广时间步上的奖励。
- $R_{t}(\mathbf{S}_{t},\mathbf{A}_{t}^{0})$：最终无噪动作在环境中执行后获得的任务奖励。
- $K$：每个环境时刻内的总去噪步数。

<div class="equation-explanation" markdown="1">

**直观理解**：当 $k>0$ 时，机器人尚未执行动作，系统只从一层含噪动作移动到下一层，因此不产生环境奖励；当 $k=0$ 时，最终动作 $\mathbf{A}^{0}_{t}$ 才进入环境，产生下一观测和任务奖励，并为下一时刻重新采样高斯起点。这样，每个去噪转移都有可计算的高斯概率，而最终环境结果又能通过优势估计归因到整条去噪链，使 PPO 能微调原本难以直接计算最终动作密度的扩散策略。<br>
**原文位置**：第 III-C 节，公式（2）与公式（3）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：离线阶段最小化 $\mathcal{L}_{\text{diff}}(\theta)$，使 $\epsilon_{\theta}$ 复现专家动作分布，得到初始化策略 $\bar{\pi}_{\theta}$。在线微调阶段不再仅优化模仿误差，而是在 $\mathcal{M}_{\rm DP}$ 中收集轨迹，用广义优势估计计算 $\hat{A}(\bar{s}_{\bar{t}},\bar{a}_{\bar{t}})$，再以 PPO 风格的 DPPO 更新每一步可计算密度的去噪策略；原文没有在所给章节中展开具体 PPO 裁剪目标，因此不应补写未报告的损失公式。联合训练时，任务奖励 $\bar{R}_{t}$ 用于提高扩散规划器的成功率，控制器预训练所用的一组奖励 $\hat{R}_{t}$ 则用于提高命令跟踪、稳定性与平滑性。二者交替更新的含义是：规划器学习提出既能完成任务又可执行的指令，控制器学习跟上规划器持续变化的实际指令分布。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 解耦式全身行走—操作控制器**

下肢策略 $\pi_{\rm lower}(\mathbf{a}^{\rm lower}_{t}\mid\mathbf{s}^{\rm lower}_{t},\mathbf{g}^{\rm lower}_{t})$ 接收摆动脚标志、倒计时和以支撑脚为坐标系的目标摆动脚位姿；上肢策略 $\pi_{\rm upper}(\mathbf{a}^{\rm upper}_{t}\mid\mathbf{s}^{\rm upper}_{t},\mathbf{g}^{\rm upper}_{t})$ 接收左右手的 $SE(3)$ 目标。两个策略分别训练，并通过域随机化学习抵抗另一半身体、载荷与接触力造成的扰动，最终将输出拼接后交给比例-微分控制器。

> 直观理解：把腿部平衡和手部操作拆开，可降低单个策略同时学习全部自由度的难度；随机扰动又避免这种拆分变成完全隔离。落脚点接口还显式消除了仅给双手全局位姿时的运动学歧义，即避免机器人虽然把手放对了，却采用不合理的躯干和脚部姿态。

**2. 条件扩散运动规划器**

规划器以观测片段 $\mathbf{S}_{t}$ 为条件，通过 $K$ 个反向扩散步骤生成动作块 $\mathbf{A}^{0}_{t}$，而非仅预测下一时刻的单步动作。动作同时包含上肢目标和下肢运动意图，使手部操作与身体移动在同一个高层序列中协调；基座速度随后由速度到足步规划器转换为低层所需的离散落脚命令。

> 直观理解：动作块让模型一次考虑短期未来，而扩散生成允许同一场景存在多条合理路线。手部目标与下肢命令同时输出，则明确告诉机器人如何移动身体来配合双手，而不是让低层控制器自行猜测全身姿态。

**3. DPPO 增广决策过程与双策略联合更新**

DPPO 将环境时刻 $t$ 和去噪步 $k$ 合并为索引 $\bar{t}(t,k)=tK+(K-1-k)$，把增广状态写成观测与当前噪声动作的组合，并把下一层去噪结果视为动作。中间去噪步奖励为零，完成最终去噪并作用于环境时才接收环境奖励；联合优化时分别使用任务奖励更新 $\bar{\pi}_{\theta}$、使用原低层跟踪与稳定奖励更新 $\pi_{\text{loco\_manip}}$。

> 直观理解：该模块解决两个不同问题：将隐式扩散生成改写成 PPO 可处理的概率决策链，以及让高层规划器和低层执行器相互适应。两个策略保留不同奖励，意味着高层主要对“任务是否完成”负责，低层主要对“动作是否跟得准、是否稳定平滑”负责。

**训练与推理**

完整训练分为预训练和在线微调。首先分别训练下肢与上肢强化学习控制器：下肢模仿参考运动并跟踪离散足步，上肢跟踪由无碰撞关节构型和正向运动学生成的可行手部目标；训练通过域随机化覆盖手臂构型、载荷、外力及上下肢相互扰动。随后使用该控制器执行遥操作和启发式规划，只收集成功轨迹，并随机化物体与机器人初始状态；再将轨迹切分为观测块和动作块，以噪声预测损失预训练条件扩散策略。在线阶段有两种设置：仅冻结 $\pi_{\text{loco\_manip}}$ 并用 DPPO 更新 $\bar{\pi}_{\theta}$，或执行联合优化。联合优化对应算法 1：每个外层迭代先 rollout 得到缓冲区 $D$，采样小批量 $D_{k}$ 并以 PPO 更新低层控制器；然后重新 rollout 得到 $\bar{D}$，采样 $\bar{D}_{k}$ 并以 DPPO 更新扩散策略。推理时给定当前观测片段，规划器从高斯噪声执行 $K$ 次反向去噪并生成动作块；基座速度转换为足步序列，双手目标直接进入上肢控制器，低层策略输出关节偏移，比例-微分控制器跟踪最终目标关节位置。

**复现信息**

为公平理解和复现框架，关键选择是命令接口、数据构成及更新次序。高层动作不是仅包含一对全局手部位姿，而是同时包含双手位姿、夹爪状态和基座速度；人形机器人具有运动学冗余，只规定双手目标不足以唯一确定躯干与腿部运动。低层实际接收离散落脚点，因此另设速度到足步规划器，将基座速度转换为摆动脚目标；这也保留了在非平整地面上显式控制落脚位置的能力。数据方面，50 条遥操作轨迹扩充到共 1000 条成功轨迹，并随机化机器人和物体初态；该比例体现了恢复行为质量与自动采集规模的折中。控制输出为相对固定默认构型的 26 维关节位置偏移，其中腿部 12 维、手臂 14 维。原文所给章节未明确报告网络层数、学习率、PPO 裁剪系数、$K$ 的具体取值、动作块长度、控制频率及各奖励权重，这些信息需结合论文网站或补充材料核验。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 专家示范数据：在 IsaacLab 中采集；核心预训练配置包含 $100$ 条轨迹、约 $3$ 小时示范，用于训练高层扩散策略。数据规模实验还比较了仅 $50$ 条轨迹微调与约 $1{,}000$ 条轨迹纯预训练的效果。原文未明确报告训练集、验证集和测试集划分。
- 仿真任务集：包含物体拾取、约 $40$ 秒的长时域拾取放置、开门并穿越，以及借助台阶取物四类任务。它们共同检验行走、接触操作、隐式阶段切换及长时域误差累积；成功率与运动质量主要在该环境中评估。
- 分布外与真实机器人评测：分布外物体运输改变机器人相对目标物体的径向距离、极角和朝向角，并将范围分别扩展到预训练范围的 $320\%$、$125\%$ 和 $600\%$。硬件评测使用 $29$ 自由度 Booster T1，每个已报告任务进行 $N=20$ 次试验，用于检验仿真所得策略在感知偏差和动力学失配下的可执行性。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务成功率（SR）**

在重复试验中完整完成指定多阶段任务的比例，综合反映规划、命令跟踪、接触操作和失败恢复是否最终奏效。 （越高越好，因为它直接表示端到端任务可靠性；但它不能单独反映动作是否平滑或跟踪误差是否较小。）

</div>
<div class="metric-item" markdown="1">

**末端执行器位置与姿态误差**

比较控制器实际实现的上肢末端位姿与规划器命令之间的偏差，用于测量高低层策略之间的命令跟踪质量。 （越低越好，因为较小误差表示控制器更准确地执行规划命令，并减少规划器分布变化造成的接口失配。）

</div>
<div class="metric-item" markdown="1">

**末端执行器线速度**

在 $100$ 次试验上取平均，作为操作运动平滑性的代理指标；论文将较低的平均速度与更少的过激、抖动式动作联系起来。 （在成功率保持较高的前提下越低越好，因为这通常表示动作更平稳；但速度过低也可能意味着效率下降，所以该指标必须结合成功率和完成时间解释。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四类仿真移动操作任务上的端到端任务成功率

<div class="result-value" markdown="1">

作者报告，完整 REFINE-DP 在所有任务上优于所列基线，并将预训练策略约 $50\%$ 至 $70\%$ 的成功率提升到超过 $90\%$。由于微调后成功率已经较高，后续联合优化的主要收益不是继续提高成功率，而是改善跟踪和运动质量。

</div>

这说明强化学习微调能够把一个已有中等成功率、偶尔失败的扩散规划器变成较可靠的端到端策略，也支持预训练为稀疏奖励学习提供必要起点。不过，摘录只给出总体范围而没有逐任务数值、方差和显著性检验，因此不能据此判断每个任务上的精确优势或统计稳定性。

<div class="result-source" markdown="1">

来源：Fig. 4；Sec. IV-C，C-1 Task Success and Planner Capacity

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

REFINE-DP can achieve more than 90% by fine-tuning from the pre-trained policy of 50-70%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 数据规模与微调效率比较

<div class="result-value" markdown="1">

纯预训练约需 $1{,}000$ 条轨迹才能达到 $90\%$ 成功率，而仅用 $50$ 条轨迹预训练的扩散策略经微调后最高达到 $95\%$，对应约 $20$ 倍的示范轨迹数量差异。

</div>

结果表明在线强化学习微调可以用环境交互替代大量昂贵的人形机器人专家示范，测试的是示范数据效率，而不是总计算或总交互效率。论文未在摘录中给出微调所消耗的环境步数，因此不能断言其总体训练成本也降低了 $20$ 倍。

<div class="result-source" markdown="1">

来源：Fig. 6；Sec. IV-C，C-2 Efficiency Gains from Fine-tuning and Joint Optimization

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In contrast, a DP pre-trained on only 50 trajectories achieves up to 95% SR after fine-tuning.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Booster T1 真实机器人上的物体拾取、长时域拾取放置和开门穿越

<div class="result-value" markdown="1">

在每项 $20$ 次试验中，Task 1、Task 2 和 Task 3 的成功率分别为 $70\%$、$50\%$ 和 $75\%$；相较仿真的 $90\%+$ 明显下降。

</div>

该结果证明策略可以在真实机器人上闭环运行，包括依赖相机而非特权状态的配置，但尚未达到仿真可靠性。三个任务各只有 $20$ 次试验，且原文没有置信区间；结果主要支持“可迁移和可执行”，不证明在真实环境中稳定达到工业级可靠性。

<div class="result-source" markdown="1">

来源：Sec. IV-D Hardware Experiment

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In real-world experiments, REFINE-DP achieves a success rate of 70% (Task 1), 50% (Task 2), and 75% (Task 3), respectively, over N=20 trials.

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

- 预训练 DiT：采用 Transformer 骨干的标准扩散策略，只做离线预训练，不做强化学习微调；它直接衡量 REFINE-DP 相对于原始扩散规划器的增益。
- LSTM：使用循环网络产生规划命令，与 DiT 比较短期记忆式序列建模和扩散式轨迹分布建模，尤其检验长时域任务中隐状态是否足够。
- MLP 与 MLP-FT：MLP 从观测直接确定性回归动作；MLP-FT 保持同一分层接口并只微调规划器，以 Ornstein-Uhlenbeck 过程加入平滑、时间相关的探索噪声。该组对照用于区分强化学习微调本身的作用与扩散策略多模态表示能力的作用。
- Residual RL：冻结预训练扩散策略，仅用 PPO 学习叠加到规划动作上的小型高斯残差；它检验直接更新扩散规划器是否优于只在其输出端进行局部纠偏。

**实验想回答的问题**

- 在四类多阶段人形机器人移动操作任务中，基于强化学习微调并联合优化高层扩散规划器与低层移动操作控制器，能否比纯预训练规划器、确定性规划器和残差强化学习更可靠地完成任务？
- 性能提升究竟来自哪些因素：扩散策略的多模态轨迹建模能力、规划器与控制器的联合适配、较高的数据效率，还是对预训练分布外初始状态的在线适应能力？

**实验实现**

训练、示范采集和微调均在 IsaacLab 中完成，使用 NVIDIA H200 GPU。低层策略以 $4{,}096$ 个并行环境预训练约 $10$ 小时；扩散策略使用 $100$ 条轨迹预训练约 $18$ 小时。联合优化执行 $L=2$ 轮，每轮约 $9$ 小时，高层扩散规划器与低层控制器各占一半，总流程报告为约 $22$ 小时。扩散策略使用 $8$ 步观测历史和 $12$ 步动作块，相邻观测与动作间隔均为 $0.1$ 秒。硬件上低层控制器以 $50$ Hz、TensorRT 加速的扩散规划器以 $10$ Hz 运行；状态输入来自本体感知以及 MoCap 或头戴式 RGB 相机估计的目标物体相对位姿。真实实验将行走速度限制为 $0.2$ m/s、手部速度限制为 $0.05$ m/s。原文未明确报告随机种子、置信区间或显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 仅微调扩散规划器与联合更新低层移动操作控制器的比较 | 采用联合优化后的低层控制器时，扩散策略达到 $90\%$ 成功率约需 $20$ 次迭代，而搭配原预训练低层控制器需要约 $40$ 次，训练迭代数约减半。 | 该消融隔离了低层控制器同步适配的作用：即使高层优化目标不变，让控制器跟随高层命令分布的变化，也能更快获得成功信号。它证明的是迭代效率提升；由于每轮联合优化还包含控制器更新，不能仅凭迭代数断言墙钟时间或样本量严格减半。 | Sec. IV-C，C-2 Efficiency Gains from Fine-tuning and Joint Optimization<br><span class="experiment-evidence">Second, the jointly optimized loco-manipulation policy π′loco_manip improves the training efficiency of DP fine-tuning, requiring approximately half as many iterations (20 instead of 40) to achieve a 90% SR compared to fine-tuning with the pre-trained RL-based loco-manipulation policy πloco_manip.</span> |
| 预训练分布内策略与课程式分布外微调的比较 | 在最大域随机化强度下，预训练策略成功率为 $0\%$，课程式微调后超过 $80\%$；此时径向距离、极角和朝向角范围分别扩展到预训练范围的 $320\%$、$125\%$ 和 $600\%$。 | 该消融测试微调能否真正扩大初始状态覆盖范围，而非只在预训练分布内修补偶发错误。结果显示扩展明显，但这是针对特定三维初始位姿参数化和自定义课程所得，不能直接外推到未测试的物体、场景几何或动力学变化。 | Sec. IV-C，C-2 Efficiency Gains from Fine-tuning and Joint Optimization<br><span class="experiment-evidence">While the pre-trained policy achieves only 0% SR at the maximum randomization level, our curriculum-based fine-tuning improves the SR to over 80%.</span> |

**定性案例**

- 真实开门实验中，机器人漏抓门把手后会迈小步靠近并再次尝试；物体位置被改变时，也会在线重规划并继续执行。作者将这些现象视为微调策略具有纠错与恢复能力的证据。该观察能说明策略不是简单回放固定轨迹，但属于定性案例，原文未报告恢复行为的发生率、成功率或与基线的配对统计。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出通过强化学习联合微调扩散运动规划器与控制器的类人机器人长程移动操作框架。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`cd5473701090856875ba84f9e6f513509832804f056e5a21bb2ecf6aeba7bf0e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
