---
title: "[论文解读] INSPIRE: An Internalize-Then-Improve Approach for Example-Driven Mathematical Reasoning"
description: "[arXiv 2608.27501][对齐 / RLHF] 原文未明确报告。"
arxiv_id: "2608.27501"
announcement_date: "2026-08-31"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:36:38.702473+00:00"
source_sha256: "f92a563a8f148d720ac1e78acbd2544fe86a61747db524ada85cb63e46930b4a"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型数学推理"
  - "例子驱动推理"
  - "反例构造"
  - "偏好优化"
  - "分阶段训练"
  - "Reference-Guided Student Internalization"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.27501</p>

# INSPIRE: An Internalize-Then-Improve Approach for Example-Driven Mathematical Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Shuai Wang, Jiayi Kuang, Yinghui Li, Haojing Huang, Xinnian Liang, Ying Shen, Liang Lin</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Sun Yat-sen University；Affiliation: Tsinghua University；Affiliation: ByteDance Inc；Affiliation: Peng Cheng Laboratory</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27501v1) · [PDF 下载](https://arxiv.org/pdf/2608.27501v1) · **关键词** 大语言模型数学推理, 例子驱动推理, 反例构造, 偏好优化, 分阶段训练, Reference-Guided Student Internalization<br>
**代码**: [https://github.com/Shea-code-xxx/INSPIRE-code](https://github.com/Shea-code-xxx/INSPIRE-code)

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

本文位于大语言模型（LLM）数学推理与偏好优化交叉领域。现有数学推理方法主要通过监督微调、数据增强和基于强化学习的后训练提升最终答案正确率，但这种结果导向的训练不一定能证明模型真正理解数学概念。本文关注更具体的概念层推理能力：面对数学命题时，模型能否主动构造例子或反例，以检验命题的适用边界，而不是仅套用抽象定理或记忆已有解题模式。研究的核心训练设定是：利用模型生成的候选答案构造偏好数据，再通过分阶段的偏好训练，使模型先学会采用例子驱动的推理方法，随后提高采用该方法时的答案正确性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**例子驱动推理与反例**

例子驱动推理是通过构造具体对象来检验、说明或应用一个数学命题；反例则是找到满足前提但不满足结论的对象，从而证明命题并非普遍成立。对本文而言，关键不只是答案是否正确，还包括模型是否主动采用这种具体化、边界检验的分析策略。

</div>
<div class="concept-item" markdown="1">

**偏好优化**

偏好优化使用成对或排序的候选回答，告诉模型哪个回答更值得偏好，并直接调整模型使其更倾向于生成优选回答。本文中的偏好不是单一的最终答案偏好，而是依据方法采用情况、推理质量和正确性等维度构造。

</div>
<div class="concept-item" markdown="1">

**分布偏移**

分布偏移是指训练样本的表达方式、推理结构或来源分布与当前模型实际生成的内容不同。若直接把更强外部模型的回答作为优选样本，目标模型可能模仿外部回答的表面风格，而未必真正内化其中的推理策略。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定数学问题或数学陈述 $x$，以及可供参考的高质量推理示例或参考推理方法，目标是训练一个策略模型生成回答 $y$。回答不仅应给出正确结论，还应在适当情况下主动使用例子或反例检验概念和定理边界。本文假设基础模型在该能力上较弱，因此单纯从自身分布采样得到的候选回答通常质量不足；同时，能力学习具有阶段性：模型需要先学会采用例子驱动方法，再学会在采用该方法的基础上保证答案正确。训练过程因此需要同时处理候选偏好数据质量、模型自身分布一致性，以及方法能力与正确性能力之间的先后关系。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入的数学问题或数学陈述。

</div>
<div class="notation-item" markdown="1">

**$y$**

模型针对输入 $x$ 生成的完整回答，通常包含推理过程与最终结论。

</div>
<div class="notation-item" markdown="1">

**$\pi$**

策略模型，即用于生成回答的语言模型分布；在本文语境中，候选回答应尽量来自该模型自身的生成分布。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{D}$**

偏好训练数据集，包含同一输入下的候选回答及其依据方法、推理和正确性等评价形成的偏好关系。

</div>

</div>

**直接相关的工作**

- **ConceptMath 与 CounterMath**: 这些基准揭示了当前 LLM 在概念层数学推理上的不足，尤其是通过例子和反例进行理解与区分的能力。本文的问题设定正是针对这一缺口，但重点从评测转向如何通过定向偏好训练主动诱导模型采用例子驱动推理。
- **Direct Preference Optimization（DPO）及其变体**: DPO、IPO 和 SimPO 等方法为直接利用偏好数据优化数学推理模型提供了基础；Step-DPO、Full-Step-DPO 和 Math-Shepherd 进一步引入推理步骤或过程级监督。本文沿用偏好优化的基本思路，但认为仅以最终答案正确性作为偏好信号不够，因此引入多维评价与分阶段训练，并通过 Reference-Guided Student Internalization 缓解弱模型难以生成高质量优选回答的问题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

INSPIRE是一套“先内化策略、再提高正确性”的两阶段偏好学习方法。输入包括数学问题集$\mathcal{D}$、对应参考解答$\mathcal{G}$、经监督微调得到的基础策略$\pi_0$以及评审模型$\mathcal{J}$；输出是最终策略$\pi_2$。方法先让$\pi_0$同时进行普通自采样和参考解答引导的生成，再由$\mathcal{J}$按方法使用$m$、推理质量$r$和答案正确性$c$三个维度评分。随后，第一阶段M-DPO依据$m$构造偏好对，使模型$\pi_1$学会主动采用基于例子的分析；第二阶段重新采样，并依据$c$与$r$构造偏好对，通过C-DPO得到更正确、更严谨且不遗忘示例推理策略的$\pi_2$。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选回答生成与RGSI增强

一部分候选从$\pi_0(\cdot\mid x)$普通采样，另一部分通过RGSI从$\pi_0(\cdot\mid x,r)$生成；参考解答只提供推理引导，实际文本仍由当前策略产生。

<div class="method-step__io" markdown="1">

**输入**：问题$x\in\mathcal{D}$、参考解答$r=\mathcal{G}(x)$和基础策略$\pi_0$。<br>
**输出**：兼有基础模型自然回答与参考引导回答的候选集合。

</div>

**直观理解**：只让能力较弱的学生独立作答，答案可能都采用不了目标方法；给学生看参考思路后再让其用自己的语言重写，既能提高候选质量，又不会完全变成外部教师模型的文本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 三维量规评分

评审模型$\mathcal{J}$独立给出方法分$m\in[0,2]$、推理分$r\in[0,3]$和正确性分$c\in[0,1]$；三者分别衡量是否使用示例分析、论证是否连贯完整以及最终答案是否正确。

<div class="method-step__io" markdown="1">

**输入**：每道问题及其全部候选回答。<br>
**输出**：带有三维评分$(m,r,c)$的候选回答池。

</div>

**直观理解**：单看答案对错无法判断模型是否真正用了目标策略，因此这里把“用了什么方法”“过程讲得是否合理”和“结论是否正确”分开检查。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段一：M-DPO方法内化

选择满足$m(y_w)-m(y_l)\geq1$且$r(y_w),r(y_l)\geq1$的偏好对，并优先保留$r(y_w)$较高的样本；以$y_w$为优选回答、$y_l$为劣选回答执行M-DPO，得到$\pi_1$。

<div class="method-step__io" markdown="1">

**输入**：带评分的候选池与参考策略$\pi_0$。<br>
**输出**：初步掌握基于例子进行数学分析的中间策略$\pi_1$。

</div>

**直观理解**：这一阶段先不强迫模型同时解决所有问题，而是重点奖励“确实会用例子且论证不是胡乱拼接”的回答，相当于先学会解题方法。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段二：C-DPO正确性精炼

首先构造$c(y_w)=1$、$c(y_l)=0$且$r(y_w)\geq1$的正确—错误偏好对；对均正确的候选，再以$r(y_w)-r(y_l)\geq1$构造质量偏好对，并以$m$作为次级排序依据。

<div class="method-step__io" markdown="1">

**输入**：中间策略$\pi_1$、问题集$\mathcal{D}$、重新采样的候选回答及其三维评分。<br>
**输出**：以正确性为主、兼顾论证质量和示例策略保持的偏好数据$\mathcal{D}_2$。

</div>

**直观理解**：模型已经学会使用例子后，再训练它辨别哪些例子和论证真正支持正确结论；在答案都正确时，则进一步偏好更严谨的推导。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### RGSI参考引导生成

$$
\tilde{y}\sim\pi_{0}(\cdot\mid x,r)
$$

**符号说明**

- $\tilde{y}$：由基础策略生成的参考引导候选回答。
- $\pi_{0}$：经监督微调的基础策略，也是第一阶段的初始化与参考策略。
- $x$：待求解的数学问题。
- $r$：问题对应的真实参考解答，用于提供推理指导。

<div class="equation-explanation" markdown="1">

**直观理解**：该式的关键不是让参考解答直接充当训练答案，而是将其作为额外上下文交给基础策略。这样生成结果通常比纯自采样更可能展示示例推理，同时其措辞和生成行为仍来自待训练模型，有利于构造既有质量差异、又较贴近策略自身分布的偏好对。<br>
**原文位置**：第3.1节，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 两阶段DPO优化目标

$$
\begin{aligned}
\mathcal{L}_{\mathrm{M\text{-}DPO}}&=-\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}_1}\!\left[\log\sigma\!\left(\beta_m\log\frac{\pi_\theta(y_w\mid x)}{\pi_0(y_w\mid x)}-\beta_m\log\frac{\pi_\theta(y_l\mid x)}{\pi_0(y_l\mid x)}\right)\right],\\
\mathcal{L}_{\mathrm{C\text{-}DPO}}&=-\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}_2}\!\left[\log\sigma\!\left(\beta_c\log\frac{\pi_\theta(y_w\mid x)}{\pi_1(y_w\mid x)}-\beta_c\log\frac{\pi_\theta(y_l\mid x)}{\pi_1(y_l\mid x)}\right)\right].
\end{aligned}
$$

