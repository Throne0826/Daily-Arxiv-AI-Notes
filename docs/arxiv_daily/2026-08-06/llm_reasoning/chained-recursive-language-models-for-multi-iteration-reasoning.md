---
title: "[论文解读] Chained Recursive Language Models for Multi-Iteration Reasoning"
description: "[arXiv 2608.05124][LLM Reasoning] 本文提出链式递归语言模型（Chained RLM）：让同一模型通过多个相互独立的新鲜推理根分阶段处理长上下文任务，并借助可持久化的纯文本摘要、黑板和任务工件传递必要状态。"
arxiv_id: "2608.05124"
announcement_date: "2026-08-06"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:51:36.050820+00:00"
source_sha256: "138604f1c61ffe79849d935a14837600128f27e0935af8901aa154e98dfa605b"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "长上下文推理"
  - "递归语言模型"
  - "推理时计算"
  - "多阶段推理"
  - "持久化制品"
  - "上下文退化"
  - "状态交接"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.05124</p>

# Chained Recursive Language Models for Multi-Iteration Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Purbesh Mitra, Sennur Ulukus</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> University of Maryland</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.05124v1) · [PDF 下载](https://arxiv.org/pdf/2608.05124v1) · **关键词** 长上下文推理, 递归语言模型, 推理时计算, 多阶段推理, 持久化制品, 上下文退化, 状态交接<br>


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

本文提出链式递归语言模型（Chained RLM）：让同一模型通过多个相互独立的新鲜推理根分阶段处理长上下文任务，并借助可持久化的纯文本摘要、黑板和任务工件传递必要状态。

**不用术语来说**：面对长文档、代码库或多步数据时，模型即使能一次读入全部内容，也不一定能把复杂工作组织好：它需要同时找证据、记录进度、完成计算、检查错误并决定何时作答，因而容易漏掉已检查事项、过早下结论，或让前期错误一路传到最终答案。论文要解决的重点不是让上下文窗口容纳更多文本，而是让模型在多轮推理中更可靠地管理中间工作。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出一种无需额外训练的线性推理时架构 Chained RLM：重复调用同一个递归语言模型，每次调用形成一个不继承完整对话历史的新鲜推理根，使复杂任务能够被拆成连续的提取、修正和审计阶段。
- 作者设计了以人类可读纯文本为接口的交接与工件工作区：前序推理根通过摘要、黑板、下一步行动以及证据账本、推导或检查清单等持久工件传递状态；完整历史轨迹单独保存，仅在后续推理根认为信息不足时按需查看。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型的长上下文推理与推理时计算研究。其基本问题是：即使模型的上下文窗口足以容纳整份文档、代码库或记录，模型仍需在一次推理轨迹中同时完成证据定位、中间状态维护、计算或工具调用、结果核验与最终作答，容易因工作状态混乱而发生浅层提取、遗漏检查或过早定论。本文关注的不是扩展上下文窗口或训练新模型，而是如何在模型参数不变的条件下，把一次复杂推理组织为多个具有清晰交接边界的阶段。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**长上下文推理**

模型需要在较长的文档、代码或多步数据中寻找并组合信息，以完成提取、计数、排序或多跳推理等任务。困难不仅在于信息能否放入上下文窗口，还在于模型能否持续维护正确、可核验的工作状态。

</div>
<div class="concept-item" markdown="1">

**递归语言模型（RLM）**

RLM把长提示视为可由模型检查和操作的外部环境，根模型能够读取相关片段、运行代码、使用工具，并对子问题递归调用语言模型。它无需修改模型权重，但全局工作状态通常仍集中在同一条编排轨迹内。

</div>
<div class="concept-item" markdown="1">

**上下文退化（context rot）**

