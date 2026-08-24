---
title: "[论文解读] Memory Augmentation Unlocks Efficient Chain-of-Thought Reasoning"
description: "[arXiv 2608.21265][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.21265"
announcement_date: "2026-08-24"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-24T02:08:52.539559+00:00"
source_sha256: "a2fbf9e4c50a44b4bc4b3fe5423ae8c194f51415a99e2fbf87112b8d6e621d8e"
tags:
  - "LLM Reasoning"
  - "LLM 效率"
  - "LLM 其他"
  - "大语言模型"
  - "链式思维推理"
  - "CoT压缩"
  - "推理记忆"
  - "预填充—解码权衡"
  - "高效推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.21265</p>

# Memory Augmentation Unlocks Efficient Chain-of-Thought Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Simeng Zhang, Yilong Chen, Wenyuan Zhang, Zhenyu Zhang, Yao Chen, Junyuan Shang, Tingwen Liu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Institute of Information Engineering, Chinese Academy of Sciences；Affiliation: School of Cyber Security, University of Chinese Academy of Sciences；Affiliation: Baidu Inc. Tencent Inc.{ zhangsimeng, chenyilong</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.21265v1) · [PDF 下载](https://arxiv.org/pdf/2608.21265v1) · **关键词** 大语言模型, 链式思维推理, CoT压缩, 推理记忆, 预填充—解码权衡, 高效推理<br>


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

本文属于大语言模型高效推理与链式思维（Chain-of-Thought，CoT）压缩研究。CoT通过生成中间推理步骤来提升复杂任务的回答准确率，但这些步骤以自回归方式逐个生成，推理链越长，解码延迟、令牌消耗和服务开销越高。本文关注的核心问题是：在不恢复长推理链的前提下，能否把部分原本需要在解码阶段生成的推理支持转移到输入上下文的预填充阶段，从而兼顾准确率与推理效率。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**链式思维（CoT）**

CoT让模型先生成中间推理序列，再根据该序列输出最终答案，而不是直接从问题生成答案。中间步骤通常包含子目标、约束和推导过程，因此可能提高复杂问题的可解性，但也会增加生成长度。

</div>
<div class="concept-item" markdown="1">

**自回归解码与预填充**

自回归解码按顺序逐个生成输出令牌，后一个令牌依赖前面已经生成的内容，因此长推理链会带来串行延迟。预填充则是模型并行处理已有输入上下文的阶段，本文利用其相对更强的并行性承载额外推理记忆。

</div>
<div class="concept-item" markdown="1">

**CoT压缩**

CoT压缩通过删减、跳过或概括推理令牌和推理步骤来缩短生成过程。压缩过强时，可能同时删除问题求解所需的子目标、关键约束或逻辑依赖，导致准确率下降。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定系统指令与用户查询的拼接输入 $\mathbf{x}=(\mathcal{I},q)$，模型 $\mathcal{M}_{\theta}$需要输出最终答案 $y$。标准CoT先生成中间推理序列 $z$，其联合概率分解为 $P_{\theta}(y,z\mid\mathbf{x})=P_{\theta}(z\mid\mathbf{x})P_{\theta}(y\mid\mathbf{x},z)$；本文假设完整的 $z$ 可以被压缩为更短的推理链 $z^{\prime}$，但压缩可能损失有用信息。为补偿这种损失，系统从历史推理轨迹构建外部记忆库 $\mathcal{C}$，针对新输入检索记忆 $M$，并将其加入预填充上下文，使模型在较短的 $z^{\prime}$ 下生成答案。本文聚焦检索后的预填充—解码权衡，明确说明其延迟分析不计入记忆检索成本。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{M}_{\theta}$**

参数为 $\theta$ 的大语言模型。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{x}=(\mathcal{I},q)$**

模型输入，由系统指令 $\mathcal{I}$ 与用户查询 $q$ 拼接而成。

</div>
<div class="notation-item" markdown="1">

**$z$**

标准CoT生成的完整中间推理序列；其长度决定主要的自回归解码负担。

</div>
<div class="notation-item" markdown="1">

**$M=\phi(\mathbf{x},\mathcal{C})$**

由检索函数 $\phi$ 根据输入 $\mathbf{x}$ 和记忆库 $\mathcal{C}$ 得到的结构化推理记忆 $M$。

</div>

</div>

