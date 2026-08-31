---
title: "[论文解读] Learning to Use Tools: Reinforcement Learning for Tool-Integrated Mathematical Reasoning"
description: "[arXiv 2608.28447][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.28447"
announcement_date: "2026-08-31"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:36:21.591850+00:00"
source_sha256: "1c8c44327653826f7a0f627253fbf2aa9a350bf9c9d9824d42f0a00ede4d44c7"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "LLM 其他"
  - "工具增强大语言模型"
  - "数学推理"
  - "Countdown"
  - "计算器调用"
  - "监督微调"
  - "可验证奖励强化学习"
  - "在线强化学习"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.28447</p>

# Learning to Use Tools: Reinforcement Learning for Tool-Integrated Mathematical Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Minghui Xu, Zi Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Department of Energy Science and Engineering；Affiliation: Stanford University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28447v1) · [PDF 下载](https://arxiv.org/pdf/2608.28447v1) · **关键词** 工具增强大语言模型, 数学推理, Countdown, 计算器调用, 监督微调, 可验证奖励强化学习, 在线强化学习<br>


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

本文属于工具增强的大语言模型数学推理研究。大语言模型通常通过自回归生成中间推理步骤，但逐词生成本身并不提供可靠的精确计算或结果校验机制，因此在多步算术中容易出现计算错误和逻辑偏离。本文将外部计算器接入模型生成过程：模型在推理中以规定格式发出工具调用，计算器执行表达式并返回结果，模型再依据该观察继续推理或验证答案。研究对象是 Countdown 任务，因为该任务同时要求组合搜索、算术运算和最终答案验证，且答案可由程序自动检查，适合研究监督微调（SFT）与基于可验证奖励的在线强化学习（RL）。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**工具增强推理**

工具增强推理指模型在生成自然语言推理时，调用外部程序完成自身不擅长或需要可靠验证的操作，例如精确计算。本文中模型输出被工具标签包围的计算表达式，环境执行后返回观察结果，模型据此继续生成。

</div>
<div class="concept-item" markdown="1">

**监督微调与在线强化学习**

监督微调使用预先构造的示范答案训练模型学习工具调用格式和推理模式。在线强化学习则让当前模型生成多条轨迹，并依据最终答案是否正确计算奖励，再提高高奖励轨迹的生成概率；本文使用的奖励可以由 Countdown 验证器自动计算。

</div>
<div class="concept-item" markdown="1">

**Countdown 任务与 pass@k**

Countdown 要求模型使用给定数字和允许的算术运算得到目标值，通常需要同时决定运算顺序和中间计算。pass@k 表示从同一问题生成最多 $k$ 个答案时至少有一个正确答案的比例，因此 $pass@1$ 更接近单次回答能力，而较大的 $k$ 还反映模型是否能够探索到正确轨迹。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个 Countdown 问题，包括一组可用数字和一个目标值，模型需要生成由算术运算组成的推理过程，并输出满足任务约束且等于目标值的最终答案。无工具模型直接完成符号推理和数值计算；工具增强模型可以在生成过程中输出置于 <tool>…</tool> 标签内的计算表达式，环境执行该表达式后插入 <obs> 观察结果，模型再基于该结果继续推理。训练阶段包括无工具和工具格式的 SFT 基线，以及 RLOO、RLOO++、GRPO 和 DAPO 等在线 RL 方法；评价阶段使用公开的 50 道测试题和新构造的 1,024 道无训练集精确重叠的保留题。最终答案由 Countdown 验证器自动判定，以便把答案正确性转化为训练或评估信号。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

一个 Countdown 输入问题，包含给定数字、目标值及其任务约束。

</div>
<div class="notation-item" markdown="1">

**$y$**

模型针对输入 $x$ 生成的完整输出或推理轨迹，包括自然语言步骤、可能的工具调用和最终答案。

</div>
<div class="notation-item" markdown="1">

**$r$**

由自动验证器根据最终答案是否满足 Countdown 规则和目标值而得到的奖励；文中 RL 主要使用最终答案奖励。

