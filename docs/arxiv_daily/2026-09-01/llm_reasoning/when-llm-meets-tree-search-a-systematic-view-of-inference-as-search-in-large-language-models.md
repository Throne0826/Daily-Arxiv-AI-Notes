---
title: "[论文解读] When LLM Meets Tree Search: A Systematic View of Inference as Search in Large Language Models"
description: "[arXiv 2608.30395][LLM Reasoning] 本文是一篇知识系统化综述，旨在用统一的“推理即搜索”视角整理大语言模型中的树搜索推理方法，并从搜索机制、评价信号与转移动态三个组件解释测试时扩展和搜索驱动自改进之间的联系。"
arxiv_id: "2608.30395"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:30:49.239778+00:00"
source_sha256: "dbc239cd8b4433e7d90bc958f3bf4f805c38f454b485585cad448a55211270a6"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "测试时扩展"
  - "推理即搜索"
  - "树搜索"
  - "蒙特卡洛树搜索"
  - "思维链"
  - "奖励与价值估计"
  - "自我改进"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.30395</p>

# When LLM Meets Tree Search: A Systematic View of Inference as Search in Large Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Jiaqi Wei, Xiang Zhang, Yuejin Yang, Wenxuan Huang, Juntai Cao, Sheng Xu, Xiang Zhuang, Zhangyang Gao, Muhammad Abdul-Mageed, Laks VS Lakshmanan, Chenyu You, Wanli Ouyang, Siqi Sun</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Zhejiang University；Affiliation: Fudan University；Affiliation: Shanghai AI Laboratory；Affiliation: University of British Columbia；Affiliation: Stony Brook University；Affiliation: The Chinese University of Hong Kong * Equal Contribution Correspondence；Affiliation: The Chinese University of Hong Kong</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30395v1) · [PDF 下载](https://arxiv.org/pdf/2608.30395v1) · **关键词** 大语言模型, 测试时扩展, 推理即搜索, 树搜索, 蒙特卡洛树搜索, 思维链, 奖励与价值估计, 自我改进<br>


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

本文是一篇知识系统化综述，旨在用统一的“推理即搜索”视角整理大语言模型中的树搜索推理方法，并从搜索机制、评价信号与转移动态三个组件解释测试时扩展和搜索驱动自改进之间的联系。

**不用术语来说**：固定一个大语言模型后，增加它在回答时的思考计算量，往往比继续扩大模型更可行；但普通思维链通常沿一条路径不断生成，一旦前面走错便难以回头，也无法充分比较多个候选思路。树搜索允许模型保留若干中间方案、依据反馈选择值得继续探索的分支，但现有研究使用的搜索算法、奖励信号和算力口径各不相同，使研究者难以判断性能提升究竟来自哪里、付出了多少计算成本，以及不同方法能否公平比较。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出统一形式化与组件化分类，把搜索式推理分解为搜索机制、奖励或价值估计、转移动态，并据此连接测试时优化与将优质搜索轨迹蒸馏为参数知识的自改进过程。
- 综合树搜索方法的经验认识与开放问题，并倡导轻量级、标准化的计算报告抽象，使不同研究中的推理算力—准确率权衡更加明确和可比较。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大语言模型的预训练规模扩张正面临收益递减，因此研究重点逐渐转向测试时扩展（Test-Time Scaling, TTS）：在模型参数固定的前提下，为不同问题分配额外且可自适应的推理计算。本文将这种推理理解为在“部分推理状态”构成的组合空间中搜索，而不只是逐词生成答案。思维链虽能显式呈现中间步骤，但常见的单轨迹解码难以在早期步骤出错后回退，也缺少对替代路径的系统探索；树搜索则维护多个候选状态，并依据中间反馈重新分配计算。本文是一篇知识系统化综述，不提出新算法或基准，而是用搜索机制、奖励或价值估计、转移动态三个组件统一整理相关方法，并讨论树搜索在测试时优化与搜索结果蒸馏训练中的双重作用。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试时扩展（Test-Time Scaling, TTS）**

