---
title: "[论文解读] SkillCAT: Contrastive, Assessment-Augmented and Topology-AwareSkill Self-Evolution for LLM Agents"
description: "[arXiv 2606.13317][LLM Agent] SkillCAT针对大语言模型智能体从执行轨迹中自动提炼技能时证据不可靠、更新缺乏验证和推理上下文冗余的问题，引入对比提取、回放筛选与拓扑路由三个环节。"
arxiv_id: "2606.13317"
announcement_date: "2026-07-30"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:25.155990+00:00"
source_sha256: "e3f947b2e95c9fd008e107226c8f5a85b539b69ab57ffc8c1ed9a0b42fc2996a"
tags:
  - "LLM Agent"
  - "大语言模型智能体"
  - "技能自演化"
  - "执行轨迹"
  - "技能补丁"
  - "对比因果提取"
  - "任务回放验证"
  - "拓扑感知路由"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2606.13317</p>

# SkillCAT: Contrastive, Assessment-Augmented and Topology-AwareSkill Self-Evolution for LLM Agents

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Kunfeng Chen, Qihuang Zhong, Juhua Liu, Bo Du</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2606.13317v2) · [PDF 下载](https://arxiv.org/pdf/2606.13317v2) · **关键词** 大语言模型智能体, 技能自演化, 执行轨迹, 技能补丁, 对比因果提取, 任务回放验证, 拓扑感知路由  


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

SkillCAT针对大语言模型智能体从执行轨迹中自动提炼技能时证据不可靠、更新缺乏验证和推理上下文冗余的问题，引入对比提取、回放筛选与拓扑路由三个环节。

**不用术语来说**：智能体可以把过去完成任务的过程整理成可复用的“操作指南”，以后无需更新模型参数便能借鉴经验；但一次成功可能只是偶然，一次失败也未必暴露真正原因，而且把所有总结直接写入指南、使用时再整本加载，容易让错误或互相冲突的规则不断累积，并浪费有限的上下文空间。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将现有技能自进化流程的关键缺口归纳为单轨迹偏差、未经验证的合并和推理时上下文过载，并据此把技能生命周期拆分为证据提取、更新验证与执行调用三个可检查阶段。
- 作者提出SkillCAT：用同一任务的多次成功—失败轨迹对比定位影响结果的候选经验，在源任务副本上回放候选补丁以排除有害更新，再把技能组织为可路由的能力节点，使推理仅加载与当前任务相关的内容。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型（LLM）智能体的技能自演化研究。LLM 智能体需要在电子表格操作、表格问答或文档问答等任务中进行多步决策并调用工具；为避免更新模型参数，可在推理时向智能体提供外部“技能文档”，其中记录可复用的操作流程、工具使用规则和任务经验。技能自演化进一步利用智能体过去的执行轨迹自动提炼、修订这些文档：早期方法通常按轨迹顺序逐次更新技能，而 Trace2Skill 一类方法先从每条轨迹生成局部技能补丁，再离线合并为通用技能。本文聚焦的核心问题不是训练新的基础模型，而是如何从已有执行记录中可靠地产生技能更新、验证更新质量，并在执行新任务时只加载相关技能内容。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**执行轨迹（execution trajectory）**

智能体完成一个任务时留下的完整过程记录，通常包含观察、推理或决策、工具调用、环境反馈以及最终成败结果。技能自演化方法将轨迹视为经验来源，从中寻找值得复用或需要避免的行为。

</div>
<div class="conceptitem" markdown="1">

**技能文档与技能补丁（skill document / skill patch）**

技能文档是推理时提供给智能体的外部指导文本；技能补丁是根据某次或某组执行经验提出的局部新增、删除或修改内容。多个补丁经筛选和合并后形成演化后的技能，而不改变 LLM 本身的参数。

</div>
<div class="conceptitem" markdown="1">

**技能拓扑与路由（skill topology and routing）**

技能拓扑把一份较长的技能文档拆成表示不同能力的节点，并组织其结构或关联。路由是在面对具体任务时选择相关节点，使智能体无需把全部技能文本都放入上下文。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一组任务及智能体在这些任务上的多次执行轨迹，每条轨迹带有成功或失败等结果信号，并给定一份待改进的初始技能文档；系统需要从同一任务的多条轨迹中提取候选技能补丁，检查补丁是否会改善或至少不损害其来源任务，再将合格补丁整合为演化后的技能。部署时，输入是一个待执行的新任务以及演化后的技能库，输出既包括为该任务路由得到的相关子技能内容，也包括智能体在这些内容指导下产生的任务执行结果。该设置假定技能能够以外部文本形式注入上下文，因而无需更新模型权重；同时允许技能作者模型与实际使用技能的模型相同或不同，并考虑分布外任务上的迁移。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Trace2Skill（Ni et al., 2026）**: 与本文最直接相关的离线批处理范式：从每条执行轨迹提取一个局部技能补丁，再将多个补丁整合为较通用的技能编辑。SkillCAT 延续“轨迹到技能”的总体设置，但针对其单轨迹证据不足、补丁未经独立验证便合并，以及推理时加载完整技能语料的问题，分别引入同任务成功/失败对比、来源任务回放验证和拓扑化路由。
- **SkillOpt（Yang et al., 2026a）**: 建立在 Trace2Skill 式技能演化范式之上，将技能自演化类比为梯度下降并进行迭代优化。本文与其共同目标是从历史执行中改进外部技能，但 SkillCAT 更强调补丁生成所依据的对比证据、合并前的任务级质量控制，以及推理阶段的选择性技能加载。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

长流程、需要工具交互的任务通常依赖可复用的程序知识和历史经验。人工持续编写技能文档成本高，因此需要让智能体从自身轨迹中自动形成和改进技能；真正的需求不只是“能总结”，而是让技能更新具有可信证据、不会破坏已有能力，并能在技能库扩大后仍以较低上下文开销被调用。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **顺序式技能自进化**：Reflexion、Self-Refine等相关范式通常按照轨迹到达顺序工作：根据一条新轨迹对当前技能做一次文本更新，然后继续处理下一条轨迹。其优点是流程直接，但每次编辑都建立在单次经历及当前技能版本之上。
- **Trace2Skill式离线批处理**：Trace2Skill从每条轨迹分别抽取局部技能补丁，再批量整合为较一般的技能修改；SkillOpt进一步把技能演化类比为梯度下降，通过迭代优化进行细化。这类方法缓解了纯顺序更新的问题，但仍主要采用“一条轨迹产生一个补丁、随后统一合并”的基本结构。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单条轨迹提供的因果证据较弱：成功可能来自偶然策略，失败轨迹也往往只显示表面症状而非根因。因此，直接概括整条轨迹容易把与结果无关的细节误写成通用规则，形成作者所称的“单轨迹偏差”。
- 候选补丁在合并前通常没有独立验证其对来源任务的实际影响，低质量甚至有害的修改可能进入技能库；技能库增长后若在推理时整体加载，还会把无关或冲突规则同时交给智能体，既占用上下文，也可能降低任务表现。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作证明了执行历史可以被蒸馏为技能，却缺少一条闭环机制来依次回答三个问题：某项经验是否真正解释了任务成败、写入后是否至少不损害原任务、实际执行时是否只向模型暴露当前任务需要的技能内容。换言之，技能的证据质量、更新安全性和调用选择性尚未被统一处理。

</div>
<div markdown="1"><span>核心问题</span>

能否设计一个无需更新模型权重的技能自进化框架，利用同任务的多次执行提高经验提取的可信度，通过任务级回放阻止有害补丁进入技能库，并借助结构化路由减少推理时的无关技能上下文，同时保持跨任务和跨模型的可复用性？

</div>
<div markdown="1"><span>作者直觉</span>

同一道题的成功与失败轨迹共享任务条件，比较二者比孤立总结一条轨迹更容易找到导致结果分化的关键做法；候选规则先回到原任务上“试用”，相当于在写入长期手册前做最小质量检查；最后把整本手册拆成带关系的能力模块，并按任务选取模块，就能避免每次都把所有规则塞给模型。三者分别在技能形成、写入和使用之前设置筛选关口。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SkillCAT把大语言模型智能体的“技能自进化”设计为离线学习与在线部署相衔接的三阶段流程。输入包括基础技能文档 S_0、用于积累经验的进化任务集合 \mathcal{X}，以及未见测试任务集合 \mathcal{X}^{*}。离线阶段先对每个进化任务进行多随机种子执行，由对比因果提取（CCE）比较同一任务的成功与失败轨迹，在行为分叉处提炼可编辑经验并生成候选补丁；随后，评估增强进化（AAE）把每个补丁单独应用到临时技能上，重放其来源任务，只保留能够修复失败或维持成功的补丁，并按评分分层合并为进化技能 S^{*}。在线阶段，拓扑感知任务执行（TTE）把 S^{*}编译为核心技能、能力节点及依赖拓扑，再针对每个测试任务路由少量相关节点，组装运行时技能 S_j。
直观地说，该方法不是把所有历史轨迹都总结后塞进一个不断膨胀的说明书，而是依次回答三个问题：成功与失败到底差在哪里、由此写出的规则是否真的有用、当前任务究竟需要说明书中的哪些部分。前两步控制经验的可靠性与补丁质量，最后一步控制推理时注入上下文的相关性和长度。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多种子轨迹采集与结果分组

智能体用多个随机种子重复执行同一任务，得到轨迹集合 \mathcal{T}_i，并依据官方评估器标注拆分为成功集合 \mathcal{T}_i^{+} 与失败集合 \mathcal{T}_i^{-}。

<div class="method-step__io" markdown="1">

**输入**：基础技能 S_0 与进化任务 x_i\in\mathcal{X}。  
**输出**：带有成功或失败标签的同任务多样化执行轨迹。

</div>

**直观理解**：同一道题多做几次，才能区分稳定有效的行为与偶然结果；成功和失败标签为后续对照提供依据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 对比因果提取与候选补丁生成

当成功与失败轨迹都存在时，CCE随机抽取一对轨迹，由LLM提取器定位动作序列的关键分叉，写出包含局部证据、失败原因和可编辑教训的经验记录 r_i；若只有单一结果类型，则退化为单轨迹提取。技能编辑器再结合 r_i 与 S_0 生成候选技能补丁 p_i。

<div class="method-step__io" markdown="1">

**输入**：同一任务的成功轨迹 \tau_i^{+}、失败轨迹 \tau_i^{-}，以及基础技能 S_0。  
**输出**：与来源任务绑定的候选经验记录 r_i 和技能编辑补丁 p_i。

</div>

**直观理解**：它像比较同一道题的一份正确解答和一份错误解答，重点找出两者从哪里开始走向不同，而不是笼统复述整段过程。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 来源任务重放、筛选与分层合并

AAE把每个 p_i 隔离地装入临时技能，在来源任务的克隆上重放得到 \hat y_i，并按结果转移评分；仅保留 a_i\geq\theta 的补丁，然后按分数从低层到高层依次调用技能合并算子 \mu。

<div class="method-step__io" markdown="1">

**输入**：候选补丁集合、各补丁的来源任务、原始任务结果 y_i，以及阈值 \theta=2.0。  
**输出**：经过行为验证和层次化合并的进化技能 S^{*}。

</div>

**直观理解**：每条新规则先参加一次“回归测试”：能把失败修好或至少不破坏原有成功才可进入正式技能库，高分规则后合并以获得更高的最终优先级。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 技能拓扑编译、节点路由与运行时组装

TTE将 S^{*}编译为核心技能 S_c、能力节点集合 \mathcal{V}、节点正文 B_v 及含标题、关键词、摘要和依赖边的紧凑拓扑 \mathcal{G}；LLM路由器只读取 \mathcal{G} 选出不超过 k 个节点，组装器再将其正文与 S_c 合成为 S_j。

<div class="method-step__io" markdown="1">

**输入**：进化技能 S^{*}、测试任务 x_j^{*} 和最多可选节点数 k。  
**输出**：每个测试任务专属的紧凑运行时技能 S_j，供智能体执行该任务。

</div>

**直观理解**：这相当于先看目录和依赖关系选章节，再加载被选章节的全文，而不是每次都把整本技能手册放入上下文。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 候选补丁的来源任务结果转移评分

$$
a_i=\begin{cases}3.0,&(y_i,\hat{y}_i)=(0,1),\\2.0,&(y_i,\hat{y}_i)=(1,1),\\1.0,&(y_i,\hat{y}_i)=(0,0),\\0.0,&(y_i,\hat{y}_i)=(1,0).\end{cases}\qquad \mathcal{P}_{\theta}=\{p_i:a_i\geq\theta\},\quad\theta=2.0
$$

**符号说明**

- $p_i$：由第 i 个进化任务的经验生成的候选技能补丁。
- $y_i$：应用候选补丁前的原始任务结果，1表示成功、0表示失败。
- $\hat{y}_i$：把候选补丁装入临时技能并重放来源任务后得到的结果，1表示成功、0表示失败。
- $a_i$：候选补丁依据前后结果转移获得的评估分数。
- $\theta$：补丁接受阈值，本文设为2.0。
- $\mathcal{P}_{\theta}$：评分不低于阈值、允许进入后续合并的补丁集合。

<div class="equation-explanation" markdown="1">

**直观理解**：该规则把“修复失败”列为最高优先级，把“维持成功”视为可接受，并拒绝无效修复及破坏既有成功的补丁。它是AAE选择性进化的核心：技能编辑不再依赖语言模型对规则质量的自我判断，而是至少经过一次可观测任务结果检验。  
**原文位置**：Method—Assessment-Augmented Evolution，公式(2)与公式(3)

</div>

</div>

<div class="equation-block" markdown="1">

#### 拓扑约束路由与运行时技能组装

$$
\mathcal{V}_j=R(x_j^{*},\mathcal{G},k),\qquad |\mathcal{V}_j|\leq k;\qquad S_j=A\!\left(S_c,\{B_v\}_{v\in\mathcal{V}_j}\right)
$$

**符号说明**

- $x_j^{*}$：第 j 个未见测试任务。
- $\mathcal{G}$：由能力节点元数据和节点依赖边构成的紧凑技能拓扑摘要。
- $k$：单个测试任务最多允许选择的能力节点数，即节点预算。
- $R$：基于LLM的技能节点路由器。
- $\mathcal{V}_j$：路由器为测试任务 x_j^{*} 选择的能力节点子集。
- $S_c$：从进化技能中编译出的核心技能部分。
- $B_v$：能力节点 v 的原始完整正文。
- $A$：基于LLM的技能组装器。
- $S_j$：为第 j 个测试任务组装的运行时技能。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分在预算 k 下根据任务和技能目录挑选节点，第二部分才取回这些节点的完整正文并与核心规则合并。节点数量约束直接限制注入内容的范围，使推理上下文更紧凑且更具任务相关性。  
**原文位置**：Method—Topology-Aware Task Execution，公式(5)与公式(6)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：该方法没有报告通过梯度下降优化模型参数的训练损失；其“学习”对象是外部技能文档，而不是LLM权重。离线优化体现为离散的选择与编辑过程：CCE生成候选经验和补丁，AAE用来源任务重放所得的结果转移分数筛选补丁，再通过LLM技能合并算子逐层改写 S_0 得到 S^{*}。因此，公式中的 a_i 是补丁接受和排序信号，而非可微损失；在线TTE也属于上下文路由与组装，不更新模型参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Contrastive Causal Extraction（CCE，对比因果提取）**

CCE利用同任务成功—失败配对控制任务输入、可用工具和评估器等条件，使提取器集中分析造成结果差异的动作分叉。记录内容包括分叉附近的局部证据、失败原因及可转化为技能编辑的通用教训；无对比结果时仍保留单轨迹通道，以免纯成功或纯失败任务完全丢失经验。

> 直观理解：单条轨迹只能说明“发生了什么”，未必说明“为什么成功或失败”；同题正反例的直接比较更容易定位真正值得写进技能的行为差异。这里的“因果”是由受控对比提供的解释性证据，并不等同于严格的随机化因果识别。

**2. Assessment-Augmented Evolution（AAE，评估增强进化）**

AAE把补丁视为待检验假设，而非直接接受的规则。它比较补丁应用前后的二元任务结果，将失败变成功、成功保持成功、失败仍失败、成功变失败依次赋予3、2、1、0分；阈值设为2，因此只合并前两类补丁，并按低分到高分的顺序分层合并，最终得到 S^{*}。

> 直观理解：提炼出来的经验可能听起来合理，却可能无效甚至有害；来源任务重放提供最低限度的行为验证。需要注意，这种验证主要检查补丁在来源任务上的即时效果，不能单独证明其在所有新任务上都无副作用。

**3. Topology-Aware Task Execution（TTE，拓扑感知任务执行）**

TTE将技能拆成始终保留的核心部分和可路由的能力节点，并用节点标题、关键词、摘要及程序或工具依赖构建紧凑拓扑。路由阶段只看拓扑元数据，选定节点后才读取原始节点正文进行组装，从而把“检索哪些能力”和“注入哪些完整规则”分开。

> 直观理解：完整技能文档可能包含无关甚至冲突的规则，全部加载既占上下文又会干扰决策；按任务选择相关节点，可以让智能体只携带当前工作所需的操作指南。

**训练与推理**

离线技能学习阶段：对每个 x_i 多次执行并收集带官方成功/失败标签的轨迹；若两类轨迹均存在，则采样同任务成功—失败对并提取行为分叉经验，否则使用单轨迹记录；技能编辑器据此生成 p_i。随后把每个补丁隔离应用于临时技能，在来源任务克隆上重放，根据 y_i\rightarrow\hat y_i 评分，以 \theta=2.0 筛除无效或有害补丁；保留补丁按评分层级从低到高合并，得到 S^{*}，再将其编译为 (S_c,\mathcal{V},\mathcal{G}) 与节点正文集合。
在线推理阶段：对于每个未见任务 x_j^{*}，LLM路由器读取任务描述和紧凑拓扑 \mathcal{G}，在节点预算 k 内选择 \mathcal{V}_j；LLM组装器获取相应节点正文，与核心技能 S_c 合成为 S_j。智能体只加载 S_j 执行当前任务，而不是加载完整 S^{*}。CCE与AAE仅在离线技能学习时运行，TTE则负责任务部署时的在线选择。

**复现信息**

复现该方法所需的关键设定包括：每个进化任务必须采用多个随机种子运行，并由官方评估器将轨迹标为成功或失败；存在混合结果时，每个任务从成功集和失败集中各随机抽取一条组成对比对，缺少混合结果时使用单轨迹后备流程。AAE对每个候选补丁使用来源任务克隆进行隔离重放，接受阈值固定为 \theta=2.0，并将通过筛选的补丁按分数从低到高合并；文中说明其技能编辑过程直接复用Trace2Skill，以从重复编辑中提炼一般原则而非记忆实例修复。TTE需要为每个能力节点保存完整正文，同时生成标题、关键词、摘要和依赖关系作为路由元数据，并通过节点预算 k 限制在线选取规模。所给方法章节未明确报告多种子运行次数、k 的具体取值、路由与组装提示词、温度、重放次数或模型调用成本，这些项目应记为“原文未明确报告”，不能据此补造。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- SpreadsheetBench-Verified：SpreadsheetBench的人工验证子集，共400个真实Excel论坛任务，涉及单元格级和工作表级操作。按既有工作划分为200个演化样本与200个留出测试样本，是域内技能演化、主结果、消融和模块分析的核心基准。
- WikiTableQuestions（WikiTQ）：基于Wikipedia半结构化表格的问答基准。论文将其作为分布外测试，用于判断从电子表格任务中演化的技能能否迁移到不同形式的表格推理；按官方协议比较预测答案与标准答案的指称结果。
- DocVQA：文档图像视觉问答基准，采用官方验证集的5,349个问题—图像对，其中前2,700个用于技能演化，后2,649个用于评测。它检验SkillCAT是否能从电子表格代理场景推广到需要视觉理解与文本生成的多模态任务。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**SpreadsheetBench任务正确率（Acc）**

在输入工作簿上实际执行代理生成的方案，并将输出单元格与标准工作簿比较；只有全部答案匹配时，该任务才计为正确，因而是严格的端到端执行指标。 （越高越好，因为它表示完整完成电子表格任务的样本比例更大，而不只是生成了表面相似的操作步骤。）

</div>
<div class="metricitem" markdown="1">

**WikiTQ Accuracy**

按照官方协议比较预测答案与标准答案的指称，即最终答案所表示的实体或数值是否一致，用于测量分布外表格问答的正确率。 （越高越好，因为正确答案指称匹配的测试问题更多。）

</div>
<div class="metricitem" markdown="1">

**DocVQA ANLS与Acc（ANLS≥0.5）**

ANLS是基于归一化编辑距离的答案相似度，允许轻微字符串差异；Acc则统计ANLS至少为0.5的样本比例。前者反映答案文本的接近程度，后者强调达到可接受匹配阈值的比例。 （二者均越高越好；同时报告可以区分近似文本匹配与达到阈值的较可靠回答。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 域内SpreadsheetBench与分布外WikiTQ的总体结果，Qwen3.5-35B-A3B作为技能使用者，Human-Written初始化，并对两个技能作者和两个任务取平均。

<div class="result-value" markdown="1">

SkillCAT的平均得分为59.04%，第二名EvoSkill为42.21%，绝对领先16.83个百分点；正文称这是其相对最强技能演化基线的最大总体优势。

</div>

这一结果说明SkillCAT的收益不局限于单一任务或单一技能作者：把域内电子表格和分布外表格问答汇总后仍明显领先。然而，平均值可能掩盖具体任务差异，且不能单独证明三个模块各自都是增益来源；后者需要消融实验支持。

<div class="result-source" markdown="1">

来源：Main Results，“SkillCAT improves average performance across in-domain and OOD settings”；Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Its largest margin over the strongest skill-evolution baseline occurs for the Qwen3.5-35B-A3B user with Human-Written initialization: when averaged across the two skill authors and both tasks, SkillCAT reaches 59.04%, compared with 42.21% for the second-best (EvoSkill), a margin of 16.83%.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨模型迁移：将在Qwen作者模型上、Human-Written初始化下演化的技能直接用于未参与演化的Gemma-4-31B-it和GPT-5.4-mini。

<div class="result-value" markdown="1">

两种Qwen作者产生的技能分别使Gemma的平均分提升11.23%和14.27%，并使GPT-5.4-mini提升7.14和7.22分，且不需要针对新使用者重新演化。

</div>

这支持了演化结果包含可复用的技能内容，而非只适配原作者模型的行为习惯。不过迁移收益并非每个任务都为正：正文指出Gemma在WikiTQ上的无技能基础已经很强，其中一个SkillCAT变体相对Human-Written下降，因此“平均可迁移”不能解释为对所有接收模型、所有任务均稳定提升。

<div class="result-source" markdown="1">

来源：Main Results，“SkillCAT skills show average gains on unseen user models without re-evolution”；Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">As shown in Table 1, skills produced by either Qwen author improve the average score of both unseen users without re-evolution: by 11.23% and 14.27% for Gemma-4-31B-it and by 7.14 and 7.22 points for GPT-5.4-mini.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### DocVQA多模态评测：由Qwen3.5-35B-A3B生成技能，分别由同规模模型和Qwen3.5-122B-A10B使用。

<div class="result-value" markdown="1">

SkillCAT在两种使用者规模上均明显优于No-Skill；相较Trace2Skill，在匹配的35B使用者上同时取得更高ANLS和Accuracy，在122B使用者上ANLS相近但Accuracy更高。节选未给出Figure 3中的具体数值。

</div>

该结果表明方法不仅适用于电子表格操作，也可能改善文档图像问答。作者将更高Accuracy解释为补丁验证减少了只产生近似答案的噪声规则；但这仍是基于结果模式的机制解释，而不是对错误类型的直接因果证明，且缺少图中数值时无法判断优势幅度。

<div class="result-source" markdown="1">

来源：Main Results，“SkillCAT achieves consistent gains in multimodal settings”；Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">When applied to the larger Qwen3.5-122B-A10B user, although both methods yield comparable ANLS, SkillCAT still ensures higher Accuracy.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 节选主要报告平均分和点估计，虽使用3个随机种子，但未给出标准差、置信区间或显著性检验；尤其在任务级差距仅约零点几个百分点时，不能确认差异是否稳定超过随机波动。
- 跨模型迁移只覆盖两个额外使用者，且DocVQA图中具体分数、路由器在不同Top-k下的完整准确率与上下文缩减数据未包含于节选。因而可支持“存在跨模型与多模态泛化”，但不足以证明对广泛模型家族、任务和路由预算都普遍有效。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- No-Skill：不加载任何技能文档，衡量语言模型及工具代理本身的能力，是判断技能是否真正带来增益的下界参照。
- Human-Written与LLM-Gen初始化：前者使用Anthropic官方xlsx技能，后者使用相应LLM生成的初始技能。两种设置分别检验SkillCAT能否改进高质量人工技能和较不稳定的模型生成技能。
- Trace2Skill：从执行轨迹中提炼技能的直接对手，也是消融实验的主要参考。它代表缺少SkillCAT多轨迹因果对比、补丁回放筛选和拓扑化部署的既有演化流程。
- EvoSkill与SkillOpt：另外两种同期技能自演化方法，用于判断收益是否仅相对于某一个较弱基线成立。正文节选没有提供二者的具体算法细节，因此不能进一步比较其内部机制。

**实验想回答的问题**

- SkillCAT相较于无技能、初始技能及现有技能演化方法，能否在同域电子表格任务、分布外表格问答和多模态文档问答上稳定提升智能体表现，并且将演化所得技能迁移给未参与演化的模型？
- CCE、AAE与TTE分别解决了证据提取、补丁质量控制和推理时技能选择中的什么问题；性能提升是否确实依赖多轨迹对比、回放过滤及拓扑路由，而非单一模块或更长上下文？

**实验实现**

所有代理均运行于ReAct式执行框架，并可调用文件系统和电子表格工具。CCE对每个演化任务采样5条不同随机种子的轨迹，以构造同任务成功—失败对比；AAE在源任务克隆上回放候选补丁，仅保留奖励a_i≥2.0的补丁，再进行分层合并；TTE采用基于图的路由器选择Top-k=7个相关能力节点并注入当前任务。Qwen3.5-35B-A3B和Qwen3.5-122B-A10B同时作为技能作者与技能使用者；跨模型实验把Human-Written设置下由Qwen演化的技能直接交给Gemma-4-31B-it和GPT-5.4-mini，不重新演化。结果取3个随机种子的平均值。该设计分别控制初始技能来源、作者模型和使用者模型，但节选未报告方差或显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除AAE，保留CCE与TTE；SpreadsheetBench、Human-Written初始化，Qwen3.5-35B-A3B同时作为作者和使用者。 | 去除AAE后正确率降至26.00%，相对Trace2Skill参考值低3.67个百分点，并低于完整SkillCAT。它是留一模块消融中破坏最严重的设置。 | 该消融隔离了“候选补丁回放验证与按分数合并”的作用。即使CCE能产生对比证据、TTE能选择节点，未经验证的错误规则仍会进入全局技能，路由只能选择已有内容而不能纠正内容本身。因此结果支持AAE是技能可靠性的关键门控环节，但不能区分收益具体来自回放验证还是分层合并。 | Ablation Study；Table 2，-w/o AAE<br><span class="experiment-evidence">Without AAE, performance falls to 26.00% (-3.67%), because bypassing replay validation and score-guided merging introduces error rules into the global skill.</span> |
| 移除TTE，保留CCE与AAE；SpreadsheetBench、Human-Written初始化，Qwen3.5-35B-A3B同时作为作者和使用者。 | 不使用TTE时正确率为46.50%，相对Trace2Skill仍提高16.83个百分点，但低于完整流程的55.00%。 | 该设置说明CCE与AAE已经能产生较可靠的技能内容，因此即使整份技能直接使用也有明显收益；完整模型进一步领先，则支持按任务选择相关节点可以抑制无关内容。由于TTE同时改变所加载内容和上下文长度，这个消融尚不能完全区分收益来自更准确的拓扑选择，还是单纯来自缩短上下文。 | Ablation Study；Table 2，-w/o TTE<br><span class="experiment-evidence">In contrast, when TTE is absent and CCE and AAE are retained, we still achieve 46.50% (+16.83%) performance improvement.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出从多条执行轨迹中对比提取、评估筛选并按拓扑路由可复用技能的 LLM Agent 自进化框架。; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`e3f947b2e95c9fd008e107226c8f5a85b539b69ab57ffc8c1ed9a0b42fc2996a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
