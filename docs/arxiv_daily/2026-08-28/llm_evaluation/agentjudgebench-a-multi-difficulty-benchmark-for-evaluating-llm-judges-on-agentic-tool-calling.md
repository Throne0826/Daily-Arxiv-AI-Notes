---
title: "[论文解读] AgentJudgeBench: A Multi-Difficulty Benchmark for Evaluating LLM Judges on Agentic Tool-Calling"
description: "[arXiv 2608.26623][LLM 评测] 本文提出 AgentJudgeBench，用受控难度的工作流有向无环图、程序化参考答案及有无真实轨迹的配对条件，系统检验大语言模型裁判评估智能体工具调用时是否可靠。"
arxiv_id: "2608.26623"
announcement_date: "2026-08-28"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:32:01.767306+00:00"
source_sha256: "d5c7f1e1c60a3117cdac8cdca354b40e9805dfe42fd4796f26d4a6637bce90d5"
tags:
  - "LLM 评测"
  - "LLM Agent"
  - "LLM Reasoning"
  - "LLM-as-a-judge"
  - "智能体工具调用"
  - "有向无环图"
  - "裁判可靠性"
  - "程序化评测"
  - "结构化工作流"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.26623</p>

# AgentJudgeBench: A Multi-Difficulty Benchmark for Evaluating LLM Judges on Agentic Tool-Calling

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Abhigya Verma, Amit Kumar Saha, Seganrasan Subramanian, Sai Harshitha Aluru</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26623v1) · [PDF 下载](https://arxiv.org/pdf/2608.26623v1) · **关键词** LLM-as-a-judge, 智能体工具调用, 有向无环图, 裁判可靠性, 程序化评测, 结构化工作流<br>
**代码**: [https://github.com/ServiceNow/SyGra/tree/scratch/agent_judge_bench/tasks/agentic_bfcl_judge_eval](https://github.com/ServiceNow/SyGra/tree/scratch/agent_judge_bench/tasks/agentic_bfcl_judge_eval) · **项目页**: [https://huggingface.co/datasets/ServiceNow-AI/AgentJudgeBench](https://huggingface.co/datasets/ServiceNow-AI/AgentJudgeBench)

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

本文提出 AgentJudgeBench，用受控难度的工作流有向无环图、程序化参考答案及有无真实轨迹的配对条件，系统检验大语言模型裁判评估智能体工具调用时是否可靠。

**不用术语来说**：智能体完成任务时，往往需要选择多个工具、填写参数，并按依赖关系安排调用顺序；任何一步出错都可能导致整个任务失败。实际评测常让另一个大语言模型充当裁判，但这种裁判可能只看到用户请求和工具说明，未必能够重新推导出正确流程。因此，一个看似合理的评分可能掩盖错误工具、错误参数、顺序冲突或任务遗漏，而现有汇总分数又难以说明裁判究竟在哪些结构和难度下失效。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 构建包含 3,808 条记录的 AgentJudgeBench，覆盖六种工作流有向无环图拓扑和三个受控难度层级，并为每条记录提供经程序验证的真实工具调用轨迹。
- 提出按工具选择、参数结构、调用顺序和查询覆盖四个维度分解的可靠性协议，在提供与不提供真实轨迹的配对条件下比较大语言模型裁判与程序化参考评分的一致性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究“大语言模型充当裁判”（LLM-as-a-judge）在智能体工具调用评测中的可靠性。与对话、摘要等文本任务不同，工具调用的正确性主要不是语言是否流畅，而是智能体是否从带类型约束的工具模式中选择正确工具、填写合法参数、按照依赖关系安排调用顺序，并完整覆盖用户请求。现有工具调用基准通常把 LLM 裁判当作评测组件，只报告总体通过率或少量人工一致性结果；本文则把裁判本身作为研究对象，在受控难度和工作流结构下，比较其判定与可程序化验证参考之间的一致程度。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**智能体工具调用**

模型不只生成自然语言，还需根据用户请求选择外部函数或 API，并输出符合工具模式的参数。多步任务中，后续调用还可能依赖前序调用的结果。

</div>
<div class="concept-item" markdown="1">

**有向无环图（DAG）**

DAG 用节点表示工具调用，用有向边表示执行依赖，即一项调用必须在另一项完成后才能开始；“无环”保证依赖不会形成循环。它能够同时表达串行、并行以及多分支汇合等工作流。

</div>
<div class="concept-item" markdown="1">

**LLM-as-a-judge**

让一个大语言模型读取任务、工具定义及候选智能体输出，并给出正确性评分或判定。本文关心的不是生成器能否完成任务本身，而是这种自动裁判能否稳定复现程序化参考或人类判断。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

每个评测实例包含用户查询、带类型信息的工具或函数模式、由 DAG 描述的多步调用依赖，以及经过程序验证的标准调用轨迹；五个生成器产生候选工具调用方案，六个 LLM 裁判分别在“可见标准答案”和“不可见标准答案”两种配对条件下评分。裁判输出位于离散集合 $\{0,0.5,1\}$，并沿工具选择、参数结构、调用顺序和查询覆盖四个维度进行判断；随后将 LLM 裁判结果与程序化裁判结果比较，以衡量裁判一致性，而非直接衡量智能体能力。基准共有 3,808 个 BFCL 风格实例，覆盖六种 DAG 拓扑与三个受控难度层级；核心假设是标准轨迹及程序化评分可作为结构正确性的参考，同时通过有无标准答案的成对设计，区分“核对现成轨迹”与“仅凭查询和工具模式重建正确轨迹”这两种难度不同的裁判场景。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$G=(V,E)$**

工具调用工作流的有向无环图；$V$ 为工具调用节点集合，$E$ 为调用之间的先后依赖边集合。

</div>
<div class="notation-item" markdown="1">

**$\tau$**

一条多步工具调用轨迹，即按依赖关系组织的工具及参数序列。

</div>
<div class="notation-item" markdown="1">

**$y\in\{0,0.5,1\}$**

LLM 裁判针对某一评测维度给出的离散判定，分别表示不满足、部分满足或满足。

</div>
<div class="notation-item" markdown="1">

**$\kappa$**

衡量不同裁判在扣除偶然一致后仍有多大一致性的统计量；本文用它分析裁判间一致程度。

</div>

</div>

**直接相关的工作**

- **BFCL（Patil et al., 2025）**: BFCL 使用带类型的 JSON 函数模式，并通过抽象语法树与标准答案进行确定性比较，是本文数据格式最直接的结构来源。AgentJudgeBench 保留其模式，但把单轮函数调用扩展为具有三档难度的多步 DAG 工作流，并将研究对象从生成器表现转向 LLM 裁判可靠性。
- **FuncBenchGen（Maekawa et al., 2025）**: FuncBenchGen 同样将多步工具调用表示为复杂度可控的 DAG 遍历，因此在任务结构上最接近本文；但它用于训练和评估生成智能体，而本文通过有标准答案／无标准答案的配对条件及四维评分分解，专门测量裁判对生成结果的判断是否可靠。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型裁判已被用于自动评估智能体工具调用，但此类任务的正确性不是语言是否流畅或回答是否讨喜，而是工具、参数、依赖顺序和用户意图覆盖是否同时正确。尤其在没有真实执行轨迹这一常见部署条件下，裁判必须仅凭查询与工具模式重建应有流程；若其判断不可靠，开发者就可能选错智能体、误判系统能力，或把有结构性缺陷的轨迹判为合格。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **文本型 LLM-as-a-Judge 评测**：让大语言模型依据提示、评分准则或成对候选，对对话、摘要、指令遵循等开放文本进行打分或偏好判断；这类研究主要分析文本质量判断中的偏差、稳定性和与人类评价的一致性。
- **工具调用基准中的聚合式裁判一致性评估**：现有工具调用工作通常让大语言模型或自动评分器判断智能体输出是否通过，再汇总总体通过率或一致率；不同工作可能采用不同数据和裁判设置，但通常不系统操纵工作流拓扑、任务难度及是否向裁判提供真实轨迹。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 开放文本评测的经验不能直接迁移到依赖驱动的工具调用：后者存在工具选择、参数结构、调用顺序和查询覆盖四类相对独立的错误，裁判可能擅长识别其中一类，却忽略扇入或菱形工作流中的跨分支依赖，因而总体评分无法揭示具体失效机制。
- 既有工具调用基准多报告聚合通过率一致性，却没有在同一记录上配对比较有真实轨迹与无真实轨迹条件，也未控制拓扑和难度；因此无法判断误差来自模型容量、缺少参考信息还是任务结构本身，更不足以指导裁判选择、提示设计及评分解释。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前缺少一个专门面向智能体工具调用裁判的校准框架：它应当具有程序可验证的逐条参考轨迹，能够独立改变工作流拓扑与查询难度，分别测量多种结构性正确性，并在相同样本上比较裁判获得和未获得真实轨迹时的表现。没有这一框架，就无法识别大语言模型裁判是否存在随难度加剧的共同上限、不同裁判是否发生相关性失误，以及提供参考答案是否始终有益。

</div>
<div markdown="1"><span>核心问题</span>

在不同工作流拓扑与难度下，大语言模型裁判对智能体工具调用的判定与程序化参考评分有多一致；这种一致性如何受到真实轨迹可见性、裁判模型、生成器以及温度、思维链和评分提示格式的影响？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把笼统的“裁判是否准确”拆成可控制、可对照的问题：有向无环图明确表示工具调用之间的先后依赖，难度改写逐步增加裁判需要推理的负担，四项指标则定位错误来源；再让同一裁判对同一输出分别在有、无真实轨迹时评分，并与确定性的程序评分器比较。这样既能隔离缺少参考信息造成的额外困难，也能观察扩大模型规模或改变提示是否真正突破结构性瓶颈，而不是仅提高某个汇总分数。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

AgentJudgeBench不是训练新的评审模型，而是构造一条可控、可复现的评测流水线，用来检验大语言模型评审者能否正确判断智能体的工具调用。系统先从企业领域种子生成带有工具模式、依赖关系和已验证执行轨迹的记录，并在保持工作流结构及真实轨迹不变的条件下，将每条记录改写为易、中、难三个查询版本；随后多个生成模型输出预测工具调用序列。确定性程序评审器依据真实序列，从工具选择、参数结构、调用顺序和查询覆盖四个维度产生参考向量；每个大语言模型评审器则在“提供真实轨迹”和“不提供真实轨迹”两种提示条件下独立打分，最后以两类评分的距离计算对齐率。
技术上，该设计把“生成模型是否完成任务”和“评审模型能否识别完成质量”分开：生成模型的输出可以有好有坏，但所有评审模型都面对同一输出，并与同一确定性参考比较。直观地说，这相当于先用规则明确、可重复的标准答案批改一份工具调用作业，再让不同大模型也批改同一份作业；研究对象不是学生得分本身，而是大模型老师的评分与规则老师有多一致。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 合成并验证工作流记录

流水线生成用例场景、带类型约束的工具函数签名、连接工具依赖的可执行伪代码、自然语言查询、JSON输入输出模式，以及包含顺序与并行调用的有序真实执行轨迹。每条记录经JSON模式、参数类型、轨迹一致性、参数充分性、语义落地和查询自然度检查，失败记录被重新生成，且质量门控不使用任何大语言模型。

<div class="method-step__io" markdown="1">

**输入**：企业领域标签，以及用于扩展场景的最小种子输入。<br>
**输出**：具有已验证真实轨迹、工具集合和工作流依赖结构的完整智能体记录。

</div>

**直观理解**：这一阶段相当于先制作一套答案可核验的流程题，而不是从企业日志中抽取答案不确定的样本。规则检查保证后续比较所依赖的“标准答案”至少在结构和内容约束上自洽。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 控制拓扑与查询难度

记录被组织为线性、扇出、扇入、菱形、可选增强和类循环六种有向无环工作流拓扑，并在任务结构与真实轨迹保持不变时，将用户查询改写为易、中、难三个版本。难度主要通过增加查询歧义来改变，从而尽量把结构复杂度和语言难度作为可区分因素。

<div class="method-step__io" markdown="1">

**输入**：已验证的基础记录及其固定真实轨迹。<br>
**输出**：覆盖六种拓扑和三个难度层级的评测实例。

</div>

**直观理解**：同一道流程题保留相同答案，只把题目说得更直接或更含糊，因此可以观察评审者是否因理解难度上升而退化。原文同时提醒，中等版本有时只是改写而非严格变难，所以中到难的比较更可信。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成候选工具调用

每个生成模型 $g\in\mathcal{G}$ 为记录生成有序工具调用序列 $G=(g_1,\ldots,g_{|G|})$，其中每次调用包含工具标识符和参数。预测序列与真实序列 $E=(e_1,\ldots,e_{|E|})$ 一同送入后续评审层。

<div class="method-step__io" markdown="1">

**输入**：各难度版本的用户查询、可用工具模式及相关记录上下文。<br>
**输出**：供程序评审器和所有大语言模型评审器共同评价的候选工具调用序列。

</div>

**直观理解**：生成模型扮演“答题者”，输出它认为应调用哪些工具、按什么顺序调用以及填写哪些参数。固定候选答案后，才能公平比较不同“阅卷者”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 双轨评审

确定性程序评审器从工具选择、参数结构、顺序和覆盖率四个维度生成参考向量 $\mathbf{p}_r$；大语言模型评审器 $j\in\mathcal{J}$ 则分别在with-GT与without-GT提示下，对相同四维度给出 $\{0,0.5,1\}$ 中的分数、一句理由和总体评价。所有生成器、评审器、难度和条件组合采用固定解码设置，以减少无关变化。

<div class="method-step__io" markdown="1">

**输入**：原始查询、完整工具模式、生成模型的预测序列，以及仅在with-GT条件下提供的真实工具调用序列。<br>
**输出**：每条记录的程序参考向量，以及每个大语言模型评审器在两种真实轨迹可见性条件下的四维裁决。

</div>

**直观理解**：规则评审器像按检查清单逐项核对；大模型评审器既要在看答案时批改，也要在不看答案时仅凭题目和工具说明判断。两种条件的差异直接反映真实轨迹究竟提供帮助，还是造成过度依赖。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 程序评审器的四维参考评分

$$
\begin{aligned}
p^{\mathrm{tool}}&=\max\!\left(0,1-\frac{|\mathcal{G}\setminus\mathcal{E}|+|\mathcal{E}\setminus\mathcal{G}|}{\max(|\mathcal{E}|,1)}\right),\\
p^{\mathrm{seq}}&=\frac{1}{\max(|E|,1)}\sum_{i=1}^{\min(|G|,|E|)}\mathbb{1}[\mathrm{name}(g_i)=\mathrm{name}(e_i)],\\
s(g)&=\begin{cases}1,&A_g=A_g^*,\\0.5,&A_g^*\subseteq A_g\ \land\ A_g\setminus A_g^*\neq\emptyset,\\0,&A_g^*\not\subseteq A_g\ \text{or }A_g^*\text{ undefined},\end{cases}\\
p^{\mathrm{param}}&=\frac{\sum_{g\in G}s(g)}{\max(|G|,1)},\\
p^{\mathrm{cov}}&=\begin{cases}1,&\mathcal{E}=\emptyset,\\0,&\mathcal{G}\cap\mathcal{E}=\emptyset,\\|\mathcal{G}\cap\mathcal{E}|/|\mathcal{E}|,&\text{otherwise}.
\end{cases}
\end{aligned}
$$

**符号说明**

- $G=(g_1,\ldots,g_{|G|})$：生成模型预测的有序工具调用序列。
- $E=(e_1,\ldots,e_{|E|})$：真实的有序工具调用序列。
- $\mathcal{G}$：预测序列中工具标识符构成的无序集合。
- $\mathcal{E}$：真实序列中工具标识符构成的无序集合。
- $A_g$：预测调用g所含的参数键集合。
- $A_g^*$：真实序列中同名工具应具有的参数键集合；若预测工具不在真实工具集合中则未定义。
- $s(g)$：单次预测调用的参数结构分数：完全匹配为1，仅有额外参数为0.5，缺少必需参数或工具错误为0。
- $\mathbb{1}[\cdot]$：指示函数，条件成立取1，否则取0。
- $p^{\mathrm{tool}},p^{\mathrm{param}},p^{\mathrm{seq}},p^{\mathrm{cov}}$：工具选择、参数结构、调用顺序和查询覆盖四项程序参考分数。

<div class="equation-explanation" markdown="1">

**直观理解**：工具选择分数同时惩罚多调用和漏调用；顺序分数按真实序列长度归一化，因此缺失位置不会被忽略。参数评分允许“必需键齐全但多带键”的调用获得部分分，覆盖率则只关心应调用工具是否出现而不惩罚额外工具；四者共同提供比单一完全匹配更细粒度的参考。<br>
**原文位置**：第3.2节，公式(1a)、(1b)、(2)和(3)

</div>

</div>

<div class="equation-block" markdown="1">

#### 评审对齐率与真实轨迹增益

$$
\begin{aligned}
\mu^m_{j,r,c}&=1-|p_r^m-\ell^m_{j,r,c}|,\\
\mu_{j,r,c}&=\frac{1}{M}\sum_{m=1}^{M}\mu^m_{j,r,c},\\
\mathrm{align}(j,g,d,c)&=\frac{100}{N_{g,d}}\sum_{r=1}^{N_{g,d}}\mu_{j,r,c},\\
\mathrm{lift}(j)&=\overline{\mathrm{align}}_{\mathrm{GT}}(j)-\overline{\mathrm{align}}_{\mathrm{without\ GT}}(j).
\end{aligned}
$$

**符号说明**

- $j$：被评估的大语言模型评审器。
- $r$：一条评测记录。
- $c$：提示条件，取with-GT或without-GT。
- $m$：四个评分维度之一，即tool、param、seq或cov。
- $p_r^m$：程序评审器对记录r在维度m上的参考分数。
- $\ell^m_{j,r,c}$：评审器j在条件c下对记录r的维度m给出的离散分数。
- $\mu^m_{j,r,c}$：单项评分匹配度，分数差越小则越接近1。
- $M$：评分维度数量，本文为4。
- $N_{g,d}$：生成器g与难度d这一配置中的记录数量。
- $\mathrm{align}(j,g,d,c)$：评审器在指定生成器、难度和提示条件下的百分比对齐率。
- $\mathrm{lift}(j)$：提供真实轨迹相对于不提供真实轨迹带来的平均对齐率变化。

<div class="equation-explanation" markdown="1">

**直观理解**：单项匹配度等于1减去两种分数的绝对差，因此完全相同得1，相差0.5得0.5，最大分歧得0；四项平均后，再跨记录换算为百分比。真实轨迹增益为正表示看答案后更接近程序参考，为负则意味着答案可能诱发过度锚定或其他判断偏差。<br>
**原文位置**：第3.2节，公式(4a)、(4b)、(5a)和(5b)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该方法是基准构建与推理期评测流程，不对生成模型、评审模型或程序评审器进行参数训练，也没有通过上述对齐率反向优化模型；$\mathrm{align}$和$\mathrm{lift}$仅用于测量与比较评审可靠性。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 受控合成数据与质量门控模块**

该模块在15个企业领域中生成完整记录，每条记录含8至19个工具，并覆盖六种依赖拓扑；最终语料包含3,808条基础记录及其难度变体。真实轨迹依次通过结构验证和语义相关的程序检查，且困难样本上的120条人工验证用于外部检查程序评分器与独立人工判断的一致范围。

> 直观理解：它的核心价值不是追求日志的自然分布，而是确保每道题都有可认证答案，并能独立控制拓扑和难度。代价是合成数据可能与真实企业环境存在领域漂移，也没有完整覆盖交互式多轮执行。

**2. 四维确定性程序评审器**

程序评审器把预测序列 $G$ 与真实序列 $E$ 比较：工具选择检查两者工具集合的缺失与多余项；参数结构检查必需参数键是否齐全以及是否存在额外键；顺序分数逐位置比较工具标识符；覆盖率检查预期工具中有多少被预测命中。四项结果组成 $\mathbf{p}_r=(p_r^{\mathrm{tool}},p_r^{\mathrm{param}},p_r^{\mathrm{seq}},p_r^{\mathrm{cov}})$，需要单一生成质量分数时才使用等权平均。

> 直观理解：四个维度分别回答“工具选对了吗、参数框架对吗、调用次序对吗、任务需要的工具覆盖了吗”。将它们分开可避免某一方面的正确掩盖另一重要方面的错误，也允许实际应用按风险重新加权。

**3. 成对提示的大语言模型评审与对齐聚合器**

每个评审器接收查询、全部工具模式和候选调用序列；with-GT提示额外包含真实调用序列，without-GT提示完全省略该信息。聚合器将离散裁决 $\ell_{j,r,c}^m\in\{0,0.5,1\}$ 与连续程序分数 $p_r^m\in[0,1]$ 比较，并分别保留总体与逐指标对齐结果。

> 直观理解：成对提示让研究者在其他输入基本相同的情况下，只改变评审者是否看到答案。聚合器衡量的是评审可靠性，而不是直接把大模型给出的高分当作生成系统表现良好的证据。

**训练与推理**

训练阶段不适用。推理与评测时，先对每条记录生成三个难度版本，再让每个生成模型产生工具调用预测；程序评审器对预测计算四维参考向量。随后每个大语言模型评审器对同一预测执行两次独立评审：一次看到真实轨迹，一次看不到真实轨迹，并输出固定JSON结构中的四项分数及理由；最后聚合器计算逐记录匹配度、配置级对齐率和评审器级真实轨迹增益。整个设计形成生成器、评审器、难度与提示条件的全因子比较，但程序参考本身保持确定性。

**复现信息**

完整流水线以SyGra图式合成数据框架实现为计算图。工具模式采用带类型参数和受约束返回类型的函数签名，返回类型包括$\mathrm{str}$、$\mathrm{bool}$、$\mathrm{list}$、$\mathrm{dict}$和$\mathrm{None}$；记录以JSON模式明确参数类型、必填字段和输出定义。为公平解释结果，大语言模型评审器的解码设置在所有$(g,j,d,c)$组合中保持不变，且with-GT与without-GT提示仅在是否加入真实调用序列这一关键条件上不同。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- AgentJudgeBench：包含 3,808 条唯一工作流记录；每条记录有 easy、medium、hard 三种查询改写，共 11,424 行。记录覆盖 linear、fan-out、fan-in、diamond、optional enrichment 和 loop-like 六类 DAG 拓扑，来自 15 个企业种子领域。每条记录提供 8–19 个候选工具，GT 轨迹实际调用 2–5 个工具，用于同时检验工具选择、参数填写、调用顺序和需求覆盖。
- 全因子评测样本：交叉组合 5 个生成器、6 个主要裁判器、3 个难度及有/无 GT 两种条件，形成 90 个因子单元和 321,648 个有效的“生成器—裁判器—难度—记录”元组。该设计用于分离生成器质量、裁判器能力、查询难度和 GT 可见性对评分一致性的影响。
- 人工验证子集：用于比较裁判器与人类标注者的一致性并检查程序化参考是否等同于人类判断；所给章节未明确报告该子集的规模、抽样方式及划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**裁判器—程序化参考一致率（alignment）**

衡量 LLM 裁判器给出的逐指标分数与程序化参考分数相同的比例，并可按生成器、裁判器、难度和 GT 条件聚合。论文还将其拆分到工具选择、参数结构、调用顺序和查询覆盖等维度，以定位错误来源。 （越高越好，因为更高表示裁判器更常复现预先定义的结构化参考判断；但它只说明与程序化参考一致，不自动等价于更符合人类偏好。）

</div>
<div class="metric-item" markdown="1">

**GT lift**

比较同一配置在提供 GT 与不提供 GT 时的一致率差异，用于判断展示标准执行轨迹究竟帮助裁判器识别错误，还是使其过度依赖参考轨迹的表面顺序。 （通常正值表示 GT 提升了与程序化参考的一致性；负值表示提供 GT 后一致性反而下降，但需要结合功能等价调用序列分析，不能简单解释为模型能力下降。）

</div>
<div class="metric-item" markdown="1">

**裁判器间一致率与 Cohen's $\kappa$**

精确一致率统计两个裁判器给出相同逐指标分数的频率；Cohen's $\kappa$ 进一步扣除随机一致的影响，$0$ 表示机会水平，$1$ 表示完全一致。 （越高通常表示裁判器判断更稳定，但高一致也可能由提示词把输出压缩到同一默认分数造成，因此必须结合与程序化参考或人类标注的一致性解释。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 全部 30 个生成器—主要裁判器组合，在有 GT 和无 GT 条件下比较 easy、medium、hard 三档难度。

<div class="result-value" markdown="1">

所有 30 个组合的一致率都随难度严格单调下降；无 GT 时的下降幅度约为有 GT 时的 $1.5$ 倍。在五个生成器中的四个上，hard 且无 GT 时六个裁判器集中在 77%–82% 的窄区间，包括 GPT-5.4 生成器。

</div>

作者据此主张，困难工作流带来的主要瓶颈是任务结构，而不只是裁判器规模不足：更大的裁判器没有拉开明显差距。分析上，这支持“共享结构性上限”，但不能证明该上限不可被新训练方法、外部执行验证器或不同评分协议突破；它只说明当前六个裁判器和本文提示设置下，单纯扩大模型能力不足。

<div class="result-source" markdown="1">

来源：第 4.2 节，Finding 1；表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

All 30 (generator, judge) pairs exhibit strictly monotone alignment degradation from easy to hard under both conditions (Table 2), without-GT degradation roughly 1.5× larger than with-GT. On hard without-GT records, all six judges converge to a narrow 77–82% band across four of five generators (including frontier GPT-5.4), indicating a task-level rather than judge-level ceiling; degradation curves are in Appendix F.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 比较各裁判器在标准 GT 可见与无 GT 条件下的评分，并用来自其他记录的错误 GT 进行 corrupted-GT 控制。

<div class="result-value" markdown="1">

GT 并非普遍有益：QwQ-32B 和 GPT-OSS-120B 的 GT lift 为正，而 GPT-5.4 与 Gemini-2.5-Pro 为负。错误 GT 控制中，Gemini-2.5-Pro 在标准 GT 与 corrupted GT 下表现相同；QwQ-32B 则与无 GT 结果相差不超过 0.2 个百分点。

</div>

作者将前沿裁判器的一致率下降解释为“过度锚定”：模型看到 GT 后，可能把参考轨迹的调用顺序当成唯一正确答案，从而惩罚功能等价但结构不同的序列。错误 GT 控制强化了锚定解释，因为裁判器可能追随所展示的轨迹而非独立验证其正确性；不过该实验仍不能单独确定锚定发生于哪一步推理，也不能证明所有负 GT lift 都由同一机制导致。

<div class="result-source" markdown="1">

来源：第 4.2 节，Finding 2 与 C3 control；表 1、图 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Replacing the reference with a wrong GT from a different record confirms pure anchoring (Table 1): Gemini-2.5-Pro aligns identically under standard and corrupted GT, while QwQ-32B tracks without-GT within 0.2 pp.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 在 5 个生成器、3 档难度和两种 GT 条件下比较六个主要裁判器的相对排名。

<div class="result-value" markdown="1">

不存在跨条件统一最优的裁判器。QwQ-32B 在有 GT 的 15 个“生成器—难度”单元中领先 10 个，但在无 GT 条件下从未排名第一；无 GT 时，Gemini-2.5-Pro 更常领先较强生成器，而 GPT-5.4 更常领先较弱生成器。

</div>

裁判器选择必须与生成器质量和 GT 可用性共同决定，不能仅按模型规模或单个总平均分部署。该结果证明的是排名具有配置依赖性，而不是 QwQ-32B、Gemini-2.5-Pro 或 GPT-5.4 在所有实际代理任务上的普遍优劣；测试范围仍受本文数据分布、评分规则和模型集合限制。

<div class="result-source" markdown="1">

来源：第 4.2 节，Finding 3；表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

QwQ-32B leads GT alignment in 10 of 15 (generator, difficulty) cells but is never the top without-GT judge; Gemini-2.5-Pro and GPT-5.4 lead without-GT on stronger and weaker generators, respectively.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主要“正确性”目标是与程序化参考一致，而非直接与人类判断一致；论文虽进行人工验证并称 GPT-OSS-120B 最符合人类，但所给章节没有报告验证子集规模、标注协议和完整排名。因此，程序化 alignment 的最佳裁判器不能直接解释为最可靠的人类代理。
- 若干机制结论来自有限配对：温度实验只复验两组裁判器—生成器组合，格式消融也仅覆盖两组且 hard 条件发生方向反转。数据的 DAG 拓扑分布还刻意模拟 15 个企业种子领域而非均匀采样，故结果未必推广到其他领域、更长执行轨迹、多轮交互、真实工具执行或本文未覆盖的裁判模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 程序化参考评分：从工作流结构和 GT 执行轨迹计算，被作为主要一致性目标。它提供可重复的大规模参照，但不应被直接视为人类判断的完全替代。
- Prometheus-2：专门训练的裁判模型，作为 judge-specialised baseline 加入全部生成器和两种 GT 条件。它不计入六个主要裁判器的均值或最佳值统计，用于检验专用裁判模型是否优于通用大模型。
- 六个通用裁判器：GPT-OSS-20B、QwQ-32B、GPT-OSS-120B、Claude Sonnet 4.5、Gemini-2.5-Pro 和 GPT-5.4，覆盖约 20B 到前沿模型规模。横向比较用于判断参数规模或模型层级能否稳定提升工具调用评分可靠性。
- 有 GT 与无 GT 条件：前者向裁判器提供标准执行轨迹，后者仅凭任务、工具定义和生成结果评分。这一配对条件直接测量外部参考信息的收益及其可能造成的锚定偏差。

**实验想回答的问题**

- LLM 裁判器对代理式工具调用的评分可靠性，如何随生成器能力、工作流 DAG 难度以及是否提供真实执行轨迹（GT）而变化？不同规模裁判器能否克服困难任务上的结构性评分上限？
- 评分误差来自哪些机制，包括具体评分维度、DAG 拓扑、GT 锚定、裁判器间分歧和提示词默认规则？温度、思维链及结构化评分格式等干预能否有效缓解这些误差？

**实验实现**

实验采用完全交叉设计：5 个生成器覆盖 3B 开源模型至 GPT-5.4，6 个主要裁判器覆盖 20B 至前沿规模；每一组合均在 easy、medium、hard 三档难度及有 GT、无 GT 两种条件下评估。另加入 Prometheus-2 供参考，但排除在六裁判器汇总统计之外。主要报告一致率和 GT lift，并通过逐指标分解、DAG 拓扑分解、裁判器两两一致性、人工验证及提示配置消融解释机制。表 2 每个生成器子块内的粗体值只表示相同难度和条件下六个主要裁判器中的最高一致率，并非跨生成器的全局最优。原文指出每个表 1 单元约含 3,764–3,771 条记录；模型标识、完整提示词及更多逐单元统计位于附录。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| C2 消融：将 hard、无 GT 提示中的默认评分从 1.0 改为 0.5，并按生成器对六个裁判器取平均。 | 三个较强生成器的提升不超过 1.0 个百分点：Llama-3.3-70B 为 +0.4、Qwen3-32B 为 +1.0、GPT-5.4 为 +0.5；两个较弱生成器提升明显，Llama-3.1-8B 为 +4.1、SmolLM3-3B 为 +5.6 个百分点。 | 该消融隔离了提示词默认分数对无 GT 收敛的影响。强生成器上的微小变化支持任务结构是其主要上限来源；弱生成器上的较大提升说明标准 1.0 默认值会过度奖励错误输出，因此上限高度也具有提示依赖性。它没有说明 0.5 是普遍最优默认值，只表明校准规则应随生成器质量调整。 | 第 4.2 节，RQ3，C2 ablation；表 4<br><span class="experiment-evidence">For the three strongest generators the delta is ≤ +1.0 pp, confirming structural task difficulty as the primary ceiling driver. For weaker generators (+4.1–+5.6 pp), the 1.0-default over-credits incorrect outputs; practitioners evaluating low-quality generators should consider the 0.5-default prompt.</span> |
| 提示输出格式消融：比较逐指标结构化 JSON 评分提示与自由文本提示，并在两组裁判器—生成器配对上复验。 | 在 Qwen3-32B 裁判 Llama-3.3-70B 的配对上，结构化格式在三档难度、有 GT 条件下提升 4.8–6.5 个百分点；在 QwQ-32B 裁判 SmolLM3-3B 的配对上，easy 和 medium 分别提升 3.9 和 2.4 个百分点，但 hard 上反而下降 0.8 个百分点。 | 该实验隔离了输出约束和逐指标 rubric 的作用。结构化格式通常能迫使模型分别检查各评分维度，是本文测试的最大配置杠杆；但 hard 条件出现反转，说明它不是与裁判器、生成器和难度无关的通用改进。由于格式变化与逐指标 rubric 同时出现，结果也不能完全区分收益来自 JSON 语法约束还是更明确的评分步骤。 | 第 4.2 节，RQ6；图 5，附录 R<br><span class="experiment-evidence">A second pairing (QwQ-32B on SmolLM3-3B) partially replicates this: structured format still wins on easy (+3.9 pp) and medium (+2.4 pp), but the effect shrinks relative to the first pairing and reverses on hard (−0.8 pp, free-form marginally ahead).</span> |

**定性案例**

- 附录 H 的案例被作者用于解释负 GT lift：GPT-5.4 和 Gemini-2.5-Pro 看到 GT 后会锚定参考轨迹的调用顺序，对功能上等价但结构上偏离 GT 的序列施加惩罚。所给章节未展示具体案例文本，因此无法进一步核验替代序列是否确实功能等价。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：构建基准以评测 LLM judge 对 Agent 工具调用工作流的可靠性，评测与 Agent 场景均为核心。; rule check: matched taxonomy keywords; top rule score=5.0
- 全文指纹：`d5c7f1e1c60a3117cdac8cdca354b40e9805dfe42fd4796f26d4a6637bce90d5`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
