---
title: "[论文解读] Spatial-Semantic Reasoning using Large Language Models for Efficient UAV Search Operations"
description: "[arXiv 2608.28270][机器人 / 具身智能] 本文研究如何让无人机仅借助轻量级目标检测、三维空间信息与大语言模型的持续语义推理，在未知环境中根据自然语言指令优先搜索最可能出现目标的区域，并以平滑连续轨迹缩短 ObjectNav 任务时间。"
arxiv_id: "2608.28270"
announcement_date: "2026-08-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:36:07.366337+00:00"
source_sha256: "d58fce02f2da0229d6e732a96acd2fdc9539b5c1c617c8222e0d9af74e7a056d"
tags:
  - "机器人 / 具身智能"
  - "LLM Reasoning"
  - "LLM 其他"
  - "物体目标导航"
  - "无人机"
  - "大语言模型"
  - "语义推理"
  - "三维空间建模"
  - "轨迹规划"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2608.28270</p>

# Spatial-Semantic Reasoning using Large Language Models for Efficient UAV Search Operations

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Marin Maletic, Marijana Peti, Tamara Petrovic, Stjepan Bogdan</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> thanks: Authors are with the University of Zagreb Faculty of Electrical Engineering and Computing, LARICS (Laboratory for Robotics and Intelligent Control Systems), Unska 3, 10000 Zagreb, Croatia</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28270v1) · [PDF 下载](https://arxiv.org/pdf/2608.28270v1) · **关键词** 物体目标导航, 无人机, 大语言模型, 语义推理, 三维空间建模, 轨迹规划<br>


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

本文研究如何让无人机仅借助轻量级目标检测、三维空间信息与大语言模型的持续语义推理，在未知环境中根据自然语言指令优先搜索最可能出现目标的区域，并以平滑连续轨迹缩短 ObjectNav 任务时间。

**不用术语来说**：当无人机受命寻找“卧室里使用的椅子”或“咖啡杯附近的钥匙”时，逐块扫描整个环境虽然直接，却耗时且可能漏掉小型或被遮挡的目标；它需要像人一样利用常识判断目标更可能出现在哪里，同时还必须在有限机载算力下快速作出判断，并把判断转化为真实无人机能够安全、顺畅执行的飞行路线。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出面向真实无人机零样本目标导航的轻量级框架：融合实时目标检测、目标三维定位、占据地图和纯 LLM 语义推理，依据自然语言指令与不断更新的观测动态评估候选区域的相关性，避免依赖计算开销更高的 VLM。
- 将语义优先级转化为三维连续飞行行为，并用多项式样条插值生成平滑、动力学可行的轨迹，使无人机能在飞行中持续扫描、更新判断，并围绕高相关候选物执行细致搜索。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于具身人工智能与无人机自主导航交叉领域，核心任务是让无人机理解人类自然语言目标，并在未知环境中通过视觉感知、空间建模与运动规划寻找指定物体。研究重点是物体目标导航（Object Goal Navigation，ObjectNav）：系统不仅要识别目标类别，还要将语言中的语义和空间线索与实际环境中的物体及位置对应起来。与主要在模拟器中运行的地面机器人方法不同，本文关注机载、实时运行的无人机系统，因此还必须处理三维空间、连续飞行轨迹、计算资源限制和真实飞行动力学可行性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**物体目标导航（ObjectNav）**

ObjectNav要求智能体在此前未见过的环境中，根据目标物体的语义类别或自然语言描述自主搜索并定位目标，例如寻找“椅子”或“卧室里使用的椅子”。它不同于只执行固定路线的导航，系统需要边观察环境边决定下一步搜索区域。

</div>
<div class="concept-item" markdown="1">

**具身人工智能与视觉—语言导航**

具身人工智能研究能够感知环境、进行推理并采取物理行动的智能体；视觉—语言导航（VLN）则要求智能体把自然语言指令落实为环境中的导航行为。本文借用这类方法的语言理解能力，但将任务聚焦到无人机搜索语义目标，而不是逐步执行诸如“经过画后左转”的路线指令。

</div>
<div class="concept-item" markdown="1">

**大语言模型与视觉—语言模型**

大语言模型（LLM）主要处理文本并进行语义推理；视觉—语言模型（VLM）同时处理图像与语言，能够直接建立视觉内容和文字描述之间的联系。本文使用目标检测器提供的物体信息，再让LLM结合物体及空间上下文推断搜索优先级，目的是避免VLM较高的计算负担，支持机载实时推理。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

系统输入包括用户提供的自然语言目标指令、无人机相机观测和深度传感器数据；指令可以包含目标类别、属性或空间关系，例如寻找“咖啡杯旁边的钥匙”。系统在未知环境中实时检测语义物体，将深度观测建立为空间占据地图，并估计候选物体在三维空间中的位置。输出是目标相关性排序或最值得搜索的区域，以及一条能够在三维空间中连续飞行、平滑执行并持续更新的无人机轨迹；任务成功意味着无人机在搜索过程中发现指定目标。本文假设目标可通过视觉检测获得一定线索，且无人机拥有相机、深度传感器和用于飞行控制的位置估计能力；具体传感器噪声、环境动态性和目标检测失败的形式，原文未明确完整规定。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$ObjectNav$**

物体目标导航任务，即在未知环境中搜索并定位语言指定的物体。

</div>
<div class="notation-item" markdown="1">

**$LLM$**

大语言模型，用于解释用户指令，并根据检测到的物体与空间上下文进行语义推理。

</div>
<div class="notation-item" markdown="1">

**$VLM$**

视觉—语言模型，同时处理视觉和语言信息；本文将其作为相关工作中的对比技术类别，而非主要推理模块。

</div>
<div class="notation-item" markdown="1">

**$UAV$**

无人机（Unmanned Aerial Vehicle），本文中承担环境观测、搜索和轨迹执行任务的飞行机器人。

</div>

</div>

**直接相关的工作**

- **Zero-Shot Object Navigation（ZSON）**: ZSON使智能体能够在未见过的环境中寻找指定物体类别，即使训练阶段没有该物体的标注示例。本文继承其零样本、开放环境导航的设定，但进一步面向无人机实时搜索，并结合自然语言语境、三维空间建模和连续轨迹规划。
- **Language-driven ZSON（L-ZSON）**: L-ZSON在ZSON基础上加入自然语言指令，使系统能够理解属性、空间线索和复杂描述，例如“寻找咖啡杯旁边的钥匙”。本文与其共享语言驱动的语义搜索方向，但强调使用轻量的LLM推理、实时更新候选区域以及在真实无人机上执行可行的三维飞行轨迹。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

面向真实 UAV 的 ObjectNav 不仅要求在从未见过的环境中理解开放式指令、识别目标与环境线索，还要求尽快完成任务。穷举式覆盖搜索会把大量时间花在低概率区域，而小型、部分遮挡的物体又可能需要近距离细致观察；因此系统必须同时兼顾语义导向的区域选择、实时响应、搜索可靠性以及符合无人机运动约束的三维机动。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **端到端训练式 ObjectNav**：通过大规模带标注数据联合学习感知、决策与导航策略，让智能体从视觉输入直接产生搜索动作；这类方法通常针对训练时定义的目标类别、环境分布和任务设置进行优化。
- **基于 LLM/VLM 的零样本语义导航**：ZSON、L-ZSON 等方法利用预训练模型处理未见目标或开放式语言指令，OpenFMNav、LM-Nav、ESC 和 PixNav 等则借助 VLM 将视觉观测与语义知识对齐，从而推断目标可能所在的位置；现有评测多在 Matterport3D、Gibson 或 Habitat 等模拟环境中，以前进、固定角度转向和停止等离散动作执行导航。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 端到端方法依赖大规模标注数据和较多计算资源，导致扩展到新类别、新环境及真实部署较困难；VLM 方法虽能增强视觉—语义推理，但计算负担较高，可能无法满足机载实时推理和时间敏感任务的要求。
- 多数现有工作面向模拟器中的地面机器人，采用简化的离散动作，并主要关注成功率和按路径长度加权的成功率等空间效率指标；这不能充分反映 UAV 的三维连续运动、真实动力学可行性、实时响应、搜索时长与动态机动需求，因而限制向真实无人机系统迁移。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚缺少一种能够部署到真实 UAV 上的统一 ObjectNav 方案：它既要在零样本条件下利用自然语言和环境语义持续重排搜索区域，又要避免 VLM 的较高机载开销，并将推理结果落实为可实时更新、平滑且动力学可执行的三维轨迹。换言之，语义推理的开放性、在线计算的轻量性与真实无人机控制的连续性尚未被同时解决。

</div>
<div markdown="1"><span>核心问题</span>

在未知环境和有限机载计算条件下，能否用实时目标检测与 LLM 对自然语言指令、已检测物体及三维空间关系进行在线联合推理，从而引导 UAV 优先检查高概率区域，并在保持目标定位可靠性的同时缩短实际搜索时间？

</div>
<div markdown="1"><span>作者直觉</span>

目标与周围物体通常存在可利用的语义共现关系，例如钥匙更可能靠近杯子或桌面，而不是随机出现在每个位置。目标检测器负责把图像压缩成少量物体标签和位置，LLM 再依据指令与常识给这些候选位置排序，因而无须让更重的 VLM 反复处理完整图像；随着新物体被发现，排序可持续修正。最后让无人机沿平滑轨迹飞向高相关区域并做局部细致扫描，就有机会把低效的全覆盖搜索转化为“先查最可能的位置”，同时降低漏检小型或遮挡目标的风险。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法面向未知环境中的无人机目标导航（ObjectNav）：输入用户的自然语言目标描述、相机图像、三维占据地图和无人机状态，先检测并定位场景中的物体，再由大语言模型（LLM）依据物体语义、空间关系、已访问区域和用户上下文估计目标附近各候选物体的相关性，选择最值得搜索的区域。随后，系统使用三维路径规划和七阶多项式样条生成可飞行轨迹，并在目标物体周围执行多视角彻底搜索；若当前候选区域相关性不足，则退回预设扫描策略并继续收集信息。整体输出是候选相关物体 $O^{*}$、通往其附近区域的安全轨迹，以及目标被找到或搜索失败的终止状态。

从直观上看，系统不是让无人机均匀扫遍整个空间，而是先问：用户要找的东西通常会和哪些已看到的东西一起出现？例如，寻找电脑鼠标时，桌子和显示器比床更可能是有效搜索位置。LLM负责把这种语言和常识线索转化为搜索优先级，几何模块则保证无人机能够安全、平滑地飞到相应位置。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 三维环境表示与状态准备

系统使用OctoMap表示三维空间，并将体素划分为自由空间 $S_{\text{free}}$、占据空间 $S_{\text{occ}}$和未知空间 $S_{\text{unk}}$，满足 $S=S_{\text{free}} S_{\text{occ}} S_{\text{unk}}$；同时记录无人机位姿和搜索历史。论文的主要实验假设地图已知且无人机能够精确定位，但作者指出也可结合机载LiDAR和增量建图处理未知环境。

<div class="method-step__io" markdown="1">

**输入**：预先构建的环境地图 $S$、无人机当前位姿 $C$、相机数据和已访问区域 $V_{\text{visited}}$。<br>
**输出**：可用于碰撞检查和物体三维定位的体素地图，以及当前搜索状态 $D$ 的空间部分。

</div>

**直观理解**：这一步相当于给无人机一张带有三种标记的立体地图：哪些地方能飞、哪些地方有障碍、哪些地方还不了解。它还要记住自己到过哪里，避免反复搜索同一区域。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 视觉检测与三维语义定位

YOLO-based视觉感知器将每帧图像映射为检测集合 $o_k=\{o_1,\ldots,o_{m_k}\}$，每个检测包含边界框、语义类别和置信度。系统根据边界框中心像素、相机内参和镜头畸变计算视线方向，从位姿 $C$沿该方向对OctoMap执行射线投射，取到达的第一个占据体素作为物体位置；随后对多帧检测按空间邻近性和语义标签使用DBSCAN聚类。

<div class="method-step__io" markdown="1">

**输入**：连续相机帧 $I_k$、相机内参、无人机当前世界位姿 $C$和占据空间 $S_{\text{occ}}$。<br>
**输出**：累计且去重后的三维物体集合 $\mathcal{O}=\{O_1,\ldots,O_n\}$，其中每个物体包含三维位置 $pos_i$和类别 $class_i$。

</div>

**直观理解**：相机只能告诉系统物体在画面的哪个位置，深度地图则帮助它沿这条视线找到物体在现实空间中的位置。多次看到同一把椅子时，聚类步骤会把这些观测合并成一个稳定的椅子记录。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### LLM语义相关性推理与动作选择

提示词要求LLM根据目标描述和带坐标的物体列表判断哪个物体附近最可能存在目标，并返回相关性标志、最相关物体及解释。系统对候选物体估计后选择 $O^{*}=\arg\max_{O_i\in\mathcal{O}}P(O_i\mid D,T)$；若最高相关性低于最低阈值，则执行墙面跟随等后备扫描，否则前往 $O^{*}$ 附近彻底搜索，若相关性超过更高阈值则判定目标已找到。

<div class="method-step__io" markdown="1">

**输入**：用户指令 $U$、目标物体 $T$、检测物体集合 $\mathcal{O}$、三维坐标、物体间空间关系、已访问区域和历史数据 $D$。<br>
**输出**：最相关候选物体 $O^{*}$、对应搜索决策，以及更新后的知识状态 $D$。

</div>

**直观理解**：LLM像一个会利用常识的搜索指挥员：它把“找我的鼠标”和“看到了显示器、桌子”联系起来，优先安排显示器或办公桌附近的搜索。搜索失败后，系统降低已检查候选的位置价值，把注意力转移给其他候选。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 安全轨迹生成与闭环彻底搜索

首先在三维空间用A*搜索从当前位置到候选区域的离散路径，并剔除穿过障碍或不在自由空间内的路径点；然后在可行三维航点上用七阶多项式样条生成满足位置、速度和加速度约束的连续轨迹。到达后，系统沿固定高度和半径执行环绕式检查，必要时因墙体或边界将圆形轨迹调整为半圆，并持续检测新物体、更新已访问区域和重新调用LLM。

<div class="method-step__io" markdown="1">

**输入**：当前无人机位姿、候选物体 $O^{*}$ 的三维位置、自由空间 $S_{\text{free}}$、占据地图和持续到达的视觉观测。<br>
**输出**：平滑、避障且可执行的无人机轨迹；目标找到时输出成功，遍历空间仍未找到时输出失败假设 $B_{\text{none}}$。

</div>

**直观理解**：A*决定从这里到目标区域应该经过哪些安全点，样条曲线再把折线变成无人机能平稳飞行的连续路线。环绕目标区域是为了从不同角度观察被物体遮挡的目标，而不是只从一个方向看一次。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 后验相关性分解

$$
P(O_i\mid D,T)\propto P(D\mid O_i,T)\cdot P(O_i\mid T)
$$

**符号说明**

- $O_i$：第 $i$ 个已检测候选物体。
- $D$：无人机在搜索中累积的数据，包括用户指令、已检测物体、空间关系和已访问区域。
- $T$：用户希望找到的目标物体，由自然语言指令中的语义类别或描述确定。
- $P(O_i\mid D,T)$：在目标 $T$ 和当前数据 $D$ 条件下，候选物体 $O_i$ 附近适合寻找目标的后验概率，即相关性分数。
- $P(D\mid O_i,T)$：若目标 $T$ 与 $O_i$ 空间相关，观察到当前数据 $D$ 的似然。
- $P(O_i\mid T)$：目标 $T$ 出现在 $O_i$ 附近的先验概率，反映语义关联和共现知识。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把相关性拆成两类证据：一类是常识先验，例如鼠标和显示器通常共处；另一类是当前任务中已经观察到的证据，例如某个区域尚未被搜索或周围出现了相关物体。论文把这种概率估计交给LLM，但未给出一个可训练的数值概率模型或明确的概率标定过程。<br>
**原文位置**：II-D 1，式（5）

</div>

</div>

<div class="equation-block" markdown="1">

#### 最相关物体选择

$$
O^{*}=\arg\max_{O_i\in\mathcal{O}}P(O_i\mid D,T)
$$

**符号说明**

- $O^{*}$：当前被选为首要搜索中心的最相关物体。
- $\mathcal{O}$：经过多帧检测和DBSCAN合并后的候选物体集合。
- $\arg\max$：返回使后验相关性最大的候选物体。

<div class="equation-explanation" markdown="1">

**直观理解**：系统比较所有已知候选物体，选择目标最可能出现的那个作为下一次搜索中心。它不是直接飞向检测到的目标，而是飞向目标可能隐藏在其附近的语义锚点。<br>
**原文位置**：II-D 1，式（6）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告对YOLO检测器、DBSCAN、LLM或轨迹规划器进行联合训练，也未定义用于端到端梯度优化的损失函数。因此该方法的核心不是训练一个新的导航网络，而是在推理阶段调用现成的视觉检测、地图、聚类、LLM推理和路径规划组件；式（5）中的概率关系描述决策逻辑，不构成已报告的可优化训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 三维体素地图与物体定位模块**

环境由OctoMap层次化占据网格表示，体素状态为自由、占据或未知。视觉检测器输出二维边界框和类别；位置估计器利用相机内参把目标中心像素转换为三维视线，再从无人机位姿向地图射线投射，获取第一个占据体素。跨帧观测通过按空间距离和语义类别约束的DBSCAN聚类合并。

> 直观理解：该模块把“图像里看到一个物体”变成“地图中某个具体位置有一个物体”。这是后续语义推理和避障的共同基础：LLM需要坐标来理解空间关系，路径规划需要地图来判断能否飞行。

**2. 概率相关性模块与LLM决策逻辑**

模块以候选物体集合 $\mathcal{O}$、目标 $T$和搜索数据 $D$为输入，要求LLM估计每个 $O_i$ 的后验相关性 $P(O_i\mid D,T)$。$D$包含用户指令、已检测物体及其空间关系和已访问区域；系统依据最高候选的最低阈值和目标确认阈值在后备扫描、局部彻底搜索和终止之间切换。

> 直观理解：这里的“相关性”不是物体本身像不像目标，而是目标出现在它附近的可能性。例如鼠标不一定已经被检测到，但看到显示器可以提高搜索该处的优先级。阈值机制避免系统在证据不足时盲目围绕某个物体搜索。

**3. A*与七阶样条轨迹规划模块**

规划分为离散和连续两阶段：A*在三维体素空间中寻找到候选区域的无碰路径，并通过OctoMap检查航点；七阶多项式样条将可行航点插值为连续轨迹，同时满足位置、速度和加速度约束。局部检查轨迹通常是固定高度、指定半径的圆周路径，但会根据墙体和自由空间裁剪为可行部分。

> 直观理解：语义模块只负责决定“先去哪里”，不能直接保证无人机飞得过去。该模块把搜索意图转成真实飞行控制器可执行的平滑路线，并在狭窄或靠墙场景中删去危险的环绕部分。

**训练与推理**

训练阶段：原文未明确报告本文是否重新训练YOLO检测器、使用何种训练数据或对LLM进行微调。推理阶段从自然语言指令 $U$ 解析目标 $T$，对每帧图像 $I_k$执行目标检测，再结合相机内参、无人机位姿 $C$和 $S_{\text{occ}}$估计物体三维位置；跨帧结果经DBSCAN合并为 $\mathcal{O}$，并与已访问区域、空间关系和历史观测组成 $D$。

随后，系统把目标描述、物体标签和三维坐标、已访问区域及所需输出格式放入提示词，要求LLM返回相关性标志、最高相关候选和解释。若候选相关性不足，系统采用后备扫描策略获取更多观测；若达到最低阈值，则用A*到达候选区域并执行环绕式彻底搜索；新观测会更新 $D$ 并再次推理，直到目标相关性达到更高确认阈值而成功终止，或整个空间被搜索后进入 $B_{\text{none}}$ 失败状态。

**复现信息**

方法依赖预先生成的OctoMap和精确定位；真实实验中地图由LiDAR与Cartographer SLAM生成，定位由OptiTrack提供。视觉模块使用基于YOLO的检测器，三维定位需要相机分辨率、镜头畸变和视场角等内参；路径规划使用三维A*与七阶多项式样条，并在执行前检查自由空间和障碍物。LLM提示词要求输出目标相关标志、最相关物体的标签与三维坐标以及解释。

论文报告，仿真中LLM首次决策的平均推理时间约为 $9.97$ 秒，该时间计入搜索时间；后续推理与轨迹执行并行，因此不额外增加总搜索时间。除这些信息外，原文未明确报告LLM型号、提示词完整实现、相关性阈值数值、YOLO模型版本与置信度设置、DBSCAN参数、样条边界条件或控制器细节；这些缺失会限制严格复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 仿真场景：论文报告了三个仿真场景，并用其比较 LLM 引导搜索与 Lawn Mower 基线；原文未明确报告场景规模、数据划分或具体环境名称。
- 真实世界环境：用于检验系统在实体无人机上的可行性；原文未明确报告实验环境数量、规模或数据划分。
- 预先构建的三维地图：仿真和真实环境均使用外部 LiDAR 采集点云，并通过 Cartographer SLAM 预先建图，再用于导航和语义定位。这是实验地图来源，不是独立的监督学习数据集。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务时长或任务持续时间**

衡量无人机从开始搜索到完成目标定位所需的时间，用于评估搜索效率。 （越低越好，因为更短的任务时间表示搜索更高效。原文所给摘录未明确报告具体数值或计算公式。）

</div>
<div class="metric-item" markdown="1">

**搜索准确率**

衡量系统成功找到指定目标的能力。 （越高越好，因为较高准确率表示目标搜索更可靠。原文所给摘录未明确报告具体定义或数值。）

</div>
<div class="metric-item" markdown="1">

**原文未明确报告的其他指标**

所给实验摘录没有提供可核实的第三项正式评价指标。 （原文未明确报告。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 仿真环境中，LLM 引导搜索与 Lawn Mower 基线的比较

<div class="result-value" markdown="1">

论文将仿真结果用于比较语义引导搜索和传统 Lawn Mower 搜索，并声称前者能够减少任务持续时间，同时维持较高的搜索准确率；所给摘录未提供表格中的具体数值、相对提升幅度或统计检验结果。

</div>

该结果支持这样一种解释：如果系统能先判断哪些已观测物体及其空间位置更可能与用户指令相关，就可能避免对整个区域进行均匀覆盖，从而节省搜索时间。但由于当前材料没有完整表格数值，不能判断改进幅度，也不能确认优势是否在所有三个场景中都稳定成立。

<div class="result-source" markdown="1">

来源：III Results；III-A Simulation results；Table I

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The results of this work are presented through a detailed analysis of both simulation and real-world experiments, highlighting the effectiveness of semantic-guided search in comparison to traditional, non-semantic search strategies.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 真实世界 Crazyflie 2.1 平台上的搜索实验

<div class="result-value" markdown="1">

论文报告了真实世界实验，并将其作为验证系统实际运行能力的场景；所给摘录未明确报告真实实验的任务时长、搜索准确率、成功率或与基线的完整数值比较。

</div>

真实平台实验主要说明该方法不只依赖仿真器中的离散动作空间，而能够在实体无人机、相机目标检测和预建地图条件下运行。不过，由于地图是预先构建的，且当前材料没有完整性能数据，这一结果不能证明系统已经能在完全未知环境中独立完成实时建图与搜索。

<div class="result-source" markdown="1">

来源：III Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The experimental platform is the Crazyflie 2.1 nano-UAV, a lightweight and modular quadcopter equipped with an AI Deck that features a monochrome camera.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 从自然语言指令到目标定位的端到端流程

<div class="result-value" markdown="1">

系统先接收自然语言指令并进行 360 度扫描，再由 LLM 根据检测物体和空间信息决定下一步动作，最后围绕语义相关物体执行细致搜索；原文所给摘录未报告该流程的独立消融结果或逐阶段准确率。

</div>

该结果展示的是系统集成能力，而不是单独证明 LLM、YOLO11 或 OctoMap 中某个模块的因果贡献。它表明各模块可以串联成搜索流程，但不能仅凭流程描述判断语义推理相对于视觉检测或地图定位分别带来了多少收益。

<div class="result-source" markdown="1">

来源：Fig. 5；III Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The process begins with the user providing natural-language instructions, after which the UAV performs a 360-degree scan to survey and detect surrounding objects.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验依赖预先由外部 LiDAR 和 Cartographer SLAM 构建的地图；因此所给材料不能证明系统在完全未知环境中同时完成在线建图、语义定位和目标搜索。
- 当前提供的实验章节摘录缺少完整结果表、数值指标、重复实验设置和详细消融数据，无法独立核验任务时长、搜索准确率及 LLM 语义推理的具体增益。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Lawn Mower baseline：按规则覆盖区域的传统搜索策略，用于检验语义推理是否能比不利用目标语义和空间上下文的系统更高效。
- 传统的非语义搜索策略：论文将其作为总体对照类别，但所给原文未明确说明其是否独立于 Lawn Mower baseline，也未报告其他具体基线。
- 原文未明确报告其他基线。
- 原文未明确报告其他基线。

**实验想回答的问题**

- 与传统的非语义搜索策略相比，LLM 引导的语义搜索能否缩短无人机执行 ObjectNav 任务的任务时长，同时保持较高的目标搜索准确率？
- 该框架在仿真环境和真实环境中能否结合目标检测、三维空间定位与语义推理，完成面向指定目标的实时搜索？

**实验实现**

实验平台为 Crazyflie 2.1 纳米无人机，配备带单色相机的 AI Deck。由于载荷有限，机载平台不能搭载用于实时建图的 LiDAR，因此仿真和真实环境均先由外部 LiDAR 采集点云，并使用 Cartographer SLAM 建立地图。飞行过程中，相机图像通过 YOLO11 进行目标检测，检测到的物体再通过 OctoMap 的射线投射方法与地图进行空间定位。OpenAI 的 o3-mini 大语言模型根据用户自然语言指令、已检测物体及空间上下文进行语义推理，确定下一步动作并解释相关目标；无人机随后围绕相关物体执行细致搜索，直到找到指定目标。原文所给摘录未明确报告每个场景的重复次数、随机种子、统计显著性、硬件计算延迟或完整评价协议。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| LLM 语义引导搜索相对于 Lawn Mower 搜索的对照 | 论文报告了 LLM-guided search 与 Lawn Mower baseline 的性能比较，但所给摘录未提供可核实的逐项数值或完整表格行。 | 这项对照近似检验语义规划整体是否有效，而不是严格的单模块消融，因为两种系统可能在规划策略、访问顺序和动作执行方式上同时不同。因此即使语义引导方法更快，也不能把全部改进唯一归因于 LLM。 | Table I<br><span class="experiment-evidence">Performance Comparison Between LLM-Guided Search and Lawn Mower Baseline Across Three Scenarios</span> |

**定性案例**

- 图 5 描述了一个代表性流程：无人机接收自然语言指令后进行 360 度扫描，检测周围物体；LLM 结合物体和空间信息判断下一个动作，并对语义相关物体生成解释；随后无人机围绕该物体执行细致搜索，直到找到指定目标。该案例直观展示了系统如何把语言目标转化为带空间依据的搜索顺序，但它是流程性定性示例，不能替代多场景统计评估。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It develops an LLM-guided semantic reasoning and real-time navigation framework for UAV object-goal search.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`d58fce02f2da0229d6e732a96acd2fdc9539b5c1c617c8222e0d9af74e7a056d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
