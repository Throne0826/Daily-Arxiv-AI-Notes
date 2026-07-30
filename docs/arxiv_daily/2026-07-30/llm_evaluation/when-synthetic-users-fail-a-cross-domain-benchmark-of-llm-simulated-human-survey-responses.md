---
title: "[论文解读] When Synthetic Users Fail: A Cross-Domain Benchmark of LLM-Simulated Human Survey Responses"
description: "[arXiv 2607.26348][LLM 评测] 本文旨在建立一套面向决策支持的跨领域验证框架，用真实人类调查数据和非LLM基线判断人口属性提示下的LLM合成用户何时可替代真人、何时会产生系统性失真。"
arxiv_id: "2607.26348"
announcement_date: "2026-07-30"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:24.997929+00:00"
source_sha256: "223f53c089f7d19b3f8e8a80de7fef9d4311908cb03a77341078be7be91e44d3"
tags:
  - "LLM 评测"
  - "LLM 其他"
  - "大语言模型"
  - "合成用户"
  - "问卷模拟"
  - "社会模拟"
  - "评估基准"
  - "人口统计条件预测"
  - "刻板化"
  - "负责任人工智能"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2607.26348</p>

# When Synthetic Users Fail: A Cross-Domain Benchmark of LLM-Simulated Human Survey Responses

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Zihan Chen, Di Zhu, Lei Nico Zheng</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26348v1) · [PDF 下载](https://arxiv.org/pdf/2607.26348v1) · **关键词** 大语言模型, 合成用户, 问卷模拟, 社会模拟, 评估基准, 人口统计条件预测, 刻板化, 负责任人工智能  


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

本文旨在建立一套面向决策支持的跨领域验证框架，用真实人类调查数据和非LLM基线判断人口属性提示下的LLM合成用户何时可替代真人、何时会产生系统性失真。

**不用术语来说**：企业和公共机构希望用LLM扮演不同人群来快速回答调查问卷，从而节省真人调研的时间与成本；但LLM能生成看似合理的答案，并不意味着这些答案真的像对应人群，更不意味着据此进行产品定位、市场细分或政策判断是安全的。因此，在使用合成回答之前，需要检验它是否至少优于简单的人口统计规律，并确认其误差会不会改变实际决策。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出统一的跨领域评估设计：固定模型、提示、解码、抽样与指标，在美国一般社会态度调查（GSS）和跨文化价值观调查（WVS）上，将四个LLM与基于留出真人数据训练的非LLM人口统计基线进行同条件比较。
- 将验证从单一总体相似度扩展到个人回答、总体分布、人口群体结构、模型与输出格式稳定性以及跨领域迁移，并把这些检查组织为可在合成用户进入决策流程前运行的适用性验证框架。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型作为“合成用户”模拟人类问卷回答的可靠性。此类系统根据受访者的人口统计信息生成人工回答，可用于问卷预测试、意见分布估计、产品功能排序、市场分群和政策分析；其价值在于以较低时间与经济成本近似真实的人类调查。然而，模型能够生成形式正确的问卷答案，并不意味着这些答案可以替代真实证据。本文因此把合成用户视为决策支持系统中的“证据生产组件”，要求其在具体用途下与真实人类数据及非大模型基线进行验证。研究范围明确限定为人口统计提示下的问卷模拟，不涵盖微调模型或包含更丰富信息的人物设定。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**合成用户（synthetic user）**

由大语言模型扮演的虚拟受访者，模型在获得人口统计特征或人物设定后生成问卷答案。本文关心的不是回答是否像问卷，而是这些回答能否可靠替代真实人类回答并支持后续决策。

</div>
<div class="conceptitem" markdown="1">

**人口统计条件预测**

利用年龄、性别、国家等人口统计变量，预测某个群体或个体更可能选择的答案。本文将大模型与直接从留出的人类数据中估计“给定人口统计特征时答案如何分布”的朴素方法比较。

</div>
<div class="conceptitem" markdown="1">

**个体保真度与聚合保真度**

个体保真度衡量模型能否预测具体受访者的答案，聚合保真度衡量大量模拟回答形成的总体分布是否接近真实人群。总体比例相近并不保证模型正确刻画了个体差异或人口群体之间的意见结构。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究以真实受访者的人口统计信息和调查题目为输入，让四个来自两个模型家族、能力范围从约 8B 参数级到前沿级的大语言模型，在单答案提示与概率分布提示两种格式下生成回答。真实参照来自两个独立领域：GSS 2016—2024 年美国综合社会调查中的 10 道态度题，以及 WVS 第七波覆盖 63 个国家的 16 道有序价值观题。模型输出分别在个体回答、总体答案分布和人口群体意见结构三个层级与真实数据比较，并与在留出人类数据上拟合的人口统计查表、逻辑回归和随机森林等非大模型预测器比较。核心假设不是人口统计信息能够唯一决定答案；相反，真实个体回答包含不可由这些特征消除的不确定性，因此任何准确率都必须相对于同信息条件下的基线解释。统一的模型、提示、解码、采样和指标设置还用于检验结论能否跨模型家族、能力规模、输出格式和调查领域复现。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$x$**

某位真实受访者的人口统计特征组合，例如年龄、性别或国家；这是对文中“demographics”的简化记号。

</div>
<div class="notationitem" markdown="1">

**$y$**

受访者对某一道调查题的真实答案；对于 WVS 中的题目，它可以是具有顺序关系的类别。

</div>
<div class="notationitem" markdown="1">

**$p_{\mathrm{human}}(y\mid x)$**

根据留出的人类调查数据估计的条件答案分布，即具有特征 x 的真实人群回答 y 的概率，也是朴素人口统计基线的基础。

</div>
<div class="notationitem" markdown="1">

**$\hat{y}_{\mathrm{LLM}}$**

大语言模型在给定人口统计特征和题目后生成的单一预测答案；若采用分布提示，则对应输出为各答案选项的预测概率。

</div>

</div>

**直接相关的工作**

- **Argyle et al.（原文参考文献 [2]）**: 该工作表明，加入人口统计条件的提示可以在美国政治调查数据上复现某些聚合模式，并推动了“silicon sample（硅基样本）”思路。本文不把聚合一致性直接视为替代有效，而是进一步要求模型在个体层面胜过人口统计基线，并检验人口群体结构与跨领域可迁移性。
- **关于合成受访者替代不安全的研究（原文参考文献 [5]、[14]）**: 这些研究对用大语言模型替代真实受访者提出警告，但所给节选未提供其题名或具体实验设置。本文试图解决既有证据相互冲突、常局限于单一调查或单一领域且依赖单个聚合相似度的问题，采用统一协议开展基线锚定的跨领域验证。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

真人调查通常耗时且昂贵，促使产品、市场、政策和组织分析团队使用LLM合成用户来预估人群反应。然而，合成回答已成为决策证据的一部分：一旦模型以系统方式误判某类人群，其偏差就会传递并放大到功能优先级、营销对象或资源配置中。因此，团队需要一种能在部署前判断合成用户是否适合特定问题、总体和分析层级的验证办法。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于人口属性提示的LLM调查模拟**：把年龄、性别、国家等人口属性写入提示，让LLM扮演具有这些属性的受访者，并输出单个选项或各选项的概率分布；随后通常将合成回答与真人调查结果比较。
- **单领域的总体分布对齐评估**：在某一政治、文化或国家调查上汇总LLM回答，再用一个总体相似度或分布指标衡量其与真人样本是否接近，据此判断模拟是否有效。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 总体分布看起来接近，并不能证明模型能预测个体回答或正确表示群体差异；不同个体误差可能在汇总时相互抵消，使一个令人放心的总体分数掩盖底层模拟失真，进而误导细分人群决策。
- 既有研究多局限于单一调查、领域、模型或提示，且常未设置在留出真人数据上拟合的简单人口条件基线；因此，已报告的准确率既无法说明LLM是否比“同类人口通常如何回答”的查表规则更有信息，也难以判断结论能否跨领域复现。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

目前缺少一种统一、可比较且面向实际用途的验证方案：它既要以真人数据上的非LLM人口统计预测器作为最低参照，又要分别检查个体保真度、总体分布和人口群体结构，并验证结果是否跨模型家族、能力规模、输出格式和调查领域保持稳定。

</div>
<div markdown="1"><span>核心问题</span>

在人口属性提示和本文测试的调查模拟协议下，LLM合成用户是否比朴素的人口条件预测器更准确地模拟真人，同时忠实再现总体答案分布及人口属性与态度之间的真实关系；这些判断能否跨模型与GSS、WVS两个独立领域成立？

</div>
<div markdown="1"><span>作者直觉</span>

作者把LLM视为一个“制造决策证据的组件”，而不是只检查它能否生成像问卷答案的文本。最有辨识力的切入点是先与简单的人口统计基线比较：如果复杂LLM连根据真人数据估计的常见答案都不能稳定胜过，就没有证据表明它提供了额外的个体信息；再分层检查总体分布与群体结构，则可发现汇总结果可能掩盖的刻板化偏差。最后在两个独立领域复用同一协议，可区分普遍失败与某个数据集、模型或提示造成的偶发现象。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文提出的不是一个需要训练的新模型，而是一套面向“LLM 合成用户”的验证框架。其端到端流程是：从两个独立的人类调查域构造带人口属性与真实回答的评测样本；使用统一的人口统计提示协议，让四个跨模型家族、覆盖 8B 到前沿能力范围的 LLM 模拟受访者；在留出的人类数据上建立问题边际、人口群体查表和学习式人口统计模型等非 LLM 基线；随后分别检验个体回答保真度、人口属性对回答的过度决定、无效输出以及对群体定位决策的影响，并用配对 bootstrap 置信区间评估不确定性。直观地说，这套方法不只问“模型猜中了多少题”，而是先问“只看人口资料的简单方法能做到多好”，再检查模型是否把身份标签刻板地放大，以及这种偏差是否会真正误导产品、政策或市场决策。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建跨域人类参照样本

按统一评测结构整理人口统计信息、调查问题及真实个体回答，并划分用于拟合非 LLM 基线的留出人类数据与评测对象。当前节选未给出具体题目筛选规则、样本量和划分比例，这些信息应以论文第 3 节及附录为准。

<div class="method-step__io" markdown="1">

**输入**：美国综合社会调查（General Social Survey）与世界价值观调查（World Values Survey）中的真实人口属性和问卷回答；后者覆盖 63 个国家。  
**输出**：两个彼此独立但可在同一协议下分析的人类回答基准域。

</div>

**直观理解**：真实调查回答相当于答案参照；使用美国社会态度和跨文化价值观两个域，是为了检验失败现象是否只来自某一个数据集。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成 LLM 合成受访者回答

在统一的人口统计提示和调查模拟协议下，调用四个模型生成个体回答或回答分布；这些模型来自两个模型家族，能力范围从 8B 参数模型到前沿模型。输出经过指定解析规则处理，并记录不能形成有效调查答案的输出。

<div class="method-step__io" markdown="1">

**输入**：每位真实受访者的人口统计描述、相应调查问题，以及论文规定的调查模拟提示。  
**输出**：与真实受访者及问题相对应的模型预测答案、预测分布和无效输出记录。

</div>

**直观理解**：模型被要求根据某人的人口资料进行角色扮演并代答问卷；统一提示可以减少因提问方式不同造成的不公平比较。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立非 LLM 参照并评估个体保真度

拟合并比较问题边际基线、人口群体查表基线和学习式人口统计模型；使用个体准确率，并以适用于有序选项的距离感知指标和适用于概率分布的 log-loss、Brier score 作稳健性检验。各项比较采用配对 bootstrap 置信区间。

<div class="method-step__io" markdown="1">

**输入**：留出的人类调查数据、真实答案，以及各 LLM 的预测答案或预测分布。  
**输出**：LLM 相对简单人口信息基线的个体级增益或损失，以及相应不确定性。

</div>

**直观理解**：如果模型连“按总体最常见答案猜”或“按相似人口群体统计规律猜”都不能超过，就不能把它的命中率解释为理解了具体个人。距离指标允许相邻等级获得部分分数，而概率评分还会检查模型是否真的把较高概率分给真实答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 测量人口过度决定与稳健性

分别估计某一群体属性能够解释真实回答变化和模型回答变化的程度，再用有界的刻板化指数比较两者；同时使用不依赖答案数值编码的 Cramér’s V 检查结论是否由选项编码方式造成。对问题—群体组合报告置信区间并判断过度关联是否显著区别于随机波动。

<div class="method-step__io" markdown="1">

**输入**：真实人类回答、模型回答，以及政治倾向等人口或群体属性。  
**输出**：各模型、调查域和问题—群体组合的人口过度决定程度及其编码稳健性。

</div>

**直观理解**：这里关注的不是模型是否总给少数群体同一个答案，而是模型是否把“属于哪个群体”看得比真人更有决定性。Cramér’s V 把答案当作类别而非人为赋值的数字，可防止结论只是编码选择的产物。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文方法是评测与验证框架，并未在所给材料中提出或训练新的 LLM，也没有通过某个损失函数优化合成用户模型；非 LLM 的学习式人口统计基线会在留出人类数据上拟合，但当前节选未报告其具体模型形式、训练目标或超参数。log-loss 与 Brier score 在此用于评价模型给出的回答分布，不应误解为本文训练 LLM 的目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 基线锚定的个体保真度评估**

将 LLM 与问题边际、人口群体查表及学习式人口统计模型比较，而非只孤立报告准确率；对有序答案补充距离感知指标，对概率输出补充 log-loss 与 Brier proper scoring，并使用配对 bootstrap 置信区间。

> 直观理解：准确率本身没有合格线：某题若大多数人都选同一项，简单猜多数项也会很高。基线锚定用于判断 LLM 是否真正提供了超出人口统计规律的新信息。

**2. 刻板化指数与 Cramér’s V 伴随检验**

刻板化指数以一个有界数值比较群体属性对模型回答和真人回答的预测或解释强度；Cramér’s V 作为编码不变的类别关联度量，不要求把问卷选项映射为具有数值间距的尺度。节选未提供刻板化指数的精确定义式、边界方向及估计细节。

> 直观理解：核心问题是模型是否让身份与态度绑定得过紧。两种度量从不同假设出发得到一致结论时，才更能排除结果由选项数字编码造成的可能。

**3. 决策影响分析**

把模型与真人的群体级估计带入群体定位任务，分别考察群体间效应差距被放大的倍数、最优目标群体是否选错，以及模型是否制造真人样本不支持的群体分裂。

> 直观理解：这一模块把统计失真转换成可执行决策的后果，使使用者能判断合成用户证据是否足以支持产品、政策或市场细分。

**训练与推理**

训练侧仅涉及在留出的人类调查数据上建立非 LLM 基线，其中问题边际基线估计每道题的总体答案分布，人口群体查表基线按人口属性组合汇总经验回答，学习式人口统计模型则从人口特征预测答案；其精确拟合算法在当前节选中未明确报告。推理侧对四个 LLM 使用同一人口统计角色提示与调查模拟协议，生成答案或概率分布，再按预先规定的解析规则转换为可评分结果并统计无效输出。随后把每个模型输出与对应真人答案和所有基线配对，依次计算个体保真度、人口属性关联强度及群体定位决策后果；所有模型、两个调查域和相关问题—群体组合均遵循同一分析逻辑，以检验失败是否能跨域、跨模型家族和跨模型规模复现。

**复现信息**

公平解释结果所必需的设计包括：两个独立数据域（GSS 美国社会态度与覆盖 63 国的 WVS 跨文化价值观）、四个来自两个家族且覆盖 8B 至前沿能力范围的模型、统一的人口统计提示和调查模拟协议、三类非 LLM 基线、对有序选项采用距离感知补充指标、对分布输出采用 log-loss 与 Brier score、以 Cramér’s V 检验答案编码不变性，以及全程使用配对 bootstrap 置信区间。框架还要求分别报告个体与聚合保真度、群体决定性及其决策影响和无效输出率，不能把更大模型默认视为更安全。论文称数据构建、推理和分析脚本以及全部提示、解析规则和基线说明位于工具包或附录并可按请求获取；当前节选未给出样本量、具体模型名称、提示全文、解码参数、bootstrap 次数、显著性阈值及刻板化指数公式，因此这些项目均需依据论文第 3 节和附录进行源文核验。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- General Social Survey（GSS）：美国一般社会态度调查，用于检验单一国家内人口特征与社会态度之间的个体、总体及群体关系。原文节选未给出题目数、受访者总数或最终评估样本量。数据按受访者ID哈希奇偶划分：50%的“fit”折用于构建基线，“eval”折中的样本用于评估，保证同一受访者不会同时出现在两折。
- World Values Survey（WVS）：覆盖63个国家的跨文化价值观调查；论文复用WorldValuesBench的题目集与量表，用来检验结论能否从美国社会态度迁移到跨国家价值观场景。其基线同样只在50%的“fit”折拟合并在独立“eval”折评估；原文节选未明确报告受访者总数、题目数和各国样本分布。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**个体回答准确率及相对基线差值Δbase**

准确率衡量模型预测与真实个体答案完全一致的比例；Δbase等于LLM准确率减去人口统计查表基线准确率，并通过配对bootstrap给出95%置信区间。它回答LLM是否增加了超出人口查表的个体预测信息，但严格精确匹配本身不反映序数答案之间距离。 （准确率越高越好，Δbase越大越好；Δbase为正才表示超过查表基线，置信区间跨越0则不能排除统计上的平局。）

</div>
<div class="metricitem" markdown="1">

**平均Jensen–Shannon散度（JS）**

比较LLM生成的答案分布与真实人群答案分布之间的差异，用于总体层面的分布拟合；该指标对称且有界，但较好的总体分布不能证明模型能预测具体个人，也可能掩盖群体结构失真。 （越低越好，因为0表示两个答案分布完全一致。）

</div>
<div class="metricitem" markdown="1">

**人口统计过度决定指标Δη²及显著问题—群体对数量**

Δη²比较人口特征在模型回答中解释的变异与其在真实人类回答中解释的变异；论文汇报其中位数及95%置信区间排除0的问题—群体对数量，并用不依赖类别编码方式的Cramér’s V复核。它测量的不是某群体是否被赋予负面标签，而是模型是否让人口身份显得过度能够预测态度。 （越接近0越忠实；正值表示人口特征在模型中比在人类数据中更具决定性，因而存在过度决定。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### GSS个体回答预测：四个模型、Style A与Style C，对比人口统计查表及更强监督基线

<div class="result-value" markdown="1">

所有LLM的准确率均未超过人口统计查表基线0.589。最接近的是Sonnet 4.6 Style C，准确率0.589、Δbase=-0.001，95%置信区间[-0.028, 0.022]，只能视为统计平局；Llama 8B Style A为0.496，比基线低0.093，置信区间[-0.120, -0.067]。此外，逻辑回归达到0.622，高于最佳LLM；随机森林为0.583。

</div>

在美国社会态度场景中，LLM并未显示出超越简单人口统计预测器的个体洞察力；更大的模型也没有稳定优势。Sonnet与查表基线打平不等于证明二者完全等价，而是现有样本无法确认其差异。该结果也不表示LLM无法生成看似合理或总体分布接近的答案，只说明其对具体受访者答案的预测没有增加可靠信息。

<div class="result-source" markdown="1">

来源：第4.1节；具体数值见表1、表2与图2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">On GSS, the individual accuracy of every model is at or below the demographic lookup baseline (0.589).</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### WVS跨文化价值观个体预测：四个模型、两种输出风格，对比人口统计查表基线

<div class="result-value" markdown="1">

WVS上的差距显著扩大且全部为负。Style A中，Haiku 4.5、Sonnet 4.6、Llama 8B和Llama 70B的准确率分别为0.170、0.236、0.179和0.249，而共同查表基线为0.388，对应Δbase分别为-0.218、-0.152、-0.209和-0.139。Style C同样未超过基线，Δbase介于-0.111与-0.218之间；其中Llama 8B Style C有85%无效输出，结果实际上不可用。

</div>

跨国家价值观不是仅凭人口标签和语言常识就能可靠还原的个体属性；即使最佳结果也明显落后于从真实人类数据建立的简单基线。跨两个模型家族均出现负差值，使失败不太可能只是某一个模型的偶发现象。不过，Style C部分结果受无效输出率影响，不能把所有模型间数值排序解释为纯粹能力差异。

<div class="result-source" markdown="1">

来源：第4.1节原句在所供节选中被截断；完整数值见表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">On WVS the gap is far larger and uniformly negative: under the single-answer prompt every model is</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨GSS与WVS的人口统计过度决定及其决策影响

<div class="result-value" markdown="1">

表1中所有可报告模型—风格—领域组合的中位Δη²均为正。GSS中范围为+0.026至+0.104，WVS中范围为+0.030至+0.376；例如WVS Sonnet 4.6 Style A为+0.107，32个问题—群体对中31个的95%置信区间排除0。作者进一步报告，在群体定位任务中，模型将群体差距夸大到真实差距的2至4倍，并会在一半美国案例及大多数跨文化案例中选择错误群体。

</div>

LLM不是简单地产生随机误差，而是系统性地把人口身份当成比现实更强的态度决定因素，因此可能制造并不存在的市场或政策分群。该结果描述的是人口信息与回答之间关联强度的失真，不直接证明模型对任何特定群体抱有负面态度，也不能据此推断失真的唯一原因是训练数据中的刻板印象。

<div class="result-source" markdown="1">

来源：摘要；过度决定数值见表1，问题级结果见图3与图4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">A decision-impact analysis shows why this matters in practice: on a segment-targeting task the models inflate between-segment gaps two to fourfold, would direct a team to the wrong segment in half of U.S. and most cross-cultural cases, and manufacture segment splits that do not exist in real people.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 分布输出协议存在明显格式可靠性问题：若某些模型的大量回答无效，Style C的准确率、JS散度和过度决定指标可能基于选择后的少量有效样本。特别是WVS上的Llama 8B有85%无效输出，因此该单元不适合用于一般能力比较。
- 结论严格适用于论文测试的人口统计提示、两类调查数据、四个模型和所选指标。虽然跨领域复现增强了外部效度，但原文节选没有检验访谈式交互、个体历史信息、检索增强、微调或其他代理架构，因而不能推出所有合成用户方法都必然失败。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 问题边际众数基线（question-marginal）：对每道题始终预测拟合折中最常见的答案。它衡量完全不使用人口信息时能够达到的最低限度预测能力。
- 人口统计查表基线（demographic lookup）：在拟合折中估计人口单元内的条件答案分布并预测其众数。单元少于20人时逐级回退：GSS从{学历、种族、性别、政治观点}退到{学历、种族}，再退到题目边际；WVS从{国家、教育、年龄组}退到{国家}，再退到题目边际。该基线直接检验LLM是否比简单记忆“类似人口群体通常怎样回答”提供更多个体信息。
- 多项逻辑回归：按题目拟合，以提示中人口变量的独热编码为输入，最多迭代2000次，并可输出完整预测分布。它是可学习但结构较简单的监督基线，用于判断查表基线是否过弱，也支持对数损失与Brier分数比较。
- 随机森林：使用与逻辑回归相同的人口特征、每个模型300棵树。它能学习非线性及变量交互，是对“LLM可能因复杂人口组合而占优”这一解释的更强检验。

**实验想回答的问题**

- RQ1：在仅给定人口统计信息并采用单答案或答案分布提示时，LLM能否准确预测真实个体的问卷回答，并且是否真正优于利用留出人类数据训练的非LLM基线？这一问题同时用精确匹配、距离感知指标和适当评分规则检验，以排除序数量表上的严格判分造成假性失败。
- RQ2：LLM生成的总体分布和人口群体差异是否忠实于真实人群；尤其是，模型是否把人口身份错误地塑造成态度的强决定因素，以及这种偏差是否会进一步误导实际的群体定位决策？

**实验实现**

论文固定同一套人口统计提示与问卷模拟协议，跨GSS和WVS运行四个模型：Haiku 4.5、Sonnet 4.6、Llama 8B与Llama 70B，覆盖两个模型家族及8B到前沿模型的能力范围。Style A要求输出单个答案，Style C要求输出答案分布。所有非LLM基线仅用fit折人类数据训练，并在独立eval折上比较；个体准确率差值采用配对bootstrap置信区间，总体分布另做人口重加权检查，群体偏差则以方差解释量和Cramér’s V双重验证。原文节选未明确报告LLM采样温度、重复生成次数、完整提示模板、API版本或随机种子。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 将人口统计查表替换为学习型基线，检验LLM失败是否源于参照物过强或过弱 | GSS上多项逻辑回归准确率为0.622，随机森林为0.583；最佳LLM仅约0.589。因此，即便不只与查表方法比较，LLM仍落后于最强的非LLM人口特征预测器。 | 这一对照隔离了“基线选择”因素：如果LLM只是不巧输给一个特别有效的查表规则，它仍可能超过其他常规学习器；但逻辑回归取得更高准确率，说明人口提示下的LLM没有表现出独特的个体预测增益。随机森林较低则同时表明，更复杂的非线性模型也不必然更好。 | 第4.1节，表2<br><span class="experiment-evidence">The lookup is not a weak straw man: a learned logistic baseline reaches 0.622 and a random forest 0.583 (Table 2), so the best LLM also trails the strongest non-LLM predictor.</span> |
| 将单答案Style A改为分布输出Style C，检验输出形式是否能修复准确率与群体失真 | 输出分布通常显著降低总体JS散度，例如GSS Haiku从0.090降至0.011，WVS Sonnet从0.274降至0.037；但个体层面的Δbase仍全部不为正，同时Δη²仍为正。部分Style C设置还出现较高无效率，其中WVS Llama 8B有85%无效输出，n=440。 | 让模型表达不确定性有助于匹配总体答案比例，却没有使其超过个体基线，也没有消除人口统计过度决定。这说明总体分布改善不能被解释为合成用户更像真实个体。无效输出率还提示，分布提示带来的表面指标改善必须与格式遵循能力一起审查。 | 表1脚注及第4.5节<br><span class="experiment-evidence">Llama-8B Style-C on WVS is effectively unusable (85% invalid, n=440).</span> |

**定性案例**

- 群体定位任务将统计失真转化为决策后果：模型把群体间差距放大2至4倍，在约一半美国案例及多数跨文化案例中会推荐错误群体，并产生真实人群中不存在的分群。它说明即使合成答案在语言上可信或总体比例尚可，仍可能向产品、政策或市场团队提供方向错误的证据；但所供节选未给出具体题目、群体名称及逐案例计算过程。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces a cross-domain benchmark and evaluation framework for measuring the validity of LLM-simulated survey respondents.; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`223f53c089f7d19b3f8e8a80de7fef9d4311908cb03a77341078be7be91e44d3`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
