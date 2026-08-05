---
title: "[论文解读] Attention is Case-Sensitive"
description: "[arXiv 2608.03711][LLM 机制与可解释性] 本文系统检验并发现：在语义与词序不变时，改变字母大小写即可重分配大语言模型及视觉语言模型的内部注意力，但注意力增强并不必然带来更高任务准确率，且推理过程构成重要边界条件。"
arxiv_id: "2608.03711"
announcement_date: "2026-08-05"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:38:53.682383+00:00"
source_sha256: "11f2122606f19a5de50b070c27313ae4873021c893c8b7d40489185cecdef007"
tags:
  - "LLM 机制与可解释性"
  - "LLM 其他"
  - "LLM Reasoning"
  - "多模态 VLM"
  - "字母大小写"
  - "注意力分配"
  - "大语言模型"
  - "视觉—语言模型"
  - "正字法变体"
  - "注意力引导"
  - "模型可解释性"
  - "推理缓冲"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2608.03711</p>

# Attention is Case-Sensitive

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Maximilian Dillitzer, Tin Stribor Sohn, Jason J. Corso, Michael Auerbach</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> University of Applied Science Esslingen；Karlsruhe Institute of Technology；University of Michigan</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03711v1) · [PDF 下载](https://arxiv.org/pdf/2608.03711v1) · **关键词** 字母大小写, 注意力分配, 大语言模型, 视觉—语言模型, 正字法变体, 注意力引导, 模型可解释性, 推理缓冲<br>


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

本文系统检验并发现：在语义与词序不变时，改变字母大小写即可重分配大语言模型及视觉语言模型的内部注意力，但注意力增强并不必然带来更高任务准确率，且推理过程构成重要边界条件。

**不用术语来说**：同一句话可以只改变大小写而不改变含义，但模型可能因此把更多“注意力”放在某些词上。过去通常把这种差异看成分词造成的格式现象，尚不清楚模型是否在预训练中把大写等排版特征学成了隐含的重要性信号，也不清楚这种信号能否跨模型、跨文本与视觉模态稳定存在，以及它究竟帮助还是损害任务表现。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将大小写作为预分词阶段的单一干预变量，在保持词序和语义上下文不变的条件下，对多种规模、架构与分词方案的语言模型和视觉语言模型进行系统表征，提出并验证“大小写显著性”这一潜在注意力属性；同时通过反向弱化设置区分目标内容与上下文的大小写，以支持注意力变化确由正字法形式触发。
- 作者揭示了注意力变化与任务效用之间并非单调对应：大写与交替大小写都可能吸引注意力，但后者可能因形式噪声而降低性能；此外，文本推理阶段可缓冲排版敏感性，而视觉语言推理可能更多转向文本流，说明该效应受到推理方式和模态的共同约束。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型与视觉—语言模型的可解释性研究领域，关注 Transformer 的注意力分配是否会受到文本表面形式影响。以往“注意力引导”通常通过修改模型参数、在推理时重缩放注意力分数或向隐藏状态注入控制向量来改变模型焦点；另一类工作研究位置偏置、特殊标记和结构化分隔符，但这些变化往往会增加标记、调整顺序或引入语义与结构提示。本文转而考察一种更小的输入扰动：只改变字母大小写，在保持词汇内容、词序、语义上下文以及多模态实验中的图像不变时，观察模型内部注意力是否系统性地转向大小写突出的目标文本及其对应图像区域。研究对象包括非推理与推理型 LLM、非推理与推理型 VLM，并覆盖不同规模和分词方案。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**Transformer 注意力**

注意力机制为当前计算中的不同输入标记分配权重，用来表示模型在形成内部表示或生成输出时对各位置的相对关注程度。本文研究的是大小写能否改变这种权重分布，而不预设更高注意力必然产生更好的答案。

</div>
<div class="concept-item" markdown="1">

**正字法变体**

正字法变体是词语书写形式的变化；本文具体指全小写、全大写或大小写交替等字母 casing 变化。实验保持词汇内容和词序不变，从而尽量把注意力差异归因于大小写这一表面特征。

</div>
<div class="concept-item" markdown="1">

**视觉—语言模型与跨模态注意力**

视觉—语言模型同时处理图像和文本提示，内部注意力可以在文字标记与图像区域之间分配。本文不仅考察提示大小写是否令模型整体减少对图像的关注，还考察剩余视觉注意力是否更集中到目标文字所对应的图像区域。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是语义内容与词序相同、仅字母大小写模式不同的文本；在 VLM 设置中，配套图像也保持完全不变。研究者在分词前控制大小写这一独立变量，将目标信息设为全大写或大小写交替，并置于小写上下文中；同时使用“上下文大写、目标小写”的对抗性去强调条件检查方向是否反转。输出不是一种新的训练算法，而是对模型行为的经验刻画：比较不同大小写条件下目标文本的相对注意力质量、VLM 对文本与图像的总体注意力分配、目标图像区域获得的视觉注意力，以及这些内部变化与下游准确率之间的关系。基本假设是词汇和语义内容不变，因而观察到的系统性差异主要来自书写表面形式；但由于大小写可能改变分词结果，研究通过多种 tokenizer 和模型进行跨架构验证，而非假定所有条件产生完全相同的 token 序列。作者还区分非推理模型与带显式“思考”阶段的推理模型，以检验推理过程是否会缓冲这种表面形式敏感性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **PASTA、AutoPASTA 与 InstABoost**: 这些方法在前向推理期间手工放大特定标记的注意力分数，能够对冻结模型实施注意力引导，但需要白盒访问、运行时钩子或额外计算。本文与之不同，仅改变输入字母大小写，不修改参数或内部计算，研究预训练模型已经具有的自然敏感性。
- **ROME、MEMAT、MEND 与 REMEDI**: 这些工作通过参数编辑改变事实回忆或相关内部行为，代表训练期或结构层面的模型干预。本文不试图把某种注意力模式写入模型，而是描述预训练权重中是否已经内化了大小写显著性，并进一步区分注意力变化与任务性能变化。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

提示词中的大小写是一种无需微调、适配器或模型内部访问即可实施的零样本干预，因此可能成为低成本的注意力控制手段；但若模型会把纯排版差异误当作内容重要性，它也会成为提示鲁棒性与模型解释中的潜在混杂因素。研究者因而需要先确定这种效应是否真实、普遍且具有因果针对性，并判断内部注意力的改变是否会可靠地转化为更好的文本或多模态任务表现。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **将大小写视为分词或输入格式差异**：常规理解把大小写主要看成会改变词元切分或词元身份的输入表面属性，并不把它单独视为模型在预训练中形成的潜在重要性信号；因此，相关分析往往停留在输入编码差异，而未系统隔离语义不变时的内部注意力响应。
- **依赖模型修改的注意力干预**：典型注意力控制思路需要微调、插入适配器或在运行时访问并调整模型内部状态。本文并未逐项评测这些方法，而是以它们为对照需求，考察仅改变提示文本大小写的黑盒、训练免费干预能否重定向模型关注。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 若仅把大小写差异归因于分词，就无法回答在词序和语义保持不变时，大小写本身是否会系统性改变注意力分配，也无法区分偶然的词元变化与模型内化的排版显著性。
- 已有认识缺少对“注意力增加是否等于任务收益”的系统区分，也未充分刻画推理模型及视觉语言模型中的边界条件；其后果是，即使观察到目标区域获得更多注意力，也不能据此断言准确率会提高或效应能跨模态直接迁移。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一项受控、跨模型且跨模态的经验研究，将字母大小写作为独立变量，联合检验三个彼此不同的问题：它是否稳定吸引内部注意力、这种变化是否独立于模型规模和分词方案、以及注意力重分配与下游性能之间究竟是什么关系。尤其未知的是，模型的显式推理阶段会过滤还是放大这种表面线索，以及文本提示中的大小写能否进一步改变视觉语言模型对图像和目标区域的关注。

</div>
<div markdown="1"><span>核心问题</span>

在不改变文本语义与词序、也不修改模型参数的前提下，仅将目标片段设为大写或交替大小写，是否会因模型预训练中形成的潜在排版显著性而因果性地重分配语言模型和视觉语言模型的注意力；若会，这种效应如何影响任务准确率，并受到推理阶段与模态差异怎样的制约？

</div>
<div markdown="1"><span>作者直觉</span>

人类在小写文本中会自然注意到形状突出的 uppercase 片段；模型虽然不以人类方式观看字符，但其预训练语料包含大量稳定的排版惯例，例如标题、强调和专名常使用大写。因而，大小写对应的词元与表示可能在训练中反复同“重要内容”共同出现，使突出的大小写模式成为隐含注意力吸引子。不过，吸引注意力只表示计算资源发生偏移，并不保证该偏移包含有用语义：规则大写可能强化目标，而交替大小写可能同时制造高熵形式噪声；推理阶段则可能依据语义一致性重新校正这种表面偏向。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是提出需要训练的新模型，而是设计一套“预分词大小写干预”协议，用受基准标注确定的目标答案文本或目标图像区域作为研究对象。给定原始字符序列 $X=(x_1,\dots,x_N)$ 及标注目标 $A$，方法只改变字母大小写，生成 $\tilde{X}$，再将 $X$ 与 $\tilde{X}$ 分别输入同一个冻结模型 $f_\theta$；通过比较目标上的平均注意力 $\operatorname{Att}_A$ 以及文本任务准确率 $\operatorname{Acc}$，估计大小写变化对模型内部注意力分配和外部任务表现的影响。对视觉语言模型，提示文本仍接受大小写干预，而目标 $A$ 从文本跨度扩展为标注框对应的图像块或像素区域。

该设计的关键是以真实标注直接定位应被强调的内容，从而不把“能否先找到目标”与“大小写是否改变注意力”混在一起。通俗地说，实验者预先知道正确答案或正确区域在哪里，只给这些内容及其上下文换一种大小写“外观”，然后观察同一模型是否因此把更多或更少注意力放到目标上；这是一项受控特性研究，而不是可直接部署的自动目标发现与提示优化系统。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 读取样本并定义干预目标

将 $A$ 作为唯一需要定向施加排版干预并测量注意力的目标；在文本任务中 $A\subseteq X$，在视觉任务中则把边界框映射到对应图像块或像素区域。

<div class="method-step__io" markdown="1">

**输入**：基准样本中的原始文本字符序列 $X=(x_1,\dots,x_N)$，以及基准提供的真实答案跨度或边界框标签 $A$。<br>
**输出**：带有确定目标位置的原始样本 $(X,A)$。

</div>

**直观理解**：这里不让另一个模型猜测重点，而是直接使用数据集给出的正确答案或正确区域。这样后续差异更容易归因于大小写，而不是目标定位错误。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 匹配并校准目标跨度

首先进行不区分大小写的精确匹配；失败时使用编辑距离不超过 $2$ 个字符的 Levenshtein 对齐，并以人工抽查验证回退匹配的可靠性。标点、数字、空白、词序和词汇结构均保持不变，固有混合大小写实体按整个跨度统一变换。

<div class="method-step__io" markdown="1">

**输入**：原始文本 $X$ 与基准答案 $A$。<br>
**输出**：与原文字符位置对齐、可确定性变换的目标跨度。

</div>

**直观理解**：这一步相当于在原文中准确圈出答案；少量拼写差异可用近似匹配处理，但不能借机改写句子。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行预分词大小写干预

在模型分词之前应用确定性变换 $\mathcal{T}_{\mathcal C}$，逐字符选择 upper、lower、title 或 alternating 模式，得到 $\tilde{X}$；干预要求字符转为小写后与原字符一致，因此改变的是字形大小写而非词汇身份。

<div class="method-step__io" markdown="1">

**输入**：已对齐的 $(X,A)$、目标大小写模式以及上下文的互补模式。<br>
**输出**：自然大小写输入 $X$ 及仅大小写不同的干预输入 $\tilde{X}$。

</div>

**直观理解**：例如可把答案改成全大写、把周围文字保持小写，从视觉形式上突出答案。虽然文字含义和空白结构不变，模型的分词器仍可能为 $X$ 与 $\tilde{X}$ 产生不同的 token ID 序列，这正是模型实际处理大小写时的一部分反应。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 冻结模型对照测量

分别运行两种输入，不更新参数，也不针对具体模型调节干预；聚合所有层和注意力头在目标 $A$ 上的平均注意力，并在文本任务中同时测量准确率，再计算其相对自然大小写基线的方向与幅度。

<div class="method-step__io" markdown="1">

**输入**：配对输入 $X$ 与 $\tilde{X}$、目标 $A$，以及冻结的语言模型或视觉语言模型 $f_\theta$。<br>
**输出**：目标注意力变化，以及文本任务中的准确率变化；跨模型汇总后用于判断现象是否稳定存在。

</div>

**直观理解**：同一模型完成两次近似相同的测试，唯一受控差别是字母大小写。研究既记录注意力是否被吸引，也记录答题是否真的改善，因为“看得更多”不必然意味着“答得更对”。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 预分词大小写变换及词汇身份约束

$$
\tilde{X}=\mathcal{T}_{\mathcal{C}}(X)=\big(c_{1}(x_{1}),c_{2}(x_{2}),\dots,c_{N}(x_{N})\big),\qquad \forall i,\ \texttt{lower}\big(c_i(x_i)\big)=\texttt{lower}(x_i)
$$

**符号说明**

- $X=(x_1,\dots,x_N)$：由 $N$ 个字符组成的原始输入文本。
- $x_i$：原始文本中的第 $i$ 个字符。
- $\tilde{X}$：仅经过大小写变换的输入文本。
- $\mathcal{T}_{\mathcal C}$：由大小写指派规则 $\mathcal C$ 决定的确定性字符级变换。
- $c_i$：施加在第 $i$ 个字符上的 upper、lower、title 或 alternating 操作。
- $\texttt{lower}(\cdot)$：将字符规范化为小写、用于检查其不区分大小写的身份是否相同的操作。
- $N$：输入字符序列的长度。

<div class="equation-explanation" markdown="1">

**直观理解**：等式首先逐字符构造干预输入，随后要求每个变换字符在转成小写后仍等于原字符的小写形式。因此实验允许“a”变成“A”，但不允许把“a”替换成“b”；它形式化了“只改变大小写、不改变词汇内容”这一核心控制条件。<br>
**原文位置**：第3.3节，公式(1)与公式(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 大小写敏感性的对照检验关系

$$
\operatorname{Att}_{A}\!\left(f_{\theta}(\tilde{X})\right)\neq \operatorname{Att}_{A}\!\left(f_{\theta}(X)\right),\qquad \text{and in text}\quad \operatorname{Acc}\!\left(f_{\theta}(\tilde{X})\right)\neq \operatorname{Acc}\!\left(f_{\theta}(X)\right)
$$

**符号说明**

- $f_\theta$：参数为 $\theta$ 的冻结语言模型或视觉语言模型。
- $\theta$：预训练模型参数；实验期间保持不变。
- $A$：基准标注给出的文本目标跨度，或视觉任务中对应的图像区域。
- $\operatorname{Att}_A(\cdot)$：跨模型层和注意力头聚合后，落在目标 $A$ 上的平均注意力权重。
- $\operatorname{Acc}(\cdot)$：冻结模型在文本下游任务上的准确率。
- $X$：采用数据集自然大小写的基线输入。
- $\tilde{X}$：施加受控大小写干预后的输入。

<div class="equation-explanation" markdown="1">

**直观理解**：该关系表达待检验假设，而不是预先保证成立的优化目标：若大小写是模型内在的重要性信号，则干预前后目标注意力应出现差异，文本任务表现也可能变化。论文不要求变化为正，也不假设注意力越集中准确率越高，而是测量变化的方向和幅度。<br>
**原文位置**：第3.3节，公式(3)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该研究没有损失函数、反向传播或参数优化；所有 $f_\theta$ 均以冻结的现成模型运行，大小写规则也不通过数据学习。公式中的注意力差异和准确率差异是经验检验量，不是训练时要最小化或最大化的目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 真实标注引导的目标定位**

目标跨度或视觉区域严格来自基准标注，而不是由辅助模型或启发式方法预测；文本目标采用精确匹配加有限编辑距离回退的两阶段对齐。

> 直观理解：该模块主要服务于因果隔离：若目标位置本身是猜出来的，注意力变化可能来自猜错位置，而不能纯粹归因于大小写。其代价是实验依赖真实标注，因此论文明确没有提供可部署的自动目标发现流程。

**2. 确定性大小写变换器**

变换器在分词前按字符应用 $\mathcal C:\Sigma\rightarrow\{\text{upper},\text{lower},\text{title},\text{alternating}\}$，只改变字母大小写，并保持词序、空白、标点、数字及词汇结构不变。目标 $A$ 使用指定模式，周围上下文使用互补模式。

> 直观理解：它像一个只允许按下 Shift 键的编辑器：可以改变文字外观，却不能增删词语或调整句序。预分词执行意味着实验同时保留大小写对分词结果产生的真实影响，而不是强行要求两种输入具有相同 token。

**3. 跨层目标注意力与性能评估器**

对冻结模型输出，$\operatorname{Att}_A(\cdot)$ 表示跨全部层和注意力头、聚合到目标 $A$ 上的平均注意力；文本实验另以 $\operatorname{Acc}(\cdot)$ 衡量任务准确率。视觉语言模型中的 $A$ 对应边界框覆盖的图像块或像素，使提示侧干预可以与视觉目标注意力关联。

> 直观理解：该模块把内部反应和最终行为分开检查：前者回答模型是否更关注目标，后者回答这种关注是否有助于完成任务。两者并列测量可避免把注意力增加直接解释成性能提升。

**训练与推理**

训练阶段不存在：论文不微调模型、不训练目标定位器，也不针对不同模型学习大小写策略。推理阶段先从基准标注取得 $A$，完成字符级对齐，再在分词前生成 $\tilde{X}$；随后将自然大小写的 $X$ 和干预后的 $\tilde{X}$ 分别送入同一个冻结模型，抽取目标注意力并评估文本任务准确率。该流程以自然大小写输入作为每个模型自身的基线，并在不同模型家族和分词方案上使用相同干预，不做逐模型调参。

这一过程属于有真实标注参与的离线特性刻画，而不是普通用户场景中的端到端推理工具。由于测试时已借助答案跨度或边界框确定应强调的位置，它能够较干净地回答“大小写本身是否调制注意力”，但不能证明系统在未知答案时能自动找到并强调最有用的内容。

**复现信息**

为复现实验，目标文本首先采用不区分大小写的精确匹配；原文报告其覆盖 $98.2\%$ 的样本，其余 $1.8\%$ 使用 Levenshtein 距离不超过 $2$ 个字符的回退对齐，并对 $100$ 个样本子集进行人工核验。变换不得改变空白、标点、数字、词序或词汇结构；对于“iPhone”一类固有混合大小写实体，应对完整跨度统一变换。需要注意，论文所称“保持 token 边界”主要指不改动空白和词汇结构，并不意味着分词结果完全相同；作者明确允许 $X$ 与 $\tilde{X}$ 产生不同 token ID 序列。

跨架构评估使用完全相同的干预协议，并以各模型在数据集自然大小写下的结果作为比较基线。解释结果时必须保留两个限制：第一，目标由真实标注提供，因而实验测的是排版干预的纯效应，而不是自动定位能力；第二，研究只刻画注意力和准确率的变化，不把注意力集中预设为性能收益，也不宣称该协议已经构成可部署的自动化控制流水线。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MMLU-Pro 与 ARC-Challenge：用于评估事实知识和科学推理。实验将答案相关文本作为目标片段，以便只修改其大小写并观察注意力与准确率变化。原文节选未明确报告样本规模、具体子集或划分。
- SQuADv2：用于阅读理解，并利用其有标准答案的文本片段定位需要施加排版干预的目标。原文节选未明确报告样本规模、具体划分及不可回答样本的处理方式。
- RefCOCOg：用于指代表达视觉定位，提供与文本对象标签对应的真实边界框。实验仅改变描述提示中目标标签的大小写，图像保持不变，再测量边界框内注意力以及整幅图像获得的注意力。原文节选未明确报告所用划分和样本规模。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**目标注意力质量的百分点变化**

在文本实验中表示分配给答案相关目标片段的平均注意力占比相对自然大小写基线的绝对变化；在视觉实验中表示落入真实目标边界框的视觉注意力占比变化。它直接测量模型内部注意力是否被大小写引向目标，但不能单独说明模型是否正确理解目标。 （若研究目标是把注意力引向正确目标，则数值越高越好；但论文特别表明，注意力增加不必然带来准确率提升。）

</div>
<div class="metric-item" markdown="1">

**任务准确率的百分点变化**

比较大小写干预后与原始自然大小写条件下的下游答题准确率，用于判断内部注意力重分配是否转化为可观察的任务收益或损失。 （越高越好，因为正值表示正确回答比例提高；该指标是行为结果，而非注意力机制本身的直接度量。）

</div>
<div class="metric-item" markdown="1">

**整幅图像注意力质量及相对脱离率**

整幅图像注意力质量衡量视觉语言模型分给全部图像特征的注意力预算；相对脱离率表示该预算相对基线下降的比例。它刻画宏观的图像—文本模态路由，与目标框内注意力这一局部空间指标相互补充。 （没有统一的越高越好方向。若任务依赖图像，整图注意力下降或脱离率升高通常意味着模型更偏向文本，可能削弱视觉证据利用；但论文未在所给节选中报告其与视觉定位准确率的直接对应关系。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen2.5-7B-Instruct 上的文本注意力与下游准确率

<div class="result-value" markdown="1">

作者报告，目标交替大小写 TA 最能吸引注意力：TA3 和 TA2 的目标平均注意力分别提高 2.77 与 2.75 个百分点；但 TA 在各文本基准上反而使准确率下降，发现模型最大下降 2.88 个百分点。相比之下，目标大写、上下文小写的 TE1 使准确率提高 1.85 个百分点。

</div>

作者结论是存在“注意力—性能分离”：排版越醒目，不代表模型越能正确利用被吸引的注意力。分析上，交替大小写可能同时提高目标显著性和字符模式复杂度，从而成为“破坏性吸引物”；常规全大写则更接近预训练语料中的强调信号，可能成为“生产性吸引物”。这些结果证明了相关干预下的行为差异，但不能证明注意力增加本身直接导致准确率上升或下降，也不能排除分词变化等中介机制。

<div class="result-source" markdown="1">

来源：第 4.3—4.4 节；图 2 与图 11，绝对值另见表 9

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

While alternating case (TA) most effectively concentrates attention, it serves as a destructive attractor: across all benchmarks, TA schemes consistently degrade downstream accuracy, with drops of up to −2.88 pp on the discovery model (cf. Fig. 11).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 四个视觉语言模型在 RefCOCOg 上的跨模态迁移

<div class="result-value" markdown="1">

作者报告，非标准大小写使目标框内视觉注意力平均增加 1.55 个百分点，即相对增加 23.08%；与此同时，整幅图像得到的注意力平均减少 1.85 个百分点，即模型相对减少 12.41% 的视觉流投入而偏向文本提示。

</div>

这说明视觉语言模型出现两个耦合但方向不同的变化：剩余视觉注意力在局部上更集中于目标框，宏观上却整体远离图像。作者据此认为主要效应是模态路由，而不是单纯改善空间定位。该结果不等价于视觉任务性能提高；所给节选没有报告相应的定位准确率或框重叠指标，因此不能据注意力对齐直接推断模型看得更准。

<div class="result-source" markdown="1">

来源：第 4.5 节；图 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across the dataset, non-standard casing induces a coupled, dual-axis response (cf. Fig. 3): a microscopic concentration of the residual visual budget onto the target region (a mean +1.55 pp absolute shift, a relative +23.08% increase in target-region attention alignment), together with a macroscopic re-allocation away from the image as a whole (a mean −1.85 pp drop in whole-image attention mass, i.e., a 12.41% relative disengagement from the visual stream in favour of the textual prompt).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨模型、跨分词器以及推理模式的稳健性比较

<div class="result-value" markdown="1">

作者称大小写效应在所有受测非推理文本模型及 BPE、SentencePiece、字节级 BPE 三类分词器中方向一致；交替大小写造成的最严重准确率损失在 LLaMA-3.1-8B-Instruct 上达到 13.96 个百分点，而 TE1 与 TE3 的平均准确率增益最高达到 8.95 个百分点。思考式文本模型的准确率变化通常控制在正负 0.5 个百分点以内。

</div>

跨架构的一致方向削弱了“现象只由某个特定分词器产生”的解释，并表明自然大写强调与高熵交替大小写具有不同的行为后果。与此同时，推理模型近乎不敏感支持作者提出的“语义缓冲”解释：额外思考可能重新依据内容组织决策。这里的“普适”仅适用于论文评估的非推理文本模型；视觉模型只在模式族聚合和宏观模态轴上稳定，不能外推为所有 Transformer 或所有语言均如此。

<div class="result-source" markdown="1">

来源：第 4.6 节；图 4，扩展结果见附录 B.2、C、E

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In non-reasoning models, high-entropy casing acts as a destructive attractor; alternating case (TA) consistently degrades performance, reaching a peak loss of −13.96 pp in LLaMA-3.1-8B-Instruct.

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

- 原始自然大小写：保留基准数据的原始表面形式，作为计算注意力质量和任务准确率相对变化的主要参照；它能够区分大小写干预造成的变化与模型原本的行为。
- 全局统一大小写组 U：包括全文大写 U1、全文小写 U2 和每词首字母大写 U3。由于目标与上下文之间没有局部大小写反差，该组检验效应来自绝对大小写，还是来自目标相对上下文的显著性。
- 目标首字母大写组 TT：采用语法上更常见、更温和的强调方式，并改变上下文大小写。它用于判断普通书写规范是否足以产生与全大写或交替大小写相同的吸引效应。
- 对抗性去强调组 ADE：将目标改为小写，同时把上下文设为大写、交替大小写或自然形式。该反向对照故意降低目标的相对显著性，用于检验注意力变化是否会随对比方向反转，而不只是任何大小写改写都会产生扰动。

**实验想回答的问题**

- 在词汇内容、词序、标点和空格均保持不变时，仅改变目标文本与上下文的大小写对比，是否会因果性地改变不同语言模型的目标注意力分配，并进一步影响任务准确率？
- 文本侧的大小写显著性是否能跨模态迁移到视觉语言模型；若能，它主要改变目标框内的局部视觉注意力，还是改变模型在图像与文本之间的整体注意力预算？

**实验实现**

实验覆盖 13 个模型、五个模型家族，包括 9 个语言模型和 4 个视觉语言模型，并横跨 BPE、SentencePiece 与字节级 BPE 分词方案，以及直接推理和思考式推理模式。文本实验先以 Qwen2.5-7B-Instruct 作为发现模型，再扩展到其余模型检查普适性。所有输入只进行确定性的字母大小写变换，词汇、词序、标点和空格不变。干预按全局统一 U、目标大写 TE、目标首字母大写 TT、目标交替大小写 TA 和对抗性去强调 ADE 五组组织，每组通过不同上下文形式区分绝对大小写与相对反差。视觉实验把对象标签嵌入通用描述模板，仅改变标签或上下文的大小写，不修改图像，并依据真实边界框统计目标区域与整图注意力。作者称表面变换平均开销约为 0.0015 毫秒，但所给节选未说明注意力跨层、跨头聚合方式、解码参数、随机种子、置信区间或显著性检验，因此数值复核仍需查阅正文方法、附录和代码。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 交替大小写目标搭配自然、小写或大写上下文：TA3、TA2 与 TA1 | TA3 和 TA2 分别使目标平均注意力增加 2.77 与 2.75 个百分点，两者差异极小；即使把上下文全部大写，TA1 仍增加 2.44 个百分点。 | 该对照固定目标为交替大小写，只改变背景，从而区分目标自身的高熵字符模式与目标—上下文反差。TA2 与 TA3 接近，支持作者关于自然英语上下文本就以小写为主、主要驱动力来自目标交替模式的解释；TA1 仍有明显增益，则表明效应并非完全依赖小写背景。不过，它没有排除不同大小写导致目标被切分为不同 token 数量或边界的影响。 | 第 4.3 节；图 2 与图 9<br><span class="experiment-evidence">Specifically, TA3 (alternating target, natural context) and TA2 (alternating target, lowercased context) yield the highest gains of +2.77 pp and +2.75 pp in mean attention mass, respectively.</span> |
| 视觉语言模型中的模式冲突 TE2：大写目标置于交替大小写上下文 | TE2 造成最大的整图注意力流失，为 4.11 个百分点；四模型平均视觉脱离率为 33.35%，在 Qwen3-VL-2B-Thinking 上最高达到 43.74%。作为弱扰动参照，全文小写 U2 的目标区域空间注意力仅变化 0.48 个百分点。 | TE2 将常规的大写目标强调与高熵背景结合，用于测试上下文模式冲突是否会把模型整体处理资源拉向文本。其强烈整图流失表明，VLM 的主要反应并非只在图像内部移动注意力，而是减少对视觉流的总体使用。U2 的微小变化说明统一、低冲突的小写本身不是同等强度的扰动；但由于这里同时改变了目标相对显著性与上下文熵，不能把全部效应唯一归因于其中一个因素。 | 第 4.5 节“Pattern-conflict drives modality disengagement”；附录 B.5、表 14<br><span class="experiment-evidence">At the individual-pattern level, the pattern-conflicting configuration TE2 (uppercase target inside an alternating-case context) is the primary driver of modality disruption, producing the largest whole-image drain (−4.11 pp) and the strongest cross-model disengagement (a mean of 33.35%, and up to 43.74% on Qwen3-VL-2B-Thinking).</span> |

**定性案例**

- 图 3 使用 Qwen3-VL-2B-Thinking 在 RefCOCOg 样例上的 Grad-CAM 可视化，对比自然基线、U2、TE3、TT3、TA1 和 ADE1。作者借此展示：仅改变文本提示的大小写，就会改变视觉 Transformer 的跨模态注意力热图。该图适合直观说明空间注意力会移动，但单个热图不能建立总体规律或证明视觉定位正确，定量结论仍应以全数据集和多模型统计为准。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：系统分析字母大小写如何改变 LLM 和 VLM 的内部注意力分配及其与任务性能的关系。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`11f2122606f19a5de50b070c27313ae4873021c893c8b7d40489185cecdef007`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
