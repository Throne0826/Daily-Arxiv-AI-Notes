---
title: "[论文解读] ExeCRE: Execution-Consistency Guided Reliability Estimation for Self-Correcting Code Generation"
description: "[arXiv 2608.04439][LLM Reasoning] ExeCRE通过比较多个候选程序在大量、多样化构造输入上的执行输出一致性，统计估计参考代码的可信度，并据此减少不可靠验证信号对代码自纠错过程的干扰。"
arxiv_id: "2608.04439"
announcement_date: "2026-08-06"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:59:22.657009+00:00"
source_sha256: "d214b7e4d45210dbd1a998e611b517f25a04ca61043141c9098bce53c85eb614"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型代码生成"
  - "执行引导自纠正"
  - "执行一致性"
  - "代码可靠性估计"
  - "Dawid–Skene模型"
  - "不可靠反馈过滤"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.04439</p>

# ExeCRE: Execution-Consistency Guided Reliability Estimation for Self-Correcting Code Generation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Yiru Dong, Richong Zhang, Fanshuang Kong, Si Chen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Beihang University Beijing China；Beihang University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04439v1) · [PDF 下载](https://arxiv.org/pdf/2608.04439v1) · **关键词** 大语言模型代码生成, 执行引导自纠正, 执行一致性, 代码可靠性估计, Dawid–Skene模型, 不可靠反馈过滤<br>


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

ExeCRE通过比较多个候选程序在大量、多样化构造输入上的执行输出一致性，统计估计参考代码的可信度，并据此减少不可靠验证信号对代码自纠错过程的干扰。

**不用术语来说**：代码生成模型通常会运行一些参考程序来判断当前答案是否需要修改，但这些参考程序也是模型生成的，可能含有隐蔽错误或只适用于部分情况。若把它们的输出直接当作正确答案，本来正确的代码可能被错误修改，错误代码也可能因错误反馈而得到强化，因此系统需要先判断哪些参考程序值得信任。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出ExeCRE，将参考代码可靠性作为执行引导自纠错中的独立估计问题：不预设参考代码正确，也不直接依赖语言模型裁判或少量生成测试，而是利用候选代码在大规模构造输入上的执行行为估计其可信度。
- 将可靠性估计信号用于筛选自纠错所依赖的参考代码；作者声称该设计能够减少误导性监督，使迭代纠错更有效、更稳定，并通过代码生成实验及GSM8K上的小规模附加研究考察其适用性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型代码生成与执行引导自纠正领域。面对需要复杂算法或实现细节的编程题，模型初次生成的代码可能有误，因此常通过“生成候选代码、执行测试、依据反馈修改代码”的循环提高正确率；其中，验证信号是否可信直接决定修改方向。现有流程会让模型生成参考代码，再用该代码产生测试预期输出，但参考代码自身也可能含有隐蔽错误或只适用于部分输入。ExeCRE关注的不是形式化证明程序对所有输入均正确，而是在没有可信标准答案的条件下，根据多个候选程序在大量构造输入上的输出一致性，估计每段参考代码是否足够可靠，进而决定能否将它用于后续自纠正。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**执行引导的自纠正**

先运行模型生成的代码，再把测试结果、报错或执行轨迹作为反馈，让模型迭代修改答案。其有效性依赖验证信号的可靠性：错误的参考输出可能促使模型破坏原本正确的程序，或保留错误程序。

</div>
<div class="concept-item" markdown="1">

**执行一致性**

对同一问题的多段候选代码输入相同的构造数据，比较它们的运行输出是否呈现稳定的一致或分歧模式。本文将这种跨输入、跨候选程序的行为关系作为可靠性证据，而不把多数输出直接等同于真实答案。

</div>
<div class="concept-item" markdown="1">

**Dawid–Skene模型**

这是一种用期望最大化方法聚合含噪标注的统计模型，可同时推断样本的潜在真实标签和不同标注者的错误倾向。在本文的对应关系中，执行输入相当于待标注样本，候选代码相当于标注者，由执行一致性导出的信号相当于观测标注。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个编程问题实例$P$，系统收集解决同一问题的候选代码集合$C_P$，并构造执行输入集合$I_P$。每个候选代码$C_j$在每个输入$I_i$上运行并产生输出$O_{ij}$，所有结果组成执行矩阵$O$；系统在缺少可信测试预言或标准实现的设定下分析其中的一致性模式，为每个候选代码输出可靠性分数$\alpha_j\in[0,1]$。该分数表示代码是否适合作为后续测试生成和自纠正的参考，而不是对其完整语义正确性的形式化保证；达到阈值的候选代码才可进入后续纠正流程，否则不加入由其生成的参考测试。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$P$**

