---
title: "[论文解读] IR2Solve: Structured Intermediate Representations for Cost-Efficient Optimization Autoformulation"
description: "[arXiv 2608.02641][LLM Reasoning] 本文针对优化自动建模中“直接生成代码易错、迭代修复成本高”的矛盾，研究能否以一次大语言模型语义调用生成结构化中间表示，再通过确定性验证与编译兼顾目标正确性、成本可控性和可审计性。"
arxiv_id: "2608.02641"
announcement_date: "2026-08-05"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:42:45.289880+00:00"
source_sha256: "449db7aa1907e494be41be04ca7ecc3d0bf7d27b6c95336652eead39809641a2"
tags:
  - "LLM Reasoning"
  - "LLM 效率"
  - "LLM 其他"
  - "优化自动建模"
  - "大语言模型"
  - "结构化中间表示"
  - "ModelIR"
  - "确定性验证"
  - "IR到求解器编译"
  - "标量约束"
  - "推理成本"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.02641</p>

# IR2Solve: Structured Intermediate Representations for Cost-Efficient Optimization Autoformulation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Penglin Zhu, Linhai Zhang, Jungang Xu, Xinchi Wei, Xiuqi Wu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> School of Computer Science and Technology, University of the Chinese Academy of Sciences</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.02641v1) · [PDF 下载](https://arxiv.org/pdf/2608.02641v1) · **关键词** 优化自动建模, 大语言模型, 结构化中间表示, ModelIR, 确定性验证, IR到求解器编译, 标量约束, 推理成本<br>


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

本文针对优化自动建模中“直接生成代码易错、迭代修复成本高”的矛盾，研究能否以一次大语言模型语义调用生成结构化中间表示，再通过确定性验证与编译兼顾目标正确性、成本可控性和可审计性。

**不用术语来说**：现实中的优化任务通常先要把文字需求准确写成变量、目标和约束，再交给求解器计算；后一步已经高度自动化，前一步却仍依赖专业人员。大语言模型虽然能代写模型代码，但可能写错索引、目标或约束，甚至生成无法运行的程序；反复让模型检查和修改又会显著增加调用次数、令牌消耗与流程复杂度。本文要解决的是：如何减少模型自由生成代码带来的错误，同时避免依赖昂贵且次数不确定的迭代修复。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出结构化的 ModelIR 表示层，将开放式求解器代码生成改为填写受模式约束的集合、参数、变量、目标与约束；其中，有限的逐索引约束族被展开为具体标量约束，以减少自由索引和隐式量化歧义。
- 作者构建 IR2Solve 单次语义调用流程：大语言模型只负责从自然语言到 ModelIR 的语义建模，后续由确定性验证器进行保守改写，并由确定性编译器生成 Gurobi 模型，从而避免迭代生成或基于大语言模型的补救。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于运筹优化自动建模（optimization autoformulation）研究。传统优化流程先把现实问题抽象为决策变量、目标函数和约束，再交给 Gurobi 等求解器；其中求解阶段已高度自动化，而从自然语言描述到形式化模型的转换仍依赖专业人员。大语言模型能够理解问题语义，但直接生成完整求解器代码时必须同时处理数学建模、索引范围、程序语法和求解器接口，容易产生无法编译、不可行或目标含义错误的模型。本文关注的核心设置是：在只进行一次语义模型调用、且不使用迭代式大模型修复的条件下，能否借助结构化中间表示和确定性处理，以较低推理成本生成可靠的求解器模型。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**优化模型**

优化模型用决策变量表示待选择的方案，用目标函数衡量方案优劣，并用约束刻画必须满足的条件。求解器在变量定义域和约束允许的范围内，寻找使目标最小化或最大化的解。

</div>
<div class="concept-item" markdown="1">

**自动建模**

自动建模是把非结构化的自然语言问题转换为可由优化求解器执行的形式化模型。它不仅要生成可运行代码，还必须正确识别集合、参数、变量、目标、约束及其索引关系。

</div>
<div class="concept-item" markdown="1">

**中间表示**

