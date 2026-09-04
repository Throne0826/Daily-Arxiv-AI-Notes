---
title: "[论文解读] ToolDF: Tool-Integrated Reasoning for Mixed-Authenticity Audio Deepfake Detection"
description: "[arXiv 2609.03620][LLM Agent] 原文未明确报告。"
arxiv_id: "2609.03620"
announcement_date: "2026-09-04"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:41:28.610479+00:00"
source_sha256: "1a4dd7361054b6ee1ecdaaef1facee8f42bca6e23a4c47a2751fbfbe9dfed977"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "音频深度伪造检测"
  - "混合真实性音频"
  - "声源分离"
  - "音频大语言模型"
  - "工具集成推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2609.03620</p>

# ToolDF: Tool-Integrated Reasoning for Mixed-Authenticity Audio Deepfake Detection

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Taewoo Kim, Young Han Lee, Nam In Park, Chanwoo Kim</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Multi-Modal Research Center, KETI, South Korea；Affiliation: Department of Artificial Intelligence, Korea University, South Korea</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03620v1) · [PDF 下载](https://arxiv.org/pdf/2609.03620v1) · **关键词** 音频深度伪造检测, 混合真实性音频, 声源分离, 音频大语言模型, 工具集成推理<br>
**代码**: [https://github.com/rlataewoo/tooldf](https://github.com/rlataewoo/tooldf)

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

音频深度伪造检测（Audio Deepfake Detection，ADD）旨在判断音频是否包含由合成、转换或其他操纵产生的伪造内容。现有研究通常将任务建模为整段音频的二分类：输入来自单一主导声学领域的音频片段，输出一个“真实”或“伪造”标签；研究对象已从语音扩展到歌唱、音乐和环境声音。本文关注这一设定在真实复杂场景中的不足：同一输入可能同时包含真实与伪造线索，且这些线索可能沿时间交替出现，也可能存在于相互重叠的声源中。因此，系统不仅需要判断整体是否被操纵，还需要定位支持判断的时间片段或声学来源。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**混合真实性音频**

混合真实性音频是指同一段输入中同时存在真实和伪造内容。例如，音频可能先播放真实语音、后切换为合成歌唱，或将伪造人声叠加在真实背景音乐上。

</div>
<div class="concept-item" markdown="1">

**声源分离**

声源分离是将混合录音拆解为较独立的组成来源，例如把人声与背景音乐分开。它有助于分别检查各个来源的真实性，但在不需要分离的单一声源输入上也可能引入音频伪影。

</div>
<div class="concept-item" markdown="1">

**音频大语言模型与工具集成推理**

音频大语言模型（ALLM）能够理解包含语音、音乐或环境声音的音频；工具集成推理则不让模型直接充当唯一分类器，而是让它分析输入结构、调用专门检测器，并综合工具返回的证据。本文把 ALLM 定位为负责规划和协调的编排器，而不是直接给出黑箱式二分类结果的模型。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文提出混合真实性音频深度伪造检测任务。输入是一段可能包含一种或多种声学领域（语音、歌唱、音乐、环境声音）的音频 $x$；其内部可能存在不同的真实性状态，例如时间上的真实—伪造转换、同时重叠的真实与伪造声源，或二者的组合。系统需要输出整体真实性判断 $y$，并提供与判断相关的证据定位，包括被怀疑的时间区域、声学来源及相应专家检测结果。该任务不再假设每个片段只有一个主导领域或只有一种真实性状态，而是要求模型先分析音频结构，再决定是否需要声源分离，并将不同组成部分路由给匹配的领域专家。最终输出应当既能支持整体检测，也能解释哪些局部组成部分导致该结论。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入的整段音频片段。

</div>
<div class="notation-item" markdown="1">

**$y$**

输入音频的整体真实性判断，例如真实或伪造；论文摘要和引言将该结果描述为最终 authenticity decision。

</div>
<div class="notation-item" markdown="1">

**$t$**

音频中的时间位置或时间片段，用于表示局部操纵发生的 temporal region。

</div>
<div class="notation-item" markdown="1">

**$c$**

音频中的声学组成部分或声源，例如语音、歌唱、音乐或环境声音；在发生重叠时，它可以对应声源分离后的局部来源。

</div>

</div>

**直接相关的工作**

- **Zang et al. (2024b) 的复合音频 ADD 方法**: 该工作代表了通过声源分离处理复合音频的固定流程：对所有输入先执行分离，再进行检测。论文指出，这种做法虽然有助于隔离重叠声源中的伪造线索，但对本来不需要分离的单一声源也可能产生不必要的伪影。ToolDF 的差异在于先分析音频结构，仅在识别出重叠来源时调用 source_separator，并进一步覆盖多个声学领域，而不是只依赖固定预处理。
- **Zhang et al. (2026) 的自适应分离框架**: 该工作已经能够在检测到重叠声源时自适应触发声源分离，解决了固定分离流程缺乏灵活性的问题；但其后续检测范围仍限于语音领域，无法系统识别歌唱、音乐或环境背景中的合成成分。ToolDF 在此基础上扩大了专家检测范围，并由 ALLM 编排器统一完成结构分析、工具选择和证据聚合。

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

ToolDF 将混合真实性音频深度伪造检测建模为结构化的工具集成推理过程，而不是直接对整段音频进行二分类。给定音频片段 $x$，音频大语言模型（ALLM）首先分析其中的声学组成，识别语音、歌声、音乐或环境声音等组件及其时间范围；随后根据组件类型和重叠情况制定工具调用计划，必要时先进行声源分离，再将局部片段送入相应的领域专家检测器；最后汇总各组件的真实性证据，并依据“任一组件为伪造则整段为伪造”的 early-fail 规则输出片段级结论。直观地说，ToolDF 不是只听整段录音后给出一个黑箱答案，而是先回答“里面有哪些声音、分别在哪里”，再让专门的检测器逐一检查，最后说明哪个局部证据导致了结论。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 音频场景理解

ALLM 生成结构化的音频理解块，识别组件集合 $\mathcal{C}(x)=\{c_1,\ldots,c_K\}$。每个组件被赋予内容类型 $t_k\in\{\texttt{speech},\texttt{singing},\texttt{music},\texttt{sound}\}$ 和支持区域 $\rho_k$；时间组件用起止时刻 $(s_k,e_k)$ 表示。

<div class="method-step__io" markdown="1">

**输入**：输入音频片段 $x$ 及文本指令上下文 $q$。<br>
**输出**：组件列表、每个组件的内容类型，以及相应的时间区域或混合声源区域。

</div>

**直观理解**：这一步类似于先给录音做“场景分层”：系统判断何时出现语音、歌声或背景声，而不是把整段音频视为一种声音。这样后续检测器可以只检查与自身领域匹配的局部内容。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 工具使用规划

ALLM 生成条件化的工具调用计划：若人声与背景声重叠，则优先调用声源分离器；之后依据 $t_k$ 将组件路由至语音、歌声、音乐或环境声音深度伪造检测器，并指定待分析的局部区域。

<div class="method-step__io" markdown="1">

**输入**：音频组件集合 $\mathcal{C}(x)$、组件类型 $t_k$、支持区域 $\rho_k$ 及其可能的时间重叠关系。<br>
**输出**：有顺序的工具使用计划，包括待调用的工具、输入声源或音频路径，以及起止时间等参数。

</div>

**直观理解**：系统像一个调度员：先判断是否需要把混在一起的声音拆开，再把语音交给语音专家、歌声交给歌声专家。工具不是固定全部调用，而是根据当前音频场景选择。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 局部工具执行

执行声源分离及领域专家检测器。每个检测器针对指定组件或支持区域输出组件级真实性预测 $\hat{y}_k$；工具响应还可以提供真实性分数等证据。

<div class="method-step__io" markdown="1">

**输入**：规划中的工具调用参数，包括原始或分离后的音频、目标时间区间和内容类型。<br>
**输出**：一组组件级预测、分数及其对应的时间区域或声源身份。

</div>

**直观理解**：这一步相当于让多个专科医生分别检查不同部分：每个专家只负责自己擅长的声音类型，因此不会完全依赖整段混合音频中的平均特征。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 证据汇总与片段判定

ALLM 将组件级结果整理为证据描述，并按 early-fail 规则聚合：若至少一个组件预测为伪造，则输出片段级标签 $\hat{y}=\texttt{fake}$；否则输出 $\hat{y}=\texttt{real}$。

<div class="method-step__io" markdown="1">

**输入**：所有组件级工具响应 $\{\hat{y}_k\}$、对应区域 $\rho_k$ 和工具证据。<br>
**输出**：可解释的组件级证据摘要和最终片段级真实性 verdict。

</div>

**直观理解**：最终答案不仅告诉用户“真”或“假”，还指出哪个时间段或哪个声源被判断为伪造。规则强调安全优先：只要混合录音中存在一个伪造组件，整段就不能被判为完全真实。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 混合真实性的片段级 early-fail 判定

$$
y=\texttt{fake}\Longleftrightarrow\exists c_k\in\mathcal{C}(x)\;\text{s.t.}\;y_k=\texttt{fake}
$$

**符号说明**

- $x$：输入音频片段
- $\mathcal{C}(x)$：音频片段 $x$ 中的组件集合
- $c_k$：第 $k$ 个异质声学组件
- $y_k$：组件 $c_k$ 的真实性标签，取值为 real 或 fake
- $y$：整段音频的片段级真实性标签

<div class="equation-explanation" markdown="1">

**直观理解**：该规则把组件级判断转换为整段判断：只要存在一个组件被标记为 fake，整段音频就标记为 fake；只有所有组件都为 real 时，整段才为 real。它对应论文对混合真实性风险的定义，而不是普通单域任务中对整段音频使用的单一标签假设。<br>
**原文位置**：Section 3.1, Task Formulation

</div>

</div>

<div class="equation-block" markdown="1">

#### 监督式轨迹学习目标

$$
\mathcal{L}_{\mathrm{SFT}}=-\sum_{m\in\mathcal{M}}\log P_{\theta}\left(o_m\mid o_{<m},x,q\right)
$$

**符号说明**

- $\mathcal{L}_{\mathrm{SFT}}$：监督式微调损失
- $\mathcal{M}$：轨迹中由编排器生成的 token 位置集合，不包括工具观察 token
- $o_m$：目标轨迹第 $m$ 个位置的 token
- $o_{<m}$：第 $m$ 个 token 之前的轨迹 token
- $P_\theta$：参数为 $\theta$ 的 ALLM 对下一个 token 的条件概率分布
- $x$：输入音频片段
- $q$：文本指令上下文

<div class="equation-explanation" markdown="1">

**直观理解**：模型通过最大化正确结构化轨迹中各个编排器 token 的概率来学习：先正确描述音频，再规划工具、总结证据并给出答案。工具返回的 observation token 被当作外部条件输入而不是模型需要模仿的输出，因此训练重点是学习如何使用和组织工具，而不是伪造工具响应。<br>
**原文位置**：Section 3.3, Supervised Trajectory Learning

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：ToolDF 使用监督式微调（SFT）训练 ALLM 遵循结构化工具集成推理协议。训练样本由组件真值注释 $\mathcal{S}^{\star}=\{(\rho_k,t_k,y_k)\}_{k=1}^{K}$ 构造：这些注释用于生成音频理解块、工具计划和局部工具调用；工具观察则使用组件真实性标签填充，并作为后续轨迹生成的条件上下文。模型优化目标是最小化 $\mathcal{L}_{\mathrm{SFT}}$，只对音频理解 $u$、工具计划 $p$、工具调用参数 $a_i$、证据摘要 $d$ 和最终标签 $y$ 对应的 token 计算损失，不对工具观察 $r_i$ 计算损失。直观上，监督信号教会编排器“如何拆解问题和调用工具”，而不是让它把专家检测器的内部判断重新学成一个黑箱分类器。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 音频大语言模型编排器**

ALLM 负责生成结构化推理轨迹 $o=\langle u,p,\mathcal{T},d,y\rangle$，其中 $u$ 是音频理解块，$p$ 是工具计划，$\mathcal{T}$ 是工具调用及响应序列，$d$ 是证据摘要，$y$ 是最终片段级标签。它连接场景分析、工具选择、工具参数生成和结果汇总，而不是直接替代所有领域检测器。

> 直观理解：它的核心作用是“理解并组织工作”：决定该检查什么、用哪个专家、检查哪一段，以及如何把分散的检查结果合成为结论。

**2. 声源分离与领域专家工具**

当不同声源在时间上重叠时，规划器调用 source separator，将混合音频分为例如 vocals 和 background；随后根据内容类型调用 speech、singing、music 或 sound deepfake detector，并在指定时间区域执行。

> 直观理解：混合声音会互相干扰，先拆分可以让检测器看得更清楚。领域专家则利用各类声音自身的伪造线索，避免一个统一检测器处理所有声学类型。

**3. 结构化证据聚合器**

ALLM 将工具返回的组件级预测和分数写入 evidence summary，并依据组件级标签执行 early-fail 聚合。训练时，工具响应作为条件上下文提供给后续生成，但响应 token 不计入编排器的语言建模损失。

> 直观理解：该模块把多个局部检查结果变成一份可追溯的报告，并明确哪个局部判断影响了最终答案。这样既得到片段级检测，也保留定位证据。

**训练与推理**

训练阶段，首先依据每个音频样本的组件区域、内容类型和真实性标签构造完整轨迹 $o=\langle u,p,\mathcal{T},d,y\rangle$；其中轨迹包含理解、规划、工具调用、工具响应、证据摘要和最终判定。工具响应由组件真值标签填充，ALLM 采用 teacher-forcing 方式根据前序 token、音频 $x$ 和指令 $q$ 预测编排器输出 token，并按照 $[1m\mathcal{L}_{\mathrm{SFT}}$ 优化参数 $\theta$。

推理阶段，输入新的音频片段后，ALLM 先生成场景理解，再根据组件类型及重叠关系生成工具计划；若需要则执行声源分离，随后以指定时间区域或分离声源调用相应领域检测器。ALLM 接收工具响应后生成证据摘要，并将组件级预测按 early-fail 规则聚合为最终 real/fake 标签，同时保留局部时间区域和声源证据。其关键区别是工具调用具有条件性和局部性：系统不会默认对所有音频使用同一固定处理链。

**复现信息**

复现或公平理解方法所必需的结构信息包括：组件类型覆盖 speech、singing、music 和 sound；时间局部组件用 onset-offset 区间 $(s_k,e_k)$ 表示，非时间局部组件用声源特定区域表示；工具调用需要显式指定工具名称、音频路径或分离声源，以及局部起止时间。论文给出的示例中，重叠的人声和背景声先经过 source_separator，再分别调用 speech_deepfake_detector、singing_deepfake_detector 和 sound_deepfake_detector。

训练数据轨迹依赖组件级真值注释，且工具观察不参与 ALLM 的 SFT token 损失。现有摘录未明确报告 ALLM 的具体基础模型、各专家检测器和声源分离器的模型架构、优化器、学习率、训练轮数或推理解码设置；这些细节不能依据当前章节补充。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 混合真实性音频深度伪造检测基准：由多个公开语料库的真实与合成子集构成，总计 973,649 个样本，其中复合类型样本为 379,900 个。数据覆盖 speech、singing、music 和 environmental sound 四类音频，用于同时评估传统单类型检测和混合真实性检测。该规模与总量信息见 Appendix A.3。
- 单类型评测集：采用 ASVspoof2019（speech）、CtrSVDD（singing）、FakeMusicCaps 与 MusicCaps（music）以及 EnvSDD（environmental sound）的官方训练、开发和测试划分，检验模型在各声学领域中的常规音频深度伪造检测能力。MusicCaps 因部分原始真实音频无法获取而作了防止数据泄漏的特殊处理；可获取的 MusicCaps 与 FakeMusicCaps 样本按 6:2:2 划分。
- 复合类型评测集：C1 为 speech→singing 或 singing→speech 的时间转换，C2 为 vocal foreground 与 music 或 environmental sound 的声学重叠，C3 为时间转换和背景重叠的混合场景。每个复合样本继承组件的时间支持区域与真实性标签，并按“任一组件为伪造则整段为伪造”的 early-fail 规则生成片段标签，用于测试局部操纵和多源证据聚合。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Macro-F1**

分别计算 real 与 fake 两个类别的 F1，再等权平均；它衡量模型是否同时识别真实和伪造样本，而不是只偏向数量较多的类别。 （越高越好，因为更高表示两类的精确率与召回率整体更平衡。）

</div>
<div class="metric-item" markdown="1">

**解析率 PR**

输出符合规定 ToolDF 轨迹格式的比例，规定格式包含音频理解、工具调用计划、工具结果描述和最终答案等结构。 （越高越好，因为不可解析的输出无法可靠执行后续评测或提供结构化证据。）

</div>
<div class="metric-item" markdown="1">

**定位 F1**

在 segment-level 或 event-level 上评估模型是否找到了正确的时间区域或声学组件；micro averaging 按实例汇总，macro averaging 则平等对待不同类型。 （越高越好，因为它表示局部操纵或提供证据的组件定位更准确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 复合类型总体检测：ToolDF 对比单体模型和 Fixed Pipeline

<div class="result-value" markdown="1">

ToolDF 的复合类型平均 Macro-F1（C-Avg.）为 81.89%，高于最强端到端单体基线 XLSR-AASIST 的 78.17%，也高于 Fixed Pipeline 的 67.50%；相对二者分别提升 3.72 和 14.39 个百分点。ToolDF Oracle 为 82.85%，说明已知正确工具路由时仍有小幅上限空间。

</div>

这表明在同时存在不同真实性组件时，动态选择是否分离、选择何种领域专家并聚合证据，比始终采用一个整体分类器或对所有输入强制分离更有效。结果支持 ToolDF 的整体设计，但不能单独证明每一次工具选择都正确，也不能说明其在未覆盖的声学类型或真实录音条件下必然保持优势。

<div class="result-source" markdown="1">

来源：Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ToolDF (Proposed) ✓ 95.78 81.58 76.13 92.67 86.54 91.21 77.66 76.81 81.89

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 不同复合结构下的检测能力

<div class="result-value" markdown="1">

ToolDF 在 C1 时间转换、C2 声学重叠和 C3 时间转换加重叠上的 Macro-F1 分别为 91.21%、77.66% 和 76.81%。性能从 C1 降至 C2/C3，说明声源同时叠加时比单纯的时间切换更困难，而 C3 是最复杂的组合场景。

</div>

ToolDF 对时间上先后出现的 speech 与 singing 较容易定位和判断；当 vocal 与背景 music 或 environmental sound 重叠时，模型还必须区分来源并处理分离误差，因此性能下降。C3 的结果说明该方法能够处理复杂混合，但也揭示声源重叠仍是主要难点，不能把较高的总体平均分解读为所有子场景同样可靠。

<div class="result-source" markdown="1">

来源：Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ToolDF (Proposed) ✓ 95.78 81.58 76.13 92.67 86.54 91.21 77.66 76.81 81.89

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 组件与事件的细粒度证据定位

<div class="result-value" markdown="1">

ToolDF 的定位性能在单类型 Speech、Singing、Sound、Music 上的 Seg-F1 macro 分别为 98.18%、97.74%、99.97% 和 99.89%；在复合类型 C1、C2、C3 上分别为 97.34%、96.11% 和 93.63%。对应 Event-F1 macro 在 C1、C2、C3 上为 94.24%、91.96% 和 87.62%。

</div>

这些结果说明模型不仅给出片段级 real/fake 判断，还能较准确地指出相关时间区间或声学组件。复合结构越复杂，尤其是同时包含时间变化与重叠时，事件级定位下降更明显；因此解释性证据是有量化支持的，但并不等于每条自然语言描述都经过人工逐条验证。

<div class="result-source" markdown="1">

来源：Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

C3 95.26 93.63 86.44 87.62

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 复合基准主要由公开数据集中的 speech、singing、music 和 environmental sound 组合构造，并采用“任一组件为 fake 则整段为 fake”的 early-fail 标签规则；该设置便于验证组件证据聚合，但未必覆盖真实世界中更复杂的篡改强度、部分伪造比例和非二元真实性。
- 实验结果依赖预先训练的 Demucs v4 分离器、四类领域专家和结构化输出格式；当分离失败、输入域超出专家覆盖范围或编排器生成不可解析轨迹时，性能和解释可靠性可能下降。现有摘录未明确报告跨数据集泛化、人工解释质量评估或真实部署成本。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- XLSR-AASIST：以自监督 wav2vec 2.0 表征结合图神经网络，是标准的单体音频深度伪造检测器，用于代表常规强基线。
- XLSR-Conformer：使用 Conformer 同时建模局部与全局时间依赖，用于检验更强的时序建模是否足以应对混合真实性场景。
- WPT-XLSR-AASIST：面向全类型音频、具有频率敏感性的检测方法，用于比较显式频域建模对跨声学域检测的作用。
- ALLM4ADD 与 Fixed Pipeline：前者是针对音频深度伪造检测微调的音频大语言模型，代表单体式 ALLM；后者对所有输入固定执行 Demucs v4 分离，再把 vocal 与 non-vocal 流送入专门检测器，最终采用任一检测器判假，用于检验动态工具选择相对于机械式工具链的价值。

**实验想回答的问题**

- 在单一声学类型与混合真实性场景中，ToolDF 是否能比端到端单体模型和固定工具流水线更准确地判断音频整体是真实还是伪造，尤其是在时间转换、声源重叠及二者结合的复合场景中？
- ToolDF 的音频理解、动态规划、工具调用和证据描述环节是否分别有助于格式可靠性、检测性能及细粒度证据定位？

**实验实现**

ToolDF 使用 Qwen2.5-Omni-3B 作为音频大语言模型编排器，并在监督式 tool-use 轨迹上微调；通过 LoRA 保持基础模型冻结，仅训练插入线性层的低秩适配器。推理时，编排器先生成按片段划分的音频理解和工具计划，决定是否进行 Demucs v4 声源分离，以及将哪些片段或分离源送入 speech、singing、music 或 environmental sound 专家检测器。各专家返回二分类真实性预测和归一化置信度，再被写回轨迹；编排器据此生成证据描述和 real/fake 结论，任一组件判为 fake 即按 early-fail 规则判定整段为 fake。专家检测器使用 XLSR-AASIST，并同时训练原始输入版本和面向分离输入、可处理分离伪影的版本；每个检测器的判定阈值由开发集等错误率确定。评测同时报告单类型与 C1、C2、C3 复合类型，并对 ToolDF 的 parsed-only 与 strict 两种结果进行消融分析：前者只计算格式成功的输出，后者把无法解析的输出当作错误预测。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除音频理解（w/o Audio Understanding） | 在 C1、C2、C3 上，strict Macro-F1 分别为 48.25%、39.77% 和 44.31%，而 ToolDF 分别为 91.21%、77.66% 和 76.81%；其解析率分别为 82.59%、79.85% 和 83.15%。 | 去掉按片段描述音频内容的中间表示后，模型难以形成正确的工具选择依据，检测性能大幅下降，尤其在重叠场景中更明显。这支持音频理解是路由前的重要信息接口，但由于该消融同时改变了轨迹结构，不能把全部损失严格归因于单一表征能力。 | Table 4<br><span class="experiment-evidence">w/o Audio Understanding 82.59 60.12 48.25 79.85 48.82 39.77 83.15 53.21 44.31</span> |
| 移除规划（w/o Planning） | 在 C1、C2、C3 上，strict Macro-F1 分别降至 44.08%、20.87% 和 34.33%，显著低于 ToolDF 的 91.21%、77.66% 和 76.81%；对应解析率为 96.71%、84.34% 和 97.52%，说明格式大多仍可解析，但判断质量严重下降。 | 规划环节决定对哪些片段调用哪些专家以及是否使用分离器；移除它后，模型即使能够输出规定格式，也缺少面向场景的行动策略。C2 的下降最大，直接说明重叠声源需要条件化的分离与专家路由，而不是仅靠固定的输出模板。 | Table 4<br><span class="experiment-evidence">w/o Planning 96.71 45.47 44.08 84.34 24.57 20.87 97.52 35.18 34.33</span> |

**定性案例**

- 原文未提供具体音频案例、逐步工具调用示例或可核验的定性样例；论文仅通过 Table 5 的定位指标说明 ToolDF 能将证据定位到时间区域和声学来源，因此不能进一步判断其在个别困难样本上的解释是否符合人工听感。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：以音频大语言模型为编排器，进行工具选择、源分离、专家路由和证据聚合，实现可解释的工具集成推理。; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`1a4dd7361054b6ee1ecdaaef1facee8f42bca6e23a4c47a2751fbfbe9dfed977`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
