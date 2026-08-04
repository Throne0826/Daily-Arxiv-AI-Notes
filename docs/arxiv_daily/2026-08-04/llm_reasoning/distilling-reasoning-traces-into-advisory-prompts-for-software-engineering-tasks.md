---
title: "[论文解读] Distilling Reasoning Traces into Advisory Prompts for Software Engineering Tasks"
description: "[arXiv 2608.00437][LLM Reasoning] 本文从小型混合推理模型在“思考”与“不思考”模式下答案正确性发生变化的案例中提炼通用建议，并将其作为简短提示注入后续任务，以检验能否在免训练、较低推理成本下提高软件工程任务的可靠性，以及这些建议能否跨模型迁移。"
arxiv_id: "2608.00437"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:04:10.264336+00:00"
source_sha256: "54a0d7950ed1a4c40d9a8383ffc20d663545b86d39e596921f0d7e97c5f30e48"
tags:
  - "LLM Reasoning"
  - "软件工程语言模型"
  - "混合推理模型"
  - "推理轨迹蒸馏"
  - "建议性提示"
  - "推理时错误削减"
  - "小语言模型"
  - "提示迁移"
  - "共同模式失效"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.00437</p>

# Distilling Reasoning Traces into Advisory Prompts for Software Engineering Tasks

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Faizan Faisal, Prem Devanbu, Toufique Ahmed</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.00437v1) · [PDF 下载](https://arxiv.org/pdf/2608.00437v1) · **关键词** 软件工程语言模型, 混合推理模型, 推理轨迹蒸馏, 建议性提示, 推理时错误削减, 小语言模型, 提示迁移, 共同模式失效<br>


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

本文从小型混合推理模型在“思考”与“不思考”模式下答案正确性发生变化的案例中提炼通用建议，并将其作为简短提示注入后续任务，以检验能否在免训练、较低推理成本下提高软件工程任务的可靠性，以及这些建议能否跨模型迁移。

**不用术语来说**：较小的语言模型速度快、成本低，也适合资源受限设备，但在生成代码、预测程序行为或识别不存在的方法时容易犯错；开启完整思考模式通常能减少部分错误，却会消耗更多计算资源和输出词元。论文要解决的是：能否让模型回顾那些“认真思考后才答对”的案例，把其中反复出现的教训压缩成几条短建议，使模型以后即使不开启完整思考也能少犯类似错误。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出一种免训练的建议提示蒸馏思路：筛选同一学生模型在思考与非思考模式之间发生正确性翻转的案例，由更强的教师模型诊断推理为何有效或有害，再将多个诊断归纳为可复用的简短建议提示。
- 将研究目标明确扩展到三类实际价值：考察蒸馏提示在未参与构造的样本上能否提高表现、能否形成优于完整思考模式的准确率与词元成本折中，以及源模型的建议能否迁移到具有相似失误模式的其他模型。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于面向软件工程任务的语言模型推理与提示工程研究。语言模型可用于代码生成、程序输入/输出预测、异常预测和方法幻觉检测，但其训练语料包含大量人类编写且可能有缺陷的代码，模型自身也可能形成错误泛化，因此不能仅依赖“无缺陷语料”消除错误；重新训练或微调又通常成本较高。混合推理模型允许在非思考模式与思考模式之间切换：后者通过生成额外推理轨迹提高部分任务的正确率，却增加推理时间和令牌消耗。本文关注一种无需更新模型参数的折中方案，即从思考模式纠正或改变答案的案例中提炼简短、可复用的建议性提示，再把提示加入后续任务输入，以期让较小模型在非思考模式下获得部分推理收益。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**混合推理模型**

同一模型可在非思考模式下直接作答，也可在思考模式下先产生较长的中间推理轨迹再给出答案。本文利用两种模式在相同样例上的正确性差异来定位值得总结的错误。

</div>
<div class="concept-item" markdown="1">

**推理轨迹蒸馏**

这里的“蒸馏”不是训练一个新模型，而是让教师模型把冗长推理轨迹及其中暴露的失误压缩为简短的通用行为规则。例如，将具体字符串与数值比较导致异常的案例概括为“判断执行结果前先检查操作数类型兼容性”。

</div>
<div class="concept-item" markdown="1">

**共同模式失效**

共同模式失效指不同模型可能在相同或相似输入上犯同类错误。若这种错误规律可以由一个模型的案例揭示，那么从该模型提炼的建议性提示就可能迁移到另一个模型。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个规模较小、支持两种推理模式的学生模型 $M$，研究首先让它以非思考模式和思考模式分别处理同一批推理密集型软件工程样例，并依据标准答案找出两种模式正确性发生翻转的案例集合 $\mathcal{C}$。对每个案例 $i\in\mathcal{C}$，可观察非思考答案 $\hat{y}_{i,0}$、思考答案 $\hat{y}_{i,1}$、思考模式产生的解释轨迹以及标准答案；前沿教师模型据此诊断思考为何有帮助或有害，并把跨案例规律压缩为候选建议性提示，最终选择提示模板 $\pi^{\star}$。研究的目标设置是：将 $\pi^{\star}$ 注入未参与蒸馏的测试样例，在不更新学生模型参数、主要使用非思考推理的条件下，提高代码生成、程序输入预测、输出预测、异常预测或方法幻觉检测的正确率，同时减少相对于完整思考模式的令牌开销；此外还考察从模型 $A$ 的错误中得到的提示能否帮助模型 $B$，以及这种迁移是否仅由两者在相同样例上的共同失误解释。该设置默认任务具有可用于判定答案正确性的参考答案或执行性判据，并且教师模型只参与错误诊断和提示构造，而不是替代学生模型完成最终评测。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$M$**

支持非思考与思考模式的学生语言模型。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{C}$**

学生模型切换推理模式后答案正确性发生翻转的案例集合，包括由错变对以及由对变错的案例。

</div>
<div class="notation-item" markdown="1">

**$\hat{y}_{i,0},\hat{y}_{i,1}$**

案例 $i$ 上学生模型分别在非思考模式和思考模式下生成的答案，其中下标 $0$ 与 $1$ 表示两种模式。

</div>
<div class="notation-item" markdown="1">

**$\pi^{\star}$**

由教师模型综合案例诊断后选出的简短建议性提示模板，用于后续未见样例或其他模型。

</div>

</div>

**直接相关的工作**

- **Hsieh et al. (2023), Distilling Step-by-Step! Outperforming Larger Language Models with Less Training Data and Smaller Model Sizes**: 该工作代表从逐步推理中进行知识蒸馏的相关路线；本文同样利用推理所包含的信息，但把产物设计为无需更新参数、可直接注入输入的建议性提示，而非仅依赖训练式蒸馏。
- **Jin et al. (2025), Understanding Chain-of-Thought Effectiveness in Code Generation: An Empirical and Information-Theoretic Analysis**: 该工作研究思维链在代码生成中的有效性，为“额外推理能够改善部分软件工程任务”提供直接背景；本文进一步询问能否把有用推理压缩成短程序性指导，以较低推理成本复现其部分收益。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

软件工程中的模型错误可能产生严重后果，但软件训练语料本身普遍含有缺陷，构造足够大且完全无错误的代码语料并不现实，重新训练模型的成本也很高。因此，实际部署尤其需要一种不修改模型参数、只在推理阶段使用的纠错机制。该需求对小型语言模型更迫切：它们便宜、快速且便于本地部署，但只有可靠性得到改善，才可能成为大型模型的实用替代方案。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **数据清洗与重新训练或微调**：通过提高训练代码的质量，或使用新的监督数据更新模型参数，使模型从训练阶段减少错误倾向。
- **测试时完整思考与提示工程**：前者让混合推理模型生成较长的中间推理过程，以检查程序执行、类型和控制流等细节；后者不更新参数，而是在输入中加入指令，引导模型采用更可靠的解题步骤。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 无缺陷的大规模软件语料难以收集，而重新训练或微调成本高，因而不适合频繁修正部署后发现的新错误。
- 完整思考模式虽然可能降低错误率，却持续增加计算量和词元消耗，而且思考并非总有帮助：论文特意收集从错误变正确以及从正确变错误的双向翻转案例，说明更长推理也可能伤害答案。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有思路尚未回答能否把同一模型完整推理中真正具有纠错价值的部分，压缩成可反复使用的短提示，并在不重新训练、也不为每个新样本支付完整思考成本的情况下推广到未见样本。进一步未知的是，这类提示究竟只是在记忆源模型的个别错误，还是能够概括跨样本乃至跨模型共享的软件推理失误。

</div>
<div markdown="1"><span>核心问题</span>

论文集中回答四个相互衔接的问题：由思考与非思考正确性差异蒸馏出的建议提示，能否提高推理密集型软件工程任务的留出集表现；它能否在非思考模式下以更少词元取得更高准确率；从源模型 $A$ 的错误中得到的提示能否帮助另一模型 $B$；若能迁移，这种收益是否源于 $A$ 与 $B$ 在相同样本上的共同失误。

</div>
<div markdown="1"><span>作者直觉</span>

作者把模型类比为会从错题中总结规则的编程学生：单个错误案例中的长推理往往包含可复用的检查动作，例如按执行顺序追踪具体输入、核对运行时类型与接口前置条件，并定位第一个会失败或不终止的操作。教师模型先比较同一案例的错误答案、正确答案和推理轨迹，再把多个案例中的共同教训压缩为建议，相当于把昂贵的逐题反思预先整理成一张简短检查表；后续模型只需遵循该检查表，就可能触发关键检查，而无需重新生成全部推理过程。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把混合推理模型在“思考模式”中表现出的有效解题行为，蒸馏为可直接附加到任务模板中的自然语言建议，即蒸馏提示或 advisory prompt。输入是带参考答案或可执行判定器的软件工程数据集，以及同一学生模型在基础模板 $[?25l[?25h$ 下的思考与非思考输出；系统先通过配对正确性差异定位“思考使错误变正确”或“使正确变错误”的样例，再由教师模型诊断其行为机制并归纳改进指令和防退化指令，最后在验证集上选择提示，在隔离的测试集上评估。全过程仅在推理阶段调用模型，不更新学生或教师模型的参数。

通俗地说，它不是让较小模型每次都写出长篇思考过程，也不是把知识重新训练进模型，而是先观察模型在哪些题上因认真思考而避开了错误，再让更强模型把这些经验压缩成简短的“做题前检查清单”。同时，方法也研究思考模式造成退步的样例，从中提炼约束，避免建议诱导模型过度推断、擅自改写问题或破坏输出格式。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 数据划分与配对基线测量

先把每个数据集划分为互不重叠的蒸馏集、验证集和测试集；仅在蒸馏集上，对同一任务分别执行 $M(\pi_0(x_i),0)$ 与 $M(\pi_0(x_i),1)$，并用任务判定函数 $s$ 记录二元正确性、输出长度、延迟及可用的推理轨迹。配对设计固定任务、模板、期望答案、模型和判定器，使模式开关成为两次执行之间的关键差异。

<div class="method-step__io" markdown="1">

**输入**：基准数据集 $\mathcal{D}=\{(x_i,y_i,m_i)\}_{i=1}^{n}$、基础提示模板 $\pi_0$、学生模型 $M$，以及思考模式指示量 $z\in\{0,1\}$。<br>
**输出**：每个蒸馏样例的非思考输出 $\hat y_{i,0}$、思考输出 $\hat y_{i,1}$、正确性 $a_{i,0}$ 与 $a_{i,1}$，以及思考模式产生的中间推理轨迹。

</div>

**直观理解**：相当于让同一名学生用“直接作答”和“写出思考过程”两种方式做同一道题，再比较结果。这样观察到的差异较少受到题目难度或评分规则变化的干扰。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 正确性差异挖掘与逐例诊断

根据 $d_i=a_{i,1}-a_{i,0}$ 建立改进集合 $\mathcal{C}^{+}$ 和退化集合 $\mathcal{C}^{-}$；教师模型读取每个差异样例的任务、期望结果、双方回答、得分和轨迹，比较思考为何帮助或伤害了最终正确性。教师为每例生成结构化诊断，包括机制标签、简短解释、提示建议、证据片段和置信度。

<div class="method-step__io" markdown="1">

**输入**：两种推理模式的配对输出、分数、参考答案或判定器摘要，以及思考模式的推理轨迹。<br>
**输出**：与具体轨迹证据绑定的逐例诊断；改进案例给出应更系统执行的行为，退化案例给出应避免的行为或约束条件。

</div>

**直观理解**：系统只重点复盘两种模式结果不同的题，因为这些题最能显示“思考到底改变了什么”。教师既总结成功经验，也分析反思过度、无依据假设或格式改变等失败原因。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 指令聚合与候选提示合成

教师把多个逐例诊断聚合为可跨样例复用的改进指令和防退化指令，并与原模板组合成有限候选集合 $\Pi=\{\pi_1,\ldots,\pi_k\}$。候选可改变措辞、顺序及两类指令的组合强度，但必须保留原任务字段和占位符。

<div class="method-step__io" markdown="1">

**输入**：来自 $\mathcal{C}^{+}$ 的改进诊断、来自 $\mathcal{C}^{-}$ 的退化诊断，以及原始任务模板和占位字段。<br>
**输出**：一组候选蒸馏提示模板 $\Pi$，每个模板都可在不提供完整推理轨迹的情况下引导学生模型采取归纳出的程序性行为。

</div>

**直观理解**：这一步把许多题目的复盘记录压缩成通用检查清单，例如先检查可行性、推导不变量、验证边界条件，同时提醒模型不要擅自改变输出格式。不同版本的清单会进入下一步竞争。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 验证选择与留出评估

在验证集上分别以思考和非思考模式评估每个候选，并以两种模式通过率的均值选择 $\pi^{\star}$；并列时依次选择导致原基线成功样例退化更少、提示更短、候选索引更小的模板。选定模板随后在测试折或留出发布集上与 $\pi_0$ 比较，同时考察非思考增益、思考模式增益、相对思考基线的差距、输出词元节省及跨模型迁移。

<div class="method-step__io" markdown="1">

**输入**：候选模板集合 $\Pi$、验证集、完全留出的测试集，以及同一学生模型的两种推理模式。<br>
**输出**：最终蒸馏模板 $\pi^{\star}$，以及其在留出数据上的正确率效应、推理成本变化和跨模型可迁移性结果。

</div>

**直观理解**：验证集负责从多份检查清单中选出最可靠的一份，测试集只用于最后验收，避免根据测试答案反复改提示。核心问题是：较短建议能否让直接作答接近甚至超过原来的深度思考，同时减少输出成本。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 配对行为差异与差异案例集合

$$
\hat{y}_{i,z}=M(\pi_0(x_i),z),\quad a_{i,z}=s(\hat{y}_{i,z},y_i),\quad d_i=a_{i,1}-a_{i,0},\quad \mathcal{C}^{+}=\{i:a_{i,0}=0,a_{i,1}=1\},\quad \mathcal{C}^{-}=\{i:a_{i,0}=1,a_{i,1}=0\}
$$

**符号说明**

- $x_i$：第 $i$ 个软件工程任务的输入。
- $y_i$：第 $i$ 个任务的参考答案或可执行判定依据。
- $M$：可在思考与非思考模式之间切换的学生模型。
- $\pi_0$：未加入蒸馏建议的基础提示模板。
- $z$：推理模式指示量；$z=0$ 表示非思考，$z=1$ 表示思考。
- $\hat{y}_{i,z}$：学生模型在模式 $z$ 下对第 $i$ 个任务生成的回答。
- $s(\hat{y}_{i,z},y_i)$：任务特定的二元评分函数，通过为 $1$，失败为 $0$。
- $a_{i,z}$：第 $i$ 个任务在模式 $z$ 下的二元正确性。
- $d_i$：思考正确性减去非思考正确性所得的配对差异。
- $\mathcal{C}^{+}$：非思考失败而思考成功的改进案例集合。
- $\mathcal{C}^{-}$：非思考成功而思考失败的退化案例集合。

<div class="equation-explanation" markdown="1">

**直观理解**：该式先让同一模型以两种模式回答同一任务，再把回答压缩为通过或失败，并通过 $d_i$ 找到发生结果翻转的样例。$\mathcal{C}^{+}$ 提供值得模仿的思考行为，$\mathcal{C}^{-}$ 提供需要写入提示的防护规则；若没有差异案例，就没有可供该方法蒸馏的行为信号。<br>
**原文位置**：Methodology，Problem Setup 与 Prompt Distillation Pipeline

</div>

</div>

<div class="equation-block" markdown="1">

#### 验证集候选提示选择目标

$$
\pi^{\star}=\arg\max_{\pi_j\in\Pi}\widehat{p}_{\mathrm{val}}(\pi_j),\qquad \widehat{p}_{\mathrm{val}}(\pi_j)=\frac{1}{2}\left(\widehat{p}_{\pi_j,0}^{\mathrm{val}}+\widehat{p}_{\pi_j,1}^{\mathrm{val}}\right)
$$

**符号说明**

- $\Pi$：由原模板与聚合指令组合得到的有限候选提示集合。
- $\pi_j$：候选集合中的第 $j$ 个蒸馏提示模板。
- $\widehat{p}_{\pi_j,0}^{\mathrm{val}}$：候选 $\pi_j$ 在验证集、非思考模式下的经验通过率。
- $\widehat{p}_{\pi_j,1}^{\mathrm{val}}$：候选 $\pi_j$ 在验证集、思考模式下的经验通过率。
- $\widehat{p}_{\mathrm{val}}(\pi_j)$：候选在两种推理模式下验证通过率的算术平均。
- $\pi^{\star}$：按验证目标及并列规则最终选出的蒸馏提示。

<div class="equation-explanation" markdown="1">

**直观理解**：选择目标没有只针对便宜的非思考模式优化，而是平均衡量候选对两种模式的作用，因而偏好总体稳健的建议。若主目标并列，论文再依次比较基线成功退化数、提示长度和候选索引；这些次级规则不改变主目标，但控制副作用、成本和复现歧义。<br>
**原文位置**：Methodology，Prompt Distillation Pipeline，第四阶段

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用传统训练目标。该方法是纯推理阶段的提示蒸馏，不执行反向传播、参数更新或软提示向量优化；唯一的显式优化是从有限自然语言候选集合 $\Pi$ 中，根据验证目标选择 $\pi^{\star}$。因此，这里的“蒸馏”指从模型行为与推理轨迹中综合出文字指令，而不是知识蒸馏中让学生网络拟合教师概率分布。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 配对正确性差异挖掘器**

对每个固定样例计算 $d_i=a_{i,1}-a_{i,0}$，只把 $d_i=1$ 的改进案例和 $d_i=-1$ 的退化案例作为主要蒸馏信号。由于两次运行共享输入、基础模板、模型和判定器，该模块提取的是思考开关与正确性变化之间的配对行为证据，但它本身不能证明某段轨迹与成功之间存在严格因果关系。

> 直观理解：它像一个复盘筛选器：跳过两种做法都对或都错、信息量较低的题，集中查看因思考方式变化而翻转结果的题。这样能把教师模型的分析预算投入到最可能揭示有效或有害策略的案例上。

**2. 轨迹约束的教师诊断与聚合器**

教师模型接收差异案例的完整比较材料，但不能看到验证集和测试集；它先生成带证据片段和置信度的逐例结构化诊断，再跨案例聚合为改进指令与 guard instructions。前者鼓励检查可行性、不变量和边界条件等程序性动作，后者限制无依据假设、不必要变换和输出格式偏离。

> 直观理解：教师不是直接替学生回答未来题目，而是从已经发生的成功与失败中抽取可迁移的做题习惯。把正向建议与防退化约束同时纳入，是为了避免提示只会增加思考步骤，却忽视“想得更多也可能想错”。

**3. 验证驱动的提示选择器**

选择器以候选提示在验证集上的思考与非思考平均通过率为主目标，并用基线成功退化数、提示长度和固定索引实施确定性的分层并列规则。原始模板 $\pi_0$ 不属于候选集合，因此该步骤选择的是合成提示之间的最优者，而不是判断是否应退回原模板。

> 直观理解：教师可能生成多种措辞，单靠语言表面无法判断哪一种真正有效，因此必须让它们在独立题目上竞争。并列规则优先保住原来能做对的题，其次减少提示成本，并保证选择过程可重复。

**训练与推理**

蒸馏阶段先在蒸馏集上运行学生模型的两种模式，挖掘 $\mathcal{C}^{+}$ 与 $\mathcal{C}^{-}$；随后调用教师模型完成逐例诊断、跨例聚合和候选提示生成，再在验证集上运行候选并选择 $\pi^{\star}$。验证和测试样例不提供给教师，测试集也不参与候选选择。

部署或最终评估时，将新任务 $x_i$ 填入选定模板 $\pi^{\star}(x_i)$，再让学生模型以目标模式生成答案；若目标是节省推理资源，则重点使用 $z=0$ 的非思考推理。跨模型迁移时，可把源模型 $A$ 蒸馏出的提示直接用于目标模型 $B$，记为 $B\leftarrow A$，无需重新训练目标模型；不过迁移有效性必须在与提示生成和选择隔离的留出样例上判断。

**复现信息**

复现时最关键的是保持三份数据严格隔离，并保存配对运行所需的任务提示、两种回答、二元得分、推理轨迹、响应长度和延迟。代码生成任务由基准测试判定通过或失败，其他软件工程任务使用精确匹配或各自的任务评分规则；教师诊断需要参考答案或判定器摘要，但不得接触验证或测试样例。

候选模板必须保留原任务字段和占位符。若只观察到单方向差异，候选只使用该方向的指令；若完全没有差异案例，则没有蒸馏信号。论文说明其实验中这两种边界情况均未发生，但所给节选未报告教师模型名称、候选数量 $k$、生成温度、随机种子或具体模板文本，这些内容需结合 Experimental Setup 与补充材料核查。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- LiveCodeBench：使用 v5/v6 的 341 个样例进行五折蒸馏与测试，并使用 v1–v4 的 713 个样例进行较早版本的额外评估。该基准测试模型生成代码通过测试的能力；其作用是检验蒸馏 prompt 在具有时间切分和潜在训练泄漏约束的编程题上的泛化能力。表 1 将 v5/v6 与 v1–v4 的结果合并报告。
- Exception Prediction、Input Prediction 与 Output Prediction：分别包含 834、800 和 7,450 个样例，测试模型预测程序执行引发的异常、满足程序行为的输入以及给定输入下的输出。Output Prediction 使用输入扰动版本，因为原始样例上的模型分数接近上限，扰动输入更能检验执行推理能力。五折划分中每折保留 20% 测试集。
- Method Hallucination：包含 290 个样例，覆盖 30 个 Python 库；每个样例要求模型使用目标库实现指定功能，静态检查器从代码中抽取库成员引用，并与文档快照核对。该数据集检验模型是否会虚构不存在的库 API，因此覆盖的是代码生成中的方法级幻觉，而非一般执行结果预测。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**pass rate（等同于 pass@1）**

每个样例只生成一个答案，因此通过率就是单次生成成功的比例；在不同任务中，成功分别表示通过代码测试、正确预测异常、输入或输出，或未引用不存在的库成员。 （越高越好，因为它表示更多样例得到正确结果。）

</div>
<div class="metric-item" markdown="1">

**output-token savings**

蒸馏后的非思考推理相对于思考模式基线减少的输出 token 百分比，用于衡量推理时资源成本。 （越高越好，因为在准确率可接受时，更少的输出 token 表示更低的推理成本。）

</div>
<div class="metric-item" markdown="1">

**directed transfer gain $\Delta_{B\leftarrow A}$**

将来源模型 $A$ 的 prompt 用于目标模型 $B$ 时，目标模型相对于自身 Base 的 pass-rate 变化；表 2 同时报告均值、中位数以及单侧 Wilcoxon 符号秩检验的 $p$ 值。 （均值或中位数越高越好；正值表示来源 prompt 在目标模型上带来收益，但不能说明收益原因。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### RQ1：非思考模式下的同模型 held-out 效果

<div class="result-value" markdown="1">

蒸馏 prompt 在 20 个模型—任务比较中的 19 个提高了 pass rate，平均提升 3.1 个百分点；Exception Prediction 上 Qwen3-4B 从 $0.447$ 提升到 $0.562$，增加 11.5 个百分点，是表中最大增益。LiveCodeBench 的四个模型也均有提升，增幅为 2.3–4.8 个百分点。

</div>

这说明从低资源模型的思考纠错案例中提炼的短建议，通常能改善关闭思考模式时的结果，尤其适合异常行为预测。它证明的是在这些数据集、模型和五折协议下的经验收益，并不证明蒸馏 prompt 在所有软件工程任务上都有效；Output Prediction 的平均收益只有 0.8 个百分点，显示高基线任务上的改进空间有限。

<div class="result-source" markdown="1">

来源：Results，表 1 后正文

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The approach generally helps; across 5 task families and 4 student models, 19 of 20 non-thinking model–task comparisons show performance gains, with a mean gain of 3.1 pass-rate points; 10 are nominally significant under paired exact McNemar tests (Table 1).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### RQ2：准确率与思考成本的权衡

<div class="result-value" markdown="1">

相对于思考模式基线，非思考蒸馏推理在全部 20 个模型—任务比较中平均减少 58.6% 的输出 token；但思考模式平均在 20 个比较中的 17 个取得更高性能，平均高出 7.5 个 pass-rate 百分点。以 Qwen3-4B 的 Exception Prediction 为例，蒸馏非思考结果为 $0.562$，相较思考基线的准确率差为 $-12.5$ 个百分点，同时 token savings 为 71.7%。

</div>

蒸馏 prompt 的核心收益是以显著更低的生成成本获得接近普通思考能力的结果，而不是全面超过思考模式。具体部署时应根据错误代价和延迟预算选择：需要最高准确率时思考模式仍占优，能接受一定准确率差且重视成本时蒸馏非思考模式更合适。

<div class="result-source" markdown="1">

来源：Results，RQ2 段落

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For RQ2, Table 1 also shows a consistent cost reduction: across all 20 model–task comparisons, non-thinking distilled inference uses 58.6% fewer output tokens than the thinking-mode baseline on average, with the largest savings on Method Hallucination (67.5%) and LiveCodeBench (63.6%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### RQ3–RQ4：跨模型迁移与共同失败的关系

<div class="result-value" markdown="1">

跨模型迁移在三类任务上为正：Exception Prediction 的 60 次迁移中有 48 次为正，平均提升 4.4 个百分点；LiveCodeBench 和 Method Hallucination 的平均提升均为 2.7 个百分点。Input Prediction 和 Output Prediction 的平均迁移收益分别为 $-0.7$ 和 $-0.7$ 个百分点。模型间共同失败率指标 $\phi$ 在各任务为 0.29–0.53，但其与迁移收益的总体 Spearman 相关为 $\rho_{\phi}=0.09$，$p=.131$。

</div>

部分 prompt 能跨模型传递，尤其是在异常预测和方法幻觉任务中，说明建议可能概括了任务层面的错误规律，而不只是记住来源模型的行为。然而迁移并不稳定：输入和输出预测没有正的平均收益。模型经常在同一样例上失败，但共同失败程度并不能可靠预测 prompt 是否能迁移，因此“模型错误相似”不是充分的迁移选择标准。

<div class="result-source" markdown="1">

来源：Results，表 2 后 RQ3 段落；共同失败相关性见表 3 后 RQ4 段落

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For RQ3, cross-model transfer is positive on three of five task families (Table 2): Exception Prediction is strongest (48 of 60 cross-model transfers are positive, mean +4.4 points), and LiveCodeBench and Method Hallucination each average +2.7.

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

- 非思考基线：学生模型接收相同的基础任务 prompt，但关闭 thinking mode；它衡量 advisory prompt 相对于普通低成本推理的准确率增益，是表 1 的主要比较对象。
- 思考模式基线：学生模型接收相同基础任务 prompt 并开启 thinking mode；它代表一种已知的推理时减错方法，用于比较蒸馏 prompt 是否能以较低 token 成本逼近或替代思考模式。
- 跨模型基线：在 RQ3 中，目标模型使用自身的非思考基础 prompt 作为 Base，再与来自其他学生模型的 distilled prompt 比较；该设计检验 prompt 是否携带可跨模型复用的任务规律，而不是只对原模型有效。
- 自模型蒸馏结果：蒸馏 prompt 由对应学生模型的错误与思考模式下的纠错案例产生，并在同一模型的 held-out 测试集上与非思考基线配对比较；它用于测量方法的直接效果，但不能单独证明 prompt 学到了模型之外的普适知识。

**实验想回答的问题**

- RQ1：在不启用思考模式的情况下，蒸馏得到的 advisory prompt 能否提高四种混合推理学生模型在软件工程任务上的准确率？
- RQ2–RQ4：与思考模式相比，蒸馏 prompt 能否降低输出 token 成本；蒸馏 prompt 能否迁移到其他模型；模型之间的共同失败是否与迁移收益相关？

**实验实现**

实验使用 Qwen3-4B、Qwen3-8B、Gemma-4-E2B-it 和 Gemma-4-E4B-it 四个混合推理学生模型；每个模型分别在思考和非思考模式下评估。蒸馏阶段由教师模型完成：GPT-5.4-mini 分析第一阶段案例，GPT-5.4 完成后续聚合和 prompt 构造；教师仅用于蒸馏，held-out 测试由学生模型完成。每个任务采用五折划分，每折约 20% 测试、70% 蒸馏、10% 验证；第三阶段为每折生成 $k=3$ 个候选 prompt，并选择一个进行测试。模型温度为 $0.7$，教师推理 effort 为 none，学生输出预算为 14k token，每个样例生成一个样本。所有基线与蒸馏 prompt 在配对样例上比较。由于 Output Prediction 有 7,450 个样例，RQ3 对每个 held-out fold 确定性抽取 200 个样例以降低迁移评估成本。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：将高成本推理轨迹提炼为可迁移的简短提示，以低成本提升 LLM 在代码与软件工程任务中的推理正确性。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`54a0d7950ed1a4c40d9a8383ffc20d663545b86d39e596921f0d7e97c5f30e48`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
