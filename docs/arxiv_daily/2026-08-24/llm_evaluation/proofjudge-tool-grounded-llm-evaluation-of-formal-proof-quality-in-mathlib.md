---
title: "[论文解读] ProofJudge: Tool-Grounded LLM Evaluation of Formal Proof Quality in Mathlib"
description: "[arXiv 2608.20432][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.20432"
announcement_date: "2026-08-24"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-25T01:57:23.473158+00:00"
source_sha256: "ba466c05a6adb1c489b84a3fa69191d5e22d8f0b5d13137da7c1f1cf911da7ef"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "Lean 4"
  - "Mathlib"
  - "形式化证明质量"
  - "大语言模型评审"
  - "工具增强评估"
  - "代码审查"
  - "可验证奖励强化学习"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.20432</p>

# ProofJudge: Tool-Grounded LLM Evaluation of Formal Proof Quality in Mathlib

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Shane Caldwell</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.20432) · [PDF 下载](https://arxiv.org/pdf/2608.20432) · **关键词** Lean 4, Mathlib, 形式化证明质量, 大语言模型评审, 工具增强评估, 代码审查, 可验证奖励强化学习<br>
**代码**: [https://github.com/SJCaldwell/ProofJudge](https://github.com/SJCaldwell/ProofJudge)

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

Lean 4 是一种带有可信内核的交互式定理证明器：形式化证明只有通过内核类型检查，才能被认定为逻辑正确。Mathlib 是规模最大的 Lean 4 数学库之一，其贡献除正确性外还需经过人工代码审查，以保证证明能够恰当复用现有库、合理使用自动化、保持清晰结构，并遵循命题设计与命名等工程规范。随着可验证奖励强化学习利用类型检查结果训练语言模型，自动生成正确证明的成本不断下降，但“能够通过检查”并不等于“适合进入长期维护的数学库”；ProofJudge 所处的研究领域正是对形式化证明进行超越二元正确性的质量评价。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**Lean 4 内核与类型检查**

Lean 4 将定理陈述视为类型、将证明视为该类型的项，并由一个较小的可信内核检查证明是否成立。通过类型检查只能保证形式逻辑意义上的正确性，不能保证证明结构清晰、易维护或具有复用价值。

</div>
<div class="concept-item" markdown="1">

**Mathlib 与代码审查**

Mathlib 是 Lean 4 的大型数学定义与定理库，新贡献通常通过拉取请求提交，并由熟悉库规范的审查者修改和筛选。审查不仅检查正确性，还关注策略使用、命题一般性、证明分解、命名惯例以及是否形成可供后续证明复用的接口。

</div>
<div class="concept-item" markdown="1">

**可验证奖励强化学习**

可验证奖励强化学习使用能够自动核验的结果作为训练奖励；在形式化数学中，Lean 类型检查器可直接判断候选证明是否正确。其优势是奖励可靠且可扩展，但单纯以“是否通过检查”为奖励，无法区分不同正确证明在工程与数学表达上的质量差异。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文研究的任务是评价已经能够通过 Lean 4 内核检查的形式化证明质量，而不是再次判断其逻辑正确性。评价对象来自不同 Mathlib 拉取请求中的声明，每个样本包含最初因质量问题被要求修改的版本，以及最终被 Mathlib 接受的版本；评审代理还可访问该拉取请求所对应提交上的库状态并调用工具查询上下文。系统需要沿五个维度给出质量判断：现有库利用程度、自动化方法的适配性、证明结构清晰度、命题陈述质量和 Mathlib 规范符合度。论文把最终接受版本获得高于初始版本的评价视为与人类审查偏好一致；这一设定默认 Mathlib 审查过程体现了目标库的质量标准，因此衡量的是对该审查偏好的恢复能力，而非证明质量的绝对、跨库通用真值。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **可验证奖励强化学习（原文文献[2]）**: 该方向利用 Lean 4 类型检查器提供可自动验证的奖励，推动语言模型形式化证明能力提升；ProofJudge 针对其二元正确性奖励无法反映证明结构、复用性和库规范的问题，补充质量层面的评价信号。
- **语言模型辅助或自主形式化证明（原文文献[3]、[4]）**: 这些工作表明语言模型可以在人机协作或自主设置下生成更多形式化证明；ProofJudge 关注随生成规模扩大而出现的下游瓶颈，即如何自动承担部分原本依赖资深 Mathlib 维护者的质量审查工作。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

Lean 4 的内核类型检查只能确认形式证明在逻辑上正确，不能判断证明是否易懂、是否合理利用 Mathlib 现有库、是否适合使用自动化工具，或是否符合 Mathlib 的代码规范。因而，Mathlib 维护者仍需人工审阅证明质量；随着形式化数学库和贡献数量增长，这会造成持续的审查负担。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **Lean 内核类型检查**：系统验证证明项是否满足 Lean 的类型规则；通过检查意味着证明在形式逻辑上正确，但该机制不评价证明的可读性、结构、库复用程度或风格规范。
- **Mathlib 维护者人工审查**：维护者比较贡献者提交的证明与修改后的版本，综合判断证明是否符合库的长期维护要求；这一过程能够评价质量，但依赖专家时间，难以低成本、规模化地应用。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 仅依赖内核检查会把“逻辑正确”误当成“高质量证明”，因此无法识别虽然能通过检查、但结构晦涩、自动化使用不当或重复实现已有库结果的证明。
- 人工审查能够覆盖更丰富的质量标准，却需要 Mathlib 专家的判断和时间；现有做法缺少一种能够查询对应库状态、并以人类审查偏好为参照进行规模化评价的自动评估机制。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚未解决的关键缺口是：能否构建一个由大语言模型驱动、能够访问提交所对应 Mathlib 版本的工具增强评审器，在证明已经通过内核检查之外，可靠评价其库复用、自动化适配、结构清晰度、陈述质量和 Mathlib 规范符合度，并恢复维护者对“初始版本”与“最终接收版本”的偏好？

</div>
<div markdown="1"><span>核心问题</span>

工具接地的大语言模型评审器能否在五个非正确性维度上评价 Lean 4 形式证明质量，并以显著高于随机猜测的准确度识别 Mathlib 维护者最终接受的证明版本？

</div>
<div markdown="1"><span>作者直觉</span>

证明质量并非完全不可观察：维护者的修改和接收决定包含了对可读性、库复用和规范性的综合判断，而 Mathlib 的具体库状态又决定了哪些定理、引理和自动化工具可被合理使用。让评审模型直接查询与 Pull Request 对应的提交，可以减少脱离实际库环境的猜测；再用维护者接受的版本作为偏好参照，便能把这些通常依赖专家经验的判断转化为可检验的评估任务。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ProofJudge 是一个带工具调用能力的智能体式评审系统，用于评价 Mathlib 中形式化证明的库级质量，而不只检查证明是否通过 Lean 编译。系统以 Lean 内核提供的客观正确性为基础，同时由大语言模型依据 Mathlib 的代码审查规范，从库复用、自动化适配、结构清晰度、陈述质量和 Mathlib 惯例五个维度独立评分，再由评审框架加权得到最终分数；评审过程中，模型可以通过 bash 查询实际的 Mathlib 库状态，以便将判断建立在现有库内容之上。数据方面，作者从 Mathlib 拉取请求中构造了包含早期版本与最终版本的声明对数据集，并使用一个开发集调节评分标准、使用测试集进行评估。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造声明版本对数据集

使用 claude-sonnet-5 检查过去的拉取请求，筛选出早期版本与最终版本存在显著差异、且差异不只是 linting，也不涉及新增声明的案例，并将两种版本组成声明对。

<div class="method-step__io" markdown="1">

**输入**：Mathlib 的历史拉取请求及其中声明的最早版本和最终版本。<br>
**输出**：一个包含 218 对声明的测试集，以及一个包含 123 对声明的开发集；开发集用于调节 rubric，测试集用于最终评估。

</div>

**直观理解**：可以把它理解为收集同一段形式化代码的“修改前”和“修改后”版本，重点保留真正涉及证明或陈述质量变化的案例，而不是只改格式的案例。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 检查形式正确性并提供库上下文

以 Lean 内核的编译或检查结果作为证明正确性的客观锚点；同时允许 ProofJudge 通过 bash 查询 Mathlib，从现有库中检索相关定义、定理和惯用写法。

<div class="method-step__io" markdown="1">

**输入**：待评价的形式化证明声明对，以及 Lean 和 Mathlib 环境。<br>
**输出**：证明是否满足形式系统正确性的基础信息，以及供语言模型判断库级质量的实际 Mathlib 上下文。

</div>

**直观理解**：Lean 负责回答“这段证明在逻辑上是否成立”，工具查询则帮助评审者回答“它是否使用了库中已有的合适资源、是否符合现有写法”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按质量 rubric 分解评审

评审智能体依据面向 Mathlib 库收录标准设计的 rubric，对五个质量维度分别以 1 到 10 分评分：library leverage、automation fit、structural clarity、statement quality 和 Mathlib conventions。

<div class="method-step__io" markdown="1">

**输入**：证明的形式正确性信息、声明对内容和通过工具查询获得的 Mathlib 上下文。<br>
**输出**：五个相互独立的维度分数及其对应的分解式评审判断。

</div>

**直观理解**：系统不把“质量”压缩成一个模糊印象，而是要求评审者分别评价是否善用已有库、自动化是否合适、结构是否清楚、定理陈述是否良好以及是否遵循 Mathlib 惯例。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 聚合最终质量分数

由评审框架按照预设权重对五个维度分数进行加权，形成最终评审分数；具体权重在所给章节中未明确报告。

<div class="method-step__io" markdown="1">

**输入**：五个质量维度的 1 到 10 分评分。<br>
**输出**：一个综合反映形式证明库级质量的最终分数。

</div>

**直观理解**：这一步类似把五位侧重不同问题的评审意见按规定比例合成为总评，但总分仍然建立在前面分项评分之上，而不是替代分项信息。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：所给方法章节没有报告可优化的参数化训练目标、损失函数或梯度更新过程。ProofJudge 的主要开发活动是使用 123 对声明的开发集调节 rubric；章节未明确说明这是通过模型微调、提示词搜索、权重搜索还是其他优化方式完成的，因此不能将其解释为语言模型训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Lean 内核正确性锚点**

Lean kernel 提供形式化证明的客观正确性检查，ProofJudge 将其作为区别于主观质量评价的基础约束。该机制回答的是证明能否被形式系统接受，而非证明是否适合长期维护或纳入 Mathlib。

> 直观理解：它像一个不能被语言模型意见取代的自动裁判：只要内核不接受，证明就不能仅凭“写得漂亮”获得正确性认可。

**2. 工具接地的评审智能体**

ProofJudge 是一个可以使用 bash 查询 Mathlib 的 agentic judge。工具访问使模型能够查看库的实际状态，并像人类审阅者一样基于现有定义、定理和代码惯例评价证明，而不是只根据输入文本猜测。

> 直观理解：普通评审可能只读眼前的证明；该模块允许评审者先查阅图书馆已有内容，再判断作者是否重复造轮子、是否错过合适的自动化或是否偏离常见写法。

**3. 五维 rubric 与加权聚合器**

rubric 要求模型分别评估 library leverage、automation fit、structural clarity、statement quality 和 Mathlib conventions，每项使用 1 到 10 分尺度；harness 再对这些分数进行加权，得到最终分数。所给章节未给出各维度的具体权重或聚合公式。

> 直观理解：该模块把“证明质量”拆成五个可检查的问题，既保留细粒度反馈，也能产生一个便于比较的总分；不过没有公开权重时，总分的相对侧重点仍需查阅论文其他章节。

**训练与推理**

按照所给信息，系统的核心流程发生在推理或评审阶段：输入 Mathlib 中的声明对及其 Lean 环境后，先获得 Lean 内核的正确性检查结果，再由可查询 Mathlib 的评审智能体收集库上下文，随后对五个质量维度分别打分，最后由 harness 加权生成综合分数。数据构造阶段使用 claude-sonnet-5 筛选历史拉取请求中的声明对；123 对开发集用于调节 rubric，218 对测试集用于评估 ProofJudge，但所给章节没有说明筛选模型或 ProofJudge 是否经过参数训练。

**复现信息**

复现或公平解读所必需的信息包括：数据来自 Mathlib 拉取请求；样本是最早版本与最终版本的声明对；排除了仅涉及 linting 的变化和新增声明；评审智能体可通过 bash 查询 Mathlib；五个维度均采用 1 到 10 分制；最终分数由 harness 加权得到。所给章节未明确报告 Lean、Mathlib 和 bash 的具体版本，未明确报告五个维度的权重、提示词、上下文截断策略、工具调用次数、聚合公式，以及开发集调节 rubric 的具体程序。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Mathlib 拉取请求中的成对证明修订：每一对包含被拒绝的前修订证明和最终被 Mathlib 接受的后修订证明；实验使用 218 对测试集样本，角色是检验评审器能否恢复人工审查者的偏好。
- 同一 218 对测试集的三次独立重复运行：每个评审器在每一对样本上进行三次评审，用于估计重复运行造成的不确定性和判断翻转情况。
- 代表性案例 PR 11640：涉及 `Set.restrictPreimage_isClosedMap` 的初始证明与合并后的替代证明，用于定性展示工具检索如何帮助评审器识别重复已有库结果的问题。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Alignment %（偏好对齐率）**

评审器给后修订证明更高分的比例；后修订是被 Mathlib 接受的版本，前修订是被拒绝的版本，因此该指标近似衡量模型能否重现审查者对证明质量的相对判断。 （越高越好，因为更高表示评审器更频繁地把被接受的证明排在被拒绝的证明之前。）

</div>
<div class="metric-item" markdown="1">

**95% CI（95%置信区间）**

基于声明与重复运行的聚类自助法计算的不确定性区间，用于表示对齐率估计的波动范围，而不是额外的准确率指标。 （区间越窄通常表示估计越稳定；区间位置越高表示总体表现越好，二者需要分别解读。）

</div>
<div class="metric-item" markdown="1">

**USD/pair（每对样本成本）**

按照公开价格和实际 token 数量计算的每一对前后修订证明的评审成本，用于比较模型效果与推理费用之间的权衡。 （在达到相近对齐率时越低越好；低成本本身不代表评审质量更高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 六个评审器在 218 对测试集上的总体性能

<div class="result-value" markdown="1">

所有评审器的对齐率均显著高于 50% 随机机会基线；最高为 `claude-sonnet-5` 的 80.8%，最低为 `deepseek-v4-flash` 的 63.5%，原文称各模型的符号检验均满足 $p<10^{-5}$。

</div>

这说明工具增强的模型通常能够从前后两个证明版本中识别出与 Mathlib 接受决定相关的质量差异，而不是完全随机地选择一个版本。但该实验只证明模型能恢复这组人工审查结果，不能证明模型已经准确掌握了所有数学证明质量标准，也不能证明其判断在 Mathlib 之外同样有效。

<div class="result-source" markdown="1">

来源：Section 0.3 Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Every judge recovers the reviewers’ preference far above chance, from claude-sonnet-5 at 80.8% of declarations down to deepseek-v4-flash at 63.5%, each at p<10^{-5} by sign test.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 开放权重模型与闭源模型的比较

<div class="result-value" markdown="1">

两个开放权重评审器 `muse-glimmer-30b` 和 `inkling-small` 的对齐率分别为 70.2% 和 69.3%；它们低于最高的闭源模型 80.8%，但仍明显高于随机基线。

</div>

结果表明，进行这类 Mathlib 证明评审并不只依赖最前沿的闭源模型，开放权重模型也能提取一部分与人工审查相符的信号。由于实验只报告了 3 个开放权重和 3 个闭源模型，且模型架构、训练数据与工具配置可能不同，因此不能把性能差异单独归因于“开放权重”这一属性。

<div class="result-source" markdown="1">

来源：Section 0.3 Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Reviewing Mathlib PRs this way is not limited to frontier models. Two open-weight judges, muse-glimmer-30b and inkling-small, sit at 70.2% and 69.3%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 准确性与重复运行稳定性的关系

<div class="result-value" markdown="1">

同一评审器重复处理相同声明时，判断可能发生明显翻转；原文称翻转比例从约五分之一到接近一半，并举例说明同一消融在不同重复运行中得到 $p=0.34$ 和 $p=0.006$。

</div>

这说明单次运行的对齐率或显著性可能不可靠，模型的随机性会改变结论。重复运行与聚类区间因此是必要的评估设计。不过，原文未明确给出每个评审器各自的翻转率，也未说明这些翻转是否主要由模型采样、工具搜索路径还是其他因素造成。

<div class="result-source" markdown="1">

来源：Section 0.3 Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Re-running one over the same declarations flips between a fifth and nearly half of its verdicts, and a single run’s interval hides that badly: the same ablation returns p=0.34 on one replicate and p=0.006 on another.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评估目标是前后修订之间是否与审查者偏好对齐，而不是独立验证证明的数学质量；因此较高对齐率可能反映模型学习了 Mathlib 审查习惯，不能直接推出模型能够发现所有错误、冗余或不可维护的证明。
- 测试规模仅明确报告为 218 对 Mathlib 修订，模型数量也为 6 个；原文未明确报告跨项目、跨证明助手或跨领域的外部测试，因此结果的普适性仍有限。重复运行显示较高噪声，也削弱了单次评审结论的可靠性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 50% 随机机会基线：在前修订和后修订之间随机偏好时，理论上的对齐率为 50%；它检验模型是否真正学到了与人工审查相关的质量信号，而不是仅凭随机选择获得结果。

**实验想回答的问题**

- 工具增强的大语言模型评审器能否识别 Mathlib 拉取请求中被接受的后修订证明，并使其评分高于被拒绝的前修订证明？
- 不同模型规模与开放权重状态下的评审器表现如何，其准确性、成本和重复运行稳定性之间存在什么关系？

**实验实现**

每个评审器分别处理每个拉取请求修订，不知道同一对中另一版本的得分，也不知道其他修订正在被评审，从而避免直接比较分数或跨样本信息泄漏。评审器可以调用工具最多 20 次，之后必须作出判断，以限制推理成本。实验比较 6 个评审器，其中 3 个开放权重、3 个闭源模型；每个评审器在 218 对测试样本上运行 3 次。对齐率与 50% 随机机会基线比较，并使用符号检验报告显著性；区间采用按声明和重复运行聚类的自助法。原文未明确报告完整提示词、工具类型清单、硬件配置或每次评审的平均工具调用次数。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 在 PR 11640 中，初始证明重新构造了 Mathlib 已经提供的 `Set.restrictPreimage_isClosedMap` 结果；合并版本改为一行调用 `H.restrictPreimage`。评审器搜索仓库、引用已有声明的签名，并在“library leverage”（复用已有库成果）维度降低初始版本的得分；原文称每个评审器在每次运行中都降低了初始版本的得分。该案例说明工具访问不仅能检查语法或正则模式，还能帮助模型发现语义上重复已有库结果的问题，但单个案例不能代表所有证明质量维度。
- 原文证据："In PR 11640, the initial proof of Set.restrictPreimage_isClosedMap reconstructed a result that Mathlib already provided."；来源：Section 0.3.1 An Example Grading。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces tool-grounded evaluation of LLM-generated formal proofs in Mathlib, centrally addressing both evaluation and mathematical reasoning.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`ba466c05a6adb1c489b84a3fa69191d5e22d8f0b5d13137da7c1f1cf911da7ef`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
