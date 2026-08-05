---
title: "[论文解读] MultiGlobeQA: A Multilingual and Globally Diverse Benchmark for Geospatial Reasoning"
description: "[arXiv 2608.03882][LLM 评测] MultiGlobeQA旨在以多语言、全球分层且可执行验证的基准，系统判断大语言模型的地理空间推理失败究竟源于地理知识不足、空间计算能力不足，还是地区与语言覆盖偏差。"
arxiv_id: "2608.03882"
announcement_date: "2026-08-05"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:37:31.964339+00:00"
source_sha256: "b910115cb305632c246d864bc9d4f3eb407c687626c66884d89fb2ace86f5fca"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "LLM Agent"
  - "地理空间推理"
  - "多语言基准"
  - "地理问答"
  - "大语言模型"
  - "地理知识图谱"
  - "执行式真值"
  - "空间计算"
  - "地域公平性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.03882</p>

# MultiGlobeQA: A Multilingual and Globally Diverse Benchmark for Geospatial Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Martin Böckling, Elizaveta Nosova, Heiko Paulheim, Andreea Iana</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Data and Web Science Group, University of Mannheim, Germany</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03882v1) · [PDF 下载](https://arxiv.org/pdf/2608.03882v1) · **关键词** 地理空间推理, 多语言基准, 地理问答, 大语言模型, 地理知识图谱, 执行式真值, 空间计算, 地域公平性<br>


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

MultiGlobeQA旨在以多语言、全球分层且可执行验证的基准，系统判断大语言模型的地理空间推理失败究竟源于地理知识不足、空间计算能力不足，还是地区与语言覆盖偏差。

**不用术语来说**：大语言模型可能知道城镇的位置、坐标和所属国家，却不一定能据此正确算出两地距离、判断包含关系、转换坐标或生成地理网格编码；现有测试又常局限于虚构场景、少量地区或单一语言，因此难以判断模型在真实世界中究竟会在哪类空间操作、哪些地区和哪些语言上失效。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者构建了MultiGlobeQA：包含46,060个问答对，覆盖14类空间函数、15种答案格式、3个知识图谱以及201个国家和地区，并按收入与人口密度分层抽样；问题以英语及另外16种高资源和低资源语言平行发布，从而支持跨操作、地区和语言的受控比较。
- 作者采用基于知识图谱查询执行的标准答案，并在参数知识、显式推理、检索与工具使用等不同条件下评测模型，以区分“缺少地理事实”与“无法完成几何、拓扑或坐标计算”两类失败，同时检验社会经济区域差异。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

地理空间推理要求模型针对真实地理实体计算距离、方向、包含关系、坐标变换等几何或拓扑关系，是导航、物流与规划系统的基础能力。大语言模型虽然可能在参数中记忆地名、坐标等地理事实，也可通过检索或工具获得这些事实，但“知道位置”并不等于能够正确执行空间计算；因此，该领域需要把事实访问能力与计算能力区分开来评测。现有基准往往使用玩具世界中的合成关系，或只覆盖少量真实地区、单一语言和有限空间操作；直接从 OpenStreetMap 或 Wikidata 采样还可能继承其偏向高收入及城市地区的数据分布。MultiGlobeQA 因而将问题置于真实地理实体、多个知识图谱、多种空间函数、不同答案格式及多语言环境中，并通过按收入和人口密度分层的地域采样，考察模型能力是否随任务类型、语言和区域而系统变化。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**地理空间推理**

指基于地理实体的位置、边界或空间结构，计算距离、方向、包含、相交和坐标变换等关系。它不同于单纯回忆某个地点属于哪个国家，因为答案通常需要几何或拓扑运算。

</div>
<div class="concept-item" markdown="1">

**地理知识图谱**

以结构化方式表示地点、行政区、道路等实体及其属性和关系的数据源，可包含坐标、几何形状和实体链接。本文在三个独立构建的地理知识图谱上生成并执行问题，以减少结论对单一数据源的依赖。

</div>
<div class="concept-item" markdown="1">

**执行式真值**

不是由语言模型或表面文本匹配决定标准答案，而是把结构化查询或空间函数交给数据库系统执行，并将执行结果作为真值。这样可以规模化生成可验证答案，并更直接地检查空间计算是否正确。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

