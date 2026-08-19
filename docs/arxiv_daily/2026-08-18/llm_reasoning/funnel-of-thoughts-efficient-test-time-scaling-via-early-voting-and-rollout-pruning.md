---
title: "[论文解读] Funnel of Thoughts: Efficient Test-Time Scaling via Early Voting and Rollout Pruning"
description: "[arXiv 2608.15065][LLM Reasoning] 本文提出无需训练的测试时推理方法 Funnel of Thoughts（FoT），通过提前保存已明确作答的轨迹，并依据犹豫词密度截断可能陷入低效自我修正的轨迹，以较低计算成本维持完整多轨迹多数投票的准确率。"
arxiv_id: "2608.15065"
announcement_date: "2026-08-18"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:12:41.563006+00:00"
source_sha256: "004f3aee81a49094a76a6139d9a9a645cdde1aefa495c2fac572e187871065cc"
tags:
  - "LLM Reasoning"
  - "LLM 效率"
  - "大型推理模型"
  - "测试时计算扩展"
  - "多样本推理"
  - "自洽性投票"
  - "推理轨迹剪枝"
  - "注意力计算成本"
  - "犹豫标记"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.15065</p>

# Funnel of Thoughts: Efficient Test-Time Scaling via Early Voting and Rollout Pruning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Chanhee Park, Sungbin Han, Jeongho Yoon, Seongtae Hong, Heuiseok Lim</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Department of Computer Science and Engineering, Korea University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.15065) · [PDF 下载](https://arxiv.org/pdf/2608.15065) · **关键词** 大型推理模型, 测试时计算扩展, 多样本推理, 自洽性投票, 推理轨迹剪枝, 注意力计算成本, 犹豫标记<br>


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

本文提出无需训练的测试时推理方法 Funnel of Thoughts（FoT），通过提前保存已明确作答的轨迹，并依据犹豫词密度截断可能陷入低效自我修正的轨迹，以较低计算成本维持完整多轨迹多数投票的准确率。

**不用术语来说**：大型推理模型对同一道题重复作答时，可能给出不同答案，因此实际使用中常让模型独立尝试多次，再选择出现次数最多的答案。然而，传统做法必须等待每次尝试全部结束；一旦某些推理反复出现“等等”“其实”等自我推翻并持续生成，它们不仅未必更接近正确答案，还会消耗大量计算。论文要解决的是：能否在推理尚未结束时识别并停止这些低价值尝试，同时保留足够可靠的候选答案来完成投票。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者基于约 11.5 万条推理轨迹进行数据分析，发现“Wait”“Actually”“perhaps”等犹豫标记在错误及低效轨迹中更密集，由此提出一种只读取已生成文本、无需奖励模型或额外模型调用的零额外推理信号。
- 作者提出 FoT：从完整的 $k$ 条并行轨迹开始，在固定长度检查点执行提前投票与轨迹剪枝，逐步缩小仍需继续生成的轨迹池；其目标不是减少初始采样覆盖面，而是删除计算代价最高的低效后半段，并支持跨模型和跨任务迁移。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大型推理模型（Large Reasoning Models, LRMs）通常通过生成较长的思维链来解决数学等复杂问题。由于随机解码会使同一问题的多次推理产生不同答案，可靠推断常采用多样本推理：并行或重复采样 $k$ 条推理轨迹，再根据最终答案投票。其主要瓶颈是每条轨迹都要完整生成数千个词元，而自注意力计算量会随序列长度近似二次增长，因此冗长轨迹的后半段尤其昂贵；反复自我修正、犹豫乃至陷入循环的轨迹不仅较难得到正确答案，还会消耗不成比例的计算资源。本文研究的核心背景由此形成：在维持完整 $k$ 轨迹投票可靠性的同时，能否在生成过程中识别并提前终止低价值轨迹。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**推理轨迹（reasoning rollout）**

模型针对一个问题进行一次随机生成所得到的完整思维链及最终答案称为一条推理轨迹。不同随机种子或采样结果会使多条轨迹在推理过程、长度和答案上出现差异。

</div>
<div class="concept-item" markdown="1">

**自洽性投票（Self-Consistency, SC）**

SC@$k$ 对同一问题采样 $k$ 条完整推理轨迹，并返回出现次数最多的最终答案，以利用多次推理之间的互补性。它提高可靠性的代价是必须支付 $k$ 条长轨迹的完整生成成本。

