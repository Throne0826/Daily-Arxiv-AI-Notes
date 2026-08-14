---
title: "[论文解读] DFM Mimir v1: An Open HRM Delivering Frontier Performance at 1B Parameters Using Only Permissible Post-Training Data"
description: "[arXiv 2608.13517][预训练] 本文研究能否以仅含许可数据的训练方案，从零训练一个面向丹麦语与英语、参数量为10亿的层次化推理模型，并在有限训练与推理成本下获得有竞争力的语言理解和推理能力。"
arxiv_id: "2608.13517"
announcement_date: "2026-08-14"
primary_category: "llm_pretraining"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T03:04:46.573072+00:00"
source_sha256: "887c1cf060c6c3d872b6347c78b8d4f93fbcada7f26efd0fae29170745069e14"
tags:
  - "预训练"
  - "LLM Reasoning"
  - "大型语言模型"
  - "分层推理模型"
  - "HRM-Text"
  - "丹麦语"
  - "低资源语言"
  - "许可合规数据"
  - "合成移植数据集"
  - "指令微调"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">预训练 · arXiv 2608.13517</p>

# DFM Mimir v1: An Open HRM Delivering Frontier Performance at 1B Parameters Using Only Permissible Post-Training Data

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Peter Schneider-Kamp, Jacob Nielsen, Gianluca Barmina, Kenneth Enevoldsen, Lukas Galke Poech</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> University of Southern Denmark；Aarhus University；Hub:https://huggingface.co/danish-foundation-models/DFM-Mimir</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13517v1) · [PDF 下载](https://arxiv.org/pdf/2608.13517v1) · **关键词** 大型语言模型, 分层推理模型, HRM-Text, 丹麦语, 低资源语言, 许可合规数据, 合成移植数据集, 指令微调<br>
**项目页**: [https://huggingface.co/danish-foundation-models/DFM-Mimir](https://huggingface.co/danish-foundation-models/DFM-Mimir)

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

本文研究能否以仅含许可数据的训练方案，从零训练一个面向丹麦语与英语、参数量为10亿的层次化推理模型，并在有限训练与推理成本下获得有竞争力的语言理解和推理能力。

**不用术语来说**：训练高能力语言模型通常需要数量极大的文本、算力和复杂的多阶段流程，其中部分数据还可能涉及版权、个人信息或使用许可不清等问题。对于丹麦语这类高质量资源较少的语言，坚持只使用许可范围明确的数据，会进一步缩小可用语料池，使研究机构很难从零训练既合规、又足以支持后续指令训练和实际应用的基础模型。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出并从零训练了Mimir v1：一个基于HRM-Text架构、参数量为10亿、面向丹麦语和英语的模型；其训练混合包含161个数据集，每个训练周期约含705亿词元，并以许可数据为约束组织训练材料。
- 针对原始HRM-Text训练方案中不符合DFM许可标准的数据，作者构造合成“移植数据集”作为替代，并据此检验在不沿用相关非许可数据的条件下，模型能否维持或改善任务表现。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大型语言模型通常先利用大规模语料进行预训练，再通过指令微调等后训练步骤获得任务遵循能力；这套流程对算力、数据规模和数据许可均有较高要求。对于丹麦语等高质量开放语料相对有限的语言，难点不仅是提高模型能力，还包括保证全部训练数据可合法使用和再分发。本文在这一约束下研究小型双语语言模型：采用分层推理模型架构，从零训练一个约十亿参数的 Mimir v1，并将通常用于后训练的数据提前用于初始训练阶段，以降低对传统海量预训练语料的依赖。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大型语言模型**

大型语言模型通过预测和生成文本学习语言规律，并可进一步适配问答、推理、数学与代码等任务。本文讨论的是约十亿参数的小型模型，而非依赖数十亿至数千亿参数的常见前沿模型路线。

</div>
<div class="concept-item" markdown="1">

**分层推理模型（HRM）**

HRM 使用具有层次结构的计算过程处理文本与推理任务，使模型能够在不同层级上组织和更新信息。本文采用 HRM-Text 框架及文献[12]提出的架构，但所给节选没有披露其内部模块或具体计算公式。

</div>
<div class="concept-item" markdown="1">

**许可合规的后训练数据**

后训练数据通常用于指令微调或任务适配；“许可合规”表示其授权条件符合项目设定的使用与发布标准。本文还用合成的“移植数据集”替换不满足 DFM 许可标准的数据，以尽量保留原任务形式和训练价值。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是由 161 个数据集组成、每个训练周期约含 705 亿词元的丹麦语与英语训练混合，其中不符合许可标准的数据需要由合成的许可合规变体替代。模型在 HRM-Text 框架下从零训练并接受指令微调，输出为能够执行丹麦语和英语任务的十亿参数基础模型 Mimir v1。研究设定的核心假设是：通过把后训练数据用于初始训练，并以合成“移植数据集”替换受限来源，可以在有限语言资源、较低训练与推理成本及严格数据许可约束下，仍获得具有竞争力的语言与推理能力；本节仅陈述这一问题设定，未提供用于验证该假设的具体指标或完整实验条件。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **HRM-Text 与原始 HRM 架构（文献[12]）**: Mimir v1 直接采用文献[12]提出的架构，并沿用 HRM-Text 将后训练数据用于初始训练阶段的思路；本文的差异在于面向丹麦语与英语、从零训练十亿参数模型，并按 DFM 标准重新组织许可合规的数据。
- **Danish Foundation Models（DFM）项目**: 该项目提供本文的数据治理背景：训练数据必须是许可合规的，并在可能时采用开放许可证。Mimir v1 旨在为这一原则下的丹麦语模型研究提供可进一步后训练的基础模型。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

丹麦基础模型项目希望提供可供社区继续后训练的模型，同时要求数据公开许可、经协议授权，或符合欧盟面向研究机构的文本与数据挖掘例外，并排除含个人信息或侵权内容的数据。然而，主流大模型训练依赖海量语料、昂贵算力和多阶段流程；丹麦语的高质量数据本就有限，许可约束又进一步减少可用材料，因此从零构建能力足够且数据权利清晰的模型具有较高门槛。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **传统大模型的整体式多阶段训练方案**：先使用超大规模通用语料进行预训练，再通过指令微调等后训练阶段获得任务能力。这类方案通常通过扩大数据、参数和计算规模提升性能，但对数据来源和基础设施提出很高要求。
- **HRM-Text层次化推理框架**：该框架允许模型在初始训练阶段就更集中地利用后训练性质的数据，从而减少对传统海量预训练语料的依赖。本文将其作为低资源、强许可约束场景下构建基础模型的技术起点。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 传统整体式训练方案需要巨量数据与算力，形成研究准入壁垒；对于丹麦语等资源有限的语言，坚持许可数据标准时，研究者往往无法获得足够的高质量预训练语料，因而难以训练可用的基础模型。
- 原始HRM-Text方案使用的部分数据不符合DFM的许可标准，不能直接迁移到本文场景；如果简单删除这些数据，可能损失相应的指令跟随或推理训练信号，而原有工作尚未证明合成许可替代品能否弥补这一缺口。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未充分验证：在丹麦语资源有限且严格限制数据权利来源的条件下，HRM-Text能否从零训练出一个小型但有竞争力的双语模型；同时，也缺少关于合成“移植数据集”能否有效替代不符合许可要求数据的直接证据。

</div>
<div markdown="1"><span>核心问题</span>

仅使用符合既定许可标准的后训练数据，并以合成“移植数据集”替换不合规材料，能否从零训练一个10亿参数的HRM模型，使其在丹麦语和英语任务上超越原始HRM-Text，并在若干基准上接近或超过参数规模更大的模型？

</div>
<div markdown="1"><span>作者直觉</span>

HRM-Text把模型学习重点前移到更接近实际任务的高价值训练样本，因此有限数据可以比无差别扩充通用语料得到更直接的能力监督；对于因许可问题而不能使用的数据，还可以保留其任务形式与能力目标、重新合成内容，从而补回训练信号而不复制原数据。直观地说，作者试图通过提高每份数据与目标任务的相关性，以及用合成样本替换权利不清的内容，来同时缓解数据规模不足和许可受限两个问题。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Mimir v1 的方法不是提出新的网络结构或损失函数，而是把已有的 HRM-Text 层次推理架构与一套强调许可合规、英丹双语覆盖及自由生成能力的数据配方结合起来，从零训练一个约 10 亿参数的模型。端到端流程为：汇集 161 个数据集并按许可与用途组织，经过重格式化、生成后审核、翻译后审核或工具调用格式化等处理，按预设重复率组成每轮约 704.8 亿 token 的混合语料；随后使用 Gemma-4 tokenizer 和聊天模板编码，以长度 4096 的上下文输入具有高层与低层循环的 HRM-Text；最后通过 AdamW 和截断反向传播更新参数，并在推理时按任务生成自由文本或单个选择题答案。
技术设计的关键不只在模型规模，而在训练信号的重新配置：83% 的 token 来自原 Sapient 集合之外，主要内容由英语指令、丹麦语指令与知识、数学推理、智能体工具使用及合成任务构成。作者有意降低多项选择分类任务的主导地位，使模型更多学习“写出答案”而非“从候选项中挑答案”；通俗地说，系统不是主要靠刷选择题训练，而是让模型反复练习回答问题、展示推理结果、生成代码、调用工具以及处理丹麦语内容。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 许可数据汇集与功能分组

将每个数据集归入八个功能类别，并以采样 token 数控制混合比例；每轮语料约含 704.8 亿 token，其中英语占 68.62%，丹麦语占 24.74%，丹英双语占 6.54%。

<div class="method-step__io" markdown="1">

**输入**：来自 161 个数据集的英语、丹麦语及丹英双语样本，覆盖指令与知识、数学推理、智能体与工具调用、机器翻译、科学和摘要等任务。<br>
**输出**：具有明确语言比例、任务比例和来源记录的候选训练语料混合。

</div>

**直观理解**：这一步相当于制定课程表：既要让模型接触通用英语任务，也要给资源较少的丹麦语和数学、工具使用等专项能力保留足够课时。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 格式统一、合成转换与质量审核

数据按七条处理路径进入训练集，包括直接重格式化、筛选后重格式化、由 Gemma4 31B 生成后审核、工具调用格式化、翻译后修复与审核、协议提供以及派生任务构造；合成转换覆盖片段填充、去噪、重排、续写和指令任务。

<div class="method-step__io" markdown="1">

**输入**：格式、授权条件和任务形式各异的候选数据，包括公开仓库、Sapient 子集合、原始文本、翻译数据及工具调用数据。<br>
**输出**：统一为模型训练格式并经过相应质量控制的数据实例，其中约 65.96% 的 token 为直接重格式化数据，11.08% 为合成并审核的数据。

</div>

**直观理解**：公开数据并非直接拼接使用：不同来源先被整理成同一种“作业格式”，机器生成或翻译的内容还要经过筛选，避免低质量样本直接成为学习目标。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 采样配比与生成式任务重平衡

通过重复采样增强稀缺或重要数据，例如将 lærebogen 重复 $4\times$、八个小型丹麦语数据集重复 $10\times$，并将 Dolci-Instruct-SFT-No-Tools 重复两次；同时用开放式回答或答案生成形式替代部分原有多项选择任务。

<div class="method-step__io" markdown="1">

**输入**：完成格式化和审核的数据集，以及各数据集的基础规模、语言和功能类别。<br>
**输出**：每轮约 704.8 亿 token 的最终训练流，其前三大来源占 38.1%，前十大来源占 66.5%，且训练信号更偏向自由文本生成和精确匹配任务。

</div>

**直观理解**：较少见但重要的数据会被多抽几次，同时把部分“选 A/B/C/D”改成“自己写答案”，从而让模型更充分地练习丹麦语和实际生成能力。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分词、聊天序列构造与层次循环计算

使用 Gemma-4 tokenizer 和聊天模板把实例编码为最长 4096 token 的序列，再输入隐藏维度 1536、32 层、每层 12 个注意力头的 HRM-Text；模型配置 $2$ 个高层循环和 $3$ 个低层循环，以层次化循环逐步更新内部表示。

<div class="method-step__io" markdown="1">

**输入**：最终训练流中的对话、指令、推理、翻译及工具调用实例。<br>
**输出**：对下一个 token 的预测及其对应训练误差信号，同时获得适应现代聊天结构的模型行为。

</div>

**直观理解**：分词器先把文本变成模型可处理的编号，聊天模板标明谁在提问、谁在回答；高层循环可理解为较慢地维护总体解题方向，低层循环则更频繁地处理局部细节。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文节选没有给出训练损失的显式方程，也没有说明是否在标准自回归语言建模损失之外加入专用的 HRM 辅助目标，因此不能据此补造公式。可确定的是，模型根据 token 预测误差信号使用 AdamW 优化，并通过最多 5 步的截断反向传播把梯度传入层次循环；数据中的指令回答、自由生成、数学答案、代码和工具调用结构共同定义了模型要模仿的输出。换言之，优化器负责“怎样改参数”，而数据配方和聊天模板决定“希望模型生成什么样的后续 token”；确切损失形式仍需对照完整论文或公开训练代码核验。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. HRM-Text 层次推理主干**

模型采用 HRM-Text，隐藏维度为 1536，共 32 层，每层 12 个注意力头，前馈网络扩展因子为 4；层次推理设置为 $2$ 个 H-cycles 和 $3$ 个 L-cycles，并以最多 5 步的截断反向传播训练。位置编码使用 RoPE，参数为 $\theta=10{,}000$；归一化采用 pre-norm，数值稳定项为 $\epsilon=10^{-6}$。

> 直观理解：普通 Transformer 主要逐层处理一次，而这里还以不同频率循环更新表示，使模型能够在较慢的全局状态和较快的局部计算之间交换信息。截断反向传播限制需要保存的循环历史，从而让这种迭代计算能在实际硬件上训练。

**2. 许可导向的多任务数据混合器**

训练混合覆盖八类功能数据和七种处理形态，每轮约 704.8 亿 token；最大三类分别为丹麦语指令与知识 22.07%、英语指令 19.26% 和 Sapient mixed 17.02%，数学与推理另占 14.76%。采样重复用于提高低资源丹麦语数据和重点指令数据的出现频率，但混合高度集中，前十大数据源贡献 66.5% 的 token。

> 直观理解：该模块决定模型实际学到什么，比单纯增加数据集数量更重要。它一方面补足丹麦语等稀缺信号，另一方面也带来来源集中风险，因此结果应理解为特定数据配方与架构共同作用，而不是仅由 HRM 架构产生。

**3. Gemma-4 分词与聊天模板接口**

Mimir 从零训练时采用 Gemma-4 tokenizer，而不是原 HRM-Text 的自定义 tokenizer，并通过聊天模板表示用户、助手及可能的结构化交互。训练上下文长度为 4096 token，每张加速卡一次容纳 4 个完整上下文。

> 直观理解：分词器规定文本如何切成基本单位，聊天模板则规定对话角色和消息边界。二者把普通文本整理为统一输入，使模型不仅学习语言内容，也学习现代对话模型预期的回答结构。

**训练与推理**

训练从随机初始化开始，先用 Gemma-4 tokenizer 和聊天模板处理混合语料。每个上下文长 4096 token，每张 GPU 放置 4 个上下文，即每卡局部批量为 16384 token；8 张 GPU 配合 2 步梯度累积形成 262144 token 的全局批量。计算使用 bfloat16，聚合精度使用 fp32，模型参数与优化状态通过 FSDP 分片；AdamW 的 $\beta_1/\beta_2$ 为 $0.9/0.95$，权重衰减为 $0.1$，峰值学习率为 $3\times10^{-4}$，前 2000 步线性升温，之后保持不变。训练共进行 165 万步，使用 8 张 NVIDIA B200 180 GB GPU，作者报告耗时略少于 3 周、平均每步略少于 1.1 秒。
评测推理采用温度 0 的贪心解码和固定 shuffle seed 4242，并在完整测试集上运行。多项选择任务设置最大生成 1 个 token，非多项选择任务或启用推理模式时最大生成 2048 个 token；部分英语任务沿用 HRM-Text 配置进行少样本提示，所有丹麦语任务均为零样本。Mimir 因 PrefixLM 与 Gemma 4 聊天模板的兼容要求使用 FlashAttention，作者比较了采用 FlashAttention4 的 vLLM 与 Hugging Face Transformers，称两者结果在数值稳定性允许范围内相近，最终报告 Transformers 结果。

**复现信息**

公平复现所需的核心配置包括：隐藏维度 1536、32 层、12 个注意力头、前馈扩展因子 4、$2$ 个 H-cycles、$3$ 个 L-cycles、最多 5 步截断反向传播、0.2 的反向传播预热比例、RoPE 的 $\theta=10{,}000$、pre-norm 的 $\epsilon=10^{-6}$，以及 4096 token 的上下文长度。训练随机种子为 0，指数移动平均衰减为 0.9999；公开框架基于 Sapient 的 HRM-Text 代码，论文给出的实现仓库为 https://github.com/schneiderkamplab/HRM-Text。
解释结果时还必须保留数据采样条件：每轮 704.8 亿 token 并不等于同等规模的唯一文本，因为 lærebogen 等数据被重复采样；而 165 万训练步与每步 262144 token 相乘所对应的累计处理量也远大于单轮语料。原文没有在所给章节中报告去重算法、审核判据、不同类别的具体接受率、损失函数公式或从训练集中排除评测污染的完整程序，这些均是复现实验和判断数据泄漏风险时仍需核查的缺口。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 英语套件包含 7 个完整测试集：BoolQ、Winogrande、Hellaswag、MMLU、ARC-C、DROP 和 GovReport，分别覆盖布尔问答、常识与代词消歧、情境续写、综合知识、科学推理、阅读理解和长文摘要。除 GovReport 为零样本外，其余分别使用 5、5、10、5、25、3 个上下文示例；该套件用于检验通用英语理解、推理及生成能力，而非单一任务表现。
- 数学与代码套件包含 GSM8K、MATH 和 HumanEval，均采用零样本评测；HumanEval 明确包含 164 道编程题。GSM8K侧重小学文字题推理，MATH侧重难度更高的竞赛数学，HumanEval通过执行生成代码来检验函数实现能力，因此三者共同测试模型能否把推理转化为可验证答案或程序。
- 丹麦语套件包含 10 项零样本任务：Angry Tweets、DaLA、GEC-DaLA、PIQA-da、Daisy、Multi Wiki QA、WMT24++ EN-DA、Nordjylland News Summarization、IFEval-Da 和 Hellaswag-da，覆盖情感或文本分类、语法判断与纠错、常识推理、问答、翻译、摘要、指令遵循和情境推理。该套件主要检验低资源语言上的广度；PIQA-da 使用本地 JSON，其余数据源见表 11。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（Accuracy，Acc）**

正确预测样本占全部样本的比例，用于多数分类、选择题、数学答案和代码任务；表中 HumanEval 虽标为 Acc，但其具体执行判定口径在所给章节中未进一步展开。 （越高越好，因为表示更多样本得到正确答案。）

</div>
<div class="metric-item" markdown="1">

**F1 与精确匹配（Exact Match，EM）**

F1 衡量预测与参考答案之间精确率和召回率的调和平均，适合允许部分重叠的问答或序列任务；EM 仅在预测与标准答案完全一致时计为正确，标准更严格。 （越高越好；较高 F1 表示答案内容重叠更充分，较高 EM 表示完全正确的样本更多。）

</div>
<div class="metric-item" markdown="1">

**ROUGE-1 与 chrF**

ROUGE-1（R1）以一元词项重叠衡量摘要与参考摘要的接近程度；chrF 基于字符级匹配衡量翻译或摘要质量，对词形变化较丰富的语言较实用。 （越高越好，因为预测文本与人工参考文本的内容或字符片段更一致，但它们不能直接保证事实正确性与可读性。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 英语 7 项基准的套件平均分及与同规模 HRM-Text、较大 Qwen 3.5 4B 的比较

<div class="result-value" markdown="1">

Mimir 1B 的英语平均分为 69.0，高于 HRM-Text 1B 的 66.1，并仅比 Qwen 3.5 4B 的 69.3 低 0.3 分；分任务看，Mimir 在 BoolQ、Winogrande 和 DROP 上分别达到 87.8、73.5 和 83.1。

</div>

作者据此主张 Mimir 在英语综合表现上已接近 4B 级 Qwen，并在若干问答或消歧任务上领先所有列出的模型。分析上，平均分支持其小参数模型具有较强竞争力，但不同任务使用 Acc、F1 和 R1，直接做未加权平均会掩盖指标语义与任务难度差异；此外，Mimir 并未在 MMLU、ARC-C、Hellaswag 或 GovReport 上全面领先，因此不能解释为普遍优于所有较大模型。

<div class="result-source" markdown="1">

来源：表 7，English benchmark results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Mimir 1B | 87.8 | 73.5 | 67.3 | 57.5 | 81.6 | 83.1 | 32.0 | 69.0

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 数学与代码 3 项零样本基准及相对 HRM-Text 1B 的比较

<div class="result-value" markdown="1">

Mimir 1B 在 GSM8K、MATH、HumanEval 上分别得到 89.9、45.8、56.7，平均 64.1；HRM-Text 1B 对应为 84.8、56.0、0.0，平均 46.9。按平均分计算，作者报告 Mimir 相对 HRM-Text 提升 36.7%；Mimir 的 64.1 也高于 Qwen 3.5 2B 的 59.0，但低于 SmolLM3 3B 的 67.9。

</div>

核心变化是 HumanEval 从 HRM-Text 的 0.0 提升到 56.7，同时 GSM8K 也提高，但 MATH 从 56.0 降至 45.8，说明收益并非覆盖所有推理类型。36.7% 是套件平均分的相对提升，不是每项任务都提升 36.7%；该结果证明 Mimir 的综合数学与代码能力更平衡，却不能证明其数学能力整体超过 HRM-Text 或所有更大模型。

<div class="result-source" markdown="1">

来源：表 8，Math & Code benchmark results；第 5 节 Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Mimir 1B | 89.9 | 45.8 | 56.7 | 64.1

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 丹麦语 10 项零样本基准，与 1B 至 9B 模型进行跨规模比较

<div class="result-value" markdown="1">

Mimir 1B 的丹麦语平均分为 56.8，是表中最高值，明显高于 HRM-Text 1B 的 21.7、Qwen 3.5 4B 的 49.2、Gemma 4 E2B 思考模式的 49.9，以及三个 8–9B Munin 模型的 43.9–45.6。Mimir 在 DaLA、GEC 和 WikiQA 上分别达到 96.1、85.6 和 66.8。

</div>

作者据此声称 Mimir 在丹麦语上达到新的最佳水平，尤其优势集中在语法判断、语法纠错和问答任务。分析上，这表明针对许可数据进行的多数据集训练能让 1B 模型在丹麦语上胜过多个更大通用模型；但 Mimir 并非每项都最佳，例如 PIQA、Daisy、WMT、IFEval 和 Hellaswag-da 均有其他模型得分更高，所以结论应限定为该套件的平均表现和若干任务，而不是所有丹麦语能力。

<div class="result-source" markdown="1">

来源：表 9，Danish benchmark results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Mimir 1B | 67.4 | 96.1 | 85.6 | 53.7 | 9.6 | 66.8 | 53.9 | 35.87 | 63.9 | 35.3 | 56.8

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验章节没有提供训练数据混合、HRM 架构组件、许可数据筛选或后训练阶段的消融实验，因此无法隔离性能提升究竟来自数据规模与组成、训练策略还是模型架构；与 HRM-Text 的结果差异只能视为整体系统比较。
- 三个套件的平均分直接汇总不同任务与不同指标，且实验仅使用单一固定种子和贪心解码，未报告重复运行的方差、置信区间或显著性检验。Gemma 4 思考模式还使用约 500–650 个额外推理 token，因此跨模型分数比较并未完全控制推理计算预算。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- HRM-Text 1B：与 Mimir 参数规模和 HRM 架构背景最接近，是判断新训练数据与训练方案是否相对原始模型带来增益的核心对照。
- Qwen 3.5 系列，包括 0.8B、2B 和 4B：同时提供近似规模与更大规模参照，可判断 Mimir 的竞争力是否仅来自参数量，并用于衡量其与前沿较大模型的差距。
- Gemma 系列，包括 Gemma 3 1B 和 Gemma 4 E2B：前者是同量级对照，后者总参数约 5B、有效参数 2.3B，且分别测试非思考与思考模式，用于比较常规生成和额外推理计算下的表现。
- OLMo 2 1B 与 SmolLM3 3B：OLMo 2 提供另一同规模开放模型参照；SmolLM3 代表表现较强的 2–3B 常规语言模型，尤其用于判断 Mimir 在数学与代码套件上能否接近更大模型。

**实验想回答的问题**

- 在统一、可复现的评测协议下，仅使用许可后训练数据训练的 Mimir 1B，能否在英语、数学与代码、丹麦语三类能力上超过同参数量模型，并接近参数量更大的强基线？
- Mimir 相对原始 HRM-Text 1B 的提升体现在哪些任务类型上，尤其是否弥补了代码生成和丹麦语能力的明显短板？

**实验实现**

所有基准均在完整数据集上评测，采用温度 $0$ 的贪心解码和固定 shuffle seed $4242$。部分英语任务按照既有评测配置使用少样本提示，全部丹麦语任务均为零样本；选择题任务设置 $max\_tokens=1$，其他非选择题以及启用推理时设置 $max\_tokens=2048$。基线通过 Inspect AI Framework 评测并由 vLLM 提供服务；Mimir 因 PrefixLM 机制需要 FlashAttention。作者还用 vLLM/FlashAttention4 与 Hugging Face Transformers 交叉运行，称结果在数值稳定性范围内可比，最终为便于复现报告 Transformers 结果。Gemma 4 分别测试非思考和思考模式，思考模式先移除推理 token 再评分，约消耗 500–650 个 token。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The central contribution is a language-model training and data recipe that produces a competitive 1B-parameter model using permissibly sourced data.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`887c1cf060c6c3d872b6347c78b8d4f93fbcada7f26efd0fae29170745069e14`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
