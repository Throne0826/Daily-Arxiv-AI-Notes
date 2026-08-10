---
title: "[论文解读] Fisher-R1: Training LLM Agents for Reliable Hypothesis Testing"
description: "[arXiv 2608.07437][LLM Agent] 原文未明确报告。"
arxiv_id: "2608.07437"
announcement_date: "2026-08-10"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-10T02:39:32.622223+00:00"
source_sha256: "064c24da0ac5c6c34573c95a2288186dda172cd319c55fac7165e92685f24f50"
tags:
  - "LLM Agent"
  - "强化学习"
  - "LLM Reasoning"
  - "LLM 其他"
  - "假设检验"
  - "大语言模型智能体"
  - "统计推断"
  - "$p$值"
  - "开放式数据分析"
  - "P-Bench"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.07437</p>

# Fisher-R1: Training LLM Agents for Reliable Hypothesis Testing

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-10</span>
<span><strong>作者</strong> Jiacheng Miao, Jin Mu, Guanhua Chen, James Zou</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Department of Biomedical Data Science, Stanford University；Department of Genetics, Stanford University；Department of Biostatistics and Medical Informatics, University of Wisconsin–Madison；Department of Statistics, University of Wisconsin–Madison；Department of Electrical Engineering, Stanford University；Department of Computer Science, Stanford University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.07437v1) · [PDF 下载](https://arxiv.org/pdf/2608.07437v1) · **关键词** 假设检验, 大语言模型智能体, 统计推断, $p$值, 开放式数据分析, P-Bench<br>


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

经验科学中的假设检验用于把科学问题转化为可由数据支持或反驳的统计结论：研究者针对零假设与备择假设选择合适的检验，基于数据计算$p$值，再按预先约定的显著性标准作出拒绝或未拒绝零假设的判断。本文关注能读数据、写代码并执行分析的LLM智能体；其关键能力不只是让程序成功运行，而是在数据分布、异常值和变量关系等条件下选对推断方法，使方法、计算出的$p$值与最终结论在统计上连贯。论文以医学、生物学和经济学的开放式任务为应用场景，强调错误的方法选择即使产生精确且可复现的数值，也可能导致错误的科学发现。（来源：摘要；第1节 Introduction）

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**假设检验**

它是在给定数据下评估某项科学主张是否有足够证据的统计决策过程，通常比较零假设与备择假设。流程包括确定问题、选择检验、计算证据量并形成结论；检验方法必须与数据和研究问题相匹配。（来源：第1节 Introduction）

</div>
<div class="concept-item" markdown="1">

**$p$值**

$p$值是特定统计检验基于数据给出的证据量，用于辅助判断零假设是否应被拒绝。它的有效性依赖于所选检验及其数据假设；因此数值计算正确不等于统计推断正确。（来源：摘要；第1节 Introduction）

</div>
<div class="concept-item" markdown="1">

**秩相关检验与异常值**

异常值或高杠杆点可能让依赖线性关系的分析得出由少数样本驱动的显著结果。本文以Spearman秩检验为例：它利用观测值的排序衡量关联，在所举情形下避免了线性回归对异常点的误导。（来源：第1节 Introduction，Figure 1）

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

每个任务向智能体提供一项科学假设、一个数据集及数据说明；智能体需要自主检查数据、选定统计方法、编写并执行分析代码、报告$p$值，并据此给出是否拒绝零假设的结论。本文的问题设定是开放式的：题目不直接指定检验方法，因而系统必须同时处理方法选择、可执行计算和结论一致性。评估所需的参考答案由规范分析的已记录执行生成，并经领域专家审计；论文特别检查所选方法、该方法实际执行得到的$p$值、以及拒绝或未拒绝决定之间是否一致。（来源：第1节 Introduction；Appendix A Additional Related Works）

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$p$**

由所选统计检验和数据计算得到的$p$值；本文将其作为评估推断正确性的重要对象。（来源：摘要；第1节 Introduction）

</div>
<div class="notation-item" markdown="1">

**$z$**

附录中用于比较$p$值的$z$分数量表尺度；原文说明奖励会在该尺度上比较$p$值，但给定节选未提供其具体转换公式。（来源：Appendix A Additional Related Works）

</div>

</div>

**直接相关的工作**

- **通用数据分析智能体基准：InfiAgent-DABench、DABStep、DA、以及Zhu等人的相关工作**: 这些工作评估智能体的数据分析能力，常奖励看似合理的答案或可执行工作流；本文认为它们通常不单独核验推断方法是否恰当、报告的$p$值是否来自该方法的实际执行、以及结论是否由该证据推出，因此无法充分覆盖“代码正确但统计推断错误”的失效模式。（来源：第1节 Introduction；原文引文："they rarely isolate the inferential method itself: which test was executed, whether the reported p-value is grounded in that execution, and whether the conclusion follows from the computed evidence."）
- **面向可验证结果的强化学习：DeepSeekMath、DeepSeek-R1、DAPO**: 这些方法表明可通过结果可验证的奖励训练推理或工具使用行为，但其正确性对象主要是数学、编程或SQL任务的最终答案。本文将差异定位为奖励目标：Fisher-R1需要评价推断有效性，即在所选方法、计算证据与拒绝或未拒绝决定之间保持一致，并在$z$分数量表上比较$p$值。（来源：Appendix A Additional Related Works；原文引文："Whereas these systems reward correctness of a final answer in math, coding, or SQL, Fisher-R1’s reward must score inferential validity"）

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Fisher-R1将开放式假设检验建模为可执行的多轮智能体任务：输入为科学问题$q$、数据集$D$和数据说明$s$，模型在R环境中检查数据、选择统计方法、编写并执行R代码，最后输出$p$值$\hat{p}$及在预设显著性水平下的拒绝/不拒绝原假设决定$\hat{\delta}$。训练不直接使用P-Bench真实任务，而是从可执行的合成数据生成过程构造带隐藏答案键的任务；先用高质量教师轨迹进行监督微调，再以结果可验证的奖励进行强化学习。直观地说，系统不是让模型背诵“什么检验适合什么场景”，而是反复训练它像分析人员一样读取数据、运行分析，并因最终$p$值和结论是否接近标准分析而获得反馈。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 合成任务与答案键构建

对每个格点实例化经作者检查的模拟脚本，生成CSV数据并用规范统计方法运行分析；记录该次模拟数据上的$p$值、在$\alpha=0.05$下的决定及方法标签为隐藏答案键。另渲染仅含研究问题的non-hint提示或指出聚类、删失、内生性等设计特征的hint提示，并加入缺失值或异常值扰动变体。

<div class="method-step__io" markdown="1">

**输入**：统计方法$M$、领域情境$S_m$、样本量$N$、效应量$E$、提示风格$P$和随机种子$K$组成的任务格点。<br>
**输出**：由研究说明、分析请求、数据集和隐藏答案键构成的合成任务包；完整语料为8,642个任务。

</div>

**直观理解**：每道练习题都能自动生成，也有“标准解答”。标准答案不是数据生成时设定的真实效应，而是规范方法实际分析这份具体随机数据后会得到的结果，因此训练目标与真实分析工作一致。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 教师轨迹收集与监督微调

教师按固定五步完成基础EDA、详细EDA、针对候选方法的假设检验、方法选择和结论；仅保留多轮轨迹有效、终结答案可解析、结论与答案键一致，且报告$p$值在$\alpha=0.05$意义上吻合并处于同一数量级的样本。随后以ReAct/CodeAct格式对助手token做掩码自回归负对数似然训练。

<div class="method-step__io" markdown="1">

**输入**：随机抽取的合成任务，以及Claude-Sonnet-4.6生成的多轮分析轨迹。<br>
**输出**：SFT初始化策略及3,851条过滤后的教师轨迹。

</div>

**直观理解**：先让模型模仿经过筛选的完整分析过程，而不是只模仿最后一句答案。这给强化学习提供一个能使用工具、会写代码的起点，减少其从随机试错开始学习的难度。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### R环境多轮强化学习采样

针对每个提示，从旧策略$\pi_{\theta_{\mathrm{old}}}$采样$G=8$条多轮轨迹；每条轨迹可交替产生思考、R代码、中间决定和最终答案，环境返回数据摘要、警告、模型输出、诊断、统计量和$p$值。对同一提示内的回报做标准化，并丢弃所有回报相同的轨迹组后重新采样。

<div class="method-step__io" markdown="1">

**输入**：SFT初始化后的策略$\pi_\theta$、一个任务提示，以及可执行R环境。<br>
**输出**：具有非退化相对优势的代码执行轨迹组及其奖励。

</div>

**直观理解**：模型会尝试多种分析路径，而不是一次作答。只有同一题中确实出现好坏差异的多条尝试才用于更新，模型才有明确的比较信号可学习。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 结果导向策略优化与部署推断

奖励先要求轨迹同时含推理、可执行代码和可解析的终结答案；通过后，以$z$尺度上的$p$值接近度为主奖励，并以结论是否匹配为辅奖励。使用DAPO的裁剪策略目标更新参数；推断时，模型对新任务在同一R环境中执行多轮分析，并从最终轨迹解析$\hat{p}$和$\hat{\delta}$。

<div class="method-step__io" markdown="1">

**输入**：轨迹的格式有效性、报告$p$值、最终结论及隐藏答案键。<br>
**输出**：经RL优化的Fisher-R1，以及可与答案键比较的最终$p$值和假设检验决定。

</div>

**直观理解**：训练主要惩罚“数值看似合理但统计推断错误”的答案，而不强制唯一的方法名称。因为同一数据问题有时存在多种可辩护的方法，作者用最终$p$值是否接近规范分析来间接评价方法选择。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### DAPO组相对优势与策略目标

$$
\hat{A}_{i}=\frac{R(o_{i})-\mu_{q}}{\sigma_{q}+\epsilon},\qquad\mu_{q}=\frac{1}{G}\sum_{j=1}^{G}R(o_{j}),\qquad\sigma_{q}^{2}=\frac{1}{G}\sum_{j=1}^{G}(R(o_{j})-\mu_{q})^{2}.\n\nJ_{\mathrm{DAPO}}(\theta)=\mathbb{E}_{q,\{o_{i}\}}\left[\frac{1}{\sum_{i=1}^{G}T_{i}}\sum_{i=1}^{G}\sum_{t=1}^{T_{i}}\min\left(r_{i,t}(\theta)\hat{A}_{i},\,\operatorname{clip}\left(r_{i,t}(\theta),1-\epsilon_{\ell},1+\epsilon_{h}\right)\hat{A}_{i}\right)\right],\qquad r_{i,t}(\theta)=\frac{\pi_{\theta}(y_{i,t}\mid h_{i,t})}{\pi_{\theta_{\mathrm{old}}}(y_{i,t}\mid h_{i,t})}.
$$

**符号说明**

- $o_i$：对提示$q$采样得到的第$i$条多轮轨迹。
- $R(o_i)$：轨迹$o_i$的Fisher标量奖励。
- $G$：同一提示下采样的轨迹数量。
- $\hat{A}_i$：第$i$条轨迹相对同组平均回报的标准化优势。
- $\mu_q,\sigma_q$：提示$q$的轨迹组奖励均值和标准差。
- $\epsilon$：优势标准化分母中的数值稳定常数。
- $\pi_\theta,\pi_{\theta_{\mathrm{old}}}$：当前策略和生成该批轨迹的旧策略。
- $y_{i,t}$：轨迹$o_i$中第$t$个被纳入策略梯度的助手token。
- $h_{i,t}$：生成$y_{i,t}$前的完整交互历史，含提示、先前token和环境观测。
- $r_{i,t}(\theta)$：当前与旧策略对该token赋予概率的比值。
- $T_i$：轨迹$o_i$中纳入策略梯度损失的助手token数。
- $\epsilon_\ell,\epsilon_h$：DAPO的下、上不对称裁剪阈值。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分只在同一问题的多条尝试之间比较优劣，消除不同题目固有难度造成的回报尺度差异。第二部分提高高奖励轨迹token的概率、降低低奖励轨迹token的概率，同时用裁剪限制单次更新幅度；作者设置$\epsilon_\ell=0.20$、$\epsilon_h=0.28$，以允许正向轨迹有稍大的更新空间。<br>
**原文位置**：第4.3节“Algorithm”，式(4)、式(5)、式(6)

</div>

</div>

<div class="equation-block" markdown="1">

#### Fisher奖励函数

$$
R(o)=I_{\mathrm{valid}}(o)\left(w_{p}r_{p}(o)+w_{c}r_{c}(o)\right),\qquad w_{p}+w_{c}=1.\n\nz(p)=\Phi^{-1}(1-p/2),\qquad r_{p}(o)=\exp\!\left(-\frac{|\min\{z(\hat{p}),5\}-\min\{z(p^{{}^{*}}),5\}|}{\sigma}\right),\quad\sigma=1.
$$

**符号说明**

- $o$：一条完整的智能体交互轨迹。
- $R(o)$：用于强化学习的总奖励。
- $I_{\mathrm{valid}}(o)$：格式有效性指示量；仅当轨迹含推理、可执行代码和可解析终结答案时为1。
- $w_p,w_c$：$p$值奖励和结论奖励的权重，文中分别设为0.9和0.1。
- $r_p(o)$：报告$p$值与答案键$p$值的接近度奖励。
- $r_c(o)$：结论正确性奖励；若最终拒绝/不拒绝决定匹配答案键则为1，否则为0。
- $\hat{p},p^{*}$：智能体报告的$p$值与规范参考分析的答案键$p$值。
- $\Phi^{-1}$：标准正态分布累积分布函数的反函数。
- $z(p)$：与双侧$p$值$p$对应的标准正态$z$分数重标记。
- $\sigma$：$p$值接近度奖励的尺度参数，文中设为1。

<div class="equation-explanation" markdown="1">

**直观理解**：若输出格式不完整，整条轨迹的奖励为零；格式合格后，奖励主要看报告的$p$值是否接近标准分析，次要看结论是否一致。$z(p)$只是对$p$值做单调重标记，并不假设原始数据服从正态分布；截断$z$为5可避免极端小$p$值主导学习信号。<br>
**原文位置**：第4.3节“Reward”，式(7)、式(8)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：优化分两阶段衔接。SFT阶段最小化过滤后教师响应中助手token的掩码自回归负对数似然，使策略先学会在工具观测条件下生成完整的统计分析轨迹；RL阶段从该策略出发，最大化$J_{\mathrm{DAPO}}(\theta)$。其优化信号来自$R(o)$而非固定“方法标签”监督：$p$值接近规范分析且结论正确的执行路径被强化。作者明确不在奖励中加入显式方法正确性项，理由是同一假设检验任务可存在多种可辩护程序；这一设计的代价是，若替代方法偶然产生近似$p$值，奖励本身不能区分其统计论证是否同样充分。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 可执行合成任务生成器**

任务空间为$M\times S_m\times N\times E\times P\times K$。其中$M$覆盖27类参数、秩检验、回归、因果、层级和生存分析方法；$E$含null、borderline、medium三档，borderline档由模拟自动校准到显著性边界附近；每个任务的答案键均由规范方法对生成数据运行得到。

> 直观理解：它解决了真实论文数据难以大规模提供、且难以自动验证训练奖励的问题。不同样本量、效应强度和提示方式迫使模型关注数据与研究设计，而不能只靠题目措辞猜方法。

**2. 质量控制的ReAct监督初始化**

教师轨迹采用$\texttt{<think>}$、$\texttt{<code>}$、$\texttt{<observation>}$和$\texttt{<answer>}$标签；训练时只优化助手生成的token，提示和工具观测仅作条件上下文。筛选剔除教师元数据与答案键泄漏，并要求轨迹结论和$p$值通过自动核验。

> 直观理解：代码、执行结果和结论被保留在同一条轨迹中，模型学到的是“看见结果后如何继续分析”的过程。质量过滤避免把教师的统计错误或答案泄漏直接教给学生模型。

**3. Fisher结果奖励**

奖励由严格格式门控$ I_{\mathrm{valid}}(o)$控制，权重为$w_p=0.9$和$w_c=0.1$。$p$值奖励将$\hat{p}$与$p^*$转换为双侧标准正态$z$分数后比较，且把$z$截断为5；结论奖励$r_c\in\{0,1\}$检查在$\alpha=0.05$下是否与答案键一致。

> 直观理解：极小$p$值在原始数值尺度上挤在接近零的位置，直接比较会掩盖证据强弱的重大差别；$z$尺度把这种差别拉开。格式门控也避免模型只报一个数字却不执行可审查的分析过程。

**训练与推理**

训练集与P-Bench隔离：合成脚本、数据和答案键用于生成可验证反馈，P-Bench不进入训练，以检验分布外泛化。SFT先从4,611条教师轨迹中筛得3,851条；RL时模型在R环境中实际执行代码，每个提示采样轨迹组、按格式及结果打分，并以DAPO更新。部署或评测时，输入$x=(q,D,s)$，模型经过多轮“生成动作-环境执行-读取观测”的循环，最终从轨迹中解析$\hat{p}$与$\hat{\delta}$，再与隐藏键$k^*=(p^*,\delta^*)$比较。

**复现信息**

为保证规范统计实现的一致性，作者选用R而非Python，理由是Cox比例风险、混合效应、工具变量、稳健和秩检验等所需R包更成熟，且默认设置更接近生物医学、统计学和经济学中的常用参考实现。SFT使用3个epoch、学习率$1\mathrm{e}{-5}$、批大小16、截断长度8192；RL使用1个epoch、学习率$1\mathrm{e}{-6}$、批大小16、最大提示/回复长度分别为2048/4096、rollout温度0.7、$G=8$。推断使用温度0.3、top-$p=0.9$、批大小10；14B模型完整RL训练约36小时，硬件为单节点NVIDIA H200 GPU。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- P-Bench：由 $425$ 个开放式、真实假设检验任务构成的评测基准，覆盖经济学、生物学和医学。每个任务只提供科学假设和数据集，要求智能体自行选择统计方法、计算 $p$ 值并给出结论；实验按难度划分为 P-Easy 与 P-Hard。其角色是检验端到端统计推断，而非只检验代码执行或结论方向。
- SFT 与 RL 训练语料：原文说明其训练任务是合成模拟任务，而 P-Bench 是真实世界任务。作者未在所给章节报告训练集规模；该语料在语义相似度分析中被用作与 P-Bench 对照的训练池，以检验评测收益是否可能来自近重复提示。
- P-Bench 与训练池的提示文本：作者提取每个输入中的研究问题与研究描述，使用 OpenAI 的 $\text{text-embedding-3-small}$ 嵌入，并计算每个样本相对训练池最近 $5$ 个邻居的平均余弦相似度。该分析数据不是额外性能数据集，而是泛化而非记忆的证据来源。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Raw（pass@1 / pass@3）**

在显著性水平 $\alpha=0.05$ 下，模型最终“拒绝”或“不拒绝”原假设的决定是否与标准答案一致；无法解析的输出计错。每题独立采样 $3$ 次，pass@1 为每次试验成功率的平均值，pass@3 表示三次中任一次成功即视为该题解决。 （越高越好，因为它衡量结论方向的端到端正确率；但它不要求模型给出的 $p$ 值准确，因此不能单独证明推断过程可靠。）

</div>
<div class="metric-item" markdown="1">

**Strict（pass@1 / pass@3）**

除满足 Raw 外，还要求报告的 $p$ 值 $\hat p$ 与标准 $p$ 值 $p^*$ 在双侧 $z$ 空间满足 $|z(\hat p)-z(p^*)|<0.5$，其中 $z(p)=\Phi^{-1}(1-p/2)$，$\Phi^{-1}$ 是标准正态分布累积分布函数的反函数。用 $z$ 空间比较能使不同量级的 $p$ 值具有更可比的误差尺度。 （越高越好，因为它同时要求结论正确和 $p$ 值足够接近标准分析，因而比 Raw 更接近“统计推断可靠性”。但它仍以专家审定的规范分析为参照，不能直接覆盖所有合理但不同的分析路径。）

</div>
<div class="metric-item" markdown="1">

**最近邻平均余弦相似度**

对每个评测或训练提示，计算其嵌入与训练池中最相近 $5$ 个提示之间的平均余弦相似度。作者用训练对训练的相似度分布形成可能的模板记忆带，再观察评测对训练分布的位置。 （此指标没有单向的“越高越好”。若评测对训练相似度明显低于训练内部的高相似度带，说明 P-Bench 缺少训练提示的近重复项，较支持泛化解释；但嵌入相似度不能严格排除训练数据中存在概念、统计程序或数据结构层面的泄漏。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### P-Bench 主结果，Fisher-R1-14B 与 GPT-5.4 在 Strict 指标上的比较。

<div class="result-value" markdown="1">

Fisher-R1-14B 在 P-Hard Strict 上达到 pass@1 $33.0\pm1.7$、pass@3 $45.5$，高于 GPT-5.4 的 $30.5\pm1.6$ 与 $39.2$；在 P-Easy Strict pass@3 为 $75.9$，高于 GPT-5.4 的 $73.4$。但 P-Easy Strict pass@1 为 $64.2\pm0.6$，略低于 GPT-5.4 的 $64.7\pm3.3$。

</div>

这支持作者的主张：在更难的任务和多次采样成功率上，$14$B 的专门训练模型可以超过该闭源基线，且优势体现在严格的 $p$ 值标准而非仅结论方向。它不证明 Fisher-R1 在所有统计任务、所有采样预算或所有闭源模型上更强；P-Easy Strict pass@1 的结果也显示其并非全面领先。

<div class="result-source" markdown="1">

来源：第 5.2 节 Main Results，表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Fisher-R1-14B further exceeds GPT-5.4 on three of four Strict metrics (P-Easy pass@3: 75.9 vs 73.4; P-Hard pass@1: 33.0 vs 30.5; P-Hard pass@3: 45.5 vs 39.2), trailing only narrowly on P-Easy Strict pass@1 (64.2 vs 64.7).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### P-Bench 主结果，Fisher-R1-7B 相对其未经 Fisher-R1 训练的 Qwen-2.5-Coder-7B 骨干。

<div class="result-value" markdown="1">

在 P-Easy 上，Raw pass@1 从 $61.4\pm8.5$ 升至 $87.0\pm1.6$，Strict pass@1 从 $36.3\pm5.5$ 升至 $65.7\pm1.2$；在 P-Hard 上，Raw pass@1 从 $37.5\pm2.8$ 升至 $63.4\pm2.5$，Strict pass@1 从 $13.2\pm0.5$ 升至 $30.6\pm1.2$。

</div>

同一 $7$B 骨干前后的大幅变化，将性能提升更直接地归因于 Fisher-R1 的训练流程，而非单纯模型规模。Strict 的增幅尤其关键，说明提升不仅是更常猜对显著性方向，也更常产生接近规范分析的 $p$ 值；不过该对照不能分别量化合成任务、SFT、DAPO 和奖励设计各自的独立贡献。

<div class="result-source" markdown="1">

来源：第 5.2 节 Main Results，表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

With the 7B backbone, Raw pass@1 rises from 61.4 to 87.0 on P-Easy and from 37.5 to 63.4 on P-Hard, while Strict pass@1 jumps from 36.3 to 65.7 (P-Easy) and 13.2 to 30.6 (P-Hard); the 14B variant achieves the best P-Hard Strict scores in the table (33.0 pass@1, 45.5 pass@3).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### P-Hard 上 GPT-5.4 的 Raw 与 Strict 差距，用于检验只看最终假设检验结论是否会高估可靠性。

<div class="result-value" markdown="1">

GPT-5.4 的 P-Hard pass@1 Raw 为 $58.3\pm0.9$，而 Strict 仅为 $30.5\pm1.6$；即它较常得到正确的拒绝/不拒绝方向，但较少同时给出接近规范值的 $p$ 值。作者还报告，将阈值放宽为 $|\Delta z|<1$ 后，定性结论不变。

</div>

该结果直接说明结论方向正确不等价于统计计算正确，因而 Raw 单指标会掩盖不可靠的 $p$ 值。它支持采用 Strict 评测，但不等于证明 Strict 阈值 $0.5$ 是唯一或普适的有效性定义；原文只说明阈值放宽后的定性结论一致，未在所给摘录中提供表 5 的具体数字。

<div class="result-source" markdown="1">

来源：第 5.2 节 Main Results，表 1；阈值稳健性见表 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GPT-5.4, for example, scores 58.3 Raw but only 30.5 Strict on P-Hard pass@1: it reports the correct reject/fail-to-reject direction nearly twice as often as it produces a p-value close to the canonical analysis.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评测的 Strict 正确性以规范分析的 $p$ 值为中心，并采用 $|z(\hat p)-z(p^*)|<0.5$ 阈值；这比只评结论更严格，但未充分处理同一研究问题存在多个合理统计模型、预处理选择或多重比较校正方案的情形。
- 所给实验章节只报告 P-Bench 上的三次 rollout 结果及嵌入相似度分析，未报告跨新领域、真实交互式研究工作流、不同工具环境或不同推理预算下的稳健性；相似度低也不能完全排除统计模板和概念层面的训练泄漏。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Qwen-2.5-Coder-7B 与 Qwen-2.5-Coder-14B：分别是 Fisher-R1-7B 和 Fisher-R1-14B 的直接骨干模型，用于隔离训练方案本身带来的增益。
- GPT-5.4：强闭源模型比较对象，用于判断 Fisher-R1 是否能在严格的 $p$ 值正确性标准下与先进专有模型竞争。
- DeepSeek-V4-Pro：强开源模型比较对象，也是摘要中平均相对提升的主要参照；其规模和训练来源不同于 Fisher-R1，因而可检验专门统计奖励训练相对通用能力扩展的价值。
- DataMind-7B/14B：已针对数据分析训练的开源模型，用于检验“通用数据分析训练”是否足以替代面向假设检验、带验证统计奖励的训练。

**实验想回答的问题**

- 在开放式、真实的假设检验任务中，Fisher-R1 是否能同时提高最终拒绝/不拒绝结论的正确性，以及所报告 $p$ 值的数值正确性，并超过通用闭源和开源模型？
- Fisher-R1 的性能提升是否依赖于监督微调（SFT）暖启动与 DAPO 强化学习的组合，且能排除对训练提示模板的近重复记忆？

**实验实现**

作者在 P-Easy 和 P-Hard 上评测各模型；每个任务进行 $3$ 条独立 rollout，并在 Raw 与 Strict 两种准则下报告 pass@1、pass@3。pass@1 报告为三次独立运行的均值 $\pm$ 标准差。规范答案来自同行评议论文或权威课程材料，并经专家审计。消融使用 $7$B 骨干，依次比较原始 Qwen-2.5-Coder-7B、仅加 DAPO、仅加 SFT、以及 SFT 后加 DAPO。泛化分析使用提示文本嵌入和最近 $5$ 邻居余弦相似度；所给章节未报告推理温度、token 预算、工具执行环境或显著性检验的统计置信区间。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 以 Qwen-2.5-Coder-7B 为起点，仅施加 DAPO，与未训练骨干比较。 | P-Hard Strict pass@1 从 $13.2\pm0.5$ 提升至 $25.2\pm0.8$，但仍低于 SFT+DAPO 的 $30.6\pm1.2$；P-Easy Strict pass@1 从 $36.3\pm5.5$ 升至 $44.4\pm0.9$，也低于组合训练的 $65.7\pm1.2$。 | 该消融隔离了直接在骨干上做 DAPO 的效果：强化学习奖励本身可以提升严格统计正确性，但不足以达到完整系统水平。由于实验没有报告不同随机种子、训练步数和计算量匹配的细节，不能由此精确判定差距全部来自 SFT 的知识初始化，而非训练配额或优化动态。 | 第 5.3 节 Ablation Analysis，表 2<br><span class="experiment-evidence">DAPO applied directly to the backbone lifts single-run accuracy (e.g., P-Hard Strict pass@1 13.2 to 25.2), but plateaus well below SFT+DAPO.</span> |
| 以 Qwen-2.5-Coder-7B 为起点，比较仅 SFT 与 SFT 后 DAPO。 | 仅 SFT 的 P-Hard Strict pass@1 为 $14.3\pm1.1$、pass@3 为 $30.2$；SFT+DAPO 分别为 $30.6\pm1.2$、$44.1$。在 P-Easy Strict 上，仅 SFT 的 pass@1/pass@3 为 $30.2\pm4.6$/$59.6$，组合训练为 $65.7\pm1.2$/$74.9$。 | 该比较表明 SFT 单独并未稳定提高单次成功率，作者将其 pass@3 的改善解释为拓宽了解题分布；在此暖启动上加入 DAPO 后，模型才在四组 Raw/Strict、pass@1/pass@3 指标上达到最高。该结果支持两阶段训练的互补性，但尚未测试 SFT 数据量、顺序互换或其他 RL 算法是否能产生同等效果。 | 第 5.3 节 Ablation Analysis，表 2<br><span class="experiment-evidence">Table 2 shows that combining the SFT warm-start with DAPO is essential to reach Fisher-R1’s full performance: SFT+DAPO achieves the best score on every metric, substantially above either stage alone.</span> |

**定性案例**

- 泛化相似度分析是唯一给出的定性诊断：训练对训练的相似度形成紧密的高相似度“memorization band”，而评测对训练的相似度明显低于该带。作者据此认为 $425$ 个 P-Bench 任务没有 RL 语料中的近重复对应项，且真实评测任务与合成训练任务在构造上不同。它支持“不是直接检索训练提示”的解释，但并非逐题人工溯源或严格数据去重审计。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It trains an LLM agent with verified-reward reinforcement learning to select valid statistical tests and perform reliable hypothesis-testing reasoning.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`064c24da0ac5c6c34573c95a2288186dda172cd319c55fac7165e92685f24f50`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
