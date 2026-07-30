---
title: "[论文解读] Time-delay Control Using a New Nonlinear Adaptive Law for Cable-Driven Robots"
description: "[arXiv 2607.26383][机器人 / 具身智能] 本文针对绳驱动机器人在时变不确定性、运动换向和测量噪声下难以兼顾跟踪精度与抖振抑制的问题，提出一种将时延估计、分数阶非奇异终端滑模和非线性自适应律结合的控制策略。"
arxiv_id: "2607.26383"
announcement_date: "2026-07-30"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T07:32:04.187448+00:00"
source_sha256: "85198c9fde085f278af0195450e120cdd51972836cfdcc11d757b860414c3316"
tags:
  - "机器人 / 具身智能"
  - "缆索驱动机器人"
  - "轨迹跟踪控制"
  - "时延估计"
  - "模型无关控制"
  - "自适应控制"
  - "分数阶非奇异终端滑模"
  - "抖振抑制"
  - "时变不确定性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2607.26383</p>

# Time-delay Control Using a New Nonlinear Adaptive Law for Cable-Driven Robots

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Wenbo Gao, Yaoyao Wang, Jiawang Chen, Wenliang Zhang, Hanzhuo Wang</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26383v1) · [PDF 下载](https://arxiv.org/pdf/2607.26383v1) · **关键词** 缆索驱动机器人, 轨迹跟踪控制, 时延估计, 模型无关控制, 自适应控制, 分数阶非奇异终端滑模, 抖振抑制, 时变不确定性  


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

本文针对绳驱动机器人在时变不确定性、运动换向和测量噪声下难以兼顾跟踪精度与抖振抑制的问题，提出一种将时延估计、分数阶非奇异终端滑模和非线性自适应律结合的控制策略。

**不用术语来说**：绳驱动机器人依靠柔性绳索传力，虽然轻便且安全，但绳索只能受拉、不能受压；机器人换向时，绳索会经历张紧—松弛—再张紧，摩擦、迟滞和弹性也会使系统特性不断变化。因此，控制器既要在突发误差和强扰动下迅速增强控制作用，又要在平稳跟踪时避免因噪声反复调节而造成高频振动，这两项目标很难同时满足。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出一种基于时延估计的自适应控制框架：用历史输入和可测状态近似未知动力学，并结合分数阶非奇异终端滑模误差动态与快速终端滑模趋近律，以降低对精确绳驱动系统模型的依赖并加快误差衰减。
- 设计含自适应指数项的非线性更新增益，使控制参数能够在性能恶化或轨迹换向时较快增大，而在平稳跟踪阶段保持更稳定，从而面向不同工况协调鲁棒性、参数调节速度与噪声诱发的抖振抑制。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于缆索驱动机器人（cable-driven robot）的高精度轨迹控制研究。此类机器人将电机布置在固定基座上，通过柔性缆索传递驱动力，因而具有低运动惯量、较高负载自重比和良好柔顺性，适用于康复机器人、空中操作和人机协作。然而，缆索只能承受拉力，运动反向时可能经历“张紧—松弛—再张紧”的状态切换，并受到摩擦迟滞、缆索弹性和张力工作点影响，形成时变、分段的非线性动力学；较低结构刚度还会把外部扰动转化为关节弹性偏转和高频振荡。因此，控制器需要在缺少精确动力学模型的条件下，同时处理未知动力学、外部扰动、测量噪声及运动状态切换。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**时延估计（Time-Delay Estimation, TDE）**

TDE利用上一采样时刻的控制输入和系统状态，近似当前未知动力学与外部扰动的合并影响，从而减少对精确机器人模型和参数辨识的依赖。其估计精度受采样频率与硬件性能限制，因此通常会留下需要鲁棒控制补偿的估计误差。

</div>
<div class="conceptitem" markdown="1">

**滑模控制与抖振**

滑模控制通过切换型控制作用把系统状态推向预先设计的误差流形，并使其沿该流形收敛，因而对模型不确定性和扰动较鲁棒。实际数字控制中的高速、不连续切换可能造成控制输入和机械系统的高频振荡，即“抖振”。

</div>
<div class="conceptitem" markdown="1">

**分数阶非奇异终端滑模（FONTSM）**

终端滑模利用非线性误差流形实现有限时间或快速收敛，“非奇异”设计用于避免某些终端滑模公式在误差接近零时出现控制量发散；分数阶设计则以非整数阶动态提供额外的误差整形自由度。本文将这种误差动态与快速终端滑模到达律结合，以兼顾快速误差衰减和鲁棒性。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是存在缆索弹性、单向受拉约束、摩擦迟滞和低结构刚度的缆索驱动机械臂，控制任务是在时变集总不确定性、外部扰动、测量噪声及有限采样条件下实现关节轨迹跟踪。控制器可使用可测系统状态、期望轨迹、历史状态及历史控制输入，但不假设已获得缆索系统的精确动力学模型；其输出为驱动机械臂的控制信号。期望结果是跟踪误差快速衰减并最终保持一致有界，同时避免滑模切换增益在平稳跟踪时因噪声而引起明显抖振，并在轨迹反向、缆索张弛切换或扰动增强时维持足够的控制增益。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Wang等人的缆索驱动机械臂自适应控制方法[21]**: 该方法通过在线调节提高跟踪精度和响应速度，是本文最直接的同类控制研究；但原文指出其更新增益仍为线性形式，难以在不同工况下同时兼顾控制性能与抖振抑制。
- **文献[6]、[13]、[27]中的自适应滑模律**: 这些方法面向刚性机械臂或气动软执行器，主要在线调节滑模控制中的不连续切换项。本文将其作为适应速度和增益稳定性的对照背景，并指出切换项系数若调节不当，可能放大振荡与抖振。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

绳驱动机械臂具有低惯量和高负载自重比，但其绳索弹性、单向受力约束及摩擦迟滞会产生低刚度和分段切换非线性。尤其在运动换向时，张紧状态变化使系统动力学显著时变；在稳定跟踪时，外部扰动又容易转化为弹性关节偏转和高频振荡。实际控制因而必须在模型不准确、外扰、硬件采样限制和测量噪声并存的条件下维持高精度与稳定性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **精确模型或数据驱动控制**：模型控制利用动力学、逆运动学、视觉反馈或张力调节计算控制输入；模糊控制、神经网络和强化学习则通过在线调参或学习映射来补偿参数变化及外部载荷。
- **时延估计结合滑模与自适应控制**：时延估计利用短时间内未知动力学变化有限的假设，以延迟的控制输入和系统状态近似当前的总未知项；滑模控制补偿剩余估计误差，自适应律再依据跟踪状态在线调整滑模切换项的增益。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 精确模型方法受绳索迟滞、摩擦和结构复杂性影响，建模与参数辨识困难；智能或数据驱动方法还可能具有较高实时计算负担，并高度依赖参数调节和在线适应，调节不当会引起超调、张力波动及振荡。
- 时延估计在有限采样率和硬件能力下必然存在残差，而既有自适应滑模律多采用线性更新增益并直接调节高频不连续的切换项，难以同时做到误差恶化时快速增益、平稳阶段抑制噪声驱动的增益波动；系数适应不当还可能放大抖振。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种面向绳驱动机器人多工况的模型弱依赖自适应机制：它不仅要补偿时延估计残差和时变扰动，还应根据运行状态非线性地改变调节强度，在轨迹换向或性能下降时保留足够控制增益，在平稳跟踪时避免切换系数受噪声驱动而频繁振荡，并尽量减少参数整定负担。

</div>
<div markdown="1"><span>核心问题</span>

能否在基于时延估计的无精确模型控制框架中，构造一种具有指数型非线性更新增益的自适应律，并与快速收敛的终端滑模动态结合，使绳驱动机器人在时变不确定性和外扰下获得快速、最终一致有界的跟踪，同时改善控制信号抖振和工程整定难度？

</div>
<div markdown="1"><span>作者直觉</span>

时延估计先用系统刚刚发生过的行为抵消大部分未知动力学，相当于让鲁棒控制器只处理剩余误差；终端滑模结构负责把跟踪误差快速压缩。关键的指数型自适应因子则像一个随工况改变灵敏度的调节器：当误差趋势表明控制能力不足时，它放大更新速度并提供较大增益；当运动平稳、误差主要来自噪声时，它使增益演化更稳定，避免把微小测量波动转化为高频控制切换。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法面向具有强非线性、低刚度、时变不确定性和外部扰动的索驱动机械臂轨迹跟踪。输入为期望关节轨迹及其一、二阶导数、当前关节状态，以及上一采样时刻的控制力矩和关节加速度；输出为当前电机力矩。整体结构由时间延迟估计（TDE）、分数阶非奇异终端滑模（FONTSM）、快速终端滑模到达律和非线性自适应增益组成：TDE用上一采样周期的数据近似未知动力学，FONTSM把位置与速度误差压缩为滑模变量，鲁棒项抵消估计残差，而新自适应律在线调节等效惯量和切换增益。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造跟踪误差与滑模变量

先计算 \(\mathbf e=\mathbf q_d-\mathbf q\)，再将误差速度、误差的分数阶微分项和分数阶积分项组合成FONTSM滑模变量 \(\mathbf s\)。分数阶幂次均取在0与1之间，以形成非线性、非奇异的有限时间误差动态。

<div class="method-step__io" markdown="1">

**输入**：期望关节轨迹 \(\mathbf q_d,\dot{\mathbf q}_d,\ddot{\mathbf q}_d\) 和实测关节状态 \(\mathbf q,\dot{\mathbf q}\)。  
**输出**：每个关节的跟踪误差 \(e_i\) 和滑模变量 \(s_i\)。

</div>

**直观理解**：控制器不分别处理许多误差量，而是把位置误差、变化趋势和历史信息浓缩为一个“偏离程度” \(s_i\)；令它接近零，就能进一步约束跟踪误差。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 用时间延迟数据估计未知动力学

将完整机械臂动力学重写为“常值对角惯量乘关节加速度＋集总未知项”，并以 \(\hat{\mathbf V}=\boldsymbol\tau_m(t-l_s)-\hat{\mathbf M}\ddot{\mathbf q}(t-l_s)\) 近似当前集总未知动力学。其有效性依赖未知项在一个采样周期内变化不大，以及等效惯量满足适当的失配约束。

<div class="method-step__io" markdown="1">

**输入**：上一采样时刻的电机力矩 \(\boldsymbol\tau_m(t-l_s)\)、关节加速度 \(\ddot{\mathbf q}(t-l_s)\) 以及在线等效惯量矩阵 \(\hat{\mathbf M}\)。  
**输出**：未建模动力学、耦合、重力、电机侧效应及外扰的合并估计 \(\hat{\mathbf V}\)。

</div>

**直观理解**：该步骤假设系统在极短的一个采样周期内不会突变，因此用“刚刚发生的未知作用”代替“现在的未知作用”，避免建立精确而复杂的索驱动机器人模型。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成名义滑模控制与鲁棒补偿

名义项 \(\mathbf u_1\) 结合期望加速度、FONTSM误差动态和快速终端滑模到达律 \(-\boldsymbol\beta_1\mathbf s-\boldsymbol\beta_2\operatorname{sig}(\mathbf s)^{\boldsymbol\eta}\)；附加项 \(\mathbf u_2=\hat{\mathbf k}\operatorname{sgn}(\mathbf s)\) 用于压制TDE误差与剩余扰动。

<div class="method-step__io" markdown="1">

**输入**：期望加速度 \(\ddot{\mathbf q}_d\)、误差相关项 \(\boldsymbol\xi(\mathbf e,\hat{\boldsymbol\theta})\)、滑模变量 \(\mathbf s\) 及在线参数 \(\hat{\mathbf M},\hat{\mathbf k}\)。  
**输出**：注入动力学命令 \(\mathbf u=\mathbf u_1+\mathbf u_2\)。

</div>

**直观理解**：名义项负责把运动拉回期望轨迹，符号切换项则像安全余量一样处理估计不准的部分；快速到达律在误差较大和接近目标时采用不同强度的非线性纠偏。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 非线性自适应并输出电机力矩

依据 \(|s_i|\) 是否越过边界层，分段增加或减小 \(\hat\theta_i\)，再由自适应指数 \(\hat\sigma_i=\bar\sigma(1-k_{6,i}\hat\theta_i)\) 构造非线性量 \(\hat\theta_i^{\hat\sigma_i}\)，同步更新 \(\hat M_i\) 与 \(\hat k_i\)。最终计算 \(\boldsymbol\tau_m=\hat{\mathbf M}\mathbf u+\hat{\mathbf V}\) 并发送给电机。

<div class="method-step__io" markdown="1">

**输入**：各关节滑模变量 \(s_i\)、边界层 \(\Omega_i\)、更新状态 \(\hat\theta_i\) 及预设参数。  
**输出**：当前采样时刻的电机力矩命令 \(\boldsymbol\tau_m\)，以及供下一周期使用的更新参数和历史数据。

</div>

**直观理解**：平稳跟踪时，较小的 \(\hat\theta_i\) 配合大于1的指数会被进一步压小，从而减轻噪声引发的抖振；轨迹反向时指数可降至1或以下，使控制增益不被削弱，必要时甚至得到增强。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="equation-block" markdown="1">

#### AFONTSM滑模流形与TDE控制律

$$
\begin{aligned}
\mathbf{s}&=\dot{\mathbf e}+\mathbf k_1D^{\chi_1}\!\left(\operatorname{sig}(\mathbf e)^{\varphi_1}\right)+\mathbf k_2D^{\chi_2-1}\!\left(\operatorname{sig}(\mathbf e)^{\varphi_2}\right),\\
\boldsymbol\tau_m&=\hat{\mathbf M}\mathbf u+\hat{\mathbf V},\qquad \hat{\mathbf V}=\boldsymbol\tau_m(t-l_s)-\hat{\mathbf M}\ddot{\mathbf q}(t-l_s),\\
\mathbf u&=\mathbf u_1+\mathbf u_2,\\
\mathbf u_1&=\ddot{\mathbf q}_d+\boldsymbol\xi(\mathbf e,\hat{\boldsymbol\theta})+\boldsymbol\beta_1\mathbf s+\boldsymbol\beta_2\operatorname{sig}(\mathbf s)^{\boldsymbol\eta},\\
\mathbf u_2&=\hat{\mathbf k}\operatorname{sgn}(\mathbf s),\\
\xi_i&=\frac{k_{1,i}D^{\chi_{1,i}}\!\left(\operatorname{sig}(e_i)^{\varphi_{1,i}}\right)+k_{2,i}D^{\chi_{2,i}-1}\!\left(\operatorname{sig}(e_i)^{\varphi_{2,i}}\right)}{1+k_{3,i}\hat\theta_i^{\hat\sigma_i}}.
\end{aligned}
$$

**符号说明**

- $\mathbf e=\mathbf q_d-\mathbf q$：期望关节角与实际关节角之差。
- $\mathbf s$：FONTSM滑模变量，用于综合表征位置、速度及分数阶误差动态。
- $D^{\chi}$：阶次为 \(\chi\) 的分数阶微积分算子；正阶对应分数阶微分，负阶对应分数阶积分。
- $\operatorname{sig}(a)^b$：逐元素带符号幂函数，即 \(|a|^b\operatorname{sign}(a)\)。
- $\boldsymbol\tau_m$：电机产生的控制力矩向量。
- $\hat{\mathbf M}$：在线调整的对角等效惯量矩阵。
- $\hat{\mathbf V}$：由上一采样时刻数据得到的集总未知动力学估计。
- $l_s$：数字控制器的采样间隔。
- $\mathbf u_1,\mathbf u_2$：分别为名义误差整形与到达控制项、抵抗估计误差和扰动的鲁棒切换项。
- $\boldsymbol\beta_1,\boldsymbol\beta_2,\boldsymbol\eta$：快速终端滑模到达律参数，其中各 \(\eta_i\) 满足 \(0<\eta_i<1\)。
- $\boldsymbol\xi$：由分数阶误差项和自适应非线性增益共同构成的误差补偿项。

<div class="equation-explanation" markdown="1">

**直观理解**：第一行规定什么状态算“已经回到正确轨迹”；后续各行则把期望加速度、滑模纠偏、鲁棒切换补偿和上一周期估计的未知动力学合成为实际电机力矩。该结构的核心是：已知的轨迹信息直接控制，未知的机器人动力学交给TDE近似，剩余估计误差由切换项覆盖。  
**原文位置**：第II-B节，式(11)、式(13)–(16)及式(15)后的 \(\xi_i\) 定义；TDE估计对应第II-A节式(5)。

</div>

</div>

<div class="equation-block" markdown="1">

#### 自适应指数与分段更新律

$$
\begin{aligned}
\hat M_i&=\bar M_i\left(1+k_{3,i}\hat\theta_i^{\hat\sigma_i}\right),\qquad
\hat k_i=\bar k_i\left(1+k_{4,i}\hat\theta_i^{\hat\sigma_i}\right),\\
\hat\sigma_i&=\bar\sigma\left(1-k_{6,i}\hat\theta_i\right),\\
\dot{\hat\theta}_i&=\begin{cases}
|s_i|\operatorname{sgn}(\hat\theta_{i,\mathrm{mid}}-\hat\theta_i),&\hat\theta_i\geq\hat\theta_{i,\max}\ \text{or}\ \hat\theta_i\leq0,\\
\left(\dfrac{|s_i|}{k_{5,i}\Omega_i}\right)^{\phi_i},&0<\hat\theta_i<\hat\theta_{i,\max},\ |s_i|\geq\Omega_i,\\
-(|s_i|+\Delta_i)^{-1},&0<\hat\theta_i<\hat\theta_{i,\max},\ |s_i|<\Omega_i.
\end{cases}
\end{aligned}
$$

**符号说明**

- $\hat\theta_i$：第 \(i\) 个关节的基础自适应更新状态。
- $\hat\sigma_i$：随 \(\hat\theta_i\) 变化的自适应指数。
- $\hat\theta_i^{\hat\sigma_i}$：实际用于放大或压缩控制参数的非线性更新增益。
- $\bar M_i,\bar k_i$：等效惯量和鲁棒切换增益的正基准值。
- $k_{3,i},k_{4,i},k_{5,i},k_{6,i},\bar\sigma,\phi_i$：预先设定的正控制系数，用于决定增益幅度、指数变化和更新速度。
- $\Omega_i$：第 \(i\) 个滑模变量的预设边界层阈值。
- $\Delta_i$：下降分支中的正偏置，用于避免 \(s_i\) 穿越切换面附近时出现除零奇异性。
- $\hat\theta_{i,\max},\hat\theta_{i,\mathrm{mid}}$：更新状态的预设上界及越界后用于回拉的中间值。

<div class="equation-explanation" markdown="1">

**直观理解**：当 \(|s_i|\) 超出边界层时，更新状态按幂律增长，使等效惯量和鲁棒增益提高；进入边界层后，更新状态下降，避免长期维持过大切换力。新增的可变指数进一步区分工作阶段：小 \(\hat\theta_i\) 时可令指数大于1以显著压低噪声增益，而较大 \(\hat\theta_i\) 时可令指数降至1或以下，从而保留或增强轨迹反向时的控制能力。  
**原文位置**：第II-B节，式(17)–(19)。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文提出的是解析设计的在线反馈控制器，不涉及数据集训练、经验风险最小化或神经网络参数优化；设计目标是使滑模变量进入有界区域，并据此保证关节跟踪误差最终一致有界。参数 \(\hat\theta_i\) 在运行中按照分段微分方程更新，这属于在线自适应控制而非离线训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 时间延迟估计（TDE）模型无关框架**

系统被表示为 \(\boldsymbol\tau_m=\bar{\mathbf M}\ddot{\mathbf q}+\mathbf V\)，其中 \(\mathbf V\) 汇总真实惯量与选定对角惯量的差异、科氏项、重力、电机惯性与阻尼、外部扰动等。控制器用前一采样时刻的数据估计 \(\mathbf V\)，不需要逐项辨识这些动力学。

> 直观理解：它把所有难以建模的作用装进一个“未知总项”，再用最近一次观测估计该总项，因此显著降低模型依赖；代价是采样必须足够快，且未知作用不能在相邻采样间剧烈跳变。

**2. FONTSM流形与快速终端到达律**

滑模流形将 \(\dot{\mathbf e}\)、误差非线性函数的分数阶微分和分数阶积分组合起来；到达律同时包含线性项 \(-\boldsymbol\beta_1\mathbf s\) 与亚线性幂项 \(-\boldsymbol\beta_2\operatorname{sig}(\mathbf s)^{\boldsymbol\eta}\)，其中 \(0<\eta_i<1\)。作者据此构造有限时间趋近机制，并在定理1中给出滑模变量及跟踪误差最终一致有界的结论。

> 直观理解：分数阶算子使控制器同时利用当前误差和一定的历史信息；线性项提供整体稳定纠偏，非线性幂项强化接近滑模面时的收敛。论文证明的是误差最终进入一个小区域，而不是在所有扰动下严格等于零。

**3. 带自适应指数的非线性增益律**

基础更新状态 \(\hat\theta_i\) 由 \(|s_i|\) 驱动：位于边界层外时按幂律增长，边界层内时按负倒数规律下降，越过预设上下范围时被拉回中间值。区别于直接使用线性 \(\hat\theta_i\) 的基线方法，本文以 \(\hat\theta_i^{\hat\sigma_i}\) 调节 \(\hat M_i\) 和 \(\hat k_i\)，且指数本身随 \(\hat\theta_i\) 变化。

> 直观理解：固定指数会同时压低平稳阶段和轨迹反向阶段的增益，而可变指数试图把两种状态分开处理：平稳时主动降噪，反向或误差较大时保留快速响应能力。

**训练与推理**

无训练阶段。在线运行时，每个采样周期依次读取期望轨迹和关节状态，计算 \(\mathbf e\) 与 \(\mathbf s\)，根据 \(|s_i|\) 和边界层 \(\Omega_i\) 积分更新 \(\hat\theta_i\)，再计算 \(\hat\sigma_i\)、\(\hat M_i\) 和 \(\hat k_i\)。随后利用上一周期的力矩与加速度形成TDE项 \(\hat{\mathbf V}\)，组合 \(\mathbf u_1\) 和 \(\mathbf u_2\)，输出当前力矩 \(\boldsymbol\tau_m\)，并保存当前量供下一周期使用。作者的理论结论是在给定假设和适当参数下实现最终一致有界，而非无条件的精确渐近收敛。

**复现信息**

公平复现需要保持数字采样间隔 \(l_s\) 足够小，并选择等效惯量使 \(\|\mathbf I-\mathbf M^{-1}\bar{\mathbf M}\|<1\)，否则TDE误差的有界性前提可能不成立。参考轨迹需有界且二次连续可微，其一、二阶导数也需有界；机械臂被假定运行在关节位置、速度和加速度均有界的紧集内。还需实现分数阶算子、上一周期力矩与加速度缓存、\(\hat\theta_i\) 的上下界处理以及边界层判定；具体离散分数阶算法、采样频率和全部参数数值在所给方法节选中原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- 本文不使用公开数据集，而是在双关节绳驱机械臂上进行48 s实时轨迹跟踪实验。RMSE在24–48 s周期稳态区间计算，用于排除初始瞬态的主要影响；ITAE和ISCT在0–48 s完整区间计算，用于评价全过程收敛与控制代价。参考轨迹的具体函数、重复次数及训练/验证/测试划分在所给原文中未明确报告。
- 自适应律比较使用实验II同一次运行得到的两个关节滑模面s_i和跟踪误差e_i作为所有候选自适应律的共同输入。这不是独立闭环控制数据集，而是固定输入条件下的增益演化对比，作用是尽量隔离自适应律结构本身的差异。
- 鲁棒性实验在机械臂上附加50 g负载，以检验载荷变化下的稳健性和可重复性；但所给原文截取部分未包含该实验的定量结果、重复次数或统计波动。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**RMSE（均方根跟踪误差）**

衡量跟踪误差的典型幅值，对较大误差赋予更高权重。本文在24–48 s稳态区间计算，因此主要反映周期稳定运行时的跟踪精度。 （越低越好；较低值表示关节位置整体更接近参考轨迹，但不能单独说明最坏瞬时误差或控制能耗。）

</div>
<div class="metricitem" markdown="1">

**ITAE（时间加权绝对误差积分）**

定义为\(\mathrm{ITAE}_i=\int_0^{T_i}t|e_i|\,dt\)，其中e_i为关节i的跟踪误差，t为时间，T_i为评价区间长度。时间权重使实验后段仍未消失的误差受到更大惩罚，因而反映全过程收敛质量和持续误差。 （越低越好；较低值表示误差更快消退或长期残差更小，但该指标不能区分误差方向。）

</div>
<div class="metricitem" markdown="1">

**ISCT（控制转矩平方积分）**

定义为\(\mathrm{ISCT}_i=\int_0^{T_i}\tau_{m,i}^2\,dt\)，其中\(\tau_{m,i}\)为关节i的电机控制转矩。它用平方积分近似刻画完整实验期间的总体控制用力。 （越低通常越好；表示在完成跟踪时所需控制作用更小，但它不是直接测得的电能、机械效率或执行器寿命。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 实验II，关节1：所提ATDC与文献[21]基线在相同平台、轨迹、采样周期和评价协议下比较。

<div class="result-value" markdown="1">

关节1的RMSE由0.5486降至0.3592，下降34.52%；ITAE由415.25降至274.92，下降33.79%；ISCT由76.26降至71.16，下降6.69%。三个指标方向一致，说明稳态误差、全过程持续误差和控制转矩代价均有改善。

</div>

通俗地说，关节1不仅跟得更准，而且没有通过明显增加控制用力来换取精度，反而使转矩平方积分略有降低。不过这只是单一实验平台和给定轨迹上的结果；没有重复试验方差或统计检验，不能据此证明对所有轨迹、负载和硬件都能获得相同比例的提升。

<div class="result-source" markdown="1">

来源：Section III-B, Experiment II；Table I

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">For Joint 1, the proposed method reduces the RMSE from 0.5486 to 0.3592, corresponding to a 34.52% reduction, while the ITAE is reduced from 415.25 to 274.92, i.e., by 33.79%. Meanwhile, the ISCT decreases from 76.26 to 71.16, corresponding to a 6.69% reduction.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 实验II，关节2：所提ATDC与文献[21]基线进行同条件闭环比较。

<div class="result-value" markdown="1">

关节2的RMSE由0.4261降至0.2935，下降31.11%；ITAE由341.34降至228.80，下降32.97%；ISCT由40.70降至33.47，下降17.77%。这表明改善并非只出现在一个关节。

</div>

关节2也同时获得更小的稳态误差、较少的长期误差累积和更低的控制代价，增强了双关节结果的一致性。但两个关节属于同一台机器人和同一次实验协议，并不等价于跨机器人或跨任务的独立验证。

<div class="result-source" markdown="1">

来源：Section III-B, Experiment II；Table I

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">For Joint 2, the proposed method reduces the RMSE from 0.4261 to 0.2935, corresponding to a 31.11% reduction, while the ITAE decreases from 341.34 to 228.80, i.e., by 32.97%. The ISCT is also reduced from 40.70 to 33.47, corresponding to a 17.77% reduction.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 实验II，所提ATDC内部的时间延迟估计误差相对于实际控制转矩的归一化评估。

<div class="result-value" markdown="1">

TDE误差与控制转矩的RMS比值在关节1和关节2上分别为0.0291和0.0306；最大值比值分别为0.1065和0.1004。按逐点误差/转矩比超过10%的标准，超限率分别为7.55%和8.18%，最长连续超限时间为59 ms和60 ms，平均约9–10 ms。

</div>

这些数值说明估计失配在整体能量意义上约为控制转矩RMS的3%，较大的相对误差主要是短暂瞬态，支持“TDE失配有界且通常较小”的实验判断。但归一化比值小不等于动力学模型完全准确，也不能单独证明闭环稳定性；稳定性仍依赖论文的理论条件和完整控制器。

<div class="result-source" markdown="1">

来源：Section III-B, Experiment II；Eq. (28) and Fig. 4(g–j)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">In the experiments, the RMS ratios are rRMS,1=0.0291 and rRMS,2=0.0306, indicating that the TDE mismatch is small in an energy sense compared with the control effort. The peak ratios are rMAX,1=0.1065 and rMAX,2=0.1004, which mainly occur during transient phases.</span>

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

- 文献[21]的基线控制方法：与所提方法共享相同平台、轨迹、采样周期及公共参数调节原则，是表I中闭环跟踪性能的直接基线，也用于判断新增非线性自适应指数项是否带来实际收益。
- 文献[6]的自适应律：在实验III中接收与所提方法相同的s_i和e_i，仅调整该自适应律特有参数，用于比较不同增益更新结构的动态响应。
- 文献[13]的自适应律：作为近期自适应增益方案之一，在固定输入条件下比较更新增益的响应速度、稳定性及噪声敏感性。
- 文献[27]的自适应律：同样使用实验II记录的共同输入，旨在避免不同闭环轨迹或工况混淆自适应律本身的效果。所给截取未提供文献[6]、[13]、[27]的完整数值比较表。

**实验想回答的问题**

- 在相同机械平台、参考轨迹、采样周期和调参原则下，所提出的ATDC控制器相较文献[21]的基线方法，能否同时提高双关节轨迹跟踪精度、减小持续误差并降低控制能量？
- 新引入的自适应指数项能否根据运行阶段调节更新增益：在轨迹换向时保持较强且快速的自适应响应，而在平滑跟踪时抑制测量噪声引起的增益振荡与控制抖振？

**实验实现**

实验平台为双关节绳驱机械臂，采用MOONS ECU19058H24-S001电机、AQMD2403BLS-M驱动器、100∶1谐波减速器和分辨率0.009°的编码器。控制器通过MATLAB/Simulink Real-Time与NI PCI-6229板卡执行，确定性闭环采样频率为1 kHz；实时目标机为Intel G2120、2 GB RAM的工业PC。实验分为自适应机理分析、与文献[21]的闭环基线比较、固定s_i与e_i输入下的多种自适应律比较，以及附加50 g负载的鲁棒性测试。公平性控制包括相同平台、参考轨迹、采样间隔和评价标准；实验II对公共控制参数采用相同设置原则，实验III仅调整各文献方法特有参数。原文给出大量控制器增益，但未在截取内容中报告实验重复次数、置信区间、随机化顺序或显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 实验I子情形一：固定其他自适应参数，令边界层\(\Omega=10^{-2}\times[7,8,9,10]\)，比较非线性更新增益\(\hat{\theta}_i^{\hat{\sigma}_i}\)的峰值、激活时长和噪声敏感性。 | 较小Ω产生更大的更新增益和更长的激活持续时间，但平滑跟踪阶段对噪声更敏感；增大Ω会降低增益峰值、缩短激活时间并减弱噪声影响，同时使控制响应变慢。 | 该消融隔离了边界层宽度的作用。边界层可理解为系统把滑模变量视为“足够接近零”的容许范围：范围越窄，控制器越积极地纠正微小偏差，也越容易把测量噪声当成真实误差；范围越宽则更平滑，但牺牲部分响应速度。该实验给出趋势而非RMSE等闭环指标的逐档数值，因此不能确定全局最优Ω。 | Section III-B, Experiment I, Subcase One；Fig. 3(a–c)<br><span class="experiment-evidence">As shown in Fig. 3(a-c), the smaller boundary layer parameter Ω results in the larger nonlinear adaptive update gain and the longer activation duration. However, it also leads to increased noise sensitivity during the smooth tracking phase.</span> |
| 实验I子情形二：固定\(\Omega=10^{-2}\times[5,5]\)，分别设置\(\bar{\sigma}=[1,2,3,4]\)，考察自适应指数项系数对响应速度、激活时长和增益振荡的影响。 | 较小\(\bar{\sigma}\)带来更快响应和更长激活时间；但\(\bar{\sigma}=1\)时不能抑制平滑阶段噪声，反而放大自适应增益振荡。取2、3、4时，\(\bar{\sigma}\)越大，平滑阶段非线性更新增益的振荡越弱。 | 该消融直接检验论文核心新增指数机制的关键系数。结果表明它调节的是“换向时保留增益”和“平滑时压制噪声”之间的折中，而不是单调提升所有性能；过小的指数系数会破坏预期的降噪作用。由于原文未给出各档设置对应的跟踪误差和控制能耗数值，这里只能确认增益曲线机制，不能量化其最终闭环收益。 | Section III-B, Experiment I, Subcase Two；Fig. 3(d–f)<br><span class="experiment-evidence">Under condition σ̄=[2,3,4], as σ̄ increases, the oscillation of the adaptive nonlinear update gain θ̂iσ̂i during the smooth tracking phase gradually diminishes, indicating an enhanced ability to suppress noise.</span> |

**定性案例**

- 图4与图5的轨迹换向片段构成一个定性案例：换向会使滑模变量和跟踪误差短时增大，所提指数自适应律随之提高更新增益；当增益达到预设上界时曲线短暂保持不变，以避免产生过大的控制信号。进入平滑跟踪阶段后，指数项降低更新增益并减弱噪声诱发的振荡。该案例直观展示了“困难阶段积极、平稳阶段克制”的设计意图，但图形观察本身不能替代跨重复实验的统计证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper proposes and experimentally validates an adaptive control law for cable-driven robots.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`85198c9fde085f278af0195450e120cdd51972836cfdcc11d757b860414c3316`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
