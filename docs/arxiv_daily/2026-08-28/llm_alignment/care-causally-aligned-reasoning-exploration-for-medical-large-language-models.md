---
title: "[论文解读] CARE: Causally-Aligned Reasoning Exploration for Medical Large Language Models"
description: "[arXiv 2608.26147][对齐 / RLHF] CARE将医疗大模型的强化学习从“只看答案是否正确”改为“筛选因果上可信且当前可学的推理轨迹”，以同时减少捷径学习和训练不稳定。"
arxiv_id: "2608.26147"
announcement_date: "2026-08-28"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:42:47.153179+00:00"
source_sha256: "d32cfd292bc80529c3188d8e322f4a81e99a52489093170948a794ad099bef05"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "强化学习"
  - "医疗大语言模型"
  - "结果监督"
  - "自回归信用分配"
  - "因果充分性"
  - "近端可学习性"
  - "推理轨迹筛选"
  - "正确答案错误理由"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.26147</p>

# CARE: Causally-Aligned Reasoning Exploration for Medical Large Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Yucheng Zhou, Peng Luo, Qianning Wang, Chengzhong Xu, Jianbing Shen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> SKL-IOTSC, CIS, University of Macau；Auckland University of Technology</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26147v1) · [PDF 下载](https://arxiv.org/pdf/2608.26147v1) · **关键词** 医疗大语言模型, 强化学习, 结果监督, 自回归信用分配, 因果充分性, 近端可学习性, 推理轨迹筛选, 正确答案错误理由<br>


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

CARE将医疗大模型的强化学习从“只看答案是否正确”改为“筛选因果上可信且当前可学的推理轨迹”，以同时减少捷径学习和训练不稳定。

**不用术语来说**：医疗模型即使答对，也可能只是利用数据中的表面规律猜中，而没有依据症状、影像或检查结果完成可靠推断；如果训练时把这类“碰巧答对”的过程也当作正例，模型会进一步强化错误习惯。与此同时，过于简单的样本几乎提供不了新知识，过难或充满幻觉的样本又会让训练信号剧烈波动，因此不能把所有答对的生成结果一视同仁。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将结果奖励下的医疗推理失败归纳为两个相互独立的问题：自回归信用分配会把最终正确奖励错误地分摊给无效推理步骤，而无约束的序列似然会造成梯度方差过大；据此提出“因果充分性”和“近端可学习性”两项轨迹准入条件。
- 作者提出CARE框架：用基于一致性的自验证检查仅凭生成理由能否恢复最终答案，以过滤因果不一致轨迹；再用动态熵界选择处于模型当前能力附近的经验，并结合在线组相对探索与按难度加权的经验回放进行优化。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于医疗大语言模型的自改进推理领域。医疗模型需要根据文本或医学影像等临床信息生成诊断答案及其推理过程；主流的监督微调依赖昂贵、难扩展的专家标注，因此研究者转向强化学习，让模型利用自身生成的推理轨迹继续训练。与答案可被程序严格验证的数学或编程任务不同，医疗推理通常缺少廉价可靠的自动验证器：只按最终诊断是否正确给予奖励，无法保证中间推理在临床上成立。此外，医疗样本的信息量和难度差异很大，从简单识别到信息不足的模糊问题均有涉及，因而不加筛选地强化所有答对轨迹，既可能学习数据捷径，也可能造成不稳定的策略梯度。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**结果式强化学习**

模型生成完整答案后，根据最终结果是否正确获得奖励，并据此提高高奖励输出的概率。它的局限是奖励只评价终点，难以判断推理链中哪些步骤真正促成了正确答案。

</div>
<div class="concept-item" markdown="1">

**自回归信用分配**

大语言模型逐词生成推理，但序列末端的整体奖励需要被分配给前面所有生成决策。如果只有最终答案奖励，碰巧伴随正确答案出现的错误推断、伪相关线索或数据集捷径也可能被一并强化。

