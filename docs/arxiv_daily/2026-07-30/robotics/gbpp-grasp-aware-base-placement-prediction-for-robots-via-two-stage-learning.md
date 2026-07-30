---
title: "[论文解读] GBPP: Grasp-Aware Base Placement Prediction for Robots via Two-Stage Learning"
description: "[arXiv 2509.11594][机器人 / 具身智能] GBPP将移动机器人的抓取基座选位转化为候选位姿可行性分类，并用“大规模廉价启发式预训练、小规模高保真仿真校准”的两阶段学习缓解训练成本与抓取真实性之间的矛盾。"
arxiv_id: "2509.11594"
announcement_date: "2026-07-30"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T07:32:04.569742+00:00"
source_sha256: "8991c0bb01624916c5e623fa87c8cdce14e7bb6b0525483da2db495e4e2c4799"
tags:
  - "机器人 / 具身智能"
  - "移动操作"
  - "机器人基座放置"
  - "抓取可行性预测"
  - "RGB-D点云"
  - "PointNet++"
  - "候选位姿评分"
  - "两阶段学习"
  - "任务与运动规划"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2509.11594</p>

# GBPP: Grasp-Aware Base Placement Prediction for Robots via Two-Stage Learning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Jizhuo Chen, Diwen Liu, Jiaming Wang, Harold Soh</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2509.11594v3) · [PDF 下载](https://arxiv.org/pdf/2509.11594v3) · **关键词** 移动操作, 机器人基座放置, 抓取可行性预测, RGB-D点云, PointNet++, 候选位姿评分, 两阶段学习, 任务与运动规划  


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

GBPP将移动机器人的抓取基座选位转化为候选位姿可行性分类，并用“大规模廉价启发式预训练、小规模高保真仿真校准”的两阶段学习缓解训练成本与抓取真实性之间的矛盾。

**不用术语来说**：移动机器人即使看见并接近目标，也可能因为停靠位置不合适而无法抓取：机械臂可能够不到目标，运动时可能碰撞障碍物，或关节需要超出允许范围。机器人因此需要在执行抓取前，从许多候选停靠位置中迅速选出既安全又便于机械臂操作的位置；在家庭、仓库和医院等存在遮挡与杂物的场景中，仅凭“离目标更近”通常不足以做出可靠选择。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者实证研究了两阶段数据课程：先用距离—可见性规则生成大规模低成本标签，再用规模较小但更接近真实抓取结果的高保真仿真数据细化分类边界，从而分析两类数据在覆盖范围与标签保真度上的互补作用。
- 作者围绕数据生成成本、预测性能和在线运行时间评估这一设计，并在仿真与真实移动操作平台上检验其相对于邻近性、几何方法和开环基线的实用性；作者明确将论文定位为对基座选位学习中设计取舍的经验研究，而非全新规划算法。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于移动操作（mobile manipulation）中的机器人基座放置问题：移动机器人不仅要导航到目标附近，还要选择一个能让机械臂完成无碰撞抓取、避免关节限位且保持目标可达的基座位姿。常见模块化系统将感知、导航和抓取分开处理，但导航阶段通常不了解机械臂的可达性；任务与运动规划（TAMP）虽能联合搜索基座、抓取与关节轨迹，却往往依赖高质量环境几何并具有秒级至分钟级延迟。GBPP采用学习式候选评分，将基座放置转化为对离散候选位姿的二分类或可行性打分，以单帧RGB-D形成的局部点云为主要环境表示，在数百个候选中快速选出最可能支持成功抓取的位置。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**移动操作与基座放置**

移动操作机器人同时具有可移动底盘和机械臂；基座放置决定机器人在开始抓取前停在哪里。位置过远会使目标超出机械臂工作空间，过近或朝向不当则可能造成碰撞、遮挡或关节受限。

</div>
<div class="conceptitem" markdown="1">

**RGB-D与部分点云**

RGB-D相机同时提供彩色图像和每个像素的深度，经过目标分割与三维反投影后可得到目标及周围场景的点云。由于只有单个观察视角，点云只覆盖传感器可见的表面，因此是不完整的局部几何表示。

</div>
<div class="conceptitem" markdown="1">

**PointNet++式集合抽象**

