---
title: "[论文解读] StairMaster: Learning to Conquer Risky Hollow Stairs for Agile Quadrupedal Robots"
description: "[arXiv 2606.25765][机器人 / 具身智能] StairMaster旨在让四足机器人依靠强化学习、抗噪深度感知与时空记忆，在存在大空隙、视觉盲区和严重传感噪声的陡峭镂空楼梯上实现稳定且可零样本迁移的攀爬。"
arxiv_id: "2606.25765"
announcement_date: "2026-07-30"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T07:32:04.300312+00:00"
source_sha256: "86438b21bf0f7e56d161b8c2832e2f9c6286435d8e468f70138eb620d6e067da"
tags:
  - "机器人 / 具身智能"
  - "强化学习"
  - "四足机器人"
  - "镂空楼梯"
  - "视觉引导运动"
  - "深度强化学习"
  - "部分可观测性"
  - "时空记忆"
  - "深度传感器建模"
  - "仿真到现实迁移"
  - "主动感知"
  - "精确落脚"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2606.25765</p>

# StairMaster: Learning to Conquer Risky Hollow Stairs for Agile Quadrupedal Robots

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Xincheng Tang, Youhan Xie, Zhengjie Shu, Wanyu Li, Lai Jiang, Wenkang Hu, Yitong Li, Ruigang Yang</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2606.25765v2) · [PDF 下载](https://arxiv.org/pdf/2606.25765v2) · **关键词** 四足机器人, 镂空楼梯, 视觉引导运动, 深度强化学习, 部分可观测性, 时空记忆, 深度传感器建模, 仿真到现实迁移, 主动感知, 精确落脚  
**项目页**: [https://sivan666666.github.io/StairMaster/](https://sivan666666.github.io/StairMaster/)  

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

StairMaster旨在让四足机器人依靠强化学习、抗噪深度感知与时空记忆，在存在大空隙、视觉盲区和严重传感噪声的陡峭镂空楼梯上实现稳定且可零样本迁移的攀爬。

**不用术语来说**：镂空楼梯没有封闭的竖直踢面，踏板之间是可能卡住机器人腿部的大空隙；同时，狭窄踏板会很快移到机身下方并离开前置相机视野，金属反光或格栅结构还会使深度图出现大量缺失和噪点。因此，机器人既难以看清下一步，也必须在看不见后腿落点时准确踩住踏板，极小误差就可能导致腿落入空隙并损坏硬件。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出面向高风险镂空楼梯的三阶段强化学习框架StairMaster：以交叉注意力从稀疏、含噪深度观测中提取结构特征，并结合空间感知LSTM保存随机器人运动更新的时空信息，以应对踏板移出视野后的持续盲区。
- 作者针对真实部署补充高保真深度传感器仿真，并设计三维航点引导的主动感知奖励、镂空间隙运动学惩罚和楼梯边缘惩罚；据作者报告，该策略在Unitree Go2上通过零样本迁移攀爬了最大倾角55°的真实镂空楼梯。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于视觉引导的四足机器人强化学习运动控制。该方向利用深度相机提供的外部环境信息与机器人自身的本体感知信息，共同生成关节控制指令，使机器人穿越非结构化地形。本文聚焦工业设施常见的镂空楼梯：与具有封闭立板的普通楼梯不同，其踏板之间存在大面积空隙，落脚误差可能使腿部插入空洞；反光或栅格材料还会造成深度像素大量缺失和高频噪声，而前向相机在踏板移至机身下方后无法继续观测它，因而后腿必须依靠此前形成的空间记忆完成精确落脚。这一任务同时要求可靠感知、长期时空记忆和敏捷控制，是典型的部分可观测视觉运动控制问题。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**深度强化学习（Deep Reinforcement Learning, DRL）**

机器人通过与仿真环境反复交互，根据奖励信号学习从观测到动作的控制策略，而不必为每一级台阶手工编写步态规则。本文训练的是端到端楼梯攀爬策略，并将仿真中学到的策略直接部署到真实机器人。

</div>
<div class="conceptitem" markdown="1">

**部分可观测性与时空记忆**

机器人当前看到的单帧图像不能完整反映环境，例如踏板经过机身下方后会离开前向相机视野，因此策略需要记住过去观测，并结合机器人自身运动推断地形当前位于何处。所谓时空记忆不仅保留时间序列信息，还要维持地形结构与机器人位置变化之间的空间对应关系。

</div>
<div class="conceptitem" markdown="1">

**仿真到现实迁移（Sim-to-Real）**

策略通常先在仿真器中大规模训练，再部署到真实硬件，但理想化仿真深度图与真实相机的掉点、噪声和运动伪影存在差异。本文通过模拟这些传感器缺陷缩小差距，目标是在真实 Unitree Go2 上实现无需现实微调的零样本迁移。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务是在具有窄踏板、大型开放间隙和陡峭坡度的镂空楼梯上控制四足机器人稳定向上攀爬。策略的输入包括前向深度相机产生但可能稀疏、缺失且含高频噪声的视觉观测，以及反映机器人自身状态的本体感知信息；由于相机视场有限，脚下踏板和空隙可能长期不可见。策略需要从当前观测与历史时空信息中提取楼梯结构，输出驱动四足运动的控制动作，使各足精确落在踏板上，同时避免腿部落入空隙或踩近楼梯边缘，并主动调整机身俯仰以观察后续台阶。研究设定以强化学习在仿真中训练、在真实 Unitree Go2 上零样本部署为主；摘要与引言报告的目标场景最高包含约 55° 的真实镂空楼梯，但所给背景章节未明确给出动作参数化、传感器分辨率或控制频率。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$r_{\text{pitch}}$**

三维航点引导的主动感知俯仰奖励，用于鼓励机器人调整机身俯仰角，以便提前观察即将到来的楼梯；所给节选仅出现该符号，未提供其完整公式。

</div>

</div>

**直接相关的工作**

- **Rudin et al. (2025), Parkour in the Wild**: 代表视觉引导的敏捷四足运动研究。本文将其作为现有视觉运动框架的相关背景，并指出在镂空楼梯上，传感器噪声与脚下长期视觉盲区叠加，使既有框架仍面临困难。
- **Yang et al. (2025a), Spatially-Enhanced Recurrent Memory for Long-Range Mapless Navigation via End-to-End Reinforcement Learning**: 提供空间增强循环记忆的直接技术基础。StairMaster采用 Spatial-Aware LSTM，以弥补普通 RNN 主要建模一维时间依赖、难以在机器人自身运动下维持全局空间拓扑对齐的问题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

电厂和建筑工地常用镂空楼梯减轻结构重量，四足机器人若要进入这些工业环境执行巡检等任务，就必须安全通过此类设施。然而，开放式空隙使一次很小的落足误差也可能造成卡腿，反光或格栅踏板又会引发深度像素大面积丢失；爬楼时机身快速转动、冲击和相机振荡会进一步恶化观测，使该任务同时具有高事故代价与高感知难度。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **无记忆视觉运动策略与多帧堆叠**：这类方法直接根据当前视觉观测和本体感知状态输出动作，或把连续若干帧拼接后交给策略，利用短期图像变化辅助判断地形。
- **标准循环神经网络与二维航点引导框架**：标准RNN通过循环隐藏状态压缩历史观测，以学习时间依赖；二维航点方法则用平面上的目标位置或方向约束机器人前进，但通常不显式表达相机俯仰方向上的观察需求。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 无记忆策略或简单帧堆叠无法在踏板长期移出前置相机视野后维持可靠的三维地形表征；标准RNN虽然能记忆时间序列，却主要编码一维时间关系，难以在机器人自身运动过程中对齐全局空间拓扑，因而无法可靠支持被遮挡的后腿精确落足。
- 现有视觉运动框架在快速机身转动、落足冲击以及反光或细薄结构造成的深度噪声下容易发生感知退化；常规奖励和二维航点引导又不会主动鼓励机器人调整机身俯仰角去观察前方踏板，因此在特别陡峭的楼梯上可能既看不清结构，也无法提前获取后续控制所需的信息。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有方法尚未形成一种可端到端训练的控制方案，能够同时处理镂空楼梯特有的深度稀疏与高频噪声、踏板移出视野造成的长期部分可观测性、后腿落足所需的空间记忆，以及陡坡攀爬中的主动观察需求，并将仿真策略无需真实环境再训练地迁移到高风险真实楼梯。

</div>
<div markdown="1"><span>核心问题</span>

能否通过融合抗噪结构特征提取、具有空间对齐能力的循环记忆、逼真的深度传感器仿真，以及面向观察姿态和安全落足的专用奖励，训练出可零样本部署于真实四足机器人的强化学习策略，使其稳定攀爬最高达55°的镂空楼梯？

</div>
<div markdown="1"><span>作者直觉</span>

机器人看见踏板时先从残缺深度图中抓住较可靠的结构线索，再把这些线索按自身运动关系写入带空间意识的记忆，相当于在踏板进入机身下方之前建立并持续更新一份内部地形印象；即使后腿落足时相机已看不到踏板，策略仍可依赖历史空间信息。与此同时，训练中复现真实相机伪影，可降低策略对理想深度图的依赖；奖励机器人主动调整俯仰角观察前路，并惩罚腿进入空隙或靠近踏板边缘，则把“先看清、再踩准”的安全行为直接纳入学习目标。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

StairMaster将空心楼梯攀爬建模为从机载本体感知与第一视角深度图直接生成12维目标关节动作的端到端控制问题。训练分三阶段：先用可访问特权高度图的教师策略通过PPO学习安全、敏捷的攀爬行为；再让仅使用真实可获得观测的学生策略以均方误差模仿教师，并通过交叉注意力和空间感知循环单元建立地形记忆；最后用PPO与空心楼梯专用奖励微调学生策略。部署时不需要高度图，策略仅依赖当前本体状态、带噪深度图和内部循环状态，即可零样本迁移至实体Unitree Go2。
直观而言，教师在训练时能够“俯视”完整地形，先学会怎样走；学生只能通过头部相机观察，因此需要学习教师动作，并把已经离开视野的台阶记在内部记忆中。深度噪声建模让模拟相机更接近真实相机，而俯仰引导、空隙避让和边缘惩罚分别促使机器人提前抬头观察、跨过空洞并踩向踏板中部。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段1：特权教师策略训练

使用PPO训练教师策略，并在标准运动奖励之外加入三维航点俯仰奖励、空心间隙运动学惩罚和楼梯边缘惩罚。地形课程从平地逐步提高台阶、缩短并缩窄踏板，最终达到55°，同时随机扰动高差与间隙。

<div class="method-step__io" markdown="1">

**输入**：机器人本体观测 o_t=[\omega_t,g_t,c_t,\theta_t,\dot{\theta}_t,a_{t-1}]^T，以及仅训练时可用的特权地形高度图；其中观测包含机身角速度、机身坐标系投影重力、速度指令、12维关节位置、12维关节速度和上一时刻12维动作。  
**输出**：能够利用完整地形信息产生专家目标关节动作的教师策略。

</div>

**直观理解**：这一阶段让机器人先在“答案可见”的条件下学会正确走法。专用奖励不仅要求它向前走，还明确告诉它应提前看向哪里、哪些空洞不能穿过、哪些落脚位置过于靠边。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段2：视觉学生策略蒸馏

CNN提取深度特征，MLP编码本体状态；以本体特征为查询、视觉特征为键和值执行多头交叉注意力，再由空间感知LSTM累积时空信息。学生动作通过均方误差损失拟合教师动作。

<div class="method-step__io" markdown="1">

**输入**：模拟生成并注入传感器伪影的当前深度图 D_t、本体观测 o_t，以及教师策略给出的专家动作。  
**输出**：无需特权高度图、可从机载观测生成目标关节动作的初始学生策略。

</div>

**直观理解**：学生像蒙住“上帝视角”后模仿教师，只能看相机和自身状态。注意力帮助它从大量无关或缺失像素中寻找与当前姿态最相关的楼梯边缘，循环记忆则保存后腿稍后仍要使用的踏板位置。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段3：学生策略强化学习微调

使用PPO让学生直接与环境交互，并沿用空心楼梯专用奖励，纠正仅靠动作模仿产生的次优行为。训练同时随机化摩擦、质量、电机强度、外力、动作延迟以及相机视场角和安装位姿。

<div class="method-step__io" markdown="1">

**输入**：蒸馏后的学生网络、带随机化的空心楼梯环境、噪声深度图、本体观测和上一时刻循环状态。  
**输出**：适用于零样本实体部署的最终视觉运动策略。

</div>

**直观理解**：模仿只能复现教师示范，不能保证学生面对自己的视觉误差时仍能恢复。再次进行强化学习，相当于让学生亲自练习并从失败中修正动作。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 实体推理与关节控制

策略依次执行视觉与本体编码、交叉注意力、空间感知循环更新和actor动作解码，直接输出目标关节角命令；实体端不使用高度图或额外在线训练。

<div class="method-step__io" markdown="1">

**输入**：实体机器人预处理后的实时深度图、当前本体观测，以及SRU保存的历史隐藏状态和细胞状态。  
**输出**：每个控制时刻的12维目标关节动作，以及供下一时刻使用的更新后时空记忆。

</div>

**直观理解**：部署时机器人边看、边记、边控制：前腿经过后即使踏板移出镜头，记忆仍可指导后腿落脚。所谓零样本迁移，是指模拟训练完成后直接在真机运行，而不再用真实楼梯数据调整参数。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="equation-block" markdown="1">

#### SRU空间门控与循环状态更新

$$
\begin{aligned}s_t&=\sigma(W_s f_t+b_s),\\(h_t,c_t)&=\operatorname{LSTM}\!\left(f_t,\,s_t\ast h_{t-1},\,s_t\ast c_{t-1}\right).\end{aligned}
$$

**符号说明**

- $f_t$：时刻 t 经交叉注意力得到的视觉—本体融合特征。
- $s_t$：由当前特征预测的可学习空间变换门，用于选择或重标定历史记忆。
- $\sigma$：Sigmoid函数，将门值压缩至0到1之间。
- $W_s,b_s$：空间门的可学习权重矩阵与偏置。
- $h_{t-1},c_{t-1}$：上一时刻LSTM的隐藏状态与细胞状态。
- $h_t,c_t$：更新后的隐藏状态与细胞状态，供actor和下一时刻使用。
- $\ast$：Hadamard逐元素乘法。

<div class="equation-explanation" markdown="1">

**直观理解**：第一行根据当前看到的地形决定历史记忆的哪些部分仍与当前空间位置相符；第二行先对旧记忆进行门控，再按LSTM规则与当前特征融合。这样可以抑制因视角变化而失效的信息，同时保留已经进入相机盲区但仍影响落脚的踏板结构。  
**原文位置**：METHOD—Visuospatial Encoder Architecture—Spatio-Temporal Memory with Spatial-Aware LSTM，式(1)–(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 空心楼梯专用奖励项

$$
\begin{aligned}r_{\mathrm{pitch}}&=\begin{cases}\exp\!\left[-4\left(\theta_{\mathrm{pitch}}-\theta_{\mathrm{pitch}}^{\mathrm{target}}\right)^2\right],&d<d_{\mathrm{th}},\\0,&\text{otherwise},\end{cases}\\r_{\mathrm{hollow}}&=\sum_{i=1}^{4}\begin{cases}-c_{\mathrm{hollow}},&\mathbf p_{\mathrm{foot},i}\in B_{\mathrm{hollow}},\\0,&\text{otherwise},\end{cases}\\r_{\mathrm{edge}}&=\sum_{i\in\mathrm{contact}}\begin{cases}-c_{\mathrm{edge}},&d_{\mathrm{edge},i}<d_{\mathrm{safe}},\\0,&\text{otherwise}.\end{cases}\end{aligned}
$$

**符号说明**

- $r_{\mathrm{pitch}}$：三维航点引导的俯仰奖励；仅当机器人接近前方航点时启用。
- $\theta_{\mathrm{pitch}},\theta_{\mathrm{pitch}}^{\mathrm{target}}$：机器人当前机身俯仰角，以及由机身指向前方第二级踏板中心的三维相对向量所确定的目标俯仰角。
- $d,d_{\mathrm{th}}$：机器人到目标航点的欧氏距离及俯仰引导的激活距离阈值。
- $r_{\mathrm{hollow}}$：足端进入空心间隙时施加的运动学惩罚。
- $\mathbf p_{\mathrm{foot},i},B_{\mathrm{hollow}}$：第 i 只足的位置，以及预定义空心间隙的三维包围区域。
- $c_{\mathrm{hollow}}$：单只足进入空隙时的正惩罚系数，实际奖励中取其负值。
- $r_{\mathrm{edge}}$：接触足落点过于靠近踏板边缘时施加的惩罚。
- $d_{\mathrm{edge},i},d_{\mathrm{safe}}$：第 i 只接触足到楼梯边缘的距离，以及允许的安全边距阈值。
- $c_{\mathrm{edge}}$：不满足安全边距时的正惩罚系数，实际奖励中取其负值。
- $\mathrm{contact}$：当前与踏板发生接触的足端集合。

<div class="equation-explanation" markdown="1">

**直观理解**：俯仰项在接近楼梯后奖励机身朝向前方第二级踏板，一方面改善腿部跨越高台阶的工作空间，另一方面让相机更早看到上方结构；距离阈值避免机器人仍在平地时过早抬头。其余两项形成两层落脚约束：足的摆动轨迹不能穿入空洞，真正接触踏板时又不能踩得太靠近边缘，从而把策略推向更高的抬腿轨迹和更居中的落脚点。  
**原文位置**：METHOD—Customized Reward Design for Hollow Stairs，式(3)–(5)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：阶段1和阶段3均以PPO最大化包含标准运动奖励与三个空心楼梯专用项的累计回报；原文节选未给出标准奖励全集、各项总权重或完整PPO目标公式，因此不能据此重建总奖励。阶段2采用动作蒸馏，以教师动作和学生动作之间的均方误差作为监督损失，使学生在仅有深度图与本体状态时复现特权教师行为；原文未明确报告MSE的具体公式、权重或是否与其他辅助损失联合使用。三阶段的职责分别是获得高质量专家、把专家能力迁移到可部署观测空间，以及通过环境交互弥补蒸馏造成的闭环控制偏差。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 多模态交叉注意力编码器**

CNN将最新深度帧 D_t 编码为稠密视觉特征图 f_v，MLP将本体观测 o_t 编码为特征 f_p。多头交叉注意力以 f_p 为query、以 f_v 为key和value，生成随机器人当前运动学状态变化的融合特征 f_t，使网络优先聚合与当前姿态和落脚需求相关的稀疏台阶边缘。

> 直观理解：直接拼接深度与状态会把大量墙面、空洞或噪声像素一并交给控制器；交叉注意力相当于用“机器人此刻怎样站立、准备怎样运动”去询问图像中哪些位置最值得关注。它解决的是当前帧的信息筛选问题，而不是长期记忆问题。

**2. 空间感知循环单元（SRU）**

SRU基于LSTM，在更新循环状态前由当前融合特征 f_t 预测空间变换门 s_t，并用该门逐元素调制上一时刻的隐藏状态 h_{t-1} 与细胞状态 c_{t-1}。该机制在不显式输入自运动估计的情况下，对历史地形特征进行隐式空间对齐，使已离开前视相机视野的踏板信息仍可参与后续动作生成。

> 直观理解：前置相机看到某级踏板时，后腿通常还没有踩到它；等后腿需要落脚时，该踏板可能已经处于机身下方的视觉盲区。SRU像一张会随机器人移动而自动调整的短期地图，避免普通循环网络把不同视角下的位置简单混在一起。

**3. 高保真深度噪声建模与统一预处理**

训练时对理想模拟深度图叠加高斯噪声、均匀噪声、随机孔洞、深度不连续处的边缘噪声、双目视差匹配误差和跨帧高斯像素平移；后者模拟足端冲击导致的相机振动。模拟与真实深度图均执行尺寸裁剪、深度截断、空间缩放和高斯模糊，以保持输入形式一致。

> 直观理解：模拟器通常给出过于干净的深度图，而真实红外或双目相机会在反光表面、细边缘和快速振动时产生缺测、漂移与错配。主动把这些缺陷加入训练，可迫使网络依赖稳定的结构线索和时间记忆，而不是记住理想像素位置。

**训练与推理**

训练先在渐进式地形课程中优化特权教师：从0°平地开始，随表现提升逐渐增加台阶高度、缩小踏板深度和宽度，直至55°；到达顶部航点后升级难度，最高级个体还会被重新分配到随机难度，以减轻灾难性遗忘。随后固定或调用教师产生动作标签，在加入多类深度伪影的模拟观测上蒸馏学生；最后让学生以PPO继续探索，并同时应用物理参数、外力、控制延迟和相机参数随机化。
推理时只保留学生网络。每个时刻将真实深度图按与模拟端相同的流程预处理，与本体观测共同输入编码器；SRU使用上一时刻状态更新地形记忆，actor输出目标关节角，更新后的循环状态传到下一时刻。教师高度图、空隙包围盒和楼梯边缘等特权信息仅服务于训练策略或奖励计算，不是文中所述实体部署输入。

**复现信息**

公平理解和复现所必需的设置包括：动作空间为12维目标关节命令；本体观测由3维机身角速度、3维投影重力、3维速度指令、12维关节位置、12维关节速度和12维上一动作组成；学生视觉输入是单个前置深度相机的最新帧，并通过循环状态利用历史。训练必须同时覆盖结构随机化、深度传感器伪影和动力学/相机域随机化，否则不能等同于论文所述零样本迁移方案。原文节选未明确报告网络层数、特征维数、图像分辨率、控制频率、PPO超参数、蒸馏批量与学习率、奖励权重、各阈值数值及训练步数，这些内容仍需依据完整论文或代码进行源核查。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- 平地基准环境：用于检查策略是否在普通连续地面上保持基本运动能力。原文未提供独立数据集、训练/测试划分或具体地形规模；每种方法在该地形上评估1000个回合。
- 标准化空心楼梯环境：具有踏板间空隙的主要目标场景，用于测试腿部避陷、结构感知和精确落脚能力。成功条件是机器人到达顶部平台的最终航点；每种方法评估1000个回合。原文未明确报告楼梯尺寸与测试实例数量。
- 随机混合楼梯环境：连续踏板的高度随机生成，且相邻踏板之间具有随机水平间隙，用于测试策略对未固定几何结构的空间推理与着地点控制。每种方法评估1000个回合；原文未明确报告随机参数范围及训练集与测试集是否分离。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**Success Rate（成功率）**

在空心楼梯试验中，机器人成功到达顶部平台最终航点的回合比例；它衡量完整完成任务的可靠性，而不是只跨过若干台阶的局部进展。 （越高越好，因为更高比例表示策略更经常完成整段楼梯。）

</div>
<div class="metricitem" markdown="1">

**Average Reached Steps（平均到达台阶比例）**

每个回合中成功越过的台阶占全部台阶的平均比例；当机器人质心越过对应踏板中心时，该台阶被计为已到达。该指标能反映失败前的任务进度，避免将差一个台阶和起步即失败都记作同一种失败。 （越高越好，因为它表示机器人平均能够深入并通过更大比例的楼梯。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 平地基准环境上的方法比较

<div class="result-value" markdown="1">

作者声称 StairMaster 在所有报告指标上优于其他方法，因此该总体结论也覆盖平地基准；但节选未给出Table 1的具体数值、领先幅度或方差。

</div>

该结果主要用于排除“专门适配空心楼梯后损害普通行走能力”的可能性。不过，在缺少逐项分数和不确定性统计的情况下，无法判断优势大小及其稳定性，也不能仅凭平地表现证明复杂楼梯能力。

<div class="result-source" markdown="1">

来源：Simulation Comparison and Ablation Study；具体结果据称见Table 1，但所给节选未包含表格行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">In comparison experiments, our method outperforms others in all metrics.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 标准化空心楼梯上的完整任务表现

<div class="result-value" markdown="1">

作者声称 StairMaster 在成功率和平均到达台阶比例上均优于所有比较方法。原文未明确报告具体成功率、平均到达台阶比例、绝对提升或统计误差。

</div>

若Table 1支持该结论，它意味着 StairMaster 不仅更常到达顶部，而且失败时通常也能前进得更远，因而对空隙避让与精确落脚更有效。但该比较仍不能单独确定优势来自感知架构、奖励设计还是训练流程，需要结合消融实验判断。

<div class="result-source" markdown="1">

来源：Simulation Comparison and Ablation Study；Table 1未包含在所给节选中

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">In comparison experiments, our method outperforms others in all metrics.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 随机台阶高度与随机水平间隙组成的混合楼梯

<div class="result-value" markdown="1">

作者声称 StairMaster 在该更具变化性的环境中同样在全部指标上优于其他方法；原文未明确报告具体数值和相对提升。

</div>

这一设置比固定楼梯更侧重空间推理和着地点精度，因此胜出可作为适应几何变化的证据。不过，原文节选没有给出随机范围、训练与测试分布关系或未见过结构上的单独统计，故不能据此断言策略实现了分布外泛化。

<div class="result-source" markdown="1">

来源：Simulation Comparison and Ablation Study；Table 1未包含在所给节选中

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">In comparison experiments, our method outperforms others in all metrics.</span>

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

- Extreme Parkour（EP）：两阶段视觉跑酷框架，先训练使用特权信息的教师策略，再蒸馏得到基于深度图的学生策略。它是有视觉、采用教师—学生训练范式的直接比较对象，可检验 StairMaster 的专用感知和记忆设计是否优于通用视觉跑酷方案。
- EP w/ Ours Rewards：在 Extreme Parkour 上加入本文的空心楼梯专用奖励，包括俯仰跟踪奖励和落脚相关奖励。该比较用于区分性能提升究竟来自奖励塑形，还是来自 StairMaster 的 Cross-Attention、SRU等架构设计。
- HIMLoco：基于混合内部模型的先进盲式运动策略，不使用本文的深度视觉处理机制。它用于检验在存在空隙和落脚风险时，视觉结构信息相对仅依赖本体感知与内部记忆是否必要。

**实验想回答的问题**

- 与视觉强化学习方法 Extreme Parkour、加入本文奖励后的 Extreme Parkour，以及无视觉的 HIMLoco 相比，StairMaster 能否在标准空心楼梯和随机混合楼梯上更可靠地到达目标并跨越更多台阶？
- 面向空心楼梯的主动感知与落脚奖励、Cross-Attention、空间感知循环单元（SRU）及仿真到现实深度噪声建模，是否分别对性能和真实部署能力具有必要作用？

**实验实现**

策略在 Isaac Gym 中训练，使用单张 NVIDIA RTX 4090 GPU。仿真比较覆盖平地、标准空心楼梯和随机混合楼梯，每种方法在每种地形上运行1000个回合。真实系统使用 Unitree Go2、以10 Hz输出深度流的 Intel RealSense D435，以及完全机载运行的 NVIDIA Jetson Orin NX；策略以50 Hz输出目标关节位置，再由低层PD控制器转换为电机力矩，其中刚度增益 Kp=40、阻尼增益 Kd=1。原文节选未说明随机种子、置信区间、统计显著性检验、训练步数或模型选择规则。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 去除Cross-Attention与SRU：以直接特征拼接替代Cross-Attention，并以标准两层LSTM替代SRU | 该变体已被纳入消融比较，但所给节选未明确报告其成功率、平均到达台阶比例或相对完整模型的下降幅度。 | 该消融联合移除了结构化视觉融合和空间感知时序记忆，用来测试完整感知—记忆模块是否优于简单拼接加通用LSTM。由于一次同时改变两个组件，即使性能下降，也只能说明二者的组合有效，不能分别归因于Cross-Attention或SRU；单独的“w/o SRU”变体才有助于进一步拆分贡献。 | Simulation Comparison and Ablation Study；数值据称见Table 1，但所给节选未包含表格行<br><span class="experiment-evidence">Ours w/o CA & SRU: Our method with Cross-Attention replaced by direct feature concatenation and SRU replaced by a standard two-layer LSTM.</span> |
| 不使用空心间隙惩罚与楼梯边缘惩罚的落脚奖励消融（Ours w/o r_foothold） | 该变体删除 r_hollow 与 r_edge，但所给节选未明确报告删除后任何指标的数值变化。 | 该消融针对精确落脚机制：r_hollow抑制脚落入空隙，r_edge抑制踩在踏板边缘。若完整模型显著更好，可支持几何风险感知奖励对安全落脚有贡献；但由于两项惩罚被同时删除，不能判断哪一项更关键。 | Simulation Comparison and Ablation Study；数值据称见Table 1，但所给节选未包含表格行<br><span class="experiment-evidence">Ours w/o r_foothold: Our method without the hollow-gap penalty r_hollow and the stair-edge penalty r_edge.</span> |

**定性案例**

- 真实部署采用Unitree Go2、RealSense D435和Jetson Orin NX，说明完整策略能够在机载算力与10 Hz深度感知条件下运行，并以50 Hz产生关节目标。摘要进一步声称机器人通过零样本迁移攀爬最高55°的空心楼梯；但所给实验节选未提供试验次数、成功率、楼梯几何尺寸或失败案例，因此该案例展示的是可行性，而不是可量化的真实世界可靠性。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Develops a reinforcement-learning locomotion framework for robust quadrupedal stair climbing with sim-to-real deployment.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`86438b21bf0f7e56d161b8c2832e2f9c6286435d8e468f70138eb620d6e067da`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
