---
title: "[论文解读] Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research"
description: "[arXiv 2608.15052][LLM Agent] 本文提出以独立验证为核心的数学研究智能体 Andy，通过求解器与评估器分离、研究问题多维审查以及基于有向无环图的逐节点证明，使数学问题求解、问题提出、证明修订和研究记录能够被检查、追踪与局部纠错。"
arxiv_id: "2608.15052"
announcement_date: "2026-08-18"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:12:13.222492+00:00"
source_sha256: "7a5f13bf374cadf14f18176894276a8199c8114a2f667af52ed0a91bd1a401db"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "自主数学智能体"
  - "异构网络"
  - "切换拓扑"
  - "指数同步"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.15052</p>

# Andy: A Mathematical Agent for Rigorous Proof and Autonomous Research

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Zi'an Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Address: School of Mathematical Sciences, Tongji University；Address: Key Laboratory of Intelligent Computing and Applications；(Tongji University), Ministry of Education, Shanghai 200092, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.15052) · [PDF 下载](https://arxiv.org/pdf/2608.15052) · **关键词** 自主数学智能体, 异构网络, 切换拓扑, 指数同步<br>


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

本文提出以独立验证为核心的数学研究智能体 Andy，通过求解器与评估器分离、研究问题多维审查以及基于有向无环图的逐节点证明，使数学问题求解、问题提出、证明修订和研究记录能够被检查、追踪与局部纠错。

**不用术语来说**：现有数学智能体可以生成答案、构造辅助对象或搜索高分方案，但“模型写出了一段看似合理的证明”并不等于证明可靠，更不等于它能继续提出值得研究的新问题。实际研究还要求系统说明每一步使用了哪些前提、错误发生在哪里、修改会影响哪些后续结论，以及新问题是否真正重要、原创且可行。本文试图把这些原本依赖研究者反复审查的环节组织成一套可追踪、可暂停、可修订的自动流程。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 构建验证中心化的双模型架构：求解器负责解题、生成研究问题和修订证明，独立评估器只负责检查前提使用、计算正确性与逻辑完整性，并返回结构化错误位置和修改建议，从角色分工上避免求解器直接批准自己的答案。
- 提出从新问题评估到严格证明的闭环机制：系统按重要性、原创性、可行性和连贯性筛选并定向修订问题，再把证明分解为具有显式依赖关系的有向无环图节点，对节点逐一验证、冻结或局部修复，最后组装并统一复核完整证明。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于自主数学研究智能体与网络化控制系统的交叉领域。自主数学研究智能体不仅要生成证明，还要独立评估证明的正确性，并能通过知识获取、定向修订和多阶段验证形成可检查的研究流程；论文以自触发脉冲一致性为起点，让智能体进一步研究具有时延、异构节点和切换通信拓扑的领导者—跟随者网络，目标是设计混合控制机制并严格证明全局指数同步及无 Zeno 行为。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**领导者—跟随者同步**

网络中一个领导者提供参考轨迹，其余跟随者通过局部通信和控制逐渐逼近该轨迹。本文要求这种逼近对所有允许的初始状态成立，并以指数速度衰减。

</div>
<div class="concept-item" markdown="1">

**自触发脉冲控制**

控制器根据当前采样信息预先计算下一次触发时刻，并仅在离散时刻施加瞬时控制作用，从而避免持续监测。本文还考虑脉冲从触发到实际执行之间存在时延。

</div>
<div class="concept-item" markdown="1">

**Zeno 行为**

Zeno 行为指有限时间内发生无限多次采样或控制事件，这在物理系统中无法实现。排除该行为通常需要证明相邻事件时刻之间存在正的时间间隔。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个带领导者的异构网络：节点动力学可以不同，通信拓扑随时间切换，信息传输或脉冲执行存在时延。待设计的输出是一种混合控制策略，由自触发脉冲、执行时延以及脉冲后的恢复阶段连续反馈组成；其中恢复反馈用于在有限恢复窗口内抵消时延误差通道。理论任务是给出保证所有跟随者全局指数同步到领导者的充分条件，同时证明采样序列和脉冲序列均不会出现 Zeno 行为；论文还通过一个数值例子检验所得结论。所给节选未明确列出网络方程、切换规则、时延上界或状态空间假设，因此这些细节不能由摘要推断。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **文献[1]：自触发脉冲一致性研究**: 该工作是 Andy 获取已有知识并形成新问题的起点；本文在其基础上扩展到带时延的异构领导者—跟随者网络、切换通信拓扑、脉冲执行延迟和恢复阶段连续反馈。所给节选未提供文献[1]的作者、题名或具体结论。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

