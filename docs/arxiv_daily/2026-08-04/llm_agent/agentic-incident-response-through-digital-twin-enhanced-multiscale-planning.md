---
title: "[论文解读] Agentic Incident Response through Digital Twin-Enhanced Multiscale Planning"
description: "[arXiv 2608.02422][LLM Agent] 本文研究如何把擅长全局决策但只能输出抽象动作的决策理论规划器，与能生成系统命令但容易产生幻觉的大语言模型结合起来，从而形成可验证、可执行的自动化事件响应计划。"
arxiv_id: "2608.02422"
announcement_date: "2026-08-04"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:00:22.345842+00:00"
source_sha256: "0072e073fb688410e30cfb8ca7cbeb63fa6766ada969aa80bcd8dd11bbf25f6c"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "LLM 其他"
  - "自主网络防御"
  - "事件响应规划"
  - "部分可观测马尔可夫决策过程"
  - "多尺度规划"
  - "大语言模型代理"
  - "数字孪生"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.02422</p>

# Agentic Incident Response through Digital Twin-Enhanced Multiscale Planning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Yiran Gao, Tao Li, Kim Hammar</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.02422v1) · [PDF 下载](https://arxiv.org/pdf/2608.02422v1) · **关键词** 自主网络防御, 事件响应规划, 部分可观测马尔可夫决策过程, 多尺度规划, 大语言模型代理, 数字孪生<br>


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

本文研究如何把擅长全局决策但只能输出抽象动作的决策理论规划器，与能生成系统命令但容易产生幻觉的大语言模型结合起来，从而形成可验证、可执行的自动化事件响应计划。

**不用术语来说**：网络遭受攻击后，安全人员既要判断应优先保护或恢复哪些主机，又要为不同服务器编写正确的处置命令。人工处理速度慢且依赖专家经验；现有自动规划通常只会给出“防御某台主机”之类的高层建议，而直接让大语言模型独立制定完整方案又可能生成错误命令或遗漏长程目标。因此，实际需要一种既能统筹网络级响应顺序，又能可靠地产生并检查具体命令的方法。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将事件响应表述为分解的马尔可夫决策过程，把网络级资源分配与响应排序归入战术尺度，把面向具体服务器的命令生成归入操作尺度，从问题建模上明确连接高层策略与底层执行。
- 作者提出多尺度智能体架构：前瞻式 rollout 规划器借助数字孪生仿真计算高层响应策略，轻量级大语言模型将策略转化为可执行命令，再通过数字孪生仿真环境进行部署前验证。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

事件响应是网络遭受攻击后，为遏制攻击、评估影响、保存证据、驱逐攻击者、加固系统并恢复服务而采取的一系列协调行动。本文属于自主网络防御领域，研究如何在仅能获得入侵检测系统告警、日志等不完整信息时，自动规划从受攻击状态恢复到安全运行状态的动作序列。传统决策理论方法可在抽象网络模型中优化高层防御策略，却通常只说明“保护或隔离哪台主机”，不能给出可直接执行的系统命令；大语言模型能够生成具体命令，但缺少可靠的长程规划机制。因此，理解本文的关键是区分战术尺度与操作尺度：前者决定资源和高层动作的安排，后者把这些决策落实为特定服务器上的可执行命令。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**部分可观测马尔可夫决策过程（POMDP）**

POMDP用于描述无法直接看见真实系统状态、只能依据带噪声观测连续决策的问题。在本文中，真实的攻击与恢复状态不可直接获得，防御者需要根据IDS告警和日志选择响应动作，并以尽快恢复系统为目标。

</div>
<div class="concept-item" markdown="1">

**多尺度事件响应规划**

多尺度规划把问题拆成战术尺度和操作尺度：战术尺度确定应对哪些组件采取何种高层防御动作，操作尺度生成实现这些动作的服务器命令。该拆分使抽象规划器负责全局决策，而语言模型负责依赖具体系统环境的执行细节。

</div>
<div class="concept-item" markdown="1">

**数字孪生**

