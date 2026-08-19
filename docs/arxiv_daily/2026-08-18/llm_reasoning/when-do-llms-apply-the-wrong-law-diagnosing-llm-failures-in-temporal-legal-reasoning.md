---
title: "[论文解读] When Do LLMs Apply the Wrong Law? Diagnosing LLM Failures in Temporal Legal Reasoning"
description: "[arXiv 2608.14610][LLM Reasoning] 本文通过构建“时间适用法律判定”（TALD）基准，系统诊断大语言模型为何会忽略案件事实发生时间，并错误地优先适用最新法律版本。"
arxiv_id: "2608.14610"
announcement_date: "2026-08-18"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:24:11.748035+00:00"
source_sha256: "6d68f48857898eb35dc3c15dddde3025946759b0b0e6d1fbda2783c1f7a22f9d"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "大语言模型"
  - "法律人工智能"
  - "时间法律推理"
  - "时间上适用的法律确定"
  - "法律版本选择"
  - "不溯及既往"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.14610</p>

# When Do LLMs Apply the Wrong Law? Diagnosing LLM Failures in Temporal Legal Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Yiqian Huang, Shuyuan Zheng, Qianying Liu, Shaowen Peng, Yuntao Kong, Kotaro Funakoshi, Chuan Xiao, Manabu Okumura, Yang Cao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Institute of Science Tokyo；Osaka University；Nara Institute of Science and Technology；Center of Juris-Informatics, ROIS-DS</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.14610) · [PDF 下载](https://arxiv.org/pdf/2608.14610) · **关键词** 大语言模型, 法律人工智能, 时间法律推理, 时间上适用的法律确定, 法律版本选择, 不溯及既往<br>


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

本文通过构建“时间适用法律判定”（TALD）基准，系统诊断大语言模型为何会忽略案件事实发生时间，并错误地优先适用最新法律版本。

**不用术语来说**：法律会随时间修订，但审理案件时通常不能直接套用今天最新的条文，而要根据关键行为发生的日期判断当时哪个版本有效。例如，同一行为在修法前后可能具有不同的法律性质或后果；模型一旦选错法律版本，后续判决预测和法律分析即使推理过程看似完整，也会建立在错误前提上。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将下游法律判断之前的关键步骤独立定义为时间适用法律判定任务，即给定案件事实及相关事件日期，要求模型识别应当适用的成文法版本，并基于中国民事判决构建受控评测基准。
- 作者不止确认模型存在偏向最新法律的现象，还通过历史法条知识、法律时间效力理解、一般推理能力与推理路径多样性等诊断角度缩小原因范围，提出推理导向的强化学习可能使模型过度收敛于“适用现行法”这一默认路径；但该机制解释属于行为证据，而非训练干预支持的因果结论。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

法律人工智能研究使用大语言模型（LLM）处理法律判断预测、法条预测、罪名预测、判决书生成和合同分析等任务。此类任务通常从案件事实出发，识别相关法律依据并作出下游预测；但法律规则并非静态不变，案件应适用的法律版本取决于相关行为发生时的法律状态。本文因此将“时间上适用的法律确定”作为下游法律推理之前的基础能力，研究模型能否依据案件事实及其发生时间，选择具有正确生效期间的法条版本。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**时间法律推理**

时间法律推理是指根据法律事实发生的时间，判断当时应适用哪一套法律规则，而不是机械使用当前有效的法律。其核心困难在于同一法条可能经历修订，不同版本的内容相近但适用期间不同。

</div>
<div class="concept-item" markdown="1">

**不溯及既往原则**

不溯及既往原则通常要求法律事件依据相关行为发生时有效的法律进行裁判，即后续修订的法律一般不自动适用于更早发生的行为。因而，法律修订后的现行版本不一定支配历史案件。

</div>
<div class="concept-item" markdown="1">

**时间上适用的法律确定（TALD）**

TALD 是本文提出并评估的任务，要求模型从案件事实和相关事件日期出发，识别支配该案件的具体法律版本。它不同于直接预测罪名、刑罚或判决结果，因为它先单独检验“应使用哪一版法律”这一前置环节。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个由真实判决书提取或整理的案件实例，包括案件事实、法律相关事件的发生日期，以及候选法律或法条的历史版本，模型需要输出在该时间条件下具有法律适用性的版本标签。任务假设适用版本可以由成文法的内容及其生效、修订时间唯一确定，因此答案具有客观可验证性。本文关注的是版本选择本身，而不是在确定版本后继续完成法律判断预测或法律分析。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

