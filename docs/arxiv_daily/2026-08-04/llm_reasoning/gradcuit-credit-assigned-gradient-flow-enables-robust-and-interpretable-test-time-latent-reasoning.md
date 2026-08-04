---
title: "[论文解读] GradCuit: Credit-Assigned Gradient Flow Enables Robust and Interpretable Test-Time Latent Reasoning"
description: "[arXiv 2608.02585][LLM Reasoning] GradCuit将可优化的连续潜变量插入Transformer中间层，利用自注意力形成从生成序列到潜变量的直接梯度通路，以改善测试时潜在推理的信用分配、优化稳健性与可解释性。"
arxiv_id: "2608.02585"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:58:08.445116+00:00"
source_sha256: "141484c4d26ec7b3499f89f6ded29256d60b835446bcee6a9660c5549f551a0f"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "潜在推理"
  - "测试时优化"
  - "信用分配"
  - "因果自注意力"
  - "策略梯度"
  - "可解释性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.02585</p>

# GradCuit: Credit-Assigned Gradient Flow Enables Robust and Interpretable Test-Time Latent Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Zhaoxin Yu, Qi Shen, Hengli Li, Zhaowei Zhang, Song-Chun Zhu, Chi Zhang, Zilong Zheng</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> NLCo Lab, Beijing Institute for General Artificial Intelligence；Institute of Automation, Chinese Academy of Sciences；School of Artificial Intelligence, Beijing University of Posts and Telecommunications；School of Artificial Intelligence for Science, Peking University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.02585v1) · [PDF 下载](https://arxiv.org/pdf/2608.02585v1) · **关键词** 大语言模型, 潜在推理, 测试时优化, 信用分配, 因果自注意力, 策略梯度, 可解释性<br>


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

GradCuit将可优化的连续潜变量插入Transformer中间层，利用自注意力形成从生成序列到潜变量的直接梯度通路，以改善测试时潜在推理的信用分配、优化稳健性与可解释性。

**不用术语来说**：大语言模型可以在回答单个问题时临时调整一组内部连续状态，而不修改模型参数，从而尝试得到更好的推理结果；但已有方法通常要先把这些内部状态转换成离散文字，再根据最终回答的好坏反过来调整它们。这个文字生成环节像一道狭窄且不透明的接口，使系统难以判断某个内部状态究竟影响了后续哪一步推理，也使优化容易受到学习率和生成过程的干扰。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出GradCuit：在提示表示与生成续文之间的选定Transformer层插入少量可学习潜在状态，使自注意力同时承担前向的词元—潜变量交互和反向的信用分配，从而让整段续文产生的奖励加权梯度直接更新潜变量，而基础模型参数保持冻结。
- 把性能、稳健性和可解释性统一到同一条梯度通路上：作者报告GradCuit相对标准思维链提示的平均准确率提高$6.6$个百分点，相对最强增强推理基线提高$2.4$个百分点；同时可利用后续词元关于潜变量的雅可比矩阵分析潜变量影响，并观察到影响集中于推理连接词元。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型的测试时优化与潜在推理研究。标准思维链（Chain-of-Thought, CoT）把中间推理过程表示成离散文本；潜在推理则使用连续向量作为中间状态，希望在不完全依赖显式文字轨迹的情况下改善推理。本文关注其中的“推理即优化”设定：面对每个测试样本，在冻结大语言模型参数的前提下，仅优化该样本专属的潜在状态，并依据生成结果的奖励调整这些状态。GradCuit进一步把可优化状态插入Transformer的某个中间层，使后续词元的计算及其梯度都能沿因果自注意力路径直接连接到潜在状态。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试时优化**

模型部署后，针对当前输入额外执行优化，以提高当前样本的输出质量。本文不更新模型参数，只更新插入模型内部、随样本变化的少量连续状态。

</div>
<div class="concept-item" markdown="1">

**因果自注意力**

Transformer生成某个词元时，只允许该位置读取此前位置的表示；这些依赖关系构成从前序状态到后续预测的可微计算路径。GradCuit利用该路径同时传递前向信息和反向梯度。

</div>
<div class="concept-item" markdown="1">

**信用分配**

