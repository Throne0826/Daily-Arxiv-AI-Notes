---
title: "[论文解读] The Thousand-Graph Hypothesis: A Testable Hypothesis of Task-Conditioned Relation Materialization in Repository-Level Code Reasoning"
description: "[arXiv 2608.26602][LLM Agent] 原文未明确报告。"
arxiv_id: "2608.26602"
announcement_date: "2026-08-28"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:45:28.395359+00:00"
source_sha256: "1dec4bc72e7f373af79efaf541ee02d7f6d9bc179af916a091660e08f1ee422d"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "仓库级代码推理"
  - "实体索引"
  - "任务条件化关系物化"
  - "千图假设"
  - "自注意力"
  - "SWE-bench Verified"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.26602</p>

# The Thousand-Graph Hypothesis: A Testable Hypothesis of Task-Conditioned Relation Materialization in Repository-Level Code Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Fei Ding</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Alibaba Group</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26602v1) · [PDF 下载](https://arxiv.org/pdf/2608.26602v1) · **关键词** 仓库级代码推理, 实体索引, 任务条件化关系物化, 千图假设, 自注意力, SWE-bench Verified<br>


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

原文未明确报告。

**不用术语来说**：原文未明确报告。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 原文未明确报告。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究仓库级代码推理，即模型需要跨越多个文件、函数、接口、配置和测试来定位并修复真实软件问题。大型仓库通常无法完整放入一次模型上下文；即使上下文窗口足够长，关键信息也可能受到位置衰减和无关证据干扰。现有知识供给方式主要包括：将仓库知识训练进模型、按任务检索局部代码，以及预先构建调用、继承、使用或依赖等显式关系图。前两者分别面临知识更新昂贵与跨文件证据遗漏，显式图则需要持续执行关系抽取、同步和一致性维护。本文据此考察一个更窄的问题：若系统只持久化代码实体并把相关实体送入上下文，模型能否通过自注意力临时形成当前任务所需的关系，而不依赖预构建的实体关系边。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**仓库级代码推理**

模型不是只理解单个函数或文件，而是要联合分析整个软件仓库中分散的代码、配置、测试与工程约束。本文的具体应用场景是依据真实问题描述修改仓库，并由可执行测试判断修复是否成功。

</div>
<div class="concept-item" markdown="1">

**实体索引与显式关系图**

实体索引记录文件、类、函数、接口等可检索对象；显式关系图还预先保存调用、继承、引用和依赖等边。前者较易随代码更新，后者便于确定性查询，但会增加关系抽取、失效边修复和图同步成本。

</div>
<div class="concept-item" markdown="1">

**任务条件化关系物化**

“物化”指把潜在联系变成当前推理中可用的关系结构；本文假设这种结构可由自注意力根据任务和上下文临时产生，而无须长期存储。同一组仓库实体面对不同任务时可能形成不同的潜在任务图，这就是“千图假设”的核心含义。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定软件仓库 $R$ 与一个仓库级修复任务 $q$，系统从仓库实体集合 $V(R)$ 中选择与任务相关的子集 $V_{\star}$，并将任务描述及这些实体组织进模型上下文。关键约束是输入侧不提供任何预构建实体关系边，即 $E_{\mathrm{input}}^{\mathrm{rel}}=\varnothing$；模型只能依据任务、实体内容和自注意力在推理时建立临时联系。由于大型仓库的实体集合本身仍可能超过上下文限制，论文使用两层实体索引：第一层负责在全仓库范围内确定相关区域，第二层在局部区域中聚焦具体实体。最终输出是针对任务的仓库修改，研究设置是在 DeepSeek-V4-Flash 与 SWE-bench Verified 上进行端到端修复评估。该设置能够检验“零预构建关系边时实体接口是否仍可支持修复”，但不能直接观测或证明模型内部确实形成了作者所设想的潜在图。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$R$**

当前待分析和修改的软件仓库。

</div>
<div class="notation-item" markdown="1">

**$V(R)$**

仓库 $R$ 中可被索引的实体集合，如文件、类、函数或接口。

</div>
<div class="notation-item" markdown="1">

**$V_{\star}\subseteq V(R)$**

针对当前任务筛选并送入推理上下文的相关实体子集。

</div>
<div class="notation-item" markdown="1">

