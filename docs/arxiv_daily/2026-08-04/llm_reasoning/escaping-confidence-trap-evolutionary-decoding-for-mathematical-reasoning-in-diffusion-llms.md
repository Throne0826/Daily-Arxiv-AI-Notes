---
title: "[论文解读] Escaping Confidence Trap: Evolutionary Decoding for Mathematical Reasoning in Diffusion LLMs"
description: "[arXiv 2608.00605][LLM Reasoning] 本文从解码轨迹而非仅从最终答案出发，指出扩散大语言模型的局部词元置信度可能与全局数学正确性错位，并据此提出无需训练的进化解码框架，在生成过程中选择、保留和扰动候选推理状态。"
arxiv_id: "2608.00605"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:57:53.336320+00:00"
source_sha256: "e8236e572743570416a2e8ba045ad861194581662fb8c52cc89b91d4ea6c6d11"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "扩散大语言模型"
  - "LLaDA 2.0"
  - "数学推理"
  - "分块渐进式解掩码"
  - "置信度解码"
  - "扩散置信陷阱"
  - "测试时扩展"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.00605</p>

# Escaping Confidence Trap: Evolutionary Decoding for Mathematical Reasoning in Diffusion LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Zhenhong Sun, Hanqing Zhao, Yatao Bian, Rongcheng Tu, Liuyue Xie, Xu Zhang, Jue Wang, Davide Modolo, Daoyi Dong, Dacheng Tao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Australian National University；Nanyang Technological University；National University of Singapore；Amazon；University of Technology Sydney</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.00605v1) · [PDF 下载](https://arxiv.org/pdf/2608.00605v1) · **关键词** 扩散大语言模型, LLaDA 2.0, 数学推理, 分块渐进式解掩码, 置信度解码, 扩散置信陷阱, 测试时扩展<br>
**项目页**: [https://engineeringai-lab.github.io/evolutionary-decoding](https://engineeringai-lab.github.io/evolutionary-decoding)

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

本文从解码轨迹而非仅从最终答案出发，指出扩散大语言模型的局部词元置信度可能与全局数学正确性错位，并据此提出无需训练的进化解码框架，在生成过程中选择、保留和扰动候选推理状态。

**不用术语来说**：扩散大语言模型通过逐步揭开被遮蔽的词元来生成答案，但数学解题要求数字、运算符和中间变换前后一致。模型可能很有把握地生成局部看似合理的内容，却在关键数字或符号上走错；一旦错误方向在当前文本块中固定下来，单纯多生成几次也可能反复得到相似的错误答案。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者通过对 LLaDA 2.0 每道题进行八次独立采样并检查其解码轨迹，将“扩散置信度陷阱”归纳为两类：采样敏感型失败中正确路径存在但难以稳定保留；采样一致型失败中不同采样反复收敛到相似、置信度高但价值低的错误续写。
- 作者提出无需修改模型参数的进化解码：步级选择在渐进揭蔽时增强具有潜在价值但置信度适中的数字与符号，并抑制重复模式；块级变异则在低支持度路径定型前引入结构化的数字和符号替代项，分别针对路径不稳定与错误吸引状态难以逃离的问题。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

扩散大语言模型（dLLM）不按从左到右的固定顺序逐词生成，而是从含有大量掩码的位置出发，通过多轮去噪逐步确定词元；LLaDA 2.0 采用分块渐进式解掩码，在块内并行预测和修正词元，并让已完成的块承接后续推理。该机制具有高效、灵活的生成能力，但数学推理不仅要求局部文本流畅，还要求数字、运算符和中间变换构成连续且一致的推理轨迹。本文因此关注一个特定问题：以局部词元置信度决定解掩码顺序时，模型能否稳定保留对最终答案至关重要的数值—符号结构，而不是过早固定到局部可信但全局错误的推理方向。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**扩散大语言模型（dLLM）**

一种通过迭代去噪或反复细化掩码词元来生成文本的语言模型，与从左到右一次确定一个词元的自回归模型不同。一次迭代可以同时预测多个位置，后续迭代再逐步修正或确定这些位置。

</div>
<div class="concept-item" markdown="1">

**分块渐进式解掩码**

模型把待生成序列划分成若干块，在当前块内经过多步预测，依据置信度逐渐把掩码位置变成确定词元，完成后再推进到下一块。数学推理中的数字或运算符如果在块内被延迟、压制或错误固定，后续块通常会继承这一偏差。

</div>
<div class="concept-item" markdown="1">

**测试时扩展（test-time scaling）**

在不重新训练模型的条件下，增加推理阶段的计算，例如重复采样、搜索、重掩码或候选选择，以提高答案正确率。本文所研究的设置进一步要求干预单条扩散轨迹内部的状态演化，而不只是生成更多彼此独立的完整答案。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一道需要多步数值—符号推导的数学问题，以及作为基础生成器的 LLaDA 2.0；模型在参数保持不变的条件下，以分块渐进解掩码生成推理过程和最终答案。研究假设局部词元置信度并不总能代表全局数学正确性，并通过每道题八次独立运行观察两类错误：采样敏感错误中，正确轨迹确实存在，但关键数字或运算符不能被稳定保留；采样一致错误中，多次运行都趋向相似、重复且高置信的错误续写。由此，论文把待解决的问题界定为：如何在测试时改变候选推理状态的保留与多样化过程，使模型既能保存尚不十分确定但有推理价值的数值—符号信号，又能在当前块完全固定之前脱离高置信、低价值的错误区域，最终输出更可靠的完整推理轨迹与答案。原文在所给章节中未形式化给出输入、输出或概率分布的专用符号。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$N$**

Best-of-N 等测试时扩展方法中生成或比较的候选样本数量；所给章节只提及该通用记号，未给出本文实验采用的具体取值。

</div>

</div>

**直接相关的工作**

- **Self-Consistency（文献[28]）**: 该方法通过对同一问题重复采样并聚合结果来利用推理随机性，是本文判断错误是否主要源于采样噪声的直接参照。本文观察到每题八次独立运行后仍有大量错误持续出现，据此认为仅增加独立样本不能解决由置信度驱动的系统性解码偏差。
- **置信度解码及其质量—探索困境（文献[6]、[13]）**: 这类方法依据模型对词元的局部置信度安排渐进解掩码，已有研究分别讨论了其理论效率以及生成质量与探索能力之间的矛盾。本文进一步把该矛盾落实到数学推理轨迹：局部高置信词元可能对应全局错误方向，而暂时低置信的数字或符号反而可能是正确推理所需信号。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

数学推理依赖连续而一致的数字—符号结构，某个关键数字、运算符或中间变换被延迟、压制或错误固定，都可能使后续推导整体失效。扩散模型采用分块渐进揭蔽，虽然具有并行和灵活生成的优势，但通用语言能力并不能保证这种精确结构在解码过程中得到可靠保存，因此需要直接提高其推理轨迹的稳定性与可纠错性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **训练与反馈驱动的模型增强**：通过大规模指令微调、数学领域监督微调，让模型学习数学解答格式和思维链；或利用偏好优化、强化学习及验证器反馈，使生成结果更符合最终答案正确性或中间推理质量。
- **推理时采样与搜索**：在不一定重新训练模型的情况下，采用重复采样、基于置信度的揭蔽、重新遮蔽、无奖励引导或测试时搜索，利用扩散生成的随机性和并行预测能力寻找更好的答案。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 重复采样隐含地假设错误主要来自随机噪声，只要增加样本就有机会恢复正确路径；但作者对每题进行八次独立运行后发现，许多错误跨样本持续出现。这说明失败可能由置信度驱动的分块解码动力学系统性地产生，增加彼此独立的输出并不能保证逃离同一错误方向。
- 常规置信度解码把局部高置信度视为优先确定词元的依据，却没有充分处理局部确定性与全局推理价值的错位：它可能过早淘汰置信度适中但关键的数字或符号，也可能不断强化重复、低价值但高置信度的文本块，分别造成正确轨迹不稳定和错误轨迹固化。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作虽能通过训练、反馈、采样或搜索提高总体表现，但尚缺少一种针对扩散模型内部解码轨迹的机制：它需要在词元逐步揭蔽时保护脆弱但有用的数字—符号信号，并在整个文本块收敛到错误方向之前主动构造有结构的替代路径。换言之，缺口不只是如何获得更多候选答案，而是如何控制候选推理状态在块内被选择、跨块被继承以及遇到错误吸引状态时被有效多样化。

</div>
<div markdown="1"><span>核心问题</span>

扩散大语言模型的分块渐进解码能否通过轨迹级干预，更可靠地保存连贯的数字—符号推理块，并同时缓解正确路径不稳定的采样敏感型失败与反复落入相似错误续写的采样一致型失败？

</div>
<div markdown="1"><span>作者直觉</span>

作者把解码类比为候选推理状态的进化：词元在块内逐步“生长”，较完整的文本块把已有推理传递到下一阶段。若只按局部置信度选择，关键但暂时不够确定的数字或符号容易被淘汰，而已经占优的重复错误又会持续自我强化。因此，一方面应在每一步保留可能承载正确计算的脆弱信号并压制重复模式，另一方面应在错误方向彻底定型前注入符合数学表达结构的替代项；这种“选择加变异”比仅增加独立样本更可能稳定正确路径并跳出高置信度错误区域。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把扩散大语言模型的数学推理解码重新表述为候选推理状态的“进化”：输入提示词后，模型仍按从左到右的顺序生成多个块，并在每个块内通过多步扩散逐渐解除掩码，但不再仅凭局部最高概率决定哪些词元立即固定。Evolutionary Decoding 在块内加入逐步选择，用数值-符号增强项保护暂时不够自信但可能承载计算信息的词元，同时用跨块重复惩罚抑制高置信度的机械续写；在块形成早期，还可按需启动块级突变，通过调整词表 logits 产生中性、数值、符号和混合候选，再让原模型置信度最高的候选存活。完整块被追加到上下文，流程重复至生成最终答案。
技术上，该框架分别针对两类置信度陷阱：逐步选择处理“存在正确路径但中间状态不稳定”的采样敏感失败，块级突变处理“多次采样仍收敛到同一错误路径”的采样一致失败。通俗地说，前者是在每一步避免把关键算式线索过早淘汰，后者是在推理已经走入固定错误套路时有控制地尝试几条更偏向数字或数学符号的岔路；它只改变测试时解码，不训练或修改模型参数。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 块式扩散初始化与基础预测

模型对当前块所有仍被掩码的位置并行预测词表分布，取得各位置的 top-1 词元 $\hat{x}_{m,i}^{t}$、置信度 $c_{m,i}^{t}$ 和 logits $\mathbf{z}_{m,i}^{t}$。前序块保持固定，当前块则在后续扩散步中反复重预测，直至完成。

<div class="method-step__io" markdown="1">

**输入**：提示词 $\mathbf{x}$、已经完成的前序块 $\mathbf{y}_{<m}$，以及初始化为掩码的当前块 $\mathcal{B}_m^{(t)}$。<br>
**输出**：当前扩散步的候选词元、置信度、概率分布和 logits，以及待解除掩码的位置集合 $\mathcal{M}_m^t$。

</div>

**直观理解**：模型一次查看当前段落里所有空格，并为每个空格提出最可能的词及把握程度；已写完的前文不再改动。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 逐步选择与防停滞回退

对每个位置计算选择分数 $s_{m,i}^{t}=c_{m,i}^{t}+s_{\mathrm{en}}(m,i,t)-s_{\mathrm{re}}(m,t)$：数值-符号增强项按预测熵提升关键词元，重复惩罚则按当前块与前块的匹配比例统一压低释放分数；只有分数达到阈值 $\tau$ 的位置才解除掩码。若惩罚导致原本有高置信位置却无任何位置过阈值，则按原始置信度释放 top-$K$ 个位置；若原始置信度本身也不足，则仅释放最自信位置，以保证解码单调推进。

<div class="method-step__io" markdown="1">

**输入**：各掩码位置的 top-1 预测与置信度、预测分布、数值或符号类别标记，以及当前块和前一块的可比较位置。<br>
**输出**：保留有用数值-符号信号并减少重复续写的下一步块状态 $\mathbf{x}_m^{t+1}$。

</div>

**直观理解**：算法不只问“模型有多自信”，还问“这个词是否可能是关键算式信息、整块是否正在照抄上一块”；回退规则相当于在筛选过严时至少填入少量最可靠内容，避免一直卡住。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按需触发结构化块级突变

先运行不修改 logits 的中性分支并计算其数值-符号置信度；若该值低于 $\tau_{\mathrm{mut}}$ 且突变次数未达到 $m_{\max}$，就在所有掩码位置分别对数值词元、符号词元或两者的 logits 增加强度为 $\delta$ 的偏置，形成中性、数值、符号和混合分支。若中性分支已得到足够数值-符号支持，则不扩展其他分支，从而控制额外推理成本。

<div class="method-step__io" markdown="1">

**输入**：当前块各掩码位置的原始 logits、数值和符号词表掩码、突变阈值 $\tau_{\mathrm{mut}}$，以及当前轨迹已突变块数和预算 $m_{\max}$。<br>
**输出**：候选分支集合 $\mathcal{Q}_m$，其中每个分支对应一种结构化的当前块搜索方向。

</div>

**直观理解**：只有当当前推理缺少算式线索时，系统才同时尝试“更偏数字”“更偏符号”等版本，而不是无条件扩大搜索。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选块解码、生存选择与跨块迭代

每个分支独立完成当前块的扩散解码，并按突变前原模型对已释放词元的平均置信度 $\bar{c}_m^{(q)}$ 评分；选择 $q^*=\arg\max_{q\in\mathcal{Q}_m}\bar{c}_m^{(q)}$，将其块状态作为唯一存活结果。完成的块被追加到上下文，随后初始化下一块并重复上述流程，直至响应结束。

<div class="method-step__io" markdown="1">

**输入**：候选分支集合 $\mathcal{Q}_m$、统一释放阈值 $\tau$，以及逐步选择规则。<br>
**输出**：逐块形成的完整推理文本及其中按统一规则抽取的最终答案。

</div>

**直观理解**：突变负责提出不同岔路，但最终仍由原模型判断哪条岔路最自然可靠；胜出的段落成为不可更改的前文，继续引导下一段推理。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 逐步选择与掩码释放规则

$$
s_{m,i}^{t}=c_{m,i}^{t}+s_{\mathrm{en}}(m,i,t)-s_{\mathrm{re}}(m,t),\qquad x_{m,i}^{t+1}=\begin{cases}\hat{x}_{m,i}^{t},&s_{m,i}^{t}\geq\tau,\\ \texttt{[MASK]},&s_{m,i}^{t}<\tau.\end{cases}
$$

**符号说明**

- $m$：当前生成块的序号。
- $t$：当前块内部的扩散解码步。
- $i$：当前块中的掩码位置。
- $c_{m,i}^{t}$：模型在位置 i 对 top-1 预测给出的原始置信度。
- $s_{\mathrm{en}}(m,i,t)$：针对数值或数学符号 top-1 预测的增强分数。
- $s_{\mathrm{re}}(m,t)$：由当前块与前一块重复程度决定的块级惩罚。
- $s_{m,i}^{t}$：综合原始置信度、数值-符号增强和重复惩罚后的选择分数。
- $\tau$：决定位置是否解除掩码的释放阈值。
- $\hat{x}_{m,i}^{t}$：位置 i 在当前扩散步的 top-1 候选词元。
- $x_{m,i}^{t+1}$：下一扩散步中位置 i 的状态，取已释放词元或继续保持掩码。

<div class="equation-explanation" markdown="1">

**直观理解**：该式是逐步选择的核心：模型置信度仍是基础，但关键数字或符号得到加分，整块重复则受到扣分。最终分数达到阈值才固定词元，使局部流畅度不再是唯一的生存标准，同时保留原扩散解码逐步填充块的基本形式。<br>
**原文位置**：第 3.2 节，公式 (2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 结构化块级突变

$$
\tilde{\mathbf{z}}_{m,i}^{t,(q)}=\mathbf{z}_{m,i}^{t}+\delta\left(\eta_{\mathrm{num}}^{(q)}\mathbf{VM}_{\mathrm{num}}+\eta_{\mathrm{sym}}^{(q)}\mathbf{VM}_{\mathrm{sym}}\right),\qquad i\in\mathcal{M}_{m}^{t}.
$$

**符号说明**

- $\mathbf{z}_{m,i}^{t}\in\mathbb{R}^{V}$：原模型对位置 i 的完整词表 logits 向量。
- $\tilde{\mathbf{z}}_{m,i}^{t,(q)}$：突变分支 q 对位置 i 调整后的 logits 向量。
- $V$：模型词表大小。
- $\delta$：施加到目标词元类别上的突变偏置强度。
- $\eta_{\mathrm{num}}^{(q)}$：分支 q 是否启用数值词元偏置的二值方向变量。
- $\eta_{\mathrm{sym}}^{(q)}$：分支 q 是否启用符号词元偏置的二值方向变量。
- $\mathbf{VM}_{\mathrm{num}}$：在整个词表中标记数值词元的二值向量。
- $\mathbf{VM}_{\mathrm{sym}}$：在整个词表中标记预定义数学符号词元的二值向量。
- $\mathcal{M}_{m}^{t}$：第 m 个块在扩散步 t 仍处于掩码状态的位置集合。
- $q$：中性、数值、符号或数值-符号混合突变分支的索引。

<div class="equation-explanation" markdown="1">

**直观理解**：该式在不修改模型参数的前提下，对目标类别的整个词表 logits 加上固定偏置，从而生成具有明确搜索方向的候选块。中性分支保持原分布，其他分支分别鼓励数字、符号或两者；这比无结构随机扰动更贴合数学推理中需要恢复数值-符号轨迹的目标。<br>
**原文位置**：第 3.3 节，公式 (6)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。Evolutionary Decoding 是训练无关的测试时扩展框架，没有新增训练损失、梯度更新或参数优化；原始扩散语言模型参数 $\theta$ 全程冻结。文中的选择分数、突变偏置和生存评分都是推理阶段的搜索控制信号，而不是用于反向传播的目标函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 数值-符号增强**

对位置 $i$ 的预测分布计算熵 $H_{m,i}^{t}=-\sum_v p_{m,i}^{t}(v)\log p_{m,i}^{t}(v)$，再定义 $s_{\mathrm{en}}(m,i,t)=\alpha\eta_{m,i}^{t}H_{m,i}^{t}$；其中 $\eta_{m,i}^{t}\in\{0,1\}$ 仅在 top-1 预测属于数值或预定义数学符号集合时取 $1$。因此普通自然语言词元仍按原置信度选择，而具有一定不确定性的数字或符号可获得与熵和强度 $\alpha$ 成正比的分数补偿。

> 直观理解：数学推理中的数字、括号和运算符可能因为局部语境不完整而暂时不够自信，却比流畅的连接词更能决定答案；该模块给这些线索多一次被保留的机会，但不直接提升普通文本。

**2. 块重复惩罚与回退**

在当前块和前一块的可比较位置集合 $\mathcal{C}_m$ 上，计算匹配率 $r_m^t=|\mathcal{C}_m|^{-1}\sum_{i\in\mathcal{C}_m}\mathbf{1}(\hat{x}_{m,i}^{t}=\hat{x}_{m-1,i})$，并令 $s_{\mathrm{re}}(m,t)=\beta r_m^t$。该惩罚对当前块所有掩码位置相同，因而不改变位置之间的相对次序，只在块整体高度重复时降低解除掩码的积极程度；额外的 top-$K$ 或单位置回退保证不会永久停滞。

> 直观理解：若新段落几乎逐位置重复上一段，高置信度可能来自机械模式而非有效推理；统一降分让模型重新考虑这些位置，而回退机制确保抑制重复不会把生成过程完全冻结。

**3. 结构化突变与生存选择**

突变不随机替换已经生成的文本，而是借助词表级二值掩码 $\mathbf{VM}_{\mathrm{num}}$ 和 $\mathbf{VM}_{\mathrm{sym}}$，对所有尚未揭示位置的特定类别 logits 施加全局偏置；分支方向由 $(\eta_{\mathrm{num}}^{(q)},\eta_{\mathrm{sym}}^{(q)})\in\{(0,0),(1,0),(0,1),(1,1)\}$ 指定。分支生成后，用突变前的原模型平均置信度选择存活候选，使探索方向受到人为结构约束，但最终判断仍锚定模型自身分布。

> 直观理解：这里的“突变”不是随意打乱句子，而是有针对性地提高数字或数学符号成为候选的机会；随后再让原模型选出最可信版本，以减少强制偏置破坏语言连贯性的风险。

**训练与推理**

训练阶段沿用现有 dLLM，本文方法不参与训练。推理时，给定提示词后先把响应划分为按序生成的块；对当前块的所有掩码位置并行预测，再利用数值-符号增强和重复惩罚计算选择分数，按阈值逐步解除掩码，并在过度抑制或整体低置信时使用回退规则维持进度。块形成早期先检查中性分支的数值-符号置信度：只有低于 $\tau_{\mathrm{mut}}$ 且尚未耗尽 $m_{\max}$ 个突变块预算时，才激活数值、符号和混合突变分支；各分支使用相同阈值完成解码后，以原模型对已释放词元的平均置信度选择唯一存活块。胜出块追加到固定上下文，随后解码下一块，最终按统一答案抽取规则读取响应中的最后一个 $\backslash\mathrm{boxed}\{\cdot\}$ 内容。

**复现信息**

数值和符号词元通过轻量、与 tokenizer 无关的词法规则识别：候选词元解码为文本后，正则分别匹配纯数字、仅由预定义字符 $+,-,*,/,=,(,),[,],\{,\},\text{逗号},\text{句点},:,;,\backslash$ 构成的符号串，以及数字与这些符号的组合。这种检测便于复现选择增强和词表掩码，但不覆盖字母变量、不等号、幂、百分号或任务特定算子，因此它只是数学信息词元的近似代理，而非完整数学词法分析器。
为公平解释输出，所有数据集使用同一提示语“Please reason step by step, and put your final answer within \$\boxed{}$.”，并从最后一个匹配到的 $\backslash\mathrm{boxed}\{\cdot\}$ 中抽取答案，再消除冗余空格、换行和简单格式差异。该正则抽取可能无法识别异常格式或数学等价但字符串不同的表达式，不过论文对所有基线和方法使用同一提示、解码约束与抽取流程；所给节选未明确报告 $\alpha$、$\beta$、$\delta$、$\tau$、$\tau_{\mathrm{mut}}$、top-$K$ 和 $m_{\max}$ 的具体取值，复现时仍需核查论文其余实现配置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- AIME 2024、AIME 2025和AIME 2026：三组高难度数学竞赛题，重点检验长链、多步的数值与符号推理，以及解码器能否从局部高置信但全局错误的轨迹中恢复。摘录未报告具体规模与数据划分；附录F另按AIME 2025的AIME-I和AIME-II子集分析逐题轨迹。
- AMC 2023：推理链通常比AIME短、但仍具有非平凡竞赛难度的数学题，用于判断ED的收益是否局限于最困难的长链问题。摘录未报告样本规模与数据划分。
- MATH500与GSM8K：前者覆盖代数、几何、计数等较广数学主题，后者测试自然语言场景中的小学算术推理；二者共同承担域外广度和较短推理任务的检验。摘录未报告所用划分及是否采用完整测试集。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**pass@1（P@1）**

衡量一次解码产生正确最终答案的比例，是论文的主要准确率指标，最接近只允许模型提交一个答案的实际使用情形。 （越高越好，因为它表示无需依赖多次尝试即可得到正确答案的概率更大。）

</div>
<div class="metric-item" markdown="1">

**pass@8（P@8）**

衡量重复随机解码八次后，候选池中至少存在一个正确答案的比例，主要反映探索和生成正确候选的能力，而不直接衡量系统能否自动选中该候选。 （越高越好，但它应被视为八候选池的近似oracle上界；若P@8远高于实际选择结果，瓶颈就在答案选择而不只是答案生成。）

</div>
<div class="metric-item" markdown="1">

**轨迹级诊断指标**

包括平均生成块数、总解码步数、数值/符号token比例、重复率、平均置信度和置信度坍塌频率。它们分别观察计算长度、推理信息密度、冗余程度及置信度是否失真，用于解释准确率为何变化，而不是替代最终正确率。 （没有统一方向：在准确率不降时，更少的块和步骤、更低的重复或坍塌频率通常更好；较高的数值/符号比例只有在确实对应有效推理而非机械符号堆积时才有正面意义。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### LLaDA2.0-Flash与LLaDA2.0-Mini在AMC 2023上的完整ED

<div class="result-value" markdown="1">

作者报告ED将两个模型在AMC 2023上的准确率都提高到$95.0\%$。这是摘录中最明确的跨模型主结果，说明该方法并非只对某一个LLaDA 2.0规格有效。

</div>

直观地说，结构化搜索让两个模型在较短但仍有难度的竞赛题上更可靠。该结果只能证明特定数据集和评价协议下的最终正确率较高，不能单独证明收益全部来自“逃离置信度陷阱”，也不能说明相同收益会推广到其他模型家族。

<div class="result-source" markdown="1">

来源：Appendix B, Figure 4 analysis corresponding to Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

This trend is especially visible on AMC23, where ED improves both models to 95.0%, and on the AIME benchmarks, where the gains are more pronounced than those from Selection alone.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 六个基准上的解码步数—准确率权衡

<div class="result-value" markdown="1">

作者观察到，在AIME 2024/2025/2026和AMC 2023等竞赛级任务上，ED增加解码步骤时通常也提高准确率；这表明额外测试时计算在困难任务上能够转化为推理收益。原文同时指出Selection在该权衡空间中接近Baseline，说明仅做逐步选择的收益和额外成本都较有限。

</div>

这一结果回答的是“多算是否值得”：对困难、长链问题，额外分支探索较可能修复错误轨迹；但图中点向右移动也意味着更高推理成本。它不是等计算预算比较，因此不能据此断言ED在计算效率上优于Baseline，也不能排除部分准确率提升只是使用了更多解码步骤。

<div class="result-source" markdown="1">

来源：Appendix B, Figure 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For challenging competition-style datasets such as AIME24/25/26 and AMC23, the trajectories generally move upward together with the step increase, showing that ED can convert additional test-time computation into better reasoning accuracy.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 两个LLaDA 2.0模型的八次重复采样

<div class="result-value" markdown="1">

作者报告ED在两个模型上同时改善P@1和P@8：前者表示单次轨迹更可靠，后者表示八条候选构成的池中更容易包含正确答案。因此ED的作用不只是在固定候选中重排结果，也扩大了可找到正确路径的候选集合。

</div>

P@8提高说明结构化探索确实生成了更多有用路径，但P@8与多数投票或置信度选择等可部署指标仍有较大差距。换言之，ED改善了“生成正确答案”的能力，却没有彻底解决“在不知道标准答案时选中它”的问题；P@8不能被当作真实系统准确率。

<div class="result-source" markdown="1">

来源：Appendix C, Figure 5 analysis corresponding to Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ED improves both P@1 and P@8 across the two models, showing that its structured exploration benefits not only a single decoding trajectory but also the overall candidate pool.

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

- LLaDA 2.0默认置信度解码（Baseline）：每步依据局部token置信度推进，是最直接的基准，也正是论文所分析的“置信度陷阱”可能发生的解码方式。
- 重复随机采样：对同一问题独立生成多条轨迹，并以pass@8衡量候选集中至少出现一次正确答案的能力。它用于区分“单条轨迹不稳定”和“模型根本难以产生正确路径”，但pass@8本身是带有正确性判定的候选池上界，并非实际可直接部署的答案选择策略。
- Selection only：只启用逐步候选选择，不加入结构化变异和生存机制，用来隔离“保留数值/符号信号、抑制重复内容”本身的贡献。原文说明变异与生存依赖已经选出的候选块，因此没有把它们作为脱离Selection的独立解码器。

**实验想回答的问题**

- Evolutionary Decoding（ED）相较于LLaDA 2.0默认的置信度解码，能否在不同难度和推理风格的数学任务上提高单次生成的正确率，并将额外的测试时计算有效转化为竞赛级问题上的准确率收益？
- 性能变化分别来自候选块的逐步选择还是结构化变异；在多次采样时，ED究竟改善了正确候选的生成能力，还是也解决了从候选池中识别正确答案的问题？

**实验实现**

实验比较LLaDA2.0-Flash与LLaDA2.0-Mini上的默认解码、Selection和完整ED，并另在重复八次采样的条件下比较Baseline与ED。完整ED先在扩散解码的每一步筛选更有推理价值的候选，再以数值、符号、混合和中性分支进行块级结构化变异，最后通过生存机制保留后续候选；附录还考察只在疑似失败时触发变异的门控版本。评价以pass@1为主、pass@8为多样性上界，并联用轨迹长度、信息密度、重复和置信度诊断。摘录没有提供随机种子、提示模板、每题运行次数、置信区间、显著性检验、硬件、解码超参数或完整候选选择规则，因此这些结果仍需对照原表和代码复核。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| AIME 2025上Baseline与Selection only的逐题轨迹比较 | 加入Selection后，平均最终块索引由$70.0$降至$54.9$，平均解码步数由$669$降至$638$，解出题数由$17/30$增至$20/30$。 | 该对比隔离了逐步选择的作用：在没有结构化变异的情况下，它同时缩短轨迹并多解出$3$题，支持“优先保留数值和符号信号能够抑制冗长漂移”的解释。不过样本只有$30$题，摘录未给出多次运行方差或显著性检验，不能据此精确估计稳定的总体增益。 | Appendix F.1, Figure 7<br><span class="experiment-evidence">Compared with the baseline, the average block index is reduced from 70.0 to 54.9, and the average decoding steps are reduced from 669 to 638, while the number of solved problems increases from 17/30 to 20/30.</span> |
| AIME 2025上无条件Mutation与失败感知的Gated Mutation | 无条件变异解出$21/30$题；门控策略只对疑似失败轨迹触发变异，将解出题数进一步提高到$22/30$，并把平均最终块索引降至$50.6$。门控条件包括较晚块索引、低选择置信度，或最近$10$个块的重复率超过$0.5$。 | 该消融检验“是否所有题都需要变异”。结果表明，把变异当作失败后的纠错机制比无条件扰动更合理：已经正确的Selection轨迹可避免被额外分支破坏，疑似陷入错误盆地的轨迹则获得探索机会。但门控规则使用了人工阈值，摘录没有报告阈值敏感性，也未给出总计算量，因此平均块索引下降不能直接等同于整体运行成本按同比例下降。 | Appendix F.1, Figure 7, Gated row<br><span class="experiment-evidence">As shown in the Gated row, it further improves the solved count to 22/30, while reducing the average block index to 50.6 compared with unconditional mutation.</span> |

**定性案例**

- AIME 2025的块级轨迹图把失败概括为两类：采样一致型失败中，模型对局部数字或符号仍保持高置信，却不断生成冗余自然语言并停留在稳定的错误路径；采样敏感型失败则表现为置信度波动和较低的数字/符号密度，说明转移容易滑向低信息续写。Selection倾向于缩短并稳定轨迹，Mutation则在前$16$个块索引内引入数值、符号、混合和中性分支，使部分稳定错误路径恢复为正确答案。这些可视化支持两组件分工的机制解释，但属于定性证据，不能独立建立因果关系。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出面向扩散语言模型数学推理的训练无关进化解码与推理时扩展方法。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`e8236e572743570416a2e8ba045ad861194581662fb8c52cc89b91d4ea6c6d11`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
