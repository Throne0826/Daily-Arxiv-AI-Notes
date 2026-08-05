---
title: "[论文解读] PACE: Adaptive Budget Allocation for Time-Efficient Embodied Planning"
description: "[arXiv 2608.03034][机器人 / 具身智能] PACE针对具身规划中“推理必须完成后才能行动”造成的高延迟，利用动作执行期间的空闲计算窗口并动态分配推理预算，以改善任务成功率与总完成时间之间的权衡。"
arxiv_id: "2608.03034"
announcement_date: "2026-08-05"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:42:32.161038+00:00"
source_sha256: "66447e5935aaf65948e45f24d4f38a5347d6843f790e4b47d788ed2d5cce9eae"
tags:
  - "机器人 / 具身智能"
  - "LLM 效率"
  - "LLM 其他"
  - "LLM Reasoning"
  - "具身规划"
  - "大语言模型"
  - "时间延迟感知规划"
  - "交错思考与行动"
  - "动态推理预算"
  - "并发规划与执行"
  - "Robotouille"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2608.03034</p>

# PACE: Adaptive Budget Allocation for Time-Efficient Embodied Planning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Yuchen Huang, Xijiang Ying, Zhenhua Ma, Xiaxiang Yuan, Zhijie Gao, Jiayi Huang, Ruichi Mao, Jiazheng Zhang, Hongsheng Ti, Maotao Tian, Rong Shi, Lu Zhao, Shizhuang Zhang, Zhuo Cui, He Wang, Ling Liu, Wei Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> ZTE Corporation</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03034v1) · [PDF 下载](https://arxiv.org/pdf/2608.03034v1) · **关键词** 具身规划, 大语言模型, 时间延迟感知规划, 交错思考与行动, 动态推理预算, 并发规划与执行, Robotouille<br>


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

PACE针对具身规划中“推理必须完成后才能行动”造成的高延迟，利用动作执行期间的空闲计算窗口并动态分配推理预算，以改善任务成功率与总完成时间之间的权衡。

**不用术语来说**：具有强化推理能力的大语言模型往往要先生成很长的思考过程，机器人只能停下来等待，拿到结果后才开始行动；但许多物理动作本身需要持续一段时间，例如移动、抓取或加工物体，这段时间原本可以用于思考下一步。与此同时，不同决策的难度并不相同：简单操作无需长时间推理，关键决策却可能需要更多计算。论文要解决的就是如何让机器人一边执行当前动作、一边规划后续动作，并把有限的思考时间用在更需要它的步骤上。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出时间延迟感知具身规划问题及PACE框架，将推理与动作执行组织为可重叠的流水线；其中，交错思考—行动架构利用当前动作的执行时段并发生成后续决策，从系统结构上减少机器人等待推理的时间。
- 提出动态预算分配器，根据每个动作提供的执行时间窗口及决策重要性调整推理令牌预算，并以提示引导结合令牌截断实现无需重新训练的预算控制；同时采用成功率与总完成时间的联合视角评估质量—效率权衡。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于具身智能中的大语言模型任务规划研究。具身规划要求智能体根据任务目标和环境反馈生成可由机器人执行的动作序列；推理增强模型通常先生成较长的思维链，再输出动作，虽然有助于处理多步依赖和纠错，却可能让机器人在推理期间持续空闲。本文关注的关键背景是：物理动作本身具有不可忽略且通常可预测的执行时长，因此动作执行阶段可以成为后续规划的计算窗口；评价系统时也不能只看任务是否完成，还要同时考虑推理延迟与总完成时间。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**具身规划**

智能体在可交互环境中把高层任务目标转化为实际动作，并依据动作后的环境状态继续决策。它不同于纯文本规划，因为物理动作有执行时间、前置条件和可能改变后续决策的信息反馈。

</div>
<div class="concept-item" markdown="1">

**思维链推理**

模型在给出可执行动作前生成若干中间推理步骤，以分解任务、检查约束并选择下一步。更长的推理可能提高决策质量，但会增加生成令牌数量和推理延迟。

</div>
<div class="concept-item" markdown="1">

**推理预算**