**直接相关的工作**

- **标准链式思维提示（CoT prompting）**: CoT通过显式生成中间推理步骤提升复杂任务表现，但其长推理序列需要逐令牌自回归解码，形成本文所要缓解的延迟与成本瓶颈。
- **CoT压缩方法，包括语义级缩短、令牌剪枝或跳过、推理轨迹压缩和推理状态压缩**: 这些方法主要减少生成阶段产生或保留的推理信息；当压缩较为激进时，可能删除子目标、关键约束和逻辑依赖。本文不直接替代压缩器，而是增加一个可插拔的记忆补偿层，把相关推理支撑放入预填充上下文，并声称可与多种压缩机制组合。

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

Memory-Augmented Compression（MAC）是一个无需额外训练的推理框架，目标是在保持复杂推理准确率的同时，减少自回归生成的推理长度。给定系统指令与问题 $\mathbf{x}=(\mathcal{I},q)$，MAC 离线把历史推理轨迹提炼为可复用的结构化记忆，在线根据当前问题检索相关记忆 $M$，将其加入模型的预填充上下文，再生成较短的推理链 $z^{\prime}$ 和最终答案 $y$。其核心不是直接复制示例，而是用问题类型、约束、子目标、解题策略和关键操作构成紧凑的推理脚手架，以弥补压缩推理丢失的信息。直观地说，标准 CoT 要在答题时一步步重新搭建完整解题过程；MAC 先从过去经验中取出一张相关的“解题提纲”，让模型少生成一些中间步骤。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 离线构建记忆库

将每条完整推理示例转换为结构化记忆表示，提取问题类型、关键约束、子目标、解决策略和关键运算等可迁移信息，而不是原样保存输入—输出示例。所有记忆组成记忆库 $\mathcal{B}$。

<div class="method-step__io" markdown="1">

**输入**：历史上已经求解的问题、答案及其推理轨迹。<br>
**输出**：可供检索的结构化记忆库 $\mathcal{B}$。

</div>

**直观理解**：这一步把完整范例压缩成“这类题通常先做什么、必须注意哪些条件、最后执行什么关键操作”的提纲。这样在线输入的不是一整道旧题，而是可复用的解题结构。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 查询相关记忆

利用推理标签与语义相似度选择与当前问题具有相似解题结构的记忆，得到 $M_x=\mathcal{R}(x,\mathcal{B},k)$。该过程强调问题求解结构的相关性，而不只匹配表面词汇。

<div class="method-step__io" markdown="1">

**输入**：当前问题 $x$、记忆库 $\mathcal{B}$ 和检索数量 $k$。<br>
**输出**：当前问题对应的记忆集合 $M_x$，其中包含至多由 $k$ 控制数量的候选记忆。

</div>

**直观理解**：类似于先判断“这道题属于哪种题型”，再从题库中找几张相同解法的提纲。$k$ 太小可能覆盖不足，太大则可能引入无关或重复信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 记忆增强预填充

将记忆与系统提示和问题拼接，形成模型的预填充上下文；这些上下文 token 在预填充阶段并行处理，从而把部分原本需要解码生成的推理信息提前提供给模型。

<div class="method-step__io" markdown="1">

**输入**：系统提示、当前问题 $x$ 和检索得到的记忆 $M_x$。<br>
**输出**：记忆增强的输入上下文，供后续压缩推理使用。

</div>

**直观理解**：预填充相当于在正式作答前先把“解题提纲”放到草稿纸上。虽然会增加输入长度，但不需要像生成 token 那样逐个等待，因此通常比增加同等数量的自回归推理更便宜。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 压缩推理与回答

模型在记忆脚手架条件下生成较短的推理链 $z^{\prime}$，随后生成最终答案 $y$；理想情况下满足 $|z^{\prime}|\ll|z|$，同时保留必要的子目标、约束和关键操作。

<div class="method-step__io" markdown="1">

**输入**：记忆增强上下文和压缩配置，例如 CoD 或其他 token、推理轨迹级、推理状态级压缩机制。<br>
**输出**：压缩推理链 $z^{\prime}$、最终答案 $y$，以及相应的准确率和延迟结果。

</div>

**直观理解**：模型不必从零写完整草稿，而是依据提纲完成必要的短推理。记忆尤其用于防止激进压缩造成“逻辑坍塌”，例如算出总数后忘记执行最后的减法。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 上下文—生成替代关系