</div>
<div class="notation-item" markdown="1">

**$k$**

pass@k 中允许针对同一输入采样的候选答案数量；只要其中一个正确，该输入就计为成功。

</div>

</div>

**直接相关的工作**

- **ReAct（Yao et al., 2023）**: ReAct 将自然语言推理与外部行动交替组织，为本文的“推理—工具调用—观察—继续推理”交互形式提供直接背景。本文进一步把计算器调用纳入 Countdown 的训练和在线 RL 流程，并研究工具格式 SFT 与多种 RL 方法对最终数学正确性的影响。
- **RLOO（Ahmadian et al., 2024）**: RLOO 是本文采用的在线强化学习基线之一，利用同一输入生成的多条样本进行相对奖励比较，并避免训练单独的价值模型。本文将其与 RLOO++、GRPO 和 DAPO 一起应用于工具增强策略，以比较不同可验证奖励 RL 方法在 Countdown 上的效果。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

多步数学推理不仅要求模型找到可行的运算组合，还要求每一步数值计算和最终答案准确。现有大语言模型主要依赖自回归生成中间推理步骤，缺少可靠的外部计算与验证机制，因此容易在复杂运算中产生算术错误或沿着错误结果继续推理。Countdown任务集中体现了这一问题：模型必须使用给定数字和算术运算得到目标值，而答案又可以由验证器自动检查，适合研究工具调用能否提升数学推理可靠性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **无工具的链式推理与监督微调**：模型直接生成包含中间步骤的数学推理轨迹，并通过监督微调学习示例中的解题格式和推理模式。它依靠模型自身完成计算和检查，不在生成过程中调用外部计算器。
- **基于最终答案奖励的在线强化学习**：模型针对同一问题采样多条推理轨迹，再根据Countdown验证器是否判定最终答案正确来计算奖励，并用RLOO、RLOO++、GRPO或DAPO等策略提高高奖励轨迹的生成概率。工具增强版本允许模型生成被<tool>标签包围的表达式，由环境执行后以<obs>形式返回结果，模型再据此继续推理。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 无工具推理把精确计算交给语言模型的逐词生成过程，缺少显式的数值验证环节；一旦中间步骤出现算术错误，模型可能基于错误结果继续推理，最终导致答案错误。
- 仅依赖最终答案的强化学习能够区分正确与错误结果，却不直接监督模型何时调用工具、如何理解工具返回值或如何形成有效推理轨迹；此外，当某个问题的一组采样轨迹中没有任何正确解时，模型缺乏正向学习信号，因而难以发现原本尚未采样到的正确方案。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚不清楚计算器工具的系统化训练方式能否与多种在线强化学习方法稳定结合，以及在只有最终答案可验证、没有逐步过程奖励的条件下，强化学习是否仍能学会更有效的工具调用和结果利用。现有问题因此不是单纯比较“使用工具”与“不使用工具”的准确率，而是需要建立从工具格式监督、在线交互到自动验证评测的完整流程，并在无训练集精确重叠的测试问题上检验工具和强化学习各自的作用。

</div>
<div markdown="1"><span>核心问题</span>

在Countdown数学推理中，若先通过监督微调使模型掌握计算器调用及其返回结果的解释，再使用仅依据最终答案正确性的在线强化学习，是否能够相较于无工具基线和工具监督微调基线，提升模型生成正确推理轨迹与最终答案的概率；不同强化学习方法在这一工具集成设置下是否表现出稳定差异？

</div>
<div markdown="1"><span>作者直觉</span>

