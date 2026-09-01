---
title: "[论文解读] REER-PT: Reverse-Engineered Reasoning for Perplexity-Guided Pre-training Data Augmentation"
description: "[arXiv 2608.30627][预训练] REER-PT面向原始预训练语料，离线筛选“难预测但可由上下文推断”的续文，并仅插入能够降低该续文困惑度的简短推理注释，从而在不改变标准下一词元预测目标的前提下显式补足上下文与续文之间的推理连接。"
arxiv_id: "2608.30627"
announcement_date: "2026-09-01"
primary_category: "llm_pretraining"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:44:04.691030+00:00"
source_sha256: "cb9b59067f63548d4513fa80290bca29ca0f5ada0cfe23c28c338c978508a170"
tags:
  - "预训练"
  - "LLM Reasoning"
  - "大语言模型预训练"
  - "预训练数据增强"
  - "反向工程推理"
  - "困惑度引导"
  - "推理注释"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">预训练 · arXiv 2608.30627</p>

# REER-PT: Reverse-Engineered Reasoning for Perplexity-Guided Pre-training Data Augmentation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Haoran Que, Jiajun Shi, Ting Huang, Renming Pang, Jiaheng Liu, Ge Zhang, Wenhao Huang, Shen Yan, Wei Ye, Shikun Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30627v1) · [PDF 下载](https://arxiv.org/pdf/2608.30627v1) · **关键词** 大语言模型预训练, 预训练数据增强, 反向工程推理, 困惑度引导, 推理注释<br>


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

REER-PT面向原始预训练语料，离线筛选“难预测但可由上下文推断”的续文，并仅插入能够降低该续文困惑度的简短推理注释，从而在不改变标准下一词元预测目标的前提下显式补足上下文与续文之间的推理连接。

**不用术语来说**：普通预训练文本通常只展示“前文之后写了什么”，却不说明两者为何相连；模型因而需要从海量文本中自行摸索这些隐含联系。直接给所有文本生成解释不仅成本高，而且生成的解释可能只是流畅的废话，甚至提前抄出后文答案。真正需要解决的是：如何在大规模语料中找出值得解释的位置，并客观判断一段解释是否确实帮助模型理解原文的下一段内容。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出REER-PT这一稀疏、离线的预训练数据增强框架：先定位高困惑度且可由上下文推断的续文，再生成书摘笔记式的简短注释，并依据续文困惑度、长度和目标泄漏约束筛选与改写候选注释；处理后保留全部源文本，可直接使用标准下一词元预测训练。
- 把“已观察续文的困惑度是否下降”转化为推理注释的实用性判据，使注释生成围绕模型真实的预测困难展开，而非仅依赖语言流畅度；论文进一步通过语料层面的困惑度分析和同配置的受控预训练比较检验这一设计。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型预训练数据增强与推理增强预训练的交叉领域。大语言模型通常在大规模文本上执行下一词预测：给定前文上下文，学习预测后续词元。现有预训练文本往往保留了“上下文之后是什么”，却没有显式表示“为什么会出现这一后续内容”的中间联系；因此，本文研究如何在不改动原始文本主要内容、也不改变标准训练目标的前提下，为普通预训练语料补充简洁的推理注释。其核心背景是：高质量数据逐渐成为扩展模型能力的瓶颈，而从问答数据构造的传统思维链数据又难以覆盖普通文档的主题、体裁和领域。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**下一词预测与困惑度**

下一词预测要求模型根据上下文逐步估计后续词元的概率。困惑度（perplexity，简称 $\mathrm{PPL}$）是衡量模型对一段文本预测难度的指标；在相同条件下，困惑度越低，表示模型越容易预测该文本。

</div>
<div class="concept-item" markdown="1">

**思维链与推理注释**

思维链（chain-of-thought，简称 CoT）是连接问题、上下文与答案的中间推理步骤。本文使用更短的“书籍批注式”推理注释，目的不是生成完整解题过程，而是把上下文到已观察后续之间原本隐含的语义过渡说清楚。

