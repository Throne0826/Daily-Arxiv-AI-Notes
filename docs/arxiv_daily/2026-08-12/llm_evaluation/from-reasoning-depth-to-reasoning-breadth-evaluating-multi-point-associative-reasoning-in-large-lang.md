---
title: "[论文解读] From Reasoning Depth to Reasoning Breadth: Evaluating Multi-Point Associative Reasoning in Large Language Models"
description: "[arXiv 2608.10444][LLM 评测] 本文提出双语基准 MPAR-Bench，用多条彼此独立且语义多样的线索共同指向一个目标词，以检验大语言模型能否进行稳健的多点联想推理，而不仅是沿单一路径进行更深的链式推理。"
arxiv_id: "2608.10444"
announcement_date: "2026-08-12"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-12T03:04:29.390224+00:00"
source_sha256: "38dff2fa50776486103d1b5d04bf457a2c6aa720ddad55f7e05726dc339951cf"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "推理广度"
  - "推理深度"
  - "多点关联推理"
  - "语义线索整合"
  - "双语基准"
  - "MPAR-Bench"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.10444</p>

# From Reasoning Depth to Reasoning Breadth: Evaluating Multi-Point Associative Reasoning in Large Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-12</span>
<span><strong>作者</strong> Si'an Xie, Jiaxun Liu, Biao Yang, Wei Yuan, Fan Yang, Tingting Gao, Ming Wu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Beijing University of Posts and Telecommunications；Peking University；Kuaishou Technology</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.10444v1) · [PDF 下载](https://arxiv.org/pdf/2608.10444v1) · **关键词** 大语言模型, 推理广度, 推理深度, 多点关联推理, 语义线索整合, 双语基准, MPAR-Bench<br>


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

本文提出双语基准 MPAR-Bench，用多条彼此独立且语义多样的线索共同指向一个目标词，以检验大语言模型能否进行稳健的多点联想推理，而不仅是沿单一路径进行更深的链式推理。

**不用术语来说**：现有推理测试通常要求模型沿着一系列连续步骤得到答案，但现实任务中的证据往往来自多个不同角度：每条信息单独看都不充分，只有把它们放在一起才能确定结论。论文关注模型能否同时考虑这些分散线索、发现它们的共同指向，并避免被缺失线索、无关信息或线索表达方式的变化所干扰。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 MPAR-Bench，将“推理广度”具体化为多对一线索整合任务：模型接收数量可变、形式自由且语义多样的线索，并恢复其共同指向的隐藏目标；同时通过线索遮蔽、顺序打乱、干扰项注入和多步线索等扰动检验稳健性。
- 建立由多智能体线索生成、基于嵌入的多样性筛选和人工核验组成的数据构建流程，并配套精确匹配、ANLS、嵌入相似度及推理轨迹验证等由粗到细的评估方式，以降低记忆已有题目的风险并区分答案错误与线索整合过程错误。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大语言模型推理评测通常关注“推理深度”，即模型能否沿一条较长的线性路径进行逐步演绎，例如完成数学推导、程序化解题或多步逻辑判断。本文转而研究与之互补的“推理广度”：当证据来自多个相互独立、语义方向不同的线索时，模型能否同时保留这些局部关系，并将其汇聚为一个共同概念。该能力适用于多文档综合、跨领域类比、假设生成，以及存在缺失信息或干扰信息时的判断；因此，一个模型即使善于沿单一路径深入推理，也未必能够可靠地整合多条分散线索。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**推理深度（reasoning depth）**

指模型沿相对线性的推理链逐步推出答案的能力，重点在推理步骤的长度、复杂度与逻辑连续性。数学文字题和多步逻辑题通常主要测量这一维度。

</div>
<div class="concept-item" markdown="1">

**推理广度（reasoning breadth）**

指模型并行考察多个语义方向，并把分散、互补甚至部分含噪的证据整合为统一结论的能力。它关注的不是单条链能走多深，而是模型能否协调多条关联路径。

</div>
<div class="concept-item" markdown="1">

**多点关联推理（multi-point associative reasoning）**

本文将其操作化为“多对一”的概念汇聚任务：若干独立生成且语义多样的线索共同指向一个隐藏目标词。模型需要寻找各线索与目标之间的不同联系，而不能只依赖某一条固定的组合规则。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

