---
title: "[论文解读] Don't Peek at the Answer: Outcome-Masked Group Relative Policy Optimization for Label-Free RLVR"
description: "[arXiv 2608.03119][对齐 / RLHF] 本文提出 OM-GRPO，通过在保留答案层面共识奖励的同时屏蔽答案片段的梯度更新，将无标签强化学习中的优化压力转移到推理轨迹，并利用成对比较增强奖励估计，以缓解投票式训练中的奖励投机与模式坍塌。"
arxiv_id: "2608.03119"
announcement_date: "2026-08-05"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:38:27.148610+00:00"
source_sha256: "eedf33ac936d99de7787fba287b632df13118d4c5be257860c04d29ae15b3144"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "强化学习"
  - "可验证奖励强化学习（RLVR）"
  - "无标签强化学习"
  - "大语言模型推理"
  - "多数投票自奖励"
  - "奖励投机"
  - "模式坍缩"
  - "推理轨迹"
  - "答案跨度梯度屏蔽"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.03119</p>

# Don't Peek at the Answer: Outcome-Masked Group Relative Policy Optimization for Label-Free RLVR

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Yongshi Ye, Liang Zhang, Yidong Chen, Xiaodong Shi, Biao Fu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Xiamen University；Key Laboratory of Digital Protection and Intelligent Processing of Intangible Cultural；Heritage of Fujian and Taiwan (Xiamen University), Ministry of Culture and Tourism</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03119v1) · [PDF 下载](https://arxiv.org/pdf/2608.03119v1) · **关键词** 可验证奖励强化学习（RLVR）, 无标签强化学习, 大语言模型推理, 多数投票自奖励, 奖励投机, 模式坍缩, 推理轨迹, 答案跨度梯度屏蔽<br>


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

本文提出 OM-GRPO，通过在保留答案层面共识奖励的同时屏蔽答案片段的梯度更新，将无标签强化学习中的优化压力转移到推理轨迹，并利用成对比较增强奖励估计，以缓解投票式训练中的奖励投机与模式坍塌。

**不用术语来说**：传统的强化学习推理训练通常需要人工提供正确答案，但这类标注昂贵且难以扩展。无标签方法可以让模型生成多个答案，并把多数答案当作较可信的信号；然而，如果训练同时奖励“答案出现得多”和“生成这些答案的每个词”，模型可能只学会重复常见答案，而没有真正改进解题过程，最终导致训练性能下降和输出趋同。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 OM-GRPO，通过对最终答案片段进行梯度屏蔽，使奖励仍可参考答案共识，但参数更新主要作用于推理轨迹，从而缓解答案词捷径、奖励投机和训练坍塌。
- 提出 Contrast-Augmented Reward，通过对同一问题已有推理轨迹进行低成本成对比较来增强软奖励估计，无需重新采样完整推理过程。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型推理后训练与强化学习的交叉领域，核心对象是“可验证奖励强化学习”（Reinforcement Learning with Verifiable Rewards，RLVR）。RLVR通常让模型针对输入问题生成包含中间推理和最终答案的轨迹，再依据最终答案是否正确给予奖励，并用该奖励更新模型策略；答案正确性通常由人工整理的标准答案或程序验证器判断。本文进一步关注无标签RLVR，即不使用金标准答案，而是利用同一问题下多条模型采样轨迹的答案一致性估计奖励，从而降低监督数据成本。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**可验证奖励强化学习（RLVR）**

模型先生成推理轨迹和最终答案，再根据答案是否满足标准答案或验证规则获得奖励。与只依赖语言流畅度的训练不同，RLVR直接优化可检查的任务结果。

</div>
<div class="concept-item" markdown="1">

**无标签RLVR与多数投票自奖励**

无标签RLVR不依赖人工提供的金标准答案，而从模型自身生成的多个答案中提取训练信号。多数投票方法把同一输入下出现频率较高的答案视为更可信，并提高生成该答案的轨迹的奖励。

</div>
<div class="concept-item" markdown="1">

**推理轨迹与答案跨度**

推理轨迹是模型为得到答案而生成的中间文字序列，答案跨度是其中明确给出最终答案的部分。本文区分二者，是因为直接优化答案跨度可能让模型重复高频答案，而不真正改善推理过程。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一批问题输入，每个问题由当前策略模型采样多条输出轨迹；每条轨迹可抽象为推理部分与最终答案的组合，例如$(y_i,z_i)$，其中$y_i$是第$i$条轨迹的推理，$z_i$是其最终答案。传统有监督RLVR使用金标准答案或验证器判断$z_i$是否正确；本文研究的无标签设定不提供这些金标准信息，而是依据同组轨迹的答案分布构造软奖励。训练目标不是单纯增加某个高频答案的出现概率，而是在保持可利用答案级反馈的同时，把策略更新的主要压力放到推理轨迹$y_i$上，以提升推理质量并避免答案多样性坍缩。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$y_i$**

同一输入下第$i$条采样轨迹的推理部分。

</div>
<div class="notation-item" markdown="1">

**$z_i$**

第$i$条采样轨迹的最终答案或答案跨度。

</div>
<div class="notation-item" markdown="1">

**$(y_i,z_i)$**

一条完整的模型输出轨迹，由推理部分和最终答案组成。

</div>
<div class="notation-item" markdown="1">

**$G$**

同一问题对应的轨迹组；组内答案频率用于估计无标签软奖励。

</div>

</div>

**直接相关的工作**

- **多数投票式自奖励方法（Shafayat et al., 2025；Zhang et al., 2025）**: 这类方法与本文共享无标签RLVR的基本设定：对同一问题采样多条轨迹，并奖励答案与组内共识一致的轨迹。本文指出其关键局限在于同一个答案级信号既用于奖励估计，又用于逐词策略优化，模型可能通过强化答案词而非改进推理来获得更高奖励，进而发生奖励投机和模式坍缩。
- **基于正则化或多视角蒸馏的稳定化方法（Yu et al., 2025b；Zhang et al., 2025）**: 这些工作试图缓解无标签RLVR的训练不稳定性，但根据本文的相关工作讨论，它们没有从根本上消除答案级信号驱动答案词优化的捷径。本文因此将问题定位为奖励估计与策略优化之间的耦合，并通过答案跨度梯度屏蔽进行结构性解耦。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

基于可验证奖励的强化学习能够提升大语言模型的复杂推理能力，但通常依赖人工整理的正确答案来构造奖励，限制了训练数据的规模化获取。无标签强化学习虽然试图从模型自身的多个输出中提取监督信号，却面临训练稳定性和推理质量难以保证的问题，因此需要一种不依赖大规模人工答案、同时又不鼓励模型走答案词捷径的训练机制。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于真实答案的 RLVR**：该类方法对同一问题生成推理结果，并使用人工整理的正确答案判断最终答案是否正确，再将结果转化为奖励来更新模型。它提供了相对明确的结果监督，但奖励构造依赖高质量标注，成本较高。
- **基于多数投票的无标签自奖励**：模型针对同一输入采样多条推理轨迹，提取每条轨迹的最终答案，并依据答案在组内出现的频率或共识程度为轨迹分配奖励。该方法不需要真实答案，但同一个答案层面的信号既用于估计奖励，也直接参与逐词策略优化。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 多数投票方法把答案共识同时当作奖励依据和词级更新信号，模型因此可以直接强化高频答案词，而不必改善产生答案所需的推理过程；论文将其概括为“the model can improve reward by directly sharpening high-frequency answer tokens, without improving the reasoning that leads to them”。其后果是奖励投机，并可能出现模式坍塌。
- 现有投票式训练的性能并不稳定：论文指出这些方法常在训练早期提升、随后急剧退化；同时，最终答案的多样性快速下降，模型可能在整个批次乃至不同批次中收敛到同一个答案。也就是说，答案共识虽然提供了廉价监督，却不能可靠地区分高质量推理与仅仅重复常见答案的行为。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作解决了“没有人工正确答案时如何构造结果奖励”的问题，但尚未充分解决“如何让这一结果奖励改善推理过程，而不是强化答案表面形式”的解耦问题。具体而言，仍缺少一种能够保留答案层面共识信息、又限制答案片段直接主导策略更新，并且能在不重新生成完整推理轨迹的情况下提高奖励辨别力的无标签 RLVR 框架。

</div>
<div markdown="1"><span>核心问题</span>

在不使用人工真实答案的条件下，能否将答案共识用于判断轨迹质量，却阻止答案片段直接获得优化优势，从而稳定地训练出更好的推理轨迹，并进一步通过低成本比较提高奖励估计的可靠性？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把“奖励如何计算”和“哪些词可以通过梯度被直接强化”分开：答案共识仍可作为粗粒度的质量线索，但答案片段的梯度被屏蔽，模型若想提高奖励，就不能仅靠重复高频答案，而必须改善通向答案的推理轨迹。进一步地，对已有轨迹进行成对比较，可以在不重新生成长推理的情况下获得更多相对质量信号，使较好的轨迹更容易获得较高的软奖励。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

OM-GRPO 是一种无需真实答案标签的可验证奖励强化学习方法。对每个问题 $x$，旧策略 $\pi_{\theta_{\mathrm{old}}}$ 生成 $G$ 条轨迹，每条轨迹由推理链 $y_i$ 和可解析的最终答案片段 $z_i$ 组成。方法先依据组内答案频率，或利用轨迹两两比较扩充后的答案池，给原始轨迹计算软共识奖励；随后在 GRPO 的组内标准化优势目标中，仅更新推理链与格式标记对应的 token，屏蔽最终答案片段的梯度，并用 KL 正则限制策略偏离参考模型。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 分组采样并拆分轨迹

从旧策略采样轨迹组 $\{\tau_i\}_{i=1}^{G}$，并把每条轨迹解析为 $\tau_i=(y_i,z_i)$：$y_i$ 是思维链，$z_i$ 是 $\boxed{\cdot}$ 内且不含格式符的答案 token 片段。若输出不存在可提取的合法答案框，则其格式奖励为 $0$。

<div class="method-step__io" markdown="1">

**输入**：训练问题 $x\sim\mathcal{D}$、旧策略 $\pi_{\theta_{\mathrm{old}}}$ 与每题采样数 $G$。<br>
**输出**：包含 $G$ 条原始推理轨迹、对应答案 $\{z_i\}$ 及答案片段位置的轨迹组。

</div>

**直观理解**：模型先对同一道题独立作答多次，再把每次作答分成“解题过程”和“最后答案”。这种拆分使系统可以用答案判断组内共识，却不必直接训练答案文字。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 构造对比增强答案池

CAR 对每个满足 $i\neq j$ 的轨迹对 $(\tau_i,\tau_j)$ 构造对比提示，让模型阅读两条已有推理并只生成一个短答案 $\hat z_{ij}$；再将原始答案与这些比较答案合并为 $\mathcal{Z}_{\mathrm{aug}}=\{z_i\}_{i=1}^{G}\cup\{\hat z_{ij}\}_{i\neq j}$。比较结果仅用于估计奖励，不作为新的策略梯度轨迹。

<div class="method-step__io" markdown="1">

**输入**：同一问题下的原始轨迹组 $\{\tau_i\}_{i=1}^{G}$。<br>
**输出**：规模由 $G$ 扩展到 $O(G^2)$ 的增强答案池 $\mathcal{Z}_{\mathrm{aug}}$。

</div>

**直观理解**：它不是让模型重新完整解题，而是让已有解法“成对辩论”后给出短结论。这样可用较低生成成本反复检验哪些答案能在不同解法比较中保持稳定。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 计算软共识奖励与组内优势

以 $z_i$ 在增强池中的经验概率质量计算软奖励 $r_i^q$，并加上二值格式奖励 $r_i^f$，得到 $r_i=r_i^q+r_i^f$；随后在同题轨迹组内将奖励标准化为优势 $\hat A_i$。若不启用 CAR，则软奖励直接由原始 $G$ 个答案的组内频率估计。

<div class="method-step__io" markdown="1">

**输入**：原始答案 $z_i$、增强答案池 $\mathcal{Z}_{\mathrm{aug}}$ 以及输出格式是否合法的信息。<br>
**输出**：每条原始轨迹的标量奖励 $r_i$ 与组相对优势 $\hat A_i$。

</div>

**直观理解**：多数投票只把答案分成“多数”和“非多数”，而软奖励保留不同答案获得了多少支持的差异。组内标准化则让优化关注同一道题中哪些轨迹相对更好，而非不同题目间不可直接比较的绝对分数。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 屏蔽答案片段并执行 GRPO 更新

在裁剪的重要性采样目标中令答案片段 token 的 $m_{i,t}=0$，其余推理与格式 token 的 $m_{i,t}=1$，从而只让后者产生策略梯度；同时加入系数为 $\beta$ 的 KL 正则约束更新幅度。

<div class="method-step__io" markdown="1">

**输入**：原始轨迹、优势 $\hat A_i$、答案位置掩码 $m_{i,t}$、当前策略 $\pi_\theta$、旧策略 $\pi_{\theta_{\mathrm{old}}}$ 与参考策略 $\pi_{\mathrm{ref}}$。<br>
**输出**：更新后的策略参数 $\theta$；模型仍依据答案层面的奖励学习，但答案 token 本身不接受该奖励的直接梯度。

</div>

**直观理解**：奖励仍由最终答案是否获得支持来决定，但训练时把“直接抄高频答案”这条捷径封住。模型若想提高回报，只能更多地改善通向答案的推理过程和可解析输出结构。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### Outcome-Masked GRPO 优化目标

$$
\mathcal{J}_{\mathrm{OM\text{-}GRPO}}(\theta)=\mathbb{E}_{x\sim\mathcal D,\,\{\tau_i\}_{i=1}^{G}\sim\pi_{\theta_{\mathrm{old}}}(\cdot\mid x)}\!\left[\frac{1}{G}\sum_{i=1}^{G}\sum_{t=1}^{|\tau_i|}m_{i,t}\min\!\left(\rho_{i,t}(\theta)\hat A_i,\,\mathrm{clip}(\rho_{i,t}(\theta),1-\epsilon,1+\epsilon)\hat A_i\right)-\beta\,\mathrm{KL}\!\left(\pi_\theta\|\pi_{\mathrm{ref}}\right)\right],\quad \rho_{i,t}(\theta)=\frac{\pi_\theta(o_{i,t}\mid o_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(o_{i,t}\mid o_{i,<t})},\quad \hat A_i=\frac{r_i-\mathrm{mean}(\mathbf r)}{\mathrm{std}(\mathbf r)+\delta}
$$

**符号说明**

- $\mathcal{J}_{\mathrm{OM\text{-}GRPO}}(\theta)$：待最大化的 OM-GRPO 策略目标。
- $x,\mathcal D$：训练问题以及问题分布或训练数据集。
- $G,\tau_i,o_{i,t}$：每题轨迹数、第 $i$ 条轨迹，以及该轨迹第 $t$ 个输出 token。
- $\pi_\theta,\pi_{\theta_{\mathrm{old}}},\pi_{\mathrm{ref}}$：当前待训练策略、采样轨迹时使用的旧策略，以及用于 KL 约束的参考策略。
- $\rho_{i,t}(\theta)$：当前策略相对旧策略在该 token 上的重要性采样比率。
- $\hat A_i,r_i,\mathbf r$：第 $i$ 条轨迹的组标准化优势、其奖励，以及同一组所有轨迹的奖励向量。
- $m_{i,t}$：结果掩码；答案片段上为 $0$，推理链及其他位置为 $1$。
- $\epsilon,\delta,\beta$：PPO 式比率裁剪宽度、避免标准差分母为零的稳定常数，以及 KL 正则系数。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标先用轨迹级优势 $\hat A_i$ 判断整条回答应被鼓励还是抑制，再把同一个优势作用到允许训练的 token 上。裁剪项限制新旧策略概率比的变化，KL 项防止策略过度偏离参考模型，而 $m_{i,t}$ 是本方法的关键：即使某条轨迹因答案获得高奖励，其答案 token 的目标项也被置零，因此不能通过直接提高该答案字符串的概率来获取捷径收益。<br>
**原文位置**：第 3 节，式 (1)；优势定义紧随式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 对比增强答案池与软奖励

$$
\mathcal Z_{\mathrm{aug}}=\{z_i\}_{i=1}^{G}\cup\{\hat z_{ij}\}_{i\ne j},\qquad r_i^q=\Pr\!\left(z=z_i\mid z\in\mathcal Z_{\mathrm{aug}}\right),\qquad r_i=r_i^q+r_i^f
$$

**符号说明**

- $\mathcal Z_{\mathrm{aug}}$：由原始答案和成对比较生成答案共同组成的增强答案池。
- $z_i$：第 $i$ 条原始轨迹中提取出的最终答案。
- $\hat z_{ij}$：模型比较第 $i$、$j$ 条已有推理轨迹后，为原问题生成的短答案。
- $r_i^q$：答案 $z_i$ 在增强池中的经验概率质量，即软共识奖励。
- $r_i^f$：格式奖励；存在合法可提取答案框时为 $1$，否则为 $0$。
- $r_i$：用于计算组相对优势的最终轨迹奖励。

<div class="equation-explanation" markdown="1">

**直观理解**：增强池把每对已有解法的比较结论当作额外“验证票”，再统计原始答案 $z_i$ 获得的票数比例。它利用的是比较生成的短答案，而不是额外的完整推理 rollout；最终仍只更新最初采样的 $G$ 条轨迹，因此奖励估计规模扩大与策略训练轨迹数相互分离。<br>
**原文位置**：第 3.1 节式 (2) 及最终奖励定义；第 3.3 节式 (3)–(4)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练最大化式 (1) 的组相对策略目标。每个问题内先根据 $r_i=r_i^q+r_i^f$ 对奖励做均值—标准差标准化，得到共享于整条轨迹的 $\hat A_i$；正优势轨迹的非答案 token 概率被提升，负优势轨迹的相应概率被压低。与普通 GRPO 的关键差异是逐 token 目标额外乘以 $m_{i,t}$，使答案片段不产生梯度，但答案层面统计仍决定优势；因此优化对象从“复制高频答案 token”转为“增加产生受支持答案的推理与格式轨迹概率”。CAR 改变的是奖励估计而非策略目标：$\hat z_{ij}$ 只扩充 $\mathcal Z_{\mathrm{aug}}$，不被视作新增训练轨迹。裁剪与 KL 正则分别控制单次更新幅度和相对参考策略的漂移。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 软共识与格式奖励**

软奖励 $r_i^q$ 是轨迹答案 $z_i$ 在候选答案池中的经验概率质量，相比硬多数投票保留答案间的相对支持度；二值格式奖励 $r_i^f$ 检查是否存在合法、可提取的 $\boxed{\cdot}$ 片段，最终使用 $r_i=r_i^q+r_i^f$。

> 直观理解：软共识避免只给“赢家”奖励而使信号过于稀疏，格式项保证答案能被程序可靠抽取。不过共识只是无标签正确性的代理：一个高频答案仍可能是集体错误，因此它不能等同于真实正确性。

**2. Outcome-Masked Update（OMU）**

为每条轨迹定义二值掩码 $\mathbf m_i$，最终答案跨度 $z_i$ 上令 $m_{i,t}=0$，其余位置令 $m_{i,t}=1$；掩码乘在逐 token 的 GRPO 代理目标上，因此答案 token 不反向传播，而推理链和格式 token 仍按整条轨迹的优势 $\hat A_i$ 更新。

> 直观理解：现有无标签方法既用答案频率估计奖励，又直接提升获得高奖励的答案 token 概率，容易把偶然高频答案固化成模式。OMU 将“用答案评分”与“训练答案文字”解耦，使奖励压力转移到推理路径；作者将其解释为抑制答案记忆和模式坍塌的核心设计。

**3. Contrast-Augmented Reward（CAR）**

CAR 枚举组内满足 $i\neq j$ 的轨迹对，通过对比提示生成短答案 $\hat z_{ij}$，把答案池从 $G$ 个原始答案扩展至 $O(G^2)$ 个候选；这些答案只作为验证票参与 $r_i^q$ 的频率估计，不进入策略梯度，也不要求额外生成完整长思维链。

> 直观理解：偶然猜对或依赖脆弱推理的答案，未必能在多次两两比较中被复现，其占比会被稀释；较稳健的推理结论则更可能反复胜出。该模块的目标不是证明答案正确，而是在固定长轨迹预算下获得比简单增加独立采样更有结构的相对质量信号。

**训练与推理**

训练时，对一批问题使用旧策略为每题生成 $G$ 条完整回答，提取 $\boxed{\cdot}$ 内的答案并定位其 token 范围。启用 CAR 时，系统对同题轨迹进行两两比较，只生成短答案来构造 $\mathcal Z_{\mathrm{aug}}$；随后计算软共识与格式奖励、组标准化优势以及答案掩码，并执行带裁剪和 KL 约束的 OM-GRPO 更新。更新后的策略成为后续采样策略，重复这一过程；测试时不需要真实答案，也不需要为普通评测执行 CAR 或策略更新，而是直接由训练后的模型生成推理和最终答案。论文另讨论测试时训练设置：此时可在目标问题上重复同一无标签更新流程，再用适应后的模型作答；该流程仍依赖组内自生成答案作为代理监督，而非访问测试标签。

**复现信息**

正文实现中，每次 GRPO 更新采样 $128$ 个问题，每题生成 $G=8$ 条 rollout；最大提示长度为 $512$，最大响应长度为 $3072$，常规训练运行 $6$ 个 epoch，测试时训练运行 $30$ 个 epoch。优化器为 AdamW，学习率 $3\times10^{-6}$，采用余弦调度与 $0.1$ 的 warmup 比例；KL 系数为 $\beta=0.005$，策略比率裁剪宽度为 $\epsilon=0.2$。训练生成温度为 $1.0$，评测温度为 $0.8$ 且使用 $\mathrm{top}\text{-}p=0.95$；不同方法保持各骨干模型的官方聊天模板一致。所有方法基于 verl 实现，并在 $8$ 张 NVIDIA A100 GPU 上训练。需要注意，附录同时将 AdamW 的数值稳定参数记为 $\epsilon=10^{-8}$，与策略裁剪符号 $\epsilon$ 同名，但两者含义不同。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- AIME系列数学竞赛题，包括主实验中的AIME24/25以及低污染分析中的AIME26。AIME24/25使用每题16次独立采样计算$\mathrm{avg@16}$；AIME26的公开时间晚于Qwen2.5-7B，用于降低预训练数据暴露对结果的干扰。题目规模与具体划分在所给原文中未明确报告。
- HMMT25与HMMT26是较新发布的数学竞赛基准，公开时间晚于Qwen2.5-7B；它们与AIME26共同构成低污染测试，用于检验性能提升能否在较少可能被预训练记忆的题目上保持。题目规模与具体划分原文未明确报告。
- Math5000验证集用于跟踪Qwen3-1.7B-Base强化学习过程中的准确率和训练稳定性，尤其用于比较OM-GRPO与ReasonFlux、PURE等过程奖励模型基线是否在训练早期发生坍塌。该验证集的规模、来源和划分细节在所给原文中未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Avg@$k$准确率**

对每道题独立采样$k$个解答，分别判定正确性后取平均；AIME24/25使用$k=16$，MATH500与GSM8K使用$k=4$，AMC使用$k=8$，LiveCodeBench与CRUX使用$k=5$。它衡量单次随机采样平均得到正确解答的概率。 （越高越好，因为它表示模型随机生成的一般解答更经常正确，而不是只要多次尝试中偶然出现一次正确答案。）

</div>
<div class="metric-item" markdown="1">

**Pass@$k$**

衡量每道题在$k$次采样中至少出现一个正确解答的能力，侧重多次采样覆盖正确推理路径的概率。论文还将其作为解空间覆盖度和推理多样性的间接指标。 （越高越好，因为它表示有限次尝试中找到至少一条正确解法的概率更高；但它不能单独证明每条推理过程都更可靠。）

</div>
<div class="metric-item" markdown="1">

**过程质量评分**

在AIME25上采用类似ReCEval的评价准则，评估器只看到问题与推理轨迹，并从正确性、信息充分性以及推理是否支持最终答案三个方面评分。 （越高越好，因为它更直接反映中间推理是否有效；不过所给原文没有报告具体评分数值，也未说明评估器类型与一致性。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen2.5-7B在AIME26、HMMT25和HMMT26三个低污染数学基准上的无标签评测。

<div class="result-value" markdown="1">

OM-GRPO的三基准平均Avg@16为3.25%，平均Pass@16为18.18%；其中平均Pass@16在所有比较方法中最高，而平均Avg@16仅低于使用人工答案的GT-Reward。分数据集看，其AIME26、HMMT25和HMMT26的Avg@16分别为$4.58\pm1.28$、$0.62\pm0.72$和$4.55\pm0.83$，Pass@16分别为20.00%、13.33%和21.21%。

</div>

作者据此主张，OM-GRPO的优势并不完全依赖模型可能在预训练阶段见过旧基准。尤其是Pass@16领先，说明多次采样时更有机会覆盖正确解法。分析上仍应谨慎：三个数据集的绝对Avg@16均较低，且“发布时间晚于模型”只能降低直接污染风险，不能排除相似题型、非公开数据或训练分布重叠。

<div class="result-source" markdown="1">

来源：Table 6；Appendix E.1 Low-Contamination Benchmark Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

OM-GRPO | 4.58 ± 1.28 | 20.00 | 0.62 ± 0.72 | 13.33 | 4.55 ± 0.83 | 21.21 | 3.25 | 18.18

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3-1.7B-Base训练轨迹上的逐步伪标签偏置分析，对比Majority Voting的训练奖励、真实准确率、最高频答案占比和预测答案1的占比。

<div class="result-value" markdown="1">

Majority Voting在最后50步中，最高频答案占比与预测答案1的占比都接近1.0，尽管真实答案中只有约2.4%为1；与此同时，平均训练奖励从1.354升至1.996，准确率却从44.0%降至2.4%。

</div>

这是奖励投机反馈环的直接证据：训练目标认为策略越来越好，但真实任务表现几乎崩溃。错误不是独立随机噪声，而是策略偶然偏好的答案1先成为多数伪标签，再被奖励继续放大。作者报告OM-GRPO的答案分布和准确率更接近GT-Reward趋势，支持答案跨度梯度掩码能够切断直接强化答案词元的路径；但该分析来自单一骨干模型，不能单独证明所有模型都会以答案1的形式坍塌。

<div class="result-source" markdown="1">

来源：Figure 10；Appendix E.4 Rollout-Level Pseudo-Label Bias Analysis

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At the same time, its training reward increases from 1.354 to 1.996, but its accuracy drops from 44.0% to 2.4%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen3-1.7B-Base的Math5000验证集训练曲线，对比OM-GRPO与三个需要额外奖励模型的PRM过程奖励基线。

<div class="result-value" markdown="1">

ReasonFlux-PRM-1.5B和ReasonFlux-PRM-7B均从约52.8%开始，随后分别降至2.2%和0.0%；PURE-PRM-7B从53.1%短暂升至第20步的55.2%，但约第40步也降至0.0%。OM-GRPO则从53.0%升至64.4%，最终检查点仍保持63.7%。

</div>

该比较表明，为推理过程引入一个独立PRM并不自动消除无标签强化学习的坍塌路径；相比之下，OM-GRPO在不加载额外奖励模型时保持稳定。它支持“优化结构中的结果掩码比单纯更换奖励来源更关键”的解释，但不能证明所有PRM设计必然失败，因为这里只测试了三个具体奖励模型及一个骨干模型。

<div class="result-source" markdown="1">

来源：Figure 11；Appendix E.5 PRM-based Process Reward Baselines

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ReasonFlux-PRM-1.5B and ReasonFlux-PRM-7B both start around 52.8%, then fall to 2.2% and 0.0%, respectively; PURE-PRM-7B briefly rises from 53.1% to 55.2% at step 20 but also reaches 0.0% around step 40.

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

- GT-Reward是有监督的理想上界：抽取轨迹$y_i$的最终答案$\mathrm{ans}(y_i)$，与人工标注答案完全一致时奖励为1，否则为0。它用于判断无标签方法与可靠真实奖励训练之间还存在多大差距，但并非同等监督条件下的竞争方法。
- Majority Voting（MV）从同一问题的$G$条采样轨迹中选择最高频答案$z_{\mathrm{maj}}$作为伪标签，并奖励所有满足$\mathrm{ans}(y_i)=z_{\mathrm{maj}}$的轨迹。它是最直接的无标签自一致性基线，也最能检验OM-GRPO是否解决了“当前策略产生偏置共识、偏置共识又反向强化策略”的反馈环。
- Self-Certainty与Entropy Minimization代表不依赖真实标签的模型内部置信度奖励：前者偏好策略赋予更高整段序列似然的轨迹，后者偏好最终答案跨度上熵更低、分布更确定的轨迹。它们用于检验单纯提高模型自信或确定性是否足以改善推理。
- PRM过程奖励基线包括ReasonFlux-PRM-1.5B、ReasonFlux-PRM-7B和PURE-PRM-7B，利用额外奖励模型评价推理过程，但仍不使用最终答案标签。该比较用于判断把奖励从答案层面改为过程层面，是否已经足以避免无标签强化学习坍塌。

**实验想回答的问题**

- 在不使用真实答案标签的条件下，OM-GRPO能否在不同推理任务和较低预训练污染风险的基准上，取得优于现有无标签奖励方法且接近监督式GT-Reward的表现？
- 结果掩码是否确实缓解由自生成伪标签引起的奖励投机和答案模式坍塌，并将优化压力转向推理过程，而非仅强化高频答案词元？

**实验实现**

评测按任务采用多次独立采样：AIME24/25报告$\mathrm{avg@16}$，MATH500和GSM8K报告$\mathrm{avg@4}$，AMC报告$\mathrm{avg@8}$，LiveCodeBench和CRUX报告$\mathrm{avg@5}$，IFEval与MMLU-Pro报告$\mathrm{pass@1}$。相应工具分别包括lighteval、ttrl评测实现、LiveCodeBench官方评测库、ZeroEval和lm-evaluation-harness。低污染实验固定使用Qwen2.5-7B，并在AIME26、HMMT25和HMMT26上同时报告Avg@16与Pass@16；训练稳定性和伪标签偏置分析使用Qwen3-1.7B-Base。所给章节未完整提供训练步数、随机种子、超参数及显著性检验方案，因此表中的均值与误差项不能被进一步解释为哪一种统计区间。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 答案多样性曲线提供了一个定性案例：Majority Voting训练时每个样本的平均唯一答案数持续下降并最终接近1，而OM-GRPO无论是否加入CAR，都维持更高且更稳定的答案多样性，并接近GT-Reward。其直观含义是MV逐渐学会跨输入重复同一答案模式，OM-GRPO则较少依赖这种捷径；不过答案更多样并不等同于答案更正确，必须结合准确率和Pass@$k$理解。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces a label-free RLVR post-training method for improving LLM reasoning while addressing reward estimation and policy-optimization stability.; rule check: matched taxonomy keywords; top rule score=6.0
- 全文指纹：`eedf33ac936d99de7787fba287b632df13118d4c5be257860c04d29ae15b3144`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
