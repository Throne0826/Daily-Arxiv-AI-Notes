---
title: "[论文解读] SpatialQuery: Benchmarking Geometry-Grounded Multi-Instance Spatial Reasoning in Vision-Language Models"
description: "[arXiv 2608.01709][VLM Reasoning] 本文针对单张RGB图像中的多实例度量空间推理缺口，研究如何找出某类别中距离参考物体最近的可见实例，并可靠估计二者在重力对齐地面上的实际距离。"
arxiv_id: "2608.01709"
announcement_date: "2026-08-04"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:01:34.065047+00:00"
source_sha256: "749e47ec8c54d840a89cbadf0462224887d11d82277099d9311946ce9308122a"
tags:
  - "VLM Reasoning"
  - "LLM 评测"
  - "LLM Reasoning"
  - "多模态 VLM"
  - "视觉语言模型"
  - "度量空间推理"
  - "最近实例距离查询"
  - "多实例推理"
  - "单目几何"
  - "重力对齐地平面距离"
  - "鸟瞰图"
  - "几何不确定性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.01709</p>

# SpatialQuery: Benchmarking Geometry-Grounded Multi-Instance Spatial Reasoning in Vision-Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Hai Nguyen, Tung Vu, Cong Tran</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Hai Nguyen, Tung Vu, and Cong Tran are with the Posts and Telecommunications Institute of Technology, Hanoi, Vietnam</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01709v1) · [PDF 下载](https://arxiv.org/pdf/2608.01709v1) · **关键词** 视觉语言模型, 度量空间推理, 最近实例距离查询, 多实例推理, 单目几何, 重力对齐地平面距离, 鸟瞰图, 几何不确定性<br>
**项目页**: [https://namhai1810.github.io/SpatialQuery/](https://namhai1810.github.io/SpatialQuery/)

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

本文针对单张RGB图像中的多实例度量空间推理缺口，研究如何找出某类别中距离参考物体最近的可见实例，并可靠估计二者在重力对齐地面上的实际距离。

**不用术语来说**：面对“哪把椅子离电视最近，以及相距多少米”这类问题，模型不能只识别椅子和电视，还必须找到所有可见椅子、避免漏检或重复计数、推断它们在真实房间中的位置，再比较各自到电视的距离。普通图像中的远近会受到透视、相机倾斜和物体高度影响，而且单张图像恢复出的深度本身并不可靠，因此视觉上看起来最近的物体未必在地面上真的最近。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将最近实例距离查询定义为一个独立的多实例空间推理问题，使评测同时覆盖可变数量候选实例的汇总、最近实例选择和重力对齐地面距离估计，并构建了相应的大规模RGB问答基准。
- 作者提出无需任务微调的SpatialQuery框架：先从单张RGB图像恢复实例级度量位置，再用Scene Cubifying生成规范化鸟瞰表示，并通过UA-CoT把实例几何不确定性纳入视觉语言模型的推理过程。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于视觉语言模型的度量空间推理研究。此类系统不仅要识别图像中的物体及其语义类别，还要使回答符合真实世界的几何关系；这对具身智能、辅助系统以及需要导航或物体交互的应用尤其重要。现有视觉语言模型通常具备较强的语义理解能力，但从单张透视 RGB 图像推断精细的物理距离仍不可靠：相机倾斜、透视畸变和物体离地高度会使图像中的表观间隔偏离真实水平距离，而单目深度本身也存在尺度与定位不确定性。本文因此关注一种更严格的场景：查询不是给定两个固定物体后估计距离，而是要求模型先找全某一类别的多个可见实例，再选出离唯一参考物体最近的实例，并估计二者在重力对齐地面上的绝对距离。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉语言模型（VLM）**

能够联合处理图像和自然语言的模型，可根据图像内容回答文本问题。本文考察的重点不是一般物体识别，而是模型能否依据恢复出的场景几何进行实例比较和米制距离推理。

</div>
<div class="concept-item" markdown="1">

**重力对齐的地平面距离**

先依据重力方向确定水平地面，再把物体位置投影到该平面并计算距离；它关注人在室内地面上移动时对应的水平间隔，而非图像像素距离或物体中心之间包含高度差的三维直线距离。

</div>
<div class="concept-item" markdown="1">

**鸟瞰图（BEV）**

从场景上方向下观察的规范化表示，可减弱第一人称图像中的透视和视角偏差。本文的 BEV 是供模型比较实例位置的紧凑视觉接口，实际度量距离仍由保留的地平面坐标计算。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文将任务定义为最近实例距离查询（CIDQ）。输入仅包含一张室内 RGB 图像和一条自然语言查询，例如“离电视最近的椅子有多远”；查询涉及一个唯一的参考物体和一个实例数量可变的候选类别。系统需要检测该类别的全部可见候选实例且避免重复，恢复各实例相对于参考物体的米制地平面位置，比较候选距离，选择最近实例，并输出其与参考物体之间的重力对齐地平面距离；基准还支持判断候选是否满足给定邻近关系的 proximity decision 任务。评测模型不能使用真实相机参数或三维标注，这些信息只用于离线构造 SpatialQuery-1M 的答案；模型在严格零样本、无需任务专用微调的设定下，仅依据 RGB 图像和文本问题完成推理。该问题同时检验候选集合聚合、最近实例选择与绝对距离估计，因此比预先指定固定物体对的距离问答更容易受到漏检、重复检测、透视失真和单目几何不确定性的影响。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\sigma_i^{\mathrm{BEV}}$**

第 $i$ 个重建实例在鸟瞰图坐标中的几何离散度或不确定性；UA-CoT 将它与重建布局一同提供给视觉语言模型，使最近实例选择和距离预测能够考虑单目重建证据的可靠程度。

</div>

</div>

**直接相关的工作**

- **SpatialVLM 与 SpatialRGPT**: 二者通过监督微调或深度感知组件增强几何落地能力，但原文指出，这类方法主要针对预先定义的物体对，没有联合处理可变规模候选集合、最近实例选择和由几何估计产生的不确定性；CIDQ 正是把这三项能力放入同一任务中评测。
- **SpatialPIN**: SpatialPIN 属于利用几何先验改进空间推理的相关方法，并体现了训练自由路线的部分思路；与本文不同，它仍主要面向固定物体对，未同时覆盖多实例最近对象搜索以及将逐实例几何不确定性传递给推理模型。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

具身智能、辅助系统和交互式应用不仅要知道场景中“有什么”，还要依据真实尺度决定“哪个目标最近、距离多远”，以支持导航和物体交互。最近实例距离查询尤其要求系统在同类物体存在多个实例时做出可靠选择；任何候选漏检、重复检测、位置偏差或距离比较错误，都可能把后续行动引向错误目标。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **固定物体对的空间距离估计与相关基准**：这类方法通常给定或预设一对目标物体，直接估计二者的空间关系或距离，重点考查单个物体对的定位与度量，而不要求模型先遍历同一类别的全部可见实例并从中选出最近者。
- **基于单目深度或物体位置重建的确定性空间推理**：这类系统从单张RGB图像估计深度和物体位置，再将估计结果作为确定坐标用于距离计算或语言推理；空间微调模型也往往围绕固定物体对学习答案，而没有显式传播每个实例的几何可靠程度。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 固定物体对设定没有联合考查候选集合是否完整且无重复、模型能否处理数量可变的同类实例，以及能否在全部候选中正确选择最近者；因此，在固定配对任务上获得的空间能力不一定能迁移到最近实例距离查询。
- 透视RGB图像与室内水平地面几何并不天然对齐，相机倾斜、透视畸变和物体离地高度可能令相似图像布局对应不同实际距离；同时，单目深度存在不可消除的歧义。若把估计坐标当作完全确定的事实，局部离群点或全局深度偏差会导致错误且过度自信的最近实例判断。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种面向单张RGB输入、无需任务专用训练，却能在统一流程中完成全部同类候选实例汇总、最近实例选择、重力对齐地面距离估计，并让推理显式感知几何不确定性的方案；相应地，也缺少能够大规模联合评测这些能力的基准。

</div>
<div markdown="1"><span>核心问题</span>

能否仅依据单张RGB图像和自然语言查询，在不微调视觉语言模型、不修改其架构的条件下，恢复足够稳定的实例级度量几何，使模型从数量可变的同类候选中识别距离唯一参考物体最近的实例，并可靠估计二者的地面平面距离？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是先把视觉问题改写成更适合比较的几何问题：将检测到的物体投影到统一朝向的鸟瞰平面，并画成大小一致、按类别编码的方块，使模型不再被纹理、原图透视和物体外观尺寸干扰，而主要观察相对地面位置。随后，把各实例位置估计的分散程度作为不确定性提供给推理链，相当于提醒模型哪些几何证据可信、哪些候选的距离比较应更谨慎。不过，这种设计只能抑制局部异常和暴露歧义，不能补回底层深度估计中完全缺失的信息。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SpatialQuery 是一个无需任务微调、也不修改视觉语言模型架构的单图空间推理框架。其输入是一张室内 RGB 图像 $I$ 和自然语言查询 $Q$；系统先解析候选类别 $C_q$、唯一参考类别 $C_r$ 以及可选阈值 $\tau$，再检测并分割所有相关实例。随后，Depth Pro 从 RGB 图像估计度量深度和相机内参，系统把实例掩码内的像素反投影成三维点云，通过基于中位数绝对偏差的 RANSAC 去除背景深度和边界噪声，并校正相机俯仰角，最终得到每个实例在重力对齐地面平面上的二维坐标 $\hat{\mathbf{g}}_i$ 及几何离散度 $\sigma_i^{\mathrm{BEV}}$。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段一：查询解析与实例语义落地

Qwen-VL 从 $Q$ 中解析候选类别 $C_q$、参考类别 $C_r$，并在 T2 中解析阈值 $\tau$；GroundingDINO 检测所有可见候选实例和参考实例，SAM 将保留的检测框转换为实例掩码。对于应当唯一的参考类别，系统执行类别内非极大值抑制并仅保留置信度最高的参考框 $b_r$。

<div class="method-step__io" markdown="1">

**输入**：单张 RGB 图像 $I$ 和自然语言查询 $Q$。<br>
**输出**：检测实例集合 $\mathcal{S}_0=\{(b_i,C_i,m_i)\}$，其中 $b_i$、$C_i$ 和 $m_i$ 分别表示第 $i$ 个实例的检测框、类别和像素掩码。

</div>

**直观理解**：这一步先弄清问题在问“哪一类物体离哪个参考物最近”，再把图中每个相关物体单独圈出。掩码比矩形框更精确，可减少后续深度计算混入背景像素的风险。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段二：单目度量几何重建

系统从深度几何估计地平线行 $v_h$，进而获得相机俯仰角 $\hat{\phi}$；对每个掩码内深度为正的像素 $(u,v)$，利用内参逆矩阵和预测深度将其反投影为相机坐标系中的三维点 $\mathbf{p}_{u,v}^{\mathrm{cam}}$。

<div class="method-step__io" markdown="1">

**输入**：图像 $I$、实例掩码 $m_i$，以及 Depth Pro 估计的深度图 $\hat{\mathbf{D}}$ 和相机内参 $\hat{\mathbf{K}}$。<br>
**输出**：每个实例的原始度量点云 $\mathcal{P}_i^{\mathrm{cam}}$、实例深度样本 $\mathcal{D}_i$ 和相机俯仰角估计 $\hat{\phi}$。

</div>

**直观理解**：深度网络为每个像素估计它离相机多远，内参则描述相机如何把三维世界投到图像上；二者结合后，可把二维掩码恢复成以米为单位的三维点集合。俯仰角用于纠正相机向下或向上拍摄导致的地面方向倾斜。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段三：稳健定位与不确定性估计

系统以深度中位数和中位数绝对偏差 MAD 构造实例自适应阈值，通过一维 RANSAC 选择占比最大的深度模态，再用共识集的中位数进行第二次异常点过滤。过滤点云的逐坐标中位数给出稳健中心，经旋转矩阵 $\mathbf{R}_{\hat{\phi}}$ 校正俯仰后投影到地面平面；旋转后点集协方差迹的平方根被用作几何离散度。

<div class="method-step__io" markdown="1">

**输入**：每个实例的深度样本 $\mathcal{D}_i$、原始点云 $\mathcal{P}_i^{\mathrm{cam}}$ 和俯仰角 $\hat{\phi}$。<br>
**输出**：每个实例的重力对齐地面坐标 $\hat{\mathbf{g}}_i\in\mathbb{R}^2$ 和实例级几何不确定性代理 $\sigma_i^{\mathrm{BEV}}$。

</div>

**直观理解**：物体掩码常会夹带墙面、地面或远处背景，直接求平均位置容易被少数错误深度拖偏；RANSAC 寻找最一致的一簇深度点，中位数进一步降低异常值影响。$\sigma_i^{\mathrm{BEV}}$ 越大，表示该物体的有效三维点在地面上越分散，因此其位置越不可靠，但它不是经过统计校准的置信区间。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段四：Scene Cubifying 鸟瞰抽象

系统以统一的场景级归一化将实例坐标映射到 $512\times512$ 的重力对齐鸟瞰图，并把所有物体绘制为尺寸一致、按类别着色的方块，以对比边框突出参考实例。鸟瞰图像 $\hat{I}_{\mathrm{BEV}}$ 仅作为视觉上下文，数值距离不由其像素间距换算，而是始终由底层米制坐标计算。

<div class="method-step__io" markdown="1">

**输入**：全部实例的地面坐标 $\hat{\mathbf{g}}_i$、类别 $C_i$ 和参考实例索引 $r$。<br>
**输出**：规范化鸟瞰图 $\hat{I}_{\mathrm{BEV}}$ 及与其对应的结构化实例几何。

</div>

**直观理解**：这相当于把透视照片改画成简化的房间俯视图：忽略物体外观、大小和透视缩放，只突出候选物与参考物的相对位置。统一大小的方块可避免模型把“图上看起来更大”错误理解为“实际更近”。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 掩码像素的度量三维反投影

$$
\mathbf{p}_{u,v}^{\mathrm{cam}}=\hat{D}_{v,u}\,\hat{\mathbf{K}}^{-1}\begin{bmatrix}u&v&1\end{bmatrix}^{\!\top},\qquad (u,v)\in\Omega_i^{+}
$$

**符号说明**

- $\mathbf{p}_{u,v}^{\mathrm{cam}}$：像素 $(u,v)$ 在相机坐标系中的三维度量点。
- $\hat{D}_{v,u}$：Depth Pro 对像素 $(u,v)$ 预测的正值米制深度。
- $\hat{\mathbf{K}}$：预测的相机内参矩阵，包含焦距和主点。
- $(u,v)$：图像像素坐标，其中 $u$ 向右增大、$v$ 向下增大。
- $\Omega_i^{+}$：实例 $i$ 的掩码内具有正深度预测的有效像素集合。

<div class="equation-explanation" markdown="1">

**直观理解**：齐次像素向量先经内参逆矩阵转换成相机射线方向，再乘以预测深度，得到以米为单位的三维位置。这是系统从二维分割结果过渡到可计算真实距离的核心步骤。<br>
**原文位置**：第 IV-C 节，式 (10)

</div>

</div>

<div class="equation-block" markdown="1">

#### 最近实例距离选择与查询不确定性聚合

$$
\hat{d}_{q,i}=\left\|\hat{\mathbf{g}}_i-\hat{\mathbf{g}}_r\right\|_2,\quad \hat{i}_q=\operatorname*{arg\,min}_{i\in\mathcal{I}_q}\hat{d}_{q,i},\quad \hat{d}_q=\hat{d}_{q,\hat{i}_q},\quad \sigma_q=\sqrt{\left(\sigma_{\hat{i}_q}^{\mathrm{BEV}}\right)^2+\left(\sigma_r^{\mathrm{BEV}}\right)^2}
$$

**符号说明**

- $\hat{\mathbf{g}}_i$：候选实例 $i$ 的重力对齐地面平面坐标。
- $\hat{\mathbf{g}}_r$：唯一参考实例的重力对齐地面平面坐标。
- $\mathcal{I}_q$：所有类别等于查询候选类别 $C_q$ 的检测实例索引集合。
- $\hat{d}_{q,i}$：候选实例 $i$ 与参考实例之间的预测地面欧氏距离。
- $\hat{i}_q$：预测的最近候选实例索引。
- $\hat{d}_q$：最近候选与参考实例之间的预测距离。
- $\sigma_i^{\mathrm{BEV}}$：实例 $i$ 在地面平面上的几何离散度，即实例级不确定性代理。
- $\sigma_q$：由被选候选和参考实例的离散度按平方和开根号合成的查询级不确定性。

<div class="equation-explanation" markdown="1">

**直观理解**：系统先计算每个同类候选到参考物的米制地面距离，再取最小值，因此同时完成多实例聚合、最近实例识别和距离估计。最后把距离两端的位置离散度合并；这能反映几何输入是否稳定，但作者明确指出它不是统计意义上校准过的置信区间。<br>
**原文位置**：第 IV-F 节，式 (18) 和式 (19)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。SpatialQuery 是 training-free、plug-and-play 推理框架，没有针对 CIDQ 的损失函数、梯度优化或参数更新；Qwen-VL、GroundingDINO、SAM、Depth Pro 和最终 VLM 均以已有能力直接使用。式 (18) 的最小距离选择和式 (20) 的阈值判断是确定性推理规则，不是训练目标；UA-CoT 只是通过结构化提示规定计算过程。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 度量几何重建与俯仰校正**

Depth Pro 在不提供真实深度或相机参数的条件下，从 $I$ 同时预测米制深度图 $\hat{\mathbf{D}}$ 和内参矩阵 $\hat{\mathbf{K}}$。系统从地平线估计 $\hat{\phi}$，将掩码像素反投影到相机坐标系，再以 $\mathbf{R}_{\hat{\phi}}$ 旋转到重力对齐坐标系，使 CIDQ 距离只在地面平面的横向和前向坐标上计算。

> 直观理解：CIDQ 要求的是现实中的米制地面距离，而不是图像像素距离。该模块负责从一张普通照片恢复可用于测量的坐标，并消除相机倾斜对俯视位置的系统性影响。

**2. MAD-RANSAC 稳健深度筛选**

每个实例先以深度中位数估计中心，以 MAD 估计自适应深度尺度；一维 RANSAC 从 $K_{\mathrm{iter}}$ 个假设中选择共识像素最多的主深度模态，并围绕共识中位数执行第二次裁剪。最终以过滤点云的逐坐标中位数定位实例，以地面投影点集协方差迹的平方根定义 $\sigma_i^{\mathrm{BEV}}$。

> 直观理解：检测和分割并不保证掩码里的所有像素都属于物体，因此需要从混杂深度中找出最稳定的主体表面。该过程既产生更抗噪的位置，也把剩余点的分散程度转化为后续推理可见的可靠性信号。

**3. Scene Cubifying 与 UA-CoT**

Scene Cubifying 将几何坐标渲染为类别编码、等尺寸方块组成的规范化 BEV；UA-CoT 同时接收该 BEV 和结构化集合 $\mathcal{U}$，显式计算候选距离、执行最小值选择，并聚合候选与参考实例的不确定性。推理阶段不再提供原始 RGB 图像，从输入层面约束模型依据地面几何而非外观线索作答。

> 直观理解：BEV 让模型容易看清“谁在谁旁边”，结构化坐标则负责精确算米数，两者承担不同作用。UA-CoT 把多实例比较拆成可检查的计算步骤，并提醒模型哪些坐标可能不稳定。

**训练与推理**

不存在任务专用训练阶段。完整推理从 $(I,Q)$ 开始：解析实体角色，检测并分割相关实例，估计深度、相机内参和俯仰角，将每个实例恢复为三维点云；随后使用 MAD-RANSAC 筛除错误深度，计算重力对齐坐标与实例离散度，并生成 Scene Cubifying BEV。最终 VLM 只接收 BEV、实例坐标、类别、参考标记和不确定性；T1 枚举候选距离并返回 $\hat{d}_q\pm\sigma_q$，T2 进一步计算 $\hat{y}_{q_\tau}=\mathbf{1}[\hat{d}_q\leq\tau]$。其中 VLM 负责按提示组织和输出推理，但数值距离来自底层坐标，而不是从 BEV 像素比例或原始 RGB 外观中估算。

**复现信息**

公平复现所需的关键配置包括：输入仅为单张室内 RGB 图像和自然语言查询，推理时不提供真实深度、相机参数或多视图；Depth Pro 同时估计度量深度和内参；GroundingDINO 与 SAM 分别承担检测和实例分割；参考类别经类别内非极大值抑制后仅保留最高置信度框。BEV 画布为 $512\times512$，所有实例共享场景级归一化并绘制成统一尺寸的类别编码方块，参考实例使用对比边框。必须保留的解释边界是：BEV 像素距离不用于米制测量，$\sigma_i^{\mathrm{BEV}}$ 和 $\sigma_q$ 只是几何可靠性代理而非校准置信区间；RANSAC 的具体采样次数、阈值参数和退化情形处理在所给正文中未展开，原文称其位于补充材料。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- SpatialQuery-1M是主要基准，共含1,064,022个问答对，来自200个室内场景的73,924帧RGB图像，覆盖315个物体类别。其中T1包含659,786条最近实例地面距离估计记录，占62.0%；T2包含404,236条阈值邻近判断记录，占38.0%。正式实验从中固定抽取5,000条T1查询和5,000条T2查询，覆盖全部200个场景，并按物体类别、地面距离及任务相关因素分层采样；它用于统一比较所有方法，而不是训练或微调模型。
- MM-Spatial的室内子集是SpatialQuery-1M的直接数据源，提供实例级三维标注和标定相机几何。其真实三维质心与相机参数仅用于离线筛选、匹配和生成答案，不会作为被测模型的推理输入，因此评测考察的是RGB条件下的空间推理，而不是读取真实几何。
- CA-1M是MM-Spatial场景的上游来源，包含1,000多个室内场景和439K个标注物体，覆盖卧室、客厅、厨房、办公室、走廊和餐厅等房型。它主要说明场景及物体分布的来源；原文未报告在CA-1M上单独进行训练或测试。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Floor-MAE**

T1中有效原图距离预测与真实重力对齐地面距离之间的平均绝对误差，单位为米。它直接衡量连续距离估计的典型数值偏差，但会受到少量极端错误的显著影响；无效、缺失或不可解析的原图预测不进入该指标。 （越低越好，因为更小的平均绝对误差表示预测距离更接近真实地面距离。）

</div>
<div class="metric-item" markdown="1">

**Acc@0.2m（以及相对误差Acc@10%）**

T1的容差准确率：Acc@0.2m检查预测是否落在真实距离上下0.2米的固定误差范围内，Acc@10%检查是否满足相对误差阈值。准确率还采用黑图健全性过滤：方法必须在原图和同尺寸黑图上都给出有效输出、原图回答正确且黑图回答错误，才获得该查询的分数；分母固定为全部5,000条查询。 （越高越好，因为它表示更多查询在规定误差容限内正确，并且答案不能在没有视觉信息的黑图上仍然成立。）

</div>
<div class="metric-item" markdown="1">

**Unc-Acc@0.2m / Unc-Acc@0.3m**

T1的不确定性感知准确率，将距离预测是否在指定米制容差内与方法给出的可靠性信息结合。SpatialQuery使用几何支持点在BEV地面上的离散程度作为实例不确定性，其他方法则使用提示诱导的不确定性；该指标同样应用黑图健全性过滤。所给节选没有展示其完整计算公式，因此不能进一步断言具体校准方式。 （越高越好，因为较高数值表示模型在考虑自身可靠性后，仍有更多预测满足给定距离容差。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 完整SpatialQuery管线，以Qwen3-VL-8B为骨干，在固定5,000条T1查询上进行零样本最近实例地面距离估计。

<div class="result-value" markdown="1">

Floor-MAE为0.259米，是摘要报告的核心连续距离误差结果。

</div>

作者据此主张，经过实例级几何恢复、TC+MR稳健细化和规范化BEV表示后，通用VLM可以从单张RGB图像给出较准确的地面距离。该数字只概括有效原图预测的平均绝对误差，不能单独说明无效输出比例、长尾误差分布或在室外及未知场景类型上的泛化能力。

<div class="result-source" markdown="1">

来源：摘要；表V的完整模型R3行亦报告Floor-MAE为0.259 m

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Without task-specific fine-tuning or architectural modification, SPATIALQUERY with Qwen3-VL-8B achieves a Floor-MAE of 0.259 m, an Unc-Acc@0.3 m of 90.5%, and a proximity-decision accuracy of 84.18%, outperforming fine-tuned spatial specialists, general-purpose VLMs, and closed-source frontier models.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 完整SpatialQuery管线，以Qwen3-VL-8B为骨干，在T1任务上采用0.3米容差的不确定性感知准确率，并应用黑图健全性过滤。

<div class="result-value" markdown="1">

Unc-Acc@0.3m达到90.5%。

</div>

作者将该结果解释为几何派生的不确定性能够帮助VLM区分较可靠与较不可靠的实例距离证据。由于该指标不等同于普通精确率，也没有在所给节选中提供完整公式，不能把90.5%直接理解为全部距离预测中有90.5%都落在0.3米误差内；它还依赖论文规定的不确定性评分与黑图过滤流程。

<div class="result-source" markdown="1">

来源：摘要；表V的完整模型R3行亦报告Unc@0.3m为90.50%

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Without task-specific fine-tuning or architectural modification, SPATIALQUERY with Qwen3-VL-8B achieves a Floor-MAE of 0.259 m, an Unc-Acc@0.3 m of 90.5%, and a proximity-decision accuracy of 84.18%, outperforming fine-tuned spatial specialists, general-purpose VLMs, and closed-source frontier models.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 完整SpatialQuery管线，以Qwen3-VL-8B为骨干，在T2任务上判断最近候选实例与参考物体的地面距离是否不超过给定阈值$\tau$。

<div class="result-value" markdown="1">

邻近判断准确率为84.18%。

</div>

这表明系统不仅能输出连续距离，还能把恢复的几何用于阈值决策；T2测试按五个距离阈值各抽取1,000条并平衡正负标签，因此结果不是由单一阈值或多数类标签主导。不过，所给节选没有给出各阈值的分项准确率、混淆矩阵或置信区间，无法判断性能是否在较小阈值处明显下降。

<div class="result-source" markdown="1">

来源：摘要；实验设置见第VI-A节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Without task-specific fine-tuning or architectural modification, SPATIALQUERY with Qwen3-VL-8B achieves a Floor-MAE of 0.259 m, an Unc-Acc@0.3 m of 90.5%, and a proximity-decision accuracy of 84.18%, outperforming fine-tuned spatial specialists, general-purpose VLMs, and closed-source frontier models.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评测查询全部来自SpatialQuery-1M，而该基准又由MM-Spatial/CA-1M的200个室内场景构建；尽管固定测试集覆盖全部场景并进行分层采样，所给节选未说明场景级训练、验证、测试隔离，也没有跨数据集、室外环境或真实机器人采集数据的实验，因此不能据此断言广泛域外泛化。
- 基准构建依赖GPT-4o可见性评分、GroundingDINO检测与MM-Spatial三维标注。真实几何不泄露给被测模型，但自动筛选可能引入模型偏好，且仅保留清晰可见、可被检测并成功匹配的实例，可能使评测低估严重遮挡、截断和检测失败场景的难度。原文节选也未报告筛选误差的人工审计结果或统计置信区间。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 纯RGB通用VLM：直接根据原始图像和文本问题作答，不使用SpatialQuery的几何恢复、BEV表示或几何不确定性。表V中的Qwen3-VL-8B raw prompt是明确的纯VLM参照，用于判断增益是否来自几何管线，而非骨干模型本身。
- 闭源前沿模型：与SpatialQuery使用相同的零样本协议和解码设置，用于检验更大或闭源模型仅凭通用视觉语言能力是否能够解决度量空间推理。所给节选未列出具体模型名称与逐项分数。
- 经过微调的空间推理专用模型：代表针对空间任务训练过的专门方法，用于比较无需任务微调的SpatialQuery是否仍具竞争力。摘要声称完整方法优于此类模型，但所给节选未提供具体专用模型名称、训练数据或逐项结果。
- 跨骨干对照Qwen2.5-VL-3B：将完整SpatialQuery管线从主骨干Qwen3-VL-8B迁移到较小的Qwen2.5-VL-3B，用于测试框架是否完全依赖某一个VLM；这项对照衡量可迁移性，而不是单独组件的贡献。

**实验想回答的问题**

- 在仅提供单张RGB图像、且推理时没有真实深度和标定相机内参的条件下，SpatialQuery能否比纯RGB视觉语言模型、闭源前沿模型和经过微调的空间推理专用模型更准确地完成最近实例距离估计（T1）与邻近判断（T2）？
- Tilt-Corrected MAD-RANSAC（TC+MR）、BEV Scene Cubifying与不确定性感知思维链（UA-CoT）分别解决什么误差来源；这些组件的效果能否迁移到不同规模和代际的VLM骨干？

**实验实现**

所有方法均采用统一零样本协议：推理阶段不进行任务专用微调，不提供真实深度或标定相机内参，并使用相同解码设置。主骨干为Qwen3-VL-8B，Qwen2.5-VL-3B用于跨骨干测试；开源实验在单张48 GB NVIDIA RTX 5880 Ada Generation GPU上完成。T2测试集在每个阈值$\tau\in\{0.5,1.0,1.5,2.0,3.0\}$米上各选1,000条查询，并平衡正负标签。准确率类指标采用原图与同分辨率全黑图的双重评测：只有原图正确、黑图错误且两次输出均有效时才计为正确，无效或不可解析输出计零；Floor-MAE则仅基于有效的原图距离预测计算。该过滤旨在降低模型依赖语言模板、类别先验或答案分布而未真正使用图像的可能性。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| R0纯VLM与R1仅启用UA-CoT对比，均不使用TC+MR和BEV；随后比较R1与加入TC+MR的R2。 | R0到R1时，Floor-MAE从0.432米恶化到16.341米，但Acc@0.2m从24.50%提高到49.50%；加入TC+MR后，R2的Floor-MAE降至0.263米，Acc@0.2m升至54.00%，Unc-Acc@0.3m升至88.00%。 | R0与R1隔离了UA-CoT本身：它让更多预测进入0.2米容差，却会在缺少可靠几何时强化少数严重错误，所以固定阈值准确率改善而平均误差崩溃。R1与R2进一步隔离TC+MR，它通过选择主导深度模式并剔除边界或背景离群点，为UA-CoT提供稳定的度量位置和几何不确定性。该消融支持“稳健几何是UA-CoT有效的前提”，但R0未启用UA-CoT而R1至R3均启用，不能从这组结果推断所有提示形式都会产生同样效应。 | 表V；第VII节AQ1<br><span class="experiment-evidence">The R0 → R1 transition reveals a non-monotonic effect: UA-CoT alone increases Floor-MAE from 0.432 m to 16.341 m while improving Acc@0.2 m from 24.50% to 49.50%.</span> |
| R2与R3对比：两者都启用TC+MR和UA-CoT，R3额外加入BEV Scene Cubifying，因此该比较隔离规范化俯视表示的贡献。 | 加入BEV后，Floor-MAE从0.263米小幅降至0.259米，Acc@10%从33.00%升至34.00%，Acc@0.2m从54.00%升至58.50%，Unc-Acc@0.2m从82.50%升至87.50%，Unc-Acc@0.3m从88.00%升至90.50%。 | BEV把实例表示为同尺寸、按类别编码的俯视块，保留候选物体与参考物体的相对地面布局，同时压低纹理、透视和真实物体尺寸差异。连续误差只改善0.004米，但多种容差准确率均上升，说明其主要作用可能是让VLM更稳定地比较实例，而不是大幅提高底层几何的平均精度。由于只有一个固定评测集和主骨干上的增量消融，尚不能确定该增益在其他数据分布中是否同样稳定。 | 表V，R3行；对应R2行为“+ Tilt-Corrected MAD-RANSAC \| ✓ \| ✗ \| ✓ \| 0.263 \| 33.00 \| 54.00 \| 82.50 \| 88.00”<br><span class="experiment-evidence">R3 \| + BEV Scene Cubifying (Full model) \| ✓ \| ✓ \| ✓ \| 0.259 \| 34.00 \| 58.50 \| 87.50 \| 90.50</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces a geometry-grounded VLM spatial-reasoning method and a million-example benchmark for evaluating metric multi-instance reasoning.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`749e47ec8c54d840a89cbadf0462224887d11d82277099d9311946ce9308122a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