</div>
<div class="concept-item" markdown="1">

**注意力 FLOPs**

FLOPs 表示浮点运算次数，注意力 FLOPs 用于估计 Transformer 在注意力模块上的计算成本。由于标准自注意力需要比较序列中大量词元对，轨迹越长，后续词元带来的边际计算成本通常越高。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个待求解问题和能够生成长思维链的 LRM，系统以随机采样方式启动 $k$ 条并行推理轨迹。标准基准 SC@$k$ 等待所有轨迹完成，从每条轨迹提取最终答案，并以多数票或相对多数票作为输出；本文所处的问题设置则允许在若干固定词元数检查点观察已经生成的文本，并据此提前保存已明确作答的轨迹或剪除低价值轨迹。目标是在不训练额外模型、不调用奖励模型、也不依赖隐藏状态或词元对数概率的条件下，仅利用在线生成文本减少长轨迹尾部的注意力计算，同时尽可能保持完整 SC@$k$ 的最终投票准确率。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$k$**

针对同一问题采样并参与候选池的推理轨迹数量。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{SC}@k$**

采样并完整生成 $k$ 条推理轨迹后，以最终答案多数票进行预测的自洽性推断方法。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{pass}@1$**

仅依据一次采样判断是否成功的单轨迹准确性指标；原文用它与多样本成功率之间的差距说明答案分布具有多样性。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{pass}@k$**

在 $k$ 次采样中至少有一条轨迹得到正确答案的成功率，用于刻画增加采样后可获得的潜在收益。

</div>

</div>

**直接相关的工作**

- **Adaptive Consistency**: 该方法根据持续更新的多数票及 Beta 停止规则决定何时停止继续采样，主要沿“样本数量”轴减少成本；但一条轨迹一旦开始仍需生成到结束，无法直接削减单条轨迹昂贵且可能无效的后半段。它与本文沿“词元长度”轴进行轨迹内提前处理的思路具有互补性。
- **Slim-SC**: Slim-SC 在并行的 $k$ 轨迹池中依据跨轨迹嵌入相似度剪除冗余轨迹，但需要独立的嵌入模型。本文关注的是出现反复犹豫和自我修正模式的病态长轨迹，并限定只使用已生成文本作为判断信号。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大型推理模型的单次输出不稳定，而困难推理题的正确答案往往只出现在部分采样轨迹中，因此可靠部署依赖多样本推理。问题在于，推理轨迹通常长达数千个 token，且标准注意力的计算量随序列长度近似二次增长，长轨迹尾部尤其昂贵；若某些轨迹陷入重复犹豫和反复自我修正，系统会在最昂贵的阶段继续为低价值文本付费。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **Self-Consistency 多数投票（$\mathrm{SC}@k$）**：针对同一问题独立采样 $k$ 条完整推理轨迹，抽取每条轨迹的最终答案，再返回出现次数最多的答案。增加 $k$ 通常能提高候选答案覆盖率和投票稳定性，因此它构成本文希望保持的准确率参照。
- **减少采样数量的高效采样方法**：通过直接生成少于完整预算的候选轨迹来降低推理成本。其节省来自缩小初始轨迹池，而不是在生成过程中辨别哪些轨迹已经有效作答、哪些轨迹正在恶化。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 标准 $\mathrm{SC}@k$ 要求全部 $k$ 条轨迹运行至完成，无法利用生成中途已经出现的答案承诺，也无法及时停止反复犹豫的轨迹；由于注意力成本随上下文增长，后期冗余 token 会造成不成比例的计算和时间开销。
- 直接减少采样数量虽然节省成本，却同时降低了初始探索范围，可能删掉携带正确答案的少数轨迹，因而难以在困难问题上同时达到完整 $\mathrm{SC}@k$ 的准确率与较低计算量；已有方案尚未充分利用一种不需要训练、奖励模型或 logits 的在线文本信号来选择性截断轨迹。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种适用于并行多样本推理的训练无关机制：它应保留完整 $k$ 轨迹池带来的答案覆盖率，仅根据生成过程中的可观测文本，在昂贵的长尾生成发生之前区分应当保留、可以提前计票和应当终止的轨迹，并且能够不经重新调参迁移到不同模型或任务。

</div>
<div markdown="1"><span>核心问题</span>

