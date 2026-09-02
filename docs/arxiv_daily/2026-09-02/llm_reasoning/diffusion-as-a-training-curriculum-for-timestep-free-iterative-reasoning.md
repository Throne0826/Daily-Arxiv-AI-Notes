---
title: "[论文解读] Diffusion as a Training Curriculum for Timestep-Free Iterative Reasoning"
description: "[arXiv 2609.01449][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2609.01449"
announcement_date: "2026-09-02"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:45:54.835544+00:00"
source_sha256: "2411d185f4812455ccd372d2ba191c15351797792181902407b7823c3062d1e5"
tags:
  - "LLM Reasoning"
  - "迭代方法"
  - "扩散模型"
  - "递归推理"
  - "持久隐藏状态"
  - "无时间步条件"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.01449</p>

# Diffusion as a Training Curriculum for Timestep-Free Iterative Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Mariia Drozdova, Aidan Sirbu, Pietro Miotti, Robert Obryk, Mayalen Etcheverry, Eyvind Niklasson, Blake Richards</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of Geneva；Affiliation: School of Computer Science, McGill University；Affiliation: Mila - Quebec AI Institute；Affiliation: Dept. of Neurology & Neurosurgery, McGill University；Affiliation: Montreal Neurological Institute, McGill University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.01449v1) · [PDF 下载](https://arxiv.org/pdf/2609.01449v1) · **关键词** 迭代方法, 扩散模型, 递归推理, 持久隐藏状态, 无时间步条件<br>


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

原文未明确报告。

**不用术语来说**：原文未明确报告。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 原文未明确报告。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于扩散模型与递归推理模型的交叉领域。扩散模型通常通过多步状态演化逐渐生成或恢复数据，信息主要由连续变化的采样状态传递；递归推理模型则通过重复使用同一个更新模块，并借助持久隐藏状态累积计算。本文关注的问题是：如果把持久隐藏状态加入扩散去噪器，并移除扩散时间步条件，扩散训练是否能够把该模型塑造成一个可运行任意深度的迭代求解器。研究在具有唯一答案的离散推理任务上展开，包括 Sudoku-Extreme 中的数独补全，以及 Maze-Unique/Maze-Hard 中从起点到终点的路径求解。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**扩散模型与去噪**

扩散模型通过逐步改变数据状态来完成生成或恢复；去噪器在每一步根据当前带噪状态预测更接近目标的数据。本文特别关注训练阶段的有序退火扰动，即逐渐改变腐蚀程度，而不是只把扩散看作推理时的采样过程。

</div>
<div class="concept-item" markdown="1">

**持久隐藏状态**

隐藏状态是网络内部用于保存中间计算结果的表示；持久隐藏状态会从一个迭代步骤传到下一个步骤，因此可以在不改变外部数据状态的情况下积累推理信息。本文将它与去噪预测分开，使同一更新模块能够反复执行。

</div>
<div class="concept-item" markdown="1">

**截断反向传播与任意深度推理**

截断反向传播只在有限长度的迭代片段内计算梯度，以降低训练成本；任意深度推理则允许测试时继续执行更新，即使执行步数超过训练时的反向传播窗口。本文检验有限训练展开是否足以支持更长时间的持续求解。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个决定唯一目标的任务输入，例如含有线索的数独棋盘或迷宫，模型需要输出唯一的完整解：数独的合法补全，或从起点到终点的路径。每一步中，网络接收当前数据表示以及上一轮产生的持久隐藏状态，使用同一个、且不接收扩散时间步或迭代编号的更新函数生成新的潜表示；该潜表示被分成两个分别归一化的视图，一个作为下一步的隐藏状态，另一个投影回数据空间形成当前去噪预测。隐藏状态不接受直接监督，只通过其对未来去噪预测的影响间接学习。研究还比较常规的渐进式去噪与最大腐蚀条件：后者在每一步都将非线索变量替换为新的高斯噪声，以测试求解是否依赖逐步降低噪声。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x_t$**

扩散或采样过程在状态索引 $t$ 处的数据状态；相关背景说明见论文第 1 节。

