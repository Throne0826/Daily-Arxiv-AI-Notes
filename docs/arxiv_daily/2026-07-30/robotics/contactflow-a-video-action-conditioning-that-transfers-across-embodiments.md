---
title: "[论文解读] ContactFlow: A video action conditioning that transfers across embodiments"
description: "[arXiv 2607.26579][机器人 / 具身智能] 本文提出以三维接触点随时间的轨迹作为跨具身动作条件，使同一视频世界模型能够联合学习人类与机器人示范，并在执行前预测和验证不同机器人形态的操作结果。"
arxiv_id: "2607.26579"
announcement_date: "2026-07-30"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.839419+00:00"
source_sha256: "6f749508fdcb846f47eb7465e3781382d064ff3737a10a6aed83f062ff39f624"
tags:
  - "机器人 / 具身智能"
  - "视频生成"
  - "多模态 VLM"
  - "视频世界模型"
  - "Contact Flow"
  - "具身无关动作表示"
  - "接触几何"
  - "可控视频生成"
  - "机器人操作"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2607.26579</p>

# ContactFlow: A video action conditioning that transfers across embodiments

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Sami Azirar, Enrico Pallotta, Jan Nogga, Jürgen Gall, Sven Behnke, Hermann Blum</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26579v1) · [PDF 下载](https://arxiv.org/pdf/2607.26579v1) · **关键词** 视频世界模型, Contact Flow, 具身无关动作表示, 接触几何, 可控视频生成, 机器人操作<br>


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

本文提出以三维接触点随时间的轨迹作为跨具身动作条件，使同一视频世界模型能够联合学习人类与机器人示范，并在执行前预测和验证不同机器人形态的操作结果。

**不用术语来说**：机器人若要在真正行动前先用视频模型“预演”，生成结果不仅要看起来逼真，还必须符合物体被接触、推动或抓取时的基本物理约束；但常见动作描述通常绑定某一种机械臂结构，或过度描述手和夹爪的外形，因而难以把人类示范中的交互经验迁移给不同形态的机器人。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 Contact Flow：将动作表示为执行者与目标物体之间三维接触点的时间轨迹，并投影到图像空间；该表示舍弃执行者的外观与运动链信息，以物体中心的接触几何作为人手和不同机器人可共享的条件信号。
- 基于 Contact Flow 构建跨具身视频世界模型及“提出—想象—验证—执行”流程：模型以混合的人类手物交互和机器人示范训练，生成候选动作的未来视频，再由视觉语言模型判断预演是否成功，仅将通过验证的轨迹交给机器人执行。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于机器人学习与可控视频生成的交叉领域。视频世界模型把当前场景及候选动作映射为未来视频，使机器人能够在真实执行前“想象”动作后果，并据此规划或验证操作；但画面逼真并不等于符合物理规律，抓取、推动等任务尤其取决于接触位置及其随时间的变化。本文关注的核心背景问题是：如何设计一种既能约束视频模型生成符合接触力学的物体运动，又不依赖特定手形、夹爪结构或机器人运动学的动作条件，从而联合利用人类手—物交互视频和不同机器人平台的数据。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视频世界模型（video world model）**

一种学习环境动态的生成模型：给定当前视觉观测和动作条件，预测随后可能出现的视频帧。机器人可把预测视频当作低成本模拟，在实际执行前比较候选动作的结果。

</div>
<div class="concept-item" markdown="1">

**动作条件化（action conditioning）**

将计划执行的动作编码为控制信号，输入视频生成模型以指定未来应如何演化。常见信号包括语言、关节状态、末端执行器状态、人体姿态、掩码、关键点和运动轨迹。

</div>
<div class="concept-item" markdown="1">

**具身无关表示（embodiment-agnostic representation）**

不绑定某一种身体形态、关节结构或末端执行器外观的动作表示。本文以演员与目标物体之间的三维接触点轨迹描述交互，使人手和不同机器人夹爪原则上能够共享同一种条件信号。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务是在物体操作场景中构建可跨具身迁移的动作条件视频世界模型。训练时，输入包括场景视频以及从人手—物体交互或遥操作机器人示范中提取的接触信息；接触信息被表示为演员与目标物体之间三维接触点随时间形成的轨迹，再投影到图像空间，用于条件化大规模视频生成模型。输出是与候选操作轨迹对应的未来交互视频，目标是同时保持时间与视觉连贯性，并更准确地反映接触所约束的物体运动。推理时，系统从机器人规划的抓取中读取夹爪与目标物体的三维接触点并投影到相机图像，以与训练阶段相同的表示生成候选执行结果；生成结果还可交由视觉—语言模型验证，只有被判断为成功的轨迹才进入真实执行。论文设定强调跨人类与机器人、跨机器人形态，以及对训练时未见物体和环境的零样本部署；不过所给章节尚未形式化说明相机标定、接触估计误差或动力学可观测性等具体假设。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Kinema4D**: 以时空机器人占据情况的4D点图表示机器人运动，可降低对原始动作接口的依赖，但仍编码执行者本身的几何形态；Contact Flow则只保留演员与物体之间的主动接触界面，以进一步削弱具身差异。
- **BridgeV2W**: 利用渲染的具身掩码引导视频在不同视角、场景和机器人平台间生成，但条件仍突出执行者的完整外形；本文改用局部接触点轨迹，试图让人手与不同夹爪共享同一操作描述。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

视频世界模型可用于在真实执行前模拟候选动作，从而支持规划、策略学习、数据扩增和安全验证。然而，视觉上连贯、逼真的生成视频未必遵守接触力学，模型可能让物体在没有合理接触的情况下移动。这样的“物理幻觉”会使预演结果无法可靠地指导机器人控制，尤其会妨碍对接触密集型操作结果的判断。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于关节或运动链的动作表示**：使用执行者各关节的位置、姿态或运动序列来条件化视频模型，能够细致表达某个机器人或人体如何运动。
- **基于执行者掩码或轮廓的动作表示**：用视频中手、夹爪或其他执行器的区域与外形变化描述动作，弱化对显式关节定义的依赖，并向生成模型提供执行者在图像中的运动信息。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 关节表示依赖特定运动链和形态：某种机械臂或人体骨架上的信号无法直接对应到具有不同关节布局、自由度或末端执行器的机器人，因此难以联合利用人类与异构机器人示范。
- 掩码或轮廓表示编码了执行者的完整形状，使模型容易关注手或夹爪“长什么样”，而不是其在何处与物体发生作用；它没有隔离决定操作结果的接触信息，可能削弱跨外观、跨具身迁移及物理结果预测。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种既能明确表达操作中的关键物理交互、又不绑定执行者外观和运动学结构的统一动作条件。这个条件还需能够以相同定义从人类视频和机器人计划中获得，使异构示范可共同训练一个世界模型，并让模型迁移到训练时未见的机器人形态、物体和场景。

</div>
<div markdown="1"><span>核心问题</span>

能否仅用执行者与目标物体之间接触点的三维时序几何来表征操作，并以此条件化视频世界模型，使其从人类和机器人数据中共同学习、跨具身预测较可信的操作结果，进而充当零样本机器人轨迹验证器？

</div>
<div markdown="1"><span>作者直觉</span>

物体并不直接“感知”操作者是人手、平行夹爪还是其他末端执行器；对物体运动更直接的因素，是力在物体什么位置、沿怎样的接触轨迹施加。Contact Flow 因而只保留接触位置随时间的变化，把执行者的外形、关节数量和运动链视为可丢弃信息。直观地说，不同身体只要以相近方式接触并带动物体，就可向视频模型提供同一种“交互说明书”，从而使人类示范中的接触经验可被机器人复用。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ContactFlow 将动作表示为“施力者与目标物体接触区域的三维轨迹”，而不是机器人关节指令、夹爪姿态或手部外观。每个时刻的条件由若干七维接触点组成：物体表面三维位置、到下一帧的三维位移以及置信度；这些点投影到图像平面后形成稀疏七通道控制视频。该表示保留直接引发物体变化的主动接触动力学，但不编码接触后产生的被动物体运动，因而不会把待预测结果提前泄露给生成器，并可统一描述人手和不同机器人形态的操作。
端到端流程分为训练与部署两部分。训练时，系统从人类视频和遥操作机器人数据中恢复目标物体、三维场景、手或夹爪及接触点，构造 Contact Flow，再用首帧和 Contact Flow 条件训练潜空间视频扩散 Transformer。部署时，从外部双目相机恢复目标物体的三维模型，根据候选末端执行器轨迹及夹爪 URDF 合成预期 Contact Flow；世界模型从噪声生成未来视频，用于预测该轨迹在真实场景中的结果。直观地说，模型不需要知道“是谁的手或哪款机器人在动”，只需要知道“物体哪里会被碰、接触区域接下来怎样移动”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 统一恢复场景、目标物体与施力者几何

系统通过 FoundationStereo 或 MapAnything 构建逐帧三维点图，并获得目标物体掩码及点云；人类数据使用 HaMeR/MANO 恢复手网格，机器人数据则利用标定、状态和 URDF 恢复夹爪几何。

<div class="method-step__io" markdown="1">

**输入**：RGB 视频序列；可选的双目图像、深度、相机标定、机器人状态与 URDF、任务文本，以及数据集已有的手部或物体网格。<br>
**输出**：相机坐标系中的逐帧点图、目标物体几何与掩码，以及手或机器人夹爪的位姿和几何表示。

</div>

**直观理解**：这一步先把二维视频整理成统一的三维舞台，明确物体在哪里、手或夹爪在哪里。后续接触估计因此不依赖某一种机器人的原始控制接口。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 估计并跟踪接触区域

人类数据结合 HACO 的手部接触预测、手物三维距离、二维掩码重叠和时间平滑；机器人数据依据前后夹指与物体的几何重叠估计可见及遮挡接触，并在夹爪闭合后用腕部刚体变换传播接触点，再以三帧 Hough 过滤器平滑对应关系。

<div class="method-step__io" markdown="1">

**输入**：目标物体点云与掩码、手网格或夹爪几何，以及相邻视频帧。<br>
**输出**：每帧位于物体表面的接触点、这些点到下一帧的三维位移，以及融合接触可信度、时间方向一致性和邻域密度的置信权重。

</div>

**直观理解**：系统寻找真正承受手或夹爪作用的物体表面区域，并跟踪这些区域如何移动。置信度会削弱孤立、方向不一致或几何上可疑的伪接触。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 编码 Contact Flow 条件视频

每个接触点被编码为七维向量，并通过相机内参投影到对应像素；七个属性写入稀疏七通道控制帧，沿时间堆叠为 Contact Flow 视频。

<div class="method-step__io" markdown="1">

**输入**：相机坐标系中的接触点位置、逐帧位移、置信权重和相机内参。<br>
**输出**：覆盖预测时域的稀疏时空条件 \(\mathbf{C}_{1:T}\)，可送入 ControlNet 分支或 VACE 视频条件单元。

</div>

**直观理解**：可以把它看成画在视频上的稀疏“接触箭头”：箭头起点表示碰哪里，方向与长度表示接触表面下一步怎样移动，亮度式权重表示估计有多可靠。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 训练条件潜空间视频世界模型

冻结的视频 VAE 将视频编码为潜变量；训练 DiT 速度网络，在首帧潜变量和 Contact Flow 条件下，用流匹配目标预测从噪声指向真实未来视频潜变量的速度。Contact Flow 分别通过 ControlNet 或 VACE 注入，以检验表示是否独立于特定控制架构。

<div class="method-step__io" markdown="1">

**输入**：真实视频、首帧、对应的 Contact Flow 视频和随机高斯噪声。<br>
**输出**：条件生成模型 \(p_\theta(\mathbf{z}_{1:T}\mid z_0,\mathbf{C}_{1:T})\)，能够由首帧和预定接触运动生成未来潜变量。

</div>

**直观理解**：训练过程教模型把随机噪声逐渐推向一个与当前场景和接触动作一致的未来视频。使用两种条件注入方式，是为了区分收益来自 Contact Flow 本身还是某个特定网络结构。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 逐帧 Contact Flow 接触点编码

$$
\mathbf{C}_{t}=\big\{\mathbf{c}_{t}^{(i)}\big\}_{i=1}^{N_t},\qquad \mathbf{c}_{t}^{(i)}=\big(x,y,z,\Delta x,\Delta y,\Delta z,w\big)\in\mathbb{R}^{7}
$$

**符号说明**

- $\mathbf{C}_t$：时刻 \(t\) 的全部 Contact Flow 接触点集合。
- $\mathbf{c}_t^{(i)}$：时刻 \(t\) 的第 \(i\) 个七维接触点描述。
- $N_t$：时刻 \(t\) 检测到的接触点数量，可随时间变化。
- $(x,y,z)$：接触点在相机坐标系中的物体表面三维位置。
- $(\Delta x,\Delta y,\Delta z)$：该接触点到下一帧的三维位移，即局部接触流。
- $w$：范围为 \([0,1]\) 的接触置信权重。

<div class="equation-explanation" markdown="1">

**直观理解**：该式规定模型看到的最基本动作单位：接触发生在哪里、该接触区域下一帧往哪里移动，以及该估计是否可信。位置和位移共同描述主动交互，置信权重则降低噪声接触对条件和训练的影响。<br>
**原文位置**：第3.1节，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 潜空间流匹配训练目标

$$
\mathbf{u}_{\tau}=(1-\tau)\boldsymbol{\epsilon}+\tau\mathbf{z}_{1:T},\qquad \mathcal{L}_{\mathrm{FM}}=\mathbb{E}_{\mathbf{z}_{1:T},\boldsymbol{\epsilon},\tau}\left[\left\|v_{\theta}(\mathbf{u}_{\tau},\tau,z_0,\mathbf{C}_{1:T})-(\mathbf{z}_{1:T}-\boldsymbol{\epsilon})\right\|_2^2\right]
$$

**符号说明**

- $\mathbf{z}_{1:T}$：视频 VAE 编码得到的真实未来帧潜变量序列。
- $\boldsymbol{\epsilon}$：与未来潜变量形状相同、采样自 \(\mathcal{N}(0,I)\) 的高斯噪声。
- $\tau$：从 \(\mathcal{U}(0,1)\) 采样的插值时间。
- $\mathbf{u}_{\tau}$：噪声与真实未来潜变量在时间 \(\tau\) 处的线性插值状态。
- $v_{\theta}$：参数为 \(\theta\) 的 DiT 速度预测网络。
- $z_0$：保持干净、不加噪的首帧潜变量条件。
- $\mathbf{C}_{1:T}$：预测时域内的 Contact Flow 条件序列。
- $\mathcal{L}_{\mathrm{FM}}$：速度预测与目标速度之间的均方流匹配损失。

<div class="equation-explanation" markdown="1">

**直观理解**：系统先在纯噪声和真实未来视频潜变量之间随机取一个中间点，再要求网络预测把噪声推向真实未来的方向。由于预测同时读取首帧和 Contact Flow，学到的速度场不仅要生成自然视频，还要生成与指定接触动作一致的后续变化。<br>
**原文位置**：第3.2节，公式(3)；插值定义紧邻公式(3)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练仅优化条件 DiT 及相应的条件注入模块，使其最小化潜空间流匹配损失；视频 VAE 编码器在原文中明确为冻结状态，ControlNet/VACE 所依附的视频生成主干也按相应机制冻结。低置信接触点对条件信号和训练损失的贡献更小，从而减少人手接触预测、遮挡区域几何和逐帧对应误差带来的监督噪声。优化后的网络近似一个以首帧和 Contact Flow 为条件的速度场，推理时可通过数值积分把随机噪声转换为未来视频潜变量。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Contact Flow 表示**

每帧表示为可变数量的七维接触点集合，包含物体表面三维位置、到下一帧的局部三维位移和置信权重。表示只描述接触界面及其运动，不纳入随后发生的被动物体运动，也不包含手形、机器人外观、关节动作或具体控制空间。

> 直观理解：它把“动作”压缩成物体真正感受到的接触，而不是执行动作的身体形式。因此，人手和不同夹爪只要在同一位置产生相同接触运动，就能向模型提供相同的条件。

**2. Contact Flow 条件视频生成器**

主干是采用视频 VAE 的潜空间视频扩散 Transformer；首帧潜变量保持干净并作为观测条件，未来帧潜变量通过流匹配学习。ControlNet 版本用可训练并行控制分支向冻结主干注入接触特征，VACE 版本则由 Video Condition Unit 编码条件，并经分布在 Transformer 层中的 Context Adapter 注入。

> 直观理解：主干负责生成看起来合理的未来，条件模块负责约束生成内容必须遵循指定接触轨迹。两种注入结构共享完全相同的 Contact Flow 输入。

**3. 部署时三维场景恢复与接触合成**

系统利用 FoundationStereo 获得度量点图，以 VLM、GroundingDINO 和 SAM3 定位目标，再用 SAM 3D-Objects 初始化三维 Gaussian Splat。其姿态和尺度经过 PCA、trimmed ICP、可微渲染比较及 Gaussian 不透明度与颜色精调，并仅接受同时改善掩码 IoU、深度内点比例和 RGB 余弦相似度的阶段结果。

> 直观理解：部署时没有真实未来接触标签，所以必须先建立足够准确的物体三维替身，再让虚拟夹爪沿候选轨迹运动以推算会碰到哪里。严格的渲染一致性门控用于避免错误三维模型产生误导性的接触条件。

**训练与推理**

训练阶段汇合人类操作视频与遥操作机器人片段，并把两类数据处理为相同的物体掩码、点图和 Contact Flow。人类管线以 HaMeR/MANO、HACO 和手物几何关系确定接触；机器人管线利用相机标定、URDF、状态、物体点云以及前后夹指的可见性关系确定接触，并丢弃机器人渲染与检测掩码明显不一致或 RobotInter 判断严重冲突的样本。真实视频由冻结 VAE 编码，未来潜变量与高斯噪声线性插值，网络在干净首帧和 Contact Flow 条件下学习目标速度。
推理阶段只要求候选末端执行器轨迹和恢复出的真实场景模型，不要求产生该轨迹的策略具有特定动作空间。系统从外部双目相机和初始帧恢复目标物体的度量三维模型，将轨迹作用于夹爪 URDF，并按训练时机器人数据的规则合成预期 Contact Flow；随后从未来潜空间噪声出发，在 \(z_0\) 与 \(\mathbf{C}_{1:T}\) 条件下积分速度场，得到 \(\hat{\mathbf{z}}_{1:T}\)，最后通过 VAE 解码器生成 \(\hat{\mathbf{x}}_{1:T}\)。论文整体部署管线可再由视觉语言模型检查生成结果，然后决定是否执行候选动作，但该验证器不属于 Contact Flow 世界模型本身。

**复现信息**

公平理解方法所需的关键实现信息包括：Contact Flow 是投影到图像平面的稀疏七通道时空控制视频；点的置信度综合基础接触可信度、邻域位移方向一致性和局部密度。模型采用潜空间视频 DiT，并分别实现基于 ControlNet 和 VACE 的条件注入；文中实验涉及 Wan 2.1 14B、Wan 2.2 5B 与 Wan 2.2 14B 主干，但所给节选未明确报告训练轮数、优化器、学习率、采样积分器或训练硬件。机器人接触对应使用三帧窗口的 Hough 平滑；部署场景至少假设一台已标定外部双目相机、夹爪 URDF 及候选末端轨迹。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- DROID：机器人操作视频数据集，既用于训练，也用于文中明确描述的定量评测。评测集包含25个留出片段；每个片段为49帧、8 FPS、分辨率832×480。其作用是检验模型对机器人操作结果的视觉预测质量。原文未明确报告训练样本规模及留出片段的具体划分规则。
- Taste-ROB与TACO：作为机器人交互训练数据加入混合训练集，用于扩展机器人动作、物体和场景的覆盖范围。给定实验节选未报告二者各自的样本规模、训练划分或单独测试结果。
- OakInk与LIBERO：OakInk提供人类手—物体交互数据，LIBERO提供机器人操作数据；二者与其他数据共同训练，使Contact Flow能够从人类和不同机器人载体中学习共享的物体接触表示。给定节选未报告各自规模、划分及分数据集结果。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**DreamSim**

感知相似度指标，用学习到的视觉表征衡量预测帧与真实帧在语义和视觉感知上的差异。本文将其作为Q1的主要指标，并在移除机器人手臂或人手后的区域上计算，以集中评估物体和场景结果。 （越低越好；距离越小表示预测与真实视频在感知表征上越接近。）

</div>
<div class="metric-item" markdown="1">

**FVD**

Fréchet Video Distance，全帧视频分布指标，用于比较生成视频与真实视频在时空特征分布上的差异，侧重整体真实性和时间一致性，而不是逐像素对齐。 （越低越好；较小的分布距离通常表示生成视频整体更接近真实视频集合。）

</div>
<div class="metric-item" markdown="1">

**预测准确率（prediction accuracy）**

Q2的主要指标：比较VLM对想象 rollout 的成功或失败判断与真实机器人执行结果是否一致。真实执行只有在完成抓取与指定区域放置、且没有碰倒或掉落物体等意外后果时才算成功。 （越高越好；准确率越高，表示想象视频加VLM组成的验证器越能正确预判候选轨迹的真实结果。）

</div>

</div>

</div>

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

- TesserAct：仅以任务语言描述为条件，不接受指向某条具体轨迹的几何控制信号。该比较用于判断显式接触轨迹条件是否比纯语言条件更适合预测特定候选动作的结果；但两者的控制信息量不同，因此不能将差异完全归因于表示形式。
- CTRL-World：使用低维动作嵌入作为条件，该嵌入绑定训练机器人的动作空间和具体载体。它用于对比Contact Flow的跨载体设计，但因其本身不支持零样本迁移，并非完全同等条件下的竞争者。
- Kinema4D：以完整机器人的4D点图为条件，编码整个执行者的几何与运动，而Contact Flow只编码执行者与目标物体之间的接触位置轨迹。两者都可进行零样本使用，因此Kinema4D是最直接的主要竞争方法，用于检验“只保留接触界面”是否比“建模完整执行者”更适合跨载体预测。
- 三种骨干与控制配置：Wan2.1-14B + VACE、Wan2.2-5B + ControlNet、Wan2.2-14B + ControlNet。它们不是独立任务方法，而是用于检查结论是否依赖某一个视频生成骨干、模型规模或条件注入机制。

**实验想回答的问题**

- Q1：Contact Flow 能否作为有效的视频生成条件，使世界模型对机器人操作过程给出准确且时序连贯的预测？
- Q2：在未见过的真实场景中，世界模型对候选轨迹结果的预测是否足够可靠，从而充当零样本验证器，在执行前判断轨迹能否完成任务且不会造成碰倒、掉落等意外后果？

**实验实现**

真实机器人平台为固定式Franka Panda机械臂，使用单个外部RGBD相机。部署时只离线恢复一次场景并构建符号化数字孪生：由FoundationStereo估计度量深度，用SAM3获得物体掩码，再拟合位于机器人基坐标系中的度量物体网格，并通过可微优化细化刚体位姿和统一尺度。π0.5视觉—语言—动作策略先在数字孪生中提出末端执行器轨迹；系统将轨迹转换为预期Contact Flow，由视频世界模型生成操作结果，再由Gemini判断任务是否完成，只有通过判断的轨迹才在真机上开环执行。视频评测对每个数据集使用25个留出片段，每段49帧、8 FPS、832×480。PSNR、SSIM、LPIPS及DreamSim在执行者掩蔽区域上计算：预测和真值均移除机器人手臂或人手，训练损失也使用相同掩码；机器人掩码来自RoboSeg，人类掩码来自SAM2。FID与FVD则在完整画面上计算。节选未报告优化器、学习率、训练轮数、随机种子、置信区间或显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出跨具身的接触流动作表示，并训练视频生成世界模型用于机器人操作的想象、验证与执行。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`6f749508fdcb846f47eb7465e3781382d064ff3737a10a6aed83f062ff39f624`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