案件实例的输入信息，主要包括案件事实和法律相关事件的日期。

</div>
<div class="notation-item" markdown="1">

**$t$**

与案件法律适用相关的时间，通常指相关行为或事件发生的日期。

</div>
<div class="notation-item" markdown="1">

**$v$**

某一法律或法条的具体历史版本。

</div>
<div class="notation-item" markdown="1">

**$v^*(x,t)$**

案件输入 $x$ 在时间 $t$ 下唯一正确的法律版本，即 TALD 的目标输出。

</div>

</div>

**直接相关的工作**

- **LawShift（Han and others, 2025）**: LawShift 研究成文法修订对法律判断预测的影响，发现即使是先进模型也常常无法根据合成修订调整判断，而是依赖当前法律。本文将问题进一步拆解为 TALD，并在真实判决-derived 案件上直接检验模型能否选择时间上适用的法律版本，同时分析这种失败的根源。
- **CAIL2018（Xiao et al., 2018）**: CAIL2018 等早期法律判断预测基准从案件事实预测适用法条、罪名和刑罚，但通常把法律标签视为静态标签。本文指出，真实法律推理还必须区分具有不同生效期间的相近法条版本，因此 TALD 用于检验下游预测之前更基础的时间版本选择能力。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

法律判断预测、法律事实预测等任务都预设模型先找到了正确的法律依据。由于法律具有时间效力范围，相关行为发生在修法前时，旧版本仍可能支配案件；误用新版本并非简单的引用差错，而可能改变行为的法律定性和案件结果。因此，在法律大模型进入司法或法律服务场景前，必须单独检验其能否依据事实发生时间选择适用版本。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **通用大语言模型法律推理**：现有研究使用大语言模型处理法律判断预测、事实预测、裁判意见生成和合同分析等任务，通常让模型根据案件事实生成结论或法律分析。这类方法展示了模型的法律应用潜力，但往往没有把“先确定哪个时间版本的法律有效”作为独立且可控的评测环节。
- **LawShift等时间维度评测**：少量研究开始考察法律变化对模型判断的影响，其中LawShift通过合成的法条修订测试模型能否相应调整法律判断，并发现先进模型仍常依据现行法作答，而未采用题目给定的修订规则。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有法律大模型研究主要评价最终预测或生成质量，没有隔离时间适用法律选择这一步，因而难以判断错误究竟来自选错法条版本，还是来自后续的事实认定与法律推理。
- LawShift揭示了模型面对法条变更仍锚定现行法的现象，但没有解释失败根源，无法区分模型是缺少历史法条知识、不理解法律的时间效力，还是形成了偏向最新法的任务特定推理策略；因此也难以据此设计有针对性的纠正方法。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少一个能够控制案件时间与候选法条版本、直接测量模型选法能力的任务，也缺少对“最新法偏置”成因的系统诊断。尤其尚不清楚，这种偏置是知识或规则理解不足，还是一般推理训练所塑造的窄化决策策略；后者意味着提高通用推理能力未必能改善时间法律推理。

</div>
<div markdown="1"><span>核心问题</span>

给定案件事实及具有法律意义的事件日期，大语言模型能否选出当时真正适用的成文法版本；如果模型系统性地误用最新版本，这一失败主要由历史法律知识缺失、时间效力规则理解不足，还是由强化学习塑造的推理路径收敛所导致？

</div>
<div markdown="1"><span>作者直觉</span>

