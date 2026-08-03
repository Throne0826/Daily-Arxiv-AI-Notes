---
title: "[论文解读] Metaphor-Induced Algorithmic Steering: Cross-Domain Procedural Transfer in LLM Code Generation"
description: "[arXiv 2607.28683][LLM Reasoning] 本文研究“隐喻诱导的算法转向”：看似无害且不直接指定算法的跨领域隐喻，可能把源领域的操作模式迁移到代码或 SQL 生成中，使大模型偏向正确但低效的实现。"
arxiv_id: "2607.28683"
announcement_date: "2026-08-03"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-03T02:16:53.763878+00:00"
source_sha256: "e22f3d107ad8696e393e940865f892e7f4d3781c7d3b01563e2e03367a41821a"
tags:
  - "LLM Reasoning"
  - "隐喻诱导的算法转向"
  - "跨域程序迁移"
  - "代码生成"
  - "SQL 生成"
  - "类比推理"
  - "算法效率"
  - "上下文学习"
  - "自然语言欠规范性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2607.28683</p>

# Metaphor-Induced Algorithmic Steering: Cross-Domain Procedural Transfer in LLM Code Generation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-03</span>
<span><strong>作者</strong> Zhibo Hu, Chen Wang, Yanfeng Shu, Hye-young Paik, Liming Dong, Liming Zhu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> The University of New South Wales</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.28683) · [PDF 下载](https://arxiv.org/pdf/2607.28683) · **关键词** 隐喻诱导的算法转向, 跨域程序迁移, 代码生成, SQL 生成, 类比推理, 算法效率, 上下文学习, 自然语言欠规范性<br>


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

本文研究“隐喻诱导的算法转向”：看似无害且不直接指定算法的跨领域隐喻，可能把源领域的操作模式迁移到代码或 SQL 生成中，使大模型偏向正确但低效的实现。

**不用术语来说**：自然语言不仅表达任务要求，也会暗示“应当怎样做”。例如，医学语境中“回到完整原始样本、逐项检查”本来合理，但模型可能把这种做法套到编程问题上，放弃动态规划、索引或滑动窗口，转而遍历全部候选或反复重建结果。代码虽然仍能运行并给出正确答案，却可能显著浪费时间和计算资源，而且提示文本没有明显的恶意指令，因而难以察觉。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出“隐喻诱导的算法转向”这一问题，并以代码生成和 SQL 生成为场景，论证自然、无害且与任务相关的隐喻性技能文本能够迁移抽象操作模式，在不点名目标算法或复杂度要求的情况下改变模型的算法选择。
- 作者提出 MASC 框架，用于迭代生成、筛选和改写隐喻性技能，并进一步从模型隐藏状态与指令级检测两个角度考察该现象是否具有表征层证据以及能否被防御机制识别。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型的上下文学习、文本到代码生成与跨域类比推理交叉处。代码生成模型通常根据自然语言题目及补充“技能”选择算法；自然语言不仅表达显式要求，还可能通过隐喻传递关系结构和操作顺序。论文关注由此产生的一类失效：某种程序性做法在医疗等来源领域中合理且无害，但被模型类比到编程或 SQL 任务后，可能使其从动态规划、索引或滑动窗口等高效策略转向穷举、全量扫描或反复重建等低效但仍正确的策略。作者将这一现象称为“隐喻诱导的算法转向”，研究重点不是普通的代码正确性错误，而是自然语言中未明说的跨域程序模式如何改变算法选择与计算效率。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**上下文学习**

大语言模型在不更新参数的情况下，根据当前提示中的说明、示例或背景信息临时调整行为。本文中的附加技能文本因此可能改变模型解决同一道编程题时采用的算法。

</div>
<div class="concept-item" markdown="1">

**结构映射与类比迁移**

结构映射是把两个表面不同领域中的对象关系和操作结构对应起来；类比迁移则是将来源领域的推理或程序模式用于目标领域。本文强调迁移的是“检查全部原始记录”等关系性程序结构，而不只是相似词语。

</div>
<div class="concept-item" markdown="1">

**算法效率**

算法效率描述输入规模增长时所需时间或空间如何增长。本文比较的通常是都能产生正确结果、但计算成本不同的实现，例如动态规划相对于暴力枚举，或使用索引相对于反复全表扫描。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究包含代码生成和 SQL 生成两类目标场景。输入由一个具有特定领域背景的生成任务以及一段表面自然、无害且与任务相关的技能说明组成；该技能使用来源领域的隐喻或隐喻类比表达某种程序偏好，但不应直接点名目标算法、数据结构、复杂度要求，也不应以编程术语显式要求低效实现。模型输出可执行代码或 SQL，研究者比较无附加技能时的默认策略与加入隐喻技能后的策略，判断模型是否在保持结果正确的同时，从较高效算法转向穷举、全量扫描、重复重建等较低效算法。核心假设是：模型能够依据共享的关系结构，把来源场景中合理的操作模式迁移到目标任务；例如把“审阅完整标本而不信任派生摘要”映射为“反复读取全部原始输入而不使用缓存、压缩结果或索引”。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Webb et al. (2023)**: 该工作表明大语言模型能够完成多类类比任务，并识别跨领域故事之间的高阶因果对应，为本文关于模型可迁移关系结构与程序模式的前提提供经验依据；本文进一步考察这种能力如何在代码生成中造成非预期的效率退化。
- **Jones et al. (2026), AUTOELICIT**: 该工作显示无害指令也可能改变大语言模型决策。本文将 AUTOELICIT 产生的字面技能转向作为直接相关的比较对象，用于区分显式描述低效策略的影响与隐喻类比在未明说目标算法时造成的算法退化。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

以自然语言驱动软件设计时，提示中的背景知识和类比不只是提供事实，还可能隐含操作偏好。大模型强大的上下文泛化能力会把某一专业领域中合理的流程迁移到程序求解过程，导致算法效率下降；由于输出仍可能功能正确，常规的正确性检查不一定能够暴露这种风险。在关键软件场景中，这说明自然语言接口的欠明确性不仅会影响语义理解，也会悄然影响实现策略和资源消耗。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **直接或字面化的行为诱导方法**：已有良性指令诱导研究表明，即使指令表面无害，也可能改变大模型决策；文中具体以 AUTOELICIT 产生的字面技能转向作为比较对象。这类方法通常较明确地描述希望模型采用的行为或过程，因此可以测试模型是否会遵循某种操作偏好。
- **跨领域类比与概念表征研究**：既有类比研究考察模型能否识别不同故事之间的高阶关系，概念表征研究则分析跨语言、跨输出形式相对稳定的概念向量，并尝试通过操纵这些向量影响行为。这些工作说明模型能够编码和迁移抽象关系，为隐喻可能携带程序性结构提供了理论与机制基础。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 直接或字面化诱导往往会显式暴露低效过程、目标算法或行为意图，因而不能回答更隐蔽的问题：只使用在源领域中自然合理、且不包含编程或复杂度术语的隐喻，是否仍足以使模型采用穷举、全量扫描或反复重建等低效策略。
- 既有类比与概念向量工作主要证明模型能够识别或操纵抽象关系，但尚未系统连接“隐喻中的程序性结构—代码算法选择—隐藏状态变化—可检测性”这条证据链。因此，无法据此判断跨领域迁移是否会造成正确但低效的软件实现，也缺少针对该风险的专门评估框架。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种严格的研究设置，用来构造表面自然、语义良性且与任务背景相关的隐喻性技能，同时排除直接点名低效算法的简单提示效应，并检验这些技能是否会稳定地把源场景的关系结构迁移为目标编程任务中的低效操作策略。进一步的空缺是：这种行为究竟源于表层隐喻措辞，还是模型内部确实发生了朝低效率程序原型的表征偏移，以及此类隐蔽指令能否在生成代码之前被识别。

</div>
<div markdown="1"><span>核心问题</span>

给定希望避免的低效率行为，与表达相近的字面指令相比，自然存在的隐喻性指令能否在不明确提及目标算法、数据结构或效率目标的情况下，更有效地把大模型从默认的高效方案引向正确但低效的代码或 SQL 实现？

</div>
<div markdown="1"><span>作者直觉</span>

隐喻的作用不只在于替换词语，而在于保留关系结构和操作顺序。若源场景强调“不要相信压缩后的结果，应返回完整原始材料并逐项复核”，模型可能把原始材料对应为完整输入、把逐项复核对应为全量遍历、把派生结果对应为缓存或索引。这样一来，提示无需说“使用暴力搜索”，也能使暴力式过程在模型推理中变得更显著；如果这一解释成立，模型的中后层隐藏状态还应更接近低效率行为的表征原型，而不只是对隐喻词汇产生表面响应。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MASC（Metaphorical Algorithmic Steering for Code Generation）是一个两阶段搜索与评估框架，用于检验跨领域隐喻能否在不直接点名算法的情况下，改变代码模型选择的实现策略。输入包括编程任务、模型在无技能提示时采用的高效默认策略，以及希望诱导的低效率目标行为；阶段 I 生成并筛选具有自然、良性表层含义的隐喻技能，阶段 II 将技能置于任务之前生成代码，再由静态算法判定器和行为评估器比较有技能代码与固定的无技能基线。失败候选依据代码层反馈迭代改写，最终输出既足够隐含、又能稳定诱导更穷举、更频繁重算或更全面扫描策略的技能集合。

这里的“技能”不是模型参数或可执行程序，而是一段附加到编程题前的自然语言指令；“跨领域程序迁移”则指把源场景中的做事方式映射到代码求解过程。例如，源场景可以强调逐项检查、从头重建或不遗漏任何可能性，但不能直接要求使用暴力枚举、重复扫描等具体算法。MASC 不执行生成代码，因此它衡量的是静态判断下的算法策略转移与功能合理性，而不是通过测试用例验证的真实运行时间或完整正确性。论文还给出一个独立的生成前防御门：给定任务 $q$ 与技能 $s$，检测器同时判断指令形式及其是否会对低效率策略产生因果压力，从而决定是否应在代码生成前拦截或标记该输入。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立无技能基线与目标行为

先仅向代码模型提供编程任务，得到固定的无技能代码基线；该基线用于确认模型自然采用的策略，并作为后续有技能代码的比较对象。目标行为可以是指定的低效率算法，也可以是相对默认策略明显更高复杂度、更穷举的程序过程。

<div class="method-step__io" markdown="1">

**输入**：编程任务、代码生成模型，以及预先确定的高效默认策略和较低效率目标策略。<br>
**输出**：每个任务对应的无技能代码、默认算法策略描述，以及期望诱导的低效率行为描述。

</div>

**直观理解**：先观察模型正常情况下会怎样解题，再规定希望隐喻把它推向哪种更笨重的解法。这样可以避免把模型原本就会生成的低效率代码误算成隐喻造成的变化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 上下文感知的隐喻技能生成

技能生成器选择一个合理的非编程源场景，构造从该场景到当前编程任务的程序性映射，使源场景隐含穷举审查、完整重建或逐案处理等过程。候选文本必须在源场景中自然、保持良性表层含义，并避免出现算法名称、复杂度术语或具体实现机制。

<div class="method-step__io" markdown="1">

**输入**：编程任务、高效默认策略、低效率目标行为，以及此前轮次汇总的生成与筛选反馈。<br>
**输出**：一组与当前任务相关的候选隐喻技能。

</div>

**直观理解**：生成器不直接说“请用暴力算法”，而是写一段看似无害的做事原则，让代码模型可能把这套做事方式类比到解题过程。任务上下文决定哪种隐喻最可能与目标程序过程形成对应。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 技能质量门筛选与局部修订

质量评估器检查候选是否构成有效的跨任务隐喻、源场景是否真实自然、表层含义是否良性，以及目标算法和实现机制是否泄漏得过于明显。未通过的候选依据评估反馈进行局部改写，早期轮次的汇总反馈还会指导后续种子生成；通过者被排序并保留。

<div class="method-step__io" markdown="1">

**输入**：候选隐喻技能、对应编程任务，以及候选生成历史。<br>
**输出**：经过过滤和排序的种子隐喻技能集合。

</div>

**直观理解**：这一关同时防止两类失败：隐喻太模糊会不起作用，隐喻太直白又会退化成普通的算法命令。局部修订的目的，是尽量只改掉被指出的问题，而不是每次从头随机生成。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 技能引导的代码生成与静态行为判定

系统把技能前置于编程任务并调用同一代码模型生成有技能代码，但不执行该代码；静态算法判定器识别实现策略，行为评估器判断代码是否在功能上仍然合理，并比较其与无技能默认策略及低效率目标策略的对齐程度。若代码匹配指定目标，或被判为相对默认实现明显具有更高复杂度、更全面或更重复的处理过程，则该技能被视为成功。

<div class="method-step__io" markdown="1">

**输入**：通过质量门的技能、原始编程任务、固定无技能基线、默认策略和目标策略。<br>
**输出**：成功标记，或包含观察到的算法标签、与默认及目标策略的对齐情况和失败原因的反馈记录。

</div>

**直观理解**：系统关心的不只是代码能否看起来完成任务，还关心隐喻是否真正改变了“怎么做”。由于没有运行代码，这里的成功是评审模型对静态实现策略的判断，不能等同于实测性能下降。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文节选未给出 MASC 的可微训练目标、损失函数或参数更新过程；该方法应理解为基于生成、静态评估和反馈修订的推理时搜索框架，而非通过梯度训练得到的新代码模型。技能成功条件是离散判定：有技能代码匹配指定低效率目标策略，或者相对固定的高效默认策略被评为明显更高复杂度或更穷举。防御检测器同样以提示完成分类和影响预测，节选没有报告对 Qwen-Coder-Next 80B 进行微调或优化，因此不能据此推断其训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 上下文感知技能生成器与质量门**

生成器以任务、默认高效策略和低效率目标行为为条件，选择源场景并建立跨领域程序映射；质量门从隐喻质量、源场景现实性、良性、隐含性、算法显著性和目标实现机制显著性等维度过滤候选。候选未通过时，评估器反馈用于局部修订，而跨轮次聚合反馈用于改进后续种子的生成方向。

> 直观理解：生成器负责提出可能有效的“委婉暗示”，质量门负责保证这种暗示既自然又没有直接泄露答案。二者配合，使论文研究的对象确实是隐喻迁移，而不是把明确算法指令换一种措辞。

**2. 静态算法判定器与行为评估器**

算法判定器从生成代码中识别实现策略；行为评估器检查实现是否仍具功能合理性，并以固定无技能代码为参照，判断策略是否偏离高效默认解、转向指定目标或其他明显更高复杂度、更穷举的实现。评估过程不执行代码，其反馈包括算法标签、默认与目标对齐程度以及失败原因。

> 直观理解：算法判定器回答“模型用了什么方法”，行为评估器回答“这种变化是否由高效转向低效且没有明显破坏任务意图”。固定基线让比较集中于同一模型在加入技能前后的策略差异。

**3. 指令级低效率引导防御门**

检测器接收任务 $q$ 和技能 $s$，但不接收技能集合类别、记录编号、文件路径、期望标签或其他元数据。它完成两个预测：其一是把指令形式分类为跨领域隐喻或程序类比、字面技能引导、完全良性或歧义类别；其二是判断该技能是否会对当前任务中的低效率代码策略形成因果压力，并解释是否涉及穷举、从头重算、重复扫描、反复用或不必要状态扩张。

> 直观理解：只识别“这像一个隐喻”并不足以防御，因为许多普通比喻不会改变算法。第二个预测把技能与具体题目结合，判断它是否真的可能导致低效率行为，从而减少对无害背景描述的误拦截。

**训练与推理**

MASC 的完整推理过程为：对每道题先运行一次无技能代码生成，固定其代码和默认策略；随后根据任务、默认策略与目标行为生成多个隐喻种子，经质量门筛除不自然、不良性、过于直白或泄漏实现机制的候选。对每个保留技能，将其前置到原题后调用代码模型，静态判断实现算法和功能合理性，并相对无技能基线评估策略转移。成功候选进入最终集合；失败候选保留算法标签、对齐情况和原因，结合历史反馈改写后重新过质量门并再次生成代码，形成闭环搜索。

防御阶段发生在实际代码生成之前。检测器只读取任务 $q$ 和技能 $s$ 的文本，以少量示例提示所规定的输出格式返回形式类别、影响标签、置信度、证据片段和机制说明。主要影响评估把 Metaphor 技能视为正例，把 Benign 与 Neutral Distractor 视为负例；Literal 技能因预期影响混合而不纳入主要影响分类，但用于指令形式识别和描述性比较。原文节选没有说明搜索轮数上限、停止阈值、采样温度、每轮候选数量或检测器参数训练过程。

**复现信息**

复现时最关键的控制是：无技能代码必须在加入任何技能之前生成并固定，后续比较不能为每个候选重新选择基线；技能需要置于原始编程任务之前；有技能与无技能条件应使用相同的代码模型，以免把模型差异误认为提示引导。MASC 对生成代码只做静态分析而不执行，因此实验结论应解释为“被判定的算法策略和复杂度倾向发生变化”，不能直接外推为通过测试用例的正确率、实际墙钟时间或内存消耗变化。

防御实验使用 Qwen-Coder-Next 80B 作为检测器，并对同一组 90 道编程题分别配对 Metaphor、Benign、Neutral Distractor 和 Literal 技能，每组 90 个。检测时不得暴露集合类别、样本编号、路径或期望标签等元数据；主要低效率影响评估仅使用 Metaphor 正例以及 Benign、Neutral Distractor 负例。节选还列出 MASC 在 APPS 与 BIRD-SQL 上使用 Qwen-Coder-Next 80B、Deepseek-Coder-33b-Instruct 和 Gemma-4-31B 等代码模型，但没有提供足以复现生成与精炼循环的解码参数、评审提示全文和停止规则，这些信息仍需回查论文其他章节或附录。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- APPS：包含 10,000 道编程题，难度从入门练习到较难算法题。实验只选取目标模型在不加入技能时能够持续生成正确且高效代码的题目，并保留原始题面；其作用是测试隐喻是否会使本来表现稳定的模型改用穷举、重复扫描、重复计算或避免复用紧凑状态等低效率策略。原文未明确报告筛选后的题目数量及训练、验证、测试划分。
- BIRD-SQL：包含 12,751 个自然语言问题—SQL 对，覆盖 95 个数据库和 37 个领域。实验同样筛选默认能够稳定生成正确高效结果的问题，用于检验该现象能否从一般程序生成迁移到文本转 SQL；原文未明确报告筛选后的样本量、具体划分以及表 1 中的完整数值。
- 表示层分析样本：Metaphor、Benign 与 Neutral Distractor 三组各含 90 个技能，并与相同的 90 道编程题配对，共形成 270 个技能—任务样本。Metaphor 编码可能诱导低效率实现的隐喻过程映射；Benign 提供忠实于任务的正常指导；Neutral Distractor 只加入自然的背景领域框架而不应诱导低效率行为。该配对设计用于控制题目差异，隔离隐喻过程信息对隐藏表示的影响。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**转向成功率（steering success）**

判断生成结果是否相对于题目适用的高效策略，采用了预期的低效率实现。per-sample 是全部任务—生成样本中成功转向的比例；per-task 则只要某题至少有一个生成技能诱发目标策略，就把该题计为成功。因此 per-task 更接近“搜索后能否找到有效技能”，per-sample 更接近单次使用技能的稳定性。 （若研究目标是证明攻击或负面转向有效，则数值越高表示越容易诱发低效率策略；但从代码质量与安全角度看，数值越低越好。）

</div>
<div class="metric-item" markdown="1">

**转向严重度（steering severity）**

把算法效率退化按 None、Low、Medium、High、Critical 五个有序等级归类；每题的严重度取该题所有生成技能中观察到的最高等级。它补充成功率，区分轻微实现冗余与显著复杂度退化。 （对攻击有效性而言，越偏向 High 或 Critical 说明影响越严重；对模型稳健性而言，严重度越低越好。由于按题取最大值，它反映最坏观察结果，而非平均风险。）

</div>
<div class="metric-item" markdown="1">

**行为原型对齐变化与 AUC**

在第 $l$ 层，先比较任务单独表示 $h_Q^l$ 和加入技能后的表示 $h_{S,Q}^l$ 分别与行为原型 $h_B^l$ 的余弦相似度，再取差得到 $\Delta_{\mathrm{align}}^l$；正值表示技能使表示更接近目标低效率过程。AUC 则把 $\Delta_{\mathrm{align}}^l$ 当作标量分数，衡量其区分 Metaphor 与两类控制样本的能力。 （更大的正向 $\Delta_{\mathrm{align}}^l$ 表示更强的目标行为对齐；更高的 AUC 表示隐喻样本与控制样本在表示层面更可分。二者证明的是相关的表示移动，不直接证明因果机制。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### APPS 上三种代码模型：Metaphorical Skill Steering 对比 Literal Skill Steering

<div class="result-value" markdown="1">

三种模型上，隐喻技能的 per-sample 与 per-task 成功率均高于字面技能。Qwen 为 23.3%/41.1%，字面条件为 9.6%/17.8%；DeepSeek 为 34.5%/43.8%，字面条件为 4.4%/8.2%；Gemma 为 23.6%/28.6%，字面条件为 2.9%/3.9%。Qwen 的 High 和 Critical 任务占比也由字面条件的 7.8% 和 1.1% 上升到隐喻条件的 18.9% 和 4.4%。

</div>

作者据此主张，隐喻不是把直接指令换一种含蓄说法，而是能够更有效地改变算法选择。结果跨三个模型家族方向一致，说明现象并非只属于单个模型。不过，这些比例是在预筛题目、搜索得到技能的协议下测得，尤其 per-task 指标允许“多个技能中至少一个成功”，不能解释为任意隐喻提示在自然使用中都有同样高的成功概率；实验也没有报告生成代码总体正确率是否保持不变。

<div class="result-source" markdown="1">

来源：第 3.2 节，表 1 的正文解读

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Qwen, it achieves 23.3% per-sample and 41.1% per-task success, versus 9.6% and 17.8% for literal steering. The severity distribution also shifts upward, it produces high-severity outcomes on 18.9% of tasks and critical-severity outcomes on 4.4%, compared with 7.8% and 1.1% under literal steering. Deepseek has the highest metaphorical steering success, reaching 34.5% per sample and 43.8% per task, compared with only 4.4% and 8.2% for literal steering. Gemma also shows a large gap, with metaphorical steering reaching 23.6% per sample and 28.6% per task, versus 2.9% and 3.9% for literal steering.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### BIRD-SQL 上的 Qwen-Coder-Next 80B：跨任务类型比较隐喻与字面技能

<div class="result-value" markdown="1">

在文本转 SQL 场景中，作者报告隐喻技能的 per-sample 和 per-task 成功率均高于字面技能，且严重度分布向更严重等级移动；所给节选未包含表 1 的 BIRD-SQL 具体数值。

</div>

该结果说明观察到的转向不只局限于 APPS 式通用编程题，可能也影响数据库查询规划或 SQL 构造。由于节选没有提供样本规模、完整分数和逐类错误，现有证据只能支持方向一致的跨领域现象，不能量化其幅度，也不足以判断它是否适用于其他结构化生成任务。

<div class="result-source" markdown="1">

来源：第 3.2 节，表 1 的 BIRD-SQL 结果说明

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Consistent with the APPS results, metaphorical skills achieve higher steering success than literal skills in both per-sample and per-task evaluations, with the severity distribution shifting towards more severe outcomes.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen 表示层分析：Metaphor 对比 Benign 与 Neutral Distractor

<div class="result-value" markdown="1">

Metaphor 在所有分析层均产生更大的目标行为对齐变化；第 37 层平均 $\Delta_{\mathrm{align}}$ 最大，为 0.144，而 Benign 和 Neutral Distractor 分别为 0.028 和 0.046。以该分数区分隐喻与控制样本时，各层 AUC 为 0.8375 至 0.9496，最高值 0.9496 出现在第 32 层。

</div>

加入隐喻后，隐藏表示不仅一般性地发生变化，而且更靠近由低效率过程描述构造的行为原型，并能在单样本层面较好地区分隐喻条件与控制条件。中层和中后层最明显，暗示过程信息可能在生成最终代码之前形成。它仍是相关性证据：行为原型由研究者构造，较高对齐与 AUC 不能单独证明该表示方向就是导致低效率代码的因果通道。

<div class="result-source" markdown="1">

来源：第 4.2 节，表 3、表 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At this layer, Metaphor has a mean alignment score of 0.144, compared with 0.028 for Benign and 0.046 for Neutral Distractor sets. As shown in Table 3, Δalign separates metaphorical skills from controls across all evaluated layers, with AUC values ranging from 0.8375 to 0.9496. The strongest separability appears at layer 32, where AUC reaches 0.9496.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 行为评估依赖预筛任务和迭代式技能搜索，但原文未明确报告筛选后题量、每题候选数、搜索预算、采样次数、代码正确率保留情况及置信区间；又因未报告 no-skill 结果表，读者无法直接量化搜索前后的绝对风险或排除筛选偏差。per-task 成功率和每题最高严重度尤其更接近“找到至少一个有效攻击”的最坏情形，而非平均部署概率。
- 过程迁移证据并不完全一致：人工审计中 Gemma、Qwen、DeepSeek 的 PCA-supported consistency 分别为 90.9%、78.4%、21.9%，DeepSeek 的低一致性说明部分成功案例可能来自其他提示效应。表示层分析又只覆盖 Qwen、90 道题和研究者构造的行为原型，没有通过激活干预证明因果性，也未验证相同表示规律能否跨模型、跨 BIRD-SQL 或跨未搜索的新隐喻泛化。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Literal Skill Steering：直接描述实现偏好或过程偏置，但不使用隐喻表示。它与隐喻条件具有相同的“试图引导模型”功能，因此可检验隐喻式过程映射是否比显式、字面的引导更有效。
- Benign 控制：提供与任务一致、但不含低效率过程诱导的指导。它用于估计仅仅增加有帮助的技能说明会造成多大的表示变化。
- Neutral Distractor 控制：加入自然的背景领域叙述，但不包含目标低效率行为。它用于区分真正的隐喻过程迁移与“任何额外背景框架都会扰动表示”的一般效应。
- 任务单独提示：同一道题不附加技能时的表示 $h_Q^l$，是表示层分析的样本内参照。论文没有在行为结果表中报告独立的 no-skill 基线，因为题目已预筛为无技能时能稳定产生正确高效解法；因此它主要承担筛选标准和表示差分参照，而不是完整的结果基线。

**实验想回答的问题**

- 在原始任务不变、且模型默认能够稳定生成正确高效解法的条件下，隐含低效率过程模式的隐喻技能，是否比直接说明实现偏好的字面技能更容易把代码生成模型引向低效率算法？这种影响能否跨模型、跨代码生成与文本转 SQL 任务出现？
- 成功转向是否源于隐喻源场景中的“过程模式迁移”，而不只是一般性的提示扰动？具体检验包括：生成代码是否复现隐喻暗示的过程，以及加入隐喻后模型隐藏表示是否更接近相应的低效率行为原型。

**实验实现**

行为实验使用 Qwen-Coder-Next 80B、DeepSeek-Coder-33B-Instruct 和 Gemma-4-31B，统一采用温度 $0.20$、top-$p=0.95$ 的生成设置。为节省成本，作者主要用 Qwen 进行迭代式 agentic skill search，再把学得的技能迁移到另外两种模型；候选技能必须自然、与任务相关，并隐含目标过程，凡是明确暴露目标算法策略的候选都会被丢弃。各模型子实验在可能情况下使用相同搜索预算与评估协议，但原文未给出具体预算、每题采样次数、随机种子或置信区间。表示层实验只分析 Qwen 的第 16、24、32、37、41 层：对同题分别输入 task-only 与 skill-task 提示，并用若干目标行为的短自然语言描述的隐藏表示均值构造行为原型。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 控制提示内容：Metaphor、Neutral Distractor 与 Benign 在 Qwen 第 37 层的配对比较 | Metaphor 的平均 $\Delta_{\mathrm{align}}=0.144$，比 Benign 高 0.116，效应量 Cohen's $d=2.24$、Mann–Whitney $p=1.28\times10^{-26}$；比 Neutral Distractor 高 0.098，$d=1.88$、$p=2.76\times10^{-20}$。Neutral Distractor 自身也由 Benign 的 0.028 上升到 0.046。 | 这项控制隔离了三种可能来源：仅增加正常指导、仅增加背景领域框架，以及加入带有目标过程映射的隐喻。中性背景相对正常指导仍有弱移动，说明额外叙事本身不是完全无效；但隐喻的增量远大于该一般扰动，支持“过程内容”而非“提示更长或换了背景”是主要关联因素。统计显著性很强，但样本由相同 90 道题构成，且原文没有说明多重检验校正，不能据此推断跨数据集的效应大小。 | 第 4.2 节，表 4<br><span class="experiment-evidence">At layer 37, Metaphor exceeds Benign by 0.116 in mean Δalign (Cohen’s d=2.24, Mann–Whitney p=1.28×10−26), and exceeds Neutral Distractor by 0.098 (d=1.88, p=2.76×10−20). Neutral Distractor also shows a significant shift relative to Benign (0.046 vs. 0.028), suggesting that background-domain framing can introduce weak procedural activation.</span> |
| 层位消融：Qwen 第 16、24、32、37、41 层的行为对齐与可分性 | Metaphor 的平均 $\Delta_{\mathrm{align}}$ 从第 16 层的 0.034 上升，在第 24、32 层均为 0.080，第 37 层达到 0.144，随后第 41 层为 0.125；AUC 则在第 32 层达到最高 0.9496，而不是在平均移动最大的第 37 层。 | 跨层比较用于判断信号是否只在最终层临时出现。结果显示信号从较早层即可观察，并在中后层增强，支持隐喻过程逐步进入内部表示的解释。第 32 层分类最好、第 37 层平均移动最大，说明“组均值移动幅度”与“逐样本可分性”并非同一性质；这也不能确定生成算法选择的真正因果层，因为实验没有在这些层上执行干预。 | 表 3：各行依次为 Layer、Benign、Neutral distractor、Metaphor、AUC<br><span class="experiment-evidence">16 \| -0.020 \| -0.015 \| 0.034 \| 0.8895; 24 \| -0.014 \| -0.009 \| 0.080 \| 0.8375; 32 \| -0.004 \| 0.020 \| 0.080 \| 0.9496; 37 \| 0.028 \| 0.046 \| 0.144 \| 0.9296; 41 \| 0.017 \| 0.029 \| 0.125 \| 0.9001</span> |

**定性案例**

- 图 3 将第 32 层的 270 个技能—任务样本画成以行为原型为中心的径向移动：空心圆表示 task-only，实心三角表示加入技能后的位置，半径越小代表与低效率行为原型越接近。Metaphor 样本呈系统性向内移动，Neutral Distractor 移动较弱，Benign 几乎没有一致方向。该可视化直观支持组均值与 AUC 结果，但它是总体定性图，而不是对某一道题、某段代码及其复杂度变化的逐例因果分析。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work studies procedural transfer and algorithmic steering in LLM code generation, directly targeting coding reasoning.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`e22f3d107ad8696e393e940865f892e7f4d3781c7d3b01563e2e03367a41821a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
