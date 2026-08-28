---
title: "[论文解读] When the Canonical Completion Is Wrong: Formalizing and Measuring the Jump in Large Language Models"
description: "[arXiv 2608.26187][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.26187"
announcement_date: "2026-08-28"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:35:00.122678+00:00"
source_sha256: "fc72563851dbd0992e9987d6891d48db4ebf8f9ea41ec6700af51412dec00c05"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "LLM 其他"
  - "大语言模型"
  - "溯因推理"
  - "跳跃"
  - "覆写"
  - "范畴论"
  - "Kan 延拓"
  - "有限扩展问题"
  - "机器检查证书"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.26187</p>

# When the Canonical Completion Is Wrong: Formalizing and Measuring the Jump in Large Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Dai Shi, Xiaoyu Li, José Miguel Hernández-Lobato</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of Cambridge, United Kingdom University of New South Wales, Australia；Affiliation: University of Cambridge, United Kingdom；University of New South Wales, Australia</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26187v1) · [PDF 下载](https://arxiv.org/pdf/2608.26187v1) · **关键词** 大语言模型, 溯因推理, 跳跃, 覆写, 范畴论, Kan 延拓, 有限扩展问题, 机器检查证书<br>
**代码**: [https://github.com/EEthanShi/kan-jump-test](https://github.com/EEthanShi/kan-jump-test)

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

本文处于大语言模型推理能力、溯因推理与范畴论形式化的交叉处。核心争议是：模型能否完成所谓“跳跃（jump）”，即从已有证据转向一个此前未显式给出的新公理或新结构。由于完整的“发明新框架”很难直接操作化，论文把问题缩小为有限扩展任务：给定只覆盖部分对象的观测数据，模型需要补全隐藏部分；数据本身诱导出左、右 Kan 延拓这两种规范补全，而额外约束又明确排除这些默认答案。论文据此只考察跳跃的第二步“覆写（override）”：模型在答案空间和约束均已给定时，能否放弃被排除的默认补全，而非考察模型能否自行发现约束或创造全新的数学语言。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**溯因推理（abduction）**

溯因推理是从观察到的证据出发，提出能够解释证据的假设或理论。本文进一步区分“生成候选假设”和“在已限定的候选空间中选择假设”，实验只测量后者。

</div>
<div class="concept-item" markdown="1">

**Kan 延拓（Kan extension）**

Kan 延拓是范畴论中把局部定义的数据系统性扩展到更大定义域的方法；左 Kan 延拓与右 Kan 延拓提供两种由已有数据直接计算出的规范补全。本文将它们视为不参考额外约束时的默认答案，但这并不等于所有学习模型在任何情形下都必然采用它们，因此还需先做无约束校准。

</div>
<div class="concept-item" markdown="1">

**同构意义下唯一（unique up to renaming）**

补全可能需要引入新的元素，而这些元素的名称本身没有意义；若两个答案仅在新元素的命名上不同，就视为同一个结构。该条件使论文能够在不依赖任意命名的情况下认证唯一正确结构，并计算有限答案空间中的机会水平。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

每个跳跃实例的输入包括：完全给定的观测部分、需要补全的隐藏部分、有限且可机器检查的约束，以及预先认证的答案空间。模型输出隐藏部分的结构补全；实例证书保证至少存在一个满足全部约束的补全，该补全在新元素重命名意义下唯一，并且不同于观测数据的左、右 Kan 延拓。实验先在无约束条件下记录每个模型实际采用的默认补全，再加入约束；只有当模型原先确实表现出相应默认、随后又因约束放弃它时，才把行为解释为“覆写”。配对控制实例则让约束选择规范补全，用于区分“无法完成扩展”与“只能按默认方式扩展”。因此任务检验的是受约束选择能力，而不检验模型能否自行生成约束、提出答案空间或发明新的表示框架。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$F_0$**

种子实例中的部分数据表，即模型已经观察到的系统部分。

</div>
<div class="notation-item" markdown="1">

**$b$**

数据表中被隐藏、需要模型补全的对象。

</div>
<div class="notation-item" markdown="1">

**$t$**

认证目标补全中的结构操作；在论文示例里，它交换模型必须新引入的两个元素。

</div>

</div>

**直接相关的工作**

- **文献 [34] 关于大语言模型能否完成“跳跃”的论述**: 该工作提出或强化了模型在结构上不能从经验跃迁到新公理系统的观点，并强调具身、前符号机制；本文不声称覆盖其完整定义，而是将争议拆成四步，仅形式化测量其中已有约束和答案空间时的“覆写”步骤。
- **文献 [16] 的左、右 Kan 延拓理论**: 该理论为部分数据提供可计算的两种规范扩展，因而构成本文定义“默认补全”的数学基础；跳跃实例要求认证答案同时不同于这两种规范延拓。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

关于大语言模型能否完成“跃迁”存在根本争议：模型可能擅长从既有规律归纳或按规则演绎，却未必能在惯常解释失效时转向数据中从未直接呈现的新结构。若“跃迁”没有可检验的定义，就无法判断模型究竟被默认答案束缚，还是能够依据约束放弃它，也无法定位失败发生在提出约束、生成新框架还是选择候选答案的阶段。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **关于皮尔士式溯因与模型结构性能力的理论论证**：一类观点把跃迁理解为从经验迈向新公理体系的溯因过程，并据此主张大语言模型因缺少具身、前符号等机制而在结构上不能完成跃迁；反方则援引无需具身基础的溯因论证以及机器生成的数学发现，质疑这种机制判断。双方主要争论模型是否具有相应能力，却没有把争议转化为统一、可重复的操作性测试。
- **基于规范外推或误差最小化的默认补全**：当观测数据只覆盖系统的一部分时，范畴论中的左、右 Kan 扩张可仅凭已有数据计算出两种规范补全；相关补全也可从误差最小化角度得到，因此可作为损失优化模型可能采用的默认延伸方式。既有做法通常研究模型能否延续已见模式，但没有专门检验：当明确约束排除这种默认补全时，模型是否仍会固守它。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- “跃迁”缺少形式定义和量化指标，因而支持或反对大语言模型跃迁能力的证据难以直接比较，也不能将一般推理失败与对默认补全的依赖区分开来。
- 只观察最终答案不足以归因：模型可能根本不会补全、搜索预算耗尽、误解约束，或仅进行记忆结构匹配。若不先测量各模型的无约束默认答案，并设置选择规范补全的匹配控制实例，就不能把失败可靠地解释为“无法放弃默认”。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺一种经过认证的实验构造：它应保证隐藏部分存在正确补全、该补全在新元素重命名意义下唯一，并且不同于数据的规范 Kan 补全；同时还需提供机器可检查的约束、有限答案空间与可计算的偶然成功水平。只有满足这些条件，研究者才能将完整“跃迁”拆分为不同阶段，并单独测量其中已经给出约束与候选空间的“覆盖默认”阶段，而不把生成约束或发明新数学语言的能力混入测试。

</div>
<div markdown="1"><span>核心问题</span>

当题目中明确陈述的约束排除了模型自身的默认补全时，模型能否放弃该默认补全，并选择约束所允许的非规范结构？

</div>
<div markdown="1"><span>作者直觉</span>

作者把宏大的科学革命问题缩小为一个可控的有限扩张问题：先让模型在无约束条件下暴露其自然补全，再加入能够排除该补全的可验证约束，并检查模型是否仍返回默认结构。Kan 扩张提供了由现有数据单独决定的规范参照，而“存在、唯一且非规范”的证书排除了无解、多解和偶然匹配等混淆因素；因此，这一设计可以像实验室测试一样隔离“看见默认答案不可行后是否愿意改选”这一具体能力，但不声称已经测量自主生成约束或创造全新理论语言的完整跃迁。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文提出的不是一种训练大型语言模型的新算法，而是一套用于形式化并测量“跳跃”的可判定测试框架。给定有限范畴中的部分数据 $F_0:\mathsf{C}_0\to\mathsf{D}$，任务要求学习器补全为完整函子 $F:\mathsf{C}\to\mathsf{D}$。框架先用左右 Kan 扩张构造不读取约束的规范补全，再用有限、可判定且不依赖元素名称的约束 $\mathcal{K}$ 排除这些默认答案，并保证剩余正确解存在且在重命名意义下唯一；随后将范畴表、约束和大小上界 $N$ 序列化给模型，检查其输出是否为满足约束的有界函子，并通过去掉约束的校准版本与匹配控制实例区分“真正覆盖默认补全”与“不会完成基本任务”。

直观地说，研究者先把部分结构最自然的两种“自动补法”明确算出来，再设计一道题，使这两种补法都确定错误，而约束只允许一种新的结构答案。模型只有读取并利用约束、离开原本默认答案，才可能成功；同时，元素名称的任意置换不影响评分，因此测试关注的是结构推理，而不是是否复现标准答案中的标签。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造有限扩张问题

定义扩张纤维 $\mathrm{Ext}(F_0)=\{F:\mathsf{C}\to\mathsf{D}\mid F\circ K=F_0\}$，完整答案必须给出新对象上的有限集合以及所有涉及新对象的态射函数表，并满足函子的恒等与复合规律。

<div class="method-step__io" markdown="1">

**输入**：有限范畴表 $\mathsf{C}$、其非空真满子范畴 $\mathsf{C}_0$、包含函子 $K:\mathsf{C}_0\hookrightarrow\mathsf{C}$，以及部分数据函子 $F_0:\mathsf{C}_0\to\mathsf{D}$；本文具体取骨架有限集合范畴 $\mathbf{FinSet}$ 为 $\mathsf{D}$。<br>
**输出**：所有与已知数据严格一致的完整函子所组成的候选空间 $\mathrm{Ext}(F_0)$。

</div>

**直观理解**：这一步把题目写成有限表格补全：旧对象和旧箭头已经固定，模型只需补出隐藏对象及其相关函数，但补出的整张表必须内部一致。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算约束盲的规范默认补全

按有限组合公式计算左 Kan 扩张 $\mathrm{Lan}^{*}$ 与右 Kan 扩张 $\mathrm{Ran}^{*}$：前者把数据元素沿所有进入新对象的路径前推并按已有等式取商，后者枚举沿所有离开新对象路径的一致取值元组。将二者的规范等价类并为 $\mathrm{Kan}(F_0)=[\mathrm{Lan}^{*}]\cup[\mathrm{Ran}^{*}]$。

<div class="method-step__io" markdown="1">

**输入**：仅使用 $\mathsf{C}$、$\mathsf{C}_0$ 与 $F_0$，不读取约束集 $\mathcal{K}$ 或大小上界 $N$。<br>
**输出**：不借助任务约束即可得到的规范类，作为待覆盖的学习器默认答案。

</div>

**直观理解**：左扩张相当于“只添加数据强迫添加的内容”，右扩张相当于“保留所有仍与数据相容的选择”；它们是部分数据自身给出的两个无额外假设答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成并认证跳跃实例

计算可接受集 $\mathrm{Adm}(S)$，并认证四项条件：至少有解、与所有预注册规范补全不相交、所有可接受解仅相差新元素重命名，以及每个新对象都通过进入或离开路径连接到数据。约束必须可判定、规范不变且不直接点名答案元素，并且必须蕴含新对象大小不超过 $N$。

<div class="method-step__io" markdown="1">

**输入**：扩张问题、预注册的有限规范算子库 $\mathcal{L}$、有限约束集 $\mathcal{K}$ 和声明的对象大小上界 $N$。<br>
**输出**：带机器可检验证书的跳跃实例 $S=(\mathsf{C},\mathsf{C}_0,\mathsf{D},F_0,\mathcal{K},N)$，以及由唯一规范分量确定的正确结构。

</div>

**直观理解**：这相当于出一道有唯一结构答案的题，并预先证明“自然默认答案必错、另一个答案确实存在”。禁止在约束中点名具体元素，是为了防止把答案暗藏在题干里。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 运行模型并进行结构化评分

先检查输出是否属于有界扩张空间 $\mathrm{Ext}_N(F_0)$，再以是否精确属于 $\mathrm{Adm}(S)$ 判定成功；不构成合法有界函子的输出记为零分并单列为格式失败。评分在规范变换下不变，因此新元素的标签置换不会改变结果。

<div class="method-step__io" markdown="1">

**输入**：范畴与数据表、约束文本及上界 $N$ 的预注册序列化，以及学习器 $L$ 输出的显式对象和函数表。<br>
**输出**：每次试验的成功、规范默认、约束错误或格式失败等结构化判定。

</div>

**直观理解**：评分器不比较答案字符串，而是检查模型交出的整张结构表是否数学上合法且满足全部约束；只改隐藏元素名称不会被误判为错误。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 跳跃实例的核心认证条件

$$
\mathrm{Adm}(S):=\{F\in\mathrm{Ext}(F_{0}):P(F)\ \text{for all}\ P\in\mathcal{K}\},\qquad \mathrm{Adm}(S)\neq\emptyset,\qquad \mathrm{Adm}(S)\cap\mathrm{Canon}_{\mathcal{L}}(F_{0})=\emptyset,\qquad \mathrm{Adm}(S)\ \text{is a single gauge component}
$$

**符号说明**

- $S$：实例元组，由有限范畴、已知子范畴、余域、数据函子、约束集和大小上界组成
- $F_0$：定义在已知子范畴上的部分数据函子
- $\mathrm{Ext}(F_0)$：所有严格限制为给定数据 $F_0$ 的完整函子
- $\mathcal{K}$：有限、可判定、规范不变且元素盲的约束集合
- $P$：约束集中的一个谓词
- $\mathrm{Adm}(S)$：满足全部约束的可接受扩张集合
- $\mathcal{L}$：测试前预注册的约束盲扩张算子库
- $\mathrm{Canon}_{\mathcal{L}}(F_0)$：算子库仅根据部分数据生成的所有规范补全之规范分量并集
- $F$：候选完整函子

<div class="equation-explanation" markdown="1">

**直观理解**：三个条件分别保证正确答案存在、任何预注册的约束盲默认答案都不可能正确，以及所有正确答案在忽略新元素重命名后具有同一结构。原文定义还要求每个新对象与已知数据相连；该支持条件防止 Kan 补全仅因没有输入或输出路径而退化。<br>
**原文位置**：第 4.3 节，Definition 2，条件 (J1)–(J4)

</div>

</div>

<div class="equation-block" markdown="1">

#### 默认校准、约束下默认率与覆盖差距

$$
\mathrm{DC}_{L}(n):=\mathbb{P}\!\left[L(S^{\circ})\in\mathrm{Canon}_{\mathcal{L}}(F_{0})\right],\qquad \mathrm{KD}_{L}(n):=\mathbb{P}\!\left[L(S)\in\mathrm{Canon}_{\mathcal{L}}(F_{0})\right],\qquad \Delta_{L}(n):=\mathrm{DC}_{L}(n)-\mathrm{KD}_{L}(n)
$$

**符号说明**

- $L$：接受序列化实例并输出显式函子表的学习器
- $n$：认证实例生成器所对应的问题尺度
- $S$：包含有效约束的认证跳跃实例
- $S^{\circ}$：与 $S$ 格式相同、但约束块被预注册中性填充替换的校准实例
- $\mathrm{DC}_{L}(n)$：学习器无约束输出落入预注册规范类的概率，即默认规范率
- $\mathrm{KD}_{L}(n)$：约束存在时学习器仍输出规范补全的概率；采用 Kan 库时即 Kan-default rate
- $\Delta_L(n)$：加入约束后规范输出概率的下降量，即覆盖默认的差距
- $\mathrm{Canon}_{\mathcal{L}}(F_0)$：相对于预注册算子库的规范补全类
- $\mathbb{P}$：对认证实例生成器与模型运行所取的概率

<div class="equation-explanation" markdown="1">

**直观理解**：若模型在消融约束时通常选择规范答案，即 $\mathrm{DC}_L(n)$ 高，而加入排除规范答案的约束后 $\mathrm{KD}_L(n)$ 显著降低，则较大的 $\Delta_L(n)$ 表明模型确实覆盖了自身默认补全。仅有该差值仍不够，正式判定还要求跳跃题成功率超过机会水平并通过匹配控制。<br>
**原文位置**：第 4.5 节，公式 (3) 及 Definition 4

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该论文构造的是评测与认证框架，不训练或微调被测模型，也没有通过梯度优化的损失函数；$\mathrm{Adm}(S)$ 成员资格、机会水平以及 $\mathrm{DC}$、$\mathrm{KD}$、$\Delta$ 都是评测判据而非训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Kan 规范补全器**

模块以有限范畴和数据函子的显式表为输入。左 Kan 扩张在每个对象 $c$ 上对所有 $(a,v)\in\mathrm{In}(c)$ 对应的 $F_0(a)$ 做不交并，再按 $\mathsf{C}_0$ 中态射诱导的关系取商；右 Kan 扩张则在所有 $(b,w)\in\mathrm{Out}(c)$ 对应集合的直积中保留满足自然一致性条件的元组。

> 直观理解：该模块提供一个事前固定、完全不看约束的参照答案。只有明确知道模型原本会补什么，才有意义判断它是否因新约束而“跳离”默认方案。

**2. 规范不变的实例认证器**

认证器验证 $\mathcal{K}$ 的可判定性、规范不变性与元素盲性，并检查跳跃条件：$\mathrm{Adm}(S)$ 非空、排除 $\mathrm{Canon}_{\mathcal{L}}(F_0)$、仅含一个规范分量且满足支持条件。大小上界 $N$ 使候选对象和有限函数表的枚举空间有限，从而让存在性、唯一性与机会水平原则上可计算。

> 直观理解：它类似自动验题程序：不仅确认标准答案正确，还确认默认答案必错、没有第二种结构上不同的正确答案，而且题目没有靠元素名字泄露答案。

**3. 校准与对照测量器**

模块同时评估跳跃实例、约束消融实例 $S^{\circ}$ 和匹配控制实例 $S'$。只有无约束输出大多落入预注册规范类、跳跃题表现高于约束盲机会水平，且控制题通过时，框架才允许声称学习器在给定尺度上具有校准后的跳跃能力。

> 直观理解：单看跳跃题答对并不足够，因为模型可能本来就不采用所定义的默认答案；三路比较分别确认“原有默认”“成功离开默认”和“具备基本解题能力”。

**训练与推理**

训练阶段不适用。推理时，学习器收到 $\mathsf{C}$、$\mathsf{C}_0$、$F_0$ 的显式表、约束文本 $\mathcal{K}$ 和大小上界 $N$ 的预注册序列化，并输出完整函子的对象表与态射函数表。评分器依次检查：输出是否延续 $F_0$，是否满足函子恒等和复合规律，所有新对象是否满足大小上界，以及全部约束是否成立；任一条件失败都不属于 $\mathrm{Adm}(S)$。

同一学习器还要在约束被中性填充替代的 $S^{\circ}$ 上运行，以确认其无约束默认确实属于规范类；再在格式匹配但约束恰好指定规范答案的控制实例 $S'$ 上运行，以验证其具备基本表格补全和约束遵循能力。最终的跳跃判断不是单次答对，而是要求校准有效、在已校准实例上的约束成功率高于格式感知但忽略约束的机会水平至少预注册边际 $\varepsilon$，并且控制成功率达到 $1-\delta$。

**复现信息**

可复现评测需要固定四项内容：预注册的规范算子库 $\mathcal{L}$，默认采用 $\mathcal{L}_{\mathrm{Kan}}=\{\mathrm{Lan}^{*},\mathrm{Ran}^{*}\}$；实例和约束的序列化格式；每个生成器的有限大小上界 $N$；以及校准阈值 $\kappa$、成功边际 $\varepsilon$ 和控制容错 $\delta$。$N$ 必须由约束实际蕴含，不能通过截断余域获得，否则会破坏 Kan 扩张所需的有限极限或余极限性质。

答案按严格有限表评分，但接受所有固定已知数据、仅置换新对象元素的规范等价答案。机会水平在严格表层面定义为 $\lvert\mathrm{Adm}(S)\rvert/\lvert\mathrm{Ext}_N(F_0)\rvert$，规范分量层面的比率仅作为次要统计；输出空间无限时不能直接计算该比率，因此声明并固定 $N$ 是使基线可计算、比较公平的关键设计。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 实验使用 pointed-chain family 的九个经形式化认证的有限扩张实例。每个实例都带有机器可检验证书，保证满足额外约束的正确补全存在、在重命名意义下唯一，并且不同于左右 Kan 扩张给出的规范补全；这些实例用于跨难度测量模型是否会放弃默认解。原文节选未报告训练集、验证集或测试集划分，它们应被理解为九道认证评测题，而非传统统计学习数据集。
- 附录 B 给出认证种子实例 $S^{\ast}$ 的无数学术语版本：模型必须补全三阶段信号管线，其中中间状态集合 QUILB 至多含三个状态，内部映射 fen 必须非恒等，并满足三条逐状态布线规则。其唯一容许解在重命名意义下具有三个 QUILB 状态，fen 固定一个状态并交换另外两个；该实例用于说明一道 benchmark item 如何编码抽象扩张问题。
- 匹配控制题将种子实例的要求 D1–D2 替换为“QUILB 至多有一个状态”，使唯一容许答案恰好成为 Kan 扩张本身。它不是独立数据集，而是用于验证测量工具是否能在默认解确实正确时识别该默认解。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Kan-default rate**

受约束试验中，模型输出退回左右 Kan 扩张规范补全的比例。该指标直接测量论文争论中的第二步：当默认补全被额外约束排除时，模型是否仍坚持默认答案。 （越低越好；零表示模型没有在任何受约束试验中返回被明确排除的规范默认补全，但不等于所有输出都满足约束或都是正确解。）

</div>
<div class="metric-item" markdown="1">

**Jump accuracy**

模型输出是否落入机器认证的唯一容许 gauge orbit，即在允许重命名后是否构成完整且满足全部关系、观测、基数界与额外要求的正确补全。 （越高越好；它衡量最终补全正确性，比仅检查是否偏离 Kan 默认解更严格。所给节选未提供该指标的具体公式或逐模型数值。）

</div>
<div class="metric-item" markdown="1">

**Failure-type attribution**

对未得到正确容许补全的回答进行原因分类，重点区分推理预算耗尽、约束错误和退回 Kan 默认解。它用于判断难题上的准确率下降是否支持“模型结构上不能 jump”的解释。 （不存在单一高低方向；若错误集中于预算或约束执行，而 Kan-default 类错误保持为零，则证据更支持模型已经完成“放弃默认解”这一步、但后续求解仍不可靠。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四个前沿模型在九个认证 pointed-chain 实例上的全部受约束试验

<div class="result-value" markdown="1">

248 次受约束试验的 Kan-default rate 均为零，即没有一次输出退回被额外约束排除的 Kan 规范补全。

</div>

作者据此主张，模型在被告知相关约束后能够放弃规范默认答案，因此论文形式化的第二步 jump 并非这些模型的直接瓶颈。分析上，这一结果只证明模型没有选择特定的 Kan 默认失败模式；它不表示 248 次回答全部正确，也不证明模型能够自行发现应加入什么约束或发明新的表示框架。

<div class="result-source" markdown="1">

来源：Abstract；Section 7 Experiments 概述对应的核心结果

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The Kan-default rate is zero in all 248 constrained trials, so the models do jump at this step and abandon the excluded default every time.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 高难度认证实例上的失败回答

<div class="result-value" markdown="1">

作者将高难度下的失败归因于推理预算耗尽或约束错误，并报告未观察到退回 Kan 默认解的失败。

</div>

这一区分说明“答错”和“没有 jump”不是同一件事：模型可能已经避开默认补全，却未能在有限预算内构造完整的唯一容许解，或者遗漏某条关系、基数界或非恒等要求。该结论依赖论文的错误分类规则；所给节选没有提供各类别数量及人工复核一致性，因此无法进一步判断两类非默认错误的相对占比。

<div class="result-source" markdown="1">

来源：Abstract；Section 7 Experiments 的结果解释

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Failures at higher difficulty stem from exhausted reasoning budgets or constraint errors, never from reverting to the default.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 将零 Kan-default rate 与关于 LLM jump 能力的争论对应

<div class="result-value" markdown="1">

作者认为，若所谓 jump incapacity 确实存在，其障碍更可能位于生成约束或发明框架，而不是在约束已给定时放弃被排除的默认补全。

</div>

这是对实验边界的因果定位，而不是对通用创造力的直接测量。实验向模型提供了问题框架和排除默认解的约束，因此只能检验“知道为何默认解不可用之后，能否转向其他补全”；它没有测试模型能否从原始证据独立提出这些约束，也没有测试能否创造描述问题所需的新公理系统。

<div class="result-source" markdown="1">

来源：Abstract；Section 7 Experiments 的争论解读

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

If the disputed incapacity is real, it lies in generating the constraints or inventing the framework.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 外部效度有限：实验只覆盖一个 pointed-chain 认证家族的九个实例及四个前沿模型，而且提示已经提供形式框架与排除默认解的约束。因此结果不能直接推广到开放世界科学发现、从噪声证据自行提出公理，或发明全新表示语言。
- 所给节选缺少逐模型 jump accuracy、逐难度试验数、错误类别计数、控制条件实测结果及评判可靠性信息。零 Kan-default rate 很清晰，但不足以量化模型找到正确非默认解的总体能力；关于预算耗尽和约束错误的归因仍需结合完整表格、原始输出和判分代码复核。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Kan-default baseline：由左右 Kan 扩张确定的规范补全，也是论文所假定的无额外约束默认答案。它是最关键的诊断基线，因为实验要区分“模型无法跳出默认补全”与“模型已经跳出默认补全但仍因其他原因答错”。
- Matched control：把额外要求改为至多一个 QUILB 状态，其唯一容许答案就是 Kan 扩张。该对照保持任务外观和回答形式相近，同时取消必须偏离默认解的条件，用于检查判分器与提示协议是否会无条件把 Kan 解判成失败。
- Certified admissible orbit：每题经机器认证的唯一正确解轨道，即允许对象或状态重命名后的等价答案集合。它不是待训练模型，而是 jump accuracy 的正确性参照，可避免把仅有命名差异的同构答案误判为错误。

**实验想回答的问题**

- 在明确排除 Kan 扩张所给出的规范默认补全后，前沿大语言模型能否稳定放弃该默认解，即完成论文所定义的第二步“jump”？
- 随着认证实例难度上升，模型失败究竟表现为退回 Kan 默认解，还是由推理预算耗尽、约束执行错误等其他因素造成？

**实验实现**

论文在 pointed-chain family 的九个认证实例上评估四个前沿模型；所给实验节选仅明确列出 GPT-5.6 Luna Pro 与 Claude Sonnet 5，并在“Gemini”处截断，因此其余完整模型名称不能由现有材料可靠恢复。评测流程是：向模型提供有限扩张问题、观测关系、额外约束及答案格式界；将输出与认证的容许解轨道和 Kan 默认解比较；分别记录是否正确、是否落入默认解以及错误类型。摘要报告受约束条件共进行 248 次试验。附录中的答案格式要求模型给出完整对象集合及 dax、rell、fen 的全表，从而允许逐项检验关系和约束。温度、采样次数、每题重复数、推理预算上限、判分程序版本及难度分层细节在所给节选中原文未明确报告。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 匹配控制：以“QUILB 至多一个状态”替换种子题的 D1–D2 | 控制条件的唯一容许答案变为 Kan 扩张本身，而非必须偏离 Kan 默认解的三状态设计。 | 该改动隔离了额外约束 D2“fen 非恒等”对 jump 要求的作用：原题中单状态、恒等 fen 的默认答案能复现观测却违反 D2；控制题取消这一冲突后，默认答案恢复为正确答案。它主要验证 benchmark 的诊断逻辑，而不是表明某个模型分数提高或下降；控制条件下的实际模型命中率原文未明确报告。 | Appendix B, The certified seed as a benchmark item<br><span class="experiment-evidence">The matched control replaces D1–D2 by the single requirement that QUILB has at most one state, and its unique admissible answer is then the Kan extension itself.</span> |
| 种子实例中的诊断性约束 D2：要求 fen 不是恒等映射 | Kan 默认答案采用单元素 QUILB 和恒等 fen，能够重现全部观测，但恰好违反 D2，因此被明确设为诊断失败模式。 | D2 把“仅拟合已有观测”与“满足新增工程要求”分开：没有 D2 时，最小单状态补全足够；加入 D2 后，模型必须扩展潜在状态并构造非平凡对合。该设计保证返回默认解具有明确含义，即模型未执行被要求的偏离，而不是普通的命名或格式差异。 | Appendix B, The certified seed as a benchmark item<br><span class="experiment-evidence">The Kan-default answer is the singleton QUILB with fen the identity; it reproduces every observation, violates exactly D2, and is the diagnostic failure mode.</span> |

**定性案例**

- 认证种子题要求构造 NARV→QUILB→SORM 管线。唯一正确轨道可由 QUILB=$\{p,q,r\}$ 表示：dax 把唯一输入状态送到 $p$，rell 为常值映射，fen 固定 $p$ 并交换 $q,r$。这样 fen 连续执行两次为恒等，且不会改变 dax 的落点或 rell 的输出，同时满足 fen 非恒等。相比之下，单状态 QUILB 的 Kan 默认解虽然解释全部已记录观测，却因 fen 必为恒等而违反 D2。该例直观展示了实验所称 jump：不是任意生成不同答案，而是在保持旧观测与关系的同时，为满足新约束引入不可由规范最小补全提供的额外结构。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文形式化并测量大语言模型在受约束外推问题中的跳跃式推理能力，同时提出机器可验证的评测实例。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`fc72563851dbd0992e9987d6891d48db4ebf8f9ea41ec6700af51412dec00c05`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
