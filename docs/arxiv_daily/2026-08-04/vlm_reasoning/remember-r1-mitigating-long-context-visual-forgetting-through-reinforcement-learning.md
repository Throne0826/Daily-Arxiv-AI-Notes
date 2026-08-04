---
title: "[论文解读] Remember-R1: Mitigating Long-Context Visual Forgetting through Reinforcement Learning"
description: "[arXiv 2608.01314][VLM Reasoning] Remember-R1通过在原始多模态推理轨迹上施加过程级强化学习监督，促使模型在长链推理的中后期持续、准确地利用与问题相关的视觉证据，从而缓解视觉遗忘。"
arxiv_id: "2608.01314"
announcement_date: "2026-08-04"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:02:44.134101+00:00"
source_sha256: "d60044bad9d0c2af4f189dcb2e2fa1e9c740b888ffa8602326d7c5a6ac6f485e"
tags:
  - "VLM Reasoning"
  - "对齐 / RLHF"
  - "LLM 其他"
  - "LLM Reasoning"
  - "多模态大语言模型"
  - "长上下文视觉遗忘"
  - "多模态思维链推理"
  - "视觉注意力"
  - "视觉 grounding"
  - "过程级监督"
  - "强化学习"
  - "原始推理轨迹"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.01314</p>

# Remember-R1: Mitigating Long-Context Visual Forgetting through Reinforcement Learning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Jianmin Chen, Jiaqi Tang, Wei Wei, Xiaogang Xu, Jiafei Wu, Zhe Liu, Qianzhou Wang, Yingying Yan, Botong Geng, Yuyang Xia, Lei Zhang, Qifeng Chen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Northwestern Polytechnical University Xi’an China；Northwestern Polytechnical University；Hong Kong University of Science and Technology Hong Kong China；Hong Kong University of Science and Technology；Zhejiang University Hangzhou China；Zhejiang University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01314v1) · [PDF 下载](https://arxiv.org/pdf/2608.01314v1) · **关键词** 多模态大语言模型, 长上下文视觉遗忘, 多模态思维链推理, 视觉注意力, 视觉 grounding, 过程级监督, 强化学习, 原始推理轨迹<br>


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

Remember-R1通过在原始多模态推理轨迹上施加过程级强化学习监督，促使模型在长链推理的中后期持续、准确地利用与问题相关的视觉证据，从而缓解视觉遗忘。

**不用术语来说**：多模态大语言模型面对数学、逻辑或空间问题时，往往需要一边观察图像一边进行多步推理；但回答越长，模型越容易把自己先前生成的文字当作主要依据，逐渐忽略图像。这样一来，早期对图像的误读或文字推断中的偏差会不断累积，最终使推理脱离图中事实，即使模型仍能生成表面连贯的答案。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者从“直接监督原始推理轨迹”的角度处理长上下文视觉遗忘，提出Remember-R1过程级强化学习框架；该框架在训练时约束视觉证据的使用方式，但不改变模型的推理流程，因而不要求在推理期间重新插入图像或增加额外交互。
- 作者将持续利用视觉证据分解为三个互补目标：覆盖更多与图像标注匹配的视觉关键词、减缓推理后期对视觉信息依赖的衰退，以及把注意力集中到与当前问题相关的关键图像区域，并分别设计奖励信号进行监督。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

多模态大语言模型（MLLM）同时处理图像与文本，并通过逐步生成的推理链完成数学、逻辑、空间推理和文档理解等任务。较长的推理链虽然可能提升复杂任务表现，却也会产生“长上下文视觉遗忘”：随着生成推进，模型对图像信息的关注和依赖逐渐减弱，后期推理更多受先前生成文本驱动，因而可能偏离图像中的事实。本文以视觉注意力作为诊断模型是否持续使用图像证据的信号，关注如何在不改变推理时输入与生成流程的前提下，使模型在整条原始推理轨迹中保持视觉依据。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多模态大语言模型（MLLM）**

能够联合接收图像和文本，并生成文本答案或推理过程的模型。本文讨论的模型需要在生成较长推理链时持续利用图像，而不能只依靠题目文字和已经生成的内容。

</div>
<div class="concept-item" markdown="1">

**多模态思维链推理**

模型围绕图像与问题逐步生成中间推理步骤，再得出最终答案。链条越长，模型越容易让先前文本占据主导，从而弱化后续步骤与原始图像的联系。

</div>
<div class="concept-item" markdown="1">

**视觉注意力与视觉遗忘**