在不增大或重新训练模型的情况下，通过增加推理阶段的采样、验证、搜索或反思计算来提高解题表现。其核心问题是如何把有限计算预算分配给更有希望的候选推理路径。

</div>
<div class="concept-item" markdown="1">

**思维链（Chain-of-Thought, CoT）**

让模型在最终答案之前生成可见的中间推理步骤，以便完成多步问题。若只沿一条路径继续生成，前面的错误可能持续传播，且系统通常无法比较其他可能的推理方向。

</div>
<div class="concept-item" markdown="1">

**树搜索与蒙特卡洛树搜索（MCTS）**

树搜索把部分推理过程视为节点，把下一步推理视为分支，从而保留并比较多条候选路径；MCTS进一步利用采样和反馈在探索新分支与利用高价值分支之间进行权衡。对大语言模型而言，节点可对应部分解答，评价信号则用于决定后续计算应投向哪里。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文研究的对象是固定大语言模型上的搜索增强推理。输入是一个待解决的任务实例、固定模型先验以及可用的测试时计算预算；系统在由部分推理状态组成的组合空间中，通过生成后继状态、评价中间候选并控制搜索方向来寻找高质量完整解答，输出是最终答案或被选中的完整推理轨迹。综述还考虑搜索到的优质轨迹如何被蒸馏为训练数据或用于学习奖励模型，使暂时性的测试时搜索转化为模型参数中的持久能力。其分析假设任务具有可定义的目标或反馈，但所给章节未规定统一的状态、动作、奖励公式或具体预算单位。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Wei et al. (2022), Chain-of-Thought prompting**: 该工作表明显式生成中间推理步骤能够提升任务表现，是本文讨论搜索式推理的直接基础；本文强调常见思维链实现多采用单轨迹解码，因而难以从早期错误中恢复或充分探索替代路径。
- **Yao et al. (2023), tree-search-based reasoning**: 该工作代表维护部分解答前沿并根据中间反馈重新分配推理计算的搜索增强方法，属于本文所系统整理的现代测试时推理算法核心。所给章节未提供其具体算法名称、公式或实验细节。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

随着仅靠增加预训练参数与数据所获得的收益递减，研究需要在固定模型先验下更有效地使用推理时算力。复杂任务包含组合式、长程的推理空间；系统不仅要产生中间步骤，还要能在发现低质量步骤后回退、比较备选路线并把计算资源集中到更有希望的分支。同时，搜索本身会带来显著开销，强模型还可能在简单问题上过度思考，因此实际系统必须回答何时搜索、搜索多深以及如何动态分配预算。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **思维链与单轨迹解码**：模型把中间推理步骤显式写出，并按照贪心选择或采样结果沿一条序列持续生成，直至得到最终答案。它让推理过程可见，也可能提高任务表现，但生成期间通常不维护可供系统比较和回访的候选分支。
- **规划、启发式树搜索与蒙特卡洛树搜索**：系统把部分推理视为树节点，扩展多个后继状态，并利用中间奖励、价值估计或策略先验决定继续探索哪些节点。其中蒙特卡洛树搜索通过反复选择、扩展、采样和回传，在尝试未知分支与利用当前优质分支之间进行权衡；搜索得到的高质量轨迹还可转化为训练数据或奖励模型，用于模型自改进。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单轨迹思维链缺少显式的分支维护与回溯机制，因此早期错误可能沿后续步骤持续传播，系统也难以探索和比较彼此不同的解题路线。
- 树搜索文献分散在不同搜索策略、奖励或价值估计方法及评价协议中，且搜索会产生较大的计算开销；更关键的是，低质量奖励可能把搜索引向错误方向，甚至出现增加采样反而降低准确率的“逆推理扩展”。这些差异使方法的通用设计规律和算力—效果关系难以辨认。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作已经证明搜索能够改善推理，却缺少一套跨方法的共同概念框架：它既要明确节点如何扩展、候选状态如何评价、搜索如何受控，也要覆盖测试时搜索和搜索轨迹蒸馏两种用途，并提供可比较的计算成本表达。该缺口不是新的搜索算法或基准不足，而是既有结果缺乏统一组织与报告标准。

