---
title: "[论文解读] TempCloze: Can Video-LLMs Identify the Missing Middle?"
description: "[arXiv 2609.01515][VLM Reasoning] TempCloze以“根据视频开头和结尾找回缺失中段”的纯视觉候选选择任务，检验Video-LLM能否摆脱语言捷径，真正判断事件内容、时间位置与演化过程。"
arxiv_id: "2609.01515"
announcement_date: "2026-09-02"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:42:40.324257+00:00"
source_sha256: "731b38840f5943592721b47c2c5218819175d64995637716c1bbc8a35c3f10ab"
tags:
  - "VLM Reasoning"
  - "LLM 评测"
  - "LLM Reasoning"
  - "视频大语言模型"
  - "视觉时间推理"
  - "视频完形任务"
  - "缺失中段识别"
  - "时间对齐"
  - "过程演变"
  - "语言捷径"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2609.01515</p>

# TempCloze: Can Video-LLMs Identify the Missing Middle?

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Wenqi Pei, Henry Hengyuan Zhao, Yilai Liu, Jiahao Meng, Han Chen, Ziyu Wang, Hongyang Du</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: The University of Hong Kong；Affiliation: National University of Singapore；Affiliation: Peking University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.01515v1) · [PDF 下载](https://arxiv.org/pdf/2609.01515v1) · **关键词** 视频大语言模型, 视觉时间推理, 视频完形任务, 缺失中段识别, 时间对齐, 过程演变, 语言捷径<br>
**代码**: [https://github.com/CedricPei/Temporal-Cloze](https://github.com/CedricPei/Temporal-Cloze)

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

TempCloze以“根据视频开头和结尾找回缺失中段”的纯视觉候选选择任务，检验Video-LLM能否摆脱语言捷径，真正判断事件内容、时间位置与演化过程。

**不用术语来说**：现有视频模型即使在时间推理测试中得分较高，也可能只是从文字选项的措辞、常见答案搭配或语言常识中猜中答案，而不是真的看懂视频先后关系。论文因此关注一个更直接的问题：只给模型同一视频的开头、结尾和四段视觉候选，它能否找出在时间上恰好位于二者之间的那一段，而不是仅挑出场景相似或内容大致合理的片段。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出TempCloze诊断基准：从七类来源筛选出1,521个视频，以缺失中段识别替代依赖自然语言描述的传统问答，并使用同源候选压低场景、物体和画面外观带来的捷径；候选分别诊断语义、时间对齐和事件进程三个维度。
- 通过评测10个闭源和21个开源Video-LLM，并结合TempCloze-Mixed、TempCloze-Hard上的错误模式与行为敏感性分析，作者识别出时间对齐是主要瓶颈，还发现模型选择会受到候选顺序、上下文方向、可见时间跨度、帧密度和测试时扩展等因素影响。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

视频大语言模型（Video-LLM）通过联合处理视频帧与语言指令来理解动作、事件及其时间关系。现有时间推理基准通常采用视频问答或文本描述生成：模型从文本选项中选择答案，或用语言描述视频内容，因此成绩可能同时反映视觉理解与语言先验，甚至可被选项措辞和答案相关性等捷径抬高。TempCloze将评测改写为视觉完形任务，不要求模型比较事件的文字描述，而是直接比较视频片段，以更集中地考查模型能否依据前后文恢复被移除的时间区间。该问题不仅要求识别“发生了什么”，还要求判断事件应在何时出现以及动作过程应如何展开。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉时间推理**

指依据连续或分段的视频证据，判断事件的先后顺序、发生位置及动态演变过程。它不同于仅识别物体或动作，因为外观相似的片段可能处于完全不同的时间位置。

</div>
<div class="concept-item" markdown="1">

**完形任务（Cloze Task）**

完形任务从完整上下文中移除一部分，再要求系统恢复缺失内容。TempCloze移除的是视频中段，并让模型从四个候选视频片段中找回真实中段，而非填写文本空缺。

</div>
<div class="concept-item" markdown="1">

**语言捷径**

模型不充分利用视频证据，而是依赖选项措辞、答案分布相关性或预训练语言知识作答的现象。以视频片段代替文本答案，可以减少但不能保证彻底消除这类非视觉线索。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

每个样本来自一段经筛选的视频：研究者保留开头片段与结尾片段作为上下文，隐藏其间的真实视频区间，并提供四个候选中段；模型输出正确候选的编号。正确答案必须既与事件语义相符，又处在开头和结尾之间的正确时间位置，并保持合理的动作演变。干扰项取自同一来源视频，尽量共享场景和物体，以削弱仅凭外观匹配作答的可能性；它们分别针对三个维度构造：语义（Semantic，$S$）用其他不重叠区间替换应发生的事件，时间对齐（Alignment，$A$）通过平移或扩展真实区间制造时间边界错误，过程演变（Progression，$P$）通过倒放、重排或重复改变事件展开方式。基准共含来自七个来源的$1{,}521$段视频，主要覆盖长镜头、第一人称和细粒度运动场景；四选一设置下，单维随机正确率为$25\%$。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$S$**

Semantic（语义）维度：判断缺失位置应当发生什么事件。

</div>
<div class="notation-item" markdown="1">

**$A$**

Alignment（时间对齐）维度：判断候选事件是否位于正确时刻并具有合适的时间边界。

</div>
<div class="notation-item" markdown="1">

**$P$**

Progression（过程演变）维度：判断事件内部的动作顺序与发展方式是否正确。

</div>
<div class="notation-item" markdown="1">

**$3/3$**

同一视频在语义、时间对齐和过程演变三个实例上均回答正确的累计准确率条件。

</div>

</div>

**直接相关的工作**

- **TempCompass与TVBench**: 二者直接评测事件顺序、时刻定位或细粒度运动等视频时间结构，但主要通过文本问题、文本选项或描述来介导评测。TempCloze保留时间推理目标，同时将待比较对象改为视频候选，以降低语言表面规律对成绩的影响。
- **MovieFIB与VideoBERT**: MovieFIB采用电影描述中的文本填空来评测视频理解，VideoBERT则把掩码预测用作视频—文本表征学习的预训练目标。它们表明完形形式可用于视频研究，但TempCloze的区别在于：将缺失视频中段的识别设计为Video-LLM的视觉时间推理评测，而不是文本补全或训练目标。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

Video-LLM需要理解动作和事件如何随时间发生，才能可靠处理长视频、第一视角活动和细粒度运动。然而，当前评测结果难以区分两种能力：模型究竟理解了视觉时间结构，还是借助文字选项和语言先验获得高分。若评测本身允许后一种策略，研究者便可能高估模型在真实视频时间推理上的进展，也难以准确定位模型是在事件识别、时间定位还是过程理解上失败。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **文本选项式视频问答**：模型观看视频后，在若干自然语言答案中进行选择；时间关系被编码为问题和选项文字，因此最终得分同时受到视觉理解、文本理解及语言先验影响。
- **开放式视频描述或字幕生成**：模型根据视频生成详细文字，评测其是否描述了事件及其时间关系；这种形式覆盖内容较广，但时间推理仍需经过语言生成与文本评价，无法单独隔离视觉证据比较能力。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 语言中介会引入可被利用的非视觉线索，包括选项措辞、答案相关性和语言先验。原文举例指出，预训练语言模型在没有多模态上下文时也能比随机基线高出25%以上，说明某些高分并不必然来自视频理解。
- 传统评测往往不能细分“内容合理”与“时间位置正确”：一个片段可能包含相关事件，却不属于开头与结尾之间被移除的准确区间。若候选在场景或物体上差异明显，模型还可依赖外观匹配，而无须判断事件何时发生、如何展开。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少一种以视觉片段直接互相比对、尽量控制语言和外观捷径，并能分别诊断“发生什么”“何时发生”“如何演化”的时间推理基准。尤其尚不清楚，Video-LLM在面对同一来源、场景与物体高度相似的候选时，能否识别与前后端点精确兼容的时间区间，而不只是选出语义上 plausible 的片段。

</div>
<div markdown="1"><span>核心问题</span>

给定同一视频的开头片段、结尾片段以及四个候选中段，Video-LLM能否找出真正缺失的中间部分，并据此表现出对事件语义、时间对齐和事件进程的视觉时间推理能力？

</div>
<div markdown="1"><span>作者直觉</span>

如果把答案从文字改成视频片段，模型就必须更多地依据画面中的动作和状态变化；再让错误候选来自同一原视频并共享场景与物体，简单的外观相似度也难以奏效。此时，语义干扰项检查模型是否知道接下来应发生什么，对齐干扰项检查片段是否恰好处于正确时间位置，进程干扰项则通过倒放、重排或重复检查模型是否理解动作如何展开。开头和结尾像拼图两侧的边缘，真正的中段不仅要“内容像”，还必须同时与两侧在时间上接得上。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

TempCloze将视频定义在时间区间$(0,T)$上，并把目标缺失区间$(s,e)$两侧的可见内容作为上下文：开头片段$B=C_{0,s}$、缺失中段$M=C_{s,e}$和结尾片段$E=C_{e,T}$组成$V=[B\mid M\mid E]$。给定$(B,E)$及四个候选片段的集合$\mathcal{Y}_d$，模型需要选出真实的$M$；其中每个维度$d\in\{S,A,P\}$分别测试语义、时间对齐和事件进展。直观而言，任务不是根据选项文字猜答案，而是根据视频前后的视觉证据判断“中间究竟发生了什么、发生在什么时刻、动作如何连续展开”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多源视频收集与初筛

首先保留时长为12至90秒的视频，并利用来源字幕进行预筛；随后使用GPT-o3判断事件是否具有时间连贯性、周围上下文是否足以约束一个缺失中段，不合适的视频被排除。

<div class="method-step__io" markdown="1">

**输入**：来自CaReBench、Daily-Omni、EgoLife、FAVOR-Bench、LVD-2M、MiraData和Video Thinking Test的公开视频及其元数据、密集字幕（部分来源提供）。<br>
**输出**：适合构造视频填空任务的候选视频集合。

</div>

**直观理解**：先从多个视频库中挑出长度合适、前后情节能形成线索的视频，避免把本来就无法判断的片段放入数据集。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 质量、运动与缺口筛选

移除码率低于200 kbps或清晰度低于30的视频；在视频时间轴中央50%的范围内采样缺口，使缺口长度占全视频20%至40%，并使用Farnebäck光流验证平均运动幅度是否高于1.0，最多重新采样三次。

<div class="method-step__io" markdown="1">

**输入**：通过语义初筛的视频。<br>
**输出**：包含可辨识运动、两侧均有上下文且不易由边界位置直接猜出的目标视频与缺失区间$(s,e)$。

</div>

**直观理解**：缺口放在视频中间而不是开头或结尾，并确保片段画面足够清楚、确实有动作，这样答案主要依赖时间推理而非画质或位置捷径。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选片段与干扰项构造

针对语义$S$、对齐$A$和进展$P$三个维度，各构造三个干扰项，形成$\mathcal{Y}_d=\{M,D_d^1,D_d^2,D_d^3\}$。语义干扰项从同一视频的非重叠位置取同长度片段；对齐干扰项平移或扩展目标区间；进展干扰项通过反向播放、打乱局部子事件顺序或重复短子片段破坏动作连续性。

<div class="method-step__io" markdown="1">

**输入**：目标视频$V$、真实中段$M=C_{s,e}$及其时间区间$(s,e)$。<br>
**输出**：每个样本的可见上下文$(B,E)$、正确候选$M$以及按维度组织的四选一候选集$\mathcal{Y}_d$。

</div>

**直观理解**：三类错误选项分别像是在问“是不是这个事件”“是不是这个时间段”和“动作顺序是否正确”，并尽量保持场景和物体相似，减少凭外观排除选项的可能。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### Video-LLM评测

将缺失中段留空，把开头、结尾及候选片段提供给Video-LLM，要求其从四个候选中识别真实中段；在不同模型、数据子集和行为敏感性设置下记录选择结果。

<div class="method-step__io" markdown="1">

**输入**：上下文视频$(B,E)$和四个候选中段$\mathcal{Y}_d$。<br>
**输出**：模型在Semantic、Alignment、Progression三个维度上的选择准确性，以及错误模式和对候选顺序、上下文方向、可见跨度、帧密度、测试时扩展等因素的敏感性。

</div>

**直观理解**：模型需要像拼接视频一样判断哪个候选能同时接上前半段和后半段；评测还检查它是否会被选项位置、只看单向上下文或改变帧数等因素影响。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 视频的缺失中段分解

$$
V=[C_{0,s}\mid C_{s,e}\mid C_{e,T}]=[B\mid M\mid E]
$$

**符号说明**

- $V$：完整视频，定义在时间区间$(0,T)$上。
- $T$：视频结束时间。
- $s,e$：缺失中段的起始时间和结束时间，满足目标区间为$(s,e)$。
- $C_{a,b}$：覆盖时间区间$(a,b)$的视频片段。
- $B$：开头上下文片段$C_{0,s}$。
- $M$：真实缺失中段$C_{s,e}$。
- $E$：结尾上下文片段$C_{e,T}$。

<div class="equation-explanation" markdown="1">

**直观理解**：该式说明完整视频由缺口前、缺口中和缺口后三段按时间顺序组成。评测时隐藏$M$，模型只能观察$B$和$E$，再从候选中恢复它。<br>
**原文位置**：第3.1节“Overview”

</div>

</div>

<div class="equation-block" markdown="1">

#### 按维度定义的四候选集合

$$
\mathcal{Y}_{d}=\{M,D_{d}^{1},D_{d}^{2},D_{d}^{3}\},\quad d\in\{S,A,P\}
$$

**符号说明**

- $\mathcal{Y}_{d}$：维度$d$对应的四个候选片段集合。
- $M$：真实缺失中段，即正确答案。
- $D_{d}^{1},D_{d}^{2},D_{d}^{3}$：针对维度$d$构造的三个干扰片段。
- $d$：测试维度；$S$表示Semantic，$A$表示Alignment，$P$表示Progression。

<div class="equation-explanation" markdown="1">

**直观理解**：每道题只有一个真实中段和三个专门制造的错误中段。改变$d$就改变主要考查点：内容是否正确、时间位置是否正确，或动作发展是否连续。<br>
**原文位置**：第3.1节“Overview”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告TempCloze用于训练模型的损失函数或优化目标；所给章节描述的是基准构造与评测，而不是Video-LLM的训练过程。因此不能据此推断模型是否进行微调，或是否使用交叉熵、排序损失等目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 缺失中段任务形式化**

视频$V$在目标区间$(s,e)$处分解为$[B\mid M\mid E]$，其中$B=C_{0,s}$、$M=C_{s,e}$、$E=C_{e,T}$。模型输入可见上下文$(B,E)$和候选集合$\mathcal{Y}_d$，输出四个候选中的一个，正确答案为真实中段$M$。

> 直观理解：模型看不到视频中间的一段，只能利用缺口前后的画面，从四个候选中选出真正能够接上的那一段。

**2. 三维度干扰项设计**

Semantic保持片段时长但更换事件内容；Alignment保持内容具有合理性，却通过前移、后移或扩大时间范围改变边界；Progression保持较粗粒度的内容和时间兼容性，却反转、重排或重复局部动作。三类设计分别隔离语义识别、时间边界判断和细粒度事件连续性。

> 直观理解：这套设计把“看懂发生了什么”和“判断它何时发生、如何发生”拆开测试，因此模型不能只凭一个大概相似的活动名称作答。

**3. 时序连续性与外观捷径控制**

数据源优先纳入长镜头和第一视角视频，以减少场景切换带来的提示；候选项尽量来自同源视频并共享场景或物体线索，缺口则从中央时间范围采样。质量和光流过滤进一步保证片段具有可用视觉信息与运动变化。

> 直观理解：如果候选来自完全不同的场景，模型只要比较背景就能答对；因此作者尽量让选项看起来相似，迫使模型使用真正的时间关系。

**训练与推理**

数据集构造阶段依次进行来源视频筛选、GPT-o3时序适配性判断、质量与运动过滤、中央缺口采样和三类干扰项生成，最终保留1,521个视频。推理阶段向Video-LLM提供开头片段$B$、结尾片段$E$及某一维度的四候选集合$\mathcal{Y}_d$，模型选择一个候选作为缺失中段；章节未说明统一的提示词、候选呈现格式或是否要求生成理由。随后以选择准确性分析Semantic、Alignment和Progression维度，并在TempCloze-Mixed与TempCloze-Hard上检查错误模式和候选顺序、上下文方向、可见跨度、帧密度及测试时扩展的影响。

**复现信息**

复现数据构造所需的关键条件包括：保留12至90秒视频；码率阈值为200 kbps、清晰度阈值为30；缺口从时间轴中央50%采样，长度为全视频的20%至40%；Farnebäck平均光流幅度需高于1.0，缺口最多重采样三次。语义干扰项为与目标区间不重叠且时长相同的片段；对齐干扰项通过Advanced、Deferred或Expanded改变时间范围；进展干扰项采用Reversed、Reordered和Repeated变体。其余详细筛选统计、候选生成数学定义和人工验证位于附录D.2、D.3及附录A，所给章节未提供更多可复现细节。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- TempCloze：包含 $1{,}521$ 个经过筛选的视频，来自七个来源，主要由长镜头和第一视角视频构成。每个实例向模型提供视频开头与结尾片段，并要求从四个候选中选出缺失的中间片段；候选干扰项来自同一来源，并在 Semantic、Alignment、Progression 三个维度上进行控制，以减少场景、物体和外观线索带来的捷径。原文在实验节未进一步明确报告训练集、验证集和测试集的划分。
- TempCloze-Mixed：随机抽取的 $300$ 个视频组成的辅助子集；每个实例包含真实答案以及来自 Semantic、Alignment 和 Progression 的候选项。该子集用于分析不同干扰维度在混合竞争条件下造成的错误，而不是单独估计某一维度的纯粹能力。
- TempCloze-Hard：选取跨模型错误数量最多的 $150$ 个实例。该子集用于放大模型在候选顺序、上下文方向、可见跨度、采样密度和测试时扩展方面的行为差异；由于它按模型错误构造，不能直接视为自然分布上的总体性能估计。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Dimension accuracy**

分别计算模型在 Semantic、Alignment 和 Progression 三种干扰维度上的选择准确率，用来区分模型是无法识别事件内容、无法判断事件发生时机，还是无法判断事件发展顺序。 （越高越好，因为它表示模型更常选出符合缺失位置的真实中间片段。）

</div>
<div class="metric-item" markdown="1">

**Cumulative accuracy**

统计模型在三个维度中至少正确 $1$ 个、至少正确 $2$ 个，以及三个维度全部正确的比例；其中 $3/3$ 表示完整理解，$\geq2$ 表示达到作者定义的充分理解水平。 （越高越好；尤其是 $3/3$ 越高，说明模型能同时满足事件语义、时间位置和发展顺序，而非只解决其中一部分。）

</div>
<div class="metric-item" markdown="1">

**FR、CFR 与 Disp.**

在每个实例测试四种候选排列时，FR 表示答案正确性至少改变一次的实例比例，CFR 表示所选片段至少改变一次的实例比例，Disp. 表示不同排列下准确率的离散程度；它们衡量候选顺序造成的行为不稳定性。 （FR、CFR 和 Disp. 均越低越好，因为较低数值表示模型较少受候选排列影响；不过稳定性低不等于准确率必然低。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三种维度的总体准确率比较

<div class="result-value" markdown="1">

Semantic 和 Progression 相对容易，Alignment 明显困难。专有模型在 Semantic、Progression 和 Alignment 上的平均准确率分别为 $70.73\%$、$67.72\%$ 和 $48.13\%$；开源模型对应为 $34.00\%$、$36.97\%$ 和 $26.54\%$。专有模型中 Seed1.8 在 Semantic 上达到 $96.25\%$，Alignment 上达到 $76.92\%$；开源模型中 Qwen3.5-397B 在 Semantic 和 Progression 上分别达到 $75.94\%$ 和 $78.24\%$，而 Qwen3.5-35B 在 Alignment 上达到 $51.55\%$。作者据此将 Alignment 认定为当前 Video-LLM 视觉时间推理的主要瓶颈。

</div>

该结果区分了三种看似相近的能力：模型可能知道“应该发生什么”，也可能知道局部动作“如何接续”，但仍不能判断该动作是否正好发生在开头和结尾之间的正确时间位置。它支持 Alignment 是更难的诊断维度，但不证明所有模型架构都必然存在相同程度的瓶颈；不同模型的训练数据、推理设置和规模也可能影响差异。

<div class="result-source" markdown="1">

来源：Section 4.2 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Alignment is substantially harder. Proprietary models drop to 48.13% on average, while open-source models drop to 26.54%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 完整视频理解的累积准确率

<div class="result-value" markdown="1">

从单维度转向同时满足多个维度后，模型表现进一步下降。专有模型在至少正确两个维度（$\geq2$）上的平均准确率为 $65.12\%$，最佳模型为 $95.40\%$；三个维度全部正确（$3/3$）时，专有模型平均为 $33.24\%$，最佳模型为 $70.81\%$，低于人类基线的 $92.00\%$。开源模型中，最强模型在 $\geq2$ 和 $3/3$ 上分别达到 $74.49\%$ 和 $35.77\%$。

</div>

单项高分不等于完整理解：模型只要在 Semantic、Alignment、Progression 中漏掉一项，就不能算 $3/3$。因此累积指标检验的是模型能否把事件内容、发生时机和发展方向同时整合起来，而不是分别完成若干局部判断。该结果表明当前模型距离稳定的全视频时间理解仍有明显差距，但不能单独说明错误究竟来自视觉识别、时间整合还是候选判别。

<div class="result-source" markdown="1">

来源：Section 4.2 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The proprietary average drops to 33.24% on 3/3, and even the best model reaches only 70.81%, far below the 92.00% Human Baseline.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 混合干扰项中的错误归因

<div class="result-value" markdown="1">

在 TempCloze-Mixed 中，四个代表模型的 Alignment 错误占比均为最高或接近最高：Gemini2.5-Pro 的总体准确率为 $76.3\%$，Semantic、Alignment、Progression 错误占比分别为 $2.7\%$、$19.7\%$、$1.3\%$；Seed1.6 为 $68.9\%$、$7.0\%$、$14.7\%$、$9.4\%$；Qwen3.5-397B-A17B 为 $62.0\%$、$9.0\%$、$20.3\%$、$8.7\%$；Qwen3VL-8B-I 为 $24.0\%$、$29.3\%$、$37.3\%$、$9.3\%$。作者还指出，Semantic 有时比 Progression 更能造成干扰，说明混合候选竞争会暴露边际准确率掩盖的错误。

</div>

这一设置不是只让模型在一个维度内做区分，而是让来自三种设计的候选同时竞争，因此更接近模型实际的选择过程。Alignment 错误占比高，说明模型常被“内容看起来合理但时间位置不对”的片段吸引；Semantic 错误有时超过 Progression，则说明错误事件可能比错误动作顺序更难排除。由于这是错误归因比例而非独立维度准确率，它不能直接替代三种维度的单独成绩。

<div class="result-source" markdown="1">

来源：Section 4.3.2 Mixed-Dimension Errors; Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across models, Alignment receives the highest error share.

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

- Human Baseline：作为人类表现参照，用于衡量模型距离人工视觉时间推理能力的差距；原文报告其在 Alignment 维度为 $98.00\%$，在三维均正确的 $3/3$ 指标上为 $92.00\%$。
- 专有 Video-LLM：共评估 $10$ 个专有模型，包括 Qwen3.5-Plus、Seed1.8、Gemini2.5-Pro、Gemini2.5-Flash、GPT5.4、Claude4.6-Sonnet、Claude4.6-Opus、Gemini3-Flash、Seed1.6 和 Grok4.1，用于考察闭源系统的整体水平。
- 开源 Video-LLM：共评估 $21$ 个开源模型，包括 Qwen、Kimi、Qwen3VL、InternVL、KimiVL、LLaVA-CriticR1、Qwen2.5VL、GLM、ThinkLiteVL、MiMoVL 和 Molmo2 系列，用于比较不同开源模型规模、架构和训练方式下的表现。
- 四个代表模型：Gemini2.5-Pro、Seed1.6、Qwen3.5-397B-A17B 和 Qwen3VL-8B-I，用于深入错误模式及行为敏感性分析。它们并非额外的训练基线，而是从专有与开源模型中选出的分析对象。

**实验想回答的问题**

- 不同规模与类型的专有及开源 Video-LLM 在 Semantic、Alignment 和 Progression 三种时间推理维度上表现如何，完整视频理解的主要瓶颈是什么？
- 候选项顺序、可见上下文方向、可见时长、帧采样密度和测试时多次采样如何影响模型的稳定性与判断性能？

**实验实现**

实验覆盖 $10$ 个专有模型和 $21$ 个开源模型。默认从每个片段均匀采样 $16$ 帧；每个实例包含六个片段，因此每个维度共得到 $96$ 帧。作者另在附录中进行边界 sanity check，以排除模型仅依赖精确边界帧的捷径。开源模型部署在 A6000 GPU 上并使用 vLLM。深入分析使用四个代表模型；候选顺序实验对每个实例测试四种排列。测试时扩展实验在温度 $0.7$ 下进行，并使用 Pass@$k$：若 $k$ 次采样中任一次正确，则该实例计为解决。原文未明确报告完整的训练、验证和测试划分，也未在所给实验节中报告所有模型的具体推理提示词。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 候选顺序置换（TempCloze-Hard） | 对每个实例测试四种候选排列后，所有模型的平均准确率变化幅度低于 $4$ 个百分点，但 CFR 为 $32.4\%$ 至 $60.7\%$，FR 为 $25.9\%$ 至 $40.2\%$；Semantic 通常比 Alignment 和 Progression 更稳定。 | 该实验隔离的是选项位置这一非视觉因素：视频内容和候选内容不变，只改变候选排列。如果均值准确率近似不变但 CFR 或 FR 较高，说明模型总体答对率看似稳定，具体选择却会随选项位置改变。对评测而言，这意味着需要控制或随机化候选顺序；对模型而言，这暴露了候选相似时决策依据不够稳固的问题。 | Section 4.4.1 Candidate Order Permutation; Table 4<br><span class="experiment-evidence">Mean accuracy changes little, with variance below 4 points for every model, but both instability measures remain substantial: CFR ranges from 32.4% to 60.7%, and FR ranges from 25.9% to 40.2%.</span> |
| 上下文方向、可见跨度与采样密度 | 只提供结尾片段通常最弱，而只提供开头片段有时接近或超过双向上下文；例如 Seed1.6 在 Progression 上使用开头片段为 $80\%$，双向上下文为 $82\%$，结尾片段则为 $46\%$。随着可见跨度或每片段采样帧数增加，Alignment 在所有模型上下降；Semantic 和 Progression 对强模型更可能保持稳定或略有提升。 | 这些消融共同检验模型如何使用时间证据。开头片段更有效，表明模型可能更擅长根据已发生内容预测后续，而不擅长从结果倒推缺失过程。更长上下文和更密集采样理论上提供更多信息，但也会稀释缺口边界附近最关键的线索；所以“输入更多帧”并不自动等于更好的时间定位能力。 | Section 4.4.2 Context Direction Ablation; Figure 4<br><span class="experiment-evidence">For example, Seed-1.6 reaches 80% on Progression with beginning-only, close to 82% with both, but drops to 46% with ending-only.</span> |

**定性案例**

- 维度特定错误显示模型的失败并非随机：在 Alignment 中，Expanded 干扰项最突出，即候选包含正确事件内容，却在目标区间前后都延伸；在 Progression 中，Reversed 是主要失败模式，即事件内容相关但发展方向相反。原文给出的例子是 Seed1.8-I 在 Alignment 错误中有 $75\%$ 选择 Expanded，GPT-5.4 在 Progression 错误中有 $67\%$ 选择 Reversed。这说明模型能识别周围视频中的相关内容，却可能无法精确判断时间边界或事件发展的方向。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It contributes a benchmark specifically evaluating temporal visual reasoning in Video-LLMs and analyzes their reasoning failures.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`731b38840f5943592721b47c2c5218819175d64995637716c1bbc8a35c3f10ab`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
