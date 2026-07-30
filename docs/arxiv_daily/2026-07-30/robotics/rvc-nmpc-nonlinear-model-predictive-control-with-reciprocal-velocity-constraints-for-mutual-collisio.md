---
title: "[论文解读] RVC-NMPC: Nonlinear Model Predictive Control with Reciprocal Velocity Constraints for Mutual Collision Avoidance in Agile UAV Flight"
description: "[arXiv 2512.08574][机器人 / 具身智能] 本文研究如何仅利用其他无人机当前可观测的位置与速度，在低通信负担下把互惠速度约束直接纳入非线性模型预测控制，从而实现适用于高速敏捷飞行的分布式相互避碰。"
arxiv_id: "2512.08574"
announcement_date: "2026-07-30"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T07:32:04.532865+00:00"
source_sha256: "f55ec0edac218536b246977a449d9c6c82396fc1a869db75edd74cf93944a8e0"
tags:
  - "机器人 / 具身智能"
  - "多无人机系统"
  - "相互碰撞避免"
  - "非线性模型预测控制"
  - "互惠速度约束"
  - "分布式控制"
  - "敏捷无人机飞行"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2512.08574</p>

# RVC-NMPC: Nonlinear Model Predictive Control with Reciprocal Velocity Constraints for Mutual Collision Avoidance in Agile UAV Flight

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Vit Kratky, Robert Penicka, Parakh M. Gupta, Ondrej Prochazka, Martin Saska</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2512.08574v2) · [PDF 下载](https://arxiv.org/pdf/2512.08574v2) · **关键词** 多无人机系统, 相互碰撞避免, 非线性模型预测控制, 互惠速度约束, 分布式控制, 敏捷无人机飞行  
**项目页**: [https://youtu.be/LYnn-eDvkec](https://youtu.be/LYnn-eDvkec)  

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

本文研究如何仅利用其他无人机当前可观测的位置与速度，在低通信负担下把互惠速度约束直接纳入非线性模型预测控制，从而实现适用于高速敏捷飞行的分布式相互避碰。

**不用术语来说**：当多架无人机在同一空域高速飞行时，每架无人机既要及时绕开其他无人机，又不能假设控制执行完全准确，也不能持续获知所有同伴未来准备怎样飞；否则，通信延迟、动力学限制或外界扰动都可能使原先安全的轨迹失效。论文要解决的是：让每架无人机依靠容易观测或低带宽传输的当前状态，自主、快速地作出兼顾飞行动力学的避碰控制。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出时间相关的互惠速度约束，并只依据其他机器人当前的位置和速度计算约束，避免依赖交换完整未来轨迹；“互惠”表示相遇双方共同承担调整速度以避免碰撞的责任。
- 将互惠速度约束直接集成到无人机控制层的非线性模型预测控制中，同时考虑非线性飞行动力学，使避碰决策能够随状态变化和外部扰动快速更新，而不是先规划轨迹、再由独立控制器被动跟踪。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于多无人机分布式运动规划与控制领域，研究多个无人机在共享空域中高速飞行时如何相互避碰。由于未来应用中的无人机可能具有较低飞行高度、密集起降点和频繁交会，集中式规划会受到通信延迟与规模扩展能力的限制；因此，本文关注每架无人机独立决策的分布式方案，并要求避碰机制能够直接考虑无人机的非线性动力学和机动限制，以适应敏捷飞行。论文的基本思路是在非线性模型预测控制器中加入随时间变化的互惠速度约束，使无人机仅根据其他机器人的当前可观测位置和速度调整自身运动，而无须交换完整的未来规划轨迹。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**非线性模型预测控制（NMPC）**

NMPC在每个控制周期内利用无人机的非线性动力学模型，预测有限时间范围内的状态，并通过求解优化问题选择控制输入。控制器只执行当前时刻的第一步控制，随后依据新观测重复优化，因此能够及时响应扰动和其他无人机的运动变化。

</div>
<div class="conceptitem" markdown="1">

**速度障碍与互惠避碰**

速度障碍描述一组会使两个运动体在未来发生碰撞的相对速度，避碰可通过选择该集合之外的速度实现。“互惠”表示相遇双方共同承担速度修正，而不是要求其中一方独自绕行。

</div>
<div class="conceptitem" markdown="1">

**分布式多机器人避碰**

分布式方法由每个机器人依据本地观测或少量通信独立计算运动，不依赖统一的中央规划器。它通常更易扩展且可减少中央通信延迟，但必须处理各机器人同时决策所产生的相互影响。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务场景是多架无人机在共享、无集中调度的空域中分别飞向目标，同时避免彼此碰撞，并保持高速、敏捷且符合真实动力学约束的飞行。每架无人机的控制器以自身状态、任务参考以及其他无人机当前的位置和速度为输入；这些外部状态可由机载感知获得，也可通过低带宽网络传输。控制器将时间相关的互惠速度约束直接纳入NMPC，在每个控制周期输出符合动力学与避碰要求的控制指令。其关键假设是能够获得其他无人机当前的位置和速度，而不要求获知或通信其未来轨迹；论文同时明确指出该方法不提供理论安全保证，因此安全性主要通过仿真和真实实验验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Velocity Obstacles / Reciprocal Velocity Obstacles（Fiorini et al. [18]；van den Berg et al. [19]）**: 这些工作奠定了基于相对速度预测碰撞以及由多个机器人互相承担避碰责任的基础。本文沿用互惠速度避碰思想，但将时间相关约束直接集成到考虑无人机非线性动力学的NMPC控制层，以面向高速敏捷飞行。
- **DCAD: Decentralized Collision Avoidance With Dynamics Constraints for Agile Quadrotor Swarms（Arul et al. [27]）**: 该工作同样研究具有动力学约束的敏捷四旋翼分布式避碰，是本文问题设置中直接相关的先前方案。本文强调仅依赖其他机器人的当前可观测位置和速度，并通过控制层NMPC统一处理避碰约束与非线性动力学。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

面向包裹配送、区域监测等应用，大量无人机将共享低空开放空间，飞行密度通常高于传统航空场景。此时，统一调度所有无人机既难以扩展，也会引入通信和计算延迟；若为了安全而显著降低速度，又会削弱无人机的效率与机动性。因此，实际系统需要一种可分布式运行、通信需求低，并能在高速敏捷飞行中持续响应其他飞行器行为变化的相互避碰方法。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **集中式规划与调度**：由中央节点收集多架无人机的状态和任务，联合计算彼此无冲突的轨迹或时序安排，再把结果下发给各无人机。其优势是能够统一协调，但系统规模增大时，集中计算、信息汇聚和下发延迟会成为瓶颈。
- **分布式轨迹共享或速度障碍类避碰**：轨迹共享方法让每架无人机依据自身状态及其他无人机发布的计划轨迹进行局部优化；速度障碍及其互惠变体则根据相对位置和速度构造可能导致未来碰撞的速度区域，并要求机器人选择区域之外的速度，通常由双方共同承担避让。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 许多方法建立在理想参考跟踪之上，或忽略无人机的运动学、动力学与加速度约束。这样得到的安全轨迹未必能被真实飞行器及时执行，尤其在高速转向、强加速或受到扰动时，规划层的无碰撞结论可能无法转化为控制层的实际安全。
- 不少分布式优化方法要求无人机持续交换未来计划轨迹，对通信带宽、时延和数据一致性提出较高要求；而既有方法即使采用这些限制性假设，也往往难以覆盖超过原文所述约每秒10米的高速场景，因而与商用无人机可达到的敏捷飞行能力之间仍有差距。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未同时满足四项关键需求：只依赖可观测的当前状态、无需高带宽未来轨迹通信、在控制层显式考虑无人机非线性动力学，并以足够高的更新频率处理高速多机交会。缺少其中任一环节，都可能使方法在密集、快速且存在扰动的真实飞行中失去可执行性或及时性。

</div>
<div markdown="1"><span>核心问题</span>

能否根据其他无人机当前的位置与速度，实时构造随预测时刻变化的互惠速度约束，并将其直接嵌入非线性模型预测控制，使多架具有真实动力学限制的无人机在低通信条件下完成高速、分布式且实际无碰撞的导航？

</div>
<div markdown="1"><span>作者直觉</span>

碰撞风险首先体现在相对位置与相对速度上，因此无需精确知道对方完整的未来计划，也可以判断哪些速度选择会让两机逐渐进入危险区域。若双方按照同一互惠规则各自承担部分避让，再由模型预测控制在短时间窗内寻找满足这些约束且符合飞行动力学的控制输入，系统便能把抽象的速度避碰要求转化为无人机实际可执行的推力与姿态动作；持续快速重算则可修正观测误差、扰动及对方临时改变运动方向带来的预测偏差。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

RVC-NMPC 是一种面向多无人机高速飞行的去中心化在线控制方法。每架无人机仅利用可观测到的其他机器人信息，计算随时间变化的互惠速度约束（Reciprocal Velocity Constraints, RVC），再将这些约束直接加入非线性模型预测控制（Nonlinear Model Predictive Control, NMPC）问题；控制器在考虑本机非线性动力学的同时，优化未来一段时间内的运动与控制量，并输出当前时刻的控制指令。作者强调该设计不要求交换其他机器人的完整规划轨迹，从而减少通信依赖，并使整个流程能够以 100 Hz 运行。
直观而言，每架无人机先根据当前观察判断“未来哪些相对速度可能导致相撞”，再把这些危险速度变成控制器不可违反的边界。NMPC 随后在动力学可实现、满足避碰限制和趋向任务目标之间进行滚动权衡；但所给材料未包含方法章节、约束构造公式或 NMPC 目标函数，因此无法进一步可靠还原 RVC 的几何计算、互惠责任分配及求解器配置。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 获取本机状态与邻机可观测信息

控制器汇集当前时刻的多机状态信息，作为碰撞风险判断和预测控制的初始条件。原文摘要明确称方法仅依赖其他机器人的可观测信息，但所给材料未说明具体状态分量、估计器或邻机筛选规则。

<div class="method-step__io" markdown="1">

**输入**：本机当前状态，以及由感知或通信得到的其他无人机当前可观测信息。  
**输出**：用于预测的本机初始状态与邻机状态估计。

</div>

**直观理解**：这一步相当于无人机先确认自己在哪里、怎样运动，并观察附近无人机在哪里、怎样运动，而不是要求对方发送整条未来航线。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算时变互惠速度约束

算法针对潜在的机间冲突生成随预测时间变化的 RVC，以限制可能导致未来碰撞的相对速度；“互惠”表示避让责任由相遇机器人共同承担。所给节选未提供约束的数学形式、机器人几何模型、安全半径或时间视界，不能据此补写。

<div class="method-step__io" markdown="1">

**输入**：本机与邻机的当前可观测状态，以及预测时域中的时间信息。  
**输出**：可直接加入 NMPC 各预测时刻的碰撞规避约束集合。

</div>

**直观理解**：可以把它理解为给未来每个时刻画出一组“不要采用的危险速度方向”，使两架迎面接近的无人机共同调整，而非把全部避让责任交给其中一方。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造并求解带 RVC 的 NMPC

将时变 RVC 直接整合到控制器层面的 NMPC 优化问题中，在非线性动力学和避碰约束下滚动优化未来状态与控制序列。所给材料未报告代价函数、状态约束、控制约束、预测时域长度及数值求解方法。

<div class="method-step__io" markdown="1">

**输入**：本机状态、非线性无人机动力学、任务目标或参考运动，以及各预测时刻的 RVC。  
**输出**：满足模型与避碰限制的有限时域控制序列。

</div>

**直观理解**：控制器不是先独立规划一条路径再设法跟踪，而是在选择控制动作时就同时检查飞行器能否做到、是否接近目标以及会不会碰撞。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行首个控制量并滚动更新

采用模型预测控制的滚动时域机制，执行优化序列中的当前控制动作，并在获得新状态后重新计算约束和控制。作者称包括 RVC 计算与 NMPC 在内的完整流程可运行于 100 Hz。

<div class="method-step__io" markdown="1">

**输入**：当前一次 NMPC 求得的控制序列及下一控制周期的新观测。  
**输出**：实时施加给无人机的控制指令，以及下一轮优化所需的更新状态。

</div>

**直观理解**：无人机只执行刚算出的第一步，约 0.01 秒后再根据最新情况重新计划，因此能及时修正高速飞行中的预测误差和邻机运动变化。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

这篇论文不以中心数学公式展开，或全文中未提取到可靠的关键公式。

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该方法是基于在线约束优化的控制算法，而非需要离线训练的学习模型；其实际 NMPC 优化目标、代价项和权重在所给材料中未明确报告，因此不能构造或推断目标函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 时变互惠速度约束生成器**

该模块根据其他无人机的可观测信息，高效计算预测时域内随时间变化的 RVC，并将潜在碰撞转化为速度层面的约束。原文摘要只说明其计算效率较高，所给材料未包含具体几何推导、线性化方式或责任分配公式。

> 直观理解：它把复杂的“两架无人机未来会不会撞上”转化成优化器可检查的速度边界，是在不交换完整规划轨迹时仍能协同避让的关键。

**2. 非线性模型预测控制器**

NMPC 在有限预测时域内显式使用受控无人机的非线性动力学，并把 RVC 作为控制优化的一部分直接处理。与只做运动学级速度修正的方法相比，这种设计原则上能避免生成无人机动力学上无法及时实现的避让动作。

> 直观理解：高速飞行器不能瞬间改变速度；该模块会考虑推力、姿态和加速度响应所造成的实际运动限制，而不是把无人机当作可以任意转向的点。

**3. 低通信依赖的分布式闭环**

每架机器人依据可观测邻机信息独立运行 RVC-NMPC，不依赖集中式协调器，也不要求交换其他机器人的完整计划轨迹。相关工作节选指出，作者排除集中式方案的主要理由是其额外通信延迟和较差的可扩展性。

> 直观理解：各无人机像驾驶员一样根据附近交通独立决策，不必等待中央服务器统一排程，也不必持续获知其他无人机准备走的每一步。

**训练与推理**

不存在机器学习意义上的训练阶段。在线运行时，每架无人机反复执行“读取本机与邻机观测—生成时变 RVC—求解包含非线性动力学与 RVC 的 NMPC—执行首个控制动作”的闭环流程；当状态或邻机观测更新后，重新建立并求解优化问题。摘要表明该流程仅依赖其他机器人的可观测信息，并可达到 100 Hz，但原文节选未说明状态估计、预测邻机运动、不可行问题恢复或通信中断处理的具体步骤。

**复现信息**

对方法复现和结果解释最关键的已知实现信息是：RVC 被直接集成到 NMPC 控制问题中，控制器显式建模无人机非线性动力学，完整在线管线运行频率为 100 Hz，并避免依赖其他机器人的完整规划轨迹。所给材料未明确报告预测与控制时域、离散化方法、无人机状态和输入定义、安全距离、RVC 计算算法、优化求解器、求解容差、硬件平台及单次求解时间；缺少这些信息时无法形成可复现的技术实现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- APCX仿真基准：10架无人机从半径10 m圆周上的位置同时飞往对跖点，刻意使航迹在圆心附近集中交叉，以提高潜在冲突数量。性能测试采用最高20 m/s的速度约束、40 m/s²的加速度约束和0.6 m避碰半径；消融实验沿用10机、半径10 m设置，每种配置统计100次飞行。它用于比较通行效率、成功率和安全裕度。
- 长时压力仿真：10架无人机在20 m×20 m×1 m受限区域内连续导航，加速度上限40 m/s²、避碰半径1.0 m。实验持续3小时，产生超过50000个目标，总航程6.28×10^5 m，平均速度5.8 m/s、最高速度25.9 m/s。它不是固定训练/测试集，而是用于检验长期运行中罕见近距离事件及累计碰撞风险的压力测试。
- 真实世界APCX验证：3架实体无人机执行圆周对跖点导航，避碰半径1.5 m，参考加速度上限最高30 m/s²；原文还概述真实飞行速度最高18 m/s。该实验用于验证算法在机载计算、真实动力学、感知与控制误差共同存在时能否运行，而非仅在理想仿真中成立。原文节选中的Table III不完整，因此各加速度档位的完整飞行次数和统计值无法核验。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**整体飞行时间（Flight time）**

从机器人集合中最早收到导航请求的时刻，到最后一架机器人稳定进入目标点ε邻域的时刻；其中“到达”要求此后持续位于目标邻域内。该指标同时反映避碰绕行、等待和收敛速度。 （越低越好，因为表示所有机器人更快完成整体转移，但必须结合成功率和最小间距判断，不能以牺牲安全为代价。）

</div>
<div class="metricitem" markdown="1">

**成功率（Success rate）**

多次试验中成功完成任务的比例；在本文消融表中用于确认飞行时间差异不是由大量失败试验换来的。 （越高越好；100%表示所统计试验全部完成，但不等同于对任意初始状态都具有理论安全或收敛保证。）

</div>
<div class="metricitem" markdown="1">

**最小互机距离（Minimum mutual distance）**

一次试验中任意无人机对达到的最小空间距离；Table II同时给出各次试验该值的均值，以及全部试验中的最小值，用于衡量最危险时刻的安全裕度。 （在任务效率相近时越高越好，因为更大的最小距离意味着对估计误差、时延和外扰留有更多安全余量。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 10机APCX高冲突性能比较，速度上限20 m/s、加速度上限40 m/s²、避碰半径0.6 m；对比MADER、EGO-SWARM-2、HDSM和RBL。

<div class="result-value" markdown="1">

作者报告RVC-NMPC在所有场景中均无碰撞，并相对飞行时间最优的既有方法HDSM将平均完成时间缩短31%；节选未包含Table I的完整数值行，因此各方法的绝对飞行时间无法核验。

</div>

这一结果表明，在大量航迹集中交叉的设定下，把时变互惠速度约束直接放入NMPC可能减少保守等待和绕行，从而兼顾效率与实验中的碰撞避免。但31%是跨方法、部分跨仿真环境的经验比较；HDSM不建模四旋翼完整动力学，其他方法也多假设完美控制，因此结果不能单独证明算法在严格同平台条件下必然领先31%，更不构成形式化安全保证。

<div class="result-source" markdown="1">

来源：Section V-A, Performance test；详细数据指向Table I，但该表未出现在所给节选中

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Our approach shows 31 % reduction compared to the best-performing approach, HDSM, even though HDSM does not consider quadrotor’s dynamics.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 10机受限区域长时压力仿真：20 m×20 m×1 m空间、加速度上限40 m/s²、避碰半径1.0 m，持续3小时。

<div class="result-value" markdown="1">

10架无人机在超过50000次目标导航、总航程6.28×10^5 m中，平均速度为5.8 m/s、最高速度达到25.9 m/s；作者报告最小互机距离违规被全部避免。

</div>

长时间、大航程和大量目标切换扩大了暴露于偶发冲突的机会，因此该测试比少量短航次更能支持工程鲁棒性。Figure 7还把启用方法与不采用避碰时的最小距离分布进行比较。不过，“100%避免违规”只针对这一有限空间、机器人数量和扰动模型下的观测样本，不能推出所有环境中的零碰撞概率。

<div class="result-source" markdown="1">

来源：Section V-C；最小互机距离分布见Figure 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">During the three-hour-long experiment, 10 UA Vs were navigated to more than 50000 goals, travelled a total distance of 6.28×10 5 m with an average velocity 5.8 ms −1, and maximum velocities up to 25.9 ms −1.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 真实世界三机APCX实验，避碰半径1.5 m，参考加速度上限最高30 m/s²。

<div class="result-value" markdown="1">

作者在实体无人机上验证了方法，概述报告真实飞行速度最高18 m/s、加速度最高30 m/s²；所给Table III内容被截断，无法核验各档加速度下的完整飞行时间、航程、最大速度和最小距离统计。

</div>

实体平台结果说明100 Hz控制管线能够面对实际飞行动力学、执行器响应和状态估计误差，而不是仅在数值模型中运行。它支持“可部署性”，但试验只有3架无人机，规模小于10机仿真；节选也未提供完整试验次数与失败置信区间，因此不能据此量化大规模真实部署的可靠性。

<div class="result-source" markdown="1">

来源：Section V-E, Real-world experiments；汇总表为Table III，但所给节选中的表格不完整

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">The practicality of the proposed approach was further verified through its deployment onboard UA V platforms in the APCX scenario involving three UA Vs with an acceleration limit up to 30 ms −2, and r ca =1.5m (see Fig. 1).</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 作者明确承认方法缺少理论保证。全部无碰撞结果来自有限仿真和真实试验，不能替代对任意初始状态、感知误差、通信时延及求解失败情形的形式化安全证明。
- 主基准并非完全同平台评测：RVC-NMPC与RBL使用完整动力学和状态估计不确定性，其他方法多来自各自环境并常假设完美控制；HDSM还不考虑四旋翼动力学。加之所给节选缺少Table I和完整Table III，31%优势及真实实验的逐项统计仍需回查原文。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- MADER：需要多机器人共享未来轨迹的分散式轨迹规划方法，用于比较RVC-NMPC仅依赖其他机器人当前位置和速度时，是否仍能取得更高通行效率。
- EGO-SWARM-2：面向无人机群的分散式轨迹优化方法，代表基于轨迹规划与优化的现有方案。
- HDSM：论文所述对比中飞行时间表现最好的既有方法，但不考虑四旋翼完整动力学，因此它既是最强时间基线，也暴露了跨仿真环境比较的公平性问题。
- RBL：基于规则的Lloyd多机器人规划与控制方法；与RVC-NMPC一样在包含无人机完整动力学和状态估计不确定性的仿真器中部署，因此相较其他外部报告结果具有更接近的评测条件。

**实验想回答的问题**

- 在多架无人机同时高速交汇的高冲突场景中，RVC-NMPC能否在保持无碰撞的同时，比现有分散式规划与控制方法更快地完成整体转移？
- 该方法的安全性与实时实用性是否能经受长时间、高速度、有状态估计不确定性的动力学仿真以及真实无人机实验检验；其中，时变RVC和PMM参考轨迹分别起到什么作用？

**实验实现**

除另有说明外，仿真运行于8核AMD Ryzen 7 5800X、3.80 GHz计算机，目标到达阈值ε=0.1 m，预测相关参数τ=8 s，默认避碰半径2 m，采用异步通信，并在碰撞评估时把机器人视为半径0.25 m的球体。性能比较中，RVC-NMPC与RBL使用包含完整无人机动力学和状态估计不确定性的仿真器；MADER、EGO-SWARM-2和HDSM主要采用各自作者环境，其中多数假设完美控制。作者还针对按轴施加运动学约束的MADER和HDSM纳入按轴原始上限设置，但这可使合速度或合加速度依方向最多超出范数约束√3倍。消融结果均为100次飞行的统计。系统整体管线据作者报告可在2 GHz ARM处理器上以100 Hz运行，但节选未给出运行时间分布、最坏求解时延或失败求解比例。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 完整方法与NoTimeDep比较：后者保留其他模块，但取消互惠速度约束的时间有效性；10机APCX、100次飞行。 | 两者成功率均为100.0%。完整方法的平均飞行时间为3.07 s，NoTimeDep为3.46 s，约降低11%；平均最小互机距离同为0.98 m，但全部试验中的最小值由0.71 m提高到0.81 m。完整方法平均航程21.15 m、平均飞行速度7.36 m/s，NoTimeDep分别为21.65 m和7.19 m/s。 | 该比较较干净地隔离了“约束只在预测碰撞仍相关的时段生效”这一设计。取消时间依赖后，已经过期的避碰约束仍可能限制后续预测，导致更长航程和更慢完成；恢复时间依赖既提高效率，也改善观测到的最坏安全裕度。它表明静态持续施加RVC会过度保守，但不证明时变机制在所有通信时延下都更安全。 | Table II, proposed row；对照值见Table II, NoTimeDep row<br><span class="experiment-evidence">proposed 100.0 3.07 2.94 21.15 7.36 0.98 0.81</span> |
| 完整方法与NoPmm比较：NoPmm取消PMM轨迹生成，直接向NMPC提供单一目标参考；10机APCX、100次飞行。 | NoPmm与完整方法的成功率均为100.0%，且平均飞行时间从3.07 s降至2.98 s；但平均最小互机距离从0.98 m降至0.90 m，全部试验中的最小值从0.81 m降至0.62 m。NoPmm平均速度为7.71 m/s，高于完整方法的7.36 m/s。 | 该消融显示PMM不是为了追求表面上的最短时间，而是向NMPC提供符合运动能力的参考轨迹。直接给终点会使控制器更激进，因而略快，却明显压缩安全裕度；作者还指出这种参考不可行，会损害NMPC收敛并增加真实部署风险。由于100次仿真中两者成功率都为100%，这里能直接确认的是安全裕度和参考可行性的权衡，而不是NoPmm已经发生更多碰撞。 | Table II, NoPmm row；完整方法对照见Table II, proposed row<br><span class="experiment-evidence">NoPmm 100.0 2.98 2.75 21.11 7.71 0.90 0.62</span> |

**定性案例**

- Figure 7比较同一类连续高速导航在启用RVC-NMPC与完全不使用互避机制时的最小互机距离直方图及累积分布。其作用是展示方法如何把近距离事件的分布推向更安全区域，而不只是报告一次最小值；但节选没有提供图中各距离阈值对应的精确频率，因此只能作定性解释，不能从图文重建新的百分比结论。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出面向敏捷多无人机互相避碰的非线性模型预测控制方法，核心贡献属于机器人运动控制与导航。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`f55ec0edac218536b246977a449d9c6c82396fc1a869db75edd74cf93944a8e0`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
