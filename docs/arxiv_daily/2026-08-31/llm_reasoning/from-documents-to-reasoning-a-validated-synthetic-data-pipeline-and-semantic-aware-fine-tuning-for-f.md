---
title: "[论文解读] From Documents to Reasoning: A Validated Synthetic Data Pipeline and Semantic-Aware Fine-Tuning for Financial Numerical Reasoning"
description: "[arXiv 2608.27919][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.27919"
announcement_date: "2026-08-31"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:39:21.332350+00:00"
source_sha256: "bbf0e1f0d5789be402e42bd0a61d657082db19cb5702522fb883d9e6b37bb325"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "LLM 其他"
  - "金融问答"
  - "数值推理"
  - "表格文本联合理解"
  - "合成数据"
  - "小型语言模型"
  - "QLoRA"
  - "算术表达式"
  - "Expression Match Accuracy"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.27919</p>

# From Documents to Reasoning: A Validated Synthetic Data Pipeline and Semantic-Aware Fine-Tuning for Financial Numerical Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Lokendra Birla, Milind Savagaonkar, Visnu Srinivasan, Sowmya Rasipuram, Shubhashis Sengupta</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27919v1) · [PDF 下载](https://arxiv.org/pdf/2608.27919v1) · **关键词** 金融问答, 数值推理, 表格文本联合理解, 合成数据, 小型语言模型, QLoRA, 算术表达式, Expression Match Accuracy<br>


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

本文研究金融文档问答（financial question answering, QA），即让模型从包含表格、图表和叙述性文本的财务报告中定位相关信息，并完成多步数值推理后回答问题。与普通文本问答相比，该任务要求模型同时理解文本与表格之间的关系、生成或执行算术运算，并正确处理货币符号、百分比、单位和数值格式；论文关注的实际目标是利用经过验证的合成数据和参数高效微调，使较小语言模型（SLM）在有限部署成本下具备稳定的金融数值推理能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**金融数值问答**

输入通常是金融报告中的文本、表格或图表以及一个问题，输出是数值答案及其推理过程。问题往往需要从多个位置提取数字，再进行加减、乘除或百分比计算。

</div>
<div class="concept-item" markdown="1">

**程序式推理与算术表达式**

模型不直接猜最终数字，而是生成一个由数字和数学运算组成的表达式，例如先计算差值再计算增长率；外部程序随后执行该表达式得到答案。这样可以把语言生成与精确计算分开，降低模型进行直接算术时的错误。

</div>
<div class="concept-item" markdown="1">

**精确匹配与表达式匹配**

精确匹配（EM）只有在模型答案与标准答案逐字符一致时才计为正确，因此容易把数值相同但单位、逗号、货币符号或百分号不同的答案判为错误。本文提出的表达式匹配准确率（EMA）比较预测表达式和标准表达式计算出的数值，旨在识别数学上等价的答案。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入包括来自金融 PDF 的混合模态内容：表格、周围的前置和后置文本，以及由此形成的问题；目标输出是能够支持答案计算的算术表达式和最终数值答案。论文进一步构造合成的问答训练样本，并将其用于微调 SLM，使模型学习金融领域中的信息定位和多步数值推理。基本假设是，经过多阶段生成与验证的表达式能够比直接生成数值答案更可靠；在评估时，预测表达式和参考表达式均可被执行并转换为数值进行比较。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

金融问题及其相关文档上下文的输入表示，包含文本、表格或图表中的可用信息。

</div>
<div class="notation-item" markdown="1">

**$e_{\text{pred}}$**

模型预测的算术表达式；执行该表达式可得到模型预测的数值答案。

</div>
<div class="notation-item" markdown="1">

**$e_{\text{ref}}$**

数据集中人工标注或验证得到的参考算术表达式，用作训练目标或评估基准。

</div>
<div class="notation-item" markdown="1">

**$\operatorname{Eval}(e)$**

