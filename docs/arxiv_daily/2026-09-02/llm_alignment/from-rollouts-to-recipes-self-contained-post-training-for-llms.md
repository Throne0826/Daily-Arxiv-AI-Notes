---
title: "[论文解读] From Rollouts to Recipes: Self-Contained Post-Training for LLMs"
description: "[arXiv 2609.01422][对齐 / RLHF] 本文将大模型自身生成结果所反映的样本级学习状态，转化为对强化学习、在策略自蒸馏、保守正则化或暂时跳过的动态选择，以替代对全部样本使用统一训练方案。"
arxiv_id: "2609.01422"
announcement_date: "2026-09-02"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:38:51.009786+00:00"
source_sha256: "2a8c463350fae94ca031e7aa4f3a8f9806d80befdc175f19535568de541a7b6a"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型后训练"
  - "基于验证器的强化学习"
  - "行为条件路由"
  - "在策略生成轨迹"
  - "在策略自蒸馏"
  - "数学推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2609.01422</p>

# From Rollouts to Recipes: Self-Contained Post-Training for LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Yifei Li, Lingling Zhang, Muye Huang, Zihan Ma, Jiashuai Liu, Jun Liu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: School of Computer Science and Technology, Xi’an Jiaotong University, China；Affiliation: Shaanxi Province Key Laboratory of Big Data Knowledge Engineering；Affiliation: Zhongguancun Academy, Beijing, China；Affiliation: National Engineering Research Center for Visual Information and Applications</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.01422v1) · [PDF 下载](https://arxiv.org/pdf/2609.01422v1) · **关键词** 大语言模型后训练, 基于验证器的强化学习, 行为条件路由, 在策略生成轨迹, 在策略自蒸馏, 数学推理<br>


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

本文将大模型自身生成结果所反映的样本级学习状态，转化为对强化学习、在策略自蒸馏、保守正则化或暂时跳过的动态选择，以替代对全部样本使用统一训练方案。

**不用术语来说**：同一个模型面对不同题目时，可能处于完全不会、时对时错、已经稳定掌握或自信地答错等不同状态；如果训练时不加区分地用同一种方式处理所有题目，就可能在缺少有效信号的样本上徒劳更新，或破坏已经形成的正确能力。本文要解决的是：能否直接依据模型当前多次作答的表现，为每个样本选择更合适的训练方式，而不依赖外部教师、新标注或额外生成。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 指出验证器驱动后训练中的结构性缺口：样本的训练价值取决于当前模型的生成行为及所施加的优化信号，不能仅被视为固定的质量或难度属性。
- 提出自包含的行为条件路由视角，利用训练过程中自然产生的正确性与置信度信号，为每个样本动态分配训练动作，并以实验说明不同生成行为状态适合不同优化机制。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型在可验证任务上的后训练研究。数学推理、代码生成和程序修复等任务可以通过答案正确性、测试通过率或补丁有效性给出结果奖励，因此无需大规模思维链标注或人工过程监督，也能利用基于验证器的强化学习改进模型。现有方法通常对全部样本统一采用一种优化目标或固定比例的混合目标，但同一模型对不同样本可能处于不同学习状态：有的样本生成结果有对有错，有的始终正确或始终错误，还有的虽然失败却表现出很高置信度。本文研究如何直接利用当前模型生成轨迹中自然出现的正确性与置信度信号，为每个样本选择合适的训练方式。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**基于验证器的强化学习**

验证器根据最终答案或执行结果是否正确提供奖励，模型据此提高高奖励输出的概率。它不要求逐步标注推理过程，但结果奖励通常较稀疏，某些样本可能无法产生有效的相对优势信号。

</div>
<div class="concept-item" markdown="1">

**在策略生成轨迹**

生成轨迹是模型针对一个提示生成的完整响应；“在策略”表示这些响应由当前正在训练的模型产生。它们反映模型此刻实际访问的生成状态，因而比外部教师或固定离线轨迹更贴近当前策略分布。

</div>
<div class="concept-item" markdown="1">

**在策略自蒸馏**

在策略自蒸馏使用模型自身或其历史版本产生的信号，为当前模型提供比二元结果奖励更密集的监督。由于教师信号与学生模型的推理风格、长度偏好和生成分布较接近，它可缓解外部教师带来的分布不匹配。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