作者选择先研究“适用哪一版法律”，是因为它位于完整法律推理链的上游，能够把选法错误与后续判断错误分离。再通过分别探测历史法条知识、时间规则理解和推理路径多样性，可以逐层排除表面原因：若模型知道旧法且理解不溯及既往原则，却仍持续选择新法，那么更合理的解释便是模型的默认推理策略发生了偏移。作者进一步以推理路径熵的变化提供行为层面的线索，直观上即强化学习可能让模型更擅长沿少数高奖励路径作答，却减少了对旧法等备选路径的探索。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是提出一个需要训练的新模型，而是建立一套诊断流程，用于判断大语言模型能否根据案件中的时间信息选择法律的正确历史版本。作者首先将“时序适用法律判定”形式化为 TALD 任务：输入案件事实 $F$ 与用户法律问题 $Q$，模型需要对候选法律集合 $N=\{1,\dots,n\}$ 中的每部法律，给出应适用的版本 $y_i$；若该法律不应被引用，则令 $y_i=-1$。随后，作者从中国裁判文书网构造包含新法适用案件与旧法适用案件的平衡数据，并用统一的提示方式测试通用推理模型和法律专用模型，最后通过准确率、版本方向错误分类以及额外的法律知识问答，区分模型是“不知道法律的时间效力规则”，还是“知道规则但没有正确应用”。

通俗地说，该方法把通常混在一起的法律推理拆开，先只检查第一道关口：模型有没有拿对法律版本。即使模型对合同、物权等实体问题的后续分析看似合理，只要它把 2021 年前发生并应受旧法调整的事实直接套入《民法典》，整个法律结论仍可能建立在错误依据上；因此，TALD 评测关注的是“先选对哪一版规则”，而不是完整判决是否写得像法官。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造案件查询与版本标签

利用中国民事判决的标准化结构，通过正则表达式自动抽取案件事实 $F$ 和原告诉讼请求并组成查询 $(F,Q)$，同时抽取判决引用的民事法律版本作为真实标签 $\boldsymbol{y}$。两名法律专家再通过随机抽样交叉核验自动抽取的准确性。

<div class="method-step__io" markdown="1">

**输入**：来自中国裁判文书网的中国民事判决文书。<br>
**输出**：以案件事实和法律问题为输入、以适用法律版本序列为标签的 TALD 样本。

</div>

**直观理解**：可以把一份完整判决拆成“给模型看的案情和问题”与“法院实际采用的法律版本”两部分；后者相当于标准答案。专家抽检用于确认自动拆分没有把文书字段或法条版本识别错。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立新旧版本平衡数据集

作者将 26,000 份民事判决均衡划分为 post-Code 与 pre-Code 两部分：前者适用 2021 年施行的《中华人民共和国民法典》，后者适用《物权法》《合同法》等先前单行法。为进行细粒度对照，作者把《民法典》视为多个与旧单行法对应的法律单元，例如物权编对应原《物权法》、合同编对应原《合同法》。

<div class="method-step__io" markdown="1">

**输入**：完成自动抽取和专家抽检的 TALD 样本。<br>
**输出**：规模相等、法律领域具有版本对应关系的新法适用集与旧法适用集。

</div>

**直观理解**：这种配对尽量让两组案件的法律主题相近，而主要差别集中在“应当用新法还是旧法”。因此，新旧两组的巨大性能差距更能指向时间版本偏差，而不只是某一法律领域本身更难。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行模型版本判定

将每个查询 $(F,Q)$ 分别交给 GPT-5.4、Claude Opus 4.6、Gemini-3.1-Pro、DeepSeek-V3.2、GLM-4.7、Qwen3 不同规模版本以及 LegalOne-8B，默认使用各模型可用的最高推理强度。模型输出其认为应参与法律推理的法律及对应版本，整理为预测序列 $\hat{\boldsymbol{y}}$。

<div class="method-step__io" markdown="1">

**输入**：每次运行从 post-Code 与 pre-Code 中分别随机抽取的 100 个案件，共 200 个平衡测试案件。<br>
**输出**：每个模型在新法案件和旧法案件上的法律版本预测。

</div>

**直观理解**：模型面对的是案情和诉求，而不是法院已经选好的法条；它需要先找到相关法律领域，再决定该案件发生的时间应落在哪一个版本的有效期内。统一采用较高推理强度，是为了降低“模型没有认真推理”对诊断结果的干扰。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 评分并诊断错误来源

先用 TALD 准确率比较预测与真实引用集合中的法律版本，再分别观察新法集和旧法集表现；对错误预测进一步划分为 Old-to-New、New-to-Old 和 Non-Versional 三类。16 道专家题用于检查模型是否记得《民法典》时间适用规则，从而为“知识缺失”与“规则应用失败”提供区分依据。