**符号说明**

- $\mathcal{L}_{\mathrm{M\text{-}DPO}}$：第一阶段的方法导向DPO损失。
- $\mathcal{L}_{\mathrm{C\text{-}DPO}}$：第二阶段的正确性导向DPO损失。
- $x$：数学问题。
- $y_w$：按照相应阶段量规筛选出的优选回答。
- $y_l$：相对于优选回答的劣选回答。
- $\mathcal{D}_1$：以方法分差异为核心构造的第一阶段偏好对集合。
- $\mathcal{D}_2$：由正确—错误对、正确答案间质量对及部分回放样本组成的第二阶段偏好集合。
- $\pi_\theta$：参数为待优化变量的当前策略。
- $\pi_0$：第一阶段的固定参考策略与训练初始化。
- $\pi_1$：M-DPO训练后的中间策略，也是第二阶段的固定参考策略与初始化。
- $\beta_m$：控制第一阶段偏好优化强度的温度参数。
- $\beta_c$：控制第二阶段偏好优化强度的温度参数。
- $\sigma$：Sigmoid函数，将优选回答相对优势映射为概率形式。

<div class="equation-explanation" markdown="1">

**直观理解**：两个目标都提高优选回答相对于劣选回答的生成倾向，同时用固定参考策略约束模型不要偏离原分布过远。区别在于偏好数据和参考策略：M-DPO依据方法使用情况训练，并以$\pi_0$为参照；C-DPO依据正确性与论证质量训练，并以已经掌握目标方法的$\pi_1$为参照，因此第二阶段是在既有能力上精炼，而不是从头重新学习。<br>
**原文位置**：第3.2节，公式(3)与公式(5)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练并非直接优化量规分数的加权和，而是先根据量规筛选回答对，再用DPO最大化优选回答相对劣选回答的隐式奖励差。第一阶段要求$m(y_w)-m(y_l)\geq1$，同时用$r(y_w)\geq1$和$r(y_l)\geq1$排除逻辑过差的回答，因此主要学习“是否采用示例分析”；得到$\pi_1$后，第二阶段主要使用$c(y_w)=1$对$c(y_l)=0$的偏好，并要求$r(y_w)\geq1$，避免奖励靠错误推理偶然猜对的答案。若两个回答均满足$c=1$，则以$r(y_w)-r(y_l)\geq1$偏好更严谨者；方法分$m$继续作为次级标准，且$\mathcal{D}_2$加入部分$\mathcal{D}_1$回放样本。由此，优化目标与学习顺序一致：先改变模型选择推理策略的倾向，再提高该策略下的答案可靠性与论证质量。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 三维评价量规**