信用分配要判断哪些中间状态或决策应对最终奖励负责。本文的核心问题是把整段续写获得的反馈直接归因到各个潜在状态，而不是让反馈仅通过已解码的离散词元间接到达它们。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个待推理的提示及冻结的指令微调Transformer，目标是生成推理续写和最终答案。对每个测试实例，方法在选定的Transformer层中，将一组可优化潜在状态插入提示隐藏表示与生成续写之间；模型其余部分保持不变，因果自注意力使每个后续词元的对数概率对先前潜在状态可微。随后利用续写结果产生的奖励加权梯度，迭代更新潜在状态$z$，再基于更新后的内部状态继续生成。该设定与测试时训练不同，因为它不修改模型权重；也与通常的软提示训练不同，因为它不要求使用监督数据预先学习一组跨样本共享的向量。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$z$**

针对当前测试实例插入Transformer中间层并被迭代优化的潜在状态集合。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{J}$**

用于优化潜在状态的策略梯度目标；原文所示更新利用其关于潜在状态的梯度。

</div>
<div class="notation-item" markdown="1">

**$\nabla_z\mathcal{J}$**

目标函数对潜在状态的梯度，用于把生成续写的反馈反向分配给潜在状态。

</div>

</div>

**直接相关的工作**

- **LatentSeek**: 同属测试时潜在优化方法，但其优化输出侧潜在表示，再将其解码成词元序列进行奖励评估；因此潜在变量与后续推理之间仍以离散解码结果为接口。GradCuit改为把状态插入Transformer中间层，使续写词元的对数概率能够通过剩余网络直接对这些状态求导。
- **LTPO**: LTPO在测试时优化输入侧潜在思维向量，使用置信度奖励和基于扰动的策略梯度。GradCuit的区别在于利用Transformer内部自注意力构成的可微路径，将后续词元的反馈直接传播到所选中间层的潜在状态。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

测试时潜在推理希望针对当前实例优化连续内部状态，以提升复杂推理质量，同时避免重新训练或更新大模型参数。真正困难的不是能否设置这些潜变量，而是如何把整段推理及最终答案得到的序列级反馈准确传回产生该推理的内部状态；若反馈归因不清，测试时优化就可能不稳定，也难以解释一次潜变量更新为何会改变答案。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **显式思维链提示（CoT）**：让模型把中间推理步骤生成为可读词元，再依据这些离散词元继续预测答案。它提供了可观察的推理轨迹，但其主要作用是引导生成，并未建立序列级结果反馈到连续内部推理状态的专门优化接口。
- **基于优化的测试时潜在推理（LatentSeek、LTPO、MILR）**：冻结大模型参数，为每个输入实例设置并迭代优化潜变量，以提高生成质量；这些方法以解码词元作为潜变量连接推理轨迹的接口，通常通过词元级目标的策略梯度，将结果反馈经由解码过程反向传到潜变量。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 间接优化：潜变量必须经过离散解码过程才能影响并接收来自后续推理的反馈，解码形成信息瓶颈，使优化信号与中间词元表示纠缠，因而难以把序列级奖励直接、明确地分配给具体潜在状态。
- 潜变量动力学不透明：离散生成路径遮蔽了单个潜变量对后续词元预测的作用，研究者难以解释某次潜变量更新改变了哪些推理环节；原文还以对学习率较敏感的LatentSeek作为稳健性比较对象，说明现有优化接口可能对超参数选择较为脆弱。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作尚缺少一种统一的测试时接口：它既能保持基础模型冻结，又能让整段续文中各词元的对数概率对先前潜变量直接可微，并据此进行明确的序列级信用分配；同一接口还应允许检查潜变量对具体后续词元的影响，而不是只能观察最终输出变化。

</div>
<div markdown="1"><span>核心问题</span>

能否把实例特定的可优化潜在状态直接嵌入Transformer内部计算图，借助因果自注意力将结果奖励从整段生成序列直接传播到这些状态，从而同时提高测试时潜在推理的效果、对优化设置的稳健性以及内部更新的可解释性？

</div>
<div markdown="1"><span>作者直觉</span>

