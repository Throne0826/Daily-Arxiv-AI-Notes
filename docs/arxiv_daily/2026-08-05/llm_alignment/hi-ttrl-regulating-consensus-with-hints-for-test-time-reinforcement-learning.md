---
title: "[论文解读] Hi-TTRL: Regulating Consensus with Hints for Test-Time Reinforcement Learning"
description: "[arXiv 2608.03545][对齐 / RLHF] Hi-TTRL针对无标签测试时强化学习中“低共识导致错误多数被放大、高共识导致学习信号消失”的两难，在多数投票前用自适应生成的前缀提示调节采样共识，使伪标签可靠性与策略更新强度取得更稳定的平衡。"
arxiv_id: "2608.03545"
announcement_date: "2026-08-05"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:38:25.374235+00:00"
source_sha256: "48ca90f924298479b22996a2752cdd6e753840e059cf586b8ec003875e3eeaf1"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "测试时强化学习"
  - "大语言模型推理"
  - "多数投票"
  - "伪标签"
  - "共识强度"
  - "组相对策略优化"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.03545</p>

# Hi-TTRL: Regulating Consensus with Hints for Test-Time Reinforcement Learning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Kunbin Xu, Xingzuo Li, Xuefeng Bai, Kehai Chen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> School of Computer Science and Technology, Harbin Institute of Technology, Shenzhen, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03545v1) · [PDF 下载](https://arxiv.org/pdf/2608.03545v1) · **关键词** 测试时强化学习, 大语言模型推理, 多数投票, 伪标签, 共识强度, 组相对策略优化<br>


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

Hi-TTRL针对无标签测试时强化学习中“低共识导致错误多数被放大、高共识导致学习信号消失”的两难，在多数投票前用自适应生成的前缀提示调节采样共识，使伪标签可靠性与策略更新强度取得更稳定的平衡。

**不用术语来说**：模型在没有标准答案时，会对同一道题生成多份答案，把出现次数最多的答案暂当作正确答案并据此学习；但如果答案非常分散，勉强胜出的答案可能本来就是错的，模型却会被强力推向它，而如果答案几乎完全一致，各答案之间又没有足够差异，模型便难以继续学到东西。本文要解决的是：怎样在投票发生之前主动调整答案群体的一致程度，避免这两个极端。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将采样组中最常见答案的频率概括为共识强度，并据此揭示TTRL中的内在耦合：该量既反映多数投票伪标签的可信度，又影响GRPO组内优势的对比度；因此，过低与过高的共识分别可能放大噪声监督和造成梯度衰减。
- 作者提出Hi-TTRL：先用半批推理轨迹在线估计共识，只有当共识落在目标区间之外时才调用基于旧策略的MCMC前缀提示采样器；通过动态设置幂指数$\lpha>1$或$\lpha<1$，分别促进答案收敛或增加探索，并在最终多数投票与奖励分配前调节完整采样组。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大语言模型的复杂推理能力可通过强化学习进一步提升。强化学习可验证奖励（RLVR）利用标准答案生成确定、可核验的奖励，适合数学推理和代码生成，但依赖昂贵的高质量标注。测试时强化学习（TTRL）则面向无标签场景：模型对同一问题采样一组推理结果，以多数投票答案作为伪标签，再依据各结果是否匹配伪标签分配奖励，并通过组相对策略优化更新模型。本文关注这一自监督闭环中的“共识强度”问题，即多数答案在采样组中所占的频率；该量既近似反映伪标签可信度，也影响组内优势值与策略梯度的有效性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试时强化学习（TTRL）**

一种不使用外部标准答案、而是在测试阶段依据模型自身多次采样结果构造奖励并更新策略的方法。其关键假设是，多数投票得到的答案通常比单次生成更可靠。

</div>
<div class="concept-item" markdown="1">

**多数投票伪标签**

对同一问题生成多个回答，抽取其最终答案，并将出现次数最多的答案暂时视为正确答案。它不是真实标注，因此当回答分散、仅形成微弱多数时可能包含较大噪声。

</div>
<div class="concept-item" markdown="1">

**组相对策略优化（GRPO）**

