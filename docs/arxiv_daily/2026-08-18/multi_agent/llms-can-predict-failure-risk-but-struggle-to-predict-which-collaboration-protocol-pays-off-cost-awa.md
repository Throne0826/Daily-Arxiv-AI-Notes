---
title: "[论文解读] LLMs Can Predict Failure Risk, But Struggle to Predict Which Collaboration Protocol Pays Off: Cost-Aware Protocol Routing Across Reasoning Tasks"
description: "[arXiv 2608.14927][Multi-Agent] 本文通过固定求解器、逐题运行四种推理协议，揭示“预测直接求解会不会失败”与“预测哪种协作协议值得额外成本”是难度不同的决策，并表明现有置信度与路由方法主要只能支持前者。"
arxiv_id: "2608.14927"
announcement_date: "2026-08-18"
primary_category: "multi_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:18:55.348112+00:00"
source_sha256: "1f05ef92eab3f7eb3876dabf88715d0eb854106eacef82605f73c377e93bcfb6"
tags:
  - "Multi-Agent"
  - "LLM Reasoning"
  - "大语言模型"
  - "多智能体推理"
  - "协作协议"
  - "成本感知路由"
  - "失败风险预测"
  - "协作价值预测"
  - "自信度校准"
  - "计算成本"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">Multi-Agent · arXiv 2608.14927</p>