训练对象是可生成推理过程与最终答案的大语言模型，任务样本包含可由验证器判定结果正确性的提示。对每个已采样提示，当前策略生成一组在策略轨迹；系统从验证结果和模型置信度中估计样本级行为状态，再决定该样本应接受基于相对奖励的强化学习、在策略自蒸馏、保守正则化，还是暂时跳过。各路由队列的损失随后被汇总以更新同一模型。该设定假设结果可自动验证，并强调不使用外部教师、额外人工标注或额外采样；输出不是推理阶段的答案选择，而是每个样本对应的训练动作及由此更新后的模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **PPO、GRPO、DAPO 等基于验证器的强化学习目标**: 这些方法主要改进奖励塑形、优势估计、KL 正则化、采样与训练稳定性，但一般仍把同一种全局机制应用于所有样本。本文不再提出一个统一的强化学习目标，而是根据样本当前的轨迹行为，在不同训练动作之间进行路由。
- **全正确／全错误过滤与课程学习**: 这类方法依据正确率、难度、不确定性或训练阶段决定哪些样本进入训练以及训练顺序；其中，全正确或全错误的轨迹组因缺少相对优势信号而常被跳过或降权。本文研究的是互补问题：一个提示及其轨迹已经被采样后，应对它施加哪一种优化信号，而不只是决定是否训练该样本。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

数学推理、代码生成和程序修复等任务可以用答案正确性、测试通过率或补丁有效性自动验证，因此适合在缺少高质量思维链监督时采用验证器强化学习。然而，模型对各样本的掌握程度并不一致，而且会随训练变化：统一目标可能让无有效相对奖励信号的样本产生低价值更新，也可能对已经稳定解决的样本进行不必要甚至过强的更新。实际需求因而不是简单增加训练数据，而是在现有生成预算内提高每个样本所获得优化信号的适配性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **统一或固定混合的后训练方案**：对数据集中所有样本统一采用验证器强化学习、在策略自蒸馏等单一机制，或按预先设定且不随样本状态变化的比例混合多个目标。此类方案改进了奖励、优势估计、正则化或蒸馏方式，但样本到目标的分配规则基本固定。
- **基于生成行为的筛选、课程安排与推理时选择**：利用多次生成的正确性、熵、置信度或一致性来过滤全对或全错样本、调整训练顺序，或者在推理阶段通过投票和重排序选择答案。这些方法主要决定哪些样本进入训练、何时训练或最终采用哪个答案，而不是针对不同样本选择不同的参数更新机制。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 统一目标或固定混合忽略样本级学习状态的异质性：全错样本通常缺少供相对优势学习使用的差异信号，混合正误的样本却可能很适合强化学习，已经稳定答对的样本则更需要保守更新；一刀切处理会浪费更新并可能扰动已掌握能力。
- 现有行为感知方法多把生成信号用于过滤、课程调度或推理选择，尚未充分回答“如何优化该样本”；而依赖外部教师、离线思维链或固定参考轨迹的蒸馏还可能使被模仿轨迹与当前策略实际访问的状态分布不匹配。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究表明模型生成结果能够揭示样本是否提供有效学习信号，但缺少一个统一、自包含的机制，把这些训练时已产生的行为信息进一步映射为样本级优化方案。尤其尚未系统验证：在不增加标注、外部评估器、教师模型或额外采样的条件下，是否可以依据当前策略的正确性与置信度，在多种更新机制之间动态路由，并随模型学习进程改变路由分布。

</div>
<div markdown="1"><span>核心问题</span>

当前模型在某一样本上的多次生成行为，能否可靠地决定该样本此刻应采用验证器强化学习、在策略自蒸馏、保守正则化还是暂时跳过，从而优于对所有样本使用统一目标、固定混合或仅做筛选与课程安排？

</div>
<div markdown="1"><span>作者直觉</span>