视觉注意力表示生成当前文本时模型对图像信息的关注程度，可用于诊断图像证据在推理中的影响。视觉遗忘是指这种依赖随推理推进而下降，使后期步骤逐渐脱离视觉事实；注意力在本文中是诊断信号，但不能被简单等同于完整的因果解释。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个图像—问题对，模型输出包含多步推理过程及最终答案的长文本响应。研究假设复杂的数学、逻辑或空间问题需要模型在生成早期、中期和后期持续引用视觉证据；核心问题是训练阶段如何直接约束原始目标推理轨迹中的视觉证据使用，使模型覆盖与图像对应的关键信息、减缓后期视觉依赖衰退，并聚焦于问题相关区域，同时保持推理时流程不变。原文使用视觉注意力随生成阶段的变化来观察遗忘现象：正确响应通常在后期保持较高的视觉注意力并继续引用视觉事实，而错误响应往往出现更明显的后期下降，但所给章节没有给出正式的任务符号体系。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **视觉重引入方法（Yang et al., 2026；Sun et al., 2025a）**: 这类方法在推理期间重新加入原图、局部区域或视觉特征，以恢复模型对视觉证据的利用。它能够帮助长程推理，但重复视觉处理会增加计算与内存开销，并可能打断推理连续性；Remember-R1则不修改推理流程。
- **基于视觉声明代理交互的 grounding 方法（Tian et al., 2025）**: 这类方法在训练或推理过程中插入视觉声明代理，以加强视觉 grounding，即文本与图像事实的对应关系。然而监督作用于新增的代理交互，而非目标问题未经插入修改的原始推理轨迹；本文要填补的缺口正是直接监督视觉遗忘实际发生的原始轨迹。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

长链思维能够提升复杂视觉数学、逻辑、文档理解和空间推理的能力，但这些任务也要求模型在多个推理步骤中始终核对图像事实。原文观察到，随着生成持续进行，模型对图像的注意会下降，后续词元更多受先前生成文本驱动；错误回答尤其表现出更明显的后期视觉注意衰减。因此，长推理带来的计算空间并不自动转化为可靠推理，反而可能放大模型偏离视觉事实的风险。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **视觉信息重新引入**：在长推理过程中，把原始图像或选定的局部区域再次放入上下文，使模型重新访问视觉输入，以恢复对图像事实的关注。
- **视觉声明代理交互**：在推理链中插入额外的视觉声明或代理交互，用这些中间环节增强视觉落地，即建立生成内容与图像证据之间的对应关系，并把监督施加到新增的代理环节上。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 反复重新处理图像会增加推理阶段的计算量和内存开销，还可能打断原有推理链，使连续的思考过程被多次视觉重输入割裂。
- 视觉声明代理方法主要监督额外插入的代理交互，而视觉遗忘实际发生在原始目标回答的生成轨迹中；因此，这类监督不能直接约束未被改写的推理链如何在中后期保存和调用视觉证据。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种直接作用于原始目标推理轨迹的过程级训练信号：它既要监督模型在整条回答中是否持续使用视觉证据，又不能依赖推理时重新输入图像或插入辅助交互。更具体地说，尚缺少对视觉证据覆盖范围、后期依赖持久性以及问题相关区域定位这三个方面的联合约束。

</div>
<div markdown="1"><span>核心问题</span>

能否在不改变推理阶段流程的前提下，通过强化学习直接监督原始长链推理轨迹，使多模态模型在生成的中后期仍持续依赖正确且与问题相关的视觉证据，并由此减少视觉遗忘、提高复杂推理的可靠性？

</div>
<div markdown="1"><span>作者直觉</span>

视觉遗忘发生在模型正在生成的那条推理链上，因此最直接的干预位置也是这条轨迹本身。仅要求最终答案正确，无法区分模型究竟依据图像完成推理，还是碰巧从先前文本中猜中答案；相反，若训练奖励同时鼓励模型提及已匹配的视觉事实、避免视觉注意随步骤快速衰减，并持续查看与问题有关的图像区域，就能让模型在每一阶段都有动力回到视觉依据。通俗地说，该方法不是在模型“忘记看图”之后重新把图递给它，而是训练它在整个思考过程中始终记得该看什么、何时继续看。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Remember-R1把“视觉遗忘”定义为：多模态大语言模型在生成较长推理链时，后期越来越依赖已生成的文字，而减少对原始图像证据的使用。给定图像$\mathcal{I}$和问题$\mathcal{Q}$，策略模型自回归生成包含推理过程与最终答案的序列$Y=(y_1,\ldots,y_T)$。作者以最后一层注意力中分配给视觉词元的总质量$\Omega(t)$作为视觉依赖的可观测代理，并用早期与晚期注意力之差$\Delta_{\mathrm{vis}}$刻画遗忘程度；这一代理不能完整解释模型行为，但能够提供沿生成轨迹变化的过程信号。

