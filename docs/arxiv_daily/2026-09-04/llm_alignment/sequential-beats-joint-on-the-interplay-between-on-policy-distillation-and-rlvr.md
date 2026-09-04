---
title: "[论文解读] Sequential Beats Joint: On the Interplay between On-Policy Distillation and RLVR"
description: "[arXiv 2609.04108][对齐 / RLHF] 本文研究如何组合在策略蒸馏与可验证奖励强化学习，指出将二者拆成“先蒸馏、后强化学习”的连续阶段，比在同一步中混合两种训练信号更能发挥其互补作用。"
arxiv_id: "2609.04108"
announcement_date: "2026-09-04"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:36:19.373001+00:00"
source_sha256: "525c61774af5277fb69e0bbb66fbe30b50161027303d6b5b2b98f249769c503f"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "强化学习与可验证奖励（RLVR）"
  - "在策略蒸馏（OPD）"
  - "大语言模型后训练"
  - "推理能力学习"
  - "策略梯度"
  - "知识蒸馏"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2609.04108</p>

# Sequential Beats Joint: On the Interplay between On-Policy Distillation and RLVR

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Boyan Li, Bingsen Chen, Chenghao Yang, Ping Nie, Chen Zhao, Xi Ye</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: New York University；Affiliation: University of Chicago；Affiliation: University of Waterloo；Affiliation: University of Alberta；Affiliation: Alberta Machine Intelligence Institute (Amii)</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.04108v1) · [PDF 下载](https://arxiv.org/pdf/2609.04108v1) · **关键词** 强化学习与可验证奖励（RLVR）, 在策略蒸馏（OPD）, 大语言模型后训练, 推理能力学习, 策略梯度, 知识蒸馏<br>
**代码**: [https://github.com/StringNLPLAB/opd-rlvr](https://github.com/StringNLPLAB/opd-rlvr)

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

本文研究如何组合在策略蒸馏与可验证奖励强化学习，指出将二者拆成“先蒸馏、后强化学习”的连续阶段，比在同一步中混合两种训练信号更能发挥其互补作用。

**不用术语来说**：训练大语言模型解决数学和逻辑推理题时，可以让强教师逐词指导，也可以只根据最终答案对错进行奖励。前者指导细致但可能把学生限制在教师的行为范围内，后者目标直接却因反馈稀疏而需要大量试错。真正困难的不是简单选择其中一种方法，而是决定以何种顺序和方式使用两类反馈，避免它们在训练中互相干扰。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将已有的 OPD–RLVR 联合方法归纳为加权相加与教师调制两类，并提出一个此前缺乏系统研究的替代方案：先执行 OPD，再单独执行 RLVR。
- 作者从 `$pass@k$` 行为、训练动态和参数更新三个角度提出一致解释：OPD 先扩大教师支持范围内的可行解覆盖，RLVR 再提高其中高奖励解的生成概率；分阶段训练因此优于同时混合两种信号。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究推理型大语言模型的后训练，即在预训练完成后，利用任务反馈或更强模型的指导来提升模型解决数学与逻辑问题的能力。核心场景同时包含两类信号：强化学习与可验证奖励（RLVR）依据答案是否正确等可自动检查的结果奖励优化模型；在策略蒸馏（OPD）则让教师模型在学生模型自己生成的轨迹上提供逐词监督。前者直接对应真实任务目标，但奖励通常只在完整输出层面给出，因而较稀疏；后者为每个生成词提供更密集的学习信号，但主要学习教师行为这一代理目标，模仿教师并不必然等价于最大化实际任务表现。本文因此考察这两种后训练信号应如何组合，并将重点放在顺序组合与单步联合组合的差异上。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**强化学习与可验证奖励（RLVR）**

模型针对输入问题生成完整回答，并依据规则、测试器或答案匹配器判断结果是否正确，再用这一结果奖励更新生成策略。由于同一完整轨迹中的所有词通常共享结果奖励，模型较难直接知道中间哪一步推理有助于最终正确。

</div>
<div class="concept-item" markdown="1">

**在策略蒸馏（OPD）**

学生模型先按照自己的当前策略生成回答，教师模型随后对这些学生轨迹中的每个位置给出下一个词的概率分布，学生再学习提高教师更偏好的词的概率。它与只训练教师生成文本的普通监督微调不同，因为监督数据来自学生自己的生成分布，能减少训练分布与实际使用分布之间的不一致。

</div>
<div class="concept-item" markdown="1">

**策略梯度与优势**

策略梯度通过调整模型生成各词的概率来提高期望目标；优势可以理解为某个动作或词相对于基准表现好坏的学习权重。RLVR中的优势由可验证结果奖励计算，OPD中的逐词优势则由教师与学生对该词的对数概率差异计算，二者都能写成逐词加权的策略梯度更新。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定问题输入 $x$，学生策略 $\pi_{\theta}$ 自己采样一条或一组回答 $y=(y_1,\ldots,y_{|y|})$，其中每个 $y_t$ 是第 $t$ 个生成词。任务提供可验证的结果奖励 $R(x,y)$，教师策略 $\pi_T$ 则在学生生成的每个历史上下文上提供下一词分布；学生的目标是在保持自身生成分布可学习的前提下，提高真实任务正确率。RLVR使用整条回答的结果奖励，本文采用基于同一问题多条采样回答进行组内标准化的策略优化形式；OPD则最小化学生轨迹分布与教师轨迹分布之间的反向KL散度，并将其分解为逐词监督。研究比较三类设置：只使用OPD、只使用RLVR，以及在同一训练步骤融合两种信号的联合方法；主要问题是这些信号应在每一步同时作用，还是先用OPD扩展学生能力覆盖范围，再用RLVR针对真实任务目标进行强化。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\pi_{\theta}$**

参数为 $\theta$ 的学生策略，即给定输入及已有生成前缀后，对下一个词进行概率建模的语言模型。

</div>
<div class="notation-item" markdown="1">

**$\pi_T$**

教师策略，通常指能力更强的教师语言模型；它在学生自己的生成历史上提供逐词概率分布。

</div>
<div class="notation-item" markdown="1">

**$R(x,y)$**

输入 $x$ 与回答 $y$ 的可验证结果奖励，反映该完整回答是否满足任务要求，而不是直接评价每个中间词。

</div>
<div class="notation-item" markdown="1">

**$h_t^{(i)}$**

第 $i$ 条学生采样回答在生成第 $t$ 个词之前的历史，即输入 $x$ 与此前词序列 $y_{<t}^{(i)}$ 组成的上下文。

</div>

</div>

**直接相关的工作**

- **Shao et al. (2024) 的 GRPO/RLVR 路线**: 本文将 GRPO 作为强化学习形式：从旧学生策略中为同一输入采样一组回答，按各回答的可验证结果奖励进行组内归一化，并把所得优势用于逐词策略更新。该路线代表了本文所研究的稀疏、结果导向监督来源。
- **Lu and Lab (2025) 的 OPD 路线**: 本文采用其在策略蒸馏的基本思想：在学生自己采样的轨迹上使用教师的逐词分布进行监督，并将教师信号表示为逐词的 OPD 优势。本文不是重新提出 OPD，而是研究 OPD 与 RLVR 在联合训练和两阶段训练中的交互关系。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

推理模型的后训练需要同时解决“怎样获得足够细致的学习指导”和“怎样直接优化真实任务成绩”两个问题。RLVR 使用答案可验证性形成序列级奖励，能够对准最终正确率，但中间推理步骤几乎没有反馈；OPD 则在学生自己生成的轨迹上查询教师，并用教师的下一词分布提供密集监督，学习效率较高，却只是在优化教师模仿这一代理目标。实际训练流程因此需要一种可靠的组合方式，在降低探索成本的同时，不让模型最终性能受教师能力或模仿目标限制。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **加权相加式联合优化**：在同一个训练步骤内，将 RLVR 的优势信号与 OPD 的逐词优势信号按权重相加，以所得统一的词元级优势更新学生模型；它试图直接兼顾任务奖励与教师监督。
- **教师调制式联合优化**：仍由可验证奖励决定更新方向的正负，但利用教师信号调整 RLVR 优势的幅度；也就是说，教师影响每次更新有多强，而最终答案奖励决定更新朝哪个方向进行。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- RLVR 的序列级奖励虽然直接对应任务目标，却无法细致评价每个中间推理步骤，导致学生必须通过大量试错发现高奖励行为；当初始策略覆盖的正确解较少时，这种探索尤其困难。
- 现有混合方法在同一步骤中融合 OPD 与 RLVR。作者的分析表明，两种信号可能在对扩大解覆盖有关键作用的参数上产生冲突，使联合训练牺牲 OPD 带来的大 `$k$` 下 `$pass@k$` 增益；与此同时，持续包含蒸馏目标还可能使学习动态受到教师性能约束。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作主要研究如何在单次更新中融合教师的密集词元级监督与可验证奖励，却未充分比较一种更简单的时间解耦方案，也缺少对两类信号究竟是互补还是相互干扰的机制性解释。特别是，尚不清楚先让学生吸收教师所支持的多种解法、再用真实奖励集中概率质量，是否会比始终联合优化更有效；实践中何时从 OPD 切换到 RLVR，以及 OPD 是否比传统离策略监督微调更适合作为 RLVR 的起点，也缺乏明确依据。

</div>
<div markdown="1"><span>核心问题</span>

对于推理大语言模型，应当在同一步中联合优化 OPD 与 RLVR，还是将二者安排为 OPD-then-RL 两个连续阶段；若分阶段更好，其优势能否由解法覆盖、学习动态与参数更新中的信号交互共同解释，并据此给出可操作的切换标准？

</div>
<div markdown="1"><span>作者直觉</span>

可以把 OPD 看成先由教师帮助学生建立一张较宽的“解题路线图”：学生在自己的生成轨迹上得到逐词指导，因此更容易覆盖教师认可的多种候选解，表现为较大 `$k$` 时更可能至少采样到一个正确答案。随后，RLVR 不再承担从零发现路线的主要负担，而是依据最终答案是否正确，把概率集中到这些已有路线中的高奖励部分，从而改善单次生成表现。若两种目标同时施加，模仿教师与追逐任务奖励可能要求同一批参数朝不同方向变化；顺序训练则让它们分别完成“扩展覆盖”和“强化优解”的职责。该直觉来自作者对实验现象的解释，其适用范围目前主要限于外部强教师、冻结教师以及在策略反向 KL 蒸馏目标等论文设定。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

方法提出两阶段训练范式 $\mathrm{OPD}\text{-then-}\mathrm{RL}$：先用教师模型提供的逐 token 分布监督进行 on-policy distillation（OPD），再切换为仅使用可验证奖励的 GRPO。训练输入是任务问题、教师生成的响应以及学生模型采样的 rollout；第一阶段输出覆盖更广、接近教师支持区域的学生策略，第二阶段在该策略支持内利用奖励信号进行强化和筛选。直观地说，OPD 先帮助学生学会“哪些解法可能存在”，RL 再帮助学生提高“其中哪些解法最值得保留”；作者认为把两个信号放在同一个更新中会互相干扰，而顺序使用可以避免这种冲突。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 教师与学生初始化

冻结教师模型并让其对问题生成回答或 token-level 概率分布；学生模型从基座参数开始训练。教师输出既用于 OPD 的密集监督，也用于后续分析教师支持区域。

<div class="method-step__io" markdown="1">

**输入**：教师模型 $Qwen3\text{-}8B$ 或跨模型实验中的 $OLMo\text{-}3.1\text{-}32B\text{-}Instruct$，以及学生基座模型 $Qwen3\text{-}1.7B\text{-}Base$；输入任务问题 $x$。<br>
**输出**：教师轨迹、教师 token 分布和待训练的学生策略 $p_S$。

</div>

**直观理解**：教师像一个会解题但不直接替学生更新参数的示范者，学生则从零开始学习如何产生类似的推理轨迹。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### OPD 分布对齐阶段

在前 $S$ 个训练步最大化 OPD 目标，使学生在生成轨迹的每个位置学习教师支持的 token 分布；实验主设定取切换点 $S=60$。该阶段不把稀疏的最终可验证奖励直接混入同一个更新目标。

<div class="method-step__io" markdown="1">

**输入**：问题 $x$、教师策略 $p_T$ 的 token-level 输出、学生策略 $p_S$ 的 on-policy 响应，以及 OPD 信号 $d_t^{(i)}$。<br>
**输出**：经过 OPD 初始化的学生策略，具有更高的教师支持解覆盖率和较强的初始验证集性能。

</div>

**直观理解**：这一步不是只告诉学生最后答案对不对，而是沿着整条解题过程逐词提供提示，因此能更快建立可行解法的范围。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 切换到纯 GRPO

当训练步数超过 $S$ 后，将算法优势改为 GRPO 优势 $\hat{A}^{(i)}$，使用组内相对奖励和 PPO clipping 更新学生；此后不再把 OPD 优势与 RL 优势加权融合。

<div class="method-step__io" markdown="1">

**输入**：OPD 阶段得到的学生策略、学生采样的多条 rollout、每条 rollout 的可验证奖励 $R^{(i)}$。<br>
**输出**：经过奖励驱动优化的最终学生策略 $p_S$。

</div>

**直观理解**：学生先用教师搭好“解法地图”，再让验证器挑选地图中真正能得到正确答案的路线，并提高这些路线的概率。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成与评估

对逻辑与数学基准生成答案，由任务验证器判断正确性，计算 $\mathrm{pass}@1$ 和 $\mathrm{pass}@32$；同时通过训练曲线、教师分布距离、共享概率质量和参数更新符号冲突率分析训练机制。

<div class="method-step__io" markdown="1">

**输入**：最终学生策略和未见测试问题；每个问题可采样多条回答。<br>
**输出**：最终正确率、不同采样预算下的覆盖与锐化表现，以及对 OPD 与 RL 是否冲突的机制证据。

</div>

**直观理解**：$\mathrm{pass}@1$ 检验模型一次是否能答对，$\mathrm{pass}@32$ 检验给它更多尝试后是否至少有一条正确；两者结合可区分“提高最可能答案质量”和“扩大可找到正确答案的范围”。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 统一的 PPO 裁剪代理目标

$$
\min\!\bigl(\rho^{\mathrm{alg}}_{i,t}A_{t}^{(i)},\,\operatorname{clip}(\rho^{\mathrm{alg}}_{i,t},1\pm\epsilon)A_{t}^{(i)}\bigr)
$$

**符号说明**

- $\rho^{\mathrm{alg}}_{i,t}$：算法 $\mathrm{alg}$ 下第 $i$ 条 rollout 在时间步 $t$ 的重要性比率，即新旧策略对相应 token 概率的比值。
- $A_t^{(i)}$：第 $i$ 条 rollout 在时间步 $t$ 使用的优势信号；不同方法可取 GRPO 优势、OPD 信号或它们的组合。
- $\epsilon$：PPO clipping 的裁剪范围，限制策略概率比率偏离 $1$ 的幅度。
- $\operatorname{clip}$：将重要性比率限制在以 $1$ 为中心、由 $\epsilon$ 决定的区间内的操作。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标让有利于训练的 token 概率上升、不利 token 概率下降，但不允许一次更新改变得过猛。各联合基线主要只改变重要性比率和优势定义，因此可以比较“如何融合信号”本身的影响。<br>
**原文位置**：第 3 节 Table 1 后的统一目标说明

</div>

</div>

<div class="equation-block" markdown="1">

#### OPD-then-RL 的阶段切换优势

$$
A^{\mathrm{alg},(i)}_{t}=\begin{cases}d^{(i)}_{t},&\text{training step}\leq S,\\[2pt]\hat{A}^{(i)},&\text{otherwise},\end{cases}
$$

**符号说明**

- $A_t^{\mathrm{alg},(i)}$：第 $i$ 条 rollout 在时间步 $t$ 的实际训练优势。
- $d_t^{(i)}$：OPD 提供的逐 token 蒸馏信号。
- $\hat{A}^{(i)}$：GRPO 根据可验证奖励构造的 rollout 级优势。
- $S$：OPD 切换到纯 GRPO 的训练步数。

<div class="equation-explanation" markdown="1">

**直观理解**：前 $S$ 步只听教师，之后只听验证奖励；因此 OPD 与 RL 不会在同一个参数更新中争夺方向。本文主实验使用 $S=60$，并额外研究更早或更晚切换的影响。<br>
**原文位置**：第 3.2 节“ A Sequential Approach: OPD-then-RL”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练始终采用 PPO-style clipped surrogate，但优势来源随阶段变化。OPD 阶段以 $d_t^{(i)}$ 替代奖励优势，优化学生对教师 token 分布的跟随；切换后以 $\hat{A}^{(i)}$ 进行纯 GRPO 更新，利用可验证奖励强化正确 rollout。与 KDRL、SRPO、HDPO、TRRD 和 RLSD 等联合方法不同，本文不在单次更新中对两个优势做加法、掩码或调制。作者的机制解释是：OPD 主要扩大教师支持解的覆盖，RL 主要在该支持内进行概率集中；同步优化会使这两个方向产生干扰。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. On-policy distillation**

OPD 在学生自身采样轨迹上使用教师的逐 token 分布作为密集监督，记其优势或训练信号为 $d_t^{(i)}$。与离线 SFT 只拟合固定数据不同，on-policy 机制使教师信号作用于学生当前实际访问的状态和生成位置。

> 直观理解：学生不是机械背诵一批固定答案，而是在自己尝试解题时获得教师对每一步选择的指导，因此更适合把教师能力迁移到学生策略中。

**2. GRPO 与可验证奖励**

GRPO 使用同一问题生成的一组 rollout，通过最终可验证奖励 $R^{(i)}$ 构造组相对优势 $\hat{A}^{(i)}$，再配合 PPO 风格裁剪限制策略更新。该信号通常是序列级、稀疏的，但直接对应答案是否满足任务验证器。

> 直观理解：教师告诉学生过程像不像高质量示范，验证器则只检查最终答案是否正确；GRPO 通过比较同一问题的多次尝试，奖励组内更好的尝试。

**3. 硬切换调度**

算法优势按训练阶段定义为 $A_t^{\mathrm{alg},(i)}=d_t^{(i)}$（训练步 $\leq S$），或 $A_t^{\mathrm{alg},(i)}=\hat{A}^{(i)}$（训练步 $>S$）。作者将其与 KDRL-annealing 对比：后者逐渐降低 OPD 权重，而本文方法直接从 OPD 更新切换到纯 GRPO 更新。

> 直观理解：不是同时踩油门和刹车，而是先完整完成模仿阶段，再完整进入奖励优化阶段；实验结果支持这种清晰的阶段边界。

**训练与推理**

训练时，教师 $Qwen3\text{-}8B$ 为问题产生示范分布，学生 $Qwen3\text{-}1.7B\text{-}Base$ 先进行 OPD 共 $S=60$ 步，再使用同等总训练步预算的纯 GRPO。GRPO 阶段对每个问题采样一组回答，用任务验证器得到 $R^{(i)}$，计算组相对优势并进行裁剪策略更新；推理时仅使用最终学生模型生成答案，不需要教师或额外的 OPD 信号，评测则通过一次或最多 $32$ 次采样计算 $\mathrm{pass}@1$ 与 $\mathrm{pass}@32$。

**复现信息**

主实验使用 $Qwen3\text{-}8B$ 非 thinking 模式教师和 $Qwen3\text{-}1.7B\text{-}Base$ 学生；逻辑任务包括 ReasoningGym 的 Knights & Knaves、Zebra Puzzles 和 Countdown，并分别独立训练与评估。数学任务使用 DeepMath-103K 训练，在 MATH-500、AMC23、AIME24 和 AIME25 上测试；所有方法使用相同总训练步预算，KDRL-annealing 的 $\beta$ 从 $0.2$ 线性降至 $0.002$，联合加法方法的 $\beta$ 使用任务特定消融得到的最优值。作者还用 Qwen3-0.6B 学生和 OLMo 跨模型组合验证可迁移性，并以训练动态、共享概率质量、参数符号冲突率和配对 bootstrap 检验补充主结果。原文未明确报告完整的 OPD 目标公式、GRPO 优势具体计算式及全部优化器超参数。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Reasoning Gym中的三个程序生成逻辑任务：Knights & Knaves、Zebra Puzzle和Countdown。每个任务固定随机种子为$1$，生成$20{,}000$个训练实例；评估时从相同难度配置中以随机种子$42$抽取$512$个问题。其作用是测试方法在不同形式的可验证逻辑推理上的表现：前两个任务要求精确匹配逻辑或约束满足答案，Countdown要求构造满足数字多重集和目标值约束的算术表达式。证据：“For each logic task, we sample 20,000 training instances using random seed 1, fixing the training set across all methods.”（Appendix A.1.1）
- DeepMath-103K训练集，约$103$K道数学推理题，每题带有可验证的最终答案，并使用官方$\mathrm{math\text{-}verify}$封装器计算规则奖励。它用于检验方法在大规模、可验证数学推理训练及外部数学基准上的迁移效果。证据：“We train on DeepMath-103K (He et al., 2025) training split, a large-scale dataset of approximately 103K problems curated specifically for mathematical reasoning RL.”（Appendix A.1.2）
- 数学推理测试集$\mathrm{MATH\text{-}500}$、$\mathrm{AMC23}$和$\mathrm{AIME24/25}$。它们承担独立评估角色，其中$\mathrm{MATH\text{-}500}$覆盖较广的竞赛数学题，$\mathrm{AMC23}$与$\mathrm{AIME24/25}$用于检验更具挑战性的数学推理能力。原文未明确报告各测试集的具体样本数。证据：“For mathematical reasoning we evaluate on MATH-500, AMC23, and AIME24/25, with maximum generation length 8192 tokens for MATH-500 and 16384 tokens for AIME and AMC.”（Appendix A.4）

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**$\mathrm{pass@1}$**

每道题只取一个采样答案时的正确率；在这些任务中由题目验证器判断答案是否满足规则。 （越高越好，因为它直接衡量模型单次生成成功的概率。）

</div>
<div class="metric-item" markdown="1">

**$\mathrm{pass@k}$**

每道题采样$k$个答案时，至少有一个答案正确的比例；论文用它分析模型覆盖多种可行解的能力，并特别报告了$\mathrm{pass@128}$消融设置。 （越高越好；它反映候选解覆盖范围，但不等同于单次部署时的可靠性。）

</div>
<div class="metric-item" markdown="1">

**验证器得分**

训练和部分评估中由任务专用验证器返回的正确性信号。Knights & Knaves与Zebra Puzzle主要采用精确匹配的$0/1$判断；Countdown在可解析但不满足全部条件时给$0.05$，空或不可解析时给$0.01$，完全满足条件时给$1.0$。 （越高越好；它是可验证奖励而非人工质量评分，不能覆盖验证器未编码的表达质量或推理过程质量。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 总体比较：$\mathrm{OPD\text{-}then\text{-}RL}$与纯$\mathrm{OPD}$、纯$\mathrm{RLVR}$及联合融合基线在逻辑和数学推理基准上的比较。

<div class="result-value" markdown="1">

作者报告两阶段方法持续优于上述对照方法，但所给章节未提供具体任务、模型和表格中的数值差异。

</div>

这支持“先扩展能力覆盖、再用奖励筛选和强化”的总体经验结论；但由于当前材料没有完整结果表，不能据此判断每个数据集、每个模型或每个指标上的提升幅度，也不能确认统计显著性。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In this paper, we show that a simple two-stage scheme, OPD-then-RL, consistently outperforms pure OPD, pure RLVR, and all such joint baselines across logic and math reasoning benchmarks.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 采样覆盖行为：比较不同训练方案的$\mathrm{pass@k}$表现，并据此解释$\mathrm{OPD}$阶段与$\mathrm{RL}$阶段的分工。

<div class="result-value" markdown="1">

作者的解释是，$\mathrm{OPD}$扩大教师支持解的覆盖范围，而$\mathrm{RL}$在这一支持范围内进一步提高解的质量；当前材料未包含对应曲线、具体$k$值结果或数值。

</div>

该结果若由完整实验支持，意味着两阶段方法的优势不只是单次答案概率变高，还包括先产生更多潜在正确解、再把概率集中到其中较可靠的解上。不过，现有摘录不足以单独验证这一机制解释。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

OPD expands the student's coverage of teacher-supported solutions and RL sharpens within that support, while jointly optimizing the two signals causes them to interfere.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 切换时机与冷启动：考察$\mathrm{OPD}$验证集得分作为阶段切换信号，以及$\mathrm{OPD}$相对$\mathrm{SFT}$作为$\mathrm{RL}$初始化的效果。

<div class="result-value" markdown="1">

作者报告$\mathrm{OPD}$验证集得分是决定切换到$\mathrm{RL}$的关键信号，并且$\mathrm{OPD}$比$\mathrm{SFT}$更适合作为$\mathrm{RL}$冷启动；当前材料没有给出切换阈值、具体曲线或数值。

</div>

这一结论把方法从“固定轮数的实验方案”推进到可操作训练规则：当蒸馏阶段的验证表现达到合适状态时再开始强化学习。但没有完整消融数据时，无法知道该信号是否在所有任务和模型规模上都可靠，也不能确定它是否优于其他可能的切换标准。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

To provide a practical recipe, we find that the OPD validation score is the key signal for when to switch to RL, and that OPD is a better cold start for RL than SFT.

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

- 纯$\mathrm{OPD}$：只使用教师的逐token监督，不使用验证器驱动的强化学习；用于检验密集蒸馏信号单独能达到的效果。
- 纯$\mathrm{RLVR}$：只使用可验证奖励进行强化学习；用于检验稀疏但任务对齐的验证器奖励单独能达到的效果。
- 加权相加类联合方法，包括$\mathrm{KDRL}$和$\mathrm{KDRL\text{-}mask}$：在同一训练步骤中把教师信号加入验证器优势函数；用于比较“同时优化两个信号”与“两阶段优化”的差异。
- 教师调制或重塑类联合方法，包括$\mathrm{HDPO}$、$\mathrm{TRRD}$和$\mathrm{RLSD}$：通过重缩放优势函数或修改重要性比率来融合教师信号与强化学习信号；用于覆盖不同的联合设计，而不是只比较一种加权方式。原文说明这些方法统一置于相同的$\mathrm{GRPO}$骨干中，并将原本的自蒸馏教师替换为外部教师。

**实验想回答的问题**

- 在逻辑推理与数学推理任务上，分两阶段的$\mathrm{OPD}\text{-then-}\mathrm{RL}$是否稳定优于纯$\mathrm{OPD}$、纯$\mathrm{RLVR}$以及将两种信号在同一步联合的基线方法？
- 为什么先进行$\mathrm{OPD}$再进行$\mathrm{RLVR}$有效，以及什么信号可以决定从$\mathrm{OPD}$切换到$\mathrm{RLVR}$？

**实验实现**

所有方法使用相同的$\mathrm{veRL}$训练框架、$\mathrm{vLLM}$ rollout、$\mathrm{FSDP}$分片、$\mathrm{bf16}$精度和$\mathrm{GRPO}$骨干，以减少工程差异造成的偏差。学生模型为$\mathrm{Qwen3\text{-}1.7B\text{-}Base}$或$\mathrm{Qwen3\text{-}0.6B\text{-}Base}$，教师为$\mathrm{Qwen3\text{-}8B}$；教师和参考模型冻结，不加入显式$\mathrm{KL}$惩罚，即$\beta_{\mathrm{KL}}=0$。训练使用学习率$1\times10^{-6}$、梯度裁剪$1.0$、$\mathrm{PPO}$裁剪比$0.2$；Reasoning Gym训练$150$步，DeepMath训练$120$步。评估时使用温度$0.7$、$\mathrm{top}\text{-}p=0.8$、$\mathrm{top}\text{-}k=20$，每题采样$32$个completion，训练和评估采用相同的提示构造、答案抽取与验证流程。由于教师与学生的$\mathrm{EOS}$词元不同，所有使用逐token教师信号的方法都屏蔽最终$\mathrm{EOS}$位置，以避免把词表不匹配误当作蒸馏误差。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 加权相加方法的$\beta$消融：在Reasoning Gym上比较$\beta\in\{1,0.2,0.02,0.002\}$的验证集$\mathrm{pass@1}$随训练步数变化。 | 作者据此为$\mathrm{K\&K}$和Zebra Puzzle选择$\beta=0.2$，为Countdown选择$\beta=0.02$；当前材料没有给出曲线中的具体分数或最优差距。 | $\beta$控制教师信号相对于验证器优势的强度。该消融测试联合方法是否对信号权重敏感，并说明不同任务可能需要不同尺度；它不能证明这些取值对所有模型或数据集普适。 | Figure 6及Appendix A.2、A.3<br><span class="experiment-evidence">Based on this ablation, we use β=0.2 on K&K and Zebra and β=0.02 on Countdown for all weighted-additive methods reported in Table 2.</span> |
| 阶段与初始化的比较：比较固定的$\mathrm{OPD\text{-}then\text{-}RL}$流程、联合训练，以及以$\mathrm{SFT}$而非$\mathrm{OPD}$作为$\mathrm{RL}$冷启动的方案。 | 作者报告$\mathrm{OPD\text{-}then\text{-}RL}$优于联合基线，且$\mathrm{OPD}$优于$\mathrm{SFT}$作为冷启动；具体消融数值、训练曲线和切换规则在所给摘录中未提供。 | 这一比较试图区分“先后顺序”的作用与“仅仅增加一个初始化阶段”的作用。若完整结果成立，优势更可能来自$\mathrm{OPD}$先建立教师支持的解空间，而不是来自额外训练步数本身；不过需要完整表格确认各方案训练预算是否严格匹配。 | Abstract<br><span class="experiment-evidence">Together, our results establish OPD-then-RL as a simple yet strong way to combine the two methods, turning two entangled signals into complementary stages.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：研究 OPD 与 RLVR 的分阶段后训练组合，以提升语言模型的数学和逻辑推理能力。; rule check: matched taxonomy keywords; top rule score=5.0
- 全文指纹：`525c61774af5277fb69e0bbb66fbe30b50161027303d6b5b2b98f249769c503f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
