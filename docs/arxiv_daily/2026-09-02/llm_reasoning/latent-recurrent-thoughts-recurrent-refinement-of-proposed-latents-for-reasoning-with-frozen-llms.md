---
title: "[论文解读] Latent Recurrent Thoughts: Recurrent Refinement of Proposed Latents for Reasoning with Frozen LLMs"
description: "[arXiv 2609.01117][LLM Reasoning] 本文研究如何在不更新大型语言模型参数、也不依赖思维链轨迹的条件下，用一个面向任务的提议器和一个小型循环推理器反复修正连续潜变量，从而为冻结的语言模型提供可解码的中间计算结果。"
arxiv_id: "2609.01117"
announcement_date: "2026-09-02"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:40:10.516612+00:00"
source_sha256: "75e1d84a9ef647967618baaec1f6459efd188a0f46408d34cd90a6fb620c17c6"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "连续空间推理"
  - "冻结大语言模型"
  - "潜在思考"
  - "递归细化"
  - "软词元"
  - "答案监督"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.01117</p>

# Latent Recurrent Thoughts: Recurrent Refinement of Proposed Latents for Reasoning with Frozen LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Zhaoliang Chen, Jie Fu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Emory University；Affiliation: IQuest Research</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.01117v1) · [PDF 下载](https://arxiv.org/pdf/2609.01117v1) · **关键词** 连续空间推理, 冻结大语言模型, 潜在思考, 递归细化, 软词元, 答案监督<br>
**代码**: [https://github.com/czl-david/latent-recurrent-thoughts](https://github.com/czl-david/latent-recurrent-thoughts)

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

本文研究如何在不更新大型语言模型参数、也不依赖思维链轨迹的条件下，用一个面向任务的提议器和一个小型循环推理器反复修正连续潜变量，从而为冻结的语言模型提供可解码的中间计算结果。

**不用术语来说**：常见的思维链要求模型把每一步推理都写成文字，一旦早期文字出错，后续生成便容易沿着错误继续，而且训练往往需要可供模仿的完整推理过程。另一种选择是在模型内部用向量表示“尚未说出口的想法”，最后只输出答案；真正困难的是，怎样以较低成本生成并逐步改进这些向量，使其承载多步搜索或约束传播，而不是成为对解题无帮助甚至有误导作用的额外输入。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将冻结的预训练语言模型与小型循环推理器结合：面向任务的提议器先根据问题生成基础潜变量，循环推理器再通过多轮、有界的残差修正进行迭代计算，最后由冻结语言模型解码答案；这一设计把计算深度与辅助模块的参数规模解耦。
- 作者明确划定并检验了冻结解码器潜变量推理中的两个关键设计变量——潜变量由通用模型还是任务专用模型提出，以及潜变量是一次生成还是经循环过程反复细化——由此针对既有方法在符号任务上容易失效的问题提出受控替代方案。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型的连续空间推理。常见的思维链（CoT）让模型把中间步骤逐词写成文本，但每一步都受离散词表约束，前序错误会随自回归生成传播，而且训练或模仿高质量推理通常需要显式推理轨迹。连续空间推理则用稠密向量表示中间“思考”，并将其作为软词元送入语言模型。本文聚焦更受限但实用的冻结解码器设定：不更新预训练大语言模型，只训练小型外接模块生成和迭代修正潜变量，从而降低微调成本及灾难性遗忘风险。该设定的核心问题不是解码器如何输出答案，而是怎样在缺少推理轨迹、主模型参数固定的条件下，计算出真正包含多步推理结果的潜变量。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**思维链（Chain-of-Thought, CoT）**

模型先生成自然语言形式的中间推理步骤，再生成最终答案。由于步骤被离散文本固定下来，错误可能逐步累积，而且监督训练往往依赖已有推理轨迹。

</div>
<div class="concept-item" markdown="1">

**连续空间推理与软词元**

中间状态不是词表中的文字，而是与模型输入嵌入兼容的连续向量；这些向量作为软词元加入提示序列。它允许模型接收难以直接语言化的信息，但向量是否有用取决于其生成与更新机制。

</div>
<div class="concept-item" markdown="1">

**潜变量递归细化**

同一个小型状态转移网络被重复应用于持续保存的潜在状态，使计算深度能够随迭代次数增加，而参数量不随之增长。与沿固定标量能量梯度调整不同，向量值转移可以学习约束传播、搜索和纠错等多维更新。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是任务实例或问题$x$，输出是冻结语言模型$\mathcal{M}$解码得到的预测答案$\hat{y}$。系统先由按任务族训练的提议器$g_{\psi}$把$x$映射为$K$个基础潜变量$L^{(0)}$，再由递归细化器$r_{\phi}$进行多轮计算并产生有界残差$\Delta$，形成$L^{\star}=L^{(0)}+\Delta$；随后将$L^{\star}$作为软词元插入指令与问题$[I;x]$之后，由$\mathcal{M}$生成答案。训练只有答案监督而不要求推理轨迹，梯度可穿过冻结模型的激活传给外接模块，但不更新语言模型权重；提议器与细化器按任务族训练，因此这不是一个无需训练、可直接跨任务使用的通用系统。论文同时考虑无推理轨迹的符号任务与自然语言推理任务，以检验该接口能否兼顾结构化计算和语言解码。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入问题或任务实例。

</div>
<div class="notation-item" markdown="1">

**$L^{(0)}$**

任务专用提议器根据输入生成的$K$个基础潜变量。

</div>
<div class="notation-item" markdown="1">

**$L^{\star}=L^{(0)}+\Delta$**

经递归细化后的潜变量，其中$\Delta$是细化器输出的有界残差修正。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{M}$**

参数始终冻结、接收文本与软词元并解码预测答案的预训练大语言模型。

</div>

</div>

**直接相关的工作**

- **SoftCoT**: 与本文采用相同类型的冻结解码器和软词元注入接口，但由冻结的通用语言助手一次性提出软思考，不进行后续细化。LRT据此把“潜变量从何而来”作为控制变量，改用任务专用编码器生成基础潜变量，并增加多步递归计算。
- **EBM-CoT**: 保留通用提议器，并通过学习到的标量能量场及其梯度校准潜变量。本文认为这种更新主要把表示推向低能量区域，未必能够执行多步搜索；LRT改用共享的向量值递归转移，通过反复、有界的残差更新细化潜在状态。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

复杂推理若完全依赖离散思维链，就必须逐词生成中间步骤，既受到固定词表和自回归生成方式的约束，也会让早期错误向后传播；更关键的是，监督或诱导高质量思维链通常预设存在可模仿的推理轨迹，但 Countdown-4、Sudoku 一类任务可能只有问题与答案，没有记录求解搜索过程。与此同时，直接微调大型语言模型成本高，并可能造成灾难性遗忘，因此需要一种仅训练小型外接模块、仍能执行多步计算的方案。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **离散文本空间中的思维链及其搜索扩展**：语言模型把中间推理逐步外化为文本，并可进一步结合多次采样、搜索或强化学习来寻找较好的推理路径；每一步都作为离散词元提交，后续步骤以此前生成的文本为条件。
- **冻结解码器的连续空间推理（SoftCoT 与 EBM-CoT）**：这类方法不更新大型语言模型，而是由辅助模型产生与当前样本相关的连续向量，并把它们作为软词元注入冻结解码器。SoftCoT 使用冻结的通用语言助手提出潜变量但不再细化；EBM-CoT沿用通用提议器，并沿学习到的标量能量函数梯度调整潜变量，使其移动到能量较低、被认为更一致的区域。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 通用语言助手产生的潜变量主要适配自然语言分布，未必包含特定符号任务所需的结构；离开其擅长的语言场景后，这些软词元可能不只是效果有限，还会误导冻结解码器。其后果是，潜变量注入本身不能保证带来有效推理，提议器必须适应具体任务族。
- 无细化的一次前向生成缺乏显式的迭代计算，而基于标量能量梯度的细化只能沿固定能量地形做局部校准。作者认为这种更新难以表达多步搜索、约束传播和反复纠错，因此计算深度不足；增加推理步骤也不能像循环状态转移那样自然复用同一组参数。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未给出这样一种冻结解码器方案：潜变量既由面向任务的模块生成，又通过可重复展开的向量值状态转移执行实质性的多步计算，同时只用答案监督训练而不要求推理轨迹。此前的小型循环推理器主要作为针对单项任务、从头训练的独立求解器使用，尚未被系统地用作冻结预训练语言模型之前的潜变量计算模块；这种分工能否兼顾循环网络的迭代计算能力与语言模型既有的序列建模和语言能力，仍是空缺。

</div>
<div markdown="1"><span>核心问题</span>

在保持大型语言模型完全冻结、仅提供按任务族训练的答案标注数据时，能否让小型任务专用提议器先产生基础潜变量，再由参数共享的循环推理器多轮修正这些潜变量，从而比通用提议器或能量梯度细化更可靠地支持符号与自然语言推理，并以较小推理开销改善最终答案？

</div>
<div markdown="1"><span>作者直觉</span>

可以把基础潜变量理解为一份面向当前问题的“内部草稿”：任务专用提议器先把草稿写在与冻结语言模型兼容的连续表示空间中，避免通用助手给出与任务结构无关的提示；循环推理器随后反复读取原始草稿和当前状态，每轮只施加受限的小幅残差修正，而不是彻底重写表示。这样既能把表示锚定在解码器可利用的起点附近，又能通过共享参数的多轮更新逐步传播约束、发现冲突并纠错；最后，冻结语言模型只需发挥其已具备的序列建模与答案解码能力。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

LRT 将推理分成“生成初始连续思路—循环修正—冻结大模型解码”三部分。给定实例 $x$ 和任务指令 $I$，任务专用 proposer 先把输入编码成 $K$ 个与解码器表示宽度一致的基础潜变量 $L^{(0)}$；小型 recurrent refiner 随后通过多轮有界残差修正得到精炼潜变量 $L^{\star}$；最后，冻结的 LLM 同时读取 $I$、实例信息与 $L^{\star}$，自回归生成答案。训练只使用最终答案监督，不要求人工推理轨迹，因而避免把中间推理强制写成离散文本。

这一设计把两种能力分工：冻结 LLM 保留已有的语言理解、序列建模和答案表达能力，约 $11.2$M 个可训练参数负责实例条件化与迭代计算。直观地说，proposer 先把题目翻译成大模型“看得懂”的一组草稿向量，refiner 像反复检查草稿一样逐步修正，而大模型负责结合题目要求把修正后的内部结果写成最终答案；因此，计算深度可以通过增加循环轮次提高，而不必扩大或微调 $8$B 解码器。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 输入表示与任务条件化

将 $x$ 的解码器嵌入经输入投影 $P_{\!\downarrow}$ 映射到工作宽度 $d'=256$，并在序列后附加 $K=32$ 个可学习查询向量。该步骤保留任务指令 $I$，供最终冻结解码器利用其指令遵循先验。

<div class="method-step__io" markdown="1">

**输入**：题目或程序任务实例 $x$、任务指令 $I$，以及冻结解码器提供的输入嵌入。<br>
**输出**：由题目 token 表示和可学习查询组成的低维编码序列。

</div>

**直观理解**：可学习查询可以看作 $32$ 个固定格式的“思考槽位”：它们读取当前题目，但不需要把中间过程写成文字。降维则使后续训练模块远小于冻结 LLM。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成任务专用基础潜变量

双向 proposer 使用两个 pre-norm Transformer block，让查询向量对整个输入进行注意力计算，再经输出投影 $P_{\!\uparrow}$ 返回解码器宽度 $d$。与从通用助手抽取软思路不同，该 proposer 直接针对目标任务和答案监督训练。

<div class="method-step__io" markdown="1">

**输入**：低维题目编码序列及其中的 $K$ 个查询槽位。<br>
**输出**：$K$ 个基础潜变量 $L^{(0)}$，其形状和表示宽度适合注入冻结解码器。

</div>

**直观理解**：这一步不是直接求出答案，而是为每道题生成不同的内部草稿。任务专用训练的目的，是先把草稿放到冻结大模型能够有效使用的表示区域，而不是提供几乎相同的通用向量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 循环残差精炼

TRM 风格的 recurrent refiner 重复使用同一转移块 $f$，在多轮高层循环与内部更新中产生有界残差修正，并逐步将 $L^{(t-1)}$ 更新为 $L^{(t)}$。标准推理配置执行 $45$ 次 refiner pass，最终得到 $L^{\star}$；参数不随循环深度复制。

<div class="method-step__io" markdown="1">

**输入**：基础潜变量 $L^{(0)}$、refiner 的可学习初始缓冲状态 $z_L^0,z_H^0$。<br>
**输出**：经过迭代计算的精炼潜变量 $L^{\star}$。

</div>

**直观理解**：同一个小网络像检查器一样被反复调用，每次只改一点，而不是用一次前向传播完成全部推理。这样可用较少参数换取较深计算，并使潜变量逐渐趋于稳定。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 冻结解码器生成答案

将 $L^{\star}$ 作为连续输入注入冻结的 LLM，由 LLM 按通常的自回归方式生成答案 token；解码器参数在两个训练阶段及推理时均不更新。模型只解码答案，不生成显式思维链。

<div class="method-step__io" markdown="1">

**输入**：任务指令 $I$、当前实例的上下文以及精炼潜变量 $L^{\star}$。<br>
**输出**：符号任务的最终解、代码或自然语言判断答案。

</div>

**直观理解**：refiner 提供经过加工的内部提示，但它并不独立负责把答案写出来；冻结 LLM 仍需结合指令、题目和潜变量完成序列建模与表达。因此 LRT 是小型循环推理器与大模型共同计算，而不是让 LLM 充当纯粹的抄写器。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文所给材料明确说明 LRT 使用“答案监督而无推理轨迹”，但未提供训练目标的显式公式、损失名称或 token 级归一化方式，因此不应补写未经原文确认的交叉熵公式。优化层面采用两阶段训练：先训练任务专用 proposer，使 $L^{(0)}$ 成为冻结解码器可利用的实例条件化表示；再固定 proposer、缓存 $L^{(0)}$，训练 recurrent refiner 产生 $L^{\star}$。最终答案经过冻结解码器得到，监督信号用于更新相应阶段的可训练潜变量模块，而解码器始终不更新。两阶段安排还避免 refiner 持续追逐一个尚在变化的 proposer；Appendix F 的作者报告称联合训练会降低稳定性，但该观察属于训练协议证据，而不是新的目标函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 任务专用 proposer**

该模块是双向编码器：$P_{\!\downarrow}$ 将冻结解码器对 $x$ 的嵌入投影到 $d'=256$，两个 pre-norm Transformer block 处理输入与 $K=32$ 个可学习查询，$P_{\!\uparrow}$ 再把查询输出映射回解码器宽度 $d$。其参数量约为 $4.2$M，并为每个实例产生不同的 $L^{(0)}$。

> 直观理解：它解决的是“从哪里开始想”的问题。若初始向量来自通用助手并偏离当前任务需要的表示区域，后续 refiner 即使循环很多次也难以补救；任务专用 proposer 因而承担题目理解和表示对齐，而不是单纯增加一段共享软提示。

**2. TRM 风格 recurrent refiner**

refiner 使用独立参数的单个转移块 $f$、投影 $P'_{\!\downarrow},P'_{\!\uparrow}$ 和初始缓冲状态 $z_L^0,z_H^0$，通过共享权重的多轮递归生成残差修正。主配置 refiner 约为 $7$M，总可训练参数约为 $11.2$M；固定参数量下，递归深度提供了超出单次前馈计算的额外处理能力。

> 直观理解：它解决的是“如何持续改进草稿”的问题。共享同一转移规则意味着增加思考轮数不需要按层复制参数；残差更新则限制每轮改动，使过程更像逐步纠错而非反复推翻重写。

**3. 冻结 LLM 解码器**

主要实验使用冻结的 Qwen3-8B，负责输入嵌入、序列建模和答案 token 解码；训练梯度只优化 proposer 与 refiner。冻结解码器使受控比较中的 backbone、prompt、数据和训练预算保持一致，也把新增能力归因于潜变量模块而非大模型微调。

> 直观理解：大模型提供已经学会的语言与序列先验，小模块不必重新学习如何读题和写答案。该分工也让同一框架可以覆盖算术、数独、代码生成和问答，而专用符号求解器通常没有自然语言接口。

**训练与推理**

训练分为两个阶段。第一阶段训练 proposer，输入任务实例并生成基础潜变量 $L^{(0)}$；第二阶段固定 proposer，将预先计算的 $L^{(0)}$ 缓存后训练 refiner，从而省去每个训练步重复运行 proposer。第二阶段采用截断梯度展开，而不是对全部 $45$ 次递归执行完整 BPTT；这保留深度递归的前向计算，但只在受控范围内保存和传播梯度，以降低显存与时间成本。原文材料未明确给出每阶段的优化器、学习率或截断边界，不能据此补全。

推理时，对新实例运行 proposer 一次得到 $L^{(0)}$，随后调用共享参数的 refiner 共 $45$ 次以形成 $L^{\star}$，最后由冻结解码器仅生成答案。任务指令 $I$ 仍在解码阶段提供，因为潜变量携带的是实例相关计算，并未取代 LLM 的指令遵循能力。该方式不输出约 $210$ 个思维链 token：Table 17 报告 LRT 只解码答案，在相同硬件上的相对延迟为 $0.34$，约 $1.1$ 秒/例，而 zero-shot CoT 为 $1.00$，约 $3.2$ 秒/例；这些数字描述该实验配置的实际代价，不代表跨硬件的普遍速度比。

**复现信息**

为复现核心结构，需要保留以下设置：proposer 工作宽度为 $d'=256$，使用 $K=32$ 个学习查询和两个 pre-norm Transformer block；refiner 使用独立的同类转移块并共享其递归参数；主实验 refiner 为约 $7$M，总可训练参数为 $11.2$M，约占所用 $8$B 解码器的 $0.14\%$，解码器全程冻结。训练的两个阶段均运行 $30$ 个 epoch、batch size 为 $64$，原文成本测量使用单张 $96$GB GPU。

公平解释结果时还需注意，主配置采用 $45$ 次 refiner pass 和截断展开。Table 18 报告，对全部 $45$ 次进行完整反向传播约需 $6\times$ 峰值显存和 $3\times$ step time，而准确率仅相差 $0.1$ 个百分点，因此截断并非通过明显牺牲准确率换取效率。Stage 2 缓存 $L^{(0)}$ 是成立于 proposer 已冻结这一前提；若改变为联合训练或持续更新 proposer，便不能直接沿用该缓存与成本结论。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 符号推理：Countdown-4（CD4）要求将四个整数通过算术运算组合为目标值；Sudoku 是 $9\times9$ 数独约束满足题。二者只有答案监督、没有真实搜索轨迹，用于测试模型脱离自然语言表面进行组合计算的能力。原文未明确报告各数据集的规模、划分和具体训练/测试样本数。
- 自然语言代码推理：HumanEval 与 MBPP 都是根据文档字符串合成 Python 函数，用于测试潜变量推理能否转化为可执行程序。原文未明确报告各数据集的规模、划分和具体训练/测试样本数。
- 自然语言常识推理：StrategyQA 是需要隐含多步推理的二分类（是/否）问答任务，用于测试方法在非代码自然语言问题上的迁移。原文未明确报告数据规模和划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Exact solve rate**

预测答案必须与标准答案完全一致的比例，文中用于 Countdown-4 和 Sudoku。 （越高越好，因为它直接表示完整题目被正确解出的比例。）

</div>
<div class="metric-item" markdown="1">

**pass@1**

只生成一个候选程序时，该程序通过测试的比例，文中用于 HumanEval 和 MBPP。 （越高越好，因为它表示单次生成即可得到可执行正确程序的概率。）

</div>
<div class="metric-item" markdown="1">

**Accuracy**

分类或问答预测正确的比例，文中用于 StrategyQA；所有指标均以百分比报告。 （越高越好，因为它表示问题答案判断正确的比例。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨五个基准的受控冻结解码器比较

<div class="result-value" markdown="1">

作者报告 LRT 在 Countdown-4、Sudoku、HumanEval、MBPP 和 StrategyQA 上显著优于既有冻结解码器连续空间推理方法，并且在相同骨干模型上以较小推理计算量超过非思维模式的 CoT。所给摘录未提供该主表各方法的具体分数，因此无法核验每个数据集上的数值差异。

</div>

这个结果支持 LRT 的总体有效性：在解码器不能更新、数据和预算保持一致时，改进主要应归因于潜变量的生成和递归精炼设计，而不是更强的解码器。它不能单独证明 LRT 在所有模型规模、不同训练预算或思维模式解码器上都更优，也不能由摘录推断具体提升幅度。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On symbolic reasoning with answer supervision but no reasoning traces (Countdown-4, Sudoku) and on natural-language reasoning (HumanEval, MBPP, StrategyQA), LRT substantially outperforms prior frozen-decoder continuous-space reasoning methods under an identical decoder, prompt, data, and training budget, and outperforms non-thinking-mode chain-of-thought prompting on the same backbone at a small fraction of its inference compute.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 实例无关软提示与实例条件化潜变量的对照（Countdown-4）

<div class="result-value" markdown="1">

Prefix-tuning 得分 $12.5$，P-tuning v2 得分 $28.4$，Direct 基线为 $27.8$；仅加入任务专用 proposer 得分 $42.0$，再加入递归精炼后 LRT 得分 $56.7$。原文还报告，相对 proposer-only，递归精炼增加 $14.7$ 个百分点；相对软提示对照，实例条件化 proposer 增加 $13.6$ 个百分点。

</div>

该实验把“参数量增加”与“根据当前题目生成并计算潜变量”区分开来。共享给所有题目的软提示几乎不能超过 Direct，而题目相关的初始潜变量带来明显提升，递归处理又进一步提升，说明 LRT 的关键不只是输入端多了一组参数，而是潜变量随实例变化并被持续计算。不过该实验只在 Countdown-4 上进行，不能单独证明同样的差距会出现在其余四个基准。

<div class="result-source" markdown="1">

来源：Appendix C, § Do soft prompts alone explain the gain?

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Prefix-tuning reaches 12.5 and P-tuning v2 reaches 28.4 – the latter essentially matching the no-latent Direct baseline (27.8).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 递归精炼模块的主设计比较

<div class="result-value" markdown="1">

完整 LRT 在 CD4、Sudoku、HumanEval 和 Avg. 上分别为 $56.7$、$49.2$、$37.8$ 和 $54.1$；将潜变量直接重新生成、只在初始化时注入 proposer 输出、或将双时间尺度状态合并为单一状态后，Avg. 分别为 $50.2$、$50.9$ 和 $51.5$。完整反向传播通过全部 $45$ 次迭代的 Avg. 为 $54.0$，相对截断版本变化为 $-0.1$，但训练内存约增加 $6$ 倍、步时间约增加 $3$ 倍。

</div>

结果表明，残差更新、每次快速更新都保留实例条件化基准，以及双时间尺度状态，分别对稳定而有效的递归计算有作用；单纯把递归过程改成重新生成潜变量会削弱题目相关锚点。全量反向传播没有带来有意义的精度收益，却显著增加成本，因此截断反向传播是更合理的工程折中。由于该表只展示部分列，不能把 Avg. 的数值解释为仅由这四个展示列计算得到的平均。

<div class="result-source" markdown="1">

来源：Appendix D, Table 9

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Full backpropagation through all 45 passes, rather than truncating to the final cycle, leaves accuracy essentially unchanged (−0.1) while raising training memory ≈6× and step time ≈3× relative to the truncated variant; truncated unrolling is therefore the better operating point.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 摘录没有提供完整的 Table 1 主结果、各数据集规模与划分、训练/测试样本数及完整计算预算，因而无法独立核验作者关于“显著优于”和“较小推理计算量”的具体幅度。
- 不同方法之间仍存在边界条件：EBM-CoT 是作者自行复现，TRM 在 Countdown-4 上还需要作者自定义的序列到序列适配；此外，软提示对照只在 Countdown-4 上运行，且 CoT 使用非思维模式而非官方技术报告设置。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Direct（无 CoT 直接回答）：不生成中间推理步骤，测量冻结 Qwen3-8B 在任务提示下的直接解题能力，是判断“是否需要思考过程”的基础参照。
- Zero-Shot CoT：通过提示词诱导模型生成推理链，但不增加可训练参数；该比较检验潜变量方法相对于离散文本推理的收益。实验中 Qwen3 使用非思维模式，以保持推理预算可比，这与官方技术报告设置不同。
- SoftCoT 与 EBM-CoT：两种训练得到的冻结解码器连续潜变量模块，与 LRT 使用相同的解码器、提示、训练数据和预算，因此主要比较潜变量模块本身。EBM-CoT 没有官方实现，文中结果来自作者复现。
- Prefix-tuning 与 P-tuning v2：在约 $11$M 可训练参数预算下学习实例无关的软提示，用于检验“任务监督加输入端可训练向量”是否已经足以解释 LRT 的提升。

**实验想回答的问题**

- 在相同冻结解码器、提示、训练数据与训练预算下，LRT 是否比直接回答、非思维模式零样本 CoT 以及既有连续潜变量推理方法更有效？
- LRT 的性能提升究竟来自实例条件化的潜变量计算与递归精炼，还是仅来自额外的可训练参数、提示适配或训练协议？

**实验实现**

所有基于 LLM 的方法使用冻结的 Qwen3-8B 解码器。主表比较无可训练参数的 Direct、Zero-Shot CoT 与训练得到的冻结解码器潜变量模块；LRT、SoftCoT 和 EBM-CoT 共享相同接口、解码器、提示、训练数据和预算，因而控制了除潜变量模块外的主要变量。主表数值是三个随机种子的均值与标准差，消融实验使用单一随机种子；Avg. 是五个基准上的非加权平均。原文未在所给章节中提供完整主结果表、各方法的具体推理步数或完整训练规模。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 残差参数化、持续注入 proposer 输出与双状态设计（Table 9） | 相对完整 LRT 的 Avg. $54.1$，直接重新生成 $L^{\star}$ 得到 $50.2$，仅在初始化时注入 $u$ 得到 $50.9$，合并 $(z_L,z_H)$ 为单一状态得到 $51.5$；完整反向传播得到 $54.0$，即变化 $-0.1$，但内存约为 $6$ 倍、步时间约为 $3$ 倍。 | 这一组实验分别隔离了三个结构假设：残差形式使递归更新围绕实例相关的初始提案进行，持续注入 $u$ 防止快速状态偏离题目，双状态允许不同时间尺度的计算协同。全量反向传播的结果说明性能差异主要来自前向递归结构，而不是必须保存所有迭代的梯度。 | Appendix D, Table 9<br><span class="experiment-evidence">Full backpropagation through all 45 passes, rather than truncating to the final cycle, leaves accuracy essentially unchanged (−0.1) while raising training memory ≈6× and step time ≈3× relative to the truncated variant; truncated unrolling is therefore the better operating point.</span> |
| 残差惩罚系数 $\lambda$ 扫描与训练协议（Table 10、Table 14） | 在残差惩罚扫描中，$\lambda=0.01$ 时 CD4 为 $56.7$、Avg. 为 $54.1$；$\lambda=0$ 时分别为 $53.0$ 和 $51.8$，且相对残差范数为 $3.9\times$；$\lambda=1.0$ 时分别降至 $48.2$ 和 $49.0$，相对残差范数为 $0.1\times$。训练协议方面，两阶段方案的 CD4/Avg. 为 $56.7/54.1$，联合训练为 $50.1/51.0$，第二阶段不冻结 proposer 为 $56.0/53.6$，推理时移除指令 $I$ 为 $52.0/50.7$。 | 惩罚系数呈现明显的中间最优：不约束会让残差把潜变量推向泛化但与实例无关的位置，约束过强又会抑制真正有用的精炼。联合训练较差且不稳定，支持先学习 proposer、再训练 refiner 的两阶段安排；移除指令后的下降说明潜变量提供题目相关计算，但不能完全替代冻结 LLM 的指令遵循先验。 | Appendix D, Table 10；Appendix F, Table 14<br><span class="experiment-evidence">With λ = 0 the residual Δ grows large and the refined latents drift toward a generic, instance-agnostic point; with λ = 1.0 the penalty suppresses Δ almost entirely and LRT collapses toward the proposer-only result.</span> |

**定性案例**

- 所给摘录没有提供具体题目的输入、潜变量轨迹、生成答案或错误案例，因此没有可据以分析的定性案例。原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Proposes recurrent continuous latent thoughts that enable frozen LLMs to perform iterative symbolic, code, and natural-language reasoning.; rule check: matched taxonomy keywords; top rule score=6.0
- 全文指纹：`75e1d84a9ef647967618baaec1f6459efd188a0f46408d34cd90a6fb620c17c6`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
