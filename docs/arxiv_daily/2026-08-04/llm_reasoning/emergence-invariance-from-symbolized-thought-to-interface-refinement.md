---
title: "[论文解读] Emergence Invariance: From Symbolized Thought to Interface Refinement"
description: "[arXiv 2608.01548][LLM Reasoning] 本文提出“涌现不变性”框架，用于区分扩大模型规模所能缩小的补偿差距与任务接口本身造成、无法仅靠规模消除的信息下限。"
arxiv_id: "2608.01548"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:03:42.993341+00:00"
source_sha256: "a4d1aa5e062ba0c7bc70520456c5b44e7b732eea5b506f45d086ac4e386e0bf2"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "涌现不变性"
  - "补偿性涌现"
  - "符号化子结构"
  - "任务接口"
  - "接口细化"
  - "贝叶斯风险"
  - "补偿差距"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.01548</p>

# Emergence Invariance: From Symbolized Thought to Interface Refinement

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Yi Liu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> MS Student, School of Astronomy and Space Science；University of Science and Technology of China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01548v1) · [PDF 下载](https://arxiv.org/pdf/2608.01548v1) · **关键词** 涌现不变性, 补偿性涌现, 符号化子结构, 任务接口, 接口细化, 贝叶斯风险, 补偿差距<br>


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

本文提出“涌现不变性”框架，用于区分扩大模型规模所能缩小的补偿差距与任务接口本身造成、无法仅靠规模消除的信息下限。

**不用术语来说**：更大的语言模型可以通过上下文学习、推理和工具使用弥补简单底层机制的不足，但如果完成任务所需的关键信息从未被模型观察、保留、表示或处理，那么“思考得更久”是否仍能解决问题并不清楚。本文关注的正是这一边界：哪些缺陷可以依靠模型能力增长来补偿，哪些缺陷必须通过改造模型与任务环境之间的接口来消除。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出“涌现不变性”，将最优风险分解为接口决定的不可约下限与随规模变化的补偿差距，从而形式化地区分“扩大模型”与“细化接口”两种改进路径。
- 作者给出两个核心判据：总补偿成立当且仅当接口下限和渐近补偿差距同时消失；在固定输入分布下，一个接口普遍不比另一个信息更少，当且仅当其完备信息 $\sigma$-代数细化后者。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型涌现能力、计算表达力与信息受限决策的交叉位置。Transformer 在一定假设下具有广泛的函数逼近和计算表达能力，扩大参数、数据或推理计算也能带来上下文学习、多步推理与工具使用；但这些能力都只能处理模型接口实际保留的信息。本文因此不把“模型能否表示某种计算”与“模型能否从当前输入中完成任务”混为一谈，而是研究一个更具体的问题：当一族不同规模的模型共享同一任务接口 $\phi$ 时，性能提升能否弥补接口丢失的任务相关区别。这里的接口广义地包括观察、语言表达、上下文记忆、内部表示与监督信号；若两个真实状态经接口后完全相同，却要求不同决策，那么仅增加固定接口内的模型能力原则上无法可靠地区分它们。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**补偿性涌现**

指规模化训练使简单的基础机制组合出上下文学习、多步推理、工具使用等原先未被逐项硬编码的能力。本文把它理解为模型逐渐缩小固定接口下的实现或推理不足，而不预设它能恢复接口已经删除的信息。

</div>
<div class="concept-item" markdown="1">

**任务接口**

任务接口 $\phi$ 是把底层真实状态映射为模型可观察、可记忆或可表示内容的机制，例如文本提示、位置编码、上下文窗口或假设语言。不同底层状态若被 $\phi$ 映射为同一观察，就形成接口碰撞，模型无法仅凭该观察确定它们之间被抹去的区别。

</div>
<div class="concept-item" markdown="1">

**贝叶斯风险与接口下界**

贝叶斯风险是在给定可用信息后，所有可能决策规则能够达到的最小期望损失；本文以 $\mathcal{R}_{\phi}^{*}$ 表示接口 $\phi$ 所决定的不可约风险。它不是某个具体模型训练不充分造成的误差，而是当前接口对任务信息保留不足时任何模型都可能面对的下界。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文考虑由规模指标 $s$ 标记的一族模型，它们通过共同接口 $\phi$ 接收任务相关信息，并输出预测、判断或行动；任务损失用于衡量输出与正确决策之间的差异。基本设定要求区分两类限制：接口自身造成的最优风险 $\mathcal{R}_{\phi}^{*}$，以及规模为 $s$ 的具体系统尚未达到该最优值所留下的补偿差距 $C_s$，二者满足风险分解 $\mathcal{R}_{s}^{*}=\mathcal{R}_{\phi}^{*}+C_s$。在保持 $\phi$ 不变时，扩大规模或增加思考计算可以降低 $C_s$，但若接口把需要不同答案的状态压成相同观察，正的 $\mathcal{R}_{\phi}^{*}$ 仍会保留；要消除这部分误差，必须细化观察、记忆、表示或监督接口，使模型获得原来缺失的任务相关区别。该框架默认在固定输入分布下比较接口的信息量，并以接口生成的完备 $\sigma$-域是否包含另一接口的信息来刻画普遍意义上的信息细化。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\phi$**

任务接口，即从底层状态或认知内容到模型可用观察、记忆、表示或监督信息的映射。

</div>
<div class="notation-item" markdown="1">

**$s$**

模型族的规模指标，可抽象表示参数、数据、训练计算或测试时推理计算的规模。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{R}_{\phi}^{*}$**

在接口 $\phi$ 所提供的信息下，所有决策规则能够达到的最小风险，即由接口决定的不可约性能下界。

</div>
<div class="notation-item" markdown="1">

**$C_s$**

规模为 $s$ 的系统相对接口最优风险仍存在的补偿差距；规模化可能使其减小。

</div>

</div>

**直接相关的工作**

- **Yun et al., “Are Transformers Universal Approximators of Sequence-to-Sequence Functions?” (ICLR 2020)**: 该工作支持 Transformer 在特定假设下具有广泛函数逼近能力，是本文区分“架构可表达某种映射”与“接口是否提供完成该映射所需信息”的理论背景。本文并不否定通用逼近结果，而是指出表达能力不能自动跨越由接口碰撞产生的信息下界。
- **Wei et al., “Emergent Abilities of Large Language Models” (TMLR 2022)**: 该工作代表关于模型能力随规模出现显著变化的涌现研究。本文进一步提出“补偿性涌现”的解释框架：规模增长能够缩小固定接口内的能力差距 $C_s$，但是否能实现完全补偿还取决于接口下界 $\mathcal{R}_{\phi}^{*}$ 是否为零。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

LLM 的规模增长能够带来多步推理、工具调用等涌现能力，但真实任务还受到输入可观测性、记忆保持、内部表示、可执行计算和优化目标的共同约束。若不区分能力不足与接口缺失，研究者可能继续增加参数或推理预算，却无法突破由缺失任务相关区分所造成的性能下限，因此需要一个能指导架构与规模联合设计的边界理论。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **规模扩展与推理增强**：通过增加模型规模、训练量或测试时思考强度，使学习器在既定接口提供的信息上形成更强的规则与推理过程，主要作用是缩小随规模变化的补偿差距。
- **任务接口与架构细化**：通过改进模型能够观察、保留、表示、计算或优化的内容，保留既有任务相关区分并暴露新的关键区分，从信息来源和处理条件上降低接口造成的不可约风险。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 只扩大模型或增加思考强度仍受固定接口约束；当决定答案的区别没有进入可用信息时，规模只能逼近而不能越过正的接口下限。
- 已有关于 grounding、记忆、位置、注意力、贝叶斯继承、科学溯因和推理控制的结果分别揭示局部障碍，但缺少一个统一判据来判断某项失败究竟源于尚未充分学习，还是源于接口没有提供必要区分。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一个同时刻画“接口内的能力增长”和“接口本身的信息改进”的统一形式框架，尤其缺少关于总补偿何时可能、接口之间何时具有普遍信息优势的充要条件。

</div>
<div markdown="1"><span>核心问题</span>

对于通过共享任务接口 $\phi$ 工作、由规模 $s$ 索引的一族学习器，涌现能力能否补偿所有缺失区分；若不能，怎样严格判定剩余误差来自可随规模缩小的补偿差距，还是来自必须通过接口细化才能消除的正下限？

</div>
<div markdown="1"><span>作者直觉</span>

模型只能利用接口实际暴露并允许其保留和处理的区别。扩大规模相当于让学习器更充分地挖掘现有信息，而接口细化相当于把此前不可见或已丢失的关键线索加入可用信息；因此，前者提高“如何利用已有线索”的能力，后者改变“究竟有哪些线索可用”。这解释了作者的设计原则：“scale the learner, and refine what the learner can observe, retain, represent, compute, and optimize”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是提出一个新的神经网络训练算法，而是建立一套“接口—决策风险”分析框架，用来区分两类能力改进：一类是在固定接口$\phi$内增加参数、数据、优化质量或推理计算，从而缩小模型相对该接口最优决策的补偿差距$C_s$；另一类是细化观察、记忆、表示、位置、路由或目标接口，使系统能够区分此前被压缩为同一观测的任务状态，从而降低接口本身的贝叶斯风险下界$\mathcal{R}_{\phi}^{*}$。这里的接口$\phi$是从完整任务状态$X$到模型实际可用信息$\phi(X)$的映射；若两个状态经接口后相同，它们就属于同一个等价类，即使正确动作不同，任何只依赖$\phi(X)$的模型也无法可靠地区分它们。

端到端方法先把语言或系统输入形式化为部分符号化及其诱导的信息接口，再对给定损失定义该接口下所有可能决策规则可达到的最小风险；随后把某一规模$s$的模型风险分解为接口下界与补偿差距，并用精确碰撞、近似碰撞和信息$\sigma$-域精化刻画哪些错误能由更多计算消除、哪些必须改变接口。直观地说，固定接口内扩展模型相当于让解题者在同一张信息不完整的试卷上思考得更充分；接口精化则相当于补上被遮住的条件、恢复关键记忆或提供可执行工具。前者只能更充分利用已有区别，后者才能恢复原先根本看不见的区别。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 任务状态与有效接口建模

将模型可访问的信息统一写成接口映射$\phi:X\mapsto\phi(X)$，并用关系$x\sim_{\phi}x'$表示$\phi(x)=\phi(x')$；由此把完整状态空间划分为接口等价类。若讨论语言符号化，则先以部分映射$E:\mathcal{T}\rightharpoonup\Sigma^{*}$表示只有认知内容子集$\mathcal{T}_{\rm sym}$能够被表达，再考察该符号通道向后续决策接口传递了哪些区别。