数字孪生是受保护系统的虚拟副本，既可通过抽象仿真快速预测攻击传播和响应效果，也可通过仿真环境中的实际命令执行来检查操作是否可行。通俗地说，它提供了一个部署前的试验场，使规划器能够推演策略，并让生成的命令先接受验证。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

受攻击的网络被表示为图$G=\langle V,E\rangle$，其中$V=\{1,2,\ldots,N\}$是包含$N$个系统组件的节点集合，$E$表示组件之间的连接。攻击被检测后，防御者以IDS告警、日志和基础设施统计等观测为输入；这些观测只与不可直接观察的安全状态相关，且攻击者策略$\theta$通常未知。系统在离散时间步上演化，防御策略依据截至当前时刻的观测历史选择动作，动作通过由攻击策略决定的状态转移过程影响网络。任务输出是一系列响应动作，使系统依次完成遏制、评估、证据保存、驱逐、加固和恢复，并最终进入完全恢复且保持运行的吸收终止状态。优化目标是在有限规划时域$H$内最小化动作执行时间之和，同时兼顾操作成本；不同动作耗时可以显著不同，例如隔离主机可能只需数秒，而取证分析可能持续数小时。本文所处的设置还要求最终方案不仅给出网络层面的高层动作，而且能够形成经过数字孪生验证、可在具体服务器上执行的命令。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$G=\langle V,E\rangle$**

受事件影响的网络图；$V$为组件或主机集合，$E$为组件间连接集合。

</div>
<div class="notation-item" markdown="1">

**$s_t$**

时间步$t$不可直接观测的系统安全与恢复状态；$s_T$表示系统完全恢复后的吸收终止状态。

</div>
<div class="notation-item" markdown="1">

**$o_t$**

时间步$t$获得的观测，例如日志、IDS告警及其他与恢复状态相关的系统指标。

</div>
<div class="notation-item" markdown="1">

**$P_\theta(s_{t+1}\mid s_t,a_t)$**

攻击者策略为$\theta$时，在状态$s_t$执行响应动作$a_t$后转移到状态$s_{t+1}$的概率。

</div>

</div>

**直接相关的工作**

- **基于抽象决策模型和模拟器的自主网络防御方法（文献[39]，以及采用马尔可夫决策过程的文献[40,36,51]）**: 这类方法利用控制与优化、博弈论或强化学习计算具有理论依据的高层响应计划，使复杂网络规划变得可处理；但计划通常停留在战术尺度，缺少服务器相关的实现步骤和可执行命令，因而难以直接部署到真实系统。
- **基于通用大语言模型与提示工程的事件响应代理（文献[42,6,37]）**: 这类代理能够读取大量系统日志并生成操作命令，弥补抽象规划缺少执行细节的问题；但其规划主要依赖反复调用语言模型，缺乏明确的决策理论规划机制，容易产生幻觉，可靠性和可支持的规划时域均受到限制。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

事件响应需要在攻击持续扩散时完成遏制、缓解和恢复，但当前流程主要依靠安全操作员按照预定义剧本处理，决策缓慢、劳动密集，并且要求专门技能。自动化系统若要真正投入运行，不能只判断“接下来保护哪台主机”，还必须针对实际网络环境生成能够执行且经过检查的系统命令。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于抽象模型的决策理论与自主网络防御方法**：这类方法把网络系统抽象为马尔可夫决策过程或模拟器，再利用控制与优化、博弈论或强化学习计算响应计划。抽象模型降低了规划复杂度，也便于比较候选动作的长期效果。
- **基于通用大语言模型的智能体响应方法**：这类方法主要通过提示工程，让通用大语言模型读取告警、日志和系统上下文，并反复调用模型生成处置步骤或可执行系统命令，从而绕过从抽象动作到具体实现的人工转换。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 决策理论方法依赖抽象模型，输出通常停留在战术尺度，例如指定应防御某台主机，却不说明应在该服务器上执行哪些命令；因此即使高层决策具有良好性能保证，也不能直接部署到真实系统。
- 现有大语言模型智能体通常缺少有原则的规划算法，并依赖反复生成来构造完整计划，容易出现幻觉和不可靠命令，同时限制可稳定处理的规划时域；这使其难以兼顾长期响应目标与操作级执行正确性。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未提供一种贯通两个尺度的事件响应机制：一端需要利用决策理论在抽象网络模型上进行高效、面向长期结果的战术规划，另一端需要把每项高层动作可靠地落实为适配具体服务器的命令，并在实际部署前验证这些命令。缺失的关键环节不是单独增强规划器或语言模型，而是建立从高层策略、环境落地到执行验证的闭环。

