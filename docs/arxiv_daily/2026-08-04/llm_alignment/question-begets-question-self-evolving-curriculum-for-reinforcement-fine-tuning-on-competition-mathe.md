---
title: "[论文解读] Question Begets Question: Self-Evolving Curriculum for Reinforcement Fine-Tuning on Competition Mathematics"
description: "[arXiv 2608.01522][对齐 / RLHF] 本文研究在训练数据稀缺且缺少可靠推理过程监督时，如何通过动态适配模型能力的合成题课程，突破竞赛数学强化微调中的性能平台期。"
arxiv_id: "2608.01522"
announcement_date: "2026-08-04"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:58:19.371334+00:00"
source_sha256: "66950f765407542271fadfac381a5af22a84712400a66b9f3440ed5a70519ef0"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "竞赛数学"
  - "强化微调"
  - "可验证奖励"
  - "课程学习"
  - "合成数据"
  - "自演化训练"
  - "Question-begets-Question"
  - "AIME"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.01522</p>

# Question Begets Question: Self-Evolving Curriculum for Reinforcement Fine-Tuning on Competition Mathematics

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Longtian Bao, Jianyou Wang, Yang Zhang, Youze Zheng, Ramamohan Paturi</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01522v1) · [PDF 下载](https://arxiv.org/pdf/2608.01522v1) · **关键词** 竞赛数学, 强化微调, 可验证奖励, 课程学习, 合成数据, 自演化训练, Question-begets-Question, AIME<br>


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

本文研究在训练数据稀缺且缺少可靠推理过程监督时，如何通过动态适配模型能力的合成题课程，突破竞赛数学强化微调中的性能平台期。

**不用术语来说**：面对模型尚未掌握的困难技能，仅仅增加训练题往往不够：真实题目数量有限，逐步解答难以获得或未必可靠，而批量生成的题目又可能彼此相似，导致模型反复练习同类内容并很快停止进步。作者以对 Qwen2.5-Math-7B 较难的 AIME 竞赛数学为受控场景，要求训练只使用题目和可验证的最终答案，不依赖教师模型给出的解题过程，从而考察性能上限究竟来自模型能力本身，还是来自训练数据组织不当。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 Question-begets-Question（QbQ）合成机制：教师模型从已有数学题出发，通过改变所考查的具体侧面生成技能相关但更具多样性的变体，使稀缺的真实题能够持续派生训练材料；强化学习阶段只使用题目与最终答案，不把教师推理轨迹作为监督。
- 提出自演化课程：每轮评估当前模型，再以模型经常答对但尚未稳定掌握的题目为种子生成下一轮变体。作者据此主张，静态训练呈现的性能平台并非必然的模型能力上限，课程的数据选择与轮次组织本身能够影响强化微调是否继续进步。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型的数学推理强化微调领域，研究如何让一个尚不擅长竞赛数学的模型，仅凭题目与可自动核验的最终答案获得新能力。作者选择 AIME 作为受控试验场：它比 GSM8K、MATH-500 更难，又不同于要求书面证明且难以自动评分的 USAMO、IMO；AIME 的答案均为整数，约四十年的竞赛提供了超过一千道格式统一的题目，因此适合使用可验证奖励进行训练。该场景集中体现三项现实约束：高难度训练题稀缺、正确推理过程通常不可得，以及固定训练分布下的强化微调可能随数据增加而进入性能平台期。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**可验证奖励强化微调**

模型生成解题过程和最终答案后，训练系统通过答案是否正确给出奖励，并据此调整模型，而不要求人工提供标准推理轨迹。本文采用 GRPO 完成这种训练，但输入监督仅包含题目和最终答案。

</div>
<div class="concept-item" markdown="1">

**pass@k**

对同一道题独立采样 $k$ 次回答，并依据成功样本统计模型的解题能力；本文用 pass@1 表示单次作答表现，用 pass@16 的成功次数衡量一道题对当前模型的难度。这里的 pass@16 分组实际记录 16 次采样中答对的次数，例如 $8\leq n\leq15$ 表示模型通常能答对、但尚未完全掌握。

</div>
<div class="concept-item" markdown="1">

**课程学习**

课程学习根据学习者当前能力选择或组织训练样本，使样本既能产生有效奖励信号，又不至于简单到无需学习或困难到几乎从不成功。本文的课程不是从固定题库反复抽样，而是让训练题分布随模型能力逐轮演化。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

基础模型为 Qwen2.5-Math-7B，目标任务是求解 AIME 高中竞赛数学题；每个输入是一道题目，模型输出自然语言推理及一个整数最终答案，训练奖励可由最终答案自动核验。作者使用 2024 年以前可获得的 1,005 道带解答 AIME 题构造初始训练资源，并在 AIME 2025 与 2026 上评估；基础模型的 pass@1 约为 $5.6\%$，说明该任务明显超出其初始能力。研究假设训练时没有可信的标准推理轨迹，因此模型不会看到教师的逐步解答，只使用问题陈述和最终答案进行强化学习；同时在匹配的数据量与计算预算下，比较固定真实或合成数据训练和会随当前检查点改变的自演化课程，以判断观察到的平台期究竟是模型固有限制，还是训练分布选择不当造成的。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\operatorname{pass@}1$**

每道题只采样一次回答时的解题通过率，用于报告模型总体性能。

</div>
<div class="notation-item" markdown="1">

**$n$**

对一道题进行 16 次独立采样后得到的正确次数，取值为 0 至 16。

</div>
<div class="notation-item" markdown="1">

**$8\leq n\leq15$**

“大多能答对但尚未掌握”的难度区间；这些题被选作下一轮 QbQ 变体生成的种子。

</div>
<div class="notation-item" markdown="1">

**$T_d$**

训练数据或训练分布的抽象记号；本文核心设定是该分布不固定，而是依据当前模型能力逐轮更新。

</div>

</div>

**直接相关的工作**

- **能力边界附近的自适应课程学习（Chen et al., 2025, 2026b；Sundaram et al., 2026；Lee et al., 2026）**: 这些工作同样认为已完全掌握或完全不会的题目提供的学习信号有限，并据模型当前能力选择任务。本文的区别是从“经常答对但不稳定”的题目生成新变体，并允许成功变体继续成为后续轮次的种子，使课程的数据分布随模型共同演化，而非仅在固定题库中重新采样。
- **强化微调平台期研究（Cui et al., 2025；Bae et al., 2026；Huang et al., 2026b）**: 既有解释分别强调策略熵下降导致探索不足，以及训练题过易或过难导致有效奖励信号稀少。本文把重点放在训练分布上：在相同数据预算下对照静态训练与动态生成课程，用于检验持续调整题目结构能否突破表面性能上限。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在竞赛数学以及其他专业困难任务中，高质量训练样本通常有限，而且即使最终结果可以核验，可信的逐步推理过程也往往不存在。实际训练因此需要同时解决两个问题：怎样从少量样本扩充出足够多且不重复的练习，以及怎样在不依赖标准推理轨迹的条件下，让模型持续获得新的解题能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **真实数据上的监督微调或结果奖励强化学习**：监督微调利用带解答的既有题目学习输出，GRPO 等强化学习方法则对同一题生成多次回答，并依据最终答案是否正确更新模型。后者可绕开逐步推理监督，但可学习内容仍受固定真实题集的规模和覆盖范围限制。
- **静态合成数据增强**：使用更强的教师模型一次性从固定原题生成大量新题，再把真实题与合成题混合训练，或打乱合成题后进行非课程式训练。其基本假设是增加样本数量和表面变化即可扩大技能覆盖。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 固定真实题集覆盖有限，单纯延长监督微调或强化学习只能重复利用既有信息；当模型已吸收其中容易获得的训练信号后，继续增加更新难以带来相应提升。
- 一次性、静态的数据增强容易生成相似问题，并且不会随模型能力变化而调整难度与内容。即使数据量显著增加，训练材料也可能过易、过难或重复，导致强化学习获得的有效反馈减少并出现性能平台期。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方案尚未区分两种可能性：困难任务上的平台期究竟反映了模型不可突破的能力边界，还是由合成数据缺乏多样性、难度选择不合适及训练顺序静态化造成。尤其缺少一种在固定数据与计算预算下，能够依据当前检查点的能力持续重组训练分布、又完全不使用教师推理轨迹的方法。

</div>
<div markdown="1"><span>核心问题</span>

在仅提供数学题目和可验证最终答案的条件下，能否让训练数据随模型共同演化，并通过选择合适的生成种子与课程顺序，使强化微调突破静态真实数据或静态合成数据训练所表现出的性能上限？进一步说，最有效的种子应是模型最难的失败题，还是模型多数时候能答对但尚未稳定掌握的题？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把训练重点放在“接近掌握但仍不稳定”的能力边界上：这类题既不会难到几乎所有尝试都失败，也不会容易到所有尝试都成功，因此同一题的多次回答更可能同时包含成功和失败，为基于组内比较的强化学习提供有区分度的信号。再从这些题生成考查同一核心技能不同侧面的变体，相当于在模型现有能力附近横向拓展；每轮重新评估和选种，则使练习内容随模型进步而移动，避免长期围绕固定题集重复训练。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把结构化合成数据、基于当前能力的数据筛选和强化学习闭合成一个持续演化的训练循环。输入是由题面与最终答案组成的数学题池 $\mathcal{D}$、初始策略 $\pi_0$、总轮数 $T$ 和每题自评采样数 $k$；每轮先用当前策略估计题目可解程度，再让教师模型仅扩写“多数时候能答对”的题目，从生成题中选择奖励有变化、适合强化学习的样本，最后以最终答案正确性为主要奖励执行 GRPO。更新后的策略重新评估本轮训练题，仍处于“多数答对”区间的题成为下一轮种子，因此训练分布随模型能力变化，而不是遵循预先规定的难度顺序。

技术上的关键是区分“课程种子”和“当前强化学习样本”：种子集合 $S_t$ 只包含更新后正确次数位于种子带 $B$ 的题，用于控制下一轮生成方向；强化学习集合 $R_t$ 则可包含正确次数从 $1$ 到 $k-1$ 的生成题，并优先选择正确次数接近 $k/2$ 的样本。直观地说，系统让模型围绕已经有较稳定理解、但尚未完全掌握的知识点不断出新题，同时把训练资源集中到当前回答既可能成功也可能失败的题上，因为这种题最容易提供“哪种回答更好”的比较信号。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始化题池与初始策略

把一道题形式化为 $p=(x_p,a_p)$，其中 $x_p$ 是题面、$a_p$ 是最终答案；先通过 LoRA 对教师扩写的解答做一次监督微调，得到仅用于建立答题格式和基本任务适应性的初始策略 $\pi_0$。随后对题池中每题采样 $k=16$ 次，取正确次数在 $8$ 至 $15$ 之间的题组成初始种子集合 $S_0$。

<div class="method-step__io" markdown="1">

**输入**：包含 1983–2024 年 AIME 题目的训练池 $\mathcal{D}$，以及 Qwen2.5-Math-7B 基座模型。<br>
**输出**：初始策略 $\pi_0$ 和首轮 QbQ 种子集合 $S_0$；主干模型对应的初始种子数为 $133$。

</div>

**直观理解**：初始化阶段先让模型学会如何按要求作答，再找出它已经会做大半、但偶尔仍会出错的题。教师解题过程只在这一步帮助模型适应格式，后续循环不会把教师推理轨迹作为训练监督。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自评与能力分带

从 $\pi_t(\cdot\mid x_p)$ 独立采样 $k=16$ 个解答，按最终答案是否等于 $a_p$ 统计正确次数 $n_t(p)$；据此分为完全掌握、主要答对、偶尔答对和从未答对四档。课程种子带定义为 $B=\{n:k/2\leq n\leq k-1\}$，即本实验中的 $8\leq n\leq15$。

<div class="method-step__io" markdown="1">

**输入**：第 $t$ 轮当前策略 $\pi_t$，以及待评估题目 $p=(x_p,a_p)$。<br>
**输出**：每题的经验可解程度 $n_t(p)$，以及落入种子带 $B$ 的候选题。

</div>

**直观理解**：单次答对可能来自运气，因此方法用同一道题的多次作答来估计模型掌握程度。全对或全错的题在一组采样中几乎没有奖励差异，而“多数答对但并非全对”的题既表明相关技能已经可用，又仍留有学习空间。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### QbQ 结构化变题

教师先为每道种子规划三个最适合的算子，再分别生成变体；五类算子是“先推广再特化”“参数化并求和”“改变所求量”“构造逆问题”和“增加一层约束”。生成过程禁止只替换数值，并要求变体答案不同于父题答案；训练时仅保留题面和最终答案。

<div class="method-step__io" markdown="1">

**输入**：当前种子集合 $S_t$、每道种子的参考解答，以及五种人工定义的结构变换算子。<br>
**输出**：保持核心解题技能、但在结构上有所变化的新题集合 $V_t=\operatorname{QbQ}(S_t)$。

</div>

**直观理解**：这不是简单改数字，也不是让教师随意写一道相似题，而是规定如何改变题目结构，使新题从另一个角度检查同一知识点。答案必须变化这一低成本检查可进一步排除原题复制和只改措辞的近重复样本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 强化学习样本选择与 GRPO 更新

先排除 $n_t(q)=0$ 或 $n_t(q)=k$ 的题，再从其余题中构造规模为 $N=300$ 的 $R_t$：先为每个父种子保留一个最接近 $k/2$ 的合格变体，再按 $|n_t(q)-k/2|$ 从小到大补足，并施加每个种子的数量上限。对每题采样 $m=8$ 个解答，以最终答案正确性和格式合规奖励计算组内标准化优势，最大化裁剪 GRPO 目标，得到 $\pi_{t+1}$。

<div class="method-step__io" markdown="1">

**输入**：生成题集合 $V_t$、当前策略 $\pi_t$、每题的预更新正确次数 $n_t(q)$ 和目标答案 $a_q$。<br>
**输出**：本轮强化学习集合 $R_t$ 和更新后的策略 $\pi_{t+1}$。

</div>

**直观理解**：GRPO 需要在同一题的多个回答之间比较好坏，因此优先选择大约一半答对、一半答错的题；若所有回答奖励相同，就很难形成有效更新方向。父题覆盖规则则避免训练集被少数容易大量生成变体的种子垄断。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 组内奖励与标准化优势

$$
\begin{aligned} r_i &= \mathbf{1}\!\left[\operatorname{ans}(y_i)=a_q\right]+0.1b_i,\\ \hat A_i &= \frac{r_i-\bar r}{s_r}. \end{aligned}
$$

**符号说明**

- $q$：当前强化学习题目。
- $y_i$：对题目 $q$ 采样得到的第 $i$ 个完整解答。
- $\operatorname{ans}(y_i)$：从解答 $y_i$ 中抽取的最终答案。
- $a_q$：题目 $q$ 的教师生成目标答案。
- $b_i$：格式合规指示变量，取值属于 $\{0,1\}$。
- $r_i$：第 $i$ 个解答的奖励，以答案正确性为主体，并加入权重为 $0.1$ 的格式奖励。
- $\bar r$：同一道题的 $m$ 个采样奖励的均值。
- $s_r$：同一道题的 $m$ 个采样奖励的标准差。
- $\hat A_i$：第 $i$ 个解答相对于同组其他解答的标准化优势。

<div class="equation-explanation" markdown="1">

**直观理解**：奖励首先判断最终答案是否正确，格式奖励只起辅助作用；随后减去同组均值并除以同组标准差，把绝对分数转为同一道题内部的相对优劣。这样无需教师提供逐步推理质量标签，模型仍可提高相对更正确、更符合输出格式的回答概率。原文的行内说明明确称格式项为“small bonus”，此处按其给出的 $0.1b_i$ 语义记录。<br>
**原文位置**：第 3.3 节“GRPO”，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 裁剪 GRPO 优化目标

$$
\begin{gathered} \rho_{i,\tau}(\theta)=\frac{\pi_{\theta}(y_{i,\tau}\mid x_q,y_{i,<\tau})}{\pi_{\mathrm{old}}(y_{i,\tau}\mid x_q,y_{i,<\tau})},\qquad \bar\rho_{i,\tau}=\operatorname{clip}\!\left(\rho_{i,\tau},1-\varepsilon,1+\varepsilon\right),\\ \ell_{i,\tau}=\min\!\left(\rho_{i,\tau}\hat A_i,\bar\rho_{i,\tau}\hat A_i\right),\\ \mathcal J(\theta)=\mathbb E\!\left[\frac{1}{m}\sum_{i=1}^{m}\frac{1}{|y_i|}\sum_{\tau}\ell_{i,\tau}\right]. \end{gathered}
$$

**符号说明**

- $\pi_{\theta}$：参数为 $\theta$、当前正在优化的策略。
- $\pi_{\mathrm{old}}$：本轮开始时锚定于 $\pi_t$ 的旧策略，也是生成训练回答时的参考策略。
- $\rho_{i,\tau}(\theta)$：第 $i$ 个解答在位置 $\tau$ 上，新旧策略给已采样词元分配概率的比值。
- $\bar\rho_{i,\tau}$：限制在 $[1-\varepsilon,1+\varepsilon]$ 内的重要性比率。
- $\varepsilon$：裁剪宽度，本文设为 $0.2$。
- $\ell_{i,\tau}$：位置 $\tau$ 的裁剪代理收益。
- $m$：每道训练题采样的解答数量，本文为 $8$。
- $|y_i|$：解答 $y_i$ 的词元长度，用于对不同长度的回答归一化。
- $\mathcal J(\theta)$：对题目、组内回答及其词元平均后的 GRPO 最大化目标。

<div class="equation-explanation" markdown="1">

**直观理解**：重要性比率衡量新策略相对旧策略改变某个词元概率的幅度，优势为正时提高该回答的概率，优势为负时降低它。裁剪把单次更新限制在旧策略附近，避免少量样本使策略变化过猛；再按回答长度和组大小平均，使不同长度解答对目标的贡献更可比。<br>
**原文位置**：第 3.3 节“GRPO”，公式（2）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标是最大化 $\mathcal{J}(\theta)$。每个 $q\in R_t$ 由旧策略 $\pi_{\mathrm{old}}$ 采样 $m=8$ 个回答，最终答案正确性提供主要奖励，格式合规提供较小附加奖励；组内标准化得到 $\hat A_i$ 后，裁剪重要性比率以限制新旧策略偏移。论文不使用 KL 惩罚，每轮最多进行 $150$ 个优化步骤，约等于对规模为 $N=300$ 的 $R_t$ 完成一次训练遍历；本轮结果记为 $\pi_{t+1}$。该目标与课程选择直接耦合：SelectRL 优先选择 $n_t(q)$ 接近 $k/2$ 的题，以提高组内奖励变化，从而让标准化优势和策略梯度更有信息量。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. QbQ 结构变换生成器**

QbQ 将 $S_t$ 映射为 $V_t$。它采用“规划后生成”的两阶段教师调用：规划器从五个结构算子中为每个种子选出三个适用方向，生成器分别接收种子、参考解答和完整算子说明，并可在算子不适用时放弃生成；只保留新题的题面与答案，且要求 $a_q\neq a_p$。

> 直观理解：该模块解决合成题的两个常见风险：只做表面改写会产生近重复数据，完全自由生成又可能偏离原技能。结构算子相当于给出受控的变题模板，使题目变化足够明显，同时尽量保持所考查的核心方法不变。

**2. 基于奖励方差的 SelectRL**

对二元正确性奖励，若经验正确率为 $\hat p=n_t(q)/k$，组内标准差为 $\sqrt{\hat p(1-\hat p)}$：它在 $\hat p\in\{0,1\}$ 时为零，在 $\hat p=1/2$ 时最大。SelectRL 因此仅从 $1\leq n_t(q)\leq k-1$ 的题中选择，并优先最小化 $|n_t(q)-k/2|$，同时保证父种子覆盖并限制单个种子的样本数。

> 直观理解：如果模型对一道题总是全对或全错，同组回答得到的反馈几乎一样，强化学习无法清楚判断应增加哪类回答的概率。选择成功率接近一半的题，可以得到更强的正负对照；覆盖和限额约束则维持训练内容的广度。

**3. 自演化课程控制器**

控制器用统一的采样计数 $n_t(\cdot)$ 同时驱动生成与训练，但使用不同选择范围：下一轮 QbQ 种子要求 $n_t\in B$，而本轮 GRPO 题可覆盖 $1\leq n_t\leq k-1$。每轮训练后只在 $R_t$ 内重新评分并产生 $S_{t+1}$，测试集表现既不参与样本选择，也不用于提前停止。

> 直观理解：生成种子需要模型已经具备较可靠的技能基础，训练题则可以稍难一些，只要仍偶尔能产生正确回答。把两种门槛分开，使系统既能沿已有能力稳定扩展，又允许暂时较难的题在模型进步后进入后续课程。

**训练与推理**

完整训练过程如下：先通过一次 LoRA 监督微调获得 $\pi_0$，并在训练池 $\mathcal{D}$ 上用每题 $k=16$ 次采样建立 $S_0$；随后对 $t=0,\ldots,T-1$，执行 $V_t=\operatorname{QbQ}(S_t)$，用 $\pi_t$ 对每个生成题评分，调用 SelectRL 构造 $R_t$，再通过 GRPO 得到 $\pi_{t+1}$。更新后重新评估 $R_t$，按 $S_{t+1}=\{q\in R_t:n_{t+1}(q)\in B\}$ 产生下一轮种子；总轮数 $T$ 事先固定， held-out 测试表现不参与选择或停止。最终返回 $\pi_T$。

推理阶段不需要教师模型、QbQ、课程控制器或参考解答，只需将新的数学题面 $x$ 输入最终策略 $\pi_T$，由模型生成包含推理和最终答案的解答 $y$，再读取 $\operatorname{ans}(y)$。论文训练阶段虽然允许模型生成推理文本，但监督信号只检查最终答案和输出格式，教师生成的逐步解答不会进入循环内的强化学习数据。

**复现信息**

为公平解释和复现，关键设定是：训练池含 $1{,}005$ 道 1983–2024 年 AIME 题，最近两个竞赛年份完全留作测试；主模型为 2024 年发布的 Qwen2.5-Math-7B。初始化时用 GPT5-mini 将过于抽象的官方解答扩写后做一次 LoRA 监督微调，但初始化之后只使用合成题的题面和答案，教师推理轨迹不参与训练。主实验中 $k=16$、种子带为 $8\leq n\leq15$、初始种子数为 $133$、每轮强化学习集合大小 $N=300$、每题 GRPO 采样数 $m=8$、裁剪参数 $\varepsilon=0.2$、每轮上限为 $150$ 个优化步骤，并且不加入 KL 惩罚。

QbQ 每个种子先选择三个结构算子，每个“种子—算子”组合单独生成，算子不适用时教师可以放弃；仅改数值被明确禁止，且变体答案必须不同于父题。SelectRL 复用自评阶段已有的 $n_t(q)$，不为选择额外采样；它先保证每个种子的合格变体覆盖，再按与 $k/2$ 的距离补足，并设置每种子的数量上限。文中说明所有自评采样使用固定解码参数，但所给章节未列出这些参数的具体数值；每轮的确切每种子上限、优化器和学习率在所给原文中亦未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 真实训练池由$1983$至$2024$年的$1005$道AIME题组成，每题带官方最终答案。它用于监督初始化、原题GRPO训练、静态增广的源题，以及自演化课程的候选种子池；监督初始化时，教师生成的解题轨迹经过答案格式和长度过滤后保留$963$条。
- QbQ合成训练集共$6000$题，由$20$轮、每轮$300$题构成。课程组保留这$20$个批次的生成顺序，非课程组则对完全相同的题目多重集进行全局随机打乱，因此该数据用于隔离“训练顺序”而非数据内容或规模的作用。静态增广另从每道原题一次性生成$5$道使用相同或相近技巧的变体，得到$5000$道可用题。
- 测试集包含AIME 2025与AIME 2026的全部$60$道题。它们晚于真实训练池，且不参与训练、题目合成、课程构造或模型选择，因此主要衡量时间外、题目外泛化。另设$499$道真实难题组成的迁移子集：监督初始化模型$M0$在采样评估中对这些题的正确率为零，而且课程从不选择它们作为种子。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Pass@1（%）**

对每道测试题采样$16$个回答后，以全部$60\times16=960$个回答中最终答案正确的比例作为单次评估结果；论文对最终检查点使用$3$个采样种子，并报告均值与标准差。它衡量一次随机生成得到正确答案的概率，而不是“给模型多次机会后至少答对一次”的传统pass@$k$。 （越高越好，因为正确回答占比越大，表示单次生成的可靠性越强。）

</div>
<div class="metric-item" markdown="1">

**训练中奖励**

GRPO对每个回答使用“最终答案完全正确”奖励，并叠加$0.1$的答案格式奖励。论文用其与测试Pass@1的走势差异判断模型是在提高训练池拟合程度，还是获得了可迁移能力。 （训练目标上越高越好，但若奖励上升而留出集Pass@1不升，则不能解释为泛化改善。）

</div>
<div class="metric-item" markdown="1">

**跨采样种子的总体标准差$\sigma$**

最终检查点在$3$个评估种子下Pass@1的总体标准差，用于描述随机解码造成的结果波动。 （在均值相近时越低越稳定，但它不是主要能力指标，也不能替代显著性检验。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 从基础模型到监督初始化，再到原始AIME题上的GRPO

<div class="result-value" markdown="1">

基础模型、$M0$和原题GRPO的三种子平均Pass@1依次为$5.62\pm0.15\%$、$9.48\pm0.34\%$和$11.53\pm0.39\%$。这表明教师轨迹初始化和最终答案强化学习都有效，但有限原题池很快被耗尽；单种子训练轨迹曾在$200$次更新达到$13.65\%$，到第$500$次更新却回落至$12.08\%$。

</div>

作者据此主张常规训练在有限真实题上出现平台。直观上，模型确实学到了一些AIME解题能力，但继续在同一批题上更新没有稳定转化为新竞赛题上的提升。由于该基线只有$500$次更新，而QbQ使用$3000$次更新，它能证明原始数据受限，却不能单独证明QbQ优于同算力的所有原题训练方案。

<div class="result-source" markdown="1">

来源：第4.2节“Conventional training quickly exhausts the original problem pool”；表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The base model reaches 5.62% pass@1, confirming that AIME is well beyond its initial capability. Supervised initialization improves pass@1 by 3.86 points to 9.48%, and GRPO on the original AIME problems reaches 11.53%. Further updates on these problems do not yield a stable gain: in a single-seed checkpoint sweep, pass@1 peaks at 13.65% after 200 updates but falls to 12.08% at update 500.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 静态增广与非课程QbQ合成数据的比较

<div class="result-value" markdown="1">

静态增广在增加$5000$道可用变体并完成$2943$次总更新后，Pass@1为$12.05\pm0.34\%$，仅比原题GRPO高$0.52$个百分点；非课程QbQ达到$14.44\pm0.61\%$，比静态增广高$2.39$个百分点。

</div>

作者将该差距解释为QbQ产生的训练题比一次性静态变体更有用。该结果说明“增加什么样的数据”比单纯扩大固定数据池更重要；不过两组题目的确切内容与生成过程不同，且更新数相差$57$次，因此这是有力但并非只隔离生成机制单一变量的因果比较。

<div class="result-source" markdown="1">

来源：第4.2节“More static data do not remove the plateau”；表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Static augmentation increases the training pool by 5,000 usable variants and nearly matches the QbQ update budget, yet its final performance is 12.05 ± 0.34%. This is only 0.52 points above GRPO on the original AIME problems. By contrast, QbQ non curriculum reaches 14.44 ± 0.61%, improving by 2.39 points over static augmentation.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 相同QbQ题目与计算预算下，课程顺序对比全局打乱

<div class="result-value" markdown="1">

QbQ课程训练最终达到$16.46\pm0.45\%$，比非课程QbQ的$14.44\pm0.61\%$高$2.02$个百分点。课程组在最后$600$次更新中从$13.58\%$升至$17.08\%$，增加$3.50$个百分点并在终点达到其最高观测值；非课程组则在$2100$次更新达到$14.55\%$后未再超过该值。

</div>

这是论文最严格的主比较，因为两组使用相同的$6000$道题、初始化、优化器和$3000$次更新，只改变是否保留逐轮顺序。结果支持“让训练分布随模型能力推进”可避免固定分布平台。它仍只证明这一顺序在当前模型、生成器、数据预算和测试集上有效；“无平台”表示截至$3000$次更新仍在上升，并不保证继续训练会无限改善。

<div class="result-source" markdown="1">

来源：第4.2节“The curriculum changes the learning trajectory”；图2与表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

QbQ curriculum behaves differently. In the plotted trajectory, pass@1 rises from 13.58% at 2,400 updates to 15.77% at 2,700 and 17.08% at 3,000. It gains 3.50 points over the last 600 updates and finishes at its best plotted checkpoint, with no observed ceiling. The three-seed endpoint is 16.46 ± 0.45%, 2.02 points above QbQ non curriculum.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 核心结论来自单一$7$B骨干模型、单一教师和AIME领域，且测试仅含两个年份共$60$题；现有证据不足以断言相同课程规则能推广到更大或更小模型、其他竞赛、非数学推理任务，或不同教师生成质量。
- 最终结果的$3$个种子是同一固定检查点的采样评估种子，而不是从数据生成到训练全过程的独立重复；论文未报告训练方差、置信区间或显著性检验。因而$2.02$个百分点的课程优势具有受控比较价值，但其对随机训练与合成数据波动的稳健性仍需额外复现实验确认。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Qwen2.5-Math-7B基础模型：给出未经本文训练时的能力下限，用来确认AIME对该模型确实困难。
- $M0$及其原题GRPO版本：$M0$先学习教师为真实题编写的解题轨迹，随后仅在$1005$道原始AIME题上进行$500$次GRPO更新；该组衡量有限真实数据上的常规监督学习与强化学习能走多远，但因更新次数较少，不是与QbQ严格算力匹配的对照。
- 静态增广：从原题一次性生成约$5000$道变体，并在原题GRPO检查点上继续训练；总计$2943$次更新，与QbQ的$3000$次预算接近，用于检验单纯增加固定合成数据能否消除平台。
- QbQ非课程训练：使用与课程组完全相同的$6000$道QbQ题、初始化、优化器、采样和$3000$次GRPO更新，但将所有题全局打乱；它是检验课程顺序是否有效的最关键对照。

**实验想回答的问题**

- 在真实竞赛数学题稀缺、强化学习只使用题目与最终答案的条件下，原始题训练、一次性静态增广和QbQ生成的数据分别能把Qwen2.5-Math-7B的域外AIME解题能力提升到什么程度？
- 当训练题多重集、初始化、优化器和$3000$次GRPO更新均保持一致时，按模型能力逐轮组织QbQ题目能否突破全局随机打乱训练的性能平台；其中，位于当前能力边界附近的“多数时候答对”种子是否比更难种子提供更有效的学习信号？

**实验实现**

骨干模型为Qwen2.5-Math-7B，上下文长度为$4096$；教师为gpt-5-mini-2025-08-07。$M0$使用秩$32$、缩放系数$64$的LoRA训练$3$轮，学习率为$10^{-5}$并采用余弦调度。后续GRPO每组采样$8$个回答，学习率为$3\times10^{-6}$、裁剪参数为$0.2$且不使用KL惩罚；训练解码温度为$1.0$、最长$3072$ token，因长度上限被截断的回答不计入损失。测试时温度为$0.7$、top-$p=0.8$、最长$3072$ token，每题采样$16$次。两种QbQ策略均从相同初始化出发，使用相同题目多重集与$3000$次更新；所有QbQ强化学习阶段仅接收题目和最终答案，不使用教师推理轨迹。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 是否保留QbQ的逐轮课程顺序 | 在相同$6000$道题和$3000$次GRPO更新下，课程组Pass@1为$16.46\pm0.45\%$，非课程全局打乱组为$14.44\pm0.61\%$，差值为$2.02$个百分点。 | 该消融只改变题目顺序，因此直接隔离课程组织的贡献。结果表明，把为不同能力阶段生成的题混在一起会削弱学习，而保留阶段推进更有效；但论文只报告$3$个解码种子的均值与波动，未提供独立训练重复或统计显著性检验。 | 表1表注及第4.2节“The curriculum changes the learning trajectory”<br><span class="experiment-evidence">Both QbQ variants use the same 6,000 generated problems and 3,000 GRPO updates and differ only in whether the training problems are organized as a curriculum.</span> |
| 课程种子难度带：多数时候答对$8\leq n\leq15$、较难$1\leq n\leq7$与混合$1\leq n\leq15$ | 三种课程的最终Pass@1分别为$16.46\pm0.45\%$、$11.35\pm0.23\%$和$11.91\pm0.30\%$；其中$n$表示$16$次采样中的正确次数。较难种子组中途达到$14.17\%$后失去全部增益，混合组早期峰值为$13.33\%$，之后大致在$10\%$至$12.2\%$之间波动。 | 该实验检验有效性究竟来自“挑更难的题”，还是来自选择能力边界附近的题。只有$8\leq n\leq15$组持续改善，支持“多数时候答对但不稳定”的种子可产生更有信息量的GRPO组内差异。这里改变种子带也会改变后续生成出的题目分布，因此它验证的是完整课程设计选择，而不是在固定合成题上的纯难度效应。 | 附录A“Results”；表2与图3<br><span class="experiment-evidence">The harder- and mixed-seed curricula finish at 11.35 ± 0.23% and 11.91 ± 0.30%, respectively. Both endpoints lie within 0.4 percentage points of the original-problem GRPO baseline and fail to reproduce the gain of the mostly-right curriculum, which reaches 16.46 ± 0.45%.</span> |

**定性案例**

- 固定难题迁移测试可视为集合级案例分析：课程明确排除$499$道$M0$在采样中从未答对的真实题，并且这些题从未作为QbQ种子；训练后该集合的聚合Pass@1从$0.0\%$升至$5.3\%$。它说明收益能扩展到课程选择范围之外，但原文没有给出具体题目、解题轨迹变化或按难度分层结果，因而不能判断迁移发生在哪些数学技能上。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Proposes reinforcement fine-tuning with a self-evolving synthetic curriculum to improve an LLM's competition-mathematics reasoning.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`66950f765407542271fadfac381a5af22a84712400a66b9f3440ed5a70519ef0`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
