---
title: "[论文解读] Load-Bearing Context: The Question Damage Score for Evaluating Context Reliance in Linguistic Reasoning"
description: "[arXiv 2608.27756][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.27756"
announcement_date: "2026-08-31"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:39:16.502053+00:00"
source_sha256: "51e57ba59f120f8e63b582258eb2034e160e0b163d572006f1f7c65d2b664c5b"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "LLM 机制与可解释性"
  - "大语言模型"
  - "上下文依赖"
  - "拒答评测"
  - "语言学奥林匹克谜题"
  - "Question Damage Score"
  - "单例上下文删除"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.27756</p>

# Load-Bearing Context: The Question Damage Score for Evaluating Context Reliance in Linguistic Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Neh Majmudar, Elena Filatova</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27756v1) · [PDF 下载](https://arxiv.org/pdf/2608.27756v1) · **关键词** 大语言模型, 上下文依赖, 拒答评测, 语言学奥林匹克谜题, Question Damage Score, 单例上下文删除<br>


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

本文属于大语言模型（LLM）推理分析与拒答（abstention）评测领域，关注模型是否真正依据题目提供的上下文作答，而不是依赖预训练知识、记忆或表面模式。研究采用英国语言学奥林匹克（UKLO）的 Rosetta Stone 语言谜题作为受控环境：每道题给出少量陌生语言及其英语翻译的例子，模型必须从这些例子归纳语言规则，再将规则应用于新的问题；原则上，解题所需信息都包含在题目上下文中。与删除全部上下文或直接构造不可回答问题的方法不同，本文只删除一个上下文例子，从而能够考察某个具体信息片段对问题可解性的作用。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自包含语言学谜题**

题目同时提供陌生语言的表达及其翻译，解题者需要从例子中归纳词序、词形或语法对应关系，再回答新问题。所谓自包含，是指原则上无需外部语言学知识，解答应仅由题目给出的例子推出。

</div>
<div class="concept-item" markdown="1">

**上下文依赖与拒答**

上下文依赖指模型的答案是否由当前题目提供的信息支持；若删除必要信息后，剩余上下文无法唯一确定答案，模型理应识别信息不足并拒绝作答。本文把“是否拒答”作为模型行为指标，但结构上不可解并不必然意味着模型一定会拒答。

</div>
<div class="concept-item" markdown="1">

**负载信息（load-bearing information）**

负载信息是某个上下文例子所独自承载的、回答至少一个问题所必需的结构信息。删除它后，其他例子仍保持不变，但相关问题在题目本身提供的信息范围内变得不可回答；若任意删除一个例子都不造成这种损害，则题目具有信息冗余。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究输入是一组来自 UKLO 的 53 道 Rosetta Stone 谜题；每道题包含若干语言—英语对应例子以及若干待解问题。对原题分别构造两类单例删除版本：一类均匀随机删除一个例子，另一类依据错误校正码（ECC）的思想，定向删除唯一承载某个问题必要信息的例子。输出包括删除后每个问题在结构上是否仍可由剩余上下文回答，以及三个前沿 LLM 在原题和修改题上的答案、正确性与拒答行为。基本假设是：题目设计者提供的例子足以支持原题求解，且判断删除造成的不可解性主要依据题目内部信息，而不是模型的外部知识；不过论文明确承认，语言谜题没有显式依赖树，因此这种结构判定是近似的。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D_Q$**

Question Damage Score（问题损伤分数），用于衡量删除一个上下文例子后有多少个问题变得结构上不可回答。

</div>
<div class="notation-item" markdown="1">

**$D_Q(j)$**

删除第 $j$ 个上下文例子后的问题损伤分数，即受该删除影响、因必要信息缺失而不可回答的问题数量。

</div>
<div class="notation-item" markdown="1">

**$l_j$**

题目中的第 $j$ 个上下文例子；定向删除的目标就是寻找可能具有负载作用的 $l_j$。

</div>
<div class="notation-item" markdown="1">

**$\max_j D_Q(j)$**