MPAR-Bench把推理广度设置为双语目标词恢复问题。每个样本向模型提供若干独立生成、形式自由且语义方向不同的英文或中文线索，模型的输出是这些线索共同指向的单个隐藏目标；线索数量可以变化，并不要求像固定三线索测试那样遵循统一构词关系。任务假设不同线索分别提供关于同一目标的局部证据，核心考察模型能否完成从多条关联到一个答案的汇聚，而不是沿预先排列的单一路径推导。基准包含共计 1,000 个样本，答案空间取自公开词表，但线索集合从头生成，以降低直接记忆已有题目的风险；论文还以线索遮蔽、顺序打乱、干扰项注入和多步线索检验这种整合能力在信息不完整、排列变化、噪声存在及关联链变长时是否稳定。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **MATH（Hendrycks et al., 2021）**: 该基准以数学问题衡量多步推导和程序化解题能力，是本文所称“推理深度”评测的代表。MPAR-Bench并非替代这类评测，而是补充其较少覆盖的多方向语义整合维度。
- **MMLU（Hendrycks et al., 2021）**: MMLU用于衡量模型在多学科任务中的知识与问题解决能力，但学科覆盖面广不等于单个样本要求并行整合多条异质线索。本文据此区分“任务或知识领域广泛”与“一个推理实例内部的推理广度”。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

多文档综合、跨领域类比、假设生成以及在证据不完整或含有干扰信息时作出判断，都要求模型同时保留若干局部关系，再把来自不同语义视角的证据协调成一个结论。即使模型能够沿单条路径进行很长的推导，也可能遗漏其他路径提供的信息，因此链式推理能力本身不足以保证其在这些现实场景中可靠工作。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **以推理深度为中心的通用与数学推理基准**：MATH、MMLU 等基准主要通过数学求解、知识问答或程序化推导，考查模型能否按照相对明确的步骤持续展开逻辑链；CoT 等方法则通过显式生成中间步骤来强化这种线性、逐步的求解过程。
- **RAT 类联想测试与既有桌游式基准**：RAT 类测试通常给出三个固定的复合词提示，要求寻找共同关联词；已有桌游式评测则多考查模型生成提示，或将一个固定词集合进行分组。这些任务涉及概念关联，但其提示数量、提示形式或模型承担的角色受到预先限定。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 深度导向基准主要测量沿单一推导方向持续前进的能力，不能直接判断模型是否会并行探索多个语义方向并汇聚分散证据；其后果是，一个在线性推理测试中表现优秀的模型，仍可能在多来源信息整合任务中失败。
- RAT 类测试采用固定数量和固定构词关系的提示，既有桌游基准又常聚焦提示生成或固定词集分组，因而没有隔离“猜测者依据开放数量、自由形式线索完成多对一整合”的能力，也缺少按扰动类型检查线索缺失、顺序变化和干扰信息影响的受控机制。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有评测尚未系统覆盖“推理广度”：缺少一个能够以开放数量、语义多样且从头生成的线索为输入，专门测量模型多对一概念汇聚能力，并进一步区分标准条件表现与不同证据扰动下稳健性的双语基准。

</div>
<div markdown="1"><span>核心问题</span>

当前大语言模型是否真正具备非线性、跨语义方向的多点联想推理能力，即能否从多条独立而分散的线索中恢复共同目标，并在部分线索缺失、顺序改变、加入干扰项或需要多步解释时仍保持稳定？

</div>
<div markdown="1"><span>作者直觉</span>

如果多条线索由相互独立的生成角色从不同语义角度产生，并经过语义多样性筛选和人工核验，那么单条线索通常不足以直接暴露答案，模型必须寻找所有线索的共同交集。再对线索集合施加受控扰动，就能观察模型究竟形成了稳定的跨线索关联，还是仅依赖某个显眼提示、固定顺序或表面词语相似性作答。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MPAR-Bench把“推理广度”操作化为多点联想推理：给定线索集合$C=\{c_1,c_2,\ldots,c_n\}$，模型需要找到唯一目标词$y$，并说明每条有效线索$c_i$与$y$之间的语义联系。与沿单一路径连续推导的推理深度不同，该任务要求模型先沿多个相对独立的语义方向建立联系，再将这些不重叠的局部证据汇聚成一个答案；同时通过线索遮蔽、顺序打乱、干扰项注入和多步联想检验这种整合能力是否稳健。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 目标词采样与双语任务设定

从公开词表中选择目标词$y$，再按同一构造流程分别建立英文和中文子集；两种语言各包含500个验证后条目，但中文条目额外允许成语、汉字字形或象形属性及当代文化梗等联想来源。

<div class="method-step__io" markdown="1">