<div class="method-step__io" markdown="1">

**输入**：模型预测 $\hat{\boldsymbol{y}}$、真实标签 $\boldsymbol{y}$，以及额外构造的 16 道二选一时间效力知识题。<br>
**输出**：总体及分组准确率、三类版本错误分布，以及关于模型是否具备必要时间效力知识的诊断证据。

</div>

**直观理解**：只看答错数量无法判断原因：模型可能根本不知道规则，也可能知道规则却习惯性选择最新法律。错误方向统计检查它是否总把旧法换成新法，知识题则单独检查它是否能够说出应遵循的时间规则。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### TALD 准确率

$$
\operatorname{ACC}(\hat{\boldsymbol{y}};\boldsymbol{y})=\frac{\sum_{i\in N}\boldsymbol{1}(y_i=\hat{y}_i\neq-1)}{\left|\left\{i\mid y_i\neq-1\text{ or }\hat{y}_i\neq-1\right\}\right|}
$$

**符号说明**

- $N=\{1,\dots,n\}$：候选法律单元的集合，共包含 $n$ 个可能被引用的法律或对齐后的法律领域。
- $\boldsymbol{y}=[y_1,\dots,y_n]$：真实适用版本序列，其中 $y_i$ 是法律 $i$ 的正确版本。
- $\hat{\boldsymbol{y}}=[\hat{y}_1,\dots,\hat{y}_n]$：模型预测的适用版本序列，其中 $\hat{y}_i$ 是模型为法律 $i$ 选择的版本。
- $y_i=-1$：真实法律推理不应引用法律 $i$；预测侧的 $\hat{y}_i=-1$ 同理表示模型未引用该法律。
- $\boldsymbol{1}(\cdot)$：指示函数：括号内条件成立时取 1，否则取 0。
- $\left|\left\{i\mid y_i\neq-1\text{ or }\hat{y}_i\neq-1\right\}\right|$：真实答案或模型预测至少一方引用过的法律单元数量，即真实引用集合与预测引用集合之并集大小。

<div class="equation-explanation" markdown="1">

**直观理解**：分子只统计“法律单元相关且版本也完全正确”的项目；分母统计真实答案或模型答案曾涉及的全部法律单元。因此，漏掉应引用的法律、额外引用无关法律、以及找到相关法律却选择错误版本都会降低得分。其结构类似带版本约束的集合交并比较，但交集中的项目只有在版本相同且不为 $-1$ 时才算命中。<br>
**原文位置**：第 2.2 节，公式（1）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文提供的是评测与故障诊断方法，没有基于 TALD 数据训练、微调或更新被测模型参数；所谓 TALD 的“目标”是在任务定义层面最大化 $\operatorname{ACC}(\hat{\boldsymbol{y}};\boldsymbol{y})$，它是评价模型输出的指标，而不是论文实际执行的梯度优化损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 版本对齐的 TALD 表示**

对每部候选法律 $i\in N$，标签 $y_i$ 表示该案应适用的具体版本；$y_i=-1$ 表示该法律不参与当前法律推理。作者把《民法典》中的物权编、合同编等视为可分别对齐旧《物权法》《合同法》的法律单元，使新旧制度能够在同一版本选择框架内比较。

> 直观理解：该表示不仅问模型“有没有提到某个法律主题”，还要求它在同一法律谱系中选中正确年代的版本。把《民法典》按对应领域拆开，可以避免把整部法典视为一个过于粗糙的标签。

**2. 方向性错误分类器**

对于模型遗漏的每个真实目标法律，作者按照预测与真实版本的关系进行归类：Old-to-New 表示真实答案是旧法而模型引用新版本，New-to-Old 表示真实答案是新法而模型引用旧版本，Non-Versional 表示模型答案只包含与目标法律不存在版本关系的其他法律。

> 直观理解：该模块区分“找到了同一家族但选错年代”和“连相关法律家族都没找到”。如果错误主要是 Old-to-New，就说明核心问题更接近偏爱最新法，而不是完全不懂案件涉及什么法律。

**3. 知识与推理解耦诊断**