<div class="method-step__io" markdown="1">

**输入**：完整任务状态随机变量$X$、目标$Y$、动作或预测空间、损失函数$\ell$，以及模型实际获得的观察、上下文、记忆、表示和目标信号。<br>
**输出**：任务相关的接口$\phi$、接口诱导的等价类，以及模型在决策时实际拥有的信息结构。

</div>

**直观理解**：这一步先明确模型究竟“看到了什么”，而不是把完整世界状态误当成模型输入。凡是被接口映射成同一记录的状态，对下游模型而言就是不可区分的观测双胞胎。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算接口风险下界

在所有仅依赖$\phi(X)$的可测决策规则中取最小期望损失，得到接口贝叶斯风险$\mathcal{R}_{\phi}^{*}$。对于零一损失下的等概率精确碰撞，若$x_0\sim_{\phi}x_1$但$Y(x_0)\neq Y(x_1)$，则任何确定性或随机规则在该配对上的平均错误率至少为$1/2$。

<div class="method-step__io" markdown="1">

**输入**：接口观测$\phi(X)$、目标$Y$、输入联合分布和损失$\ell$。<br>
**输出**：固定接口下任何规模模型都不能突破的风险下界$\mathcal{R}_{\phi}^{*}$，以及由碰撞构造得到的可检验误差地板。