多次生成相当于对模型当前掌握状态的一次低成本体检：有对有错说明答案之间存在可比较的奖励差异，适合用强化学习强化成功行为；全部失败时，稀疏的正确性奖励难以提供方向，但模型在自身访问状态上的软分布仍可形成较密集的自蒸馏信号；稳定答对时，重点应是维持能力而非大幅改变参数；若模型高置信地反复失败，现有信号可能不足以纠正它，暂时跳过可避免低收益更新。由于这些判断直接来自本轮在策略生成，它们会随训练自动变化，也较少受到外部轨迹分布不匹配的影响。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Self-Routing 面向验证器可判定的后训练任务，在固定训练集 $\mathcal{D}=\{x_j\}_{j=1}^{N}$ 上，根据当前策略对每个样本生成的回答表现，动态选择 GRPO、在线策略自蒸馏（OPSD）、正则化（REG）或跳过（SKIP）四种训练配方。其输入是训练样本、当前策略 $\pi_{\theta}$、二值验证器 $R$、每个样本的 $G$ 个采样回答，以及可选的参考策略 $\pi_{\mathrm{ref}}$；输出是更新后的策略 $\pi_{\theta}$。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 采样回答并验证

对每个 $x\in\mathcal{B}$ 生成 $G$ 个在策略回答 $o_i\sim\pi_{\theta}(\cdot\mid x)$，并计算二值结果 $r_i=R(o_i,x)\in\{0,1\}$。随后以 $a_x=\frac{1}{G}\sum_{i=1}^{G}r_i$ 汇总该样本的经验正确率。

<div class="method-step__io" markdown="1">

**输入**：小批量样本 $\mathcal{B}\subset\mathcal{D}$、当前策略 $\pi_{\theta}$、每个样本的采样数 $G$ 和验证器 $R$。<br>
**输出**：每个样本的回答集合 $\{o_i\}_{i=1}^{G}$、验证结果 $\{r_i\}_{i=1}^{G}$ 和经验正确率 $a_x$。

</div>

**直观理解**：模型先对同一道题尝试多次，再由自动判题器检查答案。多次尝试的正确比例反映模型对该样本究竟是几乎不会、时好时坏，还是已经稳定掌握。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 构造行为状态

将 $a_x$ 映射为低正确率、不确定和高正确率三个平滑隶属度，得到 $\omega(a_x)=[l,m,h]$。同时根据逐词预测熵计算回答置信度，并在当前批次内校准，形成置信度特征 $\varphi(c_x)=(\widetilde{c},\widetilde{c}^{+},\widetilde{c}^{-},\widetilde{\Delta c})$，最终得到行为状态 $b_x=(\omega(a_x),\varphi(c_x))$。

<div class="method-step__io" markdown="1">

**输入**：每个样本的经验正确率 $a_x$ 和回答中的逐词预测分布。<br>
**输出**：每个样本的行为状态 $b_x$，其中包含正确性结构和置信度、置信度倾向及相对批次均值的偏差。

</div>

**直观理解**：系统不只看“答对了多少次”，还看模型是否自信以及这种自信是否高于同批次其他样本。平滑划分可以避免一次随机采样就让样本突然跨过硬阈值。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 路由到训练配方

根据正确率分量与置信度特征计算 $s_{\mathrm{GRPO}}$、$s_{\mathrm{OPSD}}$、$s_{\mathrm{REG}}$ 和 $s_{\mathrm{SKIP}}$，再归一化为配方分布 $p_x=[p_{\mathrm{GRPO}},p_{\mathrm{OPSD}},p_{\mathrm{REG}},p_{\mathrm{SKIP}}]$，并采样 $t_x\sim\mathrm{Categorical}(p_x)$。每个样本在一次迭代中只进入一个互斥队列：$\mathcal{B}_g$、$\mathcal{B}_o$、$\mathcal{B}_r$ 或 $\mathcal{B}_s$。

<div class="method-step__io" markdown="1">

**输入**：行为状态 $b_x$ 以及由其计算的四个路由分数。<br>
**输出**：四个互斥样本队列及其规模 $n_g,n_o,n_r,n_s$。

</div>

**直观理解**：路由器像一个按样本状态分流的调度器：表现不稳定的题目更适合奖励优化，低正确率且低置信度的题目更适合模仿带答案的轨迹，已经稳定的题目只做保守约束，低信号题目则暂时不更新。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 按队列优化策略

在 $\mathcal{B}_g$ 上计算标准 GRPO 损失，在 $\mathcal{B}_o$ 上计算 OPSD 的逐词交叉熵，在 $\mathcal{B}_r$ 上计算当前策略相对于 $\pi_{\mathrm{ref}}$ 的 KL 正则，在 $\mathcal{B}_s$ 上令损失为零。仅对前三个活动队列按样本数加权聚合损失，并反向传播更新 $\pi_{\theta}$。