**$E_{\mathrm{input}}^{\mathrm{rel}}=\varnothing$**

模型输入不含预先构建的实体间关系边。

</div>

</div>

**直接相关的工作**

- **RepoCoder、Repoformer 与 Agentless**: 这些方法分别通过迭代检索、选择性检索或结构化定位改善模型“到哪里读取代码”的能力，但仍需检索编排，也未直接回答相关实体进入上下文后是否还必须预计算关系。
- **GraphCoder、CodexGraph、RepoGraph 与 LocAgent**: 这些系统构建显式代码图以支持导航或检索，是本文所对照的另一类技术路线；其优势是关系可查询且较确定，但需要外部图对象、关系抽取以及仓库演化后的同步维护。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大型软件仓库包含分散在不同文件中的函数、接口、配置、测试与工程约束，整体通常超出语言模型可有效利用的上下文范围；同时，提交、重构和需求变更会持续改变仓库状态。因此，仓库级代码推理不仅要找到与当前任务有关的信息，还要以较低成本保证这些信息及时反映最新代码。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **按需检索与结构化定位**：RepoCoder、Repoformer 和 Agentless 等方法通过迭代检索、选择性检索或结构化定位，先从仓库中筛选可能相关的文件与代码实体，再将其送入模型推理；其重点是改善模型“到哪里读代码”。
- **显式仓库关系图**：该类方法预先抽取调用、继承、使用和依赖等关系，把代码实体组织成可查询的外部图；RPG-Encoder、RIG 和 Codebase-Memory 等进一步处理代码变更后的增量更新、失效边重连与一致性检查。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 局部检索虽然灵活，但在检索步数和上下文预算有限时，可能遗漏跨文件分散的关键实体或约束；扩大上下文也不能完全解决问题，因为位置衰减与证据干扰会降低模型对关键信号的有效利用。
- 显式关系图精确且可查询，却把仓库演化带来的成本转移到关系抽取、图同步和一致性维护上；而把仓库知识直接训练进模型同样成本高，并会随代码更新迅速过时。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有工作主要改进相关代码实体的定位，或假定实体间关系应预先抽取并长期保存，但尚未充分回答一个更基础的问题：当任务相关实体已经进入上下文后，模型是否仍需要外部预建关系边，以及仅持久化实体的接口能否在大型仓库中扩展。

</div>
<div markdown="1"><span>核心问题</span>

在不提供任何预建实体关系边，即满足 `$E_{\mathrm{input}}^{\mathrm{rel}}=\varnothing$` 的条件下，系统能否仅选择任务相关实体 `$V_{\star}\subseteq V(R)$`，依靠模型在推理时形成任务特定的关系结构，并完成仓库级代码修复？进一步地，两层实体索引能否比基础条件和单层索引更有效地缓解上下文容量限制？

</div>
<div markdown="1"><span>作者直觉</span>

同一批代码实体面对不同任务时，需要关注的联系并不相同：修复接口错误可能强调实现与调用方，修复配置问题则可能强调配置项、加载逻辑和测试。作者据此推测，没有必要永久保存一张覆盖所有任务的固定关系图；只要先用全局层确定相关区域，再用局部层提供实体细节，自注意力就可能依据当前任务临时突出实体之间的有用联系。这里的“千图”不是预建许多图，而是同一实体集合可随任务诱导出不同的潜在关系结构；实验结果至多与该假设相容，并不能直接证明模型内部确实形成了这样的图。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把外部知识边界限制为“实体及其索引”，不保存任何实体关系边，即始终令 $E_{\mathrm{input}}^{\mathrm{rel}}=\varnothing$。给定持续演化的代码仓库 $R_t$ 和修复任务 $q$，系统先维护包含代码内容或摘要及元数据的实体集合 $V(R_t)$，再通过两层索引依次完成仓库级全局路由和域内实体筛选，得到符合上下文预算的任务实体集 $V_q$；随后将任务与这些实体序列化为上下文 $C_q$，交给模型 $F_\theta$ 推理、生成补丁并运行测试。测试通过后只更新实体及索引，不把推理期间形成的关系写回外部存储。