</div>
<div class="notation-item" markdown="1">

**$K$**

推理时执行的去噪或递归更新步数；论文第 1 节报告 Sudoku-Extreme 使用 $K=10{,}000$、Maze-Unique 使用 $K=100$ 的结果。

</div>
<div class="notation-item" markdown="1">

**$h$**

在迭代步骤之间持续传递的隐藏状态；论文第 1 节将其描述为与数据空间预测分离的信息通道。

</div>
<div class="notation-item" markdown="1">

**$x$**

扩散采样轨迹中的连续状态变量；论文第 1 节用其说明扩散模型主要通过演化中的状态传递信息。

</div>

</div>

**直接相关的工作**

- **Ho et al. (2020)；Song et al. (2020)**: 这些工作代表论文所采用的扩散模型背景：DDPM、DDIM 等方法通过扩散状态的逐步演化传递信息。本文保留扩散去噪训练的框架，但去除时间步条件，并额外加入持久隐藏状态，以研究扩散训练能否产生递归求解能力。
- **Graves (2016)；Banino et al. (2021)；Saunshi et al. (2025)**: 这些工作代表递归推理模型或循环计算路线，其核心是重复应用更新并在隐藏状态中累积计算。本文借鉴这一持久状态思想，将循环式更新器实例化为 Sudoku-Extreme 上的 looped Transformer，并与扩散去噪机制结合。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把扩散去噪器改造成无时间步条件的递归求解器。输入是带有固定线索的棋盘状态、线索嵌入和掩码；模型在每次递归更新中同时读取当前带噪观测与持久隐藏状态，经过共享的 Transformer 或局部卷积通信模块，输出去噪预测和下一隐藏状态。训练时使用从强噪声到干净目标的有序扩散轨迹，并只在短窗口内反向传播；推理时可运行任意深度，甚至始终保持最大噪声，使单条轨迹在观测空间探索、在隐藏状态中积累进度，最终稳定到解。直观地说，当前棋盘像一张会被反复扰动的草稿，隐藏状态像不会被擦掉的解题笔记；每轮模型依据两者修正答案，运行更久通常能继续改进。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造带噪并固定线索的输入

先按方差保持路径生成 $x_k=a(t_k)y+b(t_k)\varepsilon_k$，其中 $a(t_k)=\sin(\pi t_k/2)$、$b(t_k)=\cos(\pi t_k/2)$；再用 $\operatorname{Pin}$ 将线索位置替换回 $e$，使只有非线索单元被扰动。

<div class="method-step__io" markdown="1">

**输入**：干净目标表示 $y$、线索嵌入 $e$、线索掩码 $m\triangleq(m_i)_{i=1}^{N}\in\{0,1\}^{N}$、噪声参数 $t_k$ 和高斯噪声 $\varepsilon_k$。<br>
**输出**：固定给定线索、其余位置带有指定腐蚀程度的状态 $x_k$。

</div>

**直观理解**：模型不能修改题目已经给出的数字或迷宫墙壁；噪声只加在需要推断的格子上。$t_k=0$ 表示最大噪声，$t_k=1$ 表示干净状态。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 嵌入当前状态并循环计算

将固定后的状态经线性投影 $E_x$，与 $p$、$m\odot g$ 和 $h_k$ 相加，随后重复共享的预归一化模块 $B_\theta$ 共 $J=8$ 次，得到潜表示 $z_k$。Sudoku 使用同一行、列或 $3\times3$ 宫格内的注意力；迷宫使用局部卷积窗口。

<div class="method-step__io" markdown="1">

**输入**：带噪状态 $x_k$、上一轮隐藏状态 $h_k$、位置嵌入 $p$、给定单元标志 $g$ 以及任务专用通信掩码或卷积窗口。<br>
**输出**：表示当前求解进度的潜变量 $z_k$。

</div>

**直观理解**：先把棋盘翻译成模型能处理的向量，再让相关格子交换信息；循环使用同一个模块相当于让一个小型程序连续思考多轮。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分出记忆与去噪预测