一个待求解的编程问题实例。

</div>
<div class="notation-item" markdown="1">

**$C_P=\{C_1,C_2,\dots,C_{|C_P|}\}$**

针对问题$P$生成的候选代码集合，其中$C_j$是第$j$段候选代码。

</div>
<div class="notation-item" markdown="1">

**$I_P=\{I_1,I_2,\dots,I_{|I_P|}\}$**

为问题$P$构造的执行输入集合，其中$I_i$是第$i$个输入。

</div>
<div class="notation-item" markdown="1">

**$O=[O_{ij}],\quad \alpha_j\in[0,1]$**

$O$是执行输出矩阵，$O_{ij}$表示$C_j$在$I_i$上的输出；$\alpha_j$是候选代码$C_j$的估计可靠性分数。

</div>

</div>

**直接相关的工作**

- **ALGO**: ALGO使用模型生成的暴力参考代码构造测试，并将其用于代码选择或纠正；但这类流程通常默认参考代码足够正确。ExeCRE针对其上游风险，在参考代码生成的测试进入纠正循环之前显式估计并过滤参考代码的可靠性。
- **Dawid–Skene模型**: 经典Dawid–Skene模型从多个含噪标注者的观测中联合推断潜在标签和标注者错误率。ExeCRE借用这一统计视角，把候选代码视为标注者、执行输入视为样本，并以执行一致性信号估计各候选代码的潜在可靠性。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

面对需要复杂算法或实现细节的编程任务，大语言模型生成的初始代码更容易出错，因此常用执行反馈驱动模型反复修改答案。问题在于，自纠错的方向取决于验证信号：一旦生成这些信号的参考代码不可靠，执行本身虽然是确定的，其结果却不能代表真实正确性，进而造成无效修改或错误强化。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于语言模型裁判的验证与自纠错**：让语言模型阅读候选代码、题目或执行信息，判断代码是否正确并生成修改反馈，再据此迭代更新答案。
- **基于生成测试或参考代码执行的验证**：生成少量测试输入，或运行一个乃至多个参考程序获得预期输出，然后检查候选代码是否通过测试或是否与参考输出一致，以决定是否触发纠错。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 语言模型裁判的判断本身可能不可靠；依赖较少的生成测试也难以覆盖复杂输入空间，因此验证信号可能遗漏隐蔽错误，并错误决定候选代码是否需要修改。
- 不少执行式方法默认参考代码或测试答案正确，却没有显式量化参考代码的可信度；当参考程序含有细微缺陷、只覆盖部分情形或在复杂输入上相互冲突时，会把确定的执行结果转化为误导性监督，使正确代码被不必要地改写，或使错误代码得到强化。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究已使用一致性来选择通过更多测试或与其他答案更一致的方案，但在执行引导的代码自纠错中，仍缺少一种不依赖已知标准答案、能够直接从大规模执行行为中量化每个参考程序可靠性的机制。未解决的关键对象不是候选答案是否与某次测试一致，而是用于产生监督的参考代码本身有多可信。

</div>
<div markdown="1"><span>核心问题</span>

在没有可信测试答案、且多个生成参考程序都可能出错的条件下，能否利用它们在大量、多样化输入上的输出一致与分歧模式，统计推断各参考程序的潜在可靠性，并用该估计筛除不可靠监督，从而改善代码自纠错的有效性与稳定性？

</div>
<div markdown="1"><span>作者直觉</span>