数学研究自动化不只需要回答一个给定命题，还需要形成可审计的研究过程：验证用户提供或模型生成的证明，提出与已有问题或文献有实质联系的新问题，探索可行证明路线，并保留版本、依据、失败原因和修订记录。若这些环节仍以一次性长文本生成完成，研究者很难判断结论是否真正成立，也难以在长任务中定位错误、恢复进度或复用已确认的成果。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **生成模型与专用搜索或符号验证器结合的方法**：FunSearch 让预训练大语言模型提出程序，再由问题专用的系统化评估器打分；AlphaGeometry 由神经模型生成几何辅助构造，再交给符号引擎完成证明。这类方法通过外部评估或形式化推理约束生成结果，但主要围绕特定任务及其专用验证机制展开。
- **面向开放式数学研究的结构发现方法**：Moonshine 不把求解固定命题作为终点，而是从经典问题中提取结构、提出猜想、建立联系并识别障碍，体现了从单题求解向研究问题形成与知识关联扩展的路线。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 已有代表性系统分别擅长程序搜索、特定领域的符号证明或开放式结构发现，但原文未表明它们提供一条统一流程，同时覆盖原问题验证、新问题价值评估、问题定向修订、严格证明和最终审计；因此研究活动的多个关键阶段仍可能彼此割裂。
- 将完整证明作为一次性文本反复生成和审查，会使局部错误引发大范围重写，已经验证的无关部分也可能被重复计算；同时，若生成与批准由同一模型承担，系统还存在自我确认错误答案的风险。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种以独立验证为控制核心的通用数学研究智能体：它既要把“提出什么问题”纳入重要性、原创性、可行性和连贯性的显式审查，又要把“如何证明”表示为可检查的依赖结构，使每个证明步骤只使用已经验证的前提，并支持冻结正确部分、隔离错误影响、保留审计证据和从中断处恢复。

</div>
<div markdown="1"><span>核心问题</span>

能否构建一个端到端的自主数学研究系统，在不降低最终证明正确性要求的前提下，由相互分离的求解器和评估器协作完成原问题求解或核验、研究问题生成与筛选、证明路线选择、逐步验证、局部修复和完整证明交付？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把数学研究看成一系列具有明确职责和依赖关系的检查点，而不是一次生成一篇长证明。独立评估器相当于不能替作者改稿的审稿人，只指出依据、计算或逻辑上的缺陷；有向无环图则像证明的施工图，节点记录引理或步骤，边记录它依赖哪些已证结论。这样，某个节点出错时只需重做它及受影响的后继节点，已通过验证且接口未改变的部分可以继续保留，从而同时提高可审计性与修订效率。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文的方法不是训练一个新的神经网络，而是为一类异构领导者-跟随者网络构造可证明稳定的混合控制方案。输入包括领导者与 $N$ 个跟随者的状态历史、节点动力学参数、时变状态延迟 $h(t)$、切换通信拓扑以及控制参数；系统先在采样时刻 $s_k$ 记录同步误差和当前拓扑，再等待固定执行延迟 $\tau$，于 $t_k=s_k+\tau$ 执行拓扑相关的脉冲校正。脉冲后设置长度为 $\bar h$ 的恢复窗口，通过相位变量 $q(t)=0$ 暂时抵消误差动力学中的延迟通道；旧的脉冲前历史退出活动延迟区间后，再令 $q(t)=1$ 恢复完整延迟动力学。下次采样时刻由无需持续监测状态的自触发规则预先算出，因相邻采样与脉冲执行间隔均至少为 $\tau$，所以不会出现有限时间内无限触发的 Zeno 行为。

