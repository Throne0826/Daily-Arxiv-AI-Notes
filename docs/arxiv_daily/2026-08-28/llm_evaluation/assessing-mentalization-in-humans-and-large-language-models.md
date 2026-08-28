---
title: "[论文解读] Assessing mentalization in humans and large language models"
description: "[arXiv 2608.26291][LLM 评测] 本文研究大型语言模型是否不仅能在心智理论任务中给出类似人类的答案，还能通过推断对手的信念与意图，在互动决策中形成可适应对手复杂度的行为策略。"
arxiv_id: "2608.26291"
announcement_date: "2026-08-28"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:43:25.113695+00:00"
source_sha256: "6d755dd560a9d44418002983d6469a9b131f8c04046801a78c75fe6389182cef"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "心智化"
  - "大语言模型"
  - "人工智能"
  - "认知计算建模"
  - "心智理论"
  - "经济博弈"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.26291</p>

# Assessing mentalization in humans and large language models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Aamir Sohail, Xintong Zhong, Arkady Konovalov, Patricia L. Lockwood, Lei Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Centre for Human Brain Health, University of Birmingham, Birmingham, UK；School of Psychology, University of Birmingham, Birmingham, UK；Institute for Mental Health, University of Birmingham, Birmingham, UK；Centre for Developmental Science, University of Birmingham, Birmingham, UK；Department of Experimental Psychology, University of Oxford, Oxford, UK</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26291v1) · [PDF 下载](https://arxiv.org/pdf/2608.26291v1) · **关键词** 心智化, 大语言模型, 人工智能, 认知计算建模, 心智理论, 经济博弈<br>


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

本文研究大型语言模型是否不仅能在心智理论任务中给出类似人类的答案，还能通过推断对手的信念与意图，在互动决策中形成可适应对手复杂度的行为策略。

**不用术语来说**：一个模型答对“别人会怎么想”的测试，并不等于它在真实互动中会利用这种判断做出更好的选择。作者因此关注更严格的问题：当对手采用不同复杂程度的策略时，大型语言模型能否识别这种差异、调整自己的推理深度并改善决策，以及这种能力与人类相比处于什么水平。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将两种经济博弈与认知计算建模结合，用行为表现和模型推断出的潜在策略共同评估大型语言模型的心智化能力，而不是只依据任务答案是否正确。
- 作者比较四个模型家族、战略性提示条件及人类参与者，并报告不同提供商与模型规模之间存在明显差异；其中，GPT-5能够随对手复杂度提高而灵活调整递归推理深度。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本研究位于社会认知、计算认知科学与大语言模型评估的交叉领域。核心能力是“心智化”：智能体通过推断他人的信念、意图及推理方式来调整自身选择。已有心智理论任务表明，大语言模型能够生成与人类相似的回答，但这类静态回答并不能证明模型会在互动中利用对他人的推断获得更好的结果；因此，本文把模型置于具有不同认知复杂度对手的经济博弈中，并结合可观察行为与认知计算建模，考察其选择背后是否存在可适应对手的潜在推理策略。人类参与者在此不是绝对标准答案，而是用于比较人类与机器心智化能力的行为基准。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**心智化（mentalization）**

指根据他人的行为推断其信念与意图，并利用这些推断指导自身选择的能力。本文关注的不是模型能否口头描述他人心理，而是这种推断能否转化为经济博弈中的适应性行为。

</div>
<div class="concept-item" markdown="1">

**心智理论任务（theory-of-mind task）**

这类任务测试智能体能否理解他人可能拥有不同于自身或现实情况的信念与知识。摘要指出，大语言模型在此类任务中的表现可与人类行为一致，但这种一致性是否意味着模型能够据此进行有效决策仍不明确。

</div>
<div class="concept-item" markdown="1">

**认知计算建模（cognitive computational modeling）**

它用形式化模型从可观察选择中估计不可直接观察的认知策略，例如智能体进行了多深层次的递归推理。通俗地说，该方法不只比较谁得分更高，还试图解释模型为何做出某种选择。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象包括来自 DeepSeek、GPT-4.1、GPT-5 和 Gemini 2.0 Flash 四个模型家族的独立大语言模型智能体，共计 $N=2{,}099$，并以 $N=251$ 名人类参与者作为比较基准。每个智能体参与两种经济博弈，面对认知复杂度不同的对手；实验还比较常规提示与旨在诱发策略推理的提示。输入可概括为博弈规则、当前决策情境、对手行为信息与提示条件，输出是智能体在博弈中的选择；研究再根据这些选择评估表现，并通过认知计算模型推断其潜在心智化策略及递归推理深度。该设置隐含的关键检验是：若模型真正以心智化指导行为，其策略应随对手复杂度而改变，而不应只是产生表面上符合心智理论的语言回答。来源节选未给出两种经济博弈的名称、具体行动空间、收益结构及计算模型方程，因此这些细节不能据此确定。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$N$**