因果自注意力本来就允许后续位置读取此前位置的信息。若把潜变量放入某个中间层，并让后续Transformer层把它们视为可被关注的前置状态，那么潜变量对每个后续词元预测的影响会保留在连续计算图中：前向时，潜变量参与塑造推理；反向时，奖励加权的词元梯度可沿同一注意力路径返回潜变量。直观地说，作者不是让反馈绕过已经写出的文字去猜内部状态的责任，而是把可调状态直接接入模型进行推理和传递梯度的线路。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

GradCuit是一种仅在测试时优化连续隐状态、而不更新语言模型参数的方法。给定问题上下文$c$，方法先附加固定推理前缀，在第$l$个Transformer解码块的输入处提取该前缀对应的$N$个隐状态$\bm{z}_0^{(l)}$，并引入从零初始化的可优化偏移$\Delta\bm{z}^{(l)}$。推理时使用$\widetilde{\bm{z}}^{(l)}=\bm{z}_0^{(l)}+\Delta\bm{z}^{(l)}$替换原前缀状态；模型其余参数、位置编码与因果注意力掩码均保持不变。由于这些隐状态位于提示与续写之间，后续每个生成词元都能通过剩余Transformer层的因果自注意力依赖它们，因此整段回答的词元对数概率可将奖励加权梯度直接传回全部隐状态。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造实例级潜变量

先用模型原生聊天模板渲染$c$，再附加前缀“Let’s think about this problem and solve it step by step.”；将二者通过前$l$层，在所选解码块输入处抽取前缀跨度的表示$\bm{z}_0^{(l)}\in\mathbb{R}^{N\times d}$，并初始化$\Delta\bm{z}^{(l)}=\bm{0}$。

<div class="method-step__io" markdown="1">

**输入**：问题上下文$c$、固定文本前缀$s$、冻结的自回归语言模型$\pi$以及选定层$l$。<br>
**输出**：当前潜变量$\widetilde{\bm{z}}^{(l)}=\bm{z}_0^{(l)}+\Delta\bm{z}^{(l)}$，其中$N$由该模型分词器对前缀的切分结果决定，$d$为隐状态维度。

</div>

**直观理解**：固定前缀先提供一个模型熟悉的“逐步思考”起点，优化过程再调整其内部表示，而不是直接改写提示文字。每个问题都有独立的偏移量，处理完该问题后无需保留。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 插入潜变量并生成回答

前向预钩子在所选解码块输入处，用$\widetilde{\bm{z}}^{(l)}$替换原前缀跨度；拼接序列$[h_c^{(l)},\widetilde{\bm{z}}^{(l)},h_{\bm{x}_{<t}}^{(l)}]$通过第$l+1$至$M$层和语言模型头，按贪心解码生成完整续写$\bm{x}$。

<div class="method-step__io" markdown="1">

**输入**：提示在第$l$层的表示$h_c^{(l)}$、潜变量$\widetilde{\bm{z}}^{(l)}$以及先前生成词元的表示$h_{\bm{x}_{<t}}^{(l)}$。<br>
**输出**：一条包含推理过程和最终答案的续写$\bm{x}=(x_1,\ldots,x_T)$。

</div>

**直观理解**：潜变量像插在问题与回答之间的一组可调“内部提示”。因果注意力允许每个回答词元读取这些位置，所以对潜变量的一次修改可能影响整条后续推理，而不只影响开头几个离散词元。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自验证并形成优化损失

同一骨干模型使用统一验证提示，仅判断最终答案是否正确，得到$R(\bm{x},\bm{c})\in\{0,-1\}$；若答案错误，则固定当前词元序列，以教师强制重新计算全部续写词元的对数概率，并构造奖励加权损失$\mathcal{L}_{\mathrm{opt}}$。

<div class="method-step__io" markdown="1">

**输入**：原问题$c$与从续写$\bm{x}$中抽取的最终答案。<br>
**输出**：正确时得到停止信号$R=0$；错误时得到关于$\Delta\bm{z}^{(l)}$的梯度。

</div>

**直观理解**：验证器只回答“最终答案对不对”，不评价推理写得是否完整。错误回答的整条词元轨迹共同提供梯度，使潜变量朝降低该错误轨迹概率的方向变化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 更新、重生成与停止