若多个独立生成的程序在许多不同输入上持续给出相同结果，而某个程序经常偏离这种稳定共识，后者更可能含有错误；反过来，偶然一次一致或分歧不足以下结论。因而，大规模执行把程序之间难以直接观察的正确性转化为可重复观察的一致性模式，再由统计聚合方法区分较可信与较不可信的参考程序，就有机会在反馈进入自纠错流程之前降低误导风险。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ExeCRE 的目标不是直接证明程序在所有输入上都正确，而是判断某段候选代码是否足够可靠，可以安全地充当自纠错过程中的参考程序。给定题目 $P$，系统先生成候选代码集合 $C_P$，再依据题目输入格式抽取若干输入模式，并据此批量构造合法且多样的执行输入 $I_P$。所有候选代码都在这些输入上运行，得到执行输出矩阵 $O$；系统不需要测试答案，而是把候选代码之间的输出一致与分歧转换成统计信号，并将“输入”视作待标注样本、“候选代码”视作有不同错误率的标注者，使用 Dawid–Skene 模型通过 EM 推断每段代码的潜在可靠性分数 $\alpha_j$。
获得可靠性分数后，系统选择最高可靠或达到阈值的参考代码，由它为大量输入产生预期输出，形成可用于执行判定的测试。只有通过可靠性筛选的测试才会向当前解答提供失败反馈并触发下一轮修改；低可靠参考代码产生的冲突不会直接推动自纠错。直观地说，ExeCRE 不是询问某个模型“哪段代码正确”，也不是把多数票直接当作真值，而是先观察多段程序在大量随机情形下如何结盟或分歧，再估计每个“投票者”长期犯错的倾向，从而决定哪些程序有资格担任裁判。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选参考代码与输入模式构造

模型为同一题目生成候选参考代码集合 $C_P=\{C_1,\ldots,C_{|C_P|}\}$，同时从题目中抽取输入 schema，用结构约束和语义约束描述字段类型、范围、长度关系与依赖关系，再按多个 schema 随机采样执行输入集合 $I_P$。schema 的作用是使大规模随机输入尽量可解析且符合题目条件，而不是让语言模型逐条编写测试。

<div class="method-step__io" markdown="1">

**输入**：题目实例 $P$，包括自然语言题意、输入输出格式与约束；以及代码生成模型。<br>
**输出**：多个具有实现多样性的候选代码，以及一批结构合法、数值多样的执行输入。

</div>

**直观理解**：候选代码相当于让多名解题者独立作答，schema 则像随机出题器的模板：它规定题目实例应长什么样，再快速生成许多不同实例。这样既能扩大行为观察范围，也能减少完全无效的随机字符串。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 批量执行与一致性信号投影

对每个代码—输入组合运行 $C_j(I_i)$，记录正常输出或相应执行结果 $O_{ij}$，由此形成矩阵 $O=[O_{ij}]$。随后比较同一输入上不同候选代码的执行输出，把原始输出投影为可供统计聚合的一致性信号；该步骤只利用候选间的行为关系，不要求输入对应的真实答案。

<div class="method-step__io" markdown="1">

**输入**：候选代码集合 $C_P$ 与执行输入集合 $I_P$。<br>
**输出**：覆盖候选代码和随机输入的执行输出矩阵，以及由输出一致或分歧形成的观测信号。

</div>

**直观理解**：系统暂时不知道哪一个具体输出正确，但能够看到哪些程序经常给出相同答案、哪些程序经常偏离其他程序。单次相同并不足以证明正确，因此需要在大量输入上积累这种关系。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### Dawid–Skene 潜在可靠性估计

ExeCRE 将每个执行输入对应的结果看作未知的潜在标签，将每段候选代码看作具有自身错误倾向的噪声标注者，并使用 Dawid–Skene 模型的 EM 过程交替估计潜在标签与代码特定错误率。最终为每段代码 $C_j$ 产生可靠性分数 $\alpha_j\in[0,1]$，以区别“经常与可靠群体一致”和“仅凭局部多数碰巧一致”的候选。

<div class="method-step__io" markdown="1">

**输入**：由执行输出矩阵 $O$ 投影得到的一致性观测。<br>
**输出**：每段候选代码的可靠性分数，以及最高可靠或超过阈值的参考代码集合。

</div>

**直观理解**：普通多数投票默认每名解题者同样可信；Dawid–Skene 会同时推测答案和各解题者的可信程度，让经常表现异常的程序在后续判断中影响更小。这里估计的是统计可靠性，并非形式化正确性证明。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 可靠测试构造与迭代自纠错

