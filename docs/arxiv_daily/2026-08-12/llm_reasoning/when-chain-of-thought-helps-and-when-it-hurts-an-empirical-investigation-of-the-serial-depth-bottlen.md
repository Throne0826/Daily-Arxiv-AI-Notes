---
title: "[论文解读] When Chain-of-Thought Helps and When It Hurts: An Empirical Investigation of the Serial-Depth Bottleneck in LLM Reasoning"
description: "[arXiv 2608.09942][LLM Reasoning] 本文检验链式思维（CoT）的作用是否取决于任务所需的串行计算深度，并将其解释为：当任务超出 Transformer 单次前向传播的计算容量时，CoT 通过把中间步骤写入输出序列来绕过带宽瓶颈，而不是普遍增强推理能力。"
arxiv_id: "2608.09942"
announcement_date: "2026-08-12"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-12T03:04:45.487972+00:00"
source_sha256: "cde9ae2b556728bf6b9393332ef055aa83d9f089afeca855fca0c624ecf168a9"
tags:
  - "LLM Reasoning"
  - "链式思维提示"
  - "串行深度瓶颈"
  - "Transformer 单次前向传播"
  - "带宽界"
  - "计算复杂度类别"
  - "外化中间计算"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.09942</p>

# When Chain-of-Thought Helps and When It Hurts: An Empirical Investigation of the Serial-Depth Bottleneck in LLM Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-12</span>
<span><strong>作者</strong> Tughanbulut Kurtulush</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Faculty of Computer Engineering；Vistula University, Warsaw, Poland</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.09942v1) · [PDF 下载](https://arxiv.org/pdf/2608.09942v1) · **关键词** 链式思维提示, 串行深度瓶颈, Transformer 单次前向传播, 带宽界, 计算复杂度类别, 外化中间计算<br>
**代码**: [https://osf.io/hteuj](https://osf.io/hteuj) · **项目页**: [https://osf.io/92jdk](https://osf.io/92jdk)

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

本文检验链式思维（CoT）的作用是否取决于任务所需的串行计算深度，并将其解释为：当任务超出 Transformer 单次前向传播的计算容量时，CoT 通过把中间步骤写入输出序列来绕过带宽瓶颈，而不是普遍增强推理能力。

**不用术语来说**：面对同一道题，大语言模型既可以直接给答案，也可以先写出若干中间步骤再作答。以往常把后一种方式视为普遍更好的推理策略，但实际效果因任务和模型而异。本文要解决的问题是：能否根据一项任务必须依次完成多少步计算，预先判断写出中间过程何时有帮助、何时只是多余，甚至可能造成干扰。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 把 Chen 等人提出的 $H_{dp}$ 带宽界从渐近理论转化为可在实际上下文长度下检验的定性假设：将五个常用基准映射到不同计算复杂度与串行深度类别，并比较直接回答与 CoT 条件下的表现。
- 提出并检验“串行深度决定 CoT 收益”的经验解释：高深度任务应因外部化中间计算而获得较大恢复收益，浅层任务应对 CoT 基本不敏感，中间复杂度任务的收益则可能随模型容量变化。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究链式思维提示（chain-of-thought，CoT）为何只在部分任务上有效。核心背景是：解码器式 Transformer 在一次前向传播中完成的串行计算深度可能受限，而 CoT 通过逐步生成中间结果，把内部难以一次完成的计算外化到输出序列，使后续生成步骤可以读取并继续计算。论文借用 Chen 等人提出的 $H_{\!dp}$ 带宽界作为概念框架，但明确指出该定理只在极端长序列的渐近条件下给出失败保证，不能直接预测现实长度上的模型表现；因此，本文真正考察的是一个经验问题：在常用基准的实际上下文长度下，任务所需串行深度是否能够解释直接作答与 CoT 作答之间的准确率差异。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**串行计算深度**

指求解过程中必须按依赖顺序完成的计算步数；若第 $i$ 步必须使用第 $i-1$ 步的结果，就不能把所有步骤完全并行化。论文把这种依赖链的长短视为决定 CoT 是否有用的关键任务属性。

</div>
<div class="concept-item" markdown="1">

**链式思维提示（CoT）**

要求模型先生成中间推理步骤，再给出最终答案；相对地，no-CoT 条件要求模型直接输出答案。这里 CoT 被解释为“带宽绕行机制”：生成出的中间结果可被后续步骤重新读入，从而把一次前向传播难以容纳的串行计算分摊到多个生成时刻。

</div>
<div class="concept-item" markdown="1">

**计算复杂度深度类别**

论文用 $\mathrm{TC}^0$、$\mathbf{L}$ 和 P-complete 对基准所需的串行深度作粗粒度排序：$\mathrm{TC}^0$ 代表可由常数深度电路完成的浅层计算，$\mathbf{L}$ 表示可在对数空间内计算的中等串行任务，P-complete 则通常包含难以并行化的长依赖链。这是启发式基准映射，不表示每道题都严格属于同一种计算原语。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是三个指令微调模型 Qwen-2.5-7B、Qwen-2.5-32B 和 Llama-3.1-8B，以及五个标准基准：GSM8K、MATH、MMLU、ARC-Challenge 和 HumanEval。对每个基准，作者先依据主要计算依赖将其启发式映射到深度类别：GSM8K 与 MATH 归为高串行深度的 P-complete，MMLU 与 ARC-Challenge 归为浅层的 $\mathrm{TC}^0$，HumanEval 归为中间类别 $\mathbf{L}$；真正承载假设的是深度类别，而非不稳定的具体原语标签。随后在相同题目上比较直接作答（no-CoT）与显式逐步推理（CoT）的准确率，并检验题目级串行深度升高时，单次作答表现是否下降而 CoT 表现是否较稳定。该设定只把渐近的 $H_{\!dp}$ 定理当作机制启发：形式失败条件为 $H_{\!dp}\leq n^{2^{-4L}}$，其对应阈值 $n^{\star}=H_{\!dp}^{2^{4L}}$ 远超现实上下文长度，因而实验不能被视为对该下界的直接验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$H_{\!dp}=H\times d\times p$**

单次前向传播的概念性带宽参数；$H$ 为每层注意力头数，$d$ 为每个头的维度，$p$ 为数值精度的比特数。

</div>
<div class="notation-item" markdown="1">

**$L$**

解码器式 Transformer 的层数；在所引用定理中，也与待解决的顺序函数复合深度相关。

</div>
<div class="notation-item" markdown="1">

**$n$**

输入提示的序列长度。

</div>
<div class="notation-item" markdown="1">

**$n^{\star}=H_{\!dp}^{\,2^{4L}}$**

使理论失败条件开始非空的最小提示长度；本文用它说明形式下界只在天文尺度的序列长度上生效。

</div>

</div>

**直接相关的工作**

- **Chen, Peng & Wu (2024)**: 提出多方自回归通信模型及 $H_{\!dp}$ 无条件下界，说明当串行函数复合超出单次前向传播的通信能力时，显式输出中间步骤可带来理论优势。本文不把该渐近定理当作现实长度上的定量预测，而以其识别出的串行深度瓶颈来构造可检验的基准级假设。
- **Nye et al. (2022)**: 指出模型在一次前向传播中无法按任务难度自适应增加计算量，并发现显式草稿区能恢复多步算术任务的准确率。该工作提供了与本文机制一致的早期经验证据：外化中间状态可能缓解顺序计算瓶颈。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

实际部署和评测中，CoT 会增加输出长度、推理延迟与计算成本，因此不能只问它平均是否有效，还需要知道哪些任务值得承担这些成本。现有经验显示 CoT 在数学和符号推理上往往有效，在非符号任务上收益有限，但这种任务差异仍缺少一个能够联系模型架构与任务计算需求的统一解释。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **将 CoT 视为通用推理增强手段的提示方法**：要求模型在最终答案前生成自然语言或符号化中间步骤，希望通过逐步分解问题提高正确率；这种做法通常根据总体准确率判断效果，却不明确区分任务本身需要的串行计算深度。
- **$H_{dp}$ 带宽界与多方自回归通信模型**：Chen 等人用 $H_{dp}=H\times d\times p$ 表示注意力头数 $H$、头维度 $d$ 与数值精度 $p$ 共同决定的单次传播带宽，并证明在特定渐近条件下，有限层 Transformer 无法在一次前向传播中完成足够深的顺序函数复合；若把中间结果写入输出流，后续生成步骤便可继续利用这些结果。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 把 CoT 当作普遍有效的经验技巧，无法解释它为何主要帮助数学和符号任务，也无法在运行模型前判断新增推理步骤是必要计算还是冗余输出，因而不足以指导成本敏感的提示策略。
- $H_{dp}$ 理论界只在极端渐近尺度上给出严格保证。其非平凡阈值为 $n^{\star}=H_{dp}^{2^{4L}}$，对本文涉及的模型远超任何物理可实现的序列长度，因此该定理本身不能直接说明几百到几千 token 的现实基准是否也受同一瓶颈支配。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

理论已经证明外部化中间步骤可在渐近意义上突破单次前向传播的串行计算限制，经验研究也观察到 CoT 的收益具有明显任务差异，但两者之间缺少现实尺度的证据：尚不清楚标准 NLP 基准中的样本级串行深度是否真的对应直接回答性能下降，以及 CoT 是否会专门恢复这部分由深度造成的损失。

</div>
<div markdown="1"><span>核心问题</span>

在实际上下文长度和常用指令微调模型上，任务及样本所需的串行计算深度能否预测直接回答与 CoT 之间的准确率差异，并进一步区分 CoT 何时有显著帮助、何时基本冗余以及何时可能有害？

</div>
<div markdown="1"><span>作者直觉</span>

一次前向传播可类比为容量有限的内部工作区：若答案只依赖浅层匹配或少量可并行计算，模型可直接完成，额外生成步骤不会解锁新的能力；若问题必须按顺序执行许多相互依赖的操作，早期结果需要保留并供后续步骤使用，单次传播便更容易受限。CoT 把这些中间结果写到上下文中，使后续 token 能读取并继续计算，因此其主要作用应是“绕过串行带宽瓶颈”，而非无条件提升所有任务的推理质量。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文的方法不是提出新的模型结构或训练算法，而是把 $H_{dp}$ 带宽界转化为一套可检验的经验研究框架：先用该理论界识别解码器式 Transformer 的“串行深度瓶颈”，再按任务所需的计算深度把五个基准粗略映射到 $\mathrm{TC}^0$、$\mathbf{L}$ 和 P-complete 三类，进而预测链式思维（CoT）相对直接作答的收益。经验比较的核心因变量是同一模型、同一基准在 CoT 与 no-CoT 条件下的性能差异；理论预期是，高串行深度任务更依赖把中间结果写入输出序列，低深度任务则可在一次前向计算中完成，因此 CoT 应主要恢复前者的性能。

技术上，$H_{dp}=H\times d\times p$ 表示每层注意力计算可用的近似信息带宽，其中 $H$ 是注意力头数、$d$ 是每个头的维度、$p$ 是数值精度位数。Chen 等人的定理只在极端大的输入长度下给出必然失败条件，远不覆盖本文数百至数千 token 的实验范围；因此作者明确把它作为机制性动机，而不是用它直接预测准确率。通俗地说，一次前向传播像一张计算深度固定的工作台：简单问题可以一次做完，依赖前一步结果的长计算链可能装不下；CoT 将中间步骤写出来，相当于保存阶段性结果并重新利用模型，从而绕过单次计算的深度限制。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立串行深度瓶颈假设

计算概念性带宽参数 $H_{dp}=H\times d\times p$，并依据 Chen 等人的结果，将单次前向传播处理长串行函数复合的能力视为受限。作者不把渐近失败阈值外推到实际上下文长度，只据此提出：所需串行深度越高，直接作答越容易受损。

<div class="method-step__io" markdown="1">

**输入**：一个具有 $L$ 层、每层 $H$ 个注意力头、头维度为 $d$、数值精度为 $p$ 位的解码器式 Transformer，以及需要若干依赖步骤的任务。<br>
**输出**：关于 no-CoT 与 CoT 差异的机制假设：no-CoT 性能应随题目串行深度上升而下降，而 CoT 通过外显中间计算缓解这种下降。

</div>

**直观理解**：模型直接输出答案时，所有相互依赖的步骤都必须挤在一次固定深度的计算中；写出中间步骤后，先前结果会进入后续 token 的上下文，使模型可以分多轮继续计算。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 将基准映射到计算深度类别

作者先为每个基准指定启发式计算原语，再以更粗粒度的深度类别作为假设的主要依据：GSM8K 与 MATH 映射为需要连续复合的 P-complete 类，MMLU 与 ARC-C 映射为常数深度的 $\mathrm{TC}^0$ 类，HumanEval 映射为介于两者之间的 $\mathbf{L}$ 类。具体原语标签并不稳定，因此真正承载假设的是深度类别，而不是某个题目是否严格属于单一原语。

<div class="method-step__io" markdown="1">

**输入**：五个标准基准：GSM8K、MATH、MMLU、ARC-C 和 HumanEval，以及 Chen 等人提出的 CC primitive 分类框架。<br>
**输出**：三档任务深度及对应的预注册方向性预测：P-complete 任务预期明显受益于 CoT，$\mathrm{TC}^0$ 任务预期收益为零或很小，$\mathbf{L}$ 任务预期呈中等且可能依赖模型规模的收益。

</div>

**直观理解**：这一步不是声称整个基准都具有严格相同的复杂度，而是按典型题目需要多少连续依赖步骤进行分组，用分组结果预先规定应当观察到什么模式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造 CoT 与 no-CoT 对照

在模型与任务保持一致的前提下改变是否外显中间计算，并比较两种条件的任务表现。该设计把 CoT 视为一种推理时的外部暂存机制，而不是额外训练得到的新能力。

<div class="method-step__io" markdown="1">

**输入**：同一批基准题目、同一指令微调模型，以及两种回答方式：直接生成最终答案的 no-CoT 条件与外显中间推理步骤的 CoT 条件。<br>
**输出**：每个模型与基准组合上的 CoT 效应，以及可供跨深度类别比较的性能恢复模式。

</div>

**直观理解**：类似让同一名学生回答同一道题：一种方式只允许直接写答案，另一种允许写草稿；两者差异用于判断草稿是否主要帮助多步计算。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 检验深度梯度与标签稳健性

研究关注 no-CoT 表现是否随单题串行深度单调下降、CoT 表现是否对深度近似不敏感，并检查 CoT 恢复幅度是否随基准深度类别提高。作者还使用 LLM-as-judge 进行原语标签的一致性检查，但将该检查用于揭示细粒度标签噪声，而不把低一致性标签作为核心因果证据。

<div class="method-step__io" markdown="1">

**输入**：各题或各基准的深度分类、CoT/no-CoT 对照结果，以及对题目计算原语的额外判定。<br>
**输出**：对“CoT 是串行带宽旁路而非普遍推理增强器”这一机制解释的经验支持或反证，以及对启发式基准映射可信边界的说明。

</div>

**直观理解**：关键不只是比较哪个基准分数高，而是看题目越需要连续步骤时，直接作答是否越容易失败、允许写中间步骤后这种斜率是否明显变平。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### $H_{dp}$ 带宽参数

$$
H_{\!dp}=H\times d\times p
$$

**符号说明**

- $H_{\!dp}$：作者采用的 Transformer 单层注意力带宽参数。
- $H$：每层的注意力头数量。
- $d$：每个注意力头的表示维度。
- $p$：数值表示的精度位数；原文以 FP16 的 $16$ 位为例。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把并行注意力头、每个头可承载的维度和每个数值的位宽合并为一个概念性通道容量。它用于说明单次前向传播可传递的信息资源有限，但不能单独预测实际基准上的准确率。<br>
**原文位置**：第 2.1 节“The $H_{dp}$ Bound”

</div>

</div>

<div class="equation-block" markdown="1">

#### 渐近失败条件与非空阈值

$$
H_{\!dp}\leq n^{2^{-4L}},\qquad n^{\star}=H_{\!dp}^{\,2^{4L}}
$$

**符号说明**

- $H_{\!dp}$：由注意力头数、头维度和数值精度共同决定的带宽参数。
- $n$：输入提示的长度。
- $L$：解码器式 Transformer 的层数，同时出现在所讨论的 $L$ 重顺序函数复合设定中。
- $n^{\star}$：使失败保证开始成为非空陈述的最小提示长度，由等式 $n^{2^{-4L}}=H_{dp}$ 反解得到。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分给出 Chen 等人的渐近结论：当带宽相对于输入长度和所需串行深度过小时，单次前向模型无法完成相应的顺序函数复合。第二部分把条件反解为长度阈值；由于指数中又包含随层数增长的指数，该阈值远超任何现实上下文，因此本文只采用其揭示的架构机制，不声称实验落在定理保证范围内。<br>
**原文位置**：第 2.1 节“The $H_{dp}$ Bound”，图 1 及其后推导

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。所给章节没有提出参数训练、微调损失或新的优化目标；研究操纵发生在推理提示与输出形式层面，目标是比较 CoT 和 no-CoT 条件，而不是通过梯度下降优化一个新模型。$H_{dp}$ 公式和渐近失败条件属于理论分析工具，也不是训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. $H_{dp}$ 概念性带宽模块**

以注意力头数 $H$、头维度 $d$ 和精度 $p$ 的乘积表示单层信息通道规模，并结合 $L$ 层串行函数复合的渐近失败条件解释单次前向传播的深度限制。该模块仅产生机制假设，不用于计算实际题目的准确率阈值。

> 直观理解：它提供的是“为什么多步任务可能需要把中间结果写出来”的理论视角，而不是一个能在实际上下文长度上直接判定模型成败的公式。

**2. 深度类别映射模块**

GSM8K 被视为 $k$ 步顺序复合，MATH 被视为嵌套 $k$ 步复合，二者归入 P-complete；MMLU 与 ARC-C 分别以集合不相交和稀疏奇偶性为启发式原语，归入 $\mathrm{TC}^0$；HumanEval 以指针追踪为初始标签，归入 $\mathbf{L}$。映射是基准层面的粗粒度假设工具，并非对每一道题的形式复杂度证明。

> 直观理解：该模块把不同数据集排成“浅、中、深”三档，使 CoT 的预期效果可以事先确定；它的价值在于形成可证伪预测，而不在于给每道自然语言题贴上绝对正确的复杂度标签。

**3. 中间计算外显模块**

CoT 将当前步骤的结果生成到输出流，使后续 token 的计算能够读取这些结果；相比之下，no-CoT 要求模型在不输出中间状态的情况下直接生成最终答案。作者据此把 CoT 解释为对固定单次前向深度的推理时旁路。

> 直观理解：中间文本相当于可反复读取的草稿纸：它不能保证每一步都正确，但能减少模型必须在一次内部计算中同时维持整条依赖链的压力。

**训练与推理**

训练阶段不适用：本文直接研究已有指令微调模型，没有在所给章节中描述额外训练。推理阶段以基准题目为输入，在 no-CoT 条件下要求模型直接给出最终答案，在 CoT 条件下允许或要求模型生成中间推理步骤后再给出答案；随后按任务评分规则比较两种条件，并依据预先设定的 P-complete、$\mathbf{L}$、$\mathrm{TC}^0$ 深度顺序分析收益。该程序的识别逻辑是：如果 CoT 主要绕过串行深度瓶颈，那么收益应集中在连续依赖较强的任务上，同时 no-CoT 应呈现更明显的单题深度梯度；若所有类别都同等受益，则会削弱本文的机制解释。

**复现信息**

公平解释结果所需的关键限定有三点。第一，理论界是渐近结果：文中估算测试模型的 $n^{\star}$ 约从 $10^{10^{34.4}}$ 到 $10^{10^{77.8}}$，而基准输入约为 $10^2$ 至 $10^3$ token，因此不能把实验表现称为该定理的直接验证。第二，基准到计算原语的映射是启发式的，LLM-as-judge 检查的汇总一致性仅为 $\kappa=0.293$；作者因此将 P-complete、$\mathbf{L}$ 和 $\mathrm{TC}^0$ 的粗粒度深度类别作为核心变量。第三，所给章节没有提供提示模板、解码参数、样本数量、答案抽取规则或执行 HumanEval 测试的具体流程，这些复现信息应从论文实验章节核查，不能由当前摘录补造。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 高串行深度数学任务组：GSM8K 与 MATH。二者在论文中被归为 P-complete 基准，用于检验需要较长顺序推导的题目是否更依赖把中间计算外显为 CoT。每个模型、条件和基准的评测单元包含 $n=800$ 个样本；所用具体数据划分及抽样方法在给定节选中未明确报告。
- 浅层知识与选择题任务组：MMLU 与 ARC-Challenge。论文将其视为浅层 $TC^0$ 任务，用于检验当任务已能装入模型单次前向计算时，CoT 是否仍有稳定收益或反而造成损害。每个评测单元为 $n=800$；具体子集、学科构成和抽样方式在给定节选中未明确报告。
- 程序生成任务：HumanEval，论文将其作为中间复杂性类别 $L$ 的代表，用于检验 CoT 收益是否存在模型规模依赖的转变。实验使用完整划分，共 $n=164$ 道题；给定节选未说明执行沙箱、采样次数或程序判定细节。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率与 CoT 恢复差距 $\Delta$**

准确率衡量最终答案正确的样本比例；$\Delta$ 是同一模型、同一基准上 CoT 准确率减去 no-CoT 准确率，以百分点表示。正值代表 CoT 恢复了更多正确答案，负值代表显式推理条件表现更差。 （准确率越高越好；若目标是衡量 CoT 的增益，则 $\Delta$ 越大表示增益越强，但它不等同于模型绝对能力，也可能受到答案提取、输出长度和基准污染影响。）

</div>
<div class="metric-item" markdown="1">

**95% Wilson 置信区间**

为二项准确率提供不确定性区间；Wilson 区间比简单正态近似更适合有限样本比例。论文在表 3 中为每个准确率报告该区间。 （没有单纯的越高或越低越好；区间越窄表示准确率估计越精确，但宽度还受样本量和真实正确率影响。）

</div>
<div class="metric-item" markdown="1">

**McNemar 精确检验**

利用同一批样本在 no-CoT 与 CoT 下的配对正确/错误变化，检验两种条件的准确率是否确有差异。论文对 $5\times3=15$ 个“基准$\times$模型”单元进行检验，并采用 Bonferroni 校正阈值 $\alpha=0.05/15=0.0033$。 （校正后的 $p$ 值越小，反对“两个条件无差异”的证据越强；显著性只说明差异不易由随机波动解释，不说明差异足够大、具有实际价值或由串行深度唯一导致。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 高串行深度的 GSM8K 与 MATH，跨三个模型比较 no-CoT 和 CoT

<div class="result-value" markdown="1">

作者报告两个 P-complete 数学基准在全部三个模型上均有巨大正向恢复：单模型差值范围约为 $+53.9$ 至 $+68.0$ 个百分点；跨模型平均差值分别为 GSM8K 的 $+60.6$ 和 MATH 的 $+60.5$ 个百分点。

</div>

这说明显式写出中间步骤与高深度数学题的显著性能恢复稳定相关，符合“CoT 将单次前向过程容纳不下的串行计算外显化”的解释。它仍不能单独证明 $H_{dp}$ 界限是因果机制，因为 CoT 同时改变了输出长度、提示形式和可用计算量，而且基准标签 P-complete 不等于逐题测得的串行深度。

<div class="result-source" markdown="1">

来源：第 4.1 节 Main Effect，表 3 前的结果总结

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The mean CoT recovery gap across models is +60.6 pp for GSM8K, +60.5 pp for MATH, +3.2 pp for MMLU, +1.4 pp for ARC, and +1.2 pp for HumanEval (averaging −28.7, +9.1, and +23.2 across the three models).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 浅层 MMLU 与 ARC-Challenge，跨三个模型比较 no-CoT 和 CoT

<div class="result-value" markdown="1">

六个“模型$\times$基准”单元的 CoT 差值均落在 $[0.0,+4.6]$ 个百分点内；跨模型平均增益为 MMLU 的 $+3.2$ 和 ARC 的 $+1.4$ 个百分点。作者据此认为原先更强的“CoT 会伤害浅层任务”假设未成立，观察到的是近似中性或小幅正收益。

</div>

结果支持“浅任务中 CoT 结构上可能冗余”，但没有证明 CoT 对浅层计算永远无用。尤其 ARC 的 no-CoT 准确率最高达到 $94.5%$，存在天花板效应；论文摘要还警告高基线可能受训练数据污染影响，因此该零效应不是干净的架构检验。

<div class="result-source" markdown="1">

来源：第 4.1 节 Main Effect；具体准确率见表 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The stronger negative TC0 hypothesis does not hold: with correctly extracted answers, CoT is approximately neutral on MMLU and ARC-Challenge across all six (model, benchmark) cells (Δ∈[0.0,+4.6] pp).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 中间复杂性任务 HumanEval，在 Qwen-7B、Llama-8B 与 Qwen-32B 上比较 no-CoT 和 CoT

<div class="result-value" markdown="1">

HumanEval 呈明显模型依赖：Qwen-7B 从 $74.4%$ 降至 $45.7%$，差值 $-28.7$ 个百分点；Llama-8B 从 $51.8%$ 升至 $61.0%$，差值 $+9.1$；Qwen-32B 从 $62.2%$ 升至 $85.4%$，差值 $+23.2$。

</div>

这表明中间类别不能用“CoT 总是有益”或“总是冗余”概括：效果会随模型而改变。由于 7B 与 8B 结果方向不同，差异不能仅凭参数规模解释，还可能涉及模型家族、指令微调、代码能力、答案格式或生成预算；实验展示的是转变现象，而非隔离后的规模因果效应。

<div class="result-source" markdown="1">

来源：表 3，HumanEval 的三个完整模型行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen-7B | HumanEval | 74.4 [67.2,80.5] | 45.7 [38.3,53.4] | −28.7; Llama-8B | HumanEval | 51.8 [44.2,59.3] | 61.0 [53.3,68.1] | +9.1; Qwen-32B | HumanEval | 62.2 [54.6,69.3] | 85.4 [79.1,90.0] | +23.2

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 浅层任务的 no-CoT 基线很高，尤其 ARC-Challenge 可达 $94.5%$，可能出现天花板效应；论文摘要也明确提示潜在基准污染。因此 MMLU/ARC 上接近零的 CoT 增益不能被视为纯粹、无混杂的架构证据。
- 实验用基准级复杂性类别代理逐样本串行深度，而给定节选没有报告逐题深度测量、提示长度控制或等计算量控制。CoT 条件通常允许更多生成 token 和顺序计算，所以观察到的恢复既符合串行深度解释，也可能部分来自更大的测试时计算预算；此外，三种模型的架构、模型家族和训练数据并未被独立控制。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- no-CoT 直接作答条件：系统提示要求模型直接给出答案，并设置较短输出上限。它是核心对照，因为它尽量测量模型在不借助外显中间步骤时的单次前向计算能力；但给定节选省略了完整提示词和精确输出上限。
- CoT 条件：允许或要求模型生成显式中间推理，再提取最终答案。它是被检验的方法条件，用于判断外显推理是否能绕过单次计算的串行深度瓶颈；给定节选未提供完整提示模板、解码参数和输出长度上限。
- 模型规模对照：Qwen-2.5-7B-Instruct、Llama-3.1-8B-Instruct 与 Qwen-2.5-32B-Instruct。三者均为无内部推理阶段的指令微调 decoder-only Transformer，论文报告其 $H_{dp}$ 分别为 $57{,}344$、$65{,}536$ 和 $81{,}920$，借此观察不同单次前向带宽下 CoT 效果是否改变。
- 任务复杂性对照：将 GSM8K/MATH、MMLU/ARC-Challenge、HumanEval 分别视为 P-complete、$TC^0$ 和 $L$ 类任务。该对照不是另一种算法，而是实验的结构化分组，用于检验收益是否沿任务所需串行深度变化；复杂性类别描述的是任务原型，不能自动证明每个自然语言样本都具有对应的形式复杂度。

**实验想回答的问题**

- 思维链提示是否主要帮助单次前向计算难以容纳的高串行深度任务，并在较浅任务上变得冗余？实验以 no-CoT 与 CoT 的准确率差 $\Delta=\mathrm{Acc}_{\mathrm{CoT}}-\mathrm{Acc}_{\mathrm{no\text{-}CoT}}$ 作为“恢复差距”，比较不同复杂性类别的基准。
- CoT 效果是否随模型规模和任务类型而变化，尤其是中间复杂性类别 HumanEval 是否出现由负收益到正收益的模型依赖转变？

**实验实现**

实验覆盖三种指令微调 decoder-only Transformer：Qwen-2.5-7B-Instruct、Llama-3.1-8B-Instruct 和 Qwen-2.5-32B-Instruct。每个模型分别在 no-CoT 与 CoT 条件下评测五个基准，并对最终答案进行提取后计算准确率；GSM8K、MATH、MMLU 和 ARC-Challenge 每个单元使用 $n=800$，HumanEval 使用完整的 $n=164$。论文以 95% Wilson 区间表达准确率不确定性，并对 15 个配对单元执行 McNemar 精确检验、使用 Bonferroni 校正。给定节选未完整提供提示模板、解码策略、随机种子、硬件、输出上限数值和答案提取规则，因此无法据此独立复现实验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper empirically studies when chain-of-thought improves LLM reasoning as a function of task serial depth.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`cde9ae2b556728bf6b9393332ef055aa83d9f089afeca855fca0c624ecf168a9`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