</div>
<div class="concept-item" markdown="1">

**策略梯度方差**

强化学习通过采样输出估计参数更新方向，不同轨迹产生的更新差异越大，估计方差就越高。过易样本可能几乎不提供梯度，过难、极不确定或含幻觉的推理则可能带来剧烈波动，使训练不稳定。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究设置是医疗文本或多模态推理中的模型自改进：模型接收临床问题以及可能存在的医学图像等输入，自回归地产生解释性推理轨迹和最终答案，并利用可获得的答案级监督进行强化学习。核心问题不是单纯筛选“答对”的输出，而是从模型自身采样的轨迹中识别同时适合训练的经验：其一，推理内容应足以独立恢复最终决策，避免“答案正确但理由错误”；其二，轨迹难度应处于模型当前能够有效学习的范围，避免过易经验没有信息增益、过难经验放大优化方差。本文默认医疗任务缺少低成本、可确定验证每个中间推理步骤的外部工具，因此需要依靠模型内部的一致性检验和基于序列不确定性的动态筛选。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Supervised Fine-Tuning（SFT）**: 这是医疗大模型的主流训练范式，通过专家整理的医疗样本直接学习输入到目标答案或推理过程的映射。它能够有效注入医学知识，但高度依赖成本高、耗时长且难以规模化的专家标注，构成本文转向自生成经验和强化学习的现实背景。
- **Group Relative Policy Optimization（GRPO）**: GRPO是不依赖独立价值模型、利用同组候选输出的相对奖励更新策略的强化学习方法，已用于医疗多模态模型和推理训练。本文将其视为典型的结果式强化学习基础：若只依据最终答案强化轨迹，仍无法排除伪相关推理，也没有针对医疗样本异质性控制学习信号的方差。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

医疗大模型需要大量高质量临床标注才能通过监督微调获得可靠推理能力，但专家标注昂贵、耗时且难以规模化。利用模型自身生成轨迹进行强化学习虽可降低数据依赖，却必须保证模型学到的是可迁移的临床推断，而不是只在基准数据上有效的偶然相关性；否则表面准确率的提升可能掩盖真实临床可靠性和可解释性的下降。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **专家数据监督微调（SFT）**：使用人工整理并标注的医疗问答、诊断或多模态样本，直接最大化模型生成参考答案或参考推理过程的概率。其优势是监督信号明确，但扩展能力受专家数据数量与成本约束。
- **基于结果奖励的强化学习（如GRPO）**：模型针对同一医疗问题生成多条推理轨迹，根据最终诊断或答案是否正确给予奖励，再提高高奖励轨迹的生成概率。该范式通常只验证输出结果，而不直接判断中间临床推理是否有效。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 仅依赖最终答案奖励会产生自回归信用分配失败：一条轨迹只要最终答对，其中由伪相关、数据集捷径或无效步骤形成的内容也可能整体得到强化，从而形成“Right Answer, Wrong Reason”陷阱。其后果是基准准确率可能上升，但推理一致性、可解释性和真实临床场景中的可靠性并未同步提高。
- 标准探索往往不区分样本的学习价值， indiscriminately 强化所有正确轨迹。医疗任务的信息密度差异很大：过于简单的轨迹产生接近消失的梯度，过难、含糊或幻觉较多的轨迹则带来高方差更新；无界的序列似然因此可能导致优化震荡甚至不稳定。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种可在没有廉价、可靠过程验证器的条件下实施的轨迹准入机制：它既要判断生成理由是否足以支持最终决策，从训练信号中排除“答案正确但理由不成立”的经验，又要根据模型当前能力动态排除信息量过低或不确定性过高的经验。换言之，尚缺少同时处理因果对齐与梯度方差控制的医疗自改进框架。

</div>
<div markdown="1"><span>核心问题</span>

