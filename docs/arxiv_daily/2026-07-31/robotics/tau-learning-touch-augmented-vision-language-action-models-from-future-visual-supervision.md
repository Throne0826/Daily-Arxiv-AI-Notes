---
title: "[论文解读] {\\tau}: Learning Touch-Augmented Vision-Language-Action Models from Future Visual Supervision"
description: "[arXiv 2607.24485][机器人 / 具身智能] 本文提出触觉增强的视觉-语言-动作框架 $\\tau$，利用动作条件下的未来视觉特征变化作为训练监督，使高维视觉式触觉表示学习接触交互的时空动态，并将其用于机器人动作生成。"
arxiv_id: "2607.24485"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T05:30:51.286225+00:00"
source_sha256: "c0b0b8777433c63e72169461e7cacd6bf8394fe0bda0fbf45f9ed6e275cdddbe"
tags:
  - "机器人 / 具身智能"
  - "视觉-语言-动作模型"
  - "视觉-触觉-语言-动作学习"
  - "视觉式触觉感知"
  - "接触密集型机器人操作"
  - "跨模态自监督学习"
  - "动作条件化预测"
  - "联合嵌入预测架构"
  - "TacAura"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2607.24485</p>

# {\tau}: Learning Touch-Augmented Vision-Language-Action Models from Future Visual Supervision

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Cheng, Ning, Xu, Jinan, Li, Wanlin, Chen, Yangzhi, Gao, Jing, Wang, Yiqun, Peng, Kelan, Han, Wenjuan</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Beijing Jiaotong University；Beijing Institute for General Artificial Intelligence</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.24485) · [PDF 下载](https://arxiv.org/pdf/2607.24485) · **关键词** 视觉-语言-动作模型, 视觉-触觉-语言-动作学习, 视觉式触觉感知, 接触密集型机器人操作, 跨模态自监督学习, 动作条件化预测, 联合嵌入预测架构, TacAura<br>


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

本文提出触觉增强的视觉-语言-动作框架 $\tau$，利用动作条件下的未来视觉特征变化作为训练监督，使高维视觉式触觉表示学习接触交互的时空动态，并将其用于机器人动作生成。

**不用术语来说**：机器人执行插头插入、按压印章或擦白板等任务时，摄像头往往看不清是否已经接触、受力是否合适以及物体是否发生细微形变；触觉传感器可以补充这些信息，但可用于特定任务的视觉、触觉、语言和动作联合数据通常有限，因此模型很难仅靠常规训练学会哪些触觉变化真正关系到后续操作。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 $\tau$ 框架：在预训练视觉-语言-动作模型上增加触觉编码与适配模块，并以动作条件下的未来视觉特征变化训练动态感知的触觉表示；辅助预测分支仅在训练阶段使用，部署时不增加该分支的推理开销。
- 建立面向接触密集操作的数据基础设施与 TacAura 数据集，提供四类任务中同步的视觉、本体感觉、视觉式触觉和动作数据，为有限联合数据条件下的触觉增强策略学习提供训练与评测基础。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

视觉-语言-动作模型（VLA）利用多模态预训练，把相机观测和自然语言指令映射为机器人动作，适合执行由语义目标驱动的通用操作。然而，在插头插入、按压和擦除等接触密集型任务中，仅凭视觉通常无法可靠判断接触是否发生、受力如何分布以及物体是否产生局部形变。视觉式触觉传感器可将接触表面的细粒度空间变化记录为高维图像信号，为策略补充直接的物理交互线索；本文关注如何在任务专用数据有限的条件下，让这类触觉信号表达随动作演化的交互动态，并与预训练VLA的视觉和语言特征兼容。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉-语言-动作模型（Vision-Language-Action Model, VLA）**

一种机器人策略模型：输入视觉观测与语言指令，输出可供机器人执行的动作或动作序列。预训练使其具备较强的视觉语义理解能力，但视觉信息不一定能揭示接触界面的受力和形变。

</div>
<div class="concept-item" markdown="1">

**视觉式触觉感知（vision-based tactile sensing）**

传感器通过成像方式记录接触表面的形变、纹理或接触分布，产生具有空间结构的高维触觉图像。它比六维力-力矩测量提供更细粒度的局部接触模式，但也更难在少量机器人数据上学习有效的时序表示。

</div>
<div class="concept-item" markdown="1">

**联合嵌入预测架构（Joint-Embedding Predictive Architecture, JEPA）**

JEPA不直接重建未来像素，而是在潜在特征空间中根据上下文预测目标表示。本文借鉴这一思想，用当前触觉表示和后续动作预测未来视觉特征的变化，使触觉编码包含与控制有关的交互动态。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究场景是插接、按压和擦除等需要持续感知物理接触的真实机器人操作。模型在当前时刻接收多视角视觉观测、视觉式触觉信号和语言指令，并结合机器人动作数据学习输出后续动作块；训练时还可访问未来视觉观测，以构造仅用于表示学习的监督信号。核心假设是：后续动作作用于当前接触状态后所引起的未来视觉特征变化，能够反向监督触觉编码器学习动作条件化的时空交互表示；未来信息和辅助预测分支在部署时均不使用，因此推理输入仍限于当前可观测信息。论文将这种包含视觉、触觉、语言和动作的数据与建模设置称为VTLA，并以任务专用数据有限、需要保留预训练VLA能力为主要约束。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\tau$**

本文提出的触觉增强视觉-语言-动作框架名称；其读音及字母构造对应touch-augmented。

</div>

</div>

**直接相关的工作**

- **Joint-Embedding Predictive Architecture（LeCun et al., 2022；Assran et al., 2023）**: 为本文的潜在空间预测监督提供直接思想来源。一般JEPA根据上下文预测目标表示，而本文将预测目标具体化为未来视觉特征的变化，并以当前触觉表示和后续动作作为条件，从而学习面向机器人控制的接触动态。
- **ForceFlow（Zhang et al., 2026b）**: 代表论文所讨论的交互动态建模路线之一。根据本文作者的概括，已有动态方法通常使用六维力-力矩序列描述结构传递的力与力矩变化，尚未充分解决高维视觉式触觉信号中细粒度空间接触模式的动态表示问题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

接触密集型操作的成败取决于视觉难以直接观测的物理交互线索，例如接触状态、力的空间分布和材料或物体的形变。以视觉为主要感知来源的预训练视觉-语言-动作模型因而可能无法及时判断接触是否稳定、插入是否受阻或按压力度是否合适；研究需求是把高分辨率触觉信息有效接入已有模型，同时避免依赖难以大规模采集的任务专用联合数据。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **触觉融合、同步语义对齐与外部动作修正**：这类方法通过专门的多模态融合结构将当前触觉接入策略，将同步视觉与触觉映射到相近的语义空间，或者使用独立触觉模块对视觉-语言-动作模型给出的动作进行后续修正；其主要依据是当前时刻的接触观测。
- **基于力觉序列或大规模触觉训练的动态建模**：部分方法用六维力与力矩序列描述交互随时间的变化，另一些方法依赖较大规模的触觉数据学习通用表示。前者关注结构传递的三维力和三维力矩，后者则试图通过数据规模提升触觉策略或表征的可迁移性。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 多数现有方法主要刻画瞬时接触状态，缺少对“当前触觉、随后动作与未来交互结果”之间关系的显式学习；因此触觉特征可能能够辨认当下是否接触，却未必包含动作生成所需的交互动态。
- 已有时间建模通常采用六维力与力矩序列，难以保留视觉式触觉信号中的细粒度空间接触图案；与此同时，大规模触觉训练对数据量要求较高，不能直接解决任务专用 $VTLA$ 数据有限时的表示适配问题。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未解决：在有限的视觉-触觉-语言-动作数据下，如何为高维视觉式触觉信号学习兼具细粒度空间信息和时间交互动态的表示，并使该表示与预训练视觉-语言-动作模型的语义特征兼容。尤其缺少一种跨模态预测监督，将触觉及后续动作与可观测的未来视觉变化联系起来。

</div>
<div markdown="1"><span>核心问题</span>

能否利用当前触觉表示和随后动作预测未来视觉潜在特征的变化，把这种训练信号用于学习控制相关的触觉动态，并在保留预训练视觉-语言-动作模型能力的同时提高接触密集操作表现，且不增加部署阶段的辅助预测开销？

</div>
<div markdown="1"><span>作者直觉</span>

一次触碰是否有效，最终常会在后续画面中留下结果，例如插头进一步进入接口、印章完成下压或擦除区域发生变化。若模型必须根据当前触觉和将执行的动作预测这种未来视觉变化，它就不能只记住静态接触外观，而需要提取能说明“施加该动作后会发生什么”的触觉线索。作者在潜在特征空间预测变化而非重建像素，使监督更偏向语义和控制结果；训练完成后移除预测分支，触觉编码器仍保留由该任务学到的动态信息。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

τ 是在预训练 $\pi_{0.5}$ 视觉—语言—动作模型上增加触觉通路的端到端策略。每个时刻的输入包括多视角 RGB 图像 $\mathcal{I}_t$、任务语言 $\ell_t$、机器人本体状态 $q_t$，以及左右夹爪的触觉图 $\mathcal{T}_t^L,\mathcal{T}_t^R$；模型把视觉、语言和触觉都转换为同一潜在空间中的 token，再由动作专家通过条件流匹配生成长度为 $H$ 的动作块 $\hat a_{t:t+H}$。触觉图同时包含法向形变与两个方向的剪切形变，因此比单一力值保留了更丰富的接触位置和空间结构。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造视觉—语言—本体—触觉观测

将任务描述与本体状态拼接为 $\tilde\ell_t=[\ell_t;q_t]$，并把双侧触觉图分别组织为归一化的单通道法向图和双通道剪切图，得到扩展观测 $\tilde o_t=\{\mathcal{I}_t,\tilde\ell_t,\mathcal{T}_t\}$。

<div class="method-step__io" markdown="1">

**输入**：时刻 $t$ 的 $N$ 个 RGB 图像 $\mathcal{I}_t=\{\mathcal{I}_t^1,\ldots,\mathcal{I}_t^N\}$、任务描述 $\ell_t$、本体状态 $q_t$，以及左右触觉信号 $\mathcal{T}_t^L$ 和 $\mathcal{T}_t^R$。<br>
**输出**：包含视觉、语言、本体与双侧接触形变信息的统一时刻观测 $\tilde o_t$。

</div>

**直观理解**：视觉说明物体大致在哪里，语言说明要做什么，本体状态说明机器人当前姿态，而触觉补充夹爪已经接触到什么、接触是否滑动或受压。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 编码并对齐双侧触觉 token

共享参数的触觉编码器 $E_{\mathrm{tou}}$ 分别提取左右特征并按 token 拼接，得到 $z_t^{\mathrm{touch}}=[E_{\mathrm{tou}}(\mathcal{T}_t^L);E_{\mathrm{tou}}(\mathcal{T}_t^R)]$；线性适配器 $A_{\mathrm{tou}}$ 再将其投影为与预训练模型潜在空间兼容的 $\mathcal{Z}_t^{\mathrm{touch}}$。

<div class="method-step__io" markdown="1">

**输入**：左右触觉图 $\mathcal{T}_t^L,\mathcal{T}_t^R$。<br>
**输出**：与 VLA 多模态空间对齐的双侧触觉 token 序列 $\mathcal{Z}_t^{\mathrm{touch}}$。

</div>

**直观理解**：这一步相当于先把触觉图翻译成特征，再用一个小型“接口转换器”把这些特征变成原 VLA 模型能够理解的表示。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 多模态融合与动作块学习

三类 token 拼接为 $\mathcal{Z}_t=[\mathcal{Z}_t^{\mathrm{vision}};\mathcal{Z}_t^{\mathrm{language}};\mathcal{Z}_t^{\mathrm{touch}}]$，经大语言模型融合后提供给动作专家；训练时对专家动作加入高斯噪声，并用条件流匹配学习从噪声动作指向专家动作的向量场。

<div class="method-step__io" markdown="1">

**输入**：视觉 token $\mathcal{Z}_t^{\mathrm{vision}}$、语言及本体 token $\mathcal{Z}_t^{\mathrm{language}}$、触觉 token $\mathcal{Z}_t^{\mathrm{touch}}$，以及训练时的专家动作块 $a_{t:t+H}$。<br>
**输出**：部署时可从随机噪声逐步生成未来动作块 $\hat a_{t:t+H}$ 的触觉增强策略。

</div>

**直观理解**：模型不是直接回归单步动作，而是学习如何把随机动作轨迹逐渐“拉回”合理的专家动作轨迹，并一次规划接下来若干步。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 以动作条件化的未来视觉变化监督触觉表示

预测器 $P$ 根据当前触觉和后续动作预测 $K$ 个未来视觉潜变量，并监督预测的视觉变化与冻结梯度的真实视觉变化方向一致；各时间偏移的损失按双侧触觉变化幅度加权，使显著接触转变获得更高权重。

<div class="method-step__io" markdown="1">

**输入**：当前触觉 token $\mathcal{Z}_t^{\mathrm{touch}}$、由专家动作块编码得到的动作 token $\mathcal{Z}_{t:t+H}^{\mathrm{action}}$，以及未来时刻 $t+\Delta_k$ 的 RGB 图像。<br>
**输出**：能够表达“在给定动作下，当前接触将如何改变场景”的触觉表示，以及仅在训练阶段使用的自监督损失 $\mathcal{L}_{\mathrm{SSL}}$。

</div>

**直观理解**：例如，相同的当前触觉在“继续向下压”和“抬起”之后会产生不同结果，因此模型必须同时看触觉与动作才能预测未来；未来图像只充当训练老师，部署时无需额外预测或未来相机输入。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 条件流匹配的模仿学习目标

$$
\mathcal{L}_{\mathrm{IL}}=\mathbb{E}\!\left[\left\|v_{\theta}(a_{t:t+H}^{s},\tilde{o}_{t})-u(a_{t:t+H}^{s}\mid a_{t:t+H})\right\|_{2}^{2}\right],\quad a_{t:t+H}^{s}=s\,a_{t:t+H}+(1-s)\epsilon,\quad u(a_{t:t+H}^{s}\mid a_{t:t+H})=a_{t:t+H}-\epsilon
$$

**符号说明**

- $\mathcal{L}_{\mathrm{IL}}$：监督模仿学习损失。
- $a_{t:t+H}$：从时刻 t 到 t+H 的专家动作块。
- $a_{t:t+H}^{s}$：流时间 s 上由专家动作与高斯噪声线性插值得到的带噪动作。
- $s$：取值位于 [0,1] 的连续流时间。
- $\epsilon$：从标准高斯分布 $\mathcal{N}(0,I)$ 采样的噪声。
- $\tilde{o}_{t}$：包含视觉、语言、本体状态和双侧触觉的扩展观测。
- $v_{\theta}$：参数为 $\theta$ 的动作专家所预测的去噪向量场。
- $u$：由线性概率路径确定的目标速度方向，即专家动作与噪声之差。
- $\mathbb{E}$：对专家动作条件分布、流路径及相关采样变量求期望。

<div class="equation-explanation" markdown="1">

**直观理解**：训练先在专家动作中混入不同程度的随机噪声，再要求动作专家预测应沿哪个方向移动才能回到专家动作。最小化该均方误差后，推理阶段便可从纯噪声出发，沿学到的向量场生成与当前多模态观测相符的动作块。<br>
**原文位置**：Training Strategy，Action Policy Adaptation for VTLA，公式（6）—（7）

</div>

</div>

<div class="equation-block" markdown="1">

#### 触觉加权的未来视觉变化对齐与联合目标

$$
\mathcal{L}_{\mathrm{SSL}}=\frac{\sum_{k=1}^{K}w_{t+\Delta_k}\left(1-\cos\!\left(\Delta\hat z_{t+\Delta_k}^{\mathrm{vision}},\Delta z_{t+\Delta_k}^{\mathrm{vision}}\right)\right)}{\sum_{k=1}^{K}w_{t+\Delta_k}+\delta},\quad \mathcal{L}_{\mathrm{total}}=\mathcal{L}_{\mathrm{IL}}+\lambda\mathcal{L}_{\mathrm{SSL}}
$$

**符号说明**

- $\mathcal{L}_{\mathrm{SSL}}$：未来视觉潜变量变化的加权余弦对齐损失。
- $K$：被预测的未来时间偏移数量。
- $\Delta_k$：相对于当前时刻 t 的第 k 个预定义未来时间偏移。
- $w_{t+\Delta_k}$：由左右触觉图在当前与未来时刻之间的变化幅度计算的权重，并被截断到 [0.2,5.0]。
- $\Delta\hat z_{t+\Delta_k}^{\mathrm{vision}}$：预测的未来视觉潜变量相对当前视觉潜变量的变化。
- $\Delta z_{t+\Delta_k}^{\mathrm{vision}}$：真实未来视觉潜变量相对当前潜变量的变化，目标侧使用停止梯度。
- $\cos$：衡量两个潜在变化向量方向一致性的余弦相似度。
- $\delta$：防止除零的数值稳定常数，原文设为 1e-6。
- $\mathcal{L}_{\mathrm{total}}$：用于端到端联合优化的总损失。
- $\lambda$：预测自监督损失的权衡系数，原文设为 0.3。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标不要求预测未来视觉特征的绝对值，而只比较“未来相对现在朝哪个方向变化”，从而突出交互动态。触觉变化越明显，对应未来状态的监督权重越大；总目标则同时保证策略会模仿专家动作，并迫使触觉表示学习与接触演化有关的信息。<br>
**原文位置**：Training Strategy，Joint Fine-tuning with Predictive Self-Supervision，公式（8）—（10）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练样本由当前扩展观测 $\tilde o_t$ 与后续专家动作块 $a_{t:t+H}$ 配对。总目标为 $\mathcal{L}_{\mathrm{total}}=\mathcal{L}_{\mathrm{IL}}+\lambda\mathcal{L}_{\mathrm{SSL}}$：前一项直接训练条件流动作策略，使生成动作贴近专家演示；后一项通过动作条件化的未来视觉变化，为触觉编码器和适配器提供额外表示监督。真实未来视觉潜变量在目标侧停止梯度，避免模型通过移动监督目标来虚假降低损失；触觉变化权重则把学习资源集中到插入、压印或擦拭过程中真正发生接触转变的片段。原文将 $\lambda$ 设为 $0.3$，将触觉权重限制在 $[0.2,5.0]$，以免几乎无变化的片段或异常大的传感器变化支配优化。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 预训练 $\pi_{0.5}$ VLA 骨干**

骨干编码多视角 RGB、语言和本体状态，并通过大语言模型形成多模态表示；动作专家使用条件流匹配，从噪声生成未来动作块 $\hat a_{t:t+H}$。τ 保留该预训练感知与动作生成基础，再通过联合微调使其利用新增触觉 token。

> 直观理解：预训练骨干已经具备视觉理解、指令理解和基本机器人动作先验，因此方法不必依靠规模有限的 TacAura 数据从零学习完整策略。

**2. 触觉编码与潜在空间适配模块**

触觉编码器 $E_{\mathrm{tou}}$ 由 $\pi_{0.5}$ 的视觉编码器初始化，并在左右传感器之间共享；其输出经可学习线性适配器 $A_{\mathrm{tou}}$ 投影为 LLM 对齐的触觉 token，再与视觉和语言 token 在 token 维度拼接。

> 直观理解：高维触觉图与普通 RGB 图结构相似，但其含义和特征分布不同；视觉初始化提供图像处理起点，适配器则缩小触觉表示与原模型多模态表示之间的接口差异。

**3. JEPA 式未来视觉预测分支**

真实动作块先经向量化和两层 MLP 动作编码器 $E_{\mathrm{act}}$ 形成动作 token；三层全连接、采用 GELU 激活的预测器 $P$ 接收触觉与动作 token，预测多个偏移 $\Delta_k$ 对应的未来视觉潜变量。监督目标由预训练视觉编码器 $E_{\mathrm{vis}}$ 从未来 RGB 图像提取，并通过停止梯度避免目标分支被预测损失反向改变。

> 直观理解：该分支要求触觉表示不仅识别“现在是否接触”，还要包含足以推断接触过程如何演化的信息；在潜在空间比较而非重建像素，可把学习重点放在与任务状态变化有关的高层特征上。

**训练与推理**

训练阶段，从同步专家轨迹 $\{(\tilde o_t,a_t)\}_{t=1}^{T}$ 中抽取当前观测和未来动作块。视觉、语言、本体与触觉经各自编码和融合后，动作专家接收带噪动作并优化 $\mathcal{L}_{\mathrm{IL}}$；与此同时，真实专家动作经 $E_{\mathrm{act}}$ 编码，与当前触觉 token 一起预测多个未来视觉潜变量变化，并以未来 RGB 经 $E_{\mathrm{vis}}$ 得到的停止梯度特征优化 $\mathcal{L}_{\mathrm{SSL}}$。两个目标联合反向传播，从而同时调整触觉通路和适应后的策略参数；原文将这一过程描述为端到端联合微调。

推理阶段只需当前 RGB、任务语言、本体状态和左右触觉信号。模型生成对齐后的触觉 token，与视觉和语言 token 融合，再由动作专家从噪声生成未来动作块 $\hat a_{t:t+H}$；JEPA 预测器、真实动作编码、未来 RGB 目标和自监督损失均不参与部署。因此，未来视觉监督增加的是训练信号，而不是运行时传感器需求或预测分支开销。

**复现信息**

触觉传感器为夹爪左右两侧的 DM-Tac WS，原始反馈分辨率为 $320\times240$、约 $40$ FPS；每侧输入由分别归一化的法向单通道图和剪切双通道图拼接而成。触觉编码器由 $\pi_{0.5}$ 视觉编码器初始化并在左右侧共享，潜在空间适配器为可学习线性层；动作编码器是两层线性 MLP，JEPA 预测器是带 GELU 激活的三层全连接 MLP。训练数据流按时间戳对齐并降采样到 $10$ Hz；这些设置关系到跨模态同步与触觉输入结构，因而是复现和公平解释方法所必需的。预测分支采用多个预定义未来偏移 $\{\Delta_k\}_{k=1}^{K}$，但所给章节未明确报告 $K$、各 $\Delta_k$、动作块长度 $H$ 或条件流推理步数的具体取值。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- TacAura：作者提出的同步视觉、本体感觉与基于视觉的触觉信号数据集。实验使用其中四项真实机器人接触密集型任务：插头插入、USB插入、印章按压和白板擦除；每项任务用100条专家示范训练。泛化实验选取USB插入和白板擦除，并为每项任务设置两个未见物体及两个未见干扰物集合。原文节选未明确报告训练/验证划分、总轨迹数或各模态采样规模。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**分阶段成功率**

统计20次试验中到达各任务阶段的比例。插入任务依次评估抓取、对准并开始插入、完全插入；按压和擦除任务依次评估拾取、建立有效接触、形成完整印记或完全擦除目标区域。该指标可区分失败发生在粗粒度取物、接触建立还是最终精细执行阶段。 （越高越好，因为更高比例表示策略更稳定地完成相应阶段。）

</div>
<div class="metric-item" markdown="1">

**平均完整任务成功率**

对四项任务最终阶段成功率取平均，用于概括模型端到端完成接触操作的总体能力，而非只完成抓取或接触。 （越高越好，因为只有达到最终阶段才计为完整完成任务。）

</div>
<div class="metric-item" markdown="1">

**零样本泛化成功率**

在训练时未见的新物体或新干扰场景上统计完整任务成功率，并与分布内设置比较；分别测试物体级迁移和场景级抗视觉杂乱能力。 （越高越好；相对分布内结果的下降越小，表示迁移和鲁棒性越强。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四项TacAura任务上的总体比较

<div class="result-value" markdown="1">

最强基线T-Rex的平均完整任务成功率为31.25%；三个$\tau$变体均更高，其中$\tau\text{-Wrist}^{Sup.}$达到71.25%，比最强基线高40个百分点；$\tau\text{-Front}^{Sup.}$和$\tau\text{-DualView}^{Sup.}$分别达到68.75%和57.50%。

</div>

结果表明，在相同的小规模任务示范条件下，把触觉表示适配到VLA并用未来视觉潜表示进行训练，与所选开源基线相比能显著提高完整任务完成率。由于节选未报告多随机种子方差、置信区间或显著性检验，这一结果支持的是当前设备、任务与评测协议下的性能优势，不能单独证明对任意机器人、触觉传感器或任务都具有同等提升。

<div class="result-source" markdown="1">

来源：Main Results，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Specifically, τ-Wrist^{Sup.} obtains the best overall performance with an average success rate of 71.25%, outperforming the strongest baseline by 40 percentage points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 四项任务的最终阶段保持能力

<div class="result-value" markdown="1">

最佳$\tau$变体在插头插入、USB插入、印章按压和白板擦除上的完整任务成功率分别为65%、50%、90%和95%，相对各任务最强基线分别提高35、20、20和45个百分点。基线往往能够抓取、对准或建立接触，却在最终插入、按压或擦除阶段明显退化。

</div>

分阶段结果把收益定位到精细接触后的持续执行，而不是简单的物体获取。例如，ForceVLA在插头任务中可达到85%的对准成功率，却没有完成任何一次最终插入；ForceFlow在白板任务中有95%的接触成功率，但最终擦除仅为50%。这支持作者关于$\tau$改善接触推理和执行的主张，但阶段成功率仍是任务结果指标，不能直接揭示模型内部是否学到了可解释的力学规律。

<div class="result-source" markdown="1">

来源：Main Results，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The best τ variant achieves full-task success rates of 65%, 50%, 90%, and 95% on plug insertion, USB insertion, stamp press, and whiteboard erasing, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 未见物体与未见干扰场景上的零样本泛化

<div class="result-value" markdown="1">

USB插入从已见物体的40%降至两个未见USB上的25%和35%，未见物体平均为30%；在两个未见干扰集合中进一步降至20%和25%，平均22.5%。白板擦除从已见橡皮的95%仅降至两个未见橡皮上的90%，且在两个干扰场景中均保持95%。

</div>

泛化具有明显任务依赖性：白板擦除对物体外观、纹理变化和视觉杂乱较稳健，而USB插入对几何差异、接触配置及目标定位更敏感，尤其容易受场景杂乱影响。因此，实验不能支持“统一强泛化”的结论；更准确的解释是，$\tau$在未见条件下保留了非零能力，但高精度插入仍存在较大分布偏移损失。

<div class="result-source" markdown="1">

来源：Generalization Analysis，Scene Generalization，Figure 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For USB Insertion, the success rate decreases from 40% in the in-distribution setting to 20% and 25% under the two unseen distractor sets, respectively.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 统计可靠性报告不足：每个设置只有20次真实世界试验，所给节选未报告随机种子重复、置信区间或显著性检验；因此5个百分点对应单次试验结果，较小差异需要谨慎解释。
- 覆盖范围有限：训练与主评测仅涉及TacAura的四项任务，泛化分析又只覆盖USB插入和白板擦除；USB在未见干扰场景中的平均成功率降至22.5%，且简单双视图监督弱于最佳单视图，说明精确插入、视觉杂乱和多视角融合仍未解决。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- $\pi_{0.5}$：通用视觉—语言—动作模型，也是移除触觉编码与适配模块后的对应模型；用于判断仅依赖预训练VLA能力时能达到何种水平。
- ForceVLA：针对接触密集型操作设计的力觉感知VLA方法；用于比较高维视觉触觉表示与已有力觉增强方案。
- ForceFlow：面向接触操作的力/力矩时序建模方法；其比较意义在于检验$\tau$的触觉时空表示是否比基于6D力旋量序列的动态建模更有效。
- T-Rex：面向接触密集型操作的代表性开源方法，并在所列基线中取得最高平均完整任务成功率，因此构成最强基线。

**实验想回答的问题**

- 在每项任务仅使用100条专家示范的条件下，引入触觉编码、动作序列条件和未来视觉监督的$\tau$，能否比通用VLA及面向接触操作的基线更可靠地完成插入、按压和擦除等精细接触任务？
- $\tau$的性能提升究竟来自哪些组件，其策略能否零样本迁移到外观或表面纹理不同的新物体，以及包含额外物体和视觉杂乱的新场景？

**实验实现**

所有模型在真实世界中评测。$\tau$对每项任务使用100条专家示范并训练30000步；每个模型在中等随机化条件下进行20次试验。主实验覆盖四项任务并报告三个连续阶段的成功率。消融以表现最佳的$\tau\text{-Wrist}^{Sup.}$为基础，按增量移除协议分别去掉动作序列条件、预测式自监督学习和触觉编码与适配模块。泛化实验只在USB插入与白板擦除上开展，分别测试两个未见物体和两个未见干扰物集合。附录之外的优化器、批大小、随机种子、置信区间及显著性检验信息在所给节选中未明确报告。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除触觉编码与适配模块 | 平均完整任务成功率由71.25%降至28.75%，下降42.50个百分点；四项任务最终成功率分别下降40、20、55和55个百分点。该消融还降低插入任务的对准率和印章任务的接触建立率，而抓取、拾取仍保持100%。 | 这是幅度最大的消融，用于隔离显式触觉输入及其与预训练VLA适配机制的作用。结果说明视觉VLA仍能完成粗粒度取物，但对准、接触建立和最终执行显著依赖触觉模块。不过该设置同时移除了触觉编码和适配，因而无法进一步区分收益究竟来自触觉信号本身、编码器结构，还是适配方式。 | Ablation Study，Impact of Tactile Encoding and Adaptation Module，Table 2<br><span class="experiment-evidence">Removing the tactile encoding and adaptation module leads to the largest performance degradation, reducing the average full-task success rate from 71.25% to 28.75%, a decrease of 42.50 percentage points.</span> |
| 移除预测式自监督学习 | 平均完整任务成功率由71.25%降至51.25%，下降20个百分点；插头插入、USB插入、印章按压和白板擦除分别下降10、15、20和35个百分点，而中间对准与接触成功率保持不变。 | 该消融检验由未来视觉潜表示提供的训练监督是否改善触觉表示。下降集中在最终阶段，且持续接触时间较长的擦除任务降幅最大，符合该目标帮助建模接触随时间演化的解释。它表明未来视觉监督有用，但由于没有与其他自监督目标或等计算量控制组比较，不能证明该监督形式是唯一或最优选择。 | Ablation Study，Impact of Predictive Self-Supervised Learning，Table 2<br><span class="experiment-evidence">Removing predictive self-supervised learning decreases the average full-task success rate from 71.25% to 51.25%, resulting in a 20-point drop.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出融合触觉、视觉和语言表征的VLA模型以提升接触密集型机器人操作。; rule check: matched taxonomy keywords; top rule score=5.0
- 全文指纹：`c0b0b8777433c63e72169461e7cacd6bf8394fe0bda0fbf45f9ed6e275cdddbe`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
