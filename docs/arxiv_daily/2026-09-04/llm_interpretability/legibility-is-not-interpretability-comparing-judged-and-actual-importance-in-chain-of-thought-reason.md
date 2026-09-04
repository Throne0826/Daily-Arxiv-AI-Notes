---
title: "[论文解读] Legibility is Not Interpretability: Comparing Judged and Actual Importance in Chain-Of-Thought Reasoning"
description: "[arXiv 2609.04194][LLM 机制与可解释性] 本文质疑“推理文本清晰可读就意味着其作用可解释”这一默认前提，并研究能否先用步骤优势度量思维链步骤对最终答案的实际影响，再从步骤文本中识别这种影响。"
arxiv_id: "2609.04194"
announcement_date: "2026-09-04"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:36:10.770486+00:00"
source_sha256: "428e820532d22fd7ce5bc77fc6bbdc2d37a89b6e47bd8d07e5845eb958aa12c8"
tags:
  - "LLM 机制与可解释性"
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "链式思维推理"
  - "推理步骤重要性"
  - "优势（advantage）"
  - "过程奖励模型"
  - "可解释性与忠实性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2609.04194</p>

# Legibility is Not Interpretability: Comparing Judged and Actual Importance in Chain-Of-Thought Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Kevin Du, Alexander Hoyle, Laura Ruis, Acyr Locatelli</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: ETH Zürich；Affiliation: MIT</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.04194v1) · [PDF 下载](https://arxiv.org/pdf/2609.04194v1) · **关键词** 链式思维推理, 推理步骤重要性, 优势（advantage）, 过程奖励模型, 可解释性与忠实性<br>
**代码**: [https://github.com/kdu4108/importance-advantage](https://github.com/kdu4108/importance-advantage)

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

本文质疑“推理文本清晰可读就意味着其作用可解释”这一默认前提，并研究能否先用步骤优势度量思维链步骤对最终答案的实际影响，再从步骤文本中识别这种影响。

**不用术语来说**：一段推理中，两句措辞相似的“让我重新检查”可能发挥完全不同的作用：一句对答案毫无影响，另一句却纠正关键错误并显著提高答对概率。仅凭文字，人或语言模型评审未必能分辨这种差异，因此需要把步骤“看起来重要”与“实际上改变模型后续结果”区分开来。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出以强化学习意义下的“优势”操作化定义步骤重要性，即考察加入某一步后，最终答案预期奖励发生了多大变化；并进一步采用基于变点的判定方法，识别具有足够强或持久影响的步骤。
- 作者系统检验步骤重要性是否能从思维链文本中解码：零样本大模型评审虽可优于按类别占比预测的基线，却远低于噪声上限；微调后的步骤级批评器主要改善错误回答上的识别，在正确回答上仍只能恢复少量可解码信号。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于链式思维（Chain-of-Thought，CoT）推理与语言模型可解释性研究的交叉领域。CoT 是模型为得到最终答案而生成的一串文本推理步骤；研究者常用大语言模型评审器、过程奖励模型和生成式批评器判断这些步骤是否正确、是否忠实，或为其提供逐步监督。本文关注其中一个更基础的问题：一个推理步骤的文本是否真的包含足够信息，使外部评审器能够判断该步骤对模型最终答案的实际作用。为此，论文不把“看起来合理”作为重要性的依据，而把步骤重要性与强化学习中的优势联系起来，用该步骤对后续获得奖励的期望影响来度量其功能价值。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**链式思维（CoT）**

CoT 是模型在最终答案之前生成的多步自然语言推理轨迹。本文把轨迹拆成单独步骤，并研究每一步是否改变模型继续生成正确答案的概率。

</div>
<div class="concept-item" markdown="1">

**蒙特卡洛滚动（Monte Carlo rollout）**

从某个推理前缀继续多次采样后续内容，并统计最终获得目标奖励的频率，以近似该前缀的期望结果。直观地说，它通过大量“从这里重新开始”的试验估计模型在该步骤之后还有多大机会成功。

</div>
<div class="concept-item" markdown="1">

**优势（advantage）**

本文将某一步的优势定义为加入该步骤后，模型获得奖励的期望变化；奖励可以是最终答案正确。它衡量的是该步骤为当前模型策略增加了多少预测价值，而不是该步骤在逻辑结构上是否不可缺少。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定语言模型针对一道题生成的 CoT 轨迹，将其划分为连续推理步骤。对每个步骤，从包含该步骤的前缀继续进行多次蒙特卡洛采样，估计模型最终匹配原始最终答案或获得正确答案的概率，并据此计算该步骤的优势；随后把高优势步骤视为有信息价值的步骤，把低优势步骤视为不具信息性的步骤。论文进一步考察：仅根据步骤文本，零样本或经过微调的 LLM 评审器能否识别这些高优势步骤。该设定区分了“文本上容易读懂”与“实际上改变模型行为”两种性质；它也不同于反事实必要性，因为某个步骤即使在结构上不可缺少，只要模型从该处继续生成时成功概率没有相对基线提升，其优势仍可为零。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$s$**

一条 CoT 轨迹中的单个推理步骤。

</div>
<div class="notation-item" markdown="1">

**$A(s)$**

步骤 $s$ 的优势，即包含该步骤相对于相应基线对期望奖励的提升。

</div>
<div class="notation-item" markdown="1">

**$R$**

滚动后的结果奖励；在本文主要语境中，可表示最终答案是否正确，或是否匹配原始最终答案。

</div>
<div class="notation-item" markdown="1">

**$\pi$**

语言模型用于继续生成推理轨迹的策略，即在给定前缀后生成后续文本的概率分布。

</div>

</div>

**直接相关的工作**

- **Wei et al. (2022) 等关于 CoT 与测试时计算的工作**: 这些工作表明，通过生成多步推理轨迹可以提升模型能力，为“哪些步骤真正带来性能收益”这一重要性问题提供了研究背景。本文不再只观察最终性能，而是用优势刻画轨迹内部步骤对结果的实际影响。
- **Gandhi et al. (2025) 等关于 LLM 评审器、过程奖励模型与推理步骤评估的工作**: 这类方法把推理文本当作可以逐步检查和监督的对象，隐含假设步骤文本能够反映其功能作用。本文以蒙特卡洛估计得到的优势作为参照，检验评审器能否从文本中恢复步骤重要性，并指出这种可恢复性并不充分。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大模型评审器、生成式批评器和过程奖励模型正在被用于诊断推理错误、评价忠实性以及提供步骤级训练监督。这些用途隐含假设：一个推理步骤的文本能够反映它在生成最终答案时所起的功能。如果该假设不成立，系统就可能奖励措辞合理但不起作用的步骤，或漏掉文字普通却真正改变答案的步骤，从而削弱过程监督与推理解释的可信度。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于思维链文本的大模型评审与步骤级批评**：将推理轨迹或单个步骤交给大模型评审器，根据语义上的正确性、合理性或疑似错误位置作出判断；过程奖励模型和生成式批评器再把这类判断用作步骤级评价或训练信号。
- **基于输入或推理轨迹扰动的忠实性测试**：修改提示、删改信息或构造干预条件，观察模型答案是否随之改变，以判断显式推理文本与模型行为之间是否存在因果关联。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 文本评审容易把“语义上显得关键”误当成“实际上影响答案”。论文中的两个自检步骤在措辞和功能表象上相近，但前者未改变得到正确答案的概率，后者却将该概率从约 $52\%$ 提高到约 $94\%$；这说明可读性本身不足以揭示步骤的真实作用。
- 扰动式忠实性测试依赖对提示或轨迹的人为修改，因而只能观察有限、甚至不自然条件下的行为；它不能直接提供原始生成过程中每一步对后续答案概率的贡献，也不回答这种贡献是否可由文本本身识别。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有工作广泛使用推理文本实施步骤级判断，却缺少一个以模型实际后续行为为依据、可操作地衡量单步重要性的标准，也缺少对“该行为重要性究竟有多少编码在步骤文字中”的系统检验。尤其需要区分正确回答与错误回答，因为正确轨迹中的关键步骤更难由明显错误线索定位，却是解释模型为何成功的核心对象。

</div>
<div markdown="1"><span>核心问题</span>

论文回答两个相互衔接的问题：应如何定义并估计思维链中某一步对最终答案的重要性；在获得这种行为层面的重要性标签后，零样本或微调的大模型评审器能否仅凭推理文本识别高优势步骤，并接近由估计噪声决定的可达到上限？

</div>
<div markdown="1"><span>作者直觉</span>

作者不先询问某句话“听起来是否合理”，而是从该步骤之前与之后分别继续采样模型的后续推理，比较最终获得奖励的概率。若加入该步骤后成功概率稳定上升，它就在行为上真正推动了答案；若概率不变，再醒目的措辞也不应被视为关键。由蒙特卡洛续写得到的优势标签因此可充当独立于文字表象的参照，再用它检验评审器究竟读出了功能信息，还是只识别了诸如自检、纠错等表面语义模式。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文把一条链式思维（CoT）视为语言模型策略 $\pi$ 在字符串状态上的序列决策过程。给定提示 $x$ 和按双换行切分的步骤 $a_1,\dots,a_T$，第 $t$ 步之前的状态为 $s_t=x\circ a_1\circ\cdots\circ a_{t-1}$。方法不依据步骤看起来是否正确、是否包含“反思”等语言特征来定义重要性，而是比较两种情况下获得目标奖励的概率：从 $s_t$ 直接重新生成后续内容，以及固定原步骤 $a_t$ 后从 $s_t\circ a_t$ 继续生成。两者之差即步骤优势 $A^\pi(s_t,a_t)$，表示该步骤对最终结果概率造成的实际增减。

由于模型的真实价值函数不可直接读取，作者使用原生成模型执行蒙特卡洛续写，以样本奖励均值估计步骤前后的价值，再通过变点检测和后验效应量检验产生“关键/无信息”标签。随后，论文让现成的 LLM 评判器仅根据文本预测步骤优势，也在相同骨干上训练带回归头的 critic，并将预测与蒙特卡洛标签比较。直观地说，这套方法先通过多次“从这里重新作答”测量一句推理是否真正改变答案走向，再检查只读推理文本的评判模型能否识别这种因果意义上的变化。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造逐步推理状态

将完整输出按双换行切分为连续步骤 $a_1,\dots,a_T$，并对每个位置构造前缀状态 $s_t=x\circ a_1\circ\cdots\circ a_{t-1}$。奖励 $r$ 可定义为最终答案正确，或最终答案与原轨迹答案一致。

<div class="method-step__io" markdown="1">

**输入**：数学题或其他任务提示 $x$，以及生成模型 $\pi$ 输出的完整推理轨迹与最终答案。<br>
**输出**：一组待分析的状态—步骤对 $(s_t,a_t)$，以及与分析目标对应的二元奖励函数 $r:\Sigma^*\to{0,1}$。

</div>

**直观理解**：把一篇完整解题过程切成若干段，并在每一段前设置一个“存档点”。之后分别从存档点直接重做和保留当前段后再做，以判断当前段是否真正改变结果。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 用蒙特卡洛续写估计步骤优势

从 $\pi(\cdot\mid s_t)$ 采样续写来估计 $V^\pi(s_t)$，并从 $\pi(\cdot\mid s_t\circ a_t)$ 采样续写来估计 $Q^\pi(s_t,a_t)$；二者相减得到 $\hat A(s_t,a_t)$。主要分析采用自优势，即奖励为续写答案是否匹配原轨迹最终答案；需要研究正确性时则改用答案是否正确。

<div class="method-step__io" markdown="1">

**输入**：每个 $(s_t,a_t)$、原生成模型 $\pi$、奖励函数 $r$，以及每个前缀的续写样本数。<br>
**输出**：每条轨迹随步骤变化的价值序列，以及每个步骤的有方向优势估计 $\hat A(s_t,a_t)$。

</div>

**直观理解**：如果保留某一步后，多次续写更容易得到目标答案，该步就是正向推动；若更不容易，则是负向推动。使用原模型续写可避免把另一个模型的行为误当作被研究模型自身的推理动态。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 从含噪价值轨迹识别关键步骤

将价值轨迹近似为分段常数序列，用采用精确二项代价的 PELT 算法检测变点；其惩罚项在模拟的平坦零假设序列上校准到每条序列 $2%$ 的假阳性率。对候选变点前后的分段均值建立 Beta 后验，仅当 $P(|A^\pi(s_t,a_t)|>\delta)\geq0.95$ 时把该步标为关键，否则标为无信息。

<div class="method-step__io" markdown="1">

**输入**：逐前缀价值估计、二项奖励样本、效应阈值 $\delta=0.1$ 和整条响应的时间顺序。<br>
**输出**：步骤级关键性标签，以及“至少含一个关键步骤”或“所有步骤均无信息”的响应级标签。

</div>

**直观理解**：单次续写存在随机波动，因此不能把每个小起伏都当成重要变化。该模块先寻找持续的台阶式跳变，再要求跳变大于实际意义阈值且后验把握足够高，从而减少长推理链中的大量误报。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 训练或调用文本评判器并评估可恢复性

现成评判器在单次调用中输出区间 $[-1,1]$ 内的步骤优势评分；微调 critic 则在同类骨干与提示模板上增加回归头，用五个数学数据集的 $80%$ 数据预测价值，再由相邻状态价值推导优势。模型在同分布留出集和以 AMC 23 为代表的分布外集合上排序步骤，并与关键步骤标签比较。

<div class="method-step__io" markdown="1">

**输入**：步骤文本及其上下文、蒙特卡洛产生的价值或关键性标签，以及 Qwen3 系列评判器或 critic 骨干。<br>
**输出**：每步预测优势或重要性排序，以及按最终回答正确与否分层的 PR-AUC、precision@$k%$ 和相对于噪声上限的表现。

</div>

**直观理解**：前三步用大量重采样建立行为层面的参照答案，这一步再测试“只看文字”能否猜中。若文本评判器远低于由重复采样决定的噪声上限，就说明推理文字虽然易读，却没有完整暴露该步骤对模型行为的真实作用。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 策略价值、动作价值与步骤优势

$$
V^{\pi}(s)\triangleq\mathbb{E}_{\pi}[r\mid s],\qquad Q^{\pi}(s,a)\triangleq\mathbb{E}_{\pi}[r\mid s,a],\qquad A^{\pi}(s,a)\triangleq Q^{\pi}(s,a)-V^{\pi}(s)
$$

**符号说明**

- $\pi$：被分析的语言模型策略，即给定字符串前缀后的续写分布。
- $s$：某一步之前的状态，由提示和此前所有推理步骤拼接而成。
- $a$：在状态之后已经观察到并准备评估的具体推理步骤。
- $r$：在完整续写上计算的二元奖励；可表示答案正确，也可表示答案匹配原轨迹答案。
- $V^{\pi}(s)$：不固定当前步骤、直接从状态继续生成时的期望奖励。
- $Q^{\pi}(s,a)$：固定当前步骤后再继续生成时的期望奖励。
- $A^{\pi}(s,a)$：该步骤相对于模型从同一状态平均续写所造成的期望奖励变化。

<div class="equation-explanation" markdown="1">

**直观理解**：该式用“加入步骤前后目标答案概率之差”定义重要性。正值表示步骤提高目标结果的概率，负值表示步骤损害该概率，接近零则表示该步骤虽然可读，但对最终走向基本没有可测影响。<br>
**原文位置**：第 3 节，公式（2）；其中价值函数与 Q 值定义位于公式（2）之前

</div>

</div>

<div class="equation-block" markdown="1">

#### 优势的蒙特卡洛估计

$$
\hat V(s_t)=\frac{1}{N}\sum_{i=1}^{N}r(s_t\circ c_i),\quad c_i\sim\pi(\cdot\mid s_t);\qquad \hat Q(s_t,a_t)=\frac{1}{M}\sum_{j=1}^{M}r(s_t\circ a_t\circ c'_j),\quad c'_j\sim\pi(\cdot\mid s_t\circ a_t);\qquad \hat A(s_t,a_t)=\hat Q(s_t,a_t)-\hat V(s_t)
$$

**符号说明**

- $s_t$：第 t 个步骤出现前的提示与推理前缀。
- $a_t$：原始轨迹中的第 t 个推理步骤。
- $c_i$：从步骤前状态直接采样到终止符的第 i 个续写。
- $c'_j$：保留原步骤后，从新前缀采样到终止符的第 j 个续写。
- $N$：用于估计步骤前价值的续写次数；主要数据构造中取 50。
- $M$：用于估计固定步骤后 Q 值的续写次数；一般定义允许其与 N 不同。
- $\circ$：字符串拼接，包括所需的聊天模板格式。
- $\hat A(s_t,a_t)$：由有限续写样本得到的步骤优势估计。

<div class="equation-explanation" markdown="1">

**直观理解**：期望奖励无法从模型内部直接读取，因此用多次随机续写中目标答案出现的比例近似。这里展开写出两个样本均值以明确估计过程；原文公式（3）直接给出二者之差，而样本均值定义见同段文字。<br>
**原文位置**：第 3 节“Monte Carlo Estimation”，公式（3）及其前文定义

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：优势标签的生成本身不是参数训练，而是对固定生成策略 $\pi$ 做蒙特卡洛测量与统计判定。对于微调 critic，论文说明其在相同四类 Qwen 骨干和提示模板上添加回归头，以五个数学推理数据集的 $80%$ 划分训练“价值预测”，然后由预测价值导出优势；但所给正文节选没有列出具体损失函数、目标变体公式或优化器设置，并明确把不同训练目标放在第 B.3 节，因此不能据此补造均方误差等目标。方法上的关键连接是：critic 不直接把语言风格当作重要性，而是拟合由 rollout 奖励概率定义的价值信号，再通过步骤前后的预测价值差得到步骤重要性。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 奖励条件化的优势定义**

价值 $V^\pi(s)$ 表示从状态 $s$ 按模型策略继续生成后获得奖励 $1$ 的概率，$Q^\pi(s,a)$ 表示先固定步骤 $a$ 再继续生成时的同一概率，优势为两者之差。正确性奖励测量步骤对正确答案的贡献；自优势奖励测量步骤对复现原轨迹实际答案的贡献，后者是论文默认设置。

> 直观理解：同一段文字可能推动正确答案，也可能稳定地推动错误答案；因此“有作用”并不等于“正确”。自优势专门捕捉模型实际为何走向其最终答案，而正确性优势回答该步是否帮助解对题。

**2. 基于 PELT 的统计标签生成器**

作者不对数百个步骤分别执行独立的两比例 $z$ 检验，而是利用价值估计沿推理顺序形成时间序列这一结构。PELT 在分段拟合误差与分段数量惩罚之间权衡，找出持久变化；之后再用 Beta 后验检查变化幅度是否以至少 $0.95$ 的概率超过 $\delta=0.1$。

> 直观理解：逐句单独检验会因检验次数过多而产生假阳性，常规多重比较校正又会损失检测能力。把相邻步骤联合看成一条曲线，可以区分“采样抖动”和“从此以后答案概率真正改变”。

**3. 文本评判器、微调 critic 与噪声上限**

现成评判器包括 Qwen3-1.7B、Qwen3-8B、Qwen3-32B 和 Qwen3.6-27B，均开启 thinking mode；critic 在这些骨干上增加回归头。由于关键步骤占比很低，评估采用排序导向的 PR-AUC 与 precision@$k%$，并通过把同一响应的 rollout 分成两半构造保守和乐观的 split-half 噪声上限。

> 直观理解：类别极不平衡时，简单准确率可能靠“全部判为不重要”取得高分，因此要看模型能否把少数关键步骤排到前面。噪声上限还承认蒙特卡洛标签本身不完全稳定，避免把达不到 $1.0$ 错误地解释为评判器能力不足。

**训练与推理**

数据与标签阶段先让 Qwen3-1.7B、Qwen3-4B 和 Qwen3-8B 在 thinking mode 关闭时，对六个数学基准各抽取的 30 道题生成每题 10 个响应；另对 Qwen3-1.7B 的 thinking mode 开启版本在 AIME 24、AIME 25 和 GSM8K 上重复生成，并因计算成本去除超过 600 步的长尾响应。每个响应按双换行切步，对每个步骤前缀使用原生成模型执行 rollout；主要设置为每个前缀 $N=50$ 次，并按最终答案是否匹配原响应计算自优势。随后将价值序列送入 PELT，结合 $\delta=0.1$ 的效应阈值和 $0.95$ 的后验概率要求生成步骤级标签。

评判阶段有两条路径：OOB judge 接收步骤相关文本，在单次调用中给出 $[-1,1]$ 内的优势评分；微调 critic 使用五个数学数据集的 $80%$ 训练划分学习价值预测，并在剩余 $20%$ 的同分布数据及 AMC 23 分布外数据上推断。预测分数用于排序关键步骤，且正确响应与错误响应分开统计。为衡量标签采样噪声，作者把每条响应的 rollout 拆成两半：一半产生优势估计，另一半或完整样本产生标签，分别形成保守和乐观上限；这不是模型训练步骤，而是解释可达到性能所必需的评估校准。

**复现信息**

复现中最关键的设置是：步骤以双换行符 $\n\n$ 划分；主要数学分析每个前缀使用 $N=50$ 个 rollout；必须由生成该轨迹的原模型重采样，以免假设跨模型价值可迁移；默认奖励是“最终答案匹配原轨迹答案”的自优势，正确性分析才使用官方正确答案。关键步骤检测采用精确二项代价的 PELT，惩罚在模拟平坦序列上校准为每条序列 $2%$ 假阳性率，并要求 $P(|A^\pi|>0.1)\geq0.95$。

数据规模方面，thinking mode 关闭的主集合覆盖六个数学基准、每个基准 30 题且每题 10 个响应，即每个生成模型共 1,800 个响应、180 道不同问题；thinking mode 开启的分析只覆盖三个基准，并保留过滤后约 $81%$ 的响应。评判任务中关键步骤非常稀少，因此应使用 PR-AUC 与 precision@$k%$ 而不是普通准确率，并报告 split-half 噪声上限。所给节选未包含解码超参数、critic 的确切损失、学习率、训练轮数、上下文格式及 $k$ 的具体取值，这些内容分别被指向附录 B、H 等位置，复现时仍需核对原文附录。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 原文未明确报告数据集名称、规模、划分方式或具体任务；摘要仅说明实验基于模型生成的 chain-of-thought 推理轨迹和最终答案开展。
- 原文未明确报告用于初始回答生成与 Monte Carlo rollouts 的输入数据规模及训练、验证、测试划分。
- 原文未明确报告是否使用多个数据集或不同任务类型，因此无法判断结论在任务分布变化下的稳定性。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**step-importance identification performance**

衡量评审者识别高优势推理步骤的能力；优势被定义为包含某一步骤相对于不包含该步骤时，期望奖励的变化，奖励示例是最终答案是否正确。 （越高越好，因为表示预测出的重要步骤与基于 Monte Carlo rollouts 估计的高优势步骤更一致；具体指标名称、计算公式和数值原文未明确报告。）

</div>
<div class="metric-item" markdown="1">

**prevalence baseline comparison**

比较模型是否超过仅利用高优势步骤出现比例的简单预测规则，检验模型是否学习到超出标签先验频率的信息。 （模型性能高于该基线时更好；原文未明确报告具体数值或统计检验。）

</div>
<div class="metric-item" markdown="1">

**distance to noise ceiling**

衡量模型性能与噪声上限之间的差距，用于判断步骤重要性是否接近可由当前标签和评估过程可靠恢复的程度。 （与 noise ceiling 的差距越小越好；原文未明确报告具体差距计算方式或数值。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 通用 LLM judges 识别高优势步骤

<div class="result-value" markdown="1">

足够强的 LLM 评审者能够超过 prevalence baseline，但性能明显低于 noise ceiling。原文未明确报告具体分数、模型数量或显著性检验。

</div>

这说明推理步骤的文字并非完全没有关于功能重要性的信息：较强模型可以利用一部分可见线索进行判断。但低于 noise ceiling 表明文本可恢复的信息不完整，不能据此把评审者判断当作步骤真实因果作用的充分测量；该结果也不证明所有模型或所有任务都具有相同能力。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We find that sufficiently capable LLMs can outperform a prevalence baseline but fall well short of a noise ceiling.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 微调步骤级批评器在错误回答上的表现

<div class="result-value" markdown="1">

将模型微调为 step-level critic 后，对 incorrect responses 的识别能力有 strong improvement。原文未明确报告改进前后的数值、评估指标或统计显著性。

</div>

训练确实能帮助模型更好地判断错误回答中的步骤重要性，说明部分步骤功能信号可以通过监督学习被提取出来。但该结果不能说明微调后的批评器已经忠实地恢复了模型实际使用的推理过程，也不能排除它学习了与错误模式相关的表面线索。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Fine-tuning a model as a step-level critic yields strong improvement for incorrect responses but remains distant from ceiling for correct responses, suggesting that step importance is only partially recoverable from the text of the reasoning trace.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 微调步骤级批评器在正确回答上的表现

<div class="result-value" markdown="1">

对于 correct responses，微调后的步骤级批评器仍然明显距离 noise ceiling；作者据此认为步骤重要性只能从推理轨迹文本中部分恢复。原文未明确报告具体分数或与错误回答之间的数值差异。

</div>

即使最终答案正确，文本中的步骤也未必清楚标示哪些步骤真正决定了答案，因此正确回答不能简单被视为更容易进行过程监督。这削弱了仅依赖可读推理文本来构造可靠 process reward model 的做法，但并不证明所有正确推理轨迹都不可解释。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Fine-tuning a model as a step-level critic yields strong improvement for incorrect responses but remains distant from ceiling for correct responses, suggesting that step importance is only partially recoverable from the text of the reasoning trace.

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

- prevalence baseline：依据高优势步骤在评估集合中的出现比例进行预测，用于检验评审者是否至少超过类别或标签的先验频率；摘要明确称“a prevalence baseline”。
- noise ceiling：作为受观测噪声或标签不确定性限制的上界，用于判断评审者距离可达到的性能上限还有多远；摘要明确称“a noise ceiling”。
- out-of-the-box LLM judges：不进行任务特定微调的 LLM 评审者，用于衡量通用模型仅凭推理文本判断步骤重要性的能力。
- fine-tuned step-level critic：在步骤级监督下微调的批评器，用于检验额外训练是否能弥补通用 LLM 评审者与优势标签之间的信息缺口。

**实验想回答的问题**

- LLM 评审者能否依据推理轨迹文本识别高优势步骤，即识别那些会提高最终正确答案期望奖励的步骤？
- 将模型微调为步骤级批评器后，步骤重要性是否能从推理文本中更充分地恢复，且在正确回答与错误回答上是否表现一致？

**实验实现**

作者将步骤重要性操作化为 advantage：通过 Monte Carlo rollouts 估计加入某个推理步骤所带来的期望奖励变化，并以此构造评估所需的 ground truth。随后评估通用 LLM judges 是否能从步骤文本识别高优势步骤，并进一步将模型微调为 step-level critic，分别考察错误回答和正确回答。附录指出，初始模型回答和 rollouts 均使用 temperature 为 $1.0$、top-$p$ 为 $0.95$ 的解码设置；原文未明确报告模型名称、rollout 数量、提示模板全文、训练超参数、数据划分、随机种子及具体评价指标。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：以因果优势估计检验思维链步骤文本能否反映其实际功能重要性，核心关注推理轨迹的忠实性与可解释性。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`428e820532d22fd7ce5bc77fc6bbdc2d37a89b6e47bd8d07e5845eb958aa12c8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
