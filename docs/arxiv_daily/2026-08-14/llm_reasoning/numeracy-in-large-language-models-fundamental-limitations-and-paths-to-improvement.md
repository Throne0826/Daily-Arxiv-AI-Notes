---
title: "[论文解读] Numeracy in Large Language Models: Fundamental Limitations and Paths to Improvement"
description: "[arXiv 2608.13129][LLM Reasoning] 本文将大模型的基础数值能力与高层数学推理区分开来，提出数值基础框架（NGF），以表征基础（$RG$）和程序基础（$PG$）统一解释数值错误、结构成因、改进方法及部署选择。"
arxiv_id: "2608.13129"
announcement_date: "2026-08-14"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T02:58:54.633822+00:00"
source_sha256: "852dc6b56b02d6b5abdcf69535abb3b07d3921c987dea924588fea09b063575c"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "LLM 其他"
  - "大语言模型"
  - "基础数值理解"
  - "数值扎根框架"
  - "表征扎根"
  - "程序扎根"
  - "数字分词"
  - "长度泛化"
  - "数学推理可靠性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.13129</p>

# Numeracy in Large Language Models: Fundamental Limitations and Paths to Improvement

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Aoxin Ni</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Department of Computer Science；Affiliation: University of Chinese Academy of Sciences</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13129v1) · [PDF 下载](https://arxiv.org/pdf/2608.13129v1) · **关键词** 大语言模型, 基础数值理解, 数值扎根框架, 表征扎根, 程序扎根, 数字分词, 长度泛化, 数学推理可靠性<br>


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

本文将大模型的基础数值能力与高层数学推理区分开来，提出数值基础框架（NGF），以表征基础（$RG$）和程序基础（$PG$）统一解释数值错误、结构成因、改进方法及部署选择。

**不用术语来说**：大模型可能会解复杂的数学文字题，却仍会把 $9.11$ 判断为大于 $9.9$，或在大整数、分数和科学计数法运算中出错。这说明模型有时只是把数字当作语言片段处理，并未稳定理解数字代表的值，也不能始终按数学规则完成计算；一旦中间数值错误，后续推理即使逻辑正确，最终答案仍不可靠。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出数值基础框架（NGF），把基础数值能力分解为表征基础（$RG$）与程序基础（$PG$）：前者考察数字写法能否被正确映射到数值、大小及等价形式，后者考察模型能否忠实执行算术定义所规定的步骤。该分解为归类诊断任务、失败模式、结构原因和缓解策略提供统一视角。
- 围绕预训练模型约束整理改进路径：从头训练时可采用数字级分词、Abacus Embeddings 等结构干预；对于既有预训练模型，更现实的选择是监督微调、推理脚手架与外部工具，并据任务对 $RG$ 和 $PG$ 的要求给出部署建议。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文讨论大语言模型的基础数值理解能力，即模型能否把数字写法稳定地对应到数学数值，并依照数学定义执行运算。该问题不同于通常以 MATH、GSM8K 等题目衡量的高层数学推理：模型可能掌握解题思路，却仍会在小数大小比较、大整数加法、分数运算或科学记数法等基础步骤上出错。由于金融数据、传感器读数、时间间隔和代数系数等应用都依赖可靠的数值处理，任何中间算术错误都可能使正确的推理链得到错误结论。本文因此采用数值扎根框架，将“理解数字表示”和“正确执行运算”视为两种需要分别诊断的能力，并据此整理基准、失效原因及改进方法。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**数值能力（numeracy / number sense）**

指模型识别数字所表示的量、比较大小、转换等价写法并完成基础运算的能力。本文强调它不是笼统的数学解题能力，而是高层推理得以可靠运行的基础。

</div>
<div class="concept-item" markdown="1">

**数值扎根（numerical grounding）**

指模型能够把数字字符串或词元与其数学数值建立稳定联系，并按照运算定义操纵这些数值。若模型主要把数字当作普通语义词元处理，就可能受数字写法、分词方式或长度变化干扰。

</div>
<div class="concept-item" markdown="1">

**子词分词（BPE tokenization）**

BPE 将输入切分为训练语料中常见的子词单元，数字也可能被不一致地切成单个数字、若干位数字或完整字符串。不同切分会破坏位值和数字对齐关系，因此可能影响数值表示及跨长度泛化。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是接收文本输入并生成文本输出的预训练大语言模型。输入可包含整数、小数、分数、科学记数法或文字题中的数值；输出则是大小关系、等价表示、运算中间步骤或最终数值。本文不把正确率下降一概归因于“推理不足”，而是用数值扎根框架区分两类问题：表征扎根要求模型从数字表面形式恢复数值、数量级及格式间的等价关系，程序扎根要求模型依照加减乘除等运算的数学定义执行步骤。该设置还区分可在预训练前修改词元化或位置表示的模型，与只能通过监督微调、推理脚手架或外部工具改善的既有预训练模型；后者的兼容性是评估缓解方法时的重要现实约束。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathrm{NGF}$**

Numerical Grounding Framework，数值扎根框架，是本文组织数值能力、失效模式和缓解策略的总体分析框架。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{RG}$**

Representational Grounding，表征扎根，表示将数字表面形式映射到数值、大小及等价表示的能力。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{PG}$**

Procedural Grounding，程序扎根，表示按照数学定义忠实执行算术过程的能力。

</div>

</div>

**直接相关的工作**

- **Ahn et al. (2024)**: 该综述系统讨论思维链、工具使用和数学基准，但重点是高层数学解题，没有专门分析基础数值错误的结构性原因，也未采用表征扎根与程序扎根的区分。本文据此补足“数学推理表现较强但基础数值处理仍不可靠”这一独立问题。
- **Nogueira et al. (2021)**: 该研究在简单算术任务上揭示了 Transformer 的长度泛化失败和分词敏感性，为本文将词元化视为数值表征障碍提供了直接依据。本文进一步把这类现象归入表征扎根或程序扎根失效，并强调某些分词与架构改动只适用于从头训练模型。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

金融、工程、医学、科学分析和智能体任务都依赖对金额、测量值、时间、单位及公式的准确处理。复杂推理建立在基础数值操作之上，因此模型若误读数量、丢失精度或算错中间结果，就会形成“最弱环节”：语言解释和推理链看似合理，最终决策却可能因一个初等数值错误而失效，尤其不适合直接承担安全关键计算。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **训练期的数值表示与结构改造**：通过数字级或固定跨度分词、xVal、Little-Endian 训练、Abacus Embeddings、BitTokens 等设计，使数字切分更一致，或显式编码位值和计算位置，从输入表示或模型结构上增强 $RG$ 与 $PG$。
- **预训练后的数据与推理期补偿**：利用数值样例监督微调、课程学习和过程奖励改善模型行为，或在推理时采用思维链、自一致性及 PAL 等工具调用，让模型显式拆解步骤，或者把确定性计算交给代码解释器执行。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 高层数学基准主要检验组织和遵循逻辑推理的能力，无法保证模型已掌握数字到数值的稳定映射以及可靠的算术原语；因此优秀的综合分数可能掩盖大小比较、格式转换和基础计算中的系统性错误，也难以判断问题究竟来自 $RG$ 还是 $PG$。
- 结构性方案通常需要修改分词器、词表、嵌入或解码头，并从头训练模型，难以用于现成的大型预训练系统；监督微调又可能只在训练所覆盖的数值范围和格式内有效，而思维链与外部工具主要补偿 $PG$，仍依赖模型先正确提取数字、单位并构造方程，不能自动消除输入层的 $RG$ 错误。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究分别报告分词、位置编码、嵌入几何、训练数据、推理策略和工具调用对数值表现的影响，但缺少一个能够区分“没有正确理解数字表示”与“没有正确执行运算程序”的统一分析框架。由此，基准所测能力、失败根因和干预手段之间难以形成可比较的对应关系，也缺少在不可重训模型这一现实约束下选择方案的系统依据。

</div>
<div markdown="1"><span>核心问题</span>

如何用统一且可操作的框架刻画大模型的基础数值能力，区分并诊断 $RG$ 与 $PG$ 失败，进而解释不同结构和训练因素造成的错误，并判断从头训练与既有预训练模型分别适合哪些改进和部署策略？

</div>
<div markdown="1"><span>作者直觉</span>

一个数字任务要成功，模型必须先“读对”，再“算对”：若 $9.11$ 的字符形式没有被稳定映射到正确数值关系，增加推理步骤也无法从根本上修复；若数字已被正确理解而运算步骤不可靠，则显式推理、过程监督或计算工具可能有效。把这两层拆开后，就能按故障所在层选择干预，而不是把所有错误笼统归因于数学推理不足。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文是一篇结构化叙事综述，并辅以由“数值基础框架”（Numerical Grounding Framework, NGF）指导的协调评测；它不是提出一个需要训练的新模型。方法的核心是把大语言模型的基础数值能力拆成两个互补维度：表征基础（RG）要求模型将数字的表面写法映射到保持数值大小、顺序和格式等价性的内部表示；程序基础（PG）要求模型按照运算的数学定义执行过程，并能推广到训练分布之外的位数或数量级。作者用这一划分统一整理诊断任务、系统性错误、结构根因和缓解策略，并提出可检验的预测，例如推理脚手架应当主要改善PG，而不同分词器可能形成不同的RG盲点。

端到端来看，作者先从指定文献渠道筛选直接研究语言模型数值原语的工作，再按NGF标注任务与证据，继而将失败模式归入RG、PG或二者，并用Number Cookbook、NumericBench和GSM-Symbolic覆盖原子数值操作、自然语言上下文数值处理及符号化变体推理。直观地说，RG检查模型是否真正“认得同一个数的不同写法、知道谁大谁小”，PG检查模型是否真正“会按步骤算，而且数字变长后仍会算”；这种拆分避免用综合数学题的单一正确率掩盖底层数值缺陷。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 文献检索与范围筛选

作者从NumericBench、Number Cookbook、GSM-Symbolic和GSM-Ranges开展前向与后向引文追踪，同时检索arXiv的cs.CL与cs.LG分类并定向审阅主要会议论文。纯符号数学、没有语言模型成分的视觉语言数值研究，以及不分析数值原语的下游推理工作被排除。

<div class="method-step__io" markdown="1">

**输入**：2024至2025年的四项主要诊断基准论文，以及arXiv和NeurIPS、ICLR、ICML、ACL、EMNLP在2021至2025年发表的相关研究。<br>
**输出**：一个聚焦自回归语言模型基础数值能力、诊断基准、结构原因和缓解方法的综述文献集合。

</div>

**直观理解**：这一步先规定“哪些证据算数”：只保留能揭示模型是否理解和操作数字本身的研究，避免把一般数学推理或视觉计数混入分析。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### NGF能力分解与任务标注

作者依据NGF判断每项任务主要考查RG还是PG：识别、抽取、格式转换、大小比较、排序和上下文检索主要归入RG；四则运算、超长度运算与数字位操作主要归入PG。对同时涉及语义识别和运算执行的现象，则结合两个维度解释。

<div class="method-step__io" markdown="1">

**输入**：筛选后的研究、诊断任务，以及整数、小数、分数、科学计数法等数字表面形式。<br>
**输出**：带有RG或PG标注的数值任务分类体系，以及跨论文可比较的分析坐标。

</div>

**直观理解**：这相当于把“不会做数值题”拆成两个问题：模型究竟是没读懂数字，还是读懂了却没有正确执行算法。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 失败模式与结构根因映射

作者将脆弱性和分词伪影主要映射为RG失败，将长度泛化和算法不对称主要映射为PG失败，并据此关联分词、位置编码、嵌入几何与预训练数据分布等潜在根因。该映射还用于预测不同干预手段应改善哪一类能力。

<div class="method-step__io" markdown="1">

**输入**：各诊断基准揭示的错误案例、模型随数字格式或长度变化的性能规律，以及分词和位置编码方面的研究证据。<br>
**输出**：由“任务类别—失败模式—基础类型—结构原因—缓解策略”构成的解释链。

</div>

**直观理解**：例如把$9.11$误判为大于$9.9$，首先说明数字写法没有稳定映射到真实大小；而学会$N$位加法却在$N+1$位上崩溃，则说明算法没有真正推广。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 跨基准协调评测

作者在统一的NGF视角下比较原子数值能力、上下文中的数值定位与操作，以及借助推理过程完成数值任务的能力，并观察不同模型在RG密集型和PG密集型任务上的强弱轮廓。评测用于检验RG与PG是否表现出可分离性，以及推理辅助是否更偏向改善程序执行。

<div class="method-step__io" markdown="1">

**输入**：三类前沿模型家族，以及Number Cookbook、NumericBench和GSM-Symbolic中的原子任务、上下文任务与符号化变体。<br>
**输出**：跨模型、跨任务生态的数值能力剖面，以及对NGF预测的经验检验。

</div>

**直观理解**：三个基准像三种体检：Number Cookbook单独检查基础动作，NumericBench检查数字放进真实文本后还能否处理，GSM-Symbolic检查换数字或加入干扰后解题是否稳定。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文属于综述与诊断性协调评测，没有提出需要通过损失函数优化的新模型，也没有给出中心训练目标；NGF是分析和标注框架，而非可微优化目标。作者讨论的监督微调、架构改造和外部工具属于被综述的缓解路径，不能视为本文自身的统一训练过程。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 表征基础（RG）**

RG要求数字表面形式到内部表示的映射保持三项性质：按真实数值排序、表达数值大小，以及识别不同格式的等价性，例如$0.5\equiv\frac{1}{2}\equiv5\times10^{-1}\equiv50\%$。它主要覆盖识别、抽取、格式转换、比较、排序和上下文检索，并用于解释表面数字替换、无关数字干扰及非数学分词造成的错误。

> 直观理解：RG回答“模型是否知道这些符号代表多少”。即使数字被写成小数、分数、科学计数法或百分数，模型也应把它们看成同一数量，而不能按词元编号或字符串外观猜大小。

**2. 程序基础（PG）**

PG要求模型输出符合运算数学定义，并在操作数长度或数量级超出训练样本时继续正确执行。它主要覆盖四则运算、模运算、数字位访问和长度泛化，用于诊断负号遗漏、除法困难以及从$N$位到$N+1$位输入时的性能断崖。

> 直观理解：PG回答“模型是否真的会执行算法”。模型偶尔答对常见算式不够，它还应在数字变长或组合变化后保持同样的步骤和规则。

**3. 诊断基准组合**

Number Cookbook将整数、浮点数、分数和科学计数法上的17类原子任务细分开来，便于定位具体结构缺陷；NumericBench把数字嵌入自然语言与真实数据，重点测试上下文RG；GSM-Symbolic通过替换题中数值测试脆弱性，并以GSM-NoOp加入无关数值测试抗干扰能力。作者强调单一基准不足以覆盖数值基础，且原子任务表现不能可靠预测上下文任务表现。

> 直观理解：这三个模块分别检查“单项基本功”“文本里找数并用数”和“题目稍作变化后是否仍稳定”。组合使用能够区分真正的数值能力与模板记忆。

**训练与推理**

本文自身不执行新的模型训练。综述阶段按照结构化叙事方法检索和筛选文献，再使用NGF对任务、失败、根因与干预进行一致标注；评测阶段在推理时向三个前沿模型家族提供Number Cookbook、NumericBench和GSM-Symbolic的任务输入，收集其预测或解题输出，并按任务所属的RG或PG维度比较表现。原子设置用于尽量隔离单项数值原语，上下文设置用于检查自然语言中的数字识别与操作，推理辅助设置用于判断显式推理脚手架是否主要弥补PG；所给章节未明确报告具体提示模板、解码参数、重复次数或评分程序。

**复现信息**

复现或公平解释该方法时，关键不是一般生成参数，而是维持任务覆盖和分析边界：文献范围包括2021至2025年的指定会议及arXiv的cs.CL、cs.LG，并排除不研究语言模型数值原语的工作；评测至少应同时覆盖Number Cookbook的四种数值表示与17类原子任务、NumericBench的上下文数值任务，以及GSM-Symbolic的数值替换和GSM-NoOp干扰设置。还应分别报告RG密集型与PG密集型任务，不能用GSM8K或MATH等综合基准的总体正确率替代底层诊断。所给原文未明确报告三个模型家族的具体型号、推理配置、抽样策略、运行环境或代码实现，因此这些细节需要回查完整论文后才能复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Number Cookbook：覆盖全部44种“任务—数值表示”组合，并划分为RG任务组与PG任务组。RG组包括大小比较、格式转换、有效数字舍入、数字计数和数长判断；PG组包括算术、逐位运算和数位提取。测试输入按操作数长度分为分布内与分布外两部分，用于检验基础数值能力及长度泛化。
- NumericBench：抽取算术、情境算术、不同位数算术、数值列表理解和数字—字符串混合提取等子集。它把数值操作嵌入文本或列表，用于判断孤立原语能力是否能迁移到更自然的情境。
- GSM-Symbolic：评测主测试集和添加无关从句的变体，并通过替换题目中的数值考察模型对同一题型模板的稳定性。其作用不是单纯测算术，而是检验模型是否会因数值变化或额外语言信息而失效。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**精确匹配准确率**

预测答案必须与标准答案完全一致，用于衡量模型是否最终算对。该指标对单个数字错误也判错，因此适合检验完整RG或PG能力，但不能显示错误答案中保留了多少正确的逐位结构。 （越高越好，因为更高表示完整正确答案所占比例更大。）

</div>
<div class="metric-item" markdown="1">

**数字匹配准确率**

衡量预测结果中的数字与目标结果在逐位层面的一致程度。它用于揭示最终答案错误时是否仍保留部分程序结构，例如若干数位计算正确；该指标只在原文明确报告的模型上使用。 （越高越好，因为更高表示输出与目标具有更多正确的数字级结构，但不代表整个答案正确。）

</div>
<div class="metric-item" markdown="1">

**每请求令牌用量**

分别记录输入、内部思考、输出和总令牌数，用于衡量提高准确率所付出的推理成本。它与准确率共同构成效果—成本权衡，而不是能力质量指标本身。 （在准确率相当时越低越好，因为令牌更少通常意味着更低的延迟和推理成本；不能脱离准确率单独比较。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Number Cookbook上的分布内与分布外长度泛化

<div class="result-value" markdown="1">

所有配置从分布内转向分布外时，精确匹配准确率均下降：GPT-5.4为76.6降至40.2，Claude Opus 4.6为82.2降至50.0，Gemini 3 MINIMAL为92.5降至63.4；Gemini 3 HIGH下降较小，为86.4降至85.0。作者进一步报告，各配置中RG均高于PG，平均RG—PG差距在分布内约为0.19、分布外约为0.27。

</div>

结果支持两个相互关联的判断：数值能力不是单一能力，而且把已掌握的运算扩展到更长操作数尤其困难。数字匹配高于精确匹配还说明，模型即使最终答错，也可能执行了部分正确步骤。Gemini HIGH的表现表明额外推理能缓解部分长度泛化失败；但这只是模型与配置间的描述性比较，不能证明长度退化完全由PG机制、训练分布或某一种架构因素造成。

<div class="result-source" markdown="1">

来源：第5.3节，表2及图5—6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The main dissociation result is robust: every model configuration shows higher RG than PG, with an average RG–PG gap of approximately 0.19 in domain and 0.27 out of domain.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### NumericBench情境数值推理与Number Cookbook原子任务的跨基准比较

<div class="result-value" markdown="1">

模型排名发生反转：GPT-5.4虽然在Number Cookbook精确匹配上弱于Gemini 3 MINIMAL，却在NumericBench的Arithmetic、Context arithmetic和Different-digit arithmetic子集上分别达到84.2、84.8和78.8，均高于其余配置。Num list 100子集上，GPT-5.4为98.3，Claude Opus 4.6为33.9，Gemini MINIMAL和HIGH分别为66.3与69.2。

</div>

原子任务做得好，并不保证模型能在自然语言中找出相关数量、理解题意并调用相应运算。分析上，这提示RG和PG之外还存在“情境部署”环节：模型必须先把文本中的量映射到正确操作。该排名反转证明的是跨任务迁移不充分，而不是GPT-5.4具有普遍更强的数学能力，也不能排除提示适配或训练数据覆盖差异。

<div class="result-source" markdown="1">

来源：第5.6节，表4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The ranking inverts relative to Number Cookbook: GPT-5.4 leads in contextual arithmetic despite weaker atomic Number Cookbook performance.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### GSM-Symbolic主集与添加从句变体

<div class="result-value" markdown="1">

在主集上，GPT-5.4、Claude Opus 4.6、Gemini MINIMAL和Gemini HIGH的准确率分别为96.8、75.7、26.4和78.2；在P1 added clause变体上分别为94.3、85.5、10.5和56.3。GPT-5.4在两种设置下均保持较高准确率，而Gemini MINIMAL在添加从句后进一步下降。

</div>

该实验检验同一类符号化应用题在数值替换和附加语言成分下是否稳定。GPT-5.4的结果表明其原子数值成绩较弱并未阻止其在文字题中取得更强表现；Gemini MINIMAL则表现出原子能力较强、情境调用较弱的相反模式。不过这里只有两个汇总设置，不能据此判断错误究竟来自无关信息干扰、语言解析、运算执行还是具体提示格式。

<div class="result-source" markdown="1">

来源：第5.6节，表5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Main | 96.8 | 75.7 | 26.4 | 78.2
P1 added clause | 94.3 | 85.5 | 10.5 | 56.3

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验仅覆盖三个闭源前沿模型家族，且节选未报告精确模型快照、提示词、样本量、重复运行、置信区间和统计显著性。即使温度设为0，API后端变化和隐藏推理机制仍可能影响可复现性，因此小幅模型差异不宜过度解释。
- 分词器盲点和RG—PG分离主要来自跨模型、跨任务的行为相关性。由于分词器、架构、训练数据与对齐方式没有被独立控制，结果支持NGF的预测，却不能唯一确定根因；同时，作者自己指出，RG/PG尚不足以完整解释情境任务，还需加入在自然语言中选择并调用数值能力的部署维度。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- GPT-5.4：作为前沿闭源模型基线，用于比较其原子数值能力、情境解析能力和数值替换鲁棒性。
- Claude Opus 4.6：与GPT-5.4和Gemini 3具有不同的分词与训练体系，因此其比较可用于观察模型特定的RG能力轮廓；但实验不能单独证明差异由分词器导致。
- Gemini 3 MINIMAL：低推理预算配置，近似检验模型在不使用扩展内部推理时的直接作答能力，也是推理预算消融的对照条件。
- Gemini 3 HIGH：高推理预算配置；与同一Gemini 3模型的MINIMAL配置比较，可较好地隔离扩展内部推理的影响，但仍不能等同于严格控制所有服务端推理过程。

**实验想回答的问题**

- 数值表征基础（Representational Grounding，RG）与程序执行基础（Procedural Grounding，PG）能否在不同模型和输入长度下经验性分离，以及输入超出常见长度分布时，PG是否比RG退化得更严重？
- 增加内部推理预算能否主要补偿程序执行缺陷；同时，原子数值任务上的能力能否迁移到自然语言和表格中的情境数值推理？

**实验实现**

实验通过统一API代理访问GPT-5.4、Claude Opus 4.6和Gemini 3，并将温度设为0，以降低随机采样对模型比较的干扰。Gemini 3分别采用MINIMAL与HIGH两种$thinkingLevel$设置。Number Cookbook同时报告分布内、分布外的精确匹配结果；GPT-5.4与Claude还报告数字匹配结果。NumericBench按任务子集报告准确率，GSM-Symbolic评测主集和添加从句变体。原文节选未明确报告样本抽取数量、提示模板、重复运行次数、置信区间、显著性检验、评分脚本细节以及API具体版本日期，因此表中差异应视为描述性结果。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Gemini 3的MINIMAL与HIGH内部推理预算对照 | HIGH将分布外精确匹配准确率从63.4提高到85.0，即增加21.6个百分点，但分布内准确率从92.5降至86.4，即下降6.1个百分点；每请求总令牌由293增至6247，约为21.3倍。作者另报告，扩展推理对分布外PG与RG的提升分别为0.287和0.093。 | 由于比较的是同一模型的两种推理预算，该对照主要隔离扩展内部推理的效果。PG增益约为RG增益的三倍，符合“推理为多步程序提供工作记忆”的解释；同时，分布内回退表明更多推理可能引入额外错误。它没有隔离具体哪一种思维步骤有效，也没有证明高预算能修复分词或嵌入问题。更高准确率还伴随约21.3倍令牌成本，部署时必须同时考虑延迟和费用。 | 第5.4节，表3及图7<br><span class="experiment-evidence">Gemini MINIMAL \| 92.5 \| 63.4 \| 124 \| 0 \| 169 \| 293
Gemini HIGH \| 86.4 \| 85.0 \| 125 \| 6,084 \| 38 \| 6,247</span> |

**定性案例**

- 图8比较模型在各RG任务上维持至少90%精确匹配准确率的最大数字长度：Claude Opus 4.6在浮点比较上可处理更长输入，Gemini 3在数字计数和数长任务上更强，GPT-5.4则保持较强的整数比较能力。作者将其解释为不同分词器造成的表面形式可见性差异；更严格的解读是，这一模式与分词器假说相容，但由于模型的训练数据和架构也不同，不能形成独立因果证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The survey frames LLM numerical reasoning limitations and conducts coordinated diagnostic evaluations of numeracy.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`852dc6b56b02d6b5abdcf69535abb3b07d3921c987dea924588fea09b063575c`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
