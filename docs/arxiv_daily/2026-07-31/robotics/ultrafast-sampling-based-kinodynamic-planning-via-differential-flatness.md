---
title: "[论文解读] Ultrafast Sampling-based Kinodynamic Planning via Differential Flatness"
description: "[arXiv 2603.16059][机器人 / 具身智能] 本文提出 FLASK：利用微分平坦性把非线性机器人动力学规划转化为平坦输出空间中的解析边值问题，并结合 SIMD 并行轨迹验证，使采样式规划器能够快速生成动力学可行的运动轨迹。"
arxiv_id: "2603.16059"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T05:30:51.508914+00:00"
source_sha256: "4b2e8345462b0a131c8eab06d85d1fdd5f54078ca6e4a290077eb9a77d2cc75b"
tags:
  - "机器人 / 具身智能"
  - "动力学运动规划"
  - "采样式运动规划"
  - "微分平坦性"
  - "两点边值问题"
  - "闭式轨迹"
  - "SIMD 并行"
  - "碰撞检测"
  - "高自由度机器人"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2603.16059</p>

# Ultrafast Sampling-based Kinodynamic Planning via Differential Flatness

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Duong, Thai, Ramsey, Clayton W., Kingston, Zachary, Thomason, Wil, Kavraki, Lydia E.</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Department of Computer Science, Rice University；Ken Kennedy Institute</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2603.16059) · [PDF 下载](https://arxiv.org/pdf/2603.16059) · **关键词** 动力学运动规划, 采样式运动规划, 微分平坦性, 两点边值问题, 闭式轨迹, SIMD 并行, 碰撞检测, 高自由度机器人<br>


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

本文提出 FLASK：利用微分平坦性把非线性机器人动力学规划转化为平坦输出空间中的解析边值问题，并结合 SIMD 并行轨迹验证，使采样式规划器能够快速生成动力学可行的运动轨迹。

**不用术语来说**：机器人在杂乱或变化的环境中不能只规划一条避开障碍物的空间曲线，因为电机能力、速度、加速度和系统动力学可能使机器人无法准确跟随这条曲线，甚至造成碰撞；但若在搜索过程中逐段求解动力学或反复进行数值仿真，计算又会慢到难以支持实时反应。本文要解决的是：怎样兼顾复杂环境中的快速搜索与机器人真正可执行的运动。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出适用于广泛微分平坦机器人系统的 FLASK 框架：在平坦输出空间中构造具有显式时间参数的闭式局部轨迹，再将其映射回原状态与控制空间，从而使采样式规划器生成的轨迹按构造即满足动力学约束。
- 把闭式多项式局部轨迹与细粒度 SIMD 并行验证结合起来，使多个时间样本的碰撞检查能够批量执行；该接口可集成到 RRT-Connect、SST* 等采样式规划器中，并以闭式边值问题解为基础讨论概率穷尽性和渐近最优性保证。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于机器人动力学运动规划领域。目标是在存在障碍物的环境中，为机械臂、地面车辆或飞行器等机器人快速生成从起始状态到目标状态的无碰撞轨迹，并保证轨迹满足机器人动力学、关节角和速度等约束。仅考虑构型与障碍物关系的几何规划可能产生控制器无法准确跟踪的路径，尤其在高速运动时会带来碰撞风险；但传统动力学规划通常需要反复求解两点边值问题或数值积分动力学，计算开销较大。本文关注的核心背景是：如何利用微分平坦性得到闭式、带时间参数的局部轨迹，再以单指令多数据并行方式同时检查大量轨迹采样点，从而把采样式规划的速度优势扩展到动力学约束场景。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**动力学运动规划（kinodynamic planning）**

规划器不仅要避开障碍物，还要直接保证轨迹满足机器人的运动微分方程以及速度、控制输入等约束。其输出是机器人在动力学上能够执行的带时间轨迹，而不只是构型空间中的几何曲线。

</div>
<div class="concept-item" markdown="1">

**微分平坦性（differential flatness）**

若一个系统是微分平坦的，则可选择一组平坦输出，使原系统的状态与控制输入都能由这些输出及其有限阶时间导数表示。通俗地说，规划器可以先在更容易处理的输出空间中设计曲线，再把它精确转换成满足原机器人动力学的轨迹。

</div>
<div class="concept-item" markdown="1">

**两点边值问题（two-point boundary value problem, BVP）**

该问题要求寻找一段满足系统动力学、同时连接给定起点状态与终点状态的局部轨迹，是采样式动力学规划连接节点时的关键子问题。一般非线性系统中的数值求解代价高，而本文利用微分平坦性在平坦输出空间中获得解析的时间参数化解。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括微分平坦机器人的动力学模型及其平坦输出表示、起始状态、目标状态、障碍环境，以及需要满足的动力学和状态约束；适用对象覆盖文中所述的机械臂、地面车辆和飞行器等全驱动或欠驱动系统。规划器在平坦输出空间中采样节点，并以闭式时间参数化多项式求解节点之间的局部连接；随后把平坦输出轨迹及其导数映射回原状态与控制空间，并并行执行正运动学、碰撞及约束验证。输出是从起点到目标点的连续、无碰撞且按构造满足动力学的可执行轨迹。该设置假设机器人具有已知且可用的微分平坦表示；本文并非为任意不具备该性质的非线性系统提供通用解析连接器。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x(t)$**

机器人在时间 $t$ 的原始系统状态，例如机械臂的关节位置与速度；此处为依据正文术语整理的通用记号，节选未明确给出作者的符号定义。

</div>
<div class="notation-item" markdown="1">

**$u(t)$**

机器人在时间 $t$ 的控制输入；对微分平坦系统，它可由平坦输出及有限阶导数恢复，节选未明确给出作者的具体符号。

</div>
<div class="notation-item" markdown="1">

**$y(t)$**

时间 $t$ 的平坦输出；规划首先在该空间中构造闭式局部轨迹，节选未明确给出作者采用的具体符号。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{DOF}$**

机器人的自由度数量；高自由度意味着状态或构型维数较高，通常会显著增加搜索、正运动学和碰撞检测成本。

</div>

</div>

**直接相关的工作**

- **VAMP（Thomason et al., 2024）**: 该工作利用细粒度 SIMD 并行显著加速采样式运动规划与碰撞检测，但原文将其定位为几何规划方法。FLASK 借鉴这种并行验证思路，并通过平坦输出空间中的闭式时间轨迹加入动力学可行性。
- **SST*（Li et al., 2016）**: SST* 是面向动力学系统的采样式规划器，相关方法通常通过采样控制并向前传播动力学来扩展搜索。FLASK 可与 SST* 等规划器结合，以闭式边值连接或连续动力学传播支持规划，并讨论概率穷尽性与渐近最优性保证。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

实时机器人任务要求系统在障碍密集或动态变化的环境中迅速重新规划，同时保证所得轨迹无碰撞、满足动力学并可由控制器准确跟踪。对机械臂等高自由度机器人而言，若只生成几何路径，快速运动时的实际轨迹可能偏离规划路径；若在规划内完整处理动力学，每次树或图扩展的代价又会成为实时规划的主要瓶颈。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **优化式与搜索式动力学规划**：优化式方法把碰撞、机器人动力学以及关节位置和速度限制共同写入非线性轨迹优化问题；搜索式方法则在离散状态格点或运动基元图上搜索从起点到目标的可行序列。前者直接联合求解整条轨迹，后者借助离散结构获得系统化搜索及一定的最优性保证。
- **采样式动力学规划与并行几何规划**：采样式动力学规划通过随机采样扩展树或图；由于状态间的两点边值问题难解，常改为随机采样控制并数值积分动力学，或仅对简单、线性化系统求解边值问题，也有工作用神经网络近似局部连接。另一条路线通过 SIMD 等并行技术同时检查大量样本，把几何或运动学规划加速到很短时间，但通常不直接保证动力学可行性。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有动力学规划存在稳健性或扩展性问题：非线性优化容易陷入局部极小值并依赖初始解，格点或运动基元搜索受到维数灾难影响；采样式方法若使用随机控制传播，则容易扩展到与目标无关的状态区域，导致路径更长、搜索时间增加，而近似或线性化连接又不能为一般非线性系统提供精确局部轨迹。
- 现有高速并行方法主要解决几何或运动学规划。直接并行检查动力学轨迹并不简单，因为检查前必须获得满足动力学且带有时间参数的连续轨迹；此外，前向运动学和碰撞检测对高自由度机器人尤其昂贵，因此已有微分平坦轨迹设计也未自然消除整体规划中的验证瓶颈。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前缺少一种统一接口，能够针对一般的非线性微分平坦机器人，在采样式规划的每次局部连接中精确而解析地处理动力学，同时把连续轨迹转化为适合批量并行碰撞检查的表示，并且不牺牲采样式规划器所需的理论性质与算法兼容性。

</div>
<div markdown="1"><span>核心问题</span>

能否利用微分平坦性，为不同类型的机器人构造闭式、时间参数化且动力学可行的局部连接，并据此把 SIMD 加速从几何规划推广到具有概率穷尽性和渐近最优性依据的超快速采样式动力学规划？

</div>
<div markdown="1"><span>作者直觉</span>

微分平坦系统的状态和控制可以由一组平坦输出及其有限阶导数表示，因此可先绕开原始非线性动力学，在更容易处理的平坦输出空间内用多项式解析连接两个边界状态。因为多项式能在任意给定时刻直接求值，无须逐步数值积分，所以许多轨迹、许多时间点可以用同一条指令并行计算和检查；随后再通过平坦映射恢复原系统的状态与控制，便可同时获得快速验证和动力学可行性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

FLASK 的核心做法是利用微分平坦性，把原状态空间 $\mathcal{X}$ 中受非线性机器人动力学约束的规划问题，变换到平坦状态空间 $\mathcal{Z}$ 中的线性规划问题。对 $n$ 维平坦输出 $\mathbf{y}$，方法把其直到 $r-1$ 阶的导数组合成平坦状态 $\mathbf{z}=(\mathbf{y},\dot{\mathbf{y}},\ldots,\mathbf{y}^{(r-1)})$，并将第 $r$ 阶导数 $\mathbf{w}=\mathbf{y}^{(r)}$ 作为伪控制。由此得到带幂零矩阵 $\mathbf{A}$ 的链式积分器动力学。采样规划器每次扩展图或树时，可以选择采样终点并闭式求解两点边值问题，也可以采样恒定伪控制并解析传播动力学；生成的局部轨迹是显式多项式，因此适合用 SIMD 并行执行约束与碰撞检查。

端到端地看，输入是初始状态及控制、目标区域及期望控制和最大迭代次数；算法先把起点和目标映射到平坦状态空间，再调用任意兼容的采样式规划器，以 FlaskExtend 生成候选局部边，以 FlaskCC 验证候选边，最终在规划图中提取连续分段多项式轨迹。之后通过微分平坦性的恢复映射 $\boldsymbol{\alpha}$ 与 $\boldsymbol{\beta}$，把平坦轨迹和伪控制转换为原系统的状态轨迹 $\boldsymbol{\sigma}(t)$ 与真实控制 $\mathbf{u}(t)$。直观而言，FLASK 不是直接反复数值求解复杂机器人的非线性运动，而是先换到一个“容易画多项式曲线”的坐标系中规划，再把曲线精确翻译回机器人可执行的运动。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 起点与目标的平坦化

利用平坦输出映射 $\mathbf{h}$ 计算起始平坦输出 $\mathbf{y}_s$ 和目标平坦输出集合 $\mathcal{G}_{\mathbf{y}}$，再将输出及其直到 $r-1$ 阶的导数组合为 $\mathbf{z}_s$ 与 $\mathcal{G}_{\mathbf{z}}$。对于平坦输出不依赖控制的常见系统，不必指定起点和目标控制。

<div class="method-step__io" markdown="1">

**输入**：初始状态 $\mathbf{x}_s$、初始控制及其所需导数，目标区域 $\mathcal{G}$、目标控制及其所需导数。<br>
**输出**：平坦空间中的初始节点 $\mathbf{z}_s$ 和目标区域 $\mathcal{G}_{\mathbf{z}}$。

</div>

**直观理解**：这一步相当于把机器人的原始坐标翻译成一种更容易规划的坐标；位置、速度等必要导数被打包成一个新状态。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立平坦状态规划图

以 $\mathbf{z}_s$ 初始化图或树 $\mathbb{G}_{\mathbf{z}}=(\mathbb{V}_{\mathbf{z}},\mathbb{E}_{\mathbf{z}})$，随后重复调用 FlaskExtend。FLASK 只替换规划器中处理动力学连接和验证的原语，因此可嵌入多种采样式规划方法，而不绑定某一种树或图搜索策略。

<div class="method-step__io" markdown="1">

**输入**：初始平坦状态 $\mathbf{z}_s$、目标区域 $\mathcal{G}_{\mathbf{z}}$、最大迭代次数 $I$，以及所选采样式规划器的采样与选点规则。<br>
**输出**：逐步扩展的平坦状态规划图 $\mathbb{G}_{\mathbf{z}}$。

</div>

**直观理解**：规划器仍负责决定“下一步尝试去哪里”，FLASK 则负责快速回答“怎样动态可行地过去”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 闭式生成局部动态连接

终点采样分支求解线性二次最短时间问题，在固定或优化的 $T$ 下得到闭式伪控制 $\mathbf{w}_{loc}(t)$ 和局部路径 $\mathbf{z}_{loc}(t)$；控制采样分支则对线性平坦动力学作解析传播。由于 $\mathbf{A}^r=0$，矩阵指数截断为有限多项式，使局部输出成为显式多项式。

<div class="method-step__io" markdown="1">

**输入**：已有节点 $\mathbf{z}_0$，以及采样终点 $\mathbf{z}_f$ 和时长 $T$，或采样的恒定伪控制 $\mathbf{w}_0$ 与时长 $T$。<br>
**输出**：定义在 $t\in[0,T]$ 上的候选局部平坦路径 $\mathbf{z}_{loc}(t)$、伪控制 $\mathbf{w}_{loc}(t)$ 及其时长。

</div>

**直观理解**：通常连接两个动态状态需要运行数值求解器；这里利用特殊坐标结构，直接写出连接曲线的公式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 并行约束验证与图更新

FlaskCC 将候选轨迹恢复到机器人状态和控制层面，并对碰撞、状态可行域及控制约束进行验证；显式多项式允许在多个时间样本或候选上进行 SIMD 并行计算。若候选有效，则把 $\mathbf{z}_f$ 加入顶点集，并把携带局部轨迹、伪控制和时长的连接加入边集。

<div class="method-step__io" markdown="1">

**输入**：候选局部平坦路径 $\mathbf{z}_{loc}(t)$ 和伪控制 $\mathbf{w}_{loc}(t)$。<br>
**输出**：仅包含通过验证的新增节点和局部边的规划图。

</div>

**直观理解**：这像是同时在许多时刻检查整段动作是否撞障碍、超速度或超控制范围；只有通过全部检查的路段才进入地图。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 平坦状态的线性动力学

$$
\mathbf{w}=\mathbf{y}^{(r)},\quad r\geq\max(l,m),\qquad \mathbf{z}=(\mathbf{y},\dot{\mathbf{y}},\ldots,\mathbf{y}^{(r-1)}),\qquad \dot{\mathbf{z}}=\mathbf{A}\mathbf{z}+\mathbf{B}\mathbf{w},\quad \mathbf{A}^{r}=0
$$

**符号说明**

- $\mathbf{y}\in\mathbb{R}^{n}$：维数为 $n$ 的平坦输出，可用于恢复原系统状态和控制。
- $r$：选取的伪控制导数阶数，不小于状态恢复与控制恢复所需的最高导数阶。
- $l,m$：微分平坦性恢复关系中，分别与所需平坦输出导数阶数有关的阶数。
- $\mathbf{w}\in\mathbb{R}^{n}$：伪控制输入，即平坦输出的第 $r$ 阶导数。
- $\mathbf{z}\in\mathbb{R}^{rn}$：由平坦输出及其零阶至 $r-1$ 阶导数组成的平坦状态。
- $\mathbf{A}\in\mathbb{R}^{rn\times rn}$：链式积分器的状态矩阵，其超对角块为单位矩阵，并满足幂零性质。
- $\mathbf{B}\in\mathbb{R}^{rn\times n}$：把伪控制注入最高阶导数分量的输入矩阵。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把平坦输出的连续求导关系写成标准线性系统。关键是 $\mathbf{A}^r=0$，因此 $e^{\mathbf{A}t}$ 只包含有限项，不必近似无限级数；局部轨迹和控制由此可以写成多项式闭式表达，并被快速批量求值。<br>
**原文位置**：第 V-A 节，式（14）—（16）

</div>

</div>

<div class="equation-block" markdown="1">

#### 局部连接的线性二次最短时间目标及闭式解

$$
\begin{aligned}
\min_{\mathbf{w}(t),T}\quad &\mathcal{C}=\int_{0}^{T}\mathbf{w}^{\top}\mathbf{R}\mathbf{w}\,dt+\rho T\\
\mathrm{s.t.}\quad &\dot{\mathbf{z}}=\mathbf{A}\mathbf{z}+\mathbf{B}\mathbf{w},\quad \mathbf{z}(0)=\mathbf{z}_{0},\quad \mathbf{z}(T)=\mathbf{z}_{f},\\
\mathbf{d}_{T}=&\mathbf{z}_{f}-e^{\mathbf{A}T}\mathbf{z}_{0},\quad
\mathbf{G}_{T}=\int_{0}^{T}e^{\mathbf{A}t}\mathbf{B}\mathbf{R}^{-1}\mathbf{B}^{\top}e^{\mathbf{A}^{\top}t}\,dt,\\
\mathbf{w}_{loc}(t)=&\mathbf{R}^{-1}\mathbf{B}^{\top}e^{\mathbf{A}^{\top}(T-t)}\mathbf{G}_{T}^{-1}\mathbf{d}_{T},\\
\mathbf{z}_{loc}(t)=&e^{\mathbf{A}t}\mathbf{z}_{0}+\mathbf{G}_{t}e^{\mathbf{A}^{\top}(T-t)}\mathbf{G}_{T}^{-1}\mathbf{d}_{T},\\
\mathcal{C}_{loc}(T)=&\mathbf{d}_{T}^{\top}\mathbf{G}_{T}^{-1}\mathbf{d}_{T}+\rho T.
\end{aligned}
$$

**符号说明**

- $\mathbf{z}_{0},\mathbf{z}_{f}$：局部连接的起始平坦状态和终止平坦状态。
- $T>0$：局部轨迹持续时间，可固定、采样或通过时间最优条件求解。
- $\mathbf{R}\succ0$：用户指定的正定伪控制代价权重矩阵。
- $\rho$：时间惩罚系数，控制减少控制消耗与缩短运动时间之间的折中。
- $\mathbf{d}_{T}$：在无控制自然演化之后，终点条件仍需由控制补偿的状态差。
- $\mathbf{G}_{T}$：时长 $T$ 上的加权可控 Gramian，描述伪控制影响各平坦状态分量的能力。
- $\mathbf{w}_{loc}(t)$：在固定时长和端点条件下使伪控制能量最小的局部伪控制。
- $\mathbf{z}_{loc}(t)$：连接两个平坦状态的最优局部轨迹。
- $\mathcal{C}_{loc}(T)$：给定时长下局部连接的最优控制代价与时间代价之和。

<div class="equation-explanation" markdown="1">

**直观理解**：目标函数既惩罚伪控制过大，也惩罚轨迹耗时过长。在线性平坦动力学下，给定端点和时长即可通过 Gramian 直接写出最优控制及路径；若还需优化时长，只需在一维变量 $T$ 上求 $d\mathcal{C}_{loc}(T)/dT=0$，而不必联合数值优化整条高维轨迹。该闭式解本身不纳入碰撞、速度或加速度上限，FLASK 会在之后把违反约束的候选边判为无效。<br>
**原文位置**：第 V-C.1 节，式（20）—（25）；可变时长条件见式（26）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。FLASK 是解析建模与采样式运动规划框架，不涉及数据驱动模型训练；式（20）—（21）的“目标”是每条局部边的最优控制目标，而不是机器学习损失。固定 $T$ 时通过闭式解最小化伪控制能量，时间可变时再求使 $\mathcal{C}_{loc}(T)$ 驻定的正时长；碰撞和其他硬约束不进入该无约束局部优化，而在 FlaskCC 中作为候选有效性条件处理。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 平坦状态线性化**

选择满足微分平坦性的输出 $\mathbf{y}$，令 $\mathbf{w}=\mathbf{y}^{(r)}$ 且 $r\geq\max(l,m)$，并构造 $\mathbf{z}=(\mathbf{y},\dot{\mathbf{y}},\ldots,\mathbf{y}^{(r-1)})$。这样原系统的状态和控制可由 $\boldsymbol{\alpha}(\mathbf{z},\mathbf{w})$、$\boldsymbol{\beta}(\mathbf{z},\mathbf{w})$ 恢复，而规划动力学变为 $\dot{\mathbf{z}}=\mathbf{A}\mathbf{z}+\mathbf{B}\mathbf{w}$；其中 $\mathbf{A}$ 为幂零矩阵，使矩阵指数成为有限阶多项式。

> 直观理解：这是全部加速的前提：它把复杂非线性动力学改写成连续积分的位置—速度—加速度链，同时保留返回真实机器人运动的确定映射。

**2. FlaskExtend**

该模块提供两类扩展。BVP 分支在给定 $\mathbf{z}_0$、$\mathbf{z}_f$ 和 $T$ 时，最小化伪控制能量与时间惩罚之和，并通过可控 Gramian 得到闭式最优控制和轨迹；若时间可变，则求解 $d\mathcal{C}_{loc}(T)/dT=0$，其中常见的 $r=2$ 情形可化为关于正时长的四次多项式。传播分支对采样的恒定 $\mathbf{w}_0$ 解析积分，避免逐步数值仿真。

> 直观理解：它是规划器的“快速接线器”：既能精确连接两个采样状态，也能从当前状态按给定动作向前推演，而且两种方式都不需要昂贵的通用动力学求解。

**3. FlaskCC**

该模块接收显式的 $\mathbf{z}_{loc}(t)$ 与 $\mathbf{w}_{loc}(t)$，利用平坦性恢复映射计算原状态和控制，并并行验证碰撞及可行性约束。原文节选说明其使用 SIMD 并行化正向运动学和碰撞检查，但所给节选未包含第 V-D 节的具体采样密度、并行布局或误差处理细节。

> 直观理解：闭式轨迹不仅生成快，也能在许多检查点上批量求值；该模块把这种规则计算结构转化为硬件并行速度。

**训练与推理**

不存在训练阶段。规划时，用户提供具体机器人的平坦输出映射 $\mathbf{h}$、状态恢复映射 $\boldsymbol{\alpha}$、控制恢复映射 $\boldsymbol{\beta}$、起点、目标和约束；算法把问题转到平坦状态空间并初始化规划图。每次迭代由宿主采样式规划器选择样本或伪控制，FlaskExtend 解析生成局部多项式，FlaskCC 并行验证，合法边被加入图中。到达目标区域后，算法回溯图上的边，拼接平坦轨迹并恢复原状态与控制；达到最大迭代次数仍未到达目标时返回失败。

**复现信息**

公平复现首先要求研究对象确实是微分平坦系统，并能明确实现 $\mathbf{h}$、$\boldsymbol{\alpha}$ 和 $\boldsymbol{\beta}$；还需选定足以恢复状态与控制的阶数 $r\geq\max(l,m)$。BVP 分支必须指定正定矩阵 $\mathbf{R}$、时间权重 $\rho$，以及采用固定、采样还是优化时长 $T$；一般 $r$ 下可用数值求根，常见 $r=2$ 情形可求关于正根的四次多项式。候选轨迹必须在原状态和控制空间检查碰撞、状态可行域与控制限制，因为闭式 LQMT 解本身未纳入这些约束。所给节选未提供 FlaskCC 的离散检查分辨率、SIMD 硬件映射、数值容差和完整后处理规则，因此这些项目不能从当前材料中可靠补全。

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

**近似失败概率 $1-P({\cal A}_N)$**

衡量在平坦状态空间中，含 $N$ 个节点的规划图未能形成目标轨迹之 $(\varepsilon,\zeta_N,\eta_N)$-近分段迹线的概率。 （越低越好；该概率趋于 $0$ 表明增加样本后，规划图以高概率能够逼近任意满足安全裕度条件的轨迹。）

</div>
<div class="metric-item" markdown="1">

**单段代价界 $\zeta_N$**

限制拼接轨迹中每条局部边值问题轨迹的最大代价，其量级为 $(\log N/N)^{1/D}$。 （越低越好；$\zeta_N\to0$ 表示随着采样加密，组成近似轨迹的局部段越来越细。）

</div>
<div class="metric-item" markdown="1">

**轨迹偏离界 $\eta_N$**

限制分段迹线上的点到目标轨迹的最大几何距离；原始状态空间中的对应界为 $L_{\boldsymbol{\alpha}}\eta_N$。 （越低越好；该界趋于 $0$ 表示拼接轨迹在空间上逐渐贴近参考轨迹。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 平坦状态空间中的概率穷尽性

<div class="result-value" markdown="1">

定理 1(i) 给出失败概率 $1-P({\cal A}_N)=O(N^{-\kappa/D}\log^{-1/D}N)$。因此当 $\kappa>0$ 且 $N\to\infty$ 时，找到 $(\varepsilon,\zeta_N,\eta_N)$-近分段迹线的概率趋近于 $1$；其中 $\zeta_N=(1+\kappa)^{1/D}C_{{\cal Z}_{free}}(\log N/N)^{1/D}$，且 $\eta_N=C_p\zeta_N$。

</div>

作者的理论结论是：只要参考轨迹与障碍保持正安全裕度，采样足够多时，图中几乎必然出现一串闭式动力学可行局部轨迹，在代价和几何位置上逼近它。该结论证明的是渐近概率保证，不说明有限样本下需要多少时间或节点，也不是实际成功率测量。

<div class="result-source" markdown="1">

来源：第 VI-A 节，定理 1(i)，式 (33)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

There exists a constant $C_{\mu}$ such that as $N\rightarrow\infty$, the probability that ${\cal A}_{N}$ does not occur is bounded as: $1-P({\cal A}_{N})=O\left(N^{-\kappa/D}\log^{-1/D}{N}\right)$.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 从平坦状态空间转移到原始状态空间

<div class="result-value" markdown="1">

若状态恢复映射 $\boldsymbol{\alpha}:{\cal Z}\to{\cal X}$ 的 Lipschitz 常数为 $L_{\boldsymbol{\alpha}}$，则原始状态空间中存在 $(\varepsilon,\zeta_N,L_{\boldsymbol{\alpha}}\eta_N)$-近分段迹线的失败概率同样满足 $1-P({\cal B}_N)=O(N^{-\kappa/D}\log^{-1/D}N)$。

</div>

这说明平坦空间中的逼近不会在映射回真实机器人状态后失去概率收敛性质；映射最多把几何误差放大 $L_{\boldsymbol{\alpha}}$ 倍。它依赖 Lipschitz 连续和阶数条件，不能自动覆盖映射奇异、不连续或不满足假设的系统。

<div class="result-source" markdown="1">

来源：第 VI-A 节，定理 1(ii)，式 (34)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Then, the probability that ${\cal B}_{N}$ does not occur is bounded as: $1-P({\cal B}_{N})=O\left(N^{-\kappa/D}\log^{-1/D}{N}\right)$.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 由局部可控性与椭球覆盖支持渐近逼近

<div class="result-value" markdown="1">

平坦空间线性系统的可控性指标均为 $\nu_1=\cdots=\nu_n=r$，从而在 $T\to0$ 时 Gramian 行列式满足 $\det(\mathbf G_T)=\Theta(T^{r^2n})$，并得到局部覆盖椭球体积下界 $\mu({\cal E}_{\psi})\ge C_1\mu({\cal S}_{rn})\psi^{rn}T^{r^2n/2}$。作者据此建立有限椭球覆盖，并衔接概率穷尽性证明。

</div>

直观上，动力学局部轨迹不能像几何规划中的直线边那样简单地装进球内，因此论文改用由可控 Gramian 决定的椭球。体积下界保证这些椭球不会收缩得过快，使随机样本仍有足够概率落入覆盖参考轨迹的区域。这是证明机制，不是速度、成功率或轨迹质量的经验测量。

<div class="result-source" markdown="1">

来源：第 VI-A 节，式 (36)–(37)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Due to the controllability indices in Eq. 36, the determinant of the Gramian matrix $\mathbf{G}_{T}$ (22) is $\Theta(T^{\sum_{i}^{n}\nu_{i}^{2}})=\Theta(T^{r^{2}n})$ as $T\rightarrow 0$ according to Lemma III.4 in [schmerling2015optimal_drift], i.e., there exist constants $T_{0},C_{1},C_{2}>0$ such that $C_{1}T^{r^{2}n}\leq\det(\mathbf{G}_{T})\leq C_{2}T^{r^{2}n},\quad\forall T<T_{0}$.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给材料未包含经验实验章节，因此无法核验摘要中关于微秒至毫秒规划时间、仿真基准、真实机器人、拥挤环境或动态环境的陈述，也无法比较 FLASK 与其他规划器的速度、成功率和轨迹代价。
- 理论保证依赖多项条件：参考轨迹须有正的 $\delta$ 安全裕度，伪控制阶数须满足 $r>l$，平坦系统须可控，且从平坦状态到原始状态的映射须为 Lipschitz 连续。结果是 $N\to\infty$ 下的渐近结论，未给出有限计算预算下的实用误差界或样本复杂度保证。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。

**实验想回答的问题**

- 随着规划图样本数 $N$ 增大，FLASK 能否以趋近于 $1$ 的概率，用闭式边值问题解拼接出任意具有 $\delta$ 安全裕度轨迹的近似轨迹？
- 平坦状态空间中的概率穷尽性是否能通过 Lipschitz 连续映射 $\boldsymbol{\alpha}:{\cal Z}\to{\cal X}$ 转移到机器人原始状态空间，并进一步支持渐近最优性结论？

**实验实现**

所给章节是理论分析而非经验实验，没有报告数据集、训练—测试划分、硬件、重复次数、统计置信区间或与其他规划器的运行时间对比。分析对象是 FLASK 生成的随机规划图 $\mathbb{G}_{\mathbf z}=(\mathbb{V}_{\mathbf z},\mathbb{E}_{\mathbf z})$，其中 $N=|\mathbb{V}_{\mathbf z}|$。定理假设伪控制阶数 $r$ 严格大于状态恢复所需阶数 $l$，采用最优持续时间 $T^*$ 的闭式边值问题解与式 (20) 的代价，并要求参考轨迹在平坦自由空间中具有 $\delta>0$ 的安全裕度。由平坦空间转回原始状态空间时，还要求恢复映射 $\boldsymbol{\alpha}$ 为 Lipschitz 连续。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 图 4 是理论示意而非实际机器人案例：图 4(a) 描绘采样增加后分段轨迹逼近具有 $\delta$ 安全裕度的参考轨迹；图 4(b) 描绘安全裕度 $\delta_N$、局部代价界 $\zeta_N$ 和偏离界 $\eta_N$ 同时趋于 $0$ 时，规划结果依概率收敛到最优轨迹。该图解释收敛逻辑，但不提供有限样本实验数据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出利用微分平坦性实现超高速并行采样式机器人动力学运动规划的方法。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`4b2e8345462b0a131c8eab06d85d1fdd5f54078ca6e4a290077eb9a77d2cc75b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
