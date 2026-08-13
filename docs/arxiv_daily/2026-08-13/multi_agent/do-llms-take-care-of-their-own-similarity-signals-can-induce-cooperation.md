---
title: "[论文解读] Do LLMs Take Care of Their Own? Similarity Signals Can Induce Cooperation"
description: "[arXiv 2608.12125][Multi-Agent] 本文研究大语言模型智能体在战略互动中如何响应连续的相似度信号，并检验这种信号能否作为促进合作的机制，以及如何依据智能体的真实行为计算该信号。"
arxiv_id: "2608.12125"
announcement_date: "2026-08-13"
primary_category: "multi_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-13T02:52:33.860898+00:00"
source_sha256: "d42f98b487778bf83b6460e317328d8d999b7c2d03d289110fcf0d107c5bcc27"
tags:
  - "Multi-Agent"
  - "LLM Reasoning"
  - "大语言模型智能体"
  - "合作式人工智能"
  - "战略交互"
  - "囚徒困境"
  - "分级相似性信号"
  - "证据决策理论"
  - "行为博弈论"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">Multi-Agent · arXiv 2608.12125</p>

# Do LLMs Take Care of Their Own? Similarity Signals Can Induce Cooperation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-13</span>
<span><strong>作者</strong> Akash Kundu, Emanuel Tewolde, Ratip Emin Berker, Samuel F. Brown, Vincent Conitzer</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Cooperative AI Research Fellowship；Carnegie Mellon University；Foundations of Cooperative AI Lab (FOCAL)</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12125v1) · [PDF 下载](https://arxiv.org/pdf/2608.12125v1) · **关键词** 大语言模型智能体, 合作式人工智能, 战略交互, 囚徒困境, 分级相似性信号, 证据决策理论, 行为博弈论<br>
**代码**: [https://github.com/Akash190104/similarity-mechanism](https://github.com/Akash190104/similarity-mechanism)

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

本文研究大语言模型智能体在战略互动中如何响应连续的相似度信号，并检验这种信号能否作为促进合作的机制，以及如何依据智能体的真实行为计算该信号。

**不用术语来说**：当多个由大语言模型驱动的智能体相遇时，即使共同合作对双方都更有利，它们也可能因为各自追求自身收益而选择不合作。不过，如果一个智能体知道对方通常会以与自己相似的方式思考和行动，它就可能把自己的选择视为对对方选择的线索。现实中的相似程度通常不是简单的“相同或不同”，而是从低到高连续变化，因此需要弄清模型会怎样理解这种程度信号，以及依据什么行为得出的相似度才可信。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出首个用于评估大语言模型智能体如何响应分级相似度信号的框架，将取值为$X\in[0\%,100\%]$的成对相似度提供给参与战略博弈的智能体，并考察合作行为如何随该信号变化。
- 作者把抽象相似度进一步落到可观测行为上，研究如何从外部评测或推理表现计算智能体之间的成对相似度，同时揭示这种合作机制可能存在的可靠性风险。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于合作式人工智能与行为博弈论的交叉领域，研究以大语言模型为核心的智能体在非合作战略博弈中，能否利用“双方决策方式有多相似”这一信息实现互利合作。其现实前提是，大量智能体可能采用同一模型、同一模型家族或重叠训练数据，因而行动并非经典博弈论通常假设的完全独立；当相似性意味着双方较可能作出相同选择时，智能体可能把自己的行动视为对对方行动的证据，从而改变在囚徒困境等博弈中的决策。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**囚徒困境**

一种双人战略博弈：无论对方如何行动，单个玩家都更适合背叛，但双方都背叛的结果又劣于双方合作。它用于检验智能体能否克服个体层面的背叛激励，达成共同受益的结果。

</div>
<div class="concept-item" markdown="1">

**证据决策理论**

证据决策理论认为，选择某项行动时，可以考虑该行动为外部状态或他人行动提供的统计证据。在本文场景中，若两个智能体高度相似，则自己的合作选择可被视为对方也会合作的证据，即使自己并未因果性地改变对方。

</div>
<div class="concept-item" markdown="1">

**分级相似性信号**

分级相似性信号是一个连续分数，用于表示两个智能体在外部评测中的回答、决策或推理有多一致，而不只是给出“相同或不同”的二元判断。分数越高，智能体越有理由预期双方会作出一致的战略选择，但该分数本身不表示两者共享目标或能够通信。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是两个参与战略博弈的 LLM 智能体。每个智能体接收博弈规则与收益结构、用户指定的行动目标，以及描述双方决策相似程度的信号 $X\in[0\%,100\%]$；它随后输出合作或背叛等博弈行动。核心问题是：随着 $X$ 变化，合作行为是否系统性变化，以及这种关系能否跨合作问题、收益结构和提示措辞保持一致。引言阶段先把 $X$ 作为抽象且尚未落地测量的信号，以隔离相似性信息本身对决策的作用；后续研究再根据智能体在选定外部评测域中的个体行为计算成对相似度。这里的相似性指决策和推理模式的一致程度，不要求智能体具有相同身份、共享完整代码或直接观察对方当前行动。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$X$**

提供给智能体的双方分级相似性分数。

</div>
<div class="notation-item" markdown="1">

**$X\in[0\%,100\%]$**

相似性信号的取值范围；$0\%$ 表示最低相似度，$100\%$ 表示最高相似度。

</div>

</div>

**直接相关的工作**

- **Za, Panos, and Cuheln (2026)**: 研究二元相似性设置，即告知智能体其共同玩家是否会得出相同结论，并发现合作更随预期的共享推理变化，而非随模型身份变化。本文将该问题扩展到连续的分级相似性信号，并进一步关注如何从行为中测量和隔离成对相似性。
- **Oesterheld et al. (2025) 与 Anthropic (2026)**: 前者首先报告模型能力与证据决策理论倾向之间的趋势，后者在 Claude Opus 4.7 评测中进一步观察到更强能力与更支持证据决策理论的态度相关。这些结果为研究 LLM 是否会依据决策相关性而合作提供背景，但并未直接解决智能体如何响应分级、成对且由外部行为评测得到的相似性信号。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型智能体正进入交通、社交网络、消费市场、自动竞价、金融和游戏等多智能体环境。它们需要在各自具有用户指定目标的情况下完成合作、协调与冲突解决，但通用模型的互动行为难以预先判断。尤其值得关注的是，现实系统可能使用同一模型、同一模型家族或在重叠数据上训练，因而不同智能体的决策并非天然独立；若仍按彼此独立的经典假设设计互动机制，就可能错过本可实现的互利结果。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **经典非合作博弈与因果决策分析**：这类分析把不同参与者的决策视为可单方面改变且彼此独立。在囚徒困境中，无论对方选择什么，背叛都能给自身带来更高收益，因此标准分析建议背叛；仅仅观察到双方行动相关，并不足以改变选择，除非自己的行动会因果地影响对方。
- **共享推理的二元信号与证据式决策思路**：证据决策理论认为，自己的行动可以作为另一名相似决策者行动的证据，因此高度相似的双方可能同时合作。相关先前工作已研究二元情形，即直接告知智能体对方是否会得出相同结论，并发现合作更随预期的共享推理变化，而不只是随模型身份变化。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 经典分析预设不同智能体独立决策，难以表达多个智能体共享模型模块、训练来源或决策规律的现实；其后果是，在双方行动因共同计算结构而高度相关时，模型仍可能被导向囚徒困境中的相互背叛。
- 已有面向大语言模型的研究主要采用“会或不会得出相同结论”的二元设定，既不能刻画现实中从低到高连续变化的相似程度，也没有充分解决相似度应如何由可观测行为测量并与游戏提示中的其他因素隔离。因此，即使观察到合作，也难以判断它是否来自可信、具有现实依据的相似性证据。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有文献缺少两个彼此关联的环节：一是对大语言模型智能体如何响应分级而非二元的相似度信号进行系统评估；二是从外部行为中计算成对相似度，并检验信号的行为依据、任务相关性和测量方式是否会实质影响合作。前者关系到合作效应是否随相似程度稳定变化，后者关系到该机制能否从概念演示走向可信部署。

</div>
<div markdown="1"><span>核心问题</span>

当参与战略博弈的大语言模型智能体获得取值为$X\in[0\%,100\%]$的成对决策相似度时，它们的合作选择会如何随$X$变化；这种关系能否跨合作问题、收益结构和提示表述保持一致；以及当$X$由外部评测行为或模型对推理过程的判断产生时，该信号是否仍能可靠地代表真实相似性并诱导合作？

</div>
<div markdown="1"><span>作者直觉</span>

如果两个智能体通常采用相近的决策规则，那么一个智能体自己的选择不仅决定自身行动，也提供了对另一方行动的证据：选择合作更可能对应双方合作，选择背叛则更可能对应双方背叛。相似度越高，这条证据链原则上越强，因此即使智能体不能直接控制对方，高相似度也可能使互利合作变得有吸引力。作者据此把连续相似度作为可控信号，再尝试用独立评测中的行为一致性为它提供依据；但这种直觉成立的前提是模型确实审查信号来源，而不是看到一个较高数字就机械地合作。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文的方法由“行为测量、信号落地、博弈反馈、理论解释”四个环节组成。首先，研究者向大语言模型代理给出用户指定目标、一次性混合动机博弈及两名代理之间的相似度信号 $X$，记录代理的行动与思维链解释；随后系统改变 $X$、收益矩阵、推理强度、信号措辞和博弈类型，以检验合作是否由相似性稳定诱发。为了把抽象的 $X$ 变成可实际计算的信号，论文让不同模型回答若干外部基准题，再通过回答一致度或模型自身判断得到成对相似度，最后把该分数反馈给参与者，让它们在 Prisoners 等博弈中决策，并用合作率、收益和社会福利评价结果。

理论部分把模型思维链中反复出现的推理形式化为“相似性均衡”：代理 $i$ 考虑从共同基准策略 $s$ 改为 $s'$ 时，不把其他玩家视为完全独立，而是假设玩家 $j$ 以概率 $b_{ij}$ 作出相同改变。均衡要求在这种相关偏离预测下，任何玩家都不能通过改变策略提高自身效用。直观地说，普通纳什推理只问“如果只有我改变会怎样”，本文模型则问“如果与我相似的人也可能跟着改变会怎样”；$b_{ij}$ 从 $0$ 增至 $1$，恰好连接独立决策与“所有副本共同改变”的两个极端。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造抽象相似性决策任务

将博弈规则、收益和相似度说明写入提示，让两个大语言模型代理在一次性博弈中独立选择行动，并采集其思维链或行动解释。研究同时改变收益的基数与序数结构、推理强度、相似性或差异性措辞，以及 Prisoners、PublicGood、StagHunt、Chicken 等博弈环境。

<div class="method-step__io" markdown="1">

**输入**：一个混合动机博弈、具体收益结构、用户指令，以及抽象相似度 $X\in\{0\%,10\%,\ldots,100\%\}$；对照条件为分数不可用的“?”设置和完全不提相似性的 Base 设置。<br>
**输出**：每个模型和实验条件下的行动样本、合作率、平均收益及相应推理文本。

</div>

**直观理解**：这一阶段把相似度当作受控旋钮：研究者逐档调高分数，观察模型是否更愿意选择对双方有利、但可能承担被利用风险的行动。多个变体用于区分模型究竟在计算收益，还是只对“相似”这个词作表面反应。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分析决策理由并提炼行为假设

使用由 Gemini 3.1 Flash Lite Preview 驱动的 LLM-as-a-judge 框架，判断每条推理是否包含个人效用最大化、超理性式相关推理、社会福利最大化等理由；研究者还人工检查代表性回答。由此提炼出行为假设：代理可能把 $b_{ij}$ 解释为对方与自己采取同类偏离的概率。

<div class="method-step__io" markdown="1">

**输入**：不同相似度、收益和提示条件下收集的模型思维链，以及预先定义的 $17$ 类决策理由。<br>
**输出**：各类理由的出现频率、代表性推理模式，以及建立相似性均衡所需的行为解释。

</div>

**直观理解**：行动数据只能说明模型做了什么，理由标注则用于判断它为何合作。若模型主要声称合作能提高自己的预期收益，而非单纯关心集体福利，就需要一个允许“我的选择透露对方选择”的效用模型来解释。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 从外部行为基准计算成对相似度

外生方法根据两个模型在基准上的响应一致程度计算相似度；内生方法则把目标模型的决策、解释或二者同时交给参与判断的模型，由该模型自行评估双方有多相似。不同基准和输入信息条件产生不同的有向或成对相似度信号。

<div class="method-step__io" markdown="1">

**输入**：五个代表性模型在 $7+3$ 个基准上的回答、决策与解释；基准覆盖专家知识、决策理论倾向、功利主义困境、道德推理、日常权衡、人格特征和兴趣，并包含相似性 Prisoners 探针及随机骰子、随机硬币控制。<br>
**输出**：按模型对、基准和计算方式组织的外生与内生相似度矩阵 $\mathbf{b}=(b_{ij})$。

</div>

**直观理解**：外生方法像用统一答题卡比较两名考生，内生方法像让其中一名考生阅读对方答案后自行判断“我们是否像”。随机控制用于检查模型是否真的关心信号来源，而不只是看到一个较高数字就合作。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 反馈落地信号并评价下游合作

在最终行动前把计算出的相似度反馈给对应代理，再让模型相互博弈；聚合模型对的合作行动、个体收益和社会福利，并与无相似信息设置及既有合作机制的汇总表现作粗略比较。不同基准、外生或内生计算方式以及仅决策或仅解释条件被分别评估。

<div class="method-step__io" markdown="1">

**输入**：由上一阶段得到的 $b_{ij}$、参与博弈的模型对，以及 Prisoners 等下游合作任务。<br>
**输出**：实际可实现的下游合作率、平均收益、最优社会福利恢复比例，以及相似性机制在 CoopEval 类比较中的相对位置。

</div>

**直观理解**：关键不是两个模型在测试题上看起来多像，而是这个判断返回博弈后能否真正促成互利行动。该步骤因此把“相似度估计准确吗”和“该信号对合作有用吗”分开检验。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 相似性均衡定义

$$
\sigma(s,s^{\prime},b_{ij}):=b_{ij}s^{\prime}+(1-b_{ij})s,\qquad u_i(\mathbf{s})\geq u_i\!\left(s^{\prime},\sigma_{-i}(s,s^{\prime},\mathbf{b}_i)\right)\quad \forall i\in\mathcal{N},\ \forall s^{\prime}\in\mathcal{S}_1
$$

**符号说明**

- $G$：给定的对称博弈。
- $\mathcal{N}$：玩家集合。
- $\mathcal{S}_1$：对称博弈中任一玩家可使用的策略集合。
- $s$：所有玩家当前共同采用的基准策略。
- $s^{\prime}$：玩家正在考虑的替代策略或偏离策略。
- $b_{ij}$：从玩家 i 的视角看，玩家 j 在 i 偏离时作出同类偏离的概率，取值位于零到一之间。
- $\sigma(s,s^{\prime},b_{ij})$：对玩家 j 的预测混合策略：以概率 $b_{ij}$ 使用偏离策略，以其余概率保持基准策略。
- $\mathbf{b}_i$：玩家 i 对所有玩家的相似度判断向量。
- $\sigma_{-i}(s,s^{\prime},\mathbf{b}_i)$：除玩家 i 外所有玩家在该相关偏离假设下的混合策略组合。
- $\mathbf{s}=(s,\ldots,s)$：所有玩家均使用 s 的对称策略剖面。
- $u_i$：玩家 i 的效用函数。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分把相似度变成行动相关性：$b_{ij}=0$ 表示玩家 $j$ 完全不跟随，$b_{ij}=1$ 表示其必然作出同类改变。第二部分规定均衡条件，即玩家 $i$ 即便按照这种相关性重新预测其他人，也找不到收益更高的 $s'$；因此它在全零相似度时恢复单边偏离的纳什逻辑，在全一相似度时比较所有人共同改变后的结果。<br>
**原文位置**：第 3 节“A Similarity-based Equilibrium Concept”，Definition 1；混合策略定义位于 Definition 1 之前。

</div>

</div>

<div class="equation-block" markdown="1">

#### 高相似度下的个体效用与社会福利保证

$$
u_i(\mathbf{s})\geq u_i(s^{\prime},\ldots,s^{\prime})-R_i\!\left(1-\prod_{j\neq i}b_{ij}\right),\qquad \operatorname{Welfare}(s)\geq \operatorname{Welfare}(s^{\prime})-\sum_{i\in\mathcal{N}}R_i\!\left(1-\prod_{j\neq i}b_{ij}\right)
$$

**符号说明**

- $\mathbf{s}=(s,\ldots,s)$：任意给定的相似性均衡策略剖面。
- $s^{\prime}$：用于比较的任意共同替代策略。
- $R_i$：玩家 i 在全部行动剖面上的最大效用与最小效用之差，即其收益范围。
- $\prod_{j\neq i}b_{ij}$：在模型的独立混合构造下，除 i 外所有玩家都随 i 作同类偏离的概率项。
- $\operatorname{Welfare}(s)$：所有玩家共同采用策略 s 时的效用总和。
- $\mathcal{N}$：玩家集合。

<div class="equation-explanation" markdown="1">

**直观理解**：该界说明均衡相对“所有人一起改用 $s'$”的最优结果最多损失多少。若所有 $b_{ij}$ 都接近 $1$，乘积也接近 $1$，误差项趋近于零；在齐次相似度 $b$ 下，单个玩家的误差为 $R_i(1-b^{n-1})$，也揭示了玩家数增加会放大联合跟随失败的风险。<br>
**原文位置**：第 3 节，Theorem 1。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文没有训练或微调新的语言模型，也没有通过梯度下降优化相似度预测器；其核心是对现有模型进行受控推理调用、从行为数据计算或主观评定相似度，并提出一个均衡判据。形式化部分的“不存在有利相关偏离”是解概念而非训练损失，LLM-as-a-judge 也仅用于离线标注推理理由。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 受控相似性信号实验器**

该模块把抽象分数 $X$ 与博弈提示组合，并系统扫描 $0\%$ 至 $100\%$ 的相似度；“?”和 Base 条件分别控制“知道相似性已被测量”与“完全没有相似性概念”的影响。收益结构、推理努力、信号框架和博弈类型作为正交变体，用于检查行为规律能否跨设置保持。

> 直观理解：只有逐项控制这些因素，才能判断合作增加是否来自数值信号本身。例如“?”条件可以发现，某些模型仅因得知双方被比较过就改变行为，即使它们根本不知道比较结果。

**2. 相似度落地模块**

模块支持两条计算路径：外生路径利用两个模型在同一基准上的响应一致性；内生路径由判断模型读取另一模型的决策、解释或二者，并直接给出相似性判断。基准横跨不同能力和价值领域，同时设置理论上高相关的相似性探针及无信息的随机控制，以检验信号领域是否影响下游合作。

> 直观理解：该模块解决“百分之八十相似究竟从哪里来”的实际问题。比较多种领域和随机控制，可以揭示代理是否使用了信号的语义依据，还是主要服从分数表面大小。

**3. 相似性均衡模块**

对每次候选偏离 $s\rightarrow s'$，模块以 $b_{ij}$ 为权重构造玩家 $j$ 的混合策略 $\sigma(s,s',b_{ij})$，再检验偏离后的期望效用是否超过原对称策略剖面的效用。它允许异质且有方向的 $b_{ij}$，即玩家 $i$ 对 $j$ 的相似性判断不必等于玩家 $j$ 对 $i$ 的判断。

> 直观理解：它不是预测模型参数有多接近，而是直接规定代理应如何把一个相似分数用于决策。这样既能解释实验中的阈值式合作，也能推导多人场景为何更难：需要同时相似地跟随偏离的其他玩家越多，联合事件的概率通常越低。

**训练与推理**

全部流程发生在推理与离线分析阶段。抽象信号实验中，系统为每个模型、相似度和任务条件构造提示，调用模型生成行动及解释，再聚合重复样本；理由分析阶段把思维链交给固定的判断模型，按预定义类别进行多标签判定。信号落地阶段先让模型在多个基准上作答，再以响应一致性产生外生分数，或让参与模型读取目标模型的决策与解释并产生内生分数；得到的 $b_{ij}$ 被写回最终博弈提示，模型据此作出一次性决策。

理论分析不需要估计参数或求解神经网络。给定 $G$ 与 $\mathbf{b}$ 后，对每个对称候选策略 $s$ 和每个偏离 $s'$ 构造其他玩家的混合策略，并检查相似性均衡不等式；在有限策略博弈中，这可以通过枚举候选策略与偏离完成。需要注意，该概念在中间相似度 $0<\mathbf{b}<1$ 时并不保证对所有对称博弈都存在，因而它主要是对观察到的 LLM 决策方式进行行为建模，而不是一个普遍存在的规范性解。

**复现信息**

RQ1 测试 $9$ 个模型：Gemini 3 Flash、GPT 5.4 mini、Claude Haiku 4.5、Grok 4.20、DeepSeek V4 Pro、Kimi K2.6、Gemma 4 31B、Qwen 3.5 27B 和 GPT-4o；后续实验缩减为 Gemini、GPT、Claude、DeepSeek、Gemma，以覆盖 RQ1 中具有代表性的反应类型。每个 LLM 决策条件采集 $10$ 个样本，报告均值和标准误，因此曲线表示随机生成下的经验频率，而非单次确定性选择。

相似度扫描使用 $0\%$ 到 $100\%$、间隔 $10$ 个百分点的离散网格，并保留“?”与 Base 两类必要对照。相似度基准包括 HLE、Newcomb、GGB、Moral、DailyDilemmas、TRAIT、CABIN，以及论文自设的 Similarity-based Prisoners、Random Die 和 Random Coin；后两项是无信息控制。内生评估须分别保留“决策与解释同时提供”“仅决策”“仅解释”三种输入条件，因为可见解释会系统性影响模型的相似性自评。原文节选未给出提示全文、外生一致度到百分比分数的完整换算规则及全部 API 采样参数，复现时应进一步核查附录 B、J 和 H。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- RQ1实验响应集：由$9$个大语言模型在带相似度信号的单次社会困境提示下生成的混合策略及思维链。原文说明模型选择覆盖闭源与开放权重、大模型与小模型、不同来源国家以及一个较旧模型；节选未给出每个相似度档位的重复次数、完整模型名单或样本总量。该响应集用于比较相似度变化下的合作决策。
- RQ1思维链理由标注集：使用Gemini 3.1 Flash Lite Preview作为LLM裁判，对测试模型的思维链进行规模化分析，并按表4定义的$17$类理由进行多标签判定。类别包括个人效用最大化、均衡导向、社会福利最大化、决策独立或相关、超理性、风险厌恶和规则误解等；其作用是解释策略变化背后的推理模式，而不是单独衡量策略收益。
- 人工案例分析集：作者进一步人工检查RQ1响应，并在附录D展示Gemma-3-1b-it、Claude Haiku 4.5、GPT-5.4-mini和Kimi K2.6等模型的代表性思维链。它用于揭示同一模型在相同相似度下也可能采用互不兼容的解释，但不是具有统计代表性的独立测试集。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**合作策略概率**

模型被要求返回可行动作上的混合策略，因此合作行动所获概率反映模型在给定相似度下选择合作的倾向。节选未提供其正式变量名、聚合公式或置信区间计算方法。 （若研究目标是检验相似度能否诱导合作，则数值越高表示合作倾向越强；但它不是普遍意义上的性能指标，更高也不必然意味着个体收益或社会福利在所有博弈中更高。）

</div>
<div class="metric-item" markdown="1">

**思维链理由类别出现频率**

LLM裁判检查每条思维链是否出现表4所定义的$17$类理由，并统计各模型、各相似度水平下每类理由的出现频率，用于识别决策背后的解释模式。 （没有统一的越高越好方向。某类频率升高只表示该推理理由更常出现；例如相关决策或超理性理由增加可支持相似度机制的解释，而规则误解增加通常意味着结果可靠性下降。）

</div>
<div class="metric-item" markdown="1">

**博弈所得点数**

提示要求模型最大化自身点数，并向模型展示正规式博弈的规则与收益结构。点数是模型决策所针对的个体效用，但节选未说明实验是否将它作为跨运行汇总指标。 （对单个代理而言越高越好，因为任务明确要求最大化自身总点数；不过个体点数不能单独判断双方合作质量，且节选没有报告汇总得分结果。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Gemma-3-1b-it在$s=60\%$的同一类囚徒困境条件下

<div class="result-value" markdown="1">

定性案例显示，同一模型在相同相似度水平下既可能采用非因果相关性解释并合作，也可能依据严格占优与唯一纳什均衡背叛。作者案例中的合作推理把剩余$40\%$理解为独立理性成分；背叛推理则认为单次博弈中的相似推理不会改变行动的严格占优关系。

</div>

这说明相似度数值本身不足以唯一决定行为，模型如何解释“相似”才是关键中介变量。该结果来自作者挑选的思维链案例，可证明两类推理确实出现过，但不能据此估计它们各自的总体频率，也不能证明$s=60\%$通常会诱导合作。

<div class="result-source" markdown="1">

来源：附录D.1，Gemma-3-1b-it，$s=60\%$（Acausal, dissimilar → defect; cooperates）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

By choosing A0, I leverage the similarity of our reasoning to increase the probability that the other player also chooses A0, which outweighs the risk of being defected upon by the 40% independent rational component.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Claude Haiku 4.5在$s=80\%$条件下

<div class="result-value" markdown="1">

作者展示的非因果期望效用案例中，模型认为合作的期望收益为$1.6$，高于背叛的$1.4$，因而合作；但同一相似度下另一个案例仍根据相同博弈和占优策略选择背叛。

</div>

该对照直接表明，高相似度可以被模型转化为影响期望收益的决策相关性，也可以仅被理解为双方都会发现同一占优策略。数值比较支持该条思维链内部的选择，却不等于作者已在总体样本上证明合作平均收益更高。

<div class="result-source" markdown="1">

来源：附录D.2，Claude Haiku 4.5，$s=80\%$（Acausal EV; cooperates）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The expected payoff from cooperation (1.6) exceeds the expected payoff from defection (1.4).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### GPT-5.4-mini在$s=100\%$条件下

<div class="result-value" markdown="1">

在完全相似信号下，案例中的GPT-5.4-mini仍以严格占优为依据，以$100\%$概率选择背叛行动A1。模型分别比较对方选择A0和A1时的收益，并认定A1在两种情况下都更优。

</div>

这反驳了“完全相似必然使模型合作”这一简单推断：若模型坚持因果独立和逐行动占优分析，完全相似只会让它预测双方作出同样的背叛选择。该证据是单个定性案例，不能说明GPT-5.4-mini在所有$s=100\%$运行中都背叛。

<div class="result-source" markdown="1">

来源：附录D.3，GPT-5.4-mini，$s=100\%$（Causal / dominance; defects）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Since both players reason the same way, both will choose A1 with probability 100%.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给节选主要包含实验设置、理由分类和少量人工挑选案例，没有提供正文中的完整数据集定义、图11数值、合作率曲线、误差范围或显著性检验。因此只能可靠解释实验在测什么以及案例揭示的机制，无法独立核验摘要所称跨模型、跨博弈和跨提示框架的一般性结果。
- 思维链理由由单一LLM裁判Gemini 3.1 Flash Lite Preview依据作者定义的$17$类标签判定；节选未报告人工金标准、裁判间一致性、准确率或对裁判模型的敏感性分析。思维链还未必忠实反映生成策略的真实内部机制，所以理由频率应视为文本解释模式，而非决策因果机制的直接测量。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 无相似度机制下的标准单次囚徒困境推理：把双方行动视为因果独立，并依据严格占优策略或唯一纳什均衡选择背叛。它是有意义的参照，因为实验要检验相似度信息能否使模型偏离传统自利博弈论预测。
- 因果或占优推理：即使双方高度相似，也认为自己的选择不会影响对方的同时选择，因此继续选择严格占优行动。该比较揭示合作是否真正来自模型对相关决策的考虑。
- 非因果相关性或期望效用推理：模型把决策过程相似度解释为双方结论相关，并比较合作与背叛在该相关结构下的期望收益。它与因果推理形成直接对照，用于判断相似度诱导合作的推理机制。
- 跨模型比较：RQ1覆盖$9$个模型，以相同提示和博弈结构比较模型对相似度信号的敏感性。它不是额外训练出的算法基线，而是用于检验观察到的行为是否只属于某一个模型。

**实验想回答的问题**

- 在单次社会困境中，当共同可见的决策过程相似度信号逐渐变化时，不同大语言模型给出的合作策略是否发生系统性变化，以及这种变化是否在模型之间一致？
- 模型使用哪些理由解释合作或背叛，尤其是它们把相似度理解为决策相关性、超理性线索，还是仍按因果独立、严格占优与纳什均衡进行推理？

**实验实现**

所有模型均通过OpenRouter调用，统一使用思维链提示，温度设为$1$，可控制时将reasoning effort设为“low”。默认提示沿用并修改CoopEval的单次社会困境框架：先要求模型最大化自身点数并给出正规式博弈规则和收益矩阵，再告知双方决策过程具有$X\%$相似度、双方仍独立最大化自身收益且对方也知道该信号，最后要求模型返回各行动上的混合策略。作者说明RQ1测试$9$个模型，其中前$6$个前沿模型按推理成本大致可比且总实验成本可承受来选择。思维链解释分析由Gemini 3.1 Flash Lite Preview依据表4的$17$个预定义类别执行；类别频率展示于图11，随后辅以人工案例检查。节选未明确报告相似度取值全集、每个条件的运行次数、随机种子、统计检验、误差条或人工复核一致性。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 相似度提示措辞迭代：从“you are $X\%$ similar to your opponent”改为明确限定决策过程、独立目标和信号共同知识的最终版本 | 初始措辞在思维链中产生至少三种互不兼容的解释：一般属性相似、输出相关性以及分布同一性。最终措辞将相似度锚定到推理和决策过程，并明确双方仍独立最大化自身点数；此后实验默认使用最终版本。原文未明确报告改写前后合作率或解释一致性的数值变化。 | 该消融隔离的是提示语义歧义，而不是相似度机制本身的效果。它提高了实验构念的可解释性，使不同运行更可能讨论同一种“决策相似性”；但由于没有量化前后差异，不能判断改写使合作增加或减少了多少。 | 附录B，Iteration of the similarity prompt<br><span class="experiment-evidence">Inspecting reasoning traces across runs, we observed at least three incompatible readings: similarity as a generic, unspecified attribute (the model would speculate about stylistic or value-level similarity); similarity as output correlation—“there is an X% chance our answers are correlated”; and similarity as distributional identity—“there is an X% chance we sample from the same underlying distribution.”</span> |

**定性案例**

- Kimi K2.6在$s=50\%$处呈现临界点解释：一个案例认为两种纯行动的条件期望收益都为$1+p$，于是通过增大合作概率$p$来实现共同合作；另一个案例则认为$s=50\%$时合作与背叛的期望增益相等，但背叛具有更高最低收益且对相似度估计误差更稳健。这个案例说明，即使模型接受非因果相关性框架，临界点处的风险偏好和稳健性标准仍可能改变最终行动；它是机制示例，不是总体频率结论。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：研究核心是相似性信号如何影响多个LLM智能体在博弈中的合作行为与均衡。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`d42f98b487778bf83b6460e317328d8d999b7c2d03d289110fcf0d107c5bcc27`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