通过独立的 LayerNorm 分支得到下一隐藏状态 $h_{k+1}=\operatorname{LN}_h(z_k)$，并通过另一 LayerNorm 及线性映射 $E_o$ 得到可观测预测 $\hat y_k=E_o(\operatorname{LN}_o(z_k))$。

<div class="method-step__io" markdown="1">

**输入**：潜表示 $z_k$。<br>
**输出**：持久记忆 $h_{k+1}$ 和当前去噪目标预测 $\hat y_k$。

</div>

**直观理解**：同一次计算产生两种结果：一份是留给下一轮的内部笔记，另一份是当前对完整答案的公开猜测。隐藏状态不直接计算损失，但承担跨轮传递未被噪声破坏的信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 递归更新并持续求解

按 $x_{k+1}=\operatorname{Pin}(a(t_{k+1})\hat y_k+b(t_{k+1})\varepsilon_{k+1},e,m)$ 构造下一观测，同时将 $h_{k+1}$ 传给下一轮；推理可以使用递减的退噪日程，也可以固定 $t$，固定噪声时在输出连续若干轮不变后停止。

<div class="method-step__io" markdown="1">

**输入**：预测 $\hat y_k$、下一噪声参数 $t_{k+1}$、新高斯噪声 $\varepsilon_{k+1}$、线索嵌入 $e$ 和掩码 $m$。<br>
**输出**：任意深度的预测轨迹以及最终解码结果。

</div>

**直观理解**：模型把上一轮答案重新变成下一轮的带噪草稿，但内部笔记保持连续。固定最大噪声并不是逐步擦除噪声，而是每轮重新探索，再依靠记忆逐渐稳定。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 方差保持扩散腐蚀路径

$$
x_k=a(t_k)y+b(t_k)\varepsilon,\qquad a(t_k)=\sin\!\left(\frac{\pi t_k}{2}\right),\qquad b(t_k)=\cos\!\left(\frac{\pi t_k}{2}\right)
$$

**符号说明**

- $x_k$：第 $k$ 次去噪时的带噪棋盘或网格状态。
- $y$：干净的目标表示，即完整数独解或迷宫目标路径表示。
- $t_k$：第 $k$ 步的噪声日程参数；$t_k=0$ 为最大腐蚀，$t_k=1$ 为干净数据。
- $\varepsilon$：高斯噪声。
- $a(t_k),b(t_k)$：分别控制目标信号和噪声的权重。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把目标和高斯噪声按 $t_k$ 混合，形成模型每轮看到的观测；训练中 $t_k$ 按从最大噪声到低噪声的有序轨迹变化。线索位置随后由固定操作恢复，因此腐蚀主要训练模型解决未知位置。<br>
**原文位置**：第 2 节“Problem and corruption path”，式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 掩码均方去噪目标

$$
\mathcal{L}=\frac{1}{L}\sum_{k=0}^{L-1}\frac{\sum_{i=1}^{N}(1-m_i)\left\|\hat{y}_{k,i}-y_i\right\|_2^2}{d\sum_{i=1}^{N}(1-m_i)}
$$

**符号说明**

- $\mathcal{L}$：训练损失。
- $L$：反向传播展开的去噪步数，本文使用 $L=4$。
- $N$：网格单元数量；数独为 $81$，迷宫为 $900$。
- $m_i$：第 $i$ 个单元是否为固定线索的二值掩码；线索为 $1$，待推断单元为 $0$。
- $\hat{y}_{k,i}$：第 $k$ 步对第 $i$ 个单元的预测。
- $y_i$：第 $i$ 个单元的干净目标。
- $d$：每个单元的特征维度。

<div class="equation-explanation" markdown="1">

