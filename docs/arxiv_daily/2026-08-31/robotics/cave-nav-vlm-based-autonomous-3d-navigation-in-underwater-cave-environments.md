---
title: "[论文解读] CAVE-NAV: VLM-Based Autonomous 3D Navigation in Underwater Cave Environments"
description: "[arXiv 2608.27793][机器人 / 具身智能] 原文未明确报告。"
arxiv_id: "2608.27793"
announcement_date: "2026-08-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:44:30.901848+00:00"
source_sha256: "88999705ea5a6b864adafd488d678be336e78a99c1be5b9c2a69714eafae59f8"
tags:
  - "机器人 / 具身智能"
  - "VLM Reasoning"
  - "LLM Reasoning"
  - "多模态 VLM"
  - "水下洞穴导航"
  - "自主水下航行器"
  - "视觉语言模型"
  - "思维链推理"
  - "多模态感知"
  - "三维安全净空"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2608.27793</p>

# CAVE-NAV: VLM-Based Autonomous 3D Navigation in Underwater Cave Environments

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Zhenqi Wu, Yuanjie Lu, Yisheng Zhang, Miao Yu, Xuesu Xiao, Jaejeong Shin, Xiaomin Lin</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Embodied Robotics and Automation Lab, University of South Florida, Tampa, FL 33620, USA. {zhenqi；Affiliation: Computer Science Department, George Mason University, Fairfax, VA 22032, USA；Affiliation: Department of Mechanical Engineering, University of Maryland, College Park, MD 20742, USA. {yiszhang；Affiliation: Naval Architecture and Ocean Engineering at the Seoul National University, Seoul 08826, South Korea</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27793v1) · [PDF 下载](https://arxiv.org/pdf/2608.27793v1) · **关键词** 水下洞穴导航, 自主水下航行器, 视觉语言模型, 思维链推理, 多模态感知, 三维安全净空<br>


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

本文属于自主水下机器人导航研究，目标场景是未知、狭窄且无法依赖外部通信的水下洞穴。传统系统通常以视觉同步定位与建图（SLAM）、视觉—惯性里程计或声呐建图估计机器人位姿和障碍物几何，但洞穴中的悬浮颗粒、低纹理岩壁、非均匀自带照明和声学多径会削弱特征匹配与精细重建；顶部封闭还使水面声学基站和实时人工指导不可用。本文据此把核心问题从“精确重建整座洞穴”转为“根据当前多模态观测判断哪个三维方向可安全通行”，并利用视觉语言模型（VLM）综合理解亮度变化、通道形态和结构复杂度。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉同步定位与建图（Visual SLAM）**

机器人通过连续图像中的可重复视觉特征，同时估计自身运动并构建环境地图。水下洞穴的散射、低纹理和随机器人移动而变化的照明会破坏特征对应，进而造成跟踪失败和累计漂移。

</div>
<div class="concept-item" markdown="1">

**视觉语言模型（VLM）**

VLM能够联合处理图像与文字指令，并用语言形式表达对场景和任务约束的理解。本文关注的不是识别单个物体，而是让模型结合多种传感输入判断洞穴通道的可通行方向。

</div>
<div class="concept-item" markdown="1">

**思维链提示（Chain-of-Thought, CoT）**

思维链提示要求模型在给出最终决策前，按步骤检查观测线索和安全约束。本文用零样本CoT促使VLM先考虑净空、通道形态与照明等因素，再输出三维运动命令。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务是在预先未知的水下洞穴中，使自主水下航行器连续选择安全的三维运动方向并完成端到端穿越。每个决策步的输入包括RGB图像、深度图和基于声呐得到的垂直净空观测；模型据此解释光照强度梯度、通道形态及几何复杂度，并输出可直接作用于航行器位姿的参数化三维运动命令。场景假设包括可见度退化、低纹理与非均匀主动照明、狭窄且不规则的三维通道、声学多径，以及通信中断；因此系统不能依赖实时人工指导、预装洞穴引导线、稳定的外部定位参考或经过标定且固定的人工照明几何。安全目标是在保持洞壁净空并避免碰撞的前提下持续前进，而不是优先获得完整、精确的度量地图。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **基于人工照明几何的水下洞穴立体视觉建图方法 [7]**: 该方法利用经过标定的人工照明几何重建洞穴边界，但现场难以持续保持标定关系，而且只能描述照明覆盖区域。CAVE-NAV不把固定照明几何作为前提，而是将当前RGB、深度和垂直净空作为环境线索，用于直接判断可通行方向。
- **CavePI [1]**: CavePI通过实时语义分割检测并跟随预先铺设的洞穴引导线，证明了语义感知可用于洞穴导航，但其决策依赖外加的明确引导标志。CAVE-NAV面向没有预装引导线的未知洞穴，尝试直接从洞穴自身的通道结构、光照模式和净空信息中推断三维行动方向。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

水下洞穴中的自主导航服务于搜救、科学探测和紧急撤离，但机器人必须在浑浊、低纹理、通信中断且通道狭窄的三维环境中持续判断前进方向。洞穴边界和通行空间可能随高度、转弯和障碍物快速变化，因此系统不仅要定位，还要在缺乏人工引导的情况下选择具有足够安全余量的路径。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于视觉特征的定位、建图与规划**：系统从连续图像中提取并匹配局部视觉特征，利用视觉同步定位与建图（SLAM）估计机器人位姿、构建环境地图，再据此进行分层规划。其基本前提是不同图像之间存在稳定、可重复的视觉对应关系。
- **依赖人工条件的洞穴导航方法**：一类方法利用人工照明的几何关系重建洞穴边界；另一类方法（如 CavePI）通过实时分割预先铺设的洞穴引导绳，并沿绳导航。这些方法把可用的照明结构或明确的人工路线作为导航依据，而不是直接从未知洞穴本身推断可通行方向。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 视觉特征方法在水下洞穴中缺少可靠观测：悬浮沉积物会散射光线，低纹理岩壁难以提供足够的特征对应关系，而机载照明变化又破坏特征跟踪所依赖的亮度恒常性假设。其后果是跟踪失败和定位漂移累积，使系统在狭窄且容错率低的环境中难以稳定工作。
- 现有洞穴专用方法依赖现场预先提供的条件：照明几何法只在人工照明能够覆盖的区域刻画边界，且需要维持校准的照明布置；引导绳分割法则要求洞穴中已经安装可识别的绳索。因而它们无法充分支持对未探索、无人工基础设施洞穴的自主导航。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未解决这样一个具体问题：在不依赖密集视觉特征、预建地图、持续通信或人工铺设路线的前提下，机器人如何把 RGB 图像、深度图和声呐垂向净空观测结合起来，从洞穴的光照梯度、通道形态和几何复杂度中推断安全的三维运动方向，并将边界净空要求纳入决策过程。

</div>
<div markdown="1"><span>核心问题</span>

视觉语言模型（VLM）能否通过零样本思维链（CoT）推理，把多模态环境观测解释为关于通道形态、照明变化和结构复杂度的语义信息，同时遵守净空约束，进而在未知的水下洞穴中生成无碰撞且具有安全边界余量的三维导航指令？

</div>
<div markdown="1"><span>作者直觉</span>

洞穴导航并不总是需要先建立精确的全局地图；在局部决策层面，机器人可以根据前方是否更明亮、通道是否更宽、空间结构是否更简单以及当前垂向净空是否足够来判断哪一方向更可能安全。VLM 的作用是把这些异质观测组织成可解释的环境判断，CoT 则要求模型先逐步检查净空和几何约束，再输出运动指令。直观地说，该框架试图用“理解当前空间结构并筛除不满足安全条件的方向”补充传统定位方法，而不是仅依靠可重复的视觉纹理。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CAVE-NAV采用闭环的“感知—规划—执行”流程：自主水下航行器（AUV）在每个时刻获取前向RGB图像、深度图以及顶部和底部声呐距离，将这些信息与任务提示共同输入视觉语言模型（VLM）。VLM通过零样本Chain-of-Thought（CoT）推理判断可通行方向，并输出带有简短理由的运动指令；系统解析指令，将其直接施加到仿真器中的航行器位姿，再获取下一时刻观测，循环推进。整体方法不依赖显式的稠密特征定位、全局地图或在线人工控制，而是让模型依据通道形态、可见开口和上下净空进行局部决策。直观地说，VLM像一个根据摄像头和测距仪实时“看路”的驾驶员：先判断哪里更宽、更安全，再决定前进、转向或上下移动，并立即检查下一帧环境。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多模态环境感知

RGB-D相机提供场景外观和前方表面距离；系统将原始深度按用户设定的最小值 $D_{\min}$ 与最大值 $D_{\max}$ 归一化到 $[0,1]$，再编码为VLM可读取的8位PNG图像。两个声呐补充航行器与洞顶、洞底之间的垂直净空信息。

<div class="method-step__io" markdown="1">

**输入**：仿真器在时刻 $t$ 渲染的RGB图像 $I_{\mathrm{rgb}}$、原始深度图 $D_{\mathrm{raw}}$，以及两个单束回声测深仪测得的顶部距离 $d_{\mathrm{top}}$ 和底部距离 $d_{\mathrm{bottom}}$。<br>
**输出**：处理后的观测集合 $(I_{\mathrm{rgb}},D_{\mathrm{norm}},d_{\mathrm{top}},d_{\mathrm{bottom}})$。

</div>

**直观理解**：相机负责回答“前面看起来是什么、通道向哪里延伸”，深度图负责回答“前方哪里近、哪里远”，上下声呐则防止航行器撞到顶或底。这样即使洞穴缺少稳定的视觉特征，系统仍能利用空间开阔程度来判断方向。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### VLM提示与CoT规划

结构化提示说明各传感器的语义，并要求VLM依次进行情境评估、约束分析和动作选择。提示优先保证安全而非效率，目标是保持约 $2.0\,\mathrm{m}$ 的边界间隔；若前方障碍物距离小于 $1.5\,\mathrm{m}$，则禁止继续前进并转向最清晰方向，同时在多个开口中优先选择延续当前通道且不立即反向的方向。

<div class="method-step__io" markdown="1">

**输入**：多模态观测 $(I_{\mathrm{rgb}},D_{\mathrm{norm}},d_{\mathrm{top}},d_{\mathrm{bottom}})$、固定系统提示和任务提示 $p_{\mathrm{task}}$，例如“探索洞穴通道并避免碰撞”。<br>
**输出**：一个离散导航动作 $a\in\mathcal{A}$ 及其文字理由；动作集合包括前进、左转、右转、上升和下降等基本运动原语。

</div>

**直观理解**：提示词相当于给模型一套驾驶规则：先避免撞击，再考虑怎样继续深入洞穴。CoT要求模型先说清楚“看到了什么、受什么限制、因此怎么做”，使决策不只是一个难以检查的动作标签。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 动作解析与合法性检查

解析器将动作字符串转换为刚体增量 $a_t=(\Delta f_t,\Delta r_t,\Delta z_t,\Delta\psi_t)$，分别表示机体坐标系中的前向、右向、竖直位移和偏航变化。前向与右向位移只能取规定的离散值，偏航只能取规定角度集合，竖直位移取 $[0.1,2.0]$ 米；无法解析或越界的输出会触发重新询问，持续失败则终止运行。

<div class="method-step__io" markdown="1">

**输入**：VLM返回的单键值字典，其中键是含运动类型和幅度的动作字符串，值是关于净空、备选方向和选择理由的简短说明。<br>
**输出**：通过约束检查的四维运动指令 $(\Delta f_t,\Delta r_t,\Delta z_t,\Delta\psi_t)$，或一次重新询问/终止事件。

</div>

**直观理解**：这一步像把驾驶员的自然语言转换成车辆能执行的标准控制量，并检查它是否在安全、可实现范围内。限制动作幅度还能避免模型一次移动过远而越过安全余量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 位姿执行与闭环更新

仿真器先更新偏航角 $\psi_{t+1}=\psi_t+\Delta\psi_t$，再依据更新后的航向将机体坐标系中的前向、右向位移转换到世界坐标系，并更新 $x$、$y$、$z$ 位置。执行后重新渲染传感器观测，判断是否继续遍历，形成下一轮闭环。

<div class="method-step__io" markdown="1">

**输入**：合法动作增量 $(\Delta f_t,\Delta r_t,\Delta z_t,\Delta\psi_t)$ 以及当前位姿 $(x_t,y_t,z_t,\psi_t)$。<br>
**输出**：下一时刻航行器位姿和新的多模态观测；循环直至完成洞穴端到端遍历、发生持续解析失败或达到实验终止条件。

</div>

**直观理解**：模型不是一次性规划整条路线，而是每走一步就重新观察环境。类似人在陌生洞穴中逐步前进：走完当前动作后，根据新的视野重新决定下一步。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 深度归一化

$$
D_{\mathrm{norm}}(u,v)=\frac{D_{\mathrm{raw}}(u,v)-D_{\min}}{D_{\max}-D_{\min}}
$$

**符号说明**

- $D_{\mathrm{norm}}(u,v)$：像素坐标 $(u,v)$ 处归一化后的深度值，范围为 $[0,1]$。
- $D_{\mathrm{raw}}(u,v)$：像素坐标 $(u,v)$ 处的原始深度值。
- $D_{\min}$：用户设定的深度下界。
- $D_{\max}$：用户设定的深度上界。
- $(u,v)$：深度图中的像素坐标。

<div class="equation-explanation" markdown="1">

**直观理解**：该变换把可能具有不同数值范围的原始深度压缩到统一的 $[0,1]$ 区间，再转成图像供VLM读取。归一化后的相对明暗关系保留了“近处与远处”的空间线索，但原文未进一步说明 $D_{\min}$ 和 $D_{\max}$ 的具体数值。<br>
**原文位置**：III-A Perception Module，式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 动作增量表示

$$
a_t=\bigl(\Delta f_t,\,\Delta r_t,\,\Delta z_t,\,\Delta\psi_t\bigr)
$$

**符号说明**

- $a_t$：时刻 $t$ 的完整运动动作。
- $\Delta f_t$：机体坐标系中的前向位移。
- $\Delta r_t$：机体坐标系中的右向位移。
- $\Delta z_t$：竖直位移。
- $\Delta\psi_t$：偏航角增量。

<div class="equation-explanation" markdown="1">

**直观理解**：该表示将VLM的一次决策统一成四个可执行量，因此一次响应同时决定前后、左右、上下移动和转向。它使自然语言动作能够被确定性地解析为仿真器控制指令；原文随后给出了各分量的允许范围，但这里省略这些常数集合以突出核心表示。<br>
**原文位置**：III-D-1 Output Format，式(2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文将该方法描述为零样本VLM推理，并未报告针对洞穴导航数据进行参数训练、损失函数或优化目标。因此本方法没有可从所给章节确认的训练目标；主要“优化”发生在提示设计和动作约束层面，而非模型参数更新。安全优先级、约 $2.0\,\mathrm{m}$ 的期望边界间隔以及受限动作幅度属于推理时规则，不应误解为通过梯度优化学习得到的目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. RGB-D与垂直净空感知模块**

输入包括 $I_{\mathrm{rgb}}\in\mathbb{R}^{H\times W\times3}$、$D_{\mathrm{raw}}\in\mathbb{R}^{H\times W}$ 以及 $(d_{\mathrm{top}},d_{\mathrm{bottom}})$。深度图被归一化为 $D_{\mathrm{norm}}$ 并转换为8位PNG；顶部和底部单束声呐提供前向相机无法充分表达的垂直安全信息。

> 直观理解：该模块把不同传感器的信息整理成模型能同时理解的输入，尤其补足“上方和下方是否有足够空间”这一三维导航所需信息。

**2. 基于结构化提示的VLM规划模块**

VLM接收图像、深度、垂直净空和任务提示 $p_{\mathrm{task}}$，通过零样本CoT完成情境评估、约束分析和动作选择。提示显式规定深度图的语义：较暗区域代表较近障碍物，较亮区域代表较远、较开放的区域，并编码安全优先、障碍规避和目标导向探索三类策略。

> 直观理解：研究重点不是训练一个专门的洞穴控制器，而是通过提示把通用VLM的视觉理解能力转化为导航规则，使它直接从通道形态中寻找可走方向。

**3. 动作解析与运动学执行模块**

VLM输出被约束为单个键值对，解析为 $a_t=(\Delta f_t,\Delta r_t,\Delta z_t,\Delta\psi_t)$。系统进行格式和幅度检查后，将机体坐标系位移转换到世界坐标，并按位姿更新方程直接修改仿真器中的航行器状态；解析失败会重新询问，持续失败则结束运行。

> 直观理解：该模块连接“模型的判断”和“航行器的实际移动”，同时让每一步都有可审计的理由，并防止不合法输出直接进入执行器。

**训练与推理**

训练阶段：原文未报告CAVE-NAV对VLM进行微调、监督学习或强化学习训练，明确描述的是zero-shot CoT prompting。推理阶段首先采集并预处理RGB-D和上下声呐数据，然后将观测与任务提示输入VLM；VLM按“情境评估—约束分析—动作选择”生成带理由的单动作输出，解析器将其映射为四维运动增量并检查格式和范围；合法动作被施加到仿真器位姿，系统获取下一轮观测并重复上述过程，直至遍历完成或运行终止。

**复现信息**

复现时需要保留以下与行为直接相关的约束：输入由前向RGB-D相机和两个单束回声测深仪组成，深度图采用用户设定范围归一化后保存为8位PNG；动作输出限制为单个键值对，前向和右向位移的绝对值从 $\{0,0.1,0.2,0.5,1.0\}\,\mathrm{m}$ 中选择，偏航角从 $\{0,5,10,15,20,30,45,90,180\}^{\circ}$ 中选择，竖直位移绝对值位于 $[0.1,2.0]\,\mathrm{m}$。提示中要求在安全距离不足时将前进位移限制为 $0.1$–$0.2\,\mathrm{m}$ 并结合转向或竖直调整，在前方 $1.5\,\mathrm{m}$ 内有障碍物时完全停止前进；原文未明确报告VLM的具体型号、推理温度、调用次数上限、$D_{\min}$ 和 $D_{\max}$ 的数值，以及持久解析失败的具体次数阈值。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Blender 生成的高保真仿真洞穴环境：共 5 个场景、未报告训练集或测试集划分。S1 测试多重狭窄处的间隙感知规划；S2 测试狭窄通道与垂直起伏结合下的三维机动；S3 测试 frontal 与 lateral 障碍物条件下的避碰；S4 测试 90 度急转弯中的预判和航向调整；S5 测试不规则几何与分布式障碍物构成的复杂拓扑。其作用是覆盖受限空间、垂直机动、急转弯和杂乱环境等核心挑战。
- BlueROV2 仿真配置：采用前向 RGB 相机、同位置深度相机，以及朝上和朝下的深度相机来模拟单波束声呐的顶部和底部间隙测量。RGB 图像分辨率为 $640\times480$；每个时间步从上下深度相机分别提取最近距离 $d_{\mathrm{top}}$ 和 $d_{\mathrm{bottom}}$。该配置用于验证融合视觉场景、障碍物距离和垂直净空后的导航行为，而非构成独立数据集。
- Blue Grotto, Florida 的真实 BlueROV2 RGB 图像：原文仅报告使用真实设备在 Blue Grotto 拍摄的图像进行一次提示推理，未报告样本数量、数据划分或系统化测试规模。其作用是进行超出仿真范围的定性迁移检查。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务完成率**

完成从起点到洞穴目标或出口的端到端穿越的试验比例；文中以各仿真环境是否完成完整穿越来报告。 （越高越好，因为它直接表示导航任务是否成功。）

</div>
<div class="metric-item" markdown="1">

**碰撞次数**

导航过程中车辆与洞穴边界或障碍物发生碰撞的次数。 （越低越好；零碰撞表示轨迹没有撞到墙壁、顶部、底部或分布式障碍物。）

</div>
<div class="metric-item" markdown="1">

**边界间隙或安全间隔**

车辆轨迹与洞穴墙壁、顶部和底部边界之间的空间距离。文中强调保持预设的 nominal standoff，但没有给出汇总数值。 （在不发生碰撞的前提下，应保持足够且稳定的间隙；过小增加碰撞风险，过大则可能降低狭窄通道的可通行性。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 五种 Blender 仿真洞穴拓扑的端到端导航

<div class="result-value" markdown="1">

在 S1 至 S5 五个环境中，AUV 的任务完成率为 $100\%$，碰撞次数为零。

</div>

该结果表明系统在作者设计的五类几何挑战中都完成了完整穿越，并且没有撞击障碍物或洞穴边界。它支持方法在这些仿真场景中的可行性，但不等于已经证明系统在真实水下洞穴、更多随机环境或不同模型接口条件下具有同样的可靠性。

<div class="result-source" markdown="1">

来源：IV-B Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across all five environments, the AUV achieved 100% task completion with zero collisions, validating the framework’s ability to generalize across diverse cave topologies.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 仿真轨迹的空间安全性与三维避障

<div class="result-value" markdown="1">

五个场景的轨迹均保持在洞穴中心附近，并在墙壁、顶部和底部之间维持适当间隙；在 S3 中，车辆通过同时上升和横向位移避开正面及侧面障碍物。

</div>

这说明系统不只是沿二维平面前进，而是能够利用垂直间隙信息进行三维机动，并在受限空间中调整位置。不过原文没有提供最小间隙、轨迹长度、路径效率或控制平滑性的数值，因此无法判断其安全裕度和效率是否优于其他方法。

<div class="result-source" markdown="1">

来源：Fig. 3 and IV-B Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The orange trajectory consistently remains near the center of each cave, demonstrating collision-free navigation with appropriate clearance from walls, ceiling, and floor.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 真实 Blue Grotto 图像上的仿真外迁移检查

<div class="result-value" markdown="1">

对 BlueROV2 在 Florida 的 Blue Grotto 拍摄的 RGB 图像进行同一提示推理时，模型识别出上方明亮开口和左侧近墙，并建议上升、向右偏航和短距离前进的组合动作。

</div>

该案例说明 VLM 能把真实图像中的亮度、开口方向和近距离边界转化为方向性建议，初步显示从仿真视觉分布向真实图像迁移的可能性。但这不是完整的真实水下闭环实验：原文未报告实际执行这些动作后的轨迹、碰撞、成功率或重复次数。

<div class="result-source" markdown="1">

来源：Fig. 4 and IV-B Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The model identified the bright overhead opening, noted the near wall on the left, and proposed a combined ascent, right yaw, and short forward step consistent with the observed geometry.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验主要依赖 Blender 仿真和 5 个人工设计场景，未报告真实洞穴中的闭环航行、传感器噪声、浑浊水体、动态水流或通信延迟，因此仿真中的 $100\%$ 完成率和零碰撞不能直接外推到真实水下任务。
- 原文未报告传统导航方法、其他 VLM、去除 CoT 或去除某一模态的基线和消融，也未报告重复次数、方差、路径长度、时间、能耗或最小安全间隙等定量指标；因此无法分辨性能来自 VLM 推理、提示设计、多模态输入还是场景结构，并且无法评价效率与统计稳健性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未报告与传统特征定位或建图系统的定量基线比较。
- 原文未报告与其他 VLM 导航方法的定量基线比较。
- 原文未报告无 CoT 推理、单模态输入或其他控制策略的基线比较。

**实验想回答的问题**

- CAVE-NAV 能否在具有狭窄通道、垂直起伏、障碍物、急转弯和复杂拓扑的水下洞穴中完成安全的三维自主导航？
- 仅依据多模态观测和 VLM 推理得到的动作，能否在不同洞穴拓扑之间保持无碰撞通行，并对真实 BlueROV2 图像产生合理的导航建议？

**实验实现**

实验在 Blender 生成的高保真洞穴中进行，环境包含真实感岩石纹理、变化光照和不规则边界。车辆为模拟 BlueROV2；每个决策步通过 OpenAI API 查询一次 CAVE-NAV，输入最近的两次观测，即 $K=2$，每次试验最多执行 $T_{\max}=150$ 步。前向 RGB、深度和垂直间隙图像均为 $640\times480$ 像素；深度值从 $D_{\min}=0$ 米到 $D_{\max}=20$ 米归一化；提示词指定与所有表面保持名义上的 $2$ 米间隔。文中未报告随机种子、每个场景的重复试验次数、统计置信区间、成功判定的精确终点规则或与基线统一的计算预算，因此结果更接近场景级验证，而不是完整的统计比较。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- Blue Grotto 真实图像案例：模型观察到上方明亮开口和左侧近墙后，建议上升、右偏航和短前进。该建议与图像几何关系一致，说明 VLM 可以将视觉线索转化为复合三维动作；但因为动作未被报告为实际执行并缺少重复试验，它应被解释为迁移可行性的定性展示，而不是性能指标。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It proposes a VLM with chain-of-thought reasoning for autonomous 3D navigation of underwater robots using multimodal environmental cues.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`88999705ea5a6b864adafd488d678be336e78a99c1be5b9c2a69714eafae59f8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