</div>
<div markdown="1"><span>核心问题</span>

能否构建一种可实际运行的多尺度智能体事件响应方法，使决策理论规划器负责网络级策略与安全资源分配，轻量级大语言模型负责生成系统相关的执行命令，并利用数字孪生同时支持高效规划和部署前验证？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是让不同组件只承担其更擅长的工作：规划器在简化的网络模型中搜索未来攻击演化并确定响应优先级，避免让语言模型独立承担长程决策；语言模型利用日志和系统上下文补齐抽象动作缺少的命令细节；数字孪生则像一个可重复试运行的系统副本，既让高层策略能够低成本推演，也让生成的命令先在隔离环境中接受执行检查。这样可以缩短语言模型需要自主推理的链条，并在命令进入真实网络前暴露操作错误。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把事件响应建模为一个因子化部分可观测马尔可夫决策过程（POMDP），并将决策拆成两个时间尺度：战术层决定“下一步优先恢复哪个组件”，操作层决定“具体执行什么恢复命令”。系统状态由全局安全状态与局部恢复状态组成：对组件 $k$，$g_t^k\in\{0,1\}$ 表示其安全或失陷状态，$\ell_t^k\in\{0,1\}^6$ 表示遏制、评估、证据保全、驱逐、加固和恢复六个阶段是否完成。由于真实状态不可直接观测，模型根据日志、IDS 告警、历史动作及数字孪生执行结果维护信念 $b_t$，即对各状态可能性的概率估计。

端到端来看，离线阶段分别微调三个轻量级 LLM 变体，用于攻击研判、信念生成和恢复动作生成；在线阶段先由攻击研判模型提出攻击策略与技术猜测，再通过数字孪生测试网络依赖关系，建立带攻击传播概率的攻击图。战术规划器在该图上进行前瞻模拟，选择预期延迟成本最低的组件优先级；操作规划器让 LLM 为最高优先级组件生成候选命令和后续恢复轨迹，再在数字孪生中验证命令是否可执行并测量执行时间，选择预计总恢复成本最低的动作。动作执行产生新观测，模型随之更新信念并重复规划，直至当前组件完成六阶段恢复，然后重新计算全局优先级。通俗地说，数字孪生同时充当“快速沙盘”和“安全试验机”：前者比较先救哪台机器，后者确认具体命令能否真正工作。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 离线构造三个事件响应专用 LLM

以 DeepSeek-R1-14B 为基础，使用标准自回归交叉熵分别微调攻击研判、信念生成和响应动作生成三个模型变体；三个任务共享训练形式，但输入输出标签不同。

<div class="method-step__io" markdown="1">

**输入**：事件描述、系统日志与安全告警，以及对应的 MITRE ATT&CK 标签、状态信念与证据摘要、历史动作和下一步恢复动作等监督样本。<br>
**输出**：攻击研判模型 $\Phi_w$、信念生成模型和局部响应动作生成模型。

</div>

**直观理解**：这里不是让一个模型同时承担所有职责，而是训练三个分工明确的角色：一个判断攻击方式，一个整理当前证据和不确定性，一个提出可执行的恢复步骤。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 识别攻击猜测并建立攻击图

对 $I$ 独立生成 $M=10$ 次攻击研判，仅保留经验频率超过 $0.5$ 的攻击战术与技术，形成攻击猜测 $\hat{\theta}$；随后在数字孪生中针对依赖图每条边反复测试相关攻击技术，以估计攻击步骤的成功概率。

<div class="method-step__io" markdown="1">

**输入**：事件描述 $I$、受影响系统的组件与依赖关系，以及攻击研判模型。<br>
**输出**：带传播概率的攻击图 $G(\hat{\theta})$，以及由它诱导的全局状态转移模型 $\hat{P}^g$。

