---
title: "[论文解读] Improving LLM Interpretability with User-Centric Chain-of-Thought Reasoning"
description: "[arXiv 2608.26166][LLM 机制与可解释性] 本文提出以自包含、可验证步骤组织大语言模型推理轨迹，并通过交互界面支持逐步检查与纠错，目标是在不降低数学推理质量的同时提升解释的用户可用性。"
arxiv_id: "2608.26166"
announcement_date: "2026-08-28"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:40:10.095908+00:00"
source_sha256: "821eca3d48503ada28620273ac9ba02e4921c8197e6ee9763b7c13a642dac98f"
tags:
  - "LLM 机制与可解释性"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "人机协作"
  - "可解释人工智能"
  - "思维链推理"
  - "用户中心设计"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2608.26166</p>

# Improving LLM Interpretability with User-Centric Chain-of-Thought Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Philipp Schröppel</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> University of Ulm</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26166v1) · [PDF 下载](https://arxiv.org/pdf/2608.26166v1) · **关键词** 大语言模型, 人机协作, 可解释人工智能, 思维链推理, 用户中心设计<br>


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

本文提出以自包含、可验证步骤组织大语言模型推理轨迹，并通过交互界面支持逐步检查与纠错，目标是在不降低数学推理质量的同时提升解释的用户可用性。

**不用术语来说**：大语言模型即使给出完整的解题过程，也可能在某一步使用错误事实、遗漏条件或作出不成立的推断；普通用户面对一长段连续文字，往往难以定位错误及准确反馈。在医疗、金融等高风险场景中，如果人类不能方便地检查和修正模型的中间推理，仅仅展示“思考过程”并不足以形成可靠的人机协作。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出用户中心的思维链表示：把推理拆成自包含且可独立验证的步骤，并使用类似 XML 的标签编码步骤内容与元数据，使界面能够提供交叉引用和步骤级反馈。
- 将结构化轨迹生成、稳健解析与交互界面整合为完整实现，并在数学推理和用户研究中考察其是否兼顾任务表现与用户感知；该方案依靠提示而非任务专用微调，因此原则上可以接入不同的大语言模型。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型推理、人机协作与可解释人工智能的交叉领域。大语言模型可借助思维链提示把复杂任务分解为连续的中间步骤，并输出从问题到答案的推理轨迹；这些轨迹不仅可能改善多步推理，也为人类检查假设、计算和结论提供入口。然而，模型仍可能生成看似可信但事实错误的内容，且在缺少外部反馈时难以可靠地自我纠正。现实应用中的验证责任因而常由用户承担，尤其是在缺少自动验证工具的领域。本文关注的核心背景是：传统思维链通常以长段、非结构化文本呈现，容易增加工作记忆负担，不利于用户逐步核验和精确反馈；用户中心的可解释人工智能则要求解释适配用户需求与使用情境，并同时通过功能性评估和真实用户评估检验其有效性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**思维链推理（Chain-of-Thought, CoT）**

一种提示大语言模型显式生成中间推理步骤、再给出最终答案的方法，适用于需要多次计算、推断或知识操作的任务。本文把这些中间步骤同时视为可供用户检查的“推理轨迹”，而不只视为提高答案准确率的手段。

</div>
<div class="concept-item" markdown="1">

**可解释人工智能（Explainable AI, XAI）**

研究如何让人理解、评估并适当依赖人工智能输出的领域；解释可用于发现错误、校准信任和支持模型调试。本文采用用户中心立场，即解释是否有效取决于它能否满足具体用户在具体任务中的核验与纠错需求。

</div>
<div class="concept-item" markdown="1">

**上下文学习（In-context Learning）**

