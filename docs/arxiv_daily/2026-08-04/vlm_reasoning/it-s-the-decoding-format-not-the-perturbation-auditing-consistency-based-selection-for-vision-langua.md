---
title: "[论文解读] It's the Decoding Format, Not the Perturbation: Auditing Consistency-Based Selection for Vision-Language Test-Time Scaling"
description: "[arXiv 2608.01207][VLM Reasoning] 本文通过引入解码格式与推理预算匹配的对照组，审计视觉语言模型测试时扩展中的扰动一致性选择，发现其相对普通多数投票的表面收益主要来自短答案、无思维链的解码格式，而非图像扰动提供的额外视觉依据。"
arxiv_id: "2608.01207"
announcement_date: "2026-08-04"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:02:20.614640+00:00"
source_sha256: "2eda9f5ee62b0ff27903afd305c477408cd20d4b81f4c6dff79276c339c26439"
tags:
  - "VLM Reasoning"
  - "LLM Reasoning"
  - "LLM 其他"
  - "多模态 VLM"
  - "视觉语言模型"
  - "测试时扩展"
  - "多数投票"
  - "扰动一致性"
  - "选择层"
  - "解码格式混杂"
  - "标签保持扰动"
  - "格式匹配对照"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.01207</p>

# It's the Decoding Format, Not the Perturbation: Auditing Consistency-Based Selection for Vision-Language Test-Time Scaling

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Puzhuo Zheng, Hasan Kurban</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Hamad Bin Khalifa University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01207v1) · [PDF 下载](https://arxiv.org/pdf/2608.01207v1) · **关键词** 视觉语言模型, 测试时扩展, 多数投票, 扰动一致性, 选择层, 解码格式混杂, 标签保持扰动, 格式匹配对照<br>


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

本文通过引入解码格式与推理预算匹配的对照组，审计视觉语言模型测试时扩展中的扰动一致性选择，发现其相对普通多数投票的表面收益主要来自短答案、无思维链的解码格式，而非图像扰动提供的额外视觉依据。

**不用术语来说**：视觉语言模型面对图像问题时，可以先生成多个候选答案，再从中选出最终答案；但出现次数最多或模型自称最可信的答案，可能只是符合语言常识的猜测，并不真正依据图像。研究者因而尝试用多个轻微修改后的图像重新询问模型，偏好在这些图像上仍能被重复得到的答案。问题在于，这种方法同时改变了图像和回答形式，因此观察到的提升未必来自图像一致性，也可能只是因为简短、直接回答比长篇推理更适合当前任务。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者识别出一致性选择评测中的“解码格式混杂”：将使用短答案、无思维链采样的扰动选择方法与仅聚合长思维链样本的多数投票比较，无法判断收益究竟来自扰动信号还是回答格式。为隔离两者，论文提出 MatchedCtrl，将同样数量、同样格式的额外样本用于原始图像，使其与 PGS 之间只剩“是否经过图像扰动”这一关键差异。
- 作者在两个开源视觉语言模型和四个自动评分基准的限定范围内给出负面诊断：PGS 相对普通多数投票看似有效，但在格式和预算匹配后没有显示可靠优势；由保真扰动与破坏性扰动得到的稳定性差异虽然具有图像依赖性，却不能预测逐样本选择收益。因此，扰动一致性至多是视觉依赖的部分诊断指标，尚不能单独充当可靠的无标签答案选择信号。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究视觉语言模型（VLM）的测试时扩展：给定图像与问题，模型在推理阶段采样多个候选答案，再通过某种选择规则输出一个最终答案。该范式在大语言模型中通常依赖多数投票或模型自验证，但在视觉任务中，候选答案既可能来自图像证据，也可能只是来自语言先验；由于答案频率、语言化置信度等常用信号并不检查答案是否真正依赖像素，选择层可能无法区分“看图所得的答案”和“脱离图像的自信猜测”。本文聚焦于无需标签、额外训练、模型内部访问或外部验证器的选择层方案，并特别强调：比较不同选择器时，必须同时控制采样预算与解码格式，否则短答案与思维链输出之间的性能差异会被误认为选择机制本身的收益。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试时扩展（test-time scaling）**

模型参数保持不变，但在推理时投入更多计算，例如为同一输入采样 $N$ 个候选解答并从中选择最终答案。其效果不仅取决于候选生成质量，也取决于选择信号能否识别更可能正确的候选。

</div>
<div class="concept-item" markdown="1">

**自一致性与多数投票（self-consistency / majority voting）**

将多个生成结果归一化为答案后，选择出现次数最多的答案，即把频率视为正确性的代理信号。当错误答案受语言先验驱动并高频出现时，这一假设会失效。

</div>
<div class="concept-item" markdown="1">

**标签保持扰动（label-preserving perturbation）**

对图像进行不应改变正确答案的变换，例如面向相关区域的裁剪、背景遮罩以及轻微光度或几何抖动。若模型在这些视图上仍能重新导出某个候选答案，其跨视图稳定性可被用作视觉依赖性的候选诊断信号，但稳定并不必然意味着答案正确或真正基于图像。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个图像—问题对，以及视觉语言模型针对原始图像生成的 $N$ 条长思维链候选及其答案；目标是在不使用真实标签、不训练新模型、也不调用第二个验证网络的条件下，从候选答案中选出最终答案。普通多数投票只统计原始候选的答案频率；扰动落地选择（PGS）还在若干标签保持的图像变换上生成短、无思维链答案，并依据候选在不同视图中被重新导出的稳定程度进行重评分。论文指出该设置存在关键混杂因素：PGS相较于仅使用长思维链的多数投票，不仅引入了图像扰动，也额外引入了短、无思维链的解码格式与计算预算。因此，公平审计需要用MatchedCtrl作为对照：保留相同的原始候选，并花费与PGS相同数量的短答案采样预算，但所有额外采样都使用未扰动的原始图像。这样，PGS与MatchedCtrl之间唯一应被检验的核心差异是扰动视图是否提供了额外选择信息。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

原始视觉输入，即图像；问题文本在任务输入中与该图像配对。

</div>
<div class="notation-item" markdown="1">

**$N$**

针对同一图像—问题对采样的初始推理轨迹或候选解答数量。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{T}$**

标签保持图像扰动的集合；原文示例包括裁剪、背景遮罩以及轻微光度或几何抖动。

</div>
<div class="notation-item" markdown="1">

**$T(x)$**

对原始图像 $x$ 应用某个扰动 $T\in\mathcal{T}$ 后得到的视图。

</div>

</div>

**直接相关的工作**

- **Wu et al. (2026a)**: 该工作报告，在经过强化学习调优的视觉数学模型上，多数投票优于以自验证为核心的选择方法，且自我纠正的“aha moment”没有可靠增益；这为本文关于VLM选择层信号脆弱性的研究背景提供了直接依据。
- **Tong et al. (2026)**: 该工作发现，跨七种VLM的单模型多数投票通常只有有限且依赖思维链的收益，并在输出高度相关时失效，主要从样本多样性解释弱选择效果；本文补充解码格式隔离视角，考察短、无思维链采样是否构成扰动选择器表面增益的主要来源。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

视觉语言模型的测试时扩展需要从多个候选答案中选出较可靠者，但现有选择层通常只观察答案频率、文字化置信度或模型的自我验证结果。这些信号不要求模型重新读取图像，所以一个确有像素依据的答案与一个由语言先验产生、但表达得很自信的猜测可能表现相同。其实际后果是：增加采样预算未必改善视觉推理，甚至可能让占多数的错误常识压过较少但真正依据图像的答案。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **多数投票与模型自我验证**：多数投票从多个推理样本中选择出现频率最高的答案；best-of-$N$ 等自我验证方法则让模型评价候选答案，再选取自认为最优者。两者都假定正确性会反映在答案频率或模型给出的置信判断中。
- **训练式或额外组件式视觉纠错**：一类方法通过强化学习、工具使用课程等训练，让模型学会在必要时重新检查视觉证据；另一类方法在单次生成内部调整对证据区域的注意力，或引入外部验证器、过程奖励模型来给候选答案打分。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 频率、自我验证和文字置信度没有直接检验答案是否依赖图像像素；当语言先验产生的伪路径占多数时，多数投票会稳定地选择错误答案，而输出稳定也不能证明答案具有视觉依据。
- 训练式与额外组件式方法通常需要训练数据和计算资源、模型内部访问、监督信号或第二个已训练网络，因而不适合只有单张消费级 GPU、希望直接在推理阶段改进选择的使用场景；同时，以仅含长思维链样本的多数投票为基线，还会把选择机制收益与解码格式变化混在一起。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种严格受控的评测，能够在不训练新模型、不使用标签或外部验证器的条件下，单独检验“跨标签保持型图像扰动的一致性”是否真的为候选选择提供了超出解码格式与额外采样预算的视觉接地信息。尤其需要一个与扰动方法拥有相同短答案格式和相同推理成本、但只使用原始图像的对照组，否则相对多数投票的提升不能归因于扰动。

</div>
<div markdown="1"><span>核心问题</span>

在候选数量、额外推理预算以及短答案、无思维链的解码格式均受到匹配后，PGS 将候选答案在裁剪、背景遮蔽及轻微光度或几何变化下的可重复性纳入评分，是否能比仅在原始图像上增加同格式采样的 MatchedCtrl 更准确地选择答案？

</div>
<div markdown="1"><span>作者直觉</span>

如果某个答案真正来自图像中的关键证据，那么只要裁剪、遮蔽或轻微抖动没有改变问题的正确标签，模型应能从多个修改后的视图中再次得到该答案；只靠题目措辞或常识猜出的答案则可能缺乏这种跨视图支持。因此，扰动后的重复出现有望充当必须读取图像才能获得的选择信号。不过，要验证这一点，必须把它与“仅仅多采样了一批更短、更直接的答案”区分开：MatchedCtrl 正是用原图上的同格式采样测量后一种效应。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文研究的不是如何训练新的视觉语言模型，而是如何在推理时从同一模型生成的多个候选答案中选出最终答案。给定图像 $x$、问题 $q$ 和视觉语言模型 $p_{\theta}(a\mid x,q)$，方法先在原图上生成 $N$ 条带思维链的候选回答，经 $\mathrm{ans}(\cdot)$ 抽取并规范化最终答案，形成候选集合 $\mathcal{A}$。随后构造 $M$ 个保持真实标签不变的图像扰动 $\mathcal{T}=\{t_1,\ldots,t_M\}$，在每个扰动视图上生成 $K$ 条短答案，并统计每个候选答案能否被模型重新推导出来。Perturbation-Grounded Selection（Pgs）将原图票数与扰动视图上的重推导强度加权相加，输出得分最高的候选；当 $\mathcal{T}=\emptyset$ 或 $\lambda=0$ 时，它严格退化为多数投票。

方法设计的关键并非只比较 Pgs 与普通多数投票，而是设置格式匹配对照 MatchedCtrl。Pgs 将额外的 $MK$ 次短答案生成分配到扰动图像，MatchedCtrl 则把完全相同的 $MK$ 次短答案生成用于原图；二者共享原图上的 $N$ 条思维链候选、短答案解码格式和总预算 $B=N+MK$，只在额外样本是否经过扰动这一点上不同。因此，Pgs 超过普通多数投票可能来自短答案格式或额外生成预算，只有它超过 MatchedCtrl 才能归因于扰动一致性。直观地说，Pgs 先让模型在原图上提出若干答案，再通过多个基本不改变题意的图像版本检查这些答案是否稳定；MatchedCtrl 则用于判断这种稳定性检查是否真的比“在原图上多问几次简短答案”更有价值。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 原图候选生成与答案规范化

从 $p_{\theta}(\cdot\mid x,q)$ 采样 $N$ 条带思维链的回答 $a_1,\ldots,a_N$，再用 $\mathrm{ans}(\cdot)$ 提取并规范化每条回答的最终答案。将不同的规范化答案汇成候选集合 $\mathcal{A}=\{\mathrm{ans}(a_i)\}$，同时保留每个候选在原图样本中的票数。

<div class="method-step__io" markdown="1">

**输入**：单个图文实例 $(x,q)$、视觉语言模型 $p_{\theta}$、原图采样数 $N$。<br>
**输出**：候选答案集合 $\mathcal{A}$，以及每个 $c\in\mathcal{A}$ 的原图投票计数。

</div>

**直观理解**：这一阶段相当于让模型用较完整的推理过程独立解题 $N$ 次，然后把措辞不同但最终答案相同的回答归到同一票箱。候选集合只由原图回答产生，后续扰动样本负责重排这些候选，而不是任意引入新的最终选项。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造标签保持的扰动视图

对原图应用朝向问题相关区域的裁剪、背景遮罩、轻微亮度或对比度变化、小角度旋转或缩放，得到 $t_m(x)$。设计要求是每个变换均保留回答问题所需的证据，使真实答案 $a^{\star}$ 对 $(x,q)$ 与 $(t_m(x),q)$ 保持一致。

<div class="method-step__io" markdown="1">

**输入**：原图 $x$、问题 $q$ 和扰动集合 $\mathcal{T}=\{t_1,\ldots,t_M\}$。<br>
**输出**：$M$ 个理论上不改变问题真实标签的扰动图像 $t_1(x),\ldots,t_M(x)$。

</div>

**直观理解**：这些变换类似于用略有不同的取景、亮度或背景呈现同一证据；若答案确实由图像证据支持，模型应有机会在这些视图上再次得到它。这里的“标签保持”约束针对任务真值，而不是保证模型预测一定不变。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 扰动视图重推导与一致性计分

对每个 $t_m(x)$ 从 $p_{\theta}(\cdot\mid t_m(x),q)$ 生成 $K$ 条不含思维链的短回答 $a^{(m,1)},\ldots,a^{(m,K)}$。对每个候选 $c$，以短回答中规范化答案等于 $c$ 的比例计算重推导强度 $\rho(c\mid t_m(x),q)$。

<div class="method-step__io" markdown="1">

**输入**：候选集合 $\mathcal{A}$、每个扰动视图 $t_m(x)$、问题 $q$ 和每视图采样数 $K$。<br>
**输出**：每个候选在每个扰动视图上的一致性分数，以及总计 $MK$ 条扰动视图短回答。

</div>

**直观理解**：这一步不是让模型口头评价某个候选是否正确，而是要求模型在修改后的图像上重新作答。候选被独立生成得越频繁，其扰动一致性分数越高，但高一致性本身仍不等于答案正确。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选聚合、选择与格式匹配审计

Pgs 按 $g(c)$ 合并原图票数和扰动支持，并返回 $\hat{a}=\arg\max_{c\in\mathcal{A}}g(c)$；主要实验固定 $\lambda=2$。公平审计时，MatchedCtrl 不生成扰动视图样本，而是在原图上生成相同数量的 $MK$ 条无思维链短答案，并将其与同一批 $N$ 条原图思维链答案合并后多数投票。

<div class="method-step__io" markdown="1">

**输入**：原图票数、扰动一致性分数、扰动权重 $w_m$、权衡系数 $\lambda$，以及总生成预算 $B=N+MK$。<br>
**输出**：Pgs 的最终答案 $\hat{a}$，以及预算和解码格式匹配的 MatchedCtrl 对照答案。

</div>

**直观理解**：Pgs 用“原图有多少票”和“轻微改图后还能否答出”共同决定胜者。MatchedCtrl 则把同样的额外机会全部用于原图，因此两者的差异才较接近扰动机制本身的净作用。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### Pgs 的 grounded support 与最终选择

$$
g(c)=\sum_{i=1}^{N}\mathbf{1}[\mathrm{ans}(a_i)=c]+\lambda\sum_{m=1}^{M}w_m\,\rho\!\left(c\mid t_m(x),q\right),\qquad \hat{a}=\arg\max_{c\in\mathcal{A}}g(c)
$$

**符号说明**

- $g(c)$：候选答案 $c$ 的总支持分数，由原图票数和扰动视图支持共同构成。
- $c$：候选集合 $\mathcal{A}$ 中的一个规范化答案。
- $N$：在原图上生成的带思维链候选回答数量。
- $\mathbf{1}[\cdot]$：指示函数；括号内条件成立时取 $1$，否则取 $0$。
- $\mathrm{ans}(a_i)$：从第 $i$ 条生成回答 $a_i$ 中抽取并规范化得到的最终答案。
- $\lambda$：原图投票与扰动稳定性之间的非负权衡系数；主要结果使用 $\lambda=2$。
- $M$：标签保持扰动的数量。
- $w_m$：第 $m$ 个扰动的非负权重。
- $\rho(c\mid t_m(x),q)$：模型在第 $m$ 个扰动图像上重新生成候选 $c$ 的强度。
- $t_m(x)$：对原图 $x$ 应用第 $m$ 个标签保持变换后得到的图像。
- $\hat{a}$：在所有候选中取得最高总支持分数的最终输出答案。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项直接计算候选在原图 $N$ 次回答中得到多少票；第二项把它在各扰动视图上的重现频率按 $w_m$ 汇总，再由 $\lambda$ 控制影响力。若 $\mathcal{T}=\emptyset$ 或 $\lambda=0$，第二项消失，$g(c)$ 只剩原图票数，因此该规则严格退化为多数投票；这也说明扰动模块的作用是重排已有候选，而非取代原图生成。<br>
**原文位置**：第 3.3 节，公式 (1)；最终选择见第 3.3 节 Algorithm 1

</div>

</div>

<div class="equation-block" markdown="1">

#### 扰动视图上的重推导一致性

$$
\rho\!\left(c\mid t_m(x),q\right)=\frac{1}{K}\sum_{k=1}^{K}\mathbf{1}\!\left[\mathrm{ans}\!\left(a^{(m,k)}\right)=c\right],\qquad a^{(m,k)}\sim p_{\theta}\!\left(\cdot\mid t_m(x),q\right)
$$

**符号说明**

- $\rho(c\mid t_m(x),q)$：候选 $c$ 在第 $m$ 个扰动视图上的经验重推导比例。
- $K$：每个扰动视图上生成的无思维链短回答数量。
- $k$：同一扰动视图内短回答样本的索引。
- $a^{(m,k)}$：模型在第 $m$ 个扰动视图上生成的第 $k$ 条短回答。
- $p_{\theta}$：参数为 $\theta$ 的视觉语言模型所定义的条件回答分布；本文不更新该参数。
- $x$：原始输入图像。
- $q$：与图像配对的输入问题。
- $\mathrm{ans}(\cdot)$：把完整生成文本映射为规范化最终答案的函数。

<div class="equation-explanation" markdown="1">

**直观理解**：该式用频率近似模型在扰动图像上重新得到候选 $c$ 的倾向：若 $K$ 条短回答中有一半规范化后等于 $c$，则该视图上的 $\rho$ 为 $0.5$。它比让模型直接评价“这个答案对不对”更具操作性，但仍可能受到语言先验影响，因此论文必须用 MatchedCtrl 检查它是否真正带来额外选择准确率。<br>
**原文位置**：第 3.3 节，公式 (2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。Pgs 是无标签、免训练的测试时选择规则，不更新模型参数 $\theta$，也没有通过梯度下降优化的训练损失；$g(c)$ 是推理阶段的候选排序分数，而不是训练目标。主要实验将 $\lambda$ 固定为 $2$，该值按协议一次选定而非依据每个测试样本的真值调节；文中另行评估一种无标签选择规则，即把每个扰动视图的 $K$ 个样本分成两半，在两半所选答案至少有 $80\%$ 一致的 $\lambda$ 中取最大值，但该规则不用于主要结果表。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 标签保持扰动模块**

该模块定义有限映射集合 $\mathcal{T}=\{t_1,\ldots,t_M\}$，其中 $t_m:\mathcal{X}\to\mathcal{X}$，并要求真实答案 $a^{\star}$ 在 $(x,q)$ 与所有 $(t_m(x),q)$ 上不变。文中使用问题相关裁剪、背景遮罩、轻微光度抖动以及小幅旋转或缩放；扰动是否真正依赖视觉证据还需结合移除证据区域的标签破坏对照进行审计。

> 直观理解：该模块提供多个仍应能回答同一问题的图像版本，使选择器能够检查答案是否随无关视觉变化而崩溃。它只建立稳定性测试条件，不能自动证明稳定答案一定来自正确的视觉推理。

**2. 重推导一致性与加权选择模块**

对每个候选 $c\in\mathcal{A}$，模块先统计其原图票数，再通过 $K$ 次短答案采样估计每个扰动视图上的 $\rho(c\mid t_m(x),q)$，最后以非负权重 $w_m$ 和系数 $\lambda\geq0$ 汇入 $g(c)$。原图票数始终存在，扰动项仅对候选重新加权；$\lambda$ 过大时可能推翻原本正确的多数答案，因此 Pgs 并不保证优于多数投票。

> 直观理解：原图投票反映模型最初偏向哪个答案，扰动项反映该答案在换一种图像呈现后是否还能被重新得到。$\lambda$ 控制选择器有多信任这种稳定性证据。

**3. MatchedCtrl 因果归因对照模块**

在固定 $B=N+MK$ 时，Pgs 使用 $\mathrm{CoT}_N(x)$ 加上 $\{\mathrm{Short}_K(t_m(x))\}_{m=1}^{M}$，MatchedCtrl 使用同一批 $\mathrm{CoT}_N(x)$ 加上 $\mathrm{Short}_{MK}(x)$。二者保持总生成次数和额外样本的短答案格式一致，仅改变短答案看到的是扰动图像还是原图；普通多数投票只使用 $N$ 条思维链样本，因而不能单独隔离扰动的贡献。

> 直观理解：如果只和普通多数投票相比，就无法判断提升来自图像扰动、额外采样，还是短答案更容易形成一致票数。MatchedCtrl 相当于把除扰动之外的条件尽量对齐，使 Pgs 相对它的差值成为更可信的机制检验。

**训练与推理**

完整流程全部发生在推理阶段。对每个 $(x,q)$，先在原图上生成 $N$ 条带思维链回答并抽取规范化答案；Pgs 再为每个 $t_m\in\mathcal{T}$ 生成 $K$ 条无思维链短回答，计算 $\rho$ 和 $g(c)$，最后输出得分最高的 $\hat{a}$。若不使用扰动或令 $\lambda=0$，流程退化为原图多数投票。用于机制审计的 MatchedCtrl 复用同一批 $N$ 条原图思维链回答，但把 Pgs 的 $MK$ 次短回答预算全部放在原图上，然后对合并答案执行多数投票。

论文还区分“诊断”与“路由”两种作用：标签保持与标签破坏扰动之间的稳定性差距，以及把扰动输入置空后的分数变化，只检验 $\rho$ 是否依赖图像；路由检验则考察更大的稳定性差距能否预测逐样本的正确性差 $\mathbf{1}[\mathrm{Pgs}]-\mathbf{1}[\mathrm{MatchedCtrl}]$。前者成立并不自动意味着后者成立，只有 Pgs 相对 MatchedCtrl 获得可靠的正准确率差，或稳定性差距与逐样本收益呈单调关系，才能支持扰动一致性是一种可用选择信号。

**复现信息**

公平解释结果所需的核心配置是统一生成预算 $B=N+MK$，默认取 $32$；Pgs 与 MatchedCtrl 都消耗 $N+MK$ 次生成，而只使用原图思维链的普通多数投票消耗 $N$ 次生成。Pgs 的原图样本采用带思维链生成并抽取最终答案，扰动视图的 $MK$ 个样本采用短答案、无思维链格式；MatchedCtrl 必须在原图上使用相同数量和相同短答案格式的额外样本，否则无法排除解码格式及预算差异。扰动样本通常比长思维链便宜，但论文的主要比较按生成次数匹配，而不是声称严格匹配所有 token 或实际计算量。

主要操作点固定为 $\lambda=2$，扰动权重默认按文中所述的投票权重 $1$ 聚合，候选池采用 union 设置，且不依据单个测试样本的真值调参。复现时还必须保持答案规范化函数 $\mathrm{ans}(\cdot)$ 一致，因为原图票数和扰动重推导频率都依赖字符串归一化后的相等判断；同时应确保所选裁剪、遮罩和轻微光度或几何变化保留回答所需证据，否则测得的是标签被改变后的性能，而非标签保持条件下的一致性。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- TextVQA：图像文字问答基准，主表使用 300 个样本，准确率按“任一人工标注答案匹配”计算。它主要检验 OCR 密集、对裁剪和几何变化较敏感的场景，也是 Pgs 相对普通多数投票表面提升最大的基准。
- MATH-Vision 与 MMMU：分别覆盖视觉数学推理和多学科多模态理解；Qwen 主表规模分别为 299 和 900。二者用于检验扰动一致性是否能从文字识别场景推广到符号推理和综合知识推理。由于输出列表上限，这里合并说明两个作用相近的通用推理基准。
- ViLP：每道题同时设置符合语言先验的答案与必须依赖视觉证据的答案，Qwen 主表每个种子使用 600 个样本；StabilityGap 在非先验的接地槽位上计算。它是最直接的压力测试：若 Pgs 确实在选择层促进视觉接地，理论上应更常从先验答案转向接地答案。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**硬匹配准确率**

最终选择答案与标准答案完全匹配的样本比例，以百分数报告；TextVQA 使用任一标注者答案匹配。它直接衡量选择器是否选出正确答案。 （越高越好，因为更高值表示最终答案正确的样本更多。）

</div>
<div class="metric-item" markdown="1">

**StabilityGap**

在 MV 所选候选上计算 $\rho_{\mathrm{preserve}}-\rho_{\mathrm{destroy}}$：比较候选在保标签扰动与破坏标签裁剪下被模型重新推导出来的概率。它衡量一致性信号是否区分保留证据和破坏证据的图像。 （若只讨论视觉敏感性，较大的正值表示信号更依赖有效图像证据；但它不是准确率指标，论文实验表明更大并不意味着 Pgs 更可能胜过 MatchedCtrl。）

</div>
<div class="metric-item" markdown="1">

**Pgs 相对控制的准确率差与 95% bootstrap 置信区间**

核心差值为 $\Delta=\mathrm{acc}(\mathrm{Pgs})-\mathrm{acc}(\mathrm{MatchedCtrl})$；逐类别分析用 bootstrap 置信区间判断差值是否可靠偏离零。RoutingTest 还考察逐样本正确性差与 StabilityGap 的相关性。 （差值越高越支持 Pgs；只有置信区间完全位于零以上，才能视为该类别存在显著正收益。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen、总预算 32：Pgs 与只使用 $N$ 个 CoT 样本的普通 MV 比较

<div class="result-value" markdown="1">

TextVQA 上 MV、Pgs 分别为 54.4% 和 86.2%，表面提升 31.8 个百分点；MATH-Vision 和 MMMU 仅分别提升 0.4 与 0.7 个百分点，ViLP 则下降 0.9 个百分点。

</div>

作者结果表明 Pgs 相对传统 MV 可以出现很大增益，但这一比较同时改变了解码格式和有效短答案数量。因而 31.8 个百分点只能说明“加入扰动视图上的短、无 CoT 答案并重新聚合”优于小型全 CoT 投票池，不能单独证明扰动一致性提供了视觉接地能力。

<div class="result-source" markdown="1">

来源：第 5.2 节 Main results；表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Against plain MV, Pgs gains substantially on TextVQA (+31.8 pp) and is near-flat on MATH-V, MMMU, and ViLP.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen、总预算与解码格式匹配：Pgs 对 MatchedCtrl

<div class="result-value" markdown="1">

MatchedCtrl 与 Pgs 在 TextVQA 上为 87.6% 对 86.2%，MATH-Vision 为 25.3% 对 26.0%，MMMU 为 50.1% 对 50.3%，ViLP 为 53.7% 对 52.3%；作者将这些差异判断为均处于种子噪声范围，且 TextVQA 和视觉接地压力测试 ViLP 上控制组反而更高。

</div>

这是论文最关键的隔离实验。MatchedCtrl 已控制总调用次数和短、无 CoT 格式，因此 Pgs 没有稳定胜出意味着把短答案路由到扰动图像并使用 $\rho$ 加权，没有显示出超越原图短答案聚合的可靠价值。它支持“表面增益主要来自格式与候选池变化”的解释，但不等于证明所有可能的视觉扰动选择器都无效。

<div class="result-source" markdown="1">

来源：第 5.2 节 Main results；表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MatchedCtrl spends those same short answers on the original image and, under this format-matched control, tracks Pgs within seed noise on every benchmark (TextVQA 87.6 vs. 86.2; MATH-V 25.3 vs. 26.0; MMMU 50.1 vs. 50.3; ViLP 53.7 vs. 52.3), with MatchedCtrl still ahead on TextVQA.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨模型、预算 32 的无标签选择器比较，以及 StabilityGap 的诊断有效性

<div class="result-value" markdown="1">

在 LLaVA 和 Qwen 的匹配预算表中，SC 与 Entropy 经常低于 MatchedCtrl，SC+Borda 和 CISC 通常只与其相当；与此同时，Qwen 的 TextVQA 与 ViLP StabilityGap 分别达到 0.478 和 0.445，却没有带来 Pgs 对 MatchedCtrl 的胜出。

</div>

跨模型结果降低了结论只由某个 Qwen 检查点造成的可能性，也说明 MatchedCtrl 不是刻意设置的弱控制。较大的 StabilityGap 证明保标签与破坏标签视图会触发不同的重推导行为，即信号确实“看见”图像；但准确率不随之改善，说明视觉敏感诊断与有效选择规则是两个不同命题。

<div class="result-source" markdown="1">

来源：第 5.1 节 Baselines、表 2；第 5.2 节 Main results、表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Large mean preserve/destroy gaps on TextVQA and ViLP (+0.478/+0.445) coexist with no win over MatchedCtrl, while smaller gaps on MATH-V and MMMU (+0.025/+0.071) likewise fail to separate Pgs from MatchedCtrl.

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

- MV：只对 $N$ 个原图 CoT 样本做多数投票，是常见但存在混杂的参照。它能显示加入 Pgs 后的表面提升，却没有控制额外的 $M\cdot K$ 次生成以及 CoT 到短、无 CoT 解码格式的变化。
- MatchedCtrl：复用 $N$ 个 CoT 答案，并在原图上增加 $M\cdot K$ 个短、无 CoT 答案，使总预算满足 $N+MK\in\{16,32\}$。它与 Pgs 唯一关键差别是额外答案是否经过扰动视图，因此是判断“扰动机制本身是否有效”的决策性零假设基线。
- SC 与 Entropy：SC 按模型自评确定性选择，Entropy 按平均 token 熵衡量不确定性；二者都在匹配的解码池上经 teacher-forcing 重评分。它们检验常见的模型内部置信信号能否替代扰动一致性。
- SC+Borda 与 CISC：前者把自确定性与 Borda 排序投票结合，后者是置信度加权自一致性。它们代表更强的无标签聚合器，用于判断 MatchedCtrl 的表现是否只是弱基线造成，而非解码格式和候选多样性已经吸收主要收益。

**实验想回答的问题**

- 在总生成预算与解码格式都匹配后，扰动接地选择（Pgs）是否仍优于格式匹配控制 MatchedCtrl，即把额外短答案分配到扰动图像并按重推导支持度 $\rho$ 加权，是否比在原图上生成相同数量、相同格式的短答案真正带来选择收益？
- Pgs 的一致性信号是否确实依赖图像，以及这种视觉依赖能否进一步预测 Pgs 相对 MatchedCtrl 的逐样本或分类别收益？前者由 StabilityGap 和 BlankAblation 检查，后者由 RoutingTest、类别置信区间和 ViLP 上的先验答案到接地答案翻转检查。

**实验实现**

实验覆盖 Qwen2.5-VL-7B-Instruct 与 LLaVA-OneVision-7B。Qwen 机制主表以及 StabilityGap、BlankAblation、敏感性分析和 RoutingTest 主要报告种子 $\{0,23,42\}$ 的均值；预算匹配的选择器表同时报告两个模型的均值与标准差。默认每个样本从原图生成 $N=8$ 个 CoT 答案，再对 $M=6$ 个保标签扰动各生成 $K=4$ 个短、无 CoT 答案，总预算为 $N+MK=32$；预算 16 的结果从预算 32 的保存输出中离线下采样，使用 $N=4$、$K=2$。Pgs 采用候选池并集、投票权重 $\mathrm{vw}=1$ 和 $\lambda=2$，按“票数加 $\lambda$ 倍重推导支持度 $\rho$”选答案；MatchedCtrl 则把同样的 $MK$ 次短解码全部放在原图上。默认运行设备为单张 NVIDIA RTX 4090。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| BlankAblation：固定原图 CoT 候选池，将扰动视图输入置空 | 单种子 Qwen 实验中，TextVQA 从 Pgs 的 87.7% 降至 7.9%，ViLP-F 从 46.2% 降至 0.4%，MMMU 从 50.2% 降至 23.3%；符号性更强的 MATH-Vision 仅从 26.3% 变为 23.4%。 | 该消融隔离“扰动支路是否真的使用图像”：在 OCR、综合视觉理解和视觉接地任务上置空图像导致崩溃，说明 $\rho$ 不是纯粹由短解码格式产生。然而这些绝对值来自较早的单种子运行，不能与多种子主表直接横向比较；而且图像依赖仍未转化为相对 MatchedCtrl 的选择优势。 | 第 5.3 节 Ablations；表 4<br><span class="experiment-evidence">Blanking the perturbation inputs (BlankAblation, Table 4) collapses Pgs’s accuracy where the signal is strong (TextVQA 87.7→7.9, ViLP-F 46.2→0.4, MMMU 50.2→23.3) while symbolic MATH-V is unaffected, confirming the score is genuinely image-dependent rather than a format artifact of short decoding alone.</span> |
| RoutingTest：按任务类别和 StabilityGap 检查 Pgs 相对 MatchedCtrl 的条件收益 | Qwen 三种子汇总中，没有任何类别的 Pgs 准确率优势达到显著水平；所有正向类别的 95% bootstrap 置信区间都未完全位于零以上，ViLP 的区间完全低于零。补充分析还报告逐样本 gap 与收益的相关性接近零，gap 四分位结果不单调。 | 该分析直接检验能否只在“高 gap”样本或感知密集类别上启用 Pgs。结果否定了当前信号的实用路由价值：即使总体均值接近零，也没有发现可靠受益子集。这里否定的是论文所研究的 $\rho$ 与路由规则，不能外推为所有视觉依赖指标都无法用于条件选择。 | 图 2；第 5.4 节 RoutingTest<br><span class="experiment-evidence">No interval lies entirely in the “favors Pgs” half-plane (shaded); the ViLP interval lies entirely below zero.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：核心贡献是审计视觉语言推理中基于采样与一致性选择的测试时扩展方法，并揭示解码格式这一关键混杂因素。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`2eda9f5ee62b0ff27903afd305c477408cd20d4b81f4c6dff79276c339c26439`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
