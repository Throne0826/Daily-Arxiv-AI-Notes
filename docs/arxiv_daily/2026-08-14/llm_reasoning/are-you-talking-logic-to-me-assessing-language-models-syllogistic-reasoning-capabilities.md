---
title: "[论文解读] Are you Talking Logic to Me? Assessing Language Models Syllogistic Reasoning Capabilities"
description: "[arXiv 2608.12374][LLM Reasoning] 本文研究不同知识表示记法及三段论类别提示如何影响小型语言模型的三段论推理能力，旨在突破现有评测仅比较自然语言与一阶逻辑的局限。"
arxiv_id: "2608.12374"
announcement_date: "2026-08-14"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T02:53:29.043664+00:00"
source_sha256: "acf6343d8191f198449995f6bced5314248d17465192c0155643d12043a455d9"
tags:
  - "LLM Reasoning"
  - "三段论推理"
  - "知识表示"
  - "小型语言模型"
  - "神经符号推理"
  - "监督微调"
  - "零样本推理"
  - "Common Logic Grammar Construction"
  - "SEF"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.12374</p>

# Are you Talking Logic to Me? Assessing Language Models Syllogistic Reasoning Capabilities

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Hanna Abi Akl, Fabien Gandon, Catherine Faron, Pierre Monnin</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Université Côte d’Azur, Inria, CNRS, I；Data ScienceTech Institute, Paris, France</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12374v1) · [PDF 下载](https://arxiv.org/pdf/2608.12374v1) · **关键词** 三段论推理, 知识表示, 小型语言模型, 神经符号推理, 监督微调, 零样本推理, Common Logic Grammar Construction, SEF<br>
**项目页**: [https://pypi.org/project/clgc/](https://pypi.org/project/clgc/)

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

本文研究不同知识表示记法及三段论类别提示如何影响小型语言模型的三段论推理能力，旨在突破现有评测仅比较自然语言与一阶逻辑的局限。

**不用术语来说**：语言模型即使能处理复杂文本，也常在需要严格判断“结论成立、矛盾或无法确定”的三段论任务中出错；同一组逻辑事实可以用日常语言或不同形式化记法表达，但目前尚不清楚哪种表达更便于资源较少的小型模型稳定推理，也不清楚明确告知模型题目的逻辑结构类别是否有帮助。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出研究协议与开源的 Common Logic Grammar Construction（CLGC）框架，可将以一阶逻辑表示的三段论自动转换为多种形式化知识表示记法，并依据结构定义和标注三段论类别。
- 扩展 FOLIO 与 P-FOLIO，形成包含多种形式化记法的 FOLIO-KR 和 P-FOLIO-KR，并在监督微调与零样本设置下评估记法选择及类别定义提示对小型语言模型推理的影响。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于语言模型逻辑推理与知识表示交叉研究。研究对象是广义三段论推理，即模型需要根据若干事实和规则判断结论是否成立；这类任务要求抽象地组合前提，而不能只依赖表面词语关联。现有神经符号方法常把自然语言转换为一阶逻辑，以获得更明确、可解释的表达，但三段论评测主要局限于自然语言和一阶逻辑，尚未系统比较抽象程度不同的知识表示记法。本文因此以小型语言模型为对象，研究输入表示形式以及三段论类别信息是否会影响推理表现、稳健性和推理效率。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**三段论推理**

依据一组前提或规则，判断给定结论能否在逻辑上推出。本文采用广义三段论设定，覆盖多种三段论结构，而不只限于传统的两个前提加一个结论。

</div>
<div class="concept-item" markdown="1">

**知识表示（KR）记法**

用于明确表达实体、属性、关系和逻辑规则的形式语言。不同记法位于自然语言与高度符号化语言之间的不同抽象层级，可能改变模型识别逻辑结构的难度。

</div>
<div class="concept-item" markdown="1">

**监督微调与零样本推理**

监督微调（SFT）使用带标签样本继续训练模型，使其适应目标任务；零样本（ZS）则不提供该任务的训练示例，直接通过提示要求模型作答。两种设置分别检验模型学习特定表示的能力和无需训练时利用表示或类别定义的能力。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是来自扩展版 FOLIO 与 P-FOLIO 的三段论实例，并可被编码为自然语言、一阶逻辑或其他形式化知识表示，包括 CLIF、CGIF、TFLPLUS 和 CLINGO。模型需要根据实例中的前提与规则完成相应的逻辑判断；作者在监督微调和零样本两种设置下评估小型语言模型，并在部分零样本提示中加入由 SEF 方法确定的三段论类别及逻辑定义。研究所作的关键比较是：保持底层逻辑内容不变时，改变输入记法的抽象层级会如何影响推理表现与效率，以及显式提供结构类别信息能否进一步帮助模型推理。所给章节未明确说明具体输出标签集合及形式化语义假设，因此不宜据此补充。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathrm{NL}$**

自然语言表示，即以通常的人类语言陈述事实、规则和结论。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{FOL}$**

一阶逻辑表示，可使用谓词、变量和量词无歧义地描述对象及其关系。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{SFT}$**

监督微调实验设置，模型通过带标签的目标任务数据进行训练。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{ZS}$**

零样本实验设置，模型不经过目标任务示例训练而直接依据提示作答。

</div>

</div>

**直接相关的工作**

- **自然语言、一阶逻辑与定理证明器结合的混合架构**: 既有方法将自然语言三段论翻译为一阶逻辑，再借助定理证明器引导语言模型推理，说明符号表示能够为推理提供结构化基础。本文不把研究范围限定于一阶逻辑，而是比较多种知识表示记法对小型语言模型三段论推理的影响。
- **基于规则模板或思维链的语言模型推理方法**: 规则模板提示被用于提高三段论表现并控制推理偏差，思维链则通过生成中间步骤和解释支持自我修正。本文关注的是另一项输入侧变量：逻辑内容采用何种知识表示记法，以及在提示中加入三段论结构类别定义是否有帮助。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

规划、谜题求解和广义三段论等任务要求模型进行一致、可检验的抽象推理，但语言模型在这类逻辑任务上仍不可靠。与此同时，小型语言模型因计算和部署成本较低而具有实际价值，因此需要找到无需单纯扩大模型规模、而是通过更合适的输入表达与提示信息提升其推理稳健性的方法。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **自然语言三段论评测**：将前提与待判断结论直接写成自然语言，让语言模型依据文本判断结论是否可由前提推出。该方式贴近通常的语言交互，但自然语言可能包含歧义，也会把语言理解负担与逻辑推理能力混合在一起。
- **基于一阶逻辑的神经符号方法**：先用一阶逻辑等符号形式明确表示对象、谓词、量词及其关系，再由语言模型处理这些结构化输入。相较自然语言，一阶逻辑通常更明确且可解释，已有研究表明这种表示对中小型模型的推理表现具有潜在帮助。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有三段论数据集可能在人类参与程度、规模、多样性或泛化能力方面不足，导致评测难以充分覆盖广义三段论结构，也难以判断模型是否真正获得了可迁移的推理能力。
- 既有研究主要在自然语言与一阶逻辑两端评估三段论推理，未系统考察抽象程度介于二者之间或具有不同语法结构的其他知识表示语言；同时也很少把三段论结构类别作为提示元数据，因此无法分辨模型表现变化究竟如何受表示形式与结构先验影响。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一个统一且可自动化的实验框架，把同一批三段论转换为多种知识表示记法、按逻辑结构进行分类，并在可比条件下检验这些因素对小型语言模型的影响。因而，形式化程度如何改变推理效果，以及类别知识能否作为有效的结构先验，仍未得到系统回答。

</div>
<div markdown="1"><span>核心问题</span>

本文集中回答两个问题：第一，不同形式化输入记法如何影响小型语言模型的三段论推理；第二，将三段论归入预定义类别并在提示中提供相应类别信息，是否以及如何改变模型的推理能力。

</div>
<div markdown="1"><span>作者直觉</span>

输入记法决定模型看到的逻辑结构是否清晰以及需要处理多少语言歧义：更形式化的表达可能让量词和关系更显式，而较接近自然语言的表达可能更符合模型既有的语言模式。进一步提供三段论类别及其逻辑定义，相当于先告诉模型当前题目属于哪一种结构模板，从而缩小需要自行识别的推理模式范围；但这种帮助预计会随记法和模型而变化，而非对所有设置都同样有效。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把“知识表示形式是否影响小语言模型的三段论推理”转化为一条可重复执行的流水线。首先以一阶逻辑（FOL）版本的三段论为规范化输入，通过作者提出的 Common Logic Grammar Construction（CLGC）框架解析其抽象语法树（AST），再按照目标知识表示语言的 BNF 文法生成语义等价的 CLIF、CGIF、CLINGO、TFLPLUS 与 MINIFOL 变体。随后，方法使用 Syllogism Evaluation Framework（SEF）依据三段论的逻辑结构进行分类，并把类别定义作为附加提示信息；最终分别在监督微调（SFT）和零样本（ZS）设置中，让小语言模型预测结论的真值标签，从而分离考察表示法、模型和提示元数据的影响。

从直观上看，论文没有改变每道逻辑题所表达的事实与规则，而是把同一道题改写成多种“逻辑语言”，比较模型究竟更擅长阅读自然语言、常见逻辑符号，还是更紧凑的抽象记法。CLGC负责保证改写过程系统且可复现，SEF则相当于向模型补充“这属于哪类推理、该类推理是什么意思”的解题提示；SFT检验模型学习一种表示法之后的能力，ZS检验模型仅依赖预训练知识和即时提示时的能力。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 规范化三段论并选择目标表示法

以 FOL 作为中间规范表示，并依据冗长度、预训练中可能出现的频率、抽象程度和文法有限性四项标准选择目标表示法；其中“有限性”是硬约束，即目标语言必须具有有限词汇表和可定义的文法。

<div class="method-step__io" markdown="1">

**输入**：FOLIO 与 P-FOLIO 中可表示为一阶逻辑的前提、规则、查询以及对应真值标签。<br>
**输出**：待转换的 FOL 三段论，以及 CLIF、CGIF、CLINGO、TFLPLUS、MINIFOL 系列或自然语言等实验表示配置。

</div>

**直观理解**：先把不同来源的题目统一成一种结构清楚的逻辑底稿，再决定要把底稿翻译成哪些语言。四项标准使实验能够比较“写法长短、符号熟悉度和抽象程度”是否会改变模型表现。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 通过 CLGC 生成语义等价表示

CLGC先依据 FOL 的 Backus-Naur Form（BNF）文法把输入解析为抽象语法树（AST），再将该树映射为目标表示法中的等价语法树；最后由解析器按目标语言的空格、括号和运算符规则重建文本。

<div class="method-step__io" markdown="1">

**输入**：FOL 三段论、FOL 的 BNF 文法，以及人工实现的目标表示法 BNF 文法与排版规则。<br>
**输出**：与原 FOL 输入保持逻辑含义一致、但表面语法不同的多表示法三段论。

</div>

**直观理解**：AST保留“量词作用于什么、哪些命题由什么连接词组合”等结构，因此转换不是简单替换字符串。它类似先把句子拆成结构图，再按另一种语言的语法从结构图重新写出来。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造 MINIFOL 对照表示并扩展数据集

方法构造若干轻量 FOL 变体，以控制较小的语法变化：MINIFOL将若干 FOL 运算符替换为常见字符串，MINIFOL2进一步消除存在量词，MINIFOL3把否定改写为“not”，MINIFOL4把合取改写为逗号；生成结果与其他 KR 表示共同加入 FOLIO-KR 和 P-FOLIO-KR。

<div class="method-step__io" markdown="1">

**输入**：标准 FOL 表示及其逻辑运算符。<br>
**输出**：同一道三段论的 NL、FOL、CLIF、CGIF、CLINGO、TFLPLUS 与 MINIFOL 系列表达，以及可用于训练和测试的扩展数据集。

</div>

**直观理解**：这些变体是受控对照：它们尽量不改变逻辑结构，只改变模型看到的符号。由此可以判断性能变化更可能来自表示形式，而不是题目内容本身。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 使用 SEF 分类并构造两种零样本场景

SEF按照三段论结构将样本归入 categorical、hypothetical、disjunctive 或 complex 类别，并为类别提供逻辑描述；ZS场景 S1只要求模型根据给定三段论从候选标签中预测真值，S2则在提示中进一步加入SEF类别定义。

<div class="method-step__io" markdown="1">

**输入**：已转换的三段论及其逻辑结构。<br>
**输出**：带有SEF类别元数据的样本，以及用于比较“无类别描述”和“有类别描述”的 S1、S2 提示。

</div>

**直观理解**：S1相当于直接给题，S2则额外告诉模型题型及其逻辑含义。两者之差用于检验结构提示究竟帮助推理，还是因增加上下文和陌生符号而干扰模型。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：论文节选未给出新的损失函数，也未明确写出SFT采用的具体优化目标公式。按文中任务定义，SFT把三段论表示作为输入、真值标签作为目标输出，对Flan-T5进行监督式序列生成训练；因此其核心优化意图是提高正确标签的条件生成概率，但具体损失形式、标签序列编码和优化器配置不能由所给原文确认。ZS不进行目标数据上的参数优化，只比较不同输入表示以及是否加入SEF描述时的预测。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Common Logic Grammar Construction（CLGC）**

CLGC是基于文法的三段论表示转换框架：源端使用FOL的BNF文法建立AST，目标端使用作者为各表示法人工实现的BNF文法建立等价树，再由解析器应用目标表示法特有的括号、空格和符号规则。当前覆盖Common Logic家族中的CLIF与CGIF、Plus-Minus Algebra家族中的TFLPLUS、Answer Set Programming家族中的CLINGO，以及MINIFOL变体。

> 直观理解：该模块是实验的控制基础：只有先尽量保证不同写法表达同一逻辑内容，才能把性能差异合理地归因于表示法。公开Python包还使新表示法和新三段论可以沿同一转换流程加入实验。

**2. MINIFOL 受控表示族**

MINIFOL通过把FOL中的全称量词、异或、蕴含、否定、存在量词、合取和析取等符号替换为较常见的字符串，建立介于标准FOL与更轻量符号语言之间的表示；MINIFOL2、MINIFOL3和MINIFOL4分别继续控制存在量词、否定词和合取符号的形式。它被用作研究模型对符号频率和细微语法变化敏感性的基线，而不是新的推理算法。

> 直观理解：若只比较自然语言和完全不同的逻辑语言，很难知道差异来自哪里；MINIFOL像逐项修改界面的对照实验，让研究者观察替换某类符号后模型是否更容易读懂题目。

**3. Syllogism Evaluation Framework（SEF）**

SEF依据三段论结构给样本分配 categorical、hypothetical、disjunctive 或 complex 类别，并把相应类别的逻辑定义加入ZS提示。其作用不是替模型执行证明，而是提供显式的结构先验，以便比较S1基础提示与S2增强提示。

> 直观理解：SEF把题目先标成类别，再向模型解释这一类别通常由什么逻辑关系构成。这样可以直接检验“告诉模型题型”是否足以改善推理，同时也能发现某些模型或表示法可能因额外描述而受到干扰。

**训练与推理**

SFT阶段使用冻结的数据划分分别训练Flan-T5-small与Flan-T5-large。每个样本以某一种表示法或论文指定的表示组合呈现，模型读取前提、规则与待判断结论并输出真值类别；训练完成后在对应测试划分上推理。该设计将表示法作为主要自变量，但论文结果也表明其效果需要结合模型规模和数据集解释，不能假定某一种表示对所有模型都最优。

ZS阶段不在FOLIO-KR或P-FOLIO-KR上微调Gemma、Llama和Phi，而是向模型提供三段论、逻辑推理指令和候选标签。S1提供基础任务提示，S2在此基础上加入SEF类别定义；随后解析模型生成的标签。论文以F1处理类别不平衡，并以$AG_{F1}=F1_{\mathrm{S2}}-F1_{\mathrm{S1}}$描述加入SEF信息后的变化，但该式属于实验比较指标而非模型训练目标，因此未列入中央方法方程。

**复现信息**

CLGC依赖FOL与各目标表示法的显式BNF文法，目标文法由作者人工实现；转换还必须应用各表示法的空格、括号等语法规则，否则表面格式差异会成为额外混杂因素。数据划分被冻结，以便不同表示法共享相同样本划分。SFT采用5个epoch、batch size为4，并设置随机种子；更完整的训练参数由作者放在项目GitHub中，所给节选未逐项列出。

模型选择限制在小语言模型范围：SFT采用编码器-解码器式Flan-T5-small和Flan-T5-large，ZS采用参数量低于100亿的解码器式Gemma-2-2b-it、Llama-3.2-3b-instruct和Phi-3.5-mini-instruct。公平解释结果时需注意，各模型预训练语料并未完全公开，论文对“某种符号在预训练中更常见”以及Gemma、Llama、Phi语料特性的讨论主要是作者的合理假设，并非由受控语料审计直接证明。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- FOLIO-KR：由人工整理的 FOLIO 扩展而来，共包含 1204 个三段论；标签分布为 True 460、False 351、Unknown 393，SEF 分布为 Categorical 17、Hypothetical 67、Disjunctive 653、Complex 467。CLGC 将原始自然语言和一阶逻辑样本转换为 CLIF、CGIF、CLINGO、TFLPLUS 及多个 $\mathrm{MINIFOL}_x$ 版本，并补充 SEF 类别。SFT 使用固定的分层划分：训练集 800、验证集 201、测试集 203；其规模较大，主要用于检验模型能否从训练数据学习不同形式记法。
- P-FOLIO-KR：由人工整理的 P-FOLIO 扩展而来，共包含 301 个三段论；标签分布为 True 122、False 69、Unknown 110，SEF 分布为 Categorical 9、Hypothetical 13、Disjunctive 40、Complex 239。同样包含自然语言、一阶逻辑和 CLGC 生成的多种知识表示。SFT 的固定分层划分为训练集 144、验证集 96、测试集 61；该数据集规模较小且 Complex 类占主导，用于考察数据较少及结构分布不同条件下的记法学习与推理。
- 两个数据集中的每个样本都是由若干前提和一个结论组成的三段论，目标标签集合为 $\{\mathrm{True},\mathrm{False},\mathrm{Unknown}\}$：分别表示结论可由前提推出、与前提推理结果不符，或仅凭前提无法确定。各知识表示版本表达同一逻辑内容，因此跨记法比较主要测试表示形式对模型的影响，而不是题目语义差异。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

原文未明确报告，或这里不需要额外前置概念。

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文节选未提供任何结果表、指标定义、显著性检验、运行时间或消融数值，因而不能填写可核验的三项主要结果，也无法判断不同模型、数据集和记法上的结论是否一致。
- 从实验设置分析，SEF 类别高度不平衡：FOLIO-KR 以 Disjunctive 和 Complex 为主，P-FOLIO-KR 则有 239/301 个 Complex 样本；尤其 P-FOLIO-KR 测试集的 Categorical 数量为 0。整体指标可能掩盖稀有类别表现，而且该测试集无法评估 Categorical 类别的泛化。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 自然语言（NL）表示：这是模型预训练中通常最常见、最自然的输入形式，用来判断形式化记法能否达到具有竞争力的任务表现，同时减少输入冗余或推理开销。
- 标准一阶逻辑（FOL）表示：它是 CLGC 转换流程的源表示，也是具有量词、连接词和谓词的标准符号化参照，用于比较其他形式记法是否更容易被模型解析和学习。
- $\mathrm{MINIFOL}_x$ 系列：这些是论文刻意构造的轻量 FOL 变体，通过将部分逻辑符号替换为模型更常见的词或符号、消除存在量词，或改变否定与合取写法，作为研究细微语法变化和记法常见程度影响的对照。
- 零样本 Scenario 1：提示只提供三段论、目标记法的 BNF 语法和输出要求，不提供 SEF 类别信息。它是评估 Scenario 2 中 SEF 类别、定义和示例是否产生增益的直接提示基线。

**实验想回答的问题**

- 在监督微调（SFT）和零样本（ZS）条件下，不同知识表示记法的冗长度、常见程度与抽象程度是否会影响小语言模型对三分类三段论任务的推理表现，并在保持与自然语言相竞争的效果时提高推理效率？
- 在零样本提示中加入三段论的 SEF 类别、类别定义及示例，相比仅提供目标记法的 BNF 语法，是否能更有效地引导小语言模型完成逻辑推理？

**实验实现**

任务被实现为 True、False、Unknown 三分类。SFT 使用 Flan-T5-small 与 Flan-T5-large，在同一种记法的训练集和验证集上学习，并在省略标签的同记法测试集上预测；划分同时按真值标签和 SEF 类别分层并固定，以减少不同划分造成的比较偏差。训练进行 5 个 epoch，批大小为 4，设置随机种子，运行于 A100 GPU。ZS 使用参数量低于 100 亿的 Gemma-2-2b-it、Llama-3.2-3b-instruct 和 Phi-3.5-mini-instruct，运行于 L4 GPU：Scenario 1 提供三段论及目标记法的 BNF 语法；Scenario 2 进一步提供该题的 SEF 类别、类别定义和一个示例。模型须仅在指定标签中输出判断。所给章节没有说明采用 accuracy、macro-F1 或其他汇总指标，也没有给出解码参数或重复运行方差，因此不能据此确定具体评价口径。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 论文用同一个“患流感则患 influenza”的规则展示 FOL、CLIF、CLINGO、CGIF、MINIFOL2 和 TFLPLUS 的等价表达。该例说明实验控制的是表面语法和符号体系，而非逻辑命题本身；不过它只是记法转换示例，不构成模型正确推理或转换语义完全保持的实证结果。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The central contribution is improving and evaluating syllogistic reasoning through knowledge-representation notations and structured prompting.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`acf6343d8191f198449995f6bced5314248d17465192c0155643d12043a455d9`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
