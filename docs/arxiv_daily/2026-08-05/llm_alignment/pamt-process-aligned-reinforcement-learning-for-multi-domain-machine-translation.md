---
title: "[论文解读] PAMT: Process-Aligned Reinforcement Learning for Multi-Domain Machine Translation"
description: "[arXiv 2608.03077][对齐 / RLHF] 本文指出多领域机器翻译中的显式推理虽能帮助处理长文本和高难度输入，却可能造成术语与风格偏移，并据此提出通过步骤级奖励对齐翻译决策与最终译文的PAMT框架。"
arxiv_id: "2608.03077"
announcement_date: "2026-08-05"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:42:23.187671+00:00"
source_sha256: "bb8026d8c6d6191e5b8f8c5ede42c215f1891136dd99efc411cd92632a83cb7a"
tags:
  - "对齐 / RLHF"
  - "LLM 其他"
  - "LLM Reasoning"
  - "多领域机器翻译"
  - "大型推理模型"
  - "显式翻译推理"
  - "长链式思维"
  - "过程对齐"
  - "信用分配"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.03077</p>

# PAMT: Process-Aligned Reinforcement Learning for Multi-Domain Machine Translation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Yongshi Ye, Biao Fu, Chongxuan Huang, Yidong Chen, Xiaodong Shi</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Institute of Artificial Intelligence, Xiamen University；School of Informatics, Xiamen University；Key Laboratory of Digital Protection and Intelligent Processing of Intangible Cultural；Heritage of Fujian and Taiwan (Xiamen University), Ministry of Culture and Tourism</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03077v1) · [PDF 下载](https://arxiv.org/pdf/2608.03077v1) · **关键词** 多领域机器翻译, 大型推理模型, 显式翻译推理, 长链式思维, 过程对齐, 信用分配<br>


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

本文指出多领域机器翻译中的显式推理虽能帮助处理长文本和高难度输入，却可能造成术语与风格偏移，并据此提出通过步骤级奖励对齐翻译决策与最终译文的PAMT框架。

**不用术语来说**：面对医学、法律或其他专业领域的文本，译文不仅要通顺，还必须正确处理专业术语、歧义和领域风格。让模型先写出分析步骤再翻译，有时能把复杂问题拆开解决，但这些分析也可能看似合理、实际却把术语或语气带偏。以往训练通常只根据最终译文整体打分，难以判断究竟是哪一步分析帮助或损害了翻译，因此模型无法有针对性地改进中间决策。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者在15个领域、4个翻译方向上系统比较大语言模型与大型推理模型，发现显式翻译推理具有明显的条件依赖性：它更适合长上下文和高难度输入，但在术语密集、风格约束严格的场景中较易发生偏移。
- 作者将上述失效归因于决策粒度与监督粒度不匹配，并提出PAMT：先用领域感知的长思维链数据进行冷启动监督微调，再以序列级格式与结果奖励约束最终输出，同时用步骤级过程奖励衡量每个显式步骤对参考译文似然的增益。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

多领域机器翻译（MDMT）要求同一模型处理来自不同专业或文体领域的文本。除保持原文语义外，模型还必须依据领域语境消解歧义、采用约定术语并匹配目标文体。传统的大语言模型翻译通常把任务视为从源文本到译文的直接序列生成；大型推理模型则显式生成中间翻译步骤，使术语选择、语义分析和修订等决策可见。论文关注的关键现象是：显式推理有助于长文本和高难度输入，却可能在术语密集或文体约束严格的领域偏离专业惯例，因此仅保证推理过程“看起来合理”并不足以保证领域忠实性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多领域机器翻译（MDMT）**

让一个翻译模型面向多个领域工作，例如不同专业领域或不同文体。相同词语在各领域可能具有不同译法，译文也需遵守相应的术语和风格规范。

</div>
<div class="concept-item" markdown="1">

**长链式思维（Long-CoT）**