模型在不进行任务专用训练的情况下，根据提示中的任务说明和示例完成新问题。思维链提示通常在上下文中提供逐步推理示例，引导模型以类似方式分解待解决问题。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个需要多步推理的问题，以及用于规定输出形式的提示；论文主要在数学推理任务中研究该设置。系统调用任意无需任务专用微调的大语言模型，要求其生成由若干自包含、可独立核验的步骤组成的推理轨迹，并用类似 XML 的标签编码步骤内容及元数据；随后解析这些结构化输出，在交互式界面中呈现步骤、交叉引用和逐步反馈入口，最终输出推理过程与答案。基本假设是用户需要亲自判断模型推理是否可靠，而且结构清晰、可定位的步骤比连续长文本更便于检查假设、验证逻辑和提交针对性纠正；论文还要求这种可解释性改造不明显损害标准思维链的任务表现。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **标准思维链提示及其扩展方法**: 标准思维链通过展示逐步推理示例来改善算术、常识和符号推理；后续方法包括聚合多条推理路径的自洽性方法、探索分支的思维树方法，以及结合外部工具和迭代修正的智能体系统。本文不以探索更多推理路径为重点，而是重新组织单条推理轨迹，使其更适合人类逐步检查和纠错。
- **用户中心的可解释人工智能与分层评估框架**: 既有研究指出，解释未必能提高决策准确率或感知可信度，因此不能仅凭提供了解释就推断其有效。相关框架区分无用户参与、依赖代理指标的功能基础评估，由普通用户完成简化任务的人本基础评估，以及真实用户在实际场景中的应用基础评估；本文据此同时关注结构化推理的任务性能与用户感知的有用性、易用性。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型会生成看似可信但事实错误的内容，而且缺少外部反馈时自我纠错能力有限。专业领域有时可使用自动验证工具，但多数现实任务仍需要人类判断输出是否可靠；因此，系统必须让用户能够追踪结论来源、检查每一步逻辑，并把纠正意见准确地指向出错位置。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **标准思维链推理**：要求模型在最终答案之前输出连续的自然语言中间步骤，使用户能够看到答案形成的大致过程；既有研究主要将其作为提高多步推理表现的方法。
- **面向用户的可解释人工智能**：根据用户角色、任务和使用情境设计解释，强调解释不仅要存在，还应帮助用户理解、质疑和采取行动；该思路提示推理轨迹应围绕协作需求组织，而不能只服务于模型性能。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 标准推理轨迹通常是一段缺少显式结构的连续文本，容易占用过多工作记忆；用户难以逐项核查假设、逻辑和引用关系，也难以把反馈精确关联到某个推理步骤。
- 现有思维链研究更重视答案正确率等模型侧指标，对解释是否便于人类独立验证和纠错关注不足；已有“展示推理轨迹”的做法因而尚未解决解释的交互可用性问题。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

仍缺少一种可直接用于人机协作的推理轨迹机制：它需要把每一步组织为可单独理解和验证的单元，保留步骤间依赖关系并支持定点反馈，同时避免为了提高可解释性而明显损害原有任务表现。原文还指出，结构化解释能否进一步改善实际判断正确性和纠错行为并未得到肯定结果，这构成后续研究空间。

</div>
<div markdown="1"><span>核心问题</span>

能否通过结构化、可验证且可交互的用户中心思维链，使用户更容易评估和纠正大语言模型的推理，同时保持与标准思维链相当的数学任务表现？

</div>
<div markdown="1"><span>作者直觉</span>

如果把长篇推理改造成类似清单的独立步骤，并明确标记每一步的内容、依据和关联，用户就不必在整段文字中反复搜索上下文，而可以逐步确认“这一步是否成立”，再把异议直接附到具体步骤上。类似 XML 的标签还使程序能够稳定解析这些关系并构建交互界面，从而把被动阅读解释转变为可定位、可核验、可修正的协作过程。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把自由文本式思维链改造成面向用户核验的结构化推理轨迹。端到端流程为：使用含完整示例的少样本提示，引导大语言模型按一种类似 XML 的领域特定语言生成答案；解析器再从标签及属性中提取语义片段、推理步骤和依赖关系；最后，交互界面把这些结构显示为可独立检查的步骤，并允许用户针对错误步骤反馈，系统保留此前已确认的步骤并从纠错点继续生成。其目标不是改变模型内部推理架构，而是在尽量维持原有解题能力的同时，降低用户核查长篇推理时因信息组织不良产生的额外认知负担。
直观地说，普通思维链像一段连续草稿，用户必须自己找出事实、假设、计算和结论之间的联系；本文则把草稿整理成带标签、编号和引用关系的“可检查工作表”。每一步既是局部推理单元，也是可复用的检查点，因此用户发现中途错误时不必要求模型推倒重来。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 结构化提示与推理轨迹生成

提示要求大语言模型按照预定义答案模式逐步作答，并用类似 XML 的领域特定语言标记每个语义片段。模型生成的片段类型包括 Fact、Question、Goal、Premise、Partial 和 Final，标签属性还可记录片段标识及引用关系。

