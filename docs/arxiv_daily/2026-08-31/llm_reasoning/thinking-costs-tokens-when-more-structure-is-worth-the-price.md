---
title: "[论文解读] Thinking Costs Tokens: When More Structure is Worth the Price"
description: "[arXiv 2608.27506][LLM Reasoning] 本文研究语言模型的规划、检索、候选生成、验证与修复机制是否只有在令牌预算超过某一阈值后才值得采用，并将该问题具体化为单体架构与验证式搜索架构之间随预算变化的性能交叉。"
arxiv_id: "2608.27506"
announcement_date: "2026-08-31"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:43:24.935434+00:00"
source_sha256: "dcb60ec3d54d99c0fcd23542effdff9d4d6fe9695fae4da10e2332957b6f10a1"
tags:
  - "LLM Reasoning"
  - "LLM 效率"
  - "测试时计算"
  - "令牌预算"
  - "验证搜索"
  - "金融问答"
  - "过程验证"
  - "检索增强生成"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.27506</p>

# Thinking Costs Tokens: When More Structure is Worth the Price

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Thomas Nolasque, John Grey, Calista Pham, Ankit Vani</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27506v1) · [PDF 下载](https://arxiv.org/pdf/2608.27506v1) · **关键词** 测试时计算, 令牌预算, 验证搜索, 金融问答, 过程验证, 检索增强生成<br>


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

本文研究语言模型的规划、检索、候选生成、验证与修复机制是否只有在令牌预算超过某一阈值后才值得采用，并将该问题具体化为单体架构与验证式搜索架构之间随预算变化的性能交叉。

**不用术语来说**：让语言模型“先计划、再尝试多个答案、检查错误并修复”通常有助于提高答案质量，但这些步骤本身也要消耗令牌；当总预算很小时，模型可能把额度花在准备和协调上，反而没有足够空间完成真正的推理与作答。因此，实际系统设计不能只问复杂流程是否更准确，还必须判断在给定预算下，其额外开销能否换来足够的正确率收益。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 将推理架构与令牌预算联合视为实验变量，提出并检验一种明确的“性能交叉”假设：低预算时单体架构更有效，而预算足以容纳完整流程后，验证式搜索更有效。
- 在需要表格与文本证据、多步算术计算的金融问答场景中，对单体架构和验证式搜索进行配对比较，从而把“增加测试时计算通常有益”细化为“其收益取决于是否跨过架构开销阈值”的条件性结论。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于受预算约束的语言模型测试时推理研究。测试时推理是指模型部署后、无需重新训练，仅在生成答案阶段增加规划、检索、候选生成、验证或修复等步骤，以提高回答正确率；但这些步骤也会消耗输出等价令牌，因此核心问题不是单纯增加推理结构，而是判断在固定令牌预算下，额外结构何时能够抵消自身开销。论文将该问题放在金融问答场景中考察：输入同时包含财务文本、表格和问题，系统需要依据证据完成多步算术或计数推理，并输出正确答案。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试时计算与令牌预算**

测试时计算指模型在推理阶段投入额外计算步骤，而不是通过训练改变模型参数。本文以输出等价令牌数表示可用资源；规划、检索和验证占用的令牌越多，留给最终答案的空间就越少。

</div>
<div class="concept-item" markdown="1">

**检索增强生成**

检索增强生成（RAG）先从外部材料中找出与问题相关的证据，再让语言模型依据这些证据生成答案。本文的检索对象是财务文本和表格，检索结果还用于支持算术计算与引用来源。

</div>
<div class="concept-item" markdown="1">

**过程验证与修复**

过程验证不是只检查最终答案，而是检查中间推理是否具有正确算术和可追溯的证据来源。若检查器发现问题，修复模块会在剩余预算允许时重新生成或修改候选答案；所谓“标签盲”表示检查时不使用数据集提供的标准答案标签。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文比较两种在相同模型和预算条件下运行的系统。单体系统（monolith）对每个问题执行一次直接的语言模型调用，输入为问题及其财务证据，输出为答案；验证搜索系统则接收同样的金融问题、文本和表格，依次进行规划、确定性检索、候选解生成、标签盲检查和必要的修复，最后输出经筛选的答案。实验在 FinQA 和 TAT-QA 上进行，以答案正确性为主要因变量，以 14 个从 250 到 42,000 个输出等价令牌的预算层级和两种推理架构为自变量。论文假定两类系统使用同一基础模型，并将预算作为有限资源：额外结构只有在其带来的证据选择、候选多样性和错误排除收益超过结构自身开销时才有价值。研究特别关注交叉区域，即低预算时单体系统更有效，而高预算时验证搜索系统更有效的预算范围。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D_b$**

预算层级 $b$ 下，验证搜索系统准确率减去单体系统准确率所得的配对差值。

</div>
<div class="notation-item" markdown="1">

**$b$**

一个具体的输出等价令牌预算层级；本文共设置 14 个层级，范围为 250 至 42,000。

</div>
<div class="notation-item" markdown="1">

**$D_{\mathrm{low}}$**

低预算端点处的系统准确率差值，即验证搜索减去单体系统。

</div>
<div class="notation-item" markdown="1">

**$D_{\mathrm{high}}$**

高预算端点处的系统准确率差值，即验证搜索减去单体系统。

</div>

</div>

**直接相关的工作**

- **Snell et al. (2024)，测试时计算扩展**: 该工作表明，增加测试时计算有时比扩大模型参数更有效，但资源分配取决于任务难度。本文承接这一结论，将研究问题具体化为：在固定输出令牌预算下，复杂的验证搜索架构从哪个预算阈值开始优于直接调用的单体系统。
- **Kamoi et al. (2024)，语言模型自我纠错综述**: 该综述指出，没有有信息量的外部反馈时，语言模型单纯自我纠错可能无效甚至降低性能。本文因此采用不读取标准答案的标签盲检查器，验证中间算术和引用来源，把外部可检查信号用于候选筛选与修复。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

测试时增强机制会同时带来能力收益与资源成本。规划调用需要重复指令和证据，多个候选答案需要预留生成空间，检查与修复还会增加协调开销；在固定输出等价令牌预算下，这些开销可能挤占最终推理和回答所需的空间。对于多步金融推理系统，若架构选择忽略预算，原本旨在改善证据选择和算术可靠性的复杂流程可能在低预算下无法完成有效答案。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **单体式推理架构**：系统以较少的调用完成检索与回答，将大部分可用预算直接用于生成一个最终响应。其流程短、固定开销低，因此更容易在紧张预算下完成作答，但缺少多候选探索和独立检查错误的机会。
- **带验证的结构化搜索架构**：系统先规划所需证据和求解步骤，再执行检索、生成多个候选答案，并通过不接触正确标签的检查器判断候选是否有证据支持、算术是否合理，必要时进行修复。该架构试图用更广的证据覆盖、更多尝试以及提交前验证来提高正确率。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 已有研究表明增加测试时计算可能改善表现，但其最佳分配会随任务难度变化；这不足以说明一个包含规划、候选生成和验证的完整架构，在不同固定令牌预算下何时开始获得净收益。
- 自我纠错在缺少有效外部信号时并不可靠；与此同时，即使加入检查机制，规划、重复上下文和协调成本也可能耗尽低预算，使验证流程尚未发挥作用就挤掉最终答案。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有认识主要说明“更多测试时计算有时有用”或“验证需要可靠信号”，但尚未把架构固定开销与可用令牌预算放入同一受控比较中，也未严格检验是否存在一个方向发生反转的预算区间：阈值以下复杂架构落后，阈值以上复杂架构领先。仅观察高预算下的正向收益只能证明阈值效应，不能证明真正的性能交叉。

</div>
<div markdown="1"><span>核心问题</span>

在相同基础模型和金融推理任务上，额外的规划、检索、候选生成、标签盲检查与修复是否只有在输出等价令牌预算足够大时才“收回成本”；换言之，是否存在某个预算区间，使配对准确率差 $D_b$（验证式搜索减去单体架构）从低预算下的负值转为高预算下的正值？

</div>
<div markdown="1"><span>作者直觉</span>

两种架构对新增令牌的利用方式不同：单体架构固定成本较小，少量预算即可集中用于直接回答，所以低预算下更容易产出完整结果；验证式搜索必须先支付规划和协调的“入场费”，预算不足时其高级机制反而成为负担。一旦预算能够容纳完整流水线，额外令牌便可转化为更全面的证据搜索、多个独立候选以及提交前的算术核验，因此更有机会发现并排除单次直接回答中的错误。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文研究的是固定输出等价令牌预算下，两种金融推理架构如何分配有限推理资源。输入是来自 FinQA 与 TAT-QA 的问题及证据，系统使用相同的 GPT-5.4 Mini、证据序列化方式、严格答案格式和确定性 BM25 检索器；唯一改变的是推理结构：Monolith 直接检索并回答，Verified Search 则先规划，再检索、生成候选、盲检并在必要时修复。每个案例在一个预算层级下输出最终答案，并以数值字符串是否完全匹配隐藏金标准进行判定。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 数据筛选与隐藏标注准备

数据适配器校验快照哈希，安全执行标注推导，检查每个操作数是否出现在公开证据中，并排除不支持的操作、歧义尺度、缺失证据、重复文档和答案程序不一致的样本；最终从每个来源文档至多选一个问题，并保留至少需要两步推导的案例。

<div class="method-step__io" markdown="1">

**输入**：FinQA 和 TAT-QA 的本地数据快照、问题、证据文档及其标注推导。<br>
**输出**：1,000 个相互独立且平衡的案例，其中 FinQA 和 TAT-QA 各 500 个；公开输入包含问题、证据、难度和文档元数据，隐藏标签包含类型化答案、可执行金推导及各步骤证据项 ID。

</div>

**直观理解**：这一步先把数据清理成可复核的题目，并只保留确实需要多步计算的题。公开给模型的是题目和材料，正确答案及标准推导留到评测时使用。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按预算进行检索与候选生成

Monolith 发起一次直接查询，检索不超过预算允许的证据并进行一次答案调用；Verified Search 先执行最多 128 个输出令牌的规划器，对计划查询取确定性查询并集，再按顺序生成候选，每次候选调用最多 256 个输出令牌。

<div class="method-step__io" markdown="1">

**输入**：一个案例、对应证据语料、系统类型以及预算层级 $B_b$。<br>
**输出**：Monolith 产生一个候选答案；Verified Search 产生规划查询、检索结果和一个或多个候选答案，较高预算下还可能获得修复机会。

</div>

**直观理解**：单体系统像一个人读材料后直接作答；验证搜索系统先列出要查什么，再逐步形成答案，因此需要先支付额外的规划成本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 标签盲检验与修复

检查器在看不到正确答案或金标准数值的条件下，验证引用存在性、数值来源、算术安全性、候选与表达式是否一致、单位、尺度、实体、时期和除法安全性；通过的候选被接受，否则 Verified Search 可依据检查发现尝试受预算限制的修复，随后重新检查。

<div class="method-step__io" markdown="1">

**输入**：候选答案、其引用和表达式、检索证据，以及当前预算剩余量。<br>
**输出**：首个通过检查的候选及其接受索引；若没有候选通过、输出非法、工具因架构失败或预算耗尽，则该单元记为错误。

</div>

**直观理解**：检查器只判断答案是否符合材料和基本计算规则，不偷看标准答案。它更像一个不知道最终结果的校对员，发现格式或推导问题后让系统尝试改正。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 预算记账与准确率评测

对单元内所有调用计算总令牌使用量，并将输入令牌按输入与输出价格比折算为输出等价令牌；候选经过小数运算、单位和尺度归一化以及实体和时期兼容性检查后，只有数值字符串与金标准完全匹配才算正确。

<div class="method-step__io" markdown="1">

**输入**：每次调用的提示令牌数、完成令牌数、最终候选和隐藏金标准。<br>
**输出**：每个案例—系统—预算层级单元的预算使用记录、退出原因和二元正确性，并据此计算各系统在 14 个预算层级上的准确率。

</div>

**直观理解**：系统不仅记录答对没有，还记录钱和令牌花在哪里。最终采用严格的完全匹配，因此一个数值即使接近正确答案，也不会获得部分分数。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 单元硬预算约束

$$
T_{csb}=\sum_{i}(P_{csbi}+C_{csbi})\leq B_b
$$

**符号说明**

- $T_{csb}$：案例 $c$、系统 $s$、预算层级 $b$ 下，一个执行单元的总令牌使用量。
- $P_{csbi}$：该单元内第 $i$ 次调用所使用的提示令牌数。
- $C_{csbi}$：该单元内第 $i$ 次调用所使用的完成令牌数。
- $B_b$：预算层级 $b$ 的令牌上限；本文进一步把输入令牌按价格比折算为输出等价令牌。

<div class="equation-explanation" markdown="1">

**直观理解**：该约束把一个案例中所有调用的输入和输出成本加总，并要求不超过当前预算。它保证 Verified Search 的规划、检索、候选和修复不能无限追加，也使 Monolith 与 Verified Search 在相同资源上接受比较。<br>
**原文位置**：第 3.3 节，公式（2）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文没有训练或微调新的模型，而是固定使用解析后的 GPT-5.4 Mini，通过改变推理架构和预算分配进行推理时实验；因此没有报告可优化的参数化训练损失或梯度更新目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Monolith 单体基线**

该系统使用与另一系统完全相同的模型、提示核心指令、证据序列化、严格候选格式和确定性检索器，但只执行一次直接查询和一次答案调用，答案调用上限为 256 个输出令牌，不进行检查或修订。

> 直观理解：它把全部结构简化为一次检索加一次作答，用来测量不增加推理脚手架时，额外预算主要能否转化为更多证据上下文。

**2. Verified Search 推理架构**

该架构包含强制规划器、计划查询的确定性并集检索、顺序候选生成、标签盲检查和条件式修复。候选、修复次数及检索轮数随预算层级扩大，但每个动作均受预设上限和硬预算约束。

> 直观理解：它把作答拆成规划、查找、起草和校验几个环节，目的是用额外令牌减少证据遗漏和计算错误；代价是预算不足时，前面的规划可能挤占真正作答所需的空间。

**3. 硬预算账本与严格评测器**

账本在每次调用前精确计算提示令牌并预留最大输出，若可能超过剩余预算则拒绝调用；响应后释放未使用的预留并记录权威用量。评测器使用十进制算术、显式单位和尺度归一化、实体与时期兼容性检查，并要求数值字符串完全匹配。

> 直观理解：该模块防止某个系统偷偷超支，也把两种架构放在同一成本口径下比较。严格判分则确保提升来自真正正确的答案，而非宽松的近似匹配。

**训练与推理**

训练阶段未进行。推理时，对每个案例和每个预算层级分别运行 Monolith 或 Verified Search：先由预算账本核验调用是否可执行，再按系统规定完成检索与生成；Verified Search 额外执行规划、查询并集、标签盲检查和可能的修复。系统记录查询、检索 ID、候选、检查结果、修复尝试、接受索引、实际用量和退出原因，最后将接受答案与隐藏金标准进行严格数值匹配。实验共覆盖 1,000 个案例、2 个系统和 14 个预算层级，即 28,000 个预定执行单元。

**复现信息**

两种系统共享同一核心指令、证据序列化、严格候选模式、GPT-5.4 Mini 模型和确定性 BM25 检索器，因而主要受控变量是推理结构。预算层级为 250 至 42,000 个输出等价令牌；输入令牌按 GPT-5.4 Mini 的输入与输出价格比折算，文中给出的比例为 0.17。Monolith 始终一次检索并一次回答；Verified Search 的规划器上限为 128 个输出令牌、单次候选上限为 256 个输出令牌，检索轮数、候选数和修复数按预算表递增。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- FinQA：金融领域数值推理任务；论文使用其金融问答案例，但所给实验摘录未明确报告训练集、开发集、测试集划分及各划分规模。
- TAT-QA：基于金融文本和表格的问答与推理任务；论文将其与 FinQA 共同作为评测来源，但所给实验摘录未明确报告各数据集的独立样本数或划分方式。
- 合并评测案例：主实验共运行 1,000 个案例，在 2 个系统和 14 个预算层级下形成 28,000 个预定评测单元；摘录未明确报告 1,000 个案例在 FinQA 与 TAT-QA 之间的分配。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率**

1,000 个案例中回答正确的比例，用于衡量最终任务完成质量。 （越高越好，因为它表示更多案例得到正确答案。）

</div>
<div class="metric-item" markdown="1">

**标准误**

图中误差条表示 1,000 个案例准确率估计的标准误，用于表达样本估计的不确定性。 （它不是需要最大化或最小化的性能指标，而是结果稳定性的统计刻画。）

</div>
<div class="metric-item" markdown="1">

**配对 McNemar 检验的 $p$ 值**

在相同案例上比较两个系统正确与错误结果的方向性差异，用于检验交叉点两端的性能差异是否具有统计证据。 （在显著性检验语境中，较小的 $p$ 值表示反对“两个系统没有方向性差异”这一假设的证据更强；它本身不是准确率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 最低预算层级 $t250$ 与 $t500$

<div class="result-value" markdown="1">

两个系统的准确率均为 0%，因为预算不足以容纳完整提示和有效答案。该结果表明评测存在真实的资源下限，而不是系统在所有预算下都能正常运行。

</div>

当 token 预算连完整输入处理和答案生成都无法容纳时，系统没有可比较的有效推理空间。因此，低预算下的 0% 不能单独说明某种算法推理能力差，只能说明资源约束先于推理质量成为瓶颈。

<div class="result-source" markdown="1">

来源：第 4.2 节 Accuracy by system and tier；第 4.5 节 Floor effects

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Both systems score 0% at the t250 and t500 tiers, since at these budgets, neither system can fit a complete prompt and produce a valid answer before exhausting the token cap.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 预算交叉区间 $t1000$ 与 $t1500$

<div class="result-value" markdown="1">

在 $t1000$，monolith 准确率为 18%（180/1000），verified search 为 0.1%（1/1000）；在 $t1500$，verified search 首次超过 monolith，准确率分别为 24% 与 20.6%。因此交叉点位于 1,000 至 1,500 个输出等价 token 之间。低端点和高端点的配对 McNemar 检验均报告 $p\leq 0.001$：$t1000$ 有 180 个偏向 monolith 的不一致样本、1 个偏向 verified search 的样本，$t1500$ 则有 78 个偏向 verified search、44 个偏向 monolith 的样本。

</div>

单体系统在较小预算下更早可用，因为它把预算集中于一次检索和一次回答；verified search 必须先支付规划调用的固定开销。预算达到 $t1500$ 后，多阶段流程才完整运行，并且结构化推理带来的收益超过规划成本。该检验支持“存在严格交叉”的统计说法，但不能证明交叉点在其他模型、任务或预算设计下仍完全相同。

<div class="result-source" markdown="1">

来源：第 4.2 节 Accuracy by system and tier；第 4.3 节 The crossover region

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At t1500, verified search overtakes the monolith for the first time, achieving 24% versus 20.6%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 高预算至 $t42000$

<div class="result-value" markdown="1">

从 $t1500$ 开始，verified search 在每个后续预算层级都保持领先；随着预算增加，monolith 从 $t1000$ 的 18% 上升到 $t42000$ 的约 40%，verified search 从 $t1500$ 的 24% 上升到 $t42000$ 的约 44%。高预算允许 verified search 使用多轮检索、多个候选答案和修复循环。

</div>

额外预算对两个系统都有帮助，但帮助方式不同：monolith 主要获得更丰富的检索上下文，系统结构不变；verified search 则能把新增预算转化为更多候选生成、错误拒绝和修复机会。因此，结果支持“在预算足够后验证结构有稳定优势”，但约 4 个百分点的最高层级差距不等于每个具体案例都得到同样收益。

<div class="result-source" markdown="1">

来源：第 4.2 节 Accuracy by system and tier

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

From t1500 onward, verified search maintains a consistent advantage over the monolith at every tier.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验摘录只明确说明使用 FinQA 和 TAT-QA、1,000 个主案例及 14 个预算层级，但未报告两个数据集的样本分配、数据划分、抽样策略或各自准确率，因此难以判断结论是否由某一数据集主导。
- 实验只比较一个已解析的 GPT-5.4 mini 模型和两种系统配置；摘录未报告其他模型、其他预算单位或更多任务上的复现结果。因此，1,000 至 1,500 个输出等价 token 的交叉区间应理解为本实验设置下的估计，而不是所有语言模型和任务的普遍阈值。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Monolith：单次 LLM 调用的单体基线；它代表不显式加入规划、验证或修复的直接回答方式，因此可以检验额外推理结构是否值得其 token 成本。
- Verified search：被评估的结构化系统，加入规划、标签盲检查和修复能力；它不是无结构基线，而是用于检验多阶段搜索与验证机制相对于单体调用的净收益。

**实验想回答的问题**

- 在不同输出等价 token 预算下，单体系统与加入规划、检查和修复的 verified search 系统，其准确率如何变化？
- 是否存在一个预算交叉点：低于该点时结构化推理的额外开销损害性能，高于该点时其搜索、验证和修复收益超过开销？

**实验实现**

实验使用已解析的模型 `gpt-5.4-mini-2026-03-17-eastus-dz`，通过 LLM gateway API 记录用量。每个系统在 14 个预算层级上运行，预算范围为 250 至 42,000 个输出等价 token；主实验包含 1,000 个案例、28,000 个预定单元。比较重点是预算受限条件下的端到端准确率，而不是只比较某个中间模块。机制追踪进一步记录调用次数、候选答案数量和修复机制使用比例，以解释准确率曲线是否确实由系统结构造成。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 预算层级与系统可执行性的机制追踪：$t1000$ 对比 $t1500$ | 在 $t1000$，verified search 平均调用 1.01 次、每个单元仅产生 0.01 个候选答案；在 $t1500$，平均调用 2.0 次并产生 1.0 个候选答案。monolith 在 $t1000$ 及以上始终恰好调用 1 次并产生 1 个候选答案。 | 这不是删除某一个模块的传统消融，而是通过改变预算观察流程何时能够落地。结果定位了交叉点的机制原因：verified search 在 $t1000$ 主要消耗于规划，无法进入候选生成；到 $t1500$ 才能完成基本流水线。monolith 没有额外阶段，所以新增预算只丰富其检索上下文，而不会增加结构性步骤。 | 第 4.4 节 Mechanism traces<br><span class="experiment-evidence">At t1500, it averages 2.0 calls and 1.0 candidate, indicating the pipeline first fits at this tier.</span> |
| 高预算下的修复机制使用 | 在 $t8000$ 及以上，verified search 平均调用 2.6 次、产生 1.4 个候选答案，且 12% 至 19% 的单元使用修复机制。 | 该观察说明高预算优势并非只来自一次更长的回答，而是来自额外候选、检查和修复循环。不过，摘录没有提供“移除修复机制”后的独立准确率，因此不能把准确率提升唯一归因于修复模块，也不能据此估计该模块的边际贡献。 | 第 4.4 节 Mechanism traces<br><span class="experiment-evidence">At t8000 and above, verified search averages 2.6 calls and 1.4 candidates, with 12-19% of cells using the repair mechanism.</span> |

**定性案例**

- 原文未提供单个案例的输入、推理过程、错误答案与修复答案；第 4.4 节提供的是单元层面的机制统计，而非可复核的定性案例。因此，不能据此展示某个具体金融问题如何被检查或修复。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文研究规划、验证和修复等推理结构在不同 token 预算下的收益与开销权衡。; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`dcb60ec3d54d99c0fcd23542effdff9d4d6fe9695fae4da10e2332957b6f10a1`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