该基准的输入是关于真实地理实体的自然语言问题，问题可用英语或另外 16 种高资源、低资源语言表达，并覆盖距离、拓扑关系、方向、网格索引、形状计算、坐标变换等空间函数族；不同评测设置还可只依赖模型参数，或向模型提供检索到的事实、标准事实及计算工具。输出是与问题指定格式一致的答案，例如数值、类别或其他结构化结果，并与在三个地理知识图谱上执行空间查询得到的标准答案比较。数据集共含 46,060 个问答对、14 个空间函数族和 15 种答案格式，覆盖 201 个国家和地区；其核心假设是：通过执行式真值、跨语言平行问题以及按国家收入和人口密度分层的采样，可以分别观察知识访问、空间计算、语言资源水平与地域覆盖对模型表现的影响，而不把总体准确率误当作单一能力指标。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **SPARTQA、SpaRTUN 与 StepGame**: 这些文本空间推理基准主要在玩具世界中测试固定类别的定性空间关系，适合检查抽象关系推理，但不能充分说明模型能否处理真实地理实体、精确几何计算、全球地域差异和多语言表达；MultiGlobeQA 将评测对象转向真实地理数据及更广泛的空间操作。
- **GeoQuestions1089**: 该工作把 1,089 个手工编写的问题与可执行 GeoSPARQL 查询配对，并在 YAGO2 与 YAGO2geo 的联合数据上求解，体现了可执行地理问答的思路；但它主要面向事实和关系检索，规模、语言与空间操作覆盖均不足以支持 MultiGlobeQA 所追求的全球、多语言和分层能力诊断。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

导航、物流和规划系统需要对真实地理实体执行距离计算、方向判断、空间包含、坐标变换和网格索引等操作。大语言模型虽然储存了相当多的地理事实，甚至可能表征坐标信息，但将这些事实转化为可靠空间结论仍很困难；错误可能达到数量级差异，并且即使提供相关事实，模型也可能无法完成地理编码等计算。这使其在直接回答、检索增强或智能体工作流中的实际可靠性难以保证。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **合成或抽象空间推理基准**：这类基准通常构造抽象对象及其定性空间关系，让模型根据给定描述判断上下左右、邻接或包含等关系。它们便于控制推理结构，但主要测量抽象关系推断，而非对真实地理实体、坐标和复杂几何形状进行计算。
- **基于真实地理数据的现有评测**：这类工作从OpenStreetMap、Wikidata等真实数据源采样地点、坐标或地图信息，再通过问答任务测试模型的地理知识与空间推理；部分评测覆盖地图理解或特定空间操作，但通常规模较小、以单一语言为主，且对国家、收入水平和人口密度等覆盖因素缺少系统控制。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有基准要么以合成对象和定性关系为主，要么在真实地理场景中规模有限，因此不能同时细分并比较距离、拓扑、方向、形状、坐标变换和网格索引等不同计算能力；其后果是模型失败只能被笼统归为“地理空间推理差”，无法定位具体计算瓶颈。
- 真实地理基准多为单语且缺乏受控的全球覆盖，并常直接继承OpenStreetMap或Wikidata中不均衡的地区覆盖和社会经济偏差；因此观察到的性能差异可能混合了语言资源、数据可得性、区域代表性与计算能力，难以判断模型是否对低收入地区存在系统性劣势。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前缺少一个同时具备真实地理实体、大规模多类空间操作、多种答案表示、跨高低资源语言、按收入与人口密度分层的全球覆盖，以及可通过查询执行获得标准答案的统一基准。尤其缺少一种受控评测设计，能够通过逐步提供检索事实和计算工具，分离模型的参数化地理知识、外部信息访问能力与实际空间计算能力。

</div>
<div markdown="1"><span>核心问题</span>