PointNet++是一类直接处理无序三维点集的神经网络，通过分层采样、邻域分组和特征聚合学习局部到全局的几何特征。本文用其编码点云，再由多层感知机结合机器人参数，对各候选基座位姿输出抓取可行性分数。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定机器人在当前观察位置获取的一帧RGB-D图像、其中分割出的目标对象、由深度信息重建的部分点云，以及描述机器人几何或运动能力的参数，系统需要对预先生成的稠密候选基座位姿集合逐一评分。每个分数表示机器人移动到该候选位姿后成功抓取目标的可行性，最终执行得分最高的候选。该设置假定候选位姿已经给定或可由网格产生，重点不是在线求解完整的基座—抓取—关节轨迹联合优化，而是从不完整的视觉几何中快速筛选一个兼顾距离、可见性、机械臂可达性和碰撞风险的停靠位置；论文示例一次评估约600个候选。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$\mathcal{P}$**

由目标分割后的RGB-D观测重建得到的部分三维点云；原文节选未明确给出该符号，仅用于概括输入。

</div>
<div class="notationitem" markdown="1">

**$\theta_r$**

机器人参数，如与底盘和机械臂能力有关的描述；原文节选未明确列出参数组成或正式符号。

</div>
<div class="notationitem" markdown="1">

**$\mathcal{B}=\{b_i\}_{i=1}^{N}$**

候选基座位姿集合，其中b_i为第i个候选，N为候选数量；原文提到稠密网格及约600个候选，但未在所给章节中规定此记号。

</div>
<div class="notationitem" markdown="1">

**$s_i$**

模型为候选位姿b_i预测的抓取可行性分数，系统选择分数最大的候选执行；原文节选未给出正式符号或概率校准定义。

</div>

</div>

**直接相关的工作**

- **模块化感知—导航—抓取系统（如OK-Robot与GoToAnything）**: 这类系统便于集成并能快速导航，但导航模块通常不考虑机械臂可达性和抓取约束，可能把机器人带到后续无法完成抓取的位置。GBPP在执行抓取前显式评估候选基座位姿，旨在减少这种由模块间信息割裂造成的死胡同。
- **整体任务与运动规划（TAMP）**: TAMP联合推理基座位姿、抓取位姿和关节轨迹，能够提供更原则化的可行性判断，但通常计算延迟较高，并依赖精细网格或有符号距离场。GBPP不寻求同等形式的全局可行性保证，而是以学习式评分换取从单帧、不完整RGB-D几何出发的快速在线选择。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现有移动操作流程通常先由导航模块把机器人送到目标附近，再由抓取规划器尝试生成机械臂轨迹，但导航阶段并未考虑机械臂可达性、碰撞和关节限制。结果是机器人可能到达一个导航上合理、抓取上却不可行的位置，随后陷入失败和代价高昂的重新规划。实际系统需要根据单帧RGB-D观测，在大量候选基座位姿中快速判断哪些位置真正有利于抓取。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **模块化导航与几何筛选方法**：模块化系统先定位目标并将基座导航至附近，再独立规划抓取；改进版本会加入体素占用检查、射线投射等几何规则，以排除被遮挡或可能碰撞的候选位置。这类方法主要依靠距离、可见性和显式场景几何进行决策。
- **任务与运动联合规划或纯仿真学习**：任务与运动规划（TAMP）联合搜索基座位置、抓取方式和机械臂轨迹，以直接验证完整任务是否可执行；学习式替代方案则可通过大量仿真抓取试验收集成败标签，训练模型从观测直接预测候选基座位姿的可行性。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 模块化流程割裂了导航与抓取：导航只保证基座能够接近目标，却不保证机械臂从该处可达且无碰撞；体素检查或射线投射虽能减少部分错误，但会增加计算开销，而且简单几何条件不能完整表达关节限制和真实抓取成败。
- TAMP能够进行更全面的联合推理，但其运行时间和对物体、环境网格模型的需求妨碍实时部署；另一方面，若完全依赖高保真仿真训练分类器，则需要极大量抓取试验。原文举例称，18万条启发式标签在RTX-A5000上生成不足三天，而同等数量的仿真试验需要三周以上，说明直接扩展仿真数据在计算成本上难以承受。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

