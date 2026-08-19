---
title: "[论文解读] Ask, Condition or Abstain: Reinforcement Learning for Missing-Premise Reasoning"
description: "[arXiv 2608.16554][LLM Reasoning] 本文研究当问题缺少决定唯一答案的关键前提时，如何通过强化学习使推理模型识别信息不足，并选择提问、给出条件化答案或适当弃答，而不是自信地编造答案。"
arxiv_id: "2608.16554"
announcement_date: "2026-08-18"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:24:45.914058+00:00"
source_sha256: "97140430674a237c4396d2603930b35d133defc0685e83fd8a0c2a2fd1802f51"
tags:
  - "LLM Reasoning"
  - "强化学习"
  - "缺失前提推理"
  - "欠定问题"
  - "条件化回答"
  - "主动询问"
  - "弃答"
  - "行为评估"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.16554</p>

# Ask, Condition or Abstain: Reinforcement Learning for Missing-Premise Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Yongqi Tong, Zhenyu Zhang, Zimi Liu, Kewei Fu, Mingli Song, Haofei Zhang, Junshao Zhang, Hong Zhu, Jiang-Ming Yang, Xin Zhang, Jianshe Li</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Zhejiang University；Dingtalk, Alibaba Group</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.16554) · [PDF 下载](https://arxiv.org/pdf/2608.16554) · **关键词** 缺失前提推理, 强化学习, 欠定问题, 条件化回答, 主动询问, 弃答, 行为评估<br>


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

本文研究当问题缺少决定唯一答案的关键前提时，如何通过强化学习使推理模型识别信息不足，并选择提问、给出条件化答案或适当弃答，而不是自信地编造答案。

**不用术语来说**：现实中的问题经常没有提供完整信息，例如缺少一个比率、关系、定义范围或必要事实。此时直接给出确定答案可能是错误的，但简单回答“我不知道”又不够有帮助。模型需要判断缺少什么信息，并根据情况向用户询问、说明答案取决于哪个未知量，或在无法提供有用条件答案时明确弃答。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 Ask-Condition-Abstain Reinforcement Learning（ACA-RL），将缺少前提的问题加入强化学习训练，并用结构化奖励区分五类可观察行为：无声幻觉、明确假设、弃答、条件化表述和主动询问。
- 构建 Missing-Premise Benchmark（MPB）以评估模型处理信息不足问题的能力；该基准包含 274 个经人工验证的实例，覆盖数学、逻辑和现实文字题，并与训练使用的行为类别保持对应。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大语言模型的推理能力通常通过“答案可验证”的完备问题进行强化学习：模型读取题目、生成推理与最终答案，再依据答案是否正确获得奖励。这一范式默认题目包含确定唯一答案所需的全部前提，但真实用户查询可能遗漏数值、关系、定义适用条件或其他关键约束，使问题处于欠定状态。本文研究的重点不是检索缺失的外部事实，也不是校准答案概率，而是训练并评估模型能否从题面本身识别“现有前提不足”，继而采取有用的终端响应：询问缺失前提、用未知量给出条件化答案，或在无法提供有效条件表达时弃答。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**答案导向强化学习**

一种用最终答案是否匹配标准答案作为主要奖励信号的训练方式，适合答案明确且可自动验证的问题。若题目缺少必要前提，这种奖励会继续推动模型输出确定答案，因而可能诱发无依据猜测。

</div>
<div class="concept-item" markdown="1">

**缺失前提推理**

题目形式上类似常规推理题，但至少缺少一个确定唯一答案所必需的前提。模型需要识别缺口并显式暴露、参数化或请求该信息，而不是偷偷补入假设。

</div>
<div class="concept-item" markdown="1">

**终端响应行为**

本文关注模型最终表现出的可观察行为，而非其内部置信度或概率是否校准。响应被划分为静默幻觉、显式假设、弃答、条件化表述和主动询问五类，其中询问与条件化回答通常比笼统拒答更有帮助。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个原本完备的源问题 $s_0$，通过删除、模糊化或扰动关键前提得到缺失前提问题 $s^{\prime}$，并以 $a_{\text{gap}}$ 标注具体的信息缺口。模型输入是看似可正常求解、实际上不能由现有条件确定唯一答案的 $s^{\prime}$；输出是单轮终端响应。理想策略应根据缺口的性质选择三类建设性行为之一：直接询问用户补充所缺前提；将缺失量保留为变量，说明答案如何随该变量变化；或者在无法形成有信息量的条件回答时明确弃答。评估不要求模型恢复被删去的真实值，也不把所有不确定问题统一处理为“我不知道”，而是判断响应是否暴露、参数化或请求缺失信息。论文进一步以五类行为刻画输出质量：静默幻觉和无支持的确定答案最差，显式假设虽揭示了假设但仍可能擅自补全信息，弃答更安全，而条件化表述与主动询问通常具有更高实用性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$s_0$**