模型在给出最终译文前显式生成较长的中间分析与决策步骤，例如识别领域、解释歧义、确定术语并修订表达。其价值在于把原本隐含的翻译决策外显，但错误分析也可能逐步累积并造成术语或风格漂移。

</div>
<div class="concept-item" markdown="1">

**信用分配（credit assignment）**

强化学习需要判断一次生成中的哪些具体决策促成了好结果、哪些决策造成了错误。若奖励只赋给最终译文或整条推理轨迹，模型便难以定位真正有益或有害的中间翻译步骤。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是来自不同领域、不同语言方向的源文本，输出是符合目标语言表达习惯且忠实于相应领域语义、术语和文体规范的译文；模型还可在最终译文之前生成显式的中间翻译过程。论文的分析覆盖15个领域和4个翻译方向，并同时考虑长文本、高难度文本、术语密集文本与文体约束文本。其基本假设是，中间步骤是否有用不能仅由其表面合理性判断，而应依据该步骤是否提高参考译文出现的可能性来获得细粒度反馈；因此研究问题并非单纯提升流畅度，而是如何使中间决策与最终领域忠实译文对齐。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **工作流式翻译方法**: 这类方法把翻译拆成起草、评价和修订等固定阶段，使过程显式化，但阶段数量少、粒度较粗，难以判断某个具体中间决策对最终译文的贡献。
- **DeepTrans与TAT-R1**: 二者通过外部大语言模型评分或术语约束引入过程级和输出级奖励，与本文最直接相关；但原文指出其奖励仍施加于整个过程，因而难以识别究竟哪个中间步骤导致了不忠实译文。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

多领域机器翻译要求模型随领域改变翻译决策，包括消解语义歧义、采用规范术语以及匹配特定文体。单纯生成语义大致正确且语言流畅的译文并不足够；一旦中间判断偏离领域惯例，最终译文就可能在专业术语或风格上失真。作者的跨领域分析进一步表明，显式推理不是稳定增益：它能支持长文本和困难样本的分步处理，却在约束更强的场景中表现脆弱。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **工作流与思维链式翻译方法**：工作流方法把翻译拆成少量阶段，如分析、起草和修订；思维链方法则生成更细致的显式过程轨迹，使模型在输出译文前陈述术语选择、歧义处理或风格判断。这些方法主要通过离线示范进行模仿学习，即学习已有过程应当如何写出。
- **基于强化学习的推理增强翻译方法**：这类方法对模型采样得到的译文或完整推理轨迹计算奖励，再用强化学习提高高奖励输出的概率。奖励通常依据最终译文质量，或对整条推理轨迹给出一个总体评价，而不是分别判断各个翻译步骤的实际贡献。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 显式工作流往往阶段过粗，而思维链的离线模仿只能复现示范轨迹，不能可靠判断某一步是否真正提升最终译文；因此，看似合理的中间分析仍可能引发术语或文体偏移。
- 现有强化学习信号主要作用于最终输出或完整轨迹，监督粒度大于实际决策粒度。整条轨迹获得一个总体奖励时，有益步骤与有害步骤会共享相近反馈，形成信用分配瓶颈，使模型难以针对具体翻译决策进行优化。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究已经能够显式展示翻译过程，也能依据最终结果优化模型，但缺少一种细粒度机制，把最终译文质量归因到各个中间步骤，并据此直接训练模型保留有益决策、抑制导致领域偏移的决策。该缺口尤其影响术语密集和风格约束严格的多领域翻译。

</div>
<div markdown="1"><span>核心问题</span>

如何让多领域机器翻译中的中间翻译决策获得可归因、可优化的训练信号，从而使显式推理真正服务于领域忠实的最终译文？

</div>
<div markdown="1"><span>作者直觉</span>