</div>

**直观理解**：如果同一份可见信息对应两个不同正确答案，模型无论想多久都只能猜。该下界不是当前模型不够强造成的，而是输入接口已经删除了决定答案所需的区别。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分离规模补偿与接口缺失

把每个规模的风险写成$\mathcal{R}_{s}^{*}=\mathcal{R}_{\phi}^{*}+C_s$，其中$C_s\geq0$衡量该模型族尚未达到接口贝叶斯最优值的差距；再检查随参数、训练数据、优化或测试时计算增加时，$C_s$是否趋近于零。该分析把“信息已经存在但模型不会利用”与“信息根本不在接口中”分开。

<div class="method-step__io" markdown="1">

**输入**：共享同一接口$\phi$的规模索引模型族，以及各规模$s$可达到的最优风险$\mathcal{R}_{s}^{*}$。<br>
**输出**：规模相关的补偿差距$C_s$、规模不变的接口下界$\mathcal{R}_{\phi}^{*}$，以及总补偿是否可能的判定。

</div>

**直观理解**：模型变强可以减少读题、搜索和推理上的失误，即缩小$C_s$；但若题目漏掉关键条件，变强不能把正的$\mathcal{R}_{\phi}^{*}$变成零。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 接口精化与匹配干预验证

在固定输入分布下，比较$\phi(X)$与$\psi(X)$生成的完备信息$\sigma$-域；当$\sigma(\phi(X))$包含于$\sigma(\psi(X))$时，$\psi$保留原有区别并可能增加新区别，因此对所有决策问题普遍不劣。经验上分别实施“只增加 thinking 计算”“保持观测完全相同的精确双胞胎”以及“恢复决定性记忆或可执行语义”等干预，观察性能变化来自$C_s$下降还是$\mathcal{R}_{\phi}^{*}$移动。

