---
title: "[论文解读] ParaTempo: Efficient Parallel Reasoning via Temporal Confidence"
description: "[arXiv 2608.16425][LLM 效率] ParaTempo通过跟踪每条推理分支在一段时间内是否持续收敛到同一答案，异步决定分支的剪枝、提前退出、复制扩展与全局停止，从而减少并行推理中的冗余计算。"
arxiv_id: "2608.16425"
announcement_date: "2026-08-18"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:11:49.984903+00:00"
source_sha256: "131d407020d7eddc6258e79959b4e04c8b638dd30b01bd8830dab3f39ad045a8"
tags:
  - "LLM 效率"
  - "LLM Reasoning"
  - "并行推理"
  - "测试时扩展"
  - "自洽性"
  - "时间置信度"
  - "中间答案探测"
  - "异步分支控制"
  - "动态计算分配"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2608.16425</p>

# ParaTempo: Efficient Parallel Reasoning via Temporal Confidence

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Xuteng Zhang, Wenhao Zeng, Xiaodong Gu, Chao Hu, Haotian Lin, Yuling Shi, Min Wang, Beijun Shen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Shanghai Jiao Tong University；University of Pennsylvania</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.16425) · [PDF 下载](https://arxiv.org/pdf/2608.16425) · **关键词** 并行推理, 测试时扩展, 自洽性, 时间置信度, 中间答案探测, 异步分支控制, 动态计算分配<br>
**代码**: [https://github.com/ScottZhang812/ParaTempo](https://github.com/ScottZhang812/ParaTempo)

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

ParaTempo通过跟踪每条推理分支在一段时间内是否持续收敛到同一答案，异步决定分支的剪枝、提前退出、复制扩展与全局停止，从而减少并行推理中的冗余计算。

**不用术语来说**：让大模型同时尝试多种解题路径通常比只尝试一次更可靠，但也会产生大量浪费：有些路径已经基本确定答案，却仍在继续生成；有些路径长期摇摆、希望不大，却持续占用算力。真正困难的是，在完整答案尚未生成时，系统如何可靠地判断每条路径是正在稳定收敛，还是仍然混乱，并据此及时调整计算资源。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出“时间置信度”，即根据同一推理分支近期多次中间探测得到的暂定答案概率分布，衡量其概率质量是否持续集中于一个主导答案；该信号关注答案随时间的稳定趋势，而非单个时刻或单个词元的置信程度。
- 提出无需训练的异步并行推理框架 ParaTempo，以时间置信度统一驱动低置信分支剪枝、稳定分支提前退出、空闲预算重新分配、优良分支复制扩展以及全局提前终止，避免所有分支等待同一同步屏障。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型的测试时扩展与并行推理研究。其基本做法是在回答同一道数学或科学推理题时，同时采样多条推理轨迹，再汇总各轨迹的候选答案，以降低单条推理偶然出错带来的风险。传统自洽性方法通常为每条分支分配相同生成预算，并等到全部分支结束后才投票；但不同分支的推进速度和潜在价值并不相同，已经稳定的分支会继续生成冗余内容，长期不确定的分支也可能持续占用算力。因此，本文把并行推理重新表述为一个在线、分支级的计算资源控制问题：系统需要在推理尚未完成时判断各分支是否正在收敛，并据此动态决定保留、剪枝、提前结束、复制分支以及全局停止。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试时扩展**

测试时扩展是指不重新训练模型，而是在推理阶段投入更多计算，例如生成更长的推理链或采样更多候选解，以提高答案可靠性。本文主要扩展并管理并行采样的宽度。

</div>
<div class="concept-item" markdown="1">

**自洽性**

自洽性是对同一问题独立生成多条推理轨迹，并依据最终答案的一致程度进行投票的方法。它能提高鲁棒性，但固定采样数量和统一生成预算无法利用不同分支之间的进度差异。

</div>
<div class="concept-item" markdown="1">

**中间答案探测**

中间答案探测是在一条推理轨迹尚未生成完毕时，周期性询问模型当前更倾向于哪些候选答案，并得到暂定答案的概率分布。单次探测可能因局部措辞或短暂犹豫而波动，因此本文关注一段时间内连续探测结果的集中与稳定程度。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一道需要多步推理的问题、一个能够生成推理轨迹并输出暂定答案分布的大语言模型，以及可用于并行生成的计算预算。系统同时维护多条相互独立且不要求同步推进的活跃分支，并周期性探测每条分支当前的候选答案概率分布；目标是在尽量保持并行推理准确率的前提下，减少总生成 token 数和关键路径延迟。控制器必须在生成过程中完成两层决策：局部上判断某条分支应继续、剪枝、退休还是作为复制新分支的来源；全局上判断置信度加权后的集成答案是否已经足够集中，从而结束整个推理过程。该设定假设中间探测能够反映答案空间中的演化趋势，但不假设某一次探测必然可靠，也不要求所有分支在同一时刻到达控制点。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Self-Consistency**: 它通过采样多条完整推理轨迹并对最终答案投票来提高可靠性，是本文主要的问题基线；其固定预算和终止后聚合机制无法在生成期间处理分支效用与收敛速度的差异。
- **Parallel-Probe**: 它同样利用中间探测进行并行推理控制，但依赖同步探测和跨分支共识；ParaTempo改用分支局部、时间聚合的答案分布，使不同轨迹可以异步执行剪枝、退休和分叉。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

并行推理的准确性与鲁棒性来自同时探索多条解题轨迹，但推理成本会随分支数量和推理深度共同增长。固定预算方案对所有分支分配相同计算量，无法利用不同轨迹进展速度的差异，因此已经收敛的分支会生成冗余词元，长期不确定的分支也可能继续消耗计算；这同时增加总词元成本和由最慢分支决定的关键路径延迟。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于最终答案共识的自一致性与提前停止方法**：并行采样多条完整或接近完整的推理轨迹，统计最终答案的一致程度；当多数答案形成足够可靠的共识时停止继续采样。该类方法的判断依据较可靠，但通常需要先支付相当一部分生成成本。
- **基于生成中置信信号的在线控制方法**：这类方法在生成尚未结束时介入，包括用词元级模型置信度筛除低质量轨迹，或在若干中间位置探测当前暂定答案，以判断答案是否已经收敛。代表性思路包括 DeepConf、答案收敛方法及中间探测控制器。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 最终答案共识虽然通常较可靠，但信号出现较晚，只有在许多分支已经完成大量推理后才能触发控制，因此难以及时消除分支内部的冗余生成。
- 词元级置信度主要反映局部下一个词元的确定性，未必对应最终答案的演化；单次中间探测虽然更早，却容易受到暂时波动影响。二者都不足以稳定判断某条分支是否真正趋向一个主导答案，可能造成过早剪枝、误判收敛或继续浪费预算。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有方法缺少一种能够在生成过程中使用、面向单条分支、同时兼顾及时性与抗瞬时噪声的答案收敛信号；也缺少一个以该信号统一协调局部分支控制和全局终止、且不要求各轨迹同步推进的计算分配机制。

</div>
<div markdown="1"><span>核心问题</span>

能否通过聚合同一分支近期多个时刻的暂定答案概率分布，可靠地判断其答案空间是否正在稳定集中，并据此在无需额外训练和分支同步的条件下动态分配并行推理预算？

</div>
<div markdown="1"><span>作者直觉</span>

一次探测像一张容易受偶然波动影响的快照，而连续多次探测更像观察运动趋势：如果某条分支在近期反复把大部分概率放在同一个答案上，就有理由认为它正在稳定收敛；如果概率持续分散或主导答案频繁变化，则说明该分支仍不确定。利用这种时间上的一致性，系统可以更稳妥地回收已收敛或低价值分支的算力，并将预算转移到更有希望的探索方向。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ParaTempo把固定宽度的并行推理改写为在线资源分配：输入问题$x$后，模型$M$先采样$K$条独立推理分支，并按固定间隔暂停每条活跃分支，用其当前推理前缀查询中间答案分布。系统在长度为$W$的滑动窗口内汇总这些分布，再以聚合分布的负熵指数作为时间置信度$C_{i,t}$；该信号衡量第$i$条分支在一段时间内是否持续收敛到少数答案，而不是只看某一次探测是否自信。

控制器经过问题级预热校准后异步管理各分支：低置信度分支被剪枝并释放计算槽，连续多次保持高主答案概率的分支提前退役但保留投票证据，空出的槽可从高置信度分支复制当前前缀并以新随机种子继续探索。任意时刻，活跃与退役分支均以各自主答案的概率质量参与加权投票；当某个答案积累足够全局支持时提前停止，否则运行到没有活跃分支或预算耗尽。直观上，它像一个动态调度器：让已经想清楚的分支停止书写，让长期混乱的分支退出，并把资源转给已有希望但仍值得探索的思路。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 并行初始化与周期探测

独立采样$K$条推理轨迹$r_1,\ldots,r_K$；每生成固定数量的令牌，就用当前前缀$r_{i,t}$探测候选答案集合及其概率分布$p_{i,t}(v)$。各分支按自身进度接受探测，不要求处在相同推理深度。

<div class="method-step__io" markdown="1">

**输入**：问题$x$、推理模型$M$、并行分支数$K$以及每条分支的生成预算。<br>
**输出**：每条活跃分支在多个探测时刻得到的中间答案分布序列，以及持续更新的推理前缀。

</div>

**直观理解**：系统不是等所有答案写完后才判断，而是定期询问每条思路“目前最可能的答案是什么”。异步探测避免短分支等待长分支。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 时间聚合与收敛估计

在滑动窗口$4\mathcal{J}_{i,t}$内对同一答案桶的概率取平均，未在某次探测出现的候选答案按零概率处理，形成聚合分布$g_{i,t}$；随后计算时间置信度$C_{i,t}$、主答案$\hat{y}_{i,t}$及其概率质量$c_{i,t}$。

<div class="method-step__io" markdown="1">

**输入**：第$i$条分支最近至多$W$次探测得到的分布$p_{i,\tau}(v)$。<br>
**输出**：分支级控制状态量$C_{i,t}$、当前预测$\hat{y}_{i,t}$和投票权重$c_{i,t}$。

</div>

**直观理解**：一次探测可能因临时推理步骤而波动，因此系统观察近期一段轨迹是否持续偏向同一答案。答案越集中且越稳定，$C_{i,t}$越接近$1$。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 预热校准与异步分支控制

前$N_{\mathrm{warm}}$次探测只收集统计量，并由其分位数确定实例级剪枝阈值$\theta_{\mathrm{prune}}$；预热后，低于该阈值的分支被剪枝，连续$X$次满足$c_{i,\tau}\geq\theta_{\mathrm{retire}}$的分支退役。剪枝释放槽位时，从合格集合$\mathcal{D}_t$中选择时间置信度最高的供体，复制其前缀并用独立随机种子生成新分支；若没有合格供体，则槽位保持空闲。

<div class="method-step__io" markdown="1">

**输入**：预热阶段收集的时间置信度、当前分支的$C_{i,t}$与$c_{i,t}$、分支历史和可用计算槽。<br>
**输出**：被更新为活跃、退役、剪枝或分叉状态的分支集合，以及重新分配后的生成预算。

</div>

**直观理解**：阈值由当前问题自身的置信度分布校准，减少模型或题目变化造成的尺度失配。退役保留已经可靠的答案，剪枝清除低价值路线，分叉则从较有希望的中间思路另开一条随机续写路线。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 全局共识与最终聚合

对每个答案$a$累加所有支持该答案的分支权重$c_{i,t}$，得到置信度加权票数$V_t(a)$；若最高票数达到$\gamma_{\mathrm{ES}}|\mathcal{B}_t|$则提前终止，否则继续生成直至活跃分支耗尽或达到预算，最后返回加权票数最大的答案。

<div class="method-step__io" markdown="1">

**输入**：时刻$t$可投票的活跃和退役分支集合$\mathcal{B}_t$，以及各分支的$\hat{y}_{i,t}$与$c_{i,t}$。<br>
**输出**：最终预测$\hat{y}=\arg\max_a V_t(a)$及可能提前结束的推理过程。

</div>

**直观理解**：普通多数投票把每条轨迹视为同样可靠，ParaTempo则让答案更稳定、支持度更高的分支拥有更大权重。全局停止条件要求同一答案积累足够支持，从而约束局部分支提前退出带来的可靠性风险。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 受准确率约束的推理成本目标

$$
\min_{\pi}\;\mathcal{C}(\pi)\quad\text{s.t.}\quad\mathcal{A}(\pi)\geq\mathcal{A}(\pi_{\mathrm{fixed}})
$$

**符号说明**

- $\pi$：待选择的并行推理控制器，即决定各分支继续、退役、剪枝或获得额外计算的策略。
- $\pi_{\mathrm{fixed}}$：给所有并行分支分配相同固定生成预算的标准执行策略。
- $\mathcal{C}(\pi)$：控制器所产生的期望推理成本，可由令牌量、顺序关键路径或实际延迟等成本指标体现。
- $\mathcal{A}(\pi)$：控制器的期望答案准确率。
- $\mathcal{A}(\pi_{\mathrm{fixed}})$：固定预算并行执行所达到的期望准确率，作为可靠性下界。

<div class="equation-explanation" markdown="1">

**直观理解**：该约束优化明确了方法目标：尽可能减少推理成本，但不能以低于固定预算方案的预期准确率为代价。ParaTempo没有直接求解一个可微优化问题，而是以时间置信度驱动的启发式在线控制来逼近这一目标；因此实验必须同时检查准确率和多种成本，而不能只报告节省了多少令牌。<br>
**原文位置**：第2节 Problem Formulation，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 时间聚合与时间置信度

$$
g_{i,t}(v)=\frac{1}{|\mathcal{J}_{i,t}|}\sum_{\tau\in\mathcal{J}_{i,t}}p_{i,\tau}(v),\qquad C_{i,t}=\exp\big(-H(g_{i,t})\big)\in(0,1]
$$

**符号说明**

- $i$：并行推理分支的索引。
- $t$：当前探测时刻的索引。
- $v$：规范化后的候选答案桶。
- $p_{i,\tau}(v)$：第$i$条分支在探测时刻$\tau$对答案$v$给出的中间概率。
- $\mathcal{J}_{i,t}$：截至时刻$t$、长度最多为$W$的滑动探测窗口，即从$\max(1,t-W+1)$到$t$的探测时刻集合。
- $g_{i,t}(v)$：窗口内多个探测分布对答案$v$的平均概率；其支持集是窗口中出现过的答案桶并集。
- $H(g_{i,t})$：聚合答案分布$g_{i,t}$的香农熵，用于衡量概率质量分散程度。
- $C_{i,t}$：第$i$条分支在时刻$t$的时间置信度，范围为$(0,1]$。
- $W$：时间聚合所使用的滑动窗口大小。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分把最近多次探测平均起来，以压低某个中间推理步骤造成的偶然波动；第二部分把聚合分布的熵转换为易于比较的集中度。若近期概率几乎都落在同一答案上，熵接近零且$C_{i,t}$接近$1$；若多个答案持续竞争，熵增大而$C_{i,t}$下降。该量是剪枝和供体选择的主要信号，但退役与最终投票另外使用主答案概率$c_{i,t}$，避免把“整体分布集中”和“第一名得到多少支持”混为一谈。<br>
**原文位置**：第4.2节 Temporal Confidence，公式(8)与公式(9)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：ParaTempo是无需训练的测试时控制框架，不更新模型参数，也没有反向传播损失。公式(1)是系统层面的约束目标，表示在保持固定预算并行推理准确率的前提下压低推理成本；实际算法通过预热分位数校准、剪枝、退役、分叉和全局早停来在线近似实现，而不是通过训练直接优化$\mathcal{C}(\pi)$。这一区分很重要：所谓“置信度”来自基础模型在推理期间对中间答案的探测分布，并非另行训练的奖励模型或分类器。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 时间置信度估计器**

该模块先对最近$W$次中间答案分布做滑动平均，再计算$C_{i,t}=\exp(-H(g_{i,t}))$。由于$\exp(H(g_{i,t}))$可解释为聚合分布的困惑度，$C_{i,t}$相当于竞争答案有效数量的倒数；它反映整个答案空间的集中程度，而$c_{i,t}$只表示当前第一名答案的概率质量。

> 直观理解：仅看一次最高概率容易被暂时性的自信误导；观察一段时间内完整答案分布是否持续集中，能更稳健地判断一条推理路线是否正在收敛。

**2. 异步分支资源控制器**

控制器用实例级分位数阈值执行剪枝，用连续$X$次主答案概率约束执行退役，并从合格供体中按最高$C_{j,t}$执行分叉。分支独立改变状态，不设置跨分支的同步屏障；活跃与分叉分支继续消耗令牌，退役分支停止生成但保留证据，剪枝分支释放资源。

> 直观理解：不同思路达到答案所需的长度不同，统一等待会让已完成的路线浪费令牌，也让快速路线受最慢路线拖累。独立调度把计算投入仍有价值的轨迹，同时以退役投票避免丢失已得到的可靠结论。

**3. 置信度加权共识器**

模块把所有有效分支的主答案映射到规范化答案桶，并按$c_{i,t}$累加支持质量。它既用阈值$\gamma_{\mathrm{ES}}|\mathcal{B}_t|$判断是否已有充分共识，也在正常结束时以最大加权票数决定最终答案。

> 直观理解：分支级控制解决“计算给谁”，共识器解决“何时证据足够”和“最终相信谁”。保留退役分支并按支持强度投票，使节省计算不等于删除可靠证据。

**训练与推理**

训练阶段不存在，ParaTempo直接包裹已有长思维链推理模型。推理开始时，对同一问题$x$建立$K$条独立采样分支；每隔$\tau$个生成令牌探测一次中间答案分布，并保留至多$L$个候选答案。前$N_{\mathrm{warm}}$次探测期间不干预分支，只在满足窗口长度要求后收集$C_{i,t}$，再取预热集合$\mathcal{S}_{\mathrm{warm}}$的$1-q_{\mathrm{prune}}$分位数作为当前实例的$\theta_{\mathrm{prune}}$。

预热结束后，每条分支在自己的探测点独立决策。若已积累足够的分叉后历史且$C_{i,t}<\theta_{\mathrm{prune}}$，则剪枝；若最近$X$次探测的$c_{i,\tau}$均不低于$\theta_{\mathrm{retire}}$，则退役并冻结其$\hat{y}_{i,t}$与$c_{i,t}$用于投票；剪枝空出的槽从具有足够置信度和历史的供体集合中选择$C_{j,t}$最高者，复制其前缀并以新随机种子续写。每轮控制后汇总活跃和退役分支的加权票数；达到全局阈值便提前输出，否则直到预算耗尽或无活跃分支时输出票数最大的答案。

**复现信息**

为公平解释文中结果，所有方法均使用$K=16$条并行分支，单轨迹最大生成预算为$16{,}384$令牌，采用温度$0.6$、核采样$p=0.95$。ParaTempo每$\tau=500$个生成令牌探测一次，保留前$L=20$个答案候选；默认参数为$W=7$、$X=9$、$N_{\mathrm{warm}}=15$、$q_{\mathrm{prune}}=0.50$、$\theta_{\mathrm{retire}}=0.90$和$\gamma_{\mathrm{ES}}=0.50$。这些参数分别控制平滑时间范围、退役所需的连续稳定长度、实例阈值校准期、剪枝分位点、单分支退役强度和全局共识强度。

实验推理由$vLLM$在单张NVIDIA A100 80GB GPU上执行，并对四次独立运行取平均。单卡设置会直接影响并行调度和实际延迟，因此论文中的壁钟延迟不能脱离该硬件与服务框架直接外推；相比之下，总生成令牌和顺序生成令牌分别更接近总体计算量与关键路径长度。原文节选未明确说明中间答案探测所用提示模板、答案桶规范化规则、探测本身是否计入令牌或延迟、供体资格的具体阈值，以及并列投票的处理方式，严格复现时仍需核查技术补充材料。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 原文未明确报告数据集、数据规模、划分方式及其在实验中的作用。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**原文未明确报告**

实验章节节选未提供评价指标及其定义。 （原文未明确报告）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告任何基线方法，因此无法判断比较对象及其合理性。

**实验想回答的问题**

- 原文未提供第5章实验内容，无法据此确定实验试图回答的具体研究问题。
- 原文未提供实验设置、结果或分析，无法判断方法是否在效率、推理性能或并行化效果方面优于既有方法。

**实验实现**

所提供材料仅包含“5 Experiments”和“5.1 Experimental Setup”的章节标题，没有实验设置正文、数据集说明、基线配置、评价协议或实现细节。因此无法可靠重建评测流程。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces temporal-confidence-based parallelization to improve the efficiency of language-model reasoning.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`131d407020d7eddc6258e79959b4e04c8b638dd30b01bd8830dab3f39ad045a8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
