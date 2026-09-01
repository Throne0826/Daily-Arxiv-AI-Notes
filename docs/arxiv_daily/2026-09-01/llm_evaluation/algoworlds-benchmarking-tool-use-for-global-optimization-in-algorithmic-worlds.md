---
title: "[论文解读] AlgoWorlds: Benchmarking Tool Use for Global Optimization in Algorithmic Worlds"
description: "[arXiv 2608.29397][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.29397"
announcement_date: "2026-09-01"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:41:03.649271+00:00"
source_sha256: "d6e73cca07a0d4a01123182ca561ee9c8e0bdc185091f00c56c52fee68ab0d98"
tags:
  - "LLM 评测"
  - "LLM Agent"
  - "LLM Reasoning"
  - "大语言模型智能体"
  - "工具使用"
  - "组合优化"
  - "全局最优性"
  - "部分可观测决策环境"
  - "算法世界基准"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.29397</p>

# AlgoWorlds: Benchmarking Tool Use for Global Optimization in Algorithmic Worlds

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Zixiang Xu, Jiaan Wang, Fandong Meng</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Weixin AI, Tencent；Affiliation: University of Southern California</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.29397v1) · [PDF 下载](https://arxiv.org/pdf/2608.29397v1) · **关键词** 大语言模型智能体, 工具使用, 组合优化, 全局最优性, 部分可观测决策环境, 算法世界基准<br>
**代码**: [https://github.com/xzx34/AlgoWorlds/](https://github.com/xzx34/AlgoWorlds/) · **项目页**: [https://xzx34.github.io/AlgoWorlds/](https://xzx34.github.io/AlgoWorlds/)

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

本文位于大语言模型工具使用评测与组合优化交叉领域。传统工具使用基准主要检查智能体能否选择合适的工具、提供有效参数并完成预设流程；组合优化则研究在一组离散决策中满足全部约束并使总体目标达到最优的问题。本文关注二者的交叉情形：智能体只能通过有代价的工具调用逐步观察隐藏实例，随后必须提交一个整体决策；该决策不仅要可行，还要达到由精确算法验证的全局最优值。因此，评测对象不是单次工具调用，而是从信息获取、跨来源整合、联合约束推理到最终决策核验的完整能力链条。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**组合优化**

组合优化是在有限或离散的候选决策中寻找满足约束且目标函数最优的方案。例如车辆分配中，不能只让每项任务选择局部最便宜的路线，还必须同时考虑车辆容量、资格限制以及所有车辆共同产生的启用成本。

</div>
<div class="concept-item" markdown="1">

**全局最优与可行性**

可行性表示决策满足所有任务约束；全局最优表示在所有可行决策中，目标值达到最好。可行方案可能仍然明显劣于最优方案，因此仅报告任务是否完成会高估智能体的决策能力。

</div>
<div class="concept-item" markdown="1">

**部分可观测工具环境**

环境中的完整问题实例不会直接展示给智能体，智能体只能通过任务专用工具查询其中不同部分的信息，并在预设访问预算内决定下一步查询什么。查询结束后，智能体需要输出一个结构化决策，由独立检查器判断其约束可行性、目标值和是否达到全局最优。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

AlgoWorlds 将每个测试案例定义为一个算法世界：世界包含任务查询、一个隐藏的组合优化实例以及若干任务专用信息工具。隐藏实例决定哪些决策可行及其目标值，但智能体初始只能看到查询和工具，不能直接看到实例；它通过连续工具调用收集信息，每次调用消耗预先规定的访问成本，并受总访问预算约束。工具返回的信息来自实例的不同部分，例如城市之间的旅行距离。智能体在信息获取阶段结束后提交一个结构化决策，独立检查器输出该决策是否可行、目标值以及是否等于经过精确算法认证的全局最优值。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{I}$**

一个隐藏的组合优化实例，包含决定可行决策与目标值的具体案例信息。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{T}$**

一组任务专用信息工具；不同工具向智能体暴露隐藏实例的不同部分。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{D}$**

智能体最终提交的结构化决策，例如对任务、车辆或路线的整体分配结果。

</div>
<div class="notation-item" markdown="1">

**$f(\mathcal{D};\mathcal{I})$**

决策在隐藏实例上的目标值；只有满足实例约束的决策才可用于与全局最优值比较。

</div>

</div>

**直接相关的工作**

- **Li et al. (2023)**: 本文将其作为传统工具使用基准的代表，指出这类基准通常重点评估工具选择、参数有效性和流程完成，而没有充分检验最终决策是否达到全局最优。
- **Yan et al. (2024)**: 本文将其与其他工具使用评测工作并列为研究背景，作为“完成工作流”型评测的代表；AlgoWorlds 在此基础上增加隐藏组合优化实例、访问预算以及可验证的全局最优性要求。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

AlgoWorlds不是训练一个新模型，而是把十类形式化组合优化问题转换为部分可观测的工具使用环境，用于测试大语言模型能否从工具返回的信息中恢复隐藏实例，并一次性提交满足约束且达到全局最优的结构化决策。每个环境由文本问题$q$、隐藏实例$\mathcal{I}$、带成本的信息工具集合$\mathcal{T}_{\mathrm{info}}$、一次性的零成本最终决策工具$t_{\mathrm{dec}}$、工具成本函数$f_c$和预算$b$组成；构造阶段用确定性生成器产生实例，用专门的精确算法求得并独立验证唯一最优解，再用Direct和Mediated两种工具接口呈现同一个实例。直观地说，模型不能直接看到完整题目，而要像调查员一样付费查询资料，最后在预算内根据分散信息作出一个整体决策；评测重点不是“是否能完成流程”，而是“是否能把信息整合成全局最优方案”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 形式化优化任务与隐藏世界

为每个任务生成文本问题$q$和隐藏实例$\mathcal{I}$，并定义信息工具集合$\mathcal{T}_{\mathrm{info}}$、最终决策工具$t_{\mathrm{dec}}$、工具成本函数$f_c$与访问预算$b$。$q$只说明要作出的决策、必须满足的约束和优化目标，不直接公开实例中的具体数据。

<div class="method-step__io" markdown="1">

**输入**：十个组合优化问题族的形式化定义，包括决策变量、可行性约束、目标函数，以及实例规模和结构配置。<br>
**输出**：一个算法世界$w=\{q,\mathcal{I},\mathcal{T},f_c,b\}$，其中$\mathcal{T}=\mathcal{T}_{\mathrm{info}}\cup\{t_{\mathrm{dec}}\}$，而模型初始只能获得$w\setminus\mathcal{I}$。

</div>

**直观理解**：这一步把普通的优化题改造成“看不完整信息的决策题”。例如在车队调度中，模型知道目标是给每个工作分配车辆，却必须通过工具查询载荷、容量、可服务关系、路线价格和启用费用。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 确定性生成实例并认证最优解

对每个实例运行该问题族的精确算法，求出全局最优决策和目标值，并使用独立实现、不同状态方向或问题表述的精确求解器再次验证；只有当两次求解在最优决策、最优值和唯一最优性上均一致时，实例才被保留。

<div class="method-step__io" markdown="1">

**输入**：每个问题族预先规定的规模配置和结构配置，以及由生成器产生的候选实例$\mathcal{I}$。<br>
**输出**：具有可行解、唯一且经过双重验证的全局最优解的隐藏实例，以及用于划分工作负载等级的精确算法操作数。

</div>

**直观理解**：评测答案前，作者先用可靠的“标准答案程序”把正确解算出来，并用另一套程序交叉检查。这样模型得分不是和启发式答案比较，而是和可验证的全局最优解比较。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 按精确算法工作量划分难度

计算$\operatorname{Work}(\mathcal{I})$，并依据不同问题族的操作数把实例分到四个工作负载等级，而不是直接按原始变量数量或输入长度对齐难度。

<div class="method-step__io" markdown="1">

**输入**：每个已认证实例及其构造阶段精确算法执行的状态访问、转移考察、约束检查、数值更新和决策重构操作。<br>
**输出**：四个可跨任务族比较的工作负载等级：$[2^{15},2^{17}]$、$[2^{19},2^{21}]$、$[2^{22},2^{24}]$和$[2^{24},2^{26}]$。

</div>

**直观理解**：不同题型的“规模”不能直接比较：十个决策和十个决策可能需要完全不同的搜索量。作者因此用求解标准答案程序实际做了多少基本工作来定义难度。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 构造双接口环境并执行模型轨迹

分别用Direct接口$\mathcal{T}_{\mathrm{d}}$和Mediated接口$\mathcal{T}_{\mathrm{m}}$映射实例字段为工具，保持$q$、$\mathcal{I}$、$f_c$和$b$不变，仅改变信息之间的关系呈现方式；模型依次调用信息工具并接收观察结果$o_{s_i}$，累计成本不得超过$b$，最后只能调用一次$t_{\mathrm{dec}}(y)$提交完整决策$y$。

<div class="method-step__io" markdown="1">

**输入**：同一个隐藏实例$\mathcal{I}$、文本问题$q$、工具成本和预算，以及可复用的世界构造模板。<br>
**输出**：十个问题族、四个工作负载等级、每级三个隐藏实例和两种接口共同产生的$10\times4\times3\times2=240$个算法世界，以及每个模型的工具轨迹、收集信息和最终决策。

</div>

**直观理解**：同一份事实会通过两种组织方式展示：一种更直接，另一种需要跨工具拼接关系。模型不仅要决定查什么，还要在预算内记住并组合查询结果，最终不能逐步修改答案，只能提交一次完整方案。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 算法世界与工具轨迹约束

$$
w=\{q,\mathcal{I},\mathcal{T},f_c,b\},\qquad \pi(w\setminus\mathcal{I})\rightarrow t_{s_1}\rightarrow o_{s_1}\rightarrow\cdots\rightarrow t_{s_k}\rightarrow o_{s_k}\rightarrow t_{\mathrm{dec}}(y),\qquad \sum_{i=1}^{k}f_c(t_{s_i})\le b
$$

**符号说明**

- $w$：一个算法世界。
- $q$：文本问题，描述决策、约束和优化目标。
- $\mathcal{I}$：隐藏的具体优化实例。
- $\mathcal{T}$：全部任务工具，包括信息工具和最终决策工具。
- $f_c$：工具成本函数。
- $b$：信息查询的总预算上限。
- $\pi$：被评测的大语言模型代理。
- $t_{s_i}$：轨迹第$i$步调用的信息工具。
- $o_{s_i}$：工具调用返回的观察结果。
- $t_{\mathrm{dec}}(y)$：提交最终结构化决策$y$的唯一一次调用。

<div class="equation-explanation" markdown="1">

**直观理解**：该式规定了整个交互协议：模型从不直接看到隐藏实例，只能交替进行工具调用和观察，并且所有信息调用的成本不能超过预算，最后提交一次决策。这使工具使用、信息整合和最终优化决策成为一个连续过程，而不是三个独立测试。<br>
**原文位置**：第3.1节，式(1)–(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 算法工作量

$$
\operatorname{Work}(\mathcal{I})=N_{\mathrm{state}}+N_{\mathrm{transition}}+N_{\mathrm{check}}+N_{\mathrm{update}}+N_{\mathrm{reconstruct}}
$$

**符号说明**

- $\operatorname{Work}(\mathcal{I})$：精确求解器处理实例$\mathcal{I}$时统计的总基本操作数。
- $N_{\mathrm{state}}$：访问状态的次数。
- $N_{\mathrm{transition}}$：考察状态转移的次数。
- $N_{\mathrm{check}}$：执行约束检查的次数。
- $N_{\mathrm{update}}$：进行目标值或状态更新的次数。
- $N_{\mathrm{reconstruct}}$：重构最终决策组成部分的次数。

<div class="equation-explanation" markdown="1">

**直观理解**：作者用标准精确算法实际完成了多少基本计算来衡量难度，并据此把不同题型放入四个等级。这样比较的是求解负担，而不是表面上的输入大小。<br>
**原文位置**：第4.2节，式(6)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文没有提出或训练新的模型，也未定义模型参数的训练损失；AlgoWorlds是用于推理时评测的基准。其核心优化目标属于每个任务实例本身：模型提交的决策$y$必须满足该任务的约束，并使任务目标达到经验证的全局最优值；构造阶段的精确算法负责计算标准答案，模型本身不会看到这些算法。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 问题族专用精确求解器**

十个问题族分别使用与其全局耦合结构相匹配的精确算法，包括残差与末条带动态规划、精确覆盖位掩码动态规划、资源感知带状前沿动态规划、混合进制容量动态规划、扩展状态最短路和激活域掩码枚举等。算法在构造阶段维护未来决策所依赖的状态，例如Fleet Dispatch在逐项处理工作时维护各车辆剩余容量向量及已经产生的启用费用。

> 直观理解：每类题都有自己的“不会漏解的标准计算器”。它不能只分别选择当前最便宜的动作，因为当前选择会改变后续容量、转移费用、激活费用或可用组合。

**2. 工具成本与部分观测机制**

信息工具可重复调用，但满足$\sum_i f_c(t_{s_i})\le b$；最终决策工具零成本且只能在轨迹末尾调用一次。每个环境预先定义至少一种在预算内足以重建$\mathcal{I}$并恢复最优解的信息集合，同时验证穷举所有工具的成本超过预算。

> 直观理解：预算机制把“查得越多越好”变成了查询规划问题。作者保证答案原则上可以被查到，但不能把所有资料一次性全部打开，因此模型必须取舍。

**3. 质量验证与诊断评估**

环境保留条件包括存在可行决策、唯一全局最优解，以及工具预算内存在充分信息获取方式。除最终决策的可行性、精确最优性和参考效用外，还根据轨迹中已获得的信息$\mathcal{A}_w(\tau)$与充分信息集合$\mathcal{S}(w)$计算信息充分性$C_w(\tau)$和发现覆盖率$D_w(\tau)$，从而区分“没有查够信息”和“查够但不会整合”。

> 直观理解：评测不只看最后答案对不对，还检查模型是否已经拿到了足以解题的资料。如果资料已经足够却仍然答错，问题就更可能出在全局推理、约束整合或答案核验，而不是信息获取。

**训练与推理**

训练阶段：原文未明确报告针对AlgoWorlds进行模型训练、微调或基准专用目标函数，因此不能据此推断存在训练流程。推理阶段：模型接收$q$、工具说明、成本函数$f_c$和预算$b$，但不接收$\mathcal{I}$；随后根据任务和历史轨迹选择信息工具，读取工具返回的观察，控制累计查询成本，在预算内尽可能获得一个充分信息集，最后通过$t_{\mathrm{dec}}$提交一次完整决策$y$。评测器检查$y$是否可行、是否达到认证最优值，并结合轨迹计算信息充分性和发现覆盖率；若未提交最终决策，三项最终决策指标均记为零。

**复现信息**

可复现的关键实现包括：每个问题族使用人工编写的确定性生成器，使相同配置产生一致实例；每个实例由专用精确算法求解，并由独立精确实现交叉验证唯一最优解；同一实例通过Direct和Mediated两套接口呈现，二者共享$q$、$\mathcal{I}$、$f_c$和$b$，只改变信息的关系结构。数据规模为十个问题族、四个工作负载等级、每级三个隐藏实例，先形成$120$个隐藏实例，再通过两种接口形成$240$个算法世界；原文未明确报告更细的工具实现代码、模型提示词或运行时解码设置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- AlgoWorlds 基准共含 240 个部分可观测决策环境，覆盖 10 类组合优化问题和 4 个工作负载等级。每个环境的实例由问题族专用的确定性程序生成，并由精确算法认证全局最优解；其作用是把工具使用能力置于可客观验证的全局优化任务中。
- 每个隐藏实例通过两种结构不同的工具接口呈现。两种接口对应同一底层实例，用于考察模型表现是否依赖特定的信息组织或查询形式，而不只是问题本身的难度。原文节选未说明训练集、验证集和测试集划分。
- 评测覆盖路线规划、调度等共享约束与成本下的组合决策抽象。环境要求智能体先调用任务专用信息工具了解隐藏实例，再提交一个结构化决策；该决策同时接受可行性和全局最优性检验。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**精确最优率**

模型提交的结构化决策既满足全部约束，其目标值又与精确算法认证的全局最优值完全一致的环境比例。该指标比仅检查工具调用是否合法或任务是否完成更严格。 （越高越好，因为更高比例表示模型更经常把工具获得的信息转化为真正的全局最优决策，而非仅找到一个可行解。）

</div>
<div class="metric-item" markdown="1">

**可行率**

模型提交满足问题全部硬约束的环境比例，不要求目标值达到全局最优。它用于区分约束违反与优化不足这两类失败。 （越高越好，因为这表示模型更能生成合法决策；但高可行率本身不能证明模型具有全局优化能力。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 七个领先模型在 AlgoWorlds 全部组合优化环境上的精确全局最优表现

<div class="result-value" markdown="1">

最佳模型的精确最优率仅为 38.61%。作者据此认为，即使使用当前领先模型，在部分可观测、需要工具收集信息的组合优化环境中达到全局最优仍然非常困难。

</div>

这意味着表现最好的模型也只在不到四成的评测案例中找到经认证的全局最优决策。该结果直接说明“完成工具工作流”与“做出最佳整体决策”之间存在明显差距；但摘要没有给出各模型、各问题族或各工作负载等级的完整分项结果，因此不能仅凭这一数字判断困难主要集中在哪些任务上。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Achieving global optimality remains highly challenging: although leading models produce feasible decisions in most cases, the best-performing model reaches exact optimality in only 38.61% of cases.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 可行性与精确最优性的对比

<div class="result-value" markdown="1">

领先模型在多数案例中能够产生可行决策，但精确全局最优表现明显较弱。作者的核心结论是，仅以可行性评估工具使用会高估智能体在真实决策问题中的能力。

</div>

模型通常能遵守硬约束，却未必能正确权衡共享资源、成本和决策间相互作用。换言之，它们常能找到“能用”的方案，却找不到“整体最好”的方案。该观察不等于模型完全缺乏优化能力，因为可行且接近最优的解可能仍有实际价值；给定材料没有报告最优差距，因而无法判断次优解究竟偏离最优值多少。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Achieving global optimality remains highly challenging: although leading models produce feasible decisions in most cases, the best-performing model reaches exact optimality in only 38.61% of cases.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 模型已收集足以重建隐藏实例的信息时的失败类型分析

<div class="result-value" markdown="1">

即便智能体收集到足以重建隐藏实例的信息，大多数失败仍以可行但次优的决策结束。作者据此将瓶颈从单纯的信息获取扩展到信息整合、全局约束推理和提交前验证。

</div>

这一分析试图区分“没查到必要信息”和“查到了但没有正确利用”两种原因。结果表明，增加工具调用或暴露更多事实未必足以解决问题，模型还必须把分散观察组合成完整实例，并系统比较候选方案。不过，这是一项失败归因结论；给定材料没有说明“足以重建”的操作化判据或各原因所占比例，因此尚不能量化不同推理瓶颈的相对贡献。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Even when agents collect sufficient information to reconstruct the hidden instance, most failures end in feasible but suboptimal decisions.

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

- GPT-5.6 Terra 与 GPT-5.6 Sol：同一模型系列中的两个领先版本，可比较系列内部不同配置在信息获取和全局优化推理上的表现。
- Claude Opus 4.8 与 Claude Sonnet 5：另一主流闭源模型系列，可用于判断结果是否仅限于 OpenAI 模型。
- Qwen 3.5 Plus、DeepSeek V4 Pro 与 GLM 5.2：来自多个模型系列的对照，扩大架构与训练来源的覆盖范围，检验全局优化困难是否具有跨模型一致性。
- 精确算法认证的最优解不是参与交互的语言模型基线，而是评测参照：它为每个实例提供可验证的全局最优目标值，使模型提交能够被严格区分为不可行、可行但次优或全局最优。

**实验想回答的问题**

- 在只能通过任务专用信息工具观察隐藏优化实例、随后一次性提交结构化决策的条件下，领先大语言模型能否同时满足约束并达到可验证的全局最优？
- 模型失败主要源于信息收集不足，还是源于获得信息之后的整合、全局约束推理与决策验证能力不足？

**实验实现**

实验评测 7 个领先大语言模型，并为所有智能体启用推理模式。每个环境最多允许调用信息工具 255 次，以限制信息获取预算；模型随后提交一个结构化决策。每个智能体运行 3 次，报告均值与样本标准差。实例由确定性程序生成，精确算法负责认证最优解并确定工作负载等级。给定节选指出温度、推理强度等详细超参数另有说明，但未提供其具体取值。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出评测LLM工具使用、隐藏信息整合、全局约束推理与最优决策能力的AlgoWorlds基准。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`d6e73cca07a0d4a01123182ca561ee9c8e0bdc185091f00c56c52fee68ab0d98`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