量规将回答质量分解为方法$m$、推理$r$和正确性$c$：$m$取$0$至$2$分，判断示例分析的使用程度；$r$取$0$至$3$分，判断逻辑连贯性与完整性；$c$取$0$或$1$，判断最终答案。DeepSeek-V3.2依照附录A中的提示独立评判三个维度。

> 直观理解：该模块解决“答案正确但没有学会目标方法”无法被单一正确性标签识别的问题。分维度评分也让两个训练阶段可以使用不同信号，而不是把方法学习、论证质量和答案正确性混成一个模糊总分。

**2. 参考引导的学生内化RGSI**

RGSI让基础策略在问题$x$和参考解答$r$的联合条件下生成$\tilde y\sim\pi_0(\cdot\mid x,r)$。它不同于仅从$\pi_0(\cdot\mid x)$采样，也不同于直接使用教师模型答案：生成器仍是待训练策略$\pi_0$，参考解答仅用于提升候选中的方法与推理质量。

> 直观理解：DPO需要同一道题上存在明显的优劣回答，但能力较弱的模型自行采样时可能产生一批同样不会使用示例的答案。RGSI通过“看参考后自己讲一遍”制造较好的候选，同时尽量减少直接采用外部模型文本造成的分布错配。

**3. 阶段式量规偏好训练**