<div class="method-step__io" markdown="1">

**输入**：原接口$\phi$、候选新接口$\psi$，以及分别操纵思考计算和任务信息的匹配任务对。<br>
**输出**：候选接口是否构成信息精化的理论结论，以及补偿增益、接口地板和精化增益三种经验信号。

</div>

**直观理解**：匹配实验一次只改变一个因素：多想是在同一信息上计算，恢复记忆或工具则是增加信息。若前者对可解任务有效、对观测双胞胎无效，而后者能解除地板，就符合理论预测。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 涌现不变风险分解

$$
\mathcal{R}_{s}^{*}=\mathcal{R}_{\phi}^{*}+C_{s}
$$

**符号说明**

- $\mathcal{R}_{s}^{*}$：规模索引为$s$的模型族成员在给定任务上可达到的最优期望风险。
- $\mathcal{R}_{\phi}^{*}$：只允许决策依赖接口观测$\phi(X)$时，在全部可测决策规则中取得的贝叶斯最小风险；它是固定接口的不可约风险地板。
- $C_s$：规模$s$的模型相对接口贝叶斯最优规则的补偿差距，定义为$\mathcal{R}_{s}^{*}-\mathcal{R}_{\phi}^{*}$，且非负。
- $s$：模型规模索引，可概括参数、训练数据、优化能力或测试时计算等扩展轴。
- $\phi$：把完整状态$X$映射为模型实际可访问信息$\phi(X)$的任务接口。

<div class="equation-explanation" markdown="1">

**直观理解**：该式是全文的核心分解：总错误由接口已经造成的不可约部分和模型尚未充分利用现有信息的部分组成。扩大模型或增加思考可以压低$C_s$，但在保持$\phi$不变时，正的$\mathcal{R}_{\phi}^{*}$不会随规模消失。<br>
**原文位置**：摘要、Section 3 的涌现不变分解；并在 Theorem 5 证明与 Corollary 6 中重复使用

</div>

</div>

<div class="equation-block" markdown="1">

#### 总补偿充要条件

$$
\inf_{s}\mathcal{R}_{s}^{*}=0\quad\Longleftrightarrow\quad \mathcal{R}_{\phi}^{*}=0\ \text{ and }\ \inf_{s}C_{s}=0
$$