方法的核心不是改变模型在推理时的结构，而是在强化学习训练中直接评价原始生成轨迹：轨迹是否覆盖了更多经标注的视觉关键词、后期是否仍保持视觉注意力、视觉注意力是否落在与问题相关的图像区域。三个过程奖励与答案正确性奖励相加，再通过组相对策略优化（GRPO）更新模型。直观地说，模型不只因“最后答对”得分，还会因“推理中持续提及看见了什么、一直回看图像、并看对位置”得分；训练完成后，推理仍只输入图像和问题，不需要关键词、框或额外奖励模型。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建视觉证据标注

使用Qwen-VL-Max分别从$I_i$提取短视觉关键词集合$\mathcal{K}_i$，并根据$(I_i,Q_i,A_i)$生成关键区域框集合$\mathcal{B}_i$；随后人工删除无视觉依据或冗余的关键词，修正类别、属性和框位置，并过滤仍有歧义的样本。

<div class="method-step__io" markdown="1">

**输入**：ViRL39K中的图像$I_i$、问题$Q_i$和仅用于离线标注的参考答案$A_i$。<br>
**输出**：经筛选的38,657个训练样本，每个样本带有视觉关键词$\mathcal{K}_i$和关键区域框$\mathcal{B}_i$。

</div>

**直观理解**：这一步先为训练数据制作一份“图中有哪些重要内容、回答该题应看哪里”的参考清单。参考答案$A_i$只帮助一次性制作清单，不会被交给正在训练或测试的模型，因此不构成策略模型的答案条件。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成原始推理轨迹并提取过程信号

对同一输入采样一组$G$条响应$\{Y_i\}_{i=1}^{G}$，并从每条响应的最后一层、多注意力头权重中读取各生成步对视觉词元的注意力。视觉词元集合记为$\mathcal{T}_v$，第$t$步的总视觉注意力为$\Omega(t)$。

<div class="method-step__io" markdown="1">

**输入**：标准输入对$(I_i,Q_i)$以及旧策略$\pi_{\theta_{\mathrm{old}}}$。<br>
**输出**：包含完整推理与答案的多条候选轨迹，以及每条轨迹逐步的视觉注意力和视觉关键词出现位置。

</div>

**直观理解**：同一道题让模型给出多个解法，再记录每个解法在说每个词时是否仍关注图像。这样可以在同组答案内部比较哪些推理过程更可靠，而不只比较最终答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算答案与三类视觉过程奖励

计算答案正确性奖励$r_{\mathrm{acc}}$，并分别计算视觉词汇奖励$r_{\mathrm{voc}}$、视觉记忆奖励$r_{\mathrm{mem}}$和关键区域奖励$r_{\mathrm{region}}$。四项直接相加得到总奖励$\mathcal{R}(Y,\mathcal{I},\mathcal{Q})$。

<div class="method-step__io" markdown="1">

**输入**：候选响应$Y$、正确性判定、关键词集合$\mathcal{K}_i$、关键区域框$\mathcal{B}_i$及逐步注意力。<br>
**输出**：每条候选轨迹的标量总奖励及其分项过程评价。

</div>

**直观理解**：评分同时回答四个问题：答案对不对、是否提到足够多的可见证据、推理后期是否还在看图、看的是否是解题所需区域。三种过程奖励分别约束“说出证据”“记住要看图”和“看对地方”，作用并不等价。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 以GRPO更新策略并保持标准推理接口

在组内对奖励进行均值和标准差归一化，得到每条响应的相对优势$\hat A_i$；随后使用裁剪概率比的代理目标更新$\pi_\theta$，并通过KL正则限制其偏离$\pi_{\mathrm{ref}}$。

<div class="method-step__io" markdown="1">

**输入**：同组$G$条响应的总奖励、当前策略$\pi_\theta$、旧策略$\pi_{\theta_{\mathrm{old}}}$和参考策略$\pi_{\mathrm{ref}}$。<br>
**输出**：学习到更持续利用视觉证据的策略模型；部署时仍由$(\mathcal{I},\mathcal{Q})$直接生成$Y$。

</div>

**直观理解**：模型重点模仿同一道题下相对更好的轨迹，裁剪和KL约束则防止一次更新过大。关键词、框和注意力评分器都是训练期的“教练”，推理时全部移除，所以不会增加用户输入或改变生成流程。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 三类过程奖励与总奖励

