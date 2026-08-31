---
title: "[论文解读] Ladders in Chaos: When, How, (and Perhaps Why) Does Test-Time Scaling Improve LLM Machine Translation"
description: "[arXiv 2608.28496][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.28496"
announcement_date: "2026-08-31"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:36:10.666830+00:00"
source_sha256: "b08a0471477fd1d02e2cb14e8453400b9cb99ec9c61e16be65a6e977e4b00881"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型机器翻译"
  - "测试时扩展"
  - "顺序采样"
  - "并行采样"
  - "Best-of-$N$"
  - "自我改进"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.28496</p>

# Ladders in Chaos: When, How, (and Perhaps Why) Does Test-Time Scaling Improve LLM Machine Translation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Di Wu, Sergey Troshin, Christof Monz, Antske Fokkens, Vlad Niculae</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of Amsterdam</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28496v1) · [PDF 下载](https://arxiv.org/pdf/2608.28496v1) · **关键词** 大语言模型机器翻译, 测试时扩展, 顺序采样, 并行采样, Best-of-$N$, 自我改进<br>


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

本文位于大语言模型（LLM）机器翻译与测试时扩展（test-time scaling）交叉领域。测试时扩展不改变模型参数，而是在推理阶段增加生成计算，以获得更好的输出；本文将其简化为两种可比较的采样方式：并行采样独立生成多个候选译文，再用外部翻译质量模型进行 Best-of-$N$（BoN）重排序；顺序采样则让后续生成轮次看到并利用此前生成的译文，形成自我改进过程。研究重点不是提出复杂的多智能体系统，而是在相同生成预算下比较两种策略的样本效率、翻译质量维度差异，以及顺序采样可能有效的机制。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试时扩展**

测试时扩展是在模型已经训练完成后，于推理阶段增加采样或生成步骤，以提升最终输出质量。它不等同于继续训练，代价主要是更高的推理计算量。

</div>
<div class="concept-item" markdown="1">

**并行采样与顺序采样**

并行采样从同一个输入独立生成多个候选译文，候选之间互不依赖；顺序采样则把前一轮译文放入后续上下文，让模型基于先前结果继续生成或改写。前者探索多个独立路径，后者沿着依赖链逐步产生结果。

</div>
<div class="concept-item" markdown="1">

**Best-of-$N$与自我改进**

Best-of-$N$先生成$N$个候选，再依据外部评价模型选出得分最高者；评价信号只负责选择，不参与候选生成。自我改进是指模型在后续轮次重新翻译或修改已有译文，本文采用尽量简化的提示设置来研究这一过程，而不是引入复杂的显式推理链或多智能体反馈。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定源语言句子$x$，目标是生成目标语言译文$y$。模型在相同或可比的采样预算下运行：并行策略独立生成多个候选$y_1,dots,y_N$，再由外部翻译质量模型从候选中选择一个；顺序策略在第$t$轮根据源句子及此前轮次构造的目标侧上下文生成候选$y_t$，并从顺序生成池中选择最终结果。本文假设外部评价模型可用于候选重排序，但不把该评价信号反馈给生成过程；因此比较主要反映生成样本池本身的多样性与有效性，而不是复杂搜索器或反馈控制器的额外能力。研究还考察上下文构造方式和采样温度对顺序策略的影响，并通过人工评价区分流畅性、自然度与准确性等翻译质量维度。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

源语言输入句子。

</div>
<div class="notation-item" markdown="1">

**$y$**

目标语言译文或一个候选输出。

</div>
<div class="notation-item" markdown="1">

**$N$**

候选译文数量，即Best-of-$N$中的采样规模；在本文语境下也对应受控的采样预算大小。

</div>
<div class="notation-item" markdown="1">

**$y_t$**

顺序采样第$t$轮生成的译文候选；其生成可依赖此前轮次提供的目标侧上下文。

</div>

</div>

**直接相关的工作**

- **Wu et al. (2025a)**: 该工作显示，直接提示大语言模型“再次翻译并生成更好的版本”可能优于复杂、类人化的推理流程。本文沿用这种简化的自我改进设定，将其作为研究顺序测试时扩展机制的基础。
- **Fernandes et al. (2022)**: 该工作将并行候选生成后依据质量信号进行选择的机器翻译方法称为Quality-Aware Decoding（QAD）。本文把这一范式具体化为使用外部指标模型进行Best-of-$N$重排序，并与顺序采样进行受控比较。

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

