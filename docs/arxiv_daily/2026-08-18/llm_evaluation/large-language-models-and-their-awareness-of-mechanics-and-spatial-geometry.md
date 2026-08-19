---
title: "[论文解读] Large Language Models and their Awareness of Mechanics and Spatial Geometry"
description: "[arXiv 2608.14615][LLM 评测] 本文提出 MecEng 基准，用精确参数化几何、可执行多体系统仿真和自动化真值比较，评估大语言模型能否把文本机械描述转化为结构与物理参数均正确的仿真模型。"
arxiv_id: "2608.14615"
announcement_date: "2026-08-18"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:11:43.155130+00:00"
source_sha256: "0037e714e51dfe953d0b57d8eb163183e8d0484413795576fcc6626fdfe80317"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "柔性多体动力学"
  - "模型比较"
  - "模型验证"
  - "大语言模型"
  - "使用大语言模型进行有限元建模"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.14615</p>

# Large Language Models and their Awareness of Mechanics and Spatial Geometry

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Johannes Gerstmayr, Sebastian Weyrer, Tobias Möltner, Peter Manzl, Michael Pieber</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> aDepartment of Mechatronics, University of Innsbruck, Technikerstraße；bInstitute of Materials Resource Management (MRM), University of Augsburg, Am</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.14615) · [PDF 下载](https://arxiv.org/pdf/2608.14615) · **关键词** 柔性多体动力学, 模型比较, 模型验证, 大语言模型, 使用大语言模型进行有限元建模<br>


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

本文提出 MecEng 基准，用精确参数化几何、可执行多体系统仿真和自动化真值比较，评估大语言模型能否把文本机械描述转化为结构与物理参数均正确的仿真模型。

**不用术语来说**：让大语言模型生成一段能运行的程序，并不等于它真正理解了机械系统：模型还必须正确判断零件的形状、尺寸、相对位置、连接方式、材料与边界条件，并使生成结果能够直接用于仿真。现有三维生成方法往往只追求外观相似，而一般工程问答或代码基准又难以判断机械装配是否在空间和物理上成立，因此需要一种可自动检查模型是否真正具备机械工程理解能力的测试方法。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 构建 MecEng 机械工程基准，覆盖从简单刚性系统到复杂柔性多体系统的多个难度层级，并为测试问题提供专家实现的参数化真值模型，以系统考查空间关系、精确几何、物理参数和约束条件。
- 建立从文本生成精确三维实体、有限元网格和多体仿真模型的结构化评测流程，并通过系统图同构与数值时间序列比较，将装配结构错误同参数或动力学误差区分开来。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型（LLM）能力评测与机械工程仿真建模的交叉领域。传统的代码生成和数学推理基准不能充分反映模型对机械系统、空间几何和物理约束的理解，因此本文将这类能力概括为机械工程意识（mechanical engineering awareness）。研究对象是让 LLM 根据参数化文本描述，生成可用于多体动力学仿真的几何与系统模型，并通过结构、数值和部件物理属性等多个层次检验生成结果是否与专家基准一致。仿真对象覆盖刚体多体系统和柔性多体系统，后者还涉及三维几何生成、四面体有限元网格划分以及模型降阶。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多体系统与多体动力学**

多体系统由多个刚体或柔性部件组成，部件之间通过关节、接触等约束相互作用。多体动力学研究这些部件在力和约束作用下的运动，并通常将系统表示为部件、连接关系和物理参数组成的仿真模型。

</div>
<div class="concept-item" markdown="1">

**柔性多体系统与有限元建模**

刚体假设部件不会变形，而柔性多体系统还要描述部件的弹性变形。有限元方法把连续结构划分为许多小单元，本文特别涉及四面体网格，用于把机器零件的三维几何转换为可计算的结构模型。

</div>
<div class="concept-item" markdown="1">

**Hurty–Craig–Bampton模型降阶**

模型降阶用较少的自由度近似原本规模很大的有限元模型，从而降低仿真计算成本。Hurty–Craig–Bampton方法保留界面运动以及内部结构的代表性振型，适合将柔性零件嵌入多体系统仿真。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定参数化的自然语言机械描述，LLM需要生成两类仿真对象：一是通过专用流程生成的、可用于网格划分和有限元处理的三维零件几何；二是面向 Exudyn 的多体系统模型，包括部件、关节、接触及相关参数。系统输出随后与专家构建的 ground truth 进行多层验证，验证内容包括带节点标注的系统图同构、数值解，以及零件层面的质量、几何和特征频率等指标。任务覆盖 84 个通用问题和三个难度等级，设置从刚体关节与接触系统到需要精确三维几何和柔性建模的复杂系统；核心假设是文本描述包含足以构造目标模型的参数，而生成模型必须将这些描述转化为形式化、可执行且物理上可检验的仿真模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$LLM$**

大语言模型，本文评测的模型主体。

</div>
<div class="notation-item" markdown="1">

**$MecEng$**

本文提出的机械工程意识自动化基准名称。

</div>
<div class="notation-item" markdown="1">

**$Exudyn$**

用于构建和执行多体系统仿真的代码环境，本文将生成的多体模型面向该环境。

</div>
<div class="notation-item" markdown="1">

**$Netgen$**

本文生成流程中用于从文本描述得到仿真几何并进行相关网格处理的软件工具。

</div>

</div>

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

机械系统综合要求从自然语言规格得到可执行、可验证的工程模型。对于刚性或柔性多体系统，几何必须封闭且尺寸精确，因为形状不仅影响外观，还决定质量与惯性；在柔性部件中，它还决定结构柔顺性。零件、关节、连接器、材料、载荷和边界条件也必须形成一致的三维装配，否则即使代码能够执行，所得模型仍可能在物理上错误，无法用于有限元或多体动力学仿真。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **面向视觉效果的文本到三维生成**：DreamFusion、DreamGaussian、Magic3D 和 Point-E 等方法借助预训练视觉语言模型或文本到图像扩散模型，以 CLIP 引导、分数蒸馏等方式优化神经辐射场、高斯表示或点云；MeshGPT 与 LLaMA-Mesh 则直接合成三角网格。这类方法主要把文字转换为视觉上合理的三维对象。
- **工具增强的 CAD、工程代码与推理评测**：Text2CAD、CAD-coder 等方法让模型生成 CAD 表示或调用几何工具；MechAgents、EngiAI 和相关机械设计代理通过多代理、批评代理或迭代工具调用完成工程任务；FEM-Bench、EngiBench、ERI、NoReGeo 等基准分别评估有限元代码、通用工程能力或局部空间几何推理，并采用人工、模型裁判或程序执行进行评分。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 视觉型三维生成以外观质量为主要目标，不能稳定保证确定尺寸、封闭且无效面缺陷的实体几何；点云、神经场或视觉上近似的三角网格因而可能无法直接生成可靠有限元网格，也不能确保惯性和柔顺性等物理属性正确。
- 现有工程与空间推理工作通常只覆盖链条的一部分：有的检查概念问答或局部几何关系，有的生成底层有限元代码，有的依赖人工或大模型裁判，有的关注结构优化而非 CAD 式精确装配。因此，它们难以在同一任务中自动辨别系统拓扑错误、几何错误、参数错误和最终动力学响应错误。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前尚无统一基准同时要求大语言模型完成多步空间推理、生成精确且可网格化的三维机械几何、组装完整刚性或柔性多体系统，并依据专家真值自动验证结构与数值行为。尤其缺少一种无需仅凭代码可执行性或主观裁判，就能定位错误究竟来自部件与连接关系还是物理参数的评测框架。

</div>
<div markdown="1"><span>核心问题</span>

在零样本、以文本为输入并调用经过验证的仿真构件的条件下，当前开放权重与闭源前沿大语言模型能否正确生成不同复杂度的仿真就绪多体系统；它们的失败主要发生在空间几何与系统装配、柔性部件建模，还是物理参数和动力学结果层面？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把模型限制在经过测试的几何原语和仿真接口上，使模型负责高层工程决策，而不必逐个猜测顶点、网格连接或局部刚度矩阵。这样既能由参数化原语产生精确实体和有限元网格，又能把生成模型表示为由部件和连接关系组成的系统图：先比较该图与专家真值是否同构，再比较仿真时间序列，便可依次判断“装配是否正确”和“参数及物理行为是否正确”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文的方法不是训练新的大语言模型，而是建立一套分阶段、可定位错误的机械仿真代码验证框架。输入包括大语言模型生成的 Exudyn 仿真脚本、专家编写的真值脚本，以及任务要求的组件、柔性零件和仿真设置；框架依次检查组件选择、脚本装配与求解、机械系统图结构与参数、数值轨迹，并在柔性体任务中额外检查零件几何、材料、网格、接口和固有频率。只有当前检查通过，任务才进入下一阶段，因此每个失败样本会被归因到一个最早失败的指标，最终输出各阶段是否通过以及综合成功与否。
技术上，该框架用两类互补表示判断生成模型是否正确：一类把 Exudyn 的节点、对象、标记、载荷和传感器转成带属性有向图，以消除组件创建顺序和编号带来的影响；另一类直接比较所有时间步上的机械坐标，以验证动力学行为。直观地说，图比较回答“零件是否连接正确、参数是否填对”，轨迹比较回答“系统实际运动是否与标准答案一致”；二者结合可以区分结构错误、参数错误和仅由等价建模方式造成的表示差异。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 组件检索与任务准备

检查生成方案是否包含真值模型所需的全部组件及自动依赖；缺少任一必要组件即失败，多选组件不导致失败。柔性零件中的“盒体”或“圆柱体”也允许由相应截面的挤出组件等价实现。

<div class="method-step__io" markdown="1">

**输入**：任务描述、大语言模型选择的预定义仿真组件；对于三级柔性体任务，还包括零件生成组件。<br>
**输出**：“choose simulation components”和三级任务的“choose part components”通过或失败标记。

</div>

**直观理解**：这一步先检查工具是否备齐，而不判断工具使用得是否正确。允许多拿工具，是为了把“检索失败”和后续的“建模失败”分开。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 柔性零件预验证

依次核对接口数量与名称、杨氏模量、泊松比和密度，并比较质量、网格以及前三个固有频率；只有全部零件指标通过，才进入柔性多体系统装配。若模型请求少于六个固有频率，执行前会静默补足到六个，以保证结果可比。

<div class="method-step__io" markdown="1">

**输入**：大语言模型生成的柔性零件、对应真值零件及任务指定的接口和模态要求。<br>
**输出**：每个零件的接口、材料、质量、网格、固有频率匹配结果，以及“part overall success”。

</div>

**直观理解**：柔性体的运动取决于零件形状、材料和连接位置，因此必须先确认零件本身可靠。质量提供粗粒度形状检查，网格提供细粒度几何检查，固有频率则综合反映质量与刚度分布。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 脚本装配与动力学求解

运行脚本并检查是否完成 Exudyn 的 $\mathrm{mbs.Assemble()}$ 阶段，随后执行所要求的动力学仿真。装配前异常通常对应不存在的参数等编程错误，装配阶段异常通常对应系统结构或参数不一致，求解失败则可能来自不可实现的约束、错误运动学或隐式时间积分不收敛。

<div class="method-step__io" markdown="1">

**输入**：通过前置检查的大语言模型生成脚本及与真值模型一致的仿真时段和求解设置。<br>
**输出**：“finished assemble”和“solver success”指标，以及成功求解时的坐标时间序列。

</div>

**直观理解**：装配相当于确认机械零件能够组成一个合法系统，求解则确认该系统能沿时间稳定运行。即使代码语法正确，矛盾约束或不合理参数仍可能在这一步暴露。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 图结构与参数验证

把每个 item 转成图节点，把 item 间的索引引用转成有向边，并把质量、惯量、刚度、阻尼、初始状态和连接器参数等写入节点注释；随后按节点与边数量、带类别约束的图同构、节点注释精确匹配三级顺序验证。Python 用户函数以及受特征求解器容差影响的柔性体降阶矩阵不参与属性比较。

<div class="method-step__io" markdown="1">

**输入**：生成系统和真值系统中的 Exudyn items，包括节点、对象、标记、载荷、传感器及其参数。<br>
**输出**：节点和边数量检查、“topology match”、“graph content match”，以及按物理类别汇总的参数错误。

</div>

**直观理解**：系统中的数字编号可能因创建顺序而变化，但“谁连接谁”通常不变；转成图后，可以忽略编号而比较真实连接关系。先比骨架再比节点上的物理参数，能够判断问题究竟出在拓扑还是数值配置。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 机械系统总坐标

$$
\mathbf{q}_{\mathrm{total}}=\mathbf{q}_{\mathrm{ref}}+\mathbf{q}_{\mathrm{disp}}
$$

**符号说明**

- $\mathbf{q}_{\mathrm{total}}$：用于轨迹验证的总坐标向量，表示当前机械状态的完整坐标。
- $\mathbf{q}_{\mathrm{ref}}$：参考构形坐标向量，即系统状态表示中的基准部分。
- $\mathbf{q}_{\mathrm{disp}}$：相对参考构形的位移坐标向量。

<div class="equation-explanation" markdown="1">

**直观理解**：参考构形或位移单独都不能完整决定机械状态，因此验证器比较二者之和。这样可避免两个模型采用不同的参考状态分解，却被错误地视为具有不同实际位置。<br>
**原文位置**：第 3.1 节 Numerical Solution Comparison

</div>

</div>

<div class="equation-block" markdown="1">

#### 完整轨迹差异判据

$$
\left\|\mathbf{Q}_{\mathrm{gen}}-\mathbf{Q}_{\mathrm{gt}}\right\|_{F}\leq 10^{-5}
$$

**符号说明**

- $\mathbf{Q}_{\mathrm{gen}}$：由大语言模型生成脚本得到的总坐标矩阵，汇集全部系统坐标和时间步。
- $\mathbf{Q}_{\mathrm{gt}}$：专家真值脚本得到的总坐标矩阵。
- $\|\cdot\|_{F}$：Frobenius 范数，即对矩阵全部元素的平方求和后开平方。
- $10^{-5}$：判定两条数值轨迹匹配所使用的绝对容差。

<div class="equation-explanation" markdown="1">

**直观理解**：该判据把所有坐标在所有时间步上的误差合并成一个数；不超过阈值时判定解匹配。阈值高于求解器内部的相对容差 $10^{-8}$ 和绝对容差 $10^{-10}$，是因为连接器添加顺序等代数等价变化可能改变浮点残差、Jacobian 和 Newton-Raphson 迭代次数，局部微小误差还会在非线性时间积分中被放大。<br>
**原文位置**：第 3.1 节 Numerical Solution Comparison；原文以文字定义 Frobenius 范数比较及 $10^{-5}$ 阈值

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。所给章节描述的是对现有大语言模型生成结果的外部评估框架，没有使用这些指标反向传播、微调模型或优化生成策略；“overall success”是验证结果，而不是训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 顺序门控评估器**

一级和二级刚体任务按组件选择、装配、图验证、求解与轨迹验证推进；三级任务先对每个柔性零件执行专用指标，再复用同一套多体系统指标。任一步失败都会记录对应指标并终止该任务的下游评估。

> 直观理解：它把一个笼统的“代码失败”拆成检索、编程、建模、参数和数值行为等阶段，使成功率具有可诊断含义。由于同一大语言模型负责任务的各部分，最早失败阶段被用作该样本的单一错误归因。

**2. 基于图同构的机械结构验证器**

该模块用 NetworkX 构建带类别和属性的有向图：Exudyn items 是节点，内部引用是边，物理与运动学参数是节点注释。验证从低成本的规模检查推进到忽略编号的图同构，再推进到注释匹配；对大型随机链或网格设置最大节点数及两分钟超时。

> 直观理解：直接比较脚本文本会把创建顺序不同的等价代码误判为错误，而图同构关注连接结构本身。属性匹配进一步确认质量、惯量、载荷、关节方向、刚度和阻尼等关键量是否正确。

**3. 柔性零件多视角验证器**

材料参数要求杨氏模量、泊松比和密度全部精确一致；生成零件质量相对真值的误差须在 $1\%$ 内。网格通过 PyMeshLab 计算逐顶点距离并按真值体积归一化，容差为 $1\%$；前三个固有频率采用相对向量范数差，容差为 $5\%$。

> 直观理解：单一几何指标不足以验证柔性零件：质量可能相同但局部形状错误，网格接近也可能材料或接口位置错误。固有频率由几何、材料、质量分布和接口共同决定，因此是对这些因素的综合物理检查。

**训练与推理**

该方法没有论文内训练阶段。推理与评估时，大语言模型先根据任务和可用组件生成 Exudyn 脚本及必要的柔性零件；验证器将其与专家真值逐级比较。刚体任务从组件选择进入装配、图结构与属性验证、求解和轨迹比较；柔性体任务必须先让所有零件通过组件、接口、材料、质量、网格和固有频率检查，再执行相同的多体系统流程。数值轨迹直接按坐标矩阵位置比较，因此系统提示要求模型采用确定性的刚体创建顺序；图比较本身不依赖对象编号，可用于识别结构正确但坐标排列不同的情况。

**复现信息**

机械仿真在 Exudyn 中执行，图构建和同构验证使用 NetworkX，柔性零件网格距离使用 PyMeshLab。轨迹比较前必须确认坐标维度与时间步数一致；时间步不一致通常意味着求解提前终止。图属性比较排除 Python 用户函数和柔性体数值降阶矩阵，并对大型图设置节点数上限与两分钟超时。错误统计按任务去重：同一任务中多个刚体均出现质量错误只计一次质量类错误，但同一任务仍可同时计入连接器参数等其他类别错误。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 核心评测集由难度等级1和2的50个刚体多体系统任务模型组成。每个任务使用20组独立随机参数变体，因此每次完整模型评测包含1000个实例。该集合用于比较不同LLM的端到端建模能力；作者将等级3排除在该主表之外，因为等级3中的系统组装结果强烈依赖此前的零件生成，会引入额外的错误传播。
- 论文另设温度、推理设置和提示模板的专门运行，用于分析生成策略对结果的影响，原文指向第4.1.3至4.1.5节；但所给节选没有提供这些运行的任务规模、具体分组或数值结果。
- 每个任务的参考对象包含预期仿真组件、可运行系统、系统拓扑、数值解与图形内容。它们不是自然采集的数据样本，而是多体系统建模任务及其可执行参考结果，用于逐阶段自动判定模型输出。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**总体成功率（overall）**

衡量一个任务是否通过整条评测流水线，是最接近实际可用性的端到端指标。由于任一关键阶段失败都可能使任务不计为总体成功，该指标会反映错误累积。 （越高越好，因为更高比例表示模型生成的系统从组件选择到最终结果匹配均满足评测条件。）

</div>
<div class="metric-item" markdown="1">

**结构正确性（comp.与topol.）**

组件选择成功率（comp.）检查模型是否选对构建仿真所需的对象；拓扑匹配率（topol.）检查刚体、关节及连接关系是否与参考系统一致。前者偏向对象识别，后者更直接考察空间与机械结构建模。 （越高越好，因为这表示模型更常选择正确组件并形成正确的系统连接结构。）

</div>
<div class="metric-item" markdown="1">

**执行与结果正确性（solver、numsol与graph）**

求解器成功率（solver）检查生成模型能否运行；数值解匹配率（numsol）检查计算结果是否符合参考解；图形内容匹配率（graph）检查输出图是否包含预期内容。三者依次从可执行性推进到物理数值和结果表达的一致性。 （越高越好，因为仅能运行并不保证机械模型正确，而数值解和图形匹配进一步要求输出与参考行为一致。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 全部50个等级1和2任务、每个任务20组随机参数变体上的最佳总体表现

<div class="result-value" markdown="1">

Claude-Opus-4.8取得91.4%的总体成功率，并在组件选择、求解、拓扑、数值解和图形阶段分别达到99.4%、99.7%、99.2%、96.1%和93.2%，是表中总体成功率最高的模型。

</div>

作者结果表明，最强模型在简单和中等难度刚体多体系统任务上已能较稳定地完成端到端流程，但从早期阶段接近99%的成功率下降到91.4%的总体成功率，说明多个小概率错误会沿流水线累积。该结果不证明模型掌握了普适机械定律，也不能直接外推到被排除的等级3任务或真实工程模型。

<div class="result-source" markdown="1">

来源：附录B，表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Claude-Opus-4.8 99.4 99.7 99.2 96.1 93.2 91.4

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 同一主评测中表现最佳的开放权重模型

<div class="result-value" markdown="1">

qwen3.6:27b取得82.1%的总体成功率，各阶段依次为95.8%、94.0%、91.0%、83.3%和83.3%；其总体成功率低于Claude-Opus-4.8的91.4%，但高于其余开放权重模型。

</div>

这一结果说明，中等规模开放权重模型在该基准上可以达到较强的机械建模与空间结构生成能力，同时仍在拓扑之后的数值解和图形匹配阶段出现明显损失。它不能证明27B是最优参数规模，因为模型家族、训练方式、发布时间和量化设置并未受到控制。

<div class="result-source" markdown="1">

来源：附录B，表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

qwen3.6:27b 95.8 94.0 91.0 83.3 83.3 82.1

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨模型规模与家族的总体性能分布

<div class="result-value" markdown="1">

模型表现并不随参数规模单调上升：qwen3.5:122b的总体成功率为62.5%，低于qwen3.6:27b的82.1%；同时，较早的qwen:32b在所有阶段均为0.0%。

</div>

从表中可分析出，任务能力更可能由模型代际、训练数据、推理策略和代码生成可靠性共同决定，单纯增加参数量不足以保证机械与空间几何任务表现。由于这不是控制模型家族和训练条件的缩放实验，该现象只能反驳“表内参数越大必然越好”的简单解释，不能建立参数规模的因果效应。

<div class="result-source" markdown="1">

来源：附录B，表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

qwen3.5:122b 86.6 88.3 87.6 76.4 74.1 62.5
qwen3.6:27b 95.8 94.0 91.0 83.3 83.3 82.1
qwen:32b 0.0 0.0 0.0 0.0 0.0 0.0

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

- Claude-Opus-4.8和GPT-5.2作为专有模型参照，用于判断当前高性能闭源系统相对于本地可运行开放权重模型的性能上界；该比较同时混合了模型能力、训练数据和推理系统差异，不能单独归因于是否开放权重。
- qwen3.6:27b、gemma4:31b和qwen3.5:27b代表表现最强的一组开放权重模型，用于检验中等参数规模模型能否接近专有模型，而不把参数量直接等同于能力。
- qwen2.5-coder:32b、qwen3-coder:30b、deepseek-coder-v2:16b等代码导向模型构成有意义的功能性参照：任务最终涉及生成可执行仿真程序，因此可测试通用推理能力与代码专门化能力何者更关键。
- 从小于4B到122B有效参数规模的开放权重模型构成跨规模参照，用于观察规模与成功率的关系；但表中还同时改变了模型家族、发布时间及量化条件，因此它不是严格控制变量的参数缩放实验。

**实验想回答的问题**

- 不同规模、架构与开放方式的大语言模型，能否根据任务描述正确选择仿真组件、组装刚体多体系统，并生成与参考模型一致的拓扑、数值解和结果图？
- 模型在分阶段评测流水线中的错误如何累积，以及最终成功率是否能由早期的组件选择或求解器运行成功充分代表？

**实验实现**

实验在Windows 11工作站（64 GB内存、NVIDIA GeForce RTX 5090 32 GB显存）以及Ubuntu 24.04服务器（两张NVIDIA H100、每张80 GB显存）上本地执行，主要软件为Ollama 0.24.0和Exudyn 1.10.160。作者评测了32个开放权重模型与2个专有模型；开放权重模型覆盖小于4B至122B有效参数，并采用4位量化口径。对每个LLM，50个等级1至2任务各生成20个独立随机参数变体，共1000次任务。表1按组件选择、求解成功、拓扑匹配、数值解匹配、图形匹配和总体成功逐级报告比例。gpt-oss模型采用最低推理强度“low”。节选未说明随机种子、置信区间、显著性检验方法、专有模型调用配置以及各指标的具体容差，因此这些结果主要支持同一评测流程下的经验比较。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The study evaluates whether LLMs understand and reason about mechanics and spatial geometry.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`0037e714e51dfe953d0b57d8eb163183e8d0484413795576fcc6626fdfe80317`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
