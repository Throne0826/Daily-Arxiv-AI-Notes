---
title: "[论文解读] MathForm: Scaling Mathematical Autoformalization with Knowledge Retrieval and Verification-Guided Refinement"
description: "[arXiv 2608.14221][LLM Reasoning] MathForm将Mathlib知识检索、编译与语义反馈驱动的迭代修订组成闭环，旨在突破依赖参数记忆和单次生成筛选的数据构造上限，从而生成更可靠、更具领域多样性的自然语言到Lean 4形式化训练数据。"
arxiv_id: "2608.14221"
announcement_date: "2026-08-17"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-17T02:01:41.351940+00:00"
source_sha256: "c75a4dbd2b78e56e618e2778aadf6c142ef6ce55d9d76e9777ed935bdd065c04"
tags:
  - "LLM Reasoning"
  - "自动形式化"
  - "Lean 4"
  - "Mathlib"
  - "检索增强"
  - "机器可验证数学"
  - "语义一致性"
  - "形式化数据构造"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.14221</p>

# MathForm: Scaling Mathematical Autoformalization with Knowledge Retrieval and Verification-Guided Refinement

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-17</span>
<span><strong>作者</strong> Lushi Pu, Weiming Zhang, Xinheng Xie, Zixuan Fu, Bingxiang He, Hengyu Zhao, Hongya Lyu, Xin Li, Jie Zhou, Yudong Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: ModelBest Inc；Affiliation: Tsinghua University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.14221) · [PDF 下载](https://arxiv.org/pdf/2608.14221) · **关键词** 自动形式化, Lean 4, Mathlib, 检索增强, 机器可验证数学, 语义一致性, 形式化数据构造<br>


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

MathForm将Mathlib知识检索、编译与语义反馈驱动的迭代修订组成闭环，旨在突破依赖参数记忆和单次生成筛选的数据构造上限，从而生成更可靠、更具领域多样性的自然语言到Lean 4形式化训练数据。

**不用术语来说**：大量数学知识只以自然语言存在，若要供计算机检查或用于训练定理证明系统，就必须把它准确写成Lean 4代码；这不仅要求理解原命题，还要求选对Mathlib中的类型、定义和惯用表达。现有模型可能写出无法编译的代码，也可能生成表面合法但悄悄遗漏假设或改变条件的命题，因此仅靠一次生成再挑选结果，难以稳定处理复杂数学内容。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出MathForm数据构造框架：生成前从Mathlib检索相关定义和已有形式化，生成后利用编译器诊断与语义一致性判断定位问题，并通过迭代修订得到经过验证的Lean 4陈述。
- 利用该框架构建约36.7万条已验证样本的FormalVerse，并以监督微调和强化学习训练MathForm-8B，用于验证高质量、多领域形式化数据能否将闭环系统的能力压缩到模型的单次生成中。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

形式定理证明使用 Lean 4 等证明助理，把数学命题及其证明表示为可由机器检查的代码。当前高性能证明系统的进一步扩展受制于形式化语料稀缺：大量数学知识仍以自然语言存在，而人工录入不仅要求准确理解数学含义，还要求熟悉 Lean 4 的类型系统以及 Mathlib 中的定义、记号、结构和惯用表达。自动形式化因此承担连接自然语言数学资源与机器可验证语料的任务，但“能够编译”并不等于“忠实表达原命题”：生成代码即使类型正确，也可能遗漏关键假设、强化条件，或选用不符合原意的 Mathlib 概念。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自动形式化（autoformalization）**

将自然语言数学陈述转换为 Lean 4 等形式语言代码，使其能够接受证明助理的机器检查。本文关注的核心不只是语法转换，还包括对源命题数学语义的忠实保持。

</div>
<div class="concept-item" markdown="1">

**Lean 4 与 Mathlib**

Lean 4 是依赖类型理论驱动的编程语言和证明助理，编译器可检查形式陈述是否满足语法与类型约束；Mathlib 是其主要数学库，提供数学对象、定义、记号、定理和常用形式化模式。正确形式化往往必须把自然语言概念映射到 Mathlib 特定且可能层次复杂的类型与定义。

</div>
<div class="concept-item" markdown="1">

**参数记忆与检索增强**

参数记忆指模型在训练后固化于权重中的知识；仅依赖它时，模型可能误用 Mathlib 定义或调用不存在的引理。检索增强则在生成前从 Mathlib 获取相关定义和已有形式化示例，为当前转换提供可核对的外部知识。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一条自然语言数学陈述，系统需要输出表达同一命题的 Lean 4 形式陈述，并在 Mathlib 环境中接受机器验证。任务包含两层要求：其一是句法和类型层面的有效性，即输出能够通过 Lean 编译检查；其二是语义一致性，即形式陈述不得丢失假设、擅自加强或削弱条件，也不得因错误映射数学对象而改变原命题。本文所处的设置还包括大规模训练数据构造：系统需利用 Mathlib 知识、编译器诊断和语义反馈反复修订候选结果，得到经验证的自然语言—Lean 4 配对数据，随后用于训练可进行单次自动形式化生成的模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$N$**

Best-of-$N$ 策略中针对同一输入采样的候选形式化数量。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{Pass@}8$**

对同一问题生成八个候选时，至少有一个候选通过指定检查的评估指标。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{SC}$**

Syntax Check，即检查生成的 Lean 4 陈述能否满足语法及编译约束。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{CC}$**

Consistency Check，即检查生成形式陈述与自然语言源命题是否保持语义一致。

</div>

</div>

**直接相关的工作**

- **TheoremLlama、Herald、Kimina-Autoformalizer 与 Mathesis**: 这些工作训练端到端的自然语言到形式语言自动形式化模型，构成本文直接面对的生成范式；本文指出，此类方法主要依靠模型参数记忆中的数学和编程知识，难以完整掌握持续演化且高度专门化的 Mathlib 定义体系。
- **RAutoformalizer、DRIFT 与 Aria**: 这些工作同样探索检索增强的自动形式化，但原文认为其重点主要是推理阶段对单个实例的形式化，而非面向大规模、端到端训练数据构造；MathForm 所填补的空缺是把知识检索、自动验证和反馈驱动修订组织成数据生产闭环。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

形式化定理证明系统要继续扩展，需要大量且多样的机器可检查陈述与证明，但现有语料稀缺，而人工把自然语言数学编码为Lean 4既要精确理解数学含义，也要熟悉证明助手和Mathlib。自动形式化可以扩大数据供给，不过训练数据只有在代码可编译且语义忠于原命题时才真正有用；若形式化结果强化条件、遗漏关键假设或选错数学结构，即使能够通过语法检查，也会污染训练数据并削弱下游证明系统。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **依赖模型参数记忆的单次自动形式化**：模型根据训练期间内化的数学知识、Lean语法和库知识，直接把自然语言命题一次性生成为Lean 4陈述，生成前没有针对当前问题系统查询Mathlib。
- **Best-of-$N$候选采样与事后筛选**：模型对同一命题独立采样多个单次生成候选，再由判别器对完整候选作接受或拒绝判断，最终保留其中通过检查或得分较高的结果。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 参数记忆难以完整、及时地覆盖Mathlib不断演化的定义层级、类型系统、记号、结构和惯用形式化模式，因而模型容易误用已有定义、调用不存在的引理，或生成虽然合法却偏离库惯例的表达；这一问题在抽象代数等依赖深层库知识的领域尤其突出。
- Best-of-$N$只能从模型已有的单次输出分布中挑选候选，判别器的整体接受或拒绝也不能指出语义偏差发生在哪里以及如何修复。因此，数据难度受模型当前单次生成能力限制，复杂前提和高级数学领域持续代表不足；同时，仅能编译的候选仍可能改变原命题含义。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少一种可规模化的数据构造机制，能够同时补充当前问题所需的Mathlib专门知识、区分编译错误与语义失真、把诊断转化为局部修订，并通过多轮验证处理单次生成无法解决的命题。换言之，尚未解决的缺口不是如何增加候选数量，而是如何让候选在外部知识与可操作反馈的支持下逐步收敛到既可编译又忠实于原文的形式化结果，并由此扩展训练数据的领域和难度。

</div>
<div markdown="1"><span>核心问题</span>

能否把Mathlib知识检索、编译检查、语义一致性判断和迭代修订组织为一个闭环，使数据构造能力不再受限于模型的参数记忆与单次生成上限，并进一步用这些验证数据训练出可在单次推理中完成高质量自然语言到Lean 4转换的紧凑模型？

</div>
<div markdown="1"><span>作者直觉</span>

自动形式化更像是查阅技术手册后反复调试程序，而不是逐句翻译：检索先把当前命题可能需要的Mathlib定义、类型和既有写法放到模型面前，降低凭记忆猜测库接口的负担；编译器反馈负责暴露类型、名称和语法问题，语义反馈负责发现遗漏假设或改变命题等“能编译但意思不对”的问题。模型据此修改已有候选，便可保留正确部分并针对错误继续推进，而不必每次从头随机采样；最终再用这些修订轨迹和验证样本训练模型，有望把检索与多轮修订产生的能力沉淀到单次生成中。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MathForm 的方法由“构造高质量监督数据”和“训练专用自动形式化模型”两部分组成。数据侧以自然语言数学命题为输入，先规范化题面，再由检索规划器判断是否需要 Mathlib 知识并通过 LeanExplore 棘索相关定义、定理和记号；形式化生成器据此产生只包含定理陈述的 Lean 4 代码。候选代码依次接受格式检查、Lean 4 编译检查和语义一致性检查，失败样本携带诊断反馈进入下一轮，最多迭代三轮。通过双重验证的自然语言—形式语言对会被重建为简洁的形式化推理轨迹，并与评测集去污染，最终形成约 367K 对数据的 FormalVerse。

模型侧以 Qwen3-8B 为基座，先在 FormalVerse 上进行监督微调，得到 MathForm-8B-SFT；随后从数据构造阶段始终未通过验证的问题中筛选 3,000 个难度适中且语义无歧义的样本，用 DAPO 强化学习继续优化。奖励只在生成结果既能编译、又忠实表达原命题时取 $1$，否则取 $0$。直观地说，整个系统先借助数学库和两道质量关生产“题意正确且机器可读”的教材，再让模型模仿这些教材，最后针对仍容易出错的问题，通过可执行验证和语义判断继续纠偏。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 问题收集、规范化与候选筛选

过滤非数学内容、纯数值计算题和不适合自然表达为定理陈述的问题，并改写多余的答案格式要求或无关上下文，使每个样本成为语义相对独立、可形式化的自然语言命题。

<div class="method-step__io" markdown="1">

**输入**：来自 DeepTheorem、NuminaMath、AceReason-Math、Lean Workbook、Principia-Collection、DeepMath、OpenR1-Math，以及经典数学教材的自然语言题目和定理。<br>
**输出**：规范化的自然语言数学问题池，作为后续知识检索和 Lean 4 形式化的统一输入。

</div>

**直观理解**：这一步类似先整理题库：去掉只要求算出一个数或夹杂答题说明的内容，把剩余题目改写成明确的“在什么条件下，要断言什么结论”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按需检索 Mathlib 并生成形式陈述

由 gpt-oss-120b 驱动的检索规划器分析命题中的数学对象、关系和类型约束，判断是否需要外部库知识；若需要，则围绕关键概念发出少量定向查询，每个查询由 LeanExplore 返回前 $22$ 个结果。形式化生成器联合原命题与检索到的定义、定理、记号和既有形式化，选择对应的 Mathlib 类型与定义并生成 Lean 4 定理陈述。

<div class="method-step__io" markdown="1">

**输入**：一个规范化自然语言命题，以及可查询 Mathlib 内容的 LeanExplore 检索接口。<br>
**输出**：候选 Lean 4 形式化及其检索上下文；输出目标仅是形式陈述，不包含证明步骤或解题过程。

</div>

**直观理解**：检索规划器先判断模型是否需要“查数学库字典”，再只查真正相关的概念；生成器据此使用 Mathlib 已有的标准表达，而不是仅凭模型记忆猜测名称和类型。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 验证引导的迭代修正

系统先用格式检查剔除证明、策略和求解过程，再用 Lean 4 编译器检查语法、标识符、依赖和类型；可编译结果继续由 QwQ-32B 判断其是否忠实保留原命题的假设、量词、对象和结论。任一检查失败时，反馈被送回生成器，并在缺少库知识时重新触发检索；每个样本最多尝试三轮，通过两项检查即提前停止，否则丢弃。

<div class="method-step__io" markdown="1">

**输入**：自然语言命题、检索上下文、当前候选 Lean 4 陈述，以及前一轮可能产生的编译诊断或语义反馈。<br>
**输出**：同时满足可编译性和语义一致性的自然语言—Lean 4 配对，以及被淘汰的未解决样本集合。

</div>

**直观理解**：编译器负责判断代码“能不能被 Lean 理解”，语义裁判负责判断“Lean 理解的是否还是原题”；失败原因直接用于下一次修改，所以额外计算集中在尚未解决的样本上。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 轨迹重建、去污染与监督微调

系统不直接保留混杂检索内容、失败尝试和冗长思考的原始轨迹，而是根据最终命题对回溯合成结构化的形式化分析，明确排除证明策略、策略命令选择和解题过程。随后删除与任一评测样本共享至少一个 $13$-gram 的训练样本，得到 FormalVerse，并用其监督微调 Qwen3-8B。

<div class="method-step__io" markdown="1">

**输入**：验证通过的自然语言—Lean 4 配对、其原始多轮生成记录，以及全部评测基准样本。<br>
**输出**：约 367K 个由自然语言命题、重建形式化轨迹和已验证 Lean 4 代码组成的 FormalVerse 样本，以及 MathForm-8B-SFT。

</div>

**直观理解**：系统把曲折的试错记录改写成一条适合学习的“从题意分析到形式陈述”的清晰路线，并删除可能泄露测试题的样本；监督微调让模型先学会稳定识别对象、逻辑结构、变量依赖和隐含类型。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### DAPO 词元级裁剪目标

$$
J_{\mathrm{DAPO}}(\theta)=\mathbb{E}\Bigg[\frac{1}{\sum_{i=1}^{G}|y_i|}\sum_{i=1}^{G}\sum_{t=1}^{|y_i|}\min\Big(\rho_{i,t}A_i,\;\operatorname{clip}(\rho_{i,t},1-\epsilon_{\mathrm{low}},1+\epsilon_{\mathrm{high}})A_i\Big)\Bigg]
$$

**符号说明**

- $J_{\mathrm{DAPO}}(\theta)$：参数为 θ 的当前策略所最大化的 DAPO 训练目标。
- $x$：输入的自然语言数学命题。
- $G$：针对同一输入采样的候选形式化数量；实现中每个提示采样 8 个 rollout。
- $y_i$：第 i 个候选 Lean 4 形式化序列，|$y_i|$ 是其词元长度。
- $\rho_{i,t}$：第 i 个候选在第 t 个词元处，当前策略相对于旧策略的概率比。
- $A_i$：第 i 个候选依据同组奖励计算的组归一化优势，用来表示其相对同组候选的好坏。
- $\epsilon_{\mathrm{low}},\epsilon_{\mathrm{high}}$：策略比的下侧和上侧裁剪幅度；实现中的比率边界为 0.8 和 1.28，对应非对称的 Clip-Higher 设置。
- $\theta$：待优化的 MathForm 策略模型参数。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标提高高优势候选中各词元的生成概率，降低低优势候选的概率，同时用裁剪限制单次更新相对旧策略变化过大。分母按组内全部输出词元归一化，使不同候选长度下的词元贡献可比较；上侧裁剪范围更宽，则允许成功候选获得更充分的正向更新。<br>
**原文位置**：第 3.2.3 节，公式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 编译与语义联合二元奖励

$$
r(x,y)=\begin{cases}1,&C(y)=1\ \text{and}\ S(x,y)=1,\\0,&\text{otherwise}.\end{cases}
$$

**符号说明**

- $r(x,y)$：自然语言命题 x 与候选形式化 y 对应的强化学习奖励。
- $C(y)$：Lean 4 编译成功指示函数；候选 y 编译成功时取 1，否则取 0。
- $S(x,y)$：语义一致性指示函数；对可编译候选，由 gpt-oss-20b 判断 y 忠实表达 x 时取 1，否则取 0。
- $x$：自然语言数学命题。
- $y$：模型生成的候选 Lean 4 形式陈述。

<div class="equation-explanation" markdown="1">

**直观理解**：奖励采用逻辑“与”：只有代码可以通过 Lean 编译且没有改变原题语义，候选才算成功。这样不会奖励仅语法正确但漏条件、改量词或写错结论的形式化，也不会奖励语义看似合理但无法被 Lean 接受的文本。<br>
**原文位置**：第 3.2.3 节，公式 (2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：监督阶段采用教师给定目标，在 FormalVerse 上训练模型根据自然语言命题及重建轨迹生成已验证的 Lean 4 陈述，其作用是建立对象识别、逻辑结构解析、变量依赖分析、隐含类型推断和 Mathlib 表达映射等基础能力。强化学习阶段进一步最大化 $J_{\mathrm{DAPO}}(\theta)$：每个问题由旧策略 $\pi_{\theta_{\mathrm{old}}}$ 采样一组候选，用联合奖励 $r(x,y)$ 区分同时通过编译和语义检查的结果与失败结果，再将组内相对表现转化为优势 $A_i$。动态采样仅保留同时含正、负候选的组，因为全成功或全失败组无法提供有效的组内排序信号；Clip-Higher 和裁剪机制则控制策略更新幅度。因而，SFT 负责从大规模干净示例中学习一般翻译能力，DAPO 负责在困难样本上直接对齐最终验收条件。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 检索规划器与形式化生成器**

两者均由 gpt-oss-120b 驱动，但职责分离：规划器从命题中提取数学对象、关系及类型需求，决定是否调用 LeanExplore；生成器在原命题和检索结果条件下，将自然语言对象映射到 Mathlib 的类型、定义和记号，再输出 Lean 4 陈述。按需检索避免每道题都附加大量无关上下文，也降低对模型参数记忆中库接口名称的依赖。

> 直观理解：规划器负责决定“要查什么、是否值得查”，生成器负责“怎样用查到的标准组件写出代码”。这种分工主要解决 Mathlib 名称、类型和规范表示难以仅靠记忆准确复现的问题。

**2. 编译与语义双重验证器**

格式检查首先约束输出边界；Lean 4 编译器随后提供确定性的语法、名称解析、依赖和类型检查。对可编译候选，QwQ-32B 在数据构造阶段判断其与自然语言命题的语义一致性，重点识别遗漏假设、条件强化或弱化、量词顺序错误、额外约束、对象类型不当及结论错配；强化学习阶段则使用推理更快的 gpt-oss-20b 产生语义奖励判断。

> 直观理解：可编译并不等于题意正确，例如漏掉一个假设后代码仍可能合法。因此必须把“代码是否合法”和“表达是否忠实”拆成两道关卡，并将具体失败原因反馈给生成器。

**3. 轨迹重建器**

该模块以最终验证通过的自然语言命题和 Lean 4 陈述为端点，重新合成二者之间的结构化分析，包括对象识别、逻辑结构、类型约束与语法映射，但明确禁止加入证明方案、Lean tactic 或实际求解步骤。重建后的训练目标统一为“自然语言命题—形式化分析轨迹—Lean 4 陈述”，不再包含多轮失败输出和交错的工具反馈。

> 直观理解：原始试错日志噪声很大，也容易诱导模型去证明题目而不是翻译题目。重建器保留完成形式化真正需要的分析，同时把无关的证明冲动和重复尝试清除。

**训练与推理**

完整训练流程如下：首先运行自动形式化框架，经过最多三轮的按需检索、生成、编译和语义修正，收集通过验证的配对；之后重建只面向形式化的分析轨迹并执行基于 $13$-gram 重叠的评测集去污染，形成 FormalVerse。以 Qwen3-8B 初始化，在 FormalVerse 上进行三轮监督微调，得到 MathForm-8B-SFT。再从始终未通过构造验证的约 20,000 个问题中实施离线难度过滤和歧义过滤，保留 3,000 个问题；每个提示采样 $8$ 个候选，使用 Lean 编译结果与 gpt-oss-20b 语义判断形成二元奖励，通过 DAPO 更新模型，且只训练奖励组内同时出现成功与失败结果的样本。

数据构造阶段的推理是一条带外部工具的闭环：自然语言命题先经检索规划，必要时查询 LeanExplore，然后生成候选、执行格式检查和 Lean 4 编译，再执行语义一致性判断；失败时携带反馈继续生成，最多三轮。训练完成后的 MathForm-8B 本身则是自然语言到 Lean 4 的生成模型：输入数学命题，模型分析对象、假设、量词、变量依赖和类型约束，输出对应的 Lean 4 形式陈述。原文没有说明部署时必须继续调用检索器或外部语义裁判，因此不能将数据构造框架中的检索与多轮验证视为最终模型推理的强制组成部分。

**复现信息**

为公平复现，关键环境是 Lean 4.21.0，SFT 与 RL 均使用 16 张 NVIDIA H100 80GB GPU。SFT 基于 LLaMA-Factory：最大序列长度为 $16{,}384$，全局批大小 $128$，学习率 $2.0\times10^{-5}$，训练 $3$ 个 epoch，使用 cosine 学习率调度、$0.1$ 预热比例和 bf16 精度。RL 基于 verl 实现 DAPO：学习率 $1.0\times10^{-6}$，策略比裁剪边界为 $0.8/1.28$，训练批大小与 PPO mini-batch 均为 $32$，每张 GPU 的 PPO micro-batch 为 $2$，每个提示生成 $8$ 个 rollout，采样温度为 $1.0$，最大响应长度为 $8{,}192$，不启用 KL 正则。

影响方法解释的模型分工也需保留：数据构造中的检索规划与形式化生成使用 gpt-oss-120b，语义验收使用不同模型家族的 QwQ-32B，以降低生成器和裁判同源造成的自偏好；强化学习奖励改用更小、更快的 gpt-oss-20b。LeanExplore 每次定向查询返回前 $22$ 个结果，每个数据构造样本最多细化三轮。上述裁判均参与数据或奖励生产，二元语义标签不是由 Lean 内核自动证明，因此最终数据质量仍依赖模型裁判的可靠性。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- FormalMATH-Lite（40 个样本）：用于评测较成熟的数学形式化任务，主要检验基础场景下的总体可编译性与语义一致性。
- DeepSeek-ProverBench（ProverBench，26 个样本）和 CombiBench（17 个样本）：分别覆盖定理证明相关数学与组合学，用于检验模型在不同数学类型中的迁移能力。
- FATE-M、FATE-H 和 FATE-X（各 14 个样本）：覆盖从初等抽象代数到高级交换代数、同调代数和代数几何基础的递增抽象层次，用于检验模型对 Mathlib 类型层次和已有形式化知识的利用能力；原文未明确报告各数据集的训练集、验证集和测试集划分，实验表中使用的是这些基准的评测样本。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Syntax Check（SC）下的 $\mathrm{Pass}@8$**

对每个自然语言陈述生成 $k=8$ 个候选 Lean 形式化，只要至少一个候选成功编译，实例指标就为 1；因此它主要衡量语法、类型和编译层面的可用性。 （越高越好，因为更高表示更多测试陈述至少能得到一个可被 Lean 4 后端接受的候选。）

</div>
<div class="metric-item" markdown="1">

**Consistency Check（CC）下的 $\mathrm{Pass}@8$**

对 $8$ 个候选逐一检查：候选必须先通过编译，再由语义一致性判定器确认其与原自然语言陈述一致；实例只要有一个候选同时满足两项即通过。 （越高越好；相较 SC，CC 还要求形式化没有改变、遗漏或额外加入原陈述的数学含义，因此更接近语义保真度。）

</div>
<div class="metric-item" markdown="1">

**人工评估的 SC 和 CC 通过率**

在 FATE-M 和 FATE-H 中，每个模型每道题从 $8$ 个候选中随机抽取一个，由两名数学专家判断其是否忠实保留原陈述语义；分歧通过讨论解决。SC 和 CC 分别报告编译与人工语义判断结果。 （越高越好；它用于检验自动语义判定器得出的模型排序能否在人类专家判断下复现。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 专用自动形式化模型的六基准总体比较，表 1 的 AVG

<div class="result-value" markdown="1">

MathForm-8B 的 AVG 为 SC 88.06%、CC 72.37%，均高于最强专用基线 ReForm-32B 的 81.61% 和 68.41%，绝对提升分别为 6.45 和 3.96 个百分点。

</div>

在相同的 $\mathrm{Pass}@8$ 评测协议下，较小的 $8$B MathForm 在“至少生成一个可编译候选”和“至少生成一个语义正确候选”两个层面都超过了 $32$B 专用模型。这说明模型规模并不是唯一决定因素，但该结果只证明了所选六个基准和采样设置下的优势，不能单独证明在所有数学领域或其他解码预算下都占优。

<div class="result-source" markdown="1">

来源：第 4.2.1 节；表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 1, MathForm-8B achieves the best average SC and CC pass rates among specialized autoformalizers, reaching 88.06% and 72.37%, respectively. Compared with the strongest specialized baseline, ReForm-32B (81.61/68.41), these results represent absolute gains of 6.45 and 3.96 percentage points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### FATE 系列中随抽象层次增加的语义一致性比较

<div class="result-value" markdown="1">

MathForm-8B 在 FATE-M、FATE-H、FATE-X 上的 CC 分别为 97.33%、63.00%、37.00%，较各子集上的最强专用基线分别高 6、10、12 个百分点；差距随抽象层次提升而扩大。

</div>

模型优势主要出现在高级代数形式化，而不是较成熟、较容易的 FormalMATH-Lite 和 ProverBench。该模式与论文关于检索 Mathlib 知识并进行验证引导迭代修正的解释相符，但“相符”是分析性解释，不是仅凭分数就能建立的因果证明；FATE-X 样本量也较小，因此差距仍需更大规模测试确认。

<div class="result-source" markdown="1">

来源：第 4.2.2 节；表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MathForm-8B attains CC pass rates of 97.33%, 63.00%, and 37.00% on FATE-M, FATE-H, and FATE-X, exceeding the strongest specialized baseline on each subset by 6, 10, and 12 percentage points, with the advantage widening as the abstraction level increases.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 与通用大语言模型的比较及人工语义评估

<div class="result-value" markdown="1">

MathForm-8B 的平均 SC 为 88.06%，超过表 7 中最强通用模型 Qwen3.7-Plus 的 86.33%；但平均 CC 为 72.37%，低于 Qwen3.7-Plus 的 83.38% 和 DeepSeek-V4-Pro 的 76.54%。在人工评估中，MathForm-8B 在 FATE-M 的 SC/CC 为 86.67%/76.67%，在 FATE-H 为 54.00%/42.00%，四项均为比较模型最高。

</div>

任务专用训练显著提升了 $8$B 模型生成可编译 Lean 代码的能力，但通用前沿模型在语义保真度上仍然更强，体现出“可编译”与“表达原意”不是同一个目标。人工评估与自动评估保持相同排序，增强了结论的可信度；不过人工实验每道题只随机抽取一个候选，而自动指标取 $8$ 个候选中的最好结果，两者并非完全同一测量条件。

<div class="result-source" markdown="1">

来源：附录 B.1；表 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MathForm-8B attains an average SC pass rate of 88.06%, exceeding all evaluated general-purpose models, including the strongest, Qwen3.7-Plus (86.33%); however, its average CC pass rate (72.37%) remains below Qwen3.7-Plus (83.38%) and DeepSeek-V4-Pro (76.54%).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- FATE-M、FATE-H 和 FATE-X 每个仅有 14 个样本，且原文未明确报告训练、验证和测试划分；在小规模、高难度子集上，若干百分点差异可能对样本组成敏感，泛化范围需要更大规模数据验证。
- CC 主要依赖 gpt-oss-120b 的 LLM-as-a-Judge 自动判定，尽管附录人工评估支持总体排序，但人工评估只对 FATE-M 和 FATE-H 各抽取一个候选，且表 4 的多判定模型稳健性数值在所给章节中未报告；因此复杂语义错误仍可能被自动指标遗漏。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- ReForm-32B：最强的专用自动形式化基线之一，且参数量为 32B，用于直接检验 $8$B 模型能否超过更大规模的任务专用模型。
- Goedel-Formalizer-V2-32B：另一种 $32$B 专用自动形式化模型，用于比较不同任务专用训练策略在复杂代数形式化上的效果。
- StepFun-Formalizer-32B：覆盖 $32$B 参数规模的专用模型，用于检验 MathForm 的优势是否只是来自参数规模，而非训练和验证设计。
- Qwen3.7-Plus 与 DeepSeek-V4-Pro：通用大语言模型，分别代表较强的通用推理系统，用于衡量任务专用训练在可编译性上的优势，以及通用模型在语义保真度上的潜在优势；其余专用和通用模型结果分别见表 1 和附录表 7。

**实验想回答的问题**

- 在六个涵盖竞赛数学、组合学及高抽象代数的基准上，$\mathrm{MathForm}$-8B 的语法可编译性和语义一致性是否超过现有专用自动形式化模型，包括更大参数规模的模型？
- 知识检索、验证引导的迭代 refinement 和强化学习是否尤其有助于处理高抽象层次的数学陈述，并且自动评测结果是否与人工语义评估一致？

**实验实现**

测试时对每个陈述采样 $k=8$ 个候选，温度设为 $0.6$。编译验证使用 Kimina Lean Server 作为 Lean 4 后端；语义一致性使用 LLM-as-a-Judge 协议，由 gpt-oss-120b 在 high reasoning-effort 设置下进行二元判断。对源陈述 $x$ 和候选形式化 $y_i$，$C(y_i)$ 表示候选是否成功编译，$S(x,y_i)$ 表示其是否与源陈述语义一致；原文定义 $\operatorname{SC@k}(x)=\max_{1\leq i\leq k}C(y_i)$，以及 $\operatorname{CC@k}(x)=\max_{1\leq i\leq k}C(y_i)S(x,y_i)$。最终分数是在全部测试实例上取平均，并以六个基准的等权宏平均报告 AVG。实验还通过多种判定模型进行额外稳健性分析，但所给章节未提供表 4 的具体数值。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| MathForm-8B-SFT 与 MathForm-8B 的强化学习阶段对比 | 从仅监督微调的 MathForm-8B-SFT 到加入强化学习的 MathForm-8B，AVG SC 从 84.38% 提升到 88.06%，AVG CC 从 66.53% 提升到 72.37%；SC 增加 3.68 个百分点，CC 增加 5.84 个百分点。 | 该对比主要隔离强化学习阶段的总体贡献：两项指标都上升，而 CC 增幅更大，说明验证相关奖励可能特别有助于语义对齐，而不只是修复 Lean 语法。不过这不是对单个知识检索模块或单次迭代修正模块的独立消融，不能据此分别归因于某一组件。 | 第 4.2.1 节；表 1<br><span class="experiment-evidence">Part of this margin comes from the RL stage: relative to MathForm-8B-SFT, reinforcement learning raises the average SC pass rate from 84.38% to 88.06% and the average CC pass rate from 66.53% to 72.37%.</span> |
| 不同参数规模的专用模型比较 | 在表 1 的 AVG 中，MathForm-8B 的 SC/CC 为 88.06%/72.37%，高于 ReForm-32B 的 81.61%/68.41%；在 MathForm 自身的 8B-SFT 对照中，强化学习后的 8B 也达到更高分数。原文未提供完整的逐组件消融表。 | 这个比较测试的是方法设计能否抵消参数规模差异，而不是严格意义上的单变量消融，因为不同模型还可能有不同数据、架构和训练流程。结果支持“有效训练和验证机制比单纯扩大模型更重要”的作者主张，但不能量化知识检索、验证引导 refinement 与强化学习各自的独立贡献。 | 第 4.2.1 节；表 1<br><span class="experiment-evidence">Compared with the strongest specialized baseline, ReForm-32B (81.61/68.41), these results represent absolute gains of 6.45 and 3.96 percentage points.</span> |

**定性案例**

- 论文称附录 C.2 提供了一个代表性案例，说明知识检索和验证引导的迭代修正如何帮助形式化高级代数陈述；所给章节没有包含该案例的完整自然语言陈述、检索内容、候选演化过程或最终 Lean 代码，因此只能确认作者提供了定性案例，不能进一步核验具体修正步骤或其独立贡献。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper advances mathematical autoformalization through retrieval and verification-guided iterative reasoning.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`c75a4dbd2b78e56e618e2778aadf6c142ef6ce55d9d76e9777ed935bdd065c04`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
