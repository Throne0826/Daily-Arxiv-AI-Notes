---
title: "[论文解读] FormalTCS: Benchmarking End-to-End Frontier Formal Theoretical Computer Science Research of Large Language Models"
description: "[arXiv 2608.20153][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.20153"
announcement_date: "2026-08-21"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-21T02:05:21.793250+00:00"
source_sha256: "2916c55a9e2aa8f5464b6b9b34ca2e4201a60ca9eaf55c5802e477fb756c041c"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "理论计算机科学"
  - "大型语言模型"
  - "端到端研究自动化"
  - "自动形式化"
  - "Lean"
  - "机器验证证明"
  - "前沿研究基准"
  - "定理证明"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.20153</p>

# FormalTCS: Benchmarking End-to-End Frontier Formal Theoretical Computer Science Research of Large Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-21</span>
<span><strong>作者</strong> Dingzirui Wang, Xuanliang Zhang, Keyan Xu, Qingfu Zhu, Wanxiang Che</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Harbin Institute of Technology</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.20153) · [PDF 下载](https://arxiv.org/pdf/2608.20153) · **关键词** 理论计算机科学, 大型语言模型, 端到端研究自动化, 自动形式化, Lean, 机器验证证明, 前沿研究基准, 定理证明<br>
**代码**: [https://github.com/zirui-HIT/FormalTCS](https://github.com/zirui-HIT/FormalTCS)

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

理论计算机科学（TCS）用数学方法研究计算的基本原理，涵盖计算模型、算法、计算复杂性、可计算性及其边界。本文关注大型语言模型（LLM）能否参与前沿 TCS 研究：不仅生成或证明已有定理，还要从论文中的自然语言核心结论出发，恢复相应的形式定义与定理，并完成可机器验证的证明。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大型语言模型（LLM）**

LLM 是从大规模文本中学习语言与推理模式的模型，可生成自然语言、数学表达式和程序。本文把它作为 TCS 研究流程的自动化主体，但其输出仍需形式化工具和专家检查。

</div>
<div class="concept-item" markdown="1">

**形式化证明与 Lean**

形式化证明把定义、定理和推理步骤写成严格的机器可检查语言，从而避免自然语言证明中的歧义。Lean 4.32.2 及其 Mathlib 库是本文使用的证明助手和数学基础库。

</div>
<div class="concept-item" markdown="1">

**端到端 TCS 研究流程**

这里的端到端流程不是只测试单个能力，而是从论文中的自然语言核心结论开始，依次处理定义、定理陈述和证明，最终输出经过 Lean 验证的完整证明。该设置保留论文特有的定义、假设以及引理和定理之间的多层依赖。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

FormalTCS 将前沿 TCS 论文中的核心研究结论组织为可逐阶段评测的实例。每个实例的输入包括论文元信息、核心结论标签、自然语言核心结论 `$\mathrm{core\_claim}$`、完整自然语言陈述 `$\mathrm{nl\_claim}$` 及证明概要 `$\mathrm{nl\_proof}$`；形式化阶段提供待证明的 Lean 定理 `$\mathrm{fl\_theorem}$`，验证目标是生成完整且可编译检查的 Lean 证明 `$\mathrm{fl\_proof}$`。数据来自 2025—2026 年被 STOC、FOCS、SODA 和 COLT 接收的论文，共 175 个实例；每个实例对应一篇不同论文，并由专家验证其形式化和证明。本文的基本假设是：真实 TCS 研究不能被充分表示为脱离上下文的教材定理，模型应在保留论文特定定义、假设和证明依赖的条件下完成从自然语言结论到严格形式证明的转换。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathrm{core\_claim}$**

论文中被选作评测对象的核心研究结论或结论标签。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{nl\_claim}$**

用自然语言完整陈述的核心结论，作为生成形式定义和 Lean 定理的语义输入。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{nl\_proof}$**

核心结论的自然语言证明概要，用于说明证明思路和依赖关系。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{fl\_theorem}$**

用 Lean 形式语言表示的待证明定理；模型需要针对该形式目标生成可验证证明。

</div>

</div>

**直接相关的工作**

- **TCS-Bench**: TCS-Bench 主要评估模型根据自然语言 TCS 定理陈述生成证明的能力，代表了对单一证明环节的测试。FormalTCS 进一步要求模型处理从自然语言核心结论到形式定义、定理陈述和 Lean 证明的完整流程，并使用前沿论文中的研究级问题。
- **LCS-Bench**: LCS-Bench 从教材中提取 TCS 知识构造基准，适合测试已有知识与相对标准化的问题。FormalTCS 则采用 2025—2026 年顶级 TCS 会议论文，并保留论文特有定义、假设和多层证明依赖，以减少教材内容带来的简化和潜在训练数据污染。

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

原文未明确报告。

</div>

<p class="paper-minor-label">关键流程</p>

原文未明确报告完整流程。

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

原文未明确报告。

**训练与推理**

原文未明确报告。

**复现信息**

原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- FormalTCS 基准：论文将其定义为覆盖四个阶段的任务集合，包括定理引出（CC2NC）、自动形式化（NC2FT）、证明引出（C2NP）和定理证明（FT2FP）；但原文未明确报告实例总数、数据集规模及训练/验证/测试划分。
- 各任务的输入：CC2NC 接收 Core Claim 并输出 NL Claim；NC2FT 接收 NL Claim 并输出 FL Theorem；C2NP 接收 NL Claim 与 FL Theorem 并输出 NL Proof；FT2FP 接收 FL Theorem 并输出 FL Proof。其作用是分别测试研究流程中理解主张、形式化、设计证明思路和编写可验证证明的能力。
- 人工标注输入设置：每个任务都直接使用人工标注的输入，而不是使用前一阶段模型的预测结果。该设置用于隔离各阶段能力，避免早期错误传播；因此，实验结果主要反映单阶段能力，不等同于真实端到端串联成功率。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**LLM-Rubric**

用于 CC2NC 和 C2NP，评价预测答案与参考答案在逻辑有效性、完整性、正确性和清晰度上的语义一致性。四项分数均归一化到 $[0,1]$，总分为 $0.4s_{\mathrm{logic}}+0.3s_{\mathrm{complete}}+0.2s_{\mathrm{correct}}+0.1s_{\mathrm{clear}}$。 （分数越高越好，因为它表示答案更符合逻辑、更完整、更正确且表达更清楚；但该指标依赖 LLM 评价器，不能等同于形式验证通过。）

</div>
<div class="metric-item" markdown="1">

**BEq+**

用于 NC2FT，给定参考定理 $t_r$ 和候选定理 $t_c$，分别在 Lean 中尝试证明 $t_r\Rightarrow t_c$ 与 $t_c\Rightarrow t_r$；两个方向都能证明时才判定候选定理与参考定理等价。 （通过率越高越好。该指标依赖双向符号证明，而非主观 LLM 判断，因此测试的是候选形式定理是否与参考定理具有相同逻辑内容。）

</div>
<div class="metric-item" markdown="1">

**Pass@$k$**

用于 FT2FP，衡量每个实例生成的 $k$ 个证明样本中至少有一个被 Lean 编译器接受的实例比例；本文对每个实例生成 $8$ 个候选，因此报告 $Pass@8$。 （数值越高越好，因为它表示模型在多次尝试中至少产生一个语法正确且形式验证通过的证明的概率；它不表示所有生成证明都正确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四阶段 FormalTCS 总体比较

<div class="result-value" markdown="1">

Claude-Opus-5 在 CC2NC、NC2FT、C2NP 和 FT2FP 上分别取得 $66.9$、$11.5$、$68.7$ 和 $28.6$；其中 NC2FT、C2NP 和 FT2FP 为表中相应任务的最高结果，CC2NC 的最高结果是 GPT-5.6-sol 的 $67.4$。

</div>

作者据此认为 Claude-Opus-5 在多数任务上总体最强，但它并未在所有阶段都第一。更重要的是，最高模型在自然语言主张理解和证明思路生成上达到约三分之二的评分，而形式化与最终形式证明仍明显较弱，说明单项能力较强并不意味着模型已经能稳定完成完整研究流程。

<div class="result-source" markdown="1">

来源：第 4.2 节，表 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Overall, Claude-Opus-5 achieves the best performance on most tasks, indicating the strongest TCS research capability among the evaluated models.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 自然语言任务与自动形式化任务的对比

<div class="result-value" markdown="1">

Claude-Opus-5 在 C2NP 上为 $68.7$，在 NC2FT 上为 $11.5$；GPT-5.6-sol 在 C2NP 上为 $67.9$，在 NC2FT 上为 $10.6$。

</div>

这一对比表明，模型能够相对较好地用自然语言解释或规划理论证明，但难以把相同的理论内容精确转换为 Lean 定理。该结果支持“形式化表示是独立困难”的解释，但由于任务输入和输出形式不同，分数不能被严格当作同一量纲上的直接准确率比较。

<div class="result-source" markdown="1">

来源：第 4.2.2 节 Finding 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For example, Claude-Opus-5 achieves 68.7 on C2NP, whereas its performance on the corresponding theorem formalization task (NC2FT) is only 11.5.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 端到端流程中的最终形式证明瓶颈

<div class="result-value" markdown="1">

Claude-Opus-5 在 CC2NC 上为 $66.9$、在 C2NP 上为 $68.7$，但在 FT2FP 上的 $Pass@8$ 仅为 $28.6$；同时，所有模型的 NC2FT 最高分不超过 $11.5$。

</div>

作者将 NC2FT 视为整个流程的主要瓶颈：即使给定人工标注的形式定理，模型在后续 FT2FP 仍可达到 $28.6$ 的 $Pass@8$，但从自然语言主张生成等价 Lean 定理的能力更低。该结果说明模型的困难不只是写 Lean 证明，也包括识别数学对象、假设和逻辑结构；不过由于各阶段使用人工输入隔离，实验不能直接给出真实串联端到端成功概率。

<div class="result-source" markdown="1">

来源：第 4.2.3 节 Finding 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across the entire pipeline, NC2FT is the lowest-performing stage, with no evaluated model exceeding 11.5.

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

- GPT 模型家族及其 Codex harness：包含 GPT-5.6 的 luna、terra 和 sol 配置，用于比较同一模型家族及不同配置下的阶段性表现。
- Claude 模型家族及 Claude Code harness：包含 Haiku-4.5、Sonnet-5 和 Opus-5，用于考察不同规模 Claude 模型的理论研究能力。
- DeepSeek-V4 及 DeepSeek Harness：包含 Flash 和 Pro，用于提供另一主流模型家族的对照。
- Qwen3.8-Max 与 QoderCLI：仅作为独立的 LLM-rubric 评价器，而不是主要被测模型；它用于降低评价模型与被评模型相同所造成的潜在偏差。

**实验想回答的问题**

- 当前主流大语言模型能否完成从核心理论主张理解、自然语言到形式定理转换、证明策略生成，直到机器可验证 Lean 证明的端到端理论计算机科学研究流程？
- 该研究流程的主要性能瓶颈位于哪些阶段，以及模型规模和模型家族是否对应更强的理论计算机科学研究能力？

**实验实现**

实验评估了 GPT、Claude 和 DeepSeek 三个主流模型家族及其对应 harness，并覆盖不同模型规模。CC2NC 与 C2NP 各使用一次生成；NC2FT 与 FT2FP 各生成 $8$ 个候选，以利用 Lean 的自动验证能力。多次生成任务采用 temperature $0.6$、top_p $0.9$；单次生成任务采用确定性解码，temperature $0.0$、top_p $1.0$。为防止证明绕过，验证环境设置 `set_option warningAsError true`，使 `sorry` 导致错误，并使用自定义 linter 或 `#print axioms` 配合允许公理白名单，排除 `sorry`、自定义 `axiom` 声明等规避方式。NL 任务的 LLM-rubric 由不属于主要被测模型的 Qwen3.8-Max 与 QoderCLI 执行；论文还在附录 F 比较 LLM 评价与人工评价的一致性。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces an LLM benchmark for end-to-end formal theoretical computer science research, directly evaluating advanced formal reasoning capabilities.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`2916c55a9e2aa8f5464b6b9b34ca2e4201a60ca9eaf55c5802e477fb756c041c`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
