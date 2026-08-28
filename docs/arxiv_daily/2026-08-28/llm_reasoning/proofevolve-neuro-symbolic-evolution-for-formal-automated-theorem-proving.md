---
title: "[论文解读] ProofEvolve: Neuro-Symbolic Evolution for Formal Automated Theorem Proving"
description: "[arXiv 2608.26334][LLM Reasoning] ProofEvolve旨在让神经定理证明器不只追求一次性完成整条证明，而是持续保存、验证并跨问题复用部分证明所产生的可靠知识。"
arxiv_id: "2608.26334"
announcement_date: "2026-08-28"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:38:38.798609+00:00"
source_sha256: "de66a005e636bd91af142fa6f08e6413cb8811f4c32f73d876d0615a0d3c3474"
tags:
  - "LLM Reasoning"
  - "形式自动定理证明"
  - "Lean 4"
  - "神经—符号方法"
  - "AND-OR 证明 DAG"
  - "内核验证"
  - "可复用子证明"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.26334</p>

# ProofEvolve: Neuro-Symbolic Evolution for Formal Automated Theorem Proving

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Wenqian Ye, Ziwei Guan, Eric Xie, Bohan Liu, Shivani Modi, Buyun Zhang, Ellie Dingqiao Wen, Henry Kautz, Aidong Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of Virginia；Affiliation: Meta AI</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26334v1) · [PDF 下载](https://arxiv.org/pdf/2608.26334v1) · **关键词** 形式自动定理证明, Lean 4, 神经—符号方法, AND-OR 证明 DAG, 内核验证, 可复用子证明<br>


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

ProofEvolve旨在让神经定理证明器不只追求一次性完成整条证明，而是持续保存、验证并跨问题复用部分证明所产生的可靠知识。

**不用术语来说**：现有证明系统即使没有完成目标定理，也可能已经证明了若干有用的中间结论；但这些成果往往随本次搜索结束而丢失，或必须经过昂贵的模型再训练才能影响后续任务。作者希望构建一种会“积累经验”的证明器：只要某段推理通过 Lean 内核检查，就把它作为可复用知识保留下来，使失败尝试也能帮助以后解决新问题，同时不牺牲形式证明的正确性保证。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出以显式、经 Lean 验证的符号证明结构作为持续进化对象：在单个问题内保存结构多样的部分 AND-OR 证明 DAG，并将已闭合的子 DAG 提取为可跨问题继承的定理模式库。
- 作者提出以“验证闭包”衡量部分证明的渐进进展，并通过带类型的模式重组把既有证明结果实例化到新目标上；未满足的前提会显式转化为新子目标，所有变化仍须由 Lean 内核复核。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

形式自动定理证明把待证命题及其证明写入形式语言，并由证明助理的内核逐步检查，因此不同于仅生成自然语言论证：系统输出必须能在固定的 Lean 4 与 Mathlib 环境中通过类型检查。本文关注神经—符号证明系统，其中语言模型负责提出可能的证明步骤，Lean 内核负责判定这些步骤是否正确；搜索对象不是单段完整证明文本，而是由目标、子目标和已验证推导组成的 AND-OR 有向无环图。该设置的重要性质是：即使根命题尚未证明，图中已经闭合的子图仍对应有效的 Lean 证明项，因而可作为显式知识保留并在后续搜索中复用。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**Lean 4 内核验证**

Lean 将命题表示为类型、将证明表示为该类型的项；只有在给定环境与局部上下文中成功展开且不含未解决占位符的证明项，才会被内核接受。神经模型只负责提出候选，不能绕过这一检查，因此候选可能错误，但最终接纳的结果保持形式可靠性。

</div>
<div class="concept-item" markdown="1">

**战术状态与子目标**

战术状态写作 $s=(\Gamma\vdash g)$，表示在局部假设与变量上下文 $\Gamma$ 下需要证明目标 $g$。一个证明步骤可以关闭该目标，也可以把它分解成若干必须全部解决的子目标。

</div>
<div class="concept-item" markdown="1">

**AND-OR 证明 DAG**

DAG 是不含环的有向图；同一目标可有多种备选证明步骤，形成 OR 关系，而某一步生成的全部子目标必须同时完成，形成 AND 关系。共享节点允许不同证明分支复用同一中间结论，且无环性保证可从闭合叶节点递归组装完整证明。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是在固定 Lean 4 环境 $\mathcal{E}$ 中良构的目标命题 $T$，其中环境导入匹配版本的 Mathlib；目标根节点为 $r=(\Gamma_0\vdash T)$，通常要求封闭命题满足空上下文下的内核良构性。系统搜索一个有限、无环的证明图 $D=(V,E,r)$：节点是战术状态，超边表示已由 Lean elaborator 与内核接纳的证明构造器，可将所有子目标的证明组合为父目标的证明。若某节点存在一条已验证出边，且该边的所有子节点都已闭合，则该节点闭合；零子节点的出边直接提供关闭证明。最终输出是根目标的内核可检查证明项；即使根尚未闭合，任意闭合内部子图也能递归组装为其根节点的有类型证明，构成可保留、可复用的中间结果。本文据此将自动证明设定为对显式验证结构的累积搜索，而不是只对完整证明文本做一次性成功或失败判定。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{E};\Gamma\vdash_{\mathcal{K}}p:g$**

证明项 $p$ 在环境 $\mathcal{E}$ 和局部上下文 $\Gamma$ 中展开成功、无未解决元变量或占位符，并被 Lean 内核 $\mathcal{K}$ 接受为目标 $g$ 的证明。

</div>
<div class="notation-item" markdown="1">

**$\mathsf{Prf}_{\mathcal{E}}(s)$**

战术状态 $s$ 在环境 $\mathcal{E}$ 中所有经内核检查的证明见证所组成的集合。

</div>
<div class="notation-item" markdown="1">

**$D=(V,E,r)$**

有限无环的 AND-OR 证明 DAG，其中 $V$ 是战术状态节点集，$E$ 是经验证的证明超边集，$r$ 是待证目标对应的根节点。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{Closed}_{D}(s)$**

节点 $s$ 在图 $D$ 中已经闭合：存在一条从 $s$ 出发的已接纳证明边，并且该边的全部子节点均已闭合。

</div>

</div>

**直接相关的工作**

- **LEAP（Kung et al., 2026）**: 与本文最接近的证明 DAG 方法：它能在同一目标的不同搜索分支之间共享中间引理，但原文指出其记忆仍绑定于当前目标，未把已验证子结构持久化并跨问题继承。
- **Lean 4（de Moura and Ullrich, 2021）**: 本文采用的形式验证基础设施；Lean 的 elaborator 与可信内核检查每条证明转换，使神经模型提出的候选只有在类型正确且无未解决占位符时才能进入证明图。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

形式化定理证明能够为数学与科学推理提供机器可检查的正确性保证，而且一项证明通常还会产生可复用引理、隐藏结构和新假设。若自动证明器能够长期积累这些结果，后续问题便可建立在先前已验证的知识之上；然而当前系统对未完成证明中的有效进展利用不足，难以形成真正的递归式自我改进。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于训练的神经定理证明器**：系统通过训练或微调把证明经验编码进神经模型参数，再由更新后的模型生成后续证明。新知识通常只有经过下一轮权重更新，才会稳定影响其他问题。
- **推理时智能体与问题内证明 DAG 方法**：多智能体或类似 LEAP 的系统在求解当前目标时进行子目标分解、分支协作，并可在同一证明 DAG 的不同分支之间共享中间引理，但其工作记忆主要绑定于当前目标。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 参数化学习需要额外且昂贵的训练周期，导致新近得到的证明结果无法立即成为后续问题可直接调用的显式知识，持续积累的速度和可追踪性因此受限。
- 问题内智能体通常以根定理是否最终完成作为主要反馈，跨问题保存能力有限；一段文本发生很小的错误就可能使完整证明失效，即便其中大部分子推理已经正确，因此稀疏的整证明成败信号会浪费失败尝试中的已验证成果。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有方法缺少一种统一机制，能够把部分与完整证明中的内核已验证结构作为独立知识单元长期保存，在不同目标之间安全继承和重组，并对尚未完成的候选提供细粒度、可验证的进展评价。

</div>
<div markdown="1"><span>核心问题</span>

能否让神经模型负责提出证明结构的变化方向、让 Lean 内核逐步裁决其正确性，并通过持久化的证明 DAG 与定理模式库，使一次搜索中获得的可靠局部成果立即扩大以后证明任务的可达搜索空间？

</div>
<div markdown="1"><span>作者直觉</span>

完整证明文本很脆弱，但其中通过内核检查的子证明是稳定资产。将证明表示为可拆分的图结构后，系统可以像保留“已完成零件”一样保存闭合子图，并优先扩展已经取得较多验证进展且结构各异的候选；面对新目标时，再按类型匹配复用这些零件，把尚缺的条件明确列为子目标。这样，神经模型的探索能力与符号内核的严格验证相互分工，失败搜索也能留下可继承成果。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ProofEvolve把自动定理证明表示为对显式、可验证证明结构的持续进化，而不是要求神经模型一次生成完整证明。输入是在固定 Lean 4 环境 $\mathcal{E}$ 中的目标命题 $T$、神经策略 $\pi$、Mathlib 前提、目标内证明档案 $\mathcal{M}_T$、跨目标模式库 $\mathcal{L}$ 与错误库 $\mathcal{H}$；系统反复选择一个部分证明 DAG，在其开放前沿提出分解、模式重组或修复操作。每次操作都必须经 Lean 内核 $\mathcal{K}$ 检查，接受后才扩展 DAG、提取可复用结果并更新档案；当根节点闭合时，系统递归组装并再次核验完整证明项，输出 Lean 接受的 $T$ 的证明。

其关键区别是：失败尝试不再被整体视为零收益。AND-OR DAG 中，一个超边的全部子目标都要完成，表示“AND”；同一状态的多条候选边只需有一条成功，表示“OR”。因此，即使根目标尚未解决，已经闭合的内部子图仍是有类型、经内核验证的局部定理，可以参与当前搜索，并在抽象为模式后供后续目标使用。通俗地说，模型负责提出“下一步怎么改”，Lean 负责逐步验收；系统像维护一个可审计的解题工程图，把每块已经验收的零件留下，而不是整题失败就全部丢弃。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始化目标与选择候选证明

若 $\mathcal{M}_T$ 为空，则插入仅含根状态 $r=(\Gamma_0\vdash T)$ 的 DAG；否则按由验证闭合度 $\rho(D)$ 和温度 $\tau$ 决定的软最大分布，从档案已占用的行为单元中采样父 DAG $D$。

<div class="method-step__io" markdown="1">

**输入**：目标队列 $\mathcal{Q}$、目标 $T$ 的档案 $\mathcal{M}_T$，以及当前模式库 $\mathcal{L}$。<br>
**输出**：一个有限、无环且此前所有边均已通过 Lean 检查的父证明 DAG $D$。

</div>

**直观理解**：系统不会只沿当前最好的一条路线搜索，而会从多种结构不同的部分解中抽取下一位“父代”。这样既偏向已取得较多可靠进展的路线，也避免过早放弃其他证明策略。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 确定前沿子目标并检索上下文

对每个前沿状态 $s$，反事实地把它视为已闭合，并计算这会使根闭合度增加多少；选择增益 $\Delta_D(s)$ 最大者。随后检索与 $s$ 相关的 Mathlib 前提和已验证模式，形成神经策略可用的上下文。

<div class="method-step__io" markdown="1">

**输入**：父 DAG $D$、其未闭合且没有出边的前沿集合 $\mathrm{frontier}(D)$、Mathlib 与模式库 $\mathcal{L}$。<br>
**输出**：优先处理的状态 $s$，以及相应的库定理、模式候选和已有错误信息。

</div>

**直观理解**：系统优先解决对全局证明最有帮助的缺口，而不是简单选择最浅或最早出现的目标。检索则像先把可能用到的教材结论和以前验证过的解题片段放到模型面前。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 神经提出结构变异并由内核验收

若存在同一状态上的拒绝记录，策略提出修复；否则提出分解或模式重组。提案 $\delta$ 只有在 Lean 接受其诱导的带类型超边，且所得 $D'$ 是 $D$ 的有限无环扩展时才被接受；所有未解决占位符必须显式变成子目标。

<div class="method-step__io" markdown="1">

**输入**：状态 $s$、DAG $D$、检索上下文、策略 $\pi$，以及键为 $(T,D,s)$ 的错误记录 $\mathcal{H}(T,D,s)$。<br>
**输出**：成功时得到携带已检查证明构造器的扩展 DAG $D'$；失败时得到 $\bot$，并把提案和 Lean 错误写入 $\mathcal{H}$。

</div>

**直观理解**：语言模型可以猜步骤，但不能直接改写受信证明状态；Lean 像编译器兼裁判，只有完全类型正确的改动才能进入档案。错误也不会白费，而会成为下一轮定点修复的反馈。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 积累知识、更新多样性档案并输出证明

系统从新闭合的子 DAG 中抽取经内核检查、显式量化局部变量并暴露所用假设的可复用模式，加入持久库 $\mathcal{L}$；同时，每个行为描述单元至多保留一个 DAG，并仅以闭合度更高的挑战者替换 incumbent。若 $\rho(D')=1$，则沿见证边递归组装根证明 $\mathrm{Asm}_{D'}(r)$，并要求 Lean 再次确认其类型为 $T$。

<div class="method-step__io" markdown="1">

**输入**：内核接受的扩展 $D'$、旧 DAG $D$、行为描述符 $b(D')$、模式库 $\mathcal{L}$ 与档案 $\mathcal{M}_T$。<br>
**输出**：更新后的跨目标模式库、目标内多样化档案，或最终经内核验证的 Lean 证明项 $\mathrm{Asm}_{D'}(r)$。

</div>

**直观理解**：目标内档案保存不同风格中进展最好的部分证明，目标间模式库则保存已经验收的通用零件。只有根目标真正闭合且组装后的完整证明再次通过 Lean 时，系统才宣布求解成功。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 内核约束的证明 DAG 转移

$$
\mathrm{step}_{\mathcal{K}}(D,\delta)=\begin{cases}D',&\text{if Lean accepts the induced edge and }D'\text{ is an acyclic extension of }D,\\ \bot,&\text{otherwise}.\end{cases}
$$

**符号说明**

- $\mathcal{K}$：Lean 的可信内核，用于检查证明项与类型。
- $D$：变异前的有限无环 AND-OR 证明 DAG。
- $\delta$：神经策略提出的分解、模式重组或修复编辑。
- $D'$：保留原节点、原边及其实现器，并增加一条已检查边后的无环扩展。
- $\bot$：提案被拒绝；受信档案和模式库不发生相应证明状态更新。

<div class="equation-explanation" markdown="1">

**直观理解**：该式划定神经组件与符号组件的信任边界：模型只能提出候选编辑，不能自行宣告证明步骤有效。任何产生类型错误、遗留隐式洞或造成环路的编辑都不会进入受信状态，因此后续搜索只能建立在 Lean 已验收的结构上。<br>
**原文位置**：第 4.2 节，公式 (7)

</div>

</div>

<div class="equation-block" markdown="1">

#### 验证闭合度递归

$$
\rho_D(e)=\sum_{s'\in\mathrm{ch}(e)}w_e(s')\rho_D(s'),\qquad \rho_D(s)=\begin{cases}1,&\mathrm{Closed}_D(s),\\0,&\mathrm{out}_D(s)=\varnothing,\\\max_{e\in\mathrm{out}_D(s)}\rho_D(e),&\text{otherwise},\end{cases}\qquad \rho(D)=\rho_D(r)
$$

**符号说明**

- $\rho_D(e)$：超边的验证进度值，由其全部子目标的状态值聚合得到。
- $\rho_D(s)$：状态在 DAG 中的验证闭合度。
- $\mathrm{ch}(e)$：超边所产生的全部子状态；它们是必须同时完成的义务。
- $w_e(s')$：子状态的正权重，满足对同一非空子集合的权重和为 $1$；论文采用均匀权重。
- $\mathrm{out}_D(s)$：从状态出发且已被 Lean 接受的候选证明边集合。
- $\mathrm{Closed}_D(s)$：存在一条出边，使其所有子状态均闭合；零子节点的已检查边也可直接使状态闭合。
- $r$：证明 DAG 的根状态，即原始目标。
- $\rho(D)$：根状态的闭合度，作为候选 DAG 的选择适应度。

<div class="equation-explanation" markdown="1">

**直观理解**：单条证明路线要求其全部子目标完成，因此对孩子做加权聚合；同一状态的多种路线只需最佳者成功，因此取最大值。该量完全由内核接受的图结构计算，扩展 DAG 时不会下降，并满足 $\rho(D)=1$ 当且仅当根已闭合，所以它既能区分未完成尝试，又不把部分分数误当作完整证明。<br>
**原文位置**：第 4.2 节，公式 (8)–(10)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文所给方法不是通过反向传播训练一个新的证明模型，也未定义参数学习损失；其优化对象是推理期的显式证明结构。搜索以验证闭合度 $\rho(D)$ 作为进化适应度：档案单元只接受闭合度严格更高的同类 DAG，父代采样偏向高 $\rho(D)$ 候选，前沿调度则最大化反事实根增益 $\Delta_D(s)$。因此这里的“进化”是对经 Lean 验证的符号 DAG 和持久模式库进行选择、变异与继承，而不是把证明经验通过昂贵权重更新写入 $\pi$；策略 $\pi$ 的预训练或微调目标在所提供章节中未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Lean 内核约束的 AND-OR 证明 DAG**

每个节点是策略状态 $s=(\Gamma\vdash g)$；一条超边 $e=(s;s_1,\ldots,s_k)$ 携带经检查的实现器 $F_e$，可把所有子状态的证明组合成源状态的证明。零子节点边是直接闭合证明，多条出边表示替代方案；DAG 的无环性保证闭合判定与证明组装递归良定义。

> 直观理解：该结构同时记录“可以任选一种办法”和“一种办法产生的所有子任务都必须完成”。边中保存的不是自然语言理由，而是 Lean 已接受的证明构造器，因此闭合子图即使不连接到完整根证明，也已经是可靠成果。

**2. 验证闭合度与行为索引档案**

闭合节点取值 $1$，尚无出边的开放节点取值 $0$；AND 超边对孩子值作正权加权平均，OR 节点在候选边中取最大值，从而得到 $\rho(D)\in[0,1]$。档案以离散描述符 $b(D)$ 区分深度、主导 tactic 家族和使用的模式索引区域，每个单元只保留闭合度最高者，再以 $\rho(D)$ 的温度软最大分布选择父代。

> 直观理解：它把完整证明的二元成功信号变成来自已验证结构的连续进度，但不会把未经验证的模型信心算作进展。行为分格避免所有计算资源都集中到一种看似领先、实际可能走不通的证明套路上。

**3. 跨目标模式继承与错误驱动修复**

新闭合子 DAG 可被抽象为模式：自由局部变量被量化，实际依赖的假设成为显式前提，并以经内核检查的证明项随模式存入持久库 $\mathcal{L}$。应用模式时仍由 Lean 检查类型匹配，尚不能满足的前提被暴露为新子目标；被拒提案及 Lean 错误则按 $(T,D,s)$ 存入 $\mathcal{H}$，供策略提出修复。

> 直观理解：模式继承不是复制一段可能不适用的文本，而是把已经证明的局部结论封装成带输入条件的定理模板；缺少的条件不会被隐藏，而会变成必须继续证明的任务。错误库则让模型针对具体类型错误修改上一提案，而非从头盲猜。

**训练与推理**

该流程属于推理期搜索。系统在固定 Lean 4 与匹配 Mathlib 环境中依次处理目标：初始化根 DAG，按闭合度采样父代，选择潜在根增益最大的前沿状态，检索 Mathlib 前提和模式，然后让 $\pi$ 提出分解、重组或基于 Lean 错误的修复。提案经 $\mathrm{step}_{\mathcal{K}}$ 验收；失败时仅记录编辑和错误，受信投影 $\Sigma$ 不变，成功时则提取新模式并按行为单元更新档案。

迭代持续到预算耗尽或根闭合。根闭合后，系统根据每个闭合状态选定的见证边，自叶向根调用边实现器，构造 $\mathrm{Asm}_{D'}(r)$；仅当 Lean 证明 $\mathcal{E};\Gamma_0\vdash_{\mathcal{K}}\mathrm{Asm}_{D'}(r):T$ 时才返回结果。跨目标运行时，$\mathcal{M}_T$ 只服务当前目标，而 $\mathcal{L}$ 持续保留先前目标中抽取的已验证模式，从而实现不修改模型权重的知识积累。

**复现信息**

公平复现所必需的约束是使用固定 Lean 4 环境 $\mathcal{E}$ 和匹配版本的 Mathlib，并要求证明项无未解析元变量或占位符；所有接受边必须携带 Lean 已检查的实现器，且扩展后仍为有限无环 DAG。闭合度对子目标采用均匀正权重，档案描述符由分箱深度、主导 tactic 家族和使用的模式索引区域组成，每个描述单元最多保存一个 DAG，分数相同时保留原候选。

父代通过闭合度温度软最大分布采样，前沿状态按 $\Delta_D(s)$ 最大化选择；具体温度 $\tau$、档案分箱边界、检索器配置、搜索预算、并行方式和神经模型解码参数在所提供节选中未明确报告。模式抽取与重组的完整形式化规则在节选中被截断，因此只能确认其要求内核检查、显式处理局部变量与使用过的假设，并把未满足前提暴露为新子目标，不能据此补造更具体的匹配算法。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- PutnamBench 的纯证明子集：来源于 William Lowell Putnam 数学竞赛；排除定理陈述中已经含有固定答案值的问题，用于检验系统处理高难度、答案不能直接从陈述读取的形式化证明能力。原文节选未给出该子集的题目总数。
- IMO-LeanProofBench：包含国际数学奥林匹克水平问题的 Lean 形式化。主实验评估总体解题率；消融实验使用其中 $60$ 题，并划分为 $30$ 题 Basic 与 $30$ 题 Advanced，以比较组件对不同难度问题的作用。
- CombiBench：覆盖竞赛级组合数学，证明通常依赖显式构造或计数。它用于检验 ProofEvolve 在结构较专门的组合推理任务上是否仍有优势，而不是只在适合多引理分解的问题上有效。跨问题复用实验另使用合成组合引理族及 Lean Workbook：后者经复核与去重后保留 $10{,}968$ 个不同定理，其中 $1{,}000$ 个留作评估、$9{,}968$ 个作为证明库来源流；泄漏筛查后实际报告 $744$ 个评估定理。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Lean 核验证解题率**

基准中最终证明与目标匹配、无未解决元变量或占位符，并通过 Lean 4 内核验证的定理比例；所有解答还接受受限的 `#print axioms` 检查，且排除依赖 `native_decide` 的证明。 （越高越好，因为它直接表示在不放宽形式可靠性的前提下成功证明的目标比例。）

</div>
<div class="metric-item" markdown="1">

**验证闭包 $\rho$**

依据 Lean 内核已接受的证明 DAG 边计算的搜索适应度；它记录已被验证的中间子目标进展，根目标完全闭合时 $\rho=1$，失败搜索通常停在小于 $1$ 的值。 （越高越好；逐步上升表示更多中间证明结构已经得到形式验证，但只有达到 $1$ 才代表整条根定理被解决。）

</div>
<div class="metric-item" markdown="1">

**相对零样本的解题率提升**

加入相关已验证证明检索后，相对于不提供证明库上下文的 zero-shot 条件所增加的解题率百分点；实验还用同库随机检索控制单纯增加上下文示例的影响。 （越高越好，因为正值表示证明库提供了额外帮助；只有明显超过随机检索时，才支持收益来自相关证明结构而非更长提示。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三个竞赛级 Lean 基准上的统一基础模型与匹配预算比较

<div class="result-value" markdown="1">

ProofEvolve 的三基准平均解题率为 $57.8\%$，高于 LEAP 的 $50.5\%$ 和 Hilbert 的 $45.9\%$。分数据集看，它在 PutnamBench 达到 $71.2\%$，比 LEAP 高 $6.5$ 个百分点；在 IMO-LeanProofBench 达到 $53.3\%$，而 LEAP 为 $36.7\%$。在 CombiBench 上 ProofEvolve 为 $49.0\%$，略低于 LEAP 的 $50.0\%$。

</div>

作者据此主张 ProofEvolve 在所评估系统中取得最高平均解题率，且最大优势出现在通常需要组合多个引理的 IMO-LeanProofBench，这与分解、分级选择和模式复用的设计目标一致。分析上，这说明结构化演化搜索比同模型的直接采样及若干匹配预算的智能体搜索更有效；但它并不证明 ProofEvolve 在每一类数学问题上都占优，因为 CombiBench 上 LEAP 仍领先 $1.0$ 个百分点，也不能由该结果单独区分各内部组件的贡献。

<div class="result-source" markdown="1">

来源：第 5.2 节，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ProofEvolve has the highest average solve rate at 57.8%, ahead of LEAP (50.5%) and Hilbert (45.9%). It leads PutnamBench at 71.2%, 6.5 points above LEAP, and widens the margin on IMO-LeanProofBench, reaching 53.3% against 36.7% for LEAP. On CombiBench the strongest systems are within one point, LEAP at 50.0% and ProofEvolve at 49.0%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 具有已知依赖关系的合成组合引理族：跨目标增长证明库与每题前重置证明库

<div class="result-value" markdown="1">

在其他组件保持不变时，增长证明库的解题率为 $19.8\%$，重置证明库时为 $7.3\%$；前者解决的目标数约为后者的 $2.7$ 倍。

</div>

这一受控实验专门测试“较早目标的已验证引理能否帮助较晚目标”，因依赖结构由构造保证，所以比自然基准更容易隔离知识继承机制。结果支持持久证明库确实能产生跨问题收益；但合成家族可能比真实数学问题具有更清晰、更密集的可复用结构，因此 $2.7$ 倍不能直接外推到一般竞赛定理。

<div class="result-source" markdown="1">

来源：第 5.6 节，Controlled compositional families

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ProofEvolve solves 19.8% of the targets when the library grows across targets and 7.3% when the library is reset before each target. The growing library therefore solves 2.7× as many targets, with every other component held fixed.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Lean Workbook 未见定理上的真实跨问题复用：相关检索、零样本与同库随机检索

<div class="result-value" markdown="1">

在筛查后的 $744$ 个评估定理上，当检索深度为 $K=8$ 时，相关证明检索将解题率从 $49.5\%$ 提升到 $53.4\%$，增加 $3.9$ 个百分点；同一证明库的随机检索仅达到 $49.6\%$。仅使用 $1{,}000$ 个库证明时已提升 $3.3$ 个百分点，而 $K=64$ 时提升达到 $5.3$ 个百分点。

</div>

相关检索显著优于随机检索，说明收益主要来自选中可迁移的已验证证明结构，而不是仅向提示中加入更多示例。作者还报告多数新增成功并非逐字复制展示的证明，进一步支持结构复用解释。不过该实验刻意关闭 DAG 归档、分解、修复和验证闭包选择，只允许一次完整证明尝试，因此它测量的是证明库作为上下文示例的独立贡献，而不是完整 ProofEvolve 流程的端到端增益。

<div class="result-source" markdown="1">

来源：第 5.6 节，Figure 9 与 Table 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At K=8 the library raises the solve rate from 49.5% to 53.4%, a gain of 3.9 points, while random retrieval from the same library reaches 49.6%: the improvement comes from selecting useful verified work, not from adding examples to the prompt. A library of only 1,000 proofs already adds 3.3 points, and the gain reaches 5.3 points at K=64.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 计算成本和可复现性压力较大：最大实验并发使用 224 张 NVIDIA B200 GPU，专有模型还依赖 API。论文说明预算已匹配，但节选未给出 Table 1 各系统的完整调用量、token、时延和经济成本，因此无法仅凭解题率判断效率优势。
- 外部有效性与复用泄漏仍需谨慎：主结果只覆盖三个竞赛级 Lean 基准；真实复用实验虽经五个模型评审筛除疑似近重复项，并以随机检索作对照，但最终只保留 $744$ 个评估定理，且检索实验关闭了完整 ProofEvolve 搜索组件。因而它支持“相关已验证证明可帮助一次性生成”，尚不足以单独证明完整跨问题演化机制在更广泛数学领域中的收益。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Claude Opus 4.8 的 pass@$16$ 直接采样：不进行智能体式搜索，用来判断仅增加独立生成次数能否替代结构化证明演化。
- LEAP：在相同 Claude Opus 4.8 基础模型和匹配预算下保留其原有搜索策略，是主结果中最强、也最直接的智能体式搜索对照。
- Hilbert：同样使用 Claude Opus 4.8 并匹配预算，用于比较另一种智能体证明搜索方案与 ProofEvolve 的差异。
- AxProver、Aristotle 与 ReAct：论文分别评估了这三种智能体系统；复现实验统一基础模型并保留各自搜索策略。它们共同用于判断收益是否仅来自采用任意智能体循环，而非 ProofEvolve 特有的验证闭包、归档和重组机制。

**实验想回答的问题**

- 在相同基础模型、近似相同搜索预算和同一 Lean 4 核验环境下，ProofEvolve 是否比直接多次采样及其他智能体式证明搜索方法解决更多竞赛级形式化定理？
- 性能提升是否确实来自可验证的中间进展、分解—修复—重组三类变异算子以及跨问题证明复用；这些收益能否随测试时预算、证明库规模和检索深度增长？

**实验实现**

所有主实验中的基础大语言模型在单题搜索期间及跨目标过程中均冻结参数，因此结果不依赖微调或在线权重更新。智能体基线统一使用 Claude Opus 4.8，保留各自搜索策略并采用匹配预算；Lean 4 与同一 Mathlib 版本提供策略状态、 elaboration 错误和内核核验。每个目标获得并行尝试预算及有界的内核引导修复循环，预算约束模型调用、Lean 内核调用、token 和墙钟时间。专有模型通过 API 调用；开放权重模型部署在每卡 192 GB 的 NVIDIA B200 集群上，最大并发使用 224 张 GPU。所有报告成功均再次通过匹配内核和受限公理检查；作者称超过 400 次复核中没有发现假阳性。消融实验固定基础模型与计算预算，并以五个随机种子重复；跨问题真实数据复用实验采用三个匹配运行的均值和配对条件差。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| IMO-LeanProofBench 的 $60$ 题算子移除实验；固定基础模型与计算预算，五个随机种子重复 | 完整系统平均解决 $32/60$ 题，其中 Basic 为 $22/30$、Advanced 为 $10/30$。移除分解后降至 $11$ 题，移除重组后为 $14$ 题，移除修复后为 $9$ 题；对应 Advanced 仅分别解决 $2$、$3$、$2$ 题。 | 逐一移除算子表明三者均非冗余：分解负责把复杂目标转成较小子目标，修复利用 Lean 错误信息纠正失败步骤，重组把既有已验证结果应用到新目标。移除修复造成的总体下降最大，但这些是单组件删除结果，组件之间可能存在交互，不能据此把全部差值解释为某一算子的独立因果贡献。Advanced 上的相对损失更明显，支持复杂问题更依赖多阶段操作配合。 | 第 5.4 节，Figure 5<br><span class="experiment-evidence">As shown in Figure 5, the full system on average solves 32 of the 60 problems, with 22 of 30 on the Basic split and 10 of 30 on the Advanced split. Without decomposition it on average solves 11 (9 Basic, 2 Advanced), without recombination 14 (11 Basic, 3 Advanced), and without repair 9 (7 Basic, 2 Advanced).</span> |
| Lean Workbook 证明库贡献隔离：相关 top-$K$ 检索对比同库随机检索，并关闭完整搜索组件 | 当 $K=8$ 时，相关检索比零样本提高 $3.9$ 个百分点，而随机检索仅把解题率从 $49.5\%$ 提至 $49.6\%$。在三个运行中，相关检索额外关闭了 $351$ 个零样本未解实例，其中 $322$ 个、即 $91.7\%$ 的接受证明没有逐字复现任何展示证明。 | 随机检索控制了提示长度和“存在示例”本身，因而相关检索与随机检索之间的差距隔离了语义选择有用证明的价值；非逐字复现比例则削弱了简单答案复制的解释。不过“非逐字相同”不等于完全排除更抽象的模板迁移或数据相似性，且筛查依赖五个语言模型评审，因此仍需人工审计。 | 第 5.6 节，Figure 9 与 Table 7<br><span class="experiment-evidence">Across the three runs at K=8, relevant retrieval closes 351 theorem instances that zero-shot leaves open, and in 322 of them, or 91.7%, the accepted proof does not reproduce any shown proof verbatim.</span> |

**定性案例**

- Figure 4 展示一个成功证明 DAG：若干引理节点分别在第 $5$、$7$、$10$、$11$ 次迭代通过内核认证，$\rho$ 因而阶梯式上升并最终达到 $1$；同期二元成功/失败信号在根目标关闭前始终为 $0$。这个案例直观说明验证闭包如何保留和量化局部成果，但单条轨迹只能解释机制，不能证明总体性能提升。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出由神经模型生成候选操作、Lean内核验证并持续复用证明结构的形式化定理证明框架。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`de66a005e636bd91af142fa6f08e6413cb8811f4c32f73d876d0615a0d3c3474`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
