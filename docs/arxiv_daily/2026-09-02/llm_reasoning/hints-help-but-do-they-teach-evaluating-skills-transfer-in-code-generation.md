---
title: "[论文解读] Hints Help But Do They Teach? Evaluating Skills Transfer in Code Generation"
description: "[arXiv 2609.01106][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2609.01106"
announcement_date: "2026-09-02"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:57:54.567594+00:00"
source_sha256: "98ae40cc0c0c82f21c613bd346f722ad3ae53df9321a08f5c28624b32a6c8a70"
tags:
  - "LLM Reasoning"
  - "代码生成"
  - "程序功能正确性"
  - "提示救援"
  - "激活干预"
  - "能力迁移"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.01106</p>

# Hints Help But Do They Teach? Evaluating Skills Transfer in Code Generation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Will Badr</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.01106v1) · [PDF 下载](https://arxiv.org/pdf/2609.01106v1) · **关键词** 代码生成, 程序功能正确性, 提示救援, 激活干预, 能力迁移<br>


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

本文属于代码生成与程序正确性评估研究，关注大语言模型根据自然语言任务描述生成可执行的 Python 程序。研究重点不是单纯比较生成代码的通过率，而是分析提示中的短提示（hint）使失败程序变为通过程序时，究竟是提供了模型原本缺失的信息，还是仅仅把模型引导到它通过普通重复采样本来就能生成的解。由于代码可以通过测试执行直接判定功能正确性，本文使用 HumanEval+ 和 MBPP+ 作为可验证的代码生成环境，并进一步考察隐藏状态干预、虚拟 KV 前缀和正确性探针是否能够表示或迁移任务能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**通过率与可执行评估**

代码生成模型输出程序后，将程序放入题目提供的测试用例中执行；全部相关测试通过，才把该样本视为功能正确。这样得到的通过或失败标签来自程序行为，而不是语言模型对代码的主观评分。

</div>
<div class="concept-item" markdown="1">

**提示救援与普通采样**

若初始生成的程序失败，加入与任务相关的 hint 后生成通过程序，这称为提示救援。要判断 hint 是否提供了真正的新信息，需要与无提示条件下多次生成候选程序进行比较；如果无提示采样也能找到同一类正确解，提示的作用更可能是改变搜索路径而非传授新能力。

</div>
<div class="concept-item" markdown="1">

**激活干预与虚拟 KV 前缀**

激活干预直接修改模型中间层的隐藏向量，试图把文字提示产生的行为压缩成可复用的内部方向或低秩子空间。虚拟 KV 前缀则是在注意力机制中加入一小段可学习的键和值向量，使模型在不接收完整文字说明时近似利用被压缩的信息。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定代码任务的自然语言规格和模型条件，模型生成 Python 程序，并由执行测试得到正确或错误标签。本文首先选择模型原本失败的任务，比较四类条件：无提示生成、加入任务相关的短 hint、加入长度匹配但与任务无关的 hint，以及重复采样得到的多个无提示候选。核心问题是，相关 hint 所带来的通过结果是否超出模型在相同任务上通过普通采样已经可达到的解空间。随后，在 Qwen2.5-3B-Instruct 上，将文字提示产生的行为进一步表示为隐藏状态方向、低秩激活干预或短虚拟 KV 前缀，并用留出任务、随机匹配和打乱干预检验任务特异性与跨任务迁移。研究还训练隐藏状态探针预测代码正确性，但将其解释为可解码的正确性信号，而不是模型已经获得可靠自我认知的证明。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

代码任务及其上下文输入，通常包含自然语言规格、已有代码或提示信息。

</div>
<div class="notation-item" markdown="1">

**$y$**

模型根据输入生成的候选程序；通过执行评估后可被标记为正确或错误。

</div>
<div class="notation-item" markdown="1">

**$h$**

加入输入的短文本提示；相关提示针对当前程序或任务提供可能有用的方向，无关提示与当前任务语义不匹配。