包含求得唯一答案所需全部前提的完备源问题。

</div>
<div class="notation-item" markdown="1">

**$s^{\prime}$**

由源问题扰动而成、至少缺少一个必要前提的问题。

</div>
<div class="notation-item" markdown="1">

**$a_{\text{gap}}$**

对缺失前提所在位置或具体信息缺口的局部标注。

</div>

</div>

**直接相关的工作**

- **UMWP**: UMWP由人类专家标注不可回答的 MathWorld 问题，主要用于考察不可回答数学题上的幻觉与弃答。本文的 MPB 与其问题意识相近，但把评估对象扩展为数学、逻辑和现实文字题中的多种缺失前提扰动，并区分询问、条件化回答、弃答、显式假设和静默幻觉，而不只检查是否拒绝作答。
- **Treecut**: Treecut通过移除推理依赖图中的一条边来合成不可回答数学题，与本文利用推理结构制造信息缺口的思路直接相关。本文进一步使用局部缺口标注训练单轮响应策略，并强调模型应在询问、条件化回答与弃答之间作出选择。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现有推理模型主要在前提完整、最终答案可验证的问题上接受强化学习，因此容易把“无法由已知信息唯一确定”的问题当作普通题目求解。在真实用户查询中，缺失的可能是关键数值、关系、定义适用范围或外部事实；模型若仍给出确定值，就会产生看似连贯但没有依据的答案。安全地说“我不知道”可以降低幻觉，却未必满足用户需求，因为模型有时能够指出缺失变量、写出依赖该变量的答案，或直接询问所需前提。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **检索或外部信息补充**：系统通过检索外部事实来补足输入中的信息，再进行推理。它适合缺少的是可从外部来源获得的事实，但不能根本保证基础模型已经学会识别问题是否在当前前提下不充分。
- **先筛查后回答与提示式自省**：系统先用额外的推理步骤或提示判断问题是否缺少前提，再决定回答或拒答；LM Introspection 属于论文比较的此类方法。它不改变模型本身的响应策略，效果依赖额外的推理步骤及模型在推理时是否稳定执行该判断。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 检索只能补充可获得的外部事实，不能教会模型识别输入内部的逻辑不完备性；当缺失前提并不存在于可检索来源中时，模型仍可能把不充分问题误当成有唯一答案的问题。
- 统一拒答或依赖提示式筛查都不能稳定覆盖有用的中间行为：前者会放弃本可提供的条件化答案或澄清问题，后者需要额外的推理时步骤。论文因此认为，仅靠提示不足以让模型在缺失前提时可靠地提问、条件化作答或弃答。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究较少把“识别问题欠定并采取合适响应”作为模型内部需要学习的推理策略。尚未解决的具体空缺是：如何利用可规模化的训练实例和可验证的行为奖励，使模型不仅避免直接幻觉，还能根据缺失前提的性质，在明确假设、条件化表达、主动询问和弃答之间作出区分，同时不显著损害完整前提问题上的正常推理能力。

</div>
<div markdown="1"><span>核心问题</span>