</div>
<div markdown="1"><span>核心问题</span>

如何将大语言模型的树搜索式推理统一分解为可比较的算法组件，并据此说明不同搜索范式、评价信号和控制动态如何共同决定测试时推理与搜索驱动自改进，同时使各研究的计算—准确率权衡能够被一致解释？

</div>
<div markdown="1"><span>作者直觉</span>

把生成答案改看成在“部分推理状态”空间中寻找优质路径后，看似不同的方法便可用相同问题来分析：当前保留哪些节点、下一步如何生成、依据什么信号判断好坏，以及预算投向哪里。就像解迷宫时同时标记多个岔路并根据沿途线索调整探索顺序，这一视角既解释了树搜索为何比一路走到底更容易纠错，也能定位失败来源究竟是搜索控制、状态评价还是计算分配，从而支持更有意义的横向比较。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文是系统综述，而非提出一套可直接训练的新算法。其方法性贡献是把基于树搜索的 LLM 推理统一为确定性规划问题：给定问题 $Q$ 与条件提示 $c$，固定参数的策略 LLM $\pi$ 逐步生成动作 $a_i$；动作是一个增量推理步骤，并唯一确定下一文本状态 $s_{i+1}$。搜索过程在问题对应的树 $T_Q$ 中保留多个候选分支，通过价值或奖励信号选择、扩展并回传节点质量，最终寻找高质量推理轨迹 $p'=[s_1,\ldots,s_n]$ 或最佳完整答案。这里的“环境”只是不断增长或被改写的文本轨迹，因此该表述不同于具有随机环境转移的标准 MDP。

统一设计空间主要考察三个相互制约的选择：节点表示决定搜索对象的粒度，评价函数决定何种推理值得投入计算，MCTS 控制规则决定如何在探索新分支与利用已知优质分支之间分配预算。直观地说，普通思维链像沿一条路一直走；树搜索则同时保留若干岔路，并借助过程评分、答案验证或自我评价反复决定“接下来扩展哪条路”。细粒度节点可更早纠错但树更大，整解节点成本较低但反馈较粗，因而不存在脱离任务、验证器质量和计算预算的单一最佳配置。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 问题建模与搜索树初始化

将推理定义为确定性文本规划：状态 $s_i$ 表示当前推理内容，动作 $a_i$ 表示下一增量步骤，执行动作后唯一得到 $s_{i+1}$。据此建立问题特定的搜索树 $T_Q$，而不是立即提交一条单轨迹答案。

<div class="method-step__io" markdown="1">

**输入**：问题 $Q$、条件提示 $c$、固定参数的策略 LLM $\pi$，以及可用的价值模型、奖励模型或外部验证器。<br>
**输出**：包含根状态、动作空间 $\mathcal{A}$ 和待扩展候选的初始搜索结构。

</div>

**直观理解**：模型先把“直接回答”改造成“在许多可能推理路线中找答案”。同一基础模型不变，只在当前问题上额外花计算探索分支。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 确定节点表示与搜索粒度

从三种主要表示中选择节点：完整的部分轨迹 $p_i=[s_1,\ldots,s_i]$、局部状态—动作对 $(s_i,a_i)$，或完整终止解 $s^{\mathrm{terminal}}$。前两种把搜索看作寻找最佳路径，终止状态节点则把边定义为批评、重写或精炼操作，将任务转化为寻找最佳候选节点。

<div class="method-step__io" markdown="1">

**输入**：搜索树 $T_Q$、任务所需的反馈精度与可用推理预算。<br>
**输出**：具有明确节点语义和边操作的候选空间。