$$
\begin{aligned}
r_{\mathrm{voc}}(Y)&=\min\left(1,\frac{c}{|\mathcal{K}_i|}\sum_{k\in\mathcal{K}_i^{\mathrm{match}}(Y)}\frac{\tau(k)}{T_{\mathrm{eff}}}\right),\qquad T_{\mathrm{eff}}=\max(T,L_{\min}),\\
\Omega(t)&=\frac{1}{H}\sum_{h=1}^{H}\sum_{j\in\mathcal{T}_v}A_t^h(j),\\
\mu_{\mathrm{start}}&=\frac{1}{w}\sum_{t=1}^{w}\Omega(t),\qquad \mu_{\mathrm{end}}=\frac{1}{w}\sum_{t=T-w+1}^{T}\Omega(t),\qquad w=\max(1,\lfloor\gamma T\rfloor),\\
r_{\mathrm{mem}}(Y)&=1+\mu_{\mathrm{end}}-\mu_{\mathrm{start}},\\
R_B(t)&=\frac{\Omega_B(t)}{\Omega(t)+\epsilon_{\mathrm{den}}},\qquad \Omega_B(t)=\frac{1}{H}\sum_{h=1}^{H}\sum_{j\in S_{\mathrm{union}}}A_t^h(j),\\
r_{\mathrm{region}}(Y)&=\frac{1}{Z}\sum_{t=1}^{T}\frac{t}{T}R_B(t),\qquad Z=\sum_{t=1}^{T}\frac{t}{T},\\
\mathcal{R}(Y,\mathcal{I},\mathcal{Q})&=r_{\mathrm{acc}}(Y)+r_{\mathrm{voc}}(Y)+r_{\mathrm{mem}}(Y)+r_{\mathrm{region}}(Y).
\end{aligned}
$$

**符号说明**

- $Y=(y_1,\ldots,y_T)$：模型生成的完整响应，包含推理过程和最终答案；T为响应词元数。
- $\mathcal{I},\mathcal{Q}$：分别表示输入图像和问题。
- $\mathcal{K}_i$：样本i的人工核验视觉关键词集合。
- $\mathcal{K}_i^{\mathrm{match}}(Y)$：在响应Y中被精确匹配到的标注关键词子集。
- $\tau(k)$：关键词k在响应中最后一次匹配出现的词元位置。
- $T_{\mathrm{eff}},L_{\min},c$：分别为有效响应长度、长度归一化的最小下界和截断前的奖励缩放系数。
- $\Omega(t)$：生成第t步时，全部注意力头分配给所有视觉词元的平均总注意力质量。
- $H,h$：H为注意力头总数，h为注意力头索引。
- $\mathcal{T}_v$：模型输入中的视觉词元索引集合。
- $A_t^h(j)$：注意力头h中，第t步生成词元指向视觉词元j的注意力权重。
- $w,\gamma$：w为首尾比较窗口宽度，γ为窗口占响应长度的固定比例。
- $\mu_{\mathrm{start}},\mu_{\mathrm{end}}$：分别为响应首窗口和末窗口中的平均总视觉注意力。
- $\Omega_B(t),S_{\mathrm{union}}$：分别为第t步分配给关键区域词元的注意力质量，以及所有标注框对应视觉词元的并集。
- $R_B(t),\epsilon_{\mathrm{den}}$：分别为关键区域注意力占总视觉注意力的比例，以及防止分母接近零的数值稳定常数。
- $Z$：时间权重之和，用于将关键区域奖励归一化。
- $r_{\mathrm{acc}},r_{\mathrm{voc}},r_{\mathrm{mem}},r_{\mathrm{region}}$：分别为答案正确性、视觉词汇、视觉记忆和视觉关键区域奖励。
- $\mathcal{R}$：用于强化学习的四项奖励之和。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项奖励模型在更广范围、尤其在更晚位置提及标注视觉词；第二项比较推理开头和结尾的总视觉注意力，惩罚后期明显下降；第三项衡量每一步视觉注意力中有多少落在解题相关区域，并提高后期步骤的权重。最后将三种过程评价与答案正确性相加，使优化目标同时考虑结果和产生结果时是否持续使用了正确的视觉证据。<br>
**原文位置**：第3.2.1至3.3节，公式(5)至(16)

</div>

</div>

<div class="equation-block" markdown="1">

#### GRPO组相对优势与裁剪优化目标

$$
\begin{aligned}
\hat{A}_i&=\frac{\mathcal{R}(Y_i,\mathcal{I},\mathcal{Q})-\mu_{\mathcal{R}}}{\sigma_{\mathcal{R}}},\\
\rho_i&=\frac{\pi_\theta(Y_i\mid\mathcal{I},\mathcal{Q})}{\pi_{\theta_{\mathrm{old}}}(Y_i\mid\mathcal{I},\mathcal{Q})},\\
\mathcal{L}_i^{\mathrm{clip}}&=\min\!\left(\rho_i\hat{A}_i,\operatorname{clip}(\rho_i,1-\epsilon_{\mathrm{clip}},1+\epsilon_{\mathrm{clip}})\hat{A}_i\right),\\
\mathcal{J}(\theta)&=\mathbb{E}\!\left[\frac{1}{G}\sum_{i=1}^{G}\mathcal{L}_i^{\mathrm{clip}}-\beta D_{\mathrm{KL}}(\pi_\theta\parallel\pi_{\mathrm{ref}})\right].
\end{aligned}
$$

**符号说明**

