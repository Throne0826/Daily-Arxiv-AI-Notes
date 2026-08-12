---
title: "[论文解读] FaithformBench: Benchmarking Faithfulness of Mathematical Chain-of-Thought Autoformalisation"
description: "[arXiv 2608.10916][LLM 评测] 本文提出 FaithformBench，通过比较自动形式化系统对正确原始陈述与人为扰动后的错误陈述是否分别保持有效性和无效性，诊断系统引入错误或“静默纠错”的不忠实行为。"
arxiv_id: "2608.10916"
announcement_date: "2026-08-12"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-12T03:08:27.987417+00:00"
source_sha256: "431dd72239d36e3527fcba2477a2ddd5ae372e78961f7962b01cd569131fa0d5"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "自动形式化"
  - "数学思维链"
  - "忠实性评估"
  - "证明助理"
  - "有效性保持"
  - "无效性保持"
  - "静默纠正"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.10916</p>

# FaithformBench: Benchmarking Faithfulness of Mathematical Chain-of-Thought Autoformalisation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-12</span>
<span><strong>作者</strong> Rob Cornish, Iacopo Ghinassi, Po-Hung Yeh, Shuqi Liu, Qiyuan Xu, Haoxuan Yin, Dominik Wagner, Wenda Li, Yee Whye Teh, Luke Ong</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.10916v1) · [PDF 下载](https://arxiv.org/pdf/2608.10916v1) · **关键词** 自动形式化, 数学思维链, 忠实性评估, 证明助理, 有效性保持, 无效性保持, 静默纠正<br>
**代码**: [https://github.com/Ighina/FaithformBench](https://github.com/Ighina/FaithformBench)

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

本文提出 FaithformBench，通过比较自动形式化系统对正确原始陈述与人为扰动后的错误陈述是否分别保持有效性和无效性，诊断系统引入错误或“静默纠错”的不忠实行为。

**不用术语来说**：用 Lean 等证明助手检查大模型的数学推理时，首先要把自然语言推理翻译成形式化命题；但形式化命题能够被证明，并不代表它准确表达了原话。翻译系统可能改动变量类型、前提或结论，使原本错误的推理变成可证明命题，从而让本应发现错误的验证流程错误地放行该步骤。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出一种无需逐例人工形式化真值标注的忠实性评测思路：自动扰动原本正确的自然语言推理步骤以构造预期无效的输入，并同时检查正确输入的有效性保持与错误输入的无效性保持。
- 将评测目标聚焦于两类可明确诊断的失败：把正确输入译成错误命题的“错误引入”，以及把错误输入译成可证明命题的“静默纠错”；作者据此揭示当前自动形式化训练可能把忠实翻译与生成可证明命题混为一谈。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

自动形式化（Autoformalisation, AF）把自然语言数学推理步骤翻译成 Lean 等证明助理可读取的形式陈述，使证明助理能够检查这些陈述是否可证。该技术可用于验证大语言模型生成的思维链，但“可证”不等于“忠实”：形式陈述可能偏离原句，甚至通过改变变量类型、前提或命题含义，把错误推理悄然改写为可证明命题。因此，本文关注的核心不是证明搜索能力，而是如何可靠评估 AF 输出是否保留输入步骤的数学含义，尤其是否同时保留正确输入的有效性与错误输入的无效性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自动形式化（AF）**

将自然语言中的数学定义、命题或推理步骤转换为证明助理语言中的形式陈述。本文以单个自然语言推理步骤的翻译为基本评估对象。

</div>
<div class="concept-item" markdown="1">

**证明助理与可证性**

Lean、Rocq 和 Isabelle 等证明助理依据严格的形式逻辑检查命题能否由给定前提推出。可证性只保证形式陈述内部成立，不能保证它准确表达了原始自然语言。

</div>
<div class="concept-item" markdown="1">

**思维链验证**

思维链验证逐步检查大语言模型给出的自然语言推理，目标是定位其中不成立的步骤。若 AF 会把错误步骤改写成可证命题，后续证明助理就可能错误地放行该步骤。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个自然语言数学推理步骤 $x$，AF 系统生成证明助理中的形式陈述 $F(x)$，再由证明助理判断该陈述在其形式化前提下是否可证。本文所说的忠实性要求 $F(x)$ 与 $x$ 的含义一致；在其重点考察的判据下，原本有效的步骤应保持有效，原本无效的步骤也应保持无效。后者对于思维链验证尤为关键，因为评估系统必须允许错误暴露出来，而不能通过修改变量类型或其他语义成分将其“静默纠正”。现有评估通常把 AF 输出与人工核验的标准形式化进行比较，或利用大语言模型裁判和嵌入模型判断语义对齐；前者可靠但制作成本高，后者易扩展却缺少准确性保证，而且两类方法通常只处理已知正确的输入。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入 AF 系统的自然语言数学推理步骤。

</div>
<div class="notation-item" markdown="1">

**$F$**

将自然语言推理步骤映射为证明助理形式陈述的自动形式化系统。

</div>
<div class="notation-item" markdown="1">

**$F(x)$**

AF 系统针对输入步骤 $x$ 生成的形式陈述。

</div>

</div>

**直接相关的工作**

- **BEq 与 GTED**: 二者是文中列举的人工核验标准形式化数据集，可通过比较 AF 输出与人工 ground truth 来评估忠实性；这种路线通常可靠，但标注缓慢且昂贵。
- **Jana et al. (2025)**: 该类方法使用大语言模型裁判或嵌入模型检测 AF 输出与输入是否语义一致，具有速度和可扩展性优势，但原文指出其准确性缺少保证，并可能遗漏细微的形式化错误。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

自动形式化系统被用于逐步验证大语言模型的数学思维链，因此其输出不仅要能被证明助手处理，还必须保持原始自然语言步骤的含义。尤其当输入推理本身有错时，系统应忠实保留该错误，使证明助手能够拒绝它；若系统擅自修改类型或命题并生成可证明输出，整个验证机制就会掩盖而非发现推理错误。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **人工核验的标准形式化数据集**：由人工为自然语言陈述编写或检查对应的形式化表达，再把自动形式化输出与这些标准答案比较；文中以 BEq 和 GTED 为例。
- **神经语义评判方法**：使用大语言模型裁判或嵌入模型比较自然语言输入与形式化输出的语义是否一致，以较低成本批量判断翻译忠实性。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 人工标注通常可靠，但制作标准形式化答案缓慢且昂贵，难以扩展到大量数据、模型和新领域；神经裁判虽然快速可扩展，却缺少准确性保证，并可能漏掉细微但关键的形式化错误。
- 两类方法通常只评测已知正确的自然语言输入，因而无法检验系统是否会把错误输入“修正”为可证明命题；这恰好遗漏了思维链验证最需要识别的情形。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有评测缺少一种成本较低、可扩展、具有比神经裁判更明确的可靠性依据，并且能同时覆盖正确与错误输入的诊断方法。该方法不必解决一般语义等价性的全部难题，但至少应可靠暴露“错误引入”和“静默纠错”这两类关键不忠实行为。

</div>
<div markdown="1"><span>核心问题</span>

能否通过自动构造预期无效的自然语言推理步骤，并联合考察原始正确输入是否仍被译为有效命题、扰动错误输入是否仍被译为无效命题，可靠地诊断自动形式化系统对数学推理的忠实性及其静默纠错倾向？

</div>
<div markdown="1"><span>作者直觉</span>

直接判断自然语言与形式语言是否完全同义很困难，但从一个已知正确的步骤出发，定向修改数字等关键内容，可以低成本制造应当错误的对照输入。如果系统忠实翻译，原始版本应保持可证明，而扰动版本应保持不可证明；若两个版本都变得可证明，说明系统很可能在翻译时迎合“产出证明”的目标并偷偷修补了错误。该入口提供的是具有方向性的失败诊断，而非完整忠实性证书：原文明确指出，它不能覆盖所有语义漂移，并依赖足够强的证明器。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把自动形式化系统（AF）的忠实性定义为：系统不仅应把有效的自然语言推理步骤翻译成可证明的形式命题，还应避免把无效步骤翻译成可证明命题。评测从已知有效的推理步骤出发，自动生成预期无效的扰动版本，随后借助证明助手检查译文的可证明性，据此考察两种方向的保持能力：原始有效输入的有效性保持，以及扰动后无效输入的无效性保持。作者据此识别两类可被可靠检测的失败模式，即“错误诱导”和“静默纠正”；该程序不要求为每个样本人工编写标准形式化译文，但所给节选未披露扰动算子、判定规则及统计估计的完整形式。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造有效推理步骤集合

将这些有效步骤作为未扰动的正例，并作为后续自动扰动的起点。方法需要它们确实有效，才能把形式译文不可证明视为有效性未被保持的证据。

<div class="method-step__io" markdown="1">

**输入**：已知有效的自然语言数学推理步骤；具体数据来源与筛选流程在所给节选中未明确报告。<br>
**输出**：未扰动的有效输入集合。

</div>

**直观理解**：先准备一批原本没有逻辑错误的数学推理句子。它们既用于直接测试翻译，也充当制造错误版本的模板。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自动生成无效扰动步骤

对有效步骤施加自动扰动，生成被设计为无效的负例，以便在没有人工逐条标注形式化真值的情况下测试无效性保持。具体扰动类型、适用条件以及确保扰动无效的机制在所给节选中未明确报告。

<div class="method-step__io" markdown="1">

**输入**：未扰动的有效推理步骤。<br>
**输出**：与原步骤对应、预期无效的扰动推理步骤集合。

</div>

**直观理解**：这一步有控制地把正确推理改坏，相当于制作带有已知错误方向的测试题。随后可以观察系统会忠实保留错误，还是暗中把错误改成一个可证明的命题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 运行自动形式化系统

分别把正例和负例输入待评测的自动形式化系统，使其生成证明助手中的形式陈述。所给节选未说明提示模板、生成次数、解码策略、语法修复或失败重试流程。

<div class="method-step__io" markdown="1">

**输入**：未扰动的有效步骤与自动生成的无效扰动步骤。<br>
**输出**：每个自然语言步骤对应的形式化陈述，或可能出现的生成失败结果。

</div>

**直观理解**：同一个翻译器同时接受正确句子和被改坏的句子。关键不是要求译文逐字匹配某个标准答案，而是检查译文是否保留输入原有的有效或无效状态。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 证明助手判定与失败模式检测

利用证明助手检查形式陈述是否可证明，并比较输入预期有效性与输出可证明性：有效输入未产生可证明陈述对应“错误诱导”，无效输入却产生可证明陈述对应“静默纠正”。作者将检测结果用于估计两类失败模式流行程度的下界，但完整统计估计式及其弱假设在所给节选中未明确报告。

<div class="method-step__io" markdown="1">

**输入**：自动形式化系统生成的形式陈述，以及每个输入属于未扰动正例或扰动负例的信息。<br>
**输出**：有效性保持、无效性保持以及两类失败模式的检测结果与流行程度下界。

</div>

**直观理解**：证明助手在这里充当可机械核验的检查器。正确题被翻成不可证明内容说明翻译引入了问题；错误题反而被翻成可证明内容则说明系统没有忠实翻译，而是悄悄替输入纠错。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该工作在所给材料中被描述为一种评测基准与评估方法，而不是用于训练自动形式化模型的新目标函数；未报告通过该基准反向传播、微调模型或优化扰动生成器的训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 自动无效扰动生成器**

该模块从有效自然语言推理步骤生成被设计为无效的对应步骤，使评测同时覆盖正例与负例，并支持规模化构造测试数据。节选仅说明方法基于自动扰动，未给出扰动算法、无效性证明条件或质量控制程序。

> 直观理解：它负责系统地制造错误输入，从而检验翻译器面对错误时是否仍忠实，而不只检验它能否处理正确推理。

**2. 自动形式化系统接口**

该模块把自然语言推理步骤映射为证明助手中的形式陈述，并以同一评测流程处理未扰动与扰动输入。节选没有给出被评系统的输入输出协议、上下文设置或生成失败的记分办法。

> 直观理解：这是被考试的翻译器。评测关注它是否保留原句的逻辑状态，而不仅是最终形式命题能否通过证明助手。

**3. 证明助手验证与下界估计器**

证明助手对生成陈述进行可证明性检查，评测器再将该结果与输入的预期有效性对照，以检测“错误诱导”和“静默纠正”。作者声称该程序能在弱假设下可靠检测失败并估计其流行程度下界，但节选未提供这些假设及估计公式。

> 直观理解：该模块把主观的语言相似度判断改成机器可复核的证明检查。所谓“下界”表示它确认发现的失败至少有这么多，但不能据此断言所有未检出的样本都没有问题。

**训练与推理**

该方法主要在推理与评测阶段运行：先准备已知有效的自然语言推理步骤，再自动产生被设计为无效的扰动版本；随后把两类输入分别交给待评测的自动形式化系统，取得证明助手语言中的形式陈述；最后由证明助手检查陈述的可证明性，并按输入类别统计有效性保持与无效性保持。对于有效输入，若形式化结果不能维持可证明性，评测将其作为“错误诱导”的可检测证据；对于无效扰动输入，若系统输出可证明陈述，则将其作为“静默纠正”的可检测证据。这里的检测针对逻辑状态是否被保留，并不等同于确认译文在全部语义细节上与原句完全一致。所给节选没有提供任何新增模型的训练过程，也没有说明各自动形式化系统原有的训练数据或优化方法。

**复现信息**

复现所需的核心依赖包括：一组已知有效的自然语言数学推理步骤、能够生成预期无效负例的自动扰动程序、待评测的自动形式化系统，以及可检查生成陈述是否可证明的证明助手环境。公平比较时，应对所有系统使用相同的原始步骤、扰动样本和证明检查标准，并分别报告正例上的有效性保持与负例上的无效性保持，避免仅以可证明输出率评价系统。原文节选未明确报告证明助手及其版本、扰动算子、提示词、采样参数、超时设置、编译失败处理、下界估计公式和置信区间计算，因此无法据此给出更具体且可核验的复现配置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- FaithformBench以ProcessBench中经过人工标注为有效的思维链为来源，共构造12,784个自然语言推理步骤及其扰动对应项。每个原始步骤充当预期有效的正例，每个经过轻微修改、被设计为无效的步骤充当负例；评估不要求为每一步提供人工编写的Lean形式化真值。
- GSM8K与MATH分别覆盖较基础的文字算术问题和更复杂的竞赛式数学问题，用来比较系统随题目难度上升时的忠实性变化。原文节选未明确报告具体拆分、各子集样本数及抽样比例。
- OlympiadBench与OmniMath构成难度更高、数学表达更复杂的评估组，用来检验结论能否超出基础算术场景。由于任务限制，此处合并说明；原文节选未明确报告两个数据集各自的规模和拆分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**假负率（FNR）**

在原始、通常有效的步骤中，自动形式化结果被证明器证明其否定的比例，即满足$z_i=\bot$的样本比例。它测量系统是否在翻译过程中引入实质性错误；由于原始步骤只被假设为“高比例有效”，该指标是带弱假设的失败统计，而非逐例真值对照。 （越低越好，因为较低值表示系统较少把有效自然语言推理译成可被反驳的形式命题。）

</div>
<div class="metric-item" markdown="1">

**假正率（FPR）**

在被设计为无效的扰动步骤中，自动形式化结果反而被证明为真的比例，即满足$\bar z_i=\top$的样本比例。论文将其解释为“silent correction”或迎合性：系统没有忠实保留错误，而是生成了另一个可证明命题。 （越低越好，因为验证思维链时需要保留输入的无效性；高值可能有利于定理证明，却会掩盖原推理中的错误。）

</div>
<div class="metric-item" markdown="1">

**不忠实下界（UFLB）**

在全部$2N$个原始与扰动输入中，出现已观测失败事件的比例：原始输入被反驳或形式化失败，扰动输入被证明为真或形式化失败。它把FNR、FPR及自动形式化失败率AFFR聚合为整体统计，但没有把证明器无法判定的所有样本都直接视为不忠实，因此只称“下界”。 （越低越好，因为它表示被明确检测到的不忠实或无输出事件更少；但低UFLB不等于已经证明系统在其余样本上完全忠实。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四个专用自动形式化系统在GSM8K、MATH、OlympiadBench和OmniMath上的总体比较

<div class="result-value" markdown="1">

Goedel在四个数据集上的UFLB分别为0.14、0.19、0.20和0.21，均为专用系统中最低；StepFun约为0.19、0.34、0.34和0.33，Kimina为0.24、0.40、0.44和0.45，Herald为0.35、0.46、0.49和0.50。作者指出，Goedel的领先主要来自更低的FNR和AFFR，而不是更好的无效性保持，因为它同时具有最高的FPR。

</div>

专用模型中，Goedel最少出现被基准明确捕获的总体失败，但这不能解释为它最忠实地照译输入。它更擅长产出可证明、可编译的命题，同时也更可能把错误输入改成正确命题。因而，只检查形式化结果能否证明，会高估它在思维链验证任务中的可靠性。

<div class="result-source" markdown="1">

来源：第6.1节，图3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Notice that Goedel attains this lead despite having the highest FPR, with its advantage driven by its much lower FNR and AFFR.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 四个通用前沿模型与最佳专用系统Goedel的比较

<div class="result-value" markdown="1">

Claude Opus 4.7的四个数据集UFLB为0.09、0.12、0.13和0.14，Gemini 3.1 Pro为0.08、0.14、0.16和0.18；两者在每个数据集上都低于Goedel的0.14、0.19、0.20和0.21。GPT 5.2与Qwen Plus的UFLB较高，分别为0.14至0.26和0.17至0.35，说明“通用模型”本身并不自动保证最佳表现。

</div>

最强的两个通用模型不仅较少把扰动错误修正为真命题，也能维持较低的FNR和形式化失败率，因此整体下界优于所有专用模型。该结果支持“专用微调可能强化面向可证明性的纠错偏好”，但实验没有控制参数量、上下文长度、训练数据和推理预算，不能据此确定因果来源。

<div class="result-source" markdown="1">

来源：第6.2节，图4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The models with the lowest UFLB, Claude Opus 4.7 and Gemini 3.1 Pro, improve on the best specialised AF (Goedel) on every dataset, driven primarily by substantially lower FPR, while keeping FNR and AFFR low at the same time.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 原始步骤与扰动步骤的成对列联分析

<div class="result-value" markdown="1">

Goedel在GSM8K、MATH、OlympiadBench和OmniMath上的Faithfulness比例依次为71.2%、46.9%、37.3%和36.8%，Sycophancy比例依次为21.4%、20.8%、18.0%和15.8%。其余专用模型在较难数据集上出现大量Inconclusive，例如Kimina在MATH、OlympiadBench和OmniMath上分别为58.5%、70.0%和64.8%。

</div>

成对分析区分了系统是否同时正确处理一个原始步骤及其错误版本。Goedel得到更多“原始有效、扰动无效”的忠实配对，但仍有约六分之一至五分之一的配对表现为迎合；其他模型的大量Inconclusive主要说明形式化或证明链路没有给出足够结论，而不是证明这些输出忠实或不忠实。该分析也表明单独看FNR或FPR会遗漏两类输入之间的联合行为。

<div class="result-source" markdown="1">

来源：第6.3节，图5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Overall, the patterns from the figures reflect the previously reported results, with Goedel leading across the board on Faithfulness and presenting the least Inconclusive, while also having the highest sycophancy rate for MATH, OmniMath and OlympiadBench.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 基准的解释依赖两个弱假设：原始步骤中高比例有效，扰动步骤中高比例无效。ProcessBench为前者提供人工标注支持，但节选未报告对全部扰动的人工有效性审计；若扰动仍然成立，FPR会把忠实翻译误计为“悄悄修正”。
- 指标还受DeepSeek-Prover-V2覆盖能力影响。$\varnothing$可能来自命题不可判定、搜索超时、证明器能力不足或形式化失败，而不一定直接表示模型语义不忠实；UFLB只聚合已观察到的失败事件，因此不能作为真实不忠实率的完整估计。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Goedel（8B）是专门微调的自动形式化系统，也是专用模型中的主要强基线；已有研究认为它具有较强的有效命题形式化能力，因此可检验“可证明性强”是否等同于“忠实性高”。
- Herald、Kimina与StepFun（均为7B）代表另外三种专用自动形式化方法。它们与Goedel的比较用于判断错误修正现象是单一模型问题，还是专用训练范式下的普遍倾向。
- Claude Opus 4.7与Gemini 3.1 Pro是未针对自动形式化专门微调的通用前沿模型；它们是关键对照，因为可以检验更大的通用模型是否在保持输入语义方面优于专用小模型。
- GPT 5.2与Qwen Plus补充通用模型对照，用于避免把某一家模型的表现误认为通用模型整体规律。原文未公开这些闭源模型的参数规模，只说明它们远大于专用自动形式化模型。

**实验想回答的问题**

- FaithformBench能否在没有逐例人工形式化真值的条件下，区分自动形式化系统的三类关键失败：把原本有效的自然语言推理译成可被反驳的命题、把无效扰动“悄悄修正”为可证明命题，以及无法生成语法正确的形式化输出？
- 专用自动形式化模型与通用前沿大模型在有效性保持、无效性保持和整体不忠实程度上有何差异？尤其要检验：擅长生成可证明命题是否会以更强的迎合性，即修正错误输入，为代价。

**实验实现**

对每个原始推理步骤$x_i$，基准生成轻微修改后的$\bar x_i=\mathrm{Pert}(x_i)$；扰动既包括基于大模型的方法，也包括基于正则表达式的确定性方法。待测系统分别形式化$x_i$与$\bar x_i$，再由DeepSeek-Prover-V2尝试证明形式命题及其逻辑否定：证明原命题记为$\top$，证明否定记为$\bot$，两者均未证明或形式化为空记为$\varnothing$。实验评估4个专用自动形式化模型和4个通用前沿模型。作者称每项FNR、FPR、AFFR和UFLB统计至少基于1,282个数据点，95%置信区间半宽不超过0.03，因而未绘出置信区间；这说明抽样误差较小，但不处理扰动有效性、证明器能力或模型版本等系统误差。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 图2的GSM8K案例把原步骤“$Tue=4+1$”扰动为错误步骤“$Tue=4/2$”。评估流程将相关父节点和目标步骤形式化为直接命题及其否定，证明器未能证明直接版本，却成功证明其否定，因此该样本被判为保留了扰动后的无效性。该案例说明基准检查的不是生成文本是否表面相似，而是形式化结果是否保持原步骤的真假关系；它仅展示流程，不能代表总体错误率。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The central contribution is a benchmark for evaluating faithfulness of mathematical chain-of-thought autoformalization, including preservation of both valid and invalid reasoning.; rule check: matched taxonomy keywords; top rule score=5.0
- 全文指纹：`431dd72239d36e3527fcba2477a2ddd5ae372e78961f7962b01cd569131fa0d5`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
