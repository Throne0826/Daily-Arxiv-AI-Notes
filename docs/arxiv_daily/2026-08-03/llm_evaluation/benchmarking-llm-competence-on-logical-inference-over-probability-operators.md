---
title: "[论文解读] Benchmarking LLM Competence on Logical Inference over Probability Operators"
description: "[arXiv 2607.27405][LLM 评测] 本文旨在检验大语言模型能否依据底层逻辑稳定地处理含“可能”“很可能”“必然”等概率算子的自然语言推理，并通过控制逻辑形式、表面措辞与答案类别，揭示总体准确率可能掩盖的固定回答偏差。"
arxiv_id: "2607.27405"
announcement_date: "2026-08-03"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-03T02:15:17.669509+00:00"
source_sha256: "dbe2993b1733d550e683d61e156b8a7ae6cceb23667390e2690ecc09a47a09e6"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "大语言模型评测"
  - "认知情态"
  - "概率算子"
  - "自然语言推理"
  - "逻辑推断"
  - "回答偏差"
  - "程序生成基准"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2607.27405</p>

# Benchmarking LLM Competence on Logical Inference over Probability Operators

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-03</span>
<span><strong>作者</strong> Nayera Hasan, Jack Greff, Alvin Grissom II</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Haverford College</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27405) · [PDF 下载](https://arxiv.org/pdf/2607.27405) · **关键词** 大语言模型评测, 认知情态, 概率算子, 自然语言推理, 逻辑推断, 回答偏差, 程序生成基准<br>


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

本文旨在检验大语言模型能否依据底层逻辑稳定地处理含“可能”“很可能”“必然”等概率算子的自然语言推理，并通过控制逻辑形式、表面措辞与答案类别，揭示总体准确率可能掩盖的固定回答偏差。

**不用术语来说**：人们常用“可能”“很可能”和“必然”表达不同程度的把握，而医疗、法律和金融系统必须正确区分这些说法。例如，“治疗很可能有效”不能被当作“治疗必然有效”。问题在于，大语言模型即使在推理测试中取得看似不错的平均准确率，也可能只是偏爱回答“Yes”或“No”，或依赖姓名、否定词等表面线索，并未真正理解哪些结论能由前提推出。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 构建面向概率算子推理的基准：以十五种模板编码十三类推理模式，并系统改变问题问法、否定策略、人物姓名来源与活动描述，使逻辑形式保持不变而表面表达发生变化，从而区分稳定的逻辑推断与词面模式匹配。
- 提出并使用“能力下限”概括二元推理能力，即分别计算正确答案为“Yes”和“No”的样例准确率后取较低者；该指标要求模型既能接受有效推理，也能拒绝无效推理，因而比总体准确率更不易受到固定回答偏差的虚高影响。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于自然语言推理、形式语义学与大语言模型评测的交叉领域。研究对象是英语中的认知情态表达，即用“might”“probably”“must”等词表示说话者对命题成立可能性的判断；其中“might”和“must”可分别近似表达可能性与必然性，而“probably”等可分级表达不同程度的确信，因此被称为概率算子。论文关注的核心不是模型能否生成语言流畅的解释，而是它能否在零样本条件下，根据这些算子的语义判断一个结论是否由前提逻辑推出，并在姓名、活动描述、问句措辞或否定形式变化时保持一致。这种能力直接关系到医疗、法律和金融文本中的不确定信息处理，例如不能把“某治疗可能有效”误当成“某治疗很可能有效”或“一定有效”。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**认知情态（epistemic modality）**

认知情态表示说话者基于现有知识，对某命题的可能性、确定性或可信程度所作的判断。英语中的“might”“may”“must”和“probably”都是典型标记。

</div>
<div class="concept-item" markdown="1">

**概率算子（probability operator）**

概率算子作用于一个命题，并表达该命题具有某种程度的可信性，如“probably $p$”表示命题 $p$ 很可能成立。它比只区分“可能”和“必然”的基本模态逻辑更细致，因为它允许表达可分级的确定程度。

</div>
<div class="concept-item" markdown="1">

**逻辑推断与表层模式匹配**

逻辑推断要求模型依据前提和算子的语义确定结论是否必然得到；表层模式匹配则可能仅依赖特定词语、姓名、否定标记或常见答案形式。若逻辑等价题目换一种措辞后答案发生变化，就说明模型可能没有稳定地追踪逻辑形式。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文把概率算子上的自然语言推断构造成二元判断任务：输入是由程序生成的英语提示，其中包含带有“might”“probably”或“must”等认知情态表达的前提、候选结论以及一种自然语言问法；输出为“Yes”或“No”，分别表示该结论是否由前提有效推出。评测采用零样本设置，不为模型提供针对该任务的训练示例。基准共含14,320个提示，使用15个模板表示13种不同推断模式，其中10种有效、3种无效；在保持底层逻辑形式不变时，系统改变五种问句形式、多种否定策略、来自七类国别群体的姓名以及五类活动描述。其关键假设是：真正掌握推断规则的模型应对逻辑等价的表述给出一致答案，而不应因词汇、人物属性或否定实现方式改变判断。该设置也用于区分逻辑能力与固定回答偏好，即模型是否不顾逻辑形式而系统性偏向“Yes”或“No”。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$p$**

被认知情态词或概率算子修饰的基础命题，例如“Bob提前回家”。

</div>
<div class="notation-item" markdown="1">

**$\operatorname{might}(p)$**

表示命题 $p$ 在当前知识状态下具有成立的可能性，但不意味着其很可能或必然成立。

</div>
<div class="notation-item" markdown="1">

**$\operatorname{probably}(p)$**

表示命题 $p$ 具有较高可信度或较高成立可能性，但仍不等同于确定成立。

</div>
<div class="notation-item" markdown="1">

**$\operatorname{must}(p)$**

表示依据当前知识，命题 $p$ 被视为必然或确定成立。

</div>

</div>

**直接相关的工作**

- **Yalcin (2010)**: 为自然语言概率算子的语义及其推断规则提供理论基础；本文据此把含可分级认知情态词的推断转化为可系统评测大语言模型的模板。
- **Holliday et al. (2024)**: 直接相关的先前模型评测工作，主要考查可由模态逻辑表示的“might”和“must”推理，并发现基础错误及相关推断类型之间的不一致；本文进一步覆盖“probably”等可分级概率算子，并系统控制问法、否定与表层内容。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

认识情态词承载知识状态、可信程度或不确定性，是自然语言决策中的基础信息。在临床场景中，系统需要根据“患者很可能患病”等陈述综合证据；在法律场景中，“可能知情”与“很可能知情”具有不同的证据分量；在金融场景中，把“市场很可能复苏”误作“市场必然复苏”会造成风险误判。因此，一旦大语言模型进入医疗、法律或金融决策链，它是否能在零样本条件下正确组合这些不确定性陈述，就不仅是形式语义学问题，也直接关系到系统输出是否可靠。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于模态逻辑的认识情态推理评测**：既有研究主要用模态逻辑可表示的“可能”和“必然”等表达探测模型，检查模型是否认可有效推理并在相关推理类型之间保持判断一致。这一路线能够覆盖必要性与可能性，却较少处理“很可能”所表达的可分级置信程度，即本文所称的概率算子。
- **基于总体准确率的二元逻辑推理基准**：常见评测向模型提出答案为“Yes”或“No”的问题，再以全部样例上的平均正确率汇总能力；部分研究也替换姓名、实体或量词，以观察模型是否依赖特定词元模式。该范式操作简单，但若数据中的正确答案较为均衡，始终倾向某一答案的模型仍可能得到具有迷惑性的总体分数。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有自然语言处理研究对认识情态关注不足，已有模态推理探测主要覆盖“可能／必然”，尚未系统评估模型对“很可能”等概率算子及其不同强度关系的推断能力；其后果是，模型在真实不确定性表达上的能力不能由传统模态逻辑测试充分推知。
- 既有推理评测难以把原则性的符号推理与表面模式匹配分离：模型可能随姓名、实体、量词、问句措辞或否定形式而改变答案，也可能固定偏向“Yes”或“No”。仅看总体准确率会掩盖这种行为，使答案偏好被误判为逻辑能力。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

仍缺少一种受控基准，在固定概率算子推理的底层逻辑形式时，系统改变问题形式、极性与表面内容，并同时检查模型对两类正确答案的表现。这样的设计才可判断模型是在追踪命题及其推导关系，还是在利用词面线索和类别偏好作答；同时，否定表达是否是回答偏差的主要来源，也尚需在语义等价的条件下单独检验。

</div>
<div markdown="1"><span>核心问题</span>

面对含“可能”“很可能”“必然”等认识情态表达的英语句子，当前大语言模型能否在零样本设置中稳定地区分有效与无效推理，并在问题措辞、否定策略、姓名属性和活动内容变化时保持与逻辑形式一致的判断，而非依赖固定的“Yes／No”偏好或表面词元模式？

</div>
<div markdown="1"><span>作者直觉</span>

如果模型真正掌握了推理规则，那么只要前提与结论之间的逻辑关系不变，换一种问法、姓名或活动描述都不应改变答案；它也应当既会对有效推理回答“Yes”，又会对无效推理回答“No”。因此，作者用程序化模板把“逻辑骨架”与“语言外观”拆开，并取两种答案类别准确率中的较低值作为能力下限：固定回答者会在相反类别上暴露失败，而稳定追踪命题关系的模型才能在该指标上取得较好表现。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是训练新模型，而是构造一个受控的零样本诊断基准，用来判断大语言模型能否对含认知情态词的英语句子进行逻辑推断。作者以概率算子语义为依据，把“probably”“might”“must”等表达映射为具有已知有效性的推理模板；随后固定底层逻辑，只改变问题措辞、否定方式、人名来源、性别和活动场景，程序化生成 14,320 个二元问答提示，并测试 29 个模型。模型回答被归为 Yes、No 或不确定，再按正确标签分组计算准确率及“能力下限”，从而区分真正追踪逻辑形式的能力与固定的 Yes/No 回答偏好。

直观地说，该方法像为同一道逻辑题制作许多“换皮版本”：人物、活动和问法虽然不同，但正确答案不应变化。若模型在换词后改变答案，或只擅长正确答案为 Yes 的题而几乎不会处理正确答案为 No 的题，那么总体准确率可能高估其逻辑能力；本文的配对变化和分标签评价正是为了暴露这种问题。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立概率算子推理模板

作者将自然语言推理抽象为 13 种具有已知有效性的逻辑模式，其中 10 种有效、3 种无效；由于“合取分配”和 Conjunctivitis 各有两种表面模板，最终得到 15 个模板。模板覆盖简单蕴涵、多步推断及需要拒绝的概率谬误。

<div class="method-step__io" markdown="1">

**输入**：Yalcin（2010）等语义研究所刻画的概率算子、必要性、可能性及概率比较关系。<br>
**输出**：带有规范逻辑形式和二元正确标签的 15 类推理题骨架。

</div>

**直观理解**：先由形式语义决定每类题究竟应回答 Yes 还是 No，而不是依靠人工直觉临时标注。无效模板尤其用于检查模型是否会把听起来合理的结论误当作必然成立。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成逻辑等价的受控提示

程序将模板实例化为英语提示，并系统改变 5 种问题问法、多种否定实现、7 类来源的人名、性别和 5 种活动描述；还使用抽象字母变量作为减少人物语义影响的对照。变化原则是尽量保持推理关系不变，只替换不应决定答案的表面因素。

<div class="method-step__io" markdown="1">

**输入**：15 个模板，以及可替换的问题形式、否定策略、人名和活动描述。<br>
**输出**：共 14,320 个带正确 Yes/No 标签的提示，并形成可按模板、否定、问法及内容属性切分的测试集合。

</div>

**直观理解**：这相当于把同一张数学试卷分别换成人名版、字母版和不同措辞版。真正理解逻辑的模型应在这些版本上给出一致判断。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 对模型进行零样本二元推断

在不针对该基准训练模型的条件下，逐题要求模型判断结论是否由前提推出，并将输出归一为 Yes、No 或不确定。评价表中把不确定回答计为错误，以避免模型通过回避二元判断获得宽松得分。

<div class="method-step__io" markdown="1">

**输入**：每个自然语言提示及待评估的 29 个大语言模型。<br>
**输出**：每个模型在每个提示上的标准化答案，以及按正确标签和实验因素组织的响应记录。

</div>

**直观理解**：模型面对的是一次普通问答，而不是看到答案后的学习过程。统一答案格式后，才能比较模型是在做逻辑判断，还是习惯性地偏向某个回答词。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算能力与表面敏感性指标

作者分别计算正确答案为 Yes 和正确答案为 No 的子集准确率，并取二者较小值作为能力下限；同时比较逻辑相同但表面因素不同的切片，包括问法、否定表达、活动、姓名性别和姓名来源。该设计将总体命中率、固定答案偏好和表面形式敏感性分开考察。

<div class="method-step__io" markdown="1">

**输入**：标准化模型答案、题目正确标签及每题的模板、否定、问法、姓名和活动元数据。<br>
**输出**：模型级能力下限、总体及分组准确率，以及各控制因素引起的性能差异。

</div>

**直观理解**：若模型永远回答 Yes，它可能在 Yes 题上满分，却在 No 题上为零；取两类成绩中较差者会把这种策略的能力下限压到零。再对同一道逻辑题的不同“外包装”做比较，就能观察无关词语是否左右答案。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 概率比较关系

$$
A \succeq B \iff p(A) \ge p(B)
$$

**符号说明**

- $A$：第一个命题或事件。
- $B$：第二个命题或事件。
- $\succeq$：“至少与……一样可能”的比较关系。
- $p(A)$：命题或事件 A 的数值概率。
- $p(B)$：命题或事件 B 的数值概率。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把自然语言中的“A 至少和 B 一样可能”转换为概率大小比较，是 Positive Form Transfer、Complement Transfer 和 Conditional-to-Comparative 等模板的共同语义基础。它让题目的正确性由概率关系决定，而不是由句子听起来是否自然决定。<br>
**原文位置**：第 3.1 节 Inference Templates，Table 1 前的符号定义

</div>

</div>

<div class="equation-block" markdown="1">

#### Probably 的阈值化表示

$$
Pr(A) \iff p(A) \ge 0.5
$$

**符号说明**

- $Pr(A)$：自然语言断言“probably A”的简写，而非另一个数值概率函数。
- $p(A)$：命题 A 的数值概率。
- $0.5$：在文中所采用的典型概率假设下，“很可能”的概率阈值。
- $\iff$：在该形式化约定下两侧等价。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把“probably A”操作化为 $A$ 的概率至少为一半，使自然语言概率算子能够参与明确的有效性判断。它是模板构造中的语义约定，而不是模型输出的概率校准目标。<br>
**原文位置**：第 3.1 节 Inference Templates，Table 1 前的符号定义

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文提出的是诊断性数据集与评价方法，没有利用这些提示更新受测模型参数，也没有定义需要梯度优化的训练损失；中心目标是测量既有模型在概率算子推理上的零样本能力。能力下限属于评价统计量而非训练目标，其作用是惩罚只会处理某一种正确答案极性的模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 有效性已知的概率推理模板库**

模板以命题 $\phi$、$\psi$、概率 $p(\cdot)$、概率算子 $Pr(\cdot)$、必要算子 $\square$、可能算子 $\lozenge$ 和比较关系 $\succeq$ 表达。有效模板包括 Probably-to-Might、Must-to-Probably、Positive Form Transfer、Chancy Modus Ponens、合取分配、Conditional-to-Comparative 和 Chancy Disjunction Introduction 等；无效模板要求模型拒绝不受概率语义保证的结论，例如从“probably $\phi$”与“probably $\psi$”推出“probably $(\phi\land\psi)$”。

> 直观理解：模板库提供可核验的标准答案，是整个基准的逻辑地基。特别是，“两件事各自很可能发生”并不保证“二者同时发生”仍然很可能，因此只按日常语言顺畅度回答会落入合取谬误。

**2. 表面形式干预模块**

该模块在保持底层推理有效性和目标标签不变的前提下，替换问题引导语、否定形式、活动谓词及人物名称属性。抽象字母变量版本构成内容较少的基线，而具体姓名版本用于测量性别和来源相关的词项效应。

> 直观理解：它的用途不是扩大话题覆盖面，而是实施控制变量实验。如果仅仅把“Does it follow that”改成“Is it true that”便导致答案翻转，就不能把原先的正确回答稳妥解释为逻辑能力。

**3. 按答案极性分解的能力下限**

评价不只报告混合所有题目的准确率，而是将题目依正确标签拆为 Yes-correct 与 No-correct 两组，并以两组准确率的较小值概括模型最弱一侧的能力。由于基准通过有效性与否定变化提供两类正确标签，固定偏向 Yes 或 No 的模型会在相反标签子集上暴露出来。

> 直观理解：普通平均分可能奖励“总猜同一个答案”的投机策略；能力下限相当于要求模型两条腿都能走路。它并不证明模型使用了符号推理，但能排除最明显的单标签偏好。

**训练与推理**

训练阶段不适用：作者依据形式语义设计模板并程序化生成测试项，而不是在该数据上微调模型。推断阶段中，每个模型接收含前提、候选结论和二元问题的英语提示，独立产生回答；回答随后被标准化为 Yes、No 或不确定，并与模板预先确定的标签比较。分析阶段先按 Yes-correct 与 No-correct 切分，再比较不同问题形式、否定策略和表面内容下的表现；因此最终结论针对模型现有的零样本推断行为，不应解释为训练后获得的概率逻辑系统。

**复现信息**

公平解释结果所需的核心规模是：14,320 个程序生成提示、13 种不同推理模式、15 个表面模板和 29 个受测模型。受控因素包括 5 种问题形式、多种否定策略、7 类来源的人名、姓名性别、5 种活动描述及抽象字母变量对照；其中逻辑形式原则上保持固定。表格明确说明不确定回答按错误处理。原文节选未完整提供解码参数、随机种子、每种组合的精确采样数量、答案解析规则和全部模型调用配置，因此复现时必须回查论文正文或代码，不能从当前材料推断这些设置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 作者构建的英语概率算子逻辑推理基准。基准包含13类推理规则，其中“合取分配”和“合取谬误”各有两种表层模板，共15个表层模板；每个模板向每个模型提供80条提示。模板分为5个简单有效推理、5个多步有效推理和3个无效推理，用于同时检验规则应用与谬误拒绝。原文节选未说明训练集、验证集或测试集划分，因此它应被理解为直接评测集，而非用于模型训练的数据集。
- 问题形式控制集。相同推理内容被改写为肯定式和否定式，并覆盖 truth、correct、valid、follow、direct 五类主要问法；此外加入 not-correct 与 not-valid 两种形式，以比较“负面形容词”和显式插入 not 的否定策略。该部分用于检验模型是否在语义不变时因否定、元语言包装或诱导性语用而改变答案。
- 人口统计与场景鲁棒性控制。姓名来自印度、俄罗斯、日本、非洲、德国、法国、美国七类国籍群体，并加入抽象字母变量，同时平衡常见男性名和女性名；活动覆盖五种语义相近场景。其作用不是测量社会偏见本身，而是检查逻辑准确率是否不应当地随姓名或场景变化。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**总体准确率（Overall accuracy）**

在指定提示集合中回答正确的比例，无法解析为 Yes 或 No 的 Uncertain 也按错误计。正确标签由推理有效性与问题极性共同确定：有效肯定题和无效否定题应答 Yes，有效否定题和无效肯定题应答 No。该指标直观，但会受有效模板多于无效模板以及恒定答案策略影响。 （越高越好，因为表示更多题目被正确判断；但单独升高不能证明模型真正掌握逻辑，必须结合答案偏置与最弱极性表现解释。）

</div>
<div class="metric-item" markdown="1">

**答案偏置（Bias）**

先分别计算正确答案应为 Yes 和应为 No 时的平均准确率，再取二者之差，即 $\mathrm{Bias}=\mathrm{Acc(Yes)}-\mathrm{Acc(No)}$。正值表示偏好 Yes，负值表示偏好 No，接近0表示两类答案较均衡；它测量的是表层响应倾向，而不是准确率本身。 （绝对值越接近0越好，因为模型不明显偏向某个答案；但 Bias 为0也可能来自随机作答，所以不能独立视为推理能力证据。）

</div>
<div class="metric-item" markdown="1">

**能力下限（Floor）**

定义为 $\min(\mathrm{Acc(Yes)},\mathrm{Acc(No)})$，即取正确答案为 Yes 与正确答案为 No 两类题中较差的一侧。它专门惩罚只擅长或只偏好一种答案的系统：恒定回答者得0，随机抛硬币者期望得0.5，稳定推理者应接近1。 （越高越好，因为较高值要求模型在两种正确答案极性上都表现良好，比总体准确率更能排除恒定回答策略。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 恒定回答 Yes：不读取逻辑内容而始终肯定。它在偏置指标上达到极端正值，并在 Floor 上得0，因此可识别看似有一定总体准确率、实则只依赖肯定偏好的模型。
- 恒定回答 No：始终否定，是恒定 Yes 的对称比较；其偏置为极端负值，Floor 同样为0，用来揭示否定回答偏好。
- 随机抛硬币回答：以相同概率输出 Yes 或 No，其期望 Bias 为0、Floor 为0.5。它为“答案均衡但没有推理能力”的绝对参照，因而比只看总体准确率更能说明模型是否超过随机水平。
- 模型间横向比较：实验覆盖29个英语评测模型，包括Gemma、Qwen、DeepSeek-R1、Llama等规模递增系列以及Claude、GPT等前沿模型。规模分级家族用于考察参数规模与逻辑能力是否同步提升，前沿模型则提供当前高性能系统的参照；但节选未给出这些模型的实际比较结果。

**实验想回答的问题**

- 不同规模与系列的大语言模型能否在概率算子和认知模态算子构成的自然语言推理中，既接受有效推论，又拒绝“合取谬误”等无效推论？
- 模型的作答究竟反映了对命题逻辑关系的稳定追踪，还是主要受答案偏好、问题否定形式、措辞方式以及姓名和活动场景等表面因素影响？

**实验实现**

所有模型面对相同的每模板80条表层提示，并以温度 $\tau=0$ 各运行一次；主分析汇总不同模板和问题形式。开放权重模型采用零样本提示，解析首个回答词元为 Yes、No，其他输出记为 Uncertain。为严格评估直接作答行为，Qwen 3与DeepSeek-R1关闭思维模式，GPT-oss使用最低可用推理等级。Qwen 3:4B在无约束生成时不遵循格式的比例最高达到96%，因此改用受约束的 Yes/No 输出格式；该约束限制输出形式，但仍允许模型自由选择两个答案。评测覆盖29个模型，包括五个具有规模梯度的家族及若干前沿或专门模型。除总体准确率外，实验按“推理有效/无效”与“问题肯定/否定”构成 $2\times2$ 单元格，并分析答案偏置、否定敏感性和能力下限。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces an evaluation of LLM logical reasoning over probability operators.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`dbe2993b1733d550e683d61e156b8a7ae6cceb23667390e2690ecc09a47a09e6`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
