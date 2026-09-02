---
title: "[论文解读] ES-AHD: An Evolution Strategy Framework for Automatic Heuristic Design"
description: "[arXiv 2609.00023][LLM Reasoning] ES-AHD将进化策略的“中心引导搜索”和“搜索范围自适应”思想引入大语言模型驱动的自动启发式设计，以减少随机代码变异的盲目性，并动态平衡局部改进与全局探索。"
arxiv_id: "2609.00023"
announcement_date: "2026-09-02"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:54:09.704668+00:00"
source_sha256: "abb17bb38b7a48f8f3175fc4d186d74b2f1cee595013fdeefe8cbef19719b223"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "自动启发式设计"
  - "进化策略"
  - "大语言模型"
  - "语义重组"
  - "采样温度"
  - "组合优化"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.00023</p>

# ES-AHD: An Evolution Strategy Framework for Automatic Heuristic Design

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Yutao Lai, Kezhao Lai, Hai-Lin Liu, Yuping Wang, Ping Guo</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: 1 School of Mathematics and Statistics Guangdong University of Technology Guangzhou, China；Affiliation: 2 School of Computer Science and Technology Xidian University Xi’an, China；Affiliation: 3 School of Systems Science Beijing Normal University Beijing, China；School of Mathematics and Statistics；Guangdong University of Technology；School of Computer Science and Technology；Xidian University；School of Systems Science；Beijing Normal University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00023v1) · [PDF 下载](https://arxiv.org/pdf/2609.00023v1) · **关键词** 自动启发式设计, 进化策略, 大语言模型, 语义重组, 采样温度, 组合优化<br>
**代码**: [https://github.com/Mriya0306/ES-AHD](https://github.com/Mriya0306/ES-AHD)

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

ES-AHD将进化策略的“中心引导搜索”和“搜索范围自适应”思想引入大语言模型驱动的自动启发式设计，以减少随机代码变异的盲目性，并动态平衡局部改进与全局探索。

**不用术语来说**：复杂组合优化问题通常难以在可接受时间内精确求解，因此实践中需要启发式算法；但优秀启发式长期依赖专家反复试验，而现有自动方法要么难以表达复杂程序，要么让大语言模型围绕少量代码随机改写，容易浪费评估预算或反复生成相似的错误方案。本文关注如何让模型更有方向地提出候选算法，同时不过早困在某一类方案中。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出基于大语言模型的语义重组：从表现最好的 Top-$K$ 个候选程序中显式提炼“核心洞见”，将其作为群体层面的语义中心与改进方向，再据此生成新候选，以替代盲目的点对点交叉或个体变异。
- 提出通过采样温度实现的随机协方差适应：把进化策略中的全局搜索方差类比为大语言模型的采样温度，利用带动量和高斯噪声的随机游走逐步收缩搜索范围，同时保留偶尔升高温度、跳出语义局部最优的可能性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究面向组合优化的自动启发式设计（Automatic Heuristic Design, AHD）。车辆路径、装箱与调度等问题通常具有 NP-hard 性质，精确算法难以在可接受时间内求得最优解，因此实践中常使用贪心、局部搜索或元启发式算法；但高性能启发式长期依赖专家手工构造，成本高且跨问题泛化困难。传统 AHD 以遗传编程为代表，在抽象语法树或低层指令构成的预定义空间内演化规则，表达复杂控制逻辑和数据结构的能力有限。大语言模型（LLM）能够直接生成并理解代码，因而可充当候选启发式的生成、交叉和变异算子；本文进一步把进化策略（ES）的“围绕优良中心定向采样并调节搜索尺度”思想引入这一过程。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自动启发式设计（AHD）**

AHD 将启发式算法本身视为待搜索对象，通过自动生成、执行评估和迭代改进，减少对领域专家手工设计的依赖。本文关注的是直接生成可执行代码形式的启发式，而不只是调节现有算法的参数。

</div>
<div class="concept-item" markdown="1">

**大语言模型驱动的代码演化**

LLM 根据问题描述、已有候选代码及反馈生成新的程序，可在语义层面组合算法思想，并实现循环、条件分支和复杂数据结构。生成结果仍须由外部评估器实际运行和打分，因为语言模型输出不保证正确或高效。

</div>
<div class="concept-item" markdown="1">

**进化策略（ES）与探索—利用权衡**

进化策略通常围绕当前优良解所确定的中心进行采样，并通过方差或协方差控制搜索方向与范围；范围大偏向探索新区域，范围小偏向利用已有优良区域。本文在代码语义空间中类比这一机制，以 Top-K 候选提炼搜索中心，并以 LLM 采样温度近似控制搜索尺度。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个组合优化问题、可执行的候选启发式代码表示，以及能够在问题实例上运行代码并返回质量评价的自动评估环境，目标是在有限的 LLM 调用与评估预算内产生高性能启发式。搜索过程维护一组候选程序，依据评估结果选择表现最好的 Top-K 个体，利用 LLM 从中提炼共享的“核心洞见”，再以该语义方向生成新代码；采样温度承担类似 ES 搜索方差的作用，用于调节新候选与当前优良策略之间的差异。其基本假设是：候选代码能够被可靠执行和比较，LLM 能从优良程序及上下文中抽取有用策略，而温度变化可近似影响代码生成的语义多样性。输出是经评估后表现较好的、可执行且具有人类可读性的启发式算法代码，而非组合优化实例本身的单次解。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$K$**

参与语义重组、用于提炼核心洞见的高性能候选数量，即 Top-K 中的候选数；节选未给出具体取值。

</div>
<div class="notation-item" markdown="1">

**$T$**

LLM 的采样温度，用来类比进化策略中的全局搜索方差或搜索半径；较高温度通常对应更强探索，较低温度对应更细致的局部改进。

</div>

</div>

**直接相关的工作**

- **Evolution of Heuristics（EoH）**: EoH 同时演化自然语言“思想”和可执行代码，利用 LLM 的语义能力提高启发式生成质量，是本文最直接的 LLM 驱动演化式 AHD 前序框架之一。本文认为这类方法仍主要沿用遗传算法式的个体级交叉或变异，缺乏从多个优良个体中提取宏观共同方向的机制。
- **ReEvo**: ReEvo 使用 LLM 反思历史成功与失败，并以文字反馈形成类似“语言梯度”的指导，从而缓解盲目改写问题。与之相比，ES-AHD 的切入点是把 Top-K 候选汇聚为语义搜索中心，并通过随机变化的采样温度类比 ES 的搜索尺度适应；节选未提供二者效果优劣的实验结论。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

车辆路径、装箱和调度等现实组合优化问题通常具有 NP-hard 性，精确算法难以保证在多项式时间内得到最优解，因而需要高质量启发式算法。然而，人工设计贪心规则、局部搜索或元启发式框架要求专家具备深厚领域知识并进行大量试错，不仅成本高、周期长，还可能受认知偏差影响，且手工算法往往难以跨问题领域泛化。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于遗传编程的传统自动启发式设计**：将基础算子和规则作为构件，在预先规定的搜索空间中，通过选择、交叉和变异演化启发式规则，通常使用抽象语法树或低层指令来表示候选算法。
- **基于大语言模型的进化式自动启发式设计（如 FunSearch、EoH）**：利用大语言模型的代码生成能力和先验知识，把模型当作交叉或变异算子，在若干父代代码之间产生可直接执行的新启发式程序，并通过任务性能评估和筛选推动迭代。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 传统遗传编程受抽象语法树或低层指令集约束，程序表达能力有限；尽管形式搜索空间很大，却较为稀疏，难以有效产生同时包含高级数据结构、循环和条件分支的复杂、可读且高性能启发式算法。
- 现有大语言模型方法大多沿用遗传算法式的个体级、点对点随机交叉或变异，缺少从优良群体中提取全局策略的机制，因而搜索方向盲目；同时固定采样温度不能随搜索阶段调节探索强度，模型可能反复生成相似的缺陷代码，导致探索与利用失衡。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未形成一种适用于高维程序语义空间的群体级搜索机制：它既要把多个精英候选共有的有效策略汇总为明确的搜索中心和方向，又要根据迭代状态动态控制候选代码的语义差异，而不是继续依赖孤立个体的随机改写或固定温度采样。

</div>
<div markdown="1"><span>核心问题</span>

如何把进化策略的中心引导与搜索方差调节机制落实到大语言模型的代码生成过程中，使自动启发式设计能够在有限迭代内进行更有方向的候选生成，并兼顾精细改进与跳出语义局部最优？

</div>
<div markdown="1"><span>作者直觉</span>

如果让大语言模型先比较一组高分程序并概括它们共同奏效的“核心洞见”，新程序就能围绕一个较可信的语义中心生成，而不必从单个父代随机试探；采样温度则可被视为搜索半径，较低温度适合围绕当前思路做细节优化，偶尔出现的较高温度可产生差异更大的方案。将温度设置为带惯性和随机扰动的变化过程，理论直觉上比固定温度或单调降温更能兼顾稳定收敛与逃离局部最优。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ES-AHD 将自动启发式设计建模为离散但具有“连续式”搜索特征的高维语义优化问题。搜索空间为所有语法有效的启发式程序 $\mathcal{X}$，目标是在组合优化问题描述 $\mathcal{D}$ 和适应度函数 $f:\mathcal{X}\rightarrow\mathbb{R}$ 给定时，迭代生成并筛选高性能程序，最终输出全局最佳启发式算法 $x^*$. 技术上，方法用 LLM 对精英程序进行语义归纳，形成类似进化策略均值的语义搜索中心，再用带动量和随机扰动的温度更新控制 LLM 采样尺度。直观地说，它不是让 LLM 对某一个程序盲目改几个 token，而是先总结优秀程序共同采用的设计思想，再围绕该思想生成下一批候选，同时偶尔提高随机性以跳出局部最优。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### LLM 驱动初始化

在零样本提示下，LLM 以温度 $T_0$ 独立采样 $\lambda$ 个语法有效的启发式程序，构成初始种群 $\mathcal{P}^{(0)}=\{x_1^{(0)},\ldots,x_\lambda^{(0)}\}$。

<div class="method-step__io" markdown="1">

**输入**：目标组合优化问题的自然语言描述 $\mathcal{D}$、初始温度 $T^{(0)}=T_0$ 和种群规模 $\lambda$。<br>
**输出**：初始启发式程序种群 $\mathcal{P}^{(0)}$。

</div>

**直观理解**：方法不要求人工提供一个可用的起始算法，也不先随机拼接语法树，而是让 LLM 根据题目说明直接提出一批候选方案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 评估与精英选择

执行每个候选启发式程序并计算 $f(x)$，按照性能选择前 $\mu$ 个个体组成精英集合 $\mathcal{E}^{(g)}=\{x_{1:\lambda}^{(g)},\ldots,x_{\mu:\lambda}^{(g)}\}$，同时持续记录全局最佳程序 $x^*$。

<div class="method-step__io" markdown="1">

**输入**：当前种群 $\mathcal{P}^{(g)}$、目标问题实例和适应度函数 $f$。<br>
**输出**：精英集合 $\mathcal{E}^{(g)}$ 和截至当前的最佳程序 $x^*$。

</div>

**直观理解**：这一阶段相当于在实际题目上考试：保留成绩最好的少数程序，并把历史上最好的方案单独记住，避免后续采样变差后丢失成果。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 语义重组与搜索中心更新

通过 LLM 语义反思算子 $\Phi_{\mathrm{reflect}}$ 提取精英程序中的共同逻辑、设计模式和高性能原因，生成核心洞见 $\mathcal{I}^{(g)}=\Phi_{\mathrm{reflect}}(\mathcal{E}^{(g)})$，将其作为下一代的语义搜索中心。

<div class="method-step__io" markdown="1">

**输入**：精英程序集合 $\mathcal{E}^{(g)}$。<br>
**输出**：自然语言形式的核心洞见 $\mathcal{I}^{(g)}$。

</div>

**直观理解**：数值进化策略可以直接平均参数，但程序代码不能简单逐字符平均；因此 LLM 负责把多个优秀程序“概括成一套设计原则”，再以这套原则指导生成。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 随机协方差适应与下一代采样

先按带高斯噪声的随机递推更新温度 $T^{(g)}$，再让 LLM 以 $\mathcal{I}^{(g)}$ 为语义中心、以 $T^{(g)}$ 控制采样随机性，独立生成 $\lambda$ 个新启发式程序，形成 $\mathcal{P}^{(g+1)}$。

<div class="method-step__io" markdown="1">

**输入**：上一代温度 $T^{(g-1)}$、步长 $\delta$、温度下界 $T_{\min}$、核心洞见 $\mathcal{I}^{(g)}$ 和种群规模 $\lambda$。<br>
**输出**：下一代种群 $\mathcal{P}^{(g+1)}$；循环达到最大代数 $G$ 后输出全局最佳程序 $x^*$。

</div>

**直观理解**：温度较低时，LLM 更集中地微调已经发现的好思路；随机温度偶尔升高时，搜索会尝试更不同的语义方案，从而降低过早停在局部最优的风险。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 精英语义重组

$$
\mathcal{I}^{(g)}=\Phi_{\mathrm{reflect}}\left(\mathcal{E}^{(g)}\right)
$$

**符号说明**

- $\mathcal{I}^{(g)}$：第 $g$ 代由 LLM 生成的核心洞见，即语义搜索中心。
- $\Phi_{\mathrm{reflect}}$：LLM 的语义反思、归纳与摘要算子。
- $\mathcal{E}^{(g)}$：第 $g$ 代按适应度选出的前 $\mu$ 个精英启发式程序集合。
- $g$：进化代数。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把多个离散程序转换成一个可用于提示 LLM 的共同设计思想。它实现了进化策略中“更新均值”的功能，但均值不再是代码或参数的算术平均，而是语义层面的归纳结果。<br>
**原文位置**：Section III-A，式（2）

</div>

</div>

<div class="equation-block" markdown="1">

#### 随机温度更新

$$
T^{(g)}=\max\left(T_{\min},(1-\delta)\cdot T^{(g-1)}+\delta\cdot\epsilon^{(g)}\right),\quad\epsilon^{(g)}\sim\mathcal{N}(0,1)
$$

**符号说明**

- $T^{(g)}$：第 $g$ 代 LLM 采样温度，用于控制语义搜索的随机程度和范围。
- $T_{\min}$：温度的正下界，满足 $T_{\min}>0$，防止搜索方差完全收缩。
- $\delta$：常数步长，满足 $\delta\in(0,1)$，控制旧温度保留比例与随机扰动强度。
- $T^{(g-1)}$：上一代的采样温度。
- $\epsilon^{(g)}$：第 $g$ 代独立采样的高斯噪声变量。
- $\mathcal{N}(0,1)$：均值为 $0$、方差为 $1$ 的正态分布。

<div class="equation-explanation" markdown="1">

**直观理解**：温度主要继承上一代状态，因此搜索不会每代剧烈改变；同时加入高斯扰动，使温度有机会升高或降低。取最大值保证温度始终为正，避免探索能力完全消失。<br>
**原文位置**：Section III-B，式（3）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：该方法不是通过梯度下降训练一个固定参数模型，而是把目标组合优化问题上的启发式程序性能作为适应度。对于每个候选程序 $x\in\mathcal{X}$，系统计算 $f(x)$，选择表现最好的前 $\mu$ 个程序来产生下一代语义中心；因此优化对象是程序搜索过程及其最终输出 $x^*$，而不是 LLM 本身的参数。所给章节未明确说明 $f$ 的具体数学形式、不同问题中的最小化或最大化方向，也未给出额外的正则项或训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. LLM 语义重组**

传统进化策略用精英个体的算术平均更新数值均值 $m^{(g)}$，但离散程序代码不存在有意义的直接平均。ES-AHD 用 $\Phi_{\mathrm{reflect}}$ 对精英集合进行上下文推理和摘要，得到位于自然语言语义空间中的核心洞见 $\mathcal{I}^{(g)}$，将其视为传统搜索中心的语义对应物。

> 直观理解：该模块把“平均优秀个体”改写为“总结优秀个体的共同做法”。这样，下一轮搜索围绕可解释的算法思想展开，而不是围绕某个程序进行盲目的局部改写。

**2. 随机温度协方差适应**

方法将进化策略中的搜索协方差近似映射为 LLM 采样温度，并使用带动量的随机游走更新。因温度被限制为不低于严格正数 $T_{\min}$，搜索半径可以收缩以进行细化，但不会完全失去探索能力。

> 直观理解：温度可以理解为“尝试新想法的幅度”：通常逐渐稳定有利于精修，但保留随机跳动，必要时仍能探索远离当前方案的方向。

**3. 精英驱动的闭环搜索**

每一代都执行“生成—评估—选择—反思—再生成”闭环：LLM 负责程序提出与语义归纳，目标问题上的适应度 $f$ 负责外部评价，精英集合负责将评价结果反馈给下一代。全局最佳程序 $x^*$ 被持续跟踪，输出不依赖最后一代是否恰好包含最优候选。

> 直观理解：LLM 负责创造和总结，真实优化任务负责判定好坏；两者反复交替，使搜索方向由实际性能而非语言上的自洽性决定。

**训练与推理**

初始化阶段，输入问题描述 $\mathcal{D}$、种群规模 $\lambda$、初始温度 $T_0$、精英规模 $\mu$、步长 $\delta$ 和最大代数 $G$，LLM 生成初始种群。每一代先在目标问题上执行全部候选并计算适应度，选择精英并更新全局最佳；随后 LLM 反思精英集合得到 $\mathcal{I}^{(g)}$，按照随机温度更新式得到 $T^{(g)}$，再以核心洞见和新温度采样下一代。达到 $G$ 后返回记录的 $x^*$；这里的“推理”实质上是对候选启发式程序进行执行评估，而非对一个已训练的端到端预测器进行单次前向推理。

**复现信息**

复现所必需的高层配置包括：搜索空间限定为语法有效的启发式程序；每代种群规模为 $\lambda$，精英规模为 $\mu$；初始采样使用温度 $T_0$；温度更新使用 $\delta\in(0,1)$、高斯噪声 $\epsilon^{(g)}\sim\mathcal{N}(0,1)$ 和正温度下界 $T_{\min}$；迭代上限为 $G$。所给章节未明确报告 LLM 的具体型号、提示模板、随机种子、候选程序去重规则、无效代码处理方式、每个候选的评估次数、$T_0$、$T_{\min}$、$\delta$、$\lambda$、$\mu$ 和 $G$ 的具体取值，因此不能据此完整复现实验数值。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- TSP $N=20$ 实例：由城市及两两距离构成，目标是寻找访问每个城市恰好一次并回到起点的最短回路。训练实例用于执行候选启发式并计算适应度；对应的测试集以 Val20 平均路径长度衡量验证表现。原文未交代实例数量、坐标分布或训练—测试划分方式。
- TSP $N=50$ 实例：实验重点比较的中等规模问题，候选程序实现 `select_next_node`，根据当前节点、目标节点、未访问节点集合和距离矩阵逐步构造完整回路。训练阶段报告 Top-4 Average Score，测试阶段报告 Val50 平均路径长度；原文未交代实例数量与生成过程。
- TSP $N=100$ 实例：用于考察生成式启发式随问题规模增大时的可扩展性，对应测试指标为 Val100 平均路径长度。该设置只能检验从较小到较大 TSP 规模的经验表现，原文未说明是否使用独立分布、跨规模迁移或分别训练。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Top-4 Average Score**

训练性能指标，取训练集上表现最好的 4 个生成启发式函数所得负总路径长度的平均值。它同时反映搜索能否产生多个较优候选，但只观察前 4 名，不能完整表示整个候选群体的平均质量或方差。 （越高越好，因为得分定义为总路径长度的负值；数值越高意味着对应路径越短。）

</div>
<div class="metric-item" markdown="1">

**Val20、Val50、Val100 平均路径长度**

分别统计生成启发式在 $N=20$、$N=50$、$N=100$ 测试集上的平均回路长度，用于衡量未直接参与训练评价的实例上的解质量。 （越低越好，因为 TSP 的目标是最小化完整回路的总距离。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### TSP $N=50$ 的 ES-AHD 与 EoH、ReEvo、FunSearch 定量比较

<div class="result-value" markdown="1">

原文说明表 I 比较了 Top-4 平均训练得分以及不同规模的验证结果，但所给材料没有包含任何完整数据行，因而无法核实 ES-AHD 的具体分数、领先幅度或排序。

</div>

该比较本应回答 ES-AHD 在同一底层 LLM 下是否比现有搜索框架找到更短的路径。仅凭“表 I 展示比较结果”不能推出 ES-AHD 显著更优，也不能判断优势来自更好的训练搜索还是更强的测试泛化。

<div class="result-source" markdown="1">

来源：第 IV-D 节，表 I 引导句；所给摘录未包含表 I 数据行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table I presents the comparative results on the TSP $N=50$ instances.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨规模验证：Val20、Val50 与 Val100

<div class="result-value" markdown="1">

实验设计报告三个规模测试集上的平均路径长度，但所给材料未提供相应数值，因此无法判断 ES-AHD 是否在全部规模上占优，也无法计算性能随 $N$ 增大的退化程度。

</div>

跨规模结果旨在检验生成启发式是否只适合某个固定规模。即使三个规模均领先，也只能支持在这些 TSP 实例分布上的经验可扩展性，不能自动证明对更大规模、不同城市分布或其他组合优化问题的普适性。

<div class="result-source" markdown="1">

来源：第 IV-B 节，Evaluation Metric

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For validation, we report the average route distances on the test sets for each respective scale (Val20, Val50, Val100).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Top-4 候选的训练搜索质量

<div class="result-value" markdown="1">

原文定义了 Top-4 Average Score，并明确该指标越高代表路径越短；但所给材料没有报告各方法的具体训练分数，无法验证 ES-AHD 是否确实加速搜索或提升最优候选质量。

</div>

Top-4 平均值比单独报告最佳个体更不容易被偶然的单个高分程序主导，但它仍聚焦于精英候选。该指标不能单独证明搜索效率，因为效率还需要结合相同函数评价次数、LLM 调用次数或运行时间进行比较。

<div class="result-source" markdown="1">

来源：第 IV-B 节，Evaluation Metric

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

This score represents the negative total route distance achieved by the top 4 generated heuristic functions on the training set; a higher score indicates a shorter route and thus better performance.

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

- EoH：把 LLM 用作交叉与变异算子，直接在代码空间中进行进化搜索。它与 ES-AHD 同属 LLM 驱动的进化式自动启发式设计，因此可检验 ES-AHD 的语义中心引导与温度适应是否优于传统个体级进化操作。
- ReEvo：通过提示 LLM 重写已有启发式代码并迭代优化。该基线代表以代码改写和局部精炼为核心的进化方法，可用于比较 ES-AHD 的显式语义重组方向是否带来额外收益。
- FunSearch：将预训练 LLM 与自动评价器结合，在程序空间中发现高质量函数，是代表性的 LLM 程序搜索框架。它提供了不以 ES 式语义中心和协方差适应为核心的对照。
- 所有 LLM 驱动方法统一采用 GLM 4-Flash 作为启发式生成引擎。这不是额外算法基线，而是公平性控制：尽量让差异来自搜索框架，而不是底层语言模型。

**实验想回答的问题**

- 在统一使用 GLM 4-Flash 生成启发式代码的条件下，ES-AHD 相比 EoH、ReEvo 和 FunSearch，能否搜索到训练得分更高、测试路径更短的 TSP 贪心构造启发式？
- ES-AHD 所生成启发式能否适用于不同规模的 TSP 实例，即在 $N=20$、$N=50$ 和 $N=100$ 上保持较好的优化效果、鲁棒性与规模扩展能力？

**实验实现**

AHD 的输出是一个贪心构造函数 `select_next_node`：它在每一步读取当前节点、目标节点、尚未访问的节点和距离矩阵，选择下一座城市，反复调用后形成完整 TSP 回路。每代对候选启发式在训练实例上执行并计算适应度，再选择前 $\mu$ 个个体作为精英并更新全局最佳解。实验覆盖 $N=20$、$N=50$、$N=100$，并统一使用 GLM 4-Flash，以减少底层 LLM 差异造成的混杂。所给章节未报告实例数量、运行次数、随机种子、调用预算、停止条件、显著性检验、误差条或具体硬件，因此无法判断计算成本是否严格一致，也无法量化结果的随机稳定性。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Uses LLM semantic reasoning and code generation within an evolution-strategy search framework to design heuristic algorithms.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`abb17bb38b7a48f8f3175fc4d186d74b2f1cee595013fdeefe8cbef19719b223`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
