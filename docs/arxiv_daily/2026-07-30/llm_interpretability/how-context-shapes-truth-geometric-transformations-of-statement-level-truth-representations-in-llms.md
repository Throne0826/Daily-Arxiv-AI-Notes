---
title: "[论文解读] How Context Shapes Truth: Geometric Transformations of Statement-level Truth Representations in LLMs"
description: "[arXiv 2601.06599][LLM 机制与可解释性] 本文首次从残差流激活的几何结构出发，考察加入上下文后，区分陈述真假的“真值向量”如何在方向与幅度上发生变化。"
arxiv_id: "2601.06599"
announcement_date: "2026-07-30"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.753890+00:00"
source_sha256: "3ef27fd4e30402c3d72d5ec2ec0b0a164bb0ccdac5bb98529f3aa8912ed2297f"
tags:
  - "LLM 机制与可解释性"
  - "LLM 其他"
  - "大语言模型可解释性"
  - "真值向量"
  - "残差流激活"
  - "上下文利用"
  - "表征几何"
  - "线性方向"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2601.06599</p>

# How Context Shapes Truth: Geometric Transformations of Statement-level Truth Representations in LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Shivam Adarsh, Maria Maistro, Christina Lioma</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2601.06599v3) · [PDF 下载](https://arxiv.org/pdf/2601.06599v3) · **关键词** 大语言模型可解释性, 真值向量, 残差流激活, 上下文利用, 表征几何, 线性方向<br>


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

本文首次从残差流激活的几何结构出发，考察加入上下文后，区分陈述真假的“真值向量”如何在方向与幅度上发生变化。

**不用术语来说**：大语言模型回答问题时，既会使用训练中记住的知识，也会读取提示中的上下文；但即使上下文改善了最终答案，我们仍不清楚它在模型内部怎样改变了模型对“这句话是真的还是假”的表示。本文希望打开这一黑箱：比较同一陈述在有、无上下文时的内部激活，判断上下文究竟是改变了真假判断所依赖的方向，还是让真假两类在表示空间中分得更开。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者声称提出首个关于上下文如何变换陈述级真值几何结构的系统刻画，沿模型各层比较有上下文与无上下文条件下真值向量的方向变化和相对幅度变化。
- 研究进一步区分相关、无关或随机上下文以及与参数知识一致或冲突的上下文，从而分析不同上下文性质是否引发不同的内部几何响应。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型可解释性研究，关注模型内部如何表示陈述的真假。已有研究发现，在大语言模型的残差流激活空间中，真实陈述与虚假陈述的表示往往可被一个线性方向区分，该方向称为“真值方向”或“真值向量”。与此同时，上下文学习与检索增强生成会向模型提供额外证据，但以往工作主要考察输出是否改善、探针能否迁移或模型是否检测到知识冲突，尚未直接刻画加入上下文后真值向量的几何结构如何变化。本文因此比较同一陈述在有、无上下文时的真值向量，并从方向旋转与长度变化两个维度分析上下文对真假表征的影响。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**残差流激活（residual-stream activation）**

Transformer各层会把中间计算结果累积到一个共享表示中，称为残差流；本文具体使用每层MLP之后的残差流激活。可将它理解为模型在某一层处理当前输入时形成的高维内部状态。

</div>
<div class="concept-item" markdown="1">

**真值向量（truth vector）**

真值向量是激活空间中区分真实陈述与虚假陈述的方向，本文通过真实样本与虚假样本激活表示的均值差来获得这一方向。向量越长，表示两类样本在该方向上的平均分离越明显。

</div>
<div class="concept-item" markdown="1">

**线性探测与几何表征**

若简单的线性分类器能依据内部激活区分真假，说明真假信息至少部分表现为空间中的线性几何结构。本文不以探针分类准确率或最终生成正确率为核心，而是直接比较上下文加入前后该结构的方向和尺度。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