一种利用同一输入下成组采样结果的相对奖励来估计优势并更新语言模型策略的强化学习方法。直观上，它提高组内高奖励回答的生成概率、降低低奖励回答的生成概率，但若组内奖励几乎完全相同，学习信号会趋弱。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是无标准答案的推理问题以及当前语言模型策略；模型针对每个问题采样一个 rollout 组 $cmathcal{Y}$，其中每个 rollout 包含推理过程和最终答案。系统统计组内最常见答案的频率 $c(\mathcal{Y})$，将该答案作为伪标签，并根据各 rollout 是否与之匹配形成规则奖励，随后使用 GRPO 更新策略。论文建立在两个关键现象上：当 $c(\mathcal{Y})$ 很低时，伪标签可能只是偶然形成的错误多数，但匹配它的少数样本会获得过大的相对优势；当 $c(\mathcal{Y})$ 很高时，组内结果和奖励缺少差异，归一化优势乃至策略梯度可能消失。因此，本文所处的问题设置不是改用外部监督，而是在最终投票与奖励分配之前调节采样结果的共识程度，使其落入一个稳定的目标区间。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{Y}$**

针对同一输入问题采样得到的 rollout 组，即一组完整推理轨迹及其答案。

</div>
<div class="notation-item" markdown="1">

**$c(\mathcal{Y})$**

rollout 组的共识强度，即组内出现频率最高的答案所占比例。

</div>
<div class="notation-item" markdown="1">

**$\alpha$**

幂变换目标分布的动态指数；$calpha>1$ 用于锐化分布并促进回答收敛，$calpha<1$ 用于展平分布并鼓励探索。

</div>

</div>

**直接相关的工作**

- **Zuo et al. (2025), Test-Time Reinforcement Learning**: 提供本文采用的基本无标签学习范式：通过多数投票构造伪标签和规则奖励，再在测试阶段更新模型。Hi-TTRL针对该范式中共识强度同时制约伪标签可靠性与优势估计的问题进行改进。
- **Shao et al. (2024), Group Relative Policy Optimization (GRPO)**: 提供TTRL用于策略更新的组相对优化目标。本文指出，GRPO的组内优势分布会随共识强度变化：共识过高时奖励对比不足，共识过低时不可靠多数可能得到过强更新。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

可验证奖励强化学习依赖大量带标准答案且能自动核验的数据，高质量领域标注带来较高的人力与计算成本，难以扩展到缺少标签的任务。TTRL虽可利用模型自己的多数投票生成伪标签，但训练效果取决于同组推理结果形成了何种共识：极弱或饱和的共识都会使自监督奖励失去良好的学习性质，因此无标签训练仍可能不稳定。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于多数投票伪标签的TTRL**：对同一输入采样一组推理轨迹，以最常出现的最终答案构造伪标签，再按轨迹是否匹配该答案给予规则奖励，并使用GRPO根据组内相对优势更新策略；它把奖励生成内化到模型自身，不需要外部真实标签。
- **奖励与优势阶段的稳定化方法**：已有工作主要在采样完成后处理不稳定监督，例如筛除可信度不足的伪标签、重新塑造奖励，或裁剪过大的优势值，以降低错误奖励或异常更新对策略训练的影响。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 多数投票与GRPO之间存在无法由简单投票消除的耦合：低共识意味着胜出的伪标签可能只是偶然的“错误多数”，但少数与它匹配的轨迹会获得不成比例的较大优势，从而把模型强烈推向有缺陷的推理路径。
- 高共识虽然通常使伪标签更可靠，却令组内结果和奖励趋于一致，使归一化优势缺少对比并最终产生趋近于零的梯度；而过滤、奖励重塑和优势裁剪主要是在采样之后补救，不能主动改变造成噪声或信号消失的轨迹分布。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究主要干预多数投票之后的奖励分配和优势估计，而原文指出，在采样阶段直接调节共识强度仍未得到探索。缺少的是一种不依赖真实标签、能够在线识别共识所处极端，并在最终投票前双向改变后续轨迹分布的机制。

</div>
<div markdown="1"><span>核心问题</span>

能否仅利用当前或旧策略自身的信息，先从部分采样估计共识，再通过可控的前缀提示使低共识组趋于集中、使高共识组适度分散，从而把最终共识引导到稳定区间，同时兼顾伪标签可靠性与非退化的优势信号？

