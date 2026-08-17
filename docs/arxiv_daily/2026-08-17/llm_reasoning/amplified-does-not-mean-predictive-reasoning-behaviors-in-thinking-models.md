---
title: "[论文解读] Amplified Does Not Mean Predictive: Reasoning Behaviors in Thinking Models"
description: "[arXiv 2608.13760][LLM Reasoning] 本文追问推理导向训练究竟强化了哪些可观察行为，并指出“行为出现得更多”不等于“该行为更能预测答案正确”，因而需要把行为频率与行为对正确性的关联分开衡量。"
arxiv_id: "2608.13760"
announcement_date: "2026-08-17"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-17T02:01:15.725260+00:00"
source_sha256: "3de0df73699e9c3ef9c0f28c85f52c300ac048c59872bae02203e20bc1face97"
tags:
  - "LLM Reasoning"
  - "推理型语言模型"
  - "视觉语言模型"
  - "推理轨迹行为分析"
  - "Behavioral Lift"
  - "Amplification-Lift Gap"
  - "过程监督"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.13760</p>

# Amplified Does Not Mean Predictive: Reasoning Behaviors in Thinking Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-17</span>
<span><strong>作者</strong> Jean de Dieu Nyandwi, Leena Mathur, Yonatan Bisk, Robert Hawkins, Graham Neubig</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Carnegie Mellon University；Affiliation: Stanford University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13760) · [PDF 下载](https://arxiv.org/pdf/2608.13760) · **关键词** 推理型语言模型, 视觉语言模型, 推理轨迹行为分析, Behavioral Lift, Amplification-Lift Gap, 过程监督<br>


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

本文追问推理导向训练究竟强化了哪些可观察行为，并指出“行为出现得更多”不等于“该行为更能预测答案正确”，因而需要把行为频率与行为对正确性的关联分开衡量。

**不用术语来说**：“思考型”模型通常会输出更长、更像深思熟虑的推理过程，但这些表面现象未必意味着推理更可靠：模型可能因为先犯错才进行自我纠正，因为困惑才表达不确定，也可能列出多个假设却没有检验正确的假设。因此，只看答案准确率或推理行为出现次数，无法判断训练真正增强的是有助于成功的能力，还是仅仅增强了看起来像推理的表达模式。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 Behavioral Lift，将某种行为存在与不存在时的正确率差异量化，从而把行为的普遍程度与其对正确性的诊断价值区分开；同时以 Recovery Rate 衡量模型在已经出现至少一个推理失败后仍得到正确答案的能力。
- 利用跨文本与视觉语言推理的行为分类体系分析来自 15 个模型、6 个基准的 15,282 条轨迹，并报告 Amplification-Lift Gap：推理导向训练显著强化的行为，与最关联正确性的行为并不一致。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于推理型大语言模型（LLM）和视觉语言模型（VLM）的行为分析与过程评估交叉领域。此类模型在生成最终答案前，会产生较长的显式推理轨迹（reasoning trace），因此研究重点不应只看最终答案是否正确，还应分析轨迹中出现了哪些行为，以及这些行为是否真正与正确性相关。本文特别区分行为的出现频率（prevalence）与行为和正确答案之间的关联强度（Behavioral Lift），并比较推理导向训练后的 thinking 模型与 instruction-tuned instruct 模型。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**推理轨迹与思维链**

推理轨迹是模型在输出最终答案前生成的中间文字或视觉-语言推理过程，思维链（chain-of-thought，CoT）是其中一种显式表达形式。轨迹可能包含假设、检验、回溯、自我纠错和不确定性表达，但轨迹更长并不自动意味着推理更可靠。

</div>
<div class="concept-item" markdown="1">

**Behavioral Lift**

Behavioral Lift 衡量某种行为出现时与不出现时，模型答对率相差多少，因此描述的是该行为对正确性的诊断性，而不是它出现得有多频繁。直观地说，一个行为可能经常出现，却未必能区分成功推理和失败推理。

</div>
<div class="concept-item" markdown="1">

**Recovery Rate**

Recovery Rate 衡量模型虽然至少出现一种推理失败，最终仍然得到正确答案的频率。该指标用于分析模型是否能在中间出错后恢复，而不只是判断最终答案是否正确。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文输入是来自六类任务基准的模型推理轨迹及其最终答案，涉及纯视觉谜题、逻辑推理、数学推理和知识密集型问答；模型包括 $15$ 个、来自 $7$ 个模型家族的 LLM 和 VLM，并同时考察 thinking 与 instruct 变体。研究者使用一个跨模态行为分类体系标注轨迹，体系包含 $9$ 个跨模态高阶行为以及推理失败、推理质量、推理类型、摘要指标和视觉 grounding 等标签，最终输出每个行为的出现情况、其与答案正确性的关联，以及不同训练范式之间的放大差异。核心问题是：推理导向训练是否优先放大最能预测正确答案的行为，还是只放大看起来更具 deliberation 特征的表层行为。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$N=15{,}282$**

被标注的推理轨迹总数，即本文行为分析的样本规模。

</div>
<div class="notation-item" markdown="1">

**$LLM$**

大语言模型，本文中用于处理文本推理任务的模型。

</div>
<div class="notation-item" markdown="1">

**$VLM$**

视觉语言模型，本文中用于联合处理图像与文本输入的模型。

</div>
<div class="notation-item" markdown="1">

**$s(x)\in\{\mathrm{task},\mathrm{harm}\}$**

原文摘录未给出该形式化符号；因此不将其作为本文确定采用的正式记号。本文实际使用的是行为是否出现在推理轨迹中，以及最终答案是否正确这两类信息。

</div>

</div>

**直接相关的工作**

- **推理导向训练与长思维链：DeepSeek-R1、Kimi-k1.5、Qwen3**: 这些工作表明，强化学习或混合式后训练能够诱发较长的推理轨迹及回溯、自我纠错等行为；本文进一步研究这些行为被诱发后是否真的与正确性相关，并指出 thinking 模型放大的行为不一定是最高预测力的行为。
- **过程监督与超越准确率的评估：Lightman et al. (2023) 及后续过程评估工作**: 过程监督和过程奖励模型尝试在步骤层面评价推理，而不是只评价最终答案。本文为过程监督提出更具体的判断标准：在奖励某种推理行为之前，应先检验该行为是否具有正向的 Behavioral Lift，即是否与正确答案稳定相关。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

推理导向后训练使语言模型和视觉语言模型能够先生成较长的推理轨迹再作答，并常常提高困难任务上的准确率。然而，开发者仅凭更长的轨迹、更多自我纠正或更明显的犹豫，无法判断模型是否形成了更可靠的推理机制。这会影响训练目标和评测指标的选择：若奖励的是“看起来更会思考”的表面行为，而不是与正确性稳定相关的行为，模型即使输出更复杂的过程，也可能仍然缺乏置信度校准、证据落地和恰当知识运用。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **结果准确率与思考型/指令型模型对比**：通过最终答案是否正确来比较推理导向模型与普通指令微调模型，判断延长推理或推理导向后训练是否提升任务表现。该方法能说明模型最终是否成功，却不能解释成功或失败对应了哪些过程行为。
- **基于认知行为分类或策略发现的推理轨迹分析**：已有研究从思维链中标注认知启发的行为、分析行为的可训练性，或自动发现模型采用的解题策略，以描述推理轨迹中出现了什么。它们主要刻画行为类型及出现情况，尚未充分区分行为的出现频率与其对答案正确性的关联强度。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 最终准确率把整个推理过程压缩为一个结果信号，无法识别模型是否经历了错误、如何恢复，也无法判断自我纠正、假设检验等更常见的行为是否真正与成功相联系；其后果是模型性能提升的行为机制仍不清楚。
- 仅统计行为是否被训练放大，容易把频率增长误解为推理质量提升。同一种行为可能由相反原因触发，例如自我纠正可能意味着有效恢复，也可能意味着先前更容易犯错；不确定性表达可能体现审慎，也可能反映困惑。因此，行为 prevalence 不能直接替代其对正确性的预测价值。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有分析缺少一个跨模型、跨文本与视觉语言任务的统一框架，用于同时回答两个彼此独立的问题：推理导向训练让哪些行为更常出现，以及这些行为在出现时是否更可能伴随正确答案。尤其缺少对“训练放大量”与“正确性关联强度”是否一致的系统检验，也缺少对模型发生推理失败后能否恢复这一潜在增益机制的量化。

</div>
<div markdown="1"><span>核心问题</span>

在语言模型与视觉语言模型中，推理导向训练是否优先放大那些与答案正确性关联最强的推理行为；如果没有，哪些行为被显著放大、哪些行为最能指示成功，以及思考型模型的收益是否部分来自失败后的恢复能力？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把“常见”与“有用”拆开：先用统一分类体系标记每条轨迹是否出现某种行为，再比较该行为出现和未出现时的正确率，以估计其 Behavioral Lift；随后将这一正确性关联与思考型模型相对指令型模型的行为频率变化对照。直观上，这类似于区分学生是否更频繁地写出某个解题步骤，以及写出该步骤的学生是否真的更容易答对，从而发现训练究竟增强了可靠推理信号，还是只增强了审慎、反思等表面形式。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文提出一个用于分析思维模型推理轨迹的行为标注与度量框架，而不是新的模型架构或训练算法。框架以模型对任务的完整回答及其推理过程为输入，先标注跨模态推理行为和模态相关失败模式，再分别计算行为出现频率、行为与正确性的关联强度，以及模型在出现推理失败时仍得到正确答案的恢复能力。直观地说，研究者不只检查答案是否正确，还检查模型是如何得到答案的，并区分“经常出现的行为”和“真正与正确答案更相关的行为”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 收集模型推理轨迹

对每条回答同时保留推理过程和最终答案，以便判断模型是否通过有效推理得到结论，而不是仅凭运气猜对。研究框架覆盖不同模型和基准，并按语言模型与视觉语言模型分别分析。

<div class="method-step__io" markdown="1">

**输入**：来自语言模型和视觉语言模型的任务输入、推理轨迹与最终答案；视觉语言模型的输入还包含图像。<br>
**输出**：带有推理轨迹、最终答案和模态信息的响应样本。

</div>

**直观理解**：这一步相当于同时保存学生的答题过程和最后答案；只看最后一项，无法发现“答案对了但理由错了”的情况。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 标注高阶推理行为

依据九种跨模态高阶行为进行存在性标注，包括规划、目标跟踪、假设检验、自我纠正、不确定性承认、置信度校准、自我认知、证据引用和知识对齐。九种行为按功能分为控制与调节、监控与判断、认识论基础三类，但这些类别描述的是可观察行为，不等同于模型内部真实认知机制。

<div class="method-step__io" markdown="1">

**输入**：每条模型推理轨迹。<br>
**输出**：每条轨迹对应的行为标签集合，以及各行为在不同模型或数据中的出现情况。

</div>

**直观理解**：标注者像检查解题步骤一样，判断模型是否拆分了问题、检查了备选解释、修正了错误，或把结论和题目证据联系起来。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 标注模态相关失败模式

对每条响应标注失败模式是否出现。语言模型和视觉语言模型共同使用逻辑失败、事后合理化、捷径和幸运猜测；视觉语言模型另标注视觉幻觉、视觉忽略和语言偏置，语言模型另标注事实错误、上下文误读和知识缺口。

<div class="method-step__io" markdown="1">

**输入**：已保留的推理轨迹、最终答案和相应模态的任务信息。<br>
**输出**：每条响应的失败模式向量，其中每个失败模式取存在或不存在；同时保留最终答案是否正确。

</div>

**直观理解**：这一步专门记录推理中的“坏步骤”，例如跳过必要过程、用答案倒推理由，或在视觉任务中没有真正使用图像。这样才能研究模型出错后是否仍可能答对。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算行为关联与恢复率

对每种行为计算 $Lift$，比较该行为出现与不出现时的正确率差异；对每个模型计算 $Recovery$，统计至少出现一种相关失败模式时仍然答对的条件概率。主分析将同一模态下各模型的样本合并计算 $Lift$，并补充按模态、基准和单模型的分析以检查稳定性。

<div class="method-step__io" markdown="1">

**输入**：行为标签、失败标签、最终正确性，以及模型和模态分组信息。<br>
**输出**：各行为的行为提升值、各模型的恢复率，以及跨模态和分组比较结果。

</div>

**直观理解**：行为出现得多，不代表它有用；$Lift$ 检查某行为出现时答对概率是否更高，$Recovery$ 检查模型即使推理中出现问题，最后还能否答对。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 行为提升

$$
\text{Lift}(b)=P(\text{correct}\mid b{=}\texttt{true})-P(\text{correct}\mid b{=}\texttt{false})
$$

**符号说明**

- $b$：某一种高阶推理行为，例如规划或自我纠正。
- $\text{correct}$：最终答案正确这一事件。
- $P(\text{correct}\mid b{=}\texttt{true})$：出现行为 $b$ 时最终答案正确的条件概率。
- $P(\text{correct}\mid b{=}\texttt{false})$：未出现行为 $b$ 时最终答案正确的条件概率。

<div class="equation-explanation" markdown="1">

**直观理解**：$Lift$ 用“出现行为时的正确率”减去“未出现行为时的正确率”。结果为正表示该行为与更高正确率相关，结果为负表示该行为出现时正确率反而更低，但该指标不能说明行为造成了正确或错误。<br>
**原文位置**：第2.3节，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 失败后的恢复率

$$
\text{Recovery}(m)=P(\text{correct}\mid\exists\,f\in\mathcal{F}_{\text{all}}:f{=}\texttt{true})
$$

**符号说明**

- $m$：待分析的模型。
- $\text{correct}$：模型最终答案正确这一事件。
- $f$：某一种失败模式。
- $\mathcal{F}_{\text{all}}$：对应模态的全部七种失败模式集合。
- $\exists\,f\in\mathcal{F}_{\text{all}}:f{=}\texttt{true}$：至少存在一种失败模式被标注为出现。

<div class="equation-explanation" markdown="1">

**直观理解**：$Recovery$ 只关注那些至少出现一种推理失败的回答，并计算其中最终答对的比例。数值较高说明模型有能力在推理过程存在问题时仍得到正确结论，但这不表示其推理过程可靠或失败模式无害。<br>
**原文位置**：第2.3节，公式(2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未报告新的模型训练目标、损失函数或参数优化过程。本文的方法是对既有模型输出进行行为和失败模式标注，再计算描述性统计指标，因此不适用训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 跨模态高阶行为分类器**

该模块使用九种模态中立的行为定义，对语言模型和视觉语言模型的推理轨迹进行统一标注：规划、目标跟踪、假设检验、自我纠正、不确定性承认、置信度校准、自我认知、证据引用和知识对齐。行为定义依据其在推理轨迹中的可观察作用，而不是假设它们对应某种特定内部认知机制。

> 直观理解：统一标签使语言推理和视觉推理可以直接比较。例如，自我纠正既可以指修正数学推导，也可以指修正对图像内容的判断。

**2. 模态特定失败模式标注**

该模块把失败模式表示为存在或不存在的离散标签。两种模态共享四类失败定义；视觉语言模型和语言模型分别加入与视觉理解和语言知识相关的三类特有失败，从而支持模态内的 $Recovery$ 分析。

> 直观理解：共同失败模式负责公平比较，不同模态的专有失败模式负责记录各自特有的问题。例如，视觉模型可能忽略图像，语言模型则可能出现事实错误或知识缺口。

**3. 行为质量度量**

该模块包含两个描述性指标：$Lift$ 衡量行为存在与正确性之间的条件概率差异，$Recovery$ 衡量出现至少一种失败模式后仍然正确的概率。作者明确指出 $Lift$ 不是因果效应，较高的 $Lift$ 可能只是因为模型本来就已经朝正确方向推理。

> 直观理解：这两个指标回答不同问题：$Lift$ 问“某种行为和答对是否相关”，$Recovery$ 问“出现错误推理迹象后，模型还能否答对”。它们不能单独证明某行为导致了正确答案。

**训练与推理**

训练阶段原文未明确报告，因为该框架不提出需要训练的分类器或生成模型。推理与分析阶段包括：收集模型推理轨迹和最终答案；按模态标注九种高阶行为及相应失败模式；记录答案正确性；按模型、模态、基准或合并样本计算 $Lift$ 与 $Recovery$，其中 $Lift$ 的主分析在每种模态内合并所有模型样本，补充分析再检查单个基准和单个模型中的稳定性。

**复现信息**

复现分析至少需要获得模型的完整推理轨迹、最终答案、任务正确性标签、模型与模态标识，以及按模态定义的七种失败模式标签。九种高阶行为使用跨模态统一定义，失败模式使用四种共享定义加三种模态特有定义；完整标签定义位于附录表24和表26。原文未明确报告标注者数量、标注协议、自动或人工标注方式、样本规模、阈值、具体聚合实现及置信区间，因此这些内容不能据此重建。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 视觉语言模型的三类基准构成从结构推理到知识密集推理的任务谱：VisualPuzzles 使用约 350 个样本测试视觉结构推理，MathVista 使用 testmini 划分中的 300 个样本测试视觉数学推理，MMMU 使用约 350 个样本测试多学科多模态知识。它们用于检验同一种行为在不同视觉推理需求下是否稳定出现。
- 语言模型的三类基准同样覆盖任务谱：LogiQA2 使用约 350 个样本测试逻辑与论证结构识别，MATH-500 使用约 350 个样本测试逐步数学计算，MMLU-Pro 使用约 350 个样本测试 14 个领域的知识密集推理。该组合用于区分“依赖逐步计算的任务”和“更依赖知识或模式匹配的任务”。
- 稳健性与扩展验证包括：在 MATH-500 的 250 道题上对 Qwen3-4B 每题生成 8 条轨迹，以控制题目难度；在 MATH-500 与 MMLU-Pro 上评估共享同一基础模型的 OLMo-3-7B Think-SFT 和 Instruct-SFT，共 $N=1{,}443$；在 MathVista 与 MATH-500 上进行 2B 至 32B 的规模分析；另在完整 GPQA-Diamond 的 198 道题、7 个模型上收集 $N=1{,}386$ 条回答作前沿模型补充验证。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**行为流行率及 thinking-minus-comparison 差值**

行为流行率是被裁判标为出现某行为的回答比例；两类模型的流行率差衡量思考训练是否选择性放大该行为。 （该指标没有统一的越高越好含义。更大的正差只表示思考型模型更常表达该行为，并不表示行为更有效或答案更正确。）

</div>
<div class="metric-item" markdown="1">

**Behavioral Lift**

比较某行为出现时与缺失时的准确率差，用于衡量该行为与成功回答的关联；论文还采用每题 8 条轨迹的题内 $\Delta$ accuracy，以控制题目难度。 （正值越大，行为出现与正确回答的正关联越强；负值表示该行为更常伴随错误。但这是观察性关联，不能直接解释为该行为导致正确或错误。）

</div>
<div class="metric-item" markdown="1">

**Recovery Rate**

在轨迹中至少检测到一次失败的条件下，最终答案仍然正确的比例，用于区分模型从中间错误中恢复的能力。 （越高表示模型在已经进入错误状态后越可能修复推理并得到正确答案；它不衡量无失败轨迹的基础正确率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 15 个开放权重模型、两种模态与全部六个主基准上的行为流行率比较

<div class="result-value" markdown="1">

思考训练选择性放大三类可见的审慎行为：思考型模型的自我纠正流行率约为 21% 至 55%，对照模型为 3% 至 15%；假设检验为 22% 至 52% 对 4% 至 18%；不确定性承认为 25% 至 85% 对 4% 至 28%。相反，置信度校准并未同步增加，例如 MATH-500 上思考型与指令型模型分别为 66.1% 和 67.9%，MMLU-Pro 上分别为 40.9% 和 46.7%。

</div>

作者据此主张，思考型后训练主要改变了模型“如何展示推理”，尤其增加回头修正、尝试不同假设和表达犹豫，而不是普遍提升所有高阶行为。通俗地说，模型更像是在认真思考，不代表它更常表现出与真实推理质量一致的信心。该结果是行为频率比较，不能单独证明这些行为由某个具体训练阶段导致，也不能证明更频繁出现就会提高准确率。

<div class="result-source" markdown="1">

来源：第 4.1 节；图 2；附录表 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Self-correction appears in roughly 21–55% of thinking-model responses versus 3–15% for comparison models, with consistently large thinking-minus-comparison gaps across benchmarks (Table 7). Hypothesis testing (22–52% vs. 4–18%) and uncertainty acknowledgment (25–85% vs. 4–28%) show comparable gaps.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨模态 Behavioral Lift、题内多轨迹对照及推理质量分层分析

<div class="result-value" markdown="1">

最常被思考训练放大的行为并非最能预测成功的行为。置信度校准在视觉语言基准上的 Lift 为 +72.2%，行为出现和缺失时准确率分别为 98.8% 与 26.7%；语言基准上的 Lift 为 +79.6%，对应 99.6% 与 20.0%。相比之下，不确定性承认的 Lift 在两种模态上分别为 -16.1% 和 -13.9%，假设检验均为 +1.0%，自我纠正仅为 +20.1% 和 +12.4%。同题控制中，置信度校准的题内准确率优势仍为思考型 +0.31、指令型 +0.52，而不确定性承认分别约为 +0.01 和 -0.09。

</div>

作者的核心结论是“被放大”与“具有预测性”是两个不同问题：频繁出现的搜索、犹豫和纠错行为可能只是困难或已犯错的信号，而置信度与实际推理质量一致才更稳定地伴随正确答案。题内比较降低了简单的题目难度混杂，因为比较发生在同一道题的不同采样轨迹之间；但行为仍不是随机施加的干预，所以较高 Lift 不能证明置信度校准本身造成正确答案。

<div class="result-source" markdown="1">

来源：第 4.2 节；图 3；表 2；附录表 10 至表 13、表 17 至表 18

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across VLM benchmarks, confidence calibration shows +72.2% Lift (98.8% accuracy when present vs. 26.7% when absent); across LLM benchmarks, +79.6% (99.6% vs. 20.0%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 按基准比较检测到中间失败后的 Recovery Rate

<div class="result-value" markdown="1">

思考型模型的优势具有明显任务依赖性：VisualPuzzles 的恢复率为 23.0% 对 8.4%，MATH-500 为 40.8% 对 17.8%，MMLU-Pro 为 16.8% 对 6.3%，约为指令型模型的 2.3 至 2.7 倍；MathVista 与 MMMU 两类模型接近；LogiQA2 则反转为 11.1% 对 24.5%。总体上思考型模型在六个主基准中的四个取得更高准确率，而 LogiQA2 上指令型模型以 58.4% 对 54.1% 领先。

</div>

这说明思考型模型并非总因“少犯错”而获益：在逐步计算任务中，它可能先走错，再凭后续检查修复；在更依赖快速识别论证结构的 LogiQA2 上，较长的审慎推理反而不占优势。恢复率只在已检测到失败的轨迹上计算，因此不能与整体准确率混为一谈；行为标签还依赖裁判能否从文本轨迹识别失败。

<div class="result-source" markdown="1">

来源：第 4.3 节；附录表 7、表 16；图 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On benchmarks that reward step-by-step computation, thinking models recover at 2–3× the rate of instruct models: VisualPuzzles (23.0% vs. 8.4%, 2.7×), MATH-500 (40.8% vs. 17.8%, 2.3×), and MMLU-Pro (16.8% vs. 6.3%, 2.7×).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 行为标签主要由 GPT-4o 根据可见文本轨迹生成。尽管核心行为经过三种独立裁判和人工核查，部分标签特别是自我觉察与组织性行为的跨裁判一致性较低；模型未写出的内部计算也无法由轨迹标注捕捉。
- Behavioral Lift、题内准确率差和恢复率主要是观察性统计，不能建立行为对正确率的因果作用。发布模型的完整后训练配方并未被逐阶段严格控制；即使 OLMo SFT 对照显示错位在 DPO/RLVR 前已存在，作者也明确指出它不能隔离任一训练阶段的单独因果贡献。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 同模型家族、参数规模尽量匹配的 instruction-tuned 非思考版本是主要基线。家族内比较尽量减少基础架构和预训练差异，使观察到的行为差异更接近后训练方式差异，但发布模型仍可能采用不同的完整后训练配方。
- OLMo-3-7B-Instruct-SFT 是训练阶段对照，与 OLMo-3-7B-Think-SFT 共享 OLMo-3-7B 基座且均处于后续 DPO 和 RLVR 之前，用于判断“放大行为不等于高预测性”的现象是否在 SFT 阶段已经出现。
- Qwen3-VL Instruct 与 Qwen2.5 Instruct 系列作为规模对照，分别与思考型视觉语言模型和语言模型比较，用于检验行为放大与 Behavioral Lift 的错位是否会随参数量增加而消失。
- 同一道题中“不含目标行为的轨迹”是题内分析基线：研究者比较同题多次采样所得的含行为与不含行为轨迹，从而降低不同题目难度同时影响行为出现率和正确率的混杂。

**实验想回答的问题**

- 思考型模型是否比同家族指令型模型更频繁地表现出自我纠正、假设检验和不确定性承认等高阶推理行为，以及这种“行为放大”能否由回答长度解释？
- 被思考训练放大的行为是否真正预测答题成功；思考型模型的性能收益究竟来自更少犯错，还是在检测到中间失败后更善于恢复？

**实验实现**

实验评估 15 个 3B 至 9B 的开放权重模型，包括 4 个思考型和 3 个非思考型视觉语言模型，以及 4 个思考型和 4 个非思考型语言模型，并在可用时进行同家族配对。所有模型在标准化推理条件下运行并保留完整轨迹；因少量输出解析失败，最终人工或自动标注对象为 15,282 条回答。GPT-4o 作为 LLM-as-judge，接收问题、标准答案和模型完整输出，依据预定义行为分类体系给出二元标签；置信度校准仅在模型表达的确定程度与轨迹所呈现的推理强度一致时标为真。作者用 DeepSeek-V3、Gemini-2.5-Flash 和 Gemini-3-Flash 在覆盖 8 个语言模型的 600 个分层 MATH-500 样本上做跨裁判验证，并人工核查 120 条分层轨迹。核心行为的跨裁判 $\kappa$ 为 0.51 至 0.82；人工核查对 720 个二元判断与 GPT-4o 的一致率为 95.1%，$\kappa=0.902$。这些验证支持核心标签的可用性，但自我觉察和部分组织性标签的一致性较低。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 按模态内共享词数五分位重新计算行为流行率差，以控制思考型回答通常更长这一混杂因素 | 控制长度后，语言模型的自我纠正、假设检验和不确定性承认在除最短组之外的四个词数分组中仍更常见于思考型轨迹；视觉语言模型中，自我纠正在 4/5 个分组保持放大，不确定性承认在 5/5 个分组保持放大，假设检验在 3/5 个分组保持放大。 | 该分析隔离了“轨迹越长，越有机会出现某行为”的机械效应。长度确实解释了一部分差异，尤其是最短回答中的差异，但不能完全解释主要放大模式。由于采用分箱而非严格匹配或随机控制，分组内仍可能存在内容难度、模型家族和生成策略差异。 | 附录 D，Length-Controlled Prevalence Analysis<br><span class="experiment-evidence">Length accounts for part of the pattern, especially among the shortest traces, but does not eliminate it: for LLMs, self-correction, hypothesis testing, and uncertainty acknowledgment remain more prevalent in thinking-oriented traces in each of the four non-shortest bins. For VLMs, self-correction remains amplified in 4/5 bins, uncertainty acknowledgment in 5/5, and hypothesis testing in 3/5.</span> |
| Qwen3-VL 2B 至 32B 的 MathVista 规模分析，并以指令型同规模模型作对照 | 32B 思考型模型在 61.3% 的回答中自我纠正，指令型为 11.3%，仍相差 50 个百分点；但自我纠正 Lift 从 2B 的 +30.0% 降至 32B 的 +5.9%，相关准确率优势从 18.3 个百分点缩至 1.7 个百分点。置信度校准 Lift 则由 2B 的 +57.7% 增至 32B 的 +68.7%。 | 该消融检验错位现象是否只是小模型能力不足的产物。随着规模增大，自我纠正仍被强烈放大，却越来越不能区分正确与错误轨迹；置信度校准的预测关联反而增强。因此，参数扩展没有让“最常展示的行为”自动变成“最有用的成功信号”。不过该比较不能排除不同规模模型训练数据或后训练配方的变化。 | 第 4.5 节；图 14<br><span class="experiment-evidence">At 2B, self-correction provides +30.0% Lift and an 18.3-point advantage. At 32B, self-correction Lift drops to +5.9% and the accuracy gap shrinks to 1.7 points. Confidence calibration Lift increases with scale (+57.7% at 2B to +68.7% at 32B), reinforcing the mismatch between amplified behaviors and high-lift behaviors.</span> |

**定性案例**

- LogiQA2 是“更多思考必然更好”的反例：指令型模型准确率为 58.4%，高于思考型的 54.1%，并更常采用有效捷径，比例为 34.2% 对 20.3%。作者将其解释为该任务更奖励快速识别论证结构；分析上，这说明较长、较审慎的轨迹并非普适优势，但单个基准不足以证明所有模式识别任务都会出现同样反转。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper analyzes whether amplified reasoning behaviors in thinking models reliably predict successful reasoning.; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`3de0df73699e9c3ef9c0f28c85f52c300ac048c59872bae02203e20bc1face97`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
