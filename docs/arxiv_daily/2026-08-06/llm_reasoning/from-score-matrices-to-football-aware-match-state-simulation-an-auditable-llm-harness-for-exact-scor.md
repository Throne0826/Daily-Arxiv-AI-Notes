---
title: "[论文解读] From Score Matrices to Football-Aware Match-State Simulation: An Auditable LLM Harness for Exact-Score Reranking"
description: "[arXiv 2608.05030][LLM Reasoning] 本文研究如何让大语言模型在不取代统计概率模型的前提下，利用阵容、战术、动机和比赛状态变化等足球语义，对固定的精确比分候选进行可审计的重排序。"
arxiv_id: "2608.05030"
announcement_date: "2026-08-06"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:59:28.484047+00:00"
source_sha256: "dc561689fde234dd5a5588f8d232b9a8046d9a896bd7c5723e9782a2e3ac8254"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "足球精确比分预测"
  - "Dixon–Coles 模型"
  - "Poisson 比分分布"
  - "大语言模型"
  - "比赛状态模拟"
  - "候选比分重排序"
  - "可审计信息支架"
  - "概率预测"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.05030</p>

# From Score Matrices to Football-Aware Match-State Simulation: An Auditable LLM Harness for Exact-Score Reranking

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Shaopeng Liang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.05030v1) · [PDF 下载](https://arxiv.org/pdf/2608.05030v1) · **关键词** 足球精确比分预测, Dixon–Coles 模型, Poisson 比分分布, 大语言模型, 比赛状态模拟, 候选比分重排序, 可审计信息支架, 概率预测<br>


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

本文研究如何让大语言模型在不取代统计概率模型的前提下，利用阵容、战术、动机和比赛状态变化等足球语义，对固定的精确比分候选进行可审计的重排序。

**不用术语来说**：精确预测足球比分很困难：进球数量少，偶然性高，而且率先进球后双方往往会立即改变攻守策略。传统统计模型能给出完整且自洽的比分概率，却难以判断某次伤停是否真正破坏球队结构、特定对位是否形成持续优势，以及比赛动机会让球队冒险还是保守；大语言模型能讨论这些因素，但直接让它猜比分又容易忽略可靠的统计规律，且其理由可能只是事后解释。因此，需要一种明确划分二者职责、并能追查每一步判断依据的组合方式。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出一种可审计的混合架构：统计模型负责估计比赛状态、生成比分概率先验及候选集合，信息支架负责定义输入、组织赛前证据与不确定性提示，大语言模型只负责足球语义推理和条件化的比赛进程模拟，最后由确定性程序验证输出。
- 通过四个版本记录接口设计的演化，尤其揭示从“让大语言模型修正两个期望进球率”转向“在冻结候选集上模拟首球、赛后反应与终止过程”的原因，并配套按时间顺序回放、预测前冻结响应以及存档和哈希机制，以暴露收益、失败情形与历史评估风险。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于足球赛前概率预测与大语言模型辅助推理的交叉研究。足球精确比分预测具有较高不确定性：单场进球数通常较少，常见低比分之间存在相关性，而且首个进球会改变领先方与落后方的风险偏好，使后续进球过程不再完全独立。Poisson 家族模型可根据球队攻防强度构造完整且内部一致的比分概率矩阵，Dixon–Coles 模型还会修正独立假设对若干低比分单元造成的偏差；动态权重和时间衰减则使近期比赛对当前实力估计影响更大。此类模型擅长提供数值先验，却难以直接理解关键球员缺阵、替补对推进或防守平衡的影响、局部对位、比赛动机以及进球后的战术变化。LLM 可以解释这些关系性语境，但其输出并非天然校准的概率分布，也不能被预设为具有稳定的顶级足球专业判断。因此，论文的基本立场不是用 LLM 替换统计模型，而是让统计模型负责概率结构，让受约束的 LLM 在该先验之上进行可审计的比赛机制推理。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**Poisson 比分模型**

该模型通常以主队和客队的期望进球数为参数，计算双方取得各个进球数的概率，再组合成完整比分矩阵。它提供的不只是一个预测比分，而是从 $0$ 比 $0$、$1$ 比 $0$ 到更高比分的一致概率分布。

</div>
<div class="concept-item" markdown="1">

**Dixon–Coles 低比分修正**

标准独立 Poisson 假设可能不能准确描述足球中若干常见低比分的相关性，Dixon–Coles 方法会针对受影响最大的低比分单元进行校正。本文将动态、比分驱动的 Dixon–Coles 系统作为纯数学基线 V1。

</div>
<div class="concept-item" markdown="1">

**概率校准与适当评分规则**

概率校准要求模型给出的置信度与事件实际发生频率相符；适当评分规则则鼓励模型诚实报告完整概率分布，例如 log loss、Brier score 和 ranked probability score（RPS）。由于后续 LLM 版本只输出候选比分排序而不输出归一化概率，论文指出这些规则只能用于 V1 的原生概率分布，不能直接用于 LLM 排序版本。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究问题是：在不允许 LLM 推翻冻结概率先验的条件下，LLM 能否加入有用且可审计的比赛机制推理，从而改善精确比分候选的排序？赛前输入包括统计模型估计的球队状态、期望进球及比分分布，由信息支架进一步提供字段定义、参照尺度、结构化球队与球员证据、不确定性提示和规定的推理路线。V1 直接按数学比分矩阵排序；V2 让 LLM 对足球语境评分，再通过学习到的数值桥梁把评分映射回期望进球参数 $\lambda$；V3 和 V4 则冻结统计模型给出的比分候选集合及其概率结构，让 LLM 构造逐球的因果比赛路径并重新排序候选，V4 进一步显式记录首次破门、进球后连锁反应和随时间停止进球等共同判断。系统输出主要是候选精确比分的有序列表，而 V1 还输出可归一化的赛果概率分布。研究设置为对 2025–26 英格兰足球超级联赛前 150 场比赛进行按时间顺序的历史回放；提示词与响应须在结果评分前冻结并留存输入、输出、验证决策及哈希，但作者明确警告：该开发切片并非未接触的独立基准，封闭权重 LLM 的历史结果记忆也无法仅靠输入时间隔离彻底排除。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\lambda$**

Poisson 家族比分模型中的期望进球参数；V2 将 LLM 的语境评分数值化后映射回该参数。

</div>
<div class="notation-item" markdown="1">

**$P(H=h,A=a)$**

主队进球数为 $h$、客队进球数为 $a$ 的联合比分概率；各个取值组成统计模型的比分矩阵。

</div>
<div class="notation-item" markdown="1">

**$h$**

某一候选比分中的主队进球数。

</div>
<div class="notation-item" markdown="1">

**$a$**

某一候选比分中的客队进球数。

</div>

</div>

**直接相关的工作**

- **Dixon–Coles 动态 Poisson 回归与低比分修正**: 它构成本文统计核心的直接基础：通过球队攻防效应建立联合比分分布，并修正独立 Poisson 对关键低比分单元的偏差。本文的 V1 是动态、比分驱动的 Dixon–Coles 基线，后续版本仍保留其概率先验与候选比分结构，而不是让 LLM 自由生成比分。
- **WorldCupArena**: 该基准在开球前可获得证据的约束下评估 LLM 与深度研究代理，并考察赛果、精确比分和分级比分指标。本文采取互补方向：重点不是测试 LLM 自身掌握了多少足球知识，而是研究如何通过固定接口把 LLM 接在比分分布模型之后，并完整保存输入、输出与验证过程以支持审计。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

赛前精确比分预测既需要稳定的数值先验，也需要理解临场足球机制。分析者不仅要估计双方通常能进多少球，还要判断关键球员缺席是否影响推进或防反保护、边锋与边后卫的对位能否反复制造机会、比赛目标是否鼓励风险，以及首球出现后领先方和落后方会如何调整。由于低比分之间存在相关性且比赛状态会反过来改变后续进球过程，遗漏这些机制会使精确比分排序十分脆弱。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **动态 Poisson 与 Dixon–Coles 类概率模型**：这类方法根据历史比赛动态估计球队强弱和双方期望进球率，并生成一张完整、自洽的比分概率矩阵；Dixon–Coles 修正用于更好地处理足球中相关的低比分结果，时间衰减或动态加权则让近期比赛对当前实力估计具有更大影响。其优势是保留概率一致性，并可直接支持精确比分和胜平负决策。
- **大语言模型直接预测或参数残差式混合方法**：直接预测方案让大语言模型阅读赛前信息后自由给出比分或解释；本文早期的 V2 则采用“数学模型 + 大语言模型 + 数学映射”的夹层结构：基础模型先产生期望进球参数，大语言模型评价阵容与情境因素，再由学习得到的数值桥接把评价压缩为对期望进球率的修正。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 纯概率模型擅长学习球队实力、进球均值和比分分布，却不具备足球语义层面的关系推理，难以区分伤停的结构性影响、替补带来的战术变化、特定对位和比赛动机，也不能显式刻画首球之后双方行为如何改变；其后果是统计先验可能遗漏决定候选比分相对次序的临场信息。
- 让大语言模型自由预测会带来三类风险：忽略数值先验、先给结论再生成貌似合理的解释，以及在历史回放中接触或记忆真实赛果。参数残差式混合也不能充分解决问题，因为它把复杂的情境判断压缩为少量标量修正；原文指出，全局残差只有很小且时间上不稳定的收益，球员状态判断可能有用，但汇总后的期望进球影响方向仍可能错误。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方案缺少一种受约束的系统接口：既让统计模型继续掌握概率先验与候选空间，避免大语言模型任意重写数值基础，又允许大语言模型沿可检查的因果路径表达首球归属、进球时间、领先或落后后的策略变化和连续进球效应。同时，这一接口还必须保存赛前证据、提示和响应，使研究者能够区分真实的机制推理、无效修正与潜在的赛果泄漏。

</div>
<div markdown="1"><span>核心问题</span>

在冻结的概率比分先验之下，大语言模型能否加入有用且可审计的比赛机制推理，从而改善精确比分候选排序，同时始终从属于统计模型所规定的候选范围与概率结构？

</div>
<div markdown="1"><span>作者直觉</span>

两类模型的长处具有互补性：统计模型像一张可靠的“比分地图”，规定哪些结果通常更可能；大语言模型则像受规则约束的比赛分析员，根据阵容、战术和动机为候选比分构造逐球路径。与其让大语言模型把全部语义压成一次期望进球率修正，不如要求它在同一批冻结候选上明确判断谁先破门、何时破门、双方随后收缩还是冒险，以及比赛何时趋于停止。这样既保留数值先验，又使候选之间的重排序理由能够被逐项检查。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法是一个可审计的混合预测系统：先用动态 Dixon–Coles 进球模型从历史比赛中估计主队和客队的期望进球参数 `$\lambda_H$`、`$\lambda_A$`，再将概率矩阵中概率最高的比分冻结为候选集合。随后，证据提示器向大语言模型提供赛前背景和候选比分，模型通过共享的首个破局判断、逐球路径模拟、进球后的攻防连锁判断以及时间感知的停止规则，对候选比分重新排序；最后由确定性验证器检查输出格式和候选合法性。直观地说，统计模型负责建立一个稳定的“比分地图”，大语言模型只在这张地图内解释足球情境并选择更合理的路线，因此不能随意改写概率参数或制造未列出的比分。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 动态统计先验与比分矩阵

V1 对每支球队维护进攻状态 `$a_{i,t}$` 和脆弱性状态 `$v_{i,t}$`，使其随距上次比赛的时间间隔衰减，并在每个日期批次后根据标准化且裁剪的进球创新更新；然后依据衰减后的状态计算 `$\lambda_H$` 和 `$\lambda_A$`，将独立 Poisson 进球概率乘以 Dixon–Coles 低比分修正并归一化。

<div class="method-step__io" markdown="1">

**输入**：按时间排列的历史比赛结果、球队身份、主客场信息，以及当前比赛的主队 `$H$` 和客队 `$A$`。<br>
**输出**：完整的比分概率矩阵 `$p(x,y)$`、由矩阵聚合得到的主胜/平局/客胜概率，以及按概率排序的冻结比分候选集合。

</div>

**直观理解**：这一步只回答“从长期实力和近期结果看，各个比分本来有多大可能”。它像一个持续更新的统计底盘：球队状态不会突然重置，但近期出现异常多或少的进球会逐步改变估计。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造可审计的赛前证据包

信息框架明确每项证据的含义、来源语境和不确定性，并要求大语言模型按来源可靠性和足球情境合理性判断信息价值，而不是进行关键词匹配。证据包还说明完整矩阵的语义和候选池边界，提示模型不能把赛后事实当作赛前已知信息。

<div class="method-step__io" markdown="1">

**输入**：统计先验的 `$\lambda_H$`、`$\lambda_A$`、比分矩阵及候选比分，另加开球时间、比赛背景、排名、赛季目标、近期状态、进球、阵型、休息时间、赛程拥挤、球员出场和伤停信息，以及赛前报道和战术对位。<br>
**输出**：一个包含结构化数值、冻结候选、注释证据和推理约束的比赛输入包，以及用于检查模型输出的提示契约。

</div>

**直观理解**：这一步相当于给模型一份带注释的赛前简报。它不仅告诉模型“发生了什么”，还告诉模型这些信息有多可靠、可能影响哪类比赛状态，从而使推理过程可以被复查。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### V4 共享根节点与逐球比赛模拟

V4 首先作一个所有路径共享的首个破局判断，估计 `$0$-$0$` 平衡是否容易被打破；随后建立逐球路径，每次只发生主队进球、客队进球或停止，并在每个节点记录比分、时间段、剩余时间以及继续进攻或停止的证据。首个进球后，模型共享判断进球机制能否重复、落后方是否有真实回应能力、领先方能否利用开放空间，并据此决定比赛趋于封闭、保持开放，或对称/不对称地扩大开放程度。

<div class="method-step__io" markdown="1">

**输入**：赛前证据包、V1 的冻结候选池和初始状态 `$0$-$0$`。<br>
**输出**：若干条从 `$0$-$0$` 出发的终止路径及其终端比分，随后从合法候选中形成重新排序的 Top-3 结果。

</div>

**直观理解**：模型不再只给每个比分贴一个静态分数，而是像复盘比赛一样问：“先发生哪个进球？剩余时间够不够？落后方能不能真的反击？上一个进球的模式会不会重复？”这样可以表达首球改变比赛行为的影响。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 尾部候选扩展与确定性验证

确定性构造器最多追加五个由矩阵派生的尾部锚点，包括高比分平局、高比分主胜、高比分客胜以及主客队大胜候选；这些候选可以参与排序但不是强制选择。验证器检查返回的比分是否属于允许的候选池、输出是否符合模式约束，并在预测冻结后由独立评估流程读取实际赛果。

<div class="method-step__io" markdown="1">

**输入**：V4 的路径结果、原始冻结候选池和 V1 概率矩阵。<br>
**输出**：通过格式和候选合法性检查的最终比分排名，以及用于后续 Top-1、Top-3 和 1X2 评估的冻结预测。

</div>

**直观理解**：尾部候选用于防止模型只在低比分区域思考，但它们必须来自统计矩阵，不能由模型凭空创造。验证器像门禁一样确保最终答案可追踪、可复现，并且没有偷偷使用赛果修改预测。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 球队状态的时间衰减

$$
a^{-}_{i,t}=a_{i,t^{-}}\exp\!\left(-\log 2\,\frac{\Delta t}{h}\right),\qquad v^{-}_{i,t}=v_{i,t^{-}}\exp\!\left(-\log 2\,\frac{\Delta t}{h}\right)
$$

**符号说明**

- $a^{-}_{i,t}$：球队 `$i$` 在比赛时刻 `$t$`、尚未吸收当前比赛新信息时的衰减后进攻状态。
- $v^{-}_{i,t}$：球队 `$i$` 在时刻 `$t$` 的衰减后防守脆弱性状态。
- $a_{i,t^{-}}$：球队 `$i$` 在上一个更新时刻的进攻状态。
- $v_{i,t^{-}}$：球队 `$i$` 在上一个更新时刻的脆弱性状态。
- $\Delta t$：当前比赛与上次状态更新之间的时间间隔，单位为天。
- $h$：状态半衰期；本文所选配置为 `$1440$` 天。
- $i$：球队索引。
- $t$：当前比赛或状态更新时间。

<div class="equation-explanation" markdown="1">

**直观理解**：指数项使状态随着时间逐渐回到零；当 `$\Delta t=h$` 时，状态大小变为原来的一半。它让模型既保留长期实力记忆，又降低很久以前信息对当前比赛的影响。<br>
**原文位置**：第 3.1 节，公式 (1)–(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### Dixon–Coles 修正比分概率

$$
p(x,y)=\frac{\operatorname{Pois}(x;\lambda_H)\operatorname{Pois}(y;\lambda_A)\tau_{xy}(\lambda_H,\lambda_A,\rho)}{Z}
$$

**符号说明**

- $p(x,y)$：主队进 `$x$` 球、客队进 `$y$` 球的归一化概率。
- $x$：主队进球数。
- $y$：客队进球数。
- $\operatorname{Pois}(x;\lambda_H)$：均值为主队期望进球 `$\lambda_H$` 时，主队进 `$x$` 球的 Poisson 概率。
- $\operatorname{Pois}(y;\lambda_A)$：均值为客队期望进球 `$\lambda_A$` 时，客队进 `$y$` 球的 Poisson 概率。
- $\lambda_H$：主队期望进球参数。
- $\lambda_A$：客队期望进球参数。
- $\tau_{xy}(\lambda_H,\lambda_A,\rho)$：Dixon–Coles 对低比分组合的依赖修正项。
- $\rho$：低比分修正参数，本文配置为 `$-0.05$`。
- $Z$：归一化常数，使所有比分概率总和为 `$1$`。

<div class="equation-explanation" markdown="1">

**直观理解**：公式先假设双方进球数分别服从 Poisson 分布，再专门修正低比分区域，最后重新归一化。得到的不是单一预测，而是一张可排序、也可聚合成主胜/平/客胜的完整概率矩阵。<br>
**原文位置**：第 3.1 节，公式 (4)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文没有给出 V4 大语言模型路径模拟的独立可微训练目标；V4 的路径判断通过提示契约和受限输出执行，而不是对大语言模型进行端到端梯度优化。V1 的配置通过历史比赛上的 1X2 概率表现进行选择，随后用冻结候选和赛前输入进行推理；V2 曾学习一个将四个相对攻防评分映射回 `$\lambda$` 的标量残差系数 `$\kappa$`，但该设计在时间上不稳定，因此没有成为最终方法的核心。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. V1 动态 Dixon–Coles 概率先验**

球队 `$i$` 的进攻状态和脆弱性状态使用相同半衰期衰减，所选配置为 `$h=1440$` 天；主客队期望进球分别为 `$\lambda_H=\mu_H\exp(a_H^-+v_A^-)$` 和 `$\lambda_A=\mu_A\exp(a_A^-+v_H^-)$`。独立 Poisson 分布通过 Dixon–Coles 修正 `$\tau_{xy}(\lambda_H,\lambda_A,\rho)$` 调整低比分依赖关系，其中 `$\rho=-0.05$`，并用 `$Z$` 归一化；攻击和脆弱性更新增益分别为 `$g_a=0.04$` 与 `$g_v=0.02$`。

> 直观理解：该模块负责概率上的一致性：它把球队当前状态转化为所有比分的完整分布，而不是只猜一个比分。低比分修正尤其重要，因为 `$0$-$0$`、`$1$-$0$`、`$0$-$1$` 等结果并不完全符合两个独立进球计数过程的假设。

**2. 赛前证据与提示契约**

信息框架同时提供数值先验、候选池、球队和比赛语境、球员可用性、赛前报道及战术对位，并明确证据截止时间及不确定性。大语言模型的职责是解释预测时刻可获得的信息及其影响程度，而不是验证报道最终是否正确，也不能编辑 `$\lambda$` 或应用隐藏的赛后加权公式。

> 直观理解：该模块把“足球常识”转化为有边界的输入接口。它的价值不在于增加更多文本，而在于规定模型应如何阅读文本、哪些事实不能使用，以及所有结论必须落在统计模型给出的候选范围内。

**3. V4 状态化路径模拟与验证器**

V4 在路径分叉前使用共享首球根判断，在每个节点显式记录比分、时间带、剩余时间和停止/继续证据，并在首球后使用共享 cascade 判断控制后续进球深度。模型输出必须来自冻结候选池，尾部候选由确定性规则从比分矩阵派生，最终由验证器执行模式和集合成员检查。

> 直观理解：该模块解决静态修正无法表达的条件变化：同一个战术信息在首球前后可能有不同作用。共享判断还减少了不同模拟路径之间相互矛盾的解释，使研究者可以追查模型为何停止、继续或扩大比分。

**训练与推理**

训练或选择阶段使用 2015–16 至 2024–25 的 `$18,665$` 场比赛，其中截至 2021–22 的赛季构成训练窗口，2022–23 至 2024–25 构成验证窗口；V1 在 `$5,330$` 场国内联赛验证比赛上选择配置。推理时，系统按时间顺序读取历史结果并更新球队状态，计算当前比赛的 `$\lambda_H$`、`$\lambda_A$` 和比分矩阵，选出并冻结候选池，再将赛前证据和候选语义交给大语言模型进行 V3/V4 路径模拟。V4 的输出经过确定性候选和模式验证后冻结，之后才由独立评估流程揭示赛果并计算预测指标；论文明确承认，封闭式大语言模型内部可能保留结果记忆，因此时间隔离不能完全排除信息泄漏。

**复现信息**

复现或公平解释结果时，关键约束是候选池冻结、V1 概率参数不可被大语言模型修改、不得由输出后公式进行隐性加权、每条路径只能通过主队进球、客队进球或停止推进，并且尾部候选必须由原始矩阵确定性派生。V3 模拟三条从 `$0$-$0$` 出发的路径并返回终端 Top-3；V4 保留该结构，增加共享首破局判断、时间感知停止、首球后的共享连锁判断，并最多追加五个尾部锚点。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 核心数据是 2025–26 赛季英格兰足球超级联赛前 150 场比赛，按时间顺序组成 15 轮、每轮 10 场，用于比较 V1、V3 和 V4。它是“临时开发基准”，不是独立测试集，因为前 100 场已经参与 V4 的设计。
- 前 100 场构成 V3 与 V4 的共享开发切片，用于描述版本迭代带来的变化，并分析级联标签和大分差信号。由于该切片直接推动了 V4 的设计，其结果只能用于形成假设，不能作为独立的泛化证据。
- 作者还按比赛类型从 150 场中提取诊断子集：43 场总进球不少于 4、24 场分差不少于 3、14 场真实比分为 $1$–$1$、8 场为 $0$–$0$。这些子集用于检查模型对中心低比分、无进球状态和比分分布尾部的识别能力，而不是额外训练集。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**精确比分 Top-1 / Top-3 准确率**

真实终场比分是否等于排名第一的候选，或是否出现在前三个候选中。该指标直接衡量精确比分选择能力，但不评价候选概率是否校准；Top-3 还同时受到候选覆盖率影响。 （越高越好，因为命中的比赛比例越高。）

</div>
<div class="metric-item" markdown="1">

**胜平负准确率（Score-derived 1X2 与 V1 native 1X2）**

Score-derived 1X2 将 Top-1 精确比分映射为主胜、平局或客胜；V1 native 1X2 则汇总整个比分矩阵后再取概率最大类别。二者的差异检验单个众数比分能否代表类别总概率。 （越高越好，但两种口径不可混为同一预测规则；native 1X2 更完整地利用了 V1 的概率分布。）

</div>
<div class="metric-item" markdown="1">

**Log loss、Brier score 与归一化 RPS**

三者只用于具有归一化胜平负概率的 V1。Log loss 对真实类别被赋予很低概率的情况惩罚较强；Brier score 衡量三类预测概率与独热真值的平方误差；RPS 利用主胜、平局、客胜的有序结构比较累积概率。V3 和 V4 只输出排序，不能通过任意设置名次权重得到有效的严格概率评分。 （均为越低越好，因为较小值表示概率预测与实际结果更接近。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 前 150 场核心基准上的精确比分排序

<div class="result-value" markdown="1">

V1、V3、V4 的 Top-1 分别为 15/150（10.0%）、18/150（12.0%）和 22/150（14.7%）；Top-3 分别为 40/150（26.7%）、45/150（30.0%）和 46/150（30.7%）。因此 V4 相对 V1 提高 Top-1 4.7 个百分点、Top-3 4.0 个百分点，但配对 McNemar 检验分别为 $p=0.2295$ 和 $p=0.3075$，未达到统计显著。

</div>

作者结果显示，加入足球语境级联模拟后，精确比分命中数呈递增趋势，主要增益体现在首选比分。不过样本只有 150 场，而且该切片参与过开发；不显著的配对检验意味着目前不能排除增益来自比赛样本波动。它证明的是该混合架构在开发回放中可产生更好的排序，而不是已经建立稳定的泛化优势。

<div class="result-source" markdown="1">

来源：第 6.1 节，表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

V4 improves Top-1 exact score by 4.7 percentage points over V1’s score-cell mode and Top-3 by 4.0 points. Its score-derived 1X2 accuracy is 18 points higher. Paired exact McNemar tests are not significant for Top-1 (p=0.2295) or Top-3 (p=0.3075); the score-derived 1X2 difference is significant (p=0.0024).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 前 150 场上的胜平负决策与 V1 概率质量

<div class="result-value" markdown="1">

由 Top-1 比分推导的胜平负准确率从 V1 的 32.0%提高到 V3 的 47.3%和 V4 的 50.0%；V4 相对 V1 的差异检验为 $p=0.0024$。但 V1 汇总整个比分矩阵后的原生胜平负准确率为 80/150（53.33%），仍高于 V4 的 50.0%；V1 的 log loss、Brier score 和归一化 RPS 分别为 0.987803、0.586970 和 0.209451。

</div>

V4 显著改善的是“首选精确比分所隐含的赛果方向”，并未超过 V1 利用全部概率质量做出的原生胜平负判断。原因是概率最大的单个比分格点可能是平局，而所有主胜比分的概率之和仍可能最大。因此该结果支持 LLM 重排改善比分模式选择，却不能证明它比统计矩阵更擅长胜平负概率预测；V3、V4 没有归一化后验，也无法与 V1 做 proper score 的公平比较。

<div class="result-source" markdown="1">

来源：第 6.1 节，表 2 与表 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

This last comparison must not be confused with V1’s native 1X2 decision, which reaches 53.3% and remains above V4’s score-derived 50.0%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 候选覆盖率提升与尾部候选的实际命中

<div class="result-value" markdown="1">

真实比分落入 V1 Top-10 的比赛为 116/150（77.3%）；V4 的确定性锚点将理论覆盖扩大到 127/150（84.7%），增加 11 场。然而新增锚点只有 3 场进入最终 Top-3，且没有一次精确命中。

</div>

尾部锚点缓解了“真实比分根本不在候选集合中”的上限问题，却没有改善最终 Top-3 命中。这将瓶颈定位为排序能力：系统能够把更多大比分或异常比分放入候选池，但 LLM 路径模拟尚不会在真正需要时将其提升。覆盖率上升因此不能被解读为预测质量等比例上升。

<div class="result-source" markdown="1">

来源：第 6.3 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The true score appeared in V1’s Top-10 for 116 of 150 matches (77.3%). V4’s deterministic anchors expanded theoretical coverage to 127 matches (84.7%), an increase of 11. Yet an added anchor entered the final Top-3 in only 3 matches, and none was an exact hit.

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

- V1 score order：动态、比分驱动的 Dixon–Coles/Poisson 统计模型直接按比分矩阵中的单个格点排序。它是最关键的统计基线，用于检验 LLM 模拟是否比校准良好的结构化比分先验提供额外排序价值。
- V1 native 1X2：先将完整比分矩阵按主胜、平局、客胜汇总，再选择概率最大的类别。它不与精确比分排序解决同一决策问题，但可判断“首选比分隐含的胜平负”是否错误代表了统计模型本身的胜平负能力。
- V3 path simulation：在冻结的比分候选集合上执行逐球路径模拟，不包含 V4 的共享首球突破判断、进球后级联判断、时间感知停止和确定性尾部候选。它用于隔离从基础路径模拟升级到 V4 级联模拟的增量效果。
- V4 cascade simulation：完整方法本身，加入共享的首次突破与进球后比赛走势判断、时间感知停止机制及确定性尾部锚点；它与 V1、V3 的比较分别测试混合架构的总体价值和新增设计的边际价值。

**实验想回答的问题**

- 在按时间顺序回放英超比赛时，引入受约束的 LLM 逐球路径与进球后级联推理，能否相对 V1 统计基线提高精确比分 Top-1、Top-3 以及由首选比分推导的胜平负判断？
- 性能瓶颈究竟来自候选比分集合未覆盖真实比分，还是来自排序器无法识别并提升 $0$–$0$、大比分和大分差等尾部候选；同时，V4 暴露出的首球与比赛开放度判断是否具有可用的区分能力？

**实验实现**

实验按日期批次进行时间顺序回放：每轮最多并发处理 10 场，但各场相互独立并使用新的 LLM 上下文；同轮预测全部完成后，才将该轮赛果用于 V1 在线更新，因而避免同轮结果泄漏。提示词、证据包、结构化响应、模式版本、模型标识和内容哈希在独立评估器读取结果前写入并同步，以便审计。该流程只保证“时间输入隔离”：封闭权重 LLM 在赛季结束后运行，作者没有检测其参数或检索历史是否记忆赛果。V1 的截断比分矩阵逐场重新归一化后计算概率指标；V3、V4 因只给候选顺序，不报告人为构造的概率评分。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 前 100 场共享开发切片：V3 路径模拟升级为 V4 级联模拟 | V3 的 Top-1、Top-3 和 score-derived 1X2 命中数分别为 13、29、47；V4 分别为 14、32、49，即增加 1、3、2 场命中。 | 该对比共同反映 V4 新增的首球突破判断、进球后级联、时间停止和尾部锚点的总体增量，不能进一步归因到某一个组件。由于这 100 场正是推动 V4 设计的数据，它属于开发集上的描述性消融，容易受到针对性调试影响，不是独立因果证据。 | 第 6.2 节，表 4<br><span class="experiment-evidence">Relative to V3, V4 added one Top-1 hit, three Top-3 hits, and two score-derived 1X2 hits. These counts are descriptive development results rather than independent evidence.</span> |
| V4 大分差调整信号在前 100 场中的诊断 | 大分差调整值至少为 2.0 的比赛共有 4 场，其中 3 场实际分差至少为 3；但 100 场内共有 15 个此类尾部事件，因此该信号的命中精度为 3/4、召回仅为 3/15，且尚未接入训练后的排序规则。 | 这一诊断隔离的是“大分差调整”能否识别极端赛果。它在少数高置信触发上较准确，却漏掉绝大多数大分差比赛；更重要的是，信号未被系统性映射到候选排名，因此不能把诊断精度直接视为最终预测收益。 | 第 6.4 节<br><span class="experiment-evidence">In the first 100 matches, four fixtures received a value of at least 2.0; three truly ended with a margin of at least three goals. This is high precision but low recall (3 of 15 tail events) and was not yet mapped into a trained ranking rule.</span> |

**定性案例**

- 按真实比分类型聚合的案例显示明显的不对称：14 场 $1$–$1$ 中，V4 有 4 场将其排第一、10 场放入 Top-3；8 场 $0$–$0$ 则无一进入 Top-3。作者据此认为模型更会在常见低比分之间选择，却不能识别真正的“无突破”状态。结合全部 150 场根节点均选择 first_goal_more_likely，这不是个别比赛失误，而是首球判断缺乏校准的系统性迹象。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The contribution centers on constraining LLM contextual reasoning within an auditable football match-state simulation and reranking harness.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`dc561689fde234dd5a5588f8d232b9a8046d9a896bd7c5723e9782a2e3ac8254`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