上下文退化指模型在长而复杂的交互轨迹中逐渐失去任务结构，例如忘记已核验的内容、沿用早期错误假设或未经审计便输出答案。它说明“能够看到全部信息”不等于“能够可靠地管理全部推理状态”。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一项长上下文任务，包括原始问题及其完整上下文；任务可能要求信息提取、计数、排序或跨多处证据的推理。系统在推理时重复调用同一个底层模型，每次调用形成一个新的推理根：新根仍可访问原始问题与上下文，但不会自动继承前一根的完整对话轨迹，只接收前序阶段留下的纯文本摘要、黑板、下一步提示和持久化任务制品；必要时才主动检查保存的原始轨迹。各根能够检查变量、运行代码、调用子模型以及读写证据账本、推导记录、审计结果或检查清单，最终输出任务答案。该设定不训练模型、不使用强化学习，默认也不依赖专门验证器；核心假设是，把中间状态外化为可读、可编辑的制品，并由新上下文中的同一模型继续检查，可以减少单一轨迹中的错误固化与状态混乱。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Recursive Language Models（Zhang et al., 2025）**: 这是本文最直接的架构基础：RLM允许根模型把长提示作为外部环境进行检查、分解和递归调用，但整体工作状态仍主要保存在一次编排轨迹中。Chained RLM在其外部增加线性的多根执行结构，通过摘要、黑板和持久化制品把状态交给新的根，使早期提取或聚合结果能够被重新审阅和修改。
- **MemGPT（Packer et al., 2023）**: MemGPT将长上下文交互视为分层记忆管理问题，在活动上下文与长期存储之间移动信息。本文同样使用外部持久状态，但其重点不是一般性的存储与检索，而是由模型动态生成、并要求后续根持续保留、编辑和审计的任务专用制品。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

长上下文推理常见于大型文档、代码库、会议记录和多步数据分析。直接回答要求单条推理轨迹同时浏览上下文、筛选证据、保存中间状态、处理工具结果、核验假设并生成答案。在抽取、计数、排序和多跳推理中，这种职责集中尤其危险：模型可能因“上下文腐化”而失去工作结构，前期遗漏或错误也可能持续传播，最终得到未经充分审计的答案。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **显式推理与搜索方法**：思维链提示让模型写出中间推理步骤；自洽性对多条推理路径采样并聚合答案；Tree-of-Thoughts 则显式搜索多个候选思路。这类方法通过增加推理过程或探索分支来改善一次任务求解。
- **工具、外部记忆与递归调用方法**：ReAct 在推理与外部行动之间交替，MemGPT 在不同记忆层之间移动信息，Reflexion 保存先前尝试的文字反馈，MOTIF 迭代求解多个任务模块；递归语言模型还可针对上下文的不同部分发起递归模型调用。它们分别借助工具、记忆、反馈、模块化或递归访问来扩展单次模型交互的能力。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 作者认为，困难任务不适合把全部求解职责压在单个前向过程或一条持续增长的交互轨迹中。即使模型能够访问完整上下文并递归调用工具，仍可能忘记已完成的检查、进行浅层抽取或在真正审计之前作答；可见“能看到信息”并不等于“能稳定管理工作状态”。
- 现有机制没有直接回答如何让后续模型调用在摆脱冗长历史负担的同时，继续使用并修订前序调用形成的结构化中间成果。若每次都从头处理，会浪费既有工作；若始终携带完整轨迹，则旧推理、噪声与错误又会持续占据上下文并影响后续判断。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种受控的推理时架构，能够在不训练新模型、默认不依赖专用验证器的条件下，把同一模型的多次调用组织成若干具有新鲜上下文的阶段，并通过简洁、可检查、可编辑的持久工件维持阶段间连续性。更具体地说，仍需验证这种“新鲜推理根加工件续接”是否比直接回答，乃至带递归工具调用的常规语言模型，更适合长上下文中的多次迭代推理。

</div>
<div markdown="1"><span>核心问题</span>

在底层模型和任务条件受控时，将同一递归语言模型串联为多个新鲜推理根，并只通过纯文本连续状态和持久工件交接，能否以额外推理成本为代价，提高长上下文任务相对于直接语言模型回答及常规递归工具调用的准确性；这种收益又在何种任务条件下出现？

</div>
<div markdown="1"><span>作者直觉</span>