</div>

**直观理解**：节点可以是一整段解题过程、一个局部步骤，或一份完整答案。切得越细越容易定位错误，但需要维护和评价的分支也越多。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成并评价候选节点

策略生成下一步骤或重写后的候选，再以过程奖励评价中间轨迹、以结果奖励评价终止答案，或将价值估计、过程奖励和结果奖励组合成统一质量分数。评价器既可由独立训练的模型承担，也可复用策略 LLM 进行自我评价。

<div class="method-step__io" markdown="1">

**输入**：当前选中节点、策略 $\pi$、价值模型 $V_\theta$、奖励模型 $R_\theta$，或投票、代码执行、LLM 裁判等外部信号。<br>
**输出**：带有即时奖励 $r_i$、轨迹价值 $v_i$ 或综合质量 $Q_i$ 的新增节点。

</div>

**直观理解**：这一阶段相当于给每条候选路线设置路标：过程评分判断中间步骤是否健康，结果评分检查最终答案是否正确。多评价器可降低单一信号失误的影响，但会增加成本和设计复杂度。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### MCTS 控制、回传与答案输出

循环执行选择、扩展和回传：选择阶段用 UCB 类准则及可选的策略先验平衡探索与利用；扩展阶段生成新步骤或执行批评—重写；回传阶段以平均、最大值或平滑规则更新祖先节点统计。达到预算或终止条件后，从访问和价值统计支持的终止节点中确定输出。

<div class="method-step__io" markdown="1">

**输入**：节点访问统计、策略先验、节点质量信号及剩余测试时计算预算。<br>
**输出**：搜索得到的最佳推理轨迹 $p'$ 或最佳完整候选答案，以及对应的树统计。

</div>

**直观理解**：算法反复在“继续深挖看起来最好的路线”和“尝试尚未充分检查的路线”之间切换。子节点得到的新证据会沿树向上传递，从而影响下一轮计算应投向哪里。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 最优推理轨迹表示

$$
p^{\prime}=[s_{1},\ldots,s_{n}]
$$

**符号说明**

- $p^{\prime}$：针对问题 $Q$ 通过搜索获得的目标推理轨迹
- $s_i$：第 $i$ 步的推理状态，即截至该步形成的文本推理内容
- $n$：目标轨迹包含的推理状态数量

<div class="equation-explanation" markdown="1">

**直观理解**：该式规定搜索的输出不是孤立的下一个词，而是一系列相互衔接的推理状态。对于轨迹型和状态—动作型方法，优化对象是通向正确答案的整条路径；终止状态型方法则相应转向直接寻找最佳完整节点。<br>
**原文位置**：第 3.1 节 Unified Problem Formulation

</div>

</div>

<div class="equation-block" markdown="1">

#### 多评论者综合节点质量

$$
Q_{i}\leftarrow\beta_{1}V_{i}+\beta_{2}R^{\mathrm{PRM}}_{i}+\beta_{3}R^{\mathrm{ORM}}_{i}
$$

**符号说明**

- $Q_i$：节点 $i$ 用于搜索控制的综合质量分数
- $V_i$：节点或轨迹继续通向高质量解的价值估计
- $R_i^{\mathrm{PRM}}$：过程奖励模型对节点 $i$ 的中间推理质量评分
- $R_i^{\mathrm{ORM}}$：结果奖励模型对节点 $i$ 所关联最终结果的评分
- $\beta_1,\beta_2,\beta_3$：控制三类评价信号相对贡献的权重

<div class="equation-explanation" markdown="1">

