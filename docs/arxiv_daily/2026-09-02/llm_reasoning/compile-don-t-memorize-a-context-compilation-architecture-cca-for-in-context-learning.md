---
title: "[论文解读] Compile, Don't Memorize: A Context Compilation Architecture (CCA) for In-Context Learning"
description: "[arXiv 2609.00759][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2609.00759"
announcement_date: "2026-09-02"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:47:46.810736+00:00"
source_sha256: "f2af564ce6924f40180ef31faf07ed79ba9379e45e9ffb1249e11cd7a5b6cc64"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "上下文学习"
  - "长上下文"
  - "上下文编译"
  - "类型化中间表示"
  - "可执行核验器"
  - "评分规约"
  - "脚手架工程"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.00759</p>

# Compile, Don't Memorize: A Context Compilation Architecture (CCA) for In-Context Learning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Jinhu Qi, Minda Hu, Wentao Zhang, Weiqiang Jin, Yanyu Chen, Junli Wang, Irwin King</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: The Chinese University of Hong Kong；Affiliation: Macao Polytechnic University；Affiliation: Xi’an Jiaotong University；Affiliation: University of Science and Technology of China {jhqi25, mdhu22, yychen25</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00759v1) · [PDF 下载](https://arxiv.org/pdf/2609.00759v1) · **关键词** 上下文学习, 长上下文, 上下文编译, 类型化中间表示, 可执行核验器, 评分规约, 脚手架工程<br>
**代码**: [https://github.com/TonyQJH/cca-emnlp2026](https://github.com/TonyQJH/cca-emnlp2026)

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

本文研究长上下文条件下的上下文学习（ICL）：模型不通过参数更新，而是依据当前会话中新提供的领域文档、业务规则、自定义语言或工作流来回答一系列问题。其目标并非只找到某条相关信息，而是同时遵守上下文规定的全部内容与输出格式；在 CL-bench 这类按细粒度评分规约评测的任务中，每个问题包含 5—20 项判据，遗漏任一约束即可导致整题失败。论文将可靠性问题定位到“读取并推理”范式：单次前向生成同时承担规则提取、答案规划、文本生成和自我核验，随着上下文变长、约束增多，模型更容易漏掉细节。CCA 因而把 ICL 重新表述为上下文编译问题：先将自然语言上下文转换为固定槽位的类型化中间表示，再生成可执行核验器，以外部流程约束一个参数冻结的语言模型；这属于通过模型外围执行与验证机制提高可靠性的“脚手架工程”（harness engineering）。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**上下文学习（In-Context Learning, ICL）**

模型不重新训练，而是直接从提示中给出的新规则、知识和示例理解任务，并据此回答后续问题。本文关注的是规则密集且上下文很长的 ICL，而非少量示例下的简单模式模仿。

</div>
<div class="concept-item" markdown="1">

**评分规约（rubric）**

评分规约是针对一个答案列出的多项必要判据，例如必须包含的事实、禁止行为、条件规则和格式要求。本文所用评测采取严格的全满足标准：只要漏掉一项判据，整项任务就不能算通过。

</div>
<div class="concept-item" markdown="1">

**类型化中间表示（typed intermediate representation, IR）**

中间表示是位于原始上下文与最终作答之间的结构化数据；“类型化”表示不同信息必须进入预定义类别，如必做规则、禁止规则、条件规则和输出规范。通俗地说，它把散落在长篇文字中的要求整理成可逐项检查的清单，而不是要求模型临时凭记忆回看全文。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一份可能长达数万至数十万字符、对模型而言全新的自然语言上下文，以及共享该上下文的一系列下游问题；上下文可定义领域知识、精确术语、可用工具、条件规则和输出模式。对每个问题，系统应生成自然语言答案，并满足该题全部评分判据；论文假设基础语言模型保持冻结，因此改进来自外围处理流程而非参数训练。本文特别考察“规则密集、全约束满足”的设置：相关信息可能分散在上下文不同位置，答案不仅要语义正确，还要完整遵守必须执行、不得执行及条件触发的要求。CCA 将每份上下文编译一次并供多个问题复用，其编译结果包含固定槽位 `rules.must_do`、`rules.must_not`、`rules.conditional`、`output_spec`、`available_tools` 和 `data_profile`；后续答案由按上下文生成的可执行核验器检查，只有发现违规时才进入定向修正。原文节选未给出该任务的正式概率模型或统一数学目标函数，因此不额外构造符号化定义。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$C$**

概念性记号：给定的长篇自然语言上下文；原文节选未正式指定该符号。

</div>
<div class="notation-item" markdown="1">

**$q$**

概念性记号：在上下文下提出的一个下游问题；原文节选未正式指定该符号。

</div>
<div class="notation-item" markdown="1">

**$I$**

概念性记号：由上下文编译得到的类型化中间表示；原文节选称其为 compiled IR，但未规定数学符号。

</div>
<div class="notation-item" markdown="1">

**$V_C$**

概念性记号：针对上下文生成并复用的可执行核验器集合；原文节选未正式指定该符号。

</div>

</div>

**直接相关的工作**

- **ReadAgent-P（Lee et al., 2024）**: 该方法把长上下文分页，为每页保存摘要式 gist，并在回答问题时检索和重新读取相关页面，适合证据集中于局部页面的长文档问答。本文指出，摘要过程可能省略严格评分所需的原文事实或精确措辞；CCA 则将每份上下文一次性编译为保留具体约束的类型化 IR，并用核验器逐项检查，因此二者分别代表“摘要检索”和“显式约束编译”两种路线。
- **Ctx2Skill（Si et al., 2026）**: 该方法通过 Challenger、Reasoner、Judge、Proposer 和 Generator 的多角色自博弈生成自然语言技能库，并在推理时检索技能。其技能主要表达一般性解题程序，而不一定记录当前上下文中每项必须满足的判据；CCA 的区别是编译单位为当前给定上下文，产物是固定类型槽位和按上下文生成的 Python 核验器，更直接对应全规约满足式评测。

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

CCA 将长上下文条件下的问答拆成“按上下文编译一次、按任务推理多次”的两阶段流程。给定原始上下文 $c$ 及共享该上下文的一组问题，系统先用 Compiler 把散落在自然语言中的角色、规则、精确字符串、工作流、输出格式、工具和数据特征编译成类型化 JSON 中间表示 $I_c$；随后 CodeGen 根据 $I_c$ 有选择地生成规则检查器、格式验证器和数据分析器。数据分析器在上下文阶段预先运行并缓存结果，而前两类验证器留到回答草稿生成后执行。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤1：上下文编译

Compiler $\mathcal{C}$ 读取全文并输出固定模式的 JSON 中间表示 $I_c$，包括角色、规则、知识、工作流、输出规范、可用工具、数据概况和编译元数据。它要求逐字保留虚构或反事实设定，把 must、should、always、never 等约束归入必须做、禁止做或条件规则，并为规则标注是否可由程序机械检查。

<div class="method-step__io" markdown="1">

**输入**：原始上下文 $c$，即拼接后的系统消息与用户上下文，以及各阶段共享的指令提示集合 $\mathcal{I}$。<br>
**输出**：类型化中间表示 $I_c$，其中尤其保存评分可能要求逐字出现的精确术语、规则来源文本、输出格式和推荐推理策略。

</div>

**直观理解**：这一步像把一份冗长说明书整理成结构固定的检查清单，而不是让回答模型每次都重新从全文寻找要求。即使上下文故意改写常识，编译器也只记录文档所说的内容，不用模型训练知识去“纠正”它。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤2：验证器生成与数据预执行

CodeGen dispatcher 检查可编码规则数量、$\texttt{data\_profile.format}$ 和格式规则数量，按条件生成最多三个 Python 模块：$\mathtt{RC}$、$\mathtt{FV}$ 与 $\mathtt{DA}$。若存在至少一条可编码规则则生成规则检查器；若格式规则不少于三条则生成格式验证器；若数据是 TSV、CSV 或行内表格则生成数据分析器，并在上下文阶段运行 $\mathtt{DA}$ 得到缓存摘要 $s_c$。

<div class="method-step__io" markdown="1">

**输入**：编译后的 $I_c$，以及上下文中的原始数据块。<br>
**输出**：可复用模块集合 $\mathcal{M}_c\subseteq\{\mathtt{RC},\mathtt{FV},\mathtt{DA}\}$，以及可能为空的数据分析结果 $s_c$。

</div>

**直观理解**：系统不是给所有上下文强行安装同一套工具，而是根据清单内容决定需要哪些检查程序。表格统计可提前算一次并供所有问题复用，避免每个问题都重新读取和汇总相同数据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤3：基于清单生成回答草稿

Reasoner-1 $\mathcal{R}_1$ 依次接收系统指令、由 $I_c$ 渲染的检查清单、可选代码执行结果、原始上下文和问题，并生成草稿 $d_t$。只有推荐策略为数据分析或计算器且 $\mathtt{DA}$ 成功执行时才注入 $s_c$；原始上下文超出窗口时采用约 $70\%$ 头部与约 $30\%$ 尾部的保留策略。

<div class="method-step__io" markdown="1">

**输入**：中间表示 $I_c$、经策略门控的数据摘要 $s_c$、截断后的上下文 $\tau(c)$ 与当前问题 $q_t$。<br>
**输出**：针对任务 $t$ 的初始回答 $d_t$。

</div>

**直观理解**：回答模型既看到原文，也看到从原文整理出的重点清单，因此不必一边作答一边重新发现所有约束。原文仍被保留是为了提供细节和语义依据，而清单负责提醒模型哪些内容不能漏。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤4：违规检测与条件修正

系统对 $d_t$ 运行规则检查器和格式验证器，将各模块报告合并为违规列表 $v_t$；当 $|v_t|\geq\theta$ 时，Reasoner-2 根据草稿和违规反馈进行最小局部修改。反馈最多保留前十项且每项截至 200 个字符；若修正调用返回空文本，或者违规数未达到阈值，系统直接保留原草稿。

<div class="method-step__io" markdown="1">

**输入**：草稿 $d_t$、草稿期验证器集合 $\mathcal{V}_c=\mathcal{M}_c\cap\{\mathtt{RC},\mathtt{FV}\}$，以及阈值 $\theta=2$。<br>
**输出**：最终回答 $y_t$，即非空的修正版或原始草稿。

</div>

**直观理解**：它类似提交前运行自动检查：只有至少两项检查共同表明存在问题时才要求返修，以降低单个误报破坏正确答案的风险。返修不是从头重写，而是围绕已定位的违规做局部改动。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### CCA 两阶段联合概率分解

$$
P\!\left(\{y_t\}_{t\in\mathcal{T}_c}\mid c,\mathcal{I}\right)=\underbrace{P(I_c\mid c,\mathcal{I})\,P(\mathcal{M}_c\mid I_c)\,P(s_c\mid\mathcal{M}_c,c)}_{\textit{Per-context}\;(\mathrm{F1,F3,F5})}\;\underbrace{\prod_{t\in\mathcal{T}_c}P(d_t\mid I_c,s_c,\tau(c),q_t)\,P(y_t\mid d_t,\mathcal{V}_c,\theta)}_{\textit{Per-task}\;(\mathrm{F2,F4,F6,F7})}
$$

**符号说明**

- $c$：被多个下游任务共同使用的原始上下文。
- $\mathcal{T}_c$：共享该上下文的任务集合。
- $q_t$：任务 t 对应的问题。
- $\mathcal{I}$：四个 LLM 调用阶段使用的指令提示集合。
- $I_c$：Compiler 为该上下文生成的类型化 JSON 中间表示。
- $\mathcal{M}_c$：CodeGen 为该上下文生成的模块集合，可包含规则检查器、格式验证器和数据分析器。
- $s_c$：数据分析器对上下文数据预执行后得到的缓存摘要；未生成或未成功运行时为空。
- $\tau(c)$：按模型上下文窗口进行头尾截断后的原始上下文。
- $d_t$：Reasoner-1 针对任务 t 生成的回答草稿。
- $\mathcal{V}_c$：在草稿上运行的验证器子集，即规则检查器与格式验证器。
- $\theta$：启动修正所需的违规数量阈值，本文设为 2。
- $y_t$：任务 t 的最终输出。

<div class="equation-explanation" markdown="1">

**直观理解**：等式左侧表示在给定上下文和指令时生成整组最终答案的过程；右侧先产生一次性的上下文产物 $I_c$、$\mathcal{M}_c$ 和 $s_c$，再对每个问题分别生成草稿并决定是否修正。其重点不是提出新的训练损失，而是明确计算复用边界：编译和代码生成成本可在共享上下文的任务间摊销，回答与校验则必须逐题执行。<br>
**原文位置**：公式（1），§3.2 Pipeline as a Composition

</div>

</div>

<div class="equation-block" markdown="1">

#### 违规聚合与门控输出规则

$$
v_t=\bigcup_{m\in\mathcal{V}_c}m(d_t),\qquad y_t=\begin{cases}\mathcal{R}_2(d_t,v_t),& |v_t|\geq\theta\ \text{且修正结果非空},\\ d_t,&\text{否则}.\end{cases}\quad \theta=2
$$

**符号说明**

- $v_t$：所有草稿期验证器针对任务 t 返回的违规项并集。
- $m$：验证器集合中的一个规则检查或格式检查模块。
- $\mathcal{V}_c$：适用于当前上下文的草稿期验证器集合。
- $d_t$：Reasoner-1 生成的原始草稿。
- $\mathcal{R}_2$：接收草稿和违规反馈并进行局部修正的第二阶段推理器。
- $\theta$：修正门槛，取值为 2。
- $y_t$：经过门控选择后的最终答案。

<div class="equation-explanation" markdown="1">

**直观理解**：系统先把不同验证器找到的问题合并；只有违规数达到阈值，且第二个推理器确实返回非空文本时，修正版才替换草稿。设置 $\theta=2$ 是一种保守策略，用多个违规信号抑制单次噪声检查触发不必要的修改，但它也可能放过仅有一项真实违规的草稿。<br>
**原文位置**：§3.2 对公式（1）第二个逐任务因子的展开；§3.6；附录B算法2第5—10行

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。CCA 不是通过参数更新训练一个新模型，也没有额外的监督损失或强化学习目标；论文描述的是围绕现有 LLM 的推理时架构。公式（1）是流水线的概率因子分解，用于表达各次 LLM 调用、生成模块和条件修正之间的依赖关系，而不是待端到端最小化的训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Compiler 与类型化 JSON IR**

IR 的顶层字段为 $\texttt{role}$、$\texttt{rules}$、$\texttt{knowledge}$、$\texttt{workflow}$、$\texttt{output\_spec}$、$\texttt{available\_tools}$、$\texttt{data\_profile}$ 和 $\texttt{compilation\_meta}$。每条规则保存标识、逐字规则、来源引文、$\texttt{codeable}$ 布尔值及可选代码提示；$\texttt{knowledge.exact\_terms}$ 保存角色名、工具名、状态码和标识符等必须原样复现的字符串，$\texttt{output\_spec.format\_type}$ 则在自然产物、工具序列、结构化数据和混合格式之间分类。

> 直观理解：类型化 IR 是方法的核心，因为它把容易被长文本淹没的硬约束变成显式槽位，并同时服务于回答模型和代码生成器。特别是精确术语字段，可直接提醒模型不要把评分器要求的字面字符串换成同义表达。

**2. CodeGen 与三类 Python 模块**

$\mathtt{RC}$ 在回答文本中检查可机械判定的规则，$\mathtt{FV}$ 检查结尾字符串、JSON 字段等格式要求，二者返回带规则标识和证据跨度的违规项；$\mathtt{DA}$ 则分析原始表格数据并生成可缓存摘要。各模块由独立 LLM 调用生成，提示明确要求避免假阳性，并通过异常捕获使代码故障返回空结果而非中断流程。

> 直观理解：三类代码分别回答“内容是否违反硬规则”“格式是否合格”和“数据中能提前算出什么”。保守地少报也不要误报，是因为错误指控会诱使第二个推理器修改本来正确的回答。

**3. 双 Reasoner 与违规门控修正**

$\mathcal{R}_1$ 使用 IR 清单、可选数据摘要、截断原文和问题产生 $d_t$；随后仅在 $|v_t|\geq2$ 时调用 $\mathcal{R}_2$，并要求其依据违规列表做最小编辑。$\mathtt{DA}$ 不参与草稿违规检测，因为其结果已经在生成前写入 $s_c$；若修正版为空，输出回退为 $d_t$。

> 直观理解：第一个模型负责完整作答，程序负责发现可明确定位的遗漏，第二个模型只负责修补。门控和回退机制避免所有答案都无条件经历一次可能引入新错误的重写。

**训练与推理**

整个方法属于推理时编排。对于每个上下文组，先运行一次 Compiler 得到 $I_c$，再由 CodeGen dispatcher 生成适用的 $\mathtt{RC}$、$\mathtt{FV}$ 和 $\mathtt{DA}$；若存在 $\mathtt{DA}$，则立即对原始数据运行并缓存 $s_c$。这些上下文级产物随后供该组内全部问题复用。对于每个任务 $t$，系统先用推荐策略决定是否保留 $s_c$，再将 IR 清单、可选摘要、截断上下文和 $q_t$ 交给 $\mathcal{R}_1$ 生成 $d_t$；接着运行 $\mathtt{RC}$ 与 $\mathtt{FV}$ 汇总 $v_t$。若 $|v_t|\geq2$，则调用 $\mathcal{R}_2$ 做最小修正，否则直接返回草稿；修正结果为空时同样回退到 $d_t$。原文未描述对基础模型、Compiler、CodeGen 或 Reasoner 进行专门微调。

**复现信息**

公平复现时最关键的是保持 IR 模式、模块派发条件、提示中的保真与保守检查原则，以及上下文级和任务级计算的分界。Compiler 必须逐字保存反事实内容和 $\texttt{exact\_terms}$；规则需带 $\texttt{codeable}$ 标记。派发条件分别为：至少一条可编码规则生成 $\mathtt{RC}$，不少于三条格式规则生成 $\mathtt{FV}$，TSV、CSV 或行内表格生成 $\mathtt{DA}$；只有推荐策略为数据分析或计算器时才向 $\mathcal{R}_1$ 注入成功的 $s_c$。生成代码应优先避免假阳性，并置于异常捕获中，使失败返回空结果。超长上下文采用约 $70\%$ 头部、约 $30\%$ 尾部并插入截断标记；修正阈值固定为 $\theta=2$，反馈限制为前十项、每项 200 字符，并要求仅做局部编辑。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- CL-bench：共 1,899 个长上下文任务，分属四个领域和 18 个子类别，其中领域知识推理 DKR 有 663 题、规则系统应用 RSA 有 566 题、程序性任务执行 PTE 有 471 题、经验发现与模拟 EDS 有 199 题。每题包含长上下文、问题及 5–20 条独立评分准则；上下文中位长度为 20K 字符，最大为 247K 字符。该数据集用于检验模型能否同时遵守上下文中的全部知识、规则和输出格式要求。原文未明确报告训练集、验证集和测试集的进一步划分；实验在完整 1,899 题上报告结果。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**整题通过率（task pass rate）**

每条 rubric 准则先由强判定模型独立评分；只有一题的全部准则均满足时才算通过。它衡量答案是否完整遵守上下文中的所有要求，而不是只答对主要内容。 （越高越好，因为任何遗漏的必做规则、违反的禁止规则或格式错误都会使整题失败。）

</div>
<div class="metric-item" markdown="1">

**验证器触发率（verifier-fire rate）**

可执行验证器发现的违规数量达到阈值 $|v_t|\geq\theta=2$ 的任务比例，用于诊断多少初稿需要进入第二轮纠错。 （不是单调越高或越低越好；较高表示初稿违规较多且纠错调用更频繁，较低既可能表示初稿更好，也可能表示验证机制未启用。）

</div>
<div class="metric-item" markdown="1">

**平均每题 token 消耗**

统计 Reasoner-1 与按条件调用的 Reasoner-2 的输入和输出 token 总量，用于衡量在线推理成本；按上下文运行一次的 Compiler、CodeGen 和数据分析阶段不计入该表。 （在通过率相近时越低越好；应与准确性提升联合判断，而不能脱离效果单独比较。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四个基础模型上的总体比较：Full CCA 对 Vanilla、ReadAgent-P 与 Ctx2Skill

<div class="result-value" markdown="1">

作者报告 CCA 在四个基础模型上都优于三种对照方法；其中 Kimi K2.5 的整题通过率由 Vanilla 的 15.4% 提升到 21.4%，绝对提高 6.0 个百分点。

</div>

这说明把长上下文先编译为固定槽位的规则表示，再执行验证和按违规触发的纠错，比单次直接作答以及两类既有长上下文策略更可靠。由于这里只给出了 Kimi K2.5 的具体数值，不能据此推断其他三个模型的增幅大小，也不能把结果外推到 CL-bench 之外的数据集。

<div class="result-source" markdown="1">

来源：Abstract；总体结果对应 Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On CL-bench (1,899 tasks across 4 open base models), CCA outperforms vanilla prompting and two long-context baselines (ReadAgent-P, Ctx2Skill) on every base model, lifting Kimi K2.5 from 15.4% to 21.4% with gains concentrated on rule-dense sub-categories.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Kimi K2.5 上按领域比较 Full CCA 与 Vanilla

<div class="result-value" markdown="1">

Full CCA 在 DKR、RSA 和 PTE 上的通过率分别为 21.1%、21.2% 和 26.1%，而 Vanilla 分别为 16.7%、13.4% 和 17.2%；增益集中于需要遵守密集规则或步骤的 RSA 与 PTE。

</div>

领域分解支持作者关于“结构化规则编译尤其适合规则密集任务”的解释：RSA 和 PTE 不仅要求找到相关信息，还要求同时满足多项约束与程序步骤。不过这是按领域观察到的相关模式，并非随机化因果实验，不能单凭该表证明规则密度是增益的唯一原因。

<div class="result-source" markdown="1">

来源：Appendix G.1，Table 8；Vanilla 行：16.7 | 13.4 | 17.2 | 12.1 | 15.40；Full CCA 行：21.1 | 21.2 | 26.1 | 11.6 | 21.40

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Per-domain pass rate (%) of each ablation variant on Kimi K2.5, bracketed by Vanilla (top) and Full CCA (bottom) for reference.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 开放式 EDS 领域上的适用边界

<div class="result-value" markdown="1">

Full CCA 在 EDS 上通过率为 11.6%，低于 Vanilla 的 12.1%；与前三个领域的提升方向不同。

</div>

该结果表明 CCA 并非对所有长上下文任务普遍有效。对于更开放、较难转写成明确规则和可执行检查项的发现与模拟任务，固定 IR、验证器和纠错循环可能缺少可利用的硬约束，甚至带来轻微负收益。0.5 个百分点的差异很小，且节选未给出该领域差异的置信区间，因此不能断言 CCA 在 EDS 上显著更差。

<div class="result-source" markdown="1">

来源：Appendix G.1，Table 8 caption

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The EDS column is comparatively flat across V6/V3/V2/V4/Full (∼6–12%), and Full CCA’s EDS (11.6) sits below Vanilla’s (12.1), supporting the §5.3 reading that CCA’s components offer little or negative lift on open-ended tasks.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验只使用 CL-bench 一个基准；虽然它覆盖四个领域和 18 个子类别，但所有任务共享严格的“每条 rubric 均满足才通过”评测机制。CCA 与这种可枚举规则、可执行检查的任务结构高度契合，因此尚不能确认其优势能推广到主观写作、开放式探索或没有明确评分准则的真实应用。
- 逐条准则由强 judge LLM 判定，节选未报告人工复核、一致性分析或判定模型敏感性；此外，Full CCA 的第二轮纠错在大量任务上触发并显著增加 token 消耗，离线编译成本又未计入 Appendix G 的每题 token 表，因此效果比较不能直接等同于完整的成本效益或延迟比较。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Vanilla：把原始上下文和问题直接交给模型生成答案，代表论文所批评的“读取并推理”范式，也是判断显式上下文编译是否有增益的最低控制组。
- ReadAgent-P：先把上下文分页并压缩为 gist，再根据问题检索至多 5 页原文，最后结合 gist、取回页面和问题作答。它代表长上下文摘要与检索路线，可检验 CCA 的规则结构化是否优于仅压缩、定位相关文本。
- Ctx2Skill：通过 Challenger、Reasoner、Judge、Proposer 和 Generator 的自博弈，从上下文构建技能库，推理时按相似度检索技能并与原始上下文共同输入。它代表计算量更高的多智能体知识归纳路线，可检验 CCA 是否必须依赖反复自博弈才能获得收益。

**实验想回答的问题**

- 在严格的长上下文任务上，CCA 相比直接读取上下文的 Vanilla、基于摘要检索的 ReadAgent-P 和基于多智能体自博弈的 Ctx2Skill，能否稳定提高整题通过率，并且这种收益是否跨不同基础模型成立？
- CCA 的收益来自哪些组件，是否主要出现在规则密集型任务上；相应的验证—纠错机制需要付出多少推理开销，又在哪类任务上可能无效？

**实验实现**

实验通过 AWS Bedrock 使用四个开放权重基础模型：Kimi K2.5、GLM-5、DeepSeek-V3.2 和 Qwen3-Next-80B。四者的输入窗口均能容纳 CL-bench 最长 247K 字符的上下文，因此模型边界处不截断输入。所有方法使用相同基础模型和相同通用作答条件，温度固定为 0.0；输出上限通常为 8,192 token，DeepSeek-V3.2 按其原生限制设为 16,384 token。官方 rubric 脚本调用强判定模型逐条检查准则。ReadAgent-P 沿用官方分页、gist 和检索提示，仅把面向多项选择题的最终提示改成 CL-bench 所需的自由文本提示；Ctx2Skill 保留官方五类智能体提示，只将调用层移植到相同的 Bedrock 基础模型。CCA、ReadAgent-P 和 Ctx2Skill 中可复用的上下文准备工作均按上下文摊销，而不是对每道题重复执行。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 在无 IR 检查清单的 V6 上加入 F2，将编译后的 IR 作为清单注入 Reasoner-1：V6 → V3 | 总体通过率从 17.22% 提升到 19.59%，增加 2.37 个百分点；RSA 从 16.6% 升至 18.0%，PTE 从 20.6% 升至 24.2%。与此同时，Reasoner-1 平均 token 消耗从 14,190 增至 16,353，约增加 2,100 token。 | 该消融主要隔离“把结构化 IR 明示给首轮推理器”本身的作用，不依赖验证器或第二轮纠错。结果显示 F2 是累计构建路径中最大的单项提升，尤其帮助规则密集领域；代价是提示中加入检查清单后首轮输入更长。它支持 IR 不只是离线存储格式，而能直接引导模型逐项遵守要求。 | Appendix G，Figure 3；Appendix G.1，Table 8；Appendix G.3，Table 10 caption<br><span class="experiment-evidence">Two patterns: (i) F2 adds ∼2,100 tokens to the Reasoner-1 input (14,190→16,353 V6→V3) because the IR checklist is rendered into the prompt; (ii) enabling F6 with the correction prompt costs an additional ∼10–11K tokens per task on average (V4 vs V3; Full vs V2), reflecting the fact that R-2 fires on ∼2/3 of tasks and re-encodes the prior conversation when it does.</span> |
| 检验 F2 与 F4/F6 验证—纠错循环的交互：Full−V3 对比 V4−V6 | 启用 F2 时，加入 F4 与 F6 的联合收益为 21.40%−19.59%=1.81 个百分点；关闭 F2 时，相同纠错机制的收益为 18.33%−17.22%=1.11 个百分点，两者相差 0.70 个百分点。Full CCA 的纠错触发率为 61.7%，平均总 token 为 27,660，而不运行 Reasoner-2 的 V2 为 16,384。 | 该比较说明结构化清单与后续纠错不是简单互不相关的模块：F2 先让初稿更接近规则要求，验证器给出的违规列表因而更集中，第二轮更容易进行针对性修复。不过纠错的在线代价明显高于 F2；交互量来自消融差分而非独立重复实验，节选也未提供该 0.70 个百分点交互的显著性检验。 | Appendix G.4；触发率见 Table 9，token 消耗见 Table 10<br><span class="experiment-evidence">With F2 on, F4 + F6 jointly contribute Full − V3 = 21.40 − 19.59 = +1.81 pp; with F2 off, they contribute only V4 − V6 = 18.33 − 17.22 = +1.11 pp.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper improves long-context instruction following by compiling prose into a structured intermediate representation and applying verification and correction.; rule check: matched taxonomy keywords; top rule score=10.0
- 全文指纹：`f2af564ce6924f40180ef31faf07ed79ba9379e45e9ffb1249e11cd7a5b6cc64`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