中间表示（IR）是自然语言与求解器代码之间的结构化模型描述，不直接绑定完整程序。本文的 ModelIR 通过固定模式显式记录集合、参数、变量、目标和约束，并将数学表达式限制为 Python 风格字符串，从而缩小大模型的自由输出空间。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一段描述优化任务的自然语言文本，其中包含已知数据、可选决策、业务规则以及需要最大化或最小化的目标；输出是可交给 Gurobi 构造并求解的优化模型。IR2Solve假设问题可用有限的集合、参数、变量、目标函数和约束表达，并采用一次大语言模型语义调用先生成满足模式约束的 ModelIR；随后由确定性验证器执行固定且保守的改写，再由确定性编译器将该表示转换为求解器模型。对于按索引重复出现的有限约束族，系统要求把每个具体索引对应的约束写成独立标量条目，以避免自由索引和隐式量化带来的歧义；这一约定也意味着约束数量很大时，中间表示可能变长、扩展性受限。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{I}$**

本文所采用的结构化中间表示 ModelIR；原文节选未给出正式符号，此处不将其视为论文原定义。

</div>
<div class="notation-item" markdown="1">

**$x$**

优化模型中的决策变量；具体变量名称、维度和定义域由输入问题决定。

</div>
<div class="notation-item" markdown="1">

**$f(x)$**

需要最小化或最大化的目标函数，用于衡量决策方案的质量。

</div>
<div class="notation-item" markdown="1">

**$g_i(x)$**

第 $i$ 个约束所对应的表达式；IR2Solve倾向于将有限索引下的每个实例显式写成标量约束。

</div>

</div>

**直接相关的工作**

- **CAFA**: CAFA代表低成本的代码优先路线：一次生成完整求解器代码，再进行确定性清理。它把数学表达、导入语句、求解器 API、索引和运行控制耦合在同一次生成中；IR2Solve则先生成显式 ModelIR，再进行确定性验证与编译，以隔离语义建模和程序构造。
- **Chain-of-Experts**: Chain-of-Experts通过角色专门化的多个智能体、协调器和反思机制分解并修订建模过程，代表以额外推理调用换取纠错机会的路线。IR2Solve研究与之不同的准确率—成本取舍：仅进行一次语义调用，之后不再请求大模型，而依靠结构约束和确定性后处理提高可靠性。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

优化模型广泛用于医疗、交通和科学发现等决策场景，但将非结构化需求抽象成可执行模型仍是应用运筹学的主要瓶颈。自动建模需要同时保证变量、目标、约束及其索引关系在数学上正确，并输出求解器能够执行的模型；任何模式、索引或语义错误都可能造成编译失败、模型不可行，或得到看似可运行但目标错误的结果。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **端到端直接代码生成**：让大语言模型直接把自然语言问题转换为完整的求解器程序，将问题理解、数学建模、索引展开和程序构造集中在一次自由文本生成中。
- **分解、反思与迭代修复流程**：通过提示分解、多智能体协作、搜索、反思或多轮纠错来检查并修补初始模型，以更多推理步骤换取更高的生成成功率。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 直接生成完整程序的输出空间过于开放，大语言模型的幻觉、格式不一致和数学不准确会与求解器要求的严格模式及逻辑一致性冲突；其后果不仅是程序无法编译，还可能是索引作用域错误、不可行模型或错误目标等更隐蔽的语义失败。
- 多智能体、搜索和迭代纠错虽可改善准确率，却增加 API 调用、令牌消耗和工作流复杂度；修复轮数还可能不确定，使大规模部署的成本和运行行为难以预测。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作尚缺少一种处于两类方案之间的可部署机制：它既不能让大语言模型无约束地承担完整程序构造，也不应依靠开放式、多轮的大语言模型修复，而应保留模型对自然语言语义的理解能力，并把可机械化的模式检查、索引处理和求解器构造交给可复现的确定性过程。该机制还需要提供一个可供人工检查的中间产物，以便区分语义建模错误与程序构造错误。

</div>
<div markdown="1"><span>核心问题</span>

在面向有限 LP/MILP 类问题的优化自动建模中，能否通过一次大语言模型语义调用生成受模式约束的中间表示，并以确定性验证和编译完成求解器模型，从而在不使用迭代生成或大语言模型补救的前提下，取得有竞争力的目标正确性以及更可控的推理成本？