遍历删除每一个单独上下文例子后得到的最大损伤分数。若该值大于 $0$，题目被定义为 fragile（脆弱）；若等于 $0$，题目被定义为 robust（稳健）。

</div>

</div>

**直接相关的工作**

- **Abstain-QA、SQuAD 2.0、SelfAware**: 这些工作评估模型在没有足够信息时是否能够拒答，但通常通过构造本身不可回答的问题、移除整体支持上下文或设置无正确选项来生成测试项。本文的区别是：每个不可回答变体都由一个可回答原题删除单个例子得到，因此能够将模型行为与一个只差一条上下文信息的匹配对照项比较。
- **TreeCut**: TreeCut 在具有显式变量依赖树的算术任务中删除解题路径上的边，以制造可判定的不可回答变体。本文将类似的单点扰动思想应用于语言学谜题，但由于这类题没有现成的显式推导树，必须从表面例子近似识别负载信息；这一设置也保留了预训练记忆可能影响结果的现实问题。

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

该方法不是训练一个新的语言模型，而是构造一种用于诊断上下文依赖性的受控扰动框架。输入是英国语言学奥林匹克竞赛（UKLO）的自包含 Rosetta Stone 语言谜题：每道题包含若干上下文例句和若干待回答问题，解题所需的语言规律原则上都应能从例句中归纳出来。方法先从每道题删除一个上下文例句，生成删减版本；再用 Question Damage Score（问题损伤分数，记为 $D_Q(j)$）估计某个例句是否承载某些问题所需的唯一信息，并据此选择结构影响最大的例句进行定向删除。直观地说，研究者把例句视为“信息零件”：随机删除用于模拟普通扰动，定向删除则专门拿走最不可替代的零件，从而检验模型是否真正依赖给定上下文，而不是依赖参数记忆、猜测或语言学常识。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建并筛选自包含谜题语料

从UKLO谜题中保留能够支持单个上下文例句受控删除的任务，排除含图片上下文、需要多个情境视角或涉及两种以上语言的谜题。每道保留的谜题被表示为上下文例句集合与问题集合，并保留已验证的答案键。

<div class="method-step__io" markdown="1">

**输入**：2010年至2025年发布的UKLO Rosetta Stone谜题及其上下文例句、问题和标准答案。<br>
**输出**：53道适合单例句扰动的自包含语言推理谜题；每道谜题包含若干上下文例句和待解问题。

</div>

**直观理解**：先选择结构规整的题目，确保删掉一个例句时，改变的主要是信息供给，而不是题型、图像输入或任务定义。这样后续观察到的性能变化才更可能与上下文缺失有关。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成单例句删除版本

对每道谜题生成两个只含原上下文例句其余部分的变体：一种从例句中均匀随机选取一个删除，作为随机删除基线；另一种先计算每个例句的结构损伤，再删除损伤分数最高的例句，作为ECC启发的定向删除。

<div class="method-step__io" markdown="1">

**输入**：一道人为保留的原始谜题，以及其中的上下文例句集合。<br>
**输出**：每道原始谜题对应一个随机删除版本和一个定向删除版本，二者均比原题少一个上下文例句。

</div>

**直观理解**：随机删除相当于随手拿走一个零件，可能拿走备用件；定向删除相当于先找出最关键的零件，再故意拿走它。两种版本的比较可以区分一般删减效应与针对关键证据的删减效应。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算问题损伤分数并判定结构脆弱性

将只在一个上下文例句中出现的词元视为singleton token，并计算候选例句独有的词元数量及其被问题依赖的数量；对每道谜题删除具有最大 $D_Q(j)$ 的例句，若所有例句的最大分数为零则标记为robust，否则标记为fragile。该实现采用空格分词，因此给出的是保守的、基于词元身份和问题依赖关系的一阶估计。

<div class="method-step__io" markdown="1">

**输入**：每个例句中的空格分隔词元、每个问题需要的词元信息，以及候选被删除例句。<br>
**输出**：每个上下文例句的Base Damage Score和Question Damage Score，以及整道谜题的robust/fragile结构标签和定向删除版本。