</div>
<div markdown="1"><span>作者直觉</span>

提示前缀会改变后续推理的条件分布，因此不必等到错误投票或梯度消失后再修补奖励。将旧策略的前缀分布作幂变换时，$\lpha>1$会突出原本概率较高的前缀，使分散答案更容易向主要模式汇聚；$\lpha<1$会压平概率差异，让替代推理路径更容易被采到。先观察半批结果、仅在越界时选择相反方向的调节，相当于给采样过程加上反馈控制：困难且分歧大的组获得适度收敛，过于同质的组获得受控探索。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Hi-TTRL是在测试时进行无标签强化学习的采样—更新框架。给定问题$x$，旧策略$\pi_{\theta_{\mathrm{old}}}$先生成半组推理回答，并用多数答案所占比例估计共识强度$c^{(1)}$；若其处于目标区间$[\tau_{\mathrm{low}},\tau_{\mathrm{high}}]$，直接用这半组样本执行标准GRPO更新。若共识过低或过高，则先通过有限步、分块式MCMC近似幂变换前缀分布，再让旧策略在这些提示前缀之后完成推理，最后合并两阶段样本，重新投票、赋予伪奖励、计算组内优势并更新策略。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 第一阶段采样与在线共识估计

从$\pi_{\theta_{\mathrm{old}}}(\cdot\mid x)$独立采样$G/2$个回答，抽取其最终答案并以出现次数最多的答案作为中间伪标签；该伪标签在样本中的频率就是第一阶段共识$c^{(1)}$。

<div class="method-step__io" markdown="1">

**输入**：测试问题$x$、旧策略$\pi_{\theta_{\mathrm{old}}}$以及完整触发组规模$G$。<br>
**输出**：第一阶段样本集$\mathcal{Y}^{(1)}$、中间多数答案和共识强度$c^{(1)}$。

</div>

**直观理解**：先让模型独立解题若干次，再看最常见答案获得了多少票；票数占比用于判断当前多数意见是分裂、适中还是几乎完全一致。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按目标区间决定是否干预

若$\tau_{\mathrm{low}}\le c^{(1)}\le\tau_{\mathrm{high}}$，不再增加样本，直接令更新集为$\mathcal{Y}^{(1)}$；若$c^{(1)}$落在区间外，则启动第二阶段提示采样。

<div class="method-step__io" markdown="1">

**输入**：共识$c^{(1)}$和目标区间$[\tau_{\mathrm{low}},\tau_{\mathrm{high}}]$。<br>
**输出**：直接更新决策，或低共识/高共识两种提示触发信号。

</div>

**直观理解**：适度一致意味着伪标签已有一定支持，同时正确与错误样本之间仍有可学习的奖励差异，因此无需额外干预；只有过度分裂或过度一致时才追加计算。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 幂目标MCMC生成共识自适应提示

低共识时以$\alpha_{\mathrm{low}}>1$近似采样一个长度为$4B$的长锚定前缀，使高概率推理方向进一步集中；高共识时以$\alpha_{\mathrm{high}}<1$采样四个长度为$2B$的短前缀，提升仍受旧策略支持的次高概率方向。MCMC按块执行少量子序列重采样，前缀生成与似然评估均只调用当前旧策略。

<div class="method-step__io" markdown="1">

**输入**：问题$x$、旧策略、触发类型、块大小$B$以及相应幂指数。<br>
**输出**：低共识提示池$\mathcal{H}_{\mathrm{low}}(x)$或高共识提示池$\mathcal{H}_{\mathrm{high}}(x)$。

</div>

**直观理解**：意见太散时，给大家一个较长的共同开头，让后续解法向同一片搜索空间收拢；意见太一致时，提供多个较短的不同开头，在不彻底偏离模型能力范围的前提下重新引入少数派解法。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提示条件下补全并构造最终更新组

旧策略在条件$(x,h)$下继续自回归生成剩余推理$\tilde y$，形成完整回答$y=[h;\tilde y]$；触发时生成额外$G/2$个回答并与第一阶段样本合并，否则沿用第一阶段样本。

<div class="method-step__io" markdown="1">