仅用Adam更新$\Delta\bm{z}^{(l)}$，随后以更新后的潜变量从头贪心生成完整续写并重新验证；若$R=0$则立即返回，否则重复至最多$K=10$次潜变量更新。

<div class="method-step__io" markdown="1">

**输入**：损失$\mathcal{L}_{\mathrm{opt}}$、当前偏移$\Delta\bm{z}^{(l)}$及更新预算$K$。<br>
**输出**：首个被自验证器接受的续写，或达到预算后最后一次更新产生的续写。

</div>

**直观理解**：这不是在同一答案后继续补写，而是每次微调内部思考状态后重新作答。模型权重始终冻结，因此变化仅服务于当前测试问题。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 插入中间层潜变量后的下一词元分布

$$
\pi(x_t\mid\mathbf{x}_{<t},\mathbf{z}^{(l)},\mathbf{c})=\operatorname{LM\_Head}\!\Bigl(\operatorname{Transformer}^{l+1:M}\!\bigl([h^{(l)}_{\mathbf{c}},\,\mathbf{z}^{(l)},\,h^{(l)}_{\mathbf{x}_{<t}}]\bigr)\Bigr)
$$

**符号说明**

- $\pi$：参数冻结的自回归语言模型所定义的条件生成分布。
- $x_t$：续写中的第t个词元。
- $\mathbf{x}_{<t}$：第t个位置之前已生成的续写词元。
- $\mathbf{c}$：输入问题及其聊天模板上下文。
- $\mathbf{z}^{(l)}$：插入第l层隐空间的N个可优化连续潜变量。
- $h^{(l)}_{\mathbf{c}}$：问题上下文经过前l层后得到的隐表示。
- $h^{(l)}_{\mathbf{x}_{<t}}$：已有续写词元经过前l层后得到的隐表示。
- $\operatorname{Transformer}^{l+1:M}$：从第l+1层到第M层的剩余Transformer计算。
- $\operatorname{LM\_Head}$：把最终隐表示映射为词表概率的语言模型头。

<div class="equation-explanation" markdown="1">

**直观理解**：该式规定了潜变量如何真正进入生成过程：上下文、潜变量和已有续写的中间层表示一起经过剩余网络。与先把潜变量解码成前缀词元的方法不同，这条连续计算路径让任意后续词元的概率都能对潜变量求导。<br>
**原文位置**：第2.2节，公式(4)

</div>

</div>

<div class="equation-block" markdown="1">

#### 单轨迹测试时潜变量优化损失

$$
\mathcal{L}_{\mathrm{opt}}=-R(\bm{x},\bm{c})\sum_{t=1}^{T}\log\pi\left(x_t\mid\bm{x}_{<t},\widetilde{\bm{z}}^{(l)},\bm{c}\right)
$$

**符号说明**

- $\mathcal{L}_{\mathrm{opt}}$：每一步测试时优化所最小化的损失。
- $R(\bm{x},\bm{c})$：自验证器给出的离散奖励；正确为0，错误为-1，并在反向传播时视为常量。
- $\bm{x}=(x_1,\ldots,x_T)$：当前贪心生成并在本次梯度计算中固定的长度为T的续写轨迹。
- $\bm{x}_{<t}$：第t个续写词元之前的固定词元前缀。
- $\widetilde{\bm{z}}^{(l)}$：当前使用的前缀潜变量，等于初始前缀表示与可优化偏移之和。
- $\pi(x_t\mid\bm{x}_{<t},\widetilde{\bm{z}}^{(l)},\bm{c})$：模型在给定问题、潜变量和真实历史词元时赋予当前词元的条件概率。

<div class="equation-explanation" markdown="1">

**直观理解**：当答案错误时$R=-1$，该损失等于当前错误轨迹的对数概率总和；最小化它会压低整条错误续写在当前潜变量下的概率。正确时$R=0$且算法直接停止，因此该目标不负责进一步强化已被接受的回答；求和也未按长度归一化。<br>
**原文位置**：附录A.1“Test-Time Optimization”，公式(8)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：GradCuit没有离线训练阶段，也不修改预训练模型参数。其目标是在每个测试实例上，通过最小化$\mathcal{L}_{\mathrm{opt}}$更新$\Delta\bm{z}^{(l)}$：当前词元ID、输入嵌入和标量奖励均从计算图中分离，梯度只从各续写词元的对数概率经过第$l+1$至$M$层回传到潜变量偏移。论文在理论描述中将其写成奖励加权的策略梯度式期望，实际实现则每步只用一条当前生成轨迹进行估计；因此它是基于结果反馈的实例级近似优化，而不是对期望奖励的精确求解。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 中间层前缀潜变量**