对每个陈述 k，研究分别构造带上下文与不带上下文的输入，并改变提示中的候选选择，从而得到可按真实或虚假标签分组的样本。模型生成第一个回答词元时，研究者在每一层提取MLP后的残差流激活，再分别计算无上下文真值向量 $v_{k,nc}$ 与有上下文真值向量 $v_{k,c}$。输出不是对陈述真假的一次预测，而是两类逐层几何量：二者夹角用于衡量上下文是否旋转了真假区分方向，范数平方之比用于衡量上下文是否放大或压缩了真实与虚假表示之间的分离。该设定默认残差流中的真假差异可用线性方向近似，并聚焦内部表征而非模型最终输出行为。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$k$**

被分析的陈述或陈述实例索引。

</div>
<div class="notation-item" markdown="1">

**$v_{k,nc}$**

陈述 k 在无上下文条件下，由真实与虚假样本激活差异得到的真值向量；nc表示no context。

</div>
<div class="notation-item" markdown="1">

**$v_{k,c}$**

陈述 k 在加入上下文条件下得到的真值向量；c表示context。

</div>
<div class="notation-item" markdown="1">

**$\theta$**

$v_{k,nc}$ 与 $v_{k,c}$ 之间的夹角，用于度量加入上下文后的方向变化；文中还以 $\lVert v_{k,c}\rVert_2^2/\lVert v_{k,nc}\rVert_2^2$ 表示相对幅度变化。

</div>

</div>

**直接相关的工作**

- **Burns et al. (2023), Contrast-Consistent Search（CCS）**: 该工作以无监督方法从模型激活中提取真值方向，为“真假可由激活空间中的线性方向表示”提供了直接基础；本文接受这一表征视角，但进一步研究加入上下文后该方向如何旋转及改变幅度。
- **Bao et al. (2025)**: 该工作发现更强模型中会出现较一致的真值方向，并检验在事实陈述上训练的探针能否迁移到基于上下文的问答和摘要场景。其重点是同一探针能否跨设置泛化，而本文关注的是上下文引入前后真值向量本身的几何结构是否以及如何改变。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

上下文学习与检索增强生成可以在不重新训练模型的情况下补充知识，因而被用于高风险应用；然而，系统若只观察最终输出，就难以判断模型是否真正整合了相关证据、忽略了无关信息，或在外部证据与模型参数知识冲突时如何调整内部判断。理解这些过程有助于设计更可靠的上下文构造与检索增强系统。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **激活空间中的线性概念与真值方向分析**：既有研究从残差流激活中寻找可线性分离的方向，并训练线性分类器区分真陈述与假陈述。若两类激活可被线性边界稳定分开，就说明模型内部存在与真假相关的几何结构，常被概括为“真值方向”或“真值向量”。
- **上下文学习与检索增强生成**：这类方法把示例、文档或其他证据放入提示，使模型在不更新参数的情况下依据上下文生成答案。既有工作主要证明它们能够改善任务输出，但通常不直接测量上下文如何改变模型内部的真假表示。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 真值方向研究主要验证无上下文或固定输入条件下，真假陈述能否在激活空间中被线性分离；它没有比较加入上下文前后的真值向量，因此无法说明上下文是旋转了真假判别方向，还是仅改变了两类表示的分离强度。
- 上下文学习和检索增强研究多以答案正确率等外部行为评估效果，因而难以解释相关、无关以及与参数知识冲突的上下文为何会产生不同影响，也难以识别模型是否在内部以不同方式处理这些上下文。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究之间缺少一座连接内部真值表示与上下文处理机制的桥梁：尚未有系统研究沿网络层次比较同一类陈述在有、无上下文时的真值向量，并同时量化其方向变化与真假分离程度的变化；不同上下文类型是否对应可区分的几何变换也仍不明确。

</div>
<div markdown="1"><span>核心问题</span>

加入上下文后，大语言模型残差流中区分真、假陈述的向量会如何随层次改变其方向和幅度，以及这种变化是否会因上下文的相关性或其与模型参数知识的一致性而不同？

</div>
<div markdown="1"><span>作者直觉</span>

