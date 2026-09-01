---
title: "[论文解读] LCoT-GV: Graph Attention Networks for Verifying Long Reasoning Chains in Large Language Models"
description: "[arXiv 2608.30679][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.30679"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:28:27.701952+00:00"
source_sha256: "cd30d8cc6eaf8dfd40629ddee3fffd8b103a2ef209a44b1cb3c597f8a50b0421"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大型推理模型"
  - "长思维链"
  - "推理链验证"
  - "推理图"
  - "自然语言推断"
  - "图注意力网络"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.30679</p>

# LCoT-GV: Graph Attention Networks for Verifying Long Reasoning Chains in Large Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Bérénice Jaulmes, Mehwish Alam</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Télécom Paris, Institut Polytechnique de Paris, France</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30679v1) · [PDF 下载](https://arxiv.org/pdf/2608.30679v1) · **关键词** 大型推理模型, 长思维链, 推理链验证, 推理图, 自然语言推断, 图注意力网络<br>
**代码**: [https://github.com/ormarv/LCoT-GV](https://github.com/ormarv/LCoT-GV)

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

大型推理模型（LRM）通常通过长思维链（LCoT）把问题分解为多个中间推理步骤，再生成结论。仅检查最终答案不足以判断推理过程是否可靠：一条链即使得到正确答案，其中仍可能存在步骤间矛盾、算术不一致、无依据推断或无关内容。因此，本文关注“推理链验证”，即根据整条长推理链的内容及步骤间依赖关系，判断其推理过程整体是否正确。现有方法多按顺序或局部检查步骤；图方法则把步骤视为节点、把语义或逻辑依赖视为边，从而显式表达跨越较远步骤的关系。本文进一步强调在本地利用自然语言推断模型构图，避免依赖大型语言模型的多次调用。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**长思维链（Long Chain-of-Thought, LCoT）**

模型为解决复杂问题而生成的较长分步推理文本，每个片段承担一个中间判断、计算或推导。链条较长时，错误可能出现在中间步骤并被后续内容掩盖，因此最终答案正确不等于推理过程正确。

</div>
<div class="concept-item" markdown="1">

**自然语言推断（Natural Language Inference, NLI）**

NLI用于判断两段文本之间是否存在蕴含、矛盾等语义关系。本文用NLI模型识别推理步骤间的语义和逻辑依赖，并据此连接图中的节点，而不是让大型语言模型负责构图。

</div>
<div class="concept-item" markdown="1">

**图注意力网络（Graph Attention Network, GAT）**

GAT是一类图神经网络，会聚合相邻节点的信息，并通过注意力机制学习不同邻居的重要程度。用于本文场景时，它从推理步骤及其关系构成的图中提取整体表示，以预测推理链正确或错误。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一道问答任务对应的、由大型推理模型生成的长思维链；链中包含多个可分离的推理步骤。系统首先将每个步骤表示为图节点，再依据NLI模型识别出的语义与逻辑关系建立边，形成推理图；随后使用GAT对该图进行图级二分类，输出整条推理过程“正确”或“错误”的标签。该设定关注过程级正确性，而不把最终答案是否正确直接等同于推理链是否可靠；同时假设步骤之间可通过自动语义关系识别形成有助于验证的结构。论文还指出，已有DeltaBench虽包含经过评估的LCoT，但样本量不足以训练该图验证器，因此需要由多个领域的推理问答基准构造带正确性标签和图结构的新数据集。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Graph-of-Verification**: 该方法也把思维链表示为图，并从根节点开始逐节点验证；若某一分支检测到错误，就停止继续验证该分支。它说明图结构可用于表达和检查推理过程，但原文指出此类工作主要面向一般思维链，而非本文重点处理的长思维链。
- **LCoT2Tree**: 这是与本文最接近的长思维链结构化验证方法：它先由大型语言模型提取任务草图，并为思维片段分配抽象深度索引，再根据推进、回溯或分支重置关系构造树。LCoT-GV的关键区别是使用NLI模型识别步骤间关系并在本地构图，从而避免为表示构建而多次调用大型语言模型，并允许以一般图而非仅树结构表达依赖。

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

LCoT-GV（Long Chain-of-Thought Graph Verifier）将大型推理模型生成的长思维链拆分为若干推理步骤，并把每个步骤表示为图节点；节点之间通过自然语言推断（NLI）判断蕴含或矛盾关系，从而形成推理图。随后，模型使用句子嵌入作为节点特征、关系独热编码作为边特征，并结合邻接矩阵输入图注意力网络（GAT），学习整个推理图的表示，最终通过线性分类层预测该思维链所得最终答案是否正确。直观地说，该方法不只检查答案本身，而是把解题过程画成一张包含支持关系和冲突关系的图，再判断这张图是否整体可靠。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 将长思维链切分为推理步骤

根据“ So ”、“ Actually ”、“ Let’s ”和“ Wait ”等表示逻辑转折或推进的关键词切分文本，而不是仅依据双换行符切分。每个切分结果被视为一个具有相对完整语义的推理步骤。

<div class="method-step__io" markdown="1">

**输入**：大型推理模型生成的长思维链（LCoT）文本。<br>
**输出**：按顺序排列的推理步骤序列，每个步骤对应后续推理图中的一个节点。

</div>

**直观理解**：这些关键词类似“所以”“实际上”“等等”等路标，能帮助模型找到推理过程中的自然分段；每一段就是图中的一个“事件”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 基于NLI构造推理图

对每个新步骤先用候选父节点算法筛选可能相关的已有节点：候选集合包括主分支最近30个节点、主分支上拥有至少两个蕴含子节点的更早节点，以及图中的所有叶节点。对每个候选父节点，收集其所在分支最近五个节点的文本作为上下文，并用NLI分类器判断该上下文与新步骤之间是蕴含还是矛盾；蕴含分数最高的候选所对应分支成为新节点的主分支，得分最高的三个候选建立正边，矛盾分数最高的两个候选建立负边。

<div class="method-step__io" markdown="1">

**输入**：推理步骤序列、当前图结构，以及用于比较步骤语义关系的自然语言推断分类器。<br>
**输出**：一个有向推理图$G=(V,E)$：$V$为推理步骤节点集合，$E$为带有“Entailment”或“Contradiction”关系标签的边集合。

</div>

**直观理解**：新步骤不一定只依赖前一步。方法会在近期步骤、分支关键点和当前叶节点中寻找可能的依据，并分别记录“支持它”和“与它冲突”的连接，因此能表达回溯、分支和不一致。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 生成图节点和边的表示

使用Sentence Transformer将每个推理步骤编码为向量，作为对应节点的语义特征；每条边的关系用表示蕴含或矛盾的独热向量编码为边特征。图的连接结构由邻接矩阵表示。

<div class="method-step__io" markdown="1">

**输入**：推理图中的节点文本以及带关系标签的边。<br>
**输出**：节点特征、边特征和邻接矩阵三类图模型输入。

</div>

**直观理解**：每个节点先被转换成机器可处理的语义向量；边则告诉模型两个步骤之间是支持还是冲突，邻接矩阵告诉模型哪些节点相连。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 使用GAT进行图级正确性预测

图注意力层根据图结构聚合节点信息，并学习不同邻居对当前节点的重要性，得到推理图表示；随后将图表示输入线性分类层，进行图级分类，预测该LCoT过程产生的最终答案是否正确。

<div class="method-step__io" markdown="1">

**输入**：推理图的节点特征、边特征和邻接矩阵。<br>
**输出**：最终答案正确或错误的分类结果，以及用于训练的预测概率。

</div>

**直观理解**：GAT像是在图上分配注意力：它可以更重视与当前步骤有强支持或明显冲突的邻居，最后把整张推理图压缩成一个判断答案可靠性的结果。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：论文节选说明模型使用负对数似然损失优化，但未给出该损失的显式数学公式。训练目标是让GAT及其线性分类层根据推理图预测最终答案的正确性；输入图的标签应对应该LCoT最终答案是否正确。原文未明确报告优化器、学习率、批大小或训练轮数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 候选父节点识别与分支维护**

算法首先取得图中的叶节点，并遍历当前主分支。若节点位于主分支末端30个位置之内，或拥有至少两个带蕴含关系的子节点，则将其加入候选集合；叶节点始终加入候选集合。候选节点按相关分数排序，之后用最高蕴含分数对应的分支更新新节点的主分支。

> 直观理解：该模块限制每个新步骤需要比较的历史范围，同时保留分支汇合点和当前未延伸的节点，避免把所有历史步骤都当作潜在依据。

**2. NLI关系构图**

NLI分类器比较候选父节点所在分支最近五个节点组成的上下文与新步骤，并输出蕴含或矛盾分数。分数超过预设阈值时建立相应正边或负边，最终保留蕴含分数最高的三个候选和矛盾分数最高的两个候选作为新节点的连接。

> 直观理解：NLI模块相当于一个局部逻辑关系检查器：它判断新步骤能否由已有内容支持，或者是否与已有内容冲突，而不是只依据文本距离连接节点。

**3. 图注意力分类器**

节点特征来自每个步骤的Sentence Transformer嵌入，边特征是关系独热编码，另以邻接矩阵描述图结构。GAT层学习图表示，线性分类层据此完成图级最终答案正确性预测，并以负对数似然损失进行训练。

> 直观理解：该模块把局部步骤、步骤间关系和整体拓扑共同用于判断；因此，一个最终答案即使碰巧正确，只要其推理图中存在明显矛盾或缺乏支持，也可能影响模型的判断。

**训练与推理**

训练时，先将每条LCoT按逻辑关键词切分，使用NLI关系和候选父节点算法构图，再用Sentence Transformer生成节点嵌入，并将节点特征、边特征和邻接矩阵输入GAT。GAT学习图级表示后由线性分类层输出正确性预测，并通过负对数似然损失更新模型参数。推理时，对新的LCoT重复切分、构图和特征编码流程，将所得推理图输入训练好的GAT，输出最终答案正确性的分类结果。对于重复出现数百或数千次的相同推理步骤或步骤子序列，构图阶段检测并复用其首次出现时的图结构，而不是重新构建，以降低计算开销。

**复现信息**

步骤切分使用的关键词包括“ So ”、“ Actually ”、“ Let’s ”和“ Wait ”；候选父节点包含主分支最近30个节点、主分支上拥有多于一个正向子节点的更早节点，以及所有叶节点；候选上下文由其所在分支最近五个节点的文本组成。新节点最多连接三个最高蕴含分数候选和两个最高矛盾分数候选，关系边仅在分类器分数超过预设阈值时建立；论文节选未明确报告这些阈值的具体数值。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 作者构建了一个包含 $8{,}000$ 条已评估长思维链（LCoT）的图验证数据集：从 MMLU-Pro、MATH、LiveCodeBench-v5 和 GPQA 四个问答基准中各均匀抽取 $2{,}000$ 条。数据在三个生成模型以及最终答案正确与错误两方面保持平衡，用于检验验证器跨任务和跨模型的稳定性。
- 四类基准承担不同测试角色：MMLU-Pro 和 GPQA 主要测试多项选择与知识推理，MATH 测试数学推理，LiveCodeBench-v5 测试代码推理。答案正确性分别通过多项选择正则匹配、MATH 专用 LaTeX/数学表达式解析器和 LiveCodeBench 官方执行库判定。
- 数据按 $80\%/20\%$ 划分训练集和测试集，并从训练集取 $10\%$ 作为验证集；每条 LCoT随后被转换为一个推理图。该设置测试的是对未见样本的链正确性分类，而不是直接提升原语言模型的最终答题准确率。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

准确率，即被正确判定为正确或错误的 LCoT 占全部样本的比例；表中结果为五次运行的平均值。 （越高越好，因为它表示验证器对整条推理链正确性的判断更准确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 总体比较：LCoT-GV 对三个生成模型和四个基准的验证准确率，与 LCoT2Tree 及长度基线比较

<div class="result-value" markdown="1">

作者报告 LCoT-GV 在两个包含可用结果的 LRM 设置上的平均分为 $76.58$，高于 LCoT2Tree 的 $74.68$；但表中“Average over models”给出的 LCoT-GV 四任务平均值为 $77.03$，因此正文汇总值与表格汇总存在未解释的不一致。LCoT-GV 在 GPQA 和 LiveCodeBench 上提升明显，在 MATH 和部分 MMLU-Pro 设置上较弱。

</div>

这表明图结构验证器整体上具有竞争力，尤其适合代码和科学概念较接近自然语言的推理链。它并不证明图方法在所有任务上都优于树方法：数学推理上的表现下降说明 NLI 和句向量未必能可靠刻画形式化数学关系；同时，正文与表格的平均值不一致，需要核对原始实验记录。

<div class="result-source" markdown="1">

来源：Section 4, Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We compare our model against LCoT2Tree, the approach most close to our work, and a length-based classifier.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨任务表现：LCoT-GV 的四个基准平均结果

<div class="result-value" markdown="1">

表 1 的“Average over models”行显示，LCoT-GV 在 MATH、GPQA、LiveCodeBench 和 MMLU-Pro 上分别为 $72.37$、$78.47$、$87.58$ 和 $69.68$，四任务平均为 $77.03$。

</div>

模型在 LiveCodeBench 上最高，说明代码推理链中的步骤关系较容易被当前 NLI 和句向量模块捕捉；MATH 最低，说明数学等价性、符号变换和多步演算不能简单依靠通用语言关系建模。这里的结果描述的是验证正确性，不是这些基准上原始语言模型的答题准确率。

<div class="result-source" markdown="1">

来源：Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Average over models
Ours
72.37
78.47
87.58
69.68
77.03

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 不同生成模型：LCoT-GV 在单模型上的稳定性

<div class="result-value" markdown="1">

表 1 中 LCoT-GV 的四任务平均准确率为：DeepSeek-R1-Distill-Llama-70B 为 $77.92$，DeepSeek-R1-Distill-Qwen-32B 为 $75.24$，QwQ-32B 为 $77.92$。前者和后者相同，但其各任务分布不同；Llama-70B 在 MATH 和 GPQA 上分别为 $76.54$、$78.75$，QwQ-32B 分别为 $70.64$、$79.85$。

</div>

模型平均值相近，说明验证器并非只对某一个生成器有效；不过不同生成模型产生的推理风格和错误类型仍会改变各任务表现。由于表中 DeepSeek-R1-Distill-Qwen-32B 的名称在表头显示为截断或合并形式，模型对应关系应以原始表格核查。

<div class="result-source" markdown="1">

来源：Table 1, DeepSeek-R1-Distill-Llama-70B

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Ours
76.54
78.75
85.17
71.23
77.92

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

- Length-based classifier：仅依据思维链长度进行分类，是低成本基线，用于判断图结构和语义关系是否比表面长度信息更有用。
- LCoT2Tree：与本文最接近的结构化方法，将 LCoT 表示为树并进行验证；它能检验将推理组织成一般图、加入多种关系后是否优于树结构。

**实验想回答的问题**

- 将长思维链表示为包含语义蕴含、矛盾和相似关系的图，并用图注意力网络验证，是否比基于思维链长度或树结构的分类方法更准确？
- 去除元数据、改变边类型或改变节点特征后，模型性能如何变化，从而判断图结构、关系边和特征设计的贡献？

**实验实现**

实验使用 DeepSeek-R1-Distill-Llama-70B、DeepSeek-R1-Distill-Qwen-32B 和 QwQ-32B 三个开源大推理模型生成或提供 LCoT。图构建时使用八个最常见关键词切分推理步骤；使用长上下文 DeBERTa 进行自然语言推断（NLI），以 $0.7$ 作为蕴含和矛盾阈值，并使用对比学习微调的 MiniLM 生成句向量。验证器由两层 GATv2（隐藏维度 $64$）和带 ReLU 的两层 MLP 分类头组成，训练 $100$ 个 epoch、批大小为 $32$、学习率为 $10^{-3}$。数据生成约需两张 H100 GPU 上 $16$ 小时，单样本图构建在一张 V100 上最多需 $3$ 分钟，GAT 训练在 V100 上少于 $30$ 分钟。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 去除或替换元数据和节点特征：Default model、Meta、Mixed、Mixed, P、Embeddings, P | 在 DeepSeek-R1-Distill-Llama-Qwen-32B 设置中，默认模型平均准确率为 $75.24$，仅用元数据（Meta）降至 $52.92$，联合嵌入与元数据（Mixed）为 $73.29$，联合特征且仅保留正边（Mixed, P）为 $74.55$，仅用嵌入且仅保留正边（Embeddings, P）为 $73.39$。表 2 将 Meta 定义为使用元数据特征、Mixed 定义为联合使用嵌入和元数据。 | 仅靠元数据不能替代推理内容，因此性能大幅下降；加入语义嵌入后结果恢复，说明节点文本语义是主要信息来源。该比较也显示默认配置优于若干受限特征配置，但因为不同变体可能同时改变特征和边，不能把每个差值都归因于单一组件。 | Table 2, DeepSeek-R1-Distill-Llama-Qwen-32B<br><span class="experiment-evidence">Default model
69.92
76.82
88.79
65.42
75.24
Meta
47.77
56.69
66.51
40.71
52.92
Mixed
64.60
78.62
88.09
61.86
73.29
Mixed, P
66.10
78.04
89.58
64.50
74.55
Embeddings, P
67.81
77.77
85.63
62.36
73.39</span> |
| 保留正边（P）与不同特征组合的比较 | 在 QwQ-32B 设置中，Default model 的平均准确率为 $77.92$，Mixed 为 $75.99$，Mixed, P 为 $77.18$，Embeddings, P 为 $77.76$；在 DeepSeek-R1-Distill-Llama-70B 设置中，四者分别为 $77.92$、$75.24$、$73.84$ 和 $75.50$。 | 只保留正向关系边并不会稳定提升性能：它在 QwQ-32B 上接近默认配置，但在 Llama-70B 上明显较低。这说明矛盾或其他关系边可能包含重要的错误证据，不能简单视为噪声；不过该消融没有分别报告每一种边类型，因此无法判断究竟是哪类边贡献最大。 | Table 2, QwQ-32B<br><span class="experiment-evidence">Default model
70.64
79.85
88.77
72.40
77.92
Meta
52.27
51.21
65.94
50.25
54.92
Mixed
66.52
77.41
88.91
71.12
75.99
Mixed, P
67.51
77.07
90.53
73.63
77.18
Embeddings, P
72.90
76.56
88.15
73.42
77.76</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：将长思维链表示为推理图并训练图注意力验证器，以判断推理链的逻辑正确性。; rule check: matched taxonomy keywords; top rule score=11.0
- 全文指纹：`cd30d8cc6eaf8dfd40629ddee3fffd8b103a2ef209a44b1cb3c597f8a50b0421`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
