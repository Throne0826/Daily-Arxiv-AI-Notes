---
title: "[论文解读] RoboHarness: Memory-Driven Orchestration of Heterogeneous Robot Policies for Long-Horizon Planning"
description: "[arXiv 2607.18060][机器人 / 具身智能] RoboHarness通过执行记忆刻画不同机器人策略的适用边界，并在策略切换时将机器人引导至下一策略熟悉的状态区域，从而无需联合重训练即可编排异构策略完成零样本长时程任务。"
arxiv_id: "2607.18060"
announcement_date: "2026-07-29"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.351705+00:00"
source_sha256: "90059f0ee42ea3e3d8b482a6910be699e22d4f6c61a79d1dbed61f68c2c10cae"
tags:
  - "机器人 / 具身智能"
  - "长时程机器人规划"
  - "异构策略编排"
  - "能力感知任务分解"
  - "策略路由"
  - "跨策略分布失配"
  - "策略衔接"
  - "多模态执行记忆"
  - "零样本机器人执行"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2607.18060</p>

# RoboHarness: Memory-Driven Orchestration of Heterogeneous Robot Policies for Long-Horizon Planning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-29</span>
<span><strong>作者</strong> Jinbang Huang, Yuanzhao Hu, Zhiyuan Li, Ran Qi, Yixin Xiao, Zhanguang Zhang, Mark Coates, Tongtong Cao, Yingxue Zhang</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.18060v2) · [PDF 下载](https://arxiv.org/pdf/2607.18060v2) · **关键词** 长时程机器人规划, 异构策略编排, 能力感知任务分解, 策略路由, 跨策略分布失配, 策略衔接, 多模态执行记忆, 零样本机器人执行<br>


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

RoboHarness通过执行记忆刻画不同机器人策略的适用边界，并在策略切换时将机器人引导至下一策略熟悉的状态区域，从而无需联合重训练即可编排异构策略完成零样本长时程任务。

**不用术语来说**：复杂机器人任务通常包含多种性质不同的步骤，例如理解开放式指令、精确操作物体和维持多步逻辑一致性；单一控制系统很难同时擅长所有步骤。即使把多个各有所长的系统组合起来，也必须判断当前步骤该由谁执行，并避免前一个系统留下的场景状态让后一个系统无从下手，否则一次切换失败就可能引发后续连锁失败。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出统一的异构策略编排框架RoboHarness，将独立训练或手工设计的VLA、强化学习策略和任务与运动规划系统封装为可调用技能，并利用理解、记忆与自演化辅助技能，根据当前情境和执行证据进行能力感知的任务分解与策略路由。
- 提出可插拔的Memory Bridge，通过检索与下一策略相关的多模态执行轨迹并学习其空间状态分布，将机器人引导到该策略较熟悉的输入区域，以缓解跨策略分布不匹配，且不要求联合训练或共享动作表示。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于长时程机器人规划与异构策略编排领域。长时程任务通常包含语义理解、逻辑排序、精确操作和抗扰执行等不同要求，单一控制策略很难同时满足：视觉—语言—动作模型（VLA）擅长开放词汇指令理解与视觉语义对齐，但长程一致性和几何精度有限；强化学习（RL）策略可在特定训练分布内形成闭环行为，却容易受分布偏移和奖励设计影响；任务与运动规划（TAMP）能够联合处理符号逻辑和几何可行性，但受预定义抽象、技能及状态表示约束。因而，本文不再把规划对象视为接口统一、适用范围固定的同类技能，而是研究如何组合彼此独立开发、能力边界不确定且输入输出条件不同的异构机器人策略。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**长时程机器人规划**

将一个需要许多连续步骤才能完成的机器人目标分解为子任务，并持续选择和执行合适动作。其难点不仅是单步成功，还包括保持指令一致性、逻辑顺序和误差不随多次执行累积。

</div>
<div class="concept-item" markdown="1">

**异构机器人策略**

指架构、输入输出接口、训练方式和适用条件不同的控制系统，例如VLA、RL策略与TAMP系统。它们各有优势，但不能默认共享状态表示、能力边界或可直接衔接的执行条件。

</div>
<div class="concept-item" markdown="1">

**跨策略分布失配**

前一策略产生的终止状态可能不属于后一策略训练时常见或能够可靠处理的状态区域，直接移交控制便可能失败。直观地说，即使两个策略分别有效，前一个策略停下的位置和物体布局也未必是后一个策略熟悉的起点。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定自然语言描述的长时程机器人任务、当前视觉与环境状态，以及一组彼此独立训练或手工设计的异构控制策略，系统需要把任务分解为若干子任务，并依据当前物体配置、视觉观测、语言指令和执行历史判断各策略的情境化适用性，为每个子任务选择并调用可靠策略。输出不仅包括子任务序列和策略路由，还包括策略切换时的过渡执行，使上一策略的终止状态进入下一策略较为可行且接近其训练分布的状态区域。论文设定中，策略能力边界通常未知、重叠且随上下文变化，策略之间也不保证接口及状态分布天然兼容；目标是在不对这些策略进行额外联合训练的条件下，实现零样本长时程执行。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **任务与运动规划（TAMP；Kaelbling and Lozano-Pérez, 2011；Garrett et al., 2021）**: TAMP把符号任务推理与几何可行性检查结合起来，是本文长时程分解问题的重要基础；但其通常依赖预先设计、边界清晰且接口一致的抽象技能，未直接处理能力边界不确定的异构策略选择与跨策略移交。
- **技能链与策略衔接（Konidaris and Barto, 2009；Lee et al., 2019, 2021）**: 这类工作通过学习启动集合、过渡机制或终止状态正则化，缓解相邻短时程策略之间的状态分布失配，说明长程成功率取决于策略间兼容性而非仅取决于单个策略性能。与本文不同，它们主要是需要额外训练或策略正则化的训练阶段方案，并通常假设技能来自共享策略家族且能力边界较清楚。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

长时程机器人任务要求系统在连续多步执行中同时保持指令一致性、逻辑连贯性、几何精度、环境变化下的泛化能力以及抗噪性。然而，各类机器人策略通常只覆盖其中一部分能力：开放词汇理解、训练分布内的闭环控制和显式逻辑—几何推理分别由不同方法擅长，因此实际系统需要组合多个专门策略，而不是依赖一个所谓的通用策略。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **单一专门化机器人策略**：VLA模型依据视觉与语言直接生成动作，擅长语义理解和开放词汇指令跟随；强化学习策略通过奖励和交互训练获得特定分布内的闭环行为；任务与运动规划（TAMP）则利用预定义的符号抽象、技能和几何约束生成结构化计划。三者分别覆盖语义、控制或规划能力，但通常被作为相对独立的完整执行方案。
- **基于同质预定义技能的长时程规划**：传统规划器通常在一个静态技能集合中分解任务，每个技能具有预先规定且相对明确的适用条件、输入输出和状态表示；规划过程据此选择并顺序调用技能，默认相邻技能能够按既定接口直接衔接。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单一策略存在固有能力边界：VLA的长时程一致性和几何精度有限，强化学习在分布偏移或奖励定义不充分时性能下降，TAMP的泛化又受预定义抽象、技能及状态表示约束。因此，任何一种策略都难以可靠覆盖需要多种能力的完整任务。
- 传统同质技能规划假定技能边界固定且可直接组合，但独立开发的异构策略具有不同架构、输入输出要求、内部假设和执行历史，其适用范围会随物体配置、视觉观测、语言指令及历史状态变化；此外，前一策略的终止状态可能落在下一策略的可行区域或训练分布之外，导致切换时发生分布偏移并形成级联失败。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法尚未形成一种通用机制，能够依据在线情境和历史执行证据估计异构策略的不确定、重叠且动态变化的能力边界，同时显式处理相邻策略之间的状态分布不兼容。尤其缺少一种不修改各策略原生实现、不要求联合重训练或统一动作空间，仍能可靠衔接独立策略的编排方法。

</div>
<div markdown="1"><span>核心问题</span>

如何把独立训练或手工设计、接口与能力各异的机器人策略组织成一个长时程执行系统，使规划器能够为每个子任务选择当前条件下可靠的策略，并在控制权切换前将环境调整到下一策略能够稳定接管的状态？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把过去的执行轨迹当作策略能力的经验说明书：某策略曾在什么观测、物体布局和指令下成功，可用于判断它当前是否适用；与下一策略相关的成功轨迹还可近似描述其熟悉的状态区域。因而，系统不必强行把所有策略重新训练成统一模型，而可以先按经验选择最合适的策略，再在交接处主动靠近接收策略熟悉的状态，从接口外部降低切换风险。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

RoboHarness 将彼此独立开发的异构机器人策略包装为可调用的“智能体技能”，由编码智能体统一承担高层任务分解、策略路由与执行协调。输入是长时程任务指令、当前多模态观测与机器人状态；系统先通过理解技能评估语义匹配、视觉分布、状态兼容性和输入质量，再结合策略卡及历史成败统计，把子任务分配给具备相应能力的 VLA、强化学习策略或任务与运动规划系统。各底层策略保持原有接口和动作表示，因此不需要联合训练或统一动作空间。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 任务理解与执行证据提取

编码智能体按需调用理解技能，计算物体位姿的时序不确定性，并评估当前视觉与语言上下文相对各策略历史数据的相似度、机器人状态与候选策略的兼容性，以及图像质量和目标可见性。

<div class="method-step__io" markdown="1">

**输入**：高层任务指令 I、视觉观测、估计物体位姿、机器人状态及中间执行结果。<br>
**输出**：面向规划的结构化证据，包括场景可靠性、候选策略的语义与视觉匹配程度、状态兼容性和输入质量。

</div>

**直观理解**：系统不让高层智能体仅凭一张原始图像猜测，而是先把“看得清不清、任务像不像该策略学过的内容、当前姿态能不能直接接手”等问题分别量化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 能力感知的任务分解与策略路由

编码智能体将任务分解为子任务序列 τ，并为每个子任务选择策略 ρ；有效分配要求子任务属于该策略的可实现空间，且策略启动时的观测位于其可靠输入空间。策略卡提供能力、接口、约束、训练任务和历史统计，必要时编码智能体还可检查策略实现代码。

<div class="method-step__io" markdown="1">

**输入**：结构化理解证据、策略库 Π、各策略的策略卡、历史成功与失败统计及任务指令 I。<br>
**输出**：子任务—策略配对序列，以及需要进行跨策略桥接的位置。

</div>

**直观理解**：这一步既判断“哪个策略会做这件事”，也判断“它能否从眼前这个状态开始做”，从而避免只按技能名称匹配而忽略实际适用边界。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分层多模态记忆检索

系统先按文本嵌入的余弦相似度筛选语义相关节点，再在候选节点中按视觉嵌入相似度二次筛选；每个节点还携带机器人状态，并通过链表关系连接到同一轨迹中的前后时刻。

<div class="method-step__io" markdown="1">

**输入**：下一子任务指令、当前观测，以及保存成功执行轨迹的策略相关记忆库。<br>
**输出**：与下一策略、下一子任务和当前场景相关的锚点节点及其相邻轨迹片段。

</div>

**直观理解**：它先找“做过相似任务”的记录，再找“当时看到的场景也相似”的记录，减少仅靠文字或仅靠图像造成的错误匹配。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### Memory Bridge 构造与策略交接

系统用锚点前后时间偏移构造带进度标签的状态样本，拟合局部进度估计器，并以记忆样本邻域限定可信支持区域；随后在运动规划可达、记忆支持且进度非负的候选状态中，联合最大化预计进度并最小化移动代价，最后由现成运动规划策略生成桥接轨迹。

<div class="method-step__io" markdown="1">

**输入**：当前策略执行后的机器人状态、检索到的锚点及其前后状态、下一策略和可用运动规划器。<br>
**输出**：桥接轨迹 $b_t$ 及位于下一策略经验分布内的交接状态，随后启动下一策略。

</div>

**直观理解**：当前策略结束的位置可能不是下一策略熟悉的起点；桥接模块先把机器人移动到“下一策略曾经成功工作过、而且任务进度较靠前”的附近，再完成接棒。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### Memory Bridge 的可信支持区域

$$
\mathcal{R}_{\mathrm{conf},t}=\left\{\mathbf{s}\in\mathbb{R}^{d_s}\;\middle|\;d(\mathbf{s},\mathcal{S}_{\mathrm{ret},t})\leq\epsilon\right\},\qquad d(\mathbf{s},\mathcal{S}_{\mathrm{ret},t})=\min_{\bar{\mathbf{s}}\in\mathcal{S}_{\mathrm{ret},t}}\lVert\mathbf{s}-\bar{\mathbf{s}}\rVert_2
$$

**符号说明**

- $\mathcal{R}_{\mathrm{conf},t}$：第 t 次策略交接中，由检索记忆支持的可信机器人状态区域。
- $\mathbf{s}$：候选机器人状态，如末端执行器位姿与关节配置组成的状态向量。
- $d_s$：机器人状态表示的维度。
- $\mathcal{S}_{\mathrm{ret},t}$：从检索锚点沿其轨迹前后扩展后得到的机器人状态样本集合。
- $d(\mathbf{s},\mathcal{S}_{\mathrm{ret},t})$：候选状态到检索状态集合中最近样本的欧氏距离。
- $\epsilon$：支持区域的距离阈值，控制候选状态允许偏离历史样本的程度。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把“下一策略是否熟悉这个状态”近似为“它是否靠近相关成功轨迹中的状态”。进度模型即使对远离数据的状态给出高分，也不能将其作为交接目标，从而抑制分布外外推带来的不可靠决策。<br>
**原文位置**：第 4.2.2 节，Spatial distribution construction

</div>

</div>

<div class="equation-block" markdown="1">

#### 交接目标状态优化

$$
\mathbf{s}^{*}_{t}=\arg\max_{\mathbf{s}}\left[f_{\mathrm{score},t}(\mathbf{s})-\lambda_{\mathrm{motion}}C_{\mathrm{motion}}(\mathbf{s}_{t},\mathbf{s})\right],\quad \mathrm{s.t.}\;\mathbf{s}\in\mathcal{R}_{\mathrm{conf},t}\cap\mathcal{S}_{\mathrm{plan},t},\;f_{\mathrm{score},t}(\mathbf{s})\geq 0
$$

**符号说明**

- $\mathbf{s}^{*}_{t}$：第 t 次交接最终选择的目标机器人状态。
- $\mathbf{s}_{t}$：当前策略执行结束后的机器人状态。
- $f_{\mathrm{score},t}(\mathbf{s})$：根据检索轨迹局部拟合的进度估计；正值表示相对锚点具有更大的任务进度。
- $C_{\mathrm{motion}}(\mathbf{s}_{t},\mathbf{s})$：从当前状态移动到候选状态的非负运动代价。
- $\lambda_{\mathrm{motion}}$：运动代价的权重，用于平衡交接进度与移动开销。
- $\mathcal{R}_{\mathrm{conf},t}$：由相关记忆状态限定的可信支持区域。
- $\mathcal{S}_{\mathrm{plan},t}$：运动规划器能够从当前状态可行连接到的状态集合。

<div class="equation-explanation" markdown="1">

**直观理解**：目标不是机械地回到某个历史姿态，而是在“下一策略熟悉”“运动上可达”和“相对锚点已有正向进度”的状态中，选择进度高且移动成本低的交接点。随后运动规划器负责生成从当前状态到该目标的无碰撞可执行轨迹。<br>
**原文位置**：第 4.2.2 节，Bridge trajectory generation

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：RoboHarness 没有一个用于端到端联合训练全部异构策略的统一损失函数；其核心是推理时编排和局部优化。Memory Bridge 使用检索轨迹中的状态—进度对 ($\mathbf{s}_{i,j},y_{i,j})=(\mathbf{s}(n_{i,j}),j\Delta$ t) 临时训练轻量级进度估计器，再求解受记忆支持与运动可达性约束的交接目标优化。底层策略保留各自既有训练方式；出现持续失败时，系统可调用 SIMPACT、PDDLLM 等现成适配方法，但节选未给出这些方法在本文中的具体训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 理解技能与能力感知路由**

理解技能包含不确定性评估、视觉上下文评估、语义上下文评估、状态—策略兼容性评估和输入质量评估。编码智能体联合这些结构化结果、策略卡和全局历史统计进行任务分解与策略选择，而不是将某一固定技能永久绑定到某类子任务。

> 直观理解：异构策略的能力边界通常是模糊的：某策略可能会抓取某类物体，却只在特定视角、姿态或照明下可靠。本模块把这些隐含条件显式纳入决策，解决“名义上会做但当前条件下做不好”的路由问题。

**2. 多模态执行记忆**

记忆由按时间链接的轨迹节点组成，每个节点保存子任务指令 g(n)、观测 o(n)、机器人状态 s(n) 及文本和视觉嵌入。检索采用先文本后视觉的分层 Top-K 过程；轨迹和全局执行成败统计在每次 rollout 后持续更新，并供能力估计、路由和桥接共同使用。

> 直观理解：单个相似帧不能说明机器人应从哪里开始或接下来怎样变化，因此记忆不仅保存图片，还保存任务、状态和前后时序关系。它相当于可检索的成功案例库，为策略适用性提供经验依据。

**3. Memory Bridge**

Memory Bridge 围绕检索锚点向前、向后扩展 l 个时间步，以时间偏移 jΔt 作为局部进度监督，拟合轻量级状态进度函数 $f_score,t$。它只接受距离检索状态集合不超过 ε 的状态作为可靠交接目标，并在运动规划器可达的候选中权衡进度与运动代价；桥接本身由现成运动规划策略完成。

> 直观理解：不同策略即使分别能完成相邻子任务，也可能因启动状态分布不一致而无法直接串联。该模块利用下一策略的成功轨迹估计其“熟悉区域”，无需联合重训两套策略即可把当前状态送入该区域。

**训练与推理**

离线准备阶段不要求对异构策略联合训练：每个策略以原生接口封装，并建立记录类型、能力、约束、训练任务与历史表现的策略卡；成功执行数据被整理为包含指令、观测、机器人状态及嵌入的链式轨迹记忆。在线推理时，编码智能体读取任务和当前状态，调用理解技能获得决策证据，分解任务并选择策略；在策略切换前，系统对下一子任务执行文本—视觉分层检索，围绕命中节点扩展轨迹、拟合局部进度函数并规划 Memory Bridge，随后启动下一策略。每次 rollout 后写回轨迹和成败统计；仅在持续失败时触发策略适配、编排改进、网格搜索式参数调整或元数据更新，验证后的更新跨评测回合保留。作者明确说明四类自演化机制均用于模拟实验，但节选没有说明真实机器人实验是否全部启用。

**复现信息**

公平理解该方法所需的关键实现条件有三点。第一，系统依赖可生成文本和视觉嵌入的编码器、能够访问机器人状态的轨迹记忆，以及一个用于生成桥接轨迹的现成运动规划策略；异构策略不必共享动作表示。第二，分层检索包含文本候选数 $K_{\mathrm{text}}$ 和视觉候选数 $K_{\mathrm{vis}}$，桥接还涉及轨迹扩展半径 l、支持阈值 $\epsilon$、运动代价权重 $\lambda_{\mathrm{motion}}$ 和接受条件，这些参数可通过自演化中的网格搜索调整，但所给节选未报告具体取值。第三，原文在第 4.2.2 节将下一策略的检索写为 $\operatorname{Retrieve}_{\mathcal{M+1}}(g_{t+1},o_t)$，该下标在节选中存在记号歧义；结合问题定义中的策略专属记忆 $\mathcal{M}_i$ 和上下文，应理解为从下一策略相关记忆中检索，但复现时仍需核对论文原版公式或代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- LIBERO：公开的语言条件机器人操作基准，用于检验一般任务遵循能力。实验采用原始LIBERO任务；原文未明确报告本节所用测试任务数、数据划分或每项任务的重复次数。
- LIBERO-Plus：在LIBERO基础上加入七类分布外扰动，用于检验系统的分布外鲁棒性，以及其能否识别组成策略随执行情境变化的能力边界。文中还在仅保留π0.5与TAMP的受控设置下，比较π0.5的独立成功率和实际调用比例。
- LIBERO-LoHo：零样本长时程规划基准，任务平均时程约为原始LIBERO的四倍，包含相互依赖的子任务，用于检验任务分解、互补能力组合及跨策略交接。原文未明确报告本节的数据划分与重复试验次数。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**成功率（Success Rate）**

完整满足任务目标的试验比例，强调所有依赖子任务均完成，因此对长时程任务中的单点失败和策略交接失败较敏感。 （越高越好，因为它直接表示端到端完整完成任务的可靠性。）

</div>
<div class="metric-item" markdown="1">

**进度分数（Progress Score）**

衡量长时程任务中已完成目标或子任务的程度；即使最终任务失败，也能区分完全未执行与已完成大部分步骤的系统。原文节选未给出其精确计算公式。 （越高越好，因为它表示系统完成了更多任务进程，但高进度不等同于最终成功。）

</div>
<div class="metric-item" markdown="1">

**策略调用比例（Policy Invocation Ratio）**

某一底层策略在不同扰动类别中被路由调用的相对频率；实验将其与该策略独立运行时的成功率比较，以判断路由是否随情境可靠性变化。 （不存在统一的越高或越低越好；关键是调用比例应与策略在当前情境下的实际可靠性正相关，而不是固定偏好某一策略。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### LIBERO-LoHo零样本长时程评测

<div class="result-value" markdown="1">

RoboHarness在每项任务上均取得最佳结果，平均进度分数为97.5%，平均成功率为95.2%。组成策略π0.5和OpenVLA-OFT虽能完成部分子任务，但完整成功率较低；加入高层指导的π0.5仍明显落后。

</div>

作者据此主张，长任务的关键不只是把指令拆成步骤，还要把每一步分配给具备相应能力的策略，并使前一策略的结束状态进入下一策略熟悉的状态区域。该结果支持RoboHarness在所测基准上的互补能力组合，但不能单独证明其能泛化到任意未见策略、机器人平台或更长任务。

<div class="result-source" markdown="1">

来源：第6节Results，RQ2；表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

RoboHarness achieves the best result on every task, with an average progress score of 97.5% and an average success rate of 95.2%, outperforming all baselines.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### LIBERO-Plus七类分布外扰动评测

<div class="result-value" markdown="1">

RoboHarness的平均成功率达到93.2%，在七类扰动中的六类排名第一，并超过其组成策略π0.5和OpenVLA-OFT。

</div>

作者将机器人状态扰动下的较大增益归因于Memory Bridge把异常状态引导回VLA较熟悉的分布，将语言和视角扰动下的增益归因于指令解释与动态路由。分析上，这说明系统并非简单继承某个底层策略的鲁棒性；但各模块的因果贡献仍需结合消融实验判断，而且传感器噪声及不可达布局会直接破坏输入或物理可行性，编排层无法完全补救。

<div class="result-source" markdown="1">

来源：第6节Results，RQ3；表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

RoboHarness achieves the highest average success rate of 93.2% and ranks first in six of the seven categories.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 真实机器人Bridge任务的执行时扰动

<div class="result-value" markdown="1">

无额外扰动时Bridge成功率为86.7%；重新隐藏所需积木后降至66.7%，拆除部分已搭结构后为80.0%，物体位姿估计加入5%–10%随机误差后为73.3%，加入干扰积木时仍为86.7%。

</div>

重新隐藏积木造成最大退化，主要因为反复探索和重规划容易超过时间限制；拆毁后仍有80.0%的成功率，支持系统具备在线反应和重规划能力；干扰物影响较小，则说明任务相关物体识别较稳定。这些结果来自特定积木搭建、柜体和机器人配置，不能直接外推到更复杂接触操作或开放环境。

<div class="result-source" markdown="1">

来源：第8节Real Robot Experiments；图5(c)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Re-hiding blocks caused the largest degradation, reducing success from 86.7% to 66.7%, as repeated exploration and replanning frequently exceeded the time limit. RoboHarness retained 80.0% success after a partially completed structure was dismantled, demonstrating online reactivity and replanning. Under 5%–10% random errors in object-pose estimates, it achieved 73.3% success, showing tolerance to moderate perception errors. Distracting blocks had minimal effect, with success remaining at 86.7%, indicating robust identification of task-relevant objects.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 节选未给出表1、表2和图4的完整逐任务数值、方差、置信区间或显著性检验；部分基线结果还来自既有评测，因此不同方法是否具有完全一致的检查点、推理预算和运行协议无法由现有材料确认。
- 真实机器人实验集中于积木、柜体和五类目标结构，且每个结构或扰动设置为15次试验；它验证了特定平台上的可行性，但对其他机器人本体、开放物体集合、连续导航任务及更复杂接触动力学的外推仍需额外实验。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 单体VLA策略，包括π0.5、π0、UniVLA、X-VLA、OpenVLA-OFT和GR00T-N1.5；它们检验端到端视觉—语言—动作策略在没有异构策略编排时能达到的能力上限，其中π0.5和OpenVLA-OFT还是RoboHarness的组成策略，可用于判断增益是否来自编排而非更强的底层模型。
- 世界—动作模型，包括LingBot-VA、Fast-WAM和Cosmos Policy；这类方法显式建模视觉世界演化或动作后果，是与纯VLA不同的长时程决策路线。
- 分层规划方法，包括H-WM、LLM-guided VLA和logic-guided VLA；它们提供高层任务分解或逻辑指导，适合检验“仅增加高层规划”是否足以解决缺失能力和策略交接状态不兼容问题。
- TAMP，即任务与运动规划系统；它利用符号任务规划和几何运动约束处理结构化抓取、放置与装配。在能力路由实验中，TAMP与π0.5构成互补策略对，用于观察系统是否会在VLA不可靠的扰动条件下转而调用规划器。

**实验想回答的问题**

- RoboHarness能否依据不同策略的能力边界进行动态路由，并稳定衔接异构策略，从而完成单一策略难以独立完成的零样本长时程任务？
- 在分布外扰动和真实机器人执行中，RoboHarness能否保持鲁棒性；理解技能、进化技能和Memory Bridge分别解决哪些异构策略编排故障？

**实验实现**

模拟实验默认集成三个独立开发且能力互补的控制系统：在多个LIBERO套件上训练的开源π0.5检查点、在LIBERO-90任务上经GRPO后训练的OpenVLA-OFT，以及面向预定义物体集合和几何约束抓放任务的TAMP规划器。用于任务编排的coding agent由GPT-5.5驱动的Codex实现。除公开基准外，作者还设计了跨10类任务的500个长时程模拟任务，专门要求组合多个异构策略，并在五类结构搭建任务及四种扰动下进行了135次真实机器人试验。真实系统由π0.5负责接触丰富、难以精确建模的柜门开合与隐藏积木取回，TAMP负责解释结构要求并执行装配规划。部分基线结果取自既有基准评测，而非全部由作者在统一代码环境中重新运行；原文节选未明确报告置信区间、随机种子、统计显著性检验或统一推理预算。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 从完整系统中移除Understanding Skills | 作者报告这是最根本的性能退化：任务和场景解释不完整会继续传播为错误的任务分解与策略分配。原文节选未提供该变体的具体成功率或进度分数。 | 这一消融主要隔离高层语义理解对后续编排的作用。其退化说明，如果系统一开始误解目标、物体或场景，即使后续策略执行和交接机制完好，也会执行错误计划；但由于节选缺少图4的数值，无法量化它相对其他模块的降幅。 | 第7节Ablation Study，RQ5；图4<br><span class="experiment-evidence">Removing the Understanding Skills causes the most fundamental degradation because incomplete task and scene interpretation propagates into incorrect decomposition and policy assignment.</span> |
| 从完整系统中移除Memory Bridge | 该变体仍保持相对较高的任务进度，但更频繁地无法完整完成任务；原文节选未提供具体成功率或进度分数。 | 这一消融隔离跨策略状态交接的价值：高层可能已经选对下一策略，但前一策略留下的机器人姿态、物体位置或视觉状态不在下一策略熟悉的分布内，因而在交接处失败。进度仍高而最终成功下降，符合Memory Bridge主要修复后段交接而非决定初始任务分解的解释；不过没有数值和误差条时，不能判断效应大小及统计稳定性。 | 第7节Ablation Study，RQ5；图4<br><span class="experiment-evidence">In contrast, removing the Memory Bridge preserves relatively strong task progress but frequently prevents full task completion, indicating that appropriate policy selection does not guarantee that the output state of one policy is suitable for the next.</span> |

**定性案例**

- 真实机器人结构搭建展示了异构策略的功能分工：当所需积木隐藏在柜内时，π0.5执行难以用精确模型描述的柜门开启、探索、取回和关门操作，随后将控制权交给TAMP完成结构化装配。该案例直观说明异构编排的必要性：VLA擅长接触丰富的操作，TAMP擅长满足几何与结构约束；较高的整体表现依赖二者之间的状态交接，而非任一策略独立覆盖全过程。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：reused verified category during targeted regeneration
- 全文指纹：`90059f0ee42ea3e3d8b482a6910be699e22d4f6c61a79d1dbed61f68c2c10cae`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