缺少一种兼顾三项要求的基座选位方案：它既要获得足够广泛的数据覆盖，又要让预测与真实抓取可达性和碰撞结果一致，还要能在在线阶段迅速评估数百个候选位姿。廉价启发式标签容易规模化但不够真实，高保真仿真更可信却难以大规模生成；此前尚不清楚能否有效组合二者，以及二者分别应在学习过程中承担什么作用。

</div>
<div markdown="1"><span>核心问题</span>

能否先利用距离—可见性启发式数据学习广泛的几何先验，再以少量高保真仿真抓取结果校准模型，使其在显著降低数据生成成本的同时，仍能快速、可靠地预测候选基座位姿的抓取可行性，并从仿真泛化到真实环境？

</div>
<div markdown="1"><span>作者直觉</span>

简单规则虽然无法准确模拟完整抓取过程，却能廉价地告诉模型大量明显的正反例，例如位置是否过远、目标是否可见，从而先形成覆盖广泛的粗略判断边界；随后只需把昂贵仿真集中用于规则容易犯错的复杂情况，如机械臂不可达、潜在碰撞或关节受限，就可以修正这条边界。通俗地说，第一阶段让模型“见得多”，第二阶段让它“判断得更像真实抓取”，从而避免用昂贵仿真从零学习全部规律。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

GBPP将移动机器人基座放置建模为条件二分类与排序问题：输入单帧RGB-D观测、目标分割掩码、机器人几何参数以及一组平面候选基座位置，网络逐一预测每个位置能否支持无碰撞抓取，并从无基座碰撞的候选中选择“可行”类别得分最高者。其核心是两阶段课程式训练：先用距离—可见性启发式规则自动生成18万条低成本标签，使模型广泛学习目标、障碍物与候选位置之间的空间关系；再用约1.2万条经过逆运动学和碰撞检查的仿真标签继续训练，以修正启发式规则无法描述的关节极限、机械臂可达性和复杂碰撞。
从直观上看，第一阶段类似先教机器人掌握“不要太近或太远、尽量看清目标”的粗略常识，第二阶段再通过真实度更高的仿真练习校准这些常识。最终模型不是在线执行耗时的完整任务与运动规划，而是将密集候选网格批量评分，因此可快速给出较安全且适合抓取的站位。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 场景表示与候选基座构造

将RGB-D反投影为带颜色点云 \mathcal{P}，并为每个点附加目标二值掩码 m_i；点云裁剪到目标周围半径 d_{\mathrm{arm}} 内，并根据 h_{\mathrm{base}} 对齐竖直坐标。每个候选 \mathbf b_k=(x_k,y_k) 额外表示为位于 (x_k,y_k,0) 的50个黑色合成点，目标点统一赋予场景中不会自然出现的颜色 RGB=[0,77,77]。

<div class="method-step__io" markdown="1">

**输入**：单帧RGB-D图像、目标物体分割结果、相机高度 h_{\mathrm{cam}}、基座高度 h_{\mathrm{base}}、机械臂最大伸展距离 d_{\mathrm{arm}}，以及目标周围的平面候选集合 \mathcal{B}。  
**输出**：同时编码局部场景几何、目标身份和某一候选基座位置的点集输入。

</div>

**直观理解**：网络必须知道“要抓哪个物体”和“正在评价哪个站位”；特殊颜色相当于目标标签，50个合成点则像在三维地图上插入一个醒目的候选位置标记。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 第一阶段启发式自动标注与预训练

用非对称高斯距离分数描述偏好抓取距离，并根据杂乱渲染相对于仅含目标的理想渲染计算可见性分数；二者按 \alpha=0.51 加权后，以验证集阈值 \tau=0.4546 转换为二值可行性标签。使用18万条自动标注样本，以加权交叉熵训练PointNet++风格编码器和MLP分类头。

<div class="method-step__io" markdown="1">

**输入**：大量场景中的候选位置、候选到目标中心的距离 d_k，以及从该候选视角得到的目标可见比例 \rho_k。  
**输出**：具备广泛几何先验的初始分类器 f_\theta。

</div>

**直观理解**：这一阶段的标签并不等同于真实抓取结果，但生成便宜、覆盖面大，可先让网络学会避开明显过近、过远或目标严重被遮挡的位置。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 第二阶段高保真仿真细化

对每个候选位置，在ManiSkill中尝试多次带逆运动学求解和碰撞检查的抓取规划与执行，并以仿真返回的抓取可行性 y_k^{\mathrm{sim}} 作为标签。随后用约1.2万条仿真样本和标准交叉熵继续训练同一分类器。

