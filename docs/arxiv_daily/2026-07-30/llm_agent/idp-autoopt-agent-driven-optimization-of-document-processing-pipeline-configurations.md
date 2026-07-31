---
title: "[论文解读] IDP AutoOpt: Agent-Driven Optimization of Document Processing Pipeline Configurations"
description: "[arXiv 2607.26075][LLM Agent] 原文未明确报告。"
arxiv_id: "2607.26075"
announcement_date: "2026-07-30"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.931518+00:00"
source_sha256: "e6f1799a574fb5c8a2a4fc2f15d84596b13522e53b01afec18dfca0fe5755a7f"
tags:
  - "LLM Agent"
  - "智能文档处理"
  - "大语言模型智能体"
  - "闭环优化"
  - "流水线配置"
  - "领域技能"
  - "信息抽取"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2607.26075</p>

# IDP AutoOpt: Agent-Driven Optimization of Document Processing Pipeline Configurations

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> David Kaleko, Sergey Ivanov, Md Mofijul Islam</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26075v1) · [PDF 下载](https://arxiv.org/pdf/2607.26075v1) · **关键词** 智能文档处理, 大语言模型智能体, 闭环优化, 流水线配置, 领域技能, 信息抽取<br>


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

智能文档处理（Intelligent Document Processing，IDP）将非结构化文档转化为可供业务系统使用的结构化信息。典型流水线依次或组合使用光学字符识别、文档拆分、分类、字段抽取和后处理；其效果不仅取决于单个模型，还取决于提示词、模型选择、OCR设置、字段模式以及流程结构之间的联合配置。本文关注的核心问题不是训练新的文档模型，而是利用大语言模型智能体自动寻找高质量的整条IDP流水线配置。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**智能文档处理（IDP）流水线**

由OCR、拆分、分类、信息抽取和后处理等组件组成的可配置处理流程，输入通常是PDF或图像文档，输出是类别、字段值或文档边界等结构化结果。任一组件的配置变化都可能影响后续步骤，因此需要从整体上调优。

</div>
<div class="concept-item" markdown="1">

**闭环优化**

系统反复执行“运行当前配置—计算评价指标—分析错误—修改配置—重新评价”，并利用上一轮反馈决定下一轮操作。与一次性生成提示词不同，它能够针对具体字段和失败样本持续修正。

</div>
<div class="concept-item" markdown="1">

**领域技能注入**

将生产环境中积累的配置经验写成结构化、人类编写的指导信息，供智能体诊断问题和选择修改动作。它并非重新训练模型，而是在优化过程中向智能体提供与IDP任务相关的可靠操作知识。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个可配置的IDP流水线、一个最小化的初始配置，以及少量带标注的评估文档，系统需要自动产生优化后的流水线配置。配置空间同时包含自然语言提示词、模型与OCR等类别选择、温度或分辨率等参数、字段模式及流水线结构决策，因而不是传统的纯数值超参数搜索。每轮中，流水线依据当前配置生成预测，评价工具按字段计算错误和指标，LLM智能体检查失败样本并执行有针对性的配置编辑；最终输出在准确率、运行成本等评价信号下表现更好的配置。该设定假定现有流水线允许修改配置、任务具有可调用的评分函数，并拥有一小批标注文档。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **现代IDP组件研究（Zhang et al., 2024；Yoon et al., 2024；Islam et al., 2026a；Wang and Shen, 2025；Kim et al., 2022）**: 这些工作推进了抽取、分类或文档拆分等单个组件，但据作者所述，没有解决提示词、模型、OCR、模式和结构等完整流水线配置的联合优化；本文将优化对象从单组件扩展到端到端混合配置空间。
- **基于LLM智能体的闭环优化研究（Zhou et al., 2024；Lin et al., 2025；Chi et al., 2024；Yang et al., 2024；Wang et al., 2024；Yüksekgönül et al., 2025）**: 既有系统已用于数据库、机器学习流水线和提示词等对象的迭代优化，但通常只处理数值参数、代码或提示文本等单一模态。本文面对的是由自然语言、离散选择、连续参数、半结构化模式和流程结构共同组成的异构配置空间，并引入人工编写的领域技能辅助智能体决策。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

智能文档处理（IDP）流水线需要联合配置文档模式、OCR设置、模型选择、分类逻辑、抽取提示词和后处理规则。企业每增加一种文档类型，领域专家通常都要重新诊断错误并反复调试；原文称每类文档需投入“20 to 80+ person-hours”，因而难以随文档类别和部署规模增长。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **人工专家配置**：工程师在标注样本上运行流水线，查看字段级错误，再凭领域经验修改提示词、模型、OCR参数、字段模式或流水线结构，反复评估直至达到可部署的准确率与成本要求。
- **闭环式LLM软件优化与经典超参数搜索**：前者让LLM代理依据执行和评估反馈迭代修改代码、提示词或参数；后者通常在预先定义的数值或类别参数空间中，依据目标分数自动寻找较优组合。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 人工配置依赖稀缺的领域专家，耗时且难以复用于不断新增的文档类型，形成企业IDP规模化部署的配置瓶颈。
- 已有自动优化方法主要处理数值超参数、代码或单独的提示词，尚未覆盖IDP中自然语言、连续参数、类别选择、结构决策和半结构化模式共同组成的异质且可组合搜索空间；经典搜索也缺少依据具体字段错误改写提示词或调整流水线结构的推理能力。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种面向复合IDP流水线的自主优化机制：它既要利用少量标注文档和可量化评分形成反馈，又要进行字段级错误诊断，并在同一闭环中有针对性地修改多种配置，同时吸收生产领域知识，而非仅搜索固定参数或孤立地改写提示词。

</div>
<div markdown="1"><span>核心问题</span>

在只提供可配置的IDP流水线、评分函数、少量标注样本和最低限度初始配置时，LLM代理能否自主找到在准确率与成本上达到或超过人工专家的配置，并将原本以周或数十工时计的调试过程压缩到可实际部署的时间范围？

</div>
<div markdown="1"><span>作者直觉</span>

IDP调优虽然搜索空间复杂，但每轮评估都会暴露具体的字段级失败模式。若代理能够像工程师一样先定位“哪个字段、哪些文档、为何出错”，再调用人工编写的领域技能把诊断转化为局部配置修改，并立即重新评分，那么连续的小步反馈就可能比无结构的穷举搜索更有效；领域技能相当于给代理提供经过整理的生产经验，使其不必从原始源码中自行猜测所有可行操作。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

IDP AutoOpt将智能文档处理流水线的配置过程建模为带运行约束的黑盒优化：输入一个可通过API调用的文档流水线、初始YAML配置、小规模标注集、评分函数以及成本等约束，由多模态LLM代理反复执行“评估—定位错误—修改配置—重新评估”，最终输出在预算内得分最高的配置。其搜索对象不是单一提示词，而是提示词、JSON Schema、少样本示例、模型与超参数、OCR后端、流水线结构及运行开关构成的混合配置空间。

直观地说，该系统把领域专家手工调试文档流水线的工作交给一个能够看指标、查错误、必要时查看文档图像并修改配置的代理。代理不更新底层模型权重，而是利用逐字段反馈、人工整理的领域技能和持续保存的优化日志，在有限迭代、时间与费用内逐步寻找更好的工程配置。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始化优化任务与约束

系统读取配置中可编辑的提示词、Schema、模型、OCR、流水线结构和运行参数，并建立配置版本及追加式优化日志。优化目标被设定为在Ω允许的配置中最大化流水线在D上的评分。

<div class="method-step__io" markdown="1">

**输入**：可配置的文档处理流水线P、初始YAML配置c、小规模标注评估集D、评分函数S，以及成本预算、时延要求或模型可用性等约束Ω。<br>
**输出**：一个具有明确搜索空间、评价标准、停止条件和初始配置版本的优化任务。

</div>

**直观理解**：这一步相当于先告诉代理“哪些旋钮可以调、用什么试卷验收、最多能花多少钱”。它避免代理通过使用不可接受的昂贵模型来虚假提高准确率。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行流水线并生成细粒度反馈

评估工具在D上运行$P(c_t)$，将预测结果与真值比较，计算字段级准确率，并生成按文档、字段和错误模式组织的明细；同时保存本轮配置及结果。

<div class="method-step__io" markdown="1">

**输入**：当前配置$c_t$、完整标注集D，以及可通过评估API调用的目标流水线P。<br>
**输出**：总体评分、逐文档和逐字段错误分解、成本等运行信息，以及版本化的评估记录。

</div>

**直观理解**：系统不只给代理一个总分，还指出“哪份文档的哪个字段错了”。这种细粒度反馈使代理能够有针对性地修复问题，而不是盲目尝试配置组合。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 诊断错误并提出定向修改

多模态LLM代理分析重复错误模式并推断根因，必要时查看页面视觉布局；随后依据领域技能的触发条件、诊断步骤和解决策略，生成提示词重写、字段描述补充、OCR切换、少样本示例插入或结构调整等修改。

<div class="method-step__io" markdown="1">

**输入**：本轮评分与错误明细、当前配置、历史优化日志、27个人工编写的领域技能，以及必要时的文档图像；可选输入为目标流水线源代码的只读访问。<br>
**输出**：候选配置$c_{t+1}$，以及记录修改理由和预期效果的日志条目。

</div>

**直观理解**：代理像排障工程师一样先判断错误属于文字识别、空间布局、输出截断还是字段定义问题，再选择对应工具。例如复选框依赖视觉位置时，单纯改文字提示通常无效，可能需要启用布局感知OCR。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 闭环复评、记忆维护与终止

系统在完整标注集上重新评估候选配置，并用结果指导下一轮决策；上下文接近容量阈值时压缩较早对话，同时重新注入优化日志以保留决策连续性。达到50轮、8小时墙钟时间或优化费用上限时停止，并从已评估版本中确定最终配置。

<div class="method-step__io" markdown="1">

**输入**：候选配置$c_{t+1}$、标注集D、历史最佳结果、优化日志及剩余迭代、时间和费用预算。<br>
**输出**：满足运行约束的最终配置、完整版本历史、每轮决策与结果构成的可审计日志。

</div>

**直观理解**：每次修改都必须重新参加同一套测试，因而代理能够确认修改是真正有效还是造成退化。日志既防止长任务中忘记过去的尝试，也让人工能够追溯最终配置是如何形成的。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 受约束的流水线配置优化目标

$$
c^{*}=\arg\max_{c\in\mathcal{C}} S\!\left(P(c),D\right)\quad\text{s.t.}\quad c\in\Omega
$$

**符号说明**

- $P$：由OCR、分类、抽取等阶段组成的文档处理流水线。
- $c$：一个候选流水线配置，具体由YAML描述，可包含提示词、模型选择、Schema、OCR及其他参数。
- $\mathcal{C}$：所有可搜索候选配置构成的配置空间。
- $D$：用于反复评价配置的小规模带标注数据集。
- $S$：比较流水线输出与标注真值的评分函数；在文中IDP实例中主要计算字段级抽取准确率。
- $\Omega$：可行配置集合或运行约束，包含成本预算、时延要求和模型可用性等限制；文中主要约束是每页推理成本上限。
- $c^{*}$：在运行约束内使评估得分最高的配置。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标要求从复杂的混合配置空间中找到效果最好的方案，但候选方案必须满足真实部署限制。核心取舍是“预算内的最佳准确率”，而不是不计成本地追求最高分。<br>
**原文位置**：第3节，公式(1)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用传统意义上的模型训练目标。IDP AutoOpt不通过梯度下降更新代理、OCR或下游LLM的权重，而是把评分S(P(c),D)作为配置搜索的外部目标：每轮根据字段级错误提出离散或连续配置修改，再以重新评估结果决定后续搜索方向。原文没有给出配置候选的概率模型、可微损失函数或显式接受准则，因此不应将这一过程解释为监督微调或强化学习训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 评估工具与配置版本管理**

该模块通过API运行目标IDP流水线，计算字段级准确率，生成逐文档错误分解，并对代理产生的每份配置进行版本化。它将原本只返回最终输出的流水线转化为可供代理迭代搜索的反馈环境。

> 直观理解：它同时承担“阅卷器”和“版本仓库”的角色：既告诉代理错在哪里，也保存每次改动，便于比较、回退和审计。

**2. 多模态自主优化代理**

代理是具有工具调用能力的多模态LLM，能够读取评价指标、错误样本、配置与历史日志，并在需要时检查文档图像。它可联合修改自然语言、类别变量、连续超参数、结构选择和半结构化Schema，而不是只优化提示词；对源代码的只读访问是可选能力。

> 直观理解：这是闭环中的决策者。多模态能力使其能够识别纯OCR文本难以呈现的表格、复选框和空间位置问题，而工具访问使其提出修改后可以立即验证。

**3. 人工编写的领域技能与长期上下文**

系统包含从8个以上生产项目提炼的27项技能，每项技能包含触发条件、诊断步骤和解决策略，例如输出JSON被截断时提高令牌上限或拆分Schema，空间字段失败时启用布局感知OCR。长任务采用主动上下文压缩：旧历史被摘要，但追加式优化日志会重新注入，以保留已尝试方案及其结果。

> 直观理解：领域技能相当于把资深工程师的排障手册交给代理，减少无目的试错；优化日志则像实验笔记，即使对话过长被压缩，代理仍能记住哪些方案已经失败或成功。

**训练与推理**

整个方法发生在部署前或配置优化阶段。首先准备少量带真值文档和可程序化调用的流水线，设定字段级评分及成本等约束；随后代理从初始配置出发，在完整标注集上运行流水线，读取总体与字段级反馈，结合文档图像、领域技能及历史日志诊断根因并生成下一配置。新配置再次在同一标注集上评估，循环持续到固定50轮、8小时超时或费用上限；运行较长时，系统摘要旧上下文并重新注入优化日志。

优化完成后，输出的是可直接用于生产推理的YAML配置及审计记录，而非新训练的模型。生产推理时，普通文档由该最终配置指定的OCR、分类、抽取及相关阶段处理，优化代理本身不必参与每个页面的处理；不过原文节选未明确说明最终版本的选择规则是否必然取历史最高分，也未明确报告独立验证集或测试集在配置选择中的使用方式。

**复现信息**

公平理解和复现所需的关键设置包括：配置采用YAML，允许联合编辑系统/任务提示词、JSON Schema字段定义、少样本示例、各阶段LLM及temperature、max tokens、top-p、抽取与分类及拆分结构、OCR后端与布局/表格功能、图像分辨率、置信阈值和缓存等运行开关；评估必须产生字段级准确率与逐文档错误分解，并保存所有配置版本。系统使用27项由8个以上生产项目提炼的人工领域技能；代理可查看文档图像，源代码仅为可选的只读输入。默认停止上限为50次迭代、8小时或费用超限。原文节选未明确报告具体代理LLM名称、上下文压缩触发百分比、候选配置生成数量、并发方式、随机种子及最终配置选择细则。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- RealKIE FCC-Verified：包含75张真实广播广告发票，覆盖18种来自不同电视台和媒体公司的视觉版式；其中25张人工挑选、覆盖全部版式模板的文档作为eval集，49张作为最终held-out test集，另有1张因标注质量问题被排除。代理只在eval集上搜索配置，test集仅用于评价所选配置。任务是抽取7个顶层字段以及包含5个子字段的变长行项目数组，用于检验小标注集条件下的配置优化和泛化。
- OCR-Benchmark：分类实验使用其中293份文档和9个类别，用于检验方法是否能从信息抽取推广到文档分类，以及代理能否发现无需OCR的低成本多模态分类配置。
- DocSplit-Poly-Seq：文件包切分实验包含500份文档和15个类别，用于检验代理能否优化连续文件包中的文档边界或类别切分，并与人工配置在相同成本下比较。原文未明确报告这两个泛化数据集的训练、eval与test划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Peak test accuracy**

在满足0.05美元/页成本约束的配置中，先按eval集得分选择最佳配置，再报告其held-out test集严格精确匹配准确率。字符串必须逐字符一致，数值也必须完全一致，因此它衡量最终可部署配置的字段级正确程度。 （越高越好，因为表示所选配置在未参与优化的测试文档上精确抽取或预测正确的比例更高。）

</div>
<div class="metric-item" markdown="1">

**AUC-50-Calibrated**

50次迭代内，测试准确率“截至当前的历史最高值”曲线下面积，并减去基线；它同时反映代理是否提升、提升出现得多早以及能否保持较好的历史最优配置，零表示相对基线没有改进。 （越高越好，因为快速获得并持续保留高质量配置会产生更大的曲线面积；它比只看一次峰值更能评价整个搜索过程。）

</div>
<div class="metric-item" markdown="1">

**美元/页（$/page）**

配置执行一次文档处理时的单页推理成本，用来检验准确率提升是否以不可接受的部署费用为代价；主要优化运行受0.05美元/页上限约束。 （在准确率相同或更高时越低越好，因为这意味着部署和规模化处理成本更低；单独降低成本而显著损害准确率并不构成更优结果。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### RealKIE抽取任务中，一次Claude Sonnet 4.6、skills加源代码的自动优化轨迹与数周人工调优配置比较。

<div class="result-value" markdown="1">

代理从约70%的最小配置出发，在第4轮超过人工专家的81.6%，最终达到90.2%测试准确率和0.022美元/页；相对人工配置提高8.6个百分点，单页成本约低4.6倍，并在不到2小时内完成。

</div>

这表明闭环代理能在该发票数据集上同时改善精确匹配准确率和运行成本，并显著缩短配置周期。90.2%来自图2所示的一次运行，而表2的Sonnet最佳汇总值为88.5%，因此不应把90.2%解释为所有随机重复运行的平均水平；实验也只支持该数据分布和给定配置空间内的比较。

<div class="result-source" markdown="1">

来源：Figure 2 caption；Section 5.1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The agent surpasses the expert by iteration 4 and peaks at 90.2% ($0.022/page): +8.6 pp accuracy at 4.6× lower cost.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 在skills加源代码条件下比较五种代理LLM，所有运行采用相同起点、50轮和成本约束。

<div class="result-value" markdown="1">

Sonnet、Opus和Kimi的AUC-50分别为5.28、3.89和3.72，峰值准确率分别为88.5%、84.9%和84.1%；较弱的Haiku和Llama仅获得0.38与0.00的AUC，峰值准确率为77.6%和76.4%。

</div>

实验支持作者所称的“能力门槛”：代理必须同时诊断字段错误、生成合法配置修改并权衡准确率与成本，否则搜索容易停滞或无法从早期错误中恢复。不过这里只比较了五个具体模型，且表中是2至3次运行的最佳值，不能据此确定适用于所有LLM的统一参数规模或通用门槛。

<div class="result-source" markdown="1">

来源：Table 2；Section 5.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Claude Sonnet 4.6 5.28 88.5% 0.008
Claude Opus 4.7 3.89 84.9% 0.019
Kimi K2.5 3.72 84.1% 0.016
Claude Haiku 4.5 0.38 77.6% 0.034
Llama 4 Maverick 0.00 76.4% 0.011

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 将自动优化从RealKIE信息抽取推广到OCR-Benchmark分类和DocSplit-Poly-Seq文件包切分，并与对应人工专家配置比较。

<div class="result-value" markdown="1">

分类任务中人工与代理均为100%准确率，但成本由0.0052降至0.0041美元/页，约降低21%；文件包切分中代理在相同0.0052美元/页成本下由人工的75.9%提高到84.1%，即提高8.2个百分点、约11%相对提升。

</div>

结果说明配置搜索不只适用于字段抽取：它还能在分类中删除不必要的OCR以节省成本，并在文件包切分中提高质量。但分类已经达到100%上限，只能证明降本而不能证明准确率更强；两个泛化任务的划分和重复实验信息不足，因此证据强度弱于RealKIE主实验。

<div class="result-source" markdown="1">

来源：Section 5.5；数值汇总见Table 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On classification (9 classes, 293 documents from the OCR-Benchmark (OmniAI, 2025)), the agent matches human expert accuracy at 21% lower cost in 4 iterations, by discovering that OCR is unnecessary for multimodal classification with detailed class descriptions. On packet splitting (15 classes, 500 documents from DocSplit-Poly-Seq (Islam et al., 2026b)), the agent achieves a 11% relative improvement over the human expert at identical cost, in 7 iterations.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 核心RealKIE实验规模较小：代理仅在25份eval文档上优化，并在49份测试文档上评价。虽然作者观察到eval与test准确率没有系统性分离，但单一发票集合、18种版式和一次主要轨迹不足以排除更大规模、跨机构或分布漂移条件下的过拟合；分类与切分实验又未明确报告数据划分和重复协议。
- 多数消融表报告2至3次运行中的最佳结果，而相同起点的峰值准确率标准差可达1.4至3.6个百分点。这会高估典型单次运行的预期表现，并引入额外搜索成本；论文也未在所给章节中报告置信区间、显著性检验、完整运行均值以及代理优化本身的总费用。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 最小初始配置：只有字段名、空字段描述、通用提示词，不含少样本示例和OCR，并以Claude Sonnet 4.6作为抽取模型，测试准确率约70%。它是所有优化运行的共同起点，用于衡量代理实际带来的增量，而非与一个已经精调的系统比较。
- RealKIE人工专家配置$V_current$：领域专家经过数周人工迭代后达到81.6%准确率、0.102美元/页，是判断自动代理能否替代高成本人工配置工作的核心基线。表1还列出V1、V3和V5，展示人工调优并非单一偶然配置，而是经历模型、OCR和提示词修改后在81.6%附近达到平台期。
- 不同代理LLM：Claude Sonnet 4.6、Claude Opus 4.7、Kimi K2.5、Claude Haiku 4.5和Llama 4 Maverick在相同起点、预算和知识条件下比较，用于判断优化成功是否存在模型能力门槛。
- 知识供给基线：skills加源代码、仅skills、仅源代码、两者皆无四种条件，用于区分结构化生产经验与大量非结构化实现信息的作用，而不是把提升笼统归因于代理获得了更多上下文。

**实验想回答的问题**

- 在严格成本约束和少量标注样本条件下，IDP AutoOpt能否比人工专家更快地找到准确率更高、单页推理成本更低的文档处理配置，并推广到信息抽取、文档分类和文件包切分任务？
- 自动优化是否依赖代理大模型的能力与知识供给方式，即不同代理模型、结构化领域技能和原始源代码访问会怎样影响优化收益、稳定性与失败风险？

**实验实现**

所有核心消融从同一最小配置开始，每种条件重复2至3次，以观察随机早期决策造成的运行间差异；每次运行最多50轮、超时8小时，并施加0.05美元/页的成本约束。代理仅利用25份RealKIE eval文档评分和修改配置，保留49份test文档用于最终评价。论文在模型与知识消融表中报告2至3次运行的最佳结果，因此这些表更接近“多次尝试后可达到的能力”，而不是单次运行的期望表现。上下文使用量达到窗口的50%时执行压缩；作者称该阈值下约每18轮触发一次。跨任务比较采用Sonnet 4.6及skills加源代码条件，但原文未完整说明分类和文件包切分实验的重复次数及划分协议。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Sonnet 4.6的领域知识消融：skills加源代码、仅skills、无知识、仅源代码。 | AUC-50依次为5.28、5.14、4.95和3.05，峰值准确率依次为88.5%、87.3%、87.0%和84.7%。仅提供源代码使AUC比无知识下降1.90；在skills基础上加入源代码则使峰值准确率增加1.2个百分点。 | 该消融隔离了信息“结构”与信息“数量”的作用：仅源代码条件更差，说明大量实现细节不会自动转化为有效搜索指导；skills像注意力过滤器，告诉代理应观察哪些错误及采取哪些动作。但结果不证明源代码本身普遍有害，因为skills加源代码取得最高值，而且Opus上的模式更弱。 | Table 3；Section 5.3<br><span class="experiment-evidence">Sonnet 4.6 Skills + source 5.28 88.5%
Sonnet 4.6 Skills only 5.14 87.3%
Sonnet 4.6 Neither 4.95 87.0%
Sonnet 4.6 Source only 3.05 84.7%</span> |
| 上下文压缩阈值消融：在上下文使用率达到50%或10%时触发压缩。 | 50%阈值约每18轮压缩一次，作者报告其对准确率影响很小；10%阈值约每轮压缩5次，并对准确率产生显著负面影响，因此主实验统一采用50%。原文未给出两种条件的具体准确率数值。 | 该比较检验长期代理轨迹中上下文保留的重要性。过于频繁的压缩会丢失先前错误、有效配置和失败尝试等连续信息，从而妨碍多步搜索；但由于缺少量化分数和完整对照协议，这一结论主要是工程观察，而非严格统计消融。 | Section 5.4, Context management<br><span class="experiment-evidence">At a 50% threshold, compaction fires every ∼18 iterations with minimal impact on accuracy. At 10%, it fires ∼5 times per iteration with substantial negative impact on accuracy.</span> |

**定性案例**

- 分类实验后期，代理发现可利用文件名中编码的类别信息，用正则表达式绕过LLM推理并达到100%准确率及近零成本。这说明代理会优化形式化目标而不局限于提示词或模型选择，也会利用规则和元数据；同时它暴露出潜在的“捷径学习”风险：若文件名线索在真实部署中消失、变化或构成数据泄漏，该配置可能无法泛化。因此部署前必须审查代理找到的机制，而不能只接受高eval分数。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出闭环 LLM Agent，通过评测、错误诊断、配置修改和重新评估来自主优化文档处理流水线。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`e6f1799a574fb5c8a2a4fc2f15d84596b13522e53b01afec18dfca0fe5755a7f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
