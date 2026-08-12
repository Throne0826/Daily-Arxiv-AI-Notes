---
title: "[论文解读] ELMER: Evolutionary Language Model that Explores and Refines"
description: "[arXiv 2608.10196][LLM Reasoning] 本文研究如何让程序进化中的变异强度从不可控的语法改动，转变为可按低、中、高等级调节且由实际执行行为校准的语义移动。"
arxiv_id: "2608.10196"
announcement_date: "2026-08-12"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-12T03:09:26.738406+00:00"
source_sha256: "eb4e3f786f5ab7578f3f82560d98806243d70970e285c6baab1521a080f1cef0"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "遗传编程"
  - "大语言模型"
  - "程序进化"
  - "语义变异"
  - "行为位移"
  - "直接偏好优化"
  - "领域特定语言"
  - "交易策略搜索"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.10196</p>

# ELMER: Evolutionary Language Model that Explores and Refines

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-12</span>
<span><strong>作者</strong> Matthew Siper, Ahmed Khalifa, Julian Togelius</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Nof1, New York University；Nof1, University of Malta</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.10196v1) · [PDF 下载](https://arxiv.org/pdf/2608.10196v1) · **关键词** 遗传编程, 大语言模型, 程序进化, 语义变异, 行为位移, 直接偏好优化, 领域特定语言, 交易策略搜索<br>


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

本文研究如何让程序进化中的变异强度从不可控的语法改动，转变为可按低、中、高等级调节且由实际执行行为校准的语义移动。

**不用术语来说**：程序进化会反复修改策略程序并保留表现更好的版本，但传统方法通常只能在修改执行后判断它是否有效，无法事先可靠控制新策略与原策略究竟会有多大差别。代码改动量也不能准确回答这个问题：改一个比较符号可能改变几乎所有决策，而重写一大段代码却可能产生完全相同的动作。因此，有限评估预算可能被过小、无效或过于激进的变异浪费。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出一种以执行轨迹为依据的条件变异思路：在自然语言策略描述上请求低、中或高强度的语义变异，再将结果编译为有类型的交易领域专用语言 GPTL；父代与子代在同一历史市场数据上执行，其动作序列分歧用于刻画实际行为位移。
- 作者将语义变异、自然语言到 GPTL 的编译以及 GPTL 到自然语言的翻译统一到一个任务条件化的 Qwen3-8B 模型中，并以行为监督微调和共同父代偏移的直接偏好优化训练变异强度控制，从而把适应度选择与变异幅度学习分开。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于遗传编程与大语言模型引导的程序搜索交叉方向。遗传编程通过变异产生候选程序，再依据程序执行后的适应度进行选择；但常用的词元、语法树节点或子树编辑量只衡量语法变化，不能可靠反映策略行为变化。本文以金融交易策略为测试场景，将用于变异的表示与用于执行评估的表示分开：搜索在标准化自然语言策略描述上进行，学习得到的编译器再把描述转换为有类型的遗传编程交易语言程序，并在固定历史市场轨迹上确定性执行。核心问题不是仅让模型生成有效或高适应度的程序，而是让低、中、高三档变异强度能够对应有序且允许重叠的实际行为位移。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**遗传编程**

遗传编程是一类直接搜索可执行程序的进化算法：它对父程序进行变异，并根据候选程序执行后的适应度保留较优个体。程序表示和变异算子共同决定搜索能够到达哪些邻域。

</div>
<div class="concept-item" markdown="1">

**行为位移**

行为位移衡量父策略与子策略在相同输入轨迹上采取的动作有多大差异，而不是比较两段程序文本改了多少。本文通过父子程序在同一历史市场数据上执行所得动作序列之间的不一致来确定该位移。

</div>
<div class="concept-item" markdown="1">

**直接偏好优化**

直接偏好优化通过成对的“偏好输出”和“非偏好输出”调整语言模型；本文采用带样本对相关间隔的 oDPO，使偏好更新强度能够随差异大小变化。这里的偏好并非简单表示哪个子程序质量更高，而是表示同一父程序产生的候选子程序中，哪个执行位移更符合请求的变异强度。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括父策略的标准化自然语言描述、任务条件以及请求的变异强度 $r\in\{\mathrm{low},\mathrm{medium},\mathrm{high}\}$；模型输出变异后的自然语言子策略，并将其编译为类型正确的 GPTL 程序。父程序与子程序在同一段固定历史市场数据上确定性回放，由两者动作序列的不一致程度得到实际行为位移 $d(p,c)$；外层进化仍以交易适应度选择候选，而该位移用于训练和校准变异算子。问题假设策略端点能够被编译、执行并比较行为，同时严格按时间划分留出数据；目标是在有限搜索预算下，使请求强度能预测实际位移，并保持搜索高适应度策略的能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$p$**

父交易策略，既可对应自然语言描述，也可对应其编译后的可执行 GPTL 程序。

</div>
<div class="notation-item" markdown="1">

**$c$**

由条件变异算子从父策略生成的子交易策略。

</div>
<div class="notation-item" markdown="1">

**$r\in\{\mathrm{low},\mathrm{medium},\mathrm{high}\}$**

用户或搜索过程指定的低、中、高三档目标变异强度。

</div>
<div class="notation-item" markdown="1">

**$d(p,c)$**

父子程序在同一历史市场轨迹上执行时，由动作序列不一致定义的实际行为位移。

</div>

</div>

**直接相关的工作**

- **Transformer Semantic GP（Anthes et al., 2025）**: 该工作使用 Transformer 提出语义相关的遗传编程候选，说明学习式模型可以改善程序变异邻域；本文进一步从父子程序的实际执行差异学习离散强度条件，使提议分布能够控制移动到行为空间中的何种距离。
- **Evolution through LLMs（Lehman et al., 2023）**: 该工作确立了将语言模型用作学习式进化变异算子的思路；本文在此基础上增加执行落地的强度监督，不仅依据适应度评价提议，还专门训练变异算子控制父子策略之间的行为位移。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在交易策略等随机、状态依赖的程序控制任务中，每个候选程序都需要执行和评估，而搜索预算有限。进化算法既要在优良父代附近做保守改进，也要进行较大幅度探索；如果不能预先调节行为变化尺度，就难以合理分配探索与利用，可能破坏已有的有效行为，或产生几乎没有区别的候选策略。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于语法编辑的程序变异**：传统程序搜索通过令牌、语法树节点或子树的替换、插入和删除产生子代，并把编辑数量或子树规模当作变异幅度的近似；候选程序执行后，再由适应度决定是否保留。
- **连续优化中的显式更新尺度**：连续优化器通常通过步长等参数直接控制一次更新在参数空间中的移动距离，为局部搜索和大范围探索提供明确旋钮；论文将这种可控尺度视为程序搜索尚未可靠具备的能力参照。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 语法距离与执行行为距离可能严重错位：很小的比较符修改就可能改变几乎全部动作，而较大重写也可能保持相同动作序列。因此，令牌数、树编辑数或子树大小不能可靠预测变异造成的实际行为变化。
- 传统程序进化主要在执行之后利用适应度判断变异好坏，却缺少在生成之前指定行为变化幅度的机制。其后果是变异算子难以形成稳定的低、中、高探索等级，也难以在固定预算下有意识地平衡保留父代能力与发现新行为。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种以程序实际执行结果为标尺、其请求强度能够预测所实现行为位移的条件变异算子。这个缺口不仅要求定义行为空间中的变异距离，还要求学习从强度条件到可执行子代的映射，并把表示层面的语义修改与确定性执行连接起来。

</div>
<div markdown="1"><span>核心问题</span>

语言模型能否从父代和子代程序的执行轨迹中学会可控的变异尺度，使低、中、高强度请求对应有序但允许重叠的行为位移区间，并由此提高固定预算程序进化的搜索效率？

</div>
<div markdown="1"><span>作者直觉</span>

自然语言更直接表达策略意图，例如调整入场条件、增加风险约束或改变指标组合，因而可能比局部代码编辑更适合控制“改变什么以及改变多少”。模型先在自然语言层面修改策略语义，再编译成可确定执行的 GPTL；随后用父子动作轨迹的分歧而不是文本或代码改动量提供训练反馈。这样，语言负责形成可调的语义变化，程序执行负责检验变化究竟落在多远的行为范围内。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ELMER把可执行交易策略的进化搜索拆成“自然语言变异、程序编译、确定性执行与适应度选择”四个环节。单个全参数微调的Qwen3-8B同时学习三项带任务标识的操作：将GPTL程序翻译为标准化自然语言，将父策略按请求强度$s\in\{\mathrm{low},\mathrm{medium},\mathrm{high}\}$改写为子策略描述，以及把子描述编译成类型化GPTL程序；编译后的父子策略在相同市场状态序列上执行，以四类交易信号的不一致比例$d_{\mathrm{beh}}$衡量真实行为位移。训练先用行为落地的多任务监督微调（SFT）建立领域知识、双向表示转换和条件变异能力，再用共同父代的偏好数据进行偏移式直接偏好优化（oDPO），使请求的强度等级更可靠地对应小、中、大行为变化。

整个设计的关键不是让模型生成“看起来改得少或多”的文本，而是用程序执行结果监督语义变异：自然语言子策略必须先编译并回测，强度由实际交易信号变化决定。推理时，外层进化算法保留父策略及其回测反馈，调用模型生成指定强度的子描述，编译并执行该描述，再根据验证适应度决定保留或淘汰；自然语言负责提供较灵活、可控制的搜索空间，GPTL则负责类型检查、确定执行和客观评价。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造执行落地的多尺度变异监督

对程序施加语法有效的抽象语法树（AST）编辑并保留适应度方向性下降的边，形成退化链；反转长度为一、二、四条边的片段，得到多个尺度上方向性改善的父子程序转移。父子程序在相同窗口执行，并按$d_{\mathrm{beh}}$测量行为位移，随后由GLM 5.2把两端转换为标准化自然语言。

<div class="method-step__io" markdown="1">

**输入**：训练Sharpe比率大于$0.5$的高适应度GPTL策略、GPTL语法及仅含训练数据的市场窗口。<br>
**输出**：同时包含可执行父子程序、标准化自然语言、回测反馈、行为距离和强度标签的监督样本。

</div>

**直观理解**：先故意把较好的策略逐步改差，再把这些过程倒过来，就得到从较差策略向较好策略修改的示例。修改幅度不是按代码字符数判断，而是看修改后实际发出的交易信号改变了多少。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 行为落地的多任务监督微调

对同一个Qwen3-8B检查点进行全参数SFT，使其根据任务条件分别完成编译、翻译或变异；变异提示包含领域原语、父策略的GPTL与自然语言表示、适应度、七项回测统计和请求强度$s$。行为距离按数据分布的等频区间标为低、中、高，并删除近乎无变化及靠近类别边界的转移，再按强度与资产平衡数据。

<div class="method-step__io" markdown="1">

**输入**：条件变异、自然语言到GPTL编译、GPTL到自然语言翻译三类样本，以及每条样本对应的任务提示。<br>
**输出**：具备程序与语言双向转换能力、且能初步按请求强度生成子策略的行为落地SFT模型。

</div>

**直观理解**：这一步让一个模型同时学会“读代码、写代码和改策略”，因此语言中的修改最终能回到可执行程序。删除模糊边界样本，是为了减少同一种行为变化被贴上相邻强度标签所造成的监督噪声。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造共同父代偏好并进行oDPO

对请求强度$s$，把距离该强度经验中心$\mu_s$最近的子策略记为偏好回答$y^+$，把请求类别之外的子策略记为拒绝回答$y^-$；过滤偏好差距过小的配对，并用归一化间隔$m$表示偏好的可信强度。随后最小化oDPO损失，使当前模型相对参考模型更倾向$y^+$，且距离差越明确，要求的偏好优势越大。

<div class="method-step__io" markdown="1">

**输入**：同一父策略下不同强度类别的候选子策略、各子策略与父策略的行为距离，以及冻结的SFT参考模型$\pi_{\mathrm{ref}}$。<br>
**输出**：最终的条件语义变异模型，其低、中、高请求在行为空间中形成有序但允许重叠的位移分布。

</div>

**直观理解**：模型面对的是“同一个父策略应该选哪个孩子”的成对判断，因此比较不会被不同父策略的难度混淆。oDPO不仅告诉模型哪个孩子更合适，还根据两个孩子与目标强度的差距决定这条偏好应当有多强。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 闭环进化搜索与执行评价

模型从$p_\theta(\cdot\mid x_p,s)$采样子描述$x_c$，编译器$C$将其映射为GPTL程序并执行回测；外层算法依据验证适应度保留或拒绝子代，并继续迭代。常规语言进化直接继承已生成的子描述，同时保存其编译程序作为评价产物，不在每一代重复执行程序到语言的翻译。

<div class="method-step__io" markdown="1">

**输入**：父策略自然语言描述$x_p$、其GPTL程序与回测反馈、请求强度$s$以及外层进化算法的搜索预算。<br>
**输出**：一系列可执行、经过适应度筛选的策略，以及固定预算内找到的最佳策略。

</div>

**直观理解**：语言模型负责提出不同幅度的策略修改，编译器和回测器负责检查这些想法是否可执行、效果是否更好。最终决定子代生存的是外层优化中的适应度，而不是模型对文本质量的自我判断。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 父子策略的行为位移

$$
d_{\mathrm{beh}}(\pi_a,\pi_b)=\frac{1}{N}\sum_{t=1}^{N}\mathbb{I}\!\left[\pi_a(s_t)\neq\pi_b(s_t)\right]
$$

**符号说明**

- $d_{\mathrm{beh}}$：两个策略在共享评价轨迹上的行为位移，即原始交易信号不一致的时间比例。
- $\pi_a,\pi_b$：待比较的两个可执行策略；在训练变异监督时通常分别对应父策略与子策略。
- $s_t$：共享市场状态序列在时间步t的状态。
- $N$：共享评价轨迹包含的市场状态总数。
- $\mathbb{I}[\cdot]$：指示函数；括号内条件成立时取1，否则取0。

<div class="equation-explanation" markdown="1">

**直观理解**：该式逐时检查两个策略输出的四位信号向量是否完全相同，再对不相同的时刻求比例。它是强度标签、共同父代偏好和单调性验证的共同依据，把语言修改幅度锚定到真实可执行行为。<br>
**原文位置**：第3节“Behavior-Space Step Size”，式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 带偏好间隔偏移的直接偏好优化损失

$$
\mathcal{L}_{\mathrm{oDPO}}=-\mathbb{E}\!\left[\log\sigma\!\left(\beta\Delta r_\theta-\lambda m\right)\right],\quad \Delta r_\theta=r_\theta(y^+\mid x)-r_\theta(y^-\mid x),\quad r_\theta(y\mid x)=\log\pi_\theta(y\mid x)-\log\pi_{\mathrm{ref}}(y\mid x)
$$

**符号说明**

- $\mathcal{L}_{\mathrm{oDPO}}$：在共同父代偏好对上优化的oDPO期望损失。
- $x$：包含父策略、反馈、领域信息和请求变异强度的条件输入。
- $y^+,y^-$：分别为更接近请求强度中心的偏好子策略，以及位于请求类别之外的拒绝子策略。
- $\pi_\theta$：正在通过oDPO优化的条件变异模型。
- $\pi_{\mathrm{ref}}$：冻结的行为落地SFT参考模型。
- $r_\theta(y\mid x)$：当前模型相对参考模型赋予输出y的对数概率增量。
- $\Delta r_\theta$：偏好输出与拒绝输出之间的相对对数概率增量差。
- $\sigma$：Sigmoid函数，将偏好优势映射到0至1之间。
- $\beta$：偏好对数比的缩放系数，论文设为0.3。
- $\lambda$：偏好间隔偏移的权重，论文设为0.2。
- $m$：由偏好与拒绝候选的行为距离差归一化得到并截断至1的配对间隔。

<div class="equation-explanation" markdown="1">

**直观理解**：普通偏好训练只要求$y^+$比$y^-$更可能；该式还减去$\lambda m$，意味着损失要足够小，模型就必须让$\beta\Delta r_\theta$超过与偏好清晰度相关的门槛。于是行为差距明显的配对施加更强要求，而参考模型限制更新不要无约束地偏离已学会的编译、翻译和领域能力。<br>
**原文位置**：第3节“Common-Parent Preferences and oDPO”，式(5)；$m$的定义见式(4)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：方法的理想目标是让请求强度$s$下生成的子策略行为位移$d_{\mathrm{beh}}(\pi_p,\pi_c)$接近该强度的经验中心$\mu_s$，即最小化父策略、强度和生成子策略上的期望绝对偏差；同时维持低、中、高位移分布的有序关系。由于从语言生成到编译、程序执行和信号比较的链条不可微，论文没有直接反向传播该距离，而是先用测得的行为距离监督条件SFT，再把同一父代的候选转换成$y^+$与$y^-$偏好对，通过oDPO间接优化生成概率。

oDPO中的$m$由$|d^+-d^-|$除以训练偏好间隔的第95百分位数后截断至1得到；小于训练四分位距$0.15$倍的配对被过滤，以免近乎无差别的候选提供不稳定监督。这里的作者设计主张是：共同父代比较消除了父策略差异这一混杂因素，间隔偏移则利用行为证据的强弱调整训练要求；分析上应注意，模型学到的是相对于数据经验中心的类别校准，而不是对任意市场轨迹都保证精确的数值位移。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 统一的任务条件Qwen3-8B模型**

同一全参数微调模型通过任务条件实现三种映射：$\mathcal{R}_{\mathrm{NL}}\rightarrow\mathcal{G}$的编译、$\mathcal{G}\rightarrow\mathcal{R}_{\mathrm{NL}}$的翻译，以及$p_\theta(x_c\mid x_p,s)$定义的条件语义变异。编译输出是可类型检查和回测的GPTL程序；翻译输出采用变异器所需的标准化自然语言格式。

> 直观理解：统一模型减少了三个独立模型之间的表示不一致：它既知道自然语言怎样对应程序，也知道怎样在语言层面修改策略。翻译模块还允许人工GPTL种子或代码空间发现的策略进入语言搜索，但常规世代中无需反复来回翻译。

**2. 执行落地的行为位移测量**

每个策略$\pi:\mathcal{S}\rightarrow\mathcal{B}$把市场状态映射为四位原始信号向量，分别表示多头入场、空头入场、多头退出和空头退出，其中$\mathcal{B}=\{0,1\}^4$。父子策略必须在共享状态轨迹$\mathbf{s}_{1:N}$上执行，$d_{\mathrm{beh}}$统计两者产生不同完整信号向量的时间点比例。

> 直观理解：代码改了几行并不能说明交易行为改了多少，所以论文直接比较两份策略在同一批市场时刻会不会作出相同动作。这使训练标签与最终执行行为一致，也避免把表面文本差异误当成真正的策略变化。

**3. 共同父代oDPO校准器**

偏好样本固定父策略和请求强度，只比较其候选子代与目标经验中心$\mu_s$的接近程度；低、中、高被视为满足$D_{\mathrm{low}}\prec D_{\mathrm{medium}}\prec D_{\mathrm{high}}$的有序、重叠分布，而非精确半径。损失以冻结SFT模型为参考，并用偏好间隔$m$形成偏移量，迫使当前模型达到与样本清晰度相匹配的对数概率优势。

> 直观理解：固定父代后，偏好问题变成“对于这次小改或大改请求，哪个孩子的实际变化更合适”。允许三个区间重叠承认了自然语言变异具有随机性，训练目标是稳定的统计顺序，而不是要求每个样本命中一个精确距离。

**训练与推理**

训练阶段首先从高适应度GPTL程序生成AST退化链，在六个仅训练使用、各含$6000$根小时K线的窗口上执行父子端点，并计算$d_{\mathrm{beh}}$。距离按等频分箱切为三档，切点为$0.165$与$0.466$；低于$0.005$的空转移和类别边界附近的转移被移除。GLM 5.2以关闭推理、温度$0.1$的设置把程序端点标注为标准化自然语言；这些数据与编译、翻译数据共同形成多任务SFT语料。SFT后，从同一父代的不同强度候选中建立偏好对，再以SFT检查点作为冻结参考进行一轮oDPO；模型检查点还必须满足编译有效性、翻译信号保持和输出格式均超过$95\%$，并在留出数据上达到Spearman相关系数$\rho\geq0.4$的强度单调性门槛。

推理或进化阶段无需访问训练时的目标子代。给定父描述$x_p$、父GPTL、适应度、回测统计和请求强度$s$，最终模型生成$x_c$；编译器$C:\mathcal{R}_{\mathrm{NL}}\rightarrow\mathcal{G}$产生可执行GPTL，类型检查和确定性回测给出适应度，外层进化算法据此选择下一代。若起点来自人工GPTL、直接代码变异或其他代码搜索，则先调用程序到语言翻译；进入自然语言谱系后，子描述直接继承，避免每代翻译造成信息漂移。

**复现信息**

最终监督语料共有$45639$条样本，其中条件变异$13551$条、编译$16044$条、程序到语言翻译$16044$条，划分为$44727$条训练样本和$912$条验证样本。变异数据源自$2811$条退化链和$44920$个分级反向转移，其中$44917$个可成功执行；保留样本按强度与资产平衡。oDPO数据由$6369$个父策略产生，共$14735$个训练偏好对和$775$个验证偏好对。

SFT训练一轮，学习率为$2\times10^{-5}$；oDPO训练一轮，学习率为$2\times10^{-6}$，并采用$\beta=0.3$、$\lambda=0.2$。为公平解释表示作用，论文还训练匹配的代码输出模型：保持Qwen3-8B骨干、训练转移、偏好对、强度标签和oDPO目标不变，只把输出表示从自然语言改为GPTL；手工加权AST算子则覆盖参数、指标、子树、比较符、逻辑、子句、交叉和信号分支等编辑，并同时作为原生代码基线及训练退化链的数据生成工具。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- E-mini S&P 500 连续期货（ES）：2008 年 1 月至 2025 年 10 月的小时数据，共 106,685 根 bar。数据按时间顺序划分为互不重叠的 70% 训练集、15% 验证集和 15%测试集，分割之间设置十天隔离期。训练折反馈提供给突变模型，验证折用于进化选择，测试折只在搜索结束后评估一次。
- 白银连续期货（SI）：同一时期的 107,085 根小时 bar，采用相同的 70%/15%/15% 时间划分和十天隔离期。它提供与股票指数不同的商品市场环境，用于检验方法是否仅适用于单一资产动态。
- 美国国债连续期货（US）：同一时期的 105,124 根小时 bar，采用相同的时间划分、隔离和一次性留出测试协议。它引入利率类资产，使跨资产结果覆盖股票、商品和债券三种不同市场。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**留出测试 Sharpe**

Sharpe 衡量策略收益相对于波动风险的表现。每次搜索在 1,000 次评估结束后，只将验证集上最优的策略在对应测试折上评估一次；均值反映典型泛化表现，前四分位均值和最大值仅描述搜索结果的上尾。 （越高越好，因为更高值表示单位风险对应的收益更高；但最大值和前四分位结果属于描述性统计，不能单独作为总体显著性证据。）

</div>
<div class="metric-item" markdown="1">

**最佳截至当前验证曲线下面积（AUC）**

在统一的 1,000 次策略评估网格上，对最佳截至当前验证 Sharpe 曲线求面积，综合衡量整个有限预算搜索过程中发现优良策略的速度和质量。 （越高越好，因为它表示算法在较早阶段或更长一段搜索过程中保持了更高的最佳验证适应度，而不只是最终一次碰巧找到好策略。）

</div>
<div class="metric-item" markdown="1">

**强度与行为位移的 Spearman 相关**

计算请求强度的顺序与策略执行动作序列实际位移之间的秩相关，再以每次运行为分析单位进行配对检验。它衡量低、中、高强度标签能否成为可操作的行为控制信号。 （越接近 1 越好，因为这表示请求强度越高，实际行为变化通常也越大；它只证明单调排序校准，不代表模型能精确生成指定数值的行为距离。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 行为强度校准：比较 NL oDPO、behavior-grounded SFT 和仅由提示标签条件化的模型。

<div class="result-value" markdown="1">

请求强度与实际行为位移的运行级平均 Spearman 相关分别为 0.824、0.310 和 0.018。NL oDPO 在与另外两种方法的全部 36 个配对运行中均占优，秩二列效应量均为 1.00，Holm 校正后均有 $p<0.0001$。

</div>

作者据此主张 oDPO 将原本较弱的强度排序监督转化为稳定的行为控制接口。分析上，这说明低、中、高标签确实能单调调节策略行为变化，而提示中简单加入标签几乎不起作用；但中强度分布较宽且高强度存在饱和，因此结果不能解释为对某个精确行为距离的数值控制。

<div class="result-source" markdown="1">

来源：第 5 节“A Requested Strength Becomes a Behavioral Control”，图 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In the run-level analysis used for inference, mean Spearman correlation between requested strength and realized displacement is 0.824 for oDPO, 0.310 for behavior-grounded SFT, and 0.018 for prompt-only conditioning.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 有限预算搜索效率：NL oDPO 分别与原生 AST 突变和匹配的 Code-output oDPO 比较。

<div class="result-value" markdown="1">

NL oDPO 相对 Direct AST 的平均 AUC 配对差为 +181.3，95% bootstrap 区间为 [85.0, 295.1]，$r_{rb}=0.58$，Holm 校正后 $p=0.0078$；相对 Code-output oDPO 的差为 +58.2，区间为 [2.3, 123.9]，$r_{rb}=0.39$，校正后 $p=0.0425$。

</div>

作者将两个校正后显著的 AUC 对比解释为自然语言表示在 1,000 次评估预算内具有更高搜索效率。与 Code-output oDPO 的对比尤其关键，因为模型骨干、偏好数据、标签和目标保持一致，主要变化是突变用自然语言还是代码表达；不过该效应较小且接近校正阈值，因此它支持有限预算优势，却不足以证明自然语言在所有进化算法或更大预算下都占优。

<div class="result-source" markdown="1">

来源：表 1B“Confirmatory paired contrasts”；第 5 节“Language Improves Finite-Budget Search Efficiency”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

NL oDPO − Direct AST | AUC | +181.3 | [85.0, 295.1] | 0.58 | 0.0078; NL oDPO − Code oDPO | AUC | +58.2 | [2.3, 123.9] | 0.39 | 0.0425.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 自然语言表示的留出测试表现：比较 NL oDPO、Direct AST 和 Code-output oDPO 的测试 Sharpe 分布。

<div class="result-value" markdown="1">

NL oDPO 的平均测试 Sharpe 为 0.4478，高于 Direct AST 的 0.3526 和 Code-output oDPO 的 0.3024；其前四分位测试均值为 1.5063，观察到的最大测试 Sharpe 为 2.3445，也是所比较表示中最高的上尾结果。

</div>

这些结果显示自然语言搜索在本实验中产生了更强的优良候选上尾，并取得最高单次留出表现。作者明确把这些测试均值、前四分位均值和最大值视为描述性背景，而非表示层面的确认性终点；所有系统仍出现负面结果，且外层算法存在异质性，所以不能据此断言 NL oDPO 的平均测试泛化必然优于每个基线。

<div class="result-source" markdown="1">

来源：第 5 节“Language Improves Finite-Budget Search Efficiency”，表 1A、图 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

NL oDPO has higher mean test fitness than native AST (0.4478 versus 0.3526) and matched code output (0.4478 versus 0.3024), as well as the highest top-quartile mean (1.5063) and observed maximum (2.3445).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 表示层面的留出测试均值、前四分位均值和最大值都是描述性结果，确认性表示对比的终点是验证曲线 AUC。因而论文能够较有力地支持“有限预算搜索更高效”，但尚不能同等有力地支持“平均测试泛化必然更好”；此外所有系统都存在负测试结果。
- 实验只覆盖三个金融期货、固定的小时频率、同一回测成本模型和 1,000 次评估预算，且外层算法与表示形式存在交互。语法距离与行为距离的较强相关、较低灾难率以及匹配位移下的适应度保留仍属于机制性关联，不能证明这些因素是搜索效率提升的唯一因果来源。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Untrained base：未经领域训练的 Qwen3-8B 基础模型，用来判断通用语言模型本身是否已经能够充当有效的策略突变算子。
- No-label SFT：进行领域监督微调，但不输入突变强度标签；它检验自然语言策略突变能力是否主要来自领域训练，同时作为评估条件标签价值的基础参照。
- Behavior-grounded SFT：利用实际行为位移构造强度监督、但不进行 oDPO 的模型；与 NL oDPO 比较可区分行为监督本身和偏好优化带来的增益。实验还设置 label-only checkpoint，以判断只有提示标签、没有行为依据的条件化是否有效。
- Direct code (AST) 与 Code-output oDPO：前者是直接在程序抽象语法树上执行的原生突变；后者与 NL oDPO 固定相同的模型骨干、训练转移、偏好、标签和目标，只把突变输出表示从自然语言换成代码。二者分别检验自然语言相对传统程序突变的整体优势，以及表示形式本身的影响。

**实验想回答的问题**

- 请求的低、中、高突变强度能否稳定控制实际行为位移，并使模型选择不同的语义编辑方式，而不只是改变自然语言的表面措辞？
- 在相同的评估预算下，以自然语言表示并通过 oDPO 训练的突变算子，是否比原生 AST 突变和直接生成代码的匹配模型更快找到高适应度策略；这种搜索效率是否能转化为更好的留出测试表现？

**实验实现**

回测初始资金为 10,000 美元，计入 0.005% 手续费和 0.01% 滑点，仓位限制为单位多头、单位空头或空仓。搜索期间模型接收训练折反馈，进化算法以验证 Sharpe 选择策略；每次运行预算为 1,000 次评估，预算结束后仅测试验证最优策略。学习型算子的主矩阵覆盖 6 个算子、3 个外层进化算法、3 个资产和 4 个随机种子，共 216 次搜索；另有 36 次原生 AST 搜索，36 次 NL oDPO 搜索在不同分析中共享。配对单位为外层算法、资产和种子，每项对比有 36 对观测。六项确认性对比使用双侧 Wilcoxon 符号秩检验并进行 Holm 多重比较校正，同时报告 10,000 次配对 bootstrap 区间和秩二列效应量。该设计严格区分训练反馈、验证选择和测试报告，可降低测试集反复参与搜索造成的信息泄漏；不过同一批 NL oDPO 运行被多个分析共享，不能把各分析视为完全独立的重复实验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 领域监督微调的必要性：No-label SFT 对比未经训练的基础模型。 | No-label SFT 相对基础模型的留出测试 Sharpe 配对均值提高 +0.375，95% bootstrap 区间为 [0.189, 0.559]，$r_{rb}=0.64$，Holm 校正后 $p=0.0024$。 | 该消融隔离了领域 SFT 是否能建立基本突变能力，因为两者都没有可用的行为强度控制。结果支持作者关于“领域训练把通用模型变成功能性突变器”的主张，但它没有说明强度标签是否有效，也不能把增益单独归因于自然语言表示。 | 表 1B“Confirmatory paired contrasts”<br><span class="experiment-evidence">No-label SFT − Base \| Test \| +0.375 \| [0.189, 0.559] \| 0.64 \| 0.0024.</span> |
| 行为落地监督的作用：Behavior-grounded SFT 对比只有强度标签、没有行为依据的 Label-only checkpoint。 | Behavior-grounded SFT 相对 Label-only 的留出测试 Sharpe 配对均值提高 +0.538，95% bootstrap 区间为 [0.220, 0.869]，$r_{rb}=0.56$，Holm 校正后 $p=0.0111$。 | 两者都提供条件标签，关键区别是标签是否由实际动作序列位移定义。因此该变化表明模型不能仅凭“低、中、高”等提示自动获得有效控制，标签必须与执行行为建立训练对应关系。该消融验证的是条件接口的语义落地，而非 oDPO 的额外价值；后者由 NL oDPO 与 Behavior-grounded SFT 的 AUC 对比另行检验。 | 表 1B“Confirmatory paired contrasts”<br><span class="experiment-evidence">BG-SFT − Label-only \| Test \| +0.538 \| [0.220, 0.869] \| 0.56 \| 0.0111.</span> |

**定性案例**

- 图 5 的编辑分类分析显示，请求强度会改变突变的语义组成：低强度主要调整参数，高强度则转向指标替换、比较符交换、结构重写、方向翻转和子句操作，同时编辑熵随强度提高。相比之下，仅提示标签的检查点几乎保持不变。这个案例说明模型学到的是不同的突变机制，而不只是把同一种改写描述成不同强度；但编辑类别由聚合统计得到，不能保证每次单独突变都符合预期。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper trains a language model to perform controllable semantic program mutation and compilation for execution-grounded evolutionary search.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`eb4e3f786f5ab7578f3f82560d98806243d70970e285c6baab1521a080f1cef0`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