如果在加入某个推理步骤后，模型生成参考译文的可能性上升，就可以把这种增益视为该步骤对正确翻译的贡献。依次比较不同步骤加入前后的变化，便能把原本只属于整条输出的反馈拆分到具体决策上；再结合对最终译文格式和质量的整体奖励，模型既受到结果约束，也能学会哪些术语分析、歧义判断和风格选择值得保留。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PAMT 是一个两阶段的多领域机器翻译训练框架。第一阶段用约 7K 条领域感知 Long-CoT 数据进行冷启动监督微调，使基础模型学会按 `<think>翻译过程</think><answer>最终译文</answer>` 的格式显式表达翻译决策；第二阶段对每个源句 $x_i$ 采样 $G$ 条轨迹，并联合使用格式奖励、最终译文质量奖励和步骤级过程奖励进行强化学习。其核心不是只判断整条译文好坏，而是用冻结参考模型 $\pi_{\mathrm{ref}}$ 测量每个推理步骤加入前后参考译文似然的变化，再把变化量归因到产生该步骤的词元。
端到端看，模型输入源句，先生成包含显式翻译分析 $z_{i,g}$ 与最终译文 $y_{i,g}$ 的轨迹；系统依据双标签格式、BLEU/COMET/COMETKiwi 以及参考译文 $y_i^*$ 计算多粒度奖励，再形成逐词元回报与组内标准化优势，最后通过带裁剪和 KL 正则的 GRPO 风格目标更新策略。直观地说，PAMT 不仅批改“最终答案”，还检查每一步翻译分析是否让正确译文更容易被推出，从而奖励有帮助的术语选择、消歧和风格判断，抑制使翻译过程偏离目标的步骤。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 冷启动显式翻译过程

对完整参数进行监督微调，使模型学习输出 `<think>` 中的领域感知翻译过程，并在 `<answer>` 中给出最终译文。该阶段提供可供后续切分和归因的稳定轨迹结构。

<div class="method-step__io" markdown="1">

**输入**：Qwen2.5-7B-Instruct 或 Gemma2-9B-IT 基础模型，以及约 7K 条覆盖 10 个领域、3 个翻译方向的 Long-CoT 样本。<br>
**输出**：能够按固定双标签格式生成显式翻译步骤和最终译文的冷启动策略。

</div>

**直观理解**：先让模型学会把翻译时的判断写出来，再讨论哪些判断值得强化；否则强化学习没有稳定的中间步骤可评价。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多轨迹生成与步骤切分

对每个 $x_i$ 采样 $G$ 条轨迹 $o_{i,g}$，每条轨迹包含翻译过程 $z_{i,g}$ 和最终译文 $y_{i,g}$；再按双换行符将 $z_{i,g}$ 切成 $K_{i,g}$ 个步骤。参考译文不作为生成输入，从而避免训练时直接泄漏答案。

<div class="method-step__io" markdown="1">

**输入**：RL 训练源句 $x_i$、当前策略以及仅用于奖励计算的参考译文 $y_i^*$。<br>
**输出**：结构化轨迹 $o_{i,g}$、步骤序列 $[z_{i,g}^{(1)},\ldots,z_{i,g}^{(K_{i,g})}]$ 及其词元位置。

</div>

**直观理解**：同一道翻译题让模型尝试多种思路，并把每种思路拆成若干可单独记功或扣分的步骤。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多粒度奖励与词元级信用分配

格式奖励检查双标签结构，结果奖励平均归一化 BLEU、COMET 与 COMETKiwi；过程奖励则比较加入第 $k$ 步前后，$\pi_{\mathrm{ref}}$ 对参考译文的教师强制对数似然。每步增益按该步长度均分给其词元，终局格式与质量奖励放在最后有效词元，并通过回报传播到此前词元。

<div class="method-step__io" markdown="1">

**输入**：生成轨迹、步骤边界、参考译文 $y_i^*$ 和冻结参考模型 $\pi_{\mathrm{ref}}$。<br>
**输出**：每个生成词元的即时奖励 $r_{i,g,t}$、回报 $R_{i,g,t}$ 以及整条轨迹回报 $R_{i,g}^{\mathrm{traj}}$。

</div>

