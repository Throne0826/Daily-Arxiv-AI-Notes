---
title: "[论文解读] SeedPolicy: Horizon Scaling via Self-Evolving Diffusion Policy for Robot Manipulation"
description: "[arXiv 2603.05117][机器人 / 具身智能] 本文针对扩散策略无法从更长观测历史中稳定获益的问题，提出以紧凑递归状态和动态门控实现可扩展时间建模的 SeedPolicy。"
arxiv_id: "2603.05117"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.144251+00:00"
source_sha256: "a02e0a62bc8413f65bef48a7f7b598c62f69333c528ddc085e2085d7b34a4969"
tags:
  - "机器人 / 具身智能"
  - "机器人操作"
  - "模仿学习"
  - "扩散策略"
  - "长时序建模"
  - "观测时域扩展"
  - "门控注意力"
  - "潜在状态"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2603.05117</p>

# SeedPolicy: Horizon Scaling via Self-Evolving Diffusion Policy for Robot Manipulation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Gui, Youqiang, Zhou, Yuxuan, Cheng, Shen, Yuan, Xinyang, Fan, Haoqiang, Cheng, Peng, Liu, Shuaicheng</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2603.05117) · [PDF 下载](https://arxiv.org/pdf/2603.05117) · **关键词** 机器人操作, 模仿学习, 扩散策略, 长时序建模, 观测时域扩展, 门控注意力, 潜在状态<br>
**代码**: [https://github.com/Youqiang-Gui/SeedPolicy](https://github.com/Youqiang-Gui/SeedPolicy)

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

本文针对扩散策略无法从更长观测历史中稳定获益的问题，提出以紧凑递归状态和动态门控实现可扩展时间建模的 SeedPolicy。

**不用术语来说**：机器人完成长流程操作时，当前动作往往取决于较早发生的事情，例如物体此前的位置变化或已经完成的步骤；但把更多历史图像直接塞给现有策略，不仅没有稳定提高成功率，反而可能因难以理解帧间关系和混入无关画面而降低性能。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出自演化门控注意力 SEGA：通过反复更新一个紧凑的隐状态来累积长期上下文，并利用基于交叉注意力信号的门控抑制噪声或无关观测，从而兼顾历史信息保留与时间干扰过滤。
- 作者将 SEGA 集成到扩散策略形成 SeedPolicy，使有效时间感受野能够递归扩展，而不必持续增大每一步的观测窗口；作者声称该设计扭转了标准扩散策略随观测时域增长而性能下降的趋势。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于机器人操作中的模仿学习：策略从专家示范中学习如何根据连续观测生成控制动作。其重点是扩散策略在长时序任务中的时间建模能力。标准扩散策略能够表示同一情境下多种合理动作所形成的多模态分布，并通常一次预测一段动作以提高执行稳定性；但它主要通过堆叠有限数量的历史图像帧来提供时间上下文，随着观测窗口增长，这种简单堆叠不仅未必带来更强的长期推理能力，反而可能导致性能下降。本文因而研究如何在不过度增加计算成本的前提下，将更长历史压缩进持续更新的隐状态，使策略获得更大的有效时间感受野。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**模仿学习（Imitation Learning, IL）**

机器人利用专家示范中的观测—动作序列学习控制策略，而不必完全依赖人工编写奖励函数。训练目标是让策略在新执行过程中根据当前及历史观测产生接近专家行为的动作。

</div>
<div class="concept-item" markdown="1">

**扩散策略（Diffusion Policy, DP）**

扩散策略把动作生成视为逐步去噪过程，从随机噪声中恢复出符合观测条件的动作序列，因此能够表达多种均合理的专家行为。与只预测单步确定性动作相比，它更适合处理机器人操作中的多模态动作分布。

</div>
<div class="concept-item" markdown="1">

**观测时域与有效时间感受野**

观测时域是策略一次直接读取的连续历史观测长度；有效时间感受野则是实际能够影响当前决策的历史范围。增加堆叠帧数会扩大输入窗口，但若模型不能显式建立跨时刻联系，就不等于真正利用了更长历史。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定由专家示范构成的机器人操作数据，策略在每个控制时刻接收视觉观测及机器人状态等可用信息，并输出未来一段连续控制动作；论文讨论的核心设置是需要跨越较长时间、依赖早期线索完成后续决策的操作任务。标准扩散策略将最近若干时刻的观测直接堆叠后作为条件，但该设置隐含地要求模型自行从不断增大的帧集合中提取时间依赖。SeedPolicy改为维护随时间递归更新的紧凑潜在状态：新观测与历史状态交互，门控机制抑制遮挡、背景变化等无关信号，再以更新后的状态为扩散动作生成提供长期上下文。其基本假设是历史信息对任务的价值在时间上较为稀疏，并非每一帧都应被等量写入记忆。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **ACT**: ACT是基于Transformer的模仿学习方法，通过一次预测动作块而非单步动作来缓解控制抖动并提升轨迹平滑性；它说明了分段动作预测对机器人控制的价值，但本文关注的是观测历史随时域扩展时的长期时间建模问题。
- **Diffusion Policy（DP）**: DP使用扩散模型刻画专家行为的多模态动作分布，是SeedPolicy直接改造的基础策略。本文保留其扩散式动作生成框架，同时以持续演化、带门控的潜在状态替代单纯扩大观测帧堆叠，以扩展有效时间感受野。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

长时域机器人操作需要根据跨越多个时刻的视觉线索作出动作，但关键线索通常在时间上稀疏，还可能被背景变化、遮挡等干扰隔开。因此，策略既要记住较早的任务相关信息，又要避免将每一帧都无差别写入历史表示；否则，增加观测历史并不等于获得可用的长期记忆。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **动作分块与扩散策略**：ACT 等方法一次预测一段动作，以减少逐步控制的抖动并提高轨迹平滑性；Diffusion Policy 则用扩散模型学习专家动作的多峰分布，以表达同一情境下多种合理操作方式。标准 Diffusion Policy 通常把最近若干帧堆叠后共同输入策略。
- **堆叠观测上的时间自注意力**：该思路先提取各时刻的观测特征，再通过时间自注意力显式建立不同时刻之间的交互。文中将其作为直接改进方案，用来验证显式时间建模确实比单纯堆帧更能利用历史信息。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 简单堆叠更多图像帧并未显式刻画复杂的跨时刻依赖；随着帧数增加，标准 Diffusion Policy 反而出现性能下降，因而无法把更长输入历史可靠地转化为长时任务收益。作者指出该反直觉现象虽曾被既有工作简短提及，但其原因与解决方法仍未得到系统研究。
- 时间自注意力虽能改善历史利用，但其计算成本随观测时域呈二次增长，扩展到更长时域时还会出现收益递减；同时，无差别整合所有观测容易让背景变化、遮挡等无关信号污染历史上下文。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种适用于扩散式机器人控制的时间模块：它应在不持续扩大单步观测窗口、也不承担全历史注意力二次成本的前提下，长期保存任务相关上下文，并有选择地拒绝噪声观测。换言之，尚未解决的是扩散策略的“时域扩展”瓶颈，而不只是动作分布建模能力不足。

</div>
<div markdown="1"><span>核心问题</span>

能否让 Diffusion Policy 通过固定规模、持续演化的内部状态获得越来越长的有效时间感受野，并使更长历史稳定带来操作成功率收益，同时保持适中的计算与参数开销？

</div>
<div markdown="1"><span>作者直觉</span>

与其每一步都重新查看并两两比较越来越多的历史帧，不如维护一份可持续更新的“任务摘要”：新观测到来时，只把其中与当前任务相关的内容写入摘要，将遮挡或背景扰动挡在外面。递归状态负责压缩和携带过去，注意力负责判断新旧信息的关联，门控则控制写入强度，因此模型有机会用近似固定的单步处理规模延伸记忆，并减少无关帧对长期上下文的污染。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SeedPolicy是在扩散策略（Diffusion Policy, DP）前加入递归时序模块SEGA的端到端机器人操作框架。时刻$t$的RGB图像$I_t$与关节位姿$P_t$先被编码为固定长度的观测特征$O_t$；SEGA一面根据$O_t$门控更新缓存的历史状态$S_{t-1}$，得到$S_t$，一面让当前观测从$S_{t-1}$中检索相关历史线索，生成增强特征$EObs_t$；最后，Transformer式扩散动作专家以$EObs_t$为条件，预测包含$N$个未来14自由度动作的序列$A_t$。

关键设计是把“扩大输入窗口”改为“递归维护固定容量的状态”：每一步只处理当前观测和已经缓存的$S_{t-1}$，但历史信息可随状态逐步累积。SEGA还直接利用跨注意力的原始分数生成更新门$G_t$，让与当前任务语义相关的信息写入状态，而让背景变化或干扰物等低相关信息尽量不覆盖旧记忆；这分别解决了长时依赖、计算开销和历史状态污染问题。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 当前观测编码

视觉输入由ResNet编码，关节信息由相应的位姿编码分支处理，随后形成$O_t\in\mathbb{R}^{N_o\times D}$；其中$N_o$是观测特征向量数量，$D$是特征维度。

<div class="method-step__io" markdown="1">

**输入**：时刻$t$的RGB图像$I_t$与机器人关节位姿$P_t$。<br>
**输出**：当前时刻的观测特征$O_t$。

</div>

**直观理解**：这一步把像素和关节数值转换成统一的特征“词元”，使后续注意力模块能够比较当前场景与历史记忆。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 状态与观测的内部上下文建模

SEGA分别对$S_{t-1}$和$O_t$执行多头自注意力并采用残差连接，得到$S'_{t-1}$与$O'_t$；随后将两者送入并行的状态更新流和状态检索流。

<div class="method-step__io" markdown="1">

**输入**：上一时刻缓存的状态$S_{t-1}\in\mathbb{R}^{N_s\times D}$和当前观测$O_t$。<br>
**输出**：上下文化后的历史状态$S'_{t-1}$与观测特征$O'_t$。

</div>

**直观理解**：自注意力先整理每组特征内部的关系，例如哪些视觉区域属于同一物体、哪些记忆槽共同描述此前的操作阶段。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 门控状态更新

以$S'_{t-1}$为查询、以$O'_t$为键和值执行跨注意力，产生候选中间状态$\mathrm{Inter}\cdot S_t$及各层各头的预Softmax注意力logits；SEG汇总这些logits形成门$G_t$，再在候选状态和旧状态之间逐槽加权，得到$S_t$。

<div class="method-step__io" markdown="1">

**输入**：历史状态特征$S'_{t-1}$、当前观测特征$O'_t$以及旧状态$S_{t-1}$。<br>
**输出**：更新后并供下一控制时刻缓存的状态$S_t$。

</div>

**直观理解**：可把每个状态槽看成一格长期记忆：门值大时写入当前信息，门值小时保留旧内容，从而避免每帧背景变化都改写历史。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 历史状态检索

在与更新流并行的检索流中，以$O'_t$为查询、以$S'_{t-1}$为键和值执行跨注意力，得到历史上下文增强的观测$EObs_t$。

<div class="method-step__io" markdown="1">

**输入**：当前观测特征$O'_t$与更新前的历史状态特征$S'_{t-1}$。<br>
**输出**：融合当前感知与相关历史线索的特征$EObs_t$。

</div>

**直观理解**：当前观测主动向历史记忆提问，例如“先前抓取的是哪个物体”或“任务已进行到哪一步”，以补回当前画面本身无法提供的信息。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 基于注意力相关性的门控状态更新

$$
R=\frac{1}{LHN_o}\sum_{l=1}^{L}\sum_{h=1}^{H}\sum_{j=1}^{N_o}A_{:,j}^{(l,h)},\qquad G_t=\sigma(R),\qquad S_t=G_t\odot(\mathrm{Inter}\cdot S_t)+(1-G_t)\odot S_{t-1}
$$

**符号说明**

- $A_{:,j}^{(l,h)}$：第$l$层、第$h$个注意力头中，所有状态槽对第$j$个观测特征的预Softmax跨注意力logits向量
- $L$：参与汇总的跨注意力层数
- $H$：每层的注意力头数
- $N_o$：当前观测特征向量的数量
- $R$：跨层、跨头并跨观测位置平均后得到的逐状态槽全局相关性
- $\sigma$：Sigmoid函数，将相关性映射到零至一之间
- $G_t$：时刻$t$的逐状态槽更新门，形状为$N_s\times1$
- $\mathrm{Inter}\cdot S_t$：由历史状态查询当前观测后产生的候选中间状态
- $S_{t-1}$：更新前缓存的历史潜状态
- $S_t$：门控融合后得到的新潜状态
- $\odot$：逐元素乘法；门值沿特征维广播

<div class="equation-explanation" markdown="1">

**直观理解**：该式先把所有层、注意力头和观测位置的原始匹配分数压缩成每个状态槽的写入强度，再在新候选与旧记忆之间插值。与无条件覆盖相比，它使强相关观测更多地更新状态，而弱相关或噪声观测更多地保留旧状态。<br>
**原文位置**：Self-Evolving Gated Attention节，式(8)—(10)，对应图3(b)

</div>

</div>

<div class="equation-block" markdown="1">

#### 历史状态检索与动作生成

$$
\mathit{EObs}_t=\operatorname{CA}(O'_t,S'_{t-1},S'_{t-1}),\qquad A_t=\operatorname{Diffusion}(\mathit{EObs}_t)
$$

**符号说明**

- $O'_t$：经多头自注意力处理的当前观测特征，在检索中充当Query
- $S'_{t-1}$：经多头自注意力处理的历史状态特征，在检索中同时充当Key和Value
- $\operatorname{CA}$：跨注意力运算
- $\mathit{EObs}_t$：从历史状态中检索线索后形成的增强观测特征
- $\operatorname{Diffusion}$：以增强观测为条件的扩散动作生成过程
- $A_t$：时刻$t$预测的未来动作序列，包含$N$个14自由度动作

<div class="equation-explanation" markdown="1">

**直观理解**：检索流反转了更新流的查询方向：不是让记忆读取当前画面，而是让当前画面查询历史记忆。得到的上下文特征再作为扩散模型的条件，使动作预测能利用早于固定观测窗口的任务信息。<br>
**原文位置**：Overview of SeedPolicy节式(4)及Self-Evolving Gated Attention节式(11)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：所给Method节选没有给出扩散模型的具体训练损失、噪声参数化、时间步采样方式或SEGA是否具有额外监督项，因此不能据此重建完整优化目标。可以确认的是，SEGA、观测编码器与Diffusion Action Expert组成端到端策略；SEG的门值由跨注意力logits直接计算，节选中未报告独立的门控标签或辅助门损失。原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Self-Evolving Gated Attention（SEGA）**

SEGA维护固定容量的时变潜状态$S_t\in\mathbb{R}^{N_s\times D}$，并采用并行双流Transformer结构：更新流把$O_t$写入状态，检索流用历史状态增强当前观测。由于每个时刻只接收固定观测窗口和缓存状态，其有效时间感受野可随递归运行增长，而无需堆叠越来越多的原始帧。

> 直观理解：SEGA相当于一个容量固定但内容持续演化的工作记忆；机器人不必反复重读全部历史，而只需更新和查询这份摘要。

**2. Self-Evolving Gate（SEG）**

SEG不额外建立独立相关性预测器，而是汇总状态到观测的跨注意力预Softmax logits，得到每个状态槽的相关性$R$，再经Sigmoid形成$G_t\in\mathbb{R}^{N_s\times1}$。$G_t$控制候选状态$\mathrm{Inter}\cdot S_t$与旧状态$S_{t-1}$的融合比例，从结构上施加时间稀疏更新。

> 直观理解：注意力分数本来就在衡量历史槽与当前观测是否匹配，SEG把这一信号兼作“是否写入”的开关，因此能过滤无关帧或视觉干扰。

**3. Diffusion Action Expert**

动作专家是以$EObs_t$为条件的Transformer式扩散模型，负责生成长度为$N$的未来14自由度动作序列$A_t$。SEGA只改进提供给动作专家的时序条件表示，而动作分布仍由扩散过程建模。

> 直观理解：SEGA负责记住和找回任务历史，动作专家负责把这些信息转换为具体控制；这种分工使长时记忆改进可以直接接入扩散策略。

**训练与推理**

训练阶段的样本组织与扩散损失在所给节选中未明确报告；从框架描述只能确定，专家示范中的RGB图像和关节位姿经编码及SEGA处理，增强观测作为条件输入动作扩散专家，整体用于模仿专家未来动作序列。推理时按控制时序递归运行：初始化状态后，在每个$t$读取$I_t$和$P_t$，计算$O_t$；SEGA并行检索$S_{t-1}$以产生$EObs_t$，并门控更新得到$S_t$；动作专家由$EObs_t$生成$A_t$，同时缓存$S_t$供下一时刻使用。由于$S_{t-1}$已经由上一步计算并缓存，方法无需在每次控制时重新编码全部历史观测。

**复现信息**

公平理解该方法所需的结构信息包括：RGB视觉编码器为ResNet，框架图还标明关节位姿使用MLP；潜状态含$N_s$个、每个维度为$D$的状态槽，当前观测含$N_o$个同维特征；动作专家是Transformer式扩散模型，输出$N$个未来14自由度动作。所给节选未明确报告ResNet具体型号、$N_s$、$N_o$、$D$、$N$、SEGA层数$L$、注意力头数$H$、状态初始化方法、扩散步数、优化器、学习率或训练轮数，复现时必须回查论文其他章节或代码，不能由本节推断。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- RoboTwin 2.0是主要仿真基准：使用ALOHA-AgileX机器人评测50个操作任务，每个任务提供50条专家演示。每个策略训练600个epoch，并在每项任务上执行100次测试回合；结果取3次独立试验的平均成功率。Easy设置为训练和测试均使用干净环境，Hard设置为干净数据训练、随机化环境测试，后者主要检验分布偏移下的鲁棒性。
- RMBench用于补充检验SeedPolicy在另一套机器人操作评测体系中的泛化表现。论文称遵循该基准原始设置与评测协议，但所给章节未说明任务数量、数据划分或具体结果，详细分析被放在附录第4节。
- MimicGen是基于生成式示范数据的机器人操作基准，用于判断方法是否只对RoboTwin 2.0有效。论文称沿用原始评测协议，但所给章节未报告其任务规模、训练集划分和具体分数；此外，真实机器人实验使用Dexmal DOS W1、固定Intel RealSense D435 RGB相机和5项具有状态歧义的任务，每项收集50条演示并进行两轮、每轮50次测试。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**平均成功率**

统计机器人完整完成任务的测试回合比例，并在RoboTwin 2.0上进一步对3次独立试验取均值；它直接衡量端到端任务完成能力，但不能单独反映动作平滑性、失败类型或完成速度。 （越高越好，因为更高比例表示策略在更多测试回合中满足任务成功条件。）

</div>
<div class="metric-item" markdown="1">

**相对成功率提升**

以DP成功率为参照计算SeedPolicy的比例增益，用来比较Easy与Hard等不同难度设置下的改善幅度。相对提升可能在基线绝对成功率较低时被放大，因此应与绝对成功率共同解读；所给材料未提供相应绝对分数。 （越高越好，因为它表示相对于同设置下DP基线的改善更大。）

</div>
<div class="metric-item" markdown="1">

**参数量**

衡量策略模型包含的可训练参数规模，用于评估达到给定成功率所需的模型容量与部署成本；参数更少通常意味着存储和训练负担较低，但不等同于实际推理延迟或能耗更低。 （在性能相当或更高时越低越好，因为这表示更高的参数效率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### RoboTwin 2.0的Easy干净设置，结果在CNN与Transformer两种骨干上取平均

<div class="result-value" markdown="1">

作者报告SeedPolicy相对DP取得36.8%的平均相对提升，表明在训练与测试条件一致时，显式时间状态仍能改善操作成功率。

</div>

该结果支持SeedPolicy不仅在环境扰动下有效，在标准同分布测试中也能优于固定窗口DP。不过，所给材料没有提供两者的绝对成功率、方差或逐任务成绩，因此无法判断36.8%的相对提升对应多大的绝对百分点变化，也不能据此确认所有50项任务均有提升。

<div class="result-source" markdown="1">

来源：摘要；表1被提及，但所给节选未包含表中数值行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Averaged across both CNN and Transformer backbones, SeedPolicy achieves 36.8% relative improvement in clean settings and 169% relative improvement in randomized challenging settings over the DP.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### RoboTwin 2.0的Hard随机化测试设置：使用干净环境数据训练，在随机化环境中测试，并对CNN与Transformer骨干取平均

<div class="result-value" markdown="1">

作者报告SeedPolicy相对DP取得169%的平均相对提升，且该增幅明显大于Easy设置中的36.8%。

</div>

这一结果说明SEGA积累并筛选历史信息的机制可能在视觉条件或场景状态发生变化时更有价值，即策略不必只依赖当前短窗口作出判断。但相对提升可能受到DP在Hard设置下绝对成功率较低的影响；缺少绝对分数、置信区间和失败类型分析时，不能把169%直接解释为接近完美的鲁棒性。

<div class="result-source" markdown="1">

来源：摘要；RoboTwin 2.0的Easy/Hard协议见Experiments—Setup—Simulation Benchmark

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Averaged across both CNN and Transformer backbones, SeedPolicy achieves 36.8% relative improvement in clean settings and 169% relative improvement in randomized challenging settings over the DP.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 不同任务长度以及CNN、Transformer两种架构下的趋势比较

<div class="result-value" markdown="1">

图4的作者结论是：任务越长，SeedPolicy与固定窗口基线之间的性能差距越大，而且这一趋势在两种架构中一致。

</div>

这是支持“时程扩展”主张的关键趋势证据：若优势随任务长度增加而扩大，则改进更可能来自长期上下文建模，而非单纯增加模型容量。它仍是相关性证据；所给节选没有图4的具体分组分数、误差条或任务长度定义，因此无法量化增长速度，也不能排除长任务同时具有更高感知或控制难度等混杂因素。

<div class="result-source" markdown="1">

来源：图4：Performance comparison across varying task length

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A consistent trend emerges in both architectures: as the task length increases, the performance gap between SeedPolicy and the baseline progressively widens.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给章节缺少表1的完整数值、图4数据点、误差范围、显著性检验及逐任务结果。摘要中的36.8%和169%均为相对提升，若没有绝对成功率便容易高估实际收益；三次独立试验也不足以充分刻画高方差机器人评测。
- RMBench、MimicGen、真实机器人结果和关键消融被指向附录但未出现在材料中；RDT等VLA结果还被标为不可直接比较。因此，当前证据可以支持SeedPolicy在RoboTwin 2.0上的总体趋势，却不足以独立核验其“最先进”、跨基准泛化和实际部署效率等更强结论。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 标准Diffusion Policy（DP）是最关键基线。它同样以扩散模型表示多模态动作分布，但主要依赖固定观察窗口；与其比较可直接判断SEGA式持续状态更新是否缓解了长时程时间建模瓶颈。
- 其他模仿学习基线用于判断提升是否仅来自对DP实现的局部优化。所给章节未列出这些方法的名称、配置和逐项成绩，因此无法进一步核验比较是否完全同规模、同输入或同训练预算。
- RDT是参数量约12亿的视觉—语言—动作模型（VLA）对照，用于比较小型专用模仿学习策略与大规模预训练模型的性能—参数效率。论文同时提示表1中灰色VLA结果不可直接比较，因此该对照更适合作为效率参照，而非严格受控实验。
- CNN与Transformer骨干下对应的固定窗口策略构成架构层面的内部基线。它们用于检查SeedPolicy的增益是否依赖某一种视觉或序列骨干，而不是检验不同学习范式之间的优劣。

**实验想回答的问题**

- SeedPolicy及其核心时间模块SEGA能否在长时程机器人操作中稳定优于标准扩散策略与其他模仿学习方法，尤其是在测试环境发生随机变化的困难设置下？
- 性能增益是否来自有效的长期记忆与时间建模设计，并且能否跨CNN和Transformer骨干网络、不同任务长度以及真实机器人场景保持一致？

**实验实现**

RoboTwin 2.0中，每项任务使用50条专家演示训练600个epoch，再执行100次测试回合，并报告3次独立试验的平均成功率。真实机器人实验中，每项任务同样收集50条演示、训练600个epoch，并进行两轮各50次回合的评测。SeedPolicy使用长度为$T_{\mathrm{obs}}=3$的观察历史，输入包括$320\times240$ RGB图像与14自由度关节位姿；潜在状态长度为$N_s=60$、维度为$D=256$。训练采用AdamW、批量大小128、初始学习率$10^{-4}$、余弦衰减和500步预热，在单张NVIDIA RTX 4090D GPU上完成。真实机器人实验和消融默认采用Transformer骨干。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 改变任务长度，并分别在CNN与Transformer骨干上比较SeedPolicy和固定窗口基线 | 原文未明确报告各长度分组的数值，只报告随着任务变长，SeedPolicy相对基线的差距持续扩大，且两种架构趋势一致。 | 这一分析隔离了方法对时间跨度的敏感性：如果只是普通容量增益，差距未必会随任务长度系统性扩大；当前趋势因而支持SEGA主要改善长期依赖建模。不过，没有具体数值和统计检验，证据强度低于完整消融表。 | 图4及其说明<br><span class="experiment-evidence">This validates the architecture-agnostic effectiveness of our approach, demonstrating that the advantage of our explicit temporal modeling becomes increasingly significant in long-horizon scenarios compared to fixed-window baselines.</span> |
| SEGA与其他记忆机制、以及SeedPolicy内部设计选项的消融 | 原文未明确报告。 | 实验问题Q3和Q4表明作者计划比较现有记忆机制并分析关键设计，但所给节选没有列出被比较模块、移除组件后的成功率或计算开销。因此无法判断门控、注意力、持续潜在状态长度等设计各自贡献了多少，也无法确认增益是否可由更简单的循环记忆替代。 | Experiments开头的研究问题；具体消融结果未包含在所给节选中<br><span class="experiment-evidence">Q3: How does SEGA compare with existing memory mechanisms?</span> |

**定性案例**

- 真实机器人评测选择Looping_Place-Retrieval、Sequential_Picking、Bottle_Handover、Food_Replacement和Cover_and_Reveal五项任务，目标是检验“状态歧义”：当前画面可能不足以唯一确定下一步动作，策略需要利用早先观察区分任务阶段。该设计在概念上直接对应SEGA的长期记忆能力，但所给材料未提供成功率、视频案例或典型失败过程，因此只能确认评测意图，不能确认实际效果。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文提出具有长期时序状态建模能力的扩散模仿学习策略，以改进长程机器人操作。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`a02e0a62bc8413f65bef48a7f7b598c62f69333c528ddc085e2085d7b34a4969`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
