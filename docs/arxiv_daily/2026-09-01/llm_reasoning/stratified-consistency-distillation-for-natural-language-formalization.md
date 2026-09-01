---
title: "[论文解读] Stratified Consistency Distillation for Natural Language Formalization"
description: "[arXiv 2608.30258][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.30258"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:47:15.020438+00:00"
source_sha256: "442b9fee7447b14d4c9a290a22b6a4ee21ae5f8b3f7885723497a5be59d49774"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "自然语言形式化"
  - "SMT-LIB"
  - "神经符号推理"
  - "大型语言模型"
  - "一致性蒸馏"
  - "逻辑翻译"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.30258</p>

# Stratified Consistency Distillation for Natural Language Formalization

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Zhichao Hou, Ferhat Erata, Joe Lilien, MohamadAli Torkamani</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: North Carolina State University；Affiliation: Amazon Web Services</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30258v1) · [PDF 下载](https://arxiv.org/pdf/2608.30258v1) · **关键词** 自然语言形式化, SMT-LIB, 神经符号推理, 大型语言模型, 一致性蒸馏, 逻辑翻译<br>


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

本文位于神经符号推理与自然语言形式化（autoformalization）交叉领域。其核心任务是把人类用自然语言描述的政策、合规或规则内容转换为可由符号求解器验证的形式逻辑表示，具体采用 SMT-LIB（一种面向可满足性模理论的标准化输入语言），并使用 Z3 等自动定理证明器检查逻辑正确性。LLM 具备较强的自然语言理解和生成能力，但可能产生事实错误或逻辑不一致；因此，本文关注如何以较低推理成本，使较小的语言模型可靠地完成自然语言到 SMT-LIB 的翻译，而不只依赖大型闭源模型的提示工程。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自然语言形式化（autoformalization）**

自然语言形式化是把含义灵活、可能有歧义的人类语言转换成语法严格且可验证的形式逻辑表达式。形式化之后，符号求解器可以检查不同公式是否满足同样的逻辑约束。

</div>
<div class="concept-item" markdown="1">

**SMT-LIB 与符号求解器**

SMT-LIB 是描述变量、声明、逻辑规则和约束的统一格式；Z3 是能够读取这类公式并判断其可满足性或逻辑关系的符号求解器。直观地说，语言模型负责把文字写成机器可检查的规则，求解器负责执行严格的逻辑检查。

</div>
<div class="concept-item" markdown="1">

**语义等价与 Pass@10**

若两个 SMT-LIB 公式在逻辑上表达相同的约束，即使表面写法不同，也可称为语义等价。Pass@10 表示模型为同一个输入生成十个候选翻译时，只要其中至少一个与参考公式逻辑等价，该样本就计为通过。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定自然语言提示 $\mathbf{p}$，其中可包含任务指令、上下文以及问题—回答对，模型需要输出准确表达其逻辑语义的 SMT-LIB 完成结果 $\mathbf{t}$。训练数据集记为 $\mathcal{D}$，其中每个样本是配对的 $(\mathbf{p},\mathbf{t})$；参数为 $\theta$ 的语言模型记为 $\mathbb{LM}_{\theta}$。本文的应用设定主要是从政策文档中提取声明、变量和规则，生成自然语言问题—回答对，再建立自然语言输入与 SMT-LIB 输出之间的对应关系。理想输出必须同时满足 SMT-LIB 的语法要求和源文本的逻辑语义；评估既包括严格的逻辑等价检查，也包括衡量部分结构一致性的连续相似度。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathbf{p}$**

自然语言提示，可能包含任务说明、语义上下文和问题—回答内容。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{t}$**

与自然语言提示对应的目标 SMT-LIB 翻译或完成结果。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{D}$**

训练数据集，由自然语言提示与其 SMT-LIB 目标翻译组成的配对样本构成。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{S}$**

翻译质量函数，用于衡量模型输出与目标公式之间的精确逻辑等价性或连续逻辑相似度。

</div>

</div>

**直接相关的工作**

- **提示工程与链式思维（Chain-of-Thought）**: 已有研究通过少样本提示和链式思维引导大型语言模型完成复杂推理或翻译，但本文指出，依赖前沿模型提示的方案难以扩展到不同领域和输入格式，并且推理成本高、通常无法对闭源模型进行微调。本文转而通过一致性蒸馏，把前沿模型产生的逻辑翻译知识迁移给较小的开源模型。
- **监督微调、RLHF 与数学形式化**: 监督微调和基于人类反馈的强化学习已被用于提升一般推理能力，自动形式化也已应用于 Coq、Lean、Isabelle 等证明系统以及一阶逻辑和算术框架。然而，现有工作对自然语言直接翻译为 SMT-LIB 的研究仍较少；本文将这一未充分研究的方向作为任务对象，并结合政策文档构造训练数据。

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

该方法面向自然语言到 SMT-LIB 逻辑公式的形式化任务。输入是包含任务指令、上下文、少样本示例以及问答内容的自然语言提示 $\mathbf{p}$，输出是能够表达其逻辑语义的 SMT-LIB 完成文本 $\mathbf{t}$。核心思想不是直接相信教师模型的一次生成，而是让前沿大语言模型对同一输入生成多个候选，将逻辑等价的候选归为同一簇，再依据候选分歧程度选择、统一或放弃伪标签，最后用这些伪标签通过 LoRA 微调较小的学生模型。

从技术上看，方法将“生成不确定性”转化为“语义等价簇上的熵”：若多个候选集中表达同一逻辑含义，则采用最大簇中的候选；若存在中等歧义，则让教师模型在前两个候选簇之间判断；若歧义过高，则尝试统一候选，无法可靠统一时 abstain，即不使用该样本。直观地说，这类似于先让一组专家独立作答，再判断他们是在用不同措辞表达同一答案，还是确实对答案存在分歧，最后只把较可信的答案教给小模型。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 政策语义与合成样本构造

首先由大语言模型从政策文档中抽取语义上下文，并构造包含 SMT-LIB 声明、变量和政策规则的语义模型；随后基于该上下文生成自然语言问题—答案对，并将问题—答案内容与语义上下文共同放入翻译提示中。

<div class="method-step__io" markdown="1">

**输入**：源政策文档及其相关声明、变量和规则。<br>
**输出**：自然语言提示与对应 SMT-LIB 翻译组成的训练样本，格式为 `<Natural Language Prompt> → <SMT-LIB Completion>`。

</div>

**直观理解**：先把政策文件整理成机器可用的“词汇表、变量表和规则表”，再据此编写接近真实用户对话的问题与答案，避免形式化样本脱离原始政策语境。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 教师模型冗余生成

从前沿教师模型 $\mathbb{LLM}$ 的预测分布中采样 $M$ 个 SMT-LIB 翻译 $\{\mathbf{t}^{(1)},\mathbf{t}^{(2)},\ldots,\mathbf{t}^{(M)}\}$。论文概览图说明每个训练样本生成 10 个翻译，并以 Claude Sonnet 3.7 作为示例教师模型。

<div class="method-step__io" markdown="1">

**输入**：待翻译提示 $\mathbf{p}$，包括任务指令、必要上下文、少样本示例和问答内容。<br>
**输出**：同一自然语言输入对应的多个 SMT-LIB 候选翻译。

</div>

**直观理解**：不只问教师一次，而是让它在相同问题上独立作答多次；重复答案可以暴露模型稳定相信的逻辑含义，分歧答案则提示潜在错误或歧义。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 逻辑等价聚类与语义熵估计

使用 `check_smt_equivalence` 调用 Z3，检查两个 SMT-LIB 表达式在给定声明下是否逻辑等价，并据此把候选划分为等价类 $\mathcal{C}$。根据各等价簇的归一化概率计算符号语义熵，熵越高表示候选的逻辑含义越分散。

<div class="method-step__io" markdown="1">

**输入**：同一输入产生的 $M$ 个 SMT-LIB 候选，以及候选所需的声明。<br>
**输出**：等价簇集合 $\mathcal{C}$、各簇概率以及每个输入的熵值 $e_i$。

</div>

**直观理解**：表面写法不同并不一定代表答案不同，因此先用定理证明器判断“意思是否相同”，再统计不同意思各自获得多少支持，而不是简单按字符串投票。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分层伪标签选择

低熵样本选择最大等价簇中的翻译；中熵样本让前沿教师作为裁判，在前两个等价簇中选择；高熵样本尝试统一前两个候选翻译，若无法得到可靠统一结果则放弃该样本。

<div class="method-step__io" markdown="1">

**输入**：输入 $\mathbf{p}_i$、候选集合 $\{\mathbf{t}_i^{(j)}\}_{j=1}^{M}$、等价簇及熵值 $e_i$。<br>
**输出**：筛选后的伪标签数据集 $\{(\mathbf{p}_i,\mathbf{t}_i)\}_{i=1}^{N}$。

</div>

**直观理解**：确定性高时采用多数意见，存在一定争议时请更强的教师复核，争议极大时宁可不教这个例子，也不把可能错误的答案写入训练集。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### NL2SMT 目标函数

$$
\max_{\theta}\mathbb{E}_{({\mathbf{p}},{\mathbf{t}})\sim\mathcal{D}}\left[\mathcal{S}\left(\mathbb{LM}_{\theta}({\mathbf{p}}),{\mathbf{t}}\right)\right]
$$

**符号说明**

- $\theta$：学生语言模型的可训练参数。
- $\mathcal{D}$：由自然语言提示与其 SMT-LIB 目标翻译组成的训练数据分布。
- ${\mathbf{p}}$：输入自然语言提示，可包含指令、上下文和问答对。
- ${\mathbf{t}}$：与提示逻辑语义对应的 SMT-LIB 翻译。
- $\mathbb{LM}_{\theta}({\mathbf{p}})$：参数为 $\theta$ 的语言模型对提示 $\mathbf{p}$ 生成的翻译。
- $\mathcal{S}$：生成翻译与目标翻译之间的相似度，可表示精确逻辑等价或连续逻辑相似度。

<div class="equation-explanation" markdown="1">

**直观理解**：训练目标是让模型生成的公式尽可能接近目标公式，且“接近”不只限于字符串相同，也可以依据逻辑等价或共享的逻辑结构衡量。该目标说明蒸馏最终仍服务于 NL2SMT 翻译质量，而不是单纯复制教师的文字形式。<br>
**原文位置**：第 2 节 Preliminary，公式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 符号语义熵

$$
\operatorname{SE}({\mathbf{p}})=-\sum_{i=1}^{|\mathcal{C}|}P(\mathcal{C}_{i}\mid{\mathbf{p}})\log P(\mathcal{C}_{i}\mid{\mathbf{p}})
$$

**符号说明**

- $\operatorname{SE}({\mathbf{p}})$：给定提示 $\mathbf{p}$ 时，不同逻辑等价簇之间的语义不确定性。
- $\mathcal{C}$：由逻辑等价关系划分得到的候选翻译簇集合。
- $\mathcal{C}_i$：第 $i$ 个逻辑等价簇。
- $P(\mathcal{C}_i\mid\mathbf{p})$：给定提示 $\mathbf{p}$ 时候选落入第 $i$ 个等价簇的归一化概率。
- $|\mathcal{C}|$：等价簇的数量。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把多个文本候选压缩为多个“逻辑答案簇”，再测量概率分布有多分散。若几乎所有概率集中于一个簇，熵低且可以信任多数意见；若概率分散到多个簇，熵高，选择伪标签时应更加谨慎。<br>
**原文位置**：第 3.1 节 Equivalent Clustering & Symbolic Semantic Entropy

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：论文将 NL2SMT 学习表述为最大化模型生成结果与目标 SMT-LIB 翻译之间的期望相似度：优化参数 $\theta$，使 $\mathcal{S}(\mathbb{LM}_{\theta}(\mathbf{p}),\mathbf{t})$ 在数据分布 $\mathcal{D}$ 上尽可能大。实际蒸馏阶段，原始人工目标被流程生成的筛选伪标签 $\mathbf{t}_i$ 替代，并通过 LoRA 微调学生模型；摘录未明确报告具体的 token-level 交叉熵形式、优化器、学习率或伪标签加权方式，因此不能进一步推断训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 基于 Z3 的 SMT-LIB 语义等价聚类**

方法定义等价检查函数 $\mathbb{E}(\cdot,\cdot)$，在给定声明下比较两个 SMT-LIB 表达式。函数构造蕴含树，将待检验条件写入 SMT-LIB 文件，并检查否定等式条件的可满足性；Z3 返回 `unsat` 时判定两个表达式逻辑等价。候选按该等价关系增量归类：若新候选与已有簇中的任一成员等价，则加入该簇，否则新建簇。

> 直观理解：这个模块识别的是逻辑含义而非文本表面形式。例如，规则重排或使用等价写法的两个公式应被视作同一答案，否则普通字符串聚类会错误地把它们分开。

**2. 符号语义熵与分层选择**

对等价簇的条件概率计算语义熵，并依据熵将样本划分为低、中、高三个区间。低熵使用最大簇进行自洽选择，中熵调用教师模型在前两个簇中裁决，高熵则执行前两个翻译的统一或 abstention；摘录内容没有给出三个熵区间的具体数值阈值。

> 直观理解：熵在这里表示“不同逻辑答案之间有多不一致”：一个答案占绝大多数时可以直接采用，答案势均力敌时需要复核，完全混乱时应避免把噪声当作知识。

**3. 前沿教师到小模型的 LoRA 蒸馏**

教师模型负责多次采样和部分伪标签裁决，学生模型则在筛选后的提示—SMT-LIB 对上进行参数高效微调。LoRA 通过学习低秩适配参数来改变学生模型行为；摘录仅明确说明使用 LoRA 微调 Qwen2.5-7B 示例模型，未报告其秩、目标层或具体损失实现。

> 直观理解：前沿模型被当作无法直接改造但能力较强的教师，小模型通过可靠示范获得其形式化能力，从而降低推理阶段的模型规模与调用成本。

**训练与推理**

训练流程为：从政策文档抽取语义上下文；生成自然语言问答及其初始 SMT-LIB 表示；对每个提示由前沿教师采样多个候选；使用 Z3 检查候选间逻辑等价性并构造等价簇；计算簇级语义熵；按低、中、高熵策略选择多数候选、教师裁决结果，或统一候选并在必要时放弃样本；将保留下来的 $\mathbf{p}_i$—$\mathbf{t}_i$ 对用于 LoRA 微调学生模型。

推理时，输入新的自然语言提示及其所需上下文，学生模型直接自回归生成 SMT-LIB completion。若要评估生成质量，可对同一输入生成多个候选，并使用 Z3 判断是否至少有一个候选与目标逻辑等价；当无法达到精确等价时，再以基于结构压缩和反统一的连续相似度衡量部分逻辑结构的一致性。这里的评估流程不应与训练时的伪标签筛选混同：前者检验模型输出，后者决定哪些教师输出可以用于训练。

**复现信息**

为加速教师模型的重复采样，论文使用 vLLM，这是一个高吞吐、内存高效的推理与服务引擎。教师模型示例为 Claude Sonnet 3.7，学生模型示例为 Qwen2.5-7B；论文概览描述每个训练样本生成 10 个 SMT-LIB 翻译，但正文同时以一般变量 $M$ 表示候选数。逻辑等价检查依赖给定 SMT-LIB 声明和 Z3，连续逻辑相似度使用 Egglog 从生成公式与目标公式中抽取反统一结构；摘录未明确报告熵阈值、统一算法细节、采样温度、LoRA 配置、训练轮数或推理解码参数。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- FOLIO：开放领域一阶逻辑推理基准，包含自然语言前提、结论以及用预定义逻辑声明构造的 $SMT$-LIB 断言；本文用于评估逻辑翻译质量。数据规模、训练/验证/测试划分未明确报告。
- NL2SMT 数据集：实验设置将其作为自然语言到 $SMT$-LIB 公式翻译框架或数据来源的一部分，但所给章节未明确报告其独立规模与划分。
- Customer Service 数据集：用于表 3 的聚类候选选择实验和表 4 的 SCD 消融实验；数据规模、划分及其具体任务构成原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Pass@K**

对每个输入生成 $K$ 个候选公式，只要至少一个候选通过逻辑等价检查就算成功；本文报告 $K=1,\ldots,10$。 （越高越好，因为它表示在多次生成中找到正确逻辑翻译的概率更高。）

</div>
<div class="metric-item" markdown="1">

**Binary Equivalence Check**

使用 $Z3$ 定理证明器判断生成的 $SMT$-LIB 公式是否与金标准公式逻辑等价，结果是二值正确/不正确。 （等价判定为真越多越好；该指标严格反映精确逻辑等价，但不能区分两个都不等价的候选之间的部分接近程度。）

</div>
<div class="metric-item" markdown="1">

**Continuous Similarity Score**

在未达到精确等价时，使用基于符号压缩和反统一（anti-unification）的 $Egglog$ 实现计算区间 $[0,1]$ 内的部分逻辑相似度。 （越高越好，表示生成公式与金标准在逻辑结构或符号表达上更接近；它不是精确等价的替代证明。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### FOLIO 上的 $Pass@10$ 主结果

<div class="result-value" markdown="1">

SCD 的 $Pass@10$ 为 55.208%，普通蒸馏为 50.347%，Qwen3-14B 少样本基线为 42.708%，Qwen2.5-7B-Instruct 少样本基线为 21.875%。因此，SCD 相比普通蒸馏高 4.861 个百分点，相比 Qwen3-14B 高 12.500 个百分点。

</div>

在十个候选中允许出现一次正确翻译时，SCD 找到逻辑等价公式的比例最高。该结果支持分层伪标签比直接使用普通蒸馏信号更有效，但不能单独证明 SCD 在所有领域、数据规模或解码设置下都优于更大模型。

<div class="result-source" markdown="1">

来源：第 4.2 节，表 1 后的结果分析

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

SCD achieves the best Pass@10 performance of 55.208%, exceeding Qwen3-14B by 12.500 percentage points and vanilla distillation by 4.861 percentage points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### FOLIO 上不同 $K$ 的整体比较

<div class="result-value" markdown="1">

SCD 在表 1 报告的 $Pass@K$ 指标中均高于所列少样本模型和普通蒸馏；例如 $Pass@1$ 为 44.097%，普通蒸馏为 39.931%，Qwen3-14B 为 42.708%，Qwen2.5-7B-Instruct 为 15.625%。

</div>

SCD 的优势不只来自允许十次采样这一特定设置，在单次生成到十次生成的报告范围内都保持较强表现。由于表 1 只给出通过率，没有提供方差、重复实验或统计显著性，因此结果稳定性的统计证据仍有限。

<div class="result-source" markdown="1">

来源：表 1，SCD 行；列顺序为 Pass@10 至 Pass@1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

SCD 55.208 55.208 54.514 52.778 50.083 49.653 48.958 47.917 46.528 44.097

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 推理延迟与质量的实际部署权衡

<div class="result-value" markdown="1">

在 P4d EC2 实例上，Qwen2.5-7B-Instruct 的 P50、P90、P99 延迟分别为 4.040、5.074、5.651 秒；Claude Sonnet 3.7 分别为 16.680、28.042、29.425 秒。作者报告前者的 P50 约快 4.1 倍，并且在三个百分位上均低于 Claude。

</div>

学生模型在本文测试环境下比专有模型响应更快，说明微调后的较小模型可能具有部署效率优势。不过该表没有给出 SCD 模型单独的延迟行，且延迟受硬件、服务配置、输出长度和并发量影响，因此不能把表中结果直接解释为 SCD 本身造成的速度提升。

<div class="result-source" markdown="1">

来源：第 4.3 节 Latency，表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Its P50 latency is 4.040 seconds, approximately 4.1× faster than the 16.680 seconds required by Claude Sonnet 3.7.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 数据与实验报告不完整：所给章节未明确报告 FOLIO、NL2SMT 和 Customer Service 的规模、训练/验证/测试划分、教师模型、候选数 $K$ 的具体生成设置以及重复实验方差，因而难以判断结果的统计稳健性与可复现性。
- 外部有效性仍有限：主结果集中在 FOLIO，消融集中在 Customer Service，且连续逻辑相似度依赖作者实现的 $Egglog$ 压缩与反统一程序；文中未给出该指标与人工判断或其他独立质量标准的相关性，也未报告跨领域、不同输入格式或更多逻辑语言上的验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Qwen2.5-7B-Instruct 少样本模型：与同规模学生模型比较，可检验微调和蒸馏是否带来增益。
- Qwen3-4B、Qwen3-8B、Qwen3-14B：不同参数规模的开源模型，用于考察模型规模与 SCD 的相对效果。
- Mistral-7B-Instruct：另一种开源约 7B 模型，可作为架构和预训练模型差异下的少样本基线。
- Claude Sonnet 3.7：专有前沿模型，用于提供较强教师式或商业模型参照；其延迟也被单独比较。

**实验想回答的问题**

- 在 $NL2SMT$ 任务中，分层一致性蒸馏（SCD）能否提升自然语言到 $SMT$-LIB 公式翻译的逻辑正确性，并超过少样本基线与普通蒸馏？
- 语义等价聚类的熵水平是否能作为选择伪标签策略的可靠信号，以及不同熵区间的选择策略是否影响蒸馏效果？

**实验实现**

学生模型为 Qwen2.5-7B-Instruct，采用 LoRA（低秩适配）进行参数高效微调；学习率为 $5\times10^{-5}$，批大小为 32，LoRA 秩为 32，缩放因子为 $\alpha=64$。评估时对候选 $SMT$-LIB 公式执行 $Z3$ 逻辑等价检查，并以 $Egglog$ 实现的 $SMT$-LIB 规范进行符号压缩与反统一，从而得到二值等价结果和连续相似度。少样本比较模型包括 Qwen2.5-7B-Instruct、Qwen3-4B、Qwen3-8B、Qwen3-14B、Mistral-7B-Instruct 和 Claude Sonnet 3.7。延迟在 P4d EC2 实例上报告 P50、P90 和 P99；所给章节未明确报告每个模型的生成次数、解码参数、数据规模、数据划分以及 SCD 训练样本数量。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Customer Service 数据集上的熵分层策略消融 | 表 4 中，Qwen2.5-7B 的 $Pass@10$ 为 17.593%，普通蒸馏为 27.469%，高熵 SCD 为 26.235%，低熵 SCD 为 28.704%，分层 SCD 为 31.481%。分层 SCD 在所报告的各个 $Pass@K$ 上均达到最高或并列最高。 | 该消融分别固定在高熵样本、低熵样本或按熵分层处理，用来隔离“不同不确定性水平采用不同标签选择策略”的作用。低熵样本优于高熵样本，表明教师输出更一致时监督更可靠；分层策略进一步超过单一熵区间，支持根据不确定性切换多数投票、评审或统一/弃权策略的设计。它没有单独拆分每一种具体选择器的贡献。 | 第 4.3 节 Stratified Consistency Distillation，表 4；列顺序为 Pass@10 至 Pass@1<br><span class="experiment-evidence">SCD (Stratified) 31.481 31.481 31.481 30.247 29.938 26.852 26.852 26.852 26.852 26.852</span> |
| Customer Service 数据集上的聚类候选选择消融 | Qwen2.5-7B 的随机 $Pass@1$ 为 13.889%，$Top@1$ 为 15.741%，$Top@2$ 为 17.593%；SCD 的随机 $Pass@1$ 为 24.074%，$Top@1$ 为 25.926%，$Top@2$ 为 30.556%，$Top@3$ 为 31.481%。 | 该实验测试从语义等价簇中选择候选，而不是随机取一个候选，是否能提高找到正确翻译的机会。$Top@1$ 的改进说明最大簇具有信息；$Top@2$ 的明显提升说明只看最大簇可能遗漏中等熵情况下的正确簇。这里的 $Top@k$ 是候选选择分析，并不等同于完整训练后的 $Pass@k$ 生成指标。 | 表 3，SCD 行；列顺序为 Pass@10、Pass@1 (Random)、Top@1、Top@2、Top@3<br><span class="experiment-evidence">SCD 31.481 24.074 25.926 30.556 31.481</span> |

**定性案例**

- 图 3 和图 4 的逐样本热图构成定性案例：预训练的 Mistral-7B-Instruct 和 Qwen2.5-7B-Instruct 有较多失败或低相似度区域，普通微调后正确覆盖扩大，采用一致性蒸馏后覆盖最广且相似度整体更高。该现象说明改进不仅体现在平均表格分数，也体现在更多具体样本上；但所给章节未提供单个样本的自然语言输入、生成公式、金标准公式或错误类型，因此无法进一步分析某一案例为何成功。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过一致性蒸馏提升LLM将自然语言形式化为逻辑表达式的能力，核心涉及神经符号推理。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`442b9fee7447b14d4c9a290a22b6a4ee21ae5f8b3f7885723497a5be59d49774`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
