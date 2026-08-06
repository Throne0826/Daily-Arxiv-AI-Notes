---
title: "[论文解读] Toward Skill-Native LLMs: Skill Entropy for Benchmarking and Training Long-Horizon Reasoning"
description: "[arXiv 2608.05139][LLM Reasoning] 本文将跨技能长程推理中的“技能切换难度”显式量化为技能熵，并进一步把该量用于构建分级基准和设计强化学习奖励，以评测和训练模型在同一推理链中正确切换技能的能力。"
arxiv_id: "2608.05139"
announcement_date: "2026-08-06"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:51:13.342622+00:00"
source_sha256: "d92343dd758375e9dc4273e5bd1d77f0061bac4ad078083067a6e32df9e36bf9"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "对齐 / RLHF"
  - "大语言模型"
  - "长程推理"
  - "跨技能任务"
  - "技能切换"
  - "技能熵"
  - "组合推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.05139</p>

# Toward Skill-Native LLMs: Skill Entropy for Benchmarking and Training Long-Horizon Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Yinghui He, Ling Yang, Jiarui Liu, Yongjin Yang, Lechen Zhang, Yingcheng Wu, Zhenfei Yin, Mengdi Wang, Sanjeev Arora</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Princeton University；Carnegie Mellon University；University of Toronto；University of Illinois Urbana-Champaign；Stanford University；University of Oxford</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.05139v1) · [PDF 下载](https://arxiv.org/pdf/2608.05139v1) · **关键词** 大语言模型, 长程推理, 跨技能任务, 技能切换, 技能熵, 组合推理<br>
**代码**: [https://github.com/Gen-Verse/Skill-Entropy-RL](https://github.com/Gen-Verse/Skill-Entropy-RL)

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

本文将跨技能长程推理中的“技能切换难度”显式量化为技能熵，并进一步把该量用于构建分级基准和设计强化学习奖励，以评测和训练模型在同一推理链中正确切换技能的能力。

**不用术语来说**：现实中的复杂任务往往不能只靠一种能力完成：模型可能先做数学推导，再根据结果制定计划，最后从材料中提取信息。即使模型分别会做这些事情，把它们连续组合起来时也可能沿用上一步的思考方式，未能及时切换到当前步骤所需的能力，且早期错误还会影响后续步骤。论文关注的不是模型“会不会某项技能”，而是它能否在相互依赖的多步任务中“在正确时刻换用正确技能”。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者形式化定义跨技能长程任务，并提出有方向性的成对技能熵来表示从一种技能切换到另一种技能的难度；沿任务的技能序列聚合后，可得到任务级技能熵，从而为不同跨技能任务提供统一的难度尺度。
- 作者把技能熵同时用于评测与训练：构建覆盖九个领域、558 种技能并按低中高难度划分的 Skill²-Bench；同时提出 Skill-Entropy RL，要求模型在每步作答前预测所用技能，并以步骤正确性和预测技能链与标准技能链的一致程度共同提供奖励。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型的长程推理能力，重点不是模型能否分别完成数学、编程或规划等单项任务，而是能否在同一条多步推理链中根据当前步骤切换技能，并正确利用前序步骤的答案。现实任务往往跨越多个领域，例如先进行数学推导，再依据结果制定计划，最后从材料中提取信息；已有研究表明，即使模型单独掌握各组成技能，在组合任务中仍可能表现脆弱，因此“技能切换”应被视为区别于单领域能力的独立评测维度。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**长程推理**

指需要连续完成多个相互依赖步骤的推理过程，后一步通常要使用前一步产生的结果。其难点不仅来自步骤数量，还来自错误传播和跨步骤状态保持。

</div>
<div class="concept-item" markdown="1">

**推理技能**

指解决某类问题所需的相对明确的操作能力，例如数学中的符号积分、逻辑任务中的约束传播。本文把技能归属于其最初出现的来源领域，并为每个种子问题标注对应技能。

</div>
<div class="concept-item" markdown="1">

**跨技能长程任务**

指由多个相互依赖的问答步骤组成、且相邻步骤来自不同领域并调用不同技能的任务。模型必须保持统一情境和前序结果，同时改变当前步骤所采用的推理方式与答案形式。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文设定有限领域集合 $\mathcal{D}=\mathcal{D}_{\mathrm{ver}}\cup\mathcal{D}_{\mathrm{open}}$，分别包含可验证领域与开放式领域。每个领域 $d$ 配有种子数据集 $\mathcal{X}_d$：可验证任务中的 $a$ 是标准答案，开放式任务中的 $a$ 是评分准则；每个问题还标注一个技能。一个跨技能任务 $\tau$ 由长度 $L\in[2,10]$ 的问答步骤序列组成，并对应技能序列 $\mu(\tau)$。相邻步骤的技能来源领域必须不同，且各步骤被改写到统一情境 $\sigma$ 中；第 $i$ 步依赖先前答案，但应保留原种子问题的底层逻辑与正确答案。模型需要为每一步输出预测答案 $\hat{a}_i$，再由该步骤所属领域的评分器 $\operatorname{eval}_d(\hat{a},a,q)\in[0,1]$ 评估，例如数学使用符号等价性、编程使用沙箱单元测试，整个任务的分数取各步骤得分的平均值。通俗地说，输入是一组被串成同一故事且前后依赖的问题，输出是逐步答案；评测既要求每一步做对，也隐含要求模型在步骤之间及时更换合适的解题方式。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{D}=\mathcal{D}_{\mathrm{ver}}\cup\mathcal{D}_{\mathrm{open}}$**

全部任务领域的有限集合，由可验证领域集合与开放式领域集合组成。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{S}=\bigcup_{d\in\mathcal{D}}\mathcal{S}_d$**

所有领域技能集合的并集；每个技能具有唯一的来源领域。

</div>
<div class="notation-item" markdown="1">

**$\tau=((q_1,a_1),\ldots,(q_L,a_L))$**

长度为 $L$ 的跨技能长程任务，其中每个元素是一对当前步骤的问题与参考答案或评分准则。

</div>
<div class="notation-item" markdown="1">

**$\mu(\tau)=(s_1,\ldots,s_L)$**

任务 $\tau$ 的技能序列，$s_i$ 表示第 $i$ 个步骤调用的推理技能。

</div>

</div>

**直接相关的工作**

- **GSM8K、MATH、LiveCodeBench、ZebraLogic、MMLU-Pro 与 BBH**: 这些基准主要检验数学、编程、逻辑或综合知识等单项或相对独立的能力。本文以它们所代表的单技能评测为对照，指出模型在单项基准上的高表现不能充分说明其跨技能切换能力。
- **SkillMix、Skill Composition 与 RL-Compose**: 这些工作直接涉及技能混合或技能组合，并观察到模型即使能独立处理组成技能，在组合任务中仍可能退化。本文在这一观察上进一步把跨技能任务形式化，并寻求对任务内部技能切换难度进行定量刻画。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

深度研究、智能体编程和多步规划等应用要求模型在一条持续的推理链中处理多个相互依赖的步骤，而不同步骤可能分别需要数学、编程、规划、信息抽取或写作等技能。模型若不能在步骤边界处正确切换技能，就可能把上一阶段的推理方式或答案形式错误地带入下一阶段；由于后续问题依赖先前输出，这类局部切换失误还会沿长程任务继续传播。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **单技能或单领域基准**：以 GSM8K、MATH、LiveCodeBench、ZebraLogic、MMLU-Pro 和 BBH 等为代表，分别用数学、代码、逻辑或知识问题评估模型在某一技能或领域中的独立能力。这类评测可以回答模型是否掌握组成任务的基本技能，但通常不要求模型在同一条推理链内跨越多个技能。
- **长程、组合式或智能体任务评测**：以 GAIA、AgentBench、OdysseyBench、HeroBench 以及既有技能组合研究为代表，通过多步骤或多能力任务考查模型的综合表现。它们能够暴露模型在复杂任务上的脆弱性，但论文指出，已有评测没有提供任务级尺度来量化具体技能切换本身有多困难。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单技能评测把各项能力分开测量，因此即使模型在每项技能上都表现良好，也无法据此判断它能否在同一任务中保持上下文依赖并正确切换技能；其后果是单项高分可能掩盖独立于领域能力的技能切换缺陷。
- 既有长程或组合式评测虽能给出整体成败，却缺少对技能转换难度的有方向、可聚合量化。例如，从数学切换到创意写作与反向切换未必同样困难，但没有统一尺度便难以按切换难度分层比较任务，也难以把失败精确归因并转化为训练信号。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一个连接评测与训练的显式技能切换表示：它既要在成对层面刻画“从技能 $i$ 转向技能 $j$”的方向性难度，又要能沿多步技能序列聚合为任务级难度，并进一步用于监督模型在每一步选择正确技能。因而，模型在复杂任务中失败究竟源于单项技能不足，还是源于切换失败，过去难以被系统区分和针对性优化。

</div>
<div markdown="1"><span>核心问题</span>

能否定义一种可计算的技能切换难度，使其一方面能够对跨技能长程任务进行分级并揭示模型随切换难度增加而出现的性能退化，另一方面又能作为强化学习奖励，直接训练模型在每个步骤识别并采用当前所需技能？

</div>
<div markdown="1"><span>作者直觉</span>

不同技能具有不同的推理结构和输出形式，相近技能之间共享的结构较多，切换通常较自然；差异较大的技能之间则需要模型主动改变推理策略。若要求模型在每步回答前明确给出技能标签，原本隐含的“现在该用什么能力”就变成可检查的中间决策；再根据预测技能链与标准技能链的匹配程度给予奖励，训练便不仅纠正最终答案，也能直接纠正沿用上一技能等切换错误。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Skill-Entropy RL 是一个“先用监督学习教会结构化作答，再用强化学习校准答案与技能规划”的两阶段训练框架。输入是由多个相互依赖步骤组成的跨技能任务 $\tau=((q_1,a_1),\ldots,(q_L,a_L))$，其中相邻步骤来自不同领域；模型需要输出一段推理轨迹，并为每一步依次生成技能标签 $\hat{s}_i$ 和答案 $\hat{a}_i$。系统将这些标签解析为预测技能序列 $\hat{\mu}(\tau)$，一方面用领域专用评分器检查逐步答案，另一方面比较预测技能序列与金标准技能序列 $\mu(\tau)$ 的技能熵秩，最后以二者的加权奖励执行 GRPO 更新。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造或标注跨技能训练任务

对 Skill$^2$-Bench 数据，任务在构造时已带有金标准技能序列 $\mu(\tau)=(s_1,\ldots,s_L)$、逐步答案和领域信息。对普通训练数据，则由 Qwen3-8B 将推理轨迹切分成步骤，从技能库为每一步分配技能，并把中间结论作为逐步金标准答案。

<div class="method-step__io" markdown="1">

**输入**：主要训练输入是从 Skill$^2$-Bench 六个可验证领域合成的跨技能任务；扩展实验也可输入带正确答案和推理轨迹的 OpenR1-Math 样本。<br>
**输出**：得到带逐步问题、逐步答案、领域标签和金标准技能序列的训练实例，并可依据论文的技能熵定义计算任务级技能熵及其训练分布秩 $\rho^\star$。

</div>

**直观理解**：这一阶段把一道长题整理成一张“分步施工单”：每一步不仅有正确结果，还注明应调用哪类能力。这样强化学习才能判断模型是否在正确的时刻切换了技能。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### SFT 学习技能标注式响应格式

对基础模型进行监督微调，使其生成一个 $\langle\mathrm{think}\rangle$ 块，随后为每个步骤交替输出 $\langle\mathrm{skill}\rangle$ 与 $\langle\mathrm{answer}\rangle$。技能标签包含技能库中的“领域、技能”二元描述。

<div class="method-step__io" markdown="1">

**输入**：3K 个带教师轨迹的跨技能任务，教师为 Qwen3-8B；每条轨迹包含推理文本、逐步技能标签和逐步答案。<br>
**输出**：得到能够稳定输出结构化技能计划 $\hat{\mu}(\tau)=(\hat{s}_1,\ldots,\hat{s}_L)$ 和答案序列 $(\hat{a}_1,\ldots,\hat{a}_L)$ 的 SFT 初始化模型。

</div>

**直观理解**：SFT 先教模型遵守一种可机器读取的答题格式，相当于要求它在每步答案前写明“这一步准备使用什么技能”。这主要解决输出结构和初始行为问题，而不是最终的奖励优化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 解析并评价答案与技能计划

正则解析器抽取每一步的 $\hat{s}_i$ 与 $\hat{a}_i$；各领域评分器分别检查答案，并取逐步得分均值形成 $r_{\mathrm{ans}}$。每个预测技能先按嵌入相似度映射到技能库中最近的技能，再计算预测技能熵的训练分布秩 $\hat{\rho}$，由其与金标准秩 $\rho^\star$ 的距离得到 $r_{\mathrm{ent}}$。

<div class="method-step__io" markdown="1">

**输入**：模型对一个长度为 $L$ 的任务生成的结构化响应，以及对应的金标准逐步答案、领域、技能序列和技能库。<br>
**输出**：两个位于 $[0,1]$ 的任务级信号：答案奖励 $r_{\mathrm{ans}}$ 和技能熵奖励 $r_{\mathrm{ent}}$；格式错误的响应两项奖励均为零。

</div>

**直观理解**：答案奖励检查“每一步做得对不对”，技能熵奖励检查“整条技能切换路线的难度结构是否与标准路线相符”。嵌入匹配允许模型使用语义相近但措辞不同的技能名称，避免只按字符串完全一致来扣分。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 使用组合奖励执行 GRPO

将两项信号按 $\lambda_{\mathrm{ans}}=0.7$、$\lambda_{\mathrm{ent}}=0.3$ 加权为总奖励 $r$，再用 GRPO 在同一提示的成组采样响应之间计算相对优势并更新模型。训练同时保留 KL 约束和裁剪，以限制策略更新幅度。

<div class="method-step__io" markdown="1">

**输入**：SFT 初始化模型、6K 个强化学习任务，以及每个候选响应对应的 $r_{\mathrm{ans}}$ 和 $r_{\mathrm{ent}}$。<br>
**输出**：得到既追求逐步正确性、又倾向于生成合适技能切换结构的 Skill-Entropy RL 模型。

</div>

**直观理解**：普通答案奖励只告诉模型结果好不好；新增奖励还评价它采用的技能路线是否合理。GRPO 据此提高高奖励响应的概率，并降低低奖励响应的概率。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 答案与技能熵组合奖励

$$
r=\lambda_{\mathrm{ans}}r_{\mathrm{ans}}+\lambda_{\mathrm{ent}}r_{\mathrm{ent}}
$$

**符号说明**

- $r$：用于 GRPO 策略优化的任务级总奖励。
- $r_{\mathrm{ans}}$：逐步答案在领域专用评分器下所得分数的均值，取值属于区间 $[0,1]$。
- $r_{\mathrm{ent}}$：预测技能计划与金标准计划在技能熵秩上的一致性奖励，取值属于区间 $[0,1]$。
- $\lambda_{\mathrm{ans}}$：答案奖励权重；主要实验设置为 $0.7$。
- $\lambda_{\mathrm{ent}}$：技能熵奖励权重；主要实验设置为 $0.3$。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标同时奖励“把各步骤做正确”和“给出合适的技能切换结构”。若移除第二项，方法就退化为仅使用答案奖励的 GRPO 基线，因此第二项是论文训练方法区别于普通 GRPO 的核心。<br>
**原文位置**：公式（5），第 4.1 节；权重设置见第 4.2 节

</div>

</div>

<div class="equation-block" markdown="1">

#### 技能熵秩一致性奖励

$$
r_{\mathrm{ent}}=1-\left|\hat{\rho}-\rho^{\star}\right|
$$

**符号说明**

- $r_{\mathrm{ent}}$：预测技能序列与金标准技能序列之间的技能熵秩一致性奖励。
- $\hat{\rho}$：预测技能序列经技能库映射、技能熵计算后，在训练分布中的归一化秩，属于区间 $[0,1]$。
- $\rho^{\star}$：金标准技能序列的任务级技能熵在训练分布中的归一化秩，属于区间 $[0,1]$。

<div class="equation-explanation" markdown="1">

**直观理解**：预测秩与金标准秩完全一致时奖励为 $1$；二者距离越大，奖励线性下降。使用分布秩而非原始技能熵，可把不同数值尺度压到统一的 $[0,1]$ 范围，但该奖励主要约束整体难度结构，并不等同于逐步技能分类准确率。<br>
**原文位置**：公式（6），第 4.1 节；技能熵本身引用公式（4），但所给节选未包含公式（4）的完整表达式

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：优化从 SFT 模型开始：SFT 先最大化教师结构化轨迹的条件生成似然，使模型学会输出可解析的技能与答案。随后，GRPO 对每个提示采样一组响应，以组合奖励 $r$ 形成组内相对优势并更新生成策略；答案项推动逐步任务正确性，技能熵项推动预测计划的技能熵秩接近金标准。论文将只保留 $r_{\mathrm{ans}}$ 的设置定义为普通 GRPO，因此完整方法相对于该基线增加的直接优化约束就是 $r_{\mathrm{ent}}$。需要注意，奖励比较的是技能序列的熵秩而非逐位置标签完全一致，故其作用是学习跨步骤切换结构，同时通过嵌入映射容纳语义相近的技能表达。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 技能标注式响应与严格解析器**

响应由单个 $\langle\mathrm{think}\rangle$ 块和 $L$ 组相邻的 $\langle\mathrm{skill}\rangle$、$\langle\mathrm{answer}\rangle$ 标签组成。正则解析要求每一步的技能标签后立即出现答案标签；不符合格式的输出获得零答案奖励和零技能熵奖励。

> 直观理解：该模块把难以直接监督的长推理转成清晰的逐步记录，使系统能把“选错技能”和“技能执行错误”分开评价。严格格式也防止模型通过省略标签绕过技能规划奖励。

**2. 领域专用逐步答案评分器**

每个领域都有评分函数 $\operatorname{eval}_d(\hat{a},a,q)\in[0,1]$，例如数学使用符号等价判断，代码使用沙箱单元测试；任务答案奖励是所有步骤得分的均值。可验证领域提供客观正确答案，开放式领域的种子数据则以评分准则表示参考答案。

> 直观理解：不同任务不能用同一种字符串匹配方式评分：等价数学表达式可能写法不同，程序则必须实际运行。逐步计分还能避免只看最终答案而忽略中间步骤是否可靠。

**3. 技能匹配与技能熵秩奖励**

模型生成的自由文本技能名先通过嵌入相似度映射到技能库最近条目，然后据论文公式（4）计算预测序列的任务级技能熵，并转换为训练分布中的归一化秩 $\hat{\rho}$。奖励比较 $\hat{\rho}$ 与金标准技能熵秩 $\rho^\star$，而不是要求预测技能名称逐项完全相等。

> 直观理解：该设计关注模型给出的整条技能路线是否具有相近的切换难度，同时容忍同义技能描述。不过，秩相近不必然表示每一步技能都相同，因此它提供的是结构级训练信号，而非严格的逐标签监督。

**训练与推理**

标准训练流程在 Qwen3-4B-Instruct 和 Qwen3-1.7B 上执行。作者从六个可验证领域合成 9K 个跨技能任务，其中 3K 个由 Qwen3-8B 生成技能标注轨迹并用于 SFT 预热，其余 6K 个用于 GRPO；三个开放式领域不参与强化学习训练，只在相同的 300 题测试池上评估迁移。每轮强化学习中，模型生成带技能标签的逐步响应，解析器抽取答案与技能；答案由领域评分器评价，技能经嵌入匹配后计算技能熵秩奖励，两项合成为总奖励并用于策略更新。

对 OpenR1-Math 这类现成数据，作者先由 Qwen3-8B 切分已有金标准推理轨迹并标注技能，再以中间结论作为逐步答案、原始答案作为最后一步答案，之后复用相同的 SFT 与 RL 流程。这说明方法所需的关键接口是“逐步答案加技能序列”，而不要求原始数据天然按跨技能任务构造。推理阶段不执行训练奖励计算：模型接收任务后直接生成 $\langle\mathrm{think}\rangle$、逐步 $\langle\mathrm{skill}\rangle$ 和 $\langle\mathrm{answer}\rangle$；评分器、金标准序列及其熵秩只服务于训练和评测。

**复现信息**

SFT 训练 $4$ 个 epoch，学习率为 $10^{-5}$。GRPO 的组大小为 $8$，提示批量大小为 $256$，学习率为 $10^{-6}$，KL 系数为 $10^{-3}$，裁剪比率为 $0.2$；奖励权重设为 $\lambda_{\mathrm{ans}}=0.7$、$\lambda_{\mathrm{ent}}=0.3$，训练使用 $8$ 张 H100。复现时还必须保持严格的标签解析规则，因为畸形响应的两项奖励均为零；预测技能名称不能直接按字符串比较，而应按论文流程通过嵌入相似度映射到技能库。所给节选没有提供公式（4）的完整技能熵定义、具体嵌入模型、GRPO 完整超参数表及领域评分器清单，精确复现这些部分需要核对原文第 D.3、D.4、D.6 节和第 B.1 节。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Skill$^2$-Bench：核心评测集，覆盖数学、科学、编程、逻辑、信息抽取、规划、创意写作、上下文检索和指令遵循共 $9$ 个领域、$558$ 个带标签技能。可验证领域从 OpenR1-Math、MMLU-Pro、LiveCodeBench、ZebraLogicBench、Guru-RL-92k、WikiTable、WebSRC 和 NaturalPlan 等种子数据改写得到，并使用问题—答案对判分；三个开放式领域使用由大模型生成的问题—评分准则对，再由大模型裁判评分。任务按 $\mathrm{SkE}(\tau)$ 分为低、中、高三个难度等级，用于检验性能是否随技能切换难度变化。原文节选未明确报告任务总数及训练集、验证集和测试集的具体划分。
- Skill$^2$-Bench 开放式领域人工复核子集：从创意写作、上下文检索和指令遵循三个领域各均匀抽取 $200$ 个跨技能步骤，覆盖不同被评模型和技能熵等级；每个步骤由三名人工标注者依据与大模型裁判相同的逐步评分准则重新评分。该子集不用于比较模型能力，而用于验证 Claude-opus-4.7 裁判分数是否可信。
- OpenR1-Math：既是 Skill$^2$-Bench 数学领域技能库的种子数据，也被论文用于测试技能熵训练流程能否作用于现成训练数据。所给节选仅保留附录 D.1 标题，未提供该迁移实验的数据规模、划分或完整数值结果。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**逐步正确率与 Skill$^2$-Bench 总分**

可验证步骤依据标准答案判断，开放式步骤依据逐步评分准则判断；论文报告的 Skill$^2$-Bench 百分比概括模型在跨技能任务中的表现。Single-Skill 与 Cross-Skill 的逐步正确率差异用于衡量把已掌握技能放入长程链条后产生的损失。 （越高越好，因为更高数值表示更多步骤或任务被正确完成；但该指标同时受基础技能能力、上下文依赖和技能选择影响，不能单独证明模型已经学会显式技能切换。）

</div>
<div class="metric-item" markdown="1">

**任务级技能熵 $\mathrm{SkE}(\tau)$**

它是任务中相邻有向技能切换的平均难度，由固定参考模型在单技能与跨技能条件下的相对正确率确定。实验用它把任务分为低、中、高难度，检查不同模型是否在更难切换的任务上出现更明显的性能分化。 （它是难度尺度而非性能分数，不存在越高越好的含义；值越高表示参考模型从前一技能切换到后一技能时相对损失越大。）

</div>
<div class="metric-item" markdown="1">

**大模型裁判与人工评分一致性**

包括 Pearson $r$、Spearman $\rho$、平均绝对误差 MAE、阈值 $0.5$ 下的二元一致率以及 Cohen's $\kappa$。相关系数衡量分数共同变化及排序一致性，MAE 衡量绝对评分偏差，二元一致率和 $\kappa$ 衡量通过或不通过判断的一致程度。 （Pearson $r$、Spearman $\rho$、二元一致率和 Cohen's $\kappa$ 越高越好，MAE 越低越好；这些指标只验证裁判与人工的一致程度，不直接验证模型答案的事实正确性。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Skill-Entropy RL 在两个 Qwen3-Instruct 模型上的 Skill$^2$-Bench 结果

<div class="result-value" markdown="1">

Qwen3-4B-Instruct 的分数由 $34.4\%$ 提升到 $68.4\%$，绝对提升 $34.0$ 个百分点；Qwen3-1.7B 的分数由 $14.6\%$ 提升到 $40.1\%$，绝对提升 $25.5$ 个百分点。作者据此声称该方法优于竞争性基线，但节选没有提供基线名称、方差、重复次数或显著性检验。

</div>

同一训练思想在两个参数规模上都带来较大提升，支持“技能序列对齐可作为有效训练信号”的作者主张。不过，这些结果不能单独区分收益来自技能熵奖励、逐步正确性奖励、更多训练计算还是数据组织方式；也不能证明收益会推广到未报告的模型家族或所有外部基准。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Qwen3-4B-Instruct and Qwen3-1.7B, Skill-Entropy RL improves the Skill^2-Bench score from 34.4% to 68.4% and from 14.6% to 40.1%, respectively, outperforming competitive baselines.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 强模型从 Single-Skill 转入 Cross-Skill 条件后的失败模式

<div class="result-value" markdown="1">

对 GPT-5.5、Gemini-3.1-pro、Claude-opus-4.7 和 O4-mini，原本能在单技能条件下解决的步骤中，有 $9\%$ 至 $17\%$ 在跨技能任务中失败；这些新增失败中有 $31\%$ 至 $62\%$ 同时伴随模型选择了错误领域的技能。错误领域步骤的逐步正确率为 $32\%$ 至 $57\%$，而技能领域选择正确时为 $63\%$ 至 $79\%$。

</div>

配对比较表明，跨技能上下文确实会让一部分原本会做的步骤失败，而且选错技能类别与显著较低的答案正确率相伴。这支持“技能选择是长程推理瓶颈之一”的解释，但图中展示的是关联：错误技能标签可能是错误推理的表现，而不一定是导致答案错误的唯一因果原因。

<div class="result-source" markdown="1">

来源：图 5，附录 C

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For GPT-5.5, Gemini-3.1-pro, Claude-opus-4.7, and O4-mini, 9–17% of the steps these models solve in single-skill mode fail once placed inside a cross-skill task, and 31–62% of these new failures come with the model picking a skill from the wrong domain. On those wrong-domain steps, per-step accuracy (32–57%) is roughly half that on right-domain steps (63–79%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 开放式领域中 Claude-opus-4.7 裁判与人工标注的一致性

<div class="result-value" markdown="1">

三个开放式领域的平均 Pearson $r$ 为 $0.88$、Spearman $\rho$ 为 $0.86$、MAE 为 $0.06$、二元一致率为 $91.0\%$、Cohen's $\kappa$ 为 $0.81$。分领域二元一致率从创意写作的 $88.5\%$ 到指令遵循的 $93.0\%$。

</div>

这些数值说明大模型裁判与人工评分具有较高相关性和分类一致性，为把它用于开放式领域提供了经验依据。但验证集每个领域只有 $200$ 个步骤，且人工与裁判共享同一评分准则，因此结果主要说明“按同一准则打分时一致”，不能排除准则自身遗漏事实错误、风格偏差或裁判对特定模型输出的系统偏好。

<div class="result-source" markdown="1">

来源：表 10，附录 C

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Average 0.88 0.86 0.06 91.0 0.81

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

- Single-Skill 设置：将每个步骤脱离长程场景后独立询问模型，用来估计模型掌握单项技能时的能力。它与 Cross-Skill 设置中的对应步骤配对，因而可把同一内容在有无跨技能上下文时的差异解释为技能切换代价，而不是题目本身难度差异。
- Cross-Skill 设置：把完整任务场景及全部 $L$ 个逐步问题放入同一个提示中，要求模型连续完成相互依赖的步骤。这是论文的目标评测条件，并与 Single-Skill 设置形成直接对照。
- 未经 Skill-Entropy RL 训练的 Qwen3-4B-Instruct 与 Qwen3-1.7B：分别作为同参数规模的起点模型，用于衡量技能熵强化学习带来的净提升。摘要还声称该方法优于“competitive baselines”，但所给节选没有列出这些基线的名称、训练目标或分数，因此不能进一步比较。
- 人类评分：三名标注者的平均分作为开放式任务评分的参照，用于验证 Claude-opus-4.7 大模型裁判，而非作为可执行模型基线。

**实验想回答的问题**

- 模型在单项技能题上能够正确作答时，把同一步骤放入需要连续切换技能的长程任务后，性能是否会系统性下降；这种下降是否随任务级技能熵 $\mathrm{SkE}(\tau)$ 增大而加剧，并能否归因于模型选错技能类别？
- 将技能熵用作强化学习信号后，模型能否更准确地完成跨技能长程任务；这种收益是否同时出现在不同参数规模的模型上，并能否迁移到现成训练数据？

**实验实现**

评测包含 $8$ 个前沿模型和 $4$ 个开源模型，但节选没有给出完整名单。开源模型通过 vLLM 推理，温度为 $0.7$、top-$p$ 为 $0.9$，生成上限为 $16\mathrm{K}$ tokens；前沿模型使用供应商默认 API，不覆盖采样参数。Cross-Skill 条件把完整场景和 $L$ 个步骤问题置于单个提示中，Single-Skill 条件则在无外围场景的情况下独立询问每一步，并通过附录 D.2 的正则模板解析逐步答案。技能熵由固定参考模型计算，使同一难度尺度可用于比较不同被评模型。可验证领域依据答案自动评分；开放式领域由 Claude-opus-4.7 按逐步准则评分，并以每领域 $200$ 个样本、三名人工标注者进行一致性验证。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 图 5 给出的典型失败模式是：某一步在脱离上下文、单独作答时能够解决，但放入跨技能任务后，模型先把它归入错误的技能领域，随后给出错误答案。分组统计显示，技能领域判断错误时的正确率远低于判断正确时；这把抽象的“长程推理失败”具体化为技能路由错误，但节选没有提供单个题目的完整提示、模型推理链和答案，因而不能进一步判断错误发生在技能识别、前序状态继承还是具体求解环节。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：工作同时提出跨技能长程推理基准与技能熵度量，并以可验证步骤奖励进行强化学习后训练。; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`d92343dd758375e9dc4273e5bd1d77f0061bac4ad078083067a6e32df9e36bf9`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
