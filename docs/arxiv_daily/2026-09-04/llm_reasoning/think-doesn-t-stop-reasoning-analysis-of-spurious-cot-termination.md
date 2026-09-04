---
title: "[论文解读] </think> Doesn't Stop Reasoning: Analysis of Spurious CoT Termination"
description: "[arXiv 2609.03633][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2609.03633"
announcement_date: "2026-09-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:35:43.567485+00:00"
source_sha256: "1d72fb00b90adb2538f2dad0b38281aa5ea51723c25698962e10e9aa3493b69f"
tags:
  - "LLM Reasoning"
  - "大型推理模型"
  - "链式思维"
  - "训练无关提前退出"
  - "结束思考标记"
  - "伪 CoT 终止"
  - "推理到回答的阶段切换"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.03633</p>

# </think> Doesn't Stop Reasoning: Analysis of Spurious CoT Termination

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Seunghee Koh, Sungjae Choi, Minchan Kwon, Sunghyun Baek, Junmo Kim</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Korea Advanced Institute of Science and Technology, South Korea</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03633v1) · [PDF 下载](https://arxiv.org/pdf/2609.03633v1) · **关键词** 大型推理模型, 链式思维, 训练无关提前退出, 结束思考标记, 伪 CoT 终止, 推理到回答的阶段切换<br>
**代码**: [https://github.com/Seunghee-Koh/Spurious-CoT-Termination](https://github.com/Seunghee-Koh/Spurious-CoT-Termination)

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

本文研究大型推理模型（large reasoning models, LRMs）在推理时如何生成并控制链式思维（chain-of-thought, CoT）。这类模型通常先生成由多个中间步骤组成的推理轨迹，再生成最终答案；这种显式推理能够提升数学和科学任务的准确率，但也可能产生过长、冗余的轨迹，增加推理成本。本文聚焦一种无需重新训练模型的解码时提前退出（early exit）设置：在模型尚未完成全部推理时插入结束思考标记 `$\mathrm{EoT}=\texttt{</think>}$`，试图让模型从推理阶段切换到回答阶段；研究问题是，这个外部插入的分隔标记是否真的能可靠触发该切换。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**链式思维（CoT）**

CoT 是模型在最终答案之前生成的中间推理步骤，例如数学题中的列式、变形和自我检查。本文把这些中间步骤视为推理阶段的输出，而把随后给出的最终结论视为回答阶段的输出。

</div>
<div class="concept-item" markdown="1">

**显式思考块与结束思考标记（EoT）**

在本文采用的格式中，`<think>` 开始推理块，`</think>` 结束推理块，之后的文本属于回答阶段。EoT 的作用类似一个边界信号：模型若正确利用它，就应停止继续推理并直接组织最终回答。

</div>
<div class="concept-item" markdown="1">

**训练无关的提前退出**

提前退出是在生成过程中根据中间状态或中间答案判断模型是否可以停止继续推理，而不修改模型参数或重新训练模型。本文研究的是在选定退出点插入 EoT 的方案，因此它节省了部分原本可能生成的推理 token，但也可能造成阶段切换失效。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个需要推理的输入问题，以及一个按显式 `<think>... </think>` 格式生成文本的 LRM，模型首先生成推理轨迹；某种提前退出方法在中间位置选定退出点后，系统将 `$\mathrm{EoT}$` 插入当前序列，并继续进行自回归生成。理想情况下，插入后的后续文本应立即进入回答阶段并输出最终答案；本文考察的异常情况是，模型在回答阶段继续生成具有推理特征的内容，甚至在稍后再次生成 `$\mathrm{EoT}$`。论文将这种现象称为 spurious CoT termination，即“伪 CoT 终止”：表面上推理块已经被外部标记关闭，实际上推理行为仍在继续。实验中的最终答案按照官方提示规范，从最后一个 `$\boxed{...}$` 中抽取；研究设置覆盖四个 LRM、五个推理基准和两种提前退出方法，并以 No-CoT 与 Full-CoT 作为参照。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\texttt{<think>}$**

开始思考标记（SoT），表示显式推理阶段的起点。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{EoT}=\texttt{</think>}$**

结束思考标记，表示系统希望模型从推理阶段转入回答阶段；本文也研究它被插入中间退出点后的行为。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{CoT}$**

链式思维，即最终答案之前生成的中间推理文本。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{LRM}$**

大型推理模型，指能够生成较长显式推理轨迹以解决复杂数学或科学问题的语言模型。

</div>

</div>

**直接相关的工作**

- **DEER**: DEER 是本文比较的训练无关提前退出方法：它在推理过程中的 `Wait` 等过渡位置生成中间试探答案，并在答案置信度达到阈值时退出。本文在 DEER 选定的退出点插入 EoT，以检验外部结束标记能否真正诱导可靠的推理到回答切换。
- **DynaSoR**: DynaSoR 以固定间隔探测中间答案，并在预测结果趋于一致时停止推理。本文将其作为第二种提前退出机制，比较不同退出点选择策略下 EoT 再生成和伪 CoT 终止是否普遍存在；与已有研究主要在一开始跳过推理不同，本文研究的是动态推理过程中途插入 EoT。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大推理模型依靠链式思考（CoT）完成数学和科学推理，但完整推理轨迹往往过长，增加推理成本而未必带来相称的性能收益。因此，研究者希望在不重新训练模型的情况下提前结束推理，并让模型立即进入答案生成阶段。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **训练无关的提前退出方法**：这类方法在模型生成完整推理轨迹之前选择一个中间位置，停止继续生成原有推理内容，以减少推理令牌和计算开销。
- **注入结束思考令牌（EoT）的方法**：在提前退出位置外部插入结束思考令牌 `$\mathrm{EoT}=\texttt{</think>}$`，使输出形式符合显式思考区块的格式，并借此触发从推理阶段到答案阶段的转换。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 插入 `$\mathrm{EoT}$` 并不总能形成干净的答案阶段：模型有时会在答案阶段先继续生成推理式内容，之后才再次生成 `$\mathrm{EoT}$`。这会延长答案阶段，并削弱提前退出节省推理令牌的实际收益。
- 现有控制策略主要匹配模型输出的外部格式，却没有确认后续生成是否真正将插入的 `$\mathrm{EoT}$` 作为内部状态转换信号。论文所提供的关于模型内部状态的解释仍是间接的，无法仅凭行为现象直接验证模型在该令牌之后的内部推理状态。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚不清楚提前退出后出现的再次生成 `$\mathrm{EoT}$` 是什么现象、其前置文本是否仍包含推理行为，以及插入的退出令牌为何未能稳定触发推理到答案的转换。尤其缺少对“后续令牌是否充分关注插入的 `$\mathrm{EoT}$`”这一可能机制的系统检验。

</div>
<div markdown="1"><span>核心问题</span>

当训练无关的提前退出方法在中间位置插入 `$\mathrm{EoT}$` 时，模型为何会在答案阶段继续进行类似推理的生成并再次输出 `$\mathrm{EoT}$`；如果增强后续生成对该退出令牌的关注，是否能够减少这种虚假 CoT 终止现象并缩短答案阶段？

</div>
<div markdown="1"><span>作者直觉</span>

一个格式上的结束标记只有在后续生成真正读取并采用它时，才可能发挥状态转换作用。若后续令牌对插入的 `$\mathrm{EoT}$` 关注不足，模型可能仍沿用尚未完成的推理过程，直到稍后再次生成一个更符合其内部转换模式的 `$\mathrm{EoT}$`。因此，出口令牌注意力偏置（EAB）通过提高后续生成对插入令牌的关注，能够直接检验并可能修复这一转换失效问题；若现象随偏置减弱，则可为“注意力不足是相关机制之一”提供干预证据。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是提出新的训练目标或模型架构，而是分析一种训练免调的提前退出推理流程。给定一个启用显式思考块的语言模型和问题，DEER 或 DynaSoR 在模型完成部分推理后选择退出点，并注入结束思考标记 $\mathrm{EoT}=\texttt{</think>}$；模型随后生成答案。作者进一步在答案阶段对注入的 $\mathrm{EoT}$ 施加 Exit-token Attention Biasing（EAB），比较不同注意力偏置对伪造思维链终止、答案长度和准确率的影响。直观地说，方法研究的是“提前按下停止思考按钮”后，模型是否真的开始答题，而不是继续思考并稍后再次按下同一个按钮。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 输入问题并生成推理轨迹

模型先按照显式思维链格式生成推理文本；推理过程中的 $\texttt{Wait}$ 标记用于把连续推理划分为多个片段。在 Full-CoT 对照中，模型持续推理直到自然生成 $\mathrm{EoT}$；在 No-CoT 对照中则跳过推理阶段。

<div class="method-step__io" markdown="1">

**输入**：来自 MATH、AMC 2023、AIME 2024、GSM8K 或 GPQA-Diamond 的测试问题，以及指定的模型和提示模板。<br>
**输出**：一条尚未结束或已经自然结束的推理轨迹，以及可供提前退出算法检查的推理片段。

</div>

**直观理解**：先让模型像平常一样逐步解题，并把每个“等一下、检查答案”的位置当作检查点。Full-CoT 相当于不打断，No-CoT 相当于完全不让模型展示思考。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 在中间位置判断是否提前退出

DEER 在每个 $\texttt{Wait}$ 位置发起中间答案探针，当探针答案的置信度超过 $\lambda=0.95$ 时退出；DynaSoR 每隔 256 个 token 发起探针，当连续三个探针答案一致时退出。若未满足退出条件而达到推理预算，则直接结束推理并注入 $\mathrm{EoT}$。

<div class="method-step__io" markdown="1">

**输入**：当前推理轨迹、推理片段边界，以及模型对中间答案的置信度或连续探针答案。<br>
**输出**：一个被选中的提前退出点，以及被保留的部分推理轨迹。

</div>

**直观理解**：算法会定期问模型“现在答案是什么”。如果模型已经足够确定，或连续几次给出相同答案，就认为可以少想一些；否则继续推理，直到预算用完。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 注入结束思考标记并生成答案阶段

在退出点外部插入 $\mathrm{EoT}=\texttt{</think>}$，随后让模型生成回答阶段。若模型在回答阶段又生成一个新的 $\mathrm{EoT}$，则将注入标记之后、重新生成标记之前的文本定义为伪造思维链终止（spurious CoT termination）相关的前置跨度。

<div class="method-step__io" markdown="1">

**输入**：提前退出点及其之前的推理 token 序列。<br>
**输出**：答案阶段文本、是否再次生成 $\mathrm{EoT}$ 的标记，以及推理阶段和答案阶段的 token 数量。

</div>

**直观理解**：研究者在中途替模型写入“思考结束”。如果模型没有马上答题，而是先继续写推理并过一会儿再次写“思考结束”，这就是本文要分析的异常行为。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 对退出标记施加注意力干预并比较输出

EAB 在答案阶段增加模型对注入 $\mathrm{EoT}$ 的注意力，使用 $\alpha=2$ 作为默认值，并对 R1-Distill-14B 使用 $\alpha=4$；所有干预条件共享同一推理轨迹，以隔离答案生成时注意力变化的作用。随后比较准确率、ERR、推理阶段长度和答案阶段长度，并用 Double-EoT、Block-EoT 及提示级过渡短语作为控制干预。

<div class="method-step__io" markdown="1">

**输入**：同一条提前退出推理轨迹，以及不加偏置和不同 $\alpha$ 设置下的答案阶段生成。<br>
**输出**：不同干预条件下的答案、准确率、伪造终止率（ERR）及生成长度，用于判断注意力增强是否促成真正的推理到回答转换。

</div>

**直观理解**：不重新解题，只改变模型在答题时是否更重视那个“思考结束”标记。这样可以判断问题是否确实出在模型没有充分关注这个标记，而不是不同推理内容造成的差异。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文没有提出需要优化的新损失函数，也没有对语言模型进行参数训练；因此不存在本文方法对应的训练目标。EAB、DEER 和 DynaSoR 均在推理时运行：前两者决定退出点，后者在答案生成时干预注意力。研究重点是通过受控推理实验检验注入 $\mathrm{EoT}$ 是否足以触发推理到回答的相位转换，以及增强该标记的注意力是否能减少异常延续。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 训练免调提前退出模块**

DEER 和 DynaSoR 都通过中间答案探针决定是否终止推理，不更新模型参数。DEER 依赖 $\texttt{Wait}$ 片段边界和置信度阈值 $\lambda=0.95$；DynaSoR 使用固定的 256-token 探针间隔和“三次连续答案一致”规则。

> 直观理解：这两个模块像两种不同的“提前交卷检查器”：一种看模型当前答案是否足够自信，另一种看连续几次检查是否一致。它们的作用是决定何时打断推理，而不是改变模型本身。

**2. EoT 注入与伪造终止检测模块**

提前退出点由外部注入 $\texttt{</think>}$，然后继续解码答案阶段；若模型再次生成该标记，则计算 ERR，并分析再生成标记前后的 token 数量及 $\texttt{Wait}$ 出现次数。作者还以答案阶段中的 $\texttt{Wait}$ 和临近再生成标记的 $\texttt{\boxed{…}}$ 作为继续推理的行为线索。

> 直观理解：单纯插入“思考结束”并不保证模型真的切换模式，因此需要检查它是否又写了一段像推理的内容。再次出现结束标记是主要可观测信号，$\texttt{Wait}$ 和 boxed 答案则帮助判断这段内容是否仍在解题。

**3. Exit-token Attention Biasing（EAB）模块**

EAB 在答案阶段直接改变注入退出标记的注意力权重，正偏置提高模型对该标记的关注，负偏置则削弱关注。研究通过固定推理轨迹、改变答案阶段解码，并与 Double-EoT、Block-EoT、Ans-Prefix、Post-Box 和 Post-Ans-Box 比较，检验注意力层面的因果作用及其局限。

> 直观理解：EAB 不是再给模型一句提示，也不是禁止它输出某个 token，而是把“请注意已经结束思考”这个信号的音量调大。控制实验用于区分“真正完成了模式切换”和“只是强行不许再次输出结束标记”。

**训练与推理**

完整流程仅涉及推理阶段。首先选定模型、问题和推理预算；对于 DEER，在每个 $\texttt{Wait}$ 处生成最多 30 个 token 的 MATH 探针、2 个 token 的 GPQA 探针、20 个 token 的其他基准探针，并用每 token top-1 概率的算术平均或几何平均聚合置信度；对于 DynaSoR，每 256 个 token 探针一次，连续三次答案一致即退出。DEER 最多探针 10 次，DynaSoR 最多 20 次；达到上限仍未退出时继续推理，达到推理预算则注入 $\mathrm{EoT}$。退出后，模型生成答案阶段；EAB 在同一推理轨迹上使用不同的 $\alpha$ 重新生成答案，从而比较无偏置和有偏置条件。评估输出包括最终答案、准确率、ERR、推理阶段 token 数和答案阶段 token 数，并进一步分析 $\texttt{Wait}$、再生成 $\mathrm{EoT}$ 以及 boxed 表达式的位置。

**复现信息**

复现实验所需的关键设置包括：四个模型为 R1-Distill-1.5B、R1-Distill-14B、Qwen3-14B 和 QwQ-32B；五个测试集分别包含 GSM8K 的 1,319 个样本、MATH-500 的 500 个样本、AMC 2023 的 40 个样本、AIME 2024 的 30 个样本和 GPQA-Diamond 的 198 个样本。DEER 使用 $\lambda=0.95$，DynaSoR 使用 256-token 探针间隔；EAB 默认 $\alpha=2$，R1-Distill-14B 使用 $\alpha=4$。答案阶段的 EAB 重生成使用独立的答案长度上限，因此其长度可能不同于原始 DEER 或 DynaSoR 的上下文预算；但同一次干预扫描中的 $\alpha=0,2,4$ 共享推理轨迹和答案阶段预算，适合进行条件内比较。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 论文在五个基准上进行评估，但给定材料未提供基准名称、样本规模、数据划分或各基准承担的具体测试角色，因此无法可靠列出单个数据集。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**伪思维链终止**

判断模型在被注入 EoT 后是否仍于回答阶段生成推理式内容，并在之后再次生成 EoT；它直接衡量显式结束标记是否实现了预期的状态转换。给定材料未说明该指标最终采用发生率、样本数还是其他聚合形式。 （越低越好，因为较低值表示注入 EoT 后继续推理并再次结束思考的现象更少。）

</div>
<div class="metric-item" markdown="1">

**回答阶段长度**

统计注入 EoT 后回答区间产生的 token 数；若其中包含延续推理，该长度也会反映早退后转移到回答区间的冗余计算。 （在答案质量不下降的前提下越低越好，因为这意味着外部早退更有效地减少了后续生成；但仅凭长度下降不能证明推理行为已被正确终止。）

</div>
<div class="metric-item" markdown="1">

**早退节省的推理 token 数**

衡量相对于原始推理轨迹，早退在显式思考阶段省去了多少 token；论文用它考察被节省的推理是否可能转移到 EoT 后的回答阶段。 （该量本身通常越高代表显式推理压缩越强，但必须结合回答阶段长度与任务质量判断；若节省量被回答阶段中的继续推理抵消，则不代表真实计算节省。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 在中间推理位置注入 EoT 的训练自由早退

<div class="result-value" markdown="1">

作者发现，注入的 EoT 并不总能使模型干净地进入回答阶段：模型可能先在回答区间继续生成，并在之后再次生成 EoT；再次生成的 EoT 之前仍呈现持续推理行为。

</div>

这说明格式层面的“关闭思考块”与模型内部真正停止推理不是同一件事。早退可能只是把部分思维链从显式思考区移到了回答区，而非真正删除。该观察证明了现象存在，但给定材料没有提供发生比例，因此不能判断其在各模型或任务上的绝对严重程度。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Answering-phase generation can continue before the model regenerates another EoT, with the span preceding this regenerated EoT scaling with the reasoning tokens saved by early exit and exhibiting continued reasoning behavior.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 早退节省的推理 token 与再次生成 EoT 前区间的关系

<div class="result-value" markdown="1">

作者报告，再次生成 EoT 前的回答区间长度会随早退所节省的推理 token 数增加，并且该区间表现出继续推理的特征。

</div>

这一关系支持“被截断的推理转移到了回答阶段”的解释：越早截断，模型可能越需要在显式回答区间补完推理。不过，“随之增长”是相关性描述，并不能单独证明节省的每个推理 token 都被一一迁移，也不能排除题目难度或退出位置等共同因素。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Answering-phase generation can continue before the model regenerates another EoT, with the span preceding this regenerated EoT scaling with the reasoning tokens saved by early exit and exhibiting continued reasoning behavior.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### EAB 在四个大推理模型、五个基准和两种早退方法上的评估

<div class="result-value" markdown="1">

提高模型对注入 EoT 的注意力后，伪思维链终止与回答阶段长度均下降；这一趋势覆盖四个模型、五个基准和两种早退方法。

</div>

跨多种设置的一致改善表明，模型是否充分利用注入的结束标记，是控制推理—回答转换的重要因素。由于给定材料没有分项数值、任务正确率或统计显著性，现有证据只能支持“现象减少和生成变短”，不能据此断言所有任务的最终准确率保持不变，也不能把注意不足确认为唯一原因。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across four LRMs, five benchmarks, and two early-exit methods, increasing attention to the injected EoT reduces spurious CoT termination and answering-phase length.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 给定节选仅包含附录 D.1 的标题与不完整表头，实验表格正文缺失；因此无法核验五个基准和四个模型的名称、样本规模、具体分数、方差、显著性以及不同早退方法间的差异，所有实验结论仍需对照论文完整表格复查。
- 摘要明确报告 EAB 降低伪终止与回答阶段长度，但未在所给材料中说明最终答案准确率、计算延迟或注意力干预的副作用。因而“生成更短、伪终止更少”不能直接推出整体推理效率或任务性能一定更优。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原始完整推理：不在中间位置注入 EoT，让模型自行完成思考并进入回答，用于界定未经早退干预时的推理与回答长度；具体实现和结果在给定材料中未明确报告。
- 仅注入 EoT 的训练自由早退：在选定的中间位置插入 $\texttt{</think>}$，但不额外改变注意力，用于检验遵循显式 think-block 格式是否足以触发真实的推理—回答转换。
- 两种早退方法：摘要说明实验覆盖两种早退方法，用于检查伪思维链终止是否依赖某一种退出点选择策略；其名称及退出点计算方式在给定材料中未明确报告。
- 退出标记注意力偏置（EAB）：提高模型对注入 EoT 的注意力，并与仅注入 EoT 的条件比较，以探查注意不足是否是伪终止的影响因素。

**实验想回答的问题**

- 向大推理模型的中间推理位置注入结束思考标记（EoT，$\texttt{</think>}$）后，模型是否真正从推理阶段切换到回答阶段，还是会在显式回答区间中继续产生类似思维链的内容？
- 若伪思维链终止源于模型对注入 EoT 的注意不足，提高生成过程对该标记的注意力，能否减少伪终止现象并缩短回答阶段，同时适用于不同模型、任务与早退方法？

**实验实现**

实验覆盖四个大推理模型、五个基准和两种训练自由早退方法。核心协议是在早退方法选择的中间位置注入 EoT，观察模型是否直接回答，或先在回答区间继续生成、随后自行再生成一个 EoT；EAB 条件进一步提高生成时对注入 EoT 的注意力。附录 D.1 标题表明论文汇总了跨模型、跨基准的完整回答阶段长度结果，但给定节选仅保留标题和表头片段，未提供模型名称、基准名称、解码参数、样本数、显著性检验及质量评估细节。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 提高对注入 EoT 的注意力，与仅注入 EoT 的早退条件比较 | EAB 介入后，伪思维链终止和回答阶段长度均减少；实验覆盖四个大推理模型、五个基准和两种早退方法，但给定材料未提供注意力偏置强度、逐项数值或误差范围。 | 该干预主要隔离“模型是否关注外部注入的结束标记”这一因素：退出位置和显式标记保持为早退流程的一部分，只增强该标记在注意力计算中的影响。结果与注意不足假设相符，但若没有任务正确率、等计算量控制和其他 token 的偏置对照，尚不能排除一般性的解码扰动或生成压缩效应。 | 摘要<br><span class="experiment-evidence">Across four LRMs, five benchmarks, and two early-exit methods, increasing attention to the injected EoT reduces spurious CoT termination and answering-phase length.</span> |

**定性案例**

- 典型定性轨迹是：系统在中间推理点外部注入 $\texttt{</think>}$ 后，模型没有立即形成干净的最终答案，而是在回答阶段继续产生推理式文本，随后自行再次输出 EoT。第二个 EoT 可视为模型延迟完成思考的可观测信号，但给定材料没有提供具体样例文本，不能进一步判断这些区间的语言模式或答案质量。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该论文分析大语言模型链式思维提前退出导致的虚假推理终止，并提出注意力偏置进行缓解。; rule check: matched taxonomy keywords; top rule score=10.0
- 全文指纹：`1d72fb00b90adb2538f2dad0b38281aa5ea51723c25698962e10e9aa3493b69f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
