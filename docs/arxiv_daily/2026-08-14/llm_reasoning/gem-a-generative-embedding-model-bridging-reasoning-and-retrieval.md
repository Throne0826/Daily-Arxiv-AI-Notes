---
title: "[论文解读] GEM: A Generative Embedding Model Bridging Reasoning and Retrieval"
description: "[arXiv 2608.13200][LLM Reasoning] GEM试图让检索模型先利用自身的生成能力推理用户意图与相关性条件，再把推理后的上下文编码为向量，从而缩小复杂自然语言需求与文档匹配机制之间的理解差距。"
arxiv_id: "2608.13200"
announcement_date: "2026-08-14"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T03:04:18.296785+00:00"
source_sha256: "06676c2f1844c7316f2130f8586b84b1a147b693e9e84b5a7b35bbd900f2bbfb"
tags:
  - "LLM Reasoning"
  - "生成式嵌入模型"
  - "神经信息检索"
  - "推理密集型检索"
  - "指令遵循检索"
  - "查询理解"
  - "稠密检索"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.13200</p>

# GEM: A Generative Embedding Model Bridging Reasoning and Retrieval

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Zhili Shen, Craig Macdonald</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of Glasgow</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13200v1) · [PDF 下载](https://arxiv.org/pdf/2608.13200v1) · **关键词** 生成式嵌入模型, 神经信息检索, 推理密集型检索, 指令遵循检索, 查询理解, 稠密检索<br>
**代码**: [https://anonymous.4open.science/r/GEM](https://anonymous.4open.science/r/GEM)

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

GEM试图让检索模型先利用自身的生成能力推理用户意图与相关性条件，再把推理后的上下文编码为向量，从而缩小复杂自然语言需求与文档匹配机制之间的理解差距。

**不用术语来说**：用户现在会用完整指令表达复杂需求，例如同时说明目标、偏好和限制，但常规检索器往往只判断查询与文档在用词或整体语义上是否相似。当答案需要推断隐含意图、消解模糊表达或核对细微约束时，表面上相似的文档未必真正符合要求，而措辞不同的文档反而可能相关。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出生成式嵌入模型GEM，在同一模型中统一因果语言建模与向量表示学习，使模型能够先生成有关用户意图和相关性标准的推理，再通过嵌入标记将扩充后的上下文编码用于检索。
- 提出以经过验证的推理为条件的数据合成策略：正例与推理结论一致，困难负例保持主题相近但包含细微矛盾，以训练嵌入表示关注真实相关性条件，而非仅依赖词汇或粗粒度语义重合。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于神经信息检索与大语言模型交叉领域。现代用户会用自然语言指令表达复杂的信息需求，其中可能包含隐含意图、偏好、排除条件和其他相关性标准；但传统检索器主要依据查询与文档之间的词汇重合或语义相似度进行匹配。当相关文档与查询表述并不直接对齐时，系统还需推断用户真正想找什么、哪些约束必须满足。论文重点考察两类场景：需要超越表层匹配的推理密集型检索，以及要求检索器遵循查询特定约束的指令遵循检索。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**稠密检索与双编码器**

稠密检索将查询和候选文档分别编码为向量，再依据向量相似度排序；分别处理两端的结构通常称为双编码器。它便于预先计算文档向量并进行大规模检索，但向量是否表达了复杂意图和约束取决于训练方式。

</div>
<div class="concept-item" markdown="1">

**推理密集型检索**

这类任务中的查询与相关文档可能只有较低的词汇或直接语义相似度，因此检索器必须经过额外推断才能确定相关性。典型难点包括识别隐含意图、补足中间关系，以及判断文档是否真正满足查询条件。

</div>
<div class="concept-item" markdown="1">

**指令遵循检索**

除主题匹配外，用户还可通过查询特定的自然语言指令规定相关性标准，例如偏好易懂内容或排除技术术语。检索器不仅要理解检索主题，还要同时执行这些偏好、限制和否定条件。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定自然语言查询，以及可能随查询提供但不完整或含歧义的检索指令，系统需要从候选文档集合中返回并排序符合用户真实意图与相关性标准的文档。本文假设仅依靠查询和文档的表层词汇或语义相似度不足以完成上述任务，因此研究一种统一模型：先利用模型自身的生成能力推理用户意图及相关性条件，再将扩充后的上下文编码为检索表示。核心研究问题是，推理能否真正改变检索器对相关性及约束的理解，而不只是通过增加与相关文档的词汇或语义重合来获得表面收益。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **ReasonIR（Shao et al., 2025）**: ReasonIR使用困难查询训练基于大语言模型的稠密检索器，并显示由上游大语言模型生成的推理可增强检索。它与本文最直接的区别是采用分离的推理与检索流程，而GEM试图在单一模型内生成推理并形成与该推理对齐的嵌入；原文同时指出，已有方法的提升究竟来自推理理解还是额外的表层重合仍不明确。
- **Promptriever（Weller et al., 2025b）**: Promptriever是允许用户通过提示指定相关性标准的双编码器，例如用自然语言说明何种文档才相关。本文认为现实用户可能缺乏领域知识，所给指令常不充分或有歧义，因此进一步研究由生成式嵌入模型主动推理用户意图和相关性标准，而非完全依赖用户精确定义检索条件。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型的推理和指令遵循能力改变了用户表达信息需求的方式，查询因而变得更自然、更复杂，也更常包含隐含目标、个性化偏好和多项约束。检索器若仍主要比较查询与文档的词汇或语义相似度，就可能无法判断文档是否真正满足这些条件，造成用户表达能力与检索系统理解能力之间不断扩大的落差。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **外部推理增强的检索流水线**：先由上游大语言模型针对复杂查询生成解释、推理或查询扩展内容，再由独立检索模型使用这些内容查找文档，以补充原查询中没有直接出现的意图和概念。
- **指令跟随型稠密检索器**：将查询及其特定指令编码为连续向量，使检索器不仅表示主题，还尝试表示用户在该次查询中提出的偏好与约束，并据此和文档向量进行匹配。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 外部推理增强方法把推理与检索分配给不同模型，未利用检索模型自身的生成能力；而且性能提升可能只是因为生成文本增加了查询与相关文档的词汇或语义重合，尚不能证明检索表示真正理解了推理中的相关性逻辑。
- 现有指令跟随检索能够编码较详细的查询特定指令，但真实用户指令往往不完整或有歧义；推理是否可以帮助检索器补足隐含条件、消解歧义并更准确地执行约束，仍缺少系统研究。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作尚未建立一种由单个模型同时完成查询推理与嵌入表示、并让检索表示与该模型自身推理结果明确对齐的机制。尤其缺少证据说明：在不依赖独立上游推理模型的情况下，嵌入模型能否利用自身生成的意图分析和相关性标准，改善推理密集型及指令跟随型检索。

</div>
<div markdown="1"><span>核心问题</span>

能否在一个嵌入模型中保留大语言模型的生成与推理能力，使其先解释查询中的真实意图和相关性条件，再将推理扩充后的上下文编码为检索向量，并由此获得优于不推理版本的检索效果及可通过提示增加测试时计算的能力？

</div>
<div markdown="1"><span>作者直觉</span>

检索错误常常不是因为模型完全不认识查询主题，而是因为它没有显式判断“什么条件才算相关”。先生成意图与判定标准，相当于让模型在压缩查询为向量之前先整理需求；再用与这些推理一致的正例和主题相似但条件冲突的负例训练，能够迫使向量保留决定相关性的细节。由于推理和编码由同一模型连续完成，生成阶段形成的上下文还可直接用于构造最终表示，并可通过更有针对性的提示在测试时投入更多推理计算。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

GEM（Generative Embedding Model）以查询 $q$ 和文档语料库 $\{d_i\}_{i=1}^{N}$ 为输入，将查询先与元指令 $I$ 拼接为提示 $p=I\circ q$，再生成关于用户意图和相关性标准的响应 $r$。模型把 $p\circ r$ 的隐藏表示编码为查询向量，并把文档 $d$ 编码为文档向量，最终依据余弦相似度进行稠密检索。训练阶段同时优化响应生成的因果语言建模损失和查询-文档对比损失，使模型既保留生成能力，又学习与推理后意图相匹配的向量空间；直观地说，GEM 先把用户“真正想找什么”说清楚，再用这份扩展后的需求去搜索文档。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造查询提示并生成推理响应

将二者拼接为 $p=I\circ q$，由生成模型按照 $r\sim P_{\theta}(\cdot\mid p)$ 产生响应 $r$；训练数据生成阶段对每个查询采样 $K=8$ 个候选响应。

<div class="method-step__io" markdown="1">

**输入**：训练或推理查询 $q$，以及提示查询所需的元指令 $I$。<br>
**输出**：包含用户意图、相关性标准或任务解释的响应 $r$，以及训练阶段的候选集合 $\mathcal{R}_q$。

</div>

**直观理解**：这一步要求模型先解释查询，而不是直接依赖查询中的表面词汇。类似于检索员先把用户的口头需求改写成明确的检索条件。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 过滤并对齐生成响应

对每个候选响应判断 $f(r^{(k)},d^{+})\in\{0,1\}$；仅保留满足 $f(r^{(k)},d^{+})=1$ 的响应，形成 $\tilde{\mathcal{R}}_q$，再随机选取一个有效响应。若有效集合为空，则丢弃该查询；随后根据响应生成与其相关的正例文档和不满足意图或部分标准的困难负例文档。

<div class="method-step__io" markdown="1">

**输入**：候选响应 $r^{(k)}$、原始正例文档 $d^{+}$ 以及二元相关性分类器 $f$。<br>
**输出**：对齐的训练样本 $\mathcal{T}=\{(p,r,d^{+},d^{-})\}$，其中正负文档与生成的推理标准相匹配。

</div>

**直观理解**：模型生成的解释可能会误解原问题，因此先检查原正例是否仍然符合这份解释，再生成更细致的正负文档。这样可以减少“解释说的是一件事、标签实际表示另一件事”的训练噪声。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 联合训练生成器与嵌入器

对响应 token 计算因果语言建模损失；在响应末尾追加专用 token $\texttt{<|embed|>}$，用其最后位置隐藏状态得到 $E_{\theta}(p_i\circ r_i)$，并用文档侧提示得到 $E_{\theta}(d)$，再以 InfoNCE 损失拉近正例、推远负例，最后按 $\mathcal{L}_{GEM}=\lambda_{gen}\mathcal{L}_{gen}+\lambda_{emb}\mathcal{L}_{emb}$ 联合优化。

<div class="method-step__io" markdown="1">

**输入**：批次中的提示-响应对 $\{(p_i,r_i)\}_{i=1}^{N}$、正例文档 $d_i^{+}$、困难负例和批内负例。<br>
**输出**：能够生成响应并将推理增强后的查询和相关文档映射到相近向量位置的参数 $\theta$。

</div>

**直观理解**：同一个模型承担两个职责：语言建模保证它不会失去解释和生成能力，对比学习则教它把符合需求的文档排在前面。专用嵌入 token 像一个“读取整段解释后的摘要位置”，用于提取检索向量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成后编码并检索

推理时先生成 $r$，再在其末尾追加 $\texttt{<|embed|>}$，复用生成过程的 KV cache 计算查询表示；文档只需使用文档提示和嵌入 token 编码一次，并按照 $s_{\theta}(p\circ r,d)=\cos(E_{\theta}(p\circ r),E_{\theta}(d))$ 排序。

<div class="method-step__io" markdown="1">

**输入**：测试查询 $q$ 和文档语料库 $\{d_i\}_{i=1}^{N}$。<br>
**输出**：按相关性排序的前 $k$ 个文档，其中 $k\ll N$。

</div>

**直观理解**：查询端先思考再搜索，文档端不需要生成文字，只需提前转换成向量。检索时比较查询向量和所有文档向量的方向是否接近，取最相近的前 $k$ 个。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### GEM联合训练目标

$$
\mathcal{L}_{GEM}=\lambda_{gen}\mathcal{L}_{gen}+\lambda_{emb}\mathcal{L}_{emb}
$$

**符号说明**

- $\mathcal{L}_{GEM}$：GEM 的总训练损失。
- $\mathcal{L}_{gen}$：响应生成的因果语言建模损失，用于保持模型的 token 预测能力。
- $\mathcal{L}_{emb}$：查询-文档嵌入的对比学习损失，用于学习相关性排序。
- $\lambda_{gen}$：生成损失的权重。论文实现中设为 $0.1$。
- $\lambda_{emb}$：嵌入损失的权重。论文实现中设为 $1.0$。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标把“生成正确响应”和“让正例比负例更接近”合成一次优化。论文将生成项赋予较小权重，是因为响应来自同一骨干模型，主要训练目的仍是获得有效的检索嵌入，同时避免生成能力遗忘。<br>
**原文位置**：第 3.2 节，式（5）

</div>

</div>

<div class="equation-block" markdown="1">

#### InfoNCE嵌入损失

$$
\displaystyle\mathcal{L}_{emb}=-\frac{1}{N}\sum_{i=1}^{N}\log\frac{\exp\big(s_{\theta}(p_{i}\circ r_{i},d_{i}^{+})/\tau\big)}{\sum_{d\in\mathcal{D}_{i}}\exp\big(s_{\theta}(p_{i}\circ r_{i},d)/\tau\big)}
$$

**符号说明**

- $\mathcal{L}_{emb}$：一个批次上的嵌入对比损失。
- $N$：批次中的提示-响应样本数。
- $p_i$：第 $i$ 个查询与元指令拼接形成的提示。
- $r_i$：第 $i$ 个提示对应的生成响应。
- $d_i^{+}$：第 $i$ 个样本的相关正例文档。
- $\mathcal{D}_i$：第 $i$ 个样本的候选文档集合，由正例 $\{d_i^{+}\}$ 和负例 $\mathcal{D}_i^{-}$ 组成。
- $\mathcal{D}_i^{-}$：第 $i$ 个样本的负例集合，包括困难负例和批内负例。
- $s_{\theta}(p_i\circ r_i,d)$：模型参数为 $\theta$ 时，推理增强查询与文档 $d$ 的相似度。
- $\tau$：控制相似度分布平滑程度的温度超参数，论文实现中设为 $0.02$。

<div class="equation-explanation" markdown="1">

**直观理解**：对每个推理增强查询，损失要求其正例文档在所有候选文档中获得更高的 softmax 概率。困难负例用于检验细粒度意图是否满足，批内负例则以同一批其他样本的文档增加区分压力。<br>
**原文位置**：第 3.2 节，式（3）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：GEM 的优化目标是最小化 $\mathcal{L}_{GEM}$，其中 $\mathcal{L}_{gen}$ 对响应中的每个 token 计算因果语言建模负对数似然，$\mathcal{L}_{emb}$ 则通过 InfoNCE 使 $E_{\theta}(p_i\circ r_i)$ 更接近 $E_{\theta}(d_i^{+})$，并远离困难负例与批内负例。训练使用共享的提示-响应批次；论文设置 $\lambda_{gen}=0.1$、$\lambda_{emb}=1.0$、温度 $\tau=0.02$，因此整体上以检索嵌入学习为主、以生成建模作为正则化。其关键约束是生成损失不作用于 $\texttt{<|embed|>}$，因为该 token 只用于提取表示而不是由解码器预测。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 元指令驱动的生成式查询嵌入**

GEM 将用户查询与元指令组成 $p=I\circ q$，生成响应 $r$，并编码拼接序列 $p\circ r$。模型不使用生成结束符 $\texttt{EOS}$ 作为嵌入位置，而是在响应后追加专用 token $\texttt{<|embed|>}$，使用该位置的隐藏状态进行最后 token pooling；生成完成后可复用 KV cache。

> 直观理解：传统嵌入通常只读取原始查询，GEM 让模型先把隐含需求展开，再从展开后的完整上下文提取向量。专用 token 将“生成文本”和“读取向量”两个用途分开，避免干扰正常的结束符预测。

**2. 响应与相关性的两阶段数据对齐**

第一阶段从 $P_{\theta}(\cdot\mid p)$ 采样多个响应，并以 LLM 相关性分类器检查原正例在响应条件下是否仍相关；第二阶段以响应为条件生成正例和困难负例，并过滤与指定相关性不一致的文档。最终训练数据同时包含 Promptriever 的推理丰富样本、原始非推理样本和 ReasonIR 的困难查询样本。

> 直观理解：只让模型自由生成解释会产生幻觉或偏题，因此先做粗粒度筛选，再让正负文档体现解释中的细节标准。前者防止明显矛盾，后者处理“主题相似但不满足具体要求”的困难区分。

**3. 联合生成-对比学习**

生成损失在响应 token 上进行，嵌入损失使用正例、困难负例和批内负例构成的候选集合；两者通过权重 $\lambda_{gen}$ 和 $\lambda_{emb}$ 合并。训练时共享提示-响应批次，使生成损失可复用计算嵌入所需的隐藏状态。

> 直观理解：如果只训练向量相似度，模型可能忘记如何生成可靠解释；如果只训练生成，又不会自然获得适合检索的向量空间。两个目标共同训练，使模型在“会思考”和“会排序”之间保持平衡。

**训练与推理**

训练时，先从 Promptriever 和 ReasonIR 查询构造提示，并为每个查询采样响应；通过原正例相关性判断保留有效响应，再以响应为条件生成或复用正例和困难负例，形成 $\mathcal{T}$。模型对提示-响应序列计算 $\mathcal{L}_{gen}$，同时用末尾的 $\texttt{<|embed|>}$ 隐藏状态计算查询嵌入，用文档侧提示计算文档嵌入，再计算 $\mathcal{L}_{emb}$ 并联合反向传播。训练还加入约 $60,000$ 个原始非推理样本，使部分查询直接使用文档侧提示进行标准对比学习；最终训练集为约 $370,000$ 个样本，其中约 $260,000$ 个来自 Promptriever 的推理子集、约 $60,000$ 个原始样本、约 $50,000$ 个 ReasonIR 困难查询样本。推理时，对每个查询使用元指令生成 $r$，默认采用贪心解码，生成结束后追加 $\texttt{<|embed|>}$ 并复用 KV cache 计算查询向量；文档向量预先编码，随后按余弦相似度排序。由于模型具有生成能力，还可以通过增加推理时的生成长度或计算预算进行 test-time compute scaling，但生成更长响应会增加每个查询的编码时间。

**复现信息**

论文使用 Qwen3-4B-Instruct-2507 作为 GEM 骨干；训练 500 步，单设备批大小为 $8$，梯度累积 $32$ 步，在 2 张 GPU 上形成有效批大小 $512$。文档和提示-响应序列的最大长度均为 $1024$ token，使用 Adam、学习率 $1\times10^{-5}$ 和 50 步 warmup；采用 FSDP、CPU offloading、梯度检查点和 bfloat16，训练在 2 张 NVIDIA H100 上完成，论文报告 GEM 约需 14 小时。数据生成阶段每个查询采样 $8$ 个响应，响应采样温度为 $1.0$；正例和困难负例文档由 Llama-3.1-8B-Instruct 以贪心解码生成，但 Promptriever 中已存在的指令丰富文档子集不再重复生成。评估时默认贪心解码，最大生成长度为 $1024$，生成后编码批大小为 $16$，关闭生成时文档和查询编码批大小为 $32$；具体检索指标和数据集的官方评估实现由 BRIGHT、FollowIR 和 InstructIR 等项目提供，所给章节未明确报告各检索数据集的具体指标名称。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- BRIGHT用于推理密集型检索评测，由12个子集组成，覆盖生物学、地球科学、经济学、心理学、机器人、Stack Overflow、可持续生活、LeetCode、Pony、数学奥赛以及两种科学定理问答设置。它检验模型能否超越表面词匹配，通过理解问题和相关性条件找出文档；原文报告各子集及其平均$nDCG@10$，但所给节选未列明查询数、语料规模或具体划分。
- FollowIR与InstructIR共同用于指令跟随检索。FollowIR包含News21、Core17和Robust04，既考查常规排序质量，也通过改变检索指令考查模型是否真正响应相关性要求；InstructIR基于MS MARCO，为同一查询配置代表不同用户情境的多条提示，检验效果及最差提示条件下的稳健性。原文节选未明确报告这些评测集的实例规模。
- TREC-DL-2019和TREC-DL-2020使用含$8.8$M段落的MS MARCO语料，作为非推理密集型补充评测。它们用于判断GEM的推理生成机制是否只对专门设计的复杂任务有效，或者在常规段落排序上也能带来收益。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**nDCG@$k$**

归一化折损累计增益，综合考虑相关文档是否被排在前列以及相关性等级；BRIGHT和InstructIR使用$nDCG@10$，FollowIR的News21使用$nDCG@5$。 （越高越好，因为高相关文档越靠前，折损后的累计收益越大。）

</div>
<div class="metric-item" markdown="1">

**MAP@1000**

对每个查询计算前$1000$名的平均准确率，再跨查询取均值；用于FollowIR的Core17与Robust04，衡量相关文档在整个较深排名中的分布质量。 （越高越好，因为它表示相关文档更早且更持续地出现在结果列表中。）

</div>
<div class="metric-item" markdown="1">

**p-MRR与Robustness@10**

两者都补充常规排序指标对指令敏感性不足的问题。FollowIR的$p$-MRR取值为$[-100,100]$，衡量指令变化后排名是否按预期改变；InstructIR的Robustness@10取同一查询在不同用户提示下的最低$nDCG@10$，反映最不利提示条件下的质量。 （均为越高越好：较高$p$-MRR表示模型更能遵从指令变化，较高Robustness@10表示跨用户情境的最差表现更可靠。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### BRIGHT上的检索质量与端到端延迟

<div class="result-value" markdown="1">

GEM在生成预算$n=64$时达到$nDCG@10=27.3$，与BRIGHT/ReasonIR式两阶段提示基线相同；其单查询延迟为$2.85$秒，作者报告约$20\times$加速。

</div>

作者据此主张，GEM能用较短的内部推理达到长查询扩展流水线的检索质量，说明联合训练的生成与嵌入接口可能更有效率。该结果不表示生成式检索已接近纯嵌入的毫秒级速度，也不能直接外推到不同GPU、批量或推理引擎，因为测量仅覆盖单张L40S上的$128$个BRIGHT查询。

<div class="result-source" markdown="1">

来源：Appendix B.4, Figure 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Compared with the baseline prompting approach used in BRIGHT and ReasonIR, GEM achieves the same nDCG@10 of 27.3 with a much smaller generation budget ($n=64$), reducing inference latency to 2.85 seconds.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 非推理密集型TREC-DL检索

<div class="result-value" markdown="1">

在TREC-DL-2019上，GEM的$nDCG@10$为$70.4$，高于GEM w/o generation的$67.4$，但低于RepLLaMA的$74.5$和Promptriever的$73.2$；在TREC-DL-2020上，GEM取得$73.6$，高于GEM w/o generation的$65.8$、RepLLaMA的$71.8$和Promptriever的$72.3$。

</div>

这说明测试时生成并非只对BRIGHT式复杂推理查询有用，在常规MS MARCO段落排序上也可能改善表示；尤其DL-2020上的增益较明显。不过两个年份的结果并不一致地超过全部$7$B基线，且这里只比较最终分数，不能排除训练数据、模型规模和训练方案差异的影响。

<div class="result-source" markdown="1">

来源：Appendix B.5, Table 10

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Model | DL-2019 | DL-2020; RepLLaMA | 74.5 | 71.8; Promptriever | 73.2 | 72.3; DIVER-4B | 67.8 | 63.6; Qwen3-4B-Instruct | 69.0 | 69.1; GEM w/o generation | 67.4 | 65.8; GEM | 70.4 | 73.6

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 统一模型保留生成能力的补充评测

<div class="result-value" markdown="1">

相对其Qwen3-4B-Instruct骨干，GEM在ARC-Challenge上的准确率从$43.3$提高到$48.0$，在GSM8K上的链式思维精确匹配率从$76.9$提高到$82.1$。

</div>

作者将其解释为：加入嵌入训练后，GEM没有牺牲生成能力，反而在两个推理基准上有所提升。这一证据支持“生成与嵌入可由单一模型兼顾”，但不能证明提升必然来自检索训练中的某个具体组件；节选也未提供多次运行方差或显著性检验。

<div class="result-source" markdown="1">

来源：Appendix B.1, Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In particular, GEM shows substantial gains on the evaluated reasoning benchmarks, improving accuracy on ARC-Challenge from 43.3 to 48.0 and EM score on GSM8K from 76.9 to 82.1.

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

- Qwen3-4B-Instruct是GEM的$4$B骨干，同时作为嵌入基线；与它比较可以判断收益是否来自GEM训练及推理增强，而不只是更大的基础模型。GEM w/o generation则关闭推理生成，更直接地隔离测试时生成的作用。
- ReasonIR-8B是面向推理密集型检索训练的双编码器，但自身不生成推理。它是有意义的外部基线，因为比较目标是检验一个较小的生成式嵌入模型能否达到专用、较大检索模型的水平；所给节选没有提供其完整主表分数。
- Promptriever是面向指令检索训练的非生成式双编码器。它检验GEM保留指令微调语言模型能力并自行补全相关性标准，是否比仅编码用户所给指令更有效；同时，GEM大量采用其训练数据，因此比较也需要注意共享数据来源。
- BRIGHT与ReasonIR采用的两阶段提示流水线，以同一个Qwen3-4B骨干先生成查询扩展，再由GEM的嵌入-only变体编码。该基线与GEM使用相同的推理器和下游编码规模，主要用于比较达到相同检索质量时的生成预算与延迟。

**实验想回答的问题**

- GEM先生成对查询意图与相关性标准的推理，再据此形成向量表示，是否能在推理密集型、指令跟随型及常规段落检索中优于不生成推理的嵌入模型？
- GEM的效果是否依赖特定损失权重或骨干模型，以及通过增加测试时生成计算量获得的检索收益需要付出多大延迟代价？

**实验实现**

GEM由Qwen3-4B-Instruct-2507初始化，训练$500$步，有效批量为$512$，学习率为$1\times10^{-5}$并预热$50$步；每个查询使用一个正例和一个困难负例，同时汇集跨GPU的批内负例。默认生成损失权重为$\lambda_{gen}=0.1$、嵌入损失权重为$\lambda_{emb}=1.0$，对比学习温度为$\tau=0.02$；训练约需两张NVIDIA H100运行$14$小时。训练集共$370$K样本，包括Promptriever来源的$260$K推理样本、$60$K原始样本，以及基于ReasonIR困难查询构造的$50$K推理样本。每个查询由骨干以温度$1.0$采样$K=8$个响应，再由同一骨干贪心过滤；Llama-3.1-8B-Instruct为每个响应生成一个正例和一个困难负例。检索评测中的GEM推理统一采用贪心解码。延迟实验从BRIGHT随机抽取$128$个查询，在单张NVIDIA L40S、批量$1$、最大生成及嵌入截断长度$8192$下测量，且未使用vLLM或FlashAttention等推理优化。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 生成损失权重$\lambda_{gen}\in\{0.01,0.03,0.1,0.3,1.0\}$ | FollowIR平均Score在五种权重下分别为$26.6$、$25.4$、$25.5$、$26.3$和$25.7$，平均$p$-MRR分别为$12.4$、$11.4$、$11.7$、$10.5$和$10.5$；InstructIR的$nDCG@10$分别为$83.9$、$88.3$、$87.5$、$86.8$和$87.1$，Robustness@10分别为$49.2$、$56.2$、$54.8$、$52.2$和$53.3$。作者认为没有单调趋势，且$\lambda_{gen}\in\{0.03,0.1,0.3\}$时较稳定。 | 该消融隔离生成目标在联合损失中的相对强度。不同数据集的最佳权重并不相同，说明默认$\lambda_{gen}=0.1$是折中选择，而非所有指标的最优点；中等范围内变化较小，则表明主要结论不依赖极精细的权重调参。它没有移除生成损失，因此不能回答生成监督本身是否必要。 | Appendix B.2, Table 7 and Figure 4<br><span class="experiment-evidence">Setting \| FollowIR Average Score \| FollowIR Average p-MRR \| InstructIR nDCG@10 \| InstructIR Robust.@10; $\lambda_{gen}=0.01$ \| 26.6 \| +12.4 \| 83.9 \| 49.2; $\lambda_{gen}=0.03$ \| 25.4 \| +11.4 \| 88.3 \| 56.2; $\lambda_{gen}=0.1$ (default) \| 25.5 \| +11.7 \| 87.5 \| 54.8; $\lambda_{gen}=0.3$ \| 26.3 \| +10.5 \| 86.8 \| 52.2; $\lambda_{gen}=1.0$ \| 25.7 \| +10.5 \| 87.1 \| 53.3</span> |
| 更换骨干并比较自生成推理与Qwen3推理蒸馏 | 自生成设置下，Qwen3-4B版在FollowIR平均Score、平均$p$-MRR、InstructIR $nDCG@10$和Robustness@10上分别为$25.5$、$9.6$、$89.8$和$59.0$。Llama3.2-3B使用Qwen3数据蒸馏后对应为$25.9$、$9.6$、$86.4$和$51.2$；Gemma2-2B蒸馏版为$23.1$、$12.2$、$84.4$和$48.3$；Qwen2.5-3B蒸馏版为$24.6$、$10.5$、$88.1$和$55.5$。 | 该实验检验GEM是否绑定Qwen3骨干，以及学生模型能否使用强模型生成的推理进行训练。结果显示多种骨干均可训练且各有优势，但性能并非随模型选择一致变化：Llama3.2自生成版在InstructIR更强，蒸馏后部分指标下降；因此实验支持架构可迁移，而不支持蒸馏在所有任务上必然优于自生成。原文另称Llama3.2蒸馏版在BRIGHT更强，但节选没有给出Table 9的具体数字。 | Appendix B.3, Table 8<br><span class="experiment-evidence">Model \| FollowIR Average Score \| FollowIR Average p-MRR \| InstructIR nDCG@10 \| InstructIR Robust.@10; GEM (Qwen3-4B-Instruct) \| 25.5 \| +11.7 \| 87.5 \| 54.8; GEM (Llama3.2-3B-Instruct), corresponding backbone \| 25.5 \| +9.6 \| 89.8 \| 59.0; GEM (Llama3.2-3B-Instruct), Qwen3 distillation \| 25.9 \| +9.6 \| 86.4 \| 51.2; GEM (Gemma2-2B-Instruct), Qwen3 distillation \| 23.1 \| +12.2 \| 84.4 \| 48.3; GEM (Qwen2.5-3B-Instruct), Qwen3 distillation \| 24.6 \| +10.5 \| 88.1 \| 55.5</span> |

**定性案例**

- Pony子集构成一个失败案例：Promptriever在该子集仅有$1.7$ $nDCG@10$，不同骨干的GEM也普遍表现较差；作者据此推测Pony相对以MS MARCO/Promptriever为主的训练数据属于域外数据。该解释得到多种专有嵌入同样只有$1.5$至$3.6$的旁证，但仍是相关性观察而非受控因果验证，不能据此断言训练域差异是唯一原因。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：GEM uses explicit query reasoning and test-time reasoning compute within a generative language model to improve retrieval embeddings.; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`06676c2f1844c7316f2130f8586b84b1a147b693e9e84b5a7b35bbd900f2bbfb`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