- $G$：针对同一训练输入采样的响应数量。
- $Y_i$：组内第i条采样响应。
- $\hat{A}_i$：第i条响应经组内标准化后的相对优势。
- $\mu_{\mathcal{R}},\sigma_{\mathcal{R}}$：同组响应总奖励的均值与标准差。
- $\pi_\theta$：参数为θ的当前待优化策略。
- $\pi_{\theta_{\mathrm{old}}}$：用于生成本轮候选响应的旧策略。
- $\rho_i$：当前策略与旧策略对第i条完整响应所赋概率的比值。
- $\epsilon_{\mathrm{clip}}$：限制概率比更新范围的裁剪参数。
- $\mathcal{L}_i^{\mathrm{clip}}$：第i条响应对应的裁剪代理目标。
- $\mathcal{J}(\theta)$：训练时最大化的最终策略目标。
- $\pi_{\mathrm{ref}}$：用于KL正则化的参考策略。
- $D_{\mathrm{KL}}(\pi_\theta\parallel\pi_{\mathrm{ref}})$：当前策略相对参考策略的KL散度，用于度量策略偏移。
- $\beta$：控制KL正则强度的系数。
- $\mathbb{E}$：对训练输入与采样响应所取的期望。

<div class="equation-explanation" markdown="1">

**直观理解**：GRPO不另行训练价值网络，而是把同一输入下各响应的奖励按组标准化：高于组均值的轨迹获得正优势，低于组均值的轨迹获得负优势。概率比裁剪限制单次策略变化，KL项进一步阻止当前模型过度偏离参考模型，从而把视觉过程奖励转化为相对稳定的参数更新。<br>
**原文位置**：第3.3节，公式(17)至(20)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标是最大化$\mathcal{J}(\theta)$。对每个$(\mathcal{I},\mathcal{Q})$，旧策略采样$G$条完整响应，外部奖励评估器为每条响应计算$\mathcal{R}=r_{\mathrm{acc}}+r_{\mathrm{voc}}+r_{\mathrm{mem}}+r_{\mathrm{region}}$；组内标准化把绝对奖励转为$\hat A_i$，使更新依据同题候选之间的相对质量。随后，$\mathcal{L}_i^{\mathrm{clip}}$提高高优势响应在当前策略下的概率并压低低优势响应的概率，而$\epsilon_{\mathrm{clip}}$与$\beta D_{\mathrm{KL}}(\pi_\theta\parallel\pi_{\mathrm{ref}})$共同约束更新幅度。

这一目标的关键联系是：$r_{\mathrm{acc}}$保留任务正确性的最终约束，$r_{\mathrm{voc}}$促使轨迹显式覆盖视觉证据，$r_{\mathrm{mem}}$约束首尾视觉注意力衰减，$r_{\mathrm{region}}$约束视觉注意力的空间相关性。作者将四项直接相加，所给章节未说明额外分项权重；因此不能从原文推断各奖励经过了单独加权或自动平衡。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 视觉词汇奖励**

先对响应和关键词做小写化及轻微格式归一化，再执行严格的独立单词或短语精确匹配，不扩展同义词，且每个关键词最多计数一次。奖励按匹配关键词在响应中最后一次出现的位置$\tau(k)$加权，并以$T_{\mathrm{eff}}=\max(T,L_{\min})$归一化、用系数$c$缩放后截断到1；因此它同时鼓励覆盖更多$\mathcal{K}_i$成员，并鼓励在较晚位置继续明确引用视觉内容。

> 直观理解：只在开头罗列几个物体不能获得最高评价，模型需要在推理展开后仍用图像中的对象、属性、数量或空间关系支撑判断。严格匹配降低了规则评分的歧义，但也可能漏掉语义正确的同义表达，因此该奖励衡量的是“匹配到的标注词覆盖”，并不等同于完整的视觉理解。

**2. 视觉记忆奖励**

在最后一个Transformer层上，将第$t$个生成词元经全部$H$个注意力头分配给视觉词元集合$\mathcal{T}_v$的权重求和并按头平均，得到$\Omega(t)$。取窗口宽度$w=\max(1,\lfloor\gamma T\rfloor)$，比较首窗口平均注意力$\mu_{\mathrm{start}}$与末窗口平均注意力$\mu_{\mathrm{end}}$；末期相对初期下降越少，$r_{\mathrm{mem}}$越高。

> 直观理解：该模块关注的不是视觉注意力绝对值，而是推理结束时是否比开始时明显衰减。它直接针对长推理中“越想越只看自己的文字”的现象，但注意力只是视觉依赖的代理信号，较高注意力本身不保证推理一定正确。

**3. 视觉关键区域奖励**

