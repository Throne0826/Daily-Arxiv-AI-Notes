---
title: "[论文解读] SVR: Self-Verifying Refinement via Joint Verdict-Confidence Reinforcement Learning for Adaptive Test-Time Compute"
description: "[arXiv 2607.28457][LLM Reasoning] 本文关注如何让语言模型依据自身生成的正确性判断与置信度，逐轮决定保留当前答案还是继续修改，从而在推理时无需外部正确性反馈也能按题目难度自适应分配计算。"
arxiv_id: "2607.28457"
announcement_date: "2026-07-31"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:48.954509+00:00"
source_sha256: "89696f32d444d0466bfa8dfd6623a0f4256a4bff5b1b35f1842f94a082614727"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "测试时计算"
  - "自适应停止"
  - "多轮推理"
  - "自验证"
  - "置信度校准"
  - "答案修正"
  - "强化学习"
  - "数学推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2607.28457</p>

# SVR: Self-Verifying Refinement via Joint Verdict-Confidence Reinforcement Learning for Adaptive Test-Time Compute

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Chen, Hongyu, Lin, Liang, Wang, Guangrun</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.28457) · [PDF 下载](https://arxiv.org/pdf/2607.28457) · **关键词** 测试时计算, 自适应停止, 多轮推理, 自验证, 置信度校准, 答案修正, 强化学习, 数学推理<br>


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

本文关注如何让语言模型依据自身生成的正确性判断与置信度，逐轮决定保留当前答案还是继续修改，从而在推理时无需外部正确性反馈也能按题目难度自适应分配计算。

**不用术语来说**：语言模型多思考几轮有时能修正错误，但并非越久越好：简单题可能第一轮已经答对，继续修改反而会把正确答案改错；难题则可能确实需要多轮尝试。现实部署中通常又没有标准答案或外部验证器随时告诉模型何时答对，因此需要模型自己可靠地判断“当前答案是否值得保留”，并据此决定停止还是继续。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出无预言机的闭环精炼框架 SVR：每轮由策略同时生成解答、离散判定（Correct、Incorrect 或 Unsure）和正确性置信度，并将这些内部信号直接用于答案保留与推理时自适应停止；这里“无预言机”仅指精炼提示和推理控制器不接触真实正确性，并不表示训练无需正确性监督。
- 提出联合判定—置信度强化学习，使解题质量、结构化自验证及可停止的正确状态共同影响固定轮长轨迹的训练回报，从而学习可用于推理控制的内部信号；作者进一步主张，实验中的精度—计算权衡来自按样本停止，而非单纯增加精炼轮数。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型的测试时计算与多轮推理研究。核心前提是：模型在推理阶段增加采样、搜索或迭代修正，通常有机会提高答案正确率，但额外计算的边际收益随题目和当前解答状态而变化；简单题可能首轮已答对，困难题则可能需要多轮修正，而且继续生成还可能覆盖原本正确的答案。因此，问题不只是“投入多少计算”，还包括如何依据不断演化的中间解答，逐轮决定保留当前答案还是继续修正。已有方法常采用统一轮数、在推理前按输入难度分配预算，或依赖奖励模型、过程验证器、执行结果等外部反馈；本文关注更严格的设定，即让推理策略利用自身产生的正确性判断与置信度控制停止和续算，在部署时不访问真实答案或外部验证器。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自验证（self-verification）**

模型在生成解答后，再对该解答是否正确作出结构化判断。本文要求模型同时输出离散裁决与置信度，并将二者直接用作是否继续推理的控制信号。

</div>
<div class="concept-item" markdown="1">

**自适应测试时计算（adaptive test-time compute）**

推理时不为所有输入机械分配相同计算量，而是根据具体输入或当前解答状态决定是否追加计算。本文采用逐轮停止机制，使已具备可靠正确答案的轨迹提前结束，而不确定或疑似错误的轨迹继续修正。

</div>
<div class="concept-item" markdown="1">

**置信度校准（confidence calibration）**

校准要求模型声明的正确概率与实际正确频率相匹配，例如置信度为 $0.8$ 的答案在同类样本中应约有八成正确。在本文中，校准误差会直接变成计算分配错误：过度自信可能使错误答案提前停止，信心不足则可能让正确答案遭到不必要的后续改写。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一道数学推理问题，策略在第 $t$ 轮生成当前解答，同时给出离散裁决 $v_t\in\{\mathrm{C},\mathrm{I},\mathrm{U}\}$，分别表示 Correct、Incorrect 和 Unsure，以及当前答案正确的置信度 $c_t$。在尚未达到最大轮数 $T_{\max}$ 时，系统仅当输出未被截断、$v_t=\mathrm{C}$ 且 $c_t\geq\gamma$ 时停止并返回当前答案；否则，下一轮提示由原问题、上一轮解答及策略自身的验证信息构成，模型据此继续修正。训练阶段允许用真实正确性构造奖励，并采用固定长度的多轮轨迹；但真实正确性不会写入修正提示，也不提供给推理时控制器。因此，文中的“无预言机”限定的是部署和闭环修正过程的信息边界，而不是声称训练完全不使用正确性监督。最终目标是在保持或提高数学推理准确率的同时，按实例动态减少无效轮次与令牌消耗，并降低正确中间答案被后续修正破坏的风险。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$v_t$**

第 $t$ 轮由策略生成的离散正确性裁决，取值为 $\mathrm{C}$、$\mathrm{I}$ 或 $\mathrm{U}$。

</div>
<div class="notation-item" markdown="1">

**$c_t$**

第 $t$ 轮中，策略对当前答案正确概率给出的置信度估计。

</div>
<div class="notation-item" markdown="1">

**$\gamma$**

推理阶段的置信度停止阈值；只有裁决为正确且置信度达到该阈值时，当前答案才可被保留并提前返回。

</div>
<div class="notation-item" markdown="1">

**$T_{\max}$**

一条推理轨迹允许执行的最大修正轮数；若此前始终不满足停止条件，则运行至该轮并返回最终输出。

</div>

</div>

**直接相关的工作**

- **Learning How Hard to Think（Damani et al., 2025）**: 该方法预测输入—预算组合的奖励分布，据此为不同输入分配 best-of-$k$ 采样预算或选择解码器，代表以输入级难度预测进行计算分配的路线。SVR 的区别是将决策推迟到解答生成过程中，依据当前解答及策略自验证逐轮判断是否继续，因此能够响应解答状态随轮次发生的变化。
- **CoRefine（Jin et al., 2026）**: CoRefine 使用轻量控制器读取冻结模型词元级轨迹所导出的置信信息，并在停止与修正动作之间选择。SVR 不设置独立控制器，而是在同一个推理策略中联合生成解答、正确性裁决和置信度，再通过裁决—置信度规则控制保留或修正。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

测试时增加采样、搜索或迭代精炼可以提升推理能力，但额外计算的边际价值随题目和当前状态而变。统一执行固定轮数会在简单题上浪费 token，并让已经正确的中间答案暴露于有害修改；过早停止又会使困难题失去后续纠错机会。因此，系统不仅要生成更好的答案，还要在每一轮联合解决计算分配和答案保留问题。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **固定预算与预先分配式计算扩展**：固定预算方法对所有输入执行相同数量的采样、搜索步骤或精炼轮次；自适应预算方法虽会按输入分配不同计算量，但通常在推理开始前作出输入级预算决策，而不是观察每轮答案后再决定保留或继续。
- **自我纠错与外部验证器引导的精炼**：自我纠错方法让模型根据先前回答继续修改，但精炼次数通常由外部预设；验证器引导方法则利用奖励模型、过程验证器、程序执行结果或正确性检查来选择答案或指导下一轮修订。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 固定轮数忽略不同样本以及不同中间状态对额外计算的需求差异；预先进行输入级预算分配也无法逐轮识别“当前答案已经正确，应立即保留”的状态。其后果是无效消耗计算，甚至用后续精炼覆盖正确答案。
- 依赖外部反馈的方法在部署时可能成本高昂或根本不可用，而普通自我评估又可能失准：置信不足会使正确答案遭受不必要的继续修改，置信过高则会让错误答案提前终止。自验证一旦承担计算控制功能，校准误差就会直接转化为资源分配和最终正确性错误。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未形成一种闭环策略，使同一语言模型能够在没有推理时正确性反馈的条件下，基于当前轮产生的内部信号逐轮联合决定答案是否可信、是否应被保留，以及是否值得再投入一轮计算；尤其缺少将离散正确性判定与连续置信度共同训练为可靠停止信号的方法。

</div>
<div markdown="1"><span>核心问题</span>

语言模型能否仅利用策略自身生成的结构化自验证信号，在推理时不访问标准答案或外部验证器的情况下，可靠地决定保留当前答案还是继续精炼，并由此实现按实例自适应的测试时计算分配？

</div>
<div markdown="1"><span>作者直觉</span>

离散判定表达模型对当前状态的明确类别判断，置信度则刻画这一判断的把握程度，两者可以形成互补约束：只有模型既判断答案为 Correct，又对该判断足够确信时才停止；其余情况继续利用原问题、上一轮解答和自验证信息进行修订。训练阶段仍可用真实正确性奖励校准这种内部信号，而部署阶段只执行已经学到的判定—置信度规则，因而有望把“会检查自己的答案”转化为“知道何时停止思考”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SVR把数学解答、自我判定与推理预算控制统一到同一个语言模型策略中。给定问题$x$，策略在每轮生成推理过程$r_t$、答案$a_t$、离散判定$v_t\in\{\mathrm{C},\mathrm{I},\mathrm{U}\}$以及置信度$c_t\in[0,1]$；控制器仅在输出未被截断、判定为正确且$c_t\geq\gamma$时接受当前答案，否则根据模型自己的判定状态构造下一轮纠错提示。整个推理接口不读取标准答案、外部验证器分数或奖励，因此“oracle-free”指测试时不依赖外部正确性信号，而不是训练时完全不使用标签。

训练采用固定长度的多轮轨迹，而非按尚未可靠的自评结果提前停止。每轮都由任务评估器产生仅用于奖励的正确性标签$y_t$，轨迹奖励同时衡量答案质量与跨轮进步、判定—置信度是否可信、以及输出格式是否可解析；随后以组相对策略优化（GRPO）比较同一输入的多条轨迹。直观地说，模型不仅学习“怎样改答案”，还学习“什么时候值得相信自己的答案”；部署时再用阈值$\gamma$把这种自我验证能力转换成按题目难度分配计算量的停止策略。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始化问题与结构化生成

首先构造$p_1=\mathcal{P}_0(x)$，随后策略采样$o_t=(r_t,a_t,v_t,c_t)\sim\pi_\theta(\cdot\mid p_t)$。其中$v_t$被规范化为正确$C$、错误$I$或不确定$U$，显式不确定或无法解析的判定均归入$U$。

<div class="method-step__io" markdown="1">

**输入**：原始问题$x$、固定系统指令、任务答案格式约定和自检要求。<br>
**输出**：当前轮的推理$r_t$、任务答案$a_t$、自我判定$v_t$、置信度$c_t$以及生成是否截断的元数据$q_t$。

</div>

**直观理解**：模型被要求同时交卷和填写一张“我认为自己是否做对、把握有多大”的自评表。无法读懂的自评不会被乐观地当成正确。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 判定—置信度停止控制

若$q_t=0$、$v_t=\mathrm{C}$且$c_t\geq\gamma$，控制器返回$a_t$；否则在预算允许时继续，最迟于$T_{\max}$轮终止。控制器不访问正确性标签$y_t$、参考答案、执行结果或外部评估分数。

<div class="method-step__io" markdown="1">

**输入**：当前结构化输出$o_t$、截断标记$q_t$、置信阈值$\gamma$和剩余预算$T_{\max}-t$。<br>
**输出**：被接受的答案$a_{\hat t_\gamma}$，或一个继续细化的控制决定。

</div>

**直观理解**：只有“明确说正确”和“把握达到门槛”同时成立才提前交卷。这样既避免只凭一个偏高的置信数停止，也避免每道题都机械地运行相同轮数。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 有界上下文的状态驱动细化

继续时构造$p_{t+1}=\mathcal{P}_{\mathrm{ref}}(x,d_t,\mathcal{I}(v_t,c_t,q_t))$：截断时要求重新生成完整答案，判定正确但未通过停止门时要求独立复查高风险步骤，判定错误或不确定时要求定位并修正错误。提示只保留当前草稿和当前状态，不拼接完整历史$(o_1,\ldots,o_t)$。

<div class="method-step__io" markdown="1">

**输入**：原问题$x$、当前轮保留的限长草稿$d_t$以及状态$(v_t,c_t,q_t)$。<br>
**输出**：下一轮策略可见提示$p_{t+1}$。

</div>

**直观理解**：系统像编辑一样根据当前自评选择“重写、查错或重点复核”，但只携带最近草稿而不是全部聊天记录。这样可控制上下文增长，也保证细化依据完全来自模型自身可见的信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 固定视野轨迹采样与奖励评估

训练时无论中间自评如何，每条轨迹都强制执行$T_{\mathrm{tr}}$轮，并在每轮计算解题、进步、自我验证和格式信号，再对各轮信号取平均形成$R_{\mathrm{SVR}}(\tau)$。这种强制继续避免早期不可靠的“正确”判定遮蔽后续纠错状态。

<div class="method-step__io" markdown="1">

**输入**：训练问题$x$、每个问题采样的$G$条轨迹、固定训练视野$T_{\mathrm{tr}}$以及仅供奖励计算的逐轮正确性$y_t$。<br>
**输出**：每条固定长度轨迹的综合回报$R_i$。

</div>

**直观理解**：训练阶段暂时不让新手模型自己决定何时下课，而是让它完整经历若干次修改。教师在每一步检查答案和自评，使模型既见到纠错案例，也见到不应破坏正确答案的案例。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 自适应停止时间

$$
\hat{t}_{\gamma}=\min\left(\left\{t\in\{1,\ldots,T_{\max}\}:q_{t}=0,\;v_{t}=\mathrm{C},\;c_{t}\geq\gamma\right\}\cup\left\{T_{\max}\right\}\right)
$$

**符号说明**

- $\hat{t}_{\gamma}$：阈值为γ时实际执行并停止的轮次
- $t$：当前细化轮次
- $T_{\max}$：部署时允许的最大推理轮数
- $q_t$：第t轮输出是否因长度限制而被截断的二值标记；1表示截断
- $v_t$：第t轮规范化后的离散自我判定
- $\mathrm{C}$：离散判定中的Correct，即模型明确判断当前答案正确
- $c_t$：模型报告的当前答案正确置信度，取值范围为[0,1]
- $\gamma$：部署时接受正面自评所需的置信度阈值

<div class="equation-explanation" markdown="1">

**直观理解**：该式寻找第一个“输出完整、判定正确、置信度过阈值”的轮次；若始终没有满足条件，则集合中的$T_{\max}$保证最终终止。它把模型生成的自评转换为计算控制策略，调整$\gamma$即可在更积极的早停与更保守的继续计算之间选择运行点。<br>
**原文位置**：第3.1节，公式(4)

</div>

</div>

<div class="equation-block" markdown="1">

#### 逐轮自我验证奖励

$$
r_{\mathrm{verify},t}=(1-q_{t})\Bigl(\lambda_{\mathrm{cal}}\left[1-(c_{t}-y_{t})^{2}\right]-\lambda_{\mathrm{over}}c_{t}\mathbb{I}[v_{t}=\mathrm{C}\land y_{t}=0]+\lambda_{\mathrm{detect}}\mathbb{I}[v_{t}=\mathrm{I}\land y_{t}=0]+\lambda_{\mathrm{ready}}c_{t}\mathbb{I}[v_{t}=\mathrm{C}\land y_{t}=1]\Bigr)
$$

**符号说明**

- $r_{\mathrm{verify},t}$：第t轮用于训练判定—置信度控制信号的自我验证奖励
- $q_t$：输出截断标记；乘数$1-q_t$使截断输出不接受自我验证监督
- $c_t$：策略报告的答案正确置信度
- $y_t$：任务评估器给出的当前答案正确性标签，正确为1、错误为0，仅用于训练和评估
- $v_t$：规范化后的离散自我判定
- $\mathrm{C}$：Correct判定
- $\mathrm{I}$：Incorrect判定
- $\mathbb{I}[\cdot]$：指示函数，条件成立时取1，否则取0
- $\lambda_{\mathrm{cal}}$：Brier式置信校准项的权重
- $\lambda_{\mathrm{over}}$：错误答案被高置信判为正确时的过度自信惩罚权重
- $\lambda_{\mathrm{detect}}$：明确识别错误答案的奖励权重
- $\lambda_{\mathrm{ready}}$：正确答案获得高置信正确判定的停止就绪奖励权重

<div class="equation-explanation" markdown="1">

**直观理解**：第一项使$c_t$接近实际正确性$y_t$；第二项重点惩罚会造成危险早停的高置信假阳性；第三项奖励发现错误；第四项让正确答案形成足以触发停止的积极自评。该组合把自评训练成可执行的控制信号，而不只是供人阅读的置信报告。<br>
**原文位置**：第3.3节，公式(9)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：完整轨迹回报为$R_{\mathrm{SVR}}(\tau)=\frac{1}{T_{\mathrm{tr}}}\sum_{t=1}^{T_{\mathrm{tr}}}(r_{\mathrm{solve},t}+r_{\mathrm{verify},t}+\lambda_{\mathrm{fmt}}r_{\mathrm{fmt},t})$。其中$r_{\mathrm{solve},t}$结合当前答案质量、相邻轮次的正确性转移和截断惩罚：它奖励从错误到正确以及保持正确，惩罚从正确退化和持续失败；$r_{\mathrm{verify},t}$训练可用于停止的自评；$r_{\mathrm{fmt},t}$鼓励任务答案和自检字段可解析。按$T_{\mathrm{tr}}$取平均可避免回报尺度随训练轮数机械增大。

对同一问题采样$G$条轨迹后，使用组内均值$\mu_R$和标准差$\sigma_R$得到$\widehat A_i=(R_i-\mu_R)/(\sigma_R+\epsilon)$，再应用标准裁剪GRPO目标。需要注意，轨迹全部轮次都参与回报计算和后续上下文形成，但策略梯度只作用于最后一轮完成内容；部署阈值$\gamma$、实际停止轮次和累计输入—输出成本均不直接进入训练目标，因此同一策略可在推理时通过改变$\gamma$选择不同的准确率—计算量折中。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 联合判定—置信度接口**

策略同时输出离散判定$v_t$和连续置信度$c_t$；前者表达是否作出明确的正确承诺，后者表达承诺强度。停止规则使用二者的合取条件，而细化主模式主要由截断状态$q_t$和判定$v_t$决定，置信度作为上下文并参与停止门控。

> 直观理解：离散判定回答“你认为对不对”，连续置信度回答“你有多确定”。两者结合比单独使用任一个信号更适合控制高风险的提前停止。

**2. 一阶有界细化控制器**

下一轮提示由$\mathcal{P}_{\mathrm{ref}}(x,d_t,\mathcal{I}(v_t,c_t,q_t))$生成，只依赖原问题、限长当前草稿和最新状态，不暴露标签、参考答案、评分、奖励或完整交互历史。截断优先于解析出的自评，因而不完整输出不能触发停止。

> 直观理解：控制器不是另一个会判断答案的模型，而是一组确定性路由规则：它读取模型自己的自评，再选择下一条复核或纠错指令。其价值在于维持训练与测试相同的无外部验证信息接口。

**3. 面向控制的自我验证奖励**

自我验证奖励将Brier式置信校准、错误答案上的高置信正判定惩罚、错误检测奖励和正确答案的停止就绪奖励组合起来，并用$1-q_t$屏蔽被截断输出。它不只要求$c_t$拟合$y_t$，还针对“错误答案被自信接受”这一会直接导致提前停止的非对称风险进行塑形。

> 直观理解：仅让置信度平均上准确还不够，因为“错题却自信说正确”比“对题但不够自信”更危险：前者会直接交出错误答案，后者通常只是多算几轮。因此奖励对不同控制错误采用不同处理。

**训练与推理**

训练阶段：对每个$x$采样$G$条轨迹，每条都强制运行固定的$T_{\mathrm{tr}}$轮；第$t$轮生成$o_t$后，根据$(x,d_t,v_t,c_t,q_t)$构造下一轮提示。任务评估器逐轮计算$y_t$，但该标签只进入奖励，不进入提示；轨迹结束后汇总解题、自我验证和格式奖励，进行组内优势标准化与GRPO更新。固定视野的关键作用是避免尚未训练好的控制器因错误正判而过早截断训练数据，从而覆盖纠错、保持正确答案以及错误自评等中间状态。

推理阶段：仍使用相同策略、结构化输出和状态驱动提示，但不再强制运行$T_{\mathrm{tr}}$轮。每轮先检查$q_t$，再检查$v_t=\mathrm{C}$与$c_t\geq\gamma$；满足时立即返回$a_t$，否则在$T_{\max}$预算内继续，并在预算耗尽时返回最后一轮答案。训练与推理的差别仅是调度方式，而非模型可见信息；$T_{\mathrm{tr}}$是训练覆盖深度，$T_{\max}$是部署预算，二者无需相等。

**复现信息**

复现时必须保持四项接口约束：输出应能解析为$r_t$、$a_t$、$v_t$和$c_t$；显式不确定或非法判定统一映射为$U$；无法解析的任务答案按错误处理；截断输出不能触发停止且不接受自我验证奖励。细化上下文只保留原问题、限长草稿$d_t$和当前$(v_t,c_t,q_t)$，以避免完整历史随轮数增长。

所给方法章节未明确报告$T_{\mathrm{tr}}$、组大小$G$、各奖励权重$\lambda$及GRPO裁剪等数值配置，这些参数不能由节选推断。消融实验的统一自适应推理协议明确使用$\gamma=0.85$和$T_{\max}=10$，但这属于所报告消融的评估设置，不应误解为方法本身固定不变的阈值或预算。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Countdown：从Jiayi-Pan/Countdown-Tasks-3to4的490,364道完整题库中抽取50,000个样本训练领域策略，并在对应的留出测试集上评估。它主要检验模型在目标数字组合与算术搜索任务中能否通过多轮自检纠正答案。
- GSM8K：使用完整的7,473个训练样本训练独立策略，并在对应留出集上测试。该数据集考查小学文字应用题推理，作用是验证SVR是否适用于语言描述较多、推理链相对短的数学问题。
- Competition MATH及跨基准评测组：使用MATH完整训练集的7,500个样本训练一个领域策略，不再微调便直接评估于MATH500、AIME26、AMC23、OlympiadBench和MinervaMath。这个设置不仅衡量竞赛数学准确率，也检验同一MATH策略向不同题型和难度分布迁移的能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**最终答案准确率**

统计最终输出通过各任务专用正确性评估器的样本比例；它只评价最终答案是否正确，而不直接衡量推理过程、置信度校准或计算成本。 （越高越好，因为更高数值表示正确解决的测试题比例更大。）

</div>
<div class="metric-item" markdown="1">

**All-7与Math-5宏平均准确率**

All-7是不加权平均七个基准的准确率，Math-5是不加权平均由MATH策略评估的五个数学基准。每个基准权重相同，可避免大数据集在汇总结果中占据不成比例的影响。 （越高越好，因为它表示方法在多个基准上的整体正确率更高；但宏平均可能掩盖个别数据集上的退化。）

</div>
<div class="metric-item" markdown="1">

**平均推理轮数**

统计模型完成一道题平均执行多少轮生成、自验证和修正，是测试时计算量的直接代理指标。应与准确率联合阅读，而不能脱离质量单独比较。 （在准确率相当或更高的前提下越低越好，因为更少轮数意味着更节省推理计算；若准确率明显下降，轮数更低并不自动代表更优。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 七基准整体准确率

<div class="result-value" markdown="1">

作者报告SVR在七个数学推理基准上的All-7宏平均准确率为0.563。

</div>

这表示将七个基准等权汇总后，SVR平均约有56.3%的题目得到正确最终答案。该结果支持方法具有跨基准的整体有效性，但单一宏平均不能说明所有数据集均有提升，也无法据此判断提升是否具有统计显著性。

<div class="result-source" markdown="1">

来源：摘要；实验设置将该七基准汇总指标定义为All-7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On seven mathematical reasoning benchmarks with Qwen3.5-2B, SVR achieves a macro-average accuracy of 0.563 with only 2.99 inference turns on average.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 自适应测试时计算量

<div class="result-value" markdown="1">

作者报告SVR平均仅使用2.99个推理轮次，而不是对每个样本统一执行十轮。

</div>

平均轮数明显低于固定十轮预算，说明停止策略会让部分题目较早结束，符合“容易题少算、困难题继续修正”的设计目标。不过平均值不揭示轮数分布，也不能单独证明模型确实把额外轮次分配给了最需要的题目；这还需要按题目难度、正确性或停止轮次分组的结果。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On seven mathematical reasoning benchmarks with Qwen3.5-2B, SVR achieves a macro-average accuracy of 0.563 with only 2.99 inference turns on average.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 完整系统与强化学习、多轮及预言机参考方法比较

<div class="result-value" markdown="1">

作者声称，在其评估的完整系统比较中，SVR超过标准GRPO、强多轮基线和固定预算的预言机分数反馈参考，同时比固定十轮推理使用更少轮次。

</div>

这一比较旨在说明性能并非只来自强化学习或增加修正轮次，而且内部自验证可能替代推理阶段的外部反馈。由于所给节选未包含Table 1的完整数值、各基线的精确配置和差值，因此目前只能确认作者的总体比较结论，不能核验优势大小、公平性或逐基准一致性。

<div class="result-source" markdown="1">

来源：摘要；完整数值表在所给节选中未展示

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In the evaluated complete-system comparison, it exceeds standard GRPO, strong multi-turn baselines, and a fixed-budget oracle-guided score-feedback reference while requiring substantially fewer turns than fixed ten-turn inference.

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

- 标准GRPO：与SVR共享强化学习范式，但不包含完整的联合判定—置信度自验证控制机制，用于判断收益是否超出普通强化学习训练本身；所给节选未列出其精确目标函数和推理轮数。
- 强多轮基线：代表持续进行多轮答案修正、但未必学习自适应停止的方案，用于区分“多做几轮”与“根据内部自验证决定是否继续”的效果；具体方法名称和配置在所给节选中未明确报告。
- 固定预算预言机分数反馈参考：在固定轮数下借助外部正确性或分数反馈指导修正，是比纯自反馈更有利的参照，用来检验SVR在推理时不接触预言机信号的情况下能否仍具竞争力。
- 固定十轮推理：每道题统一执行十轮，代表不考虑题目难度的测试时计算扩展。它直接用于比较自适应停止是否能在保持性能的同时避免把相同预算浪费在容易样本上。

**实验想回答的问题**

- SVR能否相较于单轮推理、固定预算多轮推理以及依赖预言机反馈的参考方法，取得更优的答案准确率—推理计算量折中？
- SVR学习到的自验证停止策略能否比统一分配固定轮数或独立测试时采样更有效地分配计算，以及奖励和自检组件是否真正促成该行为并在不同训练随机种子下保持稳定？

**实验实现**

实验以Qwen3.5-2B为统一骨干模型，分别在Countdown、GSM8K和MATH上训练三个领域策略；所有可训练方法均使用ms-swift框架进行全参数强化学习，并在四张NVIDIA A800 GPU上通过共置的vLLM生成训练轨迹。Countdown与GSM8K策略在各自领域的留出集上测试，MATH策略则不经额外微调评估五个数学基准。不同方法在同一领域使用完全相同的训练样本、评估集和任务专用正确性评估器，以减少数据与判分差异造成的混杂。节选说明Table 1报告七个基准的最终答案准确率，但未提供该表的完整方法行、逐数据集分数、随机种子统计或显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出基于GRPO的自验证强化学习方法，用于数学推理中的自适应停止、答案改进和测试时计算分配。; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`89696f32d444d0466bfa8dfd6623a0f4256a4bff5b1b35f1842f94a082614727`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