作者除案件级 TALD 测试外，还由两名法律专家设计 16 道二选一题，覆盖中国法下《民法典》的时间适用规定。案件任务考查模型能否从具体事实提取法律相关时间并应用规则，知识题则更直接地测试其是否掌握规则本身。

> 直观理解：这相当于同时考“背得出公式”和“会不会做应用题”。若模型能答对规则题却在旧案中持续套用新法，则失败更可能发生在事实时间与法律规则的结合阶段，而非单纯知识记忆不足。

**训练与推理**

训练阶段：原文未报告对任何模型进行额外训练或微调。数据构造阶段从裁判文书中抽取 $(F,Q)$ 与真实版本标签 $\boldsymbol{y}$，并通过专家抽样交叉核验；另由两名法律专家编写 16 道时间适用规则二选一题。

推理与评测阶段：每轮分别从 post-Code 和 pre-Code 随机抽取 100 例，将共 200 个案件逐一输入各被测模型，并使用模型最高可用推理强度获得预测 $\hat{\boldsymbol{y}}$。每项实验独立重复四次并报告平均结果；随后按公式（1）分别计算新旧版本数据上的 TALD 准确率，并对错误进行 Old-to-New、New-to-Old 与 Non-Versional 分类。知识题与案件级结果联合使用：前者检验时间效力规则是否存在于模型知识中，后者检验模型能否从事实识别相关时间并将规则落实到具体版本选择。

**复现信息**

公平解释结果所需的关键设置包括：数据集共有 26,000 份中国民事判决，post-Code 与 pre-Code 两部分数量平衡；每次测试由两部分各随机抽取 100 例组成；实验重复四次并取平均；默认采用每个模型最高可用的推理强度。被测范围包含五个闭源或专有模型 GPT-5.4、Claude Opus 4.6、Gemini-3.1-Pro、DeepSeek-V3.2、GLM-4.7，三个 Qwen3 规模版本 235B、80B、30B，以及法律专用模型 LegalOne-8B。

原文节选没有给出正则表达式、提示模板、生成参数、模型服务版本日期、输出解析规则、专家抽检样本量及抽取一致性统计，因此无法仅凭所给章节完整复现。尤其需要注意，真实标签来自判决中实际引用的民事法律版本；这种设计适合诊断模型能否复现司法文书中的时间适法选择，但节选未说明如何处理判决漏引、多法并用、例外性溯及适用或引用本身可能有误的案件。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- TALD民事判决数据集：从中国裁判文书网收集并自动抽取案件事实、原告诉请和法院引用的民法版本，共含26,000份判决。数据在后《民法典》子集与前《民法典》子集之间保持平衡；前者以2021年施行的《中华人民共和国民法典》为标签来源，后者以《物权法》《合同法》等原单行法为标签来源。该数据集用于测试模型能否依据案件中的时间线索选择正确法律版本，其中旧版本子集尤其用于诊断模型偏向新法的问题。自动抽取结果由两名法律专家通过随机抽样交叉核验。
- 重复抽样测试集：每次实验分别从后《民法典》子集和前《民法典》子集随机抽取100例，构成200例的平衡测试集；常规实验重复四次并报告平均结果。第6节策略熵实验沿用旧版本子集，但表6改为三个随机种子并报告均值与标准误。
- 时间效力规则知识集：由两名法律专家设计16道二选一问题，内容覆盖中国《民法典》时间效力司法解释中的适用规则。它不直接测试案件裁判，而是隔离模型是否掌握追溯适用、不溯及既往及新旧法衔接等抽象规则。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**TALD准确率（ACC）**

模型为案件选择正确时间版本法律的比例。表5将其用于旧版本案件；表6还称其为sensitive-law recall TALD accuracy。它直接衡量模型能否避免把现行新法错误地套用于依法应适用旧法的案件。 （越高越好，因为更高值表示更多案件选择了金标准法律版本。）

</div>
<div class="metric-item" markdown="1">

**法条文本相似度（字符级F1、ROUGE-L、编辑相似度）**

把模型复述的预测法条或金标准旧法条与官方法条文本比较。字符级F1衡量字符内容重合，ROUGE-L侧重最长公共子序列，编辑相似度反映通过字符编辑把生成文本变为官方文本所需差异。三项指标共同用于诊断模型是否记得法条内容，而不是评估最终法律版本选择。 （越高越好，因为更高值表示模型复述内容越接近官方法条文本；但高相似度不等于模型能在案件中选对版本。）

