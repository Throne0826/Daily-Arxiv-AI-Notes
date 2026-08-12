---
title: "[论文解读] Optimal Stopping of Self-Refining Foundation Models"
description: "[arXiv 2608.10729][LLM Reasoning] 本文将基础模型基于验证反馈反复修改输出的过程建模为最优停止问题，以预期质量增益与每次调用成本的权衡来决定何时停止自我改进。"
arxiv_id: "2608.10729"
announcement_date: "2026-08-12"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-12T03:09:12.103915+00:00"
source_sha256: "153390d4d0360e2825cbce6b8893829a50ed9ad82eb8a3c8a068bb0e2bd75ac1"
tags:
  - "LLM Reasoning"
  - "LLM 效率"
  - "基础模型"
  - "自我精炼"
  - "外部验证反馈"
  - "上下文学习"
  - "最优停止"
  - "停止策略"
  - "马尔可夫性质"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.10729</p>

# Optimal Stopping of Self-Refining Foundation Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-12</span>
<span><strong>作者</strong> Kim Hammar, Tansu Alpcan, Emil C. Lupu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> T. Alpcan is with the University of Melbourne, Australia；K. Hammar and E.C. Lupu are with Imperial College London, United Kingdom</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.10729v1) · [PDF 下载](https://arxiv.org/pdf/2608.10729v1) · **关键词** 基础模型, 自我精炼, 外部验证反馈, 上下文学习, 最优停止, 停止策略, 马尔可夫性质<br>


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

本文将基础模型基于验证反馈反复修改输出的过程建模为最优停止问题，以预期质量增益与每次调用成本的权衡来决定何时停止自我改进。

**不用术语来说**：基础模型收到测试、约束检查或其他验证器的反馈后，往往可以再次修改答案，但修改次数并非越多越好：继续调用模型会消耗算力或产生服务费用，而且后续修改带来的改善可能逐渐变小，甚至不值得其成本。因此，实际系统需要根据当前输出的验证得分，动态判断是接受现有结果，还是再进行一次修改。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出一个决策论形式化，将自我改进中的迭代次数选择转化为序贯最优停止问题，使停止决策明确取决于预期改进与模型调用成本的比较。
- 作者建立最优阈值型停止策略成立的条件，并在三个前沿模型的代码基准上验证该策略；作者声称其成本效率优于已有的启发式停止方法。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

基础模型是以大规模数据训练的神经网络，可在不更新参数的情况下依据当前输入完成不同任务。本文关注其中的“自我精炼”：模型先生成候选输出，外部验证器再依据约束给出反馈或分数，模型将任务、原输出和反馈一并放入上下文以生成修订版本。由于每轮调用都会消耗算力或产生服务费用，系统不能只追求更多迭代，而需在输出质量的预期提升与继续调用的成本之间权衡；本文因此将是否继续精炼建模为有限时域、离散时间、连续状态且满足马尔可夫性质的最优停止问题。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**上下文学习（in-context learning）**

模型根据提示中提供的任务描述、示例或反馈调整本次生成行为，而不更新其参数。本文利用这一能力，让模型读取上一轮输出及验证反馈并生成修订结果。

</div>
<div class="concept-item" markdown="1">

**自我精炼（self-refinement）**

模型在迭代回路中反复执行“生成、验证、接收反馈、修订”，以逐步改善输出。这里的“自我”指同一基础模型负责修订，但反馈可由外部自动验证程序提供。

</div>
<div class="concept-item" markdown="1">

**最优停止（optimal stopping）**

最优停止研究在逐步观察系统状态时，何时停止才能使预期收益减去成本后的目标最优。在本文中，每轮都要选择接受当前输出，或支付一次额外调用成本以争取更好的结果。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定任务输入 $v$ 和参数固定的基础模型，模型首先从条件分布 $p_{\theta}(z\mid v)$ 生成输出 $z$；验证器依据任务约束检查该输出，并产生反馈 $x$ 或相应分数。若继续，模型从 $p_{\theta}(z'\mid v,z,x)$ 采样修订输出 $z'$，之后再次验证并重复这一过程。每个离散迭代时刻，停止策略 $\mu$ 根据当前可观测分数决定“停止并接受当前输出”或“继续修订”；问题是在有限迭代时域内，考虑每次本地计算开销或外部服务费用，选择使预期改进相对于调用成本最优的停止时刻。论文进一步假设用于决策的状态具有马尔可夫性质，即给定当前状态后，下一轮状态的分布不再依赖更早的完整历史。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$p_{\theta}(z\mid v)$**

参数为 $\theta$ 的基础模型在任务输入 $v$ 下生成输出 $z$ 的条件分布。

</div>
<div class="notation-item" markdown="1">

**$p_{\theta}(z'\mid v,z,x)$**

模型在给定任务 $v$、当前输出 $z$ 和验证反馈 $x$ 后生成修订输出 $z'$ 的条件分布。

</div>
<div class="notation-item" markdown="1">

**$\theta$**

基础模型的参数；上下文学习和自我精炼期间不对其进行更新。

</div>
<div class="notation-item" markdown="1">

**$\mu$**

停止策略，根据当前验证分数或状态选择停止并接受输出，或继续进行下一轮修订。

</div>

</div>

**直接相关的工作**

- **Madaan et al. [22]**: 该工作较早展示了基础模型可依据任务、已有输出和外部反馈生成修订结果，为本文研究的自我精炼循环提供了直接技术前提；本文关注的新增问题是如何从决策理论上确定停止修订的时机。
- **Wald [39]、Shiryaev [32] 与 Chow et al. [7] 的经典最优停止理论**: 这些工作提供了在随机序列决策中权衡继续观察成本与停止收益的理论基础。作者声称本文首次将该理论用于分析基础模型的自我精炼，并具体研究有限时域、离散时间、连续状态和马尔可夫设定。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在软件开发等自动化流程中，基础模型可形成“生成、验证、反馈、再生成”的循环。每轮调用都可能提高输出质量，但本地部署需要计算资源，外部服务则产生货币费用；在每天可能调用数千次的大规模流水线中，不必要的修改会累积成显著成本，而过早停止又可能放弃可获得的质量提升。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **固定迭代次数**：系统预先规定统一的修改轮数；模型生成初始输出后，无论当前质量、验证得分和下一轮可能收益如何，都执行到指定轮数再停止。
- **预设启发式停止准则**：系统依据人工设定的条件决定是否终止，例如在某个预定状态下接受当前输出。这类方法能够利用部分运行时信息，但其规则并非从质量收益与调用成本的统一优化目标中推导出来。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有研究主要通过代码和逻辑推理等任务进行经验评估，缺少对停止决策的正式分析，因此难以说明给定当前验证结果时，继续修改是否在期望意义上值得。
- 固定轮数或启发式规则没有系统地权衡边际改进与调用成本，后果可能是对已足够好的输出继续付费修改，或在仍有较高改善潜力时过早停止，因而无法保证成本效率。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有自我改进研究已证明外部反馈可以帮助基础模型修正输出，但尚缺少一个可计算的决策论框架，将当前验证得分、后续输出的随机变化以及单轮调用成本联系起来，并据此刻画何种停止策略是最优的；同时，人们对最优策略何时可简化为易于部署的阈值规则了解有限。

</div>
<div markdown="1"><span>核心问题</span>

在每轮只能观察当前输出及其验证得分、未来修改效果具有不确定性且每次模型调用都有成本的条件下，如何序贯决定停止并接受当前输出，或继续执行一轮自我改进，使预期质量收益相对于累计调用成本达到最优；以及在什么条件下该决策可由阈值型策略实现？

</div>
<div markdown="1"><span>作者直觉</span>

每次修改都可看成一次付费购买潜在改进的机会：当前输出较差且下一轮预期提升较大时，继续修改更划算；当前输出已经较好、进一步提升空间有限时，调用成本可能超过预期收益。最优停止理论正适合处理这种逐轮观察、逐轮付费且未来收益不确定的选择；若“当前得分越高，继续修改的边际价值越低”等结构条件成立，复杂决策还可能压缩为简单阈值，即得分达到某一水平便停止。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文把基础模型的自我改进过程建模为有限时域最优停止问题。输入是自然语言任务、模型当前生成结果及验证器给出的质量分数；每轮可以立即停止并获得当前结果的效用，也可以支付一次调用成本，让模型根据反馈继续生成。分数序列被视为马尔可夫过程，目标是在最多 $N$ 轮内选择停止时间，使最终质量收益减去累计改进成本的期望最大。作者先用真实自我改进轨迹识别分数转移模型、单轮成本和收益函数，再利用动态规划刻画最优决策，并根据论文前文证明的阈值结构，将策略计算化简为优化停止阈值 $\alpha$。
在代码优化实例中，验证器执行生成代码并检查测试正确性，同时综合运行时间和内存占用得到候选分数 $\tilde{x}_k\in[0,1]$；系统状态 $x_k$ 保存截至第 $k$ 轮见过的最高分，因此较差的新代码不会替换已有最佳代码。通俗地说，该方法不是预先规定“改写五次”，而是在每轮比较“现在交付的价值”和“再花一次钱后可能得到的价值”：只有预期改进足以覆盖成本时才继续。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成、验证并维护当前最佳结果

若代码未通过测试，则令候选分数 $\tilde{x}_k=0$；否则将运行时间与内存的联合消耗归一化并截断到 $[0,1]$。随后用 $x_k=\max\{x_{k-1},\tilde{x}_k\}$ 更新状态，只保留历史最佳代码及其分数。

<div class="method-step__io" markdown="1">

**输入**：一个自然语言编程任务、基础模型生成的代码，以及第 $k$ 轮执行测试得到的正确性、运行时间 $\mathcal{T}_k$ 和随时间变化的内存占用 $m_k(t)$。<br>
**输出**：当前最佳代码和可供停止策略观察的状态 $x_k\in[0,1]$。

</div>

**直观理解**：验证器相当于裁判，而状态 $x_k$ 是目前最高成绩。一次改写如果更差，系统仍可退回原来的最佳答案，不会因为继续尝试而丢失已有成果。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 从自我改进轨迹识别停止问题

作者把单轮延续成本 $c$ 设为实测平均货币成本，把停止收益设为 $g(x)=\beta x$，并用高斯过程回归从当前最佳分数 $x_k$ 预测下一轮候选分数。高斯过程以 $m(x)=x$ 为均值，并使用基于距离 $r=|x-x'|$ 的 Matérn 型协方差函数，以表达分数关系平滑且带随机性的假设。

<div class="method-step__io" markdown="1">

**输入**：三个基础模型在 effibench 的 $50$ 个任务上、每个任务最多 $N=10$ 轮所产生的状态转移、候选分数和调用费用。<br>
**输出**：针对每个基础模型的成本 $c$、可调收益权重 $\beta$，以及包含后验均值 $\tilde q(x)$ 和高斯噪声方差 $\sigma^2$ 的随机状态转移模型。

</div>

**直观理解**：这一步用历史试跑回答“当前已经得了这么高的分，再改一次通常能提高多少、波动多大、要花多少钱”。$\beta$ 则由使用者决定质量相对于费用有多重要，并不是从数据中学习的固定真值。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造有限时域最优停止决策

从终端条件 $V_N^\star(x)=g(x)$ 开始逆向计算 Bellman 价值：比较立即停止的收益 $g(x)$ 与支付 $c$ 后继续一步的期望价值 $Q_k^\star(x)$。若 $g(x)\geq Q_k^\star(x)$ 就停止，否则继续，且第 $N$ 轮必须停止。

<div class="method-step__io" markdown="1">

**输入**：当前阶段 $k$、状态 $x_k$、最大轮数 $N$、收益函数 $g$、单轮成本 $c$ 和已识别的随机转移模型 $f$。<br>
**输出**：各阶段的最优价值函数、停止集合与继续集合，以及从当前状态作出的停止或继续决策。

</div>

**直观理解**：该比较相当于同时估价两个选择：现在交付能值多少，以及再买一次模型调用平均能值多少。后一个选择先扣除调用费，因此“还能进步”并不自动意味着“值得继续”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 利用阈值结构压缩策略空间

将一般的状态到动作映射化简为停止阈值的优化，并通过已识别的高斯过程模型模拟轨迹，估计 $E\{g(x_{\tau_{\mu_\alpha}})-c\tau_{\mu_\alpha}\}$。作者分别采用 SPSA、交叉熵方法和差分进化搜索 $\alpha$，以降低依赖解析积分或穷举所有策略的计算负担。

<div class="method-step__io" markdown="1">

**输入**：论文前文命题得到的最优策略结构，以及由参数 $\alpha$ 表示的阈值策略 $\mu_\alpha$。<br>
**输出**：针对给定基础模型、成本和收益权重 $\beta$ 的优化阈值 $\alpha$。

</div>

**直观理解**：原本需要为大量分数和轮次分别规定动作；阈值结构把问题压缩成寻找少量分界值。模拟器反复试验不同分界值，选择平均净收益最高者。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 期望净收益最优停止目标

$$
\mu^{\star}\in\operatorname*{arg\,max}_{\mu}\;\mathbb{E}\!\left[g\!\left(x_{\tau_{\mu}}\right)-c\tau_{\mu}\right]\quad\text{subject to}\quad x_{k+1}=f(x_k,w_k),\;k=0,1,\ldots,N-1
$$

**符号说明**

- $\mu$：停止策略，即各阶段根据当前分数选择停止 $\mathsf{S}$ 或继续 $\mathsf{C}$ 的可测函数序列
- $\mu^{\star}$：使期望净收益最大的最优停止策略
- $\tau_{\mu}$：策略首次选择停止的轮次，且因第 $N$ 轮强制停止而满足不超过 $N$
- $x_k$：第 $k$ 阶段保存的当前最佳质量分数，取值位于 $[0,1]$
- $g(x)$：在分数为 $x$ 时停止所获得的质量收益；代码实验中设为 $g(x)=\beta x$
- $c$：每执行一轮自我改进产生的正成本
- $f$：描述分数从当前阶段转移到下一阶段的随机系统函数
- $w_k$：第 $k$ 轮生成过程的独立随机扰动
- $N$：允许执行的最大改进轮数

<div class="equation-explanation" markdown="1">

**直观理解**：目标把最终答案质量换算成收益，再减去停止前累计支付的调用成本。它明确说明策略优化的不是分数本身，也不是调用次数本身，而是两者之间由 $c$ 和 $\beta$ 决定的净效用权衡。<br>
**原文位置**：式 (3)，第 IV 节 Optimal Stopping Formulation；状态动态来自式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 最优价值的 Bellman 方程

$$
V_k^{\star}(x)=\max\!\left\{g(x),\;-c+\mathbb{E}\!\left[V_{k+1}^{\star}\!\left(f(x,w_k)\right)\right]\right\},\quad k=0,1,\ldots,N-1,\qquad V_N^{\star}(x)=g(x)
$$

**符号说明**

- $V_k^{\star}(x)$：从阶段 $k$、当前分数 $x$ 出发并在以后最优决策时可获得的最大期望净收益
- $g(x)$：立即停止并接受当前最佳结果所获得的收益
- $c$：选择继续时立即支付的一轮改进成本
- $\mathbb{E}$：对下一轮生成随机性求期望
- $f(x,w_k)$：在当前分数 $x$ 和随机扰动 $w_k$ 下得到的下一阶段分数
- $V_{k+1}^{\star}$：到达下一阶段后继续采用最优策略时的价值函数
- $Q_k^{\star}(x)$：文中定义的继续价值，即 $-c+\mathbb{E}\{V_{k+1}^{\star}(f(x,w_k))\}$

<div class="equation-explanation" markdown="1">

**直观理解**：花括号中的第一项是现在停止，第二项是付费再试一次并在下一阶段继续最优行动。取两者较大值产生规则：当 $g(x)\geq Q_k^{\star}(x)$ 时停止，否则继续；终点没有下一轮可选，所以价值只能等于当前收益。<br>
**原文位置**：式 (4)，第 IV 节 Characterizing the Optimal Stopping Policy

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文没有训练或微调基础模型，其优化对象是停止策略。系统识别阶段以观测对 $(x_k,\tilde{x}_{k+1})$ 拟合高斯过程后验，用于近似未知转移规律；策略阶段则通过模拟估计阈值策略的期望净收益 $E\{g(x_{\tau_{\mu_\alpha}})-c\tau_{\mu_\alpha}\}$，并搜索使其最大的 $\alpha$。其中 $g(x)=\beta x$，所以提高 $\beta$ 会提高质量在目标中的相对权重，而增大 $c$ 会使继续改进更难获得正的边际价值。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 质量评分与最佳结果保留模块**

候选评分先以测试是否通过区分不可用代码，再用归一化的内存时间积分衡量有效代码的效率；状态更新采用 $x_k=\max\{x_{k-1},\tilde{x}_k\}$。因此状态单调不降，并把完整生成历史压缩成当前最佳分数。

> 直观理解：停止策略需要一个能跨轮比较的统一质量信号。保留历史最佳结果还保证继续探索的风险主要是额外成本，而不是最终被迫采用更差代码。

**2. 高斯过程转移模型**

未知分数函数 $q$ 采用先验 $q\sim\mathcal{GP}(m,\kappa)$，其中 $m(x)=x$ 表示默认预期维持当前质量，协方差 $\kappa$ 表示相近分数处的改进规律应相近。拟合后用后验均值 $\tilde q(x)$ 和方差 $\sigma^2$ 构造受 $[0,1]$ 边界及历史最佳分数约束的随机转移；作者将被截断为 $0$ 或 $1$ 的观测直接作为高斯观测处理，因此得到的是近似后验。

> 直观理解：同一分数下再次调用模型不一定产生同样结果，所以只预测一个确定增量不够。高斯过程同时描述平均改进趋势和不确定性，使停止策略能够按“未来结果的分布”而不只是单点预测进行决策。

**3. 动态规划与阈值优化模块**

动态规划用 $V_k^\star(x)$ 表示从阶段 $k$ 和状态 $x$ 出发可获得的最大期望净收益，并以停止价值和继续价值的较大者更新。论文进一步利用已证明的单调性、边际收益递减和阈值策略结构，用 SPSA、交叉熵方法或差分进化在模拟环境中直接优化 $\alpha$。

> 直观理解：动态规划给出正确的决策标准，阈值结构则让这一标准易于计算和部署。三种随机或群体搜索算法是阈值求解器，并不改变最终策略所优化的净收益目标。

**训练与推理**

离线识别时，作者让 haiku 4.5、gemini flash-lite 3.1 和 gpt codex mini 5.1 在 effibench 上执行完整自我改进循环，记录当前最佳分数、下一轮候选分数和费用。对每个模型分别计算平均单轮成本，并以候选分数为回归目标、当前状态为输入拟合高斯过程；随后从该模型反复模拟分数轨迹，用 SPSA、交叉熵方法或差分进化优化给定 $\beta$ 下的阈值 $\alpha$。这相当于学习“模型在不同当前质量下还能改善多少”，而不是改变模型参数。
在线推理时，基础模型首先根据任务生成代码，验证器执行测试并得到 $\tilde{x}_0$，令 $x_0=\tilde{x}_0$。每轮策略读取阶段 $k$ 和当前最佳分数 $x_k$：若阈值规则判定停止，则返回历史最佳代码；若判定继续，则支付一次调用成本，将当前分数作为外部反馈再次调用模型，验证新代码并更新 $x_{k+1}=\max\{x_k,\tilde{x}_{k+1}\}$。该循环最迟在第 $N$ 轮终止。

**复现信息**

代码实验采用 effibench，共 $50$ 个任务，数据采集时最大改进轮数为 $N=10$。三个模型的平均单轮货币成本分别设为：haiku 4.5 的 $c=0.01$ 美元、gemini flash-lite 3.1 的 $c=0.0025$ 美元、gpt codex mini 5.1 的 $c=0.005$ 美元；这些费用按论文所述的 2026 年 3 月 17 日供应商单 token 价格计算。候选代码未通过测试时分数为 $0$；通过时依据内存时间积分相对参考实现的归一化结果评分并截断到 $[0,1]$。
高斯过程噪声方差 $\sigma^2$ 取拟合时估计的方差。由于评分会把边界外的潜在值截断到 $0$ 或 $1$，作者仍将边界候选分数当作未截断的直接高斯观测，因此转移后验属于计算便利的高斯近似，可能弱化边界处的统计校准。阈值优化与模拟在 M4 Pro、macOS Sequoia 15.6.1 和 Python 3.11 上运行；原文在所给章节中未明确报告高斯过程拟合库、优化器超参数、模拟轨迹数量及随机种子设置，复现时需要进一步核对论文代码或补充材料。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- EffiBench：面向代码效率评测的编程问题基准。实验使用其中 50 个问题作为停止策略的评估集；这些问题与第 V-C 节用于系统辨识的问题互不重叠，因此主要用于检验学习到的停止策略对未参与辨识的问题是否有效。原文节选未说明这 50 个问题的具体抽样方式、难度分布及完整基准规模。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**期望净价值 $\mathbb{E}\{g(x_{\tau_\mu})-c\tau_\mu\}$**

同时衡量停止时输出 $x_{\tau_\mu}$ 的收益 $g(x_{\tau_\mu})$ 与累计精炼成本 $c\tau_\mu$。其中 $\mu$ 是停止策略，$\tau_\mu$ 是该策略决定的停止时刻，$c$ 是每次迭代对应的成本。该指标直接对应论文的最优停止目标，而不是只看最终代码质量或只看成本。 （越高越好，因为更高的值表示在扣除精炼成本后仍保留了更大的输出收益。）

</div>
<div class="metric-item" markdown="1">

**输出质量随精炼轮次的变化**

用于判断自精炼是否持续改善模型输出，以及边际改善是否随迭代增加而缩小。该量在讨论中依据图 3 作定性总结，节选没有给出其具体计算公式或数值。 （输出质量本身越高越好，但实验关注的是每增加一轮所带来的增量是否足以抵消新增成本，因此不能脱离成本单独判断策略优劣。）

</div>
<div class="metric-item" markdown="1">

**Token 消耗与货币成本**

反映继续调用模型进行精炼所付出的计算资源和实际费用，并用于解释为何无限制增加迭代次数并不合理。 （在输出收益相同或相近时越低越好；论文的最终比较已通过期望净价值把该成本与输出收益合并考虑。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三个基础模型、四个收益权重 $\beta$，最大精炼次数为 $N=10$；比较优化阈值策略、固定迭代策略和 UCB 策略。

<div class="result-value" markdown="1">

作者报告，优化阈值策略 $\mu_\alpha$ 在全部模型与 $\beta$ 配置中均取得最高的期望净价值 $\mathbb{E}\{g(x_{\tau_\mu})-c\tau_\mu\}$。

</div>

这意味着本文策略在所测配置下能更有效地决定“何时继续精炼、何时停止”，而非仅通过增加迭代次数提高输出。由于节选没有提供图 7 的具体数值、误差条或显著性检验，该结果支持一致的经验优势，但不能据此量化优势幅度，也不能证明其对其他数据集、模型或成本结构必然成立。

<div class="result-source" markdown="1">

来源：第 VIII 节，Figure 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We observe that the optimized threshold policy μ α achieves the highest expected value in all configurations.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 固定迭代策略在四个不同收益权重 $\beta$ 下的比较。

<div class="result-value" markdown="1">

固定迭代策略中表现最好的预定轮数会随 $\beta$ 改变：$\beta$ 较小时较少迭代更有利，$\beta$ 较大时较多迭代更有利。

</div>

该现象说明固定预算不存在对所有收益偏好都最佳的统一选择。当输出改善的权重较低时，额外迭代成本更难被抵消；当输出改善更受重视时，多轮精炼才更值得。它解释了自适应停止的必要性，但没有单独证明本文阈值形式是唯一或普遍最优的策略结构。

<div class="result-source" markdown="1">

来源：第 VIII 节，Figure 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In particular, we observe that fewer iterations perform better when β is small, while more iterations are preferred when β is large.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### UCB 自适应策略与优化阈值策略在三个基础模型和四个 $\beta$ 取值上的比较。

<div class="result-value" markdown="1">

UCB 策略能够随 $\beta$ 自动调整停止行为，但在所有报告配置中持续落后于优化阈值策略。

</div>

这表明本文方法的收益并非仅来自“允许动态选择停止时机”，因为 UCB 也具有自适应能力；更可能的原因是本文利用了问题的最优停止结构并直接优化阈值。不过，原文节选未报告两者的具体差值或不确定性，因而不能判断这种差距在实践中是否足够大，或是否具有统计显著性。

<div class="result-source" markdown="1">

来源：第 VIII 节，Figure 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Finally, our experimental results show that the UCB policy automatically adapts to β but consistently underperforms the optimized threshold policy.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评估范围较窄：仅使用 EffiBench 的 50 个编程问题，且节选未提供三个基础模型的名称、问题抽样与难度分布。因此，实验尚不能说明策略能否推广到数学推理、文本生成等其他自精炼任务，或推广到明显不同能力与成本特征的模型。
- 结果报告不足以判断优势的稳定程度：每种方法虽以三个随机种子运行并报告平均值，但节选未给出标准差、置信区间、显著性检验或图 7 的具体分数，也没有组件消融。因而可以确认作者报告的排序，却无法从现有材料判断优势幅度、随机波动，以及系统辨识误差或阈值优化各自贡献了多少。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 固定迭代策略：预先指定精炼次数，到达该次数后停止。它是自精炼文献中最常见的做法，也是判断“根据当前状态自适应停止”是否优于固定计算预算的直接基线。
- 不同固定次数的策略族：各策略使用不同的预定迭代次数，用于观察最合适的计算预算是否随收益权重 $\beta$ 改变。节选未列出图 7 中具体比较了哪些固定次数。
- UCB 停止策略：采用 Sun 等人提出的上置信界方法，在有限阈值集合 $\alpha\in\{0,0.1,0.2,\ldots,1\}$ 上，根据各阈值价值的上置信界选择阈值。该基线同样能够自适应停止，因此用于区分本文优化方法的优势究竟来自“自适应”本身，还是来自更合适的策略建模与优化。

**实验想回答的问题**

- 在自精炼基础模型中，相比固定迭代次数和已有的自适应 UCB 策略，优化阈值停止策略能否在输出收益与迭代成本之间取得更高的期望净价值？
- 当收益权重 $\beta$ 改变时，不同停止策略能否适应“少迭代以节省成本”与“多迭代以提高质量”之间的权衡，并且这种结论能否跨三个基础模型保持一致？

**实验实现**

所有停止策略均在 EffiBench 的 50 个评估问题上运行，并分别应用于三个基础模型；每个问题最多允许 $N=10$ 次精炼。每种方法使用三个不同随机种子重复运行并报告平均性能。实验跨四个收益权重 $\beta$ 比较策略，以测试不同质量偏好或收益尺度下的成本权衡。UCB 策略在 11 个候选阈值组成的离散集合 $\{0,0.1,\ldots,1\}$ 中选择上置信界最高者。节选未给出三个基础模型的名称、每个策略的方差或置信区间、统计显著性检验、解码参数以及硬件配置。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It formalizes iterative self-refinement as an optimal stopping problem, optimizing reasoning improvement against inference cost.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`153390d4d0360e2825cbce6b8893829a50ed9ad82eb8a3c8a068bb0e2bd75ac1`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