</div>
<div class="notation-item" markdown="1">

**$z$**

模型生成过程中的隐藏状态表示，可被用于构造激活方向、低秩干预或训练正确性探针。

</div>

</div>

**直接相关的工作**

- **Hendel et al.（2023）与 Todd et al.（2023）的 task/function vectors**: 这些工作表明，示例或上下文可能在激活空间中诱导紧凑的任务或函数向量，为本文寻找“提示行为的内部表示”提供动机。但本文的对象是长程序生成，并以可执行正确性、提示救援和损伤作为评价，而不是仅观察受控映射上的目标行为变化。
- **Wang et al.（2022）的 self-consistency 与多轨迹采样**: 该方向说明重复生成多个推理或生成轨迹能够提高找到正确答案的机会，直接对应本文的无提示 best-of-eight 对照。本文将这一对照用于区分提示带来的信息增益与普通采样已经可达、但单次生成未找到的正确程序。

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

论文采用“行为可达性—内部干预—上下文依赖—正确性读出”四层评估框架，区分四个容易混淆的问题：提示能否挽救贪心生成失败的任务、成功程序是否本来就能通过无提示采样得到、从提示中提取的内部表示能否迁移为稳定能力，以及隐藏状态能否预测程序正确性。行为实验以通过 EvalPlus 的 base 与 plus 两组可执行测试作为正确标准，并分别比较相关提示、无关提示和无提示多次采样；机制实验则测试激活方向、低秩干预、虚拟 KV 前缀和生成后探针。
直观地说，作者不把“看到提示后答对”直接解释为“模型学会了技能”：提示可能只是让模型更容易抽到它原本就会生成的程序。因此，方法同时检查成功答案的采样可达性、提示信息能否脱离原任务后迁移，以及内部信号究竟是可用于控制生成的因果机制，还是只能事后识别答案对错的相关性读出。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立失败任务与可执行正确性标签

运行 EvalPlus base 与 plus 测试；仅当基线贪心补全未同时通过两组测试时，任务才进入“可挽救失败”的分析范围。任一后续补全也必须同时通过两组测试才被判为成功。

<div class="method-step__io" markdown="1">

**输入**：HumanEval+、MBPP+ 等代码生成任务，以及模型的基线贪心补全。<br>
**输出**：基线失败任务集合，以及由程序执行结果确定的二元正确性标签。

</div>

**直观理解**：先找出模型第一次确定性作答失败的题，再用实际测试而非文本相似度判断程序是否真的正确。这样可以避免把代码外观接近参考答案误当成成功。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 比较提示挽救与无提示采样可达性

若条件 $c$ 下的补全同时通过 base 与 plus 测试，则记该任务被 $c$ 挽救；若 $k$ 个无提示样本中至少一个通过，则记该任务属于预算 $k$ 下的 sampled support。相关提示与无关提示的配对差被用来接近语义提示优势，但原实验没有完全匹配尝试次数、风格、长度和随机种子。

<div class="method-step__io" markdown="1">

**输入**：基线失败任务、相关提示、无关提示，以及预算为 $k$ 的无提示随机样本。<br>
**输出**：各条件的挽救任务集合、预算依赖的无提示可达集合，以及二者的重叠关系。

</div>

**直观理解**：如果提示救回的题在多抽几次无提示答案时也能做对，那么提示可能是在“导航”已有能力，而不是提供模型原本缺失的技能。由于各条件尝试预算并未完全一致，相关提示与无关提示的差异不能被直接解释为纯语义因果效应。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 测试内部表示与上下文程序的迁移

论文测试提示条件是否共享稳定激活方向，并在生成期间持续加入该方向；同时评估学习式低秩干预和虚拟 KV 前缀。对上下文定义的程序，则比较无上下文、无关上下文、完整文字规格与示例、以及虚拟前缀的表现。

<div class="method-step__io" markdown="1">

