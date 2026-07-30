---
title: "[论文解读] VEGA: Learning Navigation VLAs from In-the-Wild Egocentric Video with Geometric Trajectory Supervision"
description: "[arXiv 2606.18426][机器人 / 具身智能] VEGA将无动作标签的第一视角视频转化为带多模态目标和避障轨迹的几何监督数据，以低成本训练兼具语义目标理解与近距离避障能力的导航视觉—语言—动作模型。"
arxiv_id: "2606.18426"
announcement_date: "2026-07-30"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:25.131190+00:00"
source_sha256: "2127afbf2109d822dfc7014c325af5424e530cae80eb0886140b016166acde3e"
tags:
  - "机器人 / 具身智能"
  - "视觉—语言—动作模型"
  - "移动机器人导航"
  - "第一视角视频"
  - "几何轨迹监督"
  - "单目三维重建"
  - "流匹配"
  - "障碍物避让"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2606.18426</p>

# VEGA: Learning Navigation VLAs from In-the-Wild Egocentric Video with Geometric Trajectory Supervision

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Gershom Seneviratne, Yohan Abeysinghe, Jianyu An, Vaibhav Shende, Rahul Kumar, Dinesh Manocha</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2606.18426v2) · [PDF 下载](https://arxiv.org/pdf/2606.18426v2) · **关键词** 视觉—语言—动作模型, 移动机器人导航, 第一视角视频, 几何轨迹监督, 单目三维重建, 流匹配, 障碍物避让  


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

VEGA将无动作标签的第一视角视频转化为带多模态目标和避障轨迹的几何监督数据，以低成本训练兼具语义目标理解与近距离避障能力的导航视觉—语言—动作模型。

**不用术语来说**：互联网上有大量人行走时拍摄的第一视角视频，它们展示了真实环境中的门、家具、行人和狭窄通道，却没有告诉机器人“要去哪里”以及“应该怎样安全地走过去”。一段视频通常也只记录实际走过的一条路线，无法说明面对同一场景中的其他目标时应如何绕开障碍。因此，关键问题是如何从这些没有机器人操作记录的视频中自动生成大量可靠的目标—路径训练样本。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出VEGA训练范式：从单目第一视角视频估计局部三维几何，为语言、图像区域或空间航点目标生成考虑障碍物与安全间距的轨迹分布，再用这些轨迹监督流匹配导航VLA；几何信息仅用于训练，部署时策略只需当前RGB图像和目标。
- 构建约含500万条目标条件轨迹及25万场景的多模态数据与VEGA-Bench，使模型能够在统一几何参照下接受和评估目标推进、碰撞率与障碍物间距。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究面向地面移动机器人的视觉—语言—动作导航：策略根据当前第一视角 RGB 图像与目标描述，直接生成机器人局部坐标系中的未来运动轨迹。该方向希望利用预训练视觉语言模型的语义知识，使机器人理解文本、图像区域或空间航点等不同形式的目标；但与机器人操作领域相比，通用导航缺少覆盖室内外杂乱环境、近距离障碍和多样目标的大规模示范。网络第一视角视频虽包含丰富的场景布局、可通行性线索与自然运动，却没有机器人动作、明确目标及与机器人动作空间对齐的安全轨迹，因此不能直接用于策略监督。VEGA所依赖的关键背景是：利用单目几何模型从视频帧恢复局部三维结构，再以几何规划产生避障轨迹，并用流匹配学习可能具有多种解的轨迹分布。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**视觉—语言—动作模型（Vision-Language-Action, VLA）**

VLA将视觉观察和语言或其他目标条件映射为机器人动作，并借助视觉语言预训练获得物体与场景的语义理解能力。在本文中，动作不是单步控制量，而是机器人局部坐标系内的一段未来路径。

</div>
<div class="conceptitem" markdown="1">

**流匹配（Flow Matching）**

流匹配学习一个随时间变化的向量场，把高斯噪声逐渐变换成目标轨迹样本。它能够表示同一目标下的多种合理路径，例如从障碍物左侧或右侧绕行，而不是被迫输出一条平均轨迹。

</div>
<div class="conceptitem" markdown="1">

**单目几何重建（Monocular Geometry Reconstruction）**

单目几何模型从普通 RGB 图像估计每个像素对应的三维点，从而近似恢复相机附近的空间结构。本文据此判断自由空间、障碍位置及轨迹净空，但几何信息仅用于训练监督，部署时策略只需视觉观察和目标。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定野外采集、无动作标签的第一视角导航视频，训练阶段首先从单目 RGB 帧估计局部三维点图，并据此构造可用于避障规划的场景几何；随后从场景中采样文本目标、图像区域目标或空间航点目标，为每个目标生成位于机器人局部坐标系中的障碍感知轨迹分布，并以这些合成轨迹监督导航 VLA。学习到的策略以当前 RGB 观察 I_t 和目标 g 为输入，输出长度由预测时域 H 决定的动作块或局部轨迹 \mathbf{a}_{t:t+H}。问题假设单目模型能够提供足以支持局部规划的近似尺度化三维结构；推理时不再使用地图、距离场或在线轨迹优化，而是从噪声出发积分所学向量场，直接生成目标条件轨迹。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$I_t$**

时刻 t 的 RGB 视觉观察；其图像尺寸可写为 I_t\in\mathbb{R}^{H\times W\times 3}。

</div>
<div class="notationitem" markdown="1">

**$g$**

导航目标条件，可表示为语言描述、图像中的目标区域或空间航点。

</div>
<div class="notationitem" markdown="1">

**$\pi_\theta(\mathbf{a}_{t:t+H}\mid I_t,g)$**

参数为 \theta 的导航 VLA；在观察 I_t 和目标 g 条件下，预测从 t 到 t+H 的动作块或局部轨迹。

</div>
<div class="notationitem" markdown="1">

**$P_t(u,v)=[X\;Y\;Z]^T$**

单目几何模型估计的稠密点图中，像素 (u,v) 在相机坐标系内对应的三维点。

</div>

</div>

**直接相关的工作**

- **现有目标条件机器人导航数据集**: 这类数据集支持社会导航、视觉目标到达或跨机器人形态学习，但一条记录轨迹通常只对应一个隐式或显式目的地，无法为同一场景中的大量语义目标及不同绕障方式提供稠密监督。原文仅以文献编号 [16, 31, 21] 引用，所给节选未提供具体论文名称。
- **经典几何导航与规划系统**: 经典方法可显式利用地图、自由空间、障碍物净空和轨迹可行性产生安全行为，但部署时通常需要在线建图、距离场或轨迹优化，也不自然具备 VLA 的开放词汇语义推理能力。VEGA试图在训练阶段用几何规划生成监督，再把这种安全性蒸馏到纯视觉策略中；原文对应引用为 [36, 14]。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

通用地面移动机器人需要在室内外杂乱环境中理解开放词汇目标，并安全绕过近距离障碍物，但导航领域缺少像机器人操作领域那样规模大、环境多样且目标密集的示范数据。若依靠人工遥操作采集，数据覆盖必须同时扩展到不同环境、目标、起点、障碍布局和可行路径，成本难以承受；而直接利用海量第一视角视频又受到无动作、无显式目标和无机器人坐标系轨迹的限制。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **机器人导航示范与自动驾驶数据**：通过遥操作或既有平台记录视觉观测及运动轨迹，用于社会导航、视觉目标到达或跨机器人本体策略学习；自动驾驶数据则从结构化道路场景提供大规模行驶样本。
- **基于显式几何的经典导航系统**：在部署时构建地图或自由空间表示，并借助距离场、障碍物间距约束和轨迹优化计算可通行路径，因此能够直接检查碰撞风险与轨迹可行性。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有导航示范通常让一条记录轨迹对应一个隐式或指定目的地，无法为同一场景中的人物、门口、家具、物体和中间视点提供密集的目标条件路径；自动驾驶数据又偏向结构化道路，不能充分覆盖通用移动机器人面对的室内外杂乱场景与近距离避障。其后果是策略可能学习与目标无关的捷径或主导行走模式，出现目标落地不准、贴障行驶或碰撞。
- 经典规划虽然具有几何安全性，但通常在运行时依赖在线建图、距离场或轨迹优化，而且不自然具备VLA从视觉—语言预训练中获得的开放词汇语义推理能力；反过来，普通VLA若缺少密集几何监督，又难以学会随目标、障碍和自由空间变化而调整路径。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法尚不能以可扩展方式，把无标签、无动作的野外第一视角视频转化为机器人坐标系中的密集监督：每个场景需要对应多个语言、图像或空间目标，并为每个目标提供满足可通行性、避碰和安全间距要求的轨迹，同时还应让训练后的策略在部署时不再依赖显式几何规划。

</div>
<div markdown="1"><span>核心问题</span>

能否仅在训练阶段从单目第一视角视频恢复局部场景几何，并据此自动生成多目标、避障的轨迹分布，从而训练一个在推理阶段只接收RGB观测与目标、却仍能兼顾目标推进和几何安全的导航VLA？

</div>
<div markdown="1"><span>作者直觉</span>

第一视角视频虽然没有机器人动作标签，却已经包含地面、障碍物、通道和人类穿行方式等视觉线索。若先把这些线索恢复成局部三维结构，就可以在同一场景内人为指定许多目标，并像经典规划器一样为每个目标计算安全路径；随后让VLA模仿这些路径，相当于把规划器的避障知识“蒸馏”进视觉策略。这样既利用了互联网视频的规模与多样性，又把昂贵的几何计算留在离线训练阶段。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

VEGA把无标签第一视角网络视频转化为可训练导航策略的几何监督。对每个采样RGB帧，系统先用单目几何模型恢复带尺度的局部三维点图，经地面校准、障碍物筛选、可见性射线追踪和栅格化构造鸟瞰占据图及欧氏符号距离场（ESDF）；随后从检测到的物体生成对齐的文本、图像区域和二维航点目标，并额外在已知自由空间采样航点。MPPI规划器利用ESDF与非完整机器人动力学，为每个目标产生兼顾到达、避碰、间距、控制代价和平滑性的局部轨迹，最终形成“图像—目标—目标模态—轨迹”训练元组。VEGA再以这些轨迹监督基于π₀.₅改造的多模态VLA，通过流匹配学习局部二维航点块；几何地图和规划器只参与数据生成与训练监督，推理时策略直接根据当前视觉观察和目标生成轨迹。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 视频采样与局部几何恢复

按固定帧率均匀采样视频，将每个RGB帧 I_t 视为一个独立局部场景，并用MoGe-2恢复相机坐标系下的稠密度量点图 P_t。通过RANSAC拟合局部地面，将点图旋转到以地面为xy平面、z轴向上的机器人局部坐标系。

<div class="method-step__io" markdown="1">

**输入**：无标签的步行游览、骑行等第一视角导航视频。  
**输出**：经过地面校准、具有近似度量尺度的局部三维点图。

</div>

**直观理解**：这一步把普通单目视频帧转换成机器人可使用的局部三维形状，并把倾斜的相机视角“扶正”，使后续路径可以在地面平面上规划。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 可见性感知的BEV与ESDF构建

按高度区间筛选障碍点并投影、栅格化为鸟瞰占据图；同时沿组织化点图进行射线追踪，将栅格划分为已知自由、已占据和未观测区域。系统据此计算ESDF，使自由区域取到最近观测障碍的正距离，而占据和未知区域取到最近已知自由单元的负距离。

<div class="method-step__io" markdown="1">

**输入**：校准后的三维点图以及机器人周围的局部鸟瞰区域 Ω_{\mathrm{BEV}}。  
**输出**：可见性感知的BEV占据表示及局部ESDF几何代价图。

</div>

**直观理解**：ESDF不仅说明哪里能走，还说明安全位置离障碍有多远；把未知区域也视为负值，可避免规划器把相机没看见的空间误当成通路。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多模态目标锚定

使用Florence-2检测物体标签与边界框，再查询边界框对应的三维点并投影到机器人地面坐标系，得到与文本标签、图像区域对齐的二维航点。系统还从已观测自由空间中采样辅助航点，以覆盖不对应具体物体的任意可通行目标。

<div class="method-step__io" markdown="1">

**输入**：RGB帧、MoGe-2点图和已知自由空间集合。  
**输出**：对齐的目标三元组 (g_j^{\mathrm{text}},g_j^{\mathrm{box}},g_j^{\mathrm{wp}})，以及额外的自由空间航点目标。

</div>

**直观理解**：同一个目标既可以被说成物体名称，也可以在图像中被框出，还可以写成机器人坐标中的位置；这种对齐让单一策略能够理解三种目标输入。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于MPPI的几何轨迹标注

MPPI在机器人动力学下滚动生成候选轨迹，并综合目标接近、碰撞、障碍间距、控制努力和平滑性进行评分，选取代价最低的无碰轨迹。若目标在局部地图内无法到达，则保留能够安全推进并缩短目标距离的最佳部分轨迹。

<div class="method-step__io" markdown="1">

**输入**：每个二维航点目标、局部ESDF和非完整机器人运动模型。  
**输出**：每个目标对应的参考航点轨迹，以及训练集合 \mathcal{D}_t=\{(I_t,g_j,m_j,\hat{\mathbf y}_{t:t+H,j})\}_{j=1}^{K_t}。

</div>

**直观理解**：这相当于先让一个能查看几何地图的规划器充当“教师”，为同一画面中的不同目标画出安全路线，而不要求原视频拍摄者真实走过这些路线。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 可见性感知欧氏符号距离场

$$
\mathrm{ESDF}(x,y)=\begin{cases}+d_{\mathrm{obs}}(x,y),&(x,y)\in\mathcal{X}_{\mathrm{free}},\\-d_{\mathrm{free}}(x,y),&(x,y)\in\mathcal{X}_{\mathrm{occ}}\cup\mathcal{X}_{\mathrm{unk}}.\end{cases}
$$

**符号说明**

- $(x,y)$：机器人局部鸟瞰平面中的栅格位置。
- $\mathcal{X}_{\mathrm{free}}$：经可见性判断确认的已知自由空间集合。
- $\mathcal{X}_{\mathrm{occ}}$：由三维障碍点投影得到的已占据空间集合。
- $\mathcal{X}_{\mathrm{unk}}$：当前相机观察未覆盖的未知空间集合。
- $d_{\mathrm{obs}}(x,y)$：位置 (x,y) 到最近已观测障碍栅格的欧氏距离。
- $d_{\mathrm{free}}(x,y)$：位置 (x,y) 到最近已知自由栅格的欧氏距离。

<div class="equation-explanation" markdown="1">

**直观理解**：正值表示当前位置已知可通行，数值越大通常意味着离障碍越远；负值表示位置被占据或尚未观察，规划器应避开。该定义使MPPI能用同一张连续代价图同时检查碰撞和衡量安全间距。  
**原文位置**：式(6)，第4.1.1节 Geometry Recovery and Visibility-Aware ESDF Construction

</div>

</div>

<div class="equation-block" markdown="1">

#### 目标轨迹的条件流匹配损失

$$
\mathcal{L}_{\mathrm{FM}}(\theta)=\mathbb{E}\left[\left\|v_{\theta}(\mathbf{y}_{\tau},\tau,I_t,g)-(\mathbf{y}_1-\mathbf{y}_0)\right\|_2^2\right],\quad \mathbf{y}_{\tau}=(1-\tau)\mathbf{y}_0+\tau\mathbf{y}_1,\quad \mathbf{y}_0\sim\mathcal N(0,\mathbf I),\quad \tau\in[0,1]
$$

**符号说明**

- $\theta$：待优化的流匹配轨迹模型参数。
- $\mathbf y_1$：MPPI生成的目标航点轨迹样本。
- $\mathbf y_0$：与目标轨迹同维、从标准高斯分布采样的初始噪声。
- $\tau$：从噪声状态0到数据状态1的连续插值时间。
- $\mathbf y_\tau$：噪声轨迹与目标轨迹在时间 τ 的线性插值状态。
- $v_\theta(\mathbf y_\tau,\tau,I_t,g)$：在图像观察 I_t 和目标 g 条件下，模型对插值状态变化方向的预测向量场。
- $\mathbf y_1-\mathbf y_0$：线性插值路径对应的真实恒定速度方向。
- $\mathbb E$：对训练轨迹、噪声和插值时间采样求期望。

<div class="equation-explanation" markdown="1">

**直观理解**：训练随机取一条教师轨迹和一份噪声，在两者之间选取中间状态，要求模型预测把噪声推向教师轨迹的正确方向。学会这一向量场后，推理阶段可从随机噪声逐步积分到一条符合当前图像与目标的导航轨迹，因此能够表示同一任务的多种可行路径。  
**原文位置**：式(2)与式(3)，第3.2节 Flow Matching for Trajectory Prediction；用于第4.2节的航点动作专家

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：优化目标是最小化条件流匹配损失 \mathcal L_{\mathrm{FM}}(\theta)：把MPPI依据训练期几何生成的航点轨迹作为目标分布样本，回归从高斯噪声到这些轨迹的条件向量场。图像 I_t 与目标 g 共同限定应生成哪一类轨迹，因此优化不仅学习一般运动形状，也将目标趋近、避碰和障碍间距等规划偏好从MPPI轨迹蒸馏进视觉策略；原文节选未给出额外辅助损失或各MPPI代价项的具体权重。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 可见性感知ESDF几何监督模块**

该模块由MoGe-2单目度量点图、RANSAC地面拟合、障碍高度过滤、BEV栅格化和射线追踪组成。它显式区分 \mathcal X_{\mathrm{free}}、\mathcal X_{\mathrm{occ}} 与 \mathcal X_{\mathrm{unk}}，并把未知空间与障碍空间一并设为负ESDF区域。

> 直观理解：单纯深度图难以直接告诉规划器路径是否安全；ESDF把三维观察压缩成地面上的“安全余量地图”，既支持碰撞判断，也能鼓励轨迹与障碍保持距离。

**2. 多模态目标锚定与MPPI轨迹教师**

Florence-2提供物体语义和图像框，MoGe-2提供框内像素对应的三维位置，从而建立文本、图像区域与机器人坐标航点之间的对齐。MPPI随后在非完整动力学约束下，利用目标、碰撞、间距、控制和平滑代价生成每个目标的无碰参考轨迹。

> 直观理解：网络视频原本没有机器人目标和动作标签；该模块自动提出“去哪里”的问题，再用几何规划器生成“怎样安全过去”的答案，从而将无标签视频变成监督数据。

**3. 多模态条件流匹配VLA**

模型基于π₀.₅，将预训练视觉语言骨干与流匹配航点动作专家结合；语言编码器、冻结视觉编码器和可训练航点编码器分别支持文本、图像和空间航点目标。条件token通过前缀上下文输入动作专家，使其预测局部二维航点分布而非单条确定轨迹。

> 直观理解：流匹配允许模型保留导航的多解性，例如同一障碍可以从两侧绕行；多种目标编码器则保证用户无论用文字、图片还是坐标指定目标，都能调用同一个策略。

**训练与推理**

训练数据生成阶段：采样视频帧，恢复并校准单目几何，建立区分自由、占据和未知空间的ESDF；检测物体并对齐文本、图像框和二维航点，同时采样自由空间航点；随后为每个目标运行MPPI，得到完整无碰轨迹或安全推进的最佳部分轨迹。模型训练阶段：根据目标模态分别编码文本、图像区域或航点，将其与当前RGB视觉上下文输入流匹配动作专家；采样教师轨迹 \mathbf y_1、噪声 \mathbf y_0 和时间 τ，构造 \mathbf y_τ 并最小化向量场均方误差。推理阶段：仅输入当前RGB观察和指定目标，从标准高斯噪声初始化轨迹，将条件向量场从 τ=0 数值积分至 τ=1，输出机器人局部坐标系中的 H 个二维航点；训练时使用的MoGe-2、ESDF和MPPI不进入策略推理流程。

**复现信息**

复现方法所需的关键组件包括：MoGe-2用于单帧度量点图恢复，RANSAC用于地面拟合，障碍高度过滤与射线追踪用于构造可见性感知BEV/ESDF，Florence-2用于物体标签和边界框提取，MPPI用于非完整动力学下的目标条件轨迹生成。策略采用π₀.₅式预训练视觉语言骨干和流匹配动作专家，并参考OmniVLA的多目标模态设计：视觉编码器冻结，航点目标编码器可训练，输出维度为 H×2。固定视频采样帧率、BEV范围与分辨率、高度阈值 z_{\min},z_{\max}、MPPI采样配置及各代价权重在所给正文节选中均未明确报告，作者指向附录8.2和8.3提供进一步细节。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- VEGA-Bench：作者构建的导航VLA基准，包含25万场景以及约500万个导航目标，并为目标配套场景几何信息。其作用是大规模、可重复地评估目标推进、碰撞避免和障碍物净空；当前节选未明确报告训练/验证/测试划分。
- 真实世界导航试验：用于检验仿真式基准上的改进能否迁移到物理环境。图3展示了三个包含静态与动态障碍物的导航场景，但当前节选未明确报告完整试验规模、场地构成、机器人平台、目标距离阈值或重复次数。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**目标到达能力**

VEGA-Bench采用平均归一化目标进展，即机器人到目标距离的减少量除以初始距离；真实世界采用成功率，即最终停在目标规定距离阈值内的试验比例。两种指标分别衡量轨迹是否朝目标有效推进，以及物理试验是否真正到达目标附近。 （越高越好，因为更高的归一化进展表示更接近目标，更高的成功率表示更多试验满足到达条件。）

</div>
<div class="metricitem" markdown="1">

**碰撞率**

在VEGA-Bench中，进入被占据、未知或越界ESDF区域的轨迹所占比例；ESDF是带符号欧氏距离场，用于表示位置与最近障碍物的距离。在真实世界中，该指标统计发生物理接触或触发安全干预的试验比例。 （越低越好，因为它直接反映策略进入危险区域或需要人工/系统介入的频率。）

</div>
<div class="metricitem" markdown="1">

**障碍物净空**

对未碰撞轨迹，计算沿途到最近障碍物的最小距离，再在轨迹间取平均。它区分了“恰好没有碰撞”和“留有稳定安全余量”两类行为。 （越高越好，因为更大的最小距离通常意味着轨迹对定位误差、控制误差及障碍物运动具有更大安全裕度。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### VEGA-Bench：与最强基线比较碰撞避免能力

<div class="result-value" markdown="1">

作者报告VEGA在保持具有竞争力的目标进展时，将碰撞率相对最强基线降低33.0%。

</div>

这说明VEGA生成的轨迹更少进入占据、未知或越界区域，支持几何监督有助于学习避障行为。但该相对降幅不能单独说明绝对碰撞率，也不能证明所有场景类型上均有相同收益；当前节选还未给出方差或显著性检验。

<div class="result-source" markdown="1">

来源：摘要；当前节选未提供对应结果表编号

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Our evaluation shows that VEGA achieves competitive goal progress while reducing collisions by 33.0% and improving obstacle clearance by 17.9% over the strongest baseline on VEGABench, while improving success by at least 150.0%, reducing collisions by at least 66.7%, and improving obstacle clearance by at least 60.0% in real-world trials.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### VEGA-Bench：与最强基线比较非碰撞轨迹的障碍物净空

<div class="result-value" markdown="1">

作者报告VEGA的平均障碍物净空相对最强基线提高17.9%。

</div>

该结果表明VEGA不仅减少了明确碰撞，还倾向于让成功避碰的轨迹与障碍物保持更大最小距离，即具有更宽的安全余量。不过净空只在未碰撞轨迹上计算，可能受到各方法非碰撞样本集合不同的影响；它也不等价于路径更短或到达更快。

<div class="result-source" markdown="1">

来源：摘要；当前节选未提供对应结果表编号

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Our evaluation shows that VEGA achieves competitive goal progress while reducing collisions by 33.0% and improving obstacle clearance by 17.9% over the strongest baseline on VEGABench, while improving success by at least 150.0%, reducing collisions by at least 66.7%, and improving obstacle clearance by at least 60.0% in real-world trials.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 真实世界导航试验：目标到达、碰撞和安全净空的综合比较

<div class="result-value" markdown="1">

作者报告，相对所比较基线，VEGA的成功率至少提高150.0%，碰撞率至少降低66.7%，障碍物净空至少提高60.0%。

</div>

三个方向一致的改进表明，从视频几何中生成的轨迹监督可能迁移到物理机器人，并同时改善到达能力与安全性。“至少”意味着不同基线间的提升幅度可能不同。然而这些是相对变化；在缺少绝对计数、试验次数、置信区间和场景分布的情况下，不能据此判断实际失败概率，也不能排除小样本导致百分比变化较大的可能。

<div class="result-source" markdown="1">

来源：摘要；当前节选未提供对应结果表编号

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Our evaluation shows that VEGA achieves competitive goal progress while reducing collisions by 33.0% and improving obstacle clearance by 17.9% over the strongest baseline on VEGABench, while improving success by at least 150.0%, reducing collisions by at least 66.7%, and improving obstacle clearance by at least 60.0% in real-world trials.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前提供的实验节选没有消融实验，因而无法独立判断性能提升究竟来自视频规模、单目几何重建、目标采样、障碍感知轨迹生成，还是流匹配策略训练；也无法评估几何估计误差对策略的敏感性。
- 当前节选仅给出相对提升，未给出主要结果的绝对分数、样本数、误差条、置信区间或显著性检验；真实试验的机器人平台、环境覆盖、成功阈值和安全干预规则也未完整说明，因此结果的统计稳定性与跨平台泛化范围仍需核查原文。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- OmniVLA：作者称其为当前先进的导航VLA之一，因此用于比较VEGA与专门面向导航任务的视觉—语言—动作策略。
- NaVILA：另一种先进导航VLA，用于判断VEGA的几何轨迹监督是否优于已有导航VLA训练路线。
- π_{0.5}：能够执行移动操作的通用VLA。评测使用其底盘线速度和角速度输出生成导航轨迹，因而检验专门学习的VEGA相对于通用具身策略的优势。

**实验想回答的问题**

- 在统一的导航评测中，相比专用导航VLA与通用移动操作VLA，VEGA能否在保持目标推进能力的同时，减少碰撞并提高与障碍物的安全间距？
- 由互联网第一视角视频重建出的几何轨迹监督，能否迁移到真实机器人导航，使策略在静态和动态障碍场景中更可靠地到达目标？

**实验实现**

评测将VEGA与OmniVLA、NaVILA和π_{0.5}比较；对π_{0.5}使用其线速度与角速度控制底盘并形成导航轨迹。VEGA-Bench中的碰撞依据轨迹是否进入占据、未知或越界的ESDF区域判定；真实试验则以物理接触或安全干预判定。图3以黄色星形标出目标，以勾号表示成功到达，以X表示碰撞或失败。当前节选未明确报告各模型检查点、输入分辨率、推理频率、轨迹执行时域、成功距离阈值、统计置信区间及显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 图3定性比较三个含静态与动态障碍物的真实导航场景：目标由黄色星形标出。作者描述VEGA均能避开障碍并到达目标，而基线VLA会出现碰撞、提前停止或轨迹未到达目标。该图直观展示了失败模式，但只有三个案例，属于说明性证据，不能替代完整定量统计。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：利用野外第一视角视频重建几何并生成轨迹监督，以训练具备避障规划能力的导航 VLA 机器人策略。; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`2127afbf2109d822dfc7014c325af5424e530cae80eb0886140b016166acde3e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