系统选择最高可靠的参考代码，并以阈值 $\alpha=0.95$ 过滤不可信代码；被采纳的参考代码在更多输入上的输出被当作预期输出，构成执行测试。当前解答若未通过这些可信测试，失败信息才进入最多若干轮的确定性自纠错；若参考代码不够可靠，则不让其生成的信号触发修改。

<div class="method-step__io" markdown="1">

**输入**：通过可靠性筛选的参考代码、待改进的当前解答，以及随机生成的合法输入。<br>
**输出**：经过可靠执行反馈迭代后的最终候选解答；同时减少对本来正确代码的无必要修改。

</div>

**直观理解**：参考程序相当于临时裁判，但先要通过资格审查；只有可信裁判指出失败时，系统才要求选手改答案。其核心价值不是增加反馈数量，而是阻止错误裁判把正确程序改坏。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 候选执行输出矩阵

$$
C_P=\{C_1,C_2,\ldots,C_{|C_P|}\},\quad I_P=\{I_1,I_2,\ldots,I_{|I_P|}\},\quad O_{ij}=C_j(I_i),\quad O=[O_{ij}]
$$

**符号说明**

- $P$：一个待求解的编程问题实例。
- $C_P$：针对问题 $P$ 生成的候选代码集合。
- $C_j$：第 $j$ 段候选代码。
- $I_P$：针对问题 $P$ 构造的执行输入集合。
- $I_i$：第 $i$ 个执行输入。
- $O_{ij}$：候选代码 $C_j$ 在输入 $I_i$ 上产生的执行输出。
- $O$：汇总所有代码—输入执行结果的输出矩阵，行对应输入，列对应候选代码。

<div class="equation-explanation" markdown="1">

**直观理解**：该式定义了 ExeCRE 的原始证据：每段候选代码都回答同一批随机实例，矩阵的一列就是一段代码在不同实例上的行为轨迹。后续方法不要求预先知道矩阵中哪个输出是真值，而是从列之间反复出现的一致与分歧估计可信度。<br>
**原文位置**：第 2 节 Preliminary

</div>

</div>

<div class="equation-block" markdown="1">

#### 候选代码可靠性评分

$$
\alpha_j\in[0,1]
$$

**符号说明**

- $\alpha_j$：Dawid–Skene 聚合后赋予候选代码 $C_j$ 的可靠性分数，数值越高表示越适合充当后续执行监督的参考代码。
- $j$：候选代码索引。

<div class="equation-explanation" markdown="1">

**直观理解**：可靠性分数把复杂的一致性行为压缩成可用于筛选的量。论文没有在所给章节中列出 Dawid–Skene 的完整似然函数或 EM 更新公式，因此这里仅保留原文明确定义的核心评分关系，不补造优化方程。<br>
**原文位置**：第 2 节 Preliminary；第 4.5 节给出筛选阈值

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：ExeCRE 不是一个需要端到端监督训练的新生成模型，论文也未在所给章节中定义神经网络损失函数。其核心计算是在每个问题内部对 Dawid–Skene 潜变量模型执行 EM：根据候选代码的一致性观测，交替推断输入层面的潜在结果和代码层面的错误倾向，直至得到可靠性分数 $\alpha_j$；这些分数服务于参考代码选择，而不用于更新底层 LLM 参数。自纠错阶段同样是推理时过程：模型根据可信执行失败反馈重新生成代码，但论文设定的生成模型权重保持不变。原文未在所给节选中明确报告 DS 的完整似然、先验、初始化、收敛准则或逐步更新式，复现时需要进一步核对论文正文或开源实现。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Schema 驱动的随机输入生成器**

该模块从题目输入规范中抽取多个 schema，并在结构与语义约束下批量采样输入。与逐条使用 LLM 生成测试相比，它支持约千级规模的输入构造；当 schema 抽取错误时，所产生的无效或不一致执行通常会降低可靠性分数，而不是自动成为高置信监督。

> 直观理解：纯随机字符大多无法被程序读入，逐条请模型编测试又昂贵且数量有限。schema 先固定“输入必须满足什么形状和关系”，再随机填充内容，因此能以较低成本观察程序在更多边界和组合上的行为。

**2. 执行一致性与 Dawid–Skene 估计器**

该模块从 $O=[O_{ij}]$ 中提取候选之间的输出一致模式，并用 Dawid–Skene 的潜变量建模估计代码特定错误率和 $\alpha_j$。它借鉴多标注者聚合：执行输入对应 item，候选代码对应 annotator，一致性投影对应观测标签；论文强调该模型能够刻画不同代码的错误倾向，而不只是计算输出众数。

