---
title: "[论文解读] What Drives LLM Self-Reflection? A Controlled Ablation of Uncertainty Routing in Armed Conflict Forecasting"
description: "[arXiv 2608.12322][LLM Reasoning] 本文通过六条件受控消融研究大语言模型自我反思的有效成分，指出性能提升主要来自“按不确定性类型选择不同后续动作”的类型化动作路由，而非结构化诊断问题或不确定性分类术语本身。"
arxiv_id: "2608.12322"
announcement_date: "2026-08-14"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T03:03:37.600319+00:00"
source_sha256: "84112376dd07f51f8bfc3c9eda30527794622b3cf9c6e9a92a1936279f71a53a"
tags:
  - "LLM Reasoning"
  - "大语言模型自反思"
  - "不确定性路由"
  - "受控消融"
  - "元认知智能体"
  - "武装冲突预测"
  - "证据质量监控"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.12322</p>

# What Drives LLM Self-Reflection? A Controlled Ablation of Uncertainty Routing in Armed Conflict Forecasting

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Poli Nemkova, Haeshitha Indukuri</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> University of North Texas；College of Computer Science</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12322v1) · [PDF 下载](https://arxiv.org/pdf/2608.12322v1) · **关键词** 大语言模型自反思, 不确定性路由, 受控消融, 元认知智能体, 武装冲突预测, 证据质量监控<br>


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

本文通过六条件受控消融研究大语言模型自我反思的有效成分，指出性能提升主要来自“按不确定性类型选择不同后续动作”的类型化动作路由，而非结构化诊断问题或不确定性分类术语本身。

**不用术语来说**：面对证据冲突、信息不足或超出既有经验的武装冲突案例，大语言模型的首次预测可能不可靠；常见补救办法是让模型再思考一次，但“自我反思”通常同时改变提示问题、概念标签和后续处理方式，因此即使结果改善，也无法判断究竟是哪一部分真正起作用。这种机制不清会使系统设计者增加复杂提示，却未必获得更好的预测。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将自我反思拆分为证据暴露、诊断脚手架、分类体系词汇和动作路由四个组成部分，并设计六个条件及词汇匹配对照，使结构化提问、术语暴露和类型化路由的作用可以分别检验。
- 作者提出包含七类不确定性的行动导向分类体系及确定性控制策略，并据消融结果主张：类型化动作路由是主要性能驱动因素；该结论在两种模型骨干上方向一致，但跨国家迁移和总体效应大小仍需更大规模验证。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型自反思、智能体控制与武装冲突预测的交叉领域。所谓自反思，是让模型在给出最终答案前检查已有证据或先前推理，并据此修正预测；但常见框架往往同时引入额外证据、诊断问题、描述不确定性的术语以及后续行动，因而无法判断性能提升究竟来自哪一部分。本文将这一过程拆成四个可控成分：证据暴露、诊断脚手架、不确定性分类词汇和行动路由，并在真实武装冲突预测中逐项消融。其关键背景假设是：预测错误不仅可能源于模型推理不足，也可能源于证据缺失、证据冲突或分布外情形；因此，仅估计“有多不确定”并不充分，还需要判断“不确定性属于什么类型”，再选择相应的纠正行动。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大语言模型自反思**

指让模型审查证据、推理过程或初步答案，然后再次作答的机制。它可能改善结果，但“再想一次”通常混合了诊断、提示词和行动等多个因素，不能直接说明真正有效的因果成分。

</div>
<div class="concept-item" markdown="1">

**不确定性类型与行动路由**

不确定性类型用于区分证据不足、证据冲突等不同认识状态；行动路由则依据诊断类型选择不同的纠正操作。通俗地说，它不是对所有疑难情况统一要求模型反思，而是针对不同问题采取不同补救办法。

</div>
<div class="concept-item" markdown="1">

**受控消融实验**

消融实验通过移除或替换系统中的特定成分，观察性能变化以识别该成分的作用。本文设置六种条件，并特别使用“分类词汇相同但行动空间固定”的控制条件，以区分术语提示本身与分类后采取不同动作的效果。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务以真实世界武装冲突案例及其可用证据为输入，要求大语言模型输出冲突预测；节选未进一步给出标签空间、预测时间范围或单条输入格式。研究场景包含五个国家的$310$个案例，并使用Llama-3.3-70B与GPT-4o两个模型骨干；另在$12$个留出国家上考察迁移，但原文指出迁移结果并不一致。系统在预测前加入证据质量监控层：监控器识别证据层面的认识不确定性，再由控制策略$\pi_{\text{control}}$把不同类型映射到相应纠正行动。六条件设计分别控制证据暴露、诊断脚手架、分类词汇和行动路由，从而回答一个机制识别问题：自反思的收益来自额外诊断提示或不确定性术语，还是来自“诊断类型决定后续动作”的路由机制。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\pi_{\text{control}}$**

确定性控制策略：把监控器识别出的不确定性类型映射为对应的纠正行动。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{F1}$**

用于评价预测分类表现的F1分数，即精确率与召回率的调和平均；本文据此比较不同自反思条件。

</div>
<div class="notation-item" markdown="1">

**$\Delta\mathrm{F1}$**

两个实验条件之间的F1分数差，用于表示加入或替换某一机制后的性能变化。

</div>
<div class="notation-item" markdown="1">

**$p$**

统计检验的p值，用于判断观察到的条件差异是否足以反对“无差异”的零假设。

</div>

</div>

**直接相关的工作**

- **Reflexion（Shinn et al., 2023）**: 该框架把语言形式的自我批评写入情景记忆，是自反思智能体的直接代表；但它同时包含多个设计成分，未单独识别诊断脚手架、分类词汇与行动路由各自的作用。
- **Degeneration-of-Thought（Liang et al., 2024）**: 该工作指出无约束自反思可能无法摆脱既有的错误承诺。本文把这一问题落实为控制机制：不同认识状态应路由到不同纠正行动，以检验定向行动是否比统一的泛化反思更能打破退化预测。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

武装冲突预测需要综合异质、可能矛盾且随时间变化的证据，同时面对类别不平衡、延迟真值和真实的人道风险。模型一旦对新型冲突形成错误的固定先验，简单地要求其“反思”未必能纠正判断；若预测系统无法说明它识别了哪种不确定性、采取了什么修正动作，也难以接受审计或在高风险场景中由人类监督使用。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **通用或非结构化自我反思**：向模型重新呈现已有证据，并要求其检查、反思或修订首次答案，但不明确区分不确定性的来源，也不为不同问题规定不同处理动作。其优势是实现简单，缺点是所有失败模式基本共享同一种“再想一次”的修正过程。
- **结构化诊断式自我反思**：使用预设诊断问题或不确定性分类词汇，引导模型检查证据冲突、信息不足、分布变化等潜在问题。一些设计还会依据诊断类型选择后续推理策略，但既有整体式评估往往同时加入诊断问题、术语和动作，因而难以把收益归因于某个单独组件。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有研究通常证明“加入自我反思后的完整系统”优于单次作答，却没有控制模型再次接触证据、结构化诊断提示、分类术语和后续动作空间等混杂因素；因此观察到的增益不能回答哪一组件具有因果贡献，也无法指导应保留哪些设计。
- 仅让模型说出不确定性类型，或让它回答更多诊断问题，不保证预测会被有效修正；如果所有诊断最终仍触发同一个通用动作，分类可能只是增加描述性词汇和提示长度，而没有改变模型处理证据的方式。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一个具有词汇匹配和动作空间控制的受控消融框架，用来区分“模型看到了分类术语”与“模型根据分类执行了不同动作”这两种效应，并检验该机制能否跨模型骨干成立。尤其需要排除两种替代解释：收益是否只是来自更详细的诊断脚手架，或只是来自显式的不确定性词汇。

</div>
<div markdown="1"><span>核心问题</span>

在大语言模型的自我反思流程中，真正驱动武装冲突预测改进的是证据再次暴露、结构化诊断问题、不确定性分类词汇，还是将不同不确定性类型映射到不同修正策略的类型化动作路由？

</div>
<div markdown="1"><span>作者直觉</span>

不同错误需要不同补救方式：证据互相冲突时应比较来源并裁定可信度，信息不足时应降低断言强度或寻找补充依据，分布变化时则应避免机械沿用历史模式。分类标签只有在改变下一步操作时才可能产生稳定价值；类型化路由相当于先识别“哪里出了问题”，再把案例送往对应的处理程序，因此比统一要求模型重新思考更可能打破错误先验。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文把自反思建模为一个“监控—诊断—路由—修正”的推理流程。系统输入初始预测、置信度、关键证据及结构化证据包；监控器先检查证据是否充足、及时且一致，再为当前认知状态分配唯一的不确定性类型；随后固定控制策略 $\pi_{\mathrm{control}}$ 将该类型映射到针对性的补救动作，最后由模型执行动作并修订预测。方法的关键不在于让模型写出更多反思文本，而在于让不同问题触发不同操作，例如证据不足时扩展信息来源，来源冲突时逐项比较，分布偏移时调整地区基线。
为识别究竟哪个组件产生作用，作者设计六个条件，并保持相邻条件只改变一个架构因素。条件链 $A\rightarrow E\rightarrow B\rightarrow F\rightarrow D\rightarrow C$ 依次引入自由反思、结构化诊断问题、分类词汇、动作路由和类型特异性；其中随机类型与“仅分类词汇”条件构成关键反事实，使分类名称本身、路由结构以及正确诊断带来的贡献可以分开考察。整个控制策略是人工固定的确定性映射，不通过实验数据学习，以免把分类体系的效果与策略训练的效果混在一起。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造当前预测状态

基础预测器根据证据生成当前预测，并同时给出置信度与关键依据；这三项与原始证据包共同组成监控器可读取的状态。

<div class="method-step__io" markdown="1">

**输入**：待预测的武装冲突案例，以及结构化证据包，包括 ACLED 冲突统计、社会经济指标、机器学习集成分数和来源质量评估。<br>
**输出**：包含预测结果、置信度、关键证据和结构化外部证据的当前预测状态。

</div>

**直观理解**：可以把它理解为先完成一份初稿，同时把“答案是什么、自己多确定、依据是什么”一起交给复核者。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 诊断证据与推理状态

完整系统中的监控器回答五类诊断问题，分别检查证据量、时效性、机器学习模型间的一致程度、可能的反论据以及当前预测的薄弱点；随后按固定顺序遍历决策树，且恰好分配一个不确定性类型。

<div class="method-step__io" markdown="1">

**输入**：当前预测状态。<br>
**输出**：一个类型标签，例如 $\mathrm{Insufficient\_Evidence}$、$\mathrm{Conflicting\_Sources}$ 或 $\mathrm{Distribution\_Shift}$。

</div>

**直观理解**：这一步类似故障排查：不只问“有没有问题”，还要判断问题是资料太少、资料互相矛盾，还是当前案例已经不同于历史常态。顺序化检查用于减少模型直接落入含义宽泛类别的倾向。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行类型化动作路由

确定性控制策略计算 $a=\pi_{\mathrm{control}}(u)$，将不同类型派发到请求更多来源、逐来源比较、情境再校准、来源重加权、优先近期证据、采样替代推理路径或直接退出等动作；无法分类的后备类型被派发到比较推理。

<div class="method-step__io" markdown="1">

**输入**：诊断得到的不确定性类型 $u\in\mathcal{U}$。<br>
**输出**：一个与诊断类型对应的补救动作 $a\in\mathcal{A}$，或在诊断为 $\mathrm{Confident}$ 时输出退出动作。

</div>

**直观理解**：核心思想是“对症处理”：资料不足与资料冲突不能使用同一种反思指令，因为前者需要寻找更多证据，后者需要裁决已有证据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行补救并形成最终预测

模型按照指定动作重新处理证据或扩展候选推理路径，再修订预测；若动作是退出，则保留当前预测而不继续 deliberation。

<div class="method-step__io" markdown="1">

**输入**：当前预测状态和路由得到的补救动作。<br>
**输出**：最终的冲突预测，以及经相应补救过程更新或保留的推理结果。

</div>

**直观理解**：诊断标签本身不会直接改善答案，真正改变预测的是标签触发的后续操作；若系统判断已有结论足够可靠，则停止额外推理以避免无效修改。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 类型化确定性控制策略

$$
\pi_{\mathrm{control}}:\mathcal{U}\rightarrow\mathcal{A},\qquad a=\pi_{\mathrm{control}}(u)
$$

**符号说明**

- $\pi_{\mathrm{control}}$：固定的确定性控制策略，即从诊断类型到补救动作的派发规则。
- $\mathcal{U}$：不确定性类型空间，包含七个主要类型，并在系统描述中另设无法分类时使用的后备类型。
- $\mathcal{A}$：动作空间，包括请求来源、比较推理、情境再校准、来源重加权、近期证据优先、替代路径采样和退出。
- $u$：监控器为当前预测状态分配的唯一不确定性类型。
- $a$：控制策略依据类型选择的补救动作。

<div class="equation-explanation" markdown="1">

**直观理解**：该映射表达论文的核心机制：系统先确定当前属于哪类认知问题，再执行该问题专属的修正动作。它是确定性的，因此同一类型总是触发同一动作，便于把性能变化归因于类型化路由，而不是额外训练出的策略。<br>
**原文位置**：第 3.2 节，Table 1；第 3.3 节

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。原文所述方法不是通过损失函数优化分类器或控制策略：$\pi_{\mathrm{control}}$ 被人工固定，诊断依据五问题协议和有序决策树完成。作者明确选择非学习策略，是为了避免把分类体系的诊断贡献与策略学习本身的贡献混淆；给定节选未报告任何额外训练目标、参数更新过程或监督标签构造方法。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 五问题监控器与有序诊断树**

监控器读取预测、置信度、关键证据和结构化证据包，通过五类问题显式检查证据量、时效性、模型一致性、反论据与弱点。问题回答随后进入按顺序检查条件的决策树，输出且仅输出一个类型；作者说明这些问题的作用是暴露类型判定所需证据，而不是被假设为独立的性能来源。

> 直观理解：监控器负责把模糊的“我不确定”转换成可操作的故障描述。有序决策树提供统一判定程序，避免不同样本随意使用过于宽泛的标签。

**2. 动作规定型不确定性分类体系**

体系包含七个主要类型：$\mathrm{Insufficient\_Evidence}$、$\mathrm{Conflicting\_Sources}$、$\mathrm{Distribution\_Shift}$、$\mathrm{Low\_Quality\_Data}$、$\mathrm{Temporal\_Inconsistency}$、$\mathrm{Model\_Ambiguity}$ 和 $\mathrm{Confident}$；另设 $\mathrm{Unknown\_Uncertainty}$ 作为无法归类时的后备类型。它不是只描述不确定性的来源，而是让每个类型直接对应一种应采取的推理操作。

> 直观理解：分类的价值取决于它能否改变下一步行为。例如“来源冲突”要求比较来源，而“模型歧义”要求探索替代预测路径；只给两者命名却仍执行同一动作，就没有实现类型化控制。

**3. 确定性控制策略与反事实控制条件**

控制策略 $\pi_{\mathrm{control}}$ 是固定映射而非学习策略。条件 $F$ 保留完整分类词汇但把所有非 $\mathrm{Confident}$ 类型压缩为同一比较推理动作；条件 $D$ 保留多动作路由结构，却从六个实质性类型中均匀随机抽取类型；条件 $C$ 则使用监控器诊断的真实类型进行确定性路由。

> 直观理解：固定映射使实验只回答“按类型派发动作是否有用”，不会同时引入策略学习能力。两个控制条件分别拆掉“动作差异”和“正确配对”，因而能区分分类词汇、拥有多种动作以及诊断与动作正确对应这三件事。

**训练与推理**

训练方面，给定节选没有描述对语言模型、监控器或控制策略进行参数训练，因而不能推断存在微调或强化学习。推理时，条件 $A$ 直接生成一次预测；其余条件加入监控阶段，但按实验配置改变诊断与动作空间：$E$ 不使用五个结构化问题而自由反思并分配类型，$B$ 使用问题但动作仅为退出或比较推理，$F$ 使用完整类型词汇却把所有非 $\mathrm{Confident}$ 类型映射到比较推理，$D$ 从六个实质性类型中均匀随机抽样后执行相应动作，$C$ 则根据证据诊断类型并由固定策略选择动作。动作执行后，模型修订预测；若路由到退出，则不再进行额外推理。

**复现信息**

公平解释实验所需的关键实现约束有三点。第一，各条件共享当前预测与结构化证据来源，完整监控器读取 ACLED 统计、社会经济指标、机器学习集成分数和来源质量评估；第二，决策树按固定顺序检查条件，并强制输出一个类型，以降低默认选择宽泛、高熵类别的可能；第三，六条件构成逐步消融链，作者声称每个相邻条件仅有一项架构变化，其中 $E$ 对 $B$ 检验结构化问题，$B$ 对 $F$ 检验分类词汇，$F$ 对 $D$ 检验多动作路由结构，$D$ 对 $C$ 检验类型特异性。完整提示词位于原文列出的 GitHub 仓库，但给定节选未提供模型采样参数、决策树全部阈值、预测标签定义或补救动作提示词全文，因此仅凭本节不能完全复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 主要评测集以 ACLED 事件数据构造二分类任务：输入过去 60 天的结构化冲突证据，预测未来 14 天死亡人数是否超过此前两周基线的 130%。数据覆盖苏丹、埃塞俄比亚、索马里、缅甸和乌克兰，每国按时间将最早 60% 样本用于训练、最近 40% 用于测试，共 310 个测试样本、每国 62 个，时间覆盖 2023 年末至 2026 年初；升级事件占 21.0%。该集合用于六条件主消融、国家分析和难度分析。
- 泛化集包含 12 个训练阶段未见国家，分布于非洲、欧洲、中东和美洲，共 300 个样本、每国 25 个，标签阈值与主要评测集相同。作者未依据该集合修改系统，因此它检验固定分类体系和路由策略的零适配跨国迁移能力，而不是重新训练后的性能。
- 难度分层不是独立数据集，而是按可观测属性预先划分主要测试集：29 个 catchable 样本具有明显动量信号，165 个 hard borderline 样本接近判定边界，116 个 hard deceptive 样本在预测窗口附近出现误导性动量下降。该划分独立于模型预测，用于判断路由机制在哪类证据结构上有效。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**F1**

精确率与召回率的调和平均，综合衡量模型识别升级事件时的漏报与误报。论文将三次独立运行的二分类输出先作多数投票，再计算主要 F1；由于正类仅占 21.0%，它比准确率更能反映少数类识别能力。 （越高越好，因为这表示模型在识别升级事件的覆盖率与预测可靠性之间取得了更好的平衡。）

</div>
<div class="metric-item" markdown="1">

**Recall**

真实升级事件中被模型正确识别的比例，直接反映漏报程度；它用于解释 F1 改善是否来自发现更多升级案例。 （越高通常越好，因为漏掉的真实升级事件更少，但仍需结合精确率或 F1，避免仅靠大量正类预测抬高召回率。）

</div>
<div class="metric-item" markdown="1">

**Brier score**

概率预测与二元真实标签之间的均方误差。论文对原始置信度进行五折交叉验证 Platt 缩放后计算该指标，仅作描述性校准评估，不用于选择或排序实验条件。 （越低越好，因为预测概率更接近实际结果；但本文各条件校准后的分数几乎相同，不能据此支持路由机制改善了概率校准。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Llama-3.3-70B 主要五国测试集：类型化监控 C 对单次基线 A

<div class="result-value" markdown="1">

条件 C 的 F1 为 0.379，条件 A 为 0.278，差值为 $\Delta\mathrm{F1}=+0.101$，bootstrap 95% 置信区间为 $[+0.020,+0.185]$；召回率由 0.385 提升到 0.677。不过逐样本 McNemar 检验的 $p=0.202$，未达到 $\alpha=0.05$。

</div>

作者据 bootstrap 区间主张完整类型化监控相对单次预测具有总体收益，且召回率表明收益主要表现为发现更多真实升级事件。分析上，这证明的是整套 C 相对 A 的效果，并不能单独归因于“类型与动作正确匹配”；同时，两种显著性分析结论不同，加上正类只有 65 个，证据应视为有支持但尚不稳固。

<div class="result-source" markdown="1">

来源：第 5.1 节，Finding 3；表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The overall gain of typed routing over the single-shot baseline is significant by bootstrap CI ($\Delta\text{F1}=+0.101$, 95% CI $[+0.020,+0.185]$, though not individually by McNemar at $p=0.202$).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### GPT-4o 跨骨干复现：通用反思 B、词汇条件 F 与随机动作路由 D

<div class="result-value" markdown="1">

GPT-4o 上 B、F、D 的 F1 分别为 0.272、0.304 和 0.345。F 相对 B 不显著，McNemar 检验 $p=0.773$；D 相对 B 显著，$p=0.025$，且正文报告 D 相对 F 的 $p=0.018$。

</div>

作者据此认为“分类词汇无明显增益、动作差异化产生增益”的分解能够跨 Llama 与 GPT-4o 复现。该结果支持动作路由比分类名称更关键，但 GPT-4o 仅运行一次，且随机路由 D 的 F1 高于类型化路由 C 的 0.328，因此它并未证明语义上正确的类型—动作匹配稳定优于任意动作变化。

<div class="result-source" markdown="1">

来源：第 5.4 节；表 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The key finding is that the ablation chain ordering replicates across backbones: generic reflection (B, $\text{F1}=0.272$) and vocabulary-only (F, $\text{F1}=0.304$) are statistically indistinguishable (McNemar $p=0.773$), while action routing (D, $\text{F1}=0.345$) significantly outperforms generic reflection ($p=0.025$) and vocabulary-only ($p=0.018$).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 12 个未见国家的零适配泛化测试

<div class="result-value" markdown="1">

单次基线 A、通用反思 B 和类型化监控 C 的总体 F1 分别为 0.260、0.290 和 0.280；B 与 C 均未显著优于 A，并且 B 的总体 F1 高于 C，逆转了主要五国测试中的排序。

</div>

这项结果界定了方法边界：固定的不确定性分类和控制策略没有自动迁移到不同冲突类型，通用回退甚至略优于类型化路由。作者进一步指出，五个国家因正例率接近零而所有条件 F1 均为 0，存在明显地板效应；因此总体结果同时混合了路由失配与极端类别稀缺，不能简单解释成反思在新国家完全无效。

<div class="result-source" markdown="1">

来源：第 5.5 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Neither generic reflection (B, $\text{F1}=0.290$) nor the typed monitor (C, $\text{F1}=0.280$) significantly outperforms the single-shot baseline ($0.260$) on 12 unseen countries, and generic reflection outperforms the typed monitor in overall F1 — reversing the primary evaluation result.

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

- 条件 A（Baseline）为单次直接预测，不加入监控或反思，是衡量整个自我反思流程是否优于原始模型判断的基准。
- 条件 E（No-Questions）允许模型反思，但不提供结构化诊断问题。它与条件 B 的比较专门检验问题脚手架本身是否有价值。
- 条件 B（Generic Reflect）使用 Q1–Q5 诊断脚手架，但将不确定情况交给通用反思动作。它是区分“进行了反思”与“根据不确定性类型采取不同动作”的核心参照。
- 条件 F（Vocab-Only）向模型展示完整的七类不确定性分类，但把所有非 Confident 类型都映射到与条件 B 相同的固定动作。它控制分类词汇带来的提示或认知框架效应，使条件 C 相对 F 的差异更接近动作路由本身的贡献。

**实验想回答的问题**

- 在武装冲突升级预测中，自我反思的收益究竟来自结构化诊断问题、不确定性分类词汇，还是由诊断类型触发不同处理动作的“类型化动作路由”？
- 上述机制能否跨越不同大语言模型骨干、国家冲突类型与样本难度成立，其有效范围和失效条件是什么？

**实验实现**

六个条件接收完全相同的证据包，包括 ACLED 冲突统计、社会经济指标、XGBoost 与随机森林的集成分数及模型间分歧，以及 LDA 主题信号，从而控制信息暴露差异。所有监控条件最多迭代一次，用于隔离反思结构而非循环深度。主要实验采用 Llama-3.3-70B，经 Groq API 推理，温度为 $T=0.2$；每个条件独立运行三次，二分类结果以多数投票聚合，概率置信度取均值。GPT-4o 跨骨干复现实验和跨国泛化实验均为单次运行。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 诊断问题消融：No-Questions E 对 Generic Reflect B | E 的 F1 为 0.297，B 为 0.296；McNemar 检验 $p=1.000$，F1 差值的 bootstrap 95% 置信区间为 $[-0.041,+0.040]$。 | 两者均允许反思，主要区别是 B 提供 Q1–Q5 结构化诊断问题。因此近零差值直接隔离出：在固定为一次监控、相同证据输入的设置中，问题脚手架本身没有可测价值。它不表示诊断问题在更多轮反思、其他任务或更大样本下必然无效。 | 第 5.1 节，Finding 1；表 2<br><span class="experiment-evidence">The no-questions monitor (E) scores $\text{F1}=0.297$, indistinguishable from generic reflection with Q1–Q5 scaffolding (B) at $\text{F1}=0.296$ (McNemar $p=1.000$, E right/B wrong $=22$, B right/E wrong $=21$).</span> |
| 词汇—路由消融：Vocab-Only F 对 Generic Reflect B，并以 Typed Monitor C 对 F 估计动作路由贡献 | F 的 F1 为 0.304，相对 B 的 0.296 仅增加 $\Delta\mathrm{F1}=+0.008$，两者 bootstrap 95% 区间高度重叠；控制分类词汇后，C 的 0.379 相对 F 增加 $\Delta\mathrm{F1}=+0.075$。但原文未明确报告 C 对 F 的配对显著性检验或差值置信区间。 | F 与 B 使用相同的实质动作，F 只额外展示完整分类体系，因此 F≈B 排除了“分类词汇仅靠提示效应就带来主要收益”的解释。C 与 F 都展示分类体系，但 C 根据类型选择不同动作，故二者差值是动作路由贡献的较保守估计；不过缺少该差值的直接显著性结果，不能把 0.075 当作已确证的因果效应。 | 第 5.1 节，Finding 2–3；表 2<br><span class="experiment-evidence">The gap from generic reflection is $\Delta\text{F1}=+0.008$ vs B, with bootstrap 95% CIs overlapping heavily; F and B are statistically indistinguishable.</span> |

**定性案例**

- 缅甸和乌克兰是最能说明机制的国家案例。缅甸中 A、B、F、D、C 的 F1 依次为 0.000、0.154、0.162、0.316、0.353；乌克兰对应为 0.167、0.091、0.100、0.432、0.500。F 与 B 在两国几乎相同，而引入动作差异的 D 和 C 大幅上升，支持收益来自路由而非分类词汇。作者将缅甸改善联系到 Distribution_Shift 诊断后的上下文重校准，将乌克兰改善联系到 Conflicting_Sources 与 Model_Ambiguity 诊断后的比较推理；这些机制解释来自模型诊断记录和国家级聚合结果，尚不是对单个预测过程的独立因果验证。证据位置：第 5.2 节、表 3。原文证据句：“Critically, Condition F (which presents the same taxonomy to the model but routes every diagnosis to a generic action) recovers only to $\text{F1}=0.162$ — essentially identical to generic reflection (B = $0.154$).”

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper experimentally isolates typed action routing as the mechanism behind gains from LLM self-reflection in forecasting reasoning.; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`84112376dd07f51f8bfc3c9eda30527794622b3cf9c6e9a92a1936279f71a53a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
