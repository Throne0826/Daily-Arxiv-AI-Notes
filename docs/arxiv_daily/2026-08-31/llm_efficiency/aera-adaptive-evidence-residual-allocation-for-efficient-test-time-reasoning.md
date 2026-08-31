---
title: "[论文解读] AERA: Adaptive Evidence Residual Allocation for Efficient Test-Time Reasoning"
description: "[arXiv 2608.27964][LLM 效率] AERA 将自适应推理的决策目标从“当前答案看起来是否可信”改为“继续计算是否仍有望改善答案”，以应对推理正确性随计算量非单调变化的问题。"
arxiv_id: "2608.27964"
announcement_date: "2026-08-31"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:36:47.762947+00:00"
source_sha256: "ad249c46f72bc3eef3d755e2e6225c4521a19ef81ec0f7f37ca7274a7f69c43f"
tags:
  - "LLM 效率"
  - "LLM Reasoning"
  - "测试时扩展"
  - "自适应推理"
  - "自适应停止"
  - "残余效用"
  - "非单调正确性"
  - "候选响应分配"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2608.27964</p>

# AERA: Adaptive Evidence Residual Allocation for Efficient Test-Time Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Ziming Wang, Ivor Tsang, Hangwei Qian</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> National University of Singapore, Singapore；Agency for Science, Technology and Research (A*STAR), Centre for Frontier AI Research (CFAR), Singapore；Nanyang Technological University, Singapore</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27964v1) · [PDF 下载](https://arxiv.org/pdf/2608.27964v1) · **关键词** 测试时扩展, 自适应推理, 自适应停止, 残余效用, 非单调正确性, 候选响应分配<br>


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

AERA 将自适应推理的决策目标从“当前答案看起来是否可信”改为“继续计算是否仍有望改善答案”，以应对推理正确性随计算量非单调变化的问题。

**不用术语来说**：让语言模型针对同一道题生成更多解答，通常能提高最终答对的机会，但给所有题目分配相同数量的解答非常浪费：有些题很快就已解决，有些题继续生成也未必有用。更棘手的是，模型当前表现得很自信或多个解答高度一致，并不保证答案正确，也不意味着后续计算没有价值；答案可能在继续推理后由错变对，也可能由对变错。因此，系统需要判断的不是“现在看起来稳不稳”，而是“再投入一批计算是否值得”。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者识别并量化了可观测证据与检查点正确性之间的错位：聚合答案会发生恢复、崩塌和振荡，而且置信度或答案一致性有时会在答案由对变错时增强、在由错变对时减弱。原文证据为“Across 792 adjacent GPQA checkpoint transitions, we observe 42 recoveries from an incorrect to a correct aggregate and 14 collapses in the opposite direction.”（Introduction，Figure 1–2 相关段落）。
- 作者提出“残余效用”这一决策目标，并据此设计 AERA：控制器只读取当前响应前缀中的答案分布、时间变化、重新求解、语义一致性及已用算力等证据，逐检查点决定停止还是分配下一批响应；未来检查点的正确性仅用于离线构造监督，不作为推理时可见信息。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型测试时推理与自适应计算领域。测试时扩展通过生成更长的推理轨迹、多个候选答案或重新求解尝试来提高问题求解能力，但固定地为每道题分配相同推理预算会浪费计算：有些题目经过少量响应即可解决，另一些题目则需要继续探索。本文关注的核心问题是：在只能看到当前已生成响应前缀的条件下，系统如何判断下一段推理计算是否仍具有足够价值，而不是简单依据当前置信度或答案一致性停止。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试时扩展**

测试时扩展是在模型参数不变的情况下，于推理阶段增加计算量，例如生成多个候选解或进行多次重新求解。其目标是用额外计算换取更高的答案正确率。

</div>
<div class="concept-item" markdown="1">

**自适应停止与响应块**

自适应停止不是预先规定所有题目都生成相同数量的响应，而是在若干检查点决定停止或继续。本文把每次新增的一组候选响应称为一个响应块，并据此逐步分配预算。

</div>
<div class="concept-item" markdown="1">

**残余效用**

