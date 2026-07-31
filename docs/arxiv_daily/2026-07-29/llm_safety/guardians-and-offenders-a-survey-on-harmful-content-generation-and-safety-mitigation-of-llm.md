---
title: "[论文解读] Guardians and Offenders: A Survey on Harmful Content Generation and Safety Mitigation of LLM"
description: "[arXiv 2508.05775][LLM 安全] 本文围绕大语言模型既可能生成有害内容、又可用于安全治理的双重角色，系统梳理无意伤害、对抗性越狱及检测、审核与预防策略，并据此归纳统一的研究版图与未来方向。"
arxiv_id: "2508.05775"
announcement_date: "2026-07-29"
primary_category: "llm_safety"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.328844+00:00"
source_sha256: "024f0a882c02d26996f99b147134a8c00ff26928709ac173ee983772560958f3"
tags:
  - "LLM 安全"
  - "对齐 / RLHF"
  - "LLM 评测"
  - "LLM 其他"
  - "大语言模型安全"
  - "有害内容生成"
  - "毒性与偏见"
  - "越狱攻击"
  - "内容审核"
  - "安全缓解"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 安全 · arXiv 2508.05775</p>

# Guardians and Offenders: A Survey on Harmful Content Generation and Safety Mitigation of LLM

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-29</span>
<span><strong>作者</strong> Chi Zhang, Changjia Zhu, Junjie Xiong, Xiaoran Xu, Lingyao Li, Yao Liu, Zhuo Lu</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2508.05775v3) · [PDF 下载](https://arxiv.org/pdf/2508.05775v3) · **关键词** 大语言模型安全, 有害内容生成, 毒性与偏见, 越狱攻击, 内容审核, 安全缓解<br>


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

本文围绕大语言模型既可能生成有害内容、又可用于安全治理的双重角色，系统梳理无意伤害、对抗性越狱及检测、审核与预防策略，并据此归纳统一的研究版图与未来方向。

**不用术语来说**：大语言模型能够理解和生成复杂文本，因此既能帮助平台识别辱骂、偏见和骚扰，也可能在训练偏差、上下文误判或恶意诱导下生成这些内容。问题的难点不只是阻止模型说出某些词，而是要同时处理隐含语境、蓄意绕过防护的攻击以及多种社会伤害，并判断现有防御究竟覆盖了哪些风险、还遗漏了什么。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 以“伤害生成—安全缓解”的双重视角综合近期研究，将无意毒性或偏见生成、对抗性越狱与多模态攻击，以及分类、审核和预防等防御角色纳入同一分析框架。
- 通过三个研究问题整理模型类型、伤害类别和评估方法，分析大语言模型面临的主要安全挑战及其作为分类器、审核器、反制言论生成器和自适应预防系统的潜力，并指出应向动态、语境感知和可自我纠正的安全系统发展。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型（LLM）安全与有害内容治理领域。其核心背景是：LLM既可能凭借语境理解和文本生成能力充当有害内容的分类器、审核器与预防工具，也可能无意生成毒性、冒犯性或偏见内容，或在越狱攻击等蓄意操纵下绕过安全限制。相关风险不仅包括对个人造成心理伤害和错误信息暴露，也包括恶意宣传、欺诈等社会层面的危害。因此，论文从“危害生成者”与“安全促进者”两种角色统一考察LLM，重点梳理危害类别、攻击方式、评估方法以及检测、审核和预防策略。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**有害内容（harmful content）**

指可能伤害个人或社会的语言内容，本文明确涉及毒性言论、网络骚扰、冒犯性语言、偏见叙事、错误信息及可被用于恶意活动的文本。其判断往往依赖语境，而不只是检查某些敏感词。

</div>
<div class="concept-item" markdown="1">

**越狱攻击（jailbreak attack）**

指攻击者通过精心设计的输入或其他操纵方式，使已经设置安全限制的LLM仍然执行危险请求或生成有害内容。本文将其视为区别于无意毒性生成的一类蓄意对抗性风险，并关注多模态利用等更复杂形式。

</div>
<div class="concept-item" markdown="1">

**内容审核（content moderation）**

指识别、分类、过滤或干预不当内容的过程；LLM可在其中担任分类器、审核器、反制言论生成器或自适应预防系统。与传统规则或关键词方法相比，LLM的潜在优势是能够处理更细微且依赖上下文的表达。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文是综述而非提出单一预测模型：分析输入是近期关于LLM有害内容生成与安全缓解的研究，覆盖模型类型、危害类别、评估方法、无意毒性或偏见生成、对抗性越狱与多模态攻击，以及分类、审核和预防措施；分析输出是该领域的研究版图、主要安全挑战和LLM可承担的缓解角色。论文以三个研究问题组织任务：RQ1描述当前研究格局，RQ2识别LLM在有害内容方面的主要安全挑战，RQ3归纳LLM用于缓解有害内容的潜在作用。其基本场景同时包含正常使用下的非故意危害与攻击者蓄意操纵下的危害，并强调安全能力需要结合具体语境动态判断，而不能仅被视为静态输出约束。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathrm{RQ1}$**

关于LLM有害内容安全研究现状的问题，涵盖模型类型、危害类别与评估方法。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{RQ2}$**

关于LLM造成的主要有害内容安全挑战的问题，包括无意生成与越狱、多模态利用等对抗性攻击。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{RQ3}$**

关于LLM如何帮助缓解有害内容的问题，包括分类、检测、审核与预防等角色。

</div>

</div>

**直接相关的工作**

- **Vishwamitra et al. (2024)；Wang et al. (2024c)**: 引言将这些研究作为LLM利用语境理解能力识别和过滤问题内容、弥补传统方法在细微语义与上下文处理方面不足的依据；所给原文未提供论文标题及更具体的方法信息。
- **Chen et al. (2024)；Wang et al. (2024a)；Mangaokar et al. (2024)**: 引言将这些研究列为LLM可能因蓄意操纵而生成有害内容的相关工作，为本文讨论越狱和其他对抗性攻击提供背景；所给原文未提供各工作的具体攻击设计或实验结论。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

数字平台中的有害互动持续增加，而大语言模型扩大了内容生产和传播能力：模型可能无意生成毒性、冒犯性或偏见内容，也可能被攻击者通过越狱等手段操纵，进而造成心理伤害、错误信息暴露，并为恶意宣传或欺诈提供便利。与此同时，传统方法常难以处理依赖语境和细微表达的有害内容，因此现实治理又需要借助大语言模型更强的语言理解能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **传统有害内容识别与过滤方法**：通过预设规则、词汇信号或既有分类机制判断内容是否有毒、冒犯或带有偏见，再对命中内容进行过滤或处置；这类方法构成了平台内容治理的既有基础。
- **基于大语言模型的安全缓解方法**：利用大语言模型的上下文理解与生成能力执行有害内容检测、分类和审核，或通过反制言论与预防机制干预风险内容；相关研究也采用人类反馈强化学习、提示工程和安全对齐来降低模型自身生成有害输出的概率。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 传统方法往往难以识别依赖上下文、隐喻或细微语义的有害表达，可能导致漏检或误判，无法充分应对大语言模型生成的灵活语言形式。
- 现有研究分别讨论无意毒性、偏见生成、文本或多模态越狱以及检测和审核，风险与防御缺少统一梳理；同时，当前评估方法仍有局限，因而难以完整比较不同模型、伤害类别和缓解策略，也不足以刻画不断变化的对抗行为。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一个同时覆盖大语言模型“伤害来源”与“安全工具”两种身份的综合框架，用来贯通无意有害生成、蓄意越狱攻击、多模态利用和检测—审核—预防链条，并系统对应模型类型、伤害类别与评估方法，从而揭示现有防御的覆盖范围及空白。

</div>
<div markdown="1"><span>核心问题</span>

本文具体回答三个相互衔接的问题：大语言模型有害内容安全研究目前由哪些模型、伤害类别和评估方法构成；模型在无意生成、对抗性越狱及多模态利用方面面临哪些主要挑战；大语言模型又能以何种方式参与有害内容的分类、审核和预防。

</div>
<div markdown="1"><span>作者直觉</span>

将模型视为同时存在的“违规者”和“守护者”，比只研究输出拦截更容易看清安全闭环：同一种上下文理解与生成能力，一方面可能放大偏见或被攻击者利用，另一方面也能识别隐含伤害、生成干预内容并调整防护。按风险产生方式与治理阶段统一整理文献，可以暴露攻防之间未被覆盖的接口，并为语境感知、动态适应和自我纠正的系统设计提供依据。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文是系统性文献综述，而非提出新的生成或防御模型。其端到端方法是：先在 OpenAlex 中用“LLM 相关词 AND 有害内容相关词”检索 2022 年 1 月至 2025 年 5 月 22 日的研究，再去重并依次进行标题—摘要筛选和全文资格审查，最后对纳入论文进行结构化、多标签编码，由此构建关于 LLM“加害者（Offender）”与“守护者（Guardian）”双重角色的文献版图。检索得到 3,347 条记录，去除 260 条重复记录后留下 3,087 条；GPT-4-turbo 初筛后保留 751 篇供全文审查，四位作者再排除 379 篇，最终语料库包含 372 项研究。原文证据：“From 3,347 records retrieved from OpenAlex, 260 duplicates were removed; 2,336 records were excluded at title-and-abstract screening; and 379 were excluded at full-text review, leaving 372 studies in the final corpus.”（图 1及第 2.3 节）
技术上，论文以四类有害内容——毒性内容、骚扰、冒犯性语言和偏见内容——作为组织框架，并将每篇研究按主要任务、有害内容类型、技术路线和 LLM 所扮演的角色进行编码。由于一篇论文可能同时研究多种伤害，类别采用多标签而非互斥划分；通俗地说，这套方法不是把论文强行放进唯一抽屉，而是给每篇论文贴上若干可重叠标签，再观察哪些问题、模型和治理手段受到较多关注。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 文献检索与候选集构建

在标题或摘要上执行“至少命中一个 LLM 词 AND 至少命中一个有害内容词”的布尔检索，并将发表日期限制为 2022 年 1 月至 2025 年 5 月 22 日。该查询返回 3,347 条候选记录。

<div class="method-step__io" markdown="1">

**输入**：OpenAlex 收录的论文和预印本元数据，包括标题、摘要、作者、DOI、日期等；检索词分为 LLM 词组和有害内容词组。<br>
**输出**：覆盖 LLM 有害生成、检测、分类、审核与越狱研究的初始候选文献集合。

</div>

**直观理解**：这一步像用两层筛网找论文：一层保证论文确实讨论大语言模型，另一层保证它涉及毒性、仇恨、骚扰、偏见、审核或越狱等安全问题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 规范化去重

将标题规范化，并结合作者列表与 DOI 匹配重复记录；共移除 260 条重复项。原文证据：“We remove 260 duplicates by matching on the normalized title together with the author list and DOI, leaving 3,087 unique records for screening.”（第 2.3 节）

<div class="method-step__io" markdown="1">

**输入**：3,347 条检索记录及其标题、作者列表和 DOI。<br>
**输出**：3,087 条唯一记录，进入相关性筛选。

</div>

**直观理解**：同一论文可能被不同来源重复索引，因此作者综合标题、作者和 DOI 判断是否为同一项工作，避免重复计数。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 两阶段资格筛选

第一阶段由 GPT-4-turbo 按高召回标准判断论文是否涉及 LLM 安全或完整性，排除 2,336 条后留下 751 篇；第二阶段由四位作者阅读全文并依据资格标准讨论解决分歧，再排除 379 篇。原文证据：“This stage excludes 2,336 records judged irrelevant and leaves 751 reports for full-text retrieval.”以及“this stage excludes 379 reports, yielding a final corpus of 372 studies.”（第 2.3 节）

<div class="method-step__io" markdown="1">

**输入**：3,087 条唯一记录的标题和摘要，以及随后取得的候选论文全文。<br>
**输出**：最终纳入的 372 项研究。

</div>

**直观理解**：机器先做宽松海选以减少人工工作量，研究者再阅读全文做最终裁决；高召回意味着初筛宁可暂时保留边界论文，也尽量不漏掉相关研究。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 结构化编码与文献版图综合

四位作者提取每项研究的主要任务、有害内容类型、技术方法、LLM 角色和模型家族；各组结果由两人手工核验，并使用附录 A 的结构化提示交由 GPT-4-turbo 再次检查。随后按技术方法、模型类型和伤害类别汇总，形成图 2 所示的多维分布与定性综合。

<div class="method-step__io" markdown="1">

**输入**：372 项纳入研究的全文，以及论文定义的伤害分类和 Guardian/Offender 角色框架。<br>
**输出**：带多标签的结构化文献语料，以及关于技术路线、模型家族、伤害类型和双重角色的研究版图。

</div>

**直观理解**：作者把每篇论文转换成统一的“信息卡片”，再按多个维度统计和比较。由于毒性、骚扰、冒犯和偏见可能同时出现，一篇论文可以拥有多个伤害标签，所以各类别数量不能相加得到论文总数。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文是系统性综述，没有训练新的 LLM、分类器或安全防御模型，也没有定义可优化的损失函数；GPT-4-turbo 被作为现成的相关性筛选器和编码复核工具使用，而非在本文语料上训练。综述的目标是提高检索覆盖率、保证纳入研究的相关性并形成一致的结构化编码，而不是通过梯度优化某个模型目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 可复现的 OpenAlex 布尔检索模块**

检索式由两个关键词集合组成：LLM 集合包含 GPT、Claude、LLaMA、Gemini、Qwen、large language model 等名称，有害内容集合包含 toxicity、hate speech、harassment、jailbreak、content moderation 等概念；标题或摘要必须同时命中两组。OpenAlex 同时索引同行评审论文与近期预印本，且查询接口开放。

> 直观理解：该模块决定综述最初能看到哪些论文。双组词的交集可降低只谈模型但不谈安全、或只谈网络伤害但不涉及 LLM 的无关结果。

**2. 人机协同筛选与质量控制模块**

GPT-4-turbo 仅承担标题—摘要层面的第一轮相关性分类，并采用高召回准则；全文资格审查由四位作者完成，分歧通过讨论解决。结构化编码结果还经过每组两人手工核验和 GPT-4-turbo 的提示式复查，原文同时承认自动摘要筛选可能引入偏差。

> 直观理解：模型负责处理数量庞大的粗筛任务，人类负责需要上下文判断的最终审查；多轮核验用于减少单个模型或单位编码者造成的遗漏和误判。

**3. 多标签伤害分类与双重角色编码模块**

伤害维度包括毒性内容、在线骚扰、冒犯性语言和偏见内容，类别被视为互补且可重叠；角色维度用“Good”表示检测、审核、预防和缓解等安全赋能，用“Bad”表示有害生成、偏见和越狱脆弱性。另行记录主要任务、技术方法以及 GPT、LLaMA、Claude 等模型家族。

> 直观理解：多标签设计承认真实伤害往往混合出现，例如一句话既可能带有毒性，也可能针对特定群体构成骚扰。Guardian/Offender 编码则把“LLM 制造风险”和“LLM 帮助治理风险”放入同一分析框架。

**训练与推理**

本文没有通常意义上的模型训练和部署推理流程。与“推理”最接近的环节是：把每条候选记录的标题和摘要输入 GPT-4-turbo，让其判断论文是否涉及 LLM 对有害内容的生成、检测、分类、审核或越狱；该判断只作为第一轮筛选，不能直接决定最终纳入。随后四位作者对保留论文进行全文审查，并对最终 372 项研究进行结构化人工编码；编码结果先由两人核验，再通过附录 A 所述的结构化提示让 GPT-4-turbo 复查。最终分析不是跨论文重新计算统一性能，而是汇总技术路线、模型家族、伤害类别和 Guardian/Offender 角色的分布并进行定性综合，因为不同研究的数据集、指标和实验设置不可直接对齐。

**复现信息**

复现时最关键的要素是：使用 OpenAlex；采用表 3 的两组关键词及“(LLM terms) AND (harm terms)”规则；将日期限定为 2022 年 1 月至 2025 年 5 月 22 日；依据规范化标题、作者列表和 DOI 去重；按图 1 执行标题—摘要初筛与全文审查；依照第 2.1、2.2 和 2.3 节定义进行多标签编码。需要注意两项解释边界：第一，原文节选没有完整列出全文纳入与排除标准，也未提供 GPT-4-turbo 初筛提示的具体文本，仅说明完整提示位于附录 A；第二，伤害分类是服务于文献组织的解释性框架，而非互斥的客观本体，因此图 2 的分类计数表示研究关注度，不能相加为 372，也不应被解释为现实伤害发生率。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**文献数量**

统计归入特定技术方法、模型类型、有害内容类型或 guardian/offender 角色的研究篇数，用于描述文献版图，而非衡量模型预测性能。 （无固定优劣方向；数量越高仅表示该主题受到更多研究关注，不代表方法更有效或模型更安全。）

</div>
<div class="metric-item" markdown="1">

**跨维度定性分布**

比较技术方法、模型家族和危害类别中的相对研究集中程度，以识别主流方向及研究不足。 （无固定优劣方向；分布偏斜用于揭示研究覆盖不均，不能直接解释真实风险发生率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 按技术方法汇总纳入研究，并比较提示工程、微调、对抗学习和架构重设计的研究覆盖。

<div class="result-value" markdown="1">

作者报告，提示工程与微调占据主要位置，尤其用于文本生成、内容审核和分类；对抗学习与架构重设计受到的研究较少。该分布表明现有工作更偏好无需从头训练或改动架构的低成本干预。

</div>

通俗地说，研究者更常通过“改变模型收到的指令”或“在已有模型上继续训练”来调整行为，而较少重做模型结构。这说明方法选择存在明显偏好，但不能证明提示工程或微调在安全性上必然优于其他路线，因为本节没有统一数据集、指标和控制变量下的性能比较。

<div class="result-source" markdown="1">

来源：Section 3, Figure 2 的第一幅极坐标图讨论

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Here, prompt engineering and fine-tuning dominate the methodological space, particularly in tasks related to text generation, content moderation, and classification.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 按被研究的模型类型汇总文献，比较 GPT、LLaMA、Claude、BERT、RoBERTa 及其他模型家族的覆盖程度。

<div class="result-value" markdown="1">

GPT 系列在纳入研究中占比最大，尤其集中于越狱检测与安全评估；LLaMA、Claude、BERT 和 RoBERTa 也较常出现，而 Gemini、Baichuan、Qwen 等模型研究不足。

</div>

这意味着当前关于风险和防御的知识主要来自少数模型家族。由 GPT 上得到的攻击成功模式或防御结论未必能直接推广到其他闭源模型、开源模型或语言文化环境；该结果反映的是文献覆盖偏斜，而不是 GPT 一定更危险或更安全。

<div class="result-source" markdown="1">

来源：Section 3, Figure 2 的第二幅图讨论

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GPT-based models account for the largest share of studies, especially in jailbreak detection and safety evaluations.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨技术方法、模型类型和危害类别比较 guardian 与 offender 两种研究角色。

<div class="result-value" markdown="1">

作者发现 guardian 取向的研究总体多于 offender 取向的研究；技术方法维度给出的示例计数为 287 篇“Good”对163篇“Bad”。

</div>

这表明文献更常研究如何让 LLM 检测、分类、审核或预防有害内容，而不是只研究其如何生成危害。但 287 对 163 是研究数量而非安全效果分数，不能据此推断现有防御已经超过攻击能力，也不能说明部署中的实际危害正在下降。

<div class="result-source" markdown="1">

来源：Section 3, Figure 2 综合讨论

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across technical methods, model types, and harm categories, studies emphasizing the guardian role of LLMs outnumber those treating them as offenders (e.g., 287 “Good” vs. 163 “Bad” in technical methods).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 作者明确指出，不同研究使用的数据集、评价指标和实验设置不一致，因此无法进行可靠的直接定量比较；本节的结论应理解为定性综合和总体趋势，而非统一基准上的性能排名。
- 所给章节未报告分类编码的一致性、各类别完整计数、置信区间或统计显著性，也未说明文献数量是否受发表偏差与模型流行度影响；因此 Figure 2 中的分布不能直接代表现实危害的发生率或防御效果。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。

**实验想回答的问题**

- 纳入文献在技术方法、模型类型与有害内容类型三个维度上呈现何种分布，由此可见哪些研究集中与空白？
- 现有研究更常将大语言模型视为有害内容的生成者（offender），还是用于检测、审核和预防有害内容的安全促进者（guardian）？

**实验实现**

这是系统性综述的景观分析，而非在统一数据集上开展的模型对照实验。作者将所收集研究沿三个轴进行编码和汇总：技术方法、LLM 模型类型、有害内容类型；同时依据研究强调模型生成危害还是促进安全，将其概括为 offender 与 guardian 两类。Figure 2 以多维图表呈现这些分类结果。所给章节未报告文献检索后的具体样本规模、训练/测试划分、统计显著性检验、统一评测流程或复现实验参数，因此不能把不同论文中的结果视为受控条件下的直接比较。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- Figure 2 将同一批文献同时投影到技术方法、模型类型和危害类别三个轴，并以 guardian/offender 角色观察各轴的非对称性。该可视化的价值是帮助识别“哪些问题被反复研究、哪些组合被忽略”；它不是单模型案例实验，也未提供因果证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：reused verified category during targeted regeneration
- 全文指纹：`024f0a882c02d26996f99b147134a8c00ff26928709ac173ee983772560958f3`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
