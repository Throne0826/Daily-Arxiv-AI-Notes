---
title: "[论文解读] Beyond the Best Guess: Improving LLM Solution Coverage with Evolution Strategies"
description: "[arXiv 2608.12679][对齐 / RLHF] 本文研究面向数学、科学与编程发现任务的后训练选择，主张以进化策略（ES）替代强化学习（RL），从而在提高单次回答准确率的同时，更好地保留多次采样时的解法覆盖率。"
arxiv_id: "2608.12679"
announcement_date: "2026-08-14"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T02:58:53.227621+00:00"
source_sha256: "85c2c77641654975b4c2bb9a277235a7d8c36e010dc679d0241ad65567dfccb7"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "测试时计算扩展"
  - "pass@k"
  - "解空间覆盖"
  - "进化策略"
  - "强化学习"
  - "分布坍缩"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.12679</p>

# Beyond the Best Guess: Improving LLM Solution Coverage with Evolution Strategies

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Conor F. Hayes, Elliot Meyerson, Kajetan Schweighofer, Roberto Dailey, Babak Hodjat, Risto Miikkulainen, Xin Qiu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: The University of Texas at Austin, Austin；Cognizant AI Lab</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12679v1) · [PDF 下载](https://arxiv.org/pdf/2608.12679v1) · **关键词** 大语言模型, 测试时计算扩展, pass@k, 解空间覆盖, 进化策略, 强化学习, 分布坍缩<br>


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

本文研究面向数学、科学与编程发现任务的后训练选择，主张以进化策略（ES）替代强化学习（RL），从而在提高单次回答准确率的同时，更好地保留多次采样时的解法覆盖率。

**不用术语来说**：在发现型任务中，模型往往需要尝试很多次，研究者再从候选答案中寻找至少一个正确解；因此，只让模型最常给出的答案更准确还不够。常规强化学习可能使模型越来越偏爱少数高分答案，把一些不常见但可能正确的解法挤出生成范围，导致增加采样次数后仍难以发现这些解法。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者在匹配计算预算的条件下，系统比较ES与RL后训练模型，覆盖多个模型家族以及从$1.5\mathrm{B}$到$32\mathrm{B}$的参数规模，并以$\mathrm{pass@}k$检验多次采样下的解法覆盖能力。
- 作者将性能比较与输出分布分析、数学基准上的测试时扩展实验结合起来，用于检验ES的优势是否来自更宽广的输出支持，以及这种覆盖优势能否转化为下游求解收益。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型在数学、编程及开放科学发现中的后训练与测试时扩展。模型通常先通过具有可验证结果奖励的强化学习（RLVR）提升推理正确率，再在推理阶段对同一问题采样多个候选解，以计算换取更高的求解成功率。此时，关键能力不再只是生成一次就答对，而是模型的输出分布能否覆盖足够多的可行解，使前 $k$ 次采样中至少出现一个正确答案。论文据此比较强化学习（RL）与进化策略（ES）两类后训练方法：前者通过序列上的策略梯度直接提高高奖励输出的概率，后者通过随机扰动模型权重并评价一组扰动模型来更新参数；二者可能分别偏向单次准确率和多样化解空间覆盖。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**pass@k**

对同一问题从模型输出分布中采样 $k$ 个候选答案，$\mathrm{pass@}k$ 表示其中至少一个答案正确的概率。$\mathrm{pass@}1$ 衡量单次作答准确性，而较大 $k$ 下的表现还取决于正确解是否在输出分布中保有足够概率以及候选之间是否具有有效多样性。

</div>
<div class="concept-item" markdown="1">

**基于可验证奖励的强化学习（RLVR）**

RLVR利用答案是否通过数学判定、代码测试等可自动检查的结果作为奖励，并通过策略梯度提高高奖励生成序列的概率。论文关注的风险是，这种更新可能让概率质量集中到少数高奖励模式，从而删除低概率但仍正确的替代解。

</div>
<div class="concept-item" markdown="1">

**进化策略（ES）**

ES是一类群体式、无梯度优化方法：它在权重空间中对模型参数施加随机扰动，评价由此形成的一组模型，再依据奖励调整参数。与直接强化某些生成序列不同，ES优化扰动参数分布上的期望表现，因而可能把模型推向对权重扰动更稳健、可容纳更多解法的参数区域。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个具有可验证正确答案的推理或发现问题，以及同一基础大语言模型经不同方法后训练得到的模型，研究任务是在匹配计算预算的条件下比较RL与ES。推理时，每个模型从自身输出分布独立生成 $k$ 个候选解，输出关注两层结果：其一是候选集合中是否至少包含一个正确解，即 $\mathrm{pass@}k$；其二是输出分布对不同可行解的覆盖程度及其对下游数学基准测试时扩展的影响。核心假设是，发现任务允许通过增加测试时计算搜索解空间，而且候选答案可以用结果型奖励可靠验证；因此，理想后训练方法不仅要提高 $\mathrm{pass@}1$，还应保留对低概率正确解和替代推理路径的支持。本文的比较范围覆盖多个模型家族及约15亿至320亿参数的尺度，但本节摘录未给出具体模型名称和完整训练配置。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$k$**

针对同一问题从模型输出分布中抽取的候选解数量；文中图1说明测量范围最高到 $k=128$。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{pass@}k$**

在 $k$ 个采样候选中至少出现一个正确解的概率，用于衡量测试时扩展下的解覆盖能力。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{pass@}1$**

只采样一个候选答案时的正确概率，即论文所称“最佳猜测”或单次准确率。

</div>
<div class="notation-item" markdown="1">

**$\theta$**

大语言模型的参数或权重；ES在该参数空间施加随机扰动，而RL主要依据生成序列上的策略梯度更新参数。

</div>

</div>

**直接相关的工作**

- **强化学习策略梯度后训练（包括PPO与GRPO）**: 这是论文的主要比较对象。引言称其通过提高高奖励输出的对数概率来优化单个模型，通常能改善 $\mathrm{pass@}1$，但可能使输出分布向少数高奖励模式集中，从而降低较大 $k$ 下的解覆盖；摘录仅给出参考文献编号，未提供对应论文题名。
- **关于RL后训练导致分布坍缩及基础模型在pass@k上反超RL模型的既有研究**: 该研究现象直接构成本文的问题依据：已有工作报告RL会削弱低概率正确轨迹，并出现基础模型在 $\mathrm{pass@}k$ 上优于RL微调模型的情况；本文进一步在匹配计算预算、多个模型家族与参数尺度下系统比较ES和RL，并分析输出分布差异。摘录未提供该既有工作的题名，仅标注参考文献25与54。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

LLM正被用于数学、科学和编程等发现型问题。这类任务通常不能依赖一次“最佳猜测”，而要通过增加测试时计算，从模型输出分布中抽取$k$个候选并搜索正确解。此时关键指标是$\mathrm{pass@}k$，即$k$次采样中至少出现一个正确答案的概率；要让扩大采样真正有效，模型必须为多种可行解保留足够的生成概率。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于可验证奖励的强化学习（RLVR，包括PPO、GRPO等策略梯度方法）**：模型生成答案后，由结果是否正确等可验证奖励进行评价；训练利用采样序列上的梯度，提高高奖励输出的对数概率。该方法直接在动作空间，也就是逐词生成决策所形成的序列空间中强化成功轨迹，主要有利于提高单次采样表现$\mathrm{pass@}1$。
- **进化策略（ES）**：ES不依赖逐词策略梯度，而是在参数空间对模型权重施加随机扰动，形成一组候选模型，再依据任务奖励更新参数分布。它优化的是扰动模型群体上的期望奖励，因而倾向于寻找对权重变化较稳健的参数区域，而不是直接把生成概率集中到某一条高奖励输出上。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- RL为提高$\mathrm{pass@}1$而持续增加少数高奖励输出的概率，可能造成输出分布坍缩：概率质量集中于少数模式，低概率但正确的替代解被削弱。其后果是解法覆盖范围缩小，增加采样数量$k$也难以获得足够多样的候选。
- 稀疏、二元奖励只区分成功与失败，进一步集中训练信号于少量成功轨迹。原文指出，随着$k$增大，RL模型的$\mathrm{pass@}k$甚至可能低于未后训练的基础模型，说明以单次准确率为导向的后训练与发现任务所需的多次搜索目标并不一致。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究表明ES能够取得与RL相近的推理表现、对基础模型输出分布的偏移较小，也可能产生更稳健的解法分布，但尚缺少在匹配计算预算下、跨模型家族与参数规模的系统证据，来确认这种分布特性是否稳定地改善$\mathrm{pass@}k$，以及覆盖率提升是否能在下游测试时扩展中形成实际收益。

</div>
<div markdown="1"><span>核心问题</span>

在相同后训练计算预算下，与RL相比，ES是否能够跨模型家族和规模获得更高的$\mathrm{pass@}k$；如果能够，这一差异是否确实对应更宽的输出分布支持，并能改善数学任务中通过多次采样与候选选择实现的最终求解表现？

</div>
<div markdown="1"><span>作者直觉</span>

RL像是反复要求模型更加确信当前已知的少数高分答案，因此容易把分布变尖；ES则同时考察多个经过权重扰动的模型，只有位于较宽、对扰动仍能取得高奖励的参数区域才会稳定获益。作者据此推测，ES可以在提高常见正确答案概率的同时，少牺牲那些不常出现但仍有效的解法，使后续的$k$次采样拥有更大的搜索范围。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文把大语言模型后训练表述为一个直接在参数空间中搜索高奖励模型的问题。给定初始模型参数 $\theta$、可验证奖励函数 $R(\cdot)$、扰动尺度 $\sigma$ 和大小为 $N$ 的种群，每轮从标准高斯分布采样多个随机方向 $\epsilon_n$，形成参数不同的候选模型 $\theta+\sigma\epsilon_n$；各候选模型完成任务后由验证器评分，奖励经种群内归一化，再用归一化奖励加权汇总扰动方向并更新中心参数。最终输出的是经过 ES 后训练的单一中心模型，而种群主要是训练期间用于估计更新方向的临时候选集合，并非推理时必须同时部署的模型集。

与基于策略梯度的 RLVR 不同，ES 不通过输出序列的对数概率反向传播，也不直接强化某条已采样高奖励回答；它优化的是模型在一片高斯参数邻域内的期望奖励。直观地说，RLVR 更像沿着当前成功答案留下的轨迹提高其出现概率，而 ES 同时试探许多略有不同的模型版本，再根据整体任务表现决定参数中心向哪些方向移动。作者据此研究这种权重空间、群体式搜索是否能在提高正确率的同时保留更宽的输出分布和更高的 solution coverage，并以较大 $k$ 下的 $\mathrm{pass@}k$ 检验这种覆盖能力。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始化中心模型与后训练目标

将模型表现定义为可验证奖励，并设置 ES 的种群大小 $N$、参数扰动尺度 $\sigma$ 和学习率 $\alpha$。在 RLVR 的典型设定中，正确答案奖励为 $1$、错误答案奖励为 $0$，还可加入格式奖励，但节选未说明本文具体实验是否加入格式奖励。

<div class="method-step__io" markdown="1">

**输入**：初始大语言模型参数 $\theta_0$、问题数据集 $\mathcal{D}$、确定性答案验证器以及由验证结果定义的奖励函数 $R(\cdot)$。<br>
**输出**：一个可被参数空间搜索优化的中心模型，以及统一评价所有候选模型的任务奖励。

</div>

**直观理解**：先准备一份待改进的模型和一套能自动判卷的题目；后续所有模型变体都用同一把尺子评分。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造参数扰动种群

对每个种群成员 $n$ 独立采样 $\epsilon_n\sim\mathcal{N}(\mathbf{0},I)$，并构造候选参数 $\theta_{t-1}+\sigma\epsilon_n$。这些扰动直接施加在权重空间，因此不需要对语言模型的生成过程求梯度。

<div class="method-step__io" markdown="1">

**输入**：当前轮中心参数 $\theta_{t-1}$、种群大小 $N$ 和扰动尺度 $\sigma$。<br>
**输出**：由 $N$ 个参数略有差异的候选模型组成的临时种群。

</div>

**直观理解**：可以把中心模型看成当前方案，并同时制作多个经过微小随机改动的版本，以观察哪些改动方向更有利。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成回答并评价种群

让每个扰动模型完成任务，计算其奖励 $r_n=R(\theta_{t-1}+\sigma\epsilon_n)$；随后在种群内部使用排名或 z-score 将奖励变换为归一化奖励 $\hat r_n$。节选只给出这两类归一化选项，未明确本文实验最终采用哪一种。

<div class="method-step__io" markdown="1">

**输入**：候选模型种群、从 $\mathcal{D}$ 取得的问题，以及奖励函数或确定性验证器。<br>
**输出**：每个扰动方向对应的原始奖励 $r_n$ 和归一化奖励 $\hat r_n$。

</div>

**直观理解**：每个模型变体都参加同一场考试，然后按相对表现重新标定分数，避免奖励绝对尺度直接控制更新幅度。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 聚合扰动并更新中心参数

计算奖励加权的平均扰动 $\frac{1}{N}\sum_{n=1}^{N}\hat r_n\epsilon_n$，再以学习率 $\alpha$ 将其加入中心参数。重复采样、评价和聚合，近似提升高斯扰动邻域中的期望奖励。

<div class="method-step__io" markdown="1">

**输入**：全部扰动向量 $\epsilon_n$、归一化奖励 $\hat r_n$、学习率 $\alpha$ 和旧中心参数 $\theta_{t-1}$。<br>
**输出**：更新后的中心模型参数 $\theta_t$，以及训练结束时的 ES 后训练模型。

</div>

**直观理解**：表现较好的随机改动获得更大正向影响，表现较差的改动影响较小或指向相反方向；综合所有试验后，只保留一个更好的中心模型。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 高斯平滑的 ES 优化目标

$$
\max_{\theta}\;\mathbb{E}_{\epsilon\sim\mathcal{N}(\mathbf{0},I)}\left[R(\theta+\sigma\epsilon)\right]
$$

**符号说明**

- $\theta$：待优化的大语言模型中心参数。
- $\epsilon$：从均值为零、协方差为单位矩阵的高斯分布采样的随机参数扰动。
- $\mathcal{N}(\mathbf{0},I)$：标准多元高斯分布，其中 $\mathbf{0}$ 为零向量，$I$ 为单位矩阵。
- $\sigma$：扰动尺度，控制候选模型距离中心参数的远近。
- $R(\cdot)$：模型参数对应的任务奖励函数，由候选模型的任务表现及验证结果确定。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标并非只要求当前单个参数点表现好，而是要求以 $\theta$ 为中心、经过随机扰动得到的一组邻近模型平均表现好。这样可把原本离散或不可微的验证奖励转化为可通过随机试验优化的目标；同时，搜索信号来自多个权重方向的整体表现，而不是某一条生成序列的 token 级概率梯度。<br>
**原文位置**：第 2.4 节“Evolution Strategies for LLM Fine-tuning”，ES 期望奖励目标，位于公式（2）之前。

</div>

</div>

<div class="equation-block" markdown="1">

#### 奖励加权的 ES 参数更新

$$
\theta_t=\theta_{t-1}+\alpha\cdot\frac{1}{N}\sum_{n=1}^{N}\hat{r}_n\epsilon_n
$$

**符号说明**

- $\theta_t$：第 $t$ 轮更新后的中心模型参数。
- $\theta_{t-1}$：第 $t$ 轮更新前的中心模型参数。
- $\alpha$：学习率，控制每轮中心参数移动的幅度。
- $N$：每轮评估的种群成员数量。
- $\hat{r}_n$：第 $n$ 个候选模型在种群内经排名或 z-score 处理后的归一化奖励。
- $\epsilon_n$：生成第 $n$ 个候选模型的随机权重扰动方向。
- $n$：种群成员索引，取值从 $1$ 到 $N$。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把每个随机方向看作一项建议，并用该方向对应候选模型的相对成绩决定建议权重。高奖励方向更强地拉动中心参数，低奖励方向则贡献较弱或相反的作用；对 $N$ 个方向求平均能够得到无需反向传播的随机梯度估计。<br>
**原文位置**：第 2.4 节，公式（2）。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标是最大化模型参数在尺度为 $\sigma$ 的高斯扰动下的期望可验证奖励，而不是直接最大化某条输出序列的对数概率。每轮先用 $r_n=R(\theta+\sigma\epsilon_n)$ 评价各候选模型，再将奖励归一化为 $\hat r_n$，最后按公式（2）得到对该平滑目标上升方向的零阶估计。与 RLVR 的 $J(\theta)=\mathbb{E}_{x\sim\mathcal{D},y\sim\pi_\theta(\cdot\mid x)}[R(y)]$ 相比，二者都追求高奖励，但 RLVR 使用采样序列的对数概率计算策略梯度，ES 则比较随机权重扰动后的整模型表现。作者的核心方法假设是：后者较少直接把概率质量集中到少数已见高奖励轨迹上，因此可能更好地保留正确解覆盖；这是方法动机和待实验检验的机制解释，不应仅凭本节视为已经证明的因果结论。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 权重空间进化搜索**

ES 围绕中心参数 $\theta$ 对各向同性高斯扰动进行采样，目标是提高 $\mathbb{E}_{\epsilon}[R(\theta+\sigma\epsilon)]$。它属于零阶优化：更新只依赖候选参数及其函数值，不需要计算 $\nabla_\theta R$，也不需要沿 token 生成轨迹反向传播。

> 直观理解：这个模块解决“怎样改模型”的问题：通过实际测试许多微小权重改动来估计有利方向，因此即使验证器只有对错结果，也能形成更新信号。

**2. 可验证奖励与种群归一化**

确定性验证器把候选模型的任务表现转换为奖励 $r_n$；排名或 z-score 再把同一轮种群奖励转换为 $\hat r_n$。归一化使更新主要反映候选成员之间的相对优劣，而不是未经控制的奖励数值尺度。

> 直观理解：验证器负责判卷，归一化负责把不同候选模型的成绩变成可比较的投票权重；两者共同决定哪些随机改动值得吸收到中心模型中。

**3. 基于 $\mathrm{pass@}k$ 的解覆盖评估**

$\mathrm{pass@}1$ 只检查一次采样能否答对，而 $\mathrm{pass@}k$ 检查 $k$ 次采样中是否至少存在一个正确答案。论文将后者用于刻画模型输出分布是否仍覆盖低概率但正确的解，并比较 ES 与 RL 后训练模型在测试时计算增加后的收益。

> 直观理解：一次答对率偏向衡量模型最常给出的答案，多次尝试成功率则能发现模型是否还保留其他可行思路；因此它更直接对应发现型任务中的探索能力。

**训练与推理**

训练阶段从预训练或已有后训练检查点的参数 $\theta_0$ 出发。对每轮 $t$，采样 $N$ 个独立高斯扰动，按 $\theta_{t-1}+\sigma\epsilon_n$ 构造候选模型；候选模型在从 $\mathcal{D}$ 取得的问题上生成回答，由确定性验证器计算任务奖励；同轮奖励经排名或 z-score 归一化后，使用奖励加权平均扰动更新中心参数。上述过程迭代至既定训练终点，输出中心参数对应的模型。由于更新仅依赖前向生成和奖励，不需要保存反向传播所需的梯度状态，且不同种群成员可以并行评价。

推理与评估阶段使用训练后的中心模型，而非重新执行 ES。对于单次性能，从模型采样一个回答并计算 $\mathrm{pass@}1$；对于测试时扩展，从同一问题采样 $k>1$ 个候选回答，只要至少一个通过验证器即记为 $\mathrm{pass@}k$ 成功。这里增加的是推理采样数量，而不是再次更新权重。节选称论文还在不可验证场景中使用跨答案投票来检验覆盖提升的下游价值，但相关章节未包含在所给材料中，因此无法可靠复述投票规则、选择器或最终输出聚合过程。

**复现信息**

公平解释该方法至少需要区分三个量：$N$ 是训练时每轮用于估计更新方向的种群规模，$\sigma$ 决定参数空间的探索半径，$k$ 是推理时每题的采样数量；三者作用不同，不能把较大的训练种群直接等同于较大的测试时计算预算。节选明确给出的算法选择包括高斯权重扰动、基于排名或 z-score 的奖励归一化，以及学习率为 $\alpha$ 的加权平均更新。文中提到既有 LLM ES 工作曾以种群规模 $30$ 获得竞争性表现，但这是对先前工作的说明，不能据此认定本文也使用 $N=30$。

所给节选没有明确报告本文采用的基础模型、实际 $N$、$\sigma$、$\alpha$、训练轮数、每个候选模型处理的问题数、采样温度、最大生成长度、奖励归一化方式、是否使用对偶扰动、参数是否全量更新、硬件配置或训练成本。因此这些值不应推断或补写；复现实验还必须查阅论文的方法后续章节、实验设置或附录。并行性和无需反向传播是算法结构带来的性质，但节选没有给出相对于 RL 的实测显存、时间或计算量优势。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：小学水平的多步数学文字题数据集。实验使用其训练数据分别微调 Qwen2.5 1.5B/3B/7B-Instruct 与 Qwen3 1.7B/4B/8B，并在 GSM8K 测试集上评估。其作用是观察 ES 与 RL 在相对容易、且训练和测试来自同一数据集的条件下如何影响解答覆盖率；原文节选未报告训练集、测试集的具体样本数。
- MATH（level 3–5）与 MATH500：前者选取较高难度题目作为训练数据，后者作为对应的标准评测集。实验用 MATH 微调 Qwen2.5-Math-7B、Qwen2.5-14B 和 Qwen2.5-32B，再在 MATH500 上比较 ES 与公开 RL 检查点，从而检验规模扩大后对较难数学推理题的效果；原文节选未明确报告实际训练规模及 MATH500 的样本划分细节。
- Olympiad Bench 与 Minerva：均用于评估在 MATH 上训练的模型，而非作为本文所述的训练集。它们用于测试模型获得的解答覆盖能力能否迁移到竞赛型或其他来源的数学问题；原文节选未报告所用子集、样本数及具体题型构成。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**$\mathrm{pass}@k$**

对每道题生成 $n$ 个回答，其中 $c$ 个正确；从这些回答中抽取 $k$ 个时至少包含一个正确回答的无偏、低方差估计为 $\mathbb{E}_{x\sim\mathcal{D}}\left[1-\frac{\binom{n-c}{k}}{\binom{n}{k}}\right]$。这里 $x$ 是数据集 $\mathcal{D}$ 中的问题，$n$ 是每题总采样数，$c$ 是正确回答数，$k$ 是允许使用的候选回答数。它衡量增加测试时采样预算后，模型能覆盖多少可解问题。 （越高越好，因为这表示在 $k$ 次候选采样中至少找到一个正确解的概率更高。需要注意，较大 $k$ 下的提升反映候选解覆盖范围，并不等同于单次输出更可靠。）

</div>
<div class="metric-item" markdown="1">

**$\mathrm{pass}@1$**

$\mathrm{pass}@k$ 在 $k=1$ 时退化为标准单次采样准确率，主要衡量模型只给出一个回答时的正确性。 （越高越好，因为单个采样回答正确的概率更高；但它不能充分反映模型输出分布中是否还存在其他可行解。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给材料止于实验设置，缺少结果章节、表格与图，因此无法按要求给出三个带完整证据句和来源位置的核心数值结果，也无法判断提升幅度、方差及统计显著性；相应的主结果与消融列表只能留空。
- 节选未说明 ES 与 RL 是否匹配训练 token 数、奖励评估次数、硬件时间或总计算预算，也未提供专门消融来分离参数空间扰动、种群规模等 ES 设计因素。因而即使完整论文报告 ES 更高的 $\mathrm{pass}@k$，仍需核查差异究竟来自优化方法，还是计算预算与训练配置不一致。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- VERL 强化学习微调：与 ES 在 GSM8K 实验中的主要训练方法基线。该比较有意义，因为两者都用于模型后训练，但 RL 直接依据奖励更新策略，而 ES 通过参数扰动在权重空间进行无梯度优化；实验意在检验 RL 是否更容易使输出分布集中。
- SimpleRL-Zoo 公开 RL 检查点：用于 MATH 训练和较大模型实验的公开先进 RL 基线，使 ES 可与已有可复现的 RL 成果比较。节选没有说明每个检查点的具体算法、训练预算或与 ES 的计算量是否严格匹配。
- OatZero 公开 RL 检查点：另一组用于大规模数学推理比较的公开 RL 基线，作用是避免结论仅依赖某一个 RL 实现。节选未给出其具体模型配置、奖励设计和训练计算量。
- 不同基础模型与参数规模：Qwen2.5、Qwen3 及 Qwen2.5-Math 系列并非独立训练算法基线，但构成跨模型家族和从 1.5B 到 32B 参数的对照条件，用于判断 ES 与 RL 的差异是否只出现在某一模型或规模上。

**实验想回答的问题**

- 在相同数学推理任务上，采用进化策略（ES）进行模型后训练，是否比强化学习（RL）保留更广的正确解覆盖范围，即在不同采样预算 $k$ 下取得更高的 $\mathrm{pass}@k$？
- ES 与 RL 在模型规模、模型家族以及题目难度变化时是否呈现一致差异；这种覆盖能力能否从训练分布内的 GSM8K 扩展到 MATH500、Olympiad Bench 和 Minerva 等更困难或分布不同的评测集？

**实验实现**

ES 使用 ES-at-Scale 库，RL 使用 VERL 库；大规模比较还采用 SimpleRL-Zoo 与 OatZero 的公开 RL 检查点。GSM8K 实验覆盖 Qwen2.5 1.5B/3B/7B-Instruct 和 Qwen3 1.7B/4B/8B，MATH 实验覆盖 Qwen2.5-Math-7B、Qwen2.5-14B 与 Qwen2.5-32B。测试时每个回答最多生成 16,384 个 token，并以温度 $0.6$、top-p $0.95$ 采样；各基准的每题总采样数 $n$ 沿用参考文献 54，但节选未给出具体数值。技术上，评估先为每题采样 $n$ 个回答并统计正确数 $c$，再用组合数估计从中取 $k$ 个回答时至少出现一个正确解的概率。通俗地说，它不是只检查模型的“最佳猜测”，而是检查多给模型若干次尝试后，是否能探索到正确解。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces evolution strategies as an LLM post-training alternative to RL for preserving diverse solution coverage during test-time reasoning.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`85c2c77641654975b4c2bb9a277235a7d8c36e010dc679d0241ad65567dfccb7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