<div class="method-step__io" markdown="1">

**输入**：ProcTHOR场景、一个目标物体、六个YCB杂物、例如25×25的密集候选网格，以及第一阶段得到的参数。  
**输出**：经真实抓取约束校准的两阶段模型。

</div>

**直观理解**：仿真标签较昂贵但更接近实际执行，因此只用较小数据集纠正第一阶段的粗糙判断，特别是规则看不到的关节极限和复杂碰撞。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 密集评分与在线选择

对所有候选位置运行分类器，取得“可行”类别的logit \ell_k，并在无基座碰撞的候选中选择得分最高的位置。原文报告在RTX-4090笔记本GPU上约0.3秒可评估600个候选位置。

<div class="method-step__io" markdown="1">

**输入**：测试场景的点云与目标掩码、机器人参数、候选基座集合，以及基座自身的碰撞检查结果。  
**输出**：用于实际导航和抓取执行的基座位置 \mathbf b^*。

</div>

**直观理解**：模型像给网格中的每个站位打分，执行时直接选择最高分且机器人底盘能安全到达的位置，而不必为所有候选逐一运行完整抓取规划。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="equation-block" markdown="1">

#### 候选基座的启发式自动标签

$$
\begin{aligned}\mathrm{distScore}(d)&=\begin{cases}a\exp\!\left(-\dfrac{(d-\mu)^2}{2\sigma_l^2}\right),&d<\mu,\\a\exp\!\left(-\dfrac{(d-\mu)^2}{2\sigma_r^2}\right),&d\geq\mu,\\0,&d\notin[0.14,0.92],\end{cases}\\\mathrm{visScore}(\rho)&=\begin{cases}0.05+\dfrac{0.25}{0.04}\rho,&0\leq\rho<0.04,\\0.3,&0.04\leq\rho\leq0.8,\\0.3+\dfrac{0.3}{0.2}(\rho-0.8),&\rho>0.8,\end{cases}\\H_k&=\alpha\,\mathrm{visScore}(\rho_k)+(1-\alpha)\,\mathrm{distScore}(d_k),\qquad y_k^{\mathrm{heur}}=\begin{cases}1,&H_k\geq\tau,\\0,&H_k<\tau.\end{cases}\end{aligned}
$$

**符号说明**

- $d$：候选基座位置到目标中心的欧氏距离，单位为米。
- $\mu$：规则所偏好的基座—目标距离中心。
- $\sigma_l,\sigma_r$：距离小于或大于 \mu 时分别使用的高斯分布尺度，使近侧与远侧惩罚可以不对称。
- $a$：距离分数的幅值系数；其具体数值在所给原文节选中未明确报告。
- $\rho_k$：候选位置 \mathbf b_k 下目标的可见比例，由杂乱场景渲染与仅含目标的理想渲染比较得到。
- $H_k$：第 k 个候选位置的距离—可见性综合启发式分数。
- $\alpha$：可见性分数的权重，文中设为0.51；距离分数权重为1-\alpha。
- $\tau$：把连续启发式分数转为二值标签的阈值，验证集上设为0.4546以平衡假阳性与假阴性。
- $y_k^{\mathrm{heur}}$：第一阶段为第 k 个候选位置生成的二值可行性标签。

<div class="equation-explanation" markdown="1">

**直观理解**：距离分数偏好位于机械臂典型工作区内且接近理想距离的位置，并允许“太近”和“太远”受到不同强度的惩罚；可见性映射重罚几乎看不到目标的视角，对中等可见性保持平坦，只额外奖励接近完整可见的视角。两者加权并阈值化后即可自动生成大量训练标签，但这些标签只表达几何常识，不保证逆运动学和真实碰撞约束一定成立。  
**原文位置**：第III-B节 Stage 1: Heuristic Auto-Labeling

</div>

</div>

<div class="equation-block" markdown="1">

#### 条件可行性评分与最优基座选择

$$
\mathbf b^*=\arg\max_{\mathbf b_k\in\mathcal B_{\mathrm{free}}} f_\theta\!\left(\mathbf b_k,\mathcal P,\mathcal M,h_{\mathrm{cam}},h_{\mathrm{base}},d_{\mathrm{arm}}\right)=\arg\max_{\mathbf b_k\in\mathcal B_{\mathrm{free}}}\ell_k
$$