**输入**：公开的RAT衍生词表和桌游Just One词卡，以及英文、中文两种语言环境。<br>
**输出**：用于后续生成线索的双语目标词集合。

</div>

**直观理解**：公开资源只提供“要猜的词”，题目中的线索由论文流程重新生成，因此不是直接搬运已有问答题。中英文共用任务骨架，但保留各自语言中特有的联想方式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多智能体分角度生成候选线索

多个基于大语言模型的线索生成智能体迭代提出候选线索；每个智能体被要求从不同语义角度关联$y$，并尽量避免与已接受线索表达相同信息。

<div class="method-step__io" markdown="1">

**输入**：一个目标词$y$、已经获准保留的线索集合，以及为当前生成智能体指定的联想角度。<br>
**输出**：一组与目标相关、来源角度多样但尚未完成质量控制的候选线索。

</div>

**直观理解**：这类似让多名玩家分别从人物、用途、文化或形状等不同方向提示同一个词。分配角度的目的不是增加线索数量本身，而是避免所有线索都只是同义改写。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 裁判筛选与嵌入多样性过滤

裁判智能体删除答案本身、直接同义词、翻译、谐音、明显词形变体、重复或近重复线索，以及无合理联系的低质量线索；随后依据线索与答案、线索与线索的嵌入相似度继续排除过于直接、关联过弱或信息重叠的候选，论文试验的相似度阈值范围为0.3至0.8。

<div class="method-step__io" markdown="1">

**输入**：目标词$y$、锁定的已接受线索、当前候选线索，以及Qwen3-Embedding-8B生成的语义表示。<br>
**输出**：与答案有意义关联、彼此低冗余且不会直接泄露答案的线索集合$C$。

</div>

**直观理解**：裁判先按明确规则检查“违规提示”，嵌入过滤再用向量距离做语义层面的复查。两层筛选共同保证每条线索既有用又带来新的信息，使答题者必须综合多个方向。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 唯一性审查与标准题定稿

裁判阶段剔除由全部线索仍无法唯一确定目标的题目，并重构存在问题的条目；此外，两名NLP专业硕士生在随机抽取的250个条目上独立判断目标是否唯一且无歧义。

<div class="method-step__io" markdown="1">

**输入**：经过生成和多样性过滤的候选题目，即线索集合$C$及预期答案$y$。<br>
**输出**：共1,000个验证后条目组成的MPAR-Bench标准设置，其中英文和中文各500个。

</div>

**直观理解**：多方向线索并不天然保证只有一个合理答案，因此还要检查所有线索合在一起是否确实指向同一目标。人工抽检用于评估自动构造流程留下歧义题的风险，而不是替代整个生成流程。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 多点联想推理任务定义

$$
C=\{c_1,c_2,\ldots,c_n\},\qquad \hat{y}=f(C)
$$

**符号说明**

- $C$：输入模型的线索集合。
- $c_i$：第$i$条线索；它应从相对独立且非冗余的语义方向提供关于目标的信息。
- $n$：当前题目包含的线索数量。
- $y$：数据集规定的隐藏目标词。
- $\hat{y}$：模型根据全部线索预测的目标词。
- $f$：待评估模型执行多点语义关联与证据整合的映射。

<div class="equation-explanation" markdown="1">

**直观理解**：该形式化强调输入不是一条待延伸的推理链，而是一组来自不同方向的线索。模型必须把每条线索提供的部分约束汇总起来，使预测$\hat{y}$与隐藏目标$y$一致；论文原文给出了$C$的集合定义和恢复$y$的任务要求，$f(C)$是对此输入输出关系的等价函数化表达。<br>
**原文位置**：Methodology，Task Definition

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。MPAR-Bench是基准构造与推理评测方法，原文没有提出需要训练的新模型、可优化损失函数或参数更新目标；Qwen3-Embedding-8B仅用于数据构造阶段的语义相似度过滤，受测模型则在既定提示下直接推理。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 分角度多智能体线索生成器**

生成过程维护已接受线索，并让不同LLM智能体在指定联想角度下迭代提出与目标词$y$相关的新线索；新候选必须尽量减少与既有线索的语义冗余。这一设计复现Just One中多个独立提示者提供互补信息的结构。

> 直观理解：如果所有提示者都想到同一件事，题目实际只测一个关联方向。让智能体承担不同角度，可以主动扩大线索覆盖的语义范围。

**2. 裁判与嵌入联合过滤器**

