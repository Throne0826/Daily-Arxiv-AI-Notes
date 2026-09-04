---
title: "[论文解读] Reflect-SQL: A Self-Reflection Based Framework for Text-to-SQL"
description: "[arXiv 2609.02944][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2609.02944"
announcement_date: "2026-09-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:40:22.236950+00:00"
source_sha256: "9ce3b936a0c7510ccb74242b484f45a798f89516f2a667e85a1249a0ed214e95"
tags:
  - "LLM Reasoning"
  - "LLM Agent"
  - "LLM 评测"
  - "Text-to-SQL"
  - "Self-reflection"
  - "Retrieval-Augmented Generation"
  - "Knowledge Base"
  - "Large Language Models"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.02944</p>

# Reflect-SQL: A Self-Reflection Based Framework for Text-to-SQL

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Anupreksha Jain, Manish Shrivastava</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: International Institute of Information Technology Hyderabad, India</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.02944v1) · [PDF 下载](https://arxiv.org/pdf/2609.02944v1) · **关键词** Text-to-SQL, Self-reflection, Retrieval-Augmented Generation, Knowledge Base, Large Language Models<br>


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

Text-to-SQL旨在将自然语言问题转换为可执行的SQL查询，使用户能够通过日常语言访问关系数据库。本文关注企业场景：数据库规模较大、表和列名称可能晦涩且缺少文档，用户问题又可能含义模糊，因此系统不仅要生成语法正确的SQL，还要选择与问题相关的表和列，并保证查询逻辑确实符合用户意图。Reflect-SQL将知识库、检索增强生成和大语言模型自反思结合起来，针对模式理解、相关信息检索和SQL校验三个环节进行迭代改进。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**Text-to-SQL**

Text-to-SQL是把用户的自然语言问题转换成SQL查询的任务。输入通常包括自然语言问题和数据库模式，输出是能够在该数据库上执行的SQL语句。

</div>
<div class="concept-item" markdown="1">

**数据库模式与模式链接**

数据库模式描述数据库中的表、列以及它们之间的关系；例如表名和列名共同决定SQL可以访问哪些数据。模式链接是把用户问题中的实体或意图对应到相关表和列的过程，模式晦涩或缺少说明时，这一步尤其困难。

</div>
<div class="concept-item" markdown="1">

**检索增强生成与自反思**

检索增强生成先从外部知识库检索与问题相关的信息，再把这些信息提供给生成模型，以减少仅凭模型记忆生成错误答案的风险。自反思则让模型对自己的输出进行评分、发现问题并迭代修改，而不是只进行一次生成。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定自然语言问题$q$、关系数据库及其模式$S$，系统需要先确定与$q$相关的表、列和关系，再生成SQL查询$y$，使$y$能够在目标数据库上执行，并且其结果回答$q$所表达的问题。本文假设数据库可能具有大规模、晦涩命名和不完整文档，且不依赖单次生成或仅检查SQL语法；系统还需要通过知识库和反馈循环逐步改善模式理解、检索上下文与SQL的语义正确性。最终评价重点是执行结果是否正确，而不仅是SQL字符串是否与参考答案完全一致。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$q$**

用户提出的自然语言问题。

</div>
<div class="notation-item" markdown="1">

**$S$**

目标数据库的模式信息，包括表、列及其关系。

</div>
<div class="notation-item" markdown="1">

**$y$**

系统生成的SQL查询。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{KB}$**

动态知识库，用于保存和补充模式说明、业务知识及相关数据库信息。

</div>

</div>

**直接相关的工作**

- **知识库构建方法**: 已有研究通过对齐元数据与业务词汇、增强列描述或注入领域知识来改善Text-to-SQL，但通常把知识库视为一次性建立的静态资源。Reflect-SQL的区别在于，根据成功执行的查询持续丰富知识库，使其能够逐步适应真实场景中的歧义和隐含模式信息。
- **迭代式检索增强生成与现代Text-to-SQL方法**: 既有检索增强生成方法会通过迭代改写查询来提高上下文质量，现代Text-to-SQL方法如DIN-SQL和SQLPrompt则利用少样本示例与链式思考提升SQL生成能力。Reflect-SQL将这类思想扩展到数据库模式的分层检索，并进一步加入SQL合成反馈循环和最终蕴含检查，以同时处理检索不足、SQL逻辑错误以及查询结果不符合用户意图的问题。

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

Reflect-SQL 是一个面向复杂数据库的多阶段推理框架，输入为用户自然语言问题与数据库资源，输出为经执行和意图一致性验证的 SQL 结果。其流程不是让大语言模型一次性生成 SQL，而是依次完成知识库构建、分层模式检索、SQL 生成与纠错、结果蕴含验证；每个阶段都设置基于 LLM-as-a-judge 的评分或反馈环，从而分别控制“找对模式元素”“写对 SQL”和“答案符合原始问题”这三类风险。通过验证的查询—结果对还会反向补充知识库，使含义晦涩的表名、列名和值编码逐步获得可检索的业务解释。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 知识库构建与向量化

系统综合这些信息，为表、列及表间关系生成描述，再用句子嵌入模型将描述编码为稠密向量。向量库采用两层结构：全局集合保存表描述，每张表对应一个局部集合保存其列描述。

<div class="method-step__io" markdown="1">

**输入**：数据库模式、样例数据值，以及 BIRD 训练集中的样例问题和外部证据；企业场景还可输入业务文档与术语表。<br>
**输出**：包含表、列、关系、样例值、语义描述及其向量表示的结构化知识库。

</div>

**直观理解**：数据库原始名称可能像缩写或代码，模型难以直接理解；该步骤相当于先为数据库编写一份带业务释义、且能够按语义搜索的目录。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 迭代式分层模式检索

系统先嵌入 $Q$，以余弦相似度检索前 $k$ 个相关表，再加入知识库中与这些表存在关系的表，以保留潜在连接路径；随后在各候选表的局部集合中检索相关列。LLM-as-a-judge 分别评估语义相关性 $R$ 和模式完整性 $C$，并计算 $Score_r=\alpha R+(1-\alpha)C$；若 $Score_r<\theta_r$，模型改写问题为更明确的 $Q'$，同时扩大表和列的检索范围，直至越过阈值或达到最大迭代次数。

<div class="method-step__io" markdown="1">

**输入**：用户问题 $Q$ 与已构建的知识库。<br>
**输出**：与问题相关且尽量完整的表、列、关系、描述和样例数据上下文。

</div>

**直观理解**：这一步先找“可能相关的表”，再在这些表里找“真正需要的列”，并把连接所需的中间表一起带上。如果裁判模型认为材料不够，系统会一边把用户问题改写得更具体，一边扩大搜索范围，而不是立即用残缺模式生成 SQL。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### SQL 生成、语法纠错与语义修正

LLM 首先生成候选 SQL，数据库引擎随后执行语法检查；发生错误时，系统把原 SQL、数据库错误消息和模式上下文反馈给 LLM 进行修复。语法通过后，裁判模型从列名一致性 $C$、粒度与聚合 $G$、连接与关系一致性 $J$、查询逻辑对齐 $Q$ 四个维度计算语义分数 $S$；若 $S<\theta_s$，则根据诊断意见迭代重写 SQL。

<div class="method-step__io" markdown="1">

**输入**：原始用户问题，以及检索得到的表、列、关系、描述和样例值。<br>
**输出**：能够被数据库引擎接受、且语义评分达到阈值的候选 SQL。

</div>

**直观理解**：“能运行”只排除了拼写或语法错误，并不代表查询正确；因此系统还检查是否用了正确的列、聚合层级、连接关系和过滤逻辑，再把具体问题交给模型修改。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行结果蕴含验证与全局反馈

数据库执行 SQL 后，LLM-as-a-judge 从模式一致性 $E_{\text{schema}}$ 和数据一致性 $E_{\text{data}}$ 两方面计算 $E(Q,R)$。若 $E(Q,R)\geq\theta_e$，结果返回用户并触发知识库更新；否则，系统依据缺列、过滤错误等失败原因重新启动检索与生成流程。

<div class="method-step__io" markdown="1">

**输入**：通过语法和语义验证的 SQL、执行结果集 $R$、原始问题 $Q$。<br>
**输出**：通过意图一致性检查的查询结果；或者用于下一轮端到端重试的失败反馈。

</div>

**直观理解**：最后一道检查不再只看 SQL 文本，而是问“查出来的内容是否真的回答了用户的问题”。只有这一判断通过，系统才交付结果并把此次成功经验写回知识库，避免错误案例污染后续检索。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### SQL 语义验证加权分数

$$
S=w_{c}\cdot C+w_{g}\cdot G+w_{j}\cdot J+w_{q}\cdot Q
$$

**符号说明**

- $S$：候选 SQL 的综合语义验证分数。
- $C$：列名一致性得分，用于判断查询引用的列是否与模式及问题一致。
- $G$：粒度与聚合得分，用于判断分组、计数、求和等操作是否符合问题要求。
- $J$：连接与关系一致性得分，用于判断表连接及连接路径是否合理。
- $Q$：查询逻辑对齐得分；此处表示语义验证维度，而不是前文表示用户问题的同名符号。
- $w_c,w_g,w_j,w_q$：四个语义维度的预定义权重。

<div class="equation-explanation" markdown="1">

**直观理解**：裁判模型不是用单一的“看起来正确”判断 SQL，而是把四类常见逻辑错误分别评分，再按预设权重合成为 $S$。当 $S$ 低于 $\theta_s$ 时，各维度的诊断信息会指导 LLM 定向修改查询。<br>
**原文位置**：第 5.2 节，公式（3）

</div>

</div>

<div class="equation-block" markdown="1">

#### 执行结果蕴含分数

$$
E(Q,R)=\beta\cdot E_{\text{schema}}+(1-\beta)\cdot E_{\text{data}},\quad \beta\in[0,1]
$$

**符号说明**

- $E(Q,R)$：执行结果集对原始用户问题的综合蕴含分数。
- $Q$：用户的原始自然语言问题。
- $R$：候选 SQL 在数据库中执行后得到的结果集。
- $E_{\text{schema}}$：模式一致性得分，衡量结果涉及的数据库结构是否与问题要求相符。
- $E_{\text{data}}$：数据一致性得分，衡量返回的数据内容是否回答了问题。
- $\beta$：模式一致性与数据一致性之间的权衡系数，取值范围为零到一。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把“查了正确的结构”和“返回了正确的数据”合并为最终验收信号。只有当 $E(Q,R)\geq\theta_e$ 时结果才会交付并用于更新知识库，否则系统携带失败原因回到前面的检索与生成环节。<br>
**原文位置**：第 6.1 节，公式（4）；判定规则见第 6.2 节

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。原文描述的是由现成大语言模型、句子嵌入模型、向量数据库和数据库执行器组成的推理时框架，没有给出参数训练损失、梯度优化过程或针对 Reflect-SQL 的端到端模型训练目标。公式中的 $Score_r$、$S$ 与 $E(Q,R)$ 是推理阶段的门控和反馈信号，而不是用于反向传播的训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 可持续精化的语义知识库**

知识库把数据库模式、样例值、训练样例、外部证据及企业术语组织为表级和列级描述，并通过全局表集合与逐表列集合支持分层向量检索。成功 SQL 必须通过语法、语义和最终蕴含验证，且 $E(Q,R)$ 超过阈值 $\theta_e$，其查询—结果信息才可用于精化列描述，例如把代码值补充为具体业务状态。

> 直观理解：该模块既解决大模式无法完整塞进模型上下文的问题，也解决名称晦涩的问题。严格的条件更新相当于只让“验收合格的经验”进入说明书，从而降低错误解释被长期保存的风险。

**2. 反馈驱动的分层检索器**

检索器采用“表后列”的层级路径：先根据问题向量与表描述向量的余弦相似度选取前 $k$ 个表，再沿知识库关系扩展关联表，最后在每张候选表内部检索列。裁判模型联合评估相关性与完整性；低于 $\theta_r$ 时，同时执行问题改写与候选范围扩张。

> 直观理解：只按关键词找表容易漏掉连接表，只扩大候选数量又会引入噪声；该设计同时改善问题表达和搜索覆盖面，在精确性与完整性之间做动态折中。

**3. 多层 SQL 验证器**

验证器依次检查数据库语法、SQL 语义和执行结果蕴含关系。前两层定位 SQL 是否可执行以及列、聚合、连接和逻辑是否合理，最后一层比较原始问题 $Q$ 与结果集 $R$ 是否一致；各层反馈分别驱动局部 SQL 修复或整个流程重启。

> 直观理解：这相当于三级验收：先检查程序能否运行，再检查程序做的事情是否合理，最后检查实际答案是否满足用户需求。分层反馈使系统能够针对错误发生的位置修正，而不是每次都盲目重新生成。

**训练与推理**

知识库准备阶段先汇总数据库模式、样例值、样例问题、外部证据及可用的业务资料，生成表、列和关系描述，并建立表级全局向量索引与列级局部向量索引。在线推理时，系统以用户问题 $Q$ 检索候选表，补入关系相连的表后再检索列；若相关性和完整性组合分数不足，则将问题改写为 $Q'$ 并扩大检索范围。获得足够模式上下文后，LLM 生成 SQL，数据库错误消息驱动语法修复，四维语义评分驱动逻辑修正。SQL 执行产生结果集 $R$ 后，系统计算最终蕴含分数；通过阈值则返回结果并精化知识库，未通过则携带诊断反馈重新触发完整流程。原文仅说明各循环在达到阈值或最大迭代次数时终止，没有在所给章节中报告具体迭代上限。

**复现信息**

公平理解该方法所需的关键实现信息包括：知识库以表级全局集合和逐表列级局部集合组织；表检索使用问题与表描述嵌入的余弦相似度并选择前 $k$ 项；关系扩展用于保留 SQL 连接路径；数据库引擎同时承担语法检查和查询执行；LLM-as-a-judge 用于检索相关性/完整性、四维 SQL 语义和最终结果蕴含评分。实验结果行将系统标为 Reflect-SQL + Claude 4.5 Sonnet，但所给方法章节未明确报告句子嵌入模型的具体名称、$k$、$\alpha$、$\beta$、各语义权重、阈值 $\theta_r$、$\theta_s$、$\theta_e$、提示词全文及各循环的最大次数；这些缺失参数会影响严格复现，应结合论文附录和代码进一步核查。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- BIRD benchmark：由多种关系数据库组成，用于模拟真实世界中大规模、复杂模式下的 Text-to-SQL。主要模型实验在 BIRD 数据集上进行，与现有方法的比较明确使用 BIRD development set；原文节选未报告样本规模、数据库数量及更细的划分信息。该数据集在实验中充当难以公开获得的企业数据库的代理，而不是实际企业部署数据。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**执行准确率（Execution Accuracy, EX）**

将生成的 SQL 与参考 SQL 分别执行，并依据执行结果是否一致判断正确性；表中分别汇报 Simple、Moderate、Challenging 和 Overall。它比仅检查 SQL 字符串是否相同更适合处理语法不同但结果等价的查询，但结果一致也不必然证明 SQL 在所有数据库状态下都具有完全相同的逻辑。 （越高越好，因为更高比例表示生成 SQL 在该基准上得到正确执行结果。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Claude-sonnet-4.5 启用与关闭完整反思框架

<div class="result-value" markdown="1">

启用反思时，Simple、Moderate、Challenging 和 Overall 执行准确率分别为 88.97%、50.65%、32.41% 和 72.03%；关闭反思时分别为 81.18%、45.25%、24.13% 和 64.92%。总体绝对提升为 7.11 个百分点，三个难度层级均有提高。

</div>

这是同一底层模型下最直接的受控比较，说明收益不只是换用更强模型造成的；其中 Challenging 提升 8.28 个百分点，表明反复检索、校验和修正对复杂问题可能更有帮助。不过 Challenging 的最终准确率仍只有 32.41%，而且节选没有显著性检验，因此不能据此断言复杂 Text-to-SQL 已被解决或增益必然能推广到企业私有数据库。

<div class="result-source" markdown="1">

来源：Table 3, Section 9.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Claude-sonnet-4.5 (with reflection) 88.97 50.65 32.41 72.03
Claude-sonnet-4.5 (w/o reflection) 81.18 45.25 24.13 64.92

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨 OpenAI、DeepSeek API 和本地开源模型检验反思框架的稳定性

<div class="result-value" markdown="1">

总体执行准确率在 o1-preview 上由 55.66% 升至 62.19%，在 deepseek-reasoner 上由 51.88% 升至 60.10%，在本地 DeepSeek-Coder-V2-Lite 上由 22.64% 升至 35.02%，对应绝对提升 6.53、8.22 和 12.38 个百分点。

</div>

反思流程在三类不同模型设置中都优于各自的无反思版本，支持其增益具有一定模型无关性，而非只适用于 Claude。开源模型的相对改善较明显，但绝对准确率仍远低于闭源 API 模型；该结果也没有分离额外调用次数和计算预算的影响，因此不能证明反思方案在等成本条件下仍然最优。

<div class="result-source" markdown="1">

来源：Table 3, Section 9.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

o1-preview (with reflection) 75.89 48.49 18.62 62.19
o1-preview (w/o reflection) 69.35 40.54 15.86 55.66
deepseek-reasoner (with reflection) 73.62 46.55 17.24 60.10
deepseek-reasoner (w/o reflection) 62.90 40.54 12.41 51.88
DeepSeek-Coder-V2-Lite… (with reflection) 43.55 21.62 3.44 35.02
DeepSeek-Coder-V2-Lite... (w/o reflection) 30.65 13.51 0.0 22.64

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### BIRD development set 上与现有 Text-to-SQL 方法比较

<div class="result-value" markdown="1">

作者报告 Reflect-SQL 的执行准确率为 72.03%，高于 DIN-SQL 的 50.72%、DAIL-SQL 的 57.41% 和 MAC-SQL 的 59.59%，并称其与 CHASE-SQL 表现可比。

</div>

相对于所列方法，Reflect-SQL 至少提高 12.44 个百分点，说明其完整系统在该开发集上具有较强竞争力。作者将其称为当前最佳水平，但节选没有提供 CHASE-SQL 的具体数值，也未说明各系统是否使用相同底层模型、外部知识、推理预算和提示资源，因此该排名不能单独归因于反思机制。

<div class="result-source" markdown="1">

来源：Section 9.4 and Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Reflect-SQL achieves a state-of-the-art execution accuracy of 72.03%, marking a significant improvement over DIN-SQL [13] (50.72%), DAIL-SQL (57.41%) and MAC-SQL (59.59%).

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

- 无反思版本：对 Claude-sonnet-4.5、o1-preview、deepseek-reasoner 和本地 DeepSeek-Coder-V2-Lite 分别关闭 Reflect-SQL，用于控制底层模型能力并直接测量反思流程的增益。
- DIN-SQL：BIRD development set 上的已有 Text-to-SQL 方法，报告执行准确率为 50.72%，用于衡量 Reflect-SQL 相对既有结构化推理方案的提升。
- DAIL-SQL 与 MAC-SQL：BIRD development set 上的代表性强基线，报告执行准确率分别为 57.41% 和 59.59%，用于判断结果是否超过较有竞争力的现有系统。
- CHASE-SQL：较新的 Text-to-SQL 架构。作者称 Reflect-SQL 与其表现可比，但所给节选没有列出 CHASE-SQL 的具体分数，因此只能支持定性比较。

**实验想回答的问题**

- 多阶段反思框架能否在不同大语言模型家族上稳定提高 Text-to-SQL 的执行准确率，尤其是在中等和高难度查询上？
- SQL 生成自反思、迭代式模式检索和蕴含检查分别贡献了多少性能；完整 Reflect-SQL 与现有 BIRD 方法相比处于什么水平？

**实验实现**

主实验分别使用 Claude、OpenAI、DeepSeek API 模型以及本地开源 DeepSeek-Coder-V2-Lite，并对每个模型比较启用和关闭反思框架的执行准确率。消融实验以 deepseek-chat 为基础模型，逐一移除 SQL 生成自反思、迭代检索或蕴含检查。框架中的评分任务采用结构化少样本提示，包含详细指令、评分规则和示例，以减轻 LLM-as-a-judge 的偏差。原文节选未明确报告提示重复次数、随机种子、解码参数、统计显著性检验、推理成本或人工评价者数量及一致性。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 以 deepseek-chat 为基础模型，移除 SQL 生成阶段的自反思 | 完整模型的 Overall 执行准确率为 55.80%，移除 SQL 生成自反思后降至 50.58%，下降 5.22 个百分点；Simple、Moderate、Challenging 分别由 68.64%、43.10%、14.48% 降至 62.91%、37.93%、12.41%。这是所报告单模块消融中最大的总体降幅。 | 该消融隔离了生成 SQL 后进行检查和修正的作用。下降说明一次性生成更容易保留语法或逻辑错误，自反思是完整框架中最关键的单项组件。不过各模块可能相互依赖，逐项删除不能证明 5.22 个百分点完全是独立、可加的因果贡献。 | Table 6, Section 10<br><span class="experiment-evidence">Full Model (Self-Reflect) 68.64 43.10 14.48 55.80
w/o Self-Reflection in SQL Generation 62.91 37.93 12.41 50.58</span> |
| 以 deepseek-chat 为基础模型，分别移除迭代检索或蕴含检查 | 移除迭代检索后，Overall 从 55.80% 降至 53.58%，Challenging 从 14.48% 降至 10.34%；移除蕴含检查后，Overall 降至 52.47%，即总体下降 3.33 个百分点。 | 迭代检索负责反复改写或细化检索目标，以找到与问题相关的表和列；其在 Challenging 上下降 4.14 个百分点，提示复杂模式链接更依赖反馈检索。蕴含检查则判断 SQL 执行结果是否真正满足用户意图；移除后总体下降更大，说明仅保证可执行或表面语义合理还不够。由于没有同时移除两个模块的组合实验，无法判断二者是否存在协同或功能重叠。 | Table 6, Section 10<br><span class="experiment-evidence">Full Model (Self-Reflect) 68.64 43.10 14.48 55.80
w/o Iterative Retrieval 67.02 40.30 10.34 53.58
w/o Entailment Check 64.10 41.59 13.10 52.47</span> |

**定性案例**

- Table 4 展示了蕴含反馈修正逻辑错误的例子：用户要求列出 continuation schools 中最低的三个 eligible free rates；初始 SQL 直接计算计数与注册人数之比，蕴含检查仅给出 2/5，并指出除零或空值导致结果为 None。修正版增加了正注册人数过滤，并将计数转换为实数后再相除。该案例说明蕴含检查关注“执行结果是否真正回答问题”，能够发现单纯语法检查可能漏掉的数值语义错误；但单个示例不能量化此类修正的总体成功率。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It proposes an iterative self-reflection framework that uses retrieval, validation, correction, and feedback loops for reliable Text-to-SQL generation.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`9ce3b936a0c7510ccb74242b484f45a798f89516f2a667e85a1249a0ed214e95`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