计算器可以把模型不擅长的精确数值运算交给外部执行器，使模型能够核对中间结果并减少算术和验证错误；监督微调则先教会模型以正确格式调用工具并读取返回值。此后，强化学习即使只看到最终答案奖励，也可以通过反复采样逐渐提高那些同时包含有效工具使用和正确推理的轨迹概率。换言之，工具负责提供可靠的计算反馈，强化学习负责重新分配模型对不同推理路径的偏好，二者可能形成互补。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法针对 Countdown 数学推理任务，将计算器作为模型可调用的外部工具，并比较监督微调与多种在线强化学习方法。输入是包含目标数值和目标结果的题目，模型先生成自然语言推理或算式，需要时输出工具调用；环境执行计算器并返回观测，模型再依据观测完成最终答案。训练阶段使用自动验证器仅检查最终表达式是否有效、是否恰好使用给定数字且计算结果等于目标，因此不需要人工逐步标注。整体方法先用错误分析构造 Tool-SFT 数据，再以 Tool-SFT 模型为初始策略进行 Tool-RLOO、Tool-RLOO++、Tool-GRPO 或 Tool-DAPO 训练；推理时则重复生成推理、调用计算器、读取结果和输出答案的过程。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 识别任务与计算错误

检查每条推理是否包含错误算术步骤；若有，则截取错误之前的上下文并纠正该数值；若最终答案错误但没有明确算术错误，则保留完整推理，并加入能够暴露错误的计算器检查。正确样本则保留原始推理，后续附加确认性计算器调用。

<div class="method-step__io" markdown="1">

**输入**：原始 Countdown 题目、原始 SFT 数据 $\mathcal{D}$ 以及其中的模型推理和答案。<br>
**输出**：带有纠错前缀、错误检查或确认性检查的训练样本候选。

</div>

**直观理解**：先找出模型究竟在哪一步算错，而不是只告诉它最后答案错了。这样可以把计算器放在最有帮助的位置，类似老师在学生出错处要求其重新验算。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 构造 Tool-SFT 数据

为每个纠错前缀从 SFT 参考模型采样 $K$ 个后续推理；选择答案正确的最短后续，若没有正确样本则使用精确求解器答案。将工具调用 `<tool>expression</tool>` 和环境返回的 `<obs>value</obs>` 插入原推理与后续推理之间，形成工具增强数据集 $\mathcal{D}^{\prime}$。

<div class="method-step__io" markdown="1">

**输入**：纠错前缀、训练好的 SFT 参考模型 $\pi$、每个前缀的采样数 $K$，以及计算器工具格式。<br>
**输出**：Tool-SFT 训练集，以及用于小规模监控的留出集；模型学习何时调用计算器、如何读取返回值并继续推理。

</div>

**直观理解**：这一步像制作示范题：示范不仅展示正确解法，还明确演示“把算式交给计算器—读取结果—继续解题”的操作顺序。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 训练工具调用策略

采用 RLOO、RLOO++、GRPO 或 DAPO 进行在线强化学习；模型生成工具调用和推理，环境执行工具并返回观测，验证器根据最终答案给出自动奖励。策略更新只作用于模型生成的 token，工具观测被视为环境输出而不作为模型动作；DAPO 额外进行组内奖励归一化、过滤全对或全错的样本组，并使用非对称概率比裁剪。

<div class="method-step__io" markdown="1">

**输入**：Tool-SFT 模型、Countdown 题目、在线生成的多条候选轨迹、计算器环境和最终答案验证器。<br>
**输出**：能够在最终答案奖励驱动下提高正确率，并更有效安排计算器调用的 Tool-RL 策略。

</div>

**直观理解**：模型不需要逐步获得人工反馈，只要一题做对就得到高奖励；在多次尝试中，强化学习逐渐提高那些更常导致正确答案的推理和工具使用行为的概率。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 工具辅助推理与答案验证

策略生成推理文本；当需要确认中间算术时输出工具调用，环境执行表达式并返回观测，策略根据观测继续生成，直到输出 `<answer>...</answer>` 中的最终表达式。验证器检查表达式语法、数字使用约束和目标值是否同时满足，并据此计算 pass@k。

<div class="method-step__io" markdown="1">

**输入**：新 Countdown 题目 $q$、训练后的策略和可执行计算器。<br>
**输出**：最终答案及其是否通过严格验证的结果；多次采样时得到 $k$ 条候选并统计至少一条正确的比例。

</div>

**直观理解**：推理阶段像带有计算器的解题者：计算器负责可靠算数，模型负责选择算什么、理解结果以及组织完整答案，最后由程序统一判分。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### RLOO 策略优化目标