</div>
<div class="concept-item" markdown="1">

**预训练数据增强**

预训练数据增强是对原始语料进行筛选、改写或插入辅助文本，再用增强后的语料训练模型。本文采用稀疏的局部变换：只在特定后续内容上方插入注释，并保留原始上下文和后续内容。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

设原始文档被划分为前文上下文 $c$ 与其真实后续 $y$。方法需要首先找出满足两个条件的候选位置：后续 $y$ 在给定 $c$ 时较难预测，但其内容仍能够由 $c$ 推断；随后生成一条简洁注释 $a$，使加入注释后后续更容易预测，即希望达到 $\mathrm{PPL}(y\mid c,a)<\mathrm{PPL}(y\mid c)$。系统的输入是原始预训练语料和离线使用的模型，输出是增强语料：在少量选定位置形成 $c$、注释 $a$、后续 $y$ 的顺序，而原始文本本身仍被保留。该设定假定困惑度下降能够作为注释有用性的近似信号，并要求注释长度受控且不能直接泄露目标后续；最终训练仍采用普通的下一词预测，而不是在线生成推理轨迹。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$c$**

选定位置之前的上下文，即用于推断后续内容的已有文本。

</div>
<div class="notation-item" markdown="1">

**$y$**

原始文档中紧接在上下文之后的真实后续或目标文本。

</div>
<div class="notation-item" markdown="1">

**$a$**

由注释模型生成并经过离线评估、筛选和 refinement 的推理注释，用于补足 $c$ 与 $y$ 之间的隐含联系。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{PPL}(y\mid c,a)$**

在同时给定上下文 $c$ 与注释 $a$ 时，模型对后续 $y$ 的困惑度；它用于判断注释是否改善了后续预测。

</div>

</div>

**直接相关的工作**

- **REER**: REER 使用已知参考输出的困惑度作为优化信号，在候选思维链轨迹中搜索能够降低参考输出生成难度的推理。REER-PT 将这一思想从有明确参考答案的场景扩展到原始预训练文档：把文档中观察到的真实后续作为参考，并离线搜索能降低其困惑度的简洁注释。
- **Quiet-STaR、TPT 等推理增强预训练方法**: 这些方法说明，在预训练过程中引入显式或潜在的中间思考可能有助于未来词元预测；但相关路线可能需要在线生成推理、较密集的推理轨迹，或面向特定文本和任务构造较长的解释。REER-PT 的背景差异在于，它只对难预测且可由上下文推断的后续进行局部增强，并在训练前完成注释生成与筛选，因此仍可直接使用标准下一词预测。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

随着语言模型训练算力增长，高质量预训练数据逐渐成为瓶颈。现有原始文档覆盖广泛领域，但其中许多因果、逻辑或话题过渡只被隐含表达；标准下一词元预测只监督实际续文，没有直接呈现连接前文与续文的中间推理。若能从现有语料中恢复这些连接，就可能在无须逐领域设计问答任务的情况下增加推理监督，但这种处理必须足够稀疏且便宜，才能扩展到语料库规模。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于整理后问答数据的思维链监督**：围绕问题与答案编写或生成逐步推理过程，再把这些过程作为训练文本，使模型显式学习从输入到答案的中间步骤。它适合结构明确的推理任务，但通常依赖人工整理的问答样本。
- **面向预训练的生成式、隐式或在线推理方法**：在预训练文本中加入模型生成的中间思考、使用潜在推理表示，或针对已观察到的续文进行在线生成与强化学习，以便把推理信号纳入语言模型训练。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 传统思维链数据主要来自精选问答对，规模与领域覆盖受限，难以直接利用普通文档中广泛存在的隐含依赖；而对语料密集生成推理或在训练时执行在线推理展开，又会带来难以承受的语料级计算成本。
- 模型生成的注释即使语言流畅，也可能与当前预测难点无关、重复上下文或缺乏依据；反过来，高损失词元也不一定对应可推理关系，它们可能只是任意姓名、日期、标识符或外部事实。若只按高损失位置或生成质量加注释，就可能制造无效监督，甚至通过复述后文产生目标泄漏。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