</div>

**直观理解**：如果某个词只在一个例句出现，而且某个问题必须用到它，那么这个例句就是该问题的唯一证据来源。删掉它就像删掉说明书中唯一写有关键规则的一行；但模型仍可能凭形态规律或先验知识补回答案，所以“结构上不可解”不等于“模型必然答错”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在原题和扰动题上评估模型行为

让三个前沿大型语言模型分别回答各版本中的问题，并观察答案正确性及其是否在缺乏必要信息时弃答；随后结合LLM-as-judge分析区分明显破坏与可能仍可由形态或语用推理恢复的边界案例。

<div class="method-step__io" markdown="1">

**输入**：原始谜题、随机删除版本、定向删除版本、问题答案键，以及要求信息不足时弃答的模型指令。<br>
**输出**：不同删除策略下的模型答案、正确性与弃答行为，用于判断模型是否根据剩余上下文进行推理，以及是否在关键信息被移除后仍不当地产生确定答案。

</div>

**直观理解**：实验不是只问模型“答对没有”，还问它在证据被拿走后是否知道自己不该继续确定作答。若模型在结构上已缺少关键证据时仍频繁给出答案，可能说明它使用了记忆、外部先验或未经证实的推断。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### Base Damage Score

$$
D(j)=\left|\{t\mid t\text{ appears in }l_j\text{ and in no other context example}\}\right|
$$

**符号说明**

- $l_j$：待评估的第$j$个上下文例句。
- $t$：按空格切分得到的词元或字符序列。
- $D(j)$：例句$l_j$独有的singleton token数量。

<div class="equation-explanation" markdown="1">

**直观理解**：该式统计删除例句$l_j$后会直接失去多少个没有其他来源的词元。它衡量的是信息覆盖的结构损失，但还没有判断这些词元是否真的被某个问题需要。<br>
**原文位置**：第4.2节“ECC-inspired Targeted Deletion”

</div>

</div>

<div class="equation-block" markdown="1">

#### Question Damage Score与脆弱性判定

$$
D_Q(j)=\left|\{q\mid q\text{ requires a singleton token uniquely provided by }l_j\}\right|,\qquad \text{fragile}\iff\max_jD_Q(j)>0,\quad \text{robust}\iff\max_jD_Q(j)=0
$$

**符号说明**

- $D_Q(j)$：删除例句$l_j$后会失去必要信息的问题数量。
- $q$：谜题中的一个问题。
- $\max_j D_Q(j)$：在所有上下文例句中，最大的问题损伤分数。
- $fragile$：至少存在一个例句，其删除会损伤至少一个问题的必要信息。
- $robust$：删除任何单个例句都不会移除问题所需的唯一词元信息。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把“独家词元”与“问题依赖”连接起来：只有当某个问题确实需要被删例句独占的词元时，删除才计为问题损伤。最大值用于选择定向删除对象，并将谜题分为存在单点关键证据的fragile和没有这种单点损伤的robust。<br>
**原文位置**：第4.2节“ECC-inspired Targeted Deletion”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该方法没有提出需要训练的新模型，也没有报告通过梯度优化学习 $D_Q(j)$ 的目标函数；Question Damage Score是对已给定谜题结构、词元覆盖关系和问题需求关系进行计算的诊断指标。模型评估阶段属于推理时干预，而非模型参数训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 自包含Rosetta Stone任务表示**

每道谜题由上下文例句集合、问题集合和标准答案组成；其设计假设是答案所需的语言规律可由给定例句归纳，而无需了解目标语言的外部知识。该模块还要求任务支持移除单个上下文单元而不改变其余问题结构。

> 直观理解：它提供了一个相对封闭的推理环境：模型应当主要依靠题目给出的示例，而不是依靠“我以前见过这种语言”。

**2. Question Damage Score**

对候选例句 $l_j$，Base Damage Score $D(j)$统计该例句独有的singleton token数量；Question Damage Score $D_Q(j)$进一步统计其中被问题要求、因而会使问题失去必要信息的词元数量或对应问题数量。定向删除选择最大化 $D_Q(j)$ 的例句，平局时任意选择。

