---
title: "[论文解读] See, Hypothesize, Validate: Multimodal Agentic Framework for Discovering Governing PDEs"
description: "[arXiv 2608.27869][Multi-Agent] 原文未明确报告。"
arxiv_id: "2608.27869"
announcement_date: "2026-08-31"
primary_category: "multi_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:42:23.669191+00:00"
source_sha256: "06c08845b7852b66abf278147b8c3a451c09463c8fcb7762b42cfdc8f7ca9ec8"
tags:
  - "Multi-Agent"
  - "LLM Reasoning"
  - "偏微分方程发现"
  - "数据驱动科学发现"
  - "多模态智能体"
  - "符号回归"
  - "假设验证"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">Multi-Agent · arXiv 2608.27869</p>

# See, Hypothesize, Validate: Multimodal Agentic Framework for Discovering Governing PDEs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Sarang Manoj Pekhale, Amartya Roy, Rajat Sarkar, Souvik Chakraborty</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Department of Applied Mechanics；Affiliation: Indian Institute of Technology Delhi, India；Affiliation: The School of Interdisciplinary Research；Affiliation: TCS Research, India；Affiliation: Yardi School of Artificial Intelligence (ScAI)</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27869v1) · [PDF 下载](https://arxiv.org/pdf/2608.27869v1) · **关键词** 偏微分方程发现, 数据驱动科学发现, 多模态智能体, 符号回归, 假设验证<br>


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

本文属于数据驱动的偏微分方程（PDE）发现领域，目标是从时空观测数据中反推出描述系统演化规律的方程。典型方法包括基于预定义候选项库的稀疏回归、在开放表达式空间中搜索的符号回归，以及利用大语言模型生成方程；本文进一步引入多模态智能体，使观测图像、数值导数和定量拟合共同参与“观察—提出假设—验证或否证”的发现过程。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**偏微分方程（PDE）**

PDE 是包含多个自变量及其偏导数的方程，用来描述物理场随空间和时间的变化。本文要发现的是这类方程的结构，例如平流、扩散或非线性输运项，而不仅是拟合一个预测模型。

</div>
<div class="concept-item" markdown="1">

**稀疏回归与候选项库**

稀疏回归通常先构造一个候选项库，再从中选择少数能够解释观测数据的项并估计系数。其主要限制是结果的表达能力取决于预先是否把真实物理项放进库中。

</div>
<div class="concept-item" markdown="1">

**时空观测与导数估计**

系统观测通常表示为随空间位置和时间变化的场，例如 $u(x,t)$。发现 PDE 需要估计 $u$ 的时间和空间导数，但数值微分会放大噪声，因此导数计算及其诊断可视化是重要的前处理环节。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个未知系统的时空观测数据，例如场变量 $u(x,t)$ 在离散空间网格和时间点上的测量值，以及由这些数据生成的数值导数和诊断图像，任务是输出一个可执行、可验证的候选 PDE。候选方程应同时包含方程结构和待估计系数；系统通过数值拟合将候选方程与观测数据比较，并依据验证结果接受或拒绝候选。本文不要求真实方程属于预先固定的符号库，但默认观测数据包含足以辨识主要动力学的信息，并承认噪声、复杂几何和有限观测会影响发现可靠性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$u(x,t)$**

在空间位置 $x$ 和时间 $t$ 处观测到的系统状态或物理场。

</div>
<div class="notation-item" markdown="1">

**$\partial_t u$**

场 $u$ 对时间的偏导数，表示局部时间变化率。

</div>
<div class="notation-item" markdown="1">

**$\partial_{x}u$**

场 $u$ 对空间坐标 $x$ 的偏导数；在多维情形中可相应扩展为各空间方向的导数。

</div>
<div class="notation-item" markdown="1">

**$F(u,\nabla u,\nabla^2u,\ldots)$**

由场变量及其一阶、二阶或更高阶空间导数组成的未知动力学算子，表示待发现的 PDE 右端结构。

