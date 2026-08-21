---
title: "[论文解读] Beyond Imitation: Filtering On-Policy Distillation by Reasoning Progress"
description: "[arXiv 2608.19408][LLM Reasoning] 本文研究如何在面向推理的在策略蒸馏中识别并过滤与真实推理进展相冲突的教师监督信号，以减少教师模仿对有效推理路径的抑制。"
arxiv_id: "2608.19408"
announcement_date: "2026-08-21"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-21T02:04:24.455880+00:00"
source_sha256: "ac68384b0e348435d0d3eab3c6e6f4d6e72f6bcef8ed5dc26cb7bc2297c9eb63"
tags:
  - "LLM Reasoning"
  - "在线策略蒸馏"
  - "知识蒸馏"
  - "大语言模型推理"
  - "过程奖励"
  - "推理进展"
  - "奖励筛选"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.19408</p>

# Beyond Imitation: Filtering On-Policy Distillation by Reasoning Progress

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-21</span>
<span><strong>作者</strong> Chen Yang, Haiyuan Wan, Rengrong Xiong, Yize Chen, Danny H.K. Tsang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> The Hong Kong University of Science and Technology (Guangzhou)；Tsinghua University；Zhejiang University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.19408) · [PDF 下载](https://arxiv.org/pdf/2608.19408) · **关键词** 在线策略蒸馏, 知识蒸馏, 大语言模型推理, 过程奖励, 推理进展, 奖励筛选<br>


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

本文研究如何在面向推理的在策略蒸馏中识别并过滤与真实推理进展相冲突的教师监督信号，以减少教师模仿对有效推理路径的抑制。

**不用术语来说**：学生模型在训练时会生成自己的推理过程，教师模型随后指导它每一步应该怎样生成。问题在于，学生有时虽然没有完全模仿教师，却正在更接近正确答案；如果训练一律奖励教师相似性，就可能把这些有用但不同的思路当成错误方向。因此，本文试图判断哪些教师指导值得保留，哪些指导应当暂时忽略。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出面向推理进展的在策略蒸馏奖励过滤框架 $R^2$-OPD：用独立估计的过程奖励衡量中间推理片段对解题成功概率的贡献，并检测其与教师蒸馏信号之间的局部排序冲突，从而屏蔽不可靠的片段级蒸馏奖励。
- 设计符号一致的过程奖励片段合并与片段级散度聚合方法；作者声称这些设计能够减弱内部边界估计误差的抵消问题，并在弱相关条件下降低局部散度的方差。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型知识蒸馏与推理后训练交叉领域。知识蒸馏通过让能力较强的教师模型指导学生模型学习；传统自回归蒸馏通常使用教师生成的静态数据，但学生训练时看到的轨迹与实际推理时自行生成的轨迹不同，形成暴露偏差。在线策略蒸馏（On-Policy Distillation，OPD）改为使用学生模型生成的回答作为训练轨迹，并在这些学生实际到达的状态上查询教师模型，从而提供逐令牌的分布匹配信号。本文关注的具体问题是：教师分布相似度可以衡量学生是否模仿教师，却不一定能衡量某个推理片段是否提高了最终解题概率；因此，在推理任务中需要区分“适合蒸馏”与“促进推理进展”这两个并不等价的属性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**在线策略蒸馏（OPD）**

学生模型先按照自身当前策略生成推理轨迹，教师模型再在学生访问到的每个状态上提供令牌级分布监督。这样训练数据来自学生自己的行为，而不是固定的教师答案，可减小训练轨迹与推理轨迹之间的暴露偏差。

</div>
<div class="concept-item" markdown="1">

**逐令牌蒸馏奖励**

在每个生成位置，依据学生分布与教师分布的接近程度构造奖励或优化信号；学生越像教师，通常得到的蒸馏反馈越有利。该信号反映的是教师兼容性，而不是该推理步骤对最终正确答案的实际贡献。

</div>
<div class="concept-item" markdown="1">

**过程奖励与推理进展**

过程奖励评估中间推理状态对最终解题成功概率的影响，通常可从不同状态采样后续过程，并比较其成功率来估计某个推理片段的边际贡献。它提供了不依赖教师表面生成路径的参考，但有限次采样会带来蒙特卡洛噪声。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定教师模型、学生模型以及由学生模型生成的推理轨迹，轨迹由连续的推理片段组成。OPD原本对轨迹中的所有令牌使用教师派生的蒸馏信号；本文的设定是额外估计每个推理片段的过程奖励，并比较过程奖励所诱导的“推理进展排序”和教师分布差异所诱导的“蒸馏兼容性排序”。当一个推理进展更大的片段反而因偏离教师而受到更强惩罚时，系统将其视为局部排序冲突，并抑制该片段的蒸馏监督，而不是把过程奖励直接加入优化目标。输入是学生轨迹、教师在相应状态上的分布以及过程奖励估计；输出是经过筛选的片段级蒸馏信号，用于学生模型的策略优化。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D_{\mathrm{task}}$**

任务数据或推理问题分布；文中具体数据集符号原文未明确给出，此处用于概括任务实例的来源。

</div>
<div class="notation-item" markdown="1">

**$x$**

一个待解决的输入问题或任务实例。

</div>
<div class="notation-item" markdown="1">

**$\tau$**

学生模型针对输入问题生成的完整推理轨迹，由若干连续推理片段构成。

</div>
<div class="notation-item" markdown="1">

**$r_{\mathrm{prog}}$**

过程奖励，表示某个推理片段对解决任务的估计进展或边际贡献。

</div>

</div>

**直接相关的工作**

- **On-policy distillation（OPD）**: OPD为本文的基础训练框架：它使用学生生成轨迹并接受教师的逐令牌分布监督。本文指出其潜在缺陷是把教师相似度隐含地当作推理质量代理，并在此基础上用过程进展信息筛选冲突的蒸馏信号。
- **Setlur et al.（2025a），Rewarding progress: scaling automated process verifiers for LLM reasoning**: 该工作代表过程奖励方向，为根据中间状态评估推理进展提供相关思路。本文并非直接把过程奖励作为新的优化目标，而是将其作为独立参考，用来检测教师蒸馏排序与实际推理进展之间的不一致。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

知识蒸馏希望以较低成本把能力较强的教师模型传给学生模型；在自回归推理任务中，传统静态教师数据与学生实际生成轨迹不一致，而在策略蒸馏（OPD）让教师直接指导学生自己访问的状态，因而更适合进行推理能力迁移。实际需求是：在保留教师有效知识的同时，不要牺牲学生可能发现的替代性正确推理路径。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **静态教师数据上的传统知识蒸馏**：先由教师生成固定的输入—输出数据集，再用这些数据训练学生模仿教师行为。它主要依赖预先收集的教师轨迹，而不是学生训练过程中实际走到的状态。
- **基于教师分布匹配的在策略蒸馏（OPD）**：学生先生成回答，教师在学生实际到达的每个状态上提供下一词分布，训练目标通过逐词分布匹配或策略优化，让学生的生成行为接近教师，并为整个回答提供较密集的监督。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- OPD把教师相似性隐含地当作推理质量的替代指标，但学生生成的某个推理片段即使偏离教师轨迹，也可能提高最终答对的概率；若统一强化教师相似性，就会惩罚具有建设性的替代思路。
- 过程奖励与逐词教师散度不能简单直接相加：前者由有限次续写采样估计，包含蒙特卡洛噪声；后者会受局部词汇选择和教师不确定性影响。两种信号尺度不同且都较细粒度，直接融合可能产生不稳定或难以解释的训练信号。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有方法缺少一种不改变原有蒸馏目标、却能判断教师监督是否与真实推理进展一致的可靠性机制。具体而言，仍需利用教师无关的过程进展信号作为参照，在稳定的推理片段层面识别“进展更高但因偏离教师而受到更强惩罚”的局部冲突，并只过滤这些可疑监督。

</div>
<div markdown="1"><span>核心问题</span>

能否通过比较推理进展对不同推理片段的排序与教师散度对这些片段的排序，可靠地识别误导性的 OPD 奖励，并在不额外把过程奖励作为优化目标的情况下，通过选择性屏蔽冲突片段提升复杂推理性能？

</div>
<div markdown="1"><span>作者直觉</span>

如果一个推理片段确实更有助于解题，那么从该片段继续生成时，成功概率应相对提高；这可以作为不依赖教师轨迹的参考。若这种片段却因不够像教师而受到更强的蒸馏惩罚，说明教师相似性与功能性进展发生了局部不一致。将相邻且进展方向一致的片段合并后再比较排序，可以减少边界切分和逐词波动带来的噪声；只屏蔽发生冲突的监督，则能保留教师在大多数一致区域中的指导，而不强迫学生放弃有效的不同解题路线。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

R²-OPD（Reasoning-Progress-aware On-Policy Distillation）以学生模型自身生成的回答为训练轨迹，先在每个解码位置计算教师与学生之间的支持集近似反向 KL 监督，再把回答按自反思话语标记切分为连续推理片段。方法通过对各片段边界进行在线蒙特卡洛续写，估计每个中间状态最终解题成功的概率，并将相邻状态成功概率的增量定义为过程奖励；随后比较过程奖励与片段级 KL 损失的排序，识别“推理进步与教师监督不一致”的片段并进行选择性屏蔽，最后仅用保留下来的监督信号更新学生模型。直观地说，标准 OPD 模仿学生已经走过的整条路径，而 R²-OPD 试图判断每一段推理是否让答案更接近正确，再减少对可疑模仿信号的依赖。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 学生生成在策略轨迹与教师分布监督

学生按 $y\sim\pi_{S}(\cdot\mid x)$ 生成回答，并在每个上下文 $h_t=(x,y_{<t})$ 上计算教师和学生的词元分布。由于完整词表计算代价高，方法取学生概率最高的 $H$ 个词元构成支持集 $\mathcal{S}_t$，用归一化学生概率近似反向 KL 损失。

<div class="method-step__io" markdown="1">

**输入**：提示 $x$、学生策略 $\pi_{S}$、教师策略 $\pi_{T}$。<br>
**输出**：每个解码位置的支持集近似 KL 损失 $\ell_t^{\mathrm{KL},\mathcal{S}}$，以及对应的学生生成回答 $y$。

</div>

**直观理解**：学生先自己作答，教师不直接提供一条完整标准答案，而是在学生每一步选择时告诉它各个候选词的分布差异。只检查最有可能的少量候选词，相当于只比较当前真正有影响的选项。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 推理片段切分与边界状态构造

方法先匹配回答中的自反思话语标记，得到候选边界；只有当相邻已接受边界之间的文本至少包含 $S_{\min}$ 个句子时，才接受该边界，以避免连续标记造成过度切分。最终将回答划分为 $M$ 个连续片段 $\Sigma(y)=\{\sigma_1,\ldots,\sigma_M\}$，并构造边界状态 $p_m=(x,y_{1:b_m})$。

<div class="method-step__io" markdown="1">

**输入**：学生回答 $y=(y_1,\ldots,y_T)$、自反思话语标记词典 $\mathcal{T}$、最小句子数阈值 $S_{\min}$。<br>
**输出**：推理片段集合 $\Sigma(y)$、边界状态序列 $p_0,p_1,\ldots,p_M$，以及每个片段对应的片段级 KL 损失。

</div>

**直观理解**：切分点主要放在“因此”“重新检查”等表示思路转折或自我修正的位置，但还要求每段足够长。这样比较的是有一定推理内容的步骤，而不是把一句话或几个连续标记误当成独立步骤。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在线估计推理进步

对每个非终止边界，从前缀状态进行 $N_{\mathrm{eval}}$ 次学生在线续写，并用答案验证器判断每次续写是否正确，从而估计该中间状态最终解题成功的概率 $\hat S_m$。初始状态固定为零，终止状态直接复用原回答的正确性，因此不必为终止状态额外生成续写；过程奖励定义为相邻边界成功概率的差值 $PR_m=\hat S_m-\hat S_{m-1}$。

<div class="method-step__io" markdown="1">

**输入**：格式标准化的前缀状态 $\bar p_m$、答案提示 $\mathcal{I}_{\mathrm{ans}}$、学生模型、真实答案 $g$ 和可验证奖励函数 $\mathcal{R}$。<br>
**输出**：每个片段的过程奖励 $PR_m$，表示该片段使预计解题成功概率增加或减少的幅度；若回答不包含真实答案字符串或切分失败，则标记为 PR-unavailable。

</div>

**直观理解**：对每个中间步骤，模型从这里重新尝试若干次，看之后有多大比例能答对。若加入某一段后成功率上升，它就是有帮助的；若成功率下降，它可能引入了错误或偏离。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 冲突检测、片段屏蔽与 R²-OPD 更新

方法将相邻片段合并为符号一致的比较单元，以减少边界噪声；然后比较过程奖励排序与 KL 损失排序，寻找高过程奖励却不对应较小蒸馏损失，或低过程奖励却受到较强模仿监督的冲突单元。按设定比例屏蔽冲突片段的 KL 监督，PR-unavailable 轨迹则不筛除、直接保留，最后用剩余的支持集近似反向 KL 损失优化学生。

<div class="method-step__io" markdown="1">

**输入**：片段级过程奖励 $PR_m$、片段级 KL 损失、可用的过程信号，以及屏蔽比例 $q$。<br>
**输出**：经过选择性过滤的词元级蒸馏损失，以及更新后的学生模型。

</div>

**直观理解**：如果一段推理看起来确实让成功率提高，但教师监督却把它判得很不相似，或者相反，就说明“该不该模仿”和“像不像教师”发生冲突。方法不是删除整条回答，而是只弱化可疑片段，尽量保留有用的教师指导。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 支持集上的反向 KL 蒸馏目标

$$
\mathcal{L}_{\mathrm{OPD}}=\mathbb{E}_{x,\,y\sim\pi_S(\cdot\mid x)}\left[\frac{1}{T}\sum_{t=1}^{T}\ell_t^{\mathrm{KL}}\right],\qquad \ell_t^{\mathrm{KL}}=D_{\mathrm{KL}}\!\left(\pi_S(\cdot\mid h_t)\,\|\,\pi_T(\cdot\mid h_t)\right)=\sum_{v\in\mathcal{V}}\pi_S(v\mid h_t)\log\frac{\pi_S(v\mid h_t)}{\pi_T(v\mid h_t)}
$$

**符号说明**

- $\mathcal{L}_{\mathrm{OPD}}$：整个回答上的 OPD 训练损失。
- $x$：输入提示或数学问题。
- $y=(y_1,\ldots,y_T)$：学生生成的长度为 $T$ 的回答。
- $\pi_S$：学生模型的词元生成策略。
- $\pi_T$：教师模型的词元生成策略。
- $h_t=(x,y_{<t})$：第 $t$ 个词元生成前的解码上下文。
- $\ell_t^{\mathrm{KL}}$：第 $t$ 个位置的学生到教师反向 KL 损失。
- $\mathcal{V}$：完整词表。
- $v$：词表中的候选词元。

<div class="equation-explanation" markdown="1">

**直观理解**：学生先自己生成整条轨迹，再在每个位置让自己的词元分布靠近教师分布。R²-OPD 的额外步骤不是替换这个基本目标，而是判断哪些位置或片段的监督与实际推理进展冲突，并选择性地移除这些损失项。<br>
**原文位置**：Preliminaries，式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 过程奖励：解题成功概率的增量

$$
PR_m\triangleq\hat{S}_m-\hat{S}_{m-1},\qquad m=1,\ldots,M
$$

**符号说明**

- $PR_m$：第 $m$ 个推理片段的过程奖励。
- $\hat{S}_m$：在第 $m$ 个边界状态之后，通过在线续写估计的最终解题成功概率；终止状态使用原回答的可验证正确性。
- $m$：推理片段或边界状态的索引。
- $M$：回答被切分出的推理片段总数。

<div class="equation-explanation" markdown="1">

**直观理解**：该式只看成功概率的变化，而不是只看某个状态本身的分数。若 $PR_m>0$，说明第 $m$ 段让后续答对的可能性提高；若 $PR_m<0$，说明它可能使推理偏离正确方向。<br>
**原文位置**：Process Reward Estimation，式（6）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：学生在自身生成的轨迹上优化支持集近似的反向 KL 损失，但 R²-OPD 先依据过程奖励与片段级 KL 损失的排序关系筛除冲突监督。其核心原则是保留与推理进展相容的教师分布指导，降低对错误、退化或可能导致未完成推理的模仿信号；对于过程奖励不可用的轨迹，采用不筛选的回退规则，因此不会因缺少显式过程信号而额外惩罚轨迹。优化目标仍服务于学生参数更新，而过程奖励估计和冲突检测只承担训练数据或损失掩码筛选作用。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 支持集近似反向 KL 蒸馏**

标准 OPD 在学生生成的上下文上最小化 $D_{\mathrm{KL}}(\pi_S(\cdot\mid h_t)\|\pi_T(\cdot\mid h_t))$。实现中只使用支持集 $\mathcal{S}_t$，并以 $w_{t,v}$ 对学生概率重新归一化后计算 $\ell_t^{\mathrm{KL},\mathcal{S}}$，从而避免遍历完整词表，同时保持反向 KL 对学生高概率区域的关注。

> 直观理解：反向 KL 会重点关注学生自己认为可能的词，因此适合在学生实际走过的轨迹上纠正其分布。支持集近似是在计算成本和监督覆盖之间做折中。

**2. 基于在线续写的过程奖励估计**

方法不依赖人工逐步标注，而是从每个中间前缀进行多次学生续写，并用可验证答案奖励估计状态的 solve probability。过程奖励不是某一步的绝对正确性，而是连续边界状态之间成功概率的增量，因此能够表达改进、退化和错误恢复。

> 直观理解：最终答对只能说明整条路的终点正确，不能说明哪一步有贡献。反复从中途继续作答，可以近似判断每个中间状态“还有多大希望答对”。

**3. PR–KL 冲突过滤与符号一致合并**

方法以过程奖励和片段级 KL 损失的相对排序为依据进行冲突检测，并先合并过程奖励符号一致的相邻片段，以提高比较单元的稳定性。仅对成功切分且包含真实答案的轨迹应用过滤；缺少过程信号时采用不惩罚的回退策略。

> 直观理解：单个短片段的成功率估计可能很嘈杂，先把方向相同的相邻片段合在一起能减少误判。无法可靠估计进步时，方法选择不做过滤，而不是武断地删除监督。

**训练与推理**

训练阶段，学生从训练问题中在线生成回答；教师在相同学生上下文上提供词元分布；系统切分回答、从各边界进行学生续写、用真实答案验证续写并计算 $\hat S_m$ 与 $PR_m$，再完成符号一致合并、PR–KL 冲突检测和片段屏蔽，最后用保留的 KL 损失更新学生。推理阶段不需要教师、在线蒙特卡洛续写或过程过滤，直接使用训练后的学生模型生成答案；论文评测时对每个问题采样多条回答，并用任务答案验证器计算准确性。

**复现信息**

主要训练配置为：使用去重后的 DAPO-Math-17K，训练一个 epoch，优化器为 AdamW，学习率为 $5\times10^{-6}$，全局批大小为 $64$，最大提示长度为 $1{,}024$ 个词元，最大回答长度为 $7{,}168$ 个词元。KL 支持集取学生每步概率最高的 $16$ 个词元，即 $H=16$；过程奖励估计每个边界进行 $N_{\mathrm{eval}}=8$ 次在线续写，采样温度为 $0.7$、$\mathrm{top}$-$k=50$、$\mathrm{top}$-$p=1.0$、最大续写长度为 $300$ 个词元；边界最小句子数为 $S_{\min}=3$，冲突检测的最小片段相关阈值为 $n_{\min}=3$，片段级屏蔽比例为 $q=30\%$。这些设置来自 Experimental Setup 和 Appendix B.1；文中未在所给章节完整展开冲突检测的全部伪代码细节，因此实际复现仍需核对 Appendix B。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 原文未明确报告实验数据集、数据规模、训练集与测试集划分及各自用途。文中参考文献提到 OlympiadBench，但该条目属于相关工作引用，不能据此认定本文使用了该数据集。
- 原文未明确报告用于训练或评估的数学推理、通用推理或其他任务数据集。
- 原文未明确报告数据预处理、采样策略或验证集设置。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**原文未明确报告**

未提供任何评价指标的名称、计算方式或适用任务。 （原文未明确报告）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告本文实际比较的基线方法。参考文献包含 on-policy distillation、process reward model 和强化学习相关工作，但这些引用不能替代实验基线。
- 原文未明确报告普通行为克隆、标准 on-policy distillation 或其他无筛选蒸馏方法是否作为对照。
- 原文未明确报告基于过程奖励、步骤验证或其他 reasoning-progress 信号的方法是否作为对照。
- 原文未明确报告模型规模、教师模型、学生模型及其训练配置，因此无法判断比较是否公平。

**实验想回答的问题**

- 原文所提供的实验章节仅包含“Experimental Setup”标题及参考文献条目，未提供可据以重建的具体研究问题。
- 原文未明确报告数据集、基线、评价指标、实验结果或消融设计，因此无法判断该方法是否优于现有方法，以及“reasoning progress”筛选机制的独立贡献。

**实验实现**

原文仅显示“Experiments”及“Experimental Setup”标题，并列出若干参考文献；没有提供实验协议、模型配置、训练步数、采样温度、筛选阈值、随机种子、评估流程或统计显著性信息。因此，无法从所给材料复现实验，也无法核验不同方法是否在相同数据和计算预算下比较。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The method filters on-policy distillation data according to reasoning progress, making language-model reasoning the central contribution.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`ac68384b0e348435d0d3eab3c6e6f4d6e72f6bcef8ed5dc26cb7bc2297c9eb63`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
