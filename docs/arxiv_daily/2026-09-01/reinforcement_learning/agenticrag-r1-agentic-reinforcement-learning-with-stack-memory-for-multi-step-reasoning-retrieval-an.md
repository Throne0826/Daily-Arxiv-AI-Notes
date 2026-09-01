---
title: "[论文解读] AgenticRag-R1: Agentic Reinforcement Learning with Stack Memory for Multi-Step Reasoning, Retrieval and Memorizing"
description: "[arXiv 2608.29622][强化学习] 本文针对多步检索推理中动作控制粗糙、错误记忆不可撤销及强化学习偏爱短轨迹的问题，提出以栈式记忆、细粒度动作奖励和信息感知轨迹筛选为核心的 AgenticRag-R1。"
arxiv_id: "2608.29622"
announcement_date: "2026-09-01"
primary_category: "reinforcement_learning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:57:25.720112+00:00"
source_sha256: "a42e4ae458e44623cf39dc0f727cfbd094200f22238c3b11f02087e99a329847"
tags:
  - "强化学习"
  - "LLM Agent"
  - "LLM Reasoning"
  - "LLM 其他"
  - "检索增强生成（RAG）"
  - "大语言模型（LLM）"
  - "强化学习（RL）"
  - "多步推理"
  - "智能体式检索"
  - "记忆栈"
  - "细粒度动作"
  - "长程推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">强化学习 · arXiv 2608.29622</p>