</div>

**直观理解**：LLM 先提出“攻击者可能怎样移动”的假设，数字孪生再用实际测试过滤和量化这些假设，因此后续规划不必完全相信一次文本生成。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 战术层选择待恢复组件

信念模型生成 $b_t$，规划器从全局信念 $b_t^g$ 采样 $M_g$ 个可能状态，并在 $\hat{P}^g$ 上前瞻模拟 $H_g$ 步；它以重要性权重、等待顺序和 $\tau_{\mathrm{avg}}$ 近似累计延迟成本，选择估计成本最低的候选顺序。为避免枚举 $N!$ 个排列，候选集合仅由上一顺序的置换产生。

<div class="method-step__io" markdown="1">

**输入**：当前观测历史、信念模型、攻击图 $G(\hat{\theta})$、上一时刻优先级顺序 $a_{t-1}^g$ 和已处理组件的平均局部执行时间 $\tau_{\mathrm{avg}}$。<br>
**输出**：战术动作 $a_t^g$，即所有组件的新优先级排列及本轮首先处理的组件。

</div>

**直观理解**：规划器把多种可能的真实受害情况放进攻击传播沙盘，比较不同抢修顺序会让多少重要组件继续暴露；它先决定“救谁”，暂不生成具体命令。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 操作层生成、验证并选择恢复动作

LLM 生成候选集合 $A_t^\ell$，并为每个候选首动作生成 $M_\ell$ 条直至局部终态 $\ell_T=(1,1,1,1,1,1)$ 的恢复轨迹；数字孪生逐项仿真执行，使用实测时间计算轨迹成本，不可执行动作的成本设为 $\infty$，最终选取平均剩余成本最低的动作。

<div class="method-step__io" markdown="1">

**输入**：当前信念及证据摘要 $(b_t,m_t)$、战术层选中的组件、前一动作 $a_{t-1}$ 和局部动作生成模型。<br>
**输出**：经数字孪生验证的局部恢复动作 $a_t^\ell$ 及其预计剩余恢复成本。

</div>

**直观理解**：LLM 可以提出多条修复路线，但不能仅凭语言判断其可靠性；系统会在隔离副本中实际运行命令，失败的命令直接淘汰，成功命令按完成整个恢复流程所需时间排序。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 轻量级 LLM 自回归微调目标

$$
\mathcal{L}(w)=-\frac{1}{B}\sum_{i=1}^{B}\sum_{k=1}^{l_i}\log \Phi_w\!\left(y_k^i\mid x_i,y_{1:k-1}^i\right)
$$

**符号说明**

- $\mathcal{L}(w)$：模型参数为 $w$ 时的批次训练损失。
- $w\in\mathbb{R}^d$：可训练的 LLM 参数向量，维度为 $d$。
- $B$：一个小批次中的训练样本数。
- $x_i$：第 $i$ 个任务输入；依模型变体可包含事件描述、观测、信念、证据摘要或历史动作。
- $y^i=(y_1^i,\ldots,y_{l_i}^i)$：第 $i$ 个目标输出的词元序列，长度为 $l_i$。
- $\Phi_w(y_k^i\mid x_i,y_{1:k-1}^i)$：给定输入和正确输出前缀时，模型为第 $k$ 个目标词元分配的条件概率。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标提高正确标签或正确响应文本中每个词元的条件概率。论文对攻击研判、信念生成和动作生成采用相同训练原则，只替换监督样本的输入与目标输出。<br>
**原文位置**：第 5.1 节，公式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 数字孪生验证的局部动作价值

$$
Q(b_t,\hat{a}_t^i)=\frac{1}{M_\ell}\sum_{j\in[M_\ell]}\sum_{\hat{a}\in q_{i,j}}c(\hat{a}),\qquad c(\hat{a})=\begin{cases}\operatorname{DT\text{-}Emul}(\hat{a}),&\text{if verified by DT},\\+\infty,&\text{otherwise.}\end{cases}
$$

**符号说明**