如果上下文真正参与了真假判断，它不应只改变最终生成的词，还应改变内部真假表示的几何关系。比较向量夹角可以判断模型是否改用了不同的判别方向；比较向量幅度则可以判断上下文是否让真、假表示分得更清楚。逐层观察这两个量，还能粗略揭示上下文影响是在网络早期形成、在中层整合，还是到后期才稳定下来。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法不是训练新的真实性分类器，而是对同一陈述构造“支持/反驳 × 有/无上下文”四种提示，记录语言模型生成首个输出词元时、各层残差流最后一个提示位置的激活。作者依据数据集真值标签，把支持与反驳生成映射为真实或虚假条件，并以两者激活之差定义逐陈述、逐层的真值向量；随后比较加入上下文前后的向量夹角与相对模长，从方向和真假表征分离强度两个维度刻画上下文造成的几何变换。
直观地说，方法先在模型内部找出“把真和假区分开”的箭头，再观察加入上下文后这支箭头是否转向、是否变长。转向表示模型表达真实性的内部方向发生变化，变长则表示真实与虚假表征在激活空间中被拉得更开。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造四类受控提示

针对每条陈述分别构造支持或反驳该陈述、且有或无上下文的四种提示；改变提示中的 Selected Choice，并随机打乱 Choice 选项顺序。作者还约束模型生成的第一个词元均为“)”以保证支持与反驳条件可比。

<div class="method-step__io" markdown="1">

**输入**：数据集中的陈述、对应上下文及真值标签。<br>
**输出**：同一陈述对应的支持-有上下文、反驳-有上下文、支持-无上下文和反驳-无上下文四个提示。

</div>

**直观理解**：这相当于只改变“是否给背景材料”和“要求站在哪一边”两个因素，其余条件尽量保持一致，从而把上下文的作用单独分离出来。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成文本并提取逐层残差流激活

让模型按提示继续生成，并在每一层提取用于产生首个输出词元的残差流激活，即提示最后一个词元位置的激活。该位置可通过因果注意力汇总整个输入，同时不受后续生成词元影响。

<div class="method-step__io" markdown="1">

**输入**：四类受控提示与待分析的语言模型。<br>
**输出**：每条陈述在四种提示条件下的逐层激活向量。

</div>

**直观理解**：作者在模型刚要开始回答的瞬间读取其内部状态，因为此时模型已经看完整个提示，但答案后文尚未反过来干扰测量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 依据真值标签构造真值向量

先用标签判断支持或反驳生成中哪一个对应真实、哪一个对应虚假，再分别在有上下文和无上下文条件下计算真实激活减去虚假激活。由此为每条陈述、每一层得到两个真值向量。

<div class="method-step__io" markdown="1">

**输入**：四种条件下的逐层激活以及数据集真值标签。<br>
**输出**：无上下文真值向量 $v^{(l)}_{k,\mathrm{nc}}$ 与有上下文真值向量 $v^{(l)}_{k,\mathrm{c}}$。

</div>

**直观理解**：真值向量是一支从“假”的内部表征指向“真”的内部表征的箭头；分别画出加上下文前后的箭头，才能比较上下文如何改变真实性编码。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 量化并聚合上下文引起的几何变化

计算两个向量的夹角 θ 作为方向变化，并计算其平方 L2 范数之比作为相对幅度；随后在数据集全部陈述上逐层取平均。作者还构造仅在真实或虚假一侧加入上下文的交叉条件向量，但其具体公式位于未提供的附录 A.2。

<div class="method-step__io" markdown="1">

**输入**：每条陈述、每一层的有上下文与无上下文真值向量。<br>
**输出**：每个数据集、每一模型层的平均方向变化与平均相对幅度曲线，以及交叉条件下的相对幅度分析量。

</div>

**直观理解**：夹角回答“真假方向是否被上下文扭转”，幅度比回答“真假两类是否被上下文进一步拉开”；逐层计算则显示这种变化在网络深度上的演化。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 有上下文与无上下文的真值向量

$$
\begin{aligned} v^{(l)}_{k,\mathrm{nc}} &= a^{(l)}_{k,\mathrm{True,nc}}-a^{(l)}_{k,\mathrm{False,nc}},\\ v^{(l)}_{k,\mathrm{c}} &= a^{(l)}_{k,\mathrm{True,c}}-a^{(l)}_{k,\mathrm{False,c}}. \end{aligned}
$$