**输入**：提示池、问题$x$、旧策略以及第一阶段样本$\mathcal{Y}^{(1)}$。<br>
**输出**：自适应大小的最终更新集$\mathcal{Y}_{\mathrm{upd}}(x)$，其规模为$G/2$或$G$。

</div>

**直观理解**：MCMC只负责挑选“从哪里开始想”，完整答案仍由同一个模型续写；额外样本只用于最需要纠正共识的题目。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 多数答案与共识强度

$$
c(\mathcal{Y})=\frac{1}{m}\sum_{i=1}^{m}\mathbb{I}[a_i=\hat a],\qquad \hat a=\arg\max_{a\in\mathcal{A}}\sum_{i=1}^{m}\mathbb{I}[a_i=a]
$$

**符号说明**

- $\mathcal{Y}=\{y_i\}_{i=1}^{m}$：由旧策略采样的、包含m条完整推理回答的组
- $y_i$：第i条推理回答
- $a_i=\operatorname{Ans}(y_i)$：从第i条回答中抽取的最终答案
- $\mathcal{A}$：候选最终答案的集合
- $\hat a$：组内出现次数最多的答案，即多数投票产生的伪标签
- $\mathbb{I}[\cdot]$：指示函数；条件成立时取1，否则取0
- $c(\mathcal{Y})$：多数答案在该组中的出现比例，即共识强度

<div class="equation-explanation" markdown="1">

**直观理解**：该式先找出票数最多的答案，再计算它占全部回答的比例。例如十个回答中有六个答案相同，则共识为$0.6$；Hi-TTRL用这一比例决定是否需要通过提示改变后续采样。<br>
**原文位置**：Method—Preliminaries，式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 幂变换提示目标分布

$$
q_{\alpha}(h\mid x)\propto\pi_{\theta_{\mathrm{old}}}(h\mid x)^{\alpha}
$$

**符号说明**

- $q_{\alpha}(h\mid x)$：给定问题时，幂指数为alpha的目标提示前缀分布
- $h$：不包含完整答案的部分推理前缀
- $x$：当前测试问题
- $\pi_{\theta_{\mathrm{old}}}(h\mid x)$：更新前旧策略生成此前缀的条件概率
- $\alpha$：控制目标分布尖锐或平坦程度的正幂指数
- $\propto$：成比例关系；右侧还需除以覆盖所有候选前缀的归一化常数

<div class="equation-explanation" markdown="1">

**直观理解**：幂变换不改变前缀的概率排序，但会改变概率差距：$\alpha>1$让原本常见的前缀更占优势，从而促进收敛；$0<\alpha<1$让较少见但仍由旧策略支持的前缀更容易被选中，从而增加分支多样性。<br>
**原文位置**：Method—Power-Target MCMC Hint Sampling，式(6)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：Hi-TTRL没有提出新的强化学习损失，而是保留标准GRPO更新：最终多数答案充当无标签伪标签，与其匹配的回答获得正向伪奖励，随后在$\mathcal{Y}_{\mathrm{upd}}(x)$内进行优势归一化并计算策略梯度。方法的创新位置在目标计算之前——通过幂目标提示改变参与最终投票和奖励分配的回答分布，使低共识组的伪标签更有支持，并使高共识组恢复奖励对比；所给章节未展开标准GRPO目标的完整公式。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 共识区间控制器**

控制器把共识定义为组内最高频答案的比例，并将$c^{(1)}$与$[\tau_{\mathrm{low}},\tau_{\mathrm{high}}]$比较。低共识意味着伪标签支持不足却可能产生较大的组内优势，高共识则意味着奖励趋同、优势和梯度可能消失。

> 直观理解：该模块把“多数票是否可信”和“样本之间是否还有学习差异”放在同一个统计量中权衡，目标不是让所有回答越一致越好，而是维持可用于学习的适中一致程度。

**2. 幂目标分块MCMC提示采样器**

采样器以$q_\alpha(h\mid x)\propto\pi_{\theta_{\mathrm{old}}}(h\mid x)^\alpha$为目标，仅对短推理前缀进行有限步分块重采样。$\alpha>1$放大原策略中高概率前缀的相对优势，$0<\alpha<1$压缩概率差距，但二者都不引入外部策略的轨迹或概率。