</div>
<div class="metric-item" markdown="1">

**版本相关策略熵（$H^{ver}$）**

先在思维链中定位法律名称、时间标记、版本说明、溯及力和生效期间等版本相关位置集合$S_i$，再计算这些位置的平均token分布熵。对第$i$个回答，单位置熵为$H_{i,t}=-\sum_{v\in\mathcal{V}}p(v\mid y_{i,<t},x_i)\log p(v\mid y_{i,<t},x_i)$，版本相关熵为$H_i^{ver}=\frac{1}{|S_i|}\sum_{t\in S_i}H_{i,t}$；其中$x_i$是案件事实，$y_{i,<t}$是位置$t$之前的输出，$\mathcal{V}$是词表。 （不存在跨模型统一的越高越好关系。论文只在同一模型及同一干预轴内解释其变化：熵升高表示版本相关候选路径更具多样性，但过高的不确定性本身不是目标，也不保证准确率继续提高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 法条记忆与时间效力规则知识诊断

<div class="result-value" markdown="1">

多数模型能够较准确地复述金标准旧法条，且旧法记忆并不系统性弱于错误预测的新法条。例如DeepSeek-V3.2的金标准法条字符级F1为0.963，高于预测法条的0.901；Qwen3-235B分别为0.902与0.776。16题规则探针中所有模型准确率均高于0.80，GLM-4.7与Qwen3-235B达到1.00。

</div>

作者据此主张，TALD错误主要不是“模型没见过旧法”或“完全不知道新旧法衔接规则”，而是在具体案件中没有调用并组合这些知识。该实验只能削弱基础知识缺失这一解释，不能证明模型对所有法条均有可靠记忆，也不能排除复述指标未覆盖的细粒度语义误解。

<div class="result-source" markdown="1">

来源：第5.1节，表3；规则知识结果见表4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For example, DeepSeek-V3.2 obtains 0.963 character-level F1 on gold articles and 0.901 on predicted articles; Qwen3-235B obtains 0.902 on gold articles and 0.776 on predicted articles.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 默认提示下比较普通模式、推理模式、推理强度与模型规模

<div class="result-value" markdown="1">

更强的通用推理没有稳定提高旧版本TALD。超过半数受测配置中，推理导向模式反而更差；典型例子是Qwen3-80B从instruct模式的0.080降至thinking模式的0.028。各家族的较优默认结果也不总来自最大或推理最重配置，例如Qwen3-30B-instruct为0.292、GPT-5.4-high为0.237、Qwen3-235B-thinking为0.148。

</div>

作者将此结果解释为：增加一般推理能力或推理计算不会自动形成正确的新旧法适用政策，显式推理甚至可能强化“优先选择最新法律”的错误路径。不过，这些是配置间的行为比较，并非严格控制训练数据、解码器和后训练过程的因果实验，因此不能推出推理能力本身必然有害。

<div class="result-source" markdown="1">

来源：第5.2.1节，表5的Default列

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For example, Qwen3-80B drops from 0.080 in instruct mode to 0.028 in thinking mode.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 旧版本案件上的默认、弱、强时间法提示及版本相关策略熵

<div class="result-value" markdown="1">

任务特定提示显著改善多种推理配置：表5中DeepSeek-V3.2 reasoner由0.092升至0.436，GLM-4.7 thinking由0.080升至0.435，Qwen3-80B thinking由0.028升至0.512，Qwen3-30B thinking由0.020升至0.395；GPT-5.4-high在强提示下由0.237升至0.457。表6进一步显示，Qwen3-30B从无提示的准确率0.020、熵0.315提升到强提示的0.450、0.462。

</div>

作者据此认为，模型往往具备可被提示调动的推理容量，核心问题更接近任务特定推理政策偏置；纠正提示使模型重新考虑旧法、溯及力等替代路径。熵与准确率同步上升只是支持机制解释的行为证据，不证明熵增加导致准确率提高；Qwen3-235B在强提示下熵继续上升但准确率不再提高，也说明更高熵不是最终目标。

<div class="result-source" markdown="1">

