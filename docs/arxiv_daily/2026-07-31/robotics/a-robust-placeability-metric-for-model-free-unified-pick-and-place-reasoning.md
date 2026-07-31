---
title: "[论文解读] A Robust Placeability Metric for Model-Free Unified Pick-and-Place Reasoning"
description: "[arXiv 2510.14584][机器人 / 具身智能] 本文提出一种直接面向噪声、局部点云的概率式可放置性度量，联合评估候选六自由度放置姿态的物理稳定性与放置条件下的抓取可执行性，从而为未知物体选择稳定、无碰撞的抓取—放置组合。"
arxiv_id: "2510.14584"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T05:30:51.234314+00:00"
source_sha256: "1e77abb443ccf7bd9ea0c0b539ffc7d34d496979cfe22fccc873f1e3842c55d1"
tags:
  - "机器人 / 具身智能"
  - "机器人抓取与放置"
  - "统一抓取—放置推理"
  - "无模型规划"
  - "部分点云"
  - "六自由度放置"
  - "概率稳定性"
  - "放置条件抓取可行性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2510.14584</p>

# A Robust Placeability Metric for Model-Free Unified Pick-and-Place Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Wingender, Benno, Dengler, Nils, Menon, Rohit, Pan, Sicong, Bennewitz, Maren</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Humanoid Robots Lab, University of Bonn；Lamarr Institute for Machine Learning and Artificial Intelligence；Center for Robotics, Bonn</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2510.14584) · [PDF 下载](https://arxiv.org/pdf/2510.14584) · **关键词** 机器人抓取与放置, 统一抓取—放置推理, 无模型规划, 部分点云, 六自由度放置, 概率稳定性, 放置条件抓取可行性<br>
**代码**: [https://github.com/HumanoidsBonn/Placeability](https://github.com/HumanoidsBonn/Placeability)

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

本文提出一种直接面向噪声、局部点云的概率式可放置性度量，联合评估候选六自由度放置姿态的物理稳定性与放置条件下的抓取可执行性，从而为未知物体选择稳定、无碰撞的抓取—放置组合。

**不用术语来说**：机器人看到的物体通常是不完整的，例如放在桌面上的物体底面会被遮挡；它不仅要判断物体放到目标位置后会不会倾倒，还要保证此前选择的抓法在货架等狭窄空间中仍能完成放置。若只挑容易抓的姿势，机械臂可能在目标处碰撞；若只检查能否到达而不判断稳定性，物体又可能靠近边缘、落在斜面上并最终倾倒。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出无需 CAD 模型或预定义放置姿态的可放置性度量，从原始局部点云共同评价候选六自由度姿态的概率稳定性与放置条件抓取可行性，用于统一排序抓取—放置对。
- 针对重建噪声与遮挡，将 TSDF 权重作为几何观测置信度，同时表达质心和接触面的不确定性，使系统能够处理支撑边缘、倾斜支撑面以及限高货架等偏离平整桌面的场景。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于机器人操作中的统一抓取—放置规划：机器人不仅要找到能够夹起物体的抓姿，还要提前判断该抓姿在目标位置是否仍可执行，并选择不会倾倒或碰撞的放置姿态。真实场景中的关键困难是，RGB-D 相机得到的点云带有噪声且因遮挡而不完整，例如桌面上的物体通常缺少底面观测；同时，货架边缘、倾斜支撑面和高度受限空间又使“平整且连续的桌面”假设失效。因此，系统需要直接依据局部几何观测，对未见物体的六自由度放置姿态进行稳定性与可执行性联合判断，而不能依赖完整 CAD 模型或少量预定义姿态。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**六自由度放置姿态（6D placement pose）**

物体在三维空间中的状态由三个平移自由度和三个旋转自由度共同描述。不同朝向即使位于同一目标区域，也可能产生完全不同的接触、稳定性、占用高度和碰撞风险。

</div>
<div class="concept-item" markdown="1">

**部分点云与 TSDF**

点云是由深度传感器获得的一组三维表面采样点；遮挡和测量误差会使其缺失、稀疏或带噪。TSDF（截断符号距离函数）把多帧深度观测融合为体素化几何表示，其融合权重可用作局部观测可信度，但本文具体计算方式未包含在所给章节中。

</div>
<div class="concept-item" markdown="1">

**放置条件抓取可行性（PCG）**

PCG 检查一个原本适合拾取的抓姿，在物体变换到候选放置姿态后是否仍然可达且不会与环境碰撞。它把“能否抓起”和“能否带着该抓姿安全放下”联系起来，避免分别规划导致的死路。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是由真实 RGB-D 观测重建的目标物体与环境点云，其中物体几何可能因遮挡而不完整，并包含传感噪声；测试对象可以是系统此前未见过的物体，目标支撑区域也不局限于连续水平桌面。系统需要生成多个朝向的候选六自由度放置姿态和候选抓姿，依据概率稳定性、目标位置处的抓取可达性与碰撞情况以及间隙等约束，对抓姿—放置姿态组合进行排序，并输出可由运动规划器执行的稳定、无碰撞组合。问题设置不要求完整 CAD 模型或预定义放置姿态；其核心不是孤立预测物体哪一面适合朝下，而是在受限环境中联合回答“物体放在哪里及以何种朝向才稳定”与“采用哪个抓姿才能完成拾取和放置”。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Haustein et al. [3] 的 CAD 几何放置规划方法**: 该方法通过将质心投影到凸包表面并结合物体间隙等任务目标，搜索稳定、可达且无碰撞的放置姿态，是本文稳定性评估实验所比较的 CAD-based baseline。其物理依据明确，但依赖完整的物体与环境几何，并主要面向连续支撑面，难以直接处理部分点云和支撑边缘。
- **Noh et al. [15] 的 UOP-Net**: UOP-Net 从部分观测中估计稳定放置区域，代表降低完整物体模型依赖的学习式方法，本文在物理仿真中与其比较放置后的物体姿态误差。原文指出该方法假设物体放置于平面桌面，且没有提供可跨物体朝向和支撑几何统一比较的通用放置质量指标。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

仓储、家庭辅助和医疗等场景要求机器人操作从未见过的物体，但真实传感器只能提供带噪且受遮挡的局部点云。机器人必须在同一次规划中兼顾拾取、目标位置的碰撞与间隙约束，以及放置后的抗倾倒稳定性；在限高货架中，可用抓法和可用物体朝向都很少，任何一项判断错误都可能导致碰撞、无法放入或放置后倾倒。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **无模型放置方法**：从未知物体的局部观测中预测可稳定接触的表面或放置姿态，重点解决没有 CAD 几何先验时“物体怎样摆放较稳定”的问题。
- **统一抓取—放置方法**：在选择抓取时提前考虑目标放置，使系统能够排除目标位置不可达或会发生碰撞的抓法；已有方法通常借助完整 CAD 模型、平面桌面假设，或仅为每个抓法检查少量预设放置姿态。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 无模型放置方法往往孤立地预测稳定表面或姿态，没有把机器人运动学、目标环境碰撞和抓取在目标姿态下是否仍可执行纳入同一任务级评分，因此稳定候选未必真正能够被机械臂放到目标位置。
- 现有统一方法常依赖完整物体几何与连续平坦支撑面，并弱化显式稳定性判断或仅搜索少数预定义姿态；面对局部点云、支撑边缘和斜面时，它们缺少能够反映重建不确定性的物理稳定性分数，因而难以可靠排序抓取—放置对。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚缺少一种统一、无模型且具有物理依据的评分机制：它应直接利用噪声局部点云，对多朝向六自由度放置候选建模稳定性不确定性，同时判断相应抓取在目标环境中是否可达、无碰撞，并据此比较完整的抓取—放置组合。

</div>
<div markdown="1"><span>核心问题</span>

能否仅依靠未知物体的局部点云，构造一个对感知不确定性稳健的可放置性度量，使机器人在狭窄或非平面支撑环境中联合选出既不会倾倒、又能够无碰撞执行的抓取与六自由度放置姿态？

</div>
<div markdown="1"><span>作者直觉</span>

稳定性和可执行性是两个互补条件：前者回答物体放下后是否会保持平衡，后者回答机器人能否以当前抓法把它送到该姿态。作者用点云重建置信度降低不可靠表面证据的影响，并让每个抓取都在候选放置姿态下重新接受可达性与碰撞检查；因此，评分高的组合不只是几何上“看起来能放”，而是同时通过了抗倾倒和实际执行两道筛选。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文提出一个无需对象先验模型的统一抓取—放置推理流程。输入是由多视角 RGB-D 观测在线重建的场景与对象几何，包括源区域 $S$、目标区域 $P$、TSDF 场景网格 $\mathcal{M}$ 以及对象的部分点云；系统生成目标区域内具有多种位置和朝向的候选放置姿态 $\mathcal{T}_{P}$，用概率稳定性和环境可行性评价候选，再根据具体放置姿态重新评价抓取，使最终输出的对象姿态 $t_o$ 同时满足稳定、可抓取、无碰撞和运动学可执行等要求。这里“统一”并非简单地先选最佳抓取、再寻找可用放置，而是把某个抓取在目标放置位置是否仍能执行纳入同一次组合选择。

核心设计是概率式 placeability（可放置性）评价：它直接从不完整、含噪的观测几何判断对象在支撑面边缘、倾斜表面或拥挤空间中的放置质量，并将稳定性与放置条件下的抓取可行性结合。直观上，系统不是只问“这个抓取现在是否容易抓”，也不是只问“对象看起来能否放稳”，而是问“用这个抓取拿起对象后，能否以这个朝向把它送入指定空间、避开环境并稳定放下”。由于所给节选未包含第 IV 节的完整算法定义，候选采样规则、概率稳定性公式和各评分项的组合方式不能从当前材料中可靠复原。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在线场景与对象重建

系统融合深度观测，构建截断符号距离函数（TSDF）场景网格 $\mathcal{M}$，并从源区域 $S$ 中获得目标对象 $o$ 的部分几何。重建结果同时提供不依赖 CAD 的逐对象几何和用于后续碰撞检测的环境网格。

<div class="method-step__io" markdown="1">

**输入**：从预定义观察位姿采集的多视角 RGB-D 数据，以及对象位置的初始估计。<br>
**输出**：目标对象的部分点云或网格、源区域 $S$、目标区域 $P$ 与场景碰撞网格 $\mathcal{M}$。

</div>

**直观理解**：机器人从几个方向观察现场，把深度图拼成一个近似三维地图；即使看不到对象底面，也不要求预先拥有该对象的完整 CAD 模型。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多朝向放置候选生成

系统在 $P$ 内生成候选放置姿态集合 $\mathcal{T}_{P}\subset SE(3)$，候选覆盖不同位置和对象朝向，而非固定原始朝向或只考虑水平桌面上的单一支撑姿态。节选表明对比基线使用六种朝向，但未明确完整方法的精确朝向集合、采样密度及筛选算法。

<div class="method-step__io" markdown="1">

**输入**：对象的观测几何、目标区域 $P$ 及其周围环境几何。<br>
**输出**：一组候选六自由度放置姿态 $t_o\in\mathcal{T}_{P}$。

</div>

**直观理解**：系统先提出多种“放在哪里、转成什么方向”的方案，让狭窄货架中横放、侧放或改变朝向成为可能，而不是抓起后才临时寻找空位。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 概率稳定性与放置可行性评价

系统计算概率稳定性分数 $f_{\mathrm{st}}(o_t)$，利用对象与环境的原始点云几何评估候选在部分支撑、边缘邻近和倾斜表面上的静态稳定趋势，并检查环境碰撞及放置可行性。该稳定性建模考虑接触几何和质心驱动的倾覆行为，但原文明确指出它不建模摩擦。

<div class="method-step__io" markdown="1">

**输入**：每个候选姿态 $t_o$、对象的部分几何、目标支撑面和场景网格 $\mathcal{M}$。<br>
**输出**：每个放置候选的稳定性与环境可行性评价，以及被排除的碰撞或物理无效候选。

</div>

**直观理解**：这一步类似判断物体的“重心投影和实际接触底座是否匹配”，并同时查看机械手和物体会不会撞到货架；概率分数还能表达点云缺失导致的不确定性。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 放置条件化的抓取重评分与联合选择

流程把抓取评分与具体目标放置姿态关联，重新排序原始 GPD 抓取候选，并联合考察抓取质量、放置稳定性、目标处碰撞和运动学可执行性。随后选择能够形成有效抓取—放置配对的最高质量方案，而不是固定最高抓取得分后再随机或顺序寻找放置。

<div class="method-step__io" markdown="1">

**输入**：抓取检测器产生的抓取候选、通过初步检查的放置候选，以及各候选的稳定性和碰撞信息。<br>
**输出**：最终抓取姿态与对象目标姿态 $t_o$ 构成的稳定、可抓取、无碰撞抓放对。

</div>

**直观理解**：某个抓法虽然容易把对象拿起来，却可能让夹爪在放入货架时撞到顶板；联合选择会改用稍低抓取得分、但能顺利放下的抓法。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。现有节选将该方法描述为基于在线几何重建、候选采样、概率稳定性评价、碰撞检查和抓取重评分的模型无关推理流程，没有报告需要训练的网络、监督标签或训练损失。GPD 抓取预测器属于外部抓取候选生成组件，UOP-Net 仅作为实验基线；不能据此推断本文方法具有端到端训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 概率稳定性评价**

模块以放置后的对象 $o_t$ 及其与支撑环境的部分观测几何为输入，输出稳定性估计 $f_{\mathrm{st}}(o_t)$。从实验描述可确认，该估计针对支撑边缘接近、支撑面倾斜、接触区域不完整及质心偏置设计，并能在约 $0.5$ 附近呈现倾覆阈值过渡；但节选没有给出概率分布、支撑多边形构造、质心估计或评分公式。

> 直观理解：普通方法常把“找到一个看似平的对象表面”当作稳定，而该模块进一步判断物体实际压在支撑区域上的方式是否容易倾覆，因此能够处理钻头等弯曲、不对称物体以及靠近桌边的情况。

**2. 多朝向候选与环境可行性评价**

模块在目标区域 $P$ 内构造六自由度候选集合 $\mathcal{T}_{P}$，并借助 TSDF 网格 $\mathcal{M}$ 检查候选与杂物、货架或容器结构之间的碰撞和空间约束。其目的不是仅预测对象自身的稳定支撑面，而是搜索在给定目标环境中真正可容纳、可到达的放置姿态。

> 直观理解：同一物体在开阔桌面上可以直立，但在低矮货架里可能只能侧放；该模块把目标空间的高度、边界和已有物体一起纳入判断。

**3. 放置条件化抓取评分**

模块接收 GPD 生成的抓取候选，并根据每个目标放置姿态下的夹爪净空、碰撞风险、放置可执行性与稳定性重新排序。它将原本彼此独立的抓取和放置决策转化为抓取—放置配对评价，从而避免选中“抓得住但放不下”的抓法。

> 直观理解：夹住物体中部可能最牢，但夹爪随后可能无法伸进窄货架；重新评分会优先保留在目标位置仍有足够操作空间的抓法。

**训练与推理**

该方法主要是在线推理。首先从多个预设视角采集 RGB-D 数据并融合为 TSDF 场景网格 $\mathcal{M}$，获得对象的不完整几何以及可靠的环境碰撞表示；随后在目标区域 $P$ 中生成包含不同位置和朝向的候选集合 $\mathcal{T}_{P}$。对每个候选，系统评价概率稳定性 $f_{\mathrm{st}}(o_t)$、目标环境碰撞和放置可行性，再将这些放置信息用于重新评价 GPD 抓取候选，最终联合选出可执行的抓取—放置对并交给运动规划器执行。

当前节选没有给出完整第 IV 节，因此无法核实稳定概率的具体计算、各评分项的权重、候选剪枝顺序、最终排序准则及无解时的回退策略。可以确定的是，完整方法不同于顺序式基线 Grasp-RP 和 Grasp-MO：它不会先固定抓取再寻找放置，而是在选择抓取时显式考虑目标放置；UniP-NoStab 则保留这种联合推理，但删除概率稳定性项。

**复现信息**

方法假设目标对象能够被充分观察，但不假设对象形状、初始朝向、CAD 模型或目标区域内其他物体的已知位姿。场景从初始未知状态开始，通过对象位置初值周围的预定义视角以及覆盖关键环境部分的附加视角重建；表示采用 TSDF 场景网格，既服务于逐对象几何评价，也服务于环境碰撞检查。

真实机器人平台为 UR5e，抓取候选由 GPD 提供。运行时间分析显示，TSDF 重建、放置候选采样和完整可放置性评价均可在线运行，但这些数字属于实验测量而非算法定义；原文还说明部分计算可以并行。稳定性模型未考虑摩擦，因此对以滑移而非倾覆失稳的对象可能高估稳定性，尤其当接触区域沿下坡方向较长时。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 实验未使用原文明确命名的公开数据集，而是在仿真与真实机器人环境中评测常见家居物体；物体具有不同几何形状和质量分布，并以未见物体及具有挑战性的支撑几何为测试对象。给定材料未报告物体数量、训练/测试划分或仿真场景规模，因此无法判断样本覆盖度及是否存在对象级数据泄漏。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**稳定性预测准确性**

衡量可放置性度量对候选六维放置姿态是否稳定的判断与实际或仿真结果的一致程度。给定材料没有说明采用准确率、精确率、召回率、ROC-AUC还是其他具体统计量。 （越高越好，因为更准确的稳定性预测可减少物体倾倒、滑落或仅靠偶然接触保持平衡的放置方案。）

</div>
<div class="metric-item" markdown="1">

**端到端拾取放置成功率**

衡量系统从部分点云观测出发，完成抓取、搬运并稳定放置物体的整体成功比例；它同时受感知、抓取可行性、碰撞检查和放置稳定性影响。 （越高越好，因为它直接反映完整机器人流程成功完成任务的频率，但不能单独定位失败来自哪个模块。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 从不完整真实点云预测候选放置姿态的稳定性

<div class="result-value" markdown="1">

作者声称，所提出的度量能够对放置稳定性作出准确预测；但给定材料没有提供具体准确率、误差、样本量或与基线的数值差距。

</div>

这项结果针对方法的核心前提：即使物体底面等区域因遮挡而不可见，系统仍可利用观测到的点云几何评估放置是否可靠。不过，摘要层面的“准确”结论不能说明模型在不同物体类别、倾斜支撑面或边缘附近分别表现如何，也不能据此量化泛化能力。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Simulation and real-robot experiments on unseen objects and challenging support geometries confirm that our metric yields accurate stability predictions and consistently improves end-to-end pick-and-place success by producing stable, collision-free grasp-place pairs directly from partial point clouds.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 仿真与真实机器人上的端到端统一拾取放置

<div class="result-value" markdown="1">

作者声称，该方法在未见物体和困难支撑几何上持续提高端到端拾取放置成功率；给定材料未报告成功率数值、绝对提升、相对提升或方差。

</div>

端到端改善意味着稳定性度量并非只在离线分类任务上有效，而可能帮助机械臂实际完成抓取和放置。然而，该指标混合了感知、运动执行、抓取和放置等多个因素；在没有对照方法及失败类型统计时，不能确定提升完全来自可放置性度量。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Simulation and real-robot experiments on unseen objects and challenging support geometries confirm that our metric yields accurate stability predictions and consistently improves end-to-end pick-and-place success by producing stable, collision-free grasp-place pairs directly from partial point clouds.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 直接依据部分点云生成抓取—放置组合

<div class="result-value" markdown="1">

作者声称，系统能够生成稳定且无碰撞的抓取—放置对，从而支持无物体模型的统一推理；给定材料未给出无碰撞比例、有效候选率或执行成功次数。

</div>

这一结果强调方法输出的不是孤立的放置姿态，而是同时考虑物体落位后稳定性与夹爪可执行性的成对方案。它支持系统具有任务级实用性的主张，但尚不能证明对所有夹爪类型、严重遮挡条件或动态扰动均保持鲁棒。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Simulation and real-robot experiments on unseen objects and challenging support geometries confirm that our metric yields accurate stability predictions and consistently improves end-to-end pick-and-place success by producing stable, collision-free grasp-place pairs directly from partial point clouds.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 给定实验节选未报告对象数量、场景数量、数据划分、逐条件成功率或失败类别；因此无法判断结果是否由少量容易对象主导，也无法评估边缘放置、倾斜支撑和严重遮挡等条件下的独立表现。
- 给定材料未列出基线和消融实验，也未提供数值结果及置信区间；因此无法隔离概率稳定性估计、面向物体的推理、多朝向候选生成和条件抓取评分各自的贡献。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。

**实验想回答的问题**

- 所提出的概率式可放置性度量能否仅依据遮挡、不完整的真实点云，准确判断未见物体在不同支撑几何上的放置稳定性？
- 将放置稳定性评估与以候选放置为条件的抓取评分统一起来，能否产生稳定、无碰撞的抓取—放置组合，并提高端到端拾取放置成功率？

**实验实现**

真实机器人平台为 UR5e 六自由度机械臂和 Robotiq 2F-85 夹爪，物体观测使用腕载 Orbbec Gemini 336 RGB-D 相机及外部 RealSense D435 相机。源区域点云由三个固定视角采集，并辅以外部相机观测以扩大可见工作空间。系统运行于 ROS 2 Humble，计算平台包含 NVIDIA RTX 4080 Super GPU、AMD Ryzen 9 7900X3D CPU 和 128 GB 内存。稳定性估计使用 $N=100$ 个蒙特卡洛样本，并设置几何参数 $\zeta=0.02\,\mathrm{m}$；可行性检查采用垂直容差 $\delta_{\min}=0.02\,\mathrm{m}$。给定材料未说明重复试验次数、随机种子、成功判据、置信区间或统计显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces a point-cloud-based placement metric and unified planning method for robotic pick-and-place manipulation.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`1e77abb443ccf7bd9ea0c0b539ffc7d34d496979cfe22fccc873f1e3842c55d1`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
