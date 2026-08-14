---
title: "[论文解读] Reasoning for Social Audio-Visual Question Answering: Where Do We Stand?"
description: "[arXiv 2608.13239][LLM 评测] 本文重新审视社会音视频问答中的推理范式，质疑现有基准与思维链训练能否真实衡量模型利用音视频理解社会情境的能力，并以清洗后的基准和简单监督微调基线揭示语言先验与文本描述已能解释相当一部分表现。"
arxiv_id: "2608.13239"
announcement_date: "2026-08-14"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T02:59:45.542621+00:00"
source_sha256: "083f07e1089e4a7b919cd4b20d19be0b7c6c3a7caeb2cc5d4a1f1b97a19d2b45"
tags:
  - "LLM 评测"
  - "VLM Reasoning"
  - "LLM 其他"
  - "LLM Reasoning"
  - "社会音视频问答"
  - "多模态大语言模型"
  - "社会理解"
  - "思维链推理"
  - "监督微调"
  - "IntentBench-Prime"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.13239</p>

# Reasoning for Social Audio-Visual Question Answering: Where Do We Stand?

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Koen P. de Vries, Xavier Alameda-Pineda, Estefanía Talavera, Stéphane Lathuilière</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Inria at Univ. Grenoble Alpes, CNRS, LJK, France；Affiliation: University of Twente, The Netherlands</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13239v1) · [PDF 下载](https://arxiv.org/pdf/2608.13239v1) · **关键词** 社会音视频问答, 多模态大语言模型, 社会理解, 思维链推理, 监督微调, IntentBench-Prime<br>
**代码**: [https://github.com/koenv759/VanillaSFT](https://github.com/koenv759/VanillaSFT)

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

本文重新审视社会音视频问答中的推理范式，质疑现有基准与思维链训练能否真实衡量模型利用音视频理解社会情境的能力，并以清洗后的基准和简单监督微调基线揭示语言先验与文本描述已能解释相当一部分表现。

**不用术语来说**：社会音视频问答要求模型观看视频、听取声音，再回答有关人物意图、情绪和互动关系的问题；但高分未必意味着模型真正理解了场景，因为题目本身可能有错误，答案也可能仅凭文字常识猜出，而且让模型生成冗长推理过程会增加训练和回答成本。因此，需要先确认评测是否可靠，再判断复杂推理方法是否确实比直接学习回答更有效。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者从评测有效性出发，识别出 IntentBench 中的坏题和可脱离音视频作答的题目，并据此提出经过自动与人工过滤的 IntentBench-Prime，使后续比较更集中于需要社会情境信息的问题。
- 作者建立不使用推理轨迹的 Vanilla SFT 作为必要参照，并通过 Question SFT 与 Caption SFT 对照模型进一步检验性能来源，从而把“方法是否有效”分解为复杂推理是否必要、模型是否依赖音视频，以及文本先验能解释多少表现三个问题。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究社会音视频问答（social AV-QA）：多模态大语言模型同时读取视频画面、声音和文本问题，判断人物的意图、情绪、关系或社会情境，并生成文本答案。这类能力被视为具身社会智能的基础，因为模型不仅要识别可见对象或语音内容，还要把人物行为、对话、时间顺序和社会常识结合起来。当前代表性路线以 Qwen2.5-Omni 等全模态模型为底座，通过显式思维链推理增强社会理解；HumanOmniV2 进一步要求模型先概括与问题相关的音视频上下文，再进行推理并回答，IntentBench 则是其主要评测基准。本文所处的核心背景不是提出更复杂的推理机制，而是检查两个更基础的前提：评测集是否真正要求音视频理解，以及显式推理训练是否确实优于直接监督微调。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多模态大语言模型（MLLM）与全模态模型（Omni-model）**

MLLM 将图像、视频或音频编码为语言模型能够处理的表示，再结合文本指令生成答案；能原生联合处理视频、音频和文本的模型在本文中称为全模态模型。本文以此类模型为社会音视频问答的基础架构。

</div>
<div class="concept-item" markdown="1">

**思维链（Chain-of-Thought, CoT）推理**

CoT 要求模型在最终答案之前生成一段显式中间推理文本，例如先概括场景，再分析人物意图。它可能改善可解释性或回答质量，但会增加训练数据制作成本，并因自回归生成大量推理词元而提高推理延迟。

</div>
<div class="concept-item" markdown="1">

**监督微调（Supervised Fine-Tuning, SFT）与 GRPO**

SFT 使用输入与目标输出配对直接训练模型；本文的 Vanilla SFT 仅学习由音视频和问题直接生成答案，不学习推理轨迹。GRPO（组相对策略优化）是一种强化学习方法，可依据同一输入下多份候选输出的相对奖励优化推理策略，HumanOmniV2 等方法将其用于强化显式推理。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

基本任务可写为：给定音视频片段 $V$、与其中社会互动有关的文本问题 $q$，模型生成答案 $a$；标准设置假定正确作答应依赖 $V$ 中的视觉、语音或环境声音证据，而不能仅凭问题措辞和常见答案模式猜测。本文还考察两个受限设置以诊断模型究竟利用了什么信息：Question SFT 只接收 $q$，用于测量训练集与评测集中的可学习语言先验；Caption SFT 接收问题无关的预生成视频文字描述 $c(V)$ 与 $q$，用于比较通用文本摘要和完整音视频输入的信息效用。评测背景中的关键风险有两类：一类是问题破损、表述不良或答案标注不可靠，使分数包含标签噪声；另一类是问题无需观看视频即可回答，使基准无法有效区分真正的社会音视频理解与文本捷径。作者据此清理 IntentBench 并构建 IntentBench-Prime，作为后续比较直接回答与显式推理方法的主要社会领域评测集。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$V$**

包含视觉画面与音频流的输入视频片段。

</div>
<div class="notation-item" markdown="1">

**$q$**

针对视频中人物、意图、情绪或社会情境提出的文本问题。

</div>
<div class="notation-item" markdown="1">

**$a$**

模型生成或选择的最终文本答案。

</div>
<div class="notation-item" markdown="1">

**$c(V)$**

由 ASID-Captioner 根据视频 $V$ 预先生成、且不针对具体问题的通用文字描述。

</div>

</div>

**直接相关的工作**

- **HumanOmniV2**: 本文最直接的比较对象和问题来源。HumanOmniV2 以 Qwen2.5-Omni 为底座，先进行 SFT，再进行两个 GRPO 阶段，并强制采用“相关视频上下文概括、显式推理、最终回答”的顺序，以缓解上下文理解不足和捷径推理；它同时引入了本文重新审查并清理的 IntentBench。
- **AffectOmni**: 它沿用并扩展 HumanOmniV2 的社会推理框架，通过 People Focus 和 Temporal Order 奖励强化人物关注与时间顺序建模，在情绪识别和时序敏感任务上报告改进。该工作代表继续增加专门推理奖励的路线，而本文考察这些复杂设计是否已经超过不生成推理轨迹的 Vanilla SFT 基线。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

具身社会智能需要模型从声音、画面和语言中识别人类意图、情绪及复杂互动，并针对具体问题提取相关证据。若基准含有歧义或错误题目，或者问题能够仅凭语言常识回答，评测分数就会混合真实多模态理解、数据偏差和猜题能力；同时，依赖长篇推理生成的方法会提高训练与查询延迟，不利于低延迟或需要针对同一视频反复提问的应用。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于思维链与 GRPO 的社会音视频问答**：现有方法通常让多模态大语言模型先生成逐步推理文本，再给出答案，并可使用群组相对策略优化（GRPO）强化这种推理行为。以 HumanOmniV2 为代表的方法还要求模型先总结相关音视频语境，意图是减少对场景理解不足和捷径推断。
- **IntentBench 基准评测**：IntentBench 以社会场景中的音视频问题测试模型对人物意图和互动的理解，并因 HumanOmniV2 的使用而成为该方向的重要参照。其默认前提是题目表述和答案可靠，且正确作答主要需要输入视频或音频中的社会信息。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 作者检查发现，IntentBench 约有 $7\%$ 的题目损坏或表述不当，另有约 $23\%$ 的题目可由多个预训练语言模型在不接收音视频时一致答对。其后果是原始分数受到标注噪声和语言先验显著干扰，难以单独反映社会音视频理解能力。上述比例是作者在引言中的报告，仍需结合完整过滤章节核验具体判定标准。
- 现有思维链方案需要蒸馏或构造推理轨迹，并在训练和推理时自回归生成较长解释，因而带来额外计算成本和响应延迟；更关键的是，领域中缺少使用相同问答数据、但直接输出答案的标准监督微调对照，因此复杂方法的增益可能来自训练数据或微调本身，而非推理机制。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未在较少受坏题和显性语言捷径污染的评测条件下，公平比较复杂思维链训练与直接监督微调；也没有充分区分模型成绩究竟来自问题文本中的数据先验、通用视频描述所提供的信息，还是针对当前问题从原始音频和视频中提取的证据。因此，当前结果不足以证明模型已经形成可靠的、问题特定的社会多模态理解。

</div>
<div markdown="1"><span>核心问题</span>

在社会音视频问答中，经过清理的基准是否会改变对模型能力的判断，思维链推理相较于使用相同数据的 Vanilla SFT 是否产生足以抵偿成本的真实收益，以及模型回答时是否确实需要直接处理完整音视频，而不是依赖问题文本或预先生成的通用字幕描述？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是设置逐步削弱输入与算法复杂度的对照：先清除明显坏题和无需视频即可回答的样本，再用相同训练问答数据比较“生成推理后回答”和“直接回答”，最后分别只提供问题文本或与问题无关的视频描述。若简单模型或弱输入模型仍能达到相近表现，就说明复杂推理并非性能的必要来源，现有分数更可能受到语言先验、数据来源偏差或文本化场景信息的推动；这种控制变量设计也能把真正需要改进的问题定位到从原始音视频提取问题相关证据的能力上。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文的方法部分并非提出新的复杂推理架构，而是建立一套用于审视社会音视频问答（social audio-visual question answering, AV-QA）的对照体系。核心做法有三层：首先清理原始 IntentBench，删除损坏题目和仅凭题干与选项即可回答的题目，得到 IntentBench-Prime；其次在完全相同的基础模型与训练数据上，将生成长推理轨迹的 HumanOmniV2 与直接输出答案字母的 Vanilla SFT 进行受控比较；最后通过 Question SFT、Caption SFT 和 Vanilla SFT 三种输入设置，分离数据集文本先验、文本化视频信息和原始音视频信息各自带来的收益。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建 IntentBench-Prime

作者先综合程序规则、Claude Haiku 4.5 审核结果和多个内部模型的答题表现，对疑似损坏题目排序，再按顺序人工检查；随后删除四个文本大语言模型仅根据题干和选项便一致答对的题目。清理仅执行删除，不修改问题、答案或视频，因此可用排除列表直接过滤已有逐题预测结果。

<div class="method-step__io" markdown="1">

**输入**：原始 IntentBench 中的 Social-IQ 2.0 问答对、对应音视频，以及每道题的正确选项与干扰选项。<br>
**输出**：两个逐级收紧的评测版本：仅删除损坏题目的 IntentBench-Prime (Clean)，以及进一步删除文本可答题目的 IntentBench-Prime (Hard)。

</div>

**直观理解**：这一步相当于先剔除答案标错、选项重复等“坏考题”，再剔除不看音视频也能猜出的“送分题”。由于只删题而不改题，已有模型无需重新推理即可重新计算分数。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 训练直接回答基线 Vanilla SFT

模型接收音频、视频和题目文本，即 $A+V+T$，但监督目标只要求输出正确选项对应的字母，不生成中间推理轨迹。主要版本冻结音频编码器、视频编码器和对齐层，仅对 Qwen2.5-Omni 的 thinker 部分应用 LoRA；作者另训练全参数微调版本作为优化方式对照。

<div class="method-step__io" markdown="1">

**输入**：Qwen2.5-Omni-7B，以及与 HumanOmniV2 对齐的原始音视频或图像多项选择训练数据；数据来源包括 OmniInstruct、Video-R1、Social-IQ 2.0 训练集和未进入 IntentBench 的 200 条 EMER 数据。<br>
**输出**：无需思维链、可直接用于多项选择 AV-QA 的 Vanilla SFT (LoRA) 与 Vanilla SFT (Full FT) 模型。

</div>

**直观理解**：模型看到的材料与推理模型基本相同，但训练时只学习“选哪个答案”，不学习先写一大段解释。这样可以检验性能提升究竟来自额外训练数据和任务适配，还是来自推理轨迹本身。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 进行同基础模型的推理与非推理对照

作者在相同或可比的基础模型规模下比较直接回答与链式推理方法，并区分域内评测和域外评测：IntentBench 系列与训练数据同源，WorldSense 和 Daily-Omni 则用于检查跨数据集泛化。同时记录训练 GPU 时、输出 token 数以及预填充和自回归解码延迟，以比较准确率之外的实际成本。

<div class="method-step__io" markdown="1">

**输入**：Vanilla SFT、未微调的 Qwen2.5-Omni-7B，以及 HumanOmniV2、AVATAR、AffectOmni 等生成推理轨迹的方法；评测输入来自 IntentBench、IntentBench-Prime、WorldSense 和 Daily-Omni。<br>
**输出**：直接回答与推理式训练在域内准确率、域外泛化、训练成本和逐题推理延迟上的受控比较。

</div>

**直观理解**：这里不只问“谁分数高”，还问“提升是否只是因为见过同类数据”以及“为了这点分数需要花多少计算”。域外数据尤其重要，因为它较难被训练集中的固定问法和答案规律蒙混过去。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分解文本先验、字幕与原始音视频的贡献

作者在其余训练设置相同的条件下训练 Question SFT、Caption SFT 和 Vanilla SFT：三者分别使用 $T$（仅问答文本）、$T+C$（问答文本与字幕）和 $A+V+T$（音频、视频与文本）。ASID 字幕独立于具体问题生成，避免字幕生成器按题目有针对性地泄露答案；评测时每个模型继续使用与训练阶段相同的模态设置。

<div class="method-step__io" markdown="1">

**输入**：同一个 Qwen2.5-Omni-7B 基础模型，以及限制为 Social-IQ 2.0 和 EMER 的同一批训练样本；每个样本分别表示为仅题目与选项、ASID-Captioner 生成的题目无关细粒度字幕、或原始音频与视频。<br>
**输出**：三种信息条件下的模型及其 IntentBench-Prime (Hard) 结果，用于估计数据集文本先验、视频文本化表示和原始音视频感知各自能够支持多少性能。

</div>

**直观理解**：Question SFT 测试模型能否只靠题目套路答题，Caption SFT 测试把视频先写成文字是否已经足够，Vanilla SFT 才测试直接看和听原始内容。三者好比闭卷猜题、看文字笔记答题和观看完整录像答题。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文没有给出带编号的损失函数或新的优化目标，因此不能据此补写专有公式。Vanilla SFT、Question SFT 与 Caption SFT 均属于监督微调：给定相应模态上下文和多项选择题，模型被训练为直接生成正确答案选项的字母；HumanOmniV2 等对照方法则生成较长的推理轨迹后再给答案。方法学上的关键不是改变损失形式，而是在相同基础模型和尽量相同的数据条件下改变目标输出的形式，使直接答案监督成为检验 CoT 训练增益的对照变量。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 保守的数据清理与排除列表**

损坏题目排序由三类信号构成：程序化异常检查、Claude Haiku 4.5 的细粒度审计，以及视频、字幕和带 oracle hint 字幕等设置下内部模型的答题一致性。人工按风险顺序复核，在连续 300 道题未发现损坏后停止；文本可答题则采用四个 LLM 全部答对的严格判据，以尽量保留仍对多模态模型有挑战的样本。

> 直观理解：自动信号只负责把最可疑的题排到前面，最终是否属于坏题仍由人工判断；四模型一致才删除的规则则减少误删真正需要理解音视频的题目。发布排除列表也使清理版本能兼容已有逐题预测。

**2. 无推理轨迹的 Vanilla SFT**

该模块沿用 Qwen2.5-Omni-7B 的多模态输入能力，冻结音频与视频编码器及模态对齐层，通过秩为 $16$ 的 LoRA 微调 thinker，并以正确选项字母作为短输出监督。它与 HumanOmniV2 尽量共享训练数据、视频采样和基础模型，使“是否训练生成 CoT”成为主要变化因素。

> 直观理解：Vanilla SFT 是论文要求后续推理方法必须超过的最低成本基线。它用于排除一种常见混淆：模型变好可能只是因为接受了任务相关监督，而不一定是因为学会了写推理过程。

**3. 三模态信息对照组**

Question SFT、Caption SFT 和 Vanilla SFT 使用相同基础模型、同源训练子集和相同的直接答案监督，只改变上下文：无外部上下文、ASID-Captioner 生成的题目无关字幕、原始音视频。未微调的 Qwen2.5-Omni 也在对应三种输入下评测，从而同时观察微调前后的模态差距。

> 直观理解：该设计把“模型记住数据集规律”和“模型真正从场景中提取信息”拆开。字幕若接近原始视频表现，说明当前模型直接处理音视频并未显著获得超出文本摘要的信息，但这不能单独证明字幕包含全部社会线索。

**训练与推理**

训练阶段，作者首先按 HumanOmniV2 代码库重建其训练数据组合，共使用约 20K 个视频和 10K 张图像及相应多项选择问答。主要 Vanilla SFT 版本冻结音频编码器、视频编码器和 aligner，仅微调 Qwen2.5-Omni-7B 的 thinker：LoRA 学习率为 $1\times10^{-4}$、秩为 $16$、训练 $1$ 个 epoch；视频按 $2$ FPS 取样，最多 $32$ 帧，超过 $16$ 秒时均匀铺开采样。全参数版本训练 $2$ 个 epoch，作者将其作为 LoRA 的辅助对照，而不是主要推荐方案。用于模态分解的三种 SFT 则把训练集缩小到 Social-IQ 2.0 与 EMER，并保持除输入模态外的训练条件一致。

推理阶段，Vanilla SFT 读取音频、视频和题目后直接输出一个或多个答案字母；推理模型需要自回归生成推理文本及最终答案。Question SFT 只读取题目与选项，Caption SFT 读取题目、选项和预先生成且不以问题为条件的 ASID 字幕。四个主要基准承担不同检验角色：IntentBench 用于与既有工作兼容，IntentBench-Prime (Clean) 降低坏题影响，IntentBench-Prime (Hard) 进一步降低文本捷径，WorldSense 和 Daily-Omni 检查训练分布之外的音视频耦合与日常场景泛化。效率测量将推理拆为输入预填充与输出解码；由于直接回答只产生极短答案，它主要减少的是自回归解码开销，而不是多模态输入编码开销。

**复现信息**

公平解释结果所需的关键设置包括：基础模型为 Qwen2.5-Omni-7B；Vanilla SFT 尽量复用 HumanOmniV2 的数据构成和视频配置；主模型采用 LoRA，训练在 $4\times$ H100 80 GB 上少于 4.5 小时，对应约 18 GPU 小时。效率实验在同一张 H100 上进行，并在必要时使用各模型原生协议；直接回答平均输出 2 个 token，而 HumanOmniV2 推理平均输出 527 个 token，因此两者的延迟差异主要反映输出轨迹长度。

评测口径也影响结论：IntentBench 的 emotion 类使用 F1，其余类别结果按样本数进行 micro-average 以得到总体指标；作者认为类别不均衡时该口径比 macro-average 更合适。IntentBench 的 deception 子集有 4 个视频加载失败，因而被排除。HumanOmniV2 在主要表格中采用其原论文通常略高的公开数字，使对 Vanilla SFT 的比较更保守；但由于复现仍存在提示词、FPS 和最大帧数等差异，这些结果应理解为严格控制下的强经验对照，而不是对所有 CoT 方法在所有训练预算下均无效的普遍证明。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- IntentBench-Prime：由作者清理 IntentBench 得到，用于评估社会意图、情绪和欺骗等音视频理解能力。清理流程从 IntentBench 所含的 $2356$ 个 Social-IQ 2.0 问题中删除 $192$ 个损坏问题；Clean 版本共 $2493$ 题，按 Why、How、What、Other、Emotion、Deception 六类统计；Hard 版本进一步排除可由多个预训练语言模型仅凭文本一致答对的简单题，共 $1895$ 题。Clean 测试总体性能，Hard 更集中检验语言捷径被削弱后的多模态能力。
- WorldSense：外部音视频理解基准，用于检验在 HumanOmniV2 训练数据之外的跨基准泛化。论文报告总体成绩，但所给原文未明确报告该数据集的规模、划分方式及各子任务样本数。
- Daily-Omni：面向日常场景音视频推理及跨模态时间对齐的外部基准。实验报告总体平均分以及 Context Understanding、Reasoning、$30$s、$60$s 等子集成绩，用于判断方法是否能处理不同视频长度和推理类型；所给原文未明确报告数据规模与划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**问答准确率**

正确回答数占评测问题总数的比例；表中以百分比报告，并分别给出类别准确率与总体平均值。它直接衡量选择正确答案的能力，但不能单独证明模型确实利用了音频或视频证据。 （越高越好，因为更高值表示在固定问题集合上答对的比例更大。）

</div>
<div class="metric-item" markdown="1">

**微平均准确率**

先汇总所有类别中的正确预测与样本数，再计算整体准确率，因此样本较多的类别权重更大。作者认为 IntentBench 类别不平衡时，微平均比对各类别等权的宏平均更适合进行方法间比较。 （越高越好，但必须确认不同方法采用相同题目集合和平均方式。）

</div>
<div class="metric-item" markdown="1">

**计算成本与推理延迟**

训练侧考察生成或蒸馏推理轨迹及模型优化所需开销，查询侧考察自回归生成长推理文本带来的响应时间。该指标用于评价准确率相近时方法的实际部署代价；所给原文没有保留相应表格中的具体数值。 （越低越好，因为更少训练计算和更短查询延迟意味着相同准确率下效率更高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### IntentBench-Prime 的 Clean 与 Hard 版本上比较 Qwen2.5-Omni-7B、HumanOmniV2 和 Vanilla SFT。

<div class="result-value" markdown="1">

在 Clean 集上，Vanilla SFT 的全参数微调和 LoRA 分别达到 $73.6\%$ 与 $73.8\%$，高于 HumanOmniV2 的 $71.8\%$；在更难的 Hard 集上，两者分别为 $69.0\%$ 与 $70.4\%$，也高于 HumanOmniV2 的 $66.9\%$。其中 LoRA 相对 HumanOmniV2 的总体优势分别为 $2.0$ 和 $3.5$ 个百分点。

</div>

作者据此主张：在相同社会问答训练数据下，直接学习“输入到答案”的简单目标已经优于显式推理方案，而且优势在去除较多文本捷径的 Hard 集上没有消失。分析上，这说明现有 CoT 训练没有在这些准确率指标上产生可见的额外收益，但不能证明所有推理方法都无效，也不能证明 Vanilla SFT 的答案过程具有可解释推理能力。

<div class="result-source" markdown="1">

来源：附录 Table 6，IntentBench-Prime (Clean)；Hard 集对应数值见附录 Table 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

HumanOmniV2 [30] A+V+T 69.0 70.8 71.7 78.7 81.9 60.2 71.8
Vanilla SFT (Full FT) A+V+T 71.1 72.3 74.7 81.2 82.6 58.2 73.6
Vanilla SFT (LoRA) A+V+T 72.0 72.5 75.3 79.9 83.2 58.2 73.8

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨数据集比较 Vanilla SFT 与 Qwen2.5-Omni-7B、HumanOmniV2、AVATAR 和 AffectOmni。

<div class="result-value" markdown="1">

WorldSense 上 Vanilla SFT (LoRA) 为 $48.8\%$，与 AffectOmni 的 $48.8\%$ 并列最高，并高于 HumanOmniV2 的 $47.1\%$；Daily-Omni 平均分为 $65.2\%$，高于基础模型和全参数 Vanilla SFT 的 $62.1\%$、AffectOmni 的 $61.9\%$、HumanOmniV2 的 $58.5\%$ 与 AVATAR 的 $55.7\%$。在 Daily-Omni 的 Context Understanding 和 Reasoning 子类中，LoRA 版本分别取得 $60.1\%$ 与 $76.6\%$。

</div>

这些外部基准用于测试结论是否局限于 IntentBench-Prime。结果支持作者关于“简单 SFT 至少应成为必要基线”的主张，尤其是 Daily-Omni 上 CoT 方法没有表现出优势。不过，不同已发表方法可能具有不同训练语料、实现和报告协议，因此该结果更适合说明现有分数不足以证明复杂推理训练有效，而不是对所有模型架构作严格受控排名。

<div class="result-source" markdown="1">

来源：Table 3(b)，WorldSense and Daily-Omni

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Vanilla SFT (LoRA) × 48.8 60.1 76.6 68.3 61.4 65.2

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 在 IntentBench-Prime 上，以 Question SFT 和 Caption SFT 替代完整音频、视频输入，诊断模型依赖的信息来源。

<div class="result-value" markdown="1">

作者报告 Question SFT 仍能学到显著的文本先验，而只使用与问题无关的通用视频字幕的 Caption SFT，其问答表现与处理完整多模态数据的 Vanilla SFT 相当。所给原文未明确报告该比较的具体分数。

</div>

Question SFT 的表现意味着，即使经过清理，题目措辞和答案选项中仍存在可学习规律；Caption SFT 与完整音视频模型相当，则表明当前模型可能没有充分提取问题特定的声画证据，通用文本摘要已覆盖其实际使用的大部分信息。该实验不能证明音频和视频普遍无用，因为字幕本身由视频生成并可能压缩了关键多模态信息，而且作者明确说明该结论目前限于社会理解领域。

<div class="result-source" markdown="1">

来源：第 1 节 Introduction，Finding 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A generic textual caption yields QA performance on par with processing the full multimodal data.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验没有报告多次运行的均值、方差、置信区间或显著性检验，因此较小分差，特别是 IntentBench-Prime Clean 上 LoRA 与全参数微调之间的 $0.2$ 个百分点，不能确认具有统计稳定性；部分外部方法还存在训练数据和报告协议差异。
- 字幕替代完整音视频的结论仅在社会理解任务上得到验证，且字幕由读取过视频的 ASID-Captioner 生成。该实验说明文本中间表示足以复现当前模型成绩，但不能证明原始声画信息本身无价值，也不能区分字幕保留了多少音频线索、视觉线索或生成偏差。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Qwen2.5-Omni-7B：Vanilla SFT 与 HumanOmniV2 所依赖的通用全模态基础模型参照。它不经过本文的任务微调，因此用于衡量性能提升是否仅来自在社会问答数据上继续训练。
- HumanOmniV2：核心思维链参照，先概括相关上下文，再生成推理过程，并采用相应推理训练策略。它与 Vanilla SFT 使用相同的音视频问答数据，因而比较重点是复杂推理训练和显式推理轨迹是否带来超出直接监督微调的收益。
- AVATAR 与 AffectOmni：额外的音视频推理方法，用于避免结论只依赖 Vanilla SFT 与单一 HumanOmniV2 的比较。AffectOmni 与 HumanOmniV2 使用相同训练数据，但原文提示其 IntentBench 原报告采用宏平均，本文为适应类别不平衡而统一关注微平均。
- Question SFT 与 Caption SFT：模态诊断参照。Question SFT 只输入问题和候选答案文本，用于测量可学习的文本先验；Caption SFT 将原始音视频替换为 ASID-Captioner 生成的、与具体问题无关的文本字幕，用于检验通用字幕是否已足以支持问答。

**实验想回答的问题**

- 在使用相同社会音视频问答训练数据时，不生成推理链的直接监督微调 Vanilla SFT，能否在 IntentBench-Prime、WorldSense 和 Daily-Omni 上达到或超过基于思维链的社会推理方法，同时降低训练与推理开销？
- 模型的问答成绩究竟来自对音频和视频中问题相关证据的提取，还是主要来自问题文本中的语言先验以及通用视频字幕提供的信息？

**实验实现**

Vanilla SFT 以 Qwen2.5-Omni-7B 为基础，输入音频、视频和问题文本，直接监督生成答案，不要求生成上下文摘要或思维链；论文同时评估全参数微调与 LoRA 参数高效微调。主要评测覆盖 IntentBench、IntentBench-Prime、WorldSense 和 Daily-Omni。HumanOmniV2 在 IntentBench、WorldSense 与 Daily-Omni 上采用其原论文中通常略高的报告值，使比较对作者主张更保守；IntentBench-Prime 的附录表则列出相应复现结果。Deception 子集中有 $4/200$ 个视频加载失败，评测时予以排除。作者还以仅文本的 Question SFT 和以预生成字幕代替音视频的 Caption SFT 做模态诊断；所给原文未明确报告随机种子、置信区间或显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 在相同 Vanilla SFT 目标下比较全参数微调与 LoRA，以隔离参数更新方式的影响。 | IntentBench-Prime Hard 上，LoRA 从全参数微调的 $69.0\%$ 提升到 $70.4\%$；Clean 上则从 $73.6\%$ 小幅提升到 $73.8\%$。Daily-Omni 平均分从 $62.1\%$ 提升到 $65.2\%$，WorldSense 从 $46.7\%$ 提升到 $48.8\%$。 | 该比较表明 Vanilla SFT 的竞争力并不依赖昂贵的全参数更新，LoRA 反而在所报总体指标上更强。它隔离的是微调参数化方式，而不是 CoT 本身；由于原文未给出多次运行方差，Clean 上 $0.2$ 个百分点的差异不应被解释为确定的统计优势。 | 附录 Table 7，IntentBench-Prime (Hard)；Clean 结果见 Table 6，跨基准结果见 Table 3(b)<br><span class="experiment-evidence">Vanilla SFT (Full FT) A+V+T 66.5 66.4 70.8 75.5 82.6 58.2 69.0
Vanilla SFT (LoRA) A+V+T 68.8 68.2 72.6 75.8 83.2 58.2 70.4</span> |
| 将 IntentBench-Prime 从 Clean 进一步收紧为 Hard，排除多个预训练语言模型无需音视频即可一致答对的问题。 | 题量由 Clean 的 $2493$ 降至 Hard 的 $1895$。Qwen2.5-Omni-7B、HumanOmniV2、Vanilla SFT (Full FT) 和 Vanilla SFT (LoRA) 的总体分数分别从 $67.8\%$、$71.8\%$、$73.6\%$、$73.8\%$ 降至 $63.2\%$、$66.9\%$、$69.0\%$、$70.4\%$；LoRA 仍保持最高总体分数。 | 该数据消融检验成绩是否依赖容易从文本猜出的题目。所有方法在 Hard 上下降，说明 Clean 集仍包含较容易或先验较强的样本；但 Vanilla SFT 的相对优势保留，意味着其主结果不是只由被移除的简单题推动。Hard 只是按语言模型一致性筛题，并不等价于彻底消除全部文本偏差。 | 附录 Table 7，IntentBench-Prime (Hard)；Clean 对照见附录 Table 6<br><span class="experiment-evidence">Qwen2.5-Omni-7B [29] A+V+T 61.7 60.3 65.8 64.6 71.4 61.2 63.2
HumanOmniV2 [30] A+V+T 63.2 65.2 67.6 71.7 81.9 60.2 66.9
Vanilla SFT (Full FT) A+V+T 66.5 66.4 70.8 75.5 82.6 58.2 69.0
Vanilla SFT (LoRA) A+V+T 68.8 68.2 72.6 75.8 83.2 58.2 70.4</span> |

**定性案例**

- 附录 Figures 5–7 展示了三类典型数据故障：原始 Social-IQ 2.0 问题本身含歧义；交换候选项后，来自同一视频其他问题的真实答案使多个选项都合理；以及错误候选项的写法直接暴露正确答案。案例说明基准清理不仅是删除语法错误，还必须检查候选项是否与视频事实共同造成多解，以及答案格式是否泄露标签。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper audits and repairs an audio-visual reasoning benchmark while evaluating whether multimodal chain-of-thought methods outperform simple fine-tuning baselines.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`083f07e1089e4a7b919cd4b20d19be0b7c6c3a7caeb2cc5d4a1f1b97a19d2b45`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