来源：第5.2.2节表5；第6.2.2节表6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen3-30B improves from 0.020 accuracy and 0.315 entropy under no hint to 0.450 accuracy and 0.462 entropy under strong hint.

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

- 默认提示与弱提示、强提示：默认提示不给时间适用规则指导；弱提示提供简短法律原则提醒；强提示给出更详细的TALD专业指令。三者控制模型和测试案件不变，用于判断错误能否通过任务特定的推理政策指导得到纠正。
- 同一模型的普通模式与推理模式：例如DeepSeek-V3.2的chat与reasoner、GLM-4.7和Qwen3的instruct与thinking。该比较尽量控制模型家族，用于检验启用显式推理是否自然提高旧版本案件准确率。
- 同一专有模型的不同推理强度：Claude Opus 4.6比较low、medium、high和max，GPT-5.4比较none、low、medium和high，Gemini-3.1-Pro比较low、medium和high。它用于测试增加推理计算是否能解决TALD，而不是比较不同供应商的绝对能力。
- 同一Qwen3家族的235B、80B与30B配置：模型规模与instruct或thinking模式共同构成能力对照，用于检查更大模型或更强推理配置是否稳定优于较小、较弱配置。LegalOne-8B则补充检验法律领域专用模型是否自然具备正确的时间适用政策。

**实验想回答的问题**

- RQ2：模型在应适用旧法的案件中误用新法，主要是因为没有记住旧法条文或不了解法律时间效力规则，还是因为未能把已有知识正确应用到具体事实？
- RQ3：为什么更强或更显式的通用推理没有稳定改善时间适用法律判定（TALD），以及错误是否与版本相关推理路径的策略熵塌缩有关？

**实验实现**

模型覆盖GPT-5.4、Claude Opus 4.6、Gemini-3.1-Pro、DeepSeek-V3.2、GLM-4.7、Qwen3-235B/80B/30B及法律专用模型LegalOne-8B；默认使用各模型可用的最高推理强度。法条记忆探针仅针对先前答错的旧版本案件，要求同一模型分别复述自己错误预测的法条和金标准旧法条，再与官方文本比较。规则知识探针使用16道专家设计选择题。推理政策实验在旧版本子集上保持其他设置不变，仅调整模型模式、推理强度或系统提示。策略熵实验只统计思维链中的版本相关片段，并明确限制为同一模型内部比较，因为分词器、概率校准与解码实现会影响熵的绝对尺度。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Qwen3-80B：固定模型规模，对比instruct与thinking模式，并保持默认提示 | 旧版本TALD准确率从instruct的0.080下降到thinking的0.028，绝对下降0.052。 | 该对照主要隔离显式推理模式的影响：同一模型启用thinking并未修复时间适用判断，反而更频繁地走向错误版本。它支持“通用推理策略可能强化新法偏置”，但由于模式切换还可能改变解码和后训练行为，不能把全部差异归因于思维链长度。 | 第5.2.1节，表5的Default列<br><span class="experiment-evidence">For example, Qwen3-80B drops from 0.080 in instruct mode to 0.028 in thinking mode.</span> |
| Qwen3-30B：固定thinking模式，仅把系统提示从默认改为弱提示和强提示 | 表5中准确率由默认提示的0.020提高到弱提示的0.350，再提高到强提示的0.395；对应的独立三随机种子熵实验中，表6报告0.020、0.371、0.450的准确率以及0.315、0.425、0.462的$H^{ver}$。 | 该干预隔离时间适用指导的作用：模型参数与推理模式不变时，加入法律版本判断原则即可大幅恢复表现，并同时扩展版本相关推理路径。表5与表6数值不同，源于所报告实验协议不同，不能混作同一轮结果；两者共同支持趋势，但不应将差值直接合并。 | 第5.2.2节表5；第6.2.2节表6<br><span class="experiment-evidence">Qwen3-30B improves from 0.020 accuracy and 0.315 entropy under no hint to 0.450 accuracy and 0.462 entropy under strong hint.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper diagnoses LLM reasoning failures when selecting temporally applicable legal rules and evaluates this capability systematically.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`6d68f48857898eb35dc3c15dddde3025946759b0b0e6d1fbda2783c1f7a22f9d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