**直观理解**：损失只比较非线索位置的预测与真实答案，并对 $L$ 个连续预测取平均；所以模型学习的是补全未知部分，而不是重新复制题目给出的部分。每轮都获得监督，使训练只需在短递归窗口内反向传播。<br>
**原文位置**：第 2 节“Training”，式（6）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标是上述掩码均方误差：对每个短展开步比较非线索位置的去噪预测 $\hat y_k$ 与目标 $y$，并在 $L=4$ 个步骤上平均。每个批次包含多个交错的持久 rollout；每条轨迹独立维护题目、腐蚀阶段、总长度 $K\sim\operatorname{Unif}[20,160]$ 和隐藏状态。虽然每次输入都从目标重新采样噪声，隐藏状态是跨步骤传递干净信息的唯一通道；截断反向传播结束后隐藏状态从计算图分离但继续保留，直到该 episode 结束。作者的关键解释是，有序递减腐蚀提供“逐步逆转腐蚀”的训练课程，而非必须在推理阶段执行的采样过程。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 持久隐藏状态与无时间步更新**

递归状态 $h_k$ 被加入每轮输入，并由 $h_{k+1}=\operatorname{LN}_h(z_k)$ 更新；网络参数在所有递归轮次共享，且网络不接收显式时间步条件。训练中不同轨迹具有不同长度 $K\sim\operatorname{Unif}[20,160]$，推理时可扩展到远长于训练展开长度的深度。

> 直观理解：隐藏状态使模型记住以前已经推断出的结构，因此当前噪声不会让它从零开始；取消时钟则让同一更新规则可以运行任意次数，而不是依赖预先规定的第几步。

**2. 任务专用空间通信**

共享递归计算链 $F_\phi$ 跨任务复用，但通信机制按任务改变：Sudoku 的注意力只连接同一行、列或局部宫格，Maze 使用迷宫网格上的局部卷积窗口。该设计将通用的递归更新与任务所需的空间归纳偏置分离。

> 直观理解：不同任务共享“如何反复更新”的方法，但使用不同的邻居关系：数独关注约束相关的格子，迷宫关注附近格子。

**3. 可变噪声观测通道**

每次观测 $x_k$ 可由有序退噪日程生成，也可在推理时固定在 $t=0$ 的最大腐蚀水平；噪声只作用于非线索变量，隐藏状态保持未被腐蚀。该机制使单条轨迹同时具有随机探索和记忆驱动的收敛能力。

> 直观理解：随机扰动帮助模型跳出错误候选，但不会抹掉内部进度；因此不需要并行生成许多答案、额外选择头或外部验证器。

**训练与推理**

训练时先为每条 rollout 采样长度和噪声阶段，从最大腐蚀到干净目标形成有序轨迹；每轮独立重新生成非线索位置的高斯腐蚀输入，调用共享递归去噪器得到 $(\hat y_k,h_{k+1})$，以掩码均方误差优化，反向传播仅穿过 $L=4$ 步。推理时令 $h_0=0$，非线索位置初始化为纯高斯噪声；模型输出 $\hat y_k$ 后按有序退噪公式重新加噪并固定线索，或将 $t$ 固定以进行持续随机强迫。运行深度 $K$ 可远超训练 rollout 和反向传播窗口；固定噪声模式下，当解码输出在预设 patience 窗口内不再变化时终止。

**复现信息**

复现或公平解读时需要保留：共享预归一化 Transformer 内循环次数采用 $J=8$；Sudoku 的注意力连接同一行、列和 $3\times3$ 宫格，Maze 使用局部卷积通信；线索通过 $\operatorname{Pin}(x,e,m)=(1-m)\odot x+m\odot e$ 始终固定。训练必须区分有序退火噪声、固定最大噪声、每步独立随机噪声和无噪声等 regime，因为原文报告固定噪声训练和无噪声训练会显著降级；推理阶段则不能据此假设必须退火，论文专门测试了固定最大噪声。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Sudoku-Extreme：约 $4.25\mathrm{M}$ 个具有唯一解的 $9\times9$ 数独，其中训练集约 $3.83\mathrm{M}$、留出测试集约 $423\mathrm{k}$；训练与测试题在数字重标记、宫或栈置换及转置等同构变换下仍保证数学不等价。输入以 $N=81$ 个格子表示，掩码固定题目给出的数字，模型预测其余格子。它用于检验深层约束传播和回溯式算法推理；消融实验仅在测试集的 $10\mathrm{k}$ 子集上进行。
- Maze-Unique：由 $1\mathrm{k}$ 个训练用的 $30\times30$ 迷宫构成，每个实例在起点与终点之间恰有一条有效路径；训练时在线应用二维正方形的 $8$ 种二面体对称变换。由于解唯一，精确匹配、路径有效和最短路径三个判据重合，因此该数据集适合直接检验迭代深度扩展能否迁移到空间路径搜索。
- Maze-Hard：包含环、死路以及多条可行路径的复杂 $30\times30$ 迷宫。每个网格有 $N=900$ 个位置，墙、起点和终点由掩码固定，模型需要在其余自由位置预测路径。该数据集通过区分精确、最优和有效求解，检验模型是否真正生成合法路径，而非仅复现数据集指定的标准答案。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**精确求解率（Exact solve）**