</div>

</div>

**直接相关的工作**

- **SINDy（Sparse Identification of Nonlinear Dynamics）**: SINDy 代表基于预定义候选项库的稀疏回归路线：它从候选函数项中选择少数项来构造动力学方程。本文针对该路线表达能力受候选库限制的问题，尝试让 Governing Law Synthesizer 在没有预定义符号库的情况下提出候选，再由数值验证约束候选。
- **SR-Scientist**: SR-Scientist 代表带有代码执行和迭代推理工具的智能体式方程发现方法。本文与其都强调提出、执行和修正方程的循环，但进一步将流程拆分为 Differential Observer、Phenomenology Extractor、Governing Law Synthesizer 和 Equation Arbiter 四个角色，并显式使用图像诊断与置信度门控的接受—拒绝协议。

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

MAGE 将偏微分方程（PDE）发现组织为“观测—假设—验证—拒绝或接受”的闭环。输入是带坐标或时间元数据的场观测数据 $\mathcal{D}=\{(\mathbf{z}^{(i)},\tilde{\mathbf{u}}^{(i)})\}_{i=1}^{N}$；系统先计算导数、频谱和几何等数值诊断，再由视觉语言模型提取物理现象线索，由大语言模型在不依赖预定义候选库的情况下提出多个候选方程，最后通过可执行代码、弱形式回归和留出数据验证候选。直观地说，MAGE 把“从数据猜公式”拆成了观察员、现象解释员、假设提出者和裁判四个角色，并要求猜出的公式经数值检验后才能被采纳。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 观测数据预处理与微分诊断

Differential Observer 对数据进行必要的噪声处理，并计算梯度、二阶导数、频谱、极值轨迹、等值线和其他诊断特征；规则网格可使用二维小波去噪，非结构化点云和带掩膜三维网格跳过去噪。该阶段是代码支持的确定性映射 $f_{\mathrm{feature}}:\mathcal{D}\mapsto\mathcal{Z}_{1}$。

<div class="method-step__io" markdown="1">

**输入**：原始场观测 $\mathcal{D}$、空间或时空坐标 $\mathbf{z}$、采样拓扑以及噪声水平 $\rho$（若适用）。<br>
**输出**：数值诊断集合 $\mathcal{Z}_{1}=\{\nabla u,\nabla^{2}u,\hat{u}(\omega),\mathrm{contours}(u)\}$，以及供后续模型查看的图像、元数据和统计特征。

</div>

**直观理解**：这一步像实验室里的测量员：不直接猜 PDE，而是先把数据中的变化方向、平滑程度、振荡频率和几何形状整理出来。这样可以避免语言模型只凭文字或图像表面印象猜方程。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多模态现象抽取

Phenomenology Extractor 使用视觉语言模型将图像证据和元数据转换为结构化 JSON 证据报告 $\mathcal{Z}_{2}=\{c_{j}\}_{j=1}^{M}$。其输出被限制为变量身份、数据几何、运动或输运线索、结构特征以及扩散、色散、源汇、变系数和不稳定性等可能机制，不允许直接命名 PDE 或生成符号表达式。

<div class="method-step__io" markdown="1">

**输入**：Agent 1 生成的可视化诊断 $\mathcal{V}\subseteq\mathcal{Z}_{1}$、数据元数据 $m$ 和固定提示模板 $\phi_{1}$。<br>
**输出**：语义物理先验 $\mathcal{Z}_{2}$，即对主导物理机制和候选算子类别的结构化描述。

</div>

**直观理解**：这一步像物理学家读实验图：它只回答“看起来发生了平流、扩散还是非线性输运”，而不抢先写出最终公式。限制输出格式是为了把观察证据与公式猜测分开。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 无候选库的方程假设生成