</div>
<div markdown="1"><span>作者直觉</span>

自然语言理解需要大语言模型的语义能力，但把声明转换为求解器 API、检查字段结构和展开有限索引关系具有较强的规则性。因而可以让模型只填写一张结构明确的“数学模型清单”，再由固定程序检查和施工。将逐索引约束写成独立标量条目，相当于要求模型明确列出每条约束作用于谁，减少悬空索引和默认量化造成的歧义；确定性后端则能对同一 ModelIR 重复生成相同模型。不过，这一设计以输出长度换取明确性，大规模索引笛卡尔积可能导致标量展开迅速增长，因此其动机是寻求实用的准确率—成本折中，而非宣称覆盖所有优化形式。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

IR2Solve将自然语言优化问题的自动建模拆成“语义建模”和“求解器实现”两段：给定问题描述$d$，大语言模型仅调用一次，生成满足固定模式的中间表示ModelIR；随后由确定性验证器得到修正后的$\widehat{m}$，再由确定性编译器构造Gurobi模型$c$并求解。随机性只存在于$d\to m$的语义解释阶段，$m\to c$不再依赖大语言模型，因此避免把变量设计、索引解释、求解器API和控制代码同时塞进一次自由代码生成中。
ModelIR是受模式约束的JSON，显式列出有限集合、参数、决策变量、目标和约束；表达式只允许算术、已声明对象的显式索引以及有界的$\operatorname{sum}$或$\operatorname{quicksum}$。尤其是，每条约束必须是已经展开索引的具体标量关系，不允许自由索引或隐含“对所有索引成立”。通俗地说，系统让模型填写一张结构固定的数学建模表格，之后由普通程序查错并翻译成求解器代码，而不是让模型从头编写一整套容易出错的程序。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自然语言到ModelIR

通过一次语义大语言模型调用执行$\operatorname{GenerateIR}(d)$，识别集合、参数、变量及其定义域、目标方向与表达式、约束关系，并输出符合固定JSON模式的ModelIR $m$。生成提示要求只输出JSON、统一使用已声明名称，并把表达式限制在允许的Python风格数学片段内。

<div class="method-step__io" markdown="1">

**输入**：自然语言优化问题描述$d$。<br>
**输出**：未经验证的结构化模型$m$。

</div>

**直观理解**：这一阶段完成真正需要理解题意的工作，但模型只负责填写数学模型，不负责处理Gurobi初始化、API调用或结果输出等程序细节。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 标量约束展开与结构表达

将每个有限索引组合对应的约束写成独立的标量条目，条目包含名称、左侧表达式、关系符和右侧表达式；禁止自由索引与隐式全称量化。变量条目同时显式记录索引集合、连续/整数/二元类型及上下界。

<div class="method-step__io" markdown="1">

**输入**：模型识别出的有限索引集合及按索引定义的约束族。<br>
**输出**：可逐条检查、索引作用域明确的ModelIR约束与变量声明。

</div>

**直观理解**：例如“对每个工厂都满足产能限制”不保留为一句带隐含循环的话，而是展开成每个工厂各自的一条约束。这样会增加输出长度，却能减少编译器猜测索引含义时产生的错误。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 确定性验证

验证器按固定顺序应用带触发条件的变换$T_1,\ldots,T_K$：规范化名称、索引键和常见参数形状，修复可恢复的索引作用域或聚合不一致，并执行少量无歧义的变量定义域及约束方向检查。若某条规则的触发条件不满足，该规则保持输入不变，不进行候选重采样或语义推断。

<div class="method-step__io" markdown="1">

**输入**：生成阶段得到的ModelIR $m$。<br>
**输出**：验证后的ModelIR $\widehat{m}=\mathcal{V}(m)$。

</div>

**直观理解**：这类似一组严格限定的格式检查和安全修补规则：只改程序能够确定如何改的地方，不能凭空补回大语言模型漏掉的问题语义。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 确定性编译与求解

编译器实例化声明的集合、参数和变量，在仅包含已声明对象及允许聚合函数的受限环境中计算表达式，设置目标并逐条添加约束，得到Gurobi模型$c$，随后调用求解器返回状态和目标值。同一$\widehat{m}$与同一编译器版本会产生固定的$c$。