仅使用轨迹已经生成的文本，能否在若干中间检查点可靠地保存已明确作答的轨迹，并依据犹豫标记的相对密度剪除最可能低效的轨迹，从而以显著更少的注意力计算维持完整 $\mathrm{SC}@32$ 的投票准确率？

</div>
<div markdown="1"><span>作者直觉</span>

有效推理通常会逐渐收敛并形成明确答案，而低效推理更容易反复推翻先前判断，在文本表面留下“Wait”“Actually”“perhaps”等犹豫痕迹。FoT把这些词看作轨迹失去方向的廉价症状，而不是正确性的严格证明：已经明确给出答案的轨迹先进入投票库，其余轨迹中犹豫标记最密集者优先停止。这样既不会像减少采样那样一开始就牺牲探索范围，又能把计算集中到仍可能产生有用答案的轨迹上。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Funnel of Thoughts（FoT）是在自洽采样（Self-Consistency, SC）框架上的推理时计算削减方法。给定问题 $q$，模型先生成 $k$ 条独立推理轨迹；FoT 在若干固定长度检查点检查仍在生成的轨迹：已经给出答案的轨迹立即进入投票库，尚未给出答案的轨迹按“犹豫标记密度”排序，仅保留密度最低的一部分继续生成，最后将已保存答案与幸存轨迹的答案进行多数或并列最多票数投票。其核心是沿两个维度压缩计算：提前结束已经提交答案的轨迹，并优先终止可能陷入反复自我修正的长轨迹；已提交的答案不会因为轨迹停止生成而丢失。直观地说，FoT 像一个逐层收窄的漏斗：有明确答案的样本先“交卷并计票”，仍然犹豫的样本则保留较少、较有希望的部分继续思考。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 独立生成推理轨迹

从模型独立采样 $k$ 条推理轨迹 $c_{1},\ldots,c_{k}\u007d$，每条轨迹最多生成给定的 token 预算；推理期间在固定 token-count 检查点 $t_{1},\ldots,t_{m}\u007d$ 暂停检查活动轨迹。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、语言模型和采样数量 $k$。论文实验通常令 $k=32$，为每条轨迹使用不同随机种子，并预先生成同一批轨迹供 FoT 与基线比较。<br>
**输出**：初始活动集合 $\mathcal{A}=\u007b1,\ldots,k\u007d$，空投票库 $\mathcal{B}=\varnothing$，以及在各检查点可见的部分轨迹 $c_i[1:t_j]$。

</div>

**直观理解**：先让多个模型实例分别解题，保留它们的思考过程；检查点相当于定时查看每个人目前是否已经写出了最终答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提前投票与答案入库

对每个活动轨迹执行 $\textsc{HasAnswer}(c_i[1:t_j])$；若检测到最终答案（通常为 `\\boxed{}` 内容），则用 $\textsc{Extract}$ 提取答案，将其加入 $\mathcal{B}$，并从 $\mathcal{A}$ 删除该轨迹。若活动轨迹数已不超过 $2$，则停止继续剪枝并进入完成生成阶段。

<div class="method-step__io" markdown="1">

**输入**：检查点 $t_j$ 的活动轨迹前缀 $c_i[1:t_j]$，活动集合 $\mathcal{A}$ 和投票库 $\mathcal{B}$。<br>
**输出**：投票库包含已经提交的答案，活动集合只包含尚未提交、仍需继续生成的轨迹。

</div>

**直观理解**：一旦某条轨迹已经交卷，就立刻记下它的答案并释放后续计算；这条轨迹虽然不再继续写，但它的票仍然保留。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于犹豫密度的轨迹剪枝

计算每条活动轨迹的累计犹豫标记密度 $d_i$，按密度升序排列，并保留 $n=\max(2,\lfloor|\mathcal{A}|\rho\rfloor)$ 条密度最低的轨迹，删除其余轨迹；随后在下一个检查点重复提前投票和剪枝。该规则只作用于尚未提交答案的轨迹。

<div class="method-step__io" markdown="1">

**输入**：检查点处每条剩余活动轨迹的可见前缀，以及保留比例 $\rho\in(0,1]$。犹豫标记包括 `Wait,`、`actually`、`perhaps` 等预先定义的文本模式。<br>
**输出**：逐个检查点缩小的活动集合 $\mathcal{A}$，其中保留下来的轨迹继续生成，已删除轨迹不再产生后续注意力计算。

</div>

