---
title: "[论文解读] Interpretable Adaptive Sampling for LLM Test-Time Scaling"
description: "[arXiv 2608.03961][LLM 效率] 本文研究如何用可解释的模糊控制器，依据每个提示的难度与不确定性动态分配候选答案采样数，从而在尽量保持全预算准确率的同时降低平均推理计算量。"
arxiv_id: "2608.03961"
announcement_date: "2026-08-05"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:38:08.935637+00:00"
source_sha256: "eff52c5c38e2b159d30b792f84e3c96787395a1ee8ae6e09d72b5a69236ecf4e"
tags:
  - "LLM 效率"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "测试时扩展"
  - "自适应采样"
  - "模糊控制"
  - "推理计算分配"
  - "可解释性"
  - "自洽性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2608.03961</p>

# Interpretable Adaptive Sampling for LLM Test-Time Scaling

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Mobina Kashaniyan, Ali Jannesari</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Iowa State University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03961v1) · [PDF 下载](https://arxiv.org/pdf/2608.03961v1) · **关键词** 大语言模型, 测试时扩展, 自适应采样, 模糊控制, 推理计算分配, 可解释性, 自洽性<br>


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

本文研究如何用可解释的模糊控制器，依据每个提示的难度与不确定性动态分配候选答案采样数，从而在尽量保持全预算准确率的同时降低平均推理计算量。

**不用术语来说**：让大语言模型为同一道题生成多个答案并从中选择，通常能提高答题表现，但简单题和难题若一律生成相同数量的答案，就会在简单题上浪费计算，也可能无法充分照顾难题；同时，系统往往不能清楚说明某道题为何获得特定数量的采样，因此难以审查、调试和在有限资源下部署。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出分层模糊控制器，将提示复杂度、模型置信度、熵、提示类型、预期答案长度及轻量历史表现等人可理解信号映射为逐提示采样预算，为固定预算或黑盒分配策略提供透明的替代方案。
- 设计公平对齐的评估思路：匹配解码设置、控制答案选择器，并让自适应方法只改变候选答案数量，以区分预算策略本身与答案选择机制带来的收益。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型的测试时扩展研究：在不更新模型参数的前提下，推理阶段为同一提示生成多个候选答案，再通过投票、重排或评分选出最终答案。增加候选数通常有助于复杂推理，但也会提高延迟与计算成本；常见的固定预算让难题和易题都生成相同数量的候选，既可能浪费易题上的计算，也可能无法充分支持难题。本文因此把推理计算分配视为一个可解释的逐提示决策问题：依据提示复杂度、模型置信度和熵等可检查信号，为不同提示分配不同采样预算，同时在匹配解码设置并控制答案选择器的条件下考察准确率与平均采样量之间的权衡。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试时扩展（test-time scaling）**

模型参数保持不变，但在回答时投入更多计算，例如生成多条推理路径或多个候选答案，再聚合这些结果。其目标是用额外推理成本换取更高的回答准确率。

</div>
<div class="concept-item" markdown="1">

**自洽性与候选聚合**

自洽性对同一问题进行多次随机采样，并通常选择出现最频繁的最终答案；更一般的候选聚合还可采用评分或重排。它依赖多个候选之间的一致性或质量差异来降低单次生成的不稳定性。

</div>
<div class="concept-item" markdown="1">

**模糊控制器（fuzzy controller）**

模糊控制器用“复杂度高”“置信度低”等可读条件及规则，把多个连续或类别信号映射为控制输出，而不是只使用难以审计的黑箱策略。本文以该输出决定每个提示应生成多少个候选，使预算分配的依据可以被检查。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个待回答的提示以及可从提示或模型行为获得的轻量信号，包括估计复杂度、置信度、熵、提示类型、预期答案长度和历史表现。系统需要为每个提示确定一个不超过全预算的整数采样数，按统一的解码配置生成相应数量的候选答案，再由受控的答案选择机制输出单个最终答案；研究假设额外采样能够改善部分问题，但其边际收益会随问题难度和不确定性变化。核心评价问题是：相较于固定的 best-of-$N$ 或全预算采样，可解释的逐提示预算控制能否减少平均候选数，同时保留大部分准确率；公平比较时应匹配解码设置并控制选择器，使方法间的主要差异仅来自候选数量。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$N$**

固定预算方法为每个提示生成的候选答案数量；在 best-of-$N$ 中，从这 $N$ 个候选中选择最终答案。

</div>

</div>

**直接相关的工作**

- **Self-consistency**: 该方法通过采样多条推理路径并选择最常见的最终答案，构成本文多候选测试时扩展的直接基础；但原文所述标准形式未按提示难度自适应分配采样预算。
- **Huang et al. 的 self-calibrated confidence 方法**: 该工作利用自校准置信度提高测试时扩展效率，与本文的自适应计算分配最接近；本文进一步强调由多种人类可读信号和显式模糊规则形成可审计的预算决策，并要求在选择器受控的公平协议下比较。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

测试时扩展通过生成并聚合多个候选答案来增强大语言模型推理，但实际部署受到推理成本限制。不同提示的难度和模型不确定性差异很大，若每题采用相同采样预算，计算资源便无法投向最需要额外尝试的实例；此外，安全审查和调试还要求系统能够解释资源分配依据。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **固定预算测试时扩展**：对所有提示统一生成固定数量的候选答案，再通过投票或重排序得到最终答案；也可统一调整温度、输出长度等解码参数，以增加推理时计算而不修改模型权重。
- **学习式重排序器或策略模型**：利用学习得到的模型对候选答案进行排序，或决定如何分配推理资源，借助数据驱动的决策改善生成与选择过程。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 固定预算忽略题目难度与不确定性的差异，因而可能在容易实例上浪费候选生成成本，同时仍对困难实例投入不足。
- 学习式重排序器或策略模型的资源分配决策通常不易审计；而且若评估没有控制答案选择器，就难以判断性能变化究竟来自预算分配还是更强的选择机制。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作尚缺少一种同时满足三项要求的逐提示预算机制：能够根据信号自适应增减采样数、能以人可理解的规则说明分配原因，并能在控制解码与答案选择条件下验证其准确率—计算量权衡。作者也承认，手工设计规则未必适用于所有模型和数据集，且预算优化无法弥补答案选择器未选中已有正确候选的问题。

</div>
<div markdown="1"><span>核心问题</span>

一个可解释的控制器能否为每个提示分配测试时样本数，使大语言模型在平均使用更少样本的情况下，保留全预算采样的大部分准确率？

</div>
<div markdown="1"><span>作者直觉</span>

若提示较简单或模型对答案较有把握，少量候选通常已经足够；若提示复杂、预测熵较高或置信度较低，则增加候选更可能覆盖正确解。模糊控制适合把“较难”“较不确定”等连续且边界不清的信号组合成人可检查的规则，再输出平滑的预算尺度，因此可避免僵硬阈值，又比黑盒策略更容易说明每次分配的原因。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把测试时扩展建模为逐题计算分配：给定提示词 $x$，系统先从提示词本身和一次短草稿中提取复杂度、置信度、熵、预期答案长度等信号，再由分层模糊控制器输出计算尺度 $s$ 与控制器不确定度 $u$。经不确定度修正后，尺度被映射为整数采样预算 $N(x)$；大语言模型据此生成多个候选答案，最后用固定的自确定性排序与 Borda 聚合器返回答案。输入是一条提示词，输出既包括最终答案，也包括可审计的预算决策及其信号依据。

技术上的关键不是训练一个追求最高拟合度的神经预算策略，而是用模糊隶属度表达“部分容易、部分困难”等连续状态。通俗地说，系统像一名可解释的调度员：先看题目是否复杂，再看模型试答时是否犹豫；简单且有把握的题少做几次，困难或不确定的题多做几次，并能说明是哪些因素促成了该分配。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提示侧难度表征

计算归一化长度、词汇丰富度、句子数、数学符号密度、语义歧义、语言复杂度和推理深度，并与标点、数字、大写及多句结构构成的表层启发式分数融合；同时判断提示类型 $\tau$ 和预期答案长度 $\lambda$。

<div class="method-step__io" markdown="1">

**输入**：原始提示词 $x$。<br>
**输出**：综合复杂度 $c$、提示类型 $\tau$、预期答案长度 $\lambda$，以及细分属性 $a_{\mathrm{sem}}$、$a_{\mathrm{ling}}$、$a_{\mathrm{rea}}$。

</div>

**直观理解**：这一步先在不进行完整多次生成的情况下估计题目有多难。表层特征便宜而稳定，语义和推理特征则用于区分“文字长但简单”和“文字短但推理密集”的提示。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 草稿生成与模型侧不确定性估计

用草稿中各词元概率的几何平均计算置信度 $\gamma$，并计算归一化熵 $\eta$；系统还从按复杂度和提示类型粗粒度分桶的历史缓存中读取相似提示的先验表现 $\pi$。

<div class="method-step__io" markdown="1">

**输入**：提示词 $x$、模型生成的一次短草稿及其逐词元概率。<br>
**输出**：完整控制特征 $\phi=(c,\gamma,\tau,\lambda,\eta,\pi,a_{\mathrm{sem}},a_{\mathrm{ling}},a_{\mathrm{rea}})$。

</div>

**直观理解**：提示侧特征描述题目看起来有多难，草稿概率则反映当前模型实际有多犹豫。历史缓存提供缓慢变化的经验信号，避免只依据单次草稿作决定。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分层模糊预算控制

第一层将复杂度 $c$ 与置信度 $\gamma$ 映射到低、中、高等重叠模糊区域，并通过规则库得到粗略计算等级；第二层利用熵、答案长度、提示类型、历史表现及三类复杂度属性，以 Type-2 模糊区间细化结果，随后解模糊得到尺度 $s$ 和区间宽度对应的不确定度 $u$。

<div class="method-step__io" markdown="1">

**输入**：归一化到 $[0,1]$ 的特征向量 $\phi$。<br>
**输出**：计算尺度 $s\in[0,1]$ 与控制器不确定度 $u\in[0,1]$，以及可供审计的规则激活和细化依据。

</div>

**直观理解**：一道题不必被硬判成“容易”或“困难”，而可同时部分属于多个等级，因此预算会随难度平滑变化。多个辅助信号意见冲突时，区间会更宽，表示控制器对自己的预算判断也不够确定。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 动态预算映射与候选生成

先按 $s'=\mathrm{clamp}(s+0.2u)$ 对不确定决策保守加码，再线性映射并舍入为 $N(x)$；若 $c>0.6$ 且 $N_{\max}\geq6$，还施加 $N(x)\geq\min(6,N_{\max})$ 的困难题预算下限，随后生成 $N(x)$ 个候选。

<div class="method-step__io" markdown="1">

**输入**：尺度 $s$、控制器不确定度 $u$、最大预算 $N_{\max}$ 和提示词 $x$。<br>
**输出**：整数预算 $N(x)$ 及对应的候选答案集合。

</div>

**直观理解**：控制器越不确定，系统越倾向于多采样一些，以降低过早节省计算造成的风险。明显困难的题还有最低预算保护，防止连续映射偶然给出过小样本数。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 草稿序列置信度

$$
\gamma=\mathrm{clamp}\left(\exp\left(\frac{1}{L}\sum_{i=1}^{L}\log p_i\right)\right)
$$

**符号说明**

- $\gamma$：归一化后的草稿置信度，值越大表示模型对已生成词元赋予的概率整体越高
- $L$：短草稿包含的词元数量
- $p_i$：模型为草稿中第 i 个实际生成词元分配的概率
- $\mathrm{clamp}$：把结果截断到控制器要求的区间，本文所有控制器输入均位于零到一之间

<div class="equation-explanation" markdown="1">

**直观理解**：该式等价于对整段草稿的逐词元概率取几何平均，因而不会让较长草稿仅因概率连乘而必然得到极小值。它提供的是模型对自身生成过程的内部把握程度，而不是答案正确率；因此方法还结合熵和提示复杂度，避免将高置信度直接当成正确。<br>
**原文位置**：第3.1节，公式(4)

</div>

</div>

<div class="equation-block" markdown="1">

#### 不确定度修正与整数预算映射

$$
s^{\prime}=\mathrm{clamp}(s+\alpha u),\quad \alpha=0.2;\qquad N(x)=\max\left(1,\mathrm{round}\left(1+s^{\prime}(N_{\max}-1)\right)\right)
$$

**符号说明**

- $s$：模糊控制器解模糊后得到的初始计算尺度
- $u$：由 Type-2 模糊输出区间平均宽度得到的控制器不确定度
- $\alpha$：不确定度加码系数，原文固定为零点二
- $s^{\prime}$：经过不确定度修正并截断后的计算尺度
- $N(x)$：为提示词 x 分配的整数候选采样数
- $N_{\max}$：实验允许的最大采样预算
- $\mathrm{round}$：将连续预算映射到最近的整数

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分在控制器自身不确定时把尺度向上推，体现“拿不准就多看几个候选”的风险控制；第二部分把零到一的连续尺度线性映射到从一个样本到最大预算的整数范围。这样，模糊规则的连续输出最终能直接控制实际生成次数。<br>
**原文位置**：第3.3节，公式(6)与公式(7)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：所给章节没有定义需要反向传播优化的损失函数，也没有报告对模糊控制器进行监督训练或强化学习。该方法是规则驱动的推理时策略：特征权重、隶属区域、规则细化、系数 $\alpha=0.2$ 及困难题预算下限共同决定分配；历史缓存仅保存相似提示上的缓慢变化表现估计 $\pi$，不能据此推断存在端到端参数训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 混合难度与不确定性信号提取器**

提示侧综合复杂度由轻量 NLP 特征与表层启发式按 $0.6$ 和 $0.4$ 加权；模型侧信号来自短草稿的词元置信度与归一化熵，并辅以提示类型、预期长度和历史表现。所有控制器输入均归一化到 $[0,1]$，以便共享模糊隶属函数和规则尺度。

> 直观理解：只看题目长度会误判短而难的数学题，只看模型置信度又可能受到错误自信影响。把题目特征、模型反应和历史经验结合起来，是为了用互补证据决定预算。

**2. 分层 Type-2 模糊控制器**

第一层以三角形和梯形隶属函数表示复杂度与置信度的低、中、高及极端区域，通过规则激活很低到很高的计算标签；第二层把辅助信号编码为 Type-2 区间修正，按第一层激活强度加权区间中心完成解模糊，并以平均区间宽度形成 $u$。

> 直观理解：模糊控制器的优势不是理论表达能力超过学习策略，而是每次分配都能追溯到具体信号和规则。Type-2 区间进一步表示“规则本身有多拿不准”，从而在信号冲突时保守增加计算。

**3. 自确定性排序与 Borda 答案聚合器**

候选先按词元概率导出的自确定性排序，再对抽取出的答案字符串进行 Borda 计分，最高累计分对应最终输出。该选择器在比较中保持固定，使动态预算的作用与答案选择策略尽量解耦。

> 直观理解：如果只生成更多候选却不能可靠聚合，额外样本甚至可能降低准确率。该模块把候选质量排序和答案间的一致支持结合起来，避免简单地选择最后一次或随机一次生成。

**训练与推理**

训练阶段方面，原文节选未提出额外模型微调或预算策略训练流程；底层大语言模型作为既有生成器使用，模糊控制器也被描述为透明的策略类而非学习得到的神经策略。历史缓存按复杂度和提示类型的粗粒度分桶记录先前表现，但其初始化、更新公式及是否在评测前冻结，原文节选未明确报告。

推理时，对每个提示词 $x$ 先提取提示侧特征并生成一次短草稿，以获得 $\gamma$ 和 $\eta$；随后将完整特征 $\phi$ 输入两阶段模糊控制器，得到 $s$ 与 $u$。系统计算修正尺度 $s'$ 和预算 $N(x)$，必要时应用困难题下限，再生成规定数量的候选；候选经同一自确定性排序和 Borda 聚合器处理后输出最终答案。需要公平解释的一点是，短草稿本身也消耗推理计算，但所给方法章节没有说明它是否计入表中平均预算。

**复现信息**

复现预算逻辑所需的核心设定包括：所有控制输入归一化到 $[0,1]$；提示长度项按词数除以 $60$ 后截断；综合复杂度以 $c=\mathrm{clamp}(0.6c_{\mathrm{NLP}}+0.4h)$ 融合 NLP 分数和表层启发式；模糊系统同时采用三角形隶属函数描述渐变区域、梯形隶属函数描述极低和极高区域；预算不确定度系数为 $0.2$。当 $c>0.6$ 且 $N_{\max}\geq6$ 时，预算至少为 $\min(6,N_{\max})$。

为公平理解结果，还应固定底层模型的解码设置和最终选择器，因为候选多样性及聚合能力都会影响多采样收益。所给节选没有列出隶属函数的精确断点、完整模糊规则表、归一化熵公式、历史缓存更新规则、短草稿长度、采样温度或 Borda 计分细节，因此仅凭当前材料无法逐项完全复现这些部分；不能自行补设这些值。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：包含 $1{,}319$ 道测试题的小学数学文字题数据集，用于检验多步算术推理；它同时测试控制器能否在一个可能仍需要充分候选聚合的任务上安全削减预算。
- MATH：实验使用 $1{,}319$ 道题的子集，题目比 GSM8K 更强调高难度数学推理；其主要作用是检验自适应分配能否在题目难度差异较大的情况下节省更多样本。
- SciQ：包含 $1{,}000$ 个测试提示的短篇事实科学问答数据集，用于补充数学推理任务，考察方法能否迁移到答案更短、推理负担通常较低的事实型问答；给定节选未提供表 2 的具体结果。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**精确匹配准确率（exact-match accuracy）**

比较抽取出的最终答案与标准答案是否完全一致，并对所有题目的正确指示取平均；它测量最终任务正确性，但不会给部分正确的推导过程计分。 （越高越好，因为更高数值表示完全答对的测试题比例更大。）

</div>
<div class="metric-item" markdown="1">

**平均样本数 $\bar{N}$**

每个提示实际生成的候选答案数量的平均值，论文将其作为推理计算量的代理指标；它反映采样开销，但不是硬件时间、能耗或 token 数的直接测量。 （在准确率相近的前提下越低越好，因为较少候选意味着较低的平均推理采样开销。）

</div>
<div class="metric-item" markdown="1">

**样本削减率（sample reduction）**

自适应方法相对同选择器、固定 $N=8$ 基线减少的平均采样比例，用来呈现准确率—计算量折中。 （在不显著损害准确率的条件下越高越好；脱离准确率单独追求更高削减率没有意义。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 选择器匹配的 MATH 主实验：自适应预算对比固定 $N=8$ 的 self-certainty+Borda，分别使用 Phi-3-mini 和 Qwen2.5-1.5B。

<div class="result-value" markdown="1">

Phi-3-mini 的准确率由 $0.585$ 降至 $0.578$，差值为 $-0.007$，同时减少 $10.8\%$ 的样本；Qwen2.5-1.5B 的准确率由 $0.315$ 降至 $0.297$，差值为 $-0.018$，同时减少 $14.5\%$ 的样本。

</div>

作者据此主张控制器在 MATH 上实现了较明确的准确率—计算量折中：它不是在准确率上击败满预算，而是用较小准确率损失换取两位数比例的样本节省。分析上，这支持“可削减部分冗余采样”，但没有证明削减在统计上无损，因为论文明确指出置信区间并非逐题配对检验。

<div class="result-source" markdown="1">

来源：第 5.1 节，表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On MATH, Adaptive uses fewer samples with only a small accuracy drop: 10.8% fewer samples for Phi-3-mini and 14.5% fewer samples for Qwen2.5-1.5B.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 选择器匹配的 GSM8K 主实验：自适应预算对比固定 $N=8$ 的 self-certainty+Borda。

<div class="result-value" markdown="1">

Phi-3-mini 的固定与自适应准确率分别为 $0.717$ 和 $0.715$，自适应减少 $1.4\%$ 样本；Qwen2.5-1.5B 的准确率由 $0.459$ 变为 $0.464$，即提高 $0.005$，并减少 $3.9\%$ 样本。

</div>

GSM8K 上的节省幅度明显小于 MATH，说明控制器更常保留接近满额的候选池。Qwen 组合出现了轻微的准确率上升，但这不应被解释为自适应预算稳定优于满预算：变化很小，而且节选未给出配对显著性检验。更稳妥的结论是，控制器在该设置下以少量采样节省维持了近似准确率。

<div class="result-source" markdown="1">

来源：第 5.1 节，表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

With Qwen2.5-1.5B on GSM8K, Adaptive is slightly more accurate than fixed N=8 while using 3.9% fewer samples.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 选择器敏感性实验：Phi-3-mini 在 MATH 上采用多数投票，对比固定 $N=8$ 与自适应预算。

<div class="result-value" markdown="1">

自适应多数投票达到 $0.5853$ 准确率和 $6.90$ 个平均样本，样本削减率为 $13.7\%$；固定 $N=8$ 多数投票的准确率为 $0.5739$。该自适应组合也是表 7 所列 Phi-3-mini MATH 设置中的最高结果。

</div>

该结果表明预算策略的效果与最终选择器相互作用：多数投票可能比 self-certainty+Borda 更适合这一模型—数据集组合。它支持自适应采样并非只能配合一种选择器，但不能推出所有模型上都成立；同一表中 Qwen2.5-1.5B 的 MATH 结果仍由固定 $N=8$ 方法领先。

<div class="result-source" markdown="1">

来源：附录 H，表 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Adaptive majority nearly matches fixed N=8 majority on GSM8K with fewer samples, and gives the best Phi-3-mini MATH result in this sweep.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 计算效率只用平均样本数 $\bar{N}$ 和样本削减率表示，没有报告端到端延迟、生成 token 数、吞吐量、显存或能耗；若不同候选的输出长度差异较大，样本数不一定等价于真实硬件成本。
- 表 1 报告的是各方法各自的边际 Wilson 置信区间，而不是基于同一提示正确性差异的配对检验；加之组件消融呈现混合效果，现有证据支持可控折中，但不足以断言小幅准确率变化具有统计显著性，或每个人工设计信号都能跨模型、跨数据集稳定贡献。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Best-of-$N$，其中 $N\in\{1,3,5\}$：固定生成若干候选再选择答案，是最直接的测试时扩展基线；它检验单纯增加候选数量是否足以提升准确率。
- 受 Snell 等工作启发的 compute-optimal 公式分配规则：作为计算感知型基线，用于比较可解释模糊控制器与预设公式预算策略，而不只是与固定预算比较。
- 固定 $N=8$ 的 self-certainty 选择：按照模型对候选答案的自我确定程度进行选择，用于检验仅依赖候选级置信信号是否能够有效利用较大的采样池。
- 固定 $N=8$ 的 self-certainty+Borda，以及相应的多数投票匹配控制：前者与自适应 Borda 版本共享最大预算和答案级选择器，是隔离“预算策略”影响的关键对照；多数投票的固定—自适应配对则用于检查结论是否依赖特定选择器。

**实验想回答的问题**

- 在解码参数和答案选择器受到控制时，自适应控制器能否按题目分配不同的采样预算，并以低于固定满预算 $N=8$ 的平均计算量维持接近的精确匹配准确率？
- 控制器的预算变化是否符合预期机制，以及结论是否对答案选择器敏感：容易或高置信度题目是否获得较少样本，而不同选择器能否有效利用这些候选答案？

**实验实现**

主实验使用 Phi-3-mini-4k-instruct 与 Qwen2.5-1.5B-Instruct。公平对齐协议统一采用温度 $1.0$、top-$p=0.95$ 和最大输出长度 $256$，自适应方法的最大预算为 $N_{\max}=8$。为避免完整系统中的短草稿和随规模调整解码参数造成混杂，主实验关闭草稿阶段并固定所有方法的解码设置，使控制器只改变候选样本数量。表 1 进一步让固定预算与自适应方法共享 self-certainty+Borda 选择器，并报告 $95\%$ Wilson 置信区间；不过这些是边际区间，若要严格判断逐题差异是否显著，仍需配对的逐题正确性记录。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Phi-3-mini 的固定预算上限消融：在 GSM8K 和 MATH 上比较自适应方法与固定 $N\in\{1,2,3,5,8\}$。 | GSM8K 上，自适应方法以平均 $7.86$ 个样本达到 $0.810$，固定 $N=8$ 为 $0.809$；MATH 上，自适应方法以平均 $7.07$ 个样本达到 $0.570$，固定 $N=8$ 为 $0.574$。固定小预算整体较弱，例如固定 $N=1$ 在 GSM8K 和 MATH 上分别只有 $0.725$ 与 $0.457$。 | 该消融隔离了“自适应分配”与“直接统一缩小预算”的区别。结果说明节省计算不能简单依靠把所有题目都限制在很小的 $N$：选择器需要足够多的候选来利用答案间的一致性。自适应方法接近固定 $N=8$，但并未证明其规则达到最优，只证明保守地按题减样本优于激进的统一低预算。 | 第 6 节，表 3<br><span class="experiment-evidence">On GSM8K, Adaptive reaches 0.810 accuracy with an average of 7.86 samples, compared with 0.809 accuracy for fixed N=8. On MATH, Adaptive reaches 0.570 accuracy with 7.07 samples, compared with 0.574 accuracy for fixed N=8.</span> |
| Phi-3-mini 的控制器组件消融：移除 NLP 特征、题型信号、熵信号、历史缓存、规则自适应或二型不确定性，并将置信度中和。 | 组件效果并不一致：移除熵信号后，MATH 准确率由完整方法的 $0.570$ 提高到 $0.585$，平均样本由 $7.07$ 变为 $7.10$；中和置信度后，MATH 准确率提高到 $0.601$，但平均预算被推至 $8.00$，不再体现采样节省。 | 这一消融检验每个手工信号是否独立必要。结果否定了“所有信号都已优化且不可缺少”的强主张：某些移除反而提高准确率，而置信度中和的提升伴随预算回到满额。因而更合理的解释是，当前模糊控制器提供透明、可调的分配政策，而不是已经学习到全局最优的预算函数。 | 第 6 节，表 4<br><span class="experiment-evidence">For example, removing entropy improves MATH accuracy, and neutralizing confidence also improves MATH accuracy while forcing the average budget to 8.00.</span> |

**定性案例**

- 预算分布图可视为群体层面的机制案例：两个模型在 MATH 上都将更多题目分配到低于 $N=8$ 的预算，而 GSM8K 更集中在满预算附近。直观上，控制器并非机械地对所有输入减样本，而是对其判断不宜削减的 GSM8K 提示保持保守；但节选没有给出具体单题轨迹，因此无法核查某一道题的复杂度、置信度与最终预算是否逐项符合模糊规则。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Proposes adaptive sampling budgets that reduce inference compute for test-time LLM reasoning.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`eff52c5c38e2b159d30b792f84e3c96787395a1ee8ae6e09d72b5a69236ecf4e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