对于缺少决定性前提、因而无法得到唯一答案的推理问题，能否通过数据增强的强化学习在模型内部学习一种响应策略，使模型稳定识别欠定性，并在提问、条件化作答和弃答之间选择比直接猜测或笼统拒答更合适的行为？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把完整问题中的关键推理连接人为“断开”，生成带有局部缺口标注的缺少前提实例，再直接用这些实例训练目标行为。这样模型学习的不是抽象地降低置信度，而是把“哪一个前提被缺失”与“应该如何回应”联系起来：如果未知量仍允许写出有用的关系式，就给出条件化答案；如果用户能够补充该信息，就主动询问；如果没有可解释且有用的条件结果，再选择弃答。结构化奖励把这些行为区分开，有助于避免模型仅通过泛化拒答来获得表面上的安全性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ACA-RL由“受控缺失前提数据构造”和“行为奖励强化学习”两部分组成。首先从答案唯一的完备推理题$s_0$出发，将其拆成背景、条件与问题，并把求解过程表示为有向无环推理图；随后定位答案路径上的关键条件$c$，对其进行定向扰动得到$c'$，生成表面自然但逻辑上信息不足的问题$s'$，同时保存缺口标注$a_{\text{gap}}$。经过重写与质量复核后，这些样本组成训练集$\mathcal{D}_{\textsc{ACA}}$。训练时，策略$\pi_\theta$针对$s'$生成响应轨迹$\tau$，行为分类器将其归入静默幻觉、显式假设、弃答、条件化表达或主动追问五类，固定价值函数再把类别转换为标量奖励，以强化主动追问和条件化回答，并抑制无依据的确定性回答。
直观地说，该方法不是只教模型在信息不够时说“我不知道”，而是先人为制造“恰好缺少一个关键条件”的题目，再按回答的实际用途给予不同奖惩：能指出并询问缺失条件最好，能把未知量写进公式次之，单纯拒答可以接受，擅自补条件则受到惩罚。因而其训练目标是可观察的终端行为，而不是模型概率是否校准。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 完备问题拆解与推理图构建

将$s_0$解析为背景、条件集合$\{C_0\}$和问题，并生成逐步求解路径；再把条件到中间推理步骤及最终答案的依赖关系组织为有向无环图。

<div class="method-step__io" markdown="1">

**输入**：来自完备推理题集合$\mathcal{D}_G$的源问题$s_0$。<br>
**输出**：结构化问题成分，以及显式标出解题依赖关系的推理图。

</div>

**直观理解**：这一步相当于先画出一道题的“解题线路图”，从而知道哪些条件真正通向答案，而不是随机删除一句话。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 关键条件定位与定向扰动

沿推理图定位关键条件$c$，从论文定义的Conditional Breaking策略中均匀采样一种扰动方式，将$c$变为$c'$并替换回题面；同时记录缺失或被破坏信息的精确说明$a_{\text{gap}}$。

<div class="method-step__io" markdown="1">