GradCuit不在语言模型输出端为前$N$个离散词元分别设置潜变量，而是在第$l$层的连续隐空间优化前缀表示$\widetilde{\bm{z}}^{(l)}$。主实验统一取$l=\lfloor M/2\rfloor$，且仅训练偏移$\Delta\bm{z}^{(l)}$。

> 直观理解：输出端方法必须先把连续状态压成离散词元，后续推理对早期状态的反馈较间接；中间层表示保留了更多连续信息，也让一次修改能通过后续网络影响完整回答。

**2. 因果自注意力梯度通路**

潜变量处于提示表示之后、续写表示之前，并与词元表示共同进入剩余Transformer层。标准因果掩码使任意续写位置$t$可关注所有更早的潜变量位置$i$，从而存在$\nabla_{z_i^{(l)}}\log\pi(x_t\mid\bm{x}_{<t},\bm{z}^{(l)},\bm{c})$。

> 直观理解：每个回答词元都能把自己的概率变化直接归因到每个潜变量，而不是只有与某个潜变量对应的开头词元能够反馈。这就是论文所称的“类电路”梯度流。

**3. 统一自奖励验证器**

被评估的骨干模型自身充当验证器，只接收原问题和抽取出的最终答案；正确映射为$R=0$，错误或无法抽取答案映射为$R=-1$。GradCuit、Self-Reflection、Self-Scored BoN与LatentSeek共享相同验证提示、答案抽取和判定规则。

> 直观理解：验证器提供无需额外奖励模型的停止与优化信号。统一验证协议也减少了方法比较中因奖励机制不同而产生的混淆，但性能仍会受模型自我判错能力限制。

**训练与推理**

完整流程全部发生在推理阶段。首先渲染问题并附加固定前缀，从选定层提取$\bm{z}_0^{(l)}$，令$\Delta\bm{z}^{(l)}=0$，再用初始潜变量贪心生成并由同一骨干模型验证。若最终答案正确则直接返回；否则关闭键值缓存，对当前固定续写执行教师强制前向传播，汇总全部续写词元的对数概率，计算$\mathcal{L}_{\mathrm{opt}}$并对偏移执行一步Adam更新。更新后重新贪心生成完整回答并再次验证，最多进行10次更新；超出预算仍未通过时返回最后一次生成结果。潜变量是问题专属状态，不会跨测试样本积累，也不会形成新的模型检查点。

**复现信息**

主实验对含$M$个解码块的模型取$l=\lfloor M/2\rfloor$；LLaMA-3.2-3B、LLaMA-3.1-8B、Qwen2.5-7B、Qwen2.5-14B和Qwen3-4B对应优化层分别为14、16、14、24和18。潜变量用Adam优化，学习率为$10^{-3}$，$\beta_1=0.9$、$\beta_2=0.999$、$\epsilon=10^{-8}$，不使用权重衰减、梯度裁剪、潜变量范数约束或额外正则化；模型推理与潜状态采用bfloat16。生成批量为1并使用贪心解码，Qwen3-4B的最大续写长度为4096，其余模型为2048；梯度计算关闭键值缓存，而标准位置与因果注意力掩码保持不变。主实验固定随机种子42，每个骨干模型、基准和答案格式组合只报告一次运行，因此结果不包含多次独立运行的不确定性估计。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GPQA-Diamond：面向高难度、专家级科学问答的基准。实验用它检验方法能否处理需要专业知识与多步推理的问题；所给章节未明确报告样本规模、具体评测划分或是否使用完整测试集。
- GSM8K：小学数学应用题基准，答案通常需要经过若干算术推理步骤。实验用它检验方法在结构较清晰、计算链相对短的数学推理任务上的效果；所给章节未明确报告样本规模与评测划分。
- MATH-500：从 MATH 数学问题中形成的 500 题评测集，覆盖更复杂的竞赛数学推理。它主要检验方法在较长推导、符号操作和高难度数学问题上的能力；所给章节未说明具体类别分布。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**答案准确率**