阶段一以方法差异为核心形成$\mathcal{D}_1$，从$\pi_0$优化得到$\pi_1$；阶段二由$\pi_1$重新采样，以正确性差异和正确答案间的推理质量差异形成$\mathcal{D}_2$，再得到$\pi_2$。第二阶段把部分$\mathcal{D}_1$作为回放数据，并继续用$m$辅助排序，从数据选择和训练回放两方面保持已学策略。

> 直观理解：作者把能力获得视为有先后顺序的过程：模型应先学会“想到用例子”，再学会“把例子用对”。若一开始同时要求方法、逻辑和答案全部最优，较弱模型可能无法获得清晰、可执行的学习信号。

**训练与推理**

完整训练过程如下：先对每个问题使用$\pi_0$采样$K$个普通回答，并额外利用真实解答$\mathcal{G}(x)$生成RGSI回答；原文未在所给章节中明确报告$K$的具体取值。评审模型$\mathcal{J}$为所有候选标注$(m,r,c)$，据此形成$\mathcal{D}_1$并以$\pi_0$为初始化和参考策略训练M-DPO，得到$\pi_1$。随后必须使用$\pi_1$重新采样，而不是完全复用第一阶段候选，因为此时模型分布及示例推理能力已经改变；重新评分后构造正确性对与质量对，将其同部分第一阶段回放对合并为$\mathcal{D}_2$，再以$\pi_1$为初始化和参考策略训练C-DPO，最终输出$\pi_2$。推理时不需要参考解答、评审模型或两阶段筛选流程，只需把新数学问题输入$\pi_2$并按常规自回归方式生成推理与答案；所给原文未明确报告额外的推理解码设置。

**复现信息**

