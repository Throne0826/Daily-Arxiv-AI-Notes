---
title: "[论文解读] JPO: Juris Policy Optimization for Structured Legal Reasoning in Criminal Judgment Prediction"
description: "[arXiv 2608.29616][对齐 / RLHF] 原文未明确报告。"
arxiv_id: "2608.29616"
announcement_date: "2026-09-01"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:54:02.233052+00:00"
source_sha256: "4dcb0ea41663b22601f800b46bb1b0f778c0486a41909f1011b52508b6328098"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "强化学习"
  - "法律判决预测"
  - "中国刑事法律"
  - "结构化法律推理"
  - "强化学习后训练"
  - "大语言模型"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.29616</p>

# JPO: Juris Policy Optimization for Structured Legal Reasoning in Criminal Judgment Prediction

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Zhaolu Kang, Yantao Liu, Tailong Luo, Leqi Zheng, Lei Wei, Chenghua Zhu, Junhao Gong, Jiachen Qian, Eric Hanchen Jiang, Jiaxin Liu, Yuan Wang, Hao Zhang, Zixia Wang, Rong Fu, Zheng Lin, Richeng Xuan, Zhichao Hu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Tencent；Affiliation: Peking University；Affiliation: Tsinghua University；Affiliation: City University of Hong Kong；Affiliation: University of California；Affiliation: University of Illinois Urbana-Champaign；Affiliation: Zhejiang University；Affiliation: University of Hong Kong</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.29616v1) · [PDF 下载](https://arxiv.org/pdf/2608.29616v1) · **关键词** 法律判决预测, 中国刑事法律, 结构化法律推理, 强化学习后训练, 大语言模型<br>


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

本文属于法律自然语言处理中的法律判决预测（Legal Judgment Prediction，LJP）研究，具体面向中国刑事案件。给定案件事实，模型需要预测适用的法律条文、罪名以及刑罚结果。与普通的多分类任务不同，刑事裁判具有明确的结构依赖：案件事实应当支持法律条文的适用，法律条文应当支撑罪名认定，而最终刑罚又必须与罪名及相关法律依据相容。因此，评价模型时不能只看最终标签是否正确，还应考察从事实到条文、罪名和刑罚的推理链条是否完整、连贯且具有法律依据。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**法律判决预测（LJP）**

法律判决预测是根据案件事实自动推断司法结果的任务。在本文中，司法结果主要包括适用法律条文、刑事罪名和刑罚结果。

</div>
<div class="concept-item" markdown="1">

**结构化法律推理**

结构化法律推理要求模型按照具有法律意义的阶段逐步分析案件，而不是直接从事实跳到最终标签。本文采用“事实提取—法律条文分析—罪名认定—刑罚预测”的四步结构，并要求相邻步骤相互支持。

</div>
<div class="concept-item" markdown="1">

**后训练与强化学习**

后训练是在通用语言模型预训练完成后，使用任务数据进一步调整模型，使其适应特定任务。强化学习通过奖励信号提高模型产生高质量输出的概率；本文中的奖励不只衡量最终预测，还衡量推理结构完整性和不同推理步骤之间的一致性。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文研究中国刑事法律判决预测。输入是案件事实文本，模型输出一条包含结构化推理和预测结果的回答：首先提取具有法律意义的事实，其次分析适用的法律条文，然后确定罪名，最后预测刑罚结果。该任务默认案件事实可以提供进行裁判所需的关键信息，并且刑事裁判结果存在可由事实、条文、罪名和刑罚构成的依赖关系。论文关注的不是单纯提高某一个最终标签的匹配率，而是在保持法律预测正确的同时，使输出形成可检查的推理链：条文应与事实匹配，罪名应由条文支持，刑罚应与罪名保持一致。由于现有数据集通常主要提供案件事实和最终标签，本文使用教师模型生成的中间推理作为额外监督，再通过强化学习优化由法律预测质量、推理结构完整性和跨步骤一致性构成的复合目标。需要注意的是，论文明确将这些奖励视为可计算的代理指标，而不是法律推理质量的完整定义。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

案件事实文本，即模型进行法律分析时接收的输入。

</div>
<div class="notation-item" markdown="1">

**$a$**

适用的法律条文或法条预测结果。

</div>
<div class="notation-item" markdown="1">

**$c$**

刑事罪名预测结果。

</div>
<div class="notation-item" markdown="1">

**$y$**

刑罚或量刑预测结果。

</div>

</div>

**直接相关的工作**

- **Xiao et al. (2018) 的 CAIL 等中国刑事判决预测基准**: 这类基准建立了根据案件事实预测法律条文、罪名和刑期的标准任务设置，但主要提供最终标签监督。本文在此类任务基础上进一步强调事实、条文、罪名与刑罚之间的结构化推理关系。
- **Ouyang et al. (2022) 的 RLHF 与 Rafailov et al. (2023) 的 DPO**: RLHF 和 DPO 代表了利用任务目标或偏好信号进行语言模型后训练的典型方法。本文沿用后训练思想，但不只优化最终答案或一般偏好，而是针对刑事裁判中的事实—条文—罪名—刑罚依赖链设计结构化奖励。

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

- JPO-Dataset：作者新构建的中国刑事判决预测数据集，来自中国裁判文书网的2024—2026年公开刑事判决文书，覆盖192种罪名和176个法条；平均事实描述长度为217.1个token，中位数为194个token。该数据集用于结构化SFT和强化学习训练，且限定为单被告、具有较完整事实与裁判结果的案件。原文报告：“JPO-Dataset is used for structured supervised fine-tuning and reinforcement learning”；统计信息见附录C表3。
- CAIL2018：较早构建的中国刑事判决预测基准，用于外部测试，检验模型在不同时间分布和文书表达上的迁移能力。作者指出其文书年代早于JPO-Dataset，并对训练集与该测试集进行了近重复检查；41条近重复样本被移除。相关设置见第4.1节和附录B。
- LawBench：另一项中国法律语言模型基准，用于外部测试，以检验JPO是否不仅适用于其训练数据分布。作者报告JPO-Dataset训练集与LawBench之间未发现近重复样本。相关设置见第4.1节和附录B。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**法条预测与罪名预测Macro-F1**

分别对法条标签和罪名标签计算宏平均F1，使每个类别具有相近权重，适合类别分布不均衡的多类别预测任务。 （越高越好；表示模型在不同法条或罪名上的精确率与召回率综合表现更强。）

</div>
<div class="metric-item" markdown="1">

**Sentence Score**

用相对误差评价预测刑期与真实刑期的接近程度，定义为 $\mathrm{Score}_{\mathrm{sentence}}=\exp\left(-\xi\cdot\frac{|\hat{S}-S|}{S}\right)$，其中 $\xi=3$，$\hat{S}$ 是预测刑期，$S$ 是真实刑期。 （越高越好；预测刑期越接近真实刑期，相对误差越小，分数越接近1。）

</div>
<div class="metric-item" markdown="1">

**4-Step Completeness与Full-Chain Consistency**

4-Step Completeness检查回答是否明确包含事实提取、法条分析、罪名确定和刑期预测四个阶段；Full-Chain Consistency衡量这些阶段之间是否连贯，由三个局部一致性分数的平均值构成，局部转移包括事实到法条、法条到罪名、罪名到刑期。 （越高越好；前者表示推理结构没有缺步，后者表示前一步结论能够支持后一步，而不是只给出彼此矛盾的独立标签。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨骨干模型与三项数据集的总体比较：JPO相对于预训练模型和结构化SFT

<div class="result-value" markdown="1">

作者报告JPO在所有开源骨干模型和三个数据集上均优于预训练模型与结构化SFT，并且提升同时覆盖法条、罪名、刑期预测以及推理完整性和全链一致性。

</div>

这说明JPO的强化学习阶段不仅改善最终标签，也改善了从事实到法律结论的中间链条。它支持“结构化初始化后再进行法律任务专用策略优化”这一设计，但由于所给材料没有表1的具体数值、显著性检验或方差，不能判断提升幅度是否在所有设置下都统计显著。

<div class="result-source" markdown="1">

来源：第4.2节 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Overall, JPO consistently improves over both the pre-trained and structured SFT baselines across all open-source backbones and all three datasets.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 两阶段训练与3B模型的基线比较

<div class="result-value" markdown="1">

RL-only虽比预训练模型有所改善，但明显弱于SFT和JPO；JPO进一步稳定优于Vanilla PPO、Legal Δ和Issue Tree Rubrics等后训练基线。

</div>

该结果将收益拆成两部分：仅靠强化学习不能稳定地产生法律推理，结构化SFT提供了必要的四步输出骨架；在此基础上，JPO的法律预测、结构完整性和跨步一致性奖励，以及令牌感知优化，才带来超过通用后训练方法的额外收益。由于没有提供对应分数，不能精确比较各基线的差距。

<div class="result-source" markdown="1">

来源：第4.3节 Detailed Analysis on 3B Backbones

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

RL-only improves over the pre-trained model, but remains clearly weaker than SFT and JPO, indicating that reinforcement learning without structured initialization is insufficient for stable legal reasoning generation.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 推理链局部转移分析：事实到法条、法条到罪名、罪名到刑期

<div class="result-value" markdown="1">

在两个代表性3B骨干上，JPO相对于SFT和Vanilla PPO提升了三种局部一致性，其中罪名到刑期的一致性增益最大；这一模式与刑期预测和Full-Chain Consistency的更强提升相符。

</div>

这表明JPO的主要额外价值可能集中在把已经确定的罪名转换为相容的刑期，而不只是改善单个标签。该分析提供了比总体分数更具体的机制线索，但它仍是相关性证据，不能单独证明罪名到刑期模块是全部总体收益的因果来源。

<div class="result-source" markdown="1">

来源：第4.4节 Further Analysis；图2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across both 3B backbones, JPO improves all three transitions over SFT and Vanilla PPO, with the largest gains appearing in charge-to-sentence consistency.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- JPO-Dataset仅覆盖单被告刑事案件，不包括多被告案件、高度非典型事实模式和复杂程序性裁判，因此结果不能直接外推到完整司法决策场景。
- 当前提供的实验章节缺少表1及消融表的具体数值、误差范围和显著性检验；因此可以确认作者报告的比较方向，但无法独立核验提升幅度、统计稳定性或不同方法之间的实际差距。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Pre-trained：直接使用未针对该任务进行后训练的开源基础模型，衡量任务专门训练带来的收益。
- Structured SFT：使用教师模型生成的标准化四步法律推理进行监督微调，检验显式推理模板本身的作用，并作为JPO强化学习阶段的初始化。
- RL-only与Vanilla PPO：RL-only直接考察缺少结构化SFT初始化时强化学习的效果；Vanilla PPO使用通用近端策略优化，考察JPO的法律任务专用奖励和令牌级优化是否超越通用强化学习。
- Legal Δ与Issue Tree Rubrics：面向法律推理或问题树评分的后训练基线，用于比较不同法律奖励或推理评价设计。专有模型如DeepSeek-V3.2、Qwen3-32B、GPT-5.2和Claude-Sonnet-4.5仅作为零样本能力参照，不是与JPO直接等价的可训练基线。

**实验想回答的问题**

- 与预训练模型、结构化监督微调（SFT）及其他强化学习后训练方法相比，JPO是否能同时提升中国刑事判决预测的法律标签准确性与四步推理质量？
- JPO中的复合奖励、重要性令牌级优势重加权和自适应裁剪，分别是否对推理完整性、跨步骤一致性及最终判决预测产生可辨别的贡献？

**实验实现**

实验覆盖五个开源骨干模型：Qwen2.5-3B/7B-Instruct、Qwen3-4B-Instruct、Llama-3.2-3B-Instruct和Llama-3-8B-Instruct。对4B、7B和8B模型报告预训练、SFT和JPO；对两个代表性3B模型进一步报告RL-only、Vanilla PPO、Legal Δ、Issue Tree Rubrics及组件消融。结构化SFT使用Qwen2.5-72B-Instruct生成推理教师信号，训练2个epoch；强化学习从对应SFT检查点开始，使用PPO相关设置，训练4个epoch、训练批大小1024、PPO小批大小256、KL损失权重为 $10^{-3}$、组大小为5。默认奖励系数为 $\alpha=0.75$、$\beta=0.0625$、$\gamma=0.1875$，令牌级优势缩放因子为 $\psi=0.6$，熵—逻辑混合系数为 $\zeta=0.5$，基础裁剪系数为 $\epsilon=0.2$。所有数据集统一将输入截断至2048个token并保留前部内容；JPO-Dataset、CAIL2018和LawBench采用相同预处理与截断策略。由于当前提供的章节未包含表1的具体分数，无法据此报告数值差异。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除复合奖励中的结构奖励 $R_{\mathrm{structure}}$ 或一致性奖励 $R_{\mathrm{consistency}}$ | 移除 $R_{\mathrm{structure}}$ 对4-Step Completeness影响最大；移除 $R_{\mathrm{consistency}}$ 对Sentence Score和Full-Chain Consistency造成最大下降。 | 该消融分别检验“是否完整执行四步”和“各步是否相互支持”这两个目标。结果说明结构完整性奖励主要防止推理缺步，而一致性奖励更直接约束罪名与刑期等跨步骤关系。原文未提供下降的具体数值，因而不能比较其绝对影响大小。 | 第4.3节 Detailed Analysis on 3B Backbones<br><span class="experiment-evidence">Removing Rstructure most strongly affects 4-Step Completeness, while removing Rconsistency causes the largest degradation in sentence score and Full-Chain Consistency.</span> |
| 移除令牌级优势重加权或自适应裁剪，并将重要性感知令牌权重替换为均匀权重 | 移除令牌级优势重加权或自适应裁剪都会导致性能持续下降；用均匀令牌权重替代重要性感知权重会带来更大的总体下降。 | 这些消融检验优化器如何分配学习信号：法律上关键的推理片段应获得更合适的更新权重，同时裁剪策略应适应不同片段。结果支持JPO不仅依赖奖励内容，也依赖奖励如何在生成序列的不同令牌上发挥作用；但原文未明确报告每个变体的具体数值。 | 第4.3节 Detailed Analysis on 3B Backbones<br><span class="experiment-evidence">Removing token-level advantage reweighting or adaptive clipping also leads to consistent declines, and replacing importance-aware token weights with uniform token weights produces a larger overall drop.</span> |

**定性案例**

- 图3给出一个代表性刑事案件的定性示例，展示先通过结构化SFT建立四步推理骨架，再通过强化学习利用法律准确性、推理完整性和跨步一致性奖励细化推理链。该案例用于说明JPO的工作流程与输出形态，而不是替代大规模定量评估；所给章节未提供该案例的具体案情、预测内容或逐步纠错结果。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文通过监督微调与强化学习后训练优化法律推理结构、奖励和一致性，兼具对齐优化与结构化 LLM 推理贡献。; rule check: matched taxonomy keywords; top rule score=6.0
- 全文指纹：`4dcb0ea41663b22601f800b46bb1b0f778c0486a41909f1011b52508b6328098`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
