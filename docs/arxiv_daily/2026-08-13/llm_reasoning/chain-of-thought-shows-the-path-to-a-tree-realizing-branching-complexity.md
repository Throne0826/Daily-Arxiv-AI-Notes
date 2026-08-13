---
title: "[论文解读] Chain-of-Thought Shows the Path to a Tree: Realizing Branching Complexity"
description: "[arXiv 2608.11716][LLM Reasoning] 本文要把“线性步数的链式思维能够表达更强计算”这一抽象复杂度结论变成可检查的具体构造：先用小深度硬注意力 Transformer 显式实现图遍历，再以遍历为计算底座求树的 Strahler 数与宽度，并考察这些能力在树和 Dyck 路径两种表示之间能否迁移。"
arxiv_id: "2608.11716"
announcement_date: "2026-08-13"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-13T02:54:37.505970+00:00"
source_sha256: "f76d12c619bdd99c4830f6b1827ca9133ad7b0bd677c785d03a13ff330bef3cb"
tags:
  - "LLM Reasoning"
  - "链式思维"
  - "Transformer 表达能力"
  - "唯一硬注意力"
  - "深度优先搜索"
  - "Dijkstra 算法"
  - "Strahler 数"
  - "树宽度"
  - "Dyck 路径"
  - "分支复杂度"
  - "NC^1"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.11716</p>

