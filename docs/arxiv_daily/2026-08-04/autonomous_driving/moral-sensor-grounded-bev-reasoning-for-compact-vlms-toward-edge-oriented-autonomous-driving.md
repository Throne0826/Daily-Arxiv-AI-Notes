---
title: "[论文解读] MoRAL: Sensor-Grounded BEV Reasoning for Compact VLMs toward Edge-Oriented Autonomous Driving"
description: "[arXiv 2608.02449][自动驾驶] 原文未明确报告。"
arxiv_id: "2608.02449"
announcement_date: "2026-08-04"
primary_category: "autonomous_driving"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:00:49.330859+00:00"
source_sha256: "d51a9b42c77afd14f91801d103c8c073195139a926d1743e446ffb30ca808965"
tags:
  - "自动驾驶"
  - "VLM Reasoning"
  - "VLM Efficiency"
  - "LLM Reasoning"
  - "视觉语言模型"
  - "鸟瞰图"
  - "多传感器融合"
  - "度量空间落地"
  - "物理推理"
  - "边缘计算"
  - "低秩适配"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">自动驾驶 · arXiv 2608.02449</p>

# MoRAL: Sensor-Grounded BEV Reasoning for Compact VLMs toward Edge-Oriented Autonomous Driving

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Ambarish Govindarajulu Kaliamurthi, Kaikai Liu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> San Jose State University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.02449v1) · [PDF 下载](https://arxiv.org/pdf/2608.02449v1) · **关键词** 自动驾驶, 视觉语言模型, 鸟瞰图, 多传感器融合, 度量空间落地, 物理推理, 边缘计算, 低秩适配<br>


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

本文处于自动驾驶多传感器感知与视觉语言模型（VLM）推理的交叉领域。车载系统需要根据激光雷达和毫米波雷达等传感器信息理解车辆周围物体的类别、距离、相对速度及潜在碰撞风险，但同时受到模型大小、推理延迟和流水线复杂度的严格限制。传统方案通常先用多视角视觉骨干、空间交叉注意力和学习式传感器融合构建鸟瞰图（BEV），再执行规划或语言推理；本文研究另一种设置，即在输入图像中用确定性规则显式编码物理量，使紧凑型VLM主要负责读取既定空间词汇并进行安全决策推理，而不必在推理时运行学习式三维感知骨干。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**鸟瞰图（Bird’s Eye View, BEV）**

BEV把车辆周围的三维场景投影到以自车为中心的俯视平面，使前后左右的位置关系和距离更容易直接表示。本文的BEV还把激光雷达距离编码为颜色带、把物体类别编码为点簇形态，并以方向楔形叠层表示雷达多普勒速度。

</div>
<div class="concept-item" markdown="1">

**度量空间落地（metric spatial grounding）**

它要求模型的回答真正对应传感器测得的距离、速度和几何关系，而不只是生成语言上合理的驾驶描述。DriveBench指出，部分VLM在移除视觉输入后仍能给出看似可信的回答，说明其可能依赖语言先验而非场景几何。

</div>
<div class="concept-item" markdown="1">

**低秩适配（Low-Rank Adaptation, LoRA）**

LoRA冻结原模型权重，并用两个低秩矩阵表示权重增量，从而只训练少量新增参数。若原权重为$W_0\in\mathbb{R}^{d\times k}$，更新写作$W=W_0+BA$；当秩$r\ll\min(d,k)$时，每层可训练参数由$dk$降为$r(d+k)$。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是在资源受限的车载边缘平台上进行开放环安全推理，而不是直接输出闭环驾驶轨迹。输入是由nuScenes中的激光雷达和雷达数据确定性渲染得到的物理编码BEV图像，以及关于驾驶场景的问题；图像以颜色、点簇形态和方向楔形分别承载距离、物体类别和多普勒速度信息。模型需要先把这些视觉符号还原为可用的度量事实，再基于距离、速度、碰撞轨迹、碰撞时间或制动需求生成自然语言判断。该设置假定BEV渲染阶段已经完成基础传感器投影与物理量编码，因此所讨论的VLM不承担从原始传感器数据学习三维表示的任务；输出侧关注八类物理落地的驾驶问答和安全决策质量，不与面向CARLA闭环轨迹执行的方法作直接指标比较。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$W_0\in\mathbb{R}^{d\times k}$**

被冻结的预训练层权重矩阵，其中$d$和$k$分别表示输出维度与输入维度。

</div>
<div class="notation-item" markdown="1">

**$W=W_0+BA$**

LoRA适配后的权重；$BA$是训练得到的低秩权重增量。

</div>
<div class="notation-item" markdown="1">

**$r$**

LoRA增量矩阵的秩，并满足$r\ll\min(d,k)$。

</div>
<div class="notation-item" markdown="1">

**$r(d+k)$**

使用LoRA后该层需要训练的参数量，相比完整权重的$dk$更小。

</div>

</div>

**直接相关的工作**

- **DriveBench**: 它在19,200帧和12种常用VLM上揭示了自动驾驶VLM的传感器落地问题：即使移除视觉输入，模型仍可能生成貌似合理的回答。该结果构成本文问题设定的直接依据，即流畅回答不能证明模型真正读取了距离、速度和几何信息。
- **VLA-MP**: 这是文中认为最接近的已发表系统，其通过ResNet50、PointPillar、BEVFusion、Q-Former、LLaVA-7B及动力学适配器实现多模态BEV感知和轨迹输出。MoRAL改用确定性BEV渲染与紧凑型2B模型，目标是nuScenes上的开放环安全推理，而VLA-MP面向LangAuto/CARLA闭环轨迹执行，因此原文明确指出二者不宜直接比较指标。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

车载自动驾驶平台必须在有限的显存、算力和时延预算内，根据传感器数据可靠判断目标距离、运动速度与潜在碰撞轨迹。安全决策既要求可度量的空间依据，又不能依赖过于庞大、复杂的推理流水线；例如紧急制动场景一旦漏检，语言上看似合理的回答也没有实际安全价值。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于学习式鸟瞰图构建的多传感器感知系统**：先用多视角相机骨干网络、空间交叉注意力和学习式传感器融合，将相机、LiDAR、雷达等信息转换为鸟瞰图（BEV）特征，再把这些特征交给下游检测、预测或驾驶决策模块。其优势是能从原始传感器输入中联合学习空间表征。
- **大型视觉语言模型的零样本驾驶推理**：直接向预训练视觉语言模型提供驾驶场景图像或工程化 BEV，并通过自然语言提示要求模型识别风险、解释场景或给出驾驶决策，主要依靠模型既有的视觉能力与语言先验，而不针对传感器编码规则进行专门训练。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 学习式 BEV 系统在推理时仍需运行多视角视觉骨干、空间注意力和传感器融合等前置模块，增加模型规模、时延与系统复杂度，使其较难适配资源受限的移动端车载平台。
- 零样本视觉语言模型缺乏可靠的度量空间 grounding：DriveBench 的研究表明，模型在移除视觉输入后仍可能生成貌似合理的驾驶回答，说明其可能依赖语言先验而非传感器几何；本文测试的零样本 8B 模型也无法正确读取工程化 BEV 的视觉词汇。由此可见，单纯扩大语言模型规模不能解决表征不匹配，并会造成关键风险漏检或空白、模板化输出。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作尚未证明：能否在不保留学习式 3D 感知骨干的条件下，把 LiDAR 距离、目标类别和雷达多普勒速度预先编码成确定性的 BEV 颜色与形状词汇，再让紧凑视觉语言模型可靠解码这些度量信息并完成多步驾驶推理。缺失的关键能力不是一般语言生成，而是面向特定传感器编码体系的显式视觉 grounding，以及这种 grounding 在小模型和边缘硬件上的可行性证据。

</div>
<div markdown="1"><span>核心问题</span>

一个约 2B 参数的紧凑视觉语言模型，经过先学习读取物理编码 BEV、再学习基于该 BEV 进行驾驶推理的分阶段微调后，能否在资源受限设备上获得比更大的零样本模型更可靠的度量空间推理与安全决策能力？

</div>
<div markdown="1"><span>作者直觉</span>

作者把原本需要神经网络隐式学习的三维感知工作前移到输入构造阶段：距离用颜色环带表示，类别用点簇形态表示，速度用带方向的楔形覆盖表示。这样，模型不必从原始点云中自行发现几何规律，只需像学习一套图例一样，把稳定的视觉符号还原为距离、类别和运动状态，再组合这些事实判断碰撞风险。先训练“读懂图例”，再训练“依据图例推理”，也可减少模型在尚未掌握空间词汇时直接模仿复杂答案所产生的语言先验依赖。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MoRAL以nuScenes的LiDAR、雷达和车辆CAN总线遥测为输入，先通过确定性渲染器生成物理编码的鸟瞰图（Bird's Eye View，BEV），再用两阶段监督微调让Cosmos-Reason2-2B依次学会“读图”和“基于图中证据推理”。BEV用LiDAR点的颜色表达距离、点簇形态表达物体类别，并用雷达楔形覆盖层表达相对运动方向与接近速度；这样把部分三维感知结果外显为普通视觉特征，推理时不需要额外训练一个三维BEV骨干网络。

两阶段设计的关键是隔离两种能力：Stage 1冻结语言模型，只训练视觉编码器的LoRA参数，使模型掌握BEV视觉词汇；Stage 2从该检查点继续训练视觉编码器和语言模型的LoRA参数，模仿8B教师生成的结构化思维链，完成八类驾驶问答。通俗地说，系统先教小模型认识“颜色、点簇和楔形分别表示什么”，再教它按照“观察证据、计算物理量、复核和表达不确定性”的顺序作出驾驶判断，避免模型只凭语言常识猜测或照抄文本中的数值。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 确定性多传感器BEV构建

渲染器将以自车为中心的$100\times100\,\mathrm{m}$区域投影为$896\times896$像素俯视图：LiDAR距离映射为颜色带，点簇形态保留类别线索，雷达检测映射为带方向颜色和速度尺寸的实心三角楔形；CAN遥测作为结构化文本提供。该步骤丢弃垂直轴，因此不同高度的物体可能在平面投影中形成歧义。

<div class="method-step__io" markdown="1">

**输入**：nuScenes单帧LiDAR回波、具有可靠质量标记的雷达检测，以及车辆速度、航向、横摆角速度和转向角等CAN总线遥测。<br>
**输出**：一张带有距离环、LiDAR彩色点簇和雷达速度楔形的物理编码BEV图像，以及自车遥测文本。

</div>

**直观理解**：渲染器相当于把难以直接阅读的传感器数组改写成一张带视觉图例的地图：颜色回答“多远”，点簇回答“可能是什么”，楔形回答“是否正在靠近以及靠近多快”。它只是整理已有传感器信息，并不自行检测物体或恢复完整三维场景。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### Stage 1：BEV视觉词汇接地

冻结语言模型，在视觉编码器注意力层上施加秩为$16$的LoRA，仅优化$14.4$M个参数；三类任务分别训练完整八区域描述、单区域真假核验和两区域距离排序。模型选择依据验证集Zone F1，而不是直接依据后续驾驶问答成绩。

<div class="method-step__io" markdown="1">

**输入**：从约34,000个训练帧中按传感器信息丰富度筛出的10,000帧，以及由这些帧构造的60,000条scan、verify和compare接地记录。<br>
**输出**：能够把BEV中的区域占用、距离、类别和速度方向视觉模式转换为结构化语言描述的Stage 1检查点。

</div>

**直观理解**：这一阶段类似先教会学生读地图图例，而暂时不要求其规划驾驶行为。verify样本专门要求确认某一区域是否确有目标，可抑制模型在空白区域凭空补充物体。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 教师数据生成与反捷径过滤

Cosmos-Reason2-8B教师按照$[\mathrm{CONDITIONS}]$、$[\mathrm{OBSERVE\_BEV}]$、$[\mathrm{PHYSICS\_WORK}]$、$[\mathrm{SECOND\_CHECK}]$和$[\mathrm{UNCERTAINTY}]$的顺序生成推理记录；约70,000条候选记录经11项硬规则筛选后保留57,696条。检测字段被压缩，速度只在雷达质量可靠时保留，且教师使用的精确物理计算结果在学生推理时不可见。

<div class="method-step__io" markdown="1">

**输入**：BEV图像、精简后的15字段检测模式、预先计算的制动距离与碰撞时间，以及八类驾驶问题。<br>
**输出**：覆盖接近速率、区域接地、威胁排序、盲区、驾驶决策、传感器不确定性、安全伦理和反事实推理的结构化监督数据。

</div>

**直观理解**：教师先用完整辅助信息写出示范解题过程，但学生最终不能直接看到教师的计算答案。强制“先观察BEV、再做物理计算”是为了阻止模型跳过图像，过滤规则则删除泄露真值、标签错序或结构不完整的示范。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### Stage 2：物理接地推理微调

在视觉编码器上使用秩为$8$的LoRA，并在语言模型全部线性层上使用秩为$16$的LoRA，共训练约$52$M个参数，即$2.2$B模型的$2.4\%$。监督信号要求模型复现有序的观察、物理计算、二次核验、不确定性分析和最终回答格式。

<div class="method-step__io" markdown="1">

**输入**：Stage 1检查点、57,696条教师生成的结构化思维链记录、对应BEV与前向摄像头输入，以及精简检测和自车遥测文本。<br>
**输出**：MoRAL 2B模型，可针对八类驾驶问题生成带$<think>$推理块和$<answer>$答案块的结构化响应。

</div>

**直观理解**：第二阶段把“会读图”的模型训练成“会按证据解题”的模型。LoRA只增加并更新少量低秩参数，使基础模型的大部分权重保持不变，从而降低训练和部署资源需求。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 干燥与湿滑路面制动距离

$$
d_{\mathrm{dry}}=\frac{v_{\mathrm{ego}}^{2}}{8.0},\qquad d_{\mathrm{wet}}=\frac{v_{\mathrm{ego}}^{2}}{4.0}
$$

**符号说明**

- $d_{\mathrm{dry}}$：干燥路面条件下的预计算制动距离。
- $d_{\mathrm{wet}}$：湿滑路面条件下的预计算制动距离。
- $v_{\mathrm{ego}}$：自车速度，由CAN总线遥测提供。
- $8.0$：论文在干燥路面制动距离规则中采用的分母常数。
- $4.0$：论文在湿滑路面制动距离规则中采用的分母常数。

<div class="equation-explanation" markdown="1">

**直观理解**：制动距离随自车速度的平方增长，因此速度翻倍会使估算距离增长到四倍；湿滑条件的分母更小，对应更长的制动距离。这些值用于帮助8B教师生成物理一致的训练示范，但在推理时对2B学生隐藏。<br>
**原文位置**：Section IV-B, “Physics precomputation”

</div>

</div>

<div class="equation-block" markdown="1">

#### 碰撞时间与动作分级规则

$$
\mathrm{TTC}=\frac{d_{\mathrm{obj}}}{v_{\mathrm{closing}}},\qquad a=\begin{cases}\mathrm{EMERGENCY\_BRAKE},&\mathrm{TTC}<1.5\,\mathrm{s}\\\mathrm{BRAKE},&1.5\,\mathrm{s}\leq\mathrm{TTC}<3\,\mathrm{s}\\\mathrm{MONITOR},&3\,\mathrm{s}\leq\mathrm{TTC}<5\,\mathrm{s}\\\mathrm{MAINTAIN},&\mathrm{TTC}\geq5\,\mathrm{s}\end{cases}
$$

**符号说明**

- $\mathrm{TTC}$：Time to Collision，即在当前相对运动保持不变时的预计碰撞时间。
- $d_{\mathrm{obj}}$：目标物体与自车之间的距离。
- $v_{\mathrm{closing}}$：目标相对自车的接近速度；只有可靠雷达测量才保留相应速度信息。
- $a$：由TTC阈值确定的目标动作标签。

<div class="equation-explanation" markdown="1">

**直观理解**：TTC用“剩余距离除以每秒缩短的距离”估算还有多久可能碰撞，再按时间阈值将动作分成紧急制动、制动、监控和保持。该规则为教师数据提供一致的动作依据，但单帧恒速假设无法表达加速度变化，因此输出仍需结合不确定性复核。<br>
**原文位置**：Section IV-B, “Physics precomputation” and “Required action”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：论文将两个阶段描述为监督微调，但未明确给出独立的损失函数公式或各输出字段的损失权重，因此不能据此声称使用了额外的物理一致性损失。可确认的优化目标是：Stage 1在冻结语言模型的条件下更新视觉LoRA，使生成结果匹配scan、verify和compare接地记录；Stage 2从Stage 1检查点出发，更新视觉与语言LoRA，使模型匹配8B教师生成的有序结构化回答。制动距离和TTC公式用于构造教师监督与动作标签，而不是论文明确声明的可微训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 物理编码BEV渲染器**

渲染器覆盖自车周围$100\times100\,\mathrm{m}$区域，并加入$10$至$50\,\mathrm{m}$距离环。LiDAR颜色从近距离的黄色逐步映射到远距离的紫色；车辆、障碍物和行人的类别线索由宽而密、细长、紧凑而稀疏等点簇形态表示；可靠雷达检测使用实心楔形，其中红、蓝、黄分别表达靠近、远离和横穿，楔形大小表达接近速度等级。

> 直观理解：该模块把公制距离和相对速度直接编码进图像，减少小模型从原始点云中自行学习复杂三维几何的负担。实心楔形替代箭头，是因为作者早期消融发现箭头几何会与模型学习的点簇形状发生冲突。

**2. 两阶段LoRA适配器**

Stage 1只在视觉编码器注意力层加入LoRA并冻结语言模型，使视觉词汇学习与语言推理解耦；Stage 2降低视觉侧LoRA秩，同时把LoRA扩展到语言模型全部线性层，使视觉证据读取和多步文本推理能够联合适配。两阶段均以Cosmos-Reason2-2B为学生，其与8B教师共享模型家族和$<think>...<answer>$输出格式。

> 直观理解：如果直接训练驾驶推理，模型可能学会照抄文本补充中的数字，却没有真正读懂BEV。先固定语言部分训练视觉能力，再联合训练推理能力，可以让后续答案建立在已经验证过的读图基础上。

**3. 反捷径物理问答构造器**

原始检测的30多个字段被压缩为15字段模式：距离离散为六档、航向离散为四类，速度仅在雷达质量为可靠时保留。教师可访问预计算物理量来生成一致示范，但学生推理时看不到这些结果；标签顺序规则还要求$[\mathrm{OBSERVE\_BEV}]$必须先于$[\mathrm{PHYSICS\_WORK}]$。

> 直观理解：这一模块控制模型能从文字中获得多少信息，防止检测表直接泄露精确答案。它迫使学生先从图像寻找对象和运动线索，再把这些观察用于物理判断。

**训练与推理**

训练前，作者先对约34,000个nuScenes训练帧按LiDAR颜色带多样性、类别多样性、检测数量、自车运动、雷达楔形存在性和可见性评分，保留信息较丰富的10,000帧。Stage 1用60,000条接地记录训练视觉编码器LoRA，并按验证集Zone F1选择第3轮检查点。随后，8B教师基于BEV、精简检测、自车状态和预计算物理量生成约70,000条候选思维链，经11项硬规则过滤后得到57,696条Stage 2记录；学生从Stage 1检查点继续训练视觉侧和语言侧LoRA。

推理时，确定性渲染器先把当前LiDAR与可靠雷达检测转换为BEV，并附加CAN遥测和允许的精简字段；MoRAL同时读取BEV与前向摄像头图像，按观察、物理计算、复核、不确定性和答案的结构生成响应。8B教师、精确预计算制动距离和TTC均不参与学生推理；系统也不执行物体检测、深度估计或学习式三维传感器融合，因此其输出是对预渲染传感器表示的阅读与推理结果，而不是完整自动驾驶感知或闭环控制结果。

**复现信息**

BEV分辨率为$896\times896$，覆盖$100\times100\,\mathrm{m}$自车中心区域；LiDAR距离颜色带覆盖$0$至$50\,\mathrm{m}$，但论文指出32线Velodyne HDL32E在$30\,\mathrm{m}$外点云稀疏，远距离读数应谨慎解释。雷达楔形按接近速度分为大于$6\,\mathrm{m/s}$、$2$至$6\,\mathrm{m/s}$和$0.5$至$2\,\mathrm{m/s}$三档。Stage 1使用学习率$2\times10^{-4}$和余弦衰减；Stage 2使用学习率$10^{-4}$、余弦衰减、最大序列长度$4096$和bfloat16，并在单张H100 PCIe 80 GB上训练。推理采用贪心解码和$1.3$重复惩罚。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- nuScenes 训练划分：论文声明全部训练数据仅来自该划分，用于构造第一阶段的 60,000 条 BEV grounding 记录和第二阶段的 57,696 条思维链记录；所给节选未报告具体训练帧数以及记录与帧之间的对应关系。
- nuScenes 验证划分（完整推理评测集）：包含 2,304 条记录、八类驾驶问题和 2,042 个唯一帧，用于比较完整模型的逐问题推理质量、安全相关行为及输出退化情况。数据中的动作标签高度不平衡：68,082 个目标中，$85.5\%$ 为 MAINTAIN，只有 $1.6\%$ 为 EMERGENCY_BRAKE。
- nuScenes 验证划分（第一阶段子集）：808 个留出帧，用于单独检验模型能否读取 BEV 编码词汇；它评估区域占用、距离、类别和速度方向，不直接检验最终驾驶决策质量。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Zone F1 与 within_20pct**

Zone F1 综合衡量八个 BEV 区域占用预测的精确率与召回率；within_20pct 统计已占用区域的预测距离落在真实距离 $\pm20\%$ 范围内的比例。前者测试模型是否识别空间占用，后者测试颜色距离带能否转化为可用的度量距离。 （越高越好；较高的 Zone F1 表示漏报和误报更少，较高的 within_20pct 表示更多距离估计达到预设相对误差门槛。）

</div>
<div class="metric-item" markdown="1">

**Gemma 逐题评分与 composite**

Gemma 4 按包含八项约束的评分规则评判回答，重点惩罚无依据的空间断言、错误动作标签和违反物理规律的推理。原始单条评分 $s_{\mathrm{raw},i}$ 以 5 分为满分，先归一化到 $[0,1]$，再对全部 $N$ 条记录取无权平均：$\mathrm{composite}=\frac{1}{N}\sum_{i=1}^{N}\frac{s_{\mathrm{raw},i}}{5}$。 （越高越好；分数越高表示回答越符合证据、动作标签和物理一致性要求，但它仍是经有限人工样本校准的模型裁判分数，不等同于真实道路安全率。）

</div>
<div class="metric-item" markdown="1">

**EMERGENCY_BRAKE recall 与 degeneration rate**

紧急制动召回率衡量真实需要 EMERGENCY_BRAKE 时模型成功识别的比例，用于突出类别极少但安全关键的事件；输出退化率衡量回答为空、不可解析、重复或不能形成有效结果等退化行为的发生比例。节选没有进一步给出退化判定规则。 （紧急制动召回率越高越好，因为漏掉危险情况更少；输出退化率越低越好，因为模型更常产生可用回答。召回率本身不反映误触发紧急制动的频率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 第一阶段 BEV 词汇学习：MoRAL S1 与零样本 Base 2B、Base 8B 在 808 个验证帧上比较。

<div class="result-value" markdown="1">

MoRAL S1 有 803/808 个输出可解析，空输出率为 $0.4\%$，产生 781/808 个唯一输出，Zone F1 为 $0.89$，within_20pct 为 $0.58$。相比之下，Base 2B 没有任何可解析输出；Base 8B 虽有 645/808 个输出可解析，但空输出率为 $79.2\%$，且只有 15/808 个唯一输出，因而两者均未获得有效的 Zone F1 或 within_20pct。

</div>

结果支持 BEV 的人工编码方式需要显式训练才能成为模型可稳定使用的输入词汇：单纯增大到 8B 参数并不足以避免空输出和模式坍缩。Zone F1 较高说明区域占用读取较可靠，而 within_20pct 只有 $0.58$，表明精确距离读取仍明显弱于占用判断。该实验只证明编码可读性，不证明最终驾驶决策正确，也不能区分收益来自视觉编码器训练、训练数据规模还是其他训练设置。

<div class="result-source" markdown="1">

来源：Section V-B；Table II 同时报告 Parse、Empty、Unique outputs、Zone F1 和 w20% 各列

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MoRAL Stage 1 achieves Zone F1 of 0.89 (precision 0.91, recall 0.90), class accuracy 0.62, and velocity direction accuracy 0.89.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 完整第二阶段推理：MoRAL 2B 与零样本 8B 基线在八类驾驶问题上比较。

<div class="result-value" markdown="1">

作者报告 MoRAL 在八种问题类型中的七种胜过零样本 8B 基线，同时模型参数规模约小四倍；最大优势出现在需要结构化、多步骤物理推理的问题类型。

</div>

这说明任务专项训练和显式物理编码可能比直接使用更大的零样本模型更有效，尤其适用于必须串联距离、速度和驾驶动作的题目。但所给材料没有提供八类问题的名称、逐类分数、置信区间或显著性检验，因此无法判断各类优势的绝对大小及统计稳定性；该结果也不能单独证明参数量是性能差异的原因。

<div class="result-source" markdown="1">

来源：Abstract；Section V-A 描述评估集与 Gemma 4 裁判协议

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On 2,304 held-out nuScenes frames evaluated by Gemma 4 (31B) calibrated against human review, MoRAL wins seven of eight question types over a zero-shot 8B baseline despite using four times fewer parameters, with the largest margins on question types requiring structured multi-step physics reasoning.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 安全相关行为与输出稳定性：完整 MoRAL 相对零样本 8B 基线。

<div class="result-value" markdown="1">

EMERGENCY_BRAKE 召回率从 $10.8\%$ 提升至 $47.8\%$，绝对提高 $37.0$ 个百分点；输出退化率从 $94.1\%$ 降至 $20.8\%$，绝对降低 $73.3$ 个百分点。

</div>

紧急制动召回率的提升表示模型识别到更多真实危险案例，退化率下降则表示其回答更常可用。这两项比总体准确率更适合当前极度不平衡的动作分布。不过，$47.8\%$ 的召回率仍意味着超过一半的紧急制动案例可能被漏掉；此外没有同时报告紧急制动精确率或误报率，因而不能断言系统已达到可部署的安全水平。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Emergency braking recall improves from 10.8% to 47.8%, output degeneration falls from 94.1% to 20.8%, and the full pipeline fits a consumer 8 GB GPU at 42 tok/s without quantization.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主要推理结果依赖 Gemma 4 (31B) 自动裁判。虽然作者用 40 个初始人工评审帧并在 40 至 80 个帧上迭代校准评分规则，但相对于 2,304 条评测记录，人工覆盖范围有限；缺少裁判与人工评分的一致率、相关系数或逐类误差，因此自动评分偏差仍无法量化。
- 实验仅使用 nuScenes 的训练与验证划分，所给材料未报告跨数据集、恶劣天气、传感器失准或真实车载闭环测试。远距离环准确率在 30–40 m 仅为 $0.227$，紧急制动召回率也只有 $47.8\%$，说明结果应被视为紧凑型物理落地推理的研究基础，而不是已验证的安全驾驶系统。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Base 2B (ZS)：未经 BEV 专项训练的 2B 基础模型，以零样本方式读取同一 BEV 输入。它控制了模型规模，主要用于判断 BEV 词汇是否可由原始紧凑模型直接理解。
- Base 8B (ZS)：未经 BEV 专项训练的 8B 基础模型。第一阶段用它检验扩大参数量能否自动解决 BEV 解析问题；完整推理评测又以零样本 8B 模型作为较大容量参照，判断专门训练的 2B 模型能否以更少参数取得更好的任务表现。
- 人工评审试点：研究者先对 40 个帧进行人工检查，每种条件 10 个，用于建立条件排序和失败模式基准，并据此校准自动裁判；它不是覆盖全部测试集的性能基线。
- Gemma 4 (31B) 自动裁判：作为主要评估器，而不是待比较的驾驶模型。选择理由是支持多模态输入、开放权重、可本地复现，并且独立于 Cosmos 模型家族，从而降低同源模型自评带来的偏差。

**实验想回答的问题**

- 经过第一阶段训练后，紧凑型模型能否稳定解析物理编码的鸟瞰图（BEV）词汇，包括八个空间区域的占用状态、距离色带、目标类别形态和速度方向，而零样本模型是否具备这种能力？
- 在参数规模和边缘设备资源受限的条件下，完整 MoRAL 流水线能否比零样本 8B 模型给出更可靠的驾驶推理，并改善紧急制动召回率与输出退化率等安全相关行为？

**实验实现**

第一阶段在 808 个留出验证帧上独立测量 BEV 词汇可读性。完整评测使用 nuScenes 验证集的 2,304 条记录，覆盖八种问题类型和 2,042 个唯一帧，且训练数据与验证数据按官方划分隔离。由于 MoRAL 不输出可通过 IoU 匹配的定位框，论文认为 mAP 不适用；同时动作分布严重偏向 MAINTAIN，因此总体准确率会掩盖安全关键的少数类。主评估采用本地运行的 Gemma 4 (31B)：研究者先人工评审 40 个帧，然后在 40 至 80 个帧范围内迭代评分规则，直至自动裁判的条件排序与人工评审一致。作者还指出，人工逐帧核对 BEV、六路相机图像和检测模式需要每帧 10 至 20 分钟，因此没有进行全量人工评测。部署方面，摘要报告完整流水线可在消费级 8 GB GPU 上无量化运行，并达到 42 token/s；所给节选未提供硬件型号、批大小、生成长度或速度测量方法。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出面向边缘自动驾驶的紧凑型VLM微调流程，利用传感器编码BEV进行度量空间与驾驶决策推理，并重点优化部署效率。; rule check: matched taxonomy keywords; top rule score=6.0
- 全文指纹：`d51a9b42c77afd14f91801d103c8c073195139a926d1743e446ffb30ca808965`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
