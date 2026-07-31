---
title: "[论文解读] SharedAssembly: A Data Collection Approach via Shared Tele-Assembly"
description: "[arXiv 2503.12287][机器人 / 具身智能] 本文针对亚毫米级紧间隙装配示范难以通过传统遥操作高效采集的问题，提出在主端与从端共同嵌入装配辅助的共享自主双边遥操作框架 SharedAssembly，以降低操作门槛并提高高质量接触数据的采集成功率与效率。"
arxiv_id: "2503.12287"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:48.993891+00:00"
source_sha256: "e7bd5e574ee5cd25a1b47b0547a208f9bca61e6d93d312ab22ea1ae689d074b8"
tags:
  - "机器人 / 具身智能"
  - "共享自主"
  - "双边遥操作"
  - "紧间隙装配"
  - "接触式操作"
  - "力反馈"
  - "VTLA"
  - "示范数据采集"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2503.12287</p>

# SharedAssembly: A Data Collection Approach via Shared Tele-Assembly

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Wu, Yansong, Chen, Xiao, Chen, Yu, Sadeghian, Hamid, Wu, Fan, Bing, Zhenshan, Knoll, Alois</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2503.12287) · [PDF 下载](https://arxiv.org/pdf/2503.12287) · **关键词** 共享自主, 双边遥操作, 紧间隙装配, 接触式操作, 力反馈, VTLA, 示范数据采集<br>


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

本文针对亚毫米级紧间隙装配示范难以通过传统遥操作高效采集的问题，提出在主端与从端共同嵌入装配辅助的共享自主双边遥操作框架 SharedAssembly，以降低操作门槛并提高高质量接触数据的采集成功率与效率。

**不用术语来说**：机器人把零件插入几乎没有余量的孔中时，位置稍有偏差就会发生卡滞或产生过大接触力；人通过遥操作完成这类任务，不仅要看准位置，还要持续感知并调节作用力，因此即使有经验的操作者也很难稳定、快速地采集大量成功示范。这造成了一个直接矛盾：需要触觉信息的机器人模型依赖这类高精度数据训练，但最有价值的数据恰恰最难获得。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 SharedAssembly 共享自主双边遥操作框架，在操作者侧与执行机器人侧同时引入面向装配过程的辅助，同时保留人的操作主导权，用于规模化采集紧间隙、接触密集任务的高质量示范。
- 将人的操作输入与自主力调节结合为力域引导机制，并通过覆盖不同经验水平操作者的真实亚毫米装配研究，验证该设计能够改善成功率和完成效率、降低数据采集对专家技能的依赖。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于机器人学习与双边遥操作的交叉领域。视觉-语言-动作模型（VLA）已能从大规模示范数据中学习通用操作，但现有数据主要覆盖依赖视觉的宽松接触任务；对于亚毫米间隙装配，机器人还必须感知接触状态并精细调节作用力，因此论文将融合触觉信息的基础模型统称为视觉-触觉-语言-动作模型（VTLA）。训练这类模型需要大量高质量紧间隙示范，而传统双边遥操作要求操作者同时保证定位精度和力控制，采集成功率与效率受技能水平制约。SharedAssembly所针对的基础数据采集模式是：操作者移动主端机器人，运动指令传至从端；从端执行装配并将环境接触力反馈给主端，使操作者能够感知远端接触。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**紧间隙接触式装配**

零件与目标孔位或配合面的尺寸差很小，装配过程会频繁接触，亚毫米级位置偏差就可能造成卡阻或过大接触力。它既要求精确运动，也要求根据接触状态及时调节力。

</div>
<div class="concept-item" markdown="1">

**位置-力双边遥操作**

操作者通过主端机器人产生运动输入，从端机器人跟随该运动；从端与环境接触产生的力或关节外力矩再反馈到主端。这样形成“运动向前传、接触力向后传”的双向通道。

</div>
<div class="concept-item" markdown="1">

**关节阻抗控制与无源性**

关节阻抗控制用刚度项和阻尼项把从端拉向期望关节位置与速度，使跟踪行为类似带弹簧和减振器的机械系统。无源性要求系统不凭空产生能量，论文采用时域无源方法（TDPA）维护遥操作稳定性，但不研究通信时延。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究目标是在真实机器人、接触丰富且间隙小于毫米的装配环境中，高效收集可用于VTLA模型训练的高质量操作示范。系统输入包括操作者在主端产生的关节位置与速度，以及从端执行装配时受到的环境外力矩；基础架构将主端状态作为从端期望状态，并把从端外力矩回传给操作者。SharedAssembly进一步在主端和从端嵌入装配专用辅助智能，但本节给出的前提模型仍是具有$n$个自由度、采用力矩控制、忽略关节摩擦的主从机械臂；输出是稳定的从端装配运动、可感知的力反馈及相应示范轨迹。论文假设时域无源方法可保障交互稳定性，并明确不考虑通信时延影响。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$i\in\{l,f\}$**

机器人端标记；$l$表示主端（leader），$f$表示从端（follower）。

</div>
<div class="notation-item" markdown="1">

**$\bm{q}_i,\dot{\bm{q}}_i,\ddot{\bm{q}}_i\in\mathbb{R}^n$**

第$i$端机器人的$n$维关节位置、关节速度和关节加速度。

</div>
<div class="notation-item" markdown="1">

**$\bm{\tau}_{c,i},\bm{\tau}_{ext,i}\in\mathbb{R}^n$**

第$i$端的控制指令力矩与环境或操作者施加的外部关节力矩。

</div>
<div class="notation-item" markdown="1">

**$\bm{K}_q,\bm{D}_q\in\mathbb{R}^{n\times n}$**

从端关节跟踪控制器的正定刚度矩阵与阻尼矩阵，分别惩罚位置误差和速度误差。

</div>

</div>

**直接相关的工作**

- **现有开放机器人学习数据集（如RT-1、RH20T、DROID与Open X-Embodiment）**: 这些数据集推动了通用VLA模型，但论文指出其内容主要由视觉中心的操作任务构成，不能充分提供紧间隙装配所需的接触状态、精确定位与力调节示范。
- **ForceVLA及后续触觉增强VLA框架**: ForceVLA被论文视为2025年兴起的触觉增强VLA方向代表；相关工作说明触觉对接触式操作的重要性，同时也产生了对高质量紧间隙示范数据的新需求，而SharedAssembly关注的是这种训练数据的采集瓶颈。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

视觉-触觉-语言-动作模型需要包含精确位置、接触状态和力调节信息的紧间隙装配示范，才能学习接触密集操作。然而，传统双边遥操作要求人同时处理亚毫米级运动控制和持续力调节，带来很高的认知与身体负担，进而造成执行成功率低、采集速度慢以及高质量装配数据稀缺。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **以视觉任务为主的大规模机器人数据采集与 VLA 学习**：RT-1、RH20T、DROID、Open X-Embodiment 等数据资源主要通过人工遥操作、动觉示教、脚本执行或既有数据聚合获得大量机器人轨迹，再据此训练视觉-语言-动作模型，使模型从视觉观测和语言指令预测机器人动作。
- **传统单边或双边遥操作**：操作者通过主端设备控制从端机器人；双边系统还把机器人与环境接触产生的力反馈给操作者，使人根据触觉自行判断卡滞、对准和插入状态，并实时修正运动与施力。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有大规模数据集以视觉中心的通用操作为主，紧间隙接触示范不足；在宽松间隙上采集的数据缺少紧密接触中关键的位置误差、接触状态与力变化特征，导致据此训练的策略部署到紧间隙场景时性能明显下降。
- 传统遥操作把精确对准、接触判断和力调节主要交给人完成；随着装配间隙缩小，操作负担和技能要求迅速上升，造成成功率与采集效率受限，也使数据质量和产量高度依赖少数熟练操作者。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尽管触觉增强的 VTLA 模型已显示出对接触信息的需求，现有工作仍缺少一种专门面向紧间隙装配的数据采集接口：它既要利用人的任务判断和操作意图，又要自动承担部分对准与力调节负担，并在保留人类控制权的同时，让不同经验水平的操作者都能稳定、快速地产生亚毫米任务示范。

</div>
<div markdown="1"><span>核心问题</span>

能否通过在双边遥操作的主端和从端同时加入装配专用的共享自主辅助，并将人的输入与自主力调节协调起来，在间隙不断缩小的真实装配任务中提高示范采集的成功率和完成效率，同时显著削弱性能对操作者经验的依赖？

</div>
<div markdown="1"><span>作者直觉</span>

人的优势是理解任务目标、选择操作方向并处理异常，自主控制的优势是快速、稳定地执行精细的局部力调节。SharedAssembly 让人负责高层意图和总体推进，让系统在接触阶段辅助抑制不合适的力并引导插入，因此操作者不必仅凭有限反馈反复进行细小修正；在间隙越小、容错越低时，这种分工越可能体现价值。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SharedAssembly是在传统位置—力双边遥操作上加入装配专用共享自治的控制框架。系统输入包括操作者通过主端机器人给出的运动、从端末端与环境的交互力、装配轴方向以及预先设定的摆动装配技能；系统先在主端通过软虚拟夹具约束不必要的姿态自由度，再由从端跟踪主端运动，并在接触力满足条件时自动叠加末端摆动扳手，最终输出从端装配轨迹、接触过程及可用于机器人学习的示范数据。整个设计仍保留双边力反馈，并以时域无源方法维持遥操作稳定性。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 操作者给出粗粒度装配运动

操作者负责沿装配轴平移、绕装配轴旋转和规划整体接近轨迹，而不必独立精确控制全部六维末端位姿。主端同时计算自身末端轴 $\bm{z}_l$ 与目标装配轴之间的方向误差。

<div class="method-step__io" markdown="1">

**输入**：操作者对主端机器人的物理操作、主端关节状态，以及任务预先给定的装配轴方向 $\bm{z}_{\mathrm{axis}}$。<br>
**输出**：体现操作者高层意图的主端位置和速度指令，以及待由主端自治纠正的姿态误差。

</div>

**直观理解**：人主要决定“零件往哪里走、何时插入”，系统接管最容易因手抖或视觉误差而失准的侧向倾斜。这样既不夺走人的任务决策权，也减少同时操纵多个自由度的负担。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 主端软虚拟夹具提供姿态引导

系统通过叉积和点积求出将主端末端轴对准装配轴所需的最小旋转，并用笛卡尔阻抗控制生成柔顺的姿态校正力矩。选择矩阵 $\bm{\Lambda}_1$ 只在轴外旋转维度施加约束，因此操作者仍可控制允许的平移和绕轴旋转。

<div class="method-step__io" markdown="1">

**输入**：主端当前位姿 $\bm{p}_l$、速度 $\dot{\bm{p}}_l$、装配轴 $\bm{z}_{\mathrm{axis}}$，以及从端返回的接触力矩。<br>
**输出**：经过姿态辅助后的主端关节运动，以及供从端跟踪的期望关节位置 $\bm{q}_{d,f}$ 和速度 $\dot{\bm{q}}_{d,f}$。

</div>

**直观理解**：这相当于一条有弹性的虚拟导轨：操作者仍能主动推动机器人，但导轨会温和地阻止零件歪斜。它不是替人完成全部运动，而是把运动限制在更容易成功的方向上。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 从端跟踪并判断是否进入接触关键阶段

从端以关节阻抗控制跟踪主端，同时根据末端横向接触力判断装配技能是否应启动；文中插入任务采用条件 $\lVert\bm{f}_{\mathrm{ext},f,xy}\rVert>f_t$。条件满足时自治开关 $\eta=1$，否则 $\eta=0$。

<div class="method-step__io" markdown="1">

**输入**：主端发送的期望关节状态、从端当前关节状态，以及末端测得的外部扳手 $\bm{f}_{\mathrm{ext},f}$。<br>
**输出**：当前任务阶段对应的自治等级 $\eta$，以及包含人工运动意图的基础从端控制力矩。

</div>

**直观理解**：系统把明显的侧向接触力视为“已经碰到孔壁、需要精细纠偏”的信号。未接触时机器人忠实跟随人，真正卡住或摩擦增大时才介入，避免全程自动动作干扰操作者。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 从端执行摆动技能并筛选力反馈

当 $\eta=1$ 时，从端在末端坐标系的指定旋转维度叠加周期性摆动扳手，以微调零件姿态并帮助解除卡滞；同时，系统用 $\bm{I}_6-\bm{\Lambda}_2$ 去除与主动技能同方向的反馈分量，只把其余环境作用传回主端。最终从端持续执行，直至完成紧间隙插入并记录示范。

<div class="method-step__io" markdown="1">

**输入**：基础跟踪力矩、自治等级 $\eta$、技能库中的正弦摆动扳手 $\bm{f}_{ff}$，以及技能维度选择矩阵 $\bm{\Lambda}_2$。<br>
**输出**：完成装配的从端运动与接触轨迹、经过筛选的触觉反馈，以及可供后续触觉感知机器人模型使用的高精度示范数据。

</div>

**直观理解**：机器人在接触阶段做很小的“左右试探”来寻找更顺畅的插入姿态，同时不把自己主动产生的摆动力冒充成环境阻力传给人。操作者因此主要感知真正有决策价值的碰撞和约束。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 主端共享控制律

$$
\bm{\tau}_{c,l}=\bm{J}_{l}^{T}(\bm{q}_{l})\bm{\Lambda}_{1}\left[\bm{K}_{c}(\bm{p}_{d}-\bm{p}_{l})-\bm{D}_{c}\dot{\bm{p}}_{l}\right]+\bm{c}_{l}(\bm{q}_{l},\dot{\bm{q}}_{l})+\bm{g}(\bm{q}_{l})+\bm{\tau}_{d,f}
$$

**符号说明**

- $\bm{\tau}_{c,l}$：发送给主端机器人的关节控制力矩
- $\bm{q}_{l}$：主端关节位置
- $\bm{J}_{l}(\bm{q}_{l})$：主端雅可比矩阵，用于在末端笛卡尔量与关节力矩之间映射
- $\bm{\Lambda}_{1}$：主端任务维度选择矩阵，指定机器人主动约束的自由度
- $\bm{K}_{c}$：笛卡尔空间刚度矩阵，决定位姿误差产生多强的恢复作用
- $\bm{D}_{c}$：笛卡尔空间阻尼矩阵，用于抑制过冲和振荡
- $\bm{p}_{d}$：由装配轴对准关系生成的主端期望末端位姿
- $\bm{p}_{l}$：主端当前末端位姿
- $\dot{\bm{p}}_{l}$：主端当前末端速度
- $\bm{c}_{l}(\bm{q}_{l},\dot{\bm{q}}_{l})$：主端科里奥利力和离心力项
- $\bm{g}(\bm{q}_{l})$：主端重力补偿项
- $\bm{\tau}_{d,f}$：从端环境作用传回主端的反馈力矩

<div class="equation-explanation" markdown="1">

**直观理解**：方括号内是一个柔顺的“回正”控制器：姿态偏离目标越多，恢复力越大；运动越快，阻尼抑制越强。$\bm{\Lambda}_1$ 保证该作用只施加于选定的倾斜自由度，之后雅可比转置把末端校正作用转换为关节力矩，并叠加动力学补偿与从端触觉反馈。<br>
**原文位置**：第 IV-1 节，式 (5)；目标轴误差的构造见式 (4)

</div>

</div>

<div class="equation-block" markdown="1">

#### 接触触发的从端共享自治控制

$$
\begin{aligned}\bm{\tau}_{c,f}&=\bm{K}_{q}\bm{e}_{q}+\bm{D}_{q}\dot{\bm{e}}_{q}+\bm{c}_{f}(\bm{q}_{f},\dot{\bm{q}}_{f})+\bm{g}_{f}(\bm{q}_{f})+\eta\bm{J}_{b,f}^{T}(\bm{q}_{f})\bm{\Lambda}_{2}\bm{f}_{ff},\\ \eta&=\begin{cases}1,&\mathcal{C}(\bm{f}_{ext,f})\text{ holds},\\0,&\text{else},\end{cases}\qquad f_{ff,j}(t)=a_j\sin(2\pi f_jt+\varphi_j)\end{aligned}
$$

**符号说明**

- $\bm{\tau}_{c,f}$：发送给从端机器人的关节控制力矩
- $\bm{K}_{q}$：从端关节跟踪刚度矩阵
- $\bm{D}_{q}$：从端关节跟踪阻尼矩阵
- $\bm{e}_{q}$：期望从端关节位置与当前关节位置之差
- $\dot{\bm{e}}_{q}$：期望从端关节速度与当前关节速度之差
- $\bm{c}_{f}(\bm{q}_{f},\dot{\bm{q}}_{f})$：从端科里奥利力和离心力项
- $\bm{g}_{f}(\bm{q}_{f})$：从端重力补偿项
- $\eta$：二值自治等级；取一时启用装配技能，取零时关闭
- $\bm{J}_{b,f}(\bm{q}_{f})$：从端身体雅可比矩阵，将关节速度映射为末端坐标系中的运动旋量
- $\bm{\Lambda}_{2}$：从端技能维度选择矩阵
- $\bm{f}_{ff}$：在末端坐标系表达的前馈装配扳手
- $\mathcal{C}(\bm{f}_{ext,f})$：依据外部接触扳手定义的任务特定技能触发条件
- $f_{ff,j}(t)$：时刻 t 在末端坐标系第 j 个方向上的前馈扳手分量
- $a_j$：第 j 个摆动分量的幅值
- $f_j$：第 j 个摆动分量的频率
- $\varphi_j$：第 j 个摆动分量的相位

<div class="equation-explanation" markdown="1">

**直观理解**：控制律的前四项让从端柔顺地跟随主端，最后一项才是机器人新增的装配技能。接触条件不满足时 $\eta=0$，技能项完全消失；检测到显著横向接触后 $\eta=1$，系统把正弦摆动扳手映射为关节力矩，在选定姿态方向执行细微纠偏。<br>
**原文位置**：第 IV-2 节，式 (6)、式 (7) 与式 (9)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。SharedAssembly不是通过数据拟合参数的学习模型，而是面向机器人示范采集的模型化控制系统；论文给出的刚度、阻尼、选择矩阵、力阈值和摆动参数用于在线控制，不存在损失函数、梯度更新或训练集优化目标。其产物才是未来可用于训练触觉感知机器人基础模型的装配示范。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 主端自由度选择与软虚拟夹具**

该模块把任务空间分成操作者控制子空间和机器人约束子空间。主端根据 $\bm{z}_l\times\bm{z}_{\mathrm{axis}}$ 与 $\arccos(\bm{z}_l\cdot\bm{z}_{\mathrm{axis}})$ 构造目标姿态，再通过选择矩阵 $\bm{\Lambda}_1$ 和笛卡尔刚度、阻尼产生姿态校正；在论文的竖直装配设置中，$\bm{\Lambda}_1=\operatorname{diag}(0,0,0,1,1,0)$，即只约束末端的两个轴外旋转分量。

> 直观理解：紧配合装配最怕零件轴线略微倾斜，而视觉透视和多自由度操作会放大这种误差。主端辅助把最难维持的两个倾斜角稳定住，使人可以把注意力集中在接近路径、下压和绕轴调整上。

**2. 接触触发的从端装配技能与自治分配**

该模块以任务特定条件 $\mathcal{C}(\bm{f}_{\mathrm{ext},f})$ 在人工跟踪与局部自治之间切换。对紧间隙插入，系统监测末端坐标系 $xy$ 平面的接触力，并在 $\lVert\bm{f}_{\mathrm{ext},f,xy}\rVert>f_t$ 时令 $\eta=1$；随后在 $rx$、$ry$ 方向应用由幅值、频率和相位定义的正弦摆动扳手，所用选择矩阵为 $\bm{\Lambda}_2=\operatorname{diag}(0,0,0,1,1,0)$。

> 直观理解：人擅长决定总体动作，却很难隔着遥操作系统快速完成细微接触纠偏；机器人则适合重复稳定的小幅摆动。因而系统只在检测到孔壁接触后调用局部技能，把“是否继续、往哪里推进”留给人，把“如何微调姿态摆脱卡滞”交给机器人。

**3. 双边力反馈筛选与稳定性维护**

传统双边遥操作将从端环境作用映射为关节力矩并反馈至主端；SharedAssembly进一步从反馈中去除技能作用维度，采用 $\bm{J}_{b,f}^{T}(\bm{q}_f)(\bm{I}_6-\bm{\Lambda}_2)\bm{f}_{\mathrm{ext},f}$ 作为返回力矩。系统还采用由既有工作改造的时域无源方法保持遥操作无源性和稳定性，但论文明确不讨论通信时延影响。

> 直观理解：若机器人主动摆动产生的反力全部传回，人会误以为环境正在阻碍自己，甚至与自治控制相互对抗。筛选后，人仍能感到未被机器人接管方向上的真实接触；无源性机制则用于避免双向能量交换造成振荡或失稳。

**训练与推理**

系统没有离线训练阶段。部署前需要确定任务装配轴、主端与从端受控自由度、接触触发条件、力阈值及摆动技能参数；在线执行时，主端持续读取操作者运动并施加轴线对准辅助，从端持续接收期望关节状态、执行阻抗跟踪并测量接触扳手。当横向接触力超过阈值时，从端自动启用摆动技能；技能方向上的外力不反馈给操作者，其余外力经双边通道返回主端。该循环持续到插入完成或任务终止，期间记录机器人状态、动作与接触信息作为示范数据。

**复现信息**

论文采用主端和从端均为力矩控制机器人的双边位置—力架构，并在从端使用关节阻抗跟踪。真实实验将装配轴设为全局竖直方向 $[0,0,1]^T$，因此主端和从端均以 $\operatorname{diag}(0,0,0,1,1,0)$ 选择两个轴外旋转维度；插入技能由末端坐标系 $xy$ 平面的接触力阈值触发，并在 $rx$、$ry$ 方向执行摆动。系统使用时域无源方法维护稳定性，但通信时延不属于本文研究范围；所给摘录未明确报告控制频率、阈值 $f_t$、摆动幅值、频率、相位以及刚度和阻尼的具体数值，因此复现时仍需查验完整论文或作者代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 间隙评估任务集：任务 A、B、C，用于检验装配间隙变化对遥操作表现的影响。原文节选未提供各任务的具体间隙、物体尺寸及训练/测试划分；它们是实体机器人用户实验任务，而非离线数据集。
- 形状评估任务集：任务 D、E、F，使用不同插销几何形状，检验方法对装配对象形状变化的适应性。具体形状配置位于原文 Table II，但当前节选未给出。
- 用户研究试次：招募 30 人，剔除 1 人的无效数据后分析 29 人，其中专家 8 人、中等经验者 10 人、新手 11 人。每位参与者在 6 个任务、3 种方法下各重复 3 次，因此按所述协议应形成 $29\times6\times3\times3=1566$ 个试次；这是依据实验设计计算的规模，并非原文直接报告的汇总数字。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**成功率（$SR$）**

定义为 $SR=N_{\mathrm{success}}/N_{\mathrm{total}}$，其中 $N_{\mathrm{success}}$ 是成功试次数，$N_{\mathrm{total}}$ 是全部试次数。若任务未在 60 秒内完成，或违反机器人安全约束，则该试次判为失败。 （越高越好，因为它直接反映系统稳定完成高精度装配、从而产生可用示范数据的概率。）

</div>
<div class="metric-item" markdown="1">

**任务完成时间**

实验将过程分为“移动至接触”和“引导插入”两阶段，分别关注平均引导插入时间 $\bar{t}_{\mathrm{insert}}$ 与平均完整装配时间 $\bar{t}_{\mathrm{entire}}$。完整时间按所有试次平均，失败试次的 $t_{\mathrm{entire},i}$ 统一记为 60 秒，因此该指标同时惩罚操作缓慢和失败。 （越低越好；$\bar{t}_{\mathrm{insert}}$ 更集中地衡量接触丰富、精度要求最高的插入阶段，$\bar{t}_{\mathrm{entire}}$ 则衡量端到端操作效率。）

</div>
<div class="metric-item" markdown="1">

**数据采集效率（$\eta_c$）**

定义为 $\eta_c=(SR/\bar{t}_{\mathrm{entire}})\times60$，其中时间以秒统计并通过乘以 60 换算到每分钟尺度。它把成功概率与平均耗时结合起来，近似表示单位时间能够获得多少次成功装配示范。 （越高越好，因为高成功率和短完成时间都会增加单位时间内采集到的有效数据量。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 全部亚毫米装配任务上的总体成功率

<div class="result-value" markdown="1">

作者报告 SharedAssembly 的装配成功率达到 97%，并将其概括为在困难的亚毫米任务上取得很高的可靠性。当前节选没有给出该数值对应的逐任务分解、置信区间、显著性检验或两个基线的具体成功率。

</div>

这意味着在该用户研究及其任务配置中，采用共享双边遥操作时绝大多数试次能够在安全约束和 60 秒时限内完成。它支持系统适合采集可用装配示范的主张，但不能单凭这一汇总值证明其可推广到其他机器人、网络条件、零件材料或未测试的装配类型。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Rigorous real-world user studies on challenging sub-millimeter tasks show that SharedAssembly achieves an exceptional 97% assembly success rate while significantly boosting completion efficiency.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 不同装配间隙下的相对性能

<div class="result-value" markdown="1">

作者声称 SharedAssembly 相对现有遥操作方法的性能收益会随装配间隙缩小而更加明显，但当前节选未提供任务 A–C 的具体间隙值、逐条件结果或统计量。

</div>

该趋势若由完整结果支持，说明共享自主主要在容错空间很小、人工仅凭视觉或力反馈更难精确对准时发挥作用，而不是只在简单任务上节省时间。不过，没有逐间隙数据时，无法判断收益增长的大小、单调性及统计可靠性。

<div class="result-source" markdown="1">

来源：Abstract；对应实验设计见 Section V-C, Phase II

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Notably, these performance gains become even more pronounced as the assembly clearance shrinks.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 不同经验水平操作者之间的性能差距

<div class="result-value" markdown="1">

作者声称 SharedAssembly 消除了明显的专业经验差距，使新手使用该方法时可以达到、甚至超过专家使用传统系统时的表现。当前节选未报告新手与专家的分组分数、效应量或交互显著性。

</div>

该结论针对的是“新手加 SharedAssembly”与“专家加传统遥操作”的跨方法比较，表明系统可能把部分精细控制负担从人转移给自动辅助。它不等同于证明新手获得了与专家相同的通用操作技能，也不能说明在关闭辅助后新手仍能保持该水平。

<div class="result-source" markdown="1">

来源：Abstract；参与者分组见 Section V-C

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Furthermore, our framework effectively eliminates the expertise gap, enabling novice operators to match or even outperform expert operators using conventional systems.

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

- 单边遥操作（Unilateral Teleoperation）：操作者只依据视觉信息控制从端机器人，不获得从端接触力反馈。该基线代表常见且自主程度最低的遥操作方式，用于判断力反馈与共享自主整体是否有价值。
- 双边遥操作（Bilateral Teleoperation）：将从端发生的交互力通过主端触觉反馈给操作者，但不加入 SharedAssembly 的共享自主。它与单边遥操作的比较主要检验力反馈的作用，与 SharedAssembly 的比较则检验在已有力反馈上进一步加入装配辅助是否有效。
- 共享双边遥操作（Shared Bilateral Teleoperation，即 SharedAssembly）：同时采用双边力反馈与共享自主，是待评估方法而非外部基线。三种方法构成从仅视觉、到力反馈、再到力反馈加共享自主的递进比较。

**实验想回答的问题**

- RQ1：在亚毫米间隙装配中，SharedAssembly 相比仅视觉的单边遥操作和带力反馈的双边遥操作，能否提高成功率、缩短完成时间并提升数据采集效率？
- RQ2：SharedAssembly 能否缩小新手、中等经验者与专家之间的操作性能差距，从而降低高精度装配数据采集的技能门槛？

**实验实现**

实验使用两台 Franka Emika Panda 机器人分别作为主端和从端；主端计算机运行 Ubuntu 20.04、Intel Core i7-10700，从端计算机运行 Ubuntu 20.04、Intel Core i9-11900K。两台计算机在同一网络内通过 UDP 通信，作者认为网络时延可忽略。从端安装两台 Intel RealSense D435i，相机垂直布置并向操作者提供双视角。用户实验先以较大间隙孔完成 3 次训练，随后依次评估间隙任务 A–C 和形状任务 D–F；每位参与者对每个任务、每种方法重复 3 次。为降低技能学习中的感觉运动适应和认知预期偏差，任务顺序与方法顺序均随机化，且参与者不知道当前评估的是哪一种遥操作方法。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work introduces a shared-autonomy teleoperation framework for scalable collection of contact-rich robotic assembly demonstrations.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`e7bd5e574ee5cd25a1b47b0547a208f9bca61e6d93d312ab22ea1ae689d074b8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
