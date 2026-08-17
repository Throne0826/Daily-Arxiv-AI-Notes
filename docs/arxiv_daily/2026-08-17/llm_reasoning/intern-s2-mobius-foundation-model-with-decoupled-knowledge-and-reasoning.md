---
title: "[论文解读] Intern-S2-Mobius: Foundation Model with Decoupled Knowledge and Reasoning"
description: "[arXiv 2608.14290][LLM Reasoning] 本文提出将知识存储与推理计算解耦的 Mobius-v0 架构，并据此构建 Intern-S2-Mobius，以提高基础模型的知识压缩能力、训练数据利用率和推理效率。"
arxiv_id: "2608.14290"
announcement_date: "2026-08-17"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-17T02:04:17.880222+00:00"
source_sha256: "7457da0613c78d7ff1308e61253e50f860fd9ef9fbbc5bc3b4dcb63ccdaef010"
tags:
  - "LLM Reasoning"
  - "知识与推理解耦"
  - "基础模型架构"
  - "知识向量"
  - "组合推理"
  - "高效推理"
  - "Transformer"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.14290</p>

# Intern-S2-Mobius: Foundation Model with Decoupled Knowledge and Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-17</span>
<span><strong>作者</strong> Kai Chen, Jifeng Ding, Ning Ding, Jiaye Ge, Lixin Gu, Yicheng Gu, Qipeng Guo, Ermo Hua, Haian Huang, Haozheng Hou, Jie Hou, Xiangyu Hong, Che Jiang, Minxi Jin, Cheng Liang, Dahua Lin, Dawei Liu, Kuikun Liu, Chengqi Lv, Haijun Lv, Han Lv, Ningsheng Ma, Biqing Qi, Jianmin Qian, Shiya Su, Youbang Sun, Huanze Tang, Zhongbo Tian, Hanjing Wang, Rui Wang, Ting Wang, Yi Wang, Baiting Wu, Jun Xu, Bowen Yang, Hui Wang, Weida Wang, Haochen Ye, Jiashuo Yu, Shan Yu, Xiaoyi Yu, Qirui Zeng, Qi Zhang, Ming Zhang, Wenwei Zhang, Bowen Zhou, Xinyu Zhou</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Intern-S2-Mobius Team, Shanghai AI Laboratory</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.14290) · [PDF 下载](https://arxiv.org/pdf/2608.14290) · **关键词** 知识与推理解耦, 基础模型架构, 知识向量, 组合推理, 高效推理, Transformer<br>


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

本文提出将知识存储与推理计算解耦的 Mobius-v0 架构，并据此构建 Intern-S2-Mobius，以提高基础模型的知识压缩能力、训练数据利用率和推理效率。

**不用术语来说**：常规基础模型往往让同一套网络参数同时承担“记住事实”和“组合已有信息完成推断”两类任务，可能造成知识被重复存储、推理过程计算冗余。本文关注的问题是：能否把模型的知识库与推理器分开设计，让推理器在需要时反复读取共享知识，从而以更少的训练数据获得相近能力，并显著加快生成时的端到端推理。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 Mobius-v0：使用全局共享的记忆模块 FFN 存储知识向量，并配置多个基于 Self-Attn 的推理器；推理器以隐藏状态作为缓存和信息载体，迭代查询记忆并执行组合推理。
- 验证该架构可用于从头训练与持续预训练：作者报告，从头训练的 7B 模型使用 Transformer 基线 62.6% 的训练数据即可获得相近下游得分；从 Qwen3.5-35B 持续预训练得到的 Intern-S2-Mobius 在保持相近下游得分的同时，实现接近 4 倍的端到端推理加速。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型架构与高效推理研究，核心关注如何在保持知识存储能力的同时降低组合推理的计算和训练成本。传统 Transformer 通常在同一层中同时使用前馈网络（FFN）处理知识变换，并使用自注意力（Self-Attention）建立 token 之间的关系；本文则考察一种知识与推理解耦的架构：让全局共享的 Memory 主要存储知识向量，让多个 Reasoner 主要执行迭代式组合推理，并通过隐藏状态在二者之间传递查询和返回结果。论文将该架构实例化为 Mobius-v0，并进一步构建从 Qwen3.5-35B 持续预训练得到的 Intern-S2-Mobius。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**Transformer**

Transformer 是当前大语言模型常用的神经网络架构，主要通过自注意力机制处理不同位置 token 之间的依赖关系，并通过前馈网络进行逐位置的非线性变换。本文把这两类功能分别对应到推理模块和知识存储模块。

</div>
<div class="concept-item" markdown="1">

**前馈网络（FFN）与知识向量**

FFN 接收每个位置的隐藏状态并进行非线性映射；在本文的设计中，Memory 由全局共享的 FFN 构成，其参数被视为存储知识的载体。知识向量可以理解为 Memory 根据当前隐藏状态检索或生成的、供后续推理使用的表示。

</div>
<div class="concept-item" markdown="1">

**自注意力（Self-Attention）与组合推理**

自注意力允许模型根据当前序列中各 token 的关系聚合信息。组合推理是指把多个已获得的信息按照问题需要逐步组合起来，本文用多个 Reasoner 反复执行这一过程。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定输入 token 序列，模型首先将其编码为隐藏状态；在每一轮推理中，Reasoner 根据隐藏状态确定当前所需的知识，向全局共享的 Memory 查询相应知识向量，再将返回的知识传回推理算子，以更新隐藏状态。多个 Reasoner 迭代执行该查询、传递和更新过程，最终输出用于语言建模或下游任务预测的结果。该设定的基本假设是，参数中长期存储的知识与依赖上下文、逐步组合信息的推理过程可以由不同模块承担；如果二者分离有效，则模型应在知识压缩、训练数据利用率或端到端推理速度方面优于同规模 Transformer 基线。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入 token 序列，具体长度或表示方式在所给章节中未明确报告。

</div>
<div class="notation-item" markdown="1">

**$h$**

模型在推理过程中使用的隐藏状态，同时承担向 Memory 发起知识查询以及携带返回知识的作用。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{Memory}$**

全局共享的知识存储模块，由 FFN 构成，负责根据隐藏状态提供所需的知识向量。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{Reasoner}$**

推理模块，由 Self-Attention 构成，负责利用隐藏状态和 Memory 返回的知识进行迭代式组合推理。

</div>

</div>

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大规模基础模型既需要容纳大量知识，又需要在回答问题时多步组合这些知识。若知识存储与推理操作紧密耦合，模型可能需要更多训练数据来形成同等能力，并在每一步推理中承担较高计算成本；因此，实际需求是在尽量维持下游性能的前提下，提高知识压缩和推理效率。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **标准 Transformer 基线**：原文将 7B Transformer 作为从头训练的对照架构，但所给节选未进一步描述其具体结构；从论文提出的对照关系看，该类模型没有采用 Mobius-v0 所强调的全局共享记忆与多个推理器之间的显式解耦。
- **常规持续预训练基础模型**：以已有基础模型参数为起点继续训练，使模型适应新的架构或数据。本文具体从 Qwen3.5-35B 出发构建 Intern-S2-Mobius，但所给节选未明确报告既有持续预训练方法如何组织知识存储与推理计算。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 知识存储与推理操作缺少显式分工，可能使不同推理步骤无法高效复用同一个知识存储模块，其后果是知识压缩和训练数据利用率受限。该项因果关系属于基于作者架构主张的分析，所给节选未提供更细致的机制实验。
- 常规架构的推理计算效率不足。作者以“相近下游得分但接近 4 倍端到端加速”说明存在显著优化空间，但节选没有给出基线名称、硬件、输入输出长度或吞吐量定义，因此不能据此判断加速具体来自哪些计算环节。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方案尚未在一个可训练的基础模型架构中明确实现并验证这样的分工：由单个全局共享的 FFN 统一保存知识向量，同时让多个 Self-Attn 推理器通过隐藏状态反复读取所需知识并进行迭代组合，而且还要证明该设计能够兼顾从头训练的数据效率与持续预训练后的端到端推理速度。

</div>
<div markdown="1"><span>核心问题</span>

将基础模型改造成“共享记忆负责知识、多个推理器负责迭代推断”的解耦系统后，是否能在保持与同规模或来源基线相近下游性能的同时，减少从头训练所需数据，并显著提升端到端推理速度？

</div>
<div markdown="1"><span>作者直觉</span>

可以把 FFN 理解为所有推理步骤共用的知识库，把 Self-Attn 理解为负责组织思路的操作器。隐藏状态记录当前推理进度；每个操作器只在需要时从同一知识库取回相关知识，再把结果写回隐藏状态供下一轮使用。这样，知识不必随不同推理阶段重复配置，而推理操作也能围绕当前状态迭代展开，因此有望以更紧凑的参数和计算方式复用知识。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Mobius 的核心做法是把 Transformer 中逐层绑定的知识存储与推理计算拆开：以全局共享的前馈网络（Memory）保存知识向量，以多个自注意力模块（Reasoners）执行组合推理。隐藏状态既是推理过程的缓存，也是访问共享知识库的查询载体；Reasoners 反复用隐藏状态检索所需知识，再把取回的信息写回隐藏状态，从而在潜在空间中迭代精炼，最后解码一个或多个后续词元。

这种结构允许任一推理模块访问同一套完整知识，而不必像标准 Transformer 那样依次穿过每层各自的前馈网络。直观地说，Transformer 更像每层各带一间资料室、信息只能沿层级向前传递；Mobius 则让多个推理员共享一个中央资料库，并可多轮查询和修正草稿。单次访问大型共享 Memory 会增加稀疏激活和内存访问压力，但作者主张，更灵活的激活路径、跨深浅层的信息访问及潜在空间迭代，可减少显式思维链和串行解码词元，从端到端角度抵消单次前向的额外成本。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 输入编码与隐藏状态初始化

模型将上下文表示为连续隐藏状态；该状态不只对应待预测词元，还充当后续推理循环中的缓存、知识查询向量和信息载体。原文没有给出初始化公式、位置编码方式或上下文掩码的具体实现。

<div class="method-step__io" markdown="1">

**输入**：已经分词的上下文序列，以及由嵌入层或前序计算产生的初始隐藏状态。<br>
**输出**：可供 Reasoners 和共享 Memory 共同处理的初始潜在表示。

</div>

**直观理解**：模型先把文字转换成可计算的内部草稿。此后主要修改这份内部草稿，而不是把每一步思考都立即写成自然语言。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### Reasoner 组织上下文并提出知识查询

多个以 Self-Attn 为核心的 Reasoners 建模状态之间的依赖关系，并据此形成对共享 Memory 的查询。Reasoners 是推理算子，重点在于组合和传播信息，而非分别保存一套层专属知识。

<div class="method-step__io" markdown="1">

**输入**：当前隐藏状态以及上下文中已有词元或潜在状态。<br>
**输出**：包含当前推理需求、可用于访问共享 Memory 的更新状态。

</div>

**直观理解**：自注意力先判断当前问题中哪些信息需要相互关联，再决定应该从中央资料库取出什么知识。它承担“怎样思考”，共享 Memory 承担“知道什么”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 共享 Memory 检索与跨层知识回注

所有 Reasoners 访问同一个 Memory，从中激活与当前状态相关的知识向量，并将检索结果回传给推理状态。由于 Memory 全局共享，浅层状态能够访问通常被视为深层知识的内容，深层状态也能重新利用浅层知识，形成作者所称的 Backward Residual Connection；但节选未提供其精确张量连接式。

<div class="method-step__io" markdown="1">

**输入**：Reasoners 产生的查询状态，以及全局共享的 FFN 知识向量库。<br>
**输出**：融合了任务相关知识的隐藏状态。

</div>

**直观理解**：资料不再被锁在某一层，任何推理阶段都可以回到同一个知识库查找。所谓“向后残差连接”并非让时间倒流，而是取消知识只能随网络深度单向取得的限制。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 潜在空间多轮迭代精炼

Reasoners 在少数层内重复“组织信息、查询 Memory、更新状态”的过程，使潜在表示持续精炼；每轮都能访问完整共享知识库，而不必为一次内部修正重新遍历全部模型层。不同词元可获得不同的内部计算量，多个未来词元也可共享这些高信息密度状态。

<div class="method-step__io" markdown="1">

**输入**：已融合共享知识的隐藏状态。<br>
**输出**：更紧凑、目标更明确的潜在表示，以及可供后续多词元预测使用的隐藏状态。

</div>

**直观理解**：模型先在内部反复修改答案草稿，直到关键信息较集中，再把结果说出来。这样可能把一部分原本需要长篇思维链表达的推理转移到连续向量中完成。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：所给节选没有展示 Mobius 的中心训练损失、监督信号组合或对应公式，因此不能确定其是否仅采用标准下一词元预测损失，也不能重建多词元预测、持续预训练、SFT 或 RL 的具体权重关系。可以确认的优化层面信息仅包括两条训练路线：其一是从头预训练约 7B 规模的 Mobius-v0，并与同规模 Transformer 比较数据效率；其二是从 Qwen3.5-35B 切换到 Mobius 架构后继续预训练，后续流程提及 SFT 与 RL。由于原文节选未给出目标函数和阶段衔接细节，本分析不补写公式。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 全局共享 Memory**

Memory 由全局共享的 FFN 构成，被描述为知识向量数据库；它替代了标准 Transformer 中知识向量随 FFN 分散并绑定于不同层的组织方式。大型共享库使单次推理激活较稀疏，并可能带来更高内存访问压力，但其目标是减少跨层知识的重复存储，并让所有 Reasoners 访问同一知识集合。

> 直观理解：它相当于全模型共用的一间中央资料库。共享可以避免多个层重复记忆同一事实，但每次从大库中找少量相关内容，对内存访问和工程实现提出了更高要求。

**2. Reasoners**

Reasoners 以 Self-Attn 为核心，负责对隐藏状态执行关系建模、知识查询和组合推理；多个 Reasoners 与共享 Memory 解耦，不再各自绑定独立 FFN。它们可在少数层组成的计算路径中反复更新潜在状态，由此提高知识访问频率和有效推理深度。

> 直观理解：Reasoner 是使用知识解决问题的计算单元。把它与 Memory 分开后，同一份知识可以被不同推理步骤反复调用，而不必在每一层复制一遍。

**3. 动态潜在推理与多词元解码**

隐藏状态在共享 Memory 与 Reasoners 之间循环，被连续精炼后共同支持多个未来词元；计算因此可从显式 CoT 词元转移到连续潜在状态。附录 E 使用 layerwise prediction lens，从每层隐藏状态分别观察 $t+1$ 至 $t+5$ 的预测，以分析中间表示是否逐渐与目标续写对齐。

> 直观理解：模型把一部分“思考过程”留在内部向量中，并让多个未来词共享这份思考结果。其目的不是简单截短答案，而是在输出前完成更密集的内部计算，从而减少重复推导和检查。

**训练与推理**

训练方面，论文采用“从头训练”和“架构迁移后持续训练”两种验证路径。从头训练用于隔离架构本身的数据效率：Mobius-v0 与 7B Transformer 基线在训练过程中比较 MMLU 表现。大规模路线则以 Qwen3.5-35B 为起点，将知识存储与推理算子改造成共享 Memory 加多个 Reasoners 的结构后继续预训练，并提及后续 SFT 和 RL；不过节选没有说明原模型 FFN 参数如何合并为共享 Memory、Reasoners 如何从原注意力层初始化，以及各训练阶段的数据与损失配置。

推理时，输入首先变成隐藏状态；Reasoners 对上下文关系进行建模，并反复查询全局共享 Memory，把获得的知识写回潜在状态。该循环可以在少数层内多次发生，使状态在完整知识库条件下持续精炼，再由较深阶段进行多词元解码。作者将端到端加速主要归因于更短的可见 CoT 和更高的信息密度，而不是声称每次 Memory 访问都更便宜；事实上，原文明确指出共享数据库会增加内存访问压力并降低单次前向效率。因此，该方法的效率判断必须同时考虑单次前向成本、潜在迭代次数、输出长度、多词元草案接受情况和总请求吞吐量。

**复现信息**

公平解释结果所需的关键实现信息有三点。第一，论文比较了约 7B 的从头预训练模型和由 Qwen3.5-35B 持续预训练得到的 Intern-S2-Mobius-35B，这两组实验回答的问题不同，不能把前者的数据效率直接当成后者加速结果的成因。第二，推理长度和案例中的词元数使用 Qwen3.5-35B tokenizer 计算；因此长度差异是在统一分词口径下得到的，但节选没有给出吞吐测试的硬件、批大小、上下文长度、生成上限或解码配置。第三，附录 E 在相同 teacher-forced context 下逐层解码隐藏状态，并观察标准位置 $t+1$ 与 MTP 位置 $t+2$ 至 $t+5$；颜色表示预测概率，黑框表示与目标续写一致。该分析可说明某个案例中的潜在表示精炼和草案接受现象，但不能单凭单例证明所有任务上都具有相同机制；架构连接图、共享 FFN 的尺寸与稀疏激活规则在所给节选中均未明确报告。

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

原文未明确报告，或这里不需要额外前置概念。

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 逐层潜在表示与目标对齐性：Mobius 与 Qwen3.5 在相同教师强制上下文下的比较

<div class="result-value" markdown="1">

作者观察到，Mobius 在中间层产生了更多可解释且与目标对齐的预测，其逐层预测呈现更连贯的语义轨迹；相比之下，基线的中间层预测稳定性较弱。原文未明确报告可量化的准确率或概率数值。

</div>

这说明 Mobius 的中间隐藏状态似乎更早形成了与任务相关的紧凑表示，并在后续层中沿着较一致的方向细化。它支持“潜在计算过程更有组织”的解释，但单个案例和定性图示不能证明这种优势在所有输入、所有层或总体测试集上都稳定成立。

<div class="result-source" markdown="1">

来源：Appendix E, Figure 8

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Mobius exhibits more interpretable, target-aligned predictions in its intermediate layers than the baseline.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 后续多词预测位置 $t+2$ 至 $t+5$ 的潜在迭代细化

<div class="result-value" markdown="1">

Mobius 的潜在迭代逐步改进后续位置的预测，并最终生成一个五词草稿且全部被接受；Qwen3.5 基线在第三个预测位置被拒绝，只保留两个词的被接受前缀。

</div>

在该示例中，Mobius 不仅预测下一个词，还能在潜在空间中持续改进多个后续位置，因此草稿序列的有效长度更长。该结果表明其多词预测过程可能受益于迭代式潜在推理，但由于原文提供的是示例性图示，不能将“五词对两词”直接解释为总体接受率或平均加速比。

<div class="result-source" markdown="1">

来源：Appendix E, Figure 8

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Further latent iterations progressively refine this representation and improve predictions at subsequent positions, ultimately yielding a fully accepted five-token draft.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 草稿接受结果：Mobius 与 Qwen3.5 基线

<div class="result-value" markdown="1">

在图示案例中，Mobius 的五词草稿被完整接受，而基线的草稿在第三个预测位置被拒绝，仅留下两个词的被接受前缀。原文未明确报告该现象在数据集层面的平均接受长度或显著性检验。

</div>

草稿完整接受意味着验证阶段无需回退或截断该五词序列；基线较早被拒绝则意味着只有前两个词可以保留。这个案例直接展示了 Mobius 可能对多词预测和推理效率有帮助，但它只反映一个可视化示例，不能单独证明整体生成速度、质量或泛化性能提升。

<div class="result-source" markdown="1">

来源：Figure 8 caption

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Mobius exhibits more target-aligned intermediate predictions and produces a five-token draft accepted in full, while the baseline produces only a two-token accepted prefix.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所提供的实验摘录仅包含 Appendix E 的逐层分析和 Figure 8 的单个定性案例，原文未明确报告数据集、样本规模、数据划分、评测指标及总体统计结果，因此无法据此判断 Mobius 的优势是否具有广泛的统计稳定性。
- 该比较只给出了 Mobius 与 Qwen3.5 基线的示例性预测和接受长度，未在摘录中控制或分析模型规模、训练数据、推理配置等潜在混杂因素；因此“更紧凑的内部表示”和“更高效的多词预测”目前应视为作者提出的解释性推断，而非由该案例单独证实的因果结论。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Qwen3.5 基线：与 Mobius 使用相同教师强制上下文进行逐层预测比较，用于检验两种模型在潜在计算过程中的预测轨迹和多词草稿接受情况是否不同。

**实验想回答的问题**

- 在相同的教师强制上下文下，Mobius 的逐层隐藏状态预测是否比 Qwen3.5 基线更稳定、更贴合目标续写？
- Mobius 的潜在推理迭代是否能够逐步改进多位置预测，并提高草稿序列被完整接受的可能性？

**实验实现**

实验采用逐层预测透镜（layerwise prediction lens）分析潜在推理过程。给定相同的教师强制上下文，研究者在每一层读取隐藏状态，并分别解码标准的下一个词位置 $t+1$ 以及四个后续的多词预测位置 $t+2$ 至 $t+5$。图中每个单元格表示对应隐藏状态视图产生的预测词，颜色深浅表示该词的预测概率，黑色边框表示预测与目标续写一致。实验同时比较草稿序列的接受长度：Mobius 产生的五词草稿被完整接受，基线仅有两个词构成被接受前缀。原文未明确报告数据集、样本规模、数据划分、具体数值指标、推理参数或统计汇总。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- Figure 8 展示了一个相同教师强制上下文下的逐层预测案例：Mobius 的中间层预测更贴合目标续写，潜在迭代后形成五词草稿并全部被接受；Qwen3.5 的预测轨迹较不稳定，并在第三个预测位置被拒绝。该案例用于直观说明潜在空间中的逐步细化可能如何改善多词预测，而不是作为总体性能统计。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work proposes a foundation-model architecture that explicitly decouples stored knowledge from reasoning capabilities.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`7457da0613c78d7ff1308e61253e50f860fd9ef9fbbc5bc3b4dcb63ccdaef010`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
