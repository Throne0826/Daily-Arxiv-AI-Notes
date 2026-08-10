---
title: "[论文解读] The Optimizer Is the Agent: Reasoning-Driven Search across Prompts, Programs, and ML Workflows"
description: "[arXiv 2608.06714][LLM Agent] 原文未明确报告。"
arxiv_id: "2608.06714"
announcement_date: "2026-08-10"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-10T02:41:39.573832+00:00"
source_sha256: "a8bd186e01f9d6bc0150cece7d249459f18d8e9c26f4791975ebfc533593e8f1"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "ReASearch"
  - "推理驱动智能体搜索"
  - "提示词优化"
  - "程序演化"
  - "机器学习工作流优化"
  - "工具调用"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.06714</p>

# The Optimizer Is the Agent: Reasoning-Driven Search across Prompts, Programs, and ML Workflows

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-10</span>
<span><strong>作者</strong> Junbo Li, Boyi Liu, Canwen Xu, Yite Wang, Yuxiong He, Zhangyang Wang, Qiang Liu, Zhewei Yao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> The University of Texas at Austin</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.06714v1) · [PDF 下载](https://arxiv.org/pdf/2608.06714v1) · **关键词** ReASearch, 推理驱动智能体搜索, 提示词优化, 程序演化, 机器学习工作流优化, 工具调用<br>


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

本文处于基于大语言模型（LLM）的文本型工件优化领域，目标对象包括系统提示词、程序代码与机器学习（ML）训练工作流。这些对象的候选空间通常庞大、离散且具有语义结构：一次修改可能是改写一段自然语言、重构一段程序，或调整训练配置。现有系统常让LLM依据执行反馈提出局部修改，同时由进化搜索、多臂老虎机、贝叶斯优化或文本梯度等外部控制器决定候选分支、评估顺序、计算预算分配及停滞后的恢复策略。本文研究能否将这些搜索决策主要交给一个可调用工具、能持续记忆搜索过程的推理智能体完成（来源：第1节 Introduction；附录A Related work）。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**外部搜索控制器**

指包裹在LLM之外的算法模块，按预先设计的规则管理候选解的生成、选择和评估。它通常决定何时探索新方案、何时继续优化已有较优方案，以及如何使用有限评估预算。

</div>
<div class="concept-item" markdown="1">

**工具调用智能体**

指能够在多轮交互中根据当前状态自行选择调用评估、分析、编辑或记忆等工具的LLM系统。与只生成一次修改建议的模型不同，它可利用工具返回的结果继续推理并调整后续行动。

</div>
<div class="concept-item" markdown="1">

**探索与利用**

探索是尝试尚不确定但可能带来更优结果的方案；利用是围绕当前表现最好的候选继续改进或验证。二者需要在有限的实验或评估次数内权衡。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文将优化过程视为一个序贯推理任务：输入是某一领域的初始文本型工件、该任务可调用的领域工具，以及由评估成本限定的搜索预算；工具覆盖候选方案的评估、结果分析、工件编辑和跨轮次记忆。输出是在预算内得到的改进提示词、程序或ML工作流，并伴随由智能体自行决定的评估、修改、验证、回退与停止轨迹。核心设定不是为每个领域另行编写固定的外层搜索循环，而是在三类任务上复用同一智能体脚手架，只替换领域相关工具；因此要检验的是智能体推理能否承担原本由显式控制器负责的搜索策略（来源：第1节 Introduction）。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **DSPy、TextGrad 与 AdalFlow**: 这些文本梯度式优化框架利用语言反馈来指导修改，但其整体更新或搜索流程仍由外部启发式控制。本文将其作为“LLM负责语义编辑、控制器负责搜索策略”的代表性对照脉络（来源：附录A LLM-based text optimization）。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

提示词、程序和机器学习工作流的优化都需要在庞大且离散的候选空间中反复试验、诊断和修改。此类任务不仅要求生成有语义意义的编辑，还要求根据执行反馈决定下一步评估什么、如何分配有限预算，以及何时回退或停止，因此单次生成一个候选方案通常不足以完成有效优化。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **外部搜索控制器结合大语言模型语义编辑**：大语言模型根据执行结果提出提示词、代码或配置的修改，而贝叶斯优化、赌博机、进化搜索等外部控制器负责选择候选方案、安排评估顺序和分配搜索预算。模型主要承担局部的语义编辑，整体搜索策略由预先设计的算法管理。
- **基于文本梯度、规划或候选集演化的方法**：系统利用文本化的错误反馈、分数历史或规划信息生成改进方向，并通过候选集扩展、筛选和版本演化逐步寻找更优解。这些方法通常把分支选择、候选保留、停滞恢复等过程编码在固定的搜索循环中。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 搜索策略主要位于模型之外，外部控制器预先决定候选选择、评估调度和预算分配，导致大语言模型只能在固定循环中执行局部修改，难以根据不同任务的反馈结构动态改变搜索方式。
- 现有方法往往需要针对提示词、程序或机器学习工作流分别设计优化器和启发式规则；当搜索出现无效分支、停滞或疑似改进时，系统的验证、回退与重启行为受固定机制限制，因而可能浪费评估预算，也无法充分利用跨步骤积累的失败经验。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究证明大语言模型能够生成有意义的候选编辑，但尚未系统回答：若把候选评估、失败诊断、编辑选择、验证、回退和停止等核心搜索决策都交给同一个具备工具使用能力与持久记忆的推理代理，代理能否在提示词、程序和机器学习工作流等不同优化场景中承担原本由外部控制器完成的搜索策略。缺少的是一种统一的、弱化固定控制器的框架，以及对这种内部化搜索能力的跨领域评估。

</div>
<div markdown="1"><span>核心问题</span>

单个使用工具的推理代理，能够在多大程度上把原本由贝叶斯优化、赌博机或进化搜索等外部控制器承担的搜索策略内部化，并在相同预算下有效优化提示词、程序和机器学习工作流？

</div>
<div markdown="1"><span>作者直觉</span>

这些优化任务通常能够提供较丰富的反馈，例如执行分数、错误信息、候选差异和历史尝试结果。代理若能读取并分析这些反馈，就可以把一次次评估视为连续推理过程：先提出关于失败原因的假设，再选择有针对性的修改，随后验证改进是否真实，并在无效时回退或借鉴历史经验。这样，复杂的搜索行为不必完全依赖预先写死的控制器，而可能从代理对工具结果的持续推理、记忆和预算权衡中自然形成。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ReASearch 将提示词、程序和机器学习工作流统一表示为待优化的文本制品 $z\in\mathcal{Z}$。系统由一个具备工具调用、代码执行、上下文压缩和持久记忆能力的智能体组成：智能体读取当前状态，决定评估什么、如何分析失败、修改哪一部分以及何时验证、继续搜索或重启。与仅负责提出候选修改的传统方法不同，ReASearch 将候选生成、评估选择、失败诊断、预算分配和最终选择都交给同一个推理循环；直观地说，它不仅提出“下一版方案”，还像研究者一样根据实验记录决定下一步实验。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 定义优化任务与初始制品

将待优化对象表示为文本制品 $z\in\mathcal{Z}$，并通过奖励函数评估其输出质量。智能体获得当前优化状态、交互历史和可用工具集合 $\mathcal{A}_{\mathcal{T}}$。

<div class="method-step__io" markdown="1">

**输入**：任务实例 $x\sim\mathcal{D}$、初始提示词、程序或机器学习训练代码，以及任务专用的系统提示。<br>
**输出**：初始制品、任务状态和可调用的领域工具。

</div>

**直观理解**：先明确要改进的“文本对象”是什么，以及什么结果算得好。提示词、源代码和训练配置虽然形式不同，但都可以被读写、执行和评估。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 推理决策与候选评估

智能体根据系统提示和交互历史选择工具；通过评估工具获得奖励或指标，并使用 $\mathrm{python\_exec}$ 编写分析脚本、统计评估日志和定位失败模式。提示词任务中，智能体可自适应抽取训练小批次、重复测试困难样本或调用验证集评估；程序和工作流任务中，则按需运行代码或有限时长训练实验。

<div class="method-step__io" markdown="1">

**输入**：当前制品、历史评估记录、剩余预算和持久化经验。<br>
**输出**：候选制品的性能结果、轨迹或训练动态，以及对失败原因的分析证据。

</div>

**直观理解**：智能体不会固定地每轮随机抽样和修改，而是根据已有证据决定下一次检查什么。Python 工具相当于一个可随时使用的小型实验台，帮助它从原始结果中找规律。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 定向修改与约束验证

智能体提出有针对性的修改；程序演化和机器学习工作流优化通过编辑工具将修改交给独立子智能体执行，并由验证子智能体检查代码有效性和约束合规性。机器学习任务中，修改可以作用于超参数、学习率计划、正则化、模型结构、损失函数或优化器。

<div class="method-step__io" markdown="1">

**输入**：候选制品、失败诊断、历史经验和任务约束。<br>
**输出**：经过编辑和合法性检查的新制品。

</div>

**直观理解**：主智能体负责判断“为什么失败、应该改哪里”，专门的编辑器负责落实改动，验证器负责检查改动是否破坏程序或任务规则。这样可以保留主智能体的推理上下文，也减少无效协调。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 记忆更新、上下文管理与最终选择

当上下文过长或智能体主动决定压缩时，压缩工具将交互历史总结；智能体周期性读写持久化文件 $\mathrm{lessons.md}$，记录有效方法、失败方法、后续尝试和关键条件。优化结束时，智能体综合完整历史和经验选择已有候选，或合成新的最终制品，而不是机械选择验证分数最高者。

<div class="method-step__io" markdown="1">

**输入**：多轮实验结果、候选轨迹、验证指标和新发现的经验。<br>
**输出**：最终提示词、程序或机器学习工作流，以及可迁移到后续运行的经验文件。

</div>

**直观理解**：长期任务容易忘记早期实验，因此系统把重要结论写入“实验笔记”。最后的决策像研究者回顾全部实验后作判断，能够识别验证集偶然高分或某个候选的隐藏缺陷。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 统一优化目标

$$
z^{\star}\in\arg\max_{z\in\mathcal{Z}}\;\mathbb{E}_{x\sim\mathcal{D}}\left[\mathbb{E}_{Y\sim P(\cdot\mid x,z)}[r(x,Y)]\right]
$$

**符号说明**

- $z^{\star}$：最优文本制品，例如提示词、程序或机器学习训练配置。
- $\mathcal{Z}$：所有可行文本制品组成的搜索空间。
- $x\sim\mathcal{D}$：从任务实例分布中采样的输入，$\mathcal{D}$ 是该分布。
- $Y\sim P(\cdot\mid x,z)$：给定输入 $x$ 和制品 $z$ 后，系统生成的输出；$P$ 是输出条件分布。
- $r(x,Y)$：输入 $x$ 与输出 $Y$ 对应的奖励或质量函数。

<div class="equation-explanation" markdown="1">

**直观理解**：目标是在所有可行制品中找到一个，使它在任务输入分布上产生高质量输出；同时考虑模型输出本身的随机性。若任务不依赖具体输入，则外层对 $\mathcal{D}$ 的期望可以省略，变成直接最大化制品的期望奖励。<br>
**原文位置**：第 2.1 节，公式（1）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文将问题定义为对制品 $z$ 的黑盒奖励最大化，但没有给出 ReASearch 自身的梯度训练目标，也没有声称通过端到端参数更新训练控制器。优化发生在推理时：智能体根据评估反馈、代码分析和记忆逐轮提出并筛选制品；因此这里的“优化”主要是搜索策略和制品内容的改进，而不是训练一个新的模型参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 通用工具使用智能体**

智能体接收编码领域指导和当前状态的系统提示、交互历史及工具集合 $\mathcal{A}_{\mathcal{T}}$，在每一轮自主决定下一次工具调用。核心工具包括文件读写、Python/Bash 执行、任务评估、候选编辑和验证；其中 $\mathrm{python\_exec}$ 将语言推理扩展为可计算的分析过程。

> 直观理解：这是整个系统的控制中心。它不只是生成文本，而是能观察实验、运行程序、分析数据并据此安排下一步。

**2. 长程上下文与持久记忆**

上下文达到阈值或智能体主动剪枝时，压缩工具总结交互历史；持久文件 $\mathrm{lessons.md}$ 保存“有效方法、无效方法、下一步尝试”及其适用条件。该设计允许智能体跨多次试验形成和修正假设，并支持经验在新运行中的迁移。

> 直观理解：上下文压缩解决一次运行中信息过多的问题，持久记忆解决运行时间过长或需要重新启动的问题。保存的是可复用的经验，而不是简单堆积所有原始日志。

**3. 领域专用评估、编辑与验证工具**

提示词优化提供 $\mathrm{get\_next\_minibatch}$、$\mathrm{call\_student\_model\_batch}$ 和 $\mathrm{validate\_candidate}$；后者仅返回验证集聚合准确率，以降低逐样本反馈导致的过拟合。程序演化使用 $\mathrm{evaluate}$ 和 $\mathrm{edit\_code}$，机器学习工作流使用 $\mathrm{run\_experiment}$；任务差异被封装在工具集合和系统提示中，主循环保持不变。

> 直观理解：不同领域需要不同的“实验按钮”，但智能体的工作方式相同。工具只暴露必要的观测和操作接口，使它能够比较方案，同时避免直接获得会诱发验证集记忆的过细反馈。

**训练与推理**

该方法的核心流程是推理时搜索。运行开始时，智能体读取初始提示词、基线程序或训练代码；随后反复选择评估、分析、编辑和验证工具，获得新的奖励、准确率、程序输出或训练曲线，再依据这些结果决定继续探索、复查困难样本、修改制品、压缩上下文、更新 $\mathrm{lessons.md}$ 或重新开始。提示词优化使用训练集和验证集工具，且验证工具只返回聚合指标；程序演化先评估基线，再通过 $\mathrm{edit\_code}$ 修改并由验证子智能体检查；机器学习工作流则通过有限时长实验观察指标和训练动态。最终输出由智能体基于完整实验历史选择或综合生成。

**复现信息**

可复现所必需的结构性配置包括：一个通用代码智能体、文件读写、Python/Bash 执行、上下文压缩工具、持久化 $\mathrm{lessons.md}$，以及按任务类别提供的评估和编辑接口。提示词任务需要训练集、验证集和测试集，并允许按剩余预算自适应选择小批次；程序任务需要 $\mathrm{evaluate}$、代码编辑和约束验证；机器学习任务需要可控制时长的 $\mathrm{run\_experiment}$。原文未在所给方法节中明确报告完整的预算数值、模型调用温度、工具实现细节或所有停止条件，因此不应据此推断具体复现实验配置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 提示词优化任务：AIME 2025、GSM8K、HotpotQA 和 Terminal-Bench 2.0，分别覆盖数学推理、多跳问答和软件工程；原文明确报告使用测试集，并对每种设置进行 3 次独立运行后取平均。
- 程序演化任务：circle packing、Heilbronn triangles、交易调度（TXN）、专家并行负载均衡（EPLB）和 ARC-AGI-2，覆盖数学优化、系统编程及视觉推理；每个任务包含需要测试时优化的困难实例。
- 机器学习工作流任务：NanoGPT、IMG-100、Atari Q*bert、MuJoCo 和 DRW Crypto Market Prediction，覆盖语言建模、100 类图像分类、强化学习与时间序列预测；每个实验采用固定训练时间预算。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务准确率或准确性**

衡量模型在 AIME、GSM8K、HotpotQA、Terminal-Bench 2.0 及 ARC-AGI-2 等任务上产生正确答案或正确程序行为的比例；ARC-AGI-2 同时报告训练集和测试集准确率。 （越高越好，因为表示正确解答或泛化到未见输入的能力更强。）

</div>
<div class="metric-item" markdown="1">

**程序任务目标分数**

衡量 circle packing、Heilbronn triangles、TXN 和 EPLB 中候选程序的任务目标值；原文对 Heilbronn triangles 明确说明目标是最小三角形面积，但表中方向标为越高越好，具体目标定义需结合各任务评估器理解。 （按表格中的方向标判断；原文给出的程序结果表均使用向上箭头，表示数值越高越好。）

</div>
<div class="metric-item" markdown="1">

**机器学习工作流指标**

NanoGPT 使用 bits per byte（BPB），IMG-100 使用 accuracy，Atari Q*bert 与 MuJoCo 使用 reward，DRW Crypto Market Prediction 使用相关系数；这些指标分别反映语言建模损失、分类正确率、环境回报和预测相关性。 （原文说明 BPB 越低越好，accuracy、reward 和相关系数越高越好；原文对不同任务的统一方向未在所给片段中完整展开。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 提示词优化：AIME 2025、GSM8K、HotpotQA 与 Terminal-Bench 2.0 测试集

<div class="result-value" markdown="1">

ReASearch 四项任务均超过 GEPA：AIME 为 $52.00\pm0.67$，GSM8K 为 $83.40\pm0.30$，HotpotQA 为 $67.60\pm0.50$，Terminal-Bench 2.0 为 $53.33\pm1.96$；对应 GEPA 分别为 $50.67\pm1.15$、$82.11\pm0.45$、$65.80\pm0.80$ 和 $42.22\pm1.28$。

</div>

这一结果支持统一智能体循环在多个提示词领域具有稳定优势，尤其在 Terminal-Bench 2.0 上差距较大。它证明的是在本文给定学生模型、调用预算和智能体模型下的性能优势，不足以证明 ReASearch 对所有模型、预算或提示词优化算法都必然更好；3 次运行的均值和标准差也不能替代更大规模的显著性检验。

<div class="result-source" markdown="1">

来源：Table 1, Performance on test sets before and after system prompt optimization

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ReASearch 52.00 ± 0.67 83.40 ± 0.30 67.60 ± 0.50 53.33 ± 1.96

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 程序演化：TXN、EPLB 与 ARC-AGI-2

<div class="result-value" markdown="1">

ReASearch 在 TXN 上使用 GPT-5 得分 $4237$，在 EPLB 上使用 GPT-5 得分 $0.2305$；ARC-AGI-2 上，GPT-5 的训练/测试准确率为 $35.0\%/11.7\%$，Sonnet 4.6 为 $85.0\%/50.0\%$。这些结果超过同表中的 AdaEvolve 对应结果：GPT-5 的 TXN 为 $3636$、EPLB 为 $0.1976$，ARC-AGI-2 为 $20.8\%/5.0\%$；Sonnet 4.6 的 ARC-AGI-2 为 $21.9\%/12.5\%$。

</div>

这些任务检验的是智能体能否通过长期记忆、因果诊断和工具验证改写程序，而不是只从若干离散范式中选一个。ARC-AGI-2 的测试集差距尤其说明结构性规则分析可能比追求训练集上的近似匹配更重要；但不同模型骨干分别取得结果，不能把全部差异归因于搜索策略而忽略模型差异。

<div class="result-source" markdown="1">

来源：Table 4, Systems Programming Results (TXN and EPLB)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ReASearch GPT-5 4237 0.2305
Sonnet 4.6 4032 0.1471

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 程序演化：Heilbronn triangles 与 circle packing

<div class="result-value" markdown="1">

在 Heilbronn triangles 上，ReASearch 使用 Sonnet 4.6 的结果为 $0.03552$、$0.03260$、$0.02700$、$0.02429$、$0.02034$，分别对应 $n=11,12,13,14,15$；在 circle packing 上，同一模型的结果为 $2.478$、$2.530$、$2.587$、$2.636$、$2.684$、$2.735$、$2.790$、$2.843$、$2.890$、$2.940$，分别对应 $n=23$ 至 $32$。

</div>

该结果检验跨数值规模的程序发现能力。作者声称 ReASearch 在几乎所有程序任务上达到最好表现，某些情况下超过此前人类已知最好结果；从所给表格看，Sonnet 4.6 在 circle packing 的若干规模略高于人类行，但 Heilbronn triangles 的部分数值低于人类行，因此“超过人类结果”不能无条件推广到所有规模和任务。

<div class="result-source" markdown="1">

来源：Table 3, Heilbronn Triangle Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ReASearch Sonnet 4.6 0.03552 0.03260 0.02700 0.02429 0.02034

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

- 未优化提示词基线：直接使用学生模型的原始系统提示词，用于测量优化本身带来的增益。
- GEPA：提示词优化领域的最新算法；两种方法均使用 Claude Sonnet 4.6 作为智能体模型，并保持学生模型调用次数一致，因此可比较提示词搜索策略。
- AdaEvolve：将策略选择视为离散搜索，采样范式标签、为各范式生成代码并选择最好结果；用于比较程序演化中的显式策略搜索。
- Claude Code：官方 AutoResearch 设置的未修改版本，仅调整到相同墙钟预算；训练脚本、数据管线、评估器、硬件和单次实验训练上限均相同，用于比较机器学习工作流优化能力。

**实验想回答的问题**

- 在相近评测预算下，统一的推理驱动智能体能否在提示词优化、程序演化和机器学习工作流优化中超过专用优化器？
- 持久记忆与 Python 执行工具是否分别为跨长时程搜索、诊断和验证提供关键增益？

**实验实现**

ReASearch 在各领域共享同一智能体循环，由智能体决定评估什么、如何诊断失败、修改哪些候选、何时验证以及何时重启；领域差异主要由工具和领域级系统提示词模板提供。提示词优化中，ReASearch 与 GEPA 使用相同数量的学生模型调用，完整运行在标准缓存下的 API 成本低于 20 美元。程序演化中，一个预算单位等于一次目标问题评估调用，circle packing 和 Heilbronn triangles 按每个 $n$ 的上限为 500 次，ARC-AGI-2 每个谜题为 100 次，EPLB 和 TXN 为 500 次。机器学习工作流中，两种系统使用相同总墙钟预算，单次训练上限按任务为 5 至 30 分钟。所有设置均进行 3 次独立运行并报告平均值；详细数据划分与超参数位于附录 H。工具调用统计显示，提示词和程序优化中超过 70% 的调用用于 Python 推理，说明主要预算用于分析而非执行。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除持久记忆机制：提示词优化中的 AIME 与 Terminal-Bench | 原文说明移除记忆后影响较大，但所给片段没有提供 Table 7 的具体数值。 | 该消融隔离的是 lesson summaries 与 search tree 的作用。AIME 和 Terminal-Bench 需要跨多轮读取长评估轨迹、保存失败原因并回到旧候选；因此性能下降应解释为历史信息丢失导致的诊断和分支管理变弱，而不是证明记忆在所有任务上都是最重要组件。 | Appendix C, Component attribution; Table 7<br><span class="experiment-evidence">For prompt optimization on AIME and Terminal-Bench, the agent reads and analyzes long evaluation trajectories to identify weaknesses in the current prompt; these findings are easily lost across iterations, so memory has the larger impact.</span> |
| 移除 Python 执行工具：ARC-AGI-2 与 Heilbronn triangle | 原文说明在 ARC-AGI-2 中移除 Python 的影响略大于移除记忆；Heilbronn triangle 也呈现相同模式，但所给片段没有提供 Table 8 或 Table 11 的具体数值。 | 该消融检验 Python 是否承担候选算法推演、数据检查和提交前验证。ARC-AGI-2 与 Heilbronn triangle 的短周期模式识别和数学发现依赖即时计算，因此工具移除带来的更大影响支持“执行工具作为推理外接验证器”的解释，但无法从当前片段估计下降幅度。 | Appendix C, Component attribution; Appendix E, Table 11<br><span class="experiment-evidence">For ARC-AGI-2, where interaction rounds are shorter but pattern recognition and algorithmic discovery are central, Python execution has the larger impact.</span> |

**定性案例**

- ARC-AGI-2 Task 72 展示了分析优先于编码的效果：ReASearch 经过 31 轮分析，分别检验左右、上下和 $180^\circ$ 旋转对称，并识别出带整数中心取整规则的左右对称；AdaEvolve 的程序虽达到 $99.5\%$ 单元格准确率，却在 4 个训练样例中仅 2 个完全正确，因为它可能选择了错误的上下对称轴。该案例说明局部单元格准确率接近满分并不等于学到了正确的结构规则，工具辅助的反例分析更直接检验了能否泛化到未见输入。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work develops a persistent tool-using LLM agent that reasons over evaluations, diagnoses failures, and autonomously searches prompts, programs, and workflows.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`a8bd186e01f9d6bc0150cece7d249459f18d8e9c26f4791975ebfc533593e8f1`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