复现时最关键的是保持训练与评分定义一致。评分器采用DeepSeek-V3.2，方法、推理和正确性三个维度的范围分别为$0$至$2$、$0$至$3$和$0$至$1$，完整评分提示位于附录A，细化量规位于附录G；若更换评审模型或提示，偏好对组成可能随之变化。基础模型先进行SFT，学习率为$1\times10^{-5}$并训练$3$个周期；两个DPO阶段均使用学习率$5\times10^{-6}$、$\beta=0.2$并训练$3$个周期，论文称不同模型规模使用相同超参数。RGSI的具体生成实现位于附录C，但当前摘录没有给出采样数量$K$、解码参数、回放比例及候选对数量，因此这些信息不能从所给文本中可靠补全。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- BrokenMath训练数据：约$15K$道定理证明题，来源于DeepTheorem和NuminaMath-1.5；作者依据预定义标准筛选涉及例子、反例或构造的问题，并经人工核验得到$1,275$道训练题。其作用是提供面向example-driven reasoning的领域训练样本。每道题从基础模型采样$16$个候选回答，并通过RGSI额外生成$4$个回答；Stage 1和Stage 2各形成约$14,000$个偏好训练对。原文未明确报告训练集的进一步划分。
- CounterMath测试集：专门评估example-driven reasoning的基准，测试模型能否通过构造例子或反例检验定理条件、支持判断。实验使用其四项指标中的三项作为核心汇报指标：Macro-F1、Examples和Strict/Loose Align中的对齐结果；由于任务要求最多列出三项指标，具体对齐指标在下方指标说明中合并为“对齐指标”。原文未明确报告测试集规模及独立验证集划分。
- 分布外一般数学推理基准：GSM8K、MATH500、AIME 2024、GAOKAO-mathQA和MMLU-collegeMath，用于检验专门训练是否造成一般数学能力退化。作者在三种模型配置上比较Base、Stage 1和完整的Stage 1 + Stage 2；这些数据集不是训练数据，承担外部泛化与副作用检查的作用。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Macro-F1**

对CounterMath判断结果的宏平均F1，综合不同类别上的精确率与召回率，适合衡量整体判断质量而不让多数类别完全主导结果。 （越高越好，因为它表示模型在各判断类别上的综合预测更准确、更均衡。）

</div>
<div class="metric-item" markdown="1">

**Examples**

模型回答中实际采用例子或反例进行推理的比例，用来测量是否采取了任务要求的推理方法，而不只是给出抽象结论。 （越高越好，但单独升高不等于推理正确；模型可能构造了无关、无效或未针对定理边界的例子。）

</div>
<div class="metric-item" markdown="1">

**Strict/Loose Align**

模型所构造例子与参考答案的匹配程度：Strict Align要求更严格的一致，Loose Align允许更宽松但仍被判定为相符的表达或构造。二者共同衡量答案与参考构造的对齐程度，而不只看是否使用了例子。 （越高越好；不过作者指出，模型可能构造出有效但不同于参考答案的例子，因此较低的绝对对齐分数不必然表示推理无效。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### CounterMath上的主结果：Qwen2.5-Math-7B-Instruct从Base、SFT、Stage 1到完整两阶段训练的渐进变化。

<div class="result-value" markdown="1">

在Qwen-7B上，SFT后的Macro-F1为$39.06$、Examples为$77.63\%$；加入Stage 1后分别升至$43.05$和$81.33\%$；完整训练进一步达到Macro-F1 $45.91$、Examples $84.79\%$、Strict Align $17.30$和Loose Align $20.07$。相对SFT，完整训练的Macro-F1提高$6.85$，Examples提高$7.16$个百分点；表中相对Base的完整阶段增益分别为$7.24$、$9.54$、$2.99$和$3.46$。

</div>

作者的解释是，Stage 1首先让模型愿意并能够使用例子，Stage 2再改善例子的针对性和正确性。这个结果支持“先内化方法、后改进质量”的训练顺序，而不是仅靠SFT模仿参考答案。它并不能证明所有性能提升都来自真正的数学概念内化，因为Examples和judge评分仍是行为层面的代理指标，且对齐指标的绝对值仍然较低。

<div class="result-source" markdown="1">

来源：Section 4.2 Main Results；Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the 7B scale, Stage 1 increases Examples from 77.63% to 81.33% and F1 from 39.06 to 43.05, confirming that method-oriented preference learning encourages example-based reasoning adoption.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨规模与跨模型家族的稳定性，以及与外部开源模型的比较。

<div class="result-value" markdown="1">

完整训练后，Qwen-1.5B的Macro-F1为$39.02$、Examples为$76.32\%$，相对其Base分别提高$3.31$和$7.08$个百分点；Llama-8B的Macro-F1为$50.27$、Examples为$93.09\%$，相对Base分别提高$8.99$和$16.36$个百分点。Qwen-7B完整模型的Macro-F1为$45.91$，高于Qwen2.5-Math-72B-Instruct的$41.89$，并接近Qwen3-32B的$45.93$；Llama-8B与Qwen-7B的Examples分别为$93.09\%$和$84.79\%$，均高于DeepSeek-R1的$80.59\%$。