**直观理解**：该式以 ALPHALLM 为例说明多评价器的共同原则：同时考虑未来潜力、当前步骤质量和最终正确性。这样可降低单一稀疏或含噪信号对搜索的支配，但权重选择会直接改变搜索偏好。<br>
**原文位置**：第 3.3.3 节 Multi-Critic and Composite Reward Functions

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：本文是综述，其统一框架本身没有待优化的单一训练损失。测试时搜索奖励是面向当前问题的临时局部目标，只改变本次搜索的节点选择与计算分配，不通过梯度更新策略参数 $\theta$；这与强化学习将多次交互中的奖励吸收到策略 $\pi_\theta$、形成可跨任务复用的长期行为变化不同。个别被综述方法会预先训练 $V_\theta$、$R_\theta$ 或利用 MCTS 轨迹生成过程监督数据，但原文节选没有给出可统一复现的训练目标，不能将这些方法特有目标视为本文目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 节点表示与粒度模块**

轨迹节点以 $p_i=[s_1,\ldots,s_i]$ 保存完整上下文，可由 $V_\theta(p_i)$ 评价长期潜力；状态—动作节点 $(s_i,a_i)$ 聚焦单步质量；终止状态节点 $s^{\mathrm{terminal}}$ 把完整答案作为原子对象，并通过精炼或重写连接候选。粒度同时影响分支因子、评价输入、纠错位置和总体搜索成本。

> 直观理解：该模块决定树上的一个“格子”到底装什么。保留更多上下文有利于整体判断，局部节点便于指出具体错误，而完整答案节点适合直接比较或迭代改写多个成品。

**2. 评价信号模块**

过程奖励模型在非终止轨迹上提供细粒度反馈，结果奖励模型主要评价 $s^{\mathrm{terminal}}$；结果信号可来自多数投票、执行验证或 LLM 裁判。评价架构可使用独立的 $V_\theta$、$R_\theta$，也可由策略 $\pi$ 自评；多评论者设计再以加权方式融合长期价值、步骤质量和最终正确性。

> 直观理解：搜索是否有效，很大程度上取决于“尺子”是否可靠。只检查最终答案反馈较晚但通常目标直接；逐步检查能及早剪除坏路线，却可能被不准确的中间评分误导。

**3. MCTS 搜索控制模块**

标准控制循环包括选择、扩展和回传。面向 LLM 的改造包括在 UCB 类选择分数中加入策略先验、在扩展阶段加入语言化批评和重写算子，以及以最佳子节点和当前值的平滑组合代替简单回传；这些设计用于适应生成空间巨大、评价稀疏或含噪的情况。

> 直观理解：评价模块说明“哪些节点好”，控制模块则决定“有限预算下一步花在哪里”。它避免只跟随当前最高分节点，也避免无目的地平均尝试所有分支。

**训练与推理**

推理阶段，固定策略 LLM 的参数，输入 $Q$ 与 $c$ 后初始化 $T_Q$；根据任务选择轨迹、状态—动作或终止答案作为节点，并确定过程奖励、结果奖励或复合评价器。随后在预算内循环运行 MCTS：依据累计访问次数、质量统计及可选策略先验选择节点；由 LLM 生成下一推理步骤，或对完整答案执行批评、精炼和重写；调用 $V_\theta$、$R_\theta$、执行环境、投票机制或 LLM 裁判评价新增节点；最后将评价结果回传至祖先节点。终止后输出搜索统计支持的高质量轨迹或完整答案。

训练阶段没有统一流程，因为本文不提出新模型。被综述系统可能离线训练专用价值模型、过程奖励模型、结果奖励模型或偏好模型，也可能完全复用策略 LLM 自评；另一些混合方法把测试时 MCTS 产生的细粒度轨迹转为训练监督，使一次性搜索经验进一步影响长期模型参数。解释实验或复现具体方法时，必须区分“搜索时临时使用奖励”和“训练时用奖励更新参数”，否则会把实例级规划收益误归因于模型能力已经被永久改变。

**复现信息**

