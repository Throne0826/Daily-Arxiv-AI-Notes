---
title: "[论文解读] REAP: Relation-Aware Elicitation and Parsing for Closed-Book Knowledge Base Construction from LLMs"
description: "[arXiv 2608.10963][LLM Reasoning] REAP研究如何在禁止外部检索、不得微调且模型规模不超过$32$B参数的条件下，从大语言模型的参数化知识中尽可能完整地提取不同基数的事实对象集合，并稳定输出为合法JSON数组。"
arxiv_id: "2608.10963"
announcement_date: "2026-08-12"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-12T03:08:57.666322+00:00"
source_sha256: "c6353f6881d97b03c8dc62e9758a8a6a8d79bf859a42a63ddafce400e1df8fa4"
tags:
  - "LLM Reasoning"
  - "闭卷知识库构建"
  - "参数化知识"
  - "大语言模型知识探测"
  - "可变基数答案集合"
  - "关系特定提示"
  - "空集判定"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.10963</p>

# REAP: Relation-Aware Elicitation and Parsing for Closed-Book Knowledge Base Construction from LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-12</span>
<span><strong>作者</strong> Thanh-Dan Bui, Thanh-Trung Do, Tuan-Phong Nguyen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: VNU University of Engineering and Technology, Hanoi, Vietnam</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.10963v1) · [PDF 下载](https://arxiv.org/pdf/2608.10963v1) · **关键词** 闭卷知识库构建, 参数化知识, 大语言模型知识探测, 可变基数答案集合, 关系特定提示, 空集判定<br>
**代码**: [https://github.com/yammdd/AKBC-Shared-Task-2026](https://github.com/yammdd/AKBC-Shared-Task-2026)

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

REAP研究如何在禁止外部检索、不得微调且模型规模不超过$32$B参数的条件下，从大语言模型的参数化知识中尽可能完整地提取不同基数的事实对象集合，并稳定输出为合法JSON数组。

**不用术语来说**：给定一个实体和一种关系，例如“某国与哪些国家陆地接壤”或“某公司在哪些证券交易所上市”，系统需要仅凭模型内部记忆返回全部答案；答案可能不存在、只有一个或有多个，还可能是需要足够精确的数值。困难不只是让模型“知道一个答案”，而是同时判断应不应该有答案、找全所有答案、避免编造，并严格遵守机器可读取的JSON格式。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出关系感知的事实引出策略：依据关系的语义与答案结构采用不同查询方式，包括带空集门控的结构化推理、用于陆地边界的四方向地理扫描，以及用于奖项获奖者的按时间多轮查询。
- 作者提出事实引出与答案序列化解耦的两阶段框架：第一阶段专注召回对象集合，第二阶段优先确定性解析，并仅在复杂输出无法直接解析时使用基于大语言模型的抽取作为后备。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型参数化知识探测与知识库构建领域。大语言模型会在参数中编码事实，但从模型中构建知识库并不等同于回答单个事实问题：系统必须针对给定的主语—关系对 $(s,r)$，找出完整的对象集合，并区分无答案、单答案和多答案情形。AKBC Shared Task 2026 进一步限定系统只能使用模型内部知识，不得检索外部资料或微调模型，因此研究重点是如何通过提示稳定地唤起已有知识，同时抑制幻觉、遗漏和格式错误。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**参数化知识（parametric knowledge）**

指语言模型在预训练过程中吸收并编码在模型参数中的事实知识。闭卷任务只能通过提示调用这些知识，不能借助搜索引擎、数据库或检索增强生成。

</div>
<div class="concept-item" markdown="1">

**知识库构建（knowledge base construction, KBC）**

把事实组织成结构化的主语—关系—对象记录；本任务固定主语与关系，要求系统补全所有正确对象。与普通问答相比，它还强调答案集合的完整性、对象数量不固定以及输出模式合法。

</div>
<div class="concept-item" markdown="1">

**完形提示与思维链提示**

完形提示把事实改写为待补全句子，通常适合预测单个对象；思维链提示则要求模型先逐步分析再给出答案。本文背景中的难点是，逐步推理虽有助于召回和判断空集，但并不能保证事实正确或答案完整。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

每条输入记录包含一个主语实体 $s$ 和六种指定关系之一的 $r$，系统需要输出与 $(s,r)$ 对应的完整对象集合 $O(s,r)$，并序列化为合法 JSON 数组。六类关系分别询问陆地接壤国家、死亡城市、场馆最大观众容量、奖项获得者、公司公开交易的证券交易所以及地理实体总面积；其中容量应为整数，面积以平方千米计且包含陆地与内陆水域。答案基数可能为 $0$、$1$ 或 $N$：例如岛国、仍在世或死亡城市未知的人、私营公司均可能对应空集。任务采用闭卷设置，禁止检索增强或其他外部知识，模型参数规模不得超过 32B，且不得进行模型微调；因此系统必须同时处理事实召回、空集判定、多对象穷举、数值精度和 JSON 格式约束。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$s$**

输入记录中的主语实体，例如某个国家、人物、场馆、奖项、公司或地理实体。

</div>
<div class="notation-item" markdown="1">

**$r$**

输入记录指定的目标关系，取自任务定义的六种关系。

</div>
<div class="notation-item" markdown="1">

**$O(s,r)$**

主语 $s$ 在关系 $r$ 下对应的完整对象集合；这是对任务输出的概括性记号。

</div>
<div class="notation-item" markdown="1">

**$\lvert O(s,r)\rvert \in \{0,1,N\}$**

答案集合可能为空、仅含一个对象或包含多个对象。

</div>

</div>

**直接相关的工作**

- **LAMA**: LAMA 使用完形填空式提示探测语言模型中的事实知识，但通常假定每个关系恰有一个对象，而且结果对提示措辞较敏感；因此它不能直接覆盖本任务要求的空集与多对象输出。
- **ReWiSe**: ReWiSe 是 LM-KBC 2025 的高表现系统，将思维链推理与按关系划分的自一致性结合。REAP 延续关系特定推理和显式空集处理的思路，但论文指出自一致性投票计算成本较高，并可能被多个自信却错误的推理链主导。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

AKBC Shared Task 2026要求系统把大语言模型内部记忆转化为可直接写入知识库的结构化事实。每条输入由主体$s$和关系$r$组成，目标对象集合可能是空集$$、单值或多值；同时，系统不能使用检索增强或任何外部知识，不得微调模型，参数量还必须不超过$32$B。因此，系统必须在信息来源受限的情况下兼顾事实覆盖率、幻觉控制、数值精度与输出格式有效性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **完形填空式事实探测与提示集成**：把主体与关系改写为带空缺的自然语言模板，让语言模型为候选对象打分或补全答案；提示集成则使用多个模板并汇总结果，以降低单一提示措辞带来的偏差。
- **单轮直接生成**：在一次提示中同时要求模型回忆与主体—关系对$(s,r)$对应的全部对象，并立即把结果序列化为规定的JSON数组。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 传统事实探测主要面向候选对象排序或孤立事实回答，不能自然处理知识库构建所需的可变基数集合，尤其难以统一应对空集、单值和长列表，也缺乏保证答案集合完整性的机制。
- 单轮直接生成把事实回忆、空集判断、完整性检查和格式控制压在同一次生成中，容易产生虚构对象、遗漏有效对象或违反JSON模式；对于面积和场馆容量等定量关系，回忆或舍入误差还可能使结果超出$5\%$相对容差。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种适用于严格闭卷约束的统一机制：它既要根据不同关系的答案结构主动引出模型中的参数化知识，又要可靠地区分无答案与未成功回忆、提高多值答案的覆盖率，并以较低额外计算成本把自由文本转换成合法的结构化集合。由于长尾实体知识本身可能未被模型充分编码，这一缺口不能仅靠扩大候选排序或加强格式指令解决。

</div>
<div markdown="1"><span>核心问题</span>

在不使用外部检索、不进行模型微调且模型规模受限的条件下，能否通过关系专用的推理与查询策略，把大语言模型内部不完整且分散的事实记忆引出为尽可能完整的对象集合，并通过混合解析稳定生成有效JSON？

</div>
<div markdown="1"><span>作者直觉</span>

不同关系需要不同的“回忆路线”：边界关系可按地理方向逐区检查，奖项可按年代分段搜索，而死亡城市或公司上市关系应先判断人物是否已去世、公司是否公开交易。先让模型围绕关系语义思考并核对是否应为空集，再单独完成格式化，可以减少内容推理与JSON语法相互干扰；简单输出由确定性程序直接解析，只有复杂输出才交给模型二次抽取，从而兼顾稳健性与成本。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

REAP把闭卷知识库构建设计成“关系感知的知识唤起，再进行受约束解析”的两阶段流程。输入是一个主体实体及待查询关系；第一阶段根据关系的基数、语义和常见错误选择专门提示，让不超过参数预算的语言模型从参数化知识中生成自由文本证据或逐步推理结果。多值关系通过时间段、地理方向等方式拆成多次查询以提高召回率，单值或可能无答案的关系则使用包含空集门控的推理流程。第二阶段读取规定标记后的内容，使用直接解析、正则表达式或必要时再次调用语言模型，将结果转换成合法 JSON 数组，并执行数值、名称和重复项规范化。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 关系识别与提示策略选择

系统按目标关系选择专用提示模板，并确定采用多轮分解查询还是带空集门控的逐步推理。每个关系固定使用一个正例和一个空集例；示例只来自训练集或人工编写三元组，原文称其不会使用评测划分中的样本。

<div class="method-step__io" markdown="1">

**输入**：主体实体、目标关系，以及该关系预先配置的静态少样本示例。<br>
**输出**：一组包含任务边界、推理步骤、输出标记和必要示例的关系专用提示。

</div>

**直观理解**：不同关系容易犯的错误不同，因此系统不使用同一套问法。例如，查获奖者重在避免漏人，查上市交易所则必须先判断公司是否真的独立上市。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 关系感知的知识唤起

语言模型生成自由文本证据或结构化思维链，并把候选答案写在 `BORDERS:` 或 `FINAL_ANSWER: [...]` 等标记之后。`awardWonBy` 使用一次一般查询和五次辅助查询，共六次以温度 $T=0.7$ 生成；其他关系使用各自的消歧、合法性检查、单位转换或范围核验流程。

<div class="method-step__io" markdown="1">

**输入**：关系专用提示和主体实体。<br>
**输出**：一个或多个带答案标记的原始模型响应，其中可能包含候选实体、数值、空数组或无法直接解析的文本。

</div>

**直观理解**：这一阶段相当于先让模型按检查清单回忆知识。对于答案很多的问题，系统从多个时间段或方向分别搜索模型记忆，再汇总各次找到的候选项。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 格式校验、重试与证据合并

系统检查响应是否包含预期标记以及标记后的内容能否解析；若生成结果不可解析，则自动重试或改用较短的后备提示。对于多轮查询，系统合并各轮证据，保留后续抽取所需的候选答案。

<div class="method-step__io" markdown="1">

**输入**：第一阶段生成的一个或多个原始响应。<br>
**输出**：格式可识别的合并证据，或明确表示无答案的空集结果。

</div>

**直观理解**：模型即使知道答案，也可能没有按要求书写；重试机制处理的是表达格式失败，而多轮合并处理的是每次只回忆出部分答案的问题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### JSON 抽取与规范化

系统优先直接解析 `FINAL_ANSWER:` 行，并用平衡括号扫描恢复被截断的 JSON 数组；定量关系再由正则表达式抽取整数或浮点数并删除千位分隔符和单位。规则难以可靠处理的多值关系可由语言模型完成抽取，随后系统清理称谓、年份、HTML、作品标题后缀及括号限定语，并进行不区分大小写的去重。

<div class="method-step__io" markdown="1">

**输入**：通过校验的标记化响应或合并证据。<br>
**输出**：符合任务格式的 JSON 数组，数组元素为规范化实体名称或数值字符串，也可能是空数组。

</div>

**直观理解**：最后一步把模型的解释文字变成知识库能够直接接收的标准字段。它还会把诸如 `1938: Albert Einstein`、`Guinea (West Africa)` 或带单位的数字还原成任务要求的核心值。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。REAP不对基础语言模型进行微调，也没有需要通过梯度优化的新训练目标；其性能来源于推理时的关系专用提示、多轮知识唤起、空集门控和确定性后处理。静态少样本示例用于展示推理链与何时输出空集，而不是用于参数更新。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 多值关系的分解式查询**

对于答案集合较大的关系，REAP把一次开放式查询拆成若干覆盖互补区域的查询。`awardWonBy` 按奖项创立至 1970 年代、1980 至 1990 年代、2000 至 2010 年代、2020 年以后以及较不知名或非西方获奖者等范围执行五次辅助查询，并加一次一般查询；`countryLandBordersCountry` 则分别检查东、西、南、北边界，只接受陆地边界并排除海上边界。

> 直观理解：单次回答容易先列出最著名的几个对象便停止。把答案空间切成时间段或地理方向，相当于让模型逐格检查清单，从而减少遗漏小国、飞地邻国或较少被提及的获奖者。

**2. 结构化推理与空集门控**

单值关系和带适用条件的关系使用固定步骤的思维链，并在输出前执行关系合法性判断。`companyTradesAtStockExchange` 先识别公司，再以严格公开上市检查排除私营公司、非营利组织和未单独上市的子公司；`personHasCityOfDeath` 先判断人物是否仍在世并处理同名歧义，只有确认死亡地点时才输出城市，否则返回 `FINAL_ANSWER: []`。

> 直观理解：空集不是“模型没想起答案”的随意替代，而是经过前置条件检查后的合法结果。该模块用于阻止系统给仍在世人物编造死亡城市，或把母公司的交易所错误赋给未单独上市的子公司。

**3. 关系专用消歧、校验与解析**

`hasArea` 先区分目标地理实体与其所属国家，保留小数精度并统一转换为 $\text{km}^{2}$；`hasCapacity` 先判断场馆类型和位置，再区分同名或同城场馆，并用小型场馆约 $1{,}000$ 至 $35{,}000$ 座、大型国家体育场约 $35{,}000$ 至 $100{,}000$ 座的范围检查估计。生成后，解析器按关系选择直接 JSON 解析、正则抽取、平衡括号恢复或语言模型抽取，并执行名称清洗和去重。

> 直观理解：该模块同时处理“问的是哪个对象”和“答案应写成什么形式”两个问题。范围检查不是新的知识来源，而是用于发现明显选错同名场馆或数量级不合理的候选值。

**训练与推理**

训练阶段不存在模型参数更新。系统预先为每种关系编写提示模板，并固定配置一个正例和一个空集例；这些示例来自 `train.jsonl` 或人工编写三元组。推理时，给定主体与关系，系统先载入相应模板：多值关系执行多轮互补查询，单值关系执行规定的逐步推理和空集检查。模型按标记输出候选答案；若缺少标记或结果不可解析，系统重试或使用后备提示。随后系统合并多轮证据，以规则优先、语言模型补充的方式抽取数组，最后进行数值和实体名称规范化，输出合法 JSON 数组。

**复现信息**

系统使用 `Mistral-Small-24B-Instruct-2501` 作为闭卷知识来源，符合最多 32B 参数且不允许微调的任务约束。只有 `awardWonBy` 的六次生成明确报告使用温度 $T=0.7$，其目的是让不同轮次产生更具互补性的候选项；原文片段未明确报告其他关系的解码参数。输出协议依关系使用 `BORDERS:` 或 `FINAL_ANSWER: [...]`，解析器支持平衡括号扫描，以恢复截断但仍可识别边界的数组。数值处理删除千位分隔符与单位；名称处理删除年份前缀、HTML 标签、作品标题后缀、`Dr.`、`Prof.`、`Sir`、`Dame`、`Lord`、`Saint`、`St.`、`Mr.` 等称谓及尾部括号说明，并在不区分大小写的条件下去重，同时保留首次出现项的大小写形式。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- AKBC Shared Task 2026 官方数据包含训练、验证和测试划分，覆盖六种关系。每条记录由一个主语、一种关系以及一组带别名列表的对象构成；答案基数包括空集、单值和多值。该设计同时检验模型是否知道事实、能否完整枚举多个对象，以及能否在无答案时返回空集。原文举例说明，新西兰的陆地边界是空集，而训练集中的 Nobel Prize in Physics 最多涉及 229 名获奖者、验证集中的 AAAI Fellow 涉及 350 人，表明长列表召回是核心难点。
- 验证集共 475 条记录，用于模型选择、零样本与两阶段流程比较，以及减法消融。六种关系的记录数并不完全均衡：countryLandBordersCountry 为 68 条，hasCapacity 为 97 条，awardWonBy 为 10 条，其余三种关系各 100 条。因此总体 macro-F1 虽按记录平均，但少样本关系的关系级结果仍可能具有较高方差。
- 官方测试集共 475 条记录，用于最终系统比较和关系级泛化评估。其中 countryLandBordersCountry 为 67 条，hasCapacity 为 98 条，awardWonBy 为 10 条，其余三种关系各 100 条。测试集覆盖 awardWonBy、companyTradesAtStockExchange、countryLandBordersCountry、hasArea、hasCapacity 和 personHasCityOfDeath 六种关系。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Macro-Precision、Macro-Recall 与 Macro-F1**

评估脚本先在每条记录上比较预测对象集合与真实对象集合，再汇总精确率、召回率及其调和平均。论文特别说明总体 macro-F1 是逐记录 F1 的均值，因此每条记录权重相同；它同时惩罚多报对象造成的假阳性和漏报对象造成的假阴性。 （越高越好。精确率高表示较少生成错误对象，召回率高表示较少遗漏真实对象，F1 高表示二者取得较好平衡。）

</div>
<div class="metric-item" markdown="1">

**Micro-Precision、Micro-Recall 与 Micro-F1**

组织方脚本也报告 micro 指标，即在更整体的匹配统计上计算精确率、召回率和 F1，因而包含对象数量较多记录的更强影响。所给结果章节主要展示 macro-F1，未给出 micro 指标的具体数值。 （越高越好；但它与 macro 指标回答的问题不同，不能仅凭 micro-F1 判断每条记录是否得到均衡处理。）

</div>
<div class="metric-item" markdown="1">

**关系级 Macro-F1**

在每一种关系内部计算逐记录 F1 的平均值，用来区分系统在哪些事实类型上有效。字符串关系先进行规范化，并通过最大二分图匹配处理对象别名；数量关系允许 5% 的相对误差，从而避免仅因可接受的数值近似而判错。 （越高越好。它适合诊断长列表、空集、单值字符串和数量关系之间的难度差异，但不同关系的样本数不同，不能把关系级分数直接解释为同等精度的总体能力估计。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 验证集上的直接零样本查询，比较 Llama-3.1-8B、Gemma-2-9B 与 Mistral-24B。

<div class="result-value" markdown="1">

三种模型的 macro-F1 分别为 0.38、0.42 和 0.43，差距很小且整体偏低。作者据此认为，仅靠直接提示时，模型难以同时完成闭卷事实回忆和严格输出格式控制，尤其容易在长多值关系与精确数量关系上失败。

</div>

这一结果建立了 REAP 所面对的基础难度：扩大到 24B 参数并未让直接查询出现明显跃升，说明问题不只是模型容量不足，还涉及如何组织检索式推理与输出。它并不能单独证明错误主要来自格式，因为实验没有在这里分别报告事实正确但格式无效、格式正确但事实错误的比例；关于两类困难并存的判断是作者结合任务现象给出的解释。

<div class="result-source" markdown="1">

来源：第 4.2 节，Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Figure 2, Llama-3.1-8B, Gemma-2-9B, and Mistral-24B achieve macro-F1 scores of 0.38, 0.42, and 0.43, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 验证集上，将三种底层模型分别从直接零样本查询切换为 REAP 两阶段流程。

<div class="result-value" markdown="1">

Llama-3.1-8B 从 0.38 提升至 0.48，Gemma-2-9B 从 0.42 提升至 0.51，Mistral-24B 从 0.43 提升至 0.65；其中 Mistral-24B 的绝对增益为 0.22，因而被选为最终提交模型。

</div>

同一流程在三个模型家族上都提高 macro-F1，支持流程设计具有一定跨模型可迁移性；Mistral-24B 的提升最大，也说明较强底层模型可能更能利用结构化推理。不过，这不是严格的单变量组件证明，因为完整 REAP 同时加入了推理、关系特定查询、空集判断和解析；各组件的独立作用需要结合消融判断。

<div class="result-source" markdown="1">

来源：第 4.2 节 Effectiveness of the Two-Stage Pipeline，Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Llama-3.1-8B improves from 0.38 to 0.48, Gemma-2-9B from 0.42 to 0.51, and Mistral-24B from 0.43 to 0.65.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 官方测试集上，比较完整 Mistral-24B REAP、Llama 与 Gemma 的 REAP 配置，以及组织方 Qwen3.5-9B 基线。

<div class="result-value" markdown="1">

完整系统总体 macro-F1 为 0.62，高于 Llama 和 Gemma 流程的 0.48，也高于组织方基线的 0.30。关系级上，countryLandBordersCountry 达到 0.95、hasArea 达到 0.77、companyTradesAtStockExchange 达到 0.73；但 hasCapacity 仅为 0.23，awardWonBy 为 0.37，显示性能仍明显依赖关系类型。

</div>

测试结果表明验证集上的模型选择能够迁移到官方测试集，并且最终系统在全部六种关系的 F1 上均领先所比较配置。总体 0.62 是六类记录混合后的逐记录平均，不能理解为系统掌握了 62% 的全部事实，也不能证明其对未见关系具有泛化能力。作者使用“significantly outperforming”描述领先，但所给章节没有报告置信区间、重复运行方差或统计显著性检验，因此这里应将其理解为较大的分数差，而非已验证的统计显著性。

<div class="result-source" markdown="1">

来源：第 4.3 节，Table 2 与 Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Overall, the Mistral pipeline leads with a macro-F1 score of 0.62, significantly outperforming the Llama (0.48) and Gemma (0.48) pipelines, as well as more than doubling the organizer’s baseline that is based on Qwen3.5-9B (0.30).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验范围仅包含共享任务规定的六种关系、一个最终主模型和单一官方数据分布；虽然流程在三种模型上均有验证集增益，但原文没有测试未见关系、跨知识库迁移、模型规模连续变化或其他闭卷知识抽取数据集。因此现有结果支持任务内泛化，不能直接推出开放域知识库构建的一般有效性。
- 结果主要依赖单次 macro-F1，未报告随机种子、重复运行方差、置信区间或显著性检验；awardWonBy 在验证集和测试集中都只有 10 条记录，关系级分数尤其容易受少量样本影响。此外，消融只给出总体和若干关系的 F1 变化，没有分别报告空集、单值、多值样本上的 precision/recall，也没有拆分事实错误与 JSON 格式错误，因而对具体失效机制的归因仍需源代码与更细粒度评估复核。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 直接零样本查询：对每个模型直接提问，不生成证据，也不进行思维链推理。它控制了底层模型不变，因而是判断 REAP 两阶段推理与解析流程是否真正增加价值的最直接基线。
- Llama-3.1-8B-Instruct：参数规模较小的指令模型，同时评估其直接零样本版本和 REAP 版本。它用于检验流程收益是否只存在于主模型 Mistral-24B，还是能跨模型出现。
- Gemma-2-9B-it：另一种约 9B 规模、不同模型家族的指令模型。与 Llama 一起构成跨架构比较，可降低把流程增益误归因于某一个模型家族的风险。
- 组织方 Qwen3.5-9B 基线：官方测试集上的共享任务参照系统，用于衡量最终提交相对标准方案的竞争力。原文只说明该基线基于 Qwen3.5-9B，未在所给章节中明确报告其提示模板、推理流程或其他实现细节。

**实验想回答的问题**

- 在不微调模型、闭卷调用参数知识并要求输出合法 JSON 数组的条件下，REAP 的两阶段流程是否比直接零样本查询更能兼顾事实召回与格式遵循？这一问题通过同一验证集上三种指令微调模型的零样本版本与 REAP 版本进行配对比较。
- REAP 的收益主要来自哪类设计：结构化思维链推理、按关系拆分任务，还是用于拒绝无答案实体的空集门控？进一步地，这些收益能否从验证集迁移到官方测试集，并在不同关系和对象基数下保持稳定？

**实验实现**

实验评估 Gemma-2-9B-it、Llama-3.1-8B-Instruct 和 Mistral-Small-24B-Instruct-2501 三种指令微调模型，最终系统选择 Mistral-24B。验证阶段先以不生成证据、无思维链的直接查询作为零样本条件，再对同一批模型应用 REAP 两阶段流程；消融则固定 Mistral-24B，在验证集上逐项移除组件。官方测试阶段报告最终系统的总体及关系级 macro-F1，并与另外两种 REAP 模型配置及组织方 Qwen3.5-9B 基线比较。实验在 Kaggle TPU v5e-8 上运行，使用 vLLM TPU Server、bfloat16 精度和批量大小 32；对验证集全部 475 条记录完成一次六关系运行约需 2–5 分钟。评估统一使用组织方的 evaluate.py：字符串对象经过规范化和别名最大二分图匹配，数量对象采用 5% 相对容差。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 在验证集的 Mistral-24B 完整流程中移除全部思维链推理，退化为零样本直接查询。 | 总体 macro-F1 从 0.65 降至 0.43，绝对下降 0.22，是表中最大的组件移除损失；hasArea 从 0.82 降至 0.55，countryLandBordersCountry 从 0.98 降至 0.27。 | 该消融隔离了结构化推理相对直接查询的总体作用。大幅下降支持作者的核心主张：增益主要来自先组织和唤起模型内部参数知识，而非仅把最终文本转换成 JSON。需要注意，原文把这一条件称为“w/o CoT (Zero-Shot)”，它可能同时改变提示内容与中间推理过程，因此不能进一步断言某一种具体思维链格式是唯一有效原因。 | 第 5 节，Table 3<br><span class="experiment-evidence">Finally, removing CoT Reasoning entirely causes the largest drop to 0.43, heavily degrading hasArea (0.82 to 0.55) and countryLandBordersCountry (0.98 to 0.27), confirming that our gains stem primarily from structured parametric reasoning rather than output parsing alone.</span> |
| 在验证集的 Mistral-24B 完整流程中移除 Empty-Set Gate。 | 总体 macro-F1 从 0.65 降至 0.57，绝对下降 0.08；personHasCityOfDeath 从 0.50 降至 0.36，companyTradesAtStockExchange 从 0.76 降至 0.57。 | 该消融检验显式空集判断是否能减少无答案记录上的幻觉。下降集中出现在容易错误补全对象的关系上，与门控旨在抑制假阳性的设计一致，因而主要说明其精确率价值。它不表示系统能够可靠识别所有不可回答事实，因为论文没有单独报告空集检测准确率、空集与非空集的混淆矩阵或门控阈值敏感性。 | 第 5 节，Table 3<br><span class="experiment-evidence">Removing the Empty-Set Gate lowers macro-F1 to 0.57 due to hallucinated answers for unanswerable entities, severely hurting precision on personHasCityOfDeath (0.50 to 0.36) and companyTradesAtStockExchange (0.76 to 0.57).</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The system primarily contributes structured reasoning and relation-specific elicitation strategies for extracting parametric knowledge from an LLM.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`c6353f6881d97b03c8dc62e9758a8a6a8d79bf859a42a63ddafce400e1df8fa4`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