能否仅利用模型自身生成和复核的经验，构造一套具有理论依据的医疗强化学习机制，使被用于更新的轨迹同时满足“理由能够支持答案”的因果充分性与“难度处于稳定可学习区间”的近端可学习性，从而在减少捷径学习的同时保持有效、低方差的优化？

</div>
<div markdown="1"><span>作者直觉</span>

如果遮去原始问题信息，让模型只依据自己写出的理由仍能复现同一最终决策，那么该理由至少比“答对但与结论无关”的文本更可能真正承载决策依据，这可作为缺少外部过程验证器时的内部一致性检查。随后再按归一化序列似然或熵筛选难度适中的轨迹，就像教学中既不反复练习已经完全掌握的题，也不直接训练远超当前能力的题：前一步改善经验的可信度，后一步改善经验的可学性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CARE 是一个面向医疗大语言模型的自改进训练框架，输入为仅含临床问题与标准答案的训练对 $(x,a^*)$，不要求专家标注推理过程。模型先针对每个问题生成 $N$ 条结构化轨迹 $y=(r,a)$，其中 $r$ 是诊断推理，$a$ 是最终答案；随后依次检查答案正确性、轨迹是否处于当前模型可有效学习的难度区间，以及仅凭推理 $r$ 能否重新得到答案 $a$。只有同时通过三项检查的轨迹才获得正向准入信号，并进入高质量经验回放池 $\mathcal{B}$。

优化阶段包含两条并行数据流：在线流将同一问题下各轨迹的准入结果组内标准化，用 GRPO 式相对优势推动模型增加优质轨迹概率，并用 KL 正则限制策略偏移；回放流则重新学习已通过筛选的历史轨迹，并按当前序列负对数似然给予较难但仍可学习的经验更高权重。直观地说，CARE 不再因为“答案碰巧正确”就奖励整段生成，而是先确认这段推理确实支持答案、难度适中，再把它用于探索与复习。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分组生成结构化医疗推理轨迹

对每个问题 $x$ 从当前策略采样 $N$ 条候选轨迹 $\mathcal{Y}_x=\{y^{(i)}\}_{i=1}^{N}$，并要求每条输出采用 $y^{(i)}=(r^{(i)},a^{(i)})$ 的推理—答案结构。该过程保留同一问题下的多种探索路径，以便后续计算组内相对优势。

<div class="method-step__io" markdown="1">

**输入**：训练集 $\mathcal{D}$ 中的临床问题与标准答案 $(x,a^*)$；多模态情况下 $x=(x_{\mathrm{img}},x_{\mathrm{txt}})$；当前策略 $\pi_\theta$。<br>
**输出**：每个问题对应的一组候选推理与诊断答案，以及生成各词元所需的策略概率。

</div>

**直观理解**：模型不是只作答一次，而是为同一道题尝试多条诊断路线。这样可以在同组候选中识别哪些路线更值得强化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 结果有效性与近端可学习性筛选

先用规则抽取函数 $\mathcal{M}(y)$ 判断最终答案是否等于 $a^*$；再计算长度归一化序列 NLL，并依据 $\mathcal{H}$ 的分位数形成动态窗口 $[\tau_{\mathrm{low}},\tau_{\mathrm{high}}]$，仅保留 NLL 落入窗口的轨迹。过低 NLL 的简单轨迹被视为学习信号弱，过高 NLL 的轨迹则被视为可能产生高方差或幻觉。

<div class="method-step__io" markdown="1">

**输入**：候选轨迹 $y=(r,a)$、标准答案 $a^*$、当前策略概率，以及近期 NLL 历史缓冲区 $\mathcal{H}$。<br>
**输出**：答案正确且处于当前模型近端发展区间的候选轨迹，以及更新后的 NLL 历史。

</div>

**直观理解**：这一步既排除答错的样本，也不让模型反复练习“已经会的题”或强行模仿“完全不会的题”。筛选边界随模型近期能力变化，而不是固定难度阈值。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于一致性自验证的因果充分性检查