对基于图像块的视觉编码器，将每个视觉词元$j$对应图像块的中心$c(j)$映射到标注框；所有落入任一$b_k\in\mathcal{B}_i$的词元组成$S_{\mathrm{union}}$。每一步计算关键区域注意力占全部视觉注意力的比例$R_B(t)$，再以$t/T$进行时间加权并归一化，使后期集中于问题相关区域的注意力贡献更大。

> 直观理解：视觉记忆奖励只能要求模型继续看图，却不能阻止它看无关背景；关键区域奖励进一步要求注意力落到真正支持答案的位置。后期权重更大，是因为方法特别要修复长推理后半段视觉依据逐渐丢失的问题。

**训练与推理**

训练阶段先离线构建标注：Qwen-VL-Max利用图像提取$\mathcal{K}_i$，并利用$(I_i,Q_i,A_i)$定位$\mathcal{B}_i$，再由人工核验。强化学习阶段，策略模型只能看到$(I_i,Q_i)$；它生成原始推理轨迹后，外部评估器才使用$\mathcal{K}_i$和$\mathcal{B}_i$进行精确词汇匹配、图像框到视觉词元映射，以及最后一层注意力统计。由此获得四项奖励，完成组内优势归一化、裁剪GRPO更新和KL正则化。

推理阶段不再运行标注器、人工核验、关键词匹配、框映射或奖励计算，也不向模型提供$A_i$、$\mathcal{K}_i$或$\mathcal{B}_i$。训练后的策略继续按标准自回归分解$P_\theta(Y\mid\mathcal{I},\mathcal{Q})=\prod_{t=1}^{T}P_\theta(y_t\mid\mathcal{I},\mathcal{Q},y_{<t})$生成推理和答案，因此Remember-R1增加的是训练监督，而不是部署时的新模块或额外输入。

**复现信息**

公平理解该方法需要保留四点。第一，训练语料来自扩充后的ViRL39K，人工过滤后共有38,657个带$\mathcal{K}_i$和$\mathcal{B}_i$的样本；关键词包含对象、属性、数量以及必要的短空间短语。第二，词汇奖励只做独立词或短语的精确匹配，每词至多计一次且不使用同义词扩展，这使奖励可复现但对措辞敏感。第三，视觉记忆与关键区域奖励均读取最后一个Transformer层并对$H$个注意力头平均；区域映射假定视觉编码器采用具有明确空间位置的图像块词元，并以图像块中心是否落入框内决定归属。第四，参考答案$A_i$只在一次性框标注阶段使用，策略训练和推理均不可访问。

所给方法章节没有明确报告Qwen-VL-Max的具体提示词、人工核验者数量或一致性、系数$c$、最小长度$L_{\min}$、窗口比例$\gamma$、稳定常数$\epsilon_{\mathrm{den}}$、GRPO组大小$G$、裁剪参数$\epsilon_{\mathrm{clip}}$、KL系数$\beta$及答案正确性奖励的具体判定规则。这些量会影响复现和奖励尺度，不能根据节选自行补全；同时，注意力被作者明确描述为视觉依赖的代理，而非对模型因果使用视觉证据的完整证明。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 训练数据：ViRL39K。作者在原数据上补充第$3.1$节所述的视觉关键词与关键区域标注，用于计算过程级奖励。原文未明确报告训练集的具体样本划分、增强后规模或是否使用独立验证集。
- 推理密集型评测：MathVision、MathVista和LogicVista，分别从视觉数学与视觉逻辑任务检验模型能否在多步推理中持续使用图像证据。它们是判断方法是否缓解长推理链视觉遗忘的核心基准；原文未在节选中报告各测试集规模与划分。
- 广义能力评测：MMVet、MMMB和MMStar覆盖多种通用多模态任务，RealWorldQA强调真实场景中的细粒度视觉识别。前一组用于检查收益能否超出推理专用任务，后一项用于检查强化推理是否损害基础视觉感知；原文未在节选中报告各测试集规模与划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**各基准官方评测得分**

作者遵循MathVision、MathVista、LogicVista、MMVet、MMMB、MMStar和RealWorldQA各自的标准协议，以表中得分衡量任务表现；节选仅明确称RealWorldQA使用准确率，未说明其余基准的具体计分公式，因此不应把所有列一概解释为准确率。 （越高越好，因为更高分表示在相应基准的官方标准下完成任务的能力更强。）

</div>
<div class="metric-item" markdown="1">

**平均视觉注意力比例**

统计不同推理步骤中分配给视觉词元的平均注意力占比，用于观察生成过程是否逐渐从图像转向已生成文本。比较重点是随步骤增长的衰减速度，而非单个时刻的绝对值。 （在长推理后期保持更高、下降更慢通常更好，因为这表示模型持续参考图像；但该指标本身不能证明注意到的是正确区域，也不能单独证明答案正确。）

</div>
<div class="metric-item" markdown="1">

**匹配标注视觉关键词数与关键区域注意**

