---
title: "[论文解读] Does Fault Localization Beat a Fresh Attempt? A Placebo-Controlled Study of Test-Guided Code Repair"
description: "[arXiv 2609.00854][LLM 评测] 本文通过“盲目重新生成完整解答—基于测试定位后的可疑代码片段补全—等长随机片段补全”三臂对照实验，检验测试导出的故障定位究竟提供了有效位置信息，还是修复收益仅来自小范围编辑或额外一次模型采样。"
arxiv_id: "2609.00854"
announcement_date: "2026-09-02"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:52:10.478937+00:00"
source_sha256: "c6a2622c4acce33fbcbb02dd10c17ee789312c5e013f02fbf2c58b08c03c622a"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2609.00854</p>

# Does Fault Localization Beat a Fresh Attempt? A Placebo-Controlled Study of Test-Guided Code Repair

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Anik Jha</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00854v1) · [PDF 下载](https://arxiv.org/pdf/2609.00854v1) · **关键词** LLM 评测<br>


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

本文通过“盲目重新生成完整解答—基于测试定位后的可疑代码片段补全—等长随机片段补全”三臂对照实验，检验测试导出的故障定位究竟提供了有效位置信息，还是修复收益仅来自小范围编辑或额外一次模型采样。

**不用术语来说**：当代码模型第一次生成的程序未通过测试时，可以让它根据失败测试只修改疑似出错的几行，也可以不看失败原因而重新生成一份完整程序。即使局部修改成功，也不能直接说明测试真的找准了错误位置：成功可能只是因为改动较小、较安全，或者只是因为模型获得了又一次尝试机会。本文要用严格对照把这几种解释分开。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出一个面向测试引导代码修复的双对照评估协议：用完整解答的盲目重采样控制“额外模型调用”的收益，并用不相交、等长度的随机代码片段补全控制“小范围编辑”本身的收益，从而单独识别测试导出位置是否有价值。
- 对失败候选程序进行可定位性审计，并预先设定跨模型家族的严格成功规则；研究重点不是提出新修复算法，而是判断基于公开测试的定位在实际可用性、尝试次数预算和生成令牌预算下是否值得采用。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于基于测试的自动程序修复与大语言模型代码修复交叉领域。给定一个未通过测试的代码候选，模型可以重新生成整个解，也可以依据失败测试推断故障位置，并只修改相应代码片段。论文关注的核心不是提出新的修复模型，而是用受控实验区分三种可能来源：测试定位是否确实提供了有用位置信息、较小编辑是否天然更容易成功，以及额外进行一次模型采样是否已经足以带来收益。为此，研究在冻结的代码模型上比较整段盲重采样、基于测试覆盖谱的故障定位后片段填补，以及不相关随机代码片段的安慰剂填补。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**基于测试的自动程序修复**

系统以未通过的程序和测试结果为输入，生成代码修改，使程序通过测试。测试提供的是可执行的错误证据，但通过测试不必然等于程序完全正确。

</div>
<div class="concept-item" markdown="1">

**频谱式故障定位（SBFL）**

SBFL根据不同测试执行时覆盖了哪些代码行，以及这些测试是否失败，为代码位置计算可疑度。本文使用 Ochiai 方法，并在多个位置并列最高时保留并列候选，而不是任意挑选一行。

</div>
<div class="concept-item" markdown="1">

**填空式生成（FIM）与安慰剂对照**

FIM先移除一个代码片段，再让模型根据缺口前后的上下文生成替代片段。随机跨度安慰剂在同样长度、但与定位跨度不相交的位置执行相同操作，用来检验收益是否来自正确位置，而不只是来自小范围编辑。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是同一批已经失败的代码候选及其公开测试执行结果。实验为每个候选设置三个处理臂：盲重采样直接重新生成完整程序；定位式填补先用公开测试的覆盖谱计算 Ochiai 可疑度，再对最高可疑度的连续代码跨度进行 FIM 替换；随机跨度填补则在不相交的随机代码位置进行同长度替换。输出是每个候选经过规定次数尝试后是否修复成功，以及相应的尝试成本、生成多样性和重复原跨度情况。研究假设测试派生的位置能够优于同大小的无关编辑，并且定位式编辑能够优于相同尝试次数的整段新采样；分析限定于文中测试的 $24$--$32$B 规模模型，因为更小模型的拼接程序存在严重解析失败，不能承担位置比较。公开测试未必包含失败用例，因此只有同时存在可用失败测试和覆盖谱的候选才可定位。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

初始失败的代码候选。

</div>
<div class="notation-item" markdown="1">

**$T$**

测试集合，包括测试执行结果以及代码覆盖信息。

</div>
<div class="notation-item" markdown="1">

**$s(x)$**

代码跨度或位置选择结果；在定位式处理下表示由 SBFL 选出的最高可疑度跨度，在随机安慰剂下表示同长度的不相交随机跨度。

</div>
<div class="notation-item" markdown="1">

**$\operatorname{Ochiai}(l)$**

代码位置 $l$ 的 Ochiai 可疑度，用覆盖该位置的失败测试与成功测试的数量计算；分数越高表示该位置与失败更相关。原文选用了该方法，但所给章节未完整列出其具体公式。

</div>

</div>

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在可验证编程任务中，测试能够证明程序行为有误，故障定位则试图指出应修改的位置。LLM使重新生成或局部改写代码都很容易，但这也造成决策难题：第一次生成失败后，有限推理预算究竟应投入到测试引导的局部修复，还是直接生成新的完整答案？此外，定位只有在公开测试中存在失败用例且能产生可用覆盖谱时才可执行，因此还必须先判断这种修复路径在真实失败样本中有多常见。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **反馈条件化自修复与完整程序重生成**：模型可读取测试失败或其他反馈后改写已有答案，也可忽略失败信息，重新采样一份完整程序。近期安慰剂对照研究表明，对冻结的小型代码模型而言，盲目重采样可能达到或超过反馈驱动的自修复，但这类研究没有专门判断测试导出的故障位置是否能使局部重试优于新生成。
- **故障定位与局部代码补全**：故障定位研究先确定疑似错误位置，再让模型只替换相应代码片段；已有工作常使用开发者补丁或其他预言机提供位置，或比较不同掩码位置的补全效果。本文关注的谱系故障定位依据测试覆盖情况为语句计算可疑度，再对最可疑的并列代码跨度执行中间填充。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 使用开发者补丁或预言机位置的研究证明的是“已知较准确位置时局部修复可能有效”，不能说明仅由公开失败测试预测出的实际位置同样可靠；若定位信号不可获得或不准确，这类结果就难以转化为真实修复策略。
- 既有比较没有同时匹配尝试次数并设置等长度随机位置对照，因此无法拆分两种混杂因素：第二次模型调用本身可能带来成功，而局部编辑无论位置是否正确都可能因改动较小而更容易保留原程序中的正确部分。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有证据尚未完成一个因果上可辨识的比较：对于同一个首次失败的候选程序，在相同尝试预算下，测试导出的预测位置是否比无关随机位置更有修复价值，以及采用该位置进行局部补全是否比直接重新生成完整解答更有效。缺少这两个对照，就不能把“位置选对了”与“小改动更安全”或“多采样一次”区分开。

</div>
<div markdown="1"><span>核心问题</span>

本文回答两个相互独立的问题：第一，在编辑长度相同的条件下，基于公开测试和谱系故障定位选出的可疑位置，是否优于一个不相交的随机代码位置；第二，在模型尝试次数相同的条件下，对该可疑位置进行局部补全，是否优于盲目重新采样完整解答。作者还将可定位性视为前置条件，以判断上述比较适用于多大比例的失败候选程序。

</div>
<div markdown="1"><span>作者直觉</span>

如果失败测试覆盖了错误语句而较少覆盖正确语句，谱系故障定位应把真正缺陷附近排到较高可疑度；模型只重写这一区域，理论上既能针对错误，又能保留其余已正确的代码。等长随机片段对照可以检验优势是否真的来自位置选择，完整重采样对照则检验保留旧程序并局部修改是否比获得一个全新候选更划算。作者因此预期局部定位补全应同时击败两种对照，但将该预期交由预先声明的严格实验规则检验。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该研究不是训练一个新的代码修复模型，而是设计一个受控的测试引导代码修复实验流程：先对失败候选程序运行测试并收集执行信息，再根据失败测试计算频谱式故障定位结果，最后分别执行盲目整题重采样、定位后局部填空和随机不相交局部填空。其核心控制变量是：三种处理都作用于同一个失败候选，局部填空使用相同长度的代码跨度，从而区分“故障位置确实有用”“局部修改本身更容易成功”和“再次调用模型即可成功”这几种解释。直观地说，研究者让模型分别进行一次完整重答、一次针对测试提示位置的局部修补，以及一次针对无关位置的局部修补，再比较修复结果；因此，局部方法的优势不能仅归因于修改范围较小。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 失败候选筛选与受控测试执行

在受监督的独立进程中运行每个测试，采用与参考解运行时间相关的超时规则，并设置地址空间限制；记录候选是否通过测试及各程序语句在测试执行中的覆盖情况。对于挂起或超出内存限制的候选，将其作为单个任务终止，避免阻塞共享进程池。

<div class="method-step__io" markdown="1">

**输入**：模型生成的候选程序、公共测试与更强的评测测试，以及候选程序的源代码。<br>
**输出**：失败候选集合、测试通过结果、每个测试对应的语句执行轨迹，以及可用于故障定位的失败测试信息。

</div>

**直观理解**：先把有问题的程序放进隔离的“测试盒子”里运行，既观察它错在哪些测试上，也记录每个测试走过哪些代码。隔离进程的作用是防止一个死循环或耗尽内存的程序拖垮整批实验。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于频谱的故障定位与跨度构造

根据失败与通过测试共同产生的覆盖信息计算语句的可疑度；若连续代码区域具有最高且集中的可疑度，则选取完整的连续最大分数范围作为定位跨度，若分数过于分散则拒绝该定位。对所有测试始终共同执行的直线语句不采用单行任意排序，而避免把没有区分力的覆盖信息误当成故障证据。

<div class="method-step__io" markdown="1">

**输入**：失败候选的测试执行轨迹，以及失败测试暴露出的语句覆盖频谱。<br>
**输出**：可用于局部修复的连续可疑代码跨度，或“不可定位”的候选标记。

</div>

**直观理解**：频谱定位类似于比较“出错测试经常经过哪些语句”与“正确测试经过哪些语句”：越偏向失败测试的语句越可疑。研究不强行给每个程序指定一个位置；如果证据太分散，就承认无法可靠定位。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 三臂受控修复生成

分别进行三种处理：盲目整题重采样，即不提供故障位置而重新生成完整解决方案；定位后填空，即移除可疑跨度并让模型生成替换内容；随机跨度安慰剂，即移除与可疑跨度不相交且具有相同代码行长度的随机代码跨度，再进行填空。随机采样器排除注释、文档字符串和空白区域，以确保安慰剂跨度具有实际改变执行的可能性。

<div class="method-step__io" markdown="1">

**输入**：同一个失败候选、原始测试上下文，以及可疑跨度或等长随机跨度。<br>
**输出**：三种处理各自生成的候选修复程序，以及每次生成所对应的处理条件和尝试次数。

</div>

**直观理解**：三组实验像医学试验中的治疗组和安慰剂组：完整重答检验“再问模型一次”是否足够，定位填空检验故障位置是否有帮助，随机填空则检验局部修改的优势是否只是来自修改较少。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成结果解析与公平评测

为不同模型的填空生成注册其实际分词器中的终止标记，截取替换片段并进行结构化拼接；对原始指令模型生成的额外演示代码采用结构性切分，避免把非替换内容拼入程序。检测生成截断，不能确认完整输出的样本不作为正常失败候选计分；最终对重建程序重新运行评测测试。

<div class="method-step__io" markdown="1">

**输入**：局部填空和完整重采样产生的模型文本、拼接所需的原始代码片段，以及测试执行环境。<br>
**输出**：可解析的修复候选、通过或失败标签，以及按处理条件汇总的修复率和尝试成本。

</div>

**直观理解**：模型有时会继续写超出填空位置的内容，或者输出没有闭合的代码块；如果直接把这些文本当成模型修复失败，会把格式问题误算成方法效果。因此，流程先确认输出确实是完整且可拼接的程序，再进行测试。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。所给章节描述的是冻结代码模型上的推理与评测实验，没有报告新的模型训练、参数更新或训练损失函数；模型只在不同提示和代码跨度条件下生成修复候选。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 受控的三臂实验设计**

实验以同一个失败候选为起点，比较盲目整题重采样、基于频谱定位的可疑跨度填空，以及等长且不相交随机跨度填空。局部处理在代码跨度长度上匹配，随机跨度同时排除注释、文档字符串和空白。

> 直观理解：该模块把“位置线索”“局部修改”和“再次调用模型”拆开测试，避免只看到局部方法成功就误以为成功一定来自故障定位。

**2. 频谱式连续跨度定位**

系统利用失败与通过测试的语句执行频谱确定可疑度，选择连续的最大高分范围，而不是在并列或完全相同的语句分数中任意选择单行；可疑度过于分散时放弃定位。

> 直观理解：它不是机械地指出一行代码，而是寻找一段由测试证据共同支持的连续区域；证据不足时不制造一个看似精确的位置。

**3. 健壮的代码生成与评测控制**

填空生成使用模型自身分词器提供的终止标记，并检测截断；候选程序在独立受监督进程中运行，采用基于参考解运行时间的超时和地址空间限制。结构化切分用于减少指令模型把演示代码或额外文本混入替换片段的风险。

> 直观理解：该模块保证比较的是修复策略，而不是超时、内存泄漏、输出过长或代码块解析错误等基础设施缺陷。

**训练与推理**

该方法属于纯推理流程。对每个失败候选，系统先运行测试并提取覆盖轨迹；若存在可用频谱，则构造连续可疑跨度，并分别生成定位填空与随机跨度填空结果，同时执行不使用定位信息的完整解决方案重采样；随后解析、拼接并重新测试所有候选。定位结论仅适用于实际获得可用频谱并成功构造定位跨度的候选，无法定位的样本不应被理解为定位方法失败后的局部修复结果。

**复现信息**

为保证可复现和公平解释，随机跨度必须与定位跨度具有相同代码行长度、与定位跨度不相交，并排除注释、文档字符串和空白。评测使用每个输入上“至少一秒，或参考解决方案运行时间四倍”中的较大值作为超时界限；每个评分任务运行在独立受监督进程中并受地址空间限制。填空生成必须注册实际分词器中的终止标记，并检测未闭合代码块造成的截断；原文还说明，结构化切分可降低指令模型输出额外演示代码导致的不可解析结果。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HumanEval+ v0.1.10：HumanEval 的函数级编程任务，提供原始测试与增强测试；参与三模型主分析，并用于 Mistral 的独立复现。原始测试构成部署情境下的 public signal，增强测试用于构成更强但不可部署的 strong signal。
- MBPP+ v0.2.0：MBPP 的函数级编程任务，提供原始测试与增强测试；作用与 HumanEval+ 相同，用于研究公开测试能否产生可用频谱以及强测试套件下的三臂比较。
- LiveCodeBench 函数调用子集：筛选任务日期为 2024-07-01 及之后的较新、较难任务；其任务是完整类而非单一函数，因此全量重采样的生成上限设为 1536 个新令牌。原文未明确报告该子集的独立任务总数。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**per-attempt success rate**

每次随机生成尝试通过该任务所有可用测试的比例；它保留了每个任务的 $K=16$ 次样本信息，而不是把结果压缩成一次成功或失败。 （越高越好，因为它表示单次修复尝试更可能产生通过全部测试的候选。）

</div>
<div class="metric-item" markdown="1">

**unlock@k**

在 $k$ 次样本中至少有一次通过全部可用测试的任务比例；文中每个实验臂使用 $K=16$ 次样本，因此该指标反映一个任务能否被解锁。 （越高越好，但它把多次样本压缩为一个二元结果，信息量低于逐次成功率。）

</div>
<div class="metric-item" markdown="1">

**task-clustered bootstrap difference**

以任务为重采样单位估计两臂逐次成功率差异及其置信区间；同一任务的 $16$ 次样本可能相关，因此不能把每次样本简单当作独立观测。 （若比较值为正，表示前者成功率高于后者；置信区间不跨零且经 Holm 校正后显著，才支持稳定的组间差异。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 定位信号的可用性：488 个失败候选，在 public signal 与 strong signal 下的定位覆盖

<div class="result-value" markdown="1">

公开测试仅使 44/488 个候选可定位，即 9.0%；增强测试将可定位数提高到 177/488，即 36.3%。公开测试下的主要瓶颈是所有公开测试都通过但隐藏测试失败，因而没有可计算的失败测试频谱；strong signal 下，主要瓶颈转为最高可疑度并列区间过于宽泛。可定位区间的文件占比中位数在公开信号下为 0.07、strong signal 下为 0.06。

</div>

这说明测试引导修复首先受“能否观察到失败信号”限制，而不只是受定位算法精度限制。部署系统通常只能看到公开测试，因此它只能作用于少数失败候选；strong signal 的 177 个候选是实验上界，不代表真实部署可获得的覆盖率。该结果也意味着进入后续三臂比较的候选不是全部失败样本，而是具有可用定位条件的筛选子集。

<div class="result-source" markdown="1">

来源：§4.1，Figure 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Public tests support localization for 44 of them (9.0%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### strong signal 下的定位填补与盲目整题重采样：177 个可定位候选、每臂 16 次尝试

<div class="result-value" markdown="1">

在匹配尝试次数的比较中，盲目整题重采样显著优于定位填补：盲目重采样的逐次成功率为 10.1%，定位填补为 4.4%，差异方向为定位填补相对盲目重采样低 5.7 个百分点；对应比较为 3:40，$p=3.0\times10^{-9}$，并且该结果在三个单独模型的主分析与次要分析中均得到校正后支持。跨模型家族的 Mistral 复现中，定位填补相对盲目重采样低 11.3 个百分点，95% 置信区间为 $[-16.6,-6.8]$。

</div>

定位并没有证明“利用失败位置”比完全重新开始更有效；在本实验的 24B--32B 模型范围内，重新生成完整解答反而更可能修复失败候选。该结果不等于所有模型或所有修复任务中定位都无效，因为分析仅覆盖具有 strong signal 的候选，并且作者明确将定位结论限制在被测试的 24B--32B 模型。它还不能单独区分定位错误、局部填补能力不足或局部修改造成的上下文约束等机制，但足以否定“定位填补必然胜过同预算的重新尝试”这一假设。

<div class="result-source" markdown="1">

来源：§4.2，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Against blind resampling at a matched number of attempts the ordering reverses, the margin is far larger (3:40, p = 3.0 × 10−9; 10.1% of blind attempts succeed against 4.4% of localized ones), and this is the one result that resolves within individual models under both analyses.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### strong signal 下的定位填补与随机片段安慰剂：位置效应检验

<div class="result-value" markdown="1">

汇总三模型时，定位填补的逐次成功率为 4.3%，随机片段安慰剂为 1.1%，差异为 $+3.2$ 个百分点，95% 置信区间为 $[+0.5,+6.2]$；不一致的任务解锁方向为 11:1，精确检验 $p=.006$，Holm 校正后 $p=.019$。然而按预先指定的逐模型主分析，三个模型均未达到校正后显著，最佳 Holm 校正后 $p=.087$；因此作者将位置效应报告为 suggestive，而非已确立的结论。

</div>

安慰剂比较表明，若只比较同样大小的局部编辑，编辑被测试信号指向的位置可能比随机位置更有用。但汇总结果把不同模型当作可交换重复样本，而预先方案拒绝据此作确认性结论；单模型结果未能稳定复现，因此不能说故障定位已经被严格证明有效。这个设计成功分离了“局部编辑本身的好处”和“编辑正确位置的好处”，但当前证据只支持后者的初步迹象。

<div class="result-source" markdown="1">

来源：§4.2，Table 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Only the pooled summary crosses the threshold: localized infilling unlocks tasks the placebo does not far more often than the reverse (11:1, exact p = .006, Holm-adjusted p = .019), at 4.3% of attempts against 1.1%, a difference of +3.2 points (95% CI [+0.5, +6.2]).

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

- 盲目整题重采样：从原始题目重新生成完整解答，不提供失败候选、覆盖率或测试结果；它检验第二次模型调用即使完全不利用失败信息是否已经足够有效。
- 定位填补：用 Ochiai 频谱定位最高可疑的连续代码片段，仅保持其前缀和后缀不变并重新生成该片段；它是待检验的测试引导修复方法。
- 随机片段安慰剂：在与定位片段行数相同、且与定位片段不重叠的可执行代码区间进行填补；它检验局部编辑的收益是否确实来自正确位置，而不只是来自编辑范围较小。
- 令牌成本重计价：不是新的修复算法，而是对盲目重采样与两种片段填补的敏感性比较；它检验在生成令牌而非尝试次数相同时，盲目重采样的结论是否仍成立。

**实验想回答的问题**

- 在失败候选中，测试引导的频谱定位实际上有多大可用性；公开测试与增强测试提供的定位信号分别能覆盖多少候选？
- 在尝试次数或生成令牌预算相当时，基于故障定位的局部填补是否优于盲目重新生成，以及相对于同长度随机代码片段填补是否存在可归因于位置的收益？

**实验实现**

研究先对每个模型和任务贪心生成一个初始候选；若候选未通过完整基准测试，则记为 dead candidate。只有当至少一个定位测试失败且执行测试能产生行覆盖率时，才允许进入三臂比较，因此三臂分析均条件于同一 localizable subset。公开信号仅使用 HumanEval+ 与 MBPP+ 的原始测试；strong signal 额外使用每个基础测试加最多 80 个增强测试，作为可用定位信号的上界而不是部署方法。对源代码行 $\ell$，使用 Ochiai 可疑度 $s(\ell)$，取所有达到最高分的连续行作为待编辑区间；若区间超过源文件行数的 60%，或不存在同长度的不相交可执行代码安慰剂区间，则排除该候选。三个主模型为 Qwen2.5-Coder-32B-Instruct-AWQ、Qwen3.6-27B 和 Gemma-4-26B-A4B-it，另以 Mistral-Small-3.2-24B-Instruct 在 HumanEval+ 与 MBPP+ 上作跨模型家族复现；主分析的三模型共覆盖 488 个失败候选，Mistral 的 62 个候选不并入该样本。所有模型权重冻结，不训练或适配。每个臂生成 $K=16$ 个随机样本，温度为 0.8、核采样概率为 0.95，并在相同候选上使用同一套运行框架。片段臂允许 256 个新令牌，整题重采样在 HumanEval+ 与 MBPP+ 上允许 512 个、在 LiveCodeBench 上允许 1536 个；比较同时按尝试次数和实际生成令牌数报告。主分析比较逐次成功率，使用以任务为聚类单位的配对 bootstrap，并在每个比较家族内对三个模型检验作 Holm 校正；任务解锁率则用双侧精确 McNemar/二项检验作为次要分析。评分要求通过所有可用测试，并采用输出精确相等，而不是 EvalPlus 的容差和顺序不敏感规则，因此绝对通过率不能直接与已发表的 EvalPlus 数字比较。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 原生 FIM 标记与 prompted pseudo-FIM 接口：两种 Qwen 模型、142 个配对候选 | 将同一批候选、定位区间和比较器从原生 FIM 标记改为聊天提示中的标记空洞后，Qwen2.5-Coder 相对盲目重采样的差值由 -7.1 个百分点变为 -4.9 个百分点，Holm $p$ 由 .011 变为 .072；Qwen3.6 的差值由 -9.1 变为 -9.6 个百分点，Holm $p$ 由 .015 变为 .041。prompted 路径的定位拼接解析失败率为 5.3%，原生路径为 2.5%；两者无操作率分别约为 49.7% 和原生同等水平。 | 该消融只改变“如何把空洞交给模型”的接口，不改变候选、定位片段、解码设置或盲目重采样比较器，因此可检验 FIM 接口是否造成定位填补的失败。接口确实会改变效应大小，尤其使 Qwen2.5-Coder 的差距不再达到校正显著，但没有在任一模型中反转定位填补相对盲目重采样的劣势，也不能解释 Gemma 的不同表现。由于模型家族与接口在原始实验中高度混杂，不能把非 Qwen 模型的差异直接归因于接口。 | Appendix F，Table 5<br><span class="experiment-evidence">The prompted path is not degenerate here, which is what makes the comparison usable at all: 5.3% of its localized splices fail to parse against 2.5% natively, far from the 65.5% that voided the capability probe, and its no-op rate (49.7%) is essentially the native one.</span> |
| 按生成令牌而非尝试次数重计价 | 片段尝试平均生成 21.7 个令牌，盲目整题重采样平均生成 371.1 个令牌；在令牌预算视角下，16 次定位尝试达到 6.8%，而一次盲目尝试已经达到 10.1%。原文未明确报告完整令牌匹配方案下每个模型的统计显著性。 | 这一分析检验了“盲目重采样只是因为每次生成更长、消耗更多计算”这一替代解释。虽然按令牌计价会缩小两种策略的资源差异，但并没有推翻盲目重采样的优势；同时，片段尝试的低令牌成本仍可能使其在实际系统中具有工程吸引力。它不能提供严格的计算成本公平性，因为作者同时指出尝试次数和令牌数是不同的资源货币，且没有系统记录墙钟时间。 | 摘要；§3.2 与 §4.2<br><span class="experiment-evidence">A span attempt spends 21.7 generated tokens against 371.1, yet 16 localized attempts reach 6.8% while one blind attempt already reaches 10.1%.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper conducts a controlled evaluation of test-guided fault localization and code-repair strategies for code-capable language models.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`c6a2622c4acce33fbcbb02dd10c17ee789312c5e013f02fbf2c58b08c03c622a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