允许模型在一次决策中用于思考的计算资源，本文主要以思考令牌数来控制。静态预算对每个步骤采用相同限制，而时间感知的动态预算会根据动作执行窗口和决策难度调整投入。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文将问题置于具有不同动作持续时间的具身任务环境中：输入包括当前任务目标、可观测环境状态，以及当前或候选动作可提供的执行时间窗口；规划器需要持续输出下一步可执行动作，并在动作执行期间为后续决策进行推理。基本假设是高层规划由推理增强大语言模型完成，低层控制器负责执行动作，且动作执行与不依赖其最终反馈的部分认知计算可以并发。目标不是单独最大化成功率或最小化令牌数，而是在任务成功与端到端完成时间之间取得更好的折中，尤其减少机器人因等待模型完成全部推理而产生的空闲时间。原文称该设置为时间延迟感知具身规划，但所给章节未呈现其完整形式化定义与符号体系。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **ReAct**: ReAct通过交替生成推理轨迹、执行动作并接收环境反馈，提高多步交互任务中的纠错能力；但论文指出，这类方法主要优化规划质量，仍未系统利用物理动作执行期间的时间窗口，也没有按窗口长度分配思考预算。
- **静态或动态预算约束推理**: 既有工作通过限制思考令牌抑制推理成本或“过度思考”，部分动态方法还依据任务复杂度或不确定性调整深度；本文与其直接差异在于把具身动作的可预测执行时间纳入预算决策，使计算投入与真实时间约束相匹配。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

推理增强型大语言模型虽然能通过较长的多步推理提升规划能力，但单次规划可能产生数百乃至数千个思考令牌，使具身系统在行动前长时间空等。对机器人等交互系统而言，问题不仅是计算成本高，更是墙钟时间不可接受：环境可能持续变化，系统却无法及时开始或继续执行任务，因此离线规划能力难以直接转化为实时具身能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **迭代式推理—行动与层次化规划方法**：以ReAct、层次化任务分解和结构化提示为代表的方法，把复杂目标拆成若干决策步骤，并在行动后读取环境反馈，再据此修正规划。它们主要通过增加推理、反馈和分解过程来提高计划的可靠性。
- **统一预算约束推理**：这类方法为模型设置固定或全局统一的思考令牌上限，以压缩生成过程和推理延迟；同一预算通常作用于所有规划步骤，而不区分步骤难度，也不利用物理动作正在执行时形成的并发计算窗口。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有规划范式通常仍按“先完成全部思考，再开始执行”的串行顺序运行。其后果是当前动作的执行时间不能用于准备下一步决策，机器人既要支付完整推理延迟，又要支付动作执行时间，导致端到端完成时间过长。
- 固定预算忽略了步骤之间的认知需求差异和可用时间差异：简单的抓取或放置可能获得不必要的长推理，造成计算浪费；复杂的多步决策又可能因相同上限而推理不足。已有方法因此无法同时避免过度思考与关键步骤思考不足。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究分别探索了通过更充分的推理提高规划成功率，以及通过统一令牌限制降低推理开销，但尚缺少一种面向具身任务时间结构的机制：它需要明确建模动作执行产生的时间窗口，将后续推理放入这些窗口，并依据窗口长度与决策需求逐步调整预算，从而联合优化规划质量和实际完成时间，而不是只优化其中一项。

</div>
<div markdown="1"><span>核心问题</span>

在无需重新训练推理模型的条件下，能否通过交错执行推理与物理动作，并按每一步可用执行时间和决策重要性分配思考令牌，使具身规划在保持或提高成功率的同时显著缩短墙钟完成时间？

</div>
<div markdown="1"><span>作者直觉</span>