</div>

这些结果说明方法增益并不局限于一个规模或一个模型家族，并显示针对性训练可以部分弥补参数量差距。这里的“超过更大模型”只是在CounterMath及所报告指标上的比较，不意味着INSPIRE在所有数学任务、所有能力维度或总体智能上超过这些模型；商业模型与开源模型之间的训练条件也不完全可控。

<div class="result-source" markdown="1">

来源：Section 4.2 Main Results；Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Compared with open-source models, our 7B model surpasses Qwen2.5-Math-72B-Instruct (F1: 41.89) and approaches Qwen3-32B (F1: 45.93).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 分布外一般数学推理：在GSM8K、MATH500、AIME 2024、GAOKAO-mathQA和MMLU-collegeMath上比较Base与完整训练。

<div class="result-value" markdown="1">

三种模型配置在完整训练后均未出现整体退化。Qwen-7B在GSM8K由$94.54$升至$95.68$、AIME 2024由$13.33$升至$20.00$；Llama-8B在MATH500由$47.80$升至$49.60$、MMLU-collegeMath由$42.00$升至$45.00$；Qwen-1.5B在MMLU-collegeMath由$70.00$升至$73.00$。Llama-8B和Qwen-1.5B的AIME 2024分数保持不变，分别为$6.67$和$10.00$。

</div>

作者据此认为，面向例子和反例的专门训练没有损害一般数学推理，并可能改善分析策略。由于这些基准的任务形式、难度和分数粒度不同，结果更适合解释为“未观察到明显负迁移”，不能据此断言对所有分布外数学任务都有正迁移；尤其AIME只有$30$道题，分数变化具有较粗粒度。

<div class="result-source" markdown="1">

来源：Section 4.3 Out-of-Distribution Evaluation；Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 3, the final model consistently maintains or improves performance across all benchmarks on all three model configurations.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- CounterMath的对齐指标依赖参考构造，作者承认模型可能构造有效但不同于参考答案的例子，因此Strict Align和Loose Align的绝对分数可能低估真实有效性；同时Examples只测量是否使用例子，不能单独保证例子相关、有效或结论正确。
- 候选筛选、rubric评分和主要评价均包含模型判断环节：训练候选由DeepSeek-R1辅助识别，训练评分使用DeepSeek-V3.2，虽以GPT-4o进行了交叉评估，但仍不能完全排除自动评审偏差。原文还未明确报告CounterMath规模、数据划分和多随机种子方差，因此结果稳定性与统计显著性仍需进一步核验。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Base模型：未经本方法训练的Qwen2.5-Math-7B-Instruct、Qwen2.5-Math-1.5B-Instruct和Llama-3.1-8B-Instruct，用于测量各训练阶段相对原始模型的增益。
- SFT：在ground-truth reference上进行监督微调，作为冷启动和模仿学习对照，用于判断仅提供标准解答格式是否足以获得性能提升。
- 正确性导向DPO：只以最终答案正确性构造偏好信号的标准直接偏好优化，用于检验“只优化答案正确”是否会忽视或抑制例子驱动策略。
- 外部模型基线：包括商业模型Claude-4.5-Sonnet、Gemini-3 Pro等，以及从$3B$到$72B$的开源通用或数学专用模型，用于比较INSPIRE与不同规模、不同训练来源模型的绝对水平；其中Qwen2.5-Math-72B-Instruct和Qwen3-32B是检验小模型是否能接近或超过更大开源模型的关键参照。

**实验想回答的问题**

- 分阶段训练是否能在不同模型规模与模型家族上，持续提升面向反例、例子和构造的数学推理能力，而不仅仅是提高最终答案正确率？
- RGSI与“先学习推理方法、再学习判断正确性”的训练设计，是否比单纯监督微调、正确性导向的偏好优化或混合训练更有效，并且不会损害分布外的一般数学推理能力？

**实验实现**