在控制空间函数、答案格式、地区和语言后，大语言模型能否可靠地对真实世界地理实体进行推理；当向模型提供检索结果、标准事实或计算工具时，其错误主要由知识访问不足还是几何、拓扑、坐标及网格计算不足造成，并且这种能力是否随地区收入水平与语言资源水平而系统变化？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把地理问答拆成可控维度，并为同一类问题设置不同信息与工具条件：若仅补充事实即可显著消除错误，瓶颈更可能是知识访问；若给出标准事实后表现仍停滞，而加入计算工具才改善，则瓶颈更可能是空间运算。再用收入、人口密度和语言进行分层，可以避免全球平均分掩盖特定地区或语言群体的失败。通俗地说，这种设计不仅问模型“答对没有”，还通过逐层提供原料和计算器，诊断它究竟是不知道数据、不会计算，还是只在某些地区和语言上表现较差。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MultiGlobeQA采用“类型化模板设计—分层实体采样—可执行答案生成—多语言扩展”的端到端构建流程。作者先将地理空间推理划分为14类空间函数，并设计65个顶层模板及其参数化子模板；随后从WorldKG、KnowWhereGraph和OSMH3KG三个知识图谱中抽取具有几何、类型和地理属性的实体，在收入等级与人口密度构成的$4\times3$分层网格内分别采样；每个问题模板都绑定一个可执行查询，由执行器直接计算答案并进行类型约束检查，从而得到46,060组经执行验证的英文问答；最后将模板翻译为16种目标语言，并用当地语言实体标签重新实例化，形成17种语言平行覆盖的基准。

直观地说，该方法不是让语言模型先编题、再靠人工猜测答案是否正确，而是先规定要考查哪一种空间运算，再从真实地理数据库中选择对象，用程序算出唯一或可验证的答案，最后把同一道题转换为多种语言。分层采样控制题目来自何种经济与人口环境，使模型能力能够按空间函数、国家收入层级、人口密度和语言分别比较。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建类型化空间推理模板体系

作者定义65个顶层模板，组织为14个空间函数类别和六个操作簇，并扩展为129个参数化子模板；每个子模板再配置1至5个人工核验的英文改写，共形成315个自然语言变体，支持15种布尔、数值、几何、类别或时间答案格式。

<div class="method-step__io" markdown="1">

**输入**：常见地理空间运算类别、实体角色、可调参数以及期望答案类型。<br>
**输出**：带有类型化占位符、查询语义和答案格式约束的模板库。

</div>

**直观理解**：模板相当于一套可填空的试题模具：它同时规定问题怎样表述、哪些实体能够填入，以及最终应返回数字、方向、集合还是几何形状。这样可以系统覆盖距离、包含、路径、方向、网格编码等不同能力，而不是随机收集问题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 统一知识图谱并进行地理分层采样

作者将三个知识图谱转换为统一实体表，保存WKT几何、规范名称、由$rdf:type$映射的语义类别和H3索引，并为每个实体附加四档国家收入标签与三档人口密度标签；在每个可满足的“模板—知识图谱—分层单元”中独立抽取最多30个实体元组。

<div class="method-step__io" markdown="1">

**输入**：WorldKG、KnowWhereGraph和OSMH3KG中的实体、类型、名称、关系及空间几何，以及世界银行收入分类和WorldPop人口栅格。<br>
**输出**：覆盖12个收入—密度分层单元、201个国家和地区的候选实体元组。

</div>

**直观理解**：若直接从开放地图随机抽样，题目容易集中在富裕国家和大城市。这里先把世界按经济水平和人口密度分成12格，再逐格取样，使欠发达或低密度地区也有机会进入测试集。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行查询并生成经验证的英文问答

执行器先按角色所需类型筛选实体，再在相应知识图谱上运行查询并从有效结果中采样；结果须通过答案类型相关的约束检查，退化执行会被丢弃，之后按$(\mathrm{question},\mathrm{ground\ truth})$去重并均匀选择一个英文表述变体。

<div class="method-step__io" markdown="1">

**输入**：类型化模板、对应的可执行查询模板，以及各分层单元中的候选实体元组。<br>
**输出**：46,060组执行式真值英文问答，其中约6.9千、24千和15千组分别基于KnowWhereGraph、OSMH3KG和WorldKG。

</div>

**直观理解**：程序先确认某组实体确实能构成一道有效题，再直接用数据库和空间算法算答案。例如距离必须在地球尺度的合理范围内，多边形必须闭合且不能自相交；除零或断路等无意义情况不会进入数据集。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造挑战切片并扩展到多语言版本

作者通过破坏原本可满足的前提生成3,589道错误前提题，并为视觉显著实体构造946道独立多模态题；同时将模板机器翻译至16种语言，经双人后编辑与分歧裁决后重新实例化，再由三个语言模型组成的集成系统修复实体替换引起的局部语法问题。

<div class="method-step__io" markdown="1">

**输入**：已验证英文问答、315个英文模板变体、多语言实体标签，以及知识图谱中的图像链接。<br>
**输出**：17种语言的large版本，每种语言46,060题；以及每种语言5,916题、按知识图谱与空间函数单元保留覆盖的small版本，另含错误前提与多模态评测切片。