$$
M=\phi(\mathbf{x},\mathcal{C}),\qquad P_{\theta}(y\mid\mathbf{x},M)\approx P_{\theta}(y\mid\mathbf{x},z)
$$

**符号说明**

- $M$：从外部记忆源中检索或构造的结构化推理记忆。
- $\phi$：根据输入与记忆源执行记忆选择或构造的函数。
- $\mathbf{x}$：系统指令与用户问题的拼接输入，即 $\mathbf{x}=(\mathcal{I},q)$。
- $\mathcal{C}$：存储可复用推理信息的外部记忆源。
- $P_{\theta}$：参数为 $\theta$ 的语言模型条件概率。
- $y$：最终答案。
- $z$：标准 CoT 中通过自回归解码生成的完整推理链。

<div class="equation-explanation" markdown="1">

**直观理解**：该关系表达 MAC 的基本假设：如果检索到的记忆包含了与当前问题相关的推理结构，那么模型在记忆 $M$ 条件下生成答案的效果可以接近依赖完整推理链 $z$ 的效果。换言之，部分显式上下文可以替代部分昂贵的逐 token 推理生成。<br>
**原文位置**：第 2.3 节，公式（2）—（3）

</div>

</div>

<div class="equation-block" markdown="1">

#### 记忆增强后的延迟条件

$$
M\tau_{\mathrm{pre}}<D\tau_{\mathrm{dec}}
$$

**符号说明**

- $M$：新增记忆上下文的 token 数量。
- $\tau_{\mathrm{pre}}$：每个预填充 token 的平均处理延迟。
- $D$：因使用记忆而减少的解码 token 数量。
- $\tau_{\mathrm{dec}}$：每个自回归解码 token 的平均处理延迟。

<div class="equation-explanation" markdown="1">

**直观理解**：只有当新增记忆的预填充成本小于因此省下的解码成本时，记忆才带来净延迟收益。由于解码是串行的，通常 $\tau_{\mathrm{dec}}$ 大于 $\tau_{\mathrm{pre}}$，所以少生成一个解码 token 往往可以抵消多个新增输入 token 的成本。<br>
**原文位置**：第 3.3 节“Prefill–decode cost quantification”，公式（9）；相关推导见第 3.2 节公式（5）—（7）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：MAC 本身是 training-free 方法，原文未给出用于训练记忆模块或更新语言模型参数的损失函数，因此不存在需要在该框架中优化的新增训练目标。方法的“优化”发生在推理设计层面：通过选择记忆 $M$、控制检索数量 $k$ 和压缩推理长度 $|z^{\prime}|$，在准确率损失与预填充、解码成本之间取得平衡；论文在第 2.3 节用 $\mathcal{J}=|z^{\prime}|+\gamma|M|+\lambda\mathcal{L}_{\mathrm{perf}}$ 表示这一设计目标，其中 $\mathcal{L}_{\mathrm{perf}}$ 是压缩造成的性能惩罚，$\gamma=\tau_{\mathrm{pre}}/\tau_{\mathrm{dec}}$ 表示两类计算成本的相对权重。该目标是分析性形式化，而非报告中的训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 结构化记忆库**

记忆库 $\mathcal{B}$ 由历史推理示例离线构建，每条记忆保留可复用的推理信息，包括问题类型、关键约束、子目标、解题策略和关键操作。MAC 不直接注入原始 few-shot 输入—输出对，而是只序列化被选中的抽象记忆。

> 直观理解：原始示例往往包含具体题目中的大量细节，换题后不一定有用；结构化记忆保留的是解法骨架，因此更适合作为不同问题之间的提示。

**2. 结构感知检索器**

给定查询 $x$，检索器依据推理标签和语义相似度从 $\mathcal{B}$ 中选取记忆集合 $M_x=\mathcal{R}(x,\mathcal{B},k)$。检索规模 $k$ 控制覆盖范围与上下文噪声之间的权衡，实验显示增加 $k$ 会增加预填充长度，而准确率通常先提升后趋于饱和或下降。

> 直观理解：检索器不是只找“字面上相似”的题，而是尽量找“需要相同解题套路”的题。找得太少可能漏掉关键套路，找得太多则会让模型面对相互重复或不相关的提示。

