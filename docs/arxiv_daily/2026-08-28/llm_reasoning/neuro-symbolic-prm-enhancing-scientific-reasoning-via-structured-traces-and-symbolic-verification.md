---
title: "[论文解读] Neuro-symbolic PRM: Enhancing Scientific Reasoning via Structured Traces and Symbolic Verification"
description: "[arXiv 2608.26329][LLM Reasoning] 本文针对定量 STEM 推理中“可执行但语义无依据”的中间步骤，将正确性拆分为符号有效性 $V$ 与语义扎根性 $G$，以确定性验证器负责前者、专用过程奖励模型负责后者。"
arxiv_id: "2608.26329"
announcement_date: "2026-08-28"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:40:59.607190+00:00"
source_sha256: "811d0ea34181ba45b5cf471c03fc48e60b25693a8cf3bd4d0f425b981099537e"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "LLM 其他"
  - "神经符号推理"
  - "过程奖励模型"
  - "符号验证"
  - "工具增强大语言模型"
  - "结构化推理轨迹"
  - "语义扎根性"
  - "定量 STEM 推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.26329</p>

# Neuro-symbolic PRM: Enhancing Scientific Reasoning via Structured Traces and Symbolic Verification

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Yuxin Zi, Cong Xu, Suparna Bhattacharya, Martin Foltin, Amit Sheth</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: AI Institute of South Carolina；Affiliation: Indian AI Research Organisation</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26329v1) · [PDF 下载](https://arxiv.org/pdf/2608.26329v1) · **关键词** 神经符号推理, 过程奖励模型, 符号验证, 工具增强大语言模型, 结构化推理轨迹, 语义扎根性, 定量 STEM 推理<br>


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

本文针对定量 STEM 推理中“可执行但语义无依据”的中间步骤，将正确性拆分为符号有效性 $V$ 与语义扎根性 $G$，以确定性验证器负责前者、专用过程奖励模型负责后者。

**不用术语来说**：给大模型配备计算器、代码解释器等工具后，它通常能把算式准确执行出来，但仍可能“算对了不该算的东西”：例如公式本身正确，却套用了错误变量，或者得到一个单位一致但与题目目标无关的量。此类步骤看起来规范、能够运行，也可能通过常规检查，因此会沿推理链继续传播并最终产生错误答案。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出神经符号过程奖励模型 NS-PRM，将步骤正确性明确分解为符号有效性 $V$ 和语义扎根性 $G$：确定性符号验证器以硬过滤保证其覆盖操作的语法、计算与执行一致性，PRM 则仅对通过验证的步骤判断其是否符合题意和解题逻辑。
- 提出反事实符号扰动 CSP，通过替换逻辑原理或交换类型匹配的变量，合成“约束仍满足、能够通过验证器、但语义错误”的困难负例；同时采用验证器优先的约束搜索，使训练时的负例分布与推理时验证器遗漏的残余错误相匹配。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究工具增强的大语言模型在定量科学、技术、工程与数学（STEM）多步推理中的可靠性。此类系统常用 Python 解释器或其他确定性工具执行计算，从而减少算术和语法错误，但“代码能够运行”并不等于“推理符合题意”：模型仍可能把正确公式用于错误变量，或计算一个数值、单位均合法但与解题目标无关的量。论文因此把步骤正确性区分为符号有效性 $V$ 与语义扎根性 $G$：前者关注表达式能否按既定规则解析、执行以及满足单位和操作数约束，后者关注该步骤是否与题目条件和当前解题路径在逻辑上相符。作者面向的核心场景不是完全形式化的定理证明，而是只能部分形式化的科学推理；确定性验证器负责可机器判定的部分，过程奖励模型则只判断剩余的上下文合理性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**工具增强推理**

大语言模型生成自然语言步骤或程序，再把精确计算交给 Python 解释器等外部工具。工具可以保证所给程序被正确执行，却无法保证模型选择的公式、变量或目标量符合题意。

</div>
<div class="concept-item" markdown="1">

**过程奖励模型（PRM）**

PRM 对推理轨迹中的单个步骤进行评分，而不是只根据最终答案判断整条解法。本文把它限制为软排序器，用于比较已通过符号验证的候选步骤是否在语义上合理。

</div>
<div class="concept-item" markdown="1">

**符号验证**

符号验证器依据明确规则检查结构、数学操作、单位及操作数使用等可判定约束，并以硬过滤方式拒绝矛盾步骤。它通常不能理解“为什么此处应使用这个公式”，因而不能独立判断完整的语义意图。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一道结构化定量 STEM 问题、此前已经生成的推理上下文，以及大语言模型提出的下一步候选；候选步骤采用可解析、可执行并可接受规则检查的结构化表示。系统需要输出一条多步解题轨迹及最终结果，同时满足两类要求：步骤具有符号有效性 $V$，并具有语义扎根性 $G$。论文假设验证器只能覆盖可形式化的操作；在其覆盖范围内，未通过结构、执行、单位或操作数约束的候选会被硬性删除，而通过者再由 PRM 按上下文适切性排序。因此，研究重点是识别“可执行但未扎根”的残余错误，而不是让神经模型重复学习确定性的算术与语法规则。作者还假定推理可以通过生成、解析、验证和失败后重试来逐步构造；这里的保证仅适用于验证器覆盖的操作，并不表示整个自然语言推理已被完全形式化证明。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$V$**

符号有效性（Symbolic Validity），表示步骤是否满足验证器可检查的结构、执行及相关符号约束。

</div>
<div class="notation-item" markdown="1">

**$G$**

语义扎根性（Semantic Groundedness），表示步骤是否与题目语境、变量含义和正确解题路径相符。

</div>

</div>

**直接相关的工作**

- **Program-of-Thoughts、PAL 与 ToRA**: 这些方法把计算交给 Python 等工具，或交替生成自然语言解释与可执行代码，主要解决算术和精确执行问题。本文指出，解释器会照常运行逻辑错误但语法合法的代码；其结构化推理表示进一步限制候选动作，并检查单位和操作数一致性，但仍需专门模型判断无法形式化的语义意图。
- **Lightman et al. (2024) 的过程监督与 Math-Shepherd**: 相关方法通过步骤级监督或由搜索轨迹推导标签来训练 PRM，通常让神经评分器综合判断步骤正确性。本文采用不同分工：确定性验证器先执行不可被神经高分覆盖的硬约束，PRM 仅在验证器接受的候选集合上评估语义扎根性，从而避免同时承担计算器、语法检查器和语义裁判三种角色。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

工具增强的大模型已能借助确定性计算引擎减少大量算术和语法错误，但在物理、数学等结构化定量任务中，高风险错误已转移到中间步骤的语义选择上。一个步骤即使语法合法、数值可执行且量纲一致，也可能采用了错误变量、错误原理或无关目标；这会削弱科学计算与教育场景对推理过程可审查性和可靠性的要求。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **外部工具与确定性符号验证**：代码解释器、Program-of-Thought 或领域符号引擎负责执行计算，并依据预定义规则检查语法、数学运算、类型或单位等形式约束，从而过滤不可执行或形式上错误的候选步骤。
- **整体式过程奖励模型（PRM）**：PRM 对推理链中的每个步骤给出正确性分数，通常用单一神经模型综合判断算术、格式、逻辑和上下文合理性，再据此筛选或排序候选推理路径。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 确定性验证器只能判断一个步骤是否满足其编码的形式规则，不能识别该公式或变量选择是否符合题目意图。因此，“数学上成立、单位也一致，但解决了错误问题”的步骤仍可能被接受并继续传播。
- 传统 PRM 同时承担计算器、语法检查器和语义裁判的职责，训练样本与模型容量会消耗在可由确定性规则解决的执行错误上；同时，常规训练数据未必充分覆盖那些能够绕过验证器的困难语义负例，导致模型对真正的推理时残余错误缺乏针对性。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有体系缺少一种边界清晰的分工机制：既对验证器覆盖范围内的执行正确性提供硬保证，又只在已通过形式检查的候选集合上学习语义判断；与此相伴，也缺少可系统生成“形式约束完全成立但逻辑意图错误”样本的训练方法，以直接覆盖工具增强模型最难处理的残余错误分布。

</div>
<div markdown="1"><span>核心问题</span>

能否把步骤级正确性分解为符号有效性 $V$ 与语义扎根性 $G$，用确定性验证器保证 $V$，再利用约束保持的困难负例训练专用 PRM 判断 $G$，从而在推理时更可靠且更高效地筛选科学推理步骤？

</div>
<div markdown="1"><span>作者直觉</span>

这一路径类似让“机器检查员”和“语义审稿人”各做擅长的工作：前者先廉价而严格地淘汰算不通、写不对或违反形式约束的步骤，后者不再浪费能力复核算术，只比较剩余步骤是否真正服务于题目。CSP 刻意制造能骗过机器检查员的错误步骤，相当于用最接近部署阶段盲点的反例训练语义审稿人；训练与推理都限定在验证器接受的候选分布上，也减少了两阶段职责错位。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把结构化定量 STEM 推理中的“正确”拆成两个条件：符号有效性 $V$ 要求步骤格式合法、运算可执行且数值与单位一致；语义扎根性 $G$ 要求所用公式、变量和物理或逻辑原理符合题目情境。模型先把自然语言题目转成由变量、操作和输出组成的结构化轨迹，再用确定性验证器把所有 $V=0$ 的候选作为硬错误删除；过程奖励模型（PRM）只在 $V=1$ 的候选中估计 $P(G=1\mid V=1,x,s_{<t},s_t)$。这样，验证器负责它能严格判定的计算与单位问题，PRM集中处理形式工具无法识别的“算得对但用错了”问题。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造机器可检查的题目状态与推理轨迹

将生成模型 $p_{\theta}$ 的输出限制在领域专用模式 $\Sigma$ 中；完整轨迹表示为 $J=(G_{\mathrm{ext}},S,a)$，其中每一步 $s_t=(\operatorname{op}_t,\mathbf{args}_t,\mathbf{\hat O}_t)$ 通过类型化指针引用题目变量或历史结果。该模式包含超过 120 个数学原语，并通过 JSON Schema 约束操作名称、参数类型及一个或多个输出。

<div class="method-step__io" markdown="1">

**输入**：自然语言问题 $x$，以及由轻量解析器抽取的已知变量集合 $G_{\mathrm{ext}}$。<br>
**输出**：可执行的结构化步骤序列 $S=(s_1,\ldots,s_T)$ 和支持多目标问题的最终答案集合 $a$。

</div>

**直观理解**：模型不是自由书写一段难以检查的推导，而是像调用一组受限 API：明确选择哪个公式、输入哪些已有变量、产生哪些带单位的新变量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 以符号验证器执行硬过滤

验证器 $\mathcal V$ 依次检查 JSON 模式与类型、重新执行 $\operatorname{op}_t$ 并比较预测值、再用 Pint 检查量纲与单位等价性；数值比较采用相对容差 $\epsilon=10^{-5}$。任何检查失败都会令 $\mathcal V(s_t)=0$，候选随即被删除。

<div class="method-step__io" markdown="1">

**输入**：候选步骤 $s_t$，以及它所引用的 $G_{\mathrm{ext}}$ 和历史步骤 $s_{<t}$。<br>
**输出**：仅包含语法合法、可执行、数值一致且单位一致步骤的验证器接受流形，即满足 $V=1$ 的候选集合。

</div>

**直观理解**：这相当于先让计算器和单位检查器复算每一步；它能排除算错、单位错和引用格式错，却无法判断题目本来是否应该使用这个公式或变量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 用 CSP 构造语义困难负例并训练 PRM

反事实符号扰动（CSP）生成满足 $V(s_t^{-})=1$ 但 $G(s_t^{-})=0$ 的负步骤：一类把正确操作替换成同领域但不适用于当前情境的公式，另一类把参数替换成单位和数据类型相同但语义角色不同的变量；确定性代数求解器随后重新计算全部输出，使负例仍能通过验证。PRM $\mathcal R_{\phi}$ 以正负步骤对训练，通过间隔排序损失使 $s^{+}$ 的分数至少比 $s^{-}$ 高 $\gamma$。

<div class="method-step__io" markdown="1">

**输入**：经 oracle 模型判定为正确且通过验证器的正步骤 $s_t^{+}$，以及可用上下文变量与同领域操作。<br>
**输出**：专门估计验证器已接受步骤之语义扎根性的 PRM，即对候选给出归一化的 $P(G=1)$ 分数。

</div>

**直观理解**：普通负例常因算术或格式错误而太容易识别；CSP故意制造“账算得完全正确，但公式或变量选错”的陷阱，迫使 PRM 学习题意而不是寻找表面错误。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 执行验证器优先的约束束搜索

先对全部候选运行 $\mathcal V$ 并删除 $V=0$ 的步骤，再仅对剩余步骤计算 $\log\mathcal R_{\phi}(s_{t,j}\mid J)$；搜索按累计 PRM 分数保留前 $B$ 条轨迹并重复，直至生成最终答案。若基础模型的符号错误率为 $\rho$，每个束扩展的预期神经评分量由 $k$ 次降为 $(1-\rho)k$ 次。

<div class="method-step__io" markdown="1">

**输入**：当前 $B$ 条活动轨迹、每条轨迹由 $p_{\theta}(\cdot\mid J)$ 采样的 $k$ 个下一步候选，以及训练后的 $\mathcal R_{\phi}$。<br>
**输出**：所有保留步骤均通过符号验证，并在这些步骤中由 PRM 优先选择语义上更符合问题情境的完整轨迹和答案。

</div>

**直观理解**：先用便宜而严格的规则筛掉明显不可执行的分支，再让昂贵的神经模型比较剩余分支是否“讲得通”；这既缩小搜索空间，也避免 PRM为算术检查浪费容量。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 单步符号有效性判定

$$
\mathcal{V}(s_t)=1\iff\texttt{TypeCheck}(\mathbf{args}_t)\wedge\left(\bigwedge_{m=1}^{M_t}\left(\frac{|v_{\mathrm{true},m}-\hat v_{t,m}|}{\max(|v_{\mathrm{true},m}|,\epsilon)}<\epsilon\wedge\operatorname{unit}(v_{\mathrm{true},m})\equiv\hat u_{t,m}\right)\right)
$$

**符号说明**

- $\mathcal{V}(s_t)$：确定性验证器对第 t 个候选步骤的二值判定。
- $\mathbf{args}_t$：步骤所引用的类型化输入参数。
- $M_t$：该步骤产生的输出变量数量。
- $v_{\mathrm{true},m}$：验证器重新执行操作得到的第 m 个真实数值。
- $\hat v_{t,m}$：生成模型声明的第 m 个输出数值。
- $\epsilon$：浮点数相对误差容限，文中设为 10^{-5}。
- $\hat u_{t,m}$：生成模型声明的第 m 个输出单位。
- $\operatorname{unit}(v_{\mathrm{true},m})\equiv\hat u_{t,m}$：重算结果的单位与声明单位在物理量纲及转换意义下等价。

<div class="equation-explanation" markdown="1">

**直观理解**：只有参数类型正确，并且每个输出的数值与复算结果足够接近、单位也等价时，步骤才被接受。合取符号要求多输出步骤中的所有结果同时通过，因此模型不能靠只报对其中一个结果绕过检查。<br>
**原文位置**：第 3.2 节，公式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### PRM 间隔排序目标

$$
\mathcal{L}_{\mathrm{PRM}}=\mathbb{E}_{(s^{+},s^{-})\sim\mathcal D}\left[\max\left(0,\gamma-\left(\mathcal R_{\phi}(s^{+})-\mathcal R_{\phi}(s^{-})\right)\right)\right]
$$

**符号说明**

- $\mathcal{L}_{\mathrm{PRM}}$：过程奖励模型需要最小化的期望排序损失。
- $\mathcal D$：由正确步骤和 CSP 困难负步骤组成的训练配对分布。
- $s^{+}$：符号有效且语义正确的正步骤。
- $s^{-}$：符号有效但语义错误的 CSP 负步骤。
- $\mathcal R_{\phi}$：参数为 phi 的 PRM 评分函数，用于估计语义扎根性。
- $\gamma$：要求正例分数领先负例分数的最小间隔。

<div class="equation-explanation" markdown="1">

**直观理解**：若正例得分比负例至少高出 $\gamma$，这一对样本的损失为零；否则损失与缺少的分数间隔成正比。由于正负步骤都已通过符号验证，优化信号主要来自公式选择、变量角色和上下文逻辑，而不是格式或算术差异。<br>
**原文位置**：第 3.3.2 节，公式 (2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标不是让一个模型同时学习计算验证和科学语义，而是在条件 $V=1$ 下学习正负步骤的相对次序。CSP首先控制负例分布，使 $s^{-}$ 与 $s^{+}$ 在格式、类型、数值执行和单位上都可验证，仅在语义上不同；随后最小化 $\mathcal L_{\mathrm{PRM}}$，推动 $\mathcal R_{\phi}(s^{+})-\mathcal R_{\phi}(s^{-})\geq\gamma$。分类头的 sigmoid 输出将分数限制在 $[0,1]$，既便于稳定使用间隔损失，也使推理时的 $\log\mathcal R_{\phi}$ 可解释为对语义可信度的对数评分。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 结构化推理语言与轨迹表示**

领域模式 $\Sigma$ 由超过 120 个数学原语构成，并由 JSON Schema 实现。已知状态写为 $G_{\mathrm{ext}}=\{(q_i,v_i,u_i)\}_{i=1}^{N_{\mathrm{ext}}}$；步骤输出写为 $\mathbf{\hat O}_t=\{(\hat q_{t,m},\hat v_{t,m},\hat u_{t,m})\}_{m=1}^{M_t}$，因此单步和最终答案都可产生多个带单位变量。

> 直观理解：统一的数据结构把变量身份、数值和单位绑定在一起，使系统能追踪每个数从哪里来，并支持向量分解、二次方程双根和多问答案等多输出情形。

**2. 确定性符号验证器**

验证器对操作参数执行类型检查，通过 $\text{exec}(\operatorname{op}_t,\mathbf{args}_t)$ 独立重算真实输出，并检查预测输出与重算值在容差内一致；Pint 后端负责单位转换和量纲等价，例如识别焦耳与 $\mathrm{kg}\cdot\mathrm{m}^2/\mathrm{s}^2$ 等价。它还检查引用完整性和单步全部输出，但只对模式覆盖的操作提供执行一致性保证。

> 直观理解：该模块给出的保证有明确边界：通过检查表示这一步确实按所声明的操作算对了，不表示该操作就是解题所需的科学原理。

**3. CSP 语义数据生成与过程奖励模型**

正例来自推理模型生成的结构化轨迹，并由 GPT-5.2 作为 oracle 进行步骤级判断；负例由 oracle 提议语义扰动、确定性求解器重算数值。$\mathcal R_{\phi}$ 初始化自 Qwen2.5-Math-7B，在步骤最终序列 token 的隐藏状态 $\mathbf h_t$ 上使用线性分类头，输出 $\sigma(\mathbf W^T\mathbf h_t+\mathbf b)\in[0,1]$。

> 直观理解：oracle只负责指出一个看似合理但语义错误的替换，精确数值由求解器计算，因此困难负例不会因为语言模型算错而泄露简单线索。论文还提出无需教师的扩展方向，包括程序化同构变量交换，以及从搜索轨迹中拒绝采样通过验证但最终错误的步骤。

**训练与推理**

训练阶段先用 Llama-3-8B-Instruct 从题目抽取 $G_{\mathrm{ext}}$，再收集推理模型生成的结构化轨迹，并由 GPT-5.2 oracle 给出步骤级正确性判断。对于验证正确的 $s_t^{+}$，CSP或替换同领域公式，或替换单位与类型相同的上下文变量；确定性求解器对扰动后的操作重新执行并填充输出，确保所得 $s_t^{-}$ 仍满足 $V=1$。这些配对用于微调以 Qwen2.5-Math-7B 初始化的 PRM。

推理阶段对每条活动束采样 $k$ 个结构化下一步，严格先运行验证器；不合格候选不进入 PRM。合格候选按步骤对数奖励累加并保留前 $B$ 条，循环至终止答案。该顺序把硬约束和软偏好分开：对验证器覆盖的操作可保证执行一致性，但完整科学正确性仍取决于结构化模式的覆盖范围、变量抽取质量、PRM判断和搜索是否找到正确路径。

**复现信息**

复现所需的关键设定包括：用 JSON Schema 实现包含超过 120 个数学原语的 $\Sigma$；验证器以 $\epsilon=10^{-5}$ 比较浮点输出，并用 Pint 执行量纲检查及单位转换；外部变量由 Llama-3-8B-Instruct 预抽取，原文报告该解析过程在验证中完整捕获初始状态的比例为 95.2%，因此实验实际上部分依赖预解析器质量。PRM以 Qwen2.5-Math-7B初始化，在最终序列 token 上接线性 sigmoid 分类头；训练语义标注与扰动提议使用 GPT-5.2。原文节选未明确给出 $B$、$k$、$\gamma$、训练轮数、学习率、批量大小、CSP两类负例比例及轨迹终止规则，复现时不能从该节选自行推定。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- PRM800K 用于抽取训练阶段的基础数学问题。作者从生成模型经预言机确认的正确轨迹构造 $140{,}000$ 个正步骤样本 $\mathcal{D}^{+}$，并用反事实符号扰动 CSP 构造 $140{,}000$ 个满足符号约束但语义错误的负步骤样本 $\mathcal{D}^{-}$；两类样本完全平衡。复杂科学适配另从 SciBench 物理和化学训练集抽取 $1{,}000$ 个数据点，构造各 $1{,}000$ 条正、负轨迹。
- ProcessBench 用于过程级元评估，测试模型能否在 GSM8K、MATH、OlympiadBench 和 OmniMATH 的推理链中区分错误步骤与正确步骤。四个子集从小学数学逐步覆盖到竞赛数学和多分支高级数学，因此可观察方法是否随推理难度上升而退化；原文节选未明确报告各测试集样本规模与具体划分。
- PRMBench 用于细粒度诊断 PRM，而非只测单一总体正确率。它从 Simplicity、Soundness 和 Sensitivity 等维度检查模型是否偏好简洁推理、能否抵抗虚构前提，以及能否察觉轻微数学或引用扰动。端到端搜索还覆盖 AIME、AMC、MATH、Olympiad、College Math、Minerva Math；科学域外评估使用 SciBench、GPQA 与 SuperGPQA，但原文节选未完整说明这些评估子集的规模。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**步骤分类 F1**

ProcessBench 同时报告错误类识别率、正确类识别率及其综合 F1；平均 F1 汇总四个数学子集，衡量模型能否兼顾发现错误与保留正确步骤，避免只偏向某一类别。 （越高越好，因为较高 F1 表示错误检测与正确步骤确认之间的综合平衡更佳。）

</div>
<div class="metric-item" markdown="1">

**PRMBench 维度平均分**

分别汇总 Simplicity、Soundness 和 Sensitivity 下的细分能力。Soundness 侧重抵抗虚构前提或不可靠推断，Sensitivity 侧重发现细微数学、引用或推理方向扰动；总平均分反映多类型过程错误上的整体稳健性。 （越高越好，因为分数提高表示模型在更多错误类型上作出符合基准标注的过程判断。）

</div>
<div class="metric-item" markdown="1">

**端到端 Accuracy**

在 PRM 引导的 Best-of-$8$ 搜索或不同束宽搜索中，最终答案正确的题目比例。它测试步骤评分改善能否真正帮助选择完整解答，而不只是提升局部分类表现。 （越高越好，因为它直接表示最终解题成功率更高；但必须结合候选数、束宽和 GFLOPs 才能公平解释。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### ProcessBench 四个数学子集的过程级错误识别

<div class="result-value" markdown="1">

完整 NS-PRM 在 GSM8K、MATH、OlympiadBench、OmniMATH 上的 F1 分别为 $83.0\pm0.5$、$77.5\pm0.6$、$68.9\pm1.0$ 和 $67.3\pm1.1$，平均 F1 为 $74.2\pm0.4$，且表中均以 $\dagger$ 标记显著改善。作为最强已列总体基线，Qwen2.5-Math-PRM-7B 的平均 F1 为 $73.5$；完整方法平均提高 $0.7$ 个百分点，而在更难的 OlympiadBench 和 OmniMATH 上分别高出该基线 $1.4$ 与 $1.0$ 个百分点。

</div>

这说明符号硬过滤与 CSP 神经评分的组合，在四类数学推理链上取得了最高的表列平均 F1，优势尤其没有在高难度集合上消失。作者据此主张验证器能稳定过程判断。分析上应注意：相对最强总体基线的平均优势并不大，显著性标记证明的是按作者重采样协议得到的统计差异，而不是对所有模型、生成器或未覆盖符号操作的普遍优势。

<div class="result-source" markdown="1">

来源：表 1，ProcessBench 结果

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

NS-PRM ($\mathcal{V}$ + CSP-PRM) 74.0 94.5 83.0 $\pm$ 0.5 $\dagger$ 68.3 89.5 77.5 $\pm$ 0.6 $\dagger$ 58.2 84.5 68.9 $\pm$ 1.0 $\dagger$ 56.8 82.5 67.3 $\pm$ 1.1 $\dagger$ 74.2 $\pm$ 0.4 $\dagger$

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### PRMBench 的细粒度稳健性诊断

<div class="result-value" markdown="1">

完整 NS-PRM 的 Simplicity、Soundness、Sensitivity 平均分分别为 $58.0\pm1.1$、$73.0\pm1.2$ 和 $77.3\pm0.9$。其总体表现中，Sensitivity 高于表列强基线 R-PRM-7B-DPO 的 $76.6$，但 Simplicity 低于 R-PRM-7B-SFT 的 $58.7$；因此优势主要体现在可靠性与扰动检测，而非所有维度都领先。

</div>

这一结果支持作者的核心分工假设：把执行有效性交给硬过滤器后，神经 PRM 更容易专注于语义混淆、虚构前提和推理方向等问题。不过，表中不同方法的各维度存在交叉胜负，所以不能把结果解释为完整 NS-PRM 在每个细分能力上均为最佳；它更准确地表明综合结构对 Soundness 和 Sensitivity 有帮助。

<div class="result-source" markdown="1">

来源：表 2，PRMBench 结果

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

NS-PRM (Verifier $\mathcal{V}$ + CSP-PRM) 52.5 63.5 58.0 $\pm$ 1.1 $\dagger$ 74.1 72.2 71.5 74.2 73.0 $\pm$ 1.2 $\dagger$ 63.5 70.1 98.4 77.3 $\pm$ 0.9 $\dagger$

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen2.5-7B-Instruct 上的 PRM 引导 Best-of-$8$ 端到端搜索

<div class="result-value" markdown="1">

完整 NS-PRM 在 AIME、AMC、MATH、Olympiad、College 和 Minerva 上的准确率分别为 $20.0\pm2.3$、$73.5\pm0.9$、$83.1\pm0.2$、$48.5\pm0.4$、$41.0\pm0.4$ 和 $43.2\pm0.5$，平均为 $51.5\pm0.3$。该平均值高于 R-PRM-7B-DPO 的 $49.4$ 和无验证器版本的 $47.8\pm0.4$，但仍低于候选集合的 pass@$8$ 上界 $61.4$。

</div>

局部步骤判别改进确实转化为了更高的最终答案准确率，说明提前删除必然无效的分支能让有限搜索预算更多地用于可行轨迹。它不证明模型已接近解决这些基准：pass@$8$ 与实际选择结果之间仍有明显差距，而且“上界”只表示八个采样答案中至少一个正确，并不是同等条件下可直接达到的系统性能。

<div class="result-source" markdown="1">

来源：表 3，PRM-guided Best-of-8 Search

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

NS-PRM (Verifier $\mathcal{V}$ + CSP-PRM) 20.0 $\pm$ 2.3 73.5 $\pm$ 0.9 83.1 $\pm$ 0.2 48.5 $\pm$ 0.4 41.0 $\pm$ 0.4 43.2 $\pm$ 0.5 51.5 $\pm$ 0.3

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 来源内部存在多处数值或配置不一致：ProcessBench 正文所述 OlympiadBench 与 OmniMATH 消融值不同于表 1；效率正文所述近似等预算束宽 $B=14$、$B=28$ 也不同于表 4 的 $B=11$、$B=22$。因此本文数值结论应优先依据表格，并在正式引用前核对 PDF、代码或勘误。
- 验证器只能保证其覆盖操作上的执行、算术与单位一致性，不能验证未编码的科学原则或开放式语义；科学实验又使用了 $1{,}000$ 个 SciBench 数据点进行领域适配。现有结果因而不能证明对任意科学领域、任意符号操作或完全零样本场景都有效，且节选未报告验证器覆盖率、拒绝率及误拒正确步骤的频率。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Qwen2.5-Math-PRM-7B 是最直接的同系列神经 PRM 基线：它与本文使用的 Qwen2.5 数学模型体系接近，但没有显式的验证器优先解耦，因而比较可检验增益是否来自神经—符号结构，而不只是基础模型能力。
- R-PRM-7B-SFT 与 R-PRM-7B-DPO 是面向扰动鲁棒性的强 PRM，分别采用监督微调和直接偏好优化。它们是有意义的比较对象，因为本文的 CSP 同样针对难负例，但进一步要求负例保持可执行性和符号约束。
- Math-Shepherd-7B 是通过蒙特卡洛树搜索自动生成步骤级标注的经典 PRM，用来代表依赖自动过程监督、但不显式拆分符号有效性与语义扎根性的路线。
- NS-PRM（CSP-PRM without $\mathcal{V}$）是内部对照：保留 CSP 训练得到的神经评分器，却关闭推理时硬验证器。它控制了训练数据与核心模型因素，因而最直接地隔离 $\mathcal{V}$ 的贡献。

**实验想回答的问题**

- 将确定性符号验证器 $\mathcal{V}$ 与仅评估语义扎根性的 CSP-PRM 解耦后，是否能比单体过程奖励模型更准确地识别数学推理链中的错误步骤，并在不同难度与不同错误类型上保持稳健？
- 在固定或近似相同的测试时计算预算下，先用 $\mathcal{V}$ 剪除不可执行、算术错误或单位不一致的候选，再进行神经评分，是否能减少无效前向传播，并将局部步骤判别优势转化为端到端数学与科学推理准确率？

**实验实现**

基础生成模型为 Qwen2.5-Math-7B-Instruct。PRM 使用 AdamW 微调 $2$ 个 epoch，学习率为 $2\times10^{-5}$、批量大小为 $128$，采用余弦学习率调度和 $0.05$ 的 warmup 比例，排序损失间隔 $\gamma=0.5$。验证器优先束搜索默认束宽 $B=8$，每次扩展采样 $k=4$ 个候选，温度为 $0.7$、top-p 为 $0.95$。ProcessBench 和 PRMBench 的显著性通过 $1{,}000$ 次配对 bootstrap 重采样检验，$p<0.05$ 记为显著；Best-of-$8$ 的 NS-PRM 结果来自 $5$ 个不同随机种子的随机推理运行。效率实验在相同的 $8\times$A100 80GB GPU 环境下按每题 GFLOPs 和相对墙钟时间计量，验证器在 CPU 上运行并设置 $50$ ms 超时。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 关闭确定性验证器 $\mathcal{V}$，比较 CSP-PRM 单独使用与完整 NS-PRM | 在 ProcessBench 上，加入 $\mathcal{V}$ 后平均 F1 从 $68.8\pm0.5$ 升至 $74.2\pm0.4$，提高 $5.4$ 个百分点；分数据集看，OlympiadBench 从 $62.6\pm1.2$ 升至 $68.9\pm1.0$，OmniMATH 从 $60.2\pm1.4$ 升至 $67.3\pm1.1$。这些数值以表 1 为准；正文另写成“62.1 to 69.8”和“60.2 to 68.5”，与表格不一致，需核对原始论文。 | 这是最关键的组件消融，因为两种设置都使用 CSP-PRM，主要变化是是否在神经评分前执行硬验证。提升表明训练时见过可执行但语义错误的难负例仍不足以保证结构正确性，推理时过滤具有独立贡献。不过，该对照同时改变了候选集合与后续排序输入，不能进一步区分收益究竟来自错误分支清除、搜索空间缩小，还是评分分布更稳定。 | 表 1，NS-PRM 无验证器消融；完整模型对照见同表下一行<br><span class="experiment-evidence">NS-PRM (CSP-PRM w/o $\mathcal{V}$) 68.5 92.1 78.6 $\pm$ 0.6 64.2 86.5 73.7 $\pm$ 0.7 51.3 80.2 62.6 $\pm$ 1.2 48.5 79.5 60.2 $\pm$ 1.4 68.8 $\pm$ 0.5</span> |
| 固定束宽与近似等计算预算下的验证器优先搜索 | 在 $B=8$ 时，单体 PRM 使用约 $450$ GFLOPs/题、相对墙钟 $1.00$ 倍，MATH 准确率为 $81.0\%$；完整 NS-PRM 使用约 $324$ GFLOPs/题、相对墙钟 $0.78$ 倍，准确率为 $82.6\%$。将节省的计算重新投入近似等预算搜索后，$B=11$ 的 NS-PRM 使用约 $446$ GFLOPs/题并达到 $83.8\%$。 | 固定束宽比较隔离了提前剪枝的直接效率收益；近似等计算比较则测试节省的神经计算能否换成更宽搜索并继续提高准确率。结果同时支持“更省”和“同预算更准”，但表 4 与紧随其后的正文存在束宽不一致：表中近似等预算为 $B=11$ 和 $B=22$，正文却声称约 $450$ GFLOPs 时可到 $B=14$，并举出 $B=16$ 到 $B=28$ 的例子，因此具体可扩展束宽需要源代码或修订版确认。 | 表 4，Test-time computational efficiency<br><span class="experiment-evidence">NS-PRM (Near-Iso-Compute) 11 0.99x $\sim$446 1.04x 83.8%</span> |

**定性案例**

- 附录 A 用“$2$ kg 物体以 $3$ m/s 运动，求动能”说明残余错误类型。正确步骤计算 $KE=\tfrac{1}{2}mv^2=9$ J；CSP 负例却计算动量 $mv=6$ kg·m/s。负例在算术、单位和可执行性上完全正确，因此 $V(s_t^-)=1$，但回答了错误的物理量，故语义扎根性为 $G(s_t^-)=0$。完整 NS-PRM 让验证器接纳其结构，再由 PRM 将正确动能步骤评分显著高于动量步骤。该案例直观展示模块分工，但属于构造示例，不能单独证明真实数据上的错误覆盖率。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：以符号验证器、过程奖励模型和受约束搜索联合提升LLM在定量科学任务中的多步推理可靠性。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`811d0ea34181ba45b5cf471c03fc48e60b25693a8cf3bd4d0f425b981099537e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
