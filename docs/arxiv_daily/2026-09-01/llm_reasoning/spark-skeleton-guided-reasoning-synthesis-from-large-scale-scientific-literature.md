---
title: "[论文解读] SPARK: Skeleton-Guided Reasoning Synthesis from Large-Scale Scientific Literature"
description: "[arXiv 2608.30214][LLM Reasoning] SPARK以科研论文中的“主张—证据—推导”结构为合成单位，先提炼自包含的推理骨架，再从机制解释、假设证伪、定量推导和边界校准四个视角生成并校验训练样本，以缓解高质量科学推理数据不足的问题。"
arxiv_id: "2608.30214"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:47:00.910499+00:00"
source_sha256: "b6593095b2f715e36067b611139fb6a9b1d9d771d4ab329fecf6d390a018ca17"
tags:
  - "LLM Reasoning"
  - "科学推理"
  - "大语言模型"
  - "数据合成"
  - "科研论文"
  - "推理骨架"
  - "主张—证据—推导链"
  - "自包含问答"
  - "Spark-234K"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.30214</p>

# SPARK: Skeleton-Guided Reasoning Synthesis from Large-Scale Scientific Literature

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Yu Li, Wei Li, Xin Gao, Mengyuan Sun, Xiaoyang Wang, Qizhi Pei, Lijun Wu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Shanghai AI Laboratory；Affiliation: University of Science and Technology of China；Affiliation: East China Normal University；Affiliation: Peking University；Affiliation: Renmin University of China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30214v1) · [PDF 下载](https://arxiv.org/pdf/2608.30214v1) · **关键词** 科学推理, 大语言模型, 数据合成, 科研论文, 推理骨架, 主张—证据—推导链, 自包含问答, Spark-234K<br>


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

SPARK以科研论文中的“主张—证据—推导”结构为合成单位，先提炼自包含的推理骨架，再从机制解释、假设证伪、定量推导和边界校准四个视角生成并校验训练样本，以缓解高质量科学推理数据不足的问题。

**不用术语来说**：开源大模型即使能回答知识题或套用公式，也常常不擅长像科研人员那样依据证据解释现象、比较并排除假设、推导数量关系，以及判断结论在什么条件下才成立。科研论文包含这些推理过程，但信息散落在正文、图表和实验讨论中，直接把论文改写成问答题容易遗漏必要背景，使问题无法独立作答，或让答案缺少论文证据支持。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出面向科研论文的数据合成框架SPARK，不直接从章节或文本块生成问答，而是提取中心主张及其证据、假设、定量关系和适用边界，组织成紧凑且自包含的推理骨架。
- 基于推理骨架从机制推理、假设证伪、定量推导和边界校准四类视角生成任务，并通过一致性检查过滤无依据或相互矛盾的输出；由此从Sci-Base的37万篇前沿论文构建包含23.4万条样本的Spark-234K。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型科学推理数据构建领域。开放源模型虽已能较好处理数学与编程推理，但科学推理不仅要求回忆知识或套用公式，还要求依据证据解释现象机制、比较并排除竞争性假设、完成定量推导，以及判断结论成立的条件与边界。教科书、考试题和网络资源构成的现有语料往往偏向既定事实与标准解法；科研论文则包含经专家论证的主张、证据、假设、推导和实验分析，因而是更贴近真实科学推理的监督来源，但其论证通常分散在正文多个章节、图表和实验讨论中，不能直接等同于可训练的自包含问答数据。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**科学推理**

指从观测、实验结果、理论假设和定量关系出发，对科学主张进行解释、推导或检验的过程。本文重点关注机制理解、假设证伪、定量推导和适用边界，而非单纯事实记忆。

</div>
<div class="concept-item" markdown="1">

**主张—证据—推导链**

“主张”是论文希望成立的核心结论，“证据”是支持结论的实验、观测或分析结果，“推导”则说明证据如何在给定假设下导向结论。SPARK把这条逻辑链视为数据合成的基本单位。

</div>
<div class="concept-item" markdown="1">

**推理骨架**

推理骨架是从长篇论文中压缩出的结构化论证摘要，保留核心主张、支持证据、必要假设、定量关系和边界条件。它为后续问题生成提供自包含上下文，避免任意文本切块割裂跨章节证据。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是来自Sci-Base、覆盖10个科学学科的前沿科研论文；总体数据来源包括37万篇论文。目标不是直接把整篇论文或局部文本块改写成普通问答，而是先恢复论文的核心主张及其证据、假设、定量关系和边界条件，形成紧凑的推理骨架，再据此生成机制推理、假设证伪、定量推导和边界校准四类自包含科学推理样本，并通过一致性检查剔除缺乏支持或相互矛盾的输出。该设置隐含的核心要求是：生成的问题与答案应仅凭样本提供的信息即可理解和作答，同时忠实保留原论文的论证关系；最终产物是包含23.4万条合成实例的Spark-234K训练数据集。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **TextbookReasoning**: 该工作从大学教科书提取科学问答，代表以课程材料为来源的数据构建路线。本文认为教科书更偏向已经确立的知识、标准推导与常规计算，难以充分覆盖科研论文中的证据驱动和机制驱动推理。
- **OpenScienceReasoning-2与MegaScience**: 二者代表追求规模和覆盖面的科学推理数据集合，并被本文用作重要比较对象。SPARK关注的缺口不是继续扩大样本量，而是从论文的主张—证据—推导结构中提取更深且自包含的监督；摘要与引言声称Spark-234K在样本更少的情况下取得更强表现，但该结论需结合实验章节核验。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

科学推理模型需要学习真实科研活动中的证据驱动论证，而现有训练资源主要覆盖事实记忆、标准推导和常规计算，难以充分训练模型理解现象机制、评价竞争性假设、从条件推导数量关系，以及识别结论的适用范围。这种数据缺口是开源模型科学推理能力仍明显落后于数学和代码推理能力的重要制约。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **教材、考试题与网络资源驱动的数据集构建**：从已有教学材料或网页中收集问题、答案和解题过程，将其作为监督微调样本；这类材料通常结构清楚、答案明确，适合训练知识回忆、公式应用和规范化解题。
- **基于科学文献的直接问答或推理样本生成**：把论文的局部章节、固定长度文本块或整篇文档交给生成模型，直接据此构造问题与答案，希望利用论文中的专业结论、实验结果和论证信息形成科学训练数据。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 教材、考试题和网页数据偏重事实回忆、标准推导及例行计算，较少呈现科研发现所依赖的机制解释、证据权衡与假设检验，因此模型可能学会答题套路，却未学会从证据走向结论。
- 论文篇幅长且结构密集，关键推理往往跨越多个章节、图表和实验讨论；直接从局部文本或整篇文档生成样本容易受到长上下文干扰，遗漏关键假设或证据，并产生依赖原文才能理解、证据不足或未保留“主张—证据”关系的问题。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作尚缺少一种可扩展的数据合成机制，能够先从长篇科研论文中恢复完整的“主张—证据—推导”链，再将其压缩为不依赖原文也能理解的表示，并据此系统覆盖机制、证伪、定量关系和适用边界等真实科学推理形态，同时过滤与论文不一致的生成内容。

</div>
<div markdown="1"><span>核心问题</span>

能否把大规模科研论文中的核心论证结构提炼为紧凑、自包含且证据可追溯的推理骨架，并以此合成比直接论文问答更困难、更多样且更具训练效率的科学推理数据？

</div>
<div markdown="1"><span>作者直觉</span>

论文真正有训练价值的部分不是某一段文字，而是结论如何由证据、假设和推导共同支撑。先制作“论证提纲”可以把散落在长文各处的必要信息集中起来，减少无关上下文和信息缺失；再从四种互补视角围绕同一提纲出题，可以迫使模型分别学习解释原因、排除错误解释、完成推导和辨认结论边界，而最终一致性检查则像核对题目、答案与原论文论证是否相符，用于剔除无依据或矛盾样本。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SPARK是一条以论文论证结构为中介的科学推理数据合成流水线。它先从Sci-Base中筛选约37万篇近期、英文、解析完整且含有明确“主张—证据”轨迹的研究论文；随后将每篇长论文压缩为由核心结论、按逻辑排序的证据步骤、可观测量及适用边界组成的“推理骨架”；再从机制推理、假设证伪、定量推导和边界校准四个视角生成至多四道自包含问题，并在答案生成后用同一骨架检查问题与答案是否有据可依；最后进行去重和评测集去污染，得到Spark-234K。技术上的关键不是直接把论文段落改写成问答，而是先重建论文用于支持中心结论的证据链，再把这条证据链转化为训练任务。

直观地说，SPARK先把一篇很长的论文整理成一张“结论如何被一步步证明”的提纲，然后依据提纲出题，而不是随意从正文中截取事实。骨架既为问题提供必要背景，也作为质量检查的参照答案来源，从而减少需要查看原论文才能作答的问题，以及表面流畅但不受论文证据支持的答案。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 论文筛选与输入规范化

保留2024年1月至2026年3月之间的英文、解析完整、非综述且具有明确论证轨迹的论文，优先选择包含公式、统计结果、表格或实验比较等具体可观测量的文献，并按十大学科进行平衡采样。对约37万篇种子论文进行线性化，保留公式、表格文字、图注和数值结果，删除页眉页脚、作者单位、参考文献及致谢等非论证内容。

<div class="method-step__io" markdown="1">

**输入**：Sci-Base约336万篇、覆盖十个科学学科的论文，以及MinerU2.5解析得到的有序段落、表格、图注和公式。<br>
**输出**：约37万篇学科相对平衡、具有明确论证结构的规范化论文文本。

</div>

**直观理解**：这一步相当于先挑出“有清楚结论且拿得出证据”的论文，再把复杂版式整理成模型能顺序阅读的文本。它避免低质量解析、综述性罗列和学科数量失衡把后续生成方向带偏。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 两阶段推理骨架抽取

首先仅依据标题和摘要定位论文的核心结论；然后让抽取模型在该结论的条件约束下阅读全文，将支持结论的论证重建为有序步骤，每一步记录其逻辑作用及测量、比较、数值、公式或边界条件等可观测量。抽取结果不沿用原论文的章节顺序，而围绕中心主张组织证据轨迹。

<div class="method-step__io" markdown="1">

**输入**：论文的标题、摘要以及规范化后的全文。<br>
**输出**：包含一个核心结论、若干有序证据步骤、具体可观测量、假设或适用边界的紧凑推理骨架。

</div>

**直观理解**：普通摘要只说明论文讲了什么，推理骨架则说明结论为什么成立。它像把论文整理成“结论—证据一—证据二—限制条件”的证明路线，使出题模型不会被长文中的背景和旁支细节分散注意力。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多视角问题与答案生成

仅在骨架证据充分支持时，从机制推理、假设证伪、定量推导和边界校准中选择相应视角，每个视角最多生成一道问题；规则过滤器随后删除格式异常、泄露来源或依赖未提供图表与上下文的问题。独立答案模型在看不到论文和骨架的条件下作答，并删除格式错误、长度异常或重复$n$元片段占比过高的回答。

<div class="method-step__io" markdown="1">

**输入**：推理骨架，以及抽取阶段为该论文推荐的推理视角。<br>
**输出**：初步通过自包含检查的科学推理问答对。

</div>

**直观理解**：四类题分别追问“为什么会发生”“哪个解释经不起证据”“数量关系怎样推出”以及“结论到哪里不再成立”。答题模型拿不到原论文，是一次现实条件下的压力测试：如果仅凭题面无法作答，说明题目没有把必要信息交代完整。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 骨架约束质量审核与最终清洗

大语言模型裁判依据骨架检查问题是否自包含且与来源一致，并检查答案推理是否连贯、是否得到证据轨迹的逻辑支持；任一条件失败即丢弃。通过审核的数据按学科使用Qwen3-Embedding-8B语义向量去重，再与所有下游评测集执行13-gram精确匹配，删除可能造成测试泄漏的记录。

<div class="method-step__io" markdown="1">

**输入**：候选问题、候选答案及其来源论文的推理骨架三元组。<br>
**输出**：经证据约束、语义去重和评测集去污染后的234K条Spark-234K指令微调数据。

</div>

**直观理解**：骨架在这里像一份压缩后的“证据账本”：裁判不仅看答案是否像真的，还要核对每一步是否能从论文证据推出。最后的去重与去污染分别防止模型反复记忆近似样本，以及因提前见过测试题而产生虚高成绩。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：SPARK本身是数据构建框架，所给章节未提出需要优化的专用损失函数或中心数学目标，因此不应为骨架抽取、问题生成或质量审核虚构训练方程。产出的Spark-234K用于标准监督微调：模型以问题为输入、以合成答案为目标序列，通过常规自回归语言建模目标学习科学推理过程；但该目标的显式公式在所给原文中未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 主张中心化推理骨架**

该模块采用“核心结论定位—证据轨迹抽取”的两阶段结构：标题和摘要用于确定中心主张，全文则在该主张条件下被重组为有序论证步骤。每一步同时保存逻辑角色和可观测量，因此骨架不同于按章节压缩的摘要，也不同于互相独立的文本分块。

> 直观理解：长论文中真正决定结论的内容通常散布在方法、结果和讨论部分；若直接输入全文，模型容易关注局部事实而忽略整体论证。骨架把分散证据串成一条围绕同一结论的路线，既缩短有效上下文，也保留出科学推理题所需的数值和限制条件。

**2. 证据自适应的四视角生成器**

机制推理将条件—效应关系转化为因果解释问题；假设证伪利用对照、消融或被排除的替代解释判断哪种模型受证据支持；定量推导要求先选择并连接公式或原理，而非仅代入数字；边界校准定位假设失效、参数跨越阈值或混杂因素不可忽略时的结论边界。系统采用保守产出策略，只使用骨架抽取时推荐且有证据支持的视角，每篇论文在每个视角下最多生成一题。

> 直观理解：同一篇论文不必强行覆盖四种题型：例如没有数值关系的论文就不应硬造计算题。保守生成以较少数量换取题型与证据匹配，避免模型编造不存在的机制、公式或反事实条件。

**3. 骨架落地的双层质量控制**

第一层使用规则检测格式错误、来源泄露、外部图表依赖、异常长度和重复片段；第二层由大语言模型裁判联合读取问题、答案和骨架，分别判定问题自包含性、问题—骨架一致性、答案连贯性及答案的证据支持性。答案生成器本身不读取骨架，而审核器读取骨架，从而将可作答性测试与来源事实核验分开。

> 直观理解：规则适合发现明显坏格式，却无法判断一个科学解释是否真的由论文支持；骨架裁判补上了语义和逻辑审核。将“闭卷答题”与“开卷核验”分离，还能同时检查题面是否充分以及答案是否忠于来源。

**训练与推理**

数据合成阶段按“论文筛选与规范化→骨架抽取→受支持视角的问题生成→无骨架条件下的答案生成→骨架约束审核→去重与去污染”顺序离线执行。这里的骨架只服务于生成和审核，不作为最终问答样本中答题模型可见的附加输入，因此最终样本能够直接用于常规指令微调。

微调阶段使用LlamaFactory训练，开启thinking mode，并对Spark-234K及各基线训练集统一进行下游评测集去污染，以保证数据比较不由测试泄漏驱动。推理或评测时，微调后的模型仅接收自包含问题并生成答案，不需要访问原始论文或推理骨架；这与数据构建时答案模型的闭卷设置保持一致。

**复现信息**

复现时最关键的配置是：训练截断长度为32,768个token，共训练3个epoch，学习率为$5.0\times10^{-6}$，warmup比例为$0.05$；通常使用16张GPU、每卡批量为4并累积2步梯度，使用32张GPU时将梯度累积改为1，以维持相同的全局批量。训练启用FlashAttention-2、Liger Kernel、thinking mode和跨设备平均token统计；所有训练数据在训练前均与下游测试集执行13-gram精确匹配去污染。数据清洗中的语义去重在各学科内部进行，向量模型为Qwen3-Embedding-8B；原文节选没有明确给出生成模型、骨架抽取模型、裁判模型、解码参数、语义相似度阈值及各项审核阈值，因此这些部分仍需查阅完整附录后才能完全复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Spark-234K：由 $370K$ 篇过滤后的种子论文经合成流水线构建，最终保留 $234K$ 条指令样本；用于训练模型并分析学科分布、推理视角、长度、多样性、正确性、难度和自包含性。
- 通用科学推理基准：包括 GPQA-Main、GPQA-Diamond、SuperGPQA、SciBench、MMLU 和 MMLU-Pro；分别覆盖专家级科学选择题、综合科学知识、定量推理和广泛学科能力，用于测试训练数据对跨学科及高难度推理的迁移效果。
- 领域专门基准：包括 ChemBench、CS-Bench、PubMedQA、MedQA-US、GSM8K 和 MATH-500；覆盖化学、计算机科学、医学和数学，用于测试科学推理数据对专门领域及数学问题的迁移能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**六项基准宏平均分 Avg.**

对 GPQA-M、GPQA-D、SuperGPQA、SciBench、MMLU 和 MMLU-Pro 的分数取宏平均，用一个数概括模型在不同科学推理任务上的总体表现。 （越高越好；较高分数表示模型在多个基准上具有更稳定的综合能力，而不是只在单一任务上受益。）

</div>
<div class="metric-item" markdown="1">

**Vendi Score**

衡量数据样本的语义多样性；分数越高，通常表示样本覆盖的语义区域越广、重复性越低。 （越高越好；但它反映的是数据分布多样性，不直接证明每条样本都正确或更有教学价值。）

</div>
<div class="metric-item" markdown="1">

**Centroid Distance**

衡量数据表示相对于整体中心的分散程度，用于补充 Vendi Score 对数据覆盖范围的描述。 （越高越好；较高值表示样本在表示空间中更分散，但不能单独说明推理质量或下游准确率更高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三种基础模型在六项通用科学推理基准上的比较

<div class="result-value" markdown="1">

Spark-234K 在三个模型规模上都取得最高宏平均：Llama3.1-8B 为 $45.37$，Qwen3-8B 为 $60.83$，Qwen3-14B 为 $63.88$。在 Qwen3-8B 上，Spark-234K 的 $60.83$ 高于规模为 $1.2M$ 的 MegaScience 的 $56.36$，训练样本量却只有其约五分之一。

</div>

这说明在本文设置下，论文推理骨架和多视角生成带来的监督密度可能比单纯增加合成样本数量更有效。结果支持“较小但结构更好的数据集具有更高数据效率”，但不能证明 SPARK 在所有模型、训练配方或未评估基准上都必然优于百万级数据集。

<div class="result-source" markdown="1">

来源：第 5.2 节 Data Efficiency；表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For instance, fine-tuning Qwen3-8B on Spark-234K yields an average score of 60.83, compared with 56.36 for the strongest baseline.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 高难度科学推理与定量推理基准

<div class="result-value" markdown="1">

在 Qwen3-14B 上，Spark-234K 在 GPQA-M 和 GPQA-D 上分别达到 $53.71$ 和 $55.05$，并在 SciBench 上达到 $69.55$、MMLU-Pro 上达到 $73.68$。数据集难度分析显示，Spark-234K 中 L4 多步推理占 $58.5\%$、L5 研究级问题占 $34.6\%$，而 L1 事实回忆仅占 $0.02\%$、L2 常规计算占 $1.2\%$。

</div>

这些结果表明训练数据不仅提升了总体平均分，也与需要多步推理、专家科学判断和定量推导的任务相匹配。难度分布与性能提升之间是一致性证据，而不是因果证明；因为实验没有单独控制问题难度、模型先验知识或其他数据质量因素。

<div class="result-source" markdown="1">

来源：第 5.2 节 Performance on Challenging Reasoning Benchmarks；表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For Qwen3-14B, training on Spark-234K yields GPQA-M and GPQA-D scores of 53.71 and 55.05, respectively, outperforming models trained on substantially larger corpora.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 领域专门迁移能力

<div class="result-value" markdown="1">

Spark-234K 在三种基础模型的领域专门基准宏平均上分别达到 $66.41$、$76.61$ 和 $79.48$，均高于 MegaScience 的 $59.72$、$74.34$ 和 $77.82$。在 Qwen3-14B 的 MedQA-US 上，Spark-234K 得分为 $79.36$，MegaScience 为 $72.58$。

</div>

该结果说明由跨学科论文构造的训练数据能够迁移到化学、计算机科学、医学和数学等专门任务，而非只改善通用科学选择题。它支持跨领域覆盖的有效性，但医学等单一领域上的优势不能直接推出 SPARK 在每个学科或真实科研场景中都具有同等优势。

<div class="result-source" markdown="1">

来源：第 5.3 节 Domain-Specialized Results；表 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Notably, Spark-234K maintains a substantial advantage on domain-specific benchmarks such as MedQA-US (e.g., 79.36 vs. 72.58 for MegaScience on Qwen3-14B).

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

- SCP-116K：规模为 $274K$，是较小规模的科学推理数据集，用于检验 SPARK 相对于已有科学数据构造方法的增益。
- TextbookReasoning：规模为 $651K$，代表教材式科学推理数据，用于比较其与论文证据链驱动数据在难度和下游性能上的差异。
- MegaScience：规模为 $1.2M$，是百万级科学推理数据集，用于检验 SPARK 是否能以更少样本超过大规模数据。
- OpenScienceReasoning-2：规模为 $1.6M$，是比较对象中规模最大的已有数据集之一，用于测试数据质量和推理结构是否比单纯扩充样本数量更重要。

**实验想回答的问题**

- 与现有科学推理数据集相比，使用仅 $234K$ 条样本训练是否能在通用科学推理和定量推理基准上取得更高性能？
- SPARK 的推理骨架抽取和四视角问题生成是否分别改善数据质量、推理难度与下游模型性能？

**实验实现**

训练使用 Llama3.1-8B-Base、Qwen3-8B-Base 和 Qwen3-14B-Base，所有数据集比较采用相同训练超参数。评估采用零样本设置，在两组科学基准上进行；所有基准报告 avg@3 或 avg@5，具体规则位于附录 $D$。数据集质量分析中，随机抽取 $20K$ 个问题，由 Gemini-3.1 Pro 在不查看参考答案的情况下独立作答，再由 GPT-OSS-120B 判断语义等价性；难度分析对每个数据集随机抽取 $20K$ 个问题，并使用五级难度分类。消融实验统一使用 Qwen3-8B-Base，并在固定的 $40K$ 条训练样本上比较；数据效率实验则从 Spark-234K 中抽取逐步增大的随机子集，在 MMLU、MMLU-Pro、SciBench 和 GPQA-Diamond 上评估。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 固定 $40K$ 样本，替换合成单元：整篇论文、分块文本或摘要，分别替代推理骨架 | 完整 SPARK 的平均分为 $63.46$；改用整篇论文、分块文本和摘要后分别为 $54.31$、$57.83$ 和 $56.75$，相对下降 $9.15$、$5.63$ 和 $6.71$。 | 该消融主要隔离“以什么表示论文”为基础生成单元的影响。整篇输入可能使核心主张被长文档噪声淹没，分块会切断跨段落的主张—证据链，摘要则可能丢失推导细节；因此结果支持推理骨架在保持证据链和自包含性方面的作用。由于替代表示的具体提示词和信息量可能不同，结果仍不能完全排除输入长度或摘要质量造成的影响。 | 第 5.5 节 Unit of synthesis；表 4<br><span class="experiment-evidence">Whole-paper input performs worst (−9.15), as processing a long document diffuses the central claims and yields shallow questions.</span> |
| 固定骨架和总样本量，对四种问题生成视角进行留一消融 | 完整 SPARK 的平均分为 $63.46$；移除 mechanistic、falsification、quantitative 或 boundary 视角后，平均分分别为 $61.59$、$60.30$、$58.82$ 和 $61.19$，相对下降 $1.87$、$3.16$、$4.64$ 和 $2.27$。 | 该设计测试四种推理任务是否提供互补监督，而不是仅仅因为样本更多才有效。移除任何视角都会下降，说明机制推理、假设证伪、定量推导和边界校准可能覆盖不同能力；定量推导的下降最大，表明它在此评估协议中贡献最明显，但不能据此断言它在所有基准上都是唯一关键因素。 | 第 5.5 节 Question generation；表 4<br><span class="experiment-evidence">With data volume fixed, the performance gaps are smaller, yet removing any perspective still causes a clear drop, indicating that each contributes complementary signal.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该论文构建基于科学文献证据链的推理数据合成框架，重点提升语言模型的机制、证伪、定量推导和边界校准能力。; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`b6593095b2f715e36067b611139fb6a9b1d9d771d4ab329fecf6d390a018ca17`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