<div class="method-step__io" markdown="1">

**输入**：四个队列、对应的在策略回答、OPSD 教师轨迹和参考策略。<br>
**输出**：下一训练步的策略参数和更新后的模型；SKIP 样本不产生梯度。

</div>

**直观理解**：同一批题目可以采用不同的学习方式，而不是强迫所有题目使用同一种算法。跳过并非删除数据，而是在当前模型状态下暂不让该样本影响参数。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 样本经验正确率

$$
a_x=\frac{1}{G}\sum_{i=1}^{G}R(o_i,x)
$$

**符号说明**

- $x$：训练样本，即提示、问题或指令输入
- $G$：每个样本生成的在策略回答数量
- $o_i$：第 $i$ 个模型回答
- $R(o_i,x)$：验证器对回答是否正确的二值判定，正确为 $1$，否则为 $0$
- $a_x$：当前策略在样本 $x$ 上多次采样的平均正确率

<div class="equation-explanation" markdown="1">

**直观理解**：该式统计模型对同一输入重复作答时的成功比例。它不是单次奖励，而是样本级学习状态信号：数值低表示大多失败，接近中间值表示行为不稳定，接近 $1$ 表示已经较稳定。<br>
**原文位置**：第 3.2 节 Rollout Collection；附录 A 算法第 7 行

</div>

</div>

<div class="equation-block" markdown="1">

#### 四类配方的最终聚合损失

$$
\mathcal{L}=\frac{n_g\mathcal{L}_{\mathrm{GRPO}}+n_o\mathcal{L}_{\mathrm{OPSD}}+n_r\mathcal{L}_{\mathrm{REG}}}{n_g+n_o+n_r}
$$

**符号说明**

- $\mathcal{L}$：当前训练批次用于反向传播的总损失
- $\mathcal{L}_{\mathrm{GRPO}}$：对 GRPO 队列执行基于组内相对优势和裁剪策略比率的强化学习损失
- $\mathcal{L}_{\mathrm{OPSD}}$：对 OPSD 队列执行的教师轨迹逐词模仿损失
- $\mathcal{L}_{\mathrm{REG}}$：对 REG 队列约束当前策略接近参考策略的 KL 散度损失
- $n_g,n_o,n_r$：GRPO、OPSD 和 REG 队列中的样本数

<div class="equation-explanation" markdown="1">

**直观理解**：总损失只聚合三个活动队列，并按各队列样本数加权；SKIP 队列不进入分子，也不进入分母。这样每个样本只接受一种配方的梯度，同时避免被跳过样本稀释活动样本的平均损失。<br>
**原文位置**：第 3.5 节 Recipe Assignment and Policy Update；附录 A 算法第 19 行

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标是使当前策略在不同样本状态下选择更合适的更新机制，而不是统一最小化单一损失。GRPO 队列使用奖励驱动的裁剪策略优化，令成功回答相对组均值获得正向优势；OPSD 队列使用同一基础模型在给定标准答案条件下生成的一次教师轨迹进行逐词监督；REG 队列最小化 $D_{\mathrm{KL}}(\pi_{\theta}(\cdot\mid x)\|\pi_{\mathrm{ref}}(\cdot\mid x))$ 以抑制已经稳定样本上的策略漂移；SKIP 队列不产生梯度。训练因此同时追求能力提升、纠正低置信度失败、保持稳定行为和减少低信号更新。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 正确率分解模块**

经验正确率 $a_x$ 被映射为以 $0$、$0.5$ 和 $1$ 为中心的三个高斯型隶属度 $l_x,m_x,h_x$，再归一化为 $\omega(a_x)=[l,m,h]$。实现中固定 $\sigma_l=\sigma_h=0.18$、$\sigma_m=0.16$，不按数据集调节。

> 直观理解：它把“模型答题状态”从一个生硬的分数变成三个有重叠的状态比例，因此采样噪声不会轻易改变路由结果。

**2. 熵置信度校准模块**

对回答每个位置的预测分布计算熵 $H_{i,t}$，取序列平均熵 $\bar{H}(o_i,x)$，经当前批次归一化后用 $1-\mathrm{Norm}_{\mathcal{B}}(\bar{H})$ 转换为回答置信度，再对 $G$ 个回答求均值得到 $c_x$，并计算相对批次均值的偏差 $\Delta c_x$。