> 直观理解：Base Damage Score只问“这个例句有多少独家词”；$D_Q(j)$进一步问“这些独家词有多少真的会影响问题”。后者更贴近任务是否还能回答，因此被用来挑选最有破坏性的删除对象。

**3. ECC启发的结构脆弱性判定**

方法借鉴Error-Correcting Code的冗余思想：在多个例句中重复出现的词元提供冗余，而只出现一次的词元类似没有副本的编码信息。若 $\max_j D_Q(j)=0$，谜题被定义为robust；若 $\max_j D_Q(j)>0$，则被定义为fragile，并认为定向删除在空格词元推理下造成结构性不可解。

> 直观理解：有重复证据的题目像有备份文件，即使删掉一个例句也可能恢复规则；关键证据只有一个来源的题目没有备份，因此更容易因单点删除而失去可解性。这个判定描述的是题目结构，不直接断言语言模型一定失败。

**训练与推理**

数据处理阶段先为每道合格谜题提取空格分隔词元，识别仅出现于一个例句中的singleton token，并建立例句与问题需求之间的依赖关系。随后分别执行均匀随机删除和基于最大 $D_Q(j)$ 的定向删除；模型推理时在原题及两类删减题上回答问题，并被明确要求在信息不足时弃答，最后比较答案正确性和弃答行为。该流程不更新模型参数，因此核心实验是同一模型在不同上下文输入下的受控推理比较。

**复现信息**

为保证可解释性，词元定义为按空格分隔的字符序列；这种语言无关的定义倾向于低估损伤，因为更细的形态切分可能揭示可由其他部分恢复的信息。每道题的定向删除选择 $D_Q(j)$ 最大的例句，平局任意处理；$D_Q(j)$采用绝对问题数量而非归一化比例，因此不同题目之间的分数大小不能直接比较，跨题分类只使用是否为零这一条件。该框架依赖四项前提：任务自包含、可移除单个模块、存在可计算的单元—问题依赖关系，以及经过验证的答案键；若任务内容与模型先验知识重叠，删除后的答案可能来自参数记忆，结构损伤便难以解释。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- UK Linguistics Olympiad 的 53 道自包含语言学竞赛题；每道题包含前言、上下文示例和问题，原始版本用于测量基础解题能力。
- 随机删除版本：从每道题中删除一个随机上下文示例，用于测试在一般性上下文扰动下的解题和弃答行为；与原始版本共同构成 159 个解题实例中的两类修改条件之一。
- ECC-inspired 针对性删除版本：依据类似纠错码的结构分析，删除一个具有承重作用的上下文示例；该版本用于检验删除确实移除了回答至少一个问题所需的信息。另有 106 个修改题（53 个随机删除、53 个针对性删除）用于相关分析。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Exact Match（EM）**

模型答案与 UKLO 官方答案的精确匹配程度；在表 1 中，$w/\ N/A$ 将弃答计为 0，$w/o\ N/A$ 只在模型实际作答的题目上计算平均分。 （越高越好，因为表示更多答案与官方答案完全一致；但修改条件下的总体 EM 会把受损问题与未受损问题混合，不能单独反映关键示例删除的影响。）

</div>
<div class="metric-item" markdown="1">

**#N/A**

模型弃答或没有输出的题目数；删除条件中括号内的数字表示删除导致的新增弃答，即原题作答而删除后弃答的题目数。 （作为弃答诊断指标时，不能简单说越高越好；在信息确实不足时，适度增加的弃答可能表示更好的校准，但过多弃答也会降低任务完成率。）

</div>
<div class="metric-item" markdown="1">

**Precision、Recall 与 F1**

在 LLM-as-a-Judge 判断“不可解”为正类时，Precision 衡量判为不可解的样本中有多少符合结构标签，Recall 衡量结构上脆弱题中有多少被识别，F1 综合二者。 （三者均越高越好；分别代表判断可靠性、覆盖率以及两者的平衡。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 原始、随机删除与 ECC-inspired 删除条件下的模型解题和弃答

