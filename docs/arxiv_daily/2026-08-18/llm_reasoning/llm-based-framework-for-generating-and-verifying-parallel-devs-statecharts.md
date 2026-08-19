---
title: "[论文解读] LLM-based Framework for Generating and Verifying Parallel DEVS Statecharts"
description: "[arXiv 2608.14956][LLM Reasoning] 本文针对大语言模型从自然语言系统描述生成并行离散事件系统规范（PDEVS）状态图时容易产生逻辑错误的问题，引入基于命题逻辑可满足性与蕴含检查的受控纠错循环，以提高生成结果与预期行为的一致性。"
arxiv_id: "2608.14956"
announcement_date: "2026-08-18"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:23:51.288408+00:00"
source_sha256: "62bbebdaa21e800172d2880bd0347b3dd6049b500bbca56d9f9a7fd8bdcb8b44"
tags:
  - "LLM Reasoning"
  - "行为建模"
  - "并行DEVS状态图"
  - "大语言模型"
  - "布尔逻辑蕴含"
  - "模型检查"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.14956</p>

# LLM-based Framework for Generating and Verifying Parallel DEVS Statecharts

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Vamsi Krishna Vasa, Hessam S. Sarjoughian, Edward J. Yellig</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> organization=Arizona State University, city=Tempe, state=Arizona, country=USA；organization=Intel Corporation, city=Chandler, state=Arizona, country=USA；organization=Arizona State University；organization=Intel Corporation</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.14956) · [PDF 下载](https://arxiv.org/pdf/2608.14956) · **关键词** 行为建模, 并行DEVS状态图, 大语言模型, 布尔逻辑蕴含, 模型检查<br>


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

本文针对大语言模型从自然语言系统描述生成并行离散事件系统规范（PDEVS）状态图时容易产生逻辑错误的问题，引入基于命题逻辑可满足性与蕴含检查的受控纠错循环，以提高生成结果与预期行为的一致性。

**不用术语来说**：把一段系统行为描述直接交给大语言模型后，模型可能生成看似合理、实际上遗漏条件或彼此矛盾的状态变化规则；系统越复杂，这类错误越难依靠人工发现。由于生成的状态图最终要用于仿真，错误规则会使仿真行为偏离原系统，因此需要在生成过程中自动检查并纠正这些规则，而不能只检查文本或代码是否形式正确。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出一种面向原子PDEVS状态图生成的逻辑验证机制：分别从系统描述中获得候选PDEVS事实和关键行为条件，将二者转换为命题逻辑，并通过可满足性与蕴含关系检查候选事实是否自洽且覆盖预期行为。
- 设计有限次数的增量、迭代式受控纠错循环，将验证发现的不一致转化为修改提示，驱动大语言模型重新生成候选事实，并据此产生逻辑一致性更高的PDEVS状态图。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于建模与仿真、形式化验证和大语言模型辅助建模的交叉领域。研究对象是原子并行离散事件系统规范（Parallel DEVS，PDEVS）模型的行为状态图：建模者先用自然语言描述系统预期的输入、输出、状态变化和时间相关行为，再将描述形式化为可仿真的状态模型。现有智能体式大语言模型能够从系统描述生成支撑状态图构造的“似真事实”，但语言上的合理性不等于逻辑正确性；随着行为复杂度增加，生成事实可能彼此冲突或偏离原始描述，进而使状态图出现结构和行为错误。因此，本文关注如何在保留人工建模者参与的条件下，用命题逻辑检查和受控迭代修正提高生成结果与系统描述之间的逻辑一致性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**并行离散事件系统规范（PDEVS）**

PDEVS是一种描述离散事件系统的形式化方法，将系统行为表示为状态、输入事件、输出事件、状态转换以及时间推进规则。本文具体处理原子PDEVS模型，即不再由更小子模型组合而成的基本行为单元。

</div>
<div class="concept-item" markdown="1">

**PDEVS状态图**

PDEVS状态图以图形化方式表达原子模型的状态及其事件驱动转换，同时要反映时间相关行为。它不仅应当看起来符合自然语言描述，还必须具有一致的逻辑结构并能正确表示预期动态。

</div>
<div class="concept-item" markdown="1">

**命题逻辑蕴含与可满足性**

命题逻辑把行为条件和生成事实转换为真假命题及其逻辑组合；可满足性检查这些约束能否同时成立，蕴含检查一组事实是否足以推出要求的行为条件。本文以这两类检查识别冲突或缺失，并据此构造修正提示。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是人工建模者提供的概念性系统描述提示，其中表达系统预期的结构和动态行为。智能体式大语言模型首先从该提示生成“似真事实”，即用于构造PDEVS状态图的候选行为规格；同时从同一描述提取这些事实应满足的关键行为条件。框架将两者转换为命题逻辑，在有限次数内进行可满足性与蕴含验证，并依据验证结果生成修改提示，以迭代或增量方式重新生成事实及PDEVS状态图。输出是逻辑上更贴合原始系统描述的原子PDEVS状态图；其逻辑正确性还可通过人工构造对应的时间自动机，并检查死锁与可达性属性来验证。该设定并非完全自动建模：人工建模者仍负责审查结果，并决定是否继续迭代生成。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **基于语法的PDEVS-LLM智能体框架（文献30）**: 这是本文直接扩展的生成框架：它依据PDEVS形式化语法和PDEVS状态图语法，从系统描述生成似真事实及状态图。本文针对其生成事实可能存在逻辑不一致的问题，增加行为条件提取、命题逻辑验证和受控修正循环。
- **使用Classic DEVS建模语法、简单系统提示和Co-Pilot的GPT-4可仿真代码生成方法（文献6）**: 该工作说明大语言模型可以在形式化语法约束下从文本生成可仿真的DEVS代码，但原文指出此类方法仍需要专家建模者检查生成模型及代码的正确性和可行性；本文进一步处理生成行为规格的逻辑验证问题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

可执行仿真模型必须同时符合领域行为和PDEVS建模规则，但从概念性自然语言描述生成状态图要求建模者具备领域、建模与仿真三方面知识。大语言模型虽能降低建模门槛，其生成的候选事实却可能包含规则冲突、条件遗漏或行为错配，导致状态图无法准确表达系统动力学，并把大量核查与修正工作留给专家。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于语法或元模型约束的大语言模型生成**：既有研究向GPT类模型提供Classic DEVS或PDEVS语法、状态图语法、活动模型元模型以及系统描述提示，让模型抽取规格并进一步生成可仿真的代码或状态图。此类方法主要约束输出的表示形式与建模结构。
- **基于候选事实的PDEVS-LLM代理框架**：代理先从系统描述中生成一组看似合理的PDEVS事实，再以这些事实为中间规格生成PDEVS状态图；候选事实由此承担从自然语言需求到形式化行为模型之间的桥梁作用。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 语法或元模型约束能够帮助大语言模型产生形式上像PDEVS模型的结果，却不能保证其行为逻辑与原始系统描述一致；随着行为复杂度提高，内部转移、输出及其触发条件更容易发生逻辑错配，仍需专家逐项检查。
- 既有PDEVS-LLM缺少对候选事实的自动正确性验证和反馈修正机制；一旦中间事实存在矛盾或遗漏，错误会继续传递到最终状态图乃至仿真代码，使生成流程难以形成可控的质量闭环。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作已经能够从文本生成PDEVS规格和状态图，但尚缺少一种以原始系统描述为依据、可机器执行且能把验证结果反馈给生成器的中间规格验证机制。该机制需要同时判断候选事实自身是否可成立，以及这些事实是否足以推出系统描述要求的关键行为，而不只是验证输出是否符合语法。

</div>
<div markdown="1"><span>核心问题</span>

能否将系统描述导出的关键行为条件与大语言模型生成的PDEVS候选事实统一表示为命题逻辑，并利用可满足性和逻辑蕴含检查构造有限次受控纠错循环，从而提高最终PDEVS状态图的逻辑完整性与行为准确性？

</div>
<div markdown="1"><span>作者直觉</span>

最终状态图的行为取决于上游候选事实，因此在状态图生成之前纠正这些事实，可以阻止错误继续向后传播。直观地说，系统描述给出了模型“必须做到什么”，候选事实说明模型“准备怎样做”；若后者内部无矛盾，并且在逻辑上能够推出前者的关键条件，就更有可能生成符合预期的状态图。检查失败时，将具体冲突或缺失反馈给大语言模型，也比无目标地重复生成更可控。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把自然语言组件描述$N$转换为可验证的原子Parallel DEVS（PDEVS）状态图$SC$。端到端流程分为四阶段：首先并行生成候选PDEVS事实与行为条件；其次把两者翻译为共享命题体系下的命题逻辑公式，并用SAT求解器分别排除内部矛盾；然后按外部转移、内部转移和输出三类执行分离式蕴涵验证，只把未被事实支持的条件反馈给生成代理进行受控修正；最后选取全部条件均通过验证的事实，或在达到修正上限时选取蕴涵条件数最多的版本，由状态图生成代理输出$SC$。输入是组件的自然语言系统描述，主要中间结果是自然语言事实、行为条件及其逻辑公式，最终结果是符合给定EBNF语法的PDEVS状态图，并可进一步转换为XML和PlantUML表示。
技术上，框架没有直接对LLM生成的状态图做端到端修补，而是把上游的自然语言行为事实视为状态图的语义来源，在生成状态图之前完成一致性与覆盖性检查。直观地说，它先从需求文档分别整理“模型打算怎样运行”和“模型必须怎样运行”两份清单，再把清单翻译成SAT求解器可判定的逻辑表达；若某项必需行为尚未被候选事实推出，就只针对缺失项要求LLM补写。这样既保留LLM处理自然语言与生成结构化模型的能力，又用确定性的逻辑检查约束反复生成过程，但其正确性仍依赖行为条件提取和自然语言到命题逻辑翻译是否忠实。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 行为条件识别与初始PDEVS事实生成

PDEVS Specification Generator代理采用few-shot提示，将$N$整理为JSON形式的候选事实，覆盖外部转移$\delta_{ext}$、内部转移$\delta_{int}$和输出函数$\lambda$；另一次LLM调用从同一描述提取原子化的外部、内部和输出行为条件$\{C_{ext},C_{int},C_{out}\}$。条件使用明确的状态、输入、动作和输出因果表述，事实生成代理保留对话历史并在系统提示中具备PDEVS规范知识。

<div class="method-step__io" markdown="1">

**输入**：组件的自然语言系统描述$N$。<br>
**输出**：自然语言PDEVS事实$\{\delta_{ext},\delta_{int},\lambda\}$与分类行为条件$\{C_{ext},C_{int},C_{out}\}$。

</div>

**直观理解**：这一步从同一份需求产生两种材料：一份是LLM提出的模型行为草案，另一份是之后验收草案所用的行为检查表。检查表被拆成不可再分的条件，便于准确指出究竟缺少哪一条行为。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 命题逻辑翻译与可满足性筛查

LLM把事实翻译为$\Gamma=\{\Gamma_{ext},\Gamma_{int},\Gamma_{out}\}$，把条件翻译为$\varphi=\{\varphi_{ext},\varphi_{int},\varphi_{out}\}$，并让两组公式共享命题定义；SAT求解器分别检查$SAT(\Gamma)$与$SAT(\varphi)$。条件只在第二阶段检查，事实则在后续每轮修正后重新检查；若不满足，则由专家或LLM重做，分别受事实修订上限$n$与条件修订上限$m$约束，超过上限仍不可满足便终止。

<div class="method-step__io" markdown="1">

**输入**：候选PDEVS事实、行为条件，以及从系统描述统一识别的命题符号。<br>
**输出**：各自内部一致、可满足的事实公式集$\Gamma$和条件公式集$\varphi$，或流程终止信号。

</div>

**直观理解**：可满足性检查回答的是“这份清单自身能否同时成立”，例如不能一边要求某状态成立、一边又无条件否定它。先排除清单内部冲突，才能让下一步的“事实是否支持条件”具有意义。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分离式蕴涵验证与受控修正

框架按$x\in\{ext,int,out\}$分别用$\Gamma_x$核验$\varphi_x$中的每个条件，并把未通过项映射回自然语言集合$C'_x$；仅将$C'=\{C'_{ext},C'_{int},C'_{out}\}$嵌入修改提示$M(C')$，要求代理补足必要端口、阶段、状态变量、转移与时间推进，同时保留已有必要行为。每轮新事实先重新通过$SAT(\Gamma)$再接受蕴涵检查；已经全部通过的类别可从后续验证中省略，循环最多执行预设的$g$轮。

<div class="method-step__io" markdown="1">

**输入**：通过可满足性检查的$\Gamma$、$\varphi$，以及对应的自然语言事实和条件。<br>
**输出**：全部条件均被支持的最终事实；若达到$g$仍未全部通过，则输出历次候选中蕴涵条件计数最高的事实版本。

</div>

**直观理解**：这相当于按“外部输入响应、模型自行演化、对外输出”三张检查表逐项验收，只把未达标条目退回修改。反馈范围受控可以减少LLM无关改写，但达到轮数上限时采用“通过条目最多”的版本只是一种保底选择，并不保证其完整正确。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### PDEVS状态图生成与表示转换

复用PDEVS-LLM中的Atomic Model Generator Agent，并在系统提示中提供EBNF形式的状态图语法，将事实解析为PDEVS状态图$SC$。框架还支持把$SC$转换为XML以存入关系数据库，以及转换为PlantUML语法用于可视化。

<div class="method-step__io" markdown="1">

**输入**：最终选定的自然语言PDEVS事实$\{\delta_{ext},\delta_{int},\lambda\}$。<br>
**输出**：原子组件的PDEVS状态图$SC$及其可选XML、PlantUML表示。

</div>

**直观理解**：前几步确定“状态图应表达什么”，最后一步才按固定语法把这些行为落成状态、转移和输出结构。语法约束主要保证表示形式可解析，而状态图的语义质量主要来自上游事实的验证结果。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 事实与行为条件的分类逻辑表示及可满足性门控

$$
\Gamma=\{\Gamma_{ext},\Gamma_{int},\Gamma_{out}\},\quad \varphi=\{\varphi_{ext},\varphi_{int},\varphi_{out}\},\quad SAT(\Gamma)=TRUE,\quad SAT(\varphi)=TRUE
$$

**符号说明**

- $\Gamma$：由自然语言PDEVS候选事实翻译得到的命题逻辑公式全集。
- $\Gamma_{ext},\Gamma_{int},\Gamma_{out}$：分别对应外部转移、内部转移和输出函数事实的命题逻辑公式集合。
- $\varphi$：由自然语言行为条件翻译得到的命题逻辑公式全集。
- $\varphi_{ext},\varphi_{int},\varphi_{out}$：分别对应外部、内部和输出行为条件的命题逻辑公式集合。
- $SAT(\cdot)$：由SAT求解器执行的可满足性判定；返回TRUE表示存在一种命题赋值使集合内公式同时成立。

<div class="equation-explanation" markdown="1">

**直观理解**：两组公式必须先分别“说得通”：候选事实不能内部矛盾，验收条件也不能内部矛盾。这里检查的不是事实是否满足条件，而只是为后续蕴涵验证建立一致的逻辑前提；条件达到$m$次、事实达到$n$次修订后仍不可满足时，算法终止。<br>
**原文位置**：第4.1节；算法1第6至26行

</div>

</div>

<div class="equation-block" markdown="1">

#### 分类未蕴涵条件收集与反馈修正

$$
C'_x=\bigcup_{k:\,\Gamma_x\not\models\varphi_{x_k}} C_{x_k},\quad x\in\{ext,int,out\};\qquad C'=\{C'_{ext},C'_{int},C'_{out}\},\quad M(C')\xRightarrow[\mathrm{Generator}]{\mathrm{PDEVS\ Specification}}\{\delta_{ext},\delta_{int},\lambda\}
$$

**符号说明**

- $x$：行为类别索引，取外部转移ext、内部转移int或输出out。
- $\Gamma_x$：类别x下的候选PDEVS事实公式集合。
- $\varphi_{x_k}$：类别x中的第k条行为条件公式。
- $\models$：语义蕴涵关系；这里表示事实集合在所有满足赋值下都能保证对应条件成立。
- $C_{x_k}$：与逻辑条件公式对应的第k条自然语言行为条件。
- $C'_x$：类别x中未被事实蕴涵的自然语言条件集合。
- $M(C')$：根据全部未通过条件构造的修改提示。
- $\delta_{ext},\delta_{int},\lambda$：修正后的自然语言外部转移事实、内部转移事实与输出函数事实。

<div class="equation-explanation" markdown="1">

**直观理解**：公式把每个类别中无法由候选事实推出的条件找出来，再将其自然语言版本合并成定向反馈；若$C'$为空，当前事实即可进入状态图生成，否则生成器依据$M(C')$更新事实。需要注意，算法1第30行原文排版写作$\varphi_{x_k}\not\models\Gamma_x$，但第4.2节文字明确说明是“condition ... checked for entailment against facts”，且方法目标是判断事实能否推出条件，因此此处按标准语义写为$\Gamma_x\not\models\varphi_{x_k}$；这一方向性差异需要结合作者代码进行源核查。<br>
**原文位置**：第4.2节；算法1第27至37行

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该框架不训练或微调LLM，也没有基于梯度的损失函数；所谓“改进”来自推理阶段的离散验证与提示反馈循环。SAT可满足性是候选能否继续处理的硬门控，分类蕴涵计数是修正循环达到上限$g$时选择候选版本的规则，而不是可微优化目标；因此不能把“最大蕴涵计数”解释为模型参数训练。作者的方法目标是提高PDEVS事实与系统描述所导出行为条件之间的逻辑一致性，最终状态图的完整性和正确性则在后续评估中检查。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. PDEVS事实与行为条件双路生成模块**

该模块从同一系统描述$N$形成两条相互独立但语义对应的表示：事实侧描述候选$\delta_{ext}$、$\delta_{int}$和$\lambda$，条件侧形成$C_{ext}$、$C_{int}$与$C_{out}$。事实代理采用few-shot提示、JSON输出和历史上下文；条件提示要求每条行为原子化，并区分外部输入触发、内部状态或时间触发以及状态变化前产生的输出。

> 直观理解：如果只让同一个生成结果自行证明正确，遗漏往往无法显现；双路生成相当于把“作答”和“出验收题”分开。它仍不是完全独立的金标准，因为两路内容均由LLM从同一描述提取，可能共享同一种误读。

**2. 共享命题空间下的SAT与分离式蕴涵验证模块**

模块先从$N$统一确定命题符号，避免事实公式与条件公式用不同符号表达同一概念；随后利用SAT求解器检查$\Gamma$和$\varphi$各自是否存在满足赋值。通过筛查后，验证按外部、内部和输出三个互不混合的子空间进行，使每个$\varphi_{x_k}$只与同类事实$\Gamma_x$比较；这种拆分符合PDEVS中转移函数可读写状态、输出函数原则上只读状态的职责差异。

> 直观理解：统一符号类似先约定同一本术语表，SAT检查负责发现自相矛盾，蕴涵检查负责发现行为遗漏。分类验证能更准确地定位错误来源，也避免某类事实偶然替另一类行为“作证”。

**3. 未蕴涵条件驱动的受控修正与状态图生成模块**

模块把未通过验证的条件集合$C'$序列化进$M(C')$，要求原事实生成代理返回完整更新后的JSON，而不是直接编辑逻辑公式或状态图；每个候选版本保留蕴涵计数，以支持达到上限$g$后的择优回退。最终事实送入带EBNF状态图语法的Atomic Model Generator Agent产生$SC$，因此验证反馈作用于状态图的自然语言语义前驱，而非最终图结构本身。

