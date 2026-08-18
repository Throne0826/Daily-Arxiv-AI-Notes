---
title: "[论文解读] Identifiability and Order-Dimension Limits of In-Context Learning on Partial Orders"
description: "[arXiv 2608.14004][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.14004"
announcement_date: "2026-08-17"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-18T02:02:55.557959+00:00"
source_sha256: "62a626caa393c8d48c3d326458e3d560c13ed759c430aea5222afbe9b122f764"
tags:
  - "LLM Reasoning"
  - "上下文学习"
  - "偏序"
  - "版本空间"
  - "开放世界语义"
  - "逻辑可识别性"
  - "序维"
  - "坐标解码器"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.14004</p>

# Identifiability and Order-Dimension Limits of In-Context Learning on Partial Orders

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-17</span>
<span><strong>作者</strong> Faizanuddin Ansari, Debanjan Dutta, Swagatam Das</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Indian Statistical Institute</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.14004) · [PDF 下载](https://arxiv.org/pdf/2608.14004) · **关键词** 上下文学习, 偏序, 版本空间, 开放世界语义, 逻辑可识别性, 序维, 坐标解码器<br>


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

上下文学习（in-context learning, ICL）研究模型如何仅依据提示中的示例完成新任务，而不更新模型参数。常见理论把示例视为未知函数的输入—输出对，但本文关注更一般的关系推理：偏序关系同时满足自反性、反对称性和传递性，并允许两个元素不可比。因此，提示中没有出现某个比较，并不等于该比较为假或两元素不可比；有限示例也未必能唯一确定查询答案。本文借助版本空间描述所有与提示及背景知识一致的偏序，并以序维刻画受限坐标解码器能够精确表示哪些偏序。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**偏序与哈斯图**

偏序是满足自反性、反对称性和传递性的二元关系，但任意两个元素不一定可比。有限偏序可用哈斯图表示：图中只保留覆盖关系，而完整的可比关系可由这些边的自反传递闭包恢复。

</div>
<div class="concept-item" markdown="1">

**版本空间与开放世界语义**

版本空间是所有满足偏序公理、背景理论和提示标签的候选关系集合；查询只有在所有候选中结论一致时才可被逻辑识别。开放世界语义允许未展示的关系仍然成立，而封闭世界语义可将给出的有限哈斯图声明为完整结构。

</div>
<div class="concept-item" markdown="1">

**序维**

Dushnik–Miller 序维是若干线性扩展的最小数量，使这些全序的交恰好等于原偏序。它衡量一个偏序需要多少个独立排序坐标才能被精确表示，并构成本文坐标解码器能力边界的结构参数。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是固定且已知的有限元素全集，其上存在一个未知偏序。输入包括背景理论 $\mathcal{B}$、由正比较与负比较组成的有限提示，以及待判断的查询比较；开放世界设定下，未标注的比较不能直接视为假。逻辑任务的输出为三类之一：查询在所有一致偏序补全中均成立时为“必真”，在所有一致补全中均不成立时为“必假”，否则为“未知”。在此基础上，论文还考察教出完整偏序所需的标签数量，以及使用 $s$ 个单调排序坐标的提示依赖解码器能否精确表示该偏序；本文背景部分所需的核心区分是，逻辑可识别性、教学成本和表示能力是不同问题。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\preceq$**

有限元素全集上的偏序关系；$x\preceq y$ 表示元素 $x$ 不大于元素 $y$。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{B}$**

解释关系符号并约束候选偏序的背景理论，例如只给出偏序公理，或额外提供自然数大小关系等语义知识。

</div>
<div class="notation-item" markdown="1">

**$n$**

固定且已知的有限元素全集大小。

</div>
<div class="notation-item" markdown="1">

**$s$**

提示依赖坐标解码器使用的排序坐标数量；论文所述精确表示边界与偏序的序维比较。

</div>

</div>

**直接相关的工作**

- **函数学习、贝叶斯推断与隐式优化等 ICL 理论**: 这些理论主要把提示建模为未知函数的样本，并分析贝叶斯最优预测、信息限制或隐式学习机制；本文转向允许不可比性的偏序关系，重点研究有限提示是否在逻辑上唯一决定查询，而非仅研究统计预测。
- **Dushnik–Miller 序维理论**: 经典序理论将偏序的序维定义为实现该偏序所需线性扩展的最小数量。本文不把这一数学结果本身视为新贡献，而是用它刻画一种形式化、提示依赖的单调坐标解码器的精确表示能力。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现有上下文学习理论通常把任务看作从示例中恢复一个函数，即每个输入对应一个确定输出；但许多推理任务描述的是关系，例如偏序中的“先于”“不大于”或“可整除”。偏序同时具有自反性、反对称性和传递性，却允许元素之间不可比较，因此提示中没有出现某个关系，并不等于该关系为假。若不明确背景知识、论证是否完整以及未知答案是否允许，模型的错误就无法区分为信息不足、提示设计不足或表示能力不足。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **函数式与统计式上下文学习理论**：这类研究通常假设提示由未知函数的输入—输出样例构成，再分析模型能否根据样例预测新输入的函数值；部分工作进一步使用贝叶斯最优推断或信息论模型刻画数据分布和不确定性。它适合单值映射，但难以直接表达偏序中传递关系、反对称关系以及不可比较性。
- **线性序与特定关系任务的经验研究**：已有经验研究将上下文学习用于线性序、整除等关系任务，通过观察模型在不同提示下的预测性能来研究其适应能力。这类实验能够揭示模型表现是否饱和，却通常不能回答一个查询是否被提示在逻辑上唯一确定，也不能系统刻画完整偏序的教学代价和结构表示边界。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 函数式建模把未观测信息与否定信息过度等同：在偏序中，提示未说明 $x\preceq y$，只能表示该关系尚未被展示，不能直接推出 $x\npreceq y$。其后果是，单纯依据示例拟合函数值可能把真正的逻辑歧义错误计为模型预测错误。
- 经验性能或统计不确定性不能替代对所有一致关系补全的逻辑分析。已有方法通常未同时区分开放世界语义与闭世界语义，也未说明需要多少正、负比较才能唯一识别目标偏序；因此无法判断困难究竟来自查询不可识别、提示标签不足，还是目标偏序本身需要更多坐标表示。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一个把偏序上下文学习形式化为关系补全问题的统一理论：它需要在固定元素集合和明确背景理论下，定义与提示一致的偏序版本空间，并判断一个查询在所有可能补全中是否恒真、恒假或仍然未知；同时还应刻画识别整个偏序所需的最少提示，以及目标结构能否由受限的坐标排序解码器精确表示。换言之，现有研究尚未把逻辑可识别性、开放世界教学成本、偏序结构复杂度和形式解码能力放进同一分析框架。

</div>
<div markdown="1"><span>核心问题</span>

对于有限偏序上的关系型上下文学习，给定固定宇宙、背景理论以及正负比较示例，提示究竟何时逻辑上确定查询答案，何时必须输出未知；唯一识别整个目标偏序所需的最少标签是多少；并且一个目标偏序何时能够被具有 $s$ 个单调坐标的提示依赖型坐标解码器精确表示？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把模型面对的可能目标关系显式写成版本空间，而不是直接假设提示背后只有一个隐藏答案。对每个查询，只需检查版本空间中的所有偏序是否一致：若正向传递闭包已经包含该关系，答案被强制为真；若加入该关系会造成环或违反负示例，答案被强制为假；若仍存在同时满足所有约束、但对该查询给出不同结果的偏序，答案就是未知。进一步地，覆盖关系负责保留目标偏序的必要正向结构，而负向阻塞关系排除开放世界下的额外边；因此，提示教学可以分别衡量结构本身的复杂度和开放世界所带来的额外信息需求。最后，偏序的序维数刻画了其能否嵌入若干个独立线性坐标的精确边界，使“模型表示不了”这一说法限定在明确的解码器类别内，而不是泛化为对所有神经网络的结论。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是提出并训练一个新的神经网络，而是建立一套用于判断“部分序关系上的上下文学习是否原则上可解”的理论分析流程。输入是有限元素全集 $U$、带正负标签的演示集 $\mathcal{D}=(\mathcal{D}^{+},\mathcal{D}^{-})$、背景理论 $\mathcal{B}$ 和查询 $q=(a,b)$；方法先构造所有与演示一致的偏序所组成的版本空间，再检查这些候选偏序是否对 $a\preceq b$ 给出相同答案。在最宽松的开放世界设定下，作者进一步把该检查化为一个可执行的闭包算法：计算正例的自反传递闭包 $R$，然后依据正向可达性、反向可达性以及加入查询后由传递性强制产生的“前驱-后继矩形”是否撞上负例，将查询精确分成确定为真、确定为假和不可识别三类。

在此基础上，论文从两个互补角度刻画可解性的结构限制。其一是表示限制：若解码器只为每个元素输出 $s$ 个实数坐标，并以所有坐标均不下降作为比较规则，那么它能精确表示的目标偏序恰好是序维数不超过 $s$ 的偏序；这是一条零误差能力边界，而不是高效学习算法。其二是证书复杂度：真比较可以用 Hasse 图中的覆盖路径证明，其最短证书长度为 $\lambda_P^{+}(a,b)$；假比较可由包含 $a$、排除 $b$ 的前向闭合集证明，规范的最小见证是 $\operatorname{Reach}_{H}(a)$，大小为 $\nu_P^{-}(a,b)$。直观地说，方法分别回答三个问题：现有提示是否已经唯一决定答案、指定坐标式解码器是否有足够表达能力，以及一个答案最短需要展示多少局部结构才能被验证。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 形式化提示与候选目标

把每个候选偏序 $P=(U,\preceq_P)$ 表示为关系图 $R_P$，保留所有包含 $\mathcal{D}^{+}$ 且与 $\mathcal{D}^{-}$ 不相交的候选，形成版本空间 $\mathcal{V}_{\mathcal{B}}(\mathcal{D})$。若版本空间为空，则提示在该背景理论下不可满足，后续的可识别性判定不适用。

<div class="method-step__io" markdown="1">

**输入**：有限公共全集 $U$、正演示 $\mathcal{D}^{+}$、负演示 $\mathcal{D}^{-}$、背景偏序类 $\mathcal{B}$ 和查询 $q=(a,b)$。<br>
**输出**：与全部演示一致的候选偏序集合，以及提示是否可满足的判定。

</div>

**直观理解**：可以把每个候选偏序看成一份可能的“完整答案表”：正例必须出现在表中，负例必须缺席。版本空间就是尚未被提示排除的全部答案表。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 开放世界闭包预处理

对正演示计算自反传递闭包 $R=\operatorname{TC}(\mathcal{D}^{+})$，得到仅由正例和偏序传递性必然推出的最小一致关系；同时为每个元素建立前驱集合 $\operatorname{Pred}_{R}(x)$ 和后继集合 $\operatorname{Succ}_{R}(x)$。由于提示可满足，$R$ 本身反对称且不会包含任何负演示，因此 $P^{-}=(U,R)$ 是一个合法的一致补全。

<div class="method-step__io" markdown="1">

**输入**：可满足的 $\mathcal{D}$，并令背景类 $\mathcal{B}$ 为 $U$ 上的全部偏序。<br>
**输出**：最小一致偏序 $P^{-}$、闭包关系 $R$ 及用于逐查询检测的前驱和后继信息。

</div>

**直观理解**：这一步只接受“正例必然连锁推出”的关系，不擅自补充其他比较，因此得到最保守的完整结构。后续只需判断把查询边加入这个结构会不会制造矛盾。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 查询三分判定

若 $aRb$，则所有一致补全都令查询为真；否则检查 $bRa$ 是否会导致反对称性冲突，以及 $\operatorname{Pred}_{R}(a)\times\operatorname{Succ}_{R}(b)$ 是否与 $\mathcal{D}^{-}$ 相交。若任一障碍成立则查询确定为假；若均不成立，则 $P^{-}$ 给出假答案，而加入 $(a,b)$ 后的闭包 $P^{+}$ 给出真答案，故查询不可识别。

<div class="method-step__io" markdown="1">

**输入**：闭包 $R$、负演示 $\mathcal{D}^{-}$ 和查询 $(a,b)$。<br>
**输出**：“确定为真”“确定为假”或“不可识别”之一，并可构造支持该结论的一致补全。

</div>

**直观理解**：加入 $a\preceq b$ 不只增加一条边：任何能到达 $a$ 的元素都必须小于任何从 $b$ 可达的元素。若这些连带关系碰到负例或形成环，就只能回答假；否则真、假两种世界都说得通。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 受限解码器与证书分析

对坐标式解码器，检查 $\operatorname{dim}(P)\leq s$ 是否成立；该条件等价于存在 $s$ 个实值坐标，使 $x\preceq_P y$ 当且仅当每一维都满足 $\phi_i(x)\leq\phi_i(y)$。对答案证书，真查询取最短覆盖路径，假查询取前向闭合的可达集 $\operatorname{Reach}_{H}(a)$，分别以 $\lambda_P^{+}(a,b)$ 和 $\nu_P^{-}(a,b)$ 衡量见证规模。

<div class="method-step__io" markdown="1">

**输入**：目标偏序 $P$、坐标数 $s$、完整 Hasse DAG $H(P)$，以及待证明的查询 $(a,b)$。<br>
**输出**：指定 $s$ 坐标解码器能否零误差表示目标的结论，以及正、负查询的规范证书和证书大小。

</div>

**直观理解**：坐标数相当于解码器可同时使用的排序视角；偏序需要的视角多于 $s$ 时，这类解码器无论如何选择参数都不能精确表达。证书分析则区分“沿一条链证明能到达”和“展示整个封闭区域证明不能到达”两种验证负担。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 版本空间与查询可识别性

$$
\mathcal{V}_{\mathcal{B}}(\mathcal{D})=\left\{P\in\mathcal{B}:\mathcal{D}^{+}\subseteq R_P,\;\mathcal{D}^{-}\cap R_P=\varnothing\right\},\qquad \left|\left\{\mathbf{1}[a\preceq_P b]:P\in\mathcal{V}_{\mathcal{B}}(\mathcal{D})\right\}\right|=1
$$

**符号说明**

- $U$：所有目标偏序和候选假设共享的有限元素全集。
- $\mathcal{B}$：背景理论允许的候选偏序类，可编码开放世界、封闭世界或额外语义知识。
- $\mathcal{D}=(\mathcal{D}^{+},\mathcal{D}^{-})$：提示中的带标签演示；前者断言关系成立，后者断言关系不成立。
- $R_P$：偏序 $P$ 的关系图，即所有满足 $x\preceq_P y$ 的有序对。
- $\mathcal{V}_{\mathcal{B}}(\mathcal{D})$：在背景理论内与全部正负演示一致的版本空间。
- $\mathbf{1}[a\preceq_P b]$：查询在候选偏序 $P$ 中成立时为 1，否则为 0 的指示量。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分筛出没有违反任何演示的全部可能目标；第二部分要求这些目标对查询只产生一种二元值。它给出了本文最基本的可解性标准：可识别性取决于提示和背景假设是否排除了所有答案相反的候选，而不取决于某个具体模型碰巧输出了什么。<br>
**原文位置**：第 3 节 Definition 1（Version space and identifiability）；普遍可靠回答的等价性见第 4 节 Proposition 2

</div>

</div>

<div class="equation-block" markdown="1">

#### 开放世界补全三分律

$$
\begin{cases}\text{identified true}, & aRb,\\ \text{identified false}, & a\not Rb\ \land\ \left(bRa\ \lor\ \left(\operatorname{Pred}_{R}(a)\times\operatorname{Succ}_{R}(b)\right)\cap\mathcal{D}^{-}\neq\varnothing\right),\\ \text{unidentifiable}, & \text{otherwise},\end{cases}\qquad R=\operatorname{TC}(\mathcal{D}^{+})
$$

**符号说明**

- $R$：正演示关系的自反传递闭包，即正例必然推出的最小偏序关系。
- $\operatorname{TC}$：自反传递闭包算子。
- $\operatorname{Pred}_{R}(a)$：在 $R$ 中能够到达 $a$ 的全部前驱，包括 $a$ 自身。
- $\operatorname{Succ}_{R}(b)$：在 $R$ 中可由 $b$ 到达的全部后继，包括 $b$ 自身。
- $\operatorname{Pred}_{R}(a)\times\operatorname{Succ}_{R}(b)$：加入 $a\preceq b$ 后由传递性必然新增的前驱-后继关系集合。
- $\mathcal{D}^{-}$：被明确标为不成立的有序对集合。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把逻辑上的“检查所有一致偏序”转化为三项有限关系测试。已有正向路径直接证明真；已有反向路径意味着加入查询会破坏反对称性，而矩形撞上负例意味着加入查询会违反演示；若两类障碍都不存在，就能分别构造一个回答假的最小补全和一个回答真的扩展补全，因此信息不足。<br>
**原文位置**：第 4 节 Theorem 3（Open-world completion trichotomy）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文给出的是有限偏序上的可识别性判据、确定性闭包算法、坐标解码器的表示能力边界和证书大小结论，没有定义损失函数、参数学习目标或梯度优化过程。Corollary S11 的充分性证明仅对每个已指定目标选择一个坐标实现并定义映射 $\Phi$；作者明确指出这不是高效学习算法，因此不能把它解释为可直接训练的模型构造。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 版本空间与可识别性判据**

版本空间收集所有满足正负演示约束的 $P\in\mathcal{B}$。查询被识别，当且仅当集合 $\{\mathbf{1}[a\preceq_P b]:P\in\mathcal{V}_{\mathcal{B}}(\mathcal{D})\}$ 只有一个值；命题 2 进一步说明，这也恰好是存在普遍可靠二元回答规则的充要条件，随机化不能消除两个一致候选之间的答案冲突。

> 直观理解：该模块把模型是否“答对”改写为信息是否足够：如果所有符合提示的结构都同意，答案才在逻辑上确定；如果存在两个同样合法但结论相反的结构，任何强制输出真或假的规则都必然在其中一个结构上出错。

**2. 开放世界补全三分器**

定理 3 用 $R=\operatorname{TC}(\mathcal{D}^{+})$ 代替显式枚举全部偏序。加入查询 $(a,b)$ 后新强制的关系恰为 $\operatorname{Pred}_{R}(a)\times\operatorname{Succ}_{R}(b)$；因此，只需检查正向闭包、反向路径和该矩形与负例的交集，即可完整判断两种答案是否分别存在一致补全。

> 直观理解：关键设计是把可能数量巨大的候选结构搜索压缩为局部冲突检测。所谓“矩形”表示所有必须跟着新增的关系，它精确捕获了传递性造成的连锁影响。

**3. 序维数与正负证书模块**

序维数 $\operatorname{dim}(P)$ 是其关系可表示为多少个线性扩展之交的最小数量，并与合取式坐标比较所需的最少坐标数等价。完整 Hasse 图则删除可由传递性推得的冗余边：正证书是覆盖边路径，负证书是前向闭合集；其中 $\operatorname{Reach}_{H}(a)$ 是包含 $a$ 且排除不可达 $b$ 的唯一包含意义下最小前向闭合集。

> 直观理解：这一模块没有声称限制所有神经网络，而是分别限制特定的坐标解码形式和特定的路径证书形式。序维数衡量“表示需要多少排序视角”，证书大小衡量“验证一次回答需要暴露多少图结构”，两者不能直接当作一般 Transformer 的深度下界。

**训练与推理**

不存在训练阶段。推理时，首先确认 $\mathcal{V}_{\mathcal{B}}(\mathcal{D})\neq\varnothing$；在开放世界且 $\mathcal{B}$ 包含 $U$ 上全部偏序时，计算 $R=\operatorname{TC}(\mathcal{D}^{+})$。对每个查询依次测试 $aRb$、$bRa$，再扫描负演示 $(x,y)\in\mathcal{D}^{-}$，检查是否同时有 $xRa$ 与 $bRy$：第一项成立输出确定为真；第一项不成立而后两类冲突之一成立，输出确定为假；否则输出不可识别，而不是未经依据地强制给出二元答案。

若评估的是封闭世界完整 Hasse 图，推理规则改为图可达性：$a\preceq b$ 当且仅当从 $a$ 到 $b$ 存在有向路径，并包含 $a=b$ 的零长度路径。若分析固定的 $s$ 坐标解码器，则先由目标序维数判断原则上的精确可表示性，再用合取式规则“所有 $i\in[s]$ 均有 $\phi_i(a)\leq\phi_i(b)$”回答；这项分析假定提示到目标是函数性的，即同一个提示不会对应两个不同目标，否则精确解码首先会被提示歧义阻断。

**复现信息**

开放世界算法可用标准传递闭包方法一次性计算 $R$，原文给出的直接实现时间为 $O(|U|^{3})$；闭包完成后，每个查询检查两次可达性，并扫描 $\mathcal{D}^{-}$，耗时 $O(|\mathcal{D}^{-}|)$。若使用长度为 $|U|$ 的前驱、后继和负邻接位集，矩形冲突检测可在每个查询 $O(|U|^{2}/w)$ 个机器字操作内完成，其中 $w$ 是机器字宽度。

复现或解释结论时必须明确背景语义：开放世界允许补入未演示且不违背公理和负例的比较，封闭世界 Hasse 语义则宣告给定 DAG 已是完整 Hasse 图，两者会对同一未观察查询给出不同的可识别性结论。还应区分三类边界的适用范围：三分律是对全部有限偏序背景的精确判定；序维数结论只约束固定的合取式 $s$ 坐标解码器；$\lambda_P^{+}$ 的下界只约束必须生成或验证覆盖路径的过程，并不排除全局可达性算法或其他神经表示。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 四元素标号偏序全集：包含固定四元素宇宙上的全部219个标号偏序。它不是从现实任务采样的数据集，而是一个可穷举的有限结构集合，用于精确计算开放世界提示下未观察查询的歧义比例；原文没有设置训练集、验证集或测试集。
- 目标一致的比较提示：对每个目标偏序，从12个非自反有序对中选取大小为$m$的子集，并赋予与目标偏序一致的正、负标签。该集合模拟提示中已观察的关系信息，$m$控制标签覆盖程度。
- 未观察查询集合：从未被选入提示的非自反有序对中产生查询，并判断该查询在所有满足提示的偏序补全中是必真、必假还是仍有歧义。它承担实际评测对象的角色。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**歧义比例**

在未观察查询中，被定理3判为无法由当前提示唯一确定的查询所占比例；论文对目标偏序、大小为$m$的提示子集以及未观察查询进行均匀平均。 （该指标没有统一的越高或越低越好含义。较高表示提示的信息充分性较差，也说明强制二分类评测更容易混淆信息限制与模型错误。）

</div>
<div class="metric-item" markdown="1">

**标签覆盖量$m$**

提示从12个非自反有序对中观察到的目标一致标签数量，用于刻画提示预算，而不是模型性能。 （通常$m$越大，提示提供的信息越多；但论文的核心检查是高覆盖时是否仍有歧义，而不是把$m$本身作为需要最大化的成绩。）

</div>
<div class="metric-item" markdown="1">

**真、假、未知逻辑分类**

定理3给出的逐查询判定：查询被所有一致补全支持时为必真，所有使其为真的补全都会产生环或违反负例时为必假，否则为未知。 （它是分类语义而非标量指标，没有单调优劣关系；其作用是为后续模型评测提供可解释的标准答案。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 固定四元素宇宙上的全部标号偏序

<div class="result-value" markdown="1">

作者穷举了全部219个标号偏序，而不是抽样一部分结构，因此图1在其指定平均方案下给出精确的有限宇宙统计量。

</div>

这消除了该小规模示例中的抽样误差，说明观察到的歧义不是偶然抽到困难偏序造成的。不过，219是四元素标号偏序的全集规模，不是模型准确率，也不能直接代表更大偏序或自然语言任务中的分布。

<div class="result-source" markdown="1">

来源：第4节“Deterministic finite-universe illustration”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We exhaustively enumerate all 219 labeled posets on four elements.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 对目标偏序、大小为$m$的目标一致提示子集和未观察查询进行均匀平均

<div class="result-value" markdown="1">

图1报告精确歧义比例；作者称即使标签覆盖较高，仍有相当一部分未观察查询保持歧义。节选未给出各$m$对应的具体数值。

</div>

结果表明，多给出标签并不必然让每个查询都获得唯一逻辑答案，因为开放世界允许未展示关系在不同一致补全中取不同值。这是提示的信息限制，不是任何特定语言模型的失败；由于缺少图中数值，不能据此量化歧义下降速度。

<div class="result-source" markdown="1">

来源：第9节讨论，Figure 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Figure 1 illustrates why this distinction matters: under the explicitly defined exhaustive averaging scheme over all 219 labeled four-element posets, a substantial fraction of unobserved queries remain ambiguous even at high label coverage.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 开放世界的混合正、负比较提示

<div class="result-value" markdown="1">

定理3可作为与模型无关的逻辑基线，将查询划分为必真、必假或未知；作者据此主张，未知查询不应自动按普通二分类错误处理。

</div>

该结果改变了评测分母和错误解释：模型若面对逻辑未知查询，输出任一二值答案都不能仅凭目标结构标签判定为推理失败。它提供的是规范化评测原则，而不是某个模型优于基线的实证证据；论文也没有在节选中报告任何LLM的准确率。

<div class="result-source" markdown="1">

来源：第9节讨论，紧随Figure 1的解释

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Such queries should not automatically be scored as ordinary binary errors.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 确定性示例只覆盖四元素偏序，并采用对目标、提示子集和未观察查询的特定均匀分布；它不能说明自然语言提示、非均匀任务分布或更大结构中的歧义比例。原文也明确指出：“The deterministic illustration is an exhaustive enumeration for the specifically defined uniform distribution over four-element targets, prompt subsets, and unobserved queries; no theorem depends on that illustration.”
- 论文没有在所给章节中评测实际Transformer或语言模型，也没有报告准确率、置信区间、训练细节或模型间比较。结论区分的是逻辑不可识别性、提示预算、证书大小和特定坐标解码器的表示限制，不能外推为对不受限Transformer、近似解码器或一般图算法的能力上界。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 定理3的开放世界逻辑基线：先对正例取自反传递闭包，再检查反向可达性以及加入查询后是否会迫使某个负例成立。该基线直接给出必真、必假或未知标签，适合判断一个模型错误究竟源于推理失败还是提示本身不充分。
- 普通二分类评分：把每个查询都强制视为真或假。它是关系预测中常见但不充分的对照，因为开放世界下存在多个与提示一致、却对查询取值不同的偏序补全；论文据此指出，逻辑未知不应自动计为一般二分类错误。
- 完整Hasse图的闭世界可达性：若提示明确声明所展示的有限Hasse图完整，则未展示关系可按图上的不可达性处理。它与开放世界基线的对比用于说明歧义来自语义假设，而不只是查询算法。

**实验想回答的问题**

- 在有限开放世界提示中，即使已经观察到较多目标一致的比较标签，未观察查询是否仍可能无法由提示唯一确定？
- 逻辑上的“真、假、未知”三分类能否为偏序关系的上下文学习评测提供一个与具体模型无关的参照，从而区分信息不足与模型推理错误？

**实验实现**

实验是确定性的穷举计算，不涉及模型训练、随机种子或参数调优。作者枚举固定四元素宇宙上的全部219个标号偏序；对每个目标偏序、每个$m$，均匀遍历12个非自反有序对的所有$m$元素观察子集，仅保留目标一致标签，并在未观察有序对上应用定理3的补全三分法，最后对目标、提示子集和查询取平均。通用算法先计算正例关系的自反传递闭包$R$，朴素预处理复杂度为$O(|U|^3)$；闭包完成后，每个查询扫描负例的复杂度为$O(|\mathcal{D}^{-}|)$。原文节选未提供代码、硬件、软件环境或可复现实验链接。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 三元素示例取$U=\{a,b,c\}$、正例$\mathcal{D}^{+}=\{(a,b)\}$、负例$\mathcal{D}^{-}=\{(a,c)\}$。查询$a\preceq b$由正例闭包判为必真；若令$b\preceq c$为真，传递性会迫使$a\preceq c$，与负例冲突，故其必假；查询$c\preceq b$既可保持为假，也可加入关系后得到一致偏序，因此为未知。该案例直观展示三类输出，但不构成模型实验或性能比较。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper analyzes the theoretical identifiability and order-dimension limits of transformer in-context reasoning over partial orders.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`62a626caa393c8d48c3d326458e3d560c13ed759c430aea5222afbe9b122f764`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
