---
title: "[论文解读] Frontier LLMs are effective batch optimizers: Assessing reasoning models in continuous and discrete settings"
description: "[arXiv 2609.03177][LLM 评测] 本文评估当前前沿推理型大语言模型能否在评估预算受限的条件下充当零样本批量黑盒优化器，并比较其在连续数值空间与语义丰富的离散分子空间中的能力和失效模式。"
arxiv_id: "2609.03177"
announcement_date: "2026-09-04"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:42:32.855576+00:00"
source_sha256: "577f2f6edcf23f9b7ed34bac80efe03432833c9a9b7078cf8d80e638eda29f0f"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "黑箱优化"
  - "批量优化"
  - "大语言模型"
  - "贝叶斯优化"
  - "连续优化"
  - "离散分子优化"
  - "SMILES"
  - "简单遗憾"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2609.03177</p>

# Frontier LLMs are effective batch optimizers: Assessing reasoning models in continuous and discrete settings

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Frank Hu, Shriram Chennakesavalu, David Graff</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03177v1) · [PDF 下载](https://arxiv.org/pdf/2609.03177v1) · **关键词** 黑箱优化, 批量优化, 大语言模型, 贝叶斯优化, 连续优化, 离散分子优化, SMILES, 简单遗憾<br>


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

本文评估当前前沿推理型大语言模型能否在评估预算受限的条件下充当零样本批量黑盒优化器，并比较其在连续数值空间与语义丰富的离散分子空间中的能力和失效模式。

**不用术语来说**：许多科学设计问题只能通过昂贵实验或计算才能知道一个候选方案有多好，因此不能逐一尝试所有可能方案；研究者必须根据少量已有结果，一次提出一批值得评估的新候选。本文要弄清：未经专门训练的前沿推理模型，是否已经能够承担这种“看过历史结果后成批提出下一轮候选”的工作，以及它在哪类问题上真正可靠。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 在统一的批量黑盒优化视角下考察 Anthropic 的 Sonnet 4.6、Opus 4.8 和 Opus 5，覆盖不同维度且经过域与值域伪装的连续测试函数，以及以 SMILES 字符串表示候选、由 PMO 确定性预言机评分的离散分子优化任务。
- 刻画模型能力的适用边界：作者报告其连续数值优化可与采用高斯过程和期望改进准则的经典贝叶斯优化竞争，但对任务变换、维度和批大小较敏感；在语义丰富的分子空间中，模型则表现出更强的性能与样本效率，说明预训练先验的价值取决于搜索空间与训练数据结构的相似程度。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究昂贵目标函数下的批量黑箱优化：算法无法利用目标函数的解析形式或梯度，只能提交候选点并观察评分，因此必须在有限评估预算内尽快找到高质量解。经典贝叶斯优化通常以高斯过程等概率代理模型近似目标函数，再用期望改进等采集函数兼顾探索未知区域与利用已知优良区域；本文则把前沿自回归大语言模型视为优化策略，考察其能否根据历史候选及评分直接提出下一批候选。研究同时覆盖连续数值空间与离散分子空间，后者使用可由语言模型处理的 SMILES 字符串表示分子。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**黑箱优化（Black-box Optimization, BBO）**

目标函数内部结构、梯度或解析表达式不可供优化器使用，算法只能通过输入候选并读取输出分数来搜索最优解。当一次评估耗时或昂贵时，核心目标是在严格预算内用尽量少的查询找到尽量好的候选。

</div>
<div class="concept-item" markdown="1">

**批量优化（Batch Optimization）**

优化策略每轮不是只提出一个点，而是同时提出大小为 $q$ 的候选集合，再统一获得这些候选的目标值。它适合并行实验，但同一批候选在生成时无法利用彼此尚未返回的结果，因此需要兼顾批内多样性和质量。

</div>
<div class="concept-item" markdown="1">

**贝叶斯优化与采集函数**

贝叶斯优化用概率代理模型估计未知目标函数及预测不确定性，再通过采集函数选择下一批值得评估的点。本文提到的高斯过程代理与期望改进采集函数构成经典非 LLM 对照，其作用是平衡探索与利用。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定搜索空间 $\mathcal{H}$ 和只能通过查询获得数值的目标函数 $f:\mathcal{H}\rightarrow\mathbb{R}$，任务是在总计 $N$ 次函数评估内寻找使 $f$ 最大的候选。搜索空间既可以是 $d$ 维连续子空间，也可以是由 SMILES 等符号序列构成的离散空间；优化过程共有 $N/q$ 轮，每轮策略提出一个点或包含 $q$ 个点的批次，并在获得对应目标值后继续决策。作为 LLM 优化器时，提示包含历史候选、历史评分和剩余轮数，模型输出下一批候选；单轮会话在每次决策时重新提供历史，多轮会话则保留同一对话及先前推理。若真实最优值已知，则以瞬时遗憾和整条轨迹的简单遗憾衡量结果，二者越低越好。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{H}$**

候选解的搜索空间；可为连续空间或离散空间。

</div>
<div class="notation-item" markdown="1">

**$f:\mathcal{H}\rightarrow\mathbb{R}$**

待最大化的黑箱目标函数，将候选点映射为实数评分。

</div>
<div class="notation-item" markdown="1">

**$h^{*}=\arg\max_{h\in\mathcal{H}}f(h)$**

搜索空间中的全局最优候选。

</div>
<div class="notation-item" markdown="1">

**$r_i=f(h^{*})-f(h_i),\quad r=\min_i r_i$**

第 $i$ 个候选的瞬时遗憾及整条优化轨迹的简单遗憾；数值越低表示越接近全局最优。

</div>

</div>

**直接相关的工作**

- **提示驱动的 LLM 优化策略（文献 [12]）**: 与本文最接近，同样以提示调用语言模型来代替完整优化策略；但原文指出该工作未系统研究标准贝叶斯优化测试函数上的批量 LLM 策略，也未将该方案用于分子优化。
- **提示驱动的 LLM 优化策略（文献 [26]）**: 同样把预训练语言模型作为直接提出候选的优化策略，是本文的重要方法前身；本文的区别在于重新评估能力更强的前沿推理模型，并统一覆盖连续数值任务和离散分子任务。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

药物发现等科学任务具有组合规模巨大的设计空间，而每个候选分子的实验或高成本计算评估都耗费时间与资源，导致可调用目标函数的次数受到严格限制。实际工作通常还希望并行评估一批候选，以利用实验设备或计算资源；因此需要一种能够依据有限历史观测，在每轮同时提出多个高价值候选的优化策略，而不是依靠穷举搜索。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **面向黑盒优化的专用方法**：这类方法不要求目标函数可求导，而是根据已评估候选及其得分建立搜索策略；文中明确提到的经典参照是高斯过程—期望改进方法，即用高斯过程近似未知目标，再用期望改进采集函数权衡高分区域的利用与不确定区域的探索。连续空间和离散空间通常分别采用针对其结构设计的专门算法。
- **基于大语言模型先验的优化**：该路线把预训练语言模型视为已吸收通用模式与领域知识的候选生成策略，让模型读取问题描述和已有评估反馈后直接推理并提出下一批候选。以往已有工作测试过较早版本的语言模型处理相近问题，但尚不足以说明新一代强化推理模型的批量优化能力。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 专用黑盒优化器通常依赖人为选择的代理模型、采集准则或离散空间结构，虽然是可靠基线，却未必能直接利用自然语言描述、SMILES 等表示所携带的领域语义；这可能限制其在语义丰富、组合复杂的设计空间中借助已有知识缩小搜索范围的能力。
- 已有语言模型研究主要涉及更早代模型或相近但不完全一致的问题设置，无法回答当前推理型前沿模型在批量决策下是否稳定，也缺少对连续与离散任务的并列评估；因此其表现究竟来自可迁移的优化能力、对已知函数的记忆，还是与预训练数据相似的语义先验，仍不清楚。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一项针对当前前沿推理型大语言模型的系统实证研究，在有限评估预算和批量提议条件下，同时覆盖连续数值与离散语义空间，并通过伪装连续函数的定义域和值域来抑制记忆利用，再与经典及领域专用方法比较性能、样本效率和脆弱性。

</div>
<div markdown="1"><span>核心问题</span>

当前一代前沿推理型大语言模型在无需额外调优或专门问题脚手架的情况下，能否成为有效的批量黑盒优化器；其相对经典贝叶斯优化和分子优化专用方法的竞争力，又如何随搜索空间类型、任务变换、维度及批大小而变化？

</div>
<div markdown="1"><span>作者直觉</span>

大语言模型的大规模预训练可被看作一种候选生成先验：模型不必完全从少量在线观测中学习搜索规律，而可调用训练期间形成的模式识别、推理和领域关联。若候选表示本身具有可读语义，例如 SMILES 中的化学结构模式，模型可能据此提出更有希望的局部修改；相反，被伪装且缺少语义线索的数值函数主要考验纯粹的探索—利用能力，因此更容易暴露模型对坐标变换、维度和一次生成候选数量的敏感性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法将前沿自回归大语言模型作为黑箱优化策略 $[?]$ 使用：给定目标函数 $f:\mathcal{H}\rightarrow\mathbb{R}$、搜索空间 $[?]$ 和已评估的候选点，模型根据提示生成下一轮的单个候选点或候选批次，再由目标函数进行评估，并将结果反馈到后续提示或同一对话中。研究比较单轮与多轮交互，以及不同批大小下 Sonnet 4.6、Opus 4.8 和 Opus 5 的优化行为；模型本身不在该流程中进行参数训练，而是作为零样本优化器进行推理。直观地说，模型像一个根据“历史尝试—得分—剩余预算”不断提出新方案的决策者，但每次方案的好坏仍由外部黑箱函数决定。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 定义黑箱优化任务

将任务表述为寻找 $h^{*}\in\mathcal{H}$，使目标函数值最大；优化过程被划分为 $N/q$ 轮，每轮可提交一个点或大小为 $q$ 的候选批次。

<div class="method-step__io" markdown="1">

**输入**：搜索空间 $[?]$、目标函数 $f:\mathcal{H}\rightarrow\mathbb{R}$、总评估预算 $N$ 和每轮批大小 $q$。<br>
**输出**：一个需要通过有限次函数调用逐步搜索的黑箱优化问题。

</div>

**直观理解**：模型看不到目标函数的内部公式，只能提交候选方案并观察得分。总预算相当于可进行的试验次数，批大小决定每轮同时试验多少个方案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造优化提示

将与优化问题有关的历史信息组织为提示 $x\in\mathcal{X}$；在单轮设置中，每轮可基于更新后的历史记录重新构造提示，在多轮设置中则保留同一会话，使模型能够参考优化过程中产生的先前推理。

<div class="method-step__io" markdown="1">

**输入**：此前选取的点及其目标函数值、当前轮次信息和剩余评估预算。<br>
**输出**：供大语言模型读取的离散提示 $x$。

</div>

**直观理解**：这一步相当于给模型一份实验日志：哪些方案已经试过、得分是多少、还剩多少次机会。多轮会话则像让同一位分析者持续工作，而不是每轮都重新接手。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 由语言模型提出候选

从条件分布 $y\sim\pi(\cdot\mid x)$ 中采样响应；响应被解析为一个待评估点或一个候选批次。实验覆盖 Anthropic 的 Sonnet 4.6、Opus 4.8 和 Opus 5，并比较单点与批量提议。

<div class="method-step__io" markdown="1">

**输入**：提示 $x$ 和指定的前沿自回归模型策略 $[?]$。<br>
**输出**：下一轮待由目标函数评估的候选点集合。

</div>

**直观理解**：模型不是直接计算最优解，而是阅读历史并生成新的试验方案。批量模式下，它一次提出多个方案，以减少交互轮数并测试其并行探索能力。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 评估并反馈候选

调用目标函数得到每个候选点的函数值，将点—值对加入优化轨迹，并在后续轮次作为新的提示信息；在多轮设置中，相关历史还保留在同一对话中。

<div class="method-step__io" markdown="1">

**输入**：模型提出的候选点或候选批次，以及黑箱目标函数 $f$。<br>
**输出**：更新后的候选轨迹、函数评估记录和下一轮优化上下文。

</div>

**直观理解**：外部评价器像实验室中的测量仪器，只返回方案的效果分数。模型据此修正下一轮建议，但不能读取评价器内部如何产生分数。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 黑箱优化目标

$$
h^{*}=\arg\max_{h\in\mathcal{H}}f(h)
$$

**符号说明**

- $h^{*}$：搜索空间中的最优候选点。
- $\mathcal{H}$：候选解组成的搜索空间，可以是连续空间或离散空间。
- $f$：黑箱目标函数，将候选点映射为实数评价值。
- $h$：搜索空间中的任意候选点。

<div class="equation-explanation" markdown="1">

**直观理解**：该式规定优化任务的最终目标：在所有合法候选点中找到函数值最大的一个。模型不直接求解这个最大值，而是通过有限次提出候选并获得反馈来逼近它。<br>
**原文位置**：第 3.1 节“Black-box optimization”

</div>

</div>

<div class="equation-block" markdown="1">

#### 瞬时遗憾与轨迹简单遗憾

$$
r_i=f(h^{*})-f(h_i),\qquad r=\min_i r_i
$$

**符号说明**

- $r_i$：第 $i$ 个候选点的瞬时遗憾。
- $f(h^{*})$：最优点的目标函数值。
- $h_i$：轨迹中第 $i$ 个被评估的候选点。
- $f(h_i)$：第 $i$ 个候选点的目标函数值。
- $r$：整条优化轨迹的简单遗憾，即所有候选点中最小的瞬时遗憾。
- $i$：候选点在优化轨迹中的索引。

<div class="equation-explanation" markdown="1">

**直观理解**：瞬时遗憾衡量某一次尝试与最优值相差多少；轨迹简单遗憾取所有尝试中最好的那一次。由于目标是最大化函数，遗憾越低表示模型至少找到过一个越接近最优的候选点。<br>
**原文位置**：第 3.1 节“Black-box optimization”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文将大语言模型作为零样本黑箱优化策略使用，未描述针对这些优化任务进行参数更新、监督微调或强化学习训练的目标。因此训练目标不适用；优化目标体现在外部函数 $f$ 的最大化以及由遗憾衡量的推理表现，而不是模型参数训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 黑箱目标函数与有限预算评估器**

目标函数定义为 $f:\mathcal{H}\rightarrow\mathbb{R}$，搜索空间 $[?]$ 可以是连续空间，例如 $[?]\subset\mathbb{R}^{d}$，也可以是语言建模等离散空间。策略在总预算 $N$ 下进行 $N/q$ 轮评估，每轮提交单点或批次。

> 直观理解：这是模型无法直接打开的评分系统。它规定哪些候选方案合法，并告诉模型每个方案的效果，但模型只能通过有限次数的试验逐步搜索。

**2. 自回归语言模型优化策略**

模型被抽象为策略 $[?]$，接收离散提示 $x\in\mathcal{X}$，并从 $y\sim\pi(\cdot\mid x)$ 生成离散响应 $y\in\mathcal{Y}$；响应可以编码单个点或候选批次。研究使用 Anthropic 的 Sonnet 4.6、Opus 4.8 和 Opus 5。

> 直观理解：模型在这里扮演“提出实验方案”的角色，而不是传统优化器中的显式数学规则。其预训练形成的语言和推理先验被用于理解历史结果并生成下一批候选。

**3. 单轮与多轮交互机制**

单轮设置中，第 $i$ 轮依据此前选取的点及其函数值形成提示 $x_i$，并采样 $y_i\sim\pi(\cdot\mid x_i)$；多轮设置维护一个连续对话，使模型能够反思优化过程中先前输出的推理。

> 直观理解：单轮模式像每次把实验记录交给一个重新开始的顾问；多轮模式像同一位顾问持续记住自己的分析，从而检验显式会话记忆和反思是否有帮助。

**训练与推理**

该流程是推理阶段流程：先把优化问题信息、历史候选及其函数值和剩余预算编码到提示 $x$ 中，再从策略 $[?]$ 的条件分布 $y\sim\pi(\cdot\mid x)$ 中采样响应，并将响应解析为单个点或候选批次。外部目标函数评估这些候选后，结果被加入下一轮提示；单轮设置重新依据历史构造提示，多轮设置继续使用同一对话并允许模型参考此前推理。原文未明确报告提示模板、候选格式解析规则、采样次数或停止条件。

**复现信息**

可据原文确认的复现实验要素包括：比较 Anthropic 的 Sonnet 4.6、Opus 4.8 和 Opus 5；覆盖连续和离散搜索空间；比较单轮与多轮设置；每轮可评估单个点或大小为 $q$ 的批次；总函数评估预算为 $N$，相应轮数为 $N/q$。原文未明确报告具体提示文本、温度或其他解码参数、批次构造约束、函数评估并行方式，以及不同模型的调用次数或成本控制。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 合成连续优化任务：Branin、Hartmann-3、Hartmann-6、Ackley 和 Rastrigin 五个有已知全局最优值的经典测试函数。每个函数的定义域统一归一化为 $[0,1]^d$，必要时取负，从而都写成最大化问题。除原始版本外，每个函数还有一个伪装版本：输入依次经过逐轴幂扭曲、随机翻转和坐标置换，输出再经过随机仿射变换。因此共形成十个“函数—版本”任务，用于区分一般黑盒搜索能力与对著名函数形状、最优位置或最优值的识别能力。
- PMO 分子优化基准：包含 23 个确定性小分子 oracle，覆盖异构体、目标分子再发现、结构相似性和多性质优化等任务。候选分子以离散的 SMILES 字符串表示；oracle 没有解析形式的已知最优解，但能以低成本、无评估噪声的方式给每个分子打分。该基准用于测试模型能否利用预训练获得的化学与序列先验，在更接近自然语言生成结构的离散空间中进行低预算批量搜索。
- ZINC 250K：PMO 每条轨迹从该分子集合中随机抽取 10 个初始分子，随后由方法提出新候选。它在本文中仅承担初始化来源的角色，而不是训练集或独立测试集；原文没有报告进一步的数据划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Simple regret（简单遗憾）**

在当前已评估候选中，已知全局最优目标值与最佳已获目标值之间的差。本文对所有合成任务统一做最大化处理，因此可理解为 $r=f(h^*)-\max_i f(h_i)$；达到机器精度意义下的零表示已找到全局最优值。该指标既按函数评估次数绘制轨迹，也报告五个随机种子中最佳候选对应的最低遗憾。 （越低越好，因为它直接衡量当前最佳候选距离已知全局最优值还有多远，零为理想值。）

</div>
<div class="metric-item" markdown="1">

**Top-10 AUC**

随 oracle 调用预算推进，当前排名前十分子的平均表现所形成曲线的面积。它不仅关心最终找到的分子，还奖励更早找到高分分子，因此本文将其视为衡量低预算样本效率的核心指标。 （越高越好，因为更大的面积意味着方法在更多早期预算阶段已经维持较高的前十候选质量。）

</div>
<div class="metric-item" markdown="1">

**Top-10 mean**

在指定 oracle 调用预算下，当前十个最高分分子的平均 oracle 得分。与只看单个最佳分子相比，它要求方法稳定地产生一组高质量候选；本文还用该曲线计算其他方法达到 Opus 5 水平所需的预算倍数。 （越高越好，因为它表示方法找到的高分候选集合整体质量更高，而非仅有一个偶然的高分样本。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 合成函数：Opus 5 多轮与 GP-EI，在五个函数的原始和伪装版本及 $q\in\{1,2,4\}$ 下比较。

<div class="result-value" markdown="1">

作者报告，Opus 5 多轮在各批量大小下均能在十个任务中的多数任务上取得低于 GP-EI 的简单遗憾，说明前沿推理模型在固定预算下可以成为有竞争力、甚至在部分标准函数上更强的零样本批量优化器。分析上，这一结果只支持其在本组低维著名测试函数上的竞争力，并不证明对任意连续黑盒函数都优于贝叶斯优化；同一节的伪装实验还显示其优势具有明显脆弱性。

</div>

简单说，模型仅根据先前点及其分数，就经常能比经典 GP-EI 更快或更准确地靠近最优点。但这些测试函数可能已以名称、公式、图形或数值模式出现在预训练材料中，所以高分既可能包含在线推理和搜索，也可能包含对熟悉函数的识别，不能直接等同于普适数值优化能力。

<div class="result-source" markdown="1">

来源：第 5.1 节，图 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We see that across all batch sizes, Opus 5 multi-turn outperforms GP-EI on a majority of the 10 optimization tasks, with the LLM regret slightly degrading with increasing batch size as evidenced by the upward vertical drift observed for the tasks other than the plain Ackley function and the two Branin variations.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### PMO 的 23 个离散分子 oracle：三代前沿模型的单轮与多轮条件，在 210 次 oracle 调用预算下比较。

<div class="result-value" markdown="1">

作者报告，Opus 5 在 23 个 oracle 中有 17 个取得最佳 Top-10 AUC，并在 20 个中取得最佳 Top-10 mean；所选任务上也呈现模型代际越新表现越好、多轮优于对应单轮的趋势。分析上，这表明持续保留并利用搜索历史对复杂离散空间很重要，也显示较新的模型更有效，但实验没有隔离模型规模、训练数据、推理算法或产品版本变化中的哪一项导致了提升。

</div>

多轮模型可以记住哪些分子已尝试、哪些结构改动有效，并据此调整下一批候选；单轮模型缺少这种持续状态。因而这里的优势更像“带记忆的迭代实验设计”胜过“每轮重新开始”，而不是单纯证明模型拥有更强的静态化学知识。

<div class="result-source" markdown="1">

来源：第 5.2 节，图 3；全部 oracle 结果见附录 B.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the selected tasks, model performance increases with newer generations of frontier reasoning models and multi-turn performance exceeds the corresponding single-turn performance, resulting in Opus 5 multi-turn once again being the best-performing condition. Indeed, on the full set of 23 oracles, Opus 5 is the best by Top-10 AUC in 17 out of the 23 cases, and the best by Top-10 mean in 20 out of the 23 cases.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### PMO 全部 oracle：Opus 5 多轮与 GenMol、ExLLM 等专业方法在 210 次调用后的最终 Top-10 mean 比较。

<div class="result-value" markdown="1">

作者报告，23 个 oracle 上的平均 Top-10 mean 为：Opus 5 多轮 0.596、GenMol 0.590、ExLLM 0.738。由此可见，直接使用、未经额外调优或脚手架化的 Opus 5 在最终候选集合质量上与专门训练的 GenMol接近，但仍明显落后于最佳方法 ExLLM。该平均值不能说明 Opus 5 在每个任务都接近 GenMol，也不能消除不同方法训练资源和系统支撑不对等的问题。

</div>

这一结果的决策意义是：若缺乏时间搭建专用分子优化系统，通用前沿模型可作为较强的即用型低预算方案；若追求最高总体性能，专门方法仍有优势。平均分还会掩盖任务差异，例如所选异构体和 mestranol 相似性任务上，Opus 5 落后于专业方法。

<div class="result-source" markdown="1">

来源：第 5.2 节；完整结果见附录 B.3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

However, we note that in terms of Top-10 mean at a budget of 210, GenMol is comparable to Opus 5 multi-turn (0.590 average across oracles for GenMol versus 0.596 for Opus 5) with ExLLM being the best-performing method with an average of 0.738 across oracles (see Appendix B.3).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 合成基准存在预训练污染或记忆混杂。Branin、Hartmann、Ackley 和 Rastrigin 都是公开且著名的测试函数；即使隐藏名称并变换输入输出，模型仍可能从有限观测的拓扑、特征值或局部形状推断函数身份。论文的伪装分析揭示了这一问题，但不能严格量化记忆与现场优化推理各自贡献多少，因此“超过 GP-EI”不应直接外推为普适连续优化能力。
- PMO 比较并非完全资源对等：通用模型没有额外调优或脚手架，而 GenMol 等方法拥有专门分子训练数据，ExLLM 和 MolLEO 则有更多系统结构；反过来，前沿闭源模型也可能包含未知规模的化学预训练知识。部分方法因无代码或无完整轨迹只能在附录比较最终结果，样本效率分析还依赖“首次达到 LLM 水平”的轨迹定义。实验仅覆盖 23 个确定性 oracle 和五个随机种子，也未在摘录中报告真实合成可行性、实验室验证、推理成本或 API 成本，因此结论限于计算 oracle 下的候选优化。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- GP-EI：以高斯过程作为目标函数代理模型，并用期望改进量选择候选点，是低维、昂贵黑盒函数上经典且较强的贝叶斯优化基线。它与大语言模型采用相同批量大小和总评估预算，因此可直接检验语言模型的连续优化表现是否来自更宽松的查询条件。
- Random：随机提出候选点，表示不利用历史观测和结构先验时的最低参照。它用于确认性能提升是否确实来自自适应优化，而不仅是固定预算下偶然抽到高分点；摘录未给出其逐项结果。
- PMO 通用或传统优化方法组：包括 REINVENT、SynNet、基于贝叶斯优化的方法、搜索方法、screening 和 SMILES GA 等。它们代表强化学习、合成路径生成、代理模型、启发式搜索及枚举筛选等不同范式，用来判断零样本前沿模型是否优于并非专为当前低预算设定设计的方法。
- PMO 专门化方法组：主要包括 SMILES Augmented Memory、GenMol、ExLLM 和 MolLEO。GenMol 已在大规模小分子数据上训练，MolLEO 与 ExLLM 则在语言模型外加入更多任务脚手架，因此这组比较检验的是“直接使用通用前沿模型”与“专门训练或系统化包装的方法”之间的性能和样本效率差距。LICO 与 GP-MoLFormer-SIM 因缺少代码或完整轨迹，只在附录中按可得最终结果比较。

**实验想回答的问题**

- 在连续黑盒优化中，前沿推理型大语言模型能否在固定函数评估预算下充当有效的批量优化器，并与经典的高斯过程贝叶斯优化相竞争？进一步地，这种能力是否能在坐标置换、翻转、非线性扭曲、输出仿射变换、维度变化及批量大小变化后保持稳定？
- 在以 SMILES 字符串表示的离散分子空间中，未经任务微调或额外优化框架支撑的前沿大语言模型，能否以较少的确定性 oracle 调用取得有竞争力的分子，并在最终质量与样本效率上接近专门训练或高度脚手架化的方法？

**实验实现**

连续实验同时考察单轮与多轮交互，并令每轮批量大小为 $q\in\{1,2,4\}$。每条轨迹的总函数评估预算固定为 $N=120$，先提供 $2d$ 个与维度相关的初始点，再按批量提出候选；原文称轨迹长度按 $N/q$ 计算。每种方法均使用相同批量大小和总预算，并运行五个随机种子。伪装输入变换为 $\mathcal{T}=\mathcal{P}\circ\mathcal{F}\circ\mathcal{W}$：$\mathcal{W}$ 对各轴使用随机指数幂，$\mathcal{F}$ 以伯努利变量决定是否将坐标翻转为 $1-h_i$，$\mathcal{P}$ 随机置换坐标轴；输出另作随机尺度和平移。直观上，这些变换保留可逆对应关系及最优目标值，却改变模型熟悉的坐标位置、方向、尺度和函数数值，用来测试其是否真正依据反馈搜索。

PMO 实验对 Sonnet 4.6、Opus 4.8 和 Opus 5 都测试单轮与多轮条件，并在全部 23 个 oracle 上各运行五个随机种子。每条轨迹从 10 个随机 ZINC 250K 分子开始，之后执行 20 个批次、每批 10 个分子，总 oracle 预算为 210，远低于原 PMO 研究采用的 10000 次预算；适用时遵循相应方法原论文的早停规则。作者先在相同的 210 次预算下比较 Top-10 AUC 与 Top-10 mean，再利用专业方法的完整轨迹，计算其首次达到 Opus 5 最终 Top-10 mean 所需的调用数与 210 的比值。图中均值和误差带或误差条来自五个种子，表示为 $\pm1$ 个标准误。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 函数伪装与维度：将同一合成函数的输入作可逆的幂扭曲、翻转和轴置换，并对输出作仿射变换，再与原始版本比较。 | 作者观察到，Opus 5 对每个任务的伪装版本都持续差于原始版本，而 GP-EI 的表现基本保持一致；在 Hartmann-6、Ackley 和 Rastrigin 等较高维任务中，伪装后模型不再达到零遗憾。该对照主要隔离“熟悉的坐标、尺度、最优位置和值域模式”带来的帮助：目标问题在可逆意义下仍等价，但表面形式改变后性能下降，说明模型并非只执行与参数化无关的黑盒优化。 | 这相当于把同一座山重新旋转坐标、翻转方向、拉伸地形并改写海拔刻度。真正对这些表示变化稳健的优化器应大致保持表现；语言模型明显退化，意味着它可能部分依赖见过的地形特征。低维任务仍能被识别或搜索好，因此该实验提示的是脆弱性和记忆混杂，而不是证明所有成功都来自背诵。 | 第 5.1 节，图 2<br><span class="experiment-evidence">However, for the higher-dimensional tasks Hartmann-6, Ackley, and Rastrigin, disguising both the domain and the range leads to a significant loss in performance, with the model no longer able to attain the zero regret optimum.</span> |
| 批量大小敏感性：保持总预算不变，将 Opus 5 多轮每次提出的候选数从 $q=1$ 改为 $q=2$ 或 $q=4$，并与 GP-EI 的对应变化比较。 | Hartmann-3 上，Opus 5 的原始版平均简单遗憾从 $q=1$ 时的 $1.00\times10^{-6}$，变为 $q=2$ 时的 $2.96\times10^{-3}$ 和 $q=4$ 时的 $1.57\times10^{-3}$；伪装版对应为 $1.00\times10^{-6}$、$4.57\times10^{-3}$ 和 $1.14\times10^{-2}$。作者同时指出 GP-EI 跨批量大小更稳定。该对照隔离的是反馈频率与并行提案的影响：批量越大，在相同总预算下模型越少获得中间反馈，且必须一次生成更多彼此有价值的点。 | 一次只提一个点时，模型每得到一个新分数就能修正方向；一次提四个点时，同批候选之间无法互相利用新反馈。遗憾总体上升说明模型的搜索策略依赖频繁交互，尚未稳定解决批内候选的多样性与互补性问题。不过数值并非随 $q$ 严格单调，因此不能把全部变化归因于单一机制。 | 第 5.1 节，图 1<br><span class="experiment-evidence">This vertical shift is most noticeable for the Hartmann-3 task, where the plain (disguised) average simple regret is 1.00×10−6 (1.00×10−6) for q=1, 2.96×10−3 (4.57×10−3) for q=2, and 1.57×10−3 (1.14×10−2) for q=4.</span> |

**定性案例**

- 样本效率案例：作者以 Opus 5 多轮在 210 次调用后的 Top-10 mean 为目标，统计专业方法首次达到该水平所需的额外预算。四个所选任务中，ExLLM 的预算倍数均不超过 $1\times$；GenMol 仅在 thiothixene 再发现任务上比 Opus 5 更低效。其余所选方法即使最终能够追平，最省样本者也至少需要约三倍调用，许多方法需要 20–40 倍；screening 在四个任务中的三个、SMILES GA 在 thiothixene 再发现、SynNet 在 osimertinib MPO 上始终没有追平。作者据此强调 Opus 5 的低预算竞争力；分析上，这并不表示它优于 ExLLM、GenMol 或 MolLEO，而是说明它相对一批传统方法能更快利用少量反馈。来源：第 5.2 节，图 5。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Evaluates frontier reasoning LLMs as batch optimizers across continuous numerical and semantically rich discrete search problems.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`577f2f6edcf23f9b7ed34bac80efe03432833c9a9b7078cf8d80e638eda29f0f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