<div class="method-step__io" markdown="1">

**输入**：验证后的ModelIR $\widehat{m}$。<br>
**输出**：求解状态以及可获得时的目标值。

</div>

**直观理解**：这一阶段相当于可靠的模板翻译器：它忠实地把结构化数学模型转成求解器对象，但不会判断上游是否误解了题意。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 自动建模的两阶段概率分解

$$
p_{\phi,\psi}(m,c\mid d)=p_{\psi}(c\mid m)\,p_{\phi}(m\mid d)
$$

**符号说明**

- $d$：自然语言问题描述。
- $m$：对问题的数学规划表述；在IR2Solve中由ModelIR承载。
- $c$：可执行的求解器实例。
- $p_{\phi}(m\mid d)$：参数为phi的语义模型根据问题描述生成数学表述的条件分布。
- $p_{\psi}(c\mid m)$：参数或实现为psi的模型到求解器转换过程。
- $p_{\phi,\psi}(m,c\mid d)$：给定描述时联合得到数学表述和可执行实例的条件分布。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把“理解题目并建立数学模型”与“把数学模型实现为求解器对象”分开。IR2Solve只让前一项具有大语言模型的随机性，而用固定编译程序实现后一项，从而去除IR到代码阶段的采样误差；这并不消除大语言模型误解题意的风险。<br>
**原文位置**：第3.2节，公式(3)

</div>

</div>

<div class="equation-block" markdown="1">

#### 确定性验证器的顺序组合

$$
\widehat{m}=\mathcal{V}(m)=T_{K}\circ T_{K-1}\circ\cdots\circ T_{1}(m)
$$

**符号说明**

- $m$：大语言模型生成的原始ModelIR。
- $\widehat{m}$：经过确定性验证与保守修正后的ModelIR。
- $\mathcal{V}$：完整的确定性验证过程。
- $T_k$：第k个固定且带触发条件的规范化、检查或修正规则。
- $K$：验证器中按既定顺序执行的规则总数。
- $\circ$：函数复合，表示前一规则的输出成为后一规则的输入。

<div class="equation-explanation" markdown="1">

**直观理解**：验证不是搜索多个候选模型，而是依次运行一组固定规则；某条规则不满足触发条件时就不改输入。因此，同一原始IR在相同版本验证器下会得到相同结果，也不会产生额外的大语言模型调用。<br>
**原文位置**：第4.3节，公式(4)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。原文没有提出或报告对大语言模型、验证器或编译器进行专门训练的目标函数；IR2Solve使用现有大语言模型进行一次推理式语义生成，后续模块是人工规定的确定性程序。这里的“objective”指ModelIR中待求解优化问题自身的最小化或最大化目标$f(x;\theta)$，而不是机器学习训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. ModelIR结构化表示层**

ModelIR包含$\texttt{sets}$、$\texttt{params}$、$\texttt{vars}$、$\texttt{objective}$和$\texttt{constraints}$五类有类型字段。集合使用显式有限元素，参数记录索引签名与数值，变量记录索引、类型和边界；目标与约束仅使用受限表达式字符串，不允许导入、控制流、模型初始化、求解器调用或结果处理代码。

> 直观理解：它缩小了大语言模型可以输出的结构空间，使名称、形状和索引问题能在执行前暴露；代价是当前表达能力主要面向基准中的有限LP/MILP模型，并不宣称覆盖所有优化形式。

**2. 确定性验证器**

验证器是固定、顺序敏感且带守卫条件的规则组合，不建立概率分布，也不优化隐式违规分数。规则仅处理可机械判定的名称、形状、索引、聚合、变量定义域和约束方向问题，因此保持验证过程可复现。

> 直观理解：该模块的价值是低成本消除常见机械错误，而不是再次调用模型“猜一个修复方案”；若目标、约束或变量在语义上被遗漏，它通常无法恢复。

**3. 受限表达式编译器**