**直观理解**：最终译文得分回答“整篇是否译得好”，过程增益回答“刚才这一步是否让正确译文更容易得到”；按步骤长度均分可避免长篇分析仅因词元多而获得更大权重。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 组内优势估计与策略更新

用组内轨迹回报的均值 $\mu_i$ 和标准差 $\sigma_i$ 标准化逐词元回报，得到优势 $A_{i,g,t}$；随后优化 GRPO 风格裁剪代理目标，并加入相对冻结参考策略的 KL 正则。裁剪限制单次策略更新幅度，KL 项则防止模型为追逐奖励而过度偏离已有语言能力。

<div class="method-step__io" markdown="1">

**输入**：同一源句的 $G$ 条轨迹及其逐词元回报。<br>
**输出**：同时改善最终翻译质量与中间翻译决策的更新后策略 $\pi_\theta$。

</div>

**直观理解**：模型在同一句话的多次尝试中比较谁更好，再提高较好步骤的生成概率；同时用“安全绳”限制模型不要一下偏离原模型太远。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 参考似然势能与步骤级过程增益

$$
\phi_{i,g,k}=\sum_{m=1}^{|y_i^*|}\log \pi_{\mathrm{ref}}\!\left(y_{i,m}^*\mid c_{i,g,k},y_{i,<m}^*\right),\qquad r_{i,g,k}^{\mathrm{proc}}=\phi_{i,g,k}-\phi_{i,g,k-1},\quad k=1,\ldots,K_{i,g}
$$

**符号说明**

- $\phi_{i,g,k}$：第 $i$ 个样本的第 $g$ 条轨迹在纳入前 $k$ 个推理步骤后，对参考译文计算的过程势能。
- $i$：训练样本索引。
- $g$：同一源句下的采样轨迹索引。
- $k$：推理步骤索引。
- $m$：参考译文中的词元位置。
- $y_i^*$：第 $i$ 个源句对应的参考译文。
- $|y_i^*|$：参考译文的词元数。
- $y_{i,m}^*$：参考译文的第 $m$ 个词元。
- $y_{i,<m}^*$：参考译文中位于第 $m$ 个词元之前的真实前缀。
- $c_{i,g,k}$：由源句、起始思考标签、前 $k$ 个推理步骤及答案起始标签拼接成的条件上下文。
- $\pi_{\mathrm{ref}}$：冻结参考模型，用于计算参考译文似然，并兼作 KL 正则的参照策略。
- $r_{i,g,k}^{\mathrm{proc}}$：加入第 $k$ 个推理步骤所产生的过程奖励或势能增量。
- $K_{i,g}$：第 $g$ 条轨迹包含的推理步骤总数。
- $\phi_{i,g,k-1}$：加入第 $k$ 步之前的过程势能；当 $k=1$ 时，$\phi_{i,g,0}$ 对应空推理前缀。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分逐词累加冻结模型对参考译文的对数概率，衡量当前推理前缀是否支持正确译文；第二部分用相邻前缀的势能差隔离新加入步骤的贡献。正差表示该步骤提高了参考译文的可预测性，负差表示它可能把后续翻译引向错误方向。<br>
**原文位置**：第 4.2 节，公式（4）与公式（5）

</div>

</div>

<div class="equation-block" markdown="1">

#### GRPO 风格裁剪策略目标

$$
\mathcal{L}(\theta)=-\frac{1}{BG}\sum_{i=1}^{B}\sum_{g=1}^{G}\frac{1}{T_{i,g}}\sum_{t=1}^{T_{i,g}}\min\!\left(\rho_{i,g,t}(\theta)A_{i,g,t},\operatorname{clip}\!\left(\rho_{i,g,t}(\theta),1-\varepsilon,1+\varepsilon\right)A_{i,g,t}\right)+\beta\,\mathrm{KL}\!\left(\pi_\theta\,\|\,\pi_{\mathrm{ref}}\right),\qquad \rho_{i,g,t}(\theta)=\frac{\pi_\theta(o_{i,g,t}\mid x_i,o_{i,g,<t})}{\pi_{\theta_{\mathrm{old}}}(o_{i,g,t}\mid x_i,o_{i,g,<t})}
$$

