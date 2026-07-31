---
title: "[论文解读] Task and Skill Planning: Hierarchical Robot Planning with Black-Box Skills"
description: "[arXiv 2504.17901][机器人 / 具身智能] 本文研究如何在不获知技能控制器内部机制的情况下，将学习型、力控型、机器人内置型等异构黑盒技能纳入分层规划，并通过面向规划器的几何接口保持动作可行性检查和由物体阻挡引起的失败推理能力。"
arxiv_id: "2504.17901"
announcement_date: "2026-07-30"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.802660+00:00"
source_sha256: "97badbc27b0e0a188b66143b097f2bc64c38732293e7950679bb9288d31ab00b"
tags:
  - "机器人 / 具身智能"
  - "任务与技能规划"
  - "任务与运动规划"
  - "层次化机器人规划"
  - "黑盒技能"
  - "异构技能"
  - "运动学包络"
  - "可组合交互原语"
  - "长时程规划"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2504.17901</p>

# Task and Skill Planning: Hierarchical Robot Planning with Black-Box Skills

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Benned Hedegaard, Yichen Wei, Ziyi Yang, Ahmed Jaafar, Stefanie Tellex, George Konidaris, Naman Shah</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2504.17901v3) · [PDF 下载](https://arxiv.org/pdf/2504.17901v3) · **关键词** 任务与技能规划, 任务与运动规划, 层次化机器人规划, 黑盒技能, 异构技能, 运动学包络, 可组合交互原语, 长时程规划<br>


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

本文研究如何在不获知技能控制器内部机制的情况下，将学习型、力控型、机器人内置型等异构黑盒技能纳入分层规划，并通过面向规划器的几何接口保持动作可行性检查和由物体阻挡引起的失败推理能力。

**不用术语来说**：现实机器人往往已有一套来源和实现方式各不相同的技能，例如抓取可由运动规划完成，擦拭依赖力控制，导航可能是机器人自带功能，而某些操作则来自学习策略。规划器需要把这些技能串成一个长任务，但它通常既看不到技能内部如何决策，也无法用同一种模型描述所有技能；同时，一个技能结束时的机器人姿态还必须适合下一个技能，若路径被物体挡住，规划器也应判断需要移动什么物体，而不能只把执行失败当成不可解释的错误。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将需要组合通用技能与运动规划的问题形式化为混合机器人规划问题，并提出分层的任务与技能规划框架 TASP，使预先存在的学习型、力控型、内置型和运动规划型技能可以在统一规划过程中被调用。
- 作者用“运动学包络”向规划器暴露黑盒技能的可启动区域及名义几何效果，并将技能封装为可组合交互基元（CIP），以合成相邻技能之间的头部和尾部运动，从而保留基于运动规划的可行性检查及面向物体的失败推理。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于长时程机器人规划领域。任务与运动规划（TAMP）通常把离散的符号任务规划与连续的运动规划结合起来：前者决定“按什么顺序做哪些动作”，后者检查每个动作能否由无碰撞轨迹实现。经典TAMP默认高层动作都能细化为纯运动规划，但真实机器人还常配有学习策略、力控制行为、内置控制器和轨迹回放等异构技能；这些技能可能闭环、随机或内部不可见，无法统一建模为运动轨迹。本文所研究的任务与技能规划（TASP）因此需要在保留符号长时程推理和几何可行性检查的同时，规划并衔接这类预先存在的黑盒技能。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**符号任务规划（symbolic task planning）**

它用谓词表示离散世界状态，并用带有前置条件和效果的高层动作搜索动作序列。其优点是适合长时程推理，但所得动作不能直接驱动机器人。

</div>
<div class="concept-item" markdown="1">

**运动规划（motion planning）**

它在机器人的连续配置空间中寻找一条从初始配置到目标配置的无碰撞轨迹。它能验证几何可执行性，但难以单独处理长时程组合、感知反馈和持续接触等行为。

</div>
<div class="concept-item" markdown="1">

**任务与运动规划（TAMP）**

TAMP在符号动作搜索与连续运动规划之间交替，将每个高层动作细化为可执行轨迹。本文关注其传统假设失效的情形：部分动作必须由学习、力控制或其他黑盒技能执行，而不能仅靠运动规划实现。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是机器人及环境的初始系统配置、对象集合、符号目标，以及由运动规划技能、学习策略、力控制行为、内置技能和轨迹回放等组成的异构预训练技能库；技能控制器可能闭环、随机或对规划器不透明。规划器必须判断各技能何时可启动、技能的名义几何效果如何影响后续动作，并为相邻技能生成衔接运动。输出是一条层次化任务计划及其可执行低层实现，使机器人从初始配置达到满足目标条件的配置。核心假设不是能够访问所有技能的内部动力学，而是可为黑盒技能提供面向规划器的几何结构，例如描述可启动区域及名义几何效果的运动学包络；该设置还要求处理非向下可细化动作，即局部细化失败时可能需要识别障碍物并修改更早的对象级决策。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{W}$**

机器人与环境共同构成的系统配置空间；单个元素描述机器人和场景对象的连续状态。

</div>
<div class="notation-item" markdown="1">

**$\alpha$**

抽象函数，把连续系统配置映射为由接地谓词组成的高层符号状态，例如由初始配置得到 \(s_i=\alpha(w_i)\)。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{A}_{\alpha}$**

定义在抽象符号关系上的高层机器人动作集合；经典TAMP假设其中每个动作均可通过运动规划执行，而本文要扩展到异构黑盒技能。

</div>
<div class="notation-item" markdown="1">

**$\Gamma$**

逆抽象或细化函数，用于把符号动作转化为相应的连续运动计划。

</div>

</div>

**直接相关的工作**

- **结合学习技能、闭环控制器或不确定性执行的TAMP方法**: 这些工作已经说明技能可以嵌入TAMP，但通常预设特定的策略结构、控制器类别，或显式学习技能可行性、效果和值函数。本文进一步面向跨实现类别的预存异构技能库，不要求规划器访问统一的控制器内部模型。
- **结合任务规划与接触丰富、力控或强化学习行为的方法**: 这些方法通常重点支持某一种技能策略。本文将其视为互补方向，目标是在同一层次化规划框架中混合运动规划、学习、力控制、轨迹回放和机器人内置技能，并通过运动学包络保留对象中心的几何失败推理。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

长时程机器人任务通常要求连续执行多种性质不同的行为，并处理技能之间的几何衔接与环境阻挡。例如，移动操作机器人可能先导航到房间、抓取工具、移动至另一房间，再以持续接触的力控技能完成擦拭。实际系统中的这些技能往往是既有资产，可能闭环、随机或对规划器不透明，因此不能为了统一规划而假定它们都能被改写成同一类控制器。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **传统任务与运动规划（TAMP）**：TAMP把离散的任务级动作选择与连续的机器人运动规划结合起来：任务层决定动作及其顺序，运动层检查相应轨迹是否在几何上可行。传统方法通常把每个任务级动作视为可进一步归约为运动学运动规划的问题。
- **集成特定技能或控制器的扩展型 TAMP**：近期方法把学习技能、闭环控制器或不确定性处理机制接入 TAMP 式系统，使规划不再局限于纯运动学动作；但这类集成通常围绕某一种预先规定的策略结构或控制器类别建立技能模型与接口。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 传统 TAMP 将技能归约为运动学路径规划，难以直接表达需要持续接触、反馈控制或学习策略的行为；其结果是擦拭、涂抹等技能不能作为已有控制器被自然复用。
- 已有技能增强型方法通常要求统一或特定的策略结构与控制器类别，因而难以同时接入闭环、随机且内部不可见的异构技能；若规划器缺少这些技能的几何启动条件和效果信息，也就难以判断技能能否衔接，或在非向下可精化动作失败时推断哪个物体造成阻挡以及应如何修改场景。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究已表明技能能够进入分层规划，但仍缺少一种面向既有异构技能库的统一规划接口：该接口既不要求显式建模或统一参数化每个控制器的内部行为，又必须提供足够的外部几何结构，使规划器能够检查技能何时可执行、技能前后如何连接，以及当前几何安排会如何妨碍后续动作。

</div>
<div markdown="1"><span>核心问题</span>

能否仅为异构黑盒技能提供有限的、面向规划器的几何描述，就让分层规划器把它们与运动规划共同组合成长时程方案，同时保留典型 TAMP 中基于物体和反事实场景修改的失败推理能力？

</div>
<div markdown="1"><span>作者直觉</span>

规划器不必理解一个技能内部如何产生每一步控制信号，只需掌握与组合有关的“边界信息”。运动学包络描述技能可从哪些机器人状态启动，以及执行后大致形成什么几何状态；CIP 再利用这些边界，为前一技能到当前技能、以及当前技能到后一技能补出过渡运动。直观地说，这类似于给不同厂商制造的模块规定兼容接口：模块内部可以完全不同，只要输入端、输出端及占用空间足够明确，系统就能连接模块并提前发现碰撞或阻挡。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

TASP（Task and Skill Planning）把长时程机器人问题建模为“符号任务规划—连续运动规划—黑盒技能执行”的分层规划。输入包括机器人与物体的当前状态、目标状态，以及一组对象中心技能；每个技能可以由运动规划、力控制、轨迹回放或学习策略实现。方法先用可组合交互原语（Composable Interaction Primitive, CIP）包装每个技能：在原技能策略前后分别加入头部运动计划和尾部运动计划，使机器人能够进入技能的运动学启动区域，并在技能结束后返回可供后续规划连接的自由空间。随后，实体抽象把CIP转换成带离散参数的高层动作，修改后的ATAM分层规划器生成符号动作序列，并通过逆抽象与采样式运动规划细化每个动作的头、尾轨迹；若某个低层细化不可行，规划器回溯并重新选择高层计划或连续端点，直到获得全部可执行的技能链。

直观地说，黑盒技能只负责完成自己擅长的局部交互，却未必知道怎样从任意姿态开始，也未必以方便下一技能接续的姿态结束。CIP相当于给每个技能添加“进场”和“退场”动作，而TASP负责同时安排技能顺序及这些进退场轨迹，从而在不要求不同技能的启动集与终止集直接重合、也不要求了解黑盒策略内部控制规律的前提下组合异构技能。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构建混合机器人规划问题

将环境表示为一阶逻辑符号状态与连续几何状态的组合，并将问题写成混合机器人规划元组；每个对象中心技能表示为含对象参数、启动条件、终止条件和策略的参数化option。符号层描述诸如附着、洁净与否等关系，连续层保留位姿、关节配置和碰撞约束。

<div class="method-step__io" markdown="1">

**输入**：对象集合、机器人集合、物体与机器人位姿、机器人关节配置、附着关系、对象属性观测、初始状态、目标状态，以及已有机器人技能集合。<br>
**输出**：混合规划模型及可由规划器调用的参数化技能库。

</div>

**直观理解**：这一步把“世界里有什么、机器人现在怎样、最终要达到什么、机器人会哪些本领”放进统一模型。技能可以来自不同控制机制，规划器只依赖其调用接口和条件，而不必展开其内部实现。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 用运动学投影提取技能的可规划接口

应用运动学投影λ，去除对象特定的非空间观测条件，得到仅由空间位姿和机器人配置定义的启动与终止运动学包络。该包络作为运动规划可直接搜索的连续目标区域，而完整条件仍用于判断技能在语义上是否适用。

<div class="method-step__io" markdown="1">

**输入**：技能的完整启动条件与终止条件，其中可能同时包含机器人和物体位姿、机器人配置及颜色、温度、洁净度等非空间属性。<br>
**输出**：每个技能的启动运动学包络和终止运动学包络。

</div>

**直观理解**：普通运动规划器能处理“机械臂要到哪里、是否碰撞”，却不能靠移动直接让白板变干净。投影因此只取出可由几何运动实现的部分，同时不把洁净度等真正的任务条件错误地当成几何目标。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 将黑盒技能封装为CIP

为技能构造头部运动计划h，使机器人从当前不满足技能启动条件的配置到达满足启动运动学包络的配置；执行原技能策略π后，再构造尾部运动计划t，使机器人离开终止运动学包络并回到可继续自由空间运动的配置。头、技能策略和尾共同组成一个CIP。

<div class="method-step__io" markdown="1">

**输入**：原始技能、其运动学投影，以及当前场景中的机器人和物体状态。<br>
**输出**：具有“头部轨迹—技能策略—尾部轨迹”结构的可组合技能单元。

</div>

**直观理解**：头部轨迹负责把机器人摆到技能能工作的姿态，黑盒策略完成擦、开、舀或涂等接触操作，尾部轨迹再把机器人撤出局部交互区域。这样相邻技能不需要恰好在同一姿态交接。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 通过实体抽象和ATAM联合搜索任务序列与连续细化

实体抽象把每个CIP转换成高层动作，并离散化表示其终点配置、头尾运动计划和技能策略等参数；修改后的ATAM先由符号规划器提出高层计划，再用逆抽象Γ把动作转成低层运动规划问题，通过采样式运动规划器寻找无碰撞的头尾轨迹和兼容端点。黑盒策略对应的动作部分直接调用策略，而不是像传统TAMP那样全部交给运动规划器细化；若任一细化失败，则通过回溯重新计算计划或参数。

<div class="method-step__io" markdown="1">

**输入**：CIP集合、初始符号状态、目标条件，以及场景几何和碰撞信息。<br>
**输出**：每个高层动作均具有有效低层细化的长时程计划，即依次排列的头部轨迹、黑盒或运动规划技能、尾部轨迹。

</div>

**直观理解**：高层规划先决定“做什么、按什么顺序做”，低层规划再检查“机器人实际上能不能到达这些姿态”。如果某个看似合理的步骤因碰撞或技能入口太窄而不可执行，系统会退回并换一条计划，而不是盲目执行。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 混合机器人规划问题及其解

$$
\mathcal{M}=\langle\mathcal{U},\mathcal{V},\mathcal{X},\mathcal{A},x_i,\mathcal{X}_g\rangle,\qquad [a_1,\ldots,a_n]:x_i\mapsto x_n\in\mathcal{X}_g
$$

**符号说明**

- $\mathcal{M}$：混合机器人规划问题。
- $\mathcal{U}=\mathcal{O}\cup\mathcal{R}$：规划对象的全集，由对象集合$\mathcal{O}$和机器人集合$\mathcal{R}$组成。
- $\mathcal{V}$：描述空间函数、机器人配置、附着关系和对象属性观测等内容的逻辑词汇表。
- $\mathcal{X}$：包含连续几何信息和高层属性信息的环境状态空间。
- $\mathcal{A}$：可用机器人技能的集合。
- $x_i$：初始环境状态。
- $\mathcal{X}_g$：满足任务目标的状态集合。
- $a_1,\ldots,a_n$：规划器选择并依次执行的技能序列。
- $x_n$：执行完整技能序列后到达的最终状态。

<div class="equation-explanation" markdown="1">

**直观理解**：该定义把目标规定为寻找一串技能，使系统从初态进入任一目标状态。它比传统TAMP更一般：动作不必都能化为关节空间中的运动规划，也可以是依赖反馈、持续接触或学习控制器的技能。<br>
**原文位置**：Section III, Definition 3

</div>

</div>

<div class="equation-block" markdown="1">

#### 可组合交互原语定义

$$
\tilde{a}=\langle\Theta_a,\mathcal{I}_a,\beta_a,\pi_a,h,t,\lambda\rangle,\qquad h:x\not\models\mathcal{I}_a\rightarrow x'\models\lambda(\mathcal{I}_a),\qquad t:y\models\beta_a\rightarrow y'\not\models\lambda(\beta_a)
$$

**符号说明**

- $\tilde{a}$：由原始对象中心技能封装得到的CIP。
- $\Theta_a$：技能作用的对象参数集合。
- $\mathcal{I}_a$：技能的完整启动条件。
- $\beta_a$：技能的完整终止条件。
- $\pi_a$：技能的控制策略，可以作为黑盒调用。
- $\lambda$：运动学投影，删除对象特定的非空间观测条件，保留位姿和机器人配置约束。
- $h$：头部运动计划，使机器人到达满足启动条件之运动学包络的配置。
- $t$：尾部运动计划，使机器人从满足技能终止条件的状态退出终止运动学包络。
- $x,x'$：执行头部运动前后的状态；x'满足投影后的启动条件。
- $y,y'$：执行尾部运动前后的状态；y满足技能终止条件，y'已离开投影后的终止区域。
- $\models$：状态满足给定逻辑条件。
- $\not\models$：状态不满足给定逻辑条件。

<div class="equation-explanation" markdown="1">

**直观理解**：该式给黑盒技能加上可由运动规划器求解的入口和出口。关键不是要求前一技能的终止集与后一技能的启动集相交，而是允许机器人先退出前一技能的局部区域，再在自由空间中移动到后一技能的启动包络。<br>
**原文位置**：Section IV-A, Definition 4

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。TASP是规划与技能组合框架，所给章节没有定义端到端训练损失，也不要求联合训练已有技能；$π_a$可由行为克隆、强化学习、力控制、轨迹回放或运动规划预先获得，但其训练目标和训练数据均由各技能自身决定，原文未明确报告统一优化目标。TASP在线求解的是离散任务序列、技能参数、头尾端点和无碰撞运动细化的可行性，而非通过梯度最小化某个损失函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 对象中心技能与混合状态模型**

环境由对象集合与机器人集合组成：物体和机器人具有SE(3)位姿，机器人还具有关节配置与物体附着集合，对象属性由分类器集合表示。技能a被建模为参数化option〈$Θ_a, I_a, β_a, π_a$〉，其中$Θ_a$是对象参数，$I_a$和$β_a$是一阶逻辑启动与终止条件，$π_a$是实际控制策略；策略可来自运动规划、行为克隆、强化学习、力控制或其他黑盒实现。

> 直观理解：这一接口把技能的“什么时候能开始、什么时候算结束、执行时调用什么控制器”与其内部算法分开。因而规划器能够统一安排来源不同的技能，同时保留物体是否干净等非几何任务状态。

**2. 可组合交互原语（CIP）**

CIP在原技能接口上增加运动学投影λ、头部运动计划h和尾部运动计划t。λ把完整条件映射为空间约束；h到达启动包络，t从技能终止状态退出终止包络，从而满足技能可达、技能后可返回自由空间以及可为技能选择兼容入口和出口这三个规划需求。

> 直观理解：CIP不是重新训练技能，而是在技能外面增加标准化的接驳层。它解决的核心问题是：两个技能在符号上前后相容，并不意味着前一技能结束时的真实机器人姿态能直接启动后一技能。

**3. 基于实体抽象的修改版ATAM分层规划器**

实体抽象把连续CIP表示成具有离散参数的高层动作；ATAM交替调用符号规划、逆抽象和采样式运动规划，并以回溯搜索排除无法低层细化的高层候选。相较原有ATAM，本文的关键修改是：细化高层动作参数时允许直接调用黑盒技能策略，而不假设每个动作都能归约为纯运动规划。

> 直观理解：该模块把离散的任务顺序与连续的姿态、轨迹选择绑在同一次搜索中。它尤其用于处理技能条件形成的狭窄兼容区域，因为只随机连接技能前后状态可能很难找到可行组合。

**训练与推理**

训练阶段：框架本身无统一训练流程，假设对象中心技能已经存在，并为每个技能提供对象参数、启动条件、终止条件和可调用策略；若策略由学习得到，其具体训练过程在所给章节中未展开。规划与执行阶段：系统读取初始环境状态和目标条件，将技能封装为CIP并通过实体抽象形成高层动作；符号规划器提出候选技能序列，逆抽象Γ为每个动作生成低层问题，采样式运动规划器选择技能入口、出口并求解头尾无碰撞轨迹。若任何动作无法细化，ATAM进行回溯并重新选择高层计划或连续参数；找到完整解后，机器人按“头部运动—技能策略—尾部运动”的顺序执行各CIP。所给章节说明CIP也支持执行时调整，但未给出具体在线重规划触发条件或更新算法，因此这些细节原文未明确报告。

**复现信息**

公平理解方法所需的实现信息包括：高层状态使用一阶逻辑表示，连续几何部分包含物体和机器人基座的SE(3)位姿、机器人关节配置以及附着关系；技能必须暴露参数、启动条件、终止条件和策略接口。规划器采用Shah等人的ATAM与实体抽象，并将ATAM修改为在动作细化中调用黑盒策略；头尾连接由采样式运动规划器求解，文中以RRT和PRM说明此类规划器，但所给方法章节未明确指定最终实验实现固定采用哪一种。具体采样预算、碰撞检测器、符号规划器名称、回溯终止条件和控制频率在所给节选中均未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 未使用标准离线数据集，也未报告训练集、验证集或测试集划分。第一项评测是KUKA双臂机器人的真实厨房操作场景：初始物体为刀、封闭的花生酱罐和面包片，目标是在面包上涂抹花生酱；该场景用于检验双臂系统能否串联运动规划与阻抗控制下的轨迹回放技能。
- 第二项评测是Boston Dynamics Spot的真实多房间移动操作场景：机器人需从抽屉中取得白板擦，穿过一扇会遮挡白板的门，将白板擦临时放到文件柜上，关门后再取回白板擦并擦除白板；该场景用于检验长时程、导航—操作交替及非单调任务规划。
- 感知与环境模型来自现场采集，而非公开数据集。双臂平台使用RealSense D455、CNOS分割和FoundationPose进行物体六自由度位姿估计；Spot预先通过遥操作建立占据栅格地图，并用AprilTag估计物体位姿。门和抽屉等关节物体不提供完整运动学模型，而以技能执行前后的静态模型及技能运动包络表示。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

原文未明确报告，或这里不需要额外前置概念。

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### KUKA双臂花生酱涂抹任务

<div class="result-value" markdown="1">

规划器给出的方案依次包含Grasp(j0)、Open(j0)、Grasp(k0)、Scoop(k0,j0)和Spread(k0,b0)，把基于运动规划的抓取与阻抗控制下的轨迹回放技能组合成一条完整任务链。作者据此将该实验作为TASP能够解决双臂混合技能规划问题的实例，但原文未报告重复次数或成功率。

</div>

该结果说明系统至少展示了一次从符号目标到真实双臂技能序列的端到端执行，而且后续动作依赖前序动作产生的状态，例如罐子必须先被抓取并打开，刀必须先被抓取才能舀取和涂抹。它并不能证明系统相对于传统TAMP或手工技能编排更可靠，也不能量化对感知误差、技能失败或物体位置变化的鲁棒性。

<div class="result-source" markdown="1">

来源：第V-B.1节，Bimanual Manipulation Experiment；图3(d)–(e)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Finally, the robot executes Scoop(k0, j0) to scoop peanut butter onto the knife, then spreads it onto the bread using Spread(k0, b0) (Figs. 3(d) and 3(e)).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Spot多房间移动操作任务的计划长度与层级结构

<div class="result-value" markdown="1">

TASP生成的解包含14个高层动作，其中7个是GoTo导航技能，并与开抽屉、开门、抓取、放置、关门和擦除等操作技能交替出现。这表明实验方案覆盖了较长的导航—操作混合链条，而不是单次抓取或单一控制器测试。

</div>

14步计划反映了任务的长时程性质：机器人必须多次在房间、抽屉、门、文件柜和白板之间移动，并让每个操作建立下一步所需条件。这个数字只描述作者展示的计划长度，不是性能分数；由于没有其他规划器的计划长度、求解时间或执行成功率，不能据此断言TASP生成了更短、更快或更可靠的方案。

<div class="result-source" markdown="1">

来源：第V-B.2节，Mobile Manipulation Experiment

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Given this task, the solution plan produced by our planner includes 14 high-level actions, seven of which are GoTo(?location) navigation skills alternating with manipulation skills.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Spot异构技能集上的非单调任务执行

<div class="result-value" markdown="1">

机器人先把白板擦从抽屉中取出并带入目标房间，但由于开着的门会挡住白板，必须先把白板擦临时放到文件柜上，再执行学习得到的CloseDoor技能，随后重新抓取白板擦并用力控制Erase技能擦除白板。该流程展示了运动规划、导航、轨迹回放、学习策略、现成黑盒技能和力控制技能在同一任务中的组合。

</div>

关键不只是技能数量多，而是任务具有非单调结构：开门是进入房间的必要步骤，之后却必须关门才能接近白板；临时放下白板擦也不是直接推进最终目标，却为关门和后续擦除创造条件。因此，该案例支持系统能表示并执行含中间状态回退的计划。它仍只是定性演示，不能证明所有黑盒技能都可无条件接入，也没有隔离CIP桥接、在线调整或对象中心失败推理各自的贡献。

<div class="result-source" markdown="1">

来源：第V-B.2节，Mobile Manipulation Experiment；图4(e)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The robot then runs CloseDoor(d1) to close the door and make the board accessible (Fig. 4(e)).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验缺少基线、消融和统一量化指标。原文未报告任务成功率、重复试验次数、规划时间、执行时间、路径长度、技能失败率或恢复成功率，因此无法判断TASP相较传统TAMP、纯行为编排或不使用CIP的版本是否更有效，也无法估计结果的方差与可复现性。
- 评测规模仅覆盖两个真实场景和两种机器人平台，且依赖预先建立的地图、已知碰撞模型、纹理网格或AprilTag等结构化感知条件。虽然技能来源多样，但当前证据不足以说明系统对新任务、新对象、显著感知误差、动态环境以及此前未建模的黑盒技能具有普遍泛化能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。

**实验想回答的问题**

- TASP能否在真实机器人上把运动规划、轨迹回放、力控制、行为克隆策略和现成黑盒能力统一编排为可执行的长时程任务方案？
- 面对具有非单调结构的移动操作任务——即机器人必须暂时改变或撤销某些中间状态才能最终达成目标——TASP能否生成并执行交替包含导航与操作技能的多阶段计划？

**实验实现**

每次实验的输入都是PDDL风格的符号规划问题〈𝒰, $s_i$, 𝒢〉，分别表示对象全集、初始符号状态和目标条件；低层初始状态由已知物体位姿与碰撞几何组成的运动学树表示。规划器需要产生可在机器人上执行并满足𝒢的技能序列。双臂平台由两台KUKA LBR iiwa 7 R800组成，提供Grasp、Open、Scoop和Spread四类技能，其中Grasp使用CBiRRT/OpenRAVE运动规划，其余技能采用物体相对的末端轨迹回放与阻抗控制。Spot提供七类技能：MoveIt!/OMPL实现的Pick与Place、A*和Spot SDK实现的GoTo、轨迹回放式OpenDrawer、力控制Erase、由真实示范训练的Action Chunking Transformer关门策略CloseDoor，以及由Gemini Robotics-ER 1.5检测门把手后调用Spot内置能力的黑盒OpenDoor。规划、学习策略控制和感知运行在配备RTX 4090的外部计算机上。原文仅报告两次真实机器人任务的定性执行过程，没有说明重复试验次数、成功率、规划时间、执行时间、失败次数或统计检验，也没有设置对照方法。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- Spot任务是最有解释力的定性案例：开门使机器人能够进入目标房间，却同时让门体遮挡白板；机器人因而不能简单地持续增加“已完成”条件，而要先取得白板擦、进入房间、把白板擦放到文件柜、关门、再次抓取，最后执行力控制擦除。该过程说明规划器需要推理门、白板擦和机器人位置之间的对象级状态关系，并在符号层面安排暂存与重新抓取。作者将其视为非单调任务结构的证据；但节选没有报告执行中是否发生技能失败、CIP如何在线修正，也没有提供失败恢复轨迹。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The core contribution is a hierarchical robot planner that composes heterogeneous black-box skills for long-horizon manipulation.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`97badbc27b0e0a188b66143b097f2bc64c38732293e7950679bb9288d31ab00b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
