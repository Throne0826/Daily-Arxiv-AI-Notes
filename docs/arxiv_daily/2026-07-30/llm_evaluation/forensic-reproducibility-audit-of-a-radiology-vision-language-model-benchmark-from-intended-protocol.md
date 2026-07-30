---
title: "[论文解读] Forensic Reproducibility Audit of a Radiology Vision-Language Model Benchmark: From Intended Protocol to Released Artifact"
description: "[arXiv 2607.25589][LLM 评测] 本文通过对一个已归档的胸部X线视觉—语言模型基准进行取证式复现审计，揭示从预定实验协议到公开发布物之间的多层偏差，并提出可由机器检查的基准契约。"
arxiv_id: "2607.25589"
announcement_date: "2026-07-30"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:25.777691+00:00"
source_sha256: "92d60b674d1405eda4f854d3b5bbdeb8cc564c494a25f0fc7dcec9afe37c6997"
tags:
  - "LLM 评测"
  - "多模态 VLM"
  - "医学影像人工智能"
  - "视觉—语言模型"
  - "胸部X线"
  - "可复现性审计"
  - "DICOM渲染"
  - "提示词溯源"
  - "工件一致性"
  - "研究完整性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2607.25589</p>

# Forensic Reproducibility Audit of a Radiology Vision-Language Model Benchmark: From Intended Protocol to Released Artifact

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Mateusz Kozłowski</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.25589v1) · [PDF 下载](https://arxiv.org/pdf/2607.25589v1) · **关键词** 医学影像人工智能, 视觉—语言模型, 胸部X线, 可复现性审计, DICOM渲染, 提示词溯源, 工件一致性, 研究完整性  
**项目页**: [https://doi.org/10.5281/zenodo.21629849](https://doi.org/10.5281/zenodo.21629849)  

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

本文通过对一个已归档的胸部X线视觉—语言模型基准进行取证式复现审计，揭示从预定实验协议到公开发布物之间的多层偏差，并提出可由机器检查的基准契约。

**不用术语来说**：医学影像基准的最终结论来自一条很长的处理链：选择病例、把DICOM影像渲染成模型可见的图像、绑定提示词和模型、保存输出、把自由文本转成标签、执行统计检验，再将结果同步到论文和代码仓库。即使某张结果表可以重新算出，只要其中任何环节使用了错误的提示词、像素、病例或标签，该数字就不再代表论文声称测试的条件；传统的结果复算往往发现不了这种“算得对但测错了”的问题。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者对一个保留的胸部X线VLM试验快照及其公开仓库进行了端到端取证审计，在不重新调用模型、不新增影像或报告标注的前提下，追踪提示词绑定、DICOM渲染、患者与队列身份、输出完整性、自动标签提取、配对统计及发布传播，形成了从实验意图偏离到结论失效的可核查证据链。
- 作者据审计中观察到的故障类型提出基准契约，将队列成员、渲染图像与提示词哈希、服务商解析后的模型身份、调用状态、标注来源、按键对齐的统计分析及衍生产物检查纳入机器可验证控制；但作者明确说明，该完整契约尚未经过前瞻性验证。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

医学影像视觉—语言模型（VLM）基准通常不是单一程序，而是一条跨越数据选择、DICOM影像渲染、提示词与模型接口调用、自由文本标签提取、统计检验以及论文和代码仓库发布的测量链。研究结论成立的前提不仅是统计计算无误，还要求链中各工件准确对应同一实验条件，例如患者与检查的抽样单位一致、模型实际看到的像素经过正确渲染、调用使用了声明的提示词和模型版本、缺失输出得到一致处理、自动标签可验证，并且论文表格与公开仓库同步更新。本文关注这种跨工件一致性：即使某张结果表在算术上可以复现，只要执行条件与报告协议不符，它也不能支持原先声称的模型性能、排名或提示词效应。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**视觉—语言模型（Vision-Language Model, VLM）**

能够联合处理图像与文本输入并生成文本等输出的模型；在本文场景中，模型接收胸部X线影像和提示词，输出自由文本报告。审计检查的是这些历史调用及其工件，而不是重新评价或调用模型。

</div>
<div class="conceptitem" markdown="1">

**DICOM渲染与MONOCHROME1**

DICOM是医学影像及其元数据的标准格式，原始像素必须依据头信息正确转换为模型可见图像。MONOCHROME1规定较小像素值应显示得更亮，因此遗漏极性反转会使明暗关系颠倒，改变模型实际接收的视觉输入。

</div>
<div class="conceptitem" markdown="1">

**配对统计分析**

当同一病例—征象单元接受多个模型或提示条件时，各条件结果相互对应，分析必须使用共同且键值一致的完整观测。Cochran's Q用于比较多个配对二元条件，McNemar检验用于两个配对二元条件，Holm校正用于控制多重比较造成的假阳性累积。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文执行回顾性取证式可复现性审计，输入是一个已保存的胸部X线VLM试验本地快照及其公开仓库记录，包括预定调用、实际提示绑定、DICOM头信息、患者别名、模型生成报告、自动标签、统计代码、论文、图表、投稿包和发布工件。审计逐项追踪计划与执行是否一致，核对非空输出和患者/检查单位，检查影像渲染与标签提取路径，并按显式的“病例—征象”键重建配对分析；输出是已识别的协议偏差、可复算但适用条件受限的统计结果、原有科学主张是否仍可识别，以及用于约束队列、图像、提示词、模型身份、调用状态、标注来源和派生工件的机器可验证控制。该任务的审计单位是工件或科学主张，而非患者临床结局；研究不重新调用模型，也不新增影像或报告标注，因此只能判断存档证据支持什么，不能恢复原本未被正确执行的提示词比较，更不能据此确立临床性能。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$(\mathrm{case},\mathrm{finding})$**

病例与影像征象组成的显式复合键，用于确保不同模型或提示条件下的二元标签在同一分析单元上正确配对。

</div>
<div class="notationitem" markdown="1">

**$Q$**

Cochran's Q检验统计量，用于比较三个或更多相关二元条件；其数值依赖共同完整的配对分析队列。

</div>
<div class="notationitem" markdown="1">

**$p$**

统计检验在零假设下得到当前或更极端结果的概率；文中以未校正的p值及Holm多重比较校正后的结果区分名义显著性与校正后显著性。

</div>

</div>

**直接相关的工作**

- **2024年《Checklist for Artificial Intelligence in Medical Imaging》更新版**: 该报告规范要求明确披露数据选择、预处理、参考标准、数据划分、缺失情况、软件和统计分析，为本文审计测量链中的报告完整性提供背景；本文进一步直接核验已发布工件是否与所述协议一致。
- **放射学大型语言模型报告指南（原文节选未给出具体名称）**: 该类指南强调精确记录提示词、采样设置、模型版本和专家相关信息；本文把这些报告要求扩展为可追踪、可机器核验的提示绑定、模型身份及调用状态控制。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

医学影像AI基准同时依赖数据集、DICOM处理、提示词、第三方模型API、自动标签器、统计代码、论文和仓库发布物。研究者通常默认这些对象彼此一致，但任一层发生静默偏差，都可能使性能、模型排名、提示词效应乃至临床安全结论失去对应的真实实验条件，而且错误还可能继续传播到图表、投稿包和公开归档中。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **报告清单与领域报告规范**：现有医学影像AI及放射学大模型指南要求作者披露数据选择、预处理、参考标准、数据划分、缺失值、软件与统计方法，并记录精确提示词、采样设置和模型版本，以提高研究过程的透明度。
- **数值复现与常规代码核查**：研究者依据保存的输出、标签矩阵和分析代码重新运行统计过程，检查表格中的统计量和显著性结果能否由现有制品重复得到。这类方法主要验证计算过程是否自洽。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 报告规范主要要求研究者说明做了什么，却不自动验证声明与实际执行是否一致；因此，被标记为不同条件的调用仍可能绑定同一提示词，过期模型名称和旧结果也可能在论文修订后继续留在仓库中。
- 仅复算统计量只能证明归档数据上的算术可重复，不能证明输入像素、队列、提示词、模型身份和标签生成过程符合预定协议。本文案例中，即使修正配对分析后得到可复现数字，错误提示词绑定、MONOCHROME1极性处理缺失、数据划分丢失及未经验证的截断式标签提取仍使目标提示词比较无法恢复。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有实践缺少一种跨越数据、像素、模型调用、标注、统计和发布层的端到端核验机制，能够区分“结果可由归档制品重新计算”与“归档制品确实实现了论文声称的实验”，并在发布前自动暴露实验身份和制品传播的不一致。

</div>
<div markdown="1"><span>核心问题</span>

一个已归档的胸部X线VLM试验在哪些环节偏离了其报告协议，这些偏差如何影响原有科学主张的可识别性，以及哪些机器可验证控制能够检测相同类型的失败？

</div>
<div markdown="1"><span>作者直觉</span>

作者把审计单位从患者结局转向“制品或科学主张”，沿每项结论的生成链反向追踪其病例键、像素、提示词、模型调用、标签和统计输入。直观上，若每一层都保存稳定身份并通过哈希、状态记录和显式键连接，系统就能在数字进入论文之前发现条件错绑、样本错位、输出缺失或旧文件未更新，而不是等到最终表格出现明显算术错误。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是训练或重新评测一个放射学视觉—语言模型，而是对一个已保存的胸部X线VLM试点进行回顾性法证式可复现性审计。审计将基准结果拆成“预期、执行、观测、分析、报告、发布”六种状态，分别检查协议设想、实际请求字节与模型端点、保存的响应、进入统计分析的数据、论文中的陈述以及读者能够下载的归档物；全过程不重新调用模型，也不新增图像或报告标注。核心原则是：每一种主张都必须由与其状态相匹配的证据支持，并在提示词、图像、输出、统计配对和发布物之间保持可核验的身份链。
端到端上，作者先冻结历史项目范围和审计单位，再通过运行时绑定、DICOM属性与渲染代码、响应文件字节、显式科学键及归档包内容重建各状态；随后用校验和与语义不变量检查状态转换是否一致，并按“可直接纠正、只能描述性重建、无法由再分析修复”的边界处理发现的问题。通俗地说，这一方法不是只检查最终分数算得对不对，而是沿着“实验计划—实际调用—输出保存—统计计算—论文展示—公开发布”的整条流水线逐站验货。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 冻结审计范围并建立六状态证据框架

把每项计算结果映射到预期、执行、观测、分析、报告和发布六种状态，并为各状态指定优先证据：例如协议说明预期，运行时绑定说明实际提示词，文件字节说明响应是否存在。不同状态的材料不得相互替代。

<div class="method-step__io" markdown="1">

**输入**：保存下来的项目状态，以及协议、源文件、运行记录、分析代码、论文源文件和公开归档包等历史材料。  
**输出**：按结果和状态组织的审计证据链，以及每项主张应接受何种材料验证的判定规则。

</div>

**直观理解**：类似调查产品事故时分别核对设计图、生产日志、成品、质检表、广告和售出版本，而不是看到最终说明书就假定此前各环节都一致。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 重建提示词、模型与图像的执行身份

以实际请求文本而非变量标签判定提示词身份，并将图像身份同时约束为选中的检查、规定视图和实际渲染像素；校验和用于判断字符串或派生文件是否逐字节相同。对于模型身份，方法要求以解析后的模型ID和执行路径作为请求侧证据。

<div class="method-step__io" markdown="1">

**输入**：预期提示词、源代码中的提示词定义、实际请求文本与运行时绑定、模型端点信息、所选检查及视图、DICOM属性、渲染代码和渲染后图像。  
**输出**：逐次调用的提示词—模型—图像身份映射，以及标签与实际内容不一致、视图或渲染不合规等偏差记录。

</div>

**直观理解**：文件名写着“提示词A”并不能证明里面真的用了A；必须打开实际寄出的请求，并确认模型看到的是哪张、以何种方式显示的图像。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 核验响应保存、标签提取与分析配对

用原始文件字节判定输出是否真实存在和非空，而不只依赖成功状态字段；随后检查自动提取与截断等转换，并要求匹配分析的各列共享显式的病例—发现键 \((\mathrm{case},\mathrm{finding})\)，同时固定共同队列、缺失处理和多重比较族。

<div class="method-step__io" markdown="1">

**输入**：原始响应文件、字节数、请求ID、结束状态、自动标签提取结果、缺失信息，以及各条件下的病例与影像学发现记录。  
**输出**：响应完整性清单、提取过程偏差、缺失模式，以及可用于配对统计的键控二元矩阵或无法可靠配对的记录。

</div>

**直观理解**：状态表显示“成功”不等于答案文件中确实有内容；比较两个条件时，也必须确保两列中的每一行都指向同一病例的同一发现，不能靠行号碰巧对齐。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 追踪统计、论文陈述与公开发布物

将每个统计量和公开主张反向连接到其代码、输入账本及生成它的发布版本，并比较当前更正材料与读者历史上实际取得的归档字节。校验和检查派生物是否一致，语义检查则判断图表是否真正支持相应结论。

<div class="method-step__io" markdown="1">

**输入**：键控分析表、统计代码、论文当前与历史源文件、表格和图形派生物、仓库或归档版本、清单、DOI及发布时间。  
**输出**：从分析输入到统计结果、论文表述和公开文件的传播图，以及过时数值、名称、表格或图形仍残留在发布包中的差异清单。

</div>

**直观理解**：即使作者电脑上的论文已改正，公开压缩包仍可能保存旧图和旧分数；因此必须检查读者实际下载到的版本，而不能只看当前稿件。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文是对既有基准工件的回顾性审计，不训练模型，也不定义用于参数优化的损失函数；其目标是验证各计算状态之间的身份一致性、分析配对和发布传播，并界定哪些历史结果可被重建、哪些必须撤回。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 六状态计算结果模型**

该模型把基准生命周期区分为 Intended、Executed、Observed、Analyzed、Reported 和 Released，并规定每一状态的首选证据。它避免用源代码注释推断运行行为、用状态字段代替文件存在性，或用当前论文版本代表历史公开版本。

> 直观理解：同一个结果在“计划怎样做”“实际上怎样做”和“最后对外发布了什么”之间可能发生变化；分状态检查可以定位偏差究竟从哪一站开始。

**2. 身份保持转换检查**

在状态转换处分别验证提示词文本、模型端点、检查与视图、渲染像素、病例—发现配对键及派生文件身份。字节级校验和负责发现对象是否完全相同，允许视图、唯一抽样单位、显式缺失和固定多重比较族等语义不变量则负责判断比较是否在科学上成立。

> 直观理解：校验和只能回答“两个文件是不是一样”，不能回答“比较是否临床合理”；因此还要增加关于视图、样本独立性和统计范围的业务规则。

**3. 三级修复边界**

修复判定取决于预期观察是否仍能由保存材料识别：明确的算术或转录转换可重做，存在测量或分母缺陷的数据只能在原标签体系内重建，而处理、输入或参考标准身份丢失意味着目标实验量不可识别。该模块明确区分“能够重新计算一个矩阵统计量”与“能够恢复原研究问题的答案”。

> 直观理解：有原始数字时可以修正计算器错误，但没有真正执行过目标实验时，再复杂的统计也无法补造缺失的观察。

**训练与推理**

无训练过程，也不进行新的模型推理。作者明确限定“不重新调用模型、不新增图像或报告标注”，仅分析保存的请求、响应、DICOM与渲染材料、自动标签矩阵、统计代码、论文及归档发布物。历史模型输出被当作不可更改的观测工件：先核验实际输入与输出身份，再按显式 \((\mathrm{case},\mathrm{finding})\) 键重建共同分析队列，最后检查统计值及其向论文和发布包的传播；任何重算结果都只解释为该归档自动标签矩阵的性质。

**复现信息**

公平复现该审计至少需要保留请求侧完整载荷、精确提示词文本或哈希、解析后的模型ID、执行路径、所选检查与视图、DICOM属性、渲染代码及渲染图像哈希；响应侧应采用原子记录，保存原始响应、字节数、请求ID和结束状态。分析侧必须使用显式病例—发现键、缺失图、共同队列规则和预先固定的多重比较族；发布侧则需保存版本化归档字节、清单、DOI和时间戳，并把表格、图形等派生物连接到其输入。所给节选未提供3.1节之后的完整执行细节，因此具体软件版本、目录结构和统计实现参数原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- 审计对象是一个保存下来的MIMIC-CXR胸片VLM试点：原计划从30项研究构成的富集样本出发，比较5个VLM家族和两种报告提示条件；实际30项研究来自28名患者。其作用不是重新估计临床性能，而是核对计划、执行记录、自动标签矩阵和发布物之间的一致性。
- 统计重建使用归档的自动标签矩阵；共同完整队列包含369个完整的病例发现块。该矩阵只反映既有自动标签流程，不能替代人工临床金标准，也不能恢复未被正确执行的提示词比较。
- 参考实现还使用合成请求和本地发布工件测试契约守卫，包括提示词路由、输出对账、分析矩阵及发布清单检查；这些测试用于验证审计控制能否发现结构性错误，而不是评价VLM诊断能力。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**调用完成度**

非空报告数相对于计划模型—提示词调用数的比例，并要求区分空输出、传输失败、安全阻断、无效响应和长度受限等终止状态。 （在请求身份和终止状态均可核验的前提下越高越好；但非空输出只说明调用产出了文本，不代表提示词、图像或模型身份正确。）

</div>
<div class="metricitem" markdown="1">

**Cochran's Q**

用于同一批配对样本上比较三个或更多相关二元条件总体差异的统计量。本文用它检查统一完整队列后总体检验是否改变。 （不存在简单的越高越好；较大的Q通常表示条件间差异证据更强，但只有在队列、标签和条件身份有效时才具有科学解释。）

</div>
<div class="metricitem" markdown="1">

**McNemar检验及Holm校正后的p值**

McNemar检验比较两个条件在同一病例上的不一致二元结果；Holm方法对一组比较进行逐步多重检验校正，以减少偶然假阳性。 （p值越低通常表示配对差异证据越强；校正后仍低于预设阈值比未校正显著更稳健，但不能补救错误提示词、错误图像渲染或未经验证的自动标签。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 计划调用与归档输出完整性核对

<div class="result-value" markdown="1">

300次计划的模型—提示词调用中，297次留下了非空报告，因此至少3次没有形成非空报告。

</div>

这说明仅按文件或文本是否存在计算，执行完成度接近但并非完整。更重要的是，297个非空结果不能证明调用使用了正确提示词、正确图像极性或正确模型版本；它只是输出层面的完整性检查。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Of 300 planned model-prompt calls, 297 yielded nonempty reports.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Claude名义提示条件A/B的请求路径审计

<div class="result-value" markdown="1">

标记为A和B的60次Claude调用实际都绑定到同一个System C提示词，因此保存结果表示C/C条件下的重复或随机变异，而不是A与B的提示效果差异。

</div>

这是对原提示词比较可识别性的直接否定：即使两组输出或自动标签不同，也不能把差异归因于A和B，因为系统并未真正执行这两个处理条件。该发现撤销提示词效应与相应排名解释，但不说明System C本身性能如何。

<div class="result-source" markdown="1">

来源：摘要；表3“Prompt routing”行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Sixty Claude calls labeled A/B were executed with the same C prompt.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### DICOM图像渲染与输入一致性审计

<div class="result-value" markdown="1">

4幅MONOCHROME1胸片未执行所需的极性反转，导致模型实际看到的明暗极性颠倒。

</div>

DICOM原文件完好不等于模型输入正确。MONOCHROME1要求按其光度解释进行显示转换；漏掉反转会把本应明亮的区域显示为暗色，反之亦然，从而使这些病例上的模型输出不能代表标准胸片输入条件。该结果揭示输入污染，但没有量化其对每个模型或病征的具体影响。

<div class="result-source" markdown="1">

来源：摘要；表3“Photometry”行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Four MONOCHROME1 images were rendered without required polarity inversion, dataset split membership was not retained, and the unvalidated extractor truncated five reports to 4000 characters.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 审计受保存工件边界限制：没有公开的历史请求负载账本、提供商解析后的稳定模型标识、逐记录标签、读者判定流程或原始提取器响应；数据集split成员关系也未保留。因此部分执行身份和标注误差只能确认风险，不能完全重建。
- 提出的契约是参考实现而非经验证的完整框架：像素验证器不会重新渲染或评价图像质量，分析模块未实现患者聚类推断和临床估计量，模型与标注条款部分仍停留在规范层面。即使所有复现门禁通过，也只能证明证据链更可检查，不能证明临床问题、伦理合规或统计设计本身有效。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 报告或计划中的协议：把名义条件、预期提示词、正位胸片队列和计划调用数视为应执行对象，再与保存下来的请求路径、DICOM元数据及输出文件逐项核对。该比较直接检验“标签所称条件”是否等于“系统实际执行条件”。
- 原始逐项删除分析：不同病征或比较可能使用不同的可用病例集合。以共同完整队列重算Cochran's Q，可检验原统计量是否受到不一致分母和缺失处理的影响。
- 未校正的McNemar显著性判断：与Holm多重比较校正后的判断对照，用于检验成组开展45次配对比较时，多少名义显著结果能够承受家族错误率控制。
- 八条基准契约的规范要求：将队列、像素、提示词、模型、输出、标注、分析和发布控制与当前参考实现逐条对照，以区分“已有可执行守卫”“部分覆盖”和“仅有规范说明”。

**实验想回答的问题**

- 保存下来的胸片VLM基准工件是否真正执行了论文声称的队列、图像渲染、提示词路由、模型调用、标签提取与统计分析协议？
- 在仅使用归档数据、不重新调用模型或标注图像的条件下，修正可识别的分析错误会怎样改变统计结论，以及哪些机器可验证控制能够阻止同类错误进入发布物？

**实验实现**

这是回顾性取证式复现审计，不重新调用任何模型，也不新增图像或报告标注。审计链路依次核对计划调用账本、实际提示词绑定、DICOM Photometric Interpretation与视图元数据、输出是否非空及其终止状态、自动标签提取与文本截断、基于科学键的配对统计，以及修正值能否传播到稿件、图表和归档包。统计上重建统一的完整病例发现矩阵，重算Cochran's Q，并对45个McNemar比较同时报告未校正结果和Holm校正结果。参考契约采用“失败即关闭”：任一关键不变量不满足，就生成明确失败状态并阻止下游发布；当前实现通过本地模式、测试、图表追踪和封闭清单等门禁构建纠正版工件，但并未覆盖全部临床与统计有效性要求。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 将原先可能随病征变化的可用样本分析，替换为369个完整病例发现块组成的共同队列 | Cochran's Q由154.73变为182.29，增加27.56。 | 该重建隔离了队列定义和缺失处理的影响：即使底层归档标签不变，仅统一所有条件使用的病例集合，总体检验统计量也会明显改变。因此，分母一致性是估计量定义的一部分，而不是无关紧要的数据清理细节。不过，新的Q值仍建立在归档自动标签上，不能修复错误提示词或图像输入。 | 摘要；分析重建结果<br><span class="experiment-evidence">Reconstructing one common cohort of 369 complete case-finding blocks changed Cochran's Q from 154.73 to 182.29.</span> |
| 对45个配对McNemar比较加入Holm多重检验校正 | 未校正时27项比较的p值低于0.05；Holm校正后仍有20项低于0.05，即有7项不再满足该阈值。 | 该对照隔离了多重比较控制的影响，表明部分名义显著结果可能来自同时检验大量假设。剩余20项只能解释为归档标签矩阵中的统计差异，不能被提升为临床性能差异，也不能验证原先声称的提示词处理效应。 | 摘要；分析重建结果<br><span class="experiment-evidence">Of 45 McNemar comparisons, 27 had unadjusted p < 0.05 and 20 remained below 0.05 after Holm adjustment.</span> |

**定性案例**

- 提示词路由故障构成最具代表性的案例：代码先按值导入默认提示词，随后对模块进行monkey-patch，但已导入的绑定并未随之更新，最终两个名义Claude条件都发送System C。普通的配置文件检查可能显示A/B文本存在，只有在请求边界记录展开后的实际文本及其哈希，并检查预期不同条件的哈希是否意外相同，才能可靠发现此类错误。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper conducts a forensic reproducibility and artifact-consistency audit of a radiology VLM benchmark and proposes verifiable benchmark controls.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`92d60b674d1405eda4f854d3b5bbdeb8cc564c494a25f0fc7dcec9afe37c6997`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