$$
\mathcal{L}=-\mathbb{E}\left[w(y_i,x)A_i\log\pi_{\theta}(y_i\mid x)\right]-\beta_{\mathrm{ent}}\mathcal{H}(\pi_{\theta})+\beta_{\mathrm{KL}}D_{\mathrm{KL}}(\pi_{\theta}\,\|\,\pi_{\mathrm{ref}})
$$

**符号说明**

- $x$：输入题目或提示。
- $y_i$：针对题目 $x$ 采样得到的第 $i$ 条完整模型响应。
- $\pi_{\theta}$：参数为 $\theta$、正在训练的策略。
- $\pi_{\mathrm{ref}}$：冻结的 Tool-SFT 参考策略，用于约束策略不要偏离初始模型过远。
- $A_i$：RLOO 留一法优势，即该响应奖励相对于同题其他响应平均奖励的相对表现。
- $w(y_i,x)$：经过裁剪的序列级重要性权重，用于校正采样策略与当前策略之间的差异。
- $\mathcal{H}(\pi_{\theta})$：策略熵，鼓励模型保留一定的探索性。
- $D_{\mathrm{KL}}(\pi_{\theta}\,\|\,\pi_{\mathrm{ref}})$：当前策略与参考策略之间的 KL 散度。
- $\beta_{\mathrm{ent}},\beta_{\mathrm{KL}}$：熵正则和 KL 约束的系数；文中 RLOO 设置二者均为 $10^{-3}$。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项提高高优势响应的生成概率，降低低优势响应的概率；熵项防止过早失去探索能力，KL 项则防止强化学习把模型推离已经学会工具格式的 Tool-SFT 策略太远。该目标把“最终答案是否正确”转化为对整条推理轨迹概率的调整。<br>
**原文位置**：第 3.2 节，RLOO overall training loss

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标分两层。Tool-SFT 通过最大化带工具调用示范的响应似然，使模型掌握调用计算器、读取观测和完成答案的格式；随后 Tool-RL 使用最终答案验证器产生的自动奖励，提升正确轨迹的概率。RLOO、RLOO++ 和 GRPO 主要通过组内相对奖励构造优势，DAPO 进一步只使用包含正确与错误混合结果的题目组，并以裁剪的 token 级策略目标更新模型；RLOO 还加入熵正则和相对于冻结 Tool-SFT 策略的 KL 约束。关键点是没有提供逐步推理奖励，因此工具调用的改进是由最终正确性间接诱导出来的，而不是由人工规定每一步何时调用工具。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 计算器环境与工具协议**

模型以 `<tool>expression</tool>` 生成工具动作，环境执行表达式并返回 `<obs>value</obs>`。在强化学习中，工具返回值不计入模型生成动作，策略损失仅作用于模型控制的推理和答案 token。

> 直观理解：工具协议把“调用计算器”和“看到计算结果”变成清晰的交互边界，避免模型把环境返回值当成自己生成的内容，也使训练信号更准确。

**2. 错误驱动的 Tool-SFT 数据构造**

算法 1 分为四阶段：从原始 SFT 数据建立纠错前缀；由参考策略采样后续；插入计算器调用并选择正确续写；最后划分训练集和监控留出集。错误样本优先使用正确续写，正确样本附加确认性计算，以同时教授纠错和验证模式。

> 直观理解：数据不是随机加入工具示例，而是针对模型常见的算术错误放置工具，因此模型学习的是“什么时候验算最有用”，而非机械地每一步都调用计算器。

**3. 在线强化学习更新**

RLOO 使用同一题目的其他采样答案作为留一法基线；RLOO++ 将优势在整个 batch 上归一化；GRPO 使用组内奖励估计优势并采用 token 级重要性权重；DAPO 在此基础上过滤奖励全同的组，并使用上下界分别为 $1-0.2$ 与 $1+0.28$ 的非对称裁剪。

> 直观理解：多种 RL 方法都比较同一道题的不同尝试，但比较方式不同。DAPO 丢掉无法区分好坏的题目组，把训练资源集中在“有的尝试对、有的尝试错”的信息丰富样本上。

