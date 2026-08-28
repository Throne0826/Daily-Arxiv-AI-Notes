---
title: "[论文解读] FaithSieve: Fine-Grained Evaluation of Math Proofs with Faithful Formal Evidence"
description: "[arXiv 2608.26310][LLM 评测] FaithSieve研究如何把自然语言数学证明拆成局部推理单元，并仅在形式化陈述与原意语义对齐时采用Lean验证证据，从而更可靠地定位首个逻辑错误。"
arxiv_id: "2608.26310"
announcement_date: "2026-08-28"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:31:41.142768+00:00"
source_sha256: "0b91e66846fe235b1cb80d826d8d6b7dce0619dc5424b1e28770f6e7d640e65e"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "自然语言数学证明评估"
  - "第一错误定位"
  - "Lean"
  - "mathlib"
  - "证明状态变化"
  - "类型化证明义务"
  - "语义忠实性"
  - "形式证据"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.26310</p>

# FaithSieve: Fine-Grained Evaluation of Math Proofs with Faithful Formal Evidence

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Ziyu Wang, Qiming Dai, Yishan Wu, Zaiwen Wen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Academy for Advanced；Affiliation: Peking University；Affiliation: School of Mathematical Sciences；Affiliation: Theory Lab, 2012 Labs；Affiliation: Huawei Technologies Co., Ltd；Affiliation: Beijing International Center for；Affiliation: Mathematical Research</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26310v1) · [PDF 下载](https://arxiv.org/pdf/2608.26310v1) · **关键词** 自然语言数学证明评估, 第一错误定位, Lean, mathlib, 证明状态变化, 类型化证明义务, 语义忠实性, 形式证据<br>


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

FaithSieve研究如何把自然语言数学证明拆成局部推理单元，并仅在形式化陈述与原意语义对齐时采用Lean验证证据，从而更可靠地定位首个逻辑错误。

**不用术语来说**：一篇证明即使最后答案正确，中间也可能漏掉条件、跳过关键推导，或从某个错误继续写出看似合理的结论；因此，评估系统不仅要判断整篇证明是否正确，还要找出最早出错的位置。语言模型容易被流畅表述迷惑，而Lean只能严格检查提交给它的形式化命题，无法保证该命题就是原文真正声称的内容。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将“局部性”和“语义忠实性”明确为Lean辅助自然语言证明评估的核心障碍，并提出FaithSieve：先把粗粒度步骤分解为局部状态转移，再提取带类型的证明义务，综合轻量检查、Lean验证与语义对齐评分来定位首个错误。
- 作者构建经专家核验的ProofLoc-Olympiad与ProofLoc-University基准，用于检验系统能否在竞赛数学和大学高等数学证明中准确定位首个错误，而不只是判断最终答案或整篇证明的对错。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于自然语言数学证明评估与形式化验证的交叉领域。大语言模型生成的证明可能结论正确却在中间遗漏条件、跳过推导、引入隐含假设，或从早期错误继续得到表面合理的后续内容，因此评估任务不仅要判断整篇证明是否正确，还要定位第一个逻辑错误。自然语言评审方法能够直接处理非形式化文本，但其依据主要是模型评分或分类，容易忽略局部推理缺口；Lean 等交互式定理证明器则能由内核严格检查形式命题及其证明对象，但它只保证“提交给 Lean 的命题被证明”，不保证该命题忠实表达原文。故本文关注的核心前提是：形式证据必须同时满足局部性与语义忠实性，避免用更宽泛、更弱或发生含义漂移的命题绕过待检查的局部推理。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**Lean 与 mathlib**

Lean 是基于依赖类型论的交互式定理证明器：一个证明只有在其内核确认所提交证明对象具有目标命题对应的类型时才会被接受。mathlib 是 Lean 的数学库，提供定义、定理、记号和自动化策略，也在实践中限定了哪些数学对象与背景事实容易被形式化和验证。

</div>
<div class="concept-item" markdown="1">

**证明状态与策略**

证明状态记录当前所有待证目标及其局部假设；策略是把一个证明状态变换为另一个状态的操作，例如引入假设、改写目标、拆分情形或解决子目标。当最终状态不再包含目标时，形式证明才算完成。

</div>
<div class="concept-item" markdown="1">

**证明状态变化与类型化证明义务**

本文把自然语言中的局部推理理解为从“步骤执行前已有的事实、条件和目标”到“步骤执行后新增、改写或消去的内容”的状态变化。类型化证明义务明确标注该变化承担的推理责任，例如推出新事实、保持等价改写、覆盖全部分类情况或验证所构造见证满足条件。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一道数学问题及其自然语言多步证明，其中单个书面步骤可能包含多个细粒度推理动作；系统在不假设整篇证明已被完整形式化的条件下，检查各局部状态转移，并输出第一个错误所在的原始证明步骤。对每个局部转移，执行前状态包含可用假设、已知事实、分支条件与当前目标，执行后状态描述该步骤声称新增、变换、分解或完成的内容；只有当对应 Lean 命题忠实保留原始上下文、数学对象和逻辑形式时，Lean 验证成功才可作为支持证据，而验证失败或超时不能直接推出自然语言步骤错误。该设定因此区别于整篇证明的二元判定：它要求证据能够对应到局部推理责任，并将细粒度判断重新汇总到原始步骤层级。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$S=\{G_1,\ldots,G_n\}$**

一个证明状态，由有限个尚未解决的目标 $G_1,\ldots,G_n$ 构成。

</div>
<div class="notation-item" markdown="1">

**$\{h_1,\ldots,h_m\}\vdash g$**

单个目标的形式：在局部假设 $h_1,[0m\ldots,h_m$ 下，需要证明结论 $g$。

</div>
<div class="notation-item" markdown="1">

**$S_0\xrightarrow{T_1}S_1\xrightarrow{T_2}\cdots\xrightarrow{T_k}S_k$**

策略序列驱动的证明过程，其中 $T_i$ 把状态 $S_{i-1}$ 变换为 $S_i$；若最终状态 $S_k$ 没有剩余目标，则证明完成。

</div>
<div class="notation-item" markdown="1">

**$G_i$**

证明状态中的第 $i$ 个待证目标，包含其局部上下文与目标结论。

</div>

</div>

**直接相关的工作**

- **ProcessBench、Hard2Verify 与 ProofGrader / ProofBench**: 这些工作为过程级判断或错误定位提供自然语言评估基线，但其证据主要来自模型对推理文本的评分或分类；本文要补足的是对局部推理缺口更严格、且可与原步骤对应的形式证据。
- **Chain of States for Lean formalization**: 本文借鉴其“状态—策略”视角，将证明表示为连续状态变化；不同之处是 FaithSieve 把该思想用于尚未完全形式化的自然语言证明，以局部前后状态和证明义务进行错误定位，而非假定每一步都已经是可执行的 Lean 策略。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型已能生成较长的多步数学证明，但这些证明可能遗漏适用条件、暗中引入假设、跳过必要推导，或在早期犯错后继续得到貌似可信的结论。实际评估需要逐步审查局部推理，并识别首个错误，因为这个位置决定了后续哪些结论已经失去可靠依据；只核对最终答案或给出整体正确性标签不足以满足这一需求。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于语言模型的自然语言过程评估**：自洽性、过程监督、过程奖励模型，以及ProcessBench、Hard2Verify、ProofGrader／ProofBench等工作，主要让模型对自然语言推理步骤进行评分、分类或错误定位。它们直接处理原始证明文本，因而无需先完成整篇证明的形式化。
- **基于Lean与mathlib的形式验证**：系统先把数学主张表示为Lean中的形式命题，再提交证明对象或策略，由Lean内核检查其类型是否满足目标；mathlib提供定义、引理和自动化工具。若形式命题及其证明通过检查，就能获得机器可核验的逻辑证据。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 自然语言评估的主要证据仍来自模型自身的评分或分类，容易忽视局部推理缺口，并可能被表面连贯、术语正确但逻辑不完整的叙述误导；因此，它难以稳定地区分真正的首个错误与由早期错误引发的后续异常。
- Lean只保证“提交的形式命题可证”，不保证该命题忠实表达原证明步骤。自动形式化可能删除假设、增加额外条件、反转蕴含方向，或把有争议的局部断言改写成另一个更宽泛或更容易证明的目标；此时Lean成功会形成与原文无关的伪支持。反过来，Lean失败或超时也可能只是形式化或库覆盖不足，不能直接证明自然语言步骤错误。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少一种把形式验证安全地用于自然语言证明首错定位的机制：系统既要把整篇证明限制为可归责的局部状态转移，又要判断生成的Lean证明义务是否保留原步骤的上下文、数学对象和逻辑形式。没有这两层约束，严格的形式验证仍可能验证错对象，无法成为可信的局部证据。

</div>
<div markdown="1"><span>核心问题</span>

能否构建一个端到端评估框架，将自然语言证明分解为细粒度局部推理责任，并通过语义对齐门控，只在形式化目标忠实于原始主张时采用Lean证据，从而比直接的自然语言判断更准确地定位首个逻辑错误？

</div>
<div markdown="1"><span>作者直觉</span>

首错定位更像检查一系列相邻的“状态变化”，而不是重新证明整篇文章：每一步都应说明它从已有假设和事实中新增了什么、改写了什么或解决了哪个目标。把这种变化转成局部证明义务，可以防止Lean绕开当前争议去证明一个过宽目标；再用语义对齐评分过滤发生含义漂移的形式化陈述，则可把Lean从不加区分的最终裁判改造成受约束的证据来源。这样既利用形式系统的严格性，也避免把“另一个命题可证”误当成“原步骤正确”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

FaithSieve把自然语言证明的首错定位建模为“局部化—筛选—形式化—融合”流程。输入是题目$p$及按基准步骤划分的证明$\pi=(s_1,\ldots,s_n)$；系统先将每个粗粒度步骤拆成忠实的细粒度子步骤，再构造证明状态树$\mathcal{T}=(V,E)$，其中节点保存当前假设与目标，边表示一次局部推理。随后，系统为所有边估计可疑度，只在最早高风险边及其短前缀组成的审计窗口$W$内生成类型化证明义务。每个义务被翻译为Lean命题或纯数值表达式；形式语句必须先通过语义忠实度门控，之后才由Lean或SymPy验证。局部结果最终映射回原始步骤，系统返回最早具有可靠反面证据的步骤，若不存在则综合证据判断为正确或输出风险步骤。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 忠实细化与证明状态树构造

语言模型在不修补原证明的前提下，将每个$s_i$拆成更细的推理动作，并递归构造证明状态树$\mathcal{T}=(V,E)$。节点$v$保存状态$S_v=(\Gamma_v,G_v)$，其中$\Gamma_v$是当前可用假设，$G_v$是当前待证目标；边$e=(v\to v')$按事实推出、改写、目标约化、分类讨论或引理引入等类型记录为$u_e$，并保留其与原始$s_i$的映射。

<div class="method-step__io" markdown="1">

**输入**：数学题$p$与自然语言证明$\pi=(s_1,\ldots,s_n)$，其中$s_i$是基准规定的第$i$个输出与标注步骤。<br>
**输出**：带上下文、目标、分支作用域、转移类型和原步骤索引的细粒度EdgeUnit集合。

</div>

**直观理解**：原始一步可能同时完成代入、计算和结论跳转，整步送入定理证明器会掩盖中间漏洞。该阶段像把一段合并的程序拆成逐条指令，并为每条指令保存执行前后的状态。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 可疑度搜索与审计窗口调度

模型对每条边进行一次轻量局部审查，输出是否可疑、可疑原因及区间$[0,1]$内的风险分数；论文将分数高于$0.6$的边视为较可疑候选。系统不只选全局最高分边，而以最早的可疑边为焦点，并纳入一段较短的前缀，特别覆盖具有特殊转移类型的前序边，形成审计窗口$W$。

<div class="method-step__io" markdown="1">

**输入**：证明状态树中的全部EdgeUnit及其前后上下文、目标关系、分支范围和转移类型。<br>
**输出**：成本受控、按首错定位需求排序的待验证局部边集合$W$。

</div>

**直观理解**：Lean验证每条边的成本很高，因此先用便宜的筛查寻找最可能且最早出错的位置。保留前缀是为了防止真正的首错分数略低，却被后续由它引发的显眼错误遮蔽。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 类型化证明义务生成

系统依据转移类型选择模板，把“状态如何变化”转换成可直接检查的局部数学责任$O(u_e)$。例如，事实推出检查新事实是否由先前上下文蕴含，目标约化检查新目标是否足以推出旧目标，分类讨论检查各分支是否有效且完备；若一条边既引入事实又改变目标，则拆成“新事实成立”和“目标约化有效”两个义务，避免把尚未验证的事实偷偷当作前提。

<div class="method-step__io" markdown="1">

**输入**：审计窗口$W$中的边$u_e$、边的转移类型、状态变化以及对应原始证明文本。<br>
**输出**：每条被审计边对应的一个或多个类型化自然语言义务$o\in O(u_e)$。

</div>

**直观理解**：状态变化本身不是定理证明器可以直接回答的问题，因此要把它改写成明确的是非题。按类型生成义务还能确保检查的是原证明在该处真正承担的逻辑责任，而不是随意挑选一个容易证明的相关命题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 忠实度门控的形式验证

语句代理生成Lean陈述$\hat{m}$；若义务是不含变量和自然语言解释的纯数值等式链或单个比较式，则改走SymPy数值检查。Lean候选先做编译与语法、类型或依赖修复，再计算$S_{\mathrm{faith}}(m,\hat{m};C)$并生成语义漂移报告；低于语言含义或关键分量阈值时，根据报告修改$\hat{m}$并重试，仍不忠实或超时则返回inconclusive，通过门控后才验证原命题、否定命题或反例存在性。

<div class="method-step__io" markdown="1">

**输入**：局部义务$o$、其自然语言陈述$m$、局部上下文$C$、题目$p$及对应EdgeUnit摘要。<br>
**输出**：每个义务的局部状态$\{\texttt{passed},\texttt{refuted},\texttt{inconclusive}\}$、经忠实度和检查器置信度调整的证据强度，以及Lean产物、反例或诊断信息。

</div>

**直观理解**：Lean只能保证它实际收到的形式命题成立，不能保证该命题就是原文想说的内容。忠实度门控相当于先核对“翻译是否忠于原问题”，核对合格后才把形式证明当作证据。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 语句忠实度总分

$$
S_{\mathrm{faith}}(m,\hat{m};C)=\sqrt{S_{\mathrm{prem}}(m,\hat{m};C)\cdot S_{\mathrm{conc}}(m,\hat{m};C)}\cdot S_{\mathrm{hol}}(m,\hat{m};C)
$$

**符号说明**

- $m$：从局部边生成的自然语言证明义务陈述。
- $\hat{m}$：准备交给Lean验证的形式化陈述。
- $C$：该义务所在的局部上下文，包括已有假设、分支条件、固定对象和见证等。
- $S_{\mathrm{faith}}$：形式陈述对自然语言义务的总体忠实度，取值属于区间[0,1]。
- $S_{\mathrm{prem}}$：前提忠实度，衡量形式陈述是否保留所需上下文、分支假设和固定见证。
- $S_{\mathrm{conc}}$：结论忠实度，衡量形式结论是否对应自然语言义务的目标断言。
- $S_{\mathrm{hol}}$：整体语义分数，检查推理方向、对象与见证、语义角色、步骤关系及空洞形式化等全局问题。

<div class="equation-explanation" markdown="1">

**直观理解**：前提分数与结论分数先取几何平均，因此任何一侧严重失真都会显著拉低总分；再乘整体分数，用来惩罚逆转蕴含方向、调换对象角色或构造空洞命题等仅靠局部槽位不易发现的问题。该分数不是数学正确性的分数，而是决定Lean结果能否被用于评价原义务的证据门控。<br>
**原文位置**：第4.1节，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 前提与结论语义槽匹配分数

$$
S_{\mathrm{prem}}=\frac{\sum_{t\in T_{\mathrm{prem}}}\mathrm{match}(t,\hat{m})}{|T_{\mathrm{prem}}|},\qquad S_{\mathrm{conc}}=\frac{\sum_{t\in T_{\mathrm{conc}}}\mathrm{match}(t,\hat{m})}{|T_{\mathrm{conc}}|}
$$

**符号说明**

- $T_{\mathrm{prem}}(m,C)$：从自然语言义务与局部上下文抽取的前提侧语义槽集合，例如假设、分支条件和固定见证。
- $T_{\mathrm{conc}}(m)$：从自然语言义务抽取的结论侧语义槽集合，例如目标对象、量词结构和目标关系。
- $t$：一个待核对的前提或结论语义元素。
- $\mathrm{match}(t,\hat{m})$：语义检查器给出的槽位保留程度，取值属于区间[0,1]；它依据语义而非字符串重合判断槽位是否被保留、遗漏、弱化、强化或替换。
- $|T_{\mathrm{prem}}|$：前提侧语义槽的数量。
- $|T_{\mathrm{conc}}|$：结论侧语义槽的数量。

<div class="equation-explanation" markdown="1">

**直观理解**：该式分别对前提侧和结论侧的关键含义逐项核对，再取平均。这样能明确诊断形式化究竟漏掉了哪个假设、替换了哪个对象或改变了哪个结论，而不是只给出一个无法修复的整体相似度。<br>
**原文位置**：第4.1节，公式(2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。原文将FaithSieve描述为由语言模型、Lean MCP工具、语义检查器和SymPy组成的推理时评估框架，没有提出用于训练模型的新损失函数，也未说明对骨干模型进行参数微调。公式(1)和公式(2)用于形式证据的语义门控与语句修订，而非通过梯度优化学习参数；因此不能把$S_{\mathrm{faith}}$解释为训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 证明状态树与EdgeUnit**

证明状态树$\mathcal{T}=(V,E)$借用Lean证明状态的视角，但节点内容仍以自然语言表达。每个节点$v$为$S_v=(\Gamma_v,G_v)$；若子步骤推出新事实$h$，则子状态更新为$\Gamma_{v'}=\Gamma_v\cup\{h\}$，若发生目标转换则更新$G_v$，若发生分类讨论则生成带各自分支条件的多个子节点。边$u_e$同时保存转移前后状态、类型、分支范围及原始粗步骤索引。

> 直观理解：该模块解决“验证位置不一致”的局部性问题：它迫使系统逐项检查原证明实际经过的中间推理，而不能绕过有问题的中间结论，直接证明一个更宽泛的最终目标。

**2. 类型化义务编译器**

义务编译器依据边类型，把状态转移转换为具有固定检查语义的陈述。支持的主要责任包括：新事实由上下文推出、改写或计算等价、后目标足以推出前目标、分类讨论覆盖全部情形、被删除分支不可能、具体见证满足目标、争议断言成立、上下文蕴含裸断言，以及多个情形构成适当划分；复合转移可产生多个义务。

> 直观理解：这一模块在自然语言状态和形式定理之间提供受约束的接口。它不是总结整篇证明，而是回答“这一小步究竟需要证明什么”，从而减少验证目标被模型任意改写的空间。

**3. 忠实度感知的形式评估代理**

代理包括形式语句生成与编译修复、语义忠实度检查、SymPy数值分支、Lean证明搜索和证据封装。语义检查分别评估前提槽、结论槽及整体关系，整体部分覆盖步骤关系、对象与见证、推理方向、语义角色和语法忠实性；通过门控后，代理根据可疑度选择尝试证明原命题，或证明其否定及寻找反例，并将超时、形式化漂移和搜索失败区分为不同的inconclusive诊断。

> 直观理解：该代理解决“形式语句与原意不一致”的语义问题，同时避免把证明器没找到证明误判为命题错误。只有形式翻译可信且Lean给出证明或反例时，证据才具有较强的正面或反面意义。

**训练与推理**

原文所述完整过程属于推理阶段。给定$p$与$\pi$后，系统先忠实细化证明并构造$\mathcal{T}$，再对全部EdgeUnit做轻量可疑度扫描，以最早风险边及其前缀形成$W$。对每个$u_e\in W$，系统执行自然语言局部审查并生成$O(u_e)$；对每个$o\in O(u_e)$，纯数值陈述由SymPy检查，其余陈述先生成并编译$\hat{m}$，必要时借助Lean MCP修复语法、类型和依赖问题。语义检查器计算$S_{\mathrm{faith}}$并给出漂移类别、置信度、缺失假设、过度概括示例和修订建议；若关键得分偏低，则据此重写$\hat{m}$并重复编译和语义检查。通过门控后，Lean证明搜索代理根据风险方向尝试证明原命题、否定命题或反例存在性，直到成功或达到时限。最后，系统把passed、refuted和inconclusive连同忠实度报告及自然语言审查融合为$\mathrm{Info}(u_e)$，映射回$s_i$，检查可靠负面证据之前的不确定前缀，并输出$\hat{y}$。原文节选未报告任何额外训练阶段。

**复现信息**

公平复现所需的关键设定包括：粗步骤是最终评测与输出单位，细分子步骤和EdgeUnit仅是内部验证单位；拆分必须保留原证明的结论、变量作用域、分类讨论措辞、具体见证和数值计算，不得借机修补逻辑。可疑度取值为$[0,1]$，文中使用高于$0.6$作为较可疑候选，但最终调度基于“最早风险边加短前缀”，而非仅取最高分。SymPy分支只处理不含变量和自然语言解释的纯数值等式链或单一比较，其他义务进入Lean分支。Lean编译成功不等于义务成立，必须先通过忠实度门控；证明搜索超时、编译或形式化失败、未通过门控均返回inconclusive，而不能直接记为refuted。节选未明确给出忠实度门限的具体数值、审计窗口长度、Lean搜索时限、提示词全文以及每个义务的最大修订轮数，这些信息需要结合论文附录和补充实验材料核查。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ProofLoc-Olympiad：350 道奥林匹克风格的代数与数论题。GPT-4o 按编号生成完整候选证明，并非被要求故意制造错误；数学专家标注证明是否正确，以及造成实质性证明断裂的最早粗粒度步骤。它用于测试竞赛数学场景中的首错定位。原文未明确报告训练、验证、测试划分，实验将其作为评测基准。
- ProofLoc-University：200 道大学教材级问题，包含拓扑与度量空间 20 道、线性代数 40 道、抽象代数 40 道、实分析 50 道、凸分析 30 道、凸优化 20 道。题目来源于相应领域的标准教材，候选证明和专家标注流程与 ProofLoc-Olympiad 相同，用于检验方法能否跨越六个高等数学领域。原文未明确报告数据划分。
- 两套数据的金标准都对齐原始证明中的编号粗步骤，而不是 FaithSieve 内部进一步拆分的 EdgeUnit。标注者为数学博士生；出现歧义时，标注者联合检查争议命题是否可修复以及后续步骤是否依赖它，达成一致后才确定标签。因此，评测目标是用户可见步骤上的首错位置，而非系统内部单元的分类准确率。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Exact accuracy**

预测必须与金标准完全一致：正确证明应输出 correct，错误证明则必须命中专家标注的首个错误粗步骤。它直接衡量本文核心任务——精确首错定位，而不只判断整篇证明有无错误。 （越高越好，因为更高值表示系统更常给出完全正确的首错位置或正确标签。）

</div>
<div class="metric-item" markdown="1">

**Binary accuracy**

只考察系统是否正确区分整篇证明为正确或错误，不要求错误证明的具体首错步骤完全命中。它用于区分整体正确性识别能力与更困难的定位能力。 （越高越好，但它不能单独证明系统具备精确定位能力。）

</div>
<div class="metric-item" markdown="1">

**Semantic-gate precision/recall**

在人类复核的形式化陈述上，以“语义忠实”为正类、gate 接受为预测正类，precision 衡量被接受陈述中忠实陈述的比例，recall 衡量忠实陈述被 gate 保留的比例。该指标检验形式命题是否保留原自然语言义务，而不是检验证明题的最终首错准确率。 （两者通常越高越好：高 precision 减少语义漂移证据进入融合阶段，高 recall 减少有效形式证据被错误丢弃；二者需要权衡。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### ProofLoc-Olympiad，GPT-5.4 骨干：完整 FaithSieve 对比同骨干 direct judge

<div class="result-value" markdown="1">

FaithSieve 的 Exact accuracy 为 81.43%，Binary accuracy 为 93.71%；direct judge 分别为 72.29% 和 88.29%，即精确首错定位提高 9.14 个百分点，二分类提高 5.42 个百分点。

</div>

这是最直接的整体效果检验：在相同 GPT-5.4 骨干下，加入局部结构和忠实形式证据后，不仅更能判断证明是否有错，也更能找准最早出错步骤。由于这是整套流水线与直接判断的比较，它证明的是组合方案有效，不能单独归因于 Lean、EdgeUnit 或 semantic gate 中某一个组件。

<div class="result-source" markdown="1">

来源：Section 5.1；Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

With the GPT-5.4 backbone, FaithSieve achieves 81.43% exact accuracy and 93.71% binary accuracy on ProofLoc-Olympiad, outperforming GPT-5.4 direct judging at 72.29% and 88.29%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### ProofLoc-University，GPT-5.4 骨干：跨六个大学数学领域的完整 FaithSieve 对比 direct judge

<div class="result-value" markdown="1">

FaithSieve 达到 84.50% Exact accuracy 和 92.50% Binary accuracy，direct judge 为 75.00% 和 87.00%；对应提升 9.50 和 5.50 个百分点。

</div>

与 Olympiad 结果相近的提升说明收益并不局限于代数和数论竞赛题，而能延伸到教材级高等数学证明。不过各领域样本量仅为 20 至 50，道域结果波动较大；总体平均不能证明所有领域都同样受益。

<div class="result-source" markdown="1">

来源：Section 5.1；Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On ProofLoc-University, FaithSieve reaches 84.50% exact / 92.50% binary accuracy, compared with 75.00% exact / 87.00% binary for GPT-5.4 direct judging.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### ProofLoc-Olympiad，Qwen3.5-9B 骨干：完整 FaithSieve 对比 direct judge

<div class="result-value" markdown="1">

完整 FaithSieve 的 Exact accuracy 为 74.00%，Binary accuracy 为 89.14%；direct judge 仅为 53.71% 和 76.00%，分别提高 20.29 和 13.14 个百分点。

</div>

较小的 9B 骨干从结构化局部证据中获得了比 GPT-5.4 更大的绝对增益，表明该流程可能在基础模型直接审查能力较弱时尤其有价值。不过这只是两个骨干上的观察，不能据此推出模型越小，FaithSieve 的增益必然越大；同时也未报告成本与延迟比较。

<div class="result-source" markdown="1">

来源：Table 5，Qwen3.5-9B 列

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Full FaithSieve 74.00 89.14 Direct judge 53.71 76.00

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 两套基准的候选证明均由 GPT-4o 自然生成，且题目集中于竞赛代数/数论和六个大学数学领域；这比人工对抗扰动更贴近日常生成错误，但尚不能证明结果适用于其他证明生成模型、几何题、概率论、组合数学或研究级证明。
- 节选未报告多次运行、置信区间或显著性检验，也未给出完整系统相对 direct judge 的计算成本和延迟。semantic gate 在人工校准中仍接受了 13 个语义漂移陈述，并具有 65.00% 的 FPR，因此形式证据经过筛选后仍不能被视为绝对可靠。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Direct judge：模型只接收题目和原始编号证明，一次输出 correct 或 step N；不使用证明分解、证明状态图、EdgeUnit、局部复核、Lean、semantic gate 或证据融合。这是最关键的对照，因为它隔离了 FaithSieve 整套结构化与形式化流程相对于同一基础模型直接判断的增益。
- Step3 graph judge：保留证明分解和证明状态图，但移除局部审查、Lean 验证与证据融合。它用于判断仅把证明组织成图结构是否已经有助于首错定位。
- EdgeUnit + NL only：保留细粒度 EdgeUnit 的自然语言局部审查和最终综合，但移除 Formal Evaluation Agent。它用于区分细粒度表示本身的收益与形式化验证额外带来的收益。
- 不同 direct-judge 基础模型：GPT-5.4、Gemini-3.1-Pro、Opus-4.6、DeepSeek-v4-Pro、GLM-5.1 和 Qwen3.5-9B。该比较展示直接判断能力随模型变化的范围；其中 GPT-5.4 是强闭源骨干，Qwen3.5-9B 是 9B 参数开放权重规模的对照。

**实验想回答的问题**

- FaithSieve 的细粒度证明分解、局部审查与经过语义一致性筛选的形式化证据，是否能比一次性自然语言判断更准确地定位自然语言数学证明中的首个错误步骤？
- 性能提升具体来自哪些组件：证明状态图、局部 EdgeUnit、Lean 辅助验证，还是过滤形式化语义漂移的 semantic gate；这些组件对不同规模的语言模型是否同样有效？

**实验实现**

主实验在两套数据上比较完整 FaithSieve 与同骨干 direct judge，并重点报告 GPT-5.4 和 Qwen3.5-9B。完整流程包括证明状态树与 EdgeUnit、由可疑度引导的审计窗口、带类型的证明义务发现、Formal Evaluation Agent、陈述忠实度评分和 Evidence Fusion。Olympiad-350 的完整产物平均含 15.59 个非占位 EdgeUnit，但平均只选择 4.91 个候选进入昂贵检查；总计选择 1,720/5,458 个 EdgeUnit，即 31.51%。局部审计窗口包含当前单元及至多六个前序单元。消融采用 replay-style 协议：已有中间产物保持固定，仅重放被改动组件之后的流程，因而更接近组件级归因，但不等同于从头运行每个变体。direct judge 的输出限制为 correct 或 step N，不可解析输出计为解析失败。原文节选未明确报告随机种子、重复运行次数或置信区间。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| ProofLoc-Olympiad：移除局部 EdgeUnit，退回粗步骤级判断 | GPT-5.4 从完整系统的 81.43% Exact / 93.71% Binary 降至 60.86% / 72.29%；Qwen3.5-9B 从 74.00% / 89.14% 降至 62.29% / 77.71%。 | 该消融直接隔离“局部性”设计：基准中的编号步骤只是标注单位，一个步骤内部可能包含多个实际推理跳跃。大幅下降支持把粗步骤拆为局部转换对于发现最早逻辑断点很关键。不过 replay-style 设置固定了已有中间产物，因此结果表示下游重放条件下移除局部单元的影响，不完全等价于重新训练或从头执行另一套系统。 | Section 5.2；Table 5<br><span class="experiment-evidence">GPT-5.4 with w/o local EdgeUnits drops to 60.86% exact / 72.29% binary, and Qwen3.5-9B with w/o local EdgeUnits obtains 62.29% exact / 77.71% binary.</span> |
| ProofLoc-Olympiad：移除 semantic gate 的严格筛选，使低置信度混合验证结果更容易进入证据集 | GPT-5.4 降至 70.86% Exact / 86.29% Binary，低于完整系统的 81.43% / 93.71%；Qwen3.5-9B 降至 70.86% / 86.00%，低于完整系统的 74.00% / 89.14%。 | 该变化说明“Lean 验证成功”本身不足以成为可靠证据：若自动形式化后的命题添加假设、弱化目标或变成空泛真命题，证明器可能验证一个偏离原意的陈述。gate 的作用是先检查形式命题与原义务的语义对齐，再允许形式结果参与最终判断；消融下降支持这一设计，但人工校准中的误接受仍表明 gate 不能彻底消除语义漂移。 | Section 5.2；Table 5<br><span class="experiment-evidence">GPT-5.4 with w/o semantic gate drops to 70.86% exact / 86.29% binary; Qwen3.5-9B with w/o semantic gate obtains 70.86% exact / 86.00% binary, also below the corresponding Full FaithSieve result.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces benchmarks and a Lean-assisted framework for evaluating and localizing errors in LLM-generated mathematical proofs.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`0b91e66846fe235b1cb80d826d8d6b7dce0619dc5424b1e28770f6e7d640e65e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
