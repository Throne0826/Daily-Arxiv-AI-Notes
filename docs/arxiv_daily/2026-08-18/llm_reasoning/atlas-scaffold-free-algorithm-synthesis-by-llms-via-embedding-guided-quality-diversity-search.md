---
title: "[论文解读] ATLAS: Scaffold-Free Algorithm Synthesis by LLMs via Embedding-Guided Quality-Diversity Search"
description: "[arXiv 2608.15546][LLM Reasoning] ATLAS试图在不预设算法内部结构的条件下，让大语言模型生成完整的组合优化算法，并通过嵌入空间中的质量—多样性搜索同时改进性能、保存多种有竞争力的设计并利用失败信息进行修复。"
arxiv_id: "2608.15546"
announcement_date: "2026-08-18"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:17:32.622545+00:00"
source_sha256: "dd4d966bafb7433b59ace0139f2e77da12cf82a17b60ffcf7dbb5c0ba56563c2"
tags:
  - "LLM Reasoning"
  - "自动算法设计"
  - "组合优化"
  - "大语言模型"
  - "质量多样性优化"
  - "多模态搜索"
  - "无脚手架全算法合成"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.15546</p>

# ATLAS: Scaffold-Free Algorithm Synthesis by LLMs via Embedding-Guided Quality-Diversity Search

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Danial Yazdani, Mohammad Nabi Omidvar, Yuan Sun, Maksud Ibrahimov, Xiaodong Li</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Thanks: Danial Yazdani and Xiaodong Li are with the School of Computing Technologies, RMIT University, Melbourne, VIC, Australia；Mohammad Nabi Omidvar is with the School of Computing and Leeds University Business School, University of Leeds, Leeds, UK；Yuan Sun is with La Trobe Business School, La Trobe University, Melbourne, VIC, Australia</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.15546) · [PDF 下载](https://arxiv.org/pdf/2608.15546) · **关键词** 自动算法设计, 组合优化, 大语言模型, 质量多样性优化, 多模态搜索, 无脚手架全算法合成<br>
**代码**: [https://github.com/Danial-Yazdani/ATLAS](https://github.com/Danial-Yazdani/ATLAS)

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

ATLAS试图在不预设算法内部结构的条件下，让大语言模型生成完整的组合优化算法，并通过嵌入空间中的质量—多样性搜索同时改进性能、保存多种有竞争力的设计并利用失败信息进行修复。

**不用术语来说**：传统自动算法设计通常只让大语言模型填写一个预留函数，其余求解流程由人类提前搭好；这虽然容易运行，却限制了模型重新安排算法步骤或创造混合方案。若改为让模型编写从读取实例到返回可行解的完整算法，设计空间会显著扩大，但搜索更难，候选程序也更容易出现运行错误、接口不匹配、输出格式错误或违反约束等问题。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出无脚手架的完整算法合成框架ATLAS：用户只提供优化目标、约束和最小输入输出接口，算法的组件选择、控制流程、解的构造及约束处理均由大语言模型完成；外部评估器仅执行、验证并独立重算目标值，不替候选算法补全求解逻辑。
- 提出嵌入引导的质量—多样性搜索及三层资源分配机制：系统在由算法名称、描述和预处理源码的预训练嵌入所形成的动态区域中保存多种候选，分别强化当前最佳区域、改进其他区域的代表，并跨区域重组完整算法；同时把分类后的失败证据交给Repair算子重新生成候选。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型驱动的自动算法设计领域，具体研究组合优化问题中的启发式算法自动合成。组合优化要求在离散、通常规模较大的可行解空间中寻找满足约束且目标值较优的解，例如物流、调度和资源分配问题。已有方法常让大语言模型只生成一个预先指定位置的算法组件，例如优先级选择器、构造启发式或评分函数，而其余控制流程、组件连接方式以及部分可行性处理逻辑由人工设计的算法脚手架固定。本文研究更自由的“无脚手架”全算法合成：给定问题目标、约束和最小输入输出接口，由大语言模型决定完整算法的组件、组件交互和控制流。由于不同的高质量算法可能具有不同的内部组织，作者将搜索视为具有多个模式的设计空间，并使用嵌入表示近似组织这些算法的语义区域；这里的“语义”指算法名称、描述和预处理源代码在预训练嵌入空间中的相似性，而不是由运行行为定义的程序语义。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**组合优化**

组合优化是在离散候选解中寻找满足约束且使目标函数尽可能优或尽可能差的解。本文中，生成的完整程序接收问题实例并返回一个解，同时必须负责解的构造和约束处理。

</div>
<div class="concept-item" markdown="1">

**算法脚手架与全算法合成**

算法脚手架是人工预先规定的整体控制流程，模型只能在指定位置替换一个组件。全算法合成只固定问题规格和最小输入输出接口，模型可以自行选择组件、安排其交互并组织端到端流程。

</div>
<div class="concept-item" markdown="1">

**质量多样性搜索**

质量多样性搜索同时追求候选解的质量和候选集合的多样性，而不是只保留一个当前最优候选。本文以算法嵌入空间中的不同区域表示多样性，使若干具有竞争力但结构不同的算法能够被保留、继续改进并相互组合。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

设一个组合优化任务由问题实例、目标函数和约束条件定义。ATLAS 的输入包括问题规格以及一个最小问题特定输入输出接口：候选算法接收实例和规定格式的数据，输出规定格式的解；外部评估器在统一的运行时间和内存协议下执行该候选算法，检查执行是否成功、接口是否符合要求、输出是否格式正确以及返回解是否满足可行性约束，并独立重新计算目标值。候选算法本身必须完成完整的解构造和约束处理，评估器不会替它补充这些逻辑，也不会把不可行解自动修正为可行解。搜索目标不仅是找到目标值较好的单个程序，还要在预训练嵌入空间中保留多个非冗余、具有竞争力的算法区域，以降低过早收敛到单一设计区域的风险，并为跨区域合成提供不同的完整算法作为参考。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

候选算法接收的问题实例或其相关输入；原文未给出统一的形式化符号定义。

</div>
<div class="notation-item" markdown="1">

**$s(x)\in\{\mathrm{task},\mathrm{harm}\}$**

原文未明确采用该符号；不能据此推断本文的任务类别或损害类别。

</div>
<div class="notation-item" markdown="1">

**$D_{\mathrm{task}}$**

原文未明确采用该符号；本文没有在所给章节中定义名为 $D_{\mathrm{task}}$ 的数据集或任务集合。

</div>
<div class="notation-item" markdown="1">

**$T_d$**

原文未明确采用该符号；本文没有在所给章节中定义名为 $T_d$ 的时间量或任务变量。

</div>

</div>

**直接相关的工作**

- **FunSearch、Evolution of Heuristics（EoH）和 Reflective Evolution（ReEvo）**: 这些方法代表基于大语言模型的组件级自动算法设计：模型迭代生成优先级选择器、构造启发式或评分函数等指定组件，但组件所处的控制流和与其他部分的交互由用户提供的脚手架固定。因此，它们使合成和评估更易管理，却不能自由添加、删除、重排组件或联合重构组件之间的交互；ATLAS 将搜索对象扩展为完整算法。
- **LLaMEA 与 AlphaEvolve**: 二者与全算法或较大范围的程序进化相关，但设计边界不同。LLaMEA 在盒约束黑箱接口下生成完整元启发式算法；AlphaEvolve 演化用户在已有程序中标记的区域。ATLAS 的边界更强调无内部脚手架：除问题定义、约束和最小可调用输入输出接口外，模型负责完整算法的组件选择、控制流、解构造和约束处理。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

物流、调度和资源分配等场景需要高质量优化算法，但人工设计通常依赖大量领域知识和针对具体问题的工程工作。大语言模型有望降低这一成本，不过要真正减少人工架构约束，模型必须能够负责完整的解构造流程和约束处理，而不只是生成某个局部启发式函数。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于脚手架的组件合成方法，如FunSearch、EoH和ReEvo**：用户预先规定总体控制流以及候选组件的接口和角色，大语言模型通过迭代搜索生成或演化其中的优先级选择器、构造启发式或评分函数；外围框架负责其余端到端流程，并可能承担解构造或可行性维护。
- **既有完整算法或程序区域演化方法，如LLaMEA和AlphaEvolve**：LLaMEA在有界黑盒优化接口下生成完整元启发式算法，AlphaEvolve则演化用户在既有程序中标记的区域；二者扩大了可修改范围，但采用的合成边界仍分别受到特定接口或用户所提供程序结构的约束。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 组件合成把算法架构的大部分内容预先固定，使模型无法自由增加、删除或重排组件，也难以联合改造组件之间的交互；因此，固定脚手架之外的构造、局部搜索、元启发式及其混合流程无法被充分探索。
- 放开到完整算法后，搜索空间会变得更大、更异质且可能包含多个彼此分离的优质设计区域；若搜索过早集中于单一当前最佳候选，就可能丢失其他有竞争力的结构。同时，完整程序还扩大了失败面，包括执行、接口、输出格式、解构造和可行性错误，使普通的单一路径演化和评价流程难以稳健处理。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚缺少一种面向组合优化的统一机制，能够在仅保留必要问题定义和外部接口的前提下搜索完整算法，同时动态保存多个结构不同但性能有竞争力的区域，利用这些区域进行定向改进与跨区域重组，并把完整算法特有的分类失败信息转化为后续搜索信号。这里的“语义区域”仅指算法名称、描述和预处理源码在预训练嵌入空间中的相似分组，并不等同于根据运行行为定义的程序语义。

</div>
<div markdown="1"><span>核心问题</span>

在不由用户预设内部组件清单、函数角色划分或控制流的情况下，能否构建一种大语言模型驱动的搜索框架，使其可靠地产生端到端可执行且满足约束的组合优化算法，并在较大的多模态设计空间中兼顾最优候选的持续改进、不同算法区域的保存以及跨区域创新？

</div>
<div markdown="1"><span>作者直觉</span>

算法源码的嵌入表示可充当一种无需人工设计行为描述符的近似地图：相近候选用于检索和去重，较远区域则保留不同的设计素材。ATLAS据此把资源分成三类，一部分深挖当前最佳区域，一部分防止其他区域被淘汰，另一部分让大语言模型阅读来自不同区域的完整源码，选择、舍弃、改造或组合其中的机制。这样，多样性不仅用于避免过早收敛，也直接为新混合算法提供原料；当候选失败时，分类诊断又能告诉Repair算子应针对哪类问题重新生成程序。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ATLAS面向给定组合优化问题，在固定问题规范、最小化算法输入输出接口和统一实验协议下，直接合成完整、可执行的优化算法。候选算法不依赖用户提供的算法骨架、预先规定的组件清单、函数角色划分或内部控制流；它必须自行完成解的构造、约束处理、内部状态管理和停止逻辑，并在资源限制内返回结构化解。外部评估器只负责执行算法、检查返回解是否可行并独立重新计算目标值，不替候选算法修复解或补全控制流程。$\n\nATLAS$以训练实例上的平均成本作为搜索信号，同时把完整算法的源代码映射到嵌入空间，在该空间中维护有效算法档案并形成暂时性的语义区域。搜索由三层组成：围绕当前最优算法及其邻域的精炼、对其他区域代表的区域内成熟化，以及跨区域的多参考合成；因此系统同时追求局部质量提升、弱势但有潜力区域的保留和新型混合算法的发现。直观地说，ATLAS不是只反复修改当前最高分方案，而是把算法视为一组可能相似或不同的设计，保留多个设计方向，再有计划地在方向内部改进并在方向之间重组。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 问题设定与候选生成

通过 $Create$ 在温度 $T=1.0$ 下生成初始完整算法；初始化采用两阶段引导，先进行随机候选生成，再从当前档案中均匀抽取参考算法并使用 $Diverge$ 请求与参考策略不同的算法。后续候选由 $Tune$、$Improve$、$Combine$、$Diverge$ 等语义操作产生，操作对象是完整算法源代码，包括辅助函数定义及其调用关系。

<div class="method-step__io" markdown="1">

**输入**：组合优化问题规范 $\mathcal{P}$、训练实例集 $\mathcal{I}_{\mathrm{train}}=\{x_1,\ldots,x_m\}$、最小化算法输入输出接口、资源限制，以及由大语言模型调用产生的源代码候选。<br>
**输出**：一批候选完整算法；只有能够执行并返回结构化解、且通过可行性验证的候选才进入后续档案。

</div>

**直观理解**：系统先让大语言模型提出若干可运行的完整解题程序，再有意要求部分程序避开已有思路，以免初始方案都变成同一种教科书算法。这里生成的是整个算法，而不是固定程序框架中的一个函数。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行评估与档案维护

外部评估器在统一环境和资源上运行每个候选算法，对每个返回结果检查可行性，并独立重新计算其目标成本；对有效算法计算训练目标 $J(a)=\frac{1}{m}\sum_{i=1}^{m}\operatorname{Cost}(a(x_i))$，然后将其插入有效算法档案 $\mathcal{A}\subseteq\mathcal{V}$。当前最优算法定义为 $a^*=\arg\min_{a\in\mathcal{A}}J(a)$，档案随后按算法源代码嵌入之间的距离组织。

<div class="method-step__io" markdown="1">

**输入**：候选完整算法、训练实例集和外部实验协议。<br>
**输出**：更新后的有效算法档案 $\mathcal{A}$、每个算法的训练成本、当前最优算法 $a^*$ 以及算法间的嵌入距离矩阵 $\mathbf{D}$。

</div>

**直观理解**：评估器像一个独立裁判：它不会替程序补漏洞，只判断程序自己返回的解是否合规，并重新算分。档案不仅保存最高分程序，也保存其他有效程序，避免搜索过早只剩下一条思路。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 嵌入空间聚类与代表选择

先以 $a^*$ 及其 $k$ 个最近邻构造精英区域 $\mathcal{G}^*$，供第一层搜索使用；再对完整档案执行自动选择聚类数 $K$ 的 $k$-medoids 聚类，得到由嵌入空间诱导的操作性语义区域。包含 $a^*$ 的聚类被整体移出，精英邻域中的其他成员也从剩余聚类中移除；空聚类被丢弃，被移除的代表由剩余成员中训练目标最优者替代，最终得到非精英聚类集合 $\Omega_t$ 及其数量 $R_t=|\Omega_t|$。

<div class="method-step__io" markdown="1">

**输入**：当前档案 $\mathcal{A}$、算法源代码的嵌入表示及距离矩阵 $\mathbf{D}$、当前最优算法 $a^*$。<br>
**输出**：精英区域 $\mathcal{G}^*$、非精英区域集合 $\Omega_t$、各区域代表及区域数 $R_t$，它们决定本轮各搜索层的参考算法和候选配额。

</div>

**直观理解**：嵌入表示把源代码转换为可比较的语义位置，距离近通常表示设计文本或策略相近；聚类则把档案划成若干搜索方向。论文强调这些区域只是由所选嵌入产生的操作分组，不能仅凭聚类断言它们一定对应真实的算法机制家族。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 三层搜索与迭代更新

第一层在 $a^*$ 及其邻域内进行重复单参考精炼，并执行局部 $Combine$；第二层对每个非精英代表进行单参考精炼，在成员足够时进行区域内 $Combine$；第三层进行跨区域发现，包括非精英代表之间的无锚点 $Combine$、$a^*$ 与非精英代表之间的质量锚定 $Combine$，以及同时参考非精英代表和 $a^*$、且要求远离参考区域的 $Diverge$。每轮重新计算聚类、精英成员和代表，因此当当前最优算法改变时，第一层会重新定位，第二、三层的名义候选数量随 $R_t$ 调整，并受剩余全局预算约束。

<div class="method-step__io" markdown="1">

**输入**：精英区域 $\mathcal{G}^*$、非精英区域集合 $\Omega_t$、各区域代表、当前最优算法 $a^*$ 以及预先固定的算子策略和全局预算。<br>
**输出**：新一轮候选算法；这些候选经过执行、可行性检查、独立成本计算和档案插入后，形成下一轮档案，直到达到实验协议规定的搜索预算。

</div>

**直观理解**：第一层负责把最好的方案打磨得更好，第二层给暂时落后的设计方向独立成长机会，第三层则像把不同方案的构造、改进和控制逻辑重新组合。每轮都重新观察档案，所以搜索资源会随当前保留下来的设计方向变化，而不是固定地把所有机会给同一个全局最优父代。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 训练集上的经验成本目标

$$
a_{\mathrm{opt}}=\arg\min_{a\in\mathcal{V}}\frac{1}{m}\sum_{i=1}^{m}\operatorname{Cost}\!\left(a(x_i)\right)
$$

**符号说明**

- $a_{\mathrm{opt}}$：希望找到的最优算法。
- $\mathcal{V}$：所有有效且可执行算法组成的集合。
- $m$：训练实例的数量。
- $x_i$：第 $i$ 个训练实例；原式中的数学符号在此定义为训练集成员。
- $a(x_i)$：算法 $a$ 在实例 $x_i$ 上返回的解，属于可行解空间 $\mathcal{S}$。
- $\operatorname{Cost}(a(x_i))$：对算法返回解独立计算的目标成本；论文针对最小化问题使用该成本作为质量信号。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标在所有有效算法中寻找训练实例平均成本最低者。它把算法合成转化为黑盒优化：每次提出一个程序，运行它得到解，再用平均成本反馈程序是否值得保留；测试实例只用于之后检验泛化，而不参与训练选择。<br>
**原文位置**：Section III-A 2, Problem Formulation, Eq. (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 档案当前最优算法的训练目标

$$
a^{*}=\arg\min_{a\in\mathcal{A}}J(a),\qquad J(a)=\frac{1}{m}\sum_{i=1}^{m}\operatorname{Cost}\!\left(a(x_i)\right)
$$

**符号说明**

- $a^{*}$：当前有效算法档案中的训练目标最优算法。
- $\mathcal{A}$：ATLAS当前维护的有效算法档案，满足 $\mathcal{A}\subseteq\mathcal{V}$。
- $J(a)$：算法 $a$ 在训练实例上的平均成本。
- $m$：训练实例数量。
- $x_i$：第 $i$ 个训练实例。
- $\operatorname{Cost}(a(x_i))$：算法在该实例上返回解的目标成本。

<div class="equation-explanation" markdown="1">

**直观理解**：第一式是在理论上对所有有效算法求解，通常无法直接穷举；第二式描述ATLAS在实际搜索中如何从已经发现的档案成员中选出当前锚点。这个锚点用于第一层精炼，也参与第三层的质量锚定合成，但其他区域代表仍被保留用于多样性和跨区域探索。<br>
**原文位置**：Section III-A 3, ATLAS Approach

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：ATLAS没有传统意义上通过梯度更新神经网络参数的训练过程；其训练阶段是以训练实例上的经验平均成本 $J(a)$ 为适应度信号的算法搜索。给定候选算法后，系统执行候选、检查返回解的可行性并重新计算成本；有效候选进入档案，当前最小 $J(a)$ 的成员成为 $a^*$，然后作为后续精炼或质量锚定合成的参考。$\n\n$优化变量是完整算法 $a$，而不是某个连续参数向量，因此搜索主要依靠大语言模型生成和语义编辑算子。档案机制使优化目标不再等同于只保留单一最低成本候选：系统还按嵌入空间保留多个区域，使当前训练较弱但结构不同的方案仍能获得搜索机会。论文将这种设计解释为应对两类风险：适应度压力过早集中到少数早期设计，以及资源分配不足导致有潜力的弱区域无法进一步精炼。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 完整算法合成与语义编辑算子**

ATLAS的候选对象是完整、可执行的算法源代码，而不是固定骨架中的组件。$Tune$主要保持整体结构并调整实现，$Improve$保持核心方法并改进其行为，$Combine$和$Diverge$允许多函数之间协调修改、重组交互关系或改变端到端工作流；参考型算子接收每个选定算法的完整源代码，包括辅助定义和函数调用。

> 直观理解：该模块决定模型能改什么：它可以修改一个局部细节，也可以把多个函数和流程一起重写，因此搜索范围覆盖整个算法设计，而不被预先规定的程序模板限制。不同编辑范围让系统既能做小修小补，也能产生真正不同的算法结构。

**2. 嵌入引导的有效算法档案**

系统维护 $\mathcal{A}\subseteq\mathcal{V}$，其中 $\mathcal{V}$ 是有效可执行算法集合；算法源代码由嵌入模型映射到向量空间，基于距离矩阵 $\mathbf{D}$ 进行近邻选择和自适应 $k$-medoids 聚类。档案的作用不是按单一训练得分只保留一个算法，而是保留多个嵌入空间区域及其代表，并用训练目标选择各区域中的优先成员。

> 直观理解：如果只保留当前最高分程序，早期偶然领先的思路可能垄断后续搜索；档案相当于保存多个候选路线。嵌入空间提供的是一种按代码语义相似性分组的办法，使系统能识别并继续探索不同路线。

**3. 三层搜索资源分配**

第一层以精英区域 $\mathcal{G}^*$ 为局部精炼对象；第二层仅处理从精英区域剔除后的非精英区域 $\Omega_t$，为每个代表提供区域内成熟化机会；第三层在多个区域之间执行无锚点合成、以 $a^*$ 为质量锚点的合成，以及以离开参考区域为目标的发散。每个迭代周期重新聚类，第三层的各合成流按 $R_t$ 安排候选并服从剩余全局预算。

> 直观理解：三层结构分别回答三个搜索问题：怎样继续提升目前最好方案、怎样避免较弱路线被忽略、怎样从不同路线中产生新组合。它与固定网格的质量多样性方法或拥有持久岛屿的进化方法动机相近，但这里使用一个全局档案和每轮重算的临时嵌入聚类。

**训练与推理**

训练或合成阶段首先固定问题规范、算法接口、训练实例和统一资源协议，用 $Create$ 生成初始候选，并用 $Diverge$ 相对于档案中的参考算法扩大初始覆盖。每轮将候选运行在训练实例上，由外部评估器验证可行性并计算平均成本；有效算法写入档案后，系统生成源代码嵌入距离矩阵，构造当前最优算法及其近邻的精英区域，并通过自适应 $k$-medoids 获得非精英区域和代表。$\n\n$随后按三层策略调用算子：第一层围绕精英区域做单参考精炼和局部合成；第二层分别成熟化非精英区域代表，并在条件满足时做区域内合成；第三层在不同区域代表之间进行多参考 $Combine$，包括不带最优锚点和带 $a^*$ 锚点的两类合成，同时进行带发散意图的 $Diverge$。新候选重复经历完整执行、可行性检查、独立目标计算和档案更新，直到达到全局资源预算。$\n\n$推理或部署阶段使用搜索得到的完整算法，在未参与合成选择的测试实例上运行，并由相同类型的外部评估器检查解的可行性和目标成本。论文给出的训练选择代表先依据训练目标和最终嵌入聚类确定身份，再报告测试表现，这一区分用于避免用测试结果反向选择代表；具体部署时采用哪个档案成员的选择规则，所给章节未进一步明确报告。

**复现信息**

为保证复现和公平比较，外部固定条件包括问题规范、最小算法接口、执行环境、资源限制和实验协议；这些条件约束算法的输入输出与运行预算，但不规定内部程序结构。给出的配置片段报告了最多维护 $50$ 个算法、使用自适应 $K$ 的 $k$-medoids、嵌入模型为 mGTE-large-en-v1.5、大语言模型为 GPT-5-mini，生成温度为 $T=1.0$，推理强度标记为 LOW；单参考算子中 $Combine$ 与 $Improve$ 的参考数或相关设置包括 $m_{\mathrm{comb}}=2$、$Tune$ 和 $Improve$ 的概率设置 $p=0.5$，$Diverge$ 的参考数为 $m_{\mathrm{div}}=3$，$Simplify$ 的概率为 $p=0.2$。所给节选没有完整呈现总预算、全部算子提示、失败路由规则、嵌入距离的具体定义、自动选择 $K$ 的细节或每轮各层的完整配额，因此这些内容不能仅据当前材料补充。可重复解读结果时，应特别注意：聚类是嵌入诱导的操作区域而非已证明的机制类别；四个示例算法的代码检查只能说明展示运行中出现了多函数协同设计，不能推出这种结构在全部档案中的比例或保证每个聚类具有功能互补性。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 路由基准包括容量约束车辆路径问题CVRP和带时间窗的CVRPTW：前者要求在车辆容量约束下最小化总行驶距离，后者进一步要求客户在指定时间窗内得到服务。默认规模均为50名客户。每个设置使用31个训练实例和31个独立测试实例，训练与测试生成种子分别为2024和42；搜索及档案构建只能访问训练集，训练阶段选出的算法随后在测试集上评估一次。
- 流水车间调度FSS：目标是在机器处理顺序固定的条件下安排作业，以最小化最大完工时间，即makespan。默认规模为50个作业、10台机器，同样采用31个训练实例和31个独立测试实例。它检验ATLAS是否能从路由之外迁移到具有不同解结构和目标函数的调度任务。
- 二次指派问题QAP：把设施分配到位置，使设施间流量与位置间距离共同决定的总成本最小。默认规模为50个设施，采用31个训练实例和31个独立测试实例。该任务用于检验完整算法合成在高耦合指派成本结构下是否仍然有效。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**相对平均差距**

各方法测试目标均值相对于该设置中经统计规则选出的人工领域参考方法均值的百分比差距。参考方法的差距定义为0.000%；该指标便于跨问题比较，但表中差距只是描述性汇总，不能替代基于逐实例原始目标值的显著性检验。 （越低越好，因为四个问题都以最小化为目标；接近0%表示平均性能接近人工参考，负值若出现则表示均值优于该参考。）

</div>
<div class="metric-item" markdown="1">

**配对Wilcoxon符号秩检验**

在相同测试实例上比较两种方法的原始目标值差异，用非参数检验判断性能差异是否具有统计显著性。表中粗体统计最优组包含最低均值方法，以及与其差异不显著的方法。 （没有单调的“越高越好”方向；应结合原始目标均值和显著性结论解释。未检出显著差异只表示现有样本不足以确认差异，不等于证明两种方法完全等价。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四个默认基准设置：ATLAS对全部LLM基线

<div class="result-value" markdown="1">

作者报告，基于逐实例原始目标值的配对Wilcoxon分析显示，ATLAS在FSS、CVRP、CVRPTW和QAP四个默认设置上均统计显著优于每个LLM基线。

</div>

这表示ATLAS的优势并非只来自某一个问题类别，也不只是相对平均差距表中的微小显示误差。不过，该结论来自每种LLM方法仅$R=5$次独立合成运行，且使用同一GPT-5-mini后端；它不能直接推出换用其他模型、预算或实例分布后仍会保持同样优势。

<div class="result-source" markdown="1">

来源：第IV-B1节，表II

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The paired Wilcoxon analysis shows that ATLAS statistically outperforms every LLM-based baseline across all four default benchmark settings (Table II).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### ATLAS相对于各任务最佳人工领域参考方法

<div class="result-value" markdown="1">

ATLAS的相对平均差距分别为FSS 0.347%、CVRP 0.094%、CVRPTW 0.000%和QAP 0.460%，即四个默认设置均不超过0.46%。

</div>

从工程效果看，自动合成的算法平均目标值已接近强人工方法，且覆盖路由、调度和指派三种结构。但0.000%仅表示在报告精度下均值相同，其他小差距也只是描述性结果；除论文明确给出的统计比较外，不能据此声称ATLAS与所有人工方法统计等价。

<div class="result-source" markdown="1">

来源：第IV-B1节，表II

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Its relative mean gaps to the best such reference are 0.347% on FSS, 0.094% on CVRP, 0.000% on CVRPTW, and 0.460% on QAP.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### CVRP与CVRPTW上的人工参考比较

<div class="result-value" markdown="1">

在CVRP上，ATLAS与选定人工参考PyVRP之间未发现统计显著差异；在CVRPTW上，ATLAS以表格显示精度匹配最低报告均值。

</div>

CVRP结果说明在31个测试实例及当前检验功效下，没有足够证据区分ATLAS与PyVRP，但“不显著”不等于证明两者等价。CVRPTW的0.000%则只是舍入后均值匹配，作者明确指出统计检验使用未舍入的配对原始目标，因此不能把显示精度上的并列扩大解释为严格相同。

<div class="result-source" markdown="1">

来源：第IV-B1节，表II

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On CVRP, the paired Wilcoxon test finds no statistically significant difference between ATLAS and PyVRP, the selected human-designed reference.

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

- 人工设计的领域专用方法：路由任务采用PyVRP、Google OR-Tools和VROOM，FSS采用NEH、IG-TB和Iterative Beam Search，QAP采用RoTS、Simulated Annealing、BLS和BMA。它们代表经过领域知识设计和长期调优的强参考点，用于判断自动合成算法是否具有实际竞争力；对运行时间敏感的方法接受与具体基准设置对应的单实例时间上限。
- EoH、ReEvo与MCTS-AHD：三者均在基于LLM4AD的共享贪心构造脚手架和统一基准接口中运行，并使用相同LLM后端及匹配的token预算。该组比较检验ATLAS相对于固定组件接口搜索的总体优势，但由于完整算法表示、操作算子和支持机制同时发生变化，不能单独归因于“去脚手架”。
- EoH-Full：作者把EoH的进化框架改造成完整算法合成方法，使其共享ATLAS的问题与接口感知算子、修复流程和评估框架，同时保留EoH的适应度驱动选择。EoH-Full与组件版EoH的比较衡量从固定组件到完整算法合成及其配套机制的综合作用。
- ATLAS与EoH-Full的匹配比较：两者共享完整算法表示、生成算子、修复机制、评估器、LLM和预算，主要差别是ATLAS采用基于档案、嵌入引导的质量多样性搜索，而EoH-Full采用标准适应度驱动选择。因此该比较最接近对ATLAS核心搜索机制的受控检验。

**实验想回答的问题**

- 在四类组合优化问题上，ATLAS自动合成的完整算法能否优于使用固定贪心构造脚手架的LLM算法设计方法，并达到接近人工领域算法的测试性能？
- 在匹配LLM、生成预算、完整算法表示、算子、修复机制和评估器后，ATLAS的嵌入引导质量多样性搜索是否比标准的适应度驱动进化更有效？

**实验实现**

所有LLM方法均使用OpenAI GPT-5-mini，reasoning effort设为low，温度为$T=1.0$；ATLAS端到端组件消融和搜索配置敏感性分析采用$B=500$次已评估算子执行。每种LLM方法进行$R=5$次独立合成运行，每次使用不同随机种子并产生一个按训练性能选出的算法，因此五次运行可能得到不同代码。作者说明五次重复主要受LLM API和候选算法反复执行成本限制。默认ATLAS单次合成约消耗500次算子调用和500万至700万token，估计API费用为4.2至5.8美元，典型耗时约10至15小时。

实验运行于WSL2 Ubuntu 22.04、Python 3.12、AMD Ryzen 9 7950X、64 GB内存和RTX 5090环境。候选算法对每个实例使用一个工作进程和一个线程，不同实例可以并行；人工领域方法也尽可能遵循相同的单实例执行模型和运行时间上限。训练集负责搜索、档案构建和算法选择，测试集仅用于最终评估，这一设计降低了直接对测试实例调参的风险。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 组件式EoH与EoH-Full的表示及配套机制对照 | 作者报告EoH-Full相较组件式LLM实现有显著改善，但所给节选未提供该改善的具体数值。 | 这一对照测试从共享贪心组件接口转向完整算法产物，并同时加入问题与接口感知算子、修复和评估框架后的综合效果。由于多个设计共同改变，它是端到端设计消融，而不是对“scaffold-free”单因素的严格隔离。 | 第IV-B1节，表II；具体数值在所给节选中未完整呈现<br><span class="experiment-evidence">The full-synthesis baseline EoH-Full substantially improves over the component-based implementations.</span> |
| EoH-Full与ATLAS的搜索机制对照 | 在匹配完整合成算子、修复、评估器、LLM和预算后，作者报告ATLAS仍优于EoH-Full；所给节选未提供差距或显著性数值。 | 该对照主要隔离档案式嵌入引导质量多样性搜索与适应度驱动进化的差别。作者的机制解释是：适应度选择可能过早集中于少数高分区域，而ATLAS保留多个嵌入区域、并行改进并进行跨聚类合成。实验支持整套搜索机制有效，但没有单独证明档案、嵌入或跨聚类操作中哪一项最关键。 | 第IV-B1节，表II<br><span class="experiment-evidence">Because EoH-Full and ATLAS share the full-synthesis operators, repair, evaluator, LLM, and budgets, ATLAS’s remaining advantage over EoH-Full more directly supports the contribution of its archive-based embedding-guided quality-diversity search.</span> |

**定性案例**

- 作者在代码仓库中提供了ATLAS为FSS、CVRP、CVRPTW和QAP分别生成的最佳算法及其说明，可用于检查LLM究竟合成了怎样的完整求解逻辑。不过，所给章节没有展示这些算法的代码结构、运行轨迹或失败案例，因此这里只能把它们视为可审查的定性产物，不能据此判断算法的新颖性、可解释性或对具体机制的依赖。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Uses LLMs with embedding-guided quality-diversity search to synthesize algorithms without predefined scaffolds.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`dd4d966bafb7433b59ace0139f2e77da12cf82a17b60ffcf7dbb5c0ba56563c2`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