本文把机器翻译中的测试时扩展统一为“在固定推理预算内生成候选，再观察候选池质量”的过程。给定源文本 $x$、语言模型 $p_{\theta}$ 和翻译提示 $I(x)$，并行采样在每一轮都从相同条件分布独立生成译文；顺序采样则采用多轮对话，把此前的改写指令及译文全部放入上下文，再要求模型“Please translate again for a better version.”。在预算为 $N$ 时，两种方法各自产生至多 $N$ 个候选，因此计算轮数可直接比较。随后，实验可以不使用选择器，逐轮评估顺序译文；也可以使用外部、无参考译文的质量度量模型，在候选池中执行 Best-of-$N$ 选择，以估计不同采样策略能够达到的性能上限。

直观地说，并行方法像让 $N$ 名彼此隔离的译者独立翻译同一句话，顺序方法则像让同一名译者看到自己此前的所有版本并持续重写。质量选择器只在全部版本产生后负责挑选，不向生成模型提供反馈，因此本文研究的是上下文依赖的采样方式本身是否能形成更有效的候选池，而不是“度量模型指导生成”带来的收益。该方法不进行参数训练，也不显式生成思维链；额外计算全部发生在推理阶段。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造初始翻译条件

将 $x$ 嵌入提示 $I(x)$，形成模型首次生成译文时的条件。作者不进行提示调优，只明确规定期望的输出格式。

<div class="method-step__io" markdown="1">

**输入**：源文本 $x$、预训练语言模型 $p_{\theta}$，以及包含输出格式要求的翻译提示模板。<br>
**输出**：初始模型输入 $I(x)$。

</div>

**直观理解**：这一步相当于把待翻译句子连同任务说明交给模型。两种采样策略从同一初始请求出发，以避免提示差异干扰比较。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按固定预算生成候选译文

并行策略从 $p_{\theta}(\cdot\mid I(x))$ 独立抽取 $N$ 次；顺序策略先生成首个译文，之后每轮把此前所有指令与译文作为上下文，并使用相同改写指令 $I$ 请求更好的版本。除温度消融外，正文所述采样温度为 $1.0$。

<div class="method-step__io" markdown="1">

**输入**：初始输入 $I(x)$、生成预算 $N$，以及采样温度。<br>
**输出**：并行候选池 $y_p^{1\ldots N}$ 或具有生成顺序和上下文依赖的候选池 $y_s^{1\ldots N}$。

</div>

**直观理解**：并行候选之间互不相见，差异主要来自随机采样；顺序候选能够参考旧版本，因此既可能修正问题，也可能继承或放大旧版本的偏差。相同的 $N$ 表示相同生成轮数，而不是保证完全相同的上下文长度或实际计算量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 选择评估模式

研究设置分为三种：并行采样加选择器、顺序采样不加选择器、顺序采样加选择器。加选择器时，外部无参考质量度量模型仅在生成结束后为候选排序并选择最佳项；不加选择器时，则直接报告顺序采样各轮译文的平均表现。

<div class="method-step__io" markdown="1">

**输入**：候选译文池及对应源文本 $x$。<br>
**输出**：每个预算下被选中的 Best-of-$N$ 译文，或顺序采样中每一轮的译文表现。

</div>

**直观理解**：不加选择器回答“模型是否能靠连续重写自然变好”；加选择器回答“只要有可靠的事后挑选工具，这批候选中最好能有多好”。二者不能混为一谈，因为后者同时依赖候选池覆盖能力与选择器判断能力。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 预算递增与策略比较

在每个预算下比较译文质量与候选多样性，从而考察性能随额外推理轮数的变化，并区分顺序采样的逐轮表现和经过 Best-of-$N$ 选择后的性能上限。所有策略均受固定生成轮数约束，以建立基本公平的预算比较。

<div class="method-step__io" markdown="1">

**输入**：从 $1$ 到 $N$ 的各级采样预算，以及三种解码设置的输出。<br>
**输出**：质量—预算曲线、不同候选池的多样性与潜在最佳性能，以及后续温度和上下文构造消融所需的结果。