可以把该架构理解为分阶段的数据分析：第一个推理根先建立候选事件账本，第二个推理根在重新获得清爽工作空间后检查并修正账本，第三个推理根再审核计数并作答。摘要与黑板保留当前进度，持久工件保存可复查的证据和推导，而完整旧轨迹不自动塞入后续提示。这样，后续调用关注的是“检查和扩展已有成果”，而不是在一条越来越混乱的推理记录中同时记忆所有步骤。不过这只是作者提出的机制性假设：若初始工件结构有误，后续推理根可能继承错误；若后续调用忽略优质工件，整条链也可能漂移，而且多次调用必然增加推理成本。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Chained Recursive Language Model（Chained RLM）是一种不改动模型参数的推理时架构。给定问题 $q$、原始长上下文 $c$、底层语言模型 $f_\theta$、工具集 $\mathcal{T}$ 和最大根节点数 $R$，系统不要求一次模型调用同时完成检索、记录、核验和作答，而是依次启动至多 $R$ 个使用同一模型的全新根节点。每个根节点都能重新访问完整的 $(q,c)$，但默认不继承前一节点冗长且可能包含错误的对话轨迹，只接收由黑板 $B_r$、持久化工件 $A_r$、交接摘要 $H_r$ 和可选近期工作摘录 $E_r$ 组成的紧凑链状态 $s_r$。根节点使用类似 Python REPL 的工具检查上下文、计算中间结果、读写纯文本工件，随后输出最终答案或交接信息。

端到端看，该方法把一条很长的内部推理轨迹改造成“提取、审计、汇总”等可跨节点延续的阶段性工作。首个根节点通常建立候选记录或证据表，后续根节点先读取并保持既有工件结构，再修正实体映射、事件定义、顺序或计数；只有证据充分时才返回最终答案，否则通过包含 SUMMARY、BLACKBOARD 和 NEXT 的纯文本交接指定下一项可验证工作。通俗地说，同一个模型会以“重新开始思考”的方式轮流接班，但每次都能看到原题、原始材料和前任留下的精炼笔记与工作底稿，从而保留有用证据，同时降低旧推理过程持续占用上下文或将早期错误直接传下去的风险。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始化任务与共享工作区

系统将黑板初始化为纯文本 $B_0$，并令工件集合 $A_0=\emptyset$、前驱摘要 $H_0=\emptyset$；随后为第一个根节点构造链状态 $s_0=(B_0,A_0,H_0,E_0)$，其中可选摘录 $E_0$ 初始时通常为空。

<div class="method-step__io" markdown="1">

**输入**：用户问题 $q$、原始上下文 $c$、底层模型 $f_\theta$、工具集 $\mathcal{T}$ 和最大根节点数 $R$。<br>
**输出**：可由根节点读取的原始任务、工具环境和初始共享状态 $s_0$。

</div>

**直观理解**：这一步相当于把原始资料放在公共资料柜中，再准备一块短笔记板和一个空的证据文件夹。它只规定协作载体，不预先规定具体任务应使用怎样的表格或推理程序。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 启动全新根节点并执行有界工作

系统以同一底层模型执行一次全新的调用 $o_r\sim f_\theta(q,c,s_r;\mathcal{T})$；根节点先检查黑板和工件清单，再使用短步骤代码检索、抽取、计算或核验，并且必须在提交结果前创建或更新至少一个任务相关的纯文本工件。

<div class="method-step__io" markdown="1">

**输入**：固定的原始输入 $(q,c)$、当前链状态 $s_r$、工具集 $\mathcal{T}$，其中 $r\in\{0,1,\ldots,R-1\}$。<br>
**输出**：当前根节点的原始轨迹 $T_r$、更新后的工件，以及类型为 FINAL 或 HANDOFF 的输出 $o_r$。

</div>

**直观理解**：每个节点都像一位刚接手任务的研究者：它能重读全部原始材料，但先前研究者的冗长思考不会自动灌入它的上下文。一次只做范围明确且能留下可检查记录的工作，避免新节点只是重复一次浅层分析。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 以工件为中心提取和审计证据