执行算术表达式 $e$ 并返回其数值结果的操作；EMA 的核心是比较 $\operatorname{Eval}(e_{\text{pred}})$ 与 $\operatorname{Eval}(e_{\text{ref}})$。

</div>

</div>

**直接相关的工作**

- **FinQA、ConvFinQA 与 TAT-QA**: 这些基准将金融报告中的表格和文本结合起来，测试模型的多步数值推理，是本文任务设定和实验评估的直接背景。原文指出，现有方法通常使用 EM 或执行准确率，但严格的字符级匹配无法充分处理单位、格式及数学等价表达式。
- **FinLLMs 与 Phogat 等人的 teacher-student 方法**: 这些工作使用金融公式、图遍历或大型教师模型生成合成推理样本，再用于适配较小语言模型，说明合成数据和 SLM 微调能够缓解人工标注成本及部署成本。本文在此基础上进一步强调从金融文档生成并严格验证算术表达式，并将 EMA 与语义相似度纳入微调损失。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

金融问答需要同时理解财务文档中的表格、图表和上下文，并完成多步数值计算；但高性能大语言模型参数规模庞大、部署成本高，小型语言模型又缺少足够且可靠的领域训练数据。人工构造这类问答样本需要标注者阅读多份报告并执行复杂计算，成本较高，因此实际需求是以较低成本获得可验证的金融数值推理数据，并可靠评估模型是否真正完成了计算。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于少样本提示的金融数值问答**：将若干示例问题、推理过程和答案放入提示中，引导大语言模型直接回答新问题。该方法无需额外训练，但其效果依赖示例的选择和排列。
- **大模型生成数据并微调小模型**：先利用大语言模型从文档生成带推理示范的问答样本，再用这些样本对小型语言模型进行领域微调，以降低部署成本。对于金融数值问答，该流程还需要处理表格与文本的对应关系，并验证生成的计算过程和答案是否正确。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 常用的精确匹配指标（Exact Match，EM）按字符逐一比较模型答案与标准答案，只给出匹配或不匹配的二元结果；因此，货币符号、逗号、百分比或单位差异可能使数学上等价的答案被判错，导致对模型数值推理能力的低估或误判。
- 现有合成数据方法较少针对包含数值表格和文本关系的金融问答进行严格验证；同时，直接让大语言模型生成最终数值答案容易出现计算错误，低质量样本会进一步削弱小型语言模型的微调效果。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一个面向金融数值问答的端到端方案：它既能从包含表格和文本的财务文档中自动生成经过多阶段验证的问答数据，又能以对数学等价形式更稳健的方式评估答案，并将这种数值正确性与表达式语义信息用于小型语言模型的训练。

</div>
<div markdown="1"><span>核心问题</span>

如何从财务文档中自动构造高质量、可验证的算术推理问答样本，并设计一种能够识别数学等价答案的评估与训练机制，从而在降低部署成本的同时提升小型语言模型的金融数值问答能力？

</div>
<div markdown="1"><span>作者直觉</span>

作者不要求大语言模型直接计算并输出最终数字，而是让它生成算术表达式，再通过表达式求值和多阶段校验确认结果。这样可以把“生成推理步骤”和“验证数值结果”分开，减少直接心算式生成带来的错误。进一步地，Expression Match Accuracy（EMA）比较预测表达式与标准表达式计算出的数值，而不是只比较表面字符串；配合交叉熵和表达式语义相似度损失，模型既能学习正确的计算结果，也能学习合理的推理结构。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把“从财务文档构造可靠训练数据”和“让小语言模型学习生成可执行算术程序”连接成一条端到端流程。输入是包含表格、正文及可能复杂版式的财务 PDF；系统分别从页面图像和 PDF 原生文本中抽取表格，利用双来源匹配筛除不一致内容，再围绕经验证的表格及其前后文生成问题、算术程序和答案。生成样本还要经过问题质量评估、迭代改写与独立答案核验，之后与 FinQA、CFinQA 等真实数据合并，用 QLoRA 微调 Mistral-v0.3-7B、Llama3.1-8B 或 Phi-4-14B，使模型根据财务上下文和问题输出结构化算术表达式。
推理与评价不要求模型直接完成容易出错的心算，而是让它生成由加、减、乘、除及表格聚合等函数构成的程序，再由 DSPy ReAct Agent 和 Python Interpreter 执行。作者提出的表达式匹配准确率 EMA 分别执行参考程序与预测程序，并比较二者的最终数值；训练侧进一步提出 SA-EMA，将逐词交叉熵、表达式字符串相似度和 EMA 结果组合起来，希望同时约束语法、整体形式和执行结果。直观地说，系统先用“两种方式抄表并相互校对”建立可信题目，再训练模型“写计算步骤而非口算答案”，最后交给计算器执行并核验。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 财务文档双通道解析

