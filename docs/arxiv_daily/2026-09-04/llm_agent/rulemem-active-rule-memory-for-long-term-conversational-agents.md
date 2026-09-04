---
title: "[论文解读] RuleMem: Active Rule Memory for Long-Term Conversational Agents"
description: "[arXiv 2609.03915][LLM Agent] 原文未明确报告。"
arxiv_id: "2609.03915"
announcement_date: "2026-09-04"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:42:16.429861+00:00"
source_sha256: "10e06b7bebac540d850c6d64ed700019c09d7a4d33f1611a2ef97eea72b41def"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "长期对话问答"
  - "外部记忆"
  - "规则记忆"
  - "规则归纳"
  - "自然语言 Horn 子句"
  - "语义鸿沟"
  - "证据检索"
  - "逻辑推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2609.03915</p>

# RuleMem: Active Rule Memory for Long-Term Conversational Agents

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Xingyuan Zeng, Zuohan Wu, Quanming Yao, Yue Wang, Wei Liu, Libin Zheng, Jiuke Wang, Jian Yin</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Sun Yat-sen University, Zhuhai, China；The Hong Kong University of Science and Technology (Guangzhou), Guangzhou, China；Shenzhen Institute of Computing Sciences, Shenzhen, China；The Hong Kong Polytechnic University, Hong Kong, China；Tsinghua University, State Key Laboratory of Space Network and Communications, Beijing National Research Center for</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03915v1) · [PDF 下载](https://arxiv.org/pdf/2609.03915v1) · **关键词** 长期对话问答, 外部记忆, 规则记忆, 规则归纳, 自然语言 Horn 子句, 语义鸿沟, 证据检索, 逻辑推理<br>


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

本文研究长期对话问答中的外部记忆：智能体需要从规模庞大、结构松散且分散于不同时间的历史对话中找出证据，并据此生成可靠答案。由于大语言模型的上下文窗口有限，且参数化记忆难以及时更新，常见系统会把历史交互存入外部记忆，并在回答时检索相关内容。该任务的关键困难有两个：一是查询与证据之间可能存在语义鸿沟，例如问题询问“为何缺席”，历史却只记录“预订了假期”，导致相似度检索漏掉隐含相关证据；二是即使取回了相关片段，模型仍须判断哪些事实可作前提、如何连接前提与结论，长而松散的上下文容易造成逻辑链断裂或幻觉。本文据此将既有记忆概括为“事实记忆”和“事实组织”，并进一步提出更高抽象层次的“规则归纳”。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**外部记忆**

独立于大语言模型参数的存储与检索模块，用于保存历史对话、用户信息或任务事实，并在推理时取回相关内容。它主要缓解上下文容量有限和模型参数难以动态更新的问题。

</div>
<div class="concept-item" markdown="1">

**语义鸿沟**

问题的表达与真正证据在字面或表层语义上并不相似，但二者在逻辑上相关。仅依赖关键词或向量相似度时，这类证据容易被漏检。

</div>
<div class="concept-item" markdown="1">

**自然语言 Horn 子句**

Horn 子句是一类形如“若若干条件成立，则得到一个结论”的逻辑规则；本文用自然语言表达其条件和结论。这样既保留规则的前提—结论结构，又能覆盖对话中灵活、多样的语义表达。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一段持续增长、跨越较长时间的历史对话，以及当前用户提出的问答查询；历史中可能包含回答所需的一个或多个事实，但这些事实可能彼此分散，也可能与查询缺少直接词汇或表层语义重合。系统需要在有限上下文条件下，从外部记忆中找回逻辑相关证据，确定这些证据能够支持的推理关系，并输出有历史事实依据的答案。本文假设大语言模型可承担规则归纳、检索辅助与答案推理，但直接让模型归纳规则可能产生过度泛化或幻觉，因此规则不能无验证地写入记忆。其问题视角不是只提高片段存储或相似度检索能力，而是从历史交互中形成可复用的条件—结论规则，使规则在新查询到来时主动提示应寻找哪些前提，并作为连接证据与答案的显式逻辑骨架。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **MemGPT、Mem0 与 LangMem**: 代表“事实记忆”范式：直接保存对话片段或实例级事实，再依据词汇或浅层语义相似度检索。本文认为这类方法在查询与证据存在语义鸿沟时容易召回失败。
- **Zep、Mem0g、A-MEM 与 MemInsight**: 代表“事实组织”范式：使用时间知识图谱、Zettelkasten 式语义网络或层次摘要连接和压缩事实。本文认为其连接仍停留在实例层面，记忆扩张后可能引入与查询无关的噪声，并把前提筛选和推理链构造留给大语言模型。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

RuleMem 将长期对话记忆组织为两个相互配合的空间：事实记忆库 $\mathcal{M}_{F}$ 保存带时间的具体事实，规则记忆库 $\mathcal{M}_{R}$ 保存从多跳推理路径中归纳出的自然语言规则。系统先自底向上从对话抽取事实、采样推理路径并诱导规则，再通过 Rule Perplexity Consistency（RPC）检验规则是否同时符合语言模型先验和事实证据，最后自顶向下用相关规则指导事实召回、实体约束和答案生成。直观地说，它不只是把过去对话“存起来”，而是从过去经验中总结“如果满足这些条件，通常可以推出什么”的可复用模板，并在回答新问题时反向使用这些模板寻找证据。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 事实记忆构建

系统解析对话，抽取主体实体、关系、客体实体和时间，形成时间四元组集合 $\mathcal{F}=\{(e_s,r,e_o,t)\}$，并将这些具体事实存入事实记忆库 $\mathcal{M}_{F}$。

<div class="method-step__io" markdown="1">

**输入**：长期、多轮对话文本及其时间信息。<br>
**输出**：可检索、可追溯的时间事实集合 $\mathcal{F}$ 及事实记忆库 $\mathcal{M}_{F}$。

</div>

**直观理解**：这一步把分散在聊天记录中的信息整理成“谁—做了什么—涉及谁或什么—发生在何时”的结构化卡片。保留时间和原始对话依据，便于后续核查事实。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 推理路径挖掘与规则归纳

系统在事实图上进行受约束随机游走，产生候选路径；随后由大语言模型过滤不合逻辑的路径，并结合事实和原始片段重建有效推理路径 $\mathcal{P}_{c}$。具有相同或相似关系模式的路径被分组，再由大语言模型抽象实体名称、加入类型占位符，并归纳为自然语言 Horn 规则。

<div class="method-step__io" markdown="1">

**输入**：事实集合 $\mathcal{F}$、其图结构组织形式以及对应的原始对话片段。<br>
**输出**：由具体推理路径抽象得到的候选规则集合，存入规则记忆库 $\mathcal{M}_{R}$ 的待验证部分。

</div>

**直观理解**：系统先从事实卡片中寻找“事实一连接到事实二”的连锁关系，再把多条相似链条概括成通用规则。例如，不记住特定的 Alice 和某场马拉松，而是总结适用于任意人物和事件的关系模式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### RPC 规则验证

RPC 分别计算规则结论在无条件和给定规则前件时的平均负对数似然下降量，得到内部一致性信号 $\Delta_{\mathrm{self}}(r)$；再比较加入事实证据前后的结论似然，得到外部事实一致性信号 $\Delta_{\mathrm{fact}}(r)$。两个信号经 Sigmoid 归一化并按权重 $\alpha$ 融合，只有分数超过阈值 $\tau$ 的规则才被保留。

<div class="method-step__io" markdown="1">

**输入**：候选规则 $r$、自回归语言模型 $M$、事实记忆库 $\mathcal{M}_{F}$ 及规则相关证据 $T_{E}^{(r)}$。<br>
**输出**：经过语言先验和事实支撑双重检验的规则记忆库 $\mathcal{M}_{R}$。

</div>

**直观理解**：仅凭语言模型觉得“这句话听起来合理”可能会接受错误的概括，所以还要检查真实对话事实是否能支持它。RPC 像一个双重质检器：规则既要自洽，也要有记忆中的证据，低于门槛的规则会被淘汰。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 规则引导的问答推理

系统先将问题与规则结论进行向量相似度匹配，选出候选规则 $\mathcal{R}_{\mathrm{active}}$；再用规则前件作为检索线索，从 $\mathcal{M}_{F}$ 召回候选事实。大语言模型依据问题中的实体和规则中的类型约束执行语义统一，过滤实体绑定错误的事实，最后把问题、规则和已验证证据组织进结构化提示词，生成显式推理答案。

<div class="method-step__io" markdown="1">

**输入**：新问题 $Q$、规则记忆库 $\mathcal{M}_{R}$、事实记忆库 $\mathcal{M}_{F}$ 及生成模型。<br>
**输出**：由规则模板和经过实体约束的事实证据共同支持的答案。

</div>

**直观理解**：回答时不是直接拿问题去匹配表面相似的聊天句子，而是先问“这个问题适用哪种推理模板”，再根据模板需要寻找前提事实。这样可以找到措辞距离较远但逻辑上相关的证据，并减少把不同人物或事件混在一起的错误。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 自然语言 Horn 规则

$$
r:\;\underbrace{B_{1}\;\wedge\;\cdots\;\wedge\;B_{n}}_{\text{Body }T_{A}^{(r)},\;n\geq 1}\;\Longrightarrow\;\underbrace{H}_{\text{Head }T_{C}^{(r)}}
$$

**符号说明**

- $r$：规则记忆库中的一条规则。
- $B_i$：规则体中的第 $i$ 个自然语言关系原子，可能包含类型占位符。
- $n$：规则体中原子的数量，满足 $n\geq 1$。
- $T_{A}^{(r)}$：规则 $r$ 的前件或规则体，即 $B_1\wedge\cdots\wedge B_n$。
- $H$：规则头中的单个自然语言关系原子，即规则要推出的结论。
- $T_{C}^{(r)}$：规则 $r$ 的结论文本，即 $H$。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把多条同时成立的前提连接成一个结论：只有规则体中的所有条件都满足，才可以推出规则头。与记忆某一条具体对话不同，它描述的是可以迁移到其他实体和事件上的推理模式。<br>
**原文位置**：The RuleMem Framework，Bottom-Up Rule Memory Construction，Rule Induction，式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### Rule Perplexity Consistency 置信度

$$
\operatorname{RPC}(r)=\alpha\cdot\sigma\left(\ell_{M}(T_{C}^{(r)}\mid\varnothing)-\ell_{M}(T_{C}^{(r)}\mid T_{A}^{(r)})\right)+(1-\alpha)\cdot\sigma\left(\ell_{M}(T_{C}^{(r)}\mid T_{A}^{(r)})-\ell_{M}(T_{C}^{(r)}\mid T_{A}^{(r)}\oplus T_{E}^{(r)})\right)
$$

**符号说明**

- $\operatorname{RPC}(r)$：规则 $r$ 的最终 RPC 置信度分数。
- $\ell_M(T\mid C)$：自回归模型 $M$ 在上下文 $C$ 条件下预测目标文本 $T$ 的平均负对数似然。
- $M$：用于计算文本可预测性的自回归语言模型，原文举例为 Llama-3-8B-Instruct。
- $T_{C}^{(r)}$：规则 $r$ 的结论文本。
- $T_{A}^{(r)}$：规则 $r$ 的前件或规则体文本。
- $T_{E}^{(r)}$：从事实记忆库检索到、与规则 $r$ 相关的外部事实证据。
- $\varnothing$：空上下文，表示不提供规则前件。
- $\oplus$：上下文拼接操作，将前件与事实证据组合起来。
- $\alpha$：内部一致性信号的权重，取值范围为 $[0,1]$；$1-\alpha$ 是外部事实一致性信号的权重。
- $\sigma$：Sigmoid 函数，用于把似然下降量归一化到 $(0,1)$ 范围。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项衡量给出规则前件后，模型是否更容易接受结论；第二项衡量再加入真实事实后，结论是否进一步变得容易预测。两个下降量越大，规则越可能既符合推理语言先验又受到对话事实支持。<br>
**原文位置**：The RuleMem Framework，Rule Validation via RPC，式（2）—（3）及 RPC 定义

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未描述针对 RuleMem 进行参数更新或端到端梯度训练，也未给出传统意义上的训练损失。规则由大语言模型通过路径过滤、抽象和提示式归纳产生；RPC 使用语言模型的平均负对数似然计算验证分数，并以阈值 $\tau$ 筛选规则，因此该方法的核心是记忆构建、规则筛选和推理时提示编排，而不是训练一个新的参数化模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双层规则—事实记忆**

事实记忆库 $\mathcal{M}_{F}$ 存储时间四元组及其对话依据，规则记忆库 $\mathcal{M}_{R}$ 存储从具体路径抽象出的自然语言 Horn 规则。前者提供可追溯的情景事实，后者提供可迁移的推理结构，二者在构建阶段由事实指向规则，在问答阶段由规则反向指向事实。

> 直观理解：单独保存事实只能记住发生过什么，单独保存规则又可能缺乏真实依据。两层记忆让系统同时拥有“经历过的细节”和“从经历中总结的做法”。

**2. 基于大语言模型的路径归纳与语义统一**

大语言模型一方面过滤随机游走产生的无效路径并重建连贯推理链，另一方面将相似路径概括为带有 $[Person]$、$[Event]$、$[Location]$ 等类型占位符的规则。在问答时，它还依据问题实体和类型约束执行近似变量绑定，过滤违反规则条件的候选事实。

> 直观理解：随机游走只能机械地产生可能的连接，模型负责判断哪些连接真的有意义。问答阶段的语义统一则像核对姓名和类别，避免规则虽然匹配，但证据属于错误的人或事件。

**3. Rule Perplexity Consistency**

RPC 将规则结论的平均负对数似然变化分成内部一致性和外部事实一致性两部分，并通过 $\operatorname{RPC}(r)=\alpha\sigma(\Delta_{\mathrm{self}}(r))+(1-\alpha)\sigma(\Delta_{\mathrm{fact}}(r))$ 融合。规则只有在该分数超过阈值 $\tau$ 时才进入可用规则记忆。

> 直观理解：规则验证同时回答两个问题：语言模型在看到前件后是否更容易接受结论，以及加入真实对话证据后是否更容易接受结论。这个设计针对规则归纳可能过度泛化的问题。

**训练与推理**

构建阶段先从长期对话抽取时间事实并存入 $\mathcal{M}_{F}$，再在事实图上进行受约束随机游走，利用大语言模型过滤和重建有效推理路径，最后将关系模式相似的路径归纳为带类型占位符的自然语言 Horn 规则。对每条候选规则，系统从 $\mathcal{M}_{F}$ 检索相关证据，计算内部和外部困惑度下降量，利用 RPC、权重 $\alpha$ 和阈值 $\tau$ 形成最终规则记忆库 $\mathcal{M}_{R}$。推理阶段先将问题 $Q$ 与规则头进行向量相似度匹配，选取 Top-$N$ 规则；再依据规则体从事实库选取 Top-$K$ 候选事实，并由大语言模型按照问题实体和类型约束执行语义统一。最终，系统把问题、激活规则和已过滤证据放入结构化提示词，由生成模型输出显式推理答案。原文未明确报告规则归纳或 RPC 过程是否使用独立训练集进行参数学习。

**复现信息**

复现所需的关键设置包括：事实表示为主体、关系、客体、时间组成的四元组；候选路径通过受约束随机游走获得，并保留相应原始对话片段；规则使用自然语言 Horn 子句和类型占位符表示；RPC 的示例自回归模型为 Llama-3-8B-Instruct，规则采用阈值 $\tau$ 进行准入，$\alpha$ 控制两类一致性信号的平衡。问答使用规则头匹配问题、使用规则体召回事实，再进行基于实体和类型约束的 LLM 过滤；原文未明确报告 Top-$N$、Top-$K$、嵌入模型、阈值具体数值、提示词完整内容及候选路径采样规模。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- LoCoMo：长期对话记忆基准，共含5,882个对话轮次和1,986个问题。实验按Single-hop、Multi-hop、Open-domain等问题类型评估，是正文比较14种基线、分析证据召回和开展消融实验的主要数据集；摘录未说明训练、验证与测试划分。
- LongMemEval_s*：MemoryAgentBench的一个子集，被重新组织为5条长对话序列，总长度约182万token、共300个问题，用于检验极长上下文中的任务特定准确率。具体结果仅在附录报告，当前摘录无法核查其分任务表现或与基线的差距。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

衡量最终答案是否被评测脚本判定为正确；LoCoMo使用与Mem0仓库一致的评测实现，LongMemEval_s*则报告任务特定准确率。 （越高越好，因为它直接反映回答正确的比例。）

</div>
<div class="metric-item" markdown="1">

**F1**

综合答案与参考答案之间的精确率和召回率，适合衡量答案内容重合程度。 （越高越好，因为它表示模型在避免无关内容和覆盖参考信息之间取得更好平衡。）

</div>
<div class="metric-item" markdown="1">

**BLEU**

根据候选答案与参考答案的$n$-gram重合度衡量生成质量；它更偏向表面措辞匹配，不等同于逻辑正确性。 （越高通常表示生成文本与参考答案更相似，但不能单独证明推理过程正确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### LoCoMo总体结果（RQ1）

<div class="result-value" markdown="1">

RuleMem在四类问题上的平均BLEU为36.90，平均准确率为78.05，作者据此认为规则记忆对复杂对话推理有效。

</div>

总体结果表明，将历史对话抽象为规则并让规则同时参与检索和作答，在所用评测协议下优于仅存储或组织事实的整体范式。BLEU和准确率衡量的是最终输出，不能单独区分增益来自规则质量、额外模型调用、提示设计还是检索范围变化；由于当前摘录缺少Table 1完整数值，也无法逐项复核相对全部14个基线的优势。

<div class="result-source" markdown="1">

来源：Main Results (RQ1), Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 1, RuleMem demonstrates strong overall performance across the four question types, with an average BLEU of 36.90 and accuracy of 78.05.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### LoCoMo支持事实召回分析：启用Guided Recall（RQ2）

<div class="result-value" markdown="1">

在使用LoCoMo人工标注支持事实的分析中，Guided Recall使各框架的平均召回率从0.56提高到0.79，相对提升41.1%。

</div>

这一比较直接测试规则前件能否作为附加检索条件：当问题措辞与证据在语义或关键词上相距较远时，规则先指出回答所需的前提类型，再据此寻找事实。结果支持其缓解召回失败，但只证明更多标注支持事实被取回，并不保证这些事实一定相关、规则一定可靠，或最终答案必然正确。

<div class="result-source" markdown="1">

来源：In-depth Analysis (RQ2), Figure 3(a)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Using LoCoMo’s (Maharana et al. 2024) manually annotated supporting facts, Fig. 3(a) shows that Guided Recall consistently improves recall rates across all frameworks, raising the average recall from 0.56 to 0.79 (+41.1%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### LoCoMo推理失败分析：启用Explicit Reasoning（RQ2）

<div class="result-value" markdown="1">

在已经成功检索事实、但最终回答仍错误的样本定义下，Explicit Reasoning使平均推理失败数从120.4降至105.9，下降12.0%，其中Mem0g的降幅最大。

</div>

该实验尽量固定“已经找到了证据”这一条件，从而检验把抽象规则注入生成阶段是否能提供清晰的逻辑骨架。失败数下降说明规则可能帮助模型组织多步依赖；不过这是失败案例的绝对数量，仍会受到样本规模和“成功检索”的判定方式影响，而且没有无规则但等长度提示等更细控制，不能完全排除提示信息量增加带来的收益。

<div class="result-source" markdown="1">

来源：In-depth Analysis (RQ2), Figure 3(b)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Fig. 3(b), Explicit Reasoning consistently reduces reasoning failures from an average of 120.4 to 105.9 (-12.0%), with the largest reduction observed in Mem0g.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前正文摘录没有给出Table 1完整结果、LongMemEval_s*详细成绩以及三种基础模型的逐项数据，因而无法独立核查对14个基线的整体领先幅度、超长上下文上的泛化程度和跨模型稳定性。
- 规则可能过度泛化并压过明确事实，尤其容易误处理否定、例外和局部条件。现有消融说明RPC有帮助，但失败案例表明RPC并未完全解决规则—事实冲突；同时摘录未报告统计显著性、多次运行方差、延迟、存储量或额外LLM调用成本，因此尚不能判断收益的稳定性与部署代价。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 事实记忆方法：Mem0、LangMem与Letta，主要按相似度存取具体事实。它们用于检验“把历史当作事实集合”是否足以支持跨片段推理。
- 结构化事实记忆方法：A-MEM、Mem0g、MemoryBank、MemInsight、Zep与SCM，通过图结构、关联关系或组织策略管理记忆。它们用于判断RuleMem的收益是否只是来自更好的记忆组织，而非抽象规则。
- 传统检索与代理式RAG：BM25和ReAct，分别代表词项匹配检索与带行动—推理循环的检索代理，用于比较规则引导召回和常规文本检索。
- 图式或结构化RAG：MetaKGRAG、LightRAG与GraphRAG，用于检验图关系检索能否替代RuleMem所提供的可复用逻辑“主要前提”。

**实验想回答的问题**

- RQ1：RuleMem在长期对话问答中，相比事实记忆、结构化记忆与RAG类方法，能否提高答案准确性和生成质量，尤其是在需要跨片段、多步推理的问题上？
- RQ2—RQ3：Guided Recall与Explicit Reasoning是否分别缓解证据召回失败和推理失败，以及这些收益对RPC超参数和不同基础语言模型是否稳健？

**实验实现**

正文实验使用gpt-4o-mini完成规则抽象与最终显式推理；事实和规则的向量表示存入ChromaDB，默认嵌入模型为all-MiniLM-L6-v2。RPC规则准入阈值设为$\tau=0.5$，内部语言先验与外部事实信号的平衡系数设为$\alpha=0.4$。除非另有说明，基线采用官方代码仓库及默认参数。LoCoMo严格沿用Mem0的脚本和指标，LongMemEval_s*沿用MemoryAgentBench的原始评测；提示模板、完整配置及扩展结果位于附录。该设计提高了协议可比性，但摘录未提供重复运行次数、随机性控制、显著性检验或计算成本。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除规则抽象、RPC验证与显式规则推理：w/o Rule+RPC | 该变体退化为标准事实组织记忆，正文称其性能严重下降并接近事实组织类基线；当前摘录未明确报告各指标的具体数值。 | 这一变体主要隔离“高层规则记忆整体”是否必要。明显退化支持规则并非可有可无，但它同时删除规则抽象和显式推理等多个环节，因此不能进一步判断性能主要由规则生成、规则检索还是规则注入回答阶段贡献。 | In-depth Analysis (RQ2), Ablation study; Table 1底部<br><span class="experiment-evidence">Removing rule abstraction (w/o Rule+RPC) causes a severe performance drop, reducing metrics to levels similar to baseline fact-organization methods.</span> |
| 保留规则但移除RPC可靠性过滤：w/o RPC | 将所有诱导规则无筛选写入记忆后，性能下降；当前摘录未明确报告下降幅度。 | 该消融更直接隔离RPC准入检查的价值：如果保留规则机制却因取消过滤而退化，说明错误、幻觉或过度泛化规则会污染后续召回和推理。不过实验只比较“有无RPC”，没有分别控制规则数量与平均质量，因此尚不能确定收益究竟来自一致性验证本身，还是来自减少规则库规模。 | In-depth Analysis (RQ2), Ablation study; Table 1底部<br><span class="experiment-evidence">Similarly, the absence of RPC filtering (w/o RPC) also degrades performance, as unfiltered, erroneous, or hallucinated rules interfere with the deduction process.</span> |

**定性案例**

- 失败案例揭示规则覆盖具体事实的风险：对“在James参加的组织做志愿者是否需要面试”这一问题，对话明确说“No, this is not necessary.”，但系统激活了“友好且礼貌的人可能通过面试”这一泛化规则，最终错误回答需要面试。这个案例说明规则即使在一般情形下合理，也不能替代当前对话中的直接、否定性证据；系统需要冲突检测或事实优先策略，使明确事实在与抽象规则矛盾时拥有更高权重。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出面向长期对话智能体的主动规则记忆，以归纳的逻辑规则共同指导证据检索与回答推理。; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`10e06b7bebac540d850c6d64ed700019c09d7a4d33f1611a2ef97eea72b41def`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