将推理 $r$ 单独放入验证提示，用推理模式下的模型 $\pi_{\bar{\theta}}$ 重新预测 $\hat a$；只有 $\hat a=a$ 时，因果充分性指示量 $\phi_{\mathrm{causal}}(r,a)$ 才为 $1$。这在操作上近似 $do(R=r)$：遮蔽原问题，检查答案能否由推理本身恢复。

<div class="method-step__io" markdown="1">

**输入**：通过前两项筛选的推理—答案对 $(r,a)$，以及不再提供原始问题 $x$ 的验证提示 $\mathcal{T}(r)$。<br>
**输出**：统一二元准入信号 $\Phi(x,y)$；准入轨迹同时写入经验回放池 $\mathcal{B}$。

</div>

**直观理解**：可以把它理解为“把题干拿走，只把解题过程交给另一轮模型，看它能否推出同一答案”。若不能，原答案可能来自题干关键词、先验记忆或数据捷径，而不是所写推理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 双流策略优化与循环更新

在线流将二元准入分数在每个候选组内标准化为优势 $A^{(i)}$，优化带 KL 约束的组相对策略损失；回放流按当前 NLL 构造批内归一化权重 $w(y)$，对较难的合格历史轨迹执行加权最大似然学习。两项损失以系数 $\lambda$ 合并更新 $\theta$，之后重新生成、筛选并训练，直至收敛。

<div class="method-step__io" markdown="1">

**输入**：当前批次各轨迹的准入分数、同问题候选组、参考策略 $\pi_{\mathrm{ref}}$，以及从 $\mathcal{B}$ 抽取的历史优质轨迹。<br>
**输出**：更新后的医疗策略 $\pi_\theta$、持续扩充的经验池 $\mathcal{B}$ 与动态历史 $\mathcal{H}$。

</div>

**直观理解**：在线流负责发现当前更好的新推理，回放流负责复习过去验证过的可靠推理。二者结合可避免只追逐新样本造成遗忘，也避免只模仿旧经验而停止探索。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 统一轨迹准入函数

$$
\Phi(x,y)=\phi_{\mathrm{valid}}(x,y)\cdot\phi_{\mathrm{learn}}(y)\cdot\phi_{\mathrm{causal}}(r,a)
$$

**符号说明**

- $\Phi(x,y)$：轨迹的统一二元准入信号，同时作为在线强化学习的奖励基础和经验回放池的写入门控。
- $x$：临床查询；多模态设置中由医学图像与文本问题共同组成。
- $y=(r,a)$：模型生成的完整轨迹，其中 r 为推理过程，a 为最终诊断答案。
- $\phi_{\mathrm{valid}}(x,y)$：结果有效性指示量；规则抽取出的答案与标准答案一致时为 1。
- $\phi_{\mathrm{learn}}(y)$：近端可学习性指示量；轨迹的长度归一化 NLL 位于动态上下界之间时为 1。
- $\phi_{\mathrm{causal}}(r,a)$：因果充分性指示量；仅凭推理重新预测的答案与原答案一致时为 1。

<div class="equation-explanation" markdown="1">

**直观理解**：三项条件采用乘积，即任何一项失败，轨迹都不会获得正向准入。该设计把“答对”“当前学得动”和“推理确实支持答案”明确区分，避免仅凭最终答案给整条自回归序列广播奖励。<br>
**原文位置**：式 (12)，第 4.2 节 Unified Admission

</div>

</div>

<div class="equation-block" markdown="1">

#### CARE 双流总训练目标

$$
\mathcal{L}_{\mathrm{CARE}}(\theta)=\mathcal{L}_{\mathrm{on}}(\theta)+\lambda\mathcal{L}_{\mathrm{rep}}(\theta)
$$

**符号说明**