**符号说明**

- $k$：陈述的索引。
- $l$：语言模型的层索引。
- $a^{(l)}_{k,\mathrm{True,nc}}$：陈述 k 在无上下文且对应真实生成时，第 l 层用于生成首个输出词元的残差流激活。
- $a^{(l)}_{k,\mathrm{False,nc}}$：陈述 k 在无上下文且对应虚假生成时，第 l 层的相应残差流激活。
- $a^{(l)}_{k,\mathrm{True,c}}$：陈述 k 在有上下文且对应真实生成时，第 l 层的相应残差流激活。
- $a^{(l)}_{k,\mathrm{False,c}}$：陈述 k 在有上下文且对应虚假生成时，第 l 层的相应残差流激活。
- $v^{(l)}_{k,\mathrm{nc}}$：陈述 k 在第 l 层的无上下文真值向量。
- $v^{(l)}_{k,\mathrm{c}}$：陈述 k 在第 l 层的有上下文真值向量。
- $\mathrm{nc},\mathrm{c}$：分别表示无上下文（no context）和有上下文（context）。

<div class="equation-explanation" markdown="1">

**直观理解**：两式都用“真实激活减虚假激活”来定义真假分离方向，区别只在于输入是否包含上下文。比较这两个向量即可把上下文的作用表示为激活空间中的几何变换。<br>
**原文位置**：第 3 节 Methodology，Truth Vectors from Residual Stream Activations，式 (2)–(3)

</div>

</div>

<div class="equation-block" markdown="1">

#### 方向变化与相对幅度

$$
\begin{aligned} \theta^{(l)}_{k} &= \arccos\!\left(\frac{v^{(l)}_{k,\mathrm{c}}\cdot v^{(l)}_{k,\mathrm{nc}}}{\left\|v^{(l)}_{k,\mathrm{c}}\right\|\left\|v^{(l)}_{k,\mathrm{nc}}\right\|}\right),\\ rm^{(l)}_{k,\mathrm{tc-fc}} &= \frac{\left\|v^{(l)}_{k,\mathrm{c}}\right\|_2^2}{\left\|v^{(l)}_{k,\mathrm{nc}}\right\|_2^2}. \end{aligned}
$$

**符号说明**

- $\theta^{(l)}_{k}$：陈述 k 在第 l 层加入上下文前后真值向量之间的夹角，即方向变化。
- $\cdot$：向量点积。
- $\|v\|$：向量的欧几里得长度。
- $rm^{(l)}_{k,\mathrm{tc-fc}}$：陈述 k 在第 l 层、真实和虚假两侧均加入上下文时的相对幅度。
- $\mathrm{tc-fc}$：true-context 与 false-context，即真实和虚假生成都使用上下文。
- $\|v\|_2^2$：向量 L2 范数的平方；按原文式 (6)，相对幅度使用平方范数之比。

<div class="equation-explanation" markdown="1">

**直观理解**：第一式通过归一化点积求夹角：角度越大，加入上下文后模型内部的真实性方向改变越明显。第二式比较有、无上下文时真值向量的平方长度，值大于 1 表示上下文扩大真假表征的分离，值小于 1 表示分离减弱；需注意，原文叙述和图 3 将其称为 L2 距离比，但式 (6) 明确写为平方范数之比，复现时应核对作者实现。<br>
**原文位置**：第 3 节 Methodology，Calculating Theta and Relative Magnitude，式 (4) 与式 (6)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该研究是对预训练语言模型进行前向生成和激活分析，没有提出可优化的损失函数，也没有训练真值向量或额外探针；数据集标签仅用于把支持/反驳生成映射为真实与虚假条件。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 四条件提示控制**

实验采用支持/反驳与有/无上下文的 2×2 配对设计，并统一首个生成词元、随机化选项顺序，以降低生成位置和选项排列造成的混杂。

> 直观理解：如果不同条件连回答格式或选项位置都不同，激活差异可能来自格式而非上下文；受控提示使后续几何比较更可信。

**2. 残差流真值向量提取**