**直观理解**：如果一条轨迹反复出现“等等”“其实”“也许”等犹豫信号，就把它视为更可能陷入冗长循环的候选；每轮只留下相对不犹豫的一部分继续思考，并至少保留两条以避免投票完全失去多样性。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 完成幸存轨迹并进行最终投票

对所有幸存活动轨迹完成生成并提取答案，将这些答案与 $\mathcal{B}$ 中已保存的答案合并；使用 $\textsc{Plurality}$ 选择出现次数最多的答案，即使其票数未严格超过 $50\%$ 也按论文约定视为多数答案。

<div class="method-step__io" markdown="1">

**输入**：最终检查点后的投票库 $\mathcal{B}$ 与活动集合 $\mathcal{A}$。<br>
**输出**：问题 $q$ 的最终预测答案 $\hat{a}$。

</div>

**直观理解**：最终统计所有“已交卷”和“坚持到最后”的答案，而不是只统计最后仍在运行的少数轨迹；因此减少的是继续生成的计算量，不是投票样本本身。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 自洽采样的多数投票

$$
\hat{a}=\arg\max_{a}\sum_{i=1}^{k}\mathbf{1}[a_i=a]
$$

**符号说明**

- $\hat{a}$：最终预测答案
- $a$：候选答案
- $k$：独立推理轨迹数量
- $a_i$：第 $i$ 条轨迹提取出的答案
- $\mathbf{1}[a_i=a]$：指示函数；当第 $i$ 条轨迹答案等于候选答案 $a$ 时取 $1$，否则取 $0$
- $\arg\max$：返回使计数最大化的候选答案

<div class="equation-explanation" markdown="1">

**直观理解**：该式统计每个候选答案获得的票数，并选择票数最多者。FoT 不改变这个最终决策原则，而是通过提前保存答案和剪枝减少产生完整轨迹所需的计算。<br>
**原文位置**：第 3.1 节，式（1）；算法 1 第 17 行

</div>

</div>

<div class="equation-block" markdown="1">

#### 注意力计算成本

$$
\mathrm{FLOPs}=\sum_{i=1}^{k}4\cdot L\cdot d\cdot s_i^2
$$

**符号说明**

- $\mathrm{FLOPs}$：所有推理轨迹的注意力浮点运算量
- $k$：轨迹数量
- $L$：模型层数
- $d$：模型维度
- $s_i$：第 $i$ 条轨迹的总序列长度，单位为 token

<div class="equation-explanation" markdown="1">

**直观理解**：在标准全注意力中，序列长度越长，单条轨迹的成本按 $s_i^2$ 增长，所以晚期生成特别昂贵。FoT 提前终止长而低效的轨迹，直接减少其后续平方增长的注意力计算；论文另行指出，若计入前馈层和投影等非注意力计算，整体模型 FLOP 节省为 $28.8\%$。<br>
**原文位置**：第 3.1 节 Cost metrics；第 3.3 节 Rollout Pruning

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文没有提出新的模型训练目标，也没有训练 FoT 专属参数。语言模型保持冻结，方法只在测试时间利用预生成或在线生成的推理轨迹进行答案检测、相对排序、轨迹终止和最终投票；保留比例 $\rho$ 与检查点安排通过池上网格搜索确定，并固定用于不同问题和模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 投票库与活动集合**

FoT 同时维护活动集合 $\mathcal{A}$ 和投票库 $\mathcal{B}$。$\mathcal{A}$ 表示仍在生成且可能被剪枝的轨迹索引，$\mathcal{B}$ 保存已经检测到答案的提取结果；最终在 $\mathcal{B}$ 与幸存 $\mathcal{A}$ 的答案上执行并列最多票数选择。

> 直观理解：这是 FoT 区别于简单截断的关键：停止一条轨迹后，系统仍保存它已经产生的票，因此缩小运行池不会同时缩小最终投票池。

**2. 提前投票模块**

在每个检查点，FoT 对活动轨迹前缀执行答案存在性检测和答案抽取，不需要额外模型推理、嵌入模型、奖励模型或 log-probability。检测到答案的轨迹从后续生成中移除，但其答案永久加入 $\mathcal{B}$。

> 直观理解：模块只做文本扫描，寻找轨迹是否已经明确写出答案；它的目的不是判断答案是否正确，而是判断这条轨迹是否已经值得停止计算并计票。

