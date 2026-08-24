---
title: "[论文解读] Why2Speak: Faithful Reasoning for Abstaining Action Policies"
description: "[arXiv 2608.20670][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.20670"
announcement_date: "2026-08-24"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-24T02:09:11.545312+00:00"
source_sha256: "1ccac46e3b86dae2405d5073fdf375e8deda108ceea13695c924c190bc7bc57b"
tags:
  - "LLM Reasoning"
  - "LLM 机制与可解释性"
  - "弃权式行动策略"
  - "多方对话干预时机"
  - "链式思考忠实性"
  - "行动策略可审计性"
  - "大语言模型智能体"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.20670</p>

# Why2Speak: Faithful Reasoning for Abstaining Action Policies

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Shreya Mendi, Brinnae Bent</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Pratt School of Engineering, Duke University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.20670v1) · [PDF 下载](https://arxiv.org/pdf/2608.20670v1) · **关键词** 弃权式行动策略, 多方对话干预时机, 链式思考忠实性, 行动策略可审计性, 大语言模型智能体<br>


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

本文位于大语言模型智能体、对话干预时机与链式思考（Chain-of-Thought，简称 CoT）可解释性研究的交叉领域。许多智能体不仅要决定“说什么”，还要决定“是否现在行动”；因此，沉默或等待也是一种有意义的策略。本文把这一问题形式化为多方对话中的干预决策：模型观察当前对话前缀，判断此时发言是否能够提供有用的信息。研究重点不是单纯提高分类准确率，而是检验模型生成的理由是否真正反映了导致行动或弃权的内部计算，即理由是否对最终决策具有忠实性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**弃权式行动策略**

弃权式行动策略要求模型在执行行动与不执行行动之间选择；在本文中，行动是发言，弃权是保持沉默。沉默不是缺失输出，而是可能正确且有代价结构的决策。

</div>
<div class="concept-item" markdown="1">

**链式思考与理由忠实性**

链式思考是模型在给出最终行动前生成的一段中间推理文字。理由忠实性要求这段文字反映实际影响决策的计算，而不是在决定已经形成后生成的、听起来合理的事后解释。

</div>
<div class="concept-item" markdown="1">

**干预时机分类**

干预时机分类是在对话的多个决策点上判断模型应当立即发言还是等待。由于真正值得发言的时刻通常少于应当等待的时刻，该任务具有类别不平衡；同时，漏掉重要干预与不必要地打断对话的代价也可能不同。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个多方对话的前缀 $x$，模型在当前时间点输出二元行动决策 $a\text{（intervene）}$ 或 $a\text{（wait）}$；若选择干预，实际系统还可以进一步生成发言内容，但本文所研究的核心输出是是否现在发言。对话数据包含由事实纠正、概念定义、信息提供、来源识别以及综合或重构等知识缺口构成的合成场景，每个词元级决策点都被标注为应当干预或等待。本文使用同一 Qwen3-8B 模型的两种解码方式：$\text{no-think}$ 模式直接产生行动决定，$\text{think}$ 模式先生成显式推理再决定行动，从而在基本模型架构不变的情况下比较直接策略与推理策略。核心假设是：如果推理文本确实参与了行动形成，那么对推理过程进行受控删除、替换或内部激活分析，应能显示其与行动之间的稳定且具有因果意义的关系；但仅能从文本中预测行动，并不足以证明这种忠实性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

当前多方对话的前缀，即模型在某一决策点之前能够看到的输入。

</div>
<div class="notation-item" markdown="1">

**$a$**

行动标签，表示模型选择干预发言或等待沉默。

</div>
<div class="notation-item" markdown="1">

**$\text{think}$**

显式生成链式思考后再输出行动的推理解码模式。

</div>
<div class="notation-item" markdown="1">

**$\text{no-think}$**

不生成公开推理、直接输出行动决定的解码模式。

</div>

</div>

**直接相关的工作**

- **Nama 等（2026），When2Speak: a dataset for temporal participation and turn-taking in multi-party conversations for large language models**: 本文建立在该数据集及其对应的多方对话时序参与任务之上，将每个词元级决策点标注为 intervene 或 wait。该工作提供了干预时机的受控测试场景，而本文进一步研究在这一行动策略中，显式理由是否忠实以及训练和审计方法是否可靠。
- **Lanham 等（2023），Measuring faithfulness in chain-of-thought reasoning**: 该工作代表了主要面向问答任务的链式思考忠实性评估方向，例如通过干预或删减推理来检验理由与答案的关系。本文将问题扩展到行动与弃权决策，并指出问答式评估可能忽略沉默这一有效行动、类别不平衡、非对称行动代价，以及推理模式本身可能改变策略等因素。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

许多智能体不仅要决定“做什么”，还要决定“是否现在行动”。在多方对话中，助手可能需要立即发言纠正错误，也可能应保持沉默以避免打断。错误发言会增加干扰并削弱信任，错误沉默则可能漏掉重要干预机会。因此，系统若输出推理说明，该说明不仅应听起来合理，还应真实反映促成行动或弃权的内部计算，以便用户和开发者进行可靠监督。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **直接决策策略**：模型接收对话前缀，直接输出“发言”或“沉默”的动作，不生成显式链式推理。这类策略通常更适合优化最终决策质量，但外部观察者无法检查它为何选择行动或弃权。
- **显式推理与忠实性审计**：模型先生成理由，再输出动作；研究者随后使用激活探针或行为干预检验推理是否与动作有关。激活探针从模型内部表示预测最终动作，行为干预则删除或替换部分推理，观察动作是否改变。相关方法主要在问答任务中发展，而问答通常要求模型始终给出答案。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 问答式忠实性评估没有充分处理弃权动作的特殊结构：沉默本身是有意义的决策，且发言错误与漏掉干预的代价可能不同；同时，真实干预机会通常少于应保持沉默的时刻，形成严重类别不平衡。若直接使用准确率、概率贡献或不控制类别比例的探针，模型可能因偏向多数类而显得“忠实”或“可预测”，却没有真正识别干预依据。
- 让模型公开推理可能改变而非仅揭示其原有决策过程。显式推理模式与直接决策模式可能具有不同的行动能力；此外，删除推理时观察到的动作变化，也可能来自推理模式被关闭所引起的推理过程变化，而不一定说明被删除的文字本身具有因果作用。现有训练和审计方法因此难以同时保证决策性能、推理可检查性及因果忠实性。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚未解决的问题是：在具有不对称行动代价、严重类别不平衡且“沉默”也是有效动作的智能体策略中，如何定义并可靠评估忠实推理，并判断公开推理究竟是行动决策的真实组成部分还是事后合理化。尤其缺少对“能力—可审计性”权衡、训练方法能否弥合该权衡，以及探针和推理干预是否会产生误导性证据的系统研究。

</div>
<div markdown="1"><span>核心问题</span>

对于决定何时发言或沉默的弃权行动策略，显式推理是否真实参与了最终动作形成；在保持或提升决策质量的同时，监督微调和强化学习能否使这种推理更忠实、更可审计；以及哪些受类别不平衡、推理模式变化和模型置信度影响的评估方法会错误地高估忠实性？

</div>
<div markdown="1"><span>作者直觉</span>

将问题放入受控的多方对话干预时机任务，可以把“是否行动”从一般文本生成中分离出来，并在同一模型家族内比较直接决策与显式推理。若推理确实参与决策，那么在推理生成过程中，模型内部表示应逐步包含可预测动作的信息；有针对性的推理删除或替换也应改变动作，而仅改变推理模式不应被误认为文字的因果作用。与此同时，显式推理若消耗能力或改变推断路径，可能降低决策质量，因此该设置能够直接检验可审计性是否以行动能力为代价。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法不是提出一个新的模型架构，而是建立一套用于评估“可弃权行动策略”推理忠实性的完整实验流程。输入是多方对话前缀，模型需要输出二元行动：在当前时刻介入，或保持沉默；系统分别比较直接决策模式与先生成链式思考、再输出决策的推理模式，并通过监督微调、强化学习、表示探针和行为干预检验“公开的理由”是否真正参与了行动决策。直观地说，研究者不仅检查模型最后答得对不对，还检查它说出的理由是否与实际推动行动的内部过程一致，以及删除或替换理由后行动是否真的改变。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造二元行动决策任务

将每个对话前缀映射为二元标签 $y\text{（介入）}$ 或 $y\text{（沉默）}$，并依据原始场景标识恢复五类介入类型：事实纠正、概念定义、提供数据、识别来源、综合与改写；这些类型只用于解释性分析，不用于训练介入预测器。

<div class="method-step__io" markdown="1">

**输入**：约 $16{,}000$ 个合成多方对话及其约 $173{,}000$ 个 token 级决策点；每个决策点是一个对话前缀，标签表示此时应当介入还是保持沉默。<br>
**输出**：带有行动标签的二元分类数据集，以及供后续分析使用的场景类型元数据。

</div>

**直观理解**：每个样本都像是在会议进行到某一句话时暂停，要求助手判断“现在该不该插话”。研究者还记录插话属于哪种需求，但不让模型利用这一额外标签作弊。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成直接决策与显式推理策略

在 no-think 模式下，模型只生成最终决策 token；在 think 模式下，模型先生成自由形式的链式思考，再生成最终决策 token。比较基础推理策略、LoRA 决策 token 分类器、屏蔽推理 token 损失的监督微调策略，以及使用 GRPO 训练的推理策略。

<div class="method-step__io" markdown="1">

**输入**：对话前缀、Qwen3-8B 的指令微调权重，以及不同训练条件得到的模型策略。<br>
**输出**：每个决策点的最终行动、可选的生成推理文本，以及对应的隐藏状态。

</div>

**直观理解**：同一个助手可以像“只按按钮”一样直接决定，也可以先写下理由再按按钮。后续实验要判断：写理由是否提高了行动质量，还是反而改变了它原本的决定方式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在自然运行点评估行动质量

以 macro-F1 作为主要部署指标，同时计算 false-intervention rate 和 missed-intervention rate；使用 AUROC 作为不依赖阈值的诊断指标，以区分判别能力变化和决策阈值或校准变化，不进行事后阈值调优。

<div class="method-step__io" markdown="1">

**输入**：模型最终决策与人工行动标签，以及各策略对决策的概率输出。<br>
**输出**：各策略在介入和沉默两类上的平衡性能、误报介入率、漏掉介入机会率，以及阈值无关的区分能力。

</div>

**直观理解**：由于真正需要插话的时刻很少，只看总体准确率会被“大多数时候保持沉默”掩盖。因此，评估同时关心两种错误：不该插话时插话，以及该插话时没有插话。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 检验推理是否忠实于行动

使用表示探针测量隐藏状态何时能解码出介入决策；用行为干预比较完整推理、截断推理和长度匹配的中性填充，以区分对推理内容的依赖和对 think 格式的依赖；用双探针比较内部表示的介入类型与生成文本声称的类型。

<div class="method-step__io" markdown="1">

**输入**：推理过程中的隐藏激活、完整推理文本、截断推理文本、中性填充文本，以及模型声明的介入类型。<br>
**输出**：决策和类型在内部表示中的可解码性、行动对推理内容或推理格式的行为依赖，以及“内部理由—文字理由”的一致性证据。

</div>

**直观理解**：如果删掉真正有意义的理由会改变决定，说明理由可能参与了决策；但如果仅仅破坏“正在思考”的格式也会改变决定，就不能把这种变化误认为是对理由内容的依赖。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 忠实性增强的强化学习奖励

$$
r=\mathbb{1}[\text{decision correct}]\,(1+\lambda\,\mathrm{dep})
$$

**符号说明**

- $r$：单个采样 rollout 获得的强化学习奖励。
- $\mathbb{1}[\text{decision correct}]$：指示函数；当最终介入或沉默决策正确时取 $1$，否则取 $0$。
- $\lambda$：忠实性依赖奖励的权重，本文设为 $0.3$。
- $\mathrm{dep}$：行为依赖指标；完整推理完成后得到的最终决策与截断推理后的决策不同时取相应的正向信号。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标先要求模型把行动做对；只有做对时，完整推理对最终决定产生行为影响才会带来额外奖励。它试图鼓励“理由确实参与决定”，但不能自动保证这种参与来自理由内容，而不是来自 think 模式或截断造成的格式变化。<br>
**原文位置**：Methods—Reinforcement Learning Reward

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：监督微调包含两种目标：其一是直接预测最终介入决策，并在 no-think 模式下使用 LoRA 适配器训练；其二是保留自由形式推理，但在损失计算中屏蔽推理 token，只优化最终决策 token。强化学习从基础指令微调模型开始，使用 GRPO 对每个提示采样多条 rollout：准确率目标只奖励最终行动正确，忠实性目标则使用 $r=\mathbb{1}[\text{decision correct}](1+\lambda\,\mathrm{dep})$。这种优化连接了“行动正确”和“行动是否依赖自身推理”两个目标，但论文指出，当同一组 rollout 全部自信地选择错误行动时，组相对目标没有有效的相对学习信号。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双模式 Qwen 策略**

主实验使用 Qwen3-8B；该模型支持原生 think 与 no-think 解码，并共享底层权重。基础推理策略直接在 think 模式运行，决策 token 分类器通过 LoRA 微调后在 no-think 模式输出直接行动；研究还在 Qwen3-30B、Nemotron-3-Nano、GPT-4o、GPT-5.1 和 Llama-3.2-3B 上检查能力—可审计性权衡是否跨模型出现。

> 直观理解：这里的关键对照不是完全不同的模型，而是同一类语言模型是否被要求先解释再行动。这样可以更直接地观察“暴露推理”本身是否改变策略。

**2. 忠实性诊断模块**

表示探针是在缓存的隐藏状态上训练的带 $L_2$ 正则逻辑回归，只用于评估，不进入任何优化目标。行为干预同时使用完整推理、截断推理和中性填充；双探针分别分析内部介入类型与生成文本中的介入类型，以避免把文字泄漏或类别不平衡误当作内部推理证据。

> 直观理解：探针相当于在模型内部装一个小型读数器，观察某个信息是否已经存在；行为干预则像剪掉或替换说明书，再看按钮选择是否变化。两者结合可以避免只凭“能读出来”就断言该信息真正导致了行动。

**3. GRPO 奖励模块**

强化学习保留自由形式推理生成，并以最终行动正确性为基础奖励。忠实性版本使用 $r=\mathbb{1}[\text{decision correct}](1+\lambda\,\mathrm{dep})$，其中 $\lambda=0.3$，$\dep$ 表示完整推理相对于截断推理是否改变最终决策；激活探针不作为奖励目标。

> 直观理解：模型只有先做对决定，推理依赖奖励才会起作用；如果完整理由确实能改变决定，还会得到额外奖励。这样设计是为了避免模型直接迎合探针指标，却也可能把“依赖推理格式”误奖励成“依赖推理内容”。

**训练与推理**

训练阶段，数据输入为对话前缀及二元行动标签；LoRA 监督微调更新低秩适配器，GRPO 则保留推理生成并依据 rollout 奖励更新策略。每种强化学习目标使用三个随机种子，以比较目标之间的差异是否超过训练随机性。推理阶段，对同一前缀选择 think 或 no-think 解码；think 模式先生成链式思考再输出最终决策，no-think 模式直接输出决策，主要行动指标只读取最终决策 token。忠实性评估另外对已生成推理进行截断或替换为中性填充，并比较行动变化；探针读取缓存隐藏状态而不参与模型训练。

**复现信息**

主数据集约含 $173{,}000$ 个 token 级决策点，来自约 $16{,}000$ 个合成对话；真实介入机会约占 $13\%$，因此采用 macro-F1 而非仅报告总体准确率。主模型为 Qwen3-8B；LoRA 使用 rank $16$、$\alpha=32$、零 dropout 并作用于所有线性层，探针为带 $L_2$ 正则的逻辑回归。实验在单张 $24$ GB GPU 上运行；配对行为干预使用精确 McNemar 检验，适用处使用 bootstrap 置信区间，并始终在各策略的自然运行点评估，不进行事后阈值调优。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 匹配评估集：$n=400$，使用种子7；用于表1中主要策略的公平比较，任务是判断多方对话中助手应当干预发言还是保持沉默。原文未明确报告该集合的正式数据集名称、训练集规模和具体划分。
- 跨模型评估切片：从同一种子7的打乱结果中抽取200条；用于比较Qwen3-30B、Nemotron-3-Nano和Llama-3.2-3B等模型。该切片与上方400条评估集的绝对分数不可直接比较，但重叠部分结果接近。
- 训练与审计数据：Token-SFT、Masked-SFT和GRPO均围绕Qwen3-8B的干预决策与推理轨迹训练；Masked-SFT仅保留基础模型自然生成且最终决策正确的推理轨迹，后续审计还使用独立验证数据和不同随机种子的重复运行。原文未明确报告各训练集的完整规模和标准数据集名称。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Macro-F1**

对干预与不干预两个类别分别计算F1后取平均，衡量类别不平衡条件下的总体分类质量。 （越高越好；但它不能单独说明模型更偏向误报还是漏报。）

</div>
<div class="metric-item" markdown="1">

**FIR与MIR**

FIR（false-intervention rate）是错误干预比例，MIR（missed-intervention rate）是漏掉真实干预机会的比例；二者分别刻画两类不对称行动错误。 （均越低越好；但在干预成本和漏干预成本不同的场景中，不能只看其中一个指标。）

</div>
<div class="metric-item" markdown="1">

**AUROC**

接收者操作特征曲线下面积，衡量模型或线性探针在不同阈值下区分两类样本的排序能力；文中也用它评估隐藏激活是否编码干预决策。 （越高越好，0.5约对应随机排序；但高AUROC不代表当前部署阈值下的Macro-F1或行动成本一定更优。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 能力与可审计性的主要比较

<div class="result-value" markdown="1">

直接Token-SFT在no-think模式下获得最高的匹配评估Macro-F1（0.620），但同一检查点在think模式下下降至0.367；基础Qwen3-8B在think模式下Macro-F1为0.536，而no-think模式仅为0.096。基础模型的FIR也从0.989降至0.232，但MIR从0.026升至0.579，说明推理模式减少了几乎总是干预的行为，却增加了漏干预。

</div>

直接优化最终行动最有利于部署分类分数，但它牺牲了模型生成可检查推理的行为；基础模型的think模式则提供了较可审计的决策过程，却在干预机会识别上付出代价。该结果证明的是策略之间存在权衡，不是证明推理文本必然忠实，也不是证明较低FIR或较低MIR在所有应用中同等重要。

<div class="result-source" markdown="1">

来源：Results > Capability and Auditability > Reasoning is essential for the base model；表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

When decoded without reasoning, the base Qwen3-8B model predicts intervention for nearly every example, producing a macro-F1 of 0.096 and a false-intervention rate of 0.989. Decoding the same weights in think mode produces a policy that discriminates rather than always intervening (macro-F1 0.536, false-intervention rate 0.232). However, missed interventions rise from 0.026 to 0.579.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 监督微调、强化学习与跨模型复现

<div class="result-value" markdown="1">

Masked-SFT保留了约99%的推理生成，但未超过基础think策略；GRPO-accuracy和GRPO-faithfulness的Macro-F1分别为0.520和0.549，基础think策略为0.536，AUROC分别为0.640、0.622和0.637。作者根据独立运行的波动将这些差异视为不可区分。更大的Qwen3-30B和不同家族的Nemotron-3-Nano也表现为no-think较差、think改善；GPT-4o与GPT-5.1的零样本推理同样未稳定改善部署性能。

</div>

保留推理并不自动提供解决困难样本所需的监督，而加入准确性或忠实性强化奖励也没有可靠地超越基础推理策略。跨模型结果支持这种现象不是单一模型的偶然故障，但由于不同模型和切片的评估规模不同，不能把所有绝对分数直接横向排序。

<div class="result-source" markdown="1">

来源：Results > Reinforcement Learning；表1；Figure 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The base policy achieves a macro-F1 of 0.536, compared with 0.520 and 0.549 for the two RL variants, while AUROC remains statistically similar across all policies.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 决策形成与推理忠实性审计

<div class="result-value" markdown="1">

基础think策略的干预决策在线性探针中，推理前AUROC为$0.664\pm0.034$，接近纯文本基线的$0.631\pm0.053$，推理后升至$0.976\pm0.045$；直接分类器在no-think模式的推理前AUROC为0.997，而对应文本基线为0.621。行为控制显示，移除全部推理会使基础模型退化为几乎总是干预；但等长度中性填充比简单截断改变更多决策，保留原推理前半段相较中性填充仍能把预测拉回完整推理策略。

</div>

这些结果支持两种不同的决策形成过程：直接分类器在推理开始前就形成行动，而think策略的二元决策主要在推理过程中变得可解码。不过，推理后探针可能只是读取刚生成的文本，简单删减也会改变推理格式，因此原始探针或删减结果不能单独证明内部理由对行动具有因果作用；只有与中性填充对照后，才能观察到 modest 的内容效应。

<div class="result-source" markdown="1">

来源：Results > Decision Formation During Reasoning；Figure 2；Behavioral Dependence on Reasoning

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Pre-CoT activations achieve an AUROC of 0.664 ± 0.034, compared with 0.631 ± 0.053 for a text-only baseline. After reasoning, decision decodability rises sharply, reaching an AUROC of 0.976 ± 0.045.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主要结论依赖特定的对话干预任务、Qwen3-8B及有限的模型和评估切片；跨模型结果使用200条切片且绝对值与400条主评估不可直接比较，因此对其他任务、规模和架构的外推仍有限。
- 推理忠实性的测量仍受方法学混淆影响：推理后探针可能读取生成文本，原始推理删减会改变推理模式，自动提取的“陈述理由”与金标准类别的一致也不能直接证明内部因果忠实性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Base Qwen3-8B在no-think与think两种解码模式下的结果：控制模型能力本身与原生推理模式的作用，是所有微调和强化学习策略的核心参照。
- Token-SFT classifier：仅对最终干预决策标记进行监督微调；用于检验直接优化行动是否能提升部署性能，以及这种优化是否抑制可审计推理。
- Masked-SFT：保留模型原有推理文本但只对最终决策计算损失；用于检验在不直接压制推理的前提下，监督学习能否改善困难决策。
- RL-accuracy与RL-faithfulness：分别以准确性和行为忠实性为主要强化学习目标；用于比较奖励设计是否能改善推理策略，而不仅是改变最终行动。GPT-4o、GPT-5.1及其他基础模型则用于跨模型复现。

**实验想回答的问题**

- 在多方对话中，直接决策策略与生成推理的可审计策略是否存在能力—可审计性权衡？不同解码方式、监督微调和强化学习如何影响干预决策质量与推理可检查性？
- 暴露的推理是否真正参与了行动决策，以及常用的探针、推理删减和行为忠实性奖励能否可靠地测量或提升这种忠实性？

**实验实现**

主要模型为Qwen3-8B，分别以no-think和think解码；比较零样本模型、直接决策Token-SFT、Masked-SFT、GRPO准确性奖励和GRPO忠实性奖励。表1的主要匹配评估使用400条、种子7；跨模型结果使用200条切片。强化学习从基础think策略出发，并通过增加rollout多样性、可用梯度和训练时长检查是否存在欠训练；原文称有效梯度增加约5–10倍。推理形成位置通过推理前后隐藏激活上的线性探针评估，并采用同族评估、纯文本基线、嵌套层选择等控制。行为审计比较完整推理、截断推理和等长度中性填充，以区分推理内容效应和推理格式效应。不同强化学习目标还在独立随机种子下重复，以避免把单次运行差异误判为方法差异。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 推理格式控制：完整推理、截断推理与中性填充 | 移除推理会使基础模型退化为几乎总是干预；但等长度中性填充改变的决策多于简单截断，保留原推理前半段相对中性填充又能稳定地把预测拉回完整推理策略。原文未明确报告该消融的具体决策变化数值。 | 该设计隔离了推理内容与推理格式。若只比较完整推理和截断推理，模型可能因看到不完整或异常长度的格式而改变策略；中性填充提供格式匹配的对照。因此，作者认为推理内容确实有 modest 且统计可靠的影响，但原始截断分析会高估这种影响。 | Results > Behavioral Dependence on Reasoning；Appendix E<br><span class="experiment-evidence">However, replacing the removed reasoning with length-matched neutral filler changes even more decisions.</span> |
| 强化学习目标与训练强度消融 | 将奖励从准确性改为行为忠实性未带来可测量改善；在增加rollout多样性、可用梯度和训练时长后，估计有效梯度增加5–10倍，但留出集性能仍停留在相同水平。原文未明确报告扩展训练的具体分数。 | 这项消融排除了两个常见解释：结果差可能不是因为训练不够久，也不是因为忠实性奖励形式单纯不合适。更关键的问题可能是奖励本身依赖未经内容控制的原始推理扰动，模型只需依赖“存在推理段”即可获得奖励，而不必让真实推理内容更深地参与行动决策。 | Results > Reinforcement Learning；Appendix C<br><span class="experiment-evidence">Despite an estimated 5–10 × increase in effective gradient, held-out performance plateaued at the same level (Appendix C), suggesting that the observed limitation is unlikely to result from undertraining.</span> |

**定性案例**

- 一个具有代表性的行为模式是：Qwen3-8B在no-think模式下几乎对所有对话都选择干预（Macro-F1为0.096、FIR为0.989），切换到think模式后能够区分更多情形（Macro-F1为0.536、FIR为0.232），但MIR升至0.579。该案例说明“是否暴露推理”并非单纯的可观测性开关，而可能改变模型实际采用的行动策略。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper studies faithful chain-of-thought reasoning for LLM action-versus-abstention decisions and analyzes whether exposed reasoning reflects the underlying computation.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`1ccac46e3b86dae2405d5073fdf375e8deda108ceea13695c924c190bc7bc57b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