# LLMs Can Predict Failure Risk, But Struggle to Predict Which Collaboration Protocol Pays Off: Cost-Aware Protocol Routing Across Reasoning Tasks

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Chih-Hsuan Yang, Jingyan Jiang, Cheng-Hau Yang, Vikram Vasudevan, Huihuo Zheng, Venkatram Vishwanath, Rajeev Thakur</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Argonne National Laboratory, Lemont, IL, USA；Affiliation: Oregon State University, Corvallis, OR, USA</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.14927) · [PDF 下载](https://arxiv.org/pdf/2608.14927) · **关键词** 大语言模型, 多智能体推理, 协作协议, 成本感知路由, 失败风险预测, 协作价值预测, 自信度校准, 计算成本<br>


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

本文通过固定求解器、逐题运行四种推理协议，揭示“预测直接求解会不会失败”与“预测哪种协作协议值得额外成本”是难度不同的决策，并表明现有置信度与路由方法主要只能支持前者。

**不用术语来说**：面对同一道题，大语言模型既可以直接作答，也可以花费更多计算进行自我修正、角色分工或多智能体讨论；后者有时能纠正错误，却也可能消耗大量令牌而没有收益。实际部署需要针对每道题判断是否值得增加计算，并在多种昂贵方案中选出真正能带来正确答案且成本合适的一种，而不能简单地对所有问题都采用最强、最贵的流程。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者构建逐题匹配的四协议比较：在每个设置内保持求解器不变，同时观察直接求解、迭代式自我修正、规划者—执行者—审查者协作和多智能体讨论的结果与令牌成本，从而把协议本身的价值与基础模型能力差异分离开。
- 作者明确区分失败风险预测与协议价值预测，并用方向性错误分析指出：保守策略往往升级不足，追求较高解题率的冻结大模型路由器则容易升级过度；同模型置信度可用于初步的“保持或升级”判断，但尚不足以完成协议特定、成本敏感的路由。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究多智能体大语言模型推理中的“协议路由”：面对同一道推理题，系统可以直接作答，也可以投入更多计算进行自我修正、角色分工或多智能体讨论。更复杂的协作通常消耗更多 token，且不保证对每道题都有帮助，因此部署问题不是单纯追求最高解题率，而是根据单题情况决定是否升级，以及升级到哪种协作协议，进而权衡正确率与推理成本。与选择不同能力或价格模型的传统模型路由不同，本文在每个比较设置内固定求解器家族，只改变协作方式，以尽量把性能变化归因于协议本身。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**协作协议**

规定一个或多个大语言模型实例如何组织推理的流程。本文比较直接求解、迭代式自我修正、规划者—执行者—审阅者分工，以及多智能体共同讨论四种协议。

</div>
<div class="concept-item" markdown="1">

**成本感知路由**

路由器根据题目或模型产生的信号，为每道题选择推理协议，同时考虑解题收益和额外 token 成本。核心不是无条件调用最强协议，而是判断增加的计算是否值得。

</div>
<div class="concept-item" markdown="1">

**失败风险与协作价值**

失败风险预测判断直接求解是否会答错；协作价值预测则进一步判断额外协作能否纠错，以及哪一种协议的收益足以抵偿其成本。前者只需识别“可能失败”，后者还需预测不同干预方式的条件性效果。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一道推理问题，以及路由时可获得的题目信息或求解器信号；输出是四种协议之一：Baseline 直接求解、Single 迭代自我修正、PER 规划者—执行者—审阅者协作、Broadcast 多智能体讨论。每道题均在四种协议下实际运行，从而形成配对的正确性与 token 成本结果；这种全协议观测允许离线比较固定策略、训练所得路由器、冻结大模型路由器与回顾性固定顺序 oracle。主要设置包含 4,181 道竞赛级数学题，配对稳健性检查覆盖数学、生物学和更广泛科学领域的四个基准及两个求解器家族；在每个具体比较中固定求解器，只改变协议。需要注意，oracle 使用事后真实结果，只表示当前协议集合和固定尝试顺序下可达到的回顾性覆盖上界，并非可直接部署的方法；此外，较完整的置信度与留出路由评估仅覆盖六个模型—条件设置，因此跨任务结果主要说明协议价值具有任务依赖性，不能据此宣称普遍有效。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{P}$**

候选协作协议集合，可理解为由 Baseline、Single、PER 和 Broadcast 构成的四种选择。

</div>
<div class="notation-item" markdown="1">

**$x$**

待求解的单个推理问题。

</div>
<div class="notation-item" markdown="1">

**$y_p(x)$**

问题 $x$ 在协议 $p\in\mathcal{P}$ 下的实际求解结果或正确性标签；该符号是为概括问题设置而采用的记号，原文节选未给出正式符号定义。

</div>
<div class="notation-item" markdown="1">

**$c_p(x)$**

问题 $x$ 使用协议 $p\in\mathcal{P}$ 时的实际计算成本，文中主要以 token 消耗体现；该符号是为概括问题设置而采用的记号，原文节选未给出正式符号定义。

</div>

</div>

**直接相关的工作**

- **模型路由与级联系统**: 相关方法在能力和价格不同的模型之间进行选择；本文固定同一比较中的求解器家族，仅切换协作协议，以避免把基础模型能力差异误当成协议收益。原文节选仅给出参考文献编号 4、13、16、17，未提供可核验的具体文献题名。
- **置信度校准研究**: 校准研究考察模型置信度能否反映答案正确性，可为“保持直接求解还是升级”提供信号；本文进一步要求预测特定协议是否值得其边际成本，因此任务比正确性校准更细。原文节选仅给出参考文献编号 9、11、12，未提供可核验的具体文献题名。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

不同推理协议的计算开销可能相差很大，而更昂贵的协作并非对每道题都有效。若始终使用直接求解，系统会错过可被协作纠正的问题；若始终使用最强协作，又会在本可直接解决的问题上浪费令牌。因此，部署系统必须把解题收益与边际成本同时纳入逐题决策。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **模型路由与自适应计算**：模型路由在能力和价格不同的模型或级联系统之间选择；自适应计算则调整推理深度、采样路径数量等计算预算。两者都试图把更多资源分配给较难的问题，但通常改变的是模型能力或计算量，而不是在固定求解器条件下比较不同协作结构。
- **置信度门控与工具／多智能体路由**：置信度门控依据模型对自身答案正确性的估计，决定保留直接答案还是触发更昂贵流程；工具或多智能体路由则在工具、角色和协作结构之间进行选择。这些方法提供了升级信号或候选工作流，但置信度是否能精确指出某一种协议的边际收益仍不清楚。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 把“直接答案可能错误”当作“某个协作协议值得调用”会混淆两个目标：识别失败只说明可能需要帮助，并不能说明自我修正、角色协作或多智能体讨论中的哪一种能够纠错。其后果是路由器可能选中昂贵但无效的协议。
- 既有比较常同时更换模型、推理预算或协作方式，难以判断性能提升究竟来自更强的基础模型，还是来自协议本身；只看总体路由准确率还会掩盖升级不足与升级过度这两类成本后果相反的错误。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

目前缺少一种受控且逐题匹配的评估框架，能够在固定求解器的前提下获得各协作协议的真实正确性与成本结果，并据此检验路由信号究竟只能预测直接求解的失败风险，还是还能可靠预测某个特定协议相对于直接求解的边际价值。尤其未解决的是如何在正确率收益和额外令牌成本之间进行可部署的实例级协议选择。

</div>
<div markdown="1"><span>核心问题</span>

在保持基础求解器不变时，能否根据问题及模型产生的信号，先准确判断直接求解是否需要升级，再从自我修正、规划者—执行者—审查者协作和多智能体讨论中选出足以补偿额外成本的协议；现有启发式、训练式及冻结大模型路由器距离逐题最优选择还有多大差距？

</div>
<div markdown="1"><span>作者直觉</span>

模型在生成答案前后的置信度可能反映它是否处于容易出错的状态，因此适合作为第一道门：高置信度时保留便宜的直接求解，低置信度时允许升级。然而，不同协作协议纠正的是不同类型的错误，而且其成本也不同；知道“当前答案危险”类似于知道需要维修，却不能据此确定应使用哪一种维修方案。逐题观察全部协议的结果，才能把一般失败信号与协议特定收益信号分开，并暴露路由器是在不该升级时升级，还是在需要升级时仍保持保守。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文把“协议路由”定义为一个带成本的单次决策问题：对于每道题，路由器在看不到标准答案、正确性标签和各协议实际结果的条件下，从 Baseline、Single、PER、Broadcast 与 None 中选择一个动作。四种求解协议按计算量由低到高排列：Baseline 直接作答；Single 让同一求解器迭代自我修正；PER 将规划、执行和审查分配给不同角色；Broadcast 让多个智能体并行讨论。None 表示预计所有协议都无法成功，因此放弃求解。论文在同一问题上预先运行全部四种协议，记录每个协议是否解对及其 token 成本，由此构造反事实完整的离线评测表；路由器本身仍只能使用题目文本及允许的元数据，不能读取这些结果。

方法的重点不是提出一个复杂的新路由网络，而是建立可诊断的比较框架：固定同一设置内的基础求解器，只改变协作协议，再比较固定策略、轻量监督式路由器、冻结 LLM 路由器和基于置信度的升级门控。该框架进一步区分两个预测任务：失败风险预测只判断 Baseline 是否可能出错；协作价值预测则判断额外计算是否能纠错，以及具体哪一种协议的收益足以抵偿其成本。直观地说，前者类似判断“当前答案靠不靠谱”，后者还要回答“若不靠谱，应购买哪一种更昂贵的复核服务”；论文认为第二个问题明显更难。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造逐题匹配的协议结果

对每道题分别运行四种协议，并记录二元正确性结果、token 消耗和协议轨迹；同一比较设置保持求解器家族不变，使结果差异主要对应协作结构与额外计算。主基准采用 4,181 道 Omni-MATH 2 竞赛数学题，稳健性检查还覆盖数学、生物和更广泛科学任务及两个求解器家族。

<div class="method-step__io" markdown="1">

**输入**：一道基准题目、固定的求解器栈，以及 Baseline、Single、PER、Broadcast 四种协议。<br>
**输出**：逐题匹配的四协议结果表，其中每道题同时具有各协议的实际成败和成本。

</div>

**直观理解**：这相当于让同一道题分别接受四种不同强度的解题流程，然后把结果放在同一行比较。因为四条路线都真实运行过，离线评测时可以知道路由器若选择另一协议，本来会发生什么。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成成本感知的路由目标

按照从便宜到昂贵的固定顺序，为每题找出能够正确求解的最便宜协议；若四种协议均失败，则目标为 None。该标签形成五分类路由任务，并允许计算路由选择造成的漏解、过度升级和额外成本。

<div class="method-step__io" markdown="1">

**输入**：每道题的四协议正确性、协议成本，以及固定的成本顺序 Baseline、Single、PER、Broadcast。<br>
**输出**：取值为 Baseline、Single、PER、Broadcast 或 None 的逐题路由标签，以及对应的离线成本与求解结果。

</div>

**直观理解**：目标不是无条件选择成功率最高的流程，而是选择“足够解决这道题的最便宜流程”。如果便宜方法已经能解对，选择昂贵协作就是浪费；如果选得太保守导致本可解题未解出，则是升级不足。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 训练或调用候选路由器

轻量学习路由器使用五分类逻辑回归：文本表示为训练集上拟合的 TF-IDF 词级一元组和二元组，元数据经过独热、多标签和标准化编码；冻结 LLM 路由器则接收统一提示，直接输出五个允许标签之一。论文还设置固定协议策略、仅元数据、仅文本、句向量及文本与元数据组合等对照，以区分标签学习、语义信息和成本偏好的作用。

<div class="method-step__io" markdown="1">

**输入**：题目文本，以及允许公开给路由器的来源、领域路径、难度分数和难度等级等元数据；监督式模型在训练阶段还使用路由标签。<br>
**输出**：每道题的单一协议预测；不可解析的冻结 LLM 输出按规定回退为 Baseline。

</div>

**直观理解**：轻量模型像一个根据题型、难度和关键词作判断的分类器；冻结 LLM 则阅读题目后直接推荐协议，但不允许真正解题。两者都必须在知道实际结果之前下注，因此不会偷看哪种协议最后成功。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 用置信度执行分层升级

预答案门控在尚未生成 Baseline 答案时估计直接求解成功概率，并据阈值决定停留或升级；后答案探针读取题目、元数据和 Baseline 最终答案，输出其正确概率，但不得重新解题。论文还检查二元门控和双阈值级联，以检验置信度更适合回答“是否升级”，还是足以决定具体升级到哪种协议。

<div class="method-step__io" markdown="1">

**输入**：Baseline 作答前或作答后的同模型置信度信号，以及在开发集上确定的阈值。<br>
**输出**：Baseline 正确概率、失败风险排序，或由阈值映射得到的协议动作。

</div>

**直观理解**：这里先使用一个较粗的安全开关：模型若对直接作答有把握就停止，否则才投入协作成本。它主要解决“要不要升级”，并不假设一个置信度分数天然知道 PER 与 Broadcast 中哪一个更划算。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：论文没有提出新的端到端可微成本目标。轻量监督式路由器以五类 oracle 标签训练多类逻辑回归，即通过常规多类对数损失学习条件类别概率；超参数和训练轮次在开发集上选择，主要选择指标为宏平均 F1，并以较低超额成本打破并列。这里存在一个需要注意的目标错位：训练直接优化标签拟合，而最终部署关心求解率、token 成本以及升级不足或过度升级的方向，因此更高的分类质量不保证更好的成本效益。冻结 LLM 路由器和置信度探针不在该数据上更新参数，只通过提示和阈值进行推理；源节选未给出可忠实复写的新中央目标方程，故 equations 留空。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 四协议固定求解器执行栈**

Baseline、Single、PER 和 Broadcast 构成由直接推理到多智能体协作的四个离散动作。每个模型—数据条件内部固定求解器家族，只改变角色组织、迭代方式和协作强度，从而尽量隔离协议本身的边际价值；但论文也明确指出，观察到的 PER 与 Broadcast 差异不能直接识别因果机制。

> 直观理解：如果同时更换更强模型和协作方式，就无法判断提升来自哪里。固定求解器后，比较更接近“同一批人员采用不同工作流程”的效果，而不是“便宜人员与昂贵专家”的混合比较。

**2. 五分类成本感知路由器**

路由动作空间包含四协议和 None。学习式实现是多类逻辑回归，可使用 TF-IDF 文本特征、来源与领域特征及标准化难度字段；冻结 LLM 实现使用包含协议成本序和适用情形的分类提示，但不提供精确 token 预算。开发集以宏平均 F1 选择配置，并以较低超额成本打破并列，因此训练损失本身仍是分类对数损失，部署评价则是多维求解—成本指标。

> 直观理解：该模块尝试直接回答“该用哪条路线”。它同时保留简单模型和冻结大模型，是为了检查失败究竟来自特征过弱、监督标签不平衡，还是模型本身难以估计额外协作的边际收益。

**3. 失败风险与协作价值探针**

后答案探针把 confidence 解释为 Baseline 最终答案正确的概率，并要求输出 $[0,100]$ 内的整数；预答案探针在作答前产生成功概率，用于阈值门控。两类探针均不能访问标准答案、正确性、oracle 标签或协议结果，从而把 Baseline 失败风险预测与特定协议价值预测分开。

> 直观理解：判断一个答案看起来可疑，通常比判断“哪一种额外讨论恰好能修好它”容易。该模块用同一置信度信号依次测试这两个层次，避免把会识别风险误解成会做精细成本路由。

**训练与推理**

数据先按统一划分形成训练、开发和测试集合。学习式路由器只在训练题上拟合 TF-IDF 词表和分类器：主文本加元数据模型及仅元数据模型扫描正则化强度 $C\in\{0.25,1,4\}$ 与是否采用类别平衡权重，并以最多 30 个单轮 warm-start 增量监控开发集对数损失，实施早停；最终配置按开发集宏平均 F1 选择，若并列则选超额成本较低者。句向量消融使用冻结的小型编码器，将题目向量单独使用或与相同元数据拼接，再训练逻辑回归或 kNN；它用于检查低成本语义表示能否改善路由，不构成论文的新主模型。

测试时，每个路由器仅接收允许字段并输出一次动作。固定策略始终选择某一协议；监督式模型取预测类别；冻结 LLM 按统一成本顺序提示返回五个标签之一，解析失败则回退至 Baseline。置信度路径分为作答前与作答后：前者根据成功概率阈值决定是否升级，后者在 Baseline 已作答但协作尚未开始时估计该答案的正确概率。最后，离线评测器用匹配结果表回放该动作，统计真实解题与成本后果，并与固定顺序回顾性 oracle 比较。oracle 使用事后结果，因而只能衡量现有路由器尚未捕获的潜在空间，不能作为在线算法。

**复现信息**

主任务的轻量路由器采用 scikit-learn LogisticRegression，求解器为 saga，random_state 为 42。TF-IDF 使用小写化和 Unicode 重音剥离的词级一元组、二元组，min_df 为 2，max_features 为 20,000；元数据包括来源独热编码、领域路径多标签编码，以及标准化的 difficulty 与 difficulty_tier。主文本加元数据模型最终使用 $C=0.25$、不加类别权重，共 15,124 个特征；仅元数据模型同样使用 $C=0.25$ 和无类别权重，共 220 个特征。无难度等级消融同时移除两个数值难度字段，文本单独版本移除全部元数据。

API 协议轨迹、冻结路由器、成本提示、直接自评和协议价值探针通常采用 temperature 0.0，以减少采样噪声。冻结 LLM 路由提示只说明 Baseline、Single、PER、Broadcast 的序数成本关系，不提供精确 token 成本；无法解析为合法标签时统一回退到 Baseline，因此解析可靠性也是公平解释结果的一部分。预答案置信度只在成功解析的样本上分析：原文报告初始解析得到 310/423，人工重解析后为 329/423；其余包含截断与 HTTP 429，且缺失不能视为随机缺失。后答案探针也排除不可解析输出。上述清理规则意味着置信度门控结论适用于可恢复概率的子集，不能直接当作完整测试集上的无条件部署性能。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Omni-MATH 2 精确答案子集：主基准包含 4,181 道经人工修订的竞赛级数学题，并保留题源、领域路径、数值难度和十级难度层等元数据。作者按固定顺序 oracle 标签分层，以随机种子 42 做 80/10/10 划分，得到 3,342 道训练题、416 道开发题和 423 道测试题；训练集用于拟合路由器，开发集用于模型与超参数选择，测试集用于主要策略比较。
- JEEBench 与 SciBench：匹配协议结果的稳健性研究所用外部基准，分别覆盖工程入学考试类 STEM 问题和大学层次科学问题。给定节选只说明其评测角色，未报告样本规模、划分方式或具体结果。
- LAB-Bench：用于把评测扩展到生物学任务；路由器可见数据集名、领域、切片或子集、原始标识符、提示条件及子任务等字段。两个提示条件被视为两个评测条件，而不是两个独立基准；给定节选未报告规模及结果。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Solve rate**

测试题中所选协议最终答对的比例，用于衡量路由决策带来的任务成功覆盖率。 （越高越好，因为表示路由策略解决了更多题；但必须结合成本判断，不能单独说明策略具有更好的成本效益。）

</div>
<div class="metric-item" markdown="1">

**Average tokens**

每道题平均消耗的 token 数，包括实际协议执行以及路由器或置信度探针的开销；None 的协议成本为零，但决策开销仍计入。 （在成功率相近时越低越好，因为它表示达到相同解题覆盖率所需的计算成本更少。）

</div>
<div class="metric-item" markdown="1">

**Excess tokens**

相对于该题已实现固定顺序 oracle 成本的平均正向 token 超额支付；选择比 oracle 更昂贵的协议属于过度升级，而 oracle 为 None 时调用任一协议所花的 token 都是超额成本。 （越低越好，零表示在这组单次匹配执行上没有超过 oracle 的已实现成本；该指标不是相对于重复运行期望成本的遗憾值。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四种固定协议在主测试划分上的成功率与成本阶梯

<div class="result-value" markdown="1">

Baseline、Single、PER 和 Broadcast 的平均 token 消耗依次为 18.2K、47.6K、401.9K 和 622.1K，对应成功率为 56.3%、78.5%、84.9% 和 88.9%。更复杂协作确实提高了解题率，但从 Single 到 PER、Broadcast 的边际成功率提升伴随数量级更高的 token 成本，因此逐题路由具有实际必要性。

</div>

通俗地说，昂贵协议通常能多做对一些题，却不适合无条件用于所有题：Broadcast 相比 Baseline 多解决 32.6 个百分点，但平均 token 约为后者的 34 倍。这组结果建立了路由问题的收益与成本张力；它不证明某个协议在重复采样下必然更可靠，也没有单独证明路由器能提前识别哪些题值得升级。

<div class="result-source" markdown="1">

来源：Section 2, “Protocols”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the main held-out split, these protocols average 18.2K, 47.6K, 401.9K, and 622.1K tokens and solve 56.3%, 78.5%, 84.9%, and 88.9%, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Self-confidence gate 与固定 Baseline、Tier-majority 的主测试集比较

<div class="result-value" markdown="1">

自置信度门控取得 78.0% 的成功率，平均消耗 45.0K tokens，超额成本为 14.8K；相比固定 Baseline 的 56.3%、18.2K 和 1.7K，它用更高成本换取 21.7 个百分点的成功率提升。相比 Tier-majority 的 65.0%、28.9K 和 5.7K，它提高 13.0 个百分点，同时增加 16.1K 平均 token 和 9.1K 超额 token。

</div>

作者结果表明，自置信度能够形成较有效的低成本升级门：模型对直接答案缺乏信心时才调用更强协议，比始终使用廉价协议或仅按难度层多数标签选择更能覆盖失败题。分析上，这说明“预测当前尝试可能失败”对成本敏感路由有用；但其 78.0% 成功率仍低于 Broadcast 的 88.9%，而且该比较不能证明置信度准确预测了哪一种具体协作协议最划算。

<div class="result-source" markdown="1">

来源：Table 1, primary held-out test split, n=423

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Confidence Self-confidence gate 78.0 [74.0, 81.8] 45.0 [41.6, 48.7] 14.8 [12.2, 17.4]

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 冻结 gpt-oss-120b 路由器与事后固定顺序 oracle 的差距

<div class="result-value" markdown="1">

普通冻结 gpt-oss-120b 路由器达到 73.8% 成功率、71.3K 平均 token 和 37.1K 超额 token；事后固定顺序 oracle 达到 92.4%、101.1K 和 0.0K。两者相差 18.6 个成功率百分点，且冻结路由器虽平均花费更少，却仍产生较多相对 oracle 的过度付费。

</div>

这揭示了论文标题中的核心困难：大模型路由器并非只因预算不足而少解题，它还经常把计算花在与该题实际最低成功协议不匹配的动作上。oracle 的 92.4% 是四种协议在单次匹配运行中的并集上界，而非可在线达到的成绩；其 0 超额 token 由指标定义保证，因此不能当作现实系统的训练或推理性能。

<div class="result-source" markdown="1">

来源：Table 1, primary held-out test split, n=423

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Frozen LLM gpt-oss-120b 73.8 [69.5, 77.5] 71.3 [56.5, 86.7] 37.1 [24.2, 50.6]

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

- Baseline 固定策略：对每题只做一次直接求解且不自我修正，是成本最低的实际协议，用来衡量“不进行协议路由和协作”时的成功率与 token 下界。
- Tier-majority：根据训练集中每个难度层最常见的固定顺序 oracle 标签进行预测，遇到无对应层时退回训练集全局多数标签。它是透明的、只使用元数据的合理性检查，用于判断学习式方法是否超越简单难度分层规则。
- 冻结 gpt-oss-120b 路由器：接收相同的题目文本和元数据，通过只输出标签的提示选择动作，不更新模型参数。它检验通用大模型能否利用语义信息直接判断应采用哪种协议。
- Fixed-order oracle：事后检查同一道题四种协议的已实现结果，并按 Baseline、Single、PER、Broadcast 的总体成本顺序选择第一个成功动作，全部失败则选择 None。它是单次匹配执行上的诊断性上界和成本参照，不是可部署策略，也不是重复采样下的期望最优策略。

**实验想回答的问题**

- 在路由器看不到协议执行结果和正确答案的条件下，能否根据题目文本及允许的元数据，在 Baseline、Single、PER、Broadcast 与 None 五种动作之间逐题选择，从而以较低的 token 成本获得较高的解题成功率？
- 不同路由策略是否真正学会了“哪种协作协议值得付费”，以及显式成本提示、自置信度门控和更强的冻结大模型路由器分别如何改变成功率、平均成本与相对事后 oracle 的过度付费？

**实验实现**

主基准对每道题分别运行四种协议一次，且均使用同一 gpt-oss-120b 求解器栈：Baseline 是单次直接作答，Single 加入迭代自我修正，PER 设置规划者、执行者和审阅者角色，Broadcast 让多个智能体共享候选解并进行同伴认可。全部运行采用温度 0.0。路由器在协议运行前一次性选出 Baseline、Single、PER、Broadcast 或 None，且不能看到标准答案、正确性标签、oracle 标签或协议结果。学习式路由器是五分类逻辑回归，可使用允许的元数据，并可选加入由题目文本生成的 TF-IDF 词级 unigram 与 bigram；模型和超参数只在开发集选择。主测试集含 423 题，95% 置信区间由 2,000 次题目级 bootstrap 重采样得到。由于协议与路由调用均为确定性解码，这些区间反映有限测试题抽样的不确定性，而不反映重新随机运行模型的波动。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 在冻结 gpt-oss-120b 路由提示中加入数值化平均协议成本和简短路由示例 | 加入成本提示后，成功率由 73.8% 提高到 78.3%，即增加 4.5 个百分点；但平均 token 从 71.3K 增至 88.6K，超额 token 从 37.1K 增至 51.6K。换言之，显式给出成本信息没有降低支付成本，反而伴随更积极、也更昂贵的升级。 | 该消融隔离了“提示中明确告知成本及示例”这一因素。作者报告的数字说明它能多解决部分题，但分析上更像是改变了动作偏好、促使路由器选择更昂贵协议，而不是让模型更精确地判断哪项升级值得。由于置信区间较宽且原文节选未给出配对显著性检验，不能据此断言 4.5 个百分点的提升具有统计显著性。 | Table 1, primary held-out test split, n=423<br><span class="experiment-evidence">Frozen LLM gpt-oss + cost prompt 78.3 [74.2, 82.0] 88.6 [71.0, 107.6] 51.6 [35.2, 68.9]</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper studies cost-aware routing among LLM collaboration protocols across reasoning tasks, making multi-agent coordination and reasoning central.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`1f05ef92eab3f7eb3876dabf88715d0eb854106eacef82605f73c377e93bcfb6`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