根节点根据任务自行选择纯文本或 TSV 工件结构：首个节点可建立候选事件账本、抽取表或推导记录，后续节点必须先读取相关工件并保持其结构，再扩展、纠错或审计其中的实体映射、事件定义、证据位置、顺序和计数逻辑。

<div class="method-step__io" markdown="1">

**输入**：原始上下文 $c$、当前黑板 $B_r$ 和已有工件集合 $A_r$。<br>
**输出**：可被后续节点继续维护的详细证据工件，以及记录当前结论、假设、矛盾和可信状态的紧凑黑板。

</div>

**直观理解**：工件是跨节点传递的“工作底稿”，而不是只供当前调用使用的草稿。例如面对长转录中的事件计数，第一轮先逐条列出候选事件，第二轮检查归类是否一致，第三轮再从审计后的行重新计数。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成交接并更新链状态

根节点按纯文本格式提交 HANDOFF，其中 SUMMARY 概括已完成工作和当前判断，BLACKBOARD 给出紧凑可审计状态，NEXT 指定一个能够改变、验证或证伪答案的具体后续动作；宿主据此生成 $B_{r+1}$、保留 $A_{r+1}$、追加 $H_{r+1}$，并可加入有界摘录 $E_{r+1}$。

<div class="method-step__io" markdown="1">

**输入**：尚不足以最终作答的根节点结果、更新后的黑板和工件，以及当前原始轨迹 $T_r$。<br>
**输出**：供下一个全新根节点使用的链状态 $s_{r+1}=(B_{r+1},A_{r+1},H_{r+1},E_{r+1})$，同时原始轨迹 $T_r$ 被单独保存。

</div>

**直观理解**：交接不是把此前全部聊天记录直接转发，而是留下“已经确认什么、仍有哪些问题、下一步具体查什么”。若摘要或工件存在矛盾、证据不足，后续节点仍可按需回看磁盘上的完整轨迹，但该轨迹默认不占用新调用的提示上下文。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 根节点条件生成

$$
o_r \sim f_{\theta}\!\left(q,c,s_r;\mathcal{T}\right),\qquad r=0,1,\ldots,R-1
$$

**符号说明**

- $o_r$：第 $r$ 个根节点的输出，可以是最终答案或交接信息。
- $f_{\theta}$：参数为 $\theta$ 的底层语言模型；不同根节点复用同一模型。
- $q$：用户提出的问题。
- $c$：所有根节点都可重新访问的原始长上下文。
- $s_r$：第 $r$ 个根节点收到的紧凑链状态。
- $\mathcal{T}$：根节点可调用的工具集合，例如类似 Python REPL 的执行环境和工件读写接口。
- $R$：允许执行的最大根节点数量。
- $r$：当前根节点的索引。

<div class="equation-explanation" markdown="1">

**直观理解**：该式刻画架构最核心的调用方式：每一轮都用同一个模型重新处理原题和原始上下文，但额外接收当前链状态并可使用工具。与单次基线 $y\sim f_\theta(q,c)$ 相比，性能差异来自推理过程的组织和额外计算，而不是更换模型参数或不给基线原始上下文。<br>
**原文位置**：第3节 System Model，公式（2）；算法1第7行

</div>

</div>

<div class="equation-block" markdown="1">

#### 链状态分解

$$
s_r=\left(B_r,A_r,H_r,E_r\right)
$$

**符号说明**

- $s_r$：传入第 $r$ 个根节点的连续性状态。
- $B_r$：当前纯文本黑板，保存紧凑、可审计的工作状态。
- $A_r$：当前可用的持久化任务工件集合。
- $H_r$：由前驱根节点交接信息累积形成的紧凑摘要。
- $E_r$：可选的前一轮近期工作摘录，只作为待核验的原始草稿信息。

<div class="equation-explanation" markdown="1">

