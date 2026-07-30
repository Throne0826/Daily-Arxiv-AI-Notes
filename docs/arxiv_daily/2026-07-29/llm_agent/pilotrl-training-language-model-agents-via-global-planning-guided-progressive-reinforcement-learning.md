---
title: "[论文解读] PilotRL: Training Language Model Agents via Global Planning-Guided Progressive Reinforcement Learning"
description: "[arXiv 2508.00344][LLM Agent] 本文针对语言模型智能体缺乏长程规划、规划与执行协同不足以及监督微调泛化受限的问题，提出自适应全局规划范式 AdaPlan，并以三阶段渐进式强化学习框架 PilotRL 依次训练计划遵循、计划生成和规划—执行协同能力。"
arxiv_id: "2508.00344"
announcement_date: "2026-07-29"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T07:32:03.653701+00:00"
source_sha256: "c5c1cc70bf20dfe751b71cc290fbf7e4af074ff725a43f4586eb93b51f986cfd"
tags:
  - "LLM Agent"
  - "强化学习"
  - "LLM 效率"
  - "LLM 其他"
  - "大语言模型智能体"
  - "长程规划"
  - "全局计划"
  - "规划与执行协调"
  - "AdaPlan"
  - "PilotRL"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2508.00344</p>

# PilotRL: Training Language Model Agents via Global Planning-Guided Progressive Reinforcement Learning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-29</span>
<span><strong>作者</strong> Keer Lu, Chong Chen, Bin Cui, Yunhuai Liu, Wentao Zhang</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2508.00344v5) · [PDF 下载](https://arxiv.org/pdf/2508.00344v5) · **关键词** 大语言模型智能体, 长程规划, 全局计划, 规划与执行协调, 强化学习, AdaPlan, PilotRL  


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

本文针对语言模型智能体缺乏长程规划、规划与执行协同不足以及监督微调泛化受限的问题，提出自适应全局规划范式 AdaPlan，并以三阶段渐进式强化学习框架 PilotRL 依次训练计划遵循、计划生成和规划—执行协同能力。

**不用术语来说**：复杂智能体任务通常需要连续完成多个相互依赖的步骤，并根据执行结果及时调整后续安排；但常见语言模型智能体往往只考虑眼前一步，或者先生成计划再交给与规划器缺乏配合的执行器，因而容易在长任务中偏离目标。若主要依靠标准答案轨迹进行监督训练，模型还可能记住特定任务的解法，而不能把能力稳定迁移到陌生情境。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 AdaPlan：在任务执行期间动态生成并持续更新全局计划，以高层目标和整体步骤指导当前行动，而不是仅依赖逐步的局部推理。
- 将全局规划器与执行器置于同一个语言模型中，使计划的表达方式与模型实际可执行的能力共同适应，减少独立设计两者造成的接口和能力错配。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型智能体研究。智能体以大语言模型作为核心决策器：模型接收任务目标和环境反馈，进行推理并输出可被环境执行的动作，由此形成“观察—决策—行动—新观察”的交互循环。研究重点不是一般的文本生成，而是在家庭探索、游戏或工具使用等需要连续多步操作的环境中，让开源模型既能从全局上规划通往目标的步骤，又能根据执行结果调整计划并可靠地完成动作。闭源模型虽常有较强智能体能力，但存在调用成本和安全风险，因此本文关注如何通过训练提升开源模型的长程决策能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**大语言模型智能体（LLM Agent）**

以大语言模型承担感知信息解释、任务推理和动作决策的系统。它通常需要与外部环境反复交互，而不是一次生成完整答案。

</div>
<div class="conceptitem" markdown="1">

**ReAct**

一种交替生成“思考”和“动作”的智能体范式，每一步根据当前观察推断接下来立即要做什么。其局部逐步决策方式易于执行，但在需要预见多个后续步骤时可能缺少全局视角。

</div>
<div class="conceptitem" markdown="1">

**全局规划器与执行器**

全局规划器根据任务和当前环境形成较高层的多步行动指导，执行器再把指导转化为具体动作。二者若分别设计或训练，计划可能超出执行器能力，执行器也可能无法正确遵循计划。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个需要多轮环境交互才能完成的智能体任务，模型在每一步接收任务目标、已有交互上下文以及环境返回的观察，并输出高层全局计划或可执行动作；动作执行后产生的新观察继续反馈给模型，直至任务成功、失败或达到交互限制。论文假设复杂任务需要跨越多个步骤的前瞻规划，而且计划必须随环境状态和执行结果动态更新；同时，全局规划与动作执行由同一个开源语言模型承担，以减少独立规划器和执行器之间的能力错配。研究目标是训练该统一模型，使其先学会遵循显式计划，再提高计划质量，最终协调规划与执行，从而在新任务情境中获得更可靠的长程决策能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **ReAct（Yao et al., 2023）**: 本文的主要范式对照。ReAct把思维链推理与动作交替进行，适合作出基于当前观察的逐步决策；作者认为它缺乏对总体任务上下文和未来步骤的显式把握，因此在家庭探索、前瞻性游戏等复杂多步任务中受到限制。
- **基于专家轨迹的开源智能体监督微调（Chen et al., 2023, 2024；Song et al., 2024；Zeng et al., 2024；Zhang et al., 2024b）**: 这些方法利用GPT-4等强模型产生的轨迹对开源模型进行行为克隆。本文将其视为重要训练基线方向，但指出模型可能主要记忆任务特定启发式和既有轨迹，因而在分布外任务上的泛化能力有限，并据此转向强化学习。
- **GRPO（Shao et al., 2024；Guo et al., 2025）**: GRPO是面向大语言模型的强化学习算法，以同组候选输出的相对评价替代传统的独立评论家模型。它构成本文所处的强化学习技术背景，使智能体能够依据结果反馈探索策略，而不必对每一步提供显式监督；所给章节未进一步报告本文使用该算法的具体目标函数。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

研究需求来自开放式、长时程的智能体任务：模型必须感知环境反馈，连续作出多步决策，并在中间结果与预期不一致时调整路线。闭源模型还伴随较高调用成本与安全风险，因此需要提升开源语言模型作为智能体核心控制器时的可靠决策与泛化能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **ReAct 智能体范式**：模型交替生成针对当前状态的“思考”和立即执行的动作，再根据环境返回的观察继续下一轮决策；其核心是把单步推理与即时行动紧密结合。
- **独立规划器—执行器方法**：先由规划模块生成任务计划，再由另一个执行模块依据该计划与环境交互。该设计引入了高层规划，但规划器和执行器通常分别设计或优化。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- ReAct 的“思考”主要服务于下一步动作，缺少对任务总体上下文和远期依赖的显式把握；在需要顺序执行多个步骤的复杂任务中，模型容易形成局部合理但全局错误的决策。
- 规划器与执行器被孤立设计时，计划可能超出执行器能力、表达方式也可能不便于执行器遵循；这种错配会使看似合理的计划无法转化为有效行动，从而损害端到端任务表现。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未形成一种面向开源语言模型的统一训练方案，能够同时提供可随环境反馈更新的全局指导、使规划与执行在同一模型内相互适配，并避免仅靠模仿固定轨迹所带来的泛化局限。关键缺口不只是“有没有计划”，而是计划能否被实际执行、能否动态修订，以及这两种能力能否通过端到端训练共同提升。

</div>
<div markdown="1"><span>核心问题</span>

能否以自适应全局计划为中介，并通过分阶段强化学习，先建立模型遵循计划的能力，再改善计划本身，最后联合优化两者，从而提升语言模型智能体在长时程任务中的规划—执行协同与对新情境的泛化能力？

</div>
<div markdown="1"><span>作者直觉</span>

先让模型学会按导航行动，再训练它生成更好的导航，最后让“制定路线”和“实际驾驶”一起磨合，比一开始同时优化所有能力更容易获得稳定协作。执行过程中持续更新全局计划，则类似根据实时路况重新规划路线：既保留最终目标和整体步骤，又能吸收环境反馈；由同一模型兼任规划器和执行器，还可使计划自然地采用模型自身能够理解并落实的形式。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PilotRL由推理范式AdaPlan与三阶段渐进式强化学习组成。AdaPlan把智能体拆成全局规划器与执行器：规划器依据任务目标和当前交互历史生成多步计划，执行器在计划指导下选择环境动作；每次获得新观察后，规划器保留已经执行的计划前缀，并根据实际结果重写尚未执行的后续步骤。训练则按“先学执行计划、再学制定计划、最后联合协调”的顺序逐步改变优化重点，避免在规划能力和执行能力都不稳定时直接进行端到端联合学习。

从端到端角度看，模型接收任务指令、初始上下文和环境允许的动作空间，先输出一份高层行动路线，再逐步执行并接收环境反馈。第一阶段由DeepSeek-V3提供或筛选高质量计划，重点训练执行器遵守计划和正确使用动作；第二阶段让模型自行生成候选计划并择优，重点提高计划的正确性、可执行性与格式规范性；第三阶段不再分别强调某个局部模块，而以格式和任务最终完成质量为主要反馈，联合优化规划器与执行器。直观地说，这类似先让学生学会按导航行驶，再让其学习规划路线，最后训练其在道路变化时一边改路线、一边稳定驾驶。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始化全局计划

全局规划器生成初始计划\mathcal{P}^{(0)}=[p_1^{(0)},p_2^{(0)},\ldots,p_{N_0}^{(0)}]，其中每个p_i^{(0)}表示建议执行器在相应阶段采取的高层行动。

<div class="method-step__io" markdown="1">

**输入**：任务目标或指令G，以及执行前的初始上下文\mathcal{C}^{(0)}。  
**输出**：包含N_0个步骤、用于显式指导后续决策的初始全局计划\mathcal{P}^{(0)}。

</div>

**直观理解**：模型不是看到一步走一步，而是先列出一条完成任务的大致路线。计划给出方向，但不会被视为不可修改的固定脚本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计划引导的逐步执行

在时间步t，执行器综合计划指导与历史交互，选择动作a^{(t)}\in\mathcal{A}并提交给环境；输出必须符合规定的Thought/Action或Action格式。

<div class="method-step__io" markdown="1">

**输入**：当前全局计划\mathcal{P}^{(t-1)}、累计上下文\mathcal{C}^{(t-1)}、任务目标G和动作空间\mathcal{A}。  
**输出**：当前环境动作a^{(t)}，以及环境随后返回的观察o^{(t)}\in\mathcal{O}。

</div>

**直观理解**：执行器把计划中的高层要求翻译成环境真正接受的具体操作。历史信息用于避免重复动作，也帮助模型理解自己已经做到哪一步。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 反馈积累与计划自适应

系统把(a^{(t)},o^{(t)})加入累计上下文形成\mathcal{C}^{(t)}，随后由规划策略\pi保留索引i\leq t的已执行计划项，并依据最新上下文重新生成i>t的未来计划项。

<div class="method-step__io" markdown="1">

**输入**：本轮动作a^{(t)}、环境观察o^{(t)}、旧计划\mathcal{P}^{(t-1)}、任务目标G和先前上下文。  
**输出**：更新后的上下文\mathcal{C}^{(t)}与下一轮使用的自适应计划\mathcal{P}^{(t)}。

</div>

**直观理解**：已经发生的步骤不能被事后改写，但还没执行的路线可以随环境变化而调整。即使执行器偏离原计划，规划器也能从当前真实状态重新安排余下步骤。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 前两阶段的能力分解训练

阶段1使用前沿模型生成并筛选计划，依据输出格式、动作对计划的遵循程度和端到端完成质量训练执行器；阶段2让待训练模型采用generate-then-select策略产生并选择计划，依据格式、端到端表现和计划质量训练规划器。

<div class="method-step__io" markdown="1">

**输入**：训练任务、环境交互轨迹、候选全局计划，以及DeepSeek-V3生成或评审的计划与评分。  
**输出**：先获得能够理解动作空间并遵守计划的执行器，再获得能够生成较正确、可执行且规范计划的规划器。

</div>

**直观理解**：作者先固定相对可靠的路线来训练“怎么走”，减少坏计划对执行学习的干扰；执行基础形成后，再训练模型自己判断“该走哪条路线”。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="equation-block" markdown="1">

#### AdaPlan未执行计划后缀的自适应更新

$$
p_i^{(t)}=\begin{cases}p_i^{(t-1)}, & \text{if } i\le t,\\ \pi\!\left(p_i^{(t)}\mid G,\mathcal{C}^{(t)},\mathcal{P}^{(t-1)},i\right), & \text{if } i>t.\end{cases}
$$

**符号说明**

- $p_i^{(t)}$：第t轮更新后，全局计划中索引为i的计划步骤。
- $t$：当前智能体—环境交互的时间步。
- $i$：计划步骤的索引；i\le t表示已经执行或已经经过的部分，i>t表示未来部分。
- $\pi$：全局计划生成器使用的计划适应策略。
- $G$：需要完成的任务目标或任务指令。
- $\mathcal{C}^{(t)}$：截至时间步t积累的动作与环境观察上下文。
- $\mathcal{P}^{(t-1)}$：执行当前动作之前使用的上一版全局计划。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把计划分成已发生的前缀和可调整的后缀：前缀原样保留，后缀根据任务目标、真实交互历史和旧计划重新预测。它是AdaPlan区别于一次性全局规划的关键，因为模型既保留历史一致性，又能根据意外结果改道。  
**原文位置**：第2.1节，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 阶段1的离散执行质量奖励

$$
\mathcal{R}_{format}=\begin{cases}1,&\text{if the format is correct},\\0,&\text{if the format is incorrect},\end{cases}\qquad \mathcal{R}_{adherence}=\begin{cases}2,&\text{if completely compliant},\\1,&\text{if partially compliant},\\0,&\text{if noncompliant},\end{cases}\qquad \mathcal{R}_{E2E}=\begin{cases}2,&\text{if accomplished efficiently},\\1,&\text{if accomplished with redundancy},\\0,&\text{if unaccomplished}.\end{cases}
$$

**符号说明**

- $\mathcal{R}_{format}$：输出格式奖励；满足规定的Thought/Action或Action结构及可读性要求时为1，否则为0。
- $\mathcal{R}_{adherence}$：动作对当前计划步骤的语义遵循奖励；完全遵循、部分遵循和不遵循分别取2、1、0。
- $\mathcal{R}_{E2E}$：完整交互轨迹的端到端表现奖励；高效完成、带冗余完成和未完成分别取2、1、0。

<div class="equation-explanation" markdown="1">

**直观理解**：三个信号分别检查“输出能否被系统解析”“当前动作是否按计划执行”和“整条轨迹最终是否有效”。阶段1使用这些分量的归一化结果之和，但原文节选没有给出归一化公式或各分量权重，因此不能据此断定三者在数值上等权。  
**原文位置**：第2.2.1节，公式(2)、(3)、(4)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：PilotRL没有在所给章节中给出一个贯穿三阶段的单一损失函数，而是为强化学习的不同阶段配置不同奖励。阶段1的奖励是归一化后的格式、计划遵循程度与端到端表现三类分量之和，目标是让执行器先掌握合法动作格式、动作空间以及按照外部计划行动的能力；阶段2的奖励是归一化后的格式、端到端表现与全局计划质量之和，目标转为提高模型自行规划的能力，其中计划质量由正确性、可执行性和规范性三个1至5分维度组成；阶段3的奖励是归一化后的格式与端到端表现之和，使规划器和执行器围绕最终任务完成情况联合协调。

这种逐阶段目标设计体现了一种能力课程：先减少执行噪声，再减少规划噪声，最后处理两者耦合。如果一开始只优化稀疏的任务成败信号，模型难以判断失败来自错误计划还是错误执行；PilotRL通过中间奖励把两类问题暂时拆开。需要注意，原文节选只说明各阶段采用归一化分量之和，没有明确报告归一化方法、奖励权重、具体强化学习算法、策略损失、价值函数、优势估计或正则项，因此这些内容不能从当前材料中补推。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 全局规划器**

规划器以任务目标G、累计上下文\mathcal{C}^{(t)}和上一版计划\mathcal{P}^{(t-1)}为条件，生成初始多步计划并在每轮交互后更新未执行部分。训练阶段2还采用generate-then-select：先生成多个可行候选，再按正确性、可执行性和规范性选择最合适的计划。

> 直观理解：它负责维护任务的长期方向，解决ReAct只围绕眼前一步思考、容易缺少连贯战略的问题。候选生成后再选择，相当于先比较若干路线，再把质量较高的一条交给执行器。

**2. 执行器**

执行器依据当前计划与历史动作—观察对选择a^{(t)}\in\mathcal{A}，并学习环境动作空间及规定的输出协议。阶段1使用语义遵循评分区分完全遵循、部分遵循和不遵循，避免仅凭任务最终是否成功而忽略执行器是否真正利用了计划。

> 直观理解：规划器只说要做什么，执行器负责把它变成工具调用或环境动作。单独训练遵循能力可防止出现“有计划但执行时完全不看”的名义规划。

**3. 环境反馈与自适应闭环**

环境在执行a^{(t)}后返回o^{(t)}，系统将其写入\mathcal{C}^{(t)}并同时反馈给执行器和规划器。规划器据此评估原策略是否仍然有效，只修改尚未执行的后缀，因此AdaPlan并非一次性静态规划。

> 直观理解：计划会接受现实结果的校正：工具失败、状态变化或执行偏差都可能使原路线失效，闭环更新让智能体从当前状态继续处理，而不是机械重复旧方案。

**4. 前沿模型监督与评审器**

DeepSeek-V3在阶段1提供候选计划并参与选择，同时评估动作遵循程度和完整轨迹的端到端表现；阶段2又对计划的正确性、可执行性和规范性分别给出1至5分。该模型提供的是训练奖励与高质量先验，不等同于待训练的最终骨干模型。

> 直观理解：环境通常只能告诉智能体成败，难以解释某一步是否合理；外部强模型充当教师和裁判，提供更细的中间反馈。不过这些奖励依赖评审模型的判断，其偏差也可能进入训练过程。

**训练与推理**

训练时，阶段1由DeepSeek-V3针对每个任务目标G和累计上下文\mathcal{C}^{(t)}先生成多个可能的全局计划，再从正确性、可执行性、格式有效性等角度选择最佳候选，用其指导待训练执行器。执行轨迹按照格式合法性、动作与当前计划步骤的语义一致性以及最终任务是否高效完成获得奖励；其中遵循和端到端评分也由DeepSeek-V3评估。该阶段结束后，模型应当能够理解可用动作并对显式计划作出相符的环境操作。

阶段2把学习重点转向规划器。模型先生成所有被认为可行的候选计划，再从候选池选择一个计划作为执行指导；计划同时接受正确性、可执行性和规范性评分，并结合格式奖励与端到端轨迹奖励进行强化学习。阶段3在前两项能力已经分别训练的基础上，以格式和端到端任务表现为直接反馈联合优化规划与执行，使局部计划质量和逐步遵循最终服务于完整任务，而不是成为彼此割裂的训练目标。

推理时不需要固定一份计划执行到底。规划器先根据G和\mathcal{C}^{(0)}产生\mathcal{P}^{(0)}；执行器在时间步t依据\mathcal{P}^{(t-1)}和\mathcal{C}^{(t-1)}选择a^{(t)}，环境返回o^{(t)}后形成新的上下文\mathcal{C}^{(t)}；规划器保持已经执行的计划项，并重写未来计划项得到\mathcal{P}^{(t)}。该循环持续到任务完成、失败或达到环境终止条件；具体终止规则在所给原文中未明确报告。

**复现信息**

复现和公平解释该方法时，需要保留两项关键协议。第一，执行输出只能采用“Thought: … Action: …”或“Action: …”形式，文本必须可读，环境反馈封装在<observation>...</observation>标签中；该协议直接参与格式奖励，并非纯粹的展示约定。第二，阶段1和阶段2采用generate-then-select策略，即先生成多个候选计划再由模型评估选择，而不是只对单次采样计划进行训练。

DeepSeek-V3承担计划先验与奖励评审器角色：它在阶段1提供和筛选计划，评估动作遵循及端到端轨迹；在阶段2对计划的三个质量维度评分。所给材料还报告作者对该评审器进行元评估：每个数据集抽取30个样本，Qwen2.5-7B-Instruct、LLaMA3.1-8B-Instruct和Qwen3-8B对应的跨数据集平均评审准确率均为0.98，但这只是评审可靠性的抽样证据，不能证明所有训练评分都无偏。当前节选未明确给出候选计划数量、采样温度、归一化方式、各奖励权重、强化学习优化器、学习率、批量大小、训练轮数、最大交互步数、参数更新范围，以及训练阶段之间是否重置优化器；这些均属于完整复现所需但原文节选不足以确定的信息。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- ALFWorld测试集用于域内评测，考查智能体能否在文本化交互环境中完成具有多步依赖的具身任务；原文节选未分别报告该测试集的样本数。
- IQA测试集用于域内评测，考查需要交互与推理的问答任务；原文节选未展开其全名、具体任务形式及测试样本数。
- TextCraft与Wordle的测试集共同用于域内评测：前者侧重具有开放性或创造性的文本生成，后者侧重通过多轮反馈进行词语推断。两者检验模型是否能在训练任务分布内进行持续决策；原文节选未分别报告样本数。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**任务完成率**

由DeepSeek-V3按照统一LLM-as-Judge协议，结合任务答案和参考轨迹，判断智能体是否完成目标。它衡量最终正确性，但会受到评审模型偏好影响。 （越高越好，因为更高表示成功完成任务的样本比例更大。）

</div>
<div class="metricitem" markdown="1">

**交互轨迹效率**

由同一评审模型评价完成任务所采用交互轨迹的效率，用于区分同样完成任务但步骤冗余程度不同的方案；所给节选未给出其精确评分公式。 （越高越好，因为更高表示完成任务的交互过程更有效率。）

</div>
<div class="metricitem" markdown="1">

**平均评测分数**

论文将任务完成率与交互轨迹效率计算为最终评价指标，并进一步汇总域内、域外或全部基准的平均表现。节选未明确两个组成部分的权重和归一化公式，因此不能将其简单理解为纯成功率。 （越高越好，因为它同时奖励任务成功与较高效的交互轨迹。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### PilotRL相对于Naive Response、开源智能体专用模型和外部规划器MPO的总体比较

<div class="result-value" markdown="1">

作者报告，PilotRL相对直接回答的平均下游任务表现提高78.51%；在相同Qwen2.5-7B-Instruct骨干条件下，相对DeepResearcher-7B高出超过29.47%；相对MPO平均提高31.10%。

</div>

这组比较表明，收益不只是来自调用一个更强的基础模型：额外智能体训练明显优于直接生成，而经过联合训练的全局规划与执行也优于推理时外挂规划器。后两项比较分别针对已有智能体模型和外部规划方案，但所给节选缺少表1逐数据集数值，无法检查优势是否均匀分布于六个基准，也不能据此单独确定训练数据、奖励设计和架构中哪一项贡献最大。

<div class="result-source" markdown="1">

来源：第3.2节 Main Results，表1总结文字

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Compared to the naive response, PilotRL enhances the average downstream task performances by 78.51%. Remarkably, when compared to open-sourced agent-specific models such as DeepResearcher-7B, our approach achieves over 29.47% higher performance with the same backbone model of Qwen2.5-7B-Instruct. In comparison to the plug-and-play external planner MPO, our method achieves an average improvement of 31.10%, further highlighting the importance of tight coordination between the planner and executor in effectively solving agent-oriented tasks.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 搭载PilotRL的开源模型与GPT-4o及GPT-4o-mini比较

<div class="result-value" markdown="1">

作者报告，集成PilotRL的模型平均超过GPT-4o 2.35%，并在参数规模更可比的条件下超过GPT-4o-mini 53.90%。

</div>

结果支持小型开源模型经专门的规划引导强化学习后，可以在论文采用的六个智能体基准及评审协议下达到很强的端到端表现。它并不证明模型在通用能力上全面优于GPT-4o，也未证明训练、推理成本或可用工具完全相同；结论应限定在该任务集合、提示方式和DeepSeek-V3评审协议内。

<div class="result-source" markdown="1">

来源：第3.2节 Main Results，表1总结文字

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Specifically, models integrated with PilotRL achieve an average improvement of 2.35% over GPT-4o, while showing a more substantial gain of 53.90% over GPT-4o-mini at a comparable parameter scale.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### PilotRL与SFT、Vanilla RL在三种骨干模型上的总体比较

<div class="result-value" markdown="1">

作者报告，PilotRL相对SFT和Vanilla RL的平均表现分别提高9.89%和7.64%。此外，在Qwen2.5-7B-Instruct与LLaMA3.1-8B-Instruct上，SFT在域内任务平均领先Vanilla RL 2.75%，而Vanilla RL在域外任务平均领先SFT 5.80%。

</div>

SFT与普通RL的接近说明，只引入全局计划监督或只引入端到端强化学习都能带来部分收益，但二者各有短板：SFT较擅长域内复现，普通RL在域外迁移上更强。PilotRL同时超过二者，支持“全局规划能力与强化学习结合”这一设计判断。不过这些是跨模型、跨基准平均值，不能说明每个数据集或每个骨干上都具有相同幅度的优势。

<div class="result-source" markdown="1">

来源：第3.2节 Main Results，表1总结文字

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Specifically, for in-domain (ID) tasks, SFT outperforms Vanilla RL by a marginal average of 2.75%, whereas Vanilla RL achieves an average lead of 5.80% in out-of-domain (OOD) tasks. In contrast, PilotRL demonstrates robust performance gains across models with diverse characteristics, achieving consistent improvements over both SFT and Vanilla RL by 9.89% and 7.64%, respectively.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评测和环境模拟都高度依赖前沿语言模型：DeepSeek-V3既模拟环境行为，又在主实验中充当评审器。即使参考轨迹与约98%的人类一致率降低了风险，模拟环境仍可能遗漏真实模拟器的状态约束，而同一模型生态中的生成与评分偏好也可能形成系统性偏差；TextCraft上较低的一致性已显示开放式任务尤其敏感。
- 主要结果采用跨六个基准、跨模型的平均分和相对提升进行概括，但所给节选缺少表1的逐数据集完整数值、方差、置信区间和多随机种子显著性检验。因此无法判断提升是否由少数数据集驱动，也无法评估训练随机性下的稳定程度。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- GPT-4o与GPT-4o-mini代表闭源前沿模型：前者用于比较PilotRL训练后的小型开源模型能否接近或超过强闭源系统，后者提供参数规模更可比的参照。不过原文未给出两者完全相同的推理预算或交互成本。
- Agent-FLAN-7B、LLaMA-xLAM-2-8B-fc-r和DeepResearcher-7B代表开源智能体专用模型，用于判断PilotRL相较已有智能体训练方案是否具有优势；其中DeepResearcher-7B与Qwen2.5-7B-Instruct版本的PilotRL共享同类骨干规模，比较更具针对性。
- Naive Response与ReAct分别代表不使用额外训练或提示策略的直接生成，以及把单步推理与即时动作交替进行的常见智能体范式。它们用于区分基础模型能力、局部逐步决策和显式全局规划带来的收益。
- MPO是即插即用的外部元规划器，用显式计划指导执行。它与PilotRL的比较主要检验：仅在推理时接入外部规划是否足够，还是必须通过训练让规划器与执行器紧密协调。

**实验想回答的问题**

- PilotRL是否能在不同类型的约70亿至80亿参数骨干模型上稳定提升智能体任务完成表现，并在域内与域外任务中优于直接回答、ReAct、外部规划器、监督微调、普通强化学习及代表性闭源模型？
- 性能提升究竟来自渐进式三阶段训练、AdaPlan全局规划范式，还是规划器与执行器的一体化架构；这些设计是否改善了规划、计划遵循和端到端执行之间的协调？

**实验实现**

实验覆盖Qwen2.5-7B-Instruct、LLaMA3.1-8B-Instruct和Qwen3-8B三种骨干，以检验方法对普通指令模型和具有较强推理倾向模型的适用性。PilotRL基于verl实现，采用GRPO；训练集共5725个样本，每个样本执行16次rollout，训练批大小256、rollout批大小64，共训练4个epoch，其中阶段1、2、3分别占1、2、1个epoch，学习率为1e-6。DeepSeek-V3模拟环境行为；环境观察被拼入交互序列，但由于并非训练策略生成，损失计算时会屏蔽<observation>...</observation>内的内容，避免对这些token反向传播。SFT训练4个epoch，峰值学习率2e-5，线性预热后余弦衰减，预热比例0.03、权重衰减0、批大小256。主要评测由DeepSeek-V3统一充当LLM-as-Judge，并向其提供既有工作的参考轨迹以校准任务完成与效率判断。实验使用32张96GB NVIDIA H20 GPU、BF16和AdamW；这些配置说明计算投入较大，也意味着完整复现实验需要显著硬件资源。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 渐进式阶段训练1→2→3与同时应用三个阶段奖励1&2&3 | 标准流程的域内、域外和总体平均分分别为73.68、61.39和69.58；同时施加全部奖励时降至71.64、58.52和67.27，总体相对下降3.32%。 | 该消融保持三个阶段的奖励来源，但去掉“先学遵循计划、再学生成计划、最后学协同”的课程顺序，因此主要检验渐进训练本身。下降支持作者关于异质奖励在早期可能产生冲突的解释，尤其域外下降更明显；但论文只给出结果与机制推测，没有直接报告梯度冲突或训练方差，因而原因仍属作者解释而非被独立测量的事实。 | 表2，第4.1节 Necessity of Progressive Training<br><span class="experiment-evidence">Standard Pipeline \| 1 → 2 → 3 \| 73.68 \| 61.39 \| 69.58; Necessity of Progressive Training \| 1 & 2 & 3 \| 71.64 (↓ 2.77%) \| 58.52 (↓ 4.68%) \| 67.27 (↓ 3.32%).</span> |
| 分别移除一个训练阶段，并固定总训练量为4个epoch | 移除阶段1的2→3流程总体平均分为66.66，下降4.20%；移除阶段2的1→3为66.57，下降4.33%；移除阶段3的1→2为67.81，下降2.54%，均低于完整流程69.58。 | 实验把剩余两个阶段各训练2个epoch，从而控制总epoch数，分别检验计划遵循、计划生成和联合协调阶段的不可替代性。三个阶段都有效，其中缺少阶段2的降幅最大、缺少阶段3的降幅相对较小；不过不同阶段的奖励目标和数据难度可能不同，等epoch并不保证完全相等的优化预算，因此不宜把降幅直接解释成精确的贡献比例。 | 表2，第4.2节 The Role of Each Stage<br><span class="experiment-evidence">The Role of Each Stage \| 2 → 3 \| 70.82 (↓ 3.88%) \| 58.33 (↓ 4.98%) \| 66.66 (↓ 4.20%); 1 → 3 \| 70.66 (↓ 4.10%) \| 58.39 (↓ 4.89%) \| 66.57 (↓ 4.33%); 1 → 2 \| 72.21 (↓ 2.00%) \| 59.02 (↓ 3.86%) \| 67.81 (↓ 2.54%).</span> |
| 统一规划器—执行器与相同骨干下分别训练的隔离式规划器和执行器 | 统一架构相对隔离架构总体下降幅度的反向表述为平均优势5.63%。表4中，Qwen2.5-7B-Instruct为68.53对64.36，LLaMA3.1-8B-Instruct为70.43对65.51，Qwen3-8B为69.77对67.11。 | 隔离方案使用相同骨干，并按阶段1和阶段2分别训练规划器与执行器各2个epoch，因此该实验主要隔离“两个能力是否在一个模型中共同学习”。三个骨干上的统一架构均更好，且域外差距通常较明显，支持内部共享表示与端到端协同的价值；但隔离方案没有执行PilotRL完整的阶段3联合优化，其劣势可能同时包含架构隔离与缺少联合协调训练两方面因素。 | 表4，第4.4节 Unified Architecture vs. Isolated Planner-Executor Architecture<br><span class="experiment-evidence">Qwen2.5-7B-Instruct \| Unified \| 72.93 \| 59.75 \| 68.53; Isolated \| 68.94 \| 55.18 \| 64.36. LLaMA3.1-8B-Instruct \| Unified \| 73.92 \| 63.46 \| 70.43; Isolated \| 68.68 \| 59.18 \| 65.51. Qwen3-8B \| Unified \| 74.18 \| 60.95 \| 69.77; Isolated \| 72.66 \| 56.02 \| 67.11.</span> |

**定性案例**

- 图3给出LLaMA3.1-8B-Instruct训练过程中的归一化奖励轨迹：执行器的计划遵循能力主要在阶段1显著提高，随后保持稳定并小幅增长；全局规划器在阶段2明显提升，进入阶段3初期短暂下降后继续上升；端到端奖励则持续提高。作者将阶段3初期的规划奖励下降解释为规划器适应执行器能力的过渡期。该动态与三阶段设计目标相符，但属于训练曲线层面的机制证据，且节选未报告误差区间或多随机种子重复结果。
- 更换LLM评审器的附录实验以Qwen2.5-7B-Instruct为骨干，将主实验的DeepSeek-V3替换为LLaMA3.1-70B-Instruct或GPT-4o。作者称不同评审模型因评分偏好产生分数差异，但PilotRL总体仍优于其他基线，说明方法排序对评审器选择具有一定稳健性；表12的具体数值未出现在所给节选中，因此无法量化排序稳定程度。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：reused verified category during targeted regeneration
- 全文指纹：`c5c1cc70bf20dfe751b71cc290fbf7e4af074ff725a43f4586eb93b51f986cfd`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