其核心设想不是“代码之间没有关系”，而是关系无需预先抽取和长期维护：模型读取 $q$ 与 $V_q$ 后，自注意力会根据当前任务赋予实体间交互不同的权重，从而在一次推理内部形成潜在任务图 $G_q$。同一批实体面对不同任务时可能形成不同的 $G_q$，因此一个仓库可以按任务临时产生许多关系组织方式；“Thousand-Graph”是对此现象的可检验假设，而不是系统显式构建或输出一千张图。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 持久化抽取实体与构建索引

从仓库抽取 $V(R_t)=\{v_1,\ldots,v_n\}$，其中每个实体 $v_i=(\operatorname{id}_i,x_i,m_i)$ 保存标识、内容或摘要以及类型、路径、代码跨度、签名和职责标签等元数据；据此建立全局索引 $I^{(1)}(R)$ 与实体索引 $I^{(2)}(R)$。外部状态不包含关系边，即 $E_{\mathrm{input}}^{\mathrm{rel}}=\varnothing$。

<div class="method-step__io" markdown="1">

**输入**：时刻 $t$ 的代码仓库 $R_t$。<br>
**输出**：持久实体集合 $V(R_t)$ 和两层实体索引 $I^{(1)}(R)$、$I^{(2)}(R)$。

</div>

**直观理解**：系统保存的是可独立更新的“代码卡片”和两级目录，而不是持续维护一张代码关系网。仓库变化时只需更新受影响的卡片与目录。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 第一层全局路由

通过 $\mathcal{D}_q=\operatorname{Locate}(q,I^{(1)}(R))$，按照模块和职责把搜索范围缩小为紧凑的候选域集合 $\mathcal{D}_q$。这一步优先判断任务大致属于仓库的哪些区域，而不直接展开全部实体内容。

<div class="method-step__io" markdown="1">

**输入**：任务描述 $q$ 与仓库级索引 $I^{(1)}(R)$。<br>
**输出**：候选模块或职责域集合 $\mathcal{D}_q$。

</div>

**直观理解**：它类似先查图书馆楼层和书架：先确定任务可能落在哪些区域，避免在整个大型仓库中逐项搜索。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 第二层实体聚焦与上下文组装

系统计算 $V_q=\operatorname{Select}(q,\mathcal{D}_q,I^{(2)}(R))\subseteq V(R)$，在候选域内挑选与任务相关的实体，再构造 $C_q=\operatorname{Serialize}(q,V_q)$。$C_q$ 仅包含任务和实体内容，不含预构建关系边。

<div class="method-step__io" markdown="1">

**输入**：任务 $q$、候选域 $\mathcal{D}_q$、实体索引 $I^{(2)}(R)$ 以及实体集合 $V(R)$。<br>
**输出**：供模型使用的任务上下文 $C_q$。

</div>

**直观理解**：第二层相当于从已找到的书架中挑出具体页面，再与问题一起装入有限的阅读窗口。两次缩小范围旨在提高跨文件证据进入上下文的覆盖率。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 任务条件关系物化与补丁推理

模型在处理任务及实体 token 时，通过多层、多头自注意力产生任务相关的交互，并可抽象为潜在权重集合 $W_q$ 与任务图 $G_q=(V_q,W_q)$。这些关系只存在于本次推理的内部计算中，不被显式输出或持久化；模型据此执行推理循环并生成仓库改动 $\Delta R$。

<div class="method-step__io" markdown="1">

**输入**：序列化上下文 $C_q$ 与推理模型 $F_\theta$。<br>
**输出**：候选代码补丁或仓库改动 $\Delta R$。

</div>

**直观理解**：实体好比散放的证据，问题本身决定模型此刻把哪些证据联系起来。换一个任务，即使输入实体相同，模型关注的联系也可能不同。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 缩放点积自注意力

$$
A_{q}^{(\ell,h)}=\operatorname{softmax}\!\left(\frac{Q_{q}^{(\ell,h)}K_{q}^{(\ell,h)\top}}{\sqrt{d}}\right)
$$

**符号说明**