预测的整个数独答案或迷宫路径网格与目标逐格完全一致的实例比例。对 Sudoku-Extreme 和解唯一的 Maze-Unique，这是最严格且直接的整题成功指标；在 Maze-Hard 上，它会把不同于标准答案但仍合法的替代路径判错。 （越高越好，因为只有完整实例全部预测正确才计为成功。）

</div>
<div class="metric-item" markdown="1">

**最优求解率（Optimal solve）**

Maze-Hard 中预测路径既合法，又达到最短路径长度的实例比例；它允许预测与标准路径逐格不同，因此比精确求解率更能反映是否解决了路径规划问题。 （越高越好，因为它表示更多预测同时满足可行性与最短性。）

</div>
<div class="metric-item" markdown="1">

**有效求解率（Valid solve）**

Maze-Hard 中预测结果能形成从起点到终点的连续、无碰撞路径的实例比例，不要求路径最短，也不要求与标准答案相同。三项指标满足 $\mathrm{valid}\geq\mathrm{optimal}\geq\mathrm{exact}$。 （越高越好，因为它表示更多输出至少满足任务的基本路径约束。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Sudoku-Extreme 上增加测试时迭代深度

<div class="result-value" markdown="1">

作者报告精确求解率达到 $99.90\%$，并称准确率在远超训练展开长度和反向传播窗口的推理深度上仍持续提高。

</div>

这表明共享更新规则并非只能执行训练时见过的固定步数，而可被重复调用形成 anytime solver：若计算预算增加，完整解题成功率还能提升。该结果支持测试时深度外推，但单凭节选不能判断额外迭代的计算成本、收敛速度，也不能证明其对不同尺寸或分布外数独同样有效。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The result is an anytime solver: accuracy keeps improving with inference depth far beyond the rollout lengths and backpropagation window used in training, reaching 99.90% exact solve on Sudoku-Extreme.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Maze-Unique 的唯一解空间路径搜索

<div class="result-value" markdown="1">

作者报告 $98.93\%$ 的求解率；由于每个迷宫只有一条有效路径，该数值同时对应精确、有效和最优求解。

</div>

该结果说明迭代深度扩展不只适用于数独的全局离散约束，也能用于 $30\times30$ 网格上的局部信息传播。由于节选没有提供其他模型的同协议分数、方差或测试规模，不能据此量化相对已有方法的优势，也无法评估统计不确定性。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We also obtain 98.93% solve rate on Maze-Unique.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Sudoku-Extreme 消融协议下采用退火噪声与教师强制训练，并在测试时使用退火噪声

<div class="result-value" markdown="1">

在 $K=10{,}000$ 的评估设置和三个随机种子下，精确求解率为 $99.54\%\pm0.02$。

</div>

这一结果给出了训练课程消融中的完整方案参照点：极小的跨种子波动表明该设置在所测协议下较稳定。它与摘要中的 $99.90\%$ 不应直接混为同一实验，因为消融只评估测试集的 $10\mathrm{k}$ 子集，且节选未说明两者的推理深度和其他配置是否一致。

<div class="result-source" markdown="1">

