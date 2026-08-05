---
title: "[论文解读] BBOWP-Bench: Evaluating LLMs on Black-Box Optimization Word Problems"
description: "[arXiv 2608.02612][LLM 评测] 本文提出黑盒优化文字问题（BBOWP）及其基准 BBOWP-Bench，用于检验大语言模型能否根据自然语言任务描述，同时设计搜索空间并选择适合评估预算的优化算法。"
arxiv_id: "2608.02612"
announcement_date: "2026-08-05"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:42:06.768852+00:00"
source_sha256: "32f29ab6db3291ef37b9237838665f64baf83f838890a914ca65d23b93d40835"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "黑盒优化"
  - "优化问题自动形式化"
  - "自然语言问题描述"
  - "搜索空间设计"
  - "算法选择"
  - "大语言模型"
  - "评估预算"
  - "BBOWP-Bench"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.02612</p>

# BBOWP-Bench: Evaluating LLMs on Black-Box Optimization Word Problems

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Yutaro Yamada, Kei Hiroshima, Nozomu Yoshinari, Kento Uchida, Shinichi Shirakawa</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Yokohama National University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.02612v1) · [PDF 下载](https://arxiv.org/pdf/2608.02612v1) · **关键词** 黑盒优化, 优化问题自动形式化, 自然语言问题描述, 搜索空间设计, 算法选择, 大语言模型, 评估预算, BBOWP-Bench<br>
**代码**: [https://github.com/shiralab/bbowp-bench](https://github.com/shiralab/bbowp-bench)

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

本文提出黑盒优化文字问题（BBOWP）及其基准 BBOWP-Bench，用于检验大语言模型能否根据自然语言任务描述，同时设计搜索空间并选择适合评估预算的优化算法。

**不用术语来说**：许多实际优化任务只能尝试一个方案并观察其得分，却不知道“方案如何决定得分”的明确公式。例如，调整机器学习超参数时，每组设置都要经过训练和验证才能知道效果。要解决这类问题，首先必须决定调整哪些变量、每个变量允许取什么范围，以及采用哪种搜索算法；这些决定往往依赖专家经验。本文关注能否让大语言模型直接阅读任务说明，自动完成这些关键决策，并通过真实优化运行判断其设计是否有效。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 BBOWP 问题设定：系统从自然语言描述 $d$ 出发，同时推断搜索空间 $S$ 与优化算法 $a$，把既有自动数学建模研究扩展到目标函数形式不可见的黑盒优化场景。
- 建立 BBOWP-Bench 数据集与评估框架：每个实例将自然语言问题描述、可执行评估环境和人工设计的参考方案配对，使研究者既能比较模型生成的搜索配置与人工方案，也能通过实际黑盒优化运行评估下游效果。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于“自然语言驱动的优化问题自动形式化”与黑盒优化（BBO）的交叉点。既有基准通常要求系统从文本中抽取变量、目标和约束，并将它们写成显式数学表达式；但超参数优化、分子设计、结构形状优化和昂贵仿真等任务往往无法获得目标函数的解析形式，只能通过实际评估观察候选方案的目标值。在这种条件下，形式化不只是翻译目标与约束，还必须决定向优化器开放哪些变量、各变量允许取什么范围，以及采用何种搜索算法；这些选择会直接影响有限评估预算下的最终解质量。BBOWP-Bench因此用带任务上下文的自然语言描述、可执行评估环境和人工参考形式化来衡量系统能否利用先验知识完成上述决策。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**黑盒优化（Black-Box Optimization, BBO）**

目标函数的内部表达式未知、不可解析或计算过程难以显式建模，优化器只能提交候选解并观察返回的目标值。由于一次评估可能来自训练、实验或仿真，通常必须在有限评估预算内高效搜索。

</div>
<div class="concept-item" markdown="1">

**搜索空间设计**

搜索空间规定优化器可以调整哪些设计变量、变量类型及其取值范围。遗漏关键变量会限制可达到的最优解，而范围过窄或各变量尺度失衡也可能使搜索难以覆盖有效区域。

</div>
<div class="concept-item" markdown="1">

**算法选择**

算法选择是根据变量空间、目标函数可能具有的结构以及评估预算，为当前任务选择合适的黑盒优化器。本文强调优化器不能脱离搜索空间预先固定，因为算法是否适用取决于二者的匹配关系。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

一个BBOWP实例向元求解器提供自然语言问题描述$d$，其中可包含任务背景、设计目标以及最大函数评估次数$N_{\mathrm{max}}$等信息；目标函数的显式形式不提供给元求解器，用户在描述任务时甚至可能尚未实现该函数。系统需要从$d$同时推断搜索空间$S$与优化算法$a$：$S$决定暴露给优化器的变量及其定义，$a$负责在该空间中产生候选解。随后，基准通过标识符映射调用内置目标函数，在不超过$N_{\mathrm{max}}$次评估的条件下执行真实黑盒优化，并结合人工设计的参考形式化比较搜索空间设计、算法选择及下游优化表现。该设置关注目标函数求值可执行但解析形式不可见的情形，而不是把文本直接转换成显式目标与约束公式。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$d$**

输入元求解器的自然语言问题描述。

</div>
<div class="notation-item" markdown="1">

**$N_{\mathrm{max}}$**

一次优化运行允许使用的最大目标函数评估次数，即评估预算。

</div>
<div class="notation-item" markdown="1">

**$S$**

系统推断的搜索空间，包括需要优化的变量及其定义或取值域。

</div>
<div class="notation-item" markdown="1">

**$a$**

系统为该任务及搜索空间选择的黑盒优化算法。

</div>

</div>

**直接相关的工作**

- **NL4Opt及后续线性、整数、混合整数与非线性优化自动形式化基准**: 这些工作评估从自然语言中抽取变量、目标和约束并生成求解器可用形式，但通常假定目标与约束能够写成显式数学表达式；BBOWP将问题扩展到只能观测目标值的黑盒场景，并要求联合设计搜索空间与选择算法。
- **ALE-Bench**: ALE-Bench考察智能体能否依据任务描述提升困难优化任务的表现；BBOWP关注更早的形式化阶段，即在搜索开始前判断应向优化器开放什么搜索空间，并选择与该空间和评估预算相匹配的算法，因此两者可视为端到端自动黑盒优化流程中的互补环节。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

超参数优化、分子设计和结构形状优化等任务通常无法把目标函数写成可直接求解的显式表达式，只能提交候选方案并观察目标值。在这种条件下，优化成败不仅取决于后续求解器，还高度依赖前期 formulation：是否找出真正重要的设计变量、是否为其设置合理且均衡的取值范围，以及是否在最大函数评估次数 $N_{\mathrm{max}}$ 下选择合适算法。人工完成这些工作需要较强领域知识，因此产生了利用大语言模型从自然语言任务信息中自动形成黑盒优化方案的现实需求。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **面向显式数学规划的自然语言自动建模基准**：以 NL4Opt 及后续非线性优化资源为代表，这类工作要求系统从文本中抽取变量、目标与约束，并将它们转换为线性或非线性规划等可由求解器处理的显式数学表达式。它们主要评价文本中的数学结构是否被正确恢复。
- **传统黑盒优化基准**：以 COCO 为例，这类基准提供可重复调用的黑盒目标函数，让不同优化算法在统一条件下比较性能；但任务通常只附带有限的上下文元数据，重点是算法在函数上的表现，而不是系统能否理解自然语言背景并据此设计搜索空间。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有自动建模基准假设目标和约束能够写成显式数学表达式，因而无法覆盖只能观察目标值、函数形式未知或难以计算的黑盒任务；这也意味着它们不能评价模型如何决定搜索变量、变量范围和黑盒优化算法。
- 现有黑盒优化基准缺少丰富的自然语言任务信息及与之对应的人工参考 formulation，因此难以研究大语言模型能否利用领域先验改进搜索，也缺少把“建模质量”与实际下游优化表现联系起来的统一评估条件。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前缺少一个面向黑盒优化自动 formulation 的标准化任务与可复现实验框架：输入应包含自然语言任务描述和评估预算等信息，输出应同时覆盖搜索空间与算法选择；评估则既要检查生成配置是否合理，又要通过可执行目标函数观察该配置最终能否找到高质量解。

</div>
<div markdown="1"><span>核心问题</span>

给定自然语言黑盒优化任务描述 $d$ 以及最大函数评估次数 $N_{\mathrm{max}}$，大语言模型能否推断出有效的搜索空间 $S$ 和合适的优化算法 $a$，并使这一完整方案在真实黑盒优化运行中达到可与人工设计基线比较的性能？

</div>
<div markdown="1"><span>作者直觉</span>

自然语言描述往往包含传统纯函数基准没有利用的先验，例如哪些因素可能影响结果、变量大致属于连续量还是离散选择，以及可用评估预算是紧张还是充足。大语言模型可以把这些语义线索转化为搜索决策：优先纳入关键变量、限制明显不合理的范围，并依据预算选择探索效率不同的算法。将模型输出接入可执行环境后，真实优化结果又能直接揭示这些语义判断是否真正有用，而不必只依赖字符串或公式匹配。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文将黑盒优化文字问题（BBOWP）定义为一个联合决策任务：元求解器读取自然语言描述 $d$，同时输出可执行的搜索空间 $S\in\mathcal{S}$ 与优化算法 $a\in\mathcal{A}$。描述可包含应用背景、目标性能指标、最大函数评估次数 $N_{\mathrm{max}}$ 和候选算法集合 $\mathcal{A}$，但不保证明确给出设计变量；因此，系统不仅要选择优化器，还要推断变量的数量、名称、类型及取值范围。论文限定单目标、无噪声、最小化的黑盒优化；最大化问题可通过对目标取负转为最小化。

端到端地看，元求解器先从描述中恢复可调对象及评价条件，再构造搜索空间并依据空间性质与预算选择算法，最后在不超过 $N_{\mathrm{max}}$ 次目标函数调用的条件下运行所选算法。系统质量不是由文字答案是否看似合理来判断，而是由实际优化所得的最佳目标值 $\mathcal{V}(a,S,N_{\mathrm{max}})$ 衡量；由于黑盒优化器通常具有随机性，论文以该值的期望作为联合选择搜索空间和算法的标准。直观而言，系统既要决定“允许调哪些旋钮、每个旋钮能调多大”，也要决定“用什么搜索策略调这些旋钮”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 解析自然语言任务与优化条件

元求解器识别待最小化的底层性能指标、可用评估预算与算法约束，并从可能较高层、由非专家撰写的描述中推断潜在设计变量。该设定不要求目标函数的解析形式或全部变量预先明确。

<div class="method-step__io" markdown="1">

**输入**：自然语言问题描述 $d$，其中可能包含问题背景、目标性能指标、预算 $N_{\mathrm{max}}$ 和可用算法集合 $\mathcal{A}$。<br>
**输出**：结构化的任务语义，包括优化目标、预算、候选算法以及候选设计变量信息。

</div>

**直观理解**：这一步相当于把“怎样让系统表现更好”的口头需求，翻译成“评价什么、能试多少次、可能调整什么”的优化需求清单。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造可执行搜索空间

系统确定设计变量的数量、名称、数据类型和取值范围，形成适合目标任务的搜索空间 $S\in\mathcal{S}$。该步骤需要在覆盖潜在优良方案与避免空间过大之间取得平衡。

<div class="method-step__io" markdown="1">

**输入**：从 $d$ 中提取或推断的设计变量信息，以及允许的搜索空间类别 $\mathcal{S}$。<br>
**输出**：一个可供黑盒优化器采样和评估的搜索空间 $S$。

</div>

**直观理解**：搜索空间规定优化器能尝试哪些方案；遗漏关键变量会封死改进方向，而范围过宽或变量过多又会浪费有限的评估次数。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 依据空间与预算选择优化算法

元求解器选择 $a\in\mathcal{A}$，使算法特性与搜索空间结构及预算相匹配。附录 F 的结果显示，模型会随预算改变选择倾向：小预算偏向样本效率较高的代理模型方法，大预算更偏向基于种群的进化策略。

<div class="method-step__io" markdown="1">

**输入**：搜索空间 $S$、候选算法集合 $\mathcal{A}$ 和最大评估次数 $N_{\mathrm{max}}$。<br>
**输出**：与所构造搜索空间及预算配套的优化算法 $a$。

</div>

**直观理解**：同一搜索区域在只能试 $100$ 次和可以试 $10{,}000$ 次时，适合的搜索办法可能不同；因此算法不能脱离预算单独选择。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行黑盒优化并评价联合方案

在空间 $S$ 上运行算法 $a$，每次只观察候选方案的目标值，并在预算内记录所得最佳值 $\mathcal{V}(a,S,N_{\mathrm{max}})$。考虑算法随机性时，通过重复运行所对应的期望表现评价元求解器输出。

<div class="method-step__io" markdown="1">

**输入**：算法与搜索空间组合 $(a,S)$、可执行的目标评价环境以及预算 $N_{\mathrm{max}}$。<br>
**输出**：预算内获得的最佳目标值，以及对联合 formulation $(a,S)$ 质量的实证评价。

</div>

**直观理解**：系统提交的不是最终答案本身，而是一套“搜索区域加搜索方法”；真正的检验是让它运行后，看能否在规定试验次数内找到足够好的方案。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 搜索空间与优化算法的联合选择目标

$$
(a^{*},S^{*})={\mathop{\rm argmin}\limits}_{a\in\mathcal{A},\,S\in\mathcal{S}}\;\mathbb{E}\left[\mathcal{V}(a,S,N_{\mathrm{max}})\right]
$$

**符号说明**

- $a^{*}$：在候选算法集合中期望表现最优的算法选择
- $S^{*}$：在允许的搜索空间类别中期望表现最优的搜索空间设计
- $a$：候选黑盒优化算法
- $\mathcal{A}$：问题描述给出的可用优化算法集合
- $S$：由变量数量、名称、类型和范围等定义的搜索空间
- $\mathcal{S}$：允许构造的搜索空间类别
- $N_{\mathrm{max}}$：目标函数可被调用的最大次数，即函数评估预算
- $\mathcal{V}(a,S,N_{\mathrm{max}})$：算法在给定搜索空间和预算下运行后取得的最佳目标值
- $\mathbb{E}$：针对随机优化过程取期望

<div class="equation-explanation" markdown="1">

**直观理解**：该式要求联合选择算法和搜索空间，使预算内找到的最佳目标值在平均意义下尽可能小。它强调两项决策相互依赖：即使算法本身强大，若搜索空间遗漏关键变量或范围设置不当，最终结果仍可能很差；反之，合理空间若配上不适应预算的算法，也未必能被有效搜索。<br>
**原文位置**：第 3 节“Black-Box Optimization Word Problem (BBOWP)”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该章节提出的是问题定义与基于实际优化结果的评价目标，而不是一个用于训练语言模型的损失函数；联合目标用于说明理想元求解器应最小化 $\mathbb{E}[\mathcal{V}(a,S,N_{\mathrm{max}})]$。原文所给内容未说明针对 BBOWP 对语言模型进行专门训练或参数更新，因此不能把该评价目标等同于梯度训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 元求解器**

元求解器是从描述 $d$ 映射到联合输出 $(a,S)$ 的策略，其中 $a\in\mathcal{A}$、$S\in\mathcal{S}$。原文将其研究对象表述为“为给定输入 $d$ 输出合适优化算法和搜索空间的策略”，但所给章节未规定其必须采用某种特定模型架构或训练方式。

> 直观理解：普通优化器在固定空间中寻找参数，元求解器则先决定应该搜索什么以及用什么优化器搜索，处于更高一层。

**2. 搜索空间设计模块**

该模块把未必明确列出变量的自然语言需求转换为搜索空间 $S$，核心决策包括变量数量、名称、类型与范围。搜索空间属于允许类别 $\mathcal{S}$，并须与描述 $d$ 所表达的实际黑盒任务一致。

> 直观理解：它把模糊需求变成机器可操作的“参数表”；这个参数表本身会直接决定优化器能否接触到好方案。

**3. 预算感知的算法选择模块**

该模块在候选集合 $\mathcal{A}$ 中选择算法 $a$，同时考虑搜索空间设计和函数评估预算 $N_{\mathrm{max}}$。附录 F 以 $N_{\mathrm{max}}=100$ 的 Small 设置和 $N_{\mathrm{max}}=10{,}000$ 的 Large 设置展示选择分布，并报告小预算偏向 GP、SMAC3、TPE，大预算由 CMA-ES 占主导。

> 直观理解：昂贵评价下每一次尝试都很珍贵，适合用重视样本效率的方法；预算充足时，可以让种群式方法进行更广泛的探索。

**训练与推理**

训练过程：所给章节未报告专门训练元求解器的流程，因而不能确认模型是否经过微调、提示优化或其他参数学习。推理与评价过程：向元求解器提供自然语言描述 $d$，其中含目标语义、预算 $N_{\mathrm{max}}$ 与候选算法集合 $\mathcal{A}$ 等信息；模型推断设计变量并输出搜索空间 $S$，再从 $\mathcal{A}$ 中选择算法 $a$。随后，在配套的可执行评价环境中，用 $a$ 在 $S$ 上进行至多 $N_{\mathrm{max}}$ 次函数评估，以运行期间观察到的最佳目标值 $\mathcal{V}(a,S,N_{\mathrm{max}})$ 评价输出；由于优化器一般具有随机性，概念上的比较对象是其期望值。用户可在收到 BBOWP 输出后再准备具体目标函数，这体现了该设定不要求输入阶段给出完整解析目标。

**复现信息**

公平解释该方法需要保留三项设定。第一，论文只讨论单目标、无噪声黑盒优化，并统一采用最小化方向；最大化任务通过最小化目标的负值转换。第二，函数形式对求解器不可见，优化器只能通过实际调用评价环境获得目标值，因此 $N_{\mathrm{max}}$ 是关键资源约束。第三，算法选择实验至少区分 Small 与 Large 两种预算，分别为 $N_{\mathrm{max}}=100$ 和 $N_{\mathrm{max}}=10{,}000$；附录 F 涉及 GP、SMAC3、TPE 和 CMA-ES 等算法类别，但所给章节未提供具体超参数、重复运行次数、提示模板或随机种子，复现时应查验论文其余章节与公开代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- BBOWP-Bench 共包含23个真实应用黑盒优化任务，每个实例由自然语言问题描述、可执行目标环境和人工设计的基准 formulation 组成。实验按 Easy、Intermediate、Hard 三档控制描述信息量：Easy 明示完整规范搜索空间，Hard 则要求模型从较含糊的背景描述中推断变量及其范围。Small 预算覆盖全部23个任务；Large 预算因单次评估成本过高而排除 MECHBench 的任务17和18，覆盖其余21个任务。
- YAHPO Gym 子集用于测试超参数优化场景，例如任务3和任务4；任务4要求识别支持向量机的关键变量 $cost$、$kernel$ 和 $gamma$。该子集主要检验模型是否能利用较常见的机器学习知识，在信息不完整时重建有效搜索空间；原文节选未明确报告其任务总数及数据划分。
- Olympus 与 MECHBench 子集分别代表化学实验设计和高成本机械设计等领域。Olympus 任务14涉及 $residence\_time$、$ratio$、$concentration$ 和 $temperature$；MECHBench 的任务17、18单次评估可能需要一分钟以上。它们用于检验模型面对领域特定变量、物理可行范围及昂贵目标函数时的稳健性；原文节选未报告传统训练集、验证集或测试集划分，因为这里评估的是任务级元求解能力，而非在该数据集上训练模型。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**优化运行中的最佳目标函数值**

按照模型生成的搜索空间和所选算法实际执行优化后，记录预算内观察到的最佳评价值。不同任务具有不同方向：表中的 $\uparrow$ 表示越大越好，$\downarrow$ 表示越小越好；若变量映射歧义、类型转换失败或取值越出规范设计域，则包装目标返回该任务的最差值，因此该指标同时反映 formulation 有效性与优化器搜索效果。 （依任务方向而定；最大化任务更高更好，最小化任务更低更好。不同任务的原始数值尺度不同，不应直接跨任务比较数值大小。）

</div>
<div class="metric-item" markdown="1">

**FRS**

附录I用该指标比较任务3、14和20在不同难度及提示方式下的 formulation 表现，并报告任务平均值与难度平均值。当前节选未给出 FRS 的全称、公式或严格语义，因此只能将其视为取值越接近1越好的归一化评价，不能进一步断言它具体衡量变量召回率、范围质量或最终优化收益中的哪一项。 （更高更好；表中较优结果接近1，但原文节选未明确报告其定义和边界条件。）

</div>
<div class="metric-item" markdown="1">

**采样目标值经验概率密度分布（EPDF）及其中位数**

分别从规范域和模型生成的搜索空间均匀采样100,000个点，比较所得目标函数值的分布和中位数。它将搜索空间本身的质量与具体优化算法分离：若生成空间中的随机点整体更优，说明模型把搜索范围集中到了更有潜力的区域。 （取决于任务的最大化或最小化方向；中位数朝更优目标方向移动表示生成空间质量更好。图中省略了最差目标值，因此该图不能完整显示所有无效点的比例。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Small 预算下，比较 Easy 与 Hard 描述难度在不同应用领域中的表现

<div class="result-value" markdown="1">

作者观察到明显的领域差异：Easy 条件明示规范空间时，多数模型能生成有效 formulation；Hard 条件下，YAHPO 的常见超参数优化仍较容易恢复关键变量，但 Olympus 和 MECHBench 更常出现无效或低效空间。表2中，Hard 的 Olympus 任务15有三个模型得到 $-\infty$，GPT-5.2 得到1320.79，低于人工基线2366.82；这表明含糊描述可能直接导致灾难性 formulation 失败。

</div>

模型并非普遍缺乏生成结构化搜索空间的能力，而是高度依赖先验领域知识以及描述是否提供变量线索。最差值尤其说明问题可能发生在优化开始之前，例如范围越界或变量映射错误。不过，每个空间只运行一次，因此单个有限分数的差距不能完全归因于搜索空间，也可能包含算法选择和随机搜索轨迹的影响。

<div class="result-source" markdown="1">

来源：表2，Tasks 3、4、14、15、17对应列；第5.2节 Sensitivity to Problem Domains and Difficulties

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Hard | GPT-5.2 | 0.81 | 0.95 | 0.78 | 1320.79 | -8507.17
Human Baseline | 0.91 | 0.98 | 0.20 | 2366.82 | -11740.92

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Small 与 Large 函数评估预算下的算法选择行为

<div class="result-value" markdown="1">

作者报告四个模型都表现出预算意识：Small 预算 $N_{\max}=100$ 时更偏好样本效率较高的 GP、SMAC3 和 TPE；Large 预算 $N_{\max}=10{,}000$ 时，群体式进化策略 CMA-ES 占主导。节选未给出各算法的精确选择比例。

</div>

这说明模型能把预算作为算法选择的重要条件：评估次数少时倾向利用代理模型，次数多时倾向采用需要更多采样的进化搜索。但该结果只证明选择分布符合常见经验，不等于模型在每个具体任务上都选到了性能最优的算法；正文节选也未给出反事实实验来比较同一搜索空间上的所有候选优化器。

<div class="result-source" markdown="1">

来源：附录F，Figure 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The results demonstrate strong budget awareness across all models: sample-efficient surrogate methods (GP, SMAC3, and TPE) are favored under Small budget, whereas population-based evolution strategies (CMA-ES) dominate under Large budget.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Small 预算、零样本条件下，以 FRS 比较模型在任务3、14和20上的 formulation 表现

<div class="result-value" markdown="1">

按三个任务和三档难度汇总的 Avg. (Task)，GPT-5 mini 为0.724，在四个模型中最高；Gemini 3 Flash、GPT-5.2 和 Gemini 3.1 Pro 分别为0.709、0.588和0.542。与此同时，分任务表现并不一致，例如 Gemini 3 Flash 在任务20的难度平均 FRS 为0.782，而 GPT-5 mini 为0.605，说明不存在对所有领域都占优的模型。

</div>

综合 FRS 支持 GPT-5 mini 在这三个代表任务上的平均 formulation 质量较强，但样本只覆盖任务3、14和20，不能外推为其在全部23个任务上总体最佳。由于节选缺少 FRS 的正式定义，也不能仅凭这些数值判断优势究竟来自变量识别、范围设置还是其他 formulation 因素。

<div class="result-source" markdown="1">

来源：附录I，表22，Small budget、zero-shot

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Avg. (Difficulty) | Gemini 3 Flash | 0.856 | 0.490 | 0.782 | 0.709
Avg. (Difficulty) | Gemini 3.1 Pro | 0.746 | 0.335 | 0.545 | 0.542
Avg. (Difficulty) | GPT-5 mini | 0.843 | 0.724 | 0.605 | 0.724
Avg. (Difficulty) | GPT-5.2 | 0.567 | 0.667 | 0.529 | 0.588

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 每个模型生成的搜索空间只执行一次优化，缺少重复运行、方差和显著性检验；最终最佳值混合了搜索空间质量、算法选择与随机轨迹，因而不宜把小幅差距解释为稳定的模型优劣。
- 固定可执行目标与人工别名列表提高了可控性和可复现性，但可能漏掉语义合理的新变量名，并把超出规范域的创新 formulation 判为无效；Large 预算还排除了两个昂贵任务，GP 和 SMAC3 的部分运行因超过48小时被终止，这会限制预算比较的完整性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Human Baseline：采用人工设计的搜索空间与 formulation，是判断大语言模型方案是否接近专家设计的直接参照。它不是理论最优解，也不能保证在一次随机优化运行中取得最佳值。
- Canonical domain：任务可执行环境所接受的完整规范设计域。在搜索空间质量分析中，从该域均匀采样100,000个点，并与模型生成空间的目标值分布比较，用于判断模型是否缩小到更有希望的区域，或因错误边界而降低有效样本比例。
- 四个代表性元求解器 Gemini 3 Flash、Gemini 3.1 Pro、GPT-5 mini 和 GPT-5.2 互为模型规模与推理能力对照。比较重点不是语言生成质量本身，而是其输出的 JSON 搜索空间和算法能否被执行并产生较好目标值。
- 零样本提示是主要实验条件；单样本提示在附录中作为提示策略对照。示例来自任务19，与 MuJoCo 任务20同域，因此该对照还可检验示例迁移是否依赖领域相似性。

**实验想回答的问题**

- 代表性大语言模型能否仅根据自然语言任务描述，联合设计可执行的黑盒优化搜索空间并从候选优化器中选择算法；这种能力如何随描述难度、应用领域和函数评估预算变化？
- 最终优化表现不佳时，主要原因是算法选择不合适，还是搜索空间遗漏关键变量、变量范围失衡或越出规范域；零样本与单样本提示能否缓解这些问题？

**实验实现**

每个模型接收任务说明、规定的 JSON 输出格式、自然语言问题描述和最大函数评估次数，并输出变量标识符、类型、上下界、线性或对数采样尺度，以及一个候选优化算法。候选池包括 CMA-ES、CMA-ESwM、CatCMA、CatCMAwM、DE、Nelder-Mead、PSO、基于高斯过程的贝叶斯优化、SMAC3 和 TPE。执行器使用 OptunaHub，根据生成的 JSON 在模型搜索空间中优化，再通过标识符匹配适配到规范变量；遗漏变量填入任务默认值，无关变量通常忽略，映射歧义、类型不可转换或越界则返回最差目标值。每个生成搜索空间仅运行一次优化并记录最好值，因此结果包含优化器随机性，未提供多次运行的均值、方差或显著性检验。Small 预算为 $N_{\max}=100$，Large 预算为 $N_{\max}=10{,}000$；前者覆盖23个任务，后者覆盖除 MECHBench 任务17、18外的21个任务。普通 Large 运行约需3小时，GP 或 SMAC3 的部分设置超过48小时后被终止。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 零样本与单样本提示对 Small 预算 FRS 的影响；单样本示例来自与任务20同属 MuJoCo 的任务19 | 任务20的难度平均 FRS 中，Gemini 3.1 Pro 从0.545升至0.747，GPT-5 mini 从0.605升至0.844，GPT-5.2从0.529升至0.868；Gemini 3 Flash 则从0.782降至0.728。跨领域任务并未一致受益，例如 Gemini 3.1 Pro 的任务3从0.746降至0.334。 | 该对照主要隔离“提供一个已解示例”对 formulation 的影响。结果支持同领域示例能够向多数模型传递可复用的变量或范围先验，但这种迁移并不稳定，也可能使模型过度套用示例，从而损害不同领域任务。由于提示方式与示例领域同时变化，实验不能区分收益来自一般格式示范，还是来自 MuJoCo 专门知识。 | 附录I，表23；与表22的零样本 Avg. (Difficulty) 行对照<br><span class="experiment-evidence">Avg. (Difficulty) \| Gemini 3 Flash \| 0.781 \| 0.508 \| 0.728 \| 0.672
Avg. (Difficulty) \| Gemini 3.1 Pro \| 0.334 \| 0.506 \| 0.747 \| 0.529
Avg. (Difficulty) \| GPT-5 mini \| 0.847 \| 0.696 \| 0.844 \| 0.796
Avg. (Difficulty) \| GPT-5.2 \| 0.598 \| 0.555 \| 0.868 \| 0.674</span> |
| 从规范域与模型生成空间各均匀采样100,000个点，并按描述难度和提示方式比较目标值 EPDF | 任务3在 Easy 难度下，无论零样本还是单样本，模型空间的样本中位数都优于规范域；在 Intermediate 和 Hard 难度下，模型空间的中位数即使加入单样本提示仍会恶化。任务20在 Easy 和 Intermediate 下因与示例同域而略有改善，但 Hard 条件以及任务3、14上的提示收益有限。 | 这一分析弱化了具体优化器的影响，直接测试生成搜索空间是否富集优质点。它表明模型在变量已知时可能有效缩窄范围，但在需要自行推断变量时，空间质量下降不是单纯换一个优化算法即可解决的。图中省略最差目标值，且节选没有报告中位数的具体数值，因此只能作分布方向上的定性解释。 | 附录J，Figures 8 and 9<br><span class="experiment-evidence">In both zero-shot and one-shot settings, for Task 3 in Easy difficulty, the median values of the samples from the search spaces designed by LLMs are better than those from the canonical domains.</span> |

**定性案例**

- Olympus 任务14说明“看似合理但范围过宽”会显著损害黑盒优化。规范温度域为 $[60.0,140.0]$；Gemini 3.1 Pro 生成 $[20.0,140.0]$，Gemini 3 Flash 生成 $[0.0,250.0]$。由于越出规范域的点会得到最差值，过宽范围浪费大量有限预算。作者认为 Gemini 3.1 Pro 的范围更贴近高压化学反应需要较高温度的情境，因此表现相对更好。该案例的关键不是边界必须与人工域完全一致，而是模型需要同时理解变量物理意义、可执行域和有限预算下的采样效率。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces a benchmark evaluating LLM reasoning about search-space formulation and algorithm selection for black-box optimization problems.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`32f29ab6db3291ef37b9237838665f64baf83f838890a914ca65d23b93d40835`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
