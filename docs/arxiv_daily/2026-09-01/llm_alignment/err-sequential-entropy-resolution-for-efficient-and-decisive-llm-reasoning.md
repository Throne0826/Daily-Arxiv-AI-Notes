---
title: "[论文解读] ERR+: Sequential Entropy Resolution for Efficient and Decisive LLM Reasoning"
description: "[arXiv 2608.28771][对齐 / RLHF] 本文针对仅凭答案正确性难以区分推理过程质量的问题，提出顺序式两阶段强化学习框架 ERR+：先奖励思考阶段中从不确定到确定的熵下降，再依据同题候选回答的相对长度优化简洁性。"
arxiv_id: "2608.28771"
announcement_date: "2026-09-01"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:45:06.576090+00:00"
source_sha256: "5725ecde4063014f21028ab0a42cfa7edc3b9c566b1de43c17083724e1d58151"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "可验证奖励强化学习（RLVR）"
  - "大语言模型推理"
  - "链式思维（CoT）"
  - "词元级熵"
  - "熵下降"
  - "回答效率"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.28771</p>

# ERR+: Sequential Entropy Resolution for Efficient and Decisive LLM Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Xin Jiang, Minhao Wang, Wen Wu, Zhentao Xie, Shangheng Du, Jinxin Shi, Jiabao Zhao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: School of Computer Science and Technology, East China Normal University, Shanghai 200241, China；Affiliation: State Key Laboratory of Estuarine and Coastal ResearchSchool of Computer Science and Technology, East China Normal University, Shanghai 200241, China；Affiliation: ByteDance {51275901099</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28771v1) · [PDF 下载](https://arxiv.org/pdf/2608.28771v1) · **关键词** 可验证奖励强化学习（RLVR）, 大语言模型推理, 链式思维（CoT）, 词元级熵, 熵下降, 回答效率<br>
**代码**: [https://github.com/XrkArul/err_response](https://github.com/XrkArul/err_response)

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

本文针对仅凭答案正确性难以区分推理过程质量的问题，提出顺序式两阶段强化学习框架 ERR+：先奖励思考阶段中从不确定到确定的熵下降，再依据同题候选回答的相对长度优化简洁性。

**不用术语来说**：现有推理模型即使给出同样正确的答案，其过程也可能一条短而明确、另一条冗长且反复试探；但只检查最终答案的训练方式会给它们相同奖励，无法教会模型偏好更可靠、更简洁的推理。与此同时，直接压低模型生成时的不确定性又可能阻止必要探索，因此需要一种既保留探索空间、又能奖励及时作出正确判断的训练信号。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者通过跨模型与推理任务的经验分析提出判别性观察：正确推理轨迹在思考阶段通常出现更频繁、幅度更大的逐词元熵下降，并据此设计熵缓解奖励 ERR；该奖励关注不确定性是否被后续推理消解，而不是惩罚高熵本身。
- 作者提出两阶段 ERR+：第一阶段利用 ERR 改善推理结构与正确性，第二阶段利用对同题共生成回答进行组内标准化并经 $\tanh$ 饱和处理的 RRER 优化长度；其理论分析认为两种目标在训练早期存在策略梯度冲突，因此应顺序训练而非直接联合优化。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型的可验证奖励强化学习（RLVR）推理训练。模型接收数学推理问题，生成带有显式思考阶段的链式思维（CoT）轨迹，并依据最终答案是否正确获得奖励；现有方法主要优化结果正确性，却较少直接约束思考过程的质量与效率。本文关注一个更具体的过程信号：正确轨迹通常在探索后出现更频繁、更明显的逐词元熵下降，因此可将“不确定性的解决”作为辅助训练目标，同时进一步压缩冗长回答。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**可验证奖励强化学习（RLVR）**

RLVR使用能够自动检查的结果作为奖励，例如数学题最终答案是否正确。模型通过反复生成回答并根据奖励更新策略，而不是仅依赖人工标注的推理过程。

</div>
<div class="concept-item" markdown="1">

**链式思维与思考阶段**

链式思维（CoT）是模型在给出最终答案前生成的中间推理步骤；本文将由 <think> 与 </think> 标记包围的部分称为思考阶段。该阶段允许模型先探索不同路径，再提交结论。

</div>
<div class="concept-item" markdown="1">

**词元级熵与熵下降**

词元级熵衡量模型在某一步对下一个词元分布的不确定性：熵高表示候选较多、仍在探索，熵低表示更倾向于某个确定选择。相邻位置熵的变化若为负，即 $4\Delta\mathcal{H}_{t}<0$4，则表示不确定性发生了局部下降，本文将其解释为推理路径得到解决或明确承诺的信号。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定输入问题 $x$，策略 $4\pi_{\theta}$4 生成词元序列 $y=(y_{1},\ldots,y_{T})$，其中 $T$ 是回答长度，$T_{k}$ 是思考阶段结束位置；若没有结束标记，则令 $T_{k}=T$。训练场景是带有可验证最终答案的数学推理任务：基础奖励判断最终答案正确性，本文还希望利用思考阶段的熵变化改善推理结构，并在第二阶段依据同一问题下共同生成的回答长度相对位置提升简洁性。核心假设不是压低所有熵，而是保留高熵探索，同时奖励随后发生的有效熵下降。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入问题或查询。

</div>
<div class="notation-item" markdown="1">

**$y=(y_{1},\ldots,y_{T})$**

模型生成的回答词元序列；$y_t$ 表示第 $t$ 个词元，$T$ 表示回答总长度。

</div>
<div class="notation-item" markdown="1">

**$\pi_{\theta}(v\mid x,y_{<t})$**

参数为 $\theta$ 的策略在给定问题 $x$ 和此前词元 $y_{<t}$ 时生成词元 $v$ 的概率。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{H}_{t}$**

思考阶段第 $t$ 个位置的词元分布熵，定义为 $\mathcal{H}_{t}=-\sum_{v\in\mathcal{V}}\pi_{\theta}(v\mid x,y_{<t})\log\pi_{\theta}(v\mid x,y_{<t})$；$\mathcal{V}$ 是词元词表。

</div>

</div>

**直接相关的工作**

- **GRPO（Shao et al., 2024）**: GRPO是本文所处的RLVR训练范式之一，通过同一问题生成的回答组进行组内优势归一化，并省略独立评论家模型。本文指出，当同组回答都正确而只获得相同二元奖励时，GRPO难以区分简洁、结构良好的推理与同样正确但冗长的推理；ERR+因此在其结果奖励基础上增加熵变化和相对长度信号。
- **PEAR（Huang et al., 2025）**: PEAR将思考阶段的平均熵作为长度代理并直接惩罚高熵，以减少回答长度。本文认为这种做法会压制高熵探索位置，而这些位置被既有研究视为RLVR学习的重要推理分岔点；ERR+改为奖励熵下降，从而允许探索并试图同时改善正确率与简洁性。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在采用可验证奖励强化学习（RLVR）的长链式推理模型中，正确性通常由最终答案的二元奖励决定。当同一提示下的一组回答都正确时，它们获得相同奖励，组内归一化后的优势差异会趋近于零，训练因而难以区分结构清晰、迅速收敛的推理与冗长、摇摆但碰巧正确的推理。这一问题在模型正确率较高时尤其突出，并造成推理质量缺乏直接优化以及输出成本偏高。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于最终正确性的 RLVR（如 GRPO、DAPO 所采用的正确性奖励范式）**：模型针对同一问题生成多条回答，以最终答案是否正确形成奖励，再通过组内相对优势更新策略。该范式能直接提升任务成功率，但主要评价结果，不细分得到相同正确答案的不同推理路径。
- **基于绝对熵水平的推理优化方法**：既有方法把逐词元熵视为模型不确定性的指标，通过全局最小化熵、按熵大小缩放梯度，或将思考阶段的高熵作为长度代理加以惩罚，从而鼓励更确定或更短的生成。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 二元正确性奖励无法在多个正确回答之间提供细粒度偏好：若正确回答的奖励相同，则正确子集中的奖励方差坍缩，策略几乎得不到选择简洁、结构良好推理而非冗长推理的信号。
- 直接抑制绝对高熵会把“有害的不确定”与“必要的探索”混为一谈。论文引用的既有发现表明，最高熵的一部分词元往往位于关键推理分岔点，也是 RLVR 学习收益的重要来源；压制这些位置可能以牺牲准确率换取长度下降，文中以 PEAR 报告的准确率退化为例。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种过程级奖励，它既能识别推理是否从探索状态有效过渡到明确结论，又不限制关键分岔处的高熵探索；此外，也缺少一种与该质量信号兼容、能够适应题目难度并抵抗组内异常长度的效率奖励及其合理训练次序。

</div>
<div markdown="1"><span>核心问题</span>

能否将思考阶段的逐词元熵变化——特别是不确定性被消解时的熵下降——转化为可训练的推理质量信号，并与相对长度奖励按适当顺序结合，使模型同时提高答案正确性和回答简洁性，而不产生早期目标冲突？

</div>
<div markdown="1"><span>作者直觉</span>

高熵可以理解为模型正在多个候选思路之间探索，因此不应天然受罚；真正有信息的是探索之后能否出现明显熵下降，即模型找到关键公式、解决子问题或形成结论后，后续选择变得更确定。先奖励这种“探索后作出决定”的动态过程，可帮助模型形成可靠推理；待该能力稳定后，再把每条回答的长度与同题候选回答比较，就能在不把困难题与简单题一概而论的情况下压缩冗余。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ERR+是在可验证奖励强化学习（RLVR）上构建的两阶段训练框架。对每个问题$x$，模型$\pi_{\theta}$先采样一组候选回答$\mathcal{G}=\{y^{(1)},\ldots,y^{(G)}\}$，并用最终答案$y^*$判断正确性。第一阶段从生成时已有的逐词元概率分布计算思考阶段的熵$\mathcal{H}_t$，只对最终答案正确且出现显著熵下降的轨迹给予熵缓解奖励（ERR），使模型学会在充分探索后形成明确判断；第二阶段再按同组回答的相对长度计算稳健相对效率奖励（RRER），在尽量保留正确性的同时删除冗余推理。两个阶段都把组内奖励标准化为GRPO优势并更新策略，最终输出兼顾准确率与回答长度的模型。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 组内采样与可验证判定

从当前策略$\pi_\theta$为同一问题采样回答组$\mathcal{G}=\{y^{(i)}\}_{i=1}^{G}$，记录每个生成位置的logits、回答长度及$</think>$位置$T_k$；再依据最终答案是否匹配$y^*$给出正确、错误或不可解析标签。

<div class="method-step__io" markdown="1">

**输入**：基础策略$\pi_{\theta_0}$、问题$x$、标准答案$y^*$以及每题采样数$G$。<br>
**输出**：带有正确性标签、思考阶段词元分布和长度$L_i$的一组回答。

</div>

**直观理解**：同一道题让模型作答多次，既能比较这些答案谁对，也能比较正确答案之间谁的推理过程更明确、更简洁。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 第一阶段：用ERR塑造决定性推理

由logits计算每个位置的预测熵$\mathcal{H}_t=-\sum_{v\in\mathcal V}\pi_\theta(v\mid x,y_{<t})\log\pi_\theta(v\mid x,y_{<t})$，再累计超过噪声阈值$\epsilon$的局部熵下降，并用$\log(T_k+1)$归一化。该ERR加成仅向最终答案正确的回答开放，并由$R_{\max}$封顶。

<div class="method-step__io" markdown="1">

**输入**：每条回答$y$的思考阶段logits、终止位置$T_k$及正确性标签。<br>
**输出**：第一阶段奖励$R_1$以及经$N_1$步GRPO训练后的阶段一策略$\pi_{\theta_{N_1}}$。

</div>

**直观理解**：熵高表示模型仍在多个下一步之间犹豫，明显下降表示它从探索转向了较确定的路线。方法并不把每次熵下降都当成正确步骤，而是只奖励最终答对的轨迹，避免“很自信地做错”也获得过程奖励。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 第二阶段：用RRER压缩冗余

计算组内长度均值$\mu_L$和标准差$\sigma_L$，将每条长度转换为$z_i=(L_i-\mu_L)/(\sigma_L+\varepsilon)$，再以$\lambda_i=\tanh(-\gamma z_i)$得到有界的相对效率分数。正确回答可以获得短于同组平均值的正奖励或因过长受到负奖励；错误回答最多只受长度惩罚，不能因简短而获得正奖励。

<div class="method-step__io" markdown="1">

**输入**：阶段一策略$\pi_{\theta_{N_1}}$及其针对同一问题生成的一组回答长度$\{L_i\}_{i=1}^{G}$。<br>
**输出**：第二阶段奖励$R_2$以及经$N_2$步GRPO训练后的最终策略$\pi_\theta$。

</div>

**直观理解**：模型不是被要求对所有题都写得一样短，而是只与同一道题的其他作答比较，因此较难问题自然允许更长推理。先学会可靠推理、再删去同类答案中的多余部分，可避免过早压缩切断必要探索。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 组相对优势计算与策略更新

对每条回答计算组内标准化优势$A^{(i)}$，即其奖励减去组均值后除以奖励标准差与稳定项$\delta$之和，并按标准GRPO目标更新$\pi_\theta$。阶段一使用$R_1$，收敛并选定检查点后切换到阶段二的$R_2$，而非同时优化二者。

<div class="method-step__io" markdown="1">

**输入**：当前阶段中同组回答的奖励$\{R(y^{(j)},y^*)\}_{j=1}^{G}$。<br>
**输出**：第一阶段形成具有有效“探索—收敛”结构的策略，第二阶段在此基础上形成更简洁的最终策略。

</div>

**直观理解**：GRPO关心的是同题多次作答之间谁相对更好；ERR让同样答对的轨迹仍可按熵下降质量区分，RRER则让它们进一步按相对长度区分。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 第一阶段正确性门控的熵缓解奖励

$$
\begin{aligned} r_t&=\max\!\left(\mathcal H_{t-1}-\mathcal H_t-\epsilon,0\right),\\ \mathrm{ERR}(y)&=\frac{\sum_{t=2}^{T_k}r_t}{\log(T_k+1)},\\ R_1(y,y^*)&=\begin{cases}\min\!\left(R_b+\lambda\,\mathrm{ERR}(y),R_{\max}\right),&\text{correct},\\ R_f,&\text{incorrect},\\ 0,&\text{unparseable}.\end{cases}\end{aligned}
$$

**符号说明**

- $y$：模型生成的完整回答。
- $y^*$：用于验证最终答案的标准答案。
- $t$：思考阶段中的词元位置。
- $T_k$：结束思考标记的位置；若不存在该标记，则取完整回答长度。
- $\mathcal H_t$：位置t处模型下一词元分布的香农熵。
- $\epsilon$：过滤微小熵波动的非负阈值。
- $r_t$：位置t处超过阈值的局部熵下降量。
- $\mathrm{ERR}(y)$：回答y经对数长度归一化后的累计熵缓解分数。
- $R_b$：回答正确时的基础奖励。
- $\lambda$：ERR加成的权重。
- $R_{\max}$：正确回答总奖励的上限。
- $R_f$：答案错误但格式可解析时的小格式奖励。
- $R_1$：第一阶段用于GRPO训练的总奖励。

<div class="equation-explanation" markdown="1">

**直观理解**：第一行只截取足够明显的熵下降，第二行累计这些下降并温和地校正推理长度，第三行再用最终正确性门控该过程信号。这样能够在传统二元正确奖励无法区分多条正确轨迹时，优先强化那些更频繁、更明显地消除不确定性的正确推理。<br>
**原文位置**：第4.1节，公式(2)–(4)

</div>

</div>

<div class="equation-block" markdown="1">

#### 第二阶段稳健相对效率奖励

$$
\begin{aligned} z_i&=\frac{L_i-\mu_L}{\sigma_L+\varepsilon},\qquad \lambda_i=\tanh(-\gamma z_i),\\ R_2(y^{(i)},y^*)&=\begin{cases}R_b+\alpha\lambda_i,&\text{correct},\\ R_f+\alpha\min(0,\lambda_i),&\text{otherwise}.\end{cases}\end{aligned}
$$

**符号说明**

- $i$：同一问题回答组中的样本索引。
- $y^{(i)}$：回答组中的第i条回答。
- $L_i$：第i条回答的词元长度。
- $\mu_L$：同组G条回答长度的均值。
- $\sigma_L$：同组回答长度的标准差。
- $\varepsilon$：防止标准差为零的稳定常数，原文设为10^{-5}。
- $z_i$：第i条回答相对于同组长度分布的标准化偏差。
- $\gamma$：双曲正切映射对长度偏差的敏感度。
- $\lambda_i$：范围位于(-1,1)内的相对效率分数；回答越短于组均值，该值越大。
- $\alpha$：效率奖励或惩罚的权重。
- $R_b$：正确回答的基础奖励。
- $R_f$：非正确回答的基础格式奖励。
- $R_2$：第二阶段用于GRPO训练的总奖励。

<div class="equation-explanation" markdown="1">

**直观理解**：该奖励先判断一条回答相对同题其他回答是偏长还是偏短，再把差异压缩到有界区间。正确回答可因相对简短获益，但错误回答即使很短也不能获得正向效率奖励，从而把“简洁”置于“正确”之后。<br>
**原文位置**：第4.2节，公式(5)、(6)和(8)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：两个阶段均通过最大化相应期望奖励训练，等价地最小化$\mathcal L_k(\theta)=-\mathbb E_{\pi_\theta}[R_k]$。具体地，同题第$i$条回答使用标准化优势$A^{(i)}=\bigl(R(y^{(i)},y^*)-G^{-1}\sum_jR(y^{(j)},y^*)\bigr)/\bigl(\operatorname{std}(\{R(y^{(j)},y^*)\})+\delta\bigr)$进入标准GRPO更新：第一阶段令$R=R_1$，用正确性门控的熵下降在正确回答内部产生非退化的过程差异；第二阶段令$R=R_2$，用组内相对长度继续区分回答。作者没有联合优化两个奖励，因为定理1认为早期$g_1$与$g_2$方向相冲突：长度梯度会删除尚处于高熵探索、但可能支撑后续有效熵下降的上下文；顺序训练让模型先建立可靠的探索—收敛结构，再优化效率。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 正确性门控的熵缓解奖励（ERR）**

对$t\in[2,T_k]$定义熵缓解$r_t=\max(\mathcal H_{t-1}-\mathcal H_t-\epsilon,0)$，并以$\mathrm{ERR}(y)=\sum_{t=2}^{T_k}r_t/\log(T_k+1)$汇总。对数归一化抑制单纯延长轨迹来累积下降的激励，但比线性长度归一化更少惩罚确实需要长推理的难题；奖励仅在答案正确时加入基础正确性奖励。

> 直观理解：该模块奖励的不是低熵本身，而是模型经历不确定探索后成功消除不确定性的过程。正确性门控是关键保险：熵下降只是“作出承诺”的代理信号，不能独立证明中间步骤在语义上正确。

**2. 稳健相对效率奖励（RRER）**

RRER用同一问题下的组内均值$\mu_L$作为隐式难度参照，通过长度$z$分数和$\tanh$映射将效率分数限制在$(-1,1)$。若$\sigma_L<\varepsilon$，所有回答等长，令$\lambda_i=0$关闭该信号；对错误回答采用$\min(0,\lambda_i)$，阻止短错误答案领取效率加成。

> 直观理解：绝对长度惩罚会把困难问题也强行截短，而组内比较只要求同题回答不要无谓地比同伴更长。$\tanh$还避免某条达到最大生成长度的异常回答扭曲整个组的奖励尺度。

**3. 由梯度冲突驱动的顺序调度**

作者把两阶段负期望奖励记为$\mathcal L_k(\theta)=-\mathbb E_{\pi_\theta}[R_k]$，梯度记为$g_k=\nabla_\theta\mathcal L_k$。定理1指出，只要仍存在高熵但尚未产生奖励性下降的“探索中”位置，即$\rho(\theta)>0$，便有$\langle g_1,g_2\rangle\le -C\rho(\theta)<0$；第一阶段收敛后$\rho(\theta)\approx0$，冲突随之减弱。

> 直观理解：早期的长度压力可能先删掉形成正确突破所需的试探上下文，因此会与ERR的学习方向对抗。等第一阶段稳定了推理结构，第二阶段主要删去低熵、重复且对ERR贡献很小的片段，压缩才更安全。

**训练与推理**

训练时，阶段一从基础模型$\pi_{\theta_0}$开始。每一步针对问题$x$采样$G$条回答，保存生成logits，在思考区间计算逐词元熵和$\mathrm{ERR}(y^{(i)})$，根据最终答案正确性分配$R_1$，计算组相对优势并执行GRPO更新；持续至$N_1$步并选出阶段一检查点。阶段二从该检查点继续，对每个问题重新组采样，先在完整回答组上统计$\mu_L$与$\sigma_L$，再逐条计算$\lambda_i$和$R_2$，执行$N_2$步GRPO更新后返回最终策略。推理时不再计算ERR、RRER或组内统计，只需像普通自回归语言模型一样输入单个问题并生成回答，因此这些奖励不会引入额外的部署模块；原文还指出训练阶段的熵直接来自已有逐词元logits，不增加额外推理调用。

**复现信息**

复现时最关键的边界条件有四项。第一，熵只在思考阶段计算，$T_k$取$</think>$的位置，缺失时取回答末尾；第二，ERR必须经过最终正确性门控，并以$R_{\max}$限制单条样本对组优势的支配作用；第三，RRER的稳定常数为$\varepsilon=10^{-5}$，若$\sigma_L<\varepsilon$则令全部$\lambda_i=0$，且错误回答只能得到非正的长度修正；第四，两阶段必须顺序执行，阶段二从阶段一检查点初始化。原文对$N_1$和$N_2$采用同一检查点规则：排除响应长度为异常值的检查点后，选择验证准确率最高者，并在不同变体、骨干模型和优化器之间一致应用。其余如$G$、$\epsilon$、$\gamma$、$\lambda$、$\alpha$、$R_b$、$R_f$与$R_{\max}$的具体数值在所给节选中未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：小学数学文字题，通常需要 2–8 步算术推理。作者使用训练集中的 7,473 道题训练全部模型，并使用其测试集评估准确率、响应长度以及轨迹结构；附录 F 的主要机制诊断基于完整的 1,319 样本测试集，安全剪枝实验从原本回答正确的日志中抽取 200 个实例。
- MATH-500：由 500 道高中数学竞赛题构成，用于检验方法能否从 GSM8K 训练分布迁移到更复杂、知识范围更广的数学推理问题。原文节选没有给出其具体测试样本筛选方式。
- AIME24：高难度数学竞赛基准，用于评估困难任务上的泛化能力，并用于比较正确与错误轨迹的熵变化。附录 F 还在四次独立运行中，以 8 个原本回答正确的实例计算安全剪枝准确率；样本很小，因此该机制结果应结合误差条理解。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Pass@1 准确率（Acc）**

每道题只生成一次回答时，最终答案被判定正确的比例；用于衡量训练后模型的任务求解能力。安全剪枝准确率是其机制版本，只在原本正确的样本上检查删除低缓解片段后续写的答案是否仍正确。 （越高越好，因为它表示单次生成得到正确最终答案的概率更高；但单独提高准确率不能说明推理更短或内部机制符合作者解释。）

</div>
<div class="metric-item" markdown="1">

**平均响应长度（Tok）**

模型每次回答平均生成的 token 数，用于近似衡量推理冗长度与生成成本。 （在准确率不下降的前提下越低越好；若长度下降同时准确率显著受损，则只是过度压缩，不能视为有效率提升。）

</div>
<div class="metric-item" markdown="1">

**梯度余弦相似度（Grad cos）**

衡量 ERR 梯度与 RRER 梯度方向的一致程度。负值表示两个目标倾向于将参数推向相反方向，接近零表示冲突减弱，正值表示局部方向略为一致。 （就验证顺序训练动机而言，从明显负值升至接近零或略为正值更好，因为这说明第一阶段结束后再施加长度目标更不容易破坏已形成的推理结构；它本身不是任务性能指标。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### DeepSeek-R1-Distill-Qwen-1.5B 在五个基准上的四次独立运行汇总

<div class="result-value" markdown="1">

作者报告 ERR+ 与其他方法比较时，准确率差异的 $t$ 检验均满足 $p<0.05$；ERR+ 的准确率标准差为 $0.61\%$、方差为 $0.3773$。这是统计稳定性证据，但节选没有提供各比较方法的均值、检验统计量或多重比较校正信息。

</div>

结果支持 ERR+ 的平均准确率优势不太可能只由单次训练波动造成，并表明其四次运行较一致。不过，四次运行的样本量仍有限；仅凭 $p<0.05$ 也不能判断实际提升幅度是否足够大，更不能排除评测集相关性或超参数选择带来的偏差。

<div class="result-source" markdown="1">

来源：Appendix E, Figure 6 accompanying text

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Its accuracy superiority has been verified by rigorous t-tests with p-values all below 0.05 in comparisons with other methods, confirming clear statistical significance and effectively ruling out the impact of random errors.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### DeepSeek-R1-Distill-Qwen-1.5B 在五个基准上的综合准确率—长度表现

<div class="result-value" markdown="1">

作者称 ERR+ 在保持所有比较方法中最高准确率的同时，将平均响应长度降至 5,794 token，长度标准差为 84 token，因而同时获得较短且较稳定的输出。

</div>

该结果直接对应论文的效率目标：不是单纯缩短回答，而是在作者报告的最高准确率条件下得到最短平均输出。它支持 ERR+ 的综合优势，但节选未给出其他方法的具体长度和准确率，也没有延迟、吞吐量或实际算力消耗，因此 token 变少不能直接等同于端到端系统加速比例。

<div class="result-source" markdown="1">

来源：Appendix E, Figure 6 accompanying text

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Furthermore, it delivers notable efficiency superiority: while maintaining the highest accuracy among all methods, it achieves the shortest response length of 5794 tokens, with a response length standard deviation of only 84 tokens that guarantees controllable fluctuations, thus perfectly balancing inference efficiency and result stability.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### GSM8K 上三个训练检查点的机制诊断：训练前、ERR 第一阶段后、完整 ERR+ 后

<div class="result-value" markdown="1">

准确率由 $84.6\%$ 提高到第一阶段后的 $88.1\%$，完整 ERR+ 后达到 $88.6\%$；平均长度同时由 2,076 token 降至 1,612 和 1,324 token。梯度余弦从 $-0.45$ 升至 $-0.05$，最终变为 $+0.02$，说明两个奖励目标的方向冲突在第一阶段后显著减弱。

</div>

这组检查点把最终收益分解为两个阶段：第一阶段贡献了大部分准确率提升并已缩短轨迹，第二阶段则在准确率略升的同时继续压缩长度。梯度余弦的变化与“先组织推理、后压缩”的理论动机一致，但这是相关性的机制诊断，并不能单独证明梯度冲突变化是性能提升的唯一原因。

<div class="result-source" markdown="1">

来源：Appendix F, Table 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

After ERR+ 88.6 1324 0.52 0.06 +0.02

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给节选缺失完整主结果表及五个评测集的完整定义，无法逐项核验四种模型骨干上的准确率、长度、基线差值和置信区间；尤其是 GRPO、PEAR 的具体结果未展示。因此，“跨模型和五个数据集一致改进”主要是作者结论，仍需回查原论文表格与代码。
- 全部模型只在 GSM8K 数学题上训练，评测也以数学或 STEM 推理为主，尚不能据此推断 ERR+ 对开放式问答、代码生成或不可验证任务同样有效。部分机制实验样本很小，例如 AIME24 安全剪枝仅使用 8 个原本正确的实例；此外，响应 token 数只是推理成本的代理指标，并未直接测量墙钟延迟、显存或能耗。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 未训练的初始模型（Before ERR）：用于机制分析，比较同一模型在 ERR 第一阶段前后的准确率、长度、平均熵、探索状态比例和梯度余弦变化，从而隔离第一阶段训练的作用。
- 仅完成第一阶段的 ERR（After ERR / Phase 1）：用于判断熵缓解奖励是否先建立较稳定的推理结构，以及第二阶段 RRER 是否在此基础上进一步压缩响应。
- GRPO：传统的组相对策略优化类强化学习方法，是有意义的优化基线；作者用它比较 ERR+ 在准确率、输出长度和多次运行稳定性上的综合表现，但所给节选未列出 GRPO 的具体分数。
- PEAR：已有推理强化学习比较方法；作者将其作为准确率与输出效率基线，并声称 ERR+ 克服了其准确率不足，但所给节选未提供 PEAR 的定义及逐项数值。

**实验想回答的问题**

- 在相同训练数据和强化学习环境下，两阶段 ERR+ 能否同时提高大推理模型的答案正确率并缩短响应，而且这种优势能否跨模型骨干与不同难度的数学推理基准保持一致？
- ERR+ 的“先建立推理结构、再压缩长度”机制是否得到过程层面的支持，即第一阶段是否增加不确定性被解决的承诺点、缓解熵奖励与长度奖励的梯度冲突，并使第二阶段能够安全删除低信息量推理片段？

**实验实现**

作者评估 DeepSeek-R1-Distill-Qwen-1.5B、DeepSeek-R1-Distill-Qwen-7B、Qwen3-4B 和 Qwen3-8B 四个模型骨干，均使用 verl 框架在 7,473 个 GSM8K 训练问题上进行强化学习。训练批量为 128，学习率为 $1\times10^{-6}$，最大响应长度为 16,384 token；强化学习生成采用温度 $0.6$、top-$p=0.95$、每个提示 8 条 rollout，以及 $0.001$ 的 KL 惩罚系数。默认奖励权重为第一阶段的 $\lambda=0.3$ 和第二阶段的 $\alpha=0.3$。稳定性分析在 DeepSeek-R1-Distill-Qwen-1.5B 上对每种方法运行四次并报告均值、标准差及两两 $t$ 检验；AIME24 与 AMC23 的机制复核同样进行四次独立运行。由于节选缺少主结果表，无法核验全部模型、全部数据集的逐项准确率和长度。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 第一阶段 ERR 的长度归一化形式：线性 $T_k$、次线性 $\sqrt{T_k}$ 与对数 $\log(T_k+1)$ | 在 DeepSeek-R1-Distill-Qwen-1.5B 的五基准平均结果中，对数归一化取得 $68.4\%$ 平均准确率和 5,450 个平均 token；表中线性归一化虽然输出更短，但准确率明显更低。作者据此选择对数形式，让第一阶段保留复杂问题所需的探索空间，再由第二阶段负责压缩。 | 该消融隔离的是 ERR 如何抵消长轨迹天然会累计更多熵下降的问题。线性除以长度相当于要求每个 token 都维持固定的“有效下降密度”，容易惩罚真正需要长推理的难题；对数惩罚更温和。应注意，对数形式在此消融中并不产生最短输出，它的作用是保护第一阶段的正确推理结构，最终效率仍依赖 RRER。 | Section 6, Table 4<br><span class="experiment-evidence">$log(T_k+1)$ 68.4 5450</span> |
| 奖励权重敏感性：$\lambda,\alpha\in\{0.1,0.2,0.3,0.4,0.5\}$ | 作者报告当 $\lambda$ 与 $\alpha$ 均位于 $[0.2,0.4]$ 时，ERR+ 保持超过 $87\%$ 的平均准确率并实现超过 $18\%$ 的长度压缩；默认值 $\lambda=0.3$、$\alpha=0.3$ 位于该区域中央。 | 该实验分别检验熵缓解奖励和效率奖励是否需要精细调节。过小的 $\lambda$ 无法充分鼓励不确定性解决，过大的 $\lambda$ 可能诱导冗长论证；过小的 $\alpha$ 压缩不足，过大则牺牲准确率。存在较宽的有效区域说明方法并非只在单一参数点工作，但“最佳折中”仍取决于作者对准确率与长度的权衡方式。 | Appendix B, Robustness region; Figure 3<br><span class="experiment-evidence">The region λ∈[0.2,0.4] and α∈[0.2,0.4] represents a “sweet spot” where ERR+ maintains >87% average accuracy while achieving >18% length compression.</span> |

**定性案例**

- AIME24 的单题轨迹可视化显示：同一模型生成的正确轨迹在初始探索后出现明显且持续的运行平均熵下降，而错误轨迹长期保持高熵。作者将前者解释为模型逐步确定解题路径，后者解释为不确定性未被解决。随后对完整 AIME24 rollout 做 16 次独立 bootstrap 聚合仍观察到正确组下降更陡，降低了单个精选案例造成假象的风险；但这仍说明熵下降与正确性相关，不能仅凭可视化断言其具有因果作用。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出基于熵下降和相对效率奖励的RLVR后训练方法，以提升LLM推理正确率与简洁性。; rule check: matched taxonomy keywords; top rule score=10.0
- 全文指纹：`5725ecde4063014f21028ab0a42cfa7edc3b9c566b1de43c17083724e1d58151`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