规则驱动的裁判智能体负责识别直接泄题、词法变体、重复概念和低质量线索，Qwen3-Embedding-8B则估计线索—答案与线索—线索的语义相似度。前者执行可解释的离散约束，后者补充难以通过字符串规则发现的语义近重复和关联强度异常。

> 直观理解：只用裁判模型可能漏掉措辞不同但含义相同的提示，只用向量阈值又难以可靠判断谐音、翻译等具体违规类型。两种过滤方式互补，目标是在“相关”与“不直接、不重复”之间取得平衡。

**3. 标准—增强双层评测协议**

标准设置使用完整且格式良好的线索测量基础推理广度；增强设置通过线索遮蔽、顺序打乱、干扰项注入和多步线索四种变换测量信息缺失、排列敏感性、抗噪性及远距离语义桥接能力。模型还需解释每条相关线索与预测答案$\hat{y}$的逻辑联系，以支持对推理轨迹的进一步核验。

> 直观理解：只看正常题答对率，无法知道模型是真的综合了所有线索，还是碰巧抓住某个强提示。四种扰动分别破坏不同条件，从而定位整合过程在哪一类变化下失效。

**训练与推理**

构造阶段先采样目标词$y$，再让多个线索智能体按指定语义角度迭代生成候选；裁判智能体依据Just One约束筛除泄题、重复及低质量线索，嵌入过滤器进一步控制线索—答案关联强度与线索间冗余，随后通过自动唯一性处理和人工抽检形成标准题。推理阶段把线索集合$C$放入Player Prompt，要求受测模型输出一个单词$\hat{y}$并解释各线索与该词的联系；同一评测框架再应用四类增强变换，通过正常条件与扰动条件间的表现差异衡量推理广度及其稳健性，不涉及对受测模型的微调。

**复现信息**

复现数据构造时，关键组件是用于语义过滤的Qwen3-Embedding-8B、取值范围为0.3至0.8的实验性嵌入相似度阈值，以及生成智能体、裁判智能体和Player Prompt之间的职责划分。英文与中文使用同一总体流水线并各保留500个验证条目；为公平解释增强结果，四类增强设置从标准任务中均匀分配词项。原文节选没有给出最终选定阈值、每题固定线索数、遮蔽比例、打乱随机种子、干扰项数量或多步线索的具体生成参数，因此这些细节不能由现有材料补全。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MPAR-Bench Standard：基准共含英汉双语的1,000个多点联想项目，每个项目要求模型根据若干独立生成、语义方向不同的线索恢复隐藏目标词。Standard设置用于测量未施加额外扰动时的基础联想检索与多线索整合能力。原文节选未明确报告英语与中文各自的项目数、训练/验证/测试划分；该基准用于评测而非训练。
- MPAR-Bench Enhanced：在同一任务框架上施加线索遮蔽、顺序打乱、干扰项注入和多步推断四种扰动，用于检验模型是否依赖个别强线索、线索位置、表面语义相关性或短联想路径。主表给出四种扰动汇总后的Enhanced结果，附录另按扰动类型分析准确率。
- 推理轨迹人工核验子集：从模型推理轨迹中随机抽取300条，由人工判断事实正确性与逻辑合理性，再与LLM评审结果比较。其作用是验证自动推理轨迹评审的可信度，而不是重新估计整个MPAR-Bench的答案准确率。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**精确匹配准确率（Acc）**

仅当预测字符串与标准答案完全一致时计为正确，直接衡量目标词恢复成功率。它标准严格且易解释，但会把语义合理、词形略有差异的答案全部记错。 （越高越好，因为更高表示更多项目准确恢复了指定目标词。）

</div>
<div class="metric-item" markdown="1">

**平均归一化Levenshtein相似度（ANLS）**

根据预测词与标准答案之间的归一化编辑距离计算字符层面的接近程度。它能识别拼写或词形上的近似答案，但字符相近不必然表示语义或推理正确。 （越高越好；取值越接近1，表示预测字符串与标准答案所需的插入、删除和替换越少。）

</div>
<div class="metric-item" markdown="1">

**推理轨迹有效性（Trace）**

从事实核验和逻辑核验两个维度检查模型如何把各条线索连接到预测答案。事实核验关注中间陈述是否真实，逻辑核验关注线索到答案的关联是否自然、直接，是否存在牵强解释、过度泛化或多层重释。 （越高越好，因为更高表示更多推理轨迹通过事实与逻辑审查；不过该指标依赖自动评审规则，不能替代最终答案准确率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 思考模式、Standard MPAR-Bench的跨模型比较