> 直观理解：预测分布越集中，模型越自信；但不同题目和批次的熵尺度可能不同，所以系统只比较同一批次中的相对置信度。

**3. 可解释配方路由器**

路由器以正确率分解和置信度特征计算四个分数：$s_{\mathrm{GRPO}}=m+h(1-\widetilde{\Delta c})+l(1-\widetilde{c}^{-})\cdot\widetilde{c}$，$s_{\mathrm{OPSD}}=l(1-\widetilde{c}^{-})$，$s_{\mathrm{REG}}=h\cdot\widetilde{\Delta c}\cdot\widetilde{c}^{+}$，$s_{\mathrm{SKIP}}=l\cdot\widetilde{c}^{-}\cdot\widetilde{c}$。分数经 $p_{x,k}=s_k/(\sum_j s_j+\epsilon)$ 转为概率后进行分类采样。

> 直观理解：该模块不是训练一个难以解释的额外网络，而是用明确规则把不同学习状态对应到不同配方。这样既能利用多种优化器的优势，也能分析每个样本为何被分流。

**训练与推理**

训练从初始策略 $\pi_{\theta_0}$ 开始，循环执行以下过程：从 $\mathcal{D}$ 采样小批量，生成共享的在策略回答并由 $R$ 评分；计算 $a_x$、熵置信度及行为状态 $b_x$；根据四个路由分数抽样配方并划分队列；分别计算 GRPO、OPSD 和 REG 损失，跳过 SKIP 样本；按最终损失更新策略。OPSD 教师轨迹在离线预处理中由同一基础模型结合问题和标准答案生成一次，训练期间重复使用，因此不需要外部教师或额外思维链标注，但需要可获得目标答案的可验证后训练场景。推理阶段不执行路由、验证或多配方更新，而是直接使用训练完成的策略生成回答；原文未明确报告额外的推理时搜索或采样流程。

**复现信息**

实验将路由模块置于 rollout 收集与损失构造之间，GRPO、Naive-GRPO、Naive-OPSD 和 Self-Routing 共用数据加载器、rollout 接口、验证器、分词器和检查点流程。训练使用 ms-swift、PyTorch 及 Hugging Face 兼容的模型和分词器接口，在单节点 8 张 NVIDIA A100 GPU 上运行；这些是公平比较所需的执行条件，而不是方法本身。数学任务的验证器提取最终答案并与标准答案比较，且同一验证机制同时用于 rollout 打分、GRPO 奖励和评测正确性。REG 使用固定参考策略，但摘录同时说明参考策略可以是初始模型、当前更新前的旧策略或脚本指定检查点，具体运行配置原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- DAPO-Math-17K：所有后训练方法共用的数学训练集。每个提示可生成多个 rollout，模型根据这些回答的正确率和置信度判断样本当前的学习状态；原文节选未明确报告训练集划分、题目长度或清洗细节。
- 数学领域内评测组：GSM8K、MATH-500、AIME24 和 AIME25，分别覆盖小学算术、一般竞赛数学和近期高难度考试题。该组用于检验后训练是否真正增强目标领域的数学推理，而不是只改善训练目标。
- 领域外评测组：GPQA-diamond 与 MMLU-Pro，用于检查数学后训练向更广泛推理任务的迁移，以及模型是否因过度数学专门化而损失原有通用能力；附录还以 SATBench、AutoLogi、LiveCodeBench-v5 的均值构成 OOD-V 补充评测。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**六基准宏平均分**

先分别计算 GSM8K、MATH-500、AIME24、AIME25、GPQA-diamond、MMLU-Pro 的任务得分，再对六项等权平均，用于概括目标数学能力与领域外迁移的综合表现；节选未明确各单项得分的具体解码和判分协议。 （越高越好，因为它表示模型在六个基准上的平均任务表现更强，但宏平均可能掩盖某个单项明显下降。）

</div>
<div class="metric-item" markdown="1">

**ID Math、OOD-V 与 General 分组分数**

ID Math 概括领域内数学评测；OOD-V 在附录中定义为 SATBench、AutoLogi、LiveCodeBench-v5 的平均分；General 用于表示通用评测表现，但所给节选未完整给出其精确定义。 （越高越好；分组报告可区分数学能力提升、可验证领域外迁移和通用能力保持，避免只看单一总平均。）