残余效用表示继续进行额外推理是否可能带来足以抵消计算成本的改进。它不同于当前答案看起来是否正确：当前证据增强并不保证未来答案不会崩溃，当前证据减弱也不排除后续恢复。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一道问题及模型逐步生成的候选响应集合，系统在每个检查点观察累计响应前缀的可见信息，并输出二元决策：停止推理，或分配下一个响应块。控制器可使用答案分布、时间变化、重新求解行为、语义一致性和已消耗计算等特征，但推理时不能访问未来检查点的正确性；未来正确性只用于离线构造监督信号。该设定的目标是在尽量保持最终答案准确率的同时减少完成 token 和整体推理计算。论文特别针对检查点正确性可能非单调变化的情形，即答案可能从错误恢复为正确，也可能从正确转为错误。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入问题。

</div>
<div class="notation-item" markdown="1">

**$R_t$**

第 $t$ 个检查点之前已经观察到的累计响应前缀或响应集合。

</div>
<div class="notation-item" markdown="1">

**$t$**

推理检查点索引，表示当前已经分配的响应块或计算阶段。

</div>
<div class="notation-item" markdown="1">

**$u_t$**

第 $t$ 个检查点的残余效用，表示继续分配下一响应块是否可能带来值得付出成本的答案改进。

</div>

</div>

**直接相关的工作**

- **Early-Stopping 与 Difficulty-Adaptive Self-Consistency**: 这些响应级自适应方法根据答案稳定性或估计的问题难度改变采样数量，说明了按题目分配不同推理预算的可行性。但本文指出，答案稳定性和当前证据主要描述已观察状态，未必能直接估计未来计算的收益。
- **Dynamic early exit 与 ConCISE**: 这类方法在单条推理轨迹内部监控中间信号，以提前终止或压缩生成过程。AERA 的差异在于面向累计候选响应进行顺序控制，并把预测目标定义为未来残余效用，而非把当前高置信度直接当作停止依据。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

测试时扩展通过生成更长推理轨迹、多个候选解答或重新尝试来提高语言模型的解题能力，但固定预算会同时对已经解决的简单题和长期无法稳定作答的困难题继续采样，造成大量无效生成。实际需求因而是按题目和当前轨迹动态分配剩余算力，在尽量保留准确率的同时显著降低响应数量与生成成本。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **推理前的预算或思考需求预测**：训练一个策略，根据题目特征预先预测所需推理预算，或判断该题是否需要显式思考；随后按预测结果选择不同计算量。此类方法能够实现题目级差异化分配，但往往在完整推理轨迹出现之前作出主要预算决定。
- **基于当前证据的自适应停止**：响应级方法依据多次采样后的答案稳定性、答案一致程度或估计难度决定是否停止；单条推理轨迹内的方法则监控中间置信度等信号，提前终止或压缩后续生成。其共同逻辑是：当前置信度越高、熵越低或候选答案越一致，继续计算的必要性越小。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 当前置信度、熵和答案一致性描述的是已经观察到的响应集合，却不直接衡量尚未执行的计算能否带来改进。只有当证据强弱与正确性可靠对应、且正确性随计算量单调改善时，才能安全地把“当前证据强”解释为“可以停止”；论文观察到的恢复和崩塌说明这一前提不成立。
- 一次性预算预测或只看当前稳定性的停止规则难以及时处理轨迹反转：错误聚合答案可能在后续检查点恢复，而正确答案也可能继续计算后崩塌。更直接的经验是“evidence sometimes strengthen during collapse and weaken during recovery”（Introduction，Figure 2 相关段落），其后果是传统规则可能过早放弃可恢复的问题，也可能在表面稳定但实际错误时停止。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究已经证明自适应计算可以减少推理成本，但尚未明确：当检查点正确性非单调、可观测证据与正确性可能反向变化时，停止准则究竟应预测什么。缺少的是一种严格区分“当前状态看起来多可信”与“未来额外计算还有多少改善机会”的序贯决策目标，以及只依赖推理时可见前缀证据来学习该目标的控制机制。

</div>
<div markdown="1"><span>核心问题</span>

能否从当前响应前缀的可观测证据中，预测分配下一批计算是否仍可能恢复或改善最终答案，并在不使用未来正确性作为推理时特权信息的条件下，逐检查点作出停止或继续决策？

</div>
<div markdown="1"><span>作者直觉</span>