**训练与推理**

训练时，先从原始 SFT 数据中定位算术错误，构造纠错前缀，并从参考 SFT 模型采样后续；正确样本附加确认性计算器调用，错误样本选择正确续写或精确求解器答案，形成 Tool-SFT 数据。之后以 Tool-SFT checkpoint 初始化 RL 策略，对每个题目采样一组轨迹；轨迹中的工具调用由环境执行，最终表达式由自动验证器判定，奖励用于 RLOO、RLOO++、GRPO 或 DAPO 更新。推理时，模型从题目开始生成推理，需要计算时暂停并调用计算器，读取观测后继续生成，最终输出带 `<answer>` 标签的表达式；验证器要求表达式语法正确、恰好使用给定数字且值等于目标。若进行 pass@k 评估，则对同一题采样 $k$ 次，并判断至少一次通过验证的比例。

**复现信息**

所有 RL 实验使用单张 H100；策略初始于 SFT checkpoint，batch size 为 $128$，group size 为 $8$，学习率为 $1\times10^{-5}$，最大生成长度为 $1024$ token，最大模型长度为 $2048$。工具 rollout 的最大交互轮数为 $10$；RLOO 和 Tool-RLOO 的训练预算分别比较 $100$ 步与 Tool-RLOO 的延长 $200$ 步设置，文中还指出 Tool-GRPO 在约第 $35$ 步后显著偏离 SFT，因此采用第 $30$ 步 checkpoint。实现上需要特别注意，工具观测不参与策略损失，且不同 RL 方法的裁剪、优势归一化和 KL 设置不同；这些设计差异会影响方法间的公平解释。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Countdown 训练数据用于 SFT 与在线强化学习。每道题给出一个目标值以及三个或四个数字；最终表达式必须恰好使用每个给定数字一次，并通过允许的算术运算得到目标值。原文节选未明确报告训练集规模及三数字、四数字题目的比例。
- 作者新建的 1,024 题 held-out Countdown 测试集是主要评测集。它与训练数据在键 $(\text{target},\text{sorted(numbers)})$ 上没有完全重合，用于以较低统计不确定性评估同分布但未重复的新题。
- 原始公开测试集仅有 50 题，作为补充评测集。它可用于与既有设置衔接，但样本过少，特别是在较大的 $k$ 下置信区间较宽，不适合据此判断细微方法差异。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**pass@$k$**

对每道题采样 $k$ 个回答，只要至少一个回答满足最终表达式格式、恰好使用每个给定数字一次，并且计算结果等于目标值，就记为通过。该指标同时反映单次成功概率和多次采样后的解题覆盖率。 （越高越好，因为它表示模型在给定采样预算内找到至少一条正确推理轨迹的题目比例更大；但较大的 $k$ 容易趋于饱和，不能等同于单条回答质量同步提高。）

</div>
<div class="metric-item" markdown="1">

**95% bootstrap confidence interval**

以题目实例为重采样单位计算的自助法置信区间，用来表示 pass@$k$ 估计的不确定性，而非额外的准确率指标。 （区间越窄通常表示估计越稳定；比较方法时还需观察区间重叠，不能只比较点估计。）

</div>
<div class="metric-item" markdown="1">

**错误类型比例**

将错误回答分为推理轨迹中的计算错误、目标或规划错误，以及最终答案中的数字使用或格式等有效性错误；计算错误与规划错误可以同时出现。 （各类错误比例越低越好。该诊断指标用于判断工具主要可能修复哪类问题，而不是替代最终正确率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 在 1,024 题新 held-out 测试集上，将 no-tool SFT 与 no-tool RLOO、Tool-SFT 与 Tool-RLOO 分别比较。

<div class="result-value" markdown="1">

作者报告，RLOO 将无工具模型的 pass@1 从 26.4% 提高到 50.6%，并将工具模型的 pass@1 从 35.8% 提高到 56.6%。这说明在两种接口条件下，仅依靠可验证最终答案奖励进行在线强化学习，都显著提高了单次采样得到正确解的概率。