**3. 犹豫密度剪枝模块**

对前缀累计统计预定义犹豫标记数，并按每 $1{,}000$ 个字符的标记密度进行相对排序。每轮保留最低密度的 $n=\max(2,\lfloor|\mathcal{A}|\rho\rfloor)$ 条轨迹，因此该规则依赖同一活动池内的相对排名，而非跨模型固定阈值。

> 直观理解：它不比较不同轨迹是否相似，而是判断某条轨迹是否正在变得反复和迟疑；这样既能削减长而低效的尾部，又较少破坏多条独立解法带来的答案多样性。

**训练与推理**

FoT 是纯推理时算法。离线复现实验中，先用相同模型和采样设置生成共享轨迹池，再模拟各检查点的前缀检查：已经出现答案的轨迹进入投票库，其他轨迹按犹豫密度保留低密度者；最终完成幸存轨迹并与投票库合并投票。在线部署时，推理服务器在固定 token 数检查点暂停活动轨迹，释放已结束或被剪枝轨迹的 KV cache，并恢复幸存轨迹；由于剪枝只需字符串计数，通常不需要额外神经网络推理。

**复现信息**

实验覆盖 $6$ 个语言推理模型、$4$ 个竞赛数学基准，并为每个问题生成 $32$ 条独立轨迹；答案使用 `math_verify` 评测。论文使用温度 $T=0.6$、$top\text{-}p=0.95$、$top\text{-}k=30$ 和最多 $32{,}768$ 个生成 token；离线检查点按字符前缀近似 token 截断，在线部署使用真实 token 计数。犹豫标记按累计文本每 $1{,}000$ 个字符统计，重叠标记按设计可重复计数；最终投票平票时按插入顺序处理。注意成本数字需区分标准全注意力、完整模型 FLOP 和 token 数减少：论文报告的 FoT 整体模型 FLOP 节省为 $28.8\%$，在线端到端耗时节省为 $37.6\%$，而不同注意力机制下的注意力 FLOP 节省会随窗口大小变化。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 四个数学基准：AIME24、AIME25、AMC23 和 MATH500。它们组成主要的 6 模型 × 4 基准评测池，用于比较 FoT、完整自洽采样和高效自洽基线；其中 AIME24/25 被视为较困难的子集，MATH500 位于相对容易的一端。
- 跨模型和跨领域测试所使用的数据集：原文摘录仅明确说明进行了 held-out models、cross-domain benchmarks 和 online deployment 测试，但未列出全部数据集名称、规模或划分。
- 诊断与校准数据：115,200 条 rollout 用于验证犹豫标记；4 benchmark calibration pool 用于超参数搜索。原文明确给出其由 6 个模型和 4 个基准构成，但未在摘录中完整说明每个集合的独立训练、验证或测试划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Exact-match accuracy / math_verify accuracy**

判断模型最终答案是否与标准答案完全匹配；部分表格使用 exact-match grading，难度分层表明确使用 $math_verify$。 （越高越好，因为它直接表示正确解题比例。）

</div>
<div class="metric-item" markdown="1">

**Attention FLOP saving**

相对于 $SC@32$，减少的注意力浮点运算比例，反映 FoT 在 rollout 生成过程中的计算节省。 （越高越好，但必须结合准确率解读；单独提高节省率可能意味着过度剪枝。）

</div>
<div class="metric-item" markdown="1">

**Pass@1、Pass@32 与 SC@32**

$Pass@1$ 是单条 rollout 的平均正确率，$Pass@32$ 是 32 条 rollout 中只要存在正确答案时的 oracle 正确率，$SC@32$ 是对 32 条结果多数投票后的正确率。$Pass@1$ 到 $Pass@32$ 的差距衡量采样随机性以及多数投票可利用的潜在空间。 （$Pass@1$、$Pass@32$ 和 $SC@32$ 均越高越好；但 $Pass@32$ 是 oracle 上界，不能等同于实际可部署性能。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四个数学基准上的 6 模型 × 32 rollout 对比：FoT@32 对 SC@32

<div class="result-value" markdown="1">

FoT@32 与 SC@32 在 3,600 个模型-问题配对中的 3,580 个给出相同正确性结果，仅有 20 个差异，其中 FoT 胜 12 次、负 8 次；McNemar 精确检验为 $p=0.50$，准确率差异的 paired-bootstrap 95% 置信区间为 $[-0.14,+0.36]$ 个百分点。原文同时声称 FoT 在保持准确率的同时将注意力 FLOP 大致降低一半，但摘录未提供 Table 2 的逐格数值。