</div>

**直观理解**：这里不是只比较某个最终分数，而是观察增加一次生成是否仍带来收益。预算曲线还能揭示收益来自后续译文本身稳定改善，还是来自候选数量增加后更容易挑到偶然的好版本。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 并行独立采样

$$
y^{(i)} \sim p_{\theta}\!\left(\cdot \mid I(x)\right), \qquad i\in\{1,\ldots,t\}
$$

**符号说明**

- $x$：待翻译的源文本。
- $I(x)$：包含源文本及翻译任务要求的初始提示。
- $p_{\theta}$：参数为 $\theta$ 的语言模型所定义的条件生成分布。
- $y^{(i)}$：第 $i$ 次独立采样得到的译文。
- $t$：当前使用的生成次数或采样预算。

<div class="equation-explanation" markdown="1">

**直观理解**：所有译文都从完全相同的提示条件中抽样；前一个译文不会影响后一个译文。因此，增加预算只会增加独立候选数量，不会让模型基于已有译文进行修订。<br>
**原文位置**：第 3.1 节，公式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 顺序上下文依赖采样

$$
y^{(t)} \sim p_{\theta}\!\left(\cdot \mid I^{(t-1)},y^{(t-1)},\ldots,I^{(1)},y^{(1)},I(x)\right)
$$

**符号说明**

- $y^{(t)}$：顺序采样第 $t$ 轮生成的译文。
- $y^{(k)}$：第 $k$ 轮已经生成并保留在对话上下文中的译文，其中 $1\leq k<t$。
- $I^{(k)}$：第 $k$ 次要求模型重新翻译并改进的指令；本文各轮均令其等于同一个提示 $I$。
- $I$：固定改写提示“Please translate again for a better version.”。
- $I(x)$：包含源文本 $x$ 的初始翻译提示。
- $p_{\theta}$：参数固定的语言模型条件生成分布。

<div class="equation-explanation" markdown="1">