对每一层，在提示最后一个位置读取生成首词元所用的残差流激活，并以真实条件激活减去虚假条件激活。真值标签只负责确定哪次生成属于真实或虚假，不涉及额外监督训练。

> 直观理解：单个激活包含大量内容，做真假配对相减能够突出与两种真实性条件之间差异相关的方向。

**3. 方向—幅度双重几何测量**

方向变化由有、无上下文真值向量的余弦夹角表示；相对幅度由有上下文向量与无上下文向量的平方 L2 范数之比表示，并对数据集中的陈述求平均。

> 直观理解：只看长度会漏掉“方向改变但长度不变”，只看角度又会漏掉“方向不变但真假距离扩大”，因此两项指标需要配合解释。

**训练与推理**

整个流程发生在推理与事后分析阶段。对每条陈述运行四次受控生成，记录各层在提示最后位置、生成首个输出词元时的残差流激活；依据真值标签重新标记真实和虚假生成后作差，得到有、无上下文真值向量。随后逐陈述、逐层计算夹角和相对幅度，并在数据集全部陈述上取平均；原文所示方法不包含参数更新，也未说明将所得向量用于新的在线预测。

**复现信息**

公平比较依赖三项关键控制：支持与反驳生成的首个词元都固定为“)”；Choice 中的选项顺序随机化，以减少位置偏差；激活统一取自提示最后一个词元位置，而不是后续生成序列。数据集级统计按陈述数 |$N_k|$ 对逐陈述指标作算术平均。对于仅向真实侧或虚假侧加入上下文的交叉相对幅度，节选只说明还计算 $v^{(l)}_{k,\mathrm{tc-fnc}}$ 和 $v^{(l)}_{k,\mathrm{tnc-fc}}$，完整定义位于附录 A.2，原文节选未提供足以复现的具体公式。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- DRUID的三个子集分别独立分析：Borderlines（982条，地理事实核查上下文）、Politifact（907条，政治事实核查上下文）和ScienceFeedback（618条，科学事实核查上下文）。三者均为真实世界数据，作用是检验不同事实核查领域中的上下文效应。原文给出数据行数、平均上下文词数及Flesch易读性，但所供章节未明确报告训练、验证和测试划分。
- MF2含1736条真实世界样本，以上下文较长的电影剧情梗概为证据；LegalBench则采用Corporate Lobbying任务中的CL-Bill和CL-Company两个子集，各500条，分别提供法律法案和公司描述。它们用于检验结论能否跨越叙事文本与高难度法律文本。为遵守数据集数量限制，此处按实验角色合并说明；原文未明确报告数据划分。
- ConflictQA为合成数据，包含两个各1244条的配对子集：ConflictQA-Parametric中的上下文与LLM参数知识一致，ConflictQA-Counter中的上下文与参数知识相冲突。该数据集用于直接比较知识一致性对真值向量几何变化的影响；原文未明确报告数据划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**方向变化θ**

衡量加入上下文前后两个真值向量之间的夹角，即上下文使“真假分离方向”旋转了多少。θ接近90°表示两个方向近似正交，较小表示方向更一致；该指标需要结合层位置和实验条件解释。 （无统一的越高或越低越好标准；它是描述性几何指标。更大的θ表示上下文对真值表示方向的重定向更强，而非模型性能必然更好。）

</div>
<div class="metric-item" markdown="1">

**真值向量相对幅度**

比较加入上下文后与无上下文时真值向量的长度，反映激活空间中真实陈述与虚假陈述表征的分离强度被放大还是减弱。 （无统一优劣方向；相对幅度增大表示真假表征分离更强，但仅凭该几何量不能推出回答准确率提高。）

</div>
<div class="metric-item" markdown="1">

**Flesch Reading Ease**

以0至100的分数近似上下文对人的阅读难度，分数越低表示文本越难。该量用于描述数据集，而不是评价模型输出或核心假设。 （不存在模型性能意义上的越高越好；较高仅表示文本更易读。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨四个LLM和四类数据，逐层比较加入上下文前后的真值向量方向

<div class="result-value" markdown="1">

