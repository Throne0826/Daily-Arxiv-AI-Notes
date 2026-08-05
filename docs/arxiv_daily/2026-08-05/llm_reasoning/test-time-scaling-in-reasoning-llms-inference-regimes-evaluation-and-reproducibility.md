---
title: "[论文解读] Test-Time Scaling in Reasoning LLMs: Inference Regimes, Evaluation, and Reproducibility"
description: "[arXiv 2608.04001][LLM Reasoning] 本文针对“测试时扩展”涵盖多种不可直接等同比较的推理算法这一问题，主张以完整推理系统为评估对象，并统一刻画其算法结构、计算成本、评估协议与可复现性要求。"
arxiv_id: "2608.04001"
announcement_date: "2026-08-05"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:38:20.815715+00:00"
source_sha256: "986809b60d6466d460358b3a6fb3ad8dbfe570d49d5fea83a99df282e8d27af6"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "LLM 其他"
  - "测试时扩展"
  - "推理型大语言模型"
  - "预算化推理"
  - "隐式前缀树"
  - "候选答案聚合"
  - "系统级评估"
  - "可复现性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.04001</p>

# Test-Time Scaling in Reasoning LLMs: Inference Regimes, Evaluation, and Reproducibility

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Mohsen Hariri, Weicong Chen, Nahal Shahini, Vikash Singh, Kai Ye, Amirhossein Samandar, Debargha Ganguly, Sreehari Sankar, Yanyan Zhang, Shouren Wang, Jerry Peng, Biyao Zhang, Michael Hinczewski, Vipin Chaudhary</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Case Western Reserve University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04001v1) · [PDF 下载](https://arxiv.org/pdf/2608.04001v1) · **关键词** 测试时扩展, 推理型大语言模型, 预算化推理, 隐式前缀树, 候选答案聚合, 系统级评估, 可复现性<br>
**项目页**: [https://mohsenhariri.github.io/scorio/tts](https://mohsenhariri.github.io/scorio/tts)

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

本文针对“测试时扩展”涵盖多种不可直接等同比较的推理算法这一问题，主张以完整推理系统为评估对象，并统一刻画其算法结构、计算成本、评估协议与可复现性要求。

**不用术语来说**：同一个语言模型在回答问题时，可以通过延长一次思考、生成多个完整答案后投票，或在尚未完成的解题步骤之间搜索来投入更多计算；但这些做法花费计算的方式、产生答案的分布以及容易出错的环节都不同。如果研究只报告一个笼统的“预算”和最终准确率，却不说明提示词、采样、搜索、验证器、停止规则等过程，就无法判断性能提升来自模型本身还是推理流程，也难以公平复现和比较结果。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将测试时扩展统一表述为自回归模型隐式前缀树上的预算约束推理，并区分单轨迹顺序扩展、叶节点级采样与终端归约、前缀级搜索三种结构，使不同算法可以按其实际决策过程而非笼统预算分类。
- 作者提出面向完整推理系统的评估与复现框架：区分共享候选库上的聚合器诊断和端到端系统性能，也区分事后选择与会改变生成成本的因果停止；同时要求联合报告效用、候选库质量、协议匹配的计算成本、不确定性及复现所需材料。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究推理型大语言模型的测试时扩展（test-time scaling）：在模型参数固定后，通过增加推理阶段的计算来提高复杂任务表现。相关算法主要分为三类：沿单条回答轨迹延长思考；生成多个完整候选答案后投票、重排或验证；在尚未完成的前缀状态上进行树式搜索。由于三类方法的候选分布、计算成本和失效方式不同，本文主张评估对象不能只是模型检查点，而应是由模型、提示模板、解码器、搜索控制器或归约器、验证器或裁判、预算及停止规则构成的完整推理系统。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自回归语言模型与隐式前缀树**

自回归模型依据已有文本逐个生成后续词元；每一种可能的后续词元都形成一个分支，所有可能生成序列可视为一棵无需显式构造的前缀树。完整回答对应叶节点，未完成的中间文本对应前缀节点。

</div>
<div class="concept-item" markdown="1">

**测试时扩展**

测试时扩展是在不继续训练模型的情况下，为单个问题投入更多推理计算，例如延长一条思维链、采样更多完整答案，或搜索更多中间状态。这里的“预算”不能只用一个含糊标量概括，还需说明计算被分配到何种推理结构和协议。

</div>
<div class="concept-item" markdown="1">

**终端归约与验证器**

终端归约是在得到一组完整候选后，通过多数投票、重排、最小贝叶斯风险解码或验证器选择最终答案。验证器是给候选答案打分或判断正确性的组件；其代理分数若不可靠，候选数量增大时可能被过度优化。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是待求解的推理问题、固定的模型检查点以及明确的推理协议与计算预算；系统在自回归模型的隐式前缀树上分配计算，并最终输出一个答案。具体过程可以是单轨迹顺序扩展、对多个叶节点候选执行终端归约，或在未完成前缀间进行搜索。基本假设是随机解码与实现细节会引入波动，而且提示、解码、控制、验证和停止规则都会影响结果，因此需要同时报告端到端效用、候选池质量、实际成本和不确定性，并区分完整系统评估与共享候选池上的归约器诊断。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$N$**

重复采样或 Best-of-N 中生成的完整候选答案数量。

</div>

</div>

**直接相关的工作**

- **Chain-of-Thought Prompting 与 Self-Consistency（Wei et al., 2022；Wang et al., 2022）**: 前者通过显式中间推理步骤提升求解能力，后者采样多条完整推理轨迹并聚合答案；它们分别构成单轨迹推理与叶级重复采样的重要背景。
- **Tree-of-Thoughts、RAP 与 value-guided decoding（Yao et al., 2023；Hao et al., 2023；Yu et al., 2024）**: 这些方法不等待完整答案生成后再选择，而是在未完成的前缀状态上搜索或使用价值信号引导解码，对应本文区分的前缀级扩展机制。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

推理模型的成绩越来越取决于测试阶段如何分配计算，而不只取决于模型权重。实际性能由检查点、提示模板、解码器、搜索控制器或归约器、验证器或裁判、预算和停止规则共同决定；在开放权重模型快速增加、训练机制与接口控制高度异质的情况下，若忽略这些组成部分，模型排名和效率结论会受到严重混杂，研究者也难以判断某种系统在真实部署成本下是否确实更好。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **单轨迹顺序扩展**：让模型沿同一条回答轨迹继续思考，例如强制生成更长的推理过程，或根据中间状态对当前回答进行干预。额外计算集中在一条逐步演化的解题路径上，不产生可供终端投票的大规模独立答案集合。
- **多候选归约与前缀搜索**：前者先采样多个完整答案，再通过多数投票、重排序、验证器选择或最小贝叶斯风险解码得到最终输出；后者在答案尚未完成时比较和扩展部分推理状态，如思维树、RAP及价值引导解码。两者分别在完整候选和未完成前缀层面分配计算。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有研究常把结构不同的推理程序压缩为单一“预算”变量，并只报告最终准确率。这会掩盖候选分布、计算口径和失败模式的差异，使跨论文性能与效率比较缺乏可解释的共同基础。
- 候选数量增加并不必然带来可靠提升：最佳候选选择或验证器重排序可能过度优化不完善的代理分数，语言模型裁判还可能受位置、冗长度及任务类型影响；再叠加随机解码和实现差异，若没有协议匹配的不确定性估计与复现控制，表面提升可能无法稳定重现。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前缺少一套同时覆盖算法结构、系统级评估、计算核算和复现条件的统一框架：它既要说明额外计算发生在单条轨迹、完整叶节点还是未完成前缀上，又要把候选库本身的质量与最终选择机制的效果分开，并明确事后分析与会改变实际生成成本的在线停止之间的区别。

</div>
<div markdown="1"><span>核心问题</span>

如何在一个统一但不抹平结构差异的形式体系中描述测试时扩展，并据此设计与真实推理协议一致的评估和复现规范，从而公平回答“哪个完整推理系统在给定计算条件下更有效、更稳定且可复现”？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把生成过程看成一棵由所有可能文本前缀组成的隐式树：不同测试时扩展方法，本质上是在预算限制下选择继续延长一条路径、比较若干完整叶节点，或搜索多个中间前缀。这样先按“计算在哪里发生、何时作出选择”拆开算法，再把模型、控制器、验证器和停止规则作为一个整体评测，就能避免用同一个预算数字混淆不同程序；共享同一候选库时可专门比较归约策略，而重新运行完整流程则衡量真正的端到端效用和成本。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是提出一个新的解题模型，而是建立一套统一分析“测试时扩展”（test-time scaling）的形式化框架。给定固定的自回归语言模型 $p_{\theta}(\cdot\mid x)$、输入提示 $x$ 和推理预算 $B$，系统在模型隐式生成的前缀树 $\mathcal{T}(x)$ 上执行带成本的操作，例如生成词元、扩展前缀、调用验证器或裁判、以及归约候选答案；最终输出完整生成 $\hat y_B(x)$ 或抽取答案 $\hat a_B(x)$。论文强调，被评价的对象应是整个推理系统，而不只是基础模型，因为解码策略、控制器、验证器、归约器和停止规则都会改变最终结果及实际成本。

框架依据额外计算发生的位置区分三种结构：单轨迹顺序扩展始终只维护一个未完成前缀；叶级扩展先独立生成多个完整候选，再进行投票、验证或重排序；前缀级扩展则在生成完成前维护候选前沿，并依据部分推理状态的评分决定扩展和剪枝。直观地说，三者分别对应“让同一个人继续思考或自我修改”“让多人分别答完再选答案”和“在解题过程中同时探索多条思路并尽早淘汰不佳分支”。实际系统可以混合这些结构，例如先做前缀搜索，再用叶级归约器从搜索所得答案库中选出最终答案。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造任务、生成树与成本预算

模型和解码策略在 $x$ 上诱导隐式前缀树 $\mathcal T(x)$ 以及完整叶节点的提议分布 $q_{\pi}(y\mid x)$；系统只允许执行累计成本不超过 $B$ 的生成、评分、验证、控制和归约操作。由于温度采样、核采样等策略会截断或重新归一化词元概率，$q_{\pi}$ 不必等于原始模型分布。

<div class="method-step__io" markdown="1">

**输入**：输入提示 $x\in\mathcal X$、固定自回归模型 $p_{\theta}$、局部解码策略 $\pi$、任务分布 $\mathcal P$ 与预算 $B$。<br>
**输出**：可供预算化推理算法 $\mathcal A_B$ 操作的前缀、终止叶节点集合 $\mathcal L(x)$、成本模型 $c(o_t)$ 与任务效用 $U_x(y)$。

</div>

**直观理解**：可以把语言模型的所有可能续写看成一棵极大的树，而预算决定系统最多能探索多少节点、生成多少答案以及调用多少次检查工具。这里的“更多计算”不能只用答案条数代替，因为生成、搜索和验证本身都可能具有不同成本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 选择推理结构并分配预算

若采用单轨迹顺序扩展，控制器从 $\pi_{\mathrm{seq}}(\cdot\mid x,z_t,b_t)$ 选择继续生成、抑制结束符、自我批评、调整解码参数或停止等元动作，并只更新唯一活动路径；若采用叶级扩展，则生成 $N$ 个完整候选；若采用前缀级扩展，则维护活动前沿 $\mathcal F_t$ 和完成候选库 $\mathcal Y_t$，循环执行选择、扩展、评分与剪枝。

<div class="method-step__io" markdown="1">

**输入**：当前前缀或候选集合、剩余预算，以及控制器、评分器和停止规则。<br>
**输出**：一个逐步修订的完整回答、一个完整候选库，或由搜索过程构造的候选库。

</div>

**直观理解**：这一阶段决定计算是集中押在一条思路上、平均分给多个独立答案，还是根据中间表现动态投向更有希望的分支。它也决定系统能否从早期错误中恢复：单轨迹只能沿原路径自我修正，而树搜索可以切换到尚未被剪掉的替代路径。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 获取候选级或前缀级评价信号

对完整候选，系统解析出推理轨迹 $r_i$ 和答案 $a_i$，再将可程序检查部分 $d_i$ 交给 $V_P$，并可由 $J_{\phi}$ 给出学习式分数 $j_i$；对未完成前缀，可使用生成似然、正确完成概率估计、过程奖励或多次蒙特卡洛续写所得的平均效用进行评分。只有满足“拒绝某前缀意味着其所有后继都不可能正确”的可靠部分检查，才支持无风险剪枝；学习式分数通常没有这一保证。

<div class="method-step__io" markdown="1">

**输入**：完整生成 $Y_i$ 或未完成前缀 $z$，以及任务专用验证器 $V_P$、学习式评价器 $J_{\phi}$ 或过程奖励模型 $R_{\phi}$。<br>
**输出**：候选元数据、程序验证结果、学习式候选分数，或供搜索控制器比较不同前缀的价值分数 $S(z)$。

</div>

**直观理解**：完整答案可以直接检查最终产物，但中间步骤通常只能由近似评分器判断“看起来是否有希望”。因此，前缀搜索可能节省大量计算，也可能因一次错误低分而永久删除真正能导向正确答案的分支。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 搜索控制或终端归约

前缀级系统可用束搜索保留评分最高的 $K$ 个状态、用最佳优先搜索反复扩展当前最高分前缀，或用 MCTS 在利用高价值动作与探索低访问动作之间权衡；叶级系统则使用验证器约束选择、自一致性投票、Best-of-$N$ 重排序或最小贝叶斯风险式经验期望效用选择。混合系统先通过搜索形成非独立同分布的叶节点库，再调用叶级归约器。

<div class="method-step__io" markdown="1">

**输入**：带分数的活动前沿，或包含 $N$ 个完整候选及其验证、评价和元数据的候选库。<br>
**输出**：被选中的完整生成 $\hat y_B(x)$ 或答案 $\hat a_B(x)$。

</div>

**直观理解**：搜索控制回答“下一份计算花在哪里”，终端归约回答“已经得到的答案中选哪一个”。二者不能混为一谈：前者会改变哪些答案有机会被生成，后者只在已经完成的候选之间做决定。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 预算化推理约束与测试时扩展曲线

$$
\sum_t c(o_t)\leq B,\qquad G(B)=\mathbb{E}_{x\sim\mathcal{P},\,\xi}\left[U_x\!\left(\hat{y}_B(x;\xi)\right)\right]
$$

**符号说明**

- $o_t$：推理算法在第 t 步执行的原子操作，例如生成词元、扩展前缀、调用验证器或归约候选
- $c(o_t)$：原子操作 $o_t$ 的成本
- $B$：允许使用的累计测试时计算预算
- $\mathcal{P}$：评测输入 x 的任务分布
- $\xi$：采样、搜索和控制过程中的内部随机性
- $\hat{y}_B(x;\xi)$：预算 B 下推理系统针对输入 x 返回的完整生成
- $U_x(y)$：完整生成 y 在输入 x 上的任务效用，可为精确正确性、执行分数或偏好奖励
- $G(B)$：预算 B 下整个推理系统的期望任务效用

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分规定任何推理协议都必须在同一成本边界内运行，第二部分把不同题目和随机运行的最终效用取平均。它将“测试时扩展”定义为整套系统的性能如何随预算变化，而不是简单考察生成长度或候选数；由于评分器过度优化、错误剪枝和额外控制开销，$G(B)$ 并不必然单调上升。<br>
**原文位置**：第 2.1 节 Problem setup and three-regime taxonomy

</div>

</div>

<div class="equation-block" markdown="1">

#### 前缀的理想续写价值

$$
Q^{\star}_{\rho}(z)=\mathbb{E}_{Y\sim q_{\rho}(\cdot\mid x,z)}\left[U_x(Y)\right]
$$

**符号说明**

- $z$：尚未完成的词元前缀或由多个推理步骤组成的宏观前缀
- $\rho$：从当前前缀继续生成时采用的 rollout 策略
- $q_{\rho}(\cdot\mid x,z)$：给定输入 x 和前缀 z，按策略 ρ 继续生成所得完整叶节点的分布
- $Y$：从前缀 z 继续得到的随机完整生成
- $U_x(Y)$：完整生成 Y 对当前任务输入 x 的效用
- $Q^{\star}_{\rho}(z)$：若从前缀 z 继续并最终返回一个完成结果，该前缀的理想期望价值

<div class="equation-explanation" markdown="1">

**直观理解**：该式把一个未完成思路的价值定义为“沿它继续做完后，最终答案平均有多好”。真实期望通常无法直接计算，所以系统才需要价值模型、过程奖励或多次续写来近似；若搜索最后还要把多个叶节点交给归约器，某个前缀的真实边际价值还会依赖已经收集的其他候选，因此这个单叶价值只是常用近似。<br>
**原文位置**：第 2.4.2 节 Prefix evaluation as continuation-value estimation

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：该章提出的是针对固定自回归模型的推理与评价框架，没有给出新的基础模型训练损失，也不要求联合训练生成模型、验证器或搜索控制器。文中出现的学习式评价器 $J_{\phi}$、结果监督价值模型和过程奖励模型 $R_{\phi}$ 均被视为可插入的代理模块；作者只说明它们可能分别由结果级或步骤级监督学习，未在所给章节中规定统一训练目标、数据构造或优化算法。因此不能把理想续写价值 $Q^{\star}_{\rho}(z)$ 或系统性能曲线 $G(B)$ 误写为本文实际执行的训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 三类预算化推理控制器**

单轨迹控制器维护唯一活动状态 $z_t$ 和剩余预算 $b_t$，不能形成竞争前沿；叶级控制器从共同提议分布生成完整叶节点，跨候选交互只发生在终端归约阶段；前缀级控制器维护 $\mathcal F_t$、$\mathcal Y_t$ 和 $b_t$，并根据未完成状态的评价结果重新分配后续计算。分类标准是候选之间何时发生交互，而不是算法名称，因此自适应停止并不必然构成前缀搜索，实际方法也可能是混合系统。

> 直观理解：该模块提供论文最关键的判别规则：只改一条回答属于单轨迹；等所有回答完成后再比较属于叶级；在回答尚未完成时就依据相互比较决定保留哪条思路，才属于前缀级。这样可以避免把统计结构、成本和失败方式明显不同的方法都笼统称为“增加测试计算”。

**2. 候选评价与终端归约器**

程序验证器 $V_P(x,d)$ 检查可确定验证的产物，学习式评价器 $J_{\phi}(x,\omega)$ 则对完整叶或部分状态给出代理分数。叶级归约器 $\mathcal R_N$ 可筛选通过验证的候选、按规范化答案频率做自一致性、按 $j_i$ 做 Best-of-$N$，或根据候选间效用执行经验最小贝叶斯风险选择；其中两两效用计算可能需要 $O(N^2)$ 次评价调用。

> 直观理解：生成更多答案只提高“正确答案被覆盖”的机会，最终是否交出正确答案还取决于选择器。硬取最高代理分数尤其可能放大奖励模型的偏差；候选越多，系统越可能找到能骗过不完整验证器或学习式裁判的异常答案。

**3. 前缀价值估计与搜索过程**

理想前缀分数是从 $z$ 出发按续写策略 $\rho$ 完成后所得效用的期望，但实践中通常使用累积对数似然、结果监督价值模型、过程奖励模型或蒙特卡洛续写估计。束搜索、最佳优先搜索和 MCTS 将这些分数转化为扩展与剪枝决策；由此产生的有效输出分布 $q_{\mathrm{search},B}(y\mid x)$ 联合依赖评分器、控制器、停止规则和预算，不能视为来自 $q_{\pi}$ 的独立同分布样本。

> 直观理解：搜索能把计算集中到有希望的思路上，但效果取决于中途打分能否正确排列同一道题的竞争分支。即使评分器整体上看似校准良好，只要它在关键节点把正确分支排在错误分支之后并将其剪掉，后续增加预算也无法找回该答案。

**训练与推理**

本文流程属于测试时推理。单轨迹模式从初始前缀开始，控制器依据 $x$、当前状态 $z_t$ 和剩余预算 $b_t$ 选择元动作，只延伸或修订同一条路径，直至停止或耗尽预算。叶级模式按 $q_{\pi}(\cdot\mid x)$ 生成完整候选库 $\mathcal Y_N(x)$，解析每个候选的答案和可验证部分，记录程序验证结果与学习式分数，最后由 $\mathcal R_N$ 输出单个生成或答案；若自适应决定是否再启动一次独立 rollout，但不在多个未完成前缀之间重新分配计算，它仍属于叶级结构而非前缀搜索。

前缀级模式从根状态建立活动前沿，反复选取前缀 $z_t$、构造其后继集合、为后继评分，并更新前沿、完成候选库和剩余预算。评分可以基于似然、预测正确率、过程奖励或 rollout 回报，控制策略可以是束搜索、最佳优先或 MCTS；预算耗尽或满足停止规则后，系统直接返回一个叶节点，或把搜索得到的候选库交给叶级归约器。整个过程中基础模型参数 $\theta$ 保持固定，变化的是推理时的计算分配、候选分布和选择协议。

**复现信息**

公平实现和复现至少要明确：基础模型及其版本、提示模板、答案解析和规范化规则、解码策略 $\pi$ 及温度或核采样设置、预算 $B$ 的计量单位、停止规则、验证器与学习式裁判的版本和提示、搜索评分函数、前沿大小或候选数，以及平票与无候选通过时的回退规则。尤其不能只报告 $N$：叶级 MBR 可能产生 $O(N^2)$ 的评价成本，而前缀搜索还包含节点扩展、rollout 和裁判调用；比较 Best-of-$N$ 与搜索方法时，应同时对齐生成成本和评价成本。

还需记录随机种子或完整候选与信号，以区分精确重放和仅复现结果分布。前缀搜索所得叶节点共享历史并受剪枝控制，其候选库不是从 $q_{\pi}(\cdot\mid x)$ 独立同分布抽取，不能直接套用固定样本库的统计解释；若实现利用共享前缀的键值缓存复用，也应报告，因为这会显著改变墙钟时间和实际计算前沿。所给章节未明确报告统一硬件配置、具体推理框架或所有模块的超参数，相关内容应标记为“原文未明确报告”，而不应自行补全。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 广泛知识基准：用于考察推理协议在知识覆盖较广、答案可能较开放的任务中的表现。所给原文未列出具体数据集名称、规模、划分或样本数量，因此无法判断是否采用固定测试集、时间切分或污染控制。
- 符号推理基准：用于检验模型能否通过多步操作得到可核验答案，并观察额外推理预算是否提高正确候选的发现概率。具体数据集、规模与划分原文未明确报告。
- 竞赛数学基准：用于测试高难度、通常具有明确正确答案的推理任务，适合比较重复采样、验证器选择及预算扩展。具体竞赛、题目数量、难度分层和测试划分原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**预算约束下的端到端系统性能**

在任务分布和算法随机性上，完整推理协议最终输出的期望任务效用；经验估计是在评测集上对每个最终输出效用取平均。该指标评估的是检查点、提示、解码器、控制器或归约器、验证器、停止规则与预算共同组成的系统，而非基础模型本身。 （越高越好，因为它直接表示给定预算下部署系统最终答案的平均效用；但只有在任务效用定义、总成本和协议均匹配时才能公平比较。）

</div>
<div class="metric-item" markdown="1">

**发现—稳定性剖面**

基于每道题单次尝试成功概率及重复采样中的正确候选数量，描述候选库是否容易发现至少一个正确答案，以及正确答案是否稳定到足以支持阈值聚合。它是候选分布诊断，不等同于某个聚合器的实际成功率。 （取决于具体坐标或函数：正确候选发现概率与达到聚合阈值的概率通常越高越好；必须同时报告采样次数和阈值，不能将不同预算下的数值直接混用。）

</div>
<div class="metric-item" markdown="1">

**总推理成本**

由生成成本与评估成本构成；评估成本进一步包括信号获取、控制器运行和最终决策。该口径还应计入预热或丢弃的词元、验证器或裁判调用、重复控制评估和聚合操作。 （在效用相同的条件下越低越好；论文主张绘制效用—总成本曲线，而不是把相同样本数或相同生成词元数误认为相同计算预算。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨广泛知识、符号推理和竞赛数学任务应用统一评估原则

<div class="result-value" markdown="1">

作者称其将所提出的测试时扩展分类、系统级评估原则与复现要求应用于三类基准；但所给原文没有提供各数据集、模型或推理协议的分项得分，因此不能量化哪一种扩展机制表现最好。

</div>

该结果表明论文试图验证框架是否能覆盖不同评价结构，而不是只适用于数学题。它不证明某个具体模型或搜索算法在三类任务上取得了统计显著的性能提升，也不能据此建立模型排名。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We also organize the open-weight reasoning ecosystem by model-side and interface mechanisms, apply these principles to broad-knowledge, symbolic-reasoning, and competition-mathematics benchmarks, and assemble over 2 billion full reasoning traces for release with progressively richer verifier and token-level signals.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 大规模完整推理轨迹资源构建

<div class="result-value" markdown="1">

作者报告整理了超过 20 亿条完整推理轨迹，并计划附带逐步增强的验证器信号和词元级信号。

</div>

这一规模说明论文的重要实证产物是候选轨迹库，可用于分析正确答案发现、候选稳定性以及验证器行为。它本身不等于 20 亿道独立题目，也不证明轨迹质量、任务覆盖或验证器标注均匀可靠；这些判断需要数据构成和质量审计。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We also organize the open-weight reasoning ecosystem by model-side and interface mechanisms, apply these principles to broad-knowledge, symbolic-reasoning, and competition-mathematics benchmarks, and assemble over 2 billion full reasoning traces for release with progressively richer verifier and token-level signals.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 匹配预算下的端到端协议比较与共享候选库诊断

<div class="result-value" markdown="1">

论文的核心评估结论是：端到端性能应相对于总成本报告；共享候选库只能识别生成后聚合阶段的差异，而发现—稳定性剖面描述的是提议分布中候选的可获得性，并非特定聚合协议的成功概率。

</div>

通俗地说，同一批答案上更会挑选的验证器，不一定在真实运行时仍是更强系统，因为生成候选和调用验证器也消耗预算。该结论属于评估方法论与分析性判断；所给文本没有给出对应分数表或显著性检验，因而不是一个带数值优势的实验结论。

<div class="result-source" markdown="1">

来源：Section 3.3，预算匹配与共享候选库比较段落

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

End-to-end utility should be plotted against total cost.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给章节没有包含完整实验表、图中数值、具体模型清单、数据集规模与划分、预算档位、随机种子或置信区间，因此无法验证任何准确率提升、模型排序、统计显著性或成本—性能前沿；相关内容均应回到论文完整实验章节和发布工件核对。
- 发现—稳定性诊断采用条件独立的重复尝试抽象，但真实候选可能因共享提示、搜索控制、缓存状态或自适应证据而相关；若直接套用二项分布解释前缀搜索或自适应采样，可能低估不确定性并误判有效样本量。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 单轨迹顺序扩展：在一条持续演化的回答轨迹上增加思考长度或进行自适应干预。它是有意义的比较对象，因为其额外计算集中在单个解答，而不是通过多个独立候选提高覆盖率。
- 叶节点级重复采样与终端归约：生成多个完整候选，再通过多数投票、自洽性、重排序或验证器选择最终答案。它用于检验性能提升究竟来自发现更多候选，还是来自终端聚合规则。
- 前缀级搜索：在未完成的推理状态上展开、评分和剪枝，如树搜索或价值引导解码。它与完整候选采样的关键区别是计算会改变后续候选的提议分布，因此不能仅按样本数直接比较。
- 共享候选库上的聚合器比较：不同决策规则使用同一批候选及相同证据。该对照可隔离投票、验证器或其他归约规则的影响，但不能代表各协议独立运行时的端到端能力。

**实验想回答的问题**

- 在推理型大语言模型的测试时扩展中，单轨迹延长、完成候选采样后聚合以及未完成前缀搜索能否在统一但不混淆其统计结构的框架下进行评估？
- 如何区分完整推理系统的端到端性能与候选库本身的“发现—稳定性”，并在匹配总计算成本、随机性和推理协议的条件下进行可复现比较？

**实验实现**

论文要求把完整推理协议作为评测对象，并明确报告提示模板、解码或搜索方式、预算分配、候选提议分布、控制器或归约器、验证器或裁判、停止规则、数值设置以及不确定性估计。端到端比较时，每个协议应生成自己的候选流、取得自己的推理时证据并执行自己的停止规则；共享候选库比较则只能归因于生成后的聚合阶段。成本应分解为生成、信号、控制和决策部分，不可仅以候选数作为统一预算。对于随机解码，结果还应同时反映评测题目抽样和候选生成随机性。所给章节未明确报告模型检查点、温度、最大词元数、随机种子、硬件、每题采样次数及置信区间构造方式，因此无法复现实验数值。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 共享候选库与端到端比较构成一个归因案例：若固定候选和证据，只更换最终决策规则，性能差异可归因于归约器；若允许每个协议自行采样、评分和停止，则评估的是完整系统。前者适合诊断“谁更会从同一批答案中挑选”，后者才回答“相同总预算下谁实际更强”。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper formalizes reasoning-time scaling regimes while centrally developing evaluation and reproducibility protocols for those inference systems.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`986809b60d6466d460358b3a6fb3ad8dbfe570d49d5fea83a99df282e8d27af6`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