</div>
<div class="metric-item" markdown="1">

**归一化训练 FLOPs**

以 $NTBL$ 为归一化单位估算训练计算量，其中 $N$ 是参数量、$T$ 是训练步数、$B$ 是批大小、$L$ 是平均序列长度；前向每 token 约需 $2N$ FLOPs，含前向与反向的训练过程约需 $6N$ FLOPs。该指标忽略序列长度变化、通信与实现开销。 （在性能相近时越低越好，因为它表示理论计算需求较少；但它不是实测墙钟时间，不能直接证明训练更快。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3-4B 的六基准宏平均比较

<div class="result-value" markdown="1">

Self-Routing 将平均分由基础模型的 61.0 提高到 73.7，并分别超过 Naive-GRPO 和 Naive-OPSD 6.9 分与 3.3 分。

</div>

作者据此主张：在较强的 Qwen3-4B 上，根据样本行为选择不同训练配方优于统一使用 GRPO 或 OPSD。分析上，这一结果支持“路由规则具有额外价值”，但不能单独确定收益来自哪一个路由信号，也不能证明所有单项任务都同幅度提高；此外，节选没有给出重复实验误差。

<div class="result-source" markdown="1">

来源：Section 4.2, Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For example, on Qwen3-4B, Self-Routing improves the average score from 61.0 to 73.7, exceeding Naive-GRPO and Naive-OPSD by 6.9 and 3.3 points, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3.5-4B 上与两种统一配方的比较

<div class="result-value" markdown="1">

Self-Routing 的平均分为 86.6，高于 Naive-GRPO 的 79.8 和 Naive-OPSD 的 83.0，即分别领先 6.8 分和 3.6 分。

</div>

该结果表明优势不仅出现在 Qwen3 系列，也延续到更新且较强的 Qwen3.5-4B；同时 OPSD 已优于 GRPO，Self-Routing 仍进一步提高分数，说明结果不只是简单地用自蒸馏替换强化学习。不过这里只能说明该骨干和实验设置下的相关优势，不能据此断言模型越大时收益必然单调增加。

<div class="result-source" markdown="1">

来源：Section 4.2, Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Qwen3.5-4B, Self-Routing reaches 86.6 average score, compared with 79.8 for Naive-GRPO and 83.0 for Naive-OPSD.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 当每个样本生成 $G=8$ 个 rollout 时的理论计算成本

<div class="result-value" markdown="1">

归一化成本分别为 Naive-GRPO 64.0、Naive-OPSD 24.0、Self-Routing 34.7；因此 Self-Routing 比全量 GRPO 少 29.3 个归一化单位，但比统一 OPSD 多 10.7。

</div>

实验支持的效率结论是“选择性分配昂贵更新”，而不是“当前实现最快”：Self-Routing 保留多 rollout 状态估计，并只对部分样本采用 GRPO，所以成本位于两种统一配方之间。该估算忽略硬件通信、不同序列长度和路由实现开销，因而不能等同于实测训练时长或能源消耗。

<div class="result-source" markdown="1">

来源：Section 4.3, Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

When G=8, the normalized costs are 64.0 for Naive-GRPO, 24.0 for Naive-OPSD, and 34.7 for Self-Routing.

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

- Base：未经后训练的基础模型，用于衡量各训练方法带来的净变化，并检查数学后训练是否损害通用任务能力。
- Naive-GRPO：对所有训练样本统一应用 GRPO。它检验按样本路由是否优于单一的强化学习式全局配方。
- Naive-OPSD：对所有样本统一应用 on-policy self-distillation。它检验路由收益是否只是因为使用了自蒸馏，而非依据行为状态选择训练目标。
- 路由与强化学习对照组：包括逐轮随机路由、固定比例随机路由、仅按准确率路由，以及附录中的 DAPO-style RL 和 PODS。前几项在相同配方集合下隔离“如何分流”的作用；后两项分别代表稳定化强化学习和 rollout 选择方法。

**实验想回答的问题**

- 相较于对全部样本统一使用 GRPO、OPSD 或固定配方混合，依据模型自身 rollout 正确率与置信度进行行为条件路由，能否在不同规模、不同代际的 Qwen 模型上稳定提高数学推理及总体评测表现？
- 这种路由是否能把计算量较大的更新集中到训练信号更有价值的样本上；其收益是否确实来自正确率、校准后的置信度、行为到配方的分配以及 REG/SKIP 保守分支，而非随机或简单阈值式分流？

