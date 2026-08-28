---
title: "[论文解读] Reasoning about In-Context Samples for Machine-Translation"
description: "[arXiv 2608.27036][LLM Reasoning] 本文研究如何让大语言模型显式分析翻译记忆库中的相似双语样例，先提取可复用的源语—目标语片段，再以这些片段作为推理轨迹生成译文。"
arxiv_id: "2608.27036"
announcement_date: "2026-08-28"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:39:06.528489+00:00"
source_sha256: "dee334c43231ca12be3a50f673cf95903392e6359effce219525466cf0d216e1"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型机器翻译"
  - "翻译记忆库"
  - "检索增强机器翻译"
  - "上下文学习"
  - "片段提取"
  - "思维链"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.27036</p>

# Reasoning about In-Context Samples for Machine-Translation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Maxime Bouthors, Josep Crego, François Yvon</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: ‡ Sorbonne Université, CNRS, ISIR, F-75005 Paris, France；Sorbonne Université, CNRS, ISIR, F-75005 Paris, France</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27036v1) · [PDF 下载](https://arxiv.org/pdf/2608.27036v1) · **关键词** 大语言模型机器翻译, 翻译记忆库, 检索增强机器翻译, 上下文学习, 片段提取, 思维链<br>
**代码**: [https://github.com/Maxwell1447/Fragment-Based-Reasoning](https://github.com/Maxwell1447/Fragment-Based-Reasoning)

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

本文研究如何让大语言模型显式分析翻译记忆库中的相似双语样例，先提取可复用的源语—目标语片段，再以这些片段作为推理轨迹生成译文。

**不用术语来说**：专业翻译经常参考过去已经人工确认的相似译文，但模型即使看到了这些样例，也未必知道其中哪些词组真正适用于当前句子：直接照搬可能引入无关内容，完全依赖自由生成又可能错失经过验证的术语和表达。本文要解决的是，能否训练模型先从若干相似样例中找出可信、可复用的对应片段，再据此完成当前翻译。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出面向翻译记忆增强机器翻译的片段式推理框架：模型显式执行片段提取，将检索样例中的双语对应片段作为中间推理轨迹，并利用这些片段生成最终译文。
- 把片段匹配转化为可监督学习的问题：由较大的教师模型生成银标片段与草稿，再通过监督蒸馏训练较小的学生模型，并围绕多样例噪声、跨领域与跨语言适用性检验这一思路。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型机器翻译、上下文学习与翻译记忆库增强翻译的交叉点。机器翻译系统需要把当前源语言句子转换为目标语言句子；在专业翻译场景中，翻译记忆库保存经过人工确认的源文—译文对，可为当前句子提供可靠的术语、固定表达和文体参照。常规上下文学习只是把若干相似历史译例放入提示，让模型自行决定如何利用；本文则把这种利用过程显式化为“片段提取”：模型先在当前源句与检索译例之间识别可复用内容，并从译例两侧抽取对应的源—目标片段，再以这些片段作为中间推理轨迹生成最终译文。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**翻译记忆库增强机器翻译（TM-augmented MT）**

翻译记忆库（TM）由历史源句及其已验证译文组成；系统先检索与当前源句相近的译例，再借用其中可信的术语和短语。它尤其适合专业领域，因为历史译文通常已经满足领域术语和表达规范。

</div>
<div class="concept-item" markdown="1">

**上下文学习（In-Context Learning, ICL）**

上下文学习是在提示中提供若干输入—输出示例，使大语言模型无需再次更新参数便可模仿示例完成当前任务。在本文中，示例是从翻译记忆库检索到的源文—译文对，也称译例。

</div>
<div class="concept-item" markdown="1">

**思维链与片段提取（CoT / FE）**

思维链让模型在最终答案前生成中间“思考”文本；本文不要求模型泛泛描述翻译策略，而是让中间文本承担可检查的片段提取（FE）任务。FE旨在找出当前源句与译例源句共享的内容，以及该内容在译例目标侧的对应译法。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括待翻译的源句，以及外部检索模块从翻译记忆库中选出的一个或多个相似译例；每个译例均由源语言句子和对应目标语言译文组成。本文假定检索步骤已由外部模块完成，重点研究后续匹配与利用：模型首先判断当前源句中哪些片段能在译例源侧找到，并识别其目标侧对应片段；随后对这些片段进行选择、组合或必要的补全，生成完整目标译文，最终修订主要依赖大语言模型自身的生成能力。研究设置还关注三个条件：多个译例带来的信息与噪声能否被区分、片段推理是否真正改善译文质量，以及该能力能否跨语言和跨领域（包括微调时未见领域）泛化。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$k$**

为当前源句检索并提供给模型的翻译记忆库译例数量；文中图2以 $k=1$ 为例。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{TM}$**

翻译记忆库，即存储历史源文—目标译文对的数据库。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{FE}$**

片段提取步骤：从检索译例中识别可供当前翻译复用的平行源—目标片段。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{CoT}$**

思维链，即模型在输出最终译文之前生成的中间推理文本；本文将 FE 结果作为一种任务特定的推理轨迹。

</div>

</div>

**直接相关的工作**

- **检索增强机器翻译与编辑式机器翻译（Bulte and Tezcan, 2019；Gu et al., 2019）**: 检索增强方法把相似译例作为额外上下文，编辑式方法则从已有译文出发，识别应保留、修改或重译的部分。本文继承“复用相近译例”的问题设定，但不要求专门的编辑解码器，而是训练大语言模型先显式抽取平行片段，再据此自由生成完整译文。
- **面向机器翻译的推理与多步骤提示（Raunak et al., 2023；Zebaze et al., 2025a）**: 既有工作通常模拟术语分析、列举修改、草拟、润色或校对等人工翻译步骤，但已有结果表明通用思维链未必提升机器翻译质量。本文将推理约束为与检索译例直接相关、且较容易检查的 FE 中间任务，从而研究显式识别现有译文片段是否比自由生成分析或草稿更有效。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

翻译记忆库保存了已经验证的源语—目标语实例，尤其能提供专业领域所需的一致术语和惯用表达。然而，针对新句子检索到的样例通常只在局部相似，而且多个样例还会混入无关信息。实际需要的不只是把样例放进提示词，而是让模型透明地识别哪些局部双语对应值得复用，并在保留可靠表达的同时完成必要的改写与补全。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **标准上下文示例翻译**：先从翻译记忆库检索与当前源句相似的一个或多个双语实例，再把完整实例直接放入提示上下文，由大语言模型隐式判断如何利用其中的术语、措辞和风格来生成译文。
- **面向机器翻译的思维链或草稿—修订方法**：让模型在输出最终译文前生成语言分析、局部翻译或完整草稿，并可能继续执行修订；这类方法主要模仿人工译者的查词、分析、初译和复核过程。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 标准上下文学习把样例利用过程留在模型内部，没有显式完成“当前源句片段—样例源语片段—样例目标语对应片段”的匹配，因此难以确认模型是否复用了真实存在且经过验证的翻译，也难以解释或追踪其依据；当检索样例增多时，无关内容还可能成为噪声。
- 一般性的思维链和草稿方法主要增加分析或改写步骤，却没有专门建模翻译记忆使用中最关键的局部匹配与重组过程。因此，多生成一份草稿不等于能够从相似样例中筛出可靠的双语证据，甚至可能把低质量中间结果传递给最终译文。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有研究尚未明确证明：大语言模型能否被训练成从检索到的完整双语样例中可靠地识别而非凭空生成实际对应片段，以及这种显式片段轨迹是否比直接提供完整样例或生成普通草稿更有助于翻译。进一步未决的是，该机制能否在多个检索样例带来额外噪声时仍然有效，并能否迁移到不同语言和训练阶段未见领域。

</div>
<div markdown="1"><span>核心问题</span>

本文集中回答四个相互关联的问题：模型能否可靠执行片段匹配与提取；提取出的双语片段能否提高最终翻译质量；随着检索样例数$k$增加，模型能否从更多噪声中筛选有价值的信息；这种收益是否因语言、领域及领域是否在微调中出现而变化。

</div>
<div markdown="1"><span>作者直觉</span>

相似翻译样例通常不是整句都可复用，但其中若干术语和短语已由过去的翻译实践验证。先把这些局部对应显式抽取出来，相当于给生成器提供一组较短、与当前句子直接相关的“翻译零件”：模型无需同时消化所有完整样例，也更容易沿用可靠术语，再利用自身生成能力完成连接、变形和补全。即使片段并不完美，它们仍可能比未经筛选的整句样例提供更集中的条件信号。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把基于实例的机器翻译（Example-Based Machine Translation, EBMT）的“检索—匹配—重组—修订”过程显式化为可监督生成的推理轨迹。给定待译源句 $\mathbf{x}$ 以及从翻译记忆库中检索出的 $k$ 个相似双语样例 $E(k)=\{(\mathbf{x}_1,\mathbf{y}_1),\ldots,(\mathbf{x}_k,\mathbf{y}_k)\}$，强教师模型先把源句拆成较小的语义单元，为各单元生成或从样例中抽取对应译文，得到银标片段集合 $F$；随后将目标片段重组为草稿译文 $\tilde{\mathbf{y}}$。这些自动生成的片段和草稿不是人工金标，因此称为“银标”推理轨迹。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 检索上下文双语样例

使用 BM25 与 Levenshtein 距离检索和当前源句相似的平行句对，形成 $E(k)=\{(\mathbf{x}_i,\mathbf{y}_i)\}_{i=1}^{k}$；训练时对每个实例均匀采样 $k\in\{0,1,2,3\}$。

<div class="method-step__io" markdown="1">

**输入**：当前源句 $\mathbf{x}$、所属领域的平行语料池，以及允许的样例数 $k$。<br>
**输出**：待译句与最多三个相似的源—目标双语样例，它们共同构成教师或学生模型的条件输入。

</div>

**直观理解**：这一步相当于翻译前先查找翻译记忆：找到措辞或结构相近的旧句及其译文。样例只提供参考，不能直接当作当前句子的完整译文。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 教师生成银标双语片段

教师先将 $\mathbf{x}$ 分解为按原顺序排列的最小可译语义单元 $(u_1,\ldots,u_m)$，再为每个 $u_i$ 给出目标片段 $v_i$。目标片段可以直接见于样例、由相似样例片段适配而来，或在样例不足时由教师从头生成。

<div class="method-step__io" markdown="1">

**输入**：待译源句 $\mathbf{x}$ 与检索样例集合 $E(k)$。<br>
**输出**：银标片段集合 $F=\{(u_1,v_1),\ldots,(u_n,v_n)\}$，其中每一对记录一个源语义单元及其候选翻译。

</div>

**直观理解**：模型不是笼统地“参考几个例句”，而是明确指出当前句子的哪一小块可以怎样翻译。这样能把样例中真正有用的局部对应关系暴露出来，同时允许模型处理没有现成匹配的内容。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 教师重组片段并生成草稿

教师按目标语言的语法和语序重组各个 $v_i$，必要时加入衔接成分、改变形态、局部调整次序或改写，生成完整草稿 $\tilde{\mathbf{y}}$。

<div class="method-step__io" markdown="1">

**输入**：银标片段集合 $F$ 及原始上下文。<br>
**输出**：一条结构完整但仍作为中间推理结果的草稿译文 $\tilde{\mathbf{y}}$。

</div>

**直观理解**：把逐块翻译直接拼接起来通常不通顺，因此该步骤像编辑初稿一样处理词形、语序和缺失的连接词。草稿为最终译文提供全句级结构，而片段负责保留可追溯的局部依据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 学生学习推理轨迹并输出最终译文

学生模型按自回归顺序生成 $F\circ\tilde{\mathbf{y}}\circ\mathbf{y}$，并以交叉熵损失进行监督微调；其中 $\circ$ 表示文本序列拼接。论文还通过删除片段或草稿训练三个对照变体，以区分不同推理阶段的作用。

<div class="method-step__io" markdown="1">

**输入**：训练时输入 $\mathbf{x}$ 与 $E(k)$，监督目标为教师产生的 $F$、$\tilde{\mathbf{y}}$ 以及平行语料中的最终目标译文 $\mathbf{y}$；推理时只提供待译句和检索样例。<br>
**输出**：完整模型先产生片段和草稿，再给出最终译文 $\mathbf{y}$；对照模型则分别生成 $F\circ\mathbf{y}$、$\tilde{\mathbf{y}}\circ\mathbf{y}$ 或仅生成 $\mathbf{y}$。

</div>

**直观理解**：训练不是只告诉模型标准答案，而是让它模仿教师展示的中间步骤；使用时，学生能够自己写出这些步骤并据此翻译。几个删减版本相当于分别拿走“局部翻译笔记”或“全句初稿”，用于判断性能提升来自哪一部分。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### Fragments+Draft 条件生成模型

$$
p_{\theta}\!\left(F\circ\tilde{\mathbf{y}}\circ\mathbf{y}\mid\mathbf{x};\left((\mathbf{x}_{1},\mathbf{y}_{1}),\ldots,(\mathbf{x}_{k},\mathbf{y}_{k})\right)\right)
$$

**符号说明**

- $p_{\theta}$：参数为 θ 的学生语言模型给出的条件序列概率
- $\theta$：由监督微调更新的学生模型参数
- $\mathbf{x}$：当前需要翻译的源语言句子
- $(\mathbf{x}_{i},\mathbf{y}_{i})$：第 i 个检索样例的源句及其目标语言译文
- $k$：作为上下文提供的检索样例数量
- $F$：银标源—目标片段集合，由若干 ($u_i,v_i)$ 对组成
- $\tilde{\mathbf{y}}$：将目标片段重组并适配后得到的草稿译文
- $\mathbf{y}$：最终目标译文
- $\circ$：按生成顺序拼接文本序列的运算符

<div class="equation-explanation" markdown="1">

**直观理解**：该式规定学生在当前源句和检索样例的条件下，不直接只预测最终译文，而是依次预测片段、草稿和终译。由于前面生成的轨迹会成为后续生成的上下文，模型可以先明确局部翻译依据，再组织全句，最后完成修订。<br>
**原文位置**：第 3.3 节 Translating with Example-Based Reasoning

</div>

</div>

<div class="equation-block" markdown="1">

#### 选择性移除推理轨迹的生成变体

$$
\begin{aligned}p_{\theta}^{(F)}&=p_{\theta}\!\left(F\circ\mathbf{y}\mid\mathbf{x};E(k)\right),\\ p_{\theta}^{(D)}&=p_{\theta}\!\left(\tilde{\mathbf{y}}\circ\mathbf{y}\mid\mathbf{x};E(k)\right),\\ p_{\theta}^{(B)}&=p_{\theta}\!\left(\mathbf{y}\mid\mathbf{x};E(k)\right).\end{aligned}
$$

**符号说明**

- $p_{\theta}^{(F)}$：Fragments only 变体的条件生成分布，生成片段后直接生成终译
- $p_{\theta}^{(D)}$：Draft only 变体的条件生成分布，生成草稿后再生成终译
- $p_{\theta}^{(B)}$：Baseline 变体的条件生成分布，不产生显式推理轨迹
- $E(k)$：由 k 个检索双语样例构成的上下文集合
- $F$：源语义单元与对应目标片段组成的银标集合
- $\tilde{\mathbf{y}}$：片段重组所得草稿
- $\mathbf{y}$：最终译文

<div class="equation-explanation" markdown="1">

**直观理解**：三种变体改变的是需要学习和生成的中间序列，而不是翻译任务本身。它们分别检验局部片段监督是否足够、仅有全句草稿是否足够，以及不展示任何显式推理时的直接翻译能力；因此是方法组成层面的消融，而非不同检索数据之间的比较。<br>
**原文位置**：第 3.3 节 Translating with Example-Based Reasoning，Fragments only、Draft only 与 Baseline 条目

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：教师首先离线为平行训练样本生成银标 $F$ 和草稿 $\tilde{\mathbf{y}}$，从而把原本只有 $(\mathbf{x},\mathbf{y})$ 的翻译监督扩展为带中间轨迹的序列监督。学生在给定 $\mathbf{x}$ 与 $E(k)$ 时，以标准自回归交叉熵最小化目标序列各 token 的负对数似然；完整模型的目标顺序为 $F\circ\tilde{\mathbf{y}}\circ\mathbf{y}$，其余变体使用删去相应阶段后的序列。原文只明确说明“optimizing the cross-entropy loss”，未在所给章节中列出逐 token 损失公式或对不同阶段设置独立权重，因此不能推断片段、草稿和终译采用不同损失系数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 相似样例检索与上下文构造**

检索模块从同领域平行语料中结合 BM25 和 Levenshtein 距离寻找相似源句，并连同其目标译文组成 $E(k)$。训练语料覆盖 16 个语言—领域组合，每个训练实例使用随机数量的样例，使学生同时接触零样例和少样例条件。

> 直观理解：BM25 偏重共享词项，Levenshtein 距离衡量字符串编辑差异，二者共同帮助找到表面内容相近的旧译例。随机改变 $k$ 可避免模型只适应固定长度的提示，也让零检索结果成为训练中见过的情况。

**2. 教师式片段匹配与银标蒸馏**

强教师 LLM 在同一生成流程中完成源句分块、跨语言模糊匹配和目标片段选择，产出 $F$ 与 $\tilde{\mathbf{y}}$。该设计没有分别调用句法分析器、词对齐器或传统翻译表，而是用提示让教师模拟这些操作，并将整套平行训练语料扩展为带推理轨迹的监督数据。

> 直观理解：分块方式可能不唯一，源片段与样例译文也不一定严格逐词对应，因此用固定规则或普通词对齐很难稳健完成。教师模型在语义层面生成近似但可用的标注，代价是这些标注属于自动产生的银标，不能被视为人工验证的真实翻译推理。

**3. 片段—草稿—终译的分阶段解码**

完整的 Fragments+Draft 模型将三个输出阶段串接为 $F\circ\tilde{\mathbf{y}}\circ\mathbf{y}$：$F$ 提供局部源—目标对应，$\tilde{\mathbf{y}}$ 完成全句级重组，$\mathbf{y}$ 则是最终提交的译文。Fragments only、Draft only 和 Baseline 保持输入及训练数据来源一致，只选择性移除中间轨迹，以形成结构化消融。

> 直观理解：片段解决“样例中的哪些局部表达值得借用”，草稿解决“这些局部表达怎样组成合乎目标语言习惯的句子”，最终阶段再进行修订。分阶段输出使局部证据和全句组织各有明确位置，而不是要求模型把所有操作隐藏在一次直接生成中。

**训练与推理**

训练阶段分为教师标注与学生蒸馏两部分。首先，对每个平行样本构造含 $k\in\{0,1,2,3\}$ 个相似双语实例的输入；强教师按提示生成源—目标片段 $F$，再生成重组草稿 $\tilde{\mathbf{y}}$，与已有参考译文 $\mathbf{y}$ 串接成监督目标。随后从同一个现有学生 LLM 出发，分别微调 Fragments+Draft、Fragments only、Draft only 和 Baseline；四者均以源句和检索样例为条件并优化交叉熵，主要差别是目标中保留哪些推理段落。

推理阶段不再需要教师，也不预先提供银标轨迹。系统先为新源句检索 $E(k)$，学生根据所训练的输出格式自回归生成：完整模型依次产生 $F$、$\tilde{\mathbf{y}}$ 和 $\mathbf{y}$，最终只把 $\mathbf{y}$ 作为翻译结果；其他变体按各自的目标顺序生成。原文所给章节没有明确说明推理时的解码算法、温度、束搜索设置、停止条件，以及银标片段是否会在输出后接受格式校验，相关细节需查阅附录 D 后再复核。

**复现信息**

为公平理解方法，关键数据设置是：训练集包含英语与德语、法语、波兰语、乌克兰语和西班牙语的 16 个语言—领域组合，每个组合选取 10,000 条高质量样本，合并后共 160,000 条；相似样例从相应训练语料池检索，并明确排除开发集和测试集。每个领域另保留 100 条开发样本和 1,000 条测试样本，另有未进入训练数据的英法 GNOME “surprise”测试集用于考察跨未见领域的泛化。

检索同时使用 BM25 和 Levenshtein 距离，且训练时随机采用零至三个样例，这些设置直接决定学生看到的上下文形式。学生属于 Qwen3 模型家族，但所给方法与数据章节未明确列出具体参数规模、教师模型名称、提示模板、学习率、批大小、训练轮数和硬件；原文将教师信息指向附录 C，将微调与提示细节指向附录 D，因此仅凭当前节选无法完整复现实验，不能自行补充这些配置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 多领域平行语料覆盖英语到波兰语、西班牙语、乌克兰语、法语和德语等方向，共16个“语言方向—领域”组合；领域包括IT、法律、金融、医疗、宗教、政治、TED演讲、Wikipedia和字幕。它用于检验方法能否跨语言、跨专业领域稳定工作，而非只适配单一测试集。
- 训练数据先用OpusCleaner去除空句及长度不在4至150词范围内的句子，再用COMETKiwi过滤低质量平行句。每个领域按综合质量分选取1万条训练样本，最终拼接为16万条多语言训练集；该选择同时偏好平行质量高且翻译较困难的样本。
- 未预先划分的数据集使用每领域100条开发样本和1000条测试样本。训练、验证和测试实例均可从排除开发集与测试集的平行语料池中检索最多3个同领域相似示例，以避免直接把测试参考译文作为示例取回。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**BLEU**

基于候选译文与参考译文之间词片段重合度的自动指标，主要反映表层措辞和局部短语匹配。 （越高越好，因为更高分表示候选译文与参考译文具有更多匹配的词片段；但它不能充分判断语义等价或译文自然度。）

</div>
<div class="metric-item" markdown="1">

**COMET**

学习式机器翻译评价指标，用模型综合评估源句、候选译文与参考译文之间的语义和翻译质量。 （越高越好，因为更高分代表评价模型判断译文质量更高。）

</div>
<div class="metric-item" markdown="1">

**MetricX**

学习式翻译错误评价指标，本实验以向下箭头标注，数值用于反映模型预测的翻译问题程度。 （越低越好，因为论文将其作为错误型指标报告，较低数值表示预测到的翻译问题更少。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 显式片段推理模型 $(F)$，使用3个检索示例，即 $k=3$ 且开启思考

<div class="result-value" markdown="1">

$(F)$ 得到BLEU 46.7、COMET 86.7和MetricX 1.99；对应直接翻译基线 $(B)$ 在相同 $k=3$ 下为46.3、86.5和2.07。因此片段推理分别改善0.4 BLEU、0.2 COMET，并将MetricX降低0.08。

</div>

这是最直接支持论文主张的汇总结果：在输入模型规模、微调框架和示例数量相近时，先抽取可复用双语片段再翻译，比直接输出译文更好，而且三个指标方向一致。表注称显著优于 $(B)$ 的结果以粗体标出，但当前纯文本没有保留粗体位置，因此不能据此确认这三个具体差异是否都达到 $p<1\%$；小幅平均增益也不意味着每个语言或领域都获益。

<div class="result-source" markdown="1">

来源：表1，模型 $(F)$、think为✓的完整数据行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

(F) ✓ 38.5 45.7 46.4 46.7 85.6 86.3 86.7 86.7 2.16 2.03 1.98 1.99

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 片段推理模型 $(F)$ 在无上下文示例条件下，即 $k=0$ 且开启思考

<div class="result-value" markdown="1">

$(F)$ 在 $k=0$ 时取得BLEU 38.5、COMET 85.6和MetricX 2.16；直接翻译基线 $(B)$ 为38.3、85.3和2.27，分别改善0.2、0.3和0.11。

</div>

该结果说明片段式训练的影响并不完全依赖测试时检索到示例：即使没有示例，开启该模型学到的思考过程仍略优于直接翻译。合理解释是银标轨迹训练改变了学生模型组织翻译的方式，但由于 $k=0$ 时没有可抽取的上下文片段，实验不能证明此处收益来自真实的示例复用，也可能来自额外监督或训练正则化。

<div class="result-source" markdown="1">

来源：表1，模型 $(F)$、think为✓的完整数据行；本项读取其中 $k=0$ 列

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

(F) ✓ 38.5 45.7 46.4 46.7 85.6 86.3 86.7 86.7 2.16 2.03 1.98 1.99

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 未微调模型 $(I)$ 与微调直接翻译基线 $(B)$ 的上下文学习表现

<div class="result-value" markdown="1">

在 $k=3$ 时，$(I)$ 的BLEU、COMET和MetricX分别为36.0、82.1和2.10，而 $(B)$ 分别为46.3、86.5和2.07；微调后BLEU提高10.3、COMET提高4.4、MetricX降低0.03。

</div>

这说明任务微调本身是主要性能来源之一，不能把所有优势归因于片段推理。尤其是未微调模型在 $k=0$ 时MetricX高达7.43，而加入一个示例后降至2.15，表明通用模型对上下文条件非常敏感。由于 $(I)$ 只能关闭推理，且作者指出其原始思考轨迹远长于微调模型，因此该比较衡量的是“通用指令模型与任务微调模型”的整体差异，不是公平的推理机制对照。

<div class="result-source" markdown="1">

来源：表1，模型 $(I)$、think为✗的完整数据行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

(I) ✗ 28.6 33.0 35.6 36.0 82.3 79.9 81.9 82.1 7.43 2.15 2.12 2.10

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

- 未微调的Qwen3-8B Instruct模型 $(I)$：用于判断通用指令模型直接进行上下文机器翻译的能力；由于其原始推理会消耗数千个token，实验仅关闭推理。
- 直接翻译基线 $(B)$：在相同Qwen3-8B学生模型和相同潜在示例条件下微调，但只输出最终译文，不学习任何推理轨迹；这是隔离“显式中间推理是否有用”的核心对照。
- 草稿模型 $(D)$：先在思考区生成教师提供的银标草稿，再输出参考译文；它检验一般性的“先草拟、后作答”是否足以解释收益。
- 片段加草稿模型 $(F+D)$：同时学习源端—目标端片段和完整草稿，再输出参考译文；它与仅片段模型 $(F)$ 的比较用于判断完整草稿能否在片段推理之上继续提供信息。

**实验想回答的问题**

- 在覆盖多语言、多领域的机器翻译测试中，让微调后的学生模型显式生成“示例片段”推理轨迹，是否比直接翻译、仅生成草稿或同时生成片段与草稿取得更好的翻译质量？
- 性能变化究竟来自显式片段推理，还是仅来自增加上下文示例数量；换言之，推理开关、示例数 $k$ 以及推理轨迹类型分别起什么作用？

**实验实现**

教师为Qwen3-32B，关闭其思考模式并用详细提示生成银标平行片段和草稿；学生为Qwen3-8B，用简短提示分别训练 $(B)$、$(D)$、$(F)$ 和 $(F+D)$。各模型在训练时等量观察 $k\in\{0,1,2,3\}$ 的示例条件，且20%的训练样本使用空推理轨迹，因此同一微调模型能够在测试时切换显式思考与不思考。所有微调均运行2个epoch。示例从同领域平行句池中以BM25和Levenshtein距离进行模糊匹配检索。表1报告16个测试组合的平均分；相对 $(B)$ 的显著性在COMET和MetricX上采用配对t检验，在BLEU上采用SacreBLEU的1000次bootstrap，阈值为 $p<1\%$。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 片段模型 $(F)$ 的推理开关：同一模型在 $k=3$ 下关闭与开启思考 | 关闭思考时为45.9 BLEU、86.4 COMET和2.09 MetricX；开启后为46.7、86.7和1.99，即BLEU提高0.8、COMET提高0.3、MetricX降低0.10。 | 因为训练模型保持不变、只改变测试时是否生成片段轨迹，这一对照较好地隔离了显式执行片段推理的作用。改善表明收益并非只来自含银标片段的微调数据，推理时实际生成中间片段也有贡献；不过它仍同时改变了生成长度和计算量，不能排除更多测试时计算带来的部分影响。 | 表1，模型 $(F)$、think为✗的完整数据行；与同表 $(F)$、think为✓的数据行比较<br><span class="experiment-evidence">(F) ✗ 37.4 44.8 45.5 45.9 85.1 86.2 86.3 86.4 2.33 2.13 2.11 2.09</span> |
| 推理轨迹结构：仅草稿 $(D)$ 与仅片段 $(F)$，均在 $k=2$ 下开启思考 | $(D)$ 得到45.0 BLEU、85.6 COMET和2.43 MetricX，而 $(F)$ 得到46.4、86.7和1.98；片段方案提高1.4 BLEU和1.1 COMET，并将MetricX降低0.45。 | 该比较检验的不是“有无推理”，而是中间轨迹应采用完整候选译文还是可追溯到示例的小型双语片段。结果显示，先生成一个完整草稿可能把早期错误带入最终译文，而片段只提供局部词语和短语约束，更易被最终解码器选择性采用。不过两种模型接受的银标监督内容不同，所以差异也可能部分来自教师生成数据的质量。 | 表1，模型 $(D)$、think为✓的完整数据行；与同表 $(F)$、think为✓的数据行比较<br><span class="experiment-evidence">(D) ✓ 36.8 44.1 45.0 46.0 84.9 85.0 85.6 85.6 2.34 2.66 2.43 2.11</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出基于检索样例片段的显式中间推理框架，以提升 LLM 机器翻译表现。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`dee334c43231ca12be3a50f673cf95903392e6359effce219525466cf0d216e1`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
