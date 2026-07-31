---
title: "[论文解读] Global Exponential Stabilization of the Kinematic Bicycle Model of a Car in Polar Coordinates"
description: "[arXiv 2607.26442][机器人 / 具身智能] 本文通过极坐标与距离归一化坐标重构运动学自行车模型，使其呈现适合反步控制的结构，从而以光滑反馈实现极坐标下的全局指数输出稳定，并生成更接近人类驾驶的泊车轨迹。"
arxiv_id: "2607.26442"
announcement_date: "2026-07-30"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.846960+00:00"
source_sha256: "d94c73246af2f57cc54aabc96e56305598ed6d452da587aee1edf32be601d7f9"
tags:
  - "机器人 / 具身智能"
  - "运动学自行车模型"
  - "非完整系统"
  - "极坐标控制"
  - "距离归一化坐标"
  - "Brockett 条件"
  - "全局指数输出稳定"
  - "自动停车"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2607.26442</p>

# Global Exponential Stabilization of the Kinematic Bicycle Model of a Car in Polar Coordinates

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Velimir Todorovski, Kwang Hak Kim, Alessandro Astolfi, Miroslav Krstic</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26442v1) · [PDF 下载](https://arxiv.org/pdf/2607.26442v1) · **关键词** 运动学自行车模型, 非完整系统, 极坐标控制, 距离归一化坐标, Brockett 条件, 全局指数输出稳定, 自动停车<br>


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

本文通过极坐标与距离归一化坐标重构运动学自行车模型，使其呈现适合反步控制的结构，从而以光滑反馈实现极坐标下的全局指数输出稳定，并生成更接近人类驾驶的泊车轨迹。

**不用术语来说**：汽车低速泊车时，需要同时调整位置、车身朝向、速度和转向，使车辆最终准确停到目标位。困难在于，汽车不能横向平移；若直接依据平面位置和朝向持续、平滑地计算控制量，系统的拓扑性质又会阻止这种反馈从所有初始状态完成渐近稳定。因此，论文要解决的是：不依赖在线轨迹优化，仅靠连续时间反馈，能否让车辆快速、平滑且以符合实际泊车习惯的方式到达目标。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者引入极坐标及额外的距离归一化坐标，用相对目标的距离来归一化姿态和运动变量；这些坐标既编码了人类式泊车的几何关系，又把非漂移型自行车模型整理为可进行非传统反步设计的严格反馈结构。
- 作者据此构造光滑反馈律和满足小控制性质的控制李雅普诺夫函数，证明极坐标输出具有全局指数稳定性，并得到笛卡尔坐标下除一个零测集外的指数吸引性；该例外对应车辆已处于目标位置但方向错误、必须先驶离再调整的状态。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于非完整车辆的连续时间几何控制研究。对象是停车低速下常用的运动学自行车模型：车辆需从任意一般初始位姿驶向原点并对准目标方向。其关键困难并非系统不可控，而是非完整运动约束带来的拓扑障碍——在笛卡尔坐标中，Brockett–Ryan–Coron–Rosier相关结论排除了连续或不连续的时不变反馈对完整车辆状态进行渐近稳定的可能性。本文因此不直接在笛卡尔状态上寻求平滑静态稳定器，而把车辆位姿改写为相对目标的极坐标，并进一步引入按目标距离归一化的几何变量；最终要求这些变换坐标全局指数收敛，由此获得极坐标输出的全局指数稳定，以及除零测集异常构型外笛卡尔位姿的指数吸引性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**运动学自行车模型（kinematic bicycle model）**

它用单个等效前轮和单个等效后轮描述汽车的平面位置、朝向与转向几何，忽略轮胎动力学等高速效应，适合停车速度。本文采用纵向加速度和转向角作为输入，因此模型带有漂移项，不属于可直接化为链式形式的无漂移版本。

</div>
<div class="concept-item" markdown="1">

**非完整约束与 Brockett 障碍**

非完整约束表示车辆不能瞬时向任意方向运动，例如汽车不能直接横移；系统虽可通过前后行驶与转向到达目标，却未必能由平滑、时不变的状态反馈稳定。Brockett 条件揭示了这种拓扑限制，也是本文改用具有奇异性的极坐标而非直接在笛卡尔坐标中设计控制器的原因。

</div>
<div class="concept-item" markdown="1">

**全局指数输出稳定**

它要求被选定的输出误差从允许的任意初态出发，均以可统一估计的指数速度衰减，而不一定要求变换系统的所有内部状态都按同样意义稳定。本文把原始极坐标视为距离归一化系统的输出，从而避开对笛卡尔完整状态实施平滑时不变渐近稳定所受到的拓扑禁止。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

车辆在平面停车速度下由状态 (x,y,θ,ϕ) 描述，其中 (x,y) 是位置，θ 是车身朝向，ϕ 是转向构型；目标状态为 (0,0,0,0)。按照原文设定，控制输入是纵向加速度与转向角，而不是无漂移模型中常见的纵向速度与转向速率；研究采用连续时间反馈，不依赖离散化模型上的在线优化。系统先经映射 (x,y,θ,ϕ)↦(ρ,δ,γ,φ) 表示相对目标的距离和角度关系，再引入距离归一化变量以编码类似人类停车的几何轨迹。任务是在这些变换坐标上构造平滑反馈，使极坐标输出全局指数收敛，并在笛卡尔坐标中实现几乎全局指数吸引；例外是车辆已经位于停车点、但朝向未对准的零测集构型，因为汽车必须先驶离目标点才能重新调整姿态。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$(x,y,\theta,\phi)$**

车辆相对停车目标的笛卡尔构型：平面位置 (x,y)、车身朝向 θ 与原图所记转向变量 ϕ。

</div>
<div class="notation-item" markdown="1">

**$(0,0,0,0)$**

期望停车构型，即车辆位于原点、朝向和转向构型均与目标对齐。

</div>
<div class="notation-item" markdown="1">

**$(\rho,\delta,\gamma,\varphi)$**

由笛卡尔构型变换得到的极坐标状态；ρ 表示相对目标的距离，其余变量描述车辆朝向、目标视线及转向之间的角度关系。节选未逐一定义 δ、γ、φ 的精确符号约定。

</div>
<div class="notation-item" markdown="1">

**$(x,y,\theta,\phi)\mapsto(\rho,\delta,\gamma,\varphi)$**

从车辆笛卡尔构型到目标相对极坐标的变换；其坐标奇异性被用于绕开笛卡尔状态上的平滑时不变反馈稳定障碍。

</div>

</div>

**直接相关的工作**

- **笛卡尔到链式形式的变换及其时变或不连续反馈方法 [15,4,20,9,14,3]**: 这些方法通过链式系统绕开拓扑障碍，但自行车模型的坐标变换只在受限区域有效，因而限制吸引域；时变反馈还可能产生振荡轨迹和较慢收敛。更重要的是，它们通常依赖以纵向速度和转向速率直接驱动的无漂移模型，不适用于本文采用纵向加速度与转向角输入的带漂移模型。
- **面向独轮车停车的极坐标反馈与控制 Lyapunov 函数方法 [1,2,18,22,21,12]**: 这些工作表明，极坐标的固有奇异性可绕开笛卡尔模型中的 Brockett 障碍，并支持全局极坐标反馈设计；但该优势不能直接推广到运动学自行车，因为 Brockett 条件只是平滑稳定器存在的必要条件而非充分条件。本文以额外的距离归一化坐标和反步结构补足这一缺口。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

运动学自行车模型是描述汽车低速运动的常用模型，但适用于真实泊车的稳定反馈律仍较少。实际控制不仅要把车辆带到目标构型，还应避免明显振荡和过慢收敛，并产生类似驾驶员先调整车身、再逐渐对准车位的轨迹。本文进一步采用纵向加速度和转向角作为输入，因此需要处理一个带有纵向动态、不能直接化为经典链式形式的模型。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **模型预测控制及离散优化方法**：在离散时间模型上反复预测车辆未来运动，通过在线求解有限时域优化问题选择控制输入；这类方法能够显式考虑轨迹和约束，但其研究重点不同于本文所追求的连续时间几何反馈与稳定性构造。
- **链式形式变换配合时变或不连续反馈**：先把无漂移运动学自行车模型从笛卡尔坐标变换为标准链式系统，再使用时变反馈或不连续反馈绕开非完整系统无法由常规时不变反馈渐近稳定的拓扑障碍。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 笛卡尔坐标中的非完整自行车系统受到 Brockett–Ryan–Coron–Rosier 型拓扑障碍约束：虽然系统全局可控，却不能由连续或不连续的时不变反馈实现渐近稳定。链式形式路线虽可绕开该障碍，但自行车的坐标变换只在受限区域有效，因而显著限制吸引域；相关时变控制还可能产生振荡轨迹并导致较慢收敛。
- 既有链式形式方法通常假设纵向速度和转向速率可直接控制，即模型无漂移；本文采用纵向加速度与转向角作为输入，模型不再无漂移，不能等价转换为该链式形式。另一方面，极坐标方法虽已成功用于独轮车泊车，但避开 Brockett 必要条件并不自动保证自行车模型存在光滑稳定器，因此不能直接移植。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚缺少一种面向“纵向加速度—转向角”输入的运动学自行车模型、在连续时间内仅依靠光滑反馈工作，并能在极坐标意义下提供全局指数稳定保证且自然形成现实泊车几何的控制设计。关键缺口不是单纯选择极坐标，而是找到能把自行车的附加动态组织成可递归稳定结构的新坐标表示。

</div>
<div markdown="1"><span>核心问题</span>

能否构造一组带奇异性的距离归一化坐标，使极坐标下的非漂移型运动学自行车呈现严格反馈结构，进而通过反步法得到光滑控制律，并严格证明目标位置与姿态相关输出全局指数收敛，同时生成类似人类驾驶的泊车轨迹？

</div>
<div markdown="1"><span>作者直觉</span>

极坐标直接描述车辆离车位还有多远以及相对车位的角度误差，其在目标处的奇异性改变了笛卡尔坐标下触发拓扑障碍的表示方式。再用剩余距离归一化关键变量，相当于要求车辆的姿态、速度与转向调整随接近车位按合适比例缩小：远处允许较大幅度机动，近处则逐渐对准并减小动作。这样不仅把“人如何泊车”的几何规律写进状态，而且形成上层误差产生虚拟控制、下层状态逐级跟踪的严格反馈结构，使反步法能够逐层构造稳定反馈。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

方法以车辆状态 $(x,y,\theta,v)$ 和控制输入纵向加速度 $a$、前轮转角 $\phi$ 为起点，先把笛卡尔坐标改写为目标中心的极坐标 $(\rho,\delta,\gamma)$，再通过 $z=\gamma+\arctan(k_2\delta)$ 与 $\hat v=v-k_1N(k_2\delta)\rho$ 暴露近似严格反馈结构。随后作者用剩余距离 $\rho$ 归一化角度和速度，得到 $(\rho,\bar\delta,\bar z,\bar v)$，并通过输入变换把原始的耦合、含 $1/\rho$ 项的动力学整理成适合反步控制的级联系统。

核心思想是把“像人一样停车”的几何规律写入状态：车辆越接近目标，方向误差与速度就必须至少按剩余距离的量级同步减小，而不能到达目标点后再原地调整方向。归一化变量直接衡量角度或速度相对于剩余距离是否足够小；配合反步中的虚拟控制，作者试图逐层稳定距离、方位角、视线角和速度误差。所给节选展示了坐标与输入变换以及归一化系统，但没有包含最终辅助反馈 $\tilde\varphi$、$\hat a$ 的明确闭环选取和稳定性定理，因此不能仅依据该节选完整复现最终控制器。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立车辆模型并转换到目标中心极坐标

定义 $\rho=\sqrt{x^2+y^2}$、$\delta=\operatorname{atan2}(y,x)+\pi$、$\gamma=\delta-\theta$，并以 $\phi=\arctan(\varphi)$ 将无约束辅助转向量 $\varphi\in\mathbb R$ 映射到物理范围。由此得到极坐标动力学 $\dot\rho=-v\cos\gamma$、$\dot\delta=(v/\rho)\sin\gamma$、$\dot\gamma=(v/\rho)\sin\gamma-(v/L)\varphi$、$\dot v=a$。

<div class="method-step__io" markdown="1">

**输入**：车辆笛卡尔状态 $(x,y,\theta,v)$、轴距 $L$，以及输入纵向加速度 $a$ 和实际前轮转角 $\phi$。<br>
**输出**：定义在 $\mathcal S=\{\rho>0\}\times\mathbb R^3$ 上的状态 $(\rho,\delta,\gamma,v)$ 及辅助输入 $(a,\varphi)$。

</div>

**直观理解**：坐标原点被放在停车目标处，$\rho$ 表示还剩多远，$\delta$ 和 $\gamma$ 描述车辆相对目标方向及视线方向的偏差。该坐标在目标点有奇异性，但也因此避开了笛卡尔坐标下阻止连续时不变静态反馈稳定的特定拓扑障碍。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造角度反步变量并显式化严格反馈结构

引入有界光滑函数 $\psi_1,\psi_2$，再定义 $z=\gamma+\arctan(k_2\delta)$，使距离和极角方程出现期望衰减项以及由 $z$ 引起的残差。原视线角可由 $\gamma=z-\arctan(k_2\delta)$ 恢复，因此新系统仍由 $(\rho,\delta,z,v)$ 完全决定。

<div class="method-step__io" markdown="1">

**输入**：极坐标状态 $(\rho,\delta,\gamma,v)$ 和设计增益 $k_2>0$。<br>
**输出**：以 $z$ 为下一层误差的级联动力学，其中 $z=0$ 对应视线角跟随稳定极角所需的虚拟目标。

</div>

**直观理解**：反步法先假设后一级变量可以被直接指定，为前一级设计一个理想值，再把“实际值与理想值之差”作为新的误差继续控制。这里 $z$ 就是方向层的这种误差，$\arctan$ 同时限制了虚拟角度命令的幅值。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 为速度层设置虚拟目标并重参数化加速度

令 $\hat v=v-k_1N(k_2\delta)\rho$，把期望速度设为与剩余距离成比例的 $k_1N(k_2\delta)\rho$；再按式（13）把实际加速度 $a$ 写成新输入 $\tilde a$ 加上补偿项，使 $\dot{\hat v}=\tilde a$。变换后的距离和角度方程含显式线性衰减项，但仍存在由 $z$、$\hat v/\rho$ 及转向—速度耦合产生的残差。

<div class="method-step__io" markdown="1">

**输入**：状态 $(\rho,\delta,z,v)$、增益 $k_1>0$，以及 $N(s)=\sqrt{1+s^2}$。<br>
**输出**：状态 $(\rho,\delta,z,\hat v)$ 的反步中间系统，以及可继续设计的输入 $(\tilde a,\varphi)$。

</div>

**直观理解**：理想停车速度不应在目标附近仍保持常数，而应随着剩余距离缩小；$\hat v$ 衡量实际速度偏离这一减速规律多少。加速度补偿把复杂项预先抵消，使速度误差看起来像一个可直接控制的积分器。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按剩余距离归一化并整理最终控制坐标

定义 $\bar\delta=\delta/\rho$、$\bar z=z/\rho$、$\bar v=\hat v/\rho$，并通过式（18）和式（19）把 $\tilde a$、$\varphi$ 重写为新辅助输入 $\hat a$、$\tilde\varphi$ 与状态补偿项。所得系统满足 $\dot{\bar v}=\hat a$、$\dot{\bar z}=\tilde\varphi-(\varphi/L)\bar v$，而 $\rho$ 和 $\bar\delta$ 方程具有显式衰减主项及结构化耦合项。

<div class="method-step__io" markdown="1">

**输入**：中间状态 $(\rho,\delta,z,\hat v)$ 和输入 $(\tilde a,\varphi)$。<br>
**输出**：在 $\mathcal S$ 上演化的归一化状态 $(\rho,\bar\delta,\bar z,\bar v)$，以及留待最终反馈设计的辅助输入 $(\hat a,\tilde\varphi)$。

</div>

**直观理解**：除以 $\rho$ 后，控制器关心的不只是角度和速度是否趋于零，而是它们是否比剩余距离下降得足够快。这样可表达“到达前已经对正并减速”的停车规律，而不是到达目标后再试图原地转向。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 极坐标自行车动力学与转向输入映射

$$
\begin{aligned}
\phi&=\arctan(\varphi),\\
\dot\rho&=-v\cos\gamma,\\
\dot\delta&=\frac{v}{\rho}\sin\gamma,\\
\dot\gamma&=\frac{v}{\rho}\sin\gamma-\frac{v}{L}\varphi,\\
\dot v&=a.
\end{aligned}
$$

**符号说明**

- $\rho$：车辆位置到停车目标的距离，设计域内满足 $\rho>0$。
- $\delta$：目标中心极坐标的极角；对原点目标，定义为 $\operatorname{atan2}(y,x)+\pi$。
- $\gamma$：视线角，满足 $\gamma=\delta-\theta$，表示目标方向与车辆航向之间的关系。
- $v$：车辆前向速度，是系统状态而非直接控制输入。
- $a$：纵向加速度控制输入。
- $L$：车辆轴距。
- $\phi$：实际前轮转角，限制在 $(-\pi/2,\pi/2)$。
- $\varphi$：无约束辅助转向输入，通过反正切映射为实际转角。

<div class="equation-explanation" markdown="1">

**直观理解**：距离变化由速度在目标视线方向上的投影决定，方位角和视线角的变化则含有 $v/\rho$，因此接近目标时会出现显著耦合。车辆只有在 $v\neq0$ 时才能借助转向改变航向，这正是后续不能把方向控制与速度控制简单分开的原因。<br>
**原文位置**：第 II 节，式（2a）—（2d）；输入变换位于式（2）之前

</div>

</div>

<div class="equation-block" markdown="1">

#### 反步与距离归一化坐标变换

$$
\begin{aligned}
z&=\gamma+\arctan(k_2\delta),\\
\hat v&=v-k_1N(k_2\delta)\rho,\qquad N(s)=\sqrt{1+s^2},\\
\bar\delta&=\frac{\delta}{\rho},\\
\bar z&=\frac{z}{\rho},\\
\bar v&=\frac{\hat v}{\rho}=\frac{v}{\rho}-k_1N\!\left(k_2\rho\bar\delta\right),
\qquad k_1,k_2>0.
\end{aligned}
$$

**符号说明**

- $z$：角度反步误差；它把视线角与极角的有界虚拟稳定目标合并。
- $\hat v$：实际速度与期望距离比例速度 $k_1N(k_2\delta)\rho$ 之间的误差。
- $N(s)$：函数 $\sqrt{1+s^2}$，来自 $\arctan$ 的正弦、余弦恒等式，并始终满足 $N(s)\ge1$。
- $\bar\delta$：单位剩余距离对应的极角误差。
- $\bar z$：单位剩余距离对应的角度反步误差。
- $\bar v$：单位剩余距离对应的速度反步误差。
- $k_1$：速度—距离比例及距离衰减相关的正设计增益。
- $k_2$：极角虚拟反馈强度的正设计增益。

<div class="equation-explanation" markdown="1">

**直观理解**：前两行给方向和速度分别指定随状态变化的理想值，后三行再检查这些误差相对于剩余距离是否足够小。若只要求原角度和速度趋于零，它们可能在距离耗尽前下降得不够快；归一化坐标专门排除了这种不符合真实停车过程的尺度失配。<br>
**原文位置**：第 III-A 节式（9）、（10）、（12）；第 III-B 节式（15）—（17）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该工作是解析非线性反馈控制器设计，不涉及数据集、参数学习或数值优化训练；$k_1,k_2$ 是人工选择的正控制增益，而非通过损失函数训练得到的模型参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 极坐标与可行转向映射**

极坐标把停车目标表示为 $\rho\to0$、$\delta\to0$、$\gamma\to0$；输入映射 $\phi=\arctan(\varphi)$ 保证任意 $\varphi\in\mathbb R$ 都对应 $\phi\in(-\pi/2,\pi/2)$。该表示仅在 $\rho>0$ 有效，并在 $\rho=0$ 出现坐标奇异性。

> 直观理解：这一模块既把任务改写成“距离和角度误差归零”，也自动避免控制器命令超过模型允许的前轮转角。奇异性不是被消除，而是通过只在尚未到达目标的区域内设计闭环来处理。

**2. 非传统反步变换**

角度层采用 $z=\gamma+\arctan(k_2\delta)$，速度层采用 $\hat v=v-k_1N(k_2\delta)\rho$；$\psi_1$ 和 $\psi_2$ 将三角差分写成在零点具有光滑延拓且全局有界的残差。该结构提取出 $-k_1\rho$ 和 $-k_1k_2\delta$ 等稳定主项。

> 直观理解：作者不是直接抵消所有非线性，而是先安排方向和速度的理想演化，再逐层控制偏差。有界辅助函数保证角度很大或接近零时，相关三角残差仍可被统一分析。

**3. 距离归一化停车几何**

通过 $\bar\delta=\delta/\rho$、$\bar z=z/\rho$、$\bar v=\hat v/\rho$ 把应随距离同步衰减的量变成新的闭环状态；因为状态空间规定 $\rho>0$，该变换在设计域内有定义。输入重参数化进一步把最高层误差整理为由 $\tilde\varphi$ 和 $\hat a$ 驱动的形式。

> 直观理解：若 $\bar\delta$、$\bar z$、$\bar v$ 保持受控并趋于零，那么原角度与速度误差至少会随着距离一起缩小。这正对应车辆在最后一小段路程之前已基本对正并降速。

**训练与推理**

不适用机器学习意义上的训练或推理。在线控制时，应由测得的 $(x,y,\theta,v)$ 计算目标中心极坐标，再依次计算 $z$、$\hat v$ 和 $(\bar\delta,\bar z,\bar v)$，根据辅助反馈生成 $\hat a$ 与 $\tilde\varphi$，经式（18）、（19）、（13）逐层还原 $a$ 和 $\varphi$，最后输出 $a$ 与 $\phi=\arctan(\varphi)$。但所给节选没有给出 $\hat a$ 和 $\tilde\varphi$ 的最终闭环公式，因此该在线流程的最后反馈选择原文在当前材料中未明确报告。

**复现信息**

实现必须保持在 $\rho>0$ 的极坐标设计域内，并一致处理 $\operatorname{atan2}$ 的分支，因为该坐标变换在负 $x$ 轴相应切线上不连续、在目标点未定义。计算 $\psi_1(r,s)=[\cos(r-s)-\cos s]/r$ 和 $\psi_2(r,s)=[\sin(r-s)+\sin s]/r$ 时，接近 $r=0$ 应使用其光滑延拓 $\psi_1(0,s)=\sin s$、$\psi_2(0,s)=\cos s$，避免直接相除造成数值不稳定。除 $k_1,k_2>0$、轴距 $L$ 和上述坐标定义外，当前节选未明确报告增益选取、离散控制周期、执行器饱和处理或最终辅助反馈参数。

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

原文未明确报告，或这里不需要额外前置概念。

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 从 x0=0、y0=±1、θ0=0 出发，分别执行前进和倒车平行停车仿真；目标为 x*=y*=θ*=v*=0。

<div class="result-value" markdown="1">

作者报告，Fig. 2 和 Fig. 3 中的闭环轨迹清楚呈现了类似人类驾驶员的平行停车行为。

</div>

该结果说明反馈律不仅在变换坐标中具有理论稳定性，而且能在所选初始状态和增益下生成具有直观停车形态的空间轨迹。不过，“类似人类”仅是作者对图形的定性判断；原文没有用户研究、轨迹相似度、停车时间、终端误差或舒适性指标，因此不能据此证明其总体上优于其他停车控制器。

<div class="result-source" markdown="1">

来源：Section V, Fig. 2 and Fig. 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

These trajectories clearly exhibit human-like parallel parking behavior.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 采用文中式（12）对应的闭环速度动态，并在上述平行停车初始条件下运行反馈控制器。

<div class="result-value" markdown="1">

作者指出，速度 v 被吸引到正流形 N(k2δ)ρ，使反馈控制倾向于前进运动。

</div>

这解释了轨迹为何会自然偏向以向前行驶完成位置调整：控制器的内部几何结构形成了一个期望速度流形，而不是依靠预先规划并切换前进、倒车动作。该陈述主要是由闭环结构和仿真现象支持的机制解释，并非与不含该流形的控制器进行对比后得到的实验结论。

<div class="result-source" markdown="1">

来源：Section V，引用式（12）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Furthermore, by (12), the speed v is attracted to the positive manifold $N(k_{2}\delta)\rho$, which causes the feedback to favor forward motion.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 检查上述前进和倒车停车仿真中的控制输入时间历程。

<div class="result-value" markdown="1">

Fig. 4 中的控制输入保持平滑，并满足预先规定的输入边界。

</div>

平滑且有界的输入意味着仿真中没有明显的不连续控制切换，并符合论文对可实施反馈的设计目标。由于节选未列出具体边界数值、输入峰值或执行器模型，该结果只能确认图示案例满足作者规定的界限，不能证明真实车辆执行器在延迟、饱和和噪声下仍可准确实现。

<div class="result-source" markdown="1">

来源：Section V, Fig. 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The inputs in Fig. 4 remain smooth and satisfy the prescribed bounds.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验没有设置任何基线控制器，也没有报告停车成功率、终端位姿误差、收敛时间、路径长度或控制能量，因此无法量化其相对性能。
- 验证仅限少量理想模型仿真；原文节选未报告参数不确定性、传感噪声、执行器动态、障碍物、碰撞约束或真实车辆实验，因而不能从现有结果判断实际部署的鲁棒性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。

**实验想回答的问题**

- 所提出的平滑反馈控制律能否从停车位上下两侧、以前进或倒车方式出发，将运动学自行车模型引导至原点处的目标平行停车位姿？
- 闭环轨迹是否呈现类似人类驾驶员的平行停车行为，同时保持控制输入平滑并满足预设边界？

**实验实现**

实验为运动学自行车模型的仿真案例，不涉及数据集划分或学习训练。目标构型设为 x*=y*=θ*=v*=0，其中黑色箭头表示目标航向。初始位置取 x0=0、y0=±1，初始航向均为 θ0=0，以检验车辆从停车位两侧出发时的对称情形。每个 y0 分别仿真一次前进与一次倒车操作：前进操作采用 v0=0，以及 k1=0.6、k2=1.4、k3=1、k4=2；倒车操作采用 v0=-1.6，以及 k1=1.2、k2=1.5、k3=0.4、k4=0.8。Fig. 2 和 Fig. 3 展示车辆轨迹，Fig. 4 展示控制输入。原文未给出仿真时长、积分器、采样周期、数值误差、车辆几何参数，也未设置定量评价指标或对照控制器。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 平行停车案例以原点为目标车位，车辆从横向偏移 y0=1 或 y0=-1 的位置出发，并分别测试前进与倒车初始速度。轨迹图用于观察车辆能否仅依靠状态反馈形成接近人类驾驶的转向—对准—入位过程，输入图则检查平滑性和边界约束。该案例直观展示了控制器行为，但不是覆盖不同车位尺寸、初始航向、障碍物或模型扰动的系统性基准测试。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops a feedback-control method for globally stabilizing a car-like robotic system during parking maneuvers.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`d94c73246af2f57cc54aabc96e56305598ed6d452da587aee1edf32be601d7f9`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
