---
title: "[论文解读] Large language models for partial differential equation workflows"
description: "[arXiv 2608.03600][LLM Agent] 本文是一篇综述，将大语言模型辅助偏微分方程研究统一为“发现—求解—优化”三阶段工作流，并据此分析其相对于传统数值计算和局部深度学习方法的作用边界、评价要求与关键缺口。"
arxiv_id: "2608.03600"
announcement_date: "2026-08-05"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:41:30.088763+00:00"
source_sha256: "7c756eca1169e7028324f228ff8fb33e4b7ee2d98c1ddb05d75e84bf51baddfe"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "偏微分方程"
  - "科学工作流自动化"
  - "可执行工作流"
  - "生命周期分类"
  - "数值求解器"
  - "PDE 约束优化"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.03600</p>

# Large language models for partial differential equation workflows

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Han Wan, Rui Zhang, Hao Sun</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Gaoling School of Artificial Intelligence, Renmin University of China, Beijing 100872, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03600v1) · [PDF 下载](https://arxiv.org/pdf/2608.03600v1) · **关键词** 大语言模型, 偏微分方程, 科学工作流自动化, 可执行工作流, 生命周期分类, 数值求解器, PDE 约束优化<br>


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

本文是一篇综述，将大语言模型辅助偏微分方程研究统一为“发现—求解—优化”三阶段工作流，并据此分析其相对于传统数值计算和局部深度学习方法的作用边界、评价要求与关键缺口。

**不用术语来说**：偏微分方程只有被转化为可运行的完整流程，才能真正服务于科学与工程：研究者需要先根据知识和数据建立方程，再选择离散方法、网格和求解器并检查结果，最后利用模拟结果进行控制、设计或优化。现有流程需要专家在数学描述、程序代码、数值软件和工程目标之间反复转换与协调，成本高且容易在环节交接处出错；本文关注大语言模型能否充当这些异构环节之间的接口，而不是取代数值求解器。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出面向完整生命周期的综述框架，按发现阶段、求解阶段和优化阶段组织已有研究，并以大语言模型在工作流中的介入位置及用途为比较轴，从而避免仅按最终预测精度比较性质不同的系统。
- 明确大语言模型在偏微分方程计算中的合理定位与评价边界：其主要价值是连接自然语言、符号数学、代码、数值求解器输出和迭代反馈；评价则应同时考察可执行可靠性、数值与物理有效性、可检查性、鲁棒性、求解器反馈使用质量、专家负担降低程度和整体科学效用。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

偏微分方程（PDE）用空间与时间上的连续变量描述物理系统及其多尺度演化，是流体、材料和工程设计等领域的核心建模工具。PDE 真正产生科学与工程价值，依赖一条可执行工作流：从物理假设、观测数据或文本知识出发，建立或发现控制方程；选择离散方法并配置数值求解器；检查稳定性、收敛性、精度和物理一致性；最后将模拟结果用于控制、优化与设计。传统流程可靠但高度依赖专家协调，深度学习通常只增强方程发现、代理求解或优化等局部环节；本文综述的重点则是大语言模型（LLM）如何在更高的工作流层面连接自然语言、符号数学、程序代码、数值求解器输出与迭代反馈。LLM 在这里不是 PDE 求解器的替代品，而是组织异构知识、调用计算工具并衔接各阶段的接口。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**偏微分方程（PDE）与控制方程**

PDE 描述未知场随多个自变量（通常为空间和时间）变化的规律；控制方程是针对具体系统选定的 PDE 及其参数、初始条件和边界条件。只有把这些要素明确下来，问题才能交给数值求解器执行。

</div>
<div class="concept-item" markdown="1">

**数值离散与求解器**

计算机通常不能直接求解连续 PDE，因此要用有限差分、有限体积、有限元或谱方法把连续问题转化为有限维计算。求解结果是否可信，不只取决于代码能否运行，还取决于离散误差、稳定性、收敛性、守恒性以及网格和求解器配置。

</div>
<div class="concept-item" markdown="1">

**PDE 约束控制与优化**

这类任务在满足 PDE 动力学约束的前提下，寻找控制策略、几何形状或设计参数，使给定目标函数最优。它们往往需要反复调用 PDE 求解器，因此计算成本高，并需要把模拟反馈正确地传回决策过程。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文是综述而非提出单一预测模型，其研究对象是 LLM 辅助的端到端 PDE 科学计算工作流。输入可以包括自然语言任务描述、物理假设、观测数据、不完整的符号方程、边界与初始条件、求解器文档、代码以及运行诊断；中间过程按发现、求解和优化三个阶段组织：发现阶段形成候选控制方程、模型结构或参数，求解阶段生成或修改可执行代码并配置数值工具，优化阶段依据模拟反馈制定控制、设计或参数更新；输出则包括可检查的 PDE 规格、可执行求解流程、诊断解释以及面向下游任务的决策。该设定默认成熟数值求解器、验证程序和专家设计的工具接口仍然存在，LLM 主要承担跨模态信息转换、工具协调和反馈利用，而不是绕过数值计算直接给出可信解；因此评价范围还应覆盖可执行可靠性、数值与物理有效性、可检查性、鲁棒性、专家负担降低程度及整体科学用途，而不能只比较最终解的精度。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{W}_{\mathrm{PDE}}$**

用于概括本文讨论的 PDE 可执行工作流；这是分析性记号，原文未给出统一数学符号。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{D}$**

发现阶段：从数据、文本、物理假设或部分符号描述中形成方程、候选模型或参数。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{S}$**

求解阶段：完成离散、求解器配置、代码生成、执行诊断与反馈驱动修订。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{O}$**

优化阶段：利用 PDE 模拟结果支持控制、参数优化、形状设计或其他工程决策。

</div>

</div>

**直接相关的工作**

- **稀疏回归与数据驱动方程发现**: 这类方法从测量数据中识别候选控制方程或候选项，属于工作流的发现阶段，但通常针对固定任务或预设候选结构；本文关注 LLM 如何进一步连接文本知识、符号表达、数据和后续可执行计算。
- **神经算子、学习型求解器与物理信息学习**: 这些方法通过学习解映射、改进离散或在训练目标与网络结构中加入物理约束来加速或增强 PDE 求解，主要优化工作流中的局部组件；本文将其与 LLM 的工作流级角色区分开，后者侧重协调模型构建、代码、外部求解器、诊断反馈和下游目标。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

从物理假设到工程决策的偏微分方程流程包含模型建立、数值离散、网格与求解器配置、诊断验证以及重复优化等相互依赖的环节。传统方法虽有成熟的稳定性、收敛性、精度和守恒分析，但具体实施仍依赖专家判断与人工协调；控制和设计还常需反复求解偏微分方程，因此在复杂场景中同时产生较高的计算成本与操作成本。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **传统偏微分方程科学计算**：专家依据第一性原理、物理约束、机理假设和观测提出并修正控制方程，再选用有限差分、有限体积、有限元或谱方法进行离散求解，最后将解嵌入最优控制、流动控制或拓扑优化。该路线理论基础成熟，但几何表达、网格生成、离散方案和求解器配置等关键选择通常需要人工完成。
- **数据驱动与深度学习方法**：稀疏回归、系统辨识和物理信息学习可从数据发现方程或估计参数；学习型离散、神经算子和代理模型可加速求解；强化学习、可微物理和学习型模拟器可支持控制与设计。这些方法通常优化某个局部模块，并依赖特定任务类别、模型结构或工作流阶段。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 传统流程各阶段长期依赖领域专家做出选择并手工传递信息；当问题涉及复杂几何、求解器配置或大量重复模拟时，这种协调方式会提高人力与运行成本，也限制流程自动化和规模化。
- 既有数据驱动与深度学习方法主要增强方程发现、数值求解或下游优化中的单个组件，通常受限于特定阶段、任务类别或模型结构，因而不能自行协调模型发现、可执行计算、求解器反馈和下游目标。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

目前缺少一个以完整偏微分方程生命周期为对象的统一视角，用来解释和比较大语言模型如何跨越科学知识、符号描述、程序代码、数值工具与任务反馈。与此同时，高质量数据集和基准尤其缺乏于知识发现及真实应用：专家标注、可执行问题构造和任务级反馈都代价高昂；模拟结果与真实科学和工程系统之间还存在持续差距，使模拟所得控制策略和优化设计难以直接迁移。

</div>
<div markdown="1"><span>核心问题</span>

大语言模型应当在偏微分方程的发现、求解和优化三个阶段分别承担什么工作流角色，现有系统提供了哪些证据，以及应通过哪些超越单一解精度的标准判断这种辅助是否可靠并具有科学价值？

</div>
<div markdown="1"><span>作者直觉</span>

大语言模型的优势不在于替代具有数值保证的求解算法，而在于它能处理多种表达形式并调用外部工具：把文字需求整理为方程与边界条件，把数学规格转成可执行代码，根据报错或求解器诊断修改配置，再把模拟反馈连接到控制和设计目标。换言之，它更像负责翻译、编排和反馈闭环的工作流接口；若每一步仍由数值验证和物理检查约束，就可能减少跨环节的人工协调，同时保留传统求解器的可检查性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文是综述与分类框架，而非提出一个需要训练的新模型。其核心方法是把“LLM 辅助 PDE”统一表示为 Discovery–Solving–Application 工作流：先用空间域 $\Omega$、时间区间 $[0,T]$、状态场 $u(x,t)$、控制或系统参数 $\lambda$、控制算子 $\mathcal{F}$、初边值条件及任务目标 $\mathcal{L}$ 描述完整问题，再依据当前尚未确定的部分划分研究方向。Discovery 阶段确定或分析控制方程及其数学结构；Solving 阶段在方程已知时计算状态场；Application 阶段把求解器置于优化闭环中，搜索满足 PDE 约束且使目标最优的参数、控制量或设计变量。作者进一步按 LLM 在每个阶段承担的主要功能，对代表性工作进行文章级归类，而不是提出一套统一的底层网络架构。
从端到端角度看，输入可以是观测数据、物理先验、自然语言任务、已知 PDE、数值状态或设计目标；LLM 负责跨语言、符号数学、代码和求解器反馈组织候选假设与操作，但数值拟合、仿真、残差检查和物理验证仍承担可执行检验。通俗地说，LLM 更像连接科学家与数学工具链的“工作流接口”：它帮助决定应写什么方程、如何调用或生成求解程序，以及下一轮应尝试什么参数，却不能仅凭语言生成替代数值计算和科学验证。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. PDE 问题规范化与阶段定位

把问题整理为状态场 $u(x,t)$、控制算子 $\mathcal{F}$、初值 $u_0(x)$、边界算子 $\mathcal{B}$、边界数据 $g(x,t)$、参数 $\lambda$ 和可选目标泛函 $\mathcal{L}$；再判断未解决对象是 $\mathcal{F}$、$u(x,t)$ 还是 $\lambda$。该判断分别把任务送入 Discovery、Solving 或 Application 阶段。

<div class="method-step__io" markdown="1">

**输入**：自然语言科学意图、观测数据、物理先验，或已经给出的 PDE、初始条件、边界条件与任务目标。<br>
**输出**：一个数学上较明确的 PDE 任务规格，以及对应的工作流阶段和所需验证方式。

</div>

**直观理解**：先把模糊需求翻译成一张“问题清单”，并找出究竟缺的是方程、方程的解，还是最佳设计参数。只有确定缺口后，才能选择发现、求解或优化工具。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. Discovery：方程发现、问题形式化与科学推理

对于未知方程，LLM 可在搜索前推断问题相关的算子、对称性和结构约束，或直接生成候选方程及方程骨架；候选项随后经回归、参数拟合、优化或仿真评估，并依据反馈迭代修订。对于已知 PDE，LLM 可辅助补全数学规格、组织符号推导、搜索解析表示，并分析结构性质或定性行为。

<div class="method-step__io" markdown="1">

**输入**：观测数据、候选变量、领域知识、物理约束、非完整的科学描述，或已知但需要分析的 PDE。<br>
**输出**：经可执行检查筛选的候选控制方程、算子库或结构约束，或者形式化后的 PDE 问题、解析表达与性质分析。

</div>

**直观理解**：LLM 不直接宣布哪个方程一定正确，而是利用学到的科学模式缩小“可能公式”的范围，再让数据拟合和物理检验做裁判。若方程已经给定，它则帮助安排多步推导和选择值得尝试的解析结构。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. Solving：生成、编排与修订可执行求解流程

LLM 生成或配置传统数值求解器代码、编排现有数值软件，或辅助构建深度学习 PDE 求解器；执行后读取 PDE 残差、收敛行为、稳定性违规、运行时错误等诊断信息并进行修订。该阶段的数学目标是计算满足方程和初边值条件的状态 $u(x,t)$。

<div class="method-step__io" markdown="1">

**输入**：已确定的 $\mathcal{F}$、初边值条件、参数 $\lambda$、计算域及求解要求。<br>
**输出**：可执行的求解配置或代码、诊断记录，以及数值或学习式近似解 $u(x,t)$。

</div>

**直观理解**：这一阶段相当于让 LLM 编写和维护“计算实验脚本”，真正的答案仍由数值软件或学习式求解器计算。报错、残差过大或不收敛时，反馈被送回系统以修改代码和设置。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. Application：求解器闭环中的优化、控制与设计

LLM 协助形式化目标和约束，提出或修订参数、控制程序、几何设计或模型形式；每个候选项由 PDE 求解器评估，再依据性能、约束违反或数据拟合误差选择后续候选。该过程形成“提出候选—仿真—解释反馈—再修订”的闭环。

<div class="method-step__io" markdown="1">

**输入**：目标泛函 $\mathcal{L}(u,\lambda)$、可调整变量 $\lambda$、PDE 约束、候选设计，以及求解器或现实观测返回的性能反馈。<br>
**输出**：在 PDE 约束下表现较好的参数、控制策略、设计或模型形式，并附带仿真评估结果。

</div>

**直观理解**：可以把求解器看成昂贵的实验台：LLM 提议下一次实验，仿真返回结果，系统据此继续改进方案。所得结果仍是仿真条件下的候选最优解，不能自动等同于现实系统中的有效方案。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 一般 PDE 初边值问题

$$
\mathcal{F}\left(x,t;u,\partial_t u,\nabla u,\ldots;\lambda\right)=0,\qquad u(x,0)=u_0(x),\qquad \mathcal{B}(u,\nabla u)=g(x,t)\ \text{on}\ \partial\Omega
$$

**符号说明**

- $x$：空间位置，属于空间域。
- $t$：时间变量，取值于时间区间。
- $u(x,t)$：待建模或待求解的物理状态场。
- $\Omega$：空间计算域；其边界为偏微分方程施加边界条件的位置。
- $\partial\Omega$：空间域的边界。
- $\mathcal{F}$：控制方程算子，编码状态及其时空导数之间的物理关系。
- $\partial_t u$：状态场关于时间的一阶偏导数。
- $\nabla u$：状态场关于空间坐标的梯度。
- $\lambda$：系统参数、物理参数或控制参数。
- $u_0(x)$：初始时刻的状态分布。
- $\mathcal{B}$：作用于状态及其空间导数的边界算子。
- $g(x,t)$：边界上给定的时空数据。

<div class="equation-explanation" markdown="1">

**直观理解**：该式是全文分类框架的共同起点：$\mathcal{F}=0$ 说明系统内部如何演化，初始条件规定从何种状态开始，边界条件规定计算域边缘如何响应。Discovery 主要确定或分析 $\mathcal{F}$，Solving 在这些条件下求 $u(x,t)$，因此三类工作可以在同一数学表示下比较。<br>
**原文位置**：第 2 节，公式（1）及其后紧接的初始条件与边界条件

</div>

</div>

<div class="equation-block" markdown="1">

#### PDE 约束下的任务级优化

$$
\min_{\lambda}\mathcal{L}\bigl(u,\lambda\bigr)\quad\text{s.t.}\quad\mathcal{F}\left(x,t;u,\partial_t u,\nabla u,\ldots;\lambda\right)=0
$$

**符号说明**

- $\min_{\lambda}$：在可调参数、控制量或设计变量上寻找最小目标值。
- $\mathcal{L}(u,\lambda)$：任务目标泛函；在优化任务中表示性能目标，在逆问题中可表示预测与观测之间的差异。
- $u$：由 PDE 和参数共同决定的系统状态。
- $\lambda$：待优化的物理参数、控制变量或其他设计变量。
- $\mathcal{F}$：必须满足的 PDE 控制算子。

<div class="equation-explanation" markdown="1">

**直观理解**：目标不是任意降低 $\mathcal{L}$，而是在候选方案仍满足控制方程的前提下优化 $\lambda$。这解释了为何 Application 阶段必须反复调用求解器：每次改变设计或控制量，都会改变状态 $u$，进而改变目标值。<br>
**原文位置**：第 2 节，公式（2）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文是工作流综述与分类研究，没有提出统一的 LLM 训练损失或端到端参数学习目标；公式（2）的 $\mathcal{L}(u,\lambda)$ 是 PDE 应用阶段的任务级优化目标，而不是语言模型训练损失。被综述系统可以用回归、参数拟合、连续优化、进化搜索或仿真评价来筛选候选，但原文所给章节未规定所有方法共享的优化算法。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 统一 PDE 任务表示与工作流路由**

作者用控制方程、初始条件、边界条件和目标泛函统一表示不同任务，并以尚未求得的对象为路由依据：Discovery 处理 $\mathcal{F}$ 及问题规格，Solving 计算 $u(x,t)$，Application 在 PDE 约束下优化 $\lambda$。这种划分统一了方程发现、求解器生成、控制和设计，但不是一个可直接运行的软件模块。

> 直观理解：它提供一张任务地图：未知方程就先做发现，方程已知但解未知就求解，需要改进控制或设计时再进入优化。这样可避免把性质不同的 LLM 能力混为同一类任务。

**2. LLM 引导的候选结构搜索**

该模块有两条路径：其一由 LLM 推断算子、对称性、中间物理属性和结构约束，再交给符号回归搜索；其二由 LLM 直接生成完整候选方程或骨架，并结合参数拟合结果、历史候选性能和数据反馈反复修订。LLM 的主要作用是提供科学先验和搜索方向，最终表达仍需数值拟合、物理验证与专家判断。

> 直观理解：传统方法要么使用过窄的人工算子库而漏掉真项，要么搜索空间过大而浪费计算。LLM 像熟悉领域规律的向导，优先推荐更可能合理的结构，但不负责最终证明。

**3. 可执行反馈闭环**

在方程发现中，反馈来自回归、优化、仿真和候选性能；在求解中，反馈包括残差、收敛、稳定性与运行错误；在应用中，反馈来自目标值、约束满足情况或观测差异。LLM 读取这些结果后修改方程结构、代码、参数或设计，使语言推理与外部计算工具形成迭代闭环。

> 直观理解：单次生成容易产生看似合理但无法运行的答案，因此必须让真实计算结果不断纠错。这个模块把“写出建议”改造成“提出、执行、检查、再修改”的工程流程。

**训练与推理**

不存在一套由本文统一执行的训练流程。工作流运行时，系统先从文本、数据和物理先验建立 PDE 规格，再根据未知对象选择阶段：若 $\mathcal{F}$ 未知，则由 LLM 构造搜索空间或生成候选方程，并调用拟合、回归、优化或仿真进行评价；若 $\mathcal{F}$ 已知，则生成或配置求解流程以计算 $u(x,t)$，并依据残差、收敛性、稳定性和运行错误修订；若目标是优化 $\lambda$，则在求解器闭环中反复提出候选、计算状态、评价 $\mathcal{L}$ 并更新候选。最终输出应经过数值验证、物理一致性检查和必要的专家判断，而不能只依据 LLM 的语言置信度。

**复现信息**

本文所给章节没有提供统一模型、提示模板、训练数据、超参数、软件栈或硬件配置，因为它总结的是多个异构系统而非实现单一算法。公平理解该框架时应保留两点：第一，LLM 的主要职责是生成、筛选、修订和编排，数值工具负责拟合与求解；第二，各系统的有效性取决于外部验证环节，包括 PDE 残差、收敛与稳定性诊断、仿真性能、物理合理性和专家审查。具体复现参数需回到表 1 所列各代表性工作的原始论文，当前节选无法支持更细的实现说明。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Discovery 阶段资源：Physical hypothesis selection datasets，用于评测方程发现中的表达式恢复、项选择准确率和物理合理性；原文未明确报告其规模、数据划分和具体构造方式。
- Solving 阶段资源：OpenFOAM tutorials、CFDLLMBench、PDEBench、CFDCodeBench、ALL-FEM verified FEniCS corpus 和 AutoNumerics，分别覆盖传统求解器工作流增强、PDE 求解器代码生成及可执行性、数值准确性和运行表现；原文未明确报告各资源的规模与划分。
- Optimization 阶段资源：Parameter-optimization workflows、PDE-control formalization tasks、Parametric shape optimization 和 ShapeBench high-fidelity CFD/FEA，用于检验参数优化、控制形式化、形状优化以及高保真 CFD/FEA 场景下的任务完成、目标改进、约束满足和保真度；原文未明确报告各资源的规模与划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务成功与可执行性指标**

包括 Task Success、Executable Rate、Code-level Success、Compilation Success 和 Recovery Rate，用于判断系统是否完成任务、生成可运行代码，或能否从失败中恢复。 （通常越高越好，因为更高值表示更多任务可执行、完成或恢复；但单独升高并不能证明数值结果正确或专家负担降低。）

</div>
<div class="metric-item" markdown="1">

**科学与数值有效性指标**

包括 Expression Recovery、Physical Plausibility、Mathematical Correctness、Numerical Accuracy、Constraint Satisfaction 和 Feasibility / Fidelity Gap，用于衡量表达式恢复、数学正确性、物理合理性、数值精度、约束满足及模拟结果与高保真目标之间的差距。 （Expression Recovery、Physical Plausibility、Mathematical Correctness、Numerical Accuracy 和 Constraint Satisfaction 通常越高越好；Feasibility / Fidelity Gap 越低越好，因为差距更小表示结果更接近可行且可信的高保真解。）

</div>
<div class="metric-item" markdown="1">

**效率与专家负担指标**

包括 Human Interventions、Execution Cost、Runtime、Budgeted Convergence 和 Reasoning Traceability，用于衡量所需人工介入次数、执行成本、运行时间、给定预算下的收敛情况以及推理过程是否可追溯。 （Human Interventions、Execution Cost 和 Runtime 越低越好；Budgeted Convergence 和 Reasoning Traceability 通常越高越好。它们用于判断系统是否真正减少专家工作，而不仅是完成精选任务。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Solving 阶段基准成熟度

<div class="result-value" markdown="1">

求解阶段的评测相对完善，可以通过代码可执行性、工作流完成、失败恢复、数值准确性和收敛等结果判断系统表现。

</div>

这说明生成代码或编排求解器的系统已有较直接的外部检查标准：代码能否运行、计算是否完成以及数值结果是否合理。不过，这只是表明求解阶段更容易被评测，不等于系统已经能处理未见过的复杂工作流，也不等于它减少了专家的科学判断。

<div class="result-source" markdown="1">

来源：第 6 节 Benchmarking and Evaluation across the PDE Workflow

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Benchmarks are relatively more developed for Solving-stage tasks, where success can be assessed through code executability, workflow completion, failure recovery, numerical accuracy, or convergence.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Discovery 与 Optimization 阶段的评测不足

<div class="result-value" markdown="1">

Discovery 阶段在数学完整性、推理透明度、物理合理性和下游可用性方面的评测仍不成熟；Optimization 阶段还必须同时考虑样本效率、约束满足、物理有效性、鲁棒性和专家介入量。

</div>

方程写得像数学表达式，并不代表它包含了完整的建模假设或能直接进入求解流程；同样，优化目标变好也不代表设计满足物理约束、对扰动稳健或值得付出大量专家时间。因此，这两个阶段不能只用单一准确率或目标值评价。

<div class="result-source" markdown="1">

来源：第 6 节 Benchmarking and Evaluation across the PDE Workflow

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Evaluation remains less mature in parts of the Discovery Stage, where the central questions concern mathematical completeness, reasoning transparency, physical plausibility, and whether a proposed formulation is usable downstream.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 现有基准对真实可靠性和专家负担的证明不足

<div class="result-value" markdown="1">

当前基准常强调代理结果而非科学意义上的专家负担降低；精选案例上的高成功率不能证明系统在陌生几何、边界条件、软件交互、数值失败和物理状态下仍然可靠。

</div>

一个系统在模板化示例中能够成功生成代码或修复预设错误，可能只是学会了任务表面模式。真正重要的检验是：当中间决策和求解器反馈改变后续流程时，系统是否仍能识别科学上有意义的失败，并在较少人工介入下完成可信工作流。

<div class="result-source" markdown="1">

来源：第 6 节 Benchmarking and Evaluation across the PDE Workflow

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A more fundamental limitation is that current benchmarks often emphasize proxy outcomes rather than the central question of this field: whether expert burden has been reduced in a scientifically meaningful way.

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

- 原文未明确报告。

**实验想回答的问题**

- 不同阶段的 PDE 工作流应采用哪些与任务输入、输出和验证要求相匹配的评测资源与指标，才能区分真正的工作流改进和表面上的任务完成？
- 现有基准是否能够证明 LLM 系统降低了专家负担，并且在陌生几何、边界条件、软件交互、数值失败和物理状态下仍保持科学可靠性？

**实验实现**

本文采用按 Discovery、Solving 和 Optimization 三个阶段组织的代表性基准、数据集、微调语料和指标进行横向评述，而非报告一个统一模型在统一数据集上的受控实验。作者强调不同工作流的输入、输出和验证要求差异很大，因此各类指标只能互补解释，不能直接互换。当前评测主要覆盖代码可执行性、工作流完成、失败恢复、数值准确性、收敛、物理有效性、目标改进、样本效率、约束满足、鲁棒性和专家介入量。原文未明确报告统一的模型版本、训练设置、数据划分、重复次数、统计显著性或具体实验协议。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It surveys LLM-driven PDE workflows involving symbolic formulation, code and solver interaction, simulation feedback, and scientific reasoning.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`7c756eca1169e7028324f228ff8fb33e4b7ee2d98c1ddb05d75e84bf51baddfe`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