使用 PyMuPDF 将每页以 300 DPI 渲染为图像，随后把图像编码为 base64 并交给 Claude Sonnet 3.5 检测表格、保持行列及表头结构并输出 Markdown；同时使用 PDFPlumber 从原始 PDF 抽取文本、表格及每张表之前和之后的上下文。

<div class="method-step__io" markdown="1">

**输入**：包含表格、图形和叙述文本的财务 PDF 文档。<br>
**输出**：两套独立的表格表示：视觉语言模型抽取的 Markdown 表格，以及带有前文、后文和位置信息的 PDF 原生表格。

</div>

**直观理解**：同一张表分别通过“看页面”和“读 PDF 内部文字”抄录。两份结果为后续交叉检查提供依据，并保留解释数字含义的邻近文字。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 跨来源表格验证与语境对齐

系统逐行计算两类互补的匹配信号：依据数值接近程度、范围重叠和模式类型得到的语义相似度，以及由 all-MiniLM-L6-v2 嵌入计算的句级余弦相似度；仅保留整体对齐程度超过预设阈值的表格对，并挂接对应前后文。

<div class="method-step__io" markdown="1">

**输入**：视觉通道抽取的表格，以及 PDFPlumber 抽取的表格和周边文本。<br>
**输出**：通过双来源一致性检查、且具有叙述语境的结构化财务表格实例。

</div>

**直观理解**：如果两名抄录者对表格内容基本一致，系统才把该表当作可信材料。这样可在出题前排除错列、漏行或数字识别错误较多的表格。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 问题生成、评分与迭代改写

提示 LLM 生成直接检索、单步运算、多行或多列中间计算以及复合推理问题；评估器先检查问题是否自然且属于金融领域，再分别以 1 至 5 分评价相关性、连贯性和事实覆盖度，未通过的问题依据上下文覆盖、逻辑连贯和可回答性进行迭代改写。

<div class="method-step__io" markdown="1">

**输入**：经验证的表格、表格前文和表格后文。<br>
**输出**：与给定财务材料相关、可由上下文回答且覆盖不同推理复杂度的问题集合。

</div>

**直观理解**：系统不是生成问题后立即采用，而是先像审题教师一样检查题目是否通顺、有依据且确实能解。质量较差的题目会被重写，而不是直接混入训练集。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 算术程序生成与答案验证

LLM 从表格及文本中选取数值，并生成由 add、subtract、multiply、divide、exp、greater、table_max、table_min、table_sum 和 table_average 等函数组成的顺序程序；中间结果用 $\#n$ 引用，程序由 DSPy ReAct Agent 配合 Python Interpreter 执行，另一轮“财务分析师”提示再独立检查问题含义、相关数据、推导方法、预期答案和最终正确性。

<div class="method-step__io" markdown="1">

**输入**：财务上下文和通过质量控制的问题。<br>
**输出**：包含上下文、问题、结构化算术表达式、执行所得答案及验证结论的合成监督样本。

</div>

**直观理解**：模型只负责写出可检查的计算清单，精确计算交给外部解释器。随后另一个检查环节从原材料重新解题，以避免“程序能运行但解决了错误问题”。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 表达式匹配准确率 EMA

