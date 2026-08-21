---
title: "[论文解读] Learning When to Think: Adaptive Reasoning for Test-Time Compute Allocation"
description: "[arXiv 2608.20256][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.20256"
announcement_date: "2026-08-21"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-21T02:07:25.385659+00:00"
source_sha256: "ff996b930246f4b525710310633b07440803e4f8a02a8a327c0d9f0cc4b1db64"
tags:
  - "LLM Reasoning"
  - "自适应推理"
  - "测试时计算分配"
  - "强化学习可验证奖励"
  - "群组相对策略优化"
  - "推理路由"
  - "链式思维"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.20256</p>

# Learning When to Think: Adaptive Reasoning for Test-Time Compute Allocation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-21</span>
<span><strong>作者</strong> Gijs Kassenaar, Zhao Yang, Vincent François-Lavet</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.20256) · [PDF 下载](https://arxiv.org/pdf/2608.20256) · **关键词** 自适应推理, 测试时计算分配, 强化学习可验证奖励, 群组相对策略优化, 推理路由, 链式思维<br>


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

本文属于大语言模型推理与测试时计算分配领域。链式思维（Chain-of-Thought, CoT）通过生成中间推理步骤提升数学和代码任务表现，但推理长度会增加推理延迟、计算成本和训练成本。现有强化学习可验证奖励（RLVR）方法通常为所有输入使用统一的最大响应长度，因此容易对简单问题过度计算，也可能限制困难问题所需的搜索空间。本文研究让模型针对每个问题自适应选择推理预算：模型首先生成一个路由标记，再按照该标记直接作答、进行短推理或进行长推理。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**链式思维（CoT）**

链式思维要求模型先生成若干中间步骤，再给出最终答案。中间步骤可能帮助模型分解复杂问题，但也会带来额外的生成长度和计算开销。

</div>
<div class="concept-item" markdown="1">

**强化学习可验证奖励（RLVR）**

RLVR 使用能够自动检查的结果作为奖励，例如数学题答案是否正确，并据此更新模型策略。它不必为每一步推理提供人工标注，但只能直接优化可验证的最终结果。

</div>
<div class="concept-item" markdown="1">

**GRPO**

群组相对策略优化（GRPO）针对同一个问题从当前策略采样一组回答，并比较它们的奖励来估计相对优势。与需要额外价值网络的强化学习方法不同，GRPO可用组内奖励统计量指导策略更新。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定输入问题$q$，本文使用一个约1.5B参数的蒸馏推理模型作为策略$pi_theta$，要求它在回答开头生成三个路由模式之一：NoThink、Short或Long。NoThink要求尽快直接作答，Short允许有限的简短推理，Long允许扩展推理；随后模型在对应的长度约束和奖励形状下生成最终响应。训练设定是无单独路由器、无人工路由标签的端到端GRPO：路由标记由主模型自身产生，并与后续推理共同接受奖励优化。目标是在保持答案准确率的同时，使简单问题使用较少计算、困难问题获得更多推理预算，并避免所有问题塌缩到同一种模式。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$q$**

输入问题或提示。

</div>
<div class="notation-item" markdown="1">

**$\pi_\theta$**

参数为$\theta$的当前语言模型策略，即生成路由标记和后续响应的模型。

</div>
<div class="notation-item" markdown="1">

**$o_i$**

对同一问题采样得到的第$i$个完整输出，包含路由标记、推理过程和最终答案。

</div>
<div class="notation-item" markdown="1">

**$A_i$**

第$i$个输出的组内相对优势，用于表示其奖励相对于同组其他输出的好坏。

</div>

</div>

**直接相关的工作**

- **PPO（Schulman et al., 2017）与GRPO（Shao et al., 2024）**: 它们是本文所采用的强化学习优化背景。原文指出，标准PPO和GRPO通常对所有训练样本统一施加单一的最大响应长度，而本文在GRPO内部增加按问题选择推理模式的机制。
- **基于折扣的推理长度控制方法（Parthasarathi et al., 2025；Ayoub et al., 2025；Zhang and Zuo, 2025；Yang et al., 2026）**: 这类方法通过逐令牌折扣直接惩罚较长推理，能够缩短响应并维持部分准确率，但其长度压力对不同难度问题基本固定。本文将其局限概括为缺乏按提示难度自适应分配预算，并改为让模型选择NoThink、Short或Long。

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

该方法将语言模型的推理过程视为一个按题目难度分配测试时计算量的路由问题。模型在回答开头生成一个离散路由标记 `$\mathrm{NoThink}$`、`$\mathrm{Short}$` 或 `$\mathrm{Long}$`，分别对应尽快作答、短推理和长推理；随后根据路由模式施加不同的奖励函数与硬性生成上限，并使用去除标准差归一化的 GRPO 更新策略。完整流程是：给每个提示附加路由指令，采样多个回答，识别首个路由标记并执行模式约束，按答案正确性和推理长度计算奖励，进行组内优势估计与模式平衡修正，最后通过 GRPO 更新模型。直观地说，模型先决定“这道题需要思考多久”，再在该计算预算内回答，而不是对所有题目统一使用最长推理。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 附加路由指令并生成模式标记

在每个提示后追加“输出 `$\mathrm{NoThink}$`、`$\mathrm{Short}$` 或 `$\mathrm{Long}$`”的指令；模型将第一个响应词作为路由标记。训练初期的预热阶段强制每个组包含各模式的 rollout，使路由位置从第一步就获得梯度；预热后则由策略自由采样。

<div class="method-step__io" markdown="1">

**输入**：一批问题提示 `$\{q\}$`、当前策略 `$\pi_\theta$`，以及运行时路由指令。<br>
**输出**：每个问题对应一组响应，以及每个响应的路由模式 `$m_i\in\{\mathrm{NoThink},\mathrm{Short},\mathrm{Long}\}$`。

</div>

**直观理解**：这一步像让模型在答题前先选择“速答、简短思考还是充分思考”三档模式。预热时人为安排三种选择，避免模型一开始只会使用原来熟悉的单一推理方式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行模式相关的推理预算

对 `$\mathrm{NoThink}$` 设置 $1{,}024$ 个令牌上限，对 `$\mathrm{Short}$` 设置 $3{,}000$ 个令牌上限，`$\mathrm{Long}$` 不设上限；若最终答案令牌超过所选模式的上限，则该响应无论内容如何都判为错误。

<div class="method-step__io" markdown="1">

**输入**：带有路由标记的响应，以及三种模式的令牌上限。<br>
**输出**：满足模式预算约束的响应及其推理长度 `$L_i$`；超出上限的响应被标记为无效答案。

</div>

**直观理解**：硬上限让三种模式真正产生不同的行为：短模式不能悄悄变成长模式，长模式也始终保留处理困难问题的能力。同时，短模式生成的令牌更少，可降低训练期间的计算开销。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算奖励并形成组内学习信号

正确响应按照模式基础奖励和逐令牌折扣计算奖励；错误但路由有效的响应得 `$0$`，缺失路由标记的响应得 `$-0.5$`。对同一问题的一组响应进行均值中心化而不进行标准差归一化，即使用奖励相对组均值的差异作为主要优势信号；随后对过度代表或代表不足的模式加入平衡修正，并仅在与正确性方向一致时作用于错误或正确响应。

<div class="method-step__io" markdown="1">

**输入**：每个响应的模式、正确性、推理长度 `$L_i$` 和路由标记有效性。<br>
**输出**：每个响应的奖励 `$r_i$` 和修正后的优势估计 `$\hat A_i$`。

</div>

**直观理解**：模型不是只看“答对还是答错”，还比较同一道题中不同路由选择的相对收益。去掉标准差除法，是为了防止全都答对时由极小的长度差异被放大成强烈的错误学习信号。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 使用 GRPO 更新策略

计算当前策略相对于旧策略的令牌级重要性比率，并对策略更新使用裁剪的 GRPO 代理目标；本文将 KL 惩罚系数设为 `$\beta=0$`，因此不把当前策略锚定在参考模型上。损失使用 token-mean 聚合，即按所有响应令牌总数平均，而不是先对每个响应求均值再对响应求均值。

<div class="method-step__io" markdown="1">

**输入**：旧策略生成的响应、修正后的优势 `$\hat A_i$`、当前策略 `$\pi_\theta$` 及响应令牌概率。<br>
**输出**：更新后的策略 `$\pi_\theta$`，能够根据问题难度学习选择不同推理模式。

</div>

**直观理解**：这一步让高优势响应更可能被模型复现，让低优势响应更少出现。token-mean 使长、短响应中的每个令牌具有相同权重，避免长推理因为令牌多而被系统性削弱。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### GRPO裁剪代理目标

$$
J_{\mathrm{GRPO}}(\theta)=\mathbb{E}\left[\frac{1}{G}\sum_{i=1}^{G}\frac{1}{N_i}\sum_{t=1}^{N_i}\left(m_{i,t}-\beta D_{\mathrm{KL}}\right)\right],\quad m_{i,t}=\min\left(\rho_{i,t}A_i,\operatorname{clip}(\rho_{i,t},1-\epsilon,1+\epsilon)A_i\right),\quad \rho_{i,t}=\frac{\pi_\theta(o_{i,t}\mid q,o_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(o_{i,t}\mid q,o_{i,<t})}
$$

**符号说明**

- $\theta$：当前策略的参数。
- $\theta_{\mathrm{old}}$：采样这些响应时使用的旧策略参数。
- $q$：输入问题或提示。
- $G$：同一问题采样的响应组大小。
- $o_i$：第 $i$ 个响应，$o_{i,t}$ 是其第 $t$ 个令牌。
- $N_i$：第 $i$ 个响应的令牌数。
- $A_i$：第 $i$ 个响应的组内优势；本文在实际设计中对其使用均值中心化且不做标准差归一化。
- $\rho_{i,t}$：当前策略与旧策略在令牌 $o_{i,t}$ 上的概率比。
- $\epsilon$：概率比的裁剪阈值，用于限制单次策略更新幅度。
- $D_{\mathrm{KL}}$：当前策略与参考策略之间的 KL 散度。
- $\beta$：KL 惩罚强度；本文设为 $0$。
- $m_{i,t}$：裁剪后的令牌级策略优化项。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标提高高优势响应中相关令牌的概率，同时限制新旧策略差异过大。论文将 KL 项关闭，使模型可以探索原始模型较少产生的快速作答和提前停止行为；外层采用 token-mean 时，则需要把所有响应令牌放在同一总和中统一平均，而不是让每条响应先获得相同权重。<br>
**原文位置**：Preliminaries, Eq. (2), 以及 Loss Aggregation 小节

</div>

</div>

<div class="equation-block" markdown="1">

#### 按模式的正确答案奖励

$$
r_i=\begin{cases}b_{\mathrm{NT}}\gamma_{\mathrm{NT}}^{L_i},&\text{correct, NoThink},\\ b_{\mathrm{S}}\gamma_{\mathrm{S}}^{L_i},&\text{correct, Short},\\ b_{\mathrm{L}},&\text{correct, Long},\\ 0.0,&\text{incorrect, valid routing},\\ -0.5,&\text{routing token absent}.\end{cases}
$$

**符号说明**

- $r_i$：第 $i$ 个响应获得的标量奖励。
- $b_{\mathrm{NT}}$：NoThink 模式的基础正确奖励，默认值为 $1.3$。
- $b_{\mathrm{S}}$：Short 模式的基础正确奖励，默认值为 $1.2$。
- $b_{\mathrm{L}}$：Long 模式的基础正确奖励，默认值为 $1.0$。
- $\gamma_{\mathrm{NT}}$：NoThink 模式的逐令牌长度折扣因子。
- $\gamma_{\mathrm{S}}$：Short 模式的逐令牌长度折扣因子。
- $L_i$：第 $i$ 个响应在路由标记之后生成的令牌数。

<div class="equation-explanation" markdown="1">

**直观理解**：奖励同时编码答案质量、所选模式和计算成本。短模式虽然基础奖励较高，但长度增加会降低奖励；长模式正确时保持稳定奖励，因此模型只有在额外推理确实有助于解决困难问题时才有动力选择 Long。<br>
**原文位置**：Method, Reward Surface 小节, Eq. (5)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标是最大化裁剪的 GRPO 目标。对每个问题，策略采样一组响应并依据奖励计算相对优势；优势为正的响应会提高其令牌概率，优势为负的响应会降低其令牌概率。本文将 `$\beta$` 设为 `$0$` 以移除 KL 约束，并采用 token-mean 聚合 `$L_{\mathrm{TM}}=\frac{1}{\sum_iN_i}\sum_i\sum_t\ell_{i,t}$`，使每个令牌而非每条响应获得相同权重。模式平衡修正直接加入优势，因此它与准确性奖励共同进入策略梯度，而不是作为独立的辅助负载均衡损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 三模式自路由器与硬令牌上限**

模型通过响应首个路由标记选择 `$\mathrm{NoThink}$`、`$\mathrm{Short}$` 或 `$\mathrm{Long}$`。三种模式分别对应无显式强制跳过、短推理上限和无上限长推理；缺失路由标记会受到负奖励。模式选择不需要数据预处理，路由标记作为响应头中的普通令牌参与梯度更新。

> 直观理解：路由器相当于一个先做预算决策的控制器。硬上限保证“短思考”确实短，也保证困难题不能被短模式无限拖长来规避模式差异。

**2. 按模式和长度设计的奖励曲面**

正确答案的模式基础奖励设为 `$b_{\mathrm{NT}}=1.3$`、`$b_{\mathrm{S}}=1.2$`、`$b_{\mathrm{L}}=1.0$`；NoThink 和 Short 的奖励分别乘以长度折扣 `$\gamma_{\mathrm{NT}}^{L}$` 与 `$\gamma_{\mathrm{S}}^{L}$`，Long 的正确奖励保持为 `$1.0$`。折扣被设定为使 NoThink/Short 的交叉长度约为 `$800$`，Short/Long 的交叉长度约为 `$3000$`，从而不同模式在不同长度区间具有奖励优势。

> 直观理解：短模式起始奖励较高，但思考越久扣分越多；长模式起始奖励较低，却不会因继续思考而下降。因此简单题倾向速答，稍难题倾向短推理，真正困难的题才值得使用长推理。

**3. 去标准差归一化与模式平衡**

标准 GRPO 将组内奖励减均值后再除以组内标准差；本文只保留均值中心化，以避免折扣奖励在“所有回答都正确”的组中制造微小差异并被标准差放大。之后加入目标模式比例 `$p^\star=1/3$` 的平衡修正：模式实际占比高于目标时降低其优势，低于目标时提高其优势；为不扭曲答案正确性，负修正只作用于错误响应，正修正只作用于正确响应。

> 直观理解：如果一组回答全都正确，模型不应因为某个回答稍长就被强烈鼓励改变策略。平衡项像轻微的“交通调度”，防止所有流量拥堵在一个模式，但不会奖励错误答案或惩罚正确答案。

**训练与推理**

训练时，对每个问题先追加路由指令，再在预热阶段强制各模式产生指定数量的响应、其余响应自由采样；预热结束后全部响应自由生成。系统识别首个响应词、执行相应硬上限，依据答案正确性、长度和路由有效性计算奖励，对组内奖励做均值中心化，加入模式平衡修正，最后以 GRPO 更新策略。推理时，模型面对新问题生成一个路由标记并按该模式继续回答：NoThink 使用短预算，Short 使用不超过其上限的简短推理，Long 使用不设上限的长推理；所选模式由模型自身决定，而非由外部难度标签指定。

**复现信息**

复现或解读结果时需要特别区分三种长度：$L_i$ 是路由标记之后的生成令牌数，模式上限在生成过程中执行，超限响应直接按错误计分。默认上限为 NoThink 的 $1{,}024$ 和 Short 的 $3{,}000$，Long 不设上限；默认基础奖励为 `$b_{\mathrm{NT}}=1.3$`、`$b_{\mathrm{S}}=1.2$`、`$b_{\mathrm{L}}=1.0$`，目标模式比例为 `$p^\star=1/3$`。论文摘录未明确报告折扣因子、平衡系数、预热步数及其他优化器超参数的具体数值；这些参数不能由本节推断。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MATH-lighteval 竞赛数学题训练划分：题目具有可验证的最终答案，用于训练路由策略；MATH-500 作为同分布留出验证集，在温度 $0.6$ 下评估。答案与参考答案匹配时奖励为 $r=1$，否则为 $r=0$。
- GSM8K：包含 $1{,}319$ 道小学数学文字题，用于较容易的分布外测试，采用 $5$ 次采样的平均准确率（avg@5）。
- AIME 2024 与 AIME 2025：每年 $30$ 道竞赛数学题，用于较困难的分布外测试，采用 $16$ 次采样的平均准确率（avg@16）；Countdown 仅用于补充性的二元路由预备研究，原文未报告其主体结果。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率**

最终答案是否匹配参考答案的比例；在数学任务中衡量解题正确性。 （越高越好，但不能脱离响应长度单独解释，因为更长的推理通常消耗更多测试时计算。）

</div>
<div class="metric-item" markdown="1">

**平均响应长度**

生成回答使用的平均 token 数，作为测试时计算成本的近似指标。 （在准确率相近时越低越好；理想方法应在准确率—长度平面上更靠左上方。）

</div>
<div class="metric-item" markdown="1">

**路由熵**

自由生成时三种模式分布的不确定性，反映策略是否保留多种模式，而不是总选择同一模式。 （在需要多模式协作时，较高且稳定的熵通常更好；但熵高本身不证明路由依据了题目难度。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### MATH-500 同分布验证：自由路由与固定预算方法的准确率—长度权衡

<div class="result-value" markdown="1">

自由路由在第 $90$ 步达到 $0.783$ 的准确率，平均响应长度为 $2{,}811$ token；相较未训练基础模型的 $4{,}796$ token，长度减少 $41\%$。在准确率—长度平面上，自由路由严格位于三种单模式基线形成的 Pareto 前沿之上；达到相同准确率时，该固定预算前沿需要多 $27\%$ 的 token。

</div>

作者的核心结论是，路由器并非只把准确率换成更短回答，而是按题目分配不同预算，使整体效率曲线外移。它仍略低于未训练基础模型的准确率，因此不能据此宣称路由提高了绝对解题能力；更稳妥的结论是，在接近基础模型准确率的情况下显著节省 token。

<div class="result-source" markdown="1">

来源：Experimental Results，Table 2 与 Figure 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Accuracy does not rise above the base model: it dips while routing is being established and recovers to 0.783 by step 90, close to the untrained model’s 0.807.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### GSM8K 分布外评估：较容易题目的自适应预算

<div class="result-value" markdown="1">

在 GSM8K 上，自由路由严格高于单模式基线形成的 Pareto 前沿；达到相应准确率时，比该前沿少使用 $44\%$ 的 token，比基础模型少使用 $76\%$ 的 token。该结果说明，在题目难度差异较大且总体偏容易的数据上，路由能把更多样本交给短模式，同时保留必要的长推理。

</div>

这一结果支持路由机制具有跨数据集的可迁移性，而不只是记住 MATH-500 的题型。由于 GSM8K 的具体方法分数和长度点主要呈现在图中，正文给出的百分比只能说明相对节省，不能单独推出某个方法在所有准确率区间都占优。

<div class="result-source" markdown="1">

来源：Token Efficiency, In and Out of Distribution，Figure 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On GSM8K, dominated by easy problems, free routing again lies strictly above the frontier: its slightly exceed the accuracy of the brief fixed modes at comparable length, using 44% fewer tokens than the frontier requires to reach its accuracy and 76% fewer than the base.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### AIME 2024/2025 分布外评估：高难度题目是否会被错误地截短

<div class="result-value" markdown="1">

在 AIME 上，自由路由与固定预算前沿的准确率相当，同时比基础模型短 $12\%$；由于 AIME 题目普遍需要较长推理，路由器没有大幅削减预算，而是更多保留 Long 模式。

</div>

该结果检验了路由器是否会对所有任务机械地追求短回答。作者的解释是，面对几乎都需要长推理的高难度题目，策略会保留较大预算，因此自适应机制表现为“该省时省、该花时花”。不过，AIME 每年只有 $30$ 道题，使用 avg@16 是为了降低单次采样噪声，结果仍应谨慎解读。

<div class="result-source" markdown="1">

来源：Token Efficiency, In and Out of Distribution，Figure 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On AIME, where nearly all problems require extended reasoning, the router correctly declines to cut budget: it matches the frontier’s accuracy at comparable length, still 12% shorter than the base.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验只覆盖一个 $1.5$B 数学推理模型、一个数学训练分布和三个随机种子；因此不能据此断言该机制对更大模型、非数学任务、代码生成或工具使用同样有效。
- 模式长度上限是任务相关的，并且验证时采用不截断生成，短模式的准确率可能相对于训练目标略显乐观；不同任务需要重新匹配模式上限，且原文未报告逐项移除平衡项、warmup 或长度约束的独立消融。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 未训练的 Base：在路由提示下直接使用基础模型，用于衡量训练是否损害或改善原始准确率与响应长度。
- Long-only：所有样本都强制使用长推理模式，代表较大固定推理预算，也检验训练后的完整推理能力。
- Short-only：所有样本都强制使用短推理模式，代表中等固定预算。
- NoThink-only：所有样本都强制快速作答，代表最小固定预算；三种单模式模型使用相同数据与超参数，但移除路由标记、平衡项和自由路由采样。

**实验想回答的问题**

- 三种推理模式能否在 GRPO 中端到端稳定学习，并避免路由策略塌缩到单一模式？
- 路由器是否依据题目难度分配推理预算，并在同分布与分布外数据上相对于固定推理预算实现更好的准确率—长度权衡？

**实验实现**

基础模型为 DeepSeek-R1-Distill-Qwen-1.5B，即由 DeepSeek-R1 蒸馏得到的 $1.5$B 参数推理模型。训练使用 GRPO，组大小为 $G=8$，从冷启动训练 $90$ 步，最大上下文长度为 $16{,}384$ token，在 $4$ 张 NVIDIA H100 GPU 上运行。路由器为每道题输出一个模式标记：NoThink、Short 或 Long；随后生成受到对应模式的长度上限约束，使路由标记与实际推理行为保持一致。训练了三个随机种子，并对路由器和每个单模式基线报告均值与标准差。验证时不限制生成长度，以测量自由生成状态下的实际生产行为。实验同时记录自由路由模式分布、路由熵、各模式准确率及平均响应长度，并以三种单模式基线形成固定预算的 Pareto 前沿。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 单模式强制基线：NoThink-only、Short-only 与 Long-only | 在 MATH-500 上，NoThink-only 为 $0.66$ 准确率、$1{,}096$ token；Short-only 为 $0.72$、$2{,}030$ token；Long-only 为 $0.80$、$4{,}507$ token；自由路由为 $0.78$、$2{,}811$ token。 | 该对照把“固定推理预算”和“按题目分配预算”区分开来。Long-only 具有最高的单模式准确率但成本较高，NoThink-only 最省 token 但准确率最低；自由路由用中等平均长度接近 Long-only 的准确率，说明收益来自样本级预算分配，而不是某一个固定模式本身。它不能证明自由路由在绝对准确率上优于 Long-only。 | Figure 6<br><span class="experiment-evidence">Free routing (ours)  0.78 @ 2,811</span> |
| 路由训练过程与模式塌缩检查 | 训练早期自由路由几乎不产生有效路由标记；放开自由路由后模型一度偏向 Long，随后短模式增加，至第 $90$ 步约为 $20\%/32\%/47\%$，且路由熵约为 $1.04$，接近 $\ln 3\approx1.10$。 | 这是对训练稳定性而非最终准确率的消融式诊断。它表明强制 warmup、模式平衡项和按模式限制长度共同帮助三种模式存活。由于这些机制没有分别逐项移除，实验只能支持“组合设计有效”，不能确定其中哪一个组件单独贡献最大。 | Three Modes Emerge and Persist，Figure 3<br><span class="experiment-evidence">Once routing is free the model at first commits heavily to Long, then the brief modes grow as the balance term takes effect, and by step 90 the split settles near 20/32/47% (NoThink/Short/Long), with routing entropy close to the theoretical maximum (H≈1.04 vs. ln 3≈1.10).</span> |

**定性案例**

- 按 MATH-500 难度等级观察的路由分层是最具解释性的案例：最容易的 Level 1 主要分配给 NoThink，最困难的 Level 5 更多分配给 Long，Short 在中间难度占比最高，且各等级准确率随难度升高而下降。它说明模式标签大体对应“需要多少推理”，但这是群体统计证据，不代表路由器能对每一道题准确识别难度。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：研究语言模型在测试时自适应分配计算量以及何时进行更深入推理。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`ff996b930246f4b525710310633b07440803e4f8a02a8a327c0d9f0cc4b1db64`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
