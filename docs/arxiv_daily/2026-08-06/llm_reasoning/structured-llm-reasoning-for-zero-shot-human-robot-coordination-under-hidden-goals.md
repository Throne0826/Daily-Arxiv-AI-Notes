---
title: "[论文解读] Structured LLM Reasoning for Zero-Shot Human--Robot Coordination Under Hidden Goals"
description: "[arXiv 2608.04309][LLM Reasoning] 本文研究在双方目标信息互相隐藏的协作搭建任务中，如何以分散式部分可观测马尔可夫决策过程为结构指导，将大语言模型的目标推断与规划能力同规则化物理验证结合起来，实现无需针对新目标组合重新训练的人机协调。"
arxiv_id: "2608.04309"
announcement_date: "2026-08-06"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:59:03.894796+00:00"
source_sha256: "6e2d688668382694c2d3ca890536b06e3425c674d9d2575b71f82e6adc31ed0b"
tags:
  - "LLM Reasoning"
  - "机器人 / 具身智能"
  - "人机协作"
  - "私有目标"
  - "Dec-POMDP"
  - "大语言模型"
  - "心智理论"
  - "零样本协调"
  - "动作可行性验证"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.04309</p>

# Structured LLM Reasoning for Zero-Shot Human--Robot Coordination Under Hidden Goals

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Dong Hae Mangalindan, Anand Gokhale, Francesco Bullo, Vaibhav Srivastava</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> the Center for Control, Dynamical Systems, and Computation, UC Santa</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04309v1) · [PDF 下载](https://arxiv.org/pdf/2608.04309v1) · **关键词** 人机协作, 私有目标, Dec-POMDP, 大语言模型, 心智理论, 零样本协调, 动作可行性验证<br>


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

本文研究在双方目标信息互相隐藏的协作搭建任务中，如何以分散式部分可观测马尔可夫决策过程为结构指导，将大语言模型的目标推断与规划能力同规则化物理验证结合起来，实现无需针对新目标组合重新训练的人机协调。

**不用术语来说**：人和机器人要共同搭出一个三维结构，但双方各自只能看到该结构的一个二维目标视图，任何一方掌握的信息都不足以单独确定最终成品。机器人因而不能只按自己的目标行动：它还要从人的动作和对话中猜测对方想实现什么，在必要时沟通，并随新信息调整计划；与此同时，每一步放置操作都必须满足空间、资源和搭建规则等硬约束。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出一种由分散式部分可观测马尔可夫决策过程启发的结构化大语言模型架构，把隐含人类目标推断、分层规划、对话解释、动作验证和基于反馈的重规划整合为统一的协调流程。
- 作者采用混合式职责划分：让大语言模型近似处理难以精确求解的语义推断与长程规划，同时以规则验证器检查动作的物理可行性，并通过人类参与者实验与移除心智理论推断的版本及离线训练的多智能体强化学习策略进行比较。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于人机协作与机器人决策研究，关注团队成员掌握不同私有信息时的协同规划。机器人不仅要依据交互历史推断人类不可直接观察的目标，还要决定何时沟通、如何规划后续动作，并在获得新信息后修正计划；与此同时，所有动作必须满足几何、资源和物理可行性约束。去中心化部分可观测马尔可夫决策过程（Dec-POMDP）能够形式化描述这种多智能体、部分可观测且目标协同的决策问题，但精确推断与规划会随问题规模迅速变得难以计算。本文据此采用混合架构：让大语言模型近似承担语义推断和长程规划等复杂计算，同时由传统规则或验证模块严格检查动作能否执行。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**去中心化部分可观测马尔可夫决策过程（Dec-POMDP）**

Dec-POMDP用于描述多个智能体在无法完整观察全局状态、只能依据各自局部信息采取行动时的协作决策。它为私有目标、交互历史、联合行动和团队收益提供统一建模框架，但一般情况下精确求解的计算代价很高。

</div>
<div class="concept-item" markdown="1">

**计算心智理论（Theory of Mind, ToM）**

ToM推断把他人的可观察行为视为关于其隐藏目标、信念或偏好的证据。本文所需的关键能力是根据人类已经采取的动作，更新机器人对人类私有目标的判断。

</div>
<div class="concept-item" markdown="1">

**零样本协调**

零样本协调指机器人无需针对当前人类伙伴与当前目标组合重新训练，就直接利用已有模型和任务描述开展合作。它要求系统能在交互过程中推断伙伴意图并及时调整策略，而不能依赖预先反复练习同一组合。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究场景是一个受 La Boca 游戏启发的合作建造任务：一名人类与一个机器人共同搭建三维结构，但双方各自只能看到一个私有的二维目标投影。任何单独视图都不足以唯一确定最终三维目标，因此机器人的输入包括自身私有目标视图、当前建造状态、对话内容以及人类和机器人此前的动作历史；其输出是下一步物理建造动作或必要的沟通行为。任务假设双方具有合作目标，但信息不对称，机器人不能直接读取人类的私有视图，并且每个候选动作都必须满足几何、动力学或可用资源等精确约束。系统最终需要通过持续推断、分层规划、沟通解释、动作验证和反馈重规划，使双方完成与两个投影一致的可行三维结构。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **意图推断、逆向规划与计算心智理论方法（文中引用[2, 3, 6]）**: 这些方法从已观察到的动作反推隐藏目标、信念或偏好，为本文依据人类行动推断其私有目标提供直接理论基础；本文进一步把这种推断嵌入完整的人机协作规划流程。
- **采用外部安全约束的LLM规划方法（文中引用[7, 8, 20]）**: 这类工作使用可达性分析、时序逻辑约束或程序化验证，在执行前检查或修改LLM生成的计划。本文沿用相同的混合系统原则，由LLM处理语义推理和长程规划，由传统验证机制保证建造动作的物理可行性。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现实中的混合人机团队经常面临非对称信息：每个成员可能拥有对方无法直接观察的目标、偏好或局部观测。在此条件下，机器人不仅要完成物理任务，还必须依据交互历史识别与协作有关的隐藏变量、决定何时沟通，并根据新证据修订计划。如果机器人不能理解人的意图，即使单个动作都合法，也可能采取在人看来目的不明、效率低或难以信任的行为。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **分散式部分可观测马尔可夫决策过程与多智能体强化学习**：分散式部分可观测马尔可夫决策过程用统一的决策模型表示多个协作者的私有观测、联合状态、动作及长期团队目标；多智能体强化学习则通过大量重复交互或离线训练，学习能够产生协同行为的策略。前者提供严谨的问题结构，后者尝试以数据驱动方式绕开直接求解复杂规划问题。
- **大语言模型规划、计算心智理论与外部安全验证**：大语言模型方法利用语言推理完成高层规划、任务分解、交流解释和执行失败后的计划修订；计算心智理论或逆向规划方法把人的可观测动作当作关于其潜在目标、信念或偏好的证据；外部验证方法则用可达性分析、时序逻辑或程序规则，在执行前检查或修改模型生成的计划。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 精确的分散式部分可观测马尔可夫决策过程推断与规划在问题规模增大后会迅速变得计算上不可处理，而多智能体强化学习通常依赖针对大量目标组合进行反复训练；这使其难以直接满足面对新目标或新伙伴时的零样本协调需求。
- 既有相关架构通常只覆盖隐含意图推断、语言交流、长程规划、执行恢复或安全验证中的一部分，尚未把这些能力组织成面向私有目标协作的完整闭环；此外，仅保证动作物理可行并不能保证行为对人而言易于理解、协调有效或值得信任。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

仍缺少一种统一的人机协作架构，能够保留决策论模型对私有信息与序贯决策的清晰分解，又不必精确求解其高复杂度推断和规划；该架构还需同时吸收自然语言与行为证据、在交互中更新对人类目标的估计，并以确定性机制守住物理可行性边界。

</div>
<div markdown="1"><span>核心问题</span>

在合作伙伴目标不可直接观察、任务又受到严格物理约束时，能否用结构化大语言模型近似完成目标推断和层级规划，并结合对话解释、反馈重规划及规则验证，在不针对每个新目标组合重新训练的情况下，提高人机协调效率和人的信任体验？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是按不同模块的优势分工：大语言模型擅长从含糊的动作和语言线索中形成语义层面的目标假设，并生成可随反馈修改的高层方案，但不适合可靠地记住全部精确合法动作；规则验证器则不理解人的意图，却能稳定判断候选动作是否违反几何、资源或搭建约束。以决策论结构串联二者后，系统可以先“推测对方想做什么并制定方案”，再“检查这一步实际上能不能做”，失败时依据验证或交互反馈重新规划，从而兼顾开放式推理与硬约束可靠性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法面向具有私有目标视图的零样本人机协作建造任务，将问题建模为有限时域的去中心化部分可观测马尔可夫决策过程（Dec-POMDP）。机器人只能直接看到自己的目标视图 $g^{R}$，需要依据公共建造状态、历史动作与对话，推断人的目标视图 $g^{H}$，再生成并执行协作动作。整体架构由基于大语言模型（LLM）的行动条件心智理论推断、分层规划、对话处理和反馈重规划组成，并以规则验证器作为物理可执行性的最终检查器。直观地说，机器人先猜测人的目标和意图，再决定当前应完成的小目标，提出具体摆放或移除动作；只有通过结构约束检查的动作才会执行，失败动作则根据明确的失败原因修改后重试。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 维护公共状态与私有信息

系统记录网格占用 $O_t$、尚未放置的部件集合 $R_t$、动作、消息、子目标和验证反馈，并把这些内容组织为结构化交互记忆。机器人保留对人类目标的近似信念 $b_t^{H}$，该信念随新的人类摆放、移除、确认和消息而更新。

<div class="method-step__io" markdown="1">

**输入**：输入包括当前物理状态 $x_t=(O_t,R_t)$、轮到行动的参与者 $rho_t$、机器人的目标视图 $g^{R}$、公开可观察的历史 $C_t$，以及人类在其私有目标视图 $g^{H}$ 下产生的动作和语言信息。<br>
**输出**：得到供后续模块使用的规划上下文 $mathcal{K}_t$，其中包含物理状态、机器人目标、人类目标信念和相关交互历史。

</div>

**直观理解**：这一步相当于建立一份持续更新的团队工作记录：机器人知道桌面上有什么、还剩什么、双方说过什么，也记录自己对人类真正目标的当前猜测。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 行动条件的心智理论推断

对于每个候选目标，行动生成模块 $mathsf{LLM}_{\mathrm{act}}$ 预测在该目标下可能出现的人类动作集合 $widehat{\mathcal{A}}_t^{H}(g)$；比较模块 $mathsf{LLM}_{\mathrm{compare}}$ 将预测动作与实际观察到的动作进行一致性比较，产生目标兼容性值。机器人据此构造对各候选人类目标的近似概率分布，并把结果传给规划和对话模块。

<div class="method-step__io" markdown="1">

**输入**：输入是候选人类目标 $g
i
author?  $g\in\mathcal{G}^{H}$、从人类视角表示的当前建造状态 $x_t^{H}$、历史信息 $h_t$ 和已观察到的人类行动历史 $h_t^{H}$。<br>
**输出**：输出人类目标信念 $b_t^{H}$ 或其近似更新结果，以及各候选目标与观察行为的兼容性信息。

</div>

**直观理解**：机器人不是只根据一句话猜目标，而是逐个假设“人可能想完成这个结构”，再检查人已经做的动作是否像是在追求该结构；越吻合的假设，可信度越高。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分层任务规划与对话整合

高层规划器 $mathsf{LLM}_{\mathrm{high}}$ 先选择中间建造子目标 $z_t$，并生成意图、子目标描述和理由；低层规划器 $mathsf{LLM}_{\mathrm{low}}$ 再依据 $mathcal{K}_t$ 和 $z_t$ 生成候选物理动作。对话模块把人类语音转写为结构化意图、部件、操作和坐标信息，决定是否澄清、解释、接受、修改或拒绝建议，并在必要时更新子目标或触发新动作提议。

<div class="method-step__io" markdown="1">

**输入**：输入为规划上下文 $mathcal{K}_t$，包括当前状态、机器人目标、人类目标信念、剩余部件和历史；对话模块还接收语音转写文本及相关对话上下文。<br>
**输出**：输出当前子目标 $z_t$、候选动作 $\widetilde{a}_t^{R}$、结构化对话信息、机器人回复，以及可能的计划修改信号。

</div>

**直观理解**：系统先决定“这一轮要完成哪一小块建造”，再决定“具体拿哪块部件放到哪里”。人的语言建议不会直接绕过规划，而是先被整理和评估，再纳入计划。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 规则验证、执行与反馈重规划

规则验证器检查部件是否仍可用、是否越界或与已有部件重叠、放置后是否满足支撑约束，以及操作特定的可行性规则。若验证通过，机器人执行动作并更新状态与记忆；若失败，验证器返回违反的约束 $e_t$，重规划器据此修改动作并重新验证，同时尽可能保留原高层子目标。

<div class="method-step__io" markdown="1">

**输入**：输入为当前物理状态 $x_t$ 和候选动作 $\widetilde{a}_t^{R}$，其中动作包含操作类型、部件、锚点坐标和方向。<br>
**输出**：输出可执行动作及更新后的状态，或输出经过失败反馈修订的新候选动作，直到通过验证或由系统决定停止。

</div>

**直观理解**：LLM 可以提出不现实的摆放方案，因此由明确的程序检查“能不能真的放”。这像给规划者配一个严格的施工检查员：方案不合格时说明具体哪里错，而不是只说“不行”。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 人类目标信念的贝叶斯更新

$$
b_{t+1}^{H}(g)=\frac{q_{t}^{H}(e_{t}^{H}\mid g,C_{t},g^{R})b_{t}^{H}(g)}{\displaystyle\sum_{\bar{g}\in\mathcal{G}^{H}}q_{t}^{H}(e_{t}^{H}\mid\bar{g},C_{t},g^{R})b_{t}^{H}(\bar{g})}
$$

**符号说明**

- $b_t^H(g)$：在时刻 $t$ 机器人认为人类目标视图为 $g$ 的概率。
- $e_t^H$：人类在当前回合产生的可观察证据，包括物理动作和消息，即 $e_t^H=(a_t^H,m_t^H)$。
- $q_t^H(e\mid g,C_t,g^R)$：假设人类目标为 $g$ 时，在公共历史 $C_t$ 和机器人目标 $g^R$ 条件下产生证据 $e$ 的响应模型。
- $mathcal{G}^H$：可能的人类目标视图集合。
- $C_t$：截至时刻 $t$ 的公共交互历史，包括状态、行动轮次、动作和消息。

<div class="equation-explanation" markdown="1">

**直观理解**：公式把旧信念与新观察结合起来：某个目标越能解释人刚刚的动作或话语，其更新后的概率越高。论文用 LLM 生成并比较目标条件行为来近似其中难以直接计算的响应模型 $q_t^H$，因此不必显式求解每个候选目标对应的完整人类策略。<br>
**原文位置**：Section II-B，公式（1）；Section III-B

</div>

</div>

<div class="equation-block" markdown="1">

#### 分层规划映射

$$
z_t=\mathsf{LLM}_{\mathrm{high}}(\mathcal{K}_t),\qquad\widetilde{a}_t^{R}=\mathsf{LLM}_{\mathrm{low}}(\mathcal{K}_t,z_t)
$$

**符号说明**

- $mathcal{K}_t$：时刻 $t$ 的规划上下文，包括物理状态 $x_t$、机器人目标 $g^R$、人类目标信念 $b_t^H$ 和相关交互历史。
- $z_t$：高层规划器选择的中间建造子目标。
- $tilde{a}_t^R$：低层规划器生成、尚未通过验证的机器人候选物理动作。
- $mathsf{LLM}_{mathrm{high}}$：根据规划上下文选择意图和中间子目标的高层 LLM。
- $mathsf{LLM}_{mathrm{low}}$：根据上下文和子目标生成具体操作、部件、位置及方向的低层 LLM。

<div class="equation-explanation" markdown="1">

**直观理解**：该公式表达先定施工目标、后定具体动作的两级决策结构。这样，低层动作即使因物理约束失败而被修改，也可以继续服务于同一个高层子目标。<br>
**原文位置**：Section III-A，Hierarchical LLM Task Planner；Figure 3

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文给出的章节描述的是零样本推理架构，而不是在本任务上训练一个新的端到端参数模型。理论上的团队目标是在策略 $\pi^H$ 和 $\pi^R$ 上最大化成功完成奖励，同时惩罚交互时间、不必要的纠正动作和无效提议；但本文所选章节未给出该目标的具体数值权重、损失函数实现或 LLM 参数更新过程。因此，方法的优化主要体现为推理时的近似决策、目标信念更新、分层规划和验证反馈循环，而非报告一个明确训练损失的梯度优化过程。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. LLM行动条件心智理论模块**

该模块近似实现 Dec-POMDP 中对人类私有目标的贝叶斯逆向规划。对每个候选目标 $g$，首先用 $mathsf{LLM}_{\mathrm{act}}(x_t^{H},g,h_t)$ 生成目标条件的人类行为预测，再用 $mathsf{LLM}_{\mathrm{compare}}(h_t^{H},\widehat{\mathcal{A}}_{0:t}^{H}(g))$ 评估预测与已观察行为的一致性，从而近似人类响应似然并更新 $b_t^{H}$。

> 直观理解：它解决的是“人没有公开告诉机器人目标是什么”的问题。用 LLM 直接生成和比较候选行为，避免为每个可能目标都完整求解一次人类最优决策。

**2. 分层LLM规划与对话模块**

规划器把决策分为高层子目标选择和低层动作生成：$z_t=\mathsf{LLM}_{\mathrm{high}}(\mathcal{K}_t)$，$\widetilde{a}_t^{R}=\mathsf{LLM}_{\mathrm{low}}(\mathcal{K}_t,z_t)$。对话处理链路将人类语音转写为文本，抽取意图和装配建议，并结合机器人目标、人类目标信念和当前状态决定回复或计划更新。

> 直观理解：分层设计把“想达成什么”和“怎样具体操作”分开，减少一次性生成复杂动作的困难；对话模块则让语言成为计划和目标推断的输入，而不只是附加的聊天功能。

**3. 规则动作验证器与反馈重规划器**

验证器执行确定性的可行性判断：$\mathsf{V}(x_t,\widetilde{a}_t^{R})$ 在动作属于 $\mathcal{A}_{\mathrm{feas}}(x_t)$ 时返回有效，否则返回无效及失败原因 $e_t$。重规划器接收上下文、当前子目标、被拒绝动作和失败解释，修改操作、部件、位置或方向后再次提交验证。

> 直观理解：该模块把语言模型的灵活推理与物理世界的硬约束分开。LLM负责提出方案，程序负责保证方案不会越界、重叠或悬空。

**训练与推理**

训练方面，所给章节未报告对本架构中的 LLM 模块进行任务特定微调，也未说明为 ToM 模块学习一个新的参数化人类策略。推理时，系统首先读取机器人目标、当前网格状态、剩余部件、交互记忆和人类目标信念；在人类回合后，根据动作和消息更新目标假设。随后高层 LLM 生成子目标，低层 LLM 生成具体候选动作；语音输入经过 gpt-4o-mini-transcribe 转写，再由 gpt-4.1-nano 抽取意图和装配建议，可能触发对话回复或计划更新。候选动作必须经过规则验证，验证失败时把结构化失败原因反馈给重规划器，修订后的动作重新进入验证环节，验证通过后才执行并更新状态。

**复现信息**

任务环境是 $\mathcal{W}=\{1,2,3,4\}^{3}$ 的离散三维网格，实验使用九个不同形状和颜色的刚性部件。机器人动作采用 $a_t^R=(\alpha_t^R,p_t^R,c_t^R,o_t^R)$ 表示，其中操作类型为放置、移除或等待，另含部件、锚点单元格和适用时的方向；验证器检查部件可用性、边界、单元格占用、结构支撑及操作规则。系统显式保存状态、动作、子目标、验证反馈和从对话中抽取的信息，以便在后续回合复用。所给章节未明确报告提示词、LLM 温度、上下文长度、重试上限、信念初始化、语音接口参数或具体软件版本，因此这些内容不能据此复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 人类参与者试验：这是试点性质的被试内实验，共招募 5 名、年龄为 25 至 30 岁的研究生。每名参与者分别与 LLM+ToM、无 ToM 的 LLM 和 RL 三种机器人策略协作完成 La Boca 搭建任务；机器人与人类从相反视角观察结构，并持有不同的私有目标视图。三种策略的出场顺序及对应的人类目标视图均随机分配。它不是预先划分训练集和测试集的数据集，而是用于比较真实人机协作行为及主观信任的现场评估样本。
- 目标视图集合：机器人使用一个固定目标视图，人类每次试验从 3 个候选目标视图中随机获得一个。ToM 评估还加入 1 个不会实际分配给参与者的干扰视图，因此机器人需要在共 4 个假设上维护对人类目标的信念；该集合用于检验机器人能否根据动作和对话逐步排除错误目标。
- 仿真评估集：分别测试 RL/RL、LLM/RL 和 LLM/LLM 三种角色配置，每种配置运行 10 个 episode，每个 episode 最多允许 15 步，超过该上限仍未完成即记为失败。该评估用于在固定预算下比较智能体组合的任务成功率和交互效率，不涉及原文明确报告的训练集、验证集或独立测试集划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**交互步数**

完成任务或参与者终止交互前记录的决策与行动步数，用于衡量协作过程的简洁程度。RL 条件包含未完成的部分轨迹，因此其步数不能直接视为标准的完成时间。 （在任务成功且比较口径一致时越低越好，因为更少步骤表示双方更快形成一致计划；若失败或提前终止，单独追求较低步数没有意义。）

</div>
<div class="metric-item" markdown="1">

**任务成功率与完成情况**

衡量任务是否在允许预算内完成。人类试验报告成功完成及参与者主动终止情况；仿真则把 15 步内未完成的 episode 计为失败，并汇总成功率。 （越高越好，因为它直接表示策略能否把共享搭建任务执行到符合目标的终态。）

</div>
<div class="metric-item" markdown="1">

**Trust Perception Scale–HRI 信任分数**

参与者在实验前以及每种策略交互后填写的人机交互信任量表分数，用于评价机器人行为带来的主观可信度变化。 （越高越好，因为更高分表示参与者对机器人的感知信任更强；但它是小样本主观量表，不能替代客观任务性能或证明长期信任。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 真实人机协作中的任务效率与完成情况

<div class="result-value" markdown="1">

LLM+ToM、无 ToM 的 LLM 和 RL 的平均记录交互步数分别为 5.2、6.4 和 10.2。两个 LLM 条件下所有参与者均完成任务；RL 条件仅 1 人完成且用了 9 步，其余 4 人因对机器人行为感到沮丧而在 8 至 14 步后终止。

</div>

作者据此主张，结构化 LLM 系统在该试点中比离线 RL 更高效，也更可能把任务执行完。分析上，最稳健的信号其实是完成情况的明显差异，而不是把 5.2 与 10.2 直接当作完成速度比较：RL 的均值混合了 1 条完成轨迹和 4 条提前终止轨迹，统计含义与 LLM 条件的完整轨迹不同。该结果也不能证明 LLM 在一般机器人任务中优于 RL，因为任务、训练覆盖范围和样本规模都很有限。

<div class="result-source" markdown="1">

来源：第 IV-B 节“Task efficiency and completion”，图 7(a)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Fig. 7(a), the mean number of logged interaction steps was 5.2 for LLM+ToM, 6.4 for the LLM ablation, and 10.2 for RL. Using the LLM planners, all participants successfully completed the task. Only one participant completed the RL condition, doing so in nine steps. The remaining four participants terminated the interaction after eight to fourteen steps because of frustration with the robot’s behavior.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 真实人机交互前后的感知信任

<div class="result-value" markdown="1">

实验前平均信任分数为 68.6；与 LLM+ToM、无 ToM 的 LLM 和 RL 交互后，平均分分别为 84.9、81.1 和 57.1。完整系统得到最高均值，而 RL 交互后的均值低于实验前水平。

</div>

作者将该结果解释为结构化 LLM，尤其是完整 LLM+ToM，更有利于参与者的信任体验。完整系统相对消融条件只高 3.8 分，原文也称这一差异较小；在没有显著性检验、量表离散程度和顺序效应分析的情况下，不能断言 ToM 本身可靠地提高了信任。RL 条件的下降还可能同时受到失败、交互过长和参与者沮丧等因素影响。

<div class="result-source" markdown="1">

来源：第 IV-B 节“Trust”，图 7(b)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The mean pre-experiment score was 68.6. Mean post-interaction trust increased to 84.9 under LLM+ToM and 81.1 under the LLM ablation, whereas it decreased to 57.1 after interaction with the RL policy. The complete architecture received the highest mean trust score, although the difference between the two LLM conditions was modest.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 15 步预算下的三种仿真智能体配置

<div class="result-value" markdown="1">

在每种配置 10 个 episode 的仿真中，RL/RL 的成功率为 100%，平均使用 5 步；LLM/RL 的成功率为 0%，达到 15 步上限；LLM/LLM 的成功率为 60%，平均使用 12 步。

</div>

结果显示策略类型之间的搭档兼容性非常关键：RL 与同类伙伴配合最好，异构的 LLM/RL 组合完全失败，而 LLM/LLM 只能部分成功。这使人类实验中“LLM 优于 RL”的结论不能简单推广到任意搭档配置，也提示 RL 在其训练或自博弈分布内可以十分有效。表中的平均步数是否只对成功 episode 计算，原文节选未明确说明；因此 LLM/RL 的 15 步更合理地理解为触及失败上限。

<div class="result-source" markdown="1">

来源：表 I“Simulation performance under different agent configurations”，第 IV-C 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

RL/RL | 100% | 5
LLM/RL | 0% | 15
LLM/LLM | 60% | 12

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

- LLM（无 ToM）消融基线：保留与完整方法相同的分层规划、对话解释、动作验证和反馈重规划模块，但不显式估计人类的私有目标，也不向规划及对话模块提供 ToM 信念。它与完整系统只在 ToM 信息这一关键因素上不同，因此是判断显式伙伴目标推断是否产生增益的最直接对照。
- 离线多智能体 RL 基线：由两个 MaskablePPO 策略通过交替式合作自博弈训练；每一阶段更新一个策略，另一个保持固定并作为伙伴。训练时采用集中式价值函数，使 critic 可额外观察伙伴当前视图和私有目标；执行时 actor 只能使用自己的局部观测和私有目标。该基线代表经过多目标组合离线训练、但在部署时仍需去中心化决策的传统学习方案。
- RL/RL 仿真配置：双方均由强化学习策略控制，用来测量同类 RL 策略在受控搭档条件下的上限表现，并判断人类试验中的 RL 困难是否也会出现在 RL 自身熟悉的策略分布内。
- LLM/RL 与 LLM/LLM 仿真配置：前者检验异构规划范式之间能否协调，后者检验两个 LLM 规划器相互配合时的成功率。二者共同帮助区分单个策略能力与搭档兼容性，但并不是对完整 LLM+ToM 人机系统的严格等价复现。

**实验想回答的问题**

- 在具有私有目标视图的协作搭建任务中，显式的行动条件化心智理论（ToM）推断能否相较于不含 ToM 的同构 LLM 系统及离线多智能体强化学习策略，提高人机协作的任务效率、完成率与参与者信任？
- 在受控仿真中，不同类型的智能体搭配，即 RL/RL、LLM/RL 和 LLM/LLM，能否在限定步数内稳定完成任务；由此可观察到的成功率和效率差异是什么？

**实验实现**

每名参与者都经历三种实验条件：完整 LLM+ToM、无 ToM 的 LLM 消融和离线 RL。条件顺序与目标视图分配在实验开始时随机化，以降低固定顺序和特定目标组合造成的混杂。参与者通过带麦克风的无线扬声器与机器人交流，并在实验前及每个条件结束后填写 Trust Perception Scale–HRI。原文还记录完成时间、无效动作提议和重规划次数，但节选没有给出这些指标的数值结果。LLM 模块采用 GPT-5.4 nano，作者说明选择该模型是为了控制交互延迟和计算成本；完整与消融条件共享规划、对话、验证和重规划实现，仅 ToM 输入不同。

RL 策略训练采用交替合作自博弈及集中训练、分散执行：训练时 critic 可以看到伙伴信息，执行时 actor 看不到伙伴目标。仿真中每种智能体配置运行 10 次，最多 15 步。人类实验属于仅 5 人的 pilot study；原文展示均值和个体观察，但节选没有报告方差、置信区间、显著性检验、效应量或功效分析，因此结果应视为初步描述性证据。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除显式 ToM 目标估计，但保留分层规划、对话、动作验证和反馈重规划 | 完整 LLM+ToM 的平均交互步数为 5.2，无 ToM 的 LLM 为 6.4，即移除 ToM 后平均增加 1.2 步；两种条件下所有参与者都完成了任务。 | 该对照主要隔离“是否把人类私有目标的显式估计提供给规划和对话模块”这一因素。方向上，ToM 使协作更精简，但没有改变本试点中 LLM 系统均能完成任务的事实。由于只有 5 名参与者，且原文没有报告配对差值、误差范围或显著性检验，这 1.2 步差异只能视为支持假设的描述性趋势。 | 第 IV-B 节“Task efficiency and completion”，图 7(a)<br><span class="experiment-evidence">As shown in Fig. 7(a), the mean number of logged interaction steps was 5.2 for LLM+ToM, 6.4 for the LLM ablation, and 10.2 for RL. Using the LLM planners, all participants successfully completed the task.</span> |
| ToM 对交互后信任的消融影响 | 完整 LLM+ToM 的平均交互后信任为 84.9，无 ToM 的 LLM 为 81.1，完整系统高 3.8 分；作者明确指出两种 LLM 条件之间的差异较小。 | 因为两种 LLM 条件的其余模块相同，该比较可初步检验显式目标推断是否改善主观体验。不过 ToM 可能通过减少步骤、改变对话内容或降低协调摩擦间接影响信任，实验没有进一步分解这些机制；3.8 分也没有配套统计检验，不能据此断言存在可靠的 ToM 信任效应。 | 第 IV-B 节“Trust”，图 7(b)<br><span class="experiment-evidence">Mean post-interaction trust increased to 84.9 under LLM+ToM and 81.1 under the LLM ablation, whereas it decreased to 57.1 after interaction with the RL policy. The complete architecture received the highest mean trust score, although the difference between the two LLM conditions was modest.</span> |

**定性案例**

- ToM 信念轨迹提供了机制层面的定性证据：系统在 4 个候选目标上从均匀信念开始，并在每两次交互后更新一次；由于任务平均较短，每次任务通常只有两次更新。作者报告正确目标的平均信念在每次更新后都上升，表明模块能逐步聚焦参与者意图。但节选未给出各更新点的具体概率、离散程度或逐参与者轨迹，因此这只能说明平均趋势，不能判断目标何时稳定成为最高概率假设，也不能排除少数失败推断被均值掩盖。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Uses structured LLM theory-of-mind inference, hierarchical planning, verification, and replanning for zero-shot human-robot coordination.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`6e2d688668382694c2d3ca890536b06e3425c674d9d2575b71f82e6adc31ed0b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