**实验实现**

实验覆盖 Qwen3-0.6B、1.7B、4B，以及 Qwen3.5-0.8B、2B、4B，用于检验路由能否跨模型代际与容量工作。所有方法使用同一 ms-swift 后训练框架，在单节点 8 张 NVIDIA A100 GPU 上运行，并通过兼容 Hugging Face Transformers 的模型和 tokenizer API 实现；Naive-GRPO、Naive-OPSD、各路由基线和 Self-Routing 使用相同运行栈，且不使用外部奖励模型或额外标注。总体分数是六个主评测基准的宏平均。计算分析设 rollout 数为 $G$，在 $G=8$ 时比较归一化 FLOPs；Self-Routing 的分支占比由 Figure 4 路由曲线积分得到，而非额外采样。原文节选没有明确报告随机种子、重复运行次数、方差、置信区间及统计显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除一个路由信号：仅使用准确率或仅使用置信度，Qwen3-4B | 完整 Self-Routing 的 ID Math/OOD-V/General 为 80.9/71.1/59.3；Accuracy-only 为 79.6/70.4/58.1，而 Confidence-only 降至 74.2/67.6/54.8。相对完整方法，仅准确率分别下降 1.3/0.7/1.2 分，仅置信度分别下降 6.7/3.5/4.5 分。 | 该消融隔离两类路由依据的贡献。准确率单独使用时较接近完整方法，说明它是更强的主信号；仅用置信度明显更差，说明置信度不能替代 rollout 正确率。与此同时，完整方法仍优于 Accuracy-only，支持置信度提供互补信息，但由于没有误差条或显著性检验，较小差值的稳定性仍需复核。 | Appendix I, Table 4<br><span class="experiment-evidence">Self-Routing \| 80.9 \| 71.1 \| 59.3; Accuracy-only \| 79.6 \| 70.4 \| 58.1; Confidence-only \| 74.2 \| 67.6 \| 54.8</span> |
| 移除置信度校准、行为条件分配或保守 REG/SKIP 分支，Qwen3-4B | 相较完整方法的 80.9/71.1/59.3，去除置信度校准得到 79.0/70.0/57.2，去除行为分配得到 77.8/69.0/56.4，去除 REG/SKIP 得到 79.1/70.3/56.9；三个变体在 ID Math、OOD-V、General 上均下降。 | 这组消融分别测试置信度数值是否需要校准、行为状态是否必须对应特定配方，以及对低信号或已稳定样本采取正则化/跳过是否必要。去除行为分配造成最大 ID Math 降幅，直接支持“配方应匹配行为状态”；去除 REG/SKIP 后 General 下降较明显，则说明保守分支可能有助于减少无谓更新和通用能力漂移，但仍不能仅凭该表确认具体因果机制。 | Appendix I, Table 4<br><span class="experiment-evidence">w/o conf. calibration \| 79.0 \| 70.0 \| 57.2; w/o behavior assignment \| 77.8 \| 69.0 \| 56.4; w/o REG/SKIP \| 79.1 \| 70.3 \| 56.9</span> |

**定性案例**

- 附录 H 给出行为到配方映射的定量诊断，而非单题案例：在 Qwen3-4B 上，每个 DAPO-Math-17K 提示采样 8 个 rollout，并以正确率 $a$ 与归一化置信度 $c$ 构造各占 50% 的行为子集。混合正确性子集按 $a(1-a)$ 选取，GRPO 得到 76.2/55.8，略高于 OPSD 的 75.5/55.5；可恢复低置信失败子集按 $(1-a)(1-c)$ 选取，OPSD 的 76.9/56.1 高于 GRPO 的 71.8/53.7。直观上，前者拥有同组正确与错误回答，可供 GRPO 比较奖励；后者缺少稳定奖励对比，更适合从自身较可信输出中蒸馏。作者明确把该路由器视为可解释的经验设计，而非理论最优分配。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出依据模型 rollout 行为自适应路由 GRPO、自蒸馏和正则化的 LLM 后训练方法，并以数学推理作为主要验证任务。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`2a8c463350fae94ca031e7aa4f3a8f9806d80befdc175f19535568de541a7b6a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