- $q$：当前仓库级任务。
- $\ell$：模型中的注意力层编号。
- $h$：该层中的注意力头编号。
- $Q_{q}^{(\ell,h)}$：在任务条件下，第 $\ell$ 层第 h 个头的查询矩阵。
- $K_{q}^{(\ell,h)}$：在任务条件下，第 $\ell$ 层第 h 个头的键矩阵。
- $d$：查询和键向量的维度；平方根缩放用于控制点积数值大小。
- $A_{q}^{(\ell,h)}$：任务 q 下第 $\ell$ 层第 h 个头的 token 间注意力权重矩阵。

<div class="equation-explanation" markdown="1">

**直观理解**：该式计算每个 token 对其他 token 的关注强度。因为任务描述与所选实体共同进入上下文，查询和键会受任务条件影响，所以相同实体在不同任务中可能产生不同的交互模式；这为临时关系的形成提供计算层面的解释，但注意力权重本身不自动等同于可解释的程序语义关系。<br>
**原文位置**：第 5.1 节“From self-attention to task-conditioned relation”

</div>

</div>

<div class="equation-block" markdown="1">

#### 实体关系聚合与潜在任务图

$$
w_{ij}(q)=\Phi\!\left(\left\{A_{q}^{(\ell,h)}[a,b]\,\middle|\,a\in T(v_i),\,b\in T(v_j),\,\ell,h\right\}\right),\qquad G_q=(V_q,W_q),\quad W_q=\{w_{ij}(q)\}
$$

**符号说明**

- $v_i,v_j$：任务实体集中的两个代码实体。
- $T(v_i),T(v_j)$：分别属于实体 $v_i$ 和 $v_j$ 的 token 集合。
- $A_q^{(\ell,h)}[a,b]$：第 $\ell$ 层第 h 个注意力头中，token a 与 token b 对应的注意力值。
- $\Phi$：把两个实体之间跨 token、跨层和跨注意力头的权重汇总为实体级关系强度的聚合函数；节选未规定其具体形式。
- $w_{ij}(q)$：任务 q 条件下实体 $v_i$ 与 $v_j$ 之间的潜在关系权重。
- $V_q$：两层索引为任务 q 选出的实体集合。
- $W_q$：任务 q 对应的全部潜在实体关系权重集合。
- $G_q$：由任务实体 $V_q$ 和潜在权重 $W_q$ 定义的任务条件图。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把 token 级注意力概念性地汇总为实体级联系，从而形式化“本次任务临时形成了什么关系结构”。它主要用于陈述可证伪假设：系统并不实际计算并保存一张外部 $G_q$；而且由于 $\Phi$ 未被具体化，该式不能直接当作可复现的显式建图算法。<br>
**原文位置**：第 5.1 节“From self-attention to task-conditioned relation”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。所给章节没有提出新的训练损失、参数更新规则或针对 $W_q$ 的图监督；模型参数 $\theta$ 在描述的流程中用于推理，任务关系由上下文条件下的既有自注意力临时产生。方法优化的是外部知识组织与推理流程，而不是通过训练把仓库知识写入模型；原文也未说明用 $w_{ij}(q)$ 作为任何可微优化目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 零持久边的实体接口**

外部状态只维护 $V(R)$、$I^{(1)}(R)$ 与 $I^{(2)}(R)$，并把 $E_{\mathrm{input}}^{\mathrm{rel}}=\varnothing$ 作为设计约束。实体 $v_i$ 包含可供检索和推理的内容 $x_i$ 与元数据 $m_i$，但不存在需要同步更新的外部关系模式、边集合或图数据库。

> 直观理解：该边界把维护成本集中在较稳定、可局部更新的代码实体上，避免仓库每次变化都重新计算调用、依赖或语义关系。代价是系统必须确保足够多的正确实体进入上下文，否则模型无从临时恢复缺失的联系。

**2. 两层任务望远镜**

第一层 $I^{(1)}(R)$ 以模块和职责为粒度产生 $\mathcal{D}_q$，第二层 $I^{(2)}(R)$ 在这些域中产生实体子集 $V_q$，最终序列化为 $C_q$。这种先粗后细的检索结构用于在上下文预算 $B$ 下兼顾仓库范围与局部精度。

> 直观理解：只做局部搜索容易漏掉分散在远处文件中的约束，直接放入整个仓库又会超过模型窗口；两层结构先跨仓库定位，再读取具体实体，是在覆盖率与上下文成本之间的折中。

**3. 隐式任务关系物化**