先前研究尚缺少一种可扩展到原始预训练语料的选择与验证机制：它不仅要判断“哪里值得加入推理”，区分可由上下文恢复的隐含联系与本质不可预测的信息，还要判断“哪条注释真正有用”，并同时控制计算开销、注释长度和目标泄漏。换言之，缺口不只是生成更多推理文本，而是用与下一词元预测直接相关的信号筛选少量、有效且有依据的注释。

</div>
<div markdown="1"><span>核心问题</span>

能否把已观察续文作为固定目标，以条件困惑度作为优化信号，在原始语料中自动发现难预测但可推断的续文，并离线生成、筛选和改写简短推理注释，使加入注释后的续文满足$\operatorname{PPL}(y\mid c,a)<\operatorname{PPL}(y\mid c)$，同时保留原文且无需改变标准预训练目标？其中$c$是前文上下文，$y$是原始续文，$a$是插入的推理注释。

</div>
<div markdown="1"><span>作者直觉</span>

续文已经存在于原始文档中，因此可以充当一个无需额外标注的“参考答案”。如果某段续文单看前文较难预测，但加入一条不泄漏答案的简短解释后明显更容易预测，那么这条解释很可能补出了原文省略的逻辑桥梁；若困惑度没有下降，它即使读起来合理，也未必提供了模型所需的信息。只在这类位置离线插入通过检验的注释，相当于把作者默认读者能够自行补全的思路写成旁注，既集中增强真正困难的连接，又避免在每个位置都生成冗长推理。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

REER-PT 将原始文档转换为带有稀疏推理注释的增强语料：先用 PPL 模型计算句子级困惑度，优先寻找难以预测但可由前文推断的句子边界；再由注释模型生成多条书籍注释风格的候选解释，并用目标续写的条件困惑度进行无梯度筛选和迭代改写；最后仅保留能降低续写困惑度且不泄漏目标内容的注释，并插入原文续写之前。该过程不改变源文本 token 的顺序和内容，因此增强语料仍可使用标准 next-token prediction 训练。直观地说，方法试图在“上下文”和“下一段文字”之间补上一段简洁的桥接说明，但只有当这座桥确实让下一段更容易预测时才保留。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选插入位置选择

PPL 模型为每个 token 计算条件对数概率 $ell_t=\log p_{\mathrm{ppl}}(x_t\mid x_{<t})$，再按句子聚合为平均对数概率和句子级困惑度；系统按困惑度从高到低排序句子，并以句首作为候选插入位置。注释模型进一步判断目标句子是否能从其前文语境中合理推断，过滤掉仅包含任意姓名、日期、标识符或外部事实的候选。

<div class="method-step__io" markdown="1">

**输入**：输入是经过分词的文档 token 序列 $D=(x_1,dots,x_T)$，以及用于计算概率的 PPL 模型。<br>
**输出**：输出是至多 $K=\lfloor T/1000\rfloor$ 个已排序且通过语境可推断性检查的插入位置。

</div>

**直观理解**：先找模型最不容易接上的句子，再检查这种困难是否来自前文缺少一个可解释的逻辑连接，而不是因为句子突然引入了完全未知的事实。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始注释生成与过滤

注释模型为每个 $(c_i,y_i)$ 生成多条第三人称或非人称的书籍笔记风格初始注释，说明上下文中的相关信息、缺失的概念或篇章联系，以及为什么 $y_i$ 会随后出现。系统过滤不在预设长度范围内的注释，通常要求约 500—1,000 个词，并删除直接重复或近似改写 $y_i$ 中信息的目标泄漏注释。

<div class="method-step__io" markdown="1">

**输入**：输入是每个选定位置形成的局部上下文—续写对 $(c_i,y_i)$，其中 $c_i$ 是前一个选定位置之后到当前位置之前的原文，$y_i$ 从当前句子开始并延续到下一个选定位置之前。<br>
**输出**：输出是每个候选位置的一组符合长度约束且不直接暴露目标续写的初始注释。

