---
title: "[论文解读] ImmigrationReason: A Structured Dataset of U.S. Immigration Appeals for Legal Reasoning Research"
description: "[arXiv 2608.20391][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.20391"
announcement_date: "2026-08-24"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-24T02:12:19.152206+00:00"
source_sha256: "964f3bbf7acb495839843d6fc781cb82f3e6cc9a79a3f2fa0907ce69fae177fc"
tags:
  - "LLM Reasoning"
  - "法律自然语言处理"
  - "行政裁决"
  - "美国移民法"
  - "AAO"
  - "结构化法律数据集"
  - "法律推理"
  - "证据充分性"
  - "裁决错误"
  - "Dhanasar"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.20391</p>

# ImmigrationReason: A Structured Dataset of U.S. Immigration Appeals for Legal Reasoning Research

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Amirhossein Afsharrad, Seyed Shahabeddin Mousavi</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Stanford University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.20391v1) · [PDF 下载](https://arxiv.org/pdf/2608.20391v1) · **关键词** 法律自然语言处理, 行政裁决, 美国移民法, AAO, 结构化法律数据集, 法律推理, 证据充分性, 裁决错误, Dhanasar<br>


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

法律自然语言处理（Legal NLP）利用语言模型和结构化数据处理法律文本，典型任务包括法律检索、分类、论证分析和结果预测。现有资源主要来自美国联邦法院判决或其他司法材料，常把任务简化为粗粒度分类或片段抽取；但行政裁决同样是法律决策的重要组成部分，其特点是行政机关依据法规和监管框架判断个人权利与资格，而不是主要依赖普通法判例。本文聚焦美国就业移民申请的行政复审：美国公民及移民服务局（USCIS）的行政上诉办公室（AAO）对服务中心拒绝的 $I$-140 职业移民申请进行重新审查，并公开发布非先例决定。该场景要求同时理解适用法律框架、逐项评估证据是否满足标准、识别原审官员的推理错误，并将结论与具体法律引文相联系，因此适合作为高风险法律推理研究的数据基础。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**行政裁决与非先例决定**

行政裁决是政府机构依据法规审查个人申请并作出决定，而非由普通法院审理诉讼。AAO 的非先例决定可以公开提供具体推理，但通常不作为对其他案件具有约束力的判例。

</div>
<div class="concept-item" markdown="1">

**EB-1A 与 Kazarian 两步分析**

EB-1A“杰出人才”申请受 $8\ C.F.R.\ \S\ 204.5(h)(3)$ 约束，申请人须先满足十项证据标准中的至少三项。AAO 依照 Kazarian 方法先统计满足的标准，再进行最终实质审查，即综合判断申请人是否确实具有持续的国内或国际声誉。

</div>
<div class="concept-item" markdown="1">

**EB2-NIW、Dhanasar 与法律制度转换**

国家利益豁免（EB2-NIW）允许在满足特定公共利益条件时免除工作邀约要求；2016 年 12 月起，AAO 使用 Dhanasar 的三项标准：事业具有实质价值和国家重要性、申请人有能力推进该事业，以及总体上豁免工作邀约对美国有利。此前适用 NYSDOT 框架，因此该时间点形成数据中的自然法律制度边界。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文不是提出一个单一的预测模型，而是构建一个面向法律推理研究的结构化数据集。输入是 2005—2026 年 AAO 公开发布的 12,375 份美国就业移民非先例决定及其扫描或数字文档；数据处理后输出包括案件层元数据、适用法律框架、法律问题及其推理、每个法律标准或“prong”的证据充分性判断、原审官员错误的逐字批评、全部法律引文和最终处置结果，同时提供经 Claude 转录的正文。每个记录还区分原审官员与 AAO 对各项标准的判断，并使用五类别标签表达证据充分性。研究假设是：公开决定中的法律框架、证据评价和裁决理由可以被可靠地抽取为机器可读结构；抽取结果由两个独立模态和比较提示裁决组成的三遍流程处理，并在 500 条记录上接受领域专家核验。数据还保留 2016 年 Dhanasar 制度转换，使模型可以在法律规则变化前后进行时间外推或分布外测试。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$I\text{-}140$**

美国职业移民申请表；本文所研究的 AAO 复审案件对象。

</div>
<div class="notation-item" markdown="1">

**$EB\text{-}1A$**

就业移民第一优先类别中的杰出人才申请类别。

</div>
<div class="notation-item" markdown="1">

**$EB2\text{-}NIW$**

就业移民第二优先类别中的国家利益豁免申请类别。

</div>
<div class="notation-item" markdown="1">

**$Dhanasar$**

2016 年 12 月后用于 EB2-NIW 审查的三项法律标准框架。

</div>

</div>

**直接相关的工作**

- **LegalBench（Guha et al., 2023）与 LexGLUE（Chalkidis et al., 2022）**: 这些资源分别提供大规模法律推理任务和跨法域法律分类数据，但主要以联邦判例为中心，并偏向分类或片段抽取；原文指出它们没有行政法覆盖、逐项证据充分性判断或原审裁决错误标注。因此，ImmigrationReason 将研究对象从粗粒度司法文本扩展到具有细致理由结构的行政裁决。
- **Pile of Law（Henderson et al., 2022）**: Pile of Law 是大规模原始法律文本预训练语料，代表了以传统 OCR 或文档抽取为主的法律文本资源。本文将其相关处理方式作为背景比较，并报告 Claude 转录相较 PyMuPDF 在扫描文档中的文本恢复优势；但 ImmigrationReason 的主要新增点不是文本规模，而是 AAO 决定中的法律框架、逐项证据结论和官员错误等结构化标注。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现有法律自然语言处理资源主要来自联邦法院判例，并常被简化为粗粒度分类任务，难以反映真实法律工作中对证据逐项衡量、随法律规则变化进行推理、依据引文论证以及识别裁决错误的要求。美国移民行政裁决尤其值得研究：行政机构处理的决定数量远超联邦法院，而美国公民及移民服务局已经明确承认在裁决流程中部署人工智能工具，因此需要能够独立评估这类高风险监管推理的数据资源。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于联邦法院判例的法律自然语言处理数据集**：这类资源从联邦法院公开判例中构建数据，通常将法律任务整理为案件级分类或其他粗粒度预测问题，用于训练和评测模型。
- **原始法律文本语料库或浅层标注资源**：这类方法主要提供判决文本、案件元数据或有限的结果标签，让研究者从文本中自行推断法律依据、证据是否充分以及推理过程中的错误。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有资源几乎没有覆盖行政裁决，而行政机构依据监管框架决定个人权利和资格，其法律标准与普通法判例存在根本差异；因此，基于法院数据训练或评测的模型未必能处理移民行政裁决。
- 既有任务多为案件级粗粒度分类，缺少行政裁判机构对每一法律要件的证据充分性判断、原审官员错误的逐字批评以及相应引文；因此，模型难以被检验是否真正完成了可追溯的多步骤法律推理，而不只是预测最终结果。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一个面向美国移民行政上诉、同时连接法律框架、逐项证据判断、裁决者错误、引文和最终处分的结构化资源，并且缺少能够检验模型适应法律制度自然变化的数据条件。该空缺使研究者无法系统分析行政裁决中的法律推理质量、错误类型及其随规则变化的表现。

</div>
<div markdown="1"><span>核心问题</span>

能否从美国公民及移民服务局行政上诉办公室的非先例决定中，构建经过验证的深层结构化数据集，使研究者能够研究逐法律要件的证据充分性、原审裁决错误、最终结果以及法律制度变化下的模型泛化？

</div>
<div markdown="1"><span>作者直觉</span>

行政上诉决定同时保留了适用法律框架、原审与上诉机构对各项要件的判断、具体批评语句、引文和最终处分，因此比单一结果标签更接近真实的法律论证链条。将这些信息结构化，并利用2016年Dhanasar规则变更形成时间上的制度转折，可以把“模型是否理解规则”与“模型是否只记住表面模式”区分开来。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ImmigrationReason 是一个面向法律推理研究的数据集构建方法，而不是训练一个预测模型。其端到端流程为：从 USCIS AAO 网站收集 EB-1A 与 NIW 非先例决定，筛选并准备高质量文本，使用带 Pydantic 校验的结构化抽取器生成决定级、法律问题级和逐标准的嵌套记录，再通过两个独立抽取通道和第三个比较裁决通道处理分歧，最终形成带来源文本、结构化标注和溯源信息的数据集。直观地说，作者先把分散的法律裁决收集起来，再把每份长文档整理成可检索的“案件—法律问题—证据标准”三层表格，并对机器抽取结果进行交叉复核。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 来源收集与样本筛选

作者收集到 13,520 份、时间跨度为 2005 年 1 月至 2026 年 3 月的 PDF，并剔除 O-1 文件、文本抽取后少于 2,000 个字符的文件以及少量重复文件，得到 12,375 份决定。

<div class="method-step__io" markdown="1">

**输入**：USCIS 网站公开的 AAO 非先例决定 PDF，目标类别为 EB-1A，表格代码为 B2203，以及 NIW，表格代码为 B5203。<br>
**输出**：最终文档语料库包含 12,375 份 AAO 非先例决定，覆盖被 USCIS 服务中心拒绝后提交上诉或相关动议的案件。

</div>

**直观理解**：这一步相当于先确定研究边界：只研究两类就业移民案件，并清除明显无法读取或重复的文件。由于样本来自上诉程序，它代表的是“被拒且选择上诉”的案件，而不是所有移民申请。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 源文本准备与转录

对文本原生文件使用 PyMuPDF 进行近无损文本抽取；对全部文件生成由 Claude Sonnet 4.6 转录的 Markdown 版本，以恢复扫描件中的正文、脚注标记、裁判引用和结构信息。作者将 Claude 转录结果与传统 OCR 进行逐记录比较，并保留低质量或使用旧 OCR 回退的记录标记。

<div class="method-step__io" markdown="1">

**输入**：筛选后的决定 PDF，包括 2017 年后含嵌入文本的原生文本 PDF，以及主要由扫描图像构成的 2017 年前 PDF。<br>
**输出**：每份决定都有清洁 Markdown 源文本，另有 OCR 对比信息；绝大多数记录使用 Claude 转录或文本层，13 份记录使用传统 OCR 回退。

</div>

**直观理解**：早期裁决像扫描照片，普通 OCR 容易漏字、错读法律符号或截断页面。作者让视觉语言模型重新“读”整份文件，目的不是改变法律内容，而是尽量恢复可供后续结构化分析的原文。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 三层结构化信息抽取

Claude Sonnet 4.6 通过强制工具调用输出一个结构化 Decision 记录，并由 Pydantic 进行类型校验；校验失败时根据反馈最多重试 3 次，仍无法解决的情况进入升级处理。记录按 Decision、LegalIssue、Finding 三层组织，分别保存案件整体信息、每个法律问题的信息，以及每个法律标准或要件的证据与 AAO 结论。

<div class="method-step__io" markdown="1">

**输入**：每份决定的 PDF 或转录 Markdown 文本，以及预先规定的 Pydantic 数据模式和抽取提示词。<br>
**输出**：输出嵌套 JSON 记录，包括案件日期、程序姿态、签证类别、服务中心、最终命令、引用、AAO 对原审官员的批评、法律问题、申请人证据、双方结论、逐标准推理摘要和逐字引文等字段。

</div>

**直观理解**：作者没有把裁决压缩成一个简单的“批准/拒绝”标签，而是把它拆成三层：案件最终怎样、涉及哪些法律问题、每个具体标准是否满足。这样研究者可以追问模型“哪一项证据不足”以及“AAO 为什么这样判断”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 独立抽取、分歧裁决与数据发布

第一遍直接让 Sonnet 4.6 阅读 PDF，第二遍让其阅读转录 Markdown；对两遍在关键字段上不一致的 3,401 份记录，第三遍将源文本、两份冲突结果和分歧字段交给 Opus 4.7，通过比较提示词作裁决。最终记录同时保留抽取模型、提示词版本、token 数量和产生最终结果的 pipeline pass 等 provenance 信息。

<div class="method-step__io" markdown="1">

**输入**：同一批决定的原始 PDF、Claude 转录文本，以及前两次抽取产生的结构化记录。<br>
**输出**：发布 12,375 条决定级记录、45,290 条逐标准 finding、源文本、OCR 对比文件、3,401 条裁决记录及完整抽取代码和模式定义。

</div>

**直观理解**：前两遍像让两名读者分别独立整理同一判决；若答案不同，第三个模型查看原文和冲突点后作出有依据的裁决。保存冲突过程意味着研究者不仅能使用最终标签，也能审计哪些字段最容易被机器读错。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告用于训练数据集抽取模型的可优化损失函数或独立训练目标。方法使用的是 Claude Sonnet 4.6 和 Opus 4.7 的提示驱动推理、工具调用、Pydantic 验证、失败重试与分歧裁决，而非作者自行训练一个端到端参数模型。对于下游任务，论文提出可利用案件结果、逐标准结论、原审推理与 AAO 修正对构造监督信号，但没有给出具体的分类损失、生成目标或优化公式。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 三层 Pydantic 结构化模式**

Decision 层保存 filename_stem、decision_date、posture、visa_category、originating_office、最终命令、引用、整体立场和批评引文；LegalIssue 层最多覆盖 17 类问题；Finding 层记录每个 prong 或 criterion 的证据类型、申请人论证、director_finding、aao_finding、推理摘要、逐字推理引文以及是否同意原审官员。

> 直观理解：该模式把长篇法律文本转换为层次化、可计算的数据结构，使研究者能够同时进行案件级预测和标准级法律推理分析，而不必每次从头阅读全文。

**2. 五类别逐标准结论标签**

aao_finding 包含 met、not_met、reserved、waived_by_petitioner 和 not_addressed 五类。reserved 表示 AAO 因其他问题已足以决定案件而不处理该问题；waived_by_petitioner 表示申请人上诉时没有提出该问题并被视为放弃；not_addressed 表示双方均未实质讨论该问题。

> 直观理解：作者区分“没有满足”“没有必要判断”“申请人放弃”和“根本没有讨论”。如果强行把这些状态都压成满足或不满足，就会把程序性信息误当成实体法律结论。

**3. 双通道抽取与比较裁决**

Pass 1 从 PDF 直接抽取，Pass 2 从 Claude 转录 Markdown 抽取；对关键字段存在分歧的记录使用 Opus 4.7 进行比较式 adjudication，而不是简单多数投票。作者报告，裁决记录中有 10.1% 的情况产生了前两遍都没有得到的值。

> 直观理解：两种输入形式会暴露不同错误：直接读 PDF 可能受版面影响，读转录文本则可能受转录误差影响。比较裁决让第三步专门分析冲突，并允许它认为前两份答案都不对。

**训练与推理**

抽取阶段的推理过程从每份决定文本开始：Pass 1 将 PDF 直接输入 Sonnet 4.6，Pass 2 将 Claude 转录的 Markdown 输入同一模型，并要求模型按照固定 schema 输出单个结构化记录。每次输出经过 Pydantic 类型和字段约束检查，验证失败时把验证反馈用于最多 3 次重试；两遍在关键字段一致时采用相应结果，在 3,401 份存在分歧的记录中，将原文、两份抽取结果和具体冲突字段输入 Opus 4.7 进行第三遍比较裁决，得到最终记录。论文没有报告作者对 Sonnet 或 Opus 进行参数微调、训练集划分或梯度优化。

**复现信息**

复现所需的主要组件包括 USCIS AAO 公开 PDF、PyMuPDF 文本抽取、Claude Sonnet 4.6 视觉转录、Anthropic Files API、强制工具调用、Pydantic schema、验证失败重试机制和 Opus 4.7 比较裁决。转录提示词要求保留文档顺序、LAW 与 ANALYSIS 等结构、所有实质文本及 I&N Dec.、F.3d、U.S.C. 和 C.F.R. 引用；最终发布 corpus_final.jsonl、源文本、ocr_comparison.jsonl、adjudicated.jsonl、schema、提示词、代码和每条记录的 provenance。应谨慎解释结果：数据仅包含初次被拒且选择上诉的非先例决定，存在上诉选择偏差；非先例决定不对未来案件具有约束力，且 LLM 抽取在罕见程序姿态或含糊裁决中仍可能出错。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ImmigrationReason：包含 $12{,}375$ 份美国公民及移民服务局行政上诉办公室（AAO）的非先例裁决，覆盖 $2005$ 至 $2026$ 年。每条记录包含法律框架、逐要件证据充分性判断、五类别 finding-state 标签、裁决者批评的逐字引文、引用和最终处置结果。该数据集用于整体统计分析、制度变化分析、服务中心差异分析以及未来法律推理任务的评估。
- 法律框架子集：包括 $1{,}280$ 份 NYSDOT 框架裁决和 $3{,}484$ 份 Dhanasar 框架裁决；前者全部发生在 $2016$ 年 $12$ 月以前，后者全部发生在此后。该子集用于考察 $2016$ 年 Dhanasar 判决带来的法律制度转换，并可构造时间上的分布外评估划分。
- 表格中的相关资源比较集：包括 ImmigrationReason、LegalBench、LexGLUE、Pile of Law、CaseHOLD、LawBench 和 Refugee NLP。比较维度是数据规模、是否具有结构化标注、是否包含逐要件判断以及是否面向美国行政法；其作用是定位本数据集相对于既有法律自然语言处理资源的结构化优势，而不是作为同一预测任务上的性能测试集。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**反转率**

某一发起服务中心的案件中，AAO 推翻原始主管机构裁决的比例，用于衡量裁决分歧或反转现象。 （不存在普遍的越高越好或越低越好；它主要用于比较机构差异，较高值表示该中心的原始裁决更常被 AAO 推翻。）

</div>
<div class="metric-item" markdown="1">

**要件成功率**

在特定法律框架下，申请人在某一 prong 或 criterion 上被 AAO 判定满足要求的比例，用于识别最常导致失败或最具争议的法律要件。 （不存在普遍的越高越好或越低越好；较低值表示申请人较少在该要件上成功，可能意味着该要件更具限制性或更常成为决定性障碍。）

</div>
<div class="metric-item" markdown="1">

**Pass 3 裁决一致性与新答案比例**

第三遍 Opus 4.7 裁决分别支持前两遍抽取结果的比例，以及不采纳任一前序答案而产生新答案的比例，用于衡量多遍抽取的分歧与补充价值。 （支持前序结果的比例越高通常表示流程更稳定；新答案比例不能简单解释为越高越好，因为它既可能发现前序错误，也可能表示抽取分歧较大。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 数据集规模、标注结构与既有法律 NLP 资源比较

<div class="result-value" markdown="1">

ImmigrationReason 包含 $12{,}375$ 条记录，并同时提供结构化标注、逐要件 findings 和美国行政法覆盖；表格中其他相关资源均未被标为同时具备这三项特征。该结果支持作者关于数据集结构化粒度具有差异化的主张。

</div>

这说明数据集不仅收集案件文本，还把裁决拆成可分析的法律要件级判断，因此可以研究“申请人在哪一个具体标准上失败”而不只是预测最终胜负。但资源比较不等于任务性能比较；它不能证明使用该数据训练的模型一定优于其他数据训练的模型。

<div class="result-source" markdown="1">

来源：Appendix F, Table 5 Dataset Comparison

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The key differentiator is structured per-criterion annotations under a five-category label; no prior resource provides this.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 服务中心反转模式

<div class="result-value" markdown="1">

不同发起服务中心的 AAO 反转率存在明显差异：California SC 为 $54.4\%$，SCOPS 为 $44.3\%$，Vermont SC 为 $36.0\%$。这表明数据集可以揭示原始裁决机构之间的制度性差异。

</div>

在这里，反转率不是模型准确率，而是 AAO 是否推翻服务中心原决定的比例。差异提示案件来源机构可能与裁决结果相关，但该统计本身不能证明服务中心差异是因果原因，也不能排除案件类型、复杂度或年份分布不同造成的混杂。

<div class="result-source" markdown="1">

来源：Section 5 Dataset Analysis, subsection “Reversal patterns by service center”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

California SC (54.4%) and SCOPS (44.3%) are reversed at notably higher rates than Vermont SC (36.0%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 法律制度转换与逐要件结果模式

<div class="result-value" markdown="1">

数据集捕获了 $2016$ 年 $12$ 月 Dhanasar 判决引起的法律框架转换：$1{,}280$ 条裁决属于 NYSDOT 框架，$3{,}484$ 条属于 Dhanasar 框架，且两者几乎没有重叠。在要件层面，Dhanasar NIW 的 Prong 3 成功率最低；Kazarian EB-1A 中，awards、published material 和 original contributions 是较具争议的标准。

</div>

这提供了一个自然的时间切分：模型可以在旧法律框架上学习，再测试其对新框架的迁移能力，或反过来研究法律规则变化如何改变裁决模式。不过，框架前后案件的申请人、年份和案件构成可能不同，因此该现象不能单独证明 Dhanasar 判决造成了所有观察到的差异。

<div class="result-source" markdown="1">

来源：Section 5 Dataset Analysis, subsection “The natural regime-change experiment”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

This transition appears as a sharp discontinuity in Figure 2 (b): the corpus captures 1,280 NYSDOT-framework decisions (all before December 2016) and 3,484 Dhanasar-framework decisions (all after), with essentially zero overlap.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 现有摘录未提供标准预测任务上的训练、验证和测试划分，也未报告与具体模型基线比较的准确率、F1 或其他预测性能。因此，数据集的结构化价值不能直接转化为模型性能优势。
- 该数据集来自 AAO 非先例裁决，且原文分析的许多模式是描述性统计；服务中心反转率、法律框架前后差异和要件成功率都可能受到案件构成、时间和程序姿态影响，不能仅凭这些结果作出因果结论。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 既有法律自然语言处理资源作为资源级比较对象：LegalBench、LexGLUE、Pile of Law、CaseHOLD、LawBench 和 Refugee NLP。它们用于比较数据规模与标注粒度，不是本文预测模型的算法基线。
- 原始表单编码作为字段质量的朴素参照。分析将表单推断的签证类别与模型抽取的 $visa\_category$、$issue\_type$ 字段进行对照，检验原始表单类别是否足以代表实质法律问题。
- 发起裁决的服务中心作为机构差异比较维度。不同服务中心的反转率用于检验裁决结果是否存在机构层面的系统差异，而非评估一个分类器。
- 两种前序抽取模态与第三遍 Opus 4.7 比较裁决作为抽取质量验证中的内部参照。第三遍判断会比较前两遍结果，并在分歧时作出裁决；该设计检验结构化抽取是否稳定，而不是与外部模型进行任务性能对比。

**实验想回答的问题**

- 数据集是否覆盖足够丰富且结构化的美国移民行政裁决信息，从而支持按法律标准、证据充分性和裁决结果开展细粒度法律推理研究？
- 数据中是否存在可用于法律制度变化、裁决者差异和错误分析的经验模式，例如服务中心反转差异、不同法律标准下的标准转换，以及各法律要件的成功率差异？

**实验实现**

实验以数据集统计和字段质量分析为主，而非训练一个统一的端到端预测模型。作者先对裁决文本进行结构化抽取，再统计法律框架、签证类别、问题类型、逐要件 finding state、引用、最终处置和 AAO 对主管机构的批评。抽取质量通过三遍流程验证：两种相互独立的模态先生成结构化结果，随后由 Opus 4.7 使用比较提示词进行第三遍裁决；此外，作者在 $500$ 条记录上进行领域专家核验。分析还按年份、服务中心、法律框架和具体法律要件分组。原文未明确报告传统监督学习或生成模型的训练集、验证集、测试集划分，也未报告统一预测任务上的模型实现细节。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 该论文没有提供单一案件的深入定性案例研究；最接近的定性分析是字段与制度模式分析。特别是，原始表单类别与实质问题不一致的现象表明，仅依据表单标签会把 EB-2 门槛、劳工认证、支付能力或程序问题误归为 NIW 实质分析，因此结构化字段对案例筛选和法律推理任务定义具有实际意义。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文构建并分析用于法律推理研究的结构化行政裁决数据集，主要服务于复杂法律证据与规则推理。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`964f3bbf7acb495839843d6fc781cb82f3e6cc9a79a3f2fa0907ce69fae177fc`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
