---
title: "[论文解读] DiagEvo: Diagnosis-Guided Self-Evolution via Hierarchical Error Memory"
description: "[arXiv 2609.00768][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2609.00768"
announcement_date: "2026-09-02"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:46:46.846329+00:00"
source_sha256: "e01a1b7cfd769c0fce97b9345f91f61674d462b2165509773a4eef29ddc96edb"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "大语言模型自我进化"
  - "自博弈"
  - "错误诊断"
  - "分层记忆"
  - "课程学习"
  - "伪标签过滤"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.00768</p>

# DiagEvo: Diagnosis-Guided Self-Evolution via Hierarchical Error Memory

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Xincheng Wei, Yifan Ding, Yoshua Li, Dongsheng Ma, Rongxiang Weng, Xunliang Cai, Wenjian Ding, Yao Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: The Chinese University of Hong Kong, Shenzhen；Affiliation: Peking University；Affiliation: Faculty of Health Data Science, Juntendo University, Chiba, Japan；Affiliation: School of Statistics and Data Science, LPMC, KLMDASR & AAIS, Nankai University, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00768v1) · [PDF 下载](https://arxiv.org/pdf/2609.00768v1) · **关键词** 大语言模型自我进化, 自博弈, 错误诊断, 分层记忆, 课程学习, 伪标签过滤<br>


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

本文研究大语言模型的自我进化（self-evolution）与自博弈（self-play）。在该设定中，挑战者生成训练问题，求解器回答问题并利用回答结果更新自身；经过多轮交替，问题应持续处于求解器的能力边界附近，即既能暴露尚未掌握的推理弱点，又具有足够的可学习性。现有方法通常依据问题难度、可学习性或多样性调节生成，或者借助人工示例、文档语料和外部难度标签提供方向。DiagEvo关注的是一种不依赖外部任务资源的设定：从求解器历次失败轨迹中诊断反复出现的错误原因，并将这些原因转化为后续问题生成的课程信号。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自博弈与伪标签**

自博弈中，挑战者负责出题，求解器负责作答，二者在多轮交互中共同更新。由于没有人工标准答案，系统通常通过求解器对同一问题的多次回答进行多数投票，把票数最多的答案作为伪标签；该标签可能继承求解器自身的错误。

</div>
<div class="concept-item" markdown="1">

**能力边界与课程学习**

能力边界指求解器刚好能够部分解决的难度区域：问题太容易时不能带来明显进步，太难时回答不稳定且训练信号较弱。课程学习则是根据模型当前状态选择或生成合适的训练样本，使训练难度和内容随模型能力变化。

</div>
<div class="concept-item" markdown="1">

**错误原因记忆**

错误原因记忆不是简单保存完整问答，而是从失败与成功轨迹的差异中提炼可迁移的原因，例如某类推理步骤或概念使用错误。DiagEvo将相关原因组织在技能节点下，并以Active或Mastered状态表示某一原因是否仍需直接练习。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

系统在每一轮接收求解器已有的回答轨迹及其伪标签结果。诊断器比较与伪标签不一致的失败轨迹和一致的轨迹，抽取可跨问题迁移的错误原因，并将其写入分层错误原因记忆；挑战者依据记忆中的技能节点、错误原因状态和出现频次生成新问题，同时保留自由探索。随后，求解器对新问题进行多次回答，系统通过多数投票形成伪标签，并使用双重置信度过滤：对于中等难度问题，仅当最高票答案相对于第二高票答案具有清晰优势时才保留。最终输出是经过过滤的问题—伪标签训练对，求解器据此更新；训练产生的新失败轨迹再用于更新记忆。该设定假定求解器的失败历史包含可识别、可重复且能指导后续练习的错误模式，但不要求人工示例、外部文档或外部难度标签。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D$**

由挑战者生成、并经置信度过滤后用于求解器训练的问题—伪标签数据集。

</div>
<div class="notation-item" markdown="1">

**$q$**

挑战者生成的一个问题；其内容可以针对某个错误原因，也可以来自自由探索。

</div>
<div class="notation-item" markdown="1">

**$y$**

问题$q$对应的伪标签，通常由求解器多次回答后的多数投票得到。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{Active},\ \mathrm{Mastered}$**

错误原因的两种记忆状态：Active表示该原因仍是直接生成目标，Mastered表示求解器在相关问题上已达到较高自一致性，因而不再需要持续直接练习。

</div>

</div>

**直接相关的工作**

- **R-Zero**: R-Zero属于不依赖人工标注的自博弈方法，利用求解器反馈调节问题生成难度，但主要回答“问题对当前求解器有多难”，不能通过跨问题诊断回答“求解器为何失败”。DiagEvo保留无外部任务资源的设定，并进一步从失败轨迹中提取反复出现的错误原因。
- **DARC**: DARC代表使用外部任务资源的引导式自博弈方法，依赖难度标签、外部文档以及文档知情的特权教师来稳定问题生成或训练。DiagEvo试图在不使用这些外部资源的情况下，仅凭求解器失败历史建立动态课程信号。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在自博弈式语言模型自进化中，挑战者持续生成问题，求解器利用这些问题及其伪标签训练自身。若问题只追求难度、可学习性或多样性，生成内容可能逐渐变长、变复杂，却未必针对求解器反复出现的推理弱点，导致训练信号失效、性能停滞甚至下降。因此，研究需要一种能够在没有持续人工监督或外部任务资源的条件下，判断求解器究竟“错在哪里”，并据此安排后续练习的课程机制。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **无标签自博弈方法**：这类方法依据求解器对问题的回答来估计难度、学习性或多样性，再调整挑战者的问题生成。例如，系统倾向于保留处在求解器能力边界附近的问题，使问题既不过于简单，也不过于困难。但它们主要观察“答对还是答错”以及回答是否稳定，通常不跨问题归纳造成失败的共同推理原因。
- **有引导的自博弈方法**：这类方法借助自博弈循环之外的任务信息来确定生成方向，例如人工标注示例、文档语料、难度标签或由外部信息增强的教师模型。外部资源可以帮助稳定问题生成和训练，但课程方向不完全由求解器自身的交互历史产生，因而仍依赖额外的任务资源。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 无标签方法能够判断问题对当前求解器是否困难，却不能解释不同问题中是否存在同一类反复出现的错误原因。结果是挑战者缺少“下一轮应练习哪种能力”的直接信号，可能不断增加题面复杂度而没有真正处理未解决的弱点。
- 有引导方法依赖人工示例、文档、难度目标或外部教师等循环外信息；同时，过难或表述不清的问题可能产生高冲突的多数投票伪标签，若直接用于训练，求解器可能把共同错误进一步强化。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未充分解决这样一个闭环问题：如何仅利用自博弈过程中已经产生的求解器失败轨迹，跨问题提炼可迁移的重复错误原因，持续判断这些原因是否仍未掌握，并将判断结果转化为下一轮的问题课程，同时降低不可靠伪标签对训练的干扰。

</div>
<div markdown="1"><span>核心问题</span>

能否把求解器自身的失败历史转化为一种无需外部任务资源的动态课程信号，使挑战者既能针对尚未解决的推理错误生成问题，又能保留自由探索，并通过可靠性筛选避免高冲突伪标签损害后续训练？

</div>
<div markdown="1"><span>作者直觉</span>

单个错误轨迹只能说明一道题没有答好，但把失败轨迹与成功轨迹进行比较，并在多道题之间寻找重复的推理差异，就可能识别出比具体题面更稳定的错误原因。若把这些原因按相关技能组织起来，并记录其出现频率及求解器在针对性问题上的自洽程度，系统便能优先练习仍处于 Active 状态的弱点；当求解器在相关问题上表现稳定后，再将其标为 Mastered，转向其他原因或自由探索。与此同时，只保留多数答案具有明确领先优势的问题，可以减少多个答案竞争激烈时形成的不可靠训练标签。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

DiagEvo 是一个由“挑战者—求解器—诊断器”组成的交替自进化闭环。第 $t$ 轮结束后，诊断器从求解器的失败轨迹中抽取可复用的推理错误原因，将其组织为技能节点—错误原因两层记忆 $\mathcal{M}_t$，并为每个原因维护 Active 或 Mastered 状态及当前活跃阶段的失败频次。下一轮挑战者根据这些频次，在自由探索与针对 Active 原因的定向出题之间动态分配概率；候选题经过双置信度过滤后获得多数投票伪标签，再用于更新求解器。挑战者和求解器交替更新，一方训练时另一方冻结，只有挑战者直接读取错误记忆。

直观上，该方法不是单纯让模型不断生成“更难”或“更多样”的题，而是把求解器过去反复犯错的位置整理成一份可更新的错题病历。尚未解决且反复出现的问题会得到更多训练题；已较稳定掌握的问题退出直接靶向，但仍可与相关弱点组合出题；当旧错误再次出现时，它又会被激活。由此，课程方向来自自博弈内部产生的失败信息，而不是人工样例、外部文档或预设难度目标。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 依据错误记忆生成并更新课程候选题

先按总活跃失败量 $F_t$ 计算下一轮自由探索概率 $\varepsilon_{t+1}$，其余概率用于按 $p_{t+1}(e)$ 抽取 Active 原因并定向出题；挑战者先利用冻结求解器给出的质量信号通过 GRPO 从 $\theta_t$ 更新到 $\theta_{t+1}$，再从混合策略采样候选池 $\mathcal{Q}^{\mathrm{cur}}_{t+1}$。

<div class="method-step__io" markdown="1">

**输入**：上一轮提交后的层次化记忆 $\mathcal{M}_t$、各 Active 原因的失败频次 $f_t(e)$、挑战者参数 $\theta_t$，以及当前冻结的求解器。<br>
**输出**：同时覆盖新区域和已知薄弱点的课程候选题池 $\mathcal{Q}^{\mathrm{cur}}_{t+1}$，以及更新后的挑战者。

</div>

**直观理解**：系统一部分时间自由出新题，防止训练范围越来越窄；另一部分时间针对错因出题，避免重复练习已经会做的内容。某个弱点在当前阶段出现得越频繁，被抽中出题的机会就越高。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 双置信度过滤并构造伪标注训练集

以票数最多的答案作为伪标签 $\hat{y}(x)$，用第一名答案票占比 $p_1(x)$ 衡量绝对自洽度，并用 $p_1(x)/p_2(x)$ 衡量多数答案相对第二名是否具有清晰领先；仅保留难度处于指定区间且领先比例达到阈值 $\tau$ 的题目。

<div class="method-step__io" markdown="1">

**输入**：候选题 $x\in\mathcal{Q}^{\mathrm{cur}}_t$ 和冻结求解器对每题独立采样的 $N$ 个构造响应。<br>
**输出**：带伪标签的求解器训练集 $\{(x,\hat{y}(x))\}$，以及供后续状态更新使用的自洽度证据。

</div>

**直观理解**：第一道门排除模型几乎必错或毫无学习空间的题，第二道门排除两个答案势均力敌、标签容易随采样改变的题。这样既保留有训练价值的中等难度问题，又降低错误伪标签在多轮训练中被不断强化的风险。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 使用独立响应更新求解器

若优化响应的最终答案与 $\hat{y}(x)$ 一致则奖励为 $+1$，否则为 $-1$，并据此通过 GRPO 更新求解器；构造响应只负责筛题和定标签，优化响应单独负责策略梯度学习。

<div class="method-step__io" markdown="1">

**输入**：过滤后的问题—伪标签对，以及求解器针对每道保留题重新采样的 $G$ 个优化响应 $\{r_j^{\mathrm{opt}}\}_{j=1}^{G}$。<br>
**输出**：本轮更新后的求解器，以及与伪标签不一致的失败优化轨迹。

</div>

**直观理解**：筛题用的答卷与真正训练用的答卷分开，避免直接重复利用同一批采样承担所有角色。训练目标是提高生成多数伪标签答案的概率，而失败答卷随后成为诊断下一轮课程方向的材料。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 诊断失败并维护层次化错误记忆

诊断器比较 $r^-$ 与 $r^+$ 的最早推理分歧，抽取去除题目具体数值和表面措辞的错误原因；随后执行已知目标原因路由、语义去重、技能节点归属和冗余节点合并，并依据定向题平均自洽度与新失败更新原因状态和频次。

<div class="method-step__io" markdown="1">

**输入**：保留题目 $x$、伪标签 $\hat{y}(x)$、一个与伪标签不一致的响应 $r^-$、一个与伪标签一致的响应 $r^+$，以及当前记忆 $\mathcal{M}_t$。<br>
**输出**：下一轮使用的提交记忆 $\mathcal{M}_{t+1}$，其中包含技能层级、错误原因、Active/Mastered 状态及当前活跃阶段频次。

</div>

**直观理解**：诊断器不只记录“这道题答错了”，而是比较失败与成功解法从哪里开始分叉，提炼可跨题复用的病因。相近病因归到同一技能下；掌握后频次清零，若后来再次犯错则重新激活。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 频次驱动的混合生成调度

$$
\frac{1-\varepsilon_{t+1}}{\varepsilon_{t+1}}=\frac{z_t}{k}=\frac{F_t}{kF_1},\qquad \varepsilon_{t+1}=\frac{1}{1+z_t/k}=\frac{F_1}{F_1+F_t/k},\qquad p_{t+1}(e)=\frac{f_t(e)}{F_t}
$$

**符号说明**

- $\varepsilon_{t+1}$：第 $t+1$ 轮采用自由探索生成的概率。
- $1-\varepsilon_{t+1}$：第 $t+1$ 轮采用错误原因定向生成的概率。
- $f_t(e)$：Active 原因 $e$ 在当前活跃阶段累计的已诊断失败次数；升级为 Mastered 时清零。
- $F_t=\sum_{e\in\mathcal{E}_t}f_t(e)$：第 $t$ 轮所有当前活跃阶段的失败总数。
- $F_1$：首轮自由探索后得到的失败总数，用作归一化参考。
- $z_t=F_t/F_1$：相对首轮参考值归一化后的当前活跃失败量。
- $k$：平衡自由探索与定向生成的超参数；当 $z_t=k$ 时两种模式概率相等。
- $p_{t+1}(e)$：进入定向模式后选择 Active 原因 $e$ 的概率。

<div class="equation-explanation" markdown="1">

**直观理解**：当前未解决错误越多，定向出题相对自由探索的比重越大；某个错误原因出现得越频繁，它在定向模式下越容易被选中。原因升级后频次被清零，会降低 $F_t$ 并把概率重新推向自由探索；若 $F_t=0$，作者规定 $\varepsilon_{t+1}=1$，全部进行自由探索。<br>
**原文位置**：第 3.1 节，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 双置信度训练集筛选规则

$$
\mathcal{D}_{\mathrm{train}}=\left\{x\ \middle|\ p_{\mathrm{low}}\leq p(x)\leq p_{\mathrm{high}},\quad p_1(x)\geq\tau p_2(x)\right\},\qquad p(x)=p_1(x)
$$

**符号说明**

- $\mathcal{D}_{\mathrm{train}}$：通过双置信度约束、用于求解器训练的问题集合。
- $x$：挑战者生成的一道候选问题。
- $p_1(x)$：求解器的 $N$ 个构造响应中，票数最多答案所占的比例。
- $p_2(x)$：票数第二多答案所占的比例；若没有第二种答案则置为零。
- $p(x)$：问题 $x$ 的自洽度分数，定义为 $p_1(x)$。
- $p_{\mathrm{low}},p_{\mathrm{high}}$：允许的自洽度下界和上界，用于保留中间难度问题。
- $\tau$：第一名票占比相对第二名票占比必须达到的最小倍数。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项约束控制题目难度：多数比例过低意味着标签不可靠，过高则可能缺少有效学习信号。第二项约束控制标签歧义：即使题目处于中间难度，也必须让第一名答案明显领先第二名，才把多数答案作为伪标签。<br>
**原文位置**：第 3.2 节，公式（2）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：DiagEvo 包含两个交替进行的 GRPO 优化阶段。挑战者更新时求解器冻结，并由冻结求解器评估挑战者生成的问题质量；原文指出完整质量奖励定义位于附录 C，但当前节选未给出其具体公式，因此不能进一步还原。求解器更新时挑战者不参与梯度更新：对每个保留的 $(x,\hat{y}(x))$，重新采样 $G$ 个优化响应，最终答案与伪标签一致者获得 $+1$，不一致者获得 $-1$，GRPO 据此提高高相对奖励响应的生成概率。

该目标实质上将“课程构造”和“课程学习”分开：挑战者学习生成对当前求解器有训练价值的问题，求解器学习解决经过可靠性筛选的问题。需要注意，$\hat{y}(x)$ 来自求解器自洽投票而非真实答案，因此奖励只表示与多数伪标签的一致性；诊断器比较 $r^-$ 与 $r^+$ 得到的也只是相对推理差异，作者明确说明这不能证明 $r^+$ 在事实意义上正确。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 频次驱动的混合出题与跨状态拼接**

混合策略以 $\varepsilon_{t+1}$ 从自由分布 $q_\theta^{\mathrm{free}}(x)$ 采样，否则先按 $p_{t+1}(e)$ 选取 Active 原因，再从条件分布 $q_\theta^{\mathrm{tar}}(x\mid e,\mathcal{M}_t)$ 出题。定向生成时，可将该 Active 原因与同一技能节点下随机选择的 Mastered 兄弟原因拼接；若没有可用兄弟，则只提供 Active 原因。

> 直观理解：自由探索负责发现记忆之外的新弱点，定向生成负责集中修补已知弱点。把同一技能下“尚未掌握”和“已经掌握”的因素组合起来，可以生成更综合的题，同时比跨技能随机配对更有语义关联。

**2. 双置信度伪标签过滤器**

绝对约束要求多数答案占比 $p(x)=p_1(x)$ 落在 $[p_{\mathrm{low}},p_{\mathrm{high}}]$，用于筛选中间难度；相对约束要求 $p_1(x)\geq\tau p_2(x)$，用于排除前两名答案高度冲突的候选。若不存在第二种答案，则定义 $p_2(x)=0$。

> 直观理解：仅看多数票比例仍可能留下接近五五开的争议题，而这种题的伪标签会随采样波动。额外检查第一名相对第二名的领先幅度，可使训练标签更稳定。

**3. 层次化错误原因记忆与生命周期管理**

记忆写作 $\mathcal{M}_t=(\mathcal{V}_t,\mathcal{E}_t,a_t)$：$\mathcal{V}_t$ 是技能节点集合，$\mathcal{E}_t$ 是错误原因集合，映射 $a_t:\mathcal{E}_t\rightarrow\mathcal{V}_t$ 将每个原因归到一个技能节点。每个原因保存文本、向量表示、状态 $s_t(e)\in\{\textit{Active},\textit{Mastered}\}$ 和频次 $f_t(e)$；Active 原因在定向题平均 $p_1(x)$ 达到 $\theta_{\mathrm{up}}$ 时升级并清零频次，之后若出现匹配的新失败则重新激活。

> 直观理解：技能节点像错题本的章节，错误原因像章节内的具体错误模式。状态转换让系统区分“仍需专项训练”和“目前已稳定掌握”，频次清零则避免陈旧失败永久主导后续课程。

**训练与推理**

训练开始时记忆为空，因此第 1 轮全部采用自由探索。每轮先冻结求解器、更新挑战者并生成候选题；再让求解器为每题采样 $N$ 个构造响应，用多数答案产生 $\hat{y}(x)$，经双置信度约束得到训练集；随后冻结挑战者，对保留题重新采样 $G$ 个优化响应，以二值一致性奖励通过 GRPO 更新求解器。最后，诊断器将每个失败响应 $r^-$ 与一个同意伪标签的响应 $r^+$ 比较，提炼最早推理分歧并更新记忆，经过去重、技能归属、节点合并和状态—频次转换后，生成下一轮的 $\mathcal{M}_{t+1}$。

推断或基准评测阶段只需要使用训练后选定的求解器检查点，不需要挑战者、诊断器或错误记忆参与答题。根据所给章节，论文在逐轮动态中发现性能前五轮持续上升，之后下降，因此实验统一采用第 5 轮检查点；这属于检查点选择规则，而不是测试时继续自进化。

**复现信息**

诊断器使用 Qwen3-Instruct-2507 系列模型承担错误抽取、语义匹配、技能归属和节点合并等所有基于大模型的语义判断；默认配置为 4B 诊断器，另有更大规模诊断器用于分析规模影响。错误抽取仅使用通过双置信度过滤之题目的 GRPO 优化轨迹，且抽取结果应删除题目特定数值与表面形式，以便跨问题复用。

复现时必须区分三类数据流：构造响应用于投票、筛题、产生伪标签和提供状态升级证据；独立的优化响应用于 GRPO 奖励及失败诊断；记忆只输入挑战者，不直接输入求解器。节选明确给出完整模型交替顺序和筛选逻辑，但未给出 $N$、$G$、$p_{\mathrm{low}}$、$p_{\mathrm{high}}$、$k$、$\theta_{\mathrm{up}}$ 的具体取值；消融表仅明确完整方法使用 $\tau=1.6$，其余数值需核对论文附录。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 数学推理基准组：MATH-500、GSM8K、OlympiadBench、Minerva Math和AMC，用于测量数学问题求解能力；原文未报告前四者的样本规模，AMC包含40道题。
- 一般推理基准组：MMLU-Pro、SuperGPQA、GPQA-Diamond和BBEH，用于检验方法能否超越数学领域，迁移到多学科或复杂推理任务；原文未明确报告各数据集的样本规模、划分及具体类别构成。
- 训练与诊断数据：方法不依赖外部任务数据，而是使用自博弈过程中生成的问题、求解器答案及其失败历史；这不是独立评测集，而是用于形成错误原因记忆和后续训练问题。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（accuracy）**

在数学基准上按simple-evals协议由GPT-4o自动判定答案正确性，在一般推理基准上采用贪心解码和exact-match准确率；数值表示答对问题的比例。 （越高越好，因为它直接衡量求解器最终回答正确的频率。）

</div>
<div class="metric-item" markdown="1">

**数学平均准确率（math average）**

五个数学推理基准准确率的平均值，用于降低单一数学数据集难度差异对总体判断的影响。 （越高越好；它反映方法在数学推理任务组上的整体收益，而不是某一个基准上的偶然提升。）

</div>
<div class="metric-item" markdown="1">

**AMC mean@32**

对AMC每道题采样32个回答后计算平均准确率；该指标同时反映单题多次采样下的平均解题成功率。 （越高越好；但它不是单次贪心回答准确率，不能直接与所有单次评测结果等同。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨三个求解器和九个推理基准的总体比较

<div class="result-value" markdown="1">

作者报告：默认4B诊断器下，DiagEvo在三个求解器（Qwen3-4B、Qwen3-8B和OctoThinker-8B）上，九个基准的平均准确率均超过所有比较基线。

</div>

这说明错误历史驱动的课程设计在不同模型规模和模型家族上都具有稳定的总体优势，而不是只对某一个求解器有效。它证明的是评测范围内的经验优越性，并不能单独证明在未测试的模型、任务或更长训练轮数上仍然保持优势。

<div class="result-source" markdown="1">

来源：Abstract；Section 4.2 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

With the default 4B diagnostician, DiagEvo outperforms every baseline in mean accuracy across all nine benchmarks for each of the three solvers: Qwen3-4B, Qwen3-8B, and OctoThinker-8B.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3-8B在五个数学推理基准上的比较

<div class="result-value" markdown="1">

Qwen3-8B使用DiagEvo时，五个数学推理基准的平均准确率为72.3%，比R-Zero高4.5个百分点。

</div>

该结果表明DiagEvo相对于无外部资源的自进化基线R-Zero，在数学任务组上获得了具有明确幅度的提升；它尤其支持“从自身失败中提取训练方向”比仅依赖一般自博弈信号更有效这一解释，但不能区分提升究竟来自诊断、记忆还是过滤机制。

<div class="result-source" markdown="1">

来源：Abstract；Section 4.2 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Qwen3-8B, it reaches 72.3% mean accuracy across five mathematical reasoning benchmarks, 4.5 percentage points above R-Zero.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen3-8B在全部九个基准上的总体平均

<div class="result-value" markdown="1">

Qwen3-8B使用DiagEvo时，九个基准的平均准确率为57.4%，比DARC高1.1个百分点。

</div>

DARC使用外部任务资源，因此该比较支持DiagEvo在不引入外部任务信息时仍能超过一种资源增强方法。提升幅度相对数学任务组的提升更小，说明一般推理基准可能稀释了数学领域的收益；该结果也不意味着DiagEvo在每一个单独基准上都一定领先。

<div class="result-source" markdown="1">

来源：Abstract；Section 4.2 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Its mean accuracy across all nine benchmarks is 57.4%, 1.1 percentage points above DARC.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主要结果中的部分基线分数取自DARC，而非全部由本实验重新运行；虽然附录F报告基础模型和R-Zero的复现结果高度接近，但跨论文结果仍可能受实现细节和报告方式影响。
- 自动评测和诊断质量依赖GPT-4o或GPT-5等外部模型：GPT-5被用来检查伪标签一致性，且问题属性中的难度也依赖GPT-5重标答案。原文报告对50道随机问题的人检查未发现oracle错误，但未证明该结论适用于全部轮次、全部数据分布或其他模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 未训练的基础模型：表示不进行自进化时的性能下界，用来判断任何训练收益是否超过初始求解器。
- R-Zero：不使用外部任务资源的自进化方法，是最直接的无标签自博弈比较对象；论文还在相同基础设施下复现其结果。
- Absolute Zero：另一种无外部任务资源的自进化方法，用于比较不同自我生成和自我训练机制。
- DARC：使用外部任务资源的引导式方法，且采用相同求解器、基准和评测协议；它检验DiagEvo能否在不获得外部任务信息的情况下达到或超过资源增强方法的效果。

**实验想回答的问题**

- 在不使用人类示例、文档语料或难度标签等外部任务资源的条件下，DiagEvo能否利用求解器自身的失败历史，持续改善数学与一般推理性能？
- 层次化错误原因记忆、双重置信度过滤，以及自由探索与原因定向生成的组合，分别是否对性能和训练信号质量有实质贡献？

**实验实现**

评测三个求解器：Qwen3-4B-Base、Qwen3-8B-Base和OctoThinker-8B-Hybrid-Base；每个求解器分别配合Qwen3-4B-Instruct-2507、Qwen3-30B-A3B-Instruct-2507和Qwen3-235B-A22B-Instruct-2507诊断器，默认诊断器为4B版本。诊断器和嵌入模型均冻结，只使用自博弈产生的信息。数学任务遵循simple-evals协议并使用GPT-4o自动评判；AMC按照每题32次采样报告mean@32。一般推理任务使用贪心解码和exact-match准确率。DiagEvo结果报告三次独立运行的均值和标准差；基础模型与R-Zero由作者复现，其余部分基线分数取自DARC论文，作者用相同求解器、基准和协议进行了可比性验证。附录F显示复现的基础模型聚合分数最多相差0.1个百分点，R-Zero最多相差0.5个百分点，逐基准偏差低于1.0个百分点。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除层次化错误原因记忆，改为纯自由探索 | 纯自由探索与保留错误原因记忆的变体都使用双重置信度过滤；相关曲线用于比较记忆是否能改善逐轮性能、问题覆盖和难度演化。论文报告移除记忆会导致性能损失，但所给摘录未明确报告Table 2中的具体数值。 | 该消融隔离了“根据已诊断错误定向生成”这一组件，保留过滤机制以避免把两个设计同时改变。若性能下降，说明仅提高问题多样性或难度不足以替代针对当前薄弱技能的课程安排。 | Appendix H Diagnostic Evaluation Protocols，Figure 5说明；Table 2相关讨论<br><span class="experiment-evidence">Free exploration maintains broad coverage, while cause-targeted generation follows the solver’s current error causes. This pattern is consistent with the performance loss when Table 2 removes either mode.</span> |
| 移除双重置信度过滤 | 双重置信度过滤是核心消融因素之一；作者报告其与层次化错误原因记忆共同促成性能提升，但摘录未给出移除该过滤器后的具体准确率或变化幅度。 | 该消融测试训练数据筛选质量，而非问题生成方向本身。过滤器只保留中等难度且多数求解器答案具有清晰票数领先的问题，目标是降低伪标签不可靠带来的训练噪声；移除后若性能下降，说明自博弈生成问题的可用性不仅取决于难度，还取决于答案信号的一致性。 | Abstract；Section 4.2 Main Results<br><span class="experiment-evidence">Ablations show that the hierarchical error-cause memory and double-confidence filtering both contribute to these gains.</span> |

**定性案例**

- 问题覆盖可视化（Figure 5）显示，纯自由探索在各轮覆盖一个较宽且相对稳定的区域；原因定向生成则随着错误原因记忆积累而移动到新的区域。作者据此将两者解释为互补机制：自由探索维持广泛覆盖，原因定向生成跟随求解器当前错误。该可视化支持生成分布发生了机制上可解释的变化，但它是二维PCA投影，不能单独证明新区域中的问题质量或因果收益。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：利用层次化错误记忆生成针对性自博弈课程以提升数学等推理能力，同时构成一种无需外部任务资源的 LLM 后训练方法。; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`e01a1b7cfd769c0fce97b9345f91f61674d462b2165509773a4eef29ddc96edb`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