</div>

**直观理解**：注释不是把答案提前抄出来，而是像教科书旁注一样解释“前面讲了什么、这里缺哪一步、所以后面为什么这样发展”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于续写困惑度的注释改写

每条注释按段落拆分，注释模型逐段提出候选替换；每轮都将当前注释保留在候选集中，并选择使 $y_i$ 条件困惑度最低的完整注释。所有初始注释分别进行有限步迭代改写，最后跨所有改写轨迹选出续写困惑度最低的候选。

<div class="method-step__io" markdown="1">

**输入**：输入是通过初始过滤的注释、对应的上下文 $c_i$ 和续写 $y_i$，以及 PPL 模型。<br>
**输出**：输出是每个位置的最终候选注释 $a_i^*$ 及其相对于无注释条件的困惑度差值 $\Delta_i$。

</div>

**直观理解**：把长注释分段反复润色，每次只接受能让模型更好预测后文的版本；保留旧版本意味着改写不会在指标上变差。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 有效性判定与增强语料构造

仅当注释相对于无注释基线产生严格正的困惑度下降时才接受；接受后，在目标续写前插入专用边界标记 `<annotation_begin>` 和 `<annotation_end>`。所有源 token 保持原有顺序和内容，多个接受的注释共同形成固定的增强预训练语料。

<div class="method-step__io" markdown="1">

**输入**：输入是最终候选注释 $a_i^*$、源文档及其目标续写。<br>
**输出**：输出是可直接用于标准 next-token prediction 的增强语料；文中称约 23B 个源 token 被转换为 42B-token 增强语料。

</div>

**直观理解**：注释像可删除的旁注：如果旁注不能帮助预测后文，就不加入；如果加入，则原文仍完整保留，只是在相关位置前增加解释。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 句子级困惑度

$$
\bar{\ell}_j=\frac{1}{|I_j|}\sum_{t\in I_j}\ell_t,\qquad P_j=\exp(-\bar{\ell}_j),\qquad \ell_t=\log p_{\mathrm{ppl}}(x_t\mid x_{<t})
$$

**符号说明**

- $D=(x_1,\dots,x_T)$：分词后的文档，包含 $T$ 个 token。
- $x_t$：文档在位置 $t$ 的 token。
- $x_{<t}$：位置 $t$ 之前的全部 token 前缀。
- $\ell_t$：PPL 模型对真实 token $x_t$ 给出的条件对数概率。
- $I_j$：第 $j$ 个句子所包含的 token 位置集合。
- $|I_j|$：第 $j$ 个句子的 token 数量。
- $\bar{\ell}_j$：第 $j$ 个句子的平均 token 对数概率。
- $P_j$：第 $j$ 个句子的困惑度；数值越大表示越难预测。

<div class="equation-explanation" markdown="1">

**直观理解**：先平均计算一个句子中各 token 的预测难度，再通过指数变换得到困惑度。句子级困惑度高，表示模型在该句的整体转折上更不确定，因此优先作为注释候选。<br>
**原文位置**：第 3.2 节，公式 (1)—(3)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：REER-PT 本身是离线数据构造方法，不改变预训练的训练目标。增强语料固定后，模型仍以标准 next-token prediction 最大化真实后续 token 的条件概率；注释通过被插入序列而间接成为可预测上下文，而不是要求训练阶段执行在线推理 rollout。论文摘录未给出完整的参数化交叉熵公式，但明确说明增强语料“can be used directly with the standard next-token prediction objective”。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. PPL 模型**

PPL 模型提供 token 级条件概率，用于计算句子级困惑度、排序插入位置，并评价候选注释条件下的续写困惑度。若使用目标模型本身作为 PPL 模型，位置选择和优化是 on-policy；若使用独立模型，则属于 off-policy。