把额外计算看成一项需要判断回报的投资：控制器不必断言当前答案究竟对不对，而只需识别这条轨迹是否还存在值得利用的“剩余机会”。完整训练轨迹可以事后揭示哪些前缀继续计算后会改善，从而为残余效用提供监督；部署时，控制器再利用当前前缀中答案集中程度、近期变化、重新求解迹象和语义一致性等线索估计这种机会。每增加一批响应后重新评估，也比预先锁定最终预算更能适应恢复、崩塌与振荡。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

AERA（Adaptive Evidence Residual Allocation）是在测试时推理阶段控制计算量的顺序决策器。它不改变冻结推理模型如何生成单条回答，而是从问题及截至当前检查点的回答前缀中提取可观测状态，预测继续生成是否仍有足够的“残余收益”，再决定停止或生成下一批回答。其核心不是把当前置信度直接当作正确性，而是估计未来计算是否可能把当前答案修复为更好的答案。

完整流程从检查点 $c=4$ 开始，依次考虑 $\mathcal{C}=\{4,8,16,32,64,128\}$。在每个检查点，系统执行答案归一化、Re$^2$聚合和 AEC 特征提取，随后由共享门控网络输出继续概率；若概率低于阈值 $\tau$，返回当前聚合答案，否则只生成到下一个检查点所需的回答，并重新观察状态。训练时可以使用真实答案和未来检查点结果离线构造标签，但这些信息在推理时不会进入控制器。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造分阶段回答前缀

推理器逐步采样回答，形成前缀 $\mathcal{R}_{q,c}=(r_{q,1},\ldots,r_{q,c})$；系统只在这些检查点重新评估，而不是为每个问题预先决定一个最终预算。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、冻结的测试时推理器，以及预设检查点集合 $\mathcal{C}=\{4,8,16,32,64,128\}$。<br>
**输出**：各检查点可用的累计回答前缀、当前累计生成成本 $K_{q,c}$ 以及下一检查点信息。

</div>

**直观理解**：可以把它看成分期追加计算：先让模型给出少量答案，只有在证据显示仍值得继续时，才追加下一批答案。这样容易在中途停止，也不会因为一次错误的预算预测而直接跳到某个终点。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 聚合答案并构造可观测状态

首先将回答映射为规范化候选答案，并用冻结的答案提取、归一化和 Re$^2$ 聚合规则得到 $A(\mathcal{R}_{q,c})$；随后 AEC（Observable Evidence Characterization）从当前及历史检查点信息计算预算与成本、答案分布、时间变化、重解行为和语义状态特征，得到 $s_{q,c}=\phi(q,\mathcal{R}_{q,c},c)$。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、当前回答前缀 $\mathcal{R}_{q,c}$、检查点 $c$、累计成本 $K_{q,c}$ 和固定检查点日程。<br>
**输出**：不含真实答案、未来回答或未来成本的数值状态 $s_{q,c}$。

</div>

**直观理解**：AEC 只描述“目前看到了什么”：答案是否集中、答案是否变化、不同回答在语义上是否相似，以及新一批回答带来了多少新信息。它刻意不判断哪个答案一定正确，避免把正确性偷偷写进输入。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 训练残余收益门控器

对每个检查点计算从当前停止到任意可达未来检查点的成本调整正确性收益；若存在收益超过阈值 $\delta$ 的未来检查点，则令 $y_{q,c}=1$。门控器学习 $p_{\theta}(s_{q,c})=P_{\theta}(y_{q,c}=1\mid s_{q,c})$，并使用类别加权二元交叉熵优化参数 $\theta$。

<div class="method-step__io" markdown="1">

**输入**：训练问题在各检查点的状态 $s_{q,c}$，以及通过离线访问真实答案和后续检查点结果构造的继续标签 $y_{q,c}$。<br>
**输出**：训练完成的共享门控器 $p_{\theta}$、训练集拟合并冻结的特征预处理统计量，以及供部署校准的概率分数。

</div>

**直观理解**：训练目标不是记住当前答案对不对，而是学习一种更实用的判断：从当前状态继续算，是否可能把结果变得更好。未来正确性只作为教师信号，推理时控制器无法看到它。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 顺序分配计算并校准停止阈值

