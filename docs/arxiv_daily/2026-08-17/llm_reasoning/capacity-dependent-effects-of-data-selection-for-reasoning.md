---
title: "[论文解读] Capacity-Dependent Effects of Data Selection for Reasoning"
description: "[arXiv 2608.13721][LLM Reasoning] 本文重新审视“应优先选择学生模型高似然响应进行推理监督微调”的经验规则，指出数据选择效果取决于学生模型容量与训练时长，并呈现高似然数据“前期拟合快”、低似然数据在大模型上“后期收益高”的容量依赖规律。"
arxiv_id: "2608.13721"
announcement_date: "2026-08-17"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-17T02:01:58.447802+00:00"
source_sha256: "a130d9cc6c7a51d52743c09497cad339855787648c9b2e46ab9b900c4489bf06"
tags:
  - "LLM Reasoning"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.13721</p>

# Capacity-Dependent Effects of Data Selection for Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-17</span>
<span><strong>作者</strong> Cuong Dang, Hoang Anh Just, Ruoxi Jia</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Department of Electrical and Computer Engineering</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13721) · [PDF 下载](https://arxiv.org/pdf/2608.13721) · **关键词** LLM Reasoning<br>


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

本文重新审视“应优先选择学生模型高似然响应进行推理监督微调”的经验规则，指出数据选择效果取决于学生模型容量与训练时长，并呈现高似然数据“前期拟合快”、低似然数据在大模型上“后期收益高”的容量依赖规律。

**不用术语来说**：同一道推理题可能有多种正确回答：有些回答接近学生模型已经会生成的内容，容易学习；另一些回答与其当前行为差距较大，学习更困难但可能包含更强的推理方式。训练者需要决定应选哪类回答作为示范，但现有经验并未说明这一选择是否应随模型大小和可用训练时间改变。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者通过覆盖 1.5B 至 8B 参数学生模型的受控数学推理实验，挑战高似然监督普遍最优的假设，并提出容量依赖的“Fast-Fit/Slow-Gain”现象：高似然数据通常带来更快、更稳定的早期提升，低似然数据则可能在容量较大且训练充分时产生更高的后期收益。
- 作者从学习动态与容量受限蒸馏的角度解释该现象，将迁移成效归因于学生容量、学生与教师之间的知识差距、数据覆盖空间及初始化等因素的共同作用，从而把数据选择转化为需要联合考虑模型容量与计算预算的问题。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大语言模型通常先在大规模文本上进行预训练，再通过监督微调（SFT）学习特定的指令遵循和推理行为。本文研究推理型 SFT 中的响应选择问题：对于同一条指令，教师模型可以生成多个难度不同的候选回答，研究者需要从中选择一个作为学生模型的训练监督。核心比较是，选择更符合学生当前分布的高似然回答，是否始终优于选择较难复现的低似然回答；其中，似然表示学生模型在给定指令下赋予某个回答的条件概率。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**监督微调（SFT）**

SFT 使用成对的指令和目标回答训练模型，使模型提高生成指定行为或任务答案的能力。本文中的目标回答主要由更强的教师模型生成，学生模型通过模仿这些回答学习推理。

</div>
<div class="concept-item" markdown="1">

**教师—学生知识蒸馏**

知识蒸馏是让能力较弱的学生模型学习能力较强的教师模型输出的过程。本文并非直接复制教师的完整概率分布，而是从多个教师回答中选择样本，再用标准 SFT 训练学生。

</div>
<div class="concept-item" markdown="1">

**条件似然与数据选择**

给定指令 $x$ 时，学生模型对回答 $y$ 的条件似然 $pi_{9theta}(yinom{|}x)$ 表示其认为该回答出现的可能性；似然越高，回答越接近学生当前的生成分布。数据选择就是依据这一数值，在同一指令的候选回答中选择高似然或低似然样本进行训练。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

设指令池为 $9mathcal{Q}=9{x_i}_{i=1}^{N}$，其中每个指令 $x_i$ 由一个或多个更强教师模型生成若干候选回答，形成候选集合 $9mathcal{A}_i$。学生模型初始化参数为 $9theta_0$，其条件分布为 $9pi_{9theta_0}(ybinom{|}x_i)$；任务是在每条指令的候选集合中选择一个回答，构造训练集 $9mathcal{D}$，再通过 SFT 更新学生参数 $9theta$。论文重点比较两种设置：对每条指令选择学生初始模型条件似然最高的回答，得到 $9mathcal{D}_{9textrm{high}}$；或选择条件似然最低的回答，得到 $9mathcal{D}_{9textrm{low}}$。实验假设教师回答质量足以提供有价值的推理监督，并考察学生模型容量和训练时长如何改变两类数据的效果。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{Q}=\{x_i\}_{i=1}^{N}$**

指令池；$x_i$ 是第 $i$ 条指令，$N$ 是指令总数。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{A}_i$**

指令 $x_i$ 的候选回答集合；候选回答由教师模型生成，并可能来自多个教师或同一教师的多次生成。

</div>
<div class="notation-item" markdown="1">

**$\pi_{\theta}(y\mid x)$**

参数为 $9theta$ 的学生或教师语言模型在给定指令 $x$ 时生成回答 $y$ 的条件概率分布。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{D}_{\mathrm{high}},\mathcal{D}_{\mathrm{low}}$**

分别表示按学生初始模型选择最高似然回答和最低似然回答构造的 SFT 数据集；下标 $9mathrm{high}$ 与 $9mathrm{low}$ 表示选择规则。

</div>

</div>

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

推理监督微调中的候选响应具有明显异质性：它们与学生模型当前分布的匹配程度不同。逐指令选择哪一个响应，会影响优化稳定性、样本效率以及最终获得的推理行为；因此，训练者需要一种能够根据学生能力和训练预算选择监督难度的可靠原则。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **高似然响应选择，以 GRAPE 为代表**：对每条指令，用目标学生模型计算候选响应的生成概率，并选择概率最高、最接近学生当前分布的响应进行微调。其依据是这类示范更容易被学生吸收，而且选择规则相对简单、额外开销较低。
- **困难样本优先的数据选择**：优先训练学生当前赋予较低对数似然的样本，因为这类样本通常提供更强的梯度信号，能够迫使模型突破已有能力边界；相应地，已被模型较好掌握的高似然样本可能被视为信息量不足。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 高似然方法隐含“容易吸收就更有效”的一般化假设，但原有证据不足以说明该结论能否跨模型容量和训练时长成立；若直接将其作为统一规则，可能使容量较大的学生长期停留在接近自身原有分布的监督上，错失更具挑战性的教师知识。
- 困难样本优先的观点强调低似然样本能够推动能力扩展，却没有充分处理学生是否具备吸收这些监督的容量。论文观察到，小模型面对与当前策略距离较远的数据时，可能无法有效趋近教师分布，反而出现训练不稳定、重复或浅层输出，因此“越难越有价值”同样不能作为无条件规则。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

两类既有原则给出了相反的数据偏好，但缺少一个统一解释来刻画监督难度、学生模型容量与训练预算之间的交互关系。尤其尚不清楚：高似然数据的优势究竟是普遍的最终性能优势，还是仅体现为早期优化更快；低似然数据又需要多大的学生容量和多长训练时间，才能从难以吸收的信号转化为有效的教师知识迁移。

</div>
<div markdown="1"><span>核心问题</span>

对于推理监督微调，高似然数据是否始终优于低似然数据；如果不是，模型容量和训练时长如何决定两类数据分别在何时有效，以及这种容量依赖现象背后的学习动态与一般机制是什么？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把低似然响应理解为距离学生当前策略更远的监督信号。容量较小的模型可表示和优化的行为范围有限，更适合沿着高似然示范做局部、快速且稳定的改进；容量较大的模型则有更充分的表示能力和优化空间，虽然需要更长时间跨越与教师之间的分布距离，却可能借助低似然示范学到当前分布之外的推理方式。因此，合理的数据选择不应固定偏好“容易”或“困难”，而应使监督难度与学生可吸收能力及训练时间相匹配。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文采用“受控数据选择实验 + 双视角动态诊断 + 线性蒸馏理论”三层方法研究教师回答的学生似然与模型容量之间的关系。首先，对每个数学问题收集两个强教师模型生成的多个候选回答，并用尚未微调的学生模型计算每个回答的条件似然；随后分别选择最高似然回答构成$\D_{\mathrm{high}}$、选择最低似然回答构成$\D_{\mathrm{low}}$，在数据规模和问题集合相同的条件下进行监督微调。作者比较不同容量学生在首个训练轮次和完整五轮训练中的正确率，并进一步从教师模型和原始学生模型两个参照系测量生成答案的对数似然变化，以区分“更接近教师”与“偏离初始化分布”这两种现象。
理论部分将上述过程抽象为教师与学生之间的二分类知识蒸馏：训练数据只能暴露教师知识差异在数据张成空间中的部分，而低容量学生还受到可表示子空间$\mathcal{F}$的额外限制。因此，低似然回答虽然可能包含更多超出学生当前分布的教师知识，但这些知识只有同时落入数据可见方向和学生可表示方向时才能被吸收。通俗地说，高似然样本更像学生当前能够读懂的教材，因而学习快；低似然样本可能包含更先进的解法，大模型经过更长训练后能从中获益，小模型则可能只能模仿表面形式或陷入重复。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造教师回答候选池

对每个问题$\x_i$，从每个教师$\T\in\mathcal{T}$收集一个或多个生成回答$\y_i^{(T,j)}$，形成该问题的候选回答集合。不同选择策略共享同一问题池，从而把主要实验变量限制为所选回答相对学生的似然高低。

<div class="method-step__io" markdown="1">

**输入**：MATH12K中的指令池$\mathcal{Q}=\{x_i\}_{i=1}^{N}$，以及教师集合$\mathcal{T}$；实验教师为Qwen/Qwen2.5-72B和google/gemma-3-27b-it。<br>
**输出**：每个问题对应的候选集合$\mathcal{A}_i=\{y_i^{(T,j)}\}$。

</div>

**直观理解**：同一道题先准备多份由强模型写出的解答，之后再决定哪一份最适合某个学生。这样比较的是“教材版本”的差异，而不是题目数量或题目内容的差异。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按基础学生似然进行对照选择

使用基础学生参数$\theta_0$为每个候选回答评分，并分别取似然最高的回答$\y_i^{\mathcal{H}}$和似然最低的回答$\y_i^{\mathcal{L}}$。论文式(4)和式(5)把候选集记为$\R_i$，而前文式(1)记为$\mathcal{A}_i$；两者在所给章节中均承担逐题候选池的角色。

<div class="method-step__io" markdown="1">

**输入**：候选回答集合$\mathcal{A}_i$以及未微调学生的条件分布$\pi_{\theta_0}(y\mid x_i)$。<br>
**输出**：逐题配对且规模相同的$\mathcal{D}_{\mathrm{high}}$与$\mathcal{D}_{\mathrm{low}}$。

</div>

**直观理解**：高似然回答是学生在训练前已经比较熟悉、容易复现的解法；低似然回答则更偏离学生原有行为。这个设计直接检验“容易学的数据”和“新颖但困难的数据”对不同容量学生的影响。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 监督微调与分阶段评估

分别在$\mathcal{D}_{\mathrm{high}}$和$\mathcal{D}_{\mathrm{low}}$上最小化教师回答的负对数似然。每轮保存四个检查点，分别汇总首轮四个检查点中的最佳结果，以及五轮共二十个检查点中的最佳结果，以区分早期学习速度和较长训练后的收益。

<div class="method-step__io" markdown="1">

**输入**：五种学生模型与两套选择数据；学生包括Qwen2.5-1.5B、Qwen2.5-3B-Instruct、Qwen2.5-Math-7B、Qwen3-4B和Qwen3-8B。<br>
**输出**：每种模型容量、数据选择策略和训练阶段对应的微调检查点及数学任务$\operatorname{pass@1}$结果。

</div>

**直观理解**：首轮结果回答“哪种数据让模型学得更快”，五轮结果回答“给足训练时间后哪种数据的最终价值更高”。这种分阶段比较是识别论文所称Fast-Fit与Slow-Gain现象的关键。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 双视角学习动态诊断

教师视角用Gemma对生成回答计算对数似然，观察学生输出是否逐渐接近教师分布；原始模型视角则用微调前的学生评估生成回答，测量训练后行为相对初始化分布的偏移、离散程度及其跨数据集泛化。两种参照系共同避免把“偏离原模型”直接误判为“学到了教师知识”。

<div class="method-step__io" markdown="1">

**输入**：不同训练检查点在MATH12K训练集和AMC测试集上生成的回答，以及教师模型和各学生的原始基础模型。<br>
**输出**：按模型容量和数据选择策略划分的教师对齐轨迹与原始分布偏移轨迹。

</div>

**直观理解**：一个视角检查学生是否更像老师，另一个视角检查学生离原来的自己有多远。只有同时观察二者，才能判断低似然训练是在获得新知识，还是仅造成不稳定漂移。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 逐题高似然与低似然回答选择

$$
\mathcal{D}_{\mathrm{high}}=\{(x_i,y_i^{\mathcal H})\}_{i=1}^{N},\quad y_i^{\mathcal H}=\arg\max_{y\in R_i}\pi_{\theta_0}(y\mid x_i);\qquad \mathcal{D}_{\mathrm{low}}=\{(x_i,y_i^{\mathcal L})\}_{i=1}^{N},\quad y_i^{\mathcal L}=\arg\min_{y\in R_i}\pi_{\theta_0}(y\mid x_i)
$$

**符号说明**

- $\mathcal{D}_{\mathrm{high}}$：由每道题的最高学生似然教师回答组成的训练集
- $\mathcal{D}_{\mathrm{low}}$：由每道题的最低学生似然教师回答组成的训练集
- $x_i$：第$i$个训练问题或指令
- $R_i$：式(4)和式(5)中第$i$个问题的候选回答集合；前文使用$\mathcal{A}_i$表示候选集合
- $y_i^{\mathcal H}$：第$i$个问题下基础学生赋予最高条件似然的回答
- $y_i^{\mathcal L}$：第$i$个问题下基础学生赋予最低条件似然的回答
- $\pi_{\theta_0}(y\mid x_i)$：参数为$\theta_0$的微调前学生在问题$x_i$条件下生成完整回答y的概率
- $N$：问题总数

<div class="equation-explanation" markdown="1">

**直观理解**：该式建立论文的核心实验干预：对每一道相同的问题，只替换学生最熟悉或最陌生的教师回答。高似然组测试分布匹配、容易优化的监督，低似然组测试偏离学生当前能力但可能包含新增教师知识的监督。<br>
**原文位置**：第3节，式(4)和式(5)

</div>

</div>

<div class="equation-block" markdown="1">

#### 低容量学生的渐近蒸馏解

$$
\hat{\mathbf{w}}=\mathbf{w}_0+P_{\mathbf{X}_{\mathcal F}}(\mathbf{w}_*-\mathbf{w}_0)
$$

**符号说明**

- $\hat{\mathbf{w}}$：训练时间趋于无穷时低容量学生收敛到的参数
- $\mathbf{w}_0$：学生训练前的初始化参数向量
- $\mathbf{w}_*$：教师线性分类器的参数向量
- $\mathcal F$：低容量学生能够表示的可行参数子空间
- $\mathbf{X}_{\mathcal F}$：训练数据张成空间投影到学生可行子空间$\mathcal F$后得到的空间
- $P_{\mathbf{X}_{\mathcal F}}$：到空间$\mathbf{X}_{\mathcal F}$的正交投影算子
- $\mathbf{w}_*-\mathbf{w}_0$：教师与初始学生之间的参数知识差异

<div class="equation-explanation" markdown="1">

**直观理解**：最终学生不是直接变成教师，而只沿着“训练数据揭示、并且学生有能力表示”的方向缩小与教师的差距。若低似然样本揭示的知识主要落在$\mathcal{F}$之外，这些监督即使信息丰富，也不会有效转化为小模型的能力。<br>
**原文位置**：第6节，定理6.2，式(10)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：经验实验采用标准监督微调目标，即在所选数据集$\mathcal{D}$上最小化回答级负对数似然$-\sum_{(x,y)\in\mathcal{D}}\log\pi_{\theta}(y\mid x)$，从基础参数$\theta_0$更新到微调参数$\theta$。因此，高、低似然实验的优化形式相同，区别仅在目标回答$\y$来自$\mathcal{D}_{\mathrm{high}}$还是$\mathcal{D}_{\mathrm{low}}$；这使性能差异可主要归因于监督内容与学生初始分布的匹配程度。理论分析则使用教师软标签$\y_i=\sigma(\mathbf{w}_*^{\top}\mathbf{x}_i)$下的归一化二元交叉熵，并用连续时间梯度流研究收敛极限；该理论目标用于解释知识迁移方向，不是实验中LLM监督微调目标的逐项复现。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 学生条件似然选择器**

选择器使用微调前学生分布$\pi_{\theta_0}(y\mid x_i)$，在每个问题内部对教师候选回答排序；最高与最低似然策略只改变回答选择，不改变问题索引$\i$。似然在这里是学生对完整回答的条件概率，论文所给节选未进一步说明是否进行了长度归一化。

> 直观理解：它把学生自身当作难度评估器：学生本来就认为自然的回答进入高似然组，学生认为陌生的回答进入低似然组。由于选择是逐题完成，两组数据仍覆盖相同问题。

**2. 容量—训练预算对照框架**

框架横向比较约1.5B至8B参数规模的学生，纵向比较首轮最佳检查点与五轮内最佳检查点。该设计把模型容量和优化时长视为影响数据价值的两个条件变量，而不是假定某一种似然选择对所有学生都最优。

> 直观理解：同一份困难教材对小模型、大模型以及不同学习时长可能产生不同效果。论文因此不只看最终分数，还检查优势出现得早还是晚。

**3. 可行子空间投影机制**

理论模型用$\mathcal{F}\subseteq\mathbb{R}^{d}$表示低容量学生能够实现的参数方向，并用$\P_{\mathbf{X}_{\mathcal{F}}}$表示投影到“数据暴露且学生可表示”的方向。该结论来自线性二分类、教师sigmoid软标签和梯度流设定，是对大语言模型现象的机制化解释，而非对非线性Transformer训练的直接等价证明。

> 直观理解：数据包含某种教师知识并不意味着学生就能学会；知识还必须落在学生能够表达的范围内。这个模块解释了为什么低似然数据可能对大模型有长期价值，却让小模型停留在重复和浅层模仿。

**训练与推理**

训练阶段先固定教师回答候选池，再针对每一种学生的初始模型单独计算候选似然，因此同一回答可能对不同容量学生具有不同的高低似然身份。随后从每题选择一个目标回答，分别训练高似然版本和低似然版本；每轮保存四个检查点，首轮分析从四个检查点取最佳值，完整训练分析从五轮共二十个检查点取最佳值。这个“区间内最佳”口径适合观察两类数据何时达到峰值，但它比较的是给定检查点搜索预算下的最佳表现，并非固定训练步数的末尾模型。
评估或推理阶段以温度$0.6$生成答案，用标准$\operatorname{pass@1}$判断一次生成能否正确解题，并在十个数学相关数据集上测试迁移。动态诊断另行收集各检查点生成的回答：Gemma教师似然用于估计输出对教师分布的接近程度，基础学生似然用于估计输出偏离原始分布的程度；训练集MATH12K与测试集AMC并列观察，用于区分训练适配和测试泛化。

**复现信息**

复现实验所必需的已报告信息包括：训练数据为MATH12K；教师为Qwen/Qwen2.5-72B和google/gemma-3-27b-it；主要学生为Qwen2.5-1.5B、Qwen2.5-3B-Instruct、Qwen2.5-Math-7B、Qwen3-4B和Qwen3-8B；训练持续五轮且每轮保存四个检查点；推理温度为$0.6$。评估覆盖AIME24、AMC、CHMATH、Gaokao、GPQA、GradeSchool、KAOYAN、MATH500、Minerva和Olympiad Bench，指标为$\operatorname{pass@1}$。
所给节选未明确报告每个教师对每道题生成多少回答、候选回答是否经过正确性过滤、似然是否按回答长度归一化、优化器与学习率、批大小、上下文长度、随机种子或多次运行方差；原文指出训练超参数位于附录B.1，但该附录内容未包含在节选中。这些信息会影响长短回答的似然排序、训练稳定性及结果可重复性，正式复现时必须回查原文附录。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MATH12K：数学推理训练数据集。两种教师模型为其中每个问题生成答案，再依据教师对答案的似然进行数据选择；选出的高似然或低似然子集用于全参数监督微调。当前节选仅给出名称，未明确报告具体样本数、划分方式及各子集规模。
- AMC：数学竞赛测试集。在学习动态分析中充当测试集，用于比较不同训练检查点生成答案的分布变化。当前节选未明确报告具体年份、题目数量及评测划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**教师模型对生成答案的对数似然**

用 Gemma 教师模型衡量学生在不同检查点生成的答案与教师分布的接近程度。对数似然越高，等价地负对数似然损失越低，通常表示学生输出越符合教师模型的分布。 （若目标是教师对齐，则对数似然越高或教师损失越低越好；但该指标只表示分布接近，不直接等同于数学答案正确率。）

</div>
<div class="metric-item" markdown="1">

**基础模型对生成答案的对数似然**

由每个学生对应的原始基础模型评价微调后生成的答案，用来刻画微调行为偏离初始分布的程度。 （没有统一的越高越好方向。较低似然或较高损失说明偏离原模型更远，但这种偏移既可能代表学到了新推理行为，也可能代表不稳定漂移。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 教师视角下比较 1.5B、3B 和 7B 学生使用高似然或低似然数据训练后的损失动态

<div class="result-value" markdown="1">

作者报告明显的容量依赖模式：1.5B 学生无法通过任一选择策略有效靠近教师；3B 学生主要从低似然数据中获得教师对齐收益；7B 学生则能在高、低似然两种训练条件下都降低教师损失。

</div>

低似然样本并非天然更难或更差，它们对具备足够容量的学生可能包含更有价值的教师知识。小模型即使接触这些数据，也可能没有能力吸收其中的行为。该结果支持“数据价值取决于学生容量”，但教师损失下降只证明输出更像教师，不能单独证明答案更正确，也不能建立模型容量与效果之间的因果机制。

<div class="result-source" markdown="1">

来源：Section 5, Learning Dynamics under Teacher View；Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Overall, these results suggest that the ability of likelihood-based data selection to pull the student toward the teacher depends strongly on model capacity: smaller students struggle to approach the teacher at all, medium-sized students benefit particularly from low-likelihood data, and larger students can align with the teacher under either selection strategy.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 原始基础模型视角下比较不同容量学生在低似然训练后的分布偏移稳定性

<div class="result-value" markdown="1">

作者观察到，1.5B 学生的损失分布更宽且更发散，但仍与初始范围大量重叠；3B 学生更明显地离开原始分布；7B 学生相较 3B 的损失方差更小，表现为更集中、更稳定的适应。

</div>

相同的低似然训练会在不同容量上产生不同性质的变化：小模型可能一部分样本改变很大、另一部分仍停留在原行为；中等模型能够形成更清楚的整体迁移；更大模型则可能以较集中的方式吸收新行为。这里的“稳定”来自损失分布形态，而非多次独立训练的统计方差，因此不能据此断言训练过程具有更强的随机稳定性。

<div class="result-source" markdown="1">

来源：Section 5, Learning Dynamics under Original Model View；Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For the 7B model, the loss variance of answers generated after low-likelihood training becomes smaller than for the 3B model, suggesting that the larger model adapts in a more stable and focused way rather than drifting broadly.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### AMC 测试集上比较高似然与低似然训练造成的输出分布差异

<div class="result-value" markdown="1">

作者报告，高、低似然训练在 1.5B 学生上的测试分布差异较小，而这一差异会随学生规模增大而扩大；作者据此认为，大模型更能把数据选择策略的影响表达到测试输出中。

</div>

若学生容量不足，两种训练集即使内容不同，也可能产生近似的最终行为；容量增加后，模型才有能力形成可区分的学习结果。这表明数据选择策略应与目标学生模型联合评估，不能只依据教师分数决定。不过，分布差异变大本身没有方向性：它说明策略影响更明显，却不自动意味着低似然或高似然策略具有更高任务正确率。

<div class="result-source" markdown="1">

来源：Section 5, Learning Dynamics under Original Model View；Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the test set, the difference between the 1.5B models trained on high- and low-likelihood data is relatively small, but this gap widens as model size increases.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前节选未提供主要性能表、具体正确率或统计显著性信息，也没有报告重复运行、置信区间和误差条；因此可以确认的是损失动态与作者的定性观察，无法从所给材料核验性能提升幅度、稳定性或不同教师之间的一致程度。
- 学习动态以教师或基础模型对生成答案的似然为代理指标。教师对齐、偏离原模型和任务正确性并不等价；同时，高低似然子集可能在答案长度、题目难度、解法风格或正确性上存在混杂，当前节选没有展示控制这些因素的实验。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 高似然数据训练：选择教师模型赋予较高似然的答案进行监督微调，代表更贴近教师常见输出的训练数据；它与低似然选择的对照用于检验“更符合教师偏好”是否一定更适合学生。
- 低似然数据训练：选择教师模型赋予较低似然的答案进行监督微调。它与高似然数据在相同学生模型上的比较，用于隔离似然选择方向的影响。
- 不同学生容量：主要比较 Qwen2.5-1.5B、Qwen2.5-3B-Instruct 和 Qwen2.5-Math-7B，并另外报告 Qwen3-4B、Qwen3-8B 等模型。跨容量比较用于判断数据选择结论能否从小模型直接外推到大模型。
- 不同教师模型：Qwen2.5-72B 与 Gemma-3-27B-IT 均用于为 MATH12K 问题生成答案。该设置用于考察现象是否依赖单一教师；但当前节选没有提供两位教师的逐项对照结果。

**实验想回答的问题**

- 按教师模型似然选择监督微调数据时，高似然数据与低似然数据对推理模型的影响是否随学生模型容量而变化？
- 不同容量的学生模型接受高似然或低似然数据训练后，其输出相对教师分布和原始基础模型分布如何移动，这些动态能否解释泛化表现的差异？

**实验实现**

教师模型 Qwen2.5-72B 和 Gemma-3-27B-IT 为 MATH12K 中的问题生成答案；训练数据随后按教师似然分成高似然与低似然选择条件。各学生模型从相应预训练或指令模型初始化，在选定子集上进行全参数监督微调。学习动态实验跨训练检查点采样学生答案，并分别从教师视角和原始基础模型视角计算其对数似然：前者判断学生是否靠近教师分布，后者判断微调后行为偏离初始分布的程度。Figure 2 同时覆盖 AMC 测试集与 MATH12K 训练集上的教师视角动态，Figure 3 覆盖相同数据角色下的基础模型视角动态。当前节选没有完整给出训练轮数、优化器、学习率、解码参数、随机种子、子集规模、重复实验次数或误差区间，也未提供主要任务正确率的定义与数值。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 固定似然选择思路，改变学生容量为 1.5B、3B 和 7B | 容量变化使低似然数据的作用从“无法明显拉近教师”转为“帮助靠近教师”，并在 7B 学生上表现为高、低似然训练均能降低教师损失。 | 该跨容量对照隔离的是学生表达与吸收能力对数据价值的调节作用，是论文容量依赖结论的核心证据。由于模型之间除参数规模外还可能存在基础训练、指令调优或数学专门化差异，尤其所列 7B 模型为 Math 变体，因此它不是严格只改变参数量的受控消融。 | Section 5, Observation 4 (Capacity-Dependent Teacher Alignment)；Figure 2<br><span class="experiment-evidence">Low-likelihood data moves larger models closer to the teacher but fails to do so for small models.</span> |
| 固定学生规模与监督微调方式，对比高似然数据和低似然数据 | 高、低似然选择在小模型上的测试输出差异不明显，但随着模型增大，两种选择产生的行为差异更清楚；低似然训练造成的基础模型分布偏移也随容量呈现不同的宽度与稳定性。 | 该对照主要隔离训练数据在教师似然轴上的选择方向，用于检验“教师更偏好的答案是否总是更好的训练样本”。结果否定了统一答案，但当前节选未说明两类子集是否严格等量，也未排除答案长度、难度、正确性和主题构成等伴随差异，因此不能把全部变化唯一归因于似然高低。 | Section 5, Observation 5 (Capacity-Dependent Distribution Shift and Generalization)；Figure 3<br><span class="experiment-evidence">As model size increases, fine-tuned behavior becomes more stable, generalization improves, and the distinction between high-likelihood and low-likelihood training becomes more pronounced.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Studies how model capacity changes the effect of training-data selection on reasoning performance.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`a130d9cc6c7a51d52743c09497cad339855787648c9b2e46ab9b900c4489bf06`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