- $\mathcal{L}_{\mathrm{CARE}}(\theta)$：用于更新参数 θ 的 CARE 总损失。
- $\theta$：当前医疗语言模型策略的可训练参数。
- $\mathcal{L}_{\mathrm{on}}(\theta)$：在线组相对策略损失；利用准入分数形成的相对优势增加优质轨迹概率，并包含相对参考策略的 KL 约束。
- $\mathcal{L}_{\mathrm{rep}}(\theta)$：难度加权经验回放损失；对经验池中的合格轨迹执行加权负对数似然训练。
- $\lambda$：控制经验回放损失相对于在线探索损失贡献的混合系数。

<div class="equation-explanation" markdown="1">

**直观理解**：总目标同时承担探索和巩固：在线项让模型从当前采样结果中发现更可靠的推理，回放项让已经验证的推理稳定沉淀到模型参数中。$\lambda$ 决定训练更偏向即时探索还是历史经验复用。<br>
**原文位置**：式 (16)，第 4.3 节 Total Objective

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：在线优化首先对同一问题的准入值 $\Phi^{(i)}$ 做组内标准化，得到 $A^{(i)}=(\Phi^{(i)}-\mu(\Phi))/(\sigma(\Phi)+\epsilon)$。当一条轨迹相对同组候选更可靠时，其对数概率受到正向推动；KL 惩罚系数 $\beta$ 则约束 $\pi_\theta$ 不要过快偏离参考策略 $\pi_{\mathrm{ref}}$。由于准入值已经联合编码正确性、可学习性与推理—答案一致性，在线更新不再把所有“碰巧答对”的轨迹等同处理。

回放优化从 $\mathcal{B}$ 中采样已通过三重筛选的 $(x,y)$，最小化 $-w(y)\log\pi_\theta(y\mid x)$，其中 $w(y)$ 与当前序列 NLL 成正比并在批内归一化。它会优先巩固尚未被模型完全掌握、但已确认可靠的轨迹；最终通过最小化 $\mathcal{L}_{\mathrm{on}}+\lambda\mathcal{L}_{\mathrm{rep}}$ 联合更新参数。需要注意，论文的“因果”保证依赖其自验证近似与理论假设：实际算法检验的是遮蔽题干后的答案一致性，而不是直接观察真实临床因果机制。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 近端可学习性过滤器**

对轨迹计算 $\mathcal{L}_{\mathrm{seq}}(y\mid x;\theta)=-|y|^{-1}\sum_t\log\pi_\theta(y_t\mid x,y_{<t})$，并用近期 NLL 历史 $\mathcal{H}$ 的分位数动态确定上下界。根据论文的方差分析，限制 NLL 上界可控制策略梯度二阶矩，而设置下界可减少几乎没有梯度与信息增益的简单样本。

> 直观理解：NLL 可近似理解为模型对整段输出的“不熟悉程度”。CARE 只选择不太简单也不至于混乱的轨迹，使训练集中在当前能力边界附近。

**2. 因果充分性与一致性自验证**

模块构造只包含推理 $r$、不包含原始问题 $x$ 的提示 $\mathcal{T}(r)$，由冻结于推理调用状态的 $\pi_{\bar{\theta}}$ 输出 $\hat a$，并以 $\mathbb{I}[\hat a=a]$ 判定推理能否独立支持答案。作者将这种遮蔽原输入的操作解释为对 $do(R=r)$ 的经验近似，用于阻断题干残余相关性对答案预测的贡献。

> 直观理解：答案正确并不证明解题过程正确；模型可能先凭关键词猜中答案，再生成一段看似合理的话。自验证要求“过程单独拿出来仍能导出结论”，从而减少正确答案对错误推理的误奖励。

**3. 组相对探索与难度加权回放**

在线部分以同一问题下 $N$ 条轨迹的准入分数均值和标准差构造 $A^{(i)}$，无需单独训练价值网络，并通过相对优势与 KL 项更新策略。离线回放部分只使用进入 $\mathcal{B}$ 的轨迹，以 $w(y)\propto\mathcal{L}_{\mathrm{seq}}(y\mid x;\theta)$ 提高能力边界附近合格经验的训练权重。

