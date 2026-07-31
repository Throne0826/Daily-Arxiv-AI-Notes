---
title: "[论文解读] Critic Architecture Matters: Dual vs. Unified Critics for Humanoid Loco-Manipulation"
description: "[arXiv 2606.11891][强化学习] 本文考察人形机器人在同一策略中同时学习行走与伸手时，采用统一评论家还是双评论家是否会形成值得进一步因果验证的任务效率差异。"
arxiv_id: "2606.11891"
announcement_date: "2026-07-31"
primary_category: "reinforcement_learning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.171537+00:00"
source_sha256: "03788df3bc46f3aefcb616c0e5571770aee16fb921d1f3482c5e486544edc55e"
tags:
  - "强化学习"
  - "机器人 / 具身智能"
  - "人形机器人移动操作"
  - "多目标强化学习"
  - "演员—评论家"
  - "双评论家"
  - "统一评论家"
  - "课程学习"
  - "目标干扰"
  - "Unitree G1"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">强化学习 · arXiv 2606.11891</p>

# Critic Architecture Matters: Dual vs. Unified Critics for Humanoid Loco-Manipulation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Yardımcı, Mehmet Turan</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2606.11891) · [PDF 下载](https://arxiv.org/pdf/2606.11891) · **关键词** 人形机器人移动操作, 多目标强化学习, 演员—评论家, 双评论家, 统一评论家, 课程学习, 目标干扰, Unitree G1<br>
**项目页**: [https://mturan33.github.io/critic-architecture-matters/](https://mturan33.github.io/critic-architecture-matters/)

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

本文考察人形机器人在同一策略中同时学习行走与伸手时，采用统一评论家还是双评论家是否会形成值得进一步因果验证的任务效率差异。

**不用术语来说**：人形机器人一边走路一边伸手取物时，既要保持稳定、按指令移动，又要准确而迅速地触及目标；强化学习必须判断每次动作对这些目标的长期作用。如果把所有目标压成一个总分来评价，行走相关信号可能掩盖手臂动作的价值，使机器人虽然最终能够触达，却动作迟缓。问题在于，常用训练奖励和累计触达次数还可能把这种低效率隐藏起来。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将评论家架构明确提出为多目标人形机器人强化学习中的待测设计变量，对统一评论家与奖励信号相互分离的双评论家进行比较，并提出“价值估计干扰可能压低手臂动作幅度”的机制假设。
- 作者指出常规训练奖励与累计触达数不足以揭示策略效率差异，主张使用统一评测流程衡量经验证的触达成功率、触达耗时和单位交互步数的有效触达量；同时明确给出后续因果检验要求，即固定课程、动作空间和奖励，仅更换评论家并至少运行三个随机种子。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

人形机器人移动操作（loco-manipulation）要求同一策略同时控制行走与伸手触达，使机器人能在移动身体的同时完成面向目标的操作。本文属于单智能体、多目标强化学习：行走强调平衡、速度与运动稳定性，操作强调末端执行器准确到达目标，两类目标可能通过共享策略产生相互干扰。研究聚焦于评论家网络的架构选择：统一评论家根据所有目标的拼接观测和合并奖励估计总体价值；双评论家则分别接收互不混合的奖励信号并学习各自的价值函数。该选择在既有人形机器人强化学习中通常被直接设定，较少被作为需要比较的设计变量。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**演员—评论家强化学习**

演员（actor）是根据机器人观测生成控制动作的策略；评论家（critic）估计当前状态或动作未来能获得的累计回报，并为演员的策略更新提供学习信号。评论家的估计方式会影响演员更偏向哪些行为。

</div>
<div class="concept-item" markdown="1">

**多目标强化学习与目标干扰**

多目标强化学习要求一个策略同时优化多个奖励目标，例如稳定行走与准确触达。当不同目标给出的更新方向不一致时，共享策略可能优先改善一个目标而削弱另一个目标，这称为目标或梯度干扰。

</div>
<div class="concept-item" markdown="1">

**课程学习**

课程学习将训练任务按难度逐步推进，使策略先掌握较简单的技能，再学习更复杂的技能。本文的课程从静止状态下伸手触达，逐步发展到行走过程中追踪具有可变朝向的目标。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究平台为 NVIDIA Isaac Lab 中的 Unitree G1 人形机器人：机器人共有 23 个主动自由度，其中 17 个由策略控制。输入是与移动和操作目标有关的机器人观测，策略输出关节层面的控制动作，以协调行走与伸手触达；训练采用由简单到困难的顺序课程。核心比较对象是在匹配计算预算下训练的两种方案：统一评论家根据全部目标的拼接观测估计合并价值，双评论家则针对移动与操作使用分离的价值函数及互不混合的奖励信号。两种方案最终都产生可执行移动触达的单一策略，但原文强调两次训练还同时存在课程安排、手臂动作维度和一个移动奖励权重的差异，且每种方案仅运行一个随机种子，因此该比较只能建立两个已训练策略之间的效率差距，不能把差距严格归因于评论家架构。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **ULC（Sun et al. [5]）**: ULC 面向 Unitree G1 构建统一控制器，并采用与本文相近的顺序技能习得方式；它说明课程式全身控制是直接相关的技术路线，但没有像本文一样把统一评论家与双评论家作为独立设计变量进行比较。
- **Haldar et al. [16] 的模仿学习策略强化学习微调**: 该工作表明，使用强化学习微调模仿学习策略可提高分布偏移下的鲁棒性。本文据此提出结构性联系：若强化学习中的竞争目标会覆盖预训练行为，那么按目标分离评论家可能有助于减轻干扰；但这是与本文观察一致的假设，而非本文已隔离验证的因果结论。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

面向人类环境的人形机器人需要用一个策略协调移动与操作，例如在保持行走稳定的同时伸手触及目标。该需求在模仿学习策略经强化学习微调的混合流程中尤其关键：强化学习本应提高演示分布之外的鲁棒性与泛化能力，但不恰当的价值评估可能使新产生的行走梯度覆盖已经学会的手臂行为。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **统一评论家**：将不同目标的观测拼接后输入同一个价值函数，并依据合并奖励估计策略的总体长期回报。它结构直接，但不同目标会共享同一价值估计通道。
- **双评论家**：为行走与操作维护彼此分离的价值函数，并向各评论家提供不相交的奖励信号，使两个目标分别形成价值估计，再共同支持单一策略的训练。直观上，这相当于让行走和伸手各有一套评分标准。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有人形机器人强化学习工作通常直接采用某一种评论家架构而不比较替代方案，因此缺少证据判断共享价值估计是否会造成目标间干扰，也无法为架构选择提供可靠依据。
- 最终训练奖励和训练期间的累计触达数主要反映是否获得回报，不能充分刻画一次触达需要多少步或单位交互预算能完成多少次有效触达；结果是动作明显迟缓的策略仍可能呈现相近的训练指标。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚未解决的缺口是：在行走与操作共享策略的条件下，分离价值估计是否能够减少多目标之间的干扰并提高实际任务效率，以及这种差异应由何种标准化指标检出。尤其对于模仿学习后再用强化学习微调的策略，目前缺乏证据说明评论家架构会促使梯度保留已有操作技能，还是将其覆盖。

</div>
<div markdown="1"><span>核心问题</span>

在匹配计算预算的人形机器人行走操作训练中，双评论家运行是否比统一评论家运行产生更快、更高吞吐量且成功率更高的触达策略；观察到的差异能否在严格控制课程安排、手臂动作维度、奖励权重和随机种子后归因于评论家架构本身？

</div>
<div markdown="1"><span>作者直觉</span>

统一评论家必须用一个标量价值同时解释行走稳定性、速度跟踪和手臂触达等信号；当行走奖励更密集或梯度更强时，价值函数可能优先拟合行走目标，使策略减少幅度较大的手臂动作。双评论家把两类奖励的价值估计分开，有望让操作信号不被行走信号淹没。作者将此解释为机制假设，而非已证实因果结论，因为现有两次运行还同时改变了课程安排、手臂动作维度和一个行走奖励权重，且每种设置仅训练了单个种子。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法在 NVIDIA Isaac Lab 中训练 Unitree G1 人形机器人完成“行走同时伸手触达目标”的联合任务。机器人共有 $23$ 个主动自由度，策略控制其中 $17$ 个：腿部分支控制 $12$ 个腿关节，手臂分支控制右臂 $5$ 个关节；腕部和手部关节固定。核心设计变量是价值函数的组织方式：统一评论家将两个分支的观测拼接为 $109$ 维输入，用单一价值函数 $V_{\mathrm{unified}}$ 评估运动与操作奖励的总回报；双评论家则使用相互独立的 $V_{\mathrm{loco}}$ 与 $V_{\mathrm{arm}}$，分别接收运动奖励和触达奖励，避免两个目标在价值估计中直接混合。两个行为分支均使用 PPO 训练，并通过由静止触达到行走触达、再到末端姿态控制的顺序课程逐步提高难度。

直观地说，演员负责“决定关节怎样动”，评论家负责“判断当前动作长期来看是否有利”。统一评论家相当于让同一位评审把走稳和伸手合成一个总分；双评论家则让两位评审分别评价腿和手臂，使某一目标的奖励尺度或学习信号不易掩盖另一目标。论文还构造 Stage 7 变体，在双评论家基础上冻结运动分支、重新训练手臂，并加入五类反奖励投机机制，用于检验更严格的有效触达判定和奖励工程能否进一步改善策略。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造分支观测与动作空间

运动演员 $\pi_{\mathrm{loco}}$ 接收 $57$ 维本体观测，包括基座速度、投影重力、腿关节状态、速度命令和步态相位，并输出 $12$ 个腿关节目标。手臂演员 $\pi_{\mathrm{arm}}$ 接收 $52$ 维手臂相关观测，在 Stage 7 中因加入三项反投机特征而变为 $55$ 维，并输出 $5$ 个右臂关节残差动作。

<div class="method-step__io" markdown="1">

**输入**：仿真器提供的机器人本体状态、基座运动、关节状态、速度命令、步态相位、末端执行器位置和目标信息。<br>
**输出**：由腿部关节目标和手臂残差动作组成的 $17$ 维受控动作，驱动 G1 在仿真中行走并触达目标。

</div>

**直观理解**：系统先把全身任务拆成“腿怎样走”和“手臂怎样伸”两条信息通道。残差动作表示手臂策略主要学习在已有动作基础上做修正，而不是独自生成所有底层控制量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按评论家架构估计长期回报

统一架构把两个观测流拼接为 $109$ 维输入，由单一 $V_{\mathrm{unified}}$ 估计运动与操作奖励的组合价值；双评论家架构则由 $V_{\mathrm{loco}}$ 仅学习速度跟踪与平衡奖励，由 $V_{\mathrm{arm}}$ 仅学习触达距离与位移奖励。

<div class="method-step__io" markdown="1">

**输入**：两个演员的观测，以及环境返回的运动和操作奖励信号。<br>
**输出**：供 PPO 更新使用的价值估计；统一架构产生一个组合价值，双评论家架构产生两个目标分离的价值估计。

</div>

**直观理解**：价值估计用于判断一个动作带来的长期收益，而不只看当前一步。双评论家的关键不是增加动作分支，而是把“走得好”和“够得着”分别记账，降低目标之间通过同一价值函数相互干扰的可能。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 通过顺序课程进行 PPO 优化

两个分支均采用 PPO 更新；训练从较简单的静止触达开始，再加入行走、固定末端姿态和可变末端姿态，并在持续达到有效触达率阈值后晋级。双评论家 S6s 使用 $13$ 级课程：等级 $0$–$4$ 为静止触达，$5$–$6$ 为行走触达，$7$–$8$ 为固定姿态，$9$–$12$ 在 $20^\circ$–$80^\circ$ 扩张圆锥内采样可变姿态。

<div class="method-step__io" markdown="1">

**输入**：当前课程等级、策略采集的轨迹、评论家价值估计，以及对应分支的奖励。<br>
**输出**：逐步适应更高速度、更严格位置阈值和更复杂末端方向命令的联合运动—操作策略。

</div>

**直观理解**：课程学习类似先练站着伸手，再练边走边伸手，最后要求手掌朝向指定方向。这样可避免策略一开始就同时面对平衡、移动、位置和姿态等全部困难。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 用反奖励投机机制训练 Stage 7 变体

Stage 7 在双评论家框架上加入绝对工作空间采样及最小距离限制、三条件有效触达判定、朝向目标速度奖励与静止惩罚、基于有效触达率的课程晋级，以及投机检测启发式规则。该变体采用独立的 $8$ 级课程，覆盖站立、行走和固定掌心朝下的行走触达。

<div class="method-step__io" markdown="1">

**输入**：已训练并冻结的运动分支、新初始化的手臂策略、目标采样结果、末端轨迹和触达时间。<br>
**输出**：一个专门检验奖励工程是否能在双评论家基础上继续提升表现的手臂策略，以及排除虚假触达计数后的有效触达事件。

</div>

**直观理解**：如果目标会自动刷新，策略可能通过很少移动或利用判定漏洞“刷到”触达次数。三条件判定要求手真正靠近目标、相对起点移动足够远且在时限内完成，从而让计数更接近真实任务成功。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 三条件有效触达判定

$$
\mathrm{valid}=(\lVert p_{ee}-p_t\rVert<\epsilon_{pos})\wedge(\lVert p_{ee}-p_{ee}^{0}\rVert>d_{disp})\wedge(t<t_{max})
$$

**符号说明**

- $\mathrm{valid}$：当前触达是否被验证为有效的布尔变量。
- $p_{ee}$：判定时刻的末端执行器位置。
- $p_t$：当前目标位置。
- $\epsilon_{pos}$：允许的末端—目标位置误差阈值。
- $p_{ee}^{0}$：本次触达开始时的末端执行器位置。
- $d_{disp}$：触达必须超过的最小末端位移。
- $t$：本次触达已经消耗的时间。
- $t_{max}$：允许完成触达的最大时间。
- $\wedge$：逻辑与，表示三个条件必须同时成立。

<div class="equation-explanation" markdown="1">

**直观理解**：有效触达必须同时满足三点：手已经足够靠近目标、手相对起点确实移动了足够距离、并且动作在时限内完成。该判定不是主要 PPO 损失，而是防止自动目标重采样等机制产生虚假成功计数，并用于 Stage 7 的评价与课程晋级。<br>
**原文位置**：第 III-C 节，公式（1）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：两个行为分支都使用 PPO 根据采样轨迹进行策略与价值函数更新。双评论家方案中，运动分支的优化信号来自速度跟踪和平衡奖励，操作分支的优化信号来自触达距离和末端位移奖励；统一评论家方案则让 $V_{\mathrm{unified}}$ 估计两类奖励的组合价值。原文节选未给出完整 PPO 损失函数、各奖励项的精确公式或组合方式，因此不能进一步写出未报告的总目标；已报告的共享超参数为学习率 $3\times10^{-4}$ 并采用余弦退火、折扣因子 $\gamma=0.99$、广义优势估计参数 $\lambda=0.95$ 和裁剪比 $0.2$。Stage 7 的有效触达公式主要约束成功判定、课程晋级和防投机机制，而非替代 PPO 优化目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双演员—双评论家结构**

运动分支由 $\pi_{\mathrm{loco}}$ 和 $V_{\mathrm{loco}}$ 构成，手臂分支由 $\pi_{\mathrm{arm}}$ 和 $V_{\mathrm{arm}}$ 构成。两个评论家不仅参数独立，而且奖励流不相交：前者只处理速度跟踪与平衡，后者只处理末端触达距离与位移；这区别于使用两个演员但共享 $V_{\mathrm{unified}}$ 的统一评论家方案。

> 直观理解：该模块试图解决多目标强化学习中的信用分配问题，即一次表现变好究竟来自腿还是手臂。分开评价后，腿部奖励不必与手臂奖励争夺同一个总价值信号，但这并不自动证明性能差异仅由评论家造成，因为两次训练还存在课程等混杂差异。

**2. 分阶段联合任务课程**

S6s 的课程沿任务能力逐步扩展：位置阈值从 $0.12\,\mathrm{m}$ 收紧到 $0.04\,\mathrm{m}$，命令前向速度上限由 $0$ 增至 $0.6\,\mathrm{m/s}$，末端方向要求从无约束变为掌心向下，再变为从最大 $80^\circ$ 圆锥中采样。课程晋级依赖持续超过阈值的有效触达率，但原文指出不同训练运行的晋级阈值并不相同。

> 直观理解：课程同时控制“走多快、够多准、手掌朝哪里”三个难度轴。它让策略逐步获得能力，但不同课程会改变策略见过的数据和最终任务，因此比较评论家架构时必须把课程差异视为潜在混杂因素。

**3. 反奖励投机与有效触达验证**

Stage 7 将触达成功定义为位置接近、实际位移和完成时限三个条件的合取，并配合受约束的目标采样、运动导向奖励、晋级指标和投机检测。该阶段冻结运动分支并重新初始化手臂策略，因此优化重点落在操作分支及其奖励设计上。

> 直观理解：仅用末端到目标的距离可能把偶然靠近、目标刷新到手边或几乎没有主动移动的情况算作成功。增加位移与时间条件，可把“看起来近”区分为“确实主动且及时地伸手到达”。

**训练与推理**

训练时，仿真环境并行生成机器人状态、命令和目标；运动与手臂演员分别读取对应观测并输出腿关节目标和手臂残差动作。环境执行组合动作后返回下一状态及奖励，评论家按所选架构估计长期回报：统一方案把观测拼接后学习组合价值，双评论家方案则按奖励类型分别估值。PPO 随后更新演员和评论家，课程控制速度范围、位置精度与末端方向要求；达到持续有效触达率阈值后进入下一等级。Stage 7 训练冻结运动分支、重新初始化手臂策略，并通过更严格的触达验证与独立 $8$ 级课程优化操作行为。

推理或评估时不再进行参数更新。给定当前机器人状态、运动命令和触达目标，$\pi_{\mathrm{loco}}$ 产生 $12$ 个腿关节目标，$\pi_{\mathrm{arm}}$ 产生 $5$ 个右臂残差动作，两者同时作用于机器人；腕部和手部保持固定。评论家主要服务于训练期价值估计，实际动作由演员输出；若采用 Stage 7 的验证规则，则仅当位置误差、实际位移和时限三个条件同时满足时才记录一次有效触达。

**复现信息**

实验平台为 NVIDIA Isaac Lab 中的 Unitree G1。机器人有 $23$ 个主动自由度，但策略仅控制 $17$ 个，其中腿部 $12$ 个、右臂 $5$ 个；腕部和手部全程固定。主双评论家方案中，运动观测为 $57$ 维，手臂观测为 $52$ 维；Stage 7 添加三项反投机特征后手臂观测为 $55$ 维。统一评论家的输入是两个观测流拼接后的 $109$ 维向量。不同运行使用的并行环境数量在节选中未给出，只说明应按运行分别报告。

公平解释结果时必须保留训练设置的非等价性。S6s 使用 $13$ 级课程，最终训练任务包括最高 $0.6\,\mathrm{m/s}$ 的行走、$0.18$–$0.40\,\mathrm{m}$ 的目标距离、$0.04\,\mathrm{m}$ 位置要求和从 $80^\circ$ 圆锥采样的掌心方向；S6u 使用不同的 $40$ 级课程，阶段边界会把基座速度命令重置为零，并包含 S6s 未训练的夹爪和负载能力，却不训练可变末端方向。论文还明确指出两次运行存在手臂动作维数、一个运动奖励权重、课程安排以及单随机种子等差异，因此现有流程只能比较两条已训练策略的效率，不能把差异严格归因于评论家架构；建立因果结论需要保持其余设置一致的单变量消融。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 本文不使用固定离线数据集，而是在 NVIDIA Isaac Lab 中对 Unitree G1 类人机器人进行在线强化学习训练与仿真评测。主要比较的 S6u 与 S6s 均使用 2,048 个并行环境训练 20,000 次迭代；S7 使用 4,096 个并行环境训练 15,000 次迭代。训练任务采用顺序课程，从静止状态下伸手触及目标逐步推进到行走过程中触及具有可变朝向的目标。
- 标准化评测集由仿真器在线采样目标构成，不存在预先划分的训练集、验证集和测试集。三种策略均在站立与行走模式下各评测 3,000 步；评测使用单环境、确定性动作和随机种子 42，并统一采用绝对目标采样、最小目标距离 0.12 m、位置阈值 0.06 m、位移阈值 0.10 m及 150 步超时限制。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**验证到达率（validated reach rate）**

同时满足目标位置阈值和位移验证条件的成功到达比例。位移验证用于排除机器人仅通过身体或坐标变化制造“已到达”表象的情况，因此比只检查末端位置更严格。 （越高越好，因为它表示更多目标在附加有效性检查后仍被判定为成功。）

</div>
<div class="metric-item" markdown="1">

**平均到达时间（average time-to-reach）**

策略从开始尝试到首次满足有效到达条件所需的平均仿真步数，用于衡量完成单次任务的速度。 （越低越好，因为更少的仿真步意味着策略更快完成目标到达。）

</div>
<div class="metric-item" markdown="1">

**到达吞吐量（validated reaches per 1,000 steps）**

每 1,000 个评测步中完成的有效到达次数，将成功数量按交互步数归一化，用于衡量固定仿真预算下的任务完成效率。 （越高越好，因为相同交互预算内可完成更多经过验证的目标到达。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 标准化目标到达评测：S6s 双评论家与 S6u 统一评论家的平均到达时间比较

<div class="result-value" markdown="1">

作者报告 S6s 平均需要 6.5 个仿真步到达目标，而 S6u 需要 22.6 步；按两者比值计算，双评论家策略约快 3.5 倍。

</div>

这说明训练得到的 S6s 策略一旦开始执行，到达目标所需的交互步骤明显更少。该结果反映的是两条完整训练流程最终策略之间的效率差距，不能单独证明差距由评论家架构造成，因为两次运行还存在课程安排、手臂动作维度和一个移动奖励权重等差异。

<div class="result-source" markdown="1">

来源：摘要；对应 IV-B Results 的 Table II 标准化评测

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under a matched compute budget, the dual-critic run reaches targets 3.5x faster (6.5 vs. 22.6 simulation steps), achieves 2x higher throughput (14.3 vs. 7.0 validated reaches per 1,000 steps), and attains a higher validated reach rate (65.2% vs. 53.8%) than the unified-critic run in a standardized evaluation.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 标准化目标到达评测：S6s 双评论家与 S6u 统一评论家的单位步数吞吐量比较

<div class="result-value" markdown="1">

作者报告 S6s 每 1,000 步完成 14.3 次有效到达，S6u 为 7.0 次，因此双评论家训练所得策略的到达吞吐量约为统一评论家的 2 倍。

</div>

吞吐量同时受到成功频率和单次到达速度影响，因此该结果表示在相同评测步数预算下，S6s 能完成约两倍数量的有效目标。它不能说明训练本身只需一半算力，也不能隔离评论家结构的因果作用；这里比较的是最终策略在评测阶段的任务完成效率。

<div class="result-source" markdown="1">

来源：摘要；对应 IV-B Results 的 Table II 标准化评测

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under a matched compute budget, the dual-critic run reaches targets 3.5x faster (6.5 vs. 22.6 simulation steps), achieves 2x higher throughput (14.3 vs. 7.0 validated reaches per 1,000 steps), and attains a higher validated reach rate (65.2% vs. 53.8%) than the unified-critic run in a standardized evaluation.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 标准化站立评测：S6s 双评论家与 S6u 统一评论家的验证到达率比较

<div class="result-value" markdown="1">

S6s 的验证到达率为 65.2%，S6u 为 53.8%，双评论家策略高 11.4 个百分点。

</div>

在统一阈值和确定性动作条件下，S6s 有更高比例的尝试通过了严格到达验证，说明其优势不只来自更快完成少数成功案例。不过，这仍是两个单随机种子策略之间的观察性比较；11.4 个百分点的差距没有置信区间或跨种子方差支持，不能据此断言双评论家在一般情况下必然更优。

<div class="result-source" markdown="1">

来源：Table II，Standing evaluation

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Validated reach rate | 53.8% | 65.2% | 60.9%

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

- S6u（Unified Critic）是核心对照：它用一个 109 维输入的统一评论家估计移动与操作的组合价值，手臂观测为 52 维、手臂动作为 12 维。它用于检验常见的单价值函数设计在移动操作联合训练中的表现。
- S6s（Dual Critic）是主要候选方法：它采用双 Actor-Critic，将不同奖励信号交给分离的评论家；手臂观测同为 52 维，但手臂动作仅为 5 维。它与 S6u 的训练迭代数和并行环境数相同，但并非严格的单变量对照。
- S7（Dual + Anti-Gaming）是在双评论家基础上加入五种防奖励投机机制的变体，同时冻结移动策略并重新训练手臂策略。它用于判断更复杂的奖励约束能否超越基础双评论家，但其并行环境数、训练迭代数和课程安排也不同。

**实验想回答的问题**

- 在类人机器人多目标强化学习中，在训练预算基本匹配的条件下，将移动与操作目标交给两个分离的价值函数，即双评论家，是否比用单一价值函数估计组合回报的统一评论家获得更高的到达成功率与样本效率？
- 在双评论家方案上增加五种防奖励投机机制，是否能够进一步改善目标到达表现？

**实验实现**

所有训练均在单张 RTX 5070 Ti GPU（12 GB 显存）上使用 NVIDIA Isaac Lab 运行，报告速度约为每秒 17,000 步。机器人为 Unitree G1，共有 23 个主动自由度，其中 17 个由策略控制。标准化评测固定为单环境、确定性动作和种子 42，每种策略分别在站立及行走模式运行 3,000 步；共享移动参数的检查点加载通过逐位一致的权重匹配进行验证。S6u 与 S6s 各训练 20,000 次迭代并使用 2,048 个并行环境，S7 训练 15,000 次迭代并使用 4,096 个并行环境。需要注意，S6u 的启动配置没有被直接记录，其环境数与迭代预算是作者根据检查点和每轮到达计数器重建的。三次运行的最终课程等级分别为 S6u 的 10/40、S6s 的 12/13 和 S7 的 7/8；等级从零开始且对应不同课程表，所以这些编号不能直接视为相同难度。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 防奖励投机机制消融：S7（双评论家加五种 anti-gaming 机制）对比 S6s（基础双评论家） | S7 的站立验证到达率为 60.9%，低于 S6s 的 65.2%，下降 4.3 个百分点；作者据此报告加入五种防奖励投机机制未带来进一步提升。 | 该比较意在测试额外的奖励约束是否能减少策略利用奖励漏洞并提高真实到达表现。结果没有显示收益，但它不是纯粹只开关五种机制的严格消融：S7 还冻结了移动策略、使用新初始化的手臂策略，并采用 4,096 个并行环境、15,000 次迭代及不同课程，因此下降不能唯一归因于防投机机制。 | 摘要；具体站立验证到达率见 Table II<br><span class="experiment-evidence">Adding five anti-gaming reward mechanisms on top of the dual critic yields no further improvement (60.9% vs. 65.2%).</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：研究多目标强化学习中双评论家与统一评论家架构对人形机器人移动操作策略训练的影响。; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`03788df3bc46f3aefcb616c0e5571770aee16fb921d1f3482c5e486544edc55e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