**3. 记忆增强压缩推理**

记忆被拼接到系统提示和查询前形成预填充上下文，模型随后生成 Short-CoT $z^{\prime}$ 与答案 $y$。该框架是压缩器的插件，可与 TokenSkip、RPC、Extra-CoT 等 token 级、推理轨迹级或其他压缩机制结合，而不改变基础模型参数。

> 直观理解：MAC 不替换原有压缩算法，而是在压缩前提供额外的外部提示。它的作用类似给不同的速记方案补上一份结构提纲，使短推理仍保留关键逻辑。

**训练与推理**

离线阶段收集历史已解决推理样例，并将其提炼为结构化记忆，构成 $\mathcal{B}$；论文强调该阶段不需要对基础语言模型进行额外训练。在线阶段首先根据当前查询 $x$ 生成或获取查询标签与语义表示，再从 $\mathcal{B}$ 中检索 top-$k$ 相关记忆 $M_x$，将记忆、系统提示和查询拼接成预填充上下文，最后使用指定的压缩器生成 Short-CoT $z^{\prime}$ 和最终答案 $y$。完整端到端延迟可写为 $T_{\mathrm{e2e}}=T_{\mathrm{ret}}+T_{\mathrm{prefill}}+T_{\mathrm{decode}}$，其中 $T_{\mathrm{ret}}$ 包括查询标签生成、查询嵌入和向量搜索；因此只报告模型推理延迟可能低估在线检索开销。整体上，MAC 的关键改变是把可复用推理信息从解码阶段的动态工作记忆转移到预填充阶段的显式记忆，而不是改变模型的参数化推理能力。

**复现信息**

复现或公平解读时应区分三类成本：记忆检索后的模型预填充与解码成本、查询侧标签生成和嵌入成本、以及 top-$k$ 向量搜索成本。论文报告在 Qwen2.5-7B、NVIDIA H20 上，每个解码 token 相当于约 $14.7$—$87.0$ 个预填充 token 的延迟，具体取决于数据集和 batch size；但端到端检索中，GSM8K 的查询标签生成与嵌入共耗时 $683.0$ ms，而向量搜索仅耗时 $0.10$ ms，因此查询表示构建是主要在线开销。实验还需要明确压缩比参数 $\gamma$ 的含义：较小的 $\gamma$ 表示更激进的压缩；记忆数量 $k$ 增大通常提高预填充长度而使解码长度相对稳定，准确率存在覆盖收益与噪声成本的权衡。记忆格式也会影响效果：在 TokenSkip 上，Long-CoT 记忆通常比 Short-CoT 记忆更稳定，但 Extra-CoT 的结果表明记忆并非对所有压缩器和压缩强度都有效。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K 与 MATH：用于测试算术和数学推理。GSM8K 使用官方测试集，共 1,319 个样本；MATH 使用 MATH-500，共 500 个样本。两者的记忆库均由官方训练样本经过正确性、完整性和格式过滤后构建，且与评测样本相互独立；对应记忆库规模分别为 4,307 和 2,242。
- BBH：用于测试多种复杂、符号化推理能力。实验选取九个任务，共 495 个评测样本；记忆来自每个任务官方提供的三个 CoT 示例，共 27 条，并与评测集不重叠。
- MMLU Science 与 AIME 2024：前者用于科学问答，选取大学物理、高中物理、大学化学、高中化学、大学生物和高中生物六个学科，按学科分层抽取 20% 评测、80% 建库，评测集 79 个样本、记忆库 317 条；后者用于竞赛级数学推理，评测 2024 年官方 30 道题，记忆来自 1983—2022 年历史题，共 287 条。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（exact-match accuracy）**

衡量最终答案是否与标准答案一致。GSM8K、MATH 和 AIME 使用任务特定的答案解析与规范化；BBH 和 MMLU Science 比较选项标签；无法解析或格式错误的输出计为错误。 （越高越好，因为它直接表示任务解答正确的比例。）

</div>
<div class="metric-item" markdown="1">

**prefill、decode 与 total tokens**

分别衡量输入上下文处理阶段的 token 数、自回归生成阶段的 token 数，以及两者的总 token 数；记忆被计入输入 token，生成的推理和答案被计入输出 token。 （通常越低越省计算，但不能脱离准确率解释；MAC 可能增加 prefill tokens，却减少 decode tokens。）

