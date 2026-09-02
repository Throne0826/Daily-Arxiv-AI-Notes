---
title: "[论文解读] From Base Rollouts to RL Reasoning: A Budgeted Search Perspective"
description: "[arXiv 2609.01274][LLM Reasoning] 本文从有限推理预算下的行为视角检验“RL 是否内化了搜索”：它考察经过可验证奖励强化学习的模型，其默认推理表现能否由基础模型通过结构化的外部解码与搜索路径近似恢复。"
arxiv_id: "2609.01274"
announcement_date: "2026-09-02"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:43:12.465313+00:00"
source_sha256: "81c9af429864b53ec0355ad172f27223324a4d997fe0041a7597476cf10072e8"
tags:
  - "LLM Reasoning"
  - "强化学习"
  - "对齐 / RLHF"
  - "强化学习与可验证奖励（RLVR）"
  - "大语言模型推理"
  - "推理时搜索"
  - "采样效率"
  - "Unified Decoding Framework（UDF）"
  - "Budgeted Operating-Point Transition Rule（BOPTR）"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.01274</p>

# From Base Rollouts to RL Reasoning: A Budgeted Search Perspective

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Wenhe Sun, Cunxiang Wang, Zijun Yao, Yixin Cao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Fudan University；Tsinghua University；Shanghai Innovation Institute</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.01274v1) · [PDF 下载](https://arxiv.org/pdf/2609.01274v1) · **关键词** 强化学习与可验证奖励（RLVR）, 大语言模型推理, 推理时搜索, 采样效率, Unified Decoding Framework（UDF）, Budgeted Operating-Point Transition Rule（BOPTR）<br>
**代码**: [https://github.com/HALIS-sh/Searchlens_boptr](https://github.com/HALIS-sh/Searchlens_boptr)

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

本文从有限推理预算下的行为视角检验“RL 是否内化了搜索”：它考察经过可验证奖励强化学习的模型，其默认推理表现能否由基础模型通过结构化的外部解码与搜索路径近似恢复。

**不用术语来说**：强化学习后的语言模型通常能用较少尝试解出更多问题，但这不一定意味着训练创造了基础模型从未具备的新推理能力；另一种可能是，正确解法原本就在基础模型能够生成的范围内，只是出现概率很低，而强化学习让模型更容易抽到它们。要区分这两种解释，需要在统一且受预算约束的条件下，系统比较强化学习模型的默认生成与基础模型采用不同搜索方式、不同尝试次数时的行为。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 SearchLens／统一解码框架，将逐词采样、类束搜索、树式探索和序列级重采样表示为共享预算空间中的可执行策略，并将生成策略与 pass@$k$、自一致性、best-of-$N$ 和 first-finish 等事后评价方式分离，从而能够公平分析“基础模型加搜索”能否恢复强化学习模型的行为。
- 提出低复杂度的预算操作点转移规则 BOPTR，用 $N_{\mathrm{Base}}\approx\alpha N_{\mathrm{RL}}^\beta$ 描述恢复强化学习目标所需的基础模型预算，并通过跨预算、跨基准和跨模型分析检验其可迁移范围及失效边界。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型推理、强化学习后训练与推理时搜索的交叉领域。强化学习与可验证奖励（RLVR）通过程序化或规则化的正确性信号训练模型，使其在数学和复杂推理任务上表现更好；推理时解码与搜索则在模型参数不变的情况下，通过增加并重新分配有限的生成预算来寻找更可能正确的推理轨迹。本文不提出新的强化学习算法，而是研究一个行为层问题：RL模型在低预算下的优势，究竟主要来自新的推理能力，还是来自将默认生成分布重新集中到基础模型本来就能生成、但默认情况下较少采样到的正确轨迹。为避免只在单一预算或单一解码策略下比较，作者把不同生成策略、搜索策略和计算预算统一表示为可比较的操作点，再考察基础模型的搜索结果能否沿一条低复杂度路径恢复RL模型的默认性能曲线。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**RLVR与默认rollout分布**

RLVR是以答案是否正确等可验证信号作为奖励，对预训练语言模型进行强化学习。给定同一个问题，rollout指模型生成的一条完整推理轨迹；默认rollout分布则是模型在固定解码策略和预算下自然生成各种轨迹的概率分布，RL可能改变的是该分布中不同轨迹被采样到的频率。

</div>
<div class="concept-item" markdown="1">

**推理时搜索与预算**

推理时搜索不更新模型参数，而是在生成阶段尝试多条候选轨迹，并通过采样、束式扩展、树搜索或候选重采样等方式选择结果。预算表示可使用的生成或评估资源，本文主要将其视为可分配的rollout数量或等价推理计算量，因此同一个基础模型可以对应多个不同的策略—预算操作点。

</div>
<div class="concept-item" markdown="1">

**pass@$k$与操作点**

pass@$k$衡量从同一问题生成的$k$条候选中是否至少有一条正确，适合评估增加采样数量带来的潜在成功率；它与逐条生成后立即停止的成功率不同。一个操作点写作$(\pi,N)$，其中策略$\pi$规定如何生成或搜索候选，$N$规定预算；本文将生成完成后再计算的指标与生成策略分离，以便比较不同策略和预算。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是成对的基础模型（Base）与经过RLVR训练的模型（RL），二者来自SimpleRL-Zoo的相应检查点，且在相同或可对应的任务设置下进行比较。对每个输入问题，模型生成一组推理轨迹或最终答案；RL侧使用其默认解码策略，并随预算$N_{\mathrm{RL}}$变化形成一条性能曲线。Base侧则允许在统一解码框架中选择策略$\pi$和预算$N_{\mathrm{Base}}$，形成操作点$(\pi,N_{\mathrm{Base}})$，再以pass@$k$、自洽性、best-of-$N$或first-finish success等指标评价输出。核心任务不是寻找每个预算下偶然最匹配RL的Base操作点，而是判断这些恢复点能否构成跨预算的低复杂度结构化路径，并检验该结构能否跨任务、模型、模型家族和训练设置迁移。该分析采用行为等价的弱假设：只比较可观察的输入—输出表现，不据此断言RL与Base在参数或内部机制上等价；结论也限定在所测试的训练配方、预算范围和模型群体内。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\pi$**

解码或搜索策略，例如逐token采样、束式搜索、树式搜索或序列级候选重采样。

</div>
<div class="notation-item" markdown="1">

**$N_{\mathrm{Base}}$**

基础模型在某个恢复操作点上使用的推理预算，通常对应生成或处理的候选数量。

</div>
<div class="notation-item" markdown="1">

**$N_{\mathrm{RL}}$**

RL模型默认策略对应的推理预算，用来参数化RL性能曲线。

</div>
<div class="notation-item" markdown="1">

**$N_{\mathrm{Base}}\approx\alpha N_{\mathrm{RL}}^{\beta}$**

BOPTR所描述的预算转移规则；$\alpha$是尺度系数，$\beta$是由基准任务条件决定的指数，表示要达到与某一RL预算相应的行为水平，Base大约需要多少预算。

</div>

</div>

**直接相关的工作**

- **SimpleRL-Zoo与DeepSeekMath等RLVR方法（Zeng et al., 2025；Shao et al., 2024）**: 这些工作使用程序化或规则化的可验证奖励训练开放基础模型，是本文成对Base/RL检查点的来源背景。本文沿用其训练后模型进行行为分析，而不是提出新的RLVR训练目标；这样可以把问题集中在RL后的默认生成分布如何变化。
- **关于RL增益、采样效率与推理边界的研究（Yue et al., 2025；Karan and Du, 2025）**: 相关研究观察到，RL模型常在小采样预算下优于Base，而Base在增大pass@$k$预算后可能缩小差距；也有研究显示无需额外训练的Base推理时采样能够接近或超过部分RL模型。这些结果提出了“RL是否主要提高采样效率”的行为解释，但未必提供一个统一的策略—预算空间和跨预算低复杂度恢复规则；本文以UDF和BOPTR检验这一缺口。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

RLVR 已成为提升语言模型数学与一般推理表现的重要后训练方法，但训练收益的来源仍不清楚。若收益主要来自提高既有正确轨迹的采样效率，那么一部分效果可能通过增加基础模型的推理预算或采用更好的外部搜索获得；若强化学习确实产生了基础模型搜索空间之外的行为，则仅靠推理时扩展无法替代训练。弄清这一点会影响研究者如何分配训练与推理资源，以及如何解释所谓“推理能力提升”。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **强化学习模型与基础模型的同策略、同预算比较**：让 Base 与 RL 检查点使用相同的默认采样方法和相同生成预算，再比较成功率。已有观察表明 RL 模型往往在低预算区间占优，而基础模型在扩大采样预算后有时能接近 RL 水平。
- **基础模型的推理时解码与搜索**：不改变模型参数，而通过扩大探索、集中概率质量或在多个候选答案中进行选择来重新分配有限 rollout 预算，包括逐词采样、类束扩展、树式探索和序列级重采样等方法。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 不同解码与搜索方法具有不兼容的控制结构，且生成策略经常与 self-consistency、best-of-$N$ 等评价或选择规则混在一起，因此同预算比较无法覆盖基础模型完整的“策略—预算”操作空间，也难以判断差异来自模型还是评测方式。
- 在庞大的策略网格中为 RL 曲线的每个预算事后挑选最接近的基础模型结果，很容易得到偶然匹配并夸大可恢复性；即使某条规则在 Math500 上成立，也不能直接假定其适用于 AIME、GPQA、IFEval 或不同模型家族与训练分布。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种受统一预算约束、生成与评价相分离的行为分析方法，用来判断 RL 默认 rollout 曲线是否对应于基础模型操作空间中的一条低复杂度、可跨预算延续并可检验迁移性的路径，而不是由互不相关的事后最优点拼接出来。与此同时，这种恢复关系在哪些任务制度、模型家族和训练分布下成立或失效，也尚未被系统刻画。

</div>
<div markdown="1"><span>核心问题</span>

对于给定的 RL 默认策略预算 $N_{\mathrm{RL}}$，是否存在基础模型的解码策略与预算操作点 $(\pi,N_{\mathrm{Base}})$，能够恢复 RL 模型的可观察表现；更严格地说，这些恢复点能否由类似 $N_{\mathrm{Base}}\approx\alpha N_{\mathrm{RL}}^\beta$ 的低维规则组织起来，并在不同预算、基准和模型之间保持可解释的迁移结构？

</div>
<div markdown="1"><span>作者直觉</span>

可以把一次推理解题看成在隐含推理树上分配有限尝试次数：基础模型可能已经能够走到正确路径，但默认概率分配过于分散，导致小预算下很少命中；RL 则可能把概率质量推向受奖励的路径。外部搜索虽然不修改参数，却也能通过增加探索、保留更有希望的分支或从候选中筛选来重新分配预算。因此，如果 RL 主要提高采样效率，基础模型应当能以某种有规律的额外预算和搜索策略逼近其行为；若始终无法恢复，则说明目标行为可能超出了本文测试的基础模型操作空间。

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

- Math500：数学推理基准；论文将 Qwen2.5-7B/Math500 作为锚点单元，用于构造 SearchLens 搜索景观、恢复分析和 BOPTR 规则。它主要测试数学问题上的多预算搜索与 RL 曲线恢复。
- AIME 2024/2025 与 GPQA-Diamond：分别用于测试竞赛数学推理和高难度科学问答场景，并承担同一模型跨基准的横向迁移检验。原文未明确报告各数据集的样本规模或具体划分。
- IFEval：指令遵循与终止行为压力测试；除通过率外，还观察有效性和 first-finish success，并将 self-consistency（SC）作为诊断指标。它用于检验方法是否只适用于数学式答案验证，还是也适用于指令遵循和生成终止。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**pass@$k$**

在最多 $k$ 次候选生成中至少有一个答案通过验证的概率，用于衡量增加推理预算后能否找到正确轨迹。 （越高越好；它直接反映搜索预算下的成功覆盖率。）

</div>
<div class="metric-item" markdown="1">

**self-consistency（SC）与 first-finish success**

SC 通过多次采样的一致答案进行聚合，诊断多数投票式解码；first-finish success 衡量首次满足终止或验证条件的生成是否成功，尤其用于 IFEval 的终止行为测试。 （越高越好；前者反映多样采样后的聚合可靠性，后者反映尽早结束时的成功率。）

</div>
<div class="metric-item" markdown="1">

**MAE（percentage points）**

目标 RL 默认策略曲线与预测或匹配的 Base 运行点之间的平均绝对误差，单位为百分点；它是主要的迁移误差指标。 （越低越好；较低误差表示规则更准确地恢复 RL 的行为曲线。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen2.5-7B 锚点模型上的 BOPTR 预算映射

<div class="result-value" markdown="1">

在 Math500、AIME、GPQA 和 IFEval 上，pass@$k$ 的 Base 恢复路径遵循 BOPTR 形式 $N_{\mathrm{Base}} \approx \alpha N_{\mathrm{RL}}^\beta$，且指数由基准决定；在 Qwen2.5-7B 上，BOPTR 的非 oracle 迁移误差为 3.41 个百分点，95% 置信区间为 [2.32, 5.53]。

</div>

这说明 RL 默认策略在这些实验条件下可以用“把 Base 的预算按基准相关的幂律重新映射”来近似，而不必把 RL 看成完全新造了一套不可搜索到的行为。它支持的是行为层面的采样效率解释，不证明 Base 与 RL 在参数、内部表示或因果机制上等价。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Qwen2.5-7B, BOPTR gives the lowest transfer error among the non-oracle rules we test, 3.41 pp (95% CI [2.32, 5.53]); a three-seed replication gives 3.07 ± 0.39 pp.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨模型与跨模型家族迁移

<div class="result-value" markdown="1">

BOPTR 被扩展到十个模型、四个模型家族，并在拟合后加入的检查点上取得 3.28 至 4.87 个百分点的误差范围。

</div>

该结果检验的不是单一 Qwen2.5-7B/Math500 曲线，而是规则能否跨规模和模型家族保持近似有效。误差仍为若干百分点，因而更适合作为行为诊断或预算规划工具，而不是精确预测器；它也不能排除某些模型或生成协议下的失败。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The rule extends to ten models across four families (3.28 to 4.87 pp on checkpoints added after fitting), to four benchmarks it was never fitted on (5.03 pp vs. 4.44 pp in fit), and holds without an RL checkpoint for the target model (4.19 pp) or without RL supervision of any kind (5.08 pp).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 未见目标模型 RL 检查点、未使用任何 RL 监督及跨基准测试

<div class="result-value" markdown="1">

在四个从未用于拟合的基准上，BOPTR 误差为 5.03 个百分点，而拟合内基准为 4.44 个百分点；没有目标模型 RL 检查点时误差为 4.19 个百分点，没有任何 RL 监督时误差为 5.08 个百分点。

</div>

这些设置测试规则是否依赖目标模型的 RL 曲线或 RL 标签。结果表明，规则在完全无目标 RL 检查点甚至无 RL 监督时仍有一定恢复能力，但跨分布误差上升，说明它更像由搜索行为和模型群体规律得到的经验映射，而不是普适定律。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The rule extends to ten models across four families (3.28 to 4.87 pp on checkpoints added after fitting), to four benchmarks it was never fitted on (5.03 pp vs. 4.44 pp in fit), and holds without an RL checkpoint for the target model (4.19 pp) or without RL supervision of any kind (5.08 pp).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验结论受 SimpleRL-Zoo 的成对 Base/RL 检查点、所用训练配方、模型家族和生成协议限制；论文将 scaling patterns 明确描述为该 recipe 和 cohort 的经验现象，不能直接推广为所有 RLVR 方法或语言模型的普遍规律。
- 跨基准和无 RL 监督设置的误差高于部分拟合内或锚点结果，且原文摘录未提供每个模型、基准、策略及置信区间的完整分解，因此尚不能判断 BOPTR 在特定困难类型、不同验证器或更大搜索预算下的失效边界。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- RL 默认策略：作为目标曲线，比较 Base 搜索运行点能否逼近 RL 在相应预算下的表现；它不是一个重新训练的模型，而是被恢复的行为参照。
- Base 默认策略：作为未经过 RL 的直接解码基线，用于衡量仅依靠模型原始采样性能时与 RL 曲线的差距。
- Base+UDF 搜索包络与近匹配策略：UDF 将 token-level sampling、beam-like search、tree search 和 sequence-level resampling 放入共享预算空间；包络表示 Base 在可测试搜索策略中的潜在性能上界，近匹配策略则寻找与 RL 运行点最接近的具体操作点。
- 低复杂度规则族与其他迁移规则：用于和 BOPTR 比较预算映射误差；其中 BOPTR 是非 oracle 规则，目标是在不使用目标测试结果直接拟合的情况下预测所需的 Base 预算。

**实验想回答的问题**

- 在相同或可比推理预算下，RL 模型的默认策略曲线能否由 Base 模型通过统一解码与搜索得到的运行点近似恢复？该问题检验 RL 增益更像是产生了 Base 模型不存在的推理能力，还是提高了对 Base 模型本已可达但较少采样的轨迹的采样效率。
- 由锚点模型与基准构造的 Budgeted Operating-Point Transition Rule（BOPTR）能否迁移到不同模型规模、模型家族、基准，以及缺少目标模型 RL 检查点或缺少 RL 监督的设置？

**实验实现**

实验使用 SimpleRL-Zoo 中成对的 Base/RL 检查点，包括 Qwen2.5-0.5B、1.5B、7B、14B、Qwen2.5-Math-7B、Llama3.1-8B 和 Mistral-7B-v0.1（仅在生成协议兼容时使用）。每个模型和基准评估 token-level 自回归策略，并在可用时加入 MCMC-like resampling、entropy branching 和 tree-style controller 等扩展搜索策略；预算为 $1,2,4,8,16$。生成结果在 $b=16$ 时去重，并复用于更小预算和全部四类指标。主要分析比较同策略曲线、Base+UDF 包络、近匹配策略和低复杂度规则族，表格以相对于 RL 默认策略目标的 MAE（百分点）报告结果。实验按锚点、横向、纵向和压力测试四类组织：锚点为 Qwen2.5-7B/Math500；横向固定模型而更换基准；纵向固定 Qwen2.5 家族而改变规模；压力测试使用跨家族及协议敏感模型。原文还报告锚点单元约需 461 H100 GPU-hours，主要成本来自八次扩展控制器运行。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 三随机种子复现实验 | Qwen2.5-7B 锚点上的 BOPTR 误差从单次报告的 3.41 个百分点进一步以三种子结果报告为 3.07 ± 0.39 个百分点。 | 该检验隔离随机种子带来的不稳定性，观察结论是否依赖一次运行。较小的均值与标准差支持结果具有一定重复性，但它仍不是对所有训练随机性或所有模型的充分验证。 | Abstract<br><span class="experiment-evidence">On Qwen2.5-7B, BOPTR gives the lowest transfer error among the non-oracle rules we test, 3.41 pp (95% CI [2.32, 5.53]); a three-seed replication gives 3.07 ± 0.39 pp.</span> |
| 去除目标模型 RL 检查点或全部 RL 监督 | 不使用目标模型 RL 检查点时误差为 4.19 个百分点；不使用任何 RL 监督时误差为 5.08 个百分点。 | 这是对方法信息依赖性的关键消融：如果没有目标 RL 轨迹仍能预测，说明规则并非单纯记忆目标模型的 RL 曲线；若完全去除 RL 监督后误差升高，则说明 RL 相关数据或拟合信息仍可能帮助校准，但不是方法运行的必要条件。 | Abstract<br><span class="experiment-evidence">The rule extends to ten models across four families (3.28 to 4.87 pp on checkpoints added after fitting), to four benchmarks it was never fitted on (5.03 pp vs. 4.44 pp in fit), and holds without an RL checkpoint for the target model (4.19 pp) or without RL supervision of any kind (5.08 pp).</span> |

**定性案例**

- IFEval 作为非数学案例，将通过率、有效性和 first-finish success 设为主要指标，并把 SC 仅作诊断使用；这一设计检验 BOPTR 是否依赖数学答案验证器。若规则在该设置仍能近似 RL 曲线，含义是其解释对象更接近预算化生成与终止行为，而不只是数学题上的正确答案搜索。原文未明确报告该案例的逐项定性样例。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper analyzes how RLVR changes LLM reasoning through inference-time search and budgeted decoding.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`81c9af429864b53ec0355ad172f27223324a4d997fe0041a7597476cf10072e8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