$$
\operatorname{EMA}(E^{GT},E^{P})=\begin{cases}1,&\left|F(E^{GT})-F(E^{P})\right|=0\\0,&\text{otherwise}\end{cases},\qquad F(E)=C(e_n)
$$

**符号说明**

- $E^{GT}$：参考或真实算术表达式序列，由多个顺序执行的操作步骤组成。
- $E^{P}$：模型预测的算术表达式序列。
- $e_n$：表达式序列中的最后一个计算步骤；步骤参数可为数值常量或先前中间结果。
- $C(e_n)$：执行最后一步算术操作后得到的数值。
- $F(E)$：完整执行表达式序列 $E$ 后得到的最终数值，定义为最后一步的执行结果。
- $\operatorname{EMA}(E^{GT},E^{P})$：表达式匹配准确率指示值；两个程序执行结果严格相等时为 1，否则为 0。

<div class="equation-explanation" markdown="1">

**直观理解**：该指标先把标准程序和预测程序都当作可执行计算过程，再比较最终数值，而不是比较表面文本。它能够认可计算顺序或数字书写形式不同但结果相同的程序；不过公式要求差值恰好为零，没有定义近似容差、单位归一化或执行失败时的处理方式。<br>
**原文位置**：第 3.1 节，公式（3）；最终值定义紧邻公式（3）之前

</div>

</div>

<div class="equation-block" markdown="1">

#### Semantic-Aware EMA 总损失

$$
\mathcal{L}_{\mathrm{total}}=\alpha\mathcal{L}_{\mathrm{CE}}+\beta\mathcal{L}_{\mathrm{sem}}+\gamma\mathcal{L}_{\mathrm{ema}},\quad \mathcal{L}_{\mathrm{CE}}=-\sum_{t=1}^{T}\log p_{\theta}(y_t\mid x,y_{<t}),\quad \mathcal{L}_{\mathrm{sem}}=1-\operatorname{Sim}(\hat{y},y),\quad \mathcal{L}_{\mathrm{ema}}=1-\operatorname{EMA}(\hat{y},y)
$$

**符号说明**

- $\mathcal{L}_{\mathrm{total}}$：用于领域适配的总训练目标。
- $\mathcal{L}_{\mathrm{CE}}$：逐 token 交叉熵，惩罚预测序列与参考序列在局部位置上的差异。
- $\mathcal{L}_{\mathrm{sem}}$：表达式字符串语义不相似损失，由归一化相似度的补数构成。
- $\mathcal{L}_{\mathrm{ema}}$：EMA 损失；预测程序和参考程序执行结果相同时为 0，否则为 1。
- $\alpha,\beta,\gamma$：分别平衡交叉熵、字符串相似度损失和 EMA 损失的标量超参数；原文未明确报告取值。
- $x$：模型输入，包括财务上下文和问题。
- $y_t$：参考算术表达式在第 $t$ 个位置的目标 token。
- $y_{<t}$：第 $t$ 个位置之前的参考 token 前缀。
- $T$：参考输出序列的 token 长度。
- $p_{\theta}$：参数为 $\theta$ 的模型给出的条件 token 概率。
- $\hat{y}$：模型生成的预测算术表达式。
- $y$：参考算术表达式。
- $\operatorname{Sim}(\hat{y},y)$：预测表达式与参考表达式之间的归一化字符串相似度，文中示例实现为 SequenceMatcher。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项确保生成序列在语法和 token 层面接近标准答案，第二项比较完整字符串，第三项检查程序执行后是否得到相同结果。设计意图是避免仅凭逐词损失惩罚诸如交换律导致的等价写法，但 SequenceMatcher 本身并不理解交换律或结合律，且后两项不可微或离散，论文没有说明如何把它们转化为稳定的参数梯度。<br>
**原文位置**：第 3.3.2 节，公式（4）—（7）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标是让模型在给定财务上下文 $x$ 和问题后生成参考算术程序 $y$。标准交叉熵 $\mathcal{L}_{\mathrm{CE}}$ 可直接通过教师强制和反向传播优化 QLoRA 的低秩适配参数；作者进一步以权重 $\beta$ 和 $\gamma$ 加入完整表达式相似度及执行结果一致性，希望模型不只模仿局部 token，还能保持全局程序形式与数值语义。按照作者的表述，预测程序与参考程序越相似且执行结果越一致，总损失应越低。
需要谨慎解释其优化可实现性：SequenceMatcher 必须取得离散预测字符串后计算，EMA 又依赖程序执行和二值比较，二者通常无法对模型参数 $\theta$ 求常规梯度；第 3.4 节也承认语义相似度是 post-hoc 且不可微。原文节选没有说明是否采用强化学习、最小风险训练、可微代理、样本重加权、直通估计或仅把这些量用于选择模型，因此可确认的直接梯度来源只有 $\mathcal{L}_{\mathrm{CE}}$。此外，$\alpha$、$\beta$、$\gamma$ 的具体值及无效程序的损失处理均为原文未明确报告，复现时必须核查代码或完整论文。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双来源表格验证模块**