**直观理解**：第 $t$ 个版本并非独立重做，而是在完整阅读此前请求和译文后继续生成。该条件依赖正是顺序测试时扩展的核心：新增预算不仅增加样本数，也逐轮扩大可供模型利用的目标语上下文。<br>
**原文位置**：第 3.2 节，公式 (2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文所比较的是推理阶段的采样与候选选择方法，不训练或微调语言模型 $p_{\theta}$，也不通过选择器优化模型参数。外部质量度量只执行生成后的候选排序，其分数既不作为损失函数，也不反馈到后续顺序生成中；因此 Best-of-$N$ 的改进应解释为推理搜索和事后选择的结果，而非学习目标带来的参数更新。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 并行独立采样**

对同一个条件 $I(x)$ 重复执行祖先采样，各候选 $y^{(i)}$ 条件独立，不把其他候选写入上下文。它不同于束搜索：本文保留随机生成路径，并通过采样预算控制候选池大小。

> 直观理解：该模块提供不含自我改写因素的对照组。它检验单纯增加独立尝试次数能否覆盖高质量译文，并帮助判断顺序策略的收益是否超出“多抽几次样本”。

**2. 顺序自我改写**

第 $t$ 轮以 $I(x)$、此前全部译文 $y^{(1)},\ldots,y^{(t-1)}$ 及重复的改写指令为条件生成 $y^{(t)}$。各轮统一采用极简指令“Please translate again for a better version.”，不提供显式错误标签、外部质量分数或思维链步骤。

> 直观理解：这一设计尽量把变量压缩为“模型能否利用自己旧译文及更长的目标语上下文”。由于没有指出哪里翻错，后续提升若出现，更接近模型基于上下文进行自我修订的能力，而不是遵循人工反馈。

**3. 外部无参考质量选择器**

选择器采用外部参考无关的翻译质量度量模型，对同一源句的候选译文进行事后比较，构成 Quality-Aware Decoding 的简单实例，即 Best-of-$N$。度量信号从不进入生成上下文，也不改变 $p_{\theta}$ 的采样分布。

> 直观理解：选择器相当于生成完成后的裁判，而不是写作过程中的教练。这样可用候选池中的最佳译文估计采样策略的潜力，但观察到的最终质量仍可能受裁判排序误差影响。

**训练与推理**

训练阶段没有本文特有的流程，直接使用既有语言模型和既有外部无参考质量度量模型。推理时，首先以 $I(x)$ 请求首次翻译；并行分支在相同提示下独立采样至预算 $N$，顺序分支则在多轮对话中反复附加固定改写指令，并保留此前全部译文作为上下文。对于“Sequential w/o selector”，每一轮的输出直接进入评估，用于观察自我改写轨迹；对于“Parallel w/ selector”和“Sequential w/ selector”，分别从截至当前预算的候选池中由外部度量模型选择最佳译文。预算由 $1$ 逐步增加到 $N$，从而绘制质量随推理轮数变化的曲线。

需要特别区分生成与选择：顺序生成虽然显式要求“更好的版本”，但模型并未得到参考译文、质量分数或具体错误反馈；选择器也不会影响下一轮生成。因而，这套流程控制性地比较了两种探索解码空间的方式：并行采样依赖多个独立随机路径，顺序采样则依赖历史译文形成的条件路径。作者还移除了显式思维链，因为所引前期研究认为一般机器翻译中显式任务分解没有清晰收益。

**复现信息**

公平比较的核心设置是：两类方法对每个源句都采用相同的最大生成轮数预算，并将预算从 $1$ 变化到 $N$；默认采样温度为 $1.0$，温度仅在专门消融中改变。顺序方法每轮使用完全相同的改写指令，并保留从初始提示到当前轮的完整多轮上下文；并行方法每次都只条件于同一个 $I(x)$。提示未经过调优，但明确约束输出格式。

复现和解释时还应注意，按“轮数相同”实现的是生成次数层面的公平，而顺序方法因上下文持续增长，单轮 token 处理量可能高于并行方法；给定节选未报告按总 token 数、延迟或实际计算量重新配平的方案。节选也未给出最大 $N$ 的具体数值、模型解码的其他参数及选择器的确切名称或版本，这些信息被指向附录 B、附录 A.1 和温度消融所在的附录 H.3，不能从当前材料中补造。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- WMT24++测试集：用于主要机器翻译评测。该数据集覆盖多种领域，参考译文由人工撰写并由专业译者后编辑；依据$is_bad_source$字段过滤低质量或无效源句后，每个语言方向保留$960$个片段。实验选择六个方向：$\mathrm{en}\rightarrow\mathrm{zh,de,ru,nl,ro,ar}$，以覆盖不同文字系统和语言族。
- WMT24++文档级映射：用于第$6.2$节的受控实验。作者依据文档元数据构造由两个连续句子组成的$633$个片段，并将前一句作为HEAD、后一句作为TAIL，以检验句子在序列上下文中的位置效应。
- 六个语言方向的分方向评测集：用于检查主要趋势是否跨语言稳定，并用于人工MQM比较和逐语言多样性分析；其中ReMedy-9B-22不支持$\mathrm{en}\rightarrow\mathrm{nl}$，因此该指标只报告五个方向。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**CometKiwi-XL**

WMT24官方参考无关质量评测模型，同时作为主要候选选择器；它在没有参考译文参与选择时估计源句与译文的翻译质量。 （分数越高越好，因为实验将其作为质量选择和主分析中的自动质量信号。）

</div>
<div class="metric-item" markdown="1">

**COMET**

基于参考译文的翻译质量指标，用于在不同于选择器的评价模型上复核结果，以降低指标投机或metric hacking造成的偏差。 （分数越高越好，表示候选译文与源文及参考译文的语义和翻译质量更好。）

</div>
<div class="metric-item" markdown="1">

**MetricX-24-Hybrid-XXL**

同时以参考无关的QE模式和基于参考的ref模式使用的混合质量指标，用于从另一类自动评价模型检验主结论；人工分析另使用MQM的accuracy、fluency和style维度。 （分数方向须按论文所采用的MetricX报告方式解释；表中作者将其与COMET并列用于比较不同策略，而非把不同指标的绝对数值直接互比。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 六个语言方向、Qwen3-32B，预算为$30$的Best-of-$N$比较；序列方法分别使用完整上下文、$h=5$和$h=1$，并与并行采样比较。

<div class="result-value" markdown="1">

序列采样在较小预算下通常优于并行采样，并且序列候选在早期轮次具有更低的重复率、更有效的探索。表1的聚合COMET结果中，完整上下文序列为$83.28$、$h=5$为$83.27$、$h=1$为$83.72$，并行采样为$83.47$；因此受控的小上下文$h=1$在该聚合设置下最高，但完整上下文并不最高。

</div>

这支持“后续生成读取前序译文能够形成更有效候选池”的作者主张，尤其说明优势不只是增加样本数量。它并不证明序列方法在所有预算、语言或评价指标上都必然胜出；完整上下文结果低于$h=1$也表明上下文越长并不等于质量越高。

<div class="result-source" markdown="1">

来源：Section 7, Ablation study；Table 1；Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We observe a similar overall pattern, i.e., sequential achieves better performance under smaller budgets.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3-32B的人工MQM比较，覆盖accuracy、fluency和style；重点比较序列第$2$轮与第$1$轮、预算$30$的序列选择结果与并行选择结果。

<div class="result-value" markdown="1">

从人工分析看，序列自我改进通常提升流畅性、准确性和风格，但在序列与并行的预算$30$比较中，并行往往具有更高准确性；这与自动结果中序列的总体优势并不矛盾，因为序列的主要收益更明显地体现在流畅性和自然性，而大预算可能引入准确性退化。

</div>

该结果揭示了单一自动分数无法表达的质量权衡：序列输出可能更自然、更顺口，却可能在事实、术语或语义对应上发生损失。因此，序列扩展适合被理解为质量维度重新分配，而不是所有维度都同时改善。

<div class="result-source" markdown="1">

来源：Appendix G, Human Evaluation Results；Figure 15；Table 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

When comparing sequential vs parallel under budget 30, we notice that parallel often demonstrates higher accuracy.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 受控文档级实验：Qwen3-32B将WMT24++文档切分为两个连续句子的片段，采用“Translate Again”，比较同一片段中HEAD与TAIL位置的平均表现。

<div class="result-value" markdown="1">

作者报告第$2$步能够恢复HEAD位置的表现；该设计支持这样的机制解释：序列自我改进的收益部分来自模型获得了更大的目标侧上下文，而不仅仅来自重复采样。实验还通过丢弃$T_1$和$T_5$避免同一句子同时出现在不可比的位置。

</div>

通俗地说，模型看到前面已经生成的目标语言内容后，可能更容易保持连贯和自然；位置对照试图把“句子本身难度”与“它在上下文中的位置”分开。不过该实验只提供部分归因，不能单独证明目标侧上下文是唯一原因。

<div class="result-source" markdown="1">

来源：Section 6, Analysis；Figure 4；Appendix D

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

It is clear that Step-2 recovers performance for the HEAD position.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 人工MQM评测并未完全覆盖所有比较：原文说明$\mathrm{en}\rightarrow\mathrm{de}$由于时间限制只部分完成，因此人工结论的跨语言稳健性有限；同时，MQM表格主要报告计数和相对改进，不能替代完整的统计显著性分析。
- 实验主要依赖WMT24++测试集、三个模型和若干自动质量模型；作者未在所给章节中报告更广泛领域、更多模型或独立人工参考的验证。因此，序列采样的优势、上下文窗口的最优性及低温度下的稳定性仍可能受模型、语言方向、选择器和提示设计影响。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Parallel sampling：对同一输入独立生成候选译文，再用选择器进行Best-of-$N$重排序；它是最直接的非依赖式测试时扩展对照，用来判断序列依赖是否提供额外收益。
- Sequential sampling without selector：采用“Translate Again”策略，后续轮次读取此前译文并继续生成，但直接考察第$1$、$2$、$3$轮输出；该设置测试自我改写本身，而非候选重排序的作用。
- Sequential sampling with selector：每一轮生成的新译文与既有候选共同进入选择器，最终选出Best-of-$N$结果；该设置与并行Best-of-$N$在选择机制和预算上尽量对齐。
- 不同模型规模与来源：Qwen3-32B、Qwen3-4B-Instruct-2507和商业模型GPT-4o-mini用于检验方法是否依赖特定模型规模或模型家族。

**实验想回答的问题**

- 在机器翻译的测试时扩展中，依赖前序输出的序列采样是否比独立并行采样更有效，尤其是在翻译轮数或采样预算较小时？
- 序列扩展带来的收益究竟来自更大的目标侧上下文，还是仅来自更多候选样本；其对准确性、流畅性、多样性以及采样温度和上下文长度的敏感性如何？

**实验实现**

实验默认使用温度$1.0$、top-$k=20$和top-$p=0.8$；每轮最多生成$4096$个token，完整上下文实验为避免长度溢出将上限设为$764$个token。预算表示翻译轮数；主要结果使用Best-of-$N$或序列自我改进策略的最后输出。默认选择器为CometKiwi-XL，另以MetricX-24的QE模式进行选择器替换实验。序列采样的上下文受滑动窗口大小$h$控制：每轮保留初始译文以及最近的若干译文，形式为$y_h^{(t)}\sim p_\theta(\cdot\mid I,y^{(t-1)},\ldots,y^{(t-h)},I,y^{(1)},I(x))$，其中$I(x)$表示输入指令和源句，$y^{(t)}$表示第$t$轮译文，$p_\theta$表示模型生成分布。人工评测采用MQM框架，比较序列第$1$轮与第$2$轮、序列选择结果与第$1$轮，以及预算为$30$时序列选择结果与并行选择结果。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 上下文长度消融：在序列采样中比较完整上下文、$h=5$、$h=2$和$h=1$的滑动窗口；同时考察无选择器的“Translate Again”和带选择器的序列Best-of-$N$。 | 受限上下文通常优于完整上下文；在表1的Qwen3-32B聚合COMET结果中，序列无选择器的第$3$轮为$82.13$，完整上下文Best-of-$N$为$83.28$，$h=5$为$83.27$，$h=1$为$83.72$，并行为$83.47$。作者还指出较小$h$带来更少的COMET退化，并将其归因于较少的重复偏置。 | 该消融隔离了“序列依赖是否需要保留全部历史”的问题。结果说明历史并非越多越好：保留少量近期译文可以减少模型反复追随同一模式，同时降低上下文成本；但这只在所报告模型、数据和选择器设置下成立，不能推出固定的最优窗口大小。 | Section 7, Ablation study；Table 1；Figure 6；Figures 18–19<br><span class="experiment-evidence">Table 1 results show that perhaps counterintuitively, larger context sizes do not imply better performance.</span> |
| 采样温度消融：比较序列与并行Best-of-$N$在不同温度下的质量和多样性，特别考察接近贪心解码的低温度情形。 | 并行采样在温度降低到接近贪心解码时预期会失去多样性并发生坍缩，而序列采样即使在极低温度下仍可能保持Best-of-$N$收益。对于并行Best-of-$N$，温度$1.0$在$\mathrm{en}\rightarrow\mathrm{de}$上接近最优；无选择器的“Translate Again”则可能受益于更低温度。 | 该实验测试序列方法是否必须依赖随机性来产生不同答案。结果暗示序列中的“改变上下文后再生成”本身可以制造有效变化，因此即使单轮采样很确定，仍可能继续改进；但温度最优性会随是否使用选择器和任务设置而改变。 | Section 7, Ablation study；Figure 6；Appendix H.3；Figure 21<br><span class="experiment-evidence">Figure 6 (right) confirms this hypothesis, showing the results for sequential with selector comparing greedy sampling vs high-temperature sampling.</span> |

**定性案例**

- 文档级HEAD/TAIL受控实验是最具解释性的定性案例：两个连续句子被放入同一翻译片段，比较其在序列第$1$步和第$2$步的表现；作者观察到“Step-2 recovers performance for the HEAD position”，说明前序目标侧内容可能帮助模型恢复或改善较早位置的翻译质量。该案例支持上下文机制的部分解释，但没有证明所有语言方向和所有错误类型都遵循相同因果机制。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：研究聚焦 LLM 机器翻译中的顺序与并行测试时扩展，并分析顺序自我改进的作用机制。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`b08a0471477fd1d02e2cb14e8453400b9cb99ec9c61e16be65a6e977e4b00881`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