样本规模；摘要分别报告大语言模型智能体为 $N=2{,}099$，人类参与者为 $N=251$。

</div>

</div>

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

心智化是指根据他人的信念和意图来指导自身选择，它直接关系到智能体能否在谈判、协作或竞争等社会互动中作出适应性决策。大型语言模型即使能生成看似理解他人的回答，也未必会把这种理解转化为有效行动，因此需要一种能够同时考察互动收益、策略调整和潜在推理过程的评估方式。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **心智理论任务**：通过描述他人的知识、信念或意图，要求模型预测人物的判断或行为，再依据回答是否符合预期来评估其社会认知表现。原文指出，大型语言模型在此类任务上已表现出与人类一致的行为。
- **基于外显行为的能力比较**：观察模型在任务中的选择或得分，并与人类表现进行比较。这类评估能够显示谁表现更好，但若不结合认知计算模型，通常难以区分相同选择背后究竟是固定规则、表面模仿，还是针对对手进行递归推理。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 在心智理论任务上产生类似人类的答案，只能证明模型具有与心智化相容的外显行为，不能证明它会利用对他人信念和意图的推断来指导适应性选择；其后果是可能高估模型在动态社会互动中的实际能力。
- 仅比较最终选择或总体成绩无法揭示产生行为的潜在策略，也难以判断模型是否会随对手 sophistication 的变化调整推理深度；其后果是不同认知机制可能被同一表面表现掩盖。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有证据尚未回答大型语言模型能否在互动博弈中真正以心智化指导行为，也缺少对其潜在策略、递归推理深度及其对不同复杂度对手的适应能力进行正式识别，并与人类置于同一框架下比较的研究。

</div>
<div markdown="1"><span>核心问题</span>

在两种经济博弈中，不同模型家族和规模的大型语言模型是否呈现可由认知计算建模识别的心智化策略，能否根据对手复杂度灵活调整这些策略，以及旨在诱发战略推理的提示是否会改善其表现并使其推理更复杂？

</div>
<div markdown="1"><span>作者直觉</span>

经济博弈迫使智能体连续面对具有不同策略水平的对手，因此“是否理解对方”会通过实际选择及结果显现出来；认知计算建模则可从选择模式反推可能的潜在推理策略。进一步加入战略性提示，可以检验模型原本未表现出的能力究竟是能力缺失，还是没有被常规提示充分调动。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文采用“受控重复博弈—行为统计—认知计算建模”的端到端方法，比较人类与大语言模型是否会依据对手行为形成并更新关于其策略的信念。被试或独立LLM智能体先完成检查博弈或石头剪刀布博弈；研究者记录逐试次选择、对手选择和收益，再用行为分析衡量表现与适应性，并用候选认知模型区分无心智推断的强化学习、一级递归推理的虚拟博弈、二级递归推理的影响学习以及不进行逐试次学习的混合均衡策略。这里的“递归推理”是指思考“对手如何看待我”：一级推理预测对手，二级推理还估计对手对自己的预测。
检查博弈主要检验智能体使用哪一种潜在策略；石头剪刀布则通过改变对手的推理层级 $k\in\{0,1,2\}$，检验智能体能否随对手复杂度调整行为。LLM另设标准提示与社会思维链（Social Chain-of-Thought, SCoT）条件：SCoT要求模型先预测对手的下一步，再提交自己的行动。通俗地说，研究并不只看谁赢得更多，而是结合选择序列与计算模型，判断参与者是在重复有奖励的动作、跟踪对手，还是进一步推断“对手正在如何预测自己”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造受控的人机重复博弈

检查博弈中，参与者固定扮演雇员并连续进行150试次，在“工作/偷懒”之间选择；石头剪刀布中，每个区块包含40试次，对手按递归推理层级 $k\in\{0,1,2\}$ 行动。人类在石头剪刀布中依次面对三个层级，而每个LLM实例只面对一个层级。