> 直观理解：它既负责寻找模型觉得困难的文本转折，也负责检验某条注释是否真的让后文更容易预测；因此它是整个数据筛选过程的评分器。

**2. 注释模型**

注释模型负责语境可推断性检查、生成多条初始注释，以及在每轮中为某个段落生成候选改写。论文强调其具体模型选择具有灵活性，而不是将其限定为某种固定架构。

> 直观理解：它相当于解释者：先判断前后文是否存在可解释联系，再尝试写出多种桥接说明，但最终是否采用由 PPL 模型而非主观判断决定。

**3. REER 式搜索与泄漏过滤**

候选注释空间无法穷举，因此方法采用有限候选集上的迭代、无梯度坐标式改写搜索；每轮比较改写候选与当前注释的续写困惑度。长度过滤控制注释规模，目标泄漏过滤防止候选通过直接重复 $y_i$ 而获得虚假的困惑度收益。

> 直观理解：系统不尝试搜索所有可能的解释，而是从几条初稿出发逐段修改；同时禁止“把答案写进提示里”，以确保收益来自解释关系而非偷看目标。

**训练与推理**

离线阶段首先用 PPL 模型对源文档进行 token 级评分和句子级排序，再由注释模型完成可推断性筛选、初稿生成、长度与目标泄漏过滤，以及基于续写困惑度的多轨迹迭代改写。最终注释插入源文档并固定为增强语料；之后可用普通预训练流程训练目标语言模型，推理阶段不需要运行 REER-PT，也不需要特殊的推理架构或在线注释生成。

**复现信息**

复现或解释结果时需要保留以下关键设置：候选位置是句首，文档长度为 $T$ 时目标位置数为 $K=\lfloor T/1000\rfloor$；候选注释通常限制在 500—1,000 个词，并使用 `<annotation_begin>` 与 `<annotation_end>` 标记；注释按段落逐段改写，每轮将当前版本纳入候选集，以保证续写困惑度不会因该轮选择而上升。PPL 模型的选择决定 on-policy 或 off-policy 性质，且不同模型或训练检查点可能产生不同的位置和改写信号；摘录未明确报告注释模型、PPL 模型的具体型号、候选数量、改写步数和完整训练超参数。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 源预训练语料：原始规模为 23B tokens；实验中一份混合语料将其与 500B-token 通用预训练语料结合，形成约 523B tokens 的 raw mixture，另一份则用 42B-token 增强语料替换 23B-token 源语料，形成约 542B tokens 的 REER-PT mixture。其作用是检验插入推理注释后的源语料是否带来下游收益。
- 通用预训练语料：规模为 500B tokens，在两种预训练混合物中均保持不变，用于控制总体训练背景，使主要差异来自源语料是否经过 $REER$-PT 增强。
- 公共下游基准：知识类包括 C-Eval、MMLU-Pro、SuperGPQA 和 Chinese SimpleQA；通用推理类包括 DROP、BBH、ZebraLogic 和 ProcBench；STEM 推理类包括 GPQA-Diamond、MATH 和 OlympiadBench；代码生成类包括 MBPP+、HumanEval+ 和 LiveCodeBench。原文未明确报告这些基准的具体样本规模、划分方式或是否使用额外训练集。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**困惑度（PPL）**

用 PPL 模型衡量模型对目标 token 的预测不确定性；实验分别在完整增强数据、仅原始 token 和被选中的续写 $y_i$ 上计算。 （越低越好，因为较低的 PPL 表示目标续写更容易由上下文预测。）

</div>
<div class="metric-item" markdown="1">

**精确 13-gram 重复率与注释到源文档重叠率**

自重复率衡量文本中重复出现的 13-gram occurrence 占比；注释到源文档重叠率 $R_{m cross}$ 衡量注释中的 13-gram 有多少也精确出现在对应源文档中。无空格语言在适用时改用字符 13-gram。 （越低越好：低自重复率表示增强文本不重复，低重叠率表示注释不是从源文档大段照抄。）

</div>
<div class="metric-item" markdown="1">

**公共基准准确率或任务得分**