**直观理解**：该式说明跨轮连续性不是靠完整对话历史维持，而是拆成短期总览、详细证据、前驱摘要和少量近期草稿。真正详细且需要持续修订的任务状态主要放在 $A_r$ 中，$B_r$ 和 $H_r$ 用于帮助新节点快速定位当前结论与下一步，$E_r$ 则不能被视为权威证据。<br>
**原文位置**：第3节 System Model，公式（3）；算法1第6行

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。Chained RLM 是推理时架构，原文没有提出新的训练损失、监督信号、参数更新规则或针对链式根节点的微调目标；所有根节点复用固定参数 $\theta$。因此其“优化”发生在计算流程层面：通过增加独立模型调用、外部化中间状态和安排后续审计，提高有限上下文下答案的证据可靠性，而非通过梯度下降改变模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 新鲜根节点执行器**

每个根节点都是对同一 $f_\theta$ 的独立推理调用，始终重新获得 $(q,c)$ 和工具 $\mathcal{T}$，但默认仅从 $s_r$ 接收经过整理的连续性信息。系统把每次调用的完整轨迹另存为 $T_r$，只有当摘要或工件不足、矛盾或缺少支撑时，后续节点才按需检查旧轨迹。

> 直观理解：该模块通过清除默认会话历史来减弱陈旧假设和早期错误的惯性，同时又允许模型回到原始证据重新判断。它不是模型集成：所有节点共享参数，变化的是每次调用获得的紧凑工作状态。

**2. 黑板与持久化工件工作区**

黑板 $B_r$ 保存当前最佳答案、已验证事实、假设、开放问题、矛盾、证据指针和工件可信状态，内容应短且便于审计；工件集合 $A_r$ 则保存候选账本、抽取表、推导、审计记录和核验清单等较详细信息。宿主仅负责存储纯文本，不解析任务语义；工件类型、数量和格式由模型按问题决定，后续节点原则上保持首个节点选定的结构。

> 直观理解：黑板回答“目前整体进展如何”，工件回答“具体证据和计算过程是什么”。这种分工既避免把所有细节塞进下一轮提示，又让后续节点能逐行纠错、扩展和复算，而不是只能相信上一轮给出的结论。

**3. 纯文本交接与终止控制**

非最终节点通过 SUMMARY、BLACKBOARD、NEXT 三段式 HANDOFF 传递状态，可附加非权威的近期工作摘录；宿主从交接文本更新 $B_{r+1}$ 和 $H_{r+1}$，保留根节点写入的 $A_{r+1}$。根节点可在证据充分时输出 FINAL，非末节点在关键不确定性仍存在时应交接，最后一个节点则必须返回当前支持最充分的答案。

> 直观理解：三段式格式迫使当前节点既说明已做工作，也给下一节点一个具体且可证伪的动作。作者刻意不用 JSON、XML 或 YAML 等宿主解析模式，使工作状态更像研究者写给下一位接手者的笔记，但这也意味着状态一致性主要依赖模型遵守指令。

**训练与推理**

训练阶段：原文未设置专门训练过程，直接使用现有底层语言模型。推理阶段：宿主接收 $(q,c)$，初始化 $B_0$、$A_0$ 和 $H_0$，随后对 $r=0$ 到 $R-1$ 循环启动全新根节点。每个节点先读取链状态或调用状态接口，检查黑板与工件，再用工具完成一个有界步骤；首个节点决定工件集合及结构，后续节点先列举并读取相关工件，在不破坏结构的前提下纠错、扩展或审计，并在 FINAL 或 HANDOFF 前至少写入或更新一个任务相关工件。

若输出为 FINAL，系统立即返回 $y_r$；若输出为 HANDOFF，宿主提取 SUMMARY、BLACKBOARD 和 NEXT，更新下一轮黑板、摘要和可选近期摘录，同时保留工件并将完整轨迹 $T_r$ 单独存盘。对长上下文抽取、计数和排序任务，系统提示首个节点优先建立候选行并交接，后续节点审计候选及聚合规则；最终节点在检查实体映射、事件定义、顺序和计数后作答。若所有允许节点都未提前结束，算法返回最后一个节点能够给出的、由现有证据支持最充分的答案。

**复现信息**