</div>

通俗地说，强化学习不是只让模型“多试几次”，而是让第一条采样轨迹更可能正确。由于这里同时比较了有工具和无工具版本，结果支持强化学习本身有效；但实验只覆盖 Countdown，不能直接推出相同幅度会出现在开放式数学证明或其他工具类型上。

<div class="result-source" markdown="1">

来源：第 5.2 节，Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

RLOO substantially improves over the SFT baseline at low k, increasing pass@1 from 26.4% to 50.6% without tool use and from 35.8% to 56.6% with tool use.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 在匹配训练预算以及延长 Tool-RLOO 训练两种条件下，比较无工具 RLOO 与 Tool-RLOO。

<div class="result-value" markdown="1">

匹配预算时，工具接入使 pass@1 从 50.6% 提高到 56.6%，pass@16 从 66.6% 提高到 74.0%；将 Tool-RLOO 延长至 200 步后，pass@1 达到 60.7%，pass@16 达到 76.5%。

</div>

工具不仅提高单次作答成功率，也扩大了 16 次采样内至少找到一个正确解的覆盖率，符合计算器减少算术和核验错误的解释。延长训练得到的 60.7% 不能与 50.6% 视为严格的纯工具消融，因为两者训练步数不同；更干净的工具效应是匹配预算下的 50.6% 对 56.6%。

<div class="result-source" markdown="1">

来源：第 5.2 节，Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

With a matched training budget, Tool-RLOO increases pass@1 from 50.6% to 56.6% and pass@16 from 66.6% to 74.0%. Extending Tool-RLOO training to 200 steps further improves performance to 60.7% pass@1 and 76.5% pass@16, corresponding to a roughly 10 percentage-point pass@1 gain over no-tool RLOO.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 在工具增强条件下比较 Tool-SFT、Tool-RLOO、Tool-RLOO++、Tool-GRPO 与 Tool-DAPO。

<div class="result-value" markdown="1">

Tool-DAPO 是作者报告的最强方法，pass@1 从 Tool-SFT 的 35.8% 提高到 66.0%；相对 Tool-RLOO，正文报告其 pass@1 再提高 9.3 个百分点，并且 pass@16 也有提升。

</div>

结果表明，过滤奖励无差异的样本组后，策略更新可能更集中于“同一题既采到正确答案也采到错误答案”的有信息样本，从而更有效地提高正确轨迹概率。不过正文节选没有给出 Tool-DAPO 的完整 pass@16 数值，而且不同算法的训练稳定性与实际训练步数并不完全一致，因此不能把差异全部归因于算法公式本身。

<div class="result-source" markdown="1">

来源：摘要；第 5.3 节的 Figure 4 与 Table 1 提供算法比较

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Our results show that calculator tool integration consistently improves both SFT and RL baselines, yielding roughly 10 percentage-point gains across pass@k. Among the RL methods, Tool-DAPO achieves the strongest performance, improving pass@1 from 35.8% for Tool-SFT to 66.0%.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原始公开测试集只有 50 题，较大 $k$ 下置信区间宽且大量重叠；因此细微的算法排序，尤其是该测试集上的 Tool-GRPO 表现，不应被过度解释。主要结论应以 1,024 题 held-out 集为准。
- 实验仅研究同一任务分布下的 Countdown 和计算器工具。新测试集虽然排除了按 $(\text{target},\text{sorted(numbers)})$ 定义的精确训练重合，但仍是同分布评测；结果尚不能证明模型能迁移到复杂证明、文字题、分布外数字组合或其他外部工具。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- no-tool SFT：模型直接生成推理轨迹和最终表达式，不调用计算器。它给出仅靠监督学习和模型内部计算能力时的基础水平。
- Tool-SFT：模型经过工具格式的监督微调，可在生成过程中发出计算器调用并读取返回结果。与 no-tool SFT 的比较主要检验工具接入本身的价值。
- no-tool RLOO：从无工具策略出发，使用可验证最终答案奖励进行在线强化学习。它与 Tool-RLOO 使用尽量匹配的强化学习超参数，可用于区分强化学习收益与实时工具执行收益。
- Tool-RLOO：同时采用计算器和 RLOO，是比较 RLOO++、GRPO、DAPO 等工具增强强化学习算法时的核心参照；它也用于判断更复杂的组采样或动态过滤机制是否带来额外收益。