在校准集上选择满足准确率约束的阈值 $\tau^{\star}$；在线时在每个检查点计算门控概率，若 $p_{\theta}(s_{q,c})\geq\tau$ 则 Continue，生成至下一检查点，否则 Stop 并返回当前聚合答案。到达 $c=128$ 时强制终止，停止的问题从后续批量生成中移除。

<div class="method-step__io" markdown="1">

**输入**：新问题的当前回答前缀、训练后冻结的门控器和预先独立保留的校准集。<br>
**输出**：每个问题的停止检查点、最终聚合答案和实际生成成本；整个数据集则得到准确率与计算节省之间的权衡。

</div>

**直观理解**：系统像一个会反复复诊的控制器，而不是一次性预测“要算多少步”：每追加一批回答就重新检查一次。阈值由独立校准集决定，目的是在允许的准确率损失范围内尽量少用计算。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 残余效用优势与继续标签

$$
\Delta U_{q}(c\!\rightarrow\!t)=z_{q,t}-z_{q,c}-\lambda\frac{K_{q,t}-K_{q,c}}{K_{q,\max}},\qquad y_{q,c}=\mathbf{1}\left[\max_{t\in\mathcal{C}:t>c}\Delta U_{q}(c\!\rightarrow\!t)>\delta\right]
$$

**符号说明**

- $q\in\mathcal{Q}$：问题集合中的一个问题。
- $\mathcal{R}_{q,c}$：问题 $q$ 在检查点 $c$ 前已采样回答组成的前缀。
- $c,t\in\mathcal{C}$：当前检查点与可达的未来检查点，其中 $t>c$。
- $z_{q,c}\in\{0,1\}$：当前聚合答案相对于真实答案的正确性，正确为 $1$，错误为 $0$；仅用于离线标签构造和分析。
- $K_{q,c}$：截至检查点 $c$ 的累计生成成本。
- $K_{q,\max}$：到终端检查点 $128$ 的生成成本，用于归一化增量成本。
- $\lambda$：正确性改善与额外计算成本之间的权衡系数。
- $\delta$：判定未来效用优势是否足够大的阈值；实验中取 $0$。
- $y_{q,c}$：二值继续标签，表示至少一个未来检查点具有超过 $\delta$ 的成本调整效用优势。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项比较未来和当前答案是否发生正确性改善，第二项扣除从 $c$ 到 $t$ 的额外生成成本。实验的二值设定下，标签实际等价于预测可恢复性：当前答错但未来某一检查点答对，就应当继续；当前已答对或未来不能修复，则无需继续。<br>
**原文位置**：式（1）—（3），AERA: Adaptive Residual Compute Allocation / Residual-Utility Objective 与 Recoverability as a special case

</div>

</div>

<div class="equation-block" markdown="1">

#### 门控器训练损失与顺序决策

$$
\ell_{q,c}=-w_{1}y_{q,c}\log p_{q,c}-w_{0}(1-y_{q,c})\log(1-p_{q,c}),\qquad \mathcal{L}(\theta)=\sum_{(q,c)\in\mathcal{D}_{\mathrm{train}}}\ell_{q,c},\qquad \pi_{\tau}(s_{q,c})=\begin{cases}\textsc{Continue},&p_{\theta}(s_{q,c})\geq\tau,\\\textsc{Stop},&\text{otherwise}.\end{cases}
$$

**符号说明**

- $s_{q,c}$：AEC 从当前可观测问题、回答前缀、检查点和成本构造的状态。
- $p_{\theta}(s_{q,c})$：参数为 $\theta$ 的门控器预测继续标签为 $1$ 的概率。
- $w_{1},w_{0}$：分别对应正类和负类的类别权重，只在训练问题上计算。
- $\mathcal{D}_{\mathrm{train}}$：用于拟合门控器的训练问题—检查点样本集合。
- $\tau$：在线停止/继续决策的概率阈值。
- $\pi_{\tau}$：由阈值 $\tau$ 定义的顺序分配策略。

<div class="equation-explanation" markdown="1">

