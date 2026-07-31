---
title: "[论文解读] MorphQuad: Morphable Quadrotor for Superhuman Maneuverability, Manipulation, and Resiliency"
description: "[arXiv 2607.02764][机器人 / 具身智能] 本文针对空中机器人难以同时获得全向最大推力、近乎全局稳定性与紧凑四旋翼结构的问题，提出通过双轴独立旋翼转向和面向奇异性、下洗干扰的控制分配协同设计，实现兼具高机动、操作与抗扰能力的 MorphQuad。"
arxiv_id: "2607.02764"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.100229+00:00"
source_sha256: "4d2936fcaa9a38a5f3441de902e846505b0f5371ad25ebe87f9b2c6c8844b45f"
tags:
  - "机器人 / 具身智能"
  - "可变倾转多旋翼"
  - "全向飞行"
  - "双轴万向节"
  - "推力矢量化"
  - "几乎处处稳定性"
  - "飞行操作"
  - "扰动抑制"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2607.02764</p>

# MorphQuad: Morphable Quadrotor for Superhuman Maneuverability, Manipulation, and Resiliency

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Pacheco, Jose Diaz Peon Gonzalez, Xu, Jiawei, Zhao, Andrew, Zhou, Hongyu, Navsalkar, Atharva, Scheffer, Andrew, Reddi, Amrith Malli, Shankar, Sashreek, Bao, Yuqing, Tzoumas, Vasileios</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.02764) · [PDF 下载](https://arxiv.org/pdf/2607.02764) · **关键词** 可变倾转多旋翼, 全向飞行, 双轴万向节, 推力矢量化, 几乎处处稳定性, 飞行操作, 扰动抑制<br>


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

本文针对空中机器人难以同时获得全向最大推力、近乎全局稳定性与紧凑四旋翼结构的问题，提出通过双轴独立旋翼转向和面向奇异性、下洗干扰的控制分配协同设计，实现兼具高机动、操作与抗扰能力的 MorphQuad。

**不用术语来说**：基础设施巡检和应急作业需要一种类似“会飞的手”的机器人：它既要在狭窄空间中以任意姿态移动，又要从任意方向施力完成按压、推动或转阀，还要在风、壁面效应和接触反力作用下保持稳定。普通四旋翼的推力方向基本固定，侧向移动或施力前通常必须先倾斜机身；现有全向飞行器则往往尺寸复杂、推力相互抵消，或者在旋翼转向的特殊姿态附近失稳，因此仍不能同时满足上述需求。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 MorphQuad 的硬件与控制协同切入点：在标准平面四旋翼布局上为四套旋翼分别配置双轴转向机构，使每个旋翼的推力方向可独立调节，从结构上支持向任意方向集中可用的最大推力，同时保留可小型化的紧凑形态。
- 将近乎处处稳定的广义几何控制与能量优化推力分配结合，并利用输入矩阵的零空间处理万向节锁和旋翼间下洗干扰；相较前期概念系统 MorphEUS，本文进一步补齐硬件实现、实际执行约束与面向机动、接触操作和抗扰任务的验证。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于全向多旋翼飞行机器人研究，目标是让飞行器像“会飞的人手”一样，同时具备机动、操作与抗扰能力（MMR）：它既要在任意姿态下沿任意方向运动，也要从任意方向施加接触力，并在风、地面效应和摩擦等外扰下保持稳定。这里的关键不只是实现全向飞行，而是同时满足三个条件：可将全部旋翼的最大推力指向任意方向；在考虑万向节锁、控制奇异和旋翼下洗干扰后仍具有几乎处处稳定性；采用可小型化的平面四旋翼结构。传统四旋翼的推力方向固定，侧向运动或施力必须依靠机身倾斜；已有全向平台则往往以更多旋翼、非平面结构、有限倾转机构或多飞行器组合换取全向驱动，因而不能同时满足上述条件。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**全向飞行与全向推力矢量化**

全向飞行是指飞行器在任意机身姿态下都能向任意方向平移；全向推力矢量化进一步要求旋翼的合推力方向可以独立于机身姿态改变。本文强调的不只是各方向“有推力”，而是能把接近全部旋翼能力的最大推力集中到所需方向，以提高加速度、接触施力和抗扰上限。

</div>
<div class="concept-item" markdown="1">

**六维力矩与推力分配**

飞行器需要同时控制三维合力和三维合力矩，二者合称六维力矩（wrench）；推力分配负责把控制器要求的六维力矩转换为各旋翼的推力大小与方向。若多个旋翼互相抵消，虽然合成结果可能正确，却会浪费能量并降低可用最大推力。

</div>
<div class="concept-item" markdown="1">

**奇异性与几乎处处稳定性**

万向节锁是某些转轴构型下的小幅目标变化需要舵机急剧转动的运动学奇异现象，控制奇异则指输入到六维力矩的映射降秩，使某些控制方向无法产生。几乎处处稳定性表示除不可避免的特殊状态集合外，系统可从任意初始位置和姿态收敛并稳定跟踪目标。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是具有四套旋翼系统的平面四旋翼，每套旋翼通过可多圈转动的双轴万向节独立改变推力方向，并采用机载计算、定位和轨迹执行。系统输入可概括为期望的位置、姿态及其轨迹，以及自由飞行或接触任务中要求的合力和合力矩；控制系统需要输出各旋翼的推力与万向节角度，使飞行器在任意姿态下完成平移、悬停、连续旋转和接触施力。问题同时受到旋翼推力上限、舵机动态、万向节锁、输入矩阵降秩、旋翼间下洗干扰和外部扰动的约束；评价目标则是能否在紧凑四旋翼结构上同时获得任意方向最大推力矢量化、考虑实际执行约束的几乎处处稳定控制，以及面向操作和抗扰任务的机载自主运行。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\alpha_i$**

第 $i$ 套旋翼系统的外侧舵机位置或万向节外轴角度；原文图 2 用它比较有无零空间修正时的指令与实际舵机运动。

</div>
<div class="notation-item" markdown="1">

**$i$**

旋翼系统索引；MorphQuad 共有四套可独立双轴转动的旋翼系统。

</div>

</div>

**直接相关的工作**

- **MorphEUS（2025）**: 作者的前期概念方案，同样采用双轴可转动旋翼并提出具有几乎处处稳定性的控制与最小范数推力分配，但没有完成硬件实现，也未处理万向节锁、下洗干扰等实际执行问题；MorphQuad面向这些缺口给出实体平台和相应控制设计。
- **Aerix quadrotor（2025，专利申请）**: 其公开专利声称采用可全向倾转的四旋翼结构，并通过“propulsion offset”避开旋翼接近 $90^\circ$ 方位极点时的问题，但原文指出公开材料没有披露实际硬件、算法细节或偏移量的数学定义，因此无法确认其如何兼顾万向节锁处理与稳定性保证。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

基础设施维护、接触式检测和应急响应不仅要求飞行器到达远处或狭窄位置，还要求它在任意机身姿态下准确指向传感器、推动物体、按压工具或转动阀门，并抵抗来自任意方向的风、地面或壁面效应以及摩擦、弹性力等接触扰动。决定任务能力的并非抽象的“能向任意方向飞”，而是飞行器能否把全部旋翼能力有效汇聚到所需方向，并在连续姿态变化和接触过程中保持可靠稳定。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **固定倾角多旋翼**：旋翼相对机体的推力方向保持不变。标准四旋翼让所有旋翼朝向相同，可通过倾斜机身改变合力方向；另一类设计则把较多旋翼预先安装在不同空间方向，通过调节各旋翼推力组合出六自由度力和力矩。
- **可变倾角多旋翼**：利用同步机构、单轴关节或双轴万向机构在飞行中改变旋翼朝向，从而使推力方向不再由机身姿态唯一决定。已有系统包括联动车辆模块、非平面多旋翼以及具有独立旋翼转向能力的单机设计。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 固定同向旋翼只能在一个机体系方向产生最大合力，侧向运动或施力必须先转动机身；固定异向旋翼虽然可形成全向控制，却通常需要较多旋翼和非平面结构，而且工作时可能出现内部推力抵消，从而降低有效推力并妨碍紧凑化。
- 现有可变倾角方案常受转向范围、联动机构、车辆组合结构、控制矩阵秩亏、万向节锁或下洗干扰限制。接近万向节锁时，目标力旋量的微小变化可能要求舵机快速大幅转动并导致饱和；若旋翼气流相互干扰或推力彼此抵消，则实际执行偏离控制模型，稳定飞行和接触施力均可能失效。已有双轴概念或专利也未同时公开并验证处理这些执行问题且具有近乎处处稳定保证的完整方案。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有平台分别具备全向飞行、紧凑结构或一定的稳定控制能力，但原文比较指出，没有现有公开系统同时满足三项关键条件：在不依赖机身姿态的情况下把最大推力指向任意方向；在考虑万向节锁、控制奇异性和旋翼间下洗干扰后仍保持近乎处处稳定；采用可缩小到紧凑尺度的标准平面多旋翼结构。作者此前的 MorphEUS 也仅是双轴转向四旋翼的概念设计，尚未解决硬件实现和实际执行约束。

</div>
<div markdown="1"><span>核心问题</span>

能否在仅含四套旋翼的平面四旋翼结构中，通过硬件和控制协同设计，使全部旋翼推力可面向任意方向，同时让闭环系统在任意位置与几乎任意姿态间运动时，显式规避万向节锁和下洗干扰，并据此可靠完成自由飞行、接触操作和多方向扰动抑制？

</div>
<div markdown="1"><span>作者直觉</span>

若四个旋翼都能通过双轴机构独立转向，飞行器就不必先倾斜机身，也不必依赖许多固定朝向不同的旋翼来合成目标作用力；它可以像四根可转向的“手指”一样，把推力直接对准任务方向。仅增加关节仍会产生多个数学上等效、物理上却优劣不同的推力组合，因此控制器利用输入矩阵的零空间，在不改变目标总力和总力矩的前提下调整各旋翼指令：优先采用低能耗分配，仅在需要避开万向节锁或减少下洗干扰时引入必要的旋翼间推力抵消。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MorphQuad采用硬件与控制协同设计，把高层的六自由度位姿轨迹转换为四组旋翼的转速和双轴云台角。硬件上，每个机臂安装一对共轴反转旋翼，并用两个独立舵机调整推力方向，因此四组旋翼合计提供十二维抽象推力输入；共轴反转用于抵消旋翼气动阻力矩和陀螺反作用，使机体力矩主要来自各推力相对质心的力臂。控制上，系统先在$\mathsf{SE}(3)$上根据位置、速度、姿态和角速度误差计算期望六维力旋量，再以$\mathcal{L}_1$自适应环节补偿未知扰动，最后通过最小范数与零空间修正相结合的推力分配，将期望合力与合力矩变为各旋翼的三维推力向量，并反解出转速与云台角。

其核心思想是把传统四旋翼“只能大致沿机体竖直轴推”的限制改成“四个推力箭头都能独立转向”。由于十二维推力变量只需满足六维合力与合力矩约束，多出的自由度可以用于节能、避开云台奇异位形和减少旋翼下洗相互干扰，而不改变飞行控制器要求的净作用。论文给出的稳定性是几乎处处渐近稳定，即除姿态空间中的零测集特殊初态外，闭环误差可收敛；这比依赖欧拉角的控制更适合连续翻滚和多圈旋转，但并不等同于对所有初态都具有全局渐近稳定性。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 状态估计与轨迹命令形成

Jetson生成或执行轨迹，Pixhawk结合机载VIO状态形成控制所需的世界坐标位置、速度和机体姿态信息；姿态始终用旋转矩阵$\boldsymbol{R}\in\mathsf{SO}(3)$表示。

<div class="method-step__io" markdown="1">

**输入**：期望轨迹$\boldsymbol{p}_d,\boldsymbol{v}_d,\ddot{\boldsymbol{p}}_d,\boldsymbol{R}_d,\boldsymbol{\omega}_d,\dot{\boldsymbol{\omega}}_d$，以及机载视觉惯性里程计和飞控提供的当前状态$\boldsymbol{p},\boldsymbol{v},\boldsymbol{R},\boldsymbol{\omega}$。<br>
**输出**：当前状态与期望状态组成的$\mathsf{SE}(3)$轨迹跟踪问题。

</div>

**直观理解**：系统先回答“飞机现在在哪里、朝哪里，以及下一刻应该在哪里、朝哪里”。使用旋转矩阵可避免欧拉角在某些姿态下无法正常表示旋转的问题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 几何跟踪与扰动补偿

几何控制器直接在$\mathsf{SE}(3)$上构造位置误差$\boldsymbol{e}_p$、速度误差$\boldsymbol{e}_v$、姿态误差$\boldsymbol{e}_R$和角速度误差$\boldsymbol{e}_\omega$，计算机体系期望力$\boldsymbol{f}_{\mathrm{Geo}}$与力矩$\boldsymbol{\tau}_{\mathrm{Geo}}$；$\mathcal{L}_1$自适应增广在线估计并抵消风、地面效应等未知扰动。

<div class="method-step__io" markdown="1">

**输入**：当前和期望的平移、旋转状态，以及质量$m$、惯量矩阵$\boldsymbol{J}$等动力学参数。<br>
**输出**：经扰动补偿的期望六维力旋量$\boldsymbol{w}=[\boldsymbol{f}^{\top}\;\boldsymbol{\tau}^{\top}]^{\top}\in\mathbb{R}^{6}$。

</div>

**直观理解**：这一层像驾驶员：根据位置和朝向偏差决定机体应当受到多大的推力与扭转作用。自适应环节则持续估计未建模的外力，并在命令中加入反向补偿。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 能量最优推力分配

先求最小范数解$\boldsymbol{t}_0=\boldsymbol{M}^{\dagger}\boldsymbol{w}$，其中$\boldsymbol{t}=[\boldsymbol{t}_1^{\top},\ldots,\boldsymbol{t}_4^{\top}]^{\top}$包含四个三维推力向量；该解在满足$\boldsymbol{M}\boldsymbol{t}=\boldsymbol{w}$的同时最小化各推力向量平方范数之和。

<div class="method-step__io" markdown="1">

**输入**：期望力旋量$\boldsymbol{w}$和由四个固定旋翼位置$\boldsymbol{l}_i$确定的输入矩阵$\boldsymbol{M}\in\mathbb{R}^{6\times12}$。<br>
**输出**：实现期望合力和合力矩的基准旋翼推力向量$\boldsymbol{t}_0\in\mathbb{R}^{12}$。

</div>

**直观理解**：满足同一合力和合力矩的四组推力组合有很多，这一步选择总体用力最小的一组。对旋翼而言，较小的推力平方和对应论文所采用的悬停效率代理目标。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 零空间安全修正

系统加入$\boldsymbol{N}_M\boldsymbol{c}^{N}$重分配各旋翼推力：当合力接近机体$\boldsymbol{i}_{\mathcal B}$轴时错开相邻旋翼的共线推力以减少下洗干扰，当合力接近$\boldsymbol{j}_{\mathcal B}$轴时将单个推力方向推离$\beta_i=\pm\pi/2$以避免云台锁死。由于$\boldsymbol{M}\boldsymbol{N}_M=\boldsymbol{0}$，该修正理论上不改变控制器要求的净力旋量。

<div class="method-step__io" markdown="1">

**输入**：基准分配$\boldsymbol{t}_0$、期望合力方向，以及$\boldsymbol{M}$的六维零空间基$\boldsymbol{N}_M$。<br>
**输出**：兼顾净力旋量、下洗规避与云台可控性的四个最终推力向量$\boldsymbol{t}_i$。

</div>

**直观理解**：可以把它理解为四个人共同搬动物体：总的推力和扭转不变，但允许每个人稍微换一个发力方向，从而避免彼此挡住气流或把关节转到失去控制的姿势。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 几何控制器的期望力与力矩

$$
\begin{aligned}
\boldsymbol{f}_{\mathrm{Geo}}&=\boldsymbol{R}^{\top}\left(-k_{\boldsymbol{p}}\boldsymbol{e}_{\boldsymbol{p}}-k_{\boldsymbol{v}}\boldsymbol{e}_{\boldsymbol{v}}-m\boldsymbol{g}+m\ddot{\boldsymbol{p}}_{d}\right),\\
\boldsymbol{\tau}_{\mathrm{Geo}}&=-k_{\boldsymbol{R}}\boldsymbol{e}_{\boldsymbol{R}}-k_{\boldsymbol{\omega}}\boldsymbol{e}_{\boldsymbol{\omega}}+\boldsymbol{\omega}\times\boldsymbol{J}\boldsymbol{\omega}-\boldsymbol{J}\left(\boldsymbol{\omega}\times\boldsymbol{R}^{\top}\boldsymbol{R}_{d}\boldsymbol{\omega}_{d}-\boldsymbol{R}^{\top}\boldsymbol{R}_{d}\dot{\boldsymbol{\omega}}_{d}\right)
\end{aligned}
$$

**符号说明**

- $\boldsymbol{f}_{\mathrm{Geo}},\boldsymbol{\tau}_{\mathrm{Geo}}$：几何控制器输出的机体系期望合力与期望合力矩
- $\boldsymbol{e}_{\boldsymbol{p}},\boldsymbol{e}_{\boldsymbol{v}}$：位置误差与线速度误差，分别为当前值减期望值
- $\boldsymbol{e}_{\boldsymbol{R}},\boldsymbol{e}_{\boldsymbol{\omega}}$：在旋转群上定义的姿态误差，以及将期望角速度变换到当前机体系后得到的角速度误差
- $k_{\boldsymbol{p}},k_{\boldsymbol{v}},k_{\boldsymbol{R}},k_{\boldsymbol{\omega}}$：位置、速度、姿态和角速度反馈增益
- $m,\boldsymbol{g},\boldsymbol{J}$：飞行器质量、世界系重力加速度向量和机体系惯量矩阵
- $\boldsymbol{R},\boldsymbol{R}_{d}$：当前和期望的机体系到世界系旋转矩阵
- $\boldsymbol{\omega},\boldsymbol{\omega}_{d},\dot{\boldsymbol{\omega}}_{d}$：当前角速度、期望角速度及期望角加速度
- $\ddot{\boldsymbol{p}}_{d}$：期望平移加速度

<div class="equation-explanation" markdown="1">

**直观理解**：第一行把位置和速度误差反馈、重力补偿及期望加速度前馈合成为世界系所需作用力，再旋转到机体系。第二行用姿态与角速度反馈纠正旋转误差，并加入刚体陀螺耦合和期望旋转运动的前馈补偿；这使控制律直接适用于任意三维姿态。<br>
**原文位置**：Materials and Methods，Control，Geometric controller，式(11)及其后紧接的力矩公式

</div>

</div>

<div class="equation-block" markdown="1">

#### 最小范数与零空间推力分配

$$
\boldsymbol{t}=\boldsymbol{M}^{\dagger}\boldsymbol{w}+\boldsymbol{N}_{M}\boldsymbol{c}^{N},\qquad \boldsymbol{M}^{\dagger}=\boldsymbol{M}^{\top}(\boldsymbol{M}\boldsymbol{M}^{\top})^{-1},\qquad E(\boldsymbol{t})=\frac{1}{2}\sum_{i=1}^{4}\lVert\boldsymbol{t}_{i}\rVert_{2}^{2}
$$

**符号说明**

- $\boldsymbol{t}=[\boldsymbol{t}_{1}^{\top}\;\boldsymbol{t}_{2}^{\top}\;\boldsymbol{t}_{3}^{\top}\;\boldsymbol{t}_{4}^{\top}]^{\top}$：四个旋翼系统的三维推力向量堆叠成的十二维控制输入
- $\boldsymbol{w}=[\boldsymbol{f}^{\top}\;\boldsymbol{\tau}^{\top}]^{\top}$：由期望合力和期望合力矩组成的六维力旋量
- $\boldsymbol{M}$：由各旋翼相对质心的固定位置决定、满足力旋量关系$\boldsymbol{w}=\boldsymbol{M}\boldsymbol{t}$的满行秩输入矩阵
- $\boldsymbol{M}^{\dagger}$：输入矩阵的Moore-Penrose伪逆，产生最小二范数基准分配
- $\boldsymbol{N}_{M}$：矩阵$\boldsymbol{M}$的零空间基，满足$\boldsymbol{M}\boldsymbol{N}_{M}=\boldsymbol{0}$
- $\boldsymbol{c}^{N}\in\mathbb{R}^{6}$：控制零空间推力重分配程度的系数向量
- $E(\boldsymbol{t})$：四组推力向量平方范数之和的一半，即论文采用的能量或推力效率代价

<div class="equation-explanation" markdown="1">

**直观理解**：第一项是精确产生目标合力与力矩所需的最省力解；第二项位于输入矩阵的零空间，因此可以改变单个旋翼如何出力而保持总效果不变。正常状态下应接近第一项的能量最优分配，接近下洗冲突或云台锁时则牺牲部分最优性，通过第二项换取可靠执行。<br>
**原文位置**：Materials and Methods，Control，Thrust allocation中的Proposition 2，以及Null-space correction for inter-rotor downwash and gimbal lock，式(15)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：该方法不是通过数据训练得到的模型，没有训练损失、训练集或参数学习阶段。其优化发生在在线控制分配中：在等式约束$\boldsymbol{M}\boldsymbol{t}=\boldsymbol{w}$下最小化$E(\boldsymbol{t})=\frac{1}{2}\sum_{i=1}^{4}\|\boldsymbol{t}_i\|_2^2$，伪逆$\boldsymbol{M}^{\dagger}\boldsymbol{w}$给出该问题的最小范数解；随后加入零空间项处理下洗和云台锁，因此最终命令在触发修正时不再是严格的全局最小范数解。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双轴云台共轴旋翼单元**

四个旋翼系统均由一对共轴反转旋翼和双轴云台组成：内轴角$\alpha_i$与外轴角$\beta_i$决定单位推力方向$\boldsymbol{G}_i(\alpha_i,\beta_i)$，转速$\Omega_i$决定推力大小。共轴反转抵消每组旋翼的气动阻力矩和陀螺反作用，因此机体力矩可主要建模为$\sum_i\boldsymbol{l}_i\times\boldsymbol{t}_i$；四个三维推力向量形成十二维抽象输入，而固定几何矩阵$\boldsymbol{M}$将其映射为六维力旋量。

> 直观理解：普通四旋翼主要靠倾斜整个机体改变水平推力，本设计让每条机臂上的推力本身转向，因此飞机可在保持任意姿态时独立产生所需合力。矩阵$\boldsymbol{M}$满行秩意味着在忽略执行器幅值等物理限制的理想模型下，六个力与力矩通道都能被直接驱动。

**2. $\mathsf{SE}(3)$几何控制与$\mathcal{L}_1$自适应增广**

几何控制器不把姿态压缩成欧拉角，而是在旋转群$\mathsf{SO}(3)$上用$\boldsymbol{e}_R=\frac{1}{2}(\boldsymbol{R}_d^{\top}\boldsymbol{R}-\boldsymbol{R}^{\top}\boldsymbol{R}_d)^{\vee}$定义姿态误差，并结合角速度误差、平移误差和刚体前馈项生成期望力与力矩。论文据此主张闭环具有几乎处处渐近稳定性，并加入$\mathcal{L}_1$自适应增广以提高对任意方向未知扰动的补偿能力；所给节选未展开该增广的预测器、滤波器及自适应律。

> 直观理解：几何控制允许姿态连续跨越多圈，不会因俯仰角接近特定角度而出现欧拉角公式奇异。需要区分的是：几何控制避免的是姿态表示奇异，推力反解中的“云台锁”则是两个机械转轴重合导致的执行器方向控制能力丢失，后者仍需分配层处理。

**3. 伪逆分配与零空间修正**

由于$\boldsymbol{M}$为满行秩的$6\times12$宽矩阵，$\boldsymbol{M}^{\dagger}\boldsymbol{w}$给出满足目标力旋量的唯一最小二范数解，而$\boldsymbol{N}_M\boldsymbol{c}^{N}$描述所有不改变净力旋量的冗余分量。论文根据期望合力与机体轴$\boldsymbol{i}_{\mathcal B},\boldsymbol{j}_{\mathcal B}$的内积设置$\boldsymbol{c}^{N}$：只在接近下洗冲突或云台锁区域时引入旋翼间推力抵消和方向偏置。

> 直观理解：伪逆负责正常情况下省力，零空间负责特殊方向下可执行且稳定。两者存在明确取舍：零空间修正会偏离严格的最小能量解，但作者有意限制推力相互抵消只用于规避下洗和云台锁，以免长期浪费推力余量。

**训练与推理**

该系统没有机器学习意义上的训练流程。部署前，作者把结构、运动学和动力学模型集成到ROS与Gazebo软件在环仿真中验证完整软件栈；所给节选未报告需要离线辨识或训练的控制器参数流程。

在线执行时，Jetson Orin Nano生成轨迹，RealSense相机提供VIO传感流，Pixhawk执行姿态和位置控制。每个控制周期依次读取当前状态和期望$\mathsf{SE}(3)$轨迹，计算几何误差与基准力旋量，由$\mathcal{L}_1$增广加入扰动补偿，再求伪逆分配和按合力方向设置的零空间修正，最后将每个$\boldsymbol{t}_i$转换为$\Omega_i,\alpha_i,\beta_i$；在多个等价角解中选择距当前舵机位置最近者并限制额外转数$n_r$，随后向四组电调和八个舵机发送命令。

**复现信息**

复现方法所必需的硬件结构是H形四旋翼机体、四套可独立转向的双轴云台共轴反转旋翼，以及舵机位置反馈；若改为单旋翼或共用倾转机构，论文中阻力矩抵消、十二维独立输入和固定满行秩矩阵$\boldsymbol{M}$等假设将不再直接成立。原型起飞质量为$4.56\,\mathrm{kg}$；每个共轴旋翼对标称可产生$2.8\,\mathrm{kg}$推力，使整机约在$40\%$油门悬停。Figure 8的包络计算则假设每臂最大推力为$24.5\,\mathrm{N}$，且未启用为规避下洗而引入的推力抵消，因此该理论包络不能直接视为所有修正开启时的持续可用能力。

计算栈由Pixhawk Autopilot FMUv6x、Jetson Orin Nano和Intel RealSense双目深度相机构成，定位和轨迹执行均可机载完成，不依赖外部动作捕捉。公平实现还需保留两类分配约束：根据当前舵机位置选择最近的三角反解分支，并在合力接近机体$\boldsymbol{i}_{\mathcal B}$或$\boldsymbol{j}_{\mathcal B}$轴时启用零空间修正。所给节选没有明确报告控制频率、几何反馈增益、$\mathcal{L}_1$滤波器与自适应律参数、零空间修正的尺度归一化方式、舵机角速度和机械限位、转数上限$n_r$的具体取值，因此这些内容仍需查阅完整论文或代码后才能完整复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**位置均方根误差（position RMSE）**

将实验全过程中机载状态估计器给出的位置与规划参考位置之差按时间汇总，衡量飞行器在旋转、接触或受扰时维持平移轨迹的能力。误差在世界坐标系中计算，但参考的是机载视觉惯性定位结果，而非外部高精度真值。 （越低越好，因为较小误差表示飞行器更接近规划位置；不过它同时受控制性能和机载状态估计误差影响。）

</div>
<div class="metric-item" markdown="1">

**姿态或方向均方根误差（orientation/attitude RMSE）**

汇总实际估计姿态与参考姿态之间的角度偏差，用于检验连续旋转、动态指向以及扰动下的姿态跟踪。操作实验主要报告未被接触方向直接影响的轴，以判断接触力是否破坏其他方向的控制。 （越低越好，因为较小角度误差表示指向和旋转跟踪更准确；但不同实验所报告的轴和动态条件并不完全相同，不能只按单个数值横向排名。）

</div>
<div class="metric-item" markdown="1">

**可施加的力与力矩**

通过成功推动、按压或转动实物，以及外接测力装置等实验条件，描述平台对环境施加作用的能力。论文将侧向力与飞行器起飞质量、转动力矩与人类手腕能力作量级比较；这不是闭环力跟踪误差。 （在保持稳定和完成任务的前提下通常越高越好，因为更大的力或力矩意味着可处理更重或阻力更大的对象；但论文没有测量期望力与实际力之间的跟踪精度。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 机动性：绕管平移并连续旋转，以及悬停时动态手部指向跟踪

<div class="result-value" markdown="1">

在绕水平管道的实验中，MorphQuad沿直径1米的竖直圆轨迹平移，同时连续俯仰旋转720度；三个位置轴的RMSE均低于6厘米，俯仰RMSE为5.5度。更动态的手部跟踪中，位置RMSE为5.5厘米、方向跟踪RMSE为6.99度，快速手部加速时偶有超过15度的离群误差。

</div>

结果表明，大幅连续姿态旋转不会必然牺牲平移控制，且平台能够在悬停位置基本不变时独立改变相机指向。这直接支持“平移与旋转可解耦”的系统目标。手部跟踪误差高于预编程绕管轨迹，也揭示了视觉检测和响应速度的限制。实验只展示指定任务中的跟踪表现，没有与传统四旋翼或其他全向平台对比，也没有证明任意未知轨迹下都能达到相同精度。

<div class="result-source" markdown="1">

来源：Results，Maneuverability: Simultaneous translation and continuous multi-revolution，Continuous rotation for pipe inspection；Figure 5(A)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MorphQuad achieves position errors below 6 cm RMSE on all three axes and pitch errors at 5.5° RMSE across the full trajectory.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 操作能力：转阀门、墙面栖附并压钉、推动重物

<div class="result-value" markdown="1">

MorphQuad完成三类接触操作，并展示与4.56千克起飞质量相当量级的侧向力，以及4.92牛·米、与人类手腕相当量级的力矩；任务完成时，在不直接受交互作用影响的轴上，位置RMSE低于5厘米、姿态RMSE低于3度。

</div>

这些任务分别考察旋转物体所需的力矩、向墙面持续施力，以及对可移动重物持续推力。结果说明平台在产生较大接触作用时仍能约束其他方向的运动，体现了全向推力对空中操作的价值。不过，接触过程没有力反馈，所谓“人类水平”是力或力矩量级比较，不代表具有人手的精细操作、触觉调节或力跟踪能力；任务成功也不能替代受控载荷下的系统化力学标定。

<div class="result-source" markdown="1">

来源：Results，Experiment setup，Evaluation summary，(b) Manipulation；Figure 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MorphQuad demonstrates omnidirectional force and torque application, including a lateral force generation comparable to its takeoff mass (4.56 kg) and its torque application comparable to a human wrist (4.92 Nm).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 抗扰韧性：30米/秒局部风扰，以及推、拉、偏心挑动等物理扰动

<div class="result-value" markdown="1">

在30米/秒气流甚至直接吹向单个旋翼的情况下，主导风向的位置RMSE约为8厘米，姿态RMSE低于5度。面对推、拉和偏心挑动，平台在与物理位移正交的轴上保持2至4厘米的位置RMSE和低于5度的姿态RMSE。

</div>

局部吹风同时引入非均匀、时变的力和力矩，比仅考察均匀平移风载更能检验单旋翼受扰和姿态耦合；物理推拉实验则检验瞬态恢复和持续外力下的控制。结果支持平台能够从多个方向生成反向控制作用，并减少扰动向正交轴传播。它没有给出扰动移除后的恢复时间、最大可承受扰动力、失败阈值或重复试验统计，因此不能据此确定鲁棒性的完整边界。

<div class="result-source" markdown="1">

来源：Results，Experiment setup，Evaluation summary，(c) Resiliency；Figure 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MorphQuad achieves a position RMSE of approximately 8 cm along the dominant wind axis, and the orientation RMSE below 5°.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未提供定量基线或消融实验，无法分别隔离双轴云台、共轴反转电机、特殊推力分配和广义几何控制各自带来的增益，也无法判断MorphQuad相对传统四旋翼或其他全向飞行器的优势幅度。
- 误差基于机载视觉惯性状态估计而非独立外部真值，且操作对接触开环、没有力/力矩传感器；原文也未明确报告重复次数、方差、置信区间、成功率和极限扰动。因此，现有结果证明了原型在所示任务中的可行性，但不足以建立定位绝对精度、接触力控制精度或统计可靠性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。

**实验想回答的问题**

- MorphQuad能否在完全机载计算、无GPS且无外部动作捕捉的条件下，同时实现机动性、操作能力与抗扰韧性，即在大范围姿态变化或接触外界时仍保持可用的位姿跟踪精度？
- 独立双轴矢量旋翼、广义几何控制与推力分配组成的软硬件系统，能否支撑连续多圈旋转、任意方向的力与力矩施加，以及来自不同方向的风扰和物理扰动恢复？

**实验实现**

实验分为三组。机动性组包括：在两根水平平行管道之间绕管飞行，间隙仅为机体边长的1.3倍；以及在距操作者1.5米处悬停，利用前视相机实时跟踪手部指向和滚转。操作组包括：转动距地面3米、轴线相对墙面成45度且轴长30厘米的阀门；在距地面2米的泡沫块上栖附并压入钉子；推动质量30千克、未固定的带轮白板。抗扰组使用距机体前面不超过30厘米的吹叶机产生30米/秒非均匀气流，并由操作者用锤头实施侧推和偏心挑动，或通过带在线测力计的系绳施加持续拉力。所有任务均采用完全机载计算、视觉惯性定位和轨迹执行，不使用GPS、动作捕捉或离板计算。规划器按照任务预设带时间戳的位置和姿态设定点；手部跟踪例外地由机载视觉实时产生姿态设定点。论文按机载状态估计器建立的世界坐标系记录位置与姿态误差。操作任务对接触是开环的：没有力/力矩传感器，也没有操作过程中的视觉伺服，控制器仅跟踪位姿参考并将接触反力视为扰动。因此，这些实验主要验证任务完成和受接触影响时的位姿稳定性，而不是接触力控制精度。原文没有设置公开数据集、训练/测试划分或定量对照基线；实验属于实体机器人能力验证，因而不能据此判断相对其他飞行平台的统计优势。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 绕管检查是最具代表性的综合案例：MorphQuad在两管之间仅为机体边长1.3倍的狭窄间隙内，沿直径1米的圆轨迹绕管运动并连续旋转720度，同时始终将朝向对准管道。该案例把位置精度、连续姿态变化和传感器定向结合在一个任务中，说明可变推力方向可让机体姿态服务于检查视角，而无需像普通四旋翼那样用倾斜机体来换取水平加速度；但案例是预先设定轨迹，尚未检验未知障碍环境中的在线规划。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出可变形四旋翼的硬件与控制协同设计，以实现全向飞行、接触操作和扰动恢复。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`4d2936fcaa9a38a5f3441de902e846505b0f5371ad25ebe87f9b2c6c8844b45f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
