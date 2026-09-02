---
title: "[论文解读] Can LLMs Discover Scientific Laws in Real and Parallel Worlds?"
description: "[arXiv 2609.01552][LLM 评测] 本文提出 SciLaws-Bench，通过真实观测下的开放式定律提出与可主动实验的“平行世界”结构恢复两种互补设置，评估大语言模型能否在避免记忆捷径的同时发现拟合良好且科学上有效的定律。"
arxiv_id: "2609.01552"
announcement_date: "2026-09-02"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:40:41.729877+00:00"
source_sha256: "5f803d68cc80c6627ce6b862baf0294f25772b6238000379a84b994be01ad705"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "科学定律发现"
  - "符号回归"
  - "大语言模型"
  - "AI for Science"
  - "真实科学数据"
  - "主动实验"
  - "科学有效性"
  - "抗记忆评测"
  - "SciLaws-Real"
  - "SciLaws-Parallel"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2609.01552</p>

# Can LLMs Discover Scientific Laws in Real and Parallel Worlds?

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Yiming Huang, Ziche Liu, Zhuohang Wu, Yiqian Wang, Junxia Cui, Xinkai Zou, Linjun Mao, Nan Huang, Naicheng Yu, Kaijie Zhu, Yue Ma, Kun Zhou, Letian Peng, Jingbo Shang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of California San Diego；Affiliation: University of California, Irvine；Affiliation: Cushing Academy；Affiliation: University of California, Santa Barbara</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.01552v1) · [PDF 下载](https://arxiv.org/pdf/2609.01552v1) · **关键词** 科学定律发现, 符号回归, 大语言模型, AI for Science, 真实科学数据, 主动实验, 科学有效性, 抗记忆评测, SciLaws-Real, SciLaws-Parallel<br>
**项目页**: [https://yiyihum.github.io/SciLaws-Bench](https://yiyihum.github.io/SciLaws-Bench)

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

本文提出 SciLaws-Bench，通过真实观测下的开放式定律提出与可主动实验的“平行世界”结构恢复两种互补设置，评估大语言模型能否在避免记忆捷径的同时发现拟合良好且科学上有效的定律。

**不用术语来说**：让模型从数据中写出一个数学公式，并不等于它真正发现了科学规律：公式可能只是碰巧拟合已有样本，也可能违反物理约束，甚至只是模型背出了训练时见过的著名公式。真正需要检验的是，面对带噪声、来源复杂的真实观测，模型能否提出可解释、可外推且符合科学背景的规律；当目标规律是文献中从未出现的新结构时，它又能否主动选择有信息量的实验并把该结构识别出来。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 构建以论文和真实数据为基础的 SciLaws-Bench，包含 118 个问题、291 条候选定律、381 篇论文及约 800 万个真实数据点，覆盖六个科学学科；其目标是把评测从经典教材公式和纯合成任务推进到较少被普及、具有真实噪声与领域约束的科学问题。
- 为同一科学问题设计互补的 SciLaws-Real 与 SciLaws-Parallel：前者分别检验固定真实观测上的留出预测拟合和文献支持的科学有效性，后者让模型主动查询经真实残差校准的环境，并恢复由已发表形式变换而来、但不直接存在于原文献中的隐藏定律，从而拆分评估拟合、有效性、记忆、结构恢复与候选选择能力。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

科学定律发现旨在从观测到的输入—输出关系中提炼紧凑、可解释的数学表达式，常被形式化为符号回归。与单纯拟合数据不同，一条可接受的科学定律还应符合领域约束，在相关取值范围内保持合理行为，并具有可解释的科学含义。随着大语言模型开始充当能够提出假设、编写代码和检查证据的科学智能体，关键问题已从“能否生成一个拟合公式”扩展为“能否依据真实且含噪的数据发现具有预测力与科学有效性的关系”。现有基准往往在科学真实性与抗记忆性之间取舍：教科书公式贴近真实知识，却可能已被模型记忆；反事实公式或模拟世界便于验证，但与真实科学测量的噪声、异质性和领域背景存在距离。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**符号回归**

给定若干输入—输出观测，直接搜索由变量、常数和数学运算组成的解析表达式，而不是只训练一个难以解释的黑箱预测器。其目标通常兼顾数据拟合与表达式简洁性，但本文强调这两点尚不足以保证科学有效性。

</div>
<div class="concept-item" markdown="1">

**科学有效性**

指候选公式除预测准确外，还符合来源文献所支持的物理或领域约束，在目标范围内不存在不合理行为，并保留正确的科学含义。例如，一个拟合较好的公式若虚构了不存在的共振峰，仍会被视为无效。

</div>
<div class="concept-item" markdown="1">

**主动实验与固定观测**

固定观测任务只能利用预先收集的数据提出定律；主动实验任务则允许模型自行选择查询点并取得新测量。两种设置分别考查从既有记录进行开放式归纳，以及通过实验设计识别隐藏结构的能力。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

SciLaws-Bench从381篇论文中整理118个跨六个学科的定律发现问题，涉及291条候选定律和约800万条真实数据。每个问题被实例化为两种互补设置：在SciLaws-Real中，模型接收科学背景与固定的真实观测，输出闭式候选定律；已发表公式仅作为参考基线而非必须复现的唯一答案，候选式分别按留出数据上的预测拟合和来源文献支持的科学有效性评价。在SciLaws-Parallel中，模型起初没有观测，可在固定预算内主动选择测量点；环境中的隐藏定律是由已发表公式合成的新结构变体，其系数与残差噪声根据对应真实记录校准，模型最终需恢复这个未出现在来源文献中的固定隐藏结构。该双设置在保留同一科学语境的同时，将“基于真实固定记录提出合理规律”和“通过主动查询恢复可验证的新规律”区分开来。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$N$**

best-of-$N$研究中生成或比较的候选答案数量；该研究用于检验模型生成优质定律与自行选出优质定律之间的差距。

</div>
<div class="notation-item" markdown="1">

**$E=\hbar\omega$**

文中列举的典型教科书物理公式，用于说明经典公式恢复基准可能受到模型参数记忆的影响。

</div>
<div class="notation-item" markdown="1">

**$F=Gm_1m_2/r^2$**

标准万有引力形式，文中用它与人为修改的反事实目标对照，以说明某些基准如何降低记忆带来的影响。

</div>
<div class="notation-item" markdown="1">

**$F=G'm_1m_2/r^{1.5}$**

NewtonBench式反事实目标的示例；它保留熟悉的科学外观但改变幂次，从而测试模型是否能依据环境证据而非直接复述已知公式。

</div>

</div>

**直接相关的工作**

- **AI Feynman**: 代表以标准教科书方程恢复为核心的符号回归评测。它提供明确的目标公式，但这些经典方程可能已存在于大语言模型训练数据中，因此无法可靠区分基于观测的归纳与参数记忆。
- **NewtonBench**: 通过修改经典规律构造反事实目标，以减少直接记忆标准公式的作用并考查交互式发现。相比之下，SciLaws-Bench同时引入真实科学记录、论文语境与来源文献支持的有效性检查，并以残差校准的平行世界提供可验证的新结构恢复任务。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

科学定律发现不仅要从不完美观测中找到紧凑的闭式表达式，还要求表达式在相关取值范围内行为合理、满足物理或领域约束，并保留明确的科学含义。随着大语言模型开始参与符号回归和更广泛的 AI for Science 工作流，仅检查它能否生成一个低误差公式已不足以判断其是否具备可靠的科学发现能力，因此需要一种同时覆盖真实数据、科学约束和主动实验的评测。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **经典方程恢复基准**：以 AI Feynman 一类任务为代表，向模型提供变量与数据，要求恢复教材中的标准解析式，例如 $E=\hbar\omega$。这类设置具有明确答案，便于用表达式匹配或预测误差判断是否恢复成功。
- **反事实目标或纯模拟发现环境**：NewtonBench 等方法人为修改熟知定律的结构，例如把平方反比关系改成 $r^{-1.5}$；DiscoveryWorld 等则让智能体在虚构环境中通过实验推断隐藏规则。它们借助未在现实文献中直接出现的目标，降低背诵标准答案的可能，并使实验过程和真值验证更可控。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 经典方程恢复任务大量复用教材和公开文献中的著名公式，模型可能依靠预训练记忆直接复现目标，而不是根据给定观测完成经验归纳；因此，即使恢复率较高，也难以区分“记住公式”和“发现规律”。
- 为避免记忆而采用的反事实公式或模拟世界虽然便于控制，却与真实科学数据中的噪声、异质性及领域语境存在距离；同时，只用拟合误差评价候选式会漏掉虚假峰值、错误极限行为或违反科学约束等问题，导致统计上好看的公式被误判为有效定律。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有基准尚未同时满足两项需求：一方面，在真实论文语境和真实观测上评价开放式定律提出，并把留出预测能力与科学有效性分开；另一方面，在保留同一科学背景及真实噪声特征的条件下，提供文献中不存在、可以通过主动查询被严格验证的隐藏结构。缺少这种成对设计，使研究者无法系统判断模型的成功究竟来自数据驱动的发现、已知公式记忆，还是偶然拟合。

</div>
<div markdown="1"><span>核心问题</span>

大语言模型能否在固定的真实观测记录上提出兼具预测性能与科学有效性的定律，并在不能直接依赖已发表答案的可查询平行世界中，通过自主设计测量恢复新的隐藏数学结构；同时，记忆与候选选择能力如何影响其最终表现？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把现实性与可验证性拆成两个互补视角，而不是强迫单一任务同时承担二者。SciLaws-Real 保留真实数据和文献约束，用来观察模型面对实际噪声时会提出什么；SciLaws-Parallel 则沿用相同科学语境，并用真实记录的系数与残差校准环境，但替换为新合成的隐藏结构，使答案既不容易被背出，又能被明确核验。若模型在前者只会复现文献公式、在后者却不能恢复新结构，就说明其表现主要受记忆驱动；若它能生成优质候选却无法从候选池中选中，则可进一步定位为选择瓶颈，而非生成能力不足。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SciLaws-Bench 的方法核心不是训练一个新的方程发现模型，而是构建一套由论文、真实数据与合成平行世界相互关联的评测流程。基准首先整理科学论文及其配套数据，形成固定观测记录上的 SciLaws-Real；随后依据论文中已发表的函数形式合成新的隐藏定律，并构造允许模型主动查询的 SciLaws-Parallel。最终得到 118 个问题，覆盖六个学科、381 篇论文、291 条候选定律和约 800 万个真实数据点。两种设置保留相同或相近的科学语境，但分别考查模型能否从既有真实观测中提出有效定律，以及能否通过主动实验恢复一个新合成、不可直接照搬的隐藏定律。

每个问题还按参数组织方式分为单组与多组。单组问题在整个任务中采用一个全局函数形式和一套参数；多组问题则要求各组共享同一函数形式，同时允许部分参数随组变化。因此，后者不只检查模型能否拟合某一批数据，还检查它是否发现了可跨组迁移的结构。直观地说，SciLaws-Real 类似于拿到一份已经完成的实验记录后总结规律，SciLaws-Parallel 则类似于进入一个可自行做实验的模拟世界，通过选择观测点逐步推断幕后规律。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 整理相互关联的论文与真实数据

将论文与其数据集建立关联，并据此整理具有明确科学语境的方程发现问题。原文汇总出 118 个问题、381 篇论文、291 条候选定律和约 800 万个真实数据点，覆盖六个科学学科。

<div class="method-step__io" markdown="1">

**输入**：已发表的科学论文、论文对应的真实科学数据，以及论文中报告的候选定律或函数形式。<br>
**输出**：一组以真实研究材料为依据、同时保留文献定律信息的基础问题。

</div>

**直观理解**：这一步相当于把论文中的研究问题、实验数据和作者提出的规律装订成同一份题目，避免只生成缺乏实际背景的人工函数题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造固定数据的 SciLaws-Real

把真实观测作为不可由模型扩充的输入，要求模型据此提出科学定律；评估面向未参与发现过程的留出数据预测拟合，并结合源文献判断科学有效性。

<div class="method-step__io" markdown="1">

**输入**：论文—数据配对、固定的真实观测记录，以及源论文提供的科学约束与候选定律。<br>
**输出**：考查固定记录下定律提出能力的 SciLaws-Real 任务。

</div>

**直观理解**：模型只能阅读已有实验记录，不能追加实验；它既要预测没见过的数据，也要提出在科学意义上说得通的表达式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造可主动查询的 SciLaws-Parallel

从已发表形式派生合成隐藏定律，并据此建立允许模型主动选择查询的残差校准世界。模型通过查询获得观测，再尝试恢复该世界中预先隐藏的新定律；现有节选未说明具体合成算法、残差模型或查询接口。

<div class="method-step__io" markdown="1">

**输入**：已发表的函数形式、对应问题的科学语境，以及用于形成平行世界的残差校准机制。<br>
**输出**：具有新隐藏定律和主动实验能力的 SciLaws-Parallel 任务。

</div>

**直观理解**：这类似于保留现实问题的实验背景，却悄悄更换真正起作用的公式；模型必须自己选择实验点来揭示它，而不能只背出论文中的原公式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 实例化单组与多组问题

单组实例对整个任务采用一个全局定律及一套参数；多组实例让各组共享函数形式，但允许部分参数取值不同，以测试结构层面的跨组泛化。

<div class="method-step__io" markdown="1">

**输入**：SciLaws-Real 或 SciLaws-Parallel 中的具体科学问题、函数形式、参数及数据分组。<br>
**输出**：覆盖全局单一规律和跨群组共享规律两类发现情景的最终评测实例。

</div>

**直观理解**：单组题只需解释一个系统；多组题则要求看出多个系统背后使用同一种公式，即使每个系统的常数并不完全相同。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。当前节选描述的是基准构建与评测任务，而不是需要端到端训练的模型，因此没有统一的训练损失或参数优化目标。任务层面的目标是让被测模型提出或恢复科学定律：SciLaws-Real 面向固定真实观测，兼顾留出预测拟合与源文献所支持的科学有效性；SciLaws-Parallel 面向可主动查询的平行世界，考查对合成隐藏定律的恢复。具体评分公式、拟合指标及科学有效性的操作化判据在所给节选中未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 论文—真实数据关联模块**

以已发表研究及其真实数据为任务依据，同时保留源文献中的候选定律与科学语境。该模块为后续固定数据评测和隐藏定律合成提供共同的问题基础。

> 直观理解：它确保题目不是脱离领域含义的数字拟合游戏，而是能够追溯到真实科学研究的数据与规律。

**2. 双世界任务模块**

SciLaws-Real 固定真实观测，并分别关注留出预测拟合和源文献支持的科学有效性；SciLaws-Parallel 使用从已发表形式派生的合成隐藏定律，并允许模型主动查询残差校准世界。两者分别隔离固定记录发现与主动恢复新规律这两种能力。

> 直观理解：同一类科学问题被做成两种考试：一种只能读现成记录，另一种可以自己提问和做实验。这样可区分模型的拟合能力、科学判断能力与主动探索能力。

**3. 单组／多组定律模块**

单组任务令一个函数形式及其参数集合对全部样本全局有效；多组任务令所有组共享函数形式，但部分参数允许按组变化。该设计把发现目标从单数据集拟合扩展到跨组稳定的结构识别。

> 直观理解：它检查模型找到的是可复用的规律骨架，还是只对某一组数据有效的一次性曲线。

**训练与推理**

基准本身不规定模型训练过程。评测 SciLaws-Real 时，被测模型接收某个科学问题的固定真实观测及相应任务信息，在不能增加观测的条件下生成候选定律；这些候选定律随后用于留出数据预测，并依据源论文所提供的科学信息判断其有效性。对于多组任务，模型还需输出或隐含表达一个跨组共享的函数形式，同时容纳部分组别参数变化。

评测 SciLaws-Parallel 时，被测模型进入由合成隐藏定律定义的残差校准世界，并可主动选择查询以获得新观测；模型根据多轮查询结果恢复隐藏定律。该设置的关键是隐藏目标由已发表形式派生但被重新合成，因此目标并非简单复述原论文公式。所给节选没有说明查询轮数、查询预算、返回观测的噪声形式、候选公式的语法限制、参数估计程序或最终提交格式，不能据此补写。

**复现信息**

公平解释该方法时需要保留四项规模与结构信息：基准包含 118 个问题，覆盖六个学科、381 篇科学论文、291 条候选定律和约 800 万个真实数据点；每个问题原则上具有互补的 SciLaws-Real 与 SciLaws-Parallel 设置；前者由固定真实观测构成，后者由已发表形式派生的合成隐藏定律及主动查询世界构成；两种设置均可包含单组和多组问题。多组任务必须共享函数形式而允许部分参数按组变化，否则会改变其所测试的跨组泛化能力。

当前来源仅为第 2.1 节的概览，未提供六个学科的具体名称、论文和数据的筛选标准、训练集与测试集划分、真实数据预处理、残差校准方法、隐藏定律的采样或合成规则、主动查询协议、参数范围、噪声设置及评测实现。因此，这些内容均应记为“原文未明确报告”，不能仅凭该节选推断复现实验所需的具体配置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- SciLaws-Real：包含 118 个问题，来自 381 篇科学论文，覆盖六个学科、291 个候选定律和约 800 万个真实数据点。66 个任务为单组问题，使用基于文献设计的插值、输入范围外推、时间迁移或跨条件划分；52 个为多组问题，完整留出若干组，并将每个测试组再分为参数校准子集与互不重叠的评估子集。它用于测试固定观测记录下的定律发现、留出预测与科学有效性。
- SciLaws-Parallel：由相同的 118 个科学问题构造可主动查询的平行世界，保留科学语境、合法输入范围、有效性约束和组结构，但以残差校准模拟器替代固定观测。隐藏目标是从已发表公式出发、经过执行检查、拟合检查及科学完整性筛选后得到的新结构变体；模型从无观测开始，在任务特定预算内选择输入并恢复隐藏结构。
- AI Feynman 公式集：由教科书方程构成，仅作为八个共同 OpenAI 模型上的匹配冷回忆参照，用于判断 SciLaws-Real 的目标形式是否比常见教科书公式更难通过直接记忆得到；它不是主任务的训练集或统一预测测试集。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**SciLaws-Real 数值拟合分数 $S_N$**

每个任务先选用 RMSE、SMAPE、log-MAE 或 $R^2$ 中一个主指标，再相对于最强已发表公式的 $m_{\mathrm{ref}}$ 归一化并截断到 $[0,1]$。参考公式得 0.5，完美预测得 1.0，因此该分数衡量留出数据上的相对预测表现，而不直接判断公式是否符合科学机制。 （越高越好；高于 0.5 表示按该任务的留出指标优于最强已发表参考公式。）

</div>
<div class="metric-item" markdown="1">

**SciLaws-Real 科学有效性分数 $S_V$**

代码增强裁判依据冻结且有来源支撑的任务量表进行确定性探测和源码检查。若提交通过反作弊检查，则按满足条目数 $M_t$ 占总条目数 $N_t$ 的比例计分；查表、过量拟合常数或把自由度移出声明定律等行为会使全局门控 $a_t=0$，从而整项为零。 （越高越好；高分表示公式满足更多文献规定的科学约束，但仍依赖量表覆盖范围与裁判可靠性。）

</div>
<div class="metric-item" markdown="1">

**SciLaws-Parallel 结构恢复分数 $S_S$**

代码增强裁判比较提交公式与隐藏模拟器的机制结构，离散取 0、0.25、0.5、0.75 或 1，分别表示无效或无关、仅捕捉变量或趋势、恢复已发表基础结构、恢复基础结构及大部分新增项、完整恢复隐藏结构。代数等价和等价重参数化不受罚，预测接近但漏掉机制项仍会扣分。 （越高越好；1 表示结构在代数等价意义下完整恢复，且系数符号或尺度与隐藏机制一致。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 118 个 SciLaws-Real 任务、九个模型的无数据冷回忆审计

<div class="result-value" markdown="1">

在 1062 个任务—模型单元中，30.7% 被判为冷回忆，69.3% 未被冷回忆。作者据此主张，大多数单元不能仅凭受限任务描述稳定复现最强已发表参考结构。

</div>

这说明直接公式记忆是显著但非占主导的解释渠道：约三成单元存在稳定复现参考结构的证据，约七成没有达到“五次中至少三次”的判定门槛。不过，“未冷回忆”不等于证明模型在主任务中真正进行了科学发现；它也可能反映提示不足、采样不稳定，或模型知道相关规律但没有输出审计指定的最佳参考形式。

<div class="result-source" markdown="1">

来源：Appendix E.4 Main Results；Table 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across 118 tasks and nine models, 30.7% of task-model cells are cold-recalled, while 69.3% are not cold-recalled under this protocol.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 按任务统计九个模型的冷回忆覆盖情况

<div class="result-value" markdown="1">

56 个任务（47.5%）没有任何受审计模型达到冷回忆标准，构成作者所称的“discovery moat”；相对地，14 个任务（11.9%）被全部九个模型冷回忆，属于普遍熟悉的经典公式。

</div>

任务难度并非均匀分布：近半任务对所有受测模型都缺少稳定的无数据公式复现证据，而一小部分经典定律几乎必然受预训练记忆影响。因此，汇总平均分需要结合任务级记忆标签解释，否则在经典任务上的高分可能夸大实际发现能力。该结果只刻画九个模型和当前提示协议下的可回忆性，不能证明 56 个任务从未出现在训练语料中。

<div class="result-source" markdown="1">

来源：Appendix E.4 Main Results；Figure 11

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

There are 56 tasks, or 47.5% of the panel, that no audited model cold-recalls.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 按单组与多组任务结构分层的冷回忆分析

<div class="result-value" markdown="1">

多组任务的任务—模型单元冷回忆率为 40.2%，高于单组任务的 23.2%。作者推测，多组问题更常围绕具名的跨组定律或不变常数形式组织，因此更可能以经典闭式公式出现在训练语料中。

</div>

这一差异表明，任务的组织结构会影响记忆污染风险；多组任务虽然测试跨组共享规律，却不一定更能隔离预训练记忆。这里是观察性分层而非受控因果实验，因此不能断言“多组设计本身”导致回忆率升高；领域构成、公式知名度和任务描述方式都可能是混杂因素。

<div class="result-source" markdown="1">

来源：Appendix E.5 Type and Domain Findings；Figures 12–13

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Multi-group tasks have higher cold recall than single-group tasks: 40.2% versus 23.2% over all task-model cells (Figure 13).

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

- 每个 SciLaws-Real 任务中表现最强的已发表公式：其原始指标记为 $m_{\mathrm{ref}}$，归一化数值分固定为 0.5，是判断提交公式是否真正超越现有文献锚点的核心比较对象。
- 朴素基线：任务纳入条件要求至少一个已发表公式优于朴素基线。它主要用于数据与任务质量筛选，排除连简单关系都无法可靠验证的问题；节选未给出其具体形式及逐任务成绩。
- 已发表基础结构：在 SciLaws-Parallel 中对应结构分 0.5，用于区分只复现原论文公式与进一步识别隐藏世界新增修正项、交互项或其他机制结构。
- 无数据冷回忆：模型只看到目标量及有序输入变量的名称、符号、单位、描述和典型范围，不看到数据行、引用或论文文本。它不是发现算法本身，而是用于估计主任务成绩可能由预训练记忆解释的程度。

**实验想回答的问题**

- 在真实论文与观测数据支持的任务中，LLM 引导的系统能否提出既在留出数据上优于已发表参考公式、又满足文献所规定科学约束的闭式定律？该问题由 SciLaws-Real 检验，并刻意区分数值拟合分数 $S_N$ 与科学有效性分数 $S_V$，以判断“预测得准”是否等同于“科学上成立”。
- 当模型可以主动选择测量输入时，它能否在有限查询预算和经验噪声下恢复一个新合成的隐藏机制，而非仅复述训练语料中的已发表公式？该问题由 SciLaws-Parallel 的结构恢复实验及无数据冷回忆审计共同检验。

**实验实现**

SciLaws-Real 的公式在文献支持的留出划分上评估。单组任务采用任务特定的泛化划分；多组任务完整留出新组，仅允许利用每个新组的校准子集拟合组特定参数，再在独立子集上测试共享函数形式，并对测试组等权平均。数值拟合与科学有效性分开报告，以避免把经验预测成功误判为机制正确。任务元数据、可执行参考公式、变量映射、数据划分与有效性量表均经过人工核验。

SciLaws-Parallel 的模拟器先在真实数据上拟合隐藏定律参数，再在线性或对数残差空间去除残差趋势，以 k-NN bootstrap 重采样随机误差，并用缩放因子 $\alpha$ 调节噪声，使隐藏结构在查询预算内仍可识别。冷回忆审计覆盖 118 个任务与九个主表模型，共 1062 个任务—模型单元；每个单元以温度 0.8 采样五次，再由温度 0 的 GPT-4.1 判断与最佳参考公式是否结构等价，至少三次命中才记为冷回忆。节选未提供主表各模型在 $S_N$、$S_V$ 和 $S_S$ 上的具体成绩，因此不能据此重建模型性能排名。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 多组光学色散任务展示了跨组泛化协议：模型在 11 种晶体材料上训练，完整留出 CdSe、TiO$_2$ 和 ZnWO$_4$；对每种新材料，仅以短波长测量校准组特定参数，再用长波长测量检验共享定律。这个案例把“函数结构能否迁移到新材料”与“是否允许估计新材料参数”分开，但节选未报告该案例的模型得分。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces a benchmark that evaluates LLM scientific-law discovery and active reasoning over real and synthesized observations.; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`5f803d68cc80c6627ce6b862baf0294f25772b6238000379a84b994be01ad705`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
