---
title: "[论文解读] SCAFFOLD: A Large-Scale Structured Dataset of Computer Science Research Figures with Diagram QA and Chain-of-Thought Reasoning Traces"
description: "[arXiv 2609.00018][VLM Reasoning] 原文未明确报告。"
arxiv_id: "2609.00018"
announcement_date: "2026-09-02"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:47:30.498710+00:00"
source_sha256: "824f4cc74039169dfbfa146cfa56525c571df869298af6f4d638fadfba26de32"
tags:
  - "VLM Reasoning"
  - "LLM Reasoning"
  - "多模态 VLM"
  - "视觉语言模型"
  - "计算机科学研究图"
  - "图表问答"
  - "链式思维推理"
  - "科学文献理解"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2609.00018</p>

# SCAFFOLD: A Large-Scale Structured Dataset of Computer Science Research Figures with Diagram QA and Chain-of-Thought Reasoning Traces

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Ranjit Raut, Aarav Subedi, Sagun Rai, Sudan Jha</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Department of Artificial Intelligence；Affiliation: Kathmandu University；Affiliation: Department of Computer Science and Engineering</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00018v1) · [PDF 下载](https://arxiv.org/pdf/2609.00018v1) · **关键词** 视觉语言模型, 计算机科学研究图, 图表问答, 链式思维推理, 科学文献理解<br>
**代码**: [https://github.com/theranjitraut/scaffold](https://github.com/theranjitraut/scaffold)

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

本文位于视觉语言模型（VLM）与科学文献理解的交叉领域。VLM将图像和文本共同作为输入，既要识别图中内容，也要结合文字完成问答；本文关注的不是自然照片或普通统计图，而是计算机科学论文中的架构图、流程图和多阶段管线图。这类图通常通过方框、箭头、模块名称及其连接顺序表达系统结构，因此理解任务需要同时利用图像、图注和论文上下文，并进行结构化推理。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉语言模型（VLM）**

VLM能够联合处理图像与文本，例如根据一张图和一个问题生成答案。本文将其应用于论文图表，而不是通常的照片或日常场景。

</div>
<div class="concept-item" markdown="1">

**计算机科学研究图**

这类图包括架构图、系统流程图和管线示意图，常用方框表示模块、箭头表示数据或控制流。正确回答问题往往要求追踪模块之间的连接或处理步骤，而不只是识别单个物体。

</div>
<div class="concept-item" markdown="1">

**链式思维推理轨迹**

链式思维推理轨迹是从问题到最终答案之间的逐步中间说明。它使数据不仅监督答案，还监督模型如何依据图中结构、图注和上下文得到答案。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文将公开发表的计算机科学论文作为数据来源，先从论文 PDF 中提取研究图及其图注，再关联图所在位置附近的论文上下文，并为每个图文样本生成问题、答案和逐步推理轨迹。单个样本可表示为 $(I,C,X,Q,A,R)$：其中 $I$ 是图像，$C$ 是图注，$X$ 是上下文，$Q$ 是问题，$A$ 是答案，$R$ 是推理轨迹；数据集的输出是大量此类结构化样本，而非一个新的预测模型。其基本假设是，图像区域能够被可靠地从 PDF 中分离出来，图注和上下文能够提供解释图中结构所需的语义信息，AI 辅助生成的问题、答案与推理轨迹能够形成可用于 VLM 训练和评测的监督数据。论文报告了三个规模版本：SCAFFOLD-157K、SCAFFOLD-37K 和 SCAFFOLD-12K，并使用后者进行基线训练实验。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$I$**

从论文 PDF 中提取并裁剪得到的研究图像

</div>
<div class="notation-item" markdown="1">

**$C$**

与图像对应的图注

</div>
<div class="notation-item" markdown="1">

**$X$**

图像所在论文位置附近的上下文文本

</div>
<div class="notation-item" markdown="1">

**$Q,A,R$**

分别表示问题、答案和逐步链式思维推理轨迹

</div>

</div>

**直接相关的工作**

- **FigureQA、DVQA 与 PlotQA**: 这些数据集主要使用合成的柱状图、折线图或饼图，并配以模板化的判断题或简短答案问题。它们说明了视觉问答数据构建的可行性，但不能覆盖计算机科学架构图中“哪个模块向哪个模块提供输入”或“步骤按何种顺序连接”等结构推理。
- **CharXiv**: CharXiv 同样从 arXiv 论文中提取真实图表，因此在数据来源上最接近本文；但其问题主要围绕图表和曲线读取，而不是研究系统图中的模块连接、数据流和流程关系。本文据此将目标进一步限定为计算机科学研究图的图级理解。

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

SCAFFOLD并非提出新的视觉语言模型，而是建立一条从计算机科学论文PDF到图表问答训练样本的自动化数据构建流水线。其输入是arXiv论文PDF；系统先逐页渲染并检测图像与图注区域，再从原始PDF精确裁剪图像、匹配图注，并从正文中检索首次引用该图的句子；随后以“图像—图注—上下文”三元组为条件，通过Gemini生成问题、答案及可用的思维链，失败时则由确定性模板生成结构完整的替代样本。最终输出包含标识符、图号、图注、引用句、问题类型、问答、推理轨迹及来源标记等信息的结构化记录，同时提供便于检查的完整JSON形式和可直接用于视觉语言模型训练的聊天消息形式。

这套方法的核心设计不是让单个生成模型包办所有步骤，而是把版面解析、图文关联、上下文定位和问答生成分开处理，并为关键的不确定环节保存状态与来源信息。例如，正文引用句未找到时记录$\texttt{ref\_sentence\_found}=\texttt{False}$，Gemini不可用时启用模板回退，用户因而可以按完整性或生成来源筛选数据，而不必把所有自动生成记录视为同等可靠。直观地说，它像一条论文图表“装配线”：先把图从PDF中找准、裁好并补齐周边说明，再把这些材料加工成可训练的问答样本，并为每件产品附上来源和质量状态标签。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 论文获取与页面标准化

系统按页而非按整篇论文处理PDF，并将每页独立渲染为150 DPI的固定分辨率图像，供后续版面检测器使用。PDF本身仍被保留，以便后续从矢量或高质量源内容中裁剪图像。

<div class="method-step__io" markdown="1">

**输入**：来自arXiv的计算机科学论文PDF；当前版本覆盖3,058篇论文。<br>
**输出**：页面级栅格图像、原始PDF及对应的论文和页码关联信息。

</div>

**直观理解**：先把不同来源、不同页面尺寸的论文统一成检测器容易处理的页面图片，但真正截取图表时仍回到原始PDF，避免因截图造成不必要的清晰度损失。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 版面检测、精确裁图与图注匹配

使用在DocLayNet版面类别体系上微调的YOLOv8检测页面中的Picture和Caption区域，再由PyMuPDF依据检测框直接从源PDF裁剪图像。每个图像区域通过结合垂直距离与水平边界框重叠程度的启发式规则，与空间上最可能对应的图注配对。

<div class="method-step__io" markdown="1">

**输入**：150 DPI页面图像及其原始PDF页面。<br>
**输出**：高质量裁剪图像、候选图注文本及二者的配对关系。

</div>

**直观理解**：检测器负责回答“哪里是图、哪里是图注”，PDF工具负责把图清晰地剪出来；匹配规则不能只找正下方文字，因为论文图注的位置和宽度并不总是完全规整。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 正文上下文链接与记录清理

系统在全文中搜索第一条提及对应图号的句子，并兼容“Figure 3”“Fig. 3”和“Fig.3”等写法，将该句作为图表的语境依据。无法检测图注、无法解析图号或找不到引用句的情况不会被静默删除，而是通过状态字段标记；其中引用句缺失记为$\texttt{ref\_sentence\_found}=\texttt{False}$。

<div class="method-step__io" markdown="1">

**输入**：裁剪图像、匹配图注、从图注解析出的图号，以及论文正文文本。<br>
**输出**：清洗后的“图像—图注—正文引用句”三元组，以及反映抽取完整性的状态信息。

</div>

**直观理解**：图注说明图里有什么，正文引用句通常说明作者为什么使用这张图；把两者同时连接到图像，可减少仅凭图注生成浅层问题的风险。保留失败标记则让使用者能够自行选择严格过滤或尽量保留数据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 问答、问题类型与推理轨迹生成

主路径调用开发期间使用的Gemini模型版本，以图像、图注和引用句为联合条件生成问题、答案，并在可行时生成采用$\texttt{<think>...<\/think><answer>...<\/answer>}$结构的推理轨迹；若API密钥缺失或生成失败，则确定性模板仅依据图注和上下文产生结构有效的问答。每个问题被标为component、relationship、process、result、comparison、architecture或general之一，并记录问答与推理各自来自Gemini还是synthetic回退路径。

<div class="method-step__io" markdown="1">

**输入**：清洗后的图像、图注和正文引用句三元组。<br>
**输出**：带问题、答案、问题类型、可选推理轨迹以及$\texttt{qa\_source}$、$\texttt{cot\_source}$和$\texttt{has\_cot}$等来源或可用性信息的样本。

</div>

**直观理解**：Gemini路径追求更自然、能结合图像内容的问答，模板路径则像备用发电机，保证外部服务失效时流水线仍能产出非空记录。七类标签帮助构造或筛选不同能力测试，例如识别部件、理解连接关系和追踪流程。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。所给章节描述的是数据集构建方法，没有提出需要优化的损失函数或新的模型训练目标；问答与推理轨迹由Gemini辅助生成或由确定性模板构造，而版面检测器仅被说明为已在DocLayNet类别体系上微调的YOLOv8，原文未给出其微调目标、损失公式或本项目中的再训练过程。SCAFFOLD记录可用于视觉语言模型监督微调，其中图像和对话消息可作为输入，答案或带推理结构的目标文本可作为监督输出，但具体如何计算训练损失在所给章节中原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 页面版面检测与源PDF裁剪模块**

该模块将版面定位与内容提取解耦：YOLOv8在150 DPI页面渲染图上依据DocLayNet类别检测Picture和Caption区域，而PyMuPDF使用对应坐标从原始PDF裁剪图表。这样既利用固定分辨率输入稳定检测，又避免直接保存低分辨率页面截图。

> 直观理解：检测用的图片适合“找位置”，原PDF适合“取内容”；让两个工具各做擅长的事，可以同时保持定位一致性和图像清晰度。

**2. 图注匹配与正文引用定位模块**

图注匹配不是简单选择图像正下方最近文本，而是联合考虑图像框与图注框的垂直间距及水平重叠。正文定位则从图注解析图号，归一化多种Figure/Fig.书写形式，并选取正文中首次提及该图号的句子作为$\texttt{ref\_sentence}$；若未命中则保留记录并显式标记。

> 直观理解：这一模块为孤立图像补上两层文字语境：图注给出局部说明，正文引用句给出论文叙述中的作用。显式记录未匹配状态也比悄悄丢弃样本更利于检查数据覆盖率和选择过滤标准。

**3. 双路径问答与推理生成模块**

主路径使用Gemini同时读取图像、图注和正文引用句，生成问答及可用的思维链；回退路径在外部API不可用或失败时，以确定性模板从图注和上下文生成问答。模块分别记录$\texttt{qa\_source}$与$\texttt{cot\_source}$，并通过$\texttt{has\_cot}$指示推理轨迹是否存在，使训练者可以过滤纯Gemini样本、模板样本或仅含推理轨迹的样本。

> 直观理解：双路径设计在“内容丰富”与“流程可靠”之间折中：AI生成更灵活，但依赖外部服务且可能产生错误；模板较机械，却能保证记录结构完整。来源标签让这种差异保持可见，而不是混入数据后无法追溯。

**训练与推理**

就数据生产阶段而言，完整“推理”过程是：输入论文PDF，逐页渲染；检测Picture和Caption区域；回到源PDF裁图并匹配图注；解析图号并检索正文首次引用句；把图像、图注和上下文送入Gemini生成问题、答案与可选推理轨迹，失败时切换到模板；最后写入统一模式并导出检查版和训练版记录。该过程产生29,887幅图，并可进一步形成不同规模的问答对集合。

就下游模型而言，轻量记录已经被格式化为目标视觉语言模型所需的聊天消息结构，因此可直接用于监督微调；完整记录则适合在训练前按照$\texttt{ref\_sentence\_found}$、$\texttt{qa\_source}$、$\texttt{cot\_source}$、$\texttt{has\_cot}$或问题类型进行筛选。论文说明SCAFFOLD-12K用于Qwen2.5-VL-3B-Instruct基线实验，但所给方法与统计章节未提供训练轮数、优化器、学习率、批量大小、目标序列拼接方式或测试时解码流程，因此这些步骤原文未明确报告，不能据此补写。

**复现信息**

复现数据构建所必需的信息包括：数据源为arXiv计算机科学论文PDF；按页处理并以150 DPI渲染；使用在DocLayNet版面类别体系上微调的YOLOv8检测Picture与Caption；使用PyMuPDF从源PDF而非页面栅格图裁剪；用“垂直间距＋水平框重叠”的启发式规则匹配图注；搜索正文中首次提及图号的句子，并兼容Figure 3、Fig. 3和Fig.3等格式；主生成路径在开发期间使用gemini-2.5-flash、gemini-3.1-lite-flash和gemini-3.5-flash，失败时启用确定性模板。

数据规模与解释边界方面，流水线从3,058篇论文中抽取29,887幅图，形成SCAFFOLD-157K的157,387对、SCAFFOLD-37K的36,797对和SCAFFOLD-12K的12,000对；SCAFFOLD-12K划分为10,000条训练记录和2,000条验证记录。原文说明较小版本来自少量完整处理的论文并经过人工抽查，数据说明部分还称人工复核了1,000个样本，但没有给出抽查判定准则、错误率、论文选择规则、启发式阈值、Gemini提示词、各生成模型对应的样本比例或去重办法；这些缺失会影响严格复现与质量比较，应在使用该数据集前通过代码仓库和原始记录进一步核验。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- $SCAFFOLD\text{-}12K$：数据集的小规模版本，实验使用其训练集进行微调，并在匹配的 $2{,}000$ 个样本验证集上评估；其作用是验证数据格式、问答内容和推理轨迹是否足以支持视觉语言模型训练。
- $ChartQA$：面向图表问答的外部基准，包含数值、类别等问题类型；其作用是测试模型对结构化视觉数据和图表答案的迁移能力。
- $DocVQA$：面向文档图像问答的外部基准，包含数值、类别和文本问题；其作用是测试模型能否把论文图示训练所得能力迁移到更一般的文档视觉问答场景。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Numeric accuracy**

衡量模型在数值答案上的正确率，通常比较预测数值与参考数值是否一致或满足规定的容差；它直接反映模型读取和计算图中数字信息的能力。 （越高越好，因为更高表示正确回答的数值问题更多。）

</div>
<div class="metric-item" markdown="1">

**Answer-only ROUGE-L**

只对模型最终答案部分计算基于最长公共子序列的文本重叠分数，不把推理轨迹的文字差异混入评价；它主要衡量答案表述与参考答案的接近程度。 （越高越好，但分数高只能说明文本重叠较好，不能单独证明视觉理解或推理过程正确。）

</div>
<div class="metric-item" markdown="1">

**Format well-formed rate**

衡量输出是否遵循预期的 `<think>` 与 `<answer>` 结构，属于格式合规性指标，而非答案正确性指标。 （越高越好，因为更高表示更多输出能够被下游训练或解析流程直接使用。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### $SCAFFOLD\text{-}12K$ 验证集上的基础微调结果

<div class="result-value" markdown="1">

模型的格式合规率为 $0.995$，数值准确率为 $0.638$，答案部分的 $ROUGE\text{-}L$ 为 $0.419$。

</div>

这说明模型几乎总能输出预期的 `<think>`/`<answer>` 结构，并且在数值问题上取得了相对较好的验证集表现；答案文本与参考答案仍存在明显差异。该结果支持“数据能够被用于监督微调”这一作者主张，但不能证明模型优于其他模型，也不能证明生成的推理轨迹必然忠实于模型的真实决策过程。

<div class="result-source" markdown="1">

来源：Table 6, Baseline fine-tuning results on the Scaffold-12K validation split

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Format well-formed rate
0.995

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### $ChartQA$ 外部基准迁移结果

<div class="result-value" markdown="1">

整体 relaxed accuracy 为 $0.455$，其中数值问题为 $0.500$、类别问题为 $0.270$；answer containment 为 $0.670$。

</div>

模型在图表数值问题上的表现高于类别问题，表明从论文图示中学习到的结构化读图能力可能更适合具有明确数值答案的任务。answer containment 较高说明参考答案常被包含在输出中，但这不等于答案完全匹配，也不能据此断言模型在通用图表问答上具有竞争力，因为原文没有提供其他模型的同条件结果。

<div class="result-source" markdown="1">

来源：Table 7, Benchmark Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ChartQA | relaxed accuracy (overall) | 0.455

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### $DocVQA$ 外部基准迁移结果

<div class="result-value" markdown="1">

整体 relaxed accuracy 为 $0.330$，数值问题为 $0.515$，类别问题为 $0.145$，文本问题为 $0.160$；answer containment 为 $0.505$。

</div>

模型仍然在数值问题上明显好于类别和文本问题，说明跨数据集迁移并不均衡：它可能较容易复用数字读取能力，但对文档中的开放式文字理解和类别判断较弱。该结果只能说明存在一定迁移能力，不能证明 $SCAFFOLD$ 专门训练是唯一原因，因为没有报告未微调模型或其他训练数据的对照。

<div class="result-source" markdown="1">

来源：Table 7, Benchmark Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

DocVQA | relaxed accuracy (overall) | 0.330

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验没有报告真正的消融研究：未比较不同数据规模、是否使用上下文或推理轨迹、不同量化配置，以及 Gemini 生成记录与 synthetic fallback 记录的影响，因此无法判断哪些数据组成部分对性能最关键。
- 比较范围有限且缺少强基线。作者只微调一个 $3$B 级视觉语言模型，未提供未微调模型、其他模型或现有图表问答数据集训练模型的同条件结果；此外，$LLM\text{-}judge$ 只评估了 $73$ 个样本，自一致性只使用 $50$ 个样本，外部基准的完整评估协议在所给章节中未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- $Qwen2.5\text{-}VL\text{-}3B\text{-}Instruct$ 的单一监督微调基线：模型使用 $QLoRA$ 在 $SCAFFOLD\text{-}12K$ 上训练，作为验证数据集可用性的基准，而不是与其他模型进行严格的性能竞争。原文未报告未微调模型、其他视觉语言模型或现有数据集训练模型的对照结果。

**实验想回答的问题**

- 在 $SCAFFOLD\text{-}12K$ 上微调 $Qwen2.5\text{-}VL\text{-}3B\text{-}Instruct$ 后，模型能否学习生成格式正确、内容合理并包含推理轨迹的图表问答输出？
- 该数据集训练出的模型在外部视觉问答基准 $ChartQA$、$DocVQA$ 和 $AI2D$ 上是否表现出可迁移性？

**实验实现**

作者对 $Qwen2.5\text{-}VL\text{-}3B\text{-}Instruct$ 进行监督微调，采用 $QLoRA$，即使用 $4$ 位量化，并在所有注意力层和多层感知机投影层加入秩为 $64$ 的 $LoRA$ 适配器。模型在 $SCAFFOLD\text{-}12K$ 训练集上训练，在匹配的 $2{,}000$ 个验证样本上评估；同时报告了 $ChartQA$、$DocVQA$ 和 $AI2D$ 的结果。作者将该实验定位为数据集和处理管线的可用性验证，而非状态最优比较。外部基准的训练或零样本评估细节、数据划分细节及超参数在所给章节中未完整报告。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文给出了一个跨注意力图的示例记录，而非模型预测案例：问题是“Which component provides the queries in the cross-attention module?”，答案为“The decoder hidden state.”，推理轨迹根据图注和图中箭头判断查询来自解码器隐藏状态、键和值来自编码器分支。该例说明记录同时保留图像、图注、上下文、问题、答案和推理轨迹，能够表达组件来源与关系；但它不能替代系统性的定性错误分析，也不能证明所有自动生成样本都同样可靠。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Provides a large-scale diagram question-answering dataset with chain-of-thought traces for training and evaluating visual reasoning.; rule check: matched taxonomy keywords; top rule score=5.0
- 全文指纹：`824f4cc74039169dfbfa146cfa56525c571df869298af6f4d638fadfba26de32`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