**符号说明**

- $\mathbf b_k=(x_k,y_k)$：平面工作空间中的第 k 个候选机器人基座位置。
- $\mathcal B_{\mathrm{free}}$：候选集合中通过基座碰撞检查的位置；原文任务定义写作 \mathcal B，推理时进一步要求候选collision-free。
- $\mathcal P$：由RGB-D图像反投影得到、同时含三维坐标与颜色的点云。
- $\mathcal M$：点云对应的目标物体二值掩码集合。
- $h_{\mathrm{cam}},h_{\mathrm{base}}$：相机高度和机器人基座高度。
- $d_{\mathrm{arm}}$：机械臂最大伸展距离，也用于限定局部点云裁剪范围。
- $f_\theta$：参数为 \theta 的神经二分类器，预测给定场景和机器人条件下候选位置的抓取可行性。
- $\ell_k$：分类器对第 k 个候选输出的“可行”类别logit；它用于候选间排序，不必先转换为概率。
- $\mathbf b^*$：最终选择并交付执行的最高分无碰撞基座位置。

<div class="equation-explanation" markdown="1">

**直观理解**：该式将基座放置从连续、昂贵的在线运动规划简化为有限候选集合上的评分与取最大值。由于所有候选共享同一场景表示并可批量计算，系统能够密集搜索；但最终选择质量取决于候选网格覆盖范围和模型对真实抓取可行性的校准程度。  
**原文位置**：第III-A节 Task Definition与第III-D节 Inference

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：第一阶段以启发式二值标签 y_k^{\mathrm{heur}} 为监督，采用加权交叉熵优化分类器参数；加权的目的在于处理可行与不可行样本可能存在的类别不均衡，但所给节选未报告具体类别权重。第二阶段从第一阶段参数继续训练，以仿真抓取可行性 y_k^{\mathrm{sim}} 为监督并使用标准交叉熵；因此优化目标仍是候选级二分类，变化的是标签来源和可信度。技术上，交叉熵推动正确类别logit相对增大；方法意图上，第一阶段学习覆盖广的距离、遮挡和局部几何规律，第二阶段使输出排序更符合经过逆运动学与碰撞验证的实际抓取结果。原文节选未给出交叉熵的显式公式，故不额外虚构损失表达式。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 候选条件化点云表示**

每个点 \mathbf p_i=(x_i,y_i,z_i,r_i,g_i,b_i) 同时具有三维坐标和RGB信息，并通过 m_i 标识其是否属于目标；候选基座被转成50个共址的黑色合成点，目标点则用唯一颜色突出。裁剪范围由 d_{\mathrm{arm}} 决定，竖直参考由 h_{\mathrm{base}} 对齐，使输入同时反映机器人尺度与场景布局。

> 直观理解：若只输入普通点云，网络可能不知道当前候选在哪里，也可能混淆目标与杂物；显式加入候选标记和目标标记后，同一场景可以针对不同站位分别判断。

**2. PointNet++风格空间编码器与二分类头**

网络使用3个Set-Abstraction层提取点云的分层局部—全局几何特征，再由带BatchNorm和Dropout的MLP完成二分类；文中给出的MLP宽度为1024→512→256→2，输出候选不可行与可行两类logit。Set-Abstraction通过逐级采样、邻域聚合和特征抽象处理无序点集，适合识别目标、遮挡物与候选基座之间的空间关系。

> 直观理解：编码器先把大量散乱三维点压缩成“目标在哪里、周围是否拥挤、候选离目标多远”等特征，MLP再据此判断该站位是否值得尝试。

**3. 低成本覆盖—高保真校准的两阶段课程**

第一阶段标签只依据距离与可见性，规模大但存在系统性偏差；第二阶段通过逆运动学和碰撞检查产生较少但更可信的执行级标签，并从第一阶段参数继续优化。两阶段并非两个独立推理模型，部署时仅保留经过第二阶段细化后的单一分类器。

> 直观理解：该设计用便宜规则解决“数据量不够”，再用昂贵仿真解决“标签不够真实”，避免完全依赖大规模抓取试验或完全相信简单规则。

**训练与推理**

