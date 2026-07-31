---
title: "[论文解读] RAGuard: A Layered Defense Framework for Retrieval-Augmented Generation Systems Against Data Poisoning"
description: "[arXiv 2607.26339][LLM 安全] RAGuard通过“检索阶段预先降权、生成阶段反事实过滤”的两层机制，防御恶意语料利用高相关性虚假文档操纵RAG事实问答的问题。"
arxiv_id: "2607.26339"
announcement_date: "2026-07-30"
primary_category: "llm_safety"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.872278+00:00"
source_sha256: "6402c6d246ac9f802df2bd4ce680435454a99599f4877db86d26a6735b142aac"
tags:
  - "LLM 安全"
  - "LLM 其他"
  - "检索增强生成"
  - "语料投毒"
  - "密集检索"
  - "分层防御"
  - "留一法反事实比较"
  - "黑盒过滤"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 安全 · arXiv 2607.26339</p>

# RAGuard: A Layered Defense Framework for Retrieval-Augmented Generation Systems Against Data Poisoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Pushkal Kumar, Tucker Nielson, Tanish Kolhe, Shubham Zala, Vincent Li</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26339v1) · [PDF 下载](https://arxiv.org/pdf/2607.26339v1) · **关键词** 检索增强生成, 语料投毒, 密集检索, 分层防御, 留一法反事实比较, 黑盒过滤<br>
**代码**: [https://github.com/RAGuard-AI/RAGuard](https://github.com/RAGuard-AI/RAGuard)  

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

RAGuard通过“检索阶段预先降权、生成阶段反事实过滤”的两层机制，防御恶意语料利用高相关性虚假文档操纵RAG事实问答的问题。

**不用术语来说**：RAG系统会先从外部资料库找出与问题相关的文档，再据此生成答案；如果攻击者能向资料库加入看似相关但内容虚假的文档，这些文档就可能被优先检索并诱导模型给出错误答案。困难在于，防御系统通常既不知道哪些文档有毒，也没有每个问题的标准答案，而且攻击形式还可能不断变化。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出两层防御框架：先用包含捏造事实、矛盾陈述和推理陷阱的合成毒文档对稠密检索器进行对抗式训练，使其在排序阶段压低可疑文档；再由ZKIP在生成前检查并移除仍然漏过检索器的异常文档。
- 作者提出无需毒性标签、标准答案或模型内部访问的黑盒ZKIP：逐一移除检索文档并重新生成答案，根据答案语义变化与输出不确定性变化识别可疑文档，从而面向训练时未见过的攻击形式提供推理时防线。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

检索增强生成（RAG）先从外部语料库中检索与用户问题相关的文档，再让大语言模型依据这些文档生成答案，从而补充模型参数中缺失或过时的知识。该机制同时引入了语料投毒风险：若攻击者能够向语料库写入内容，就可注入表面相关但包含虚假事实、矛盾信息或误导性推理的文档，使其进入检索结果并操纵最终答案。本文聚焦事实问答场景中的密集检索系统，目标是在恶意文档到达生成器之前降低其排名，并在生成阶段继续识别遗漏的可疑文档；其结论不直接覆盖观点操纵等其他攻击类型。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**密集检索（Dense Retrieval）**

密集检索器把问题和文档编码为向量，并按向量相似度选出最相关的若干文档。它能捕捉语义相似性，但也可能把语义上贴近问题、事实却被篡改的投毒文档排在前列。

</div>
<div class="concept-item" markdown="1">

**语料投毒（Corpus Poisoning）**

攻击者向RAG可检索的语料库注入恶意文档，使这些文档被检索并作为生成证据。本文研究的是事实性投毒，包括捏造事实、制造矛盾和设置推理陷阱。

</div>
<div class="concept-item" markdown="1">

**留一法反事实比较（Leave-One-Out Counterfactual Comparison）**

先用全部检索文档生成一次答案，再逐次移除其中一篇文档并重新生成，通过比较答案语义和输出不确定性的变化估计该文档的影响。这里的目的不是一般性的贡献归因，而是发现移除后会令答案更稳定或更确定的可疑文档。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括用户问题、可能被攻击者写入恶意内容的外部语料库、一个返回前若干篇相关文档的检索器，以及依据检索上下文回答问题的黑盒生成模型。攻击者构造保留问题关键词或语义相关性的虚假文档，试图提高其检索排名并诱导模型输出错误事实；防御方不应假设推理时拥有投毒标签、标准答案、外部判定器或生成模型内部参数。系统需要输出经过筛除或降权后的检索上下文及最终答案，并兼顾三项目标：降低攻击成功率、尽量保持正常相关文档的检索召回能力，以及支持训练阶段未见过的投毒形式。本文采用检索阶段与生成阶段分层防御，但明确将主要威胁范围限定为针对密集检索RAG的事实性语料投毒。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$k$**

每个问题送入生成阶段的顶部检索文档数量；ZKIP需基于完整上下文生成一次，并对每篇文档分别执行一次留一重生成。

</div>
<div class="notation-item" markdown="1">

**$k+1$**

ZKIP处理单个问题所需的生成器前向调用次数：一次使用全部文档，另有k次分别移除一篇文档。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{Recall@5}$**

前5个检索结果覆盖相关文档的召回指标，用于衡量防御是否破坏正常检索质量。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{ASR}$**

攻击成功率（Attack Success Rate），用于衡量投毒是否成功操纵系统输出；具体判定规则在所给背景章节中未明确报告。

</div>

</div>

**直接相关的工作**

- **PoisonedRAG（Zou et al., 2025）**: 该工作表明，向RAG语料库插入对抗性文档可以同时扰乱检索排序和生成结果，是本文所防御攻击面的直接代表。本文仅在受控的事实性投毒设置中进行研究，并指出仍需进一步用PoisonedRAG等完整攻击框架检验更广泛的鲁棒性。
- **FlippedRAG（Chen et al., 2025）**: 该工作研究黑盒观点操纵攻击。本文将观点操纵明确排除在威胁模型之外，因此它主要用于划定RAGuard结论的适用边界，而不是本文实验中已被充分覆盖的攻击基线。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

RAG依赖可更新的外部语料来补充大模型的参数化知识，但这种依赖同时开放了语料写入攻击面。攻击者只需注入少量与查询高度相关、却包含虚假或误导事实的段落，就可能让生成器把恶意内容当作证据。该风险直接削弱RAG用于事实问答时最重要的可信性，而且检索相关性本身无法区分“相关且真实”与“相关但有毒”。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **毒文档检测与检索器对抗训练**：检测式方法利用已标注毒样本或人工启发式规则过滤文档；检索器对抗训练则把合成毒文档作为困难负例，通过对比学习让稠密检索器降低这些文档的排名，尽量在生成之前阻断攻击。
- **生成器加固与推理阶段防御**：这类方法通过额外训练、验证或多次推理，使生成器减少对不可靠上下文的依赖。与普通相关性重排序不同，论文所需的推理防御必须判断某篇文档是否对答案产生异常影响，而不能只判断它与查询是否相似。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 依赖毒性标签、启发式规则或训练时合成攻击的防御容易学习特定攻击模式；当毒文档换一种伪装方式时，检测器可能失效，对抗训练过的检索器也仍可能把未见类型的毒文档送入生成器。
- 仅加固生成器通常带来较高推理成本，并可能在毒文档占据检索结果多数时退化；更根本的是，既有单点机制通常只保护检索或生成中的一个阶段，无法同时处理前端漏检和后端受误导的问题。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种覆盖检索与生成两个阶段的互补防御：它既要在检索端主动压低已知类型的毒文档，又要在推理端不依赖毒性标签、标准答案、外部事实裁判或模型内部参数，识别并过滤绕过检索器的未知攻击。论文将范围明确限定为稠密检索RAG中的事实型语料投毒，而非宣称解决所有RAG安全问题。

</div>
<div markdown="1"><span>核心问题</span>

能否构建一种分层RAG防御，使检索器先学习排斥典型毒文档，并让一个黑盒、无标签的推理时补丁仅通过比较“使用全部文档”与“逐篇移除文档”后的模型自身输出，发现残余毒文档，同时尽量保持正常证据的检索质量？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把每篇检索文档视为一次可撤销的干预：分别观察保留它和移除它时，模型答案的语义与不确定性如何变化。正常证据即使重要，其移除未必会让模型同时变得更稳定、更确定；毒文档则常通过制造错误方向或冲突来扰乱生成，因此移除后更可能出现答案显著变化且不确定性下降。前层负责拦截训练中可模拟的攻击，后层只看文档造成的行为后果，两者因依据不同而具有互补性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

RAGuard在标准检索增强生成（RAG）流程中加入两层互补防御。输入用户查询后，第一层使用经过对抗微调的稠密检索器，根据查询与文档向量的余弦相似度排序候选文档；训练时，它直接比较原始正确文档与三类合成投毒改写，使正确文档的得分至少比投毒版本高出给定间隔。第二层ZKIP在生成阶段对前k篇文档逐一进行留一法反事实测试：分别移除一篇文档并重新解码，以答案语义变化和输出熵变化衡量该文档对模型输出的异常影响，随后删除被标记的文档，再用剩余上下文完成最终生成。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造带投毒对照的训练数据

抽取30%的查询—文档对，并让LLM将正确文档分别改写为事实捏造、关键事实矛盾或误导推理三类投毒文档，三类样本均匀分配。每条记录同时保留查询、未修改的正确文档、投毒改写及攻击类别，以便组成显式的正负训练三元组。

<div class="method-step__io" markdown="1">

**输入**：Natural Questions（NQ）或BEIR中的查询—原始正确文档对。<br>
**输出**：包含查询q、正确文档$d^{+}$和负文档$d^{-}$的训练三元组；投毒样本的$d^{-}$是对应正确文档的恶意改写，干净样本的$d^{-}$是语料库内随机抽取的干净文档。

</div>

**直观理解**：这一步为同一问题制作“正确版本”和“有迷惑性的错误版本”，让检索器学习二者之间最关键的语义差异，而不只是学习一般的主题相关性。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 对抗微调稠密检索器

将查询、正确文档和负文档编码为稠密向量，用余弦相似度计算匹配程度，并通过间隔为0.2的三元组损失优化参数，使正确文档得分高于负文档。对投毒三元组，负例就是该正确文档的攻击式改写，因此优化信号直接针对投毒内容。

<div class="method-step__io" markdown="1">

**输入**：干净与投毒训练三元组，以及由all-MiniLM-L6-v2初始化的查询和文档编码器。<br>
**输出**：能够主动降低已见类型投毒文档排名的对抗检索器。

</div>

**直观理解**：普通检索器只需要找到“看起来相关”的文档，而这里还要求它把内容相似但事实被篡改的文档压到正确版本之后。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 检索候选上下文

分别编码查询与文档，按二者向量的余弦相似度排序，并选取前k篇文档。该层首先阻断训练分布内的已知投毒模式，但作者明确指出它可能无法覆盖未见攻击或分布外样本。

<div class="method-step__io" markdown="1">

**输入**：用户查询q和待检索的外部文档语料库。<br>
**输出**：供生成模型使用、但尚未完全信任的top-k候选文档集合。

</div>

**直观理解**：第一层相当于一道经过恶意样本训练的入口筛查，但不会假设所有危险文档都能在入口处被识别。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### ZKIP留一法反事实过滤

先在完整上下文上解码，再对每篇候选文档各执行一次移除该文档后的留一解码，并依据移除前后的答案语义偏移和输出熵变化为文档评分；异常影响较大的文档被标记并删除。所给节选未提供两类信号的精确合成公式、阈值设定或具体语义度量，因此不能据此进一步还原评分算法。

<div class="method-step__io" markdown="1">

**输入**：top-k候选文档、用户查询和可黑盒调用的生成模型。<br>
**输出**：过滤后的上下文集合及各候选文档的反事实影响判定。

</div>

**直观理解**：它逐篇追问：“如果拿掉这篇文档，模型的答案会不会异常地大变？”一篇投毒文档若要攻击成功，通常必须显著操纵答案，这种影响正是第二层试图捕捉的信号。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 三元组间隔损失

$$
\mathcal{L}=\max\!\bigl(0,\;s(q,d^{-})-s(q,d^{+})+0.2\bigr)
$$

**符号说明**

- $\mathcal{L}$：单个查询—正例—负例三元组的训练损失。
- $q$：用户查询。
- $d^{+}$：与查询对应的未修改正确文档，即应当获得更高排名的正例。
- $d^{-}$：负例文档；对投毒三元组是$d^{+}$的攻击式改写，对干净三元组是随机抽取的语料库内干净文档。
- $s(q,d)$：查询q与文档d的余弦相似度。
- $0.2$：要求正例相似度超过负例相似度的间隔超参数。

<div class="equation-explanation" markdown="1">

**直观理解**：若正确文档的得分已经比负文档高至少0.2，损失为零；否则就产生与差距不足程度相对应的惩罚。对投毒样本而言，这直接迫使模型把内容非常相近但事实被篡改的版本排在原始正确文档之后。<br>
**原文位置**：第3.3节“Retriever fine-tuning”，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 查询—文档余弦相似度

$$
s(q,d)=\cos\bigl(f_{\theta}(q),g_{\theta}(d)\bigr)=\frac{f_{\theta}(q)\cdot g_{\theta}(d)}{\lVert f_{\theta}(q)\rVert\,\lVert g_{\theta}(d)\rVert}
$$

**符号说明**

- $s(q,d)$：查询q与文档d的检索匹配分数。
- $f_{\theta}$：参数为$\theta$的查询编码映射，将查询转换为稠密向量。
- $g_{\theta}$：参数为$\theta$的文档编码映射，将文档转换为稠密向量。
- $\cdot$：两个向量的内积。
- $\lVert\cdot\rVert$：向量的欧几里得范数，用于消除向量长度对分数的影响。
- $\theta$：在对抗微调中被优化的编码器参数。

<div class="equation-explanation" markdown="1">

**直观理解**：该分数衡量查询向量与文档向量的方向是否一致，越接近1通常表示语义越相似。它既是文档排序依据，也是三元组损失比较正负文档的基础，但仅靠语义相似度仍可能把保留关键词的投毒文本排到前列，因此需要定向训练和ZKIP补充。<br>
**原文位置**：第3.3节“Retriever fine-tuning”，公式(2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练只针对第一层稠密检索器：最小化三元组间隔损失，使$s(q,d^{+})$至少比$s(q,d^{-})$高0.2。对抗鲁棒性的核心来自负例采样而非新的网络结构——在投毒三元组中，$d^{-}$是对应正确文档的特定攻击改写，因而梯度直接惩罚检索器偏好捏造、矛盾或错误推理文本；在干净三元组中，随机语料负例维持一般检索区分能力。作者不用InfoNCE及批内负例，是因为随机共现文档可能被无差别地当作困难负例，而显式间隔更直接地表达正确版本与其投毒改写之间的排序要求。ZKIP在推理阶段不使用投毒标签或标准答案，所给材料也未表明其需要参数训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 攻击定向的稠密检索器**

基础编码器为all-MiniLM-L6-v2，查询编码器$f_{\theta}$与文档编码器$g_{\theta}$产生向量表示，并以余弦相似度排序。其关键并非模型结构本身，而是负例设计：投毒训练样本将同一正确文档的恶意改写作为$d^{-}$，从而用三元组间隔损失明确要求模型区分真实内容与高度相关的篡改内容。

> 直观理解：随机负例通常很容易区分，不能教会模型识别“主题完全正确、事实却被改动”的危险文本；成对的投毒改写提供了更有针对性的训练题。

**2. 三类合成投毒生成器**

投毒构造覆盖fabrication、contradiction和reasoning三类攻击：分别加入虚假陈述、翻转关键事实词，以及插入误导逻辑步骤或错误中间结论。作者选择自行生成这些样本，是为了统一覆盖三类参数化攻击、精确控制5%至30%的实验投毒比例，并在NQ和BEIR上构造跨领域数据。

> 直观理解：三类攻击分别破坏“事实内容”“关键真假”和“推理过程”，使训练不依赖单一固定模板；但它们仍是LLM改写，而非通过梯度搜索得到的最强攻击。

**3. 零知识推理补丁ZKIP**

ZKIP是无投毒标签、无标准答案且无需访问模型内部参数的黑盒过滤器。它把各篇文档视作可移除的上下文因素，通过完整解码与k次留一解码之间的语义变化和输出熵变化，估计每篇文档对答案的反事实影响，并在最终解码前移除异常文档。

> 直观理解：该模块不判断文档本身“像不像假消息”，而是观察它是否不正常地左右模型回答。因此，即使某种投毒形式未在检索器训练时出现，只要它必须强烈改变答案才会奏效，就仍可能被发现。

**训练与推理**

训练阶段先从原始语料生成三类投毒改写，并以30%的投毒训练三元组、三类均分的方式微调检索器；投毒三元组使用成对恶意改写作为负例，干净三元组使用随机干净负例。推理阶段先由微调检索器返回top-k文档，再由ZKIP执行一次完整上下文解码和每篇文档一次留一解码，根据语义偏移及输出熵变化移除异常文档，最后在过滤后的上下文上生成答案。两层的职责边界明确：检索器主动压低训练中见过的投毒模式，ZKIP则作为黑盒、攻击无关的后置安全网；不过作者同时承认，检索器在基于正确文档改写的合成投毒上训练，可能部分记忆训练查询的相关性，尚不能据此声称可泛化到未见领域。

**复现信息**

检索器以all-MiniLM-L6-v2初始化，采用最后隐藏状态均值池化、AdamW优化器、学习率$2\times10^{-5}$、批大小16、训练3个epoch、最大序列长度256，三元组间隔为0.2；这些设置足以复现所述第一层训练。数据方面，文中构造12,344条BEIR样本（其中3,700条投毒）和1,000条NQ样本（其中300条投毒），实验可按5%至30%比例替换投毒三元组。推理的主要成本是k+1次生成器调用，k=5时为6次；所给节选没有完整报告ZKIP的阈值、语义相似度实现、熵计算粒度、解码参数或早停规则，复现第二层前必须回查论文未提供的后续方法章节。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Natural Questions（NQ）：主题覆盖广的开放域问答数据。实验构造干净语料以及投毒比例为 5%、10%、20%、30% 的语料版本，并为每篇文档保存投毒标签。Recall@5 和 MRR 在完整的 1,000 个查询上计算；不同投毒比例下分别有 33、69、139、190 个查询检索到了投毒候选，可用于计算 ASR。NQ 是端到端防御效果的主要测试集。
- BEIR 的 NFCorpus：医疗与科学领域检索基准，相关性信号比 NQ 稀疏，用于考察防御信号及对抗训练能否迁移到领域外语料。正文报告干净语料和 30% 投毒语料的检索结果，其中有 2,481 个可计算 ASR 的查询；ZKIP 防御结果尚未完成。
- 监督式投毒分类数据：由 NQ 和 BEIR 中带有真实投毒标签的金标准文档—投毒文档样本及检索文档特征组成。它只用于验证文本和 ZKIP 反事实特征是否具有可学习性，属于需要标签的分析性上界，不是论文主张的零标签部署方案。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Recall@5**

金标准相关文档出现在前五个检索结果中的查询比例，衡量检索器是否仍能把正确证据放入生成器可见的候选集合。 （越高越好；较高值表示更多查询能够检索到正确证据，但不直接保证生成答案正确。）

</div>
<div class="metric-item" markdown="1">

**MRR**

每个查询首篇相关文档排名倒数的平均值，用于同时衡量是否检索到相关文档以及其排序是否靠前。 （越高越好；相关文档排名越靠前，其倒数排名越大。）

</div>
<div class="metric-item" markdown="1">

**ASR**

投毒文档排名高于金标准文档并且成功误导生成器的查询比例。附录说明，该指标在检索候选中实际出现投毒文档的查询上计算。 （越低越好；零表示在已评估样本中没有观测到同时满足高排名与误导生成的成功攻击，但不等于对所有攻击类型具有形式化安全保证。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### NQ，10% 语料投毒：干净训练的稠密检索器与对抗训练检索器分别在无防御和加入 ZKIP 时比较。

<div class="result-value" markdown="1">

Dense（clean）无防御时 Recall@5、MRR、ASR 分别为 0.259、0.176、0.101；加入 ZKIP 后前两项保持为 0.259、0.176，ASR 降至 0.000。Dense（adv-trained）无 ZKIP 时为 0.319、0.215、0.072；加入 ZKIP 后为 0.314、0.215、0.000。

</div>

作者结果表明，对抗训练本身降低了该条件下的攻击成功率，并提高了检索指标，但仍有攻击成功；ZKIP 则消除了本次评估中观测到的成功攻击，且对对应检索器的 Recall@5 影响很小。分析上，这支持“检索阶段加固与生成后反事实过滤互补”，但 ASR 为零只适用于已测试的样本、生成器和事实型攻击，不能解释为普遍安全证明。

<div class="result-source" markdown="1">

来源：Table 1，Section 4.3 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Dense (clean) | None | 0.259 | 0.176 | 0.101
Dense (adv-trained) | None | 0.319 | 0.215 | 0.072
Dense (clean) | ZKIP | 0.259 | 0.176 | 0.000
Dense (adv-trained) | ZKIP | 0.314 | 0.215 | 0.000

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### NQ，30% 语料投毒：比较三类检索器加入 ZKIP 前后的高投毒比例表现。

<div class="result-value" markdown="1">

无 ZKIP 时，BM25、Dense（clean）和 Dense（adv-trained）的 ASR 分别为 0.011、0.053、0.068；加入 ZKIP 后三者的 ASR 均为 0.000。Dense（clean）加入 ZKIP 后 Recall@5/MRR 保持在 0.256/0.175；Dense（adv-trained）则由无 ZKIP 的 0.318/0.212 降至 0.274/0.196。

</div>

该条件显示 ZKIP 的零观测 ASR 不局限于 10% 投毒比例，也能覆盖不同检索器；但高投毒比例下，对抗训练检索器加入 ZKIP 后出现较明显的检索质量下降。因此，“攻击被过滤”与“正确证据仍被保留”需要分开评价，不能只看 ASR。

<div class="result-source" markdown="1">

来源：Table 4，Appendix A

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

NQ (30%) | BM25 | 0.071 | 0.059 | 0.011
NQ (30%) | Dense (clean) | 0.256 | 0.175 | 0.053
NQ (30%) | Dense (adv-trained) | 0.318 | 0.212 | 0.068
NQ (30%) | BM25 + ZKIP | 0.071 | 0.059 | 0.000
NQ (30%) | Dense (clean) + ZKIP | 0.256 | 0.175 | 0.000
NQ (30%) | Dense (adv-trained) + ZKIP | 0.274 | 0.196 | 0.000

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### BEIR（NFCorpus），30% 语料投毒：检验检索器对医疗/科学领域外语料的稳健性。

<div class="result-value" markdown="1">

BM25 的 Recall@5/MRR/ASR 为 0.016/0.013/0.000；Dense（clean）为 0.021/0.015/0.008；Dense（adv-trained）为 0.019/0.014/0.007。对抗训练只将 ASR 从 0.008 降到 0.007，未表现出有意义的领域外改善。

</div>

作者将其解释为：NQ 上训练出的检索器加固不能可靠迁移到稀疏相关性的医疗/科学语料，而关键词保持型投毒对 BM25 的影响仍很小。由于该数据集的 ZKIP 防御运行尚未完成，这组结果不能证明 ZKIP 在 BEIR 上有效或无效，只能评价检索器及对抗训练层。

<div class="result-source" markdown="1">

来源：Table 5，Appendix A

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

BEIR (30%) | BM25 | 0.016 | 0.013 | 0.000
BEIR (30%) | Dense (clean) | 0.021 | 0.015 | 0.008
BEIR (30%) | Dense (adv-trained) | 0.019 | 0.014 | 0.007

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

- BM25：基于词项匹配的词法检索器。它用于判断保留查询关键词的投毒文本是否会影响传统词法检索，并作为与稠密语义检索器不同的参照。
- Dense（clean）：只用干净训练三元组训练的稠密检索器，是衡量语料投毒影响以及 ZKIP 单独贡献的主要基线。
- Dense（adv-trained）：使用合成投毒文档进行对抗微调的稠密检索器，用于检验第一层防御能否在检索阶段主动降低恶意文档排名；名称表示检索器接受过防御性训练，而非其权重遭到攻击。
- 监督分类基线：附录分别采用文档文本级 BERT 分类器，以及基于 ZKIP 影响特征的逻辑回归和 BERT 分类器。它们用于验证投毒结构是否可学习，而非与无标签 ZKIP 进行同等部署条件下的直接比较。

**实验想回答的问题**

- 在攻击者只能向语料库写入虚假事实、矛盾或错误推理文本，而不能修改模型、查询和提示词的条件下，对抗训练检索器与生成后过滤器 ZKIP 能否降低事实型语料投毒的攻击成功率，同时尽量保持正常相关文档的检索能力？
- ZKIP 所依据的反事实影响信号——移除单篇文档后答案语义及输出熵的变化——是否确实包含可用于识别投毒文档的结构化信息，并且是否比仅分析文档文本更有效？

**实验实现**

每个查询检索 k=5 篇文档。主流程的生成器为 GPT-4o-mini，温度为 0.2、top-p 为 0.95、最多生成 128 个 token；答案语义表示由 all-MiniLM-L6-v2 计算。批量特征提取实验另用 FLAN-T5-small。ZKIP 对完整候选上下文生成一次答案，再分别移除每篇候选文档进行留一法解码，因此标准设置每个查询需要 k+1=6 次生成。实验比较干净语料、投毒语料以及加入 ZKIP 后的设置；NQ 的防御运行只报告已完成的 10% 和 30% 条件，未完成的条件不作估计。威胁模型仅覆盖事实型语料投毒，不覆盖观点操纵、提示注入、检索干扰、后门触发、对抗查询和白盒梯度攻击。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 文本级 BERT 投毒分类：在 NQ 的金标准文档与投毒文档对上，仅依据文档文本识别投毒。 | 在 NQ 5% 至 30% 投毒比例下，精确率约为 0.843–0.853，但召回率仅为 0.220–0.228；AUPRC 为 0.717–0.720，ROC-AUC 为 0.685–0.690。 | 该消融隔离了“只看文档文字表面是否足够”这一因素。高精确率但低召回率意味着分类器只敢标记少数明显样本，许多保留原文风格和关键词的细微事实篡改会被漏检。因此，结果支持引入文档对生成答案实际影响的反事实信号；但它没有直接比较相同训练条件下的文本特征与 ZKIP 特征，不能据此量化两者的纯粹因果差距。 | Table 7，Appendix D.2<br><span class="experiment-evidence">Across NQ, AUPRC remains stable at ≈ 0.717–0.720 over poisoning ratios from 5% to 30%, with ROC-AUC ≈ 0.685–0.690 (Table 7). Precision is high (≈ 0.84–0.85) but recall is low (≈ 0.22–0.23): the classifier is conservative, flagging only a limited subset of poisons.</span> |
| ZKIP 影响特征的监督分类：比较线性逻辑回归与能够建模非线性交互的 BERT 分类器。 | 逻辑回归的 AUPRC、ROC-AUC、F1 分别为 0.377、0.571、0.514；BERT 分别提升到 0.732、0.814、0.636，召回率也由 0.614 提升到 0.792。 | 该消融检验 ZKIP 衍生信号是否只是简单的单变量阈值，还是需要组合答案稳定性、检索排名和相似度等线索。非线性模型显著优于线性模型，说明特征间交互具有信息量。不过这些分类器使用投毒标签训练，部分完整特征还依赖金标准答案，因此只是机制验证和监督上界，不能替代无标签、黑盒的 ZKIP。 | Table 8，Appendix D.3<br><span class="experiment-evidence">A logistic-regression baseline achieves AUPRC 0.377 and ROC-AUC 0.571, while the BERT-based classifier improves substantially to AUPRC 0.732 and ROC-AUC 0.814, with F1 increasing from 0.514 to 0.636 (Table 8).</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Proposes and evaluates a layered defense against corpus-poisoning attacks on retrieval-augmented LLM systems.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`6402c6d246ac9f802df2bd4ce680435454a99599f4877db86d26a6735b142aac`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