**直观理解**：加权交叉熵让门控器在正例稀少时仍重视“确实值得继续”的状态。推理时只需把概率与阈值比较；继续就生成下一块并重新计算状态，停止就返回当前答案，因此训练目标和在线动作直接衔接。<br>
**原文位置**：式（4）及 AERA: Adaptive Residual Compute Allocation / Residual Gate Learning、Sequential Allocation and Calibration

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练数据首先在每个检查点形成可观测状态 $s_{q,c}$。研究者离线应用与评测相同的答案提取、归一化和 Re$^2$聚合规则，利用真实答案得到 $z_{q,c}$，再访问后续检查点的结果和成本，根据残余效用公式生成 $y_{q,c}$；真实答案和未来结果不会进入状态。门控网络通过最小化 $\mathcal{L}(\theta)=\sum\ell_{q,c}$ 学习从状态到继续概率的映射，其中 $w_1$ 和 $w_0$ 用于抵消继续标签稀疏造成的类别不平衡。训练完成后，特征中位数、均值、标准差、语义编码器和投影参数均冻结，避免验证集或测试集信息泄漏。

在当前实验的二值正确性设定中，$y_{q,c}=1$ 等价于“现在错误、未来可恢复”，所以优化的是可恢复性预测而不是完整的连续效用预测。论文明确指出，真实值奖励场景仍可使用式（1）的成本敏感目标，但本文实验主要验证这一二值特殊情形；因此不能把实验结论扩大为已经验证了所有形式的残余效用建模。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. AEC 多源证据状态表示**

AEC 将状态分为五组。预算与成本特征包括当前检查点比例、下一检查点和累计成本；答案分布特征包括最大经验答案比例、归一化熵、唯一答案比例和前两名答案差距；时间特征描述多数答案比例、熵和重解率的变化、首选答案是否改变及其持续时间；重解特征概括重解率及其变化；语义特征包括回答间相似度、围绕语义质心的离散度、质心移动、新回答块的新颖性以及 $32$ 维投影。语义编码器和投影参数在门控器拟合前冻结，缺失值用训练分区的中位数填充，特征标准化统计量也只由训练分区拟合。

> 直观理解：单看多数答案比例可能产生误导，因为答案可能暂时一致后又崩溃，也可能暂时分散后恢复。AEC 因而同时看当前形态、变化趋势、重解行为和语义变化，试图识别“还有没有可恢复空间”。

**2. 残余效用标签与共享门控器**

标签由当前检查点 $c$ 与未来检查点 $t$ 的效用差构造。实验中的正确性 $z_{q,c}$ 是二值变量、$\delta=0$ 且 $0\leq\lambda<1$，因此标签等价于：当前答案错误且存在某个未来检查点变正确，即可恢复性预测。门控器是一个共享所有检查点的两层 MLP，隐藏层维度为 $64$ 和 $32$，使用 LayerNorm、GELU、$0.1$ dropout，并用类别加权损失处理正例稀少问题。

> 直观理解：共享门控器意味着不同检查点使用同一套判断规则，但“当前处于第几阶段”和“还剩多少预算”仍作为输入，因此它能理解决策上下文。标签把研究问题从“当前是否正确”改成“继续计算是否值得”。

**3. 顺序策略与安全校准**

策略为 $\pi_{\tau}(s_{q,c})$：当 $p_{\theta}(s_{q,c})\geq\tau$ 时继续，否则停止。阈值在候选集合 $\mathcal{T}$ 中选择，使校准集成本最小，同时满足 $\operatorname{Acc}_{\mathrm{cal}}(\pi_{\tau})\geq\operatorname{Acc}_{\mathrm{cal}}(\mathrm{Fixed\text{-}128})-\epsilon$；若无可行阈值，则保留全量计算。策略只能逐块推进到下一检查点，不能跳跃到预测的终止预算。

> 直观理解：“继续”不是承诺一定会正确，而是表示当前证据下继续尝试更划算。逐块重观测可以处理非单调轨迹；准确率约束则防止系统为了节省计算而无声地改变目标。

**训练与推理**

训练阶段：对训练问题生成至终端检查点 $128$，在 $4,8,16,32,64,128$ 处保存前缀；对每个前缀计算 AEC 状态，离线用当前与未来正确性构造继续标签，拟合类别加权 MLP。之后只用训练分区拟合预处理统计量和类别权重，并冻结这些统计量以及语义表示模块。阈值不直接由训练损失决定，而是在独立校准集上从候选集合中选择：在满足相对于 Fixed-128 准确率约束的前提下，使校准成本最小；阈值选择和其他模型选择应在测试访问前完成。

