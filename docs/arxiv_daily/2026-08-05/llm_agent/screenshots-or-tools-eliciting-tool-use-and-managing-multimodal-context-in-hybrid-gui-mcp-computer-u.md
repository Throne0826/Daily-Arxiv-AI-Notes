---
title: "[论文解读] Screenshots or Tools? Eliciting Tool Use and Managing Multimodal Context in Hybrid GUI-MCP Computer-Use Agents"
description: "[arXiv 2608.03327][LLM Agent] 本文指出，混合 GUI–MCP 计算机操作智能体的关键瓶颈并非工具是否可用，而是模型能否在合适时机选择、正确调用并整合工具结果，以及训练时的观察方式是否与压缩后的部署环境一致。"
arxiv_id: "2608.03327"
announcement_date: "2026-08-05"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:38:57.463827+00:00"
source_sha256: "a161b2e18ab5d9fb15c302740a629a96adfec6eacf6e1ba2ce0caf02f6c08b73"
tags:
  - "LLM Agent"
  - "LLM 效率"
  - "LLM Reasoning"
  - "计算机使用智能体"
  - "GUI–MCP混合智能体"
  - "工具使用"
  - "采用缺口"
  - "多模态上下文管理"
  - "OSWorld-MCP"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.03327</p>

# Screenshots or Tools? Eliciting Tool Use and Managing Multimodal Context in Hybrid GUI-MCP Computer-Use Agents

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Siqi Fan, Minghao Li, Xiaoqian Ma, Wenhui Tan, Xiusheng Huang, Juntong Wu, Liujie Zhang, Shuo Shang, Weihang Chen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> AI Platform, Xiaohongshu Inc；Gaoling School of Artificial Intelligence, Renmin University of China；School of Electronic and Computer Engineering, Peking University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03327v1) · [PDF 下载](https://arxiv.org/pdf/2608.03327v1) · **关键词** 计算机使用智能体, GUI–MCP混合智能体, 工具使用, 采用缺口, 多模态上下文管理, OSWorld-MCP<br>


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

本文指出，混合 GUI–MCP 计算机操作智能体的关键瓶颈并非工具是否可用，而是模型能否在合适时机选择、正确调用并整合工具结果，以及训练时的观察方式是否与压缩后的部署环境一致。

**不用术语来说**：计算机操作智能体既可以看截图后点击和输入，也可以调用直接操作软件的文本工具：前者通用但消耗大量输入资源且容易受界面变化影响，后者便宜、精确却只覆盖部分任务。现实中的难点不是简单地二选一，而是让智能体知道何时值得调用工具、怎样正确调用，以及工具成功后是否还需要继续保留可能已经多余的截图。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者把“工具可用但未被采用”明确为采用缺口，并诊断出同一套 MCP 工具与注入框架可能产生方向相反的效果：工具决策较差的模型会忽略工具、写错工具名或错误终止，而较强模型虽然避免了部分错误，仍只使用少量可达工具。这将研究重点从“是否提供更多工具”推进到“模型是否会正确选择并理解工具”。
- 作者从动作与上下文两个层面检验共同机制：动作层面的强化学习奖励能够提高工具采用，却不能同步提高未见任务的准确率，说明决策偏好与工具语义能力不同；上下文层面则表明，成功调用工具后可以删除冗余截图，但要通过训练—推理观察规则匹配，才能避免因输入分布变化造成的性能损失。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

计算机使用智能体（CUA）负责在桌面软件中理解用户指令并完成跨多步操作。本文关注同时具备两条执行路径的混合智能体：一条路径依据截图定位坐标并点击、输入，适用范围广，但视觉输入占用大量令牌，且界面变化会使旧坐标失效；另一条路径调用文本级工具，如模型上下文协议（MCP）服务器提供的应用接口，通常更便宜、精确，却只覆盖部分应用或任务，也不能单独提供视觉确认。因此，核心问题不是用工具完全替代截图，而是智能体应在何时选择工具、何时保留GUI操作，以及工具成功后是否仍需保留后续截图。论文在含309项任务的OSWorld-MCP桌面基准及统一GUI–MCP运行框架中研究这种选择行为，同时考察任务成功与输入令牌成本。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**计算机使用智能体（Computer-Use Agent, CUA）**

能够观察计算机界面、规划多步操作并通过点击、键盘输入等动作完成用户任务的模型系统。其执行结果可在真实或虚拟桌面环境中直接验证。

</div>
<div class="concept-item" markdown="1">

**模型上下文协议工具（Model Context Protocol, MCP tool）**

通过标准化文本接口向模型暴露软件功能的工具；模型生成工具名称与参数，系统执行调用并把文本结果放回上下文。相比逐步点击，它可能更精确且节省视觉令牌，但前提是存在覆盖当前任务的工具，并且模型能正确选择和调用它。

</div>
<div class="concept-item" markdown="1">

**多模态上下文管理**

对智能体历史中的截图、文本指令、动作及工具返回结果进行保留、删除或压缩。本文特别关注工具成功后，其文本结果可能已包含下一张截图所传达的信息，因而可删除冗余截图以降低输入成本。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是自然语言桌面任务、当前及历史GUI截图，以及经检索注入的可用MCP工具描述；智能体在多轮交互中输出GUI坐标动作或带参数的文本工具调用，直至报告完成或达到运行限制。研究设定允许两条路径并存：工具可达任务能够借助MCP执行至少部分关键操作，而工具不可达任务仍必须依赖视觉与GUI，例如验证码、幻灯片重新着色或大量浏览器内交互。论文首先比较相同工具和注入框架对推理型与非推理型模型的影响，再从两个层面刻画选择问题：动作层面考察模型是否从GUI路径切换到可用工具，语境层面考察工具成功后是否可以丢弃冗余截图并缩短图像历史。主要观察对象包括任务成功、工具采用行为和输入令牌成本；其中“采用缺口”指工具虽可用、模型也可能具备调用能力，却仍频繁选择较昂贵GUI路径的现象。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **OSWorld-MCP**: 本文采用的直接评测基础：它在OSWorld执行式桌面环境上加入经过验证的MCP工具，并曾报告强模型也只在36.3%的任务上调用工具。本文进一步追问可见工具为何未被采用、采用后是否真正有益，并在其309项任务上比较统一注入框架下不同模型的工具决策。
- **ToolCUA**: 与本文最接近的GUI–工具混合智能体工作，通过较重的拒绝采样微调与强化学习学习路径编排，并指出朴素MCP注入可能损害GUI智能体。本文对该结论作条件化解释：工具注入并非普遍有害，其效果方向与基础模型能否正确忽略、命名、调用工具及判断终止密切相关；同时本文额外研究训练与推理阶段的多模态上下文规则匹配。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

部署混合 GUI–MCP 智能体时，开发者既要承担工具服务器的建设与注入成本，也要承担截图带来的视觉输入成本。然而，仅把工具暴露给模型并不保证其会使用：模型可能继续执行更熟悉但更昂贵的 GUI 路径，也可能在调用工具时犯名称、参数或终止判断错误。与此同时，工具已经返回文本结果后，继续保存后续截图又可能重复表达同一状态，扩大长轨迹的上下文与服务成本。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **纯 GUI 或以 GUI 为主的计算机操作**：模型根据连续截图理解界面，再用坐标点击、键盘输入等动作完成任务。这种方式可以覆盖没有专用工具的应用和视觉任务，但每轮截图都会增加视觉输入，界面变化还可能使先前坐标失效。
- **GUI 与文本工具混合的注入式智能体**：系统在 GUI 动作之外提供 MCP、命令行接口或智能体技能，并通过检索—注入框架把相关工具描述交给模型，由模型自行决定继续点击还是发起工具调用。既有实践通常着重检查工具集合及注入框架是否足够完善。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 工具可用性被近似当作工具收益的前提，但原文观察到，同一工具与框架对不同策略可能分别产生帮助和伤害；忽略、误命名及围绕工具的错误终止会抵消工具带来的效率或精度收益。因此，只增加工具或改进注入机制，无法保证最终任务表现提升。
- 现有训练通常没有显式教会模型采用较便宜但陌生的路径：它既未充分学习工具调用的语义，也未适应删除冗余截图后的观察分布。结果是奖励可以改变“想不想调用”的行为，却未必形成“会不会正确调用”的能力；直接在推理时压缩截图又可能造成训练—部署分布不匹配。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一个统一分析，区分工具的“存在”、模型的“采用决策”和实际的“调用能力”，并进一步说明工具成功后应如何管理多模态上下文。尤其需要判断两个问题的瓶颈是否相同：动作层面为何放着可用工具不用，以及上下文层面为何不能直接舍弃已被文本结果替代的截图。

</div>
<div markdown="1"><span>核心问题</span>

在同时提供截图操作与 MCP 文本工具的混合智能体中，模型何时会主动选择并正确整合工具；工具成功后，能否删除冗余视觉观察并降低成本；以及训练信号与训练—推理观察规则分别如何影响这两类选择？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把工具调用与截图保留都视为策略选择，而不是固定的系统配置。若问题只在于模型偏好熟悉的 GUI 路径，那么奖励应能推动它更多调用工具；若准确率仍不提高，就能把瓶颈定位到工具名称、参数、结果理解等语义能力。类似地，工具结果已经用文本描述状态时，下一张截图往往信息重复；若在相同的压缩观察规则下重新训练，模型便可能学会依赖文本结果，在保留必要视觉能力的同时减少输入成本。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文构建统一的 GUI–MCP 混合计算机操作代理：模型在每一步同时看到任务指令、有限窗口内的截图与动作历史、上一工具返回结果，以及经检索注入的 MCP 工具签名；随后在同一 `<tool_call>` 格式下选择 GUI 动作、文本工具调用或终止。该框架把研究问题分成两个层次：动作层研究代理是否主动采用工具以及能否正确填写参数，上下文层研究工具返回文本后能否删除冗余截图、缩短图像历史，并通过训练与部署使用相同观察规则来消除分布错配。
在训练侧，作者使用多轮 GRPO。每个任务采样一组完整轨迹，以终局成功或失败为主要回报，并用轻量长度惩罚抑制拖延；工具采用实验还在执行成功且有副作用的新工具调用步骤上加入归一化之后的稠密奖励。上下文压缩实验不奖励工具，而是让 rollout、训练重放、评估和部署都采用 `$k=2$` 图像窗口与成功工具调用后丢弃下一张截图的规则。直观地说，方法一方面训练代理“愿意走工具捷径”，另一方面让代理从训练时就习惯“工具已用文字说明结果，因此不一定还需要看下一张图”的信息环境。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造统一的混合动作空间与当前上下文

系统把 GUI 的 `computer_use` 与检索得到的 MCP 工具签名放入同一工具列表，并把窗口内的用户观察与助手动作交替组织成步骤提示 `$C_t$`。当前用户轮还附加完整指令和动作轨迹，使模型能在 GUI、MCP 与终止动作之间统一决策。

<div class="method-step__io" markdown="1">

**输入**：任务指令 `$I$`、截至步骤 `$t$` 的动作历史 `$H_t$`、最近 `$k$` 个视觉观察、已有工具结果，以及当前应用可用的 MCP 工具集合。<br>
**输出**：供模型在步骤 `$t$` 生成动作 `$a_t$` 的多模态提示 `$C_t$`。

</div>

**直观理解**：这相当于给代理一个共同的“操作菜单”：既可以像人一样点击屏幕，也可以调用直接修改文档或表格的文本接口，而不是让两条执行路径由不同系统分别管理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 执行动作并按观察策略更新上下文

执行器解析并执行动作，将环境截图、错误信息或 MCP 返回值送回代理；若 MCP 调用在执行层成功，`drop-on-success` 可把紧随其后的截图替换为文本占位符，同时图像窗口只保留最近 `$k$` 张被保留的截图。论文的富上下文操作点取 `$k=4$` 且不丢图，压缩设置 `ctx_opt` 取 `$k=2$` 并启用丢图。

<div class="method-step__io" markdown="1">

**输入**：模型生成的 `$a_t$`，其类型可以是 GUI 操作、MCP 调用或成功/失败终止。<br>
**输出**：更新后的环境状态、工具结果与下一步上下文；轨迹持续到模型终止或达到最大步数 `$T_{\max}$`。

</div>

**直观理解**：工具已经用文字报告修改结果时，下一张截图常常只是重复证明同一件事，因此可以暂时不把它塞回模型；但“接口返回成功”不保证任务语义真的完成，参数复杂的工具仍可能需要视觉核验。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 采样多轮轨迹并计算组内优势

先根据终局结果、轨迹长度和触顶情况计算轨迹回报 `$R(\tau)$`，再在同一任务的轨迹组内用均值 `$\mu_x$` 和标准差 `$\sigma_x$` 标准化，并以 `$1/T$` 分配到各步骤。只有成功率位于 `$p\in(0.1,0.9)$` 的固定“梯度带”任务参与训练，以保证组内同时存在成功和失败轨迹、能够产生非零学习信号。

<div class="method-step__io" markdown="1">

**输入**：训练任务 `$x$`、当前策略，以及同一任务采样的 `$G=8$` 条最长 `$T_{\max}=50$` 步轨迹。<br>
**输出**：每个动作步骤对应的训练样本 `($C_t$,$a_t$)` 及基础优势信号。

</div>

**直观理解**：系统让同一道题的多次尝试互相比较：比同组平均水平更好的完整尝试得到正向更新，而且长轨迹不会仅因包含更多步骤就支配梯度。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 按实验目标加入工具奖励或匹配压缩观察

动作层实验在执行成功、非只读且本轨迹中首次出现的“工具—参数”键上设置 `$b_t=1$`，并在组内标准化后加入权重 `$\lambda_{\mathrm{mcp}}=0.1$` 的稠密奖励；上下文层实验则设置 `$\lambda_{\mathrm{mcp}}=0$`，仅使训练 rollout 和评估都使用 `ctx_opt`。奖励不以最终任务成功为触发条件，并且同一键每条轨迹只奖励一次，以减少重复调用或无副作用调用带来的刷分。

<div class="method-step__io" markdown="1">

**输入**：基础优势、每步工具执行记录，以及所选训练配置。<br>
**输出**：工具采用实验的增强优势 `$\hat A_t$`，或上下文匹配实验中基于压缩观察产生的普通优势。

</div>

**直观理解**：前一种配置直接奖励“确实尝试了一个新的有效写操作”，用来检验工具采用意愿能否被塑造；后一种不改变任务奖励，只让代理提前适应部署时会缺少部分截图的观察方式。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 带长度与触顶惩罚的轨迹回报

$$
R(\tau)=\mathrm{succ}(\tau)-\lambda_{\mathrm{len}}\frac{T}{T_{\max}}-\lambda_{\mathrm{cap}}\,\mathbb{1}\!\left[T\geq T_{\max}\right]
$$

**符号说明**

- $\tau$：一次完整的多轮计算机操作轨迹。
- $R(\tau)$：轨迹用于强化学习的标量回报。
- $\mathrm{succ}(\tau)$：终局任务结果，成功取正一，失败取负一。
- $T$：该轨迹实际包含的动作步数。
- $T_{\max}$：允许的最大轨迹长度，实验中为 50 步。
- $\lambda_{\mathrm{len}}$：归一化长度惩罚系数，取 0.05。
- $\lambda_{\mathrm{cap}}$：达到最大步数时的额外惩罚系数，取 0.2。
- $\mathbb{1}[\cdot]$：指示函数，条件成立时为一，否则为零。

<div class="equation-explanation" markdown="1">

**直观理解**：任务成败的 `$\pm1$` 项主导优化，而较小的长度项偏好更短的成功路径；若轨迹耗尽步数预算，再施加额外惩罚。该设计主要用于在成败相同的轨迹之间打破平局，而不是让省步骤取代任务正确性。<br>
**原文位置**：第 5.1 节，公式 (3)

</div>

</div>

<div class="equation-block" markdown="1">

#### 长度去偏并加入稠密工具奖励的步骤优势

$$
\hat{A}_{t}=\frac{1}{T}\cdot\frac{R(\tau)-\mu_x}{\sigma_x}+\lambda_{\mathrm{mcp}}b_t
$$

**符号说明**

- $\hat{A}_t$：轨迹中第 t 步用于 GRPO 更新的优势值。
- $T$：当前完整轨迹的步数；因子一除以 T 用于长度去偏。
- $R(\tau)$：由公式 (3) 得到的当前轨迹回报。
- $\mu_x$：任务 x 的同组轨迹回报均值。
- $\sigma_x$：任务 x 的同组轨迹回报标准差。
- $\lambda_{\mathrm{mcp}}$：稠密工具奖励权重；工具采用实验取 0.1，结果奖励与匹配压缩训练取零。
- $b_t$：工具奖励指示量；满足执行成功、非只读且键首次出现时为一，否则为零。
- $x$：产生当前轨迹的训练任务。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项判断整条轨迹相对同一道题其他尝试好多少，并把信号均匀缩放到各步骤；第二项只在合格的工具调用步骤上提供直接推动。把工具项放在标准化之后，可以避免小奖励被长轨迹和组内归一化几乎完全冲淡。<br>
**原文位置**：第 5.1 节，公式 (4)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：优化目标是用 GRPO提高正优势动作的生成概率、降低负优势动作的概率，并通过相对 rollout 时策略的 KL 正则控制更新幅度。基础信号来自终局任务成败，因此普通 outcome-only 配置学习的是“哪些整条操作轨迹更可能完成任务”；工具采用配置额外使用 `$\lambda_{\mathrm{mcp}}b_t$`，刻意把“是否调用合格工具”与“调用后是否真正完成任务”拆开，以检验采用行为本身能否被奖励塑造。作者明确将执行层成功与语义成功区分：API 返回 `success:true` 只说明调用被服务器接受，不说明正则替换确实匹配、格式转换确实生效或任务目标已经完成。
上下文匹配训练不引入新的压缩奖励，其目标仍是公式 (3) 的任务结果，只改变策略接收的观察分布。因而若压缩损失被恢复，应解释为策略学会在较短图像历史和缺失的工具后截图下行动，而不能解释为删图规则本身提供了额外监督。富观察控制使用相同优化配方但关闭压缩，用于区分一般的训练集学习或记忆，与观察策略匹配带来的适应效果。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 统一 GUI–MCP 上下文与动作接口**

GUI 动作和 MCP 调用共享 `<tool_call>` 模式；上下文交替包含窗口化截图、可选的工具返回 `$\rho(r_i)$`、助手动作、当前指令 `$I$` 与完整历史 `$H_t$`。MCP 工具通过 BM25 检索注入最多 18 个相关签名，执行反馈必须闭环返回模型；对于 Qwen3-VL，GUI 坐标按模型原生的相对 `$1000\times1000$` 网格转换。

> 直观理解：统一接口保证比较的是模型是否选择并正确使用工具，而不是两种动作格式或坐标约定谁更容易解析；闭环反馈则让模型能看到动作成功、失败或报错后继续修正。

**2. 后归一化稠密工具奖励**

奖励指示量 `$b_t$` 只对执行成功、非只读、且此前未出现过相同“工具—参数”键的调用触发，并直接加到组内标准化及 `$1/T$` 分摊之后的步骤优势上。作者指出，若把该奖励放入轨迹回报 `$R(\tau)$` 内，它会经过轨迹平均、组内标准化和长度分摊后衰减到约 `$10^{-4}$`，难以影响策略。

> 直观理解：终局成功信号最多要跨 50 步反传，很难教会模型在某一步主动换用工具；因此作者把一个更清晰的局部信号直接放在正确类型的工具动作上，同时限制重复奖励以避免代理只为得分而反复调用。

**3. 匹配训练的多模态上下文压缩**

压缩策略联合使用两项规则：把截图历史深度从 `$k=4$` 降为 `$k=2$`，并在 MCP 执行成功后用文本占位符代替下一帧截图。训练 rollout、日志重放、评估和最终部署严格共享该观察策略，以避免仅在推理时压缩造成的观察分布变化。

> 直观理解：仅在部署时突然少给图片，模型可能不是能力不足，而是不习惯这种输入；从训练采样开始就使用相同删图规则，相当于让它在考试前一直用同一种简化版资料练习。

**训练与推理**

训练前，作者从 8 个应用的 172 个候选训练任务中，用固定的 `$G=8$`、温度 1.0 rollout 估计成功率，仅保留 `$p\in(0.1,0.9)$` 的 74 个“梯度带”任务；其余任务不参与 rollout，48 个任务作为已见应用中的留出集，Chrome 与 `multi_apps` 的 89 个任务从未训练。每次更新对所有 74 个任务各采样 8 条轨迹，在 96 个并行环境运行，计算公式 (3) 与公式 (4)，并丢弃组平均成功率不在 `(0.05,0.95)` 内的组。策略通过带 KL 惩罚的 GRPO更新；KL 锚定 rollout 时策略，而不是初始基础模型，因为后者的回拉会抵消较小的工具奖励诱导漂移。
工具采用探针只在梯度带的 24 个任务子集上启用 `$\lambda_{\mathrm{mcp}}=0.1$`，检查稠密信号是否能进入贪心策略；匹配压缩训练则取 `$\lambda_{\mathrm{mcp}}=0$`，并在 rollout、训练记录与重放、评估中始终使用 `$k=2$` 加成功工具调用后丢图。推理统一使用贪心解码：模型逐步接收当前压缩或未压缩上下文，生成 GUI/MCP/终止动作，执行器反馈结果后继续循环。对比时还保留 `$k=4$`、不丢图的富上下文基础操作点，以分别评估工具决策、任务能力与输入成本。

**复现信息**

公平解释结果所需的关键实现约束包括：动作解析必须符合模型原生 `computer_use` 调用格式；Qwen3-VL 的坐标必须映射到相对 `$1000\times1000$` 网格；动作执行到观察或错误返回的 VM–代理闭环必须确定且完整。所有报告的强化学习运行使用经过验证的 on-policy 管线，文中给出的诊断为每个窗口 `clip_frac=0`、重要性比率为 1.0；保存检查点除权重外与基础模型字节一致，以排除恢复训练时的配置漂移。
训练的核心配置为温度 1.0、每任务 `$G=8$` 条轨迹、最大 50 步、KL 系数 `$\beta=0.02$`；评估采用贪心解码，准确率探针重复 3 次。上下文有两个关键部署配置：强化学习基准为 `$k=4$` 且保留工具后的截图，`ctx_opt` 为 `$k=2$` 且在 MCP 执行成功后以占位符替图。需要特别注意，丢图门控依据的是执行层 `$\mathrm{succ\_mcp}$`，并非任务语义验证；因此零替换等“机械成功、实际无效”的调用可能删除本可用于纠错的视觉证据。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- OSWorld-MCP：主要评测基准，共包含 309 个计算机操作任务，覆盖可通过截图执行的 GUI 操作以及部分可通过 MCP 文本工具完成的操作；用于比较纯 GUI 路径与 GUI-MCP 混合路径。
- 工具可达任务子集：指至少存在适用 MCP 工具的 OSWorld-MCP 任务。该子集用于衡量模型是否实际采用已有工具；原文摘要仅报告推理模型调用工具的任务数及其占工具可达任务的比例，未给出完整子集构造细节。
- 预注册退化子集：用于检验上下文压缩在视觉信息质量较差时是否扩大“丰富观察”与“精简观察”之间的性能差距；原文未明确报告该子集的规模和具体退化方式。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务成功率或准确率**

由基准任务判定器衡量代理是否完成目标；百分点差表示两种配置成功率的绝对差，而不是相对百分比变化。 （越高越好，因为它直接反映端到端任务完成能力。）

</div>
<div class="metric-item" markdown="1">

**工具采用率**

模型在适合或可达的任务中实际调用 MCP 工具的比例；电子表格强化学习实验还报告采用率从训练前到训练后的变化。 （在工具确实适用且调用语义正确的前提下通常越高越好；单纯提高调用频率并不等于提高任务成功率。）

</div>
<div class="metric-item" markdown="1">

**输入成本**

代理处理的输入 token 数量或相对于未压缩运行点的成本比例，用于衡量截图历史带来的多模态上下文开销。 （在准确率相近时越低越好，因为更少的输入 token 通常意味着更低的推理成本和上下文负担。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 相同 OSWorld-MCP 框架下，比较启用 MCP 工具后推理模型与非推理模型的端到端表现。

<div class="result-value" markdown="1">

同样的工具使推理模型成功率提高 4.0 个百分点，却使非推理模型降低 5.9 个百分点；两种比较均各运行 5 次，差异超过 2 个标准误。

</div>

作者据此主张，工具是否有益并不由“工具存在”单独决定，而取决于模型能否正确判断调用时机、工具名称、参数和终止条件。分析上，这一对照说明工具接口可能放大不同模型的决策能力差异，但不能单凭该结果断言推理机制本身是唯一原因，因为所给材料未展示模型规模、预训练数据或其他能力是否完全匹配。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under one identical GUI-MCP harness on the OSWorld-MCP benchmark (309 tasks), the same MCP tools improve a reasoning model by +4.0pp and degrade a non-reasoning model by -5.9pp (5 runs each, both beyond 2 SE).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 动作层多轮强化学习：在电子表格任务中加入稠密工具奖励，并检查工具采用行为及留出集准确率。

<div class="result-value" markdown="1">

工具采用率由 0.03 提高到 0.33，而且这一倾向延续到贪心解码；然而留出任务准确率没有随之提高。

</div>

该实验把“愿不愿意调用工具”与“能不能正确利用工具”区分开来。作者的结论是行为偏好可以被奖励塑造，但能力没有同步提升；这表明瓶颈更可能位于工具调用语义，例如选择正确工具、生成有效参数并把返回结果整合进后续行动，而不只是缺少调用动机。它也不能证明强化学习普遍无效，因为这里只说明当前奖励和训练设置未把更高采用率转化为留出准确率。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At the action level, a dense tool bonus raises spreadsheet adoption 0.03 -> 0.33 and carries into greedy decoding, but held-out accuracy does not follow.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 上下文层压缩并重训：成功调用工具后省略冗余截图、缩短图像历史，并在同一压缩观察规则下训练和评测。

<div class="result-value" markdown="1">

压缩代理达到 37.8% 的准确率，高于未压缩运行点的 33.0%，输入成本仅为后者的 53%；在预注册退化子集上，丰富观察与精简观察之间的差距降为零。

</div>

作者据此认为，多模态上下文中存在可安全删除的冗余信息，而且模型若按压缩后的观察分布重新训练，能够适应缺少部分截图的输入。该结果同时改善了准确率和成本，但不应解释为“删除截图天然提高准确率”：提升来自压缩规则与重新训练的组合，且所给材料没有提供跨模型、跨基准或统计显著性证据。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The compressed agent then reaches 37.8% against 33.0% for the uncompressed operating point, at 53% of the input cost, and closes the rich-lean gap on a pre-registered degraded subset to zero.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给材料主要包含摘要与附录中的按域机制说明，缺少完整结果表、置信区间、模型配置和任务级数据；除工具开关比较外，多项结果的方差与统计显著性无法核验。
- 调用与未调用任务的难度并非随机分配，存在明显的自选择偏差；同时，压缩结果把观察规则变化与重新训练结合在一起，因此现有证据不足以分别估计截图删除和训练适配的独立因果贡献。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 同一模型的 GUI-only 与 GUI-MCP 配置：保持交互框架和模型不变，仅比较是否提供 MCP 工具，用于隔离“工具可用性”本身的影响。
- 推理模型与非推理模型：用于检验工具收益是否依赖显式推理和正确的工具选择、命名、参数填写及终止判断能力。
- 未经过工具采用强化学习的原始策略：与加入稠密工具奖励的策略比较，以判断工具使用频率是否能够通过训练直接操控。
- 未压缩上下文的运行点：保留常规截图和较长图像历史，与调用工具后丢弃冗余截图并缩短图像历史的策略比较，用于评估准确率—输入成本权衡。

**实验想回答的问题**

- 在相同的混合 GUI-MCP 交互框架中，提供文本工具究竟会提高还是降低计算机操作任务的成功率；这种差异能否由模型的工具决策行为解释？
- 通过强化学习促进工具采用，以及在成功调用工具后压缩截图上下文，能否分别改善工具使用行为和推理成本，同时保持任务准确率？

**实验实现**

核心比较在同一个 GUI-MCP harness 上进行，使模型既可依据截图执行 GUI 动作，也可调用文本形式的 MCP 工具。推理模型和非推理模型的工具开关比较各运行 5 次，并以超过 2 个标准误作为差异稳定性的辅助判断。机制实验分为两层：动作层通过多轮强化学习和稠密工具奖励促进电子表格工具调用，并检查效果能否迁移到贪心解码及留出任务；上下文层则在成功工具调用后省略通常冗余的下一张截图并缩短图像历史，随后在相同观察规则下重新训练。所给材料未明确报告模型名称、任务划分、奖励公式、训练步数、随机种子及任务判定器细节。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 按 Writer 域比较“调用过工具”与“未调用工具”的任务成功率。 | 调用工具的任务成功率为 42%，未调用工具的任务成功率为 82%。 | 这一域内切分用于检查实际工具调用是否与成功相关。作者明确指出，较低成功率同时受到难度自选择和 Writer 复杂工具参数错误的影响：模型往往只在更难任务上求助工具，因此该比较不是随机对照，不能得出“调用工具导致成功率下降”的因果结论。它更直接地暴露了复杂工具的参数化和调用语义问题。 | Appendix E, “Per-domain mechanism notes (Section 3.1 of the main paper)”<br><span class="experiment-evidence">On writer, tasks where a tool is invoked succeed 42% of the time versus 82% without a call — a combination of difficulty self-selection (the model reaches for tools on harder tasks) and mis-parameterized calls to writer’s more complex tools — whereas calc and impress show almost no invoked/non-invoked success-rate difference.</span> |
| 检查 VLC 域中工具覆盖充分时，两类模型是否会主动采用原生工具。 | VLC 提供 12 个原生工具，17 个任务中有 16 个工具可达，但两个模型都从未调用这些工具。 | 该域控制了“没有可用工具”这一解释：大多数 VLC 任务实际上存在工具路径，却仍然没有任何调用，因而直接展示了工具采用缺口。它证明接口覆盖率与实际使用率之间可能严重脱节，但没有说明这些工具路径一定比 GUI 路径更容易，也没有测量强制调用后的成功率。 | Appendix E, “Per-domain mechanism notes (Section 3.1 of the main paper)”<br><span class="experiment-evidence">Gimp, Thunderbird, and Chrome expose no MCP tools at all; VLC exposes 12 native tools with 16/17 tasks tool-reachable, yet neither model ever calls one.</span> |

**定性案例**

- 多应用任务揭示了“全任务可用工具”与“当前步骤可用工具”的区别：任务早期经常位于工具不适用的应用中，因此整体被视为工具不可达。该现象说明工具采用率必须结合步骤级可达性解释，否则可能把合理的不调用误判为采用不足。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Studies tool-use behavior in multimodal computer-use agents and reduces agent context cost through screenshot and image-history compression.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`a161b2e18ab5d9fb15c302740a629a96adfec6eacf6e1ba2ce0caf02f6c08b73`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
