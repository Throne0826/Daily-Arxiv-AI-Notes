---
title: "[论文解读] COGTRL: Training LLMs for Scientific Discovery Assistance using Cognitive Traces via Reinforcement Learning"
description: "[arXiv 2608.30109][对齐 / RLHF] 本文研究如何让开源小型大语言模型不仅复述科学知识，还能围绕研究目标与约束显式推演取舍，并利用这些推演改善后续科学方法步骤的生成质量。"
arxiv_id: "2608.30109"
announcement_date: "2026-09-01"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:50:53.777004+00:00"
source_sha256: "47792bfbe03ca840ac4275c64c30df7e620d4a2c346db3db4119e6a03cc0a4b1"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "科学发现辅助"
  - "认知轨迹"
  - "强化学习"
  - "GRPO"
  - "约束感知方法生成"
  - "开源语言模型"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.30109</p>

# COGTRL: Training LLMs for Scientific Discovery Assistance using Cognitive Traces via Reinforcement Learning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Shrinidhi Kumbhar Santosh Mashetty Divij Handa Kevin Coutinho, Siddharth Sambhaji Ghule, Chitta Baral</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Arizona State University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30109v1) · [PDF 下载](https://arxiv.org/pdf/2608.30109v1) · **关键词** 大语言模型, 科学发现辅助, 认知轨迹, 强化学习, GRPO, 约束感知方法生成, 开源语言模型<br>
**代码**: [https://github.com/shri071/CoGTRL](https://github.com/shri071/CoGTRL)

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

本文研究如何让开源小型大语言模型不仅复述科学知识，还能围绕研究目标与约束显式推演取舍，并利用这些推演改善后续科学方法步骤的生成质量。

**不用术语来说**：科学家面对“开发适用于海洋环境且环保的自修复涂层”一类任务时，需要逐步考虑目标、约束、候选方案及失败风险，而论文通常只记录最终方法，不记录形成方法的思考过程；因此，仅从论文学习的模型可能知道许多事实，却未必能在新目标和多重约束下设计出连贯、可执行的方法。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出以认知轨迹强化学习训练科学发现助手：模型交替生成认知轨迹与方法步骤，并在整条轨迹层面联合优化二者，而不是只训练最终答案或把推理文字当作独立解释。
- 作者设计奖励机制，同时评价认知轨迹和方法步骤，并额外奖励能够提升下游步骤质量的认知轨迹，以检验和强化认知过程对方法设计的实际作用。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于“大语言模型辅助科学发现”方向，关注的不是封闭式科学问答、文献摘要或单一性质预测，而是开放式、受约束的科学方法设计：模型需要把研究目标转化为可执行的多步方案。论文的基本判断是，科研论文通常只呈现最终方法，较少记录研究者如何检查约束、排除失败备选方案并逐步修正决策；因此，仅用科学文献训练模型可能不足以习得真实的方法设计过程。CogTRL据此要求开源大语言模型交替生成认知轨迹与方法步骤，使每段认知轨迹说明下一步为何能够推进目标并满足约束，而后续步骤又以此前全部轨迹和步骤为条件。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**认知轨迹（Cognitive Trace）**

指模型在给出某个方法步骤前，对目标、约束、候选选择及决策理由所作的显式推理记录。本文强调它必须对后续步骤有实际帮助，而不只是事后生成的解释。

</div>
<div class="concept-item" markdown="1">

**强化学习（Reinforcement Learning, RL）**

模型先生成候选方案，再根据奖励信号调整生成策略，使高奖励行为更可能出现。本文分别评价认知轨迹和方法步骤，并把二者合成为轨迹级训练信号。

</div>
<div class="concept-item" markdown="1">

**组相对策略优化（Group Relative Policy Optimization, GRPO）**

GRPO针对同一输入采样一组输出，通过比较组内输出的奖励来估计各输出的相对优势，再更新模型策略。本文以它作为强化学习骨架，对包含多轮认知轨迹与方法步骤的完整轨迹进行优化。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一项研究目标及一组必须满足的约束，例如目标为开发适用于海上环境的自修复涂层，约束为方案应当环保。模型输出长度为$N$的分步科学方法，其中第$i$个阶段包含认知轨迹$CT_i$和对应的方法步骤$MS_i$；生成$MS_i$时可利用从第$1$阶段至第$i$阶段的认知信息，并以此前阶段的轨迹和步骤作为上下文。生成持续到目标被实现且全部约束得到满足。论文研究的是不依赖外部工具的开放式方法生成，重点提升开源$3$B参数模型自身的、面向约束的科学推理能力；其应用定位是为人类研究者提供方法设计建议，而非声称模型已经通过真实实验验证了所生成方案。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$CT_i$**

第$i$个阶段的认知轨迹，用于说明该阶段如何结合目标与约束作出决策。

</div>
<div class="notation-item" markdown="1">

**$MS_i$**

第$i$个阶段生成的科学方法步骤。

</div>
<div class="notation-item" markdown="1">

**$N$**

一条完整生成轨迹所包含的阶段或方法步骤总数。

</div>
<div class="notation-item" markdown="1">

**$\tau=((CT_1,MS_1),\ldots,(CT_N,MS_N))$**

由交替出现的认知轨迹和方法步骤组成的完整科学方法生成轨迹；该符号是对图1和图2所述结构的紧凑表示。

</div>

</div>

**直接相关的工作**

- **LLM智能体辅助科学发现**: 既有方法常通过检索增强、文献工作流、多智能体协作、外部工具或模拟器完成科学问答、文献综合和假设生成，并往往依赖闭源前沿模型。CogTRL则面向开放式、受约束的方法生成，通过训练开源模型把结构化科学推理内化到模型参数中，重点减少对外部工具的依赖。
- **基于推理轨迹、过程监督与强化学习的LLM推理训练**: 相关研究已经利用显式或隐式推理轨迹、理由蒸馏、过程监督和强化学习提升模型推理，但主要服务于数学、问答或可程序化验证的任务。CogTRL将这一路线扩展到答案难以自动判定的科学方法设计，并联合奖励认知轨迹本身及其对后续方法步骤质量的作用。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

科学发现辅助要求模型根据明确研究目标和约束生成逐步方法，从而降低研究人员进行方法设计的时间与劳动成本。此类任务不是单纯检索已有结论：模型必须在连续步骤中提出假设、检查约束、判断方案是否推进目标，并根据先前决定迭代后续计划。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于前沿大模型的智能体式科学辅助**：调用能力较强的大模型，并结合多步智能体流程处理信息抽取、性质预测、文献综合或假设生成等相对狭窄的科学子任务。
- **科学文献训练、提示或常规微调**：让模型从研究论文等科学语料学习领域知识，再通过零样本思维链提示、监督微调或不含认知轨迹的常规强化学习，直接生成科学方法或相关答案。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 研究论文通常省略约束审查、失败备选方案和迭代决策等细粒度认知过程；以论文为主要训练数据会使模型更容易学到最终结果，而难以学到研究者如何在约束下形成该结果，进而削弱其开放式方法设计能力。
- 既有智能体研究多依赖前沿大模型并聚焦较窄的科学子任务，尚未充分解决如何直接训练开放源代码的小参数模型完成端到端、目标与约束驱动的科学方法生成；此外，若认知轨迹只被当作独立解释来优化，也不能保证它会真正改善后续步骤。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少一种面向开源小型模型的训练机制，能够把“思考为何采取某一步”与“实际采取的方法步骤”组织成相互依赖的完整轨迹，并依据认知轨迹对后续方法质量的贡献进行联合优化。换言之，未解决的关键不是让模型写出更多推理文字，而是让这些文字成为对下游科学决策有用的中间计算。

</div>
<div markdown="1"><span>核心问题</span>

在给定科学研究目标和一组约束时，能否通过轨迹级强化学习，使约 $3$B 参数的开源大语言模型交替生成人类可理解的认知轨迹与方法步骤，并让认知轨迹因能够提高后续步骤质量而获得奖励，从而优于仅依赖科学文献、提示、监督微调或普通强化学习的训练方式？

</div>
<div markdown="1"><span>作者直觉</span>

如果每个方法步骤之前，模型都必须说明该步骤如何推进目标、满足哪些约束以及为何优于备选方案，那么后续生成便拥有一个针对当前决策的中间工作区。进一步地，只有当这段认知轨迹确实带来更好的后续步骤时才提高其奖励，可减少空洞但听起来合理的解释，促使模型学会对方法设计真正有帮助的约束检查与迭代规划。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

COGTRL（Cognitive Traces Reinforcement Learning）以研究目标和约束为输入，将输出组织为交替排列的认知轨迹与方法步骤：先说明如何理解目标、约束、科学机制、替代方案或不确定性，再据此生成可执行的方法步骤。训练时，模型使用基于大语言模型的评分器分别评价认知轨迹和方法步骤，并通过轨迹级的组相对策略优化（GRPO）联合更新两类输出；推理时则保留这些认知轨迹，使每个方法步骤都显式依赖先前的推理过程。直观地说，该方法不是只要求模型直接给出“做什么”，而是训练模型先说明“为什么这样做、受到什么限制、有哪些取舍”，再给出具体操作，从而提高科学方法的完整性和可执行性。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 目标与约束建模

将开放式科学发现任务表示为目标条件的方法生成问题，并把目标和约束提供给策略模型 $\pi_{\theta}$。

<div class="method-step__io" markdown="1">

**输入**：研究目标 $g$ 与约束集合 $C$，合并为输入 $x=(g,C)$。<br>
**输出**：模型生成轨迹所需的条件输入 $x$。

</div>

**直观理解**：这一步相当于先明确“要解决什么问题”和“不能违反哪些条件”，避免模型只凭一般知识提出脱离任务要求的方案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 交替生成认知轨迹与方法步骤

策略模型自回归地产生 $n$ 个交替单元 $(t_i,s_i)$：$t_i$ 是简短的认知轨迹，说明目标约束、科学机制、因果依据、替代方案或不确定性；$s_i$ 是在此前轨迹和步骤条件下生成的对应方法步骤。输出格式要求使用匹配的标签、连续编号，并保持 Trace 与 Step 交替。

<div class="method-step__io" markdown="1">

**输入**：输入 $x$ 以及已经生成的部分轨迹。<br>
**输出**：完整轨迹 $\tau=(t_1,s_1,t_2,s_2,\ldots,t_n,s_n)$。

</div>

**直观理解**：模型每提出一个行动，先写出该行动的理由，再写出行动本身；这类似研究者先分析实验设计，再决定具体实验。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 轨迹级奖励计算

使用 o3-mini 作为基于评分标准的奖励模型，对认知轨迹和方法步骤分别按六个维度进行 $1$ 到 $5$ 评分；评分归一化后形成 $R_{\mathrm{trace}}$ 和 $R_{\mathrm{step}}$，并用提升奖励 $R_{\mathrm{uplift}}$ 鼓励能带来高质量步骤的认知轨迹，同时加入格式结构奖励 $R_{\mathrm{struct}}$。

<div class="method-step__io" markdown="1">

**输入**：生成的轨迹 $\tau$。<br>
**输出**：每条轨迹的总奖励 $R_{\mathrm{total}}$。

</div>

**直观理解**：评分器不仅检查最终方案是否好，也检查中间理由是否有用；如果某种思考确实帮助产生更好的步骤，它会得到额外奖励。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### GRPO策略优化与推理

在组内将各轨迹奖励标准化为优势 $A_i$，使用带概率比裁剪和 KL 约束的 GRPO 目标更新联合 trace-step 策略；训练完成后，模型在给定目标和约束时继续按相同的交替格式生成轨迹。

<div class="method-step__io" markdown="1">

**输入**：同一输入下由旧策略采样的 $G$ 条轨迹及其总奖励。<br>
**输出**：训练后的科学发现辅助模型，以及包含认知轨迹的方法生成结果。

</div>

**直观理解**：模型把同一问题的多份候选方案相互比较，提升组内更好的方案，同时限制每次更新不要偏离原有模型过远，以减少训练不稳定。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 轨迹自回归概率

$$
\pi_{\theta}(\tau\mid x)=\prod_{i=1}^{n}\pi_{\theta}(t_i\mid x,\tau_{<i})\,\pi_{\theta}(s_i\mid x,\tau_{\leq i})
$$

**符号说明**

- $\pi_{\theta}$：参数为 $\theta$ 的策略模型，即生成轨迹的概率分布
- $\tau$：完整的认知轨迹与方法步骤序列
- $x=(g,C)$：由研究目标 $g$ 和约束集合 $C$ 构成的输入
- $t_i$：第 $i$ 个认知轨迹片段
- $s_i$：第 $i$ 个方法步骤
- $\tau_{<i}$：第 $i$ 个认知轨迹之前已经生成的轨迹内容
- $\tau_{\leq i}$：截至第 $i$ 个认知轨迹及其方法步骤的已生成内容
- $n$：轨迹中认知轨迹—方法步骤单元的数量

<div class="equation-explanation" markdown="1">

**直观理解**：该式把完整输出拆成连续的小决策：模型先根据已有内容生成 $t_i$，再根据包括该认知轨迹在内的上下文生成 $s_i$。因此，方法步骤在概率模型中明确受到相应认知轨迹的影响。<br>
**原文位置**：第 3 节 Method

</div>

</div>

<div class="equation-block" markdown="1">

#### 总奖励与认知轨迹提升奖励

$$
R_{\mathrm{uplift}}=R_{\mathrm{step}}\cdot\sigma\!\left(R_{\mathrm{trace}}-\alpha\right),\qquad R_{\mathrm{total}}=R_{\mathrm{step}}+\gamma R_{\mathrm{uplift}}+\lambda R_{\mathrm{struct}}
$$

**符号说明**

- $R_{\mathrm{trace}}$：认知轨迹质量奖励，归一化到 $[0,1]$
- $R_{\mathrm{step}}$：方法步骤质量奖励，归一化到 $[0,1]$
- $R_{\mathrm{uplift}}$：由认知轨迹质量调制的方法步骤提升奖励
- $\sigma$：Sigmoid 函数，将轨迹质量相对于阈值的影响平滑地映射为权重
- $\alpha$：认知轨迹质量阈值；实验中设为 $0.6$
- $R_{\mathrm{struct}}$：输出格式、标签、交替顺序和索引合法性的结构奖励
- $\gamma$：提升奖励权重；训练中设为 $0.5$
- $\lambda$：结构奖励权重；训练中设为 $0.1$

<div class="equation-explanation" markdown="1">

**直观理解**：提升奖励只有在认知轨迹质量足够高时才会有效地放大步骤奖励，所以模型不能仅靠写出形式正确的理由获益。总奖励将步骤质量作为主体，再加入认知轨迹带来的提升和格式约束。<br>
**原文位置**：第 3.1.3 节、第 3.2 节

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：COGTRL 以总奖励 $R_{\mathrm{total}}$ 为优化信号，使用 GRPO 更新策略。对于同一输入 $x$，旧策略 $\pi_{\theta_{\mathrm{old}}}$ 生成 $G$ 条候选轨迹，轨迹 $i$ 的奖励为 $r_i=R_{\mathrm{total}}(\tau_i)$，并计算组内标准化优势 $A_i=(r_i-\mathrm{mean}(\{r_1,\ldots,r_G\}))/[\mathrm{std}(\{r_1,\ldots,r_G\})+\epsilon]$；这使更新主要依赖同一问题中候选方案的相对优劣。优化目标采用裁剪后的策略比率 $\rho_i(\theta)=\pi_{\theta}(\tau_i\mid x)/\pi_{\theta_{\mathrm{old}}}(\tau_i\mid x)$，并减去 $\beta D_{\mathrm{KL}}(\pi_{\theta}\|\pi_{\mathrm{ref}})$，其中参考策略 $\pi_{\mathrm{ref}}$ 是 SFT 模型，KL 项用于限制策略偏移、保持训练稳定。与只优化方法步骤的普通 GRPO 不同，COGTRL 的策略概率覆盖交替的认知轨迹和方法步骤，因此奖励会联合塑造“如何思考”和“采取什么方法”。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 交替式 Trace–Step 策略**

策略以 $\pi_{\theta}(\tau\mid x)$ 建模完整轨迹概率，其中每个认知轨迹 $t_i$ 条件于输入和此前轨迹，方法步骤 $s_i$ 条件于输入以及当前和此前的轨迹—步骤序列。该设计使认知过程不再是独立的解释文本，而成为后续方法步骤的直接条件。

> 直观理解：它把“思考”和“行动”绑定起来：每一段理由都必须服务于紧接着的方法步骤，而不是事后附加一段看似合理的解释。

**2. 认知轨迹与步骤的联合奖励**

认知轨迹奖励考察目标和约束整合、科学与机制推理、因果逻辑与可行动性、信息密度、科学准确性与一致性、不确定性与权衡；方法步骤奖励考察目标对齐、科学合理性、创新性、可测试性、可行性与可扩展性、潜在影响。提升奖励定义为 $R_{\mathrm{step}}\sigma(R_{\mathrm{trace}}-\alpha)$，以使高质量认知轨迹与高质量步骤共同受益。

> 直观理解：这相当于同时给“理由”和“方案”打分，并额外奖励那些能真正改善方案的理由，而不是奖励冗长或形式上像推理的文本。

**3. 结构奖励与稳定策略更新**

结构奖励约束 `<Trace_i>…</Trace_i><Step_i>…</Step_i>` 的标签匹配、交替关系和连续索引；GRPO 使用组内相对优势、裁剪的策略比率以及相对于 SFT 参考策略的 KL 惩罚。

> 直观理解：结构奖励保证输出能被稳定解析，KL 约束则像安全护栏，防止强化学习为了追逐评分而彻底改变原模型的语言能力和行为。

**训练与推理**

训练阶段首先从任务分布 $\mathcal{D}$ 采样目标—约束输入，当前策略为每个输入生成多条完整 trace-step 轨迹；随后由 o3-mini 按预设评分标准评估认知轨迹和方法步骤，计算提升奖励、结构奖励及总奖励，再进行组内优势归一化和裁剪式 GRPO 更新。推理阶段输入研究目标与约束，模型按照 `<Trace_i>` 后接 `<Step_i>` 的交替顺序自回归生成，直到形成完整方法；认知轨迹在推理时也被保留并作为后续步骤的条件，而非仅在训练时使用的隐藏监督信号。

**复现信息**

论文给出的关键复现实验设置包括：SFT 使用 AdamW、余弦学习率调度器、批大小 $4$、学习率 $2.0\times10^{-5}$ 和 $5$ 个训练轮次；GRPO 与 COGTRL 使用学习率 $1\times10^{-6}$，mini-batch 大小为 $12$，每 GPU 的 micro-batch 大小为 $2$。GRPO 训练 $400$ 步，COGTRL 训练 $200$ 步，rollout size 为 $5$；训练基础设施分别使用 HuggingFace、VERL 和 vLLM。奖励权重为 $\gamma=0.5$、$\lambda=0.1$，认知轨迹阈值为 $\alpha=0.6$；这些设置决定不同奖励项在策略更新中的相对影响，但不改变方法的核心流程。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 训练集由 4,990 篇 arXiv 论文构成，覆盖物理、计算机科学、数学、人工智能、电气工程与生物学六个领域。模块化 LLM 流水线从论文中抽取研究目标、约束和分步方法，再由 GPT-4o 为每个样本生成三个候选认知轨迹，并由 GPT-4o、Gemini-2.5-Pro 和 OpenAI-o1 联合评分选出最终轨迹。抽取质量由每领域随机 10 个样本、四名标注者核验，平均正确性为 2.58/3，Krippendorff’s alpha 为 0.71。该数据用于 SFT 初始化；强化学习阶段使用策略模型自行生成的轨迹和步骤，而不直接复用教师轨迹。
- AI 测试集包含 50 篇 NeurIPS 2024 论文，覆盖 LLM、优化和强化学习等子领域；两名领域专家独立抽取目标、约束及分步方法。它与训练数据中的 AI 领域相近，因此主要检验域内科学方法生成能力。模型知识截止时间为 2023 年，而测试论文来自 2024 年，用于降低论文内容泄漏风险。
- 材料科学测试集包含 MatDesign 基准中的 50 篇论文；基准提供研究目标和约束，两名领域专家补充抽取方法步骤。训练集未包含材料科学这一领域，因此该集合主要检验跨领域泛化。两个科学测试集的参考抽取经专家按三级序数量表复核，二次加权 Cohen’s $\kappa$ 为 0.67。另有 AMC23、AIME、MMLU-Pro、GPQA-Diamond、HumanEval 和 OlympiadBench 等域外推理基准用于检查原模型能力是否得到保留，但所给正文未提供其具体结果。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**科学方法综合质量分数**

Codex/GPT-5.4 与 Claude Code/Claude Sonnet 4.6 两套独立代理式评审框架，分别按“目标与约束对齐、科学合理性、创新性、可检验性、可行性与可扩展性、潜在影响”六个维度给生成的方法步骤打 1–5 分；不评价认知轨迹本身。最终分数为 $\mathrm{FinalScore}=\frac{\sum_{i=1}^{6}s_i}{30}\times100$，其中 $s_i$ 是第 $i$ 个维度的分数。 （越高越好，因为高分表示生成方法在六项方法学标准上获得更积极的独立评价；但它仍是基于评审模型和量规的代理指标，不等同于真实实验成功率。）

</div>
<div class="metric-item" markdown="1">

**固定高质量步骤的逐词概率 $\exp(-\mathrm{NLL})$**

对完全相同的目标方法步骤进行 teacher forcing，只改变前置条件为对齐轨迹、无轨迹或同领域错配轨迹；$\mathrm{NLL}$ 在相同目标步骤 token 上平均。该指标衡量给定轨迹后，模型认为这些方法步骤有多自然或多可能。 （越高越好；在目标 token 完全相同的情况下，更高概率说明轨迹更支持这些步骤。对齐轨迹高于错配轨迹尤其有助于排除“仅因上下文更长或格式不同而提升”的解释。）

</div>
<div class="metric-item" markdown="1">

**通用能力保留评测**

使用数学、专业知识、科学问答、代码与奥林匹克题等域外基准，检查面向科学发现的训练是否损害基础模型原有推理能力。所给章节只列出了基准名称，没有明确说明统一的聚合方式或具体结果。 （取决于各基准原有评分规则；本文的实验目的不是在这些任务上创造新最佳结果，而是观察训练后能力是否明显退化。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 3B 模型采用交错式认知轨迹—方法步骤生成，在 AI 与材料科学上比较 COGTRL、vanilla GRPO 以及同规模非 COGTRL 基线。

<div class="result-value" markdown="1">

作者报告，交错式 COGTRL 相对 GRPO 平均提高 4.12 分，相对使用相同 3B 基础模型的全部非 COGTRL 基线平均提高 7.85 分。表 2 中，Llama-3.2-3B 的 COGTRL 得分为 AI 52.63±0.58、材料科学 55.64±0.51；Qwen-2.5-3B 对应为 51.13±0.61 和 53.17±0.56，且均高于各自的交错式 GRPO。

</div>

这项比较支持 COGTRL 的主要结论：提升不只是来自科学数据微调或一般强化学习，因为它在两个 3B 模型、域内 AI 和域外材料科学上都超过了最接近的 GRPO 对照。尤其是材料科学结果表明方法具有一定跨领域迁移性。不过，分数来自 LLM 量规评审，不能直接证明生成方案在真实实验室中可实现或能产生新发现。

<div class="result-source" markdown="1">

来源：第 5 节“CogTRL with Interleaved Trace-Step generation improves Quality of Scientific Methods”；具体模型分数见表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In the interleaved setting, CogTRL improves over GRPO by an average of 4.12 points and over all non-CogTRL baselines using the same 3B models by 7.85 points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 在同一 COGTRL 训练思想下比较交错式生成与 think-first 生成，两个 3B 模型的结果分别在 AI 和材料科学上取平均。

<div class="result-value" markdown="1">

交错式 COGTRL 相对 think-first COGTRL，在 AI 上平均提高 4.30 分，在材料科学上平均提高 4.99 分；SFT with traces 也呈现相同方向的趋势。

</div>

结果说明，把局部思考紧邻其对应的方法步骤，优于先一次性写完全部思考再执行方法。合理解释是：每个新步骤都能同时依据前面的轨迹和已生成步骤作出调整，更接近受约束的迭代决策过程。但这只是两种输出组织方式的比较，尚不能证明模型生成的自然语言轨迹完整复现了人类科学家的真实认知过程。

<div class="result-source" markdown="1">

来源：第 5 节“CogTRL with Interleaved Trace-Step generation improves Quality of Scientific Methods”，表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Averaged across both models, interleaved CogTRL improves over think-first CogTRL by 4.30 points on AI and 4.99 on Material Science.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 将交错式 3B COGTRL 与未经任务训练、仅做零样本 CoT 的开源 70B/72B 模型比较。

<div class="result-value" markdown="1">

Llama-3.2-3B COGTRL 在 AI 和材料科学上分别获得 52.63±0.58 与 55.64±0.51，高于 Llama-3.3-70B 零样本 CoT 的 52.27±0.57 与 54.00±0.53，也高于 Qwen-2.5-72B 的 50.47±0.62 与 54.57±0.49。Qwen-2.5-3B COGTRL 的 51.13±0.61 与 53.17±0.56 则超过 72B 模型的 AI 分数，但未超过其材料科学分数。

</div>

这表明针对科学发现流程设计的训练可以让小模型在该量规下接近甚至超过大得多的开源零样本模型，具有明显的参数效率价值。比较并非同训练预算的公平算法对照：70B/72B 模型没有接受 COGTRL 训练，因此结果不能推出 3B 模型在一般能力上优于 70B 模型，也不能说明 COGTRL 已达到 GPT-5.4、Gemini-2.5-Pro 或 Claude Opus 4.6 的水平。

<div class="result-source" markdown="1">

来源：表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Llama-3.2-3B-It | CogTRL (Int. Think) | 52.63 ± 0.58 | 55.64 ± 0.51; Qwen-2.5-3B-It | CogTRL (Int. Think) | 51.13 ± 0.61 | 53.17 ± 0.56; Llama-3.3-70B-It | Zero-shot-CoT (Int. Think) | 52.27 ± 0.57 | 54.00 ± 0.53; Qwen-2.5-72B-It | Zero-shot-CoT (Int. Think) | 50.47 ± 0.62 | 54.57 ± 0.49.

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

- Zero-Shot Chain-of-Thought：不进行任务专门训练，仅通过提示让模型推理。它衡量基础模型自身能力，并覆盖 3B、70B/72B 及闭源前沿模型，从而区分训练方法收益与单纯扩大模型规模的收益。
- SFT without cognitive traces：只用科学方法步骤做监督微调，检验领域数据和方法写作监督本身能带来多少提升；与 COGTRL 的差异在于没有显式认知轨迹，也没有强化学习。
- SFT with cognitive traces：同时监督认知轨迹和方法步骤，并分别采用 think-first 与交错生成格式。它用于判断收益是否只来自教师生成轨迹的模仿，还是还需要 COGTRL 的轨迹级强化学习。
- Vanilla GRPO：以交错格式训练，但只使用步骤质量奖励，不引入 COGTRL 的认知轨迹相关联合奖励。它是最关键的强化学习对照，用于隔离 COGTRL 奖励设计，而不是把 RL 相对于 SFT 的一般收益误当成认知轨迹收益。

**实验想回答的问题**

- 在给定研究目标与约束后，联合强化学习认知轨迹和方法步骤的 COGTRL，能否比零样本推理、监督微调以及仅优化步骤质量的 GRPO 生成质量更高的科学方法？这种收益能否从域内 AI 论文迁移到域外材料科学论文？
- 性能提升是否真正来自认知轨迹对后续方法步骤的帮助，而非模型规模、额外上下文长度或更冗长的输出？具体考察交错式轨迹—步骤生成、提升奖励 $R_{\mathrm{uplift}}$ 以及轨迹与步骤语义对齐的作用。

**实验实现**

所有 SFT 和强化学习实验均在 Llama-3.2-3B-Instruct 与 Qwen-2.5-3B-Instruct 上进行，并比较两种输出格式：think-first 先生成完整认知轨迹、再生成完整方法；interleaved 则让轨迹与方法步骤交替出现。评测只给最终方法步骤打分，不直接奖励文字形式上“像推理”的轨迹。两套评审代理在相同设置下启用高推理强度、互联网检索和工具使用，且与 RL 使用的 OpenAI o3-mini 奖励模型不同，以降低对单一奖励模型的过拟合风险。评审采用基于量规的独立打分而非参考答案匹配或成对比较；表 2 和表 5 的结果来自三次独立运行并报告标准差。聚合 LLM 评审与人类专家偏好在 77.14% 的案例上一致，作者还使用另一套独立量规复评零样本、GRPO 与 COGTRL，但所给正文仅说明结论一致，未提供附录 P 的具体分数。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 保留步骤奖励 $R_{\mathrm{step}}$、轨迹奖励 $R_{\mathrm{trace}}$ 和结构奖励 $R_{\mathrm{struct}}$，只移除提升奖励 $R_{\mathrm{uplift}}$。 | 作者报告，移除 $R_{\mathrm{uplift}}$ 后，两个模型跨两个领域的平均性能下降 5.38%。无该奖励时，Llama-3.2-3B 在 AI/材料科学上的分数为 50.65/53.20，Qwen-2.5-3B 为 48.35/48.96，均低于表 2 中完整交错式 COGTRL 的对应结果。 | $R_{\mathrm{uplift}}$ 专门要求认知轨迹改善后续方法步骤，而不只是生成表面合理的解释。删除它后的下降说明，单独奖励轨迹质量、步骤质量和格式结构不足以获得完整收益。该消融隔离了提升奖励的增量作用，但表 3 未报告标准差，因而无法仅凭所给内容判断各项差异的统计显著性。 | 第 5 节“CogTRL with Interleaved Trace-Step generation improves Quality of Scientific Methods”，表 3<br><span class="experiment-evidence">Removing it while retaining Rstep, Rtrace, and Rstruct causes an average degradation of 5.38% across both models (Table 3), suggesting that cognitive traces are most beneficial when they improve downstream method quality and not just superficial explanations.</span> |
| 固定 COGTRL 生成的同一组高质量方法步骤，仅把输入条件改为对齐轨迹（w/A）、无轨迹（w/O）或来自同领域另一样本的错配轨迹（w/M），比较步骤 token 的 $\exp(-\mathrm{NLL})$。 | 四个模型—领域组合中，对齐轨迹的概率均最高：Llama 的 AI 为 0.6324，对比无轨迹 0.5274、错配轨迹 0.4732；材料科学为 0.6108/0.5145/0.4598。Qwen 的 AI 为 0.5028/0.4127/0.3631；材料科学为 0.4859/0.3991/0.3473。 | 因为目标步骤 token 完全固定，差异不能由输出内容或长度造成；又因为错配轨迹甚至低于无轨迹，额外上下文本身并不足以解释提升，关键在于轨迹与当前方法步骤是否语义对齐。这提供了认知轨迹影响模型条件概率的机制证据，但它仍是 teacher-forcing 分析，并不单独证明概率提高必然导致真实科学质量提高。 | 表 4；第 5 节“Uplift Evidence of Cognitive Traces”<br><span class="experiment-evidence">Llama 3.2 3B-It \| AI \| 0.6324 \| 0.5274 \| 0.4732; Llama 3.2 3B-It \| MatSci \| 0.6108 \| 0.5145 \| 0.4598; Qwen 2.5 3B-It \| AI \| 0.5028 \| 0.4127 \| 0.3631; Qwen 2.5 3B-It \| MatSci \| 0.4859 \| 0.3991 \| 0.3473.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该工作通过轨迹级强化学习训练 LLM 生成认知过程和科学推理步骤，核心贡献同时涉及后训练对齐与推理能力。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`47792bfbe03ca840ac4275c64c30df7e620d4a2c346db3db4119e6a03cc0a4b1`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