> 直观理解：若十段代码中有几段源自同类错误，多数票也可能集体出错；估计器尝试根据多次行为识别哪些程序一贯可信、哪些程序容易偏离。它仍依赖统计假设，特别是候选错误并非完全独立，因此输出只能解释为信任程度。

**3. 可靠性门控的执行反馈器**

该模块依据 $\alpha_j$ 选择或过滤参考代码，并让通过筛选的代码生成输入—预期输出测试；论文实现采用全局阈值 $0.95$。这些测试作为当前解答的执行 judge，失败信息用于迭代修正，而低分参考代码产生的测试被排除，从源头限制误导反馈及其跨轮累积。

> 直观理解：普通自纠错通常默认生成的测试或评论值得相信，ExeCRE 则在反馈进入修正循环前设置一道门。这样做尤其保护已经正确的代码，因为不可信测试不会仅凭一次冲突就迫使模型重写答案。

**训练与推理**

整个框架运行于推理阶段。对每个 LiveCodeBench 问题，先以较高采样随机性生成多段候选参考代码，并抽取多个输入 schema；随后按 schema 生成随机输入，对所有候选批量执行，形成约为“候选数乘输入数”的输出矩阵。系统将执行一致性输入 Dawid–Skene 估计器，为每个候选产生 $\alpha_j$，再选取最高可靠且满足阈值条件的参考代码。该参考代码为更大测试集生成预期输出；当前解答只在可信测试失败时接收反馈，并以确定性解码生成下一版代码，重复执行与修改，最终以最后一版代码作为输出。
这一流程中，候选参考代码的用途与最终代码不同：前者主要提供低效率但力求语义正确的“临时答案生成器”，因此可靠性评价可在 semantic-only 设置下把超时视为正确；后者仍需通过正式评测中的正确性和效率要求。GSM8K 扩展则不运行多轮修正，而是从数值扰动产生的执行一致性判断代码推理路径是否可信：达到同一阈值便执行代码，否则退回直接回答。需要注意，ExeCRE 给出的只是相对于所采样候选和输入分布的统计证据；若所有候选共享同一错误，或随机输入没有触及错误区域，方法并不能提供完备正确性保证。

**复现信息**

LiveCodeBench 的主要配置为：每题采样 $10$ 个参考代码候选和 $5$ 个输入 schema，每段代码通过 schema 驱动策略生成 $300$ 个输入，原文称执行输出矩阵规模约为 $10\times300$。候选参考代码使用温度 $1.0$、top-$p=0.99$ 以增加实现多样性；自纠错采用温度 $0.0$ 的贪心解码以控制跨轮随机性，涉及多轮修正的方法统一运行 $20$ 轮。可靠性筛选阈值设为 $\alpha=0.95$；构造自纠错测试时，测试套件在单线程下限制为 $1$ 分钟，实践中约可执行 $2000$ 个测试用例。
这些配置中最影响解释的是候选多样性、输入覆盖和阈值：候选过少或高度同质会削弱“多标注者”证据，输入过少可能遗漏实现差异，而较高阈值会提高采用参考代码时的保守程度但降低召回。论文在 LiveCodeBench 上评估 GPT-5.2、DeepSeek-V3.2、Qwen2.5-Coder-32B-Instruct 和 LLaMA-3.1-8B-Instruct，并将结果取 $5$ 次运行的均值与标准差；GSM8K 只使用后两种模型。运行时间分析采用多线程执行和批量 API 请求，但 DS 估计本身少于 $3$ 秒，主要成本来自候选及执行证据收集。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- LiveCodeBench：主要代码生成评测集，按 Easy、Medium 和 Hard 难度报告结果，并用于评估最终 Pass@1、候选程序可靠性识别及自纠错过程中的误导反馈。摘录未给出具体版本、题目数量或评测时间窗口，只说明 Qwen2.5-Coder-32B-Instruct 与 LLaMA-3.1-8B-Instruct 的知识截止日期早于整个评测窗口。
- LiveCodeBench 隐藏测试：作为候选程序语义可靠性的事后真值。仅当程序在每个隐藏测试上的状态均为 Accepted 或 TLE，且没有任何失败测试时，才标为正例；这是把 TLE 视为语义正确的“semantic-only”判定，因而不评价运行效率是否真正满足限制。
- GSM8K：附加适用性研究，用来检验同一种可靠性估计机制能否迁移到基于代码的数学推理。当前摘录未提供其样本规模、划分、具体基线或数值结果。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Pass@1**