**符号说明**

- $\mathcal{L}(\theta)$：关于当前策略参数 $\theta$ 的待最小化训练损失。
- $\theta$：当前翻译策略的可训练参数。
- $B$：一个训练批次中的源句数量。
- $G$：每个源句采样的策略轨迹数量。
- $T_{i,g}$：第 $i$ 个样本第 $g$ 条生成轨迹的响应长度。
- $t$：生成轨迹中的词元位置。
- $\rho_{i,g,t}(\theta)$：当前策略相对于生成数据时旧策略的逐词元概率比。
- $A_{i,g,t}$：由组内均值和标准差归一化得到的逐词元优势值。
- $\operatorname{clip}$：将概率比限制在指定区间内的裁剪操作。
- $\varepsilon$：策略概率比的裁剪范围超参数；原文公式还用另一处 $\epsilon$ 表示优势标准化中的数值稳定项。
- $\beta$：KL 正则项权重。
- $\mathrm{KL}$：衡量当前策略与冻结参考策略差异的 Kullback–Leibler 散度。
- $\pi_\theta$：参数为 $\theta$ 的当前策略。
- $\pi_{\mathrm{ref}}$：冻结参考策略。
- $\pi_{\theta_{\mathrm{old}}}$：采样这些轨迹时使用的旧策略。
- $o_{i,g,t}$：第 $i$ 个样本第 $g$ 条轨迹在位置 $t$ 生成的词元。
- $o_{i,g,<t}$：该轨迹在位置 $t$ 之前已经生成的词元前缀。
- $x_i$：第 $i$ 个训练源句。

<div class="equation-explanation" markdown="1">

**直观理解**：优势为正的词元应提高生成概率，优势为负的词元应降低生成概率；概率比裁剪避免一次更新过猛，KL 项避免策略远离冻结参考模型。由于优势来自终局奖励与局部过程奖励的组合，该目标会同时优化最终译文和产生译文的中间步骤。<br>
**原文位置**：第 4.2 节，公式（10）与公式（11）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：奖励首先按粒度映射到词元：最后有效词元接收格式奖励 $r_{i,g}^{\mathrm{fmt}}$ 与结果奖励 $r_{i,g}^{\mathrm{out}}$，推理步骤中的词元接收按步骤长度均分的过程奖励，并由权重 $\lambda$ 控制其影响。对每个位置向后累加得到回报 $R_{i,g,t}$，因此终局奖励会作用于整条生成序列，而步骤奖励保留局部信用；再以同一源句的 $G$ 条轨迹总回报计算组内均值 $\mu_i$ 和标准差 $\sigma_i$，形成 $A_{i,g,t}=(R_{i,g,t}-\mu_i)/(\sigma_i+\epsilon)$。
优化时最小化带裁剪的 GRPO 风格损失：提高正优势词元的概率、降低负优势词元的概率，并用系数 $\beta$ 加权的 KL 项约束 $\pi_\theta$ 不要过度偏离 $\pi_{\mathrm{ref}}$。这里最终质量奖励仍提供主要任务方向，过程奖励负责区分具体中间步骤，格式奖励确保轨迹可解析；三者并非替代关系，而是分别解决“输出是否合规”“译文是否正确”和“哪一步促成或破坏正确译文”。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 领域感知 Long-CoT 冷启动**

使用从强教师模型蒸馏的结构化翻译推理样本进行全参数 SFT，样本覆盖 10 个领域以及 De$\rightarrow$En、En$\rightarrow$Zh、Zh$\rightarrow$En 三个方向。统一的 `<think>`/`<answer>` 结构使显式过程和最终输出具有清楚边界。

> 直观理解：该模块不是直接追求最终强化学习得分，而是先建立可读、可切分的翻译过程，降低模型在 RL 初期产生无格式输出或不可归因文本的风险。

**2. 参考似然差分过程奖励**