> 直观理解：前者回答“这次尝试中哪条路线更好”，后者回答“过去可靠经验中哪条最值得继续练”。回放权重偏向仍有学习空间的样本，而不是平均重复所有已验证轨迹。

**训练与推理**

训练初始化时给定数据集 $\mathcal{D}$、当前策略 $\pi_\theta$ 和参考策略 $\pi_{\mathrm{ref}}$，并令经验池 $\mathcal{B}$ 与 NLL 历史 $\mathcal{H}$ 为空。每轮从 $\mathcal{D}$ 抽取问题批次，依据 $\mathcal{H}$ 的近期分位数更新 $[\tau_{\mathrm{low}},\tau_{\mathrm{high}}]$；随后对每个问题生成 $N$ 条轨迹，计算 NLL 并写入历史。算法先检查答案有效性和近端可学习性，仅对通过者执行一次遮蔽原问题的自验证；三项条件均成立时置 $\Phi=1$ 并将轨迹加入 $\mathcal{B}$，否则置 $\Phi=0$。完成组内优势计算后，再从 $\mathcal{B}$ 抽取回放批次，联合最小化在线损失与回放损失，循环至收敛。

常规任务推理时，训练后的 $\pi_\theta$ 接收临床输入 $x$ 并生成结构化响应 $y=(r,a)$；原文所给算法没有说明部署时必须继续运行三重筛选或生成 $N$ 条候选，因此不应把训练期自验证默认视为推理期必需步骤。验证阶段的 $\pi_{\bar{\theta}}$ 表示模型在推理模式下仅接收 $\mathcal{T}(r)$，其作用是给训练轨迹打准入标签，而非独立的专家模型。

**复现信息**

公平复现至少需要保持以下设计：输出必须能可靠分离为推理 $r$ 和答案 $a$；规则函数 $\mathcal{M}$ 应按任务格式抽取答案；每个问题须生成分组轨迹以计算组内优势；NLL 必须按序列长度归一化；动态窗口由近期历史 $\mathcal{H}$ 的分位数更新；自验证提示只提供 $r$，不能泄露原始问题 $x$；经验池只接收 $\Phi=1$ 的轨迹；回放权重按当前 NLL 构造并在批内归一化；在线目标保留对 $\pi_{\mathrm{ref}}$ 的 KL 约束。

所给章节未明确报告 rollout 数 $N$、NLL 分位数及历史窗口容量、$\beta$、$\lambda$、优化器、学习率、批大小、采样温度、经验池容量或验证解码细节，因此这些数值不能从当前材料中补造。复现或比较时还应固定自验证提示模板与答案规范化规则，因为它们会直接影响 $\hat a=a$ 的一致性判定和最终准入率。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- PMC-VQA：医学图像视觉问答数据集，同时用于训练混合数据和多模态评测；作者声明训练样本与各评测测试集不存在重叠，但原文节选未报告样本规模、具体划分及去重流程。
- MedMCQA：面向专业医学知识的文本选择题数据集，同时用于训练混合数据和文本评测，用来检验模型对医学知识及问题推理的掌握；原文节选未报告训练或测试规模。
- MedQA：纯文本医学问答评测集，不在文中列出的训练混合数据之内，因而主要用于测试方法对医学考试式推理的泛化；原文节选未报告版本、规模和具体划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**各基准官方评测分数**

衡量模型在对应医学视觉问答或文本问答测试集上的任务表现。论文称评分脚本与指标遵循 Hulu-Med 官方仓库，但节选没有逐项说明这些数值是否全部为准确率，因此不应擅自将所有列统一解释为 Accuracy。 （越高越好，因为更高分表示按照相应基准官方协议得到更多正确或更符合标准的回答。）