# AgenticRag-R1: Agentic Reinforcement Learning with Stack Memory for Multi-Step Reasoning, Retrieval and Memorizing

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Xinke Jiang, Yue Fang, Zhibang Yang, Jiaran Gao, Zhixin Zhang, Tao Feng, Rihong Qiu, Wentao Zhang, Hongxin Ding, Ruizhe Zhang, Yongxin Xu, Yuheng Huang, Xu Chu, Junfeng Zhao, Yasha Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: National Engineering Research Center of Software Engineering, Peking University, Beijing, China；Affiliation: School of Computer Science, Peking University, Beijing, China；Affiliation: Key Laboratory of High Confidence Software Technologies, Ministry of Education, Beijing, China；Affiliation: GRG Banking Equipment Co., Ltd., Guangzhou, China；Affiliation: Center on Frontiers of Computing Studies, Peking University, Beijing, China；Affiliation: Peking University Information Technology Institute (Tianjin Binhai), Tianjin, China * Equal contribution；Affiliation: Peking University Information Technology Institute (Tianjin Binhai), Tianjin, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.29622v1) · [PDF 下载](https://arxiv.org/pdf/2608.29622v1) · **关键词** 检索增强生成（RAG）, 大语言模型（LLM）, 强化学习（RL）, 多步推理, 智能体式检索, 记忆栈, 细粒度动作, 长程推理<br>
**代码**: [https://github.com/jiangxinke/Harness-RL/tree/AgenticRAG-R1-Whitebox](https://github.com/jiangxinke/Harness-RL/tree/AgenticRAG-R1-Whitebox)

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

本文针对多步检索推理中动作控制粗糙、错误记忆不可撤销及强化学习偏爱短轨迹的问题，提出以栈式记忆、细粒度动作奖励和信息感知轨迹筛选为核心的 AgenticRag-R1。

**不用术语来说**：复杂问题通常不能靠一次搜索解决：模型需要先判断缺少什么信息，再多次搜索、推理和调整计划，同时保留有用结论并删除错误内容。现有系统往往只是把每次思考和检索结果不断追加到上下文；一旦某次搜索无关或中间推断错误，后续步骤就可能沿着错误继续展开。训练时若只看最终答案是否正确，模型也难以知道究竟是哪一步做得好或不好。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将代理式强化学习形式化在搜索与记忆环境中，设计包含思考、搜索、规划、总结和回退的细粒度动作空间，并用可压入、修订和弹出的栈式记忆表示持续变化的内部状态；与动作对齐的过程奖励进一步为不同中间动作提供监督。
- 作者提出跨批次的信息感知轨迹拒绝策略，综合轨迹奖励与同一输入多次展开结果的方差，过滤低信息轨迹并优先训练具有行为差异、需要较长决策链的样本，以减少强化学习对浅层固定模板的偏好。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型（LLM）与检索增强生成（RAG）的交叉领域。RAG通过在生成答案前访问外部知识，缓解LLM的事实错误、知识过时和领域知识不足；但复杂任务通常需要多跳检索、逐步推理，以及根据新证据持续修改中间结论。本文进一步将强化学习（RL）用于训练能够自主决定何时检索、如何推理以及如何管理中间记忆的智能体，重点处理长程、多步骤交互中的动作控制、奖励分配和错误累积问题。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**检索增强生成（RAG）**

RAG先从外部文档或知识库中检索与问题相关的信息，再将这些信息提供给LLM生成答案。与只依赖模型参数中的知识相比，它能够利用更新或更专业的外部证据，但检索结果可能无关、误导，因而需要在推理过程中动态判断和修正。

</div>
<div class="concept-item" markdown="1">

**多步推理与智能体式RAG**

多步推理将复杂问题拆成相互依赖的若干步骤，每一步的结论可能影响后续检索和判断。智能体式RAG允许模型在生成最终答案前循环执行推理、检索、规划和记忆操作，而不是只进行一次固定检索。

</div>
<div class="concept-item" markdown="1">

**强化学习（RL）**

RL把模型看作根据当前状态选择动作的策略，并依据任务结果或过程反馈调整策略。本文关注的是长程轨迹：一次回答包含多个连续动作，因此只在最终答案处给奖励会难以判断每个中间动作的贡献。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文研究开放域、多跳和智能体式推理环境中的长程检索增强生成。给定用户问题以及可访问的外部检索工具，模型需要交替执行推理、检索、规划和记忆管理动作，逐步形成并修订内部上下文，最终输出答案或下游任务结果。关键假设是：中间检索内容和推理结论都可能含噪，系统不能只采用不可撤销的追加式上下文，而应能够检查、总结、回退或删除已有内容；同时，训练过程需要对不同动作提供更细粒度的反馈，并优先学习信息量较高、具有长程决策价值的轨迹。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **AEPO、ARPO与MEM1**: 这些工作代表了面向多步推理和工具交互的近期RL方法：AEPO处理多轮智能体中的熵不平衡与轨迹坍缩，ARPO针对不确定的高熵工具调用进行探索和优势归因，MEM1尝试联合记忆与推理以支持长程交互。本文认为它们及其他现有方法仍主要受粗粒度动作、轨迹级标量奖励、探索不足和多步错误累积限制，因此引入更细粒度的记忆感知动作和动作级过程奖励。
- **基于提示或监督微调的推理—检索方法**: 早期方法主要依靠人工设计的提示策略，后续方法使用监督微调来协调推理与检索。它们能够在特定任务或固定推理模式下有效，但对启发式设计依赖较强，容易过拟合预设模板，尚未从根本上学习在复杂环境中联合决定检索、推理和记忆修订。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

真实的开放域与多跳任务包含相互依赖的多个步骤，模型必须随推理进展动态决定何时检索、检索什么，以及如何把外部证据纳入当前判断。检索文档可能无关或具有误导性，中间推断也可能包含逻辑错误；若这些内容持续进入内部上下文而不能检查、修订或删除，噪声会逐步传播，最终破坏后续决策与答案可靠性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **提示工程与监督微调式推理—检索协同**：这类方法通过人工编写的分步提示，或用示范轨迹进行监督微调，规定模型如何交替思考与调用检索工具。它们能在特定任务中形成可执行流程，但协调方式主要来自预设模板或训练示例，而非模型通过长期交互自行学习。
- **基于强化学习的代理式 RAG**：这类方法让模型在推理过程中选择是否调用外部检索，并依据最终答案正确性优化策略；典型设计把思考和搜索表示为少数粗粒度动作，再将生成内容追加到上下文。相较固定提示，它能够从任务反馈中学习工具使用，但通常缺少显式的记忆编辑动作和中间步骤反馈。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有代理式 RAG 常把复杂过程压缩为粗粒度的思考与搜索动作，并采用只追加、不可逆的上下文记忆。模型无法明确总结、修订或撤回已经写入的中间内容，因而无关检索和错误推断容易累积；若奖励只依据最终答案，中间动作的责任也难以分配，训练便倾向浅层、可重复的固定策略。
- 常见多跳或检索训练样本中，一次检索或短推理即可完成的低信息轨迹更容易获得即时奖励，并在训练分布中占据优势。即使提供细粒度动作，模型也可能很少练习规划、总结和回退，导致需要多次决策的长程动作组合得不到充分探索与优化。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未形成一套统一的强化学习机制，同时解决两个相互关联的问题：一是让代理能够显式管理、纠正和撤销多步推理中的内部记忆，并把奖励准确归因到异质的中间动作；二是从大量容易但信息量低的展开轨迹中识别更有训练价值的长程轨迹，使复杂动作真正获得足够训练。

</div>
<div markdown="1"><span>核心问题</span>

如何构建一个将推理、外部检索与可逆记忆管理深度结合的代理式强化学习框架，使模型既能获得动作级过程反馈，又能优先学习高信息、多样且具有长程结构的轨迹，从而提升复杂多步任务中的稳健决策能力？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把上下文从只能不断追加的“笔记本”改造成可操作的“栈”：模型可以保存当前有用结论，也能总结、修订或弹出已经证明错误的内容，从结构上阻断噪声继续传播。随后，过程奖励告诉模型每类动作是否有效，而信息感知筛选把训练资源集中到结果差异较大、确实需要多步探索的样本上；两者分别改善“每一步如何学”和“优先从哪些经历中学”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

AgenticRag-R1是一个面向多步推理、检索与记忆协同的强化学习框架。给定问题$q$，策略模型$[?25l\pi_\theta$以多轮方式生成由结构化动作组成的轨迹：用$\langle\mathrm{Plan}\rangle$分解目标，用$\langle\mathrm{Think}\rangle$进行推理，用$\langle\mathrm{Search}\rangle$调用检索器，并通过$\langle\mathrm{Backtrack}\rangle$和$\langle\mathrm{Summary}\rangle$操作后进先出记忆栈，从而支持回溯与上下文压缩，最后由$\langle\mathrm{Conclusion}\rangle$产生答案。训练时，框架将最终答案质量与具体动作质量分开建模，并采用信息增益感知的动态轨迹筛选，以改善长轨迹探索和奖励分配。直观地说，该方法不是让模型固定地“先检索再回答”，而是让模型像一个可修改草稿的研究助手：先规划，必要时查资料，发现冲突时撤销最近步骤，信息过长时压缩记忆，确认后再作答。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 问题与记忆状态初始化

初始化空轨迹$y\leftarrow\emptyset$与空记忆栈$\mathcal{M}\leftarrow\emptyset$，随后在每一轮以$q$、当前轨迹$y$和栈状态$\mathcal{M}$作为策略条件。

<div class="method-step__io" markdown="1">

**输入**：用户问题$q$、策略$\pi_\theta$、检索器$\mathcal{R}$和最大动作预算$T$。<br>
**输出**：可供策略生成的初始环境状态。

</div>

**直观理解**：这一步相当于给模型一张空白工作台：问题是任务，轨迹是已经写下的内容，记忆栈保存当前仍然有效的推理单元。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多动作轨迹生成

模型逐token采样，直到生成动作分隔符；系统将该片段解析为$\mathrm{Plan}$、$\mathrm{Think}$、$\mathrm{Search}$、$\mathrm{Backtrack}$、$\mathrm{Summary}$或$\mathrm{Conclusion}$之一，并循环生成后续动作，直至结束或达到$T$。

<div class="method-step__io" markdown="1">

**输入**：当前问题$q$、轨迹$y$、记忆栈$\mathcal{M}$以及策略模型$\pi_\theta$。<br>
**输出**：包含推理文本、动作调用和可能的检索结果的完整轨迹$y$。

</div>

**直观理解**：模型每次不是只输出一长段不可分的文字，而是完成一个有明确用途的“操作”。这使训练系统能够知道模型是在规划、思考、搜索，还是在纠错和压缩记忆。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 检索与栈式记忆更新

$\mathrm{Plan}$、$\mathrm{Think}$、$\mathrm{Search}$和$\mathrm{Conclusion}$将相应推理单元压入栈；$\mathrm{Search}$还依据结构化查询调用$\mathcal{R}$并将外部观察加入后续上下文；$\mathrm{Backtrack}$弹出错误或不一致的顶部元素后继续探索，$\mathrm{Summary}$弹出近期内容并压入压缩表示。

<div class="method-step__io" markdown="1">

**输入**：解析后的动作$a_t$、动作片段$x_t$、当前记忆栈$\mathcal{M}$以及检索器$\mathcal{R}$。<br>
**输出**：更新后的记忆栈$\mathcal{M}$、检索观察和持续扩展的轨迹$y$。

</div>

**直观理解**：记忆栈像一叠可撤销的便签：新想法放在顶部，错误时撕掉最近几张，内容太多时把几张便签整理成一张摘要。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分层奖励与强化学习更新

计算最终结果奖励$r_{\mathrm{out}}^{(k)}$和动作级过程奖励$r_{\mathrm{proc},i}^{(k)}$，按token构造奖励；随后使用信息增益感知的动态rollout选择保留更有学习价值的轨迹，并以GRPO更新策略参数$\theta$。

<div class="method-step__io" markdown="1">

**输入**：生成轨迹$y^{(k)}$、最终答案、动作标记、掩码信息以及轨迹筛选所需的信息增益。<br>
**输出**：筛选后的训练样本、token级奖励和更新后的策略$\pi_\theta$。

</div>

**直观理解**：最终答案决定“整次尝试是否成功”，具体动作奖励则指出哪些决定做得好。动态筛选会减少低信息量或重复的尝试，使训练资源更多用于真正能教会模型新行为的长轨迹。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 分层token级奖励

$$
r^{(k)}_{i}=\bigl(1-\mathbb{I}^{(k)}_{\mathrm{mask},i}\bigr)\,r^{(k)}_{\mathrm{out}}+\mathbb{I}^{(k)}_{\mathrm{act},i}\,r^{(k)}_{\mathrm{proc},i},\quad i\in[1,|y^{(k)}|]
$$

**符号说明**

- $r^{(k)}_{i}$：第$k$条轨迹中第$i$个token获得的总奖励。
- $y^{(k)}=(x^{(k)}_1,\ldots,x^{(k)}_{|y^{(k)}|})$：第$k$条rollout生成的token序列；$x^{(k)}_i$是其中第$i$个token。
- $r^{(k)}_{\mathrm{out}}$：第$k$条轨迹的结果奖励，用于评价最终答案质量。
- $r^{(k)}_{\mathrm{proc},i}$：与第$i$个token所属动作对应的过程奖励。
- $\mathbb{I}^{(k)}_{\mathrm{mask},i}$：掩码指示变量；为真时表示该token不参与策略优化，例如检索得到的观察。
- $\mathbb{I}^{(k)}_{\mathrm{act},i}$：动作指示变量；为真时表示该token对应某个动作调用。
- $|y^{(k)}|$：第$k$条轨迹的token数量。

<div class="equation-explanation" markdown="1">

**直观理解**：对于未被掩码的生成token，系统提供共享的最终结果奖励；对于动作token，再额外提供相应的过程奖励。这样既保留整条轨迹对最终答案负责的信号，又把更细的监督集中到真正影响环境交互的动作上。<br>
**原文位置**：第2.1节，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 策略采样条件

$$
x\sim\pi_{\theta}(\cdot\mid q,y,\mathcal{M})
$$

**符号说明**

- $x$：当前采样的token。
- $\pi_{\theta}$：参数为$\theta$的策略模型。
- $q$：输入问题。
- $y$：截至当前时刻已经生成的轨迹。
- $\mathcal{M}$：当前的LIFO记忆栈。

<div class="equation-explanation" markdown="1">

**直观理解**：每个新token都由策略根据问题、已有轨迹和可逆记忆状态共同生成，而不是只依赖连续文本上下文。因此模型的下一步决定会显式受到已保存、已压缩或已回退状态的影响。<br>
**原文位置**：附录B，Algorithm 1第7行

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练采用基于GRPO的强化学习框架。对每个问题生成多条随机rollout，使用分层token级奖励评价最终结果和具体动作，再结合信息增益感知的动态轨迹选择进行策略优化；所给章节未提供完整的GRPO裁剪目标公式，因此不补写未出现的目标函数。结果奖励负责长期任务成败，过程奖励负责动作决策的局部信用分配，token掩码则阻止检索观察等非策略生成内容产生虚假梯度。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 记忆感知多动作模型**

框架将轨迹划分为六类语义动作：$\mathrm{Plan}$、$\mathrm{Think}$、$\mathrm{Search}$、$\mathrm{Backtrack}$、$\mathrm{Summary}$和$\mathrm{Conclusion}$。其中前者以及搜索和结论主要执行push；$\mathrm{Backtrack}$执行pop后push，$\mathrm{Summary}$执行pop并将摘要重新push入栈。每个栈元素对应一个离散的推理单元，因此轨迹可分解、可回滚且具有可解释的内部状态。

> 直观理解：普通生成通常把所有推理混在一段文本里，模型很难明确撤销某一步。这里把推理变成可操作的便签单元，因此能够定位错误并恢复到较早的状态。

**2. 分层动作感知奖励**

奖励由结果奖励和过程奖励组成。结果奖励评价$\langle\mathrm{Conclusion}\rangle$中抽取的最终答案，并共享到未被掩码的有效生成token；过程奖励只赋予与相应动作调用对应的token，从而避免把同一个粗粒度回报平均、无差别地施加到整条轨迹。检索到的观察等被掩码内容不参与策略优化，以避免由非策略生成内容产生错误梯度。

> 直观理解：该模块同时回答两个问题：“答案对不对”和“模型刚才采取的这个动作是否合理”。这样模型不仅学会结果导向，也能逐渐学会何时搜索、何时回退和何时总结。

**3. 信息增益感知动态rollout选择**

训练过程中生成多条随机轨迹，并依据轨迹带来的信息增益进行动态选择，以支持长时域探索和提高数据效率。该策略与动作级奖励配合，试图降低短视、重复或模板化轨迹对强化学习训练的影响。

> 直观理解：如果每次都保留几乎相同的尝试，训练不会获得新经验。该模块优先保留能带来新信息的轨迹，让模型更有机会学会较长的推理路径。

**训练与推理**

训练时，输入问题$q$后初始化轨迹和LIFO记忆栈；策略模型逐token生成动作片段，系统解析动作并执行对应的栈操作或检索调用，将结果继续反馈给模型，直到生成结论、达到动作预算或轨迹终止。对每条轨迹计算最终答案奖励和动作级过程奖励，筛选信息增益较高的rollout后，用GRPO更新$\pi_\theta$。推理时沿用同一交互流程，但不进行参数更新：模型根据当前问题、轨迹、记忆栈和检索观察反复选择规划、思考、搜索、回退或总结，最终由$\mathrm{Conclusion}$产生候选答案。

**复现信息**

论文给出的可复现实验设置包括：GRPO批大小为16，学习率为$1\times10^{-6}$，训练1个GRPO epoch、300个优化步；每个问题采样4条随机生成（附录文字另给出表7的Number of Generations为10，二者存在原文不一致，需核查）；采样温度为0.7，启用多样性采样，diversity penalty为1.0。每条生成最多2048个新token，最大上下文长度为4096，单个episode最多10次迭代生成；GRPO参数为$\beta=0.04$、$\mu=2$、$\epsilon=0.1$。实验未使用量化或KV缓存，并在单一整理数据集上固定超参数。上述设置主要影响训练成本、探索范围和结果可比性；其中采样数量冲突不应在复现实验时自行忽略。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 训练集由HotpotQA与2WikiMultiHopQA训练划分筛选而成。作者让无需训练的TC-RAG对每道候选题独立生成10条轨迹，删除十次均答错、正确率不低于50%，或至多一次检索即可答对的问题，以保留“可解但必须多步搜索”的样本。原文未明确报告筛选后的训练集规模；这一构造主要用于避免强化学习只学到短程模板。
- 域内及多跳评测包括2Wiki、HotpotQA，并以MuSiQue和Bamboogle检验分布变化后的组合推理。完整数据规模分别为：2Wiki含154,878/12,576/12,576个训练、开发、测试样本；HotpotQA含90,564/7,405/14,810个样本；MuSiQue含19,938/2,417/2,459个样本，Bamboogle仅含125个测试问题。前两者与训练来源重合，后两者更能观察迁移能力。
- 开放域与智能体评测覆盖Natural Questions、TriviaQA和FRAMES：NQ含307,373/7,830/7,842个训练、开发、测试样本，TriviaQA含138,384/17,944/17,210个样本，FRAMES含824个测试问题。这组数据分别考察真实查询、词汇与句法变化较大的知识问答，以及需要整合多来源信息的真实智能体式任务。正文称评测十个基准，附录D则称九个且实际列出七个名称，具体评测清单需结合完整表格复核。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**F1-Score**

衡量模型预测答案与标准答案之间的词项重合，同时综合精确率与召回率；论文也以七个基准的平均F1汇总总体表现。 （越高越好，因为更高的F1表示答案与参考答案具有更完整且更准确的重合；但它不直接衡量检索证据是否正确、推理链是否忠实。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen2.5-3B上的域内2Wiki与HotpotQA

<div class="result-value" markdown="1">

相对各数据集最强基线，AgenticRag-R1在2Wiki和HotpotQA上的绝对提升分别为3.02和6.76个百分点。

</div>

作者据此主张，细粒度动作、记忆栈和强化学习优化在与训练来源相近的多跳任务上优于强基线。HotpotQA上的提升较大，但这两个数据集也参与训练数据构造，因此该结果主要证明域内有效性，不能单独证明跨分布泛化；节选亦未提供置信区间，无法判断提升的统计稳定性。

<div class="result-source" markdown="1">

来源：第3节实验结果，Table 1相关分析，Strong Performance Compared with Baselines

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the in-domain datasets, AgenticRag-R1 consistently surpasses the strongest baselines, with, for example, absolute gains of +3.02% on 2Wiki and +6.76% on HotpotQA using the 3B backbone.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen2.5-1.5B的TriviaQA与Qwen2.5-7B的Bamboogle域外评测

<div class="result-value" markdown="1">

相对最强Agentic RAG基线，1.5B主干在TriviaQA上约提升7.2个百分点，7B主干在Bamboogle上约提升7.1个百分点。

</div>

这两个结果表明收益并不限于单一参数规模，也能迁移到开放域问答和手工组合问题。由于两个数字来自不同模型规模和不同数据集，不能据此推断模型规模与收益之间的单调关系；Bamboogle仅有125题，单次评测也可能对少数题目的变化较敏感。

<div class="result-source" markdown="1">

来源：第3节实验结果，Table 1相关分析，Strong Performance Compared with Baselines

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On out-of-domain benchmarks, AgenticRag-R1 exhibits strong generalization, e.g., achieving an absolute improvement of about +7.2% on TriviaQA with the 1.5B backbone and +7.1% on Bamboogle with the 7B backbone over the strongest Agentic RAG baselines.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨1.5B、3B和7B主干及域内、域外多跳问答的总体比较

<div class="result-value" markdown="1">

作者报告AgenticRag-R1在不同主干规模上均取得最好或接近最好的表现，并将跨规模持续收益解释为强化学习方案具有有效性和稳健性。

</div>

这一总体趋势比单个最佳分数更重要：方法并非只对某个主干偶然有效。不过，“最好或接近最好”允许个别设置未获第一，且节选缺少Table 1完整分数、运行方差和显著性检验，因此只能确认作者报告的覆盖面，不能量化所有设置中的优势幅度或排除随机波动。

<div class="result-source" markdown="1">

来源：第3节实验结果，Table 1相关分析，Strong Performance Compared with Baselines

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across in-domain and out-of-domain multi-hop QA benchmarks (Table 1), AgenticRag-R1 achieves the best or near-best performance across backbone model sizes.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 节选未提供Table 1完整结果、每个基准的具体评测划分、随机种子、重复运行次数、标准差、置信区间或显著性检验；因此可以比较作者报告的点估计，但无法判断较小差距是否稳定。正文称十个评测基准，附录D称九个且实际列出七个名称，也需要对照完整论文核验。
- 训练数据直接来自HotpotQA和2Wiki的筛选样本，域内提升可能同时受数据来源重合影响；过程奖励又依赖通用LLM裁判，可能引入裁判偏好、额外计算成本和复现差异。长程实验虽把步数上限扩展至30，但所给节选没有报告相应分数或成本曲线，因此尚不足以确认更大预算必然改善长程推理。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- No-RAG与CoT代表不访问外部知识的参数化知识和纯内部推理能力；与它们比较可判断性能提升是否确实来自检索，而非仅来自更长的思维链。
- FS-RAG与FL-RAG代表固定规则的朴素RAG，分别按句子或固定token间隔触发检索；它们用于检验自适应决定“何时搜、搜什么”是否优于机械增加外部上下文。
- ReAct、IRCOT与TC-RAG代表提示驱动的Agentic RAG，其中TC-RAG同样使用支持push/pop的记忆栈；这一组能够区分强化学习优化的收益与手工提示、已有栈式控制结构本身的收益。
- ReSearch、Search-R1、AEPO、ARPO与Mem1代表强化学习智能体基线，分别涵盖联合推理搜索、GRPO工具调用、熵平衡或自适应采样，以及恒定记忆约束下的长期任务；它们是判断细粒度动作、过程奖励和轨迹拒绝是否优于已有RL训练策略的关键比较对象。

**实验想回答的问题**

- RQ1：在相同主干规模下，AgenticRag-R1能否在域内多跳问答及域外开放域、组合式和智能体问答上稳定优于无检索、固定检索、提示式智能体RAG与强化学习智能体RAG基线？
- RQ2：记忆动作、信息感知轨迹拒绝、检索过程奖励与记忆过程奖励分别贡献了什么，它们能否协同支持更长程且更有效的推理？

**实验实现**

实验使用Qwen2.5的1.5B、3B和7B等不同规模主干，在同一套经难度筛选的多跳数据上训练方法及基线，并在域内与域外基准上评测。ReSearch以PPO实现，Search-R1以GRPO训练；AgenticRag-R1的检索奖励$r_{\mathrm{rag}}$和记忆奖励$r_{\mathrm{mem}}$由通用LLM裁判依据固定提示进行语义评分，无须额外训练奖励模型。组件实验以Qwen2.5-3B为主，分别移除记忆动作、轨迹拒绝和两类过程奖励；阈值实验改变轨迹拒绝门槛并同时观察F1和拒绝样本数；长程实验把最大步数预算从10依次提高到15、20、25和30。原文节选未给出检索器、解码参数、重复运行次数、方差或显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Qwen2.5-3B：移除记忆动作或信息感知轨迹拒绝 | 完整模型在2Wiki和HotpotQA上的F1分别为32.92%和44.00%；移除记忆动作后降至27.54%和28.77%。移除轨迹拒绝使七基准平均F1从33.55%降至25.43%，同时移除两项则进一步降至24.24%。 | 该实验隔离了“模型能否主动管理记忆”与“训练时是否过滤低信息轨迹”两项设计。记忆动作对HotpotQA的影响尤其大，而联合移除比单独移除轨迹拒绝更差，支持二者互补的作者结论。不过这不是完全独立的因果分解：移除动作会同时改变可生成轨迹的空间和长度分布，下降不一定只来自记忆内容质量。 | Table 2；第3.3节，Model Component Ablation<br><span class="experiment-evidence">Removing memory-related actions (w/o MemAction) substantially degrades performance, e.g., 2Wiki drops from 32.92% to 27.54% and HotpotQA from 44.00% to 28.77%. Removing information-aware rejection (w/o Reject) also reduces the average score from 33.55% to 25.43%, while removing both components further lowers it to 24.24%, confirming their complementary contributions.</span> |
| Qwen2.5-3B：移除检索奖励$r_{\mathrm{rag}}$、记忆奖励$r_{\mathrm{mem}}$或同时移除二者 | 去除$r_{\mathrm{rag}}$后，2Wiki由32.92%降至23.70%，HotpotQA由44.00%降至34.71%；去除$r_{\mathrm{mem}}$后，MuSiQue由16.48%降至7.63%；同时去除两类过程奖励时，七基准平均F1仅19.94%。附录H还报告，把LLM语义裁判替换为ROUGE-L和合法记忆操作奖励后，平均F1由33.55降至29.40。 | 这一消融检验过程级监督是否提供了超出最终答案奖励的信息。$r_{\mathrm{rag}}$直接鼓励检索结果与当前需求相关，$r_{\mathrm{mem}}$鼓励有效压缩、保存或回退上下文；二者同时移除造成最大下降，说明搜索质量和记忆管理都需要显式训练信号。启发式替代也更差，支持“语义判断比表面重合或动作合法性更有用”，但由于裁判是通用LLM，实验尚不能排除裁判偏差或额外推理成本的影响。 | Table 2；第3.3节，Process-level Reward Ablation；Appendix H，Semantic Reward Analysis<br><span class="experiment-evidence">Removing the RAG reward (w/o $r_rag)$ hurts 2Wiki (32.92% to 23.70%) and HotpotQA (44.00% to 34.71%), while removing the memory reward (w/o $r_mem)$ weakens out-of-domain performance, e.g., MusiQue drops from 16.48% to 7.63%. Removing both rewards yields the largest drop (Avg 19.94%), showing that both signals are necessary for effective reasoning and memory utilization. The average F1 score across seven benchmarks decreases from 33.55 to 29.40, and further drops to 19.94 when both $r_rag$ and $r_mem$ are removed, demonstrating the importance of semantic process supervision.</span> |

**定性案例**

- 动作频率分析显示，Qwen2.5-3B训练期间$\langle think\rangle$持续增加，$\langle summary\rangle$与$\langle backtrack\rangle$虽有波动但总体增加，$\langle search\rangle$大致稳定，$\langle conclusion\rangle$持续增加；1.5B模型则减少搜索但仍增加结论动作。作者将其解释为模型逐步学会依靠内部推理、摘要和回退控制记忆，并减少无法输出最终答案的轨迹。更谨慎地说，这只是动作使用模式的可解释性证据，未逐例验证摘要是否保留关键事实、回退是否真正纠错，因而不能证明每条推理链都忠实可靠。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Its main contribution is an RL framework for training an agent to perform adaptive retrieval, memory operations, and multi-step LLM reasoning over long horizons.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`a42e4ae458e44623cf39dc0f727cfbd094200f22238c3b11f02087e99a329847`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