Governing Law Synthesizer 根据物理语义和数值数据生成 $K=10$ 个结构不同的候选方程 $\mathcal{Z}_{3}=\{\mathcal{F}_{k}\}_{k=1}^{K}$，候选可包含微分算子、非线性项和坐标依赖系数，但不从固定字典中选择。为保持探索，至多两个候选细化上一轮最佳假设，至少四个候选来自实质不同的结构族；系数估计被延后给 Equation Arbiter。

<div class="method-step__io" markdown="1">

**输入**：语义证据 $\mathcal{Z}_{2}$、数据子样本 $\mathcal{D}_{s}\subset\mathcal{D}$ 和提示模板 $\phi_{2}$。<br>
**输出**：带有方程编号、目标项、特征项和规范化 PDE 表达式的候选集合 $\{\mathcal{F}_{k}\}_{k=1}^{10}$。

</div>

**直观理解**：这一步像提出多个可证伪的科学假设，而不是只给一个答案。候选库不是预先写死的，因此模型可以组合训练者没有列出的算子，但多样性约束也防止十个候选都只是同一个公式的微小改写。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 弱形式回归、排序与闭环更新

Equation Arbiter 为每个候选生成可执行验证程序，将 PDE 项转换为弱形式支持积分，利用 $L_{2}$ 归一化普通最小二乘估计系数并计算留出残差；候选按带简洁性惩罚的测试得分排序。若最高候选的置信度达到 $80\%$，则接受；否则先把验证分数、诊断和拒绝候选反馈给 Synthesizer 进行细化，若细化预算耗尽，再重启现象抽取并保留当前最高分候选，最多进行文中规定的迭代次数。

<div class="method-step__io" markdown="1">

**输入**：候选方程 $\mathcal{F}_{k}$、完整数据 $\mathcal{D}$、固定的训练—测试划分以及候选对应的验证代码 $\mathcal{C}_{k}$。<br>
**输出**：估计系数 $\boldsymbol{\theta}_{k}^{\ast}$、损失或测试拟合结果、排序后的候选以及最终的接受方程或继续搜索信号。

</div>

**直观理解**：这一步像答辩委员会：每个公式都必须在未参与拟合的数据上表现良好，同时不能靠无必要的复杂项取胜。没有通过门槛时，系统不是盲目输出，而是利用失败原因重新提出假设。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### PDE 发现的最大似然目标

$$
(\mathcal{F}^{\ast},\boldsymbol{\theta}^{\ast})=\arg\max_{\mathcal{F}\in\mathcal{H},\boldsymbol{\theta}}p\left(\mathcal{D}\mid\mathcal{F},\boldsymbol{\theta}\right)
$$

**符号说明**

- $\mathcal{D}$：观测数据集合，由坐标或时空位置与观测场响应组成。
- $\mathcal{F}$：候选 PDE 的符号结构或显式 governing law。
- $\boldsymbol{\theta}$：PDE 中待估计的连续系数。
- $\mathcal{H}$：候选方程结构组成的组合假设空间。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标同时回答两个问题：应该选择什么形式的方程，以及这些项的系数是多少。直接在组合结构空间和连续系数空间上联合优化通常难以计算，因此 MAGE 用分阶段代理和后验验证来近似这一目标。<br>
**原文位置**：第 3.1 节，式（2）

</div>

</div>

<div class="equation-block" markdown="1">

#### 候选方程的弱形式回归

$$
y_{j}\approx\Theta_{j}\xi_{j}
$$

**符号说明**

- $y_{j}$：候选 $j$ 的目标项在各个有效局部支持上的弱形式积分所组成的向量。
- $\Theta_{j}$：候选 $j$ 的特征项弱形式积分组成的设计矩阵，每一列对应一个特征项。
- $\xi_{j}$：候选 $j$ 的待拟合系数向量。
- $j$：候选方程的索引。

<div class="equation-explanation" markdown="1">

