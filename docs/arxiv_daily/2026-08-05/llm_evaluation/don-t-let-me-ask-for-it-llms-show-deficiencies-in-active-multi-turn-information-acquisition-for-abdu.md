---
title: "[论文解读] Don't Let Me Ask for It: LLMs Show Deficiencies in Active Multi-Turn Information Acquisition for Abductive Inference"
description: "[arXiv 2608.03388][LLM 评测] 本文提出交互式探针 Alien Abduction，用受控的黑盒函数归纳任务检验大语言模型能否主动选择证据、依据新证据修正假设，并在证据充分时停止探索。"
arxiv_id: "2608.03388"
announcement_date: "2026-08-05"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:40:56.729668+00:00"
source_sha256: "ab11feccb0d64b4d3e74ee246e77d142a1e37036e5998f94a79fd859126ac801"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "溯因推理"
  - "主动信息获取"
  - "多轮交互"
  - "黑盒函数归纳"
  - "程序综合"
  - "假设一致性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.03388</p>

# Don't Let Me Ask for It: LLMs Show Deficiencies in Active Multi-Turn Information Acquisition for Abductive Inference

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Shahrukh Mohiuddin, Chalamalasetti Kranti, Sherzod Hakimov, David Schlangen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Computational Linguistics, Department of Linguistics；University of Potsdam, Germany；German Research Center for Artificial Intelligence (DFKI), Berlin, Germany</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03388v1) · [PDF 下载](https://arxiv.org/pdf/2608.03388v1) · **关键词** 溯因推理, 主动信息获取, 多轮交互, 黑盒函数归纳, 程序综合, 假设一致性<br>


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

本文提出交互式探针 Alien Abduction，用受控的黑盒函数归纳任务检验大语言模型能否主动选择证据、依据新证据修正假设，并在证据充分时停止探索。

**不用术语来说**：现实中的智能体通常不会一开始就获得全部信息，而要通过提问或试验逐步弄清未知规则。例如，模型面对一个只知道输入输出接口、却不知道内部实现的工具时，需要决定先测试什么、如何利用测试结果排除错误猜测，以及何时已有足够把握提交答案。传统单轮评测只检查最终答案，因而无法区分模型是真正善于搜集和利用证据，还是仅在信息已被整理好时能够解题。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 构建 Alien Abduction 黑盒函数归纳游戏：模型仅获得隐藏 Python 函数的签名，并须在有限轮次内重建函数；六种模式系统改变证据由模型还是裁判选择、反馈为精确输出还是候选输入—输出对的二元判定，从而能够比较主动与被动、单轮与多轮的信息获取。
- 建立面向推理过程而非仅面向最终答案的评估框架：使用五个领域的 50 个经自动验证的目标函数，在沙箱和留出测试用例上检验最终程序，同时分析轮次预算使用情况以及显式中间假设与累计证据的一致性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型的交互式黑盒规则发现与程序归纳研究交叉点。不同于根据自然语言规格生成代码，或对可见程序预测输入输出，这里的模型既看不到目标代码，也没有完整行为说明，只能通过有限次数的交互收集证据，再重建隐藏函数。该过程同时涉及溯因、演绎与归纳：先从观测提出可能的规则，用规则预测新案例，再依据反馈修正假设；因此，评价重点不应只有最终代码是否正确，还应包括模型能否主动选择有信息量的查询、利用反例排除竞争假设，以及在证据充分时停止探索。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**溯因推理**

从已经观察到的现象出发，提出一个能够解释这些现象的候选假设。它寻找的是合理解释，而非仅由前提必然推出的结论，因此后续必须用新证据检验和修正。

</div>
<div class="concept-item" markdown="1">

**黑盒函数归纳**

模型无法查看目标函数的实现，只能依据函数签名及若干输入输出行为推断其规则。最终目标是写出一个在未见测试输入上也与隐藏函数一致的程序，而不是记住已观察样例。

</div>
<div class="concept-item" markdown="1">

**主动信息获取与成员判定反馈**

主动信息获取指模型自行选择下一次测试什么；成员判定反馈则只告知模型提出的输入—输出配对是否正确，而不直接给出真实输出。后一种反馈要求模型设计能够证实或否定候选规则的测试，尤其需要主动寻找反例。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

在 Alien Abduction 游戏中，游戏主持人隐藏一个目标 Python 函数 $f$，模型初始只获得其函数签名，并受到有限交互轮数约束。依据模式不同，证据可以一次性提供或逐轮给出，查询可以由模型主动选择或由预言机提供，反馈则可能是给定输入 $x$ 的精确输出 $f(x)$，也可能只是对候选输入—输出对 $(x,y)$ 的二元正确性判定。模型最终提交作为假设的 Python 函数 $\hat{f}$，系统在沙箱中用未公开的保留测试案例比较 $\hat{f}$ 与 $f$；除任务成功与轮数使用外，论文还关注最终假设是否与交互期间已经获得的证据一致。目标函数共 50 个，覆盖数值、数值对、字符串、列表和布尔逻辑五类输入或规则域。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$f$**

由游戏主持人隐藏、需要模型重建的目标 Python 函数。

</div>
<div class="notation-item" markdown="1">

**$x$**

提交给目标函数的测试输入。

</div>
<div class="notation-item" markdown="1">

**$y$**

模型为输入提出的候选输出；在成员判定模式中，系统只判断该输出是否等于真实的 $f(x)$。

</div>
<div class="notation-item" markdown="1">

**$\hat{f}$**

模型在交互结束时提交的候选函数或最终规则假设。

</div>

</div>

**直接相关的工作**

- **CodeARC（Wei et al., 2025）**: 与本文最接近的交互式程序综合基准之一：智能体可查询隐藏目标函数，并依据差分测试反馈迭代 Python 实现。Alien Abduction 在相同隐藏函数上进一步控制证据由谁选择及反馈采用精确输出还是二元判定，并检查最终假设是否符合模型自己收集的证据。
- **Geng et al.（2025）**: 该工作比较大语言模型逆向推断程序、形式语言和方程时的被动观察与主动干预，但只使用精确输出反馈。本文据此补充成员判定及否定性证据条件，从而研究模型是否会设计能够区分竞争假设的查询。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型正被部署为需要与陌生环境、工具和 API 交互的智能体。在缺少完整说明时，成功不仅取决于能否写出一个看似合理的规则，还取决于能否主动设计有信息量的试验、利用支持性与反驳性证据更新解释，并避免过早提交或无休止地继续查询。因此，需要一种能够把“最终是否答对”与“如何获得、验证和管理证据”分开考察的受控评测。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **单轮推理与代码生成基准**：这类评测通常预先给出全部题目信息、显式规格或可见程序，要求模型一次性生成答案或代码，并主要依据最终答案是否正确评分。它们适合测量在信息已经组织好的条件下完成推理或实现规格的能力。
- **交互式程序合成与规则发现基准**：这类方法允许智能体查询隐藏函数，或根据给定示例和主动查询逐步归纳规则；黑盒推理环境还把隐藏规则发现扩展到更多任务领域。已有主动—被动信息收集比较主要采用返回精确输出的反馈形式。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有设置没有同时系统控制“由谁选择证据”和“反馈以何种形式给出”。特别是，主动与被动证据收集的既有比较主要返回精确输出，因而难以判断模型面对二元正确性反馈时，是否会主动寻找能够否定当前猜测的证据。
- 既有评测多聚焦最终答案正确性，没有检验模型逐轮陈述的中间假设是否始终符合其已收集证据。其后果是，即使最终失败或偶然成功，也难以定位问题究竟来自查询选择不佳、未根据反例修正假设，还是停止时机不当。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一个统一、受控的交互框架，能够正交比较主动与被动取证、精确输出与二元成员判定、单轮与多轮信息呈现，并把最终任务成功与证据一致性、假设修正和轮次预算管理联系起来。由此，自主探索是否真正提高了规则辨识能力、负面证据是否被有效利用，以及模型的显式假设是否扎根于累计证据，仍未得到充分研究。

</div>
<div markdown="1"><span>核心问题</span>

当大语言模型需要在有限轮次内重建未知函数时，证据控制权、反馈形式以及信息是一次给全还是逐轮提供，会怎样影响其查询选择、假设形成与修正、证据一致性、停止决策和最终成功率？

</div>
<div markdown="1"><span>作者直觉</span>

隐藏函数提供了一个可精确执行和验证的未知规则，而不同交互模式则像实验中的控制变量：保持目标任务不变，只改变谁挑选例子以及模型看到的是完整输出还是“对/错”判定。这样可以观察模型是否会设计能够区分多个候选规则的测试，而不只是寻找符合当前猜测的例子；逐轮记录显式假设并与累计证据核对，还能揭示模型究竟是在持续缩小候选范围，还是仅让当前解释适配自己选择的证据。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文提出 Alien Abduction 游戏，将溯因推理建模为对隐藏函数的交互式识别。每个实例给定函数签名、交互模式与轮次预算 $T$，但不公开目标函数 $f:X\to Y$ 的源码；模型通过主动设计测试或接收 Game Master 提供的证据，逐轮形成、检验并修正假设，最后以 Python 代码提交候选实现 $\hat f$。系统在未公开的留出输入上执行该代码，只有当 $\hat f$ 与 $f$ 一致时才判定成功。

方法的关键不是提出新的训练算法，而是用六种受控模式分解信息获取过程中的两个因素：证据由模型还是 oracle 选择，以及反馈是精确输出还是二元成员关系判断；另外再比较证据一次性给出与逐轮给出。通俗地说，这是一场“猜黑箱程序”的游戏：既考查模型能否根据例子猜出规律，也考查它会不会主动询问最能排除错误规律的问题、能否根据反例更新判断，以及是否知道何时已有足够证据可以作答。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 初始化隐藏函数识别实例

Game Master 保留对 $f$ 的 oracle 访问权，仅向模型公开参数类型、返回类型和协议；目标函数的源码与最终留出测试输入均不公开。若 $X$ 是多变量域，则一个输入 $x$ 可以包含多个参数值。

<div class="method-step__io" markdown="1">

**输入**：隐藏目标函数 $f:X\to Y$、函数签名、六种交互模式之一，以及最大轮次预算 $T$。<br>
**输出**：一个受固定协议约束的黑箱函数识别任务。

</div>

**直观理解**：模型知道程序“吃什么、吐什么”，但不知道内部规则。它只能像做科学实验一样通过有限观察反推规律。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 按模式获取证据

在主动模式中，模型自行选择探针：AO 查询输入 $x$ 并获得精确输出 $f(x)$，AV 提交候选对 $(x,y)$ 并获得其是否属于函数图 $F_f$ 的布尔判断。在被动模式中，模型请求下一条 oracle 证据：PO 获得有效输入输出对，PV 获得带真伪标签的候选对；STO 与 STV 则在作答前一次性分别给出十条输出证据或十条带标签证据。

<div class="method-step__io" markdown="1">

**输入**：当前证据历史、模型的当前假设，以及该实例所规定的证据控制方式和反馈形式。<br>
**输出**：精确输出证据、正负成员关系证据，或预先给出的固定证据批次。

</div>

**直观理解**：AO 类似让模型自己挑输入并查看答案；AV 类似让模型问“我猜这个输入会得到这个输出，对不对”。被动模式则由出题者决定给哪些例子，因此可区分“推理能力不足”和“不会挑关键问题”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 逐轮维护并记录假设状态

在每个满足 $t\leq T$ 的回合，模型只能请求一条协议允许的证据，或通过 SOLVE 提交候选实现 $\hat f$ 并终止实例；同时报告当前假设、处于 probing、confirming 或 uncertain 的状态、选择该查询的理由和置信度。这些附加字段只用于行为分析，不会被 Game Master 处理，也不会改变后续反馈。

<div class="method-step__io" markdown="1">

**输入**：新获得的证据、此前的交互历史与剩余轮次。<br>
**输出**：更新后的行为轨迹，或一个终止交互的候选 Python 实现 $\hat f$。

</div>

**直观理解**：研究者不仅查看最终答案，还记录模型是在探索新规律、确认已有猜测，还是仍不确定。这样可以分析失败究竟源于过早作答、无效询问，还是到预算耗尽仍无法收敛。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 隔离执行并判定解答

系统在临时隔离容器中执行 $\hat f$，比较其输出与隐藏函数 $f$ 在留出输入上的输出；仅当两者全部满足测试所要求的一致性时，实例才算 solved。模型若在 $T$ 个回合内没有提交，则直接记为失败；单轮模式在固定十条证据给出后只允许执行 SOLVE。

<div class="method-step__io" markdown="1">

**输入**：模型通过 SOLVE 提交的 Python 实现 $\hat f$，以及每个实例专门构造且未向模型公开的留出测试输入。<br>
**输出**：该实例的成功或失败判定，以及可供后续分析的完整交互记录。

</div>

**直观理解**：模型不能只用一句自然语言描述看似合理的规律，而必须交付真正可运行的程序，并通过未见样例检查。隐藏测试可避免模型仅复述已经观察到的输入输出对。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 隐藏目标函数及其函数图

$$
f:X\rightarrow Y,\qquad F_f=\{(x,y)\in X\times Y\mid y=f(x)\}
$$

**符号说明**

- $f$：玩家需要识别、但无法查看源码的隐藏目标函数
- $X$：目标函数的输入域；输入可以由一个或多个参数值组成
- $Y$：目标函数的输出域
- $x$：一个具体输入
- $y$：与输入对应的候选或真实输出
- $F_f$：函数 $f$ 的图，即所有满足 $y=f(x)$ 的有效输入输出对组成的集合

<div class="equation-explanation" markdown="1">

**直观理解**：该定义统一了两类反馈：输出模式直接揭示某个属于 $F_f$ 的有效对，成员判断模式则回答候选对是否属于 $F_f$。因此六种模式虽然交互方式不同，最终都在帮助模型恢复同一个隐藏映射关系。<br>
**原文位置**：第 3.1 节 Task Formulation

</div>

</div>

<div class="equation-block" markdown="1">

#### 回合动作与成功条件

$$
t\leq T,\qquad \mathrm{Solved}(\hat f)\iff \forall x\in H,\ \hat f(x)=f(x)
$$

**符号说明**

- $t$：当前交互回合编号
- $T$：该实例允许的最大回合数
- $\hat f$：模型通过 SOLVE 提交的候选 Python 函数
- $H$：按实例构造且不向模型公开的留出测试输入集合
- $\mathrm{Solved}(\hat f)$：候选实现通过验证、该实例被判定为成功

<div class="equation-explanation" markdown="1">

**直观理解**：原文以文字规定：每轮只能取证或提交，而提交后要在未公开测试输入上与目标函数一致。这里将这一判定忠实整理为逻辑式；它强调成功取决于隐藏样例上的行为一致性，而不是假设说明写得是否合理。<br>
**原文位置**：第 3.1 节 Task Formulation；原文未给出独立公式编号

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该方法是面向现成大语言模型的交互式评测框架，没有定义参数训练、损失函数或梯度优化目标；模型的任务目标是在预算 $T$ 内利用证据提交可通过隐藏测试的 $\hat f$。置信度、查询理由和假设状态仅被记录用于分析，不参与奖励计算，也不影响 Game Master 的响应。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 证据控制模块**

该维度区分 active 与 passive：active 由模型选择要测试的输入或输入输出对，passive 由 Game Master 决定下一条证据。AO 与 PO 的对比用于考查主动选点的影响，而 PO 与 STO 的对比可在同为被动证据的前提下考查逐轮呈现相对于一次性呈现的影响。

> 直观理解：它回答“失败是因为不会根据证据推理，还是因为不会问有价值的问题”。把提问权交给不同一方，可以单独观察信息选择策略的作用。

**2. 反馈形式模块**

output 反馈直接返回 $f(x)$，因此提供有效函数对这一正证据；membership 反馈判断 $(x,y)\in F_f$ 是否成立，可同时产生正证据与负证据。AV 允许模型直接尝试证伪自己的预测，PV 则由 oracle 提供带真伪标签的对比证据。

> 直观理解：精确输出告诉模型“正确答案是什么”，成员判断只告诉它“这个猜测对不对”。后者虽然信息形式更弱，却能明确否定某个假设，因此可检查模型是否善于利用反例。

**3. 时序与终止模块**

AO、AV、PO、PV 在预算 $T$ 内逐轮交换证据，模型可在任意回合选择 SOLVE；STO、STV 将固定十条证据一次性展示，并只允许随后提交答案。预算耗尽而未提交被定义为失败，从而同时测量证据利用、假设收敛与停止决策。

> 直观理解：即使模型最终可能猜到规律，如果它过早提交或一直询问而不作答，仍会失败。该模块因此把“会不会推理”扩展为“会不会在有限资源下完成整个调查过程”。

**训练与推理**

论文所述流程属于推理时评测而非训练。对每个 episode，系统先选定隐藏函数、签名、模式和预算；多轮模式下，模型根据历史选择 TEST、NEXT 或 SOLVE，其中允许的动作及返回内容由 AO、AV、PO、PV 协议决定。每获得一条证据后，模型可更新假设并决定继续取证还是提交；单轮模式则先展示固定的十条证据，随后模型只能 SOLVE。提交后系统执行候选代码并用留出输入验证；若模型未在预算内提交，episode 记为失败。

**复现信息**

公平解释结果所必需的实现约束包括：候选解必须是 Python 代码；验证通过实际执行而非自然语言匹配完成；代码运行在临时隔离容器中；留出测试输入按实例构造且始终对模型隐藏。六种模式形成受控比较：STO 与 PO 主要隔离一次性证据和逐轮证据的差异，PO 与 AO 主要隔离 oracle 选证据和模型主动选证据的差异；output 与 verdict 模式则区分精确输出证据和二元成员判断证据。除单轮模式固定展示十条证据外，所给第 3 节摘录未明确报告具体 $T$、提示模板、采样参数或留出集规模。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Alien Abduction 基准包含 5 个类型域：单整数、整数对、字符串、整数列表和布尔逻辑；每个域有 10 个隐藏目标函数，共 50 个。函数均为短小、纯函数、确定性且仅使用标准库的 Python 变换。候选函数由 GPT5.4 生成并经语法、签名和可执行性检查，再以固定随机种子抽样；所有交互模式使用同一组目标，以避免模式差异被函数难度混淆。
- 每个目标函数配有 100 个类型感知测试用例，共对应 5,000 个目标—输入实例。输入池同时包含零、负数、空字符串、空列表等边界情况和随机值，输出由实际执行目标函数得到。这些用例一方面是在被动模式和单轮模式中提供的证据，另一方面构成检验最终假设的留出测试套件；原文未明确报告训练集、验证集与测试集的传统划分。
- 评测覆盖 GPT5.4、GPT5.4-mini、Mistral-Large-3 和开放权重模型 Qwen3.6-35B-A3B。每个模型在 50 个目标和 6 种交互模式上运行，共 300 个 episode；这一设置主要比较同一任务在不同证据获取机制下的行为，而不是比较不同数据集上的迁移能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**成功率（Success rate）**

若模型提交的假设通过隐藏函数的全部留出测试，该 episode 记为 1，否则记为 0，再按模型、模式或领域取平均。它衡量最终恢复的函数在测试套件上的行为是否正确，而不是代码文本是否与目标实现完全相同。 （越高越好，因为更高值表示更多最终假设通过了全部留出测试。）

</div>
<div class="metric-item" markdown="1">

**轮次预算使用率（Turn Budget Use, TBU）**

交互模式下定义为 $\mathrm{TBU}=(n-1)/T$，其中 $n$ 是已使用轮数，$T$ 是最大轮次预算；本文令 $T=15$。它衡量 episode 结束前消耗了多少交互预算，但不能单独区分高效求解、过早提交和耗尽预算仍未收敛。 （不存在统一的越高或越低越好；必须结合成功率解释。成功且较低可表示高效停止，失败且较低可能是过早承诺，失败且接近 1 则可能是无法收敛。）

</div>
<div class="metric-item" markdown="1">

**假设回溯预测准确率（Hypothesis Retrodiction Accuracy, HRA）**

第 $t$ 轮定义为 $\mathrm{HRA}_t=N_t^{\mathrm{matched}}/N_t$，其中 $N_t^{\mathrm{matched}}$ 是当前假设能够正确复现的已观察证据数，$N_t$ 是截至该轮的证据总数。它检查当前假设是否与已积累证据一致，而不直接保证该假设能区分尚未观察到的竞争规则。 （越高越好；$1$ 表示当前假设与全部已观察证据一致，但若证据由模型自行选择且覆盖狭窄，高 HRA 仍不等同于高任务成功率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四个模型在全部交互模式与领域上的总体能力

<div class="result-value" markdown="1">

总体成功率从 Qwen3.6-35B 的 $0.03$、Mistral-Large-3 的 $0.20$ 到 GPT5.4 的 $0.64$，说明最佳模型也未达到任务饱和。作者进一步将较弱模型的部分失败归因于持续探测而不提交，以及结构化回复解析失败。

</div>

结果表明模型并非完全不会从输入—输出证据归纳函数，但模型能力差异很大，而且最终成功受到规则归纳、协议遵循和停止决策共同影响。它不能单独证明失败全部来自溯因推理缺陷，因为解析错误也会直接消耗有效轮次或造成单轮失败。

<div class="result-source" markdown="1">

来源：第 5.1 节，Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The overall success rates range from 0.03 for Qwen3.6-35B, through 0.20 for Mistral-Large-3, to 0.64 for GPT5.4.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 一次性证据与多轮分发证据的比较

<div class="result-value" markdown="1">

对大多数模型及两类反馈，成功率通常按 single-turn、passive、active 的顺序下降，即证据一次性给出时最好，由 Game Master 分轮提供时次之，由模型主动选查询时最差。

</div>

这说明把相同类型的推理任务改成多轮过程会引入额外负担，包括维护当前假设、吸收后续反例和决定何时停止。该排序是“多数模型”的总体模式，并不意味着每个模型、领域和模式组合都严格服从这一顺序，也不能证明多轮交互本身必然有害。

<div class="result-source" markdown="1">

来源：第 5.1 节，Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For most models, across both feedback types, success rates follow the order single-turn, passive, and active, indicating that models perform better when evidence is provided upfront than when they must acquire it through interaction.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### GPT5.4 与 GPT5.4-mini 在 single-turn-output 和 passive-output 中的停止管理差异

<div class="result-value" markdown="1">

两者在 single-turn-output 中成功率相近，分别为 $0.82$ 和 $0.74$；转为允许模型控制证据积累与停止的 passive-output 后，GPT5.4 为 $0.78$，而 GPT5.4-mini 降至 $0.40$。

</div>

当证据一次性提供时，两模型差距较小；改成逐轮接收证据并自行决定何时提交后，小模型下降明显。这支持“交互管理能力存在模型差异”的解释，但比较同时改变了证据呈现时序和停止控制，因此不能把全部下降唯一归因于某一个因素。

<div class="result-source" markdown="1">

来源：第 5.2 节，Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GPT5.4 and GPT5.4-mini achieve similar success rates in single-turn-output, at 0.82 and 0.74, respectively, but differ in passive-output, at 0.78 and 0.40 (Figure 2).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 目标函数候选由 GPT5.4 生成，因此 GPT5.4 面对的是来自自身输出分布的函数；这使目标保持在 LLM 可表达范围内，但也可能使其与其他模型的比较受到生成分布匹配影响。实验只覆盖短小、纯函数、确定性 Python 变换，结论不应直接外推到开放世界诊断、自然科学发现或含噪声的真实溯因任务。
- 最终成功率同时受推理能力、响应格式遵循和提交行为影响。特别是 Qwen3.6-35B 与 Mistral-Large-3 的高解析错误率会压缩有效交互预算，因此低成功率不能完全解释为证据获取或假设修订不足；此外，每个领域仅有 10 个目标函数，领域级结果可能对个别函数较敏感。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- single-turn-output：一次性向模型提供输入及其正确输出，随后只允许一次 `SOLVE`。它是 output 反馈下的基准，用来判断多轮分发证据和模型自主停止是否带来额外困难。
- single-turn-verdict：一次性提供候选输入—输出对及其真假判定，随后只允许一次 `SOLVE`。它与 single-turn-output 的比较隔离了证据信息量：正确输出直接揭示函数映射，而真假反馈只排除或确认一个候选输出。
- passive-output：Game Master 在多轮中提供输入—正确输出样例。它与 active-output 具有相同的 output 反馈形式，但不要求模型选择查询，因此二者比较主要检验主动查询选择是否有效。
- passive-verdict：Game Master 在多轮中提供带真假标签的候选输入—输出对。它与 active-verdict 的比较用于检验在较弱的 membership/verdict 反馈下，自选查询是否改善证据获取与停止行为。

**实验想回答的问题**

- 大型语言模型能否根据隐藏 Python 函数的输入—输出证据，归纳出通过全部留出测试的函数规则；将证据一次性给出或分散到多轮交互，是否会改变成功率、证据利用和停止行为？
- 当查询由模型主动选择而非由 Game Master 提供时，模型能否选择足以区分竞争假设的输入，并根据新证据持续验证、修正假设，在合适时机提交答案？

**实验实现**

Alien Abduction 在 clembench 的 Game Master 循环中实现。交互模式最多允许 $T=15$ 轮，单轮模式仅允许一次 `SOLVE`；四个模型均通过各自 API、使用默认解码参数运行。系统逐轮记录动作、查询与反馈、当前假设、交互状态、查询理由、置信度和解析是否成功。提交的 Python 解答在一次性沙箱容器中执行，只将测试结果返回 Game Master。该协议既评估规则归纳，也把格式遵循、查询决策和停止决策纳入实际成功条件。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 主动查询选择：active-output 对比 passive-output | 两种模式都采用多轮 output 反馈，主要区别是查询由模型选择还是由 Game Master 提供。多数模型在 passive-output 中成功率更高，但所有模型在 active-output 中的最终 HRA 更高。 | 这一对照隔离了“谁选择输入样例”的影响。主动模式的高 HRA 说明模型生成的假设更能解释自己选择的证据；然而其较低成功率说明这些证据可能覆盖狭窄、区分力不足。换言之，模型可能在做确认性查询，而不是主动寻找能推翻当前假设的反例。 | 第 5.3 节，Figures 2、5<br><span class="experiment-evidence">At the final turn, hypothesis retrodiction accuracy (see Figure 5) is higher in active-output for all models, but this accuracy is measured against examples selected by the model and may therefore reflect consistency with its current hypothesis rather than the ability of those examples to distinguish it from competing hypotheses.</span> |
| 反馈信息量：single-turn-output 对比 single-turn-verdict | single-turn-output 的成功率高于 single-turn-verdict；前者直接显示给定输入的正确输出，后者只返回候选输入—输出对是否成立。 | 该比较检验反馈内容本身是否足以支持函数归纳。output 证据直接缩小可能函数集合，而 verdict 仅确认或排除一个猜测，因此需要更有效的候选构造和排除推理。原文未在所给章节中列出这一对照的逐模型完整数值。 | 第 5.1 节，Figure 2<br><span class="experiment-evidence">Between the two single-turn modes, the single-turn-output mode achieves higher success rates.</span> |

**定性案例**

- GPT5.4-mini 的失败中有 $7.56\%$ 属于“unclaimed wins”：模型已经产生正确假设，却继续查询直至预算耗尽，没有提交解答。结合 GPT5.4 在 active-verdict 中收到 `False` 后会改变后续查询和假设、但修订后仍不一定符合全部证据的观察，这一案例表明失败不仅来自无法发现规则，也来自无法判断当前假设何时已获得充分支持。证据位置：Figure 7 与第 6 节；原文图注为“7.56% of failed instances of GPT5.4-mini’s end with a correct hypothesis but no submitted solution.”

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces an interactive benchmark probing LLM abductive reasoning, active evidence acquisition, hypothesis revision, and stopping behavior.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`ab11feccb0d64b4d3e74ee246e77d142a1e37036e5998f94a79fd859126ac801`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