模型的注意力矩阵 $A_q^{(\ell,h)}$ 随任务上下文变化；论文用聚合函数 $\Phi$ 将实体 $v_i$ 与 $v_j$ 对应 token 间、跨层跨头的注意力汇总为潜在权重 $w_{ij}(q)$，进而定义 $G_q=(V_q,W_q)$。$W_q$ 是用于陈述和检验假设的潜变量，而非方法实际存储、查询或直接监督的图。

> 直观理解：这里的“物化”指关系在计算过程中发挥作用，并不意味着生成一份可查看的边表。论文预测同一仓库面对不同任务 $q_1$ 与 $q_2$ 时会有 $G_{q_1}\neq G_{q_2}$，但该差异属于行为假设，不能仅凭输入不同就视为已经证明。

**训练与推理**

持久化阶段从当前仓库 $R_t$ 抽取或更新实体，并维护全局索引 $I^{(1)}(R)$ 和实体索引 $I^{(2)}(R)$，不抽取、存储或同步外部关系边。推理阶段输入任务 $q$：第一层定位候选域 $\mathcal{D}_q$，第二层选择 $V_q$，随后把 $q$ 与实体内容序列化为 $C_q$；模型 $F_\theta$ 在该上下文中通过注意力隐式组织实体关系，执行推理循环并输出改动 $\Delta R$。补丁测试失败时，将失败信息作为新证据继续推理；测试通过时写回仓库，并只刷新实体和索引。所给章节未描述额外微调、索引器训练或端到端联合训练过程。

**复现信息**

公平解释该方法必须保留三项边界条件：第一，输入中预构建实体关系边数量为零，即 $E_{\mathrm{input}}^{\mathrm{rel}}=\varnothing$；第二，最终上下文 $C_q$ 只能由任务与选中实体内容组成；第三，补丁通过测试后只更新实体与两层索引。实体元数据至少可包含类型、路径、代码跨度、签名和职责标签，这些字段支持两层定位；但节选未明确报告实体粒度、$\operatorname{Locate}$ 与 $\operatorname{Select}$ 的具体算法、排序阈值、上下文截断策略、$\Phi$ 的实现、提示模板、测试重试次数或失败证据的编码方式，因此不能据此补造完整复现实参。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- SWE-bench Verified：用于评估真实软件仓库问题解决能力的验证子集。本文以任务成功率为结果指标，但所给章节未说明样本规模、具体版本、任务筛选方式或是否评估完整子集，因此这些信息均为“原文未明确报告”。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Success rate (%)**

衡量在 SWE-bench Verified 上被判定为成功解决的任务比例。所给章节没有进一步说明成功判定流程、测试执行规则或置信区间。 （越高越好，因为更高比例表示系统成功完成了更多基准任务。）

</div>
<div class="metric-item" markdown="1">

**Absolute gain（百分点）**

两个条件成功率的直接差值，例如 $95.6\%-92.1\%=3.5$ 个百分点；它反映绝对改善幅度，而不是相对百分比增长。 （正值越大通常表示相对对照条件的绝对提升越明显。）

</div>
<div class="metric-item" markdown="1">

**Error reduction**

作者先以 $100\%-\text{Success rate}$ 计算失败率，再比较失败率由一个条件下降到另一个条件的变化。原文给出的是失败率从 $7.9\%$ 或 $5.8\%$ 降至 $4.4\%$，未明确将其换算为相对错误减少比例。 （失败率越低越好；相对于对照的下降越大，表示未成功任务越少。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Base system，无实体索引、无预构建关系边

<div class="result-value" markdown="1">

作者报告成功率为 $92.1\%$。

</div>

这是受控比较的参照点，说明同一基础系统在没有实体索引时已取得较高成功率。该结果本身不证明实体索引有效，也不能说明系统在其他模型、仓库或上下文预算下具有同样表现。

<div class="result-source" markdown="1">

来源：Table 2, Section 6.1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Base system | none | 92.1

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### One-layer index，无预构建关系边

<div class="result-value" markdown="1">

作者报告成功率为 $94.2\%$，相对 Base system 绝对提高 $2.1$ 个百分点。

</div>

在共同排除预构建关系边后，单层实体索引优于无索引条件，支持“仅提供实体级外部接口也可能帮助仓库级推理”的作者主张。不过，该比较不能单独确定增益来自更好的实体定位、额外可访问的信息、提示结构变化还是推理资源差异。