**输入**：相关提示和无关提示诱导的隐藏激活、学习得到的低秩干预、虚拟 KV 前缀，以及需要上下文说明的程序任务。<br>
**输出**：干预造成的挽救与退化、估计的行为改变量，以及不同上下文载体对程序执行成功率的影响。

</div>

**直观理解**：这一阶段把提示携带的信息从文字表面剥离出来，检查它能否压缩成一个可复用的内部控制信号。仅有相似的激活模式并不够；只有在未用于估计该信号的任务上稳定改善行为，才构成能力迁移证据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 训练并跨基准评估正确性读出

使用隐藏状态训练正确性探针，并在不同基准之间测试其迁移；探针还与 token confidence 等候选选择信号比较。该实验只检验正确性是否可从表示中解码，不把预测成功等同于模型在生成时使用了该特征。

<div class="method-step__io" markdown="1">

**输入**：代码生成完成后的隐藏状态及其执行正确性标签。<br>
**输出**：跨基准正确性预测分数，以及用于候选程序排序或 top-one 选择的信号。

</div>

**直观理解**：探针像一个事后阅卷器：它观察模型内部状态并猜测代码能否通过测试。阅卷器猜得准只说明内部状态含有相关信息，并不能证明生成器会主动利用该信息修正代码。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：所给章节没有给出统一的模型训练目标或中心优化方程。方法主要是评估协议：用可执行测试定义成功，以相关提示、无关提示和无提示采样比较行为可达性，再对激活方向、低秩干预、虚拟 KV 前缀和正确性探针进行迁移或读出测试；低秩干预与探针的具体损失函数、参数估计过程及优化器在所给节选中未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 行为可达性与语义提示对照**

核心分析对象包括条件 $c$ 的 rescue、预算 $k$ 下的 sampled support，以及相关提示相对匹配无关提示的配对差。原文明确指出当前无关提示对照没有同时匹配尝试次数、风格、长度和随机种子，因此只能提供提示语义作用的提示性证据。

> 直观理解：该模块用于区分“提示补充了不可缺少的信息”和“提示提高了抽中已有答案的概率”。若不控制尝试预算等因素，提示条件成功更多也可能只是因为获得了不同数量或不同形式的尝试机会。

**2. 任务外估计的内部干预**

激活对象只有在不使用评估任务进行估计，并相对于范数、秩、通道和计算量匹配的控制条件改善留出任务表现时，才被定义为 intervention transfer。余弦方向稳定或对训练集激活能量的高解释率只被视为表征证据。

> 直观理解：一个方向在不同提示下都出现，只能说明模型内部反应相似；真正的迁移要求把该方向施加到新题时能可靠提高正确率，而且提升不能由干预更强或计算更多解释。

**3. 上下文依赖与正确性读出**

上下文定义程序要求无上下文和无关上下文的重复尝试很少成功，而完整规格与示例能够成功；除非随机秘密使缺少上下文时在信息论上不可能求解，否则论文不声称能力“可证明地不存在”。正确性探针则从生成后隐藏状态预测执行标签，其结论限于给定训练—测试协议下的可解码性。

> 直观理解：上下文任务检查模型是否真正获得了题目现场给出的新规则；探针检查内部是否留下“这段代码可能正确”的痕迹。前者研究信息传递，后者研究信息读取，两者都不能单独证明模型形成了可泛化的新技能。

**训练与推理**

推理时，先对每个任务取得基线贪心补全并执行 EvalPlus base 与 plus 测试，筛选同时未通过两组测试的失败任务；随后分别在相关提示、无关提示和无提示随机采样条件下生成代码并再次执行测试。对无提示条件，以至少一个成功样本定义预算 $k$ 下的 sampled support，并检查提示挽救集合有多少也能由普通采样覆盖。机制部分在 Qwen 上提取相关与无关提示共享的激活方向并持续注入生成过程，同时评估学习式低秩干预；上下文任务比较完整文字规格及示例与虚拟 KV 前缀；最后用生成后的隐藏状态训练正确性读出并进行跨基准测试。上述模型层、注入位置、采样参数、干预训练划分和探针结构在所给节选中未明确报告。