**实验想回答的问题**

- 在 Countdown 算术推理中，允许模型实时调用计算器，能否在监督微调与强化学习两种训练阶段稳定提高正确率，尤其减少局部计算和验证错误？
- 在仅使用可自动验证的最终答案奖励时，RLOO、RLOO++、GRPO 与 DAPO 哪种在线强化学习方法最有效；性能差异是否与训练样本组的信息量及更新稳定性有关？

**实验实现**

评测时，每道题采样 $k$ 个响应，并由可执行规则检查 `<answer>…</answer>` 中的表达式是否恰好使用全部给定数字一次、是否仅采用允许的运算以及是否得到目标值。工具模型可在生成期间调用计算器并接收 observation，无工具模型则直接输出推理和答案。RLOO 与 Tool-RLOO 在未特别说明时匹配强化学习超参数、批大小、组大小、采样温度、熵系数和 KL 系数，主要变量是 rollout 时是否启用实时工具。所有置信区间均为按题目实例计算的 95% bootstrap 区间。作者还按三数字与四数字难度分析 SFT 错误，并比较 RLOO、RLOO++、GRPO 和 DAPO；节选未提供完整的采样 $k$ 列表、随机种子数量或多次独立训练方差。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 工具执行消融：在其余强化学习设置匹配时，对比 no-tool RLOO 与 Tool-RLOO。 | 启用实时计算器后，pass@1 从 50.6% 增至 56.6%，pass@16 从 66.6% 增至 74.0%。 | 该比较主要隔离 rollout 中工具执行的作用：模型可以把中间算术交给计算器并依据返回值继续推理。两个指标同时提高，说明收益不只是在多次采样时偶然找到答案；但工具版本此前还接受过工具格式训练，因此它隔离的是完整“工具能力栈”，而不只是一次 API 调用的瞬时作用。 | 第 5.2 节，Figure 3<br><span class="experiment-evidence">With a matched training budget, Tool-RLOO increases pass@1 from 50.6% to 56.6% and pass@16 from 66.6% to 74.0%.</span> |
| 动态样本组过滤分析：考察 Tool-DAPO 在更新前移除组内奖励零方差的全对或全错题组。 | 作者报告 60.7% 的生成题组被过滤；Tool-DAPO 用 100 步、6.29 小时达到高于延长版 Tool-RLOO 的 pass@1，而后者训练 200 步、耗时 16.15 小时。 | 这一设计提高了每个更新批次中有效偏好信号的密度，因为全对或全错组无法指出同题下哪条轨迹更值得强化。结果支持过滤机制有助于样本效率，但这不是只开关过滤组件的严格消融：DAPO 与 RLOO 还可能存在其他算法差异，过滤也带来额外重采样开销。 | 第 5.3 节；运行时间详见 Appendix B<br><span class="experiment-evidence">Although this filtering introduces additional resampling overhead, Tool-DAPO reaches higher pass@1 in 100 steps and 6.29 hours than the 200-step extended Tool-RLOO baseline, which requires 16.15 hours, as documented in Section B.</span> |

**定性案例**

- Appendix A 给出题目数字 $[99,11,46,48]$、目标 $44$ 的案例，参考解为 $(99-11)/(48-46)$。普通 RLOO 在 16 次采样中为 0/16，而 Tool-RLOO 为 4/16，说明计算器可能帮助模型核验中间量并保留可行轨迹。该例只能展示一种可能机制，不能单独证明总体增益或排除采样随机性。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper studies calculator tool use for mathematical reasoning and improves it through reinforcement-learning-based post-training.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`1c8c44327653826f7a0f627253fbf2aa9a350bf9c9d9824d42f0a00ede4d44c7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