最终输出与数据集标准答案一致的样本比例。论文分别在五个指令微调模型、三个基准和两种答案格式上报告准确率，并进一步计算跨设置平均值。 （越高越好，因为它表示正确解决问题的比例更大；但该指标不能单独说明推理文本是否忠实，也不能区分提升来自知识、推理还是答案格式遵循。）

</div>
<div class="metric-item" markdown="1">

**跨学习率准确率标准差**

在七种学习率设置下，准确率随学习率变化的离散程度，用于衡量测试时潜状态优化对超参数的敏感性。 （越低越好，因为较小的标准差表示更换学习率时性能波动更小；不过它必须结合平均准确率判断，低波动本身不代表性能高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 五个骨干、三个基准和两种答案格式的全部 30 个设置之平均结果

<div class="result-value" markdown="1">

作者报告 GradCuit 的平均准确率为 64.5%，比 CoT 高 6.6 个百分点，比最强竞争方法高 2.4 个百分点。

</div>

这是覆盖面最广的总体证据：直接优化插入的潜状态在多模型、多任务和两种输出约束下具有平均优势，而不是只在单一数据集上取胜。它仍不能证明每个设置都优于所有基线，也不能排除不同方法测试时计算预算不一致的影响；当前节选也没有给出显著性检验或置信区间。

<div class="result-source" markdown="1">

来源：摘要；第 3.2 节 Overall Effectiveness 对表 1 的汇总

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across five instruction-tuned backbones, three reasoning benchmarks, and two answer formats, GradCuit achieves an average accuracy of 64.5%, outperforming chain-of-thought prompting by 6.6 percentage points and the strongest competing method by 2.4 points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### GSM8K，跨五个骨干分别汇总 Boxed 与 JSON 格式

<div class="result-value" markdown="1">

GradCuit 的平均准确率分别为 88.8% 和 84.8%；CoT 分别为 85.4% 和 80.3%，LatentSeek 分别为 86.3% 和 81.0%。因此，GradCuit 相对 CoT 提高 3.4 和 4.5 个百分点，相对 LatentSeek 提高 2.5 和 3.8 个百分点。

</div>

在较结构化的算术推理任务上，两种答案格式都呈现一致优势，说明改进不只是 Boxed 或 JSON 解析规则造成的。这里的平均值跨越不同模型规模，因此反映总体趋势；它不表示每道题都产生了更合理的中间推理，也不能证明潜状态优化减少了推理计算量。

<div class="result-source" markdown="1">

来源：表 1，GSM8K 的 GradCuit 行；比较值来自同表 CoT 与 LatentSeek 行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GradCuit (Ours) 82.5 75.7 86.2 84.5 91.8 82.1 93.3 92.6 90.0 88.9 88.8 84.8

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### MATH-500，跨五个骨干分别汇总 Boxed 与 JSON 格式

<div class="result-value" markdown="1">

GradCuit 的平均准确率分别为 72.0% 和 65.0%，高于 CoT 的 66.1% 和 54.0%，也高于 LatentSeek 的 69.2% 和 56.1%。对应地，GradCuit 相对 CoT 提高 5.9 和 11.0 个百分点，相对 LatentSeek 提高 2.8 和 8.9 个百分点。

</div>

MATH-500 需要更复杂的数学推导，这组结果表明 GradCuit 的优势在高难度数学任务上仍然存在，且 JSON 格式下相对提升更大。该差距可能同时包含推理能力与格式遵循能力的变化；没有错误类型分析时，不能把全部提升都解释为更好的数学推理。

<div class="result-source" markdown="1">

来源：表 1，MATH-500 的 GradCuit 行；比较值来自同表 CoT 与 LatentSeek 行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GradCuit (Ours) 53.6 47.4 57.4 53.6 77.2 68.6 80.2 68.6 91.8 86.8 72.0 65.0

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