**直观理解**：系统不必先对含噪观测逐点求高阶导数，而是在局部支持上把方程各项与测试函数积分。于是方程发现被转化为线性系数拟合：寻找能使特征项组合逼近目标项的系数，再用留出支持检验泛化。<br>
**原文位置**：第 3.3.1 节 Weak-Form Formulation，式（23）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文将该系统描述为推理时的代理分解与验证流程，而不是需要在本文中重新训练的端到端神经网络。全局目标仍对应最大化 $p(\mathcal{D}\mid\mathcal{F},\boldsymbol{\theta})$；实际执行中，Synthesizer 生成结构，Arbiter 通过最小二乘估计系数并以测试残差和简洁性排序，验证失败后将反馈用于下一轮候选生成。对候选 $j$，文中使用 $R_{j}=R^{2}_{\mathrm{test},j}\max(0,1-0.3\log_{10}N_{j})$ 排序，其中 $R^{2}_{\mathrm{test},j}$ 是测试集拟合度，$N_{j}$ 是候选项数量；最高候选的置信度达到 $80\%$ 才接受。该机制的优化重点是结构选择、系数估计和留出验证，而不是对 MAGE 本身进行梯度训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Differential Observer 与噪声证据层**

Agent 1 将原始观测转换为确定性的数值特征。规则二维网格使用 sym8 二维离散小波变换和 BayesShrink 对细节系数软阈值化，再重建去噪场；时间依赖场还可输出 $u$、$u_x$、$u_t$、功率谱、色散谱、谱能量演化和谱熵等诊断。

> 直观理解：PDE 发现高度依赖导数，而噪声会把导数放大，因此该模块先建立较稳定的证据底座。它并非消除所有误差；原文明确指出，确定性处理不能消除噪声观测中的导数估计误差。

**2. Phenomenology Extractor 与 Governing Law Synthesizer**

VLM 通过受限 JSON 把多模态诊断映射为物理机制描述，LLM 再从 $q_{3}(\mathcal{F}\mid\mathcal{Z}_{2},\mathcal{D}_{s},\phi_{2})$ 采样候选结构。两者的接口将“看到了什么物理现象”和“哪些符号方程可以解释它”分离，并使候选生成不依赖固定项库。

> 直观理解：前者负责把图像翻译成物理语言，后者负责把物理语言翻译成数学假设。分工的关键作用是降低直接让一个模型从原始数据跳到最终方程时的推理跨度。

**3. Equation Arbiter 与自主验证闭环**

Arbiter 为候选生成验证代码 $\mathcal{C}_{k}$，执行弱形式回归并计算系数与测试质量；候选得分采用测试拟合度和候选项数量的联合排序，置信度由测试 $R^{2}$ 转换而来。弱形式通过分部积分把数据导数转移到紧支撑测试函数上，从而减少直接有限差分对噪声的敏感性；点云则使用局部加权多项式拟合估计导数。

> 直观理解：裁判不接受语言模型对“这个方程合理”的口头解释，而是运行代码检验它能否重现数据。闭环的拒绝机制把失败变成下一轮搜索的反馈，因此 MAGE 是迭代验证系统而非一次性生成器。

**训练与推理**

完整推理从场数据和坐标元数据开始。Agent 1 计算诊断，Agent 2 输出受限 JSON 物理证据，Agent 3 生成十个候选结构，Agent 4 为每个候选生成并执行验证代码，使用弱形式支持积分构造回归系统，在确定性的 $80/20$ 训练—测试划分上进行 $L_{2}$ 归一化普通最小二乘拟合，并据测试表现排序。若候选达到置信度门槛，控制器返回其结构和系数；若未达到，拒绝整组候选，把候选、验证指标和诊断写入共享交互记忆，先执行合成器细化，必要时重启现象抽取以刷新语义先验。代码运行失败只触发验证代码重生成，不改变当前候选集合；细化或重启预算耗尽后，系统保留迄今最高分候选，但是否接受仍受置信度规则约束。

**复现信息**

