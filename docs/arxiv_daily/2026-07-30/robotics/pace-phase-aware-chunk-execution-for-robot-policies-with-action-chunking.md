---
title: "[论文解读] PACE: Phase-Aware Chunk Execution for Robot Policies with Action Chunking"
description: "[arXiv 2606.00537][机器人 / 具身智能] 本文指出动作分块机器人策略的执行时域会以任务相关且非单调的方式显著影响成功率，并提出无需训练的 PACE，根据预测动作块中的低速谷值在线选择重规划时机。"
arxiv_id: "2606.00537"
announcement_date: "2026-07-30"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:25.220154+00:00"
source_sha256: "232a02219197aa1528698d8df8963929e25f583e1e95b810850254235dbcc5e7"
tags:
  - "机器人 / 具身智能"
  - "机器人策略"
  - "动作分块"
  - "执行时域"
  - "滚动重规划"
  - "开环执行"
  - "测试时执行"
  - "视觉—语言—动作模型"
  - "扩散策略"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2606.00537</p>

# PACE: Phase-Aware Chunk Execution for Robot Policies with Action Chunking

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Junnan Nie, Jiayi Li, Jiachen Zhang, Junyi Lao, Chenghao Liu, Tianle Zhang, Liang Lin, Songfang Huang</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2606.00537v2) · [PDF 下载](https://arxiv.org/pdf/2606.00537v2) · **关键词** 机器人策略, 动作分块, 执行时域, 滚动重规划, 开环执行, 测试时执行, 视觉—语言—动作模型, 扩散策略  


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

本文指出动作分块机器人策略的执行时域会以任务相关且非单调的方式显著影响成功率，并提出无需训练的 PACE，根据预测动作块中的低速谷值在线选择重规划时机。

**不用术语来说**：机器人策略一次通常会预测未来一小段连续动作，但部署者仍须决定机器人实际连续执行多少步后再观察环境。执行太短会频繁打断本来连贯的动作，执行太长又可能让机器人迟迟不能根据环境变化纠错；而且合适的步数会随任务乃至操作阶段改变，因此不能可靠地用一个固定值解决。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将“执行时域”明确为动作分块策略部署中的关键独立变量，并通过固定时域扫描表明，成功率随该变量呈任务相关、非单调变化，因而单一固定时域不是可靠的跨任务默认规则。
- 作者提出即插即用的测试时方法 PACE：仅分析策略已经输出的动作块，在预测速度曲线中寻找代表操作阶段转换的低速谷值，并据此在线确定执行前缀；该方法不需要重训练、辅助输入、额外学习模块或策略内部信号。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于机器人策略的测试时执行研究。视觉—语言—动作模型与扩散式机器人策略常采用“动作分块”：策略根据当前观测一次预测一段未来动作，以提高局部运动的连续性；机器人只执行其中一个前缀，随后获取新观测并重新规划。因此，预测块有多长（预测时域）与实际连续执行多少步（执行时域）是两个不同变量。现有策略主要改进动作块的生成质量，而部署时通常将执行时域固定为常数；本文关注的正是给定已预测动作块后，应在何处停止开环执行并重新查询策略。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**动作分块（action chunking）**

策略每次不是只输出下一步动作，而是输出一个按时间排列的未来动作序列。它能让短时间内的运动更连贯，但仍需额外决定该序列实际执行到哪里。

</div>
<div class="conceptitem" markdown="1">

**执行时域（execution horizon）**

每次策略查询后，机器人在再次观察环境和重新规划之前连续执行的动作步数。较短时域提高反馈与纠错频率，较长时域则减少对连贯局部运动的打断，但会延迟对环境变化的响应。

</div>
<div class="conceptitem" markdown="1">

**滚动时域／重规划（receding-horizon replanning）**

机器人执行当前预测序列的一部分后，基于最新观测再次预测动作块，如此循环推进任务。已执行部分通常是开环的，即执行期间不利用新观测修正该前缀。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

在每个重规划时刻，已有机器人策略接收当前观测，并输出长度由策略决定的未来动作块；部署规则需要从该块中选择前缀长度 h_i，机器人开环执行此前缀后再采集观测、查询策略。研究设定假定执行时域并非策略训练所学习或规定的量，且不同任务、不同操作阶段可能需要不同长度；目标是在不修改或重训底层策略、不访问注意力图、置信度或去噪状态等内部信息的条件下，仅利用预测动作块在线确定 h_i。这里需要区分：预测时域限定策略一次能预测多远，执行时域限定机器人在闭环反馈介入前真正走多远。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$H$**

固定执行时域，即每次重规划前恒定执行预测动作块的前 H 个动作。

</div>
<div class="notationitem" markdown="1">

**$h_i$**

第 i 次策略查询后在线选出的执行时域，可随动作块及操作阶段变化。

</div>
<div class="notationitem" markdown="1">

**$i$**

滚动执行过程中的策略查询或重规划轮次索引。

</div>

</div>

**直接相关的工作**

- **ACT**: ACT 推广了面向精细双臂模仿学习的动作分块，并通过时间集成组合相互重叠的预测。它代表了动作块生成与固定测试时执行规则的既有路线，而本文研究预测完成后应执行多长前缀这一互补问题。
- **AutoHorizon**: AutoHorizon同样在线选择执行时域，是与本文设定最接近的工作，但依赖流式视觉—语言—动作模型内部的动作自注意力。PACE拟将该问题改写为策略无关的外部执行问题，只读取预测动作块，因而不要求特定模型结构或内部信号。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

视觉—语言—动作模型和扩散式机器人策略常通过动作分块一次预测多个未来动作，以保持局部运动连续性；但动作块的预测长度并不规定实际应执行多少步。部署时必须额外选择执行时域，即机器人在重新获取观测并查询策略之前执行的动作数。该选择直接控制闭环反馈频率与开环运动连续性之间的权衡，因此会影响接触、抓取、对准和释放等操作能否可靠完成。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **固定执行时域**：在整段任务中使用常数 H：每次策略预测一个动作块后，机器人固定执行其前 H 个动作，再获取新观测并重新规划。较小的 H 提高反馈和纠错频率，较大的 H 则更完整地执行连续局部运动。
- **离线经验调参与时域扫描**：在部署前尝试多个固定 H，并依据特定任务的实验表现选择一个经验值；它仍然把选出的时域作为整段执行过程中的常数，而不根据当前动作块或操作阶段动态调整。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 固定 H 强迫不同运动阶段采用相同重规划间隔：H 太小时可能打断连贯动作，太大时又会延迟基于新观测的纠错。作者报告，在三个 RoboTwin2.0 任务上将 H 从 1 扫描到 50 时，成功率呈明显非单调变化；例如 Click bell 在 H≈6 附近达到峰值，在 H≈25 附近下降近 40 个百分点，随后在 H≈35 附近再次出现峰值。这意味着固定值可能落入性能骤降区间。证据位置：第1节 Introduction、图1。证据原文：“Sweeping H from 1 to 50 on three RoboTwin2.0 tasks, we observe that the success rate is strongly non-monotonic in H and that the preferred horizon is highly task-dependent. On Click bell, for instance, the success rate peaks near H≈6, drops by nearly 40 points around H≈25, and rebounds to a second peak near H≈35.”
- 离线扫描所得最优时域依赖具体任务，难以迁移到新任务或真实机器人环境，也不能适应同一回合中接近、接触、操作和释放等阶段对反馈频率的不同需求；因此增加调参成本仍不能形成可靠的通用部署规则。证据位置：第1节 Introduction。证据原文：“An offline sweep does not resolve this problem either, since the best horizon identified on one task does not transfer to new tasks or to real-robot deployment.”

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有动作分块策略学习了要预测哪些未来动作，却没有学习或规定每个动作块实际执行到哪里；部署端也缺少一种能够依据当前预测内容、随操作阶段变化而在线确定重规划边界，同时不依赖任务专属调参、额外训练或策略内部访问的通用执行机制。

</div>
<div markdown="1"><span>核心问题</span>

能否只利用策略当前预测的动作块，在测试时为每次查询在线选择执行前缀长度，从而在保留连贯运动的同时，于需要反馈的阶段转换附近及时重新观测和规划？

</div>
<div markdown="1"><span>作者直觉</span>

操作轨迹通常由若干运动学上连贯的阶段构成，例如先接近物体、减速对准、接触抓取，再移动和释放；阶段交界处常伴随减速，因此会在预测速度曲线上形成低速谷值。若机器人执行到最早可信谷值便重新查询策略，就相当于让一个连贯动作阶段尽量完整执行，并在下一个阶段开始前刷新观测，而不是机械地每隔固定步数打断动作。作者同时限定了这一假设的适用范围：若关键决策点没有体现为低速谷值，或预测轨迹速度噪声较大，该信号可能变弱；此外，PACE 只能改善已有动作的执行时机，不能补足基础策略根本未生成的操作能力。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PACE 是一种用于动作分块机器人策略的测试时执行规则。基础策略在第 i 次查询时根据当前观测和语言指令预测长度为 L 的动作块；PACE 不改变动作预测本身，而是从各机械臂的预测运动中构造并平滑一维速度曲线，检测具有足够显著度的低速谷值，将其视为潜在的操作阶段边界，并选择最早边界作为本轮执行长度。机器人仅执行该长度对应的动作前缀，丢弃剩余后缀，再用新观测查询策略；若没有可靠边界，则执行至预设最大长度 H_{\max}。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 预测动作块

策略一次输出长度为 L、动作维度为 d_a 的动作序列 \mathbf{A}_i=(a_{i,1},\ldots,a_{i,L})。PACE 保持策略及其训练时预测长度不变，仅读取该动作块。

<div class="method-step__io" markdown="1">

**输入**：第 i 次查询时刻 \tau_i 的机器人观测 o_{\tau_i}、语言指令 \ell，以及已训练的动作分块策略 \pi_\theta。  
**输出**：当前查询对应的预测动作块 \mathbf{A}_i\in\mathbb{R}^{L\times d_a}。

</div>

**直观理解**：策略先给出未来一小段完整动作计划，PACE 再决定其中多少步可以放心地连续执行，而不是重新生成动作。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 提取并平滑机械臂速度曲线

对每个机械臂组 b，算子 \psi_b 从动作块的机械臂运动分量构造一维速度序列 \mathbf{v}_i^b=(v_{i,1}^b,\ldots,v_{i,L-1}^b)，再由平滑算子 \mathcal{S} 得到 \tilde{\mathbf{v}}_i^b=\mathcal{S}(\mathbf{v}_i^b)。平滑用于抑制短程波动，避免产生虚假的局部极小值。

<div class="method-step__io" markdown="1">

**输入**：预测动作块 \mathbf{A}_i，以及实际执行的机械臂组集合 \mathcal{B}。  
**输出**：每个执行机械臂组的平滑预测速度曲线 \tilde{\mathbf{v}}_i^b。

</div>

**直观理解**：这一步把高维动作计划压缩成随时间变化的“快慢曲线”；去除细小抖动后，真正的减速位置更容易识别。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 检测阶段边界并选择执行长度

PACE 在每条曲线的前 H_{\max} 步内寻找满足最小时间间隔约束的低速谷值，并以显著度 \Phi_i^b(r) 衡量候选 r 相对周围运动是否体现了明显减速；达到阈值的候选在各机械臂间取并集。若存在候选，则选择最早者；否则令执行长度为 H_{\max}。

<div class="method-step__io" markdown="1">

**输入**：各机械臂的平滑速度曲线、最大执行长度 H_{\max}、最小候选时间间隔，以及由训练示范校准的任务级阈值 \delta_{\mathcal T}。  
**输出**：本轮执行视野 h_i\in\{1,\ldots,H_{\max}\}。

</div>

**直观理解**：明显减速通常对应接触准备、对齐、抓取、释放或稳定等阶段切换，因此应在越过该位置前重新观察。多臂任务选择任一机械臂最早出现的可靠边界，避免某只机械臂继续依据过时观测跨越关键阶段。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 执行动作前缀并重新规划

机器人依次执行前缀 (a_{i,1},\ldots,a_{i,h_i})，丢弃未执行后缀，并将下一次策略查询时刻更新为 \tau_{i+1}=\tau_i+h_i。上述过程在任务执行期间循环进行。

<div class="method-step__io" markdown="1">

**输入**：预测动作块 \mathbf{A}_i 和选定的执行长度 h_i。  
**输出**：执行后的机器人状态、新观测，以及下一轮策略查询。

</div>

**直观理解**：连贯运动阶段可以一次多走几步以减少重复规划；接近阶段切换时则较早停下来，用新观测重新决定后续动作。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 动作分块策略与执行时序

$$
\mathbf{A}_{i}=\pi_{\theta}(o_{\tau_{i}},\ell)\in\mathbb{R}^{L\times d_{a}},\qquad \mathbf{A}_{i}=(a_{i,1},\ldots,a_{i,L}),\qquad \tau_{i+1}=\tau_i+h_i
$$

**符号说明**

- $i$：策略查询的序号。
- $\pi_\theta$：参数为 \theta 的已训练动作分块机器人策略。
- $o_{\tau_i}$：查询时刻 \tau_i 的机器人观测。
- $\ell$：任务的语言指令。
- $\mathbf{A}_i$：第 i 次查询预测的完整动作块。
- $L$：策略的预测视野，即每个动作块包含的动作数。
- $d_a$：单个动作向量的维度。
- $a_{i,j}$：第 i 个动作块中的第 j 个预测动作。
- $h_i$：本轮实际执行的动作数量，即执行视野。
- $\tau_i$：第 i 次策略查询对应的时间步。

<div class="equation-explanation" markdown="1">

**直观理解**：策略虽然一次预测 L 步，但机器人不必全部执行；它只执行前 h_i 步，然后在时刻 \tau_i+h_i 获取新观测并重新查询。PACE 的核心不是改变预测动作，而是按动作块内容动态决定 h_i。  
**原文位置**：第 3.1 节，式 (1)；查询时序紧随式 (1) 后给出。

</div>

</div>

<div class="equation-block" markdown="1">

#### 跨机械臂候选聚合与阶段感知执行视野

$$
\mathcal{R}_{i}=\bigcup_{b\in\mathcal{B}}\left\{r\in\mathcal{V}_{i}^{b}:\Phi_{i}^{b}(r)\geq\delta_{\mathcal{T}}\right\},\qquad h_{i}=\begin{cases}\min\mathcal{R}_{i},&\mathcal{R}_{i}\neq\emptyset,\\ H_{\max},&\mathcal{R}_{i}=\emptyset,\end{cases}\qquad H_{\max}\leq L
$$

**符号说明**

- $\mathcal{B}$：当前任务中实际执行动作的机械臂组集合。
- $\mathcal{V}_i^b$：机械臂组 b 的平滑速度曲线中检测到的候选低速边界集合。
- $r$：动作块内某个候选重规划边界的位置。
- $\Phi_i^b(r)$：候选 r 在机械臂组 b 的速度曲线上的谷值显著度，用于衡量减速相对周围运动是否足够突出。
- $\delta_{\mathcal T}$：任务 \mathcal T 的候选接受阈值，由训练示范一次性校准。
- $\mathcal{R}_i$：所有执行机械臂中通过显著度阈值的候选边界并集。
- $h_i$：PACE 为当前动作块选择的实际执行长度。
- $H_{\max}$：允许连续执行的最大动作数，且不超过动作块预测长度 L。

<div class="equation-explanation" markdown="1">

**直观理解**：只要任一机械臂出现可靠的低速阶段边界，PACE 就在所有可靠候选中选择最早的位置，以便在关键运动转换前更新观测；若曲线中没有明显转换，则执行较长前缀 H_{\max}。该规则实现了“转折处短执行、连贯运动中长执行”。  
**原文位置**：第 3.3 节，候选聚合公式及其后的分段执行视野公式。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：PACE 不包含可学习参数，也不增加或修改基础策略的训练损失。其任务级显著度阈值 \delta_{\mathcal T} 仅使用训练示范进行一次性校准；作者明确说明该过程不使用评测轨迹、成功标签或固定执行视野扫描，因此它是规则参数校准而非对策略进行梯度训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 机械臂运动剖面模块**

对每个执行机械臂组使用算子 \psi_b，将预测动作块中对应的机械臂运动分量转换为长度 L-1 的标量速度曲线，再通过 \mathcal{S} 平滑。原文节选未进一步给出 \psi_b、速度计算方式及 \mathcal{S} 的具体形式。

> 直观理解：模块只保留判断运动阶段所需的速度变化，使系统无需理解动作块中的全部高维细节；平滑则防止微小预测噪声被误判为需要重规划的边界。

**2. 低速谷值与显著度筛选模块**

模块从每条平滑速度曲线提取候选集合 \mathcal{V}_i^b，并以 \Phi_i^b(r) 评价候选低速谷相对于周围运动的减速显著程度；仅保留满足 \Phi_i^b(r)\geq\delta_{\mathcal T} 的候选。最小时间间隔约束用于避免过密候选，任务级阈值依据训练示范校准且评测期间固定。

> 直观理解：单纯速度低并不一定代表阶段转换，例如整段动作都可能很慢；显著度要求该位置相对前后确实形成明显“谷底”，从而减少无意义的频繁查询。

**3. 跨机械臂保守边界聚合模块**

单臂任务只处理被执行的一个机械臂；多臂任务将所有执行机械臂达到阈值的候选合并，并选取全局最早候选作为 h_i。若候选集合为空，则回退到满足 H_{\max}\leq L 的最大允许执行长度。

> 直观理解：双臂协作中，只要一只手即将进入抓取或接触等新阶段，就应提前刷新观测；没有发现关键转折时，则允许较长的连续执行以保留动作连贯性。

**训练与推理**

训练阶段沿用原有基础策略 \pi_\theta 的训练流程，PACE 不参与策略优化；所给节选未报告基础策略的具体损失。部署前，使用训练示范为每个任务校准阈值 \delta_{\mathcal T}，随后在整个评测中固定。推理时，每次基础策略输出动作块后，PACE 分别提取各执行机械臂的速度曲线并平滑，检测低速谷值、计算显著度并跨机械臂聚合候选；机器人执行至最早可靠边界，若没有候选则执行至 H_{\max}，之后丢弃动作块后缀、获取新观测并重复查询。整个过程仅访问策略输出的动作块，不要求访问策略内部结构，也不重新训练基础策略。

**复现信息**

复现时必须保持基础策略原有预测长度 L，并设定不超过 L 的最大执行长度 H_{\max}；还需按任务从训练示范校准 \delta_{\mathcal T}，评测时不得利用成功标签或固定视野扫描重新调参。候选检测需要速度曲线平滑、低速谷值提取、最小时间间隔约束和谷值显著度筛选；多臂场景必须对所有实际执行的机械臂分别处理并选取最早边界。所给章节未明确报告速度算子 \psi_b、平滑算子 \mathcal S、显著度 \Phi_i^b、最小间隔及阈值校准算法的具体计算形式或参数值，完整复现这些细节仍需核对论文其余附录或代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- RoboTwin2.0仿真基准：包含50个双臂操作任务，覆盖不同持续时间和时序需求。每个任务单独训练一个预测长度为L=50的π0.5检查点；主要比较在全部50项任务上进行，六个代表性任务用于展示分任务结果及训练预测长度消融。其作用是大规模检验执行规则能否跨不同操作任务稳定有效。
- RoboChallenge真实机器人基准：在双臂ALOHA上评测stack_bowls与put_pen_into_pencil_case。两项任务分别使用1047和1220条示范进行微调，每种执行方法、每项任务运行30次。前者强调重复抓取、搬运和精确堆叠，后者强调双臂协作、顺序依赖与接触敏感操作；公共提示、复位和评分规则用于增强可复现性。
- place_object_on_plate实验室任务族：在单臂Franka上把玉米、卷心菜、青椒、红椒或大蒜放入目标盘，五种物体共享一个由301条示范微调得到的π0.5检查点。每种物体、每种方法评测20次，共100次，作用是检验PACE能否从双臂公共基准迁移到单臂、跨物体的真实部署场景。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**任务成功率（Success Rate）**

仿真中由RoboTwin2.0任务成功谓词判定；真实实验中的Succ.只统计完整完成任务的试验比例。它衡量端到端任务是否真正完成，而不奖励中间进展。 （越高越好，因为更高数值表示完整达到任务目标的试验占比更大。）

</div>
<div class="metricitem" markdown="1">

**Score**

RoboChallenge的0–100部分得分：若第n次试验得分为p_n、单次满分为P_max=10、总试验数为N，则Score=100·(1/(NP_max))·∑_{n=1}^N p_n。它可反映打开容器、抓取物体或完成堆叠等中间进展；Franka二元任务中Score与成功率相同。 （越高越好，因为它表示平均完成了更多评分步骤，但高Score不一定意味着完整成功率同样高。）

</div>
<div class="metricitem" markdown="1">

**50任务平均成功率**

先对每个RoboTwin2.0任务的九个评测批次求任务级成功率，再对50个任务等权平均，是仿真实验的主要汇总指标；等权设计避免高样本量任务支配总体结果。 （越高越好，因为它表示执行规则在完整任务集合上的平均可靠性更强。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 50项RoboTwin2.0仿真任务的总体比较

<div class="result-value" markdown="1">

PACE将50任务平均成功率从57.8%提高到64.2%，绝对提升6.4个百分点，约为11.1%的相对提升。

</div>

由于各方法共享策略检查点和输入，该差异主要支持“自适应执行前缀优于单一固定执行规则”的作者主张，而不是模型容量或训练数据更多带来的收益。结果覆盖50项任务，说明收益并非仅来自单个案例；但所给节选未报告置信区间或显著性检验，因此不能据此判断所有任务上都存在统计显著提升。

<div class="result-source" markdown="1">

来源：Abstract；仿真设置与汇总指标定义见第4节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">On 50 RoboTwin2.0 tasks, PACE raises the average success rate from 57.8% to 64.2%.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 三项真实机器人设置的平均结果

<div class="result-value" markdown="1">

PACE将平均Score从60.7提高到77.7，并将平均完整成功率从50.7%提高到70.4%，分别增加17.0分和19.7个百分点。

</div>

Score和完整成功率同时提升，说明PACE不仅让失败轨迹推进得更远，也提高了最终完整完成任务的比例。比较横跨双臂ALOHA公共基准和单臂Franka实验室任务，支持其跨平台适用性；但三项任务的简单平均规模较小，尚不能证明对其他机器人、策略架构或更广泛任务均可泛化。

<div class="result-source" markdown="1">

来源：第5.1节，Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Averaged over the three real-robot evaluations, PACE raises the Score from 60.7 to 77.7 and Succ. from 50.7% to 70.4%.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 单臂Franka的place_object_on_plate五物体任务族

<div class="result-value" markdown="1">

PACE把表现从72.0%提高到88.0%，绝对提升16.0个百分点；该任务中Score与Succ.相同。

</div>

这一结果专门表明改进并不局限于双臂ALOHA或RoboChallenge评分体系：在共享单一检查点、覆盖五种物体且采用二元成败判定时，PACE仍有明显提升。它测试的是执行规则跨机器人形态和物体变体的迁移，而不是跨策略模型的迁移。

<div class="result-source" markdown="1">

来源：第5.1节，Table 5；任务与试验规模见附录E.1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">On the Franka place_object_on_plate task family, where Score and Succ. are identical, PACE improves performance from 72.0% to 88.0%.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验主要基于π0.5策略，且任务内共享检查点只能证明收益来自执行规则差异，不能证明PACE对其他视觉—语言—动作模型、扩散策略、动作表示或控制频率具有同等效果；原文节选未提供跨策略架构的直接对照。
- 真实机器人证据仅包括三项设置，其中两项任务各30次、Franka共100次；节选也未报告置信区间、显著性检验、额外策略查询带来的计算延迟或失败类型汇总。因此，虽然观察到较大提升，仍需更广任务覆盖和不确定性分析来确认稳定性及部署成本。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 固定短执行长度H=5：每次只执行预测动作块前5步便重新观测和规划，用于检验高频闭环反馈是否足以取得最佳结果。
- 固定中等执行长度H=25：在反馈频率与连续开环运动之间取固定折中，用于比较自适应选择是否优于一个看似合理的全局中间值。
- 固定整块执行H=50：执行完整预测块后才重新查询策略；它最大化动作连续性但也最易受陈旧观测和误差累积影响，并作为真实机器人实验中的直接基线。
- 训练预测长度消融中的固定H_eval执行：对每个测试执行长度保持H_eval不变，仅改变训练时监督预测长度H_train，用于排除重规划频率变化并单独测量长序列监督的作用；这不是独立的新策略，而是机制分析对照。

**实验想回答的问题**

- 在保持策略检查点、观测、语言指令和预测动作块完全相同的条件下，PACE依据动作块内部运动结构在线选择执行长度，是否比固定执行长度更能提高仿真与真实机器人任务的完成表现？
- PACE的收益是否来自对不同操作阶段采用不同重规划频率，以及训练时预测长度、测试时执行长度等设计因素如何影响动作分块策略的表现？

**实验实现**

仿真中，所有方法在每个任务上共享同一π0.5检查点、观测和语言指令，仅改变每个预测动作块在重新规划前执行多少步。固定基线取H∈{5,25,50}，且不按任务单独调参；PACE从相同预测块在线选择前缀，其阈值仅由训练示范校准，不使用评测轨迹、成功标签或固定长度扫描结果。完整协议对每个任务—方法组合使用3个随机种子，每个种子运行3批、每批100回合，即900回合；50任务结果按任务等权平均。真实实验同样在任务内共享微调检查点和输入，仅比较H=50整块执行与PACE：两项ALOHA任务各30次，Franka五种物体各20次。训练预测长度消融因需重新训练，仅在六个代表任务上使用种子0，每个设置运行3批100回合；同一行固定H_eval，只改变H_train，且H_train<H_eval因预测动作不足而不可行。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 训练预测长度H_train与测试执行长度H_eval解耦消融：六个代表任务上固定H_eval，仅增加H_train | 相对于每行最短可行训练长度H_train=H_eval，更长训练长度带来的成功率增益在H_eval=10、15、20时最高分别达到+20.7、+13.0和+6.6个百分点。 | 该消融保持实际执行和重规划频率不变，因此隔离出训练时长动作序列监督的贡献。结果说明，即使只执行较短前缀，让模型联合预测更长未来仍可能改善前缀质量；同时增益从20.7降至6.6，支持“执行前缀越长，额外未来监督对已执行动作的边际帮助越小”的解释。由于只覆盖六项任务、单个随机种子，数值不宜直接视为50任务总体效应。 | 附录C.2，Figure 7<br><span class="experiment-evidence">For example, the gain reaches +20.7 at H_eval=10, +13.0 at H_eval=15, and +6.6 at H_eval=20.</span> |
| 极短测试执行长度H_eval=5下的训练预测长度敏感性 | 当H_eval=5时，大多数更长H_train设置的变化接近零或为负，未呈现其他非平凡执行长度下的普遍增益。 | 该对照表明“训练时预测越长越好”并非无条件成立。每5步就重新查询时，性能更受高频观测反馈支配，长未来联合监督的优势被削弱；这也帮助区分PACE的收益来源——关键不是单纯延长训练目标，而是在测试时选择适合当前阶段的执行长度。原文在该句中未给出H_eval=5各单元格的具体数值。 | 附录C.2，Figure 7<br><span class="experiment-evidence">Second, H_eval=5 is an exception: most entries in this row are near zero or negative.</span> |

**定性案例**

- 成功的真实ALOHA stack_bowls轨迹中，PACE在接近和搬运阶段选择27、30、31步的长执行段；进入对位敏感的堆叠阶段时缩短为7步，以尽快利用新观测修正误差；对齐后又扩展到43步。该案例直观展示了“平滑运动少查询、接触转换多反馈”的阶段自适应机制，但它只是成功个例，不能单独证明这种模式在所有轨迹中都出现。证据位置：第5.2节，Figure 5。原文："During approach and transport, PACE selects long horizons (27, 30, and 31 actions), allowing the robot to preserve continuous motion while open-loop execution remains reliable. Near the contact-sensitive stacking phase, where small pose errors can determine whether the bowls align correctly, the horizon contracts to 7 actions so that the next query can incorporate an updated observation. After this alignment phase, the horizon expands again to 43 actions, showing that PACE does not remain in a high-frequency replanning mode once a coherent motion segment becomes available."

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出面向动作分块机器人策略的训练免测试时方法，依据运动阶段动态选择执行与重规划时机。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`232a02219197aa1528698d8df8963929e25f583e1e95b810850254235dbcc5e7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
