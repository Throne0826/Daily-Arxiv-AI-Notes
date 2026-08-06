---
title: "[论文解读] Same Formulas, Different Semantics: Do Language Models Follow Modal Logic Specifications?"
description: "[arXiv 2608.05097][LLM Reasoning] 本文通过构造“公式完全相同、仅语义条件不同且正确标签相反”的成对模态逻辑问题，检验语言模型是否真正遵循题目明确规定的语义，而非套用自身熟悉的默认逻辑。"
arxiv_id: "2608.05097"
announcement_date: "2026-08-06"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:58:23.326721+00:00"
source_sha256: "d8a5d657bbbd2fd6a19b9f1133ef96d74d3622563c8ea76cc0297fe18c72114e"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "大语言模型"
  - "量化模态逻辑"
  - "Kripke 语义"
  - "语义规范遵循"
  - "对比评测"
  - "自动定理推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.05097</p>

# Same Formulas, Different Semantics: Do Language Models Follow Modal Logic Specifications?

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Réemi Andrieu, Damien Sileo</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Univ. Lille, Inria, CNRS, Centrale Lille, UMR 9189 - CRIStAL, F-59000 Lille, France</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.05097v1) · [PDF 下载](https://arxiv.org/pdf/2608.05097v1) · **关键词** 大语言模型, 量化模态逻辑, Kripke 语义, 语义规范遵循, 对比评测, 自动定理推理<br>
**代码**: [https://github.com/sileod/modal-semantics-reasoning](https://github.com/sileod/modal-semantics-reasoning) · **项目页**: [https://huggingface.co/datasets/sileod/modal-semantics-reasoning](https://huggingface.co/datasets/sileod/modal-semantics-reasoning)

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

本文通过构造“公式完全相同、仅语义条件不同且正确标签相反”的成对模态逻辑问题，检验语言模型是否真正遵循题目明确规定的语义，而非套用自身熟悉的默认逻辑。

**不用术语来说**：一句关于“必然”或“可能”的推论是否成立，不只取决于句子本身，还取决于题目如何规定不同可能世界之间的联系，以及对象能否在世界之间出现或消失。例如，“如果命题 $p$ 是必然的，那么 $p$ 是可能的”在某些规则下成立，在另一些规则下却不成立。实际应用要求模型根据当前给出的规则调整判断，但常见测试难以区分模型是在遵守这些规则，还是仅凭训练中形成的固定答题习惯得到正确答案。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出语义敏感性评测设计：在每个问题对中固定前提、待证结论、词汇内容和公式难度，只改变一个可达关系或对象域条件，并由自动推理工具验证两个版本具有相反标签，从而把“读取并执行语义规范”的能力与一般公式识别能力分离开。
- 作者构建主要的平衡核心集，使每种语义条件在真、假标签中出现次数相同，避免模型仅根据条件名称猜测答案；同时设置省略框架条件的评测，以分析模型在没有明确约束时倾向采用哪一种熟悉的模态逻辑。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型形式推理评测，关注模型能否遵循题目明确指定的量化模态逻辑语义。模态逻辑用“必然”与“可能”描述命题在多个可能世界中的成立情况；推理是否有效不仅取决于前提和结论的公式形式，还取决于世界之间的可达关系以及各世界中对象是否相同。例如，$p\rightarrow\Box\Diamond p$ 在某些满足特定可达条件的框架上有效，在任意 Kripke 框架上却未必有效。因此，本文评测的核心不是模型是否熟悉某一种常用模态逻辑，而是它能否根据当前题目声明的框架条件或论域条件调整判断。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**Kripke 语义**

Kripke 语义把模态推理解释为一组“可能世界”及其可达关系：$wRv$ 表示从世界 $w$ 可以考虑世界 $v$。$\Box p$ 要求 $p$ 在所有可达世界成立，$\Diamond p$ 则要求至少存在一个可达世界使 $p$ 成立。

</div>
<div class="concept-item" markdown="1">

**框架条件**

框架条件是对可达关系 $R$ 的约束，如自反性、对称性和传递性；不同约束对应不同的模态推理规则。即使前提与待证结论完全相同，改变框架条件也可能改变推理有效性。

</div>
<div class="concept-item" markdown="1">

**变化论域语义**

在量化模态逻辑中，每个世界可有自己的对象集合 $D_w$，对象可能沿可达关系出现或消失。是否允许对象出现或消失会影响量词 $\forall$、$\exists$ 与模态算子 $\Box$、$\Diamond$ 交换时的有效性。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

一个测试实例由形式化前提、一个猜想，以及明确声明的语义条件组成；模型需要输出该猜想是否由前提在指定语义下必然推出。关键设计是成对构造实例：一对题目的对象层公式，即前提与猜想，保持完全相同，只改变一个框架条件或论域条件，并由自动定理推理基础设施验证两题具有相反标签。框架条件涉及可能世界间可达关系的性质，论域条件涉及对象能否随世界迁移而出现或消失；此外，作者还在省略框架说明的设置下考察模型默认采用哪种熟悉逻辑。主要的平衡核心进一步保证每种语义条件在真、假标签中等量出现，使模型不能只凭条件名称猜答案，而必须联合读取公式和语义规范；严格成功意味着一对实例的两个判断均正确。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\Box p$**

命题 $p$ 在当前世界可达的所有世界中都成立，即“必然 $p$”。

</div>
<div class="notation-item" markdown="1">

**$\Diamond p$**

至少存在一个当前世界可达的世界使命题 $p$ 成立，即“可能 $p$”。

</div>
<div class="notation-item" markdown="1">

**$wRv$**

可能世界 $v$ 对世界 $w$ 可达；模态算子的真假由这种可达关系决定。

</div>
<div class="notation-item" markdown="1">

**$D_w$**

世界 $w$ 中存在并可被量词取值的对象集合，即该世界的论域。

</div>

</div>

**直接相关的工作**

- **ProofWriter、FOLIO、LogicNLI 与 LogicBench**: 这些基准主要在固定的预设逻辑下改变事实、规则或证明深度，因而可能奖励模型对基准主导推理制度的适应；本文则固定对象层公式并改变声明的模型论语义，直接测试判断是否随规范变化。
- **QMLTP、非经典 TPTP 格式与基于嵌入的定理证明**: 这些工作提供量化模态逻辑的形式表示和自动推理基础设施。本文使用该基础设施生成或核验正确标签、证明产物与反模型，而不提出新的模态逻辑或定理证明器。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在义务推理、法律推理以及其他受明确规则约束的场景中，同一组事实和同一结论可能因局部语义规定不同而具有不同有效性。系统若忽略当前规定，擅自采用训练中更熟悉的逻辑，即使在常规基准上准确，也可能在规则发生变化时给出方向相反的判断，因此需要专门测量模型对语义规范的服从能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **固定背景逻辑的自然语言推理基准**：这类基准预先采用一种不随样例变化的推理制度，主要改变事实、规则或证明深度，再依据固定逻辑判断结论是否可推出。它们能够测试模型在既定制度内处理不同内容或推理链长度的能力。
- **单一预设语义下的模态推理评测**：这类评测扩大了被测试的推论类型，引入“必然”“可能”等模态表达，但通常仍为每道题指定一个统一或预设的目标语义，考察模型能否解决单个问题，而不系统改变同一公式所处的语义条件。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 固定逻辑基准允许模型学习数据集中占主导地位的推理制度；较高准确率因而不能证明模型会在题目改变语义规范时同步改变判断，可能高估其在新规则下的稳健性。
- 既有模态评测通常没有保持对象层公式不变并仅干预语义条件，因此无法直接判断错误来自公式本身太难，还是模型没有服从框架与对象域规定；若条件与标签分布不平衡，还可能出现仅凭条件名称预测答案的捷径。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前缺少一种受控且抗捷径的评测：它需要对完全相同的前提和待证结论施加最小语义干预，使正确标签随干预翻转，同时平衡语义条件与标签的对应关系。没有这种设计，就难以把模型拥有某种模态逻辑知识与模型能够让当前规范覆盖其默认逻辑这两种能力区分开。

</div>
<div markdown="1"><span>核心问题</span>

当提示明确给出不同的 Kripke 框架条件或对象域变化规则时，语言模型是否会据此改变对同一模态推论的有效性判断；这种规范服从能力又在多大程度上取决于模型身份和推理模式？

</div>
<div markdown="1"><span>作者直觉</span>

如果一对题目的公式、词汇和复杂度都不变，而自动推理 oracle 证明仅更换一条语义规则就会使标签反转，那么模型只有识别该规则对公式的具体影响，才可能连续答对两个版本。进一步让每条规则同样频繁地对应真、假标签，就切断了“看到某个条件便固定回答”的捷径；省略条件时观察模型选择，则可反向揭示其默认逻辑偏好。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法不是训练新的语言模型，而是构造一种“最小语义对照”评测：每个样本对共享完全相同的前提集合 $P$ 与猜想 $C$，只把语义规范从 $S_a$ 改为 $S_b$，并要求自动定理证明器确认答案标签发生翻转，即 $y_a\neq y_b$。语义差异被限制为一个框架条件或论域条件，因此模型若在两个问题上给出正确的相反答案，就必须利用题目明确规定的语义，而不能只靠公式表面、常见模态逻辑习惯或条件名称猜测。无前提时任务判断 $C$ 在 $S$ 下是否有效；有前提时判断 $P$ 是否在 $S$ 下蕴涵 $C$。

端到端流程是：先选择一个待检验的语义对照并生成候选公式，再执行结构检查和去重；随后把问题序列化为非经典 TPTP，经 LET 嵌入转换为高阶逻辑，交由 Vampire 与 Leo-III 寻找证明或反模型；只保留两侧均被可靠解析且标签相反的样本对，并将形式化语义确定性地渲染为受控英语提示。平衡核心进一步让每种条件与真假标签等频，使仅观察语义条件的策略只能达到 $50\%$ 严格准确率。直观地说，这相当于保持“题干和结论”不动，只替换一条世界规则或对象存在规则，再检查模型是否会随规则改变而改变判断。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 选择语义对照并生成候选问题

框架轴使用 K–D、K–T、T–B、T–S4、B–S5 等单条件对照，分别改变序列性、自反性、对称性或传递性；论域轴比较可变、累积、递减与常量论域，并生成含量词和模态词交替的公式。候选族专门针对一个语义差异生成，而不是对全部公式与语义做笛卡尔积采样。

<div class="method-step__io" markdown="1">

**输入**：一个框架语义对照或论域语义对照，以及有效性题或带前提推理题的模板。<br>
**输出**：候选三元组 $(S,P,C)$，其中 $S$ 是明确的语义规范，$P$ 是可为空的前提集合，$C$ 是待判断的猜想。

</div>

**直观理解**：研究者先固定只想测试的一条规则，例如“可达关系是否对称”或“对象能否消失”，再设计恰好会受这条规则影响的问题。这样可以把模型的成败归因到目标语义，而不是多个条件同时变化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 结构约束、配对与核心平衡

结构检查会拒绝框架轴中的一阶构造、论域轴中的常量、非目标语义变化、规范化后重复的公式以及深度过大的公式；随后将共享 $P$ 和 $C$、仅有一个语义条件不同且标签相反的两侧组成样本对。平衡核心使用 B 对 S4、累积论域对递减论域，并交叉两种翻转方向与两类任务，使条件和标签相互独立。

<div class="method-step__io" markdown="1">

**输入**：生成的候选三元组及其公式结构。<br>
**输出**：满足 $P_a=P_b$、$C_a=C_b$、$y_a\neq y_b$ 的候选配对，以及由 160 个非嵌套配对组成的平衡核心。

</div>

**直观理解**：配对像控制变量实验：同一道题只换一条规则。平衡步骤还消除了“看到某条规则就总答真或总答假”的捷径，迫使模型结合规则与公式作答。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自动推理预言机验证

LET 嵌入工具链将模态问题翻译为高阶逻辑，Vampire 与 Leo-III 分别尝试给出标准 SZS 证明状态或反模型状态；系统不会把“未证明成功”当作无效，而会丢弃冲突、超时或任一侧未解决的候选。平衡核心中的无效侧还由独立 Kripke 求值器检查二世界或三世界反模型。

<div class="method-step__io" markdown="1">

**输入**：候选问题两侧的非经典 TPTP 表示。<br>
**输出**：每一侧都有证明或反模型依据、且两侧标签确实相反的已验证问题对，并保留翻译、命令、版本、运行状态与输出哈希等预言机材料。

</div>

**直观理解**：定理证明器相当于答案裁判：真命题需要证明，无效命题需要具体反例，不能因为搜索暂时没有结果就判错。独立检查小型反模型则进一步防止翻译或证明器状态被误读。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 受控英语渲染与模型推断

确定性渲染器把语义规则、前提和猜想写成受控英语，直接说明相关规则，但隐藏 B、S4、“累积”等传统系统名称；命题和谓词使用中性词汇，嵌套模态作用域通过“当前世界”和“该世界”明确表达。主协议对每一侧分别请求二元 Yes/No 判断，并把格式错误的回答计为错误。

<div class="method-step__io" markdown="1">

**输入**：已验证的 $(S,P,C,y)$ 问题及其成对关系。<br>
**输出**：可直接提交给语言模型的成对提示，以及每侧解析结果、严格配对正确性和条件解析准确率等评测记录。

</div>

**直观理解**：模型看到的是规则的实际含义，而不是可能触发背诵答案的逻辑名称。严格配对计分要求同一公式在两种语义下都答对，因此真正测试的是模型是否跟随语义变化。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 成对模态任务表示

$$
((S_a,P,C),y_a),\quad ((S_b,P,C),y_b),\qquad y_a,y_b\in\{\mathrm{true},\mathrm{false}\}
$$

**符号说明**

- $S_a$：样本对第一侧规定的框架语义或论域语义。
- $S_b$：样本对第二侧的语义；它与第一侧仅相差一个目标条件。
- $P$：两侧共享的前提集合，可以为空。
- $C$：两侧共享的猜想或待验证公式。
- $y_a$：在语义 $S_a$ 下，猜想有效或由前提蕴涵时对应的布尔标签。
- $y_b$：在语义 $S_b$ 下对应的布尔标签。

<div class="equation-explanation" markdown="1">

**直观理解**：该式定义了评测的基本单位：两侧题目具有相同前提和猜想，只改变语义。若模型真正服从题目规定的语义，它应根据 $S_a$ 与 $S_b$ 的差别给出相应判断。<br>
**原文位置**：第 3 节 Task formulation

</div>

</div>

<div class="equation-block" markdown="1">

#### 最小语义翻转保留条件

$$
P_a=P_b,\qquad C_a=C_b,\qquad y_a\neq y_b
$$

**符号说明**

- $P_a$：样本对第一侧的前提集合。
- $P_b$：样本对第二侧的前提集合。
- $C_a$：样本对第一侧的猜想。
- $C_b$：样本对第二侧的猜想。
- $y_a$：第一侧经自动推理预言机确认的标签。
- $y_b$：第二侧经自动推理预言机确认的标签。

<div class="equation-explanation" markdown="1">

**直观理解**：前两项保证题目的逻辑内容不变，最后一项保证仅改变语义就会翻转正确答案。因而，一个模型若对两侧给出相同答案，至少会错一侧；若两侧都正确，则表明它捕捉到了语义条件对推理结论的影响。<br>
**原文位置**：第 3 节 Task formulation

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文提出的是数据构造与推断评测协议，没有使用这些样本训练或微调被测语言模型，也没有定义需要梯度优化的损失函数；自动推理器的作用是生成和核验金标准标签，而不是优化模型参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 单因素语义对照生成器**

该模块把语义拆成可控的框架属性与论域属性。框架题仅使用命题模态逻辑，以排除论域和名称语义的影响；论域题统一使用序列框架 D、变量与谓词，并禁止常量和函数，以便把答案变化归因于对象跨世界出现或消失的约束。

> 直观理解：它负责保证实验每次只拧动一个旋钮：框架题只改变世界之间如何可达，论域题只改变各世界有哪些对象。

**2. 证明与反模型预言机**

模态公式先通过 LET 的浅层语义嵌入转换为高阶逻辑，再由 Vampire 和 Leo-III 求解。有效侧以证明为依据，无效侧以反模型为依据；双证明器一致与单证明器决定性结果被分开记录，任何冲突或未解决样本均不进入最终集合。

> 直观理解：这个模块为数据生成可信标签，并区分“确实存在反例”和“证明器没找到证明”。后一区分是逻辑评测可靠性的关键。

**3. 平衡核心与确定性语言渲染器**

平衡核心由 B 与 S4、累积与递减两组非嵌套对照构成，并均衡语义条件、标签、翻转方向和任务类型。渲染器对同一形式结构采用固定语言模板，显式陈述语义属性但不提供传统系统名称。

> 直观理解：平衡核心堵住了按条件猜标签的捷径；固定模板则减少措辞变化带来的噪声，使分数更能反映语义推理能力。

**训练与推理**

推断时，每个已验证样本对被拆成两个提示，两者的前提与猜想相同，但语义规则不同。主协议让模型直接输出 Yes/No；回答随后被解析并与预言机标签比较。严格准确率仅在一对中的两个回答都正确时记为成功，因此随机独立回答的配对成功率为 $25\%$；在平衡核心中，任何只根据当前语义条件猜测标签、而忽略公式的策略，其严格准确率为 $50\%$。论文还比较推理模式设置，但这仍属于同一提示上的推断配置变化，不涉及训练。

**复现信息**

复现时需要保留三类关键约束。第一，框架题必须保持命题性，论域题必须避免常量与函数，并检查重复公式、非目标语义变化和过深结构。第二，问题应以非经典 TPTP 序列化，经 LET 嵌入后分别调用 Vampire 与 Leo-III；不能将超时或搜索失败解释为无效，冲突或任一侧未解决的候选必须剔除。第三，英语提示应由确定性模板生成，明确写出自反、对称、传递、对象不消失或不出现等规则，同时隐藏传统系统简称；评测时格式错误回答按错误处理，并同时报告严格配对正确性与回答可解析性，以区分推理失败和输出格式失败。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 完整配对评测集包含 $800$ 对问题。每对的两个版本共享同一组前提和同一待证公式，仅框架条件或域条件不同，并由自动定理证明器验证两侧标签相反。其中 Frame 与 Domain 各含 $400$ 对；Frame 测试可能世界之间的可达关系约束，Domain 测试不同世界中对象存在域的约束。五个直接推理模型均评测全部 $800$ 对。
- 平衡非嵌套核心集包含 $160$ 对，是主要的语义控制测试集。每种条件在每个对比中都同时出现在两个标签下，且偏向任一条件的公式各占一半，因此不能只凭条件识别标签。核心集的 $320$ 个侧面均获自动推理结果支持：每个无效侧还有独立 Kripke 求值器核验的二世界或三世界反模型；$160$ 个有效侧中有 $136$ 个得到两个自动定理证明器一致确认，其余 $24$ 个得到一个证明。
- 辅助诊断包括两个子集：省略框架规格的全部 $400$ 个 Frame 问题用于测量模型对 K、D、T、B、S4、S5 等熟悉模态逻辑的默认亲和性；固定的 $50$ 对 Frame 子集用于比较命名英语、关系定义和 TPTP 三种等价表示，每种框架对比取 $10$ 对，以隔离输入表示的影响。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**严格配对准确率**

对 $N$ 个问题对求平均，只有第 $i$ 对的两侧预测都分别等于真值时才记为正确，即 $\frac{1}{N}\sum_i\mathbf{1}[\hat{y}_{i,a}=y_{i,a}\land\hat{y}_{i,b}=y_{i,b}]$。它比单侧准确率更直接地检验模型是否根据语义条件改变判断。 （越高越好；在平衡核心集上超过 $50\%$ 才能排除只看条件、不读公式的最优简单策略。）

</div>
<div class="metric-item" markdown="1">

**单侧准确率与可解析准确率**

单侧准确率分别评价每个语义规格的判断；可解析准确率在一对的两个回答都可解析时再计算正确率，Pair parse 则统计两侧回答均成功解析的问题对比例。主评分把格式错误直接视为错误，因此二者共同区分推理错误与输出格式失败。 （均为越高越好；但较高的条件化可解析准确率若伴随较低 Pair parse，不能代表整体系统可靠。）

</div>
<div class="metric-item" markdown="1">

**答案变化率**

定义为 $\Pr(\hat{y}_a\neq\hat{y}_b)$，测量只改变语义条件后模型是否改变判断；论文还检查发生变化时的正确率及两侧正确或错误的四种组合。 （不存在脱离正确率的单调优劣：过低表示忽略干预，过高也可能只是无依据地翻转；应与严格配对准确率联合解释。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 平衡非嵌套核心集上的直接推理

<div class="result-value" markdown="1">

五个模型中有四个低于 $50\%$ 条件唯一基线：DeepSeek V4 Flash、DeepSeek V4 Pro、GPT-5.6 Luna 和 GPT-5.6 Terra 的严格配对准确率分别为 $4.4\%$、$2.5\%$、$21.2\%$ 和 $25.0\%$；只有 Claude Sonnet 5 达到 $65.0\%$。

</div>

作者据此主张，多数被测模型即使看到明确语义规则，也常未让该规则真正控制结论。由于一对中的公式不变而正确标签相反，低分不能仅解释为公式普遍困难；它更具体地反映模型忽略或误用语义干预。不过，该结果只覆盖给定模型端点、提示和题集，不能推出所有语言模型都无法遵循模态语义。

<div class="result-source" markdown="1">

来源：第6节“ A failure of semantic control”；具体逐模型数值见表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Four of five models score below the 50% condition-only baseline under direct prompting, ranging from 2.5% to 25.0%; only Sonnet exceeds it at 65.0%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### DeepSeek V4 Flash 在相同核心集上由直接推理切换为 high reasoning

<div class="result-value" markdown="1">

严格配对准确率从 $4.4\%$ 提升至 $88.1\%$，增加 $83.7$ 个百分点；提示内容保持不变。

</div>

作者将其解释为推理时计算不仅提高一般准确率，还改变了模型是否会对语义条件差异作出有效响应。该对照有力表明推理模式是独立于模型身份的重要变量，但它不是严格的算力因果分解，也不意味着开启推理后必然正确；论文明确指出模型仍可能在推导中偷带未声明的框架性质。

<div class="result-source" markdown="1">

来源：第6节“Reasoning can restore control”；核心集区间见表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

With unchanged prompts, DeepSeek V4 Flash rises from 4.4% to 88.1% on the balanced core; the pattern also appears on the broader Frame and Domain sets, and for Luna on Frame.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 省略 Frame 问题的显式框架规格后进行语义亲和性诊断

<div class="result-value" markdown="1">

模型的回答与 K 或 T 等熟悉模态逻辑呈现连贯亲和性，但这些默认偏好不能可靠预测模型在显式指定语义时会犯哪些错误。

</div>

这说明模型在条件缺失时并非完全随机，而可能依赖训练中形成的默认逻辑；然而“默认逻辑恰好合适”与“能够服从当前声明的模型类”是两种能力。该实验是向标准逻辑判断向量的匹配诊断，不直接证明模型内部存储或执行了某个形式化逻辑系统。

<div class="result-source" markdown="1">

来源：第6节“Defaults are real, but not decisive”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Without specifications, models exhibit coherent affinities with familiar logics such as K or T.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 核心结论来自五个带日期的商业或托管模型端点、零温度单次采样和特定提示模板；端点更新、重复采样或其他提示策略可能改变结果，因此不宜把排名外推到整个模型家族。
- 部分数据只能由一个自动定理证明器作出决定性解析：全部 $1600$ 个已接受侧面中，$727$ 个获得双证明器一致结果，$873$ 个只有一个决定性结果且无冲突。虽然作者保留完整证明工件、拒绝冲突和未解决样本，并对核心集无效侧另做独立反模型核验，但完整集合的验证强度并非处处相同；此外，表示实验只有 $50$ 对，适合诊断敏感性而不足以建立普遍格式排序。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 条件唯一基线：在平衡核心集上，仅把每个语义条件映射到其最有利标签而不读取公式，可获得 $50\%$ 严格配对准确率。它是关键比较线，因为超过该值才说明模型同时利用了公式内容与条件，而非从条件本身猜测标签。
- 独立随机回答：分别随机判断一对问题的两侧，期望严格配对准确率为 $25\%$。它刻画在二元标签上同时猜对两侧的机会水平。
- 常量回答或固定语义策略：始终输出同一标签，或者无视显式条件、对两侧套用同一套固定语义，在标签相反的配对设计下严格配对准确率为 $0\%$。该基线直接对应“没有响应语义干预”的失败模式。
- 熟悉逻辑亲和性参照：删除 Frame 问题中的框架规格后，将模型的判断向量与 K、D、T、B、S4、S5 六种标准模态逻辑比较，并对各类对比等权、保留并列。它用于诊断模型默认采用哪套逻辑，但不是显式条件评测中的性能上界。

**实验想回答的问题**

- 当一对问题保持前提与待证公式完全相同、只改变显式给定的模态语义条件时，语言模型能否据此作出相反且正确的有效性判断，而不是沿用固定的熟悉逻辑或仅根据条件名称猜答案？
- 推理模式、语义条件的表示方式以及省略框架条件后模型表现出的默认逻辑偏好，会如何影响模型遵循指定模态语义的能力？

**实验实现**

作者通过 OpenRouter 评测带日期版本的 DeepSeek V4 Flash、DeepSeek V4 Pro、GPT-5.6 Luna、GPT-5.6 Terra 和 Claude Sonnet 5。直接推理条件下，每个模型以温度 $0$、每侧一次响应完成全部 $800$ 对；原始响应先原样保存，格式错误不修复并直接计错。额外实验保持提示不变：Flash 以 high reasoning 运行全部 $400$ 对 Frame、全部 $400$ 对 Domain 及完整核心集，Luna 以 medium reasoning 运行 Frame；三种表示的匹配实验使用主表中的 Terra 端点。逻辑题以非经典 TPTP 序列化，经 LET 嵌入转换为高阶逻辑，再由 Vampire 与 Leo-III 返回证明或反模型状态；作者不把“未证明有效”当作无效，并剔除冲突、未解决或超时的候选。二元准确率和解析率报告 $95\%$ Wilson 区间，跨轴非加权均值使用分层配对 bootstrap。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 推理模式消融：DeepSeek V4 Flash 的 direct 与 high reasoning，核心集提示及题目保持不变 | 严格配对准确率由 $4.4\%$ 上升到 $88.1\%$；表2还显示 high reasoning 的 Pair parse 为 $99.4\%$，因此增益不能主要归因于修复不可解析输出。 | 该消融主要隔离推理时计算强度，而没有更换题目或提示。大幅变化表明模型原本可能具备相关推理资源，但在直接模式中没有稳定调用。由于服务端推理模式的内部机制未被进一步拆分，实验不能确定究竟是更长推导、搜索策略还是其他隐藏配置造成增益。 | 第6节“Reasoning can restore control”；表2<br><span class="experiment-evidence">With unchanged prompts, DeepSeek V4 Flash rises from 4.4% to 88.1% on the balanced core; the pattern also appears on the broader Frame and Domain sets, and for Luna on Frame.</span> |
| 表示方式消融：GPT-5.6 Terra 在同一确定性 $50$ 对 Frame 子集上比较命名条件、关系定义和 TPTP | 严格 Frame 准确率分别为 $38\%$、$6\%$ 和 $44\%$；从命名条件改为关系定义下降 $32$ 个百分点，改为 TPTP 则比命名条件高 $6$ 个百分点。 | 该匹配实验固定模型端点、问题子集和其余字段，主要隔离语义规则的表达形式。Terra 对关系定义尤其敏感，而 TPTP 略优于命名条件；但作者指出其他模型的排序不同，所以不能把 TPTP 视为普遍修复方案，也不能仅凭该 $50$ 对小规模试验断言形式语法总体更优。 | 第6节“Representation is not a simple fix”<br><span class="experiment-evidence">For Terra, strict Frame accuracy moves from 38% with named conditions to 6% with relational definitions and 44% with TPTP; the other models show different rankings.</span> |

**定性案例**

- 论文给出的代表性错误是：模型生成看似合理的推导，却引入题目未声明的框架性质，例如在实际需要传递性的步骤中擅自使用自反性。这表明输出具有推理外观并不足以证明模型遵守了指定语义；核查时必须逐步确认每个模态推理规则是否由当前框架或域条件授权。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces a controlled modal-logic evaluation to test whether language models reason according to explicitly stipulated semantics.; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`d8a5d657bbbd2fd6a19b9f1133ef96d74d3622563c8ea76cc0297fe18c72114e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
