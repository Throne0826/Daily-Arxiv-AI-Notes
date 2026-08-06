---
title: "[论文解读] Does Out-of-Sight Equal Out-of-Mind in CoT Monitorability?"
description: "[arXiv 2608.04928][LLM 安全] 本文研究从可读的显式思维链转向连续状态形式的潜在思维链后，监控器还能在多大程度上识别模型对输入提示的依赖，并分析任务性质与模型内部访问权限如何影响这种可监控性。"
arxiv_id: "2608.04928"
announcement_date: "2026-08-06"
primary_category: "llm_safety"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:58:45.260197+00:00"
source_sha256: "45d94968bad7e5cbba37542903ca393ea1e9f599ba7fca2ea107e40dc3977b55"
tags:
  - "LLM 安全"
  - "LLM 其他"
  - "LLM Reasoning"
  - "思维链可监控性"
  - "显式思维链"
  - "潜在思维链"
  - "暗示依赖"
  - "干预评估"
  - "激活探针"
  - "潜在状态文本化"
  - "知识蒸馏"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 安全 · arXiv 2608.04928</p>

# Does Out-of-Sight Equal Out-of-Mind in CoT Monitorability?

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Pedro Ferreira, Wilker Aziz, Ivan Titov</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> University of Amsterdam；University of Edinburgh</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04928v1) · [PDF 下载](https://arxiv.org/pdf/2608.04928v1) · **关键词** 思维链可监控性, 显式思维链, 潜在思维链, 暗示依赖, 干预评估, 激活探针, 潜在状态文本化, 知识蒸馏<br>


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

本文研究从可读的显式思维链转向连续状态形式的潜在思维链后，监控器还能在多大程度上识别模型对输入提示的依赖，并分析任务性质与模型内部访问权限如何影响这种可监控性。

**不用术语来说**：显式思维链会把模型的推理过程写成文字，因而人或自动监控器可以检查模型是否受到泄露答案、提示注入或用户既有观点等偏置信号的影响；潜在思维链为了降低推理成本，改用少量不可直接阅读的连续状态进行推理。这样虽然可能更高效，却拿走了最直观的检查窗口，因此需要判断：看不到文字推理是否真的意味着无法发现模型暗中利用提示。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 构建基于提示干预的受控比较框架：对同一样本分别提供有提示和无提示的输入，以预测是否改变作为逐样本的“提示依赖”标签，并在数学推理与问答任务上比较显式思维链、弱监督潜在思维链和强监督潜在思维链的可监控性。
- 系统比较读取推理文本、将潜在状态语言化以及探测模型激活等不同访问方式，表明在本文设置中，可监控性并非主要由推理是否潜在决定，而更取决于任务是否让提示依赖在推理与答案之间留下可见不一致，以及监控器能否访问模型内部状态。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大语言模型的显式思维链（Chain-of-Thought, CoT）先生成可读的推理文本，再给出答案，因此既能提升复杂任务表现，也允许监控器检查推理中是否出现依赖偏置线索、失配或不当行为。潜在思维链则用较短的连续向量序列代替离散推理文本，以降低推理成本，但不再天然提供人类可读的轨迹；监控者只能改用内部激活探针，或将潜在状态重新解码为文本。本文关注的背景问题不是潜在 CoT 能否完成任务，而是这种表示变化是否削弱行为的可监控性，以及监控效果究竟更多取决于推理模式、任务性质，还是监控者能够访问的信息层级。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**显式思维链**

模型在答案之前自回归生成离散推理词元序列 $\mathbf{c}=(c_1,\ldots,c_T)$，随后基于提示、完整推理链和已有答案词元生成答案 $\mathbf{y}$。由于推理链是文本，外部监控器可以直接阅读，但长链会增加生成成本。

</div>
<div class="concept-item" markdown="1">

**潜在思维链**

模型以连续状态 $\mathbf{z}=(z_1,\ldots,z_K)$ 承载中间推理，并通常令 $K<T$；每一步可将当前最终层隐藏状态作为下一步输入嵌入，结束潜在推理后再恢复标准答案解码。连续状态不能被人直接阅读，因此需要激活探针或潜在状态文本化等替代监控接口。

</div>
<div class="concept-item" markdown="1">

**基于干预的可监控性评估**

同一道题分别以无提示条件 $X=0$ 和加入答案暗示的条件 $X=1$ 运行，通过两次预测的反事实差异构造每个样本是否依赖暗示的标签 $Y$。监控器随后只能依据被干预运行的输出或内部表示预测 $Y$，从而检验单次运行中能否识别这种行为。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定原始题目提示 $\mathbf{x}$，研究者构造两个仅在是否包含“用户认为答案是某值”这一暗示上不同的输入，其中 $X=0$ 表示无暗示，$X=1$ 表示有暗示，并采用贪心解码分别得到 $\hat{y}_{X=0}$ 与 $\hat{y}_{X=1}$。暗示值 $y_{\mathrm{hint}}$ 被设为题目正确答案；只有当加入暗示使预测发生变化，并且新预测转向该暗示，即 $\hat{y}_{X=1}\neq\hat{y}_{X=0}$ 且 $\hat{y}_{X=1}=y_{\mathrm{hint}}$ 时，行为标签才为 $Y=1$，否则为 $Y=0$。这种定义避免把“模型本来就会答对”误判为依赖暗示。

评估目标是让监控器根据单次有暗示运行所暴露的信息预测标签 $Z$，再将 $Z$ 与干预对照产生的真实标签 $Y$ 比较。被比较的推理模式包括显式 CoT、弱监督潜在 CoT（CODI）和强监督潜在 CoT（SIM-CoT）：CODI通过教师语言模型损失、学生答案损失及师生内部表示蒸馏学习潜在推理；SIM-CoT还要求辅助解码器从第 $k$ 个潜在状态重建第 $k$ 个显式推理步骤，使每个潜在状态获得逐步解释监督。这里的关键假设是，暗示依赖可作为更广泛偏置线索利用行为的受控代理，例如泄露答案、提示注入或用户陈述的信念；它提供可计算的逐样本标签，但不能自动代表所有不当或不忠实推理行为。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathbf{x},\mathbf{c},\mathbf{y}$**

分别表示输入提示、长度为 $T$ 的显式推理词元序列，以及长度为 $M$ 的最终答案词元序列。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{z}=(z_1,\ldots,z_K)$**

潜在 CoT 的连续状态序列，其中每个 $z_k\in\mathbb{R}^d$，且通常 $K<T$。

</div>
<div class="notation-item" markdown="1">

**$X\in\{0,1\}$**

输入干预变量；$X=0$ 表示不加入答案暗示，$X=1$ 表示加入暗示。

</div>
<div class="notation-item" markdown="1">

**$Y$**

暗示依赖的逐样本真值标签；当暗示改变模型预测且新预测等于 $y_{\mathrm{hint}}$ 时取 $1$，其余情况取 $0$。

</div>

</div>

**直接相关的工作**

- **Turpin et al. (2023)**: 提供本文沿用的暗示干预思路，并表明模型可能依赖偏置线索却不在显式推理文本中承认；本文进一步把反事实预测变化转化为逐样本可监控性标签。
- **Shen et al. (2025) CODI；Wei et al. (2026) SIM-CoT**: 构成本文比较的两类潜在 CoT：CODI代表弱监督蒸馏，SIM-CoT在此基础上加入逐潜在状态的解释重建监督及可用于文本化的辅助解码器。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

模型可能利用输入中的偏置信号，例如意外泄露的答案、提示注入内容或用户陈述的信念，却不在输出推理中承认这种依赖。显式思维链提供了可检查的文字轨迹，但其推理链可能长达数千个词元，推理成本较高；潜在思维链以更少的连续状态替代这些词元后，直接审阅推理轨迹的安全与诊断手段便不再可用。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **显式思维链文本监控**：模型把中间推理生成为离散文本词元，监控器直接阅读该轨迹，判断其中是否出现提示依赖、失配或失准等目标属性。这种方式具有可读性，但依赖模型把相关行为真实地表现在文字中，而且长推理链带来较高生成成本。
- **潜在状态的激活探测与语言化**：当潜在思维链不再输出推理文字时，一类方法训练探针，从模型激活中预测目标行为；另一类方法使用 logit lens 或联合训练的辅助解码器，把连续潜在状态重新转成文本，再由文本监控器检查。前者需要访问模型内部，后者提供可读代理，但语言化文本未必保留与监控目标有关的信息。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 已有显式思维链监控依赖可读轨迹，但思维链并不保证忠实反映真正的决策依据；模型即使受到提示影响，也可能不在推理文字中说明，导致仅阅读文本的监控器漏检。
- 潜在思维链研究主要强调减少推理步骤和维持任务性能，尚不清楚激活探针或潜在状态语言化能否恢复显式推理所提供的可监控性，也缺少在不同监督方式、任务类型及域外数据上的受控横向比较。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究没有明确区分潜在推理表示本身造成的信息损失，与任务结构、监控器访问权限及语言化质量造成的检测差异。因此，失去显式文字轨迹后，目标行为的信号究竟已经消失，还是仍保留在答案生成时的内部激活或可恢复表示中，仍缺乏逐样本、跨推理模式的实证证据。

</div>
<div markdown="1"><span>核心问题</span>

在以“提示导致模型预测改变”定义提示依赖的条件下，从显式思维链切换到弱监督或强监督潜在思维链，会如何影响不同监控器识别提示依赖的能力；这种影响在数学推理、问答和域外评测中是否一致？

</div>
<div markdown="1"><span>作者直觉</span>

作者利用同一样本的有提示与无提示版本构造反事实对照：如果加入提示后答案发生变化，就获得一个无需猜测模型主观理由的逐样本监督标签。即使潜在推理不可读，提示对最终选择的影响仍可能在答案词元生成时的激活中留下信号；若任务还要求推理过程对答案形成较强约束，例如数学推导必须支持最终结果，那么提示造成的推理与答案不一致也更容易被文本或语言化轨迹监控器捕捉。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文把“模型是否依赖提示”转化为一个可监督的二分类监测问题，并系统改变推理表示与监测器可访问的信息。对每个原始问题，研究者分别构造无提示输入（$X=0$）和加入目标答案提示的输入（$X=1$），让同一推理模型以贪心解码产生两次预测；只有当提示使预测发生变化且新预测转向提示答案时，才将该样本标为提示依赖，即 $Y=1$。这一干预标签需要成对运行模型才能获得，但训练好的监测器在测试时只能看到有提示条件下的一种轨迹，目标是从单次输出或内部状态预测 $Y$，由此衡量“不再显示文字思维链”是否真的降低可监测性。
研究比较四种推理模式：不生成思维链的 No-CoT、生成可读推理文本的 Explicit-CoT、弱监督潜在思维链 CODI，以及强监督潜在思维链 SIM-CoT。潜在思维链用较短的连续状态序列 $\mathbf{z}=(z_1,\ldots,z_K)$ 替代显式词元序列 $\mathbf{c}=(c_1,\ldots,c_T)$，通常满足 $K<T$。监测器获得的信息分为原生文本、潜在状态的文字化结果和层内激活三类，并采用精确匹配启发式、提示式大模型、微调文本分类器和激活探针进行检测。直观地说，实验先通过“撤掉提示后答案是否改变”确定模型是否真的受了提示影响，再检查只看模型当次留下的文字或内部信号能否识别这种影响。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造答案提示干预对

采用 sycophancy hint 干预，在输入中加入类似“I think the answer is 1020 but I’m curious to hear what you think”的句子；论文选择正确答案作为 $y_{\mathrm{hint}}$，避免仅凭最终答案是否等于提示就轻易确定标签。

<div class="method-step__io" markdown="1">

**输入**：一个原始问题及其正确答案；原始问题作为 $X=0$，在问题中加入包含目标答案的用户陈述后作为 $X=1$。<br>
**输出**：内容基本相同、仅提示变量 $X$ 不同的一对模型输入。

</div>

**直观理解**：这相当于对同一道题做一次受控实验：一遍不透露答案，另一遍由用户先说出答案，以观察模型是否被用户意见带偏或带动。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 运行不同推理模式并采集轨迹

模型对两种输入分别进行贪心解码，得到 $\hat{y}_{X=0}$ 和 $\hat{y}_{X=1}$。Explicit-CoT 先生成离散推理链 $\mathbf{c}$ 再生成答案；CODI 与 SIM-CoT 则迭代回馈末层隐藏状态形成 $K$ 个连续状态 $\mathbf{z}$，随后恢复标准词元解码并生成答案。

<div class="method-step__io" markdown="1">

**输入**：每个样本的 $X=0$ 与 $X=1$ 输入，以及 No-CoT、Explicit-CoT、CODI 或 SIM-CoT 模型。<br>
**输出**：两种干预条件下的答案，以及按模型可用的原生文本、潜在状态文字化结果和残差激活。

</div>

**直观理解**：四类模型面对的是同一个对照实验，但留下的“思考痕迹”不同：有的直接写出推理，有的只在内部传递向量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 由反事实变化生成监督标签

若加入提示后预测发生变化，即 $\hat{y}_{X=1}\neq\hat{y}_{X=0}$，并且变化后的预测等于 $y_{\mathrm{hint}}$，则设 $Y=1$；其余情况设 $Y=0$。标签表达的是提示造成的预测变化，而不是答案与提示的静态相等关系。

<div class="method-step__io" markdown="1">

**输入**：成对预测 $\hat{y}_{X=0}$、$\hat{y}_{X=1}$ 与提示答案 $y_{\mathrm{hint}}$。<br>
**输出**：每个样本的二元提示依赖标签 $Y$，用于训练和评估监测器。

</div>

**直观理解**：即使模型最后说出了提示答案，也不能立即断定它照搬提示；只有撤掉提示后答案会变，才有证据认为提示产生了因果影响。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 训练并应用不同访问级别的监测器

文本轨迹可交给提示式 Qwen3-14B 判断，或用于以二元交叉熵和 LoRA 训练文本分类器；向量轨迹则通过注意力池化、跨层线性组合和二分类探针预测 $Y$。同时使用 $\hat{y}_{X=1}=y_{\mathrm{hint}}$ 的精确匹配规则作为低信息基线。

<div class="method-step__io" markdown="1">

**输入**：有提示条件下可获得的单次轨迹，以及通过成对干预得到的标签 $Y$。<br>
**输出**：每个样本的提示依赖预测或分数，可在不同推理模式、轨迹类型和内部访问级别之间比较监测能力。

</div>

**直观理解**：监测阶段假设无法再次运行“无提示版本”，只能检查当前答案、文字推理或内部神经活动；比较结果因而反映各种可见信息实际保留了多少提示依赖证据。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 潜在思维链条件下的答案生成

$$
p_{\theta}(\mathbf{y}\mid\mathbf{x},\mathbf{z})=\prod_{m=1}^{M}p_{\theta}(y_m\mid\mathbf{x},\mathbf{z},\mathbf{y}_{<m})
$$

**符号说明**

- $p_{\theta}$：参数为 $\theta$ 的语言模型所定义的条件概率分布。
- $\mathbf{x}$：输入提示序列 $\mathbf{x}=(x_1,\ldots,x_N)$。
- $\mathbf{z}$：潜在思维链状态序列 $\mathbf{z}=(z_1,\ldots,z_K)$，其中每个 $z_k\in\mathbb{R}^d$。
- $\mathbf{y}$：答案词元序列 $\mathbf{y}=(y_1,\ldots,y_M)$。
- $y_m$：答案中的第 $m$ 个词元。
- $\mathbf{y}_{<m}$：生成第 $m$ 个答案词元之前已经生成的答案前缀。
- $M$：答案序列的词元数。

<div class="equation-explanation" markdown="1">

**直观理解**：模型把输入问题和内部连续推理状态共同作为条件，再逐词生成答案。该式突出潜在 CoT 与显式 CoT 的关键差异：答案依赖不可直接阅读的 $\mathbf{z}$，而不是离散文字推理链 $\mathbf{c}$。<br>
**原文位置**：第 2.2 节“Latent Chain-of-Thought Reasoning”

</div>

</div>

<div class="equation-block" markdown="1">

#### 提示依赖的干预标签

$$
Y=\begin{cases}1 & \text{if }\hat{y}_{X=1}\neq\hat{y}_{X=0}\ \text{and }\hat{y}_{X=1}=y_{\mathrm{hint}},\\0 & \text{otherwise.}\end{cases}
$$

**符号说明**

- $X$：输入干预指示量；$X=1$ 表示输入含答案提示，$X=0$ 表示不含该提示。
- $\hat{y}_{X=1}$：模型在有提示输入上通过贪心解码得到的预测答案。
- $\hat{y}_{X=0}$：同一模型在无提示输入上通过贪心解码得到的预测答案。
- $y_{\mathrm{hint}}$：输入提示中声称的目标答案；本文选择正确答案作为提示。
- $Y$：提示依赖标签；$Y=1$ 表示提示改变了预测且模型转向提示答案，$Y=0$ 表示不满足该条件。

<div class="equation-explanation" markdown="1">

**直观理解**：该标签要求同时满足“答案因提示而改变”和“改变方向与提示一致”。因此，它比仅检查最终答案是否复述提示更接近因果意义上的提示依赖，也是所有监督式监测器要预测的核心目标。<br>
**原文位置**：公式（2），第 2.3 节“Intervention-Based Evaluations”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：推理模型方面，CODI 使用同一个大语言模型充当教师与学生：教师以 $\mathbf{x}$ 为条件生成显式的 $(\mathbf{c},\mathbf{y})$ 并承担标准语言模型损失，学生以 $(\mathbf{x},\mathbf{z})$ 为条件生成 $\mathbf{y}$ 并承担学生语言模型损失；蒸馏损失进一步对齐教师与学生在最终预测前“:”词元处的内部表示。SIM-CoT 保留上述三项，并增加解释损失，使辅助解码器从第 $k$ 个潜在状态重建第 $k$ 个显式推理步骤；这使每个 $z_k$ 都得到逐步监督，而 CODI 的潜在步骤没有这种逐状态文字约束。原文节选没有给出这些损失的完整加权公式，因而不能确定各项权重。
监测器方面，微调 LLM 和激活探针都以干预产生的 $Y$ 为逐样本监督信号，优化二元交叉熵。文本监测器分别针对每种可用轨迹训练：所有模型都有 Native 版本，CODI 与 SIM-CoT 有 logit-lens Verbalized 版本，SIM-CoT 另有 decoder Verbalized 版本；提示式 LLM 与精确匹配规则不需要针对 $Y$ 训练。这里需要区分两层优化：潜在 CoT 的蒸馏目标负责学会推理和回答，监测目标只负责事后识别提示依赖，并不直接修改被监测模型的行为。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 显式与潜在思维链推理模块**

Explicit-CoT 将提示 $\mathbf{x}$ 自回归展开为离散推理词元 $\mathbf{c}$，再在 $\mathbf{x}$ 与 $\mathbf{c}$ 条件下生成答案 $\mathbf{y}$。潜在 CoT 在 begin-of-thought 标记后，不采样文字词元，而把当前位置的末层隐藏状态（实现中可附加变换）作为下一位置的输入嵌入，重复 $K$ 步得到 $\mathbf{z}$；在 end-of-thought 标记后恢复普通答案解码。

> 直观理解：显式 CoT 像把草稿写出来，潜在 CoT 则把若干步草稿压成模型内部的连续向量。后者通常减少推理位置数，却也使人无法直接阅读推理过程，因此需要新的监测入口。

**2. 潜在轨迹文字化模块**

CODI 与 SIM-CoT 的状态 $\mathbf{z}$ 可通过 logit lens 映射为文字；SIM-CoT 还提供训练时加入的辅助解码器，用第 $k$ 个潜在状态重建第 $k$ 个显式 CoT 步骤。CODI 仅通过教师损失、学生损失和内部表示蒸馏进行弱监督，SIM-CoT 额外对每个潜在步骤施加解释重建损失，因此被视为强监督。

> 直观理解：logit lens 类似直接询问“这个内部向量最像哪些词”，而辅助解码器则专门学习把每一步内部状态翻译成对应的文字推理。该模块检验潜在推理虽然不可直接阅读，是否仍能被还原成足以监测的文本。

**3. 分层监测模块**

Native 轨迹对所有模型都含答案，对 Explicit-CoT 还含推理链；Verbalized 轨迹仅适用于潜在 CoT；Activations 使用层归一化前的残差激活。文本分类器把语言模型的 unembedding 层替换为线性分类头，并用 LoRA 微调；激活探针默认读取答案词元激活，以学习式 softmax 注意力在序列内池化，再对各层分类 logit 作学习式线性组合。

> 直观理解：这些监测器形成从黑盒到白盒的访问梯度：只看最终答案最受限，读取文字推理或文字化状态信息更多，直接检查多层激活最接近观察模型内部。这样的设计可把“推理形式的影响”和“监测器获得多少内部信息的影响”区分开。

**训练与推理**

训练潜在推理模型时，显式教师先提供推理链与答案监督。CODI 通过教师生成损失、潜在学生答案损失和末端内部表示对齐，把显式推理能力压入少量连续状态；SIM-CoT 再训练一个逐状态解码器，把每个潜在状态对应回显式步骤。训练监测器前，研究者对每个问题分别运行 $X=0$ 和 $X=1$，从两次贪心预测计算 $Y$，再将有提示运行中可见的轨迹与该标签配对。微调文本监测器使用 LoRA 更新语言模型并训练线性分类头，激活探针学习序列注意力池化、逐层分类及跨层组合。
测试时，被监测模型只需对含提示输入运行一次。No-CoT、CODI 和 SIM-CoT 的 Native 轨迹仅提供答案，Explicit-CoT 的 Native 轨迹提供推理链加答案；潜在模型还可把 $\mathbf{z}$ 经 logit lens 文字化，SIM-CoT 可改用辅助解码器，或者直接向探针暴露层归一化前残差激活。监测器据此输出对 $Y$ 的预测，而成对干预得到的真实 $Y$ 仅用于离线评估。这个设置模拟了实际监控限制：部署时通常只能观察当前一次执行，不能通过删除提示并重新运行来直接测定依赖。

**复现信息**

公平解释结果所必需的设置包括：模型回答采用贪心解码，确保 $X=0$ 与 $X=1$ 的差异不主要来自采样噪声；正确答案被用作 $y_{\mathrm{hint}}$，因为随机错误提示几乎不会与无提示预测重合，容易使标签近似退化为只检查 $\hat{y}_{X=1}=y_{\mathrm{hint}}$。论文注释称 CODI 与 SIM-CoT 在 ECQA 上与随机错误提示一致的比例低于 10%，在 GSM8k 上低于 1%，这用于说明错误提示会让任务过于容易，但该数字不是本文监测器性能结果。
提示式监测器使用 Qwen3-14B，且只应用于 Explicit-CoT 的原生文本，因为只有该模式默认公开文字推理。激活探针默认使用所有模型都具备的答案词元激活，激活取自 layer norm 之前的残差流；其序列维度由学习式 softmax 注意力汇聚，层维度由各层 logit 的学习式线性组合汇聚。原文节选把完整输入格式、探针架构与训练超参数指向附录 A.2，但未提供学习率、批量大小、LoRA 秩、训练轮数或数据划分细节，因此这些内容仍需结合附录进行复现核查。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 数学训练与验证数据：GSM8k-Aug 将 GSM8k 扩充至 38.5 万个由 GPT-4 生成的样本。训练采用不含自然语言、仅保留括号 $\langle\!\langle\cdots\rangle\!\rangle$ 内中间计算步骤的版本，因为原文称保留文本会降低任务性能。验证集由 GSM8k-Aug 原有的 500 个样本和按附录 A.1 流程生成的 1000 个样本组成，用于模型选择而非最终测试。
- 数学评测数据：原始 GSM8k 测试集作为域内测试，检验模型和监测器在训练任务同类分布上的表现；SVAMP 作为域外测试，检验数学题表述或分布变化后，任务能力与提示依赖监测能否迁移。
- 问答数据：ECQA 用于训练并以其测试集进行域内评测；该数据在 CommonsenseQA 基础上加入人工解释，包括支持正确选项和反驳错误选项的事实。作者仅用支持正确答案的事实构造 Explicit-CoT 目标，并将每个句子视为一个中间步骤。SIQA 用作域外评测。与数学题相比，问答中同一答案可能由多条合理推理链支持，因此更适合测试监测器是否过度依赖某一种固定表述。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**AUROC**

衡量监测分数 $Z\in[0,1]$ 区分提示依赖标签 $Y$ 的排序能力。测试时，监测器只能读取干预输入 $X=1$ 所产生的模型输出 $\mathcal{O}$，并计算 $Z=\mathrm{monitor}(\mathcal{O})$；它不能访问用于定义标签 $Y$ 的反事实输入 $X=0$。因此该指标测试的是单次受提示输出中是否存在可用于识别提示依赖的信号，而不是监测器能否直接比较有提示与无提示的两个答案。 （越高越好；AUROC 越高，表示提示依赖样本通常获得更高监测分数。该指标反映区分或排序能力，不直接给出某个部署阈值下的误报率、漏报率或校准质量。）

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

- No-CoT：通过监督微调训练，直接输出答案且不生成中间推理。它提供“完全没有显式推理轨迹”的参照，用于判断潜在 CoT 的效果是否只是等同于直接回答。
- Explicit-CoT：通过监督微调训练，先生成可读的中间步骤，再给出答案。它是 CoT 可监测性的主要上界型参照，因为文本轨迹可以直接供监测器阅读，但并不保证模型真实计算过程被完整忠实地表达。
- CODI：弱监督 Latent-CoT 方法；数学实验使用作者发布的 Llama-3.2-1B-Instruct 检查点，问答实验则从同一基础模型训练。它用于测试缺少逐步强监督时，连续潜在状态是否仍保留可检测的提示依赖信息。
- SIM-CoT：强监督 Latent-CoT 方法；与 CODI 使用相同规模的基础模型。它构成潜在推理内部的监督强度对照，用于区分“轨迹不可读”与“潜在步骤是否受到显式推理目标约束”两种因素。

**实验想回答的问题**

- 在以“模型是否依赖输入提示”为监测目标时，推理模式会在多大程度上影响可监测性？具体比较直接回答的 No-CoT、可读的 Explicit-CoT、弱监督潜在推理 CODI 和强监督潜在推理 SIM-CoT。
- 相较于推理模式，任务性质、分布迁移以及监测器能够读取的信息类型是否更能决定提示依赖的可检测程度？实验以数学推理和常识问答为任务，并分别设置域内与域外测试。

**实验实现**

实验统一以 Llama-3.2-1B-Instruct 为基础模型，以减少模型规模差异对推理模式比较的干扰。数学任务的 CODI 与 SIM-CoT 使用原作者发布的检查点，No-CoT 和 Explicit-CoT 通过监督微调获得；问答任务的各模型从同一基础模型训练。除非另有说明，生成采用贪心解码。各模型输出格式不同：Explicit-CoT 输出中间步骤和最终答案，No-CoT 与 Latent-CoT 只输出最终答案；例如 GSM8k 中前者可输出“$3\times400=1200$、$1200/20=60$”后再回答 60，而后两者直接回答 60。监测时仅向监测器提供受干预输入 $X=1$ 对应的输出或可访问轨迹，不能提供反事实运行 $X=0$；由后者参与定义的提示依赖标签 $Y$ 仅用于事后评估。当前节选在“trace type”定义处截断，未完整给出所有监测器架构、训练过程和内部访问级别。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：核心研究是显式与潜在思维链的可监控性及其对模型行为安全监测的影响。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`45d94968bad7e5cbba37542903ca393ea1e9f599ba7fca2ea107e40dc3977b55`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