- $Q(b_t,\hat{a}_t^i)$：在当前信念 $b_t$ 下，以候选动作 $\hat{a}_t^i$ 开始时的平均预计剩余恢复成本。
- $b_t$：时刻 $t$ 对全局安全状态和各组件局部恢复阶段的概率信念。
- $\hat{a}_t^i$：LLM 生成的第 $i$ 个候选局部恢复动作。
- $M_\ell$：为每个候选首动作生成的局部恢复轨迹数量。
- $q_{i,j}$：从候选动作 $\hat{a}_t^i$ 开始的第 $j$ 条 LLM 恢复轨迹，持续到目标组件完全恢复。
- $c(\hat{a})$：轨迹中动作 $\hat{a}$ 的成本；通过数字孪生验证时取实测执行时间，否则取正无穷。
- $\operatorname{DT\text{-}Emul}(\hat{a})$：动作 $\hat{a}$ 在数字孪生仿真执行环境中的实测耗时。

<div class="equation-explanation" markdown="1">

**直观理解**：系统不是只比较下一条命令的即时耗时，而是估计该命令开启的完整恢复路线平均需要多久。任何无法在数字孪生中执行的动作都会获得无穷成本，因此不会被选为实际动作。<br>
**原文位置**：第 5.3 节，Operational Planning 段落

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：三个模型变体均通过最小化公式 (1) 的教师强制自回归交叉熵进行监督微调。攻击研判模型学习从事件描述预测 MITRE ATT&CK 战术与技术；信念模型学习从观测及历史动作输出结构化信念 $b_t$ 和证据摘要 $m_t$；动作模型学习在事件上下文、$(b_t,m_t)$ 与前一动作 $a_{t-1}$ 条件下预测下一局部动作 $a_t^\ell$。该训练目标只优化目标文本的似然，并不直接优化恢复时间；恢复时间、组件等待风险和命令可执行性是在在线规划阶段通过攻击图前瞻与数字孪生测量进入决策目标的。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 因子化多尺度 POMDP**

状态写为 $s_t=((g_t^k,\ell_t^k)_{k\in[N]})$，动作写为 $a_t=(a_t^g,a_t^\ell)$：$a_t^g$ 是组件优先级排列，$a_t^\ell$ 是施加于最高优先级组件的局部恢复命令。转移模型将网络级攻击传播与单组件六阶段恢复进度分解，但两者通过“局部完全恢复后全局状态才变为安全”这一条件耦合；论文还假设各服务器状态相互独立，使全局信念可表示为伯努利分布的乘积。

> 直观理解：这一模块把规模较大的网络问题拆成“全网风险排序”和“单机逐步修复”。独立性假设显著降低了信念计算难度，但若真实攻击在多个主机间存在强相关关系，该近似可能低估联动风险。

**2. 双模式数字孪生**

数字孪生是对相关主机、服务、网络连接和配置的隔离复制。在 simulation 模式下，它基于攻击图快速模拟传播和不同优先级顺序，服务于战术规划；在 emulation 模式下，它实际执行候选命令并返回可执行性、耗时和系统观测，服务于操作规划与信念更新。

> 直观理解：模拟模式追求快速比较大量“先处理谁”的方案，仿真执行模式追求确认“这条命令是否真的有效”。两种模式分别解决决策搜索效率和 LLM 命令可靠性问题。

**3. LLM 候选生成与滚动规划器**

LLM 负责把非结构化日志压缩为 $(b_t,m_t)$、生成有限候选动作及其可能后续轨迹；决策规划器不直接接受单次生成结果，而是通过全局蒙特卡洛前瞻和局部多轨迹平均成本进行选择。每轮只执行当前最优动作，获得反馈后重新规划，属于滚动时域的闭环决策。

> 直观理解：LLM 负责提出可读且具体的办法，规划器和数字孪生负责比较、验证与纠错。只执行一步再复查，可缩短一次生成所需的规划跨度，并减少早期错误沿长计划累积。

**训练与推理**