</div>

**直观理解**：翻译的是试题模具而非逐题自由改写，因此各语言尽可能保持同一计算任务；人工复核负责纠正“在内部”和“在范围内”等关键语义差异。实体名称填入句子后可能造成冠词或一致关系错误，集成后编辑器只修改实体周围的语法，以避免改变题意。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。MultiGlobeQA是基准数据集构建方法，不训练一个新的预测模型，也未提出需要优化的损失函数；其核心目标是通过分层采样、可执行查询和类型约束生成可复核的问答真值。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 空间函数与答案格式类型系统**

模板体系覆盖距离、包含与拓扑、网络与路径、行政层级与比较、中心性、网格、坐标与变换、方向、形状、不确定性以及时空事件等14类空间函数，并将占位符角色和15种答案格式显式类型化。类型约束贯穿候选实体过滤、查询执行和答案验证。

> 直观理解：该模块明确每道题究竟要求哪一种计算，以及答案应该长什么样。它既防止把不合适的实体填入模板，也使错误能够定位到具体能力，如“知道地点但不会算geohash”，而不只得到一个总准确率。

**2. 收入—人口密度分层采样器**

每个实体按世界银行FY2026分类获得$\{\mathrm{LIC},\mathrm{LMC},\mathrm{UMC},\mathrm{HIC}\}$之一，并依据WorldPop R2025A的1公里人口栅格及全球第33、67百分位获得低、中、高密度标签；两者组合成$4\times3=12$个分层单元，采样在各单元内独立进行。

> 直观理解：该模块不是为了让总题数在每格完全相同，而是保证每个有可用数据且模板可执行的格子都能贡献样本。因而实验可以区分模型是否在低收入地区或稀疏地区系统性表现较差，而不把数据来源失衡误当成模型能力。

**3. 查询执行与类型约束验证器**

每个自然语言模板绑定一个知识图谱查询或空间计算过程，执行器从查询结果中生成实体—答案实例，并检查距离范围、几何有效性及图连通性等约束；错误前提题则由可满足实例定向扰动得到，要求模型识别前提不成立。

> 直观理解：这是基准答案可信度的核心：答案来自可重复执行的数据库查询和几何运算，而不是人工直觉或语言模型生成。验证器再过滤数学上或拓扑上无意义的结果，降低“题目本身有错”对评测的干扰。

**训练与推理**

数据构建阶段不涉及模型训练。生成时，系统对每个“模板—知识图谱—分层单元”组合筛选满足角色类型的实体、执行绑定查询、验证结果、排除退化情况并去重，然后选择自然语言变体完成实例化；多语言版本使用已经人工后编辑的模板和多语言实体标签重复实例化。用于语言质量修复的三个模型仅充当受限后编辑器：它们输出13类之一的类型化局部修改，至少两个模型同意时采用多数编辑，否则回退到Gemini-3-Flash的结果。

实际评测时，large版本提供每种语言46,060道题，small版本提供5,916道覆盖性子集以降低约八倍评测成本。模型接收实例化问题并输出与指定答案格式相符的答案；错误前提题测试模型能否拒绝无效前提，多模态切片则用代表性图像替代实体名称。原文所述模型评测还可在参数化、显式推理、知识图谱或网页检索代理以及注入金标准三元组的oracle条件下运行，但这些属于评测设置，并非基准生成流程。

**复现信息**

复现所需的关键数据表示包括统一的WKT几何、规范实体名、语义类别和H3索引；重名实体通过添加街区、街道或必要时的坐标消歧。英文实例按$(\mathrm{question},\mathrm{ground\ truth})$去重，每个有效实体元组均匀抽取一个自然语言变体；距离须受地球周长约束，多边形须闭合且不自相交，除零和断开图等退化执行被删除。