该模块将 Claude Sonnet 3.5 从页面图像提取的表格，与 PDFPlumber 从 PDF 内容层提取的表格进行成对、逐行比较。匹配同时考虑数值接近性、数值范围重叠、表示模式和 all-MiniLM-L6-v2 嵌入余弦相似度；达到阈值的表格才与其前后叙述文本组合为出题上下文，但原文未给出具体阈值。

> 直观理解：图像解析能够处理复杂视觉布局，却可能看错字符；PDF 原生解析通常更精确，却可能破坏复杂行列关系。将二者相互校验，可以利用各自优势并降低由错误表格继续生成错误题目的风险。

**2. 可执行算术程序与 EMA 模块**

参考表达式 $E^{GT}$ 和预测表达式 $E^{P}$ 都是顺序操作集合，每一步可以读取常数或以 $\#k$ 引用先前结果，最终值由最后一步给出。EMA 不比较答案字符串或程序字符串，而是分别执行两个程序，并在最终数值严格相等时记为 1，否则记为 0。

> 直观理解：例如“1000000”和“$1\times10^6$”文本不同但数值相同，直接文本匹配可能误判；执行程序后比较结果可以避免这类格式差异。不过当前定义仍采用零容差严格数值相等，因此浮点误差、单位换算和两个程序同时得到错误结果等情况仍需额外防护。

**3. 语义感知 SA-EMA 监督模块**

SA-EMA 线性组合 token 级交叉熵、基于 SequenceMatcher 的表达式字符串不相似度，以及由执行结果产生的 EMA 损失。三项分别试图约束局部序列预测、表达式整体字符串接近程度和最终执行结果，但作者在第 3.4 节明确指出语义相似度是事后计算且不可微；二值 EMA 和离散解码同样不能直接提供常规反向传播梯度，因此其具体可微优化实现未被充分说明。

> 直观理解：交叉熵要求模型逐字写得像标准程序，字符串相似度关注整段程序是否相近，EMA 则只看算出的结果是否一致。这一组合目标方向合理，但若后两项只在生成完整文本后才能计算，它们更像评分或样本级惩罚；没有代理梯度、强化学习或重加权机制时，不能像交叉熵那样直接指导每个参数更新。

**训练与推理**

训练阶段先运行文档解析与双来源表格验证，只用达到相似度阈值的表格及其前后文生成问题。问题通过领域合法性、相关性、连贯性、事实覆盖度和可回答性检查后，LLM 生成顺序算术程序，外部 Python 工具执行程序，独立验证器再根据原始上下文重建解法并判断程序与答案是否正确；通过验证的合成样本可与 FinQA、CFinQA 真实数据混合。随后量化基础模型，并使用 QLoRA 训练低秩适配参数，使其从上下文与问题预测算术表达式；论文将这一过程描述为使用 SA-EMA 目标，但不可微分量如何参与参数更新原文未明确报告。
推理阶段向微调模型提供财务表格、相关叙述和问题，模型不直接输出未经验证的心算结果，而是输出预定义函数构成的线性程序。程序中的 $\#k$ 指向第 $k$ 个中间结果，DSPy ReAct Agent 调用 Python Interpreter 顺序执行各步并返回最终答案。评价时，参考程序和预测程序由同一执行逻辑计算，EMA 根据最终数值是否严格相等给出 0 或 1；若还需要展示答案文本，可将执行值格式化输出，但原文没有给出单位恢复、浮点容差、异常执行或无效语法的完整规则。