<div class="result-value" markdown="1">

作者报告Gemini-3.1pro在英语和中文准确率上均居首，分别达到86.8%和72.2%；英语中GPT-5.2和Sonnet-4.5随后。与此同时，表2显示Gemini-3.1pro的ANLS、词向量相似度和Trace分别为英语0.884、0.915、0.941，以及中文0.802、0.869、0.957。

</div>

这说明在无额外扰动的任务中，Gemini-3.1pro最能把多个语义方向汇合到目标词，而且优势不只体现在严格字符串匹配上。它并不证明该模型已经获得稳健的推理广度，因为Standard结果没有检验线索缺失、干扰项或联想链延长时的稳定性，也不能排除答案词频和预训练知识覆盖的影响。

<div class="result-source" markdown="1">

来源：Main Results, Model Comparisons；Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under the thinking mode, Gemini-3.1pro leads on both English (86.8%) and Chinese (72.2%), followed by GPT-5.2 and Sonnet-4.5 in English.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Standard与Enhanced设置的扰动稳健性比较

<div class="result-value" markdown="1">

作者指出，四类扰动会使各模型的准确率整体下降；摘要将降幅概括为英语9至18个百分点、中文5至12个百分点。附录进一步报告，线索遮蔽相对顺序打乱在英语上平均降低20.0%，而Qwen3-max和Seed-2-pro在干扰项注入下相对各自Standard准确率下降均超过28%。

</div>

结果表明模型常依赖可用强线索和表面语义相关性：删除线索会减少交叉约束，无关词则可能把搜索方向带偏。顺序打乱通常影响最小，说明多数模型并不严重依赖固定线索位置。这里的下降证明模型对这些特定扰动敏感，但不能单独确定失败来自注意力分配、知识不足还是答案生成阶段。

<div class="result-source" markdown="1">

来源：Abstract；Tables 3、5、11、12；Appendix E, Enhanced MPAR-Bench Result Analysis

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across evaluated models, perturbations reduce accuracy by 9-18 percentage points in English and 5-12 percentage points in Chinese.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 推理轨迹错误类型分析

<div class="result-value" markdown="1">

英语思考模式的Standard设置中，Deepseek-v3.2、Kimi-k2和Qwen3-max的逻辑错误率分别为43.60%、40.56%和38.21%，最佳模型Gemini-3.1pro仍为20.61%；对应的事实错误率则分别为13.60%、15.77%和11.52%。作者据此认为主要失败不是知识事实错误，而是从线索到答案的无效推断跳跃。

</div>

模型往往知道相关事实，却不能自然地把多条线索约束到同一具体概念；因此只增加知识或生成长度未必能解决问题。该结论依赖论文设定的自动轨迹审查标准，且错误率的表格列结构需要结合原文完整表头复核，不能把轨迹评审直接等同于人类对全部样本的判断。

<div class="result-source" markdown="1">

来源：Appendix E, Reasoning Trace Error Analysis；Table 13

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across all models, logical error rates substantially exceed factual error rates.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验主要依赖单词恢复任务及从公开词表抽取的答案空间，能够较干净地测量多点语义联想，但对开放式科学推理、规划或真实多文档证据整合的外部有效性仍不明确。节选也未给出语言子集规模、项目分布和完整划分，限制了对统计稳定性与英汉难度可比性的判断。
- 跨模式比较并非全部为同一模型、同一配置的严格配对：Gemini的思考与非思考表使用不同型号，Kimi-k2仅出现在思考表；推理轨迹指标还依赖LLM评审，尽管300条人工样本显示较高一致率。因而模型排名、模式增益及错误类型比例仍需结合完整附录、置信区间和更大规模人工核验进行源文复查。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 模型家族横向比较：实验覆盖GPT、Gemini、Sonnet、Qwen、Kimi、DeepSeek和Seed系列。代表性比较包括GPT-5.2、Gemini-3.1pro或Gemini-3flash、Sonnet-4.5以及Qwen3-max等，用来判断结果是否只属于单一供应商或模型架构；不同模式下部分Gemini型号不同，因此不能把所有跨模式差异都视为严格的同模型对照。
- 思考模式与非思考模式：对支持相应配置的模型比较显式扩展推理和直接作答。该对照用于区分增加推理深度是否同时改善多方向线索整合，但非思考表未包含Kimi-k2，且Gemini使用的具体型号不同，跨模型平均值应谨慎解释。
- Standard与Enhanced设置：将无额外扰动的标准任务作为稳健性基线，再与四类扰动后的结果比较。该对照直接测试模型在信息缺失、顺序变化、无关语义和更长联想链下是否仍能保持答案。
- Seed-2-pro原始思考提示与结构化三步提示：三步提示要求全面检查线索、优先选择具体概念并从候选答案反向验证线索。该对照隔离了显式推理策略提示的增益，用于判断性能瓶颈能否仅靠提示工程缓解。

