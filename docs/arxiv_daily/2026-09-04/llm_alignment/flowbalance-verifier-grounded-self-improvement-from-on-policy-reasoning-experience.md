---
title: "[论文解读] FlowBalance: Verifier-Grounded Self-Improvement from On-Policy Reasoning Experience"
description: "[arXiv 2609.03241][对齐 / RLHF] FlowBalance旨在把稀疏但可靠的验证器反馈与稠密但可能出错的模型自我指导结合起来，构造并学习一个经过结果校准的完整回答概率分布。"
arxiv_id: "2609.03241"
announcement_date: "2026-09-04"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:36:47.146536+00:00"
source_sha256: "8f7b9655a7634ddd14de275b6cb6166054e43daa86632b5b8d5fc5736d29fd29"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "可验证结果强化学习（RLVR）"
  - "在策略推理经验"
  - "特权回溯自指导"
  - "轨迹平衡"
  - "归一化目标分布"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2609.03241</p>

# FlowBalance: Verifier-Grounded Self-Improvement from On-Policy Reasoning Experience

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Zixun Huang, Kishan Panaganti, Haitao Mi, Leowei Liang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03241v1) · [PDF 下载](https://arxiv.org/pdf/2609.03241v1) · **关键词** 可验证结果强化学习（RLVR）, 在策略推理经验, 特权回溯自指导, 轨迹平衡, 归一化目标分布<br>


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

FlowBalance旨在把稀疏但可靠的验证器反馈与稠密但可能出错的模型自我指导结合起来，构造并学习一个经过结果校准的完整回答概率分布。

**不用术语来说**：推理模型可以通过反复生成答案、检查对错并更新自身来提高能力，但它面对两种不完美的老师：最终答案验证器通常可信，却只能在整段推理结束后给出一个稀疏分数；模型对自己推理过程的逐步评价更细致，却可能对错误答案过度自信。若只听前者，模型难以知道具体哪些推理内容值得保留；若盲目听后者，模型又可能不断强化自己的错误偏好，并收缩到少数单一解法。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 将验证器的组相对优势与特权后见自我指导合并为一个完整轨迹能量，并通过带参考策略支持的轨迹平衡学习归一化回答分布；其更新对象不是额外的逐词模仿损失，而是模型完整推理轨迹上的目标概率分布。
- 提出结果校准的符号门控：正优势轨迹保留自我指导，负优势轨迹反转自我指导，零优势时关闭该分支，从机制上防止被验证器拒绝但被模型高置信评价的回答形成自我确认。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于可验证结果强化学习（RLVR）、大语言模型数学推理自我改进与轨迹分布匹配的交叉领域。模型针对提示 $x$ 生成完整推理回答 $y$，终端验证器根据最终答案是否正确提供可靠但稀疏的奖励；与此同时，训练时可利用带有额外参考解或反馈的特权上下文 $c$，为已生成回答提供密集的同模型指导。FlowBalance关注的基本问题是：如何将这两类信号结合为一个定义在完整回答上的、归一化的目标分布，再通过轨迹平衡训练策略，而不是直接施加逐词模仿损失。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**可验证结果强化学习（RLVR）**

模型生成回答后，自动验证器检查最终答案并返回奖励，例如正确或错误。它的优点是结果监督通常可靠，但奖励只出现在回答结束处，难以直接说明哪些中间推理步骤有帮助。

</div>
<div class="concept-item" markdown="1">

**在策略经验与组相对优势**

在策略经验指使用当前冻结策略实际采样出的回答，而不是从固定数据集中读取的回答。对同一提示采样一组回答后，将某个回答的奖励与该组平均奖励比较并标准化，得到组相对优势，用于判断它相对于同组其他回答是更值得保留还是应被抑制。

</div>
<div class="concept-item" markdown="1">

**轨迹平衡与归一化目标分布**

轨迹平衡通过约束完整生成轨迹的概率与其目标权重相匹配，学习一个能够覆盖多种高质量回答的生成分布，而不只是把概率集中到单个最高奖励答案。本文的目标分布以参考策略为基础，再用回答级能量进行指数加权，因此既表达偏好，又限制策略偏离初始模型过远。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定从提示分布 $x\sim\mathcal{D}$ 中抽取的推理提示，模型生成变长 token 序列 $y=(y_1,\ldots,y_T)\in\mathcal{Y}(x)$。可训练策略按 $\pi_\theta(y\mid x)=\prod_{t=1}^{T}\pi_\theta(y_t\mid s_t)$ 分解，其中状态为 $s_t=(x,y_{<t})$；每次迭代先将当前参数冻结为 $\theta^{-}$，再从 $\pi_{\theta^{-}}$ 为同一提示采样一组回答，并由终端验证器计算奖励 $R_i=R(y^{(i)};x)$。训练还可使用仅在训练阶段可见的上下文 $c$，例如参考解或任务反馈；该上下文用于评价已经采样的 token，不参与生成替代轨迹，也不会在推理时提供给部署策略。方法的输出是更新后的策略，使其在不直接观察 $c$ 的情况下，更倾向于验证结果较好且具有多样性的完整推理回答。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x\sim\mathcal{D}$**

$x$ 表示从提示分布 $\mathcal{D}$ 中抽取的推理问题。

</div>
<div class="notation-item" markdown="1">

**$y=(y_1,\ldots,y_T)\in\mathcal{Y}(x)$**

$y$ 是针对提示 $x$ 生成的完整回答，包含长度为 $T$ 的 token 序列；$\mathcal{Y}(x)$ 表示该提示可能产生的回答集合。

</div>
<div class="notation-item" markdown="1">

**$\pi_\theta(y\mid x)=\prod_{t=1}^{T}\pi_\theta(y_t\mid s_t)$**

$\pi_\theta$ 是参数为 $\theta$ 的生成策略；它将完整回答的概率分解为各生成步骤的条件概率，其中 $s_t=(x,y_{<t})$ 表示当前提示和此前 token。

</div>
<div class="notation-item" markdown="1">

**$A_i=\frac{R_i-\mu_R(x)}{\sigma_R(x)+\epsilon}$**

$A_i$ 是第 $i$ 个回答的组相对优势，$R_i$ 是其验证器奖励，$\mu_R(x)$ 和 $\sigma_R(x)$ 分别是同一提示回答组的奖励均值与标准差，$\epsilon$ 是防止除零的小常数。优势为正表示该回答优于组内平均水平，为负则表示低于平均水平。

</div>

</div>

**直接相关的工作**

- **FlowRL**: FlowRL与本文都属于基于轨迹平衡的分布式推理策略学习方法，并使用提示条件的归一化项或组内估计来处理完整生成轨迹。本文将与FlowRL的比较用于检验：在相近的轨迹平衡框架中，加入由验证器优势校准的特权自指导是否能带来额外收益。
- **β-OPSD**: β-OPSD代表利用特权同模型视角进行在策略蒸馏的一类方法，并通过可调参数平衡参考策略与教师信号。本文与其不同之处在于，仅把特权视角产生的 token 级信息作为停止梯度的回答级自指导特征，再由验证器优势决定保留、反转或关闭该指导，最终通过完整回答上的轨迹平衡拟合目标分布，而不使用独立的 token 级模仿损失。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

长程数学推理的自我改进不能只提高平均奖励，还需要把概率稳定地移向正确推理，同时保留多种有用策略。训练时，每个回答可能包含数百乃至数千个词元，而验证器通常只提供一次终局奖励；因此，更新信号既难以定位推理路径中的有效部分，也可能反复强化某条局部偏好的轨迹，造成训练不稳定、探索减少或策略多样性下降。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于可验证奖励的强化学习与结果分布方法，如GRPO、FlowRL**：模型针对同一题目采样一组回答，由验证器判断最终结果并形成回答级或组相对训练信号。GRPO据此进行策略优化；FlowRL进一步把终局证据转化为完整回答上的概率分布，以改善结果级信用分配。
- **同模型的特权后见自我指导与RL—自指导混合方法，如OPSD、RLSD**：冻结当前策略的一个训练时副本，并让它看到参考解答或任务反馈等推理时不可用的上下文，再对已采样回答中的每个词元给出概率评价。该信号成本较低且比终局奖励稠密，可单独用于蒸馏或作为额外指导加入强化学习。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 仅依赖验证器结果的方案虽然方向可靠，但监督过于稀疏：同一个回答级信号被附着到整条长轨迹的所有决策上；即使FlowRL能更合理地塑造完整回答分布，纯结果能量仍无法利用路径内部哪些步骤受到细粒度支持的信息。
- 未经结果校准的稠密自我指导并不可靠：特权评分视角可能偏爱表面合理但最终错误的轨迹，也可能鼓励缩短推理、抑制因不确定性产生的探索，或把概率集中到狭窄局部模式。其后果是模型把自身的错误置信度当作下一轮监督，形成自我确认；直接增强指导强度也不等于更好的学习。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有方法分别擅长提供可靠的结果方向或稠密的路径信息，但尚缺少一种统一的分布式更新规则：它既要让验证结果约束自我指导的方向，又要把两类信号转化为参考策略支持下、对完整回答显式归一化的目标分布，同时避免另设逐词模仿目标与结果目标相互竞争。

</div>
<div markdown="1"><span>核心问题</span>

给定当前策略产生的同策略推理轨迹、稀疏的已验证结果，以及稠密但不完全可信的自我指导，下一轮策略究竟应学习什么样的归一化完整回答分布？

</div>
<div markdown="1"><span>作者直觉</span>

可以把验证器看作负责判定“总体该奖励还是该惩罚”的裁判，把特权后见模型看作负责提供“这条路径内部哪些内容更受支持”的顾问。FlowBalance不允许顾问推翻裁判：当轨迹相对更好时，顾问信号沿原方向增强它；当轨迹相对更差时，同样的高置信指导会被反向使用，从而压低错误轨迹；当组内结果没有偏好时，则不采用该指导。随后，轨迹平衡把这种复合偏好转成完整回答之间一致且归一化的概率关系，使细粒度信息只在可靠结果方向内发挥作用。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

FlowBalance 的输入是提示—上下文对 $(x,c)$、当前策略 $pi_{\theta}$、固定参考策略 $pi_{\mathrm{ref}}$ 和终端验证器 $R$。每轮训练先将当前策略冻结为 $pi_{\theta^{-}}$，在不提供训练专用上下文 $c$ 的条件下为每个提示采样一组完整推理轨迹；随后用验证器计算组内相对优势，并让同一个冻结策略在事后看到 $c$，对已采样 token 计算密集的 hindsight 自引导分数。方法用优势的符号校准该分数：验证结果较好时保留引导，验证结果较差时反转引导，组内没有结果偏好时关闭引导；再以参考策略为基准、以轨迹能量为指数权重构造归一化完整响应分布，最后用轨迹平衡损失更新可训练策略。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 冻结策略并采样在策略经验

每轮开始时复制参数 $\theta^{-}\leftarrow\theta$，得到冻结 rollout 策略 $pi_{\theta^{-}}$；对每个提示只输入 $x$，采样 $N$ 个完整响应 $\{y^{(i)}\}_{i=1}^{N}\sim\pi_{\theta^{-}}(\cdot\mid x)$。响应按 $\pi_{\theta}(y\mid x)=\prod_{t=1}^{T}\pi_{\theta}(y_t\mid s_t)$ 分解，其中 $s_t=(x,y_{<t})$。

<div class="method-step__io" markdown="1">

**输入**：当前可训练策略 $pi_{\theta}$、提示—上下文数据集中的 $(x,c)$，以及每个提示的组大小 $N$。<br>
**输出**：一组不依赖训练专用上下文的 on-policy 推理轨迹及其 token 序列。

</div>

**直观理解**：模型先像部署时一样独立解题，而不是直接偷看参考解。冻结快照保证同一轮中所有样本来自同一个旧策略，避免采样过程中策略不断变化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 验证结果并计算组内优势

验证器依据最终答案正确性给出终端奖励 $R_i$，再用该组奖励的均值 $\mu_R(x)$ 和标准差 $\sigma_R(x)$ 计算停止梯度的相对优势 $A_i=(R_i-\mu_R(x))/(\sigma_R(x)+\epsilon)$。奖励、组统计量、轨迹和优势在策略更新时均不反向传播。

<div class="method-step__io" markdown="1">

**输入**：同一提示的响应组 $\{y^{(i)}\}_{i=1}^{N}$ 和终端验证器 $R(y^{(i)};x)$。<br>
**输出**：每条轨迹的验证奖励 $R_i$ 及组相对优势 $A_i$。

</div>

**直观理解**：优势不是问“这道题绝对有多好”，而是问“它在本组样本中相对好还是相对差”。这样验证器只需提供稀疏但可靠的方向：提高相对正确的轨迹，降低相对错误的轨迹。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成训练专用的 hindsight 自引导特征

对同一已采样 token $y_t$，分别用不看 $c$ 的 rollout 视图和看见 $c$ 的 hindsight 视图评分；hindsight 视图为 $\pi_{\mathrm{H}}(\cdot\mid s_t,c)=\pi_{\theta^{-}}(\cdot\mid x,c,y_{<t})$，并计算截断增益 $\delta_t^{\mathrm{H}}=\operatorname{clip}(\log\pi_{\mathrm{H}}(y_t\mid s_t,c)-\log\pi_{\mathrm{ref}}(y_t\mid s_t),-B,B)$。将其按完整响应平均得到 $G_{\mathrm{H}}(y\mid x,c)=T^{-1}\sum_{t=1}^{T}\delta_t^{\mathrm{H}}$；不从 hindsight 视图重新采样，也不对该分数求梯度。

<div class="method-step__io" markdown="1">

**输入**：已采样响应 $y$、提示 $x$、仅训练时可见的上下文 $c$，以及冻结策略和固定参考策略。<br>
**输出**：每条完整轨迹的停止梯度自引导分数 $G_{\mathrm{H}}$。

</div>

**直观理解**：训练时让同一个模型事后参考解题线索，检查已经走过的 token 哪些更符合“知道答案后的判断”。它只是给完整轨迹提供一个辅助评分，不会变成直接逐 token 模仿参考答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按验证方向构造归一化目标并更新策略

先构造能量 $E_{\mathrm{FlowBalance}}(y\mid x,c)=\eta_AA(y)+\beta_GG_{\mathrm{H}}(y\mid x,c)\operatorname{sgn}(A(y))$，再形成以参考策略为支持的 Gibbs 目标 $p^{\star}(y\mid x,c)\propto\pi_{\mathrm{ref}}(y\mid x)\exp(E_{\mathrm{FlowBalance}}(y\mid x,c)/\tau)$。在实际采样组上用每条轨迹隐含的分区函数估计值的组平均作为 $\widehat{\log Z}$，计算完整轨迹平衡残差，并只通过可训练策略的 $\log\pi_{\theta}(y^{(i)}\mid x)$ 更新参数。

<div class="method-step__io" markdown="1">

**输入**：组内优势 $A(y)$、hindsight 分数 $G_{\mathrm{H}}(y\mid x,c)$、参考策略 $\pi_{\mathrm{ref}}$、温度 $\tau$，以及当前策略对采样轨迹的概率。<br>
**输出**：更新后的策略参数 $\theta$，下一轮再将其冻结并生成新经验。

</div>

**直观理解**：正确轨迹的引导分数会被放大，错误轨迹的引导分数会被反向使用，因此模型不会因为“看起来很自信”就重复错误答案。归一化目标像一个总量为一的概率预算，决定概率质量如何在完整解题过程之间重新分配，而不是孤立地奖励某些 token。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### Outcome-calibrated FlowBalance trajectory energy

$$
E_{\mathrm{FlowBalance}}(y\mid x,c)=\eta_{A}A(y)+\beta_{G}G_{\mathrm{H}}(y\mid x,c)\operatorname{sgn}(A(y))
$$

**符号说明**

- $E_{\mathrm{FlowBalance}}(y\mid x,c)$：轨迹 $y$ 在提示 $x$ 和训练专用上下文 $c$ 下的停止梯度能量，用于重新加权完整响应。
- $A(y)$：轨迹相对于同一 rollout 组的标准化验证优势；正值表示相对更好的验证结果，负值表示相对更差。
- $G_{\mathrm{H}}(y\mid x,c)$：hindsight 视图相对于参考策略的截断 token 对数概率增益的轨迹平均值。
- $\eta_A$：验证器优势项的系数，控制终端验证信号的强度。
- $\beta_G$：自引导项的系数，控制密集 hindsight 证据的强度。
- $\operatorname{sgn}(A(y))$：优势的符号函数：正优势保留引导方向，负优势反转引导方向，零优势使该项为零。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把稀疏但可信的最终答案验证和密集但可能错误的自评估合并起来。关键不是简单相加，而是让验证结果决定自评估应被信任、反向纠正，还是完全不使用。<br>
**原文位置**：第 3.2 节，式 (11)

</div>

</div>

<div class="equation-block" markdown="1">

#### Trajectory-balance training objective

$$
\mathcal{L}_{\mathrm{FlowBalance}}(\theta)=\mathbb{E}_{(x,c)\sim\mathcal{D}}\left[\frac{1}{2N}\sum_{i=1}^{N}\Delta_{\mathrm{TB}}(y^{(i)};x,c)^{2}\right],\quad\Delta_{\mathrm{TB}}(y^{(i)};x,c)=\tau\log Z_{\mathrm{FlowBalance}}(x,c)+\tau\log\frac{\pi_{\theta}(y^{(i)}\mid x)}{\pi_{\mathrm{ref}}(y^{(i)}\mid x)}-E_{\mathrm{FlowBalance}}(y^{(i)}\mid x,c)
$$

**符号说明**

- $\mathcal{L}_{\mathrm{FlowBalance}}(\theta)$：待最小化的策略训练损失，优化变量只有当前策略参数 $\theta$。
- $\mathcal{D}$：提示—上下文数据分布，样本为 $(x,c)$。
- $N$：每个提示采样的 rollout 响应数量。
- $\Delta_{\mathrm{TB}}$：轨迹平衡残差，衡量当前策略相对参考策略的概率比是否匹配目标能量和分区函数。
- $Z_{\mathrm{FlowBalance}}(x,c)$：目标分布的分区函数，负责把指数加权后的完整响应权重归一化。实际训练中使用停止梯度的组内估计。
- $\tau$：温度参数，控制能量对目标分布重加权的敏感程度。
- $\pi_{\theta}(y^{(i)}\mid x)$：当前可训练策略对已采样完整响应的概率；梯度仅通过其对数概率传播。
- $\pi_{\mathrm{ref}}(y^{(i)}\mid x)$：固定初始参考策略对该响应的概率，用于提供支持并约束策略漂移。

<div class="equation-explanation" markdown="1">

**直观理解**：如果残差为零，当前策略相对参考策略的完整轨迹概率比就与能量规定的偏好一致；同一提示的分区函数只提供共同偏移，不改变轨迹之间的相对排序。最小化平方残差就是让模型逐步逼近这个归一化目标分布，而不是直接对每个 token 施加模仿损失。<br>
**原文位置**：第 3.3 节，式 (16) 和式 (18)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标是采样响应组上的轨迹平衡残差平方平均。对每个 $(x,c)$，先用停止梯度的能量和组内分区估计构造 $\Delta_{\mathrm{TB}}$，再最小化 $\mathcal{L}_{\mathrm{FlowBalance}}$；梯度只作用于当前策略的完整响应对数概率 $\log\pi_{\theta}(y^{(i)}\mid x)$。因此优化的直接目标是使当前策略匹配由验证优势、自引导分数和参考策略共同定义的归一化完整响应分布，而不是单独拟合 hindsight token。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Privileged-Hindsight Self-Guidance**

该模块使用同一冻结快照的两个条件视图：rollout 视图 $\pi_{\mathrm{roll}}(\cdot\mid s_t)=\pi_{\theta^{-}}(\cdot\mid x,y_{<t})$ 用于无上下文采样，hindsight 视图 $\pi_{\mathrm{H}}(\cdot\mid s_t,c)=\pi_{\theta^{-}}(\cdot\mid x,c,y_{<t})$ 仅对相同已采样 token 进行事后评分。token 级对数概率差经截断后取完整轨迹平均，形成停止梯度特征 $G_{\mathrm{H}}$；该特征进入轨迹能量，而不是进入独立的 token-level imitation loss。

> 直观理解：模型可以在训练时借助参考解检查自己的旧答案，但部署时既看不到 $c$，也不会运行 hindsight 分支。这样既获得较密集的训练信号，又避免把训练专用信息直接带入推理。

**2. Outcome-Calibrated Energy**

轨迹能量由验证优势项和符号校准的自引导项组成：$\eta_AA$ 提供终端结果方向，$\beta_GG_{\mathrm{H}}\operatorname{sgn}(A)$ 提供密集轨迹证据。当 $A>0$ 时保留自引导方向，当 $A<0$ 时反转方向，当 $A=0$ 时关闭密集分支；所有这些量在更新时停止梯度。

> 直观理解：自引导可能“说得很像正确推理”却实际答错，因此不能单独决定学习方向。验证器像安全开关，决定自引导应该帮助还是纠正。

**3. Reference-Supported Trajectory Balance**

目标分布以固定 $\pi_{\mathrm{ref}}$ 为基底，并通过 $\exp(E/\tau)$ 重新加权完整响应。训练最小化采样轨迹上的平方平衡残差；分区函数不由额外的 prompt 网络学习，而由组内各响应给出的 $\widehat{\log Z}_i=E_i/\tau-\log(\pi_{\theta}(y^{(i)}\mid x)/\pi_{\mathrm{ref}}(y^{(i)}\mid x))$ 的平均值估计，且该估计停止梯度。

> 直观理解：参考策略限制模型不要无界漂移，能量只表达不同完整解法之间的相对偏好。轨迹平衡把这些相对偏好转化为整个响应分布的更新，因此不会把长推理简单压缩成局部 token 模仿。

**训练与推理**

训练时，从数据分布采样 minibatch 的 $(x_b,c_b)$；将当前策略快照为 $\pi_{\theta^{-}}$，仅输入 $x_b$ 生成每个提示的 $N$ 条响应；用验证器计算 $R_{b,i}$、组统计量和 $A_{b,i}$，再用冻结 hindsight 视图输入 $(x_b,c_b,y_{<t})$ 对这些既有响应评分，并结合参考策略得到 $G_{\mathrm{H}}$、能量和组内 $\widehat{\log Z}$。随后计算轨迹平衡损失并更新 $\theta$，进入下一轮时重新冻结新策略。推理时只部署更新后的 $\pi_{\theta}(\cdot\mid x)$，不提供训练专用上下文 $c$，不运行验证器或 hindsight 视图，也不从参考策略和分区函数额外采样。

**复现信息**

复现实验所必需的核心实现约束是：rollout 使用每轮冻结的 $\pi_{\theta^{-}}$，参考策略是初始 checkpoint 的固定副本；hindsight token 增益按 $[-B,B]$ 截断并在完整响应长度 $T$ 上平均；奖励、优势、$G_{\mathrm{H}}$、能量、分区估计和采样响应全部停止梯度。实际论文实验采用完整响应轨迹平衡实现；文中虽给出可按区间计算的 subtrajectory balance，但明确说明实验默认并非该实现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- AIME24：数学竞赛推理基准，主实验采用 Pass@16，以考察模型在允许生成多个候选答案时至少成功一次的能力；附加诊断还使用该基准检查正确策略的多样性。题目数量、训练/测试划分及具体提示模板在所给原文中未明确报告。
- HMMT25：数学竞赛推理基准，采用 Pass@1，检验单次生成的解题正确率。题目规模与数据划分在所给原文中未明确报告。
- Minerva、MATH500 与 OlympiadBench：三者共同构成覆盖不同数学难度和题型的 Pass@1 评测组，用于判断提升是否具有跨基准一致性，而非只针对 AIME24 调参；所给原文未分别说明其规模与划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Pass@1**

每道题只评估一次生成时的正确率，用于衡量部署条件下单次回答的可靠性；HMMT25、Minerva、MATH500 和 OlympiadBench 使用该指标。 （越高越好，因为表示无需多次采样即可得到正确答案的概率更高。）

</div>
<div class="metric-item" markdown="1">

**Pass@16**

对每道题生成至多 16 个候选答案，统计其中至少一个正确答案的概率；AIME24 使用该指标，以反映竞赛题上的采样式求解能力。 （越高越好，因为表示模型在有限候选预算内覆盖正确推理路径的能力更强，但它不等同于单次回答准确率。）

</div>
<div class="metric-item" markdown="1">

**验证成功质量与分布诊断**

包括精确可枚举空间中的 verified-success mass、成功模式间的 conditional Simpson diversity、相对参考策略的 reverse KL，以及训练曲线中的更新速度、后期稳定性和响应长度。这些指标分别检查概率是否移向正确答案、正确策略是否仍保持多样、策略改变是否保守，以及训练过程是否稳定。 （成功质量和成功模式多样性通常越高越好；reverse KL 越低表示偏离参考策略越小，但必须结合达到的目标能量或正确率解释；波动和无意义的长度漂移越小越好。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3-4B 与 Qwen3-8B 的五个数学推理基准主评测，第 180 步、5 个随机种子。

<div class="result-value" markdown="1">

作者报告 FlowBalance 在两个模型规模上的跨基准平均表现均优于最直接的结果式轨迹平衡基线 FlowRL，同时训练更快、更稳定，并避免了直接 OPSD 的响应长度坍缩。所给节选没有包含表 1 的具体数据行，因此无法核验各基准分数、平均提升幅度及标准差。

</div>

这项结果回答了方法是否能在真实语言模型训练中产生总体收益：优势并非只在一个模型尺寸上出现，而且相对于结构最接近的 FlowRL 有平均性能提升。它还表明稠密自指导不必以生成长度失控为代价。不过，缺少完整表 1 和图 2 数值意味着不能从当前材料判断提升是否在每个数据集上都成立、是否超过随机种子波动，或对其他模型家族是否可推广。

<div class="result-source" markdown="1">

来源：摘要；第 5.2 节主结果指向表 1，第 5.1 节指向图 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On mathematical reasoning, FlowBalance improves average performance over FlowRL on both Qwen3-4B and Qwen3-8B, while also improving training speed and stability, avoiding direct OPSD's response-length collapse, and exhibiting higher correct-strategy diversity in a controlled AIME24 diagnostic.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 四模式精确可枚举诊断：两个失败模式与两个成功模式；参考分布为 $\rho=(0.30,0.20,0.30,0.20)$，优势为 $A=(-1,-1,+1,+1)$，自指导为 $G=(0.45,0.25,0.30,0.75)$，且 $(\eta,\beta,\tau)=(0.75,0.80,1)$。

<div class="result-value" markdown="1">

结果奖励单独塑形的成功总概率质量为 $0.818$；不做门控的自指导为 $0.832$，但会强化失败模式上的正向错误支持；FlowBalance 将成功总质量提高到 $0.900$，其中更稳健成功模式的质量为 $0.440$。

</div>

该可枚举实验直接展示了符号门控的作用：验证器先区分成功与失败，自指导再在成功答案内部偏向更稳健的解法；若某个失败答案也被模型错误地认为“很像正确答案”，FlowBalance 会反转而非保留这部分指导。由于这是人工构造的四模式概率空间，而不是语言模型训练结果，它证明的是目标分布在受控条件下的机制行为，不证明现实任务中的指导评分总是可靠。

<div class="result-source" markdown="1">

来源：附录 C.1.1，图 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

FlowBalance preserves the useful ranking among successes while reversing the failed-response contribution, reaching success mass 0.900 and robust-success mass 0.440.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 精确分布诊断与局部高斯风险分析：比较 FlowBalance 的指数倾斜路径、一个匹配相同能量的固定数据目标，以及每组仅使用一个对比方向的估计器。

<div class="result-value" markdown="1">

在达到相同复合能量的构造对照中，固定数据目标相对参考分布的 reverse KL 为 $0.973$，FlowBalance 为 $0.273$，前者位移约为后者的 $3.6$ 倍；当 rollout 组大小为 $N=32$ 时，保留全部 $N-1$ 个组内对比方向的精确参数风险为单对比估计器的 $2.92\%$，约低 $34$ 倍。

</div>

左侧结果说明 FlowBalance 以较小的策略分布改动达到给定目标能量，可理解为更保守地重新分配概率；右侧结果说明对每个 rollout 组只剔除一个公共截距、保留其余全部相对差异，比每组只抽取一对轨迹进行比较更充分地利用样本。这些是理论性质的数值验证，不等同于真实训练中必然获得 $34$ 倍速度提升。

<div class="result-source" markdown="1">

来源：附录 C.1.4，图 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At group size N=32, its exact parameter risk is 2.92% of a one-contrast-per-group estimator, approximately 34× lower risk.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前节选省略了表 1 的完整分数、图 2 的训练曲线以及附录 D.1 的实现参数，因而无法核验 FlowBalance 相对各基线的逐数据集提升、方差显著性、实际训练加速幅度和长度坍缩程度；主实验结论仍需对照原表复查。
- 实验仅明确覆盖 Qwen3-4B、Qwen3-8B 和数学推理任务；图 4—7 多为精确可枚举或局部高斯构造诊断。它们能解释目标分布为何有效及何时失效，但不能替代跨模型家族、跨任务和真实验证器噪声条件下的泛化验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- GRPO：以终局验证器奖励训练的强化学习基线，用于判断 FlowBalance 的自指导是否提供了超出稀疏结果监督的增益。
- OPSD：直接同策略蒸馏基线，按其原始设定使用固定的特权教师；它检验未经结果校准的稠密指导是否会带来收益，以及是否出现响应长度坍缩等副作用。
- RLSD：验证器与蒸馏相结合的基线，也通过冻结的当前策略快照进行评分；与它比较可区分 FlowBalance 的轨迹分布拟合和符号门控是否优于一般的强化学习—自蒸馏混合。
- FlowRL：仅使用结果信号的轨迹平衡基线，是最直接的结构对照；二者都在轨迹层面学习分布，但 FlowBalance 额外加入经验证器优势校准的自指导。

**实验想回答的问题**

- 在相同提示、采样预算、验证器与评测流程下，FlowBalance 能否比仅依赖结果验证器的强化学习、直接同策略蒸馏、验证器—蒸馏混合方法以及仅结果驱动的轨迹平衡更准确、稳定且高效地提升数学推理策略？
- FlowBalance 的优势是否确实来自“用验证器优势校准自指导”的机制，即保留成功轨迹上的指导、反转失败轨迹上的错误自信；这种机制在指导可靠性下降或强度增大时又有哪些边界？

**实验实现**

主实验使用 Qwen3-4B 与 Qwen3-8B。所有部署策略在推理时只接收题目；FlowBalance 仅在训练阶段让冻结的当前策略快照看到训练解答或任务反馈，并用这些特权上下文为已经采样的 token 评分，因此测试时不需要额外教师或反馈。各方法在同一骨干模型内共享训练提示、rollout 组大小、验证器、最大响应长度、检查点计划和评测脚本。表 1 报告训练第 180 步、5 个随机种子的均值与样本标准差，并将五个基准的均值再取平均；AIME24 使用 Pass@16，其余基准使用 Pass@1。图 2 用中间训练轨迹检查更新效率、后期稳定性和响应长度。具体超参数被指向附录 D.1 表 5，但所给节选未包含这些字段。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 二元混合结果组中的假阳性自指导扫描：成功回答有正指导 $G_{+}>0$，失败回答也被错误赋予正支持 $G_{-}>0$；比较 FlowBalance、仅奖励塑形与无门控自指导。 | 当 $G_{-}=0.5$ 时，FlowBalance 的精确目标成功概率为 $0.894$，仅奖励塑形为 $0.817$，无门控自指导为 $0.807$。这隔离了失败轨迹上反转指导符号的贡献：无门控方法会因错误自信而比仅奖励方法更差，而 FlowBalance 利用 $-G_{-}$ 增大成功答案相对失败答案的对数优势。 | 该消融固定成功答案上的有用指导，只逐步增加失败答案上的错误支持，因此差异可归因于是否使用验证器结果校准自指导。它说明门控可以精确修正一种特定的“假阳性自确认”，但实验空间只有一个成功和一个失败响应，不能覆盖复杂语言生成中的所有误差结构。 | 附录 C.1.2，图 5<br><span class="experiment-evidence">At G−=0.5, the exact target success probabilities are 0.894 for FlowBalance, 0.817 for reward-only shaping, and 0.807 for ungated shaping.</span> |
| 五模式可靠性—强度扫描：以 $G_q=qG_{\mathrm{useful}}+(1-q)G_{\mathrm{adv}}$ 在有用指导和对抗性指导间插值，同时改变可靠性 $q$ 与指导强度 $\beta_G/\tau$。 | 作者报告存在可靠性阈值：阈值以上，FlowBalance 相比仅奖励塑形增加验证成功质量并保留多个成功模式；阈值以下，更强的指导可能降低验证成功率。所给原文未明确报告该阈值的数值位置或各网格点增益。 | 该实验隔离了自指导质量与强度的交互作用，防止把符号门控误解为“任何模型自评都安全”。门控能修正失败答案上的正向错误置信度，却不能挽救对成功答案也系统性判断错误的指导，因此实际使用仍需控制指导强度并监测其与验证器的一致性。 | 附录 C.1.3，图 6<br><span class="experiment-evidence">Below that threshold, stronger guidance can reduce verified success.</span> |

**定性案例**

- 受控 AIME24 诊断由 LLM 判断正确回答是否采用不同解题策略，作者报告 FlowBalance 的正确策略多样性更高。其意义是模型并非只把概率集中到单一成功模板，这与学习“完整回答的归一化分布”的目标一致；但节选未提供评审模型、提示词、一致性校验、样本规模或具体多样性数值，因此该结果应视为辅助性定性证据，而非独立的正确率证明。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces verifier-grounded on-policy post-training that improves mathematical reasoning through outcome-calibrated self-guidance and trajectory balance.; rule check: matched taxonomy keywords; top rule score=6.0
- 全文指纹：`8f7b9655a7634ddd14de275b6cb6166054e43daa86632b5b8d5fc5736d29fd29`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
