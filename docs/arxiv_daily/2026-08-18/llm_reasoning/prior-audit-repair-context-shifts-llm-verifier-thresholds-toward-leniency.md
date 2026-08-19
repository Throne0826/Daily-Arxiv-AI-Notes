---
title: "[论文解读] Prior Audit-Repair Context Shifts LLM Verifier Thresholds Toward Leniency"
description: "[arXiv 2608.16003][LLM Reasoning] 本文研究自动审查流水线中的上下文效应：即使当前待审任务完全不变，先让大语言模型经历一次针对其他样本的“审查后修复”，也可能使其随后充当验证器时更少报错，从而在没有可检测判别能力增益的情况下悄然改变决策阈值。"
arxiv_id: "2608.16003"
announcement_date: "2026-08-18"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:23:11.136628+00:00"
source_sha256: "9a24b9792cc9a5a7b8a6e71c9866b8f0d07554e02b1199e323310c05ae24c3ab"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "大语言模型验证器"
  - "审计→修复上下文"
  - "误报率"
  - "判准偏移"
  - "信号检测理论"
  - "ProcessBench"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.16003</p>

# Prior Audit-Repair Context Shifts LLM Verifier Thresholds Toward Leniency

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Parsa Mazaheri, Kasra Mazaheri</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of California, Santa Cruz；Affiliation: Massachusetts Institute of Technology</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.16003) · [PDF 下载](https://arxiv.org/pdf/2608.16003) · **关键词** 大语言模型验证器, 审计→修复上下文, 误报率, 判准偏移, 信号检测理论, ProcessBench<br>
**代码**: [https://github.com/parsa-mz/crtitxer](https://github.com/parsa-mz/crtitxer)

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

本文研究自动审查流水线中的上下文效应：即使当前待审任务完全不变，先让大语言模型经历一次针对其他样本的“审查后修复”，也可能使其随后充当验证器时更少报错，从而在没有可检测判别能力增益的情况下悄然改变决策阈值。

**不用术语来说**：实际系统常让模型先指出代码、证明或推理过程中的问题，再由模型修复这些问题；工程人员通常把这种流程编排视为不会影响审查标准的实现细节。然而，模型会读取此前的完整对话，因此先前的审查与修复经历可能改变它面对下一项任务时有多严格。这样一来，系统观察到的“误报减少”未必说明模型更会分辨对错，也可能只是模型变得更宽松；若只统计被标记样本的修复效果，还会把这种阈值变化误判为能力提升。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者通过保持当前问题文本、推理步骤、指令、输出格式和证据预算逐字节一致，并仅改变此前是否出现针对另一项目的完整“审查→修复”对话，隔离了流水线历史本身对验证器判断的影响；相对于等长填充上下文，该历史在所测的全部模型与措辞组合中均降低了正确推理轨迹上的误报。
- 作者进一步区分“判断极性漂移”与真正的判定标准变化：先前审查若报告了错误，后续验证器在可干净比较的条件下反而更加宽松，与简单的消息极性累积预测方向相反；论文据此将现象解释为缺乏可检测判别能力增益的决策标准偏移，并提醒实践者不要把特定运行点上的误报改善等同于验证能力增强。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于“大语言模型充当验证器（LLM verifier）”的研究场景：一个模型检查代码、证明或推理过程是否存在错误，随后由同一模型或另一模型修复被标记的内容。已有研究表明，模型判断会受对话历史、提示措辞、样例顺序和自我归因等上下文因素影响；本文进一步关注一种常见但容易被视为工程细节的因素，即当前检查之前的上下文中是否已经出现过一次针对其他样本的“审计→修复”完整交互。为避免把上下文效应与当前任务格式混在一起，论文要求各实验条件下当前问题文本、推理步骤、指令、输出格式和证据预算逐字节一致，只改变此前的对话经历。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**误报率（False-Alarm Rate, FAR）**

在人工确认正确的推理轨迹中，验证器仍报告存在错误的比例。本文用它衡量验证器是否过于严格，因为每次误报都可能触发一次不必要的修复。

</div>
<div class="concept-item" markdown="1">

**信号检测理论（Signal Detection Theory）**

一种将“识别能力”和“作答倾向”分开的分析框架：$d^{\prime}$刻画模型区分正确与错误样本的能力，判准$c$刻画模型更倾向于报告错误还是放行。因而，误报率下降既可能来自识别能力改善，也可能只是验证器变得宽松。

</div>
<div class="concept-item" markdown="1">

**上下文极性漂移（Polarity Drift）**

模型的当前判断向此前对话所表达的正面或负面结论偏移的现象。按照该解释，先前审计若报告错误，应使模型之后更容易报告错误；本文所述现象的方向与这一预测相反。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是自动化检查流水线中的语言模型验证器。当前输入为一个问题及其推理轨迹；论文重点测量人工已确认正确的 ProcessBench 轨迹，并辅以带标签的错误轨迹来判断模型是否真正提高了区分能力。模型输出是对轨迹是否含错的判断及实验规定的证据；核心自变量是当前任务之前的上下文类型，尤其比较已完成的“审计→修复”交互与长度匹配的填充上下文，而该先前交互讨论的是另一条样本。核心因变量是误报率，并结合错误轨迹上的检出率、$d^{\prime}$和判准$c$区分两种解释：前序修复经历究竟提高了验证能力，还是仅把报告错误的决策阈值推向宽松。研究假设当前任务在各条件下逐字节相同，因此观察到的差异不能归因于当前提示、输出模式或证据预算变化。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathrm{FAR}$**

误报率，即在人工标注为正确的轨迹中，模型错误报告存在问题的比例。

</div>
<div class="notation-item" markdown="1">

**$d^{\prime}$**

信号检测理论中的敏感度指标，用于表示验证器区分正确轨迹与错误轨迹的能力。

</div>
<div class="notation-item" markdown="1">

**$c$**

信号检测理论中的判准，表示验证器报告错误时采用的决策阈值或严格程度。

</div>

</div>

**直接相关的工作**

- **Temkit (2026)**: 该研究基于12个模型的84,088次调用，发现当前判断会向先前对话的极性漂移，并且负面历史引起的漂移更强。它据此预测“先前审计报告错误”应提高当前误报率；本文报告的方向相反，因此需要区别于一般极性累积的新解释。
- **Zhou et al. (2026)**: 该工作同样在 ProcessBench 上直接操控验证器的严格程度，证明严格性是一条可移动的行为轴。本文研究的缺口是：即使没有显式要求模型改变严格程度，普通的审计→修复流水线安排是否也会无意中移动这一判准。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型正被广泛用于审查代码、批改证明和核验推理轨迹，并常与后续修复模型串联，或在同一对话中自行修复其发现的问题。每次误报都会让本来正确的结果进入不必要的修复周期，而更隐蔽的风险是：流水线中的既往修复历史可能在系统没有显式调整标准时改变验证器的严格程度，使部署者无法稳定控制误报与漏报之间的权衡。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **同轮“解释并修复”提示**：已有研究在一次响应中同时要求模型审查、解释问题并给出修复，然后比较这种提示格式下的判断表现；相关结果表明，要求解释和修复可能增加模型对正确代码的误判。
- **自我归属或作品位置框架**：另一类研究考察监控模型是否会对被呈现为“自己的工作”的内容更宽松，通过改变作品在交互流程中的位置或归属表述来测量监控偏差；已有结果提示宽松效应主要随作品所处位置出现，而单独声明作品来自监控模型并不足以产生自我归属偏差。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 同轮要求审查与修复同时改变了输出任务和响应格式，因此无法判断误判变化究竟来自修复语境、额外生成要求，还是格式负担；其结论不能直接回答“先前已经完成的修复经历”是否会影响下一次独立审查。
- 自我归属研究把作品的位置、交互历史及归属线索交织在一起，难以隔离完整“审查→修复”上下文本身的作用；同时，既有两类结果对效应方向给出不同暗示，尚不能确定验证器会变严格、变宽松，还是获得了更好的辨别能力。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前缺少一个受控实验：当前待审任务及其全部指令保持逐字节相同，只改变上下文中是否已经存在一段关于其他样本的完整“审查→修复”交流，并以人类确认正确的样本测量误报。因而尚不清楚，流水线历史能否独立移动验证器的决策标准，以及观察到的误报变化是判别能力改善、简单的先前消息极性延续，还是无意产生的宽严阈值偏移。

</div>
<div markdown="1"><span>核心问题</span>

在当前任务完全相同的条件下，先前针对另一项目完成的“审查→修复”对话是否会系统性降低大语言模型验证器对正确答案的误报率；若会，这一变化究竟反映更强的正确与错误区分能力，还是仅反映验证器判定阈值向宽松方向移动？

</div>
<div markdown="1"><span>作者直觉</span>

语言模型并非把每个审查请求视为独立统计事件，而是依据整个上下文推断当前角色、任务阶段和适当的响应方式。此前已经完成一次“发现问题并修好”的互动，可能让模型把后续任务理解为修复流程之后的复核阶段，或让其形成更偏向接受现有结果的局部判断标准。因此，即便当前证据一字未变，模型也可能需要更强的错误证据才会再次报警；通过使用针对其他样本的既往对话和等长填充对照，可以把这种上下文诱发的标准变化从当前任务内容及输出格式影响中分离出来。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该研究不是训练新模型，而是对大语言模型作为数学解答审计器时的判定阈值进行受控行为实验。输入是带有逐步候选解的数学题，模型在固定的 JSON 输出约束下判断解答是否正确；研究者先生成并冻结一段“审计→修复”历史，再把它放入目标审计请求之前，比较不同上下文条件下的误报率，并在独立的错误解答集合上同时测量检出率。直观地说，研究者要判断：模型刚刚经历过一次修复后，是否会在下一次审计中变得更不愿意指出错误，以及这种变化究竟是判断能力改善还是单纯变得宽松。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造分离且匹配的数据臂

从 1,101 条符合条件的全正确轨迹中划分出 929 条目标、50 条用于生成历史片段的预热题和 122 条备用题；另取 929 条彼此不重叠、按来源组成匹配的错误轨迹作为信号臂，并为错误情形另取每个模型 50 条轨迹生成错误审计历史。全正确目标臂用于测量误报率，错误目标臂用于测量检出率。

<div class="method-step__io" markdown="1">

**输入**：ProcessBench 中带有逐步候选解的数学题，以及每一步均标记为正确或错误的标签。<br>
**输出**：干净目标集合、错误目标集合、历史片段生成集合和备用集合；各集合之间不共享题目，且正确臂与错误臂在 GSM8K、MATH、OlympiadBench 和 OmniMath 上按来源匹配。

</div>

**直观理解**：研究者把“本来正确的解答”和“确实错误的解答”分开，避免模型在生成历史时已经看过后来要审计的题目。前者回答模型会不会乱报错，后者回答模型还能不能找到真正的错误。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成固定格式的基础审计输出

分别在 Qwen3.6-27B、Qwen3.6-35B-A3B 和 Ministral-3-14B 上执行审计。模型通过受约束解码返回一个 JSON 对象，包含 verdict、first-error step、confidence、error type 和最多 40 个词的 evidence；主实验关闭推理轨迹，并在采样温度 $T=0.7$ 下对每个项目采样 8 次。

<div class="method-step__io" markdown="1">

**输入**：一条数学问题及其逐步候选解；每个实验条件还使用五种语义匹配的审计指令措辞 $F1$–$F5$。<br>
**输出**：每个项目、模型、措辞和上下文条件下的多次审计 JSON，以及由 verdict 汇总得到的正确或错误判定。

</div>

**直观理解**：输出格式像一张固定的审计表，确保不同条件比较的是同一种行为。使用多次随机采样而不是只看一次最可能答案，可以捕捉“更容易报错”这种概率上的小幅变化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成并注入先前审计—修复历史

模型先在 $T=0$ 下完成历史审计；随后根据审计结果请求修复，并冻结所得完整对话，使其在所有比较单元中逐字一致。历史被放置在目标请求前，并交叉操纵其说话角色和归属标签，形成 $2\times2$ 条件：AS（assistant、自身）、AO（assistant、标注的同行）、US（user、标注的自身）和 UO（user、同行）；无上下文基线 $R0$ 在同一目标子集上重新测量。

<div class="method-step__io" markdown="1">

**输入**：由同一个待测模型在独立历史题上生成的审计结果和修复结果，以及 465 条目标正确轨迹。<br>
**输出**：先前审计—修复 episode 的四个交叉条件及其平均效果；episode 只使用正确目标臂中按来源比例抽取的 465 条目标。

</div>

**直观理解**：这一步模拟“模型刚刚审计并修好另一份解答，现在继续审计新解答”。交叉改变历史是谁说的、被称作谁做的，是为了区分真正的经历内容与简单的角色或归属提示。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 加入控制条件并分解历史作用

构造 AF（长度匹配的非审计填充）、AV（只有审计、删除修复请求和修复）、AN（审计后仅要求原样重述结论）、AX（对真实错误轨迹进行审计并产生真实修复）及 AXN（错误审计后使用无效续接）。通过 episode−AF、AV−AF、AN−AF、AS−AN、AX−AXN 和 AXN−AN 等对比，分别检验上下文、审计内容、续接存在、修复内容以及错误判定的影响。

<div class="method-step__io" markdown="1">

**输入**：同一批目标和冻结历史，外加非审计对话、删去修复的对话、无效续接和错误审计历史。<br>
**输出**：一组具有明确控制含义的成对差异，而不是只依赖一个总的上下文与无上下文差异。

</div>

**直观理解**：每个控制都尽量只删掉或替换历史中的一个成分。例如，AS 与 AN 的差异近似回答“真正修复而不是继续说话”是否重要；AX 与 AXN 则回答修复真实错误是否带来额外影响。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未报告训练新模型、更新参数或优化损失函数；本研究的目标是测量既有模型在不同先前上下文下的推理与判定行为。因此不存在适用于本文方法的训练目标，实验阶段只进行条件化推理、采样和统计比较。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 冻结的审计—修复 episode**

历史片段由待测模型自身生成，生成温度为 $T=0$，随后在所有相关实验单元中保持字节级一致。主 episode 是 AS、AO、US 和 UO 四个 $2\times2$ 单元的均值；标签长度匹配，并检查去除标签后四个单元的文本完全一致。

> 直观理解：冻结历史可以减少一个重要混淆：不同条件不能因为历史内容本身不同而产生差异。四个单元的交叉设计还允许研究者检查“内容效应”是否其实只是角色效应。

**2. 分层控制体系**

AF 保留了先前交流的形式和长度但移除审计语义；AV、AN、AX 和 AXN 逐步控制续接存在、续接内容、错误 verdict 以及真实修复。特别是 AX−AXN 是唯一把两侧都限定为真实错误审计、只移除真实修复内容的对比。

> 直观理解：总效果可能来自很多原因，例如看到任何上下文、看到审计、看到“正确”这个词，或者看到修复动作。控制条件把这些可能性逐层拆开，使每个差异都有较明确的解释边界。

**3. 双臂信号检测评估**

正确臂的 929 条轨迹提供 FAR，错误臂的 929 条匹配轨迹提供 detection rate；两臂无共享项目，并分别按 episode 归类重采样后组合。判定标准 $c$ 描述模型偏向报告错误还是不报告错误，敏感性 $d^{\prime}$ 描述区分正确与错误轨迹的能力，balanced accuracy 是检出率与 $1-$FAR 的平均值。

> 直观理解：这相当于同时测试“误伤无辜”和“放过真正错误”。如果前者下降、后者几乎不变，模型更可能只是改变了报告门槛，而不是学会了更好的辨别。

**训练与推理**

研究者先进行预设的模型筛选：候选模型必须对明确的 framing 操作产生可观测的 FAR 反应，另外两个候选模型因未通过该 instrument-sensitivity screen 而未纳入主实验。正式实验中，三个模型分别接收数学题、逐步候选解和审计指令；在上下文条件中，目标请求前加入冻结的 episode 或对应控制文本，使用约束解码生成规定 JSON，推理轨迹主实验关闭，温度为 $T=0.7$，每题 8 次采样；生成历史 episode 时使用 $T=0$，以固定其内容。之后在正确和错误两类互不重叠的目标臂上分别计算 FAR 和 detection rate，并由两者得到 $d^{\prime}$、$c$ 和 balanced accuracy；所有区间采用 20,000 次、按 episode 聚类的 bootstrap，显著性按预先声明的 Holm–Bonferroni 家族校正判断。附加实验在 §7 重新打开推理轨迹，但所给材料未报告其完整操作流程和结果细节。

**复现信息**

复现实验至少需要保持以下设计不变：目标题、历史生成题和备用题必须互不重叠；正确臂和错误臂须独立，并按来源组成匹配；先前 episode 必须由对应模型自己生成、冻结且在各条件中逐字复用；AS、AO、US、UO 的文本在去掉归属标签后应完全相同，标签还要长度匹配；每个条件须覆盖五种语义匹配措辞 $F1$–$F5$。需要明确区分 episode 的四单元均值与单独的 AS 条件，区分“检测到错误”与“定位到错误步骤”，并注意不同对比的可识别性边界：例如 AS−AV 同时混合了修复存在与修复内容，AXN−AN 还混合了错误与正确历史所来自的不同题目池。原文未明确报告完整提示词、约束解码 schema 的形式化语法、随机种子、模型版本哈希、硬件、batch size 或发布复现实验代码的地址。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ProcessBench：用于验证器评估的基准数据集，包含带有逐步解答的数学问题及其正确性标签。实验重点使用人工验证为正确的解题轨迹，以测量模型错误报告问题的频率；论文摘录未明确报告完整数据集规模及官方训练、验证、测试划分。
- 正确轨迹目标子集：实验从 ProcessBench 的正确轨迹中抽取目标样本，并在上下文条件的源比例子集上重新测量无上下文基线。原文明确报告该子集包含 $929$ 个目标，其中 $465$ 个接受先验交互条件；其作用是保证不同上下文条件比较同一批目标。
- 先验交互 episode 池：针对留出的不同项目，由各被测模型在 $T=0$ 下生成并冻结审计—修复、审计—复述、仅审计及非审计填充交互。它不是独立性能数据集，而是用于构造上下文操纵和长度匹配控制的实验材料。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**误报率（$FAR$）**

在人工标注为正确的解题轨迹上，模型报告存在错误的比例；它直接衡量验证器把正确内容送入不必要修复流程的频率。 （在本实验的正确轨迹目标上越低越好，但单独降低 $FAR$ 不能证明总体验证质量提高，因为模型也可能漏掉真正错误。）

</div>
<div class="metric-item" markdown="1">

**判别指数（$d'$）**

信号检测理论中的判别能力指标，用于衡量模型区分正确与错误轨迹的能力，尽量与整体判定阈值区分开。 （越高越好；若 $FAR$ 下降而 $d'$ 不变，更支持“阈值变得宽松”而不是“辨别能力提高”的解释。）

</div>
<div class="metric-item" markdown="1">

**判定准则或阈值（criterion）**

模型把内部证据转化为“报告错误”或“不报告错误”的决策门槛。实验通过跨条件估计其移动来判断模型是否改变了严格程度。 （不存在脱离任务目标的单调优劣；在正确轨迹上降低阈值式误报可能有益，但阈值过度宽松会增加漏报。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 先验完整审计—修复 episode 与长度匹配非审计填充 AF 的比较，覆盖 $3$ 个模型、$5$ 种措辞及其 $15$ 个模型×措辞组合。

<div class="result-value" markdown="1">

加入先验审计—修复上下文后，$15/15$ 个组合的 $FAR$ 都低于 AF；下降幅度为 $2.8$ 至 $11.5$ 个百分点，相对 AF 降低 $9\%$ 至 $25\%$。这说明先验交互会使验证器报告错误的决策更少。

</div>

作者将该结果解释为稳定的宽松化效应，而不是提示词格式变化，因为当前待审计任务在条件间保持字节级相同，且 AF 控制了先前对话的存在和长度。该结果本身只证明正确轨迹上的误报减少，不证明模型在所有错误类型上都更可靠；需要结合 $d'$ 和阈值分析判断是否只是降低严格程度。

<div class="result-source" markdown="1">

来源：Abstract；Introduction §1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Measuring false alarms on human-verified-correct ProcessBench traces with the present task held byte-identical, we find that a completed audit → repair episode already in the model’s context lowers false alarms in 15 of 15 model × wording combinations, by 2.8 to 11.5 pp against a length-matched non-audit control, a 9 to 25% reduction relative to that control.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 信号检测分析：比较先验上下文前后的判定准则与判别能力。

<div class="result-value" markdown="1">

先验 episode 导致判定准则在 $15/15$ 个组合中移动，并在多重比较校正后保留 $13$ 个；$d'$ 在校正后没有保留显著变化。作者据此把主要变化定位为阈值移动，而非可检测的判别能力提升。

</div>

直观上，模型并没有明显变得更会区分正确和错误解答，而是降低了“必须有多强证据才报告错误”的门槛，因此在正确轨迹上少报错。作者同时提醒 $d'$ 检验按构造只有约一半的敏感度，所以“未检测到 $d'$ 变化”不能等同于证明判别能力绝对不变。

<div class="result-source" markdown="1">

来源：Abstract；Introduction §1；Experiments §6（摘录未提供完整表号）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The criterion moves in 15 of 15 combinations and survives correction in 13 while d′ survives in none, though the d′ test is half as sensitive by construction.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 对误报样本进行人工复核，检验降低误报是否在当前运行点具有实际收益。

<div class="result-value" markdown="1">

作者人工检查了 $50$ 个被模型标记为错误的样本，其中 $82\%$ 被判断为确实错误的误报；因此，在该运行点，降低 $FAR$ 的阈值移动未必有害。

</div>

该分析回答的是“模型少报的错误中，有多少原本就是不应报告的”，而不是重新估计整个验证器的准确率。由于复核由一名作者完成且没有报告标注者一致性，$82\%$ 应视为支持性证据，不能当作无偏的总体质量估计。

<div class="result-source" markdown="1">

来源：Abstract；Introduction §1；Appendix F

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A hand audit of 50 false alarms finds 82% simply wrong, so at this operating point the shift need not be harmful.

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

- R0（无先验上下文）：只提供当前待审计任务，是判断先验交互是否产生影响的基线。
- AF（长度匹配的非审计填充）：在相同对话角色和近似相同长度下，加入不涉及正确性、错误、审查或修复的任务，用于区分“任何先前对话”与“先前审计—修复内容”。
- AN（审计加惰性延续）：保留审计及第二个助手回合，但把修复替换为对审计结论的原样复述，用于隔离“修复行为”相对于一般延续的作用。
- 2×2 角色—归属条件 AS、AO、US、UO：分别交叉助手/用户消息位置与自我/同行标签，用于检验效果究竟由消息位置、归属表述，还是交互内容驱动；四者平均值被称为 episode 条件。

**实验想回答的问题**

- 在目标任务、提示词和输出格式完全相同的情况下，把一个已完成的审计—修复交互放入模型上下文，是否会改变模型对正确解题轨迹的误报率（$FAR$）？
- 误报率变化来自判别能力（$d'$）变化，还是来自判定阈值（criterion）移动？审计结论、修复内容、交互角色和上下文位置分别发挥什么作用？

**实验实现**

实验测试 Qwen3.6-27B、Qwen3.6-35B-A3B 和 Ministral-3-14B；另有两个候选模型因预筛选未通过而未作为主实验模型。每个目标在 $T=0.7$ 下采样 $8$ 次，使用约束 JSON 解码；先验 episode 在 $T=0$ 下生成并冻结。每个条件使用五种语义匹配的审计措辞（F1–F5），当前任务的题目、步骤、指令、输出模式和证据预算在条件间保持字节级一致。主操纵是在目标请求前加入留出项目的先验交互；对比时采用同一目标和冻结 episode，并使用长度匹配的 AF 控制。论文还报告了按模型、对比和项目聚类的区间估计及多重比较校正，但摘录未明确给出所有具体区间、显著性数值或完整表格。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| episode 内容分解：AS（审计+修复）与 AV（仅审计）、AN（审计+复述）比较，并加入 AX（基于错误轨迹的审计—修复）控制。 | 作者报告修复内容和审计结论在不同模型族上呈互补作用；AS−AN 用于识别修复相对于一般第二回合的作用，AX 用于处理正确轨迹与错误轨迹 episode 结构不对称。摘录未明确报告这些对比的完整数值。 | 这个消融不是只问“有没有上下文”，而是问上下文中的哪一部分在起作用。AS 与 AN 的差异较能隔离修复行为；AS 与 AV 还混入了长度和是否存在后续回合的差异，因此不能单独作为强因果证据。AX 检验效应是否只是因为先验 episode 中模型面对的是正确还是错误对象。 | Abstract；Experiments §5；Appendix 控制条件说明<br><span class="experiment-evidence">Decomposing the episode finds repair content and audit verdict complementary: different components carry the effect on different model families.</span> |
| 消息位置与归属的 $2\times2$ 交叉消融：AS、AO、US、UO。 | 两个 Qwen 模型的四个条件彼此相差不超过 $0.63$ 和 $0.72$ 个百分点；Ministral 的四个条件跨度为 $5.65$ 个百分点，显示该模型存在位置效应。作者最终将四个条件的平均值作为 episode 对比。 | 该消融区分“内容本身”与“内容出现在用户消息还是助手消息、被说成自己的还是同行的”。Qwen 上条件接近，说明其主效应不依赖单一角色或归属标签；Ministral 的差异则表明模型间可能存在不同的消息位置敏感性，因此跨模型合并解释需要谨慎。 | Experiments §3.3<br><span class="experiment-evidence">The 2 × 2 was close to flat on the two Qwen models (all four cells within 0.63 and 0.72 pp of each other) but not on Ministral, whose cells span 5.65 pp because that is the one model with a placement effect.</span> |

**定性案例**

- 附录 F 对 R0 条件下的 $50$ 个误报进行人工分类：四类为 wrong、defensible、unclear 和 label_error；样本按该条件全部 $390$ 个误报的错误类型比例抽取，具体样本数为 arithmetic $12$、logical $20$、algebraic $9$、misread $7$、unjustified $2$。该案例的作用是说明较低 $FAR$ 可能确实减少了错误警报，但由于只由一名作者复核且无跨标注者一致性，结论仍需独立复核。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work studies how preceding audit-and-repair context changes an LLM verifier's acceptance threshold, directly concerning reasoning verification and judge reliability.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`9a24b9792cc9a5a7b8a6e71c9866b8f0d07554e02b1199e323310c05ae24c3ab`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
