---
title: "[论文解读] Second Thought: Reasoning in Parallel as LLM Agents Act and Observe"
description: "[arXiv 2608.13667][LLM Agent] 本文指出 ReAct 智能体在执行动作并等待环境返回结果时存在反复出现的“推理空闲窗口”，并提出无需训练的 Second Thought，在这些窗口中并行生成可中断、互补的辅助思考，供下一轮决策使用。"
arxiv_id: "2608.13667"
announcement_date: "2026-08-17"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-17T02:01:05.284230+00:00"
source_sha256: "2b18a596586fa282e384ab91699d59df3cccbdf56341138312de4acffe57a0c7"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "大语言模型智能体"
  - "ReAct"
  - "推理空闲窗口"
  - "并行推理"
  - "推理时计算"
  - "智能体延迟"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.13667</p>

# Second Thought: Reasoning in Parallel as LLM Agents Act and Observe

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-17</span>
<span><strong>作者</strong> Zhensu Sun, Chengran Yang, Yunbo Lyu, Jieke Shi, David Lo</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Singapore Management University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13667) · [PDF 下载](https://arxiv.org/pdf/2608.13667) · **关键词** 大语言模型智能体, ReAct, 推理空闲窗口, 并行推理, 推理时计算, 智能体延迟<br>
**代码**: [https://anonymous.4open.science/r/2nd-thought](https://anonymous.4open.science/r/2nd-thought)

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

本文指出 ReAct 智能体在执行动作并等待环境返回结果时存在反复出现的“推理空闲窗口”，并提出无需训练的 Second Thought，在这些窗口中并行生成可中断、互补的辅助思考，供下一轮决策使用。

**不用术语来说**：现有智能体想得越久，通常越可能解决复杂任务，但用户也必须等待更久；与此同时，智能体调用工具后往往只是等待执行结果，没有利用这段时间继续思考。问题在于，如何把原本浪费的等待时间转化为有效思考，又不延长主流程，并保证环境结果随时返回时，已经产生的内容仍然可用。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者识别并形式化了 ReAct 式智能体中的“推理空闲窗口”：每轮 Thought 结束后，Action 执行及 Observation 返回前没有生成推理，因此这段外部等待时间构成尚未利用的并行计算机会。
- 作者提出无需训练的 Second Thought：在空闲窗口内并发运行 Check、Recall、Rehearse 和 Alternative 四类互补分支，并以相互独立的原子思考流式输出；环境观察到达后，系统收集已完成内容并拼接到工具消息末尾，使下一轮主推理可以直接利用。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究基于大语言模型的自主智能体。此类智能体通常采用 ReAct 范式，将多步交互组织为“思考（Thought）→行动（Action）→观察（Observation）”循环：模型先根据已有轨迹形成计划并生成工具调用，外部环境执行该调用并返回结果，模型再据此继续推理。推理时计算扩展通常通过生成更多思考文本提高求解能力，但这些额外 token 位于任务的串行关键路径上，会直接增加交互延迟。本文关注其中尚未利用的并行机会：思考结束后，智能体在序列化行动及等待环境响应期间不再进行实质推理，作者将这一反复出现的 Action–Observation 时间段称为“推理空闲窗口”。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**ReAct 范式**

一种让语言模型交替进行文本推理、调用外部工具和读取执行结果的智能体框架。每轮的新思考以此前轨迹和最新观察为条件，使智能体能够根据环境反馈修正计划。

</div>
<div class="concept-item" markdown="1">

**推理时计算扩展**

在不重新训练模型的情况下，投入更多生成或搜索计算来改善任务表现，例如延长推理链或并行采样多个候选思路。若新增计算位于主线程上，生成量增加通常也会延长用户实际等待时间。

</div>
<div class="concept-item" markdown="1">

**串行关键路径**

完成任务前必须按顺序执行、无法被其他并行工作隐藏的操作链。本文中特别指主智能体逐轮生成 Thought、Action 并等待 Observation 的路径，其解码耗时直接影响端到端延迟。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个需要多轮工具交互才能完成的任务，以及截至当前轮的智能体轨迹，包括先前的 Thought、Action 和 Observation；运行环境可以是代码仓库、命令行系统或多轮工具调用场景。基本假设是每轮 Thought 一旦结束，当前 Action 已经确定，因此 Action–Observation 窗口内启动的辅助推理不能改变本轮决策，只能以既有轨迹为条件，为后续轮次准备补充信息；同时，外部 Observation 的返回构成不可预知的硬截止点，辅助生成可能随时被中断。目标是在不训练模型、尽量不增加主线程串行解码的条件下利用该窗口，并在 Observation 到达时输出仍可使用的辅助思考，将其并入轨迹供下一轮推理使用，从而改善任务成功率、交互轮数与延迟之间的权衡。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$T_t$**

第 $t$ 轮的 Thought，即智能体依据当前轨迹生成的推理与计划；该符号为便于说明问题设置所作的概括，原文节选未给出正式符号。

</div>
<div class="notation-item" markdown="1">

**$A_t$**

第 $t$ 轮由 Thought 确定并提交给工具或环境的 Action；原文节选未给出正式符号。

</div>
<div class="notation-item" markdown="1">

**$O_t$**

环境执行 $A_t$ 后返回的 Observation，它触发下一轮推理；原文节选未给出正式符号。

</div>
<div class="notation-item" markdown="1">

**$W_t$**

第 $t$ 轮从 Thought 结束到 Observation 到达之间的推理空闲窗口，即辅助推理可与行动执行和环境等待并行运行的时间段；原文节选未给出正式符号。

</div>

</div>

**直接相关的工作**

- **Self-Consistency**: 该方法在 Thought 阶段并行采样多条候选推理链，再通过一致性选择答案，用于扩大推理搜索空间。本文研究的并行维度不同：辅助推理在当前 Thought 已结束、Action 已确定后才启动，因此不是竞争本轮决策的候选分支，而是服务后续轮次的互补思考。
- **Tree of Thoughts**: 该方法把思考过程组织为树状搜索，在 Thought 阶段探索和评估多个推理分支。本文指出这种横向候选搜索不能直接处理 Action–Observation 窗口，因为窗口受 Observation 到达这一外部截止点约束，所生成内容必须允许中途停止，并且不能再修改当前 Action。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

LLM 智能体依靠更长的推理轨迹提升复杂多步任务的正确率，但新增推理 token 位于关键执行路径上，会近似按比例增加墙钟延迟，因而不适合强调响应速度的交互式软件工程、终端操作和工具调用任务。ReAct 工作流又在每轮动作执行与环境响应之间反复等待，形成有计算资源却没有继续推理的时间段。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **延长主线程推理的测试时计算扩展**：在 Thought 阶段生成更多推理 token，让模型进行更充分的规划、检查和修正，以计算量换取任务准确率。
- **Thought 阶段的横向并行搜索**：Self-Consistency、Tree-of-Thought 以及群体选择或跨分支共享方法，会在作出动作前并行采样多条候选推理链，再通过投票、搜索、选择或信息聚合确定当前决策。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 延长主线程推理会把所有新增 token 都放在关键路径上，准确率提升直接伴随更长的顺序解码和用户等待时间，未利用工具执行期间本来就存在的等待窗口。
- 横向并行方法面向当前 Thought 内的候选决策竞争，而空闲窗口开始时当前动作已经确定并正在执行，新增分支无法再改变本轮动作；此外，环境观察可能随时返回并强制终止生成，普通分支若在中途被截断，可能留下不完整且难以复用的结果。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有方法缺少一种专门适配 Action–Observation 间隔的推理机制：它既要以已确定的轨迹为条件，为未来轮次提供互补信息，而不是重新竞争当前动作；又要能在外部截止时间不可预测的情况下被随时中断，并保留截至中断前已经完成的有效内容。

</div>
<div markdown="1"><span>核心问题</span>

能否利用 ReAct 智能体每轮动作执行和观察等待期间的空闲时间开展额外并行推理，使这些推理补充既有轨迹并改善后续决策，同时不增加主线程的顺序推理延迟？

</div>
<div markdown="1"><span>作者直觉</span>

工具运行时，主智能体虽然暂时不能依据尚未返回的观察修改当前动作，却可以提前完成与未来决策有关的准备工作，例如核查当前计划的假设、回忆早先约束、预演下一步以及准备失败后的替代方案。这些视角彼此补充而非互相竞争，因此无需投票，只需把已完成内容拼接给下一轮；再把输出拆成各自完整的“原子思考”，即使观察突然到达，也只会丢失正在生成的那一小段，其余内容仍可直接使用。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Second Thought 将标准的 ReAct 智能体作为主线程：在第 $t$ 轮根据轨迹历史 $H_t$ 生成思考 $R_t$，再序列化动作 $A_t$ 并等待环境返回观察 $O_t$。其核心不是改变主线程的决策顺序，而是在动作序列化和环境执行所形成的推理空闲窗口 $W_t$ 内并行运行辅助推理分支，并在观察到达后截断、筛选和合并已完成的推理单元，使下一轮思考能够利用这些信息，同时不增加主线程关键路径上的推理令牌。直观地说，主线程在等待工具结果时，几个副线程提前检查假设、回忆上下文、准备后续反应并寻找替代策略；工具结果返回后，只保留已经完整写完的有效片段。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 主线程生成思考与动作

主线程首先生成显式思考 $R_t$，评估当前状态并规划下一步；随后将计划序列化为可执行动作 $A_t$，例如结构化工具调用。

<div class="method-step__io" markdown="1">

**输入**：当前轨迹历史 $H_t$，包括此前各轮的思考、动作和观察。<br>
**输出**：已生成的思考 $R_t$ 和待执行动作 $A_t$，以及进入动作与观察阶段的时刻。

</div>

**直观理解**：这是普通 ReAct 流程中的主决策过程：模型先想清楚要做什么，再把计划翻译成工具能够执行的格式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在推理空闲窗口分叉

在主线程结束 Thought 阶段、进入 $W_t$ 的瞬间执行 fork，复制共享的上下文前缀，并启动四个异步分支：Check、Recall、Rehearse 和 Alternative。各分支在主线程序列化 $A_t$ 和等待 $O_t$ 的同时并行解码，并关闭模型原生的隐藏思考以快速产生显式辅助思考。

<div class="method-step__io" markdown="1">

**输入**：完整历史 $H_t$、新生成的思考 $R_t$，以及动作执行期间形成的窗口 $W_t$。<br>
**输出**：四个分支分别生成的原子思考流；它们可能因观察到达而在任意位置被中断。

</div>

**直观理解**：主线程在等待工具时并不空闲：四个助手使用同一份任务记录，同时从不同角度补充分析。由于等待时间不固定，助手必须边生成边产出可独立使用的小结论。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成原子思考

每个辅助输出由带有显式 XML 边界的原子思考组成，每个单元只表达一个自包含的局部洞见，长度不超过 $25$ 个单词，并避免依赖同一流中的其他单元。

<div class="method-step__io" markdown="1">

**输入**：每个分支的共享对话快照和对应的分支指令。<br>
**输出**：形如 `<thought>...</thought>` 的连续思考单元流。

</div>

**直观理解**：每条辅助意见都像一张独立便签，而不是一段必须从头读到尾的长文章；即使生成被突然停止，已经封闭的便签仍然可读。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 观察到达后的合并与截断

执行 merge，立即取消所有仍在生成的分支；每个缓冲区截断到最后一个完整的 `</thought>` 标签，丢弃未完成单元，并将每个维度最多保留 $5$ 个原子思考。没有完成任何单元的分支被省略，剩余内容追加到工具观察消息末尾。

<div class="method-step__io" markdown="1">

**输入**：环境执行 $A_t$ 后返回的观察 $O_t$，以及四个分支当前的输出缓冲区。<br>
**输出**：包含 $R_t$、$A_t$、$O_t$ 和辅助思考的更新历史 $H_{t+1}$，供下一轮 Thought 阶段使用。

</div>

**直观理解**：工具一返回，系统马上停止助手并清理半成品，只把完整便签贴到观察结果后面；如果助手没有来得及写出任何便签，系统就退化为普通 ReAct。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### ReAct 历史更新

$$
H_{t+1}=H_t\cup\{R_t,A_t,O_t\}
$$

**符号说明**

- $H_t$：第 $t$ 轮开始时的轨迹历史，包含此前各轮的思考、动作和观察。
- $R_t$：第 $t$ 轮主线程生成的显式思考或行动计划。
- $A_t$：根据 $R_t$ 序列化出的可执行动作或工具调用。
- $O_t$：环境执行 $A_t$ 后返回的观察或反馈。

<div class="equation-explanation" markdown="1">

**直观理解**：该式说明每轮结束后，主线程会把本轮思考、动作和环境反馈加入历史，形成下一轮的条件。Second Thought 在此基础上还会把已收获的辅助思考追加到观察消息中，但不会改变主线程的基本状态转移。<br>
**原文位置**：Method, Preliminaries: The Reasoning Idle Window

</div>

</div>

<div class="equation-block" markdown="1">

#### 推理空闲窗口与总轮次延迟

$$
\tau_t=\tau_t^{\mathrm{think}}+\tau_t^{\mathrm{act}}+\tau_t^{\mathrm{obs}},\qquad W_t=\tau_t^{\mathrm{act}}+\tau_t^{\mathrm{obs}}
$$

**符号说明**

- $\tau_t$：第 $t$ 轮从思考开始到观察结束的总墙钟延迟。
- $\tau_t^{\mathrm{think}}$：主线程 Thought 阶段的墙钟耗时。
- $\tau_t^{\mathrm{act}}$：动作序列化或提交执行阶段的墙钟耗时。
- $\tau_t^{\mathrm{obs}}$：环境执行动作并返回观察阶段的墙钟耗时。
- $W_t$：动作和观察阶段合计形成的推理空闲窗口。

<div class="equation-explanation" markdown="1">

**直观理解**：第一式分解一轮需要等待的时间，第二式指出 Second Thought 可以利用的时间范围。辅助分支必须在 $W_t$ 结束前尽可能输出完整思考，因此它们不会要求主线程额外等待。<br>
**原文位置**：Method, Preliminaries: The Reasoning Idle Window

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告 Second Thought 的参数训练目标、损失函数或额外微调过程。方法描述的是推理时系统：使用同一个模型在主线程和辅助分支上继续生成，并通过分支指令控制四种推理维度；因此不能据此推断存在新的训练目标或需要优化的辅助模块参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 推理空闲窗口并行调度**

每轮总延迟为 $\tau_t=\tau_t^{\mathrm{think}}+\tau_t^{\mathrm{act}}+\tau_t^{\mathrm{obs}}$，其中动作与观察阶段构成 $W_t=\tau_t^{\mathrm{act}}+\tau_t^{\mathrm{obs}}$。辅助分支只在 $W_t$ 内运行，因此其解码不被加入主线程关键路径；观察 $O_t$ 到达时统一取消在途生成。

> 直观理解：系统把主线程等待工具的时间当作额外计算预算。等待越久，助手可能完成的思考越多，但等待结束不会被助手拖慢。

**2. 四维互补推理分支**

参考配置沿时间方向和作用范围两个轴组织四个分支：Check 回溯检查当前 $R_t$ 的未经验证假设，Recall 从 $H_t$ 恢复可能被忽略的历史约束，Rehearse 为可能的工具结果预先生成条件化后续步骤，Alternative 为当前目标提出带触发条件的替代策略。分支集合可按任务、领域或计算预算裁剪、扩展或定制。

> 直观理解：四个助手分别负责“检查现在的想法”“记住过去的重要信息”“提前准备工具异常时怎么办”和“不要只押注一个方案”，目的是补足主线程容易遗漏的角度，而不是重复主线程原有思路。

**3. 原子思考收获协议**

每个单元使用 `<thought>...</thought>` 明确分隔，单元长度不超过 $25$ 个单词且不引用同流中的其他单元。合并时只保留完整闭合单元，并按每个维度最多 $5$ 个单元限制上下文增长；共享主线程前缀的 KV cache，以减少重复前缀处理。

> 直观理解：该协议解决了异步生成最关键的工程问题：系统可以在任意时刻硬停止分支，而不会把半句话或依赖上下文的残片注入下一轮。

**训练与推理**

该方法的完整流程发生在推理阶段。输入是任务及当前历史 $H_t$；主线程生成 $R_t$ 和 $A_t$ 后，在 $W_t$ 开始时复制包含 $H_t$ 与 $R_t$ 的上下文快照，异步启动四个分支；分支流式生成原子思考，主线程同时执行动作并等待 $O_t$。观察到达后，系统取消所有在途分支，保留每个分支最后一个完整闭合标签之前的内容，并将每个维度最多 $5$ 个单元追加到观察消息；下一轮模型据此生成新的主线程思考。若窗口太短导致所有分支均无完整输出，更新过程等价于基线 ReAct。

**复现信息**

复现或公平解读结果所需的关键约束包括：四个分支共享截至 $R_t$ 的提示前缀并复用 KV cache；分支输出采用显式 `<thought>` 标签，每个原子思考不超过 $25$ 个单词且不得依赖其他单元；观察到达后立即取消生成，只保留完整单元，每个维度最多保留 $5$ 个。分支可按部署需求减少或扩展，原文特别报告了保留单个表现最佳的 Alternative 分支的成本设置；除此之外，原文未明确报告训练配置、具体并发运行时、模型参数或分支指令的完整文本。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- SWE-Bench-Pro：仓库级软件工程基准。每个样本把代理置于独立 Docker 容器中，要求定位并修复真实缺陷，以隐藏的 fail-to-pass 测试判定是否成功。实验从中随机抽取 150 个样本，并将每个样本限制为最多 100 轮；它主要检验长程代码理解、工具操作和修复规划能力。
- Terminal-Bench 2.1：包含 89 个容器化终端操作任务，覆盖系统管理、数据处理和软件构建等场景，由每项任务专属的验证脚本评分；它用于检验代理在开放式命令行环境中的规划、执行与纠错能力。
- $\tau^3$-bench 银行业子集：包含 97 个多轮客服任务。代理一边与 LLM 模拟用户对话，一边调用函数，并须依据从非结构化语料中检索到的政策文档作答；它用于检验知识检索、政策遵循和多轮交互，而不只是操作规划。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Pass@1**

每个任务仅运行一次时成功完成的比例；在不同基准中，成功分别由隐藏测试、任务验证脚本或基准评分机制判定。 （越高越好，因为它直接反映代理单次执行的任务完成可靠性。）

</div>
<div class="metric-item" markdown="1">

**$\#OUT_{\mathrm{main}}$**

主线程生成的输出 token 数，只衡量位于代理执行关键路径上的解码量，而不是简单汇总所有并行分支 token。 （在 Pass@1 不降低的前提下越低越好，因为主线程解码通常直接影响等待时间与推理成本；单独降低该指标并不代表任务质量更高。）

</div>
<div class="metric-item" markdown="1">

**#Turns**

主线程完成任务所经历的代理交互轮数，通常每轮包括推理、动作或工具调用以及环境反馈。 （在任务成功率相当时越低越好，因为更少轮次意味着更短的交互链和更少的工具执行开销。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 九个“基准—模型”组合的总体效率与准确率

<div class="result-value" markdown="1">

Second Thought 在全部 9 个组合中都减少了平均轮数，在其中 6 个组合中减少主线程解码量；这些组合的平均降幅约为 20%，最大降幅为 43%。Pass@1 在 8 个组合中保持或提高，唯一下降是 SWE-Bench-Pro 上 Qwen3.6-Plus 从 52.0% 降至 51.3%，对应 150 个样本中的 1 个且不显著。

</div>

结果支持该方法通常能把部分后续推理提前放入并行分支，从而减少关键路径上的生成和交互，同时大体维持任务成功率。不过，这只是跨 3 个基准和 3 个模型的经验结果；唯一的小幅退化虽不显著，也说明该方法并非保证逐设置提升。

<div class="result-source" markdown="1">

来源：Main Results，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Second Thought reduces the average turn count in all nine pairs, and reduces main-thread decoding in six of them by up to 43% (from 36.5k to 20.8k tokens on SWE-Bench Pro with Qwen3.6-Plus) and by roughly 20% on average among those settings. Pass@1 is preserved or improved in eight; the single decrease (from 52.0% to 51.3% on SWE-Bench Pro with Qwen3.6-Plus) amounts to one instance out of 150 and is not statistically significant, whereas the largest gain (+12.4 points on Terminal-Bench 2.1 with Qwen3.6-Plus) is.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Terminal-Bench 2.1，Qwen3.6-Plus：与 base 和计算量匹配的 $s1$ 比较

<div class="result-value" markdown="1">

Second Thought 的 Pass@1 为 51.7%，相对 base 的 39.3% 提高 12.4 个百分点，相对 $s1$ 的 46.1% 提高 5.6 个百分点；主线程输出为 31,396 tokens，少于 $s1$ 的 40,642，轮数为 24.0，也低于 base 的 25.5。

</div>

这是最强的准确率增益，且显著性标记表明 Pass@1 提升不是表中随机波动的普通表现。由于 $s1$ 使用相当的额外推理预算，该比较说明收益不能仅用“多生成了一些推理 token”解释，并行分支的内容与时机可能更关键。但 ours 的主线程 token 高于 base 的 25,158，因此该设置体现的是用更多关键路径解码换取大幅准确率提升，而不是同时优于 base 的所有成本指标。

<div class="result-source" markdown="1">

来源：Main Results，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On tasks where extended reasoning improves accuracy (e.g., Terminal-Bench 2.1 with Qwen3.6-Plus), Second Thought delivers even superior Pass@1 gains (+12.4 points, +5.6 over s1) while decoding 1.3× fewer main-thread tokens than s1 (31,396 vs. 40,642) and taking fewer turns than the baseline agent (24.0 vs. 25.5).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 受控延迟复现实验：SWE-Bench-Pro，DeepSeek-V4-Flash

<div class="result-value" markdown="1">

Second Thought 将每任务墙钟时间中位数从 256.9 秒降至 229.0 秒，下降 10.9%；其中主线程解码时间从 168.7 秒降至 146.1 秒，工具执行时间从 71.6 秒降至 67.3 秒。并行分支造成主线程吞吐从 141.3 降至 138.6 tokens/s，但该竞争代价仅为 2.8 秒，低于每任务节省的 27.9 秒。

</div>

受控的成对运行表明，表 1 的 token 与轮数下降确实能转化为真实延迟下降，而不只是把 token 记到不同线程后的统计现象。该实验同时揭示并行执行存在资源竞争，因此延迟收益小于 token 降幅；结论目前只直接适用于指定模型、基准、服务端点和并发条件。

<div class="result-source" markdown="1">

来源：In-depth Analysis，Measured Timing Analysis

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under this protocol, Second Thought reduces median per-task wall-clock time from 256.9s to 229.0s (−10.9%), decomposing along exactly the two quantities of Table 1: main-thread decoding time drops from 168.7s to 146.1s (−13.4%), broadly in proportion to the 15.0% fewer main-thread output tokens, while tool execution time drops from 71.6s to 67.3s (−6.0%), tracking the decrease from 56.2 to 52.8 turns at an unchanged 1.27s per turn.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原始主实验跨越不同时间段，API 服务速度和共享服务器执行负载会漂移，因此其墙钟时间不可直接横向比较；受控延迟实验仅覆盖 50 个 SWE-Bench-Pro 样本、DeepSeek-V4-Flash、固定并发 4 和单一端点，尚不能证明延迟收益可无条件推广到其他模型、基准或部署环境。
- $s1$ 并非所有组合都可运行：MiniMax-M3 不会按未闭合 Thought 前缀继续推理，而 $\tau^3$-bench 的函数调用请求不能与前缀续写结合。因此在这些设置中缺少计算量匹配对照，无法同样严格地区分收益来自额外计算还是并行推理结构；此外，消融只在 SWE-Bench-Pro 与 DeepSeek-V4-Flash 上进行，组件作用是否跨领域稳定仍待验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- base：不作修改的标准代理，即主文所称的标准 ReAct 基线。它给出各模型与执行框架原本的任务成功率、主线程解码量和交互轮数，是判断 Second Thought 是否带来实际增益的直接参照。
- $s1$：计算量匹配的 budget-forcing 对照。若当前主线程 Thought 在消耗完 Second Thought 分支所用的同等 token 预算前结束，系统便抑制思考结束符并强制模型继续生成，直至达到该预算。该对照把额外计算放在主线程关键路径上，用于区分“多用了推理 token”与“并行组织推理”两种解释；由于 MiniMax-M3 不遵循未闭合思考前缀，且 $\tau^3$-bench 的函数调用不能与此前缀续写方式结合，相关设置不提供 $s1$。

**实验想回答的问题**

- Second Thought 能否在不同代理任务和推理模型上，在保持或提高一次成功率的同时，减少主线程输出 token 数与交互轮数，从而缩短代理执行的关键路径？
- 性能变化究竟来自额外推理 token 的数量，还是来自并行分支的组织方式；Recall、Check、Rehearse 与 Alternative 等分支是否承担互补作用？

**实验实现**

每种设置将一个推理 LLM 与基准专用执行框架配对：DeepSeek-V4-Flash、Qwen3.6-Plus 和 MiniMax-M3 均通过流式 API 调用，并启用各自原生 reasoning/thinking 模式；SWE-Bench-Pro 使用 mini-SWE-agent，Terminal-Bench 2.1 使用官方执行框架，$\tau^3$-bench 使用标准函数调用对话循环及用户模拟器。表 1 共比较 3 个基准与 3 个模型形成的 9 个组合。Pass@1 的显著性采用经 Benjamini–Hochberg 校正的 McNemar 检验，其余指标采用 Wilcoxon 符号秩检验，星号表示 $p<0.05$。此外，作者在固定并发为 4 的受控条件下，对 50 个 SWE-Bench-Pro 样本成对连续运行 base 与 ours，各重复 3 次并报告中位数，以检查 token 和轮数下降是否真正转化为墙钟延迟下降。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| SWE-Bench-Pro，DeepSeek-V4-Flash：only-recall 与完整配置比较 | only-recall 将主线程输出降至 19.7k tokens，为所有变体最低，但 Pass@1 只有 46.0%；完整配置约为 20.3k tokens、52.0% Pass@1。因此 only-recall 仅额外节省约 2.5% 主线程 token，却损失 6.0 个准确率百分点。 | 该变体隔离了被动回忆历史信息的作用。结果说明 Recall 能压缩后续主线程推理，但若缺少主动验证、下一步预演和备选方案，代理更容易选择错误动作；因此最低 token 数不能单独作为方法更优的证据。 | Ablation Study，Figure 3<br><span class="experiment-evidence">Overall, the full configuration is Pareto-optimal: no variant attains higher Pass@1, and the only variant that decodes fewer main-thread tokens (only-recall, 19.7k) sacrifices 6.0 points of accuracy for a 2.5% saving.</span> |
| SWE-Bench-Pro，DeepSeek-V4-Flash：w/o-recall 与 w/o-rehearse | 移除 Recall 后 Pass@1 降至 48.0%，是留一消融中最明显的准确率下降；移除 Rehearse 后 Pass@1 仍为 52.0%，但主线程输出从 20.3k 增至 22.4k tokens，增加 10%。 | 两个留一消融区分了组件职责：Recall 更直接影响正确性，可能通过重新呈现历史约束来避免重复犯错；Rehearse 对该设置的成功率影响较小，但能预先计算条件化的后续步骤，从而把原本逐轮发生的主线程推理移出关键路径。这里的机制解释是作者根据指标变化提出的归因，并非直接观测到的因果过程。 | Ablation Study，Figure 3<br><span class="experiment-evidence">Conversely, leave-one-out experiments highlight the complementary roles of each component: removing Recall (w/o-recall) causes the sharpest accuracy drop (48.0% Pass@1), suggesting that resurfacing historical constraints helps prevent repeated errors, whereas removing Rehearse (w/o-rehearse) maintains Pass@1 (52.0%) but inflates main-thread output from 20.3k to 22.4k tokens (+10%), confirming that pre-computing conditional next steps primarily offloads deliberation the main thread would otherwise perform turn by turn.</span> |

**定性案例**

- 推理替代重放实验从 DeepSeek-V4-Flash 在 SWE-Bench-Pro 上生成的轨迹中随机抽取 100 条，比较保留与删除 harvested second thoughts 后的下一轮生成，并重复 3 次。删除这些内容后，下一轮平均推理量由 196.2 增至 316.5 tokens。作者据此认为，并行分支并非只增加旁路文本，而是在下一轮替代了主线程本来会重新生成的一部分推理；但该实验测量的是 token 替代效应，并未单独报告两种条件下的任务成功率变化。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It proposes parallel reasoning during an LLM agent's action-observation loop, making both agent execution and reasoning central.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`2b18a596586fa282e384ab91699d59df3cccbdf56341138312de4acffe57a0c7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