> 直观理解：系统只告诉生成器“哪些要求还没覆盖”，而不是要求它推倒重写全部模型，这就是受控修正。其优势是反馈具体、改动目标明确；局限是最终状态图生成仍可能引入从事实到图结构的新误差，本文方法描述中的逻辑闭环没有再次自动验证该转换。

**训练与推理**

训练过程：原文未提出新的模型训练、参数更新或微调，使用的是公开LLM的API式代理调用和独立LLM调用。推理过程：给定$N$，事实生成代理产生初始$\{\delta_{ext},\delta_{int},\lambda\}$，另一调用提取$\{C_{ext},C_{int},C_{out}\}$；再基于共享命题将二者翻译为$\Gamma$与$\varphi$。系统先在最多$m$次条件重做范围内获得可满足的$\varphi$；进入受控修正后，每轮又在最多$n$次事实重做范围内获得可满足的$\Gamma$，随后逐类判断事实是否蕴涵每条条件。若全部通过，则提前结束；若存在失败项，则用$M(C')$让保留历史的事实代理生成完整修订版，重新翻译、检查并循环，最多进行$g$轮。若始终未全部通过，选蕴涵条件总数最多的历史事实版本；最后Atomic Model Generator Agent依据EBNF语法生成$SC$。算法正文对循环条件使用$\#_{correction}\leq g$、$\#_{facts}\leq n$和$\#_{conditions}\leq m$，其实际最大调用次数可能涉及边界计数解释，复现时应以公开代码为准。

**复现信息**

公平复现所需的关键实现要点有四项。第一，事实和行为条件均采用JSON结构，事实代理的系统提示包含PDEVS规范知识并保留修改历史；条件提取提示必须要求原子条件，并明确区分内部行为、外部行为和输出行为。第二，自然语言到命题逻辑的翻译使用LLM调用，但事实与条件必须共享从系统描述识别出的命题定义，否则同义行为可能因符号不同而被误判为未蕴涵。第三，需要SAT求解器执行可满足性与蕴涵相关判定，并实现条件修订上限$m$、事实修订上限$n$、受控修正上限$g$、历史候选蕴涵计数及终止逻辑；给定节选未报告具体求解器、LLM名称、温度、$m$、$n$和$g$的数值。第四，状态图生成器的系统提示应包含EBNF语法，并实现到XML和PlantUML的转换；论文称代码与测试用例位于GitHub Repository，但本节选未给出可核验的具体URL。方法评估中用于UPPAAL模型检查的Timed Automata副本是人工构建的，因此它属于外部验证设施，不是上述自动生成流水线的一部分。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 完整测试集包含 14 个经过人工整理的独立原子组件系统描述，行为复杂度不同，并纳入离散事件系统基准模型 MiniFab 的组件。该集合用于 UPPAAL 模型检查，检验死锁和阶段可达性。
- 正确性评分实验从上述 14 个系统中选取行为复杂度较高的 8 个系统。领域专家依据原始系统描述，逐项判断状态图中的转移或输出是否必要，以及其守卫、消息、动作和时间推进是否正确。
- Phone 系统作为定性案例，包含 Off、On、SearchingForService、Ready 和 Active 五个阶段，以及服务可用性和来电队列等状态。它用于展示 SEV 每轮蕴含结果、验证前后状态图差异，以及状态图到 UPPAAL 时间自动机的人工映射过程。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**死锁失败系统数**

将生成的 PDEVS 状态图人工转换为 UPPAAL 时间自动机后，统计存在死锁的系统数量。死锁表示系统进入没有任何可执行后续行为的状态。 （越低越好，因为较少死锁意味着生成模型在更多可能执行路径上能够继续运行。）

</div>
<div class="metric-item" markdown="1">

**阶段可达性失败系统数**

统计无法满足目标阶段可达性性质的系统数量，即某些按描述应当能够到达的阶段在完整状态空间中不可达。 （越低越好，因为它表示状态图中的转移连接更完整，预期阶段更可能实际到达。）

</div>
<div class="metric-item" markdown="1">

**状态图正确性分数**

领域专家首先以 1 或 0 判断每个外部转移、内部转移或输出是否必要，并检查守卫、消息、动作和时间推进等属性；随后先在单个函数或转移内取平均，再分别汇总为外部转移、内部转移和输出函数分数。 （越高越好，1 表示被纳入计算的规格项与系统描述完全一致；但该指标依赖人工判断，且三个函数类别分别计分，并非一个自动化的整体语义等价指标。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 14 个系统上的 UPPAAL 模型检查，比较 8 种基础模型在验证前（BV）和验证后（AV）的死锁与阶段可达性失败数

<div class="result-value" markdown="1">

多数基础模型在验证后同时减少了死锁和阶段不可达系统数。例如 Llama-3.1-8b 的两类失败均由 5 个降至 2 个，GPT-4o-mini 均由 3 个降至 1 个，Llama-3.3-70b 均由 1 个降至 0 个；但 Mistral-7b-instruct 的死锁失败由 2 个增至 3 个。

</div>

作者据此主张，SEV 纠错通常能够改善状态图的全局行为性质，而且收益不仅出现在大模型上。分析上，这说明形式化反馈可以修复部分转移缺失或逻辑不一致，但不同模型并非稳定受益，Mistral-7b-instruct 的反例表明纠错循环也可能引入新的死锁。由于 UPPAAL 模型是人工转换的，这些数字同时受到转换准确性的影响。

<div class="result-source" markdown="1">

来源：表 6，Statechart Evaluation，第 6.1 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Llama-3.1-8b† | 5 | 2 | 5 | 2; Llama-3.3-70b‡ | 1 | 0 | 1 | 0; Mistral-7b-instruct* | 2 | 3 | 2 | 0; GPT-4o-mini*§ | 3 | 1 | 3 | 1

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 8 个高行为复杂度系统上的人工状态图正确性评分

<div class="result-value" markdown="1">

Qwen3-32b 的外部转移、内部转移和输出函数分数分别由 0.7471、0.6667、0.7380 提高到 0.9214、0.8849、0.9523；GPT-4o-mini 分别由 0.6423、0.7175、0.6944 提高到 0.7757、0.8555、0.7222。Claude-opus-4.1 验证后三区分数均为 1.0000，其中外部转移由 0.9047 提高到 1.0000，内部转移和输出函数原本已为 1.0000。

</div>

作者将这些结果解释为强推理模型在验证后达到最高或接近最高的一致性。分析上，Qwen3-32b 的三类函数都明显改善，是较完整的正面证据；Claude-opus-4.1 的内部转移和输出函数存在满分天花板，因此只能证明 SEV 没有破坏这两类结果，不能证明它继续提升了它们。此外，评分由专家依据系统描述人工给出，尚不能视为自动证明状态图与需求完全等价。

<div class="result-source" markdown="1">

来源：表 8，Statechart Evaluation，第 6.2 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen3-32b‡§ | 0.7471 | 0.9214 | 0.6667 | 0.8849 | 0.738 | 0.9523; Claude-opus-4.1*§ | 0.9047 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000; GPT-4o-mini*§ | 0.6423 | 0.7757 | 0.7175 | 0.8555 | 0.6944 | 0.7222

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 较小基础模型在 8 个复杂系统上的分类正确性变化

<div class="result-value" markdown="1">

Llama-3.1-8b 的内部转移与输出分数由 0.6416、0.7935 提升至 0.7736、0.8571，但外部转移由 0.9434 降至 0.8809；Ministral-3b 也呈现内部转移和输出提高、外部转移下降；Ministral-8b 的内部转移和输出保持 0.7857 和 0.8571，外部转移则由 0.8392 降至 0.8142。

</div>

这组结果揭示了纠错收益的类别差异：SEV 对内部行为和输出规格可能有效，却可能损害小模型已经生成正确的外部转移。作者将其归因于模型规模与推理深度敏感性；更谨慎的解释是，受控再生成存在修复一类事实、同时改坏另一类事实的风险，因此不能仅凭某一类别分数上升断言整体规格更正确。

<div class="result-source" markdown="1">

来源：表 8，Statechart Evaluation，第 6.2 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Llama-3.1-8b† | 0.9434 | 0.8809 | 0.6416 | 0.7736 | 0.7935 | 0.8571; Ministral-3b† | 0.8065 | 0.7755 | 0.6427 | 0.7801 | 0.8809 | 0.9047; Ministral-8b† | 0.8392 | 0.8142 | 0.7857 | 0.7857 | 0.8571 | 0.8571

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评估规模有限：模型检查仅覆盖 14 个整理后的系统描述，正确性评分进一步只覆盖其中 8 个较复杂系统；原文没有报告随机抽样、训练测试隔离、重复运行、方差或显著性检验，因此难以判断结果对更广泛 PDEVS 任务和 LLM 随机性的稳定程度。
- 两项核心评估均包含人工环节：PDEVS 状态图被手工转换为 UPPAAL 时间自动机，输出函数还被省略；正确性分数也由领域专家手工标注。原文未明确报告标注者人数、一致性或盲评协议，且 Phone 案例证明验证后仍可能遗漏关键转移，所以现有结果不能等同于端到端形式正确性保证。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 验证前状态图（BV）：直接使用 PDEVS Specification Generator 生成、尚未经过 SEV 纠错的 PDEVS 事实生成状态图。这是最关键的内部基线，因为它与验证后状态图使用相同输入和基础模型，主要差别是是否经过受控纠错循环。
- 小型模型组：Llama-3.1-8b、Ministral-3b 和 Ministral-8b，用于判断 SEV 能否弥补参数规模较小模型的规格生成缺陷。
- 大模型与推理模型组：Llama-3.3-70b、Qwen3-32b、Claude-opus-4.1 和 GPT-4o-mini，用于考察具有更强生成或推理能力的模型是否仍能从形式验证反馈中获益。
- 指令微调模型 Mistral-7b-instruct：用于检验收益是否对所有模型都稳定；它尤其重要，因为其验证后死锁失败数反而增加，构成方法并非单调改进的反例。

**实验想回答的问题**

- 引入隔离蕴含验证（SEV）及受控纠错循环后，由不同规模和类型的大语言模型生成的 PDEVS 状态图，是否更少出现死锁与阶段不可达问题？
- 验证前后，状态图的外部转移函数、内部转移函数和输出函数与自然语言系统描述的一致性是否提高；这种收益是否依赖基础模型的规模与推理能力？

**实验实现**

PDEVS Specification Generator 分别采用 8 个公开模型，生成温度固定为 0.3。行为条件识别、命题提取、PDEVS 事实与行为条件的命题逻辑翻译由 GPT-4o-mini 完成，温度同为 0.3；输出要求为 JSON，解析失败最多重试 3 次。命题逻辑可满足性与蕴含检查使用 Microsoft 的 Python z3-solver，事实和条件的纠错循环阈值均设为 $m=n=3$，最终选择总体蕴含条件最多的一轮 PDEVS 事实。状态图生成沿用 PDEVS-LLM 的 EBNF 文法，并使用 GPT-4-0125-preview、温度 0.7。模型检查阶段由研究者手工将状态图复制为 UPPAAL 时间自动机：阶段映射为位置，端口和消息映射为同步通道，时间推进映射为局部时钟约束；输出函数未复制。正确性评分同样由领域专家手工完成。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除或加入 SEV 受控纠错循环：以同一基础模型生成的 BV 状态图为对照，比较 AV 状态图 | 以 GPT-4o-mini 为例，14 个系统中的死锁失败由 3 个减少到 1 个，阶段可达性失败也由 3 个减少到 1 个；在 8 个复杂系统中，外部转移、内部转移和输出正确性分别由 0.6423、0.7175、0.6944 提高到 0.7757、0.8555、0.7222。 | 该对照直接隔离了验证驱动纠错是否有用，是全文最接近消融实验的设计。结果表明加入 SEV 后，GPT-4o-mini 在结构性质和专家评分上均改善；但流程中的辅助逻辑翻译固定使用 GPT-4o-mini，且状态图生成另用 GPT-4-0125-preview，因此不能把全部增益单独归因于基础生成模型自身能力。 | 表 6，第 6.1 节；正确性补充数值见表 8，第 6.2 节<br><span class="experiment-evidence">GPT-4o-mini*§ \| 3 \| 1 \| 3 \| 1</span> |
| 纠错循环的迭代选择机制：Phone 案例在阈值为 3 时比较三轮 PDEVS 事实，并选择蕴含行为条件最多的一轮 | 第 2 轮蕴含 9 个行为条件中的 5 个，为三轮最高，因此其 PDEVS 事实被用于生成最终状态图；修正后解决了阶段可达性问题并补充了部分缺失转移，但仍遗漏 SearchingForService 到 On 以及 Active 到 Ready 的期望内部转移。 | 这一分析检验“保留最后一轮”之外的关键设计，即按蕴含条件数量选择候选。它说明中间轮次可能优于后续轮次，也说明最大蕴含计数只是启发式目标：5/9 并不代表完整满足需求，未被蕴含的关键条件仍会转化为状态图缺陷。 | 表 4及第 5.1 节 Case Study: Phone<br><span class="experiment-evidence">For the provided system description, the PDEVS facts in the 2nd iteration entail the most conditions (5 out of 9) compared to that of the other iterations.</span> |

**定性案例**

- Phone 案例中，验证前状态图存在错误的 Dynamic 阶段、On—SearchingForService—Ready 链路缺失，以及无法从其他阶段正确转入 Off 等问题，导致 Ready、Active、SearchingForService 和 Dynamic 阶段不可达。采用第 2 轮 SEV 纠正后的事实生成状态图后，阶段可达性检查通过，多数缺失转移得到补充；不过与专家状态图相比，SearchingForService 在服务不可用时返回 On，以及 Active 在无中断来电时返回 Ready 的内部转移仍然缺失。该案例支持“显著减少后续人工修订”，而不支持“无需专家检查即可获得完整正确模型”。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The central contribution uses LLMs to generate and formally verify parallel discrete-event statecharts, emphasizing structured logical and code-like reasoning.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`62bbebdaa21e800172d2880bd0347b3dd6049b500bbca56d9f9a7fd8bdcb8b44`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
