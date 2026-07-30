---
title: "[论文解读] Living-Harness Is an Interactive-Agent Evolver"
description: "[arXiv 2607.26598][LLM Agent] 本文针对交互式大语言模型智能体会跨任务重复犯错的问题，提出让外部运行框架在每轮任务结束后依据轨迹与评估信号积累受约束的程序性修复。"
arxiv_id: "2607.26598"
announcement_date: "2026-07-30"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T07:32:04.639418+00:00"
source_sha256: "334b0a6fea336ad500b967ec9da40867b9491b33ae71f75216862c760502d3a3"
tags:
  - "LLM Agent"
  - "LLM 其他"
  - "大语言模型智能体"
  - "交互式智能体"
  - "智能体支架"
  - "跨回合适配"
  - "持久程序性修复"
  - "情节记忆"
  - "状态图"
  - "Evolution-SOP"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2607.26598</p>

# Living-Harness Is an Interactive-Agent Evolver

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Yuetian Du, Yucheng Wang, He Xu, Jiexu Xu, Shanwen Tan, Bing Zhao, Boyu Yang, Zhijie Xu, Ming Kong, Hu Wei, Jie Liu, Qiang Zhu</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26598v1) · [PDF 下载](https://arxiv.org/pdf/2607.26598v1) · **关键词** 大语言模型智能体, 交互式智能体, 智能体支架, 跨回合适配, 持久程序性修复, 情节记忆, 状态图, Evolution-SOP  


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

本文针对交互式大语言模型智能体会跨任务重复犯错的问题，提出让外部运行框架在每轮任务结束后依据轨迹与评估信号积累受约束的程序性修复。

**不用术语来说**：智能体即使在一次任务中根据反馈纠正了错误，也往往不会把纠正方式真正写入以后持续使用的操作流程。例如，它可能已经知道某种情况下应转接人工，却在后续相似任务中再次忘记调用转接工具；问题不只是“没有记住一句教训”，而是没有持久记录何时触发、应该执行什么动作以及流程下一步如何改变。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者明确提出“持久程序性修复”这一研究目标：将有评估依据的失败转化为跨回合复用的触发条件、修复动作和流程转移关系，从而区分单次重试中的纠错与面向未来任务的流程更新。
- 作者提出 Living-Harness 的 rollout–evaluate–update 思路：在冻结工具和基础上下文的边界下，由领域级 Evolution-SOP 指导更新情景记忆与状态图，使经验性教训和工作流规则能够持续积累并供后续检索。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于基于大语言模型的交互式智能体研究，场景包括任务型对话和需要调用工具的环境。此类智能体不仅生成文本，还要根据用户请求、环境反馈和既定流程选择动作，例如查询信息、调用接口或转接人工；其可靠性通常由模型外部的“智能体支架”保障，支架负责组织提示、工具、上下文、记忆、工作流及评估接口。本文关注跨回合持续改进：一次任务结束后，如何把已验证的失败原因与修复方式写入持久支架，使后续相似任务能够复用这些程序性经验，而不是再次犯同样的执行错误。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**智能体支架（agent harness）**

围绕基础模型搭建的外部运行结构，用来配置提示、工具、上下文、记忆、工作流和评估接口。它决定模型能够获得哪些信息、执行哪些动作，以及按何种程序与环境交互。

</div>
<div class="conceptitem" markdown="1">

**情节记忆（episodic memory）**

以一次具体交互经历为单位保存的经验记录。本文所需的记录不仅描述发生了什么，还包含失败的触发条件、失败模式以及对应的恢复动作。

</div>
<div class="conceptitem" markdown="1">

**状态图（state graph）**

以状态节点和状态间转换边表示工作流程的结构化知识。本文用它记录在特定状态下应增加或修改的动作、修复边及转换规则，使文字经验能够落实为可执行的流程约束。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一轮已经完成的智能体—环境交互轨迹及其评估器信号；系统还持有面向某一任务领域的 Evolution-SOP，以及由情节记忆和状态图组成的持久支架状态。任务是在每轮结束后，从轨迹与评估结果中提取有依据的失败条件、缺失动作和恢复方式，对持久状态实施范围受限的更新；后续任务再检索相关记忆和图结构，作为智能体决策的程序性上下文。其关键假设是基础模型之外存在可持久化的支架，并且跨轮适配只修改情节记忆与状态图，工具集合和基础上下文保持冻结，从而避免经验积累任意改变智能体的操作边界。输出不是对单次回答的临时修正，而是可在后续相似交互中复用的程序性修复，包括经验层面的触发条件—失败模式—恢复动作，以及工作流层面的状态—动作—转换关系。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$\tau$**

一轮已完成的智能体交互轨迹；本文将其与评估信号一起作为跨回合支架更新的证据。

</div>
<div class="notationitem" markdown="1">

**$\tau^{2}\text{-Bench}$**

论文实验所采用的交互式智能体基准之一；这里的上标 2 属于基准名称，并非本文定义的轨迹平方运算。

</div>
<div class="notationitem" markdown="1">

**$\text{Pass@1}$**

论文摘要所报告的主要成功率指标，表示首次执行即通过任务评估的表现；其具体判定细节在所给背景节选中未明确说明。

</div>
<div class="notationitem" markdown="1">

**$\text{POMDP}$**

部分可观测马尔可夫决策过程。作者以“程序状态 POMDP”视角区分单轮内的环境执行与单轮后的支架修订，但所给节选未提供其形式化状态、动作或转移定义。

</div>

</div>

**直接相关的工作**

- **Meta-Harness: End-to-End Optimization of Model Harnesses（Lee et al., 2026）**: 代表支架设计与优化方向：通过优化提示、工具约束或执行结构增强外部程序控制。本文指出，此类支架通常在部署前完成设计或优化，部署后作为固定产物复用，因而不能持续吸收新出现的失败模式与恢复动作。
- **Reflexion（Shinn et al., 2023）**: 代表反思与经验记忆方向：保留批评、总结或成功与失败轨迹以辅助后续尝试。作者认为，仅保存“应当转接人工”之类的文字教训，尚未明确何时触发、必须调用什么工具以及工作流如何转换；Living-Harness试图把这类经验进一步写成持久、可检索的程序性修复。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

任务型对话和工具调用智能体需要长期稳定地遵守操作流程，但任务结束后的反馈通常只影响当前回答或重试，不会修订后续交互所依赖的持久 harness（即围绕基础模型组织提示、工具、上下文、记忆和工作流的外部运行框架）。因此，同一种工具漏调、状态判断错误或流程转移缺失可能在后续任务中反复出现，降低部署可靠性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **Harness 设计与工作流优化**：在部署前设计或优化提示词、标准操作程序、工具约束、技能模块和执行结构，用预先规定的路径约束智能体行为，以减少越界操作或流程错误。
- **反思与经验记忆**：保存自我批评、任务摘要或成功与失败轨迹，并在重试或未来任务中将相关文本经验提供给智能体，帮助其参考过去的教训。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 预先设计或优化的 harness 通常在部署后保持静态，能够执行已有规则，却不能把运行中发现的新失败模式及其恢复方式安装为后续可用的流程修复；结果是实际部署暴露的新问题仍可能重复发生。
- 文本反思或轨迹记忆往往只表达抽象教训，例如“应当转接人工”，但没有明确绑定触发条件、必要的工具动作和工作流状态转移；此外，未经评估验证的自我反思也可能缺乏可靠依据，因而不足以稳定改变未来执行。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种跨回合、由评估证据支撑且受操作边界约束的机制，能够把已完成轨迹中的失败转化为结构化、可检索的程序性关系：失败在什么条件下出现，缺失或错误的动作与状态转移是什么，以及后来遇到相似状态时应如何恢复。该机制还需同时保存失败原因与恢复经验，以及面向执行的工作流规则，而不是只保留自由文本反馈。

</div>
<div markdown="1"><span>核心问题</span>

如何把任务结束后的失败及评估信号转化为持久的程序性修复，使智能体在未来相似交互中能够调用这些修复，同时仅更新 harness 的有状态部分，而不任意改写工具集合和基础上下文？

</div>
<div markdown="1"><span>作者直觉</span>

一次失败轨迹可以看作关于现有流程缺陷的新证据。若先由评估器确认结果，再用领域级 Evolution-SOP 限定哪些信息可写入，就能降低无依据自我修改的风险；把“为何失败、如何恢复”写入情景记忆，并把“处于何种状态、应执行何种动作或转移”写入状态图，则分别补足经验理解与可执行流程。后续任务只需检索与当前情形相关的条目，就可能复用过去的修复，而冻结工具和基础上下文则为这种持续演化设置边界。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Living-Harness 将智能体的工具、基础上下文和领域规则保持冻结，只让可持久化的“程序性状态”在任务之间演化。每个任务开始时，系统依据任务及其作用域，从情景记忆和状态图中检索相关经验，渲染成执行上下文供 LLM 智能体使用；任务结束后，评估器给出结果信号，固定的领域级 Evolution-SOP 再把完整轨迹压缩为任务目标、已验证事实、执行结果和关键失败或恢复点，提取候选修复，并在证据充分、作用域合适且不违反固定约束时写回持久状态。这里的“后验”是指先观察已经完成的交互及其评估结果，再决定是否修改未来任务可见的程序性指导，而不是在当前任务执行途中改写规则。
直观地说，该方法给静态智能体外壳加了一本会更新的“故障手册”和一张会补路的“流程图”：故障手册记录某种条件下发生了什么错误、应如何恢复，流程图记录在特定状态应采取或补充哪一步。二者只在一次任务彻底结束并经过检查后更新，因此不会用当前任务尚未得到的结果反过来影响当前轨迹，也不会修改基础模型、工具或硬编码领域规则。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 初始化并冻结执行资源

构造固定执行资源 C_d^{act}、固定更新协议 \psi_d，并初始化 S_d^{(0)}=(\emptyset,G_{d,\mathrm{scaf}})；基础模型、C_d^{act} 和 \psi_d 在后续演化中均不更新。

<div class="method-step__io" markdown="1">

**输入**：领域 d 的工具、基础上下文、领域规则，以及仅含领域根节点和任务族结构的粗粒度图骨架。  
**输出**：初始 harness H_d^{(0)}，其中情景记忆为空，状态图尚无细粒度故障修复。

</div>

**直观理解**：系统先准备不可改动的工具箱和安全规则，再放入一本空的经验册与一张只有目录结构的流程图。之后学到的只是如何更可靠地使用既有资源。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 按任务检索程序性上下文

先构造查询 q_n=Q(x_n,f_n)，分别检索记忆和图中的相关条目，再将结果渲染为执行上下文 \kappa_n；固定规则 C_d^{act} 的优先级高于检索内容。

<div class="method-step__io" markdown="1">

**输入**：当前任务 x_n、任务作用域 f_n，以及任务开始时的情景记忆 \mathcal{R}^{(n)} 和状态图 G^{(n)}。  
**输出**：仅包含当前任务相关故障模式、恢复操作和状态转移提示的上下文 \kappa_n。

</div>

**直观理解**：系统不会把所有历史记录塞给模型，而是像查手册一样，只取出与当前任务类型和范围相符的几页。这样既减少无关信息，也避免旧经验覆盖正式规则。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 执行交互并获得评估

智能体依照 p_M(\tau\mid x_n,C_d^{act},\kappa_n) 与环境交互，生成由观察、回复和工具动作组成的完整轨迹 \tau_n；终止后由评估器计算 y_n=E(x_n,\tau_n)，且整个 rollout 期间 S^{(n)} 保持不变。

<div class="method-step__io" markdown="1">

**输入**：任务 x_n、固定执行资源 C_d^{act}、检索上下文 \kappa_n 和基础模型 M。  
**输出**：已完成轨迹 \tau_n 及其执行结果信号 y_n。

</div>

**直观理解**：模型带着相关经验完成一次任务，但任务进行中不能临时改写长期手册。只有任务结束后，外部检查结果才可作为新经验的依据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 抽象轨迹并提取候选修复

后处理器生成 episode abstraction e_n，保留任务目标、已验证交互事实、执行结果及关键失败或恢复点；随后提取 u_n=(u_n^{\mathcal R},u_n^G)，分别描述记忆修复证据与图修复证据。

<div class="method-step__io" markdown="1">

**输入**：任务 x_n、轨迹 \tau_n、评估信号 y_n、固定资源 C_d^{act} 和领域级 Evolution-SOP \psi_d。  
**输出**：结构化候选修复 u_n，而非未经筛选的完整历史轨迹。

</div>

**直观理解**：这一步类似把冗长事故录像整理成事故报告：先找出真正导致成败的环节，再分别写成“何时会出错、如何补救”和“流程应在哪里增加或修改一步”。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="equation-block" markdown="1">

#### Harness 与演化状态分解

$$
H_{d}^{(n)}=\left(C_{d}^{\mathrm{act}},\psi_{d},S_{d}^{(n)}\right),\qquad S_{d}^{(n)}=\left(\mathcal{R}_{d}^{(n)},G_{d}^{(n)}\right)
$$

**符号说明**

- $H_d^{(n)}$：领域 d 在第 n 个 episode 时使用的完整智能体 harness。
- $d$：交互任务所属领域。
- $n$：跨 episode 的任务序号，也是持久状态的演化时间索引。
- $C_d^{\mathrm{act}}$：actor 可用且保持冻结的执行资源，包括工具、基础上下文和领域规则。
- $\psi_d$：固定的领域级 Evolution-SOP，规定如何解释评估结果、提取证据并审查更新。
- $S_d^{(n)}$：第 n 个 episode 开始时的可演化持久状态，在该 episode 内保持不变。
- $\mathcal{R}_d^{(n)}$：领域 d 的情景记忆，保存触发条件、失败模式和恢复动作。
- $G_d^{(n)}$：领域 d 的状态图，保存状态节点、转移规则和修复边。

<div class="equation-explanation" markdown="1">

**直观理解**：该分解明确划定了系统可以学习什么：工具、正式规则和更新规程不动，只有记忆与状态图能在任务之间改变。这样把适应限制在程序性指导层，而不是训练模型参数或自动改写工具代码。  
**原文位置**：Method，Problem Setting and Harness State，式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 评估后有界状态更新

$$
S^{(n+1)}=\operatorname{Update}_{\psi_d}\left(S^{(n)},u_n;C_d^{\mathrm{act}}\right)
$$

**符号说明**

- $S^{(n)}$：当前 episode 使用的持久 harness 状态。
- $S^{(n+1)}$：完成评估和候选审查后，供后续 episode 使用的新状态。
- $\operatorname{Update}_{\psi_d}$：由 Evolution-SOP 控制的更新算子，执行证据、作用域和约束一致性检查并决定是否提交。
- $\psi_d$：领域 d 的固定更新协议。
- $u_n$：由第 n 个 episode 抽象提取出的候选修复证据，包含记忆证据 u_n^{\mathcal R} 和图证据 u_n^G。
- $C_d^{\mathrm{act}}$：作为不可违反的参照条件传入更新过程的固定工具、基础上下文和领域规则。
- $n$：当前已完成并经过评估的 episode 索引。

<div class="equation-explanation" markdown="1">

**直观理解**：该式是持久演化的核心：一次任务产生的修复建议不会直接生效，而要在固定规则约束下由 SOP 审核。若证据不足或发生冲突，更新算子使状态保持不变；若通过，经验才进入下一次任务可检索的长期状态。  
**原文位置**：Method，Rollout–Evaluate–Update Loop，式 (9)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用传统的参数训练目标。原文方法不更新基础模型参数，也未给出通过梯度最小化的损失函数；其优化方式是基于已完成轨迹和评估信号进行离散、受约束的持久状态更新。成功或失败信号用于支持或拒绝候选程序性修复，而不是反向传播到模型、工具或基础上下文，因此这里更准确地称为跨 episode 的 harness 演化，而非模型训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双组件持久状态**

演化状态 S_d^{(n)}=(\mathcal{R}_d^{(n)},G_d^{(n)}) 由情景记忆与状态图组成。\mathcal{R} 保存带作用域的触发条件、失败模式和恢复动作，G 保存状态节点、转移规则以及把观测条件连接到缺失或修订动作的修复边；前者表达修复“为何及何时有用”，后者表达修复“在流程何处改变动作”。

> 直观理解：只保存文字经验容易知道问题却不知道该插入流程的哪一步，只保存流程边又可能丢失适用条件。记忆与图联合使用，使系统同时记住事故语境和可执行的流程修改。

**2. Evolution-SOP**

Evolution-SOP \psi_d 是固定的领域级更新协议，不属于 actor 的任务执行提示。各领域共享 posterior–extract–commit 总流程，但 \psi_d 提供领域特定的失败解释、更新作用域划分以及领域规则和工具约束检查；它将评估后的轨迹转成候选证据，并通过有界门控决定是否提交。

> 直观理解：它相当于维护手册的审核规程，而不是完成业务任务的现场指令。其作用是防止一次偶然失败、错误归因或越界建议直接污染以后所有任务。

**3. 任务条件化检索与渲染**

系统根据任务 x_n 和作用域 f_n 生成查询，独立检索 \mathcal R^{(n)} 与 G^{(n)}，再将命中条目组织为 actor 可读的程序性上下文 \kappa_n。该机制是对持久状态的选择性投影，不重放全部历史，并明确让固定规则 C_d^{act} 保持更高优先级。

> 直观理解：长期状态可以不断增长，但当前模型只看到最相关的一小部分。这样既控制上下文负担，也降低不相关经验误导当前决策的风险。

**训练与推理**

演化阶段与部署推理使用同一闭环。对第 n 个任务，先从固定于该 episode 的 S^{(n)} 中检索相关记忆和图结构，渲染为 \kappa_n，随后基础模型在 x_n、C_d^{act} 和 \kappa_n 条件下执行交互；任务结束后，评估器生成 y_n，Evolution-SOP 将 (x_n,\tau_n,y_n,C_d^{act}) 压缩为 episode abstraction，再提取并审查 u_n，最后生成 S^{(n+1)}。若任务本身允许重试，失败尝试还可以形成仅供当前任务使用的局部反思，但该反馈在任务实例结束时丢弃；只有经过评估和门控后写入情景记忆或状态图的修复才属于持久演化。
纯推理或迁移复用时，无须重新训练模型，也可以只读取已经演化好的状态：针对新任务执行查询、检索、渲染和 rollout 即可。原文摘要称该状态支持跨模型骨干的 retrieval-only reuse，但所给方法节选未明确说明跨骨干时的序列化格式、兼容性处理或额外校准步骤，因此不能据此推断具体迁移实现。

**复现信息**

公平解释该方法所需的关键约束有四点：第一，状态以 episode 为更新边界，当前 rollout 内不得改变；第二，actor 的工具、基础上下文、领域规则和基础模型均冻结，演化对象仅为情景记忆与状态图；第三，检索采用任务及作用域条件化的选择性投影，而非直接拼接完整历史，且固定规则优先于检索经验；第四，写回前必须检查证据支持、任务作用域和固定约束一致性，无合格候选时状态不变。初始状态为无情景记忆加粗粒度领域图骨架。所给原文未明确报告检索器类型、相似度函数、召回条数、图数据库或记忆存储格式、SOP 的完整提示模板、更新阈值、评估器具体实现及候选冲突消解细则，这些均需要结合论文其余部分或代码进行源核查。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- τ²-Bench：面向对话智能体的真实多轮交互基准，包含策略约束和可执行工具调用。实验使用 Retail、Airline、Telecom 三个领域，用于检验复杂业务规则下的持续程序修复。原文未明确报告本实验使用的样本规模与具体数据划分。
- MultiWOZ-2.4：经过纠正的多领域任务型对话基准。实验使用 Restaurant、Hotel、Train、Attraction、Taxi 五个主要领域，用于检验修复知识在不同任务领域及跨领域组合中的迁移。原文未明确报告本实验使用的样本规模与具体数据划分。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**Pass@1（任务成功率）**

衡量智能体在被计分的一次任务执行中是否完成目标；论文将其作为两个基准的主要指标。协议允许任务局部重试时，报告分数仍遵循论文规定的任务级评估流程。 （越高越好，因为更高数值表示更大比例的交互任务满足基准成功条件。）

</div>
<div class="metricitem" markdown="1">

**相邻演化周期的 Pass@1 绝对变化**

Table 2 括号中的数值表示当前周期相对前一周期的百分点变化，用于观察持久 harness 在在线更新后是否持续改善，以及是否出现回落。 （通常正值且越大表示该周期带来的增益越强；负值表示波动或退化，但不能单独说明长期累计效果。）

</div>
<div class="metricitem" markdown="1">

**组件移除后的平均 Pass@1**

比较完整系统与移除 Evolution-SOP、情景记忆或状态图后的平均任务成功率，以估计各组件对最终效果的贡献。 （越高越好；消融后下降越大，说明被移除组件与整体性能的关联越强，但不等同于严格的独立因果效应。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 两个基准上的总体 Pass@1，与旗舰模型及 GPT-5.2 交互基线比较

<div class="result-value" markdown="1">

Living-Harness 在 τ²-Bench 和 MultiWOZ-2.4 上的平均 Pass@1 分别为 83.09 和 65.50。τ²-Bench 上，它比最强交互基线 Reflexion 的 73.02 高 10.07 个百分点，并略高于旗舰模型 Gemini 3 Pro 的 82.92；MultiWOZ-2.4 上，它比最强交互基线 ReasoningBank 的 55.59 高 9.91 个百分点，比 Reflexion 高 12.40 个百分点。

</div>

结果支持持久化、受约束的程序修复能在相同 GPT-5.2 骨干条件下超过任务内反思和一般记忆方法，而不仅是依赖更强的单步推理。MultiWOZ 的两领域、三领域任务表现尤其好，也与跨领域复用程序知识的设计目标一致。不过，这些结果只覆盖八个选定领域，且无法证明对所有交互环境或其他评估器同样有效。

<div class="result-source" markdown="1">

来源：Main Results，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Table 1 shows that Living-Harness achieves the best overall performance on both benchmarks, reaching 83.09 average Pass@1 on τ²-Bench and 65.50 on MultiWOZ-2.4.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Cycle 0 至 Cycle 3 的在线自演化动态

<div class="result-value" markdown="1">

τ²-Bench 中，Retail 从 57.02 提升到 85.96，Telecom 从 57.39 提升到 78.07；Airline 在 Cycle 2 达到 88.00，Cycle 3 略回落到 86.00。MultiWOZ-2.4 最终周期相对 Cycle 0 的增益依次为 Restaurant +13.96、Hotel +24.11、Train +22.83、Attraction +25.25、Taxi +28.71。多数最大增益发生在首个演化周期，之后以较小修正和偶发波动为主。

</div>

这说明从早期失败中写入的程序修复可以供后续任务使用，而不是只帮助当前重试；首周期的大幅提升符合“先补齐缺失关键步骤、再逐步细化”的解释。Airline、Restaurant 等领域出现周期性回落，表明状态持续增长并不保证每轮单调变好，也提示噪声更新或检索干扰仍可能存在。

<div class="result-source" markdown="1">

来源：Main Results，Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">On τ²-Bench, all three domains improve substantially over Cycle 0: Retail rises from 57.02 to 85.96, Telecom from 57.39 to 78.07, and Airline reaches 88.00 at Cycle 2 before remaining high at 86.00 in Cycle 3.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 将 GPT-5.2 演化出的冻结 harness 状态，以仅检索方式迁移到 Gemini 3 Pro、GLM-5、Qwen3-max 和 Kimi-k2

<div class="result-value" markdown="1">

冻结状态提升了四种目标骨干在五个 MultiWOZ-2.4 领域中的每个已报告分数。Taxi 上，GLM-5 从 0.00 升至 43.08，Qwen3-max 从 0.00 升至 45.13，Kimi-k2 从 0.00 升至 45.13；较强的 Gemini 3 Pro 也由 Restaurant 47.83、Hotel 45.18、Train 55.35、Attraction 63.64、Taxi 30.26，分别提升至 66.13、63.71、66.87、66.67、68.72。

</div>

目标模型没有继续写入全局状态，因此提升表明记忆和状态图包含能被不同 actor 利用的可检索程序知识，而不只是 GPT-5.2 参数内部的适配。该实验仍不是完全独立来源上的迁移：目标任务仍属于 MultiWOZ-2.4 的相同五个领域，因而不能证明对全新环境、工具集合或政策体系也能直接迁移。

<div class="result-source" markdown="1">

来源：In-depth Analysis：Harness transfer，Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">The gains are especially large in domains where the base model struggles, such as Taxi, where GLM-5, Qwen3-max, and Kimi-k2 improve from 0.00 to 43.08, 45.13, and 45.13, respectively.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验覆盖 τ²-Bench 的三个领域和 MultiWOZ-2.4 的五个领域，原文未明确报告所用样本规模、数据划分及统计置信区间，也未提供多随机种子方差或显著性检验。因此，约 10 个百分点的平均提升具有实际意义，但其抽样稳定性和对其他交互环境、工具体系及真实用户的外推性仍需验证。
- 作者明确指出提交门控“do not provide full rollback or regression testing”。同时，Table 2 出现个别周期回落，Tables 4–5 显示持久状态持续扩张；论文尚未充分检验长期运行中的错误知识累积、检索延迟与上下文成本、状态污染，以及自动回滚或回归测试能否控制这些风险。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 旗舰模型组，包括 GPT-5.2、Gemini 3 Pro、GLM-5、Qwen3-max 和 Kimi-k2；它们不进行在线 harness 演化，用于区分 Living-Harness 的提升究竟来自持久程序状态，还是仅来自骨干模型本身的能力。跨模型迁移实验还把其中若干模型作为冻结 harness 的目标骨干。
- ReAct：标准“推理—行动”循环基线，在相同工具与交互预算下测试仅靠即时推理和工具操作能达到的水平，不维护本文所定义的演化式持久 harness。
- Reflexion：允许每个任务至多三次尝试的任务内反思基线，是检验“失败后临时总结并重试”与“把修复写入跨任务持久状态”差异的关键比较对象；局部反思缓冲区在任务结束后被丢弃。
- 记忆与自改进方法组，包括 Agent Workflow Memory、ReasoningBank 和 EvoTest；其中记忆型基线在相同上下文预算下向 actor 注入检索内容，用于比较一般经验记忆或自改进机制与本文受门控、双表示的程序状态演化。

**实验想回答的问题**

- 在相同骨干模型、工具接口、评估器与重试预算下，把已完成轨迹及评估信号转化为可持续更新的情景记忆和状态图，是否比任务内反思、一般记忆或推理—行动方法带来更高的交互任务一次成功率？
- 性能提升是否确实来自受 Evolution-SOP 约束的持久化程序修复，并能随演化周期累积、跨领域及跨模型复用，而不是仅由更强骨干模型、更多上下文或当前任务内重试造成？

**实验实现**

所有基于 GPT-5.2 的交互方法均采用 GPT-5.2 medium reasoning effort；Living-Harness 的 actor 与全部演化模块共享该骨干。τ²-Bench 的模拟用户由 GPT-5.1 实现。采样温度为 0.2，top_p=1.0；记忆和状态图分别检索 top-k=3，并优先检索同一任务家族。适用时，各交互基线共享工具接口、评估器和任务级重试预算；Living-Harness 与 Reflexion 均允许每个任务至多三次局部尝试，但局部反思不会直接写入全局记忆或状态图。
评估采用“先计分、后更新”：第 n 个 episode 只能使用其开始前已有的 harness 状态，轨迹完成并由基准计分后，系统才能从该轨迹提出并提交全局更新，因此当前 episode 的证据不能反过来改善自身分数。τ²-Bench 每个已计分 episode 后更新，MultiWOZ-2.4 每四个已计分 episode 同步一次。更新须通过 schema、scope、evidence、constraint 和 merge 五类门控。跨模型实验只允许目标骨干从由 GPT-5.2 演化并冻结的记忆与状态图中检索，不允许继续全局更新。所有推理通过远程兼容 OpenAI 的 API 完成，供应商侧硬件与服务软件信息不可得。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除 Evolution-SOP：保留记忆和状态图容器，但用通用抽取器替代领域更新流程，并禁用领域特定提交门控和任务家族范围规则 | τ²-Bench 平均 Pass@1 从完整系统的 83.09 降至 73.38，下降 9.71 个百分点，是所有组件消融中最大跌幅。 | 该消融主要隔离“如何解释失败并约束持久更新”的作用。大幅下降说明仅设置记忆库和工作流图并不足够，领域化的证据归因、提交门控及范围控制与性能密切相关。但该变体同时改变了抽取器和多类门控，无法进一步判断究竟哪一道门控贡献最大。 | Ablation Studies：Component ablation，Figure 3<br><span class="experiment-evidence">Removing the Evolution-SOP causes the largest drop, reducing the average score from 83.09 to 73.38, suggesting that the gain is not due to attaching memory or a workflow graph alone, but from structured posterior interpretation and bounded state evolution.</span> |
| 分别移除情景记忆或状态图：前者禁用记忆检索与更新，后者禁用图检索与更新 | 移除情景记忆后平均 Pass@1 为 77.34，比完整系统低 5.75 个百分点；移除状态图后为 79.50，低 3.59 个百分点。完整系统在每个领域均取得最佳结果。 | 情景记忆保存“触发条件—失败模式—恢复动作”式经验，状态图保存状态条件下的流程转移和修复边；两种消融都退化，支持二者互补，而不是完全重复。记忆消融下降更大并不等于记忆在所有场景中必然更重要，因为两个组件的容量、检索形式和信息粒度不同，不能仅凭跌幅作严格横向因果比较。 | Ablation Studies：Component ablation，Figure 3<br><span class="experiment-evidence">Removing memory or the state graph also degrades performance, with average scores of 77.34 and 79.50, respectively, indicating that reusable recovery lessons and structured workflow transitions provide complementary benefits.</span> |

**定性案例**

- Figure 4 展示了“识别教训”与“执行修复”的差异：Cycle 0 中，Reflexion 已多次认识到应把用户转接给人工客服，却始终遗漏必需的 transfer_to_human_agents() 工具调用。Living-Harness 在评估后将该失败同时写成情景记忆条目和状态图修复边，把“检测到终止性暂停状态”连接到具体工具动作；Cycle 1 检索该修复后一次完成任务。该案例直观说明状态条件化、可执行的程序修复可能优于模糊的自然语言反思，但它只是单个定性案例，不能单独证明普遍效果。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出可从历史轨迹和评估反馈中持续更新记忆与状态图的自演化 LLM Agent harness。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`334b0a6fea336ad500b967ec9da40867b9491b33ae71f75216862c760502d3a3`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