物理系统执行动作时，语言模型并不一定需要同步闲置：当机器人正在完成一个耗时动作时，模型可以提前思考下一步，这类似流水线中不同工序同时处理不同阶段。动作持续越久，可隐藏的推理越多；若某一步容易，就应尽早停止思考，把计算余量留给更关键的分支选择。因而，PACE的关键不是一律减少推理，而是让推理发生在合适的时间，并把认知资源投向最有价值的决策。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PACE（Planning with Adaptive Cognitive Effort）是一套面向具身规划推理阶段的时间感知框架，不训练新的规划模型，而是在启用推理模式的大语言模型外增加调度与预算控制。其输入包括当前环境观测$o_i$、任务目标$g$、上一动作$a_{i-1}$的执行状态、模型推理速度$v$以及各类动作的预计执行时间$t_{\mathrm{exec}}(a)$；系统先用很小的首步预算$b_{\mathrm{first}}$尽快生成$a_0$，随后把动作$a_i$的物理执行与下一步$a_{i+1}$的语言模型推理重叠。动态预算分配器依据当前动作形成的执行窗口、固定系统开销和任务难度系数$\alpha$计算下一轮思考预算，混合预算控制再通过提示词引导和强制截断使推理尽量按时结束。每轮输出一个可执行动作，并将环境反馈写回上下文，直至任务成功或达到最大步数$N_{\max}$，最终输出成功标志$d$与流水线总耗时$T$。

技术上，PACE把传统的“先完整思考、再执行动作”改造成一条认知—执行流水线：第$i$步的思考时间$t_{\mathrm{think}}^{(i)}$可以被第$i-1$步的执行时间$t_{\mathrm{exec}}^{(i-1)}$遮蔽，只有超出执行窗口的正差值才会让机器人空等。直观地说，机器人在移动、抓取或加工物体时，不再让语言模型闲置，而是利用这几秒提前准备下一条动作；与此同时，系统不会一味允许更长的思维链，而是按照“当前能用多少时间、这一步有多难”分配认知资源，从而同时控制延迟和无效的过度推理。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 环境初始化与首动作快速生成

调用$\mathcal{E}.\mathrm{reset}()$取得初始状态与观测，将难度系数初始化为$\alpha=1.0$，并以通常为50至100个token的$b_{\mathrm{first}}$构造提示$p_0$。规划器$\pi_\theta$在该预算约束下生成首动作$a_0$，避免首动作之前不存在可供遮蔽的执行窗口而造成长时间停顿。

<div class="method-step__io" markdown="1">

**输入**：环境$\mathcal{E}$、语言模型规划器$\pi_\theta$、初始观测$o_0$、任务目标$g$和首步预算$b_{\mathrm{first}}$。<br>
**输出**：首个可执行动作$a_0$、其思考时间$t_0$以及开始运行的规划上下文。

</div>

**直观理解**：流水线启动前没有上一动作可与思考并行，因此首步相当于“快速起步”：先做一个通常较直接的动作，再利用它的执行时间认真考虑后续。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 动作执行与前瞻推理交错

ITA循环让$a_i$开始物理执行，并在该执行阶段为下一决策进行预算受限的语言模型推理；从第$i\geq1$步起，该阶段的可见耗时由$\max(t_{\mathrm{think}}^{(i)},t_{\mathrm{exec}}^{(i-1)})$决定。若推理先完成，动作仍继续执行；若推理更慢，则产生等待间隙$\Delta_i=t_{\mathrm{think}}^{(i)}-t_{\mathrm{exec}}^{(i-1)}$。

<div class="method-step__io" markdown="1">

**输入**：当前动作$a_i$、当前观测$o_i$、预算$b_i$以及上一动作的执行窗口。<br>
**输出**：下一候选动作、实际思考耗时，以及已被执行窗口遮蔽或形成等待间隙的时间记录。

</div>

**直观理解**：这类似厨房中一边等待食材烹饪，一边安排下一道工序；只有计划所需时间超过烹饪等待时间时，流水线才真正被推理拖慢。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 动态计算下一轮认知预算

DBA先把可用执行秒数换算为token容量，扣除动作输出预留，再以$\alpha(s_i,g)$整体缩放基础预算；算法还设置最小预算$b_{\min}$，避免窗口很小时完全没有推理空间。动作失败时将$\alpha$乘以1.5并截断到2.0，成功时乘以0.8并下限截断到0.5，使后续资源随反馈调整。

<div class="method-step__io" markdown="1">