前者衡量回答覆盖了多少与标注匹配的视觉关键词，后者衡量注意力与问题相关图像区域的对齐程度，分别对应视觉事实覆盖和视觉关注位置。节选未给出二者的具体归一化方式或数值刻度。 （通常越高越好，因为它们分别表示使用了更多相关视觉概念、并更集中于问题相关区域；但关键词增多也可能只是表面复述，仍需结合任务得分和注意力分析解释。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 相对同规模Qwen2.5-VL基础模型的推理密集型基准比较

<div class="result-value" markdown="1">

作者报告Remember-R1在MathVision上的$3\mathrm{B}/7\mathrm{B}$增益为$+3.78/+3.44$，在MathVista上为$+13.60/+7.50$，在LogicVista上为$+2.46/+1.79$；三个基准、两个规模的变化均为正，其中MathVista提升最大。

</div>

这说明过程级视觉监督与更好的视觉数学、逻辑推理结果相关，而且效果并非只出现在单一参数规模。尤其是MathVista的大幅提升支持该方法适合需要多步读取图像事实的任务。不过，这些结果没有单独证明提升完全来自“减缓视觉遗忘”，因为强化学习也可能同时改变推理长度、语言表达或答案策略；此外，节选没有重复实验和显著性检验。

<div class="result-source" markdown="1">

来源：第4.2节，Results on reasoning-intensive benchmarks

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Specifically, the 3B/7B gains are +3.78/+3.44 on MathVision, +13.60/+7.50 on MathVista, and +2.46/+1.79 on LogicVista.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Remember-R1-3B与Qwen2.5-VL-3B在七项基准上的比较

<div class="result-value" markdown="1">

表$2$中，基础模型七项得分依次为$20.90$、$51.90$、$40.49$、$52.98$、$80.60$、$54.73$和$65.22$；完整Remember-R1-3B依次达到$24.68$、$65.50$、$42.95$、$63.44$、$80.95$、$59.54$和$65.88$。这对应七项均提升，绝对增量分别为$3.78$、$13.60$、$2.46$、$10.46$、$0.35$、$4.81$和$0.66$。

</div>

结果覆盖推理、通用多模态和真实场景视觉感知，说明收益不是以明显牺牲某一类基准为代价；MathVista和MMVet的增幅最突出，而MMMB与RealWorldQA的变化较小。该比较能够说明训练前后得分一致上升，但因为表$2$是消融表且未报告误差范围，小幅增益是否稳定仍无法判断。

<div class="result-source" markdown="1">

来源：表2，列顺序为MathVision、MathVista、LogicVista、MMVet、MMMB、MMStar、RealWorldQA

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Remember-R1-3B | 24.68 | 65.50 | 42.95 | 63.44 | 80.95 | 59.54 | 65.88

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### LogicVista与MMStar上的逐步视觉注意力分析

<div class="result-value" markdown="1">

图$6$显示基础模型和Remember-R1的平均视觉注意力比例都会随推理步骤下降，但Remember-R1下降更慢，且差距在生成中后段更明显。节选未给出具体注意力比例或斜率数值。

</div>

这一过程指标直接对应论文所称的长上下文视觉遗忘：模型生成越久，分配给视觉词元的注意力越少；Remember-R1较慢的衰减说明它在后期仍更依赖图像。相同趋势同时出现在逻辑推理基准和通用多模态基准，提供了一定的跨任务证据。不过，注意力比例只是内部行为的代理指标，不能等同于因果解释，也不能保证较高注意力必然落在正确区域。

<div class="result-source" markdown="1">

来源：第4.3节Attention Ratio Analysis，图6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Compared with the base model, however, Remember-R1 shows a consistently slower decline, with the gap becoming more pronounced in the middle and later stages.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 节选未报告重复运行、随机种子、置信区间或显著性检验。MMMB和RealWorldQA等基准上的小幅变化可能落在训练或评测波动范围内，因此“稳定提升”的作者结论仍需多次独立实验支持。
- 视觉注意力比例、关键词数和关键区域注意都是视觉依赖的代理指标。注意力较高不必然表示正确使用视觉证据，关键词覆盖也可能来自表面复述；此外，训练仅采用ViRL39K、基础模型仅为Qwen2.5-VL两个规模，尚不能证明结论能推广到其他训练语料、模型架构或更长推理上下文。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Qwen2.5-VL-3B/7B：Remember-R1直接采用的同规模基础模型，因此该比较最能隔离过程级强化学习相对于原始模型的增益。
- Qwen2.5-VL-3B-GRPO（仅使用$r_{\mathrm{acc}}$）：控制强化学习算法与基础模型，只保留答案正确性奖励，用于判断过程级视觉监督是否提供了超越结果级监督的价值。
- Ocean-R1-3B、LMM-R1-3B与VLAA-Thinking-3B/7B：推理导向的多模态大模型，用于判断Remember-R1相对于专门增强长链推理的方法是否仍有竞争力。
- DeepSketcher-7B与TVC-7B：已有视觉遗忘缓解方法，是与本文问题设定最直接的对照；InternVL-4B/8B则作为不同模型家族的通用多模态参照。节选未提供表$1$的完整逐模型分数，因此不能据此量化Remember-R1对这些方法的领先幅度。