编译器仅在白名单环境中解析ModelIR表达式，环境包含已声明的集合、参数、变量和允许的聚合器，然后直接构造Gurobi目标与标量约束。每条求解器约束可追溯到对应IR条目，且编译阶段不增加语义模型调用。

> 直观理解：受限环境既减少任意代码带来的执行风险，也避免第二个大语言模型在IR到代码的转换中再次引入随机错误；不过确定性只保证忠实编译，不保证原始建模语义正确。

**训练与推理**

训练阶段：原文未描述针对IR2Solve的参数训练、微调或强化学习流程。推理阶段：输入描述$d$后，大语言模型进行一次语义调用并输出ModelIR；系统不进行候选重采样、反思、评论器评审、搜索或语义修复调用。随后验证器按$T_1$到$T_K$的固定顺序处理IR，编译器将结果转换为Gurobi模型并调用求解器，最终返回构建/求解状态及目标值。因而完整流程可概括为$ir\leftarrow\operatorname{GenerateIR}(d)$、$ir\leftarrow\operatorname{Verify}(ir)$、$c\leftarrow\operatorname{CompileToGurobi}(ir)$、$\operatorname{Solve}(c)$。

**复现信息**

为正确复现方法，需要固定ModelIR的JSON模式、允许的表达式语法、标量约束约定、验证规则及其执行顺序，以及编译器版本。编译器的表达式求值环境只能暴露已声明对象和允许的$\operatorname{sum}$或$\operatorname{quicksum}$等聚合器，并应保持IR约束到Gurobi约束的逐条对应。方法面向具有显式有限集合的LP/MILP基准；把大型索引族完全展开会增加输出长度，因此不能在未验证规模适应性的情况下直接推断其适用于任意大规模或更广泛的优化形式。原文节选未给出具体大语言模型解码参数、Gurobi版本、求解时间限制或完整验证规则，复现时需查阅附录与代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- NL4Opt（214 个实例）与 NLP4LP（178 个实例）：均测试从自然语言描述恢复线性规划或混合整数线性规划。前者是常用自然语言优化基准，后者来自 OptiMUS 系列；二者用于检验方法在一般自然语言建模任务上的目标正确性。
- MAMO 系列包括 EasyLP（545 个实例）和 ComplexLP（111 个实例），另有 IndustryOR（42 个工业风格实例）。EasyLP 与 ComplexLP分别代表较容易和较复杂的建模问题；完整的 IndustryOR 与 ComplexLP 共 153 个实例被用于嵌套消融，因为其中索引、参数形状和语义错误较频繁。
- ReSocratic（403 个实例）：来自 OptiBench/ReSocratic 系列，用于补充考察系统面对另一类自然语言优化描述时的泛化表现。NL4Opt、EasyLP、NLP4LP 和 ReSocratic 合计构成 1,340 个实例的最终本地评测；六个主基准均采用调查工作清洗后的版本。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Objective correct**

求解所得目标值是否在第 3 节规定的容差内与参考目标一致。它比“代码能运行”更接近最终建模是否正确，但仍主要检查目标值，不能保证模型的全部语义结构都与参考模型等价。 （越高越好，因为更高比例表示更多自然语言问题被转化为得到正确目标值的优化模型。）

</div>
<div class="metric-item" markdown="1">

**Build**

生成的模型能否成功构建或编译为 Gurobi 模型，用于测量模式、名称、表达式和索引等执行层错误是否被消除。 （越高越好；但成功构建只表示模型可执行，不表示目标、约束或变量语义正确。）

</div>
<div class="metric-item" markdown="1">

**Solved**

构建后的模型能否在每实例 60 秒限制内由求解器完成求解，用于区分编译成功与实际可求解。若该指标高于 Objective correct，说明仍存在能够运行但数学语义错误的模型。 （越高越好，但必须与 Objective correct 联合解读，避免把可求解误当成建模正确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 六个调查清洗基准上的目标正确率比较。

<div class="result-value" markdown="1">

IR2Solve 在 NL4Opt、IndustryOR、EasyLP、ComplexLP、NLP4LP 和 ReSocratic 上分别达到 86.4%、64.3%、97.4%、70.3%、90.4% 和 86.6%。它在六列中均高于调查表内的 ORLM、Standard、CoT、Chain-of-Experts 和 CAFA；与更近期的 SAC-Opt 相比，IR2Solve 在 IndustryOR 和 EasyLP 更高，而 SAC-Opt 在其余四个数据集更高。