推理阶段：每个问题从检查点 $4$ 开始，规范化当前回答并计算 $s_{q,c}$，应用冻结的缺失值填充和标准化，再得到 $p_{\theta}(s_{q,c})$。若该值小于 $\tau$，立即输出当前 Re$^2$聚合答案；若不小于 $\tau$，只生成达到下一个检查点所需的增量回答，然后重新提取特征和评分。问题只能按检查点顺序前进，不能直接跳到预测的终止预算；到达 $128$ 时无条件停止。在线实现按检查点批量处理仍活跃的问题，并将已停止问题从后续生成批次中移除。

**复现信息**

为便于复现和公平解释，关键实现约束包括：门控器是共享所有检查点的两隐藏层 MLP，隐藏维度为 $64$ 和 $32$，使用 LayerNorm、GELU 和 $0.1$ dropout；首个检查点的时间差分使用固定中性值，不读取不存在的前一状态；回答语义特征由冻结编码器和冻结的 $32$ 维投影产生。状态只允许使用 $\mathcal{I}_{q,c}=\{q,\mathcal{R}_{q,1:c},c,K_{q,c},\mathcal{C}\}$ 中的信息，明确排除真实答案、当前或未来检查点正确性、未来回答、未来成本和残余标签。

评估时应区分描述性离线前沿与严格在线协议。论文的冻结阈值增量生成实验先固定 $50$ 个校准问题，再在 $300$ 个未接触的 GSM8K 测试问题上执行；校准所得阈值不能用测试结果回调。由于门控分数没有跨数据集的固定操作含义，每个部署环境都需要独立校准；若准确率约束没有可行阈值，安全行为是保留完整计算，而不是改变优化目标。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：测试集包含 $1{,}319$ 道题，作为数学推理基准，用于评估大规模、相对规则的推理任务。原文未进一步明确训练、校准和测试划分的具体题目数量；普通五折分析按题目划分，保证同一题的所有检查点处于同一折。
- GPQA Diamond：包含 $198$ 道题，作为更困难、知识密集型的问答基准，用于检验方法在高难度任务上的残余计算分配能力。原文未进一步明确其外层测试划分的具体规模。
- 未触碰的 GSM8K 增量生成测试集：包含 $300$ 道题，用于检验冻结阈值在真正独立测试条件下的表现；测试时另外生成配对的 Fixed-128 响应池作为参照。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Re$^2$ 准确率**

使用原始 Re$^2$ 评估器对停止时暴露的响应前缀进行答案提取、重做过滤和聚合，衡量最终答案正确性。 （越高越好；但应结合响应数或令牌数解读，因为更高计算预算通常可能提高准确率。）

</div>
<div class="metric-item" markdown="1">

**每题平均响应数**

统计每道题平均采样了多少个响应，反映响应级推理计算量；它不等同于墙钟延迟或 FLOPs。 （在达到相近准确率时越低越好，因为表示更少的采样计算。）

</div>
<div class="metric-item" markdown="1">

**响应节省率与完成令牌节省率**

响应节省率相对于 $128$ 响应预算定义为 $100(1-\mathbb{E}_{q}[c_q]/128)$，其中 $c_q$ 是题目 $q$ 的停止响应数；完成令牌节省率则统计生成令牌的减少幅度。 （越高越好，但不能单独使用；必须与准确率一起判断是否以可接受的性能代价换取计算节省。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 离线前沿：与检查点对齐的 ESC 比较

<div class="result-value" markdown="1">

在 GSM8K 上，默认五响应一致性窗口的 ESC 平均使用 $20.30$ 个响应并达到 $94.31\%$；在 GPQA Diamond 上平均使用 $115.80$ 个响应并达到 $38.85\%$。作者据此认为 AERA 可在相近准确率范围内暴露明显更少的响应。

</div>

该结果测试的是“答案窗口一致”是否会过于保守。ESC 需要连续窗口达成一致，因此在难题上可能接近完整预算；AERA 的优势若成立，说明停止控制应识别未来继续计算的价值，而不只是等待当前答案稳定。这里的结果只支持相对于该 ESC 配置的效率优势，不能证明 AERA 在所有一致性方法或所有硬件延迟指标上都更优。

<div class="result-source" markdown="1">