训练时，作者基于标注事件样本分别形成三类指令—答案对，并从同一 DeepSeek-R1-14B 基础模型得到三个专用变体。在线推理开始后，攻击研判模型对事件描述 $I$ 生成十次独立判断，经多数频率过滤得到 $\hat{\theta}$；数字孪生测试系统依赖边并形成 $G(\hat{\theta})$。每个决策时刻，信念模型根据告警、日志、历史动作和执行反馈生成 $(b_t,m_t)$；战术规划器从 $b_t^g$ 采样状态，在攻击图上模拟候选顺序并选择累计延迟成本最低的 $a_t^g$。

确定目标组件后，动作模型产生 $N_\ell$ 个候选首动作，并为每个候选生成 $M_\ell$ 条到达 $\ell_T$ 的轨迹；数字孪生仿真执行轨迹中的命令，记录耗时并淘汰不可执行项。规划器选择 $Q(b_t,\hat{a}_t^i)$ 最小的动作，只执行当前一步，再以新观测 $o_{t+1}$ 更新信念并重新规划。组件完成六个响应阶段后，全局状态中该组件由失陷变为安全，系统回到战术层更新剩余组件的恢复顺序；所有目标组件恢复后结束。

**复现信息**

公平理解和复现所必需的设定包括：基础模型为 DeepSeek-R1-14B；攻击猜测采用 $M=10$ 次独立生成，并保留经验频率超过 $0.5$ 的战术与技术；数字孪生必须既能根据攻击图进行快速 simulation，也能在隔离副本中进行命令级 emulation。战术成本用已处理节点的平均局部执行时间 $\tau_{\mathrm{avg}}$ 近似未知的未来恢复时间，并由 $\lambda\in(0,1]$ 调节组件等待成本相对执行时间的权重。

战术搜索不枚举全部 $N!$ 个优先级排列，而从上一顺序 $a_{t-1}^g$ 的置换中产生候选；其行为还取决于全局采样数 $M_g$、前瞻深度 $H_g$、组件重要性权重 $r(g_t)$、局部候选数 $N_\ell$ 和每个候选的轨迹数 $M_\ell$。所给章节未明确报告这些量的具体取值、微调数据规模、批大小、学习率、训练轮数以及候选置换规则，因此不能仅依据该摘录完整复现实验配置；此外，服务器状态独立和未来执行时间以历史均值近似均属于影响规划准确性的建模假设。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 事件评估数据集 $D_{incident}$：取自文献 [19] 的训练数据。每个样本包含系统描述和安全日志，监督目标包括判断是否发生事件、总结事件、识别相关实体以及标注 MITRE ATT&CK 战术。原文节选未给出样本规模、训练/验证/测试划分比例；其作用是训练事件检测与语义归因模块。
- 信念生成数据集 $D_{state}$：同样来自文献 [19]，输入包括系统描述、日志、事件摘要、局部状态和此前执行的响应动作，目标是预测下一时刻的全局恢复状态、局部恢复状态及证据摘要。系统通过重复生成状态预测并计算经验分布形成“信念”，即对当前恢复状态不确定性的概率表示。原文节选未报告数据规模和划分比例。
- 动作生成数据集 $D_{action}$：来自文献 [19]，根据局部状态和历史动作训练模型生成下一项响应动作。它负责把规划信息转化为操作级动作。三个微调数据集满足 $D=D_{incident}\cup D_{state}\cup D_{action}$；原文节选没有说明三者是否存在样本重叠，也未提供各自规模。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**恢复动作执行时间**

衡量从开始执行恢复动作到完成恢复所需的时间，主要反映响应效率以及生成命令在数字孪生环境中的可执行性。 （越低越好，因为事件处置期间较短的执行时间通常意味着受攻击系统能更快恢复；但该指标本身不说明恢复是否完整或正确。）

</div>
<div class="metric-item" markdown="1">

**恢复率**

衡量攻击场景中系统成功恢复的比例，用于评价响应方案是否最终达到恢复目标。节选没有给出成功恢复的形式化判定条件、分母定义或重复实验次数。 （越高越好，因为它表示更多实验运行或受损对象达到了论文设定的恢复条件。）

</div>
<div class="metric-item" markdown="1">

