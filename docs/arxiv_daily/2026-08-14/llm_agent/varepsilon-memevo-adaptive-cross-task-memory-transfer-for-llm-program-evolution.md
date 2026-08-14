---
title: "[论文解读] $\\varepsilon$-MemEvo: Adaptive Cross-Task Memory Transfer for LLM Program Evolution"
description: "[arXiv 2608.12522][LLM Agent] $\\varepsilon$-MemEvo 将以往任务中成功的算法策略提炼为跨任务可复用的自然语言记忆，并根据当前搜索状态自适应决定跳过、提示或强化注入，以同时改善程序进化的冷启动效率并降低负迁移风险。"
arxiv_id: "2608.12522"
announcement_date: "2026-08-14"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T03:03:36.194581+00:00"
source_sha256: "4c67c98536217a4c70f383d7e4b3c76137bf6074aebf578393792bcaee4250fc"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "大语言模型程序进化"
  - "自动算法发现"
  - "跨任务知识迁移"
  - "策略记忆"
  - "负迁移"
  - "自适应注入门控"
  - "留一评测"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.12522</p>

# $\varepsilon$-MemEvo: Adaptive Cross-Task Memory Transfer for LLM Program Evolution

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Aofan Liu, Shiyuan Song, Yiyan Qi</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12522v1) · [PDF 下载](https://arxiv.org/pdf/2608.12522v1) · **关键词** 大语言模型程序进化, 自动算法发现, 跨任务知识迁移, 策略记忆, 负迁移, 自适应注入门控, 留一评测<br>


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

$\varepsilon$-MemEvo 将以往任务中成功的算法策略提炼为跨任务可复用的自然语言记忆，并根据当前搜索状态自适应决定跳过、提示或强化注入，以同时改善程序进化的冷启动效率并降低负迁移风险。

**不用术语来说**：现有的大语言模型程序进化系统每接到一个新优化任务，通常都从头试错；即使刚刚解决过结构相近的问题，也不会保留哪些思路有效。这会重复消耗模型调用和评估预算，并使搜索早期进展缓慢。直接把旧任务的代码或经验塞给新任务也不可靠，因为任务接口、评分方式和问题语义可能不同，不相关的经验反而会把搜索引向错误方向。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出内容层面的 Tactic Memory Bank：把已完成任务中的成功经验压缩为与具体代码接口和评价器解耦的自然语言“策略记忆”，从而支持异构优化任务之间的知识迁移。
- 将记忆使用形式化为自适应干预问题，并提出 Adaptive Injection Gate：依据搜索状态在 $\mathrm{skip}$、$\mathrm{hint}$ 和 $\mathrm{guide}$ 三种注入强度之间选择，使系统既能利用相关经验，也能在经验不匹配时退回接近无注入的搜索行为。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于基于大语言模型的程序进化与自动算法发现领域。典型系统以待优化程序及其评测器为起点，让大语言模型反复生成或修改代码，再依据执行得分选择较优程序继续搜索；FunSearch、AlphaEvolve 与 AdaEvolve 已将这一范式用于组合优化、矩阵乘法、科学计算和系统工程问题。然而，这些系统的选择与经验积累通常局限于当前任务：任务结束后，已发现的策略不会被显式保留并用于后续任务。本文关注的背景问题因此不是单次搜索能否找到高分程序，而是如何让不同接口、指标和代码结构的任务共享可复用的算法经验，同时避免不相关经验干扰当前搜索。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大语言模型程序进化**

一种以大语言模型充当变异或重写算子的程序搜索方法：模型生成候选代码，评测器执行并打分，搜索过程再从较优候选出发继续迭代。它与传统遗传编程的核心差别是，代码变化主要由能够理解自然语言和程序语义的大语言模型提出，而非完全依赖人工规定的变异规则。

</div>
<div class="concept-item" markdown="1">

**跨任务知识迁移与负迁移**

跨任务知识迁移是把已完成任务中学到的策略用于新任务，以减少重复探索和冷启动成本；当旧策略与新任务不匹配并使搜索表现变差时，则称为负迁移。本文把避免负迁移视为跨任务记忆系统的核心控制问题。

</div>
<div class="concept-item" markdown="1">

**岛模型与自适应干预**

岛模型并行维护多个候选程序群体，通过各自演化及周期性交互保持搜索多样性；AdaEvolve 等系统还会注入概念上不同的策略以突破局部停滞。本文不替代这种任务内搜索机制，而是在其上增加跨任务记忆层，并自适应决定何时以及以多强的方式向生成提示注入旧经验。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

设系统按顺序处理多个程序优化任务；每个目标任务提供任务描述、程序接口、可执行评测器以及当前任务内产生的候选程序与得分。系统可以访问由其他已完成任务构建的策略记忆，但在评测任务 $k$ 时采用内容级留一法，明确排除来自任务 $k$ 自身的全部记忆，从而检验真正的跨任务迁移，而非复用同一任务的历史答案。系统需要检索与当前问题可能相关的自然语言策略摘要，并根据当前搜索状态在“跳过记忆”“作为提示轻度建议”和“作为指导强力注入”等干预强度之间选择；随后由大语言模型生成新程序，经目标任务评测器打分并进入后续进化。最终输出是当前任务中搜索得到的高质量程序及其搜索轨迹，目标是在异构任务接口和评价指标下提高收敛效率与最终搜索质量，同时使语义不匹配的记忆不会造成明显负迁移。该设置假定旧任务经验能够被压缩成与具体代码和 API 相对解耦的策略描述，也假定目标任务具有可自动执行、可比较候选程序的评测器。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\varepsilon\text{-MemEvo}$**

本文提出的记忆增强程序进化框架名称，其中 MemEvo 表示 memory-augmented evolution。

</div>
<div class="notation-item" markdown="1">

**$k$**

当前接受评测的目标任务索引；留一设置会从记忆库中排除该任务自身的经验。

</div>

</div>

**直接相关的工作**

- **FunSearch 与 AlphaEvolve**: 二者代表以大语言模型迭代生成、评测和改进程序的自动算法发现系统，证明了该范式在数学优化与科学计算中的能力；但据本文概括，它们按任务独立运行，没有显式的跨任务记忆，因此新任务仍从零开始。
- **AdaEvolve**: 它是本文最直接的任务内进化参照，通过自适应岛模型和周期性的范式突破改善多样性与搜索；本文在此类任务内机制之上增加跨任务层，用策略记忆表示旧经验，并以自适应门控决定是否及如何注入这些经验。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

LLM 程序进化依靠反复生成、执行、评分和改写程序来发现算法，因此每一次无效探索都会消耗模型 API、运行时间和候选程序评估预算。现有系统完成一个任务后往往丢弃搜索经验，导致后续相关任务仍需冷启动，重复发现相似的布局规律、搜索启发式或系统优化原则；论文以几何装箱为例，说明一种任务中学到的结构化排列与对称偏移经验，本可帮助另一种相关装箱任务。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **FunSearch 与 AlphaEvolve 一类 LLM 程序进化方法**：让 LLM 迭代生成候选程序，通过任务专用评价器获得分数，再利用较优程序继续变异和改进。它们能够发现新算法，但其基本工作单元是单个任务，搜索轨迹和成功策略通常不会被组织成可供后续任务调用的长期记忆。
- **AdaEvolve 的自适应单任务搜索**：在程序进化过程中使用自适应岛模型和范式突破机制维持候选方案的多样性、推动当前任务跳出局部搜索模式。它改进的是任务内部的探索过程，并未解决已完成任务的策略如何迁移到接口和评价指标不同的新任务。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 任务之间缺少持久知识传递：每个新任务都从头开始，系统既不保留成功策略，也不形成对搜索结构的可复用认识，后果是相关任务间出现冗余探索、冷启动收敛较慢以及 API 预算浪费。
- 无条件注入旧经验存在负迁移：来自其他任务的策略可能在语义或约束上与目标任务不匹配，持续注入会压制当前任务自身的有效搜索方向。作者报告其消融中，始终注入策略和基于停滞规则的策略都曾使五个任务中的两个无法产生任何分数改进，说明仅检索到记忆并不等于记忆适合被使用。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作缺少一种面向异构程序优化任务的完整迁移机制：一方面，需要把经验表示成不依赖源任务代码、API 和评价器的可复用策略；另一方面，还需要在线判断检索结果是否适合当前搜索状态，并控制其影响强度。尤其未解决的是，如何在没有目标任务自身记忆、也不为每个任务手工调整阈值的条件下，使跨任务迁移既产生收益又保持安全。

</div>
<div markdown="1"><span>核心问题</span>

能否让 LLM 程序进化系统从其他已完成任务中提取并迁移抽象策略，同时根据目标任务的实时搜索状态，自适应选择不注入、弱提示或强引导，从而加快收敛并避免语义不匹配记忆造成的负迁移？

</div>
<div markdown="1"><span>作者直觉</span>

可迁移的往往不是一段绑定具体函数签名的源代码，而是更抽象的解题动作，例如“采用规则网格并加入对称偏移以减少重叠”；自然语言策略摘要因此更容易跨越 API 和评分标准差异。但记忆应被视为可能有副作用的外部干预：搜索本来持续改善时没有必要打断它，进入平台期时则可逐步尝试提示；如果某种注入连续无效，就降低再次采用它的概率。这样，系统可在相关任务上借助旧经验缩短试错过程，在不相关任务上逐渐恢复接近独立搜索的行为。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把跨任务经验作为一个持续状态 $\mathcal{M}=(\mathcal{B},\pi)$ 接入 AdaEvolve：策略记忆库 $\mathcal{B}$ 保存以往成功程序中提炼出的、与具体 API 无关的自然语言算法策略，注入策略 $\pi$ 则根据当前搜索状态决定不使用记忆、弱提示或强引导。对于任务 $T_i$，系统以任务描述 $d_i$、种子程序 $p_i^0$ 和评价函数 $f_i:\mathcal{P}\to\mathbb{R}$ 为输入，在最多 $M$ 次迭代内生成、执行并评价候选程序，以提高当前最优分数；任务成功结束后，最终最优程序再被压缩为一条策略，供后续任务使用。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建跨任务策略记忆

使用 GPT-4.1-mini 将具体程序蒸馏为任务无关的自然语言策略摘要，并保存策略文本、方法类型标签、原任务描述、嵌入向量和相对基线的改进量 $\Delta_i$。每个成功任务只追加一条记录，而且该记录仅对后续任务可见。

<div class="method-step__io" markdown="1">

**输入**：已成功完成任务 $T_i$ 的描述 $d_i$、最终最优程序 $p_i^{\mathrm{best}}$ 及其分数 $f_i(p_i^{\mathrm{best}})$。<br>
**输出**：持久化策略记忆库 $\mathcal{B}$ 中的一条新策略记录。

</div>

**直观理解**：系统不背诵旧代码，而是总结旧代码为何有效，例如“先贪心初始化，再局部优化”。这样即使新任务的函数接口和评分器不同，抽象的解题套路仍可能复用。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 识别搜索状态并选择注入强度

系统将搜索阶段划分为 improving、plateau、stagnating，并按 $t/M<0.4$ 区分 early 与 late，组合成六个离散状态 $s_t$。随后对三个动作 $a\in\{\texttt{skip},\texttt{hint},\texttt{guide}\}$ 分别从 Beta 后验采样，以 Thompson Sampling 选择样本值最大的动作 $a_t$。

<div class="method-step__io" markdown="1">

**输入**：当前迭代 $t$、总预算 $M$、全局改进率 $\rho$，以及各状态—动作对的 Beta 后验参数 $\alpha_{s,a}$ 与 $\beta_{s,a}$。<br>
**输出**：本轮状态 $s_t$ 与注入动作 $a_t$。

</div>

**直观理解**：当原有搜索仍在稳定进步时，额外经验可能干扰有效方向，因此系统倾向少干预；当搜索停滞时，系统才更愿意尝试外部策略。随机后验采样还保留了探索机会，不会因早期少量结果就永久锁定某个动作。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 检索策略并构造增强提示

若 $a_t=\texttt{skip}$，直接使用 AdaEvolve 的基础提示；否则以任务描述嵌入与记忆条目嵌入的余弦相似度为主，并按历史改进量加权，检索得分最高的三条策略。$\texttt{hint}$ 将这些策略作为可选参考，$\texttt{guide}$ 则把排名第一的策略作为推荐方案，并注入范式突破生成过程。

<div class="method-step__io" markdown="1">

**输入**：目标任务描述 $d_k$、排除目标任务内容后的记忆库 $\mathcal{B}_{-k}$，以及动作 $a_t$。<br>
**输出**：包含父程序、搜索上下文和适量跨任务策略的生成提示。

</div>

**直观理解**：检索负责找“看起来与当前问题相关且过去确实有效”的经验，门控负责决定这些经验只是备选建议还是主要方向。两者分工可以减少语义相似但实际不适用的经验造成负迁移。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成评价并延迟更新门控

LLM 生成候选程序 $p_{\mathrm{new}}$，评价器计算 $f_k(p_{\mathrm{new}})$，AdaEvolve 更新种群与当前最优分数 $f_t^*$；系统把 $(s_t,a_t,t,f_{\mathrm{pre}}^*)$ 放入 FIFO 队列。五轮后若最优分数超过动作前分数至少 $\epsilon=10^{-8}$，就增加对应的 $\alpha_{s_t,a_t}$，否则增加 $\beta_{s_t,a_t}$；任务结束时用最终最优分数结算尚未到期的记录。

<div class="method-step__io" markdown="1">

**输入**：增强提示、目标任务评价函数 $f_k$、动作前最优分数 $f_{\mathrm{pre}}^*$、奖励窗口 $w=5$ 和待结算队列 $\mathcal{Q}$。<br>
**输出**：更新后的程序种群、最优程序与分数，以及反映该状态下各注入动作成败经验的后验策略 $\pi$。

</div>

**直观理解**：某次提示不一定立刻产生更好程序，也可能先生成一个有潜力的中间版本，所以系统等待五轮再判断它是否有帮助。成功和失败会逐渐改变后续动作概率，使不匹配的强引导快速失去选择优势。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 策略记忆的加权语义检索

$$
r_k=\cos(\mathbf{e}_j,\mathbf{e}_k)\cdot\left(1+0.3\cdot\log\left(1+\max(\Delta_k,0.01)\right)\right)
$$

**符号说明**

- $r_k$：记忆条目 $k$ 针对当前任务的最终检索排序分数。
- $\mathbf{e}_j$：当前任务描述 $d_j$ 的文本嵌入向量。
- $\mathbf{e}_k$：记忆条目 $k$ 所对应历史任务描述的文本嵌入向量。
- $\cos(\mathbf{e}_j,\mathbf{e}_k)$：两个任务描述嵌入的余弦相似度，用于衡量语义相关性。
- $\Delta_k$：条目 $k$ 所记录策略相对其基线取得的分数改进。
- $0.3$：历史改进量对检索分数的固定加权系数。
- $0.01$：对改进量设置的下限，避免非正或过小改进造成不适当的对数权重。

<div class="equation-explanation" markdown="1">

**直观理解**：公式先按任务描述是否相似确定主要排序，再温和提高历史上更有效策略的权重；对数函数限制大改进量的影响，避免它完全压过语义相关性。系统据此返回排名前三的策略，但检索得分本身不保证策略适用，因此后续仍需门控。<br>
**原文位置**：第 3.3 节，公式 (2)

</div>

</div>

<div class="equation-block" markdown="1">

#### Thompson Sampling 决策与延迟二元奖励

$$
\theta_{s_t,a}\sim\mathrm{Beta}(\alpha_{s_t,a},\beta_{s_t,a}),\qquad a_t=\arg\max_a\theta_{s_t,a},\qquad R_t=\mathbf{1}\!\left[f^*_{t+w}>f^*_{\mathrm{pre}}+\epsilon\right]
$$

**符号说明**

- $s_t$：第 $t$ 轮的离散搜索状态，由改进阶段和任务进度共同决定。
- $a$：候选注入动作，取值为不注入、弱提示或强引导。
- $\alpha_{s_t,a}$：状态 $s_t$ 下动作 $a$ 的成功计数参数；奖励为 $1$ 时增加 $1$。
- $\beta_{s_t,a}$：状态 $s_t$ 下动作 $a$ 的失败计数参数；奖励为 $0$ 时增加 $1$。
- $\theta_{s_t,a}$：从对应 Beta 后验采样得到的动作成功率样本。
- $a_t$：第 $t$ 轮选择的注入动作，即后验样本最大的动作。
- $R_t$：第 $t$ 轮动作在延迟窗口结束后的二元奖励。
- $f^*_{\mathrm{pre}}$：执行第 $t$ 轮动作之前的全局最优分数。
- $f^*_{t+w}$：经过 $w$ 轮后获得的全局最优分数。
- $w$：奖励观察窗口，原文设为 $5$ 次迭代。
- $\epsilon$：判定真实改进所需超过的数值容差，原文设为 $10^{-8}$。
- $\mathbf{1}[\cdot]$：指示函数；条件成立时取 $1$，否则取 $0$。

<div class="equation-explanation" markdown="1">

**直观理解**：门控先从每个动作当前可信的成功率分布中抽样，再选择抽样值最高者，因此能在利用已知好动作和探索不确定动作之间自动权衡。奖励不要求注入后的下一条程序立即改进，而是检查五轮内是否刷新全局最优值；这更符合程序进化中中间候选可能间接促成后续突破的情况。<br>
**原文位置**：第 3.4 节“Decision and reward”及算法 1

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：该工作没有训练一个新的 LLM 参数模型，也没有定义可反向传播的统一损失函数；底层优化目标是在每个任务 $T_i$ 的 $M$ 次迭代内最大化评价函数 $f_i$。跨任务控制器在线学习的是状态—动作成功概率：若动作后五轮内出现超过 $\epsilon$ 的全局最优分数提升，就把该观察记为成功并更新 $\alpha_{s,a}$，否则记为失败并更新 $\beta_{s,a}$；因此它优化的是“某种搜索状态下该注入强度促成后续改进的概率”，而不是直接拟合程序分数。策略摘要提取也属于推理式蒸馏，不涉及摘要模型的参数训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 策略记忆库**

记忆条目存储任务无关策略摘要而非原始代码，并以 1536 维 text-embedding-3-small 表示任务语义。检索同时考虑目标描述与历史描述的余弦相似度，以及策略相对基线的改进量 $\Delta_k$，返回前三条记录；目标任务评估时使用 $\mathcal{B}_{-k}$ 排除同任务内容。

> 直观理解：原始代码往往绑定具体数据结构、接口和评分方式，直接搬到新任务中很难使用；策略摘要保留的是可迁移的算法结构。改进量加权则避免仅凭文字相似度优先取回一个过去效果很弱的方案。

**2. 自适应注入门控**

门控是一个离散上下文多臂老虎机：上下文 $s$ 是搜索阶段与任务进度的组合，动作 $a$ 是 $\texttt{skip}$、$\texttt{hint}$ 或 $\texttt{guide}$，每个 $(s,a)$ 独立维护 $\mathrm{Beta}(\alpha_{s,a},\beta_{s,a})$。先验在 improving 状态偏向 $\texttt{skip}$、在 stagnating 状态偏向 $\texttt{guide}$，对应参数均为 $\mathrm{Beta}(3,1)$，其余组合使用无偏的 $\mathrm{Beta}(1,1)$。

> 直观理解：该模块的首要目标是阻止负迁移，而不是假设记忆总能提升得分。若强引导连续失败，其后验会迅速降低；若当前任务本身搜索顺利，系统也有先验理由保持基础搜索过程。

**3. AdaEvolve 搜索与延迟反馈接口**

该框架不替换 AdaEvolve 的程序生成、评价和种群更新机制，而是在生成提示之前增加检索和门控，并在评价之后返回二元延迟奖励。待结算决策存入 FIFO 队列 $\mathcal{Q}$，从而允许多个尚未达到奖励窗口的动作并行等待反馈。

> 直观理解：跨任务模块相当于包裹在现有程序进化器外的一层控制器：它只改变本轮给 LLM 多少旧经验，不改变目标任务的真实评分标准。延迟队列让系统根据随后几轮的搜索结果评价建议，而不是只看下一步是否立刻涨分。

**训练与推理**

运行前，系统持有记忆库 $\mathcal{B}$、各 $(s,a)$ 的 Beta 参数和队列 $\mathcal{Q}$；首次运行时按照 improving 偏向 $\texttt{skip}$、stagnating 偏向 $\texttt{guide}$ 的信息先验初始化。处理任务 $T_k$ 时，每轮先由改进率 $\rho$ 与进度 $t/M$ 得到状态，再通过 Thompson Sampling 选择注入动作；非 $\texttt{skip}$ 动作从 $\mathcal{B}_{-k}$ 检索三条策略并按动作强度写入提示，随后由 LLM 生成程序、由 $f_k$ 评价、由 AdaEvolve 更新种群。每个动作及其执行前最优分数进入 $\mathcal{Q}$，达到 $w=5$ 后结算奖励并在线更新后验；任务边界处结算剩余记录。任务成功完成后，GPT-4.1-mini 根据 $d_k$、$p_k^{\mathrm{best}}$ 和 $f_k(p_k^{\mathrm{best}})$ 生成一条抽象策略并追加到记忆库，更新后的 $\mathcal{B}$ 与 $\pi$ 一并传给下一任务。

**复现信息**

公平解释该方法需要保留以下设置：底层搜索器是 AdaEvolve；每项任务由描述、种子程序和独立评价函数定义，各比较方法共享相同种子程序与评价器。策略提取模型为 GPT-4.1-mini；任务描述嵌入使用 1536 维 text-embedding-3-small；每次最多检索三条策略。状态阈值为 $\rho>0.1$ 对应 improving、$0.02<\rho\leq0.1$ 对应 plateau、$\rho\leq0.02$ 对应 stagnating，且 $t/M<0.4$ 为 early、其余为 late；奖励窗口为 $w=5$，改进容差为 $\epsilon=10^{-8}$。留一评估只删除目标任务的记忆内容，保留跨任务累计的策略后验，因此复现实验时不能把该协议误解为对每个目标任务都重新初始化门控。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- AlphaEvolve 数学优化任务组：共 4 个任务，包括圆堆积、信号处理和两个不等式问题。它们用于检验策略性自然语言记忆能否跨数学问题迁移；所有目标分数均为越高越好。原文节选未给出各任务实例规模、数据划分或两个不等式任务的具体名称。
- ADRS 系统优化任务组：共 4 个任务，即 EPLB、LLM-SQL、PRISM 和事务调度，用于检验方法在接口、评估器及程序结构不同的系统工程问题上是否仍有效；所有目标分数均为越高越好。原文节选未解释各缩写、实例规模与数据划分。
- 消融任务子集：从上述基准中选取 5 个任务，并以 AUCC@50 评估不同记忆注入策略。节选明确提到其中的 circle_packing、signal、txn_scheduling、EPLB 和 LLM-SQL，作用是同时覆盖记忆有益和语义失配会导致严重负迁移的情形。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**AUCC**

搜索过程中最佳目标分数随迭代或计算预算变化的收敛曲线下面积，综合衡量解的质量与取得该质量的速度；AUCC@50 表示统计前 50 次迭代。消融中还报告相对 AdaEvolve 的逐任务百分比改进，并将 AUCC 为 0 的失败计为 $-100\%$。 （越高越好，因为较大的面积表示在更多搜索阶段维持了更高的目标分数，而不只是在终点偶然得到较好程序。）

</div>
<div class="metric-item" markdown="1">

**早期阶段收敛改进**

衡量有限搜索预算的早期阶段相对基线取得高质量程序的速度。节选只给出平均相对增益，没有说明早期阶段的精确迭代边界或计算公式。 （越高越好，因为它表示方法更早利用到可迁移经验。）

</div>
<div class="metric-item" markdown="1">

**有效改进程序产生情况**

用于识别灾难性失败：若 50 次迭代内没有生成任何能提高分数的程序，则该任务的 AUCC 为 0。该指标主要用于判断静态记忆注入是否使搜索完全失效。 （能够产生有效且提高分数的程序更好；AUCC 为 0 表示最严重的失败情形。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 以 GPT-5 为主干，在全部 8 个数学与系统优化任务上比较 $\varepsilon$-MemEvo 和 AdaEvolve，并采用内容级 LOO 排除目标任务记忆。

<div class="result-value" markdown="1">

作者报告 $\varepsilon$-MemEvo 在 8 个任务上的 AUCC 均超过 AdaEvolve，平均相对增益为 $+8.7\%$。

</div>

这说明跨任务策略记忆在所测任务上不仅提高了平均搜索效率，而且没有出现某个任务被基线反超的情况。由于 AUCC 同时受中间解质量和收敛速度影响，该结果比只比较最终最好分数更能反映预算内表现；但 8 个任务规模有限，且节选缺少方差与显著性检验，不能据此证明对任意程序进化任务都稳定有效。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the primary GPT-5 backbone, $\varepsilon$-MemEvo improves AUCC over AdaEvolve on all 8 tasks, with a mean relative gain of +8.7%, and improves early-stage convergence by +9.4% on average.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### GPT-5 主干下考察搜索早期阶段的收敛表现。

<div class="result-value" markdown="1">

作者报告早期阶段收敛平均提高 $+9.4\%$。

</div>

该结果支持记忆的主要价值之一是让搜索更早获得可用策略，而不只是提高终点成绩。这对调用大模型成本受限的程序进化尤其重要；不过节选未定义“早期阶段”的边界，也未给出逐任务数值，因此无法判断增益是否由少数任务主导。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the primary GPT-5 backbone, $\varepsilon$-MemEvo improves AUCC over AdaEvolve on all 8 tasks, with a mean relative gain of +8.7%, and improves early-stage convergence by +9.4% on average.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 分析采用自适应门控的完整方法在 5 个消融任务上的稳健性，并与 AdaEvolve 及静态记忆策略比较。

<div class="result-value" markdown="1">

作者称 $\varepsilon$-MemEvo 是唯一无需逐任务调阈值、且在全部 5 个任务上均优于 AdaEvolve 的记忆增强变体。

</div>

该结果强调门控的核心作用是控制负迁移风险，而非在每个适配任务上追求最大峰值收益。它表明统一策略在这 5 个任务上具有较好的稳健性，但不意味着完整方法在每个任务上都是绝对最优，因为部分语义匹配任务中静态策略取得了更大的增益。

<div class="result-source" markdown="1">

来源：Section 4.5, Ablation

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

$\varepsilon$-MemEvo is the only memory-augmented variant that improves over AdaEvolve on all 5 tasks without per-task threshold tuning.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给节选缺少完整结果表、每次实验的重复次数、随机性控制、方差或置信区间及显著性检验。因此 $+8.7\%$、$+9.4\%$ 和消融差异只能作为作者报告的点估计，尚不能据此判断统计稳定性；Gemini-3-Pro 虽被称为复现实验主干，但其具体跨模型结果未在节选中呈现。
- 外部有效性仍受限制：实验只有 8 个任务，且来源集中于 AlphaEvolve 与 ADRS；5 任务消融还表明收益依赖记忆与目标任务的语义匹配。内容级 LOO 能排除直接使用目标任务记忆，但不能自动排除任务间高度相似、共享模板或评估结构所带来的近邻迁移效应。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- AdaEvolve：$\varepsilon$-MemEvo 所扩展的基础自适应程序进化框架，不使用本文的留一法记忆和 Thompson Sampling 门控。与它比较可隔离跨任务记忆机制带来的增益。
- TopK：较简单的 top-$K$ 变异基线。它用于判断收益是否只是来自一般性的候选保留与变异，而非自适应进化和跨任务记忆；节选未给出 $K$ 值及完整更新规则。
- MemEvo-always：每轮都注入检索记忆的静态策略。它用于检验“拥有记忆”本身是否足够，以及无条件注入是否会造成负迁移。
- MemEvo-stagnation：检测到停滞便注入记忆的规则策略。它与自适应门控比较，用于判断简单的停滞启发式能否取代数据驱动的注入决策。

**实验想回答的问题**

- 在严格排除目标任务记忆的跨任务迁移条件下，$\varepsilon$-MemEvo 是否能比无记忆的 AdaEvolve 更有效地利用固定搜索预算，并加快搜索早期的收敛？
- 自适应注入门控能否在保留有用记忆收益的同时，避免语义不匹配记忆造成的负迁移；其决策是否具有可解释性并能迁移到不同大模型生成器？

**实验实现**

实验覆盖 8 个任务，主生成器为通过 LiteLLM 调用的 GPT-5，并在表格中报告 Gemini-3-Pro 复现实验；检索使用 text-embedding-3-small。$\varepsilon$-MemEvo 在 AdaEvolve 上加入内容级 Leave-One-Out（LOO）记忆和 Thompson Sampling（TS）门控：评估某个目标任务时，记忆库排除来自该任务的条目，因此测试的是跨任务迁移，而不是复用同任务答案。消融采用 AUCC@50。节选提到实验 1 为“memory accumulation”，但预算、随机种子、重复次数、置信区间、硬件配置以及 Gemini-3-Pro 的逐项结果均未完整提供。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 将完整 TS 门控分别替换为每轮注入的 MemEvo-always 和检测停滞即注入的 MemEvo-stagnation，在 EPLB 与 LLM-SQL 上运行 50 次迭代。 | 两种静态策略在 EPLB 和 LLM-SQL 上均得到 AUCC $=0$，即 50 次迭代没有一次产生提高分数的程序；相同任务上的 $\varepsilon$-MemEvo 与 AdaEvolve 均能产生有效程序。 | 该消融隔离了“是否自适应决定注入”这一组件。灾难性差异说明检索到记忆并不等于记忆适用，固定注入会反复强化不合适的代码模式；完整门控可依据失败反馈降低 guide 的后验概率并回到 skip。该结果证明了所测失配任务上的风险控制价值，但节选没有给出多次运行的失败频率，因而无法判断失败是否具有随机波动。 | Section 4.5, Ablation<br><span class="experiment-evidence">MemEvo-always and MemEvo-stagnation both achieve AUCC $=0$ on EPLB and LLM-SQL—no iteration in 50 produces a score-improving program on these tasks, while $\varepsilon$-MemEvo (full) and AdaEvolve both produce valid programs on the same tasks.</span> |
| 在记忆较匹配的 circle_packing、signal 和 txn_scheduling 上比较完整门控与静态注入策略。 | circle_packing 上 MemEvo-stagnation 与完整方法的相对增益分别为 $+13.4\%$ 和 $+9.9\%$；signal 上分别为 $+4.0\%$ 和 $+2.9\%$；txn_scheduling 上 MemEvo-always 最佳，增益为 $+55.3\%$。 | 该消融显示门控不是无条件提高峰值：当记忆确实匹配时，更积极的静态注入可能得到更高 AUCC。完整方法牺牲部分单任务上限以避免在 EPLB、LLM-SQL 这类失配任务上归零，因此其优势应解释为跨任务风险调整后的稳健性，而不是每项任务的最高得分。 | Section 4.5, Ablation<br><span class="experiment-evidence">On circle_packing (+13.4% vs. +9.9%) and signal (+4.0% vs. +2.9%), MemEvo-stagnation edges out $\varepsilon$-MemEvo by small margins; on txn_scheduling, MemEvo-always is best (+55.3%).</span> |

**定性案例**

- Figure 3 的后验均值热图提供了门控行为案例：在 improving 状态选择 skip，在 plateau_early 状态仍选择 skip，在 plateau_late 状态改选 hint；未被观测到的 stagnating 状态则保留偏向更强记忆使用的信息先验。均匀 $\mathrm{Beta}(1,1)$ 先验下已观测状态的贪心动作不变，支持这些动作主要来自实验数据更新。不过未观测状态仍由先验决定，不能视为已经从数据中验证。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops an LLM-based program-evolution agent that retrieves and adaptively transfers tactic memories across algorithmic search tasks.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`4c67c98536217a4c70f383d7e4b3c76137bf6074aebf578393792bcaee4250fc`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