<div class="method-step__io" markdown="1">

**输入**：人类参与者或独立LLM智能体，以及预先规定的算法对手、收益矩阵和游戏规则。<br>
**输出**：逐试次的参与者选择、算法对手选择、收益结果及所属实验条件。

</div>

**直观理解**：算法对手使每位参与者面对可控且可重复的社会环境。两个任务分别强调长期学习潜在策略，以及面对不同“聪明程度”对手时能否灵活调整。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 操纵LLM的战略推理提示

标准条件仅要求LLM选择合法动作；SCoT条件则在每一试次额外要求LLM先预测对手动作，再作出自己的选择。检查博弈测试Gemini、DeepSeek和GPT-4.1的标准/SCoT条件，并以GPT-5的正常推理设置作为另一组；石头剪刀布测试DeepSeek标准/SCoT和GPT-5正常设置。

<div class="method-step__io" markdown="1">

**输入**：游戏规则、收益信息、最近选择历史和当前选择问题。<br>
**输出**：不同模型家族与提示条件下的合法结构化选择，以及SCoT条件中的对手预测。

</div>

**直观理解**：该操纵把“先猜对方会做什么”变成显式中间步骤，从而检验战略推理究竟是模型自发产生，还是需要提示才能稳定出现。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 量化收益、选择规律与适应性

检查博弈比较各组选择、任务得分与SCoT预测准确率；石头剪刀布以平均收益为因变量，用线性混合效应模型检验组别、对手层级及二者交互，并以卡方拟合优度检验三种动作是否偏离各占 $1/3$ 的均匀分布。

<div class="method-step__io" markdown="1">

**输入**：完整的逐试次选择和收益序列，以及模型/人类组别、提示条件和对手层级。<br>
**输出**：组间表现差异、同组随 $k$ 变化的表现、组别与对手复杂度的交互，以及可能的固定动作偏好。

</div>

**直观理解**：收益说明策略是否有效，交互效应说明参与者是否会随对手变强而改变表现；动作分布检查则用于排除“总爱选某个符号”造成的伪优势。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 用候选认知模型反推潜在策略

分别拟合强化学习、虚拟博弈、影响学习和混合均衡参考模型，通过各模型对观察到的选择序列的解释能力识别更符合数据的策略。模型复杂度从只跟踪自身奖励，逐步增加对对手动作的一阶信念以及对“对手如何预测自己”的二阶信念。

<div class="method-step__io" markdown="1">

**输入**：检查博弈中每位参与者或LLM智能体的逐试次行动、对手行动和奖励。<br>
**输出**：各组更可能采用的计算策略，以及信念更新率、二阶影响权重等潜在参数的估计。

</div>

**直观理解**：同样的总得分可能来自不同心理过程，因此需要比较会生成不同逐步选择模式的模型。它类似于根据棋手的一连串落子，判断其是在记住成功招法、预测对方，还是预测对方对自己的预测。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 强化学习价值与奖励预测误差更新

$$
\begin{aligned}V_t^{\mathrm{Work}}&=V_{t-1}^{\mathrm{Work}}+\eta\,\delta_{t-1},\\ \delta_{t-1}&=R_{t-1}-V_{t-1}^{\mathrm{Work}}\end{aligned}
$$

**符号说明**

- $V_t^{\mathrm{Work}}$：第 $t$ 试次“工作”动作的估计价值。
- $\eta$：学习率，控制新奖励信息改变既有价值估计的幅度。
- $\delta_{t-1}$：第 $t-1$ 试次的奖励预测误差，即实际奖励与此前价值预期之差。
- $R_{t-1}$：第 $t-1$ 试次实际获得的奖励。
- $t$：重复博弈的试次索引。

<div class="equation-explanation" markdown="1">

