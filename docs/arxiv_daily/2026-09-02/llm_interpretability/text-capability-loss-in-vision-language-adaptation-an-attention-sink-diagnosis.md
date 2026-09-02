---
title: "[论文解读] Text Capability Loss in Vision-Language Adaptation: An Attention-Sink Diagnosis"
description: "[arXiv 2609.00746][LLM 机制与可解释性] 原文未明确报告。"
arxiv_id: "2609.00746"
announcement_date: "2026-09-02"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:49:02.117763+00:00"
source_sha256: "513248526600c2bb7928927f77a25f20f2631c6778684d147b52255bc0842cb5"
tags:
  - "LLM 机制与可解释性"
  - "多模态 VLM"
  - "LLM Reasoning"
  - "视觉—语言模型"
  - "大语言模型适配"
  - "文本能力损失"
  - "格式敏感任务"
  - "注意力汇"
  - "Sink Strength"
  - "QK-RMSNorm"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2609.00746</p>

# Text Capability Loss in Vision-Language Adaptation: An Attention-Sink Diagnosis

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Minsik Choi, Geewook Kim, Young Geun Kim</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Korea University；Young Geun KimKorea University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00746v1) · [PDF 下载](https://arxiv.org/pdf/2609.00746v1) · **关键词** 视觉—语言模型, 大语言模型适配, 文本能力损失, 格式敏感任务, 注意力汇, Sink Strength, QK-RMSNorm<br>


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

本文研究视觉—语言模型（VLM）的多模态适配及其对语言能力的影响。典型 VLM 将视觉编码器和投影器连接到预训练大语言模型（LLM）的解码器，并在图文数据上进行联合微调；该过程可能改变 LLM 原有的文本处理能力。本文特别关注格式敏感任务，即不仅要求答案内容正确，还要求模型严格遵守输出格式或规则的任务，例如指令跟随，以及最终答案必须经过严格解析的链式思维推理。研究的核心背景是：注意力机制通常会把较大比例的注意力概率集中到少数早期位置，这些位置被称为注意力汇（attention sink）；本文考察视觉—语言微调是否会破坏这一结构，以及这种破坏是否能解释文本能力损失。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉—语言模型与多模态微调**

视觉—语言模型把图像编码为向量，再通过投影器转换成语言模型可以处理的表示，并与文本共同输入语言模型。多模态微调会更新部分或全部 LLM 解码器参数，使模型能够根据图像和文字生成回答，但也可能改变其原有的纯文本行为。

</div>
<div class="concept-item" markdown="1">

**注意力汇**

在 Transformer 的自注意力机制中，某些早期 token 位置会吸收大量注意力概率，即使这些位置未必包含当前任务最重要的语义信息。它可以被理解为注意力分布中的稳定“锚点”，帮助其他位置维持较稳定的注意力分配；本文将其在微调后的减弱或消失称为注意力汇腐化。

</div>
<div class="concept-item" markdown="1">

**QK-RMSNorm**

查询向量和键向量分别由投影矩阵 $W_q$ 和 $W_k$ 产生，二者的内积决定注意力分数；QK-RMSNorm 在计算该内积前对查询和键进行均方根归一化。按注意力头分别归一化可以削弱输入幅度对注意力分数的直接影响，而按整层归一化则可能使不同注意力头受到不均等的尺度约束。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是一个预训练文本 LLM 经过视觉—语言适配后形成的 VLM，以及其适配前的参考 LLM。给定文本输入或图文输入，模型输出文本；研究比较参考 LLM 与适配后 VLM 在格式敏感文本任务上的性能差异，并把该差异视为文本能力间隙。本文假设视觉—语言微调会扰动读取早期注意力汇特征的查询、键投影，从而改变注意力汇的稳定性；同时假设适配前 LLM 的注意力汇强度可以在不进行 VLM 训练的情况下，预测适配后会损失多少文本能力。比较还需要区分多模态微调造成的损失与普通文本继续训练造成的损失，并考虑不同 LLM 架构是否原生采用 QK-RMSNorm。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$S$**

Sink Strength，本文提出的注意力汇强度标量；它完全在适配前的基础 LLM 上，通过少量仅推理前向计算得到，用于衡量各注意力头的汇集中程度。

</div>
<div class="notation-item" markdown="1">

**$W_q$**

查询投影矩阵，将隐藏状态映射为 query 向量；本文认为视觉—语言微调对它的扰动可能放大注意力汇处的分数变化。

</div>
<div class="notation-item" markdown="1">

**$W_k$**

键投影矩阵，将隐藏状态映射为 key 向量；它与 $W_q$ 共同决定查询位置对各键位置的注意力偏好。

</div>
<div class="notation-item" markdown="1">

**$\rho$**

Spearman 秩相关系数，用于衡量 Sink Strength 对不同骨干 LLM 的排序与其视觉—语言适配后文本能力损失排序的一致程度。

</div>

</div>

**直接相关的工作**

- **Xiao et al. (2024)，attention sinks**: 该工作揭示了现代 LLM 会把大量注意力集中到少数早期位置，为本文研究注意力汇提供基础。本文不只分析固定网络在推理时的注意力汇，而是进一步研究视觉—语言微调过程中注意力汇如何被破坏，以及这种破坏与文本能力损失的关系。
- **Sun et al. (2024)，massive activations**: 该工作指出注意力汇位置的隐藏状态往往由少数具有极大幅度的特征维度主导。本文沿用这一机制解释，认为视觉—语言微调扰动读取这些维度的 $W_q$ 与 $W_k$ 后，会因输入幅度效应在注意力汇处产生更强的分数变化。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

将预训练大语言模型适配为视觉语言模型时，联合多模态训练可能损害原有文本能力，而且损害主要出现在格式敏感任务上：模型不仅要答对，还必须严格遵守输出格式，例如指令跟随或最终答案需按规则解析的链式推理。这会削弱视觉语言模型在实际文本交互和严格自动评测中的可靠性。论文指出，多个已发布的视觉语言模型—语言模型组合出现了两位数的文本能力差距，而仅进行文本训练的对应模型退化明显较小，说明问题与视觉语言适配过程有关。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **训练数据与参数更新约束**：在多模态监督微调数据中重新加入文本数据，以维持语言能力；或冻结语言模型、使用低秩适配器等方式，限制视觉语言训练对原有语言参数的直接改动。
- **训练后参数修复与合并**：在视觉语言训练完成后，将文本模型或其他模型的参数重新混合，采用线性、谱方法或稀疏化等权重合并策略，试图恢复被削弱的文本能力；另一类做法是在预训练后、视觉语言训练前注入 $QK$-RMSNorm，以稳定查询和键投影。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 这些方法只能部分缓解能力损失，且可能牺牲多模态适配效果；更根本的问题是它们没有解释为什么视觉语言训练会特别损害格式敏感能力，因此缺乏在训练前识别高风险语言骨干模型的依据。
- 现有工作没有充分区分预训练阶段已经存在的脆弱性与视觉语言更新诱发的额外破坏。论文的负向对照显示，训练后注入 $QK$-RMSNorm 不能复现原生架构中的保护作用，而所测试的训练后权重合并也未能恢复损失的能力，表明简单的事后修复不足以解决该问题。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚未解决的空缺是：能否从基础语言模型本身，在不进行视觉语言训练的情况下，测量一种可解释且低成本的指标，预测其适配视觉语言模型后会发生多少格式敏感文本能力退化；同时，还需要说明该指标为何与退化相关。论文将候选机制定位为注意力汇损坏：现代语言模型会把大量注意力概率集中到少数早期位置，而视觉语言微调可能扰动读取这些位置特征的查询、键投影，导致每个注意力头的汇集中度下降。

</div>
<div markdown="1"><span>核心问题</span>

基础语言模型的早期注意力汇强度，能否作为视觉语言适配后格式敏感文本能力退化的训练前预测信号；如果可以，注意力汇在视觉语言微调中的破坏是否构成连接模型结构、参数更新与能力损失的机制解释？

</div>
<div markdown="1"><span>作者直觉</span>

注意力汇可以理解为模型用于吸收分散注意力概率的稳定锚点，使注意力更有秩序地分配给真正承载格式信息的表面词元。若视觉语言更新改变了查询和键投影对输入幅度的敏感性，早期汇位置上的巨大激活会放大对应的对数几率扰动，从而使部分注意力头的汇集中度坍塌。因而，预训练模型原本拥有越强、越稳固的注意力汇，适配时越可能保留这种锚定功能，格式敏感文本能力也越可能少受损；反之，汇较弱的模型在视觉语言训练前就更脆弱。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文提出一个不需要进行视觉语言训练的事前诊断指标 $S$（Sink Strength），用于预测语言模型骨干在适配视觉语言模型（VLM）后会损失多少文本能力。方法先在候选文本语言模型上测量注意力汇聚位置的强度，再将该指标与视觉语言适配后的文本能力下降联系起来；其核心解释是，视觉语言训练会扰动早期的 attention sink，而原始模型中更强、更稳定的 sink 能为严格格式输出提供更大的保护裕度。直观地说，模型在加入视觉能力前先接受一次“注意力结构体检”：如果注意力已经没有明显的稳定锚点，它在多模态训练后更容易忘记精确遵守输出格式。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造语言模型—视觉语言模型配对

从已发布的 VLM 中抽取语言骨干，将其作为独立的因果语言模型（VLM-LM），并与对应的文本参考 LLM 配对；比较时尽量区分视觉语言训练造成的影响与一般继续训练造成的影响。

<div class="method-step__io" markdown="1">

**输入**：候选文本参考模型、对应的视觉语言模型及其语言骨干；模型家族包括 Qwen、InternVL 和 LLaVA-OneVision。<br>
**输出**：模型配对及其文本能力差值，即 VLM-LM 相对于参考 LLM 的退化。

</div>

**直观理解**：先把多模态模型中的“语言部分”单独拿出来，与原来的纯文本模型比较，像是检查同一个人的语言能力在学习视觉知识后是否下降。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在基座语言模型上测量 Sink Strength

对每个校准提示执行推理，记录最后约 $10$ 层中各层、各注意力头和各查询位置的注意力分布；在每个 $(\ell,h,q)$ 上找出注意力概率最大的键位置 $p_{\mathrm{sink}}$，计算其相对其余位置总质量的对数优势，并对这些值取中位数。

<div class="method-step__io" markdown="1">

**输入**：未经视觉语言适配的参考 LLM、约 $15$ 个与 IFEval 测试集不重叠的校准提示。<br>
**输出**：单一标量 $S$，完全由文本参考 LLM 计算得到，不需要 VLM 前向传播或视觉语言训练。

</div>

**直观理解**：观察模型是否把大量注意力稳定地放在一个早期“锚点”上；锚点越突出，$S$ 越大，通常表示模型更能抵抗后续多模态训练的扰动。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 进行视觉语言适配并评估文本能力

按照各模型公开的训练方案进行视觉语言适配，包括 SFT、RL、DPO 或 MPO 等；同时使用文本-only 训练轨迹或同一基座的文本训练端点作控制，以判断退化是否特异于视觉模态。

<div class="method-step__io" markdown="1">

**输入**：语言模型骨干、视觉语言训练数据与训练配方，以及适配后的 VLM-LM。<br>
**输出**：适配后的 VLM-LM、训练过程中的 sink 变化，以及其在格式敏感文本任务上的得分。

</div>

**直观理解**：让模型真正学习图像输入，再检查它还能否完成严格规定的文本任务，并与只继续学文本的版本对照。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 用相关性与留一法验证预测能力

先用 Spearman 相关系数检验 $S$ 对退化排序的能力，再用一维线性拟合和 leave-one-pair-out 验证估计退化幅度；另外测试不同任务、模型规模、稠密或 MoE 架构的扩展面板。

<div class="method-step__io" markdown="1">

**输入**：每个参考 LLM 的 $S$、适配后的文本能力差值，以及多个格式敏感任务的结果。<br>
**输出**：跨模型和跨任务的排序相关性、留出预测误差，以及 $S$ 作为训练前筛选指标的适用边界。

</div>

**直观理解**：先看指标能否正确判断谁更脆弱，再看它能否大致预测会掉多少分；留一法相当于每次把一个模型藏起来测试。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### Sink Strength 定义

$$
S:=\operatorname{median}_{(\ell,h,q)}\log\frac{a_{p_{\mathrm{sink}}}^{(\ell,h,q)}}{1-a_{p_{\mathrm{sink}}}^{(\ell,h,q)}}
$$

**符号说明**

- $S$：Sink Strength，表示基座语言模型的注意力 sink 强度。
- $\ell$：网络层索引；中位数统计限制在最后约 $10$ 层。
- $h$：注意力头索引。
- $q$：查询位置索引。
- $p_{\mathrm{sink}}$：在给定层、注意力头和查询位置下，注意力概率最大的键位置，即每个头的 sink 位置。
- $a_{p_{\mathrm{sink}}}^{(\ell,h,q)}$：对应 sink 位置的注意力概率。

<div class="equation-explanation" markdown="1">

**直观理解**：分数先把 sink 的注意力概率与其余位置的总概率进行比较，再取对数并在层、头和查询位置上取中位数。因此，$S$ 越高，说明注意力越集中且这种集中越稳定；它是后续视觉语言训练前可获得的基座侧保护裕度代理。<br>
**原文位置**：第 3.2 节 Definition

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文的核心方法不是提出新的视觉语言训练损失，而是提出训练前诊断指标 $S$。视觉语言适配仍使用各模型原有的训练目标和配方，包括 SFT、RL、DPO 或 MPO；文中机制分析进一步把视觉语言更新造成的 sink 对数优势扰动记为 $B_{\mathrm{gap}}$，并以基座优势与扰动之间的裕度 $G_{\mathrm{base}}-B_{\mathrm{gap}}$ 解释 sink 是否能够保留，但所给节选未提供该理论界限的完整公式。因而，$S$ 主要承担低成本排序功能，而不是直接参与模型参数优化。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Attention Sink 与格式敏感能力关联**

Attention sink 指注意力概率长期集中于早期位置的现象。论文将 IFEval、EQ-Bench、GSM8K-CoT 和 GPQA-Diamond-CoT 定义为格式敏感任务，因为它们依赖严格可解析的表面输出规则；视觉语言训练若破坏 sink，可能削弱逐位置的格式跟踪，而知识型任务主要依赖 MLP 权重中的事实表征，受影响相对较小。

> 直观理解：严格评分的任务不只要求答案内容正确，还要求长度、语言、标记或最终答案格式完全合规；一个稳定的注意力锚点有助于模型持续记住这些表面规则。

**2. Sink Strength $S$**

指标定义为最后约 $10$ 层、各注意力头和查询位置上的 sink 注意力对数优势的中位数。$S>0$ 表示 sink 的注意力质量超过所有非 sink 位置的合计质量，$S\leq0$ 表示 sink 未能占据多数聚合注意力质量；指标在基座 LLM 上计算，约需 $15$ 次推理型前向传播。

> 直观理解：它把许多注意力矩阵压缩成一个数：数值越大，模型越有一个清晰的注意力“支点”；数值较小则说明支点本来就弱，后续训练更容易使其崩溃。

**3. QK-RMSNorm 结构关联与负向干预**

参考模型中逐头 QK-RMSNorm 与较高 $S$ 聚类，而无该结构的模型处于中等范围；逐层 QK-RMSNorm 虽然存在，但不能提供相同的逐头保护。实验还表明，预训练后再注入逐头 QK-RMSNorm，以及视觉语言训练后的多种权重合并修复，均未稳定复现或恢复原有能力。

> 直观理解：论文观察到，真正从预训练阶段就与注意力投影共同适应的逐头归一化可能更重要；训练结束后再补模块或把权重混回去，并不能简单“修复”已经形成的损伤。

**训练与推理**

推理阶段先对候选基座 LLM 使用校准提示，提取最后约 $10$ 层的注意力概率并计算 $S$；整个过程不需要图像、不需要 VLM 前向传播，也不需要先训练 VLM。训练阶段再按公开配方将语言骨干适配为 VLM，并从 VLM 中抽取语言骨干进行文本评测；同一基座的 text-only 训练轨迹用于控制一般继续训练的影响。评测阶段在 IFEval、EQ-Bench、GSM8K-CoT 和 GPQA-Diamond-CoT 等格式敏感任务上比较参考 LLM 与 VLM-LM，并通过每个提示的 both-pass、regression、recovered 和 both-fail 分类定位能力损失。最后以 $S$ 对各模型的退化进行排序相关分析，并用留一模型外的一维线性回归估计退化幅度。

**复现信息**

可复现所需的关键设置是：$S$ 使用与 IFEval 测试集不重叠的 $15$ 个校准提示；对 $7$B 规模骨干，单张 A6000 GPU 的计算时间约为 $8$ 秒。主分析包含五个 headline VLM–LLM 配对，并将 Molmo2-O 作为非 headline 控制；IFEval 的逐提示分析使用 $541$ 个验证提示。逐头 QK-RMSNorm 是每个注意力头分别按自身 RMS 归一化，逐层版本则对层内拼接的全部头使用一个 RMS。文中报告的关键限制是：六个配对样本较少，$S$ 能排序但不能区分具有相同 $S$ 的模型；例如 Qwen3-VL 与 InternVL3.5 共享 $S=2.36$，但观测退化仍相差 $3.5$ 个百分点。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 九任务文本能力套件：MMLU、MMLU-Pro、BoolQ、MBPP（代码，指标为 pass@1）、RULER（长上下文）、GSM8K-CoT、IFEval、GPQA-Diamond-CoT 和 EQ-Bench。其作用是覆盖知识、推理、代码、长上下文及严格格式遵循等能力；其中 IFEval 的检查器直接判定表面格式，因此被指定为注意力汇聚点损坏的重点指标。原文未明确报告各数据集的样本规模与具体划分。
- 五个主分析视觉语言模型及一个控制模型：Qwen3-VL-8B-Instruct、InternVL3.5-8B、Qwen2.5-VL-7B-Instruct、InternVL3-8B、LLaVA-OneVision-Qwen2-7B-OV，以及 Molmo2-O-7B 控制模型。它们用于比较不同视觉语言适配结果的文本能力保留情况；MMLU-Pro 和 RULER 的主分析排除了 Molmo2-O。
- IFEval 专用的 17 对模型面板：在主面板之外加入不同规模的 Qwen3-VL、Ovis2、MolmoE、InternVL3、MiniCPM-V、LLaVA-NeXT-Mistral 和 Idefics3 等模型。其作用是检验格式敏感能力与诊断量之间的关系能否超出少量主模型配对；原文未明确报告该面板的样本划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**IFEval prompt-level strict accuracy**

按提示级别统计严格格式检查通过率，要求模型不仅回答内容正确，还必须遵守指定的输出格式；它直接测量格式敏感的指令遵循能力。 （越高越好，因为更高表示更多提示同时满足内容与表面格式约束。）

</div>
<div class="metric-item" markdown="1">

**GSM8K-CoT 与 GPQA-Diamond-CoT 的严格最终答案评测**

评估包含链式推理的数学或知识问题，并依据严格解析的最终答案评分；它用于观察视觉语言适配是否损害需要正确生成并遵守答案格式的推理能力。 （越高越好；但分数通常只反映最终答案是否通过评分器，并不能单独证明中间推理过程正确。）

</div>
<div class="metric-item" markdown="1">

**MMLU-Pro、MMLU、BoolQ、MBPP、RULER 与 EQ-Bench 的任务分数**

分别覆盖学科知识、判断、代码通过率、长上下文和对话式能力等文本侧表现，用于比较能力损失是否集中于格式敏感任务，而不是所有能力均匀下降。 （各任务均为分数越高越好；不同任务的原始分数含义并不完全相同，因此更适合在同一任务、同一协议下比较参考 LLM 与 VLM-LM。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 评测流水线与外部 OpenCompass 结果的一致性检查

<div class="result-value" markdown="1">

在匹配的 OpenCompass 配置下，Qwen2.5-7B-Instruct 的 GSM8K-CoT 得分为 90.67，相比 Qwen 博客的 91.6 相差 0.93 分；MMLU-Pro 得分为 55.84，相比 56.30 相差 0.46 分。

</div>

这一结果说明作者的文本评测实现与外部参考结果大体一致，降低了后续能力差异来自评测框架错误的可能性。它只验证了评测流水线的可复现性，不能证明 VLM 适配造成的损失，也不能证明 Sink Strength 的预测能力。

<div class="result-source" markdown="1">

来源：Appendix B.1, Pipeline sanity

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Our LLM-side numbers reproduce the Qwen blog values on Qwen2.5-7B-Instruct GSM8K-CoT to within 0.93 pt (90.67 vs. 91.6) and MMLU-Pro to within 0.46 pt (55.84 vs. 56.30) when run under matched OpenCompass configurations.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 语言骨干抽取后的数值一致性检查

<div class="result-value" markdown="1">

从视觉语言模型抽取语言骨干后，作者在留出的纯文本探针上检查往返转换，并报告其 logits 与原始语言模块一致。

</div>

该检查确认被评测的 VLM-LM 没有因为参数重命名或模块拆装而被意外改变，因此参考 LLM 与 VLM-LM 的差异更可能来自视觉语言适配本身。由于原文没有给出最大误差、平均误差或容差数值，这一结论是流程级验证，不是精度性能结果。

<div class="result-source" markdown="1">

来源：Appendix B.2, Backbone Extraction

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

All extracted backbones are saved to safetensors, and the round-trip reproduces the original language module’s logits on a held-out text-only probe.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨模型、跨任务的主评测覆盖范围

<div class="result-value" markdown="1">

文本侧评测覆盖九项任务，并应用于全部六个模型配对；其中 MMLU-Pro 和 RULER 在五个主分析配对上测量，并排除 Molmo2-O。IFEval 被设为注意力汇聚点损坏的重点指标。

</div>

这一设计同时检验任务类型和模型家族两个维度：如果损失主要出现在 IFEval、严格最终答案等格式敏感任务，而不是所有文本任务都下降，就能支持“能力损失具有选择性”的解释。但所给章节没有提供各模型在这些任务上的具体得分、相对下降值或统计显著性，因此不能据此复述主假设已被定量证实。

<div class="result-source" markdown="1">

来源：Appendix B.1, Nine-task suite

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

IFEval is the headline metric for sink corruption because its checker grades surface format directly (Zhou et al., 2023).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验章节主要是评测协议、模型抽取和复现性说明，缺少主结果表、Sink Strength 数值、相关性统计、完整消融结果及逐模型比较，因此无法严格判断作者关于跨六个配对模型和多项格式敏感任务的核心结论。
- 任务规模、数据划分和各模型的具体评测分数在摘录中未充分报告；此外，协议差异本身可能改变格式敏感任务的结果，所以跨研究或跨框架比较时必须保持聊天模板、few-shot 设置和评分器一致。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 对应的文本参考 LLM，例如 Qwen3-8B、Qwen3-4B 和 Qwen3-1.7B，用作视觉语言适配前的文本能力参照，帮助计算参考 LLM 与抽取后的 VLM-LM 之间的相对差异。
- 从 VLM 中抽取的语言骨干（VLM-LM），并保留原始输入嵌入、输出语言模型头及必要的 per-head 归一化参数；这是被测对象，而非独立训练的竞争方法。
- Instruct protocol 与 Community-default protocol 的协议对照：前者使用聊天模板、零样本，后者采用各任务默认 few-shot 数量且关闭聊天模板。该对照检验结果是否依赖评测格式，而不是检验模型结构本身。
- Qwen2.5-7B-Instruct 在 OpenCompass 下的社区报告值，用于流水线 sanity check，而非用于证明本文方法优于其他方法。

**实验想回答的问题**

- 在统一的文本评测协议下，从视觉语言模型中抽取的语言骨干相较于对应文本参考模型是否出现能力损失；不同协议之间的差异是否会影响这一诊断？
- 评测与骨干抽取流程能否可靠地区分文本能力，并支持在多个视觉语言模型—语言模型配对及格式敏感任务上分析损失？

**实验实现**

所有文本侧能力使用 lm-evaluation-harness v0.4.12，在两个协议下评测。Instruct protocol 使用 --apply_chat_template、--num_fewshot 0、--batch_size 8 和 bf16，模拟指令模型的聊天式使用；Community-default protocol 使用各任务默认 few-shot 数量，例如 MMLU 为 5、GSM8K 为 8，并关闭聊天模板。研究者将 Qwen2.5-VL、LLaVA-OneVision/LLaVA-Llama3 等模型的语言参数重新映射到对应的 <Family>ForCausalLM 命名空间，同时保留原始输入嵌入和 lm_head.weight；Qwen3-VL 还保留 $q_norm/k_norm$ 的 per-head 归一化尺度。抽取后的骨干保存为 safetensors，并通过文本探针检查往返转换是否保持 logits。文本评测、诊断量计算及部分差异测量在单张 48GB NVIDIA A6000、bf16 上完成；原文报告单个 7B 骨干的 Sink Strength 前向计算约需 8 秒。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Instruct protocol 与 Community-default protocol 对照 | 作者明确使用两种协议，并指出“their disagreement on a single backbone is itself diagnostic”；Instruct protocol 为聊天模板、零样本，Community-default protocol 使用任务默认 few-shot 且关闭聊天模板。 | 该对照隔离评测接口与提示格式的影响：同一骨干在两种协议下表现不一致，可能反映模型对聊天模板或提示构造的敏感性，而不应直接解释为参数能力损失。摘录没有给出协议差异对应的具体分数，因此无法判断差异大小。 | Appendix B.1, Evaluation Protocols<br><span class="experiment-evidence">We evaluate all text-side capability with lm-evaluation-harness v0.4.12 (Gao et al., 2024) under two protocols whose disagreement on a single backbone is itself diagnostic.</span> |
| VLM-LM 骨干抽取的保真度控制 | 抽取过程保留原始输入嵌入、输出语言模型头以及 Qwen3-VL 的 $q_norm/k_norm$ 尺度，并通过留出文本探针检查往返 logits；作者报告 logits 得以复现。 | 这项控制实验隔离了“抽取错误”这一替代解释：若忽略输出头或 per-head 归一化参数，文本能力下降可能只是评测对象不再等价于原始语言模块。结果支持抽取流程的功能等价性，但没有报告误差数值或统计检验。 | Appendix B.2, Backbone Extraction<br><span class="experiment-evidence">For Qwen3-VL, the same procedure additionally preserves the $q_norm/k_norm$ scale parameters used in per-head normalization.</span> |

**定性案例**

- 流水线 sanity check 是本摘录中唯一可具体核对的案例：Qwen2.5-7B-Instruct 在匹配配置下的 GSM8K-CoT 和 MMLU-Pro 结果分别为 90.67 与 55.84，均接近 Qwen 博客报告值。它说明实验环境能够复现合理的外部基准，但不等同于本文关于视觉语言适配损失或注意力汇聚点机制的案例性证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It diagnoses VLM adaptation-induced text capability loss through attention-sink behavior and proposes a predictive internal-mechanism metric.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`513248526600c2bb7928927f77a25f20f2631c6778684d147b52255bc0842cb5`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