> 直观理解：直接对完整推理链做MCMC会反复调用长序列推理，成本较高；只选择短前缀相当于低成本地改变搜索入口，然后把剩余推理交还给原模型。

**3. 非对称提示配置**

低共识分支使用一个$4B$长前缀作为共享锚点，高共识分支使用四个$2B$短前缀作为多入口提示。前缀长度控制约束强度，前缀数量控制可探索分支数，因此两类异常不是用同一温度或同一种提示统一处理。

> 直观理解：低共识的问题需要“把答案拉到一起”，所以使用强而统一的引导；高共识的问题需要“温和地分开”，所以使用多个较弱入口，避免破坏已有多数答案。

**训练与推理**

这是测试时训练流程，而非仅改变一次解码：对每个无标签测试问题，当前旧策略先完成第一阶段采样和共识判断；区间内样本直接更新，区间外样本经过MCMC提示生成、条件补全和两阶段合并后再更新。每次更新的伪标签、奖励和优势都只依据该问题的最终更新组产生，不需要人工答案，也不使用外部或陈旧策略。

提示前缀本身不是最终预测，第二阶段仍由$\pi_{\theta_{\mathrm{old}}}(\cdot\mid x,h)$补全完整回答。所给方法章节明确描述了测试时策略更新，但未明确单独规定训练结束后的部署推理解码流程，因此不能据此断言最终推理时仍运行MCMC提示器。

**复现信息**

公平理解该方法所需的关键设置是：第一阶段固定采样$G/2$条回答；仅当$c^{(1)}$越出目标区间时再采样$G/2$条，使最终更新规模从$G/2$自适应增加到$G$。提示MCMC只作用于短前缀并按大小为$B$的块生长；低共识使用一个$4B$长提示和$\alpha_{\mathrm{low}}>1$，高共识使用四个$2B$短提示和$\alpha_{\mathrm{high}}<1$。

前缀提议、似然评估及后续补全全部使用同一旧策略，避免外部模型造成能力或知识混入。给定节选未明确报告$G$、$B$、目标阈值、两个幂指数及每块MCMC步数的具体取值；这些参数必须查阅论文其余实现章节或代码后才能完整复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- AMC2023 与 AIME2024：数学竞赛题基准，主要检验模型处理竞赛式、多步且答案较精确的数学推理能力。AMC2023 还被用于预备诊断、分支消融和直接采样控制实验，因此承担机制验证集的角色。原文节选未明确报告样本规模、训练/测试划分或是否使用完整测试集。
- MATH-500 与 MINERVA：覆盖一般高难度数学题和技术性数学推理的基准，用于判断共识调节能否跨题目来源与难度泛化。MINERVA 在直接采样控制实验中尤其用于检验方法的稳健性，因为温度和 top-$p$ 控制在该基准上出现明显退化。原文节选未明确报告具体规模与数据划分。
- GAOKAO2023-en：英文高考数学题基准，用于补充不同考试来源和题型分布下的评估。它也揭示方法并非逐项占优：在 Qwen3-4B-Base 上，Hi-TTRL 的两种解码评估均略低于 TTRL。原文节选未明确报告样本规模与数据划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**greedy@1**

对每道题进行一次确定性贪心解码，并计算最终答案准确率，侧重衡量训练后模型在不依赖多次采样时的单次稳定推理能力。 （越高越好，因为更高数值表示更多题目的单次贪心输出得到正确最终答案。）

</div>
<div class="metric-item" markdown="1">

**mean@16**

对每道题进行 16 次随机采样并汇总平均答案准确率，衡量模型在随机解码分布下产生正确答案的总体能力，而不是多数投票后的 pass rate。 （越高越好，因为更高数值表示随机采样得到正确答案的平均比例更高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三个骨干模型、五个数学基准的跨模型平均结果

<div class="result-value" markdown="1">

作者报告 Hi-TTRL 在三个骨干上都取得最高平均性能；相对 TTRL，Qwen2.5-Math-1.5B、Qwen3-1.7B-Base 和 Qwen3-4B-Base 的 greedy@1/mean@16 平均准确率分别提高 9.87/7.40、3.34/2.70 和 2.54/1.49 个百分点。

</div>