翻译流程将占位符标记为不可翻译，并自动检查每个源占位符在译文中恰好出现一次；每种语言由两名熟练双语者逐模板后编辑，确定性分歧以规则解决，其余由Claude Opus 4.7裁决。KnowWhereGraph不进入多模态切片，因为其灾害和事件实体缺少稳定图像绑定。作者公开了代码、数据和知识图谱快照，代码地址为https://github.com/andreeaiana/MultiGlobeQA，数据地址为https://huggingface.co/datasets/aiana94/MultiGlobeQA。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 核心评测集为 MultiGlobeQA，共 46,060 个问答对，覆盖 14 个空间功能家族、65 个顶层模板和 15 种答案格式；包含英语及另外 16 种高资源与低资源语言的平行问题。实体分布覆盖 201 个国家和地区，并按世界银行 FY2026 收入等级和人口密度分层采样。所给章节未说明训练集、验证集与测试集的具体划分；其角色是统一评测参数知识、空间计算、检索和工具使用能力。
- 问答实例及可执行真值来自 WorldKG、KnowWhereGraph 和 OSMH3KG 三个空间知识图谱。三者分别提供 14,840、6,899 和 24,321 条问题记录，总计对应 MultiGlobeQA 的 46,060 条记录；它们在地理实体类型和空间功能覆盖上互补，并用于生成问题、保存支持答案的知识图谱三元组以及执行空间运算得到标准答案。
- 地域分层数据由 Natural Earth 10m 国家多边形、世界银行 FY2026 收入分类和 WorldPop R2025A 1 km 人口栅格构成。实体通过空间连接获得国家及收入层级；人口栅格聚合到 H3 分辨率 3，并按全球第 33 与第 67 百分位划分密度层。该部分不是独立问答集，而是用于控制地域覆盖并检验收入与人口密度相关的性能差异。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

原文未明确报告，或这里不需要额外前置概念。

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 不同空间功能家族上的总体表现

<div class="result-value" markdown="1">

作者报告，模型在需要网格索引和形状计算的任务上出现明显性能崩溃，而拓扑关系和方向判断相对最好。

</div>

网格索引要求把坐标转换为 H3 或 S2 单元，形状任务则涉及面积、周长、紧致度或边界不规则度等几何运算；它们通常不能仅靠记住地名或事实完成。相反，拓扑与方向问题中有较多布尔或预定义类别答案，也更可能由局部关系和语言线索支持。该结果说明不同空间功能的难度高度不均衡，但所给材料没有提供各功能的具体分数，因而不能量化差距，也不能证明答案格式是造成差异的唯一原因。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across parametric, reasoning, and agentic settings, LLMs collapse on tasks requiring grid indexing and shape computation, while topological relations and directions fare best.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 检索、工具使用与标准事实注入

<div class="result-value" markdown="1">

作者报告，检索和工具使用能带来显著提升，但即使直接提供标准支持事实，总体表现仍低于三分之二。

</div>

如果错误主要来自不知道实体坐标、边界或关系，那么标准事实注入应使性能接近上限；实际仍低于三分之二，表明模型还难以把事实转换成正确的程序、选择合适的几何操作并按目标格式返回答案。因此作者将主要瓶颈归因于计算而非知识访问。不过，“低于三分之二”是总体性上限描述，所给摘录未列出具体模型、指标和置信区间，不能据此判断所有模型或所有子任务都低于该水平。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Retrieval and tool use yield considerable gains, yet performance plateaus below two thirds even when gold facts are supplied, indicating that computation, not access to knowledge, is the bottleneck.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 按地区收入水平分层的评测

<div class="result-value" markdown="1">

作者报告，模型在低收入地区上的表现更差，而且提供标准事实后，这一差距不但没有缩小，反而扩大。

</div>

这一结果反驳了“地域差异只由检索不到当地事实造成”的简单解释：当输入事实被控制为标准三元组后，剩余差距可能与实体标签、几何复杂度、数据分布、语言表达或模型处理这些事实的能力有关。但摘要没有报告各收入层级的样本量、绝对分数或控制变量分析，因此不能确定差距的因果来源，也不能直接把收入水平本身解释为致因。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Models also underperform on low-income regions, a gap that gold facts widen rather than close.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验摘录没有包含主结果表、各模型与空间功能的具体分数、评分指标定义、数值答案容差、答案规范化方法或显著性检验。因此，除摘要明确给出的“低于三分之二”外，无法复核提升幅度、模型排序及不同任务之间的定量差异。
- 收入层级分析具有重要警示意义，但摘要未说明是否同时控制知识图谱来源、国家样本量、城市化程度、实体类型、几何复杂度、语言和答案格式。因而目前能确认的是相关性能差距及其在标准事实条件下的变化，不能把收入层级解释为直接原因。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 多数类基线：对每个参数绑定后的子模板始终预测其最常见标准答案，作为不进行空间推理的下界。按子模板而非全数据取多数类，可避免答案分布差异使基线失去可比性。
- Qwen3.5 系列：评测 Qwen3.5-35B 和 Qwen3.5-27B 两个开放权重多模态模型；前者使用原生推理模式，后者采用提示式思维链。二者用于比较同一模型家族在不同规模与推理机制下的空间推理表现。
- Gemma-3-27B-Instruct：开放权重多模态指令模型，使用提示式思维链；它提供不同模型家族、相近参数规模下的对照。
- Gemini-3-Flash：闭源模型并启用原生推理模式；它用于判断结论是否仅局限于开放权重模型。