**符号说明**

- $\inf_s\mathcal{R}_{s}^{*}$：在整个规模模型族上能够逼近的最低任务风险。
- $\mathcal{R}_{\phi}^{*}$：当前接口所允许的贝叶斯最小风险。
- $\inf_s C_s$：随模型族扩展后仍残留的最小补偿差距。
- $\inf$：下确界，表示模型族可能无限逼近而不要求某个有限规模实际达到的最低值。

<div class="equation-explanation" markdown="1">

**直观理解**：任务风险能够趋近于零必须同时满足两个条件：接口中已经包含足以确定正确决策的信息，并且模型族最终能够充分利用这些信息。对于有限确定标签和零一损失，第一项为零等价于目标$Y$可由$\phi(X)$生成的完备信息$\sigma$-域测得；若任一条件失败，仅靠规模扩展都不能实现总补偿。<br>
**原文位置**：Equation (13), Theorem 5（Total-compensation criterion）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：论文主要提出决策论框架和黑盒匹配实验，没有训练新的模型，也没有给出用于参数更新的统一训练损失。文中关于推理控制的$J_{\lambda}(H_t)$、计算成本惩罚和可执行有效性奖励属于候选目标接口的理论说明：它们表明只监督最终答案会把答案分布相同的不同推理过程压缩到同一目标等价类，而加入计算成本或过程有效性后才可学习扩展、剪枝与停止的区别；这些公式并未在所述 DeepSeek API 实验中用于训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 接口商空间与碰撞模块**