训练时，先为大量候选计算 d_k 与 \rho_k，经规则得到 y_k^{\mathrm{heur}}，并把每个“场景—候选”组合编码为带目标标记和候选合成点的点云样本；18万条样本用于训练初始网络。随后在ProcTHOR中布置目标和六个YCB杂物，对密集网格上的候选在ManiSkill里执行多次逆运动学与碰撞检查抓取，得到约1.2万条 y_k^{\mathrm{sim}}，再以这些高保真标签细化同一网络。
推理时，只需从新RGB-D观测生成点云与目标掩码，对目标周围所有候选构造条件化输入并批量前向计算。系统过滤会造成基座碰撞的位置，然后按可行类别logit排序并输出 \mathbf b^*；此时不再运行自动标注规则，也不需要为每个候选执行完整IK抓取试验。

**复现信息**

复现和解释方法所需的关键设置包括：点云裁剪半径为 d_{\mathrm{arm}}，竖直坐标按 h_{\mathrm{base}} 对齐；每个候选以50个黑色合成点表示，目标点颜色固定为[0,77,77]；编码器含3个Set-Abstraction层，分类MLP为1024→512→256→2并使用BatchNorm与Dropout。第一阶段使用18万条自动标注样本、\alpha=0.51和验证阈值\tau=0.4546，距离规则仅在[0.14,0.92]米典型工作区内给出非零分数；第二阶段约有1.2万条仿真样本，场景包含一个目标与六个YCB杂物，候选网格示例为25×25。在线效率方面，原文报告RTX-4090笔记本GPU评估600个候选约需0.3秒；学习率、优化器、批大小、训练轮数以及 a、\mu、\sigma_l、\sigma_r 的具体值在所给节选中原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- ProcTHOR合成室内场景：共12,000种布局，通过ManiSkill完成物理仿真与抓取执行。每个场景包含1个目标物体和6个作为杂物的YCB物体；目标从30种不同YCB物体中选择并放置在家具上。该数据用于构造多样化的室内几何、遮挡与碰撞条件。
- 第一阶段启发式标签数据：完整数据约252,000个样本，其中180,000个启发式标注样本用于训练，30,000个用于验证，30,000个用于测试。标签由距离—可见性规则自动生成，作用是以较低标注成本学习候选底座位姿与局部场景几何之间的粗粒度关系。
- 第二阶段仿真标签数据：12,000个仿真标注样本用于第二阶段训练与评估。标签依据仿真中的逆运动学可行性和碰撞检测产生，比启发式标签更接近实际抓取结果，其作用是校准第一阶段模型。原文节选未进一步说明这12,000个样本内部是否另行划分训练集与测试集。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span>原文未明确报告，或这里不需要额外前置概念。</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文节选仅说明实验包含基线，但未给出基线名称、实现方式或比较目的；因此无法从所提供内容可靠列出具体基线。

**实验想回答的问题**

- 两阶段学习流程能否先利用低成本的距离—可见性启发式标签获得广泛的几何覆盖，再通过少量高保真仿真标签使模型贴近真实的抓取可行性？
- 面对不同室内布局、目标物体和机器人几何参数，模型能否仅根据单帧RGB-D点云，为目标周围的候选平面底座位姿预测有效分数？

**实验实现**

每个场景先在目标周围采样平面底座位姿网格B，每个候选位姿记为b_k。数据生成时随机覆盖多种机器人配置：相机高度h_cam∈[0.8,1.5]米、底座高度h_base∈[0.5,1.0]米、机械臂可达距离d_arm∈[0.3,1.0]米。场景先运行5,000个物理步以达到稳定状态，再将单帧RGB-D图像反投影为点云P，并按方法章节所述进行裁剪和对齐。第一阶段以距离—可见性规则产生的y_k^heur训练模型；第二阶段以逆运动学和碰撞检测得到的y_k^sim进行细化。训练协议节选仅显示模型使用三层集合抽象结构及一个以1024→512→256开头的MLP描述，但原句被截断，优化器、学习率、批大小、训练轮数以及完整网络尺寸均无法确认。所给节选也未包含具体评价指标和测试时的位姿选择协议。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work proposes a learned base-pose scorer for grasp-aware mobile robot manipulation.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`8991c0bb01624916c5e623fa87c8cdce14e7bb6b0525483da2db495e4e2c4799`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
