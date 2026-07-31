---
title: "[论文解读] Direct Rotor Thrust Sensing and Feedback Control for Disturbance Rejection of Multirotors Using Load-cells"
description: "[arXiv 2607.10099][机器人 / 具身智能] 本文研究能否在多旋翼旋翼处用称重传感器直接测量瞬时推力，并通过高速内环调节推力，从而在阵风、垂直入流和地面效应等复杂气动扰动影响飞行轨迹之前或之初抑制其作用。"
arxiv_id: "2607.10099"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.162040+00:00"
source_sha256: "29328b57e5e0779720ecae5b6ad28b3063424514b397efefe231df028782eea5"
tags:
  - "机器人 / 具身智能"
  - "多旋翼"
  - "直接推力测量"
  - "负载传感器"
  - "推力反馈控制"
  - "气动扰动抑制"
  - "垂直入流"
  - "地面效应"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2607.10099</p>

# Direct Rotor Thrust Sensing and Feedback Control for Disturbance Rejection of Multirotors Using Load-cells

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Böhm, Peter, Brünig, Michael, Moghadam, Peyman Z., Pounds, Pauline E. I.</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.10099) · [PDF 下载](https://arxiv.org/pdf/2607.10099) · **关键词** 多旋翼, 直接推力测量, 负载传感器, 推力反馈控制, 气动扰动抑制, 垂直入流, 地面效应<br>


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

本文研究能否在多旋翼旋翼处用称重传感器直接测量瞬时推力，并通过高速内环调节推力，从而在阵风、垂直入流和地面效应等复杂气动扰动影响飞行轨迹之前或之初抑制其作用。

**不用术语来说**：多旋翼控制器通常根据电机转速推算推力，但同一转速在阵风、上下气流或靠近地面时未必产生同样的力；传统系统往往要等飞行器已经偏离姿态或轨迹后，才能从运动变化中发现并纠正扰动。论文希望像给旋翼安装“力觉”一样，直接感知它实际产生了多少推力，并立即调整电机，使实际推力持续贴近期望值。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出一种直接推力反馈架构：在旋翼受力位置使用称重传感器测量瞬时推力，并以高速内环调节旋翼，使实际推力跟踪上层控制器给出的期望推力，而非默认转速与推力之间始终保持固定关系。
- 针对“称重传感器噪声过大、难以用于旋翼闭环控制”的既有质疑，使用低成本通用器件构建单旋翼枢轴台、双旋翼跷跷板平台及可飞行四旋翼原型，验证直接推力感知与反馈控制在复杂气动现象下的可实施性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于多旋翼飞行器的气动扰动抑制与底层推力控制研究。常规控制器通常依据悬停、静止空气等条件下的简化动力学模型，将旋翼推力和力矩近似为转速的二次函数，并假定实际推力能够准确跟随控制器指令；但阵风、垂直入流、涡环状态、地面效应、桨叶挥舞和平移升力等现象会改变相同转速下的真实推力。若控制器仅从机体的位置、姿态或速度偏差反推扰动，就必须等到飞行轨迹已经受到影响后才能补偿。本文所处的研究方向因此是：在旋翼产生力的位置直接测量瞬时推力，并以高频内环使实际推力跟踪期望推力，从而将复杂气动效应尽可能隔离在机体运动控制环之外。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多旋翼级联控制**

多旋翼通常由外层位置或姿态控制器计算所需合力与力矩，再由内层执行控制将其分配为各旋翼指令。本文在常规飞行控制器与电机之间增加推力反馈内环，直接校正“指令推力”与“实际推力”的差异。

</div>
<div class="concept-item" markdown="1">

**气动扰动与垂直入流**

气流经过旋翼盘会改变叶片所见的相对来流，因此即使电机转速不变，旋翼产生的推力也可能变化；阵风、地面反流和涡环状态都可能造成这种现象。垂直入流尤其指沿旋翼轴向进入旋翼盘的气流，是本文实验关注的主要扰动来源之一。

</div>
<div class="concept-item" markdown="1">

**负载传感器与闭环推力调节**

负载传感器（load cell）通过结构微小形变测量受力，可安装在旋翼与机架之间以获得旋翼施加的力。闭环调节将该测量与期望推力比较并快速修正电机输入，使系统不必仅凭转速或功率间接推断推力。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是受阵风、动态垂直入流和地面效应等未知或难建模气动现象影响的多旋翼系统。上层控制器给出各旋翼的期望推力，安装在旋翼受力路径上的负载传感器提供瞬时实际推力，高速内环据此调整电机驱动，使测得推力跟踪期望值；其输出是更接近指令的旋翼实际推力，并最终降低姿态或三维位置对扰动的响应。该问题建立在旋翼推力通常按转速平方建模、传统控制往往默认指令推力等于实际推力的背景上，但本文不要求预先精确辨识每一种气动效应。研究首先在单旋翼和双旋翼跷跷板装置上检验测量与控制可行性，再在集成负载传感器的四旋翼上进行初步自由飞行验证；由于负载传感器可能受到振动、机械耦合和噪声影响，能否获得足以支持高速反馈的有效信号本身也是问题的一部分。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$T_d$**

上层控制器要求旋翼产生的期望推力；原文所给节选未明确规定符号，本文仅以该符号概括问题设置。

</div>
<div class="notation-item" markdown="1">

**$T_m$**

负载传感器测得的旋翼实际瞬时推力；原文所给节选未明确规定符号。

</div>
<div class="notation-item" markdown="1">

**$\omega$**

旋翼角速度；常规模型通常把推力和力矩近似为其平方的函数。

</div>
<div class="notation-item" markdown="1">

**$e_T=T_d-T_m$**

推力跟踪误差，即期望推力与实测推力之差；原文所给节选未明确给出这一记号。

</div>

</div>

**直接相关的工作**

- **Bangura and Mahony（2017）的电功率驱动推力估计方法［4, 5］**: 该方法利用电功率等旋翼上游信号估计推力，以补偿平移升力以及未建模的轴向和水平气流，并较基础转速控制降低了跟踪误差。本文与其目标相近，但认为间接推断可能限制扰动抑制的保真度，因而改为在旋翼处直接测力；同时，Bangura和Mahony曾判断负载传感器会因噪声而难以用于这一任务，本文将该判断作为需要实验检验的关键问题。
- **薄膜力传感器和四旋翼机架应变计的直接推力测量工作［8, 6］**: 这些工作表明固定翼螺旋桨或四旋翼结构上的直接测力在技术上可行，但测量受到传感器特性、振动和机械相互作用影响，并需要惯性补偿。它们主要验证测量实现，没有利用实测推力构成推力调节闭环；本文进一步把直接测量纳入高速控制，以主动跟踪期望推力。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

阵风、动态垂直入流、涡环状态和地面效应会改变旋翼在给定转速下产生的真实推力，使基于悬停和静止空气条件建立的简化模型失准。其直接后果是姿态与轨迹受到扰动，严重时模型与真实气动行为的偏差还可能导致飞行状态发生非预期发散。因此，控制系统需要更快地识别并抵消旋翼实际受力的变化。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **显式气动建模与基于机体运动的控制**：建立旋翼、桨叶挥舞、平移升力及不同气动区域的模型，再依据飞行器的位置、姿态和速度误差估计扰动力并修正推力指令；常规控制还通常假定旋翼转速与推力近似呈二次关系。
- **自适应或学习方法，以及基于电功率的间接推力估计**：自适应与机器学习方法通过重复飞行数据逐步调整隐式模型参数；另一类方法测量电功率等旋翼上游信号，据此估算推力变化，并补偿平移升力以及未建模的轴向或水平气流扰动。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 显式模型只能覆盖预先纳入的气动机制，难以完整描述非平稳、外生且未预见的真实环境现象；自适应或学习方法又常需针对特定机动进行重复训练和迭代调整。更根本的是，仅依据机体动力学进行建模、学习或自适应控制，通常必须等扰动已经改变飞行器运动后才能识别它，因而补偿存在天然滞后。
- 电功率等信号位于推力生成链条的上游，推力变化仍是间接推断，可能限制扰动估计与抑制的保真度。已有薄膜力传感器或机架应变计工作虽探索了直接测力，但受到传感器噪声、振动、机械耦合及惯性补偿需求影响，且主要验证测量可行性，并未利用测得推力实施闭环推力调节。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前尚缺少一种经过系统实验验证的多旋翼控制方案，能够在旋翼推力生成位置直接测量实际作用力，并将该测量作为高速闭环反馈来调节推力。特别需要回答的是：在旋翼振动和机械耦合显著的条件下，低成本称重传感器的噪声是否仍允许有效控制，以及这种直接反馈能否比传统基于转速指令的控制更好地隔离多类气动扰动。

</div>
<div markdown="1"><span>核心问题</span>

使用称重传感器获得旋翼瞬时推力并建立高速推力内环，是否能在真实的横向扰动、垂直入流和地面效应下稳定运行，并相较于仅输出转速需求的传统控制器更有效地维持多旋翼姿态与期望推力？

</div>
<div markdown="1"><span>作者直觉</span>

扰动最终改变的是旋翼实际施加到机体上的力，而转速、电功率和机体轨迹只是这一变化的间接线索。若传感器直接位于力的传递路径上，控制器便可比较“要求产生的力”和“此刻真正产生的力”，并立即修正电机输出；这样既不必准确辨认扰动属于阵风、入流还是地面效应，也不必先等待整架飞行器出现明显偏移。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文把多旋翼抗气动扰动重新表述为“在推力生成处直接测量并闭环调节”的控制问题。系统采用串级控制架构：外环根据惯性测量单元（IMU）给出的姿态误差计算各旋翼的期望推力，内环则利用安装在电机底部的称重传感器实时测量实际推力，并根据推力误差调整电调的脉宽调制（PWM）指令。外环处理飞行器姿态，内环处理旋翼推力；每个旋翼具有独立的传感器和推力控制环，因此阵风、垂直入流、涡环状态或地面效应一旦改变实际推力，内环可在这些变化明显传递到机体姿态之前进行补偿。

从控制机理看，常规方法通常由期望姿态直接推算电机输入，隐含假设“相同控制输入产生相同推力”；但旋翼推力同时取决于转速和局部入流，扰动会破坏这一对应关系。本文在姿态控制器与电机之间加入推力反馈层，使上层只需提出“需要多少推力”，下层负责在变化的空气动力条件下实现该推力。直观地说，传统控制器要等机体被风吹偏后才知道推力不对，而本文像在每台电机下安装一台高速电子秤，推力刚发生变化就立即增减电机输入。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 姿态感知与外环推力分配

外层PID姿态控制器根据俯仰误差生成旋翼推力需求；在双旋翼装置中，两侧设定值围绕零互补变化，以产生恢复俯仰角所需的差动推力矩。

<div class="method-step__io" markdown="1">

**输入**：目标俯仰角、BNO055 IMU以$100\,\mathrm{Hz}$输出的当前俯仰角，以及由两者形成的姿态误差。<br>
**输出**：分别发送给各旋翼内环的期望推力参考值。

</div>

**直观理解**：外环只判断横梁或飞行器应向哪一侧施力以及施力多少，不直接假定某个PWM一定对应某个实际推力。它相当于给每个旋翼下达力的目标。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 旋翼推力原位测量与滤波

NAU7802SGI 24位ADC以$320\,\mathrm{Hz}$采样每个传感器，随后采用采样频率为$320\,\mathrm{Hz}$、截止频率为$2\,\mathrm{Hz}$的低通Butterworth滤波器抑制称重信号噪声。测量位置位于推力生成路径的电机基座处，使信号直接反映旋翼传给机体的瞬时轴向力。

<div class="method-step__io" markdown="1">

**输入**：安装在每台电机底部的CE08685梁式或DYZ-100柱式称重传感器产生的模拟信号。<br>
**输出**：每个旋翼经过滤波的实际推力估计。

</div>

**直观理解**：称重传感器像装在电机下面的电子秤，但原始读数会快速抖动；低通滤波保留较慢且与控制有关的推力变化，同时削弱高频噪声。代价是滤波可能引入延迟，因此其动态带宽应结合实验结果理解。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 独立内环推力调节

系统计算每个旋翼的推力误差，并在$500\,\mathrm{Hz}$内环中生成电机PWM控制量；尽管新传感器样本仅以$320\,\mathrm{Hz}$到达，控制循环仍以更高频率运行，以向电机提供过采样的输出。各旋翼内环相互独立，使局部入流变化能够被局部补偿。

<div class="method-step__io" markdown="1">

**输入**：外环给出的期望推力与对应称重传感器给出的实际推力。<br>
**输出**：发送至四合一BLHELI-S电子调速器的各电机PWM信号。

</div>

**直观理解**：若阵风使某个旋翼在相同PWM下少产生了推力，内环直接看到偏差并提高电机输入；扰动消退后，内环又降低输入，避免恢复正常效率时推力突然过大。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 机体响应与闭环迭代

旋翼推力共同决定机体平移和俯仰运动，IMU再将新的俯仰角反馈给外环，从而形成“姿态外环—推力内环”的完整串级闭环。用于公平对照时，可绕过推力内环，改用等于闭环增益的线性增益级，使同一外层PID直接驱动电机。

<div class="method-step__io" markdown="1">

**输入**：各旋翼经推力内环调节后产生的实际推力、作用于机体的气动力以及气动扰动力矩$w$。<br>
**输出**：受控的俯仰角和位置运动，以及进入下一控制周期的姿态反馈。

</div>

**直观理解**：内环先尽量保证旋翼确实产生被要求的力，外环再处理剩余的机体姿态误差。旁路版本则代表常见的开环推力生成方式，用于判断性能提升究竟是否来自直接推力反馈。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 俯仰转动动力学

$$
\mathrm{I}\ddot{\theta}=d_{1}T_{1}+d_{2}T_{2}+w
$$

**符号说明**

- $\mathrm{I}$：飞行器或跷跷板系统绕俯仰轴的转动惯量。
- $\theta$：俯仰角，$\ddot{\theta}$为俯仰角加速度。
- $d_i$：第$i$个旋翼轴线到系统重心的有符号距离；符号反映旋翼位于重心哪一侧。
- $T_i$：第$i$个旋翼实际产生的推力。
- $w$：直接作用于系统的气动扰动力矩。

<div class="equation-explanation" markdown="1">

**直观理解**：该式说明俯仰运动由各旋翼“推力乘力臂”的总和以及外部扰动力矩共同决定。本文内环直接控制式中的实际$T_i$，从而降低因入流变化导致“请求推力”和“真实推力”不一致而产生的额外俯仰运动；但直接作用于机体的$w$仍需由姿态外环纠正。<br>
**原文位置**：第II-A节，公式(3)

</div>

</div>

<div class="equation-block" markdown="1">

#### 含入流扰动的瞬时旋翼推力模型

$$
T_i=k_T\omega_i^2-k_c\omega_i\Delta v_i,\qquad \Delta v_i=\dot{z}+d_i\dot{\theta}+v_w
$$

**符号说明**

- $T_i$：第$i$个旋翼的瞬时推力。
- $k_T$：旋翼推力系数，描述理想情况下转速平方对推力的贡献。
- $\omega_i$：第$i$个旋翼的角速度。
- $k_c$：入流阻尼系数，描述入流变化对推力的影响强度。
- $\Delta v_i$：第$i$个旋翼处的入流速度变化。
- $\dot{z}$：系统沿垂向的位置速度。
- $d_i\dot{\theta}$：俯仰转动在第$i$个旋翼位置引起的局部垂向速度分量。
- $v_w$：外部阵风造成的入流扰动速度。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项表示常见的“推力近似正比于转速平方”，第二项表明同一转速下，垂向运动、俯仰运动或阵风改变局部入流后，实际推力仍会变化。因此仅控制RPM不能保证$T_i$恒定；直接测量并闭环控制$T_i$正是本文方法相对于RPM控制的关键。<br>
**原文位置**：第II-A节，公式(4)与公式(6)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文是基于物理传感器与PID反馈的控制系统，不包含数据驱动模型训练、损失函数或参数学习；$K_p$、$K_i$和$K_d$属于控制器调节参数，而非通过训练集优化的模型参数。原文说明对照控制器与所提方案的外层姿态控制器使用相同调节参数，以隔离新增推力内环的作用，但未在所给章节中明确报告参数整定算法或数值。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 原位称重式推力感知模块**

每台电机直接安装在额定量程为$1\,\mathrm{kg}$的低成本称重传感器上，多通道定制控制板通过NAU7802SGI 24位ADC并行读取推力，最高采样率为$320\,\mathrm{Hz}$。该结构测量的是电机—旋翼组件传给机架的力，而不是根据转速、PWM或机体加速度间接反推推力。

> 直观理解：这一模块解决“控制器要求的推力是否真的产生”这一可观测性问题。转速相同并不保证入流变化时推力相同，而直接测力能把这种偏差作为控制误差立即暴露出来。

**2. 串级姿态—推力控制器**

外环PID以$100\,\mathrm{Hz}$运行，使用IMU姿态误差形成推力设定值；每个旋翼的内环以$500\,\mathrm{Hz}$运行，使用期望推力与实测推力之差形成PWM。对照控制器与推力反馈方案的外环采用相同的$K_p$、$K_i$和$K_d$，区别在于后者增加了基于称重测量的内环。

> 直观理解：串级设计把两个时间尺度和两个任务分开：较慢的外环负责“机体是否保持水平”，较快的内环负责“旋翼是否按要求出力”。这样可减少气动扰动先改变姿态、再被姿态控制器被动纠正的等待过程。

**3. 推力信号调理与嵌入式执行模块**

ESP32-S3-WROOM-1负责读取传感器、执行控制并生成PWM；称重信号统一经过截止频率为$2\,\mathrm{Hz}$的低通Butterworth滤波。高频数据记录在板载SD卡中，遥测数据则通过WiFi和MQTT以$100\,\mathrm{Hz}$传至板外处理，后两者主要用于实验记录而非闭环控制的必要通信链路。

> 直观理解：低成本称重传感器的噪声较大，若未经处理直接反馈，电机会追逐测量抖动；滤波模块使控制器主要响应持续的推力变化。板载执行避免把高速闭环依赖于无线通信的延迟和丢包。

**训练与推理**

不存在机器学习意义上的训练与推理。部署时，系统先完成称重传感器标定并持续采样；每个控制周期中，外环读取IMU姿态并计算期望推力，内环读取滤波后的实际推力、计算推力误差，再更新PWM并通过电子调速器驱动电机。该过程在线连续运行，不需要把数据发送到板外才能形成控制闭环。

比较模式包括两种：所提模式启用每个旋翼的独立推力反馈内环；传统模式绕过该内环，用与闭环增益相等的线性增益级将外环输出映射为电机命令。实验中的外层姿态调节器被作者有意设置为较差的调节器，以突出推力调节的影响；因此该比较主要检验“增加直接推力反馈能否在相同外环下改善抗扰性”，不能直接代表其相对于现代飞控中PID角速度内环的最终优势，后者被作者列为未来工作。

**复现信息**

复现控制链路所需的关键硬件为ESP32-S3-WROOM-1、BNO055 IMU、四合一BLHELI-S电子调速器、每旋翼一个额定量程$1\,\mathrm{kg}$的CE08685或DYZ-100称重传感器，以及NAU7802SGI 24位ADC。时间配置为：IMU与姿态外环$100\,\mathrm{Hz}$，称重采样$320\,\mathrm{Hz}$，推力内环$500\,\mathrm{Hz}$；所有实验使用采样频率$320\,\mathrm{Hz}$、截止频率$2\,\mathrm{Hz}$的低通Butterworth滤波器。内环频率高于传感器更新率意味着部分控制周期会复用最近一次推力样本，其作用是提高发送至电机的输出更新率，而不是创造新的测量信息。

方法解释还需注意两项边界。第一，$2\,\mathrm{Hz}$低通滤波虽然抑制噪声，却会限制可观测推力变化的有效带宽，原文所给章节未明确报告滤波器阶数、群时延或完整离散PID实现，因此尚不足以逐行复现控制器。第二，论文使用单旋翼和双旋翼跷跷板装置研究垂直入流、侧风和瞬态地面效应，并称还使用飞行器验证可行性；但本次所给方法章节只详细描述了跷跷板控制链路，不能据此推断完整四旋翼飞行控制中的推力分配矩阵、偏航控制或现代角速度内环配置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 双转子跷跷板式物理实验数据：装置以中心支点固定，两端各安装一个转子，仅一侧暴露于扰动；平衡控制器的俯仰设定值为 $0^\circ$。该数据用于比较两种控制器在可重复、受约束条件下的姿态与推力响应，不是公开数据集，也没有训练集、验证集或测试集划分。
- 垂直入流实验：两个转子各产生约 $60\,\mathrm{g}$ 推力，实验流程与论文第 IV 节的单转子实验相同。图 11 的说明提到结果由连续 $10$ 次运行取平均，但节选对图 12 和图 14 所示双转子曲线是否采用完全相同的平均方式未作更明确说明。该实验测试第二个转子的入流阻尼存在时，控制器能否应对局部垂直气流变化。
- 侧风与地面效应实验：侧风实验将一侧转子暴露于逐渐增强的横向气流；地面效应实验则让平板间歇移入和移出一侧转子下方，整个序列重复 $10$ 次。前者测试风致俯仰力矩和强风下的振荡，后者测试近地升力突变及平板撤出后的瞬态超调。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**最大俯仰偏差**

测量装置俯仰角相对 $0^\circ$ 设定值的最大偏离；该指标直接反映扰动作用下姿态保持能力，但节选没有给出统一的数学统计定义或置信区间。 （越低越好，因为更小的角度偏差表示控制器更能抑制扰动导致的姿态变化。）

</div>
<div class="metric-item" markdown="1">

**俯仰振荡及触及机械偏转极限的情况**

观察响应是否出现持续大幅振荡，以及是否达到装置允许的最小或最大偏转位置；这是稳定性和控制失效严重程度的定性指标。 （振荡越小、越少触及偏转极限越好，因为触及极限意味着姿态误差已超出装置的正常调节范围。）

</div>
<div class="metric-item" markdown="1">

**系统总推力一致性**

比较两个转子推力之和在扰动期间是否保持稳定。跷跷板装置只要求两端力矩平衡，因此即使总推力错误也可能保持水平；该指标用于揭示这种在固定装置上不明显、但在自由飞行中会造成额外升力的问题。 （越接近期望总推力越好，因为无意的总推力增加会在自由飞行中引起不希望出现的爬升或升力变化。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 双转子垂直入流扰动

<div class="result-value" markdown="1">

传统转速控制器在最大扰动开始时以及扰动输入逐步下降时失去控制，最大俯仰偏差达到 $\pm30^\circ$；直接推力反馈将偏差限制在 $\pm10^\circ$ 内。作者还观察到，传统互补控制分配会提高未受扰转子的控制信号，使系统总推力上升，而推力反馈可按各转子的局部流场调整需求。

</div>

这表明直接测量实际推力能够更早地修正入流造成的推力变化，并显著缩小固定双转子装置的姿态偏差。传统控制器即使重新实现两端平衡，也可能在更高的总推力水平上达到平衡；固定支点不会表现为上升，但自由飞行器可能因此获得额外升力。该结果来自特定跷跷板装置，不能单独证明真实飞行中的位置误差也会按相同比例下降。

<div class="result-source" markdown="1">

来源：第 V-A 节，图 12 与图 14

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The classical RPM controller loses control at the onset of the maximum disturbance and again when the disturbance input begins stepping down with a maximum deviation of ± 30 °.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 双转子侧风扰动

<div class="result-value" markdown="1">

当风速达到约 $6\,\mathrm{m\,s^{-1}}$ 后，传统转速控制器出现明显振荡并触及最小和最大偏转极限；直接推力反馈在相同条件下将俯仰保持在 $\pm10^\circ$ 内。

</div>

侧风不仅改变推力，还会通过诱导阻力或桨叶挥舞产生俯仰力矩。传统控制器尝试提高另一侧转子的推力，但强风下发生过冲；直接推力反馈的较小偏差说明其能更稳定地补偿局部气动变化。不过，实验没有提供均方误差、重复次数或统计显著性，因此不能据此量化不同风况下的平均改进幅度。

<div class="result-source" markdown="1">

来源：第 V-B 节，图 13

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In contrast, the thrust controller maintained stable pitch within ± 10 °, effectively mitigating the wind-induced disturbances under the same conditions.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 双转子间歇地面效应扰动

<div class="result-value" markdown="1">

地面平板撤出时，传统转速控制器出现约 $10^\circ$ 的显著超调，而直接推力反馈仅出现约 $2^\circ$ 的小偏转；图 15 的概括则将推力控制器的偏差报告为 $3^\circ$ 以内。

</div>

平板移入会增加近地升力，移出又会使升力快速回落。直接推力反馈可以直接看到这种实际力变化，因此比仅控制转速更快地修正瞬态响应。正文的约 $2^\circ$ 与图注的 $3^\circ$ 以内并不矛盾，前者描述特定撤出瞬态的近似值，后者给出图中整体偏差范围；但原文没有给出逐次试验分布，无法判断 $10$ 次重复之间的一致性。

<div class="result-source" markdown="1">

来源：第 V-C 节，图 15

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In contrast, the thrust force controller maintained stable pitch control, experiencing only a minor deflection of approximately 2 ° when the plate withdrew.

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

- 传统转速控制器（classical RPM controller）：以转子转速或油门控制信号为直接调节对象，不测量实际产生的瞬时推力。它是有意义的基线，因为常规多旋翼控制通常默认所请求的推力能够由电机和转子准确实现，并采用互补式控制分配来修正姿态。
- 负载传感器直接推力反馈控制器（thrust feedback/controller）：利用负载传感器测得的转子实际推力进行高速闭环调节，并按每个转子的局部流场改变推力需求。它是论文提出的实验方案，也是与传统转速控制器进行同条件比较的对象。

**实验想回答的问题**

- 在单侧转子受到垂直入流、侧风或地面效应时，基于负载传感器的直接推力反馈能否比传统转速控制更有效地抑制双转子系统的俯仰偏差？
- 直接推力反馈能否在姿态控制过程中按各转子的局部气流条件调整推力，同时避免传统控制分配引起的系统总推力上升？

**实验实现**

三组双转子实验分别施加垂直入流、侧风和地面效应扰动，并在相同装置与扰动条件下比较传统转速控制和直接推力反馈控制。装置采用 $0^\circ$ 俯仰设定值；垂直入流实验中每个转子约提供 $60\,\mathrm{g}$ 推力。地面效应序列重复 $10$ 次，图 11 所述垂直入流结果由连续 $10$ 次运行平均。控制器加入前馈项以提供不依赖积分作用的油门设定值，并使用模拟与数字两级滤波降低负载传感器噪声，从而允许采用适合快速无人机动力学的较高比例增益；原文同时指出，滤波不足而控制增益较高时会诱发振动。节选未报告采样频率、滤波器参数、风速完整范围、误差统计量或显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 垂直入流实验展示了固定跷跷板装置可能掩盖总推力错误：传统控制器提高未受扰侧的控制信号后，两端仍可在更高的共同推力水平上重新平衡，因此俯仰恢复并不等于飞行状态正确。图 12 表明直接推力控制维持了更一致的总推力；这一案例说明评估多旋翼扰动抑制时，应同时检查姿态误差和合力，而不能只看装置是否重新水平。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出利用负载传感器直接测量旋翼推力并进行高速反馈控制的多旋翼扰动抑制方法。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`29328b57e5e0779720ecae5b6ad28b3063424514b397efefe231df028782eea5`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