**实验想回答的问题**

- 在仅依赖参数记忆、显式推理、外部检索与可执行工具的不同条件下，大语言模型能否完成真实世界地理实体上的距离、拓扑、方向、网格索引和形状计算等空间推理任务？性能瓶颈主要来自事实缺失，还是来自对已有空间事实进行几何与拓扑计算的能力不足？
- 模型性能是否会随空间功能、知识图谱来源、事实表示方式、语言资源水平及地区收入水平而系统变化，尤其是完美提供支持事实后，语言和地域差距是否仍然存在？

**实验实现**

评测分为三个层级。T1 只向模型直接提供问题，主要测量参数记忆与无需外部工具时的作答能力；T2 在相同问题上加入显式推理，以检验语言化推理是否足以改善空间计算；T3 允许模型在受限 CodeAgent 解释器中编写并执行 Python，并通过多轮工具调用收集证据。T3a 只检索空间知识图谱，T3b 只进行网页搜索，T3c 同时使用两者。Gemini-3-Flash 与 Qwen3.5-35B 使用原生推理模式，Qwen3.5-27B 与 Gemma-3-27B-Instruct 使用提示式思维链；更具体的推理配置位于原文附录 D、E，但未包含在所给摘录中。

实验另设四种 oracle 条件。T1 oracle-structured、T1 oracle-raw 和 T1 oracle-verbalized 向模型注入支持答案的同一组标准知识图谱三元组，但分别表示为结构化 JSON、原始 N-Triples 和自然语言文本，用于测试事实表示敏感性。T3 oracle 将结构化标准三元组直接交给保留 Python 解释器的代理，同时关闭检索工具，用于近似“完美检索”。因此，T1 与 T1-oracle 的差异主要反映事实可得性的作用，T3 与 T3-oracle 的差异则比较在线检索和完美检索。所给章节没有明确给出评分指标名称、答案归一化规则、容差设置或统计显著性检验，因此 metrics 留空，不能据此推断使用了准确率、F1 或数值误差等特定指标。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| T1 与三种 T1 oracle 表示形式：structured、raw、verbalized | 三种条件包含相同的标准知识图谱支持事实，仅将其分别表示为结构化 JSON、原始 N-Triples 和自然语言文本。所给摘录仅说明该消融用于测试表示敏感性，未明确报告三种形式各自的数值结果或优劣排序。 | 这组消融固定事实内容，只改变事实的表面编码，因此可隔离模型是否更擅长读取 JSON、知识图谱三元组或自然语言。若结果不同，差异应优先解释为事实解析和表示适配能力，而不是检索召回率变化；但由于结果表未出现在材料中，不能断言哪种表示最佳。 | Section 4, Experimental Setup — Evaluation Settings<br><span class="experiment-evidence">Three differ only in surface form – structured JSON, raw N-Triples, or verbalized prose (T1 oracle-structured / -raw / -verbalized) – to test representation sensitivity.</span> |
| 标准事实注入下的收入层级差距 | 标准事实没有缩小低收入地区的性能差距，作者报告该差距反而扩大。 | 该比较通过改善事实可得性来检验地域差距是否主要源于知识缺失。差距扩大意味着检索覆盖不足不是充分解释，模型对事实的解析、计算过程或不同地区实例的结构差异仍可能造成不均衡。它并未控制所有潜在混杂因素，因此只能排除“只要提供事实就会消除差距”的强假设，不能确定真正的因果机制。 | Abstract<br><span class="experiment-evidence">Models also underperform on low-income regions, a gap that gold facts widen rather than close.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces a multilingual benchmark that measures LLM geospatial reasoning across parametric, retrieval-assisted, and tool-using settings.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`b910115cb305632c246d864bc9d4f3eb407c687626c66884d89fb2ace86f5fca`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
