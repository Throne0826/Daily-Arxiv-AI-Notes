---
title: "[论文解读] Measuring in-context algorithmic reasoning in language models against an exact Bayes-optimal standard"
description: "[arXiv 2608.01575][LLM 评测] 本文提出 F-ICL，以可穷举的小型图灵完备机器及有界通用先验构造精确的贝叶斯最优后验，用统一标准检验语言模型的上下文学习究竟接近算法归纳，还是主要依赖表面统计规律。"
arxiv_id: "2608.01575"
announcement_date: "2026-08-04"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:58:22.694806+00:00"
source_sha256: "0879c4a5d8fb7e269b291e7cc609574fbc01dc9027207352fcf4271dcb1f959c"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "上下文学习"
  - "算法推理"
  - "贝叶斯最优预测"
  - "Levin–Solomonoff先验"
  - "程序穷举"
  - "补码对称化"
  - "图灵完备自动机"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.01575</p>

# Measuring in-context algorithmic reasoning in language models against an exact Bayes-optimal standard

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Hector Zenil, Luan Ozelim</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Oxford Immune Algorithmics, Oxford University Innovation & London Institute for Healthcare Engineering, U.K；Department of Biomedical Computing, School of Biomedical Engineering and Imaging Sciences & King’s Institute for AI, King’s College London, U.K</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01575v1) · [PDF 下载](https://arxiv.org/pdf/2608.01575v1) · **关键词** 上下文学习, 算法推理, 贝叶斯最优预测, Levin–Solomonoff先验, 程序穷举, 补码对称化, 图灵完备自动机<br>


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

本文提出 F-ICL，以可穷举的小型图灵完备机器及有界通用先验构造精确的贝叶斯最优后验，用统一标准检验语言模型的上下文学习究竟接近算法归纳，还是主要依赖表面统计规律。

**不用术语来说**：给语言模型看几个输入输出例子后，即使它答对了新问题，也不能据此判断它是否真正推断出了生成规则，因为有限例子通常同时符合许多规则，而常见测试只检查最终答案，不说明模型依据当前证据本应给各种答案多大概率。研究所需的不是另一个答案集，而是一把能够精确衡量模型推断分布是否合理的标尺。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 将有界的 Levin–Solomonoff 归纳标准落实为可计算基准：作者穷举固定长度与运行预算内的程序，并据此精确计算少样本上下文下的贝叶斯最优后验，使语言模型输出的预测分布可以直接与规范性目标比较。
- 通过输出补码对称化的机器 $sF$ 以及原任务与逐位补码孪生任务，消除参考机器偏好零输出造成的极性混杂，并利用孪生任务上的表现差异识别模型自身的归纳偏置。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究语言模型的上下文学习，即模型仅根据提示中的少量输入—输出示例推断潜在规则，并对新输入或后续符号作出概率预测。判断这种能力是否属于算法推理，关键不只是检查最终答案是否正确，而是比较模型在当前证据下给出的完整预测分布与规范性最优分布是否一致；然而，常见基准通常只规定一个预期答案，无法说明有限示例究竟支持哪些假设。本文因此在一个可穷举的小规模计算系统中引入有界的通用先验：对图灵完备的五指令位带自动机 $F$ 的所有长度不超过 $13$ 的程序进行枚举，以程序长度决定先验权重，再对与示例一致的程序进行贝叶斯条件化。这样可得到精确而非近似的后验预测，并将其作为衡量语言模型算法归纳能力的标准。由于原始机器的全零初始纸带会造成输出极性偏置，实际基准使用补码对称化机器 $sF$，使任务及其逐位取反孪生任务具有相同的最优得分，从而把模型自身的归纳偏置与参考机器偏置区分开。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**上下文学习**

模型不更新参数，而是从当前提示中的少量示例临时推断任务规则，并将该规则用于新的查询。本文关注的不是模型能否偶然给出正确答案，而是其预测分布如何随示例增加而更新。

</div>
<div class="concept-item" markdown="1">

**贝叶斯后验预测**

先为每个候选程序分配先验概率，再排除所有与已观察示例矛盾的程序，最后汇总剩余程序对查询结果的概率质量。若任务确实由该先验中的程序生成，这一分布在期望对数损失意义下是贝叶斯最优的。

</div>
<div class="concept-item" markdown="1">

**有界通用先验**

Levin–Solomonoff思想倾向于给短程序更高权重，本文采用类似 $w(p)=2^{-\ell(p)}$ 的长度权重；其中程序越短，先验质量越大。一般的通用归纳不可计算，本文通过限制程序长度、运行步数和纸带规模，使指定范围内的先验及后验能够被穷举并精确计算。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

参考系统是位带自动机 $F$ 及其补码对称化版本 $sF$；程序长度限制为 $L\leq13$，每次运行最多执行 $1024$ 步并使用 $128$ 个纸带单元，概率归一化仅覆盖产生输出并停机的程序。穷举程序后，将它们在固定有序输入集合上的映射合并为行为 $b$，并累计得到每种行为的先验质量 $w(b)$。给定少样本证据集 $\mathcal{E}=\{(x_i,o_i)\}$ 和查询 $x_q$，只保留满足所有 $b(x_i)=o_i$ 的行为，再按其质量汇总查询结果 $s$ 的精确后验概率 $P(s\mid x_q,\mathcal{E})$。基准据此考查三类设置：归纳任务根据若干输入—输出对预测保留查询的输出；续写任务根据已显示的输出前缀预测 $\{0,1,\mathrm{end}\}$ 上的下一符号分布；溯因任务主要用于验证基准设计。每个任务还配有逐位取反的孪生任务，其理论最优得分相同，因此两者的表现差可用于识别语言模型的输出极性或表面模式偏好。需要注意，精确最优性是相对于有界 $F$ 先验而言；评测样本还经过输出长度、复杂度配额及可学习性筛选，所以该后验并非针对筛选后评测分布的无条件最优预测。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{E}=\{(x_i,o_i)\}$**

上下文中已经观察到的输入—输出示例集合，其中 $x_i$ 是第 $i$ 个输入，$o_i$ 是对应输出。

</div>
<div class="notation-item" markdown="1">

**$w(p)=2^{-\ell(p)}$**

程序 $p$ 的长度先验权重，$\ell(p)$ 表示程序编码长度；较短程序获得较大的先验质量。

</div>
<div class="notation-item" markdown="1">

**$w(b)$**

产生同一行为 $b$ 的全部程序的先验质量之和；行为是在固定输入集合上从输入到输出的映射。

</div>
<div class="notation-item" markdown="1">

**$P(s\mid x_q,\mathcal{E})$**

观察证据 $\mathcal{E}$ 后，查询输入 $x_q$ 的结果为 $s$ 的精确后验预测概率。

</div>

</div>

**直接相关的工作**

- **ARC 与 CLRS**: 二者通过规则归纳或算法执行任务评估推理能力，但通常只按单个预期答案评分，没有给出有限证据所许可的完整预测分布；本文的区别是以穷举程序得到的精确贝叶斯后验作为规范性目标。
- **面向 Solomonoff 归纳的元学习方法**: 相关方法从相近的 Brainfuck 系机器采样程序来生成训练流，但采样无法给出完整目标后验，因而只能依据对数损失的宽松上界比较模型；本文通过有界穷举直接计算后验，以获得可逐任务核验的精确标准。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

上下文学习被广泛用来衡量语言模型从少量示例中归纳任务并泛化到新输入的能力，但一次正确回答可能来自真正的规则推断，也可能来自与当前样例偶然吻合的前缀、频率或表面模式。若没有“这些证据应当支持什么预测分布”的可信标准，就无法比较模型利用证据的效率，也难以判断模型规模、训练方式或推理后训练是否真正改善了算法性归纳。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **可处理假设类上的贝叶斯式上下文学习分析**：相关研究把上下文学习解释为贝叶斯更新，但通常将候选规律限制在线性函数或参数化混合等便于解析的假设类中，再分析模型如何依据示例更新预测。此类方法能够提供明确计算，却不覆盖一般可计算程序所表达的循环、递归和组合算法。
- **算法推理与近似算法信息基准**：ARC、CLRS 等基准依据预设规则的唯一目标答案评估规则归纳或算法执行；SuperARC 使用近似复杂度评价抽象与递归预测；面向 Solomonoff 归纳的元学习方法则从相关程序机器采样训练序列，并以宽松的对数损失上界评估模型。它们分别测试任务正确性、压缩式抽象或对程序分布的近似学习。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 只按单一正确答案计分会忽略证据不足时多个假设仍然成立的事实，因此高准确率无法区分模型是否形成了正确的不确定性分布，也无法衡量其距离理想归纳还差多少。
- 通用的 Solomonoff 预测在一般情形下不可计算，而既有可计算替代方案依赖受限假设类、采样目标、近似复杂度或损失上界，因而不能把模型实际给出的分布与一个经过完整枚举、可复核的精确后验直接比较。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一个同时满足四项条件的评测对象：假设空间具有真实的算法表达能力；在明确资源边界内可以穷举；每个少样本上下文都有精确而非近似的规范性后验；评测还能控制参考机器自身的输出偏置。这个缺口使“模型是否按算法先验进行证据更新”长期只能通过答案准确率或代理指标间接判断。

</div>
<div markdown="1"><span>核心问题</span>

在相同可见证据下，语言模型提供的完整预测分布与有界通用程序先验所规定的精确贝叶斯最优后验有多接近；这种接近程度是否会随示例增加而稳定改善，并能否与低阶表面统计、输出极性偏好及单纯的答案准确率区分开来？

</div>
<div markdown="1"><span>作者直觉</span>

作者选择一台足够小但仍图灵完备的机器 $F$，把无限且不可计算的通用归纳问题缩到固定程序长度和运行预算内，于是可以逐个统计所有候选程序对观察证据与查询答案贡献的先验质量。直观上，这相当于不猜测“合理规则”有哪些，而是在边界内把所有短程序全部清点，再检查模型是否像理想的证据加权器一样分配概率；补码对称化与孪生任务则让参考标准对 $0$ 和 $1$ 一视同仁，使剩余差异更能归因于模型的归纳倾向。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

F-ICL先把一个通常不可计算的规范性问题限制到可穷举范围：在固定的图灵完备参考机 $F$ 上，只考虑长度不超过 $13$ 的程序，并限制每次执行最多使用 $1024$ 步和 $128$ 个纸带单元。系统对这些程序进行穷举，以长度较短者获得更高权重的有界 Levin–Solomonoff 先验汇总程序质量；由此得到“行为到先验质量”的完整表。给定若干输入输出示例后，只需保留与全部示例一致的行为，再按其先验质量归一化，就能精确计算查询输出的后验预测分布。为消除参考机全零初始纸带造成的输出极性偏差，实际基准使用补码对称化机器 $sF$，并为每个任务生成逐位取反的孪生任务。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 限定参考机与可计算程序空间

固定程序长度上限 $L\leq13$、运行上限 $1024$ 步和空间上限 $128$ 个单元，并明确停机输出的归一化规则。该限制把一般情况下不可计算的 Solomonoff 归纳转化为一个有限、可穷举的推断问题。

<div class="method-step__io" markdown="1">

**输入**：五指令位纸带自动机 $F$、候选二进制输入集合，以及程序长度、运行步数和纸带空间预算。<br>
**输出**：有限程序集合、确定性的执行语义，以及每个程序在各输入上的停机状态、输出和停机时间。

</div>

**直观理解**：可以把它理解为先规定一种极小编程语言，再把允许编写的程序长度和运行资源封顶。这样虽然不再覆盖所有可计算程序，却能逐个检查预算内的每一种解释。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 穷举程序并汇总行为质量

在所有指定输入上执行每个程序，把产生相同输入输出映射的程序合并为同一行为 $b$，并将这些程序的先验权重相加为 $w(b)$。归纳任务采用仅依赖长度的权重；随着证据逐步累积的任务还采用包含 Elias-$\delta$ 停机时间编码的 Levin 式权重。

<div class="method-step__io" markdown="1">

**输入**：预算内的全部 $F$ 程序、固定且有序的输入集合，以及长度或长度加停机时间的先验权重。<br>
**输出**：行为到总先验质量的表，以及可用于多示例查询的完整程序索引。

</div>

**直观理解**：多个不同程序可能做出完全相同的回答，因此基准不必在查询时反复检查每个程序。它预先把“表现相同的解释”装入同一组，并统计这一组总共有多少先验可信度。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 补码对称化并构造孪生任务

将机器补码对称化为 $sF$，使一个行为及其逐位补码在规范性标准中获得镜像质量；同时把每个原任务配成输出逐位取反的孪生任务。由于最优标准在原任务和孪生任务上应给出相同分数，两者的模型表现差可归因于模型自身的输出极性偏置。

<div class="method-step__io" markdown="1">

**输入**：原始机器 $F$ 所诱导的行为质量及其对零输出的结构性偏好。<br>
**输出**：去除已知零偏置的对称先验、原任务与补码孪生任务，以及镜像相等的精确最优目标。

</div>

**直观理解**：原始纸带全为零，会让输出零的短程序天然更便宜。对称化相当于同时考虑一套颜色完全反转的世界，避免把参考机的初始设置误当成模型应学习的规律。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按可见证据计算精确后验

筛选所有满足每条示例约束 $b(x_i)=o_i$ 的行为，再按 $w(b)$ 对其质量归一化；对候选结果 $s$，累加同时满足 $b(x_q)=s$ 的一致行为质量。由于程序空间已被完整穷举，该计算是固定预算和固定先验下的闭式精确后验，而不是蒙特卡洛估计。

<div class="method-step__io" markdown="1">

**输入**：示例集 $\mathcal{E}=\{(x_i,o_i)\}$、查询输入 $x_q$，以及行为质量表 $w(b)$。<br>
**输出**：查询结果的 Bayes 最优分布 $P(s\mid x_q,\mathcal{E})$，或续写任务中每个位置对 $\{0,1,\mathrm{end}\}$ 的精确条件分布。

</div>

**直观理解**：先删掉所有与已知例子矛盾的程序解释，再让剩余解释按“短且适当快”的程度投票。例子增加时，投票者会逐渐减少，因此可以观察模型是否像这个理想推断器一样利用新证据。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 程序先验与行为质量

$$
w(p)=2^{-\ell(|p|)},\qquad w(b)=\sum_{p:\,\operatorname{beh}(p)=b}w(p)
$$

**符号说明**

- $p$：预算内的一个参考机程序。
- $|p|$：程序的指令长度。
- $\ell(|p|)$：用于先验加权的程序长度编码长度；原文将其写入有界通用先验。
- $w(p)$：程序 $p$ 的先验权重，随编码长度指数衰减。
- $b$：程序在固定有序输入集合上表现出的完整输入输出行为。
- $\operatorname{beh}(p)$：程序 $p$ 在指定输入集合上诱导的行为；此记号用于表达原文所述的程序到行为归并。
- $w(b)$：所有诱导行为 $b$ 的程序权重之和，是后续 Bayesian 推断所需的充分统计量。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分实现奥卡姆原则：程序每增加编码长度，其先验权重便指数下降。第二部分把功能相同的程序权重相加，因此后验关心的是一种输入输出规律获得了多少总程序质量，而不是任意挑选一个代表程序。<br>
**原文位置**：图 1、结果 §2.1；程序权重及行为质量对应 Methods Eq. (4)，源摘录未完整展示 Eq. (4) 的排版。

</div>

</div>

<div class="equation-block" markdown="1">

#### 一致行为上的精确后验预测

$$
P\!\left(s\mid x_q,\mathcal{E}\right)=\frac{\sum_{b\,\text{consistent},\,b(x_q)=s}w(b)}{\sum_{b\,\text{consistent}}w(b)}
$$

**符号说明**

- $\mathcal{E}=\{(x_i,o_i)\}$：提示中已经给出的输入输出示例集合。
- $x_i$：第 $i$ 条示例的输入。
- $o_i$：第 $i$ 条示例中观察到的输出。
- $x_q$：需要预测的查询输入。
- $s$：查询的一个候选输出；在续写条件分布中可对应 $0$、$1$ 或结束符。
- $b$：一个候选程序行为；一致性要求对所有示例均有 $b(x_i)=o_i$。
- $w(b)$：行为 $b$ 在有界程序先验下的总质量。
- $P(s\mid x_q,\mathcal{E})$：看到示例集后，查询输入产生候选结果 $s$ 的后验预测概率。

<div class="equation-explanation" markdown="1">

**直观理解**：分母汇总所有没有被示例排除的解释，分子只汇总其中还会在查询上输出 $s$ 的解释；两者相除就是这些一致解释对 $s$ 的归一化支持度。穷举的完整性使该概率在给定机器、预算和权重约定下是精确值，因此模型与它的非零距离不是采样噪声。<br>
**原文位置**：结果 §2.1，Eq. (1)。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：F-ICL不是训练语言模型的方法，也不通过目标函数更新被测模型参数。它固定参考机、程序预算和先验，离线计算规范性后验；评测阶段把模型所服务的预测分布与该后验比较。Jensen–Shannon 散度在这里是评价量而非反向传播损失，源摘录只说明 F-ICL-A 由最差预测器、按键参照和 Bayes 最优三个点锚定，未给出 Methods Eq. (20) 的完整公式，因此不在此补造。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 有界通用程序枚举器**

该模块穷举长度 $L\leq13$ 的五指令 $F$ 程序，在固定输入集上执行并记录输出、停机时间和程序身份；生产实现使用 GPU 加速，独立的无依赖纯 Python 解释器用于语义与计数核验。程序的基础权重随描述长度指数衰减，即较短程序具有更大先验质量。

> 直观理解：它是规范性标准的离线建造器：昂贵计算只做一次，冻结出的行为表和程序索引随后可被许多模型共享。独立慢实现的作用类似用不同方法复算答案，降低加速器错误被误当成模型误差的风险。

**2. 精确后验服务与认证模块**

该模块从行为质量表或完整程序索引筛选与当前证据一致的行为，并返回精确归一化后的预测分布。认证链包括逐输入输出程序计数的逐字节一致、见证程序重执行、程序身份集合一致，以及小程序穷举联合分布与生产服务后验在 $0$ 至 $5$ 个示例范围内逐位一致。

> 直观理解：枚举结果正确并不自动保证在线查询也正确，因此作者分别检查“程序是否真的存在”“程序集合是否遗漏”和“最终概率是否算对”。只有各条独立路径精确一致，构建结果才被接受。

**3. 任务与分布评分模块**

模块支持归纳和续写两类计分任务，并以溯因任务验证设计；所有计分目标均来自同一固定先验下的精确后验。模型分布通过有界对称散度与最优分布比较，同时拆分终止符与比特坐标，并利用补码孪生任务检查输出极性偏置。

> 直观理解：不同任务考察的是同一件事的不同切面：能否从示例推断输入输出规则，以及能否在序列逐步展开时正确更新概率。单独观察结束符很重要，因为序列何时停止可能主导总体差异，而掩盖模型对零和一的判断。

**训练与推理**

基准构建阶段首先枚举预算内全部程序，在指定输入集合上执行并按行为归并，再依据任务族选择长度权重或包含 Elias-$\delta$ 停机时间编码的质量时间权重；随后进行补码对称化，冻结行为质量、程序索引、任务及其精确目标。该过程不使用被测模型的数据或输出调参，因而目标对模型是外生的。推理评测阶段按顺序向模型揭示示例或序列前缀，在每个证据水平读取其完整预测分布，并与相同证据条件下的 $sF$ 后验比较；原任务与补码孪生任务使用镜像提示，从二者差异中分离模型自身的归纳偏置。

**复现信息**

公平解释结果所必需的固定约定是：参考标准使用补码对称化机器 $sF$；程序长度为 $L\leq13$；单次执行限制为 $1024$ 步和 $128$ 个纸带单元；概率在停机输出上归一化；归纳任务采用仅依赖程序长度的权重，而积累证据的任务采用长度加 Elias-$\delta$ 停机时间编码的 Levin 式权重。作者称共穷举约 $15$ 亿个程序。生产后端使用完整预算程序索引，另有小程序精确联合分布作为度量兼容的交叉检查后端；冻结数据写出时还检查孪生镜像相等、概率归一化和首位置概率定律。需要注意，该后验只对固定的有界 $F$ 先验是 Bayes 最优，并非对经过输出长度、复杂度配额及可学习性门控筛选后的评测样本分布自动最优；因此指标衡量的是对指定算法先验的忠实度，而不能直接等同于在策展数据上的最低预测误差。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 核心评测集由完整程序库中选出的$120$个归纳任务组成；每个任务在多个示例数下评测，共形成$1{,}080$个任务—shot单元。每项任务还配有逐位取反的孪生任务，用于控制输出极性偏差。实验所需的精确目标分布由穷举长度$L\leq13$的程序得到，而本次模型面板对应的隐藏程序处于$L\leq6$范围。
- 模型面板覆盖开放权重模型和多家实验室的专有系统。论文摘要报告$105$种服务配置、$37$个开放模型及四家实验室的前沿系统；在正文主要分布评测中，最终有$46$个不同模型、$81$次运行提供可用的对数概率，答案侧分析还包含只能返回答案而不能提供完整分布的运行。
- 续写评测在输出的九个已揭示位置逐位置读取三类候选的概率，用于判断模型是否学到了程序生成的条件分布，并特别分离终止符坐标。重新服务后的本地模型在全部$1{,}736$个相关单元上均能解析三个类别。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**归纳答案正确率**

比较模型给出的离散答案与任务真实输出，主要报告最终shot及随示例数变化的学习曲线。它衡量是否答对，但不能判断模型的置信分布是否符合贝叶斯后验。 （越高越好；$1$表示所有任务均答对。）

</div>
<div class="metric-item" markdown="1">

**Jensen–Shannon散度**

衡量模型服务得到的候选输出分布与精确最优后验之间的差异，单位为bit；该指标对称且可用于比较逐位置续写分布。 （越低越好；$0$表示模型分布与最优后验完全一致。）

</div>
<div class="metric-item" markdown="1">

**锚定F-ICL-A**

将模型对算法最优后验的分布忠实度放到以按键参考为锚点的统一尺度上，用于跨模型比较。它关注整个分布，而不是只看概率最大的答案。 （越高越好；低于按键参考表示模型比该弱参考距离最优后验更远，贝叶斯最优预测器构成上界。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 随上下文示例增加的归纳学习曲线，比较模型面板均值与精确最优预测器。

<div class="result-value" markdown="1">

最优预测器在四个示例时正确率已达$0.98$，五个示例时达到$1.0$；模型面板到八个示例时平均正确率仅为$0.62$。此外，$81$次可用分布运行中有$69$次在看到一个示例后反而比零示例时具有更大的后验散度，符号检验为$p<10^{-9}$。

</div>

模型能够从示例中提高答题率，但其证据利用速度明显慢于精确推断，而且首个样本常导致过度承诺。该结果说明模型的上下文更新轨迹不像此任务上的贝叶斯后验；它并不单独证明模型在所有推理任务中都不执行算法。

<div class="result-source" markdown="1">

来源：Figure 4及“The measurement, made concrete.”小节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The optimum locks onto the truth quickly: its induction accuracy is 0.98 by four examples and exact by five. The panel, in contrast, rises slowly and plateaus far short (mean accuracy 0.62 at eight examples; Fig. 4a), leaving a large and persistent shortfall.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 在最终shot上比较答案正确率与锚定F-ICL-A，并以按键参考及经典统计基线定位分布差距。

<div class="result-value" markdown="1">

在$81$次具有可用对数概率的运行中，$78$次运行、即$46$个模型中的$45$个低于按键参考；模型最高答案正确率可达$92\%$，但正确率与后验忠实度的Spearman相关仅为$\rho=-0.19$、$p=0.21$。九个续写位置上的面板平均散度为$0.29$至$0.50$ bit，始终高于按键参考的$0.19$ bit。

</div>

答对和以正确概率理由答对是两件事：模型可以选中真实答案，却仍把大量概率放在不符合程序后验的候选上。低阶前缀统计基线与模型处于相近区间，支持“模型行为更像局部模式统计”的解释；但这只是相对于本基准参考机器和候选空间的结构性证据，不能直接识别模型内部实际执行了哪种算法。

<div class="result-source" markdown="1">

来源：Figure 5a及“Models track accuracy but are confidently far from the posterior.”小节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Models reach up to 92% accuracy yet cluster below the keystroke reference (78 of 81 runs; two-sided sign test p<10−9): answering well does not imply reasoning like the optimum.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 检查同一任务在加入下一个无噪声示例后，是否从已解决变为未解决。

<div class="result-value" markdown="1">

在$98$次完整运行中，新增示例造成$6{,}545$次“已解决到未解决”转移，而“未解决到已解决”为$13{,}702$次；每次运行的遗忘事件中位数为$66$，并且所有曾被解决的运行—任务对中有$24\%$在八个示例后以错误结束。

</div>

在该可实现、无噪声设置中，理想贝叶斯预测器的已解决集合应随证据单调扩大；大量反向转移表明模型不能稳定维持已获得的假设。该统计描述的是行为非单调性，不等于证明模型没有任何内部记忆，也不能排除提示格式和服务过程对个别转移的影响。

<div class="result-source" markdown="1">

来源：“In-context learning is non-monotone: models un-solve tasks.”小节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The panel’s is not: across the 98 complete runs, additional examples produce 6,545 solved→unsolved transitions against 13,702 gains (one forgetting event per two learnings, a median of 66 per run on 120 tasks), and 24% of ever-solved (run, task) pairs end wrong at eight examples.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 参考机器互换实验只验证了当前面板使用的较短程序任务；论文明确指出隐藏程序长度$7$至$9$的扩展困难区间尚未对任何模型评分，因此现有结论主要适用于当前长度和任务分布。
- 概率读取仍受服务接口限制。修复后本地行可解析全部三类，但API行仍存在概率下限并列，$24$行中有$14$行在至少$5\%$的单元上发生该现象，最高为$17.2\%$；这种残留会轻微抬高受影响模型的表现，并削弱同一供应商内部精细排序的可靠性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 精确贝叶斯最优预测器：由可计算的程序混合后验得到，是评测目标而非待训练模型；在可实现、无噪声条件下，它给出正确归纳应达到的答案与概率分布。
- 按键参考（keystroke reference）：一种不利用当前证据的弱参考，其本质是由无循环、仅打印机器诱导的算法混合。它用于判断模型分布至少是否比简单的“按键式”生成机制更接近带循环机器的最优后验。
- 输入无关频率基线：包括全数据集输出频率和按shot汇总的最优分布，分别达到$0.60$和$0.73$的F-ICL-A。它们利用冻结后的最优分布构造，因此不是可部署竞争者，而是衡量模型遗漏了多少与具体任务无关的总体结构。
- Krichevsky–Trofimov前缀统计基线：在可见前缀上拟合加$rac{1}{2}$估计器，包括无记忆模型和一阶二元模型。它们代表只学习局部符号频率或相邻转移、不执行程序归纳的模式补全策略。

**实验想回答的问题**

- 随着上下文示例从零逐步增加，语言模型的答案正确率和输出分布是否会收敛到由有界通用先验给出的精确贝叶斯最优预测？
- 模型与最优后验之间的差距能否由模型规模、答案正确率或简单序列统计解释；新增证据是否像贝叶斯更新那样稳定改善推断？

**实验实现**

评测按证据量逐步向模型展示最多八个上下文示例，并在相同候选集合上记录离散答案与对数概率；所有运行都与同一冻结的最优后验比较。主要曲线覆盖零至八个示例和九个续写位置。统计分析包括任务自助法置信区间、符号检验、Spearman或Pearson相关、Cohen的$\kappa$及难度分桶。服务管线另设近均匀分布、top-$k$截断造成的概率并列、空回复和模板映射错误审计；失败的答案侧运行被排除出相应准确率分析，而无法取得可靠三类概率的运行不进入分布忠实度分析。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 用交换后的参考机器最优分布重新计算全部已存模型分布，以检验结论是否依赖具体机器和加权约定。 | 两种最优分布在$1{,}080$个任务—shot单元上的平均Jensen–Shannon散度为$0.028$ bit，MAP答案一致率为$98\%$；对$81$次模型运行重新评分后，F-ICL-A排名相关为$0.975$、平均绝对变化为$0.015$，且两种工具下均有$80$次可计算宏观分数运行中的$77$次低于按键参考。 | 该稳健性实验隔离了参考机器、程序权重和枚举预算对排名的影响。极高的排名一致性说明主要结论不是某一种编码约定偶然造成的；但它没有覆盖隐藏程序长度为$7$至$9$的更难扩展任务，因此不能外推到该范围。 | 参考机器等价性与robustness tool分析段落<br><span class="experiment-evidence">Models are tested equivalently: rescoring every stored model distribution against the swapped optima on identical candidate sets reproduces the per-run F-ICL-A(induction) with rank correlation 0.975 (mean absolute change 0.015, n=81 runs), and the headline count is unchanged, 77 of 80 macro-scored runs below the keystroke reference under either instrument (one of the 81 log-probability runs, the retired mistral row, has no continuation leg and so no macro score).</span> |
| 提高本地服务的top-$k$概率采集深度，重新服务出现类别概率并列的四个失败行及共享配置的全部十九行。 | 修复后十九行在全部$1{,}736$个单元上都能区分三个类别；其中十四行的散度变化小于$0.01$ bit。最大变化出现在Qwen3-30B-A3B-Instruct，其续写散度上升$0.096$ bit，F-ICL-A由$0.343$降至$0.308$。 | 该消融隔离的是概率采集工具而非模型能力：过小的top-$k$会把未返回类别统一填成平滑下限，制造虚假的相同分数。修复总体不改变大多数行，但会显著修正个别模型，并扩大而非制造相应的后训练性能下降，因此审计是主结论可信度的重要前提。 | 服务概率退化审计与top-k修复段落<br><span class="experiment-evidence">The repair moves fourteen of the nineteen rows by less than 0.01 bits; the largest move is Qwen3-30B-A3B-Instruct, whose continuation divergence rises by 0.096 bits and whose F-ICL-A falls from 0.343 to 0.308, which was 94% tie-degenerate and is the middle rung of one of the two post-training triads, so the repair enlarges that triad’s base-to-instruct drop rather than creating it.</span> |

**定性案例**

- 错误解剖显示，限定在后验支持非退化的任务—shot单元上，错误答案中$31\%$在截断且以停机为条件的程序支持下具有零后验质量，$46\%$连输出长度都不正确；另有$41\%$直接复制已展示的输出，到八个示例时该比例升至$70\%$，而仅$2.8\%$是Occam式Bayes-MAP答案。作者据此主张错误更符合复制和近邻模式补全，而不是单纯偏好最简单程序；分析上，这也解释了为何准确率可能上升而完整后验仍不正确。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces an exact Bayes-optimal benchmark for evaluating in-context algorithmic reasoning in language models.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`0879c4a5d8fb7e269b291e7cc609574fbc01dc9027207352fcf4271dcb1f959c`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