**复现信息**

公平解释结果所必需的细节有三点。第一，正确程序必须同时通过 EvalPlus base 与 plus 测试，rescue 只针对基线贪心失败的任务；第二，sampled support 是预算 $k$ 依赖的经验概念，有限次采样失败不能证明成功概率为零；第三，当前提示条件没有完全匹配尝试预算、风格、长度和随机种子，因此不能从相关提示与无关提示的原始差值中识别纯语义效应。内部干预若要被认定为迁移，还应在任务外估计，并采用范数、秩、通道及计算量匹配的控制；这些匹配控制的具体实现，以及模型解码超参数，在所给材料中原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HumanEval+：包含 $164$ 个 HumanEval 任务；程序必须同时通过基础测试和 EvalPlus 增强测试。Qwen 学生模型通过 $113/164$ 个任务，教师通过 $136/164$ 个任务；两者交集得到 $29$ 个“教师通过、学生失败”的选定失败任务，用于提示和干预实验。
- MBPP+：包含 $378$ 个 MBPP 任务，评测规则与 HumanEval+ 相同。Qwen 学生模型通过 $249/378$ 个任务，教师通过 $268/378$ 个任务；交集得到 $50$ 个 Qwen 选定失败任务。Phi-3.5-mini 的对应选定失败任务为 $68$ 个。
- 上下文定义程序任务与跨基准候选程序集：前者包含四类程序族，每类有 $3$ 个示例和 $6$ 个留出问题，共 $24$ 个问题；后者覆盖 HumanEval+ 与 MBPP+ 的 $542$ 个任务，每个任务生成 $8$ 个候选，共 $4,336$ 个带执行标签的程序，用于训练和测试正确性探针。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**通过率或救援数**

通过率是通过执行测试的任务或候选数占总数的比例；救援数是原先失败、在干预或提示后通过的任务数。 （越高越好，但救援数必须结合对应的选定失败集合、尝试次数和解码协议解释，不能直接外推为完整基准准确率。）

</div>
<div class="metric-item" markdown="1">

**AUROC**

受试者工作特征曲线下面积，衡量模型将正确候选排在错误候选之前的整体排序能力；汇总 AUROC 混合了任务难度，任务内 AUROC 则在同一任务的候选之间比较。 （越高越好；$0.5$ 表示接近随机排序，但较高的汇总值不一定意味着能稳定选出每个任务的最佳候选。）

</div>
<div class="metric-item" markdown="1">

**精确 McNemar 检验的 $p$ 值**

在同一批任务上比较两个二元选择器，检验一个选择器相对于另一个选择器的改进与退化是否不对称。 （通常以较小的 $p$ 值作为差异更有统计证据的信号；较大的 $p$ 值表示未检测到可靠差异，而不是证明两者等价。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 相关提示、无关提示与普通采样的行为救援（Qwen2.5-3B-Instruct；选定的 $79$ 个失败任务）

<div class="result-value" markdown="1">

相关提示梯度救援 $36/79$ 个任务，无关提示救援 $19/79$ 个任务；无提示八次采样解决 $46$ 个任务，并覆盖相关提示救援中的 $31$ 个。

</div>

相关提示确实能把部分失败程序变成通过程序，但许多这样的解已经能通过普通随机采样获得，因此结果不支持“提示主要传授了全新任务技能”的强解释。由于相关提示有最多三次机会、无关提示只有一次，而采样还改变了解码规则，这些数字只能比较整套程序，不能隔离提示语义的纯粹因果效果。

<div class="result-source" markdown="1">

来源：摘要；第 4.2 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For Qwen2.5-3B-Instruct, adaptive relevant hints rescue 36 of 79 selected failures; an unrelated hint rescues 19, while eight unhinted samples solve 46 and recover 31 of the 36 relevant-hint rescues.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 隐藏状态方向的持久注入与任务级干预（Qwen 主学生模型）

<div class="result-value" markdown="1">

