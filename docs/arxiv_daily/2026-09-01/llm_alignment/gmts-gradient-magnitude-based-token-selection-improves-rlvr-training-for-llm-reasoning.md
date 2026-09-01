---
title: "[论文解读] GMTS: Gradient Magnitude-based Token Selection Improves RLVR Training for LLM Reasoning"
description: "[arXiv 2608.30632][对齐 / RLHF] 原文未明确报告。"
arxiv_id: "2608.30632"
announcement_date: "2026-09-01"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:49:56.010540+00:00"
source_sha256: "756561ceab3a9b1ac8b4584b76d18cf35a8b798b46407a47751832d69d39ddc2"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "带可验证奖励的强化学习"
  - "词元选择"
  - "梯度幅度"
  - "词元熵"
  - "推理训练"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.30632</p>

# GMTS: Gradient Magnitude-based Token Selection Improves RLVR Training for LLM Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Outongyi Lv, Yuanwei Zhang, Xiaoqun Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: School of Mathematical Sciences, Shanghai Jiao Tong University；Affiliation: Institute of Natural Sciences, Shanghai Jiao Tong University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30632v1) · [PDF 下载](https://arxiv.org/pdf/2608.30632v1) · **关键词** 大语言模型, 带可验证奖励的强化学习, 词元选择, 梯度幅度, 词元熵, 推理训练<br>
**代码**: [https://github.com/outongyiLv/GMTS](https://github.com/outongyiLv/GMTS)

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

本文研究大语言模型（LLM）的强化学习训练，具体聚焦于带可验证奖励的强化学习（RLVR）。在该设置中，模型根据问题生成推理答案，外部规则或验证器判断答案是否正确并提供奖励；随后，策略优化算法利用这些奖励调整模型，使其更倾向于生成可验证的正确推理。现有 RLVR 方法通常把同一答案的奖励或优势信号均匀分配给所有生成词元，但不同词元对最终答案的贡献并不相同，因此本文关注如何在训练时识别更值得更新的词元。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自回归策略与词元熵**

LLM 按顺序生成词元，在第 $t$ 步根据问题和此前词元形成分布 $\pi_{\theta}(\cdot\mid\boldsymbol{q},\boldsymbol{o}_{<t})$。该分布的熵衡量模型对下一词元的不确定性：熵越高，表示模型在多个候选词元之间越难作出选择。

</div>
<div class="concept-item" markdown="1">

**RLVR 与回答级优势**

RLVR 使用可验证的任务奖励，例如数学答案是否正确，而不必依赖人工逐步标注。GRPO 等方法先比较同一问题生成的多个回答，将回答奖励标准化为回答级优势 $A_i$，再把这个信号分配给回答中的各个词元。

</div>
<div class="concept-item" markdown="1">

**词元选择与梯度幅度**

词元选择是在一次训练更新中只保留部分词元的损失或梯度，从而减少低贡献位置对优化的干扰。词元梯度幅度可理解为该词元对模型参数更新潜在影响的大小；幅度越大，通常表示该位置更值得关注。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定问题 $\boldsymbol{q}$，参数为 $\theta$ 的 LLM 策略 $\pi_{\theta}$ 自回归生成回答 $\boldsymbol{o}=(o_1,\ldots,o_T)$，其中 $T$ 是回答长度。模型在第 $t$ 步根据 $\boldsymbol{q}$ 与此前生成的词元 $\boldsymbol{o}_{<t}$ 输出词汇表上的概率分布，并从中生成 $o_t$；RLVR 验证完整回答并产生奖励。本文要解决的是：在保持现有 GRPO 或 DAPO 等 RLVR 训练框架基本不变的前提下，如何从回答中的全部词元中筛选出更能代表真实训练贡献的部分词元。论文将熵选择作为重要对照：熵选择方法（ETS）保留每个回答中熵最高的约 $20\%$ 词元，而 GMTS 试图依据近似的梯度幅度排名进行选择。基本假设是，同一回答内高熵与大梯度幅度通常相关，但不同回答的奖励信号和样本特征存在差异，因而单独使用熵可能无法可靠比较跨回答的词元重要性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{V}$**

有限词汇表，即模型能够生成的全部词元集合。

</div>
<div class="notation-item" markdown="1">

**$\boldsymbol{q}$**

输入问题或查询。

</div>
<div class="notation-item" markdown="1">

**$\boldsymbol{o}=(o_1,\ldots,o_T)$**

模型生成的回答词元序列；$o_t$ 表示第 $t$ 个词元，$T$ 表示回答长度。

</div>
<div class="notation-item" markdown="1">

**$E_t$**

第 $t$ 个生成位置的预测分布熵，定义为 $E_t=-\sum_{k=1}^{V}p_{t,k}\log p_{t,k}$；其中 $p_{t,k}$ 是第 $t$ 步生成词汇表中第 $k$ 个词元的概率，$V$ 是词汇表大小。

</div>

</div>

**直接相关的工作**

- **GRPO（Group Relative Policy Optimization）**: GRPO 从同一问题采样的 $G$ 个回答及其奖励计算组内相对优势，不需要单独训练价值模型，并将回答级优势 $A_i$ 赋给该回答的所有词元。GMTS 可嵌入这一目标，通过筛选高估计重要性的词元，缓解 GRPO 对所有词元使用统一训练信号的问题。
- **Entropy-based Token Selection（ETS）**: ETS 根据词元预测熵选择每个回答中熵最高的约 $20\%$ 词元进行 RLVR 更新；已有工作报告这种稀疏训练能够提升推理性能。本文认为 ETS 主要反映同一回答内部的不确定性，无法充分处理不同回答之间奖励差异造成的词元重要性差异，因此提出用熵与梯度幅度关系近似梯度排名的 GMTS 作为更细粒度的选择方法。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

GMTS（Gradient Magnitude-based Token Selection）是一种用于RLVR训练的令牌筛选方法。其输入是同一问题下由旧策略采样的一组回答、每个回答的可验证奖励，以及当前策略计算出的逐令牌概率、熵和PPO式学习信号。方法先把逐令牌目标的梯度分解为“标量学习系数”与“对数概率梯度”的乘积，再利用令牌熵近似后者的大小，由此以$\delta_{i,t}=|E_{i,t}\omega_{i,t}(\theta)|$估计真实梯度幅值；最后只保留一个训练批次中得分最高的$\rho$比例令牌计算策略更新。
直观地说，熵衡量模型在某个位置有多犹豫，但“犹豫”不等于“对当前RL更新重要”：回答奖励形成的优势、PPO裁剪和KL正则都可能放大或压低该令牌的实际作用。GMTS因此将“模型有多不确定”与“当前优化器实际上会给它多大权重”结合起来，比仅按熵排序的ETS更接近真实梯度贡献。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 采样回答并构造回答级优势

对每个问题采样$G$个回答$\boldsymbol{o}_1,\ldots,\boldsymbol{o}_G$并获得奖励$R_1,\ldots,R_G$；在GRPO中将组内标准化奖励作为回答优势$A_i$，并令该回答各位置共享$A_{i,t}=A_i$。若使用DAPO，还会按其动态采样规则丢弃全对或全错、因而缺少有效组内区分的回答组。

<div class="method-step__io" markdown="1">

**输入**：问题$\boldsymbol{q}\sim\mathcal{D}$、旧策略$\pi_{\text{old}}$、每个问题的采样数$G$以及可验证奖励函数。<br>
**输出**：带有回答级优势$A_i$的逐令牌训练轨迹。

</div>

**直观理解**：同一道题生成多份答案，再用它们之间的相对好坏决定每份答案应被鼓励还是抑制。这个信号最初属于整份回答，而不是某一个具体令牌。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算逐令牌熵与有效学习系数

由当前策略的词表分布计算熵$E_{i,t}=-\sum_{k=1}^{V}p_{i,t,k}\log p_{i,t,k}$；同时依据概率比、优势、PPO裁剪状态和可选的KL项计算标量系数$\omega_{i,t}(\theta)$。DAPO没有KL惩罚，因此其系数只保留裁剪后的策略梯度部分。

<div class="method-step__io" markdown="1">

**输入**：每个回答的上下文、当前策略$\pi_\theta$、旧策略$\pi_{\text{old}}$、优势$A_{i,t}$，以及GRPO情形下的参考策略$\pi_{\text{ref}}$。<br>
**输出**：每个令牌的熵$E_{i,t}$和实际优化权重$\omega_{i,t}(\theta)$。

</div>

**直观理解**：熵表示模型在该位置是否拿不准，系数则表示训练规则是否真的允许并要求这个位置产生较强更新。两者分别描述“潜在梯度大小”和“奖励及优化约束给出的力度”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 估计梯度幅值并进行全批次排序

为每个令牌计算GMTS分数$\delta_{i,t}=|E_{i,t}\omega_{i,t}(\theta)|$，然后在整个批次的所有回答和位置之间统一排序。取使得$\delta_{i,t}\geq\tau_\rho$的令牌，其中阈值$\tau_\rho$对应最高$\rho$比例。

<div class="method-step__io" markdown="1">

**输入**：批次内所有令牌的$E_{i,t}$与$\omega_{i,t}(\theta)$。<br>
**输出**：包含$S_\rho$个高估计梯度幅值令牌的选择掩码。

</div>

**直观理解**：这不是在每份答案内部各挑一些“最犹豫”的词，而是把批次里的令牌放到同一标尺上竞争。来自高价值回答且未被裁剪抑制的令牌，通常会比只有高熵但学习信号弱的令牌排名更高。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 仅用选中令牌执行策略更新

只累计满足$\delta_{i,t}\geq\tau_\rho$的逐令牌目标，并按$S_\rho$归一化后对$\theta$求梯度更新；未选中令牌不参与该步反向传播目标。该过程可嵌入GRPO或DAPO，区别仅在$\omega_{i,t}(\theta)$的具体定义。

<div class="method-step__io" markdown="1">

**输入**：选择掩码、逐令牌PPO式目标$\ell_{i,t}(\theta)$和选中令牌数$S_\rho$。<br>
**输出**：由高估计贡献令牌更新后的策略参数$\theta$。

</div>

**直观理解**：训练算力集中在预计最能改变模型的少量位置上，而不是平均处理回答中的每个词。模型结构和生成方式不变，改变的只是哪些令牌进入训练损失。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 逐令牌梯度分解与有效学习系数

$$
\nabla_{\theta}\ell_{i,t}(\theta)=\omega_{i,t}(\theta)\nabla_{\theta}\log\pi_{\theta}(o_{i,t}),\qquad \omega_{i,t}(\theta)=r_{i,t}(\theta)A_{i,t}\mathbb{I}_{\epsilon_1,\epsilon_2}(r_{i,t}(\theta),A_{i,t})+\beta\frac{\pi_{\mathrm{ref}}(o_{i,t})}{\pi_{\theta}(o_{i,t})}-\beta
$$

**符号说明**

- $\ell_{i,t}(\theta)$：第$i$个回答中第$t$个令牌的PPO式训练目标。
- $\theta$：当前语言模型或策略的参数。
- $\omega_{i,t}(\theta)$：缩放对数概率梯度的有效学习系数，综合优势、PPO裁剪和KL正则信号。
- $\pi_{\theta}(o_{i,t})$：在问题与回答前缀条件下，当前策略生成令牌$o_{i,t}$的概率。
- $r_{i,t}(\theta)$：当前策略与旧策略对该令牌的概率比，即$\pi_\theta(o_{i,t})/\pi_{\mathrm{old}}(o_{i,t})$。
- $A_{i,t}$：分配给该令牌的优势；在文中GRPO设置下等于所属回答的组内标准化优势$A_i$。
- $\mathbb{I}_{\epsilon_1,\epsilon_2}$：PPO裁剪指示函数；正优势且概率比超过$1+\epsilon_2$，或负优势且概率比低于$1-\epsilon_1$时取$0$，其余情况取$1$。
- $\beta$：KL惩罚强度；DAPO省略KL项，相当于删除公式中的后两项。
- $\pi_{\mathrm{ref}}$：用于KL约束的参考策略。

<div class="equation-explanation" markdown="1">

**直观理解**：该分解指出，真实逐令牌梯度不仅取决于模型在该位置的概率分布，还要乘上RLVR目标给出的有效系数。GMTS正是利用这一结构：用熵代理对数概率梯度的幅值，同时保留$\omega_{i,t}(\theta)$中由奖励、裁剪和KL产生的差异。<br>
**原文位置**：第3节“Gradient of each token”

</div>

</div>

<div class="equation-block" markdown="1">

#### GMTS分数与稀疏令牌训练目标

$$
\delta_{i,t}=\left|E_{i,t}\omega_{i,t}(\theta)\right|,\qquad \max_{\theta}\mathbb{E}_{\boldsymbol{q}}\left[\frac{1}{S_{\rho}}\sum_{i=1}^{G}\sum_{t=1}^{|\boldsymbol{o}_i|}\mathbb{I}[\delta_{i,t}\geq\tau_{\rho}]\,\ell_{i,t}(\theta)\right]
$$

**符号说明**

- $\delta_{i,t}$：第$i$个回答第$t$个令牌的GMTS重要性分数，即真实梯度幅值的可计算代理。
- $E_{i,t}$：当前策略在该位置的词表预测熵。
- $\omega_{i,t}(\theta)$：逐令牌目标中的有效标量学习系数。
- $\boldsymbol{q}$：从训练分布中抽取的输入问题。
- $G$：针对同一问题采样的回答数量。
- $\boldsymbol{o}_i$：第$i$个采样回答，$|\boldsymbol{o}_i|$为其令牌长度。
- $\rho$：预先指定的保留比例，例如保留得分最高的一部分令牌。
- $\tau_{\rho}$：与Top-$\rho$选择相对应的分数阈值。
- $S_{\rho}$：当前组或批次中被选择的令牌总数，用于对损失归一化。
- $\mathbb{I}[\cdot]$：选择指示函数，条件成立取$1$，否则取$0$。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分用“熵乘以有效学习系数的绝对值”近似令牌的真实梯度范数；第二部分只让高于Top-$\rho$阈值的令牌进入目标，并按实际选中数平均。这样既不会像普通GRPO或DAPO那样平等处理回答内全部令牌，也不会像ETS那样忽略回答级奖励和PPO约束。<br>
**原文位置**：公式（2），第3节“Gradient magnitude token selection”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：优化仍采用GRPO或DAPO的逐令牌PPO式目标$\ell_{i,t}(\theta)$，GMTS不替换奖励、优势估计或策略目标本身，而是在求和前增加由$\delta_{i,t}$决定的二值掩码。梯度只从批次内Top-$\rho$令牌回传，并以选中数$S_\rho$而非回答长度归一化；因此它改变的是训练样本在令牌层面的有效支持集。对GRPO，$\omega_{i,t}$含KL参考策略修正；对DAPO，KL项被移除，并沿用DAPO的动态采样、令牌级损失平均和较大上裁剪阈值等基础机制。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 熵—梯度代理**

命题3.1令$G_t$为已生成令牌对logits的对数概率梯度的$\ell_2$范数，并令$\varepsilon=1-\pi_\theta(o_t\mid\boldsymbol{q},\boldsymbol{o}_{<t})$；当$\varepsilon\rightarrow 0$时，有$\log G_t/\log E_t\rightarrow 1$。再由链式法则，参数梯度等于logits关于参数的雅可比矩阵乘以logits层梯度，因此论文用$E_t$近似对数概率参数梯度的相对大小。

> 直观理解：直接为每个令牌单独计算完整参数梯度代价过高；熵是前向计算中已有的廉价统计量。该命题说明，当模型给已生成令牌的概率较高时，熵与logits梯度在对数尺度上近似同阶，但这只支持一种排序代理，并不声称二者在所有状态下严格相等。

**2. 有效学习系数$\omega_{i,t}(\theta)$**

逐令牌梯度可写成$\omega_{i,t}(\theta)\nabla_\theta\log\pi_\theta(o_{i,t})$。在GRPO中，$\omega_{i,t}$汇集概率比$r_{i,t}$、优势$A_{i,t}$、非对称裁剪指示函数以及KL参考策略修正；在DAPO中去除KL项，若当前策略接近旧策略且裁剪未激活，则$\omega_{i,t}\approx A_{i,t}$。

> 直观理解：两个令牌即使熵相同，也可能因为所属回答的奖励不同而产生完全不同的更新强度；越界裁剪还可能让原本看似重要的梯度失效。该系数把这些RLVR特有因素纳入重要性判断。

**3. Top-$\rho$令牌选择器**

选择器按$\delta_{i,t}=|E_{i,t}\omega_{i,t}(\theta)|$对批次内令牌排序，以阈值$\tau_\rho$保留最高$\rho$比例，并仅在选中集合上平均逐令牌目标。绝对值使正、负优势造成的强更新都能按幅值进入候选，而不是只保留鼓励方向的令牌。

> 直观理解：重要性关心“会产生多大的参数变化”，而不关心变化是提高还是降低该令牌概率。因此，强奖励与强惩罚对应的位置都可能被保留。

**训练与推理**

训练阶段，首先由$\pi_{\text{old}}$针对每个问题生成一组回答，使用可验证奖励计算组内优势；随后当前策略完成逐令牌前向计算，得到预测分布、熵、概率比和裁剪状态，并据所用RLVR框架计算$\omega_{i,t}(\theta)$。系统在批次范围内计算$\delta_{i,t}$、确定Top-$\rho$阈值$\tau_\rho$，再仅以选中令牌的目标更新参数；更新后继续下一轮采样与优化。
推理阶段不需要GMTS打分、令牌筛选、优势或参考策略。训练所得模型仍按普通自回归方式，根据问题$\boldsymbol{q}$和已有前缀$\boldsymbol{o}_{<t}$逐步预测并生成答案，因此该方法没有引入新的推理模块或额外推理开销。

**复现信息**

实现GMTS所需的$A_{i,t}$、$\pi_\theta$、$\pi_{\text{old}}$以及GRPO中的$\pi_{\text{ref}}$本来就会在标准RLVR训练中计算；新增操作主要是熵计算、$\delta_{i,t}$构造、批次内Top-$\rho$排序或阈值化以及损失掩码，因此作者称额外计算开销较小。筛选范围是批次内所有回答的全部令牌，而不是分别在每个回答内选取；损失必须按$S_\rho$归一化，才能避免回答长度或实际选中数改变梯度尺度。原文方法描述将$\rho$视为预定义比例，并在论文整体设定中重点讨论Top 20%令牌，但所给章节未明确报告排序算子的具体工程实现、并列分数处理方式或额外显存开销。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 数学领域：使用 $\mathrm{MATH\text{-}12K}$ 训练集训练 $1.5\mathrm{B}$ 与 $7\mathrm{B}$ 模型，使用 $\mathrm{DAPO\text{-}MATH\text{-}17K}$ 训练 $8\mathrm{B}$ 模型；评测包括 $\mathrm{AIME2024}$、$\mathrm{AMC23}$、$\mathrm{MATH\text{-}500}$、$\mathrm{Minerva}$、$\mathrm{OlympiadBench}$，并在 $8\mathrm{B}$ 模型上额外评测 $\mathrm{AIME2025}$。这些数据测试模型在不同难度和题型上的数学推理能力。
- 代码领域：使用 $\mathrm{KodCode}$ 训练 $\mathrm{Qwen2.5\text{-}coder}$ 的 $1.5\mathrm{B}$ 与 $7\mathrm{B}$ 模型，评测 $\mathrm{LiveCodeBench}$（202407–202411）、$\mathrm{MBPP}$、$\mathrm{HumanEval}$ 和 $\mathrm{BigCode\text{-}Bench}$。其中代码执行正确率检验模型将推理转化为可运行程序的能力；$\mathrm{HumanEval}$、$\mathrm{MBPP}$$\text{的}$结果分别平均了其 $\mathrm{Base}$ 与 $\mathrm{Plus}$ 子集，$\mathrm{BigCode\text{-}Bench}$ 结果平均了 $\mathrm{Full}$ 与 $\mathrm{Hard}$ 子集。
- 常识领域：使用 $\mathrm{CS\text{-}QA}$ 训练 $\mathrm{Qwen2.5\text{-}base}$ 的 $1.5\mathrm{B}$ 与 $7\mathrm{B}$ 模型，评测 $\mathrm{CS\text{-}QA}$ 测试集和更一般的 $\mathrm{CS\text{-}QA2}$。该设置检验令牌选择方法能否从形式化推理迁移到常识问答。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**accuracy（准确率）**

在数学和代码基准上，模型答案正确或程序通过测试的比例；数学领域报告 $\mathrm{average@16}$，即每题生成 $16$ 个候选答案后的平均正确率，代码领域采用贪心解码后的正确率。 （越高越好，因为它直接表示正确解决测试题的比例。）

</div>
<div class="metric-item" markdown="1">

**Avg.（平均准确率）**

同一设置下多个评测基准准确率的平均值，用于概括跨数据集的总体表现。 （越高越好，但它可能掩盖单个基准上的退步，因此不能替代逐基准分析。）

</div>
<div class="metric-item" markdown="1">

**selected ratio（选择比例）**

训练时实际保留并用于更新的答案令牌比例；主实验通常选择排名最高的前 $20\%$，敏感性实验测试 $0.1$、$0.2$、$0.5$、$0.7$ 和 $0.9$。 （没有固定的越高越好标准；该指标用于分析训练信号稀疏程度与性能之间的关系。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 数学推理：$\mathrm{Qwen2.5\text{-}math}$ 的 $1.5\mathrm{B}$ 与 $7\mathrm{B}$ 模型，在 $\mathrm{DAPO}$、$\mathrm{GRPO}$ 及五个数学基准上比较前 $20\%$ 的 $\mathrm{ETS}$ 与 $\mathrm{GMTS}$。

<div class="result-value" markdown="1">

按表中 Avg.，$\mathrm{GMTS}$ 相比 $\mathrm{ETS}$ 的提升为：$1.5\mathrm{B}$-$\mathrm{DAPO}$ 提升 $1.55$ 个百分点，$1.5\mathrm{B}$-$\mathrm{GRPO}$ 提升 $1.30$ 个百分点，$7\mathrm{B}$-$\mathrm{DAPO}$ 提升 $1.33$ 个百分点，$7\mathrm{B}$-$\mathrm{GRPO}$ 提升 $3.41$ 个百分点。

</div>

该结果表明，按估计梯度幅度挑选令牌通常比只按熵挑选更能改善数学训练，而且优势在两个模型规模和两个训练骨干上都出现。它支持方法的跨规模、跨骨干有效性，但平均分提升并不意味着每个单独基准都必然提升，也不能单独证明梯度幅度估计就是唯一原因。

<div class="result-source" markdown="1">

来源：第4.2.1节，表1和表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Tables 1 and 2 show that GMTS Top (20%) consistently outperforms ETS across both DAPO and GRPO backbones (1.5B-DAPO: +1.55, 1.5B-GRPO: +1.30, 7B-DAPO: +1.33, 7B-GRPO: +3.41).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 更大数学模型：$\mathrm{Qwen3\text{-}8B}$ 在六个数学基准上使用 $\mathrm{DAPO}$，比较 $\mathrm{ETS}$ 与 $\mathrm{GMTS}$。

<div class="result-value" markdown="1">

$\mathrm{GMTS}$ 相比 $\mathrm{ETS}$ 在总体 Avg. 上提升 $1.85$ 个百分点；在较困难的 $\mathrm{AIME2024}$ 和 $\mathrm{AIME2025}$ 上分别提升 $5.21$ 和 $3.75$ 个百分点。

</div>

该实验把验证范围扩展到更大的模型和更具挑战性的评测，说明方法并非只适用于 $1.5\mathrm{B}$ 或 $7\mathrm{B}$ 模型。困难基准上的较大增益显示令牌重要性估计可能特别有助于训练复杂推理，但该结论仍受限于此处只使用 $\mathrm{DAPO}$ 和单一 $8\mathrm{B}$ 模型。

<div class="result-source" markdown="1">

来源：第4.2.1节，表3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

With an overall average gain of 1.85%, these results demonstrate the generality of GMTS, suggesting it has the potential to scale effectively to larger and more complex reasoning models.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨领域泛化：代码与常识任务上，$1.5\mathrm{B}$、$7\mathrm{B}$ 模型分别结合 $\mathrm{DAPO}$ 和 $\mathrm{GRPO}$，比较 $\mathrm{GMTS}$ 与 $\mathrm{ETS}$。

<div class="result-value" markdown="1">

代码领域 Avg. 相对 $\mathrm{ETS}$ 的提升为 $1.5\mathrm{B}$-$\mathrm{DAPO}$ 的 $1.87$、$1.5\mathrm{B}$-$\mathrm{GRPO}$ 的 $1.90$、$7\mathrm{B}$-$\mathrm{DAPO}$ 的 $0.74$、$7\mathrm{B}$-$\mathrm{GRPO}$ 的 $0.69$ 个百分点；常识领域对应提升为 $0.87$、$0.67$、$1.53$、$1.26$ 个百分点。

</div>

在不同任务形式、模型规模和训练骨干下，$\mathrm{GMTS}$ 的总体平均表现都高于 $\mathrm{ETS}$，说明其收益不局限于数学题。代码结果采用贪心解码、常识结果采用多样本平均，因此两领域的绝对分数不能直接与数学领域比较；这些结果主要证明方向上的泛化，而不是证明所有单项基准均有显著提升。

<div class="result-source" markdown="1">

来源：第4.2.2节，表4和表5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Tables 4 and 5, GMTS achieves consistent performance gains within the code domain (1.5B-DAPO: +1.87, 1.5B-GRPO: +1.90, 7B-DAPO: +0.74, 7B-GRPO: +0.69). Furthermore, in the commonsense domain (1.5B-DAPO: +0.87, 1.5B-GRPO: +0.67, 7B-DAPO: +1.53, 7B-GRPO: +1.26).

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

- 未进行额外令牌选择的基础训练（$\mathrm{DAPO}$ 或 $\mathrm{GRPO}$）：提供训练收益的参照点，用来判断选择令牌本身是否优于直接使用全部训练信号。
- $\mathrm{ETS}$：选择答案中熵最高的前 $20\%$ 令牌，是本文最直接的比较对象，因为已有工作认为高熵令牌对训练尤其重要。
- $\mathrm{DAPO}$：一种用于可验证奖励强化学习（$\mathrm{RLVR}$）的训练框架，与 $\mathrm{GRPO}$ 结合后可检验方法是否依赖特定策略优化算法。
- $\mathrm{GRPO}$：另一种 $\mathrm{RLVR}$ 训练框架，用于检验 $\mathrm{GMTS}$ 在不同强化学习训练骨干上的稳定性。

**实验想回答的问题**

- 在数学推理任务及不同模型规模、训练算法（$\mathrm{DAPO}$ 与 $\mathrm{GRPO}$）下，基于梯度幅度的令牌选择（$\mathrm{GMTS}$）是否比基于熵的令牌选择（$\mathrm{ETS}$）更有效？
- $\mathrm{GMTS}$ 的优势是否能跨越代码推理与常识推理领域，并且对令牌选择比例、低梯度令牌选择等训练设置是否稳健？

**实验实现**

作者在 $\mathrm{verl}$ 框架中实现并评测 $\mathrm{GMTS}$ 与 $\mathrm{ETS}$，覆盖 $\mathrm{GRPO}$ 和 $\mathrm{DAPO}$；同时提供支持有限 GPU 的独立实现。除非另有说明，两种选择方法均使用排名最高的前 $20\%$ 令牌。数学与常识任务每道题生成 $16$ 个候选答案，并以温度 $T=1.0$ 计算 $\mathrm{average@16}$；代码任务采用贪心解码。主要模型规模为 $1.5\mathrm{B}$ 和 $7\mathrm{B}$，数学领域另测试 $8\mathrm{B}$。实验还比较了选择最低梯度幅度或最低熵令牌的底部选择方案，并改变选择比例，以区分“选择重要令牌”与“仅选择高熵令牌”的作用。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 底部选择：在 $\mathrm{Qwen2.5\text{-}math\text{-}1.5B}$ 上使用 $\mathrm{DAPO}$，比较选择最低梯度幅度令牌与选择最低熵令牌，并测试保留比例为 $80\%$ 和 $90\%$。 | 底部 $\mathrm{GMTS}$ 相比底部 $\mathrm{ETS}$ 的平均表现，在 $80\%$ 和 $90\%$ 比例下分别下降 $1.08$ 和 $1.28$ 个百分点。 | 该消融隔离了低梯度幅度令牌的作用：它们被选中后反而弱于低熵令牌，支持“高梯度幅度令牌包含更有用训练信号”的解释。结果不能说明所有低熵令牌都无用；作者明确指出低熵令牌仍可能包含有效信号。 | 第4.3节，图5左图和表6<br><span class="experiment-evidence">This suggests that low gradient magnitude tokens contribute less to RLVR training, whereas low-entropy tokens may still contain useful signals.</span> |
| 选择比例敏感性：在 $\mathrm{Qwen2.5\text{-}math\text{-}1.5B}$ 上分别使用 $\mathrm{DAPO}$ 和 $\mathrm{GRPO}$，测试比例 $0.1$、$0.2$、$0.5$、$0.7$ 和 $0.9$，比较顶部 $\mathrm{ETS}$ 与顶部 $\mathrm{GMTS}$。 | 在十种训练配置中，$\mathrm{GMTS}$ 有九种优于 $\mathrm{ETS}$；原文未明确报告各配置的完整数值差异。 | 该实验测试方法是否只在前 $20\%$ 这一单一设定下有效。九成配置中保持优势说明 $\mathrm{GMTS}$ 对选择强度具有一定稳健性，但由于原文摘录未给出完整数值和方差，无法判断优势大小或统计显著性。 | 第4.3节，表7和图5右图<br><span class="experiment-evidence">It shows that GMTS consistently outperforms ETS in nine out of ten configurations.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出基于梯度幅度的 token 选择方法，核心是改进 RLVR 后训练并提升 LLM 推理能力。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`756561ceab3a9b1ac8b4584b76d18cf35a8b798b46407a47751832d69d39ddc2`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
