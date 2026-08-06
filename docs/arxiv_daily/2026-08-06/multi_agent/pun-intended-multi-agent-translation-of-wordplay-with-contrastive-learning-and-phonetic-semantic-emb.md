---
title: "[论文解读] Pun Intended: Multi-Agent Translation of Wordplay with Contrastive Learning and Phonetic-Semantic Embeddings"
description: "[arXiv 2608.04311][Multi-Agent] 本文研究如何通过显式的语音—语义约束与多智能体迭代反馈，使大语言模型在英译法双关语翻译中优先重建幽默、歧义和自然表达，而不是拘泥于原文词汇。"
arxiv_id: "2608.04311"
announcement_date: "2026-08-06"
primary_category: "multi_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T07:04:04.786701+00:00"
source_sha256: "018f31989e34a588db1f39f4806a4c328a1fe76799d4be1c43c027da18c32645"
tags:
  - "Multi-Agent"
  - "LLM 其他"
  - "LLM Reasoning"
  - "双关语翻译"
  - "英法机器翻译"
  - "计算幽默"
  - "功能等效"
  - "语音—语义嵌入"
  - "大语言模型"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">Multi-Agent · arXiv 2608.04311</p>

# Pun Intended: Multi-Agent Translation of Wordplay with Contrastive Learning and Phonetic-Semantic Embeddings

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Russell Taylor, Benjamin Herbert, Michael Sana</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Georgia Institute of Technology, Atlanta, GA 30332, USA</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04311v1) · [PDF 下载](https://arxiv.org/pdf/2608.04311v1) · **关键词** 双关语翻译, 英法机器翻译, 计算幽默, 功能等效, 语音—语义嵌入, 大语言模型<br>


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

本文研究如何通过显式的语音—语义约束与多智能体迭代反馈，使大语言模型在英译法双关语翻译中优先重建幽默、歧义和自然表达，而不是拘泥于原文词汇。

**不用术语来说**：双关语往往利用一个词的多重含义、相近发音或上下文反差制造幽默，但这些条件通常无法直接迁移到另一种语言：英语中恰好同音或多义的词，在法语中可能毫无对应关系。因此，即使系统理解了原笑话，逐词翻译也容易只留下字面意思而丢失笑点；它必须在法语中重新找到或创造一种既大致传达原意、又能触发类似幽默效果的说法。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将英法双关语翻译明确设定为追求功能对等的生成问题，即以目标语中的幽默效果、歧义和表达自然度为主要目标，而非要求原词及其语言形式与译文逐项对应。
- 作者比较了三种逐步增强的基于大语言模型的方案：判别器反馈生成、由语音—语义嵌入辅助的候选词引导推理，以及通过专业化角色反复评价和重写译文的多智能体框架，用以检验显式语言约束与迭代评价能否改善双关语翻译。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究英法跨语言双关语翻译，位于机器翻译、计算幽默与创造性文本生成的交叉领域。与常规翻译主要保持命题意义不同，双关语通常借助一词多义、同音或近音等语言现象，使同一表达同时激活两个不相容但可被语境支持的解释，由此产生意外感和幽默。由于词义关系、发音系统及文化联想具有语言特异性，英语双关往往没有形式和含义都对应的法语表达；系统因而不能只逐词复现原句，而要在理解原意后重新寻找或创造法语文字游戏。本文据此采用“功能等效”视角：译文可以改变具体词汇乃至造梗机制，但应尽可能保留源文本的语义内容、歧义结构、惊奇效果和目标语自然度。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**双关语与语义歧义**

双关语让一个词或表达在同一语境中关联两个解释，并利用二者之间的不协调制造幽默。翻译时不仅要识别表层句义，还要识别被暗示的第二层含义。

</div>
<div class="concept-item" markdown="1">

**语音—语义表示**

语音—语义表示把词的发音相似性和意义相似性共同编码，用于寻找既能近音成梗、又与上下文含义相关的候选词。本文背景所依赖的语音信息包括国际音标及其发音特征表示。

</div>
<div class="concept-item" markdown="1">

**功能等效**

功能等效关注译文是否产生与原文相近的交际和幽默效果，而不要求词汇或修辞形式逐项对应。对双关翻译而言，这通常意味着允许创造新的目标语双关，只要核心语义和幽默功能得到保留。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务场景是 CLEF JOKER 2025 Task 2 的英语到法语文字游戏翻译。输入是一段包含英语双关的源文本，系统需要理解其显性语义、隐含解释以及可能依赖的语音或词义关系；输出是一条自然的法语译文，并尽可能在法语中形成可理解的文字游戏。该设置隐含的关键假设是：源语双关通常不存在可直接替换的目标语对应项，因此允许改变具体词汇和造梗机制，通过目标语中的新歧义或近音关系实现功能等效。任务质量不能仅由词面重合判断，因为 BLEU 和 BERTScore 更偏向奖励与参考译文的词汇或语义相似性，未必能充分反映歧义、惊奇和幽默是否保留。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Low（2011）的双关翻译迭代搜索框架**: 该框架要求逐步扩展语义和语音替代项，直到找到合适的目标语文字游戏；它为本文的候选检索与生成式流程提供了翻译学依据。
- **Sharma、Dhawan 与 Pailla（2021）的语音词嵌入**: 该工作构造基于国际音标的语音嵌入，并在英语 JOKER 数据上验证其用途；本文在此基础上构建法语语音嵌入，并将其用于跨语言双关翻译中的引导式候选检索。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

跨语言双关翻译同时要求保留信息内容与文字游戏产生的幽默效果。双关依赖特定语言中的多义、同音或近音关系以及文化语境，而这些关系在目标语言中通常没有现成对应物；因此，译者或机器不仅要理解原文，还要在法语中创造新的文字游戏。这种创造任务需要兼顾语义忠实、语音关联、文化可理解性和表达自然度，长期以来即使对专业译者也很困难。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **大语言模型直接生成与判别器反馈**：生成模型先提出法语双关译文，再由一个根据法语正例和负例提示的判别器提供反馈，以促使模型调整候选结果。这类方法利用大语言模型从大规模语料中获得的语言与文化知识，但主要依赖提示和整体评价来寻找笑点。
- **计算双关生成中的语言特征建模与迭代改写**：既有双关生成研究尝试利用语义歧义、语音相似性、关键词或结构化推理产生文字游戏，也有方法通过评价后再生成来逐步修正文本。这些机制说明双关可以被拆分为若干可检查的语言条件，为跨语言翻译提供候选检索和反复优化的技术基础。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 常规机器翻译及偏向字面对应的生成方式主要学习规则性的语言和语义模式，而双关的关键恰恰是歧义与不协调带来的意外感；其后果是译文可能准确传达表层内容，却消除双重解释和幽默效果。
- 仅依靠通用模型生成或单一判别器的整体反馈，未必能明确协调语义忠实、发音相似与法语自然度等相互竞争的条件；当目标语中不存在原双关的直接对应词时，系统缺少系统化寻找替代词并针对不同缺陷反复修订的机制。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作尚未充分回答：在原双关无法直接移植到目标语言时，如何把大语言模型的开放式创造能力与可操作的语言约束结合起来，并在运行时持续评价候选译文，使系统能够主动重建功能上等效的新双关。尤其需要比较显式语音—语义候选引导与多角色迭代反馈，相对于较简单的判别器反馈究竟能提供什么增益。

</div>
<div markdown="1"><span>核心问题</span>

对于英译法双关语，显式加入语音—语义候选检索，或让承担不同评价职责的多个智能体反复审查和重写，能否比直接的判别器引导生成更有效地同时保留原文意义、文字游戏及目标语自然度？

</div>
<div markdown="1"><span>作者直觉</span>

双关译文通常不是从原句逐词推导出的唯一答案，而是在众多法语表达中寻找一个新的平衡点。语音—语义嵌入可以先把“意思相关”和“听起来相近”的词汇候选送入模型，缩小创造性搜索范围；多智能体机制则把笼统的“这个笑话好不好”拆成不同角度的检查，并让生成器依据具体问题继续改写。前者帮助模型想到更合适的材料，后者帮助模型筛除只有字面正确、只有音近或表达生硬的候选。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文设计了三条英法双关翻译路线。基线系统先规范化英文输入，再让生成模型直接创作兼顾语义与幽默的法语双关，并由对比式判别器检查候选是否仍含双关；引导式系统先显式解析英文双关词、双关类型及两重含义，再利用法语语音嵌入与语义嵌入检索可用词，最后按双关类型约束大语言模型生成；多智能体系统则不直接接受初稿，而是由四个专门评估器从等效性、质量、情感和真实性四方面评分并反馈，驱动生成模型反复修订，最终保留最高分候选。三条路线的共同输入是英文双关句，输出是力图保留原句语用功能和幽默效果的法语句子，而非逐词对应的直译。
从直观上看，基线方法相当于“先写笑话，再由裁判判断它是不是笑话”；引导式方法像译者先拆解笑点的两个含义，再从法语词库中寻找一边意思接近、另一边读音可联想的材料；多智能体方法则像一组编辑分别检查译文是否忠实、通顺、有情绪效果且像自然法语，然后要求作者根据编辑意见改稿。这里的核心设计选择是把双关翻译视为候选搜索与迭代筛选问题，并将“重建笑点”置于词面复现之上。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 输入规范化与源双关解析

系统先规范化标点、大小写、话题标签和命名实体。引导式路线随后用 Gemini 2.5 Pro 识别双关词，判断其为同形双关还是同音双关，并为两个预期含义分别生成同义词列表；基线路线不执行这套显式语义分解。

<div class="method-step__io" markdown="1">

**输入**：一条待翻译的英文双关句；引导式路线还使用作者人工整理的双关位置、双关类型、两重含义和上下文标注来评估解析质量。<br>
**输出**：规范化英文句子；对引导式路线，额外输出双关词、双关类型以及分别表示两重含义的英文同义词列表。

</div>

**直观理解**：这一步先回答“笑点落在哪个词、这个词同时让人想到什么”。如果不能拆清两重含义，后续检索到的法语词即使读音有趣，也可能与原句笑点无关。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 法语含义转换与语音—语义候选检索

系统用 o4-mini 翻译双关词和两组同义词，并以双语嵌入余弦相似度检查含义转换；随后将候选词的 $300$ 维语音嵌入与 $300$ 维语义嵌入联合用于检索。检索双向进行：先令第一重含义提供语义查询、第二重含义提供语音查询，再交换两者；每个方向保留至多两个同时满足两项余弦相似度大于 $0.75$ 的候选。

<div class="method-step__io" markdown="1">

**输入**：识别出的英文双关词、两组英文同义词及双关类型，以及由 Lexique、PanPhon 和 French FastText 构建的法语词表示。<br>
**输出**：法语双关词译法、两组法语同义表达，以及兼顾一重含义的语义接近性和另一重含义的语音接近性的法语候选词。

</div>

**直观理解**：普通词典只会找“意思像”的词，这里还要找“声音能勾起另一层意思”的词。双向搜索避免预先假定哪一层含义必须由词义表达、哪一层必须由谐音表达。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按双关机制生成法语候选

基线让 Mistral Medium 2505 或 o4-mini 直接生成保留原语义和幽默效果的法语双关。引导式路线分三种策略：若原同形双关词翻译后仍是覆盖两义的法语同形异义词，就围绕该词写句子；否则另选近似两义的法语同形异义词；若为同音双关，则生成分别对应两义且发音相近的一对法语词。

<div class="method-step__io" markdown="1">

**输入**：规范化原句；基线使用原句和示例提示，引导式路线还使用双关类型、法语同义词列表及语音—语义检索候选。<br>
**输出**：一条或多条法语双关候选句，以及候选所采用的同形或同音实现方式。

</div>

**直观理解**：系统不是机械翻译每个英文词，而是根据笑点机制重新搭建法语句子。显式分类的作用是避免用同一套提示处理所有双关，但论文也指出，同形与同音二分法无法覆盖多重双关等复杂情况。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选判别、迭代修订与最终选择

基线由 Gemini 2.5 Flash 判别候选是否含双关，被判为非双关时最多重新生成十轮。多智能体路线分别评价等效性、整体质量、情感保留和真实性，计算四项分数的平均值，将文字反馈交给生成模型修订；平均分达到 $2.0$ 或完成五轮后停止，并从历轮候选中保留得分最高者。

<div class="method-step__io" markdown="1">

**输入**：初始法语候选；基线还使用各 $25$ 个正例和负例组成的少样本判别提示，多智能体路线使用四类评价提示。<br>
**输出**：通过双关判别的基线译文，或经过多维反馈迭代后得分最高的多智能体译文。

</div>

**直观理解**：基线裁判只重点回答“这是不是双关”，因此可能接受与原文关系较弱但确实好笑的法语句子。多智能体方法增加了多个编辑视角，使修改同时考虑笑点、原意和法语自然度，而不是只追求某一个指标。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 音素二元组的 Jaccard 相似度

$$
S\bigl((P_{a1},P_{a2}),(P_{b1},P_{b2})\bigr)=\frac{\left|F(P_{a1},P_{a2})\cap F(P_{b1},P_{b2})\right|}{\left|F(P_{a1},P_{a2})\cup F(P_{b1},P_{b2})\right|}
$$

**符号说明**

- $S$：两个音素二元组之间的相似度。
- $(P_{a1},P_{a2})$：第一个发音片段中相邻的两个音素。
- $(P_{b1},P_{b2})$：第二个发音片段中相邻的两个音素。
- $F(P_{a1},P_{a2})$：第一个音素二元组对应的 PanPhon 发音器官特征集合。
- $F(P_{b1},P_{b2})$：第二个音素二元组对应的 PanPhon 发音器官特征集合。
- $|\cdot|$：集合中元素的数量；分子计算共有特征数，分母计算全部不同特征数。

<div class="equation-explanation" markdown="1">

**直观理解**：该式用“共有发音特征占全部发音特征的比例”衡量两个短发音片段有多相像。它把清浊、发音部位和发音方式等细粒度特征纳入比较，因此比要求音素完全相同更适合发现近音关系，并为语音嵌入训练提供相似度信号。<br>
**原文位置**：第 3.3.2 节，Phonetic-Semantic Retrieval

</div>

</div>

<div class="equation-block" markdown="1">

#### 语义与语音双阈值候选条件

$$
\cos(\vec{w}_{\mathrm{sem}},\vec{S})>0.75\quad\text{and}\quad\cos(\vec{w}_{\mathrm{phon}},\vec{P})>0.75
$$

**符号说明**

- $\vec{w}_{\mathrm{sem}}$：候选法语词的语义嵌入分量。
- $\vec{w}_{\mathrm{phon}}$：候选法语词的语音嵌入分量。
- $\vec{S}$：由其中一重目标含义构造的语义查询向量。
- $\vec{P}$：由另一重目标含义构造的语音查询向量。
- $\cos(\cdot,\cdot)$：余弦相似度，用向量夹角衡量候选与查询的接近程度。
- $0.75$：作者通过经验选择的两项相似度阈值。

<div class="equation-explanation" markdown="1">

**直观理解**：候选必须同时过两道门槛：词义上足够接近一层意思，读音上也足够接近另一层提示。这样能排除只有语义相关但没有声音笑点的词，也能排除听起来相似却与原句含义无关的词；作者进一步只保留排名最高的两个候选，以控制提示中的噪声。<br>
**原文位置**：第 3.3.2 节，Phonetic-Semantic Retrieval

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：该系统没有统一的端到端可微训练目标，也没有用官方英法双关对训练一个翻译模型；主要生成器、翻译器和评估器均以预训练大语言模型进行提示式推理。唯一明确涉及训练的部分是依据 Sharma 等人的方法训练 $300$ 维 BiLSTM 法语语音嵌入，其监督信号来自 PanPhon 特征二元组的相似关系，但原文节选未给出具体损失函数、负采样方法、优化器或训练轮数，因此不能还原为更具体的优化目标。对比式判别也采用少样本提示，而非在所构造的正负数据上微调；多智能体的平均分是停止和选择规则，不是反向传播的训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 对比式双关判别器**

作者为 JOKER 中每个法语双关生成一个不含双关的对应负例，形成平衡的正负数据；负例由 Gemini 2.5 Flash 生成，并反复生成直至独立提示确认不再含有文字游戏。推理时，判别器采用包含 $25$ 个正例和 $25$ 个负例的少样本提示，且与候选生成器使用不同模型，以降低同一模型偏好的潜在影响。

> 直观理解：仅告诉模型“请写双关”并不能保证结果真的有双重解释，因此需要正反例帮助裁判建立判断边界。它主要控制候选是否具备双关形式，并不充分保证译文忠实于英文原意。

**2. 法语语音—语义联合检索器**

系统把 Lexique 中的法语发音表示为国际音标序列，再转换为基于 PanPhon 发音器官特征的音素二元组；二元组之间的 Jaccard 相似度用于训练 $300$ 维 BiLSTM 语音嵌入。检索时，该语音表示与 $300$ 维 French FastText 语义表示配合使用，使候选可在语义子空间中贴近一重含义，同时在语音子空间中贴近另一重含义。

> 直观理解：双关候选通常不能只靠语义近邻找到，因为真正的桥梁可能是读音。把“意思像不像”和“声音像不像”分别表示，可以筛出更适合重建双重解释的法语词。

**3. 四角色多智能体评价器**

四个评价提示依据 MMTE 的等效性、质量、情感和真实性维度设计：等效性与质量采用 $0$ 至 $2$ 分，情感采用 $0$ 或 $1$ 分，真实性采用 $0$ 至 $4$ 分。系统直接平均四个量表不同的分数，并把各评估器的简短文字意见用于下一轮重写；论文没有报告量表归一化或学习得到的权重。

> 直观理解：不同评估器相当于分工明确的编辑：有人检查是否保留原意，有人检查整体表达，有人检查情绪效果，有人判断是否像自然法语。需要注意的是，直接平均不同取值范围的分数会让真实性维度具有更大的数值影响，这是根据方法定义得到的分析，不是作者明确验证过的结论。

**训练与推理**

准备阶段包含三类资源构建。第一，作者协作标注 CLEF JOKER 2023 数据中的双关词、类型、两重含义和上下文，并将标注与大语言模型预测比较后人工复核分歧；这些标注用于评估源双关识别。第二，作者以 JOKER 法语参考双关为正例，为每个正例生成一个已去除文字游戏的负例，建立平衡数据，供判别器少样本提示。第三，系统从 Lexique 取得法语发音，用 PanPhon 特征计算二元组相似度并训练语音嵌入，再与预训练 French FastText 语义表示共同支持检索。
推理时，基线系统规范化英文句子后直接生成法语双关，由独立判别器检查，失败则最多重生十轮。引导式系统依次执行双关解析、两重含义翻译、翻译后同形异义性检查、双向语音—语义检索和类型条件生成。多智能体系统从初始候选出发，由四个角色评分并给出反馈，生成器据此修订；平均分达到 $2.0$ 或完成五轮即停止，最终返回所有轮次中分数最高的候选。原文将三者作为三种端到端方案比较，但节选没有明确说明多智能体初稿究竟固定来自基线生成还是引导式生成，因此复现时不能擅自确定该连接方式。

**复现信息**

数据规模方面，CLEF JOKER 2025 Task 2 训练集含 $1{,}405$ 条英文双关及 $5{,}838$ 条法语译文，隐藏测试集含 $376$ 条英文双关；这些数据用于组件评估和官方端到端测试，而论文说明系统总体上接近无监督提示式方案。模型分工为：Gemini 2.5 Pro 识别双关，o4-mini 翻译双关词及同义词，Lajavaness/bilingual-embedding-large 计算英法语义相似度，Mistral Medium 2505 与 o4-mini 承担基线生成，Gemini 2.5 Flash 承担判别；作者未覆盖服务商默认生成参数。
公平解释结果时还需保留几项关键设定：判别器提示含 $25$ 个正例和 $25$ 个负例；基线最多迭代十次；检索在两个含义方向上交换语义与语音角色，仅保留余弦相似度均高于 $0.75$ 的前两个词；多智能体最多修订五轮，停止阈值为平均分 $2.0$。代码、完整提示和增强数据由作者公布于 https://github.com/dsgt-arc/joker-2025，但源文节选没有给出随机种子、提示采样是否固定、BiLSTM 训练超参数、模型调用版本冻结方式及多智能体初稿来源，这些缺失会影响严格复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 人工标注的训练集：用于独立评估双关位置识别、双关类型分类和两组预期含义的近义词翻译。原文未明确报告该训练集的样本规模、划分方式及标注者信息，因此相关组件分数只能视为训练数据上的诊断结果。
- 人工标注的判别器评估集：包含450个正、负样例，用于检验对比判别器能否区分成功的法语双关与字面或失败译文。原文未明确报告正负样例各自数量，也未说明该集合是否与训练数据完全隔离。
- CLEF JOKER 2025 Task 2官方测试集：端到端评测覆盖1,682条生成译文，并从中对42个例子进行专家人工评价；该集合用于比较Multi-Agent、Guided CoT和Baseline，并给出它们在51个官方提交系统中的排名。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**组件级分类与翻译指标**

双关识别采用准确率、精确率、召回率和$F_1$，分别衡量总体判断、预测为正时的可靠性、真实目标的覆盖率及二者平衡；近义词翻译采用英法双语嵌入的平均余弦相似度衡量语义接近程度，并报告方差和错误率。判别器则分别统计正、负样例分类准确率。 （准确率、精确率、召回率、$F_1$和平均余弦相似度越高越好；错误率和通常反映不稳定性的方差越低越好。）

</div>
<div class="metric-item" markdown="1">

**BLEU与BERTScore**

BLEU衡量生成译文与参考译文的表层词组重合，BERTScore利用上下文表示衡量两者的语义相似性。二者适合检查一般翻译接近度，但当一个双关存在多种合理创译时，可能低估与参考措辞不同但仍成功的译文。 （均为越高越好，因为更高值表示与参考译文具有更强的表层或语义一致性；但不能单独证明幽默、歧义或双关结构得到保留。）

</div>
<div class="metric-item" markdown="1">

**Pun Location与专家人工成功率**

官方Pun Location指标检查生成译文的双关是否出现在某个参考译文对应的位置；人工评价由一名具备双关翻译研究生训练的法语母语者完成，只要译文完全或部分保留源文含义并产生目标语言双关，就判为成功。前者是位置匹配代理指标，后者更直接评估创译是否成立。 （均为越高越好；更高Pun Location表示更常复现参考双关位置，更高人工成功率表示更多译文被专家判定为兼顾含义与法语双关。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 官方CLEF JOKER 2025 Task 2测试集上的Multi-Agent系统

<div class="result-value" markdown="1">

Multi-Agent取得BLEU 21.41、BERTScore 80.66、Pun Location 9.27%和人工成功率88.09%；前两项均列第41，而后两项均列第1。对应计数为1,682条译文中156条命中参考双关位置，42个人工评测例中37条成功。

</div>

作者结果表明，专门智能体反复评价和重生成，明显有利于双关位置与专家认可的创译质量，并且是三套内部系统中整体表现最强者。其BLEU和BERTScore排名仍较低，说明参考重合指标没有充分反映双关创译质量。该结果支持多智能体反馈有效，但没有随机化消融或显著性检验，因而不能单独证明提升只由“多智能体”机制造成。

<div class="result-source" markdown="1">

来源：第4.2节；表3对应行：Multi-Agent | 21.41 (41) | 80.66 (41) | 9.27% (1) | 88.09% (1)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The multi-agent system correctly localized the reference pun in 156 of the 1,682 evaluated translations, compared with 132 for the guided system and 60 for the baseline.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 官方CLEF JOKER 2025 Task 2测试集上的Guided CoT系统

<div class="result-value" markdown="1">

Guided CoT取得BLEU 16.52、BERTScore 78.42、Pun Location 7.85%和人工成功率85.71%；前两项均列第45，而后两项均列第2。对应计数为1,682条译文中132条命中参考双关位置，42个人工评测例中36条成功。

</div>

作者结果说明，即使不采用完整多智能体迭代，显式检索兼顾发音和语义的候选词，也能在双关专用指标和人工判断上远超直接反馈基线，并接近Multi-Agent。分析上，这支持“候选词空间需要语言学引导”的解释；但Guided CoT与Baseline可能同时存在提示过程和推理流程差异，因此不能把全部差距严格归因于语音—语义嵌入。

<div class="result-source" markdown="1">

来源：第4.2节；表3对应行：Guided CoT | 16.52 (45) | 78.42 (45) | 7.85% (2) | 85.71% (2)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under manual evaluation, the three systems produced successful translations for 37, 36, and 20 of the 42 evaluated examples [9].

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 官方CLEF JOKER 2025 Task 2测试集上的判别器反馈Baseline

<div class="result-value" markdown="1">

Baseline取得BLEU 14.94、BERTScore 78.30、Pun Location 3.57%和人工成功率47.62%，排名分别为第46、第46、第45和第25；其1,682条译文中有60条命中参考双关位置，42个人工评测例中20条成功。

</div>

这组结果给出了内部比较的下界：仅让判别器依据正负例反馈，虽可生成部分成功双关，但在双关位置和人工评价上显著落后于两种带更强结构化引导的系统。它也显示判别器自身分类准确并不等于生成器能找到高质量译文，因为可靠地识别成品与有效地搜索成品是不同问题。

<div class="result-source" markdown="1">

来源：表3，Baseline行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Baseline | 14.94 (46) | 78.30 (46) | 3.57% (45) | 47.62% (25)

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

- Baseline：使用大语言模型生成译文，并由基于法语正、负示例提示的对比判别器提供反馈。它是最关键的内部基线，因为与另外两套系统共享大语言模型生成范式，但不包含显式语音—语义检索引导或专门化多智能体迭代。
- Guided CoT：利用组合语音—语义嵌入检索法语词汇候选，再通过引导推理生成双关译文。它既是参赛系统，也是用于判断显式词汇约束是否优于直接判别器反馈的比较对象。
- Google Translate：仅用于近义词列表翻译组件的外部基线，用来判断通用机器翻译是否能胜任把双关两种含义映射为法语词汇集合的受约束翻译任务；它不是端到端双关生成基线。
- 多种通用大语言模型，包括Gemini 2.5 Pro、Claude Sonnet 4、Gemini 2.5 Flash、GPT-4.1、o3、o4-mini和Mistral Medium 2505：用于比较双关识别或近义词列表翻译能力，并为流水线选择组件模型，而非全部参与官方端到端系统排名。

**实验想回答的问题**

- 各中间组件是否足以支撑端到端系统：模型能否识别英语双关的位置与类型、把双关的两组预期含义翻译成法语近义词，并区分成功双关与直译或失败译文？
- 在官方英译法双关翻译任务中，显式利用语音—语义候选引导与多智能体迭代反馈，是否比直接使用对比判别器反馈的基线更能生成兼顾原意、法语双关和自然表达的译文？

**实验实现**

实验先在训练集上分别验证三项中间能力，再将组件整合进端到端系统，并在官方测试集上比较三种方案。近义词列表翻译阶段选择o4-mini，理由是其质量接近最强模型，同时成本和延迟更低。官方评测同时使用BLEU、BERTScore、Pun Location和人工评价，并报告在51个提交中的排名；其中自动评测覆盖1,682条译文，人工评测仅覆盖42例。原文节选未报告生成温度、提示词全文、迭代轮数、显著性检验、置信区间或重复运行结果。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Studies LLM-based pun translation with an iterative multi-agent evaluation and regeneration framework alongside phonetic-semantic guidance.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`018f31989e34a588db1f39f4806a4c328a1fe76799d4be1c43c027da18c32645`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