主实验以Qwen2.5-Math-7B-Instruct为基础模型，并将同一流程与超参数应用于Qwen2.5-Math-1.5B-Instruct和Llama-3.1-8B-Instruct，以检验规模和模型家族泛化。流程先用ground-truth references进行SFT冷启动，再进行两个阶段的LoRA偏好训练：Stage 1学习采用例子或反例的方法，Stage 2在此基础上优化构造和判断的正确性。训练使用LLaMA-Factory，SFT与DPO均采用LoRA；DeepSeek-V3.2负责rubric评分，推理使用vLLM和greedy decoding，实验使用$4$张NVIDIA L20 GPU。作者另以GPT-4o重新评分进行交叉评估。正确性-only DPO敏感性实验固定学习率为$5\times10^{-6}$、训练$3$个epoch，并改变偏好温度参数$\beta$；原文未明确报告所有主实验的完整超参数，完整设置位于Appendix E。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 训练策略消融：比较正确性-only DPO、Chosen SFT、Mixed DPO、单独M-DPO、单独C-DPO与完整顺序训练；均在Qwen2.5-Math-7B-Instruct上进行。 | 以SFT为起点时，正确性-only DPO的Macro-F1为$39.38$、Examples为$73.19\%$；Chosen SFT为$41.75$和$79.52\%$；Mixed DPO为$42.72$和$81.17\%$；单独M-DPO为$43.05$和$81.33\%$；单独C-DPO为$40.27$和$77.88\%$；完整方法达到$45.91$和$84.79\%$。在表4中，完整方法的Strict Align和Loose Align也最高，分别为$17.30$和$20.07$。 | M-DPO优于C-DPO表明先学习方法是关键；Mixed DPO即使使用更多合并数据仍不如单独Stage 1，支持方法目标与正确性目标可能产生冲突梯度的解释。正确性-only DPO降低Examples，说明只奖励最终答案正确可能压制例子使用。该消融验证了组件和顺序的重要性，但没有完全分离数据量、训练步数或偏好对质量等潜在混杂因素。 | Section 4.4 Effect of Training Strategy；Table 4<br><span class="experiment-evidence">Mixed DPO, trained on the shuffled union of Stage 1 and Stage 2 preference pairs in a single pass, underperforms even Stage 1 alone (42.72 vs. 43.05) despite using more data, suggesting that method and correctness objectives introduce conflicting gradients when mixed.</span> |
| Stage 1的候选回答增强策略消融：Self-sampling、Teacher rewriting与RGSI。 | 相对SFT基线的Macro-F1为$39.06$、Examples为$77.63\%$，Self-sampling达到$40.40$和$78.55\%$，Teacher rewriting仅达到$39.14$和$74.01\%$，RGSI达到$43.05$和$81.33\%$；RGSI的Strict Align和Loose Align分别为$16.53$和$19.08$，同样高于另外两种增强方式。 | Self-sampling产生的候选质量差异不足，难以形成有效偏好信号；Teacher rewriting虽然回答质量高，却可能因教师与学生的生成风格存在分布偏移，使模型学习表面风格差异。RGSI让学生先理解参考答案，再在自身分布中重生成，因而形成更适中的、持续可学习的偏好差异。该解释与Figure 3中的训练动态一致，但仍依赖judge对候选质量的评分。 | Section 4.4 Effect of Reference-Guided Student Internalization；Figure 3；Table 5<br><span class="experiment-evidence">RGSI maintains moderate margins (a) with gradual accuracy growth (c), providing meaningful learning signals throughout.</span> |

**定性案例**

- 附录F的测度论案例展示了三阶段的定性变化：基础模型直接套用“从上连续性”定理，却没有检查前提$m(E_1)<\infty$，因而错误判断；Stage 1开始主动构造例子，但所选例子满足定理前提，只能确认而不能挑战定理；Stage 2识别出关键前提，并构造违反该前提的反例$E_n=[n,\infty)$，最终得到正确判断。该案例直观说明Stage 1获得“使用例子”的策略，Stage 2进一步学习“针对定理边界构造有效例子”的质量要求；它是机制示例而非统计性证明。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出分阶段偏好优化方法，通过示例驱动的概念内化提升大型语言模型的数学推理能力。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`f92a563a8f148d720ac1e78acbd2544fe86a61747db524ada85cb63e46930b4a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
