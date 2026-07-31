---
title: "[论文解读] TiPToP: A Modular Open-Vocabulary Robot Manipulation System That Plans"
description: "[arXiv 2603.09971][机器人 / 具身智能] 原文未明确报告。"
arxiv_id: "2603.09971"
announcement_date: "2026-07-30"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.746727+00:00"
source_sha256: "be7f59c567fd2b5fad49cd7eb114191b6ff5143d355bd2e23b449f787c889b8b"
tags:
  - "机器人 / 具身智能"
  - "开放词汇机器人操作"
  - "任务与运动规划"
  - "基础模型"
  - "模块化机器人系统"
  - "零样本迁移"
  - "三维场景表示"
  - "视觉语言动作模型"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2603.09971</p>

# TiPToP: A Modular Open-Vocabulary Robot Manipulation System That Plans

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> William Shen, Nishanth Kumar, Sahit Chintalapudi, Ryan Lindeborg, Jie Wang, Christopher Watson, Edward Hu, Jing Cao, Dinesh Jayaraman, Leslie Pack Kaelbling, Tomás Lozano-Pérez</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2603.09971v2) · [PDF 下载](https://arxiv.org/pdf/2603.09971v2) · **关键词** 开放词汇机器人操作, 任务与运动规划, 基础模型, 模块化机器人系统, 零样本迁移, 三维场景表示, 视觉语言动作模型<br>
**项目页**: [https://tiptop-robot.github.io](https://tiptop-robot.github.io)  

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

原文未明确报告。

**不用术语来说**：原文未明确报告。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 原文未明确报告。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于开放词汇机器人操作研究：系统需要从视觉观测与自然语言指令中识别任意类别的目标物体，并生成机器人可执行的操作。其关键难点是把视觉基础模型提供的语义、深度、分割和抓取信息，转化为同时满足任务逻辑、机器人运动学与避碰约束的动作序列。TiPToP采用模块化路线，将感知、任务与运动规划、执行分开，并以预训练模型和测试时搜索代替针对特定机器人收集操作数据后进行端到端训练。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**任务与运动规划（Task and Motion Planning, TAMP）**

TAMP联合求解离散的“做什么”与连续的“怎么动”：前者决定抓取、放置等操作顺序，后者计算满足运动学和避碰约束的关节轨迹。本文使用GPU并行、基于优化的cuTAMP来搜索可行操作计划。

</div>
<div class="concept-item" markdown="1">

**开放词汇感知（open-vocabulary perception）**

开放词汇感知允许系统依据自然语言描述检测和定位训练类别表之外的物体，而不局限于预先固定的标签集合。本文组合视觉语言模型、深度估计、分割和抓取预测，建立以物体为中心的三维场景表示。

</div>
<div class="concept-item" markdown="1">

**视觉—语言—动作模型（Vision-Language-Action model, VLA）**

VLA通常以图像和语言为条件，端到端预测机器人动作，并通过大规模机器人示范数据学习控制。它能直接从像素执行任务，但往往需要针对机器人形态的数据训练，且内部耦合使故障原因较难定位。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入为一对立体RGB图像和自然语言指令；系统首先估计深度、检测并分割相关物体、预测六自由度抓取位姿，形成物体中心的三维场景表示，然后联合规划符号操作序列与连续无碰撞运动，最终输出带夹爪命令的机器人关节轨迹，并由关节阻抗控制器跟踪执行。目标设置是零样本部署：不使用机器人训练数据，也不针对具体物体、场景或机器人形态重新训练。受支持的机器人需具备相机、夹爪、URDF机器人描述以及轨迹跟踪控制器，部署时仍需完成相机标定；因此“任意机器人”并非无条件成立。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{L}$**

输入给系统的自然语言任务指令。

</div>
<div class="notation-item" markdown="1">

**$\pi_{0.5}\text{-DROID}$**

用于对比的视觉—语言—动作模型；原文称其在350小时DROID机器人示范数据上进行了微调。

</div>
<div class="notation-item" markdown="1">

**$SE(3)$**

三维空间刚体位姿的数学空间，可用于表示抓取器相对于物体或世界坐标系的位置与朝向；正文以“6-DoF grasp poses”描述这一类输出，但未在所给章节中显式写出该符号。

</div>

</div>

**直接相关的工作**

- **Curtis et al.：学习感知模块与PDDLStream结合的未知物体长时程操作系统**: 这是与TiPToP最接近的规划式系统之一，同样把学习感知接入任务与运动规划。TiPToP的主要区别是采用GPU并行、基于优化的cuTAMP，而非采样式PDDLStream，并进一步使用更大规模的基础模型，将系统封装为可跨机器人形态部署的完整流水线。
- **$\pi_{0.5}\text{-DROID}$**: 这是本文的核心端到端VLA对照方法，以350小时DROID示范数据微调。它代表依赖机器人数据学习像素到动作映射的路线；TiPToP则不使用机器人训练数据，通过可替换的感知、规划和执行模块完成任务，并可把失败定位到具体模块。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

TiPToP将语言条件机器人操作实现为“感知一次、规划整段、开环执行”的模块化系统。输入是自然语言指令、标定腕部双目相机在初始时刻采集的RGB图像、机器人初始关节状态及已知运动学；系统先并行恢复三维几何与理解任务语义，再把二者合并成带物体网格、候选抓取和符号目标的对象中心场景，随后由GPU并行任务与运动规划器cuTAMP联合搜索动作顺序及连续运动参数，最终输出并执行包含关节位置、速度和夹爪状态的完整定时轨迹。系统不使用机器人训练数据，FoundationStereo、M2T2、Gemini Robotics-ER 1.5、SAM-2等预训练模型主要在推理时直接组合使用。
直观地说，TiPToP不是让一个神经网络边看边决定下一小步，而是先拍一张立体“工作台快照”，辨认物体并建立三维模型，再像解约束题一样决定先搬什么、从哪里抓、放到哪里以及机械臂如何避障。其优势是能显式处理遮挡物、动作先后关系和碰撞约束，也能把错误定位到感知、抓取、规划或执行模块；代价是计划执行期间不再观察环境，因此物体移动、抓取打滑或建模误差无法在线纠正。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 初始观测与三维几何恢复

FoundationStereo从双目图像预测与左图对齐的稠密深度图\(D\)，系统再用内参反投影为相机坐标点云，并通过外参与机器人正向运动学变换到世界坐标系。M2T2在完整场景点云上预测并排序六自由度抓取姿态，使候选抓取能够考虑周边几何，但此时尚不保证无碰撞。

<div class="method-step__io" markdown="1">

**输入**：自然语言指令\(\mathcal{L}\)、初始关节构型\(q_0\)、标定腕部双目图像\(\mathbf{o}_0=(I_0^{\mathrm{left}},I_0^{\mathrm{right}})\)，以及相机内参\(K\)、双目基线\(b\)和相机到末端执行器的外参\(T_{\mathrm{cam}}^{\mathrm{ee}}\)。<br>
**输出**：世界坐标系中的稠密场景点云、深度图和场景级候选抓取集合。

</div>

**直观理解**：这一步相当于把双目照片变成一张可测量距离的三维地图，并在地图上标出若干可能的“下手位置”。抓取只是候选答案，之后仍要由规划器结合碰撞和任务要求筛选。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 语义理解与对象中心场景构建

Gemini Robotics-ER 1.5在一次查询中联合输出物体标签、二维边界框和由谓词合取构成的符号目标\(\mathcal{G}\)，SAM-2再依据各边界框生成像素级掩码。系统用掩码切分点云、重建逐物体网格，并通过最近邻查询把抓取分配给具体物体；默认采用保守而廉价的凸包网格，也可用RecGen进行较高成本的完整形状补全。

<div class="method-step__io" markdown="1">

**输入**：左相机RGB图像、自然语言指令、世界坐标点云及场景级候选抓取。<br>
**输出**：对象中心三维场景表示：桌面、逐物体身份与网格、分配到各物体的候选抓取，以及如\(\texttt{On}(a,b)\)所表达的目标关系。

</div>

**直观理解**：几何分支回答“东西在哪里、形状多大”，语义分支回答“它是什么、指令指的是谁”。合并后，规划器看到的不再是一堆无名点，而是“这个饼干盒要放到那个托盘上”这样的可操作场景。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 任务与运动联合规划

cuTAMP先用PDDL风格符号规划器枚举计划骨架，即尚未确定抓取、放置、关节构型和轨迹参数的动作序列；随后为每个骨架批量采样粒子，并在GPU上联合优化抓取/放置姿态和机器人构型，使其满足避碰、稳定放置及运动学可行性。对满足约束的粒子，cuRobo补全无碰撞、带时间参数的运动轨迹；若直接抓取被障碍物阻挡，搜索可选择包含“先移开障碍物”的较长骨架。

<div class="method-step__io" markdown="1">

**输入**：对象中心场景、机器人运动学模型、初始构型\(q_0\)和符号目标\(\mathcal{G}\)。<br>
**输出**：完整操作计划\(\{(q_t,\dot q_t,g_t)\}_{t=0}^{T}\)，其中包含各时刻的关节位置、关节速度和二值夹爪命令。

</div>

**直观理解**：计划骨架类似“先拿起A，再把A放到B上”的步骤清单，粒子则是这些步骤的许多具体执行方案。系统同时尝试大量方案，先淘汰会碰撞、够不到或放不稳的方案，再为可行方案生成机械臂实际行走的路径。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 定时轨迹开环执行

自定义关节空间阻抗控制器跟踪\(q_t\)和\(\dot q_t\)，并按计划执行\(g_t\)；论文称调参后在高速运动时可将末端跟踪误差控制在5 mm以内。整个计划开环执行，不利用执行过程中的新视觉观测进行重规划。

<div class="method-step__io" markdown="1">

**输入**：规划得到的定时关节轨迹与夹爪命令。<br>
**输出**：机器人对场景实施抓取、搬运、放置等动作，使最终物体关系满足符号目标。

</div>

**直观理解**：控制器像严格按乐谱演奏一样复现整段计划，精确跟踪能避免很小的位置偏差破坏抓取。它不会边执行边重新看场景，因此静态环境中简单高效，但遇到物体滑动或抓空时不能立即补救。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 语言条件操作策略接口

$$
a_t=\pi(\mathbf{o}_t,q_t\mid\mathcal{L})
$$

**符号说明**

- $a_t$：时刻\(t\)输出的机器人动作；在TiPToP中，初始输出是整段定时轨迹。
- $\pi$：从观测和机器人状态生成动作的策略；TiPToP用由感知、规划和执行模块组成的测试时规划系统来实例化它。
- $\mathbf{o}_t$：时刻\(t\)来自一个或多个相机的RGB观测。
- $q_t$：时刻\(t\)的机器人关节构型。
- $\mathcal{L}$：指定目标任务的自然语言指令。

<div class="equation-explanation" markdown="1">

**直观理解**：该式统一了端到端策略与TiPToP的输入输出：二者都依据视觉、关节状态和语言产生动作，但实现方式不同。端到端模型以较高频率连续输出短动作块，TiPToP则在\(t=0\)观察一次并规划完整轨迹，因此比较的是同一任务接口下的两种决策范式。<br>
**原文位置**：第III节 Problem Formulation and System Overview

</div>

</div>

<div class="equation-block" markdown="1">

#### 点云从相机坐标系变换到世界坐标系

$$
\mathbf{p}^{\mathrm{world}}=T_{\mathrm{ee}}^{\mathrm{world}}T_{\mathrm{cam}}^{\mathrm{ee}}\mathbf{p}^{\mathrm{cam}},\qquad T_{\mathrm{ee}}^{\mathrm{world}}=\operatorname{FK}(q_0)
$$

**符号说明**

- $\mathbf{p}^{\mathrm{cam}}$：由深度图和相机内参反投影得到的相机坐标系三维点。
- $\mathbf{p}^{\mathrm{world}}$：同一三维点在机器人世界坐标系中的位置。
- $T_{\mathrm{cam}}^{\mathrm{ee}}$：从相机坐标系到末端执行器坐标系的已知外参变换。
- $T_{\mathrm{ee}}^{\mathrm{world}}$：从末端执行器坐标系到世界坐标系的变换。
- $\operatorname{FK}(q_0)$：在初始关节构型\(q_0\)上计算的机器人正向运动学。

<div class="equation-explanation" markdown="1">

**直观理解**：深度模型得到的点最初以相机为参照，规划器却需要知道它们相对机器人和工作台的位置。该式依次利用相机安装标定和机械臂当前姿态完成坐标变换，使物体网格、抓取姿态及碰撞检查处于同一个世界坐标系。<br>
**原文位置**：第IV-A节 3D Vision Branch，Unprojecting depth to 3D

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。TiPToP没有提出端到端训练损失，也不使用机器人示范数据训练系统；其核心计算发生在测试时，包括预训练基础模型推理、计划骨架搜索、连续参数采样与约束优化，以及无碰撞轨迹规划。原文说明cuTAMP通过可微优化联合调整放置姿态和机器人构型，使碰撞规避、稳定放置与运动学可行性约束得到满足，但所给章节未明确列出统一的标量目标函数，因此不应据此虚构损失公式。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 感知模块：三维视觉与语义双分支**

三维视觉分支以FoundationStereo生成深度，以标定参数和正向运动学将点云置于世界坐标系，并由M2T2产生场景级六自由度抓取。语义分支以Gemini Robotics-ER 1.5联合检测物体并把语言指令落地为符号目标，再由SAM-2细化分割；两分支最终合并为逐物体网格和抓取集合。默认凸包模式通过将物体点向下投影至该物体最低观测点后计算凸包，便于得到封闭且通常偏保守的碰撞几何；复杂形状可改用RecGen补全。

> 直观理解：规划既需要“看懂”指令，也需要可用于计算碰撞的三维模型，单独依靠二维识别或点云都不够。凸包速度快且倾向于留出安全余量，但会把香蕉等凹形物体估得过于饱满；形状补全更准确，却明显增加计算成本。

**2. 规划模块：cuTAMP与cuRobo**

cuTAMP把离散任务决策与连续几何参数统一处理：符号规划枚举不同动作顺序和辅助动作，粒子初始化从M2T2或启发式俯视抓取器采样抓取，并采样放置姿态、逆运动学构型；可微优化并行修正参数以满足碰撞、稳定性和运动学约束，最后由cuRobo生成定时无碰撞轨迹。为适应不完美的真实场景重建，作者忽略初始状态中的部分伪碰撞、增加运动规划尝试并逐步放宽碰撞阈值，同时用有向包围盒扩展任意朝向支撑面的放置代价。

> 直观理解：该模块的关键不只是算一条机械臂路径，而是同时决定“做哪些动作、按什么顺序、从哪里抓和放、怎么移动”。这使系统能发现最短的直接方案不可行，并自动改用先清障再操作的方案；针对感知误差的扩展则避免略显膨胀的网格让规划器误判所有方案都发生碰撞。

**3. 执行模块：关节空间阻抗控制**

执行器跟踪规划器输出的关节位置与速度，并同步控制二值夹爪状态。作者因DROID默认Polymetis控制器不能足够精确地跟踪定时轨迹而实现自定义关节阻抗控制器；当前版本在首次感知后不再闭环观测或重规划。

> 直观理解：任务规划只有在实际机械臂准确走到计划位置时才成立，亚厘米误差就可能使夹爪错过目标。专用控制器提高了计划的可兑现性，但它不能弥补抓取打滑、物体被碰动或初始三维模型错误。

**训练与推理**

训练阶段：TiPToP自身没有机器人数据训练流程，直接组合冻结或预训练的FoundationStereo、M2T2、Gemini Robotics-ER 1.5、SAM-2，并可选使用RecGen；控制器增益由作者调节，cuTAMP的真实部署扩展属于算法与工程修改，而非学习一个端到端策略。
推理阶段：机器人先移动到能良好覆盖工作区的捕获姿态，仅采集一次标定双目图像。三维分支恢复深度、世界点云和候选抓取，语义分支识别物体、分割实例并将语言转成符号目标；系统融合两者形成对象中心场景。cuTAMP枚举计划骨架，为每个骨架批量初始化连续参数粒子，按初始可行性排序后并行优化；找到满足约束的粒子时，cuRobo求解剩余的无碰撞定时轨迹。最后控制器开环执行整段轨迹，不再接收新的视觉反馈；若某个物体没有M2T2抓取预测，规划阶段改用启发式四自由度俯视抓取采样器。

**复现信息**

公平解释该方法需要注意四点。第一，系统依赖标定腕部双目相机、已知内外参、双目基线和准确机器人运动学，并假设捕获姿态能清楚观察工作区；这不是仅凭任意单目图像工作的系统。第二，默认物体几何采用快速凸包，桌面由RANSAC拟合主平面；凸包通常利于保守避碰，却可能过度近似凹形物体或因遮挡低估几何，可选RecGen形状补全约需每个物体10秒（RTX 3090），但可跨GPU并行。第三，cuTAMP和cuRobo均利用GPU并行，实际部署版本包含对伪初始碰撞、碰撞阈值和任意朝向放置面的专门处理，这些修改是从理想仿真规划迁移到真实感知结果的重要条件。第四，执行依赖高精度自定义关节阻抗控制器；作者报告高速时末端跟踪误差在5 mm以内，但系统仍为开环，静态场景与可靠抓取是其成功的重要前提。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 受控对比任务集：共28个桌面场景，分布在三个评测环境——IsaacSim仿真5项任务、TiPToP开发者使用的DROID实体平台8项任务、外部评测团队操作的另一套DROID平台15项任务。场景按难度划分为简单、干扰物、语义和多步骤四类，总计对每个系统执行165次试验；它主要检验跨环境、跨任务复杂度的真实操作能力。
- MolmoSpaces：大规模家庭操作基准。论文在DROID平台上运行其中9项抓取及抓取—放置任务，每项1,000个episode；由于TiPToP暂不支持开、关操作，相关任务被排除。该基准将使用MolmoSpaces或MolmoBot仿真数据训练的方法归为分布内方法，将未使用这些数据的方法归为非分布内方法，用于检验系统在独立基准上的泛化能力。
- 四类受控场景子集：简单任务是无干扰物的单步抓取—放置；干扰物任务要求在杂乱环境中只操作目标；语义任务要求理解指代表达并运用常识或物理推理；多步骤任务要求安排多个动作并处理装箱、障碍移除等约束。该分组不是额外训练集，而是用于分析性能是否随推理和规划难度变化。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**成功率（SR）**

二元任务成功比例；一次试验只有在完成整个任务时才计为成功。类别和总体结果通过汇总成功次数计算。 （越高越好，因为它直接衡量完整完成用户指令的可靠性。）

</div>
<div class="metric-item" markdown="1">

**任务进度（TP）**

按照每项任务预先定义的子目标计算的细粒度完成程度。它能区分完全失败与已经完成大部分步骤、仅在某一步失败的试验。 （越高越好，因为更高数值表示完成了更多任务子目标，但它不能替代完整成功率。）

</div>
<div class="metric-item" markdown="1">

**成功试验平均完成时间（Time）**

只对成功试验统计从规划到执行结束的平均时间；TiPToP的感知与规划耗时包含在总时间中，并另以Plan列报告。 （越低越好，因为相同成功条件下耗时更短意味着系统效率更高；但该指标排除失败试验，不能单独反映整体可靠性。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 28个受控场景、三个环境、共165次试验的总体比较

<div class="result-value" markdown="1">

作者报告TiPToP取得98/165的完整成功次数和74.6%的平均任务进度，而$π_{0.5}-DROID$分别为55/165和52.4%；因此，在该受控任务集合上，TiPToP的总体完整成功数高43次，任务进度高22.2个百分点。

</div>

这表明无需机器人示范训练的模块化系统，在所测开放式桌面任务上整体优于使用350小时DROID示范微调的端到端VLA。结果支持“预训练感知模型加显式规划具有竞争力”，但不能证明TiPToP对所有机器人形态或所有家庭任务都更强，也不能排除任务选择、提示设置和硬件差异的影响。

<div class="result-source" markdown="1">

来源：第VII-A节，表I后的结果分析

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Over 165 trials, TiPToP achieves a higher overall success rate (98/165 vs. 55/165) and task progress (74.6% vs. 52.4%) than π 0.5 $\pi_{0.5}$ -DROID.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 按任务复杂度划分的简单、干扰物、语义和多步骤场景

<div class="result-value" markdown="1">

简单任务中$π_{0.5}-DROID$的成功次数略高，为27/40对22/40，但TiPToP的任务进度更高；随着任务从单步操作扩展到干扰物筛选、语义指代和多步骤规划，作者报告TiPToP在后三类场景中均表现更好。表I给出的类别成功次数分别为：干扰物27/45对12/45、语义26/40对10/40、多步骤23/40对6/40，均为TiPToP领先。

</div>

这一分层结果比单一总体平均数更能说明优势来源：TiPToP并非在最简单的抓取—放置上全面占优，其收益主要出现在需要选择相关物体、解释自然语言或安排动作顺序的场景。这与显式任务与运动规划的设计目标一致，但该分组不是严格的组件消融，因而不能仅凭这些结果断定性能提升完全来自规划器。

<div class="result-source" markdown="1">

来源：第VII-A节；类别汇总见表I

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On simple pick-and-place the two are comparable, with π 0.5 $\pi_{0.5}$ -DROID slightly ahead on success rate (27/40 vs. 22/40) and TiPToP ahead on task progress.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 六个仿真或实体场景上的成功试验完成时间比较

<div class="result-value" markdown="1">

TiPToP在六个被报告的场景中有五个完成得更快，另一个与$π_{0.5}-DROID$持平；作者指出，单步任务的总完成时间通常约为基线的一半。表II还将TiPToP的感知和规划时间计入总时间，因此该效率优势并非通过忽略规划开销得到。

</div>

显式规划并未必然造成更慢的端到端执行；在这些成功试验中，TiPToP通常能够以较短轨迹完成任务。不过，时间只在成功试验上取平均，而且仅覆盖六个场景，因此不能推出其在全部165次试验或失败恢复情况下都更快。

<div class="result-source" markdown="1">

来源：第VII-A节，表II后的结果分析

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

TiPToP is also faster in total completion time (Table II), beating π 0.5 $\pi_{0.5}$ -DROID on five of six scenes and matching it on the sixth, often completing single-step tasks in roughly half the time.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 受控评测中的部分场景由系统设计者执行，只有未标†的场景由外部团队评测；因此虽然包含外部复现环境，整个比较并非完全独立或统一盲测。时间指标又只统计成功试验，可能低估经常失败或需要重试的方法的实际时间成本。
- TiPToP使用凸包网格近似物体几何，可能错误表示香蕉等凹形物体；同时执行是开环的，抓取滑脱后不能根据反馈重试。MolmoSpaces中的开、关任务也因系统暂不支持而被排除，说明其当前能力范围尚未覆盖完整家庭操作。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- $π_{0.5}-DROID$：在350小时DROID机器人示范数据上微调的先进视觉—语言—动作模型（VLA）。它是有意义的强基线，因为它代表依赖大量同类机器人数据训练的端到端策略，而TiPToP不使用机器人训练数据；比较可检验模块化基础模型加任务与运动规划是否能替代大规模示范微调。

**实验想回答的问题**

- 在不使用特定机器人形态训练数据的条件下，TiPToP能否在简单、干扰物、语义推理和多步骤等不同难度的开放式桌面操作任务上，取得优于端到端视觉—语言—动作模型的成功率与任务进度？
- TiPToP将感知、任务与运动规划、执行模块串联后，是否仍具有可接受的总完成时间；同时，其失败能否被定位到具体模块或设计选择？

**实验实现**

受控比较采用“in-the-wild”协议：TiPToP与$π_{0.5}-DROID$接收相同自然语言指令和相同初始场景配置。28个场景横跨仿真、开发者实体平台和外部团队实体平台；表I中带†的场景由系统设计者评测，未标记者由外部团队评测，因此结果同时包含内部和外部执行，但并非全部盲测。时间比较仅统计成功试验，且TiPToP的Plan时间包括感知和规划。MolmoSpaces每项任务运行1,000个episode，但所给摘录未包含其具体排行榜分数、方差或显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- “Cube→bowl”仿真任务中，TiPToP完整成功率为5/10，但任务进度达到72.5%。作者据此认为不少失败只发生在单一步骤。该例说明TP能够揭示二元成功率掩盖的部分完成情况，但单一场景不能证明所有失败都具有这种局部性。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出结合基础模型、视觉感知及任务与运动规划器的模块化开放词汇机器人操作系统。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`be7f59c567fd2b5fad49cd7eb114191b6ff5143d355bd2e23b449f787c889b8b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
