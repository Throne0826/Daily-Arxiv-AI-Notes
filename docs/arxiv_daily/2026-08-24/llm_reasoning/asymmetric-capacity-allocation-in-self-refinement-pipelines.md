---
title: "[论文解读] Asymmetric Capacity Allocation in Self-Refinement Pipelines"
description: "[arXiv 2608.21345][LLM Reasoning] 本文通过逐阶段独立改变生成器、批评器与修订器的模型规模，研究自我修正流水线中算力应如何非均匀分配。"
arxiv_id: "2608.21345"
announcement_date: "2026-08-24"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-25T01:58:07.542994+00:00"
source_sha256: "36ecc424745480cd627607e95e9c39cf8f316112ab0492cd6d8e04cccef1babb"
tags:
  - "LLM Reasoning"
  - "大语言模型"
  - "自我精炼"
  - "生成—批评—修订"
  - "模型容量分配"
  - "推理时计算"
  - "阶段式规模分析"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.21345</p>

# Asymmetric Capacity Allocation in Self-Refinement Pipelines

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Zhuoyi Yang, Ian G. Harris, Salar Hashemitaheri, Cassie Huang, Yuangang Li, Hyunwoo Oh, Paul Dourish, Tony Givargis, Mohsen Imani, Li Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of California, Irvine；Affiliation: Drexel University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.21345) · [PDF 下载](https://arxiv.org/pdf/2608.21345) · **关键词** 大语言模型, 自我精炼, 生成—批评—修订, 模型容量分配, 推理时计算, 阶段式规模分析<br>


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

本文通过逐阶段独立改变生成器、批评器与修订器的模型规模，研究自我修正流水线中算力应如何非均匀分配。

**不用术语来说**：语言模型常先给出答案，再检查问题，最后依据检查意见修改答案；这三个步骤的难度和作用并不相同，但现有系统往往凭经验选模型，或让各步骤使用同等规模的模型。这样可能把大量计算花在扩容收益很小的步骤上，也可能因负责修改的模型能力不足，使最终答案反而差于初始答案。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 开展作者所称的首个自我修正流水线逐阶段模型规模研究：分别改变生成器、批评器和修订器的规模，同时固定另外两个阶段，并在两个模型家族和五个跨领域基准上比较各阶段对模型容量的敏感性。
- 识别出非对称的容量需求：生成与修订阶段通常更依赖模型规模，过小的修订器可能损害初始结果；批评阶段对规模相对不敏感，但保留轻量批评器仍优于完全取消显式批评。据此提出各阶段不应统一配置模型容量。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型在推理阶段的“自我精炼”流程。该流程不把模型的首次回答直接作为最终结果，而是依次执行生成、批评和修订：生成器根据输入给出初始解，批评器以自然语言指出其中的问题，修订器再结合原输入、初始解和反馈生成最终解。此类流程已用于推理、规划、代码和文本生成，也是许多智能体工作流中评估与改进中间结果的基本机制。与主要研究反馈机制或修订算法的既有工作不同，本文关注一个更基础的系统设计变量——三个阶段应分别配置多大容量的模型，而非默认统一使用相同规模或凭经验选型。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自我精炼（self-refinement）**

一种推理时改进机制：模型先生成答案，再对答案进行批评，最后依据批评完成修订。它通常不要求额外训练，而是通过增加多阶段推理计算来提高输出质量。

</div>
<div class="concept-item" markdown="1">

**模型容量与模型规模**

模型容量表示模型学习和执行复杂任务的能力，本文以同一模型家族中的不同参数规模作为可控代理变量。更大的模型通常能力更强，但推理所需的计算与部署资源也更高。

</div>
<div class="concept-item" markdown="1">

**阶段式容量分配**

在生成器、批评器和修订器三个功能不同的阶段分别选择模型规模，而不是让整条流水线统一放大或缩小。其目标是在维持任务效果的同时，避免把昂贵模型配置给对规模不敏感的阶段。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定任务输入$x$，生成器首先产生初始解$y_0$；批评器读取$x$与$y_0$并输出自然语言反馈$f$；修订器随后根据$x$、$y_0$和$f$生成最终修订结果。研究假设三个阶段可以由同一家族中不同规模的模型承担，并通过在固定另外两个阶段时单独改变某一阶段的模型规模，考察整体任务表现对生成器、批评器和修订器容量的敏感程度。核心问题不是提出新的反馈或修订算法，而是确定多阶段自我精炼系统中的模型容量是否应均匀配置，以及计算资源应优先投入哪些阶段。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入问题或任务实例。

</div>
<div class="notation-item" markdown="1">

**$y_0$**

生成器根据输入产生的初始解。

</div>
<div class="notation-item" markdown="1">

**$f$**

批评器针对输入与初始解生成的自然语言反馈。

</div>
<div class="notation-item" markdown="1">

**$y$**

修订器综合输入、初始解与反馈后得到的最终输出；该符号的具体写法在所给节选中未明确展示。

</div>

</div>

**直接相关的工作**

- **SELF-REFINE（Madaan et al., 2023）**: 该工作证明单个语言模型可以在无需额外训练的情况下迭代地产生反馈并改进自身输出，奠定了本文所采用的生成—批评—修订范式；但其重点并非系统比较三个阶段各自对模型规模的敏感性。
- **推理时计算分配方法：LLM routing、model cascading 与 adaptive model selection**: 这些方法根据输入难度或计算预算选择回答查询的模型，主要把推理视为单一预测阶段；本文则研究计算能力如何分配给相互依赖的生成、批评和修订阶段，因此分析单位由“查询或模型选择”转为“流水线内部阶段”。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

生成—批评—修订式自我修正已用于推理、规划、代码生成及智能体工作流，因此每次任务可能连续调用多个模型。若所有阶段都默认使用大模型，部署成本会随调用次数累积；若为节省资源而随意缩小某一阶段，又可能破坏修正效果。实际系统需要知道有限算力应优先投入哪个阶段。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **启发式模型选型**：现有自我修正系统通常根据经验或实现便利，为生成器、批评器和修订器选择模型规模，把容量配置视为工程细节，而非需要控制变量研究的设计问题。
- **整条流水线统一扩容**：另一类做法让各阶段使用相同或同步增大的模型，默认生成、评价和修改都能从额外容量中获得近似收益，而不单独测量每个阶段的规模效应。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 启发式配置没有隔离单个阶段的贡献，因而无法判断性能变化究竟来自生成器、批评器还是修订器，也不能形成可迁移的容量配置依据。
- 统一扩容忽略三个阶段承担的认知功能不同，可能在边际收益有限的阶段浪费计算资源，同时掩盖能力不足的关键阶段对最终输出造成的负面影响。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未在受控条件下系统刻画生成器、批评器和修订器各自随模型规模变化的性能曲线，也未检验有效自我修正是否真的要求三个阶段具有相近能力；因此缺少跨任务、跨模型家族的阶段级容量配置证据。

</div>
<div markdown="1"><span>核心问题</span>

在生成—批评—修订流水线中，应如何在三个阶段之间分配模型容量，以及各阶段的规模变化对最终性能分别有多敏感？

</div>
<div markdown="1"><span>作者直觉</span>

生成器负责建立初始解答基础，修订器需要综合原问题、初始答案和反馈并真正完成纠错，因此二者可能需要较强的表达与推理能力；批评器只需指出问题并提供方向，较小模型也可能产生足够有用的反馈。通过每次只改变一个阶段、固定其余阶段，可以把这种直觉转化为可比较的阶段级证据，并据此把更多算力留给真正限制最终质量的环节。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文的方法不是提出新的模型架构或训练目标，而是建立一个受控实验框架，用于判断自精炼流程中不同阶段的模型容量分别有多重要。给定输入 $x$，生成器 $G$ 先产生初始答案 $y_0$；批评器 $C$ 结合输入与初始答案生成自然语言反馈 $f$，指出潜在错误并给出可执行建议；精炼器 $R$ 再依据 $x$、$y_0$ 和 $f$ 输出最终答案 $y_r$。完整配置记作 $P(G,C,R)$，其中三个位置分别指定生成器、批评器和精炼器所用模型。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始答案生成

生成器 $G$ 根据任务提示对 $x$ 进行一次确定性解码，得到初始解答 $y_0=G(x)$。

<div class="method-step__io" markdown="1">

**输入**：任务输入 $x$。<br>
**输出**：尚未经过反馈修正的初始答案 $y_0$。

</div>

**直观理解**：这一阶段相当于先独立完成一道题；后续实验通过改变 $G$ 的规模，检验“第一稿质量”对最终结果有多大影响。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自然语言批评

批评器 $C$ 计算 $f=C(x,y_0)$，以自然语言描述答案中的潜在错误并提供可执行的修改建议。

<div class="method-step__io" markdown="1">

**输入**：原始输入 $x$ 与初始答案 $y_0$。<br>
**输出**：批评反馈 $f$。

</div>

**直观理解**：批评器不直接提交最终答案，而是扮演审阅者；其价值在于帮助精炼器定位问题，而不只是让模型无指导地再回答一次。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 反馈驱动的答案精炼

精炼器 $R$ 联合使用三项信息，计算 $y_r=R(x,y_0,f)$，生成最终解答。

<div class="method-step__io" markdown="1">

**输入**：任务输入 $x$、初始答案 $y_0$ 和批评反馈 $f$。<br>
**输出**：精炼后的最终答案 $y_r$。

</div>

**直观理解**：该阶段类似作者依据审稿意见修改初稿；改变 $R$ 的规模可检验“理解并执行反馈”的能力是否需要较大模型。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 逐阶段容量扫描与无批评对照

每次只改变 $G$、$C$ 或 $R$ 中一个阶段的模型规模，其余两个阶段固定为相同模型；另将采用 Qwen3-0.6B 批评器的流程与移除批评器但保留精炼步骤的匹配流程比较。

<div class="method-step__io" markdown="1">

**输入**：不同规模的 Qwen3 或 Gemma 3 模型、各基准任务，以及完整流程 $P(G,C,R)$ 和无批评流程 $P(G,\emptyset,R)$。<br>
**输出**：生成器、批评器和精炼器的逐阶段容量—性能关系，以及轻量批评器相对无批评精炼的性能增益。

</div>

**直观理解**：这是一种控制变量设计：一次只更换一个岗位上的模型，避免把性能变化错误归因于多个同时变化的因素；无批评对照则区分收益究竟来自明确反馈，还是仅来自额外生成一遍答案。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 三阶段自精炼映射

$$
\begin{aligned} y_0 &= G(x),\\ f &= C(x,y_0),\\ y_r &= R(x,y_0,f). \end{aligned}
$$

**符号说明**

- $x$：待求解任务的输入。
- $G$：生成器模型。
- $y_0$：生成器产生的初始答案。
- $C$：批评器模型。
- $f$：针对初始答案的自然语言批评，包括潜在错误与可执行建议。
- $R$：精炼器模型。
- $y_r$：结合初始答案与批评后得到的最终答案。

<div class="equation-explanation" markdown="1">

**直观理解**：三式依次刻画初稿、审阅和修改：后一阶段接收前一阶段产物，但精炼器还保留原始任务与初始答案，以免只依赖可能不完整或错误的批评。它定义了论文进行容量分配实验的基本计算路径。<br>
**原文位置**：第 3.1 节 Self-Refinement Pipeline

</div>

</div>

<div class="equation-block" markdown="1">

#### 显式批评的增益

$$
\begin{aligned} \Delta_{\mathrm{critique}}^{\mathrm{gen}}(G_i) &= P(G_i,0.6\mathrm{B},R)-P(G_i,\emptyset,R),\\ \Delta_{\mathrm{critique}}^{\mathrm{ref}}(R_i) &= P(G,0.6\mathrm{B},R_i)-P(G,\emptyset,R_i). \end{aligned}
$$

**符号说明**

- $P(G,C,R)$：采用生成器 $G$、批评器 $C$ 和精炼器 $R$ 的完整流程；在差值中，$P$ 表示该流程在相应基准上的性能。
- $G_i$：生成器规模扫描中的第 $i$ 个生成器。
- $R_i$：精炼器规模扫描中的第 $i$ 个精炼器。
- $0.6\mathrm{B}$：作为固定轻量批评器的 Qwen3-0.6B。
- $\emptyset$：不使用批评器，也不向精炼器提供批评反馈。
- $\Delta_{\mathrm{critique}}^{\mathrm{gen}}(G_i)$：固定精炼器时，第 $i$ 个生成器配置中显式批评相对无批评精炼的性能差。
- $\Delta_{\mathrm{critique}}^{\mathrm{ref}}(R_i)$：固定生成器时，第 $i$ 个精炼器配置中显式批评相对无批评精炼的性能差。

<div class="equation-explanation" markdown="1">

**直观理解**：两项差值都比较“有轻量批评”与“无批评但仍进行精炼”，因此尽量消除额外精炼轮次带来的影响。正差值表示显式批评优于无指导修订，但由于固定使用特定的 Qwen3-0.6B 批评器，该量首先反映这一批评器及当前任务、模型组合下的效果。<br>
**原文位置**：第 3.3 节 No-Critique Baseline

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。所给章节描述的是预训练模型的推理期组合与受控容量分析，没有提出损失函数、参数更新规则或额外训练过程；这里的“objective”是实验目标，即通过一次只改变一个阶段的模型规模，量化该阶段容量对流程性能的贡献，而不是用于梯度优化的训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 生成器—批评器—精炼器三阶段流程**

流程记为 $P(G,C,R)$：$G$ 产生 $y_0$，$C$ 根据 $(x,y_0)$ 产生反馈 $f$，$R$ 根据 $(x,y_0,f)$ 产生 $y_r$。三个角色可以由不同参数规模的模型承担，例如 $P(32\mathrm{B},0.6\mathrm{B},32\mathrm{B})$ 表示使用 32B 生成器、0.6B 批评器和 32B 精炼器。

> 直观理解：将一次回答拆成“写初稿—提意见—改稿”三个角色，才能分别研究算力应该分配到哪个角色，而不是只比较整套系统的总规模。

**2. 逐阶段模型规模分析协议**

生成器扫描评估 $P(G_i,C,R)$，批评器扫描评估 $P(G,C_i,R)$，精炼器扫描评估 $P(G,C,R_i)$；每次扫描仅改变带下标 $i$ 的模型，其余两阶段固定。该过程在每个基准和每个模型家族上重复；原文示例中的 Qwen3-32B 固定配置会将生成器依次替换为 0.6B、1.7B、4B、8B、14B 和 32B。

> 直观理解：该协议要回答的不是“最大模型是否最好”，而是“把额外容量放在哪一阶段最有效”。固定其他阶段可使观察到的差异更接近被扫描阶段的独立贡献，但它仍是受所选模型家族和固定配置约束的实验性归因。

**3. 匹配的无批评基线**

无批评流程记为 $P(G,\emptyset,R)$：删除 $C$，让 $R$ 在没有反馈 $f$ 的情况下直接修订 $y_0$。比较时将显式批评流程的批评器固定为 Qwen3-0.6B，并分别沿生成器和精炼器规模扫描计算批评增益，最后按基准汇总两类扫描的平均增益。

> 直观理解：如果只比较一次生成与完整三阶段流程，提升可能只是因为多进行了一次推理；这个基线保留第二次改写，只拿掉批评文本，因此更直接地检验“明确意见”本身是否有用。

**训练与推理**

该方法完全按推理流程执行。对每个基准和模型家族，先用任务专用的少样本提示让 $G$ 生成 $y_0$，再让 $C$ 输出反馈 $f$，最后让 $R$ 生成 $y_r$；随后分别进行生成器、批评器和精炼器扫描，每次只替换目标阶段的模型规模。为检验批评的独立作用，还运行结构匹配的 $P(G,\emptyset,R)$：精炼器仍执行一次修订，但不接收 $f$；显式批评侧固定采用 Qwen3-0.6B，并在生成器与精炼器扫描中分别计算差值，再对每个基准汇总平均批评增益。原文未报告任何针对这些任务重新训练或微调模型的步骤。

**复现信息**

实验使用 Qwen3 与 Gemma 3 模型，并在 NVIDIA H100 GPU 上运行。生成器、批评器和精炼器分别使用任务专用少样本提示；所有模型规模和流程阶段统一采用贪心解码，温度设为 $0.0$，最大输出长度为 700 个新 token。统一解码设置是公平解释容量差异的关键，因为它减少了采样随机性、温度或输出预算变化对结果的混淆；完整提示模板据原文位于附录，但当前节选未提供其具体内容。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 五类任务基准：Meeting Planning（500个样例，限制为最多5人，用于测试满足时间与出行约束的规划）；CNN/DailyMail（官方v1.0.0测试集前500个样例，用于测试摘要信息覆盖）；ZebraLogic（320个样例，限制为最多10个单元格，用于测试逻辑网格求解）。
- PIE（随机抽取500个样例，用于测试程序优化后是否同时保持功能正确并实现优化）；该任务计算代价较高，因此采用随机子集。
- CollaboSentGen（从ROCStories衍生，随机抽取500个样例，用于测试缺失句子的关键词条件生成及其与上下文的连贯性）。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

原文未明确报告，或这里不需要额外前置概念。

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3-32B固定其余阶段时的生成器规模扫描

<div class="result-value" markdown="1">

生成器规模增大在五个基准上都稳定提升端到端性能。Qwen3生成器扫描的标准差在CollaboSentGen为0.96个百分点、在PIE为10.43个百分点；这表明生成器容量在不同任务上都重要，但影响幅度依任务而异。

</div>

生成器负责产生最初的解答，因此更大的生成器能提供更好的起点，后续阶段也更容易在此基础上修正。该结果支持“生成阶段需要容量”，但不能单独证明生成器必须比其他阶段更大，也不能说明所有任务的绝对性能都同样提升。

<div class="result-source" markdown="1">

来源：第5.1节 Finding 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under the Qwen3 family, the generator exhibits standard deviations ranging from 0.96 on CollaboSentGen to 10.43 percentage points on PIE, indicating that generator scaling substantially affects pipeline performance.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3-32B固定其余阶段时的批评器规模扫描

<div class="result-value" markdown="1">

批评器规模对端到端性能最不敏感。表1显示，在Qwen3下，批评器标准差为Meeting Planning 3.10、CNN/DailyMail 3.10、ZebraLogic 1.46、PIE 1.63、CollaboSentGen 0.20；这些波动整体低于生成器和修订器。人工分析还显示，在ZebraLogic上，32B批评器产生的非误导性批评占70%，0.6B批评器为64%。

</div>

较大批评器往往能发现更多错误，但小批评器通常已经能给出基本正确或至少不误导的反馈；真正限制收益的可能是修订器不会充分利用额外信息。因此，批评器并非没有作用，而是继续扩大其规模的边际收益较小。

<div class="result-source" markdown="1">

来源：第5.2节 Finding 2.1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across all benchmarks and both model families, the critic consistently exhibits the lowest variability.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen3-32B固定其余阶段时的修订器规模扫描

<div class="result-value" markdown="1">

修订器对模型规模最敏感。Qwen3下，修订器标准差在PIE达到20.60个百分点，而批评器为1.63个百分点；Meeting Planning中分别为11.20和3.10个百分点，CNN/DailyMail中分别为8.99和3.10个百分点。弱修订器还可能使结果低于初始生成：30条修订器配置中有12条出现这种退化。

</div>

修订器不仅要读懂批评，还要决定哪些内容应保留、哪些内容应修改，并执行正确修改，因此它是把批评转化为最终质量的关键瓶颈。该结果说明扩大修订器通常比扩大批评器更值得优先考虑，但退化比例来自特定配置和子集，不能据此推断所有任务或所有模型都会退化。

<div class="result-source" markdown="1">

来源：第5.3节 Finding 3.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under the Qwen3-32B configuration, 12 of the 30 evaluated refiner pipelines (5 benchmarks × 6 refiner sizes) perform worse than the corresponding initial generation.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 各基准只使用受限子集：Meeting Planning和ZebraLogic限制问题难度，其他任务多采用500个样例；因此结论对完整测试集、更困难实例和不同数据分布的外推仍有限。
- 批评质量只在每个基准从0.6B和32B批评器各抽取50条样本进行人工评估，且Overall-Story-Fit依赖GPT-4自动评分；人工量表、自动评估器及任务专用指标都可能影响对批评质量和端到端收益的判断。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 无批评基线$P(G,\varnothing,R)$：生成器输出直接交给修订器，不提供显式批评，用于区分“批评信息的作用”和“仅增加一次推理步骤”的作用。
- 初始生成性能：不经过修订的生成器输出，图4以灰色虚线表示，用于判断自我修正是否真正改善原始答案，而非只比较不同流水线之间的相对差异。

**实验想回答的问题**

- 在自我修正流水线中，生成器、批评器和修订器分别对模型规模有多敏感；扩大哪个阶段的模型容量最能改善端到端性能？
- 批评器规模较小仍能否带来有效的自我修正，以及弱修订器是否会抵消批评带来的收益甚至损害初始输出？

**实验实现**

实验使用Qwen3和Gemma 3两个开放权重模型族。Qwen3覆盖$0.6\mathrm{B}$、$1.7\mathrm{B}$、$4\mathrm{B}$、$8\mathrm{B}$、$14\mathrm{B}$和$32\mathrm{B}$；主结果固定另外两个阶段为Qwen3-32B，并独立扫描一个阶段的模型规模。Gemma 3使用1B-IT、4B-IT、12B-IT和27B-IT进行泛化验证；另以Qwen3-14B和Qwen3-8B作为最大固定模型开展稳健性分析。每条流水线包含生成器、批评器和修订器三个阶段，三个阶段均采用任务专用少样本提示。作者从每个基准随机抽取0.6B和32B批评器各50条批评，使用五级人工量表评估批评是否正确、全面及具有误导性。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 最小批评器$\mathrm{Qwen3}\text{-}0.6\mathrm{B}$对比无批评基线 | 在生成器扫描和修订器扫描中，使用0.6B批评器相对于匹配的无批评基线，在Meeting Planning上的平均提升分别为+9.67和+10.34个百分点；其余四个基准也观察到类似提升。 | 该对照隔离了显式批评的增益：即使批评器很小，提供具体反馈也比让修订器盲目重写更有效。因此，收益不能简单归因于增加计算量；不过表中给出的平均增益只明确列出了Meeting Planning的数值，其他基准的具体数值原文未明确报告。 | 第5.2节 Finding 2.2；表3<br><span class="experiment-evidence">We observe that even incorporating the smallest explicit critic would yield improvements over the initial generation across all five benchmarks, as shown in Table 3.</span> |
| 弱修订器$0.6\mathrm{B}$与强修订器$32\mathrm{B}$的退化事件分析 | 在最极端配置$P(32\mathrm{B},32\mathrm{B},0.6\mathrm{B})$中人工分析50个退化事件：全部事件中0.6B修订器都比同一初始解和32B修订器产生更差输出；其中41个事件虽收到非误导性批评，0.6B修订器仍不必要地改动正确内容，另外9个事件则传播了误导性批评。 | 这项分析区分了两类失败：修订器可能过度修改本来正确的内容，也可能无法识别并拒绝错误反馈。强修订器的优势不只是“执行更多修改”，而是更能保留正确部分并选择性应用批评；但这是50个案例的人工归因分析，不等同于对所有样例的统计保证。 | 第5.3节 Finding 3.2<br><span class="experiment-evidence">In all 50 degradation events, the 0.6B refiner produced a worse output than both the initial generation and the 32B refiner under the same initial solution and critique.</span> |

**定性案例**

- Meeting Planning的代表性案例中，初始行程将Ronald安排为60分钟而其会议需要75分钟，并将Nancy安排在可用时间窗之外。0.6B批评器只指出“Ronald’s meeting is only 60 min”，而32B批评器同时发现两个错误；该例说明大批评器可以提供更完整的诊断，但论文同时指出修订性能提升仍较有限，暗示额外信息未必会被修订器充分利用。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：标题表明其核心是自我精炼推理流程中的计算能力分配，属于推理期扩展与验证方向。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`36ecc424745480cd627607e95e9c39cf8f316112ab0492cd6d8e04cccef1babb`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
