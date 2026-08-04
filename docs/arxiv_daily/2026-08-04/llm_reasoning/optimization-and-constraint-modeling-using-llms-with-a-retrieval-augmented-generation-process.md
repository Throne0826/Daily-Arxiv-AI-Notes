---
title: "[论文解读] Optimization and Constraint Modeling using LLMs with a Retrieval Augmented Generation Process"
description: "[arXiv 2608.00015][LLM Reasoning] 本文研究能否利用经过验证的合成优化问题库与检索增强生成，为大语言模型提供结构相近的已解示例，从而在不微调模型的情况下提高自然语言到形式化优化模型的转换准确率。"
arxiv_id: "2608.00015"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:04:40.342058+00:00"
source_sha256: "2f9016a5d487901cd5dcd4da0ef2777871156f3655a4b5e46bd678331789fc16"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "检索增强生成"
  - "优化建模"
  - "约束规划"
  - "合成数据"
  - "向量数据库"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.00015</p>

# Optimization and Constraint Modeling using LLMs with a Retrieval Augmented Generation Process

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Prateek Roy, Akash Singirikonda</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.00015v1) · [PDF 下载](https://arxiv.org/pdf/2608.00015v1) · **关键词** 大语言模型, 检索增强生成, 优化建模, 约束规划, 合成数据, 向量数据库<br>


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

本文研究能否利用经过验证的合成优化问题库与检索增强生成，为大语言模型提供结构相近的已解示例，从而在不微调模型的情况下提高自然语言到形式化优化模型的转换准确率。

**不用术语来说**：现实中的物流、医疗、能源和供应链决策通常要先把文字描述转换成变量、目标和约束明确的数学模型，但这一步既需要领域知识，也要求熟悉建模语言。通用大语言模型虽然能生成模型或求解代码，却容易遗漏约束、破坏结构一致性，尤其难以处理需要多步推理的组合优化问题，因此不能直接作为可靠的决策支持工具。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 构建了一个包含500余个人工约束与优化问题的检索语料库；每个样本将自然语言描述、JSON形式化表示和可编译执行的Python求解脚本组织在一起，为模型提供格式统一的已解案例。
- 提出并评估了一条基于Chroma向量数据库、余弦相似度检索、语义网关和LangChain智能体的RAG推理路线，用于检验检索到的相似案例能否提升Qwen 3 30B Instruct生成优化模型的准确率。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于“大语言模型辅助数学建模”与检索增强生成的交叉领域。优化建模把自然语言中的决策需求转写为变量、变量取值域、约束条件和优化目标，并进一步生成可由求解器执行的程序；典型范式包括线性规划（LP）、混合整数线性规划（MILP）、混合整数非线性规划（MINLP）和约束规划（CP）。这类任务不仅要求理解业务语义，还要求输出在数学结构上完整且自洽：变量域错误、最大化与最小化方向颠倒或遗漏一条关键约束，都可能造成模型不可行、求解结果次优或程序无法执行。本文研究用检索增强生成（RAG）为大语言模型提供语义相近且经过执行验证的建模示例，使模型不只依赖参数中储存的知识，而能参照外部案例生成结构化模型与求解器代码。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**优化与约束建模**

优化模型通常由决策变量、变量取值域、约束和目标函数组成，用于在满足业务规则的可行方案中寻找成本最低或收益最高的方案。LP只含线性关系，MILP允许部分变量取整数或二元值，MINLP还允许非线性关系，而CP主要通过变量域与约束传播来搜索满足条件的赋值。

</div>
<div class="concept-item" markdown="1">

**检索增强生成（RAG）**

RAG先把输入问题与外部知识库中的条目比较，检索语义相近的案例，再将这些案例连同原问题一起交给大语言模型生成答案。本文中的外部知识不是普通文本资料，而是自然语言题目、结构化JSON表示和经过求解器执行验证的Python脚本所组成的建模案例。

</div>
<div class="concept-item" markdown="1">

**向量数据库与余弦相似度**

文本嵌入模型把问题描述编码为向量，向量数据库据此快速查找含义接近的历史问题；余弦相似度衡量两个向量方向的一致程度，通常越大表示语义越接近。本文使用Chroma保存案例向量，并以相似度检索和语义网关决定候选案例是否适合作为上下文。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一段自然语言描述的优化或约束问题，可能属于LP、MILP、MINLP或CP；目标输出是语义正确、结构完整且可供求解器使用的正式模型，包括明确的变量及其取值域、全部必要约束、方向正确的目标函数，以及相应的结构化JSON或Python求解代码。研究设置以Qwen 3 30B Instruct为基础模型，并比较直接生成与RAG辅助生成：后者从由500余个合成问题构成的Chroma库中检索相似的已解决案例，经语义网关筛选后作为上下文交给LangChain智能体。该设置依赖一个关键假设，即自然语言描述上的语义相似性通常对应底层优化结构的相似性，因此历史案例中的变量设计、约束模式和代码框架能够迁移到新题；但原文也限定了证据范围，指出数据由人工方式合成，脚本虽经过编译和执行检查，所有最优性证书的正确性并未得到领域专家独立确认。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

待建模的自然语言优化或约束问题；原文没有给出统一的形式化符号，此处仅用于概括任务输入。

</div>
<div class="notation-item" markdown="1">

**$e(x)$**

问题描述$x$经嵌入模型编码后得到的向量表示；原文说明了向量编码过程，但未明确指定该函数记号。

</div>
<div class="notation-item" markdown="1">

**$\operatorname{sim}(e(x),e(d))$**

输入问题$x$与数据库案例$d$在嵌入空间中的余弦相似度，用作检索及语义筛选信号；原文未给出具体阈值或统一公式。

</div>
<div class="notation-item" markdown="1">

**$d$**

检索库中的一个已解决案例，包含自然语言描述、JSON形式化表示和经过执行验证的Python求解脚本。

</div>

</div>

**直接相关的工作**

- **Text2Zinc**: Text2Zinc提供自然语言描述及对应的CP-SAT/MiniZinc形式化，是本文合成数据所用的种子描述来源。作者认为其问题集合规模有限且类型差异较大，不能直接满足本文对大规模、统一JSON结构和验证后Python求解代码的检索语料需求。
- **NL4OPT**: NL4OPT面向自然语言到LP/MILP模型的翻译，既代表已有优化建模数据资源，也被本文用作评测基准之一。作者指出该数据集对问题多样性和解答细节的覆盖仍不充分，因此本文并非以它构建完整检索库，而是用合成语料补充结构一致的已解案例。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

优化建模是现实决策系统将业务需求转化为可求解方案的关键环节，但自然语言需求与LP、MILP、MINLP或CP等形式化模型之间存在较高的知识门槛。若自动生成的模型结构不完整或约束错误，求解器即使能够运行，也可能求解错误的问题，进而影响资源配置和决策质量；因此需要一种既能提高建模可靠性、又不要求使用者掌握专业建模语言的辅助方法。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **直接使用通用大语言模型生成优化模型**：将自然语言问题直接交给预训练指令模型，由模型依赖其参数中已有的知识生成形式化模型或Python求解代码，不额外提供领域案例。该路线部署简单，适合作为本文衡量检索增益的直接LLM基线。
- **模型微调与检索增强生成**：微调通过领域样本更新模型参数，使输出适应特定建模任务；RAG则不改动模型参数，而是把问题编码后从外部案例库检索语义相近的已解问题，并将其作为上下文示例注入生成过程。本文选择后一条路线，并增加语义网关，只在检索结果满足相似性条件时接受相关上下文。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 直接生成依赖模型内部的参数化知识；面对结构严格、约束相互关联或需要多步推理的任务时，现有LLM会产生结构不一致或不完整的形式化结果，导致生成代码无法正确表达原问题。
- 微调需要额外的数据准备、训练计算和模型维护成本，而在优化建模场景中，原文指出此前尚未系统评估一种可扩展的检索式补救方案；因此尚不清楚只增加外部已解案例、而不重新训练模型，能否稳定改善复杂组合建模。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有RAG理论表明，外部检索能够补充语言模型的参数化知识，选择性注入上下文也可能优于无条件注入；但在自然语言到优化或约束模型的转换任务上，仍缺少基于系统化、格式统一且经过运行验证的合成问题库，并跨多个公开基准与直接LLM基线进行对照的实证研究。尤其需要验证一个关键前提：自然语言描述在嵌入空间中的语义相似性，是否足以指示底层变量、目标和约束结构的相似性。

</div>
<div markdown="1"><span>核心问题</span>

在固定使用Qwen 3 30B Instruct的条件下，将500个生成并验证的优化问题组织为外部向量知识库，再检索和筛选语义相似的已解案例作为上下文，是否能相对于直接LLM生成，在NL4OPT、MAMO Easy和MAMO Complex等公开基准上提高优化与约束模型的生成准确率？

</div>
<div markdown="1"><span>作者直觉</span>

许多业务故事虽然使用不同的人物、行业和对象名称，但背后可能共享同一种数学骨架，例如容量限制、指派关系或成本最小化。若先找到一份语义和结构都接近的已解案例，模型便可参照其中变量、目标、约束及求解代码的组织方式，而不必完全依赖记忆从头构造；语义网关进一步避免把不够相似的案例强行加入提示，从而减少错误示例对生成过程的干扰。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法不是对基础语言模型进行参数微调，而是先构造一个可检索的“已解题库”，再在推理时把与新问题结构相近的历史问题及求解代码作为上下文交给模型。题库由 $500$ 个 Text2Zinc 自然语言描述出发：GPT-5/ChatGPT 5.0 先为每个种子生成职业角色，再生成严格 JSON 优化模型，最后生成带小型数值实例的 Python 求解脚本；清洗后的问题文本被编码为向量并存入 Chroma，元数据则链接 JSON 文件和对应代码。需要谨慎理解论文所称的“验证”：后文明确指出脚本只通过编译或执行检查，这能排除部分语法与依赖错误，却不能证明模型约束正确、实例可行或所得解全局最优。
推理时，系统用与建库相同的嵌入模型编码新查询，以余弦相似度检索候选示例，并通过语义网关决定是否注入上下文：高相似候选直接采用，低相似候选舍弃，中间区间交给轻量 LLM 判断其对建模结构是否有用。通过网关的示例连同原始查询和输出约束被送入 LangChain agent，再由 Qwen 3 30B Instruct 生成完整 JSON 形式化描述与 Python 求解器代码。直观地说，该系统让模型先查阅几道可能同型的已解例题，但在抄用前设置一道过滤关，避免仅主题相近、数学结构不同的例题误导建模。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 合成问题—解答语料构造

对每个种子依次调用 GPT-5/ChatGPT 5.0：生成与场景匹配的职业角色，依据固定模式生成可由 `json.loads()` 解析的优化问题 JSON，再选择适当的优化或约束编程库生成包含变量、目标、约束、小型数值实例和结果打印逻辑的 Python 脚本。种子仅作为语义起点，生成内容被设计为受其启发的新问题，而非直接复用 Text2Zinc 的原解答。

<div class="method-step__io" markdown="1">

**输入**：从 Text2Zinc 抽取的 $500$ 个自然语言优化问题描述。<br>
**输出**：$500$ 个结构化优化问题及其关联的 Python 求解脚本。

</div>

**直观理解**：这一步把简短题意扩写成“业务背景、数学模型说明、可运行参考程序”三者配套的例题。职业角色用于增加现实语境和问题多样性，但也可能把生成模型自身的表达偏好带入整个题库。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 清洗、检查与向量索引

系统对 JSON 做 Unicode 规范化，并把脚本中的数值实例稳定为确定性实例；随后执行编译或运行检查，再用面向语义相似性的 Transformer 嵌入模型编码完整问题描述，将向量写入 Chroma，并以元数据链接原始 JSON 与代码文件。

<div class="method-step__io" markdown="1">

**输入**：合成的 JSON 文件和 Python 求解脚本。<br>
**输出**：固定的 Chroma 向量数据库，其中每条问题向量都可追溯到一个结构化问题和一个求解脚本。

</div>

**直观理解**：向量索引把题意转换成可比较的数字坐标，使措辞不同但含义相近的问题仍可能被找到。这里的代码检查主要说明脚本能够执行，不能替代对目标、约束、可行性和最优性的数学验证。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选检索与语义网关过滤

系统用建库时相同的嵌入模型编码查询，以余弦相似度进行最近邻搜索；实验流程称检索 top-$3$ 候选，并逐一应用三段式网关：分数至少为 $0.88$ 时接受，至多为 $0.70$ 时拒绝，中间区间由轻量 LLM 输出 `ACCEPT` 或 `REJECT`。

<div class="method-step__io" markdown="1">

**输入**：一个未见过的自然语言优化查询，以及固定的 Chroma 题库。<br>
**输出**：最多 $3$ 个获准进入生成提示的参考问题—解答示例；若全部被拒绝，则检索字段为空并退化为基线推理。

</div>

**直观理解**：主题相似不等于数学结构相同，例如两个问题都谈运输，却可能分别是路径规划和连续流量分配。网关的作用是判断检索结果是否真的能提供变量、约束或目标形式上的参考，而不是见到相似关键词就强行加入。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### Agent 组织提示并生成模型

LangChain agent 将获准示例的问题、解答摘要与用户查询组织成结构化提示，约束模型先分析优化形式，再生成正式模型和完整求解代码；Qwen 3 30B Instruct 最终输出 JSON 形式化描述及 Python solver 脚本。网关仅控制检索字段是否填充，不改变 agent 图结构，因此拒绝上下文时可直接回落到简单 agent 基线。

<div class="method-step__io" markdown="1">

**输入**：原始查询、通过网关的参考示例，以及 JSON 和 Python 输出格式指令。<br>
**输出**：针对新查询生成的优化问题 JSON、可执行 Python 求解器代码，以及运行后用于评价的预测目标值。

</div>

**直观理解**：参考例题向模型展示“类似问题通常怎样定义变量、写容量或指派约束、构造目标函数”，agent 则负责把这些参考材料按固定步骤交给模型。最终仍由语言模型完成迁移和改写，所以检索正确并不自动保证新代码正确。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 语义网关三段式接受规则

$$
g(q,r)=\begin{cases}\mathrm{ACCEPT}, & s(q,r)\ge 0.88,\\ C(q,r), & 0.70<s(q,r)<0.88,\\ \mathrm{REJECT}, & s(q,r)\le 0.70,\end{cases}
$$

**符号说明**

- $q$：当前自然语言优化查询。
- $r$：从向量数据库检索到的候选问题—解答示例。
- $s(q,r)$：查询与候选嵌入向量之间的余弦相似度分数。
- $C(q,r)$：轻量 LLM 分类器对候选结构用途作出的二元 `ACCEPT` 或 `REJECT` 决策。
- $g(q,r)$：语义网关的最终接受或拒绝结果。

<div class="equation-explanation" markdown="1">

**直观理解**：该规则把明显相关和明显不相关的候选快速分流，只对边界样本增加一次模型判断。它降低无关示例污染提示的风险，但阈值来自经验选择，并非通过本文完整消融或理论推导得到。<br>
**原文位置**：第 6.8 节 Semantic Gateway for Retrieval Filtering；第 6.9 节步骤 5

</div>

</div>

<div class="equation-block" markdown="1">

#### 目标值正确性判据

$$
\left|\mathrm{pred}-\mathrm{GT}\right|<\mathrm{ABS\_TOL},\qquad \mathrm{ABS\_TOL}=\begin{cases}5.0,&\text{Simple Agent Baseline},\\10^{-3},&\text{RAG-Enhanced}.\end{cases}
$$

**符号说明**

- $\mathrm{pred}$：生成的求解脚本运行后得到的预测目标函数值。
- $\mathrm{GT}$：基准数据提供的真实目标函数值。
- $\mathrm{ABS\_TOL}$：判定预测是否足够接近真值的绝对误差容限。

<div class="equation-explanation" markdown="1">

**直观理解**：只有预测目标值与真值的差小于容差时，实例才计为正确。两种条件采用不同容差，而且 RAG 的 $10^{-3}$ 比基线的 $5.0$ 严格得多；这不是同一判定尺度，虽然不会显然偏袒 RAG，但会使准确率差异混合了推理方法与评价阈值的影响。<br>
**原文位置**：第 6.2 节 Variables and Measurements；第 7.2 节 Evaluation Metrics

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：论文没有训练或微调 Qwen 3 30B Instruct、嵌入模型或生成数据所用的 GPT-5，也未给出新的可学习损失函数。这里的“优化”指系统需要生成的运筹优化模型，而不是对神经网络参数执行梯度优化；方法改进来自外部合成语料、向量检索、语义过滤和提示编排。系统最终以目标值判据衡量输出，但该判据是测试指标，不是训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 结构化合成语料生成器**

该模块采用角色引导的三级生成链：Text2Zinc 种子到职业角色、职业角色到固定模式的 JSON 问题、JSON 问题到 Python 求解器。JSON 明确要求给出题目、目标、决策变量、至少三项约束、参数、模型类型、复杂性和期望输出；代码提示允许模型根据问题选择 MILP、LP、MINLP、CP、OR-Tools 或 PuLP 等适用形式和工具。

> 直观理解：RAG 能提供什么知识，取决于题库中预先放入了什么。结构化生成使每条记录同时具备可检索题意和可模仿代码，但由同一个 LLM 系列生成全部语料可能造成风格偏差，也不能仅凭格式完整断言数学模型正确。

**2. Chroma 语义检索与三段式网关**

Chroma 保存问题描述的嵌入向量及其 JSON、代码链接，查询与候选间以余弦相似度排序。网关组合两个固定阈值与一个轻量 LLM 路由器：明确相似或明确不相似的候选直接处理，只把不确定区间交给分类器，从而控制检索上下文是否进入提示。

> 直观理解：检索器负责找“像的题”，网关负责判断“像得是否有用”。这一模块是方法区别于无条件 top-$k$ RAG 的关键，但阈值 $0.70$ 与 $0.88$ 是经验设定，原文也承认尚缺少系统消融来证明它们是最佳选择。

**3. LangChain 受控生成 Agent**

Agent 将原始问题、获准示例及输出规范编排为统一提示，并要求 Qwen 3 30B Instruct 先形成优化建模思路，再输出完整 JSON 和 Python 实现。基线与 RAG 条件保持基础模型、总体提示结构和评价任务不变，主要干预变量是是否提供通过网关的检索示例。

> 直观理解：Agent 不负责真正求解优化问题，而是约束语言模型的信息读取顺序和输出结构。它试图减少漏变量、凭空添加约束和代码语法错误，但论文没有分别消融 agent 编排、检索和网关，因此不能从现有结果精确分离三者各自贡献。

**训练与推理**

构建阶段先从 Text2Zinc 采样 $500$ 个种子描述，对每个种子生成职业角色、严格 JSON 优化模型和对应 Python 脚本；随后进行 Unicode 规范化、确定性数值实例整理和代码编译或执行检查。完整问题文本由 Transformer 句子嵌入模型编码，向量及其 JSON、代码元数据写入 Chroma；该数据库构建一次，并在所有实验中保持固定。论文没有报告以这些样本更新任何模型参数，因此这一阶段是知识库构造而非监督训练。
推理阶段对每个测试查询生成同源嵌入并检索候选。第 6.9 节和第 7.1 节明确采用 top-$3$，但第 6.6 节以单数描述“top retrieved neighbor”，因此复现时应以实验流程的 top-$3$ 为主，同时记录这一文本不一致。每个候选经过阈值网关，获准示例与查询共同进入 LangChain 提示；Qwen 3 30B Instruct 输出 JSON 和 Python 代码，执行脚本取得 $\text{pred}$，再依据绝对容差与 $\text{GT}$ 比较。基线走相同基础模型和简单 agent，但不注入检索上下文；当网关拒绝全部候选时，RAG 图中的检索字段为空，行为也回落到这一基线形式。

**复现信息**

公平解释和复现所需的关键信息包括：合成库规模为 $500$；向量存储为 Chroma；问题与查询必须由同一语义嵌入模型编码；近邻度量为余弦相似度；实验检索数为 top-$3$；网关边界为 $s\geq0.88$ 自动接受、$s\leq0.70$ 拒绝、中间区间由轻量 LLM 分类；生成模型为 Qwen 3 30B Instruct；每个 NL4OPT、MAMO Easy 和 MAMO Complex 基准各使用 $25$ 个测试查询，并在无检索和 RAG 两种条件下重复生成。原文未明确报告具体嵌入模型名称、轻量分类器型号、Qwen 的解码温度与随机种子、Chroma 索引参数、候选同时通过时的排列方式、失败代码的处置规则，以及每个查询是否多次采样，这些缺失会限制严格复现。
还需保留三项方法学限定。第一，论文一处称脚本为“verified”或“executable ground-truth”，但讨论部分承认 executability 仅由 compilation 判断，不能保证可行性、最优性或模型忠实度。第二，实验声称两条件保持评价指标不变，却分别使用基线容差 $5.0$ 与 RAG 容差 $10^{-3}$，这与“metric constant”的表述存在冲突。第三，全部合成数据来自单一生成模型系列，且每个基准只有 $25$ 个样本、推理只使用一个基础模型；因此现有设计主要检验该固定配置下加入检索上下文是否改善目标值命中率，尚不能独立证明 persona 生成、网关阈值或跨模型泛化的效果。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- NL4OPT：自然语言优化建模评测集，用于检验系统从问题描述生成形式化模型及可执行 Python 求解代码的能力。表 1 报告其准确率，但节选未明确说明该数据集的总规模、具体划分以及从中抽取了多少测试查询。
- MAMO Easy：MAMO 的较简单子集，用于考察 RAG 对相对容易的优化建模问题是否仍有增益。表 1 报告准确率；节选未明确说明总规模、划分和具体题型组成。
- MAMO Complex：MAMO 的复杂子集，用于检验语义检索在更复杂优化问题上的效果。表 1 报告准确率；节选未明确说明总规模、划分和复杂度定义。另有一个包含 500 个合成优化问题的向量库作为检索语料，但它不是测试集：每个实例包含 persona、JSON 问题规格和对应 Python 求解脚本。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**容差准确率**

把预测结果与真实答案之差满足 $|\mathrm{pred}-\mathrm{GT}|<\mathrm{ABS\_TOL}$ 的实例记为正确，再计算正确实例所占比例。其中 $\mathrm{pred}$ 是模型输出的数值结果，$\mathrm{GT}$ 是真实答案，$\mathrm{ABS\_TOL}$ 是允许的绝对误差。该指标主要衡量最终数值答案是否足够接近真实值，并不单独验证模型形式、约束语义或代码质量。 （越高越好，因为更高的比例表示更多测试实例的预测值落入规定误差范围。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### NL4OPT：Simple Agent Baseline 与 RAG-Enhanced

<div class="result-value" markdown="1">

准确率由 40.0% 提升至 72.0%，绝对增加 32 个百分点；按基线计算，相对提升 80%。

</div>

作者据此认为，检索相似的已解问题能够帮助模型更准确地完成 NL4OPT 优化建模任务。分析上，这是三个基准中最大的绝对增益，并且 RAG 使用了更严格的数值容差，因此结果方向支持检索上下文有效。不过，该结果只比较了完整基线与完整 RAG 流程，不能判断收益究竟来自语义检索、示例答案、semantic gateway，还是更长且结构化的提示；小样本和缺少重复实验也使统计稳定性无法判断。

<div class="result-source" markdown="1">

来源：表 1，第 7.3 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

NL4OPT 40.0% 72.0%

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### MAMO Easy：Simple Agent Baseline 与 RAG-Enhanced

<div class="result-value" markdown="1">

准确率由 40.0% 提升至 56.0%，绝对增加 16 个百分点，相对提升 40%。

</div>

作者将这一结果解释为 RAG 在较容易的 MAMO 问题上同样有效。其增幅小于 NL4OPT，说明检索收益可能随数据分布或问题结构而变化，但节选没有给出错误类型、题目级结果或显著性检验，因而不能断言数据集难度是增益差异的原因，也不能证明模型生成的每个约束都在语义上正确。

<div class="result-source" markdown="1">

来源：表 1，第 7.3 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MAMO Easy 40.0% 56.0%

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### MAMO Complex：Simple Agent Baseline 与 RAG-Enhanced

<div class="result-value" markdown="1">

准确率由 32.0% 提升至 56.0%，绝对增加 24 个百分点，相对提升 75%。

</div>

作者据此主张，检索增强对复杂组合优化问题也有明显帮助。分析上，RAG 将复杂子集的准确率提高到与 MAMO Easy 相同的 56.0%，表明相似示例可能为复杂问题提供了有用的建模骨架；但这并不证明系统已经稳定解决复杂优化建模，因为仍有 44.0% 的实例未达到正确标准，而且没有按约束类型或失败原因细分结果。

<div class="result-source" markdown="1">

来源：表 1，第 7.3 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MAMO Complex 32.0% 56.0%

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Simple Agent Baseline：Qwen 3 30B Instruct 直接根据测试查询生成形式化问题描述和 Python 求解代码，不访问检索库。它控制了底层模型和智能体框架，使与 RAG-Enhanced 的差别主要集中在是否提供检索示例。
- RAG-Enhanced：论文的目标系统，而非外部基线。它从 500 个合成优化问题构成的向量数据库中检索语义最相似的前 3 个示例，经 semantic gateway 后作为上下文交给同一模型。与 Simple Agent Baseline 的比较用于估计整个检索增强流程的综合作用。
- 相关工作方法：第 7.4 节称表 2 将本方法与 OR-LLM-Agent 等既有结果比较，但所给节选未包含完整方法名称、配置和数值，因此不能据此进行可靠的逐项复述或公平性判断。

**实验想回答的问题**

- 在相同的 Qwen 3 30B Instruct 模型下，引入基于合成优化问题库的检索增强生成（RAG），是否比不使用检索的简单智能体更准确地求解自然语言优化问题？
- 这种改进能否同时出现在 NL4OPT、MAMO Easy 和 MAMO Complex 三种不同难度或来源的测试集上，从而表明收益并非局限于单一基准？

**实验实现**

实验使用 Qwen 3 30B Instruct，并称两种条件采用一致的模型参数。论文随机抽取了 25 个测试查询，这些查询来自合成检索语料未覆盖的领域；每个查询要求系统同时生成形式化优化问题和可执行 Python 求解代码。基线直接生成，RAG 条件则从 500 个合成问题的 Chroma 向量库中取语义最相近的前 3 个示例作为上下文。节选没有明确说明 25 个查询是每个评测集各 25 个，还是三个评测集合计 25 个，也没有报告随机种子、重复运行次数、解码参数、求解器执行流程或置信区间。尤其需要注意，评价阈值并不一致：基线采用 $\mathrm{ABS\_TOL}=5.0$，RAG 采用 $\mathrm{ABS\_TOL}=10^{-3}$。RAG 的判定明显更严格，因此表中提升并非由更宽松阈值造成；但不一致阈值仍破坏了标准化的同条件比较，应补充统一阈值结果。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work improves LLM generation of formal optimization and constraint models through retrieval of validated synthetic examples.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`2f9016a5d487901cd5dcd4da0ef2777871156f3655a4b5e46bd678331789fc16`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