**输入**：动作$a_i$的预计执行时间$t_{\mathrm{exec}}(a_i)$、推理速度$v$、固定开销$t_{\mathrm{overhead}}$、动作输出预留$c_{\mathrm{output}}$、状态$s_i$、目标$g$和动作成败反馈。<br>
**输出**：下一轮软预算$b_{i+1}$和更新后的难度系数$\alpha$。

</div>

**直观理解**：执行时间较长就像提供了一段更长的免费思考窗口，而失败说明问题可能更难，应增加推理资源；连续成功则允许系统缩短思考，减少不必要的延迟。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 混合预算约束下生成动作

软控制把预算及相应推理策略写入系统提示：低于100个token时要求立即给出动作，300至600个token时允许多步规划，更大预算时鼓励更完整的依赖分析。硬控制在思考token达到上限时插入思考结束分隔符并转入动作生成，实际硬上限设为软预算的$1.2\times$。

<div class="method-step__io" markdown="1">

**输入**：观测$o_{i+1}$、任务历史、目标$g$和预算$b_{i+1}$。<br>
**输出**：在时间边界内形成的下一动作$a_{i+1}$及其预算使用记录。

</div>

**直观理解**：软提示类似告诉规划者“你有多少时间”，帮助其主动压缩思路；硬截断则像计时器到点强制提交答案，防止模型忽略提示而无限延长推理。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 交错推理—执行的流水线总时间

$$
T_{\mathrm{total}}^{\mathrm{pipe}}=t_{\mathrm{think}}^{(0)}+\sum_{i=1}^{N}\max\left(t_{\mathrm{think}}^{(i)},t_{\mathrm{exec}}^{(i-1)}\right)+t_{\mathrm{exec}}^{(N)}
$$

**符号说明**

- $T_{\mathrm{total}}^{\mathrm{pipe}}$：交错推理与执行模式下的端到端流水线总时间。
- $t_{\mathrm{think}}^{(0)}$：生成首动作前的初始推理时间；由于没有上一动作，它不能被执行窗口遮蔽。
- $t_{\mathrm{think}}^{(i)}$：规划第$i$步动作所需的语言模型推理时间。
- $t_{\mathrm{exec}}^{(i-1)}$：第$i-1$步物理动作的执行时间，也是第$i$步推理可利用的并发窗口。
- $t_{\mathrm{exec}}^{(N)}$：最后一步动作的执行时间；其后没有下一轮推理可与之配对。
- $N$：规划轨迹的最后一步索引。

<div class="equation-explanation" markdown="1">