</div>
<div class="metric-item" markdown="1">

**跨任务一致提升**

比较 CARE 与其直接骨干在多个测试集上的分数方向，考察收益是否仅发生在单一数据集，还是覆盖多模态与纯文本任务；这是综合分析方式，而非论文另行定义的正式指标。 （在更多任务上保持正向差值更好，因为这降低了结论由单个数据集偶然性驱动的可能，但不能替代显著性检验。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 以 Hulu-Med-7B 为直接骨干的多模态医疗评测

<div class="result-value" markdown="1">

CARE-7B 在表 1 的七个多模态基准上均超过 Hulu-Med-7B：OmniVQA、PMC-VQA、VQA-RAD、SLAKE、PathVQA、MedXQA 和 MMMU-Med 分别由 $84.2/66.8/78.0/86.8/65.6/29.0/51.4$ 提升至 $85.6/68.2/79.3/88.1/67.1/31.2/53.0$，对应绝对增益为 $1.4/1.4/1.3/1.3/1.5/2.2/1.6$ 个分数点。

</div>

这是最直接的受控证据：骨干不变而训练框架改变后，所有多模态任务都出现正向变化，说明 CARE 的收益并非由某一个测试集单独驱动，其中 MedXQA 的增幅最大。该结果支持 CARE 改善医疗视觉问答表现，但没有单独证明提升必然来自“因果对齐”；还需要完整消融排除筛选、回放或一般强化学习训练所产生的替代解释。

<div class="result-source" markdown="1">

来源：表 1，Medical Multimodal Benchmarks

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Hulu-Med-7B (Jiang et al., 2025b) 84.2 66.8 78.0 86.8 65.6 29.0 51.4
CARE-7B 85.6 68.2 79.3 88.1 67.1 31.2 53.0

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 以 Hulu-Med-7B 为直接骨干的纯文本医学评测

<div class="result-value" markdown="1">

CARE-7B 在表 2 的六个文本任务上也全部超过 Hulu-Med-7B：MMLU-Pro-Med、MedXQA、PubMedQA、MedMCQA、MedQA 和 MMLU-Med 分别从 $60.6/19.6/77.4/67.6/73.5/79.5$ 提升到 $62.4/22.1/78.6/69.1/75.0/81.1$，绝对增益为 $1.8/2.5/1.2/1.5/1.5/1.6$ 个分数点。

</div>

CARE 虽以医疗视觉语言模型为基础，但增益不局限于图像理解：纯文本任务也一致改善，尤其表中的文本 MedXQA 提升 $2.5$ 个分数点。这支持方法增强医学知识问答与推理的跨模态适用性。不过，基准最终分数只能说明答案层面的效果；仅凭这些分数无法直接验证推理链更具因果性、长程推理确实改善，或“正确答案、错误理由”已经减少。

<div class="result-source" markdown="1">

来源：表 2，Medical Text Benchmarks

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Hulu-Med-7B (Jiang et al., 2025b) 60.6 19.6 77.4 67.6 73.5 79.5
CARE-7B 62.4 22.1 78.6 69.1 75.0 81.1

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 将 CARE 迁移到 HuatuoGPT-V 7B 的跨骨干验证

<div class="result-value" markdown="1">

在 HuatuoGPT-V 上应用 CARE 后，表 1 七个多模态任务由 $74.3/53.1/67.6/68.1/44.8/23.2/49.8$ 提升至 $75.8/54.6/69.0/69.8/46.3/25.4/51.2$；表 2 六个文本任务则由 $44.6/10.1/72.8/51.2/52.9/69.3$ 提升至 $46.3/12.2/73.9/53.0/54.6/71.0$。两类评测的所有列均为正向变化。

</div>

第二骨干上的一致提升削弱了“CARE 只适配 Hulu-Med”的解释，是方法具有一定骨干无关性的关键证据。通俗地说，同一套训练思路换到另一个医疗模型上仍然有效。但实验只覆盖两个 $7$B 医疗视觉语言骨干，尚不足以证明它适用于任意规模、任意架构或纯文本基础模型。