公平实现首先要明确节点的文本粒度，因为单步、短片段、多句轨迹和完整答案会产生不同的树深度、分支因子与评价调用次数。其次应报告评价信号的来源及作用位置，包括是否使用 $V_\theta$、过程奖励、结果奖励、执行验证、投票、独立 LLM 裁判或策略自评，以及这些信号只评价终止节点还是也评价中间节点。还需说明选择阶段是否加入策略先验、扩展阶段是否含批评或重写、回传采用平均、最大值还是平滑更新。

原文节选没有提供统一的模型规模、采样温度、分支数、搜索深度、停止条件、硬件或精确计算预算，因此这些内容均不能从该综述框架中推定。复现具体被综述方法时，应回到对应原论文；跨方法解释时则至少统一报告 LLM 生成调用、评价器调用、展开节点数或等价测试时计算量，否则准确率差异可能只是来自搜索预算不同，而非节点设计或控制策略本身更有效。

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

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**正确率**

衡量最终答案或程序通过数值检查器、单元测试等验证的比例。本文将其作为讨论树搜索相对解码基线收益的主要效果指标，但所给节选未规定跨任务统一的计算公式。 （越高越好，因为它表示更多实例得到可验证的正确输出。）

</div>
<div class="metric-item" markdown="1">

**推理延迟**

衡量搜索、模型生成和候选评估造成的测试时运行时间；它用于判断正确率提升是否以不可接受的响应成本为代价。 （在正确率相当时越低越好；若正确率不同，则应结合准确率—延迟权衡判断，不能单独比较。）

</div>
<div class="metric-item" markdown="1">

**推理计算预算**

测试时用于生成、树扩展、回报评估与验证的总计算资源。节选特别讨论其中分配给评估过程的比例，但没有给出统一的硬件无关计量公式。 （不存在无条件的越高或越低越好；应在固定预算下获得更高正确率，或在固定正确率下消耗更少计算。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 具有可靠终局验证器的数学推理与程序综合，对比树搜索和贪心解码。

<div class="result-value" markdown="1">

作者综合既有研究称，MCTS 方法相对贪心解码通常报告约 $10\%$–$40\%$ 的提升；同一段同时指出，在缺少可验证正确性的开放式生成中，搜索相对强解码基线通常只有边际改善。

</div>

决定搜索是否有效的关键并非“树越大越好”，而是候选路径能否被可靠地区分。数值检查器或单元测试可为完整答案提供稳定反馈，使搜索能够淘汰错误分支；开放式任务中的主观评分噪声则可能被搜索反复放大。这里的 $10\%$–$40\%$ 是综述对不同研究的概括，节选没有说明它是绝对百分点还是相对增幅，也没有在统一模型、预算和数据集上验证，因此不能据此断言任意任务都能获得相同收益。

<div class="result-source" markdown="1">

来源：第3.7节，Decision Criteria: When to Use Search

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In such domains, MCTS-based methods routinely report substantial gains (e.g., 10–40%) over greedy decoding.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 奖励模型不可靠、任务较短或较容易，以及验证成本占据大部分预算的条件。

<div class="result-value" markdown="1">

作者总结了三类搜索回报不佳的情形：奖励与最终正确性相关性弱时可能出现虚假信号过度利用和逆向扩展；简单或短程实例在大预算下可能“过度思考”；验证过贵时可探索的深度受限，准确率—延迟权衡恶化。

</div>

树搜索会有针对性地寻找高评分路径，因此评分器的系统性偏差比随机采样时更危险：搜索可能找到最能欺骗评分器、而非真正正确的答案。对简单题继续扩展还会引入新的出错机会；若每个节点都需要昂贵验证，则名义上的大预算未必转化为更广或更深的探索。这是跨研究归纳的适用性结论，不是同一实验中对三个因素分别控制后的因果证明。

<div class="result-source" markdown="1">

来源：第3.7节，When Search Is Unwarranted

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Empirical evidence suggests several recurring regimes where search offers poor returns or degrades performance.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 搜索适用时，在候选生成与节点评估之间分配测试时计算预算。

<div class="result-value" markdown="1">

