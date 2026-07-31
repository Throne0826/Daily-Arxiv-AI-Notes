---
title: "[论文解读] DLAM: Distributional Latent Actions with Temporal Constraints"
description: "[arXiv 2607.27138][机器人 / 具身智能] DLAM将视频中的潜在动作由确定性向量改为对角高斯分布，并用归一化的时序合成与反转约束同时学习均值和逐维方差，以获得更适合与机器人动作联合生成的转移表征。"
arxiv_id: "2607.27138"
announcement_date: "2026-07-30"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.571485+00:00"
source_sha256: "1c033438e3d994f070b4dd88a91b84e8c2fdd52bb782dbc57778f3649ff199d7"
tags:
  - "机器人 / 具身智能"
  - "视觉—语言—动作模型"
  - "潜在动作模型"
  - "无动作标签视频"
  - "对角高斯转移"
  - "时间组合约束"
  - "反转约束"
  - "流匹配"
  - "机器人策略迁移"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2607.27138</p>

# DLAM: Distributional Latent Actions with Temporal Constraints

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Zuojin Tang, Feifan Luo, Haoyun Liu, Botai Yuan, Dekang Qi, Ronghan Chen, Yandan Yang, Tong Lin, Xinyuan Chang, Mu Xu, Bin Liu, De Ma, Zhiheng Ma</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27138v1) · [PDF 下载](https://arxiv.org/pdf/2607.27138v1) · **关键词** 视觉—语言—动作模型, 潜在动作模型, 无动作标签视频, 对角高斯转移, 时间组合约束, 反转约束, 流匹配, 机器人策略迁移<br>


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

DLAM将视频中的潜在动作由确定性向量改为对角高斯分布，并用归一化的时序合成与反转约束同时学习均值和逐维方差，以获得更适合与机器人动作联合生成的转移表征。

**不用术语来说**：机器人策略通常需要带有动作指令的示范数据，但这类数据昂贵且稀缺；普通视频虽然数量丰富，却只展示“画面如何变化”，没有说明机器人采取了什么动作。已有方法可从相邻画面中压缩出表示变化的隐藏编码，但这些编码可能主要记录相机移动、背景变化或外观差异，而且把每次变化视为一个完全确定的点。当模型把多段变化连续拼接起来时，局部估计误差可能逐步累积，最终使该编码难以可靠地辅助机器人控制。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出分布式潜在动作模型DLAM：将帧间转移表示为对角高斯分布，使时序监督不只约束代表主要视觉变化的均值，也约束各潜在维度的方差；解码重建仅使用均值，从而保持表征与实际观测变化的联系。
- 提出面向等时间间隔帧三元组的归一化合成与反转约束，并在方差合成中引入共享相关系数以处理相邻转移共享中间帧所导致的依赖；迁移时冻结编码器，仅将均值序列作为辅助生成目标，与机器人动作共同用于流匹配策略训练。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于机器人学习中的视觉—语言—动作（Vision-Language-Action, VLA）与潜在动作建模交叉方向。VLA策略根据视觉观测和语言指令生成机器人动作，但训练通常依赖成本高昂的动作标注示范；相比之下，大量无动作标签视频记录了物体与场景如何随时间变化。潜在动作模型（LAM）试图从视频帧之间的变化中推断不可直接观测的“动作式”转移表示，再将这种表示用于机器人策略学习。本文关注的关键背景是：仅靠下一帧重建得到的潜变量虽然能预测视觉变化，却可能混入相机运动、背景动态或外观变化，因而未必具有适合控制的时间结构；已有结构化LAM加入组合、反转等时间约束，但通常把一次转移表示成确定性向量，无法显式描述局部转移估计的不确定性及其在递归组合中的传播。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉—语言—动作模型（VLA）**

一种机器人策略模型，以当前视觉观测和自然语言任务指令为条件，输出可执行的机器人动作。本文不重新设计VLA主干，而是把从无标签视频学到的潜在转移作为辅助生成目标接入现有策略。

</div>
<div class="concept-item" markdown="1">

**潜在动作模型（LAM）**

LAM从两个或多个视频帧的变化中推断一个低维潜变量，用它概括帧间发生的转移，而不要求视频带有真实机器人动作标签。该潜变量并不天然等同于物理动作，因此需要重建或时间关系约束来使其与可控变化对齐。

</div>
<div class="concept-item" markdown="1">

**对角高斯转移**

DLAM不把一次帧间转移表示为单个确定点，而表示为各维度相互简化建模的高斯分布，由均值和逐维方差刻画。直观上，均值表示模型认为最可能发生的视觉转移，方差则表示各潜在维度上的不确定程度。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

预训练阶段的输入是无动作标签视频中的帧对，以及用于施加时间约束的等时间间隔帧三元组。编码器要从任意帧对推断一个对角高斯转移，其输出包含转移均值和逐维方差；以源帧为条件的解码器仅使用均值重建目标帧。训练还要求相邻两段转移的组合与跨越两段时间的直接转移一致，并要求正向与反向转移满足均值取负、方差保持不变的关系；组合方差额外使用共享相关系数处理相邻转移因共享中间帧而产生的依赖。下游迁移时冻结编码器，从机器人示范的连续图像中提取均值转移序列，并在受控的 π₀ 策略框架内通过流匹配联合生成潜在转移与真实机器人动作；未来帧只用于构造训练目标，部署时仅执行动作输出。该设置假定视频中的时序变化能够提供有助于控制的转移先验，但不假定潜在转移严格满足全局群结构。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mu$**

帧间高斯转移的均值，即用于目标帧重建并在下游作为辅助生成目标的中心转移表示。

</div>
<div class="notation-item" markdown="1">

**$\sigma^2$**

高斯转移的逐维方差，用于表示各潜在维度的不确定程度，并接受组合与反转约束；下游策略不直接使用该方差。

</div>
<div class="notation-item" markdown="1">

**$\rho$**

组合相邻转移方差时使用的轻量共享相关系数，用于考虑两段转移因共享中间帧而并非独立；原文节选未给出其完整公式。

</div>
<div class="notation-item" markdown="1">

**$\pi_0$**

论文采用的受控下游VLA迁移框架，用于比较不同潜在动作表示对策略性能的影响。

</div>

</div>

**直接相关的工作**

- **Genie（Bruce et al., 2024）**: 原文将其列为从视频学习潜在动作的代表工作之一。这类方法通常通过视觉重建使潜变量对应观测变化，但重建目标本身不能保证所得表示具有适合机器人控制和长时组合的时间结构。
- **ALAM（Tang et al., 2026a）**: 与DLAM最直接相关的结构化潜在动作方法：它对确定性的转移点施加组合与反转关系。DLAM进一步把转移扩展为对角高斯，使时间约束同时作用于均值和逐维方差，并在方差组合中考虑相邻转移的相关性。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

视觉—语言—动作模型的扩展依赖大量带动作标签的机器人示范，而采集这类数据需要真实机器人、人工操作和安全控制，成本较高。海量无动作标签视频提供了丰富的物理变化信息，因此关键需求是把这些视频中的转移规律提取成真正有助于下游控制的表征，而不只是有助于预测下一帧的视觉特征。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于重建的潜在动作模型**：编码器根据一对视频帧推断潜在转移编码，解码器以该编码为条件重建目标帧；重建损失迫使编码携带从源帧到目标帧的可预测变化信息。
- **确定性的结构化潜在动作模型**：在重建之外加入合成、反转、逆变换或循环一致性等时序关系，使不同时间段的潜在转移满足一定结构；但每段转移仍由单个确定性向量表示，所有关系都直接作用于这个点估计。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 仅靠画面重建无法保证潜在编码与可控动作对齐：编码可能吸收相机运动、背景动态或外观变化。这些信息虽能降低帧预测误差，却可能与机器人应执行的动作关系很弱，因而不适合直接作为动作联合生成的辅助目标。
- 现有结构化方法没有表达转移估计的不确定性。相邻转移本身可能含有残余误差，而且因共享中间帧而并非相互独立；若仍以确定性点进行递归合成，误差可能随时间跨度扩大而传播和累积。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前缺少一种面向无动作标签视频的潜在动作表示，能够在保留重建锚定作用的同时，显式刻画每个转移各维度的不确定性，并以考虑相邻转移相关性的方式约束跨时间合成与反转，最终还能无须额外潜在动作解码器地接入现有VLA策略。

</div>
<div markdown="1"><span>核心问题</span>

把帧间潜在转移建模为对角高斯，并联合约束其均值、逐维方差及相邻转移的相关性，能否比确定性潜在动作获得更一致的时序结构，并使从无标签视频学到的变化先验更有效地迁移到机器人动作生成？

</div>
<div markdown="1"><span>作者直觉</span>

均值可理解为模型对“这两帧之间主要发生了什么”的最佳估计，方差则表示各个隐藏变化维度有多不确定。两段变化拼接时，不仅应把主要变化合起来，也应传播其不确定性；由于两段相邻转移共享中间帧，使用一个轻量相关系数比假定二者完全独立更合理。反向观看同一变化时，变化方向应取反，而不确定程度应保持不变。这样，模型既被重建任务拉回真实画面变化，又被局部时序规律限制，不必假设整个视频严格满足全局代数结构；下游只使用较稳定的均值序列，可避免让策略直接处理方差，同时获得比纯重建编码更适合控制的训练信号。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

DLAM把无动作标注视频中的帧间变化表示为一组对角高斯潜在动作 token，而不是单个确定性向量。预训练时，从等间隔三帧中同时编码相邻、跨段和反向转移；解码器依据源帧与转移均值重建目标帧，使均值描述可观察的视觉变化。随后，模型要求两段相邻转移的归一化组合与直接跨段编码一致，并要求反向转移的均值取反、方差保持不变；相邻转移共享中间帧，因此方差传播还加入一个有界的共享相关系数。完整目标联合优化重建、标准高斯先验、组合一致性和反转一致性。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 等间隔视频转移构造

采样满足 a<b<c 且 b-a=c-b=k 的三元组 ($O_a,O_b,O_c)$，构造前向转移集合 {(a,b),(b,c),(a,c)}，并额外编码反向对 (b,a)。这些样本分别提供相邻转移、直接长跨度转移和方向反转监督。

<div class="method-step__io" markdown="1">

**输入**：无动作、语言或本体感觉标签的视频帧。<br>
**输出**：四个有序帧对及其共享的等间隔时间关系。

</div>

**直观理解**：模型不需要知道机器人做了什么，只比较画面怎样从起点变到终点。三帧结构使它能够检查“分两步走”是否与“直接走到终点”一致。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分布式潜在转移编码与重建

关系编码器 E_φ 使用 K 个可学习查询，输出 K×d 的均值与原始对数方差；对数方差经区间裁剪和指数变换得到正标准差，从而形成按 token 槽位分解的对角高斯后验。源条件解码器 D_ω 只使用 $O_i$ 和转移均值重建 $O_j$，并以像素均方误差训练。

<div class="method-step__io" markdown="1">

**输入**：任意有序帧对 ($O_i,O_j)$。<br>
**输出**：转移后验 $q_φ(Z_i^j|O_i,O_j)$、其均值和逐维方差，以及重建帧。

</div>

**直观理解**：每次视觉变化不再被压成一个固定点，而被描述成“中心位置加各维度的分散程度”。但画面重建只读取中心，因此均值必须真正概括从源帧到目标帧的变化，而不能依赖随机采样。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 均值与方差的时间关系约束

对应 token 槽位的相邻转移以 1/√2 归一化相加；均值按同样规则组合，方差则依据两段方差及共享相关系数 ρ 传播，再与直接编码的 $q_a^c$ 匹配。反转算子将均值取负并保持方差，以约束 $q_a^b$ 与变换后的 $q_b^a$ 一致。

<div class="method-step__io" markdown="1">

**输入**：相邻后验 $q_a^b$、$q_b^c$，直接后验 $q_a^c$，以及反向后验 $q_b^a$。<br>
**输出**：组合损失 $L_comp$、反转损失 $L_rev$，以及具有近似时间一致性的转移表示。

</div>

**直观理解**：这相当于同时检查“两小步是否等于一大步”和“往回走是否抵消往前走”。归一化避免转移尺度随组合而无控制地增长，相关项则承认两段转移因共享中间帧而不一定相互独立。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 冻结编码器并迁移到联合策略

丢弃重建解码器并冻结编码器，从每个视角的 H 对连续未来帧提取 H 个转移均值序列；策略通过联合流匹配同时学习生成各视角潜在转移轨迹和可执行动作轨迹。方差不传给策略，未来示范帧仅在训练期间用于构造潜在监督目标。

<div class="method-step__io" markdown="1">

**输入**：带机器人动作的示范序列、多个相机视角的连续帧，以及预训练完成的转移编码器。<br>
**输出**：能够联合预测潜在视觉变化与机器人动作的策略；部署时仅执行动作流。

</div>

**直观理解**：预训练编码器先把未来示范画面翻译成紧凑的“变化目标”，策略再学习让动作与这些目标共同出现。实际运行时没有未来画面，策略自己生成变化轨迹作为辅助思考，但机器人只执行生成的动作。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 相关性感知的归一化组合

$$
\bm{Z}_{a\rightsquigarrow c}=\frac{\bm{Z}_{a}^{\,b}+\bm{Z}_{b}^{\,c}}{\sqrt{2}},\qquad \overline{\bm{\mu}}_{a}^{\,c}=\frac{\bm{\mu}_{a}^{\,b}+\bm{\mu}_{b}^{\,c}}{\sqrt{2}},\qquad (\overline{\bm{\sigma}}_{a}^{\,c})^{2}=\frac{(\bm{\sigma}_{a}^{\,b})^{2}+(\bm{\sigma}_{b}^{\,c})^{2}}{2}+\rho\,\bm{\sigma}_{a}^{\,b}\odot\bm{\sigma}_{b}^{\,c},\qquad \rho=\rho_{\max}\tanh(r)
$$

**符号说明**

- $\bm{Z}_{a}^{\,b},\bm{Z}_{b}^{\,c}$：从帧 a 到 b、从帧 b 到 c 的对应槽位随机转移 token。
- $\bm{Z}_{a\rightsquigarrow c}$：由两段相邻转移归一化组合得到的 a 到 c 随机转移。
- $\bm{\mu}_{a}^{\,b},\bm{\mu}_{b}^{\,c}$：两段相邻高斯转移的均值向量。
- $\overline{\bm{\mu}}_{a}^{\,c}$：组合后高斯转移的均值；上横线表示它来自组合而非直接编码。
- $\bm{\sigma}_{a}^{\,b},\bm{\sigma}_{b}^{\,c}$：两段相邻转移的逐维标准差向量。
- $(\overline{\bm{\sigma}}_{a}^{\,c})^{2}$：组合转移的逐维方差向量。
- $\rho$：相邻转移的共享相关系数，在样本、token 槽位和潜在维度之间共用。
- $\rho_{\max}$：固定的相关系数幅值上界，满足 $0<ρ_max<1$。
- $r$：用于参数化相关系数的可学习标量。
- $\odot$：逐元素乘法。

<div class="equation-explanation" markdown="1">

**直观理解**：1/√2 归一化使两个独立标准高斯相加后仍保持单位方差尺度，避免潜变量仅因时间段变长而膨胀。若 ρ=0，方差按独立变量传播；非零 ρ 则修正两段转移共享 $O_b$ 所带来的统计依赖，组合结果随后与直接编码的 a→c 后验比较。<br>
**原文位置**：Method，Temporal Constraints on Mean and Variance，式(5)、式(7)、式(8)，相关系数定义位于式(6)之前

</div>

</div>

<div class="equation-block" markdown="1">

#### DLAM预训练总目标

$$
\mathcal{L}_{\mathrm{DLAM}}=\sum_{s\in\mathcal{S}}\lambda_s\mathcal{L}_s,\qquad \mathcal{S}=\{\mathrm{rec},\mathrm{prior},\mathrm{comp},\mathrm{rev}\}
$$

**符号说明**

- $\mathcal{L}_{\mathrm{DLAM}}$：分布式潜在动作模型的完整预训练损失。
- $\mathcal{S}$：参与联合优化的损失类型集合。
- $\mathcal{L}_{\mathrm{rec}}$：源条件目标帧重建的像素均方误差。
- $\mathcal{L}_{\mathrm{prior}}$：各前向后验相对于因子化标准高斯先验的 KL 散度正则。
- $\mathcal{L}_{\mathrm{comp}}$：直接跨段后验与相邻转移组合后验之间的均值及对数方差差异。
- $\mathcal{L}_{\mathrm{rev}}$：前向后验与经均值取反、方差不变变换后的反向后验之间的差异。
- $\lambda_s$：损失项 s 的权重。
- $s$：重建、先验、组合或反转中的某一损失索引。

<div class="equation-explanation" markdown="1">

**直观理解**：重建项让均值保留可解码的视觉变化，先验项控制潜在分布，组合与反转项则把时间结构写入均值和方差。四项共同训练同一个编码器；其中方差虽不参与重建或下游策略输入，仍会通过先验和时间约束获得学习信号。<br>
**原文位置**：Method，Temporal Constraints on Mean and Variance，式(14)；各组成项见式(3)、式(4)、式(12)、式(13)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：预训练阶段联合更新关系编码器 E_φ、源条件解码器 D_ω 以及共享相关参数 r。$L_rec$ 仅通过转移均值和解码器建立视觉监督；$L_prior$ 将全部前向后验正则到分解的标准高斯，并在最终归约前使用 free-nats 下限；$L_comp$ 和 $L_rev$ 以均值与对数方差的 Frobenius 平方差约束时间关系，因此均值和方差由同一编码器共同优化。迁移阶段不再优化该预训练目标，而是冻结编码器、丢弃解码器，以 $L_transfer=λ_u L_FM^u+Σ_m λ_m L_FM^m$ 联合训练动作流和各相机视角的潜在均值流。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 对角高斯关系编码器**

E_φ 对源帧和目标帧进行关系编码，并借助 K 个可学习查询为每个 token 槽位预测 d 维均值 μ 与对数方差 ℓ。后验在 token 槽位之间因子化，每个槽位采用对角协方差，因此只建模同一 token 各潜变量维度的独立边际尺度。

> 直观理解：均值负责表示“发生了什么变化”，方差为时间组合提供额外可学习结构。论文明确指出该方差不是对未知未来的校准不确定性，因为编码时两个端点都已经可见。

**2. 源条件重建解码器**

D_ω 接收源帧 $O_i$ 和堆叠的转移均值 $μ_i^j$，输出目标帧估计；重建路径不使用后验样本或预测方差。源帧提供场景外观，迫使潜在均值主要携带通向目标帧的视觉变化。

> 直观理解：如果解码器已经看到起始画面，潜在 token 就不必重复存储整个场景，而应重点说明物体怎样移动或状态怎样改变。该解码器只服务预训练，迁移策略时会被丢弃。

**3. 相关性感知的时间约束模块**

模块对相同 token 槽位执行一次 k+k→2k 的归一化组合，并用 $ρ=ρ_max$ tanh(r) 描述共享中间帧的相邻转移之间的逐维交叉协方差；ρ 在样本、token 和维度间共享且满足 |ρ|<1。它还采用均值取反、方差不变的反转算子，并以均值及对数方差的归一化平方差比较后验。

> 直观理解：共享相关系数是一种低成本折中：它不为每个样本学习复杂协方差矩阵，却避免把共享中间帧的两段变化错误地当作完全独立。该组合只定义成对的归一化关系，论文没有宣称它是可任意递归使用的结合律。

**训练与推理**

预训练时，从无标注视频抽取等间隔三元组，编码三个前向帧对及一个反向帧对；直接跨度和相邻跨度均参与重建与先验正则，相邻—直接关系用于组合一致性，正向—反向关系用于反转一致性。重建始终采用后验均值，不进行后验采样；预测标准差只参与高斯后验、先验和时间约束，不能解释为对不可见未来的校准不确定性。

下游训练时，冻结转移编码器，并从每个相机视角的 H+1 个连续示范帧提取 H 个相邻转移均值，作为流匹配策略的潜在轨迹目标；同一策略同时拟合机器人动作轨迹。未来示范帧和冻结编码器只在训练时构造监督，推理时策略直接生成潜在流与动作流，不需要未来观测，也不接收编码器预测的方差，最终仅将动作流发送给机器人执行。

**复现信息**

为公平解释迁移结果，各冻结转移编码器接入同一 $π_0$ 策略：视觉语言骨干为 PaliGemma-2B，动作专家为 Gemma-300M；更新策略骨干、动作专家和投影层，而不更新转移编码器。每个第三人称视角和腕部相机视角分别提供潜在均值目标；策略训练采用 AdamW，学习率 5×10^{-5}、权重衰减 10^{-4}、单设备批量大小 32。预训练中的对数方差按固定上下界逐元素裁剪，相关系数由有界 tanh 参数化；具体 K、d、裁剪边界、各损失权重及 free-nats 数值在所给原文片段中未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 无动作机器人视频预训练集：由 11 个视频数据源混合而成，主要取自 Open X-Embodiment 和 CALVIN。所有潜在动作模型使用同一混合数据、数据顺序和训练预算；Figure 4 给出各来源的可用样本占比与归一化采样概率。原文节选未报告总视频数、总转移数及具体训练/验证划分。
- MetaWorld MT50：包含多种仿真机器人操作任务，用于检验从无动作视频中学习的潜在动态能否迁移到多任务策略学习。摘要说明采用相同的受控 π₀ 迁移协议，但节选未提供任务划分、演示规模或逐任务结果。
- LIBERO 与真实世界操作评测：用于分别检验跨任务仿真操作和真实机器人控制中的迁移效果。原文摘要称 DLAM 在两类评测中均有提升，但所给节选未报告 LIBERO 的具体套件、真实任务名称、数据规模或评测回合数。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**时间一致性**

衡量跨不同时间间隔推断出的潜在转移，能否满足组合与反转关系；它关注潜在空间是否具有可递归使用的时间结构，而不仅是单帧预测准确。所给节选未说明其具体计算公式。 （一致性越强越好，因为相邻转移组合后应接近对应的跨步转移，反向转移也应与正向转移保持规定关系。）

</div>
<div class="metric-item" markdown="1">

**直接与累计重建性能**

直接重建考查单个留出转移的视觉变化预测；累计重建考查模型递归组合或滚动多个转移后能否维持准确性，因而更容易暴露局部误差传播问题。节选未给出具体指标名称或数值。 （重建误差更低或重建质量更高时更好；累计重建改善尤其说明长期递归使用时误差累积较少。）

</div>
<div class="metric-item" markdown="1">

**策略任务性能**

衡量下游策略在 MetaWorld MT50、LIBERO 和真实操作任务上的控制效果，通常用于判断潜在动作先验是否真正帮助机器人完成任务。所给材料未明确其采用成功率、回报还是其他统计量。 （任务完成表现越高越好，但在指标名称、回合数和方差缺失时，只能确认作者报告了相对提升，不能判断提升幅度或统计显著性。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 留出转移上的潜在动态一致性

<div class="result-value" markdown="1">

作者报告 DLAM 相比已有潜在动作基线学到了更具时间一致性的潜在动态。所给材料没有给出具体指标、绝对分数、相对增幅或统计显著性。

</div>

该结果支持分布式转移表示与时间组合/反转约束能够塑造更适合跨时间运算的潜在空间，而不是仅记住单步视觉差异。但由于缺少定量表格，无法判断优势大小，也不能单独确定收益来自高斯表示还是时间约束。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On held-out transitions, DLAM learns more temporally consistent latent dynamics than existing latent-action baselines and achieves stronger direct and cumulative reconstruction on held-out videos.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 留出视频上的直接重建与累计重建

<div class="result-value" markdown="1">

作者报告 DLAM 在直接重建和累计重建两方面均优于已有潜在动作基线，尤其针对递归组合时可能发生的误差传播。原文节选未明确报告任何数值。

</div>

直接重建提升表示模型更好地解释单段视觉变化；累计重建提升则更符合论文的核心主张，即局部转移误差在多步组合中不易持续放大。不过，重建质量不等同于机器人策略成功率，也不能证明潜在变量具有唯一或可解释的物理语义。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On held-out transitions, DLAM learns more temporally consistent latent dynamics than existing latent-action baselines and achieves stronger direct and cumulative reconstruction on held-out videos.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 相同受控 π₀ 迁移协议下的下游策略评测

<div class="result-value" markdown="1">

作者报告 DLAM 在 MetaWorld MT50、LIBERO 和真实世界操作任务上均提升了策略性能。所给材料未提供各基准的具体得分、提升幅度、方差或显著性检验。

</div>

在迁移协议相同的前提下，跨仿真基准与真实任务的一致提升表明潜在动态先验可能对控制有实际价值，而不只是改善视频重建。但现有证据不足以判断其样本效率、对不同任务类别的稳健性，以及是否全面优于每个单独基线。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under the same controlled π₀ transfer protocol, it also improves policy performance on MetaWorld MT50, LIBERO, and real-world manipulation tasks.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验节选主要包含预训练配置，缺少结果表、图中数值、完整基线名称、指标定义、重复实验次数和置信区间。因此上述结果只能按作者摘要中的定性结论复述，无法独立核验提升幅度、统计稳定性或公平比较的全部条件。
- 虽然评测覆盖 MetaWorld MT50、LIBERO 和真实操作任务，但节选未说明真实任务数量、机器人平台、环境变化、失败类型与安全约束，也未报告分布外场景或长时程任务表现，因而不能据此推断方法对开放环境的普遍适用性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 已有潜在动作模型：用于比较 DLAM 的分布式转移表示和时间约束是否优于传统的重建式潜在动作学习。所给节选未列出具体模型名称。
- 采用确定性转移点的结构化潜在动作方法：这是最直接的机制对照，因为此类方法同样施加时间约束，但不能显式表达局部转移的不确定性。具体基线名称及配置原文节选未明确报告。
- 受控模型变体：所有变体共享视觉 tokenizer、Transformer 容量、源帧条件解码器、数据顺序和训练预算，用于隔离归一化均值约束、学习式方差及相关性感知方差组合的作用。
- 相同 π₀ 迁移协议下的下游策略对照：用于避免把策略架构或迁移流程差异误认为潜在动作表征带来的收益。节选未说明 π₀ 的结构、基线策略名称或训练数据量。

**实验想回答的问题**

- 在相同无动作视频预训练条件下，将单步潜在动作表示为对角高斯，并加入归一化的时间组合与反转约束，能否比已有潜在动作基线学到更一致的时间动态，并改善留出视频上的直接重建与递归累计重建？
- 冻结预训练编码器后，使用流匹配策略联合生成潜在转移均值序列与机器人动作，能否在受控的 π₀ 迁移协议下提升仿真及真实机器人操作性能；其中均值约束、方差建模和相关性感知组合分别贡献了什么？

**实验实现**

无动作预训练阶段中，所有受控变体均使用同一套 11 源视频混合、视觉 tokenizer、Transformer 容量、源帧条件解码器、样本顺序和训练预算，以减少数据与模型规模造成的混杂。模型训练 57 个 epoch，使用 64 张 AMD MI308X GPU、AdamW、峰值学习率 10^{-4}、权重衰减 10^{-4}，单卡批量为 64。损失权重设为 $λ_rec=1$、$λ_prior=0.005$、$λ_comp=λ_rev=0.05$、λ_ℓ=0.1。下游阶段冻结编码器并训练流匹配策略，使其联合生成潜在转移均值序列与机器人动作；策略评测使用相同的受控 π₀ 迁移协议。所给节选没有提供随机种子、重复运行次数、置信区间、完整数据划分、解码分辨率或下游训练预算。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除或替换归一化的均值时间约束 | 作者称归一化均值约束解释了大部分重建收益，但所给材料没有报告完整模型与消融模型的重建分数或差值。 | 该消融试图隔离时间组合与反转关系对潜在均值的作用。结论意味着，重建改善主要不是因为模型额外预测了方差，而是因为均值被约束为可稳定组合的视觉变化表示；但缺少数值，无法量化其贡献比例。 | Abstract<br><span class="experiment-evidence">Controlled ablations show that normalized mean constraints account for most of the reconstruction gain, while learned variance and correlation-aware composition provide complementary improvements in downstream control.</span> |
| 学习式方差与相关性感知方差组合 | 作者称学习方差以及使用共享相关系数处理相邻转移依赖，可为下游控制带来互补改进。原文节选未明确报告各组件单独或联合加入时的数值。 | 这一消融针对分布式建模是否超越确定性潜在动作：方差表达每个潜在维度的不确定性，共享相关系数则避免把共享中间帧的相邻转移错误地当作独立变量。所谓“互补”说明两者在均值约束之外仍有增益，但不能据此判断哪一项更重要或增益是否显著。 | Abstract<br><span class="experiment-evidence">Controlled ablations show that normalized mean constraints account for most of the reconstruction gain, while learned variance and correlation-aware composition provide complementary improvements in downstream control.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It proposes a distributional latent-action model for transferring action-free video dynamics into robot manipulation policies.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`1c033438e3d994f070b4dd88a91b84e8c2fdd52bb782dbc57778f3649ff199d7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