- CoT：标准思维链提示，让模型用离散文本显式展开推理。它是最基本且成本较低的参照，用于判断优化连续潜状态是否比直接生成推理过程更有效。
- Self-Consistency：采样多条推理轨迹并聚合答案。它代表通过增加测试时采样量获得性能提升的方法，用于区分 GradCuit 的收益是否只是来自更多候选输出。
- Self-Scored Best-of-$N$（BoN）：生成多个候选，并利用模型自身评分选择较优答案。它代表“采样后重排序”路线，用于比较直接优化内部状态与外部候选筛选的差异；所给章节未明确报告 $N$ 的具体取值。
- LatentSeek：已有的测试时潜变量推理方法，是与 GradCuit 最直接的同类基线。该比较主要检验：把整段续写的奖励梯度直接分配到插入潜状态，是否优于已有潜变量搜索或优化机制。

**实验想回答的问题**

- GradCuit 在不同模型规模、推理任务和答案格式下，是否能稳定提高答案准确率，并优于显式思维链、采样与重排序以及已有测试时潜变量优化方法？
- GradCuit 的收益究竟来自奖励梯度、潜状态更新还是仅仅插入额外前缀；同时，它对优化超参数和潜状态插入层是否具有足够的稳健性？

**实验实现**

实验覆盖五个指令微调骨干：LLaMA-3.2-3B-Instruct、LLaMA-3.1-8B-Instruct、Qwen2.5-7B-Instruct、Qwen2.5-14B-Instruct 和 Qwen3-4B-Instruct-2507。每种方法在 GPQA-Diamond、GSM8K 与 MATH-500 上评测，并使用 Boxed 和 JSON 两种答案格式，因此主表包含 $5\times3\times2=30$ 个“模型—任务—格式”设置。两种格式的设计用于检查收益是否依赖某一种答案提取模板。原文说明完整基线流程和提示词位于附录，但当前节选未提供生成预算、采样温度、Self-Consistency 与 BoN 的候选数、GradCuit 的优化步数、学习率默认值及随机种子，因此无法仅据所给材料判断各方法的推理计算量是否完全匹配。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 去除奖励梯度：用高斯随机方向替代奖励导出的梯度 | 当前节选只给出了该变体的定义，未包含表 3 的完整数值，因此原文未明确报告可核验的准确率变化。摘要补充说明随机游走版本仍可与 LatentSeek 竞争，但没有在所给材料中提供对应分数。 | 该消融隔离“有方向的奖励梯度”是否必要：若完整 GradCuit 明显优于随机方向，说明收益来自把结果反馈正确分配给潜状态，而不只是对连续状态施加扰动；若随机方向也有较强表现，则说明局部探索或增加测试时计算本身也贡献了收益。由于数值缺失，这里不能判断两种机制各自贡献了多少。 | 第 4.1 节 Ablation Study；表 3 数值未包含在当前节选中<br><span class="experiment-evidence">We compare the full GradCuit with three variants: w/o Gradient replaces the reward-derived gradients with Gaussian random directions, w/o Latent Update retains the inserted prefix without updating it, and w/o Inserted Prefix reduces the method to standard CoT.</span> |
| 去除潜状态更新，或进一步去除插入前缀 | 当前节选说明“w/o Latent Update”保留插入前缀但不更新，“w/o Inserted Prefix”退化为标准 CoT；表 3 的结果行被截断，因此原文未明确报告两者相对完整 GradCuit 的数值降幅。 | 这组对照把两个可能来源拆开：前者检验仅增加一段固定潜前缀是否足以带来收益，后者给出不插入潜状态的 CoT 下界。只有当“完整方法”优于“固定前缀”，且“固定前缀”与 CoT 的关系也被报告时，才能判断提升主要来自梯度更新还是结构性增加上下文；当前材料不足以完成这一因果归因。 | 第 4.1 节 Ablation Study；表 3 数值未包含在当前节选中<br><span class="experiment-evidence">We compare the full GradCuit with three variants: w/o Gradient replaces the reward-derived gradients with Gaussian random directions, w/o Latent Update retains the inserted prefix without updating it, and w/o Inserted Prefix reduces the method to standard CoT.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出通过结果反馈直接优化测试时潜变量的 LLM 推理方法，以提升推理准确率、鲁棒性和可解释性。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`141484c4d26ec7b3499f89f6ded29256d60b835446bcee6a9660c5549f551a0f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