对包含前 $k$ 个推理步骤的上下文 $c_{i,g,k}$，冻结模型 $\pi_{\mathrm{ref}}$ 计算参考译文 $y_i^*$ 的教师强制对数似然 $\phi_{i,g,k}$；相邻前缀之差 $\phi_{i,g,k}-\phi_{i,g,k-1}$ 即第 $k$ 步的过程增益。相同的 $\pi_{\mathrm{ref}}$ 同时承担过程评分与 KL 正则参照，因此无需另训过程奖励模型。

> 直观理解：如果加入某一步后，参考模型更有把握逐词生成正确译文，这一步就获得正奖励；反之则被视为可能引入术语、语义或风格漂移。

**3. 多粒度信用分配**

序列级格式奖励取 $1$ 或 $-1$，结果奖励为归一化 BLEU、COMET、COMETKiwi 的等权平均；二者置于最后有效词元，步骤增益则除以该步骤词元数后分配到对应位置。逐词元回报将终局质量信号传播到全轨迹，同时保留过程奖励在具体步骤中的局部差异。

> 直观理解：只给整条轨迹一个总分无法知道哪一步应负责；把局部增益放回相应词元，模型才能有针对性地保留有用判断、压低有害判断。

**训练与推理**

训练阶段先在约 7K 条难度自适应 Long-CoT 样本上进行两轮全参数 SFT，初始化两个基础模型的显式翻译能力。随后使用独立的 20K 多领域平行语料进行两轮 RL：每个源句采样 8 条轨迹，计算格式、结果与过程奖励，完成词元级信用分配和组内优势标准化，再执行带 KL 正则的策略更新；冻结参考模型不更新，并同时用于过程势能计算和 KL 约束。
推理阶段仅需输入源句，由训练后的策略直接生成 `<think>` 与 `<answer>` 结构；使用 vLLM、温度 $0.0$ 和重复惩罚 $1.05$ 进行确定性解码。参考译文、BLEU、COMET、COMETKiwi 和冻结评分模型都只参与训练，不构成部署时的额外评分开销。

**复现信息**

为公平复现，冷启动阶段采用 Qwen2.5-7B-Instruct 与 Gemma2-9B-IT 两种骨干，最大输入长度为 4096，学习率为 $1\times10^{-5}$；RL 阶段全局批量为 128，每个源句采样 8 条轨迹，采样温度为 $1.0$，最大响应长度为 2048，学习率为 $1\times10^{-6}$。关键奖励与约束超参数为过程奖励权重 $\lambda=0.1$、KL 系数 $\beta=1\times10^{-3}$；两个阶段均训练 2 轮并使用 8 张 NVIDIA A100 80GB GPU，RL 阶段约耗时 9 小时。
RL 数据覆盖 De$\rightarrow$En、En$\rightarrow$Zh 和 Zh$\rightarrow$En：各领域随机抽取 2K 对句子，并保留源端至少 20 个词或中文 20 个字符的样本，以给显式推理留出空间。过程步骤通过双换行符切分，这一规则直接决定步骤级奖励的归因边界，因此比优化器、调度器等常规细节更影响方法解释与复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- WMT22：用于英德、英中双向翻译评测，并同时承担句子级、文档级和难度分层分析。文档级部分重点测试实体、时态、代词和篇章标记等跨句现象；原文节选未明确报告样本规模与具体划分。
- Multi-Domain 与 Guofeng WebNovel：前者提供德译英多领域样本，后者提供中译英网络小说样本；两者与 WMT22 一起被 DeepSeek-V3 划分为五个难度等级，用于观察普通大语言模型与推理模型的性能随难度如何变化。原文节选未明确报告规模和划分。
- WMT23 Terminology Shared Task：提供带源语—目标语术语对齐的双语句对。评测时只向模型提供源句，再检查译文是否生成预期目标术语，从而隔离术语控制能力；原文节选未明确报告所用样本数和划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**BLEU、COMET 与 COMETKiwi**