来源：Appendix D, Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Annealed noise + teacher forcing | 99.54 ± 0.02

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

- 固定最大噪声训练：每个训练迭代都采用相同的最大扰动，而不按顺序退火；它直接检验“持续强噪声”本身是否足以学到求解器。
- 自由运行训练：将模型上一步预测重新加上较低一级噪声后作为下一步输入，不使用真实中间状态进行教师强制；它检验训练时暴露于自身预测是否能替代教师强制。
- 逐步独立采样噪声等级：每一步独立随机选择噪声等级，保留多噪声强度训练，但破坏噪声由强到弱的顺序；它用于隔离有序退火课程的重要性。
- 仅干净输入训练：训练期间不注入噪声；它检验普通的无扰动迭代监督能否自行形成可扩展的求解动态。

**实验想回答的问题**

- 去除扩散时间步条件、加入持久隐藏状态后，同一个共享迭代更新能否在测试时通过增加推理深度持续提高数独与迷宫的精确求解率，并迁移到局部通信的二维网格拓扑？
- 模型的推理能力究竟依赖测试时的渐进退火采样，还是主要来自训练时按顺序降低噪声并配合教师强制所形成的去噪课程？

**实验实现**

数独训练在线采用保持解不变的增强，包括以 $p=0.5$ 转置棋盘、随机置换数字，以及随机置换宫、宫内行、栈和栈内列；迷宫训练使用旋转与水平反射构成的 $8$ 种对称变换。训练课程消融采用 one-hot 可见状态编码，并以 $K=10{,}000$ 步进行测试；各方案在 Sudoku-Extreme 上训练和测试，报告三个随机种子的均值与波动，评估阶段统一使用退火噪声日程。因此该消融主要归因于训练制度差异，而不是测试采样制度差异。原文节选未给出优化器、批量大小、训练步数以及主结果所用测试集样本数。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 将有序退火训练替换为每一步独立随机采样噪声等级 | Sudoku-Extreme 精确求解率降至 $20.59\%\pm3.40$，相比完整方案的 $99.54\%\pm0.02$ 显著下降。 | 该对照仍让模型见到不同噪声强度，却取消了从高噪声到低噪声的顺序，因此主要隔离“有序课程”而非“是否存在噪声”。结果支持作者关于训练顺序至关重要的主张；不过不同方案的优化难度可能也不同，节选没有训练损失或收敛曲线来排除这一替代解释。 | Appendix D, Table 2<br><span class="experiment-evidence">i.i.d. Noise level per step \| 20.59 ± 3.40</span> |
| 训练时完全不进行输入噪声扰动（clean-only） | Sudoku-Extreme 精确求解率为 $0.00\%\pm0.00$，而完整的退火噪声加教师强制方案为 $99.54\%\pm0.02$。 | 这一对照检验普通的干净输入监督是否足以让迭代网络自行学会求解。零成功率说明，在当前架构和训练协议下，去噪扰动不是可随意删除的数据增强，而是形成有效迭代动态的关键训练信号；但它不证明所有无噪声递归模型都无法求解，因为架构、目标函数或训练策略改变后结论可能不同。 | Appendix D, Table 2<br><span class="experiment-evidence">Clean-only \| 0.00 ± 0.00</span> |

**定性案例**

- 定性行为方面，作者称即使测试时始终保持最大扰动、每一步都把所有非线索变量替换为新高斯噪声，单条轨迹仍能探索解空间并最终稳定到正确答案。其解释是持久隐藏状态承担跨步记忆，因此可见变量持续被重置也不会完全抹去推理进度；但所给章节没有展示具体轨迹、棋盘案例或逐步收敛图，仍需查阅原文图表核验。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该论文研究基于扩散训练课程的迭代式数独和迷宫推理，但并非语言模型或多模态模型推理，现有 taxonomy 没有通用推理类别。; rule check: matched taxonomy keywords; top rule score=6.0
- 全文指纹：`2411d185f4812455ccd372d2ba191c15351797792181902407b7823c3062d1e5`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
