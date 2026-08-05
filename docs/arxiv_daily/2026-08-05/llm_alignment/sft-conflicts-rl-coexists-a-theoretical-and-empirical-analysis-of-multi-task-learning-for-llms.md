---
title: "[论文解读] SFT Conflicts, RL Coexists: A Theoretical and Empirical Analysis of Multi-Task Learning for LLMs"
description: "[arXiv 2608.03573][对齐 / RLHF] 本文围绕多任务推理训练中的“SFT 冲突、RL 共存”现象，解释监督微调为何在多阶段训练中发生任务间破坏，而强化学习为何能以近似正交的参数更新累积不同任务能力，并据此提出可并行训练后合并更新的 Parallel-RL。"
arxiv_id: "2608.03573"
announcement_date: "2026-08-05"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:42:39.849164+00:00"
source_sha256: "49580f80c4c34d2af98b2c6f3002afda34c03b52d1d45aa9c8bd6ed3f77c4273"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "强化学习"
  - "大语言模型"
  - "监督微调"
  - "多任务学习"
  - "多阶段训练"
  - "梯度干扰"
  - "参数更新正交性"
  - "灾难性遗忘"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.03573</p>

# SFT Conflicts, RL Coexists: A Theoretical and Empirical Analysis of Multi-Task Learning for LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Kejian Zhu, Zhuoran Jin, Shangqing Tu, Hongbang Yuan, Yushi Bai, Kang Liu, Juanzi Li, Jun Zhao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03573v1) · [PDF 下载](https://arxiv.org/pdf/2608.03573v1) · **关键词** 大语言模型, 监督微调, 强化学习, 多任务学习, 多阶段训练, 梯度干扰, 参数更新正交性, 灾难性遗忘<br>
**代码**: [https://github.com/GaryStack/Parallel-RL](https://github.com/GaryStack/Parallel-RL)

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

本文围绕多任务推理训练中的“SFT 冲突、RL 共存”现象，解释监督微调为何在多阶段训练中发生任务间破坏，而强化学习为何能以近似正交的参数更新累积不同任务能力，并据此提出可并行训练后合并更新的 Parallel-RL。

**不用术语来说**：若让同一个大语言模型依次学习多种推理任务，后学任务可能破坏先前能力。作者发现，这种问题在监督微调中尤为严重，但强化学习却能较稳定地保留并累积不同任务的能力。论文要解决的不是简单比较两类方法的最终分数，而是查明这种差异来自什么优化机制，以及能否利用该机制设计更灵活、高效的多任务训练方式。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者通过单任务影响、多阶段训练和参数更新分析，将两种训练范式的差异概括为“SFT Conflicts”与“RL Coexists”：SFT 的跨任务更新存在明显干扰，而 RL 在不同任务上产生更稀疏、相似度更低且近似正交的参数变化。
- 作者从优势函数与同策略优化出发，将 SFT 的任务干扰刻画为受绝对梯度幅值约束的“范数受限”，将 RL 的干扰刻画为受多次采样梯度方差约束的“方差受限”，并据此提出独立并行训练各任务、随后合并更新的 Parallel-RL。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型推理能力的多任务后训练。两种主流范式是监督微调（SFT）与强化学习（RL）：SFT让模型拟合给定的高质量答案或推理轨迹，RL则依据生成结果获得的奖励来调整生成策略。在多任务场景中，训练可以采用“混合数据”方式，即同时使用多个任务的数据，也可以采用“多阶段”方式，即依次在不同任务上训练。已有研究主要比较二者在单任务中的记忆与泛化行为，但尚不足以解释它们在多阶段多任务训练中为何表现不同，尤其是后训练更新是否会破坏先前任务能力，以及不同任务的参数更新能否兼容。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**监督微调（Supervised Fine-Tuning, SFT）**

给定输入及其参考答案或推理轨迹，通过最大化参考输出的条件概率来训练模型。直观上，它要求模型直接模仿数据中指定的解题路径。

</div>
<div class="concept-item" markdown="1">

**强化学习（Reinforcement Learning, RL）**

模型从当前策略生成候选回答，再依据回答获得的奖励更新策略；本文特别关注优势函数与同策略采样对更新方向的影响。直观上，模型不是逐词照抄标准轨迹，而是强化自身探索到的高奖励行为。

</div>
<div class="concept-item" markdown="1">

**多任务梯度干扰**

不同任务产生的梯度或参数更新方向彼此冲突时，优化一个任务可能降低另一个任务的性能；若方向近似正交，则相互影响较小。本文以跨任务更新的大小、稀疏性和相似性分析这种干扰。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是同一个基础大语言模型在多个异质推理任务上的后训练。输入包括基础模型、各任务的训练样本，以及SFT所需的参考输出或RL所需的可验证奖励；训练设置包括混合多任务训练和按任务依次进行的多阶段训练。输出是经过SFT或RL更新后的模型，并通过各任务性能及参数更新之间的关系判断能力是发生冲突还是能够共存。核心比较是在相同多任务目标下，不同阶段产生的参数变化$\Delta W$是否损害未参与当前阶段训练的任务，以及不同任务的更新方向是否近似正交；作者进一步把这一经验现象与SFT的“范数受限”干扰和RL的“方差受限”干扰联系起来。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\Delta W$**

一次任务训练相对于训练前模型产生的参数更新，用于比较不同任务更新的幅度、稀疏性与方向相似度。

</div>
<div class="notation-item" markdown="1">

**$W$**

大语言模型中被后训练过程优化的参数。

</div>

</div>

**直接相关的工作**

- **Chu et al. (2025)**: 该工作在单任务设置下将差异概括为“SFT memorizes, RL generalizes”，认为SFT偏向拟合监督轨迹，而RL更有利于泛化；本文把比较范围推进到多任务与多阶段训练，并分析跨任务参数更新的干扰。
- **Shenfeld et al. (2025), RL’s Razor**: 该工作从隐式KL约束和较小参数偏移解释RL为何减少遗忘，但重点是灾难性遗忘，而非SFT与RL两种训练范式在多任务环境中的梯度干扰差异。本文据作者陈述，进一步结合经验参数分析与理论界限研究这种范式分化。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

面向通用推理能力的大语言模型需要同时掌握多类任务。实际训练既可以混合多个任务的数据，也可以按阶段依次训练任务；后者更便于增加、替换或单独强化某项能力，但前提是新阶段不会覆盖旧能力。论文的初步实验显示，多阶段 SFT 会出现严重性能退化，而多阶段 RL 能较稳定地累积任务收益，因此多任务能力能否共存成为训练方案选择中的关键问题。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **混合数据监督微调（mixed-data SFT）**：把多个任务的带标注示范合并为一个训练集，以最大化参考答案的似然来共同更新模型。任务同时出现可在一定程度上避免依次训练造成的覆盖，但训练过程依赖预先确定的数据配比，新增或调整任务时往往需要重新组织联合数据并再次训练。
- **多阶段强化学习（multi-stage RL）**：模型在每个阶段集中处理一个任务，根据采样回答获得的奖励及相对优势更新策略，再切换到下一任务。论文关注的 RL 具有优势归一化和同策略采样特征，即更新权重取决于当前模型所生成回答之间的相对好坏，而不只是模仿固定答案。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有比较主要集中于单任务训练，尚不足以解释 SFT 与 RL 在多任务、尤其是多阶段设置中的行为为何相反；因此，实践中采用混合 SFT 或分阶段 RL 更多体现经验选择，而缺少统一的参数与梯度层解释。
- 多阶段 SFT 虽能提升当前目标任务，却可能显著损害未训练任务，导致各阶段的局部收益无法在最终模型中累积。仅观察最终性能无法判断这种冲突究竟来自更新幅度、更新方向相似性，还是训练目标本身。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一条从“单任务更新如何影响其他任务”到“跨任务参数变化与梯度干扰如何形成”，再到“这种机制能否支持模块化并行训练”的完整解释链。特别是，尚未明确 SFT 与 RL 的任务间干扰分别受什么量控制，以及 RL 的优势函数和同策略数据来源为何会使不同任务的优化方向趋于近似正交。

</div>
<div markdown="1"><span>核心问题</span>

为什么 SFT 在多阶段多任务训练中会发生性能崩塌，而 RL 能在不同任务之间实现稳定、累积式的能力增长；这种差异能否由任务间梯度干扰的不同上界解释，并进一步转化为可并行、可合并的多任务 RL 范式？

</div>
<div markdown="1"><span>作者直觉</span>

如果两个任务要求大幅修改同一批参数且更新方向相互冲突，那么依次训练时后一次更新就容易覆盖前一次学习。作者据此不只比较任务分数，而是检查各任务引起的参数变化 $\Delta W$。其直觉是：SFT 对固定参考答案持续施加直接模仿信号，更新更大且更容易在共享参数上重叠；RL 则依据当前策略采样结果的相对优势进行更新，大量无区分度或低优势信号会被削弱，使有效更新更稀疏、跨任务内积更小。若不同任务的更新近似正交，就可以分别训练后再合并，而较少彼此抵消。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Parallel-RL建立在一个参数几何观察上：从同一基础模型出发，不同推理任务经强化学习得到的参数更新通常稀疏、幅度小且近似正交，因此任务间内积$\langle\Delta W_i,\Delta W_j\rangle$接近零。方法将任务集合$\mathcal{T}=\{T_1,\ldots,T_N\}$拆开，为每个任务独立运行一次全参数RL，获得任务更新$\Delta W_i$；随后用求和、平均、TIES稀疏合并或基于SVD的秩一合并等函数$\mathcal{M}$组合更新，并将结果加回共享基础参数$W_{base}$。可选的Adapted Parallel-RL还会使用原训练集规模5%的样本，对合并模型进行一次轻量适配。

端到端地看，该方法不是在一个训练进程中反复混合或顺序切换任务，而是把各任务视为可独立生产的“能力模块”：并行训练负责生成模块，参数合并负责组装模块，少量后适配负责修复简单线性组合造成的偏差。其主要价值是解耦计算调度与任务组成——新增、删除或替换任务时，可以重新组合相应的$\Delta W_i$，而不必从头执行完整的多任务联合训练；但这种可组合性依赖RL更新确实近似正交，不能直接推定对SFT更新同样成立。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 任务拆分与共享初始化

为每个任务$T_i$建立独立训练分支，并让所有分支从完全相同的$W_{base}$初始化。任务是否适合并行以及单任务训练技巧也属于该范式的设计范围，但节选仅说明其在附录D中初步讨论。

<div class="method-step__io" markdown="1">

**输入**：推理任务集合$\mathcal{T}=\{T_1,\ldots,T_N\}$、每个任务的训练数据与同一基础模型参数$W_{base}$。<br>
**输出**：$N$个互不共享训练轨迹、但具有共同参数起点的任务分支。

</div>

**直观理解**：这相当于复制同一份底稿，让不同小组分别专攻数学、科学、逻辑或代码；共同起点使后续参数差值具有可比性。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 任务级并行强化学习

每个分支独立执行on-policy RL；主实验采用全参数GRPO，使模型提高本任务高奖励轨迹的采样概率。训练结束后计算任务更新$\Delta W_i=W_i-W_{base}$，其中$W_i$是任务$T_i$的RL模型参数。

<div class="method-step__io" markdown="1">

**输入**：第$i$个任务的数据、奖励信号和初始化参数$W_{base}$。<br>
**输出**：一组任务特定更新$\{\Delta W_1,\ldots,\Delta W_N\}$。

</div>

**直观理解**：不直接保存若干完整模型用于集成，而是提取每个专家相对同一基础模型“改了什么”。由于论文观察到这些RL改动较小且方向近似互不重叠，它们更可能被安全叠加。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 更新预处理与合并

Naive策略直接对更新求和或取平均；TIES先处理稀疏性与更新冲突，SVD策略则对每个$\Delta W_i$分解并仅保留秩一方向。随后由$\mathcal{M}$生成一个联合更新，并加回$W_{base}$得到$W_{final}$。

<div class="method-step__io" markdown="1">

**输入**：所有任务更新$\Delta W_1,\ldots,\Delta W_N$以及选定的合并策略。<br>
**输出**：同时承载多个任务能力的合并模型$W_{final}$。

</div>

**直观理解**：求和或平均像把各专家的修改直接汇总；TIES和秩一SVD则先删减或压缩修改，希望减少少量仍会碰撞的参数变化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 可选的合并后快速适配

Adapted Parallel-RL在合并后进行短程适配，使联合模型重新协调各任务RL模型所提升的高奖励轨迹概率。该步骤不是所有Parallel-RL变体的必需部分，而是用于补偿独立训练和线性合并之间的偏差。

<div class="method-step__io" markdown="1">

**输入**：Naive Parallel-RL求和所得模型与原始训练集规模5%的少量样本。<br>
**输出**：经过轻量校准的多任务模型。

</div>

**直观理解**：独立模块拼接后可能存在接缝，这一步用少量数据做整体调试，而不是重新进行完整的多任务训练。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### Parallel-RL参数合并

$$
W_{final}=W_{base}+\mathcal{M}(\Delta W_{1},\dots,\Delta W_{N})
$$

**符号说明**

- $W_{final}$：完成多任务更新合并后的最终模型参数。
- $W_{base}$：所有单任务RL分支共享的基础模型参数。
- $\mathcal{M}$：参数更新合并函数，可实现求和、平均、TIES或基于SVD秩一成分的合并。
- $\Delta W_i$：任务$T_i$独立RL训练所得模型相对于基础模型的参数变化，即$\Delta W_i=W_i-W_{base}$。
- $N$：并行训练并参与合并的任务数量。

<div class="equation-explanation" markdown="1">

**直观理解**：该式先把每个任务相对共同起点产生的“参数补丁”合成一个联合补丁，再加回基础模型。其合理性不是任意更新都可相加，而是论文发现不同任务的RL更新近似正交，使一个任务的补丁较少抵消或破坏另一个任务的补丁。<br>
**原文位置**：第5.1节 Methodology

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：Parallel-RL没有提出新的单步RL损失，而是改变多任务优化的组织方式：各任务分别使用RL目标优化自己的策略参数，主实验采用GRPO；随后在参数空间合并各任务训练结果。其隐含条件是不同任务更新之间的干扰项$\langle\Delta W_i,\Delta W_j\rangle$足够小，因此联合更新可以近似保留各单任务方向。作者将这种小干扰归因于RL更新的低方差、稀疏性与近似正交性，但所给节选没有提供GRPO、优势归一化或理论方差界的完整公式，因而不应据此补写具体目标函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 独立GRPO任务训练器**

所有任务从共享的$W_{base}$出发，分别进行全参数GRPO训练并输出参数差$\Delta W_i$。论文将其可合并性的机制归因于on-policy RL及优势归一化所形成的低方差更新，以及实证上观察到的稀疏、近似正交参数方向；节选未给出GRPO目标函数或具体超参数。

> 直观理解：该模块把各任务能力先分开学习，避免训练过程中直接争夺同一批梯度；统一起点则让不同任务的“修改补丁”可以对齐后组合。

**2. 参数更新合并器**

合并器实现$\mathcal{M}(\Delta W_1,\ldots,\Delta W_N)$。候选方案包括直接求和、算术平均、TIES稀疏合并，以及对每个更新执行SVD并保留秩一成分后再合并；后两者意在进一步降低更新重叠。

> 直观理解：这是把多个独立学到的能力装回一个模型的核心接口。不同策略在保留更新强度与抑制冲突之间作不同取舍。

**3. 轻量合并后适配器**

Adapted Parallel-RL以Naive Parallel-RL的求和模型为起点，仅使用原训练集规模5%的样本进行快速适配。其目标是利用各单任务RL模型已经提高的高奖励轨迹采样概率，修正直接合并后尚未充分协调的行为。

> 直观理解：它类似组装后的短时联调：成本远低于重新联合训练，却可能恢复甚至增强被简单合并削弱的任务表现。

**训练与推理**

训练阶段首先复制同一DeepSeek-R1-Distill-Qwen基础模型，为数学、科学、逻辑、代码等任务分别启动全参数GRPO进程。每个进程独立采样、获得奖励并更新参数，训练完成后只需提取相对基础模型的$\Delta W_i$；随后选择求和、平均、TIES或秩一SVD策略生成联合更新。若采用Adapted Parallel-RL，则在Naive求和合并后，再用相当于原训练集5%的样本进行快速适配。

推理阶段不需要路由器、多个专家同时前向计算或在线参数合并，而是直接加载已经形成的$W_{final}$。当部署场景需要改变能力组合时，可离线重新选择更新子集并合并；不过，论文证据主要覆盖所测试的推理任务和模型规模，不能保证任意新任务的更新仍然正交，因此实际应用前应检查更新余弦相似度及合并后的跨任务性能。

**复现信息**

主实验以DeepSeek-R1-Distill-Qwen-1.5B和7B为基础模型，采用全参数训练，RL算法为GRPO。Parallel-RL比较四类实现：Naive求和、Naive平均、TIES稀疏合并、逐更新SVD后仅保留秩一方向；Adapted版本从Naive求和结果出发，用原训练集规模5%的样本追加适配。节选说明其他RL算法结果位于附录E.2、更多训练配置位于附录A，但没有给出学习率、批量大小、采样数、奖励定义、训练步数或硬件信息，复现时必须回查这些位置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 数学任务：SFT 使用 OpenR1-Math-220k 的一个未注明规模子集，RL 使用 DeepScaleR-Preview-Dataset 的一个未注明规模子集；评测采用 MATH500 与 AIME2025。AIME2025 题量较小，因此报告 16 次测试的平均准确率 avg@16。训练、验证划分及具体样本数原文未明确报告。
- 科学任务：SFT 使用 AM-Thinking-v1-Distilled 的未注明规模子集，RL 使用该数据集科学部分的未注明规模子集；评测采用 GPQA-Diamond，以及 MMLU 中与科学推理直接相关的六个学科：高中物理、高中化学、大学化学、大学生物、天文学和职业医学。具体训练、验证划分及样本数原文未明确报告。
- 代码与逻辑任务：代码 SFT 使用 AM-DeepSeek-Distilled-40M 的一个子集，RL 使用 DeepCoder-Preview-Dataset 的一个子集，并以 LiveCodeBench 评测；逻辑训练与评测均基于 knights-and-knaves。由于原始逻辑数据没有思维链，作者通过 DeepSeek-R1 API 蒸馏 LongCoT，并使用 Logic-RL 的规则验证器检查答案。各子集规模及训练—测试去重细节原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**参数更新的 $L_2$ 范数**

将某任务训练前后的参数差写成更新向量 $\Delta W_i$，其 $L_2$ 范数衡量模型为该任务移动了多远。该指标用于比较 SFT 与 RL 对参数的总体扰动规模，而不是直接衡量任务准确率。 （在保持任务性能的前提下通常越低越有利，因为较小更新较不容易破坏其他任务；但单独的低范数不能证明模型性能更好。）

</div>
<div class="metric-item" markdown="1">

**参数更新稀疏率**

原文通过统计更新幅度超过 $10^{-5}$ 的参数占比，衡量训练改动覆盖了多少参数。占比越低表示更新越集中、越稀疏。 （若目标是减少跨任务相互影响，则超过阈值的参数占比越低通常越有利；该判断依赖阈值选择，也不等同于准确率提升。）

</div>
<div class="metric-item" markdown="1">

**跨任务参数更新的两两余弦相似度**

比较任务 $T_i$ 与 $T_j$ 的更新向量 $\Delta W_i$、$\Delta W_j$ 的方向关系：接近 $1$ 表示同向，接近 $-1$ 表示反向，接近 $0$ 表示近似正交。它直接检验不同任务是否共享或冲突于相同优化方向。 （对于论文关注的任务解耦，绝对值越接近 $0$ 越好，因为这意味着一个任务的更新较少投影到另一个任务的更新方向；但近似正交本身不保证每项任务都获得高性能。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 比较 RL 与 SFT 在不同任务训练后产生的参数更新总体幅度。

<div class="result-value" markdown="1">

RL 更新向量的平均 $L_2$ 范数约为 $3\times10^{-2}$，SFT 则达到 $7.4$，相差两个数量级以上。

</div>

作者据此认为 RL 只需对模型作很小调整，因而较不容易覆盖其他任务已经形成的能力。分析上，这一结果证明的是参数移动规模不同；由于节选没有同时给出对应任务得分、置信区间及学习率匹配对照，它不能单独证明较小更新必然带来更高性能，也不能完全排除优化配置差异的影响。

<div class="result-source" markdown="1">

来源：第 3 节“Parameter-Level Empirical Analysis”，Observation 1；Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The heatmaps reveal a stark difference between ΔW_RL and ΔW_SFT in scale: the average $L_2$ norm of ΔW is approximately 3 × 10−2 for RL, whereas it reaches 7.4 for SFT, showing a difference of over two orders of magnitude.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 以更新幅度超过 $10^{-5}$ 的参数占比比较 RL 与 SFT 的参数更新稀疏性。

<div class="result-value" markdown="1">

RL 中约 $20\%$ 的参数更新幅度超过 $10^{-5}$，SFT 中该比例为 $93\%$。

</div>

这说明在给定阈值下，RL 的显著更新集中于较少参数，而 SFT 几乎改动整个参数空间。作者将其解释为 RL 对其他任务更少扰动的原因之一；但该统计依赖 $10^{-5}$ 这一阈值，节选未给出其他阈值下的稳健性结果，也未证明被修改的少量参数在功能上彼此独立。

<div class="result-source" markdown="1">

来源：第 3 节“Parameter-Level Empirical Analysis”，Observation 1；Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Furthermore, RL updates exhibit high sparsity; only about 20% of parameters in RL have magnitudes exceeding 10−5, compared to 93% in SFT.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 比较数学、科学、代码和逻辑任务之间参数更新向量的两两余弦相似度。

<div class="result-value" markdown="1">

不同 RL 任务的更新余弦相似度平均约为 $10^{-5}$，近似为零；SFT 的相似度量级则从 $10^{-1}$ 到 $1.0$，且数学与代码等任务之间还出现反向更新。

</div>

作者据此把 RL 的任务更新视为实践上的近似正交：训练某一任务时，更新在其他任务方向上的投影很小，因此多任务更可能共存。SFT 更新方向高度重叠，反向分量则可能造成遗忘。需要注意，余弦相似度仅描述局部参数位移的几何关系；它不是因果干预测试，也不能排除模型重参数化、LoRA 子空间或更新尺度对几何统计的影响。

<div class="result-source" markdown="1">

来源：第 3 节“Parameter-Level Empirical Analysis”，Observation 2；Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We observe that the pairwise cosine similarity of ΔW between different RL tasks is negligible, averaging around 10−5. In contrast, SFT exhibits high similarity across tasks (on the order of 10−1 to 1.0), with some updates even pointing in opposite directions (e.g., Math vs. Code).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 提供的章节主要报告参数更新几何，没有给出六个评测基准上的完整性能表、方差或显著性检验，因此无法从该节选核验“RL 稳定共存”是否在所有模型规模和任务上都转化为显著准确率收益。
- SFT 与 RL 使用不同训练数据、学习率和优化过程，且部分分析采用 LoRA；更新范数、稀疏度和余弦相似度可能同时受数据内容、参数化方式与超参数影响。节选没有提供等数据、等步数、等性能或多阈值消融，因而当前证据更支持相关机制解释，而非完全识别 RL 算法本身的因果效应。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 监督微调（SFT）：模型直接学习教师生成的思维链轨迹，是检验多任务监督学习是否产生较大、重叠乃至冲突参数更新的核心对照。
- 强化学习（RL/GRPO）：模型针对任务奖励进行组相对策略优化，是论文所主张的低干扰训练方式；与 SFT 在相同任务族和相同基础模型上的参数更新几何进行比较。

**实验想回答的问题**

- 在数学、科学、代码和逻辑四类推理任务上，SFT 与 RL 产生的参数更新在幅度、稀疏性和跨任务方向相似度上有何差异，这些差异能否解释多阶段训练中的任务干扰？
- RL 的跨任务参数更新是否足够小且近似正交，从而为不同任务可稳定共存、可解耦训练这一经验现象提供参数层证据？

**实验实现**

基础模型为 DeepSeek-R1-Distill-Qwen-1.5B 和 7B，实验运行于 8 张 NVIDIA A100 80GB GPU；部分参数分析使用 LoRA，秩为 $r=64$、缩放系数为 $\alpha=32$。多阶段训练顺序固定为数学、科学、代码、逻辑。SFT 通过 LLaMA-Factory 学习教师思维链，学习率为 $1\times10^{-5}$，截断长度为 8K token；RL 通过 VeRL 实现 GRPO，学习率为 $3\times10^{-6}$，每个提示采样 $G=16$ 条 rollout，温度为 $0.6$、$\mathrm{top\text{-}p}=0.95$，最大输出长度为 8K token，并在该分析中关闭 KL 散度惩罚。多数任务使用 lighteval 评测，逻辑任务使用 Logic-RL 专用评测套件；生成评测同样采用温度 $0.6$ 和 $\mathrm{top\text{-}p}=0.95$。节选未提供随机种子、重复训练次数或误差区间。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- Figure 2 的任务对热图中，数学与代码的 SFT 更新出现相反方向，而 RL 的各任务更新整体接近正交。该案例直观展示了 SFT 可能在学习代码时抵消数学方向的更新；不过原文节选未提供该任务对的精确单元格数值或对应性能下降幅度，因此只能作为几何现象示例，不能单独量化灾难性遗忘。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Analyzes and improves reinforcement-learning post-training for multi-task LLM reasoning through gradient-interference theory and Parallel-RL.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`49580f80c4c34d2af98b2c6f3002afda34c03b52d1d45aa9c8bd6ed3f77c4273`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