理论保证建立在分阶段 Lyapunov 分析上：恢复阶段使用只依赖当前误差的二次型，正常阶段使用同时包含当前误差、时变延迟区间和最大延迟区间历史的 Lyapunov-Krasovskii 泛函。线性矩阵不等式控制连续流的增长，脉冲矩阵不等式保证每次跳变产生收缩，模态矩阵比较与平均驻留时间约束控制拓扑切换造成的代价，最后用累计耗散条件统筹连续增长、切换放大、执行延迟和脉冲收缩。直观地说，方法将难以同时处理的“旧延迟历史、延迟执行的脉冲和拓扑切换”拆成有明确边界的阶段：先按已采样的信息纠偏，再暂时屏蔽可能携带旧误差的延迟反馈，待历史被刷新后恢复正常运行。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立同步误差系统并补偿节点异构性

定义节点误差 $e_i(t)=x_i(t)-s(t)$，连续控制器先加入模型匹配项以抵消领导者与第 $i$ 个跟随者之间的参数差异，再施加反馈 $-K_i e_i(t)$；由 $q(t)$ 决定是否额外抵消延迟非线性误差通道。代入原系统后得到统一闭环误差动力学，其当前状态项为 $-(C_i+K_i)e_i(t)+A_i\Delta f_i(t)$，延迟项为 $q(t)B_i\Delta g_i(t-h(t))$。

<div class="method-step__io" markdown="1">

**输入**：领导者状态 $s(t)$，跟随者状态 $x_i(t)$，异构矩阵 $C_i,A_i,B_i$，参考矩阵 $C,A,B$，非线性函数 $f,g$，以及时变延迟 $h(t)$。<br>
**输出**：以零误差为不变状态、并可在恢复阶段关闭延迟通道的闭环误差系统。

</div>

**直观理解**：控制器先把不同跟随者的动力学差异校正到同一参照系，再直接压低它们与领导者的偏差。这样后续证明只需研究误差是否趋于零，而不必分别追踪每个节点的完整状态。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 采样拓扑相关的误差并延迟执行脉冲

构造 $M_k=\mu_k(L_{\sigma(s_k^-)}+D)$，并在 $t_k=s_k+\tau$ 执行跳变，使脉冲后的堆叠误差满足 $e(t_k)=(M_k\otimes I_n)e(s_k^-)$。调度假设要求从 $s_k$ 到 $t_k+\bar h$ 保持模态 $r_k=\sigma(s_k^-)$，从而避免控制器按采样拓扑计算、却在另一拓扑下执行的模式失配。

<div class="method-step__io" markdown="1">

**输入**：采样时刻 $s_k$ 的左极限误差 $e(s_k^-)$、当前拓扑拉普拉斯矩阵 $L_{\sigma(s_k^-)}$、钉扎矩阵 $D$、脉冲增益 $\mu_k$ 和执行延迟 $\tau$。<br>
**输出**：由采样误差和采样拓扑确定的脉冲后状态 $e(t_k)$。

</div>

**直观理解**：系统在 $s_k$ 拍下一张包含误差和通信关系的“快照”，经过执行延迟后仍严格按这张快照纠偏。冻结相关时段的拓扑，是为了保证脉冲命令的含义在等待期间不会改变。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 运行延迟清洗恢复窗口

在 $[t_k,t_k+\bar h)$ 设置 $q(t)=0$，连续控制器精确抵消闭环误差中的 $B_i\Delta g_i(t-h(t))$ 通道；到 $t_k+\bar h$ 后令 $q(t)=1$，重新启用该延迟通道。由于 $0\le h(t)\le\bar h$，窗口结束时脉冲前的状态历史已经离开所有可能被读取的活动延迟区间。

<div class="method-step__io" markdown="1">

**输入**：脉冲后的误差 $e(t_k)$、最大状态延迟 $\bar h$、相位变量 $q(t)$ 以及连续控制器。<br>
**输出**：不再受脉冲前旧历史直接影响、可恢复完整延迟动力学的误差轨迹。

</div>

**直观理解**：脉冲虽然立即改写当前状态，但延迟项仍可能读取改写前的数据，因此直接恢复延迟反馈会把旧误差重新注入系统。等待一个最大延迟长度并在此期间屏蔽该通道，相当于让系统的延迟记忆完成刷新。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自触发计算下一采样时刻