为复现和公平解释结果，需区分三类数据拓扑：规则二维网格使用紧支撑弱形式积分，非结构化点云使用局部加权多项式最小二乘，带掩膜三维网格不得跨越无效值积分。弱形式支持以归一化局部坐标构造，测试函数采用可分离紧支撑多项式；所有候选复用相同的有效支持行交集和确定性训练—测试划分，训练设计矩阵列按 $\ell_{2}$ 范数归一化后拟合，再恢复物理单位。噪声实验中，规则网格可先用 sym8 小波去噪；复杂值场的实部和虚部分别处理，点云及掩膜三维网格则不使用小波去噪。候选生成阶段固定为每轮十个结构候选，并施加“至多两个细化旧最佳、至少四个来自不同结构族”的多样性约束；最终接受阈值为 $80\%$，且方法章节描述最多三次迭代。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Canonical PDE Benchmark Suite：由多个典型偏微分方程组成，用于检验方程结构恢复和系数估计；表 1 汇总了 7 个方程的结果，因为精确恢复率以 1/7 为步长呈现。原文未明确报告每个方程的数据规模、训练—测试划分和具体采样方式。
- Complex geometries：两个复杂几何场景，用于检验方法能否在几何结构更复杂时恢复预期算子。原文未明确报告数据规模、划分和噪声设置。
- Laboratory sensor record：一条实验室传感器记录，用于检验方法从真实观测数据中选择恢复力模型的能力。原文未明确报告记录规模、训练—测试划分和传感器类型。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Exact recovery**

精确恢复率，表示预测方程的符号结构与真实方程完全一致的比例。 （越高越好，因为它要求所有必要项、系数对应项和项的组合均正确。）

</div>
<div class="metric-item" markdown="1">

**Structural failure、missing terms（MT）和 extra terms（ET）**

结构性错误指标：failure 表示结构恢复失败，MT 表示遗漏真实项，ET 表示引入额外项；它们从不同角度刻画结构错误。 （failure、MT 和 ET 越低越好，因为较低数值意味着更少的结构遗漏、冗余或整体失败。）

</div>
<div class="metric-item" markdown="1">

**Normalized RMS coefficient error**

归一化均方根系数误差，用于衡量预测方程系数与真实系数之间的数值偏差，记作归一化的 $\bar{\varepsilon}$。 （越低越好，因为它表示估计系数更接近真实系数。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Canonical PDE Benchmark Suite：符号结构恢复

<div class="result-value" markdown="1">

MAGE 的精确结构恢复率为 $100.0\%$，failure rate 为 $0.0\%$；在比较方法中，L4E 为 $85.7\%$，EG 为 $71.4\%$，PF 和 WI 均为 $42.9\%$。这些数值来自表 1 的 Aggregate summary。

</div>

这说明在该基准套件及其统一评测协议下，MAGE 对 7 个测试方程都恢复了完整结构，而其他方法至少在部分方程上遗漏或添加了项。它支持 MAGE 在该实验范围内的结构发现能力，但不能证明其对未见过的方程族、不同采样密度或更强噪声具有普遍优势。

<div class="result-source" markdown="1">

来源：Table 1, Aggregate summary

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Exact (%)
PF
SGA
WS
WI
PSR
PR
L4E
EG
MAGE
42.9
14.3
28.6
42.9
0.0
0.0
85.7
71.4
100.0

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Canonical PDE Benchmark Suite：系数估计误差

<div class="result-value" markdown="1">

MAGE 的归一化均方根系数误差为 $7.96\mathrm{e}{-7}$，是表中方法的最低值；原文摘要进一步声称，MAGE 在 8 个系统中的 7 个取得最低系数误差，最高改善达到 4 个数量级，几何平均改善约 3 个数量级。

</div>

结构正确并不等于参数准确；该结果表明 MAGE 在恢复项结构之外，也能较精确地估计项系数。由于表 1 的汇总误差与摘要使用了不同的系统计数表述，且所给摘录没有逐方程误差明细，因此“7/8”和改善倍数仍需结合完整论文逐项核查，不能仅凭汇总值判断每个方程上的优势。