该结果表明收益不只存在于某一个模型系列或某一种解码方式，因而支持“共识调节具有跨骨干适用性”的作者主张。提升在较小的数学专用模型上最大，说明该机制可能在原始探索与伪标签质量较不稳定时更有价值；但这只是三个 Qwen 系骨干上的证据，不能直接证明可迁移到其他模型家族或非数学任务。

<div class="result-source" markdown="1">

来源：Main Results，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

It achieves the best average performance for all three backbones, improving over TTRL by 9.87/7.40 points on Qwen2.5-Math-1.5B, 3.34/2.70 points on Qwen3-1.7B-Base, and 2.54/1.49 points on Qwen3-4B-Base under greedy@1/mean@16, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen2.5-Math-1.5B 上的平均性能

<div class="result-value" markdown="1">

在提升最明显的骨干 Qwen2.5-Math-1.5B 上，Hi-TTRL 将五个基准的平均 greedy@1 从 42.34 提高到 52.21，将平均 mean@16 从 42.27 提高到 49.67。

</div>

单次贪心输出和多次随机采样的平均正确率同时提高，说明方法不仅改变采样多样性，也改善了训练后策略本身的确定性预测。不过平均值可能掩盖不同数据集上的难度差异；它不能说明所有题型获得等量提升，也不能单凭均值判断额外 MCMC 提示采样的计算收益比。

<div class="result-source" markdown="1">

来源：Main Results，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The gains are most pronounced on the smaller math-specialized backbone, where Hi-TTRL raises the average greedy@1 score from 42.34 to 52.21 and the average mean@16 score from 42.27 to 49.67.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen3-4B-Base 上逐基准比较 Hi-TTRL 与 TTRL

<div class="result-value" markdown="1">

Hi-TTRL 并非在每个单项上都胜过 TTRL：AIME2024 的 mean@16 下降 0.21 个百分点；GAOKAO2023-en 的 greedy@1 和 mean@16 分别下降 0.52 和 0.45 个百分点。其余所列单项总体匹配或超过 TTRL。

</div>

这些小幅负差揭示共识调节并非无条件改善所有任务分布。尤其在较大骨干已经具有较高性能时，额外改变共识可能轻微损害部分基准。由于节选没有给出显著性检验，不能断言这些差异具有统计显著性；同时，这些例外也不推翻整体平均提升。

<div class="result-source" markdown="1">

来源：Main Results，Table 1；具体差值见 Appendix B，Table 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At the benchmark level, Hi-TTRL generally matches or surpasses TTRL, with only minor drops on Qwen3-4B-Base for AIME-2024 mean@16 and GAOKAO2023-en.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验范围集中于五个数学推理基准和三个 Qwen 系开放权重骨干，尚未验证非数学任务、其他模型家族、指令微调模型或更大参数规模。因此，“跨模型一致有效”应限定为本文所测骨干，而不能外推为通用结论。
- 虽然每项评估重复十次并报告标准差，但节选未提供显著性检验、训练随机种子间方差、MCMC 提示采样的额外计算成本或与等计算预算基线的比较。部分差值较小且存在单项退化，因而方法的统计可靠性与成本效益仍需进一步核验。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Baseline：未经所比较测试时强化学习方法更新的对应骨干模型，用来衡量 TTRL、Intuitor 和 Hi-TTRL 相对原始模型的适应收益。节选未进一步说明该行是否采用完全相同的推理提示与采样配置。
- TTRL：核心对照方法，通过同一提示的多次 rollout 进行多数投票，以多数答案构造无标签伪奖励，再用 GRPO 更新策略。它与 Hi-TTRL 使用相同优化框架，因而比较主要隔离了“采样前调节共识并加入提示”所带来的作用。
- Intuitor：以模型自身的确信度作为内部奖励信号的无标签基线。它用于比较两类伪监督来源：Hi-TTRL/TTRL 依赖组内答案共识，而 Intuitor 依赖单个模型输出所反映的自确信度。
- TTRL + Temp 与 TTRL + Top-$p$：两种直接采样控制对照。前者在低、高共识分支分别采用温度 $T=0.5$ 和 $T=2.0$；后者分别采用 top-$p=0.8$ 和 top-$p=1.0$。它们检验仅通过降低或提高采样熵，是否足以复现 Hi-TTRL 的结构化前缀引导效果。