</div>

作者的结论是，一次语义调用的 IR-first 系统无需迭代语义修复，也能获得与近期强系统竞争的目标正确率。分析上，这表明结构化输出和确定性后处理可以替代一部分搜索或修复开销；但各行使用的工作流、运行聚合方式和部分求解参数不同，因此不能据此宣称 IR2Solve 全面优于 SAC-Opt，也不能把差异完全归因于中间表示。

<div class="result-source" markdown="1">

来源：表 2，Cleaned Benchmark Comparison

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

IR2Solve ‡ 86.4% 64.3% 97.4% 70.3% 90.4% 86.6%

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 匹配的 10 实例推理成本面板。

<div class="result-value" markdown="1">

IR2Solve 每实例使用 1 次语义调用；Chain-of-Experts 和 SAC-Opt 分别使用 8 次和 39 次调用，其 token 总量分别是 IR2Solve 的 3.3 倍和 22.9 倍。

</div>

该结果直接检验系统定位中的成本优势：IR2Solve 把 LLM 限制在一次语义解析，后续检查与编译由确定性程序完成，因而避免代理讨论、候选搜索和反复修复造成的调用膨胀。不过面板只有 10 个实例，且所给节选未展示对应样本选择、货币成本或延迟明细，所以这些倍数不应外推为所有数据集和部署环境中的固定比例。

<div class="result-source" markdown="1">

来源：摘要；第 5.4 节标题为 Inference Cost and Accuracy–Cost Analysis，但所给正文节选未包含其完整表格

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On a matched ten-instance cost panel, IR2Solve uses one semantic call per instance, whereas Chain-of-Experts and SAC-Opt use 8 and 39 calls per instance and consume 3.3 and 22.9 times the token volume of IR2Solve, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 153 个 IndustryOR 与 ComplexLP 实例上的可执行性诊断。

<div class="result-value" markdown="1">

汇总编译失败数从直接代码条件 $R0$ 的 96 个，依次降至 $R1$ 的 84 个、$R2$ 的 42 个和最终 $R3$ 的 30 个；同时所有变体的 Build 与 Solved 都高于 Objective correct。

</div>

结构化表示、约束粒度指令和验证器确实减少了无法编译的模型，但“能构建、能求解”仍不等于“数学模型正确”。因此系统剩余瓶颈不只是 JSON、变量名或索引错误，还包括目标方向、系数、变量类型或约束含义等语义偏差。由于这些数字来自嵌套变体，不能把总下降量归因于某一个独立组件。

<div class="result-source" markdown="1">

来源：第 5.3 节，Executability diagnostics

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Pooled compilation failures fall from 96 in R0 to 84, 42, and 30 in R1–R3.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主表不是完全受控的同协议比较：调查基线、SAC-Opt/OptiMUS 的五次运行均值与 IR2Solve 本地单次配置在工作流细节和聚合方式上不同；MCTS-based Autoformulation 与 NEMO 也因数据版本或评测范围不对齐而未进入表 2。因此结果支持有限范围内的竞争力结论，不支持跨系统的严格优越性排序。
- 消融的识别边界有限：$R0\rightarrow R1$ 同时替换 schema、表达式语言、提示契约和构建路径，未单独隔离各因素，也未比较确定性编译器与 LLM 编译器；此外，显式展开逐索引约束在大型笛卡尔积上会增加生成长度，10 实例成本面板也不足以刻画这种扩展性代价。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- ORLM-LLaMA-3 8B：经过优化建模数据微调的模型，可用于判断一次调用的 IR2Solve 是否能接近专门训练模型。
- CAFA：轻量级、代码优先的自动建模方法，是与 IR2Solve 的“先生成中间表示、再确定性编译”路线最直接的外部对照。
- Chain-of-Experts：多代理协作工作流，用于比较结构化单次生成与多专家、多次调用方案之间的准确率—成本取舍。
- OptiMUS-0.3 与 SAC-Opt：前者采用模块化反思流程，后者采用迭代语义纠错；二者代表较强的近期系统。不过其结果是 SAC-Opt 统一评测中的五次运行均值，与 IR2Solve 的本地单次配置并非完全受控的同协议比较。

