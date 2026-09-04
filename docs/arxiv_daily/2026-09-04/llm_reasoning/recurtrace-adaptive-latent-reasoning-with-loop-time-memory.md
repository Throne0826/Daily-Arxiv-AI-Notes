---
title: "[论文解读] RecurTrace: Adaptive Latent Reasoning with Loop-Time Memory"
description: "[arXiv 2609.03379][LLM Reasoning] RecurTrace利用循环过程中自然产生的历史隐状态作为记忆，并依据额外循环是否仍能降低损失来学习逐样本停止，从而同时缓解潜空间循环推理中的遗忘与固定计算预算问题。"
arxiv_id: "2609.03379"
announcement_date: "2026-09-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:36:36.099587+00:00"
source_sha256: "6ffa26172e3195e3ce09b4fddc900789325d865654421666346955274a2667a2"
tags:
  - "LLM Reasoning"
  - "LLM 效率"
  - "潜在循环推理"
  - "循环时间记忆"
  - "自适应计算"
  - "提前停止"
  - "参数共享 Transformer"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.03379</p>

# RecurTrace: Adaptive Latent Reasoning with Loop-Time Memory

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Yuxiang Wang, Kunyu Feng, Yingda Shen, Haoning Xu, Junyu Wang, Zhizheng Wu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> The Chinese University of Hong Kong, Shenzhen；Tencent Hunyuan；Shenzhen Loop Area Institute；Amphion Technology Co., Ltd</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03379v1) · [PDF 下载](https://arxiv.org/pdf/2609.03379v1) · **关键词** 潜在循环推理, 循环时间记忆, 自适应计算, 提前停止, 参数共享 Transformer<br>


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

RecurTrace利用循环过程中自然产生的历史隐状态作为记忆，并依据额外循环是否仍能降低损失来学习逐样本停止，从而同时缓解潜空间循环推理中的遗忘与固定计算预算问题。

**不用术语来说**：现有循环式语言模型会让同一组中间层反复处理问题，以增加推理深度而不增加模型主体参数或输出更多推理文字；但它每次通常只能接着上一次的结果计算，无法直接回看更早的中间思路，而且所有问题使用相同循环次数。这会使早期有用信息被覆盖，也会让简单题浪费计算、困难题计算不足，甚至因循环过多而性能下降。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 Loop Memory Attention：每个循环层中的当前词元可沿“循环时间轴”读取该词元在先前循环中的层状态，使模型直接复用早期计算；该模块不跨词元位置混合信息，因而不引入对未来词元的泄漏，也不需要独立的外部存储及复杂读写路由。
- 提出由 oracle 蒸馏的逐样本停止机制：先根据不同循环深度下的训练损失确定继续加深是否仍有收益，再用这一实测信号监督停止头；推理时由停止头为每个输入选择循环次数，而不是依赖统一深度、额外计算惩罚或中间置信度代理。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究的是语言模型的潜在推理深度与自适应计算。标准 Transformer 在推理时通常执行固定层数，因此简单问题和困难问题消耗相同计算量；潜在循环方法则重复执行一个参数共享的中间层模块，使模型在不增加参数、不生成额外推理 token 的情况下获得更深的有效计算。本文关注两个基本设定：循环模块能否访问自身较早迭代产生的隐藏状态，以及模型能否根据输入难度决定循环次数。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**潜在循环（latent looping）**

模型重复执行同一个、参数共享的层块，每次迭代都更新隐藏状态，但不把中间推理过程作为文本 token 输出。这样可以增加内部计算深度，同时保持词表、分词器和常规解码流程不变。

</div>
<div class="concept-item" markdown="1">

**参数共享与有效深度**

参数共享意味着不同循环迭代使用同一组层参数，因此增加循环次数不会按比例增加模型参数。有效深度指输入在推理中实际经过的变换次数，循环可以在参数规模不变时提高这一深度。

</div>
<div class="concept-item" markdown="1">

**自适应计算与提前停止**

自适应计算让不同输入使用不同数量的推理步骤：简单输入较早停止，困难输入继续计算。提前停止机制需要一个判定信号，预测当前状态是否还会因增加深度而得到更好的结果。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个预训练语言模型及其可重复执行的中间层块，输入是文本序列，模型输出通常是下一个 token 的概率分布或最终生成文本。设循环迭代产生一系列隐藏状态；普通循环只把上一轮的最终隐藏状态传给下一轮，因而较早轮次的计算可能被覆盖。本文要研究的设置是在冻结基础模型大部分参数的条件下，为循环层加入对历史循环状态的访问，并为每个输入预测应执行的循环次数，从而在不生成额外推理 token 的情况下平衡准确率与推理计算量。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入文本序列或其中的 token 序列。

</div>
<div class="notation-item" markdown="1">

**$h^{(t)}$**

第 $t$ 次循环后的隐藏状态；其中 $t$ 表示循环时间，而非文本位置。

</div>
<div class="notation-item" markdown="1">

**$T$**

某个输入实际执行的循环次数，也就是该输入获得的潜在推理深度。

</div>
<div class="notation-item" markdown="1">

**$p(y\mid x,h^{(T)})$**

模型在执行 $T$ 次循环后，对输出 $y$ 的条件概率分布；它用于生成答案或计算训练损失。

</div>

</div>

**直接相关的工作**

- **Saunshi et al. (2025) 与 Geiping et al. (2025) 的循环深度方法**: 这些工作说明，重复执行参数共享的层块能够提高语言模型的有效推理深度，并在推理任务上取得收益。但普通循环主要传递上一轮输出，不能直接寻址更早轮次的中间状态；本文针对这一信息访问限制。
- **Adaptive Computation Time（ACT，Graves 2016）与 PonderNet（Banino, Balaguer, and Blundell 2021）**: 这类方法根据停止概率、计算惩罚或步数先验决定何时停止，代表了自适应推理计算的典型路线。本文的问题设定不同：停止头由“增加一轮是否仍能降低损失”的 oracle 信号监督，而不是依赖计算惩罚、几何先验或单纯置信度规则。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

Transformer通常为所有输入分配相同层数，但问题难度并不相同。潜空间循环虽然能通过重复一个权重共享的层块增加有效推理深度，且无需增加主体参数、生成额外思维链词元或改变解码流程，却不能保证增加的深度被有效利用。原文以 MathQA 为例指出，固定循环模型在两次循环达到 $54.7\%$，八次循环约为 $53.6\%$，十六次循环降至 $47.5\%$；这说明计算量并非越多越好，实际系统需要既能保存跨循环推理轨迹、又能按输入难度分配深度的机制。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **外部循环记忆**：Frey 等人的方法使用带门控的键值存储，MeSH 使用多槽缓冲区和学习式读写路由，让循环模型把中间信息写入循环块之外的存储，并在后续迭代中取回。
- **自适应计算与提前退出**：ACT 和 PonderNet分别利用计算惩罚或几何先验约束停止行为；CALM依据中间状态的置信度达到阈值后退出；Mixture-of-Recursions则为不同词元分配递归深度，并从头训练相应路由器。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 普通潜空间循环只向下一次迭代传递一个最新隐状态，早期计算必须被压缩进该状态，否则会被后续更新覆盖；已有外部记忆虽可补救，却引入额外参数以及专门学习的读写机制，没有充分利用循环轨迹本身已经形成的历史状态。
- 固定循环深度无法适应样本难度，而既有停止准则与预训练循环模型的需求并不匹配：额外循环惩罚容易使模型过早停止，置信度阈值又可能使其停止过晚。更根本地说，这些信号没有直接回答“下一次循环是否还会改善该样本的目标损失”。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种面向预训练语言模型的统一方案：在保持循环块权重共享、主体参数冻结和自回归因果性的前提下，直接把同一层先前循环的状态变成可访问记忆，并用额外深度的实际收益而非间接代理来学习停止，使单个模型能够同时支持多种测试时计算预算。

</div>
<div markdown="1"><span>核心问题</span>

循环模型能否仅利用自身产生的循环轨迹，一方面让当前迭代回看更早的层状态，另一方面判断继续循环是否仍会降低损失，从而为每个输入自适应选择推理深度，并优于固定深度及现有自适应计算方法？

</div>
<div markdown="1"><span>作者直觉</span>

循环轨迹本身恰好包含两类所需证据：过去各轮的隐状态记录了模型先前算过什么，当前状态随深度变化的收益则反映继续计算是否值得。因此，与其另建外部存储或用“模型是否自信”猜测停止时机，不如让每个词元直接查看自己的历史轨迹，并从不同深度下损失是否继续下降这一可测事实学习停止。两部分具有互补性：记忆使额外循环真正可能带来新收益，停止机制再把这些有益循环分配给需要它们的输入。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

RecurTrace把预训练语言模型的连续三层中间层选为权重共享的“思考块”，在编码器与解码器之间重复执行。给定输入词元，前部层先产生块输入$e$；循环块随后运行至多$T_{\max}$次，每次都可通过输入重注入保持原问题信息，并通过循环记忆注意力读取同一层在先前循环中的状态；轻量停止头在每轮后预测继续概率$p_t$，决定是否达到足够推理深度；最后，后部层和语言模型头把停止时的隐藏状态解码为下一词元分布。新增机制不生成中间推理文本，也不复制循环块参数，因此增加的是按需计算深度而非模型主体规模。
训练时，基础模型参数被冻结，只训练循环相关的记忆、输入注入和停止参数。循环深度$T$按截断的对数正态—泊松分布逐次采样，使同一模型同时学习浅层和深层展开；语言模型损失在采样深度处计算。停止策略不是直接依赖答案对错，而是由一个可访问多个深度损失的训练期“预言机”提供标签：只有当更深循环能把损失降低至少$\delta$时，当前轮才被标为继续。直观上，该方法让模型保留早先的思考痕迹，并把有限计算集中给继续思考确实可能有用的样本。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 前部编码与循环块定位

先用相邻层表示的角距离寻找变化较小、近似固定点的中部区域，再通过行为消融从中选择连续$k=3$层组成循环块$\mathcal{B}=\{s,\ldots,s+k-1\}$。输入经过第$0$至$s-1$层后得到循环块输入$e$。

<div class="method-step__io" markdown="1">

**输入**：输入词元，以及具有$L$个Transformer层的预训练语言模型。<br>
**输出**：固定的循环层集合$\mathcal{B}$与初始隐藏状态$e$。

</div>

**直观理解**：模型前部先把题目编码成内部表示，再把最适合反复加工的一小段中间层当作可重复使用的思考单元。选择中部稳定区域，是为了减少反复执行时对预训练表示的破坏。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 带输入锚定的循环计算

首轮直接执行循环块；当$t>1$时，先按$h\leftarrow h+\alpha\,\mathrm{RMSNorm}(e)$重新注入块输入，其中可学习标量$\alpha$初始化为零。随后依次执行$\mathcal{B}$中的共享层，并保存每一层本轮输出$x_\ell^{(t)}$。

<div class="method-step__io" markdown="1">

**输入**：上一轮循环状态、原始块输入$e$及当前轮编号$t$。<br>
**输出**：当前轮末状态$h$，以及按层组织的新循环轨迹$x_\ell^{(t)}$。

</div>

**直观理解**：多轮加工可能让模型逐渐偏离原题，因此每轮都轻量提醒一次最初输入。零初始化使该通路训练开始时不起作用，从而先保持基础模型原有行为，再逐步学会利用它。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 沿循环时间轴读取历史

在执行层$\ell$前，循环记忆注意力对同一词元位置在不同历史轮次的键和值进行注意力汇聚，并加入可学习的相对循环距离偏置、标量门和逐词元门。所得记忆项以残差形式加入$h$，再由原始层映射得到$x_\ell^{(t)}$。

<div class="method-step__io" markdown="1">

**输入**：层$\ell$上一轮状态$x_\ell^{(t-1)}$，以及该层最近至多$W$轮的记忆$M_\ell^{(t)}$。<br>
**输出**：融合早期循环轨迹的层状态，以及更新后的滑动记忆窗口。

</div>

**直观理解**：普通循环只能看到上一轮结果，早期有用线索可能被覆盖；这里允许当前轮回看最近几轮的同层状态。注意力只跨循环轮次、不跨词元位置，因此不会把未来词元信息泄漏到当前位置。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 难度自适应停止与后部解码

停止头汇聚提示词位置的状态$z_t$并计算$p_t=\sigma(w^\top z_t+b)$；若$t\geq T_{\min}$且$p_t<\tau$则停止，否则继续，直至达到$T_{\max}$。停止后的状态通过第$s+k$至$L-1$层和语言模型头，形成下一词元概率分布。

<div class="method-step__io" markdown="1">

**输入**：当前循环末状态$h$、最低轮数$T_{\min}$、最大预算$T_{\max}$和阈值$\tau$。<br>
**输出**：输入自适应的实际循环深度与下一词元分布。

</div>

**直观理解**：停止头相当于一个检查员：如果当前表示显示继续思考不太可能有收益，就提前结束；较难样本则可消耗更多循环。阈值只在留出数据上选择，不使用测试集调参。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 循环记忆注意力

$$
\begin{aligned} A_{i,j}&=\operatorname{softmax}_{j}\!\left(\frac{Q_i^{\top}K_{i,j}}{\sqrt{d_h}}-\beta_h(t-t_j)\right),\\ \operatorname{LMA}_{\ell}(q,X)&=\gamma\, g\odot\left(\left[\sum_j A_{i,j}V_{i,j}\right]_i W_o\right),\\ g&=\sigma\!\left(\operatorname{MLP}([q,\overline{X}])\right). \end{aligned}
$$

**符号说明**

- $q=x_{\ell}^{(t-1)}$：层$\ell$在上一循环产生的查询状态。
- $X$：由该层最近$m\leq W$个历史循环状态堆叠而成的记忆。
- $Q_i,K_{i,j},V_{i,j}$：词元位置$i$的查询，以及该位置在历史循环槽$j$上的键和值；它们由归一化状态经分头投影得到。
- $A_{i,j}$：当前位置$i$对历史循环槽$j$的注意力权重。
- $d_h$：单个注意力头的维度，用于缩放点积。
- $\beta_h$：第$h$个注意力头的可学习有符号循环距离斜率，初始化为ALiBi取值。
- $t_j$：历史槽$j$中的状态被写入时的循环编号。
- $\gamma$：控制整个记忆支路强度的可学习标量门。
- $g$：由当前查询$q$与记忆均值$\overline{X}$预测的逐词元门。
- $W_o$：把多头聚合结果映射回模型隐藏维度的输出投影。

<div class="equation-explanation" markdown="1">

**直观理解**：第一式综合内容相似度与循环距离来决定应回看哪一轮：点积越大越相关，而距离项允许不同注意力头学习偏好近期或更早状态。第二、三式先汇总历史值，再用全局门和逐词元门控制写回强度，使记忆只在有帮助时影响原模型。<br>
**原文位置**：第3节“Loop Memory Attention”，公式(4)–(5)

</div>

</div>

<div class="equation-block" markdown="1">

#### 深度收益预言机与停止监督

$$
\begin{aligned} y_t&=\mathbb{1}\!\left[\min_{t'>t}\mathcal{L}_{t'}<\mathcal{L}_t-\delta\right],\\ p_t&=\sigma(w^{\top}z_t+b),\\ \mathcal{L}_{\mathrm{halt}}&=-\sum_{t\in\mathcal{P}}\left[y_t\log p_t+(1-y_t)\log(1-p_t)\right]. \end{aligned}
$$

**符号说明**

- $\mathcal{L}_t$：在循环深度$t$处进行解码所得的逐样本语言模型损失。
- $y_t$：预言机给出的继续标签；若某个更深轮次至少带来裕量$\delta$的损失下降，则取$1$，否则取$0$。
- $\delta$：判定更深计算具有实质收益所需的最小损失下降裕量。
- $z_t$：第$t$轮后在提示词位置上汇聚得到的块状态向量。
- $w,b$：停止头的线性权重与偏置。
- $p_t$：停止头预测的继续循环概率。
- $\mathcal{P}$：训练时施加停止监督的一组探测深度。
- $\mathcal{L}_{\mathrm{halt}}$：停止头相对于预言机标签的二元交叉熵；该展开是原文所述训练方式的标准写法。

<div class="equation-explanation" markdown="1">

**直观理解**：预言机不要求下一轮立即更好，而是检查任何更深轮次能否显著降低损失，因此标签表达的是“继续计算是否仍有潜在收益”。停止头学习从当前状态预测该标签；推理时若$p_t<\tau$且已达到最低深度，就无需真正运行未来轮次。<br>
**原文位置**：第3节“Difficulty-adaptive halting”，公式(6)及其后关于二元交叉熵的文字说明

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：主体目标是在随机采样的循环深度$T$处计算标准自回归语言模型损失，使循环块在不同有效深度下都能产生可解码表示；反向传播覆盖完整展开，不采用截断反向传播。停止头另以预言机标签$y_t$为目标最小化二元交叉熵，学习预测额外循环是否能把逐样本损失降低至少$\delta$。原文说明基础模型被冻结，因此优化只更新循环记忆、输入注入、循环相关模块和停止头参数；停止损失与语言模型损失的具体加权系数在给定节选中未明确报告。
随机深度来自截断的对数正态—泊松分布：先以目标额外循环均值$\bar r$和对数空间标准差$\sigma$采样泊松率，再令循环数至少为一并截断到训练上限。该分布让多数训练样本使用较浅展开，同时保留较深长尾；技术作用是让单一参数集合适配多个测试深度，并与基于循环距离的注意力偏置共同支持超出常见训练深度的推理。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 权重共享循环思考块与输入重注入**

连续三层组成循环块，所有轮次复用同一组基础层权重；第$t>1$轮把$\alpha\,\mathrm{RMSNorm}(e)$加入当前状态。$\alpha$采用ReZero式零初始化，因此在初始化且$T=1$时，计算与基础模型一致。

> 直观理解：共享权重让模型获得更大的有效推理深度，却不必为每一轮复制新层；输入重注入则像反复查看题干，防止深层循环遗忘最初条件。

**2. 循环记忆注意力**

每个循环层$\ell$维护$M_\ell^{(t)}=\{x_\ell^{(t')}\mid\max(1,t-W)\leq t'\leq t-1\}$，即最近至多$W$轮的同层输出。查询、键和值经过归一化和多头投影后，仅沿循环时间轴做注意力；每个头使用可学习的有符号距离斜率$\beta_h$，输出再经标量门$\gamma$和逐词元门$g$调制。

> 直观理解：该模块把循环从“只保留最后一步”的链条改为可检索的短期轨迹，使模型能恢复早先形成但后来被覆盖的中间信息。滑动窗口把存储和注意力开销限制为常数，而门控允许简单输入关闭不必要的记忆。

**3. 预言机蒸馏停止头**

训练期在若干探测深度计算逐样本语言模型损失$\mathcal{L}_t$，据此产生是否继续的二元标签$y_t$；停止头以汇聚状态$z_t$预测$p_t$并接受二元交叉熵监督。推理时不再计算未来深度损失，只使用当前状态、阈值$\tau$和深度上下限作决策。

> 直观理解：预言机训练时可以事后比较“现在停”和“再算几轮”哪个损失更低，再把这个判断教给只看当前状态的小型分类器。这样，部署时无需试遍所有深度，也能近似判断额外计算是否值得。

**训练与推理**

训练流程：先确定三层循环块并冻结基础模型；每次前向传播为所有数据并行进程同步采样一个循环深度$T$，完整展开循环，在每层保存最近$W$轮状态并启用输入重注入和循环记忆；在采样深度处计算语言模型损失，并在选定探测深度解码得到$\mathcal{L}_t$，构造$y_t$后训练停止头。由于门控和$\alpha$接近零初始化，新增路径最初近似关闭，模型从预训练行为平滑过渡到使用循环轨迹。
推理流程：输入先经过前部层，随后从$t=1$开始重复循环块；首轮无历史记忆，之后每轮重注入$e$并让各层读取自己的滑动记忆。每轮结束计算$p_t$，达到$T_{\min}$后若$p_t<\tau$则提前停止，否则继续到$T_{\max}$；最后只解码停止时的状态。$\tau$在留出集上选择，原则是在不损失似然的候选中采用平均深度最小者，且不在测试集上调节。

**复现信息**

循环块固定为连续三层：对$28$层的$0.6$B和$1.7$B Qwen3基础模型使用第$12$–$14$层，对$36$层的$4$B和$8$B模型使用第$15$–$17$层。各尺度均冻结基础网络，只训练循环、记忆、输入注入和停止参数；记忆窗口$W=3$，注意力仅沿循环时间轴运行，循环块跨轮权重共享。训练默认循环深度目标均值约为$4$、$\sigma=0.5$、上限为$8$，实现后的平均深度约为$3.9$；完整展开可行的原因是循环块和记忆窗口都较小。数据并行训练中，各进程根据共享随机种子和前向计数器采样相同的$T$，避免不同进程因循环次数不同而失步。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MathQA：自适应停止的核心受控实验使用 Qwen3-1.7B。作者从测试集构造 $8$ 个互不重叠的评测种子，每个包含 $300$ 道题，共 $2400$ 个唯一样本，约覆盖测试集的 $80\%$；停止阈值只在留出数据上选择。该数据集用于比较固定深度、不同停止方法及正确性预言器上限。
- Train-covered reasoning suite：包含 $14$ 个训练分布覆盖的推理任务，例子包括 GSM8K、MATH 和 MathQA。它主要检验循环计算对数学、多跳问答和受控逻辑任务的生成准确率及教师强制负对数似然是否有一致收益。
- Classic suite：包含 ARC、HellaSwag、MMLU 等 $8$ 个通用基准，用于检查加入循环模块后模型的一般能力是否保持或改善，而非只对训练混合中的推理任务过拟合。BIG-Bench Hard 仅作诊断，不作为主要结论依据。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**贪心解码生成准确率**

使用贪心解码生成短答案后，统计最终答案正确的样本比例；它直接衡量模型实际推理和作答能力。 （越高越好，因为正确回答的样本更多。）

</div>
<div class="metric-item" markdown="1">

**教师强制负对数似然（NLL，nats）**

在给定正确历史 token 时计算目标答案的负对数概率；文中的 $\Delta$ NLL 是相对同预算无循环基线的变化。 （越低越好；对于 $\Delta$ NLL，负值表示比基线赋予正确答案更高的概率。）

</div>
<div class="metric-item" markdown="1">

**平均循环次数**

每个样本实际执行循环块的平均次数，是自适应潜在计算量的代理指标；作者用它比较不同停止方法是否在相近计算量下获得更高准确率。 （没有单调的优劣方向；应与准确率联合考察，在准确率相当时更少循环更节省计算，在循环数相当时更高准确率更优。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3-1.7B 上的 MathQA 自适应停止受控比较

<div class="result-value" markdown="1">

RecurTrace 取得 $56.9\%$ 准确率，标准差为 $0.41$ 个百分点，平均执行 $2.04$ 次循环；在几乎匹配最佳固定深度 $T=2$ 的计算量时，准确率高出 $2.2$ 个百分点，而且每个训练种子的精确 McNemar 检验均满足 $p<0.001$。

</div>

作者据此主张，停止头不是单纯多花计算，而是把额外深度分配给更可能从中受益的样本。两循环下限负责防止模型退化为统一的一循环，停止头再决定哪些样本需要继续。该结论严格支持的是同一 1.7B 循环骨干上的 MathQA 设置；它不能单独证明所有任务都适合动态深度，也不能排除不同硬件上循环操作带来的实际延迟差异。

<div class="result-source" markdown="1">

来源：第 4.2 节，Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

It reaches 56.9% accuracy (std 0.41 pp) at a mean of 2.04 loops, outperforming the best fixed depth (T = 2) by 2.2 points at matched compute. The exact McNemar test confirms this gain for every training seed (p < 0.001, Appendix E).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 不同模型规模上的同预算生成评测

<div class="result-value" markdown="1">

与同预算微调基线相比，RecurTrace 在 0.6B、1.7B、4B 和 8B 四个规模上均提高生成准确率；增益随规模由 $0.6$ 个百分点扩大到 $3.4$ 个百分点。

</div>

作者的结果表明，循环记忆并非只在单一小模型上有效，而且较大模型可能更能利用新增的潜在深度。这里的“同预算”指训练步数、token、数据和硬件受控，并不等于推理墙钟时间完全相同；所给节选也没有列出每个规模、每项任务的完整分数，因此增长趋势仍需结合原表复核。

<div class="result-source" markdown="1">

来源：摘要；完整分规模结果表在所给节选中未展示

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Finally, RecurTrace improves generation accuracy over same-budget fine-tuned baselines at 0.6B, 1.7B, 4B, and 8B, with the gain growing with model size from 0.6 to 3.4 points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### MathQA 上不同停止机制与预言器上限的比较

<div class="result-value" markdown="1">

CALM 以平均 $5.6$ 次循环得到 $54.1\%$；LoopUS-Conf 以 $3.2$ 次循环得到 $55.3\%$；TaH-Mismatch 以 $2.1$ 次循环得到 $55.7\%$；RecurTrace 以约 $2.0$ 次循环得到 $56.9\%$。使用贪心答案正确性直接选择深度的理想化预言器可达 $61.0\%$，而最佳固定深度为 $54.7\%$。

</div>

结果区分了“会停止”和“知道何时继续”两件事：CALM 使用更多循环却更不准确，说明置信度并不可靠地代表额外深度的边际收益；TaH-Mismatch 的计算量接近 RecurTrace，但 token 不匹配无法区分“继续算可能改对”和“样本本身很难”。正确性预言器不是可部署方法，而是展示按样本选深度仍有剩余空间；RecurTrace 只实现了这一上限的一部分。

<div class="result-source" markdown="1">

来源：第 4.2 节，Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

CALM spends 5.6 loops but reaches only 54.1%. Two recent baselines narrow the gap. LoopUS-Conf, a learned confidence head with monotonicity training, reaches 55.3% at 3.2 loops, while TaH-Mismatch, which distills an oracle based on token mismatch, reaches 55.7% at 2.1 loops. Oracle supervision based on loss improvement lets RecurTrace surpass both with 56.9% at 2.0 loops. A correctness oracle that assigns each item the depth at which its greedy answer is correct reaches 61.0%. RecurTrace therefore lies between the best fixed depth (54.7%) and this ceiling, closing about one third of the 6.3 point gap.

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

- 无循环、全参数微调基线：在相同训练步数、数据、token 数和硬件预算下微调整个模型。它检验 RecurTrace 的收益是否超过常规微调；由于 RecurTrace 最多只训练约 $2.2\%$ 的新增参数，若存在预算偏差，反而更有利于该基线。
- 固定循环深度与无记忆 plain looping（即 ETD）：前者给所有样本相同循环次数，用于判断自适应分配深度是否必要；后者重复同一中间层块但不能直接读取更早循环状态，用于隔离 Loop Memory Attention 的作用。
- ACT、PonderNet 与 CALM：ACT 和 PonderNet 分别利用期望深度惩罚与几何先验鼓励提前停止；CALM 根据预测置信度提前退出。它们代表常见的惩罚式或置信度式动态计算方法，可测试这些方法在冻结骨干、后置训练停止器时是否适用。
- LoopUS-Conf 与 TaH-Mismatch：前者训练带单调性目标的置信度头，后者蒸馏基于答案 token 不匹配的预言器；二者是更强、也更接近 RecurTrace 设置的近期自适应循环基线。

**实验想回答的问题**

- 在相同循环骨干和近似计算量下，基于损失改善预言器训练的自适应停止策略，能否优于最佳固定循环深度，并避免过早停止或无效增加循环？
- 性能提升究竟来自额外循环深度、增加的参数容量，还是来自可访问历史循环状态的 Loop Memory Attention；这种机制在不同模型规模和不同任务结构上是否稳定有效？

**实验实现**

实验覆盖 Qwen3 的 0.6B、1.7B、4B 和 8B 四种规模。作者从预训练检查点出发，冻结基础模型权重，只训练循环块、记忆、注入和停止相关参数；训练数据约含 $115$ 万个直接作答样本。所有规模各运行 $3$ 个训练种子，改变循环模块初始化和数据顺序。生成评测采用贪心解码，似然评测采用教师强制 NLL；由于目标是短最终答案，增加循环只增加隐空间中的计算，不增加输出 token。MathQA 自适应停止实验还在 $8$ 个互斥评测子集上估计方差，并用精确 McNemar 检验比较配对预测。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 1.7B、固定两循环下移除 Loop Memory Attention，仅保留 plain looping | 在 MathQA 上，加入记忆将准确率从 $52.4\%$ 提高到 $54.7\%$，增加 $2.3$ 个百分点；在 classic suite 上则从 $64.0\%$ 提高到 $66.4\%$，增加 $2.4$ 个百分点。 | 该对照保持循环深度和冻结基础模型的设置不变，主要隔离“能否读取更早循环状态”的影响。因此它比单独比较无循环模型更能说明收益来自记忆机制，而非仅来自重复执行网络。classic suite 中 plain looping 低于全参数微调基线的 $64.5\%$，而加入记忆后才超过基线，也削弱了“冻结骨干自然保留通用能力”这一替代解释。 | 第 5.1 节，Table 5<br><span class="experiment-evidence">At 1.7B, memory raises accuracy over plain looping by 2.3 points on MathQA and 2.4 points on the classic suite. Freezing the base is not what earns the classic-suite gain, since plain looping freezes the same base yet reaches only 64.0%, below the fine-tuned baseline’s 64.5%, and only memory lifts it to 66.4%.</span> |
| 超过八循环训练上限的合成任务结构对照 | 在指针追踪任务中，plain looping 比记忆模型高 $4.7$ 个百分点；在符号状态跟踪和算术任务中，记忆模型分别高 $17.7$ 和 $16.7$ 个百分点。 | 这项消融检验记忆是否对所有递归任务一概有利。指针追踪每一步只需当前符号，旧状态可能成为干扰；状态跟踪和算术则必须保留中间结果，因而历史循环状态价值更大。结果支持记忆的收益来自任务对持久状态的需求，而不是无条件增加容量或注意力。作者进一步将兼容两类任务的能力归因于逐 token 门控，但该因果解释仍需更直接的门控行为分析验证。 | 第 5.1 节，Table 5 最后三行<br><span class="experiment-evidence">Plain looping leads by 4.7 points on pointer chasing, where past states are unnecessary. Memory instead leads by 17.7 points on symbolic state tracking and 16.7 points on arithmetic, where state must be preserved.</span> |

**定性案例**

- 任务结构诊断可视为一个机制案例：指针追踪只需沿映射读取当前符号，历史状态并非必要；符号状态跟踪与算术必须持续保存中间状态。记忆模型只在后两类任务上大幅领先，说明 Loop Memory Attention 更像可选择调用的“草稿记录”，而不是对每种问题都有效的额外上下文。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该工作通过循环时间记忆和自适应停机扩展语言模型的潜在推理深度，并在匹配计算预算下提升推理效率。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`6ffa26172e3195e3ce09b4fddc900789325d865654421666346955274a2667a2`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
