---
title: "[论文解读] ARCSnake V2: Mechanical Adaptations For An Amphibious Multi-Domain Screw-Propelled Snake-Like Robot"
description: "[arXiv 2511.11970][机器人 / 具身智能] 本文针对原版 ARCSnake 无法水下作业的关键缺口，研究如何通过防水传动、关节密封与可调浮力控制，将螺旋推进蛇形机器人扩展为能在狭窄、非结构化陆水环境中运动和执行操作任务的两栖平台。"
arxiv_id: "2511.11970"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.032097+00:00"
source_sha256: "18b965c8e458180ed7d2b2a8101fe14dede26dec37c4df8a94511205b1b541fe"
tags:
  - "机器人 / 具身智能"
  - "两栖机器人"
  - "蛇形机器人"
  - "超冗余机构"
  - "阿基米德螺旋推进"
  - "水下机器人"
  - "防水机械设计"
  - "浮力控制"
  - "多域移动"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2511.11970</p>

# ARCSnake V2: Mechanical Adaptations For An Amphibious Multi-Domain Screw-Propelled Snake-Like Robot

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Wickenhiser, Sara, Peiros, Lizzie, Joyce, Calvin, Gavrilov, Peter, Mukherjee, Sujaan, Sylvester, Syler, Zhou, Junrong, Cheung, Mandy, Lim, Jason, Richter, Florian, Yip, Michael C.</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2511.11970) · [PDF 下载](https://arxiv.org/pdf/2511.11970) · **关键词** 两栖机器人, 蛇形机器人, 超冗余机构, 阿基米德螺旋推进, 水下机器人, 防水机械设计, 浮力控制, 多域移动<br>


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

本文针对原版 ARCSnake 无法水下作业的关键缺口，研究如何通过防水传动、关节密封与可调浮力控制，将螺旋推进蛇形机器人扩展为能在狭窄、非结构化陆水环境中运动和执行操作任务的两栖平台。

**不用术语来说**：洞穴、水域、松软地面和地外冰层等环境既可能崎岖湿滑，又可能包含狭窄通道或水下区域，普通轮式、足式乃至仅能在陆地工作的蛇形机器人很难用同一套机体连续通过。实际任务需要一种细长、灵活且不依赖稳定地面附着力的机器人，同时还要解决进水损坏、下潜上浮以及水下姿态不稳等工程问题。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出 ARCSnake V2 的水密机械架构，在保留重复分段、万向节和阿基米德螺旋模块这一核心构型的同时，实现串联螺旋驱动链与缆索驱动关节的防水封装；作者称各分段经过严格测试，并达到所提出系统相当于 IP67 的防护水平。
- 作者集成可选择、可调节的浮力系统，用于深度控制和水下机动，使平台能够执行下潜、上浮与水下稳定运动，并与螺旋推进及超冗余关节运动配合。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于多域移动机器人与仿生蛇形机器人研究，目标是在洞穴、海洋、松软地表及狭窄空间等牵引条件变化显著的环境中实现连续运动。传统轮式机器人虽在平地上能效较高，但在松软或崎岖地形中容易因牵引不足而受限；足式机器人能够跨越离散障碍，却在未知、狭窄且需要专用运动方式的环境中面临部署困难。ARCSnake 路线将超冗余蛇形骨架与阿基米德螺旋推进结合：前者通过多个关节模块提供贴合地形和穿越狭窄空间的能力，后者依靠旋转螺旋面与水体、颗粒或柔顺介质持续作用来产生推力。本文关注的关键扩展，是将这种原本面向多种地面的平台改造成可持续水下运行的两栖系统，同时保留模块化关节运动和螺旋推进能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**超冗余蛇形机器人**

由大量短节段和受控关节串联形成的细长机器人，其自由度通常多于完成基本位姿任务所必需的数量。额外自由度使机器人能够改变全身形状、贴合不规则环境并通过狭窄通道，但也提高了机械传动、密封和协调控制的难度。

</div>
<div class="concept-item" markdown="1">

**阿基米德螺旋推进**

通过旋转带有连续螺旋叶片的圆柱部件，使叶片与水、雪、泥沙或颗粒介质相互作用并产生轴向推力。与依赖身体弯曲和方向性摩擦的传统蛇形运动不同，它可使推力生成在一定程度上独立于机器人骨架的形变。

</div>
<div class="concept-item" markdown="1">

**浮力控制**

通过调节机器人所受浮力或其浮力分布，控制下潜、上浮和水下姿态稳定性。对于由多个串联节段组成的机器人，浮力系统还需避免妨碍关节转动，并与整机密封和质量分布协同设计。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是由重复节段、万向关节、螺旋推进模块及串联传动机构组成的 ARCSnake V2。给定陆地、颗粒介质和水下等跨域环境，系统需要以各节段的螺旋旋转和关节姿态控制作为执行输入，输出可控的推进、转向、下潜与上浮运动；机械系统同时必须阻止水进入分布式驱动与传动结构，并在水压作用下维持传动完整性。论文设定的核心工程任务不是提出一种抽象运动规划算法，而是在保留 ARCSnake V1 模块化构型与螺旋推进原理的前提下，完成串联螺旋传动、线缆驱动关节的防水改造以及可选择、可调节的浮力系统，使平台从可跨越多类地面的机器人扩展为能够持续水下作业的真正多域机器人。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **ARCSnake V1**: 本文平台的直接前身，已经将阿基米德螺旋推进与超冗余蛇形骨架结合，并展示多地形运动能力；其主要局限是缺少持续水下运行能力。ARCSnake V2 保留重复节段、万向关节和螺旋模块的核心构型，重点增加串联驱动链与关节机构的防水设计及浮力控制。
- **EELS**: 由 ARCSnake 技术路线发展而来的外星探索机器人，用于说明螺旋推进在冰面及低温地形中的可行性。它支持螺旋蛇形机构面向极端环境的研究价值，但本文所要填补的缺口仍是集成式、防水且能够持续水下运行的蛇形机器人平台。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

极端环境探索、搜救、环境监测和空间探测要求机器人跨越不平整或松软地面、水域及狭窄空间，并在可能对人员危险或人员无法进入的区域完成检查、取样和物体回收。这里的核心需求并非单一地形上的最高速度，而是同一平台在牵引条件不断变化、空间受限且可能进水的环境中保持可通行性和任务能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **传统轮式与足式移动机器人**：轮式机器人依靠车轮与地面接触产生牵引，通常在平坦硬地上能效较高；足式机器人通过离散落足和关节运动跨越障碍，理论上能适应比车轮更复杂的地形。二者仍依赖可预测、足以承载和提供摩擦的接触区域，而且常受机体尺度限制，难以进入紧凑通道。
- **螺旋推进的超冗余蛇形机器人 ARCSnake V1**：该方案把多个可弯曲关节串成细长蛇形骨架，并在重复分段上配置旋转的阿基米德螺旋。蛇形骨架提供大量关节自由度和狭窄空间通过能力，螺旋旋转则可在两栖介质或颗粒介质中产生推进力，从而降低对普通车轮式牵引方式的依赖。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 轮式机器人在不平整或松软地形上容易因牵引不足和越障能力有限而失效；足式机器人在不可预测、连人类都需要专门工具才能通过的地形中也面临导航与机动困难。其后果是这些传统形态难以可靠覆盖极端环境中的连续多地形路线，尤其难以兼顾狭窄空间。
- ARCSnake V1 虽已展示螺旋推进与蛇形超冗余结构的机动潜力，但作者明确指出其主要限制是缺少水下能力。未解决的进水防护、跨分段传动密封以及水下深度和稳定性控制，使其不能把既有陆地或颗粒介质能力直接扩展到可靠的浸没作业。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究分别证明了阿基米德螺旋适合两栖或颗粒介质推进、蛇形超冗余骨架适合狭窄空间，但原文所述前代平台尚未把这些优势落实为可长期浸没的完整机器人系统。具体缺口是：如何在模块化细长机体中同时实现串联螺旋传动和缆索关节驱动的水密封装，并提供主动、可调的浮力机制，使机器人能够控制水下深度和机动状态。

</div>
<div markdown="1"><span>核心问题</span>

在保留 ARCSnake 重复分段、万向节连接和螺旋推进基本架构的前提下，能否通过机械防水改造与自适应浮力控制，使平台获得经过实验验证的下潜、上浮、水下机动和执行操作任务的能力，同时维持面向多域环境的模块化运动优势？

</div>
<div markdown="1"><span>作者直觉</span>

这一切入点的合理性在于，现有构型已经把两类互补能力放在同一细长机体上：多关节骨架负责弯曲、绕行和适应受限空间，旋转螺旋负责在不同接触介质中持续产生推力。因此无需更换整个运动原理，关键是补齐水环境特有的系统约束。密封让传动与执行器在浸没时仍可工作，可调浮力则改变机器人相对水体的净浮沉趋势，使其不必只依靠关节或螺旋持续对抗重力与浮力；二者结合后，原有机动结构才可能真正转化为可控的水下运动与取物平台。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ARCSnake V2 的方法不是学习算法，而是一套将陆地螺旋推进蛇形机器人改造成两栖平台的机电系统设计。系统输入包括岸上提供的 $48\,\mathrm{V}$ 电力、CANBus 控制指令、压缩空气以及操作者给出的螺旋转速、关节角度和浮力状态命令；各节段依次完成防水供电与通信、螺旋壳旋转、万向关节姿态调节，并通过泡沫壳和可充放气环形气囊改变排水体积。最终输出是跨地形推进能力、受控下潜或上浮、俯仰姿态调节，以及由头部夹爪和相机支持的水下取样能力。

从直观上看，该机器人把三类机构串成一条“可弯曲的水陆螺旋”：旋转外壳负责在地面或介质中产生推进力，主动万向关节负责改变身体形状和推进方向，浮力系统负责决定整机缓慢下沉、近似悬浮或上浮。设计的关键约束是这些机构必须共存于狭长串联节段中，同时保持水密、电力与通信贯通，并提供足以抬起相邻节段的关节力矩。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 节段密封与串联基础设施

每个节段把电子器件置于 IP67 级内腔，电源线和 CANBus 线通过 WetLink 穿舱件进入并继续传递到下一节；螺旋传动轴使用旋转轴封，端部使用 O 形圈，螺旋块与内腔之间使用橡胶垫片和卡箍密封。贯穿全身的正压管路向内腔提供约 $4\,\mathrm{psig}$，使细小泄漏优先表现为空气向外逸出。

<div class="method-step__io" markdown="1">

**输入**：来自岸上的 $48\,\mathrm{V}$ 电源、CANBus 控制链路、正压空气，以及需要串联连接的头部、中间和尾部节段。<br>
**输出**：获得可在水下工作的串联式供电、通信和气路骨架，以及与旋转螺旋外壳相容的密封节段。

</div>

**直观理解**：这一步相当于先造一条带有连续“电线、神经和气管”的密封身体。内部略高于外界的气压不能替代密封，但可降低水从微小缝隙向内渗入的风险。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 螺旋推进与主动关节姿态控制

RMD-L-7015 电机经皮带轮、太阳轮和行星齿轮驱动兼作齿圈的螺旋外壳，传动通过密封轴穿过螺旋块；相邻节段之间的俯仰、偏航轴分别由带减速器的 RMD-X8 Pro 电机和缆索滑轮机构驱动，并利用编码器闭环控制位置。两个半万向关节以 $90^\circ$ 相位差组合，使连接处在俯仰和偏航方向形成半球形活动范围。

<div class="method-step__io" markdown="1">

**输入**：主机发送的螺旋电机转速命令和万向关节目标角度，以及各电机编码器反馈。<br>
**输出**：输出各节段的螺旋旋转和关节角度，从而产生推进力、改变推进矢量并适应地形高差。

</div>

**直观理解**：螺旋壳类似旋转的阿基米德螺杆，负责“推”；万向关节类似可主动弯曲的脊柱，负责“朝哪里推”。编码器让控制器能比较目标角度和实际角度并持续纠偏。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 被动浮力配平与主动浮力调节

先根据阿基米德浮力计算各节段的浮力缺口，再扩大螺旋壳并填充低密度海用泡沫，提供无需耗气的被动浮力；剩余浮力由套在万向关节处的环形气囊承担，气囊尺寸依据圆环体积确定。前、后气囊使用独立气路充气或放气，因此既可整体改变升沉趋势，也可通过两端浮力差调节水下俯仰。

<div class="method-step__io" markdown="1">

**输入**：各节段质量、排水体积和初始净浮力，以及目标为中性浮力上下约 $5\%$ 的工作区间。<br>
**输出**：形成默认轻微负浮力、充气后转为正浮力的可逆状态，并能独立控制机器人前后端的浮力分布。

</div>

**直观理解**：泡沫像永久救生衣，持续抵消大部分重量；气囊像可调救生衣，只补足最后一段浮力。让机器人默认缓慢下沉、充气后上浮，比依赖推进器持续对抗重力更直接，也保留了失去推进时的浮力控制手段。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 系统级控制与任务输出

岸上主机经系缆访问各电机和节段控制板；节段 PCB 将 $48\,\mathrm{V}$ 母线转换并分配为所需电压，Arduino/CAN 控制板读取经 I2C 连接的 IMU。运动时联合设定螺旋转速、关节角度及前后气囊状态，取样时再驱动头部四连杆张口、伸出夹爪并使用前视相机观察抓取区域。

<div class="method-step__io" markdown="1">

**输入**：主机任务命令、各组件的 CANBus 地址、关节编码器和节段 IMU 数据，以及头部取样和成像命令。<br>
**输出**：输出水陆多域移动、下潜、上浮、姿态调整和水下样本抓取行为，并产生编码器、IMU与相机观测。

</div>

**直观理解**：主机把分散在各节段的电机当作带唯一地址的执行单元统一调度。机器人不依靠一个机构完成所有动作，而是把推进、身体弯曲、浮力和末端夹取组合成完整任务。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 阿基米德浮力

$$
F_b=\rho_w g V_{disp}
$$

**符号说明**

- $F_b$：水对节段或气囊产生的浮力。
- $\rho_w$：水的密度。
- $g$：重力加速度。
- $V_{disp}$：结构排开的水体积。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把几何设计直接转换为浮力：排开的水越多，向上的浮力越大。设计者先以它评估裸节段的浮力缺口，再确定泡沫壳和气囊需要增加多少排水体积，以便在约 $-5\%$ 到 $+5\%$ 的中性浮力邻域内切换。<br>
**原文位置**：第 III-B.1 节，公式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 环形气囊体积

$$
V_b=2\pi^2 r^2 R
$$

**符号说明**

- $V_b$：单个充满后环形气囊的总体积。
- $r$：圆环管截面的半径；原文文字称其为 minor diameter，但公式按标准圆环体积应对应截面半径，需结合原图或补充材料核查。
- $R$：从圆环中心到管截面中心的主半径；原文称 major diameter，但公式按标准定义应对应主半径，需做源文核查。
- $\pi$：圆周率。

<div class="equation-explanation" markdown="1">

**直观理解**：设计者用圆环体积估算气囊完全充气后的排水量，再代入浮力公式得到可增加的浮力。论文据此把中间节段从轻微负浮力推到正浮力区间；不过原文对 $r$、$R$ 使用了“直径”措辞，与所列标准公式的半径定义不一致，复现时不能直接混用。<br>
**原文位置**：第 III-B.3 节，公式 (2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。ARCSnake V2 是机电与气动系统设计，不包含数据驱动模型训练、损失函数或参数学习；其设计目标是通过结构配平使机器人在中性浮力上下约 $5\%$ 的区间切换，同时满足密封、关节承载、螺旋推进和规定充气时间等工程约束。这些目标通过部件选型、几何计算、压力计算和闭环电机控制实现，而不是通过优化训练集上的目标函数实现。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 水密螺旋推进节段**

外部螺旋壳由两半 3D 打印结构组成，壳内集成齿圈并由行星齿轮啮合；电机通过皮带传动太阳轮，额外铝轴穿过弹簧加载旋转轴封，将密封内腔中的驱动传递给外壳。电源、CANBus 和正压气路分别通过穿舱件与密封接头跨节段贯通，内腔采用垫片、卡箍和端部 O 形圈达到 IP67 设计目标。

> 直观理解：难点在于外壳必须持续旋转，而内部电子器件必须保持静止和干燥。该模块用密封旋转轴传递机械功，并用独立穿舱接口传递电、通信和空气，使“能转”和“不进水”同时成立。

**2. 缆索驱动主动万向关节**

每个完整关节由两个相差 $90^\circ$ 的半万向关节构成，分别控制俯仰和偏航；每轴由带内部 $5{:}1$ 齿轮箱的 RMD-X8 Pro 电机驱动，并增加外部 $1.8{:}1$ 减速，通过树脂打印滑轮收放 D12 M-RIG MAX 缆索。电机编码器提供高分辨率位置测量，使关节能够闭环跟踪目标角度；论文称其连续力矩足以抬起相邻节段。

> 直观理解：直接把大型电机装在关节转轴上会扩大关节并增加密封困难，缆索机构则把电机转动转换为关节摆动。减速机构以较低速度换取更大力矩，使加重和密封后的 V2 仍能主动弯曲身体。

**3. 泡沫壳与双支路环形气囊浮力系统**

海用泡沫填充的加大螺旋壳提供固定排水体积，环形尼龙塔夫绸气囊提供可变排水体积；气囊织物一面带热塑涂层用于热合，另一面抗刮擦。前后气囊由独立气动支路控制，供气压力根据充气时间、管路摩擦和局部损失确定；设计使用约 $3$ 至 $5\,\mathrm{psi}$ 调节气囊，并将气囊工作压力限制在低于接缝破裂压力的范围内。

> 直观理解：固定泡沫承担大部分配平，可以减少气囊尺寸和耗气量；可充气部分只负责跨过中性浮力点。前后分路相当于分别调节船头和船尾的浮力，不仅能控制升沉，还能让机身抬头或低头。

**训练与推理**

不适用传统“训练/推理”划分。部署前先测定或计算各节段质量、体积和净浮力，配置泡沫壳，使机器人在气囊未充气时保持轻微负浮力；随后依据目标浮力和圆环体积设计气囊，并配置前后独立气路、压力调节器和供气压力。运行时，岸上主机通过 CANBus 向具有唯一地址的螺旋电机、关节电机和节段控制器发送命令；编码器闭环跟踪关节位置，IMU可提供节段相对运动或相对重力方向的信息。下潜时气囊放气并利用轻微负浮力下降，上浮时向气囊充气以增加排水体积，前后差分充放气用于调节俯仰；与此同时，螺旋壳提供推进，万向关节改变身体形状和推进方向。执行采样任务时，操作者利用头部前视相机确认目标，再驱动四连杆机构打开头部并伸出夹爪完成抓取。

**复现信息**

公平复现需要保留四项系统级条件。第一，每个节段由 $48\,\mathrm{V}$ 母线供电，定制 PCB 经 VICOR V48B24C250BL 转换器提供 $24\,\mathrm{V}$，万向关节电机直接使用 $48\,\mathrm{V}$，螺旋电机、微控制器、舵机和通信部件使用分配后的 $24\,\mathrm{V}$。第二，螺旋执行器标称连续力矩为 $1.0\,\mathrm{N\,m}$、峰值为 $3.8\,\mathrm{N\,m}$；半万向关节标称连续力矩为 $2.6\,\mathrm{N\,m}$、峰值为 $13\,\mathrm{N\,m}$，这些规格决定加大泡沫壳后仍可接受的直径和质量。

第三，内腔正压管路约为 $4\,\mathrm{psig}$，论文所列调节器设置为密封正压线 $6\,\mathrm{psi}$、气囊线 $3$ 至 $5\,\mathrm{psi}$；气囊热合接缝约在 $7\,\mathrm{psi}$ 存在破裂风险，文中另给出 $2.15\,\mathrm{psi}$ 的安全工作压力和 $2.9\,\mathrm{psig}$ 的最小上游压力。上述压力的表压、绝压及施加位置必须在复现实验前按原始气路图核对，因为摘录中的单位表述并不完全统一。第四，气囊管路采用 $6\,\mathrm{mm}$ 外径、$2\,\mathrm{mm}$ 内径管材，并以最长 $60\,\mathrm{s}$ 的充气时间为设计约束；前后支路必须独立，否则无法复现差分浮力带来的俯仰控制。原文公式 (4) 至 (5) 的压力损失、流速、截面积和空气黏度单位在摘录中存在疑似排版或量纲错误，因此具体气动参数仍需对照论文 PDF、图 2(D) 和原始设计文件复核。

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

**峰值切向力**

测量螺旋驱动在给定指令角速度下能够施加的最大切向作用力，单位为牛顿；它反映驱动机构克服外部阻力或产生推进作用的能力。 （在不超过电机、传动机构和结构安全限制的前提下通常越高越好，因为更大的切向力意味着更强的负载与推进潜力。）

</div>
<div class="metric-item" markdown="1">

**螺旋外壳合成扭矩与传动效率**

合成扭矩由测得的切向力换算得到；传动效率则比较螺旋外壳的实测扭矩与依据电机最大空载扭矩和传动比计算的理想扭矩，衡量传动链中的损失。 （扭矩需结合任务负载判断；传动效率越高越好，因为这表示齿轮、密封和机械摩擦造成的能量损失更小。）

</div>
<div class="metric-item" markdown="1">

**气囊充气时间误差**

比较前、后气囊的实测充气时间与理论期望时间，用百分比表示浮力系统模型和实际响应之间的偏差。 （越低越好，因为较小误差意味着理论计算更能预测实际浮力调节速度。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 闭环速度控制下，将螺旋驱动指令角速度从 $10\,\mathrm{rad/s}$ 提高到 $50\,\mathrm{rad/s}$。

<div class="result-value" markdown="1">

峰值切向力由 $40.0\,\mathrm{N}$ 增至 $75.9\,\mathrm{N}$，对应的合成扭矩范围为 $3.60$ 至 $6.83\,\mathrm{N\,m}$。

</div>

作者报告的结果表明，在所测速度范围内，更高的速度指令伴随更大的最大电机扭矩和螺旋切向力，说明闭环驱动能够在不同指令速度下提供可观的机械输出。分析上，这验证了驱动链的基本承载能力，但没有给出水下推进速度、牵引力随滑移变化的曲线或长期热稳定性，因此不能单凭该结果判断整机在真实复杂地形中的移动效率。

<div class="result-source" markdown="1">

来源：第 IV-A 节（Screw Drive Validation）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The peak tangential force measured ranged from 40.0 N to 75.9 N at commanded speeds of 10 rad/s and 50 rad/s, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 在 $50\,\mathrm{rad/s}$ 指令速度下，将实测螺旋外壳扭矩与依据 $1.5\,\mathrm{N\,m}$ 最大空载电机扭矩和 $7{:}1$ 传动比得到的 $10.5\,\mathrm{N\,m}$ 理想扭矩比较。

<div class="result-value" markdown="1">

作者计算得到螺旋驱动传动链效率约为 $65.7\%$。

</div>

该数值表示实测输出仅达到理想扭矩基准的一部分，剩余差异可能来自齿轮、轴承、密封和其他机械损失。它直接检验了密封串联驱动结构的机械传递效果，但由于理想基准采用电机最大空载扭矩，且节选未报告测量不确定度或其他负载点，$65.7\%$ 不应被视为覆盖全部工况的系统效率。

<div class="result-source" markdown="1">

来源：第 IV-A 节（Screw Drive Validation）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Thus, the efficiency of the screw drive train is calculated to be about 65.7% at a commanded speed of 50 rad/s.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 气囊完全放气后，同时打开连接至 $2.9\,\mathrm{psi}$ 气源的两个阀门，以检验第 III-B5 节预测的充气时间。

<div class="result-value" markdown="1">

后部气囊在 $68\,\mathrm{s}$ 完成充气，前部气囊在 $70\,\mathrm{s}$ 完成充气；作者报告其相对期望充气时间的误差为 $13.3\%$。

</div>

结果说明气动浮力系统可以在约一分钟量级内完成充气，且理论预测与实测响应大体接近。前后气囊存在 $2\,\mathrm{s}$ 的响应差异，提示气路或气囊特性并非完全一致；同时，该实验只验证充气时间，没有单独证明浮力变化量、深度控制精度或反复充放气的可靠性。

<div class="result-source" markdown="1">

来源：第 IV-B2 节（Buoyancy Control Tests）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In 68s, the rear bladders inflated and the front in 70s.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验没有报告与其他两栖蛇形机器人、螺旋推进平台或替代驱动结构的直接对照；现有“基准”主要是理论扭矩和理论充气时间，因此只能验证内部设计是否达到预期，不能证明其相对现有方法更优。
- 所给实验节选未明确报告重复试验次数、样本量、置信区间、长期防水与耐久测试、能耗、真实复杂地形移动性能，以及水下转向和深度闭环控制精度；此外，下沉与上浮结果文本被截断，相关定量结论仍需核对原论文图表。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 螺旋驱动的理想扭矩基准：以电机约 $1.5\,\mathrm{N\,m}$ 的最大空载输出乘以 $7{:}1$ 传动比，得到螺旋外壳处 $10.5\,\mathrm{N\,m}$ 的理想输出；该基准用于估算传动效率，而不是与另一种机器人进行性能比较。
- 浮力系统的理论充气时间：依据第 III-B5 节的计算值，将实测充气时间与期望时间比较，以检验气路和气囊模型的预测准确性。

**实验想回答的问题**

- 螺旋推进驱动机构在闭环速度控制下能否输出足够的切向力与扭矩，以及从电机到螺旋外壳的传动效率达到什么水平？
- 集成浮力系统能否按预期完成气囊充气，并支持机器人在水中的下沉与上浮过程？

**实验实现**

螺旋驱动实验在闭环速度控制下设置从 $10\,\mathrm{rad/s}$ 到 $50\,\mathrm{rad/s}$ 的指令速度，测量峰值切向力，并将其换算为螺旋外壳处的合成扭矩；随后以电机约 $1.5\,\mathrm{N\,m}$ 的最大空载扭矩和 $7{:}1$ 传动比计算 $10.5\,\mathrm{N\,m}$ 的理想扭矩，用于估算效率。体积测量采用排水法：将中间节段完全浸没于已知水量的矩形容器，通过浸没前后的水位变化计算节段体积。浮力控制实验从气囊完全放气开始，同时打开连接至 $2.9\,\mathrm{psi}$ 气源的两个阀门，分别记录前、后气囊充气时间。下沉与上浮实验先让气囊保持放气并从水面释放机器人，从侧窗录像；机器人到达底部后，再向全部气囊供气并记录上浮过程，最后进行视频后处理。原文节选未说明重复次数、误差统计方法、测试水池尺寸或完整环境条件。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 作者通过侧窗视频记录了机器人在气囊放气时从水面下沉、到达底部后向全部气囊供气并上浮的完整流程，用于直观验证浮力状态切换。该案例能说明系统具有下沉与上浮的定性能力，但所给节选在定量结果句中被截断，因此无法可靠报告加速度、上浮速度或统计误差。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work contributes the mechanical design and locomotion capabilities of an amphibious snake-like exploration robot.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`18b965c8e458180ed7d2b2a8101fe14dede26dec37c4df8a94511205b1b541fe`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
