---
title: "[论文解读] PhysMind: From Video to Executable Worlds for Training-Free Physical Reasoning"
description: "[arXiv 2608.04575][VLM Reasoning] PhysMind要解决的核心问题是：如何在不进行任务特定训练的条件下，把视频还原为可检查、可干预、可继续执行且能被多问题复用的物理世界，使视觉语言模型依据执行结果而非仅凭文本推断回答物理推理问题。"
arxiv_id: "2608.04575"
announcement_date: "2026-08-06"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T07:01:05.029625+00:00"
source_sha256: "ca32bf8d4e7df6eb6fa355a7e012012b593ba548c8fc89d1eb57073383eefd09"
tags:
  - "VLM Reasoning"
  - "LLM Agent"
  - "LLM Reasoning"
  - "多模态 VLM"
  - "视频物理推理"
  - "视觉语言模型"
  - "可执行世界"
  - "动态场景重建"
  - "六自由度位姿跟踪"
  - "物理系统辨识"
  - "连续时间动力学"
  - "反事实推理"
  - "免训练框架"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.04575</p>

# PhysMind: From Video to Executable Worlds for Training-Free Physical Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Chen Yang, Shenxiang Zeng, Haoyang Zhao, Zhouyuan Xu, Youquan He, Haoyu Li, Mingyi Deng, Jiansheng Fan, Chen Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Tsinghua University；The University of Hong Kong</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04575v1) · [PDF 下载](https://arxiv.org/pdf/2608.04575v1) · **关键词** 视频物理推理, 视觉语言模型, 可执行世界, 动态场景重建, 六自由度位姿跟踪, 物理系统辨识, 连续时间动力学, 反事实推理, 免训练框架<br>
**项目页**: [https://physmind.github.io/](https://physmind.github.io/)

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

PhysMind要解决的核心问题是：如何在不进行任务特定训练的条件下，把视频还原为可检查、可干预、可继续执行且能被多问题复用的物理世界，使视觉语言模型依据执行结果而非仅凭文本推断回答物理推理问题。

**不用术语来说**：只看视频画面并不等于理解其中的物理过程：模型不仅要识别物体，还要判断它们如何运动、何时碰撞，以及移除某个物体后会发生什么。现有视觉语言模型容易根据表面线索或语言模式猜测答案，尤其难以可靠处理未来预测和“如果改变场景会怎样”的反事实问题；机器人操作与自动驾驶等应用则要求系统真正估计世界将如何演化。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出训练自由的智能体框架 PhysMind：每段视频只构建一次与问题无关的可执行世界，之后针对不同问题选择检查已有状态、延续动力学或编辑场景，并以执行产生的轨迹、交互事件和结果作为回答依据。
- 将动态场景重建与解析式连续时间系统辨识结合起来：前者恢复跨帧持续一致的物体身份、条件化网格和 $6$ 自由度位姿轨迹，后者从观测运动中拟合质量、摩擦、恢复系数及初始运动等潜在物理属性，为长时预测和反事实干预提供显式动力学模型。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究视频物理推理：系统不仅要识别画面中的物体，还要理解物体如何运动、碰撞，以及在移除物体等干预下场景将如何演化。现有视觉语言模型（VLM）虽擅长图像、视频与语言理解，但在稳定性、碰撞、隐含材料属性、物体恒存和定量运动学等方面仍不可靠；这会直接限制机器人操作和自动驾驶等需要预测行动后果的应用。PhysMind所处的技术交叉点包括动态三维场景重建与物理系统辨识：前者从视频恢复具有持续身份、几何形状和六自由度运动轨迹的物体，后者利用观测轨迹估计质量、摩擦、恢复系数和初始运动等不可直接观察的物理属性，最终得到可检查、可继续执行且可编辑的显式物理世界。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**六自由度位姿（6D pose）**

六自由度位姿用三个平移分量和三个旋转分量描述刚体在三维空间中的位置与朝向。跨视频帧跟踪该位姿，可得到物体随时间变化的空间运动轨迹。

</div>
<div class="concept-item" markdown="1">

**物理系统辨识（physical system identification）**

系统辨识是根据观测到的运动反推控制运动的动力学参数或规律，例如质量、摩擦、碰撞恢复系数和初始速度。本文用它把重建出的视觉轨迹转化为能够预测未来和反事实结果的物理模型。

</div>
<div class="concept-item" markdown="1">

**可执行世界（executable world）**

可执行世界是包含物体几何、状态、动力学参数及状态转移机制的显式场景模型，可以被运行以产生后续轨迹和碰撞事件。它区别于只在语言或隐特征中推测答案的方法，并允许系统检查原场景、延续运动或施加干预。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一段展示多个物体运动和交互的视频；系统首先在不使用具体问题的情况下，为该视频构建一次可复用的场景级可执行世界。构建过程需要完成物体分割与身份关联、网格重建、六自由度位姿跟踪，并从恢复的运动中拟合连续时间解析动力学及质量、摩擦和恢复系数等隐含物理参数。随后才输入关于视频的物理问题，问题可要求解释已发生事件、预测未来结果，或判断移除物体等干预造成的反事实结果；系统据此检查、继续执行或编辑已构建的世界，并依据生成的轨迹、参数和交互事件输出答案。该设置的关键假设是视频提供了足以恢复对象级运动并约束动力学的视觉证据，同时可调用预训练感知、重建和跟踪工具；框架本身不进行任务微调，并以同一世界服务同一视频上的不同问题。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **VRDP**: VRDP从视觉轨迹学习或辨识物体动力学，并通过基于冲量的离散时间模拟器进行可微优化，是与本文视觉系统辨识最直接相关的任务专用方法。PhysMind改为拟合连续时间解析轨迹，并把碰撞表示为瞬时状态转移，以缩短长时程优化中的梯度传播路径。
- **LLMPhy**: LLMPhy利用轨迹误差引导大语言模型在MuJoCo或PyBullet中进行黑盒物理参数搜索，代表无需沿模拟器梯度反传的推理时系统辨识方案；但它仍需反复评估离散时间 rollout。PhysMind则从视频构建一个与问题无关、可跨问题复用的显式世界，并直接拟合解析连续时间动力学。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

视频物理推理需要从有限观测中解释已经发生的事件、预测后续状态，并评估移除或改变物体等干预的影响。现有模型在稳定性、碰撞、潜在材料属性、物体恒存性和定量运动学方面仍不可靠，这会直接限制机器人操作和自动驾驶等具身系统，因为其动作决策取决于环境接下来如何变化，而不只是当前画面看起来是什么。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **训练式物理推理方法**：早期方法为特定任务训练模型以恢复轨迹、学习物体交互模式或预测未来状态；较新的方法通过监督微调或强化学习，使通用视觉语言模型生成更符合物理规律的描述与推理轨迹。
- **推理时增强方法**：在不完全依赖直接思维链提示的情况下，向视觉语言模型提供帧记忆、感知工具或模拟器产生的补充证据，使模型能够查询视频细节或借助外部计算回答问题。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 多数方法没有公开表示观测场景的显式状态转移模型，而是从潜在特征、文本推理或针对单个问题收集的证据直接得到答案。因此，连接视频观测与答案的物理状态和作用机制难以检查、编辑或重新执行，在未来预测和反事实推理中尤其容易产生缺乏物理依据的事件判断。
- 训练式方法需要额外标注数据、适配计算和面向任务的训练，并可能以损害通用视觉语言能力为代价；与此同时，单纯恢复几何形状也不足以形成可执行世界，因为场景演化还取决于质量、摩擦、恢复系数和初始运动等视频中不可直接观测的潜在参数。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究分别提供了视觉语言推理、几何重建、运动跟踪、外部模拟和系统辨识能力，但仍缺少一种无需任务特定训练的统一机制，能够协调这些组件，从单段视频恢复身份与时间一致的场景状态和潜在动力学，并形成一个在问题提出前就已构建、可供多个问题重复检查与干预的显式可执行世界。

</div>
<div markdown="1"><span>核心问题</span>

能否让视觉语言模型作为协调者，在无需微调的情况下，从视频中一次性构建几何与动力学一致的可执行世界，并针对解释、预测和反事实问题，通过检查、延续或编辑该世界产生可核验的执行证据，从而提高物理推理可靠性？

</div>
<div markdown="1"><span>作者直觉</span>

其出发点类似于先搭建一个可运行的实验模型，再在模型里做实验：重建模块把视频中的物体变成具有稳定身份、形状和运动轨迹的实体，系统辨识再反推出哪些动力学参数能够解释已观察到的运动。回答普通问题时可以检查该模型，预测未来时继续运行它，回答反事实问题时则先修改对应物体或条件再执行。这样，同一视频的物理解释只需建立一次，不同问题共享同一套世界状态；答案也可以追溯到具体轨迹和碰撞事件，而不是完全依靠视觉语言模型在文字空间中猜测。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PhysMind把视频物理推理转化为“先建世界、后问问题”的两阶段过程。第一阶段仅根据视频$\mathcal{V}=\{I_t\}_{t=1}^{T}$重建与问题无关的动态场景$\mathcal{S}$：系统分割并持续跟踪物体，恢复相机、深度、物体网格、支撑面和每个物体的六自由度位姿轨迹$X_i(t)\in\mathrm{SE}(3)$。第二阶段把这些观测轨迹拟合成可执行世界$\mathcal{W}$，其中包含初始状态以及摩擦、恢复系数和相对质量等物理参数$\Theta$。收到问题$q$后，智能体才选择检查已有事件、延续未来运动，或复制并编辑世界进行反事实模拟，得到结构化执行记录$\mathcal{R}_q$，最后将其映射到答案空间$\mathcal{A}(q)$。

技术核心是以分段解析的连续时间动力学表示运动：碰撞之间使用自由飞行或库仑摩擦等运动模式的闭式解，碰撞时施加瞬时速度更新，而不是用固定时间步逐帧展开通用模拟器。通俗地说，系统先把视频变成一个可反复运行的“数字实验台”，再针对问题读取记录、让实验继续，或修改某个条件后重做实验；因此同一视频只需建模一次，不同问题共享同一个基础世界。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 持久物体发现与语义描述

SAM 3使用宽泛的物体提示生成匿名掩码轨迹$\tau_i=\{M_{i,t}\}_{t=1}^{T}$，并为每条轨迹选择遮挡较少、物体最清晰的代表帧。VLM依据代表图像标注颜色、材质、几何类别和外观，同时保留匿名身份作为后续几何处理的稳定索引，并确定物体可见及适合估计位姿的时间区间。

<div class="method-step__io" markdown="1">

**输入**：完整视频$\mathcal{V}=\{I_t\}_{t=1}^{T}$。<br>
**输出**：带持久匿名身份、逐帧掩码、活动区间和语义属性的物体集合。

</div>

**直观理解**：这一步相当于先给视频中的每个物体分配不会随帧变化的编号，再记录“它是什么样”，避免后续把相似物体混为一谈。语义属性主要用于网格生成和问题中的语言指代，几何计算仍由匿名轨迹锚定。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 共享三维场景与位姿轨迹重建

MoGe-2从采样帧估计并聚合固定相机内参$K$，Video Depth Anything产生时间一致的深度$\{D_t\}$；代表帧中的掩码像素经反投影形成三维点，并与RGB和掩码共同条件化SAM 3D Objects以恢复彩色规范网格$\mathcal{M}_i$。FoundationPose从RGB、深度、掩码和内参出发进行前向与后向六自由度跟踪，随后依据重力方向、共享支撑面、相机滚转和物体对称性校正各轨迹，并沿相机射线调整位置以恢复接触关系。

<div class="method-step__io" markdown="1">

**输入**：视频帧、物体掩码轨迹及其代表帧与语义属性。<br>
**输出**：动态场景$\mathcal{S}=(K,\mathbf{g},\Pi,\mathcal{O})$，其中包含相机$K$、重力$\mathbf{g}$、支撑几何$\Pi$、物体网格及一致位姿轨迹$\{X_i(t)\}$。

</div>

**直观理解**：单独追踪每个物体容易出现“物体漂浮、地面倾斜或朝向跳变”等彼此不一致的结果，因此系统还要把所有轨迹放回同一个受重力和支撑面约束的三维坐标系。对球体或圆柱等具有对称性的物体，视觉上无法确定的旋转不会被当成真实误差。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 连续时间动力学辨识与可执行世界构建

系统利用网格邻近性提出候选碰撞区间，将运动表示为由碰撞事件分隔的解析片段，并联合优化初速度、地面摩擦、碰撞恢复系数及接触连通物体之间的质量比。优化使解析轨迹同时贴合观测位置与对称性感知的朝向，满足候选接触，并通过物理先验与有界参数化抑制不合理解；长序列采用逐步扩展时间前缀的方式引入后续碰撞。

<div class="method-step__io" markdown="1">

**输入**：校正后的物体位置$\mathbf{p}_{i,t}$、朝向$R_{i,t}$、网格、活动区间和候选接触关系。<br>
**输出**：可执行世界$\mathcal{W}=F_{\mathrm{id}}(\mathcal{S})$，包含几何场景、初始动态状态、碰撞事件结构和辨识参数$\Theta^*$。

</div>

**直观理解**：系统不是给每一帧硬配一条运动，而是寻找一组能够解释整段观测的物理参数：物体在两次碰撞间按公式运动，碰撞瞬间再更新速度。碰撞通常只能揭示物体之间“谁相对更重”，所以方法在发生接触的物体组内固定一个参考质量，只估计可观测的质量比例。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 问题条件执行与证据化回答

VLM先把问题中的颜色、形状或关系描述绑定到匿名物体身份，再选择世界接口：解释性问题检查状态与接触记录，预测性问题延续已拟合动力学，反事实问题复制世界后删除物体或修改题目指定条件并比较执行结果。执行产生包含轨迹、接触、状态变化和干预的$\mathcal{R}_q$，回答VLM依据该证据包输出$\hat{a}\in\mathcal{A}(q)$。

<div class="method-step__io" markdown="1">

**输入**：问题$q$、答案空间$\mathcal{A}(q)$、基础世界$\mathcal{W}$及必要的视频信息。<br>
**输出**：查询专属执行记录$\mathcal{R}_q$及最终答案$\hat{a}$，基础世界$\mathcal{W}$保持不变并可供其他问题复用。

</div>

**直观理解**：解释题像查实验日志，预测题像继续播放实验，反事实题则像复制实验装置后改变一个条件再运行。VLM负责理解语言和选择操作，实际的运动与碰撞判断由可检查的世界轨迹提供依据。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 问题无关世界构建与问题条件执行

$$
\begin{array}{rcl}\mathcal{S}&=&F_{\mathrm{scene}}(\mathcal{V}),\\ \mathcal{W}&=&F_{\mathrm{id}}(\mathcal{S}),\\ \mathcal{R}_{q}&=&F_{\mathrm{exec}}(\mathcal{W},q),\\ \hat{a}&=&F_{\mathrm{ans}}(\mathcal{V},q,\mathcal{W},\mathcal{R}_{q}).\end{array}
$$

**符号说明**

- $\mathcal{V}=\{I_t\}_{t=1}^{T}$：由$T$帧图像构成的输入视频。
- $\mathcal{S}$：重建的动态场景，包含相机、重力、支撑几何、物体网格和位姿轨迹。
- $F_{\mathrm{scene}}$：从视频恢复动态三维场景的映射。
- $\mathcal{W}$：加入初始状态和物理参数后的可执行世界。
- $F_{\mathrm{id}}$：通过系统辨识把观测场景转化为可执行物理世界的映射。
- $q$：输入的自然语言问题。
- $\mathcal{R}_q$：针对问题生成的结构化执行记录，包括轨迹、接触、状态变化和干预。
- $F_{\mathrm{exec}}$：根据问题检查、延续或编辑世界的执行过程。
- $\hat{a}$：模型在问题答案空间中的最终预测。
- $F_{\mathrm{ans}}$：综合问题、视频、基础世界和执行证据形成答案的映射。

<div class="equation-explanation" markdown="1">

**直观理解**：该式规定了方法的信息边界：前两步只看视频，因此一个场景只需构建一次；问题仅影响后续执行和回答。这样可以区分“视频本身的物理事实”与“某个问题要求进行的检查或干预”，也是世界可复用和反事实结果可比较的基础。<br>
**原文位置**：第3.1节，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 物理参数的联合轨迹辨识目标

$$
\Theta^{*}=\arg\min_{\Theta}\Bigg[\sum_{i,t}w_{i,t}\|\widehat{\mathbf{p}}_{i}(t;\Theta)-\mathbf{p}_{i,t}\|_{2}^{2}+\lambda_{R}\sum_{i,t}w_{i,t}d_{R}\!\left(\widehat{R}_{i}(t;\Theta),R_{i,t}\right)^{2}+\lambda_{\mathrm{contact}}\mathcal{L}_{\mathrm{contact}}(\Theta)+\lambda_{\mathrm{reg}}\Omega(\Theta)\Bigg]
$$

**符号说明**

- $\Theta$：待辨识的物理参数集合，包括初速度、地面摩擦、成对质量比和恢复系数。
- $\Theta^{*}$：使联合目标最小的最终物理参数。
- $\widehat{\mathbf{p}}_{i}(t;\Theta)$：使用参数$\Theta$执行解析动力学后，物体$i$在时刻$t$的预测位置。
- $\mathbf{p}_{i,t}$：从视频重建并校正得到的物体$i$在时刻$t$的位置观测。
- $\widehat{R}_{i}(t;\Theta)$：解析动力学给出的物体$i$预测朝向。
- $R_{i,t}$：从视频恢复的物体$i$朝向观测。
- $w_{i,t}$：对应物体和时刻的观测置信权重。
- $d_R$：考虑物体旋转对称性的朝向距离，不惩罚视觉上不可区分的对称轴旋转。
- $\mathcal{L}_{\mathrm{contact}}$：候选接触损失，用于惩罚接触时仍有残余间隔或不符合接近条件的运动。
- $\Omega$：软接触物理先验或正则项，用于抑制不稳定、不合理的参数解。
- $\lambda_R,\lambda_{\mathrm{contact}},\lambda_{\mathrm{reg}}$：分别控制朝向误差、接触约束和正则项相对强度的权重。

<div class="equation-explanation" markdown="1">

**直观理解**：目标函数要求同一组参数同时解释物体的位置、朝向和接触事件，而不是分别拟合每一段表面运动。前两项让模拟轨迹贴近视频观测，接触项使碰撞的时间和几何关系合理，正则项则在视频证据不足时限制参数落入物理上可信的范围。<br>
**原文位置**：第3.3节“Analytic Continuous-Time System Identification”，公式(5)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用传统意义上的训练目标。PhysMind是训练自由框架，不使用任务数据更新SAM 3、深度模型、位姿模型或VLM的权重；公式(5)是每个视频在推理期执行的系统辨识目标，只优化该视频对应的物理参数$\Theta$，而非学习跨数据集共享的神经网络参数。优化前先从位移和减速度获得速度、摩擦的局部解析初始化；观测不足的起始状态采用保守的零速度初始化，随后在接触连通的物体组内联合拟合，必要时通过逐渐增长的时间前缀加入更晚发生的碰撞。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 几何感知的动态场景重建**

该模块组合SAM 3、MoGe-2、Video Depth Anything、SAM 3D Objects和FoundationPose：掩码轨迹建立跨帧身份，固定内参$K$与时间一致深度把二维观测提升到共享三维空间，规范网格$\mathcal{M}_i$为位姿注册和接触检测提供几何代理。随后由VLM按场景选择重力、支撑面或相机滚转约束，并以对称性感知规则处理球、立方体和圆柱的方向歧义。

> 直观理解：仅从二维像素看，两个物体靠得很近并不等于在三维中真正接触；深度、网格和统一坐标系使接触判断具有几何依据。约束校正则把多个工具各自可能合理、合在一起却矛盾的输出整理成同一个物理场景。

**2. 解析连续时间系统辨识**

状态$\mathbf{z}(t)$按运动模式划分为解析片段，片段内由闭式流$\Phi_k$计算，碰撞时由更新映射$\Delta_{k+1}$施加冲量响应。候选参数通过全轨迹拟合确定；接触连通分量内联合估计相对质量与碰撞参数，未发生接触的分量之间因绝对质量尺度不可观测，方法仅在新接触时使用语义先验和相似物体参数。

> 直观理解：这种设计直接计算“经过任意时长后物体在哪里”，不必把时间切成大量小步，因此避免固定步长模拟带来的长计算链。它仍显式保留碰撞造成的速度突变，适合需要比较事件先后和干预结果的问题。

**3. VLM编排的世界接口与证据回答**

问题$q$不会参与场景重建和参数辨识，只进入$F_{\mathrm{exec}}$与$F_{\mathrm{ans}}$。VLM根据问题和可调用函数模式完成语言指代消解、操作规划及执行时域选择；除非题目明确指定物理干预，否则它不能任意改动已拟合参数$\Theta^*$，回答阶段使用由执行产生的轨迹与事件摘要。

> 直观理解：VLM在这里更像实验操作员和结果解释员，而不是凭语言直觉猜测物理结论。将建模与提问分离还能保证不同问题面对同一个基础世界，反事实修改也发生在副本上，不会污染原始场景。

**训练与推理**

整个流程均在推理期运行。首先，在不知道具体问题的情况下，对视频执行物体分割、匿名身份跟踪、相机与深度估计、网格重建、六自由度位姿恢复以及场景约束校正，得到$\mathcal{S}$；然后提出候选接触区间，以分段解析动力学拟合$\Theta^*$并构造一次性的基础世界$\mathcal{W}$。这两部分不读取$q$，因此同一视频的解释、预测和反事实问题可共享重建与辨识结果。

问题到达后，VLM先从文本提取显式属性并将其绑定到物体身份；若仍有歧义，再结合候选物体图像完成指代消解。之后它依据问题类型调用检查、继续执行、复制、删除或参数编辑等世界操作：默认执行时域延伸至观测序列之后的20%，但可按问题需要调整；只有问题明确描述物理干预时才修改相应参数。最终，回答VLM接收问题、选项以及由$\mathcal{R}_q$整理出的紧凑证据，按要求输出结构化答案。

**复现信息**

公平理解该方法需要注意四点。第一，几何组件各有明确职责：SAM 3负责全视频掩码轨迹，MoGe-2估计采样帧内参并聚合成固定$K$，Video Depth Anything提供时间一致深度，SAM 3D Objects恢复规范网格，FoundationPose结合RGB、深度、掩码和内参进行双向位姿注册；VLM主要提供语义、约束选择和工具编排。第二，规则物体会重新拟合为几何基元，不规则网格则在保留可见表面的前提下简化；随后通过可见性感知渲染优化尺度和平移，但不改变前表面深度，以免利用掩码拟合破坏已有深度证据。

第三，碰撞候选来自网格邻近性而非数据集碰撞标签；自由飞行使用弹道闭式解，受支撑运动使用带显式停止时刻的精确库仑摩擦解，碰撞通过瞬时冲量更新衔接前后解析片段。第四，绝对质量无法仅由孤立运动或成对碰撞唯一确定，因此每个接触连通分量固定一个参考质量并估计质量比；跨分量尺度在新接触前不可观测，系统只能借助语义先验和视觉相似物体参数。上述选择说明输出是由视觉重建、有限物理模式和先验共同决定的估计，并非从视频中无歧义恢复全部真实物理量。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- CLEVRER：由平面桌面上的合成刚体运动视频构成，对象可进入或离开画面并发生碰撞。实验使用固定验证子集，共1,000个场景、4,280个多选问题和14,228个答案选项，覆盖解释、预测和反事实三类任务。解释题检验事件链与因果前提恢复；预测题检验从观测边界继续外推运动；反事实题要求移除指定对象后重新推演碰撞链。PhysMind只接收渲染视频和问题，不使用基准提供的真实运动轨迹或事件历史。
- Physion++：检验模型能否从已观察运动推断摩擦、质量等潜在机械属性，并预测观测结束后的目标物体接触。实验选择5个刚体类别、共384个试验，以每场景准确率为主；附录还报告匹配对准确率。匹配对具有相同的预测阶段初始摆放，但机械属性和接触结果不同，因此可进一步检查模型是否真正区分属性条件，而非依赖位置偏差。所有输入都在基准规定的预测边界结束，不包含结果帧。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**CLEVRER逐选项准确率**

把每个候选答案分别视为二元判断，衡量模型正确接受或拒绝单个选项的比例。它允许同一问题有零个、一个或多个正确选项，但可能掩盖同一道题中其他选项的错误。 （越高越好，因为表示单个候选事件判断更可靠。）

</div>
<div class="metric-item" markdown="1">

**CLEVRER逐问题准确率**

只有一道多选题的所有候选选项都判断正确时才计为正确，比逐选项准确率严格，更能反映模型是否完整恢复了因果链、未来事件集合或反事实事件集合。 （越高越好，因为表示整个答案集合完全正确；文中的总体比较和成本分析主要采用该指标。）

</div>
<div class="metric-item" markdown="1">

**Physion++逐场景准确率与匹配对准确率**

逐场景准确率衡量单个试验的未来接触预测是否正确；匹配对准确率要求机械属性和结果不同的一对试验均答对，用于检验模型能否稳定地区分由潜在物性造成的不同结局。 （两者均越高越好；匹配对指标更严格，也更能排除仅凭共同初始摆放猜测答案的可能。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### CLEVRER总体与各问题类型，重点比较PhysMind、同骨干Gemini-3-Flash CoT和GPT-5.5

<div class="result-value" markdown="1">

PhysMind达到逐问题72.55%、逐选项87.22%的总体准确率；相对同骨干CoT分别提高38.23和22.25个百分点，相对GPT-5.5分别提高5.31和3.56个百分点。最显著的收益来自反事实题：逐问题准确率比同骨干CoT高53.95个百分点，比GPT-5.5高19.25个百分点；但它在预测题上仍落后GPT-5.5达18.75个百分点。

</div>

作者结果表明，可执行世界最有价值的情形不是复述视频中已经出现的运动，而是删除对象后重新计算原视频中从未发生过的碰撞与后续事件。预测题上的落后说明，世界重建和动力学拟合并非在所有任务上都优于强视觉语言模型：当未来可由当前可见速度和运动趋势直接延续时，重建误差可能抵消显式模拟的收益。该结果支持“执行有助于反事实推理”，但不能单独证明模型恢复了真实物理参数，因为最终答案也可能受几何重建、事件提取和语言决策共同影响。

<div class="result-source" markdown="1">

来源：第4.2节，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 1 shows that PhysMind obtains the highest overall accuracy, reaching 72.55% per question and 87.22% per option. Relative to same-backbone CoT, the overall gains are 38.23 and 22.25 points; relative to GPT-5.5, they are 5.31 and 3.56 points. The advantage is concentrated in counterfactual reasoning, where PhysMind exceeds same-backbone CoT by 53.95 points per question and GPT-5.5 by 19.25 points. By comparison, PhysMind nearly matches GPT-5.5 on explanation, with a 0.24-point gap, but trails it by 18.75 points on prediction.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Physion++五类刚体未来接触预测，比较PhysMind、同骨干CoT和GPT-5.5

<div class="result-value" markdown="1">

PhysMind总体逐场景准确率为59.64%，比同骨干CoT高8.08个百分点，比GPT-5.5高1.57个百分点。相对同骨干CoT，摩擦碰撞和质量碰撞分别提高17.18和10.93个百分点，而摩擦平台下降1.56个百分点；相对GPT-5.5，PhysMind在五类中的四类领先1.05至3.13个百分点，但在摩擦碰撞上落后1.56个百分点。

</div>

这一分项模式检验可执行碰撞建模是否在答案依赖对象间相互作用时更有帮助。作者将碰撞类别上的较大增益解释为显式建模两体交互的贡献，而平台摩擦可从视频中的减速直接观察，额外建模未必占优。这个解释与结果一致，但属于机制推断而非直接因果证明；总体领先幅度较小，且类别间存在反向结果，因此不能概括为PhysMind在所有潜在物性推断上稳定优于GPT-5.5。

<div class="result-source" markdown="1">

来源：第4.2节，Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 2 reports 59.64% overall accuracy for PhysMind, improving same-backbone CoT by 8.08 points and GPT-5.5 by 1.57 points. Relative to same-backbone CoT, the gains concentrate on friction collision (17.18 points) and mass collision (10.93 points), while friction-platform accuracy decreases by 1.56 points. PhysMind also exceeds GPT-5.5 in four of five categories, with gains of 1.05–3.13 points, and trails it by 1.56 points on friction collision.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### CLEVRER准确率与令牌估算API成本的权衡

<div class="result-value" markdown="1">

PhysMind平均每题成本为0.01654美元；其逐问题总体准确率比GPT-5.5高5.31个百分点，而GPT-5.5成本是其6.30倍。与Gemini-3.1-Pro相比，PhysMind准确率高27.08个百分点，成本低24.7%。

</div>

该结果测试的是在实际API预算下，复用一次问题无关的世界重建是否比对每个问题调用昂贵大模型更划算。结果显示，在本文的模型价格、提示方式、令牌统计和共享重建协议下，PhysMind位于更有利的成本与准确率位置。不过这不是算法运行时间、GPU能耗或全生命周期成本的完整测量；API价格变化、同一视频包含的问题数量以及重建成本如何分摊，都可能改变结论。

<div class="result-source" markdown="1">

来源：第4.2节，Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Averaged over the evaluation questions, PhysMind costs $0.01654 per question. It improves overall accuracy over GPT-5.5 by 5.31 points, while GPT-5.5 costs 6.30 times as much. Compared with Gemini-3.1-Pro, PhysMind improves overall accuracy by 27.08 points and reduces cost by 24.7%.

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

- 同骨干直接CoT：以Gemini-3-Flash直接观察视频并进行思维链推理，与PhysMind使用相同的代理视觉语言模型。该对照最关键，因为它尽量固定语言与视觉能力，把差异集中在是否构建并执行物理世界。
- 强基础视觉语言模型：Qwen3-VL-235B-A22B、GLM-4.6V、Gemini-3.1-Pro、GPT-4o和GPT-5.5均使用CoT。它们检验PhysMind的结构化物理推演能否弥补模型规模或通用推理能力差距，其中GPT-5.5是文中最强的被评估视觉语言模型对照。
- 训练式视频推理方法：VideoRFT、Video-R1、VideoThinker-R1和Chain-of-Frames。该组用于比较无需训练的可执行世界方法与依赖任务训练或强化学习的视频推理方案，但不同方法的训练数据和输入接口可能不同，因此不是完全受控的组件比较。
- 训练自由代理方法与弱参考：VideoAgent、STAR用于比较其他无需训练的代理式视频推理；随机和盲猜参考用于刻画不利用有效视觉物理证据时的基准水平。

**实验想回答的问题**

- 在不针对基准训练或微调的条件下，PhysMind把视频重建为可编辑、可执行的物理世界后，是否比同一视觉语言模型直接进行思维链推理，以及比更强的基础视觉语言模型和已有视频推理方法，更准确地回答因果解释、未来预测、反事实干预和未来接触问题？
- 性能提升究竟来自哪些环节：解析式动力学辨识、跨帧位姿校正，还是对重建世界的实际执行？这种收益是否主要出现在必须改变场景并重新推演、因而无法直接从已观察轨迹读取答案的反事实问题上？

**实验实现**

PhysMind全程使用Gemini-3-Flash作为代理模型；每段视频只进行一次与具体问题无关的世界重建，同一视频的多个问题共享该重建结果。所有组件都未在CLEVRER或Physion++上训练或微调。Gemini系列基线接收观测视频；不支持视频的接口接收按时间顺序采样的帧，CLEVRER为8帧、Physion++为16帧。Physion++的视频和采样帧输入均保留场景冻结后由基准提供的红色、黄色目标提示，避免把目标识别与物理预测完全混在一起。主实验还比较由令牌用量估算的API成本。需要注意，CLEVRER采用固定验证子集而非完整验证集，消融则使用其中相同的100场景子集；这使同表内比较可复现，但总体数值仍可能受子集选择影响。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 以固定步长数值积分替换解析式动力学辨识 | 总体准确率从73.10%降至30.80%，下降42.30个百分点；解释、反事实和预测准确率分别下降43.87、47.03和25.71个百分点。该总体损失大于移除位姿校正造成的25.05个百分点损失，也大于只使用轨迹而不执行造成的32.56个百分点损失。 | 此消融主要隔离连续时间解析辨识相对固定步长展开的作用。大幅下降表明，在匹配的消融设置中，避免逐步积分的误差累积和不稳定性对恢复事件时序及反事实碰撞链非常重要，尤其影响解释与反事实题。不过该替换可能同时改变优化难度和轨迹精度，因此不能把全部差值简单解释为“解析公式本身”的纯贡献。 | 第4.3节，Figure 4<br><span class="experiment-evidence">Replacing analytic identification with fixed-step numerical integration produces the largest overall loss, reducing accuracy from 73.10% to 30.80%. Its 42.30-point drop exceeds the losses from removing pose correction (25.05 points) and using trajectories without execution (32.56 points). Analytic identification has a larger effect on explanatory and counterfactual accuracy, which decrease by 43.87 and 47.03 points, than on predictive accuracy, which decreases by 25.71 points.</span> |
| 仅根据已恢复轨迹回答，不执行可编辑世界 | 仅使用轨迹时，预测准确率由60.00%小幅升至61.43%，但反事实准确率由71.89%降至16.22%，形成55.67个百分点差距。 | 这是最直接检验“执行是否必要”的消融：轨迹仍提供原视频中的可见运动证据，却无法在移除对象后生成新的碰撞链。预测不降反升说明执行并不天然改善普通外推；反事实的巨大下降则把主要收益定位到干预后的重新推演。它有力支持执行模块的任务针对性，但仍不能排除完整系统中的编辑逻辑和事件读取器共同贡献。 | 第4.3节，Figure 4<br><span class="experiment-evidence">Trajectory-only answering slightly increases predictive accuracy from 60.00% to 61.43%, but reduces counterfactual accuracy from 71.89% to 16.22%. The 55.67-point counterfactual gap separates access to observed motion from the ability to evaluate an intervention.</span> |

**定性案例**

- 对CLEVRER的100场景子集进行人工错误归因时，作者把错误归到“最早出现且足以导致失败的可见不一致”：典型链条包括对象掩码合并或残缺后引发位姿错误、碰撞时刻或碰撞拓扑拟合错误，以及微小轨迹偏差在长时预测中演化为接触判断错误。该分析说明主要瓶颈位于可执行世界的构建质量，而不是世界已经正确后最终语言回答阶段；但人工归因依赖判定者对“最早充分原因”的主观判断，且只覆盖100个场景。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work develops an agentic executable-world framework for physical, predictive, and counterfactual reasoning over video.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`ca32bf8d4e7df6eb6fa355a7e012012b593ba548c8fc89d1eb57073383eefd09`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