BLEU衡量译文与参考译文的词片段重合；COMET利用学习式模型评估语义翻译质量；COMETKiwi属于无参考或质量估计式指标。三者共同刻画句子级总体质量，但不能充分发现跨句一致性、风格或术语错误。 （均为越高越好，因为更高分通常表示与参考译文或质量模型所认可的正确翻译更接近。）

</div>
<div class="metric-item" markdown="1">

**BlonDe**

面向文档级机器翻译的指标，关注实体、时态、代词及篇章标记等话语现象，用于补充句子级指标容易遗漏的跨句连贯性和一致性问题。 （越高越好，因为更高分表示文档级话语现象处理得更一致。）

</div>
<div class="metric-item" markdown="1">

**GEMBA-MQM 与术语准确率**

GEMBA-MQM依据 MQM 错误体系统计严重度加权错误、错误率以及准确性、流畅性、漏译、风格和术语等类别；术语准确率则直接检查预期目标术语是否出现。前者分析整体及细粒度错误，后者专门测试领域词汇控制。 （GEMBA-MQM 严重度分数、错误率和错误类别占比越低越好；术语准确率越高越好。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### WMT22 文档级翻译：比较普通大语言模型与大型推理模型的篇章处理能力。

<div class="result-value" markdown="1">

作者报告组内最佳 LRM 的 BlonDe 为 36.17，高于组内最佳 LLM 的 35.79；与此同时，句子级最高 BLEU 和 COMET 来自 LLM，LRM 只在 COMETKiwi 上领先。

</div>

该结果支持显式推理更可能帮助跨句实体、代词、时态和篇章一致性，而非无条件提高所有句子级指标。差距只有 0.38 分，且节选没有显著性检验，因此不能据此断言 LRM 在文档翻译上普遍或显著优于 LLM；它更适合作为后续过程对齐研究的现象证据。

<div class="result-source" markdown="1">

来源：第 2.1 节，Document-level Evaluation；Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At the document level, the best LRM obtains the highest BlonDe score (36.17 vs. 35.79 for the best LLM), suggesting that explicit reasoning may be more useful for discourse phenomena.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 五级翻译难度分析：在 Multi-Domain、WMT22 和 Guofeng WebNovel 上比较普通 LLM 与 LRM。

<div class="result-value" markdown="1">

作者观察到普通 LLM 在简单输入上具有竞争力，但从 Level 2 起，LRM 在 COMET 和 COMETKiwi 上持续超过普通 LLM；表 2 中不同模型和难度等级的绝对分数同时表明，难度升高并不保证每个 LRM、每项指标都优于所有 LLM。

</div>

这说明显式过程的价值主要在复杂决策场景中显现：模型需要先消解歧义、拆分复杂结构，再保持前后翻译一致。该实验是相关性分析而不是受控因果实验，因为难度等级由 DeepSeek-V3 自动分配，且采用组内最优比较；因此它不能排除模型规模、训练数据或难度标注偏差的影响。

<div class="result-source" markdown="1">

来源：第 2.1 节，Impact of Translation Difficulty；Figure 6、Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A clear pattern emerges: while traditional LLMs perform competitively on easy inputs, their performance drops sharply as difficulty increases, whereas LRMs surpass them from Level 2 onward and maintain consistent advantages on COMET and COMETKiwi.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 60 个样本的专家人工偏好评测：PAMT 分别与 GPT-5、DeepSeek-V3 和 CoT-FT 比较。

<div class="result-value" markdown="1">

PAMT 对 GPT-5 的胜、负、平比例为 15.0%、26.7%、58.3%；对 DeepSeek-V3 为 21.7%、26.7%、51.7%；对 CoT-FT 为 61.7%、11.7%、26.7%。因此 PAMT 与两个强通用模型的多数样本被判为平局，但其负率仍高于胜率；相对 CoT-FT 则获得明确多数偏好。

</div>