衡量模型一次生成或完成自纠错后提交的首个最终程序通过评测的比例，直接反映端到端代码生成效果。 （越高越好，因为更高值表示更多问题的最终答案能够通过测试。）

</div>
<div class="metric-item" markdown="1">

**F1**

可靠性识别中 Precision 与 Recall 的调和平均。正预测表示最高分候选的可靠性达到阈值 $\alpha=0.95$ 并被采用；Precision 对应采用错误参考程序、从而引入误导反馈的风险，Recall 对应保留正确参考信号的能力。 （越高越好，因为它同时惩罚错误采用和过度回退，比只看 Precision 或 Recall 更能反映自纠错场景中的取舍。）

</div>
<div class="metric-item" markdown="1">

**Fallback**

没有任何参考程序达到采用条件、因而退回公开测试反馈的问题比例。它描述系统的采用覆盖率，而不是独立的正确性指标。 （不存在脱离上下文的单调优劣：过高表示可靠候选利用不足，过低则可能意味着系统采用了不可靠程序；应与 F1、Precision 及最终 Pass@1 联合解释。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四个不同规模模型上的 LiveCodeBench 总体结果

<div class="result-value" markdown="1">

作者报告 ExeCRE 在全部四个模型上都取得最高的总体 Pass@1，收益主要出现在 Medium 和 Hard 题目；Easy 题目因准确率接近饱和，各方法差异较小。

</div>

这说明可靠性筛选带来的端到端收益具有跨模型一致性，并且在复杂问题上更有价值，因为此时错误候选更可能形成误导反馈。但摘录没有提供表 2 的完整分数、标准差或显著性检验，且其中两个模型存在数据污染无法排除的问题，所以该结论不能单独证明所有提升都来自 ExeCRE，也不能据此量化四个模型上的平均增益。

<div class="result-source" markdown="1">

来源：第 5.1 节 RQ1；表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 2, ExeCRE achieves the best overall Pass@1 on all four models.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 知识截止日期早于评测窗口的 Qwen2.5-Coder-32B-Instruct

<div class="result-value" markdown="1">

ExeCRE 将 Pass@1 从 31.5 提高到 32.5，即增加 1.0 个百分点；同时将误导反馈案例的平均数量从 50.4 降至 7.4，减少 43.0 个，约下降 85.3%。

</div>

该模型提供了相对更干净的时间切分证据：最终通过率虽只小幅提高，但错误纠错信号大幅减少，说明可靠性筛选首先改善的是反馈质量，最终性能增益可能受可纠正题目数量等因素限制。它仍不是严格因果隔离实验，也不能排除模型随机性；应结合表 2 的五次运行标准差判断波动，但摘录未给出对应数值。

<div class="result-source" markdown="1">

来源：第 5.1 节 RQ1；表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Qwen2.5-Coder-32B-Instruct, ExeCRE increases Pass@1 from 31.5 to 32.5 and reduces misleading feedback from 50.4 to 7.4.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 知识截止日期早于评测窗口的 LLaMA-3.1-8B-Instruct

<div class="result-value" markdown="1">

ExeCRE 将 Pass@1 从 19.4 提高到 21.0，即增加 1.6 个百分点；误导反馈案例的平均数量从 30.0 降至 1.2，减少 28.8 个，约下降 96.0%。

</div>

较小模型上仍出现最终性能提升，并且误导反馈几乎被消除，支持该机制不只适用于最强模型。与此同时，Pass@1 仍为 21.0，表明减少错误反馈并不等同于解决基础模型的代码生成能力瓶颈；可靠性估计主要防止自纠错把答案改坏，不能保证生成正确修复。

<div class="result-source" markdown="1">

