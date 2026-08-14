---
title: "[论文解读] TsuGO: Probing Search Efficiency in LLM Reasoning via Go Life-and-Death Problems"
description: "[arXiv 2608.13221][LLM 评测] TsuGO以围棋死活题构造封闭、可验证且带对抗性的搜索空间，用于评估大语言模型能否有效生成候选、比较分支、检验应对并把推理资源持续投入正确路径。"
arxiv_id: "2608.13221"
announcement_date: "2026-08-14"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T02:54:23.474054+00:00"
source_sha256: "60028e588efc6b8842e4a857e1096cf0852faf2db31c39a0d586ab826b226120"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "大语言模型推理评测"
  - "过程级评测"
  - "搜索效率"
  - "思维链"
  - "搜索树"
  - "围棋死活题"
  - "推理资源分配"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.13221</p>

# TsuGO: Probing Search Efficiency in LLM Reasoning via Go Life-and-Death Problems

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Shunwen Bai, Ziping Ma, Chaoyang Zhang, Yarong Wang, Jiale Liu, Zhen Qin, Qingpei Guo</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Zhejiang University；Central South University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13221v1) · [PDF 下载](https://arxiv.org/pdf/2608.13221v1) · **关键词** 大语言模型推理评测, 过程级评测, 搜索效率, 思维链, 搜索树, 围棋死活题, 推理资源分配<br>


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

TsuGO以围棋死活题构造封闭、可验证且带对抗性的搜索空间，用于评估大语言模型能否有效生成候选、比较分支、检验应对并把推理资源持续投入正确路径。

**不用术语来说**：现有评测通常只看模型最后答得对不对，或生成答案用了多少文字，即使检查推理过程，也多半把它视为一条从题目通向答案的直线；但面对存在多种候选方案的问题，模型还必须决定先尝试哪条路、如何预判反方应对、何时放弃错误方向以及是否回到更有希望的分支。只看答案或文本长度无法判断模型是在有计划地搜索，还是碰巧试中了答案。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出TsuGO，将围棋死活题用作受控的过程级评测环境。此类题具有封闭、可验证的解空间和内在对抗结构，因而候选生成、应对检查、分支比较与回溯是求解所必需的过程，而非推理文本中偶然出现的现象。
- 作者提出搜索轨迹分析框架，把自由形式的思维链解析为过程搜索树，并以搜索效率衡量推理资源是否投向正确分支，同时以词元效率作为表面生成成本的参照，从而区分“写得省”与“搜得好”。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大语言模型推理评测正在从只检查最终答案，转向分析模型产生答案的过程。现有过程级评测通常沿单条思维链考察中间步骤是否正确、连贯或冗余，或者用可观察的文本长度衡量成本；但数学与逻辑基准中的许多题目可以通过一条静态推导路径完成，因而难以判断模型面对多个候选方向时，是否能生成候选、预判反方回应、比较分支并在失败后回溯。本文把这种跨多条可能轨迹组织探索并分配推理资源的能力称为搜索效率，即 $\mathrm{SearchE}$，并以围棋死活题构造过程级评测环境：死活题具有封闭、可验证且天然对抗的解空间，每一步都必须经受对手后续应对，因此分支探索是解题所必需的过程，而非思维链中偶然出现的冗余文本。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**思维链（Chain-of-Thought, CoT）**

模型在给出最终答案前生成的中间推理文本，用于呈现候选方案、判断依据和修正过程。本文不只评价这段文本是否连贯，还将其中的落子与应对关系解析成结构化搜索树。

</div>
<div class="concept-item" markdown="1">

**搜索树**

以问题初始状态为根节点、以候选行动及其后续回应形成分支的树状表示；一条根到叶的路径对应一种可能的推演。它使评测者能够观察模型何时找到正确候选，以及推理资源究竟投入了哪些分支。

</div>
<div class="concept-item" markdown="1">

**围棋死活题（tsumego）**

在受限局部棋形中判断一组棋能否存活，或能否被对手杀死的问题。由于解答必须考虑双方最强应对且结果可以验证，它适合把领域内的多分支对抗推演转化为可检查的搜索过程。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是经过验证的围棋死活题；论文概述说明题目会被渲染为五种模态，并在有界或开放的 $K$-Search 设置下交给模型求解，但所给章节未进一步定义五种模态及 $K$ 的具体含义。模型输出包括最终解答和自由形式的思维链；TsuGO随后把思维链解析为过程搜索树，联合最终正确性、$\mathrm{SearchE}$、词元效率 $\mathrm{TokenE}$ 及辅助诊断指标，评估模型是否尽早提出正确候选并持续把资源投入有效分支。该设置假定题目的解空间封闭且可验证，并利用双方交替行动的对抗结构，使候选生成、回应检查、分支比较和回溯成为必要操作；其目标不是单纯测量围棋胜负能力，而是在受控解空间内尽量区分领域知识与搜索组织能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathrm{CoT}$**

思维链，即模型生成的自由形式中间推理轨迹。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{SearchE}$**

搜索效率，描述模型能否跨多个候选分支组织搜索，并把推理资源集中到正确或有价值的分支。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{TokenE}$**

词元效率，即按可观察的输出词元成本对任务准确性进行归一化的效率指标。

</div>
<div class="notation-item" markdown="1">

**$K$**

概述中有界或开放 $K$-Search 设置涉及的参数；所给章节未明确说明其精确定义。

</div>

</div>

**直接相关的工作**

- **CoTJudger 与 ReEfBench**: 二者都属于过程级推理评测：CoTJudger依据依赖图分析必要推理和结构冗余，ReEfBench把推理轨迹映射为逻辑结构以研究效率与行为模式。它们主要分析单条推理轨迹是否正确、简洁和连贯，而TsuGO关注模型如何在多条竞争轨迹之间组织搜索与分配资源。
- **Tree-of-Thought 与 Graph-of-Thoughts**: 这类方法把中间思考显式组织成树或图，说明外部结构化搜索程序能够改善推理。TsuGO不以提供外部搜索程序为主要目标，而是评估模型在自身自由形式推理轨迹中是否已经表现出有效的内部搜索组织。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

随着思维链和延长推理被用于数学、代码及科学问题，评测不仅要判断最终答案是否正确，还需要判断模型怎样组织求解过程。真实的困难任务往往包含多个相互竞争的候选路径，模型必须探索备选方案、预测后续反应、验证局部结论并在失败后回溯；如果不能观察这些决策，就难以定位模型失败究竟来自知识不足、状态理解错误，还是搜索与推理资源分配失当，也无法据此改进训练数据和规划框架。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **结果正确性与词元效率评测**：GSM8K、MATH和ARC等传统基准主要依据最终答案是否正确评价模型；词元效率则进一步把准确性与可观察的生成词元成本联系起来，用较少文本获得正确答案通常被视为更高效。它们适合衡量结果和表面成本，但不会还原模型在多个候选分支之间如何移动。
- **单轨迹过程评测与步骤监督**：CoTJudger从依赖图判断必要推理和结构冗余，ReEfBench把推理轨迹映射为逻辑结构以分析效率与行为模式，过程监督或基于过程奖励模型的方法则对中间步骤提供逐步反馈。这类方法主要检查一条推理链是否正确、简洁且逻辑连贯，并识别哪些步骤必要、哪些步骤可以删除。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有过程方法通常隐含“有效推理是一条主要推导路径”的假设，因此容易把分叉视为冗余；然而在对抗性或多候选任务中，适度分叉本身是必要操作，真正需要评价的是模型是否优先探索有价值的分支、比较对手应对并及时回溯。忽略这一点会把必要探索与无效重复混为一谈。
- 最终准确率、思维链长度和词元效率只反映结果或表面文本成本，无法揭示正确候选出现得早还是晚、模型是否过早放弃关键分支，以及推理预算是否浪费在无效路径上。因此，更长的思维链或更高的词元效率都不必然意味着更好的搜索组织。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

大语言模型评测仍缺少一种受控且可验证的过程级设置，能够把领域知识影响与搜索组织能力尽量分离，并将自由文本推理映射到多分支解空间中，直接诊断候选生成、分支比较、响应验证、回溯以及跨分支资源分配。换言之，已有工作能评估“答得是否正确”和“单条推理链是否精炼”，却尚不能可靠评估“模型是否以合理顺序和合理预算搜索”。

</div>
<div markdown="1"><span>核心问题</span>

在一个解空间受约束、答案可验证且必须考虑对手应对的任务中，能否从大语言模型的自由形式思维链重建其搜索过程，并衡量模型是否较早发现正确候选、持续投入有产出的分支、及时修正错误方向，从而得到区别于最终准确率和词元效率的搜索效率评价？

</div>
<div markdown="1"><span>作者直觉</span>

围棋死活题适合作为切入点，不是因为研究目标是测试一般围棋棋力，而是因为每个落子都会引出对手回应，模型无法只给出一条未经检验的静态推导；它必须在有限候选中反复进行“提出走法、检查回应、比较变化、必要时退回”的操作。由于局面和解法可以验证，推理文本中的走法能够被组织成搜索树：若模型有计划，它会较早触及关键着法，并把更多后续分析留给能成立的变化；若模型接近无引导试探，其资源就会分散、延迟或遗弃正确分支。观察这棵树因此比单纯计算答案和词元数更接近搜索组织本身。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

TsuGO不是训练一种新的围棋求解模型，而是一套把大语言模型的自由文本推理转换为可比较搜索过程的评测方法。其端到端流程为：先将经过筛选和验证的围棋死活题统一表示为棋盘状态、候选点和参考解树，再以坐标、矩阵、图像或组合形式向模型提供棋盘、行棋方与任务指令；随后收集模型可观察的思维链或推理摘要，将其中的候选探索、变化阅读、局面判断和回溯操作解析成带时间戳的过程搜索树；最后同时计算首着准确率、搜索效率、轨迹结构与文本规模指标，从而区分“答案是否正确”“搜索资源是否投向了有希望的分支”和“为得到答案消耗了多少可观察文本”。
技术上，每条推理被表示为过程搜索树 $T=(V,E,\tau)$：根节点是初始棋盘，动作节点是模型提出或模拟的落子，评价节点是胜、负或未确定判断，根节点下的动作子节点构成首层候选集合 $C=\{c_1,\ldots,c_m\}$。直观地说，这一方法不只检查模型最后选了哪个点，而是把模型的解题文字还原成一张“走过哪些岔路、在哪条岔路投入多少、何时返回重搜”的路线图；因此，长思维链不会自动被视为更好，只有较早发现正确候选并减少错误分支浪费的过程才会得到较高搜索效率。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 死活题筛选与标准化

仅保留满足局部性、首着可确定性和可验证性的题目，并将每题规范化为SGF与JSON；JSON包含 $19\times19$ 棋盘矩阵、坐标、行棋方及参考解树，解树记录正确首着、主变化、有效替代、反驳线和失败标注。

<div class="method-step__io" markdown="1">

**输入**：公开死活题材料、古典题集和可追溯来源记录，以及相应的专家解答与围棋引擎分析。<br>
**输出**：具有统一棋盘状态、来源记录和可核验参考搜索空间的题目集合。

</div>

**直观理解**：这一步相当于先给每道题建立一份可复查的标准答案及错误原因清单。限制题目局部且首着有限，可减少广泛围棋知识对评测的干扰，让评测更集中于模型如何组织搜索。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多模态题面与候选空间构造

将同一局面渲染为符号坐标、网格矩阵、符号加网格、视觉图像以及符号加视觉五种形式，并设置 $K=4$ 与 $K=\mathrm{None}$ 两种条件；前者给出含正确点在内的四个首着候选，后者要求模型自行生成、比较并论证落子。

<div class="method-step__io" markdown="1">

**输入**：标准化棋盘状态、正确首着和经过标注的错误候选点。<br>
**输出**：结构相同但输入模态和候选约束不同的模型测试实例。

</div>

**直观理解**：$K=4$ 主要测试模型能否从少量选项中辨别正确点，$K=\mathrm{None}$ 则进一步测试模型能否自己提出候选并组织搜索。对同一局面采用不同表示，可以判断结果来自真实棋形理解还是坐标、版式等表面线索。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 可观察推理采集与原子步骤识别

提示词不强制规定推理格式或树搜索策略；提取器结合由开放式回答建立的领域先验词典 $\mathcal{D}$，按时间顺序从自由文本 $\mathcal{T}$ 中识别候选探索、变化阅读、局面评价和回溯四类原子步骤。

<div class="method-step__io" markdown="1">

**输入**：题面、行棋方、任务指令，以及模型输出的完整思维链或闭源模型提供的压缩推理摘要。<br>
**输出**：带有时间顺序、步骤类型、落子信息及胜负极性信息的结构化事件序列。

</div>

**直观理解**：模型可以自然地写出自己的解题过程，评测器再把“先看A点、发现失败、返回尝试B点”之类文字拆成标准事件。闭源模型的摘要只能被视为可观察证据，不能等同于其完整内部计算。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 过程搜索树提取与结构校验

基于时间与语义上下文推断动作节点的父节点和有向边，为评价节点赋予胜、负或未确定极性，并记录跨候选切换与回溯；随后强制根节点仅连接动作、评价节点必须为叶节点、未闭合分支补充未确定叶、同父重复动作合并且时间戳单调，最后从并行提取结果中经规则过滤和交叉验证选出最终树 $T=(V,E,\tau)$。

<div class="method-step__io" markdown="1">

**输入**：结构化事件序列、初始棋盘根节点和参考解树。<br>
**输出**：可用于统计候选顺序、分支资源、阅读深度、跳转和回溯行为的合法过程搜索树。

</div>

**直观理解**：自由文本可能省略结论、重复落子或突然切换讨论对象，因此不能直接计数。结构校验把这些文字整理成规则一致的树，同时保留不同分支中的再次访问，以免抹去真实搜索历史。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 搜索效率

$$
\mathrm{SearchE}=100\cdot\left(0.5(1-\mathrm{SWR})+0.3\,\mathrm{SFH}+0.2(1-\mathrm{SCR})\right)
$$

**符号说明**

- $\mathrm{SearchE}$：综合搜索效率分数，以百分制缩放。
- $\mathrm{SWR}$：Search Waste Ratio，错误候选分支所占的搜索资源浪费比例；数值越低越好。
- $\mathrm{SFH}$：Search First Hit，正确候选在首次候选探索中被命中的程度；数值越高越好。
- $\mathrm{SCR}$：Search Correct Rank，正确候选在搜索顺序中的归一化排名代价；数值越低表示越早搜索正确候选。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把三种互补行为合成一个总分：一半权重用于惩罚在错误分支上的资源浪费，另外两部分奖励较早发现正确候选。作者称 $\mathrm{SFH}$ 比 $\mathrm{SCR}$ 更直接反映早期正确候选直觉，因此分别赋予 $0.3$ 和 $0.2$；这里的加权规则是评测定义，不是通过模型训练学习出来的目标。<br>
**原文位置**：第4.4节 Metrics

</div>

</div>

<div class="equation-block" markdown="1">

#### 令牌效率

$$
\mathrm{TokenE}=100\cdot\frac{A}{A+\mathrm{ITT}/1000},\qquad A=100\cdot\mathrm{Acc}
$$

**符号说明**

- $\mathrm{TokenE}$：相对于可观察推理令牌成本的准确性效率分数。
- $A$：百分制准确率量，即准确率乘以 $100$ 后的数值。
- $\mathrm{Acc}$：首着答案准确率。
- $\mathrm{ITT}$：Inference Total Tokens，模型可观察推理输出的总令牌数。

<div class="equation-explanation" markdown="1">

**直观理解**：该式在准确性收益与推理文本成本之间形成比值：准确率不变时，$\mathrm{ITT}$ 越大，$\mathrm{TokenE}$ 越低；令牌数不变时，准确率越高，分数越高。但它只反映可观察文本的成本，不能判断令牌是否被用在正确分支上，也不能代表闭源模型未公开的内部计算量。<br>
**原文位置**：第4.4节 Metrics

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。TsuGO是数据集与过程级评测框架，不训练被评模型，也没有通过梯度优化 $\mathrm{SearchE}$ 或 $\mathrm{TokenE}$；两式均为推理完成后的诊断性评分。文中使用LLM提取器将自由文本转成搜索树，但所给章节未报告针对本任务训练或微调该提取器的损失函数，因此不能把指标公式解释为训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 受控且可验证的死活题空间**

数据模块以局部性、首着可确定性和可验证性为筛选条件，并为每题保存能够支持答案评分与过程核验的参考解树。错误候选由局部显著但战术上错误的点、常见业余误判或可被反驳的表面先手构成；候选条件采用 $K=4$ 和 $K=\mathrm{None}$，另以旋转、镜像、颜色反转、坐标重标和候选顺序置换检查表面记忆与顺序偏差。

> 直观理解：死活题的对手会选择最强应手，因此模型不能只给出一条看似合理的线路，而要确认候选能够经受反驳。参考解树使这种对抗搜索可以核验，受控候选则把“识别好候选”和“自主产生候选”拆开测量。

**2. 基于LLM的过程搜索树提取器**

提取器把推理文本映射为 $T=(V,E,\tau)$：$V$ 包含根、动作与评价节点，$E$ 表示推理中的父子关系，$\tau$ 给出严格递增时间；动作节点记录行棋方 $\mathrm{side}(a)$ 与位置 $\mathrm{pos}(a)$，评价节点记录 $\mathrm{polarity}(j)\in\{\textit{win},\textit{lose},\textit{undetermined}\}$。同一父节点下的重复动作合并，不同分支内的重访仍分别保留；并行提取结果经结构规则过滤和交叉验证后确定。

> 直观理解：这一模块是从自然语言到可计算指标的桥梁。它不仅抽取模型提到的落子，还要判断落子属于哪条变化、模型何时否定该变化，以及何时返回之前的候选，否则无法可靠估计分支资源分配。

**3. 搜索效率与令牌效率诊断**

$\mathrm{SearchE}$ 综合错误分支资源浪费、正确候选是否首次即被命中，以及正确候选出现的搜索排名，其中错误浪费权重为 $0.5$、首次命中权重为 $0.3$、正确排名权重为 $0.2$。$\mathrm{TokenE}$ 则把答案准确性与可观察的总推理令牌 $\mathrm{ITT}$ 联系起来；二者分别刻画搜索组织与文本成本，不能互相替代。

> 直观理解：少写文字可能只是没有充分验证，写很多文字也可能是在错误分支上反复消耗。因而该框架用一组指标检查“搜索方向是否好”，再用另一指标检查“可观察文字成本是否高”，避免把两种效率混为一谈。

**训练与推理**

评测推理时，系统向模型提供棋盘、行棋方和任务说明，不指定思维链格式或树搜索算法；在 $K=4$ 条件下还提供四个首着候选，在 $K=\mathrm{None}$ 条件下由模型自行提出候选。模型输出最终落子以及可公开的完整推理内容；若闭源接口只返回压缩摘要，则仅把摘要作为候选提出、变化阅读、局面判断和分支切换的可观察痕迹。之后，提取流程按时间扫描文本，建立动作与评价节点、推断父边、记录回溯，补齐未确定叶并执行结构校验，再以参考首着和参考解树计算答案与过程指标。
该流程的核心边界是“评估可观察推理”，而不是声称恢复模型真实内部状态。完整思维链模型与摘要模型的候选和分支结构仍可分析，但依赖文本长度的 $\mathrm{ITT}$、$\mathrm{IPN}$ 和 $\mathrm{TokenE}$ 不应跨这两类输出直接比较；非LLM搜索基线也只能比较搜索侧指标，因为其过程不是令牌驱动的，而KataGo没有暴露与思维链同构的内部决策记录。

**复现信息**

数据方面，完整整理池含 $1{,}500$ 道题并提供五种输入形式；主评测从三个实际评估的难度层级各抽取 $200$ 道，共 $600$ 道，其余更难子集留待未来模型。难度结合人类棋力段位、参考主线深度和似是而非的错误候选确定；同一题在符号、网格和视觉表示下保持局面结构一致。为公平解释结果，还应保留两种候选设置，并使用旋转、镜像、颜色反转、坐标重标及候选顺序置换检查记忆、坐标捷径和答案顺序偏差。
提取可靠性方面，最终树由并行提取器经规则筛选和交叉验证得到；作者在抽样的 $300$ 道题上使用两名人类专家并辅以KataGo进行核验，报告Gemini-2.5-Pro与人工标注达到 $93\%$ 至 $98\%$ 的一致率，并说明区间来自自由文本的语义歧义。该数字支持提取器具备较高一致性，但并不证明树等同于模型内部搜索；复现时还必须执行根节点类型、评价叶节点、未闭合分支补全、同父重复动作合并和时间戳单调等结构约束。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- TsuGO 围棋死活题评测集的抽样子集：共 600 题，Easy、Medium、Hard 各 200 题。难度分层用于检验搜索空间扩大后性能是否稳定；同一批问题分别在 $K=4$ 候选选择和 $K=\mathrm{None}$ 开放生成条件下评测，以区分“从给定选项中辨别”与“自行生成、排序并验证候选”的能力。原文节选没有提供训练集、验证集或测试集的正式划分，因此不能把这 600 题解释为完整数据集规模。
- Symbolic 输入模态：过程指标统一基于符号化棋盘输入计算，以便从思维链中解析搜索轨迹并比较不同模型的树结构；总体准确率则对模型可用的输入模态取平均。它不是另一套独立数据集，而是承担过程级可比性控制的评测表示。
- 聚合过程搜索树：由模型思维链解析得到，并在 Figure 4 中按模型及 $K$ 设置聚合。节点大小表示平均子树资源权重，颜色表示胜负极性，用于定性检查资源是集中到少数可验证候选，还是扩散到浅层错误分支。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy（Acc）**

最终答案正确率，并对模型可用的输入模态取平均。它回答模型是否解对，但不说明正确答案是通过有效搜索、猜测还是利用候选提示得到。 （越高越好，因为表示正确解决的死活题比例更大。）

</div>
<div class="metric-item" markdown="1">

**Search Efficiency（$SearchE$）**

论文的主要结构效率信号，由 $SWR$、$SFH$ 和 $SCR$ 聚合而成，用于衡量搜索是否较早找到正确候选、是否把后续资源持续投入有生产力的分支，以及是否形成与成功解题一致的搜索结构。节选没有给出三个分量的完整定义和聚合公式，因此不能据此复现精确计算。 （越高越好，因为更高值表示推理资源更集中地支持正确搜索方向，而非仅生成更宽或更深的轨迹。）

</div>
<div class="metric-item" markdown="1">

**Token Efficiency（$TokenE$）**

相对于思考 token 成本的准确率，用来衡量单位推理开销带来的最终正确性。它主要反映成本效率，不能单独判断 token 是否被分配到正确候选或有效验证步骤。 （越高越好，因为相同 token 成本下正确率更高，或相同正确率下消耗更少；但高值不必然代表搜索组织更好。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 当前模型的总体解题稳定性，重点比较最强开放模型、最强专有模型及开放困难条件

<div class="result-value" markdown="1">

作者报告：在 $K=4$ Easy 上，最强开放模型 Kimi-K2.5 的准确率仅为 52.0；Gemini-3.1-Pro 在该条件达到 80.0，但到 $K=\mathrm{None}$ Hard 时降至 19.0。说明即使领先模型也无法在候选移除和难度增加后保持稳定。

</div>

这表明模型在有候选时可能利用棋形知识或选项线索完成判别，但开放条件要求自行提出并验证正确落点，暴露出更明显的搜索控制缺陷。该结果证明的是现有系统在这套 600 题评测上的稳定性不足，并不证明模型完全没有围棋知识，也不能直接外推到所有逻辑推理任务。

<div class="result-source" markdown="1">

来源：Section 5.2, Main Results；Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Even under K=4 Easy, the strongest open model, Kimi-K2.5, reaches only 52.0 accuracy; Gemini-3.1-Pro reaches 80.0 but falls to 19.0 on K=None Hard.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 无引导 MCTS、LLM 与神经网络引导 KataGo 的搜索定位

<div class="result-value" markdown="1">

在 Hard 条件下，MCTS/UCT 的准确率从 $K=4$ 的 22.0 降至 $K=\mathrm{None}$ 的 1.0，而 KataGo-b18 在相同 200 次访问预算下分别达到 58.0 和 43.0。作者据此判断，较强 LLM 虽优于盲目搜索，但仍明显落后于稳定的神经引导搜索。

</div>

MCTS 的开放搜索崩溃说明仅扩大搜索树而缺乏可靠方向并不足以解决问题；KataGo 的高结果则说明该任务在有限访问预算下并非不可解，关键在搜索引导质量。由于 LLM 与两种搜索器的计算单位不同，这一比较只能定位搜索行为，不能宣称 KataGo 在相同算力或时间成本下必然更优。

<div class="result-source" markdown="1">

来源：Section 5.3, Insight；数值见 Table 3 的 Search Baselines/Hard 行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MCTS reaches mid-tier LLM accuracy under K=4 but drops to single digits without candidates, showing that unguided expansion cannot maintain direction in open space.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### $SearchE$ 与 $TokenE$ 对最终正确率的解释关系

<div class="result-value" markdown="1">

作者报告 Figure 5 中 $SearchE$ 相对于准确率的聚类比 $TokenE$ 更紧，因而把 $SearchE$ 解释为更一致的过程成功信号；主表也显示短输出或较高单位 token 效率不必然伴随有效搜索。

</div>

直观上，少花 token 只说明成本较低，不说明资源是否用在正确候选上；$SearchE$ 直接检查分支选择与持续投入，因此更接近论文要测量的“搜索智能”。不过节选没有给出相关系数、回归结果或显著性检验，所以“更强”在这里主要是作者依据图形分布作出的经验判断，而非已报告统计检验的结论。

<div class="result-source" markdown="1">

来源：Section 5.3, Insight；Figure 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Figure 5 shows tighter clustering around accuracy for SearchE than TokenE, indicating stronger alignment with task success.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 计算公平性有限：MCTS、KataGo 使用每题 200 次 playout/visit，而 LLM 使用思考 token，二者不是等价预算；专有模型的规模数据还是由摘要信息推导并被排除在排名之外。因此实验能比较搜索组织的位置，却不能给出严格的等算力、等延迟或等成本结论。
- 节选缺少若干复现与统计信息，包括完整数据构建及划分、提示模板、采样参数、最大输出长度、重复试验次数、误差区间和显著性检验；Figure 5 关于 $SearchE$ 更贴近准确率的结论也未附相关系数。另一个领域模型 Logos 因常继续整盘对局或落子到局部死活区域之外，输出不适合轨迹分析，说明评测协议与专门模型的输出形式之间仍可能存在适配偏差。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- MCTS/UCT（Smargo 实现）：每题采用 200 次 playout/visit 的无引导搜索参照。它用于定位模型是否仅接近盲目扩展，而不是提供 token 等价的速度比较；其候选移除后的性能尤其能检验无可靠先验时是否会失去搜索方向。
- KataGo-b18：每题同样采用 200 次访问的神经网络引导围棋搜索参照。它代表具有领域策略与价值先验的定向搜索，可判断任务是否能在有限搜索预算内被良好求解，并量化大语言模型距离稳定、问题自适应搜索控制还有多远。
- 开放推理模型组：Kimi-K2.5、Qwen3-VL Thinking、MiniMax-M2.5 和 DeepSeek-R1-0528。该组用于检验显式长推理是否带来更好的搜索组织，并比较模型规模、思维链长度与实际搜索效率是否一致。
- 开放非推理与专有模型组：包括 GLM-4.6V、DeepSeek-V3.2、Gemini-2.5-Flash 和 Gemini-3.1-Pro-Preview。前者帮助判断长推理标签是否为高搜索效率的必要条件，后者提供更强闭源系统的参照；原文说明专有模型的规模指标由摘要信息推导且不参与排名。

**实验想回答的问题**

- 当前大语言模型能否稳定解决围棋死活题，并且在候选受限的判别式设置与无候选的开放搜索设置中，表现出有效的候选生成、分支比较、对抗验证和回溯能力？
- 搜索效率指标 $SearchE$ 能否比仅反映答案正确率或单位 token 成本的指标更准确地揭示模型如何把推理资源分配给正确分支，以及大语言模型的搜索组织与无引导 MCTS、神经网络引导 KataGo 分别有多大差距？

**实验实现**

实验覆盖开放推理、开放非推理和专有模型。每个模型在 $K=4$ 与 $K=\mathrm{None}$ 两种条件下处理三个难度层级：前者提供四个候选，主要测试候选判别；后者不提供候选，要求模型自行生成、排序和验证落点。主表同时报告准确率、$SearchE$、$TokenE$，以及搜索树最大深度 $TMD$、单节点分支宽度 $TMF$、节点数 $TNC$、初始正确候选位置 $IPN$ 和千 token 计的 $ITT(k)$ 等诊断量。过程指标使用 Symbolic 输入，准确率对可用模态取平均；MCTS/UCT 与 KataGo 均以每题 200 次搜索预算运行。原文明确提醒这些搜索基线与大语言模型并非 token 等价，因此其作用是定位搜索组织水平，而不是进行等计算成本比较。节选未明确报告采样温度、最大输出 token、重复运行次数、置信区间或显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 候选约束消融：同一任务从 $K=4$ 改为 $K=\mathrm{None}$ | Kimi-K2.5 在 Easy 上的准确率从 52.0 降至 27.8，$SearchE$ 从 39.9 降至 26.4。该变化把“从四个给定候选中辨别”替换为“自行生成、排序并验证候选”，直接暴露开放搜索瓶颈。 | 该对照主要隔离候选列表对搜索空间的压缩作用。准确率和结构效率同时下降，支持模型不仅更难给出正确答案，也更难把过程资源维持在正确方向。不过它同时改变了任务接口和生成负担，不能被解释为只移除了一个内部模型组件。 | Section 5.2, Main Results；Table 3<br><span class="experiment-evidence">For example, Kimi-K2.5 drops from 52.0 accuracy and 39.9 SearchE on K=4 Easy to 27.8 and 26.4 on K=None Easy; GLM-4.6V nearly collapses across the open tiers, with SearchE approaching blind-search levels.</span> |
| 模型规模对照：Qwen3-VL-235B-Thinking 与 Qwen3-VL-30B-Thinking | 在 $K=\mathrm{None}$ Hard 上，235B 模型的准确率为 7.2、$SearchE$ 为 7.3；30B 模型的准确率为 3.6、$SearchE$ 为 10.5。较大模型获得更高最终准确率，却没有在该条件下获得更高结构搜索效率。 | 这一对照用于判断增大参数量是否自动改善搜索组织。结果显示规模可能提高部分解题能力，但不会保证资源分配更有效；因此参数量与搜索结构不能视为同一能力。由于两个版本的具体训练数据和训练流程在节选中未受控，该结果是模型家族内比较，而不是严格的仅参数量因果消融。 | Section 5.2, Main Results；数值见 Table 3 的两个 Qwen3-VL Hard 行<br><span class="experiment-evidence">Size alone is insufficient: Qwen3-VL-235B usually beats its 30B variant, yet both degrade sharply on open hard problems, pointing to search organization rather than parameter count or token volume.</span> |

**定性案例**

- Figure 4 的聚合搜索树显示：在 $K=4$ 下，候选约束使不同模型的树形较为相似；在 $K=\mathrm{None}$ 下，Kimi-K2.5 与 Gemini-3.1-Pro 更倾向于集中搜索少数候选并推进到验证阶段，而 GLM-4.6V 与 MCTS 把资源分散到多个浅层错误分支。该可视化为 $SearchE$ 提供行为层面的解释：有效搜索不是树越大越好，而是尽早集中到值得对抗验证的候选。聚合图会隐藏单题差异，因此它适合说明总体模式，不能证明每一道题都遵循同样轨迹。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该工作提出围棋死活题基准，从搜索组织和资源分配层面评测 LLM 推理过程。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`60028e588efc6b8842e4a857e1096cf0852faf2db31c39a0d586ab826b226120`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
