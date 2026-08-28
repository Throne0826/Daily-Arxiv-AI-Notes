---
title: "[论文解读] Understanding Evolution Strategies for LLM Reasoning: Broader Reasoning Coverage than GRPO"
description: "[arXiv 2608.27351][对齐 / RLHF] 本文旨在厘清演化策略（ES）相较于主流群组相对策略优化（GRPO）的真正优势边界：ES是否能在提升单次作答成功率的同时保留更广的推理路径覆盖，以及其参数漂移、遗忘风险与可扩展训练条件应如何理解。"
arxiv_id: "2608.27351"
announcement_date: "2026-08-28"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:33:41.335458+00:00"
source_sha256: "8aa172809d7252f813436ab986e754be380aff1da6def8643fdf42618a1e740d"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "大语言模型推理"
  - "进化策略"
  - "组相对策略优化"
  - "推理覆盖"
  - "Pass@K"
  - "熵坍缩"
  - "灾难性遗忘"
  - "零阶优化"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.27351</p>

# Understanding Evolution Strategies for LLM Reasoning: Broader Reasoning Coverage than GRPO

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Yunpeng Ba, Zhi Zheng, Yue Xie, Jiaqing Li, Xialiang Tong, Tao Zhong, Mingxuan Yuan, Zhichao Lu, Xuyang Wu, Zhenkun Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Southern University of Science and Technology；Affiliation: National University of Singapore；Affiliation: Harbin Institute of Technology, Weihai；Affiliation: Huawei Noah’s Ark Lab；Affiliation: City University of Hong Kong</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27351v1) · [PDF 下载](https://arxiv.org/pdf/2608.27351v1) · **关键词** 大语言模型推理, 进化策略, 组相对策略优化, 推理覆盖, Pass@K, 熵坍缩, 灾难性遗忘, 零阶优化<br>
**代码**: [https://github.com/yunpengba7/understanding-es](https://github.com/yunpengba7/understanding-es)

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

本文旨在厘清演化策略（ES）相较于主流群组相对策略优化（GRPO）的真正优势边界：ES是否能在提升单次作答成功率的同时保留更广的推理路径覆盖，以及其参数漂移、遗忘风险与可扩展训练条件应如何理解。

**不用术语来说**：训练大语言模型做推理时，不能只让它更容易给出一种标准答案，还希望它保留多条可能成功的解题路线，以便重复采样时找到较少见但正确的答案。GRPO通常能提高第一次作答正确的概率，却可能使模型越来越集中于少数路线；ES不依赖反向传播且更节省显存，但此前尚不清楚它究竟只是较便宜的替代方案，还是具有不同的探索优势，也不清楚其较大的参数变化是否会破坏模型原有能力。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将“推理覆盖范围”确立为比较ES与GRPO的关键维度，并从理论与经验两方面提出：ES通过多个参数扰动策略进行群体搜索，可维持更高的验证器投影Jensen–Shannon多样性，从而改善重复采样成功率和较大$K$下的Pass@$K$；这一视角把ES定位为具有独特探索特性的后训练范式，而非低效但省显存的GRPO替代品。
- 作者进一步挑战“整体参数漂移必然导致灾难性遗忘”的既有解释，提出ES的任务收益主要由少量幅度较大的更新贡献，并将其概括为功能稀疏性；同时把能力保留问题与训练集过拟合、奖励归一化、估计器及群体规模等训练条件联系起来，为判断ES何时有效且可扩展提供研究框架。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型（LLM）的推理后训练，即在预训练模型基础上利用可自动验证的奖励进一步提升数学等任务的解题能力。核心比较对象是进化策略（Evolution Strategies, ES）与组相对策略优化（Group Relative Policy Optimization, GRPO）：ES在参数空间中生成一组受扰动模型，仅通过前向推理获得奖励并聚合扰动方向，因而无需反向传播、显存需求较低且易于并行；GRPO则从同一策略采样多条回答，根据组内相对奖励构造逐词元目标并反向传播。论文关注的不只是单次回答的正确率，还关注重复采样时能否覆盖多种潜在正确推理路径，以及后训练是否损害预训练模型已有的其他能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**进化策略（ES）**

一种零阶优化方法：对模型参数施加随机扰动，分别评估多个扰动模型的奖励，再用奖励加权扰动来估计参数更新方向。它不需要对奖励或模型执行反向传播，但优化质量取决于种群规模、奖励归一化和梯度估计器等设计。

</div>
<div class="concept-item" markdown="1">

**组相对策略优化（GRPO）**

一种用于LLM后训练的强化学习方法：从单个策略对同一问题采样多条回答，以组内奖励的相对高低估计优势，并通过逐词元目标更新模型。它能有效提高单次采样表现，但可能发生熵坍缩，使输出概率集中到较少的推理模式。

</div>
<div class="concept-item" markdown="1">

**推理覆盖与Pass@K**

推理覆盖表示模型能够以非忽略概率生成多少种有效解题路径；$\mathrm{Pass@}K$衡量对同一问题采样$K$次时至少出现一次正确答案的成功率。较高的$\mathrm{Pass@}K$不仅取决于最常见答案是否正确，也取决于低概率正确路径是否仍可被采到。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个预训练LLM、带有可验证答案的推理训练问题，以及将生成回答映射为离散奖励的验证器，研究分别使用ES与GRPO进行后训练后，模型的推理性能、输出分布和能力保持情况。ES的输入是当前参数及随机参数扰动组成的模型种群，经前向生成和验证器评分后估计更新方向；GRPO的输入是单一当前策略，经组内多回答采样、相对优势计算和反向传播后更新参数。主要输出是后训练策略，并从三个方面评价：单次采样正确性$\mathrm{Pass@}1$与重复采样成功率$\mathrm{Pass@}K$所反映的推理覆盖；参数漂移是否对应真实的功能变化及灾难性遗忘；奖励归一化、估计器和种群规模等设置能否使ES稳定扩展到更大的模型。论文的关键比较前提是两类方法都利用采样回答的验证器奖励，但探索空间不同：ES搜索参数扰动产生的多个策略，GRPO主要在一个策略的回答空间内采样。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$K$**

对同一问题进行独立回答采样的次数。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{Pass@}K$**

在$K$次采样中至少得到一次正确答案的问题比例或成功概率；$K=1$时即单次采样表现。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{Maj@}32$**

对同一问题采样32次后，以多数答案决定最终预测的评估指标；原文图1将其用于概括留出任务上的能力变化。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{JSD}$**

Jensen–Shannon散度；本文语境中用于刻画ES种群经过验证器投影后的预测或成功模式多样性。

</div>

</div>

**直接相关的工作**

- **Salimans et al. (2017)**: 提供本文采用的进化策略基础范式，即通过参数扰动、前向奖励评估和奖励加权聚合来估计更新方向；本文将该范式置于LLM推理后训练场景中分析。
- **Shao et al. (2024)**: 提出本文的主要对照方法GRPO。论文以其基于单策略采样和相对优势反向传播的机制为参照，考察ES是否具有不同的推理覆盖、能力保持及扩展特性。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

LLM推理后训练需要同时兼顾三个实际目标：提高常见采样下的正确率、保留多样且低概率的正确推理路径，以及避免在目标任务训练后损害预训练阶段获得的其他能力。ES通过仅执行前向计算来评估参数扰动，具有显存效率和并行化优势，但若其探索行为、遗忘风险及模型规模变化下的训练条件不明确，就难以判断它是否适合替代或补充现有强化学习后训练。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **群组相对策略优化（GRPO）**：GRPO从同一个策略模型采样多条回答，根据组内回答的相对奖励构造优势信号，再通过反向传播优化词元级目标。它直接把概率质量推向奖励较高的回答，因此通常擅长提高Pass@1，即单次采样得到正确答案的概率。
- **演化策略（ES）**：ES在参数空间中生成一组受扰动的模型，分别用前向推理取得验证器奖励，再将扰动方向按奖励加权聚合成更新方向。它不需要对生成过程反向传播，并通过多个参数扰动策略形成群体式搜索，理论上可探索同一预训练模型中不同的推理模式。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- GRPO可能发生熵坍缩，即输出分布逐渐集中于少数高概率回答。其后果是Pass@1虽然上升，但推理路径多样性可能下降，较大$K$下的Pass@$K$甚至低于基础模型，使低概率但正确的解法更难通过重复采样被发现。
- 既有ES研究主要强调显存效率，尚未系统解释其优化动态；部分工作又把灾难性遗忘归因于显著的整体参数漂移，但相关证据局限于特定任务和小规模训练集，未验证参数移动是否真正对应广泛的功能变化，也未充分确定奖励归一化、梯度估计方式和群体规模如何随模型规模调整。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一个能够同时连接ES的参数空间群体探索、输出层面的推理覆盖、任务外能力保留和训练可扩展性的系统解释。特别是，尚无充分答案说明ES是否比GRPO更能保留多种可验证的正确推理模式、较大的参数漂移是否具有实际功能后果，以及哪些设计条件使这种优势稳定出现。

</div>
<div markdown="1"><span>核心问题</span>

论文集中回答三个相互关联的问题：ES是否呈现不同于GRPO的后训练特征并获得更广的Pass@$K$推理覆盖；ES是否必然造成灾难性遗忘；以及奖励归一化、扰动估计器和群体规模应如何配置，才能使ES在更大LLM上保持有效和稳定。

</div>
<div markdown="1"><span>作者直觉</span>

GRPO始终围绕单个策略分布强化当前较成功的回答，容易把概率进一步集中到已经占优的少数路径；ES则同时考察多个参数扰动后的策略，相当于从若干稍有不同的“解题者”中汇总有益方向，因此更可能接触到基础模型中原本存在但概率较低的正确路线。另一方面，参数数值发生变化不等于模型所有功能都发生变化：若正负扰动大多相互抵消，而任务收益只依赖少量大幅更新，那么整体漂移可以很大，真正影响行为的更新却仍然稀疏，因而未必自动导致灾难性遗忘。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文把进化策略（Evolution Strategies, ES）用于大语言模型推理后训练：从中心策略 $\pi_\theta$ 出发，对参数加入高斯扰动 $\sigma\epsilon_i$，得到由 $N$ 个成员组成的策略群体；各成员生成回答并由正确性验证器评价，再依据适应度形成权重并更新中心参数。作者关注的不只是单次回答正确率，而是群体中的不同成员能否覆盖互补的推理路径，以及这种覆盖能否被迁移到更新后的中心策略 $\pi_{\theta^+}$。理论链条依次说明：参数扰动产生策略分布差异；成功率有差异的多个策略比同平均成功率的单一策略更容易在多次采样中找到至少一个正确答案；若适应度权重与真实成功率正相关，奖励加权会偏向更可靠的成员；若中心更新充分逼近该加权混合策略，则更新后模型的 Pass@$K$ 可高于初始模型。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造扰动策略群体

独立采样 $\epsilon_i\sim\mathcal N(0,I)$，构造参数为 $\theta+\sigma\epsilon_i$ 的成员策略 $\pi_i(\cdot\mid x)$。局部分析用提示条件 Fisher 信息 $\mathcal I_x(\theta)$ 衡量参数扰动在输出分布上造成的实际位移。

<div class="method-step__io" markdown="1">

**输入**：中心模型参数 $\theta$、扰动尺度 $\sigma$、群体规模 $N$ 与训练提示 $x$。<br>
**输出**：包含 $N$ 个具有不同回答分布和潜在成功率 $p_i(x)$ 的策略群体。

</div>

**直观理解**：这相当于在同一个模型附近生成多名略有差异的“解题者”。参数变化本身不是目的，关键是这些解题者是否会探索不同且有用的答案路径。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成回答并由验证器评估

各成员从自身策略中生成回答 $y$，验证器判断回答是否属于正确集合 $\mathcal C(x)$，并据此获得实现的适应度 $R_i$。理论上将成员在提示 $x$ 上输出正确答案的概率记为 $p_i(x)$。

<div class="method-step__io" markdown="1">

**输入**：扰动策略群体、训练提示以及二值正确性验证器 $v(x,y)\in\{0,1\}$。<br>
**输出**：每个群体成员的回答、正确性结果、适应度以及由此体现的群体异质性。

</div>

**直观理解**：验证器只负责判定答案对错，而不要求给出可微分的训练信号。因此，ES 可以根据整段推理最终是否成功来筛选参数扰动。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 奖励加权与中心策略更新

权重满足 $w_i\geq0$ 且 $\sum_iw_i=1$；理论分析先构造奖励加权混合策略 $\pi_w=\sum_iw_i\pi_i$，实践中则通过 ES 更新把中心参数移动到更受高适应度成员支持的方向。所给章节未列出实际 ES 参数更新估计量、适应度标准化方式或学习率公式，因而不能从节选中进一步复原。

<div class="method-step__io" markdown="1">

**输入**：各成员扰动 $\epsilon_i$、适应度 $R_i$ 及其单调变换得到的归一化权重 $w_i$。<br>
**输出**：更新后的中心参数 $\theta^+$ 及中心策略 $\pi_{\theta^+}$。

</div>

**直观理解**：可以把它理解为让表现较好的扰动拥有更大的“投票权”，再把群体经验压回一个可独立部署的中心模型。理论中的混合策略是分析桥梁，并不等同于实践中的中心更新。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 单独或顺序组合 ES 与 GRPO

除纯 ES 和纯 GRPO 外，作者把总预算平均分成两个阶段，比较 $\mathrm{ES}\rightarrow\mathrm{GRPO}$ 与 $\mathrm{GRPO}\rightarrow\mathrm{ES}$。前者先扩大推理覆盖再强化单样本表现，后者先提升 Pass@$1$ 再尝试恢复或扩展大采样预算下的覆盖。

<div class="method-step__io" markdown="1">

**输入**：固定的总更新预算、基础模型以及选定的 ES/GRPO 训练次序。<br>
**输出**：纯 ES、纯 GRPO 和两种顺序组合的最终中心模型，用于比较 Pass@$1$—Pass@$K$ 的 Pareto 权衡。

</div>

**直观理解**：GRPO 更像集中训练最常成功的一条路线，ES 更像保留多种可能路线。顺序训练试图在相同计算更新预算下兼得单次作答能力和多次尝试时的覆盖能力。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 扰动诱导的局部策略多样性

$$
\mathbb{E}_{\epsilon_{1:N}}\!\left[\operatorname{JS}^{\mathrm{pol}}_{N}(x)\right]=\frac{\sigma^{2}}{2}\!\left(1-\frac{1}{N}\right)\operatorname{tr}\mathcal{I}_{x}(\theta)+O(\sigma^{4})
$$

**符号说明**

- $\epsilon_{1:N}$：群体中从标准高斯分布独立采样的全部参数扰动。
- $\operatorname{JS}^{\mathrm{pol}}_{N}(x)$：给定提示时，各成员策略到群体平均策略的平均 KL 散度，用于衡量群体策略多样性。
- $\sigma$：参数扰动尺度；越大表示成员离中心参数通常越远。
- $N$：ES 群体规模。
- $\mathcal I_x(\theta)$：中心策略在提示条件下的 Fisher 信息矩阵，反映参数变化对输出分布的局部敏感性。
- $\operatorname{tr}\mathcal I_x(\theta)$：Fisher 信息矩阵的迹，汇总各局部参数方向对策略分布的敏感程度。
- $O(\sigma^4)$：当扰动很小时四阶及更高阶的近似误差项。

<div class="equation-explanation" markdown="1">

**直观理解**：在小扰动区域内，预期策略多样性近似按 $\sigma^2$ 增长，并随群体规模因子 $1-1/N$ 增大；模型对参数越敏感，扰动越容易产生不同回答分布。这一式只证明扰动能够带来策略差异，并不单独保证差异会提高正确率。<br>
**原文位置**：第 3.1 节，Lemma 1，式 (9)；Fisher 信息定义见式 (8)

</div>

</div>

<div class="equation-block" markdown="1">

#### ES 中心实现 Pass@K 改进的充分条件

$$
J_K(\pi_{\theta^{+}})\geq J_K(\pi_w)-K\sqrt{\varepsilon_{\mathrm{succ}}/2}>J_K(\pi_\theta),\quad J_K(\pi)=\mathbb E_{x\sim\mathcal D}\left[1-\left(1-p_\pi(x)\right)^K\right]
$$

**符号说明**

- $J_K(\pi)$：策略在提示分布上的期望 Pass@K，即独立生成 K 次时至少一次正确的概率。
- $\pi_\theta$：ES 更新前的中心策略。
- $\pi_{\theta^+}$：ES 更新后的中心策略。
- $\pi_w$：按适应度权重形成的理论策略混合，是分析比较器而非实际 ES 更新本身。
- $p_\pi(x)$：策略在提示 x 上单次生成正确回答的概率。
- $\mathcal D$：评估提示的分布。
- $K$：每道题独立生成回答的采样预算。
- $\varepsilon_{\mathrm{succ}}$：加权混合策略与更新后中心策略在正确/错误结果分布上的平均 KL 迁移误差上界。

<div class="equation-explanation" markdown="1">

**直观理解**：加权群体先要比初始策略形成足够大的 Pass@$K$ 优势，随后中心模型对该群体的功能性逼近误差不能吞掉这一优势。误差惩罚随 $K$ 线性放大，因此该结论是充分条件而非无条件保证，也没有声称任何扰动或奖励设计都必然提升 Pass@$K$。<br>
**原文位置**：第 3.1 节，Proposition 1，式 (12)–(14)；$J_K$ 与裕量 $m_K$ 的定义位于命题正文

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：ES 的优化信号来自各扰动成员在验证器奖励上的实现适应度，而不是对语言模型损失直接反向传播。适应度经单调变换产生权重后，中心参数朝高权重扰动所支持的方向更新；理论上，若 $\operatorname{Cov}_i(w_i,p_i(x))>0$，则奖励加权混合的成功率高于均匀群体平均。需要严格区分：$\pi_w$ 只是用于证明的混合策略，不是实际部署对象，也不等同于中心策略；中心模型能否获益还取决于成功结果上的迁移误差 $\varepsilon_{\mathrm{succ}}$。原文节选没有给出实际 ES 梯度估计公式或 GRPO 的具体目标函数，因此不能据此声称采用了某种特定的基线、优势标准化或裁剪形式。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 高斯参数扰动与策略多样性**

成员参数写为 $\theta+\sigma\epsilon_i$，其中 $\epsilon_i$ 独立服从标准高斯分布。作者用群体策略相对于平均策略 $\bar\pi_N$ 的 Jensen–Shannon 型散度 $\operatorname{JS}^{\mathrm{pol}}_N(x)$ 描述输出分布差异，并用 $\mathcal I_x(\theta)$ 连接参数空间扰动与策略空间位移。

> 直观理解：只有参数不同并不能保证功能不同；Fisher 信息刻画某个参数方向的变化是否真的会改变模型回答，而策略散度直接检查群体是否形成了不同的输出分布。

**2. 验证器投影的成功覆盖**

验证器把复杂的回答分布投影为“正确/错误”Bernoulli 结果，成员成功率为 $p_i(x)$。由数据处理不等式，成功结果上的差异不超过完整策略分布的差异；当各成员成功率不完全相同时，每个成员采样一次的群体成功概率至少不低于从同平均成功率的单一策略采样 $N$ 次。

> 直观理解：模型可能用不同表述生成许多实际上等价的答案，因此仅看文本差异会高估有用多样性。投影到正确与否后，保留下来的才是与 Pass@$K$ 直接相关的“功能性多样性”。

**3. 奖励加权与中心迁移条件**

若权重 $w_i$ 与成员成功率 $p_i(x)$ 正相关，则加权混合策略的成功率 $p_w(x)$ 高于均匀群体平均；进一步要求更新后的中心策略在验证器结果分布上接近 $\pi_w$，且加权混合相对初始策略的 Pass@$K$ 优势足以覆盖迁移误差。

> 直观理解：群体多样性只说明有人可能找到新解，并不会自动改进最终模型。还必须让评分机制识别这些成员，并确保中心更新没有在压缩群体经验时丢掉其覆盖优势。

**训练与推理**

训练时，Easy Setting 从 Qwen2.5-1.5B-Instruct、Llama-3.2-3B-Instruct 或 Qwen2.5-7B-Instruct 出发，在 GSM8K 上训练两个 epoch；Hard Setting从 DeepSeek-R1-Distill-Qwen-1.5B 出发，在 DeepScaleR 上训练一个 epoch。每轮 ES 训练围绕中心模型采样参数扰动、生成并验证回答、计算成员适应度，再更新中心参数；纯 GRPO 作为主流策略优化对照。顺序组合保持总更新预算不变，并将预算等分给两个阶段，分别执行 $\mathrm{ES}\rightarrow\mathrm{GRPO}$ 与 $\mathrm{GRPO}\rightarrow\mathrm{ES}$。

推理或评估时只使用最终中心模型，而不是同时部署整个 ES 群体。对每个提示独立采样：Pass@$1$ 测试单次回答正确性，Pass@$K$ 测试 $K$ 次回答中是否至少一次正确，Maj@$K$ 则对规范化后的答案进行多数投票；因此 Pass@$K$ 主要检验推理覆盖，Maj@$K$ 更强调多个样本能否稳定集中到正确答案。作者还在训练任务之外评估 GPQA、MATH-500、AIME24、AIME25、AMC23、CSQA、HotpotQA、Countdown 和 MBPP 等任务，以区分训练任务收益、跨任务覆盖以及潜在遗忘。

**复现信息**

公平解释结果所需的关键设置有三点。第一，Easy Setting 的三种模型均进行两个 epoch 的 GSM8K 后训练，Hard Setting 对 DeepSeek-R1-Distill-Qwen-1.5B 进行一个 epoch 的 DeepScaleR 后训练；不同设置之间不应直接把绝对分数视为同难度比较。第二，两种顺序方法与单一方法使用相同总更新预算，并在两个阶段间等分预算，因此新增 Pareto 点不是简单增加训练步数所得。第三，Pass@$16$、Pass@$32$ 依赖独立重复采样，Maj@$K$ 在答案规范化后多数投票；表中 Pass 和 Maj 数值均按 $\times100$ 报告。节选未明确提供扰动尺度 $\sigma$、群体规模 $N$、每个成员的训练采样数、学习率、适应度变换、随机种子与解码参数，完整复现仍需核对论文其他章节或代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：小学数学文字题数据集。表11在Easy Setting中用它评估Qwen2.5-1.5B-Instruct、Llama-3.2-3B-Instruct和Qwen2.5-7B-Instruct；所给节选未明确报告评估划分与样本规模。
- MATH-500：由500道数学题组成的评测集。表12在Hard Setting中用它评估DeepSeek-R1-Distill-Qwen-1.5B；所给节选未明确报告具体划分方式。
- 附录B还列出CSQA、HotpotQA、Countdown、GPQA和MBPP，并说明这些任务用于补充Maj@16与Maj@32结果；但所给节选没有提供对应分数，因此不足以据此分析ES与GRPO的主要比较结论。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Pass@1**

每道题仅保留一次作答机会时的经验正确率；本附录由每题32个保留回答估计单样本准确率，主要衡量模型一次采样直接答对的能力。 （越高越好，因为它表示随机抽取一次回答时正确的概率更大。）

</div>
<div class="metric-item" markdown="1">

**Update sparsity**

在原本非零的ES参数变化中，被幅度阈值规则清零的坐标比例；原本变化为零的坐标既不进入分母，也不属于消融集合。 （它本身不是单调的优劣指标；在Pass@1基本不变时，稀疏度越高，越能说明较多小幅更新对目标任务性能并非必要。）

</div>
<div class="metric-item" markdown="1">

**$\Delta$ Full ES**

阈值化模型的Pass@1相对同一模型未经消融的Full ES终点之有符号绝对差，单位为百分点。 （越接近零表示越能保留Full ES性能；正值表示阈值化后反而提高，负值表示性能损失。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四个模型在约78%更新稀疏度附近的跨模型汇总

<div class="result-value" markdown="1">

在删除约62%至79%的非零ES更新坐标后，四个模型相对Full ES的Pass@1变化依次为$-0.351$、$-0.130$、$+0.488$和$+0.169$个百分点，绝对变化均不超过$0.488$个百分点。作者据此主张，ES的任务收益主要由较少的大幅更新贡献，而大量小幅参数漂移在这些目标任务上可被移除。

</div>

直观上，模型虽然在许多参数上发生了变化，但把大部分幅度较小的变化撤销后，答题正确率几乎不变。这支持“功能稀疏性”：参数发生变化不等于每个变化都对任务有可见作用。不过，这只是基于幅度阈值和目标任务性能的证据，不能证明被删除坐标对所有能力、所有输入或组合效应都完全无用。

<div class="result-source" markdown="1">

来源：Appendix D，表11—12之后的汇总段落

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At comparable sparsity near 78%, all four endpoints remain close to Full ES: the Pass@1 changes are −0.351, −0.130, +0.488, and +0.169 percentage points for Qwen2.5-1.5B-Instruct, Llama-3.2-3B-Instruct, Qwen2.5-7B-Instruct, and DeepSeek-R1-Distill-Qwen-1.5B, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### GSM8K Easy Setting中的Qwen2.5-7B-Instruct，高阈值参数消融

<div class="result-value" markdown="1">

当$\tau=2.0\times10^{-3}$时，98.11%的非零ES更新被清零，Pass@1仍由Full ES的91.016%升至91.824%，即提高$0.808$个百分点；其结果也接近Base Model的91.774%。

</div>

该模型在测试范围内没有因删除小幅更新而退化，反而略有改善，说明小幅更新可能包含目标任务上的无益扰动。但阈值化结果与Base Model非常接近，也表明该设置下Full ES相对基础模型的净收益本来就较小；单个表格结果不能证明阈值化普遍具有正则化作用，且没有统计不确定性来判断$0.808$个百分点是否稳定。

<div class="result-source" markdown="1">

来源：Appendix D，Table 11，Qwen2.5-7B-Instruct

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

2.0 × 10−3 | 98.11 | 91.824 | +0.808

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### MATH-500 Hard Setting中的DeepSeek-R1-Distill-Qwen-1.5B，高稀疏度参数消融

<div class="result-value" markdown="1">

Full ES的Pass@1为82.844%，Base Model为80.856%；即使在$\tau=2.5\times10^{-3}$、更新稀疏度93.16%时，Pass@1仍为82.213%，仅比Full ES低$0.631$个百分点，并明显高于Base Model。

</div>

这说明在较难数学设置中，只保留不到7%的原非零更新坐标，仍可保存大部分ES训练收益，为“大幅更新承担主要功能”提供了较强例证。不过，继续把稀疏度提高到96.64%时性能下降更明显，因此实验并不支持任意压缩；它显示的是存在一个较宽的可删除区间，而不是更新越稀疏越好。

<div class="result-source" markdown="1">

来源：Appendix D，Table 12，DeepSeek-R1-Distill-Qwen-1.5B

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

2.5 × 10−3 | 93.16 | 82.213 | −0.631

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

- Full ES：未经阈值化处理的完整ES训练终点，是判断删除参数更新是否损害ES所得能力的直接参照。
- Base Model：ES训练前的基础模型。它用于判断阈值化模型是否仍保留训练收益，以及高稀疏度下是否已基本退化回训练前状态。
- Magnitude-thresholded ES：将满足$0<|\Delta\theta_i|\leq\tau$的更新坐标清零，即把相应参数恢复为Base Model值。改变阈值$\tau$可以直接检验小幅更新是否具有任务功能。
- GRPO：论文摘要将其设为主流推理后训练对照，用来比较Pass@1、Pass@K与熵坍缩；但本节选没有给出GRPO实验表或数值，因而不能复原其具体配置与差距。

**实验想回答的问题**

- ES训练带来的任务性能是否依赖于全模型范围内的大量参数变化，还是主要由少数幅度较大的更新坐标贡献？
- 按更新幅度逐步删除ES参数变化后，不同模型规模与任务难度下的性能—稀疏度关系是否一致？

**实验实现**

幅度阈值实验对每个ES更新坐标$\Delta\theta_i$应用阈值$\tau$：凡是$0<|\Delta\theta_i|\leq\tau$，就把该更新置零，等价于将对应参数恢复到Base Model。随后在目标任务上重新评估Pass@1，并同时报告更新稀疏度及其相对Full ES的百分点变化。Pass@1由每道题32个保留回答估计。表11覆盖GSM8K上的三个指令模型，表12覆盖MATH-500上的DeepSeek-R1-Distill-Qwen-1.5B。节选没有报告随机种子、置信区间、显著性检验、解码参数或GRPO的完整复现实验配置。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| GSM8K上的Qwen2.5-1.5B-Instruct：逐步提高幅度阈值 | 在$\tau=1.0\times10^{-3}$时清零79.11%的更新，Pass@1仅下降$0.351$个百分点；但当$\tau$升至$1.5\times10^{-3}$、稀疏度达到92.47%时，Pass@1下降$1.260$个百分点。这隔离出一个转折：小幅更新大多可删，但阈值继续进入较大幅更新区域后，开始删除真正承担任务收益的坐标。 | 该消融不是比较不同训练算法，而是在同一个ES终点上按更新幅度撤销参数变化。约79%的小更新可移除而损失很小，支持功能稀疏性；92.47%时损失扩大，则说明剩余较大更新并非冗余。由于参数可能相互作用，实验只能说明这种幅度规则下的整体效果，不能把每个保留坐标单独解释为因果关键参数。 | Appendix D，Table 11，Qwen2.5-1.5B-Instruct<br><span class="experiment-evidence">1.5 × 10−3 \| 92.47 \| 72.091 \| −1.260</span> |
| MATH-500上的DeepSeek-R1-Distill-Qwen-1.5B：从93.16%继续提高到96.64%稀疏度 | 当$\tau=3.0\times10^{-3}$、稀疏度达到96.64%时，Pass@1降至81.388%，相对Full ES下降$1.456$个百分点；相比93.16%稀疏度时仅下降$0.631$个百分点，最后约3.5%的额外删除造成了更明显损失。 | 这一阈值扫描检验性能是否会随稀疏度持续稳定。结果显示存在非线性退化：先删除大量小更新影响有限，但当阈值覆盖更多较大更新时，性能下降加速。因此，证据支持“贡献集中于更新分布的较大幅尾部”，而不是“只需任意极少量参数即可无损训练”。 | Appendix D，Table 12，DeepSeek-R1-Distill-Qwen-1.5B<br><span class="experiment-evidence">3.0 × 10−3 \| 96.64 \| 81.388 \| −1.456</span> |

**定性案例**

- Qwen2.5-7B-Instruct是一个反常但有信息量的个案：从25.43%到98.11%的更新稀疏度范围内，Pass@1相对Full ES均未下降，最高提高$0.808$个百分点。分析上，这可能表示小幅ES更新对GSM8K含有噪声或该基础模型已接近任务上限；但原文没有显著性检验或机制证据，不能据此断言删除小更新必然改善大模型。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work studies Evolution Strategies as an LLM reasoning post-training method and compares its reasoning coverage with GRPO.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`8aa172809d7252f813436ab986e754be380aff1da6def8643fdf42618a1e740d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