公平解释该方法时，关键控制变量是所有根节点与单次基线使用相同底层模型并接收相同的原始问题和上下文；方法增益伴随更多模型调用、输入输出 token 和工具执行，不能视为等计算量比较。根节点需要类似 Python REPL 的环境，并能检查原始上下文、运行代码、列举和读写持久化工件、查询链状态以及提交 FINAL 或 HANDOFF。宿主应保存每个 $T_r$，但默认不把完整轨迹加入下一轮提示，只传递 $s_r$，以避免历史内容重新占满上下文。

连续性数据使用纯文本：交接固定包含 SUMMARY、BLACKBOARD 和 NEXT，可选加入有界的近期摘录；工件优先采用 `.txt` 或 `.tsv`，不依赖 JSON、XML、YAML 或宿主理解任务含义。每个节点必须维护至少一个问题相关工件，首个节点选择结构，后续节点保持结构并明确记录修改；如果旧结构确实失效，应建立名称清楚的替代工件，并在黑板说明迁移原因。原文节选没有明确给出 $R$ 的具体取值、上下文截断策略、摘要长度上限、近期摘录长度、采样参数、工具沙箱配置或宿主解析失败时的恢复规则，这些均需在复现时另行核对完整论文或实现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- RULER：长上下文能力基准，用于检验模型在长文本中的信息定位、聚合或推理能力；原文未明确报告该实验所用的样本规模、具体子任务、数据划分及上下文长度。
- BABILong：长文档多跳推理基准，用于测试模型能否从分散在长上下文中的信息完成多步推理；原文未明确报告样本规模、划分、具体任务配置及上下文长度。
- LongBench v2 与 OOLONG-real：分别用于评估更综合的长上下文理解能力和真实场景中的长文档任务表现；原文未明确报告二者的样本规模、划分、具体子任务及上下文长度。由于实验表同时列出这两个基准，本分析将其作为两个独立评测来源，但不补充未给出的数据集细节。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Pass@1 accuracy**

对基准中的 `$L$` 个问题，统计首次尝试得到正确答案的问题比例：`$\mathrm{Pass@1}=\frac{1}{L}\sum_{j=1}^{L}\mathbb{I}_j$`，其中 `$\mathbb{I}_j$` 表示第 `$j$` 个问题的答案是否正确。 （越高越好，因为它直接表示一次推理成功的比例；但它不反映答案生成所消耗的根节点数、令牌数或成本。）

</div>
<div class="metric-item" markdown="1">

**平均根节点数**

每个任务平均使用的推理根节点数量，用于衡量 Chained RLM 将任务拆分为多少次新鲜上下文推理。 （通常越低越好，但必须结合准确率解释；更多根节点可能换来更高准确率，因此该指标主要用于评估准确率与计算量之间的权衡。原文未提供具体数值。）

</div>
<div class="metric-item" markdown="1">

**交接次数与每任务推理成本**

交接次数衡量前后根节点传递摘要、黑板或工件的频率；每任务推理成本衡量一次任务的资源开销，原文称令牌和成本依据当前 `$GPT\text{-}5\text{-}mini$` API 定价计算。 （交接次数和成本越低越好，但应与准确率共同判断系统是否具有实际效率优势；原文未报告表 2 的具体数值。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### RULER：Regular LLM 与 Chained RLM 的准确率比较

<div class="result-value" markdown="1">

Regular LLM（`$GPT\text{-}5\text{-}mini$` toolcall）准确率为 `$87\%$`，Chained RLM 准确率为 `$92\%$`，绝对提升 `$5$` 个百分点。

</div>

在 RULER 上，链式工件交接方案比直接工具调用方案取得更高的首次答案准确率，说明将长任务拆成多次新鲜推理可能有助于处理长上下文信息。不过，这只是该基准上的结果，不能单独证明提升来自某一个具体组件，也不能说明 Chained RLM 的资源成本更低。

<div class="result-source" markdown="1">

来源：Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

RULER | 87% | 92%

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### BABILong：Regular LLM 与 Chained RLM 的准确率比较

<div class="result-value" markdown="1">

Regular LLM（`$GPT\text{-}5\text{-}mini$` toolcall）准确率为 `$44\%$`，Chained RLM 准确率为 `$59\%$`，绝对提升 `$15$` 个百分点。

