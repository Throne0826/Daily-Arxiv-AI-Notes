---
title: "[论文解读] Explanations, Prompts, and Formalizations: Arguments for New Norms in LLM-Enabled Mathematical Research"
description: "[arXiv 2608.29401][LLM Reasoning] 本文主张为大语言模型参与的数学研究建立更严格的发表规范：人类作者不仅应披露模型版本、完整提示词与运行框架，还应提供可机器核验的形式化证明，并主动写出突出关键创新的直观解释。"
arxiv_id: "2608.29401"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:53:56.188750+00:00"
source_sha256: "15d29ef099e13c512ca49d966b4ee15bbc4006c1702768852c16f259d1dac9f1"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型辅助数学研究"
  - "数学证明形式化"
  - "Lean"
  - "可复现性"
  - "数学解释"
  - "科学出版规范"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.29401</p>

# Explanations, Prompts, and Formalizations: Arguments for New Norms in LLM-Enabled Mathematical Research

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Axel Boldt</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Address: Department of Mathematics and Statistics；Metropolitan State University, Saint Paul, Minnesota, U.S.A</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.29401v1) · [PDF 下载](https://arxiv.org/pdf/2608.29401v1) · **关键词** 大语言模型辅助数学研究, 数学证明形式化, Lean, 可复现性, 数学解释, 科学出版规范<br>
**代码**: [https://github.com/openai/cdc-lean](https://github.com/openai/cdc-lean) · **项目页**: [https://arxiv.org/abs/2602.05192v2](https://arxiv.org/abs/2602.05192v2)

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

本文主张为大语言模型参与的数学研究建立更严格的发表规范：人类作者不仅应披露模型版本、完整提示词与运行框架，还应提供可机器核验的形式化证明，并主动写出突出关键创新的直观解释。

**不用术语来说**：大语言模型已经能够提出证明或反例，但读者看到最终答案后，仍可能不知道它为什么成立、机器如何得到它，也无法可靠检查其中是否藏有错误。如果论文只公布看似完整的证明，却不公开提示词、模型和辅助软件，其他研究者便难以复查发现过程或学习有效做法；如果又缺少形式化验证和人类解释，数学成果即使结论正确，也未必真正转化为可检验、可复用的人类知识。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出三项相互补充的规范性要求：公开模型的精确版本、完整提示词及运行框架；将新结果形式化到可由证明助理核验的程度；由人类作者提供强调新思想、相关前人工作和结果意义的直观解释。
- 作者把披露计算设置视为数学研究方法透明度的一部分：即使大语言模型输出具有随机性，公开设置仍可让他人多次重复实验、比较输出并积累提示与多智能体协作经验，而不应因无法做到逐字复现就放弃披露。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型（LLM）辅助数学研究、数学证明形式化与科学出版规范的交叉领域。数学研究通常以自然语言提出定义、定理、证明和反例；而形式化数学则把这些内容编码到如 Lean 的形式语言及其数学库 mathlib 中，由证明检查器自动验证推理。本文讨论的核心背景是：LLM 已能够参与数学猜想的证明或反驳，但由此产生的结果不仅需要数学正确性，还涉及发现过程是否透明、证明是否可机器核验，以及人类读者能否真正理解其新颖思想。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大语言模型（LLM）**

LLM 是根据大量文本训练、能够生成自然语言和数学文本的人工智能系统。在本文语境中，它可以根据提示搜索已有工作、提出证明思路，并生成证明或反例，但输出可能错误、不完整或难以解释。

</div>
<div class="concept-item" markdown="1">

**数学形式化与 Lean**

数学形式化是把定义、命题和证明转换为具有严格语法与逻辑规则的计算机可检查对象。Lean 是一种形式化证明语言，证明检查器可以核验证明是否遵守其基础逻辑；mathlib 则是其中可复用的大型数学定义、定理和证明库。

</div>
<div class="concept-item" markdown="1">

**提示词、harness 与可复现性**

提示词是发送给 LLM 的指令，harness 是负责与模型交互并根据输出提供后续提示、数据或工具的软件系统。即使模型版本、提示词和 harness 全部公开，LLM 输出仍可能具有随机性；但公开这些信息可以让他人重复运行多次并比较结果。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文不是提出一个需要训练或评测的算法，而是分析一种出版与研究实践问题：当数学结论由 LLM 全部或部分产生时，作者应公开哪些信息并承担哪些解释责任。其输入是 LLM 参与数学研究的具体过程及其产物，包括提示词、模型版本、harness、自然语言证明或反例，以及可能的 Lean 形式化；其目标输出是可供人类理解、同行核查和机器验证的数学研究记录。文章关注的基本假设是，LLM 生成的结果可能正确但难以理解，也可能遗漏相关文献、包含缺陷，或无法直接纳入现有形式化数学库，因此单独发布一个结论或一份未经整理的模型文本不足以满足高质量数学传播与审查的要求。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$LLM$**

大语言模型（large language model）。

</div>
<div class="notation-item" markdown="1">

**$Lean$**

用于表达和检查形式化数学定义、命题与证明的证明助手语言。

</div>
<div class="notation-item" markdown="1">

**$mathlib$**

Lean 生态中的大型数学库，包含可复用的定义、定理和证明，并遵循便于后续形式化工作的规范。

</div>
<div class="notation-item" markdown="1">

**$n$**

单位距离猜想背景中的平面点数；文中讨论的是由 $n$ 个平面点构成的点集及其距离为 $1$ 的点对数量。

</div>

</div>

**直接相关的工作**

- **First Proof 项目及其 Second Batch**: 该项目发布研究级数学问题并收集 LLM 解答，用于检验 LLM 独立解决数学问题的能力。文中将其作为现实案例，指出许多解答存在缺陷，且第二批问题采用多位独立盲审专家评估，同时公开了提示词和 harness，说明研究过程披露对判断结果质量具有直接作用。
- **Leiden Declaration on Artificial Intelligence and Mathematics**: 该声明代表数学共同体对 LLM 参与数学工作的已有规范，包括披露 LLM 使用、追查模型遗漏的先前工作，以及在可行和适当时提供形式化证明。本文的研究动机正是认为这些规范仍不够具体：尤其应明确公开精确的软件设置和提示词，并更坚定地要求机器可验证的形式化结果及人类撰写的直观解释。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型开始独立解决研究级数学问题，相关成果可能迅速进入传播、评审和发表流程。由于模型会生成错误证明、遗漏引用，并可能把常规推导写得很长却略过真正的新步骤，评审者和读者需要同时判断结论是否正确、成果如何产生以及它是否增进了人的数学理解；否则，大量低成本自动生成的工作可能加重评审负担，并使关键发现过程掌握在少数拥有未公开提示技术和软件配置的人手中。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **既有数学出版与莱顿宣言式规范**：现有规范要求作者披露使用了大语言模型，尽力追查模型未注明的前人工作，并在可行且适当时提供形式化版本。这些要求主要解决作者责任、引用完整性和形式核验的原则问题。
- **证明助理形式化与公开推理材料**：研究者可把定义、定理和证明编码为 Lean 等形式语言，由计算机逐步检查；部分项目还公布模型的思维链、提示词或技术报告，以帮助外界理解生成过程。进入 mathlib 前通常还需“规范化”，即把原始形式化整理成符合库内约定、便于后续复用的版本。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有规范只要求披露使用了大语言模型，并未普遍要求公开精确模型版本、完整提示词和运行框架。仅发布思维链不能还原系统受到的指令、工具与反馈机制，导致他人难以重复实验、比较结果或学习有效的提示与智能体协作方法，并可能使提示技术变成少数内部人员掌握的“秘密技艺”。
- 形式化通常只是“可行且适当时”提供，而且原始形式化未必达到可并入 mathlib、可供后续证明复用的标准；与此同时，机器生成的自然语言证明即使通过形式检查，也可能缺少对核心新技巧、前人脉络和数学意义的解释。因此，机器核验只能回答证明步骤是否合规，不能自动产生人类所需的理解。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有数学共同体规范尚未形成一套覆盖“发现过程可审查、结论可机器核验、思想可被人理解”三个层面的统一责任框架。尤其缺少对精确软件设置和提示材料的强制透明要求，也没有把人类撰写直观解释明确视为大语言模型辅助成果的必要组成部分。

</div>
<div markdown="1"><span>核心问题</span>

当数学定理、证明或反例主要由大语言模型获得时，作者和出版体系应要求披露与补充哪些材料，才能在模型输出具有随机性且可能晦涩或出错的条件下，保障成果的透明度、可核验性、可学习性与人类理解？

</div>
<div markdown="1"><span>作者直觉</span>

作者的出发点是把大语言模型辅助发现同时看成数学论证和计算实验：像数学论证一样，它需要形式化检查来排除隐藏错误，并需要概念解释来揭示真正的新思想；像带随机性的实验一样，它虽不能保证每次产生相同文本，仍应完整记录模型版本、提示词和运行框架，使其他人能够重复运行并比较结果。三类材料分别回答“是否正确”“如何得到”和“为什么重要”，合在一起才使机器产出的答案成为公共数学知识。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是提出或训练一个新的大语言模型，也没有给出可执行算法；其“方法”是规范性论证：先用近期由大语言模型参与解决数学问题的案例，识别当前发表实践中缺失的信息，再以“扩大人类数学理解、提高正确性并使发现过程可复查”为判断原则，推出三项作者责任。最终输出是一套面向大语言模型辅助数学研究的发表规范：提供人类可理解的解释、机器可检查的形式化，以及完整披露模型版本、提示词和交互软件。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 界定问题并收集代表性案例

作者比较这些案例公开了哪些材料，例如自然语言证明、思维过程、提示词、交互软件和 Lean 形式化，并记录其信息缺口。该步骤属于案例驱动的规范分析，而不是系统综述或统计实验。

<div class="method-step__io" markdown="1">

**输入**：近期大语言模型参与数学研究的公开案例，包括 First Proof、单位距离猜想、循环双覆盖猜想和 Jacobian 猜想等。<br>
**输出**：对现行披露实践不一致性的案例性证据，以及需要进一步规范的关键对象。

</div>

**直观理解**：作者把几次具有代表性的研究发布当作样本，检查别人能否看懂、核验并大致复现其发现过程。目的不是给案例排名，而是找出发表流程中反复缺少的材料。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 评估既有规范的覆盖范围

作者将现有要求与案例中的实际缺口对照：已有规范强调披露大语言模型使用、追查既有文献，并在可行时提供形式化，但没有充分要求公开精确提示词与软件环境，也未把机器可验证形式化确立为普遍责任。

<div class="method-step__io" markdown="1">

**输入**：Leiden Declaration 等已有建议，以及 mathlib、Lean 和形式化“典范化”实践。<br>
**输出**：三个待补足的规范缺口：解释不足、形式验证要求偏弱、生成过程披露不完整。

</div>

**直观理解**：这一步相当于拿现有检查表去审查真实论文，确认哪些重要问题尚未被检查表覆盖。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 依据人类理解与可靠性原则推导作者责任

作者以促进人类理解、提高数学正确性的可信度、保存发现过程的可学习性为原则，分别论证解释、形式化和过程披露为何应由报告结果的人类作者负责。作者同时讨论形式化并非绝对保证、随机生成无法完全复现等限制，但认为这些限制不推翻相应要求。

<div class="method-step__io" markdown="1">

**输入**：前述规范缺口，以及大语言模型证明可能存在隐蔽错误、叙述详略失衡和引用不完整等风险。<br>
**输出**：三项核心责任及其适用理由与边界。

</div>

**直观理解**：即使机器给出了答案，人类作者仍要回答三个问题：为什么这个证明有意义、机器是否真的证明了目标、别人怎样重复或研究这一发现过程。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 形成可执行的发表规范

作者提出发布大语言模型所得数学成果时，应附人类撰写的直观解释、可由证明检查器验证的形式化，并披露精确模型版本、全部提示词及所用交互软件版本；对于符合 mathlib 规范的典范化形式化，则仅列为最佳实践而非强制要求。

<div class="method-step__io" markdown="1">

**输入**：三项核心责任及对公平性、成本和不可完全复现性的反对意见。<br>
**输出**：供作者、审稿人与出版流程采用的规范性清单。

</div>

**直观理解**：最终建议不只是“说明用了 AI”，而是要求同时交付讲解材料、核验材料和实验记录；但作者没有要求每位研究者都完成专业门槛更高的 mathlib 典范化工作。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文是关于大语言模型辅助数学研究发表规范的立场与论证文章，没有模型参数、损失函数、优化目标或训练过程；原文也未提出用于量化三项规范的目标函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 人类解释**

人类作者应重新组织大语言模型生成的证明：补充相关文献和结果意义，突出真正新颖的步骤，压缩例行计算，并在适合时提供概念说明或图示。作者还必须完整理解论证并对最终正确性承担责任。

> 直观理解：模型常把熟悉的步骤写得很长，却跳过最关键的新想法；人的任务不是润色文字，而是把证明变成其他数学家能够理解、评价和继续使用的知识。

**2. 机器可验证形式化**

作者主张把定义、定理陈述和证明编码到 Lean 等形式语言中，由证明检查器自动核验。形式化仍可能错误地表达原命题，检查器内核也可能有漏洞；因此它提高可信度和可检查性，却不构成绝对正确性的保证，符合 mathlib 复用规范的典范化仅被视为最佳实践。

> 直观理解：自然语言证明像人工检查的程序说明，形式化则更接近可由计算机逐步验收的代码。它不能消除所有风险，但能显著减少隐藏在长篇新论证中的逻辑漏洞。

**3. 提示词与交互环境披露**

发布材料应说明精确的大语言模型版本、完整提示词序列，以及交互软件的具体版本和行为；这里的交互软件是依据模型先前输出继续提供提示、数据或工具的程序。作者承认生成具有随机性，完全重现同一输出通常不可行，因此复查方式是重复运行多次并比较结果。

> 直观理解：只公布最终证明而隐藏提示词和工具配置，就像只公布化学产物却不写实验装置与步骤。完整记录不能保证每次得到相同答案，但能让其他研究者学习方法、重复尝试并判断结果是否稳定。

**训练与推理**

不适用。本文没有训练或推理算法，也没有运行新的大语言模型实验。文中所述模型、提示词、多代理协作、对抗复核和 Lean 形式化均来自被讨论的外部案例；它们被用来支持规范性判断，而非组成作者实现的一条计算流水线。

**复现信息**

若将作者建议落实为可审查的发布流程，最低限度应归档：精确模型版本、全部提示词、交互软件及其版本、工具或数据提供方式、模型生成的数学论证、人类解释和机器可检查的形式化。由于输出并非完全确定，复核者应在相同已披露配置下进行多次重复并比较输出；原文没有规定重复次数、随机种子、采样参数、硬件环境、形式化文件格式或验收阈值。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 原文未明确报告用于实验评估的数据集、数据规模或训练集与测试集划分；文中仅讨论 First Proof 项目的两批数学问题，其中第二批包含十道问题，但这些问题被作为背景案例而非本文的实验数据集。
- 原文未明确报告本文自行构建的任务数据集、问题采样标准或可复现实验划分。
- 原文未明确报告用于统计检验或人工评测的独立数据集。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

原文未明确报告，或这里不需要额外前置概念。

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 缺少本文自己的数据集、基线、指标和受控实验，因而无法量化解释、形式化、提示词披露或 harness 披露对正确性、可复现性和人类理解的具体影响。
- 文章主要依赖少数近期案例和原则性推理；原文未明确报告案例选择标准、专家评测流程或系统化的反例分析，因此其规范性建议仍需要更大规模、可重复的实证研究检验。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告本文设置的模型基线或传统数学研究基线。
- 原文提及 First Proof 第二批测试了四个系统，但这些系统并非本文实验中的受控基线比较；原文也未给出系统名称、统一实验协议或本文重新评测结果。
- 原文提及非形式化证明与 Lean 形式化证明之间的可靠性差异，但未将二者设置为可量化比较的实验条件。
- 原文讨论公开与不公开提示词、模型版本和 harness 的不同做法，但未进行对照实验。

**实验想回答的问题**

- 原文未设计实证实验来比较不同数学研究流程、提示词、模型或形式化方案的效果。
- 原文未通过数据集、基线和定量指标检验其关于解释、形式化以及披露提示词与软件设置的规范性主张。

**实验实现**

本文是关于 LLM 辅助数学研究规范的论证性文章，而非实验研究。原文未报告模型训练或推理配置、提示词实验方案、软件版本、随机种子、评测协议、统计显著性检验或可复现实验脚本。文中引用了若干外部案例，包括 First Proof、Erdős 的单位距离猜想、环双覆盖猜想和 Jacobian 猜想，但这些材料用于说明披露、解释与形式化的必要性，而不是构成本文的实验结果。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- Erdős 单位距离猜想、环双覆盖猜想和 Jacobian 猜想被用作对比性案例：前者发布了 Chain-of-Thought 文档但未公开确切模型版本、提示词和 harness，随后才有 Lean 形式化；环双覆盖猜想公开了完整提示词以及 Lean 形式化，但未公开模型版本；Jacobian 猜想的反例最初只在社交媒体发布，缺少展开说明。作者借此说明，数学结果的发表不应只提供结论或证明文本，还应让读者了解发现过程、验证机制和直观意义。不过这些案例没有经过本文统一的控制条件或量化评测，因此只能支持规范性讨论，不能证明某一种披露方案在统计意义上优于另一种方案。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：围绕LLM辅助数学研究提出提示披露、形式化验证和可理解解释等规范，核心涉及LLM数学推理结果的验证与解释。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`15d29ef099e13c512ca49d966b4ee15bbc4006c1702768852c16f259d1dac9f1`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
