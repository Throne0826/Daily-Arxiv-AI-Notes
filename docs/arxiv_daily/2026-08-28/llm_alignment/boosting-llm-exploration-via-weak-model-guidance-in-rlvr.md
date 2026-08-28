---
title: "[论文解读] Boosting LLM Exploration via Weak-Model Guidance in RLVR"
description: "[arXiv 2608.27420][对齐 / RLHF] 原文未明确报告。"
arxiv_id: "2608.27420"
announcement_date: "2026-08-28"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:31:10.654516+00:00"
source_sha256: "45aa8442d4fa6c3e66bb00d636af7b7972857db0b507f06b20f974c91b7e4bf7"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "强化学习"
  - "可验证奖励强化学习"
  - "组相对策略优化"
  - "策略熵"
  - "熵坍缩"
  - "推理覆盖度"
  - "跨模型前缀引导"
  - "pass@k"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.27420</p>

# Boosting LLM Exploration via Weak-Model Guidance in RLVR

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Xingyu Shen, Huishuai Zhang, Peng Li, Yinchun Wang, Dongyan Zhao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Wangxuan Institute of Computer Technology, Peking University；Affiliation: National Engineering Research Center of New Electronic Publishing Technologies</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27420v1) · [PDF 下载](https://arxiv.org/pdf/2608.27420v1) · **关键词** 可验证奖励强化学习, 组相对策略优化, 策略熵, 熵坍缩, 推理覆盖度, 跨模型前缀引导, pass@k<br>


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

本文属于大语言模型推理的强化学习后训练研究。其基本场景是可验证奖励强化学习（RLVR）：模型针对数学题等提示生成完整推理与答案，外部验证器依据答案是否正确给出奖励，训练再提高高奖励轨迹的生成概率。论文关注的不只是单次生成正确率，而是模型在重复采样时能否覆盖多条可能成功的推理路径；标准RLVR虽然常能提高$\mathrm{pass@1}$，却可能使策略熵迅速下降、概率集中于少量既有路径，从而降低大$k$下的$\mathrm{pass@}k$。本文据此将“推理覆盖度”视为与单次准确率并列的重要能力，并研究来自其他模型的部分推理前缀能否扩展目标模型的探索范围。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**可验证奖励强化学习（RLVR）**

模型生成推理答案后，由规则程序或外部验证器给出可核验的标量奖励，再用强化学习提高正确答案的概率。它不要求逐步人工标注推理过程，但训练效果取决于采样到的轨迹及奖励能否区分其质量。

</div>
<div class="concept-item" markdown="1">

**组相对策略优化（GRPO）**

GRPO对同一问题采样一组回答，以组内奖励的均值和标准差归一化每个回答的优势，因此不需要另行训练价值模型。其更新采用类似PPO的概率比裁剪，并可通过相对参考模型的KL惩罚限制策略偏移。

</div>
<div class="concept-item" markdown="1">

**策略熵与$\mathrm{pass@}k$**

策略熵衡量模型下一词分布的不确定性；熵过快下降意味着模型越来越固定地选择少量表达或推理路径。$\mathrm{pass@}k$表示一个问题在$k$次采样中至少出现一次正确答案的能力，大$k$结果因而更能反映推理覆盖度，而不只是最常见答案的正确率。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定问题提示$q$，目标策略$\pi_\theta$生成一组完整响应$\{r_i\}_{i=1}^{G}$，每个响应由外部验证器赋予奖励$R_i$，随后使用GRPO进行序列级强化学习。标准设置仅以原问题为生成条件；本文所研究的扩展设置还允许较小、较弱的辅助语言模型先生成部分推理轨迹，并将其作为目标模型续写时的外部前缀。核心假设是：不同模型因预训练数据、架构和优化过程不同，会对同一问题形成具有分布差异的推理轨迹；即使弱模型前缀并非高质量解答，它也可能把目标策略置于不熟悉的中间状态，迫使其探索原本低概率的后续路径。期望输出仍是可由验证器判定的完整答案，评价则需要同时考察单次成功率与大$k$重复采样下的覆盖能力。该设置不等同于知识蒸馏：辅助模型不是更强的教师，前缀的作用主要是非参数化扰动和探索引导，而非向目标模型传递标准答案。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\pi_\theta$**

参数为$\theta$的目标策略模型，即接受问题及可能的推理前缀并继续生成回答的模型。

</div>
<div class="notation-item" markdown="1">

**$\{r_i\}_{i=1}^{G}$**

针对同一提示采样得到的一组$G$个响应，用于GRPO的组内奖励比较。

</div>
<div class="notation-item" markdown="1">

**$R_i$**

外部验证器为第$i$个响应给出的标量奖励。

</div>
<div class="notation-item" markdown="1">

**$H_\theta(t_k\mid t_{<k})$**

目标策略在已有词元$t_{<k}$条件下，对位置$k$的下一词分布所具有的策略熵，用于衡量生成不确定性与探索程度。

</div>

</div>

**直接相关的工作**

- **Cui et al. (2025)**: 该工作指出语言模型在强化学习中可能以降低熵来换取性能，并采用熵正则化拓宽探索。本文以其揭示的熵坍缩为直接问题背景，但转而使用跨模型推理前缀这一非参数化扰动，而不是只修改目标函数。
- **Yue et al. (2025)**: 该工作利用$\mathrm{pass@}k$说明RLVR主要增强既有推理路径的置信度，同时可能缩小整体推理覆盖范围；在足够大的$k$下，基础模型甚至可能优于RLVR模型。本文沿用大$k$评估所代表的覆盖视角，研究弱模型前缀能否缓解这种多样性退化。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

RLVR通过外部可验证奖励提升大语言模型的推理能力，但训练过程可能迅速降低策略熵，使模型过度集中于少数已知推理轨迹。这样虽然可能提高单次采样的正确率，却会缩小可探索的解空间，降低在多次采样设置下发现不同正确解的能力；因此，如何在保持RLVR性能收益的同时维持推理多样性，是一个重要问题。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **训练目标与策略梯度正则化**：这类方法直接修改RLVR的内部优化过程，例如加入熵正则以抑制模型过度自信，或校准特定词元的策略梯度，使训练不要过快集中到少数推理路径。
- **奖励函数与优势函数设计**：这类方法通过重新设计奖励或优势估计，鼓励模型探索更多候选轨迹，而不是只强化当前已经获得高奖励的行为。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有方法主要在目标模型自身的生成分布和搜索空间内调整训练信号。它们能够重新分配梯度或抑制置信度上升，却难以主动提供目标模型原本较少访问的推理起点；其结果可能仍受目标模型固有分布的限制。
- 既有评估往往偏重$pass@1$，即单次生成的正确率，因而可能掩盖推理覆盖范围的下降。当采样次数$k$较大时，模型是否能够产生多条不同且至少一条正确的解答，才更能检验其探索能力；这一维度在RLVR中相对不足。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究关注通过内部正则化、梯度控制或奖励设计缓解熵坍缩，但较少研究跨模型、非参数的输入层引导能否改变RLVR的探索动力学。具体而言，尚不清楚由较小且较弱模型生成的部分推理轨迹，尽管可能错误或具有误导性，是否能够作为目标模型不熟悉的前缀，帮助其进入原本低概率的推理区域并扩大解答覆盖范围。

</div>
<div markdown="1"><span>核心问题</span>

在RLVR训练中，如果强制目标模型从较小弱模型生成的部分推理轨迹继续作答，而不是始终从原始问题独立开始，跨模型前缀引导能否有效减缓策略熵下降、扩大推理路径覆盖，并在尤其是较大$k$的$pass@k$评估中稳定优于标准RLVR？

</div>
<div markdown="1"><span>作者直觉</span>

不同模型因预训练数据、架构和优化过程不同，即使面对同一问题，也可能生成分布不同的推理轨迹。弱模型产生的前缀因此会把目标模型带到它平时不太可能自行选择的初始状态，打破其对少数熟悉路径的过度依赖；目标模型仍负责后续推理和接受可验证奖励，前缀的作用不是提供可靠答案，而是扩大探索的出发点。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法在标准 RLVR 的 GRPO 训练中加入跨模型前缀完成机制。首先由较小的辅助语言模型为问题生成完整推理轨迹，再依据目标模型的步级熵变化截取部分前缀；训练时，目标模型有一定概率基于该前缀继续推理并接受验证器奖励，另一部分时间仍从原问题直接生成答案。其核心不是让小模型充当高质量教师，而是利用不同模型之间的生成分布差异，使目标模型进入自身较少访问的推理状态，从而缓解 RLVR 中的策略熵坍缩并扩大可探索的解题轨迹覆盖范围。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 辅助模型生成候选轨迹

辅助模型从问题 $q$ 出发生成完整推理轨迹，并按换行符和句号将轨迹划分为推理步骤 $\{\tilde{s}_1,\ldots,\tilde{s}_M\}$。这些模型可以与目标模型使用不同的模型家族，以制造更明显的生成分布差异。

<div class="method-step__io" markdown="1">

**输入**：数学问题 $q\in\mathcal{D}$，其中 $\mathcal{D}$ 是训练问题集合；一个或多个较小的辅助模型。<br>
**输出**：候选完整轨迹 $\tilde{r}_{\mathrm{full}}=\{\tilde{s}_1,\ldots,\tilde{s}_M\}$。

</div>

**直观理解**：先让小模型写出一份解题草稿，但这份草稿主要用来提供一种不同的思路起点，并不要求它本身正确。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于目标模型熵的前缀截取

目标模型在观察每个辅助步骤后计算步级平均 token 熵，并找到相邻步骤间熵下降幅度最大的转折点 $L^*$；保留前 $L^*$ 个完整推理步骤作为前缀 $\tilde{r}=\{\tilde{s}_1,\ldots,\tilde{s}_{L^*}\}$。截取在步骤边界进行，避免把一个推理步骤从中间截断。

<div class="method-step__io" markdown="1">

**输入**：辅助模型的分步轨迹 $\tilde{r}_{\mathrm{full}}$，以及 RLVR 训练前的目标基座模型参数 $\theta_0$。<br>
**输出**：用于训练的部分辅助前缀 $\tilde{r}$。

</div>

**直观理解**：选择目标模型最不适应、最不确定的那一段附近作为切入点：前缀不能短到没有扰动，也不能长到把答案几乎全部告诉目标模型。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 混合式 RLVR 采样与奖励计算

以概率 $1-p$，目标模型仅以 $q$ 为条件生成完整轨迹 $r$；以概率 $p$，目标模型以 $(q,\tilde{r})$ 为条件生成后缀 $r_{\mathrm{suf}}$，并将其与前缀拼接为完整轨迹 $\tilde{r}\circ r_{\mathrm{suf}}$。验证器根据完整解答是否满足题目要求计算奖励，而不是单独评价前缀的教学质量。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、截取前缀 $\tilde{r}$、目标策略 $\pi_\theta$、前缀注入概率 $p$ 和可验证奖励函数 $R$。<br>
**输出**：两类 rollout：无前缀轨迹 $r$ 和前缀完成轨迹 $\tilde{r}\circ r_{\mathrm{suf}}$，以及各自的验证器奖励。

</div>

**直观理解**：训练数据一部分要求模型独立解题，另一部分要求它接着不同模型的草稿继续解题；这样既练习探索，也不丢失测试时需要的独立作答能力。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### GRPO 策略更新

GRPO 在同一问题的多条回答之间进行奖励标准化，得到序列级优势，并使用 PPO 风格的裁剪目标和相对于参考策略的 KL 正则更新目标模型参数。无前缀样本与前缀完成样本共同参与优化，使成功的替代推理路径获得更高概率，同时限制策略更新过度偏离参考模型。

<div class="method-step__io" markdown="1">

**输入**：每个问题对应的一组采样轨迹、验证器奖励、旧策略 $\pi_{\theta_{\mathrm{old}}}$ 和冻结参考策略 $\pi_{\mathrm{ref}}$。<br>
**输出**：训练后的目标策略 $\pi_{\theta^*}$，可在没有辅助前缀的条件下直接回答问题。

</div>

**直观理解**：如果某种续写最终通过验证器，模型就提高这类续写的概率；GRPO 同时用同题其他答案作参照，减少奖励尺度差异带来的不稳定。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 混合式前缀完成 RLVR 目标

$$
\begin{split}\theta^{*}=&\operatorname*{argmax}_{\theta}\mathbb{E}_{q\sim\mathcal{D}}\Big[(1-p)\mathbb{E}_{r\sim\pi_{\theta}(\cdot\mid q)}R(q,r)\\&+p\mathbb{E}_{r_{\mathrm{suf}}\sim\pi_{\theta}(\cdot\mid q,\tilde{r})}R(q,\tilde{r}\circ r_{\mathrm{suf}})\Big].\end{split}
$$

**符号说明**

- $\theta^{*}$：训练后目标策略的最优参数。
- $\theta$：训练过程中目标策略的参数。
- $q$：输入问题。
- $\mathcal{D}$：训练问题的数据分布或问题集合。
- $p$：使用辅助前缀进行训练的概率。
- $r$：目标模型仅根据问题 $q$ 生成的完整推理轨迹。
- $\pi_{\theta}$：参数为 $\theta$ 的目标策略，即目标语言模型的生成分布。
- $R(q,r)$：验证器对问题 $q$ 及完整轨迹 $r$ 给出的可验证奖励。
- $\tilde{r}$：由辅助模型生成并截取的部分推理前缀。
- $r_{\mathrm{suf}}$：目标模型在给定 $q$ 和 $\tilde{r}$ 后生成的推理后缀。
- $\circ$：轨迹拼接操作，将前缀 $\tilde{r}$ 与后缀 $r_{\mathrm{suf}}$ 连接成完整轨迹。

<div class="equation-explanation" markdown="1">

**直观理解**：目标是最大化两种训练情形的期望可验证奖励：一部分样本让模型独立回答，另一部分样本让模型接着陌生前缀回答。这样前缀样本负责扩大探索范围，普通样本负责保持模型在实际推理条件下的解题能力。<br>
**原文位置**：第 4.3 节，公式 (4)

</div>

</div>

<div class="equation-block" markdown="1">

#### 熵变化驱动的前缀长度选择

$$
L^{*}=\operatorname*{argmax}_{L}\left[\bar{H}_{\theta_{0}}(\tilde{s}_{L})-\bar{H}_{\theta_{0}}(\tilde{s}_{L+1})\right],\qquad \tilde{r}=\{\tilde{s}_{1},\cdots,\tilde{s}_{L^{*}}\}.
$$

**符号说明**

- $L^{*}$：选定的前缀最后一个推理步骤的索引。
- $L$：候选截断位置的推理步骤索引。
- $\bar{H}_{\theta_{0}}(\tilde{s}_{L})$：目标基座模型在观察辅助步骤 $\tilde{s}_L$ 时，该步骤内部 token 熵的平均值。
- $\theta_{0}$：RLVR 训练开始前目标基座模型的参数。
- $\tilde{s}_{L}$：辅助模型轨迹中的第 $L$ 个推理步骤。
- $\tilde{r}$：由前 $L^{*}$ 个辅助推理步骤组成的最终前缀。

<div class="equation-explanation" markdown="1">

**直观理解**：对每个候选位置比较当前步骤和下一步骤的平均不确定性，选择熵下降最大的位置，并保留其之前的步骤。直观上，这是在目标模型开始快速适应辅助轨迹之前停止，以保留最有价值的陌生性。<br>
**原文位置**：第 4.2 节，公式 (5)–(6)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：该方法仍以可验证奖励为最终优化信号，而不是为前缀额外设计奖励或进行额外监督微调。标准 RLVR 的目标是最大化 $\mathbb{E}[R(q,r)]$；加入前缀后，优化变为混合期望：无前缀样本优化 $R(q,r)$，前缀样本优化完整拼接轨迹的奖励 $R(q,\tilde{r}\circ r_{\mathrm{suf}})$。实际更新使用 GRPO：对同一问题采样多条回答，按组内奖励计算优势，再通过 PPO 式裁剪和 KL 正则更新目标策略；因此只有最终解答通过验证器时，辅助前缀引出的后续推理路径才会被强化。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 跨模型前缀引导**

前缀由辅助模型生成，而后缀由目标策略生成。由于辅助模型的轨迹通常与目标模型自身的高概率轨迹存在分布差异，目标模型在前缀后的早期步骤具有更高策略熵，这种非参数的轨迹级扰动将训练引向原本较少探索的推理状态。

> 直观理解：它不是把小模型的答案当作标准答案，而是把小模型的不同思路当作“换一条路走”的提示。

**2. 熵驱动的步骤级截断**

令 $\bar{H}_{\theta_0}(\tilde{s}_L)$ 表示目标基座模型在辅助步骤 $\tilde{s}_L$ 上的平均 token 熵，方法选择相邻步骤间最大熵降的位置作为截断依据。该位置近似对应目标模型从陌生状态逐渐适应辅助轨迹的转折点，因此保留转折点之前的前缀以维持较强的不确定性。

> 直观理解：方法寻找目标模型从“很不熟悉”变成“已经适应”的分界处，并在这里停止提供草稿。

**3. 混合训练目标**

训练目标以概率 $p$ 使用前缀完成 RLVR，以概率 $1-p$ 使用标准问题到完整答案的 RLVR。该设计将探索收益与训练—推理条件的一致性结合起来，避免模型过度依赖推理时不存在的外部前缀。

> 直观理解：不能每次都让模型接着小模型的草稿训练，否则测试时突然没有草稿可能不适应；因此必须保留直接解题样本。

**训练与推理**

训练阶段，辅助模型先为训练问题生成完整轨迹；目标基座模型据此计算步骤级熵并一次性确定每条轨迹的截断位置。之后每个问题按概率 $p$ 进入前缀完成分支，目标模型条件为 $(q,\tilde{r})$ 并生成后缀；按概率 $1-p$ 进入标准分支，仅以 $q$ 生成完整回答。两类完整轨迹都由验证器评分，并共同用于 GRPO 更新。推理阶段不需要辅助模型、前缀或额外提示，目标模型直接根据原问题 $q$ 生成答案；混合训练正是为了保证这种无前缀推理方式仍然有效。

**复现信息**

复现该方法至少需要：将辅助轨迹按换行符和句号切分为步骤；使用目标基座模型而非辅助模型计算每一步的平均 token 熵；在最大相邻熵降处截取完整步骤；对每个问题混合无前缀与有前缀 rollout；并使用同一验证器评价拼接后的完整解答。论文在主实验中将前缀注入概率设为 $p=0.2$，但所给章节未明确报告辅助轨迹的最大长度、熵计算时的具体 tokenization 细节、GRPO 组大小、裁剪系数或 KL 系数，因此这些内容不能据此补全。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MATH 训练集：包含 7,500 个互不重复的问题—答案对，用于通过 GRPO 训练目标模型。它提供可自动核验的数学答案，是本文 RLVR 训练的数据来源，而非主要泛化测试集。
- 竞赛数学测试组：AIME 2024、AIME 2025 与 AMC 2023。它们用于检验模型在高难度、答案可验证的竞赛题上的推理覆盖；由于题目数量相对较少，每题采样 200 个回答，以较稳定地估计较大 $k$ 下的 $\mathrm{pass@}k$。
- 综合数学测试组：MATH 500、Minerva 与 Olympiad Bench，分别覆盖一般高难度数学题、技术性定量推理及奥林匹克风格问题。每题采样 128 个回答，用于检验方法能否跨不同数学题型泛化，而非只适配 MATH 训练分布。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**$\mathrm{pass@}k$**

衡量每道题独立采样 $k$ 次时至少出现一个正确答案的概率。论文采用无偏估计 $\mathrm{pass@}k=1-\binom{N-c}{k}/\binom{N}{k}$，其中 $N$ 是每题总采样数，$c$ 是其中正确回答数；跨基准报告平均值。该指标尤其适合衡量推理覆盖：即使单次成功率相近，能覆盖更多有效路径的模型也可能在较大 $k$ 时表现更好。 （越高越好，因为它表示在给定采样预算内找到至少一个正确解的概率更大。）

</div>
<div class="metric-item" markdown="1">

**策略熵（Policy Entropy）**

衡量模型生成分布的分散程度。训练中熵过快下降意味着策略过早集中于少数高置信路径，可能损害多样性；本文用它判断前缀是否延缓探索坍缩。 （在本文机制分析中，训练早期相对较高更有利，因为它保留更多候选推理路径；但熵并非越高越好，过高也可能对应随机或低质量生成。）

</div>
<div class="metric-item" markdown="1">

**奖励结构指标**

包括平均奖励、零奖励比例和非平凡样本比例。平均奖励反映当前生成正确答案的总体水平；零奖励比例反映完全失败的样本或问题；非平凡样本比例用于观察同组回答是否包含异质奖励，从而能否为 GRPO 提供有效的相对优势信号。 （平均奖励与非平凡样本比例通常越高越好，零奖励比例通常越低越好；但本文强调前缀可能以暂时降低平均奖励为代价换取更充分的探索。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 多个数学基准上的弱模型前缀引导 RLVR 与 vanilla RLVR 对比

<div class="result-value" markdown="1">

作者声称，该方法在多个数学基准上持续优于 vanilla RLVR，而且随着 $k$ 增大，性能增益更明显，表明外部前缀主要扩展了多次采样时可覆盖的有效推理路径。

</div>

直观上，弱模型给出的部分推理会把目标模型带到它平常不常访问的中间状态，目标模型再尝试续写和纠错，因此多次采样更可能覆盖新的正确解法。该结果支持“推理覆盖扩大”的解释，但所给节选没有包含第 5.2 节的具体分数、误差或逐数据集表格，因此无法判断提升幅度、统计稳定性及每个基准是否都显著改善。

<div class="result-source" markdown="1">

来源：摘要；第 5.2 节具体结果表未包含在所给节选中

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Experiments across multiple mathematical benchmarks show that our method consistently outperforms vanilla RLVR.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen2.5-7B 使用或不使用 Gemma-2-2B 前缀的训练动态

<div class="result-value" markdown="1">

作者观察到，前缀引导方法在训练早期维持了高于 vanilla GRPO 的策略熵，从而延缓策略过早集中；训练后期的熵最终趋近基线。

</div>

这说明前缀的主要作用不是永久让模型输出更随机，而是在训练早期争取更长的探索窗口。它与大 $k$ 下覆盖改善的机制相容，但较高熵本身并不能证明推理质量更高，还需结合正确率和 $\mathrm{pass@}k$ 判断。

<div class="result-source" markdown="1">

来源：第 6.1 节，Figure 3(a)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Figure 3(a), our prefix-guided method maintains higher policy entropy than the vanilla GRPO baseline, especially in the early stage of training.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 前缀引导与 vanilla GRPO 的奖励动态对比

<div class="result-value" markdown="1">

作者报告，前缀会降低平均奖励，但同时使同组轨迹的奖励模式更异质，从而缓解 GRPO 中相对优势信号稀疏的问题；目标模型后期还能从不完美前缀中恢复并生成正确答案。

</div>

平均奖励下降是探索成本：弱模型前缀可能包含次优甚至误导步骤。另一方面，如果一组回答不再全部正确或全部错误，GRPO 就能比较轨迹优劣并获得训练信号。因此，该结果支持“用短期难度换取更有信息的梯度”，但不能单凭奖励异质性断定最终泛化一定提升。

<div class="result-source" markdown="1">

来源：第 6.1 节，Figure 3(b)–(d)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

By introducing external prefixes, our method diversifies the sampled trajectories and produces more heterogeneous reward patterns.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给来源节选缺少第 5.2 节的结果表，因此无法核验各数据集上的具体 $\mathrm{pass@}k$、绝对增益、方差或显著性；摘要中的“持续优于”属于作者总体结论，仍需对照完整论文表格复查。
- 实验范围集中于约 7B 参数的目标模型、1B–2B 的异构前缀模型和数学推理任务。现有证据不足以说明该方法能否扩展到更大目标模型、非数学任务或不可自动验证的开放式奖励场景。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Vanilla GRPO：不注入弱模型前缀、仅依赖目标模型内部采样进行探索的标准 RLVR 基线。它直接检验性能变化是否来自跨模型前缀这一干预，而不是来自更换强化学习算法。
- 不同前缀注入概率 $p$ 的 GRPO：包括无前缀与更高注入概率的设置，用于分析外部扰动强度如何改变策略熵和奖励结构；这是机制对照，而不是独立训练算法。
- 不同目标模型：Qwen2.5-7B 与 Qwen2.5-Math-7B，用于观察方法对通用模型和数学专用模型是否具有一致作用。
- 不同弱前缀模型：LLaMA-3.2-1B 与 Gemma-2-2B。二者与目标模型属于不同模型家族，因而可测试异构推理风格，而不只是同系列小模型知识蒸馏。

**实验想回答的问题**

- 在使用可验证奖励的强化学习（RLVR）中，由弱模型生成的外部推理前缀，能否相较标准 GRPO 缓解策略熵下降、扩大推理路径覆盖，并提升不同采样预算下的 $\mathrm{pass@}k$？
- 前缀注入概率及弱模型与目标模型之间的分布差异如何影响训练动态，包括策略熵、平均奖励、零奖励样本比例和非平凡样本比例？

**实验实现**

目标模型为 Qwen2.5-7B 和 Qwen2.5-Math-7B，前缀模型为 LLaMA-3.2-1B 和 Gemma-2-2B。训练使用 VeRL 实现 GRPO，学习率为 $10^{-6}$，不设预热；训练批量为 1,024，PPO mini-batch 为 256。每个训练问题以温度 1.0 采样 8 个回答，且不使用 KL 惩罚。弱模型以温度 0.4 生成前缀，以避免前缀质量过低。评测使用 vLLM，生成温度为 0.6，top-$p$ 为 0.95，最大生成长度为 4,096。MATH 500、Minerva 和 Olympiad Bench 每题采样 128 次；AIME 2024、AIME 2025 和 AMC 2023 每题采样 200 次。这样的多次采样协议支持估计大 $k$ 的 $\mathrm{pass@}k$，但不同测试组的总采样数不同，比较时应限定在各自可估计的 $k$ 范围内。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 改变弱模型前缀的注入概率 $p$ | 作者观察到，随着 $p$ 增大，策略熵轨迹一致上移，说明更频繁的外部分布扰动带来更强探索；节选未报告各概率对应的具体数值，也未给出哪个 $p$ 的最终性能最佳。 | 该消融隔离了“注入强度”的作用：若只改变 $p$ 就系统性改变熵，可将探索变化更直接地归因于前缀出现频率。不过，更高熵不必然意味着更高最终正确率，因此仍需与平均奖励和 $\mathrm{pass@}k$ 联合解读。 | 第 6.1 节，Figure 3(a)<br><span class="experiment-evidence">Moreover, increasing the prefix injection probability leads to a consistent upward shift in the entropy trajectory.</span> |
| 无前缀的 vanilla GRPO 与使用 Gemma-2-2B 前缀的 Qwen2.5-7B 对照 | 前缀设置在早期表现出更高策略熵和更丰富的奖励模式，但平均奖励较低；作者将后者解释为探索成本。原文节选未明确报告对应数值。 | 该对照直接隔离了“是否引入异构弱模型轨迹”。它表明前缀不是无成本的数据增强，而是在训练难度、即时奖励和探索广度之间进行权衡。由于同时改变了输入上下文及轨迹分布，该对照尚不能完全区分收益来自异构模型、前缀内容本身，还是额外上下文扰动。 | 第 6.1 节，Figure 3(b)<br><span class="experiment-evidence">The lower average reward of prefix-guided models in Figure 3(b) can be interpreted as the cost of exploration.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出以弱模型生成的部分推理轨迹引导RLVR探索，从而缓解熵坍缩并扩大数学推理覆盖率。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`45aa8442d4fa6c3e66bb00d636af7b7972857db0b507f06b20f974c91b7e4bf7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
