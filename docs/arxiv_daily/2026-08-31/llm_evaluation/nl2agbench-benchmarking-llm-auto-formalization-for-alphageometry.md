---
title: "[论文解读] NL2AGBench: Benchmarking LLM Auto-Formalization for AlphaGeometry"
description: "[arXiv 2608.28481][LLM 评测] 本文针对自然语言几何题到 AlphaGeometry 专用形式语言之间的转换瓶颈，提出以求解器实际执行为核心的 NL2AGBench，用于检验大语言模型能否生成语法有效且保持原题几何约束的形式化表示。"
arxiv_id: "2608.28481"
announcement_date: "2026-08-31"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:35:39.401214+00:00"
source_sha256: "cdeb05f760aeeeb76b3b7e1e6e9b51299ad34814ab118e02d741274ccdbc6fa6"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "AlphaGeometry"
  - "数学自动形式化"
  - "自然语言到形式语言翻译"
  - "神经符号推理"
  - "几何定理证明"
  - "大语言模型评测"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.28481</p>

# NL2AGBench: Benchmarking LLM Auto-Formalization for AlphaGeometry

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Samuel Xiao, Judy Song, Rory Hu, Ziliang Zong</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Valley Christian High School Fremont, CA；Affiliation: Vandegrift High School Austin, TX；Affiliation: Groton School Cupertino, CA；Affiliation: Computer Science Department Texas State University；Affiliation: Valley Christian High School；Affiliation: Vandegrift High School；Affiliation: Groton School；Affiliation: Computer Science Department；Texas State University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28481v1) · [PDF 下载](https://arxiv.org/pdf/2608.28481v1) · **关键词** AlphaGeometry, 数学自动形式化, 自然语言到形式语言翻译, 神经符号推理, 几何定理证明, 大语言模型评测<br>


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

本文针对自然语言几何题到 AlphaGeometry 专用形式语言之间的转换瓶颈，提出以求解器实际执行为核心的 NL2AGBench，用于检验大语言模型能否生成语法有效且保持原题几何约束的形式化表示。

**不用术语来说**：AlphaGeometry 虽然擅长证明奥林匹克几何题，却不能直接读取人类通常使用的英文题目；使用者必须先把点、线、相交、垂直等条件以及待证结论准确改写成严格的机器语言。这个步骤目前主要依赖人工，既费时又容易因遗漏一个条件或写错一种构造而改变题意，因此论文关心的是：大语言模型能否可靠地替人完成这道“翻译工序”，并让译文真正被 AlphaGeometry 接受和使用。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出 NL2AGBench，将英文几何题与经过验证的 AlphaGeometry 形式表示配对，并通过在 AlphaGeometry 中直接执行模型输出，建立面向几何自动形式化的标准化评测框架。
- 作者评测十个不同规模的开源与闭源大语言模型，并以语法错误和逻辑错误分类诊断失败，同时考察少样本提示、监督微调和人工提示等改进路径。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于数学自动形式化与神经符号几何定理证明的交叉领域。数学自动形式化是把自然语言描述的数学问题转换为机器可检查的符号表示；在 AlphaGeometry 中，转换结果必须符合其专用领域特定语言（DSL），随后由神经模型提出辅助构造、由符号推理引擎进行演绎证明。该流程的关键困难不只是生成表面上相似的文本，而是准确保留几何对象、位置关系、约束条件和证明目标的语义；任何遗漏或错误都可能使下游定理证明失败。NL2AGBench 因而把研究重点放在从英语几何题到 AlphaGeometry 可执行形式表示的翻译能力上，并采用在 AlphaGeometry 中直接执行的方式检验结果。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自动形式化（auto-formalization）**

自动形式化是将自然语言或非正式数学表述转换为严格的形式语言，使计算机能够解析、检查并进一步推理。对本文而言，输出必须同时满足语法要求和原几何问题的语义要求。

</div>
<div class="concept-item" markdown="1">

**神经符号定理证明**

神经符号系统结合神经网络的模式识别或候选生成能力与符号系统的严格推理能力。AlphaGeometry 中，神经模型生成可能有用的辅助几何构造，符号引擎再验证并推导几何结论。

</div>
<div class="concept-item" markdown="1">

**领域特定语言（DSL）**

DSL 是为某一类任务设计的形式语言，而不是面向所有程序的通用语言。AlphaGeometry 的 DSL 需要显式写出几何对象、对象之间的关系、已知条件和待证结论，因此自然语言问题不能直接输入定理证明器。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一份用英语书写的自然语言欧氏几何题，模型需要生成与该题对应的 AlphaGeometry DSL 表示。输入通常包含几何对象、构造关系、已知约束和目标结论；输出则是可被 AlphaGeometry 解析和执行的形式化程序。任务的隐含要求是：输出具有合法语法，并且执行后保留原题的几何语义。论文将翻译质量区分为语法正确性与可执行、语义有效性，并以 AlphaGeometry 的执行验证作为核心评估，而不是仅依据自然语言与形式文本之间的字符串相似度。研究设置覆盖不同参数规模的开源和闭源大语言模型；论文称其评估了十个模型，但所给章节未列出完整模型清单、数据划分或每道题的具体输入输出格式。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

一条输入的英语自然语言几何题。

</div>
<div class="notation-item" markdown="1">

**$y$**

模型为输入题目生成的 AlphaGeometry DSL 形式表示。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{DSL}$**

AlphaGeometry 所使用的领域特定语言，用于编码几何对象、约束、已知条件和证明目标。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{AlphaGeometry}$**

执行并验证形式化几何问题的神经符号定理证明系统；在本文中，它也是翻译结果的下游验证环境。

</div>

</div>

**直接相关的工作**

- **AlphaGeometry**: AlphaGeometry 是本文翻译任务的下游定理证明系统。相关工作将其描述为结合神经辅助构造生成与符号演绎的欧氏几何证明系统；它在三十道历史国际数学奥林匹克几何题中解决了二十五道，但要求输入采用专用 DSL，因此其强大的证明能力与自然语言输入之间仍存在形式化瓶颈。
- **Lean、Isabelle、Metamath 相关自动形式化与定理证明研究**: 这些研究说明大语言模型和形式系统可以连接自然语言数学、证明草图与机器可验证证明，但主要关注通用数学形式化或证明生成。本文的直接区别在于：它专门评测英语几何问题到 AlphaGeometry DSL 的翻译，并检查对象定义、已知条件、目标结论及几何约束是否能在 AlphaGeometry 中执行。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

神经—符号几何系统需要精确的符号输入才能启动证明，但现实中的竞赛题和教材题通常以自然语言书写。AlphaGeometry 即使具备接近顶尖竞赛选手的证明能力，其入口仍要求专用领域特定语言（DSL）；人工编码必须显式写出几何对象、关联、约束和证明目标，形成了可访问性、规模化处理和实际部署上的瓶颈。几何题还常含隐含空间关系或依赖图形的信息，微小漏译或误译便可能改变命题语义，使后续证明失败。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **人工 AlphaGeometry DSL 形式化**：由人阅读英文几何题，识别其中的点、直线、构造关系、约束和证明目标，再按照 AlphaGeometry 的严格语法逐项编码，之后交给符号证明器执行。
- **通用数学自动形式化与形式证明评测**：既有研究使用大语言模型把非形式数学转换为 Lean、Isabelle 或 Metamath 等证明助手语言，或直接评测证明生成与数学推理；这类工作主要面向通用形式语言和证明任务，而非 AlphaGeometry 特有的几何输入表示。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 人工转换成本高、扩展性弱，并且严格依赖操作者正确补全和编码全部几何关系；任何遗漏或错误构造都可能从根本上改变问题含义，导致证明器无法生成有效证明。
- 既有基准主要测量证明生成、数学推理或一般自动形式化，缺少专门针对“英文几何题到 AlphaGeometry DSL”的评测；若仅比较生成文本与参考答案的表面相似度，也不能确认输出是否可执行、是否真正保留了证明所需的几何语义。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

在本文所述研究现状下，尚无专门基准能够系统比较不同大语言模型生成 AlphaGeometry 兼容表示的能力，也缺少一种借助 AlphaGeometry 实际执行结果，同时区分语法合法性与几何约束保真度的验证机制。因此，模型在这一关键接口上的真实可用性、开源与闭源模型之间的差距以及主要失败类型仍不清楚。

</div>
<div markdown="1"><span>核心问题</span>

给定一段英文几何问题，大语言模型能否生成可由 AlphaGeometry 执行、并忠实保存原题对象、约束及证明目标的 DSL 表示；不同模型在这种能力上有何差异，其失败主要来自语法错误还是几何逻辑错误，又能否通过少样本提示、微调或人工提示得到改善？

</div>
<div markdown="1"><span>作者直觉</span>

作者选择把生成结果直接送入 AlphaGeometry，而不是只做字符串匹配，因为同一个几何含义可能存在不同但等价的写法，而表面相似的文本也可能漏掉关键约束。求解器执行相当于让目标系统亲自检查译文是否符合其语言并能进入证明流程；再将失败拆成语法与逻辑两类，则可判断模型究竟是不熟悉 DSL 规则，还是没有正确理解几何关系，从而为提示、训练或局部人工纠错提供更有针对性的方向。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

NL2AGBench将英文几何题目自动形式化为AlphaGeometry可执行的领域专用语言（DSL）。方法不是用字符串相似度判断生成结果，而是先让大语言模型（LLM）根据AlphaGeometry语法资料、人工规则和题目生成形式化表示，再由AlphaGeometry执行该表示，并依据执行结果区分成功、语法错误和逻辑错误。整体上，系统的输入是自然语言几何问题，输出是可执行的AlphaGeometry问题定义及其验证类别；直观地说，它检验的不是模型“写得像不像标准答案”，而是生成的程序能否被几何证明器正确理解并表达原题。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基准题目构建

从已形式化题目中筛选具有较丰富几何概念覆盖、且在AlphaGeometry中执行成本可控的代表性问题，保留每道题的英文陈述与经验证的DSL规格作为参照。

<div class="method-step__io" markdown="1">

**输入**：JGEX仓库中的奥林匹克风格几何题，以及AlphaGeometry项目已经人工形式化的题目。<br>
**输出**：NL2AGBench题目集合；论文报告最终选取48道题，覆盖圆、圆内接四边形、角平分线、垂心、外心、中点、反射和垂线等结构。

</div>

**直观理解**：先建立一批“有标准机器写法”的题目，这样模型生成的内容才能被客观检查，而不是只能由人凭感觉打分。筛选执行效率是为了避免某些题目因证明器运行过慢而干扰模型比较。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### LLM提示与形式化生成

令LLM执行映射$f_{\theta}(P_{NL})\rightarrow P_{AG}$，其中模型须将自然语言中的对象、几何约束和目标结论转换为AlphaGeometry DSL，并只生成包含题目标识符和DSL表示的两行结果，不输出解释或候选答案。

<div class="method-step__io" markdown="1">

**输入**：英文几何题目、官方AlphaGeometry语法定义、手写的子句使用规则和格式限制。<br>
**输出**：候选AlphaGeometry问题定义$P_{AG}$，包括几何构造子句和以问号标记的证明目标。

</div>

**直观理解**：模型相当于把“人能读懂的题目”翻译成“几何程序”。严格限制输出格式，是为了测试真实的自动接口能力，而不是让评测器替模型清理多余说明。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行式验证

将候选表示交给AlphaGeometry解析、构造几何配置并尝试处理证明目标；不依赖文本与参考翻译的逐字相似度，因为不同DSL写法可能具有相同语义。

<div class="method-step__io" markdown="1">

**输入**：LLM生成的候选DSL表示$P_{AG}$和AlphaGeometry执行引擎。<br>
**输出**：执行分类结果：被引擎接受并成功执行的Successful Translation、违反DSL语法或构造规则的Syntax Error，或语法有效但几何语义与原题不一致的Logic Error。

</div>

**直观理解**：这一步像运行自动生成的程序：能运行并正确表达问题才算成功。即使代码能解析，如果漏掉条件、关系写错或目标谓词错误，也会被归为逻辑错误。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 错误诊断与改进

将底层异常归纳为AssertionError、KeyError、ValueError等语法类别，并将遗漏约束、错误几何关系、错误目标谓词和术语误解归为逻辑错误；随后比较零样本、少样本、人工引导和监督微调条件下的可执行翻译表现。

<div class="method-step__io" markdown="1">

**输入**：失败的执行日志、生成的DSL、题目图示，以及可选的示例、人工提示或监督微调数据。<br>
**输出**：可解释的错误分布和改进后的翻译结果，用于判断失败主要来自DSL语法陌生、局部形式化失误，还是几何语义推理不足。

</div>

**直观理解**：仅报告“答对了多少题”无法说明模型为何失败。错误分类像给程序报错贴上原因标签，改进实验则分别测试增加范例、加入人类纠错，或训练模型是否能解决这些原因。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 自然语言到AlphaGeometry的形式化映射

$$
f_{\theta}(P_{NL})\rightarrow P_{AG}
$$

**符号说明**

- $f_{\theta}$：参数为$\theta$的大语言模型形式化函数
- $P_{NL}$：自然语言描述的几何问题
- $P_{AG}$：对应的AlphaGeometry DSL问题规格
- $\theta$：LLM的模型参数

<div class="equation-explanation" markdown="1">

**直观理解**：该映射规定了任务的核心输入和输出：模型读取英文几何题，生成AlphaGeometry能处理的形式化问题。它强调研究对象是翻译接口，而不是让LLM直接输出自然语言证明。<br>
**原文位置**：III-A 3 Evaluation Objective

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确给出可优化的损失函数或统一训练目标。基准评测的成功标准是生成的$P_{AG}$能否被AlphaGeometry无错误执行并形成有效问题规格；监督微调实验仅说明使用HAGeo-409中的自然语言—DSL配对训练模型，使其直接生成DSL表示，未报告具体目标函数、优化器或损失公式。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. AlphaGeometry DSL形式化接口**

DSL通过triangle、midpoint、on_line、on_circle、on_tline、circumcenter、angle_bisector等构造或关系子句描述几何对象，并通过cyclic、eqangle、perp、para等证明谓词表达目标。子句通常使用分号连接，问号分隔构造部分与证明目标；部分构造允许重复输出点以满足AlphaGeometry的参数约定。

> 直观理解：它是一套面向几何的编程语言：前半部分定义点、线和圆怎样构造，后半部分说明要证明什么。模型必须同时记住关键词、参数数量、对象顺序和标点规则。

**2. 执行式语义验证器**

AlphaGeometry不仅检查候选表示是否符合语法，还执行其几何构造与目标规格。因此评测同时覆盖语法正确性和语义正确性；语法有效但遗漏约束、误用几何关系或目标谓词不正确的结果仍会被识别为逻辑错误。对长时间无新输出的错误逻辑实例，论文说明采用五分钟终止标准并归为逻辑错误。

> 直观理解：验证器既像编译器又像问题检查器：先看“代码”能否解析，再看它是否真的描述了原题。这样可以区分“不会写这种语言”和“写得像，但把几何关系理解错了”。

**3. 提示与纠错策略**

基础提示包含官方语法、人工规则和目标题目；少样本条件额外提供自然语言题目—人工验证DSL的配对示例。人工引导采用两阶段流程：先提供题图帮助恢复共线、共圆等空间关系，再提供针对参数数量、谓词或构造错误的局部提示；监督微调则使用HAGeo-409中的自然语言—DSL配对训练较小的开源模型。

> 直观理解：这些策略分别回答三个问题：看更多标准例子能否学会语言规则，给出题图和具体报错能否修正当前答案，以及直接训练能否让模型稳定模仿形式化格式。它们不是同一种帮助，因此可以区分语法知识、视觉或几何理解和推理能力的作用。

**训练与推理**

核心基准是推理流程：给定题目和AlphaGeometry语法资料，LLM生成唯一的两行DSL翻译，然后由AlphaGeometry执行并分类。少样本推理在提示中加入54个自然语言题目—DSL配对示例；人工引导推理先让模型结合题图重新检查，再在需要时提供针对具体错误的提示。监督微调流程面向较小开源模型，使用HAGeo-409配对数据训练生成器，训练后仍通过同一执行式验证协议评测。原文未明确报告微调轮数、批大小、学习率、数据划分或具体损失。

**复现信息**

复现实验必须保留严格的两行输出格式：第一行是题目标识符，第二行是DSL定义，且不得附加解释、评论或备选翻译。评测应使用AlphaGeometry实际执行结果，而非字符串匹配；应记录AssertionError、KeyError和ValueError等异常以支持错误分类，并将语法有效但几何语义错误的结果与纯语法失败分开。论文给出的运行约束是：若逻辑错误导致执行超过五分钟且没有新输出，则终止该运行并归为逻辑错误；其余模型规模、硬件、推理参数和微调超参数原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- NL2AGBench：从 AlphaGeometry 已形式化的 $231$ 个 JGEX 几何问题中筛选 $48$ 个样本，覆盖圆、循环四边形、角平分线、垂心、外心、中点、反射和垂线等概念；同时排除在 AlphaGeometry 中运行时间或计算资源开销过高的问题。其作用是作为主要的自然语言到 AlphaGeometry DSL 翻译评测集。原文未明确报告训练集、验证集和测试集的具体划分。
- JGEX：开放源代码几何定理证明框架中的数百道奥林匹克风格几何题。论文使用其中已被 AlphaGeometry 人工形式化的 $231$ 个实例作为 NL2AGBench 的候选来源，而不是将整个 JGEX 仓库直接作为最终评测集。
- HAGeo-409：人工验证的几何问题及其 AlphaGeometry 形式化表示配对数据集，用于较小开放源代码模型的监督微调实验。原文未明确报告其训练、验证和测试划分，也未明确说明是否与 $48$ 个 NL2AGBench 评测题存在重叠。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**可执行翻译率**

生成的 AlphaGeometry 表示能够通过 AlphaGeometry 执行验证的样本比例；它同时要求输出具有可接受的语法，并且基本保留原几何问题所需的约束与目标。 （越高越好，因为更高比例表示翻译结果可以直接交给下游定理证明器，而不只是看起来像 DSL。）

</div>
<div class="metric-item" markdown="1">

**语法正确性**

输出是否符合 AlphaGeometry DSL 的形式语法，例如对象定义、关系表示和目标表达是否能被解析；它主要检测格式和语言规则，不足以单独证明几何语义正确。 （越高越好，因为语法错误会阻止执行；但即使该指标较高，仍可能存在语义错误。）

</div>
<div class="metric-item" markdown="1">

**错误类型统计**

将 AlphaGeometry 翻译执行失败归类为语法错误或逻辑错误。语法错误指输出无法按 DSL 规则解析，逻辑错误指语法表面可接受但遗漏、改变或错误表达了几何约束。 （不存在简单的统一高低方向；理想情况是两类错误数量或比例都降低。该分析用于诊断失败原因，而不是直接替代翻译准确率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 开放源代码与闭源 LLM 的总体比较

<div class="result-value" markdown="1">

作者报告闭源前沿模型与开放源代码模型之间存在显著性能差距；领先闭源模型的可执行翻译率超过 $80\%$，而最大的开放源代码模型仍难以稳定保留几何约束并生成有效形式化。

</div>

这表明将几何英语转换成可执行 DSL 不只是一般语言翻译或数学答题能力的问题，还要求准确识别对象、关系和目标并保持约束。该结果支持“闭源模型整体更强”的作者结论，但不能据此证明所有闭源模型都优于所有开放源代码模型，因为原文节选没有给出逐模型数值、置信区间或模型名称。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

While leading closed-source models achieve executable translation rates exceeding 80%, even the largest open-source models struggle to consistently preserve geometric constraints and produce valid formalizations.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 基于 AlphaGeometry 执行验证的评测与错误分析

<div class="result-value" markdown="1">

论文采用执行式验证，而非仅比较文本相似度，并将失败划分为语法错误和逻辑错误；因此评测同时关注输出能否运行以及其是否保留几何语义。

</div>

这一设计能区分“格式写错”和“格式正确但几何含义写错”两种失败。它比字符串匹配更接近实际部署需求，但执行成功本身仍不等于已经证明原题结论；该评测首先验证翻译表示是否可被系统接受和使用。原文未明确报告两类错误的具体比例或各模型的完整错误矩阵。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

NL2AGBench evaluates translation quality using execution-based verification within the AlphaGeometry framework rather than relying solely on textual similarity metrics.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 缓解策略比较

<div class="result-value" markdown="1">

作者报告少样本提示、监督微调和人工引导提示均能在多个模型家族上带来可测量改进；结论部分进一步称少样本提示最具可扩展性且效果最稳定，人工纠正显示部分失败来自局部歧义，而非完全缺乏几何推理能力。

</div>

提示中加入示例可能同时帮助模型学习 DSL 结构和对齐几何表达，人工提示则说明某些错误可以通过澄清局部信息修复。监督微调虽然改善语法遵循，却未必充分解决几何语义推理；因此这些策略改善的是翻译可靠性，而不是已经证明模型获得了普遍的几何定理证明能力。

<div class="result-source" markdown="1">

来源：Section VI, Conclusion and Future Work

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Among these approaches, few-shot prompting is the most scalable and consistently effective strategy, while human-guided correction demonstrates that some translation failures arise from localized ambiguities rather than a complete lack of geometric reasoning capability.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评测规模和覆盖范围有限：最终仅选取 $48$ 个问题，且来自 AlphaGeometry 已人工形式化的 JGEX 子集；原文未明确报告数据划分和与 HAGeo-409 的重叠控制，因此对更广泛几何题或分布外题目的泛化能力仍不清楚。
- 实验报告信息不完整：所给章节未提供十个模型的具体名称、逐模型分数、完整表格、提示模板、解码设置和统计显著性；因此闭源—开放源代码差距及各缓解策略的相对收益需要根据原始实验表进一步核验。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 十个不同参数规模的开放源代码和闭源 LLM：这是主要模型比较基线，用来衡量模型家族、参数规模和模型开放性对 AlphaGeometry 自动形式化能力的影响；原文节选未列出十个模型的具体名称、版本或参数量。
- 少样本提示：作为提示增强比较条件，用于检验向模型提供示例形式化是否能改善 DSL 遵循和语义保持；它不是独立模型，而是与基础提示条件的对照。
- 监督微调模型：使用 HAGeo-409 训练后生成 DSL，作为比较模型是否能通过目标领域数据学习 AlphaGeometry 表面语法与翻译模式的条件。
- 人工引导提示：向模型提供人类提示或局部纠正，用于检验错误是否可通过澄清局部歧义来修复；原文未明确报告统一的人工提示协议或对应的独立基线模型。

**实验想回答的问题**

- 不同规模、不同来源的开放源代码与闭源大型语言模型，能否将英文几何题稳定翻译为可被 AlphaGeometry 执行的形式化表示？
- 少样本提示、监督微调和人工引导提示能否减少语法错误与逻辑错误，并提高可执行翻译率？

**实验实现**

评测流程以英文几何题为输入，让各 LLM 输出 AlphaGeometry 兼容的 DSL 表示，再将输出直接送入 AlphaGeometry 执行验证，并记录可执行翻译率、语法正确性及失败类型。该协议避免仅用字符串相似度判断，因为不同形式化表达可能文本不同但语义可执行。实验覆盖开放源代码和闭源模型，并比较多种参数规模；此外分别测试少样本提示、HAGeo-409 监督微调和人工引导提示。原文节选未明确报告完整提示模板、解码参数、重复采样次数、随机种子、硬件、统计显著性、各模型名称及每个实验条件的详细样本数。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 监督微调（HAGeo-409）相对于直接生成 | 微调改善了 AlphaGeometry 语法遵循并减少若干语法相关错误，但可执行翻译准确率的提升有限。 | 该对照主要隔离目标领域示例训练的作用：模型更会写出形式上像 DSL 的结果，却不一定能正确解释几何关系。因此它说明语法模仿与完整语义形式化之间仍有差距，而不是说明微调完全无效。 | Section V，Fine-tuning experiment<br><span class="experiment-evidence">Fine-tuning improves adherence to AlphaGeometry syntax and reduces several categories of grammar-related errors. However, improvements in executable translation accuracy remain limited.</span> |
| 少样本提示、监督微调与人工引导提示的策略比较 | 三种策略均被报告为在多个模型家族上带来可测量改进，其中少样本提示被作者评价为最具可扩展性且效果最稳定；原文未明确报告每种策略的具体数值增益。 | 该比较检验改进究竟来自示例、参数更新还是人类提供的局部信息。少样本提示在无需重新训练和大量人工干预的情况下改善表现，因此更适合规模化使用；但由于缺少逐条件数值和统一成本报告，不能精确判断其相对优势大小。 | Abstract<br><span class="experiment-evidence">We further investigate mitigation strategies, including few-shot prompting, fine-tuning, and human-guided hinting, demonstrating measurable improvements across multiple model families.</span> |

**定性案例**

- 定性检查发现，一些微调模型能够生成语法上看似合理、但几何构造语义错误的 DSL；论文据此认为较小模型的主要瓶颈不只是熟悉 DSL，还包括不足的几何推理能力。该案例说明“语法正确”不能替代“约束正确”，但原文未提供具体题目、模型输出或逐步纠错示例。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：构建执行验证的几何自动形式化基准，并评测 LLM 将自然语言数学问题转换为 AlphaGeometry DSL 的能力。; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`cdeb05f760aeeeb76b3b7e1e6e9b51299ad34814ab118e02d741274ccdbc6fa6`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