<div class="result-value" markdown="1">

表 1 显示，Gemini 3 Flash 的原始条件 EM 最高，为 0.730；GPT-5.4 为 0.425；Claude Sonnet 4.6 为 0.313。加入删除后，三者的总体 EM 均仅小幅下降：Gemini 在 ECC-inspired 条件下为 0.662，GPT-5.4 为 0.406，Claude 为 0.293。删除导致的新增弃答分别为 Gemini 2 次（均在 ECC-inspired 条件）、GPT-5.4 0 次、Claude 21 次。原文还报告人工基线为 0.484，但该基线来自每道题最高报告难度层级的计算。

</div>

模型在删除关键示例后仍大多继续作答，而且总体 EM 下降有限。这并不证明模型真正恢复了被删除的信息：总体平均会把未受影响的问题与受损问题混合，且模型可能利用冗余信息、语言先验、记忆或猜测。该结果主要说明“结构上缺少证据”并没有稳定转化为“模型主动弃答”。

<div class="result-source" markdown="1">

来源：第 6.1 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Gemini 3 Flash performs best on original puzzles (0.730), followed by GPT-5.4 (0.425) and Claude Sonnet 4.6 (0.313).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 结构脆弱性与 LLM-as-a-Judge 判断的一致性

<div class="result-value" markdown="1">

在 53 个 ECC-modified puzzles 上，结构标签以 $\max D_Q>0$ 表示 fragile、以 $\max D_Q=0$ 表示 robust。Gemini 将 45 个结构脆弱题中的 32 个判为不可解，Recall 为 71.1%、Precision 为 94.1%、F1 为 81.0%；GPT 的对应 Recall 为 48.9%、F1 为 64.7%；Claude 的 Recall 为 60.0%、Precision 为 100.0%、F1 为 75.0%。

</div>

Gemini 的评审判断与结构判据总体最一致，尤其在识别脆弱题方面优于另外两个模型；Claude 几乎不把结构稳健题误判为不可解，但漏掉了较多脆弱题。两者测量的不是同一个概念：$D_Q$ 描述预设推理结构中是否移除了必要信息，而评审模型判断的是在自身知识和推理能力下题目看起来是否仍可解。因此，一致性增强了对结构分析的信心，但不等于证明模型实际解题过程遵循了该结构。

<div class="result-source" markdown="1">

来源：第 6.2 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Gemini is the strongest overall agreement: 32 of 45 fragile puzzles correctly labeled (71% recall) at 94% precision, for an F1 of 81%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 删除驱动的弃答是否跟随结构损伤

<div class="result-value" markdown="1">

在 106 个修改题上，GPT-5.4 共弃答 2 次、Gemini 6 次、Claude 30 次；排除原始题中已经存在的弃答后，GPT 没有由删除引起的弃答，Gemini 有 2 次且全部发生在 ECC-inspired 条件，Claude 有 21 次，随机删除 10 次、针对性删除 11 次。

</div>

即使是弃答最多的 Claude，新增弃答也没有明显集中在结构上更关键的删除条件；Gemini 的新增弃答确实只出现在针对性删除下，但总数仅为 2 道题。因而，模型的弃答行为与 $D_Q$ 识别出的结构损伤并不稳定对应。该结论支持“模型很少承认信息不足”，但不能仅凭弃答统计判断模型是否使用了先验知识。

<div class="result-source" markdown="1">