**实验想回答的问题**

- 不同大语言模型在英汉双语多点联想推理中，能否综合多个彼此独立且语义多样的线索，准确恢复唯一目标词；模型的词面接近度、语义接近度和推理过程有效性是否与精确匹配结果一致？
- 显式思考模式以及线索遮蔽、顺序打乱、干扰项注入和多步线索四类扰动，会如何影响模型的推理广度；更长的推理过程是否真正提高跨线索整合的稳健性？

**实验实现**

实验在MPAR-Bench的英语与中文子集上，同时覆盖Standard和Enhanced设置，并分别报告思考与非思考模式。所有模型沿用各提供方官方默认采样参数；API支持时，推理模型设置$reasoning\_effort=high$，且不针对单个模型调参。除Acc、ANLS和Trace外，原文还用fastText余弦相似度报告词级语义接近度。推理轨迹评审先把解释拆成独立步骤，再分别进行Fact Check和Logic Check；逻辑评审会拒绝牵强的边缘含义、以宽泛上位概念替代更精确答案以及需要超过两层重释的关联。对随机抽取的300条轨迹，人工与LLM评审在事实核验和逻辑核验上的一致率分别为98.7%和94.7%。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Seed-2-pro思考模式、Standard设置：加入结构化三步推理提示 | 英语准确率从71.4%升至72.4%，增加1.0个百分点，ANLS从0.724升至0.734，词向量相似度从0.802升至0.807；中文准确率从64.6%升至67.8%，增加3.2个百分点，ANLS从0.739升至0.765，词向量相似度从0.820升至0.838。 | 该消融隔离了“全面查看线索、优先具体概念、反向验证”这一提示策略。中文取得较明显但仍有限的提升，英语增益很小，支持作者关于思考模型可能已经隐式执行部分步骤的解释；但实验只使用Seed-2-pro，因此不能证明所有模型或所有扰动条件下提示工程都只有有限作用。 | Appendix E, Structured Reasoning Skill Experiment<br><span class="experiment-evidence">On the English subset, accuracy rises marginally from 71.4% to 72.4% (+1.0pp), ANLS from 0.724 to 0.734, and embedding similarity from 0.802 to 0.807.</span> |
| 思考模式与非思考模式对照 | 作者报告思考模式会稳定提高英语中各模型的准确率，平均提升幅度也明显大于中文；中文效果依赖模型，Sonnet-4.5出现轻微回退，而且扰动条件下的改善并不单调。节选未给出作者所述跨模型平均提升的精确数值。 | 该对照检验增加显式推理计算是否同时改善多线索整合。结果显示思考主要提高标准任务表现，却没有一致降低扰动敏感性，因此推理更长不等于搜索语义方向更全面。由于Gemini在两种模式下使用不同型号，且非思考实验缺少Kimi-k2，这不是所有模型都完全受控的模式消融。 | Main Results, Thinking vs. Non-Thinking；Tables 2至5<br><span class="experiment-evidence">Comparing thinking-mode results (Tables 2, 3) against their non-thinking counterparts (Tables 4, 5), we find that thinking mode consistently improves most indicators, but the magnitude of the gain is markedly larger on English than on Chinese: averaged across models, thinking lifts English accuracy by a substantially wider margin and produces clear, stable gains for every model, whereas its effect on Chinese is much smaller and model-dependent (Sonnet-4.5 even shows a slight regression), and the improvement under perturbation is non-monotonic.</span> |

**定性案例**

- 作者在挑战案例和附录的定性分析中观察到“过度思考”：模型可能先提出正确候选，随后在重复自检、生成冗余候选或循环论证时推翻正确答案。Qwen3-max尤其表现出反复自我验证和循环 deliberation。该案例说明更长轨迹可能扩大搜索，也可能让后续弱关联覆盖早期强证据；它是机制线索而非总体因果证明。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces and validates a benchmark for measuring multi-point associative reasoning breadth in large language models.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`38dff2fa50776486103d1b5d04bf457a2c6aa720ddad55f7e05726dc339951cf`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
