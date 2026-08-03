---
title: "[论文解读] ThinkReset: Learnable Intermediate Interface Construction for Bounded-Context Long-Horizon Reasoning"
description: "[arXiv 2607.28642][LLM Reasoning] 本文将固定上下文窗口中的长程推理重新界定为“可复用中间接口”的学习问题：模型应学习一种能够替代冗长历史并支持后续求解的文本状态，而非仅压缩或调度原有推理轨迹。"
arxiv_id: "2607.28642"
announcement_date: "2026-08-03"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-03T02:16:03.145496+00:00"
source_sha256: "41726810d3907a45b1685e1d89d1b7fcf8ef8fac738a8db5eebf97e73a294ede"
tags:
  - "LLM Reasoning"
  - "长程推理"
  - "有界上下文窗口"
  - "中间接口学习"
  - "思维链"
  - "上下文重置"
  - "文本状态写回"
  - "继续求解"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2607.28642</p>

# ThinkReset: Learnable Intermediate Interface Construction for Bounded-Context Long-Horizon Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-03</span>
<span><strong>作者</strong> Fei Ding, Yongkang Zhang, Runhao Liu, Yuhao Liao, Zijian Zeng</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Alibaba Group；Tsinghua University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.28642) · [PDF 下载](https://arxiv.org/pdf/2607.28642) · **关键词** 长程推理, 有界上下文窗口, 中间接口学习, 思维链, 上下文重置, 文本状态写回, 继续求解<br>


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

本文将固定上下文窗口中的长程推理重新界定为“可复用中间接口”的学习问题：模型应学习一种能够替代冗长历史并支持后续求解的文本状态，而非仅压缩或调度原有推理轨迹。

**不用术语来说**：模型解决复杂数学或逻辑问题时，推理文字会不断增长；一旦接近上下文容量上限，早期内容可能被截断，冗余信息和错误假设也会持续干扰后续判断。更关键的是，只按最终答案奖励模型，会促使尚未完成推理的模型在空间将尽时仓促猜答案。本文关注如何让模型在适当时刻写下一份足以继续解题的“交接记录”，用它替换此前的长篇过程，然后在清空出的上下文空间中继续认真推理。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出问题重构：固定上下文下的长程推理不应主要视为轨迹保留、压缩或调度问题，而应视为中间接口学习问题；冗余累积、错误假设锚定与上下文溢出可统一理解为模型缺少构造和复用有效接口的能力。
- 提出 ThinkReset 这一文本空间实现：达到上下文使用阈值时写回中间接口并重置此前轨迹，将重置后的继续求解成功作为直接优化目标，而不是依赖逐词重构、长度惩罚等间接代理目标。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究固定上下文窗口下的大语言模型长程推理。长思维链能够把复杂问题拆成连续步骤，但自回归历史会随推理不断增长，进而带来三类相互关联的困难：重复内容占用窗口、错误假设长期滞留并影响后续判断，以及任务尚未完成时上下文已耗尽。既有方法通常把完整或部分推理轨迹作为核心对象，通过剪枝、压缩、重编码或运行时调度延长其可用时间；本文则将核心问题重新表述为“中间接口学习”：模型需要生成一段可替代旧历史的文本状态，使后续推理即使看不到原始长轨迹，仍能从该状态继续求解。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**思维链推理**

模型在给出最终答案前，以文本形式逐步展开分析过程。较长的思维链可能支持复杂推导，但会持续消耗有限的上下文空间。

</div>
<div class="concept-item" markdown="1">

**有界上下文窗口**

模型在一次生成中能够读取和保留的文本长度存在固定上限；问题描述、既有推理和新生成内容共同占用这一容量。窗口接近耗尽时，未完成的求解过程可能被截断，或迫使模型仓促作答。

</div>
<div class="concept-item" markdown="1">

**可复用中间接口**

它是模型根据当前求解进度写出的新文本状态，用来替换此前较长的推理历史，并作为后续推理的入口。其质量不以逐字复现旧轨迹衡量，而以重置后是否仍能支持继续求解衡量。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个需要较长推理过程才能完成的问题，模型在固定上下文窗口内自回归地产生推理文本与最终答案。随着窗口使用量达到某个阈值，系统不再无限保留既有轨迹，而是主动写回一个文本形式的中间接口，以该接口替换此前的长历史并重置上下文，然后继续推理。期望输出仍是正确的最终答案；关键学习目标则是让重置后的状态保留足够的任务信息、已取得的有效进展和后续行动依据，从而提高继续求解的成功率。该设定聚焦单条推理轨迹内部的状态重置，不涉及多轮对话管理、工具调用、额外潜变量模块或执行引擎改造。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **TokenSkip（Xia et al., 2025）**: 代表轨迹压缩与长度控制路线，通过选择性保留或跳过轨迹内容缓解上下文限制。按本文的分类，它仍以原推理轨迹为主要保留对象；ThinkReset关注的则是学习一段能够替代历史并支持后续求解的新接口。
- **ReSum（Wu et al., 2026）**: 代表运行时上下文刷新与状态管理路线，主要面向多轮交互、搜索或外部记忆，将增长的历史转换为阶段性状态。ThinkReset与其思想接近，但范围更窄：它专门处理单次推理轨迹内的固定窗口重置，并直接以重置后的继续求解成功为训练目标。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

长思维链虽然能提升复杂任务表现，但固定上下文窗口无法无限容纳推理历史。随着轨迹增长，重复内容会占用容量，错误假设会长期留在上下文中并形成锚定，尚未完成的求解过程还可能因窗口耗尽而被迫截断。因此，系统需要一种在有限容量内保存“下一阶段真正需要的信息”并持续求解的机制。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **推理轨迹压缩、剪枝与保留**：把不断增长的自回归推理轨迹作为核心对象，通过缩短、删减或选择性保留历史内容，减少上下文占用，同时尽量维持原有推理信息。
- **测试时轨迹控制与结果奖励驱动的长链强化学习**：前者在推理期间调度或干预轨迹长度和生成过程；后者主要根据最终答案是否正确提供奖励，以此训练模型生成能够到达正确答案的长推理链。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 轨迹中心方法仍假定后续推理依附于原有历史，只关注如何更短地保存或更好地调度轨迹；局部重构忠实度和长度等指标不能保证压缩后的状态保留了继续解题所需的能力，错误假设也可能随摘要或保留内容继续传播。
- 仅依赖最终答案奖励时，训练目标没有显式评价模型在中途是否留下了可继续求解的状态。当窗口接近耗尽而任务尚未解决时，剩余生成空间缩小，奖励压力可能推动模型放弃细致推理并提前猜测答案，形成固定上下文约束与训练目标之间的结构性错配。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种把中间状态本身作为显式、可训练对象的框架：该状态不仅要比完整历史短，还必须能够替代被丢弃的历史，并以重置后能否继续推进直至成功求解来评价。换言之，尚未解决的是“可续解性”而非单纯“压缩率”或“对原轨迹的复现度”。

</div>
<div markdown="1"><span>核心问题</span>

在固定上下文窗口内，能否学习何时将既有推理写回为一个新的文本中间接口，并让该接口包含足够的任务状态，使模型删除此前长轨迹后仍能稳定继续求解？进一步地，能否通过直接优化重置后的继续求解成功，使这种接口优于仅压缩、剪枝或调度原轨迹的方案？

</div>
<div markdown="1"><span>作者直觉</span>

可以把长程推理类比为多人分班次处理复杂任务：下一班不需要逐字阅读上一班的全部工作日志，而需要一份准确的交接记录，其中包含已确认结论、仍待解决的问题、有效进展以及应避免的错误方向。若训练直接奖励“接班后能否把问题解决”，模型就会倾向于写出对未来行动有用的接口；替换旧日志还能释放上下文容量，并减弱冗余和早期错误对后续推理的持续影响。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ThinkReset将固定上下文窗口下的长程推理建模为“可复用中间接口学习”，而不是轨迹压缩或摘要生成。给定问题$x$、容量为$C$的上下文窗口和已生成的推理轨迹$r_{1:i}$，当上下文使用量达到$\alpha C$时，系统追加触发提示$p_{\mathrm{trig}}$，由模型写出自然语言状态$s$；随后彻底移除原推理历史，只保留$x\oplus s$作为新上下文继续求解。接口$s$的质量不按它与旧轨迹的相似度、长度或信息复述完整度衡量，而按删除历史后从$x\oplus s$出发的8次独立续推中有多少次得到正确答案$a^\star$衡量。

训练分为三个阶段：先用500个人工设计样本对首次重置后的写回片段进行监督微调，再在接近窗口上限但仍未正确完成的困难轨迹上，以留一法策略优化（RLOO）直接提升首次接口的后续求解成功率；若某个首次接口对应的8次续推全部失败，则继续推理至下一次阈值并训练第二个接口。直观地说，方法不是设法把整本“推理草稿”塞回有限窗口，而是要求模型写一张足以接着工作的“交接单”：旧草稿可以丢弃，但关键中间结论、约束和未完成任务必须让后续推理能够真正接手。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 困难长轨迹筛选与重置位置构造

保留上下文使用量超过$\alpha C$且最终答案错误的轨迹，并在$\alpha C$处截断；为避免语义断裂，截断后删除未完成句子，构造前缀$h_{i,g}=(x,r_{1:i}^{(g)},p_{\mathrm{trig}})$。若保留数$G<2$，该题不进入第二阶段的RLOO更新。

<div class="method-step__io" markdown="1">

**输入**：问题$x$以及基础策略为每题采样的$G'=16$条完整轨迹。<br>
**输出**：一组确实需要历史替代接口的困难前缀$\{h_{i,g}\}_{g=1}^{G}$。

</div>

**直观理解**：只训练那些“窗口快用完、题还没做对”的案例，因为它们最能暴露接口是否有用；容易题无需重置，已经做对的长轨迹也可能诱导模型把接近完整的答案直接塞进接口。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自然语言接口写回与历史替换

策略从$\pi_\theta(\cdot\mid h_{i,g})$采样写回状态$s_g$，随后删除$r_{1:i}^{(g)}$与触发前历史，将有效上下文替换为$x\oplus s_g$；$s_g$是无外部结构槽位的自然语言文本。

<div class="method-step__io" markdown="1">

**输入**：重置前缀$h_{i,g}$，其中包含原题$x$、截至触发点的推理$r_{1:i}^{(g)}$和提示$p_{\mathrm{trig}}$。<br>
**输出**：不依赖原始轨迹、可作为后续求解新入口的上下文$x\oplus s_g$。

</div>

**直观理解**：模型必须把“以后还要用什么”写出来，而不是复述“刚才做过什么”；替换后旧草稿不可再访问，因此无用摘要无法靠回看历史补救。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 续推成功评估与首次接口强化学习

从$x\oplus s_g$独立采样8次续推，以正确续推比例${R_{\mathrm{succ8}}}_g$作为接口奖励；RLOO用同组其余$G-1$个接口的平均奖励作为基线，只对生成$s_g$的写回片段施加策略梯度。

<div class="method-step__io" markdown="1">

**输入**：每个替换后的上下文$x\oplus s_g$以及标准答案$a^\star$。<br>
**输出**：更倾向生成高续推成功率接口的更新后策略$\pi_\theta$。

</div>

**直观理解**：同一道题上多个候选交接单彼此比较，优于同组平均水平的写法被增强，较差写法被抑制；这样优化的是“接手后能否做完”，而非接口是否短或是否像摘要。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 失败样本的第二重置与层级接口训练

允许模型从首次接口继续推理，直至上下文再次达到$\alpha C$，再生成第二个写回状态并用同一续推成功奖励训练；当前系统每条轨迹最多执行两次重置。

<div class="method-step__io" markdown="1">

**输入**：首次写回后8次独立续推全部失败的样本。<br>
**输出**：能够在更长求解跨度中依次构造两个中间接口的策略。

</div>

**直观理解**：第一张交接单不足以完成极难问题时，模型继续工作并再写一张新的交接单；这相当于把超长任务分成多个可独立接续的阶段，而不是要求一次写回覆盖全部未来。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 八次独立续推成功奖励

$$
R_{\mathrm{succ8}}=\frac{1}{8}\sum_{m=1}^{8}\mathbf{1}\!\left[\pi_{\theta}(x\oplus s\leadsto a^{\star})_{m}\right]
$$

**符号说明**

- $R_{\mathrm{succ8}}$：从写回接口继续求解时，8次独立续推的正确比例，也是接口的样本级奖励。
- $x$：原始待求解问题。
- $s$：模型在触发点生成、用于替代已删除历史的自然语言中间接口。
- $\oplus$：文本上下文拼接操作，即把原问题与写回状态组成新的输入。
- $\pi_{\theta}$：参数为θ的生成策略。
- $a^{\star}$：问题的标准正确答案。
- $m$：8次相互独立续推中的第m次。
- $\mathbf{1}[\cdot]$：指示函数；括号内事件成立取1，否则取0。
- $\leadsto$：表示策略从给定上下文继续生成并最终到达某答案。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把接口质量定义为“删掉旧历史后还能做对多少次”。例如8次续推中有6次得到标准答案，则奖励为$6/8$；因此训练不会直接奖励复述完整、写得短或措辞相似，而只奖励接口对后续求解的实际支持。<br>
**原文位置**：第3.2节，公式(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 首次重置阶段的RLOO策略梯度

$$
\hat{g}_{\mathrm{RLOO}}=\frac{1}{G}\sum_{g=1}^{G}\left({R_{\mathrm{succ8}}}_{g}-\frac{1}{G-1}\sum_{g^{\prime}\neq g}{R_{\mathrm{succ8}}}_{g^{\prime}}\right)\nabla_{\theta}\log\pi_{\theta}(s_{g}\mid h_{i,g})
$$

**符号说明**

- $\hat{g}_{\mathrm{RLOO}}$：RLOO给出的策略梯度估计量。
- $G$：同一问题中通过困难轨迹筛选、实际参与更新的候选轨迹数；若小于2则跳过更新。
- $g$：当前候选轨迹或其写回状态的索引。
- $g^{\prime}$：除当前候选g外的其他候选索引。
- ${R_{\mathrm{succ8}}}_{g}$：第g个写回状态对应的8次续推成功比例。
- $h_{i,g}$：第g条轨迹在首次重置前的条件前缀，由问题、截至触发点的推理和触发提示组成。
- $s_g$：策略根据第g个前缀生成的首次写回状态。
- $\nabla_{\theta}\log\pi_{\theta}(s_g\mid h_{i,g})$：写回状态对数概率关于策略参数θ的梯度；实际梯度只作用于写回片段。

<div class="equation-explanation" markdown="1">

**直观理解**：括号内是第$g$个接口相对同题其他接口平均奖励的“留一优势”：高于其他候选平均值时提高该写法的概率，低于平均值时降低其概率。用同题候选作基线可以减少题目难度造成的奖励波动，使更新更聚焦于不同接口内容的相对效用。<br>
**原文位置**：第3.3节Stage 2，公式(3)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：总体目标是在每条轨迹峰值有效上下文满足$M(\tau)\leq C$的约束下，最大化增强策略$\pi_\theta^+$所产生轨迹的期望续推奖励$\mathbb{E}_{\tau\sim\pi_\theta^+}[R_{\mathrm{succ8}}(\tau)]$。这里的关键不是保持$s$与被删除轨迹$r_{1:i}$之间的局部忠实度，而是让$s$接替历史原本承担的计算角色；因此论文明确不把长度惩罚、预设“信息完整性”或摘要相似度作为主目标。

阶段1仅对写回片段做监督学习，为稀疏、延迟的续推奖励提供稳定初始化。阶段2用公式(3)优化首次写回：每题先采样$G'=16$条轨迹，只保留超过$\alpha C$且答错者，并用公式(2)评价每个$s_g$；正确且较短的样本无需接口，而超过阈值后仍正确的长样本也被排除，因为它们可能促使模型把几乎完整的解答塞进$s$，使接口退化为轨迹保留。阶段3对首次写回后8次续推全败者复用同一奖励训练第二接口，从而把单次接口学习扩展为层级接口学习。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 固定比例触发与文本空间写回**

当上下文占用达到$\alpha C$时插入$p_{\mathrm{trig}}$，提示模型“写回支持继续求解、仅保留未来进展所需信息的中间状态”。写回$s$紧接提示生成，直到模型停止该片段或达到上下文限制；它没有结构化字段、外部存储或专用状态对象。

> 直观理解：触发器只决定何时交接，写回接口决定交接什么。论文刻意采用简单固定阈值，以把研究重点放在接口内容学习上；作者称语义触发因缺少稳健判据，容易造成过早或反复写回。

**2. 基于8次续推的接口效用评估**

对每个$s_g$删除原历史后，从$x\oplus s_g$独立生成8条续推，并以到达$a^\star$的比例作为${R_{\mathrm{succ8}}}_g$。该信号同时用于首次与第二次重置训练，并与主要评测采用的Avg@8形式对齐。

> 直观理解：一个接口偶然支持一次正确续推并不稳定，重复8次可以近似衡量它作为新起点的可靠性。奖励不要求接口像原轨迹，因此模型可以舍弃无关过程，只保留真正影响后续求解的信息。

**3. 三阶段接口学习**

阶段1用500个可在重置后继续求解的人工样本，只监督首次重置后的写回段；阶段2在困难轨迹上通过RLOO优化首次接口；阶段3仅处理首次接口的8次续推全部失败者，并训练第二次写回。

> 直观理解：少量监督学习先教会模型写出基本可用的交接单，避免稀疏奖励下生成空文本或模糊改写；强化学习再按真实接续效果改进，而第二重置专门覆盖一次交接仍不够的长任务。

**训练与推理**

训练时，第一阶段收集500个人工设计的可接续写回案例，只监督首次重置后的$s$，目标是避免直接强化学习在稀疏奖励下坍缩为空写回、泛泛改写或无效复述。第二阶段对每题采样最多16条原始轨迹，筛出在$\alpha C$附近仍未完成且最终错误的样本；截断并清理未完成句后生成$s_g$，删除旧历史，从$x\oplus s_g$独立续推8次，再以组内留一基线执行RLOO。第三阶段只接收${R_{\mathrm{succ8}}}_g=0$的首次接口样本，让其继续推理到下一阈值并训练第二写回；最坏情况下，第二阶段每题最多有$16\times8=128$条首次接口续推，但第三阶段只处理其中完全失败的子集。

推理时，模型从$x$正常生成推理轨迹；占用达到$\alpha C$后追加$p_{\mathrm{trig}}$并生成$s$，然后以$x\oplus s$替代此前上下文。若后续推理再次达到阈值，可再执行一次相同操作，因此当前实现的重置次数属于$\{0,1,2\}$；不需要重置即可完成的问题保持普通推理路径。该流程始终使用固定窗口，而非外接检索记忆或扩大上下文，因此$s$必须在文本空间中显式携带后续真正需要的中间结论、约束、进度和待办信息。

**复现信息**

所有任务、模型和基线统一使用$C=32\mathrm{k}$上下文窗口；主实验采用Temperature$=0.6$、TopP$=0.95$、TopK$=20$和MinP$=0$，基础模型包括Qwen3-8B、Qwen3-14B与Qwen3-32B。写回接口$s$是触发提示后直接生成的自然语言片段，不引入结构化槽位或外部状态；其终止条件是模型主动停止该片段，或达到上下文限制后被截断。

固定比例$\alpha$是超参数，正文敏感性实验将$\alpha=3/4$作为较稳定选择，但方法核心不依赖语义边界检测。公平性上，ThinkReset与“固定比例触发+自由写回”共享相同的$p_{\mathrm{trig}}$、写回停止规则、窗口限制和解码参数，区别仅在于$s$是否经过重置条件下的强化学习；训练奖励与评测均使用8次续推平均成功形式。阶段2最多允许一次重置，阶段3只为首次接口全败样本增加第二次重置，评测时每条轨迹同样最多重置两次。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- DeepMath-103K：去污染后的数学推理训练集，用于训练 Qwen3-8B、Qwen3-14B 和 Qwen3-32B；原文未明确报告本文实际使用的样本数、训练划分比例及去污染流程。
- AIME 2024 与 AIME 2025：高难度竞赛数学评测，主要检验固定上下文下的多阶段推导与误差累积；ZebraLogic 与 AutoLogi：长链逻辑推理评测，检验中间状态能否保留后续求解所需的约束。原文未明确报告各评测集在本文中的题目数或具体划分。
- GPQA-Diamond：跨领域高难度问答评测，用于检查中间接口学习的收益是否局限于数学和逻辑任务；它是跨领域补充证据，而非主要训练域。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Avg@8**

从写回状态出发进行 8 次相互独立的续解，并对其正确率取平均；该指标直接衡量原推理历史被替换后，中间接口支持继续求解的能力。结果再对 5 个随机种子报告均值与 $95\%$ bootstrap 置信区间。 （越高越好，因为更高的 Avg@8 表示同一中间接口在多次续解中更稳定地保留了完成任务所需的信息，而不是偶然产生一次正确答案。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3-14B，在 AIME 2024、AIME 2025、ZebraLogic、AutoLogi 和 GPQA-Diamond 上进行固定 $32\mathrm{k}$ 窗口评测。

<div class="result-value" markdown="1">

ThinkReset 的 Avg@8 依次为 $83.9\pm0.6$、$75.8\pm0.7$、$95.2\pm0.5$、$93.7\pm0.5$ 和 $68.9\pm0.8$。相较原始 Qwen3-14B，绝对提升分别为 $4.6$、$5.4$、$6.7$、$4.5$ 和 $4.9$ 个百分点；五项均有提升。

</div>

作者结果表明，学习后的写回接口在数学、逻辑以及跨领域问答上都能提高历史被替换后的续解成功率，而非只对某一个基准有效。分析上，这支持接口具有一定任务迁移性；但它不能单独证明模型掌握了更强的一般推理能力，因为指标专门面向 8 次重置后续解，且训练数据主要来自数学领域。

<div class="result-source" markdown="1">

来源：Appendix C, Table 4, ThinkReset row

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ThinkReset 83.9 ± 0.6 75.8 ± 0.7 95.2 ± 0.5 93.7 ± 0.5 68.9 ± 0.8

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3-32B，在与主实验相同的五项评测和固定 $32\mathrm{k}$ 窗口下测试模型规模扩大后的效果。

<div class="result-value" markdown="1">

ThinkReset 的 Avg@8 依次达到 $86.1\pm0.5$、$77.3\pm0.6$、$95.4\pm0.5$、$92.9\pm0.6$ 和 $72.6\pm0.8$。相较原始 Qwen3-32B，绝对提升分别为 $4.7$、$4.4$、$6.6$、$5.6$ 和 $4.2$ 个百分点。

</div>

收益在 32B 模型上仍覆盖全部五项任务，说明方法并非只修补较小模型的容量不足。需要注意的是，AutoLogi 上的 ThinkReset 分数低于其 14B 版本，因此结果并不支持“扩大模型后每个任务都会单调提升”；更稳妥的结论是接口训练的相对收益能够延续到更大骨干模型。

<div class="result-source" markdown="1">

来源：Appendix D, Table 5, ThinkReset row

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ThinkReset 86.1 ± 0.5 77.3 ± 0.6 95.4 ± 0.5 92.9 ± 0.6 72.6 ± 0.8

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 将 ThinkReset 与各规模下最强的轨迹保留或测试时重置基线比较，并考察跨领域 GPQA-Diamond。

<div class="result-value" markdown="1">

在 14B 模型上，ThinkReset 的 GPQA-Diamond 为 $68.9\pm0.8$，高于最佳基线的 $66.2\pm1.0$，提升 $2.7$ 个百分点；在 32B 模型上为 $72.6\pm0.8$，高于 Halo 的 $70.3\pm0.9$，提升 $2.3$ 个百分点。原文进一步声称相对基线的改进在配对 bootstrap 检验下满足 $p<0.01$。

</div>

GPQA-Diamond 并非主要数学或逻辑证据，因此该结果用于检查收益是否能跨到不同知识问答域。它支持“可续解接口优于仅保留或动态刷新轨迹”的作者主张，但不能证明对所有领域均可泛化，因为这里只报告了一个跨领域基准。

<div class="result-source" markdown="1">

来源：Appendix C, Table 4 caption; Appendix D, Table 5 caption

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Improvements over baselines are statistically significant under paired bootstrap tests (p<0.01).

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

- Qwen3 原始基座模型：不引入专门的写回与重置训练，用于衡量 ThinkReset 相对常规固定窗口推理的净收益。
- Fixed-ratio trigger + free writeback：与 ThinkReset 使用相同触发提示、写回停止规则、上下文限制和解码参数，但写回状态不接受重置条件强化学习优化；因此它是最直接的接口学习对照。
- Length-penalized RLOO 与 TokenSkip：前者通过长度代理奖励训练更短轨迹，后者进行轨迹压缩且带额外 SFT；二者用于检验“减少文本或保留压缩轨迹”是否足以代替可续解接口。
- Halo：依据注意力熵和阈值控制器在测试时执行语义重写与轨迹重新初始化，用于比较动态测试时干预与训练得到的文本空间接口。

**实验想回答的问题**

- 在统一的 $32\mathrm{k}$ 上下文窗口内，ThinkReset 能否通过“写回中间状态—清除原历史—继续推理”提高重置后的续解成功率？
- 性能提升是否确实来自经过训练的可复用中间接口，而不是普通轨迹保留、自由文本写回、长度压缩或仅在测试时触发重置？

**实验实现**

实验使用 Qwen3-8B、Qwen3-14B 和 Qwen3-32B，统一采用 $C=32\mathrm{k}$ 的上下文窗口。训练分为冷启动 SFT、首次重置后的 RLOO，以及仅针对首次重置后 8 次续解全部失败样本的第二次重置训练；单条轨迹最多重置两次。训练奖励和评测均基于 8 次续解的平均成功率，以减少训练目标与 Avg@8 之间的不一致。主表解码参数为 Temperature=0.6、TopP=0.95、TopK=20、MinP=0。各方法使用相同解码设置和 Avg@8 协议，Length-penalized RLOO、TokenSkip 与 ThinkReset 具有相同 GPU 时间预算。写回状态是自然语言文本，不依赖结构化槽位或外部存储；其提示要求仅保留未来推进所必需的信息。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 14B 接口学习隔离实验：ThinkReset 对比 Fixed-ratio trigger + free writeback；两者共享触发提示、停止规则、窗口和解码参数，核心差异是写回状态是否接受重置条件强化学习。 | free-writeback 在五项任务上的 Avg@8 为 $81.9\pm0.8$、$72.3\pm0.9$、$91.5\pm0.7$、$92.1\pm0.7$、$66.2\pm1.0$；ThinkReset 分别提高到 $83.9\pm0.6$、$75.8\pm0.7$、$95.2\pm0.5$、$93.7\pm0.5$、$68.9\pm0.8$，即提升 $2.0$、$3.5$、$3.7$、$1.6$ 和 $2.7$ 个百分点。 | 该对照主要隔离“是否学习接口”这一因素：触发写回本身已经带来部分收益，但进一步按重置后续解成功率训练写回文本，会在全部任务上继续提高性能。因此数据更符合“内容的可续解性是关键”，而不是“只要清空上下文并生成一段摘要就够了”。不过这仍是方法级对照，不是逐组件移除的标准消融。 | Appendix C, Table 4, Fixed-ratio trigger + free writeback row; comparison target is the ThinkReset row in the same table<br><span class="experiment-evidence">Fixed-ratio trigger + free writeback 81.9 ± 0.8 72.3 ± 0.9 91.5 ± 0.7 92.1 ± 0.7 66.2 ± 1.0</span> |
| 32B 训练式接口对比测试时动态控制：ThinkReset 对比 Halo，二者使用相同骨干和固定窗口，但 Halo 根据注意力熵在测试时触发语义重写，ThinkReset 则训练自然语言接口。 | Halo 在五项任务上的 Avg@8 为 $83.1\pm0.7$、$75.2\pm0.8$、$92.2\pm0.6$、$91.9\pm0.7$、$70.3\pm0.9$；ThinkReset 为 $86.1\pm0.5$、$77.3\pm0.6$、$95.4\pm0.5$、$92.9\pm0.6$、$72.6\pm0.8$，对应提升 $3.0$、$2.1$、$3.2$、$1.0$ 和 $2.3$ 个百分点。 | 这一比较隔离的是“何时重置并重写”与“写出什么状态才能继续求解”的差异。Halo 表明动态检测不稳定并刷新轨迹本身有效，而 ThinkReset 的进一步提升说明直接训练接口内容更有利于后续推理。由于两种方法的控制机制并非只相差单一组件，该结果应解释为机制对照，而不是严格的因果组件消融。 | Appendix D, Table 5, Halo row; comparison target is the ThinkReset row in the same table<br><span class="experiment-evidence">Halo 83.1 ± 0.7 75.2 ± 0.8 92.2 ± 0.6 91.9 ± 0.7 70.3 ± 0.9</span> |

**定性案例**

- 附录 M 给出一个长链逻辑案例：在上下文接近上限且问题尚未解决时，ThinkReset 两次把已有推理改写为自然语言中间接口，移除原历史后仍得到与更大上下文 full-CoT 相同的最终答案。该案例直观展示接口可承担“替代历史”的作用，而不只是局部修补轨迹；但原文未提供题目全文、逐步输出或案例选择规则，因此它只能作为机制示例，不能替代量化证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It proposes a learnable intermediate interface for maintaining long-horizon reasoning despite bounded context.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`41726810d3907a45b1685e1d89d1b7fcf8ef8fac738a8db5eebf97e73a294ede`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
