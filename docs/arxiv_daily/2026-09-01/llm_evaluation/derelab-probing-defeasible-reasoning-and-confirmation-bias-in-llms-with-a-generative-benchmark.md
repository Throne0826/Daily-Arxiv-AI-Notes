---
title: "[论文解读] DERELAB: Probing Defeasible Reasoning and Confirmation Bias in LLMs with a Generative Benchmark"
description: "[arXiv 2608.30413][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.30413"
announcement_date: "2026-09-01"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:30:16.720024+00:00"
source_sha256: "6866fe8aab00566b33984af72437d5dc3df90bb1939e14f99f7ed31586cba0a6"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "可废止推理"
  - "非单调推理"
  - "默认推理"
  - "继承推理"
  - "信念更新"
  - "确认偏误"
  - "大语言模型"
  - "生成式基准"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.30413</p>

# DERELAB: Probing Defeasible Reasoning and Confirmation Bias in LLMs with a Generative Benchmark

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Jayanta Sadhu, Sayem Shahad, Kenneth Marino</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of Utah；Affiliation: Bangladesh University of Engineering and Technology</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30413v1) · [PDF 下载](https://arxiv.org/pdf/2608.30413v1) · **关键词** 可废止推理, 非单调推理, 默认推理, 继承推理, 信念更新, 确认偏误, 大语言模型, 生成式基准<br>
**代码**: [https://github.com/Jayanta47/DeReLab](https://github.com/Jayanta47/DeReLab)

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

本文研究大语言模型在可废止推理中的表现。现实信息通常不完整且会持续更新，因此基于当前证据得到的合理结论不一定永久成立；新证据可能支持原结论，也可能迫使系统撤回原结论。这类过程属于非单调推理：加入信息后，可接受的结论可能减少，而不是像经典单调逻辑那样只能保留或增加。论文关注其中两种典型范式——默认推理与继承推理，并将其组织为多轮信念更新对话，以检验模型能否随证据变化正确修订判断，以及是否会表现出偏好一致证据、抵制不一致证据的确认偏误。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**可废止推理**

依据当前不完整但合理的证据作出暂时性推断，并允许在出现新证据时撤回该推断。例如，由“一般鸟会飞”可暂时判断某只鸟会飞，但知道它是企鹅后应撤回结论。

</div>
<div class="concept-item" markdown="1">

**默认推理与继承推理**

默认推理是在没有反例时采用通常成立的规则；继承推理则让个体或子类继承上位类别的属性，同时允许更具体的信息覆盖一般属性。两者都可能因例外或来源优先级而发生结论逆转。

</div>
<div class="concept-item" markdown="1">

**确认偏误**

确认偏误是更容易接受支持既有判断的证据、却抵制与既有判断冲突的证据的倾向。本文将其操作化为比较模型面对确认性更新与否定性更新时的信念修订行为。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

DeReLab把参数化图结构转换成多轮信念更新对话：系统先提供事实、默认规则或类别继承关系，使模型对某个假设作出判断；随后逐轮加入可能确认或削弱该假设的新信息，要求模型在每一轮更新结论。生成器覆盖默认推理和继承推理，并通过形式化验证为每一轮生成标准答案；属性链长度、分支因子、干扰信息密度和信息源优先级等参数可控制推理类型与难度。该设置假定结论应由当前轮次累积的信息及规则决定，输出则是模型对目标假设在各轮中的判断或信念更新结果。与只给出一次性问题的静态数据集不同，这一设置同时测试模型是否理解新证据的作用、是否真正撤回已被击败的结论，以及确认性和否定性证据是否造成系统性不对称。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Rudinger et al. (2020)**: 该工作构建了早期的自然语言可废止推理数据集，并通过附加信息改变原有推断，是本文多轮更新任务的重要前序工作；但其评测依赖静态数据，不能像 DeReLab 一样按参数持续生成带逐轮形式化真值的实例。
- **Allaway and McKeown (2025)**: 该工作围绕泛称、实例化和继承属性构建可废止推理数据集，为本文的继承推理类别提供直接背景；本文进一步将默认推理与继承推理纳入统一生成框架，并支持可控难度和增量证据更新。

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

DeReLab不是一个固定题库，而是一套可按参数持续生成可废止推理对话的评测框架。其输入是推理范式、图拓扑与难度参数，包括默认规则链的长度、对象数、干扰项密度和击败边稀疏度，以及继承层级的深度、分支因子和阻断位置；框架先生成带正负边的知识图，再用无现实语义的伪词实体和领域一致的属性填充节点，将图中事实按指定顺序逐轮披露。每轮累积前提后，路径解析器依据支持、击败、优先级、特异性抢占和怀疑式推理，自动给目标假设产生$\{\mathrm{yes},\mathrm{no},\mathrm{unknown}\}$标签；默认推理还产生更新效果标签$\{\mathrm{strengthening},\mathrm{weakening},\mathrm{no\ effect}\}$。最终输出是具有逐轮形式化真值、可控难度和已知更新作用的多轮对话，可直接用于评测模型是否在新证据到来时正确修改结论。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 参数化推理图生成

生成由实体节点和属性节点构成的有向图，并加入事实属性边、可废止的正属性边、可废止的负属性边及目标假设边。默认推理形成属性主链并可加入多来源优先级、旁路和无关属性；继承推理形成线性或分支分类层级，并在特定节点注入局部阻断。

<div class="method-step__io" markdown="1">

**输入**：推理类型与生成配置：默认推理、线性继承或树形继承，以及链深、层级深度、分支因子、对象数、干扰项密度、稀疏因子和假设数量等参数。<br>
**输出**：一个结构难度已知、包含目标查询和潜在支持或击败路径的抽象推理图。

</div>

**直观理解**：这一步相当于先画出题目的“逻辑电路图”，再精确控制电路有多长、分支有多少以及哪里会断路。难度来自推理结构本身，而不只是换一种句子表述。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 实体、属性与自然语言实例化

用可发音但语义为空的伪词填充实体，并从领域匹配的属性池中抽取属性值，再通过单数或复数谓词模板把节点和边转写为语法完整的陈述。无关更新使用与主推理链距离较远、且不位于通向假设的推理路径上的属性。

<div class="method-step__io" markdown="1">

**输入**：抽象图中的实体节点、属性节点、边类型，以及选定的语义领域和语言模板。<br>
**输出**：不依赖模型既有世界知识、但语言表面连贯的前提、规则、实体事实和更新语句。

</div>

**直观理解**：例如实体名“Kitylu”本身不暗示任何事实，模型不能靠记住“企鹅不会飞”一类常识猜答案。它必须只根据当前对话中给出的规则完成推理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 逐轮对话编排与更新控制

先给出背景规则和实体实例，再提出假设，随后每轮只披露一个新事实并重复询问蕴含状态；默认推理还询问该更新增强、削弱还是不影响假设支持。披露顺序可独立配置，因此可以刻意构造先击败后恢复、相关证据与干扰证据交错，或高优先级来源越过先前击败的轨迹。

<div class="method-step__io" markdown="1">

**输入**：已实例化的推理图、边的披露顺序、目标假设，以及可选的来源及其优先级。<br>
**输出**：一组前提随轮次单调累积、但结论允许非单调变化的多轮信念更新对话。

</div>

**直观理解**：框架不是把全部信息一次给完，而是像持续收到新证据一样逐条展示。这样可以观察模型究竟在哪一次更新后应当改口、何时应当保持原判断。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 路径解析、逐轮标注与偏差条件归类

解析器先保留从$x$经正边可达且仍能通向$y$的相关子图，再按拓扑次序传播支持和击败状态；实体上的直接证据优先，更具体来源抢占更一般来源，无法按特异性消解的对称冲突判为未知。随后依据模型自己的上一轮回答与当前更新的真实效果，将轮次归入C1至C5，并用C1与C2的正确率差和优势比衡量支持性与反驳性更新之间的不对称。

<div class="method-step__io" markdown="1">

**输入**：某一轮为止的累积图$\Gamma$、查询源实体$x$、目标属性$y$、模型上一轮预测，以及当前更新的形式化作用。<br>
**输出**：每轮的$\mathrm{yes}$、$\mathrm{no}$或$\mathrm{unknown}$真值，默认推理的更新效果标签，以及用于确认偏差分析的条件编号和汇总统计量。

</div>

**直观理解**：解析器像一个不受语言表面影响的裁判：只检查与当前对象和属性真正连通的路径。偏差分析再比较模型面对“顺着自己原判断”的证据和“要求推翻原判断”的证据时是否表现不对称。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 确认偏差差值（Bias Gap）

$$
\mathrm{BiasGap}=\mathrm{Acc}(\mathrm{C1})-\mathrm{Acc}(\mathrm{C2})
$$

**符号说明**

- $\mathrm{BiasGap}$：模型处理一致证据与不一致证据时的准确率差。
- $\mathrm{Acc}(\mathrm{C1})$：C1轮次上的准确率；模型先前回答为肯定，且新证据真实地增强假设。
- $\mathrm{Acc}(\mathrm{C2})$：C2轮次上的准确率；模型先前回答为肯定，但新证据真实地削弱或击败假设。

<div class="equation-explanation" markdown="1">

**直观理解**：该式直接比较模型接受支持性证据与接受反驳性证据的能力。正值表示模型在C1上比C2更准确；作者将这种系统性正差距视为确认偏差的标志，但它是行为不对称指标，并不单独解释偏差产生的内部机制。<br>
**原文位置**：第3.8节，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 确认偏差优势比（Odds Ratio）

$$
\mathrm{OR}=\frac{\mathrm{C1}_{\mathrm{correct}}\,\mathrm{C2}_{\mathrm{wrong}}}{\mathrm{C1}_{\mathrm{wrong}}\,\mathrm{C2}_{\mathrm{correct}}}
$$

**符号说明**

- $\mathrm{OR}$：C1相对于C2产生正确反应的优势比，是不依赖准确率绝对尺度的效应量。
- $\mathrm{C1}_{\mathrm{correct}}$：C1条件中回答正确的轮次数。
- $\mathrm{C1}_{\mathrm{wrong}}$：C1条件中回答错误的轮次数。
- $\mathrm{C2}_{\mathrm{correct}}$：C2条件中回答正确的轮次数。
- $\mathrm{C2}_{\mathrm{wrong}}$：C2条件中回答错误的轮次数。

<div class="equation-explanation" markdown="1">

**直观理解**：优势比把两种条件下“正确相对于错误”的比值再作比较；$\mathrm{OR}>1$表示模型对一致证据的相对优势更大，$\mathrm{OR}=1$表示两种条件没有这种不对称。论文在对话层级进行bootstrap并计算95%置信区间，以避免把同一对话内高度相关的多个轮次误当成完全独立样本。<br>
**原文位置**：第3.8节，公式（2）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。DeReLab是生成式评测与诊断框架，不训练被测语言模型，也未提出需要梯度优化的新模型目标；图解析器通过确定性规则计算标签，Bias Gap与优势比用于测试后统计分析，而不是训练损失。框架中的“生成式”指按参数生成新推理实例和多轮更新轨迹，并非训练一个生成模型来拟合数据。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 参数化图生成器**

图包含实体与属性两类节点，以及假设边、单调事实属性边、可废止正属性边和可废止负属性边。默认拓扑用属性链、多个对象、干扰节点和按深度排序的击败边表示规则传播；线性继承使用从根类到叶实体的单链，树形继承则加入兄弟分支，并把阻断边限定在单个节点及其路径范围内。

> 直观理解：该模块决定题目真正考什么：长链考连续传播，分支树考作用域，多来源冲突考优先级，无关节点考抗干扰。因为这些因素都能单独调节，研究者可以在保持其余条件不变时诊断某一种能力。

**2. 怀疑式路径解析器**

解析器把逻辑结构抽象为带符号的有向无环图：继承、蕴含、属性和可废止正属性边提供正支持，可废止缺失属性边提供负证据，假设边与无关属性边不参与传播。它先用从$x$出发的正向可达集合与可到达$y$的反向集合之交裁剪图，再按前驱均已处理的拓扑层次传播状态；直接附着于主体的证据覆盖较长继承链，更具体类别的证据抢占更一般类别的冲突证据，彼此无特异性关系的冲突采用怀疑式结论$\mathrm{unknown}$。

> 直观理解：裁剪可以防止模型或标注器把兄弟分支、无关属性误算进来；抢占规则则表达“更具体的信息优先”。当两条相反路径同样有资格而无法决定谁更具体时，系统不武断二选一，而是标为未知。

**3. 认知偏差条件分配器**

每个更新轮次根据模型自身上一轮预测与更新的真实效果动态分类：C1表示先前回答为$\mathrm{yes}$且证据增强假设，C2表示先前回答为$\mathrm{yes}$但证据削弱假设；C3和C4分别检验假设已被击败后，表面否定更新或中性无关更新是否诱发错误变化；C5检验模型从$\mathrm{unknown}$状态接受方向性证据的能力。确认偏差的核心比较在同一类多轮轨迹中进行，以C1作为接受一致证据的控制条件，以C2作为是否愿意推翻既有结论的关键条件。

> 直观理解：条件归类以模型上一轮实际相信什么为基准，而不是只看标准答案，因此测到的是模型自身信念轨迹中的“坚持原判断”。如果模型容易接纳支持原判断的证据，却在同样明确的反证出现时拒绝更新，C1与C2就会出现系统性差距。

**训练与推理**

生成阶段先选定默认、线性继承或树形继承拓扑及难度配置，采样抽象图、冲突边、干扰边、假设和披露顺序，再以伪词实体、领域一致属性和语言模板实例化。对每个对话轮次，系统把新事实加入累积前提，并重新运行路径解析器，从而得到当前假设的三值标签；默认推理还比较更新前后的支持状态，生成增强、削弱或无影响标签。被测模型在推理时只接收当前轮可见的对话上下文并回答蕴含问题；默认推理还回答效果问题，实验也可交换两类问题的先后顺序。完成预测后，系统以模型紧邻前一轮的预测而非前一轮标准答案确定其先验信念，再结合当前更新的真实作用分配C1至C5条件，汇总准确率、Bias Gap和优势比；置信区间在完整对话层级重采样。

**复现信息**

复现时最关键的是保持结构参数、标签规则和信息披露顺序一致。默认推理的Easy配置使用5至10个链节点、2至3个对象、1至2个无关属性、$0.30$至$0.50$的稀疏因子和最多2个假设段；Hard配置使用10至20个链节点、4至6个对象、2至4个无关属性、$0.40$至$0.70$的稀疏因子和最多3个假设段。继承推理的难度由最大深度、根宽度、分支范围、生存概率、分支衰减和稀疏因子共同控制，不能只按文本长度解释难度。

标签实现必须区分支持边、击败边和被忽略边，并保证树形继承中的阻断只影响该节点对应的路径，不扩散至兄弟或堂兄弟分支。图解析应先裁剪到与查询相关的子图，再按拓扑顺序处理；主体直接证据、来源优先级、特异性抢占、对称冲突的怀疑式未知，以及默认链允许的合成旁路均会改变答案。主数据集使用程序生成的可发音伪词，目的是减少预训练语料污染和现实常识捷径；因此若改用真实实体，所得结果将同时混入记忆知识，不能与原设定直接等同解释。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- DeReLab规范评测集：由参数化图结构生成多轮信念更新对话，覆盖默认推理、线性继承和树状继承三种拓扑；每种拓扑均含简单与困难划分，每个“拓扑—难度”组合有150段对话，共900段对话和18,390个需要作答的轮次。其作用是以逐轮形式验证模型能否依据新增证据修正当前结论。困难划分相对简单划分增加图规模、干扰属性、结构密度和推理深度，因此用于测试复杂度增长带来的退化。
- 规范集的拓扑子集：默认推理包含简单划分1,905个作答轮次、困难划分9,325个；线性继承分别包含646和2,483个；树状继承分别包含963和3,068个。默认推理测试可被例外推翻的一般规则，继承推理测试属性沿层级结构传播及被局部信息覆盖的能力。所有规范样例均使用伪词实体，以尽量排除模型调用记忆中的现实知识，而非根据给定结构推理。
- 重播种稳健性集：包含1,200个样例，由20个随机种子、两种拓扑以及每个“种子—拓扑”组合30段对话构成。该集合不用于扩展任务类别，而用于检验观察到的性能和偏差是否依赖某一次随机生成。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**逐轮准确率**

将每个需要作答的对话轮次与形式化验证的真实标签比较，衡量模型在当前证据状态下是否给出正确结论；该指标同时用于总体推理任务及加强、削弱、无影响的信念更新分类。 （越高越好，因为更高值表示模型在更多证据更新节点上与形式化真实答案一致。）

</div>
<div class="metric-item" markdown="1">

**确认偏差差距（BiasGap）**

定义为一致证据条件准确率减去不一致证据条件准确率，即$\mathrm{C1\ acc}-\mathrm{C2\ acc}$。C1表示新证据与模型原有结论方向一致，C2表示新证据要求模型反向修正；该差值衡量模型是否对冲突证据存在额外阻力。 （绝对值越接近零越好；显著为正意味着模型处理一致证据比处理不一致证据更准确，符合确认偏差的行为模式。）

</div>
<div class="metric-item" markdown="1">

**更新效果元认知准确率**

在独立的effect-of-update问题上，分别计算模型把一致更新识别为strengthening的C1-effect准确率，以及把不一致更新识别为weakening的C2-effect准确率。它把“知道证据朝哪个方向起作用”与“真正修改最终结论”区分开。 （越高越好，因为更高值表示模型更能正确识别证据对当前信念的作用方向；但该指标高并不必然意味着最终结论更新正确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 总体可撤销推理能力：比较推理型配置与标准指令微调配置，并区分默认推理、继承推理和信念更新任务。

<div class="result-value" markdown="1">

作者报告，具备推理能力的配置整体明显优于标准指令微调配置；默认推理持续比继承推理困难，而要求判断strengthening、weakening或no effect的信念更新任务最具挑战性。

</div>

这说明测试的难点不只是沿图结构传播属性，而是当默认规则可能被新证据推翻时，维护并修订一个暂时成立的结论。该结果支持“推理模式有帮助”和“任务类型难度不同”，但节选未给出图2的具体准确率，因而不能据此量化模型间差距。

<div class="result-source" markdown="1">

来源：第5.1节 Overall Reasoning Accuracy；相关结果见图2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We notice a significant performance gap between reasoning-enabled and standard instruction-tuned configurations, where reasoning models clearly outperform the latter.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 确认偏差：比较模型对一致证据条件C1和不一致证据条件C2的处理准确率。

<div class="result-value" markdown="1">

作者称，几乎所有受测模型都表现出系统性不对称：更容易接受与当前结论一致的证据，同时更抗拒要求反向更新的不一致证据。图3同时提示，并非每个“模型—推理类型”组合都在Holm校正后显著，因此该结论是总体趋势而不是无例外的普遍规律。

</div>

若模型只是一般性地不擅长更新，C1和C2应当近似同样困难；C1优于C2则表明错误与证据方向有关，更接近操作化的确认偏差。不过，这一行为指标不能证明模型具有类似人类的心理机制，只能说明其输出呈现方向性更新不对称。

<div class="result-source" markdown="1">

来源：摘要；第5.2节 Confirmation Bias in Belief Updating；图3左侧

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Applying this capability to the study of confirmation bias, we evaluate nine open and proprietary large language models and find that nearly all exhibit a systematic tendency to accept congruent evidence while resisting incongruent updates, with several models correctly identifying a weakening update yet failing to revise their conclusion.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 元认知与实际修订的分离：对同一更新轮次，同时询问证据作用方向和最终蕴含结论。

<div class="result-value" markdown="1">

若干模型能够正确识别某条不一致证据正在削弱原结论，却仍未据此修改最终答案，显示“识别更新方向”和“执行信念修订”可以发生分离。

</div>

这一结果把失败定位得更精细：模型未必不理解新证据的局部含义，而可能在把该含义整合进全局结论时失败。它不证明内部表征中一定存在独立的元认知模块，只表明两个外显问答指标可以不一致。

<div class="result-source" markdown="1">

来源：摘要；图3右侧 Metacognitive accuracy on the belief-update task

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Applying this capability to the study of confirmation bias, we evaluate nine open and proprietary large language models and find that nearly all exhibit a systematic tendency to accept congruent evidence while resisting incongruent updates, with several models correctly identifying a weakening update yet failing to revise their conclusion.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 规范集全部采用伪词实体，这有助于控制事实记忆污染，却降低了对真实语言环境的直接外推性；现实任务中的语义常识、歧义和知识冲突可能使信念更新呈现不同难度。当前实验主要证明模型在受控形式结构上的行为，而非真实世界确认偏差的完整表现。
- 所给章节节选未包含图2的具体分数、图3的完整置信区间或第5.2节完整统计表，因此只能核实总体趋势及少数显著性例外，无法独立判断效应大小、模型排序的稳定程度或所有条件下的统计可靠性。作者另设重播种集以测试随机种子稳健性，但节选没有报告该集合的最终结果。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 闭源GPT模型：gpt-5.1作为较强前沿模型参照，gpt-5-mini作为紧凑型推理模型参照，用于判断开放权重模型与强闭源系统之间是否存在能力差距。
- Gemma-4系列：比较Gemma-4-31B-it、Gemma-4-12B-it和Gemma-4-E4B，可在同一模型家族内观察规模变化；Gemma-4-26B-A4B还提供混合专家架构与稠密模型之间的架构参照。
- Llama-3.1系列：Llama-3.1-70B与Llama-3.1-8B构成同家族的大、小模型比较，用于检验可撤销推理能力是否呈现常见的规模效应。
- Qwen3-32B双模式：同一模型分别以thinking和non-thinking模式推理，减少模型家族和参数规模等混杂因素，直接测试显式延长推理过程是否改善表现。

**实验想回答的问题**

- 当前大语言模型能否在新证据到来后正确进行可撤销推理，并且这种能力是否随推理拓扑、任务难度、模型规模及推理模式而系统变化？
- 模型在信念更新时是否更容易接受与既有结论一致的证据、抵制与既有结论冲突的证据；当最终结论更新错误时，模型是否仍能元认知地识别证据是在加强还是削弱原结论？

**实验实现**

所有模型均在多轮聊天设置下评测，逐轮接收由DeReLab生成的新证据，并依据每一轮的形式化真实标签计分。实验覆盖闭源与开放权重模型、不同参数规模、稠密与混合专家架构，以及Qwen3-32B的thinking和non-thinking两种模式。总体能力按推理拓扑和简单、困难层级报告；确认偏差分析则对第一阶段推理结果应用一致性条件框架，每个模型得到9,029至11,682个带条件标签的轮次。图3还区分默认推理与继承推理，并对多重统计检验使用Holm校正。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Qwen3-32B的thinking与non-thinking模式比较。 | 关闭扩展思考后，Qwen3-32B的表现显著下降。 | 这是节选中最接近受控消融的比较：模型主体保持不变，只改变是否启用扩展推理过程，因此较直接地隔离了推理模式的作用。不过原文节选没有提供下降的具体幅度，也不能排除两种解码模式在计算预算上的差异是收益来源之一。 | 第5.1节 Overall Reasoning Accuracy；图2<br><span class="experiment-evidence">For Qwen3-32B, performance decreases substantially when extended thinking is disabled.</span> |
| 同一模型家族内的规模比较：Gemma-4系列与Llama-3.1系列。 | 作者观察到更大模型在各项条件中优于同家族较小模型，并将其解释为与其他推理基准一致的规模趋势。 | 该比较主要隔离模型规模与同家族版本差异的联合影响，说明容量较大的版本更适合本任务；它并非严格消融，因为不同规模模型的训练过程和数据暴露可能也不完全相同。原文节选未提供各模型准确率及差值，不能判断收益是否线性或是否具有统计显著性。 | 第5.1节 Overall Reasoning Accuracy；图2<br><span class="experiment-evidence">Larger models perform better within each family: Gemma-4-31B > Gemma-4-12B > Gemma-4-E4B and Llama-3.1-70B > Llama-3.1-8B across all conditions, consistent with the general scaling trend observed in reasoning benchmarks.</span> |

**定性案例**

- 代表性行为模式是：模型在effect-of-update问题中把不一致证据正确标为weakening，却在随后的蕴含判断中保留原结论。该案例说明局部证据理解正确并不足以保证全局信念状态被更新，也是作者将元认知准确率与最终任务准确率分开报告的原因。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces a controlled benchmark for evaluating LLM defeasible reasoning and belief updating, including confirmation bias.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`6866fe8aab00566b33984af72437d5dc3df90bb1939e14f99f7ed31586cba0a6`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