**实验想回答的问题**

- Remember-R1在$3\mathrm{B}$与$7\mathrm{B}$两种模型规模上，能否相对基础模型及已有多模态推理方法，稳定提升视觉数学、逻辑推理、通用多模态能力和细粒度视觉感知表现？
- 性能变化是否确实来自三类过程级奖励对视觉证据覆盖、后期视觉依赖和关键区域注意的约束，而非仅由答案正确性奖励或一般强化学习训练带来？

**实验实现**

作者分别以Qwen2.5-VL-3B和Qwen2.5-VL-7B为基础模型，在$8$张NVIDIA L20 GPU上训练；学习率设为$1\times10^{-5}$，GRPO组大小为$8$，两个规模采用相同超参数，以检查方法是否具有跨规模稳定性。评测遵循各基准的标准协议，但节选未明确报告解码策略、随机种子、重复运行次数、方差、显著性检验以及各基准的具体评分脚本，因此表中差异应视为报告得分差，而不能自动解释为统计显著提升。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 完整Remember-R1-3B对比仅使用正确性奖励$r_{\mathrm{acc}}$的Qwen2.5-VL-3B-GRPO | 准确率奖励版本在七项基准上的得分为$21.05$、$60.20$、$40.79$、$59.98$、$80.70$、$56.20$和$64.75$；完整模型为$24.68$、$65.50$、$42.95$、$63.44$、$80.95$、$59.54$和$65.88$，对应完整模型分别高$3.63$、$5.30$、$2.16$、$3.46$、$0.25$、$3.34$和$1.13$。 | 该对照隔离了“只奖励最终答对”和“同时约束推理过程如何使用图像”的差别。完整模型七项均更高，支持过程级奖励提供了结果级奖励无法替代的监督信号；但三种过程奖励同时加入，因此这一行不能区分各奖励的独立贡献，也不能排除奖励尺度或总奖励强度不同带来的影响。 | 表2；完整模型对照行为Remember-R1-3B<br><span class="experiment-evidence">Qwen2.5-VL-3B-GRPO ($r_acc)$ \| 21.05 \| 60.20 \| 40.79 \| 59.98 \| 80.70 \| 56.20 \| 64.75</span> |
| 分别移除视觉关键词奖励$r_{\mathrm{voc}}$、视觉记忆奖励$r_{\mathrm{mem}}$或关键区域奖励$r_{\mathrm{region}}$ | 完整模型在七项基准上均不低于三个单项移除版本。以MathVista为例，完整模型为$65.50$，移除$r_{\mathrm{voc}}$、$r_{\mathrm{mem}}$和$r_{\mathrm{region}}$后分别为$62.00$、$62.20$和$61.70$，下降$3.50$、$3.30$和$3.80$；图$7$还分别显示关键词匹配数减少、视觉注意衰减加快和关键区域注意降低，但原文未报告这些行为变化的具体数值。 | 单项移除实验分别检验三种奖励是否具有不可替代的边际作用。MathVista上三者被移除都会明显降分，且图$7$中的对应过程指标按设计方向恶化，支持三种奖励分别约束视觉内容覆盖、后期持续性和空间聚焦。需要注意，七项基准上的降幅并不均匀，例如某些移除版本在个别列分数相同；因此证据支持“互补且整体有效”，但不足以断言每项奖励在每类任务上都同等重要。 | 表2与第4.4节，图7<br><span class="experiment-evidence">Remember-R1 w/o $r_region$ \| 21.05 \| 61.70 \| 40.82 \| 62.50 \| 80.70 \| 58.20 \| 63.79</span> |

**定性案例**

- 图$5$的几何推理案例中，基础模型虚构了图中不存在的蓝色球体，并沿着这一错误文本前提计数出五个球；Remember-R1则持续核对形状、颜色和空间关系，识别出与问题匹配的两个立方体并答对。该案例直观展示了视觉遗忘如何演变为文本自洽但无图像依据的推理，也说明维持视觉落地可能阻止错误累积；但单个成功案例不能估计此类错误在数据集中的发生率或方法的平均因果效果。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过面向视觉证据覆盖、持续依赖和区域关注的过程奖励后训练多模态模型，以缓解长链视觉推理中的遗忘。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`d60044bad9d0c2af4f189dcb2e2fa1e9c740b888ffa8602326d7c5a6ac6f485e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
