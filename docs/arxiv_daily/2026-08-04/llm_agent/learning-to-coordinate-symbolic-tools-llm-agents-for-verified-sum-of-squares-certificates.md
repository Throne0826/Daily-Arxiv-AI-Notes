---
title: "[论文解读] Learning to Coordinate Symbolic Tools: LLM Agents for Verified Sum-of-Squares Certificates"
description: "[arXiv 2608.00326][LLM Agent] 本文研究能否通过代数能力后训练、精确符号工具和验证器反馈，使大语言模型学会协调多步符号操作，从而搜索可被机器严格验证的加权平方和证书。"
arxiv_id: "2608.00326"
announcement_date: "2026-08-04"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:02:50.828983+00:00"
source_sha256: "ad04b173933a99513ab3fd47638c2e48964b85843723a079b6ea88d85df2c700"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "LLM 其他"
  - "大语言模型智能体"
  - "符号工具调用"
  - "加权平方和"
  - "多项式非负性"
  - "机器可验证证书"
  - "SymPy"
  - "神经符号推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.00326</p>

# Learning to Coordinate Symbolic Tools: LLM Agents for Verified Sum-of-Squares Certificates

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Bohan Chen, Shivam N. Patel, Richard Hoffmann, Sam Looi, Tony Yue Yu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> California Institute of Technology</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.00326v1) · [PDF 下载](https://arxiv.org/pdf/2608.00326v1) · **关键词** 大语言模型智能体, 符号工具调用, 加权平方和, 多项式非负性, 机器可验证证书, SymPy, 神经符号推理<br>


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

本文研究能否通过代数能力后训练、精确符号工具和验证器反馈，使大语言模型学会协调多步符号操作，从而搜索可被机器严格验证的加权平方和证书。

**不用术语来说**：给定一个多项式，任务是把它改写成若干个多项式平方的正有理数加权和；一旦找到这种写法，只需展开并比较系数就能确认答案正确，但真正困难的是从许多可能的拆项、配方和因式分解路线中找到一条最终能够完整消去余项的路线。计算机代数工具可以准确完成某一步变换，却不会替模型判断下一步该做什么。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将加权平方和证书搜索构造成一个“搜索困难、验证廉价且精确”的符号工具协调测试环境，并用八类支撑性多项式任务训练模型所需的局部代数能力。
- 作者提出完整的代数后训练方案：先用直接代数题和模拟符号轨迹进行监督微调，再用任务特定的符号奖励进行验证器驱动优化，部署时允许模型调用原生 SymPy 工具，并对最终证书进行精确展开和逐项系数核验。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于数学推理智能体、符号计算与多项式非负性证明的交叉领域。研究对象不是让大语言模型独立完成所有代数运算，而是考察它能否在多步搜索中协调确定性的符号工具：模型选择操作、构造参数、解释工具返回结果并决定何时停止，SymPy 则精确执行展开、同类项收集、重排和因式分解。论文以加权平方和证书作为受控测试环境，因为候选证书可通过展开及逐项系数比较低成本、确定性地验证，但发现证书仍需从多种可能的配方和重组方式中搜索；因此，“局部运算正确”并不自动意味着“全局策略能得到有效证明”。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多项式非负性**

若实系数多项式$f$对其变量的所有实数取值都满足$f\ge 0$，则称其全局非负。证明这种性质通常不能只检查有限个代入点，而需要给出覆盖整个定义域的代数证书。

</div>
<div class="concept-item" markdown="1">

**加权平方和证书（weighted SOS certificate）**

它把目标多项式表示为$f=\sum_{j=1}^{m}c_jp_j^2$，其中每个权重$c_j$都是正有理数；由于平方项非负且权重为正，该恒等式直接推出$f\ge 0$。证书的正确性可通过精确展开右侧并比较左右两边每个单项式的系数来检查。

</div>
<div class="concept-item" markdown="1">

**符号工具调用**

语言模型不近似计算代数结果，而是调用SymPy等计算机代数系统执行指定变换，并根据返回的精确表达式继续推理。工具保证一次受支持操作的执行结果可靠，但操作选择、调用顺序、结果利用和搜索终止仍由智能体负责。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是由论文合成生成器构造的小规模多项式$f$；核心任务是在不采用数值修正的条件下，搜索并输出一个形如$f=\sum_{j=1}^{m}c_jp_j^2$的加权平方和分解，其中$p_j$为多项式、$c_j\in\mathbb{Q}_{>0}$。在核心加权SOS评测中，具备工具的系统可原生调用四类SymPy函数完成展开、收集、重排和因式分解；最终输出必须同时满足结构约束、正有理数权重约束以及精确系数恒等。该设置的关键难点不是验证，而是搜索：同一$f$可能存在多个分解，展开式会掩盖平方结构，混合项可按不同方式配方，而一次局部正确的变换也可能留下无法继续分解的余项。论文同时设置八个辅助多项式任务，用来训练局部代数操作和较广义的结构识别能力；加权SOS是第九个复合任务，也是唯一在评测时使用原生工具调用的任务。实验结论仅针对同一生成器分布下的合成多项式、单一基础模型及所比较的完整系统配置，不应直接理解为一般多项式不等式证明能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$f$**

待证明全局非负并需要构造加权平方和证书的输入多项式。

</div>
<div class="notation-item" markdown="1">

**$p_j$**

证书中的第$j$个多项式，其平方$p_j^2$构成一个非负分量。

</div>
<div class="notation-item" markdown="1">

**$c_j\in\mathbb{Q}_{>0}$**

第$j$个平方项的权重，要求属于正有理数，以保证该项非负并支持精确符号验证。

</div>
<div class="notation-item" markdown="1">

**$m$**

加权平方和分解所包含的平方项数量。

</div>

</div>

**直接相关的工作**

- **NSPI**: NSPI同样利用合成多项式与SOS数据、监督微调和课程式强化学习，但其模型先猜测近似SOS结构，随后依赖数值精化、有理数恢复和Lean验证。本文研究的是另一种边界：智能体按顺序协调精确符号变换，不使用数值修复，主要经验对象是工具协调而非通用或最先进的不等式证明。
- **ToRA**: ToRA训练模型在语言推理、计算程序与符号求解器之间形成交互轨迹，说明数学工具使用可以是迭代过程而非一次性计算。本文把这一思想收窄到确定性的多项式代数环境，并用最终系数恒等式直接验证智能体经过多步工具调用后得到的证书。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在自动数学推理中，仅让大语言模型调用计算工具并不能保证它能解决需要多步搜索的问题。以加权平方和为例，目标证书满足 $f=\sum_{j=1}^{m}c_jp_j^2$，其中每个权重 $c_j\in\mathbb{Q}_{>0}$；该恒等式能够证明多项式 $f$ 在全局非负，并可由机器精确核验。因此，这一任务既有明确的数学意义，也适合检验智能体能否把可靠的局部计算组织成正确的整体证明。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **直接工具调用**：语言模型根据当前状态选择展开、合并同类项、重排或因式分解等操作，将参数交给计算机代数系统执行，再读取精确结果并继续推理。工具保证被调用操作本身可靠，但操作的选择、顺序、结果解释和停止时机仍由模型决定。
- **面向复合任务的训练与输出验证**：模型直接学习从输入多项式生成完整的加权平方和表达式，并在终点通过展开和系数比较检查候选答案。该范式利用了答案可精确验证的优势，但若只围绕最终任务训练或奖励，就未必能系统补足配方、重排和处理余项等支撑性代数能力。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 精确符号工具只能执行模型已经提出的局部操作，不能决定全局搜索策略；即使每一步代数变换都正确，错误的拆项或配方顺序仍可能产生无法继续处理的余项，导致最终搜索失败。
- 加权平方和分解通常不唯一，展开形式又会掩盖潜在的平方结构；仅依赖最终答案训练或终点验证，反馈较稀疏，难以教会模型如何在多种合理候选中持续选择有利于完成整个证书的中间变换。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有能力之间缺少有效衔接：模型可能会做孤立的代数题，符号系统也能精确执行单次变换，验证器还能判断最终恒等式是否成立，但尚不清楚代数领域的后训练能否让模型把这些能力协调起来，在非唯一、需要回溯或调整策略的多步符号搜索中稳定地产生完整证书。

</div>
<div markdown="1"><span>核心问题</span>

论文要回答的核心问题是：代数基础上的后训练，能否使大语言模型在多步符号搜索中主动选择、组合和解释精确符号操作，而不只是机械执行彼此孤立的代数变换？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把“会算”“会用工具”和“知道最终是否正确”作为相互配合但彼此不同的能力来培养。支撑性代数任务先提供可复用的局部技能，监督微调示范这些技能如何形成过程，验证器驱动优化则让模型偏向真正通向正确证书的策略；部署时，SymPy 负责避免局部计算误差，模型集中处理更难的操作选择与全局规划。通俗地说，计算器负责把每一步算准，训练负责教模型何时按哪个键，而验证器负责确认整条解题路线最终确实成立。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文把加权平方和（weighted sum-of-squares, weighted-SOS）证明构造为“代数能力训练、顺序工具协调、精确验证”三部分组成的端到端系统。输入是有理系数多项式 $f\in\mathbb{Q}[x_1,\ldots,x_n]$；系统需要寻找正有理数权重 $c_j$ 和多项式 $p_j$，使 $f=\sum_j c_jp_j^2$。训练阶段先用九类合成任务进行监督微调（SFT），其中八类辅助任务教授排序、收集、展开、因式分解等局部操作以及 Horner 形式、对称约化、商余式和扩展 GCD 等结构能力，第九类任务教授完整的加权 SOS 搜索；随后以精确代数判定产生的奖励进行 GRPO 策略优化。推理阶段模型通过原生 SymPy 接口选择并执行展开、收集、重排和因式分解操作，再提交候选证书，由独立验证器按结构、权重符号和系数恒等式进行终局判定。

关键设计是把“局部计算是否正确”与“全局搜索是否成功”分开：SymPy 确定性地完成每次局部变换，但模型仍须决定应处理哪些项、采用什么表示、何时放弃无效分组、何时重试以及何时提交。换言之，工具相当于不会算错的代数计算器，却不会替模型选择证明路线；GRPO 则利用最终代数状态而非参考答案字符串评价不同路线，使多个形式不同但数学上等价的证书都能获得正向信号。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造多任务合成课程

每类任务生成 $150{,}000$ 个样本；加权 SOS 样本通过采样 $m\in\{1,\ldots,5\}$、基多项式 $q_j$ 和整数权重 $c_j\in\{1,\ldots,10\}$，计算并打乱 $f=\operatorname{expand}(\sum_{j=1}^{m}c_jq_j^2)$ 的展开式，同时隐藏原始分组。

<div class="method-step__io" markdown="1">

**输入**：一至三个已声明变量、随机生成的多项式参数，以及九类任务各自的生成规则。<br>
**输出**：验证划分前共 $1{,}350{,}000$ 个样本，划出 $5\%$ 后得到 $1{,}282{,}500$ 条训练记录；另用独立随机种子为每项任务生成 $10{,}000$ 个测试实例。

</div>

**直观理解**：生成器先从一个确定成立的平方和出发，再把它完全展开并打乱，因此系统看到的是“结果”，必须反向找回某个可验证的平方分组。训练集与测试集来自相同生成器族，所以该设计测量的是受控环境内的代数能力，而不是自然数学题或分布外泛化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 监督微调代数能力与模拟搜索轨迹

以 Phi-4-reasoning-plus 为骨干实施四比特 QLoRA；系统和用户 token 仅作为上下文并从损失中屏蔽，只对助手 token 计算交叉熵。SFT 数据不含原生函数调用消息或工具描述，因此学习的是代数变换及其上下文效果，而不是对部署接口的逐字模仿。

<div class="method-step__io" markdown="1">

**输入**：八类直接代数任务的题目—答案记录，以及包含 Python 风格符号操作、返回结果、重试和错误的模拟 SOS 轨迹。<br>
**输出**：一个具备局部代数操作、结构表示和初步 SOS 搜索行为的 SFT 检查点。

</div>

**直观理解**：这一阶段像先让学生大量练习代数基本功，并阅读带有计算结果的解题草稿。草稿看起来像工具使用过程，但模型尚未真正调用部署时的 SymPy 函数。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于精确符号奖励的 GRPO 优化

解析候选答案的规定包装格式，并依据各任务的精确数学契约计算奖励 $R_k(y)$；GRPO 在同一提示的多次生成之间进行相对策略更新，使产生更优代数状态的响应概率上升。奖励比较数学等价性、正规形式或证书残差，而非要求输出与单一参考字符串一致。

<div class="method-step__io" markdown="1">

**输入**：SFT 检查点、九类任务提示，以及每个提示采样得到的一组候选响应。<br>
**输出**：经过验证器约束的 Full 策略检查点，能够更倾向于产生格式有效且满足代数条件的答案与搜索行为。

</div>

**直观理解**：同一道题可能有多种正确分解和工具顺序，因此不能只奖励“像标准答案”。这里相当于让代数验算器直接批改结果，再用同题多个尝试的相对好坏调整模型。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 原生符号工具驱动的顺序证书搜索

在每个时刻，模型—执行框架系统可输出文本、带具体参数且符合模式约束的原生调用，或终局证书；合法调用由 SymPy 确定性执行展开、收集、重排或因式分解，并把观察 $o_t=T(a_t)$ 追加到上下文。系统据此选择分组、检查局部结构、修订不利分支并组装完整的加权平方和。

<div class="method-step__io" markdown="1">

**输入**：目标多项式 $f$、先前动作 $a_{<t}$、精确工具观察 $o_{<t}$，以及剩余调用和尝试预算 $b_t$。<br>
**输出**：一个候选终局对象，或在最多十次工具调用、三次分解尝试和单回合时间预算内以耗尽预算或放弃结束。

</div>

**直观理解**：计算工具只回答“这次展开或分解得到什么”，不会回答“下一步该处理哪一组项”。真正需要学习的是连续决策：先看什么、何时换路，以及证书何时已经完整。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 加权 SOS 生成与精确验收恒等式

$$
f=\operatorname{expand}\!\left(\sum_{j=1}^{m}c_jq_j^2\right),\qquad \operatorname{expand}\!\left(f-\sum_j c_jp_j^2\right)=0
$$

**符号说明**

- $f$：输入给模型并需要证明非负的目标多项式。
- $m$：生成样本时平方项的数量，取值属于一至五。
- $q_j$：数据生成器采样的第 $j$ 个隐藏基多项式。
- $p_j$：候选证书中由系统找到的第 $j$ 个多项式，不要求等于生成时的 $q_j$。
- $c_j$：第 $j$ 个平方项的权重；生成时为一至十的整数，验收时允许任意严格正的精确有理数。
- $\operatorname{expand}$：对多项式进行精确展开并合并同类项的符号运算。

<div class="equation-explanation" markdown="1">

**直观理解**：左式说明训练题如何从已知平方和反向生成：先构造必然成立的证书，再只展示打乱后的展开式。右式是最终验收标准；模型可以找到与隐藏分组完全不同的 $p_j$，只要所有权重合法且相减后的每个系数都精确为零，就得到对所有实数输入成立的非负性证明。<br>
**原文位置**：“Algebra-Grounded Post-Training—Synthetic curriculum”与“Verified Weighted-SOS Search—Acceptance contract”；验收式对应文中 Eq. (1) 所定义证书形式的精确检查。

</div>

</div>

<div class="equation-block" markdown="1">

#### 任务特定的验证器奖励

$$
R_k(y)=\begin{cases}-1,&E(y)=\bot,\\0.1I_{\mathrm{fmt}}(y)+0.9r_k(y),&\text{otherwise},\end{cases}
$$

**符号说明**

- $R_k(y)$：任务 $k$ 上候选响应 $y$ 的总奖励。
- $y$：模型采样生成的完整候选响应。
- $E(y)$：从响应中解析规定答案包装的函数。
- $\bot$：答案包装缺失或无法解析的标记。
- $I_{\mathrm{fmt}}(y)$：响应是否满足规定输出格式的指示量。
- $r_k(y)$：由任务 $k$ 的精确符号契约计算的分数，范围为 $[0,1]$。
- $k$：九类多项式任务之一的任务索引。

<div class="equation-explanation" markdown="1">

**直观理解**：没有规定答案外壳的响应直接得到 $-1$；可解析响应的主要奖励来自数学正确性，权重为 $0.9$，格式仅占 $0.1$。因此优化重点是候选所达到的代数状态，而不是与某条参考解答逐字一致，这对存在多种合法分解的 SOS 搜索尤其重要。<br>
**原文位置**：Eq. (2)，“Algebra-Grounded Post-Training—Verifier-grounded GRPO”。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：第一阶段 SFT 最小化助手 token 的自回归交叉熵，系统与用户 token 只提供条件上下文；这让模型学习九类任务的直接答案以及模拟符号轨迹中的操作模式。第二阶段从 SFT 检查点继续训练，以 $R_k(y)$ 为核心符号目标执行 GRPO：每个提示采样八个响应，在组内依据精确任务奖励进行相对策略优化，而不是用唯一参考轨迹进行行为克隆。其优化逻辑是，若两条响应表面形式不同但均满足代数契约，它们都可以得到高分；若某条轨迹包含正确但无助于完成证书的局部计算，则只有在到达更好的可验证状态或终局成功时才获得相应优势。

对 SOS 而言，奖励先由可解析的正有理数加权平方结构门控，再检查精确系数残差；部署时最终成功只由独立终局验证器决定。论文还使用偏好合法、可执行、不重复调用的轨迹塑形信号，但未对奖励分量做单独消融，因此现有证据只能支持“组合符号目标有效”，不能确认格式奖励、任务奖励或轨迹塑形各自的独立贡献。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 多任务代数课程与任务契约**

课程包含四个与工具对齐的局部任务：字典序项排序、按变量收集、展开和因式分解；还包含 Horner 形式、对称约化、商余式和扩展 GCD 四个结构任务，以及最终的加权 SOS 搜索。每项任务均用专门契约判定，例如商余式要求精确满足 $f=qg+r$ 且余式已约化，扩展 GCD 要求首一最大公因式及精确 Bézout 恒等式。

> 直观理解：局部任务训练模型执行小步代数操作，结构任务训练它选择更有用的表达形式；完整 SOS 任务再要求把这些能力串成一条证明路线。论文只把这种任务分组用于描述性分析，并未通过实验将某个辅助任务因果归因到某种搜索行为。

**2. 模型—工具执行框架**

环境暴露 $\operatorname{expand\_polynomial}$、$\operatorname{collect\_terms}$、$\operatorname{reorder\_polynomial}$ 和 $\operatorname{factorize\_polynomial}$ 四个原生函数。执行框架负责验证调用 JSON 和模式、管理预算、调用 SymPy 并回填精确观察；策略与执行框架共同形成有限时域顺序决策系统，其历史状态为 $h_t=(f,a_{<t},o_{<t},b_t)$。

> 直观理解：模型负责提出动作，执行框架负责保证动作格式有效并忠实运行，SymPy 负责具体计算。因而论文中的轨迹结论描述的是模型与执行框架的整体表现，不能把每次重组、重试或停止决定都单独归因于语言模型。

**3. 精确证书验证器与符号奖励**

终局验证器同时实施结构门控与系数恒等检查；训练奖励则按任务调用相应精确契约，并加入较小的格式分量。SOS 奖励要求候选具有正有理数加权平方结构，并根据精确系数残差判定；另有轨迹塑形项偏好合法、可执行且不重复的调用，并把最大增量留给终局验证。

> 直观理解：验证器既是最终裁判，也是强化学习信号的数学依据，因此模型不必复现唯一标准写法。论文评估的是合并后的奖励设计，没有消融格式、任务分数和轨迹塑形等单独分量，不能据此判断哪一部分最关键。

**训练与推理**

训练分两阶段。SFT 使用全部九类任务：八类辅助任务采用题目到直接代数答案的记录，SOS 采用带模拟 Python 风格操作及观察结果的多轮记录；这些数据不包含原生函数调用消息。随后，GRPO 从 SFT 模型初始化，对多任务提示生成候选响应，通过任务特定的精确符号契约和格式门控计算奖励并更新同一 LoRA 适配器。所有报告检查点共享 Phi-4-reasoning-plus 骨干，因而比较集中在后训练和部署协调方式，而不是模型规模差异。

推理时，八类辅助任务始终直接输出答案且不允许调用工具；只有 weighted-SOS 环境为 Base+Tools 和 Full 开放原生 SymPy 接口。每轮系统根据 $h_t=(f,a_{<t},o_{<t},b_t)$ 产生文本、函数调用或终局对象，执行框架检查调用、运行 SymPy 并把精确结果加入后续上下文。工具配置最多允许十次调用、三次分解尝试，每次调用限时五秒、每个回合限时六十秒；最终候选不按自然语言推理过程计分，只按结构和系数验证器计分。训练与部署接口存在刻意差异：SFT 教授模拟操作效果，部署才要求模型适应原生调用；论文没有隔离评估这一表示转换本身的贡献。

**复现信息**

数据方面，每项任务生成 $150{,}000$ 个实例，使用 $5\%$ 验证划分，最终训练记录为 $1{,}282{,}500$ 条；测试集由独立种子生成，但与训练集共享生成器族。该设置足以评估课程定义范围内的能力，却不能直接证明对真实竞赛不等式、不同生成机制或分布外多项式的泛化。所有测试 SOS 多项式都按构造保证存在 SOS 证书，但模型不知道这一点，因此耗尽预算或主动放弃只表示搜索失败，不能视为非 SOS 判定。

SFT 采用四比特 QLoRA，LoRA 秩为 $32$、缩放为 $16$、dropout 为 $0.05$，上下文上限为 $2{,}048$ token，学习率为 $5\times10^{-5}$，训练一轮；运行包含 $181{,}848$ 个打包序列、约 $3.72\times10^8$ token 和 $22{,}731$ 个优化步，使用一张 H100。GRPO 保持相同 LoRA 配置，提示与补全上限各为 $2{,}048$ token，全局提示批量为 $64$、每个提示八次生成、学习率为 $10^{-6}$，共 $20{,}039$ 个优化步，约用四张 80GB H100 训练 $55$ 小时；采样温度为 $0.9$、$\operatorname{top\text{-}p}=0.95$。公平解释结果时还需注意，原生工具调用只用于 SOS 部署，工具后端和终局验证器均是模型无关组件；更换骨干在软件上可行，但是否保持效果需要重新进行 SFT 与验证器驱动后训练，原文未提供跨骨干迁移证据。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 自建合成测试套件：九项任务各含独立生成的 $10{,}000$ 个测试实例，共 $90{,}000$ 个。其中八项支持任务包括项排序、同类项合并、展开、Horner 形式、对称约化、商与余数、扩展欧几里得算法和因式分解，用于评估不借助原生工具的检查点级代数能力；第九项加权 SOS 用于评估完整系统能否搜索到经精确验证的非负性证书。测试实例与训练数据由相同生成器产生但被留出，因此主要测量受控的同分布泛化，而非真实竞赛题或分布外泛化。
- AI-MO AIME validation set（AIME-90）：包含 AIME 2022 至 2024 年的全部 $90$ 道验证题。它作为次要保留性检查，考察专门化训练后模型的一般竞赛数学样本正确率是否出现明显下降，不用于证明广泛迁移能力。
- GSM-8K 测试集：使用全部 $1{,}319$ 道测试题，作为基础数学文字题上的次要保留性检查。该评测关闭工具，并与 AIME-90 一样只进行单次、每题 $16$ 个样本的检查。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**精确准确率**

用于八项支持任务；只有输出满足相应的直接精确判定规则才计为正确。它衡量检查点在无原生工具条件下执行多项式操作的能力。 （越高越好，因为更高数值表示更多测试实例得到精确正确的代数结果。）

</div>
<div class="metric-item" markdown="1">

**加权 SOS 验证成功率**

最终输出必须是结构合法的加权平方和表达式，并且精确展开后与目标多项式逐系数一致，才记为成功。该指标评估的是模型与工具执行环境共同达到的终态，而不只是工具调用语法是否合法。 （越高越好，因为只有验证器接受的输出才能作为机器可检查的多项式非负性证书。）

</div>
<div class="metric-item" markdown="1">

**$\mathrm{avg@16}$**

对每道 AIME-90 或 GSM-8K 题生成 $16$ 个样本，再对所有样本的正确性指示量取平均。它是平均单样本正确率，不是至少一次成功的 $\mathrm{pass@16}$，也不是多数投票准确率。 （越高越好，因为它表示随机生成的单个答案平均更可能正确；但它不直接反映多次采样后挑选最佳答案的能力。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 八项支持任务的无工具检查点评测

<div class="result-value" markdown="1">

Full 在八项任务上均为最优，宏平均准确率为 $93.35\%$；SFT 为 $78.08\%$，Base 为 $42.01\%$。相对 SFT，Full 的宏平均高 $15.27$ 个百分点；相对 Base 高 $51.34$ 个百分点。

</div>

由于三个检查点在这些任务上都不能调用原生工具，该结果直接说明专门训练后的检查点更擅长精确的多项式操作，而不能把提升归因于评测时由 SymPy 代做计算。Full 从 SFT 到 GRPO 之间仍有明显差距，但实验没有把训练样例类型、奖励项或训练随机性分别控制，因此不能确定具体是哪一种数据或奖励机制产生了提升。

<div class="result-source" markdown="1">

来源：Table 5；Results，Direct algebraic performance

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 5 shows that Full is strongest on every supporting task. Its eight-task macro-average is 93.35%, compared with 78.08% for SFT and 42.01% for Base.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 加权 SOS 的四种完整系统比较

<div class="result-value" markdown="1">

Full 的精确验证成功率达到 $78.96\%$，高于 SFT 的 $51.82\%$、Base+Tools 的 $44.73\%$ 和 Base 的 $7.63\%$。Full 比 SFT 高 $27.14$ 个百分点，比 Base+Tools 高 $34.23$ 个百分点；其 Wilson 95% 区间为 $[78.15\%,79.75\%]$。

</div>

完整系统在受控、同生成器的合成测试上最常找到可由验证器接受的证书。Base+Tools 明显优于 Base，说明工具访问有帮助；但 SFT 在没有原生工具时仍高于 Base+Tools，说明仅提供工具并不足以替代领域能力训练。需要严格区分的是，Full 相对 SFT 同时增加了 GRPO 后的检查点变化和原生工具，Full 相对 Base+Tools 又同时增加了 SFT/GRPO 训练，因此这些差值是完整系统差异，不是任何单一组件的净因果贡献。Wilson 区间也只反映 $10{,}000$ 个测试实例的有限样本误差。

<div class="result-source" markdown="1">

来源：Table 6；Results，Verified weighted-SOS performance

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Full reaches 78.96%, compared with 51.82% for SFT, 44.73% for Base+Tools, and 7.63% for Base. Relative to Base, SFT improves by 44.19 percentage points and Base+Tools by 37.10 points; Full is a further 27.14 points above SFT and 34.23 points above Base+Tools.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### AIME-90 与 GSM-8K 通用数学保留性检查

<div class="result-value" markdown="1">

在一次每题 $16$ 样本的评测中，Full 的 AIME-90 $\mathrm{avg@16}$ 为 $38.89\%$，高于 SFT 的 $34.44\%$ 和 Base 的 $16.67\%$；其 GSM-8K $\mathrm{avg@16}$ 为 $96.29\%$，高于 SFT 的 $93.71\%$ 和 Base 的 $91.58\%$。

</div>

这两组结果没有显示专门化训练造成明显的一般数学能力退化，至少在当前骨干、检查点和单次采样设置下如此。作者将其谨慎定位为保留性检查，而非迁移实验：没有其他骨干、重复训练运行、分布外符号推理基准或统计检验，所以不能据此声称 Full 普遍提升了数学推理能力。

<div class="result-source" markdown="1">

来源：Table 6；Results，General-mathematics retention checks

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under one 16-sample evaluation pass, Full has the highest mean sample accuracy on AIME-90 (38.89%) and GSM-8K (96.29%).

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

- Base：未经适配的 Phi-4-reasoning-plus，支持任务与加权 SOS 均不使用原生工具。它给出固定骨干模型的零专门训练起点，用于衡量后续领域训练或工具接入带来的系统差异。
- SFT：对 Phi-4-reasoning-plus 进行 QLoRA 监督微调，但评测时不开放原生工具。它与 Base 的差异主要对应监督训练后的检查点变化，也用于观察仅靠模型生成能否完成加权 SOS 搜索。
- Base+Tools：未适配的 Phi-4-reasoning-plus，但在加权 SOS 任务上获得与 Full 相同的原生 SymPy 接口和资源限制。它检验通用基础模型仅获得工具访问后能达到什么水平，是判断“工具本身是否足够”的关键对照。
- Full：SFT 后继续进行 GRPO，并在加权 SOS 评测中开放原生工具，是论文的完整系统。它与其他配置的比较回答完整训练与部署方案是否有效，但由于同时涉及检查点和工具条件变化，不能自动解释为单一组件的因果效应。

**实验想回答的问题**

- 在关闭原生工具的直接评测中，Base、SFT 与 Full 三个检查点在八类多项式支持任务上的代数能力有何差异，从而判断训练是否真正改善了模型内部的符号操作能力？
- 在加权平方和（weighted SOS）证书搜索中，Base、SFT、Base+Tools 与 Full 四种完整系统的精确验证成功率有何差异；同时，专门化训练是否在 AIME-90 和 GSM-8K 上表现出明显的通用数学能力损失？

**实验实现**

所有实验固定使用 Phi-4-reasoning-plus，以控制预训练来源与模型容量。可比配置共享测试实例、解码设置、答案解析器、精确验证器以及适用的时间和调用预算。八项支持任务及两项保留性检查对所有模型关闭原生工具；加权 SOS 中只有 Base+Tools 与 Full 可调用四个原生函数，并共享最多 $10$ 次工具调用、$3$ 次尝试、单次调用 $5$ 秒和单个 episode $60$ 秒的限制。加权 SOS 的终端验证通过精确展开和系数比较完成。

保留性检查中，每个检查点对每题生成 $16$ 个样本，温度为 $0.65$，$\mathrm{top}\text{-}p=0.95$，输出上限为 $2{,}048$ tokens，随机种子为 $1234$。论文还报告加权 SOS 成功率的 Wilson 95% 区间，但该区间只量化有限测试集下的二项抽样不确定性，不涵盖不同训练运行或不同检查点的波动。训练预算方面，SFT 使用一张 H100 训练一轮，共 $22{,}731$ 个优化步骤；GRPO 使用四张 80GB H100，完成 $20{,}039$ 个优化步骤，约耗时 $55$ 小时。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 工具使用与失败类型分析显示，经验证成功的 Full episode 平均调用原生工具 $3.8$ 次，低于 $10$ 次上限；失败终态可分为提前结束或拒答、输出并非合法加权 SOS、以及加权 SOS 形式正确但展开后多项式错误三类。这一分析说明瓶颈不只是调用次数，也包括搜索是否完成、证书结构是否合规以及代数恒等式是否真正成立。证据：“Successful Full episodes use 3.8 native calls on average, below the ten-call limit.”（Results，Verification separates search from proof；Appendix I，Tool-use summary）

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：核心贡献是训练可调用符号工具的 LLM Agent，并通过 SFT、GRPO 和精确验证器反馈求解数学证明任务。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`ad04b173933a99513ab3fd47638c2e48964b85843723a079b6ea88d85df2c700`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
