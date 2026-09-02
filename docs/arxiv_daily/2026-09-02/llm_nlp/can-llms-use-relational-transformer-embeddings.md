---
title: "[论文解读] Can LLMs Use Relational Transformer Embeddings?"
description: "[arXiv 2609.00457][LLM 其他] 本文检验一种看似互补的融合设想：将冻结的关系 Transformer 表征投影为软 token 输入大语言模型，能否在关系数据库预测中结合结构建模与语言推理能力；实验结论总体是否定的。"
arxiv_id: "2609.00457"
announcement_date: "2026-09-02"
primary_category: "llm_nlp"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:51:13.492082+00:00"
source_sha256: "0d2c77f757454c783a274ccb290f12df83a935413a1dd5d2d1716fd4ee9bfb82"
tags:
  - "LLM 其他"
  - "LLM Reasoning"
  - "关系型数据学习"
  - "Relational Transformer"
  - "大语言模型"
  - "软令牌融合"
  - "跨模式迁移"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 其他 · arXiv 2609.00457</p>

# Can LLMs Use Relational Transformer Embeddings?

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Francisco Galuppo Azevedo, Clarissa Lima Loures</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Kunumi Institute, Brazil</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00457v1) · [PDF 下载](https://arxiv.org/pdf/2609.00457v1) · **关键词** 关系型数据学习, Relational Transformer, 大语言模型, 软令牌融合, 跨模式迁移<br>


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

本文检验一种看似互补的融合设想：将冻结的关系 Transformer 表征投影为软 token 输入大语言模型，能否在关系数据库预测中结合结构建模与语言推理能力；实验结论总体是否定的。

**不用术语来说**：企业数据通常分散在相互关联的多张表中，例如客户表、订单表和评论表。预测某位客户是否流失，需要同时理解其属性、跨表关系和时间历史。专用模型善于处理这种数据库结构，却难以利用大语言模型预训练所得的语义与推理能力；大语言模型可以处理文字，但若先把多表记录改写成长文本，可能遗漏关系、混淆不同字段的含义，并迅速占满上下文窗口。本文因此研究能否不把全部数据库邻域写成文字，而是直接把关系模型生成的向量交给大语言模型。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出并实际检验一条具体的软 token 融合路线：冻结关系 Transformer，用可学习的 MLP 将其关系表征映射到 Qwen3.5-4B 的嵌入空间，再通过 LoRA、监督微调与基于组的强化学习训练语言模型完成二分类预测。
- 在 RelBench 的 6 个数据库、10 个任务和 4 种监督范围上系统考察该设想，并报告负面证据与失败模式：该混合模型不能稳定超过独立关系 Transformer，而且对序列化方式、关系 token 预算和训练初始化较为敏感。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究关系型数据库上的实体级预测，以及关系编码器与大语言模型的融合。关系型数据库通过多张表、实体属性、外键关系和时间历史表示用户、产品等对象；给定一个目标实体，模型需要综合其跨表关联信息，预测一个二元结果。现有方法主要分为两类：关系编码器直接在关系图或其局部邻域上学习结构表示，擅长处理多表依赖；大语言模型则通过文本化数据进行语言推理，但多跳关系序列化可能造成信息损失、上下文过长，并削弱外键图中的类型语义。本文考察能否将冻结的关系编码器表示作为连续的“软令牌”注入大语言模型，从而同时利用结构建模与语言推理能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**关系型数据库与关系图**

关系型数据库由多张表组成，表中记录通过主键和外键相互连接；把实体视为节点、把表间连接视为边，就得到用于建模的关系图。目标实体的局部多跳邻域称为其关系上下文或关系自我图。

</div>
<div class="concept-item" markdown="1">

**Relational Transformer（RT）**

RT 是面向关系型数据的 Transformer 编码器：它从目标实体出发，在主键—外键图上进行有界宽度的广度优先搜索，并结合时间约束构造上下文窗口，再用结构化注意力编码单元格信息。本文冻结 RT 参数，并把它输出的向量作为关系信息输入后续大语言模型。

</div>
<div class="concept-item" markdown="1">

**软令牌与参数高效微调**

软令牌不是可读的文字词元，而是直接送入语言模型输入层的连续向量；它可以携带关系编码器压缩后的结构信息。LoRA 通过学习低秩参数增量适配原模型，避免更新大语言模型的全部参数，因此适合训练这种跨模态接口。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

对每个关系型数据库中的目标实体，输入包括自然语言任务提示、候选二元标签以及该实体由 RT 编码的关系上下文表示。RT 先对目标实体的多表邻域进行编码，得到关系嵌入；一个可学习的多层感知机（MLP）将这些嵌入投影到 Qwen3.5-4B 的词嵌入空间，并把投影结果插入文本序列作为软令牌。经 LoRA 适配后的语言模型输出推理文本和格式化的二元标签，目标是正确预测实体级分类结果。实验覆盖 RelBench 的 6 个关系数据库和 10 个二元分类任务，并考察单任务、同数据集、多数据集迁移及全部任务联合训练等设置；关键假设是冻结 RT 的结构表示能够被语言模型可靠地对齐和利用，而无需把关系邻域损失性地转换为长文本。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D$**

一个关系型数据库，包含多张通过主键和外键连接的表。

</div>
<div class="notation-item" markdown="1">

**$v$**

待预测的目标实体，例如某个客户或用户；模型围绕该实体构造关系上下文。

</div>
<div class="notation-item" markdown="1">

**$h_v^{\mathrm{RT}}$**

RT 为目标实体 $v$ 的关系上下文生成的嵌入向量；该编码器在本文中保持冻结。

</div>
<div class="notation-item" markdown="1">

**$z_v$**

经 MLP 投影后的关系嵌入，位于 Qwen3.5-4B 的输入嵌入空间，并作为软令牌插入文本序列。

</div>

</div>

**直接相关的工作**

- **Wydmuch et al. (2024)**: 该工作将目标实体的两跳关系邻域序列化为嵌套 JSON，并使用冻结的大语言模型结合上下文示例进行预测，说明语言模型可以处理关系数据，但性能依赖提示设计和上下文长度。本文改用 RT 的连续结构嵌入，试图避免多表关系的文本序列化损失。
- **Wu et al. (2025), Rel-LLM**: Rel-LLM 通过可学习投影把 GNN 嵌入作为软令牌注入冻结的大语言模型，但其 GNN 需要针对每个数据库单独预训练，且语言模型未被训练去理解注入的令牌，因此没有检验跨模式迁移。本文使用具备跨数据库能力的冻结 RT，并通过 LoRA 训练大语言模型解释关系令牌。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

关系数据库中的实体级预测是常见的工业机器学习需求。模型必须综合实体属性、外键连接形成的跨表关系以及随时间累积的行为记录；这些信息既具有明确的数据库结构，又可能需要结合字段语义进行判断，因此单纯依靠结构模型或文本模型都可能只覆盖问题的一部分。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **专用关系编码器，如关系 Transformer（RT）**：该类模型直接在由多张表及其外键关系构成的关系图上运算，将目标实体周围的关系邻域压缩成具有结构信息的稠密向量，从而用于实体级预测。
- **基于序列化关系数据提示大语言模型**：该类方法把目标实体及其相关表记录转换为自然语言或线性文本，再将任务说明和这些记录一起输入大语言模型，由模型根据文本上下文推理并输出标签。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 关系编码器能够保留多表结构，却不能直接利用大语言模型预训练形成的语言语义和推理能力，因而结构表征与通用语言知识之间仍然分离。
- 文本序列化会把图状的多表邻域压平成线性序列；对于两跳邻域，它可能丢失信息、耗尽上下文窗口，并弱化外键图中不同关系类型的语义。最接近的既有融合工作还冻结大语言模型，并采用需要针对每个数据库分别预训练的特定模式 GNN，因此没有验证跨模式迁移。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少直接而系统的实证研究来判断：无需完整文本序列化、也无需为每个数据库单独预训练结构编码器时，由冻结 RT 产生的跨表结构向量能否与大语言模型的嵌入空间有效对齐，并在单任务、同库多任务、跨数据库和全任务训练条件下形成可迁移的预测能力。

</div>
<div markdown="1"><span>核心问题</span>

把冻结 RT 的关系嵌入经可学习 MLP 映射为软 token，并通过 LoRA 适配 Qwen3.5-4B，是否能够稳定利用这些结构表征，在 RelBench 二分类任务上达到或超过独立 RT，尤其是在跨任务和跨数据库监督条件下？

</div>
<div markdown="1"><span>作者直觉</span>

可以把 RT 看作负责“读数据库结构”的模块：它先把目标实体的多表邻域浓缩为少量向量；再把这些向量转换成大语言模型能够接收的软 token，使语言模型像读取额外上下文一样使用结构信息。若两个表示空间能够对齐，RT 可避免冗长且有损的文本展开，而语言模型可在结构摘要之上贡献语义推理与跨模式泛化；本文要验证的关键正是这种看似自然的分工能否在训练中真正建立起来。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<p class="paper-minor-label">关键流程</p>

原文未明确报告完整流程。

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

原文未明确报告。

**训练与推理**

原文未明确报告。

**复现信息**

原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 实验采用 RelBench 基准中的 6 个关系数据库及其时间切分测试集，共覆盖 10 个二分类任务。时间切分用于避免用未来记录预测过去目标；当前节选未给出各数据库的表数、样本量、类别比例和具体时间边界。
- 任务包括 driver-dnf、driver-top3、item-churn、user-visits、user-clicks、user-engagement、user-badge、study-outcome，以及分别来自 rel-amazon 与 rel-hm 的两个 user-churn 任务。它们共同检验模型是否能从多表关系与历史记录中预测实体级二元标签。
- 实验设置四种监督制度：单任务 $ST$ 在同一任务上训练和测试，可视为任务内上界；库内跨任务 $WD$ 在相同数据库模式下迁移到不同任务；跨数据库 $CD$ 面向完全不同的模式；联合训练 $ALL$ 使用全部任务。不同制度分别隔离任务专用学习、同模式迁移、跨模式迁移和多任务共享能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**AUROC**

衡量模型把随机正例排在随机负例之前的概率，适合比较二分类排序能力；约 $50$ 表示接近随机。论文用它评估 RelBench 时间测试切分，并汇报制度均值与逐任务结果。 （越高越好，因为更高值表示正负样本的排序区分能力更强。）

</div>
<div class="metric-item" markdown="1">

**二值任务奖励**

消融实验所用的训练奖励，表示单次预测是否正确，用于比较注意力掩码、序列化和上下文长度对训练行为的影响。它不是主实验的 AUROC，因此不应直接把奖励增量解释为同等幅度的测试 AUROC 提升。 （越高越好，因为更高奖励表示更多训练样例被正确分类。）

</div>
<div class="metric-item" markdown="1">

**格式奖励**

检查模型输出是否遵循要求的回答格式。论文通过训练曲线观察其是否饱和，以区分预测质量问题与单纯的格式遵循失败。 （越高越好；接近饱和说明模型通常能够遵守输出格式，但不代表其标签预测正确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四种监督制度下的平均 AUROC

<div class="result-value" markdown="1">

独立 RT 在可比较的 $ST$ 和 $CD$ 制度中分别达到 $71.9$ 与 $69.7$，均为最强。混合模型在 $ST$ 下只有 SFT $48.3$、GSPO $51.1$、SFT+GSPO $50.7$；在 $CD$ 下 GSPO 与 SFT+GSPO 分别为 $54.9$ 和 $52.2$，都明显落后于 RT。

</div>

作者据此主张，冻结关系表示经投影后并未被大语言模型稳定解码，且在跨模式迁移时也没有保留 RT 的优势。分析上，这说明当前训练与融合方案没有产生平均收益；但它不能证明所有软词元融合都不可行，因为结论限于所测试的编码器、投影器、语言模型与训练目标。

<div class="result-source" markdown="1">

来源：第 4.3 节，表 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Standalone RT is the strongest model in every regime and no hybrid configuration closes the gap on average.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### SFT 预热对 GSPO 的作用

<div class="result-value" markdown="1">

在 $ST$ 中，GSPO 为 $51.1$，SFT+GSPO 为 $50.7$，两者近乎相同；在 $WD$ 中，SFT+GSPO 为 $48.2$，反而低于无预热 GSPO 的 $53.5$。因此，实验没有观察到 SFT 预热带来的稳定收益。

</div>

如果监督阶段已把关系嵌入与语言模型内部表示有效对齐，完整两阶段方案通常应优于直接强化学习；结果却相同或更差，说明 SFT 推理轨迹可能没有教会模型可靠读取关系软词元，或者后续强化学习破坏了预热所得行为。该比较不能单独区分这两种机制。

<div class="result-source" markdown="1">

来源：第 4.3 节，表 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In WD, SFT+GSPO (48.2) is weaker than GSPO-only (53.5), the opposite of the expected ordering.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### $ALL$ 联合训练及其任务分布

<div class="result-value" markdown="1">

GSPO 在 $ALL$ 下的平均 AUROC 为 $61.4$，但主要由 user-clicks 的 $81.5$ 和 user-visits 的 $68.9$ 两个异常高结果拉升；其余八个任务平均仅为 $57.9$。

</div>

总体均值看似是混合模型最好的制度，但逐任务分解显示收益高度集中，不能解释为普遍的多任务迁移能力。它提示联合训练可能利用了少数任务特有的文本或模式线索，同时多数任务仍缺乏稳定改善；由于节选未给出方差或重复实验，也不能判断两个异常值是否可复现。

<div class="result-source" markdown="1">

来源：第 4.3 节，表 3；附录表 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In ALL, GSPO reaches 61.4 but this is driven by two outlier tasks (user-clicks=81.5, user-visits=68.9); the remaining eight tasks average 57.9.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 消融实验仅覆盖两个任务且只运行一个随机种子；主结果节选也未报告方差、置信区间或显著性检验。因此，序列化、掩码和上下文长度差异可能混入随机训练波动，尤其不能把小幅变化视为确定性结论。
- 实验只验证一种冻结 RT、MLP 投影、Qwen3.5-4B、LoRA 与 SFT/GSPO 组合。结果支持“当前实现不可靠”，但不足以否定带有显式对齐目标、模式感知投影、可训练关系编码器或其他语言模型的软词元融合方案。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 独立 RT：不经过大语言模型，直接使用关系 Transformer 完成关系预测，是检验软词元融合是否真正增加价值的首要基线。RT 按设计没有 $WD$ 和 $ALL$ 结果。
- SFT：混合模型仅使用带思维链推理轨迹的监督微调，不进行强化学习；它检验监督信号本身能否教会大语言模型解释冻结的关系嵌入。
- GSPO：混合模型不经 SFT 预热，直接进行基于组的强化学习；与 SFT+GSPO 对比可判断监督预热是否必要。
- SFT+GSPO：完整两阶段流程，先监督微调、再进行 GSPO；它是论文所设想的完整训练方案，也用于检验强化学习能否在已有对齐基础上进一步改善关系预测。

**实验想回答的问题**

- 将冻结的关系编码器表示投影为软词元并注入大语言模型后，混合模型能否在关系型数据库的二分类任务上稳定利用多表结构信息，并达到或超过独立关系 Transformer（RT）？
- 这种融合能力能否跨任务或跨数据库模式迁移；其效果是否对注意力掩码、文本序列化方式和关系词元预算等设计选择保持稳健？

**实验实现**

所有模型在 RelBench 时间测试切分上评估。主实验比较 $ST$、$WD$、$CD$ 和 $ALL$ 四种制度，并报告平均 AUROC；完整逐任务结果见附录表 6。SFT 是每个任务一个检查点，因此其结果不随迁移制度变化；RT 按设计不提供 $WD$ 或 $ALL$。消融只在两个任务上运行一个随机种子，以二值训练奖励比较关系注意力掩码、文本序列化和关系上下文长度 $L$。训练曲线另报告 rollout 长度、任务奖励与格式奖励。当前节选未明确给出训练轮数、学习率、LoRA 秩、批量大小、统计显著性检验或主结果的随机种子数量。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 文本序列化：flat 与 JSON | 从 flat 切换到 JSON 后，rel-f1 的二值任务奖励增加 $0.632$，rel-trial 增加 $0.359$，是三类消融中最大的变化。 | 该实验隔离软词元周围文本脚手架的组织方式。若连续关系嵌入已成为主要信息来源，改变外围文本格式不应造成如此大的差异；作者因此将结果解释为模型更依赖 JSON 的文本结构提示，而非稳定解码软词元。不过这里只使用一个随机种子，且奖励增量不是测试 AUROC，不能据此量化泛化提升。 | 第 4.2 节 Serialization；表 2<br><span class="experiment-evidence">Switching from flat tokens to json yields large gains on both tasks (+0.632 on rel-f1, +0.359 on rel-trial).</span> |
| 关系上下文长度 $L$：$64$、$256$ 与 $1024$ | 将 $L$ 从 $64$ 增至 $256$，rel-f1 和 rel-trial 的任务奖励分别增加 $0.070$ 与 $0.144$；继续增至 $1024$ 时额外信息收益有限，却增加了显存需求与训练时间，因此论文选择 $L=256$。 | 该消融检验向语言模型提供更多关系词元是否能按比例带来更多结构信息。收益在较短上下文后迅速递减，说明瓶颈可能是关系嵌入与语言模型之间的对齐或利用方式，而不只是词元数量不足。但因为不同长度还会改变优化难度与计算预算，该结果不能独立证明额外关系词元完全无信息。 | 第 4.2 节 Context size；表 2<br><span class="experiment-evidence">Increasing L from 64 to 256 improves task reward modestly (+0.070 on rel-f1, +0.144 on rel-trial); increasing further to L=1024 adds little while increasing memory and training time.</span> |

**定性案例**

- 逐任务结果显示明显的偶发性：GSPO 在 $ALL$ 的 user-clicks 上达到 $81.5$，但同一任务在 $ST$、$WD$、$CD$ 下分别只有 $44.4$、$38.7$、$48.2$。这说明某个制度下的高分并未形成跨制度一致的能力证据，更可能与联合训练中的任务交互、共享文本线索或训练不稳定性有关；原文未提供样例级错误分析来确定具体原因。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：研究将关系编码器嵌入作为软token注入LLM的融合方法，并分析其训练不稳定和结构对齐失败问题。; rule check: matched taxonomy keywords; top rule score=5.0
- 全文指纹：`0d2c77f757454c783a274ccb290f12df83a935413a1dd5d2d1716fd4ee9bfb82`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