**直观理解**：该模型把上一试次“实际得到多少”与“原本预计得到多少”的差异乘以学习率，再加入动作价值。它只要求参与者重复或回避近期带来不同奖励的行为，不要求其表示对手的意图，因此是检验心智化解释是否必要的低层基线。<br>
**原文位置**：Methods—Computational modeling—Inspection game—Reinforcement learning，公式(1)–(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 影响学习的一阶与二阶信念联合更新

$$
\begin{aligned}P_t^{\mathrm{Not\ Inspect}}&=P_{t-1}^{\mathrm{Not\ Inspect}}+\eta\,\delta_{t-1}^{P}+\kappa\,\delta_{t-1}^{Q},\\ \delta_{t-1}^{P}&=P_{t-1}-P_{t-1}^{\mathrm{Not\ Inspect}},\\ \delta_{t-1}^{Q}&=Q_{t-1}-Q_{t-1}^{\mathrm{Work}}\end{aligned}
$$

**符号说明**

- $P_t^{\mathrm{Not\ Inspect}}$：在第 $t$ 试次对雇主选择“不检查”概率的一阶信念。
- $\eta$：一阶信念学习率，控制对手实际动作对该信念的更新强度。
- $\delta_{t-1}^{P}$：对手动作预测误差，由观察到的雇主动作与此前“不检查”概率之差给出。
- $P_{t-1}$：第 $t-1$ 试次观察到的雇主动作指标；“不检查”为1，“检查”为0。
- $\kappa$：二阶信念权重，表示推断“对手如何预测自己”对当前信念更新的影响程度。
- $\delta_{t-1}^{Q}$：二阶预测误差，即参与者实际动作与所推断的对手对参与者动作之预期的差。
- $Q_{t-1}$：第 $t-1$ 试次参与者自身实际动作的编码。
- $Q_{t-1}^{\mathrm{Work}}$：模型所表示的、对手认为参与者会选择“工作”的概率或预期。

<div class="equation-explanation" markdown="1">

**直观理解**：更新包含两种信息：第一项根据雇主刚才是否检查来修正对其下一步的预测；第二项根据自己的行为与“雇主对自己的预期”之间的偏差作进一步修正。因而该式把简单观察对手提升为二阶递归推理，是论文用来识别较高层心智化策略的核心机制。<br>
**原文位置**：Methods—Computational modeling—Inspection game—Fictitious play与Influence learning，公式(3)–(4)、(6)–(7)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。研究没有训练或微调LLM，也没有以任务收益反向传播更新模型参数；LLM仅通过API在既有权重下完成博弈。这里的“拟合”是研究者在实验结束后，用参与者的选择序列估计认知模型参数并比较候选策略，而不是训练语言模型。算法对手本身使用预设或由既有人类数据拟合得到的参数：检查博弈对手采用影响学习模型，给定一阶更新率 $\eta=0.3$、二阶更新权重 $\kappa=0.1$ 和逆温度 $\beta=1.5$。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 检查博弈与分层候选策略模型**

参与者作为雇员在“工作/偷懒”间选择，对手作为雇主在“检查/不检查”间选择。强化学习仅根据自身动作的奖励预测误差更新价值；虚拟博弈根据雇主历史动作更新 $P_t^{\text{Not Inspect}}$；影响学习再加入二阶预测误差及其权重 $\kappa$；混合均衡模型则以单一伯努利率生成选择且不逐试次更新，雇员的混合策略纳什均衡参照为 $P(\text{Work})=0.5$。

> 直观理解：四个模型形成一条从“完全不猜对手”到“猜对手如何猜我”的解释阶梯。混合均衡模型尤其用于区分真正的学习与单纯通过随机化降低可预测性。

**2. 分层石头剪刀布对手与适应性分析**

算法对手按固定递归层级 $k\in\{0,1,2\}$ 生成行动，层级越高代表其纳入的战略推理越深。平均收益的模型写为 $\text{Payoff}\sim\text{ModelStrategy}*\text{BotLevel}+(1|\text{SubjectID})$，其中固定效应刻画组别、对手层级及交互，随机截距控制同一人类参与者的重复测量。

> 直观理解：如果智能体真正具有可调节的心智化能力，它不应只对某一种固定对手有效，而应根据对手的推理深度改变自己的策略。随机效应避免把同一个人多次作答误当成彼此独立的样本。

**3. SCoT提示与输出可靠性控制**

SCoT在行动前增加一次显式对手预测；所有LLM调用统一经过LiteLLM，并在需要时由Instructor强制JSON结构、由Pydantic验证字段和数据类型，最终动作被限制为任务允许的选项。石头剪刀布动作改编码为低频字母J、Q、Z，以减少数字顺序或传统R/P/S符号带来的先验选择偏差。

> 直观理解：SCoT检验显式“先预测再行动”是否能提升战略表现；结构化输出和中性符号则确保结果反映决策，而不是格式错误、习惯性字母或数字偏好。

**训练与推理**

LLM推断流程按独立智能体运行。每个试次向模型提供规则、收益信息、滚动的最近10试次选择历史和当前问题；标准条件直接请求动作，SCoT条件先请求对手预测再请求动作。返回结果经过结构和合法值校验后提交给环境，环境调用算法对手产生同步行动、计算收益，并把新结果加入后续上下文。检查博弈每个实例运行150试次；石头剪刀布每个LLM实例只运行一个40试次区块和一个固定的 $k$ 层级，人类则面对全部三个层级且次序随机并平衡。
实验后先做行为统计，再拟合认知模型。石头剪刀布的两个线性混合模型分别用于总体主效应/交互和组内对手层级比较；检查博弈则比较强化学习、虚拟博弈、影响学习和混合均衡对选择序列的解释。原文节选没有完整给出候选模型的参数估计算法、模型选择准则及选择概率映射，因此这些步骤不能从现有材料中进一步复现，需结合论文后续方法或补充材料核查。

**复现信息**

任务由oTree 5.11.1、botex 0.2.0和LiteLLM 1.73.1集成实现；LLM输出通过Instructor 1.6.0与Pydantic模式强制为合法JSON及限定动作。为兼顾近似人类工作记忆、运行时间和API成本，LLM上下文只保留最近10试次历史，且两个任务均不设响应时限。Gemini、DeepSeek和GPT-4.1温度设为0；GPT-5因供应商参数限制使用温度1，并将 $\text{reasoning\_effort}$ 设为medium，响应token上限未人为限制。
检查博弈的LLM样本为GPT-4.1标准/SCoT各50、DeepSeek标准/SCoT各50、Gemini标准49与SCoT 50、GPT-5正常提示100；石头剪刀布为DeepSeek标准566、DeepSeek-SCoT 568、GPT-5正常提示566。人类行为分析纳入检查博弈67人和石头剪刀布172人；石头剪刀布计算建模纳入184人。RPS建模时将独立LLM运行按组组合并丢弃余数，得到DeepSeek标准188、DeepSeek-SCoT 189和GPT-5正常提示188个建模单位；该合并会改变行为分析与计算建模中的有效样本定义，解释结果时不可混用。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 检查博弈（Inspection game）行为数据：参与者固定扮演雇员，在150轮中选择“工作”或“偷懒”，对手是采用二阶信念、即推理层级为$k=2$的自适应雇主算法。人类组$n=67$；七个LLM条件均$n>48$，包括Gemini、DeepSeek、GPT-4.1及其SCoT版本，以及仅使用常规提示的GPT-5。该任务主要检验参与者能否递归推断一个会适应自己的对手，并以累计回报衡量策略有效性。
- 石头—剪刀—布（RPS）行为数据：参与者依次对抗推理层级$k\in\{0,1,2\}$的算法，每个层级40轮，共120轮；三个区块的次序随机化并做参与者间平衡。人类组$n=184$，各LLM组$n\geq188$；文中在该任务中测试DeepSeek、DeepSeek-SCoT和GPT-5。该任务用于检验模型能否根据对手复杂度灵活调整递归推理深度。
- 人类—LLM比较数据：两项任务合计收集251名人类参与者和2,099个LLM代理的数据。人类并不知道对手是计算机算法；LLM则通过API接收尽量保持原始规则、对手配置和试次数量不变的文本版任务。人类数据不是训练集，而是比较不同智能体策略表现与计算特征的行为基准。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**平均回报（mean payoff）**

汇总参与者在重复博弈中根据对手行动获得的分数；检查博弈中它反映预测并适应对手的实际策略收益，RPS中胜、负、平分别计$+1$、$-1$、$0$。 （越高越好，因为更高回报表示行为更有效地利用了对手的选择规律；但单独的高回报不能确定参与者采用了哪一种心理化策略。）

</div>
<div class="metric-item" markdown="1">

**显著性检验与校正后的$p$值**

Welch独立样本$t$检验比较各LLM条件与人类，因方差不齐而采用Welch版本；七次比较使用Bonferroni校正，阈值为$\alpha=0.007$。模型与提示的联合影响使用Type-III Wald $F$检验。 （较小的$p$值表示在零假设下观察到该差异的证据更强，但不表示差异更大，也不直接衡量实际重要性。）

</div>
<div class="metric-item" markdown="1">

**效应量及95%置信区间**

两组比较报告Hedges’ $g$，方差分析报告偏$\eta^2$，整体模型比较还报告$\omega^2$；这些指标分别衡量标准化组间差异或实验因素解释的变异比例。 （绝对值或解释比例越大，代表效应越强；Hedges’ $g$的正负方向取决于组别相减顺序，不能脱离比较定义仅凭符号判断优劣。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 检查博弈：Gemini、DeepSeek和GPT-4.1在常规提示下与人类参与者比较

<div class="result-value" markdown="1">

三种常规提示模型的平均回报均显著低于人类：Gemini为14.2，DeepSeek为18.0，GPT-4.1为18.5；相应Hedges’ $g$分别为$-6.40$、$-4.59$和$-4.57$，且经$\alpha=0.007$的多重比较校正后仍显著。

</div>

作者结果表明，仅给出规则和历史并直接要求选择时，这三类LLM尚未达到人类在检查博弈中的适应性收益。效应量很大，说明差距不仅是样本量导致的统计显著。不过，较低回报只说明其外显策略较差，不能据此断言模型完全没有表征对手信念的能力。

<div class="result-source" markdown="1">

来源：Results，三级小节“Assessing mentalization using the inspection game”，Fig. 2a相关文字

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Specifically, Gemini (M payoff = 14.2; t(112.01) = -36.6, p = 3.58×10-64, g = -6.40, 95% CI [-7.29, -5.49]), Gemini-SCoT (M payoff = 22.4; t(109.42) = -13.7, p = 1.59×10-25, g = -2.37, 95% CI [-2.84, -1.89]), DeepSeek (M payoff = 18.0; t(110.59) = -26.5, p = 1.16×10-49, g = -4.59, 95% CI [-5.28, -3.89]), DeepSeek-SCoT (M payoff = 25.1; t(106.59) = -6.04, p = 2.32×10-8, g = -1.04, 95% CI [-1.42, -0.65]) and GPT-4.1 (M payoff = 18.5; t(95.42) = -27.2, p = 8.7×10-47, g = -4.57, 95% CI [-5.26, -3.88]), all earned significantly less than humans.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 检查博弈：GPT-4.1-SCoT和GPT-5与人类参与者比较

<div class="result-value" markdown="1">

GPT-4.1-SCoT的平均回报为27.8，与人类差异不显著（$p=0.085$，$g=0.31$）；GPT-5平均回报为26.6，与人类差异同样不显著（$p=0.123$，$g=-0.26$）。

</div>

作者将这两种条件视为检查博弈中达到人类可比表现的例外：GPT-4.1需要显式SCoT，而GPT-5在常规提示下即可达到统计上无法区分于人类的回报。需要注意，“差异不显著”不是两者完全等价的证明；它只表示本实验样本和检验下没有足够证据拒绝无差异假设。

<div class="result-source" markdown="1">

来源：Results，三级小节“Assessing mentalization using the inspection game”，Fig. 2a相关文字

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The only exceptions were GPT-4.1-SCoT (M payoff = 27.8; t(114.78) = 1.74, p = 0.085, g = 0.31, 95% CI [-0.06, 0.68]) and GPT-5 (M payoff = 26.6; t(112.18) = -1.55, p = 0.123, g = -0.26, 95% CI [-0.57, 0.05]), which did not significantly differ from humans.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 检查博弈：三种模型与两类提示组成的$2\times3$因子分析

<div class="result-value" markdown="1">

模型主效应显著（$F(2,293)=286.95$，$p=9.62\times10^{-70}$，偏$\eta^2=0.68$），提示主效应显著（$F(1,293)=2501.89$，$p=1.57\times10^{-145}$，偏$\eta^2=0.90$），模型与提示的交互也显著（$F(2,293)=14.96$，$p=6.53\times10^{-7}$，偏$\eta^2=0.09$）。

</div>

这说明回报既取决于底层模型，也强烈取决于是否使用SCoT；显著交互进一步表示SCoT并非对所有模型产生相同幅度的作用。提示主效应的解释比例很大，但该实验只比较特定模型和特定任务，不能推出SCoT会普遍改善所有LLM社会推理任务。

<div class="result-source" markdown="1">

来源：Results，三级小节“Assessing mentalization using the inspection game”，Fig. 2a相关文字

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We found significant main effects of model (F(2, 293) = 286.95, p = 9.62×10-70, partial η² = 0.68, 95% CI [0.62, 0.72]), and prompt (F(1, 293) = 2501.89, p = 1.57×10-145, partial η² = 0.90, 95% CI [0.88, 0.91]), with a significant model × prompt interaction (F(2, 293) = 14.96, p = 6.53×10-7, partial η² = 0.09, 95% CI [0.04, 0.16]).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 模型覆盖受API可用性和运行成本限制：检查博弈测试四个模型家族，而RPS只测试DeepSeek与GPT-5；GPT-5也没有SCoT配对条件。因此，跨任务差异可能与模型选择不一致混杂，且无法直接估计SCoT对GPT-5的额外贡献。
- 人类被告知对手是真人，而LLM明确通过文本任务与算法交互；两类参与者的界面、时间限制、先验信念和推理资源并不完全一致。此外，回报达到人类水平或符合某个认知模型，只是心理化的行为与计算特征，不能单独证明LLM具有与人类相同的主观理解或内部机制。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 人类参与者：提供现实行为参照，用于判断LLM回报是否达到或超过人类水平；这不是能力上限，也不能直接证明LLM与人类使用了相同认知过程。
- 常规提示：只呈现规则、选择历史并要求模型作答，是评估SCoT增益的直接对照条件。
- 固定推理层级的计算机对手：检查博弈使用$k=2$自适应算法，RPS使用$k=0,1,2$对手；它们提供可控的对手复杂度，从而测试递归心理化和适应性心理化。
- 认知计算模型：检查博弈比较Influence play、Fictitious play、强化学习等候选策略；RPS比较CHASE、Reward learner、EWA、混合均衡、Fictitious play与$\mathrm{ToM}k$等模型。其意义在于从选择序列反推潜在策略，而不只依据最终得分判断心理化。

**实验想回答的问题**

- 不同模型家族、模型规模与提示策略下，LLM能否在重复社会博弈中通过推断对手的选择获得回报，并表现出可与人类参与者比较的心理化能力？
- 要求模型先预测对手行动的社会思维链提示（SCoT）是否能提升策略表现，以及这种提升是否因模型而异？

**实验实现**

检查博弈中，人类完成一个150轮区块；RPS中完成三个各40轮的区块，对抗$k=0,1,2$对手，区块顺序随机化并平衡。LLM任务通过API以文本形式运行，保留原任务的收益规则、对手配置和试次数；为减少LLM对传统“石头、剪刀、布”词语的先验偏好，RPS动作被无语义字母J/Q/Z替代。SCoT条件先要求LLM预测对手下一步，再据此选择理性回应；GPT-5因原生支持审慎推理，仅测试常规提示。检查博弈的人类比较使用Welch $t$检验并进行Bonferroni校正；三种同时具有常规与SCoT条件的模型使用$2\times3$因子方差分析，因方差不齐报告Type-III Wald $F$检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 检查博弈中的提示消融：同一模型使用常规提示或SCoT | Gemini的平均回报由14.2升至22.4，DeepSeek由18.0升至25.1，GPT-4.1由18.5升至27.8；三种模型在SCoT下均显著获得更高回报。文中报告提示主效应为$F(1,293)=2501.89$、$p=1.57\times10^{-145}$、偏$\eta^2=0.90$。 | 该对照主要隔离“先预测对手再行动”这一提示步骤的贡献，因为底层模型和博弈规则保持不变。结果支持SCoT能把模型引向更有效的对手建模，但不能区分增益究竟来自真正的递归信念推断，还是来自额外计算步骤、答案约束或更明确的任务分解。 | Results，三级小节“Assessing mentalization using the inspection game”，Fig. 2a<br><span class="experiment-evidence">Whilst every model earned significantly higher payoffs under SCoT (Fig. 2a), the magnitude of this benefit varied, being smallest for DeepSeek (Hedges’ g = −5.29, 95% CI [−6.12, −4.45], p = 1.95×10-46), intermediate for Gemini (g = −5.77, [−6.67, −4.87], p = 3.64×10-49) and largest for GPT-4.1 (g = −6.31, [−7.28, −5.35], p = 5.26×10-46).</span> |

**定性案例**

- RPS将传统动作名称替换为无语义字母J/Q/Z，以控制LLM对“石头、剪刀、布”文本标签的固有偏好。这一设计说明观察到的选择模式应更多来自反馈历史和对手建模，而不是词语语义联想；但所给节选没有提供该重编码与传统标签之间的直接定量对照。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过经济博弈和认知计算建模评测 LLM 的心智化、递归推理与策略适应能力。; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`6d755dd560a9d44418002983d6469a9b131f8c04046801a78c75fe6389182cef`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