# Chain-of-Thought Shows the Path to a Tree: Realizing Branching Complexity

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-13</span>
<span><strong>作者</strong> Debanjan Dutta, Anish Chakrabarty, Swagatam Das</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Debanjan DuttaIndian Statistical InstituteKolkata, IndiaAnish ChakrabartyLTCI, Télécom ParisPalaiseau, France</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.11716v1) · [PDF 下载](https://arxiv.org/pdf/2608.11716v1) · **关键词** 链式思维, Transformer 表达能力, 唯一硬注意力, 深度优先搜索, Dijkstra 算法, Strahler 数, 树宽度, Dyck 路径, 分支复杂度, NC^1<br>


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

本文要把“线性步数的链式思维能够表达更强计算”这一抽象复杂度结论变成可检查的具体构造：先用小深度硬注意力 Transformer 显式实现图遍历，再以遍历为计算底座求树的 Strahler 数与宽度，并考察这些能力在树和 Dyck 路径两种表示之间能否迁移。

**不用术语来说**：已有理论说明，固定层数的 Transformer 如果允许逐步输出中间结果，就可能完成单次前向计算无法完成的递归任务，但这种理论通常没有说明模型究竟应在每一步寻找哪个节点、保存什么状态以及如何完成回溯。本文选择树的分支复杂度作为检验对象：模型需要真正沿树移动并汇总局部信息，才能判断一棵树的递归分支难度和各层最大规模，而不能只依靠一次全局模式匹配。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 给出 DFS 与 Dijkstra 的显式 CoT 实现，将图遍历落实为至多两层、两个注意力头的唯一硬注意力解码器；其中 Dijkstra 还包含 BFS 这一特例，从而补上既有 CoT 表达力理论所依赖但未构造的遍历机制。
- 把遍历作为共享计算底座，在一般有序多叉树及其 Dyck 路径表示上分别构造 Strahler 数和树宽度的 CoT 实现；同时指出，两种表示虽由显式双射联系，派生量的实现机制和层数却不能直接照搬，由此提出 CoT 可实现性是否对双射换表示或函数复合封闭的问题。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于 Transformer 表达能力与链式思维（Chain-of-Thought, CoT）计算复杂度的交叉领域。固定深度 Transformer 的单次前向计算能力受到限制，例如文中所采用的唯一硬注意力模型在无 CoT 时只能覆盖较低的复杂度范围；自回归 CoT 则把中间结果写成后续步骤可读取的 token，使固定深度解码器能够通过多步生成执行算法。已有理论把 CoT 步数与复杂度类联系起来，例如对数步和线性步分别对应 $\textsf{L}$ 与 $\textsf{NC}^1$，但这种类别层面的“可计算性”并未充分给出显式、层数受限的遍历程序。本文选取树的分支复杂度作为具体问题：Strahler 数刻画递归分支合并的难度，树宽度刻画同一深度上的最大节点数；前者在二叉树项表示下是 $\textsf{NC}^1$-完全问题，因此适合作为线性 CoT 表达能力的非平凡实例。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**链式思维计算**

这里的 CoT 不是自然语言解释，而是自回归解码器逐步产生中间 token，并在下一步把此前输出作为计算状态重新读取。因而 CoT 步数可视为算法运行时间，而每一步仍由层数固定的 Transformer 完成。

</div>
<div class="concept-item" markdown="1">

**唯一硬注意力**

硬注意力在每个注意力头中直接选取最高分位置，而不是对所有位置做加权平均；“唯一”表示最高分位置唯一。本文在这种受限模型中构造算法，并且不依赖层归一化或位置编码，以突出计算能力来自 CoT 迭代本身。

</div>
<div class="concept-item" markdown="1">

**树的分支复杂度**

Strahler 数通过自底向上的递归规则衡量多个同等复杂子树汇合时产生的额外复杂度，也对应求值算术表达式所需的最少寄存器数等经典量；树宽度则是各层节点数的最大值。二者分别强调递归合并难度和横向并行规模，是相互独立的结构指标。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入主要有两种等价表示：一是具有 $n$ 个顶点的任意有序树 $G_T$，二是通过深度优先遍历得到的 Dyck 路径；图遍历部分还考虑一般图以及 Dijkstra 算法所需的带权图。模型是在逐步自回归生成的 CoT 设置下运行、深度固定的唯一硬注意力 Transformer 解码器，每一步可读取输入及此前生成的中间状态。基础任务是显式实现 DFS 和 Dijkstra，其中 BFS 是 Dijkstra 的特例；在此基础上，目标输出包括遍历序列、树与 Dyck 路径之间的展开或重建结果，以及树或路径表示上的 Strahler 数 $\\str(G_T)$ 和宽度 $\\wid(G_T)$。作者研究的不只是这些量是否存在某种 Transformer 实现，还要求给出明确的层数、注意力头数和 CoT 步数上界，并比较同一组合对象更换表示后是否能够直接复用计算机制。文中构造面向任意多叉有序树，不限于已知复杂度结论所针对的二叉树，也不使用层归一化或位置编码。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$G_T$**

作为输入的有序树；文中同时讨论二叉树和更一般的任意多叉树。

</div>
<div class="notation-item" markdown="1">

**$n$**

输入树的顶点数；相关构造的 CoT 步数以此计量。

</div>
<div class="notation-item" markdown="1">

**$\str(G_T)$**

树 $G_T$ 的 Strahler 数，即反映递归分支合并复杂度的秩。

</div>
<div class="notation-item" markdown="1">

**$\wid(G_T)$**

树 $G_T$ 的宽度，即所有深度层中节点数的最大值。

</div>

</div>

**直接相关的工作**

- **文献 31 的按步数划分的 CoT 复杂度框架**: 该工作把对数 CoT 步与 $\textsf{L}$、线性 CoT 步与 $\textsf{NC}^1$ 联系起来，为本文判断 Strahler 数应落在线性步制度提供理论坐标；但它主要给出复杂度类别层面的可能性结论，没有提供本文所需的显式 DFS、Dijkstra 和分支复杂度解码器构造。
- **文献 6 的 Ehrenfeucht–Haussler 秩刻画**: 该工作证明 EH 秩等于单层硬注意力解码器所需的最少 CoT 步数，并在证明中使用穷举树遍历；由于二叉决策树的 EH 秩与 Strahler 数遵循相同递推，它直接启发本文的问题选择。其不足是把遍历作为证明工具而未显式构造遍历过程，也未处理带权图，本文据此把遍历本身提升为需要实现的计算对象。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

树的 Strahler 数刻画递归分支合并所需的资源，例如求值算术表达式所需的最少寄存器数；树宽度则刻画同一深度上的最大节点规模，并与最大反链等层次结构性质相关。要让 Transformer 可靠计算这些量，必须提供能够逐节点访问、回溯或按距离扩展，并在过程中保存和更新状态的程序化机制，因此它们适合作为检验 CoT 是否真正具备递归与遍历计算能力的具体科学问题。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于复杂度类或 EH 秩的 CoT 表达力刻画**：这类理论把允许的 CoT 步数与可表达的计算复杂度联系起来：单次或固定步计算受到有界深度模型的限制，而对数或线性数量的自回归步骤可进入更强的复杂度范围；EH 秩框架还从函数秩出发刻画固定步数下的可实现性。它们主要回答某类函数原则上是否存在 CoT 实现。
- **图算法 Transformer 与经验性 CoT 方法**：已有工作使用循环式 Transformer、可直接与图结构交互的注意力头来模拟 DFS、BFS 或 Dijkstra，也有研究通过实验考察连续 CoT 能否解决可达性问题。这些方法或依赖模型反复循环及专用图交互组件，或只观察最终任务表现，并未在按自回归步骤计数的标准 CoT 解码器中显式生成完整遍历过程。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 复杂度刻画属于“可能性”结果：即使证明某函数在给定 CoT 步数内可表达，也未给出低层数解码器如何选择下一节点、记录访问状态和执行回溯。原文特别指出，既有界限会借助穷举式树遍历达到，但没有构造该遍历；因此理论上界尚不能直接转化为可验证的 Transformer 程序。
- 既有图算法实现不处在本文关注的自回归、逐步计数 CoT 设置中，而可达性研究主要是经验性的且没有物化遍历轨迹。这使得研究者无法判断普通 CoT 步骤本身是否足以承载 DFS、BFS 或 Dijkstra，也无法据此构造 Strahler 数、宽度等处于线性步数复杂度边界附近的非平凡任务。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

缺失的是一种端到端、显式且深度受限的构造：在不依赖层归一化、位置编码或专用图交互原语的条件下，让硬注意力自回归解码器实际执行遍历，并证明该遍历能够支持一般有序多叉树上的分支复杂度计算。此外，文献尚未回答同一组合对象经树到 Dyck 路径的算法性双射换表示后，已有 CoT 实现能否直接迁移。

</div>
<div markdown="1"><span>核心问题</span>

本文具体回答两个相连的问题：能否用常数层、少量注意力头的 Transformer 解码器把 DFS 与 Dijkstra 显式实现为逐步 CoT 过程，并复用这些过程在线性数量步骤内计算树的 Strahler 数和宽度；对于由显式双射关联的树表示与 Dyck 路径表示，这两个派生量是否需要分别设计 CoT 构造，而不是由双射自动转移？

</div>
<div markdown="1"><span>作者直觉</span>

Strahler 数的递归更新天然依赖深度优先遍历：先深入处理子树，再在回溯时合并子节点结果；树宽度则适合按距离逐层扩展，可借助 Dijkstra 在每步选出当前最小距离节点。硬注意力可以把“从候选节点中唯一选出下一节点”压缩成一次选择操作，而自回归输出序列可充当外部工作轨迹，保存访问顺序和中间状态。另一方面，DFS 的前进与回退恰好对应 Dyck 路径的上升与下降，因此它既能执行树上计算，也能显式产生树到路径的编码，为比较两种表示下的独立实现提供自然入口。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文采用“显式构造”而非训练或经验拟合：先把图算法写成逐步更新的有限维状态机，再为每次状态转移指定一个定深、唯一硬注意力（unique hard-attention）的自回归 Transformer 解码器。输入是图的邻接矩阵或树对应的 Dyck 词；每生成一个 CoT token，解码器就读取原始输入和此前全部 token，借助硬注意力定位所需的顶点、边或历史状态，并由前馈网络执行比较、指示函数和状态更新。指定输出坐标在每一步都必须等于目标算法状态的固定编码，因此这里的“实现”是对所有合法输入成立的参数存在性证明，不是近似预测。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 将组合对象编码为解码器输入

图表示使用顶点集合、边权邻接矩阵及源点；树还可通过 DFS 轮廓映射 $[33m\phi[0m$ 编为 Dyck 词，其中沿未访问边向下记录 $\mathtt{U}$，回到父节点记录 $\mathtt{D}$。反向映射 $\psi$ 扫描 Dyck 词：$\mathtt{U}$ 创建并连接新子节点，$\mathtt{D}$ 将当前指针移回父节点。

<div class="method-step__io" markdown="1">

**输入**：图或根树 $G=(V,E,A)$，或者长度为 $2(n-1)$ 的 Dyck 词 $w$。<br>
**输出**：可供 Transformer 读取的输入 token 序列，以及图算法所需的邻接关系或路径步信息。

</div>

**直观理解**：树可以直接以“节点和边”输入，也可以写成一串上行、下行括号式动作；两种表示包含相同的有序树结构。路径表示使某些树统计量转化为对高度或同层节点的计数。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立遍历状态并生成下一步 CoT token

DFS 状态保存当前位置、父节点映射和访问标记；Dijkstra 状态保存暂定距离 $\mathsf{Dist}^{(t)}$、当前顶点 $cur^{(t)}$ 和访问标记 $vst^{(t)}$。唯一硬注意力按查询与键的内积选择得分最大的最早位置，多头结果经输出投影和 ReLU 前馈网络组合为下一状态 $y_t$。

<div class="method-step__io" markdown="1">

**输入**：原始输入 token、初始结束标记 $y_0$，以及此前生成的状态 token $y_1,\ldots,y_{t-1}$。<br>
**输出**：编码第 $t$ 次 DFS、Dijkstra 或 BFS 状态转移的 CoT token $y_t$。

</div>

**直观理解**：每个 token 相当于算法运行日志中的一行。注意力负责从输入和日志里找出当前真正需要的数据，前馈网络负责完成这一轮的条件判断和数值更新。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 复用遍历器累计树的分支复杂度

计算 Strahler 数时，在 DFS 首次进入节点时把其局部值置为 $0$，回溯时依据已处理子树的最大 Strahler 数 $M$ 及其达到次数 $c$ 更新父节点；计算宽度时，把无权树上的 Dijkstra 特化为 BFS，并维护当前深度层计数 $twd^{(t)}$ 与历史最大值 $mwd^{(t)}$。

<div class="method-step__io" markdown="1">

**输入**：DFS 或 BFS 的逐步状态，以及附加的少量统计坐标。<br>
**输出**：根节点的 $\str(G_T)$，或遍历结束时的 $mwd^{(n-1)}=\wid(G_T)$。

</div>

**直观理解**：Strahler 数要等子节点处理完再合并，所以与 DFS 回溯天然匹配；宽度要逐层数节点，所以与 BFS 的访问顺序天然匹配。论文的关键设计是把遍历器当作共享计算底座，而不是为每个树指标重新构造完整算法。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 投影并验证算法输出

构造参数使所有合法输入和每个预定步骤 $t$ 都满足 $\pi(y_t)=\operatorname{enc}(\mathsf{s}_t)$，其中 $\mathsf{s}_t$ 是目标算法的精确状态。生成步数由输入规模预先确定：论文摘要报告 DFS 路线以四层解码器在 $2n-1$ 步得到 Strahler 数，Dijkstra/BFS 路线以三层解码器在 $n-1$ 步得到宽度。

<div class="method-step__io" markdown="1">

**输入**：每一步解码器输出 $y_t$ 及指定的状态坐标投影 $\pi$。<br>
**输出**：目标遍历轨迹及最终树复杂度量；终止不依赖模型学习停止条件。

</div>

**直观理解**：作者证明的不是“模型大概率答对”，而是“存在一组固定权重，使每个中间 token 都严格等于算法的相应状态”。运行到事先规定的步数后，读取指定坐标即可得到答案。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### DFS 的前进与回溯转移

$$
\mathsf{dfs}^{(t)}(s)=\begin{cases}v_j,&v_j\in\mathcal{N}(\mathsf{dfs}^{(t-1)}(s))\ \text{且}\ vst^{(t-1)}(v_j)=0,\\ par^{(t-1)}(\mathsf{dfs}^{(t-1)}(s)),&\text{否则。}\end{cases}
$$

**符号说明**

- $\mathsf{dfs}^{(t)}(s)$：从起点出发的 DFS 在第 $t$ 步所在顶点
- $\mathcal{N}(v)$：顶点 $v$ 的邻居集合
- $vst^{(t)}(v)$：第 $t$ 步时顶点 $v$ 是否已访问的二值指示量
- $par^{(t)}(v)$：DFS 树中顶点 $v$ 在第 $t$ 步已记录的父节点
- $s$：DFS 的起始顶点

<div class="equation-explanation" markdown="1">

**直观理解**：若当前位置还有未访问邻居，算法选择一个这样的邻居并向下遍历；否则返回父节点。这个二分转移同时产生完整 DFS 轨迹和树到 Dyck 词的编码：前进对应 $\mathtt{U}$，回溯对应 $\mathtt{D}$。<br>
**原文位置**：第 2.1 节，公式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 任意叉树的 Strahler 递归

$$
\str(G_T)=\begin{cases}M+1,&c=|\{i:\str(\tau_i)=M\}|\ge 2,\\ M,&\text{否则},\end{cases}\qquad M=\max_i\str(\tau_i)
$$

**符号说明**

- $G_T$：当前有限根树或当前节点所根植的子树
- $\tau_i$：根节点的第 $i$ 棵子树
- $\str(\tau_i)$：子树 $\tau_i$ 的 Strahler 数；叶节点取 $0$
- $M$：所有孩子子树 Strahler 数的最大值
- $c$：达到最大值 $M$ 的孩子子树数量

<div class="equation-explanation" markdown="1">

**直观理解**：父节点通常继承最复杂孩子的数值；只有至少两个孩子同时达到该最大复杂度时，父节点才把复杂度提高一级。DFS 回溯时已经得到各孩子的结果，因此只需维护最大值及其是否重复出现，即可逐节点完成这一递归。<br>
**原文位置**：第 2.2 节，Strahler 数定义及 Observation 2

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文给出 Transformer 权重的存在性与显式构造，用逐步状态一致性 $\pi(y_t)=\operatorname{enc}(\mathsf{s}_t)$ 定义 CoT 实现；原文选段没有设置损失函数、梯度优化、训练样本分布或可学习性实验。因此该等式是正确性规格而非需要最小化的训练目标，不能把它解释为监督学习损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 唯一硬注意力定深解码器**

对当前序列最后位置形成查询，位置 $i$ 的注意力分数为 $a_{i,m-1}=\langle Kx_i,Qx_{m-1}\rangle$；若多个位置并列最大，则选择下标最小者。各头取出所选位置的 $V_hx_i$，拼接后经 $W_O$ 投影，再与残差一起通过两层线性映射和 ReLU；多层模型在每个生成步骤重新对扩展后的完整上下文执行各层计算，且构造不依赖位置编码或层归一化。

> 直观理解：普通软注意力会混合多个位置，这里则像精确寻址一样只读取一个位置，并用“最早下标”消除并列时的不确定性。这样才能把找父节点、找最小暂定距离顶点等离散算法操作写成确定的状态转移。

**2. DFS 与 Strahler 后序聚合器**

DFS 若当前节点存在未访问邻居就前进、记录父节点并标记访问，否则沿父指针回溯。每个节点保存已完成子树中的最大值及其重数；子树值为最大值加上“最大值至少由两个孩子达到”的指示量，因而回溯一步即可把刚完成子树的信息合并到父节点。

> 直观理解：DFS 的前进阶段发现节点，回退阶段意味着这个节点的所有后代已经处理完。于是回退时正好可以计算该子树的最终 Strahler 数，不需要另做一次后序遍历。

**3. Dijkstra/BFS 与层宽统计器**

Dijkstra 每轮松弛当前顶点的所有出边，然后从未访问顶点中选择暂定距离最小者；把边权域设为 $\{1,\infty\}$ 后，有限距离就是根到节点的深度，算法退化为 BFS。附加状态 $twd^{(t)}$ 统计当前距离层已访问的节点数，$mwd^{(t)}$ 保存此前各层计数的最大值，最终输出树宽。

> 直观理解：在无权树中，最短距离相同的节点恰好位于同一深度。只要在访问顺序跨入下一距离时结束上一层计数，并持续保存最大计数，就能边遍历边得到宽度。

**训练与推理**

训练阶段不适用：各层的查询、键、值投影以及输出和前馈矩阵由证明直接指定，而非从数据估计。推理时先把图、树或 Dyck 词编码为输入向量，并加入初始 token $y_0$；在第 $t$ 轮，把原输入与 $y_0,\ldots,y_{t-1}$ 组成当前上下文，逐层执行唯一硬注意力、残差和 ReLU 前馈计算，产生 $y_t$ 并追加到上下文。对 Strahler 数，token 依次模拟 DFS 的前进和回溯并在回溯时聚合子树值；对宽度，token 模拟 Dijkstra/BFS 并更新同层计数和历史最大值。运行预定轮数后，从 $\pi(y_T)$ 读取最终量，因此不存在采样、束搜索或学习式停止判定。

**复现信息**

公平理解该构造需要注意四点。第一，注意力是离散的唯一硬注意力，并以最小下标解决最大分数并列，这与常用 softmax 注意力不同；其“常数时间选最小者”是模型计算原语，不等同于常规机器上的实际墙钟复杂度。第二，作者保留标准值矩阵 $V$，但令输入仅为词嵌入 $x_i=\operatorname{WE}(\sigma_i)$，不使用位置编码；摘要还明确说明构造不需要层归一化。第三，层数和 CoT 步数是不同资源：网络深度固定，而自回归生成的线性数量 token 承担随输入规模增长的顺序计算。第四，所给选段省略了部分定理中的具体矩阵参数与头数分配，完整复现必须核对相应定理及附录；仅凭当前选段可以复现算法状态、输入输出契约和总体解码流程，但不能可靠还原全部权重。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 原文未明确报告。

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

#### 图遍历的显式 Transformer 构造

<div class="result-value" markdown="1">

作者声称，DFS 与 Dijkstra 算法均可由至多两层的唯一硬注意力解码器实现，其中 Dijkstra 构造同时涵盖 BFS。

</div>

这一结果说明固定而很浅的 Transformer 可以把遍历状态写入逐步生成的思维链，并根据历史状态决定下一步访问哪个顶点。这里证明的是理想化硬注意力模型中的精确可实现性，不是标准软注意力 Transformer 在真实数据上经过训练后必然学会这些算法，也没有给出速度或泛化准确率的经验比较。

<div class="result-source" markdown="1">

来源：摘要；第 4 节 Main Results，具体遍历构造指向第 4.1 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We give CoT realizations of depth-first search (DFS) and of Dijkstra algorithm, the latter subsuming breadth-first search, by unique hard-attention decoders of at most two layers, and use them as a shared computational substrate: reusing the DFS decoder yields the Strahler number of an $n$-vertex tree in $2n-1$ steps with four layers, and reusing the Dijkstra decoder yields its width in $n-1$ steps with three.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 复用 DFS 解码器计算含 $n$ 个顶点树的 Strahler 数

<div class="result-value" markdown="1">

作者声称，该构造使用四层，并在 $2n-1$ 个思维链步骤内得到 Strahler 数。

</div>

Strahler 数衡量树的递归分支复杂度：叶节点取基本值，父节点根据子树中最大值是否重复出现而更新。$2n-1$ 的线性步数与一次完整 DFS 进入和退出各子树的轨迹相对应，说明模型可以沿遍历路径汇总分支信息。该结论是构造性的最坏情形上界；节选没有证明四层或 $2n-1$ 步是不可进一步降低的最优下界。

<div class="result-source" markdown="1">

来源：摘要；第 4.2 节相关主定理，汇总见 Figure 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We give CoT realizations of depth-first search (DFS) and of Dijkstra algorithm, the latter subsuming breadth-first search, by unique hard-attention decoders of at most two layers, and use them as a shared computational substrate: reusing the DFS decoder yields the Strahler number of an $n$-vertex tree in $2n-1$ steps with four layers, and reusing the Dijkstra decoder yields its width in $n-1$ steps with three.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 复用 Dijkstra 解码器计算含 $n$ 个顶点树的宽度

<div class="result-value" markdown="1">

作者声称，该构造使用三层，并在 $n-1$ 个思维链步骤内得到树宽。

</div>

该构造借助 Dijkstra/BFS 式的按距离分层访问统计各深度上的节点数量，再取得最大的层大小作为树宽。结果表明遍历模块可以被复用于更高层的树结构统计，并且所需步骤随顶点数线性增长。它不表示三层模型在所有树问题上都足够，也不构成与其他神经网络在计算成本或实际精度上的经验优越性证明。

<div class="result-source" markdown="1">

来源：摘要；第 4.2 节相关主定理，汇总见 Figure 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We give CoT realizations of depth-first search (DFS) and of Dijkstra algorithm, the latter subsuming breadth-first search, by unique hard-attention decoders of at most two layers, and use them as a shared computational substrate: reusing the DFS decoder yields the Strahler number of an $n$-vertex tree in $2n-1$ steps with four layers, and reusing the Dijkstra decoder yields its width in $n-1$ steps with three.

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

- 原文未明确报告。

**实验想回答的问题**

- 在不使用层归一化和位置编码的条件下，固定深度、唯一硬注意力的 Transformer 解码器能否通过线性长度的思维链，显式实现 DFS、Dijkstra 等图遍历过程？
- 这些遍历解码器能否作为共享计算底座，在任意多叉树及其 Dyck 路径表示上精确计算 Strahler 数与树宽，并给出思维链线性步数对应分支复杂度的具体见证？

**实验实现**

本文呈现的是理论构造与复杂度分析，而非基于数据集的统计实验。给定一棵含 $n$ 个顶点的树，作者构造固定层数的唯一硬注意力解码器，逐步生成 DFS 或 Dijkstra 遍历轨迹，再复用相应解码器计算 Strahler 数或树宽。评价依据是构造是否对任意合法输入精确成立，以及所需 Transformer 层数和思维链步数；原文所给节选未报告训练过程、数据划分、随机种子、误差率或运行时间，也没有设置经验模型基线。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops explicit bounded-depth Transformer chain-of-thought constructions for graph traversal and tree-complexity computations.; rule check: matched taxonomy keywords; top rule score=6.0
- 全文指纹：`f76d12c619bdd99c4830f6b1827ca9133ad7b0bd677c785d03a13ff330bef3cb`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