来源：Experiments—Offline Accuracy–Compute Frontiers

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Checkpoint-aligned ESC is substantially more conservative: its standard five-response unanimity window uses 20.30 responses on GSM8K and 115.80 on GPQA, obtaining 94.31% and 38.85%, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 离线前沿：与检查点对齐的 ASC 比较

<div class="result-value" markdown="1">

在发布的 $0.95$ 置信阈值下，ASC 在 GSM8K 上达到 $94.43\%$ 准确率、平均使用 $9.40$ 个响应；在 GPQA Diamond 上达到 $38.99\%$、平均使用 $81.82$ 个响应。进一步地，在不超过 AERA 于 $\tau=0.3$ 时计算量的非支配 ASC 混合方案中，配对准确率差为 GSM8K 的 $-0.09$ 个百分点，$95\%$ 置信区间为 $[-0.30,+0.09]$；GPQA 的差为 $-0.93$ 个百分点，区间为 $[-3.45,+1.46]$。

</div>

ASC 是更有竞争力的直接基线，因此该比较比 ESC 更能检验 AERA 的独特价值。区间均跨过零，作者将其解释为总体准确率“相当”而非 AERA 普遍优于 ASC；AERA 的可取之处主要可能在于相近准确率下的计算分配方式。该结果也提醒读者，不应把某个离线前沿点解读成经过独立测试集校准的部署性能。

<div class="result-source" markdown="1">

来源：Experiments—Offline Accuracy–Compute Frontiers

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Against nondominated ASC mixtures using no more computation than AERA at τ=0.3, the paired differences are -0.09 points on GSM8K (95% CI [-0.30,+0.09]) and -0.93 on GPQA ([-3.45,+1.46]), establishing comparable rather than uniformly superior aggregate accuracy.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 冻结阈值的增量生成：未触碰的 300 道 GSM8K 测试题

<div class="result-value" markdown="1">

在冻结阈值增量生成评估中，AERA 达到 $92.61\%$ 准确率；$128$ 响应参照达到 $93.01\%$，同时 AERA 将完成令牌减少 $95.99\%$。

</div>

这是最直接的部署式检验：阈值先在校准题上选择，之后冻结，再访问不相交测试题；因此它比回顾性离线前沿更能检验阈值选择是否泛化。结果表明，AERA 以约 $0.40$ 个百分点的准确率差换取极大的完成令牌节省，但它并不证明墙钟时间、能耗或 FLOPs 同样减少，因为实验主要报告令牌和响应层面的计算量。

<div class="result-source" markdown="1">

来源：Abstract；Experiments—Metrics and Evaluation Protocols

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In a frozen-threshold incremental-generation evaluation on 300 untouched GSM8K questions, AERA achieves 92.61% accuracy versus 93.01% with 128 responses while reducing completion tokens by 95.99%.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评估依赖冻结的 Qwen2.5-7B Re$^2$ reasoner、固定采样设置和最多 $128$ 个响应；原文未报告不同模型、提示词、采样温度或更大预算下的结果，因此方法的跨模型和跨任务可迁移性仍未得到充分验证。
- 主要计算指标是平均响应数和完成令牌节省率，而不是墙钟延迟、FLOPs、显存或真实服务成本；此外，普通离线前沿中的代表点是回顾性选择的描述性点，且 ESC、ASC 等基线的完整数值前沿在所提供章节中并不完整，部署结论需要进一步的独立、多硬件和完整成本评估。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 固定预算：始终在 $4$、$8$、$16$、$32$、$64$ 或 $128$ 个响应处停止，用来测量不进行题目级自适应时的完整准确率—计算量前沿。
- 证据启发式与随机控制：前者在多数回答比例、语义共识或归一化熵达到阈值时停止，检验简单的当前置信度信号是否足够；Matched random 将 AERA 选出的检查点在题目间打乱但保持预算分布，用来排除仅由平均预算分布带来的收益。
- 一次性分配：只根据检查点 $4$ 的状态预测最终停止点，且不能修正决定，用来检验 AERA 在后续检查点反复读取证据并更新决策是否必要。
- 检查点对齐的 ESC 与 ASC：ESC 使用窗口一致性规则，默认窗口长度为 $w=5$；ASC 使用 Beta 后验停止准则，默认置信参数为 $C=0.95$。二者都被限制在与 AERA 相同的检查点和动作空间内，因此直接比较的是停止控制策略，而不是响应池或评估器差异。