**实验想回答的问题**

- 在六个清洗后的自然语言优化建模基准上，仅进行一次语义生成、随后采用确定性验证与编译的 IR2Solve，能否在目标函数正确性上达到近期代码生成、微调模型及迭代式代理系统的竞争水平？
- 结构化 ModelIR、逐条标量约束指令和确定性验证分别带来什么顺序增益；这些增益能否同时改善模型可构建性、可求解性与推理成本，而不只是减少语法错误？

**实验实现**

最终配置使用 GPT-4o-2024-08-06、温度为 $0$，每个实例只执行一次自然语言到 ModelIR 的语义调用；之后使用确定性验证器和 IR-to-Gurobi 编译器，并给 Gurobi 每实例 60 秒。系统不进行语义重试、候选选择或 LLM 修复，参考目标仅用于事后评测。主表混合了调查论文报告值、SAC-Opt 统一管线的五次运行均值和作者本地结果，因此适合做限定范围内的竞争力比较，不是统一骨干模型与解码协议下的严格正面对照。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| $R0\rightarrow R1$：从一次调用直接生成 Gurobi 代码，改为生成结构化表达式字符串 ModelIR，并通过确定性编译器构建模型。 | 汇总 Objective correct 从 7.2% 提升到 35.9%，增加 28.8 个百分点；IndustryOR 从 7.1% 提升到 50.0%，ComplexLP 从 7.2% 提升到 30.6%。这是所有顺序阶段中最大的汇总正确率增幅。 | 这一对照测试的是完整“结构化 IR 接口包”，其中同时改变了输出模式、表达式表示、提示契约和确定性模型构建路径。通俗地说，先让模型填写受限的数学模型表格，再由程序写求解器代码，比让模型直接写完整代码更稳健。但该实验没有分别隔离 schema、表达式字符串、提示词和编译器，因此不能声称其中任一单项独立贡献了 28.8 个百分点；而且 $R0$ 提示并非专门优化的最强代码生成提示。 | 表 3及第 5.3 节 Results<br><span class="experiment-evidence">The structured IR interface gives the largest observed sequential increase (+28.8 points pooled; +33.2 macro).</span> |
| $R1\rightarrow R2\rightarrow R3$：先加入“每个约束必须是单个标量、逐索引展开且禁止自由索引”的指令，再对完全相同的 $R2$ ModelIR 施加确定性验证器。 | 加入标量约束指令后，汇总 Objective correct 从 35.9% 升至 57.5%，增加 21.6 个百分点，结构违规由 522 降至 39；验证器不增加模型调用，又把汇总正确率升至 68.6%，增加 11.1 个百分点，并将结构违规进一步降至 12。验证器对 IndustryOR 没有正确率增益，仍为 64.3%，但使 ComplexLP 从 55.0% 升至 70.3%。 | 前一阶段较窄地检验约束粒度指令：要求把“对所有 $i$”显式展开，可以显著避免未绑定索引和向量式约束。后一阶段检验确定性验证本身，因为 $R3$ 复用完全相同的 $R2$ 输出而不再调用 LLM；其收益主要出现在更复杂的 ComplexLP，说明规则化修正具有数据集依赖性。两段变化是顺序效应，不是相互独立的因果贡献；相应配对检验为 $p=1.1\times10^{-6}$ 与 $p=1.5\times10^{-5}$。 | 表 3及第 5.3 节 Results<br><span class="experiment-evidence">The concrete scalar-constraint instruction adds +21.6 pooled points (+19.3 macro) and reduces free-index/non-scalar violations from 522 to 39. The verifier adds +11.1 pooled points (+7.7 macro), with a dataset-dependent effect: IndustryOR remains 64.3%, whereas ComplexLP increases from 55.0% to 70.3%.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出结构化中间表示与确定性编译流程，以更少模型调用完成优化问题的正确形式化。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`449db7aa1907e494be41be04ca7ecc3d0bf7d27b6c95336652eead39809641a2`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