**实验想回答的问题**

- 在无标签测试时强化学习中，先依据部分 rollout 的共识强度，自适应地对低共识组施加收敛提示、对高共识组施加探索提示，是否能比标准 TTRL 和基于自确信度奖励的方法更稳定地提升数学推理准确率？
- Hi-TTRL 的收益究竟来自低共识分支、高共识分支的单独作用，还是来自两者的自适应组合；简单调节温度或 top-$p$ 所产生的熵变化能否替代结构化的前缀提示？

**实验实现**

实验覆盖三个开放权重骨干：Qwen2.5-Math-1.5B、Qwen3-1.7B-Base 和 Qwen3-4B-Base；前者是数学专用小模型，后两者是不同规模的通用基础模型。所有比较方法都在相同训练配置下使用 GRPO 优化，并同时报告 greedy@1 与 mean@16。每项评估重复十次，主表报告平均准确率，附录表进一步给出十次重复结果的标准差。预备诊断在 Qwen2.5-Math-1.5B 与 AMC2023 上进行：每个训练步抽取 8 个提示，每个提示生成 32 条 rollout 用于多数投票，再选取其中 16 条执行 GRPO 更新；共识强度被划分为低区间 $[0,0.25)$、中区间 $[0.25,0.75)$ 和高区间 $[0.75,1]$。诊断使用真实答案计算分支准确率和错误提升率，但真实答案不参与奖励构造。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| AMC2023 上分别启用低共识收敛分支、高共识探索分支，以及完整 Hi-TTRL | 在 Qwen2.5-Math-1.5B 上，TTRL、with-low、with-high 和完整 Hi-TTRL 的 greedy@1/mean@16 分别为 44.58/44.88、48.19/45.02、48.07/45.11 和 51.81/48.12；在 Qwen3-4B-Base 上分别为 46.69/48.19、46.02/47.62、53.86/53.70 和 54.22/54.49。完整方法在四个比较列中均为最佳。 | 该消融隔离了两类触发机制。小骨干从任一单分支都能获益，但大骨干主要受益于高共识探索分支，低共识分支单独使用反而略低于 TTRL；完整方法仍然最好，支持两分支按共识状态自适应协作，而不是固定采用一种提示。不过实验只在 AMC2023 和两个骨干上进行，尚不足以确定各分支在所有数据集中的贡献。 | Table 2，列顺序为 Qwen2.5-Math-1.5B greedy/mean 与 Qwen3-4B-Base greedy/mean<br><span class="experiment-evidence">TTRL 44.58 44.88 46.69 48.19; with-low 48.19 45.02 46.02 47.62; with-high 48.07 45.11 53.86 53.70; Hi-TTRL 51.81 48.12 54.22 54.49</span> |
| Qwen3-1.7B-Base 上以分支相关温度或 top-$p$ 调节替代 MCMC 前缀提示 | 在 AMC2023 上，TTRL + Temp 和 TTRL + Top-$p$ 均优于标准 TTRL，但仍低于 Hi-TTRL；在 MINERVA 上，两种直接控制相对 TTRL 明显退化，而 Hi-TTRL 在两项指标上均超过 TTRL。节选未提供 Table 3 的具体数值。 | 这一比较控制了“根据共识改变采样随机性”这一共同因素。如果简单温度或 top-$p$ 调节已经足够，它们应接近 Hi-TTRL；但其跨数据集表现不稳定，说明 Hi-TTRL 的收益更可能来自对 rollout 前缀进行结构化引导，而非一般性的熵增减。由于缺少节选中的具体分数和计算预算，该证据只能支持效果差异，不能量化稳健性或效率优势。 | Ablation Study，Comparison with Direct Sampling Controls，Table 3<br><span class="experiment-evidence">On MINERVA, both direct controls degrade substantially relative to TTRL, whereas Hi-TTRL improves over TTRL on both metrics.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper proposes a test-time reinforcement-learning method that regulates rollout consensus with sampled hints to improve LLM reasoning.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`48ca90f924298479b22996a2752cdd6e753840e059cf586b8ec003875e3eeaf1`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