**实验想回答的问题**

- 在相同响应池、检查点和聚合规则下，AERA 是否能比固定预算、基于当前证据的启发式以及已有自适应停止方法取得更好的准确率—计算量权衡？
- 当阈值只用校准数据选择、并在接触独立测试集前冻结时，AERA 的节省计算量和准确率表现是否仍然成立？

**实验实现**

实验控制冻结的 Qwen2.5-7B Re$^2$ reasoner；采样温度为 $0.6$，$top\text{-}p=0.95$，最大生成长度为 $16{,}384$ 个令牌。每题最多生成 $128$ 个响应，并只在检查点集合 $\{4,8,16,32,64,128\}$ 暴露累计响应前缀。离线顺序重放先完整生成响应池，但控制器在每次决策时只能看到当前检查点状态，不能访问规范答案正确性；选择停止点后，再用同一 Re$^2$ 规则评分。普通分析采用五个按题目划分的折；特征预处理和优化在互补题目上进行，留出折损失用于提前停止。嵌套分析进一步把每个外层训练划分为模型训练、内部验证和校准部分，分别用于训练、选择训练时长和选择阈值，最后在外层折上只评估一次冻结的模型—阈值对。AERA 控制器使用 $55$ 个数值输入，语义特征由冻结的轻量级句子编码器压缩到 $32$ 维；门控参数为 $\lambda=0.10$，使用 Adam、学习率 $10^{-3}$、权重衰减 $10^{-4}$、最多 $300$ 个 epoch、耐心值 $25$。阈值前沿报告 $\tau\in\{0.1,\ldots,0.9\}$；作者明确指出表格中的代表点是回顾性选择的描述性点，而非独立校准的运行点。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 证据启发式、一次性分配与 AERA 的控制策略对照 | 原文给出了多数比例、语义共识、归一化熵、Matched random 和一次性分配等完整控制，但所提供章节未报告这些控制在表格或图中的具体数值，也未提供单独的组件移除结果。 | 这些对照所要隔离的是 AERA 的两个关键属性：是否使用多类检查点可观测特征，以及是否允许在后续检查点重新决策。随机控制检验预算分布本身的影响，一次性分配检验顺序更新的价值，证据启发式检验当前稳定性信号是否足够。由于具体数值未提供，不能据此量化每个组件的独立贡献。 | Experiments—Baselines<br><span class="experiment-evidence">Matched random shuffles AERA’s selected checkpoints across questions, exactly preserving its empirical budget distribution.</span> |
| 普通五折分析与嵌套校准协议 | 原文明确区分两种协议：普通五折分析用于描述性前沿，但不是未触碰外层测试估计；嵌套分析在外层训练划分内再分为模型训练、内部验证和校准分区，并在外层折上评估冻结的模型—阈值对。原文未报告该协议相对于另一协议的独立准确率或令牌节省差值。 | 这不是模型结构消融，而是评估可靠性检查。它测试的是阈值和训练时长是否无意中使用了外层评估信息；嵌套协议把模型选择、阈值选择和最终评估分开，因此更接近真实部署流程。缺少两种协议的数值并列结果时，只能确认实验设计降低了测试泄漏风险，不能判断嵌套校准会带来多大性能损失。 | Experiments—Question-level splits<br><span class="experiment-evidence">This protocol is useful for descriptive frontiers but is not an untouched outer-test estimate.</span> |

**定性案例**

- 原文摘要指出检查点级正确性会非单调变化：可观测证据可能在答案崩溃前增强，也可能在答案恢复前减弱。该定性现象解释了为什么 AERA 不把当前置信度直接等同于正确性，而是使用累计响应前缀的答案分布、时间、重解、语义和计算特征来估计继续生成的潜在收益；但所提供实验章节没有给出具体题目的逐步轨迹或可复核图示，因此不能进一步归因于某一道题的具体错误恢复过程。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出根据未来计算收益自适应分配测试时推理预算的方法，核心同时涉及高效推理控制与推理性能提升。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`ad249c46f72bc3eef3d755e2e6225c4521a19ef81ec0f7f37ca7274a7f69c43f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
