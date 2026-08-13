---
title: "[论文解读] Claim-Level Reliability Assessment for Efficient Test-Time Reasoning"
description: "[arXiv 2608.11994][LLM Reasoning] 本文提出免训练的声明级可靠性评估框架（CLR），把部分测试时计算从重复生成完整解答转向核验决定答案正确性的关键声明，再依据核验结果加权聚合候选答案。"
arxiv_id: "2608.11994"
announcement_date: "2026-08-13"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-13T02:51:49.265086+00:00"
source_sha256: "ffcdd30e0c01d4ea0d88e1ae2c15deeb87157c034ec94dce6fe8e7e621c23cb8"
tags:
  - "LLM Reasoning"
  - "大语言模型"
  - "测试时扩展"
  - "主张级可靠性评估"
  - "语义证伪"
  - "自一致性"
  - "可靠性加权聚合"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.11994</p>

# Claim-Level Reliability Assessment for Efficient Test-Time Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-13</span>
<span><strong>作者</strong> Sen Xu, Wei Wang, Shixi Liu, Jixin Min, Yingwei Dai, Zhibin Yin, Yirong Chen, Junlin Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Sina Weibo Inc</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.11994v1) · [PDF 下载](https://arxiv.org/pdf/2608.11994v1) · **关键词** 大语言模型, 测试时扩展, 主张级可靠性评估, 语义证伪, 自一致性, 可靠性加权聚合<br>


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

本文提出免训练的声明级可靠性评估框架（CLR），把部分测试时计算从重复生成完整解答转向核验决定答案正确性的关键声明，再依据核验结果加权聚合候选答案。

**不用术语来说**：大语言模型在解题时多生成几份答案并进行投票，通常能提高正确率，但多数答案也可能共享同一种错误；同时，一整段推理中的大量常规文字会掩盖少数真正致命的逻辑问题。因此，有限的推理预算未必应该全部用于继续生成答案，还需要一种成本可控、能够集中检查关键错误的方法。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出“声明级证伪”这一测试时扩展原则：将完整推理压缩为少量决定结论的关键声明，并主动寻找能够推翻这些声明的反例或逻辑缺陷，以获得比整体置信度更直接的可靠性信号。
- 将该原则实现为免训练的CLR框架：使用同一基础模型完成候选解答生成与独立声明核验，并通过非线性可靠性评分进行加权聚合，使经核验的可靠少数有机会纠正错误多数。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型的测试时扩展研究：在不更新模型参数的前提下，通过增加推理阶段的计算来提高复杂推理的正确率。典型方案包括依据词元概率、熵或隐藏状态评估单条推理轨迹的不确定性，采样多条轨迹后进行答案聚合或 Best-of-N 选择，以及利用显式评价信号执行分支、剪枝和回溯。本文关注其中的共识式答案聚合，但指出额外采样只有在可靠性信号足够准确且有区分度时才有效；如果多条高置信度轨迹共享同一关键错误，简单多数投票可能形成“错误共识”。为此，论文把评估粒度放在完整轨迹与逐步验证之间：从每条轨迹中提取少量决定答案正确性的主张，再针对这些主张寻找反证，以减少常规推理词元造成的信号稀释。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试时扩展（test-time scaling）**

模型参数保持不变，在回答问题时投入更多采样、搜索或验证计算，以换取更可靠的输出。本文研究如何重新分配固定推理预算，而不是训练一个能力更强的新模型。

</div>
<div class="concept-item" markdown="1">

**自一致性（self-consistency）**

对同一问题独立生成多条推理轨迹，并按最终答案的出现次数进行聚合，通常以多数票作为预测。它能降低偶然采样错误，但无法保证多数轨迹在逻辑上正确。

</div>
<div class="concept-item" markdown="1">

**可证伪的决策关键主张**

决策关键主张是从推理轨迹中提炼出的、直接支撑最终答案的少量语义命题；“可证伪”表示验证过程主动寻找足以推翻命题的反例、矛盾或关键漏洞。直观上，完整构造正确解需要所有关键环节都成立，而否定错误主张通常只需发现一个致命问题。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个需要推理的问题，以及同一基础模型在该问题上独立采样得到的 $K$ 条解题轨迹；每条轨迹同时附带一组紧凑的决策关键主张。系统不更新参数，也不依赖单独训练的过程验证器，而是让同一模型仅依据原问题和提取出的主张进行独立核验，再把主张级判定映射为非线性的轨迹可靠性分数，并据此对候选答案加权聚合，输出一个最终答案。比较采用匹配模型调用预算的设置：$\mathrm{CLR}@K$ 使用 $K$ 次解答生成和 $K$ 次主张验证，共 $2K$ 次调用；$\mathrm{Cons}@2K$ 则把相同调用预算全部用于生成 $2K$ 条解答轨迹。该设置要检验的核心问题是：在固定测试时预算下，把一部分计算从重复解题转向定向证伪，是否比单纯增加样本更能识别高置信度但含有致命错误的轨迹。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$K$**

CLR 第一阶段采样的解题轨迹数量，也是第二阶段执行主张验证的调用数量。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{Cons}@K$**

使用 $K$ 条独立采样轨迹进行自一致性答案聚合的方法。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{CLR}@K$**

对 $K$ 条轨迹生成决策关键主张并分别验证，再进行可靠性加权答案聚合的方法。

</div>
<div class="notation-item" markdown="1">

**$2K$**

CLR 的总模型调用数；在预算匹配比较中也对应自一致性方法生成的轨迹数量。

</div>

</div>

**直接相关的工作**

- **Self-Consistency**: 它是本文最直接的共识聚合基线：通过增加独立解题样本并按答案频次投票提高稳定性。CLR 保留多轨迹聚合框架，但用一半预算验证关键主张，并以可靠性加权取代仅依赖票数的聚合，使可靠的少数轨迹有机会推翻错误多数。
- **Step-level Verification**: 逐步验证可以定位推理中的局部错误，但原文指出这种方法通常计算开销大，并需要过程级监督或单独训练的验证器。CLR 采用更粗但更集中的主张级粒度，试图在完整轨迹评价的信号稀释与逐步评价的高成本之间取得平衡。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

测试时扩展希望在不更新模型参数的情况下，用额外推理计算提升复杂任务的正确率。然而，随着预算增加，系统仍难以判断哪些候选推理真正可信，导致新增计算可能只产生更多相似答案，甚至强化由多个高置信错误解答形成的错误共识。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **整条推理的内在置信度评估**：利用词元概率、熵或隐藏状态等模型内部统计信号，为一条完整推理估计总体不确定性，再据此选择或排序答案。
- **多轨迹聚合与生成中搜索**：前者并行采样多条解答，通过自一致性投票或Best-of-N选择最终答案；后者在生成过程中借助评价信号执行分支、剪枝或回溯，尝试搜索出更可靠的推理路径。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 统计置信度不能等同于逻辑正确性，而整条推理中的大量常规步骤会稀释可靠性信号，使局部但致命的错误被看似流畅、整体高置信的文本掩盖；结果是系统难以区分真正正确的轨迹与自信但错误的轨迹。
- 逐步核验虽然能定位局部错误，却需要近乎穷举地检查推理步骤，通常还依赖过程级监督或单独训练的验证器；仅增加采样和多数投票则无法有效处理多个轨迹共享同一错误的情形，计算成本增加也未必带来同等幅度的可信度提升。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种介于整条推理评价与逐步核验之间的评价粒度：它既要直接覆盖决定最终答案的语义依据，又要避免检查所有词元或步骤，并且最好无需额外训练验证器。尚未解决的关键缺口是，如何在固定测试时预算内从候选推理中提取高区分度的可靠性信号，并用该信号抑制错误共识。

</div>
<div markdown="1"><span>核心问题</span>

能否把部分用于继续采样完整解答的测试时计算，重新分配给少量决策关键声明的独立证伪，并依据证伪结果进行可靠性加权聚合，从而在相同模型调用预算下获得比普通自一致性投票更可信的最终答案？

</div>
<div markdown="1"><span>作者直觉</span>

构造一个完全正确的解答要求整条推理链都成立，但推翻一个错误声明通常只需找到一个决定性反例或逻辑漏洞。CLR利用这种“构造难、证伪相对容易”的不对称性：先删去不影响结论的常规文字，只保留推理的逻辑支点，再让模型集中寻找反对证据。这样，验证预算被投入最可能改变答案判断的位置；一条轨迹只要关键声明暴露严重问题，其聚合权重就会被显著压低，而少数经受住核验的答案可以超过表面上的多数。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CLR 是一个无需训练的两阶段测试时推理框架。给定问题 $q$ 和采样数 $K$，第一阶段用同一语言模型独立生成 $K$ 条完整推理轨迹，并要求每条轨迹同时给出最终预测 $y_k$ 与恰好 $M$ 个决定性主张 $C_k=(c_{k,1},\ldots,c_{k,M})$；第二阶段不再生成新解，而只根据问题和这些主张寻找反例、矛盾或推理缺口。每条轨迹随后依据未被证伪的主张比例获得非线性可靠性分数 $r_k$，语义等价的预测被分组并累加可靠性，支持度最高的组给出最终答案 $\widehat{y}$。
直观地说，普通自洽方法把每条解答都视为一票，容易让许多具有相同错误的解答形成错误多数；CLR 则先从长推理中抽取真正支撑答案的若干“承重点”，再有针对性地检查这些点。发现一个决定性错误不需要重新构造完整正确解，因此有限的测试时计算被用于削弱可疑候选，而不是继续增加同权重样本；但它只能在第一阶段已经采到的答案中重新选择，不能创造缺失的正确答案。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 采样完整推理并提取决定性主张

对问题独立发起 $K$ 次第一阶段请求；第 $k$ 次请求生成完整推理轨迹 $t_k$、任务特定结构化格式的最终预测 $y_k$，以及有序主张列表 $C_k=(c_{k,1},\ldots,c_{k,M})$。每个主张必须是其失败会动摇预测的中间结论、约束、变换、决策点或证据连接，而不能只是摘要或答案复述。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、解答采样数 $K$、固定解码配置以及预设主张数 $M$。<br>
**输出**：$K$ 个三元组 $(t_k,y_k,C_k)$，其中每个 $C_k$ 恰含 $M$ 个简洁主张。

</div>

**直观理解**：这一阶段既写出候选解，也把长篇解答压缩成固定数量的关键支点。后续检查因此不必在大量常规文字中寻找少数真正决定答案的错误。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 逐轨迹联合证伪

复用同一模型，通过一次联合的第二阶段请求检查该列表中的全部主张，搜索决定性矛盾、反例、事实或逻辑错误、缺失条件、无依据推断以及主张间冲突。若主张 $c_{k,m}$ 被找到决定性缺陷，则令 $v_{k,m}=0$，否则令 $v_{k,m}=1$。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$ 与某条轨迹的有序主张列表 $C_k$；原始轨迹 $t_k$ 和最终预测 $y_k$ 不作为第二阶段的独立输入。<br>
**输出**：每条轨迹对应的二值判定向量 $(v_{k,1},\ldots,v_{k,M})$。

</div>

**直观理解**：检查器只需要找到一个足以否定主张的缺陷，不需要证明整个解答正确或另写一份完整答案。因而“未被证伪”只表示本次检查没有找到错误，不等同于形式化正确性证明。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算轨迹可靠性

先计算存活比例 $s_k=\frac{1}{M}\sum_{m=1}^{M}v_{k,m}$，再取 $r_k=s_k^M$。当 $M>1$ 时，该幂变换相较线性平均会更强地压低含有被证伪关键主张的轨迹，但作者明确将其视为启发式分数，而非联合正确概率。

<div class="method-step__io" markdown="1">

**输入**：主张判定向量 $(v_{k,1},\ldots,v_{k,M})$ 与主张数 $M$。<br>
**输出**：每条可解析轨迹的非负可靠性分数 $r_k$。

</div>

**直观理解**：不是简单地按“通过了几个检查”线性打分，而是让关键错误带来更重的扣分。这样，数量很多但各自存在明显缺陷的解答不会轻易凭票数压过较少却更可靠的解答。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 等价分组与可靠性加权选择

丢弃无法解析出预测的轨迹，将其余预测划分为等价组集合 $\mathcal{G}$；对每组 $G$ 累加组内轨迹分数得到 $R(G)$，再选择支持度最大的组并输出其规范化答案。若并列或所有组分数均为零，则选择采样顺序中最早出现的等价组。

<div class="method-step__io" markdown="1">

**输入**：可解析预测集合 $\{y_k\}$、对应分数 $\{r_k\}$，以及任务适用的答案等价判定规则。<br>
**输出**：最终预测 $\widehat{y}$，且必有 $\widehat{y}\in\{y_k:y_k\text{ 可解析}\}$。

</div>

**直观理解**：相同含义的答案共同累积分数，但每条解答的票重由证伪结果决定。该步骤只改变已有候选的影响力，因此第一阶段没有采到正确答案时，CLR 无法补救候选覆盖不足。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 主张证伪判定与轨迹可靠性

$$
v_{k,m}=\begin{cases}0,&\text{refuted, if a decisive flaw is found},\\1,&\text{not refuted, otherwise},\end{cases}\qquad s_k=\frac{1}{M}\sum_{m=1}^{M}v_{k,m},\qquad r_k=s_k^M=\left(\frac{1}{M}\sum_{m=1}^{M}v_{k,m}\right)^M
$$

**符号说明**

- $k$：轨迹索引，取值对应第一阶段采样得到的第 $k$ 条轨迹。
- $m$：决定性主张索引，满足 $1\le m\le M$。
- $M$：每条轨迹固定提取的决定性主张数量，同时也是可靠性幂函数的指数。
- $v_{k,m}$：第 $k$ 条轨迹中第 $m$ 个主张的二值证伪结果；找到决定性缺陷时为 $0$，否则为 $1$。
- $s_k$：第 $k$ 条轨迹中未被证伪主张所占的比例。
- $r_k$：第 $k$ 条轨迹的非线性可靠性分数。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分把证伪结果变成二值信号，第二部分统计一条轨迹有多少关键主张存活，最后用 $M$ 次幂放大不完整存活带来的惩罚。例如存活比例低于 $1$ 时，取幂后的分数会比线性比例更小；该值只用于排序和加权，不应解释为轨迹正确的概率。<br>
**原文位置**：第 2 节 Falsification-Based Claim Assessment，式 (1)；Reliability Scoring and Aggregation，式 (2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 等价答案组的可靠性加权聚合

$$
R(G)=\sum_{k:y_k\in G}r_k,\qquad \widehat{y}=\operatorname{canon}\!\left(\underset{G\in\mathcal{G}}{\arg\max}\;R(G)\right)
$$

**符号说明**

- $y_k$：从第 $k$ 条轨迹中解析出的最终预测。
- $\mathcal{G}$：按照任务适用的语义等价标准形成的预测等价组集合。
- $G$：集合 $\mathcal{G}$ 中的一个预测等价组。
- $R(G)$：等价组 $G$ 的总可靠性支持，即组内所有轨迹可靠性分数之和。
- $\operatorname{canon}(G)$：等价组 $G$ 对应的规范化候选答案。
- $\widehat{y}$：最终输出的规范化预测。

<div class="equation-explanation" markdown="1">

**直观理解**：语义相同但表面形式不同的预测先归入同一组，再把支持该组的轨迹分数相加。最终选择总可靠性最高的答案组，因此决策依据是“可靠支持量”而不是原始出现次数；当所有分数相同时，它与普通多数投票等价。<br>
**原文位置**：第 2 节 Reliability Scoring and Aggregation，式 (3)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。CLR 是 training-free 框架，不更新模型参数，也没有通过反向传播优化的训练损失；式 (1) 至式 (3) 是测试时判定、启发式赋权和答案选择规则。这里的“目标”是将额外测试时计算用于寻找否定性证据，以降低高置信错误轨迹对共识的影响，而不是学习一个新的验证器。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 决定性主张压缩器**

第一阶段在生成轨迹与预测的同时，输出固定长度的语义表示 $C_k$；其中仅保留会实质影响 $y_k$ 的中间结论、约束、决策或证据链环节。固定为恰好 $M$ 个主张，使不同轨迹接受结构一致的检查，并减少完整轨迹中常规 token 对错误信号的稀释。

> 直观理解：它把长解答浓缩成一张关键检查清单，让有限计算集中在“错了就会导致答案站不住”的地方。

**2. 单侧语义证伪器**

第二阶段复用生成模型，仅接收 $q$ 和 $C_k$，并在一次请求内同时检查单个主张的错误及主张之间的冲突。其目标是寻找负面证据；输出 VALID 只代表此次评估未证伪，而不代表已经证明主张为真。

> 直观理解：构造正确解通常要求整条推理都正确，而推翻错误主张只需找到一个决定性反例。CLR 利用这种可能存在的不对称性，但作者将其定位为归纳偏置，并不保证证伪在所有问题上都比生成更容易。

**3. 非线性可靠性聚合器**

聚合器用 $r_k=(\frac{1}{M}\sum_m v_{k,m})^M$ 给轨迹赋权，再按预测语义等价组累加权重。若所有轨迹获得相同的正分数，该规则退化为普通自洽投票；分数不同时，被证伪轨迹对共识的贡献会减小。

> 直观理解：普通自洽只数有多少解答支持某答案，该模块同时考虑每条支持证据是否经得住检查，因此较可靠的少数候选有机会推翻有共同缺陷的多数候选。

**训练与推理**

训练阶段不存在。推理时，CLR@ $K$ 先执行 $K$ 次完整解答生成，每次同时产生 $t_k$、$y_k$ 和 $C_k$；随后对每条主张列表执行一次联合评估，共进行 $K$ 次证伪请求。系统解析 $y_k$，丢弃无法解析的轨迹，根据证伪向量计算 $r_k$，按任务特定规则合并等价预测，最后输出累计可靠性最高组的规范答案。整个流程共使用 $K$ 次生成请求和 $K$ 次评估请求，因此请求数与使用 $2K$ 条完整样本的 Cons@$2K$ 相同；但第二阶段只处理 $q$ 和 $M$ 个短主张，实际 token 数通常不同，故公平比较需同时报告请求预算与实际 token 消耗。

**复现信息**

复现所必需的设计约束包括：第一阶段必须输出任务特定的结构化预测，并附加恰好 $M$ 个简洁且决定性的主张；第二阶段对每条轨迹只发起一次联合请求，输入不包含完整轨迹或作为独立字段的最终预测；生成与证伪复用同一模型；所有实验均以 $M$ 作为可靠性分数的指数。答案解析器和等价判定规则必须与任务类型匹配，无法解析的预测应被排除；并列组以及全零分数组均按采样顺序选择最早出现者。原文节选未给出具体 $M$ 取值、解码超参数、任务解析器细节或完整提示词，后两者分别指向附录 B.2 和 B.3，复现时仍需对照原文核查。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HMMT25：数学推理基准，用于检验 CLR 在竞赛型问题上的答案选择和错误共识纠正能力。所给节选未报告题目规模、具体划分或是否使用完整测试集。
- HMMT26：与 HMMT25 相邻年份的数学推理基准，可用于观察结论能否跨题目集合保持。所给节选未报告规模和数据划分。
- CMIMC25：数学推理基准，是摘要中 GPT-OSS-20B 效率与准确率结果的具体测试场景，也是附录救援率统计的四个基准之一。原文还使用 Apex-shortlist，但受输出数量限制，此处不展开；所给节选同样未说明 CMIMC25 的规模和划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（accuracy）**

最终选择答案正确的问题比例，用来比较 pass@1、自一致性和 CLR 的整体任务表现。 （越高越好，因为更高数值表示最终回答正确的问题更多。）

</div>
<div class="metric-item" markdown="1">

**token 消耗或 token 降幅**

衡量达到相应结果所需的生成计算量；摘要以相对自一致性的 token 减少比例报告效率收益。 （在准确率相当或更高时越低越好；单独减少 token 并不能说明方法更准确。）

</div>
<div class="metric-item" markdown="1">

**CLR rescue rate（救援率）**

在“至少一个 Stage-1 候选具有正确最终答案，但未加权 Cons@$K$ 仍答错”的可恢复问题—flow 对中，被 CLR 使用同一批候选纠正的比例，即纠正数除以可恢复错误数。统计汇总 $N=8$ 个独立 flow，因此分母不是独立题目数。 （越高越好，因为它表示 CLR 更常利用可靠性评估压制错误共识并选回已经存在的正确候选；但该指标只覆盖可恢复子集，不等于总体准确率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### GPT-OSS-20B 在 CMIMC25 上，CLR 与 pass@1 比较

<div class="result-value" markdown="1">

作者报告 CLR 的准确率比 pass@1 高 $27.15$ 个百分点。

</div>

这一结果表明，在该模型与基准组合上，把测试时计算用于声明级验证，相比只生成一次解答可显著改善最终答案选择。但这是单一模型—数据集组合的摘要结果，不能单独证明同等幅度的提升会出现在全部四个模型和全部基准上。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On GPT-OSS-20B/CMIMC25, for instance, CLR exceeds pass@1 by 27.15 percentage-points and raises self-consistency accuracy from 77.50\% to 82.19\% with 37.0\% fewer tokens.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### GPT-OSS-20B 在 CMIMC25 上，CLR 与自一致性比较

<div class="result-value" markdown="1">

作者报告自一致性准确率为 $77.50\%$，CLR 将其提高到 $82.19\%$，即提升 $4.69$ 个百分点，同时 token 消耗减少 $37.0\%$。

</div>

该结果同时支持准确率和计算效率两方面的优势：CLR 并非仅靠生成更多完整解答获得提升，而是通过针对性验证重新分配预算。不过，所给节选没有给出该结果的方差、置信区间或显著性检验，因此无法据此判断重复实验中的统计稳定性。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On GPT-OSS-20B/CMIMC25, for instance, CLR exceeds pass@1 by 27.15 percentage-points and raises self-consistency accuracy from 77.50\% to 82.19\% with 37.0\% fewer tokens.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### CMIMC25 的 CLR 救援率，$K=32$，汇总 $N=8$ 个独立 flow

<div class="result-value" markdown="1">

CLR 在 $61$ 个可恢复的错误共识问题—flow 对中纠正 $29$ 个，救援率为 $47.54\%$。

</div>

这说明当正确答案已经出现在候选集合中、但普通多数聚合仍选错时，CLR 接近纠正其中一半，直接支持其“压制高置信错误共识”的机制解释。该比例不能解释为 CLR 对全部 CMIMC25 题目的总体准确率，因为其分母只包含可恢复错误，而且同一题目可在不同 flow 中重复计数。

<div class="result-source" markdown="1">

来源：附录 A.2，表 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

32 | 14/40 (35.00%) | 20/55 (36.36%) | 29/61 (47.54%) | 32/199 (16.08%)

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

- pass@1：仅使用一次生成所得答案，代表不进行额外测试时扩展的基础性能。它用于判断 CLR 的额外验证计算相对于普通单次推理是否带来实质收益。
- Cons@$K$：自一致性基线，独立采样 $K$ 条解答并根据最终答案聚合。它是有意义的比较对象，因为它把测试时计算主要用于增加候选解答，而 CLR 则把部分计算重新分配给针对候选声明的验证。
- Cons@64：主要的匹配请求数基线，与 CLR@32 比较。按照原文第 2 节的请求核算，两者被视为主要 matched-request 对照，因此该比较主要回答“相似请求预算下怎样分配计算更有效”。
- 未加权 Cons@$K$：在救援率分析中，直接对同一批 Stage-1 候选答案进行未加权聚合。该对照使分析聚焦于可靠性加权本身能否从已有候选中恢复正确答案，而不是候选生成差异。

**实验想回答的问题**

- 在模型、推理基准和测试时请求预算相匹配的条件下，CLR 能否比单次生成（pass@1）和自一致性（self-consistency）更准确地选择最终答案，同时减少推理所消耗的 token？
- 当候选集合中已经存在正确答案、但未加权自一致性仍选择错误答案时，CLR 的声明级可靠性评估能在多大比例上纠正这类“错误共识”，且纠正能力是否随候选数 $K$ 和基准变化？

**实验实现**

实验覆盖 Gemma-4-12B-it、GPT-OSS-20B、GPT-OSS-120B 和 Qwen3.5-27B 四个模型，以及四个推理基准。Cons@$K$ 使用 $K\in\{8,16,32,64\}$，CLR@$K$ 使用 $K\in\{4,8,16,32\}$；主要匹配请求数比较为 CLR@32 对 Cons@64。普通采样采用“题目加一步步作答指令”的最简提示，CLR Stage 1 在其后追加声明生成指令。所有模型均开启 thinking mode，并使用默认 thinking effort；解答生成和声明级可靠性评估采用相同采样配置。Gemma-4-12B-it、GPT-OSS-20B 和 GPT-OSS-120B 的 temperature、top-$p$、top-$k$、presence penalty 分别为 $1.0$、$1.00$、$40$、$0.0$；Qwen3.5-27B 分别为 $1.0$、$0.95$、$20$、$1.5$，其余运行设置保持模型默认值。救援率汇总 $N=8$ 个独立 flow，并以问题—flow 对而非唯一题目为统计单位。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces claim-level falsification and targeted verification to improve test-time LLM reasoning under fixed compute budgets.; rule check: matched taxonomy keywords; top rule score=6.0
- 全文指纹：`ffcdd30e0c01d4ea0d88e1ae2c15deeb87157c034ec94dce6fe8e7e621c23cb8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