持续加入由提示差分得到的方向产生 $14$ 个救援和 $18$ 个回归，未检测到净准确率提升；学习到的低秩干预效果为正，但估计不精确。完整的每任务 oracle 增量只作为正控制，不代表可部署方法。

</div>

相关提示和无关提示可能共享稳定的内部激活方向，但把这个平均方向持续注入生成过程并不能稳定改善结果，甚至会损害原本正确的生成。因而“存在共同表示方向”不等于“该方向编码了可迁移的任务能力”；低秩结果也不足以给出精确的正向因果结论。

<div class="result-source" markdown="1">

来源：摘要；第 4.3 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Persistently adding this direction yields 14 rescues and 18 regressions, with no detectable net accuracy gain; learned low-rank interventions have a positive but imprecise estimated effect.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨基准生成候选的正确性读取与选择

<div class="result-value" markdown="1">

源基准选择后的隐藏探针在 HumanEval+ 上的汇总 AUROC 为 $0.806$，在 MBPP+ 上为 $0.780$；任务内 AUROC 分别为 $0.654$ 和 $0.634$。与平均词元对数概率结合后，HumanEval+ 目标集选择 $122/164$ 个通过程序，MBPP+ 选择 $244/378$ 个；相对于置信度单独选择，精确 McNemar 检验的 $p$ 值分别为 $0.093$ 和 $0.503$。

</div>

隐藏状态包含可跨基准迁移的正确性相关信号，并且部分信号超出简单词元置信度；但汇总与任务内 AUROC 的差距说明任务难度解释了其中一部分。最终选出每个任务一个候选时，组合方法的点估计更高，却未达到通常的统计显著性标准，因此不能宣称其稳定优于置信度或贪心解码。

<div class="result-source" markdown="1">

来源：第 7 节；表 3；图 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The hidden probe’s pooled AUROC is 0.806 (task-bootstrap 95% CI [0.750, 0.861]) on HumanEval+ and 0.780 ([0.742, 0.819]) on MBPP+.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 提示、无关提示和八次采样的机会数及解码规则不一致，相关提示实验回答的是程序条件之间的整体差异，而非语义内容的纯因果效应；同时，救援集合只包含教师通过、学生失败的任务，不能代表完整基准。
- 正确性探针使用 $4,336$ 个程序的执行标签，推理仍需八次生成和白盒隐藏状态；隐藏信号可能来自长度、终止、语法、记忆化错误模式等未完全控制的因素。虚拟上下文实验仅有 $24$ 个问题且嵌套于四个程序族，干预研究的样本也较小，因此未检测到优势不能解释为等价或普遍有效。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 无提示的最佳八次采样：使用温度 $0.8$ 和 $top\text{-}p=0.95$，用于检验提示带来的救援是否只是增加生成机会或改变随机搜索，而非语义信息的作用。
- 无关提示：为另一个已通过任务生成的一级提示，并按词元长度匹配相关提示，用于测试非任务相关文本本身是否也能产生救援。
- 平均词元对数概率：对八个候选按模型置信度排序，是隐藏状态正确性探针的主要黑盒比较对象；它测试隐藏表示是否提供超出常规生成置信度的信号。
- 表面特征与字符级 TF-IDF 分类器：分别使用 $23$ 个代码语法及长度特征、字符 $3$--$5$ 元 TF-IDF，检验隐藏状态探针是否只是利用代码长度、终止形式、语法或其他可见文本线索。

**实验想回答的问题**

- 相关提示使原本失败的代码通过测试时，提升是否主要来自提示提供了任务所缺失的信息，还是普通采样本来就能找到该解？
- 模型隐藏状态中的提示方向、低秩干预和正确性探针，能否分别实现任务行为迁移或跨基准的候选程序正确性识别？

**实验实现**

