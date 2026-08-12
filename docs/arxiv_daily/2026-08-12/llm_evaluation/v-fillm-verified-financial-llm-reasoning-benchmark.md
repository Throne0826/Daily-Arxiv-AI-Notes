---
title: "[论文解读] V-FiLLM: Verified Financial LLM Reasoning Benchmark"
description: "[arXiv 2608.11047][LLM 评测] V-FiLLM旨在解决金融表格推理基准难以区分模型推理缺陷与数据噪声、且难以低成本扩展的问题，其核心切入点是用基于表格数值的可执行计算树自动生成问题并以符号执行得到可验证答案。"
arxiv_id: "2608.11047"
announcement_date: "2026-08-12"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-12T03:04:29.705499+00:00"
source_sha256: "ea00926a93517daa63d10b7617568ab28043311f1f824d2fbe84175d79f7bfb0"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "金融表格问答"
  - "大语言模型评测"
  - "组合推理"
  - "可执行计算树"
  - "自动验证答案"
  - "可控难度"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.11047</p>

# V-FiLLM: Verified Financial LLM Reasoning Benchmark

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-12</span>
<span><strong>作者</strong> Alicia Larsen, Victoire Laurent, Aulia Kharis Rakhamsari, Lara Turgut, Nino Antulov-Fantulin</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: ETH Zürich, Zürich；Affiliation: Aisot Technologies Ltd {alarsen, vlaurent, arakhmasari</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.11047v1) · [PDF 下载](https://arxiv.org/pdf/2608.11047v1) · **关键词** 金融表格问答, 大语言模型评测, 组合推理, 可执行计算树, 自动验证答案, 可控难度<br>
**代码**: [https://github.com/auliakharis/ML-in-Finance-and-Complex-System](https://github.com/auliakharis/ML-in-Finance-and-Complex-System)

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

V-FiLLM旨在解决金融表格推理基准难以区分模型推理缺陷与数据噪声、且难以低成本扩展的问题，其核心切入点是用基于表格数值的可执行计算树自动生成问题并以符号执行得到可验证答案。

**不用术语来说**：回答金融表格问题不只是做算术：模型需要先从正确的行列取数，理解毛利润、营业利润和净利润等概念，再按正确顺序完成多步计算。现有测试题通常由人工标注或模型辅助抽取，因此一道题答错，可能是模型不会推理，也可能是原表格式混乱、数值缺失、题目有歧义或标准答案本身不可靠；与此同时，人工制作大量覆盖不同难度的题目成本很高。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出确定性的金融推理基准生成框架：从表格数值出发采样可执行计算树，通过符号执行自动获得标准答案，再将计算过程渲染为自然语言问题，从而将模型排除在答案标注环节之外。
- 使基准能够按计算深度、表达式宽度、金融概念复杂度和上下文规模四个轴控制难度，以便分别考察组合推理、领域知识以及对表格上下文的处理能力。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于金融表格问答与大语言模型组合推理评测领域。此类任务要求模型从结构化财务表格中定位正确数值，理解毛利润、营业利润和净利润等领域概念及其计算关系，再对金额、比率和百分数等异质量执行多步运算。它与一般数学题的关键区别在于：错误既可能来自表格检索，也可能来自财务概念理解或运算组合，因此需要能够区分这些能力来源、并可系统调节推理难度的基准。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**金融表格问答**

给定财务表格和自然语言问题，模型需要读取相关单元格并计算答案。问题通常不只是查找某个数值，还会要求根据财务公式完成多步推导。

</div>
<div class="concept-item" markdown="1">

**组合推理**

组合推理是把多个检索或算术步骤按依赖关系连接起来，例如先计算毛利润，再用它推导营业利润。计算链越深，模型越需要正确保留并使用中间结果。

</div>
<div class="concept-item" markdown="1">

**可执行计算树**

计算树以表格数值为叶节点、以算术或财务运算为内部节点，并可由程序逐层求值得到根节点答案。由于答案直接来自符号执行，这种设计能够自动核验标签，并明确控制运算步骤和表达式结构。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是在结构化财务表格上进行自然语言数值推理的大语言模型。基准生成器以电子表格中的数值为基础，采样可执行计算树，通过符号求值得到确定的标准答案，再把计算关系渲染为自然语言问题；被测模型接收表格上下文与问题，输出数值答案或相应推理结果。该设置假定生成树中的运算和财务概念定义可执行且确定，从而把答案正确性建立在程序计算上；同时可分别调节计算深度、表达式宽度、金融概念复杂度和上下文规模，以观察模型失败究竟来自长链组合、复杂表达式、领域知识还是信息检索负担。引言将数据载体描述为合成财务电子表格，而摘要称计算树以真实表格为依据，两处表述存在口径差异，需结合完整方法章节进一步核对。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **FinQA**: 面向财务报告的多步数值推理基准，是本文最直接的金融问答参照之一；其样本依赖人工标注，难以低成本扩展并系统控制推理深度，而本文试图用可执行计算树自动生成和验证答案。
- **TAT-QA**: 评测金融领域表格与文本混合证据上的问答能力，体现了真实金融材料中的异构信息需求；本文聚焦可控的表格组合推理，以减少格式异常、缺失值和歧义措辞等源数据噪声对推理能力诊断的干扰。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

金融决策场景要求模型可靠地处理结构化表格，但此类任务同时包含数值定位、金融公式理解以及跨金额、比率和百分率的多步组合运算。研究者因此需要一种能够稳定提供正确答案、覆盖多种推理复杂度，并能明确诊断模型失败来源的评测工具。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **人工标注的真实金融文档问答基准**：从真实财报、表格及配套文本中选择信息，由人工编写问题、推理过程或答案；这类数据保留了真实业务材料的结构与语言特征，代表性工作包括文中引用的 FinQA、ConvFinQA、FinanceBench 和 TAT-QA。
- **模型辅助或启发式抽取的金融问答基准**：借助模型或预设规则从真实文档中抽取数值、问题与答案，以减少完全人工构建的工作量；其标准答案仍依赖生成模型输出或启发式抽取结果，而非由一个可执行程序直接验证。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 真实文档中的格式异常、缺失值和歧义表述会与真正的金融推理困难混杂，导致评测无法明确判断错误来自取数与数据质量问题，还是来自金融概念理解及多步计算能力不足。
- 人工编写答案成本高，模型辅助或启发式抽取又可能继承生成与抽取错误，因此现有方案难以低成本扩展到覆盖广泛推理深度、同时保持标准答案可靠的数据规模。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种兼具答案可验证性、规模可扩展性和难度可控性的金融表格推理基准生成机制，尤其无法在控制其他因素时系统改变组合推理深度与金融概念复杂度，从而隔离并定位模型的具体能力边界。

</div>
<div markdown="1"><span>核心问题</span>

能否从表格数值和金融概念出发，以确定性的可执行计算结构自动生成自然语言金融问答，使答案在构造时即得到验证，并据此可重复地测量大语言模型随推理复杂度增加以及输入受到扰动时的性能变化？

</div>
<div markdown="1"><span>作者直觉</span>

如果先构造一棵每个节点都对应明确算术运算或金融公式的计算树，那么机器可以直接执行整棵树得到唯一答案，再把同一结构改写成自然语言问题。这样，题目表面仍要求模型完成取数和多步金融推理，但出题方始终掌握可执行的解题程序；改变树的深度、分支数量或所用金融概念，也就能像调节参数一样改变题目难度。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

V-FiLLM采用“先构造可执行计算、再生成语言问题”的确定性流程。输入是结构化金融表格，包括简化财务报表以及由真实$10$-Q申报文件整理的表格；系统先把单元格转换为带有数值、财务语义和类型信息的原子表示，再按指定深度、叶节点数量和运算符组合采样有类型的计算树。计算树可以直接执行，因此系统可在语言生成之前得到唯一的数值答案和完整计算轨迹；随后再把树渲染为自然语言问题，形成问题、表格、表达式、轨迹和答案相互对应的问答样本。其关键保证是“答案由程序执行得到”，而不是由人工或另一个语言模型标注。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 结构化金融数据准备

将财务数据组织为可定位的表格单元格，并保留数值及其行列、科目、单位等元数据。论文同时使用两类格式：较规整的简化报表支持更深的计算树，真实$10$-Q表格则保留更复杂的版面、脚注和混合单位环境。

<div class="method-step__io" markdown="1">

**输入**：简化财务报表，或从真实$10$-Q申报文件获得的结构化表格。<br>
**输出**：可供后续语义分解和数值引用的结构化金融表格。

</div>

**直观理解**：这一步相当于先准备一张机器能够准确查账的报表；后续每个问题所需的原始数字都必须能回指到其中的具体位置。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 带类型原子的构造

把可用单元格分解为带类型的语义原子，使系统能够区分金额、比率、利率以及具有特定财务含义的项目。原子不仅保存数值，还承担连接表格证据与后续运算节点的作用。

<div class="method-step__io" markdown="1">

**输入**：表格单元格的数值、位置和财务元数据。<br>
**输出**：可被计算树叶节点引用的带类型原子集合。

</div>

**直观理解**：普通数字只有大小，没有用途；加入类型和科目语义后，系统才知道某个数字是收入、成本还是百分比，从而避免随意拼接不相容的量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 可控计算树采样与落地

系统采样有类型的表达式树，以原子作为叶节点、算术或财务运算作为内部节点，并将每个叶节点落地到表格中的具体数值。树的深度控制连续推理步数，叶节点数量体现表达式广度，派生概念与运算符组合控制金融知识和计算结构的复杂度。

<div class="method-step__io" markdown="1">

**输入**：带类型原子集合，以及目标深度、叶节点数量、派生财务概念概率和运算符配置。<br>
**输出**：与具体表格证据绑定、可执行且难度可控的计算树。

</div>

**直观理解**：可以把它看成自动生成一份带步骤的计算题：系统先决定要经过多少步、使用多少个数字和哪些财务公式，再从报表中填入真实可查的数值。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 符号执行与语言渲染

系统对计算树进行符号化求值，得到确定的最终答案和可验证计算轨迹；然后把同一棵树渲染为自然语言问题，并保留其对应表达式。由于答案来自树的执行结果，语言模型不参与答案标注。

<div class="method-step__io" markdown="1">

**输入**：已落地的可执行计算树及其表格上下文。<br>
**输出**：包含表格上下文、自然语言问题、可执行表达式、推理轨迹和确定性答案的问答样本。

</div>

**直观理解**：流程先用计算器得到标准答案，再把计算过程改写成题目；即使题目措辞发生变化，答案仍由底层程序决定。不过论文也承认，语言渲染仍可能产生歧义或上下文不足，因此“数值答案正确”不等于“问题表述一定完美”。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：基准生成本身不涉及需要学习的目标函数：标准答案由可执行计算树直接求值，因此不存在人工标签拟合或生成模型标签优化。LoRA阶段使用通过最终答案验证的思维链样本对Qwen3.5-4B进行监督式参数高效微调，但所给原文没有明确写出损失函数或优化目标公式，故不能据此补写具体交叉熵表达式；可确定的是仅LoRA适配参数参与更新，基础模型主体参数保持冻结。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 有类型的可执行计算树**

该模块用叶节点表示表格中的带类型数值，用内部节点表示算术运算或派生财务概念，并通过树结构显式保存运算依赖。计算深度、表达式广度、财务概念复杂度和上下文规模可以分别调节，使评测能够针对不同失败来源进行分层。

> 直观理解：它既是题目的“施工图”，也是答案的“可执行程序”。相比只保存问题和答案，树能明确指出模型需要查哪些数字、按什么顺序计算，以及难度究竟来自步骤多、数字多还是金融概念复杂。

**2. 确定性验证与语言渲染**

验证器直接执行计算树以生成标准答案，语言渲染器再依据树及其财务语义产生问题和表达式，从而把答案生成与自然语言生成解耦。该设计消除了模型生成器参与标签环节所带来的答案错误率，但不能自动消除问题措辞的歧义。

> 直观理解：核心思想是让程序负责算对，让语言模块负责说清楚。这样可以低成本扩展题量，也能在发现某种措辞不佳时重新渲染问题，而不必重新人工计算答案。

**3. 已验证思维链与LoRA适配**

训练分为两阶段：第一阶段为训练题生成思维链，并以计算树的确定性答案过滤轨迹；原始$688$条候选中保留$608$条，即保留率为$88\%$。第二阶段仅训练LoRA低秩适配参数，论文报告其可训练参数约占模型参数的$0.50\%$，以较低计算成本使基础模型适应金融表格推理。

> 直观理解：LoRA不重训整个模型，而是在若干权重旁增加小型可训练更新；答案过滤则减少明显错误示范进入训练集的风险。需要注意，过滤条件只检查最终答案是否一致，因此相同答案可能由偶然抵消的错误步骤得到。

**训练与推理**

训练时，先从金融QA训练池中的$688$个问题出发，让Qwen3.5-4B为每个问题生成思维链；将每条轨迹的最终答案与对应表达式树计算出的真值比较，仅保留一致的$608$条轨迹。随后在这些轨迹上训练LoRA适配器，并在包含$90$题的留出基准上扫描秩$r$、缩放因子$\alpha$和dropout。论文最终用于跨数据集验证的配置为$r=8$、$\alpha=8$、dropout为$0.10$。

基准推理时，模型接收表格上下文和自然语言问题并输出最终答案，系统再按确定性真值判定正确性。单轮模式要求模型一次完成检索和全部计算；多轮模式将复杂问题按依赖关系拆为连续子查询，使前一轮结果成为后续推理的中间信息。加载LoRA时推理接口基本不变，只是在基础模型上叠加训练得到的低秩权重更新；论文还在FinQA上直接评估该适配器，以检查提升是否仅局限于V-FiLLM生成分布。

**复现信息**

复现基准生成时，最重要的是保存表格单元格、类型原子、计算树叶节点、自然语言提及和最终答案之间的可追溯映射，并固定计算树执行规则；否则无法保证“正确由构造保证”，也难以按深度或运算结构分组评测。难度控制至少应覆盖采样深度、叶节点数量、派生财务概念概率和运算符组合；Figure 1明确将这些因素列为可控项，论文结论部分另将上下文规模和语言变化概括为评测维度。

LoRA实验的必要解释性配置包括：基础模型为Qwen3.5-4B，候选秩为$r\in\{4,8,16\}$，缩放因子为$\alpha\in\{4,8,16,32\}$，dropout为$\{0.05,0.10,0.15\}$，留出集规模为$n=90$。原文前述实现段落提到$r=16$、$\alpha=32$、dropout为$0.05$，而结果部分将$r=8$、$\alpha=8$、dropout为$0.10$列为最佳且用于FinQA的配置；复现时应按具体实验表区分固定示例配置与超参数扫描后的选定配置。原文未明确报告优化器、学习率、批大小、训练轮数、随机种子、解码参数和逐步轨迹验证器，因此这些内容不能从当前材料中确定。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- V-FiLLM：由合成但内部一致的金融表格自动生成。数据源包括仿 10-Q 申报表和格式规则化的金融工作表；后者覆盖 15 家合成公司、2020 至 2025 年，公司数量可调，提示中使用 6 家公司。每道题绑定可执行的计算树，因此答案、计算轨迹、实际深度、运算符和所用单元格均可自动验证。原文节选未明确报告总题量及训练、验证、测试划分规模。
- V-FiLLM 留出问题集：用于检验在已验证思维链轨迹上进行 LoRA 微调后的域内泛化。摘要报告微调前后准确率，但原文节选未明确报告留出策略、样本量以及是否按公司、年份或表达式模板隔离。
- FinQA：外部金融问答基准，用于检验 V-FiLLM 上的轻量适配能否迁移到现有真实金融问答任务。原文节选仅在摘要中报告相对基础模型的提升，未明确说明采用的 FinQA 划分、评测子集和预处理方式。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（Accuracy）**

正确回答的问题数占全部评测问题数的比例，用于衡量模型最终数值答案与计算树确定的标准答案是否一致。原文节选未说明数值容差、单位归一化、答案抽取规则或精确匹配细节。 （越高越好，因为更高准确率表示模型在更多问题上得到与可执行表达式一致的答案。）

</div>
<div class="metric-item" markdown="1">

**准确率下降值**

比较推理深度增加或施加对抗性数值扰动前后的准确率变化，用于衡量模型对组合复杂度和输入数值变化的敏感程度。 （绝对下降越小越好，因为下降较小表示模型在难度提高或数值被扰动后仍能保持稳定表现。）

</div>
<div class="metric-item" markdown="1">

**准确率提升百分点**

LoRA 微调模型相对基础模型的准确率之差，用于量化轻量领域适配带来的绝对收益；百分点变化不同于相对百分比增长。 （提升百分点越大越好，但只有在评测协议、数据划分和答案判定规则一致时才可直接归因于微调方案。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 随 V-FiLLM 计算树深度增加的受控评测

<div class="result-value" markdown="1">

作者报告，开源模型的准确率随着推理深度增加最多下降 51%。

</div>

这说明模型即使面对答案可执行验证、数据内部一致的题目，也会在需要组合更多中间计算时明显退化，支持“多步组合推理仍是瓶颈”的作者结论。由于摘要只给出最大降幅，没有给出起止深度、对应模型、绝对准确率或误差范围，该结果不能证明所有模型都会下降 51%，也不能排除更长问题文本、更多叶节点或特定运算符同时造成影响。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

By evaluating on open-source models, we find that accuracy falls up to 51% as reasoning depth increases, and up to 47% points under adversarial numerical perturbations, highlighting remaining challenges in robust financial reasoning over tables.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 对抗性数值扰动下的稳健性评测

<div class="result-value" markdown="1">

作者报告，对抗性数值扰动可使准确率最多下降 47 个百分点。

</div>

该结果表明模型可能依赖训练中常见的数值模式、量级或表面线索，而未始终执行稳定的符号计算。这里报告的是最严重设置下的绝对百分点下降，不等于平均下降 47%，也不能仅凭该数字判断错误来自取数、运算过程还是答案格式；所给节选还未说明扰动是否保持财务一致性。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

By evaluating on open-source models, we find that accuracy falls up to 51% as reasoning depth increases, and up to 47% points under adversarial numerical perturbations, highlighting remaining challenges in robust financial reasoning over tables.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 使用已验证思维链轨迹进行 LoRA 微调，并在 V-FiLLM 留出题和 FinQA 上评测

<div class="result-value" markdown="1">

V-FiLLM 留出题准确率由 81.1% 提升至 85.6%，绝对提高 4.5 个百分点；在 FinQA 上相对基础模型提高 5 个百分点。

</div>

域内留出题的提升说明自动生成且可验证的推理轨迹可以成为有效的轻量训练信号；FinQA 上的提升进一步提供了跨基准迁移证据。它仍不能证明收益完全来自“答案可验证”这一性质，因为节选没有提供使用未验证轨迹、仅答案监督、全参数微调或等量真实数据训练的对照，也未报告统计显著性。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We further show that lightweight LoRA fine-tuning on verified chain-of-thought traces improves accuracy from 81.1% to 85.6% on held-out problems and outperforms the base model by 5% points on FinQA (Chen et al., 2022a), s), suggesting that targeted, low-cost adaptation is a promising direction for compositional reasoning in financial QA.

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

- 未具名的开源大语言模型：用于测量 V-FiLLM 各难度轴上的基础推理能力。它们是有意义的比较对象，因为论文关注可公开使用模型在受控金融表格推理中的能力边界；但所给节选未列出模型名称、参数规模或具体分数。
- LoRA 微调前的基础模型：与采用同一模型架构、仅增加低秩适配参数的版本比较，用来判断收益是否来自针对已验证推理轨迹的轻量训练，而非更换更强模型。原文节选未明确报告基础模型名称。
- 经已验证思维链轨迹进行 LoRA 微调的模型：作为论文提出的低成本适配方案，在 V-FiLLM 留出题和 FinQA 上与基础模型比较。该设置可测试训练信号的实用性，但不能单独区分 LoRA、思维链格式和训练数据质量各自的贡献。

**实验想回答的问题**

- 当计算树深度、表达式广度、金融概念复杂度和上下文规模受到独立控制时，开源大语言模型的表格金融推理准确率如何变化，尤其能否稳定完成多步组合计算？
- 模型对数值扰动是否稳健，以及使用自动验证的思维链轨迹进行轻量 LoRA 微调，能否提高域内留出题和外部金融问答数据集上的准确率？

**实验实现**

评测题由类型化二叉计算树生成：叶节点是带有金融概念、公司、财年、单位和数量类型元数据的表格单元格，内部节点执行加、减、乘、比率、增长率、最小值、最大值或平均值等运算。系统直接执行表达式得到标准答案，再把同一表达式自底向上渲染为自然语言问题。实验可通过采样深度、叶节点数量或树宽度、派生金融概念采样概率、运算符组合和上下文规模控制难度，并可加入拼写、大小写和措辞变化测试语言表面稳健性。训练实验使用自动验证的思维链轨迹进行 LoRA 轻量微调。所给节选未明确报告模型清单、提示词、解码参数、随机种子、重复实验次数、置信区间、硬件配置、LoRA 超参数及答案匹配协议，因此数值结果仍需结合论文完整实验章节核验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 图 2 给出深度 0、1、2 的生成实例：深度 0 直接查询收入；深度 1 对流动负债和所得税率做一次乘法；深度 2 分别计算总资产与销货成本按税率缩放后的值，再求二者差。该案例直观说明计算树深度如何对应所需中间步骤，但它是任务构造示例，不是模型成功或失败的定性案例，不能据此判断错误类型。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：构建可执行计算树生成的金融表格推理基准，重点评测 LLM 的组合式数值推理能力。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`ea00926a93517daa63d10b7617568ab28043311f1f824d2fbe84175d79f7bfb0`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
