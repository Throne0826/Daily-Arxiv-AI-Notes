---
title: "[论文解读] RMBench: Memory-Dependent Robotic Manipulation Benchmark with Insights into Policy Design"
description: "[arXiv 2603.01229][机器人 / 具身智能] 本文针对机器人在长时程操作中难以保留并调用历史信息、且现有研究缺少统一评测与机制分析的问题，以任务记忆复杂度、RMBench基准和模块化策略Mem-0建立从任务刻画到架构消融的系统研究框架。"
arxiv_id: "2603.01229"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T05:30:51.441389+00:00"
source_sha256: "ea320d7992b9d2149c2ec406f950aee94219a14f23189139daa1f4dd6cec5f42"
tags:
  - "机器人 / 具身智能"
  - "机器人操作"
  - "记忆依赖任务"
  - "长期记忆"
  - "模仿学习"
  - "任务记忆复杂度"
  - "RMBench"
  - "Mem-0"
  - "双臂操作"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2603.01229</p>

# RMBench: Memory-Dependent Robotic Manipulation Benchmark with Insights into Policy Design

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Chen, Tianxing, Wang, Yuran, Li, Mingleyang, Qin, Yan, Shi, Hao, Li, Zixuan, Hu, Yifan, Zhang, Yingsheng, Wang, Kaixuan, Chen, Yue, Wang, Hongcheng, Wang, Junjie, Yang, Tianhang, Xu, Renjing, Wu, Ruihai, Mu, Yao, Yang, Yaodong, Dong, Hao, Luo, Ping</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> MMLab, The University of Hong Kong；Peking University；PsiBot；The Hong Kong University of Science and Technology (Guangzhou)；Tsinghua University；Shenzhen University；Shanghai Jiao Tong University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2603.01229) · [PDF 下载](https://arxiv.org/pdf/2603.01229) · **关键词** 机器人操作, 记忆依赖任务, 长期记忆, 模仿学习, 任务记忆复杂度, RMBench, Mem-0, 双臂操作<br>
**代码**: [https://github.com/robotwin-Platform/rmbench](https://github.com/robotwin-Platform/rmbench) · **项目页**: [https://RMBench.github.io](https://RMBench.github.io)

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

本文针对机器人在长时程操作中难以保留并调用历史信息、且现有研究缺少统一评测与机制分析的问题，以任务记忆复杂度、RMBench基准和模块化策略Mem-0建立从任务刻画到架构消融的系统研究框架。

**不用术语来说**：现实中的机器人不能只看眼前画面做决定：物体可能已被遮挡，关键线索可能只在较早时出现，后续动作还可能取决于之前尝试过什么。例如，机器人需要记住先前放置物体的位置，或在多次尝试中保留已经获得的信息。许多现有策略只接收最近一小段观测，因此一旦关键线索离开输入窗口，就可能无法继续正确执行任务。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出任务记忆复杂度，作为刻画机器人操作任务之记忆需求的原则性指标；据此构建RMBench，在RoboTwin 2.0上设置9个具有不同记忆复杂度的双臂操作任务，为大规模、受控的记忆能力评测提供平台。
- 提出模块化记忆策略Mem-0，通过双系统架构和任务阶段分类器组织长时程记忆使用，并利用可替换、可重配置的组件开展系统消融，以分析锚点记忆、滑动记忆和关键记忆等设计对记忆性能的作用。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于机器人操作与模仿学习研究：策略依据相机观测、机器人状态和任务指令生成动作，使机械臂完成物体抓取、放置等操作。多数现有策略只接收固定长度的近期观测，并近似假设当前观测已包含决策所需信息；然而在记住先前放置位置、跨阶段保留线索等任务中，关键内容可能长期不可见，策略必须从历史中选择性保存、检索并利用信息。本文因此关注“记忆依赖型机器人操作”的统一评测，并在 RoboTwin 2.0 仿真平台上构建包含 9 个双臂任务的 RMBench，以不同任务记忆复杂度考察策略的长期信息保持与使用能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**马尔可夫性与非马尔可夫任务**

若当前观测足以支持正确决策，可近似视为马尔可夫任务；若未来动作还依赖较早但当前已不可见的观察或行为，则属于本文所说的非马尔可夫、记忆依赖型任务。

</div>
<div class="concept-item" markdown="1">

**模仿学习**

模仿学习利用专家示范训练机器人从观测直接预测动作，而非主要依靠奖励试错。RMBench强调可用于一般模仿学习策略的评测，而不仅针对强化学习方法。

</div>
<div class="concept-item" markdown="1">

**视觉—语言—动作策略**

视觉—语言—动作策略将视觉观测和语言任务指令映射为机器人动作，常通过大规模机器人数据预训练以增强泛化能力。本文指出，这类策略即使操作能力较强，若只使用固定长度的观测历史，仍可能无法处理长期记忆需求。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是在仿真及真实机器人环境中执行长时程操作的策略。策略接收当前与有限历史的视觉观测、机器人状态及任务指令，并输出双臂机器人后续动作；任务设置会使早期出现的关键信息在后续阶段不再可见，因此不能假设当前观测完整描述任务状态。评测目标不是单纯检验动作精度或任务长度，而是检验策略能否跨较长时间保留、检索并用于决策的任务相关信息；RMBench通过 9 个具有不同任务记忆复杂度的任务进行分层和受控比较。本文同时引入模块化策略 Mem-0，借助双系统架构和任务阶段分类器研究不同结构选择如何影响记忆表现。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **MemoryBench**: 同样评测带有记忆需求的机器人操作，包含 7 个单臂任务；但据本文作者所述，其中只有 3 个任务能够在仿真中可靠复现，且缺少原则化的任务设计指导，因此不足以支持稳定、分层的系统分析。
- **MIKASA**: 提供 32 个记忆相关操作任务，覆盖面较大；但其任务表述主要面向强化学习，而 RMBench旨在形成更适合一般机器人策略、尤其是模仿学习策略的记忆能力评测设置。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

真实机器人操作普遍具有非马尔可夫性，即当前可见信息不足以唯一决定正确动作，较早的观测与动作可能在很久之后仍影响决策。机器人因而必须跨越较长时间保留、检索并使用任务相关信息；否则，在目标被遮挡、状态发生变化或任务包含多次尝试时，即使局部操作能力很强，也可能因遗忘关键线索而失败。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **固定长度近期观测策略**：Pi0.6、RDT2等现代操作策略主要面向短时程任务和精细动作，通常把最近一段固定长度的视觉或状态观测输入策略，并近似假设当前决策所需信息都包含在该窗口内。
- **显式记忆策略与已有记忆相关基准**：MemoryVLA、MemER、CronusVLA和SAM2Act等方法向操作策略加入显式记忆机制，以支持长时程或依赖历史的决策；MemoryBench、MIKASA和LIBERO-Long则分别通过记忆任务、强化学习式任务或长时程任务评测相关能力。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 固定长度观测窗口隐含近似马尔可夫假设，只能利用有限的近期信息；当决定后续动作的线索早已离开窗口时，策略难以记住物体位置、先前动作或多次尝试的结果，因而不适合真正的长期记忆任务。
- 已有评测平台未同时满足可复现、原则化任务设计和对通用模仿学习策略适用的要求：MemoryBench的7个单臂任务中只有3个能在仿真中可靠复现，且缺少任务设计原则；MIKASA的32个任务主要面向强化学习；LIBERO-Long虽有10个长时程任务，但任务相关信息始终可见，因而不明确要求记忆。其后果是不同策略难以在受控条件下公平比较，也无法可靠归因具体架构组件的作用。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尽管已有方法开始加入记忆模块，领域仍缺少一套能够明确刻画任务记忆需求、覆盖多个复杂度层级并支持受控实验的操作基准；同时，现有研究尚未解释哪些架构选择真正改善了信息的长期保留与调用，以及这些选择为何有效。

</div>
<div markdown="1"><span>核心问题</span>

如何以原则化方式定义并构造不同记忆复杂度的机器人操作任务，并在统一、可复现的实验平台上判断现有策略的记忆能力，以及锚点记忆、滑动记忆、关键记忆和任务阶段划分等架构设计分别如何影响长期记忆表现？

</div>
<div markdown="1"><span>作者直觉</span>

先按任务必须跨越多长时间、保留哪些历史线索来划分记忆难度，可以避免把“执行步骤很多”误当成“确实需要记忆”；再用阶段分类器识别机器人当前处于任务的哪一部分，并让不同记忆组件分别保存稳定参照、近期上下文和关键事件，就能更有结构地选择相关历史。由于Mem-0将这些组件模块化，逐项替换或移除后观察性能变化，便可把整体效果更清楚地归因到具体设计。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文的方法由“任务侧的记忆复杂度定义”和“策略侧的显式记忆实现”两部分组成。首先，作者把机器人操作建模为部分可观测马尔可夫决策过程，并以任务记忆复杂度（Task Memory Complexity, TMC）刻画最优决策至少需要保留多少个与任务相关的历史观察；据此构建包含九项任务的 RMBench。随后提出 Mem-0：规划模块根据初始图像、全局指令及已完成子任务的关键帧记忆生成下一子任务；执行模块利用当前观察、子任务文本、固定锚点记忆和短期滑动记忆，通过扩散 Transformer 预测动作块；子任务结束分类器检测执行边界，并把结束图像写回规划记忆，形成闭环。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 任务记忆复杂度标注与数据组织

依据 TMC 定义，寻找使某个最优策略仅依赖当前记忆状态即可决策的最小历史观察数 $m$，并将任务标为 $M(0)$、$M(1)$ 或 $M(n)$。RMBench 据此组织五个 $M(1)$ 任务和四个 $M(n)$ 任务，并在 RoboTwin 2.0 与 SAPIEN 中统一生成数据和评测。

<div class="method-step__io" markdown="1">

**输入**：机器人任务的观察—动作历史 $h_t=(o_{1:t},a_{1:t-1})$，以及为获得最优决策可能需要保留的任务相关历史观察。<br>
**输出**：具有明确记忆需求等级的九项仿真操作任务，以及与动作—观察对齐的细粒度语言标注。

</div>

**直观理解**：这一步不是按轨迹长度判断任务难度，而是问“要做对下一步，至少必须记住几个关键往事”。因此可以把任务本身的记忆需求与某一种具体网络架构分开评价。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于关键帧记忆的子任务规划

规划视觉语言模型 $\mathcal{V}_{\text{plan}}$读取上述信息并生成下一条文本子任务 $s_t$。规划只在上一子任务被判定结束时调用，而不是每个控制时刻都调用，因此在总时长为 $T$、子任务数为 $N$ 且 $N\ll T$ 时，调用量由 $O(T)$ 降为 $O(N)$。

<div class="method-step__io" markdown="1">

**输入**：回合初始 RGB 观察 $o_0$、全局任务指令 $g$，以及此前所有已完成子任务及其结束观察构成的关键记忆 $\mathcal{M}_{t-1}$。<br>
**输出**：供低层执行模块遵循的当前子任务描述 $s_t$。

</div>

**直观理解**：规划器类似一名查看任务清单和关键完成照片的主管：它先确认过去做过什么、结果如何，再下达下一条指令，而不必在机器人每移动一次时重新思考全局计划。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 双时间尺度记忆融合与动作块生成

执行视觉语言模型分别编码图像和文本并进行均值池化；当前图像表示以交叉注意力读取锚点记忆与滑动记忆，所得两个记忆增强表示再与文本表示拼接为条件向量 $\mathbf{c}_t$。扩散 Transformer 在该条件下去噪并预测长度固定为 $H=30$ 的动作序列，实际执行其中长度为 $\Delta$ 的前缀后再次更新控制。

<div class="method-step__io" markdown="1">

**输入**：当前 RGB 观察 $o_t$、当前子任务 $s_t$、子任务起点的锚点记忆 $\mathcal{A}$、最近 $K$ 个视觉表示构成的滑动记忆 $\mathcal{S}_t$，以及带高斯噪声的候选动作序列。<br>
**输出**：去噪动作块 $\hat{\mathbf{a}}_{t:t+H-1}$及实际下发的动作前缀 $\hat{\mathbf{a}}_{t:t+\Delta-1}$。

</div>

**直观理解**：锚点记忆像始终摆在桌上的“子任务开始照片”，用于防止忘记最初目标；滑动记忆像只保留最近几页的工作日志，用于理解刚刚发生的变化。动作块则让模型一次规划一小段连续运动，而不是逐个动作孤立预测。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 子任务结束检测与闭环更新

轻量 MLP 输出当前子任务是否结束；只有连续 $L=8$ 个时刻均预测结束，系统才确认边界，以减少瞬时噪声导致的提前终止。确认后，系统将当前子任务 $s_t$与结束观察 $o_t^{\mathrm{end}}$写入关键记忆，清空锚点和滑动缓冲区，并重新调用规划模块。

<div class="method-step__io" markdown="1">

**输入**：每个控制时刻的融合条件向量 $\mathbf{c}_t$及结束分类器最近若干时刻的二元输出。<br>
**输出**：可靠的子任务终止信号、更新后的关键记忆，以及下一轮规划—执行循环的触发信号。

</div>

**直观理解**：系统不会因为一次偶然判断就宣布任务完成，而要连续八次得到同样结论。完成后保存一张“结果照片”和对应工作名称，使高层规划器能够根据真实执行结果继续安排后续步骤。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 任务记忆复杂度定义

$$
\exists\,\pi^{*}\ \text{s.t.}\ \pi^{*}(a_t\mid h_t)=\pi^{*}(a_t\mid\mathcal{M}_t^{(m)}),\quad\forall t
$$

**符号说明**

- $\pi^{*}$：能够实现任务最优决策的策略。
- $a_t$：时间步 t 执行的机器人动作。
- $h_t$：截至时间步 t 的完整交互历史，即观察序列与此前动作序列。
- $\mathcal{M}_t^{(m)}$：由完整历史构造、至多编码 m 个任务相关历史观察的记忆状态。
- $m$：满足该等价决策条件的最小非负整数，即任务记忆复杂度。
- $t$：交互时间步；等式要求对所有时间步成立。

<div class="equation-explanation" markdown="1">

**直观理解**：该式要求：即使不把完整历史交给策略，只提供由至多 $m$个关键历史观察构成的记忆，仍能产生与某个最优策略相同的动作分布。满足条件的最小 $m$就是任务自身所需的最低记忆容量；它衡量的是关键历史信息数量，而非必须保存最近多少个连续帧。<br>
**原文位置**：第 3.1 节，公式 (2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 记忆条件化的扩散动作预测

$$
\hat{\mathbf{a}}_{t:t+H-1}=\mathrm{DiT}\!\left(\mathbf{a}_{t:t+H-1}^{\epsilon},\mathbf{x}_t,\mathbf{c}_t\right)
$$

**符号说明**

- $\hat{\mathbf{a}}_{t:t+H-1}$：模型预测的、从时间步 t 开始且长度为 H 的去噪动作序列。
- $\mathrm{DiT}$：用于动作序列去噪生成的扩散 Transformer。
- $\mathbf{a}_{t:t+H-1}^{\epsilon}$：由真实动作序列加入高斯噪声得到的带噪动作序列。
- $\mathbf{x}_t$：时间步 t 的扩散过程状态或相关输入；节选未进一步定义其具体组成。
- $\mathbf{c}_t$：由锚点记忆增强视觉表示、滑动记忆增强视觉表示和子任务文本表示拼接得到的条件向量。
- $H$：动作预测时域，本文固定为 30。

<div class="equation-explanation" markdown="1">

**直观理解**：扩散模型从一段被噪声扰动的动作开始，在当前扩散状态和多模态记忆条件的指导下恢复可执行动作。关键点不只是生成长度为 $H$的动作块，而是去噪过程同时参考任务语言、子任务起点和近期视觉历史，使动作对历史状态保持一致。<br>
**原文位置**：第 4.2 节，公式 (8)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：所给章节说明执行模块以真实动作序列加高斯噪声，并训练 DiT 预测对应的去噪动作序列；规划模块通过 LoRA 微调视觉语言模型以学习基于关键记忆的子任务推理，结束分类器学习二元终止判断。然而，节选没有明确给出扩散损失、语言建模损失、分类损失及其加权组合公式，因此不能据此断言使用了哪一种具体噪声预测参数化或损失权重。可确定的优化关系是：规划监督使模型输出下一子任务，动作监督使执行模块恢复动作块，边界监督使分类器识别子任务结束，三者在推理时通过记忆写入和边界触发组成闭环。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 关键记忆规划模块**

采用视觉语言模型进行子任务级推理，输入为固定的初始观察 $o_0$、全局目标 $g$和关键记忆 $\mathcal{M}_{t-1}=\{(s_i,o_i^{\mathrm{end}})\}_{i=1}^{t-1}$。关键记忆同时保存已完成子任务的语言描述与其视觉结果，使规划器可追踪按钮按压次数、试错记录等跨子任务状态。

> 直观理解：仅看当前画面可能无法知道已经尝试过哪些对象或重复操作了几次；保存“做过什么”和“做完后看到什么”可以避免重复尝试，并支持依赖长期历史的下一步推理。

**2. 锚点—滑动双记忆执行模块**

锚点记忆 $\mathcal{A}$在子任务开始时写入首帧视觉潜变量，并在整个子任务内保持不变；滑动记忆 $\mathcal{S}_t$逐步追加当前视觉潜变量，只保留最近 $K$ 项。当前视觉表示分别通过交叉注意力读取两类记忆，再与文本表示共同条件化扩散 Transformer。

> 直观理解：固定锚点保留“从哪里开始、原本是什么样”，短期窗口保留“刚才发生了什么”。两者互补，使模型既能比较当前状态与起点，也能利用近期运动趋势，而且不必把每个难以语言描述的空间细节都拆成子任务。

**3. 子任务结束分类器**

该模块是作用于条件向量 $\mathbf{c}_t$的轻量 MLP，输出 $\mathcal{C}_{\text{end}}(\mathbf{c}_t)\in\{0,1\}$。系统以连续八帧一致的结束预测作为真正边界，并在边界处负责关键帧写入、执行记忆清空和下一次规划触发。

> 直观理解：它是高层规划与低层控制之间的“交接开关”。若没有可靠边界，规划器可能在动作尚未完成时过早换指令，或在任务已经完成后继续执行并造成漂移。

**训练与推理**

训练时，规划模块以 Qwen3-VL-8B-Instruct 为基础，使用 LoRA 针对单项任务微调，使其能读取初始观察、任务目标和已完成子任务关键记忆；执行模块也采用逐任务从头训练。执行训练在批内并行产生 VLM token 和 DiT 动作块，但锚点与滑动记忆融合必须按每个回合的时间顺序串行进行；系统为各回合维护跨批次全局记忆结构，以避免打乱帧顺序后丢失历史。节选没有明确说明规划器、执行器与结束分类器是否端到端联合优化，因此应理解为模块化训练流程，而不应自行推断联合损失。

推理时，系统先由规划器根据 $o_0$、$g$和当前关键记忆生成 $s_t$；执行模块把子任务首帧写入锚点记忆，并持续更新最近 $K$项的滑动记忆。每个控制周期，DiT 预测 $H=30$步动作并执行长度为 $\Delta$的前缀，同时结束分类器检查是否连续八帧判定完成；若未完成则继续执行和更新短期记忆，若完成则将 $(s_t,o_t^{\mathrm{end}})$加入关键记忆、清空执行记忆并规划下一子任务，直至全局任务结束。

**复现信息**

RMBench 构建于 RoboTwin 2.0 和 SAPIEN，支持自动数据合成与统一策略评测，并提供动作—观察级语言标注。规划模块使用 Qwen3-VL-8B-Instruct、LoRA 秩 8、批量大小 16、学习率 $1.0\times10^{-4}$和 25 个 epoch；每个任务使用 8 张 NVIDIA A800 训练约半小时。执行模块对每个任务从头训练 30,000 次迭代，使用 8 张 A800、全局批量大小 448 和 AdamW；视觉输入缩放至 $224\times224$，VLM 与记忆库使用 bfloat16，其余模块使用 float32，每项任务训练约 18 小时。这些设置表明表中不同任务对应独立训练的策略实例，而不是一个统一的九任务模型；同时，记忆融合要求轨迹时间顺序完整，是复现时比普通随机帧采样更关键的实现约束。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- RMBench 仿真基准：包含 9 个机器人操作任务，并按记忆结构区分为 $M(1)$ 与 $M(n)$。前者不进行子任务分解，主要检验执行模块在单阶段任务中保持历史信息的能力；后者在关键决策点进行子任务分解，联合检验规划模块和执行模块。每个任务使用 50 条专家示范训练，并以 100 次 rollout 的成功率评估。主要实验运行于 SAPIEN；原文还说明 RMBench 已在 NVIDIA Isaac Lab-Arena 上实现，但未给出该平台上的独立结果。
- Mem-0 消融实验：沿用 RMBench 的全部两类任务。$M(1)$ 任务只消融锚点记忆和滑动记忆，因为该类任务不启用子任务分解；$M(n)$ 任务进一步消融规划模块中的关键记忆，并以仿真器提供的真实终止信号替换子任务结束分类器，从而分别定位长期规划信息与阶段切换判断的影响。
- 真实机器人数据：在 X-One 双臂平台上选取与 RMBench 对齐的 Put Back Block、Rearrange Blocks 和 Cover Blocks 三项任务。每项任务采集 100 条真实示范，训练后执行 40 次 rollout；该设置用于检验仿真结论在真实感知噪声、人工示范差异和精细操作误差下是否仍成立，原文未明确报告训练集与测试集之外的额外划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务成功率**

在固定次数 rollout 中完整满足任务成功条件的比例。该指标同时受历史信息利用、子任务规划、终止判断和低层动作精度影响，因此能衡量端到端完成能力，但不能单独诊断失败来自哪个模块。 （越高越好，因为更高比例表示策略在更多独立试验中完成了整个任务；对于多阶段任务，任一阶段失败都可能使整次 rollout 记为失败。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### RMBench 仿真总体比较：Mem-0 对比 DP、ACT、Pi0.5 和 X-VLA

<div class="result-value" markdown="1">

作者报告，相对基线，Mem-0 在 $M(1)$ 任务上的平均成功率提高 38.4%，在 $M(n)$ 任务上提高 21.2%。这表明显式记忆在多数需要保留历史线索的任务中具有显著价值；但节选未给出 Table 1 的完整逐任务分数，也未明确该“提高”是百分点、相对增幅还是相对哪一种基线计算。

</div>

直观而言，只看当前画面的策略可能不知道先前展示了哪个目标、物体原来位于哪里，或某一步是否已经完成；Mem-0 将关键历史信息带入后续决策，因此总体成功率更高。该结果支持“显式记忆有用”，但不能证明 Mem-0 在所有任务上都最佳，也不能排除参数规模、训练方式或模块容量差异的影响。

<div class="result-source" markdown="1">

来源：Section 5.1, Table 1 discussion

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On average, Mem-0 improves success rates by 38.4% on M(1) tasks and 21.2% on M(n) tasks relative to the baselines, underscoring the critical role of memory modules in addressing memory-dependent manipulation in RMBench.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 真实 X-One 双臂机器人：三项任务的平均成功率

<div class="result-value" markdown="1">

三项真实任务的平均成功率为 ACT 0.00%、Pi0.5 5.83%、Mem-0 22.50%；Mem-0 分别高出 22.50 和 16.67 个百分点。逐任务上，Mem-0 在 Put Back Block、Rearrange Blocks 和 Cover Blocks 中分别达到 17.5%、37.5% 和 12.5%，均高于两种基线。

</div>

这说明 Mem-0 的相对优势并未完全依赖仿真环境，在真实视觉变化和动作误差下仍能体现。不过其绝对成功率只有 22.50%，不能据此认为真实部署问题已解决；而且只有三项任务、单一机器人平台，每项 40 次试验，原文也未报告置信区间。

<div class="result-source" markdown="1">

来源：Table 3, Average row

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Average
0.00%
5.83%
22.50%

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Mem-0 在不同任务类型上的边界与失败

<div class="result-value" markdown="1">

Mem-0 并非全面领先：强语义理解的 Observe and Pick Up 中，预训练模型仍有优势；精细放置任务 Swap T 的提升有限；Press Button 的成功率为 0%，主要瓶颈是微小按压造成的视觉变化难以被子任务结束分类器稳定识别。

</div>

实验把“记住历史”与“看懂对象、精确控制、判断动作是否完成”区分开来。显式记忆能解决历史信息缺失，却不能自动补足视觉语义预训练、精细运动控制或触觉反馈。因此总体平均提升不应被解读为所有机器人能力均得到改善。

<div class="result-source" markdown="1">

来源：Section 5.1; Table 1 discussion

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In the Press Button task, the small magnitude of individual press actions further complicates reliable termination detection: the Subtask End Classifier may fail to consistently recognize task completion, causing repeated presses or missed contacts and ultimately zero success.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 结果覆盖 9 个仿真任务和 3 个真实任务，但真实实验仅使用 X-One 双臂平台，每任务 40 次 rollout；原文未报告随机种子方差、置信区间或显著性检验，因此小幅差异的稳定性和跨平台泛化仍需验证。
- Mem-0 的主要瓶颈包括目标语义辨识、精细抓取与放置、按钮状态感知及子任务终止判断。特别是纯视觉分类器难以识别微小状态变化，而模型又缺少专门的机器人操作预训练、触觉和本体感觉输入；因此实验支持显式记忆的价值，但尚不能证明当前架构足以处理真实世界中的精细长时序操作。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- DP：非预训练基线，用于比较仅由当前观测预测动作、且不依赖大规模预训练或显式记忆的操作策略。
- ACT：非预训练基线；既参与 RMBench 仿真比较，也参与真实机器人实验，因此可用于判断 Mem-0 的优势是否来自显式记忆架构，而非仅来自同一平台上的训练条件。
- Pi0.5：预训练机器人策略，代表大规模预训练带来的语义理解与运动先验；它尤其适合检验显式记忆是否能在总体上超过预训练，以及在目标辨识等强语义任务上是否仍存在短板。
- X-VLA：预训练视觉—语言—动作策略，作为另一类预训练方法参与仿真比较，用于避免结论只依赖单一预训练基线。所有基线均不采用 Mem-0 的子任务分解。

**实验想回答的问题**

- 现有非预训练策略、预训练策略与显式记忆策略 Mem-0 在不同记忆复杂度的 RMBench 任务上表现如何；显式保存历史信息能否缓解仅依赖当前观测的马尔可夫式策略在非马尔可夫任务中的失败？
- Mem-0 的锚点记忆、滑动记忆、关键记忆和子任务结束分类器分别解决什么问题；该架构从仿真迁移到真实双臂机器人后，是否仍具有相对优势？

**实验实现**

仿真实验对每个任务和每种 $M(1)$、$M(n)$ 设置统一使用 50 条专家示范训练，并评估 100 次 rollout。Mem-0 在 $M(1)$ 中关闭子任务分解，结果主要反映执行模块；在 $M(n)$ 中由规划模块在关键决策点推断子任务，再由执行模块完成动作。基线不做子任务分解。真实实验中，每项任务使用 100 条示范并评估 40 次。论文还报告，子任务结束分类器使 Mem-0 只在必要时触发高层规划：其规划频率约为 5–10 Hz，而每时刻进行高层推理的 MemER 约为 1–2 Hz；但节选未提供统一硬件、时延或统计置信区间，因而不能据此作严格的效率显著性比较。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除锚点记忆（w/o Anchor） | 在 $M(1)$ 任务中，完整模型平均成功率为 52.8%，移除锚点记忆后降至 26.8%，下降 26.0 个百分点；Rearrange Blocks、Put Back Block 和 Swap Blocks 分别从 89%、90%、67% 降至 73%、35%、15%。 | 该消融隔离了“长期固定保存任务关键线索”的作用。滑动窗口仍存在，但关键观测会随时间被淘汰，因此策略后来可能忘记目标或初始状态。明显下降支持锚点记忆对长期保留信息的重要性；不过 Observe and Pick Up 均为 4%，说明仅有锚点机制并不能解决语义辨识问题。 | Table 2, $M(1)$ w/o Anchor row<br><span class="experiment-evidence">w/o Anchor
4%
73%
35%
15%
7%
26.8%</span> |
| 以仿真器真实终止信号替换子任务结束分类器（GT Classifier） | 在 $M(n)$ 任务中，完整模型平均成功率为 28.5%，使用真实终止信号后达到 45.3%，提高 16.8 个百分点；Blocks Ranking Try 从 18% 升至 45%，Press Button 从 0% 升至 14%。 | 该实验不改变规划模块和执行模块的主要能力，而是用理想的阶段完成信号替换学习式分类器，因此主要测量错误切换时机造成的损失。提升说明子任务分解有潜力，现有分类器却限制了该潜力；同时 45.3% 仍不高，表明即使切换完全正确，感知、规划和精细动作仍会失败。 | Table 2, $M(n)$ GT Classifier row<br><span class="experiment-evidence">GT Classifier
30%
45%
92%
14%
45.3%</span> |

**定性案例**

- Press Button 展示了纯视觉记忆的边界：按钮按下前后的视觉差异极小，分类器可能在未按成功时误报结束，也可能在已经成功后继续重复按压。Figure 10 将两种错误分别呈现为 insufficient presses 与 excessive presses。作者据此建议加入本体感觉或触觉反馈；分析上，这意味着问题不仅是“记不记得”，还包括输入中是否存在足够可辨识的完成信号。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文构建记忆依赖型机器人操作基准，并提出带显式记忆模块的操作策略用于分析。; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`ea320d7992b9d2149c2ec406f950aee94219a14f23189139daa1f4dd6cec5f42`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