**复现信息**

与方法解释和复现直接相关的配置包括：PDF 页面由 PyMuPDF 以 300 DPI 渲染；视觉表格抽取使用 Claude Sonnet 3.5，并要求输出保持表头、行列和对齐关系的 Markdown；原生文本及表格由 PDFPlumber 抽取；跨表匹配使用数值与模式相似性以及 all-MiniLM-L6-v2 嵌入余弦相似度。程序执行依赖 DSPy ReAct Agent 和支持 Python Interpreter 的工具调用环境，允许的操作至少包括 add、subtract、multiply、divide、exp、greater、table_max、table_min、table_sum 和 table_average，中间结果采用 $\#n$ 表示。
模型侧采用 QLoRA 微调 Mistral-v0.3-7B、Llama3.1-8B 和 Phi-4-14B。公平解释结果仍需要但节选未提供的信息包括：表格对齐阈值、问题质量分数的最终保留规则、迭代改写次数、合成数据规模及真实与合成样本比例、量化位宽、LoRA 秩与目标层、优化器和学习率、训练轮数、解码策略、损失权重 $\alpha$、$\beta$、$\gamma$，以及不可微 SA-EMA 分量的实际训练实现；这些项目均不应从现有节选中自行推断。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- FinQA：面向金融文档的表格加文本数值推理基准，要求模型从异构信息中提取相关数值并执行多步算术计算。摘录未给出其训练集、开发集或测试集规模；其作用是评估表格—文本联合推理能力。
- ConvFinQA：FinQA 的对话式扩展，问题和答案按顺序相互依赖，模型需要结合累计对话历史、金融文本和表格回答最终问题。实验使用其 3965 个训练样本和 542 个开发样本；由于测试集没有真实标签，作者在开发集上评估。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Exact Match（EM）**

检查模型输出是否与标准答案在字符串或严格格式上完全一致。它反映严格答案匹配能力，但可能把单位、格式或表达形式的轻微差异误判为错误。 （越高越好，因为更高表示完全匹配的答案比例更大；但它对数值等价而表面形式不同的答案不够鲁棒。）

</div>
<div class="metric-item" markdown="1">

**Expression Match Accuracy（EMA）**

将模型答案对应的算术表达式所计算出的结果与参考答案进行匹配，而不是只比较答案字符串。该指标旨在判断模型是否得到相同的计算结果，从而减少单位或格式差异造成的误判。 （越高越好，因为更高表示更多预测在计算意义上与参考结果一致；不过摘录没有完整给出表达式解析、单位归一化或异常输出的具体规则。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 在 ConvFinQA 开发集上比较 EM 与 EMA，并以 Sonnet 3.5 为代表。

<div class="result-value" markdown="1">

Sonnet 3.5 的 EM 为 61.25，EMA 为 68.63，EMA 高于 EM 7.38 个百分点。

</div>

这表明严格字符串匹配可能低估模型得到正确数值结果的比例。它支持 EMA 对格式差异更宽容，但不能单独证明 EMA 一定比 EM 更符合人工判断，因为摘录没有提供人工复核或误差分类。

<div class="result-source" markdown="1">

来源：Table 2, Section 4.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Sonnet3.5 | 61.25 | 68.63

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 在 ConvFinQA 开发集上比较不同规模的 Llama 3.1 基线。

<div class="result-value" markdown="1">