</div>
<div class="metric-item" markdown="1">

**模型延迟与端到端延迟**

模型延迟包括 prefill 和 decode 时间；MAC 的端到端延迟还包括查询标签生成、编码、检索和提示构造时间。实验同时报告延迟及相对标准 CoT 的加速比。 （越低越好；端到端延迟比只测模型执行时间更能反映实际部署收益。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨任务的 CoD 与 CoD+Memory 比较：GSM8K、MATH、BBH 和 MMLU-Sci。

<div class="result-value" markdown="1">

作者报告，与 CoD 相比，CoD+Memory 在 GSM8K、MATH、BBH 和 MMLU-Sci 上的准确率分别提升 21.4、28.0、29.5 和 6.61 个百分点；同时在不同领域相对标准 CoT 达到 1.14—1.49 倍延迟加速。

</div>

这说明记忆能够补回短 CoD 轨迹中被省略的关键约束和操作，使准确率接近或超过标准 CoT，而不是简单地把完整推理重新生成一遍。结果支持“用部分输入上下文替代部分 decode 生成”的设计，但不能据此证明所有任务、模型或检索器都必然获得相同幅度的收益；尤其检索开销需要单独计入。

<div class="result-source" markdown="1">

来源：第 4.2 节 Main Results，General evaluation across domains；延迟范围见同节 Accuracy–latency trade-off

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Adding Memory consistently recovers performance, improving over CoD by 21.4, 28.0, 29.5, and 6.61 points on GSM8K, MATH, BBH, and MMLU-Sci, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 准确率—延迟权衡：标准 CoT、CoD 与 CoD+Memory。

<div class="result-value" markdown="1">

MAC 增加 prefill tokens，但相较标准 CoT 减少 decode-side reasoning，并报告在各领域达到 1.14—1.49 倍延迟加速；把检索开销加入后，作者仍称 MAC 在各数据集上端到端快于 CoT。

</div>

该比较检验的不是“总 token 越少越好”，而是 prefill 和 decode 的成本是否可以有效替代。MAC 把一部分可复用推理放入输入侧，换取更短的在线生成过程；因此其实际优势依赖硬件和服务系统对 prefill、decode 速度的相对支持。作者的端到端结论比只排除检索开销的模型延迟更有部署意义。

<div class="result-source" markdown="1">

来源：第 4.2 节 Main Results，Accuracy–latency trade-off；端到端延迟定义见附录 B.6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

When the retrieval overhead is added back, MAC still remains faster than CoT end-to-end across datasets (full breakdown in Appendix).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨压缩机制的即插即用比较：TokenSkip、RPC 和 Extra-CoT 的 Base 与 +Memory。

<div class="result-value" markdown="1">

在保持模型、数据集、压缩设置和解码设置相同、只增加记忆注入的配对实验中，Memory 在不同压缩比例和模型上的 TokenSkip 上均带来提升，并且与 RPC、Extra-CoT 结合时也获得正向收益。

</div>

这表明记忆模块补偿的是“压缩造成的推理信息损失”，而不是只针对 CoD 的特定提示格式。由于这些方法同时包含训练式和训练无关式压缩，结果支持 MAC 的方法兼容性。不过，给出的摘录未提供各个组合的完整数值，因此不能判断哪一种压缩方法或压缩比例最受益。

<div class="result-source" markdown="1">

来源：第 4.2 节 Main Results，Plug-in compatibility；完整结果见附录 C.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Memory augmentation improves TokenSkip across different compression ratios and models, and also yields positive gains with RPC and Extra-CoT.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验依赖与评测集分离的历史或训练样本构建记忆库；虽然作者明确排除了评测样本以防数据泄漏，但摘录未充分说明记忆库质量、领域迁移和检索失败时的表现，因此跨分布泛化仍需更多验证。
- 作者报告了若干总体准确率增益和延迟加速，但所给章节摘录缺少完整表格、方差或显著性分析；部分 API 模型也无法分别测量 prefill 与 decode 延迟。因此不能仅凭这些结果判断收益的统计稳定性或在不同服务商成本模型下的实际优势。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 标准 CoT：要求模型生成不受严格长度约束的逐步推理，是准确率和完整推理上下文的参照。
- CoD：要求每个中间推理步骤最多五个词，是主要的提示式推理压缩基线，用于检验 MAC 是否能恢复激进压缩丢失的信息。
- TokenSkip：训练式压缩方法，用于测试 MAC 是否能与不同压缩比例结合，而不是只对 CoD 有效。
- RPC 与 Extra-CoT：分别代表训练无关和训练式的其他压缩机制；它们用于检验 MAC 的跨方法兼容性。

