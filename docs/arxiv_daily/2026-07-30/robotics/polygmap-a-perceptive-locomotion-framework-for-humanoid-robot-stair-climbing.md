---
title: "[论文解读] PolygMap: A Perceptive Locomotion Framework for Humanoid Robot Stair Climbing"
description: "[arXiv 2510.12346][机器人 / 具身智能] 原文未明确报告。"
arxiv_id: "2510.12346"
announcement_date: "2026-07-30"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T07:32:04.512622+00:00"
source_sha256: "386689b77a2c4af0cf295f2d504639ff270ba787cdf044739b6836f818ae7d59"
tags:
  - "机器人 / 具身智能"
  - "人形机器人"
  - "楼梯攀爬"
  - "感知运动"
  - "多边形平面地图"
  - "多传感器融合"
  - "足步规划"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2510.12346</p>

# PolygMap: A Perceptive Locomotion Framework for Humanoid Robot Stair Climbing

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Bingquan Li, Ning Wang, Zhicheng He, Yucong Wu, Tianwei Zhang</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2510.12346v2) · [PDF 下载](https://arxiv.org/pdf/2510.12346v2) · **关键词** 人形机器人, 楼梯攀爬, 感知运动, 多边形平面地图, 多传感器融合, 足步规划  


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

原文未明确报告。

**不用术语来说**：原文未明确报告。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 原文未明确报告。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于人形机器人的感知运动（perceptive locomotion）研究：机器人在落脚前利用环境感知识别可通行表面，并将几何约束直接用于足步规划和全身运动生成。楼梯相较平地具有踏面狭窄、相邻台阶存在高度差且跌落风险高等特点，因此系统不仅要维持动态平衡，还要可靠估计踏面、台阶边缘与障碍物，在机载算力限制下持续输出安全落脚区域。本文聚焦的核心表示是具有明确边界的多边形楼梯平面地图；与稠密栅格或高程地图相比，该表示更便于直接约束脚掌是否完整落在可通行区域内。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**感知运动（Perceptive Locomotion）**

指机器人把传感器观测到的地形几何直接纳入落脚点和身体运动规划，而不是主要依靠接触后的平衡调节来补偿地形变化。其目标是在脚掌接触地面前预判可行区域和风险。

</div>
<div class="conceptitem" markdown="1">

**平面语义地图（Plane Semantic Map）**

将环境表示为带有类别或通行含义的有限平面区域，例如把每一级楼梯踏面表示成具有高度、朝向和多边形边界的可落脚区域。这里的“语义”主要体现为区分可通行踏面、边缘及障碍，而非仅保存无结构点云。

</div>
<div class="conceptitem" markdown="1">

**多传感器融合与里程计**

多传感器融合联合使用 LiDAR、RGB-D 相机、IMU 及机器人运动学信息，以互补不同传感器在纹理、光照、振动和测距方面的缺陷。里程计用于估计机器人随时间变化的位姿，使不同帧观测能够变换到统一坐标系并累积成地图。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务是在未知的室内或室外真实楼梯环境中，为行走中的人形机器人在线生成可执行的上楼运动。系统输入包括 LiDAR 与 RGB-D 相机采集的点云、IMU 测量，以及可由关节状态和机器人模型获得的前向运动学信息；这些观测可能受到低纹理、黑色吸光材料、视角变化、机体振动、滚动快门、数据丢失和状态估计漂移的影响。系统需要先定位机器人并融合多帧观测，再提取具有稳定边界的楼梯踏面多边形，从中选择满足稳定性与安全约束的落脚区域，最终实时输出足步及全身运动规划。问题设定隐含楼梯踏面可近似为局部平面，且机载 NVIDIA Orin 必须承担实时感知—规划闭环；摘要报告全身运动规划输出频率为 20–30 Hz，但所给章节没有进一步明确地图坐标系、机器人状态向量或安全裕量的形式化定义。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$\mathcal{P}_{L}$**

LiDAR 点云；原文仅以 LiDAR point clouds/PCD 描述输入，未明确给出该数学符号。

</div>
<div class="notationitem" markdown="1">

**$\mathcal{P}_{D}$**

RGB-D 相机产生的深度点云；原文未明确给出该数学符号。

</div>
<div class="notationitem" markdown="1">

**$\mathbf{T}$**

机器人或传感器在地图坐标系中的位姿变换，用于多帧点云配准；原文提到视觉里程计和精确定位，但未明确规定符号及坐标系。

</div>
<div class="notationitem" markdown="1">

**$\Pi_i$**

第 i 个具有多边形边界的楼梯平面或可落脚踏面；这是对文中“polygonal plane segments”的便于理解的记号，原文未给出正式符号。

</div>

</div>

**直接相关的工作**

- **基于三维多边形地图的 RRT 足步搜索方法 [11]**: 该工作同样使用多边形环境表示来搜索人形机器人足步，说明有界平面可直接服务于落脚规划；但原文指出，基于 RRT 的搜索在机载系统中面临实时效率问题。PolygMap因而强调实时楼梯平面建图以及与在线足步、全身运动生成的紧密衔接。
- **融合平面区域测量与运动学—惯性状态估计的地形建图方法 [14]**: 该方向通过状态估计提高平面地图的时空一致性，与本文处理机体运动和多帧融合误差的需求直接相关。PolygMap进一步面向楼梯，将 LiDAR 定位、RGB-D 平面提取和安全落脚区域生成组合为完整的人形机器人上楼框架。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

人形机器人要进入楼宇巡检、应急响应和工业协作等真实场景，必须可靠攀爬楼梯。与平地行走相比，楼梯具有台阶高度差、落脚面狭窄和跌落风险高等特点；机器人不仅要保持身体平衡，还要在脚接触前识别可踩踏平面、台阶边缘与障碍物，并把感知结果及时转化为安全落脚点。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **依赖平衡控制与高带宽跟踪稳定器的方法**：通过快速调节全身姿态和关节运动，在脚部接触楼梯后抵消几何扰动，主要依靠控制器的动态稳定能力完成攀爬。
- **基于感知的楼梯平面提取与建图方法**：利用深度或点云观测拟合台阶平面，并通过里程计进行多帧融合，从而为落脚规划提供楼梯几何信息。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 仅依赖姿态调节的方法没有显式表示环境几何和可落脚区域，容易产生过度保守的步态与较大的落脚不确定性，因此难以在长楼梯、光照变化或踏面退化时持续可靠攀爬。
- 现有感知流程在楼梯场景中容易失稳：狭小踏面和尖锐边缘，加上低纹理、黑色吸光材料、视角变化、机身振动及滚动快门，会造成深度噪声、数据缺失、法向估计不稳定和过度分割；同时，里程计漂移会在多帧融合中累积，破坏台阶边界与可通行区域的时空一致性。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种能够同时应对感知噪声、状态估计不确定性和实时计算约束的楼梯表示：它既要稳定、低漂移地给出适应楼梯形状的可通行区域，又要采用便于控制器快速使用的形式，从而将环境感知有效连接到全身运动生成。

</div>
<div markdown="1"><span>核心问题</span>

如何融合LiDAR、RGB-D相机、IMU及机器人本体状态，实时构建稳定的多边形楼梯平面语义地图，并基于这些多边形安全区域生成满足稳定性与安全约束的落脚点和足端轨迹？

</div>
<div markdown="1"><span>作者直觉</span>

与其让机器人在踩到台阶后再靠强力平衡控制补救，不如先把传感器观测整合成明确的多边形踏面：LiDAR和状态估计提供较稳定的定位基础，RGB-D点云补充台阶表面细节，多边形则直接描述脚可以放置的范围。规划器据此避开边缘并选择安全区域，可减少落脚的不确定性；这种紧凑几何表示也比直接处理大量原始点云更适合实时接入全身运动规划。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PolygMap 是一条从多传感器观测到全身运动指令的在线感知—规划流水线。输入包括向下 RGB-D 相机的深度图、LiDAR—IMU 里程计（LIO）、关节编码器、IMU 姿态与足底接触状态；系统先融合运动学状态和 Point-LIO 位姿，得到平滑且低漂移的机器人基座位姿。随后，它直接在深度图上计算表面法向量，经各向异性扩散、Canny 轮廓提取和 RANSAC 平面拟合，将楼梯压缩成带空间位姿的多边形平面语义地图。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多传感器机器人状态估计

线性卡尔曼滤波器以基座位置、速度和八个接触点位置构成 30 维状态，通过前向运动学约束更新身体状态；再利用预标定的 LiDAR—基座外参，将 LIO 位姿转换到机器人质心，并以互补滤波融合位置和旋转。

<div class="method-step__io" markdown="1">

**输入**：IMU 测得的加速度与姿态、关节编码器、八个足部接触点的接触状态，以及 Point-LIO 输出的 LiDAR 位姿。  
**输出**：世界坐标系下平滑、低漂移的机器人基座位姿与速度，供地图构建、落脚点生成和步态规划共同使用。

</div>

**直观理解**：关节与足部接触信息在短时间内较平滑，但会逐渐漂移；LiDAR 能提供全局校正，却可能受机器人振动影响。系统把两者组合，相当于用前者保证动作连续、用后者定期纠正位置和朝向。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 楼梯多边形平面地图构建

系统先对深度图做保边的各向异性扩散，再由相邻像素反投影点的叉积计算表面法向量；随后通过 Sobel、Canny 提取平面边界，以 RANSAC 拟合平面，并借助融合位姿把检测结果变换到统一世界坐标系。

<div class="method-step__io" markdown="1">

**输入**：RGB-D 深度图、相机内参，以及融合后的机器人位姿。  
**输出**：由楼梯踏面等平面片段构成的实时多边形语义地图，每个多边形包含边界顶点、平均高度和空间位置。

</div>

**直观理解**：系统不长期保留稠密点云，而是把每一级台阶概括成一个多边形平面。这样既保留“哪里能踩”的结构，又减少地图数据量和后续搜索成本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 安全候选区域与最优落脚点生成

每个平面先投影到水平面并计算二维凸包，再按固定网格栅格化、恢复其平均高度；系统执行基座附近范围过滤、每格最高点提取、足高阈值过滤和分层形态学腐蚀，最后按可跨越高度与水平距离选择主要及后续候选点。

<div class="method-step__io" markdown="1">

**输入**：多边形地图、机器人基座位姿、当前足底高度、搜索范围及允许跨越高度。  
**输出**：远离台阶边缘、位于机器人可达范围内并带有位置与朝向信息的结构化落脚点集合。

</div>

**直观理解**：腐蚀操作会从平面边界向内缩一圈，使候选脚印不贴近容易踩空的台阶边缘。之后优先选择满足抬脚高度条件且离机器人最近的安全位置，以降低迈步难度。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 足步序列与全身轨迹生成

系统将左右脚偏置按躯干偏航角旋转，生成各步目标脚位；摆动脚竖直方向采用正弦式抬起和落下、前进方向采用时间插值，并用旋转矩形检测当前脚与支撑脚是否重叠，同时依据局部横向位移和转向选择摆动腿。

<div class="method-step__io" markdown="1">

**输入**：估计的躯干路径、最优落脚点、左右脚相对躯干的偏置，以及步态时序参数。  
**输出**：按固定时间间隔离散的足端位置、躯干位姿和时间戳序列，供下游全身运动规划与执行。

</div>

**直观理解**：规划器不仅决定“脚踩在哪里”，还决定“脚怎样平滑地抬起、越过台阶并落下”。脚掌被近似成有方向的矩形，可在执行前排除双脚互相穿插的轨迹。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="equation-block" markdown="1">

#### 基座位置与姿态的互补融合

$$
{}^{W}\mathbf{p}_{\mathrm{base}}^{(\mathrm{fused})}=\alpha\,{}^{W}\mathbf{p}_{\mathrm{base}}+(1-\alpha)\,{}^{W}\mathbf{p}_{\mathrm{base}}^{(L)},\quad \Delta R=\log\!\left(\left({}^{W}R_{\mathrm{base},k}\right)^{\top}{}^{W}R_{\mathrm{base},k}^{(L)}\right),\quad {}^{W}R_{\mathrm{base}}^{\mathrm{fused}}={}^{W}R_{\mathrm{base},k}\exp\!\left((1-\alpha)\Delta R\right),\quad \alpha=\frac{\tau}{\tau+\Delta t}
$$

**符号说明**

- ${}^{W}\mathbf{p}_{\mathrm{base}}$：由运动学与本体感知估计的基座位置，表达在世界坐标系 W 中。
- ${}^{W}\mathbf{p}_{\mathrm{base}}^{(L)}$：由 LIO 位姿经 LiDAR—基座外参转换得到的基座位置。
- ${}^{W}R_{\mathrm{base},k}$：第 k 时刻本体状态估计给出的基座旋转矩阵。
- ${}^{W}R_{\mathrm{base},k}^{(L)}$：第 k 时刻由 LIO 转换得到的基座旋转矩阵。
- $\Delta R$：两种姿态估计之间在旋转李代数中的相对旋转误差；log 将旋转矩阵映射为可加权的局部旋转量。
- $\exp$：把加权后的局部旋转量映射回旋转矩阵的指数映射。
- $\alpha$：互补融合系数，取值范围为 [0,1]；越大越偏向本体状态估计。
- $\tau$：互补滤波时间常数。
- $\Delta t$：状态更新的时间间隔。

<div class="equation-explanation" markdown="1">

**直观理解**：位置部分对运动学估计与 LIO 校正作加权平均；姿态不能直接逐元素平均，因此先计算二者之间的旋转差，再施加其中的一个加权部分。该式在保留短时平滑性的同时利用 LIO 抑制长期漂移。  
**原文位置**：第 III-A 节，式 (6)–(9)

</div>

</div>

<div class="equation-block" markdown="1">

#### 满足高度约束的最近安全落脚点

$$
p^{*}=\underset{p\in P_{\mathrm{eroded}},\;z(p)>z_{\mathrm{foot}}+\Delta_{\mathrm{foot}}}{\arg\min}\;\left\|\left(x(p)-x_{\mathrm{base}},\;y(p)-y_{\mathrm{base}}\right)\right\|_{2}^{2}
$$

**符号说明**

- $P_{\mathrm{eroded}}$：经过范围、高度过滤及分层腐蚀后保留的安全候选点集。
- $p$：候选落脚点。
- $p^{*}$：被选中的主要落脚候选点。
- $x(p),y(p),z(p)$：候选点 p 的三维坐标分量。
- $x_{\mathrm{base}},y_{\mathrm{base}}$：机器人基座在水平面内的位置。
- $z_{\mathrm{foot}}$：由左右脚趾和脚跟变换得到的当前最小足底高度。
- $\Delta_{\mathrm{foot}}$：用于判定下一可迈上平面的足部高度差阈值。

<div class="equation-explanation" markdown="1">

**直观理解**：优化先要求候选点明显高于当前足底，从而对应要迈上的台阶，再在腐蚀后的安全区域中选择水平距离最近者。它是一条轻量的启发式选择规则，而不是求解完整的动力学最优控制问题。  
**原文位置**：第 III-B 节，式 (26)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该方法是由状态估计、几何视觉、启发式落脚点筛选和解析轨迹生成组成的在线机器人系统，原文没有给出需要离线训练的神经网络、数据驱动损失函数或训练目标；其中“最优落脚点”仅通过带高度约束的最近点规则在线选取。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 运动学—LIO 松耦合状态融合**

卡尔曼滤波状态为基座三维位置、三维速度及八个足部接触点的三维世界位置；控制量是世界系下的质心线加速度，观测包含接触点相对基座的位置、速度与高度。Point-LIO 位姿经刚体外参转换到基座后，通过互补系数分别融合平移，并在 SO(3) 的对数—指数映射上融合旋转。

> 直观理解：这是整个系统的坐标基准：若机器人自身位置估计不准，即使相机正确识别出台阶，也会把台阶放到错误位置。松耦合设计允许 LIO 与运动学估计相对独立，工程上更容易替换或调试。

**2. 深度图多边形平面提取**

像素深度通过相机内参反投影为三维点，相邻方向差分向量的归一化叉积给出局部法向量；各向异性扩散在平坦区域抑制深度噪声而保护边缘，Canny 提取轮廓，RANSAC 从含噪观测中估计楼梯平面。

> 直观理解：法向量用于区分朝向不同的表面，轮廓用于找出台阶边界，RANSAC 则避免少量错误深度把整个平面拟合带偏。三者共同把原始深度图转成适合规划的几何平面。

**3. 基于腐蚀的落脚安全区与步态规划**

多边形凸包被栅格化为结构化点集，并按高度分层执行多次形态学腐蚀，以删除孤立点、尖锐边缘及缺乏完整脚掌支撑的区域；所得候选点再接受高度、距离和朝向筛选，随后生成带碰撞检查的摆动脚轨迹。

> 直观理解：检测到一个平面并不意味着脚掌的任意部分都能安全落下，尤其是台阶边缘附近。该模块先把可踩区域缩成更保守的内部区域，再从中选择易达到的位置并规划完整迈步动作。

**训练与推理**

无训练阶段。在线运行时，Point-LIO 持续处理 Livox Mid360 与 IMU 数据，关节编码器、接触状态和 IMU 同时进入状态估计器；融合位姿用于把 RGB-D 相机检测出的楼梯平面注册到统一地图。系统随后实时更新多边形地图，栅格化并腐蚀安全区域，选择可达落脚点，生成足步与躯干协调轨迹，并将离散轨迹交给下游全身运动规划和控制执行。规划过程中若相邻双脚的旋转矩形相交，则判为轨迹冲突，需要调整输入躯干路径。

**复现信息**

硬件感知配置包括向下安装的 Intel RealSense L515 RGB-D/LiDAR 深度相机、Livox Mid360 LiDAR、IMU、关节编码器及足部接触信息；L515 可在低照度下获取深度，但原文指出其在高吸收率表面上的性能会下降。LIO 使用 Point-LIO，计算平台为 NVIDIA Orin；论文摘要声称全身运动规划输出频率为 20–30 Hz。原文节选未明确报告互补系数、扩散步长、栅格分辨率、腐蚀次数、搜索范围、足高阈值及步态时长等具体数值，因此复现时仍需核查完整论文或作者实现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- Gazebo仿真场景：共5次试验，其中3次攀爬10级楼梯、2次攀爬4级楼梯。该场景用于在较理想条件下检验完整感知—规划—控制闭环的连续运行能力、实时性、攀爬效率与落脚误差；原文未报告训练集、验证集或测试集划分。
- 室内真实楼梯：表II包含3次室内试验，分别为2次双步态（DS）和1次单步态（SS），均攀爬4级楼梯。图6所示代表性楼梯的台阶高度为13 cm、踏面宽度为28 cm，而机器人脚长为26 cm，因此主要检验狭小落脚余量下的在线感知、重新规划和执行精度。
- 室外真实楼梯：表II包含2次SS试验，分别攀爬6级和5级楼梯，用于检验地面不平、光照变化及台阶突出边缘等干扰下的实时检测与系统鲁棒性。原文只报告5次真实试验的逐次结果，没有给出重复试验统计、成功率或固定数据划分。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**连续攀爬级数**

机器人在一次试验中能够连续完成的楼梯级数，用于衡量闭环系统能否持续生成有效楼梯平面、落脚区域和全身轨迹。该指标应结合是否碰撞或失败解释，不能单独代表成功率。 （在无碰撞且保持稳定的前提下越高越好，因为更多级数意味着闭环能够维持更长时间。）

</div>
<div class="metricitem" markdown="1">

**平面检测频率**

系统每秒更新楼梯平面检测结果的次数，单位为Hz，用于判断感知是否足够及时地支持在线落脚规划；它不同于文中20–30 Hz的全身运动规划输出频率。 （通常越高越好，因为环境与机器人状态更新更及时，但频率本身不能证明检测准确。）

</div>
<div class="metricitem" markdown="1">

**最大落脚误差**

从感知和规划得到的目标落脚点到实际执行落脚位置之间的最大偏差，单位为mm；文中还通过图7分别检查足端在x、z方向上的轨迹跟踪误差。该指标直接反映从感知到执行的闭环精度及剩余安全裕量。 （越低越好，因为误差越小，脚掌越不容易越出台阶踏面或撞上突出边缘。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Gazebo完整闭环：3次10级楼梯和2次4级楼梯试验

<div class="result-value" markdown="1">

5次仿真中最长完整攀爬时间为35 s，作者据此估计每级约需3.4–3.7 s；最大落脚误差为12.4 mm。表I还显示平面检测频率为20–29 Hz，且所有试验均完成对应的4级或10级任务。

</div>

在理想仿真条件下，感知、平面建图、落脚规划和控制可以连续闭环运行，厘米级以下到约1.24 cm的最大落脚偏差相对踏面宽度较小。该结果支持系统的实时可执行性，但仿真缺少真实传感器噪声、光照变化、执行器误差和复杂接触，因此不能直接证明真实环境中的同等可靠性。

<div class="result-source" markdown="1">

来源：第IV-B节，表I（Gazebo Simulation Results）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">The results show that the most extended duration from the start of climbing until the robot reaches a stable stance is 35 s, with an average time of approximately 3.4–3.7 s per step.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 室内真实楼梯上的DS与SS攀爬

<div class="result-value" markdown="1">

两次室内DS试验均完成4级楼梯，总时间分别为9.6 s和10.2 s，最大落脚误差分别为12.1 mm和11.4 mm；室内SS完成4级仅需7.7 s，但最大误差增至24.7 mm。

</div>

DS在每次到达稳定姿态后再规划，因此速度较慢但误差更小；SS边走边规划，速度更快，却因基座观测不够稳定而产生更大误差。这揭示了真实系统中明确的速度—精度权衡，但每种条件的试验次数很少，尚不足以形成具有统计意义的优劣结论。

<div class="result-source" markdown="1">

来源：第IV-C节，表II（Real World Stair Climbing Experiment Results）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Indoor | SS | 7.7 | 4 | 23 | 24.7</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 室外真实楼梯上的连续SS攀爬

<div class="result-value" markdown="1">

两次室外试验分别完成6级和5级楼梯，检测频率为20 Hz和21 Hz，最大落脚误差分别为33.4 mm和22.2 mm；其中33.4 mm为全部真实试验中的最大值。

</div>

结果表明，在地面不平和光照变化下，平面检测仍能维持约20 Hz，并支持5–6级连续攀爬；但较大的SS落脚误差会侵蚀狭窄踏面的安全余量，文中还观察到脚尖与突出边缘碰撞。因此，这些结果说明系统具备一定室外适应性，而不是证明其已能可靠处理任意长楼梯或复杂台阶几何。

<div class="result-source" markdown="1">

来源：第IV-C节，表II与图8

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">In both scenarios, the robot successfully climbed 5–6 steps.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验规模很小：仅有5次仿真和5次真实试验，未报告成功率、失败次数的完整统计、均值方差或置信区间，也没有与其他完整感知式楼梯攀爬系统进行量化比较。因此，现有结果能支持原型系统可行性，但不足以证明普遍优越性或长期可靠性。
- 室外长楼梯尤其是SS仍存在失败风险。作者将潜在原因归于状态估计误差、室外光照和执行器问题，并报告突出边缘处发生脚尖碰撞；此外，实验未分别量化各因素的贡献，也未报告对不同台阶尺寸、材质、遮挡、动态障碍或严重传感器退化的系统测试。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- odom_base：仅依赖机器人本体感知传感器的位姿估计，是判断多传感器融合能否减少长期累积漂移的直接参照。
- odom_lidar（LIO）：基于LiDAR惯性里程计的位姿估计，具有较好的绝对定位精度，但存在高频振荡；与融合结果比较可判断引入本体观测是否改善控制所需的平滑性。
- DS（Double Step，双步态）：双脚先后踏上同一级台阶并恢复稳定双支撑，再规划下一级。它是较保守的真实机器人策略，用于衡量稳定观测和逐步重规划所能达到的误差水平。
- SS（Single Step，单步态）：左右脚交替踏上相邻台阶，并在行走过程中在线规划。它与DS的比较用于揭示更快连续运动对状态观测稳定性、落脚误差和碰撞风险的影响。

**实验想回答的问题**

- 多传感器融合能否同时缓解机器人本体里程计的累积漂移与激光里程计的高频振荡，从而为楼梯检测和落脚点规划提供平滑、可靠的位姿估计？
- 完整的感知—规划—控制闭环能否在仿真以及室内外真实楼梯上实时运行，并以可接受的落脚误差连续完成攀爬；不同步态策略在速度、稳定性和误差之间有何权衡？

**实验实现**

实验平台为KUAVO人形机器人，高166 cm、重55 kg、具有28个自由度，脚掌尺寸为26×9.6 cm；传感器包括3D LiDAR、RGB-D相机和IMU，计算平台为NVIDIA Orin NX，全身运动规划以20–30 Hz实时输出。实验依次包括里程计对比、5次Gazebo仿真以及5次室内外真实攀爬。仿真记录总时间、级数、平面检测频率和最大落脚误差；真实实验采用DS或SS策略并记录相同类型指标。原文没有报告正式训练过程、随机种子、置信区间、均值方差、独立成功率统计，也没有给出与其他完整楼梯攀爬方法的量化对比，因此这些试验主要属于系统可行性和闭环性能验证。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 位姿估计来源对比：odom_base、odom_lidar与odom_fused | 仅本体感知的odom_base在x、z轴随时间产生明显累积漂移；odom_lidar绝对定位较准，但尤其在y轴存在显著高频振荡；odom_fused同时抑制高频噪声并减小累积漂移。原文未给出三者的RMSE、漂移率或其他数值误差。 | 该对比隔离了多传感器融合的作用：LIO负责限制长期漂移，本体观测则为状态估计增加短时平滑约束。它支持“融合轨迹更适合反馈控制”的设计判断，但由于只有轨迹图和定性描述，无法判断提升幅度或统计稳定性。 | 第IV-A节，图4<br><span class="experiment-evidence">The fused result (odom_fused) combines the advantages of both estimations: it retains the global accuracy of LIO while incorporating proprioceptive observations to constrain and smooth the state estimation, resulting in much more stable trajectories along all three axes.</span> |
| 真实室内步态策略对比：DS与SS | DS完成4级楼梯需要9.6–10.2 s，最大落脚误差为11.4–12.1 mm；SS完成同样4级任务需要7.7 s，但最大落脚误差为24.7 mm。 | 该对比主要隔离“稳定站立后逐步规划”和“运动中连续在线规划”的影响。SS将时间缩短约2 s以上，但误差明显扩大，说明快速连续步态会降低基座观测及落脚规划的稳定性。不过两种策略并非在多次完全相同条件下进行严格配对测试，因此差异还可能受到单次场景和执行波动影响。 | 第IV-C节，表II<br><span class="experiment-evidence">The results show that the DS gait requires a total time of approximately 9.6–10.2 s.</span> |

**定性案例**

- 图6的室内案例使用台阶高度13 cm、踏面宽度28 cm的楼梯，而机器人脚长为26 cm，前后方向仅有约2 cm的名义几何余量。系统先检测绿色楼梯平面，再生成蓝色可落脚区域和下一步足端目标；机器人在每次稳定双支撑后更新落脚点并重新规划，最终以DS完成4级攀爬。该案例直观说明多边形平面表示如何转化为可执行落脚区域；与之相对，图8的突出边缘室外案例中，SS较大的落脚误差导致脚尖碰撞，说明仅检测主平面可能不足以消除边缘几何与动态误差共同造成的风险。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Proposes a perception-based mapping and locomotion-planning framework for humanoid robot stair climbing.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`386689b77a2c4af0cf295f2d504639ff270ba787cdf044739b6836f818ae7d59`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