主要学生模型是冻结的 Qwen2.5-3B-Instruct，Phi-3.5-mini-instruct 用于复现实验；Qwen2.5-Coder-7B-Instruct 仅用于找出教师通过而学生失败的任务并生成最小提示，不被视为全知 oracle。默认采用贪心生成，采样采用温度 $0.8$、$top\text{-}p=0.95$，最多生成 $512$ 个新词元；运行使用 BF16、随机种子 $42$、批大小 $12$ 和左填充。提示实验中，相关提示形成最多三级的自适应梯度，每项通常不超过 $23$ 个词；无关条件仅使用一级提示，因此与相关提示及八次采样并非严格等预算比较。隐藏状态实验在每层后块残差流捕获表示，并在提示与基础输入共享的对齐位置比较；持久注入、一次性 oracle 增量和低秩干预分别测试方向稳定性、单位置因果作用及跨任务概括。正确性探针采用单位归一化隐藏状态上的类别平衡、$\ell_{2}$ 正则逻辑回归，候选层为 $\{8,14,20,26,32\}$，通过按任务分组的五折交叉验证在源基准选择层、池化方式和正则强度，再在另一基准上评估。统计上以任务为重采样单位，使用任务 bootstrap、配对任务 bootstrap、精确 McNemar 检验和 $95\%$ Wilson 区间。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 完整文本规范与虚拟 KV 前缀在上下文定义程序上的比较 | 四类程序族的完整文本上下文加示例共解决 $22/24$ 个留出问题；训练的虚拟 KV 前缀各长度和控制组的逐族结果见表 B1，效果明显较弱，例如 $k=2$、$k=4$、$k=8$、$k=16$ 在四族合计分别为 $8$、$2$、$4$、$6$ 个通过问题。 | 完整文字规范能直接提供模型执行新程序语言所需的规则和示例，而短虚拟前缀即使在示例交叉熵上拟合成功，也未稳定把规则迁移到隐藏测试题。这说明压缩后的参数化提示不应仅凭训练损失判断其是否学会了程序规则。 | 摘要；附录 B 表 B1<br><span class="experiment-evidence">Full textual specifications solve 22 of 24 context-defined problems, versus 5-11 for tested virtual-KV prefixes.</span> |
| 正确性探针相对于表面特征、字符 TF-IDF 和置信度的消融 | HumanEval+ 上隐藏探针的汇总/任务内 AUROC 为 $0.806/0.654$，平均词元对数概率为 $0.653/0.627$，$23$ 个表面特征分类器为 $0.692/0.567$，字符 TF-IDF 为 $0.657/0.560$；MBPP+ 上对应隐藏探针为 $0.780/0.634$，平均词元对数概率为 $0.626/0.593$，表面特征为 $0.612/0.567$，字符 TF-IDF 为 $0.623/0.555$。 | 这一比较检验隐藏表示是否只是在识别代码长度、语法和字符模式。隐藏探针的点估计整体更高，尤其任务内排序仍高于随机水平，支持其包含额外的正确性相关信息；不过表面基线也有明显信号，且未覆盖所有可能的文本混淆因素，所以不能据此断言探针读取了模型独有的“自知”。 | 第 7 节<br><span class="experiment-evidence">A 23-feature syntax-and-length classifier reaches pooled/within-task AUROC 0.692/0.567 on HumanEval+ and 0.612/0.567 on MBPP+; a character TF-IDF classifier reaches 0.657/0.560 and 0.623/0.555.</span> |

**定性案例**

- 在选定的 CRW（有序字符串重写）程序族中，$k=2$ 的虚拟 KV 前缀后续测试使用新测试案例和五个扰动初始化；每次运行都解决相同的 $3/6$ 个案例，而大小匹配控制组解决 $2/6$ 个。该重复性更像是稳定的题目重叠或问题级偏差，而不是五次独立的六题泛化复制，因此只能说明局部可重复，不能证明虚拟前缀学会了完整规则。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper studies whether hints and internal interventions transfer coding problem-solving capabilities in language models.; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`98ae40cc0c0c82f21c613bd346f722ad3ae53df9321a08f5c28624b32a6c8a70`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
