---
title: "[论文解读] When Does the Best Sampling Temperature Rise with the Budget? Sufficient Conditions for Pass@k"
description: "[arXiv 2608.14665][LLM Reasoning] 本文解释了为何在任务难度和温度响应存在异质性时，基准整体的最优采样温度可能随 pass@$k$ 的采样预算增加而上升，并给出保证这一趋势成立的可检验充分条件。"
arxiv_id: "2608.14665"
announcement_date: "2026-08-18"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:23:16.375826+00:00"
source_sha256: "98bd9bf54a6f1a25609c3b927a968851f672587eb369af7e92a0d6c478d9116a"
tags:
  - "LLM Reasoning"
  - "pass@k"
  - "采样温度"
  - "多样本推理"
  - "任务异质性"
  - "条件对数成功率响应"
  - "单调似然比排序"
  - "比较静态"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.14665</p>

# When Does the Best Sampling Temperature Rise with the Budget? Sufficient Conditions for Pass@k

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Changsu Jeong</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.14665) · [PDF 下载](https://arxiv.org/pdf/2608.14665) · **关键词** pass@k, 采样温度, 多样本推理, 任务异质性, 条件对数成功率响应, 单调似然比排序, 比较静态<br>


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

本文解释了为何在任务难度和温度响应存在异质性时，基准整体的最优采样温度可能随 pass@$k$ 的采样预算增加而上升，并给出保证这一趋势成立的可检验充分条件。

**不用术语来说**：生成模型通常可以针对同一道题采样多次，只要其中一次正确就算成功。经验上，只有少量尝试时较低温度往往更好，而允许大量尝试时较高温度可能更好；但这不能仅用“高温增加多样性”严格推出，因为对任何一道固定题目，增加尝试次数都不会改变使其单次成功率最高的温度。真正需要解释的是：许多难易不同、对温度反应不同的题目汇总成一个基准后，什么条件会让整体最优温度随预算上升。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出基于条件对数成功响应的充分条件：在当前温度下，若单次成功率较低的任务从升温中获得的相对收益不小于成功率较高的任务，则聚合 pass@$k$ 的归一化温度导数随预算呈单调变化；进一步假设各预算下的温度—性能曲线严格单峰时，唯一最优温度关于 $k$ 非递减。
- 作者用可解析的双层任务模型展示最优温度既可能上升也可能下降，并给出相变边界；同时以 $\mathrm{Beta}(2,k)$ 核和单调似然比倾斜刻画预算增大时评价权重如何转向仍然较难成功的任务，使经验性的“困难任务重加权”解释成为可检验的条件命题。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究语言模型推理阶段的多次采样：给定同一任务，模型以温度 $t$ 独立生成 $k$ 个候选，只要至少一个候选通过验证便算成功。温度控制输出分布的集中程度与探索程度，而 pass@$k$ 衡量 $k$ 次尝试内至少成功一次的概率。已有代码生成与多样本推理研究观察到，基准测试上的最佳温度常随预算 $k$ 增大而升高；但这并非 pass@$k$ 公式本身必然产生的性质，因为对任一固定任务，pass@$k$ 只是单次成功率 $p_t(X)$ 的严格递增变换，其最优温度不会因 $k$ 改变。因此，基准总体上的最优温度移动必须来自任务间异质性，即不同难度任务对升温具有不同方向或幅度的响应；或者来自条件独立同分布采样、固定温度解码及完美验证等建模假设被破坏。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**采样温度**

温度是调整模型输出概率分布的解码参数：低温通常使概率集中于少数高概率候选，高温则增加输出多样性。本文把温度 $t$ 视为一个可连续调节的推理控制量，并研究性能关于 $t$ 的变化。

</div>
<div class="concept-item" markdown="1">

**pass@k**

pass@$k$ 表示对同一任务采样 $k$ 次时至少有一个候选被接受的概率；若每次采样条件独立且单次成功率为 $p$，则该概率为 $1-(1-p)^k$。它强调多次尝试后的覆盖能力，而不只评价一次生成。

</div>
<div class="concept-item" markdown="1">

**单调似然比排序**

单调似然比排序用于比较两个加权分布是否系统性地把更多权重移向变量的一端。本文中，随着预算 $k$ 增大，相关权重向单次成功率较低的任务倾斜，从而可与任务的温度响应顺序结合，判断总体温度导数的符号如何变化。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

从任务总体中抽取随机任务 $X$，在温度 $t$ 下对每个任务进行 $k$ 次条件独立同分布采样，并假定每次生成使用同一固定温度且验证结果可靠。输入是任务分布、预算 $k$ 以及各任务随温度变化的单次成功率函数 $p_t(X)$；总体目标是选择使总体 pass@$k$ 最大的温度。论文关注的核心问题不是计算某个模型的经验最优温度，而是寻找一个任务级充分条件，使总体性能对温度的导数符号在不同预算间具有嵌套关系，并在各预算的温度—性能曲线严格单峰时推出唯一最优温度随 $k$ 弱单调上升。该条件通过条件对数成功率响应 $m_t(u)$ 表述：在当前成功率为 $u$ 的任务中，若升温带来的平均相对成功率变化随 $u$ 增大而不增加，即较难任务获得弱更大的比例收益，则更大的采样预算会在规范化边际量中更偏重这些低成功率任务。该结论是总体层面的条件性理论，并非“更大预算必然需要更高温度”的普遍定律；原文还明确说明没有训练语言模型，也没有以模型查询进行实验测量。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$X$**

从研究总体中抽取的随机任务。

</div>
<div class="notation-item" markdown="1">

**$t$**

语言模型推理时采用的采样温度。

</div>
<div class="notation-item" markdown="1">

**$p_t(X)$**

任务 $X$ 在温度 $t$ 下单次采样成功并通过验证的概率。

</div>
<div class="notation-item" markdown="1">

**$m_t(u)=\mathbb{E}[\dot p_t(X)\mid p_t(X)=u]/u$**

当前单次成功率为 $u$ 的任务，其温度导数 $\dot p_t(X)$ 的条件均值除以 $u$；它表示升温对该类任务单次成功率造成的平均相对变化。

</div>

</div>

**直接相关的工作**

- **Slocum et al. [12]**: 该工作已明确指出固定任务的最优温度不随预算 $k$ 改变，并定性解释高预算下低成功率任务会获得更大边际权重。本文不主张这些观察的优先权，而是在此基础上引入随当前成功率递减的条件对数成功率响应，给出温度导数符号嵌套及最优温度有序化的严格充分条件。
- **Chen et al. [2]（Codex）**: 该研究提供本文试图解释的代表性经验现象：某一模型的 pass@1 最优温度约为 $0.2$，而 pass@100 最优温度约为 $0.8$，并展示最佳温度随预算上升的上包络。本文将这种基准总体模式作为理论解释目标，而不重新进行模型实验或声称首次发现该现象。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

推理阶段必须根据采样预算选择温度。已有语言模型研究观察到，小预算常偏好低温，而大预算可能偏好高温，例如引言转述 Codex 的一个模型中 pass@1 的最优温度约为 $0.2$、pass@100 约为 $0.8$。如果缺少理论判据，实践者只能针对每个预算反复搜索温度，也无法判断观察到的上升趋势是稳定的总体规律，还是由有限基准、估计噪声或特定任务构成造成的现象。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **质量—探索或多样性解释**：该解释认为低温集中概率质量，适合在尝试次数少时争取高质量答案；高温扩大候选答案的多样性，因此在尝试次数多、只需一次成功的 pass@$k$ 指标下更有价值。相关实证工作还发现，不同温度会解决不同题目，温度组合可能优于单一温度。
- **固定任务分析与困难任务重加权解释**：在给定任务且各次采样条件独立同分布时，若温度 $t$ 下的单次成功率为 $p_t$，则 pass@$k$ 为 $1-(1-p_t)^k$，它对 $p_t$ 严格递增。因此，固定任务上使 $p_t$ 最大的温度不会因 $k$ 改变。既有工作据此指出，基准最优温度的移动必须来自任务间异质性，并定性说明大预算会让低成功率任务对边际变化更重要。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- “预算越大越需要多样性”只是直觉，不能推出聚合最优温度必然上升。对单个固定任务，pass@$k$ 只是单次成功率的单调变换；若不刻画不同任务对温度的响应方向和幅度，该直觉也无法排除最优温度不变甚至下降的情形。
- 既有困难任务重加权观察指出了权重因子及大致机制，却没有给出一个任务层面、可由数据检验的响应排序条件，从而保证不同预算之间的温度导数符号具有嵌套关系。尤其不能把该机制误述为原始导数 $\partial_t\operatorname{pass}@k$ 必然随 $k$ 增大；论文强调真正单调的是经过归一化后的导数。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前尚缺少连接“任务当前有多难”与“该任务从升温中获得多少相对收益”的严格条件，也缺少从这一条件推导基准总体比较静态的结果。需要明确何种任务响应结构足以保证更大预算不会把最优温度推低，同时说明该结论在哪些响应结构下会反转，以及它依赖哪些建模边界。

</div>
<div markdown="1"><span>核心问题</span>

在条件独立同分布采样、同一计划内温度固定、验证器能够准确识别成功且评价对象为任务总体的设定下，什么任务层面的温度响应条件，能够保证聚合 pass@$k$ 的最优温度随采样预算 $k$ 增大而弱单调上升？

</div>
<div markdown="1"><span>作者直觉</span>

预算增加后，已经较容易的任务很快达到“至少成功一次”，继续改善它们对 pass@$k$ 的边际价值会下降；评价权重因而逐渐偏向仍经常失败的任务。若这些低成功率任务恰好能从升温中获得更大的比例性改善，即其条件对数成功响应随当前成功率下降而不减，那么这种权重转移就会让升温在大预算下相对更有利。反之，若容易任务更受益于升温，或困难任务因升温受损更大，最优温度上升便没有保证，甚至可能向下移动。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是训练新模型或提出新的采样算法，而是建立一个关于 pass@$k$ 最优温度如何随推理预算变化的理论分析框架。输入是任务总体分布 $X\sim\mu$、温度区间 $I=[\underline{t},\overline{t}]$，以及每个任务在温度 $t$ 下单次生成被接受的概率 $p_t(X)$；在给定任务与温度后，假设 $k$ 次生成独立同分布，验证器能够无误判断二元成功事件。作者先把总体 pass@$k$ 写成任务级成功概率的期望，再对温度求导，确定哪些任务在边际上推动温度升高或降低。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立总体 pass@$k$ 目标

令失败概率为 $q_t(X)=1-p_t(X)$，利用条件独立性把任务 $X$ 上至少一次成功的概率写为 $1-q_t(X)^k$，再对任务分布取期望得到 $A_k(t)$。固定任务上该表达式严格随 $p_t(x)$ 增大，因此单个任务的最优温度不依赖 $k$；总体最优温度发生变化必须来自不同任务之间的温度排序交叉。

<div class="method-step__io" markdown="1">

**输入**：任务总体 $X\sim\mu$、候选温度 $t\in I$、任务级单次成功概率 $p_t(X)$ 和采样预算 $k$。<br>
**输出**：待最大化的总体性能曲线 $t\mapsto A_k(t)$，以及“预算依赖来自任务异质性”的问题分解。

</div>

**直观理解**：重复采样只会把同一任务的单次成功率通过一个递增函数放大，不会改变该任务偏好的温度。预算改变总体最优温度，是因为大预算重新分配了不同难度任务对总体决策的影响。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 把温度边际效应改写为任务加权平均

对 $A_k(t)$ 求导，并定义条件对数成功响应 $m_t(u)=\mathbb{E}[\dot p_t(X)\mid P=u]/u$。随后构造重加权任务分布 $\nu_{k,t}$，其权重与 $p_t(X)q_t(X)^{k-1}$ 成正比，使导数符号由 $\mathbb{E}_{\nu_{k,t}}[m_t(P)]$ 决定。

<div class="method-step__io" markdown="1">

**输入**：当前内部温度 $t$、任务级成功率 $P=p_t(X)$、温度导数 $\dot p_t(X)=\partial_t p_t(X)$。<br>
**输出**：一个将“预算造成的任务权重变化”与“任务对升温的响应”分离的导数表示。

</div>

**直观理解**：作者把每个任务看成对升温投赞成票或反对票，$m_t(P)$ 是票的方向和相对强度，$\nu_{k,t}$ 是预算为不同任务分配的票重。这样可以直接判断增加预算后，升温是否更有利。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 证明预算增大导致导数符号嵌套

作者证明从预算 $k$ 增至 $\ell$ 时，任务权重额外乘以 $(1-P)^{\ell-k}$，因此按单调似然比次序向较低 $P$ 的任务移动。若 $m_t(u)$ 随 $u$ 非增，即低成功率任务从升温中获得更大的比例收益或更小的比例损失，则归一化导数随预算非减，进而有 $A_k'(t)\geq0\Rightarrow A_\ell'(t)\geq0$。

<div class="method-step__io" markdown="1">

**输入**：两个预算 $\ell>k$、重加权分布 $\nu_{k,t}$ 与条件响应函数 $m_t(u)$。<br>
**输出**：定理 3.3 的导数符号嵌套结论；若每条 $A_k(t)$ 还严格单峰，则得到最优温度 $t_\ell\geq t_k$。

</div>

**直观理解**：预算越大，已经容易成功的任务越快“退出边际决策”，尚未成功的困难任务更重要。如果困难任务相对更喜欢高温，那么低预算下值得升温的位置，在高预算下仍然值得升温；单峰性再把这个局部方向结论转化为最优点的排序。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 用解析模型、核表示与诊断条件检验边界

在连续情形中，作者用 $\mathrm{Beta}(2,k)$ 核说明导数主要如何加权不同单次成功率区域；在两层仿射模型中解析求出 $t_k$，展示最优温度既可上升也可下降。实际检验时应分别估计 $m_t(u)$ 的单调性和 $A_k(t)$ 的严格单峰性，只有两者均获支持时才预测 $t_k$ 随预算非减。

<div class="method-step__io" markdown="1">

**输入**：连续成功率分布或有限任务分层、不同温度附近估计的任务级 $p_t$ 与 $\dot p_t$。<br>
**输出**：可证伪的充分条件、反例构造和面向后续实证研究的检验流程，而不是无条件的温度调节规则。

</div>

**直观理解**：核表示回答“哪些难度附近的任务正在决定是否升温”，两层模型则像最小化示例，明确展示缺少条件时结论会反向。诊断流程要求先检查论文假设，再使用其预测。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 总体 pass@k 目标

$$
A_k(t)=\mathbb{E}_{X\sim\mu}\!\left[1-q_t(X)^k\right]=\mathbb{E}_{X\sim\mu}\!\left[1-\left(1-p_t(X)\right)^k\right]
$$

**符号说明**

- $X\sim\mu$：从基准任务总体分布 $\mu$ 中抽取的随机任务。
- $t\in I$：采样温度，取值于紧区间 $I=[\underline{t},\overline{t}]$。
- $p_t(X)$：给定任务 $X$ 和温度 $t$ 时，一次生成被接受的条件概率。
- $q_t(X)=1-p_t(X)$：相应的一次生成失败概率。
- $k$：对同一任务进行的条件独立同分布生成次数，即推理预算。
- $A_k(t)$：在任务总体上平均的至少一次成功概率，即 population pass@$k$。

<div class="equation-explanation" markdown="1">

**直观理解**：对一个任务而言，$q_t(X)^k$ 是连续 $k$ 次全部失败的概率，用 $1$ 减去它便得到至少成功一次的概率；再跨任务平均就是优化目标。由于 $1-(1-u)^k$ 对 $u$ 严格递增，固定任务的最优温度等同于最大化其 $p_t(x)$，所以总体最优点的预算变化不能仅用“更多样本带来更多多样性”解释。<br>
**原文位置**：第 2 节，公式 (1)；固定任务解释见命题 2.1

</div>

</div>

<div class="equation-block" markdown="1">

#### 预算重加权下的温度导数分解

$$
\begin{aligned} P&=p_t(X),\qquad Z_{k,t}=\mathbb{E}\!\left[P(1-P)^{k-1}\right],\\ m_t(u)&=\frac{\mathbb{E}[\dot p_t(X)\mid P=u]}{u},\\ \frac{\mathrm{d}\nu_{k,t}}{\mathrm{d}\mu}(X)&=\frac{p_t(X)q_t(X)^{k-1}}{Z_{k,t}},\\ A_k'(t)&=kZ_{k,t}\,\mathbb{E}_{\nu_{k,t}}[m_t(P)]. \end{aligned}
$$

**符号说明**

- $P=p_t(X)$：随机任务在当前温度 $t$ 下的单次成功率。
- $\dot p_t(X)=\partial_t p_t(X)$：任务级单次成功率关于温度的局部变化率。
- $m_t(u)$：在当前成功率为 $u$ 的任务中，成功率对温度的平均比例响应。
- $Z_{k,t}$：使任务权重归一化的正常数；在论文设定的内部点上为正。
- $\nu_{k,t}$：由预算 $k$ 和当前温度 $t$ 诱导的重加权任务概率分布。
- $\mu$：原始任务总体分布。
- $A_k'(t)$：总体 pass@$k$ 对温度的导数，其符号表示局部升温是否提高目标。

<div class="equation-explanation" markdown="1">

**直观理解**：该分解把导数拆成正尺度因子 $kZ_{k,t}$ 与加权平均响应。随着 $k$ 增大，因子 $q_t(X)^{k-1}$ 更强地压低容易任务的权重；若低成功率任务的 $m_t(P)$ 更大，则更大预算下的平均响应不会降低，由此得到温度导数的符号嵌套。<br>
**原文位置**：第 3 节，公式 (3)–(5)；导数起点见公式 (2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文没有训练模型、学习损失或参数更新过程；数学优化对象是在给定生成模型、任务分布和验证规则后，对每个预算 $k$ 选择 $t_k\in\operatorname*{arg\,max}_{t\in I}A_k(t)$。主要结果提供的是使 $t_k$ 随 $k$ 非减的充分条件，而非用于数值训练的目标函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 条件对数成功响应**

定义 $\eta_t(X)=\partial_t\log p_t(X)=\dot p_t(X)/p_t(X)$，并按当前单次成功率 $P$ 条件化得到 $m_t(u)=\mathbb{E}[\eta_t(X)\mid P=u]$；在仅假设 $\dot p_t$ 可积时，论文采用等价形式 $\mathbb{E}[\dot p_t(X)\mid P=u]/u$。核心假设是 $m_t(u)$ 在 $u$ 上非增，它是需要由任务级响应数据检验的“困难任务受益”条件，并非 pass@$k$ 的代数必然结果。

> 直观理解：直接比较成功率增加多少会偏向本来就容易的任务，因此作者比较升温带来的比例变化。该模块把任务难度和温度敏感度联系起来，明确指出什么样的跨任务结构足以推动最优温度随预算上升。

**2. 预算诱导的似然比倾斜**

分布 $\nu_{k,t}$ 以 $P(1-P)^{k-1}$ 重加权任务；当 $\ell>k$ 时，$\mathrm{d}\nu_{\ell,t}/\mathrm{d}\nu_{k,t}$ 与 $(1-P)^{\ell-k}$ 成正比，且该比率随 $P$ 非增。因此更大预算在单调似然比意义下把边际决策权移向单次成功率更低的任务，而定理实际排序的是归一化导数 $A_k'(t)/(kZ_{k,t})$，不声称原始导数幅值随 $k$ 增大。

> 直观理解：一个容易任务在多次采样后几乎必然成功，继续为它调整温度的价值会迅速下降；困难任务仍有较高的全失败概率，所以更能影响下一点温度变化是否值得。归一化限制很重要，因为总边际增益可能随预算饱和并缩小。

**3. 从局部导数到全局最优温度**

导数符号嵌套本身只给出同一温度处的局部比较。作者额外要求每个 $A_k$ 严格导数单峰：存在唯一最大化点 $t_k$，其左侧导数为正、右侧导数为负；由 $A_k'(t_k)=0$ 和符号嵌套可推出较大预算的最大化点不能位于 $t_k$ 左侧，边界点则用单侧方向处理。

> 直观理解：知道某一点继续升温是否有利，并不足以确定整条曲线的最高点在哪里。严格单峰性排除了多个峰和反复起伏，使局部方向能够可靠地转化为最优温度顺序。

**训练与推理**

该方法属于推理配置分析。理论上，先在候选温度附近获得每个任务的单次成功率函数 $p_t(X)$ 或其局部估计，再计算总体目标 $A_k(t)$；随后用邻近温度估计 $\dot p_t(X)$，按当前成功率分组或进行形状约束回归以估计 $m_t(u)$，检验其是否随 $u$ 非增。还需独立扫描 $t\mapsto A_k(t)$，确认各预算下目标严格单峰；只有这两个条件都得到支持时，才能依据推论 3.6 预测更大预算的最优温度不低于较小预算。若条件不成立，应直接比较各预算的经验目标，不能把论文定理当作无条件调温规则。

**复现信息**

理论成立依赖以下关键设定：给定 $(X,t)$ 后的 $k$ 个完成独立同分布；验证器对二元成功事件完全正确；分析点满足 $0<p_t(X)<1$，$p_t(X)$ 对温度几乎处处可微，$\mathbb{E}|\dot p_t(X)|<\infty$，且允许交换求导与期望。边界温度需要单侧导数及相应的支配收敛条件。连续密度情形的 $\mathrm{Beta}(2,k)$ 表示不能原样视为有限基准集上的密度估计；它主要用于解释权重位置。附录 C 说明配套的标准库 Python 程序只核验闭式最优解、上下行示例、离散凸性恒等式、有限差分诊断和图中数值，主要定理仍以解析证明为依据。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**总体 $\operatorname{pass}@k$**

定义为 $A_k(t)=\mathbb{E}[1-(1-p_t(X))^k]$，衡量从任务总体中抽取任务后，以同一温度独立生成 $k$ 次、至少一次被接受的平均概率。 （越高越好，因为目标事件是 $k$ 次尝试中至少一次成功；但这一指标依赖条件独立同分布采样和完美验证假设。）

</div>
<div class="metric-item" markdown="1">

**归一化温度导数**

衡量温度微调对总体 $\operatorname{pass}@k$ 的边际方向，并通过归一化把不同预算下的权重解释为对任务成功率分布的概率倾斜。论文证明单调的是该归一化导数，而非原始导数幅度。 （其正负而非绝对大小是关键：正值表示在当前温度继续升温会提高目标，负值表示降温方向更有利；随 $k$ 增大而不减可产生跨预算的导数符号嵌套。）

</div>
<div class="metric-item" markdown="1">

**最优温度 $t_k^*$**

在给定预算 $k$ 下最大化总体 $A_k(t)$ 的温度。它是论文最终关心的比较静态量，而不是直接测得的模型质量分数。 （不存在统一的越高或越低越好；应选择使 $A_k(t)$ 最大的温度。论文研究的是在额外单峰假设下，$t_k^*$ 是否随 $k$ 非递减。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 一般任务总体；比较任意两个采样预算，并假设条件对数成功响应 $m_t(u)=\mathbb{E}[\dot p_t(X)\mid p_t(X)=u]/u$ 随当前成功率 $u$ 非递增。

<div class="result-value" markdown="1">

作者证明，聚合 $\operatorname{pass}@k$ 的归一化温度导数随预算 $k$ 非递减，因此较小预算下已经支持升温的导数符号，在更大预算下不会反转为支持降温。若每条温度—性能曲线还严格单峰，则唯一最优温度 $t_k^*$ 随 $k$ 非递减。

</div>

条件要求“当前越难的任务，升温带来的相对成功率增益越大”。增大预算会把边际决策权转向仍容易全部失败的任务，于是总体更倾向高温。该结论只是充分条件，不表示所有模型、任务集或温度区间都满足该响应排序；没有严格单峰性时，导数排序也不能自动给出唯一最优温度的排序。

<div class="result-source" markdown="1">

来源：Abstract；一般充分条件定理的摘要陈述

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

If $m_t(u)$ is nonincreasing in current success probability, then the normalized temperature derivative of aggregate pass@$k$ is nondecreasing in $k$.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 双层任务总体的仿射响应模型，用两个具有不同成功率和温度响应的任务层分析参数区域。

<div class="result-value" markdown="1">

作者导出闭式相图和最优解；不同参数区既可能出现最优温度随预算上升，也可能出现下降，并可计算大预算极限。

</div>

这一结果说明“预算越大，最佳温度越高”不是 $\operatorname{pass}@k$ 的代数定律。方向由低成功率任务与高成功率任务各自如何响应温度决定；若响应排序与主定理相反，聚合最优温度可以下降。双层模型是解析反例和机制示范，不是从真实基准数据拟合出的经验规律。

<div class="result-source" markdown="1">

来源：Abstract；双层模型与核表示概述

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We derive a closed-form two-stratum phase diagram, including upward and downward regimes, and show that the marginal temperature derivative admits an exact $\mathrm{Beta}(2,k)$ kernel representation whose kernel concentrates at one-sample success of order $1/k$.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 具有连续单次成功率分布的总体边际分析；将温度导数写成 $\mathrm{Beta}(2,k)$ 核加权形式。

<div class="result-value" markdown="1">

边际温度效应具有精确的 $\mathrm{Beta}(2,k)$ 核表示；随着 $k$ 增大，该核集中到单次成功率约为 $1/k$ 的区域。作者同时指出，把这种核集中解释为任务层面的局部化，还需要零附近的密度—响应因子规则且不消失。

</div>

直观上，预算为 $k$ 时，最能左右“再升一点温是否有利”的任务不是任意难题，而是单次成功率与 $1/k$ 同量级的任务。不过，核本身集中并不保证真实任务贡献也集中：如果该成功率区域几乎没有任务，或任务对温度几乎不响应，局部化解释就会失效。

<div class="result-source" markdown="1">

来源：Abstract；紧接 $\mathrm{Beta}(2,k)$ 核表示的限定说明

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Interpreting that scale as task-level localization additionally requires a regular, nonvanishing density–response factor near zero.

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

- 固定任务基线：对单个任务，$\operatorname{pass}@k=1-(1-p_t)^k$ 是单次成功率 $p_t$ 的严格递增变换，因此最优温度不随 $k$ 改变。它用于排除“预算直接改变单任务偏好”这一解释，并表明总体最优温度移动必须来自任务异质性或模型假设失效。
- 定性难题重加权解释：已有工作指出，大预算通过权重 $k(1-p)^{k-1}$ 更重视低成功率任务。本文以此为概念基线，进一步检验何种条件可将定性直觉升级为导数符号嵌套和最优温度单调性的充分条件。
- OSCA多配置分配框架：该框架允许在温度、模型或语言等配置间混合预算，是附录离散分配结果的直接比较对象。本文只给出整数端点、稀疏支持和大预算极限等细化，不声称首次提出混合配置优化。

**实验想回答的问题**

- 在条件独立同分布采样、固定温度和完美验证器的总体模型下，什么任务级响应条件能够保证：随着采样预算 $k$ 增大，聚合 $\operatorname{pass}@k$ 的最优温度不会下降？
- 这种预算依赖性通过何种任务重加权机制产生，并且在双层任务模型、连续成功率分布及多配置分配中会呈现哪些可检验的结构？

**实验实现**

本文没有训练语言模型，也没有调用模型形成实验测量，因而没有真实数据集、训练/测试划分、模型规模或采样次数等常规实验设置。评估以解析证明和标准库 Python 回归检查为主：总体任务记为 $X\sim\mu$，温度位于紧区间 $I=[\underline{t},\overline{t}]$，给定任务与温度后各次生成条件独立同分布，验证器对二元成功事件完全准确。Python 检查覆盖闭式最优解、双层模型的上升与下降区间、离散凸性恒等式、有限差分诊断和文中展示数值；图形直接由解析公式生成。这些计算仅检查推导实现是否一致，不构成对真实大语言模型的经验验证。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 论文将 Codex 中“$\operatorname{pass}@1$ 最优温度约为 $0.2$、$\operatorname{pass}@100$ 最优温度约为 $0.8$”作为既有经验现象，而不是自身实验结果。它说明待解释的总体模式确实曾被观察到，但单个外部案例既不能验证条件对数成功响应的单调性，也不能证明该规律跨模型普遍成立。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper studies how sampling temperature should scale with inference budget under Pass@k, a central test-time reasoning and sampling question.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`98bd9bf54a6f1a25609c3b927a968851f672587eb369af7e92a0d6c478d9116a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