</div>

这说明 FoT 在总体正确性上与完整 32 次自洽采样基本持平，且观察到的差异不足以支持存在系统性准确率变化。结果支持“减少后期无效计算”的主张，但不能证明 FoT 在每个模型、每道题或所有任务上都不损失准确率；其 12 次胜出和 8 次落败表明剪枝仍可能改变最终投票。

<div class="result-source" markdown="1">

来源：Section 4.1 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

FoT@32 and SC@32 return the same correctness outcome on 3,580 of 3,600 paired model-problem instances, differing on only 20 cases: 12 FoT wins and 8 FoT losses.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### FoT 的投票稳定性：按 SC@32 多数答案占比和答案多样性分层

<div class="result-value" markdown="1">

在 SC@32 多数答案占比大于 50% 的分组中，FoT 仅在 0.2% 的案例改变最终答案；在多数答案占比小于 25% 的分组中，平均有 15.2 个不同答案，FoT 改变最终答案的比例为 49.1%，且该组的 FoT 正确率相对 SC@32 净增加 4 个百分点。

</div>

FoT 主要保留强共识池的原有决定，把作用集中在答案分歧大的池子。低共识组既更不可靠，也更容易因剪枝改变投票，因此这里的净收益说明 FoT 可能修正一部分无效轨迹，但不能据此断言所有低共识问题都会改善；该分析还排除了 4 个没有可提取 SC 答案的配对。

<div class="result-source" markdown="1">

来源：Appendix B.3 Vote-Concentration Diagnostic, Figure 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

When SC@32 has a clear majority, FoT almost always preserves it: in the >50% bin, the final answer changes in only 0.2% of cases.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 统一完整模型 FLOP 基准下的 token-axis 与 sample-axis 方法比较

<div class="result-value" markdown="1">

在统一的 full-model FLOP basis 上，DSC 在相同汇总准确率下相对 SC@32 节省 69.4% FLOP，FoT 节省 28.8%；FoT+DSC 的节省达到 80.9%（全部基准）和 75.7%（困难基准），对应准确率变化分别为 $-0.4$ 和 $-1.4$ 个百分点。按难度看，DSC 在 MATH500 上节省 75.0%、在 AIME24/25 上节省 54.4%；FoT 则分别节省 21.9% 和 44.0%。

</div>

两类方法利用不同计算轴：DSC 减少要生成的 rollout 数量，FoT 缩短已经开始生成但后期会浪费计算的 rollout。因此二者可以组合，获得更高的总体 FLOP 节省。这个结果支持互补性，但由于组合方案有轻微准确率下降，且摘录指出 Certaindex 只是 offline proxy，不能把所有节省率直接视为在线部署保证；FoT 额外具有降低单次查询延迟和 KV-cache 占用的特点。

<div class="result-source" markdown="1">

来源：Appendix B.6 Sample-Axis Baselines on a Unified FLOP Basis, Table 15

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At equal pooled accuracy DSC saves more than FoT overall (69.4% vs. 28.8%), and our offline Certaindex proxy also holds SC accuracy at an 11.5–13.2% saving, though the proxy is only indicative: it can fire later than the original online probe, understating savings, while paying no probe cost, overstating them.

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

- SC@32：从同一个 32-rollout 池进行完整 self-consistency，通过多数投票选择答案，是 FoT 的主要准确率和计算量参照。
- Adaptive Consistency（AC）：一种沿 sample axis 自适应决定采样数量的高效自洽方法，用于比较 FoT 的 token-axis pruning 是否具有竞争力。
- Slim-SC：另一种高效 self-consistency 基线；其通过相似性等策略压缩或筛选采样结果，用于检验 FoT 是否比相似度剪枝更稳定。
- DSC 及其与 FoT 的组合：附录中的统一 FLOP 基准比较，DSC 代表 sample-axis 方法，用于分析样本轴和 token 轴节省是否互补；原文摘录未给出 DSC 的全称。

**实验想回答的问题**

- FoT 是否能在保持 $SC@32$ 正确率的同时，显著减少注意力计算量，并且在不同模型、数学基准和在线部署场景下稳定工作？
- FoT 的早期投票、基于犹豫标记的 rollout pruning，以及检查点和保留比例等设计，分别是否对准确率、计算节省和跨模型泛化产生实质作用？