作者称，跨研究把约 $20\%$–$30\%$ 的推理计算用于评估，通常能取得稳健收益；高保真的过程奖励模型可降低奖励噪声，但其成本会压缩搜索深度，而轻量自评可以覆盖更多分支。

</div>

评估太少会导致搜索依据噪声选择分支，评估太多又会减少真正用于生成和扩展候选的计算量，因此合理配置应处于两者之间。$20\%$–$30\%$ 是经验性预算区间，不是经过本文统一消融得到的普适最优值；不同模型、验证器成本和任务长度可能需要不同配置。

<div class="result-source" markdown="1">

来源：第3.7节，Configuration Trade-offs When Search Applies

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across studies, allocating roughly 20–30% of inference compute to evaluation yields robust gains.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给章节主要综合不同论文的经验，没有提供统一数据集、模型规模、搜索预算、硬件和验证成本下的受控比较；因此 $10\%$–$40\%$ 的收益及 $20\%$–$30\%$ 的评估预算建议可能混合了任务难度、基座模型和计算口径等因素。
- 节选中的 Evaluation Framework 内容被截断，无法确认作者最终提出的标准化计算报告指标、计算公式及其完整验证结果；同时，表2报告的是典型超参数范围而非对应性能，不能据此推断 rollout、深度或温度变化与正确率之间的因果关系。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 贪心解码（greedy decoding）：每一步直接选择当前概率最高的输出，不探索替代推理分支；它是判断树搜索额外推理计算是否真正改善正确率的基本参照。
- Tree-of-Thoughts 等启发式搜索：依赖大语言模型生成的中间启发分数选择分支，适合与维护访问次数和回报统计量的蒙特卡洛树搜索比较，尤其用于考察低延迟与稀疏奖励条件下的差异。
- 重排序（re-ranking）：先生成有限个候选答案，再用评分器选出一个答案；它代表不进行深层树扩展的轻量替代方案。
- 小规模自一致性（small-$n$ self-consistency）：采样少量独立推理轨迹并通过答案聚合决策，用于判断复杂树搜索相对简单增加采样数量是否值得。

**实验想回答的问题**

- 综合既有研究，树搜索在什么任务条件下能比单轨迹解码带来稳定收益，哪些条件会使搜索收益很小甚至导致性能下降？
- 当任务适合搜索时，验证信号、备份策略与推理计算预算应如何配置，才能取得合理的准确率—成本权衡？

**实验实现**

该文是综述而非在统一数据集上复现实验的方法论文。节选汇总数学与逻辑、代码生成、检索增强生成和自主智能体等任务中的已有结果，并按验证可靠性、树结构、评价信号和备份方式解释差异。表2给出的典型配置包括：数学任务约 $16$–$128$ 次 rollout、深度 $8$–$20$；代码任务约 $16$–$64$ 次 rollout、每步 $5$–$50$ 个样本及温度 $0.6$–$0.8$；检索任务的检索数量 $k=3$–$10$、深度 $3$–$5$；智能体任务约 $20$–$50$ 次 rollout。作者还建议二元验证任务采用最大值备份，高方差数学任务采用平均值备份。由于所给节选没有统一模型、数据划分、硬件、随机种子或复现实验协议，这些范围只能视为跨论文经验汇总，不能被当作受控基准测试。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 表2以任务类型给出配置案例：代码生成使用终局执行结果作为二元 ORM，并采用最大值备份；数学与逻辑任务依赖轨迹级 PRM/PPRM，并采用平均值或求和备份。该对照说明配置应服从反馈语义：代码中“一条路径通过测试”具有明确意义，而数学过程评分更连续且有噪声，需要聚合多个回报。它是实践指南而非统一数据集上的定量案例，不能证明所列配置在所有模型上最优。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文系统综述通过树搜索和测试时计算扩展来提升大语言模型推理能力的方法。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`dbc239cd8b4433e7d90bc958f3bf4f805c38f454b485585cad448a55211270a6`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
