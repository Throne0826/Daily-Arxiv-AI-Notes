---
title: "[论文解读] Solver-Guided Reasoning for Mixed-Equilibrium Strategies"
description: "[arXiv 2608.06741][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.06741"
announcement_date: "2026-08-10"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-10T02:39:10.475132+00:00"
source_sha256: "c80a931b5d964fb54dcc7f670433c11200b0131561e87ca87d87bed2e8507456"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.06741</p>

# Solver-Guided Reasoning for Mixed-Equilibrium Strategies

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-10</span>
<span><strong>作者</strong> Han Wang, Philippe Beardsell, Boning Li, Aaron Sasmita, Shuai Li, Hongyuan Zha, Baoxiang Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Shanghai Jiao Tong University；Tsinghua University；The Chinese University of Hong Kong, Shenzhen；Vector Institute</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.06741v1) · [PDF 下载](https://arxiv.org/pdf/2608.06741v1) · **关键词** LLM Reasoning<br>


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

本文位于大语言模型推理与不完全信息扩展式博弈的交叉领域。大语言模型通常从人类文本、示范和推理轨迹中学习，但博弈均衡要求模型在隐藏信息下输出完整的行动概率分布，而不是只选择一个看似最优的动作。本文以两人无限注德州扑克（No-Limit Texas Hold’em，简称 $NLH$）的翻牌后决策为具体场景：扑克求解器通过博弈论算法计算接近纳什均衡的混合策略，本文则研究如何把这些数值化、难以解释的策略转化为语言模型能够理解和执行的稀疏战略规则。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**不完全信息扩展式博弈**

扩展式博弈用状态、行动和后续历史表示决策过程；不完全信息意味着玩家不能观察全部状态，例如扑克中看不到对手的底牌。模型因此不能只依据当前可见牌面作确定性判断，还必须考虑隐藏牌和对手可能持有的牌的分布。

</div>
<div class="concept-item" markdown="1">

**纳什均衡与混合策略**

纳什均衡是一组策略，使任何一方在其他方策略不变时都无法通过单独改变策略获益。混合策略不是每次都选择同一动作，而是在给定信息集上按概率分配多个动作，例如以不同频率过牌、下注或加注。

</div>
<div class="concept-item" markdown="1">

**范围层面的策略**

扑克中的“范围”是玩家在当前公共牌和行动历史下可能持有的所有底牌及其概率分布。均衡决策不仅取决于某一手牌的强弱，还取决于整段范围中不同牌型之间如何共同分配行动频率，以避免被对手利用。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文研究不完全信息扩展式博弈中的“求解器策略表述”问题。输入是一个两人 $NLH$ 翻牌后决策点，包括公共牌、行动历史、底牌以及求解器给出的范围层面和手牌层面策略信息；输出是语言模型可读、可检查并能迁移到新状态的战略规则，以及模型依据这些规则生成的行动概率分布。设求解器提供接近均衡的目标分布，模型需要在相同信息集上尽可能复现各候选行动的完整概率，而非只预测最高频动作。本文假设商业扑克求解器能够查询任意牌局状态，并将其作为高质量但不直接提供文字解释的策略“预言机”；实验覆盖全部 $1{,}755$ 个 $NLH$ 翻牌及其转牌、河牌延续状态。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$NLH$**

无限注德州扑克，即本文用于实例化研究问题的两人扑克环境。

</div>
<div class="notation-item" markdown="1">

**$L_1$**

两个行动概率分布之间的 $4L_14$ 距离；它比较所有对应行动概率的绝对差之和，因此能衡量模型是否复现了完整混合策略，而不只关注一个最大概率行动。

</div>
<div class="notation-item" markdown="1">

**$D_{4\mathrm{task}4}$**

本文任务数据的概念性表示，即由求解器生成的决策状态、策略分布及其相关摘要组成的数据集合；给定该数据，模型学习或依据规则执行均衡推理。

</div>
<div class="notation-item" markdown="1">

**$s(x)\in\{\mathrm{task},\mathrm{harm}\}$**

本文背景材料未定义该符号；原文选段中没有使用这一表示，因此不能据此推断论文的具体含义。

</div>

</div>

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

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

该方法将求解器输出转化为可解释、可迁移的混合策略规则，再让下游大语言模型据此预测未展示目标手牌的策略分布。输入是决策历史 $h$、公共场景、目标手牌以及求解器产生的混合动作分布、动作价值和延续性摘要；MDT 将这些信息压缩为稀疏路由，SCCS 再通过同一公共场景下的反事实对比，把路由差异表述为自然语言规则。直观而言，方法不是教模型记住某一手牌该下注多少，而是先从大量求解器决策中提炼“哪些战略属性会改变选择”，再用相近但策略不同的手牌说明这条边界。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造求解器监督样本

从求解器查询大量决策点，并将公共牌、下注历史、位置、筹码和底池信息，与范围级及手牌级的延续性摘要组成紧凑特征 $\mathbf{x}$。摘要包括 EV、EQ 和可用行动线下的动作差值；原文摘要未明确报告完整特征维度或数据划分细节。

<div class="method-step__io" markdown="1">

**输入**：决策历史 $h$、公共状态、玩家私有手牌、范围信息，以及求解器输出的策略分布 $\pi^{*}(\cdot\mid h)$ 和动作价值 $Q^{*}(h,a)$。<br>
**输出**：带有求解器策略标签和动作价值标签的样本对象 $\mathcal{O}(h)=\bigl(\pi^{*}(\cdot\mid h),\{Q^{*}(h,a)\}_{a\in\mathcal{A}(h)},\mathbf{x}\bigr)$。

</div>

**直观理解**：求解器提供的是“每个动作应占多少概率”以及“各动作值多少钱”，而不是一句人类式解释。作者把牌面、下注线和隐藏牌范围等信息整理成模型可以使用的战略摘要。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 训练混合策略决策树 MDT

MDT 使用稀疏局部路由将输入送往多个叶节点，每个叶节点只存储一个纯动作 $a_l$；路径概率的乘积形成叶节点概率，再将指向同一动作的叶节点概率相加以恢复混合策略 $\hat{\pi}(a\mid\mathbf{x})$。训练同时优化策略频率拟合损失和求解器条件下的 EV 损失，并比较可微稀疏路由与逐步转为硬 Top-$K$ 的教师辅助方案。

<div class="method-step__io" markdown="1">

**输入**：战略摘要 $\mathbf{x}$、动作集合 $\mathcal{A}$、求解器策略 $\pi^{*}$ 和动作价值 $Q^{*}$。<br>
**输出**：一个将战略摘要映射为动作分布的稀疏 MDT，以及每个输入样本经过的路由和所使用的局部摘要。

</div>

**直观理解**：每个叶子像一个简单的“纯动作原型”，真正的混合概率来自不同叶子的分流比例。这样模型可以用多个简单条件共同产生下注、过牌等动作的频率，而不是在叶子中直接藏一个难以解释的完整概率表。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 场景约束反事实采样 SCCS

SCCS 搜索公共牌面和下注线相同、但求解器策略明显不同的影子手牌，并定位目标与影子手牌在 MDT 中发生分叉的关键节点。随后将分叉节点上的主动摘要差异转写为对比性自然语言规则；目标手牌的求解器策略不展示给下游预测器。

<div class="method-step__io" markdown="1">

**输入**：目标手牌的 MDT 路由、同一公共场景下的求解器查询集合 $\mathcal{D}$，以及目标与候选影子手牌的策略分布。<br>
**输出**：规则 $r=A(\mathcal{O}(h),\mathcal{D})$，其中包含能够区分目标手牌和影子手牌的局部战略条件。

</div>

**直观理解**：它不单独解释“这手牌为什么下注”，而是寻找同一牌面下“另一手相似但改为过牌”的牌，再比较两者在哪个属性上越过了策略边界。固定公共场景并只改变私有牌，有助于排除牌面和下注历史本身的干扰。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 遮蔽目标后的下游预测

下游预测器根据场景和目标手牌直接预测，或结合规则 $r$ 预测动作分布 $\tilde{\pi}(\cdot\mid h_{\mathrm{test}})$。将该分布与被遮蔽的求解器目标 $\pi^{*}(\cdot\mid h_{\mathrm{test}})$ 比较，以测试规则是否能迁移到未展示目标，而不是复述已显示标签。

<div class="method-step__io" markdown="1">

**输入**：公共场景、目标手牌，以及可选的 SCCS 规则 $r$；目标手牌的求解器策略被遮蔽。<br>
**输出**：目标状态上的预测混合策略，并以 $\ell_1$ 距离等指标评价其与求解器策略的接近程度。

</div>

**直观理解**：测试时模型看不到答案，只能使用牌面、目标手牌和提炼出的规则做判断。若规则有效，它应当帮助模型预测完整的下注频率分布，而不只是选出概率最大的一个动作。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### MDT 混合策略聚合

$$
\rho_{l}(\mathbf{x})=\prod_{(n,c)\in\mathrm{Path}(l)}p_{n,c}(\mathbf{x}),\qquad \hat{\pi}(a\mid\mathbf{x})=\sum_{l\in\mathcal{L}}\rho_{l}(\mathbf{x})\mathbf{1}[a_{l}=a]
$$

**符号说明**

- $\mathbf{x}$：公共上下文、范围信息、手牌信息和延续性摘要组成的输入特征。
- $\mathcal{L}$：MDT 的叶节点集合。
- $l$：一个叶节点。
- $\mathrm{Path}(l)$：从根节点到叶节点 $l$ 的路由分支集合。
- $p_{n,c}(\mathbf{x})$：在节点 $n$ 的分支 $c$ 上，输入 $\mathbf{x}$ 的路由概率。
- $\rho_l(\mathbf{x})$：输入到达叶节点 $l$ 的概率，即路径上各分支概率的乘积。
- $a_l$：叶节点 $l$ 存储的单一纯动作。
- $\mathbf{1}[a_l=a]$：指示函数；当叶节点动作等于 $a$ 时为 $1$，否则为 $0$。
- $\hat{\pi}(a\mid\mathbf{x})$：MDT 对动作 $a$ 输出的混合策略概率。

<div class="equation-explanation" markdown="1">

**直观理解**：该式说明 MDT 不把完整混合分布直接放进叶子，而是先计算输入到达各纯动作叶子的概率，再把相同动作叶子的概率相加。因而混合策略由路由结构产生，路由中使用的摘要也能作为解释依据。<br>
**原文位置**：第 5.1 节，公式（4）和（5）

</div>

</div>

<div class="equation-block" markdown="1">

#### MDT 训练目标

$$
\mathcal{L}_{\mathrm{task}}=\lambda_{\pi}\mathcal{L}_{L_{1}}+\lambda_{\mathrm{ev}}\mathcal{L}_{\mathrm{EV}},\qquad \mathcal{L}_{L_{1}}=\frac{1}{|\mathcal{A}|}\sum_{a\in\mathcal{A}}|\pi^{*}(a\mid h)-\hat{\pi}(a\mid h)|,\qquad \mathcal{L}_{\mathrm{EV}}=V^{*}(h)-\sum_{a\in\mathcal{A}}\hat{\pi}(a\mid h)Q^{*}(h,a),\qquad V^{*}(h)=\sum_{a\in\mathcal{A}}\pi^{*}(a\mid h)Q^{*}(h,a)
$$

**符号说明**

- $\mathcal{L}_{\mathrm{task}}$：MDT 的主要训练损失。
- $\lambda_{\pi},\lambda_{\mathrm{ev}}$：分别控制策略频率损失和 EV 损失权重的超参数；具体数值原文未明确报告。
- $\mathcal{L}_{L_{1}}$：预测动作分布与求解器动作分布之间的平均绝对差异。
- $\mathcal{L}_{\mathrm{EV}}$：求解器价值 $V^{*}(h)$ 与 MDT 策略在求解器动作价值下产生的期望价值之间的差距。
- $\pi^{*}(a\mid h)$：求解器在历史 $h$ 上选择动作 $a$ 的目标概率。
- $\hat{\pi}(a\mid h)$：MDT 在历史 $h$ 上预测动作 $a$ 的概率。
- $Q^{*}(h,a)$：求解器评估在 $h$ 采取动作 $a$ 的动作价值。
- $V^{*}(h)$：按照求解器目标策略加权后的状态价值。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项要求模型模仿求解器的完整动作频率，而不是只预测最大概率动作；第二项要求预测分布在求解器提供的动作价值下也保持高价值。作者明确说明 EV 项只是局部保真度指标，不等同于完整对局的可利用性或 exploitability。<br>
**原文位置**：第 5.1 节，公式（6）和（7）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标为 $\mathcal{L}_{\mathrm{task}}=\lambda_{\pi}\mathcal{L}_{L_{1}}+\lambda_{\mathrm{ev}}\mathcal{L}_{\mathrm{EV}}$。其中 $\mathcal{L}_{L_{1}}$ 直接拟合求解器的混合动作频率，$\mathcal{L}_{\mathrm{EV}}$ 则约束预测策略在求解器动作价值下的期望收益接近求解器价值；前者防止只学最大动作，后者防止频率拟合却产生战略上低价值的分布。另有可微稀疏训练目标 $\mathcal{L}_{\mathrm{soft}}$，加入权重 $\ell_1$ 正则、路由熵和正交损失；另一种训练策略采用稠密教师、结构化学生和硬 Top-$K$ 选择，最终每个节点保留 $K=5$ 个活动局部摘要。各损失权重和优化器配置原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 求解器监督与战略摘要**

求解器对象包含 $\pi^{*}(\cdot\mid h)$、每个合法动作的 $Q^{*}(h,a)$ 和特征向量 $\mathbf{x}$。$\mathbf{x}$ 汇总公共上下文、范围级与手牌级延续性信息，包括 EV、EQ 及动作差值，从而保留影响局部策略的隐藏状态和未来收益线索。

> 直观理解：这是方法的知识来源：求解器告诉模型平衡策略是什么，并提供解释策略差异所需的范围和未来收益信息。单纯的牌面或人类经验不足以表达这些隐藏信息。

**2. Mixed-Strategy Decision Tree**

对于叶节点 $l\in\mathcal{L}$，每条路径上的局部路由概率相乘得到 $\rho_l(\mathbf{x})$，叶节点仅保存纯动作 $a_l$。最终策略通过聚合所有动作相同的叶节点概率得到；最终模型采用硬稀疏局部路由，教师辅助课程将结构从稠密教师逐步压缩为每个节点 $K=5$ 个活动摘要。

> 直观理解：MDT 把复杂的混合策略拆成“多个简单动作由不同条件触发”，再用条件满足程度决定各动作获得多少概率。稀疏化减少无关摘要的影响，使展示出来的变量更接近实际决策依据。

**3. Scenario-Constrained Counterfactual Sampling**

SCCS 在相同公共场景中选择策略分布不同且 MDT 路由跨越关键分支的影子手牌，随后将目标与影子之间的主动摘要差异转化为规则。其目标是获得局部、对比性且可用于未见目标的中间表示，而非寻找视觉或词汇上最相似的手牌。

> 直观理解：SCCS 相当于制作一个受控对照实验：公共条件保持不变，只改变私有手牌，并观察哪一项战略属性导致动作频率变化。这样的规则比孤立的事后解释更容易迁移和检验。

**训练与推理**

训练阶段首先以求解器标注的决策点训练 MDT，使其从 $\mathbf{x}$ 预测完整策略分布并使用 $Q^{*}$ 计算 EV 约束；随后依据 MDT 路由和同一公共场景中的策略差异构造 SCCS 规则。推理阶段，对目标手牌 $h_{\mathrm{test}}$ 隐藏其求解器策略，SCCS 在求解器侧找到目标路由和影子手牌，但下游预测器只接收公共场景、目标手牌以及可选规则 $r$，输出 $\tilde{\pi}(\cdot\mid h_{\mathrm{test}})$，再与隐藏的 $\pi^{*}(\cdot\mid h_{\mathrm{test}})$ 比较。该设置检验的是规则能否帮助预测未展示目标，而不是模型能否复制展示过的策略标签。

**复现信息**

MDT 的最终形式使用硬稀疏局部路由；作者比较了可微路由与教师辅助的硬 Top-$K$ 路由，后者以 $K=5$ 个活动局部摘要为显式决策变量。SCCS 按照算法 $1$ 的思路筛选同一公共场景下策略分布不同、且 MDT 路由跨越关键分支的影子手牌；参考集合 $\mathcal{D}$ 可通过增加求解器状态、行动延续或私有手牌分配来扩展。所给章节未明确报告完整求解器查询采样规则、训练轮数、学习率、损失权重、模型具体架构、规则文本模板和数据划分，因此这些内容不能据此复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- NLH求解器标注数据：使用商业高端无限注德州扑克求解器生成超过$250$百万个翻牌后决策样本，包括约$16$百万个翻牌决策和$235$百万个转牌决策；配置为$6$人、$100$BB、无抽水，并覆盖两名玩家继续游戏的翻牌后局面。数据用于训练和评估策略蒸馏模型。
- 战略公共状态样本：从$1{,}755$种具有战略差异的翻牌牌面纹理中采样，并记录根节点、过牌线、下注线、下注后跟注线和连续下注线等动作节点；转牌数据由代表性翻牌分支扩展，并为每个分支采样$5$张转牌。该设置用于覆盖不同公共牌面和行动路径。
- 未见目标手牌的匹配上下文测试集：固定公共牌面和行动上下文，要求独立LLM预测未见目标手牌的求解器均衡混合策略；目标手牌不出现在规则展示的参考手牌或影子手牌中，且与每个展示手牌的求解器策略在动作平均$L_1$距离上至少相差$0.20$。该测试检验规则迁移，而不是近邻策略复制。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**$L_1$距离**

计算预测动作概率分布与求解器目标或蒸馏MDT策略之间的动作概率差异，衡量混合策略的整体分配是否接近参考策略。 （越低越好，因为较低距离表示预测的概率质量更接近均衡策略。）

</div>
<div class="metric-item" markdown="1">

**Oracle EV Gap**

在求解器提供的动作价值下，衡量蒸馏策略与求解器策略之间的局部期望价值差距；它反映局部策略保真度，而不是完整游戏中的可利用性或整体可剥削度。 （越低越好，因为更小的差距意味着策略选择造成的局部价值损失更小。）

</div>
<div class="metric-item" markdown="1">

**Argmax-action agreement**

判断LLM预测概率最高的动作是否与求解器概率最高的动作一致，主要衡量主导动作分类是否正确，而不完整反映其他动作上的概率分配。 （越高越好，因为更高比例表示模型更常选中求解器的主导动作。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 八种LLM配置上的未见目标手牌迁移

<div class="result-value" markdown="1">

相对于求解器目标，SCCS Rule将平均$L_1$距离从$0.211$降至$0.100$，相对改善$52.6\%$；相对于蒸馏MDT策略，距离从$0.204$降至$0.114$，相对改善$44.0\%$。

</div>

完整对比规则能显著改善LLM对混合动作概率的预测，并且效果同时出现在求解器目标和MDT目标上。这说明规则既帮助模型接近原始均衡，也帮助它复现可解释的蒸馏策略；但该结果只证明局部、匹配公共上下文中的策略迁移，不证明LLM已经成为能够独立运行的完整扑克智能体。

<div class="result-source" markdown="1">

来源：第6.3节，表2前

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across eight LLM configurations, SCCS rules reduce average L1 to the solver target from 0.211 to 0.100, a 52.6% relative improvement over direct prompting.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 主导动作和剩余概率分配

<div class="result-value" markdown="1">

Direct条件到SCCS Rule条件的Argmax-action agreement从$57.2\%$升至$76.1\%$。在三种条件都选中求解器主导动作的后验匹配诊断中，SCCS相对Route-only对求解器目标的$L_1$距离仍降低$38.8\%$，对MDT目标仍降低$33.0\%$。

</div>

规则的作用不只是把模型从错误的最大概率动作纠正到正确动作；即使最大动作已经正确，SCCS仍能改善Call、Fold、Raise等动作之间的概率比例。因此，它传达的是动作概率如何跨越局部战略边界移动，而不仅是一个动作标签。

<div class="result-source" markdown="1">

来源：第6.3节，表2后

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In a post-hoc matched diagnostic restricted to predictions where Direct, Route-only, and SCCS all select the correct solver argmax, SCCS still lowers Route-only L1 by 38.8% to the solver and 33.0% to MDT.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### MDT的求解器策略蒸馏保真度

<div class="result-value" markdown="1">

最终硬MDT的$L_1$损失为$0.087\pm0.007$，Oracle EV Gap为$0.44\pm0.04\%$；在树学生模型中，Dense-router tree的对应结果为$0.031\pm0.004$和$0.12\pm0.03\%$，Soft-sparse tree为$0.057\pm0.005$和$0.21\pm0.02\%$。

</div>

树结构能够以较少参数表示求解器策略中的层级条件，但为了让规则足够稀疏、便于语言表达，最终硬MDT牺牲了一部分数值保真度。该结果支持MDT作为解释和沟通层，而不意味着它在所有局面都等价于原始求解器。

<div class="result-source" markdown="1">

来源：表1，Final hard MDT行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Final hard MDT 0.087±0.007 0.44±0.04% top-k/node mask; ∼0.7K

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评估主要集中于NLH的局部翻牌后决策和匹配公共上下文中的未见手牌迁移；原文未明确报告完整对局收益、整体可剥削度或与人类玩家直接对局的结果。
- SCCS依赖求解器生成的规则、动作价值和匹配影子手牌，且实验使用商业高端求解器；因此其效果可能依赖求解器抽象、数据覆盖范围和规则构造方式，跨游戏的可迁移性虽由Liar's Dice实验提及，但所给章节未提供该实验的具体数据。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Direct：只向LLM提供公共状态和目标手牌，代表没有求解器辅助的直接提示基线，用于衡量模型自身的扑克推理能力。
- Direct+Summaries：在Direct基础上加入数值化战略摘要，用于测试原始求解器数量是否已经足以帮助LLM决策。
- Route-only：展示目标手牌在MDT中的路由轨迹，但删除参考手牌、影子手牌和跨手牌比较，用于隔离树结构计算路径本身的贡献。
- SCCS Rule：加入由策略分歧影子手牌提取的对比规则，是完整方法；其与Route-only的差异用于判断对比性战略解释是否带来额外收益。

**实验想回答的问题**

- Mixed-Strategy Decision Tree（MDT）能否将求解器输出转化为可理解的策略规则，并改善独立大语言模型对均衡混合策略的预测？
- 从策略分歧的影子手牌中提取的对比规则，是否能帮助模型在相同公共牌面下，将求解器知识迁移到未见过的目标手牌？

**实验实现**

实验分为两部分。第一部分比较不同表示和模型结构对求解器策略的蒸馏能力，包括原始PBS输入、战略摘要、树学生模型以及最终硬稀疏MDT；训练和评估使用求解器标注的NLH数据。第二部分在匹配公共上下文中测试$8$种LLM配置，分别使用Direct、Direct+Summaries、Route-only和SCCS Rule四种提示条件。每个测试要求模型为未见目标手牌输出动作概率混合，并分别计算其到求解器策略和MDT策略的$L_1$距离。SCCS规则不能直接显示目标手牌的求解器标签，也不能包含策略近似的展示手牌，因此测试重点是从局部对比规则中迁移战略区别。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Route-only相对于SCCS Rule | 相对于求解器目标，Route-only的平均$L_1$距离为$0.173$，SCCS Rule为$0.100$，降低$42.2\%$；相对于MDT目标，Route-only为$0.172$，SCCS Rule为$0.114$，降低$33.7\%$。 | Route-only保留了目标手牌经过MDT的树计算路径，因此可以测试树路由是否本身足够。完整SCCS进一步加入策略分歧影子手牌的对比后仍明显更好，说明跨手牌的反事实对比是独立且决定性的贡献。 | 第6.3节，表2前<br><span class="experiment-evidence">SCCS also improves on Route-only: L1 falls from 0.173 to 0.100 relative to the solver and from 0.172 to 0.114 relative to MDT, reductions of 42.2% and 33.7%, respectively.</span> |
| Direct+Summaries负控制 | Direct+Summaries相对于求解器目标的平均$L_1$距离为$0.256$，高于Direct的$0.211$。 | 额外提供求解器数值摘要并未自动改善决策，反而使平均距离变大。这表明问题不是信息数量不足，而是LLM缺少判断哪些摘要变化会改变当前公共上下文下的策略边界；SCCS通过组织成对比规则解决了部分可沟通性问题。 | 第6.3节，表2前<br><span class="experiment-evidence">Direct+Summaries has worse average L1 to the solver target (0.256) than the direct prompt, suggesting that raw continuation quantities are not automatically communicable to an LLM.</span> |

**定性案例**

- 在SB对BB单次加注底池、公共牌$8s6h5d$、行动为下注后加注的案例中，目标手牌$Td9c$属于同花顺听牌之外的卡顺听牌。Direct提示主要选择Fold，而求解器不给Fold概率，并在Call与Raise之间混合。SCCS将其与同一听牌类别但更弱的折牌原型$Jc4c$对比，突出继续牌在听牌强度、手牌期望价值和相对于整个范围的权益上的差异，使LLM把$Td9c$识别为带有一定激进加注频率的继续型听牌。该案例说明，对立即底池赔率的保守启发式可能忽略深筹码下保留坚果牌范围和后续牌面权益的价值；它是机制示例，不足以单独证明整体性能提升。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The contribution elicits equilibrium game reasoning in LLMs using solver-generated mixed-strategy decision rules.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`c80a931b5d964fb54dcc7f670433c11200b0131561e87ca87d87bed2e8507456`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