Llama 3.1-8B 的 EM/EMA 为 32.84/44.09，Llama 3.1-70B 为 53.50/57.01，Llama 3.1-405B 为 57.19/62.17；随着参数规模增加，EM 和 EMA 整体提高。

</div>

结果说明模型规模与该金融多步推理任务的表现存在正相关，且 EMA 对 8B 模型给出的宽松评价提升尤其明显。由于不同规模模型的训练数据、提示设置和推理配置可能不同，结果不能被解释为规模 alone 已经确定因果地优于所有其他设计。

<div class="result-source" markdown="1">

来源：Table 2, Section 4.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Llama3.1-8B (Dubey et al., 2024) | 32.84 | 44.09
Llama3.1-70B (Dubey et al., 2024) | 53.50 | 57.01
Llama3.1-405B (Dubey et al., 2024) | 57.19 | 62.17

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 比较不同 Mistral 基线在 ConvFinQA 开发集上的 EM 与 EMA。

<div class="result-value" markdown="1">

Mistral 7B v0.2 的 EM/EMA 为 11.80/15.68，Mistral 7B v0.3 为 31.26/48.71，Mistral Large 2407 为 56.27/61.07，Mixtral 8×7B 为 30.26/35.05。

</div>

同为 7B 级别的 v0.3 明显高于 v0.2，说明基础模型版本或训练差异可能对金融推理影响很大；Mistral Large 2407 的结果最高，符合更大模型通常更强的趋势。该表没有展示作者合成数据与自定义损失微调模型的具体数值，因此不能仅凭这些基线行确认所提出完整管线的增益大小。

<div class="result-source" markdown="1">

来源：Table 2, Section 4.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Mistral7B v0.2 (Jiang et al., 2024) | 11.80 | 15.68
Mistral 7B v0.3 (Jiang et al., 2024) | 31.26 | 48.71
Mistral Large 2407 | 56.27 | 61.07
Mixtral8*7B | 30.26 | 35.05

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

- Sonnet 3.5 和 Haiku：通用大语言模型基线，用于衡量金融专门微调模型与商业模型之间的性能差距。
- Llama 3.1 系列（8B、70B、405B）：覆盖不同参数规模的开源模型，用于检验模型规模对 ConvFinQA 数值推理的影响。
- Llama 3.2 系列（11B、90B）：另一组开源模型基线，用于与相近及更大规模模型比较。
- Mistral 系列（7B v0.2、7B v0.3、Large 2407、Mixtral 8×7B）：包含较小模型、混合专家模型和大型模型，适合比较基础模型架构及规模差异；作者还将结果与 Srivastava 等人（2024）报告的模型进行比较。

**实验想回答的问题**

- 在金融数值问答中，Expression Match Accuracy（EMA）是否比 Exact Match（EM）更能反映模型答案与正确计算结果之间的一致性？
- 使用合成数据和自定义损失函数微调后的较小语言模型，能否在 ConvFinQA 上达到接近大型语言模型的表现，并优于既有较小模型？

**实验实现**

实验在两张 80GB NVIDIA A100-SXM4 GPU 上进行。基础模型使用 Unsloth 的 4-bit NF4 量化，并采用 QLoRA 微调；LoRA 秩搜索范围为 8、16、32、64、128 和 256，alpha 为 16 至 128，dropout 为 0.0、0.05 和 0.1，适配模块覆盖注意力层、前馈网络投影层及语言模型头。训练使用学习率 $2\times10^{-4}$、线性学习率调度、有效批大小 8（每设备批大小 2、梯度累积 4 步）、8-bit AdamW、权重衰减 0.01 和 5 个 warmup steps。ConvFinQA 的测试集没有真实标签，因此主要结果来自开发集；摘录未明确说明每个模型的解码设置、随机种子、重复实验次数或统计显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出经验证的合成数据、语义感知微调损失和表达式级指标，以改进并评估金融数值推理。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`bbf0e1f0d5789be402e42bd0a61d657082db19cb5702522fb883d9e6b37bb325`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