作者报告：早期层中的有、无上下文真值向量大致正交；到中间层二者趋于一致；后期层则可能稳定，也可能继续增大。这里的“继续增大”依摘要语境指方向变化θ的后期走势，但不同模型或数据上的具体数值与显著性在所供材料中未报告。

</div>

这表明上下文并非在所有层以同一种方式改变真假表征：浅层的表示方向差异很大，中层逐渐形成较共同的真假判别方向，深层行为则依模型或数据而异。它描述的是内部激活几何轨迹，并不直接证明这些层已经正确理解上下文或产生了更准确的最终答案。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across four LLMs and four datasets, we find that (1) truth vectors are roughly orthogonal in early layers, converge in middle layers, and may stabilize or continue increasing in later layers;

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 加入上下文与无上下文条件的真值向量幅度比较

<div class="result-value" markdown="1">

作者报告加入上下文通常会增大真值向量幅度，即真实陈述和虚假陈述的激活表征在空间中分得更开。所供材料没有给出增幅、置信区间或逐数据集结果。

</div>

直观而言，上下文像是增强了模型内部区分真假的“信号强度”。但向量更长只说明表征分离增强，不等价于模型最终判断更准确，也不能单独排除提示长度、上下文词汇或其他激活尺度因素。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

(2) adding context generally increases the truth vector magnitude, i.e., the separation between true and false representations in the activation space is amplified;

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 相关与无关上下文在不同模型规模上的几何效应比较

<div class="result-value" markdown="1">

作者报告较大模型主要通过方向变化θ区分相关与无关上下文，而较小模型的差异主要体现在真值向量幅度上。所供材料未报告规模分界、效应量或统计检验。

</div>

这意味着不同规模模型可能使用不同的内部几何机制响应上下文：大模型更像是在旋转真假判别方向，小模型更像是在调节既有方向上的信号强弱。这是跨所选3B至12B模型得到的关联性观察，不能据此断言模型规模本身导致了该机制，也不能外推至所有架构或更大模型。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

(3) larger models distinguish relevant from irrelevant context mainly through directional change (θ), while smaller models show this distinction through magnitude differences.

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

- 无上下文提示条件：作为几何参照，先从不含上下文的陈述激活中构造真值向量，再与加入上下文后的真值向量比较方向和幅度。原文未设置传统任务基线模型。
- 无关上下文条件：与相关上下文条件比较，用来判断模型是否会根据上下文与陈述的关联程度产生不同的几何响应；所供章节未给出该条件的具体构造细节或单独分数。
- ConflictQA-Parametric条件：将与模型参数知识一致的上下文作为参照，与ConflictQA-Counter的冲突上下文比较，从而隔离知识一致性这一因素。
- 跨规模模型比较：实验采用Llama-3.1-8B-Instruct、Mistral-Nemo-12B-Instruct、Qwen3-4B-Instruct和SmolLM3-3B四个指令微调模型。这不是训练方法基线，而是用于检验几何现象能否跨模型家族和3B至12B规模复现。

**实验想回答的问题**

- 加入上下文后，LLM残差流中的陈述级“真值向量”在各网络层如何发生几何变化，尤其是方向变化θ和相对幅度如何变化？
- 这些几何变化是否随模型规模、上下文相关性以及上下文与模型参数知识的一致或冲突关系而呈现系统差异？

**实验实现**

实验只保留模型在四种提示下均遵循指令的陈述，以减少格式失败或不服从指令对激活分析的干扰；四种提示的具体文本在所供章节中未展开。作者使用Hugging Face API对四个现成的指令微调模型进行推理，并采用贪心解码以提高可复现性。实验在NVIDIA A100和H100 GPU上完成，总计算量约500 GPU小时。核心评估是在网络各层提取残差流激活，比较有、无上下文时真值向量的方向变化θ和相对幅度；所供章节仅引用式(5)与式(7)，未提供公式正文，因此此处不补造其具体表达式。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过残差流中的真值向量分析上下文如何几何变换 LLM 的真假表征，属于机制可解释性研究。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`3ef27fd4e30402c3d72d5ec2ec0b0a164bb0ccdac5bb98529f3aa8912ed2297f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