**输入**：源问题$s_0$、其推理图，以及答案路径上的候选条件。<br>
**输出**：逻辑上欠定的问题与缺口标注对$(s',a_{\text{gap}})$。

</div>

**直观理解**：它像从机器的关键传动链中取走一个零件：题目仍然看似完整，但现有信息已不足以推出唯一答案，而且系统知道究竟缺了什么。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自然化重写与双重质量复核

把各部分重新组合并改写成流畅、表面上合理的文字题；再用基于大语言模型的质量过滤器检查推理图是否正确以及$s'$是否确实不可唯一作答，任一检查失败即丢弃。

<div class="method-step__io" markdown="1">

**输入**：扰动后的条件$c'$、原始背景与问题，以及对应推理图和缺口标注。<br>
**输出**：经过过滤的训练集合$\mathcal{D}_{\textsc{ACA}}$，其中每个样本均包含$(s',a_{\text{gap}})$。

</div>

**直观理解**：重写用于避免模型靠生硬删改痕迹识别样本，复核则防止把仍可求解或原本就有错误的题目送入训练。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 响应生成、行为分类与强化学习

策略生成完整响应轨迹$\tau$，行为分类器计算$\operatorname{Behav}(\tau)$，将其映射到五种互斥终端行为之一；价值函数$V$把类别转换为奖励，强化学习据此更新参数$\theta$以最大化期望行为价值。

<div class="method-step__io" markdown="1">

**输入**：欠定问题$s'\sim\mathcal{D}_{\textsc{ACA}}$和当前策略$\pi_\theta$。<br>
**输出**：更倾向于主动追问、条件化表达或必要时弃答，并减少显式假设和静默幻觉的策略。

</div>

**直观理解**：评分依据不是最后有没有写出数字，而是模型面对信息缺口采取了什么行动；因此训练可以区分“有帮助地处理未知条件”和“机械地拒绝回答”。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### ACA终端行为奖励

$$
R_{\textsc{ACA}}(\tau\mid s')=V\!\left(\operatorname{Behav}(\tau)\right),\qquad V(b)=\begin{cases}1.0,&b=\text{Elicit},\\0.6,&b=\text{Cond},\\0.3,&b=\text{Abs},\\-0.3,&b=\text{EA},\\-1.0,&b=\text{SH}.\end{cases}
$$

**符号说明**

- $R_{\textsc{ACA}}(\tau\mid s')$：策略在欠定问题上生成轨迹后获得的ACA行为奖励
- $s'$：由完备源问题扰动得到的缺失前提问题
- $\tau$：模型针对问题生成的完整响应轨迹
- $\operatorname{Behav}(\tau)$：把轨迹映射到五种终端行为之一的分类函数
- $V(b)$：将行为类别映射为固定标量奖励的价值函数
- $b$：行为类别，取Elicit、Cond、Abs、EA或SH之一

<div class="equation-explanation" markdown="1">

**直观理解**：该式先判断回答属于哪种行为，再按预设层级发放奖励。它把“是否有用地处理信息缺口”转成强化学习可优化的数值信号，同时明确惩罚未说明依据的确定性回答。<br>
**原文位置**：第4节 Ask-Condition-Abstain RL，公式(1)及紧随其后的价值函数定义

</div>

</div>

<div class="equation-block" markdown="1">

#### ACA-RL期望回报目标

$$
J_{\textsc{ACA}}(\theta)=\mathbb{E}_{s'\sim\mathcal{D}_{\textsc{ACA}}}\!\left[\mathbb{E}_{\tau\sim\pi_{\theta}(\cdot\mid s')}\!\left[V\!\left(\operatorname{Behav}(\tau)\right)\right]\right]
$$

**符号说明**

- $J_{\textsc{ACA}}(\theta)$：参数为θ的策略在缺失前提训练分布上的期望行为价值
- $\theta$：待优化的策略模型参数
- $\mathcal{D}_{\textsc{ACA}}$：经推理图扰动、重写和质量过滤得到的缺失前提训练集
- $\pi_{\theta}(\cdot\mid s')$：给定欠定问题时，当前策略对响应轨迹的条件分布
- $\mathbb{E}$：分别对训练问题采样和策略响应采样计算期望

<div class="equation-explanation" markdown="1">

**直观理解**：该目标要求模型在许多欠定问题及可能响应上获得尽可能高的平均行为奖励。优化后，概率质量会从静默幻觉和无依据假设转向主动追问、条件化表达与必要的弃答。<br>
**原文位置**：第4节 The ACA-RL Objective，公式(2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练直接最大化$J_{\textsc{ACA}}(\theta)$，即策略在$\mathcal{D}_{\textsc{ACA}}$上的期望终端行为价值。其关键作用是为答案监督中通常不存在的“询问缺失条件”和“用未知量条件化作答”提供显式梯度方向；由于奖励只依赖行为分类结果，该目标优化的是行为稳健性而非置信概率校准。作者同时使用cold-start SFT提供初始行为先验，再通过强化学习细化ask/condition/abstain策略；所给章节未明确报告具体策略梯度算法、优势估计、KL约束或各阶段损失的组合公式。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 推理图引导的缺失前提合成器**

该模块以完备问题$s_0$的求解依赖为依据，只扰动答案路径上的关键条件$c$，并同步产生缺口标注$a_{\text{gap}}$。与随机删除文本不同，这种“外科手术式”扰动尽量保留原题结构，同时使$s'$具有明确且可定位的信息缺口。

> 直观理解：它保证训练题难点来自真正缺少推理所需的信息，而不是语句残缺、格式异常或无关噪声。

**2. 终端行为分类器**

分类函数$\operatorname{Behav}(\tau)$把响应轨迹划分为五个互斥集合：静默幻觉$\mathcal{T}_{\text{SH}}$、显式假设$\mathcal{T}_{\text{EA}}$、弃答$\mathcal{T}_{\text{Abs}}$、条件化表达$\mathcal{T}_{\text{Cond}}$和主动追问$\mathcal{T}_{\text{Elicit}}$。分类关注响应最终如何处理缺失信息，而非模型内部置信度。

> 直观理解：同样没有直接给出答案，“请补充条件”“设未知条件为变量”和“我不知道”的帮助程度不同；分类器负责把这些行为区别开来。

**3. 分层行为价值函数**

固定价值函数按$\text{Elicit}\succ\text{Cond}\succ\text{Abs}\succ\text{EA}\succ\text{SH}$排序，分别赋值$1.0$、$0.6$、$0.3$、$-0.3$和$-1.0$。这些数值表达作者预设的行为偏好层级，并非通过概率校准或数据拟合得到的权重。

> 直观理解：最高奖励给能推动对话获得缺失信息的追问；条件化答案仍保留推理价值，单纯拒答只是安全后备，而无依据补条件会被扣分。

**训练与推理**

训练数据阶段从完备问题集合$\mathcal{D}_G$采样$s_0$，构建推理图、定向破坏关键条件、生成$a_{\text{gap}}$并通过质量过滤，最终形成$\mathcal{D}_{\textsc{ACA}}$。策略训练阶段先进行cold-start SFT初始化，再对$s'$采样响应轨迹$\tau$；行为分类器判定终端类别，$V(\operatorname{Behav}(\tau))$产生标量奖励，优化器据此更新$\theta$。推理时只需向训练后的策略输入新问题，策略直接生成追问、条件化答案或弃答；缺口标注$a_{\text{gap}}$用于数据构造与奖励设计，原文节选未说明推理时需要将该标注作为额外输入。

**复现信息**

训练集包含约$120\text{K}$个生成实例；MPB来自独立留出候选池并经人工专家验证，不与强化学习训练实例混用。扰动策略从Conditional Breaking方法中均匀采样，质量过滤同时检查推理图正确性与问题不可唯一作答。为公平解释方法，应注意五档奖励是人工设定的偏好值，行为分类器的误差会直接转化为奖励噪声；所给章节未明确报告分类器架构、cold-start SFT样本规模、强化学习优化器、采样超参数及训练时是否显式使用$a_{\text{gap}}$，因此这些复现细节仍需查验正文其他章节或附录。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MPB是作者构建的缺失前提行为基准，共274个样本；它从未参与训练的候选池中筛选，并经过缺失前提有效性核验。该基准与12万条ACA-RL训练实例相互独立，主要检验模型遇到信息不足的问题时，能否采取询问、条件化回答或弃答等合适行为。
- UMWP与SUM是第三方不可回答问题数据集，用于测试分布外鲁棒性。它们与MPB的作用不同：MPB直接对应作者设计的缺失前提场景，而UMWP和SUM用于检查学到的行为能否迁移到外部数据，而非只适配自建基准。
- GSM8K、MATH-500和AIME’24组成正常、前提完整的数学与逻辑推理测试组，用于衡量鲁棒性训练是否牺牲普通解题能力。GSM8K和MATH-500报告单次生成的Pass@1，AIME’24报告8次采样的平均Pass@1。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Behavior Score**

GPT-5先把每个回答归入五类终止行为，再映射为离散分数：无提示地臆答为0，明确声明假设为25，弃答为50，基于未知变量给出条件式答案为75，主动询问缺失前提为100；基准得分是所有样本的算术平均。它衡量的不只是是否拒绝，还衡量模型是否有效利用现有信息并主动补全缺失条件。 （越高越好，因为更高分对应条件化回答或主动询问，而不是无依据作答。不过该指标的类别定义同时参与训练奖励设计和测试评分，因此应理解为与作者行为量规对齐的表现，而非完全独立的开放式正确性评价。）

</div>
<div class="metric-item" markdown="1">

**IDK score**

采用二元评分：对不可回答问题按要求输出“$\boxed{I don$'t know.}”视为正确，否则视为错误。它主要测量保守弃答能力，不能区分主动询问、条件化回答与其他利用已知信息的行为。 （越高越好，表示模型更能识别不可回答问题并拒绝作答；但单独追求该分数可能鼓励过度拒绝，因此不能替代Behavior Score。）

</div>
<div class="metric-item" markdown="1">

**Pass@1**

衡量模型第一次生成是否得到正确答案，用于前提完整的GSM8K、MATH-500和AIME’24。AIME’24的报告值为8次运行或采样的平均Pass@1。 （越高越好，因为它表示模型在正常、可回答问题上的直接解题成功率更高；在本文中，该指标主要承担能力保持检查，而不是衡量缺失前提行为。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3-8B在MPB上的缺失前提行为比较

<div class="result-value" markdown="1">

作者报告ACA-RL的MPB Behavior Score为51.73，高于Vanilla PPO的8.66，也高于IDK-RL的48.72。相对Vanilla PPO提升43.07分，说明仅奖励完整问题的最终答案不足以形成缺失前提处理能力；相对IDK-RL提升3.01分，则表明结构化行为奖励在相同量规下比单纯学习IDK略有优势。

</div>

作者的结论是，ACA-RL不仅减少无依据作答，还会把部分回答引向条件化表达和主动询问。分析上，Vanilla PPO的大幅落后是较强证据，说明答案导向RL与缺失前提行为不匹配；但ACA-RL对IDK-RL的优势较小，而且评测量规正好奖励ACA-RL所训练的行为，因此该结果不能单独证明其在所有真实场景中都比保守拒答更可靠。

<div class="result-source" markdown="1">

来源：第5.2节，Table 1正文说明

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Qwen3-8B, ACA-RL obtains an MPB Behavior Score of 51.73, compared with 8.66 for Vanilla PPO and 48.72 for IDK-RL.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨模型架构与规模的总体缺失前提鲁棒性

<div class="result-value" markdown="1">

作者称ACA-RL在Qwen3-8B、Qwen3-14B和Llama3.1-8B-Instruct三个模型组上均改善了缺失前提鲁棒性，说明方法的效果并非只出现在单一参数规模或单一模型家族。所给节选未包含Table 1的完整数值，因而无法核验各模型组的提升幅度、方差或统计显著性。

</div>

这一结果主要测试方法是否具有架构迁移性。它支持“多个模型组上方向一致”的作者主张，但不等于证明对任意模型都有效；尤其是节选缺少完整表格和置信区间，不能判断较小提升是否稳定，也不能比较不同架构受益程度。

<div class="result-source" markdown="1">

来源：第5.2节，Table 1正文说明

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 1, ACA-RL improves missing-premise robustness across all three model groups.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### GPT自动裁判与人类专家在MPB行为标签上的一致性检查

<div class="result-value" markdown="1">

3名人类专家与GPT裁判在抽样回答上的标签一致率约为98%和95%：前者对应抽样的GPT-5回答，后者对应抽样的Qwen3-235B-A22B-Instruct回答。作者据此认为MPB自动评分具有较好一致性，并对不同回答生成模型保持一定评估独立性。

</div>

该检查回答的是“分数是否只是自动裁判随意给出的”。高一致率表明，在作者定义的五类行为标签下，人类与GPT大多能作出相同分类。不过原文未明确报告抽样规模、类别分布、置信区间或机会校正一致性，因此98%和95%不能证明裁判没有系统偏差，也不能证明Behavior Score与真实任务效用完全一致。

<div class="result-source" markdown="1">

来源：附录E.4，Conclusion

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Human labels agree with the GPT judge on approximately 98% of the sampled GPT-5 responses and 95% of the sampled Qwen3-235B-A22B-Instruct responses.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- Behavior Score的五类定义同时用于训练奖励与MPB测试评分，因此ACA-RL与评测量规存在直接对齐关系。虽然MPB来自留出候选池，且人类与GPT裁判有较高标签一致率，但这主要证明按既定量规分类较稳定，不能完全排除指标偏向方法设计；原文也未明确报告人工抽样规模、类别不平衡情况或机会校正一致性。
- 所给实验节选缺少Table 1和Table 5的完整数值，也未报告主要结果的方差、置信区间或显著性检验。除AIME’24采用8次平均外，无法判断MPB上ACA-RL相对IDK-RL的3.01分优势是否具有重复训练稳定性；比例消融又仅在Qwen3-8B、10K样本和100步设置下进行，其最优折中不宜直接推广到所有模型和训练规模。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Cold-start SFT：Qwen系列在合成数据上进行监督微调后得到的初始检查点，不包含后续强化学习；它用于区分监督冷启动本身与强化学习带来的行为变化。Llama3.1-8B-Instruct则直接采用原始指令模型，不额外蒸馏思维链或“Think”轨迹。
- Vanilla PPO：只使用前提完整、可回答的问题训练，并仅奖励最终答案正确。它代表传统的答案导向强化学习，用来检验普通正确性奖励是否足以自动产生缺失前提意识。
- IDK-RL：混合可回答与不可回答问题训练；对前者奖励正确解答，对后者仅奖励输出IDK。它是最关键的行为基线，因为其训练数据与ACA-RL相同，但目标偏向二元弃答，因而能够比较“只学会拒绝”与“询问、条件化回答、弃答三种行为”之间的差异。
- ACA-RL：作者方法；训练集约30%的样本通过推理图引导的条件扰动转化为缺失前提版本，并用结构化奖励鼓励询问缺失前提、根据未知变量给出条件式答案，或在无法继续时弃答。

**实验想回答的问题**

- ACA-RL能否在自建的缺失前提基准MPB及第三方不可回答问题基准上，使模型从无依据作答转向询问缺失信息、给出条件化答案或明确弃答，同时避免明显损害正常推理能力？
- 缺失前提训练数据的生成来源和混合比例如何影响行为鲁棒性与标准推理能力之间的权衡？

**实验实现**

实验覆盖Qwen3-8B、Qwen3-14B和Llama3.1-8B-Instruct。所有强化学习方法均使用veRL实现PPO，并在各RL基线间保持可回答训练查询总量和计算预算一致；IDK-RL与ACA-RL使用相同的合成数据，从而把主要差异集中到奖励设计。主训练使用12万条ACA-RL实例，默认约30%为缺失前提版本；训练数据仅由DeepscaleR合成或选取。PPO共训练400步，批大小512，actor与critic学习率均为$1\times 10^{-6}$，KL系数为0，最大响应长度为14000；硬件为4个节点、每节点8张GPU。KL系数为0意味着训练不通过KL惩罚约束新策略贴近初始策略，这有利于探索新行为，但也可能增加能力漂移风险。

MPB自动评测由GPT-5完成：先判定五类行为，再按0、25、50、75、100映射并求平均。由于训练奖励和基准评分使用同一套类别定义，结果应视为“对该行为量规的留出集泛化”。作者另请3名具有研究生学位的专家，对部分GPT-5及Qwen3-235B-A22B-Instruct回答进行同标签标注，以检查自动裁判一致性；这能支持标签判定的稳定性，但不能消除量规本身可能偏向ACA-RL目标的风险。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 固定数据预算下比较缺失前提训练数据来源：Treecut、SUM与推理图引导合成 | 作者方法在MPB上得到51.73，高于SUM来源的47.35和Treecut的15.41；同时GSM8K为91.50、AIME’24为64.16。与SUM相比，作者方法的MPB提高4.38分，GSM8K提高0.45分，AIME’24提高4.58分；与Treecut相比，MPB提高36.32分，但Treecut的GSM8K和AIME’24分别更高2.51分和3.34分。 | 该消融在固定数据预算下隔离“缺失前提样本从哪里来”的影响。结果支持推理图引导合成比直接加入SUM式不可回答数据更适合本文量规；Treecut保持普通推理能力较好，却几乎没有学到同等强度的缺失前提行为。它说明数据构造方式重要，但由于节选未明确说明不同来源样本在难度、题型和语言分布上的匹配程度，不能把全部差异严格归因于推理图机制。 | Table 3，列顺序为Source、MPB、GSM8K、AIME’24<br><span class="experiment-evidence">Ours 51.73 91.50 64.16</span> |
| 在10K训练样本、100步训练条件下，将缺失前提样本比例设为10%、30%或50% | 50%比例取得最高MPB 53.19，但GSM8K和AIME’24降至82.10和52.56；30%比例对应43.79、90.14和60.83；10%比例对应28.28、92.49和63.33。从10%提高到50%使MPB增加24.91分，同时GSM8K下降10.39分、AIME’24下降10.77分。作者选择30%作为默认折中。 | 该消融直接测量训练分布中“不可回答行为监督强度”的影响。更多缺失前提样本确实强化目标行为，但模型减少了对正常可回答问题的训练暴露，或策略更倾向保守响应，因此标准推理能力下降。30%并非在每个指标上最优，而是在MPB提升与普通推理保持之间选取的操作性折中；此外，该消融仅使用Qwen3-8B、10K样本和100步，未证明同一比例对完整12万样本训练或其他模型同样最优。 | Table 4，列顺序为Portion、MPB、GSM8K、AIME’24<br><span class="experiment-evidence">50% 53.19 82.10 52.56</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work uses reinforcement learning to improve reasoning under missing premises through asking, conditioning, or abstaining.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`97140430674a237c4396d2603930b35d133defc0685e83fd8a0c2a2fd1802f51`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