定义单调递增函数 $\Psi_k(t)=(\bar\lambda+\rho)(t-t_k)-a_k-\bar\lambda\tau$，并把其首次达到非负值的时刻设为 $s_{k+1}$；等价地，$s_{k+1}=t_k+\Phi_k$，其中 $\Phi_k=(a_k+\bar\lambda\tau)/(\bar\lambda+\rho)$。条件 $a_k>\rho\bar h$ 与 $\tau\ge\bar h$ 保证下一次采样位于恢复窗口之后，而 $s_{k+1}-s_k=\tau+\Phi_k>\tau$ 给出严格正的事件间隔。

<div class="method-step__io" markdown="1">

**输入**：当前执行时刻 $t_k$，参数 $a_k>0$、$\bar\lambda\ge0$、$\rho>0$ 和固定执行延迟 $\tau$。<br>
**输出**：预先确定的下一采样时刻 $s_{k+1}$ 和下一脉冲执行时刻 $t_{k+1}=s_{k+1}+\tau$。

</div>

**直观理解**：控制器不必连续观察误差来等待阈值越界，而是在当前事件发生时直接算出下一次检查时间。固定的正时间间隔同时降低监测需求，并排除了事件无限密集的 Zeno 现象。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 统一闭环混合误差系统

$$
\left\{\begin{aligned}\dot e_i(t)&=-(C_i+K_i)e_i(t)+A_i\Delta f_i(t)+q(t)B_i\Delta g_i(t-h(t)),&&t\ne t_k,\\e_i(t_k)&=\left[(M_k\otimes I_n)e(s_k^-)\right]_i,&&t=t_k,\end{aligned}\right.
$$

**符号说明**

- $e_i(t)$：第 $i$ 个跟随者相对领导者的同步误差，即 $x_i(t)-s(t)$。
- $C_i,A_i,B_i$：第 $i$ 个异构跟随者的系统矩阵。
- $K_i$：第 $i$ 个跟随者的连续误差反馈增益。
- $\Delta f_i(t)$：当前状态上的非线性差分 $f(x_i(t))-f(s(t))$。
- $\Delta g_i(t-h(t))$：延迟状态上的非线性差分 $g(x_i(t-h(t)))-g(s(t-h(t)))$。
- $q(t)$：取值为 $0$ 或 $1$ 的阶段指示量；$0$ 表示恢复窗口，$1$ 表示正常流阶段。
- $M_k$：第 $k$ 次拓扑相关脉冲映射矩阵，定义为 $\mu_k(L_{\sigma(s_k^-)}+D)$。
- $s_k,t_k$：第 $k$ 次采样时刻与执行时刻，满足 $t_k=s_k+\tau$。
- $I_n$：$n$ 维单位矩阵；Kronecker 积使节点级脉冲映射作用于每个 $n$ 维状态块。

<div class="equation-explanation" markdown="1">

**直观理解**：该方程是整个控制方案的端到端模型：两次脉冲之间，误差按连续动力学变化；到执行时刻，当前误差被替换为采样时误差经通信拓扑映射后的结果。$q(t)$ 是关键开关，它使证明能够在脉冲后先研究无延迟系统，待旧历史退出后再研究完整延迟系统。<br>
**原文位置**：第 2.1 节，式 (10)；脉冲映射定义见式 (8) 与式 (9)

</div>

</div>

<div class="equation-block" markdown="1">

#### 全局指数同步结论

$$
\|e(t)\|\le C_{\rm GE}\|e_{s_0}\|_{\bar h}\exp\!\left[-\frac{\alpha_{\rm eff}}{2}(t-s_0)\right],\qquad \alpha_{\rm eff}=\alpha+\bar\lambda-\bar\lambda_1,\quad t\ge s_0
$$

**符号说明**

- $e(t)$：由全部节点误差堆叠得到的网络同步误差。
- $C_{\rm GE}$：与具体初始历史无关、但可依赖系统和设计参数的全局指数界常数，且 $C_{\rm GE}\ge1$。
- $\|e_{s_0}\|_{\bar h}$：初始历史区间 $[s_0-\bar h,s_0]$ 上误差范数的上确界。
- $\alpha_{\rm eff}$：最终有效指数耗散率参数，定理给出 $\alpha_{\rm eff}\ge\alpha>0$。
- $\bar\lambda$：自触发与连续流估计使用的统一增长率参数。
- $\bar\lambda_1$：所有拓扑模态中 Lyapunov-Krasovskii 连续流上界 $\lambda_{1,r}$ 的最大值。
- $s_0$：初始采样时刻，也是指数估计的时间起点。

<div class="equation-explanation" markdown="1">

**直观理解**：这不是待最小化的训练损失，而是控制设计最终必须证明的性能证书。它说明无论初始误差历史如何，只要满足定理中的可行性和累计耗散条件，整体同步误差都会按至少 $\alpha_{\rm eff}/2$ 的指数速率衰减。<br>
**原文位置**：第 2.2 节，定理 2.4，式 (20)；$\alpha_{\rm eff}$ 的定义位于式 (14) 后

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该方法是解析控制器设计与稳定性证明，不包含数据驱动训练、参数反向传播或经验风险最小化；需要求解的是控制增益、正定 Lyapunov 矩阵及标量参数的可行性问题。具体而言，应寻找 $P_r,S_r,R_r\succ0$、$K_i$、$\varepsilon_{i,r}>0$、$\lambda_{1,r}$、脉冲参数和触发参数，使式 (15) 的连续流矩阵不等式、式 (16) 的脉冲收缩约束、式 (17) 的跨模态比较约束及式 (19) 的累计耗散约束同时成立。原文在所给章节中给出的是充分条件，没有把它们表述为唯一的数值优化目标，也未明确规定最小化控制能量、触发次数或最大化收敛率的求解程序。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 异构补偿与相位切换连续控制器**

控制器由三部分组成：参数失配补偿、局部误差反馈 $-K_i e_i(t)$，以及受 $1-q(t)$ 控制的延迟通道抵消项。$q(t)=0$ 时闭环误差方程不含延迟非线性项，$q(t)=1$ 时恢复原延迟通道；全局 Lipschitz 条件用 $l_f,l_g$ 将非线性增量转换成误差范数界。

> 直观理解：该模块同时解决“节点模型不同”和“脉冲后旧历史仍在”两个问题。前者靠补偿项对齐，后者靠短时关闭延迟反馈，因而无需假设所有节点完全同构或延迟立即消失。

**2. 切换拓扑脉冲与领导者钉扎**

脉冲矩阵 $M_k=\mu_k(L_{\sigma(s_k^-)}+D)$ 将邻居间误差差分和部分节点的领导者误差合并；$D=\operatorname{diag}(d_1,\ldots,d_N)$ 中 $d_i>0$ 表示节点 $i$ 可在脉冲时直接获得领导者信息。条件 $M_k^{\mathsf T}M_k\preceq\eta_kI_N$ 且 $0<\eta_k<1$ 把每次脉冲限制为欧氏意义下的严格收缩。

> 直观理解：并非每个跟随者都必须直接连接领导者：被钉扎的节点先接收领导者信息，其他节点通过通信图间接获得影响。矩阵收缩条件检查这一轮纠偏是否确实减小整体误差，而不是仅改变误差在节点之间的分布。

**3. 分阶段 Lyapunov-Krasovskii 证书**

恢复窗口采用 $\mathcal V_r^0=e^{\mathsf T}(I_N\otimes P_r)e$，因为此时延迟通道已关闭；正常阶段采用含 $S_r$ 单积分项和 $R_r$ 双积分项的 $\mathcal V_r^1$，覆盖实际延迟 $h(t)$ 及其上界 $\bar h$。模态间关系 $P_r\preceq\mu P_j$、$S_r\preceq\mu S_j$、$R_r\preceq\mu R_j$ 将一次切换的泛函放大限制为至多 $\mu$，平均驻留时间再限制长期切换频率。

> 直观理解：恢复阶段没有延迟项，使用简单能量函数即可；正常阶段必须把一段历史也计入能量，否则无法判断延迟反馈的影响。不同拓扑各有一套能量刻度，$\mu$ 用来限制切换刻度时产生的跳增。

**训练与推理**

不存在机器学习意义上的训练与推理划分。离线设计阶段先给定网络动力学、Lipschitz 常数、延迟上界 $\bar h$、执行延迟 $\tau\ge\bar h$、候选切换图和平均驻留时间约束；随后选择连续增益 $K_i$、钉扎矩阵 $D$、脉冲增益 $\mu_k$、触发参数 $\bar\lambda,\rho,a_k$，并验证定理 2.4 的条件。尤其需要确认每个图连通、采样至恢复结束期间拓扑保持不变、$M_k^{\mathsf T}M_k\preceq\eta_kI_N$、$a_k>\rho\bar h$，以及长期累计耗散式 (19) 对所有时间区间成立。

在线运行时，在 $s_k$ 读取 $e(s_k^-)$ 和模态 $\sigma(s_k^-)$，生成 $M_k$ 并预先计算 $s_{k+1}=s_k+\tau+(a_k+\bar\lambda\tau)/(\bar\lambda+\rho)$；在等待期间按 $q(t)=1$ 运行连续控制，于 $t_k=s_k+\tau$ 执行脉冲并把 $q$ 置为 $0$。接下来在 $[t_k,t_k+\bar h)$ 抵消延迟误差通道，到窗口终点恢复 $q=1$，继续正常连续控制直到下一采样。输出不是类别或预测值，而是所有跟随者状态轨迹及其相对领导者的误差；当离线条件成立时，这些误差满足式 (20) 的统一指数上界。

**复现信息**

公平复现首先需要实现右连续的混合时延系统：脉冲时刻必须区分 $t_k^-$ 与 $t_k^+$，并按采样历史 $e(s_k^-)$ 而非执行前误差重新计算跳后状态。系统还必须保存至少 $\bar h$ 长度的状态历史，以计算 $x_i(t-h(t))$ 和领导者对应延迟状态；$q(t)$ 在 $t_k$ 立即置零，在 $t_k+\bar h$ 恢复为一，普通拓扑切换不得重置它。拓扑信号按原文取左连续，脉冲使用 $\sigma(s_k^-)$，且调度器必须强制 $[s_k,t_k+\bar h]$ 内无切换，并排除恢复窗口右端点后的立即切换。

参数层面需满足 $0\le h(t)\le\bar h$、几乎处处有 $\dot h(t)\le\delta<1$、$f$ 与 $g$ 全局 Lipschitz、每个候选图为连通无向图，以及平均驻留时间不等式。自触发公式在当前表述下可直接闭式计算，不需要在线根搜索；正事件间隔至少为 $\tau$。所给章节未明确报告数值求解器、离散积分步长、容差、代码版本或用于构造可行矩阵与增益的具体优化流程，因此这些内容不能从当前摘录中可靠补全；论文只提供了完整研究日志与报告的 GitHub 地址，并说明外部 Codex 充当模拟人类监控者、检查中间推理并给出针对性指导，但不直接重写 Andy 的结果。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 本文没有机器学习意义上的数据集、训练集或测试集。实验对象是第 3 节的单个数值控制系统实例，用于模拟延迟异构领导者-跟随者网络；所给节选未包含该实例的节点数、参数、初始条件、切换信号及仿真时长。
- 论文还将一次 Andy 研究运行作为系统级案例，完整日志和报告据称发布于项目仓库。它用于展示研究过程的可追踪性，不构成多任务基准数据集，也未报告样本规模或数据划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

原文未明确报告，或这里不需要额外前置概念。

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 第 3 节数值实例：在延迟异构网络、切换拓扑和混合控制共同作用下观察领导者-跟随者同步

<div class="result-value" markdown="1">

作者声称数值实例验证或确认了所建立的同步结论，但所给节选没有提供同步误差曲线、收敛率、最终误差或控制代价等数值。

</div>

这一结果至多说明某个选定参数实例呈现了与定理一致的同步趋势。由于缺少具体图表和数值，不能核验误差是否按理论指数速率下降，也不能据此证明控制器在更广参数范围内优于其他方法；一般性保证主要来自理论定理，而不是该单次仿真。

<div class="result-source" markdown="1">

来源：摘要；具体实验应位于第 3 节，但该节内容未包含在所给节选中

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A numerical example confirms the result.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 数值案例对恢复窗口混合控制总体行为的说明

<div class="result-value" markdown="1">

作者称数值实例展示了预期的同步行为；节选没有报告用于判定“预期行为”的量化阈值或统计检验。

</div>

通俗地说，仿真中跟随者应当逐渐追随领导者，说明“延迟执行的脉冲”和“脉冲后的临时连续补偿”在该实例中能够协同工作。但“illustrates”只表示示范性证据，并不等同于与无恢复窗口控制器、周期触发控制器或已有方法进行过受控比较。

<div class="result-source" markdown="1">

来源：第 4 节结论

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Sufficient conditions were established, Zeno behavior was excluded for both timing sequences, and the numerical example illustrates the expected synchronization behavior.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Andy 的单次端到端自主数学研究案例

<div class="result-value" markdown="1">

作者将该案例解释为：Andy 能从一个已有结果出发，提出具有技术意义的新控制问题，并完成定理、证明和数值说明，同时保留可追踪的依赖关系。

</div>

该案例覆盖了问题生成、证明和仿真的完整链路，因此能提供流程可行性的定性证据。不过它只有一个研究主题，且研究过程中存在外部模拟人类监控者提供针对性指导，所以不能单独证明 Andy 在其他数学领域中的自主成功率、稳定性或相对其他数学智能体的优势。

<div class="result-source" markdown="1">

来源：第 4 节结论

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The case study verifies that Andy can develop a technically meaningful problem from an established result and carry it through theorem construction, proof, and numerical illustration.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文节选未提供第 3 节的数值设置和图表，也未明确报告收敛误差、经验指数速率、触发次数、最小触发间隔、控制能耗或计算时间。因此无法独立核验“确认结果”的强度，也无法判断仿真是否覆盖定理允许范围中的困难情形。
- 实验没有报告基线、消融、多实例重复或数学任务基准，并且案例运行接受外部模拟人类监控者的针对性指导。因此现有证据无法隔离恢复窗口、双模型验证、DAG 证明或人工干预各自的贡献，也不足以支持 Andy 在普遍自主研究能力、可靠性或效率方面的比较性结论。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。

**实验想回答的问题**

- 数值仿真能否说明：在时变状态时延、切换通信拓扑和脉冲执行时延同时存在时，所提出的“自触发脉冲加恢复窗口连续反馈”控制方案仍能使跟随者状态趋近领导者状态？
- 该案例能否作为端到端实例，展示 Andy 从已有自触发脉冲一致性结果出发，完成新问题提出、定理构造、证明验证和数值说明的完整研究流程？

**实验实现**

实验采用数值仿真检查闭环网络的同步行为，理论目标是全局指数领导者-跟随者同步，并同时讨论采样时刻序列和脉冲执行时刻序列不存在 Zeno 行为，即有限时间内不会发生无限多次触发。根据节选，控制器在采样时刻取得网络误差，经过固定执行时延后施加脉冲；随后开启长度等于状态时延上界的恢复窗口，以连续反馈暂时抵消误差系统中的延迟通道，待脉冲前历史退出有效时延区间后再恢复该通道。原文节选未给出第 3 节的具体参数、求解器、步长、重复次数、比较方法、定量评价指标或误差统计，因此无法重建实验协议，也不能判断结果对不同随机种子、初值或参数扰动是否稳健。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 案例从 Hong 与 Zhang 的切换时延多智能体自触发脉冲一致性结果出发，将问题扩展为具有节点异质性、领导者-跟随者结构、时变状态时延、切换拓扑和脉冲执行时延的同步问题。其关键设计是在每次延迟脉冲后设置恢复窗口，由连续反馈暂时消除延迟误差通道。案例的价值在于展示 Andy 如何把已有结果转化为一个条件相互耦合的新问题，并形成定理、证明和数值说明；但由于所给节选缺失第 3 节图表及完整运行统计，这仍是定性案例，不能视为系统性能的综合评测。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops an autonomous mathematical research agent centered on rigorous proof construction and mathematical reasoning.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`7a5f13bf374cadf14f18176894276a8199c8114a2f667af52ed0a91bd1a401db`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