接口$\phi$将所有满足$\phi(x)=\phi(x')$的状态归入同一纤维或等价类。只要某个等价类内部存在不同目标或最优动作，接口就产生任务相关碰撞；精确碰撞给出严格误差下界，近似碰撞则可用接口分布之间的总变差距离刻画接近$1/2$的二元测试误差。

> 直观理解：该模块负责定位错误究竟是不是由“不同世界看起来完全一样”造成的。它把抽象的感知缺失、遗忘、位置混淆和表示不足统一成同一种可检查结构。

**2. 规模风险分解模块**

对共享接口的规模索引模型族，定义接口最优风险$\mathcal{R}_{\phi}^{*}$和模型族在规模$s$上的最优风险$\mathcal{R}_{s}^{*}$，两者之差为$C_s$。参数、数据、优化和测试时计算可以改变$C_s$，但只要有效接口不变，就不能降低由接口碰撞产生的正下界$\mathcal{R}_{\phi}^{*}$。

> 直观理解：这一模块将性能差拆成“模型还没把现有信息用好”和“现有信息本来就不够”两部分，因此能判断下一步应增加计算还是修改系统接口。

**3. 信息精化与双向推理控制模块**

接口精化通过完备$\sigma$-域包含关系定义：新接口若保留旧接口的全部可测事件并增加任务相关事件，就在所有决策问题上普遍不劣。对于推理控制，论文还以嵌套假设语言$H_0\subseteq H_1\subseteq\cdots$表达表示空间扩展：复杂度惩罚负责奥卡姆式压缩，而扩展假设空间负责在当前语言不足时增加可表示区别；仅依据最终答案的目标无法区分答案分布相同但计算成本或执行有效性不同的推理轨迹。

> 直观理解：系统不仅要决定“想多久”，还要判断现有观察、记忆和概念是否足够。信息足够时应剪枝和停止，信息或表示不足时则应调用检索、工具、实验或扩展假设空间。

**训练与推理**

训练阶段不适用，实验直接调用已有的 DeepSeek V4-Flash API。推理与评估阶段采用匹配设计：对同一任务条件分别使用直接回答和 thinking 模式，以改变测试时计算而尽量保持观察接口不变；随后构造接口碰撞，使两个需要不同答案的世界向模型提供完全相同的有效证据，检验性能是否停留在理论构造地板；最后只恢复决定答案的记忆、语义支持或关系信息，形成精化接口，再比较匹配性能。理论分析把第一类变化解释为可能降低$C_s$，把第二类碰撞解释为暴露$\mathcal{R}_{\phi}^{*}$，把最后的恢复操作解释为改变接口生成的信息$\sigma$-域并移动风险下界。

该流程的输出不是单一排行榜成绩，而是结构化诊断：若 thinking 在答案已可由接口信息确定时显著改善表现，说明原模型存在可由计算弥补的补偿差距；若精确观测双胞胎在增加思考后仍保持机会水平，则支持正接口地板；若补回决定性记忆后匹配任务达到正确解，则说明此前失败来自接口缺失而非推理能力绝对不足。作者将这些 API 结果定位为初步证据，并明确提出后续需在本地模型上分别控制参数量、数据量和训练计算，验证共享碰撞接口的规模曲线是否收敛到同一地板。

**复现信息**

公平解释结果所需的关键信息是：研究使用同一 DeepSeek V4-Flash API 条件进行直接模式与 thinking 模式的匹配比较，并将观察、记忆和可执行语义接口作为独立干预变量；pointer chasing 用于测试在相关区别已存在时增加推理计算能否缩小$C_s$，精确 observational twins 用于测试固定接口的$1/2$构造地板，恢复 decisive memory 的配对用于测试接口精化是否移动该地板。长上下文部分还将普通随机访问检索作为能力控制，与关系选择或无编号序数访问压力测试区分开，避免把“模型能从上下文取回文本”等同于“模型能利用任务所需的关系接口”。

原文节选没有完整给出 API 参数、温度、随机种子、提示词模板、重复采样策略、具体模型版本快照、失败调用处理规则及全部任务实例，因此不能据此完全复现实验；这些项目均为原文未明确报告。论文自己也把当前结果称为 initial validation 或 preliminary support，而非跨规模因果验证，并计划通过本地部署模型、固定接口及逐项精化来控制参数、数据与训练计算轴。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 合成算法与因果任务套件：包括指针追踪、置换、3SUM、被动因果干预和模拟器识别。各任务直接在提示中提供求解所需信息，用于检验模型在固定且信息充分的接口上能否通过额外思考恢复可执行算法或利用已有因果区分。原文未说明训练集、验证集或测试集划分，属于API黑盒评测实例。
- 接口碰撞与精化套件：观察孪生任务构造可见证据完全相同但正确世界标签相反的成对因果世界；记忆任务比较共享可见后缀的截断历史与包含决定性早期比特的完整历史；假设语言任务比较受限解释器与可扩展解释器。其作用是分别测试观察、记忆和可执行语义接口造成的性能下限。原文未报告传统数据划分。
- 长上下文检索与关系压力套件：普通键值和规则检索最多加入$2{,}048$个干扰项，作为基础检索能力对照；关系压力测试在$2{,}048$、$8{,}192$和$32{,}768$个竞争项下考查分散键绑定、五属性合取匹配、八跳图组合、有效修订选择、相对锚点偏移、无显式索引的序数访问以及权限优先级判断。关系套件每个任务和模式原则上重复两次，共完成79次调用。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**有效答案准确率**

在被判定为格式或语义有效的回答中，正确回答所占比例；表2除标注为paired的项目外均采用该口径。该指标同时依赖求解正确性与有效性筛选，因此需结合有效回答数量解释。 （越高越好，因为表示模型在可评分回答上更稳定地得到正确答案。）

</div>
<div class="metric-item" markdown="1">

**成对得分**

对共享同一可见接口、但真实答案相反的成对实例联合计分。观察孪生或截断记忆条件下，一个相同且有效的回答只能在一对实例中的一个上正确，因此构造下限为$0.5$。 （在碰撞条件中不能简单理解为越高越好；保持在$0.5$是接口不可区分性的预测信号，而接口精化后升至$1.0$才表示关键区分已恢复。）

</div>
<div class="metric-item" markdown="1">

**端到端准确率**

长上下文压力测试中，按全部已完成调用统计最终回答正确比例，用来揭示随着竞争项数量增加，检索、关系选择和推理的联合退化。 （越高越好，因为它表示整个长上下文处理流程成功，而不只是局部找到了某个键值。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 固定且任务相关区分可见的算法与因果任务，比较Direct和Thinking。

<div class="result-value" markdown="1">

Thinking将指针追踪从$0/16$提高到$14/16$、置换从$9/16$提高到$16/16$、3SUM从$8/16$提高到$16/16$；被动因果干预从$162/200$提高到$200/200$，模拟器识别从$35/48$提高到$48/48$。

</div>

作者据此主张，额外串行计算能够恢复输入中已经具备信息支持的算法和因果区分。分析上，这说明Thinking可显著缩小特定API与合成任务上的补偿差距，但没有证明参数规模增长具有相同作用，也没有证明提升可泛化到自然数据、其他模型或所有信息充分任务。

<div class="result-source" markdown="1">

来源：第5.2节，Result I

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Thinking raises pointer chasing from 0/16 to 14/16, permutation from 9/16 to 16/16, and 3SUM from 8/16 to 16/16. On passive causal intervention questions it raises accuracy from 162/200 to 200/200; on simulator identification, from 35/48 to 48/48.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 观察孪生与记忆碰撞任务：成对实例具有相同可见证据或相同可见后缀，但正确答案由被隐藏的信息决定。

<div class="result-value" markdown="1">

观察孪生在Direct和Thinking下的100个stage均得到$0.5$成对得分；截断记忆的24个Direct回答及13个有效Thinking回答也均为$0.5$，而完整记忆在两种模式下均为$48/48$。

</div>

作者将不随Thinking改变的$0.5$解释为接口碰撞的行为签名：如果两种真实状态在模型可见输入中完全相同，增加计算不能决定缺失的那一比特。完整记忆达到满分则表明恢复关键区分能够移动性能下限。不过，这一结论严格适用于人工构造的精确孪生；它不表示现实任务中的所有错误都源于接口缺失，也不能排除无效回答筛选对Thinking记忆结果的影响。

<div class="result-source" markdown="1">

来源：第5.3节，Result II；表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across 100 stages per mode, the paired score is exactly 0.5 with thinking disabled and enabled. Full-context instances score 48/48 in both modes. When paired histories share the visible suffix but the decisive earlier bit differs, every valid response receives a 0.5 paired score: 24/24 direct responses and all 13 valid thinking responses.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 受限与可扩展假设语言条件，比较解释器提供的可执行语义支持，并分别运行Direct和Thinking。

<div class="result-value" markdown="1">

受限解释器下，Direct没有产生有效的留出预测，Thinking仅为$1/16$；可扩展解释器下，Direct有效性为$2/16$，Thinking达到$16/16$。

</div>

作者据此区分表示支持与思考计算的互补作用：解释器必须先允许表达并执行所需假设，Thinking才能充分利用这种支持。该结果并不意味着扩大任意输出词表都会带来满分，也未证明表示接口单独足够，因为可扩展接口在Direct下仍只有$2/16$，满分依赖接口精化与Thinking共同出现。

<div class="result-source" markdown="1">

来源：第5.4节，Result III；表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under a restricted interpreter, direct decoding produces no valid held-out executable prediction and thinking produces 1/16. Under an extensible interpreter, validity rises to 2/16 direct and 16/16 with thinking.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 研究只报告单一DeepSeek V4-Flash API的黑盒匹配实验，没有在本地模型上控制参数量、训练数据和训练计算；因此尚未直接验证不同规模曲线是否收敛到同一接口下限。作者也明确把受控本地缩放列为下一阶段。
- 多数任务是小样本人工构造，部分条件仅有16、24或48个实例，长上下文关系任务每种任务与模式仅重复两次；同时缺少随机种子、置信区间、提示模板与无效回答处理细节。尤其截断记忆的Thinking仅有13个有效回答，可能使跨模式比较受到选择效应影响。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Direct模式：关闭额外思考，直接生成答案。它与Thinking模式使用匹配的任务接口，因此是衡量测试时串行计算是否缩小补偿差距的核心基线。
- Thinking模式：开启模型的思考能力，但保持可见观察、记忆和表示接口不变。它不是另一种模型架构，而是用于隔离额外推理计算影响的实验条件。
- 碰撞接口条件：包括观察孪生、截断记忆和受限解释器。它们有意删除或合并决定答案的区分，用来检验思考是否能从不可区分的输入中恢复缺失信息。
- 精化接口条件：包括完整记忆和可扩展解释器。它们恢复决定性历史信息或扩大可执行语义支持，与对应碰撞条件配对，用来判断性能变化来自接口精化还是单纯增加思考。

**实验想回答的问题**

- 在任务所需区分已经包含于输入接口时，增加测试时思考计算能否缩小模型的补偿差距，即提高算法执行、因果判断和关系推理的正确率？
- 当两个任务状态经过观察、记忆或表示接口后不可区分时，额外思考能否突破由接口信息缺失造成的性能下限；反之，恢复关键区分是否会移动该下限？

**实验实现**

实验是匹配的DeepSeek V4-Flash API黑盒研究，核心控制变量是是否启用Thinking；在接口碰撞与精化比较中，模型和任务形式保持匹配，只改变可见观察、历史记忆或解释器支持。观察孪生每种模式评测100个stage；被动干预为200题；截断记忆Direct有24个成对样本，Thinking仅报告13个有效回答；完整记忆两种模式各48题；表示支持任务每种条件为16题。长上下文关系压力测试在三个竞争规模上运行，图3注明Direct/Thinking完成调用数分别为$14/14$、$14/13$和$12/12$。原文节选未明确报告温度、采样次数、随机种子、完整提示模板、API版本日期、无效回答判定细则或置信区间，因此结果应视为初步行为证据，而非受控缩放实验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 记忆接口消融：从完整上下文中删除决定答案的早期比特，使成对历史仅共享可见后缀，再恢复完整记忆。 | 截断后，Direct的24个成对回答和Thinking的13个有效回答均为$0.5$；恢复完整上下文后，两种模式均为$48/48$，即从构造下限$0.5$移动到$1.0$。 | 该消融隔离了“关键记忆是否可见”：Thinking保持不变时，仅恢复决定性历史信息就消除了碰撞。它支持接口精化能够改变可达性能上限的解释，但Thinking条件存在无效回答，且原文未报告这些无效回答的具体原因。 | 第5.3节，Result II<br><span class="experiment-evidence">The contrast between 0.5 after truncation and 1.0 after restoration is precisely refinement monotonicity in an executable setting.</span> |
| 语义支持消融：保持假设语言任务匹配，将受限解释器替换为可扩展解释器，并观察Thinking能否执行留出预测。 | Thinking从受限支持下的$1/16$提升到可扩展支持下的$16/16$；Direct则从无有效留出预测变为$2/16$有效。 | 该消融隔离了表示接口能否表达和执行所需操作。结果表明额外思考不能稳定执行接口不支持的语义，而扩展支持后Thinking可把这种能力转化为满分；由于接口变化可能同时改变输出有效性与任务难度，不能仅把全部增益归因于推理质量。 | 第5.4节，Result III；表2<br><span class="experiment-evidence">Under a restricted interpreter, direct decoding produces no valid held-out executable prediction and thinking produces 1/16. Under an extensible interpreter, validity rises to 2/16 direct and 16/16 with thinking.</span> |

**定性案例**

- 长上下文关系压力测试显示任务类型之间存在明显差异：在$32{,}768$个竞争项下，Thinking仍能在相对锚点和八跳图任务上保持$2/2$，但无显式索引的序数访问在全部规模下Direct合计为$0/6$。这说明“上下文长度”本身不是充分解释变量；位置标识、关系组合和选择机制是否向模型提供可利用的区分，可能比普通键值检索是否成功更关键。由于每个任务与模式仅约两次重复，该现象更适合作为诊断案例，而非稳定的任务级排名。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：核心贡献是形式化 LLM 推理涌现的接口信息下界，并通过思维、记忆和指针追踪实验检验该理论。; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`a4d1aa5e062ba0c7bc70520456c5b44e7b732eea5b506f45d086ac4e386e0bf2`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
