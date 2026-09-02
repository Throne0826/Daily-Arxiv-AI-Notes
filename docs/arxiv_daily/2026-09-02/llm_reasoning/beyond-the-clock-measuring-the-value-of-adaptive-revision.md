---
title: "[论文解读] Beyond the Clock: Measuring the Value of Adaptive Revision"
description: "[arXiv 2609.00874][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2609.00874"
announcement_date: "2026-09-02"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:53:16.740679+00:00"
source_sha256: "cc57452a4f8f1c5da282449f6602ce6d5ee051bf02d23ac3910c7ca7aa78ec64"
tags:
  - "LLM Reasoning"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.00874</p>

# Beyond the Clock: Measuring the Value of Adaptive Revision

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Ayushi Chadha</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00874v1) · [PDF 下载](https://arxiv.org/pdf/2609.00874v1) · **关键词** LLM Reasoning<br>


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

本文位于复合人工智能系统与元级控制研究的交叉领域。复合系统不仅执行具体任务，还包含一个更高层控制过程，用来决定是否保留或修改指导下层计算的提示、轨迹、程序、子目标、记忆状态或代理运行框架。本文聚焦其中一个可直接测量的决策：层级潜在推理器的管理器在观察当前计算过程后，是继续保留当前承诺，还是替换该承诺；研究重点不是单纯提高任务准确率，而是判断状态相关的修订决策是否真正带来超越强固定时序策略的任务收益。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**复合人工智能系统**

复合人工智能系统由多个相互配合的过程组成，通常包括执行任务的下层模块和调度、评估或修改下层行为的上层模块。本文关心的是上层模块如何为下层计算分配有限的修订机会。

</div>
<div class="concept-item" markdown="1">

**元级控制**

元级控制是对“如何执行任务”的过程进行控制，而不是直接完成任务本身。在本文中，控制动作是管理器决定保留当前指导下层计算的承诺，或在后续计算中替换它。

</div>
<div class="concept-item" markdown="1">

**层级潜在推理器**

层级潜在推理器把推理分为较慢的管理器和较快的工作器：管理器产生一种不直接呈现为自然语言的方向性潜在承诺，工作器据此进行多轮细化。这样可以研究上层决策如何影响连续的下层计算。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文采用源自 Hierarchical Reasoning Model 的紧凑层级潜在推理器作为实验环境。管理器在每个可决策的计算轮次观察当前状态，并对正在指导工作器的承诺执行二选一操作：$\mathrm{PERSIST}$，继续保留该承诺；或 $\mathrm{REPLAN}$，替换承诺并让后续下层计算沿新的方向进行。输入因此包括当前内部状态、活动承诺和剩余的固定计算预算；输出是各次可决策位置上的保留或替换序列，以及该序列对应的最终任务结果。研究假设决策预算有限、干预位置和次数可枚举，并在相同冻结模型检查点上比较学习得到的状态相关策略与强制采用固定时序的策略。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$m$**

较慢的管理器（manager），负责产生或替换指导下层计算的潜在承诺。

</div>
<div class="notation-item" markdown="1">

**$w$**

较快的工作器（worker），在管理器承诺的引导下执行多轮推理细化。

</div>
<div class="notation-item" markdown="1">

**$c_t$**

第 $t$ 个计算轮次期间生效的方向性潜在承诺；它决定工作器后续计算所遵循的方向。

</div>
<div class="notation-item" markdown="1">

**$a_t\in\{\mathrm{PERSIST},\mathrm{REPLAN}\}$**

第 $t$ 个可决策位置的元级动作：$\mathrm{PERSIST}$ 表示保留当前承诺，$\mathrm{REPLAN}$ 表示替换当前承诺。

</div>

</div>

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

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

该方法把层级潜变量推理器视为一个可精确干预的“管理者—工作者”系统。模型执行固定的 $M=8$ 次外层推理：工作者利用当前承诺更新高、低层隐藏状态，管理者随后观察更新后的状态，决定保留承诺还是生成新承诺。承诺由方向目标、注入强度和锚点组成，用于引导后续工作者表示沿指定方向变化；因此，管理者在第 $m$ 次之后作出的替换决定只能从第 $m+1$ 次开始生效。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 工作者执行当前承诺

在第 $m$ 次外层推理中，工作者先消费先前缓存的承诺，再更新高、低层隐藏序列；其汇总表示为 $w_m=T^{-1}\sum_t z_{m,t}^L$。

<div class="method-step__io" markdown="1">

**输入**：任务输入、当前高层状态 $z_m^H$、低层状态 $z_m^L$，以及循环缓存中的目标、门控强度和锚点。<br>
**输出**：更新后的隐藏状态、工作者汇总表示 $w_m$，以及供管理者观察的高层表示 $h_m=z_m^H[:,0]$。

</div>

**直观理解**：工作者像执行当前计划的解题者：它必须先按旧计划完成这一轮，管理者不能在本轮结束后再反过来改变已经发生的计算。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造并维持方向承诺

管理者将 $h_m$ 映射为归一化方向目标 $\tilde g_m$ 和标量门控 $\alpha_m$，再投影回共享隐藏空间并注入后续更新；承诺发出时保存当轮工作者表示作为锚点 $a=w_s$。

<div class="method-step__io" markdown="1">

**输入**：管理者观察到的后验高层表示 $h_m$。<br>
**输出**：可跨多轮持续使用的目标 $g_m$、门控 $\alpha_m$ 和锚点 $a_m$。

</div>

**直观理解**：方向目标说明内部表示应朝哪里移动，门控说明推动力度，锚点则记录计划开始时的位置；三者共同定义一项可持续、也可被替换的内部计划。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算状态条件触发信号

模型构造六维且停止梯度的摘要 $\phi_m=[c_m,d_m,\rho_m,\tau_m/M,q_m,\alpha_m]^\top$，并通过仿射逻辑回归得到替换概率 $\beta_m$。

<div class="method-step__io" markdown="1">

**输入**：当前与历史工作者表示、活动目标、锚点、承诺持续时间、停止置信信号和门控强度。<br>
**输出**：训练时的伯努利动作 $u_m$，或推理时经阈值 $\theta$ 得到的确定性保留/替换决定。

</div>

**直观理解**：触发器不读取完整隐藏状态，而只查看“累计进展、最近进展、趋势、计划已持续多久、是否应继续以及当前推动强度”等仪表盘信号。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行替换并分配局部信用

若决定替换，则新承诺在第 $m+1$ 次工作者推理中首次被消费；训练时使用值保持的局部雅可比重建，使前向计算仍消费缓存值，而梯度仅从首个消费轮传回重新计算的承诺。

<div class="method-step__io" markdown="1">

**输入**：动作 $u_m$、旧缓存承诺，以及由当前状态重新计算的新承诺。<br>
**输出**：更新后的循环缓存，以及对管理者目标、门控和保留/替换选择的单个消费轮信用信号。

</div>

**直观理解**：这相当于保持实际执行记录不变，但在反向学习时给刚作出的计划决定接上一条短梯度通道；它避免跨完整未来轨迹保存计算图。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 方向承诺的辅助目标

$$
\ell_m^F=A_m\alpha_m\left[1-\cos\!\left(w_m-a_m,g_m\right)\right]
$$

**符号说明**

- $\ell_m^F$：第 m 次外层推理的方向一致性辅助损失。
- $A_m$：因果有效性掩码；尚未有承诺被工作者消费时屏蔽该损失。
- $\alpha_m$：当前承诺的标量门控强度。
- $w_m$：第 m 次外层推理后的工作者汇总表示。
- $a_m$：当前承诺发出时保存的工作者表示锚点。
- $g_m$：当前活动承诺指定的方向目标。
- $\cos(\cdot,\cdot)$：衡量两个向量方向一致性的余弦相似度。

<div class="equation-explanation" markdown="1">

**直观理解**：该损失要求工作者相对锚点的累计位移 $w_m-a_m$ 与管理者给出的方向 $g_m$ 对齐；方向越一致，损失越小。掩码保证只有承诺真正被后续计算消费后才计入损失，门控则调节该目标的作用强度。<br>
**原文位置**：第 2.1 节，公式 (3)

</div>

</div>

<div class="equation-block" markdown="1">

#### 状态条件触发策略与单消费轮信用重建

$$
\begin{aligned}
\phi_m&=[c_m,d_m,\rho_m,\tau_m/M,q_m,\alpha_m]^{\top},\\
\beta_m&=\sigma(w_\beta^{\top}\phi_m+b_\beta),\qquad u_m\sim\operatorname{Bernoulli}(\beta_m),\\
v_{\mathrm{used}}&=v_{\mathrm{cached}}+I_{\mathrm{pending}}\left(v_{\mathrm{recomputed}}-\operatorname{stopgrad}(v_{\mathrm{recomputed}})\right).
\end{aligned}
$$

**符号说明**

- $\phi_m$：第 m 次推理后供触发器使用的六维、已停止梯度的状态摘要。
- $c_m$：工作者相对锚点沿当前目标方向的累计进展。
- $d_m$：最近一次工作者更新沿当前目标方向的进展。
- $\rho_m$：累计方向进展的变化趋势，定义为 $c_m-c_{m-1}$。
- $\tau_m/M$：当前承诺的归一化驻留时间。
- $q_m$：有界的停止相对继续置信信号。
- $\alpha_m$：当前活动承诺的门控强度。
- $w_\beta$：触发器对六维摘要的可学习权重。
- $b_\beta$：触发器的可学习偏置。
- $\beta_m$：第 m 次推理后替换当前承诺的概率。
- $u_m$：二元替换动作；1 表示替换，0 表示保留。
- $v_{\mathrm{used}}$：工作者在首个消费轮实际使用、同时带有局部梯度路径的承诺量。
- $v_{\mathrm{cached}}$：循环缓存中以分离梯度形式保存的承诺量。
- $v_{\mathrm{recomputed}}$：为恢复局部梯度而根据相关状态重新计算的同一承诺量。
- $I_{\mathrm{pending}}$：指示当前是否为新承诺首个消费轮的指示变量。
- $\operatorname{stopgrad}$：前向保留数值、反向阻断梯度的操作。

<div class="equation-explanation" markdown="1">

**直观理解**：前两行把进展、趋势和驻留时间等信息压缩成替换概率，并在训练时采样动作。最后一行所加括号项在前向传播中的数值严格为零，因此不会改变实际缓存承诺；反向传播时，停止梯度造成的不对称会把首个消费轮的学习信号传给重新计算的承诺。<br>
**原文位置**：第 2.3 节公式 (4)–(5)；第 2.4 节公式 (6)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文明确给出了方向辅助损失 $\ell_m^F$，用于使工作者表示相对锚点的位移与管理者目标一致，并通过 $A_m$ 排除尚未发生因果消费的轮次。所给章节没有明确写出包含最终任务损失、方向辅助损失和触发策略学习项的完整加权总目标，因此不能据此断言各项的权重或优化组合；可确认的是，目标、门控以及自适应保留/替换选择通过首个消费轮的局部信用路径获得梯度。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 管理者—工作者层级推理器**

慢速管理者依据每轮结束后的 $h_m$ 生成潜在方向承诺，快速工作者在后续轮次中消费该承诺并细化任务表示。承诺一直保留到下一次管理者干预，其持续轮数称为驻留时间。

> 直观理解：管理者负责定方向，工作者负责连续执行；论文关注的不是是否需要层级结构，而是何时继续旧方向、何时改换方向。

**2. 状态条件修订触发器**

触发器是以六维摘要 $\phi_m$ 为输入的伯努利策略。所有摘要特征在进入触发器前均被分离梯度，从而使触发器读取状态证据，但不通过这些输入反向重塑底层表示。

> 直观理解：它把固定时钟式改计划改成看状态再决定，同时通过停止梯度减少触发器为了让自己更容易决策而扭曲底层推理状态的可能。

**3. 因果时序与单消费轮信用**

每轮严格遵循“消费旧承诺—更新隐藏状态—管理者决策”的顺序，因此第 $m$ 轮后的决策只能影响第 $m+1$ 轮。局部雅可比重建只让首个消费轮向该决策提供梯度，而不进行贯穿全部剩余推理轮次的反向传播。

> 直观理解：该模块保证训练时的因果方向与实际执行一致，但代价是管理者主要依据紧邻下一轮的效果学习，未必直接优化更远处的最终任务收益。

**训练与推理**

训练时，模型先完成第 $1$ 次引导推理并强制发出初始承诺；可选修订仅允许发生在第 $2$ 至第 $7$ 次之后，第 $8$ 次之后不再发出承诺，因为已无后续工作者计算可以消费它。触发器依据分离梯度后的 $\phi_m$ 计算 $\beta_m$，再采样 $u_m\sim\operatorname{Bernoulli}(\beta_m)$；若替换，新承诺从下一轮生效，并仅从该首个消费轮通过值保持的局部雅可比获得信用。

确定性推理不再采样，而采用 $u_m=\mathbb{1}[\beta_m>\theta]$。固定时钟对照则令动作只依赖轮次，即 $u_m=f(m)$；在恰有 $K=2$ 次发出、且第一次固定在第 $1$ 次之后时，候选日程为 $[1,k]$，其中 $k\in\{2,3,4,5,6,7\}$，从而在相同干预算下比较不同承诺驻留长度。

**复现信息**

公平解释该方法必须保留其严格时序：管理者在工作者完成第 $m$ 次更新后才决策，决定绝不能影响同一轮。所有主要实验固定 $M=8$；缓存的目标、门控和锚点均以分离梯度值保存，局部信用重建应用于目标、门控及自适应选择。原文未在所给章节中明确报告阈值 $\theta$ 的具体取值、完整优化器配置或各损失权重。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ConceptARC-mini：所有主要实验使用的抽象推理任务集。最终评估包含按固定顺序排列的 $3,686$ 个回合；阈值校准另用与最终集不相交的 $921$ 个回合。其作用是同时评估任务正确性、控制器产生的承诺次数及不同干预时序的因果效果。原文未明确报告训练集规模或任务类别构成。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**回合平均词元准确率**

先在每个回合内计算输出词元的正确比例，再对回合取平均；用于三种子自适应审计、匹配预算训练比较和冻结强制时序比较。 （越高越好，因为它表示平均每个任务回合中有更多输出词元正确。）

</div>
<div class="metric-item" markdown="1">

**微平均词元准确率**

把所有评估回合的正确词元数汇总后除以总词元数，是六时序穷举、随机策略、预言机及顺序比较的预注册主指标；不能与回合平均词元准确率直接混用。 （越高越好，因为它表示整个评估语料中正确词元所占比例更高。）

</div>
<div class="metric-item" markdown="1">

**平均承诺次数 $\bar K$**

每个回合实际发出承诺的平均数量，用于校准并核验自适应控制器是否与固定策略共享约 $K=2$ 的干预算；该指标本身不衡量任务质量。 （不是单调越高或越低越好；本实验要求它尽量接近目标值 $2$，从而避免把更多干预次数误当成更优时序。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三个预先指定种子的自适应控制器，与各自在同一冻结检查点上表现最好的强制固定时序比较。

<div class="result-value" markdown="1">

自适应策略在三个种子上均未超过最佳强制时序：种子 $0$ 为 $0.467015$ 对 $0.487511$，差 $-2.0496$ 个百分点；种子 $1$ 为 $0.486149$ 对 $0.489535$，差 $-0.3386$ 个百分点；种子 $2$ 为 $0.474947$ 对 $0.475515$，差 $-0.0568$ 个百分点。

</div>

作者的直接结论是，学习到的修订时机没有在三个复现实验中产生超越强固定时序的任务收益。由于比较在同一冻结检查点内完成，这一差距主要归因于时序决策，而不是模型容量或重新训练差异。不过，该结果只说明当前训练方法、数据和 $K=2$ 预算下未实现增益，不能证明所有状态依赖控制在原则上都无价值。

<div class="result-source" markdown="1">

来源：Appendix B, Table 2: Three-seed adaptive audit and frozen-checkpoint forced controls

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

0 | 2.0008 | 0.467015 | [1,4] | 0.487511 | −2.0496
1 | 1.9674 | 0.486149 | [1,6] | 0.489535 | −0.3386
2 | 1.9135 | 0.474947 | [1,2] | 0.475515 | −0.0568

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 种子 $0$ 的冻结检查点上，穷举全部六种 $K=2$ 固定时序，并比较最佳固定策略、均匀随机策略和逐回合预言机。

<div class="result-value" markdown="1">

最佳固定时序 $[1,5]$ 的微平均词元准确率为 $0.52121$，均匀随机时序为 $0.51791$，逐回合预言机为 $0.52256$；预言机相对最佳固定时序仅提高 $0.00135$。

</div>

作者据此认为，在该检查点和决策预算下，一个强固定时序已经获得绝大多数可测量的时序价值。分析上，预言机只多出 $0.00135$，说明即使允许事后逐回合挑选最优时序，可开发的剩余空间也很小；但这是候选集合内的经验上界，不排除更丰富的动作、不同预算或更好的状态表示带来更大收益。

<div class="result-source" markdown="1">

来源：Appendix B, Table 3: Headline quantitative checks

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

K = 2 sweep | best fixed [1,5] micro acc. | 0.52121
K = 2 sweep | uniform-random micro acc. | 0.51791
K = 2 sweep | oracle micro acc. | 0.52256
K = 2 sweep | oracle headroom over best fixed | 0.00135

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 预注册的反向驻留顺序比较：对驻留长度相同但先后顺序相反的时序对，计算“较长驻留在前”减“较短驻留在前”的微平均词元准确率。

<div class="result-value" markdown="1">

$[1,7]-[1,2]$ 的差为 $0.00924$，$95\%$ 配对 bootstrap 区间为 $[0.00847,0.01006]$；$[1,6]-[1,3]$ 为 $0.00405$，区间 $[0.00346,0.00472]$；$[1,5]-[1,4]$ 为 $0.00097$，区间 $[0.00075,0.00123]$。三组差异均为正。

</div>

这表明时机并非无关变量：即便两种承诺的总驻留长度相同，仅交换先后顺序也会改变结果，而且报告的区间均未跨越零。更直白地说，模型在早期长期保留第一次承诺，与早期迅速替换后长期保留第二次承诺，并不等价。但该实验只建立顺序敏感性，不能单独证明学习控制器能够识别应采用哪种顺序的具体回合。

<div class="result-source" markdown="1">

来源：Appendix B, Table 4: Preregistered reversed-order comparisons

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

[1,7] − [1,2] | 0.00924 | [0.00847, 0.01006]
[1,6] − [1,3] | 0.00405 | [0.00346, 0.00472]
[1,5] − [1,4] | 0.00097 | [0.00075, 0.00123]

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 深度机制分析、六时序穷举、预言机和反事实诊断仅在种子 $0$ 上完成；三个种子都接受了匹配预算审计和冻结强制时序比较，但关于剩余预言机空间及具体机制的结论仍需更多种子验证。
- 实验仅使用 ConceptARC-mini、固定 $M=8$ 和 $K=2$ 的紧凑设置，且完整序列准确率为零；因此结论主要适用于词元级表现与有限时序候选，不能直接外推到更大模型、其他任务、可变计算预算或更丰富的元控制动作。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 固定周期训练基线：周期 $P\in\{1,3,4,6,\infty\}$，每个周期使用种子 $\{0,1,2\}$，共 $15$ 次训练，每次 $400$ 个优化步骤。它检验固定时钟控制在不同随机种子下的表现；其中 $P=4$ 与 $P=6$ 都恰好产生 $K=2$ 次承诺，因此可在干预次数相同的条件下比较时机。
- 冻结检查点上的强制时序：冻结自适应模型的全部参数，只把第二次承诺强制放在 $[1,k]$ 的位置。它比重新训练固定模型更严格，因为学习到的推理器、管理器及权重完全相同，变化仅来自监督干预时机。
- 六种固定时序的穷举与均匀随机时序：在 $M=8$、$K=2$ 下评估全部六个合法的 $[1,k]$ 时序，并与从这些时序中均匀随机选择的策略比较，用于确定强非自适应策略能够取得的上界水平。
- 逐回合预言机：对每个回合事后选择六种固定时序中结果最好的一个。它不是可部署策略，而是估计在既定检查点、候选时序和 $K=2$ 决策预算下，完美按状态分配时序最多还能带来多少结果增益。

**实验想回答的问题**

- 在外层推理次数固定为 $M=8$、每回合承诺次数约束为 $K=2$ 时，依据内部状态学习何时替换承诺的自适应控制器，能否稳定优于同一冻结检查点上的最佳固定时序策略？
- 干预时机本身是否会因承诺顺序与驻留长度而影响结果，以及逐样本选择时序的理想预言机相对最佳固定时序还剩多少可利用空间？

**实验实现**

主要实验统一使用 $M=8$ 个外层推理轮次，使时序变化只改变承诺被替换的时间，而不改变外层计算量。固定周期矩阵与自适应控制器均训练 $400$ 个优化步骤，并预先指定三个随机种子。自适应训练不施加显式干预惩罚，即 $\eta=0$；随后仅根据校准集上的平均承诺次数选择阈值 $\theta^*$，不使用准确率、损失或最终集标签。选定阈值后冻结，在独立最终集上只评估一次。

冻结干预实验保留自适应模型的全部参数和正常因果轨迹，只覆盖第二次承诺的位置；到达强制位置时，仍使用管理器根据当时状态生成的目标。种子 $0$ 进一步穷举 $M=8$、$K=2$ 下全部六种合法时序。时序与预言机比较采用对同一批回合进行配对重采样的 $10,000$ 次 bootstrap，区间为百分位置信区间。完整序列准确率在该紧凑设置中为零，因而未用于时序比较；早期 $96$ 步实验仅验证梯度流、因果执行和阈值机制，不支持主要性能结论。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 固定训练基线中的匹配次数对照：比较都产生恰好 $K=2$ 次承诺、但第二次承诺位置不同的 $P=4$ 与 $P=6$。 | $P=6$ 在三个种子上都超过 $P=4$，平均留出集词元准确率差为 $0.00248$。 | 该对照固定了承诺次数，只改变第二次干预出现的时间，因此隔离出时机效应，而非“多干预一次”的收益。差值较小，且跨种子差异大于周期差异，所以它支持时机可能重要，却不足以确定一个跨种子普适的最佳周期。 | Section 3.2, Why K = 2 is the controlled budget<br><span class="experiment-evidence">P=6 exceeds P=4 on all three seeds, with a mean held-out token-accuracy difference of 0.00248.</span> |
| 泄漏隔离的预算校准：阈值只按校准集平均承诺次数选择，然后冻结并转移到独立最终集。 | 所选阈值 $\theta^*=0.498200$ 在校准集得到 $\bar K_{\mathrm{cal}}=2.000000$，在 $3,686$ 回合最终集得到 $\bar K_{\mathrm{final}}=2.000814$。 | 该检查验证自适应策略与固定时序的干预预算确实近似匹配，并排除利用准确率挑阈值的性能泄漏。它并不证明阈值分数是“重新规划有益概率”的良好估计，也不证明预算匹配后自适应选择本身有效。 | Section 3.3, Leakage-free budget calibration<br><span class="experiment-evidence">The chosen θ∗=0.498200 gives K̄cal=2.000000 and, once frozen, K̄final=2.000814 on the ordered 3,686-episode final split.</span> |

**定性案例**

- 种子 $0$ 展示了“看似状态依赖但行为近似固定时钟”的典型失败模式：最终平均承诺数为 $2.0008$，却有 $99.19\%$ 的回合选择 $[1,2]$，且控制分数 $\beta$ 的方差有 $96.76\%$ 可由决策位置解释。作者据此提醒，分数非恒定或可预测并不等于控制器能在同一位置上区分哪些回合应保留、哪些应重规划；其变化可能主要编码时间位置。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该工作研究层级推理系统中何时保留或修订推理策略的元级控制，以及自适应修订相对于固定调度的决策价值。; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`cc57452a4f8f1c5da282449f6602ce6d5ee051bf02d23ac3910c7ca7aa78ec64`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