来源：第 5.1 节 RQ1；表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On LLaMA-3.1-8B-Instruct, Pass@1 increases from 19.4 to 21.0, while misleading feedback decreases from 30.0 to 1.2.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- GPT-5.2 的知识截止日期晚于整个 LiveCodeBench 评测窗口，DeepSeek-V3.2 又未公开精确截止日期，因此这两个模型的结果不能视为无污染证据；作者明确只把它们用于比较。较可信的时间切分支持主要来自 Qwen2.5-Coder-32B-Instruct 与 LLaMA-3.1-8B-Instruct。
- 所给摘录缺少表 2 和表 4 的完整数据，也未提供 RQ3、RQ4、GSM8K、运行时间、token 成本及输入构造敏感性的具体结果。因此无法核验可靠性识别的 Precision、Recall、F1、Fallback，不能判断阈值稳健性或计算代价，也不应从当前材料推断统计显著性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 代表性自纠错基线：用于检验在常规执行反馈式自纠错之上加入可靠性筛选，是否能提高最终 Pass@1 并减少对原本正确代码的误导反馈；摘录未给出该基线的具体名称和完整流程。
- LLM Judge／LLM Analyze：前者直接要求大模型判断代码是否正确，后者采用 TextGrad 风格先分析再判断。两者代表依赖模型文本推理、但不访问隐藏测试的可靠性判断方法。
- CodeJudge：采用 Analyze then Summarize 流程，先分析候选程序，再根据分析输出 YES 或 NO；它用于比较专门的代码评审提示流程与执行一致性推断之间的差异。
- ExeCRE-Voting：使用多数投票聚合候选程序在生成输入上的执行输出，是 ExeCRE 的直接替代聚合器；与采用 Dawid–Skene 模型和 EM 推断的 ExeCRE 对比，可检验显式估计各候选程序错误率是否优于简单按输出多数取胜。

**实验想回答的问题**

- RQ1：ExeCRE 能否在不同规模和不同知识截止日期的代码大模型上提高最终代码生成的 Pass@1，尤其是在更容易受到错误参考程序干扰的中高难度题目上？
- RQ2–RQ4：基于随机输入执行一致性的可靠性估计，能否准确区分语义正确与错误的候选程序、减少误导性或不必要的自纠错反馈，并对可靠性阈值、错误程序之间的一致以及输入构造方式保持稳健？

**实验实现**

主实验覆盖四个不同规模的模型，并按题目难度拆分 LiveCodeBench 的 Pass@1；所有表 2 数值均来自五次运行的均值与标准差。可靠性识别把每道题视为一个实例：系统仅在最高分候选达到 $\alpha=0.95$ 时采用该程序，否则回退到公开测试；隐藏测试只用于事后建立真值，各判断方法均不能访问隐藏测试。语义评估将 TLE 与 Accepted 一同视为正确，因此主要测试程序输出语义，而非严格的时间性能。ExeCRE 与 ExeCRE-Voting 使用相同的 $0.95$ 阈值，分别通过 Dawid–Skene 的 EM 推断和多数投票处理执行一致性；SLM Judge 则使用经二分类微调的 Qwen2.5 Coder 3B，并将阈值设为 $0.06$，以使其回退率接近 ExeCRE。摘录提到还分析运行时间与 token 成本，但未给出实现配置或数值。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 优惠券边界条件案例展示了“错误程序抱团”问题：正确程序 A–C 实现 $subtotal\geq25$ 且 $count\geq3$，错误程序 D–E 将第一个条件写成严格大于，F–G 将第二个条件写成严格大于。在同时触发两类边界错误的输入上，四个错误程序一致输出 F，使多数投票出错；跨三个输入计算后，ExeCRE-Voting 给 A–C 的分数为 $13/21$、给 D–G 的分数为 $11/21$，两者都低于 $0.95$，只能回退。Dawid–Skene 联合估计每个程序的错误率后能把 A–C 与 D–G 更清楚地区分并采用正确程序。该例说明模型化“谁经常错、错法是否相关”可能优于逐输入数票，但它只是构造性示例，并非大规模消融或统计证明。证据：“Across the three inputs, ExeCRE-Voting assigns A–C a score of 13/21 and D–G a score of 11/21.”；位置：第 5.2.1 节，表 3。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Proposes execution-consistency-based reliability estimation to improve verification and self-correction in LLM code generation and mathematical reasoning.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`d214b7e4d45210dbd1a998e611b517f25a04ca61043141c9098bce53c85eb614`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
