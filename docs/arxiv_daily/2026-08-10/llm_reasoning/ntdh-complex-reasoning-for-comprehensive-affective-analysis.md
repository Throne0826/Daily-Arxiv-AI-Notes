---
title: "[论文解读] NTDH: Complex Reasoning for Comprehensive Affective Analysis"
description: "[arXiv 2608.06425][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.06425"
announcement_date: "2026-08-10"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-10T02:42:46.144480+00:00"
source_sha256: "5c4bfc2f37a9c2657803e244f1f14734e6a7297d198c0c668fd49640a3ae450d"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "情感计算"
  - "情绪分析"
  - "推理路径"
  - "强化学习"
  - "GRPO"
  - "推理数据合成"
  - "SemEval-2018"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.06425</p>

# NTDH: Complex Reasoning for Comprehensive Affective Analysis

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-10</span>
<span><strong>作者</strong> Tianlei Zhu, Zhiwei Liu, Yuyan Wang, Xiao-Yang Liu, Sophia Ananiadou</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> aColumbia University, New York, NY, USA；bDepartment of Computer Science, The University of Manchester, Manchester, United Kingdom</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.06425v1) · [PDF 下载](https://arxiv.org/pdf/2608.06425v1) · **关键词** 情感计算, 情绪分析, 推理路径, 强化学习, GRPO, 推理数据合成, SemEval-2018<br>


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

情感分析（affective analysis）旨在从文本中识别情感极性、具体情绪及其强度，为观点分析、立场分析、情感检索、对话系统、心理健康监测和社交媒体分析提供基础信号。本论文关注“综合情感分析”：同一研究框架需要处理情感强度回归、情感类别多标签分类、效价回归和效价有序分类四类任务。这些任务的输出空间不同，既可能是连续数值，也可能是有序等级或多个情绪标签的集合；同时，文本中的否定、程度修饰、反讽、讽刺、习语以及多种情绪之间的相互作用，可能使表面线索与最终情感含义发生冲突。因此，问题不只是把文本直接映射到标签，还需要整合上下文证据并作出可解释的最终判断。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**情感效价与情感强度**

情感效价描述文本整体偏积极还是偏消极，通常可表示为一个连续数值。情感强度描述某种情绪或情感表现得有多强，二者都适合用回归任务预测。

</div>
<div class="concept-item" markdown="1">

**有序分类与多标签分类**

有序分类的类别具有明确顺序，例如从负面到正面，但类别之间的距离未必相等。多标签分类允许一段文本同时对应多个情绪标签，因此评价时需要比较预测集合与真实集合的重合程度。

</div>
<div class="concept-item" markdown="1">

**可验证奖励与推理轨迹**

可验证奖励是依据任务评价规则自动判断答案是否合格，并将判断结果转化为强化学习信号。推理轨迹是从输入文本出发、经过情感线索分析并最终生成标签或数值的中间过程，它为优化过程提供了可调整的对象，也使判断过程更容易检查。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一段文本及其任务指示，模型需要在四个互补的 SemEval-2018 子任务中完成预测：情感强度回归（EI-reg）、多标签情绪分类（E-c）、效价回归（V-reg）和效价有序分类（V-oc）。模型不再仅输出一个孤立标签，而是生成一条结构化推理路径，并在末尾给出自然语言形式的结论；该结论可对应连续强度、效价数值、有序类别或情绪标签集合。不同任务保留各自的语义和评价标准：回归任务按照数值容差判断，类别任务按照类别是否正确判断，多标签任务按照标签集合的一致程度判断。论文假设单一策略可以共享跨任务的情感线索分析，同时让最终输出适应具体任务的标签空间；训练阶段先使用监督微调（SFT）学习推理模式，再使用群组相对策略优化（GRPO）依据可验证奖励进一步优化推理与预测策略。论文报告使用 $16{,}302$ 条训练记录，并在包含 $9{,}201$ 个实例的官方测试集上评估。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D_{\mathrm{task}}$**

某一具体情感分析任务的数据集或数据子集，例如 EI-reg、E-c、V-reg 或 V-oc 对应的数据。

</div>
<div class="notation-item" markdown="1">

**$x$**

输入文本，通常是一段需要进行情感判断的自然语言内容。

</div>
<div class="notation-item" markdown="1">

**$y$**

与输入文本 $x$ 对应的真实目标，包括连续情感强度、效价值、有序类别或多标签情绪集合。

</div>
<div class="notation-item" markdown="1">

**$\hat{y}$**

模型根据输入文本和任务指示生成的预测结果；它可能是数值、类别或多个情绪标签。

</div>

</div>

**直接相关的工作**

- **EmoLLM**: EmoLLM 是论文所处设定中最接近的已有工作，代表使用指令微调大语言模型处理情感分析的方法。论文将其作为主要比较背景，并指出现有方法总体上主要学习从输入文本到输出标签的直接映射，没有显式建模情感线索之间的冲突协调过程。
- **基于监督推理轨迹与强化学习的数学、临床问答框架**: 这类框架通常由教师模型合成推理过程，再由评价器筛选，并已在数学和临床问答中取得进展。论文借鉴其“推理监督加可验证强化学习”的基本思路，但认为通用方案不能直接适应情感分析，因为情感任务同时包含回归、分类和多标签输出，且需要处理效价转移、反讽和情绪交互等领域现象。

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

NTDH 将综合情感分析重新表述为带结构化推理轨迹的生成任务：输入一条文本和指定子任务，模型先生成包括思考过程与最终答案的输出，再由与任务评分容差一致的验证器判断答案是否合格。方法先把 SemEval-2018 Task 1 的原始标签自然语言化，随后通过领域感知的重思策略和方向性提示修正失败轨迹，并按验证轨迹质量将数据分流到监督微调（SFT）或群组相对策略优化（GRPO）。直观地说，NTDH 不只训练模型记住标签，而是训练模型以统一的语言格式分析线索、形成判断，并在错误时依据“偏高、偏低、漏标”等信息重新推理。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 任务预处理与标签格式转换

系统将每条样本转换为包含分析目标和输出格式要求的指令，并按子任务编码标签：EI-reg 输出 $[0,1]$ 的情绪强度，V-reg 使用 $[-1,1]$ 的情感强度，V-oc 使用七级有序类别，E-c 使用固定的十一种情绪索引及中性类别。随后将原始标签改写为明确说明量表、类别或情绪集合的自然语言句子。

<div class="method-step__io" markdown="1">

**输入**：SemEval-2018 Task 1 的原始文本、子任务标识和金标准标签；子任务包括 EI-reg、V-reg、V-oc 和 E-c。<br>
**输出**：任务特定的指令、文本输入和自然语言化金标准答案。

</div>

**直观理解**：不同任务原本使用数字、等级或标签集合，难以用同一种生成接口处理；这一步把它们统一成模型可以直接阅读和生成的句子，同时保留各任务的含义。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始推理轨迹生成与容差验证

生成器为每个样本生成结构化的推理轨迹和最终答案；验证器解析答案，并使用与子任务评分标准一致的容差 $\tau$ 判断其是否正确。与二元 LLM 评审不同，该验证主要采用确定性任务门控；回归、序数分类和多标签分类分别依据各自的数值误差、类别偏差或标签集合标准进行判断。

<div class="method-step__io" markdown="1">

**输入**：自然语言化样本，以及生成模型产生的初始 Inner Thinking 推理步骤和 Final 答案。<br>
**输出**：通过验证的推理轨迹、失败但可继续修正的轨迹，以及对应的验证状态。

</div>

**直观理解**：验证器不是凭语言感觉判断“像不像正确答案”，而是按照该任务真正允许的误差范围检查答案，因此训练数据的正确性标准与最终评测标准保持一致。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 领域感知重思与方向性提示

系统迭代选择 Backtracking、Exploring New Paths、Verification 和 Correction 四类策略，分别检查深层线索、语境线索、直接证据以及细粒度强度或类别错误，并在后续轮次重新验证。若仍失败，方向性提示只告知错误类型和方向，例如“过高”“过低”“漏标”或“部分正确”，不泄露金标准答案；系统还允许失败样本保留为未收敛样本，而不是强行注入标签。

<div class="method-step__io" markdown="1">

**输入**：未通过验证的推理轨迹、原文证据和验证器提供的错误方向信息。<br>
**输出**：收敛的 reasoning-augmented 样本，或带有金标准答案但没有正确推理轨迹的未收敛样本；每个样本同时获得 Gold、Silver、Bronze、Low 或 Unconv. 质量标签。

</div>

**直观理解**：模型只得到“判断偏正面了”或“漏掉了一种情绪”这类导航信息，必须自己回到文本找原因，避免把答案直接抄进推理过程而造成虚假的解释。领域策略则让重思关注否定、程度词、反讽、隐喻和情绪共现等真实情感现象。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 质量分流与两阶段训练

每个子任务的训练池按固定种子 42 划分为 half-A 和 half-B；half-A 经合成流程后，将带有非空正确推理链的 Gold、Silver、Bronze 样本用于 SFT，half-B 的问答对与 half-A 的未收敛困难样本组成 RL 集。模型先对 Qwen3-8B 进行全参数 SFT，使其学习生成 `<think>` 后接 `<answer>` 的格式，再从 SFT 检查点出发使用 GRPO：对一组采样结果按满足任务容差的二元奖励进行相对优化。

<div class="method-step__io" markdown="1">

**输入**：收敛的高质量推理样本，以及半数未经过 CoT 生成的问答样本和半数中未收敛的困难样本。<br>
**输出**：能够生成结构化情感推理并输出任务答案的最终 affective reasoning policy。

</div>

**直观理解**：SFT 先教模型“应该怎样组织推理和答案”，GRPO 再用严格的任务正确性标准强化可得分的输出；即使某些困难样本没有成功的推理链，它们仍可在强化学习阶段提供奖励信号。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：SFT 阶段以收敛样本中的结构化推理轨迹和自然语言化答案作为监督目标，训练模型生成 `<think>` 推理与 `<answer>` 结果。GRPO 阶段从 SFT 检查点继续训练，对每个问题采样一组候选完成，并依据解析后的答案是否满足任务容差 $\tau$ 给予二元奖励：满足则为 $1$，否则为 $0$；GRPO 根据组内候选结果估计相对优势，不需要单独的价值网络。原文未明确给出完整的 GRPO 损失函数或显式公式，因此不补写未提供的数学表达。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Naturalisation（自然化）**

该模块使用每个子任务专属的模板，把原始数字、序数类别或多标签集合转换为明确的自然语言答案；监督目标直接采用自然语言化金标准，而不是模型在改写过程中生成的可能漂移的答案。

> 直观理解：生成器、验证器和最终训练目标都使用同一种答案表达，减少数字标签与文字答案之间的格式错配，并保证监督答案从一开始就是正确的。

**2. Tolerance-aware verification（容差感知验证）**

验证器依据每个子任务的评分容差 $\tau$ 进行确定性门控：回归任务检查数值误差，V-oc 检查七级类别是否满足允许偏差，E-c 检查十一类情绪集合的匹配标准。该门控既用于筛选合成数据，也用于 GRPO 的二元奖励，使数据构造和优化使用同一正确性标准。

> 直观理解：情感强度预测不一定要求小数完全相同，序数类别也可能允许有限偏差；验证器把这些任务自身的“多接近算正确”规则落实到训练中。

**3. Domain-aware refinement and Directional Hints（领域感知修正与方向性提示）**

四种重思策略将情感科学知识加入搜索过程：Backtracking 处理深层线索推翻表层解读的情况，Exploring New Paths 转向语境和非组合性表达，Verification 检查词语、否定、表情符号和标点等证据，Correction 处理强度等级及细粒度类别错误。方向性提示根据任务类型提供回归偏差方向、多标签过标或漏标、以及序数情感极性和偏差程度，但不显示目标标签。

> 直观理解：该模块把“请重新思考”变成有针对性的检查清单，同时只给模型纠错方向，不给最终答案，因此更有可能产生真实而非答案泄漏式的推理。

**训练与推理**

训练时，原始 SemEval-2018 数据先经过任务格式转换、标签自然化、推理生成和确定性验证。验证成功且含有非空正确推理链的样本进入 SFT；未经过 CoT 生成的 half-B 问答对和 half-A 中未收敛的困难样本进入 RL。Qwen3-8B 先进行全参数 SFT，再使用 GRPO 按任务容差优化最终策略。推理时，模型接收文本、子任务说明和预期输出格式，生成结构化 `<think>` 轨迹及 `<answer>`；论文所给章节重点描述训练流程，未明确规定部署阶段是否继续执行外部验证或重思循环。

**复现信息**

NTDH 将每个子任务的训练池按固定随机种子 42 平分为 half-A 和 half-B，并确保每个训练实例只使用一次。质量层级为 Gold（首次成功，权重 1.0）、Silver（第 2 至 3 轮成功，权重 0.8）、Bronze（至少第 4 轮成功，权重 0.5）、Low（标签泄漏成功，权重 0）和 Unconv.（始终未正确，权重 0）；当前实现只把质量层级作为收敛筛选条件，保留样本在训练中使用统一权重。搜索预算从原框架的最多 1 次新启动和每次 2 轮修正提高到最多 3 次新启动、每次 3 轮修正。SFT 使用 LLaMA-Factory，学习率为 $5\times10^{-6}$、3 个 epoch、每设备批量大小为 1、梯度累积 8、最大长度 8192；GRPO 使用 open-r1 / TRL，学习率为 $1\times10^{-6}$、2 个 epoch、每设备批量大小为 2、梯度累积 4，两个阶段均采用带 $0.1$ warmup 的余弦学习率计划。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- SemEval-2018 Task 1 的四个英文子任务：$EI$-$reg$（四类情绪强度回归）、$E$-$c$（11标签多标签情绪分类）、$V$-$reg$（价度回归）和 $V$-$oc$（7级有序价度分类）。所有结果使用官方测试集；训练数据共16,302条，其中5,388条用于SFT，10,914条用于RL。其作用是覆盖连续值、有序标签和多标签三种输出形式，检验统一复杂推理接口的适用性。
- 固定随机种子后，每个子任务的训练池被均分为 half-A 和 half-B。half-A 用于生成思维链（CoT）；其中收敛样本进入SFT，未收敛、空或非法链样本与 half-B 一同进入RL。该划分使每条训练记录只使用一次，避免同一实例同时出现在两个训练阶段。
- 官方测试划分共9,201条：$EI$-$reg$ 4,068条、$E$-$c$ 3,259条、$V$-$reg$ 937条、$V$-$oc$ 937条。它只用于最终评估；论文说明没有根据官方测试集选择检查点。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Pearson相关系数 $r$**

衡量预测值与金标准值之间的线性相关程度，适用于 $EI$-$reg$ 和 $V$-$reg$；在 $EI$-$reg$ 上先按四种目标情绪计算，再进行宏平均。 （越高越好，因为更高表示预测随真实情感强度变化的方向和幅度更一致。）

</div>
<div class="metric-item" markdown="1">

**Jaccard相似度（SemEval 的 acc）**

衡量多标签预测集合与真实标签集合的交集相对于并集的比例，适用于 $E$-$c$；它同时惩罚漏报和误报。 （越高越好，因为更高表示预测标签集合与真实集合重叠更多。）

</div>
<div class="metric-item" markdown="1">

**micro-F1 与 macro-F1**

micro-F1 在所有标签决策上汇总计算，较受高频标签影响；macro-F1 先逐标签计算再平均，更能反映低频标签表现，二者均用于 $E$-$c$。 （越高越好；micro-F1 衡量总体多标签识别能力，macro-F1 衡量各标签之间是否较为均衡。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### RL-final 相对 SFT init 的官方测试比较

<div class="result-value" markdown="1">

作者报告最终策略在六个官方测试指标中的五个上优于其SFT检查点。

</div>

这说明GRPO阶段通常改善了SFT模型的任务表现，支持“先学习可用输出格式，再通过可验证奖励优化”的训练流程。但该结论不等于所有任务或所有指标都提升；原文摘录没有给出六个指标逐项数值，也不能据此判断提升幅度或统计显著性。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

the final policy improves over its SFT checkpoint on five of six official-test metrics

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 与已有系统比较的 $EI$-$reg$ 结果

<div class="result-value" markdown="1">

NTDH 在被比较系统中取得最强的 $EI$-$reg$ 结果，Pearson相关系数为0.862。

</div>

该结果表明NTDH在四种目标情绪的强度回归上具有较强的预测排序和线性拟合能力，并且优于论文比较范围内的系统。它只直接支持 $EI$-$reg$ 上的优势，不能推出NTDH在所有子任务或所有指标上都排名第一；完整对比数值应以Table 7核查。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

achieves the strongest EI-reg result among the compared systems, at a Pearson correlation of 0.862.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 训练数据规模与使用方式

<div class="result-value" markdown="1">

实验使用16,302条训练记录，其中5,388条进入SFT、10,914条进入RL；每条训练实例恰好使用一次，整体利用率为100%。

</div>

这一设计说明实验将收敛的高质量推理轨迹用于建立初始策略，将未收敛或困难样本保留给强化学习，避免简单样本和失败样本被重复利用。它证明的是数据分流与利用率的设定，不单独证明数据规模导致了性能优势，也不能替代与相同数据预算基线的公平比较。

<div class="result-source" markdown="1">

来源：Section 5.1, Data

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Every training instance is therefore used exactly once (100% utilisation; 16,302 instances total: 5,388 SFT and 10,914 RL)

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

- EmoLLaMA-chat-13B：EmoLLM 指令微调模型家族中在 $EI$-$reg$ 和 $V$-$oc$ 上最强者，因此是主要参照，适合检验较大规模情感指令模型与本文方法的差异。
- SemEval-2018 竞赛系统 SeerNet 和 NTUA-SLP：代表该任务的专门竞赛方法，用于比较本文方法是否超越传统任务定制系统。
- BERT、RoBERTa 和 SentiBERT：预训练语言模型微调基线，用于比较复杂推理式生成方案与直接判别式微调之间的差异。
- Falcon、Vicuna、LLaMA2、ChatGPT 和 GPT-4：零样本或少样本大语言模型基线，用于检验任务专门训练是否比通用提示式推理更有效。

**实验想回答的问题**

- 在四个异质情感分析子任务上，经过监督微调（SFT）后再进行群组相对策略优化（GRPO）的最终策略，能否超过其 SFT 初始化模型以及已有系统？
- 自然化、容忍度感知门控、领域感知策略和方向性提示共同构造的训练数据质量设计，是否能够支持有效的强化学习训练？

**实验实现**

模型为全参数微调的 Qwen3-8B。训练先使用SFT，再从SFT检查点进行GRPO，采用 open-r1 / TRL 技术栈。评估比较两个预先固定的检查点：SFT init（训练步数280）和最后保存的 RL-final；未在官方测试集上选择检查点。模型输出采用结构化的 `<think>` 和 `<answer>` 格式，论文报告两个检查点在官方测试集上均无解析失败。GRPO奖励使用严格的容忍度准确率，该指标用于训练验证但没有作为主结果报告，因为已有系统未报告该指标。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper recasts affective prediction as verifiable complex reasoning and trains the model with SFT and GRPO-based preference optimization.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`5c4bfc2f37a9c2657803e244f1f14734e6a7297d198c0c668fd49640a3ae450d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