人工判断与自动指标方向一致，降低了改进完全来自指标迎合的可能性。最有力的证据是 PAMT 明显优于 CoT-FT，说明完整过程对齐方案比单纯思维链微调更有实际价值；但与 GPT-5、DeepSeek-V3 的结果只能说明“具有竞争力”，不能解释成 PAMT 已经胜过这些模型。样本仅 60 个，节选也未报告置信区间或显著性检验。

<div class="result-source" markdown="1">

来源：Appendix D，Table 18

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

PAMT vs. CoT-FT 61.7 11.7 26.7

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 给定节选缺少 PAMT 在域内、域外和多语设置中的完整自动评测表，也没有提供关键组件移除实验。因此无法从当前材料定量判断步骤级过程奖励、序列级结果奖励和冷启动领域 Long-CoT 监督各自贡献了多少；消融列表只能留空。
- 部分结论依赖自动评估器：难度等级和 GEMBA-MQM 标注均使用 DeepSeek-V3，可能引入同一评估模型的偏好。人工评测虽可交叉验证，但仅覆盖 60 个样本，且未报告置信区间、显著性检验、领域分布或标注者一致性，结论仍需对照原文完整实验设置复核。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 普通大语言模型组，包括 GPT-4o、DeepSeek-V3 和 Gemini-2.0-Flash。它们不以显式长推理过程为主要输出形式，用于判断显式过程相对直接翻译是否真正有益。
- 大型推理模型组，包括 OpenAI-o1、DeepSeek-R1、OpenAI-o3-mini 和 Gemini-2.0-Flash-Thinking。它们显式生成中间过程，是检验“推理是否有助于翻译、又是否引入领域漂移”的直接参照。
- GPT-5 与 DeepSeek-V3：在人类偏好实验中分别作为强通用模型参照；该比较检验 PAMT 的译文是否能在人类判断下接近强闭源或强通用模型，而非只在自动指标上占优。
- CoT-FT：领域思维链微调基线，在人工评测中代表仅使用显式过程监督、但未体现 PAMT 完整过程对齐机制的方案。它用于判断 PAMT 相对传统过程微调是否具有可感知优势。

**实验想回答的问题**

- 显式翻译过程在什么条件下有助于多领域机器翻译？预备实验分别考察输入上下文长度和翻译难度，以判断推理型模型的优势是否主要出现在需要跨句一致性、歧义消解、组合分解或反复修订的样本上。
- 显式推理是否会损害领域敏感决策，以及 PAMT 的改进是否只是假象性的自动指标提升？实验以风格错误、术语控制和人工偏好为重点，检验过程推理能否在保持整体翻译质量的同时遵守领域约束。

**实验实现**

预备评测覆盖 15 个领域以及英中、英德四个翻译方向。作者采用“组内最优”协议：不是固定挑选一对模型，而是分别报告普通大语言模型组和推理模型组中的最佳表现，以比较两种范式可达到的上限。难度实验由 DeepSeek-V3 将 Multi-Domain、WMT22 和 Guofeng WebNovel 的源句划分为五级；MQM 分析同样使用 DeepSeek-V3 充当 GEMBA-MQM 自动标注器，因此错误分析依赖该模型的判断。人工偏好实验抽取 60 个样本，每个样本由三名专家标注，并将 PAMT 分别与一个强 LLM、一个强 LRM 和一个强机器翻译基线比较。节选没有给出 PAMT 完整自动评测表、解码参数、显著性检验或标注者一致性。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 节选未提供逐例翻译、显式中间步骤或错误修正案例，因此无法核查 PAMT 究竟在哪一步纠正了术语、歧义或篇章一致性问题。现有定性解释来自聚合结果：LRM 在复杂输入上更强，却在风格与术语类别上更脆弱，这与作者提出的过程级信用分配问题一致，但尚不能替代具体案例证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出结合长思维链监督、结果奖励和步骤级过程奖励的强化学习后训练框架，以改进多领域机器翻译。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`bb8026d8c6d6191e5b8f8c5ede42c215f1891136dd99efc411cd92632a83cb7a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