**实验实现**

实验沿用第 3 节的 6 模型、4 基准设置，并从与 $SC@32$ 相同的 32 条 rollout 池开始。FoT 将已经提交答案的 rollout 纳入已完成集合，同时在多个生成检查点观察仍处于活动状态的轨迹；若其已生成文本呈现被验证的无效犹豫标记，则终止相应轨迹。这样，FoT 的计算节省来自删除后期无效生成，而不是减少初始答案候选的多样性。犹豫标记通过在 115,200 条 rollout 上计算与正确率的加权 point-biserial correlation 进行筛选，保留 21 个与正确性显著负相关的标记；实际剪枝使用同一活动池内、同一检查点的相对排序，因此不依赖跨模型固定密度阈值。实验还包括 held-out model、cross-domain benchmark、online deployment、discordant-instance、投票集中度和难度分层分析。附录报告了覆盖检查点数量、检查点位置和保留比例的 340 组超参数搜索；完整采样参数、基线配置和搜索细节位于 Appendix D，但摘录未给出具体默认配置。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 犹豫标记核的构建与在线相对排序 | 作者从 21 个标记构建剪枝核，所有标记都满足加权 $r<0$ 且加权 $p<0.05$；组合密度与正确性的 point-biserial correlation 为 $r_{\mathrm{pb}}=-0.30$。密度最低十分位的准确率为 96.9%，最高十分位为 65.6%，两者相差 31.4 个百分点；按十分位序号与准确率的相关系数为 $r=-0.82$。 | 这一分析检验的是剪枝信号是否具有稳定的方向性，而不是直接证明每个标记都能单独提升最终系统准确率。结果表明高密度轨迹整体更不可靠，但不同模型的绝对密度差异较大，所以 FoT 使用同一活动池内的相对排序，而不是跨模型共享固定阈值。作者还排除了与正确性正相关、可能表示有效自我纠错的词语，避免把生产性修正误剪掉。 | Appendix A.1 Hesitation-Marker Validation, Table 9<br><span class="experiment-evidence">Accuracy falls monotonically with density (r = −0.82 between decile index and accuracy), for a 31.4pp gap between the lowest and highest decile.</span> |
| 按问题难度分层的 FoT 与 SC@32 对比 | 在所有四个基准中，$0<p_1\leq0.25$ 的低 $Pass@1$ 分组中，SC@32 为 23.1%，FoT 为 28.9%，提升 5.8 个百分点；在困难 AIME24/25 子集中，该分组为 SC@32 35.7%、FoT 40.5%，提升 4.8 个百分点。$p_1=0$ 的分组两者均为 0.0%，而 $p_1>0.5$ 的高通过率分组中 SC@32 为 100.0%、FoT 为 99.9%。 | 该分层检验 FoT 是否主要作用于存在较大采样不确定性的题目。低 $Pass@1$ 但仍有正确 rollout 的题目获得最大净改善，符合剪枝无效轨迹、保留潜在正确答案的机制；没有任何正确 rollout 的题目无法由 prune-only 方法修复，而接近饱和的题目几乎没有提升空间。该结果不能解释 FoT 对每个具体问题的因果作用，因为它是按问题难度分组的相关性分析。 | Appendix B.5 Difficulty-Stratified Accuracy, Table 14<br><span class="experiment-evidence">FoT sits 4.8–5.8pp above SC@32 in the low-pass@1 bins (0 < p1 ≤ 0.25), where the pass@1–pass@32 gap is largest and the vote is least concentrated.</span> |

**定性案例**

- 无答案轨迹诊断显示，FoT 会逐个检查点逐步移除不提交最终答案的尾部，而不是在单个时间点完美识别所有失败 rollout：AIME24/AIME25/AMC23 stress subset 中，每个 32-rollout 池的平均 no-answer 数量从 2.67 降至最终检查点的 0.79，原文称最终减少 71%。这支持 FoT 对“迟迟不承诺答案”的轨迹进行在线处理的解释，但也表明该机制是群体层面的尾部清理，并非可靠的单轨迹错误判定器。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Improves test-time reasoning scalability and computational efficiency through early voting and selective rollout pruning.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`004f3aee81a49094a76a6139d9a9a645cdde1aefa495c2fac572e187871065cc`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
