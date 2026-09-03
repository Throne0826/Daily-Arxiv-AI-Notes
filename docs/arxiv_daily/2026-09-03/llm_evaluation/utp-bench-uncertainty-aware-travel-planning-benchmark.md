---
title: "[论文解读] UTP-Bench: Uncertainty-aware Travel Planning Benchmark"
description: "[arXiv 2609.02421][LLM 评测] 原文未明确报告。"
arxiv_id: "2609.02421"
announcement_date: "2026-09-03"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-03T04:27:22.384898+00:00"
source_sha256: "b4c42a96908628b00d4da34f16f5c348fb507d7a982548f4f30b74dca8e228e2"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型旅行规划"
  - "不确定性感知规划"
  - "行程鲁棒性"
  - "交通延误"
  - "人流密度"
  - "旅行规划基准"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2609.02421</p>

# UTP-Bench: Uncertainty-aware Travel Planning Benchmark

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-03</span>
<span><strong>作者</strong> Etcharla Revanth Rao, Priyanshu Karmakar, Shubhojit Mallick, Manish Gupta, Shreya Ghosh, Abhik Jana</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Microsoft, India</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.02421v1) · [PDF 下载](https://arxiv.org/pdf/2609.02421v1) · **关键词** 大语言模型旅行规划, 不确定性感知规划, 行程鲁棒性, 交通延误, 人流密度, 旅行规划基准<br>
**代码**: [https://github.com/ETCHARLAREVANTHRAO/UTP-Bench](https://github.com/ETCHARLAREVANTHRAO/UTP-Bench)

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

本文位于大语言模型（LLM）自动旅行规划与基准评测交叉领域。旅行规划要求模型根据用户的目的地、出行天数、预算、偏好和时间要求，组织景点、餐厅、住宿及多模态交通，生成按天或按时段排列的行程。传统评测主要检查行程是否满足静态的空间、时间和预算约束；本文进一步将旅行环境视为随机环境，即交通延误、景点游览时长变化和人流波动可能使原本可行的计划失效，因此关注行程在扰动下的鲁棒性，而不仅是生成时刻的可行性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**约束满足与行程可行性**

约束满足是检查行程是否符合预先规定的条件，例如景点开放时间、交通连通性、预算和每日时间范围。静态可行性只判断计划当前是否成立，并不说明它能否承受实际旅行中的延误或拥堵。

</div>
<div class="concept-item" markdown="1">

**随机环境与鲁棒性**

随机环境中的交通耗时、人流密度或活动持续时间不是固定值，而是会按照某种经验分布变化。鲁棒性表示行程在这些变化发生后仍能继续执行、少发生连锁违约的能力。

</div>
<div class="concept-item" markdown="1">

**多模态交通与级联失效**

多模态交通是指在同一行程中组合不同交通方式，例如步行、道路交通或其他公共交通。级联失效指前一段交通延误后挤压后续活动时间，进而导致多个后续安排连续无法执行。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

UTP-Bench将任务设定为：给定一个真实旅行查询、旅行者的风险偏好以及覆盖多个城市和交通方式的旅行数据，LLM需要输出一个多日、细粒度的旅行行程，包含景点、餐厅、住宿和交通安排。数据集包含印度504座城市的现实旅行信息，并提供1000条覆盖3日、5日和7日旅行的查询及人工标注的黄金行程。与确定性设定不同，评测还输入经验交通延误统计和人流密度模式，通过随机扰动检验生成行程的时间缓冲、交通延误吸收能力和避开拥挤时段的能力；风险容忍型、风险优化型和风险规避型旅行者对应不同的可接受缓冲时间与行程密度。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D_{\mathrm{task}}$**

旅行规划任务或查询数据集，包含用户需求、地点、日期和相关约束。

</div>
<div class="notation-item" markdown="1">

**$I$**

模型生成的旅行行程输出，即按时间组织的活动、地点与交通安排。

</div>
<div class="notation-item" markdown="1">

**$\Delta t$**

交通或活动持续时间相对于计划值的随机延误或时间变化。

</div>
<div class="notation-item" markdown="1">

**$r$**

旅行者的风险偏好类型，用于表示对不确定性和行程密度的容忍程度。

</div>

</div>

**直接相关的工作**

- **TravelPlanner**: TravelPlanner使用真实旅行数据评估LLM是否能够满足景点、交通、时间和其他静态约束，为自动旅行行程生成提供了基准。但原文指出其假设固定交通时刻、固定活动时长和确定性交通条件，因此不能评估交通延误或人流变化下的行程鲁棒性。
- **TripCraft**: TripCraft扩展了细粒度的空间、时间和旅行者角色评测，使行程生成能够处理更复杂的长期约束和个性化需求。不过，原文指出其环境仍是确定性的；与其不同，UTP-Bench使用经验交通延误和人流模式来评估随机扰动下的行程表现。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现实旅行中的交通延误、拥堵、人流波动和活动耗时变化具有随机性。一个在固定时刻表下看似可行的行程，可能因某一段延误而引发后续活动连续错过；不同风险偏好的旅行者对缓冲时间和行程密度的接受程度也不同。因此，旅行规划系统不仅要生成满足预算、偏好和时间约束的计划，还需要判断计划在不确定事件发生后能否继续执行。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **确定性旅行规划基准**：TravelPlanner、TripCraft 和 ChinaTravel 等基准主要依据固定的交通时刻、游览时长与连接条件构造任务，再检查生成行程是否满足地点、时间、交通和用户偏好等静态约束。
- **静态约束满足评估**：现有评估通常把可行性视为二元结果：若计划在给定条件下没有时间或资源冲突，就判为满足约束；这种方式关注计划的名义可行性，而不模拟延误或动态人流对后续安排的影响。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 固定交通和活动时长的确定性假设忽略了真实延误、拥堵及多交通方式之间的依赖关系，导致静态可行的行程在实际执行时可能出现级联失败。
- 二元约束检查无法区分“刚好可行”和“留有余量”的计划，也不能衡量避开客流高峰的程度或计划是否符合旅行者的风险容忍度，因而不足以评价行程鲁棒性。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一个将经验交通延误分布、动态客流模式和旅行者风险偏好共同纳入的标准化测试环境，也缺少分别量化活动间缓冲、交通延误吸收能力与错峰安排质量的评估指标。因此，模型在真实随机条件下维持行程可执行性的能力无法被系统比较。

</div>
<div markdown="1"><span>核心问题</span>

如何构建一个基于真实旅行数据与经验不确定性信号的基准，并用可解释的指标检验大语言模型生成的多日行程能否在交通延误和客流变化下保持稳健，同时适配不同风险偏好的旅行者？

</div>
<div markdown="1"><span>作者直觉</span>

与其只检查行程在理想条件下是否排得下，不如直接考察其是否为活动转换留出余量、交通安排能否承受常见延误，以及景点访问是否避开拥挤时段。将这三类风险拆开度量，并结合风险容忍、风险优化和风险规避型旅行者画像，可以揭示两份表面上都“可行”的行程在实际可靠性上的差异。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

UTP-Bench 的方法重点不是训练一个新的旅行规划模型，而是构建一个能够检验不确定性鲁棒性的基准。其端到端流程为：从覆盖印度 504 个城市的真实旅行数据中建立结构化数据库，加入交通延误与人流密度信号；生成包含行程、预算、偏好和风险承受度的自然语言查询；由人工专家制作带有不确定性感知的金标准行程；最后使用结构约束检查和不确定性指标评估模型生成的行程。直观而言，该基准不只问“行程是否能按表执行”，还问“出现延误、拥挤或等待时间变化时，行程是否仍有足够余量”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 不确定性旅行数据库构建

作者收集并清洗覆盖 504 个城市、33 个印度邦和联邦属地的旅行实体与多模态交通数据，同时补充 20 个主要城市的历史交通延误统计和景点、餐厅的人流密度模式。缺失记录被删除或标准化；带有不确定性信号的交通数据包括 29,346 条航班、68,068 条火车和 34,925 条公交记录。

<div class="method-step__io" markdown="1">

**输入**：来自真实来源和开放资源的城市、景点、餐厅、住宿、航班、火车、公交、出租车、活动、交通站点及距离数据。<br>
**输出**：一个包含静态旅行信息与动态不确定性信号的结构化数据库，其中还包括 3,433 家餐厅、2,990 个景点、3,670 家住宿、783 个活动、10,025 个最近交通站点和 253,513 条距离关系。

</div>

**直观理解**：这一步相当于先制作一张“可查路线地图”，再为路线加上现实世界中的延误和拥挤信息。这样，评测时可以判断模型是否考虑了真实旅行中经常发生的变化，而不是只检查地点和时间是否形式上匹配。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 查询与风险画像生成

作者通过少样本方式使用 GPT-5 将结构化规划输入组合成自然语言查询，并为每个查询附加常识约束、硬约束和不确定性约束。行程长度决定地理范围：3 天聚焦一个目的地城市，5 天覆盖一个邦内的两个城市，7 天覆盖三个城市；查询还依据景点密度、交通连接复杂度和调度约束划分为 Easy、Medium 或 Hard。

<div class="method-step__io" markdown="1">

**输入**：出发城市、目的地、旅行日期、预算、旅行天数、旅行者类型、出行目的、消费偏好、地点偏好和风险画像。<br>
**输出**：1,000 条覆盖 3 天、5 天和 7 天行程的旅行查询，每条查询都带有偏好、可行性要求和风险承受类型，包括 Risk-Tolerant、Risk-Optimized 和 Risk-Averse。

</div>

**直观理解**：同一个目的地对不同人并没有唯一答案：有人愿意把日程排得很紧，有人需要较大的安全余量。风险画像把这种差异明确写入任务，使评测不仅考察行程可行性，也考察缓冲时间是否符合旅行者的风险偏好。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 人工金标准行程制作

14 名经过训练的标注员在辅助脚本支持下规划行程；脚本提供历史交通延误、拥挤模式和预计景点访问时长等上下文信息。标注员经过多轮修订，并为每个行程撰写说明，解释时间安排、约束满足和不确定性缓冲的决策。

<div class="method-step__io" markdown="1">

**输入**：结构化旅行查询、数据库中的延误与人流信息、约束条件和风险画像。<br>
**输出**：每条查询对应一个人工标注的金标准行程及其决策理由，目标是同时满足时间可行性、空间连贯性、用户偏好、交通延误吸收、人流敏感安排和风险画像。

</div>

**直观理解**：人工答案不是凭经验随意写出的“参考路线”，而是要求规划者查看延误和拥挤资料后再安排时间。它因此可以作为更现实的参照，用来衡量模型是否遗漏了人类规划者会主动加入的安全余量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 结构与不确定性评估

自动脚本检查时间一致性、实体正确性和关键行程约束，人工与领域专家审查则用于确认可行性、最优性及 persona 一致性。随后基于交通延误缓冲、拥挤时段安排和活动间隔余量计算 Buffer Adequacy Score、Crowd-Aware Timing Score 和 Transport Delay Absorption Score。

<div class="method-step__io" markdown="1">

**输入**：模型生成的旅行行程、人工金标准行程、数据库中的交通延误分布、人流密度模式及任务约束。<br>
**输出**：结构有效性结果、与查询约束和偏好的符合情况，以及反映行程在交通延误和人流波动下鲁棒性的三类指标结果。

</div>

**直观理解**：普通检查像是在问“这趟旅行有没有逻辑错误”；不确定性评估则进一步模拟“车晚点或景点变拥挤后还能不能接上下一项活动”。两类检查结合后，才能区分一个静态可行但脆弱的计划和一个具有恢复能力的计划。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告 UTP-Bench 自身的模型训练目标、损失函数或参数优化过程。该章节描述的是数据集和评测基准构建：查询由 GPT-5 少样本生成，金标准由人工标注员制作，LLM 的生成结果在评测阶段与约束和不确定性信号进行比较；因此不能据此推断作者训练了一个新的端到端规划模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 经验不确定性建模**

交通不确定性使用航班、火车和道路旅行的历史延误信号表示，覆盖航班、火车、公交和出租车等交通方式；人流不确定性使用景点与餐厅按小时变化的拥挤模式表示。数据分析报告火车平均延误为 40.8–46.7 分钟、延误航班平均延误为 40.59 分钟、道路旅行平均延误为 52.2 分钟，并指出平均延误大于中位数，说明分布具有偏斜和少量严重延误。

> 直观理解：系统不是假设所有交通都只晚点一个固定分钟数，而是使用历史上“通常会晚多少、偶尔会严重晚点”的现实信号。人流也按一天中的时段变化，因此午后景点和晚间餐厅可能需要不同的时间安排。

**2. 约束、persona 与风险画像**

基准保留 TripCraft 和 TravelPlanner 中的常识约束与硬约束，例如活动不能跨天重复、餐食需保持适当时间间隔、景点访问须按有效时间顺序排列，以及每日通常从指定住宿出发并返回。新增的不确定性约束要求交通缓冲能够覆盖经验延误，访问和等待时间反映高峰拥挤，并要求活动之间的间隔吸收交通和人流扰动；风险画像分别对应较小、中等和较大的缓冲偏好。

> 直观理解：硬约束保证行程“基本不出错”，不确定性约束保证它“遇到小波折也不容易崩溃”。风险画像则决定安全余量应该多大：风险厌恶者需要更保守，风险容忍者可以接受更紧凑的日程。

**3. 脚本辅助标注与质量控制**

辅助脚本向标注员呈现历史延误、拥挤密度和预计访问时长；多轮人工修订、领域专家反馈和最终人工审查共同验证行程的可行性、最优性、persona 一致性与风险配置。自动程序进一步检查时间一致性、实体正确性及关键结构约束。

> 直观理解：这一模块减少了人工规划时遗漏延误或拥挤因素的可能，也避免金标准只依赖单个标注员的主观判断。自动检查负责发现格式和逻辑错误，人工审查负责判断计划是否真的合理。

**训练与推理**

训练流程原文未明确报告。推理与评测流程是：向待测 LLM 提供 UTP-Bench 查询及相应的 uncertainty-aware prompting setting，获得模型生成的旅行行程；再使用数据库中的实体、距离、延误和人流信息检查其静态约束与不确定性约束，并计算 BAS、CATS 和 TDAS，同时可与人工金标准行程比较。原文未明确报告提示词的完整格式、是否调用外部工具、是否进行多轮模型修订或是否对模型参数进行微调。

**复现信息**

复现实验所需的已报告关键信息包括：数据覆盖印度 504 个城市和 33 个邦及联邦属地，交通与人流不确定性数据来自真实来源、网页抓取和 OpenStreetMap 等开放资源；历史人流信号覆盖 20 个主要印度城市；数据集含 1,000 条 3 天、5 天或 7 天查询，每条查询配有人工金标准行程。原文未明确报告延误分布的完整参数化形式、拥挤信号的具体离散化方法、BAS/CATS/TDAS 的计算公式、模型提示词全文、采样参数、重复运行次数或评测脚本的公开地址，因此这些细节不能从本节补充推断。

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

**Buffer Adequacy Score（BAS）**

BAS 衡量每个兴趣点的时间缓冲是否与基础游览时长、拥挤程度及旅行者风险偏好相匹配。对第 $i$ 个兴趣点，实际缓冲为 $B_a=(t_d-t_a)-v$，其中 $t_a$ 和 $t_d$ 分别为到达与离开时间，$v$ 为基础游览时长；最终对 $N$ 个兴趣点转移的惩罚取平均并从 $1$ 中扣除。 （越高越好，接近 $1$ 表示缓冲时间处于适合当前不确定性的范围；过紧会导致计划脆弱，过宽则表示时间利用低效。）

</div>
<div class="metric-item" markdown="1">

**Crowd-Aware Timing Score（CATS）**

CATS 衡量兴趣点访问时段是否避开高峰拥挤并贴合低拥挤时段。每次访问根据其持续时间与预定义拥挤窗口的重叠程度计算拥挤得分，并加入低密度时段奖励与高密度时段惩罚，最后对 $N$ 次访问的归一化得分取平均。 （越高越好，表示行程更持续地安排在有利的低拥挤时段。）

</div>
<div class="metric-item" markdown="1">

**Transport Delay Absorption Score（TDAS）**

TDAS 衡量交通区段预留的时间缓冲能否吸收历史数据中常见的延误，而不把扰动传播到后续活动。第 $j$ 个区段的隐含缓冲为 $B_j=\mathit{planned\_duration}_j-\mathit{hist\_duration}_j$，再将其与基于历史延误期望和旅行者风险偏好确定的可接受范围比较。 （越高越好，表示交通缓冲与预期延误更匹配；缓冲不足意味着计划易受延误破坏，过度缓冲则意味着效率损失。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。

**实验想回答的问题**

- 生成的旅行计划能否在交通延误、拥挤波动等随机扰动下保持时间安排的稳健性，而不仅满足静态可行性约束？
- BAS、CATS 与 TDAS 是否能够分别衡量景点缓冲时间、拥挤规避和交通延误吸收能力，并揭示人工计划与大语言模型计划之间的差异？

**实验实现**

原文摘录说明，UTP-Bench 同时使用 TripCraft 沿用的五项指标和三个不确定性感知指标，但所提供章节未给出具体数据集规模、训练测试划分、模型提示方式、重复次数或完整评测协议。评估计划时同时考虑硬约束、常识约束和不确定性约束；BAS、CATS 与 TDAS 分别对兴趣点时间缓冲、拥挤时段安排和交通区段延误吸收能力进行独立计算。附录进一步说明，每项指标分别对人工标注计划和大语言模型生成计划计算。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces a benchmark and metrics for evaluating LLM planning under stochastic travel delays and crowd uncertainty.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`b4c42a96908628b00d4da34f16f5c348fb507d7a982548f4f30b74dca8e228e2`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