<div class="result-source" markdown="1">

来源：表 1 与表 2，HuatuoGPT-V 7B 和 CARE-7B（HuatuoGPT-V）行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

HuatuoGPT-V 7B (Chen et al., 2024b) 74.3 53.1 67.6 68.1 44.8 23.2 49.8
CARE-7B (HuatuoGPT-V) 75.8 54.6 69.0 69.8 46.3 25.4 51.2
HuatuoGPT-V 7B (Chen et al., 2024b) 44.6 10.1 72.8 51.2 52.9 69.3
CARE-7B (HuatuoGPT-V) 46.3 12.2 73.9 53.0 54.6 71.0

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给节选仅出现表 3 的标题，没有提供任何消融行或数值，因此无法核验因果充分性筛选、近端可学习性窗口、在线组相对探索、经验回放及难度权重各自的独立贡献，也无法返回满足证据要求的定量消融结论。
- 主要结果只给出单次基准分数，未报告多随机种子均值、方差、置信区间或统计显著性；同时，节选没有展示专门衡量“正确但推理不一致”的指标或人工推理质量评审，所以最终答案分数的提升不能直接证明伪相关推理已经被因果机制消除。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Hulu-Med-7B：CARE-7B 的直接初始化骨干，是最关键的受控基线；二者采用相同基础架构时，分数差异主要用于衡量 CARE 训练框架而非模型规模或骨干更换带来的收益。
- HuatuoGPT-V 7B：第二个医疗视觉语言骨干。比较原模型与 CARE-7B（HuatuoGPT-V）用于检验 CARE 是否依赖 Hulu-Med 的特定架构。
- Lingshu-7B：较强的同规模医疗模型，用于判断 CARE 相对于现有领域专用模型是否仍有竞争优势，而不只是超过自身骨干。
- GPT-4.1：闭源专有模型参照，用于呈现 CARE-7B 与更大通用系统之间的能力位置；由于模型规模、训练数据和访问条件并不相同，这不是严格受控比较。

**实验想回答的问题**

- 在相同的医疗视觉语言骨干上，CARE 的因果充分性筛选、近端可学习性筛选与双流优化，能否在多模态医疗问答中稳定超过原始骨干及其他医疗模型？
- CARE 的收益能否跨越骨干架构与输入模态，在 HuatuoGPT-V 上复现，并迁移到纯文本医学知识与临床推理任务？

**实验实现**

CARE 主要建立在 Hulu-Med-7B 医疗视觉语言模型上，并额外在 HuatuoGPT-V 7B 上复现。训练数据混合了 PMC-VQA、SLAKE、PathVQA、MedMCQA 与 PubMedQA；评测覆盖七个多模态基准和六个表中列出的文本任务。作者声明训练样本与评测测试集无重叠，并沿用 Hulu-Med 官方评测协议、评分脚本和指标。训练使用 $8\times$A100 GPU，rollout batch 为 $128$、更新 batch 为 $64$，每个提示生成 $N=8$ 条在线轨迹。动态可学习窗口采用分位阈值 $\alpha=0.2$ 与 $\beta=0.9$，依据保存 $2000$ 个长度归一化负对数似然值的 FIFO 历史缓冲区更新；经验回放损失权重为 $\lambda=1.0$，KL 惩罚系数为 $0.04$，回放比例固定为 $50\%$。经验优化及回放缓冲区仅在批次 Pass@1 达到 $35\%$ 后启用。节选未报告随机种子、多次运行均值、标准差、置信区间或显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces a reinforcement-learning post-training framework that curates causally valid trajectories to improve and stabilize LLM medical reasoning.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`d32cfd292bc80529c3188d8e322f4a81e99a52489093170948a794ad099bef05`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