在四类下游任务上报告 0–100 分数，并以增强模型分数减去 raw baseline 分数的百分点差值 $Delta$ 表示变化。 （越高越好；正的 $Delta$ 表示增强模型优于 raw baseline，但不同基准的任务形式并不完全相同，因此不宜把各分数直接横向比较。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 困惑度：No annotation 与 Optimized 的全增强数据比较

<div class="result-value" markdown="1">

完整增强数据的 PPL 从 18.68824 降至 11.40323，降低 7.28501；仅原始 token 的 PPL 从 18.68824 降至 17.65746，降低 1.03078。后者说明新增注释提供的上下文也改善了模型对未修改源文本的预测。

</div>

这是最直接的数据分析证据：最终注释不仅自身可能更流畅、更易预测，而且能帮助模型预测后续原始内容。不过，完整数据上的大幅下降部分可能来自注释文本本身较容易预测，因此不能单独证明模型获得了更强的外部知识或推理能力；原始 token 范围的下降更能支持上下文连接被改善这一解释。

<div class="result-source" markdown="1">

来源：第 4.1 节，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At the global scope, the optimized condition reduces full augmented-data PPL by 7.28501 and original-token PPL by 1.03078 relative to no annotation.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 重复与复制检查：源文档、最终注释及注释到源文档的精确重叠

<div class="result-value" markdown="1">

源文档自重复率为 0.615%，注释自重复率为 0.203%，注释到源文档的精确 13-gram 重叠率为 0.051%。这些结果表明最终注释的内部重复和对源文本的逐字复制都较少。

</div>

该分析检验增强数据是否只是机械重复或复制原文，而不是检验注释内容是否事实正确、推理是否有效。低重叠率支持“注释重构上下文与续写之间连接”的数据形态，但不能排除语义层面的重复，也不能证明所有注释都具有高质量。

<div class="result-source" markdown="1">

来源：第 4.1 节，Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The mean annotation-to-source exact-overlap ratio is 0.051%, indicating that only a small fraction of annotation 13-gram occurrences exactly match a source span.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 受控预训练与公共基准评测：augmented-data model 对比 raw baseline

<div class="result-value" markdown="1">

增强模型在知识、通用推理和 STEM 推理基准上均报告正增益，其中 BBH 和 GPQA-Diamond 各提升 2.07 个百分点，MATH、OlympiadBench 和 DROP 分别提升 1.50、1.49 和 1.40 个百分点；但代码基准全部下降：MBPP+ 下降 2.65、HumanEval+ 下降 1.83、LiveCodeBench 下降 1.79 个百分点。

</div>

结果支持该增强方式对多类知识与推理任务可能有帮助，且最大提升达到 2.07 个百分点。但收益并不普遍：代码任务的系统性下降说明把自然语言推理注释插入代码文档可能破坏局部程序结构。由于两种混合物分别约为 523B 和 542B tokens，训练 token 总量并未完全匹配，因此结果不能只归因于注释内容本身，也不能据此断言所有任务都会受益。

<div class="result-source" markdown="1">

来源：第 4.2 节，Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

However, all three code-generation benchmarks decline. The changes are−2.65points on MBPP+,−1.83points on HumanEval+, and−1.79points on LiveCodeBench.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 增强模型使用约 542B tokens，而 raw baseline 使用约 523B tokens；作者明确说明两者总 token 数不同。因此下游增益同时可能受到新增注释内容和更多训练 token 的影响，当前实验未完全隔离这两个因素。
- 实验摘录未报告下游基准的具体评测协议、随机种子或多次运行方差，也未提供代码文档专用注释格式的对照；因此结果的统计稳定性、可复现性以及代码任务退化的确切因果机制仍需进一步验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- raw baseline：在 23B-token 源语料加 500B-token 通用语料上从头训练的 680M 参数模型，是评估数据增强效果的主要对照；其余架构、分词器、优化器配置和训练超参数与增强模型一致。
- augmented-data model：在 42B-token REER-PT 增强语料加 500B-token 通用语料上训练的 680M 参数模型。它不是无变化的严格等 token 对照，因为增强语料包含新增注释，最终混合物约为 542B tokens。
- No annotation：只保留源文档的条件，用于比较插入最终注释前后的困惑度变化。
- Initial：插入经过初步过滤但尚未完成困惑度引导精炼的注释，用于隔离后续优化与筛选步骤的额外作用。