**直观理解**：中间每一轮只计推理和上一动作执行二者中较长的时间，因为较短者已经被并行过程遮蔽。若所有$i\geq1$都满足$t_{\mathrm{think}}^{(i)}\leq t_{\mathrm{exec}}^{(i-1)}$，那么中间推理不再额外增加总耗时；可隐藏的思考时间等价于各轮$\min(t_{\mathrm{think}}^{(i)},t_{\mathrm{exec}}^{(i-1)})$之和。<br>
**原文位置**：第III-B节，公式(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 动态思考token预算分配

$$
b_{i+1}=\alpha(s_i,g)\cdot\left(\left\lfloor\left(t_{\mathrm{exec}}(a_i)-t_{\mathrm{overhead}}\right)\cdot v\right\rfloor-c_{\mathrm{output}}\right)
$$

**符号说明**

- $b_{i+1}$：为下一轮推理分配的思考token预算。
- $\alpha(s_i,g)$：由当前状态$s_i$和目标$g$决定的难度调整系数，取值范围为$[0.5,2.0]$。
- $s_i$：第$i$步的当前环境状态。
- $g$：具身任务需要达到的目标。
- $t_{\mathrm{exec}}(a_i)$：动作$a_i$的预计物理执行时间。
- $t_{\mathrm{overhead}}$：网络通信和预处理等不能用于生成思考token的固定时间开销。
- $v$：语言模型的推理生成速度，单位为token每秒。
- $c_{\mathrm{output}}$：为最终动作文本生成预留的token数量。

<div class="equation-explanation" markdown="1">

**直观理解**：公式先计算动作执行窗口扣除系统开销后能生成多少token，再预留输出动作所需的token，最后按任务难度整体放大或缩小。因而预算既与实际时间容量相匹配，又允许失败恢复或关键决策获得额外推理资源；主循环实现还通过$b_{\min}$设置最低预算。<br>
**原文位置**：第IV-C节，公式(4)；最低预算实现见算法1第20行

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。PACE不是通过监督学习、强化学习或参数微调训练出的新模型，原文也没有定义用于更新$\theta$的损失函数；它是在现成的推理模式LLM上进行推理时调度。文中关于成功率$\mathrm{SR}(b)$随预算$b$呈凹函数以及存在$b^*\ll b_{\mathrm{full}}$仍可保留大部分成功率的讨论，是预算缩减的理论假设与解释，不是实际训练目标。系统层面的设计目标是在成功率$\mathrm{SR}(\pi)$与平均总时间$\overline{T}(\pi)$之间推进Pareto前沿，即避免存在另一策略同时具有更高成功率和更低耗时；这同样属于评价准则，而非可微优化损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Interleaved Think-Act（ITA）循环**

ITA把第$i$步推理与第$i-1$步动作执行放入同一时间窗口，并采用首动作快速响应、执行期前瞻思考和动作间无缝交接三项原则。其目标不是减少每个物理动作的固有耗时，而是将$t_{\mathrm{think}}^{(i)}$尽可能包含在$t_{\mathrm{exec}}^{(i-1)}$内，使推理对端到端延迟的新增贡献接近首步思考与少量正间隙之和。

> 直观理解：传统系统让机器人和模型轮流工作，ITA则让二者像流水线上的两个工位并行工作。它解决的是调度浪费：即使推理本身没有变快，只要能藏在机器人本来就必须花费的执行时间里，用户感受到的总延迟也会下降。

**2. Dynamic Budget Allocator（DBA）**

DBA以$t_{\mathrm{exec}}(a_i)$和实测推理速度$v$估算当前执行窗口可容纳的token数，扣除网络／预处理开销$t_{\mathrm{overhead}}$及动作生成预留$c_{\mathrm{output}}$，再用$\alpha\in[0.5,2.0]$适配任务难度。论文给出的启发式语义是：成功后的简单操作可取$\alpha=0.5$，默认取1.0，前一步失败取1.5，连续失败或关键决策可取2.0；主循环用乘法更新实现逐步升降。

> 直观理解：固定token上限无法同时适合短移动、长加工、简单操作和失败恢复。DBA相当于按“可用时间”和“问题难度”联合发放思考额度，让简单步骤少想、困难或失败后的步骤多想，但其难度判断是启发式规则而非学习得到的最优策略。

**3. Hybrid Budget Control（混合预算控制）**

该模块把提示级软约束与解码级硬约束结合：软层要求模型根据预算采用立即作答、多步规划或完整分析等不同策略；硬层在达到token界限时结束思考并迫使模型输出动作。硬上限为软预算的$1.2\times$，用于容纳生成波动，同时保留确定性的时间边界。

> 直观理解：只有软提示时，模型可能不严格遵守预算；只有硬截断时，推理又可能在毫无准备的中间位置被切断。两者结合使模型先主动组织有限思考，再由硬边界兜底，是质量与时限之间的工程折中。

**训练与推理**

训练阶段：原文未报告对基础模型进行任何额外训练，PACE直接使用具备内在思维链能力、已启用推理模式的LLM，例如DeepSeek-R1或Qwen3。难度系数$\alpha$不是由数据拟合，而是依据动作成功／失败和关键决策设置的启发式控制量；动作时间模型也由预设的类别时长提供。因此，复现时不应把结果解释为模型参数能力提升，而应归因于推理预算控制和认知—执行调度。

推理阶段：环境重置后，系统以$b_0=b_{\mathrm{first}}$构造首轮提示并调用$\pi_\theta$生成$a_0$；动作送入环境后得到新观测$o_{i+1}$、奖励$r$和完成标志$d$。随后根据动作执行时长$e_i=t_{\mathrm{exec}}(a_i)$、推理速度$v$与固定开销计算$b_{i+1}$，软提示告知模型预算和建议的推理粒度，硬截断保证生成不会无限越界；与此同时，下一轮推理原则上与当前动作执行并发。若观测表明动作失败，系统提高$\alpha$，否则降低$\alpha$；循环持续至$d$为真或达到$N_{\max}$，最后返回$d$和流水线时间$T$。需要注意，算法1以逐行伪代码表达环境交互和计时，但其时间累计使用$\max(t_i,e_{i-1})$来刻画概念上的并发流水线，而不是要求读者将伪代码理解成严格串行执行。

**复现信息**

公平解释和复现所必需的设置包括：首步预算$b_{\mathrm{first}}$通常为50至100个token；难度系数限制在$[0.5,2.0]$，失败后按$\alpha\leftarrow\min(1.5\alpha,2.0)$增加，成功后按$\alpha\leftarrow\max(0.8\alpha,0.5)$减少；硬预算设置为软预算的$1.2\times$。动作执行时间按类别建模：移动为3.0秒，Pick、Place、Stack、Unstack等操作为4.0秒，Cut、Cook、Fry、Boil等加工为5.0秒；原文在分段函数中还列出Do nothing对应$t_{\mathrm{noop}}$，但未在所给章节明确报告其数值。

预算换算依赖部署环境下的实际推理速度$v$以及$t_{\mathrm{overhead}}$和$c_{\mathrm{output}}$，因此这些量应在目标硬件与服务路径上测量，不能直接把示例数值当作跨平台常数。论文举例称，在$v$约为150 token/秒且操作执行窗口为4.0秒时，扣除开销后可分配约540个token；这是说明计算方式的例子。所给实验摘要使用Qwen3-8B-AWQ，但摘录未明确报告$t_{\mathrm{overhead}}$、$c_{\mathrm{output}}$、$b_{\min}$和$N_{\max}$的具体数值，复现时需回查完整论文或代码，不能自行补造。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Robotouille 同步数据集：Robotouille 是面向大语言模型智能体的厨房具身规划基准，完整基准包含同步与异步模式下的 20 类任务、共 200 个测试实例；实验仅采用其中 100 个同步实例。该子集的动作执行时间确定且预先已知，便于检验 PACE 是否能够依据可用执行窗口分配推理预算。任务难度从最优路径为 10 步的简单三明治制作，到最优路径为 63 步的多食材组合任务。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务成功率**

达到任务目标的测试实例占比，直接衡量规划与执行是否最终完成任务；论文同时为部分成功率报告 95% 置信区间，以表示有限样本下的不确定性。 （越高越好，因为更多实例成功完成目标。）

</div>
<div class="metric-item" markdown="1">

**总完成时间**

从任务开始到成功达到目标或判定失败的墙钟时间，综合包含模型推理、动作执行及未被重叠隐藏的等待时间。 （越低越好，因为具身系统通常需要及时行动；但应与成功率联合考察，避免以快速失败换取较短时间。）

</div>
<div class="metric-item" markdown="1">

**思考时间隐藏率**

与动作执行时间重叠的思考时间占全部思考时间的比例，用来衡量交错流水线利用执行窗口的效率，而不是直接衡量任务质量。 （通常越高越好，因为更大比例的推理没有转化为额外墙钟等待；但它本身不能保证计划正确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Robotouille 同步数据集的默认 PACE 与 ReAct+Think 对比

<div class="result-value" markdown="1">

默认 PACE 的成功率为 10%，95% 置信区间为 [5.0%, 17.8%]；ReAct+Think 为 6%，95% 置信区间为 [2.5%, 12.0%]。论文将二者差异表述为 67% 的相对提升。

</div>

作者结果表明，在同一模型和推理配置下，按执行窗口交错推理并动态分配预算，没有因压缩可见等待时间而降低成功率，点估计反而高于串行的 ReAct+Think。这里的 67% 是从 6% 到 10% 的相对增幅，绝对提升只有 4 个百分点；两个置信区间明显重叠，因此该实验提供的是有利迹象，而不能单凭这些数字断言差异具有统计显著性或可推广到其他机器人环境。

<div class="result-source" markdown="1">

来源：Section VI-A, Table II

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

PACE achieves a 10% success rate (95% CI: [5.0%, 17.8%]) with the default configuration, representing a 67% relative improvement over the ReAct+Think baseline at 6% (95% CI: [2.5%, 12.0%]).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 以成功率为优先目标的 PACE-C 配置与全部参评方法对比

<div class="result-value" markdown="1">

PACE-C 达到 13% 成功率，95% 置信区间为 [7.2%, 21.4%]，作者称其为所有已评测方法中的最高成功率。

</div>

该结果说明 PACE 的预算策略可以配置为更偏重任务完成质量，而不仅是最低延迟；在 100 个实例上，13% 对应的成功数量仍然有限，且较宽的置信区间说明估计不确定性较大。由于所给章节没有完整列出 PACE-C 的耗时以及所有方法的表格行，这一结果只能支持“成功率点估计最高”，不能据此判断它在成功率—时间联合目标上必然最优。

<div class="result-source" markdown="1">

来源：Section VI-A, Table II

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The precision-optimized PACE-C configuration achieves 13% success rate (95% CI: [7.2%, 21.4%]), the highest among all methods evaluated.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### PACE 的推理时间效率与流水线重叠效果

<div class="result-value" markdown="1">

相对于无约束推理，PACE 的思考时间获得 6.9 倍加速；同时，66.8% 的思考时间被隐藏在动作执行窗口内。

</div>

这两项结果分别说明预算约束减少了思考耗时，以及交错架构把相当一部分剩余思考与机器人动作并行执行。直观地说，模型在机器人移动或操作期间继续准备后续决策，而不是让执行器等待全部推理结束。不过，隐藏率衡量的是时间重叠，不等价于端到端总完成时间缩短 66.8%；6.9 倍也针对思考时间，而非必然针对完整任务墙钟时间。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the Robotouille benchmark using Qwen3-8B-AWQ, PACE achieves a 10% success rate-representing a 67% improvement over the ReAct+Think baseline-while delivering 6.9 times acceleration in thinking time compared to unconstrained reasoning. The framework hides 66.8% of thinking time within execution windows, demonstrating that strategic cognitive effort allocation can simultaneously improve both planning quality and time efficiency.

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

- IO：一次模型推理直接生成完整计划，不接收执行过程中的环境反馈。它代表串行、开环规划范式，用于判断交错执行和反馈式重规划是否必要。
- IO+Think：在 IO 完整计划生成方式上开启推理模式。它检验仅增加扩展思考、但不改变串行架构，是否足以改善规划表现。
- ReAct+Think：在逐步推理—行动循环中启用扩展思考，是与 PACE 最直接的比较对象；两者都可逐步响应环境，但前者必须先完成当前推理再执行动作，不能系统地利用执行时间窗口。
- ReAct+Think(HB512)：将每轮推理硬性限制为固定的 512 个 token。它用于比较固定预算与 PACE 动态预算的差异，即预算是否应随动作执行窗口和任务状态自适应变化。

**实验想回答的问题**

- 在 Robotouille 的具身规划任务中，PACE 能否在缩短推理等待时间的同时，保持或提高任务成功率，从而改善成功率与总耗时之间的权衡？
- 交错推理—执行与动态推理预算能否把模型思考隐藏在动作执行窗口内，并使自适应预算优于无扩展思考、无约束思考和固定预算等替代方案？

**实验实现**

所有方法均使用相同的 Qwen3-8B-AWQ 模型与 vLLM 推理框架，并在 NVIDIA RTX 3090 GPU 上运行，以减少模型和硬件差异造成的混杂。实测生成速度约为每秒 150 token。PACE 从 ReActAgent 扩展，加入交错思考—行动循环与动态预算分配器。动作时长模型设置为导航 3.0 秒、操作 4.0 秒、处理 5.0 秒、填充 6.0 秒；预算参数包括最小预算 30 token、首步预算 50 token、0.2 秒额外开销和 30 token 输出预留。评测同时观察成功率和总完成时间，并用 Pareto 前沿识别不存在“成功率更低且耗时更长”的被完全支配方案。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过交错推理执行和动态推理预算分配提升具身规划的成功率与推理时效。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`66447e5935aaf65948e45f24d4f38a5347d6843f790e4b47d788ed2d5cce9eae`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