**MITRE ATT&CK 战术识别精确率**

针对测试数据中的真实战术标签，检查模型预测包含某项战术时有多大比例是正确的，用于测试事件评估模型的战术归因质量。 （越高越好，因为较高精确率意味着模型较少错误地报告并不存在的攻击战术；但仅有精确率不能反映模型漏掉真实战术的程度。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三个攻击场景上的平均恢复动作执行时间，对比前沿 LLM 基线

<div class="result-value" markdown="1">

作者报告，所提智能体事件响应方法将平均恢复执行时间降低了 $15.1\%$。

</div>

这说明把高层资源分配交给 rollout 规划器、再由轻量级 LLM 生成可执行命令，可能比反复调用前沿 LLM 直接规划更快。该结果是三个场景的平均相对改进，不能据此判断每个场景都取得同样幅度的提升，也不能证明在更大或真实企业网络上仍然有效。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across three attack scenarios, our agentic approach reduces recovery execution time by 15.1\% on average and increases the recovery rate by 33.6\% over frontier LLM baselines.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 三个攻击场景上的平均恢复率，对比前沿 LLM 基线

<div class="result-value" markdown="1">

作者报告，所提方法相对前沿 LLM 基线将恢复率提高了 $33.6\%$。

</div>

恢复率提升表明该架构不仅追求更快地产生命令，也更可能使系统达到论文定义的恢复状态。不过，当前节选没有给出恢复率的绝对值、成功判据、逐场景结果或方差，因此无法判断相对提升是否由较低的基线值驱动，也无法评估结果稳定性。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across three attack scenarios, our agentic approach reduces recovery execution time by 15.1\% on average and increases the recovery rate by 33.6\% over frontier LLM baselines.

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

- 前沿 LLM：用于检验直接依赖通用大模型进行事件响应规划时，与论文所提出“规划器决定高层策略、轻量模型生成命令”的架构相比是否存在效率和恢复成功率差距。节选没有列出具体模型名称、版本或提示协议。
- IRCopilot [37]：现有智能体式事件响应基线，用来比较论文方法与专门面向事件响应的既有 LLM 系统，而不只是与通用前沿模型比较。节选未提供其配置和复现细节。
- LLM-IR [19]：与微调数据来源直接相关的现有事件响应方法。该比较有助于判断性能提升是否来自论文提出的多尺度规划和数字孪生架构，而不只是沿用相同训练数据；但要严格确认这一点仍需要消融实验。

**实验想回答的问题**

- 离线 LoRA 微调能否使轻量级语言模型分别完成事件评估、恢复状态信念生成和下一步响应动作生成，从而为后续多尺度规划提供可靠的操作级能力？
- 在三个数字孪生攻击场景中，将战术级 rollout 规划与操作级 LLM 命令生成结合后，是否能比前沿 LLM、IRCopilot 和 LLM-IR 更快、更成功地执行恢复？

**实验实现**

核心模型实例化为 DeepSeek-R1-Distill-Qwen-14B，并使用 LoRA 分别微调事件评估、信念生成和动作生成三个版本；基础模型参数保持冻结，仅训练 LoRA 适配器权重。生成能力测试采用文献中报告的测试事件样本，但当前节选未列出样本数量。端到端实验运行在 Docker 化数字孪生上：环境模拟一个分段小型企业网络，包括客户端子网、服务器子网和兼任路由器与 IDS 监测点的网关；网关通过 Snort 收集告警，并通过 iptables 执行隔离和恢复动作。攻击端包含 nmap、hydra、curl、smbclient 和 sshpass 等工具。端到端评价覆盖 Weak-Credential-3、Shellshock-4 和 Command-Injection-5 三种攻击场景，它们组合了不同攻击模式并危害不同节点。当前节选将详细场景设置指向附录 A，但没有给出运行次数、随机种子、硬件、统计显著性检验或置信区间。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops an LLM agent that converts decision-theoretic rollout plans into executable incident-response actions using a digital twin.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`0072e073fb688410e30cfb8ca7cbeb63fa6766ada969aa80bcd8dd11bbf25f6c`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