**实验想回答的问题**

- 将经过 $REER$ 注释增强的预训练语料用于标准下一词预测，是否能提高文本续写的可预测性，并且这种提升是否作用于原始文本而非仅作用于新增注释？
- 在架构、分词器、优化器和其他训练超参数保持一致的条件下，$REER$-PT 是否能改善知识、通用推理、科学推理和代码生成基准上的模型性能？

**实验实现**

数据分析阶段比较 No annotation、Initial 和 Optimized 三种注释条件；Optimized 是经过困惑度引导精炼、长度与目标泄漏约束过滤，并与无注释条件比较后保留的最终注释。PPL 分别按完整数据、原始 token 和 selected continuations 三种范围计算。重复率使用滑动窗口提取的 13-gram，并对每个文档或注释的比率取算术平均。预训练阶段从头训练两个 680M 参数模型，二者采用相同架构、分词器、优化器配置及其他训练超参数；作者还通过 raw training loss、gradient norm 和训练 100B consumed tokens 后的指数移动平均损失观察训练动态。下游评测覆盖知识、通用推理、STEM 推理和代码生成四类基准。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 初始注释 Initial 与最终注释 Optimized 的困惑度比较 | 相对于 Initial，Optimized 将完整增强数据 PPL 从 11.89156 降至 11.40323，降低 0.48833；将原始 token PPL 从 18.07970 降至 17.65746，降低 0.42224；在 selected continuations 上从 21.93265 降至 20.54801，降低 1.38464。 | 该比较主要隔离困惑度引导精炼和最终筛选，而不是单纯隔离“是否插入注释”。结果表明，初步生成和过滤后的注释仍可通过目标续写的 PPL 信号进一步改进；selected continuations 上的下降最大，符合优化过程直接针对这些续写进行筛选的设计。但这仍是数据层面的 PPL 证据，不等于下游模型性能必然同幅度提升。 | 第 4.1 节，Table 1<br><span class="experiment-evidence">Relative to the initial condition, perplexity-guided refinement further reduces full augmented-data PPL by 0.48833 and original-token PPL by 0.42224.</span> |
| 代码生成任务作为任务类型敏感性分析 | 增强模型在 MBPP+、HumanEval+ 和 LiveCodeBench 上分别比 raw baseline 低 2.65、1.83 和 1.79 个百分点；原文未明确报告针对代码文档禁用注释或使用专门注释格式的独立对照。 | 这不是完整的模块消融，而是对方法适用边界的关键分组分析。代码任务全部下降，提示自然语言注释可能与可执行代码的局部结构冲突，并可能诱使模型生成解释性文字而非严格合法的程序。由于没有代码专用格式的对照，现有结果只能定位问题，不能证明改变格式就一定能消除退化。 | 第 4.2 节，Table 3 后讨论<br><span class="experiment-evidence">Our case-level analysis suggests that inserting natural-language annotations into code documents can disrupt local program structure and encourage models to mix explanatory text with executable code.</span> |

**定性案例**

- 作者的案例级分析认为，在代码文档中插入自然语言注释会破坏局部程序结构，并使模型倾向于把解释文本与可执行代码混合输出；因此模型即使表达了看似合理的解法，也可能无法通过要求简洁且语法有效程序的代码基准。该解释与三个代码基准一致，但所给摘录未提供具体代码样例或逐例统计。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It proposes a pre-training data augmentation framework that inserts reverse-engineered reasoning annotations to improve continuation prediction and downstream reasoning.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`cb9b59067f63548d4513fa80290bca29ca0f5ada0cfe23c28c338c978508a170`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
