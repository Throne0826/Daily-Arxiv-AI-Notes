---
title: "[论文解读] Benchmarking and Reasoning Distillation of Large Language Models for Feedback Controller Design in Complex Dynamical Systems"
description: "[arXiv 2608.07004][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.07004"
announcement_date: "2026-08-10"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-10T02:38:58.136155+00:00"
source_sha256: "0e7195027f676de2db35a88822b866b6c9c2bcb4bdf2d50b1f236a62e1b31eaf"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "LLM 其他"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.07004</p>

# Benchmarking and Reasoning Distillation of Large Language Models for Feedback Controller Design in Complex Dynamical Systems

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-10</span>
<span><strong>作者</strong> Zhongchao Zhou, Yixuan Xie, Wenwei Yu, Yuxi Lu, Yaonan Zhu, Qian Niu, Yutaka Matsuo, Yusuke Iwasawa</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> the Matsuo-Iwasawa Laboratory, Department of Technology Management for Innovation, School of Engineering, The University of Tokyo, Tokyo, Japan；the Department of Statistics, University of Illinois Urbana-Champaign, Champaign, IL, USA. Wenwei Yu is with the Center for Frontier Medical Engineering, Chiba；the Center for Frontier Medical Engineering, Chiba University, Chiba, Japan. Yuxi Lu is with the Shanghai Research Institute for Intelligent Autonomous；the Shanghai Research Institute for Intelligent Autonomous Systems, Tongji University, Shanghai, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.07004v1) · [PDF 下载](https://arxiv.org/pdf/2608.07004v1) · **关键词** LLM Reasoning<br>


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

反馈控制是机器人、机电系统、能源管理和生物医学设备实现稳定运行、准确跟踪与抗扰动的基础方法。控制器根据传感器测得的系统状态或输出，持续修正参考目标与实际响应之间的误差。传统设计通常从被控对象的动力学模型出发，在状态空间中构造控制律，使闭环系统保持稳定并满足状态调节或目标跟踪要求。对于线性单自由度系统，可以使用传递函数、根轨迹和频率响应等经典工具；但真实系统往往包含多自由度耦合、非线性或时变参数，因此还需要控制律知识、数学推理、参数选择和反复调试。本文研究大型语言模型是否能够直接完成这类从动力学描述到控制器设计的任务，并进一步考察小型模型在边缘设备上的可部署性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**闭环反馈控制**

系统测量输出后，将其与目标值比较，并依据误差调整控制输入。这样可以持续纠正偏差，并在一定程度上抵抗扰动、模型不确定性和参数变化。

</div>
<div class="concept-item" markdown="1">

**状态空间模型与自由度**

状态空间模型用状态变量描述系统当前情况，并用微分或差分方程表示状态如何随控制输入演化。自由度（DoF）表示系统中需要独立描述的运动或状态方向；自由度增加且各方向发生耦合时，控制器设计通常更困难。

</div>
<div class="concept-item" markdown="1">

**控制器设计成功**

本文语境中的控制器设计不是只生成一段文字，而是为给定动力学系统选择控制结构和参数，使闭环系统达到预定的稳定性、跟踪或调节要求。具体成功判据应以论文实验章节的定义为准，所给摘录未进一步列出该判据。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是一个以自然语言或相应数学描述给出的动力学系统配置，包括自由度数量、系统类型、耦合情况、阻尼状态以及待使用的控制器类型等；部分任务还要求采用启发式或模型驱动的设计方式。模型需要输出可实现的控制器设计，核心包括控制律、增益或其他必要参数，以及能够满足目标跟踪或状态调节要求的设计说明。评测设置覆盖 $1$ 至 $6$ 个自由度、四类系统、两种耦合配置和三种阻尼状态，共 $132$ 个系统配置，并比较商业闭源模型、开源模型和参数量为 $1.5$B 的专用模型。该问题默认系统动力学或足以进行设计的信息已经提供；摘录未明确说明所有任务是否要求模型自行辨识系统、统一的稳定性判据或统一的控制输入约束。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathrm{DoF}$**

自由度数量，表示系统需要独立建模和控制的运动或状态方向数。

</div>
<div class="notation-item" markdown="1">

**$x$**

系统状态向量，例如位置、速度或其他能够描述系统当前动态状况的变量集合；摘录未给出论文统一的具体定义。

</div>
<div class="notation-item" markdown="1">

**$u$**

控制输入向量，即控制器施加给被控对象的作用量；摘录未给出论文统一的具体维度或约束。

</div>
<div class="notation-item" markdown="1">

**$y$**

系统输出或测量响应，通常用于与参考目标比较并形成反馈；摘录未明确规定其与状态变量的具体关系。

</div>

</div>

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

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

方法由两条相连的流程组成。第一条是用 CoDyControlBench 将动力学模型、控制器类别和迭代反馈统一为可执行的控制器设计任务：LLM 接收系统状态空间描述、固定代码骨架、跟踪目标及上一轮仿真反馈，补全或修改 PID/SMC 控制代码；仿真器执行代码，并按稳态误差与瞬态约束判断该设计是否成功。第二条是面向边缘部署的推理蒸馏：以 GPT-5.5 为教师，在同一批控制调参轨迹上分别生成“简短理由+代码”和“诊断推理链+代码”两类监督目标，微调同一个 $1.5$B 学生底座，再在未参与训练的基准与真实气动人工肌肉机械臂上测试泛化能力。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造控制设计任务

将任务连同预定义系统提示词和代码模板交给模型；模板已给出被控系统及 PID、SMC 两类控制器的结构，模型只需填充标记为 [TODO] 的控制律、增益或必要变体。

<div class="method-step__io" markdown="1">

**输入**：某个受控对象的状态空间模型、DoF 数、系统类型、耦合程度、阻尼工况、指定控制器族，以及所有自由度的常值参考信号 $r_i(t)=5$。<br>
**输出**：一段可执行的候选控制器代码。

</div>

**直观理解**：模型不是从零搭建整个仿真程序，而是在固定骨架中设计控制器。这样评测更集中于“是否会设计和调参”，而不是代码工程细节。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 闭环仿真与迭代调参

执行闭环仿真并将响应反馈给 LLM，使其基于跟踪误差、超调、振荡或执行错误修改控制器。Fixed-3 强制完成三轮并选取其中得分最高的成功设计；Success-Stop 在首次满足成功条件时停止，否则最多尝试三次。

<div class="method-step__io" markdown="1">

**输入**：候选控制器代码、系统模型、仿真时长 $T=5$ s、采样间隔 $4Delta t=10$ ms，以及上一轮的性能指标或报错日志。<br>
**输出**：每个任务的一次成功控制器，或失败标记，以及对应性能得分。

</div>

**直观理解**：这相当于让模型经历有限次数的“写控制器、看响应、再修改”。两种协议分别测量固定预算下的能力和达到可行解后及时停止的能力。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成配对蒸馏数据

GPT-5.5 为每一轮控制更新产生监督文本。Answer distillation 的目标是简短理由加可执行代码；Reasoning distillation 的目标额外保留教师对响应现象的诊断及相应修改理由，随后接相同类型的代码。

<div class="method-step__io" markdown="1">

**输入**：随机采样得到的 $599$ 个线性时不变系统调参 episode；每个 episode 包含未知对象、跟踪目标、至多十轮响应反馈和控制器更新。<br>
**输出**：共享相同底层任务、但监督文本粒度不同的两套训练样本。

</div>

**直观理解**：两种学生看到的是同一批控制问题，因此比较结果主要可归因于是否学习了“根据响应诊断问题并决定如何改控制器”的中间过程。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 微调与跨场景推理

分别微调得到 Answer-Model 与 Think-Model；随后将基座、两种学生模型置于 CoDyControlBench 的 Fixed-10 设置下评估，并部署到 Jetson AGX Orin 上，为气动人工肌肉驱动单自由度机械臂生成本地控制器和执行器命令。

<div class="method-step__io" markdown="1">

**输入**：DeepSeek-R1-Distill-Qwen-1.5B 底座模型、两套蒸馏样本，以及新任务的系统描述和迭代反馈。<br>
**输出**：轻量化控制器设计模型，以及基准成功率、性能分数和真实机械臂跟踪试验结果。

</div>

**直观理解**：训练阶段让小模型模仿大模型的设计过程；推理阶段小模型在设备本地根据实测反馈持续改控制器，不依赖云端教师模型。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 非线性时变多自由度系统的状态空间动力学

$$
\dot{x}=A(t,x)x+Bu
$$

**符号说明**

- $\dot{x}$：状态向量 $x$ 对时间的导数，即系统状态变化率。
- $x$：系统状态向量；在文中的 $3$ DoF 示例中包含各质量块的位置和速度状态。
- $A(t,x)$：随时间 $t$ 和状态 $x$ 变化的状态矩阵，编码非线性、时变弹簧、阻尼及自由度耦合。
- $B$：输入矩阵，将控制输入 $u$ 映射到状态变化。
- $u$：控制输入向量。
- $t$：时间。

<div class="equation-explanation" markdown="1">

**直观理解**：该式定义了控制器面对的对象：当前状态会在自身动力学 $A(t,x)x$ 与控制输入 $Bu$ 的共同作用下演化。由于 $A$ 同时依赖时间和状态，控制器不能只按固定线性模型调参，必须处理参数变化、非线性和多通道相互影响。<br>
**原文位置**：Section II-C, Eq. (3)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文没有给出显式的损失函数或其数学表达式，故不能据此断言具体优化目标。可确认的是，两种学生均以教师生成的文本目标进行监督微调：Think-Model 的目标在控制器代码前包含中间诊断推理，Answer-Model 则不包含；二者使用相同的底层 $599$ 个 episode 和相同优化设置。因而实验意图是隔离推理轨迹这一监督内容对控制设计泛化的影响，而不是比较不同任务数据或不同训练配方。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. CoDyControlBench 任务与执行框架**

基准覆盖 $132$ 个系统配置，按 DoF 数、系统类型、耦合水平、阻尼状态和控制器类型五个维度组织。任务要求 PID 或 SMC 家族控制器跟踪各通道常值目标；多 DoF 情形逐通道评估，任一通道违反任一通过/失败条件时，整个 trial 记为 Fail。

> 直观理解：该模块把“复杂动力学下能否写出有效控制器”变成可重复运行的测试。逐通道判定避免多自由度系统中某个失控关节被整体平均指标掩盖。

**2. 响应驱动的有限轮控制器修订**

LLM 在每轮获得上一轮的性能指标或错误日志，并调整 PID 增益、SMC 结构或瞬态限制机制。成功判定首先检查预定义的稳态与瞬态通过/失败条件；只有未失败的设计才可进入分数计算，终端振荡还会受到额外惩罚。

> 直观理解：这里的反馈相当于实验结果，而非标准答案。模型必须把“响应不好”的现象转换成合理的参数或控制律改动，这正是控制设计的关键能力。

**3. 推理蒸馏学生模型**

教师为相同的控制调参轨迹生成两种标签：Answer-Model 仅学习简短理由及代码，Think-Model 还学习中间诊断推理。训练数据不含 CoDyControlBench 的实例、响应轨迹或控制器解，且训练系统与测试系统来自不同参数分布，因而测试针对分布外泛化。

> 直观理解：答案蒸馏教小模型直接给出改法；推理蒸馏还教它先判断问题来自何处再选择改法。分离训练和测试系统可降低模型靠记住题目取胜的可能。

**训练与推理**

训练时，首先随机生成恒定 $A$、$B$ 的线性时不变系统 episode，并记录目标跟踪过程中的多轮响应反馈和控制器更新；GPT-5.5 据此生成两类标签。两个学生均从 DeepSeek-R1-Distill-Qwen-1.5B 初始化，在相同 episode 上分别学习对应标签。原文明确说明，训练集未包含 CoDyControlBench 的题目、响应轨迹或控制器解，且两侧系统参数分布独立定义。推理时，模型读取代码模板、对象说明、目标和最近一次响应反馈，输出下一版控制器代码；在轻量模型评测中，最多允许 $10$ 次修订，稳态带从主基准设置的 $2\%$ 放宽至 $5\%$，其余条件保持不变。真实系统中，IMU 测得关节角度和角速度，经 I2C 传至 Jetson；Jetson 本地运行学生模型和控制器，并通过 PWM 输出执行器指令。

**复现信息**

为复现蒸馏比较，关键配置是：教师为 GPT-5.5，学生底座为 DeepSeek-R1-Distill-Qwen-1.5B；两种学生使用 $4$-bit QLoRA，秩 $r=16$、缩放因子 $\alpha=32$、dropout 为 $0.05$，适配器施加于全部注意力投影层和前馈投影层。优化器为 AdamW，学习率 $1.5\times10^{-4}$，有效 batch size 为 $8$，最大序列长度为 $1{,}792$ tokens，训练 $3$ 个 epoch。解释蒸馏结果时还需注意一个未控制的差异：原文说明 Think-Model 的监督目标通常比 Answer-Model 更长，且“no token-length matching was applied”，所以其收益不能被严格归因于推理内容本身而完全排除监督 token 数差异。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- CoDyControlBench：包含132个系统配置，覆盖系统类型、DoF数量、耦合程度、阻尼状态和控制器类型五个评价维度。其作用是系统测试大语言模型对从动力学描述到控制器代码与参数设计的能力；原文未明确报告训练集、验证集和测试集划分。
- 基准仿真任务：每个任务要求模型为多DoF系统设计PID族或SMC族控制器，使所有DoF跟踪恒定目标$r_i(t)=5$。仿真时长为$T=5$秒，采样间隔为$\Delta t=10$毫秒；原文未明确报告独立数据集划分。
- 气动人工肌肉驱动机械臂的三次物理试验：用于检验蒸馏模型从仿真控制器设计迁移到真实机器人目标跟踪的可行性。原文未明确报告该试验的样本规模、具体轨迹划分或完整硬件参数。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**设计成功率**

某模型在规定任务和运行协议下通过预定义控制要求的试验比例。多DoF任务中，只要任一DoF违反稳态误差带或超调要求，整个试验即判定为失败。 （越高越好，因为它表示模型产生可执行且满足基本跟踪约束的控制器比例更高。）

</div>
<div class="metric-item" markdown="1">

**性能分数$\mathrm{Score}$**

综合稳态误差$|e_{ss}|$、超调$M_p$、延迟时间$T_d$和终端振荡惩罚$P_{\mathrm{osc}}$的指标：$\mathrm{Score}=-(w_{ess}|e_{ss}|+w_{mp}M_p+w_{td}T_d)-P_{\mathrm{osc}}$。其中$w_{ess}=2$、$w_{mp}=2$、$w_{td}=1$；$P_{\mathrm{osc}}$在末段出现满足条件的振荡时取$5$，否则取$0$。 （越高越好，即越接近零越好；但该分数只对通过成功判定的试验求平均，不能单独代表模型的总体成功概率。）

</div>
<div class="metric-item" markdown="1">

**真实目标跟踪成功**

气动人工肌肉驱动机械臂在物理试验中是否成功完成目标跟踪，用于检验仿真评估之外的实际控制可行性。 （成功次数或成功比例越高越好；原文未明确报告该指标的误差、超调和响应时间分解。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 六个大语言模型在CoDyControlBench上的总体设计成功率

<div class="result-value" markdown="1">

GPT取得最高设计成功率94.8%，Qwen最低，为50.0%。该结果表明不同模型在复杂反馈控制器设计上的可用性差异显著。

</div>

该比较测试模型能否稳定生成满足仿真通过条件的控制器，而不仅是生成形式上合理的代码。成功率差距说明模型规模、训练数据或控制知识可能影响控制器设计；但它不能单独证明GPT在所有控制任务或真实系统中都优于Qwen，也不能区分模型推理能力与API、提示或实现差异的影响。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GPT achieved the highest design success rate at 94.8%, whereas Qwen showed the lowest rate at 50.0%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 按CoDyControlBench复杂度维度分析模型平均表现

<div class="result-value" markdown="1">

DoF数量和控制器类型造成的模型平均设计成功率变化最大，成功率范围分别为36.3%和17.6%，高于系统类型、耦合程度和阻尼状态对应的变化。

</div>

该结果测试哪些任务因素最能改变模型设计难度。DoF增加会扩大状态、输入和稳定性分析空间；PID族更依赖增益选择与迭代调参，SMC族则要求构造滑模面和模型相关控制律。因此，模型可能首先受问题规模和控制器推理形式影响。不过，维度分析揭示的是相关性，不能严格证明某一维度是性能下降的唯一因果原因。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across the benchmark dimensions, DoF and controller type exhibited the largest model-averaged variations in design success, with success-rate ranges of 36.3% and 17.6%, respectively, exceeding those associated with system type, coupling level, and damping regime.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 基础模型、答案蒸馏模型与推理蒸馏模型的边缘部署评估

<div class="result-value" markdown="1">

专门的1.5B参数推理蒸馏模型在CoDyControlBench上优于答案蒸馏模型和基础模型，在1至6 DoF范围内保持稳定表现，并在气动人工肌肉驱动机械臂的三次物理试验中全部成功完成目标跟踪。

</div>

该比较测试蒸馏模型是否能把教师模型的控制设计过程压缩到小模型中，并检验仿真优势能否延伸到真实硬件。推理蒸馏优于答案蒸馏，支持保留中间推理步骤可能有助于增益选择和控制结构设计。真实试验中的全部成功说明具有初步可行性，但三次试验规模很小，不能据此证明对不同负载、扰动、目标轨迹或硬件故障都具有鲁棒性。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The reasoning-distilled model outperformed the answer-distilled and base model on CoDyControlBench, maintained stable performance across 1-6 DoFs, and achieved successful traget tracking in all three physical trials on a pneumatic-artificial-muscle-driven robotic arm.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验通过条件主要是目标跟踪、稳态误差带和超调约束，作者明确指出这属于基准级可行性筛选而非正式安全验证；因此成功率不能代表对稳定裕度、输入饱和、噪声、扰动或故障的全面保证。
- 真实机器人验证仅报告三次物理试验全部成功，样本量、负载变化、外部扰动和跨硬件泛化结果未明确给出；该证据支持初步可部署性，但不足以证明1.5B模型已具备普遍可靠的边缘控制能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- GPT、Gemini和Claude：商业API模型，用于比较闭源大语言模型在控制器设计任务上的能力。
- GLM、DeepSeek和Qwen：开源模型，用于比较可部署或可获得模型与商业模型之间的性能差异。
- 基础模型：用于评估蒸馏前的小型模型能力，是判断蒸馏是否有效的直接参照。
- 答案蒸馏模型：只蒸馏最终控制器答案的模型，用于隔离推理过程蒸馏相对于结果蒸馏的额外作用。

**实验想回答的问题**

- CoDyControlBench能否在系统类型、自由度数量、耦合程度、阻尼状态和控制器类型等维度上，区分不同大语言模型的反馈控制器设计能力？
- 推理蒸馏能否使小参数模型在复杂控制器设计任务和真实边缘设备实验中达到可用性能？

**实验实现**

所有模型使用统一系统提示和代码模板，模型需要填充预设的TODO以保证控制器能够执行。任务目标为各DoF跟踪恒定阶跃信号$r_i=5$。每个任务在Fixed-3和Success-Stop两种协议下各进行三次独立运行。Fixed-3强制模型进行三次迭代，并从满足成功标准的候选中选择性能分数最高者；若三次均失败，则该试验失败。Success-Stop在首次满足成功标准时停止，失败时最多重试三次。成功判定要求仿真最后$1$秒内所有采样输出均位于目标值的$\pm2\%$范围内，且最大超调不超过目标值的$100\%$；通过后才计算性能分数。成功率报告三次运行的均值和标准差，性能分数仅在成功试验上平均。模型推理强度固定为high，其余推理参数采用相应API或OpenRouter端点的默认设置。蒸馏实验比较基础模型、答案蒸馏模型和推理蒸馏模型，并进一步在真实机械臂上进行三次物理验证。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 推理蒸馏与答案蒸馏、基础模型的对比 | 1.5B参数推理蒸馏模型在CoDyControlBench上的表现优于答案蒸馏模型和基础模型；原文未明确报告三者的具体数值差异。 | 该消融隔离了蒸馏内容的影响：答案蒸馏主要传递最终控制器，推理蒸馏则传递形成控制器时的分析与决策过程。若推理蒸馏稳定胜出，说明控制知识的步骤化表达可能比单纯复制最终增益或代码更适合小模型学习；但由于缺少具体分数和训练细节，无法判断优势大小或排除训练预算差异。 | 摘要<br><span class="experiment-evidence">The reasoning-distilled model outperformed the answer-distilled and base model on CoDyControlBench</span> |
| Fixed-3与Success-Stop评估协议 | 论文对两种迭代协议均进行三次独立运行；原文未明确报告两种协议各自的成功率、性能分数或统计显著性。 | 该对比用于检验允许模型在满足条件后提前停止，是否会改变控制器设计结果。Fixed-3更强调固定计算预算下的最终候选选择，Success-Stop更接近实际交互式修正流程。若两者数值不同，差异可能来自迭代次数和停止规则，而非模型本身；当前摘录没有给出结果，因此不能断言哪种协议更有效。 | Section II-D<br><span class="experiment-evidence">Each benchmark task was evaluated over three independent runs under both the Fixed-3 and Success-Stop protocols.</span> |

**定性案例**

- Q60作为示例是一个3-DoF、NLTV、欠阻尼、全耦合的质量-弹簧-阻尼系统，要求控制器同时处理非线性、时间变化、DoF间相互作用和明显瞬态风险。它说明基准并非只测试单DoF线性系统，而是把复杂动力学描述直接交给模型；但所给摘录未报告某个模型在Q60上的具体控制器、曲线或分数，因此不能将该案例视为单独的定量结果。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：研究大型语言模型在复杂动力系统控制器设计中的推理能力，并构建基准和推理蒸馏模型进行评测。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`0e7195027f676de2db35a88822b866b6c9c2bcb4bdf2d50b1f236a62e1b31eaf`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