**实验想回答的问题**

- 在数学、复杂推理和科学问答等不同任务上，向压缩推理提示中加入可检索的推理记忆，能否弥补 Chain-of-Draft（CoD）因删减中间步骤造成的准确率损失，同时保留其推理加速优势？
- Memory-Augmented Compression（MAC）是否能够作为独立于具体压缩算法的即插即用补偿模块，并且其收益是否来自相关推理信息，而非单纯增加输入上下文长度？

**实验实现**

主要使用指令微调的 LLaMA-3.1-8B 和 Qwen2.5-7B，并额外测试 Qwen2.5-72B 及三个 API 推理模型。所有模型均不更新参数。对每个评测输入，系统根据当前问题生成查询标签，用同一嵌入模型编码后检索 top-$k$ 条相关记忆，并把记忆作为 prefill 侧脚手架注入原压缩提示；记忆库的构建、标签生成和索引建立均在线下完成。默认开放权重模型采用贪心解码，温度为 $T=0$、$p_{m top}=1.0$；成对比较时，基线与“+Memory”使用相同模型、压缩指令、最大生成长度、硬件、批大小、张量并行和服务配置，因此加入记忆不会额外获得 decode token 预算。主要报告准确率、prefill/decode/total tokens 和延迟；延迟通常在 batch size 为 1 时测量，并补充 batch size 为 8 的结果。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Qwen2.5-72B 上的模型规模扩展：MATH-500 中比较 CoT、CoD 与 CoD+Memory。 | 作者报告，CoD 相比完整 CoT 显著减少 decode length 和延迟，但造成明显准确率下降；加入检索推理记忆后，准确率得到恢复并略微超过完整 CoT，同时仍明显快于完整 CoT。摘录中的具体 token 数在句子末尾被截断，原文未明确报告完整数值。 | 这是对模型规模鲁棒性的验证：如果较大模型仍从外部推理记忆获益，说明该方法并非只弥补小模型能力不足。它支持“记忆增强压缩”在更大模型上仍有价值，但单一的 MATH-500 设置不能证明跨规模、跨任务的普遍规律。 | 附录 C.1 Model Scaling，Scaling to Qwen2.5-72B；表 8<br><span class="experiment-evidence">Adding retrieved reasoning memories recovers and slightly surpasses the full-CoT accuracy, while remaining considerably faster than full CoT.</span> |
| 检索与记忆设计的消融：比较无记忆、随机记忆与基于相关性的检索，并分析记忆数量与记忆格式。 | 摘录提供了表格片段：No Memory（CoD）准确率为 43.00%，Random 为 50.20%；同时说明检索规模 $k$ 在 $1,3,5,8,10,12,14,16,18,20$ 中变化，并比较 Long-CoT、Short-CoT 和 Summary 三种记忆格式。其余完整数值和最优设置在所给摘录中未呈现，原文未明确报告。 | 随机记忆相对无记忆的变化只能说明增加某些上下文可能有帮助，不能单独证明语义相关性是全部收益来源；必须结合完整的相关检索、长度匹配和格式消融表判断。$k$ 与格式实验分别检验“需要多少条记忆”和“记忆应保留哪些信息”，可区分检索数量效应与推理内容效应。 | 第 4.2 节 Main Results 后的检索器对比表片段；完整检索规模与记忆格式设置见附录 B.4，完整结果位置原文未明确报告<br><span class="experiment-evidence">No Memory (CoD) 43.00 –</span> |

**定性案例**

- 原文摘录未提供具体样例、问题—记忆匹配过程或逐步输出的定性案例，因此无法据此判断某条记忆如何改变模型的错误推理；只能确认作者将记忆解释为包含可复用推理模式、关键约束和关键操作的 prefill 侧脚手架。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper improves chain-of-thought reasoning through retrieved reasoning memories while centrally reducing generation length and inference latency.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`a2fbf9e4c50a44b4bc4b3fe5423ae8c194f51415a99e2fbf87112b8d6e621d8e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