来源：第 6.1 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Once pre-existing abstentions are excluded, only Gemini’s deletion-driven abstentions occur exclusively under targeted deletion, and they amount to two puzzles; Claude’s split evenly (10 vs. 11). Abstention does not track structural damage even for the model that abstains most.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验只使用 53 道 UKLO 题目，每个条件每道题只有一次模型调用；作者明确提醒，在 $N=53$ 下，小幅总体差异通常不具有充分信息量，且不同题目的问题数量和受损比例会影响 EM。
- LLM-as-a-Judge 不是独立于语言知识的人工金标准：评审模型也可能利用自身语言学知识，并且结构标签只描述预设推理过程下的信息必要性。因此，评审与 $D_Q$ 的一致或不一致都不能单独证明实际求解机制。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原始完整上下文：作为无删除条件，检验模型在标准题目上的解题能力，并作为计算删除影响的参照。
- 随机单示例删除：作为非定向扰动基线，用于区分普通信息删除与结构上专门移除关键示例的效果。
- ECC-inspired 单示例删除：作为核心受控干预，保留大部分推理任务，同时移除结构上对至少一个问题必要的信息。
- 完整上下文移除：与既有语言学推理研究中的设置比较；该条件去除全部题内证据，因此主要检验模型是否仍会依赖记忆、先验知识或其他非上下文来源作答。

**实验想回答的问题**

- 在随机删除或针对性删除单个上下文示例后，语言模型能否依据剩余信息判断问题不可解，并在信息不足时按指令停止作答？
- 结构层面的不可解性（由 $D_Q$ 判定）、模型作为评审者感知的可解性，以及模型实际作答行为之间是否一致？

**实验实现**

实验评估 Claude Sonnet 4.6、Gemini 3 Flash 和 GPT-5.4 三个前沿模型。模型均通过 API、默认设置、对每道题进行一次零样本调用；输入是包含前言、上下文示例和问题的单一提示。系统提示要求模型只依据给定上下文，并在问题无法回答时输出 N/A。解题实验在原始、随机删除和 ECC-inspired 删除版本上计算 EM，并额外记录弃答。独立的 LLM-as-a-Judge 实验向评审模型同时提供原题、答案键和修改题，要求判断原答案是否仍能从修改后的上下文推出；其作用是辅助验证结构判据，而不是替代 $D_Q$。完整上下文移除实验用于与既有研究的设置对照。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 完整上下文移除对照 | 原文将完整移除作为既有研究中的比较设置，并报告三个模型在没有题内上下文时仍很少弃答、偶尔答对；但所给章节未提供该条件的具体 EM 数值。 | 该对照测试模型在完全没有支持证据时是否仍会输出答案。它能显示模型可能依赖记忆或其他非上下文来源，但无法区分记忆、一般语言推断和随机猜测；相比之下，单示例删除保留了大部分原始推理任务，因此诊断分辨率更高。 | 第 6.1 节<br><span class="experiment-evidence">Removing the entire context eliminates the intended reasoning task, leaving memorized knowledge as the only possible source of correct answers.</span> |
| 随机删除与 ECC-inspired 针对性删除的条件对照 | 表 1 中，随机删除与 ECC-inspired 删除均使总体 EM 仅小幅变化；ECC-inspired 条件下的 EM 为 GPT-5.4 0.406、Claude Sonnet 4.6 0.293、Gemini 3 Flash 0.662。原文指出，ECC 删除对每道题 $m$ 个问题中受损问题的比例最多造成 $D_Q(j)/m$ 的 EM 下降，因此总体均值天然会稀释影响。 | 随机删除提供普通扰动参照，ECC-inspired 删除则有意打掉结构上承重的示例。二者总体分数接近并不表示两种删除同样无害，而是说明总体 EM 不适合直接衡量局部信息损失；应按受损标签或逐题结果条件化分析。 | 第 6.1 节<br><span class="experiment-evidence">These aggregate numbers understate the effect by construction.</span> |

**定性案例**

- 论文进一步选取 Gemini 3 Flash，分析“LLM-as-a-Judge 判定修改题不可解，但求解器随后仍答对”的矛盾案例。该案例类型用于区分模型是否能意识到信息不足与模型是否仍能输出正确答案；所给章节在第 6.3 节只开始介绍该分析，未提供具体题目、答案或后续定量结论，因此不能据此断言模型使用了记忆或真正完成了题内推理。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文提出 Question Damage Score 诊断框架来评测 LLM 对上下文的依赖及其语言推理行为。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`51e57ba59f120f8e63b582258eb2034e160e0b163d572006f1f7c65d2b664c5b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