<div class="result-source" markdown="1">

来源：Table 1, Aggregate summary

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ε
¯
$\overline{\varepsilon}$
5.04e-2
4.70e-2
2.18e-2
8.90e-4
2.49e2
4.49e4
3.13e-2
6.93e-2
7.96e-7

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 复杂几何与实验室传感器记录

<div class="result-value" markdown="1">

作者报告 MAGE 在两个复杂几何中恢复了预期算子，并在一条实验室传感器记录上选择了三次恢复力模型；该模型在留出数据上的 $R^2$ 为 $0.98538$。

</div>

这些结果把测试从标准基准推进到几何更复杂和更接近实验的数据，说明方法不仅能处理规则基准中的符号表达式，也可能从真实观测中选择合理的动力学形式。但两个复杂几何的定量指标、传感器记录的样本规模以及与替代模型的比较在摘录中未给出，因此这更像是可行性证据，而不是充分的泛化验证。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The pipeline also recovers the expected operators in two complex geometries and, on one laboratory sensor record, selects a cubic restoring-force model with held-out $R^2=0.98538$.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评测范围仍然有限：作者明确指出，更广泛的泛化能力尚待评估；当前摘录仅包含典型 PDE、两个复杂几何和一条实验室传感器记录，不能代表多种物理系统、采样条件和噪声水平。
- 基于候选库的基线获得了包含全部真实项的统一候选库，而 MAGE 强调无需预定义候选库；这种设置有助于比较库内组合与估计难度，但没有完全解决不同方法在候选空间定义上的不对称问题。此外，摘录提到有针对性的组件消融，却未提供消融结果，因此无法从现有证据确认四类代理各自的必要性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- PF：经典稀疏回归方法，用于比较在共享候选库中筛选偏微分方程项的能力。
- SGA：经典稀疏回归基线，用于检验不同稀疏估计策略的结构恢复与系数稳定性。
- WS：经典稀疏回归基线，用于比较其在非线性和色散方程上的候选项组合能力。
- WI：经典稀疏回归基线；它与其他基于候选库的方法共同获得了包含所有真实项的统一候选库，因此比较重点是库内组合与参数估计，而不是候选项覆盖范围。

**实验想回答的问题**

- 在标准典型偏微分方程基准上，MAGE 能否同时恢复正确的方程结构并准确估计系数，而不依赖预定义候选库？
- MAGE 的验证循环能否扩展到复杂几何、加性噪声和实验传感器记录等非理想数据情形？

**实验实现**

MAGE 按照“观察—假设—验证”的循环运行：用户或系统控制器先将微分诊断结果传给 Differential Observer，再将多模态诊断证据传给 Phenomenology Extractor，随后由 Governing Law Synthesizer 生成候选方程，最后由 Equation Arbiter 执行系数拟合和数值验证。候选方程只有在其置信度超过用户指定阈值时才被接受，否则进入下一轮迭代。典型 PDE 实验中的所有基于候选库的基线都使用包含全部真实项的统一候选库，因此该比较并未测试基线能否发现候选库之外的新算子。原文未明确报告 MAGE 的具体模型版本、随机种子、硬件、完整超参数、数据规模或训练—测试划分。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 实验室传感器记录是最具体的应用案例：MAGE 从观测记录中选择了三次恢复力模型，并在留出数据上获得 $R^2=0.98538$。这表明框架能够把实验信号转化为可验证的候选动力学规律；但由于摘录没有报告候选模型集合、基线模型或置信度阈值，不能据此断言该模型在物理解释性或模型选择上优于其他方案。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文以多个角色特化的 VLM/LLM 智能体协作构建假设、验证方程并迭代发现 PDE，核心同时涉及多智能体协作与结构化推理。; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`06c08845b7852b66abf278147b8c3a451c09463c8fcb7762b42cfdc8f7ca9ec8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