<div class="method-step__io" markdown="1">

**输入**：用户提出的复杂推理问题，以及包含示例问题和完整结构化解答的少样本提示。<br>
**输出**：同时包含实际推理内容与结构元信息的领域特定语言文本。

</div>

**直观理解**：这一步相当于先给模型一份规定栏目和填写示例的答题模板，使模型不再输出一整段难以拆分的草稿，而是把事实、目标、前提、中间结果和最终答案分别填写。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 容错解析与依赖图构建

系统使用正则模式提取片段的语义类型、键值属性和内容，再依据类型及顺序把片段组合为推理步骤，并处理 ref 等交叉引用属性以建立可导航的依赖图。解析器还处理标签未闭合、属性缺失等格式偏差；无法完整解析时展示可恢复的部分，必要时退化为原始文本。

<div class="method-step__io" markdown="1">

**输入**：大语言模型生成的领域特定语言文本，其中每个片段原则上采用“开始标签、内容、结束标签”的形式。<br>
**输出**：由推理步骤、语义片段、标识符和依赖边构成的结构化推理数据。

</div>

**直观理解**：这一阶段像把模型填写的半结构化表格读入程序，并画出“这一步用了哪些前面结果”的连线；即使个别格式写错，系统也尽量显示仍可识别的内容，而不是让整个答案失效。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 交互展示、定点反馈与局部再生成

界面将步骤视觉分隔，并允许用户点击引用片段以高亮其依赖项；发生纠错时，系统把纠错点之前的全部推理步骤与用户反馈共同组成新的生成提示，再调用大语言模型产生更新后的后续答案。该机制把已验证步骤作为检查点保留，避免无条件重新生成整条推理轨迹。

<div class="method-step__io" markdown="1">

**输入**：结构化推理数据、依赖关系，以及用户对某一错误步骤给出的定向反馈。<br>
**输出**：可逐步核验、可追踪依赖并可迭代修正的推理界面，以及利用既有正确步骤生成的更新答案。

</div>

**直观理解**：用户可以像批改分步解答一样定位具体错误，并查看该步骤依赖了哪些信息。修改时只从出错位置继续做，前面已经确认正确的部分继续沿用。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。原文方法没有提出新的损失函数、参数优化目标或专门的模型训练过程，而是通过少样本提示约束现有大语言模型在推理时生成结构化输出；因此改进对象主要是输出表示、解析和人机交互，而不是模型权重。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 自包含推理步骤答案模式**

普通步骤由 Goal、Premise 和 Partial 等语义片段组成，分别表达本步目标、所用假设或前序信息以及局部结果；轨迹开头另设摘要步骤，从题目提取 Fact 和 Question，末尾步骤用 Goal 与 Final 给出总体目标和最终结果。每一步应包含足以独立核验的上下文，并形成一个可保存、复用的部分解状态。

> 直观理解：该设计把一次长推理切成若干能单独检查的小题。用户无需始终记住整条解题路线，也更容易判断错误究竟出现在信息提取、前提使用、局部计算还是最终汇总。

**2. 领域特定语言与容错解析器**

领域特定语言使用类似 XML 的标签编码语义角色，以标签属性编码交叉引用等元信息；例如 Premise 片段可通过 ref 属性引用先前编号的片段。解析器利用命名捕获组识别类型、属性和内容，并在模型未严格遵守格式时提供部分解析或原始文本回退。

> 直观理解：标签使同一份模型输出既能被人阅读，也能被程序转成交互界面；容错机制则承认大语言模型并非严格的格式化程序，避免一个漏写的标签导致整个推理过程无法使用。

**3. 依赖导航与检查点式纠错**

系统根据交叉引用构造步骤间的依赖关系，支持点击片段后高亮其全部相关依赖。纠错时，提示仅纳入纠错点之前的已有步骤和用户反馈，使模型基于已验证的部分解继续生成，而不是重新求解全部问题。

> 直观理解：依赖导航回答“这个结论从哪里来”，检查点机制则回答“改错后哪些内容可以保留”。两者共同把查看静态解释转变为用户与模型协作完成和修正解答的过程。

**训练与推理**