</div>

BABILong 通常强调长文档中的多跳信息组合；在该设置下，Chained RLM 的相对优势比 RULER 更明显，表明中间摘要、黑板和持久化工件可能帮助后续推理根节点重新检查并延续前序结果。但由于没有计算量匹配结果，不能排除额外调用次数本身对准确率的贡献。

<div class="result-source" markdown="1">

来源：Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

BABILong | 44% | 59%

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### LongBench v2 与 OOLONG-real：综合长上下文与真实任务比较

<div class="result-value" markdown="1">

在 LongBench v2 上，Regular LLM 准确率为 `$41\%$`，Chained RLM 为 `$52\%$`，绝对提升 `$11$` 个百分点；在 OOLONG-real 上，Regular LLM 为 `$14\%$`，Chained RLM 为 `$38\%$`，绝对提升 `$24$` 个百分点。

</div>

两个更具综合性或真实性的评测都显示 Chained RLM 准确率更高，尤其是 OOLONG-real 上的差距最大，说明该方法的潜在收益不限于单一合成基准。然而，作者没有报告各数据集的任务组成、方差或统计显著性，也没有在所给摘录中给出成本和交接次数，因此这些结果支持“准确率提升”的作者主张，却不足以证明整体效率或普适性提升。

<div class="result-source" markdown="1">

来源：Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

LongBench v2 | 41% | 52%
OOLONG-real | 14% | 38%

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 比较缺少完整的计算量匹配证据。原文称最终实验包含 compute-matched setting，但又说明第一版首先采用直接 LLM 基线；所给摘录没有报告匹配后的准确率，因此无法区分架构收益与额外推理调用带来的收益。
- 实验报告不完整：虽然提到平均根节点数、交接次数和每任务成本，并引用了 Table 2，但所给章节摘录没有这些数值，也没有样本规模、数据划分、重复采样、误差范围或显著性检验。因此结果的统计稳定性、资源代价和可复现性原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Regular LLM（`$GPT\text{-}5\text{-}mini$`，toolcall）：模型直接根据问题和上下文生成答案，并允许递归工具调用；它是检验 Chained RLM 是否带来额外收益的低复杂度直接比较对象。原文说明该基线是“clean lower-complexity reference point”，但未明确报告工具调用的具体工具、调用预算或提示词。

**实验想回答的问题**

- 在相同底层模型 `$GPT\text{-}5\text{-}mini$` 下，采用新鲜推理根节点与持久化工件交接的 `$Chained\text{ RLM}$`，是否比直接回答或带工具调用的常规 `$LLM$` 在长上下文任务上获得更高的精确答案准确率？
- 新鲜上下文、摘要、黑板和任务工件组成的多轮链式推理，能否在提取、计数、多跳检索和长上下文聚合等任务中减少单条推理轨迹中早期错误持续传播的问题，同时带来可接受的推理资源开销？

**实验实现**

实验比较两种系统：Regular LLM 直接依据问题和上下文预测，Chained RLM 则让同一个底层模型被反复调用，每次调用从新的推理根节点开始。新根节点不继承完整对话历史，而是接收原始问题与上下文，以及前序根节点留下的简短纯文本摘要、纯文本黑板和任务特定持久化工件。原文指定两种系统均使用 `$GPT\text{-}5\text{-}mini$`，并说明 Chained RLM 记录最大链长度、每个根节点的最大迭代次数、每个根节点的最大子 `$LLM$` 调用次数以及是否启用缓存。实验还计划包含计算量匹配设置，但原文明确指出第一版首先使用直接 `$LLM$` 基线作为较低复杂度参照，因此计算量匹配结果原文未明确报告。评测主指标是首次尝试的精确任务准确率，辅以根节点数、交接次数和每任务成本；数据集规模、划分、随机采样次数、置信区间及完整资源表数值均原文未明确报告。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出通过连续的新上下文推理根、摘要和持久化工件来提升长上下文多步推理的推理时架构。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`138604f1c61ffe79849d935a14837600128f27e0935af8901aa154e98dfa605b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