<div class="result-source" markdown="1">

来源：Table 2, Section 6.1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

One-layer index | none | 94.2

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Two-layer index，无预构建关系边

<div class="result-value" markdown="1">

作者报告成功率为 $95.6\%$；相对 Base system 绝对提高 $3.5$ 个百分点，相对 One-layer index 提高 $1.4$ 个百分点。

</div>

这是三种条件中的最佳结果，与“两层结构比无索引和单层索引更有效”的作者结论一致。分析上，它为分离全局路由与局部实体聚焦提供了受控但有限的支持；由于没有方差、重复运行或显著性检验，不能据此判断 $1.4$ 个百分点的单层到两层差异是否稳定，也不能直接证明推理过程中确实形成了正确的任务条件关系。

<div class="result-source" markdown="1">

来源：Section 6.1, discussion of Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 2, the two-layer design improves success from 92.1% to 95.6%, with an absolute gain of 3.5 points over the base and 1.4 points over one-layer.

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

- Base system：不使用实体索引，是判断实体索引整体是否有增益的主要对照；它与其他条件一样不含预构建实体—关系边，因此差异主要对应索引设计，而非显式关系图。
- One-layer index：采用单层实体索引，是两层索引的结构性对照；两者比较用于检验将全局路由与局部实体聚焦分层是否比单层组织更有效。
- Two-layer index：论文提出的完整实验条件；它不是外部基线，而是与 Base system 和 One-layer index 比较的目标方法。

**实验想回答的问题**

- 在同一模型和同一代码修复基准上，仅引入实体索引、且不预先构建实体间关系边，是否能提高仓库级代码推理的任务成功率？
- 相比单层实体索引，两层索引能否通过区分全局路由与局部实体聚焦进一步提高成功率，从而为“按任务在推理时物化关系”的设计提供受控证据？

**实验实现**

实验固定使用 DeepSeek-V4-Flash，并在 SWE-bench Verified 上比较 Base system、One-layer index 与 Two-layer index 三种条件。关键控制是三者均不包含预构建实体—关系边，使比较集中于“是否使用实体索引”以及“索引采用一层还是两层”。所给章节未报告提示模板、推理预算、检索数量、运行次数、随机性控制、统计显著性、置信区间、成本或延迟，因此无法判断结果对具体执行配置的敏感程度。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除全部实体索引：Two-layer index 对比 Base system | 成功率由 $95.6\%$ 降至 $92.1\%$，即移除两层实体索引对应 $3.5$ 个百分点的下降；失败率则由 $4.4\%$ 升至 $7.9\%$。 | 该比较整体隔离“完整两层实体索引”相对于“完全无实体索引”的作用，并在双方均无预构建关系边时检验索引是否有用。它同时改变了索引的存在与层级结构，因此不能进一步区分全局路由层和局部聚焦层各自贡献了多少。 | Section 6.1, discussion of Table 2<br><span class="experiment-evidence">This corresponds to an error reduction from 7.9% to 4.4% versus base and from 5.8% to 4.4% versus one-layer.</span> |
| 将两层索引简化为单层索引：Two-layer index 对比 One-layer index | 成功率由 $95.6\%$ 降至 $94.2\%$，即两层设计相对单层设计具有 $1.4$ 个百分点的优势；对应失败率由 $4.4\%$ 升至 $5.8\%$。 | 该消融最直接检验分层组织是否必要：在两者都有实体索引且都没有预构建关系边时，差异主要对应一层与两层结构。结果方向支持分离全局路由和局部实体聚焦，但原文没有分别移除两层中的某一层，也没有统计不确定性，因此无法判断具体是哪一层产生增益或该小幅差异是否可重复。 | Section 6.1, discussion of Table 2<br><span class="experiment-evidence">As shown in Table 2, the two-layer design improves success from 92.1% to 95.6%, with an absolute gain of 3.5 points over the base and 1.4 points over one-layer.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It proposes an inference-time external indexing and task-conditioned retrieval interface for repository-level code reasoning.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`1dec4bc72e7f373af79efaf541ee02d7f6d9bc179af916a091660e08f1ee422d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
