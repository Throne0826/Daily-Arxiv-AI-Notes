---
title: "[论文解读] Divergent-Convergent Reasoning: Scaling Test-Time Compute through Structured Solution Synthesis"
description: "[arXiv 2608.15303][LLM Reasoning] 本文研究如何把测试时算力从固定、均匀的多次采样，转化为围绕候选解分歧进行审查、综合与按需追加的推理过程，从而在没有训练判别器的条件下挽救正确的少数意见。"
arxiv_id: "2608.15303"
announcement_date: "2026-08-18"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:13:19.725168+00:00"
source_sha256: "a4186f2f83ecdcf92e282371d67477a5ed606262364ef13f5c4dabd33af83eca"
tags:
  - "LLM Reasoning"
  - "测试时计算扩展"
  - "大语言模型推理"
  - "多智能体推理"
  - "候选解协调"
  - "少数正确答案放大"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.15303</p>

# Divergent-Convergent Reasoning: Scaling Test-Time Compute through Structured Solution Synthesis

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Bo Wen, Yuhao Chen, Erhan Bilal, Carla Agurto Rios, Chen Wang, Junchen Jiang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: School of Computing, Queen’s University, Kingston, Ontario, Canada；Affiliation: IBM T.J. Watson Research Center, USA；Affiliation: Department of Computer Science, University of Chicago, USA；Affiliation: Tensormesh Inc., USA</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.15303) · [PDF 下载](https://arxiv.org/pdf/2608.15303) · **关键词** 测试时计算扩展, 大语言模型推理, 多智能体推理, 候选解协调, 少数正确答案放大<br>


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

本文研究如何把测试时算力从固定、均匀的多次采样，转化为围绕候选解分歧进行审查、综合与按需追加的推理过程，从而在没有训练判别器的条件下挽救正确的少数意见。

**不用术语来说**：面对一道难题，大语言模型可以重复作答，再从多个答案中选出最终答案；但最常见的答案未必正确，一个出现次数较少的候选反而可能包含关键推理。现实系统还必须决定哪些题值得继续投入算力，而在得到答案之前准确判断题目难度通常很困难。本文要解决的核心实际问题，是如何利用候选答案之间的分歧识别有价值的少数解，并把有限的额外计算集中用于仍有争议的问题。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出发散—收敛推理（DCR）：先独立生成多种候选解，再由审查调用分析分歧并综合最终答案；其重点不是按出现频率直接表决，而是检查候选推理的论证质量，使正确答案处于少数时仍可能被恢复。
- 作者进一步提出递归 DCR 与无需训练的离散度诊断：系统逐轮审查争议，在审查者一致时提前停止，否则继续分配测试时算力；离散度则用于判断当前分歧是否处于值得追加计算的区间。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型的测试时计算扩展，即模型在推理阶段投入更多生成或评审计算，以提高复杂问题的回答准确率。典型做法是独立采样多个候选解，再通过多数投票、聚合或评估选出一个答案；本文关注其中一个关键问题：当候选解彼此不一致，尤其当正确答案只出现在少数候选中时，额外的协调计算能否识别并利用这一少数意见。论文将该过程概括为先发散生成候选方案，再收敛分析分歧并综合答案的两阶段推理。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试时计算扩展**

指模型参数训练完成后，在实际回答问题时增加采样、搜索或评审等计算。直观上，同一个问题可以让模型尝试更多次，并用额外步骤筛选或整合这些尝试。

</div>
<div class="concept-item" markdown="1">

**自洽性与多数投票**

自洽性方法对同一问题生成多个推理结果，并选择出现次数最多的答案，隐含假设是正确答案通常占多数。它计算简单，但可能忽略少数候选中的正确论证。

</div>
<div class="concept-item" markdown="1">

**验证器与无验证器推理**

验证器是能够判断候选答案或推理过程是否正确的外部反馈信号，可以是规则、奖励模型或专门训练的评估器。无验证器方法在答案揭晓前没有可靠的真值反馈，因此需要依靠候选之间的结构化讨论、评审或聚合来分配有限计算预算。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个需要推理的问题输入，系统首先生成多个相互独立且具有差异的候选解，形成候选池；随后使用若干评审调用分析候选之间的分歧，并综合得到一个最终答案。本文研究的核心设定是在答案真实标签或可靠验证器不可用的情况下，如何利用有限的测试时计算，特别是如何处理正确候选可能处于少数的情形。单轮方法使用固定数量的评审调用；递归方法按轮次重复协调，在评审调用达成一致或计算预算耗尽时停止，并输出最终答案。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$K$**

评审宽度，即每一轮并行调用的评审数量。单轮设置的默认值为 $K=25$，递归设置的默认值为 $K=8$。

</div>
<div class="notation-item" markdown="1">

**$DCR$**

Divergent–Convergent Reasoning，即发散—收敛推理框架：先生成多个候选解，再由评审过程分析分歧并综合单一答案。

</div>
<div class="notation-item" markdown="1">

**$T_d$**

测试时计算预算或计算投入；本文用它表示推理阶段可用于候选生成、评审和递归协调的有限资源。原文未给出统一的形式化定义。

</div>
<div class="notation-item" markdown="1">

**$s(x)\in\{\mathrm{task},\mathrm{harm}\}$**

该符号未在所给论文节选中定义，因此不能据此确定其在本文中的具体含义。原文未明确报告。

</div>

</div>

**直接相关的工作**

- **多数投票与自洽性方法**: 这是本文最直接的聚合基线：对多个候选解进行采样并选择多数答案。DCR 保留多候选生成这一基本范式，但增加评审式协调，目标是恢复多数投票会丢失的正确少数答案。
- **ReConcile**: ReConcile 使用多模型、多轮讨论和置信度加权投票达成共识，与 DCR 都利用多实例交互来改善答案选择。本文强调二者机制不同：DCR 使用评审者分析候选分歧，专门研究正确少数意见的放大，并采用评审调用一致即停止的递归规则。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

测试时计算扩展可以通过生成和审查更多候选解提高大语言模型的推理准确率，但部署环境通常具有严格的调用、延迟或成本预算，并且可能缺少真实标签与经过训练的判别器。因此，系统既要从相互矛盾的候选推理中得到可靠结论，也要在线判断何时继续计算、何时停止，避免对所有问题机械地投入同等资源。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **多样本生成与多数投票**：对同一问题独立采样多个答案，再选择出现频率最高的答案。该方法把样本间的一致性视为正确性的近似信号，流程简单，但主要利用答案计数，而不深入比较少数候选所包含的推理依据。
- **判别器或预测式路由方法**：判别器方法利用奖励信号、真实标签或专门训练的验证模型评价候选解；预测式路由则在正式求解前，根据输入特征估计难度并决定模型或算力预算。两者都试图把额外计算投向更需要它的问题。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 多数投票默认占多数的答案更可信，因而把分歧主要视为需要平均掉的噪声；当多个样本重复同一种错误、而正确推理仅占少数时，它会系统性丢弃有价值的少数意见，也无法利用候选论证之间的结构性差异。
- 判别器依赖可获得的奖励信号、标签或额外训练，而预测式路由需要在尚未求解时预判计算需求，对新任务或分布变化可能泛化不足；固定计算方案又会对简单题浪费调用，并可能没有为真正困难但可恢复的问题投入足够审查。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法尚未给出一种统一、无需训练判别器的机制，同时完成两件事：首先，通过审查候选推理而非仅统计答案频率，从少数候选中恢复可能正确的论证；其次，把候选间的实际分歧转化为在线控制信号，自适应决定是否继续投入测试时算力。尤其缺少对“何种分歧能够通过进一步协调被修复”的系统研究。

</div>
<div markdown="1"><span>核心问题</span>

候选解之间的分歧，特别是包含正确答案的少数意见，能否被结构化的发散—收敛过程稳定利用；进一步地，系统能否根据逐轮协调结果与分歧程度按需追加计算，在固定预算聚合和多数投票之外获得更好的准确率—计算成本权衡？

</div>
<div markdown="1"><span>作者直觉</span>

作者的出发点是“选择通常比从零生成更容易”：模型第一次作答时可能难以独立找到正确推理，但当多个候选已经把不同思路摆在一起后，审查者可以比较假设、步骤与结论，识别少数解中的关键证据。分歧也并非只有负面意义：低分歧通常表示可以停止，中等分歧可能意味着正确线索已经出现但尚未占优，适合继续协调，而极端分歧可能表示模型能力不足。因而先少量采样、再观察分歧，比仅凭题目表面特征预估难度更能反映当前模型对该题的实际不确定性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Divergent–Convergent Reasoning（DCR）是一种无需外部验证器的推理时答案合成框架。在给定问题 $Q$ 和以模型 API 调用总数衡量的计算预算后，系统先独立采样 $N$ 个候选解，形成解池 $S=\{x_n\}_{n=1}^{N}$；随后调用与提案生成者角色分离的审稿模型，对候选解中的共识、分歧和少数意见进行结构化审查，并生成新的协调答案。其目标不是选择票数最多的原答案，而是利用候选解之间的分歧定位推理难点，再重新推导这些关键步骤，最终返回预测答案 $\hat{x}$。

DCR既可只执行一轮协调，也可递归执行：每轮产生的 $K$ 个审稿结果成为下一轮的提案池；若一轮内所有审稿调用给出相同最终答案，系统立即停止，否则继续协调直至达成一致或耗尽最大调用预算。直观地说，它先让多个“解题者”独立提出方案，再让一组“审稿人”比较各方案为什么一致或冲突；遇到简单题时迅速一致，遇到难题时则用更多轮次反复检查争议点。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 问题输入与预算设定

系统以探索和协调阶段的模型 API 调用总数衡量预算，而不以生成 token 数衡量；推理过程中不访问标准答案、奖励模型或外部验证器。

<div class="method-step__io" markdown="1">

**输入**：待求解任务 $Q$、可调用的一个或多个大语言模型，以及最大推理时计算预算。<br>
**输出**：受最大调用次数约束的推理任务实例。

</div>

**直观理解**：API 调用次数是系统可直接控制的资源，因此便于在不同答案聚合方法之间进行计算量匹配。这个设定相当于规定委员会最多能请多少位解题者和审稿人，而不是规定每个人能说多少字。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 发散式探索

使用不同随机种子或温度，对一个或多个大语言模型副本进行相互独立的随机采样；模型可以同构，也可以构成异构集成，由此得到候选解 $\{x_n\}_{n=1}^{N}$。

<div class="method-step__io" markdown="1">

**输入**：问题 $Q$ 与候选解数量 $N$。<br>
**输出**：包含全部候选解的初始解池 $S=\{x_n\}_{n=1}^{N}$。

</div>

**直观理解**：这一阶段刻意保留不同思路，而不急于形成共识。它类似于让多个互不交流的小组分别解同一道题，以增加覆盖正确推理路径的机会。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 收敛式结构化协调

并行执行 $K$ 次独立审稿调用；每位审稿模型先识别多数候选共有的步骤，再定位候选之间发生分歧的准确位置，最后验证共识部分、重新推导争议部分，并检查少数意见是否包含多数解遗漏的关键修正。

<div class="method-step__io" markdown="1">

**输入**：当前解池 $S$ 与每轮审稿宽度 $K$。<br>
**输出**：本轮产生的 $K$ 个新协调解及其最终答案。

</div>

**直观理解**：审稿人不是给现有答案简单投票，而是检查答案为什么不同，并据此写出一份新的完整解答。这样，即使多数候选犯了同一种错误，少数候选中的有效线索仍可能被保留并扩展。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 递归细化与一致同意停止

若 $K$ 次审稿调用给出的最终答案完全相同，则提前停止并返回该答案；若仍有分歧，则把本轮协调解作为下一轮提案池继续执行协调，直到达成一致或达到最大轮数或调用预算。

<div class="method-step__io" markdown="1">

**输入**：当前轮的 $K$ 个协调解、已消耗调用次数及最大预算。<br>
**输出**：最终答案 $\hat{x}$，以及由停止时机决定的实际推理计算量。

</div>

**直观理解**：简单问题通常一轮就能取得一致，因此少花计算；持续存在争议的问题会自动获得更多审查轮次。这是一种由内部意见分歧驱动的资源分配机制，但一致并不等于正确，因为系统没有外部验证器。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。DCR是训练无关的推理时框架，所给章节没有定义新的模型训练损失、参数更新规则或监督信号；候选生成、结构化审稿、递归反馈和离散度诊断均在不更新模型参数的情况下执行。其任务层面的目标是让最终答案 $\hat{x}$ 尽可能正确，但由于推理时没有标准答案或验证器，这一目标并未被写成可直接优化的损失函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 独立候选生成器**

该模块通过不同随机种子或采样温度独立生成 $N$ 个提案，也允许使用多个不同模型组成异构集成。独立性和随机性用于提高解池中的推理路径覆盖率。

> 直观理解：如果所有解题者都沿着完全相同的思路作答，后续审查就没有可比较的信息；多样化采样为系统提供不同假设、步骤和潜在纠错线索。

**2. 审稿人—作者角色分离的协调器**

协调器接收完整解池，并要求每个审稿调用显式完成共识识别、分歧定位、少数意见检查和新答案合成。审稿模型产生的是重新组织并推导出的协调解，而非对原候选的多数投票或简单选择。

> 直观理解：角色分离让第二阶段以批判性检查为任务，而不是继续重复第一阶段的独立作答。它的核心价值是把“大家在哪一步意见不同”转化为下一次推理的重点。

**3. 递归控制器**

控制器逐轮比较 $K$ 个审稿调用的最终答案：完全一致时提前终止，否则将本轮输出反馈到下一轮，并以最大轮数或总调用预算作为硬上限。每轮宽度 $K$ 与最大预算是其主要控制参数。

> 直观理解：该模块把计算从固定平均分配改为按分歧持续程度分配。需要注意，它检测的是答案字符串或最终答案的一致性，而不是经外部证明确认的正确性。

**训练与推理**

训练阶段：原文没有为DCR设置专门训练流程，直接使用已有大语言模型作为候选生成器和审稿器。推理阶段：输入问题 $Q$ 后，先通过独立随机采样获得 $N$ 个候选解并组成 $S$；再以审稿宽度 $K$ 并行生成协调解。单轮版本在一次协调后结束；递归版本检查本轮 $K$ 个最终答案是否一致，一致则返回该答案，不一致则把协调输出反馈为下一轮解池，并重复该过程直至一致或预算耗尽。

这一流程属于无验证器的测试时计算扩展：系统既不根据真实标签挑选答案，也不依靠独立判分器决定继续与否，而是将审稿人之间是否仍有分歧作为控制信号。因此，它能够自适应决定调用次数，但也存在共同错误导致过早一致的风险；可选离散度信号只能用于诊断或分流，不能证明最终答案正确。

**复现信息**

公平解释该方法需要保留四项关键设置。第一，计算量按探索与协调的 API 调用总数统计，因为调用次数是可控变量，而输出 token 数会随模型和题目难度内生变化。第二，发散阶段需使用独立采样，并通过不同随机种子或温度促进多样性；模型既可相同，也可异构。第三，协调提示词必须明确要求识别共识步骤、定位分歧步骤、保留并检查少数意见，再合成完整新解，否则实现会退化为普通投票或同伴讨论。第四，递归实现必须记录每轮宽度 $K$、一致性判定方式、最大轮数或最大调用预算，并将当前轮的协调输出完整传入下一轮。

所给章节在实验示例中报告单轮设置使用 $K=25$，递归设置每轮使用 $K=8$，但这些是被评估的配置而非算法固有常数。原文还说明审稿提示词位于附录B、离散度正式定义位于附录C；当前摘录未包含二者全文，因此无法从所给材料严格复现提示模板、答案规范化规则或离散度计算方法。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MATH500：具有标准答案的高难度数学推理基准。实验用它检验模型能否从包含正确与错误推导的候选池中识别可靠解法；原文节选未明确报告所用划分细节，但表中按完整基准名称汇报结果。
- AIME 2024 与 AIME 2025：竞赛数学基准，分别用于检验方法在不同年度高难度题目上的泛化表现。原文未明确报告具体题数、筛选方式或划分；两者特别适合观察基础采样准确率很低时，协调过程能否恢复少数正确提案。
- MMLU-PRO：覆盖多领域的高难度知识与推理基准，用于检验收益是否超出数学任务。原文节选未明确报告类别规模与划分，并说明更细的类别结果位于附录 E。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Trial accuracy（逐次尝试准确率）**

在全部 $I$ 道题和每题 $T$ 次随机试验中，最终答案与标准答案相同的比例，即 $\mathrm{Acc}_{\text{trial}}=\frac{1}{IT}\sum_{i=1}^{I}\sum_{t=1}^{T}\mathbb{I}[a_{i,t}=a_i^\star]$。其中 $a_{i,t}$ 是第 $i$ 题第 $t$ 次试验的答案，$a_i^\star$ 是标准答案。它衡量一次独立调用平均有多大概率成功。 （越高越好，因为它表示随机运行 DCR 时获得正确最终答案的平均概率更高；但它不能单独区分稳定掌握与偶然猜中。）

</div>
<div class="metric-item" markdown="1">

**Consistency（多数正确率）**

对每道题先判断 $T$ 次试验中是否有严格超过 $50\%$ 的试验正确，再计算满足该条件的题目比例，即 $\mathrm{Acc}_{\text{cons}}=\frac{1}{I}\sum_{i=1}^{I}\mathbb{I}[\frac{1}{T}\sum_{t=1}^{T}\mathbb{I}[a_{i,t}=a_i^\star]>0.5]$。它关注正确答案能否从偶发少数变为稳定多数。 （越高越好，因为更多题目在重复运行时形成正确多数，因而更可能通过多数投票稳定得到正确答案。）

</div>
<div class="metric-item" markdown="1">

**API calls（计算预算）**

以审阅调用次数衡量测试时计算量。递归设置每轮使用审阅宽度 $K=8$，若三轮结束约需 $8\times3=24$ 次调用，接近单轮设置的 $T=25$ 次随机协调试验；最多十轮时可达 $80$ 次调用。 （在准确率相当或更高时越低越好；它衡量方法能否让简单题因一致同意而提前停止，把更多计算留给尚未收敛的困难题。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### AIME 2024，GPT-OSS-120B，自有提案池上的单轮 DCR

<div class="result-value" markdown="1">

相较 Sampling，Trial accuracy 从 $74.3\%$ 提升到 $88.1\%$，增加 $13.8$ 个百分点；Consistency 从 $76.7\%$ 提升到 $90.0\%$，增加 $13.3$ 个百分点。

</div>

作者据此主张，协调不仅提高单次调用的成功概率，还使更多题目在重复运行中形成正确多数。分析上，这支持 DCR 能筛选和综合候选方案，但不能单独证明收益来自真正的逻辑纠错，因为审阅阶段使用了额外计算，且没有与严格等计算量的所有替代策略逐一比较。

<div class="result-source" markdown="1">

来源：第 5.1 节；表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For example, on AIME 2024, GPT-OSS improves from 74.3% trial accuracy (Sampling) to 88.1% (DCR Single), and from 76.7% consistency to 90.0%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### MATH500，Llama-4-Maverick-17B-128E，自有提案池上的单轮 DCR

<div class="result-value" markdown="1">

Trial accuracy 从 Sampling 的 $36.4\%$ 提升到 DCR (Single) 的 $73.7\%$，增加 $37.3$ 个百分点；表 1 同时给出 Consistency 从 $35.8\%$ 提升到 $74.0\%$。

</div>

结果说明即使基础采样只有约三分之一正确，只要候选池中仍含有可识别的正确推导，协调也可能把少数信号放大为稳定多数。不过，这一结果不意味着 DCR 能在完全没有正确线索时凭空求解，也不能由单个模型与数据集组合推断所有任务都会获得同等幅度的提升。

<div class="result-source" markdown="1">

来源：表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MATH500 | Llama-4 | 36.4 | 73.7 | 79.1 | 35.8 | 74.0 | 79.0

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 递归 DCR，相对于预算为 $50$ 次调用的单轮 DCR

<div class="result-value" markdown="1">

作者报告递归 DCR 通过一致同意提前停止，使平均计算量降低约 $27\%$，同时达到更高准确率；节选未给出对应准确率、平均调用次数及分数据集数值。

</div>

这一结果支持“按题目难度动态分配计算”的设计：容易题较快达成一致，困难题继续接受审阅。由于当前节选缺少表 2 的完整数据、方差和停止轮数分布，只能确认作者给出的总体比较，不能核验提升大小，也不能判断节省是否在各数据集上都成立。

<div class="result-source" markdown="1">

来源：第 5.2 节；表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Recursive DCR stops early on easy problems (unanimity), reducing average compute by ∼27%, while achieving higher accuracy.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 论文把 Consistency 视为 Majority Vote 的对应量，并以独立同分布公式从 Trial accuracy 联系 Pass@$N$，但这些不是独立运行的基线。DCR 各次试验共享固定提案池，试验间可能相关；同时真正的 Best-of-$N$ 还需要验证器选出正确候选，因此这些近似不等同于完整的计算匹配比较。
- 节选未报告置信区间、随机种子敏感性、每个数据集的实际评测题数以及递归实验的完整表 2 数值。尤其是 AIME 等规模较小的基准，少量题目的变化可能造成较大的百分点波动；因此“跨数据集一致提升”和约 $27\%$ 计算节省仍需结合完整论文数据与源码复核。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Sampling：发散探索阶段直接进行随机采样，不执行协调，是判断性能增益是否来自收敛协调步骤的主要基线。
- DCR (Single)：审阅模型只协调自己生成的提案池。它既是单轮 DCR 的核心设置，也为混合提案实验提供对照，用于区分“协调本身”与“跨模型提案多样性”的作用。
- Majority Vote：论文没有另行执行独立多数投票实验，而以一致性指标近似其正确率；若某题超过一半试验正确，则对这些试验进行多数投票也会得到正确结果。
- Best-of-$N$/Pass@$N$：论文用单次试验准确率 $p$ 及独立同分布近似 $\mathrm{Pass@}N\approx1-(1-p)^N$ 建立联系，并未实际运行带有答案验证器的 Best-of-$N$。因此它只能说明候选覆盖概率，不能直接证明系统能够识别并选出其中的正确答案。

**实验想回答的问题**

- 单轮收敛协调能否把发散探索阶段偶尔出现的正确少数方案转化为稳定的多数正确结果，并同时提高逐次尝试准确率与跨试验一致性？
- 提案来源、审阅模型能力和递归轮数如何影响协调效果：混合强弱模型的提案是否优于模型自审，以及递归协调能否按题目难度动态分配测试时计算量并趋于一致？

**实验实现**

实验使用 Granite-4-H-Small、Llama-3.3-70B、Llama-4-Maverick-17B-128E 和 GPT-OSS-120B，GPT-OSS 仅采用默认或中等推理强度。实验 1 中，每个模型先为每题生成自己的候选提案池，再由同一模型以审阅宽度 $K=25$ 完成一轮协调；固定该提案池并重复 $T=25$ 次随机协调，以估计结果可靠性。实验 2 把四个模型在实验 1 中的提案合并，再抽取 $25$ 个候选，使提案池近似反映四个模型等量贡献时的平均准确率；随后分别让各模型审阅该混合池。实验 3 采用递归 DCR：每轮生成 $K=8$ 个审阅结果，将协调结果继续输入下一轮，达到全体一致时提前停止，否则运行到最大轮数；正文主要报告 GPT-OSS-120B 同时负责生成提案和审阅的设置。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| AIME 2024，Llama-3.3 审阅自有提案池与四模型混合提案池 | DCR (Single) 的 Trial accuracy 为 $23.2\%$，改用 DCR (Mix) 后达到 $62.4\%$，增加 $39.2$ 个百分点；Consistency 从 $23.3\%$ 提升到 $63.3\%$。 | 该对照主要隔离提案来源的影响，因为审阅模型保持为 Llama-3.3，而候选池从自有提案变为强弱模型混合提案。大幅提升表明弱审阅者可以利用其他模型提供的高质量线索，但实验同时改变了候选的能力构成与多样性，无法进一步区分收益究竟来自强模型答案、表达多样性还是二者共同作用。 | 表 1；第 5.1 节<br><span class="experiment-evidence">AIME 2024 \| Llama-3.3 \| 13.2 \| 23.2 \| 62.4 \| 16.7 \| 23.3 \| 63.3</span> |
| AIME 2024，GPT-OSS-120B 审阅自有提案池与四模型混合提案池 | 从 DCR (Single) 改为 DCR (Mix) 后，Trial accuracy 由 $88.1\%$ 降至 $84.0\%$，下降 $4.1$ 个百分点；Consistency 由 $90.0\%$ 降至 $83.3\%$，下降 $6.7$ 个百分点。 | 该对照显示混合提案并非单调有益：强模型自有候选已经质量较高，加入弱模型的错误推导可能稀释有效证据。作者将其描述为提案“污染”并引发幻觉或偏离正确路径；从实验本身能确认的是性能下降，具体认知机制仍属于作者解释，尚未由错误类型标注或受控噪声实验直接验证。 | 表 1；第 5.1 节<br><span class="experiment-evidence">AIME 2024 \| GPT-OSS \| 74.3 \| 88.1 \| 84.0 \| 76.7 \| 90.0 \| 83.3</span> |

**定性案例**

- 论文给出的代表性模式是“正确少数放大”：某题在 Sampling 中只有少数试验得到正确答案，因此整体表现不稳定；协调器比较不同推导后反复选择或综合正确路径，使该题超过 $50\%$ 的试验正确。当前节选没有提供具体题目、候选推导文本或逐轮轨迹，因此这一机制主要由 Trial accuracy 与 Consistency 的联合变化间接支持，不能据此判断协调器究竟完成了逻辑验证、答案复用还是多数模式匹配。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper scales test-time reasoning compute by generating divergent solutions and synthesizing them into a converged answer.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`a4186f2f83ecdcf92e282371d67477a5ed606262364ef13f5c4dabd33af83eca`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