该方法属于推理时工作流。首先，把原问题与若干遵循答案模式的完整示例放入提示，调用现有大语言模型生成带语义标签和引用属性的推理轨迹；其次，解析生成文本并构造步骤及依赖图；然后在界面中呈现可点击、可核验的结果。若用户指出某一步错误，系统收集其反馈，将该步骤之前的推理检查点与反馈拼接成新的提示，再次调用模型生成修订后的后续推理和最终答案。原文未描述利用这些反馈更新模型参数，也未说明单独训练解析器。

**复现信息**

复现所需的核心约定是六类语义标签 Fact、Question、Goal、Premise、Partial、Final，以及以键值属性保存元信息的标签格式；原文示例使用 ref=[#2] 或 ref=[#2,#5] 表示对一个或多个已有片段的引用。片段解析模式概念上由类型、属性和内容三个命名部分组成，内容采用非贪婪匹配，并要求结束标签与开始标签类型一致。工程实现还需提供对未闭合标签、缺失属性等异常的容错处理，以及“部分结构化展示—原始文本展示”的降级路径。原文摘录未明确报告具体基础模型、解码参数、提示示例数量、编程语言或前端框架，因而不能据此补充这些配置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K 数学文字题数据集：功能评估使用包含 1,319 道未见题目的完整测试集，比较两种提示方式的任务准确率与输出长度；在线用户实验也从 GSM8K 取题，每位参与者完成四轮，其中两题是 Llama3.3-70B 初始解答正确的题目、两题是初始解答错误的题目，并随机呈现。该数据集在本文中的作用是提供步骤可检查、答案可客观判定的推理任务。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**答案准确率与平均输出长度**

答案准确率衡量模型在 GSM8K 测试集上最终答案正确的比例；平均输出长度以 token 计，衡量结构化输出的生成开销与冗长度。前者检验可解释格式是否损害任务能力，后者刻画这种格式的成本。 （准确率越高越好；在准确率相当的前提下，输出长度通常越短越经济，但本文预期自包含步骤需要重复必要上下文，因此长度增加是可解释性设计的直接代价，而不能单独视为推理质量下降。）

</div>
<div class="metric-item" markdown="1">

**主观感知量表**

以 1 至 7 分 Likert 量表测量易用性、有用性和信任，并将各构念对应题项取平均。内部一致性以 Cronbach’s alpha 检查；组间比较因数据不服从正态分布而采用单侧 Mann–Whitney U 检验，检验用户中心 CoT 是否得到更高评分。 （构念均值越高表示参与者主观上认为系统越易用、越有用或越值得信任；但较高主观评分不等同于更高的实际判断或纠错能力。）

</div>
<div class="metric-item" markdown="1">

**判断准确率与纠错成功率**

判断准确率是用户将模型初始答案正确分类为“正确”或“错误”的比例；纠错成功率是在初始答案错误时，用户反馈促使更新后答案变正确的比例。两项均采用双侧 Mann–Whitney U 检验比较组间差异。 （两项均越高越好：前者表示用户更能识别模型是否出错，后者表示用户反馈更能实际修复错误。不过，纠错成功率只对曾正确识别至少一个错误的参与者定义，因此其有效样本量更小。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### GSM8K 功能评估：三种模型规模下，用户中心 CoT 与标准 CoT 的准确率和平均输出长度比较。

<div class="result-value" markdown="1">

Llama3.3-70B 的准确率为 0.959 对 0.953，Gemma 27B 为 0.943 对 0.941，说明中大型模型的最终答案表现基本相当；Llama3.2-3B 则为 0.487 对 0.367，用户中心格式高出 0.120。代价是三种模型的用户中心输出均明显更长：分别为 1088.5 对 345.1、1114.6 对 301.2、1172.0 对 338.1 token，约为标准 CoT 的三倍。

</div>

作者据此主张，结构化、自包含的推理格式没有损害中大型模型的任务表现，并可能帮助小模型。更谨慎的解释是：该格式至少能在 GSM8K 上保持最终答案准确率，但长度成本很高；小模型的提升也不能直接归因于“可解释性”，因为一次示例中的额外结构、提示内容和更长计算轨迹都可能共同影响答案。论文没有报告重复运行、置信区间或显著性检验，因此不能确认三种模型的准确率差异具有统计显著性。

<div class="result-source" markdown="1">

来源：表 2（Table 2）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Llama3.3-70b | 0.959 | 1088.5 | 0.953 | 345.1; Gemma3-27b | 0.943 | 1114.6 | 0.941 | 301.2; Llama3.2-3b | 0.487 | 1172.0 | 0.367 | 338.1

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 在线组间用户实验：比较用户中心 CoT 与标准 CoT 的易用性、有用性和信任。

<div class="result-value" markdown="1">

用户中心 CoT 在易用性上获得显著更高评分，检验结果为 $U=1004.0$、$p<0.05$；在有用性上也显著更高，$U=970.5$、$p<0.05$。信任的组间差异不显著。

</div>

这支持作者关于“结构化步骤改善用户主观使用体验”的核心主张：参与者更容易使用这种界面，也更认可其用途。但结果没有证明用户更信任系统，更没有证明他们实际更善于发现或修复错误。由于论文只报告 $p<0.05$，未给出效应量或多重比较校正，差异的实际大小和稳健性仍需谨慎判断。

<div class="result-source" markdown="1">

来源：第 5.3 节 Analysis and Results；描述性分布见图 4，均值见表 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Participants in the treatment group provided significantly higher values for ease-of-use (U = 1004.0, p < 0.05) and usefulness (U = 970.5, p < 0.05). Differences for trust were not significant.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 在线组间用户实验：比较用户判断模型答案对错的准确率，以及反馈将错误答案修正为正确答案的概率。

<div class="result-value" markdown="1">

两项行为指标均未出现显著组间差异。描述性结果甚至没有呈现用户中心组更高的趋势：判断准确率为 0.62 对 0.68；纠错成功率为 0.36 对 0.60，但后者有效样本量分别只有 13 和 24。

</div>

用户中心 CoT 提升了主观易用性和有用性，却没有转化为可检测的行为收益；因此论文不能据此声称用户更准确地识别错误或更成功地修复模型。纠错成功率的样本量较小，而且只纳入曾识别出错误的参与者，估计可能不稳定；另一方面，“未显著”也不等于两种方法已被证明完全等效。

<div class="result-source" markdown="1">

来源：第 5.3 节 Analysis and Results；描述性数值见表 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Both measures were not normally distributed (Shapiro-Wilk test, p < 0.001 for both measures) and two-sided Mann-Whitney U tests did not show significant differences between the groups for both measures.

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

- 标准 CoT 提示：让模型生成常规自然语言逐步推理，不使用本文的 XML 式领域专用语言、原子化步骤、交叉引用及步骤级反馈结构。它是最直接且有意义的对照，因为实验要隔离的核心变量正是“面向用户的结构化推理呈现”，而非是否要求模型展示推理。
- 用户中心 CoT：作为实验处理条件，通过一次示例提示要求模型生成带 XML 式标签、元数据和交叉引用的自包含推理步骤；解析后在网页界面中分步展示，并允许用户针对具体步骤提交反馈、触发后续步骤的选择性重生成。

**实验想回答的问题**

- 功能层面：与标准思维链（Standard CoT）相比，将推理组织成带标签、可交叉引用且自包含的步骤，是否会降低不同规模大语言模型在数学文字题上的答案准确率，并带来多大的输出长度开销？
- 人因层面：在用户检查并纠正模型解答的协作任务中，用户中心思维链（User-Centric CoT）能否改善易用性、有用性与信任等主观体验，以及判断正确性和纠错成功率等实际行为表现？

**实验实现**

功能评估在 GSM8K 的 1,319 道测试题上进行，以一次示例提示分别驱动小型 Llama3.2-3B、中型 Gemma 系列 27B 和大型 Llama3.3-70B，比较用户中心 CoT 与标准 CoT。用户中心输出先由正则解析器转换为结构化 JSON，再由 React 网页界面显示为可点击引用的原子步骤；用户纠正某一步后，系统将纠正内容和已有步骤传回模型，仅重生成受影响的后续步骤。用户实验采用组间设计，底层模型固定为 Llama3.3-70B：处理组查看用户中心 CoT，对照组查看标准 CoT。参与者先完成示例，再完成四轮检查与纠错，最后填写问卷。共招募 122 人，排除未通过注意力检查或多次复制题目、答案文本者后，论文称最终样本为 80 人，其中处理组 37 人、对照组 43 人。主观构念不服从正态分布，故采用单侧 Mann–Whitney U 检验；行为指标采用双侧 Mann–Whitney U 检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It structures LLM chain-of-thought into self-contained, verifiable steps to improve human inspection and correction of mathematical reasoning.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`821eca3d48503ada28620273ac9ba02e4921c8197e6ee9763b7c13a642dac98f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
