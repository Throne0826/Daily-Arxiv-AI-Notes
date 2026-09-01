---
title: "[论文解读] Automated Testing of LLM-Based Post Hoc Explainers Using Model Checking as an Oracle"
description: "[arXiv 2608.30581][幻觉检测] 原文未明确报告。"
arxiv_id: "2608.30581"
announcement_date: "2026-09-01"
primary_category: "hallucination"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:48:47.434773+00:00"
source_sha256: "5a9a6e2a829eaf5850c92531cffe069fca633c00a224a1cec2842cd24a7c6aac"
tags:
  - "幻觉检测"
  - "LLM 其他"
  - "LLM Reasoning"
  - "软件测试"
  - "大语言模型"
  - "概率模型检验"
  - "可解释强化学习"
  - "测试预言机"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">幻觉检测 · arXiv 2608.30581</p>

# Automated Testing of LLM-Based Post Hoc Explainers Using Model Checking as an Oracle

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Dennis Gross, Helge Spieker</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Simula Research Laboratory, Oslo, Norway</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30581v1) · [PDF 下载](https://arxiv.org/pdf/2608.30581v1) · **关键词** 软件测试, 大语言模型, 概率模型检验, 可解释强化学习, 测试预言机<br>


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

本文位于可解释强化学习、概率模型检验与软件测试的交叉领域。序贯决策任务通常用有限马尔可夫决策过程（MDP）描述：智能体观察状态、选择动作，环境依据转移概率产生后继状态。深度强化学习得到的策略往往难以直接解释，因此大语言模型（LLM）被用作事后解释器，根据环境、当前状态和决策查询生成自然语言说明；本文关注如何自动检验这些说明是否忠实于底层环境和策略。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**马尔可夫决策过程（MDP）**

MDP用状态、动作和概率转移描述智能体与随机环境的交互，并假设下一步行为只依赖当前状态和所选动作。本文研究有限状态、有限动作集合以及无记忆策略的情形。

</div>
<div class="concept-item" markdown="1">

**概率模型检验**

概率模型检验把系统表示为形式模型，并计算某个性质成立的精确概率，例如最终到达目标状态或危险状态的概率。本文利用这些结果作为判断LLM答案是否正确的测试预言机。

</div>
<div class="concept-item" markdown="1">

**事后解释器与测试预言机**

事后解释器是在策略已经作出动作后，根据当前状态回答“为什么选择该动作”的LLM。测试预言机提供可比较的正确答案；本文用模型检验器计算的环境性质结果解决原本缺少可靠答案的问题。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括一个形式化的有限MDP、其自然语言描述、一个状态级决策查询，以及待测试的LLM解释器。MDP包含状态集合、初始状态、动作集合、随机转移函数和状态标签；策略是从状态到动作的无记忆映射。LLM接收描述环境和状态的提示，生成自然语言回答，解析器再将回答转为结构化结果，例如是/否判断或动作排序。系统需要自动生成具有代表性的查询和状态级测试用例，并将LLM答案与模型检验器计算的精确属性结果比较，从而评估解释是否忠实。测试阶段假定存在环境的形式模型，但该假设仅用于建立测量工具；论文希望借此推断同类LLM在没有可验证预言机的模型自由场景中的可信程度。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{M}=(S,s_{0},\mathit{Act},P,\mathit{AP},L)$**

MDP；其中 $S$ 是有限状态集合，$s_{0}$ 是初始状态，$\mathit{Act}$ 是有限动作集合，$P$ 是状态—动作—后继状态的转移概率，$\mathit{AP}$ 是原子命题集合，$L$ 为状态标记函数。

</div>
<div class="notation-item" markdown="1">

**$\pi:S\to\mathit{Act}$**

确定性的无记忆策略，表示策略在每个状态 $s$ 选择的动作；固定策略后，MDP中的选择被消除，系统变为离散时间马尔可夫链。

</div>
<div class="notation-item" markdown="1">

**$P:S\times\mathit{Act}\times S\to[0,1]$**

转移函数；$P(s,a,s')$ 表示在状态 $s$ 执行动作 $a$ 后到达状态 $s'$ 的概率，并且对每个启用动作有 $\sum_{s'}P(s,a,s')=1$。

</div>
<div class="notation-item" markdown="1">

**$\mathsf{P}_{\max}=?\,[\mathsf{F}\;\textit{goal}]$**

PCTL可达性性质，询问从某状态出发、在所有策略中最终到达目标状态的最大概率；其中 $\mathsf{F}$ 表示“最终”，$\textit{goal}$ 表示目标状态标签。论文还使用 $\mathsf{P}_{\min}=?\,[\mathsf{F}\;\textit{unsafe}]$ 计算最终到达危险状态的最小概率。

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

该方法把基于大语言模型的事后解释器视为待测系统，把概率模型检测器提供的精确结果视为测试预言机。输入是一个马尔可夫决策过程（MDP）、待验证的概率性质、查询类别、待测大语言模型以及测试预算；系统先计算状态和动作的精确参考值，再生成并按诊断难度排序的自然语言测试用例，最后将模型回答解析为结构化结果并与预言机自动比对，输出各查询类别和各模型的通过判定。直观地说，它不是直接判断一段解释“听起来是否合理”，而是把解释拆成可验证的小问题，例如“哪个动作最好”或“该状态是否是死路”，再用环境的精确计算结果逐题核对。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造概率模型与测试预言机

使用概率模型检测器对 MDP 和 PCTL 性质进行计算，得到每个可达状态的性质结果 $V(s)$、每个可用动作的动作值 $Q(s,a)$，以及需要时的危险度 $D(s)$。由这些结果进一步生成动作排序、最优动作集合、最差动作集合、最优策略、死路状态和瓶颈状态；瓶颈状态通过将候选状态设为吸收状态后重新检查目标可达性来确定。

<div class="method-step__io" markdown="1">

**输入**：一个 MDP $\mathcal{M}=(S,s_{0},\mathit{Act},P,\mathit{AP},L)$，以及一个主要的 PCTL 可达性性质；若测试安全性，还输入定义危险度 $D(s)$ 的安全性质。<br>
**输出**：每个候选测试问题所需的精确期望答案，包括状态概率、动作偏好、状态间比较结果、瓶颈判定和子集判定。

</div>

**直观理解**：这一步先让 Storm 等模型检测器把环境“算透”，因此后续不依赖人工猜测答案。它相当于为每道题制作标准答案：模型负责回答自然语言，模型检测器负责告诉系统什么才是正确的环境事实。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 按查询分类生成测试用例

按照三个维度组织查询：对象可以是状态性质或动作偏好，范围可以是单个状态或状态子集，模式可以是单对象判断或两个对象比较。由此生成单状态、状态对或状态子集测试用例，覆盖达到目标的概率、瓶颈、死路、最佳动作、最差动作、完整动作排序、更加有希望的状态和更加安全的状态等原子问题。

<div class="method-step__io" markdown="1">

**输入**：模型检测结果、查询类别、环境描述模板和可访问状态集合。<br>
**输出**：结构化候选测试用例，每个用例包含所需状态、动作或状态子集，以及对应的预期判定。

</div>

**直观理解**：自然语言问题本身没有明显的测试结构，所以方法先把它们整理成固定题型。每道题只检查一个小事实；如果模型连这些基本事实都答错，就不能认为它能忠实解释完整策略。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 计算诊断难度并优先选择

为每个候选用例计算诊断难度 $\delta$，并在测试预算内保留难度最高的用例；瓶颈、子集瓶颈和子集死路三类二元问题先平衡正例与负例，再在各类别内按 $\delta$ 排序。难度主要刻画三种风险：候选值接近导致的歧义、正确动作在多个干扰项中的选择性，以及结构上像瓶颈但实际不是瓶颈的高显著性诱饵。

<div class="method-step__io" markdown="1">

**输入**：候选测试用例及其预言机数值，包括 $V(s)$、$Q(s,a)$、$D(s)$、动作集合和底层状态图的介数中心性 $C_B(s)$。<br>
**输出**：按题型和诊断难度排序的有限测试集。

</div>

**直观理解**：测试预算通常不允许穷举所有状态，因此优先挑最容易暴露模型错误的题。比如两个状态的成功概率很接近，或一个真正的瓶颈旁边有一个同样位于许多路径上的诱饵状态，这类题比明显简单的题更有诊断价值。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 提示执行、解析与判定

将选中的状态、状态对或状态子集填入环境特定的提示模板，要求 LLM 输出概率、判断、动作或动作排序等结构化答案；每个测试用例重复执行若干次，以考虑 LLM 的随机性。解析回答后，按查询类别与预言机精确比较：概率必须等于 $V(s)$，最佳或最差动作必须属于对应集合，动作排序需在允许并列的条件下正确，其他判断则与相应状态或子集事实核对。

<div class="method-step__io" markdown="1">

**输入**：优先测试集、自然语言提示模板、待测 LLM、每个测试用例的重复次数。<br>
**输出**：每个 LLM、每个查询类别和每次重复的通过或失败判定，并可聚合为类别级测试结果。

</div>

**直观理解**：系统把同一批题发给每个模型，并把自由文本转换成可检查的答案格式。最终不是由评审者凭印象打分，而是逐项检查模型是否答中了计算得到的标准答案。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### MDP 定义与转移归一化

$$
\mathcal{M}=(S,s_{0},\mathit{Act},P,\mathit{AP},L),\qquad P:S\times\mathit{Act}\times S\to[0,1],\qquad \sum_{s'}P(s,a,s')=1
$$

**符号说明**

- $\mathcal{M}$：用于描述环境的马尔可夫决策过程。
- $S$：有限状态集合。
- $s_{0}$：初始状态，且 $s_{0}\in S$。
- $\mathit{Act}$：有限动作集合。
- $P(s,a,s')$：在状态 $s$ 执行动作 $a$ 后转移到状态 $s'$ 的概率。
- $\mathit{AP}$：有限原子命题集合，例如目标或不安全标签。
- $L$：状态标记函数，将状态映射为在该状态成立的原子命题集合。

<div class="equation-explanation" markdown="1">

**直观理解**：这个定义规定了测试环境的输入格式：系统处于某个状态，策略选择动作，环境按照概率分布产生下一状态。最后的归一化条件保证每个已启用动作的所有可能后继概率之和为 $1$。<br>
**原文位置**：第 3.1 节

</div>

</div>

<div class="equation-block" markdown="1">

#### 查询诊断难度

$$
\delta=1-2\left|V(s)-\tfrac{1}{2}\right|,\qquad \delta=1-\frac{|A^{\star}(s)|}{|\mathit{Act}(s)|},\qquad \delta=1-|V(s_{1})-V(s_{2})|
$$

**符号说明**

- $\delta$：测试用例的诊断难度分数，通常越大表示越值得优先测试。
- $V(s)$：从状态 $s$ 出发满足目标性质的最优概率。
- $A^{\star}(s)$：状态 $s$ 中使动作值达到最大值的最优动作集合。
- $\mathit{Act}(s)$：状态 $s$ 中可执行的动作集合。
- $s_{1},s_{2}$：用于比较“哪个状态更有希望”的两个状态。

<div class="equation-explanation" markdown="1">

**直观理解**：同一个符号 $\delta$ 会根据题型采用不同实例：成功概率越接近 $0.5$，判断越模糊；最优动作越少，越需要从干扰动作中精准挑出它；两个状态的概率越接近，比较题越难。系统用这些分数在有限预算下优先测试高风险案例。<br>
**原文位置**：第 5 节“Test case generation and prioritization”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该方法不训练或微调 LLM，也没有提出需要优化的神经网络损失函数；模型检测器、测试用例排序器和答案判定器均在推理与测试阶段运行。其核心目标是测量现有 LLM 解释回答相对于精确环境事实的通过率，而不是通过梯度优化改变模型参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 概率模型检测预言机**

MDP 中的状态转移由 $P(s,a,s')$ 给出，固定策略后可得到诱导离散时间马尔可夫链。对目标可达性使用 $\mathsf{P}_{\max}=?\ [\mathsf{F}\;\textit{goal}]$ 等 PCTL 查询，计算状态性质结果 $V(s)$ 和动作值 $Q(s,a)$；对安全问题另行计算 $D(s)=\mathsf{P}_{\min}[\mathsf{F}\;U]$。

> 直观理解：该模块把环境中的随机性和长期后果精确算出来，例如某动作最终到达目标的概率，而不是只看下一步是否看起来合理。它提供自动化测试所缺少的可靠标准答案。

**2. 查询分类与难度排序器**

查询由对象、范围和模式三个维度组合而成；难度函数根据任务类型使用概率间隔、动作集合大小、相邻排序间隔、介数中心性或子集中的最低价值等信息。中心性 $C_B(s)$ 只用于寻找结构上具有迷惑性的候选，不作为瓶颈事实本身。

> 直观理解：这一模块将开放式解释问题变成可枚举的测试空间，并优先安排最可能出错、因而最能区分模型能力的案例。尤其要区分“像瓶颈”和“确实是瓶颈”：前者只是选题启发式，后者仍由模型检测器验证。

**3. LLM 提示—解析—判定模块**

系统为每一类查询使用提示模板，将状态描述、可用动作和问题填入提示，并要求模型返回可解析的 JSON 等结构化格式。解析后的答案依据题型与 $V(s)$、$A^{\star}(s)$、$A^{\circ}(s)$、动作真实排序、$D(s)$ 或精确瓶颈集合进行自动判定。

> 直观理解：该模块把语言模型的自然语言输出变成机器可核验的答案。这样既能测试模型是否理解环境事实，也能避免人工逐条阅读解释造成的主观性和规模限制。

**训练与推理**

训练阶段原文未明确报告，且所述方法不包含模型训练。推理阶段首先对输入 MDP 和 PCTL 性质运行模型检测，得到 $V(s)$、$Q(s,a)$、必要时的 $D(s)$ 及派生标准答案；随后按查询分类生成候选状态、状态对或状态子集，用对应的 $\delta$ 排序并截取测试预算内的样本。每个测试用例被填入提示模板并发送给每个待测 LLM，重复执行以处理非确定性；系统解析模型回答，按查询类型与预言机进行精确比较，最后聚合每个模型和查询类别的通过或失败结果。

**复现信息**

复现或公平解释结果所需的关键设置包括：输入是 MDP、相关 PCTL 性质、查询类别及其提示模板、测试预算和每个用例的重复样本数；环境特定部分主要是如何用文字描述状态和如何要求结构化输出。答案判定对概率采用与 $V(s)$ 的相等比较，对最佳和最差动作采用集合成员判定，对完整排序允许真实相等值动作任意交换；瓶颈必须通过将候选状态设为吸收状态后重新检查可达性确认，$C_B(s)$ 仅用于排序而不是作为真值。原文未明确报告具体测试预算、重复样本数、提示模板总数以及模型检测器的运行参数。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 七个马尔可夫决策过程（$MDP$）环境组成统一测试基准：Frozen Lake、Wolf–Goat–Cabbage、Water Jug、Transporter、Stock Market、Job Shop和Dam。每个环境都配有一个可达性性质，其经概率模型检查得到的结果充当解释正确性的oracle。
- 环境任务覆盖随机移动、河流运输、随机价格、随机工期和随机入流等情形；Frozen Lake与Wolf–Goat–Cabbage含瓶颈状态，其余环境不含瓶颈状态，因此相应三类瓶颈查询记为缺失。该设计用于测试方法能否跨越不同状态空间结构与决策任务。
- 测试样本不是传统训练/验证/测试数据划分，而是从每个查询类别中按诊断难度$\delta$选取的状态；每类测试预算为$20$个状态，并与随机状态选择进行比较。原文未明确报告各环境的训练集、验证集或测试集划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**测试通过率**

每个环境—查询类别单元中，回答通过模型检查oracle判定的测试用例比例，取值范围为$[0,1]$；它衡量自然语言解释是否给出了与环境事实一致的答案。 （越高越好，因为更高比例表示更多回答与精确oracle一致。）

</div>
<div class="metric-item" markdown="1">

**诊断优先级与随机选择的分数差**

在同一模型和查询类别下比较诊断难度排序与随机状态选择的通过率；优先级分数更低表示选出了更难的测试状态。 （对于测试生成方法而言，优先级分数相对随机分数更低通常更好，表示测试集更有诊断性；但它不意味着模型质量更差。）

</div>
<div class="metric-item" markdown="1">

**平均查询类别分数**

将所有模型和两种状态选择策略的结果合并后，计算每个查询类别的平均通过率，用于估计类别的总体难度。 （作为难度指标时分数越低越难；它反映类别层面的困难程度，而不是某一个模型的最佳性能。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### RQ1：诊断难度优先级与随机状态选择的比较

<div class="result-value" markdown="1">

在$220$个可比较单元中，诊断优先级得到更低分数的单元有$75$个（$34.1\%$），随机选择更低的有$61$个（$27.7\%$），持平$84$个（$38.2\%$）；单侧Wilcoxon符号秩检验得到$p=0.035$。作者据此认为诊断优先级能获得更多非平凡测试用例。

</div>

该结果支持测试生成器确实能在总体上集中到更难的状态，而不是只改变抽样噪声。它不表示所有模型、所有类别和所有环境的优先级分数都必须更低；随机回答器对状态难度不敏感，小模型接近分数下限时也缺少进一步下降空间。

<div class="result-source" markdown="1">

来源：第6.2节“Effect of diagnostic prioritization (RQ1)”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Over all 220 comparable cells, prioritization yields the harder case in 75 cells (34.1%), the easier case in 61 (27.7%), and a tie in 84 (38.2%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### RQ2：不同规模与推理能力模型的总体通过率

<div class="result-value" markdown="1">

跨七个环境平均，Qwen3.5得分$0.85$，Gemma 4 31B得分$0.70$，均高于Random基线的$0.51$；Gemma 3 1B在诊断优先级测试上为$0.43$，低于Random。随机选择下，Gemma 3 1B为$0.55$，Random为$0.54$，二者基本持平。

</div>

结果表明，较强模型更能回答需要精确环境推理的解释问题，且诊断优先级可以揭示小模型在困难状态上的错误。它支持模型间的相对区分，但不能证明通过率等同于自然语言解释的全部质量，也不能说明模型在未测试环境或未覆盖的查询类型上同样可靠。

<div class="result-source" markdown="1">

来源：第6.2节“LLM performance (RQ2)”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Averaged over all environments, the reasoning model Qwen3.5 is strongest at 0.85, followed by Gemma 4 31B at 0.70, both clearly above the Random baseline at 0.51.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### RQ3：查询类别的总体难度排序

<div class="result-value" markdown="1">

按两种状态选择策略、所有模型的结果汇总后，最难类别为dead ends in subset（$0.59$）和worst action（$0.60$），其次为bottleneck in subset（$0.63$）；最容易的是关系型which-is-bottleneck（$0.72$）。

</div>

模型更难回答涉及子集内多个状态比较、死端识别或最差动作判断的问题，可能是因为这些问题要求组合式比较而非单一事实检索。该排序用于指导后续测试资源分配，但平均分混合了模型差异、环境差异和选择策略，不能单独归因于某一种认知能力。

<div class="result-source" markdown="1">

来源：第6.2节“Category difficulty (RQ3)”及图3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The hardest categories are dead ends in subset (0.59) and worst action (0.60), followed by bottleneck in subset (0.63); the easiest are the binary bottleneck queries, at 0.72 for the relational which-is-bottleneck variant.

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

- Random：均匀随机回答器，用于衡量不利用环境信息时的机会水平；它也是比较诊断优先级是否真正筛出困难状态的基线。
- Optimal policy：最优策略，按构造达到分数$1$，作为测试分数的理论上限，而不是可部署的语言模型基线。
- Gemma 3 1B：小规模开源权重模型，用于检验低容量模型在结构化解释测试中的表现。
- Qwen3.5与Gemma 4 31B：较大规模开源权重模型，其中Qwen3.5使用逐步推理模式；二者用于检验模型规模与推理能力是否对应更高的解释忠实度。

**实验想回答的问题**

- RQ1（优先级排序）：基于诊断难度的测试用例排序，是否比随机选取发现更多非平凡、较难的测试状态？
- RQ2–RQ3（模型区分与类别难度）：更强的$LLM$是否通过更多测试用例，不同查询类别的固有难度是否存在差异？

**实验实现**

实验使用三个通过Ollama服务的开源权重模型：Gemma 3 1B、Qwen3.5和Gemma 4 31B；回答温度设为$0$，采用贪心解码和样本数$1$，因此输出近似确定。模型回答被约束为结构化JSON并自动解析。每个环境的oracle由Storm模型检查器一次性计算，再复用于所有模型与查询类别。每类使用$20$个按诊断难度$\delta$选择的状态，并与随机选择比较。实验在Docker容器中运行，报告硬件为16 GB内存、AMD Ryzen 7 7735HS（16线程）和Ubuntu 20.04.5 LTS；模型检查器版本为Storm 1.12.0，语言模型部署在本机或Ollama云端并通过REST API访问。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 状态选择策略：诊断难度优先级 versus 随机选择 | 优先级方案在$220$个可比较单元中有$75$个单元筛出更难案例，随机方案有$61$个，持平$84$个；Wilcoxon检验的单侧$p=0.035$。表1进一步逐单元报告“prioritized/random”分数，以显示优先级是否降低通过率。 | 这是对测试用例生成组件的关键消融：固定模型、环境和查询类别，仅替换状态选择方式。如果优先级选择得到更低通过率，说明其确实增加了测试难度；但由于仍有许多持平或反向单元，效果不是普遍、无条件的提升。 | 第6.2节“Effect of diagnostic prioritization (RQ1)”<br><span class="experiment-evidence">A one-sided Wilcoxon signed-rank test rejects the null in favor of prioritized < random at p=0.035.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It develops automated model-checking tests to detect unfaithful and factually incorrect explanations generated by LLMs.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`5a9a6e2a829eaf5850c92531cffe069fca633c00a224a1cec2842cd24a7c6aac`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
