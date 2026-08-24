---
title: "[论文解读] KREL: Automatic Medical Coding via Knowledge-Guided Reasoning over Clinical Evidence with LLMs"
description: "[arXiv 2608.20887][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.20887"
announcement_date: "2026-08-24"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-24T02:09:11.234553+00:00"
source_sha256: "6fe26bcf99ae86f8e4c7cc89578f6a75993cf98c539d72daf6910947b4faa992"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "自动医疗编码"
  - "国际疾病分类"
  - "大语言模型"
  - "知识引导推理"
  - "知识图谱检索增强生成"
  - "临床证据"
  - "代码核验"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.20887</p>

# KREL: Automatic Medical Coding via Knowledge-Guided Reasoning over Clinical Evidence with LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Xubin Chen, Yipeng Zhou, Wen Sun, Chengkai Huang, Xiaoming Fu, Quan Z. Sheng</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: The University of New South Wales, Institute of Computer Science, University of Göttingen[0.5em]；Affiliation: The University of New South Wales；Institute of Computer Science, University of Göttingen[0.5em]；School of Computing；Macquarie University；Beijing Intelligent Decision Medical Technology Co. Ltd</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.20887v1) · [PDF 下载](https://arxiv.org/pdf/2608.20887v1) · **关键词** 自动医疗编码, 国际疾病分类, 大语言模型, 知识引导推理, 知识图谱检索增强生成, 临床证据, 代码核验<br>


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

自动医疗编码（Automatic Medical Coding, AMC）旨在从临床病历中识别诊断相关信息，并将其映射为标准化的国际疾病分类（ICD）代码。该任务服务于医疗报销、公共卫生统计、质量报告和临床研究；传统方法通常依赖人工编码或将任务建模为预定义代码集合上的极端多标签分类，而近期方法开始使用大语言模型（LLM）进行代码生成和多步推理。本文关注的核心设定是：如何利用 LLM 的临床文本理解能力，同时引入 ICD 的层级结构、代码定义和编码规则，使系统能够在完整且规模巨大的代码空间中进行可验证的编码。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**极端多标签分类**

极端多标签分类是指一个输入可能对应多个标签，且标签总数非常大。在 AMC 中，模型需要从大量 ICD 代码中选择与一份临床病历相关的一个或多个代码，而不是只在少数互斥类别中进行选择。

</div>
<div class="concept-item" markdown="1">

**ICD 代码与层级分类体系**

ICD 是用于统一描述疾病和健康相关状况的标准化分类体系，代码之间通常具有章节、类别和细分类别等层级关系。代码不仅有名称或定义，还受到适用条件、排除条件和其他编码规则约束，因此语义相似并不一定意味着编码正确。

</div>
<div class="concept-item" markdown="1">

**检索增强生成与知识图谱**

检索增强生成（RAG）先从外部知识中检索与输入相关的证据，再让语言模型依据这些证据生成结果。知识图谱以节点和关系表示实体及其结构联系；在本文中，ICD 知识图谱用于表达代码层级、定义以及编码规则，从而支持候选代码检索和后续核验。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一份临床病历 $x$，系统需要输出与其中诊断和临床证据相符的 ICD 代码集合 $Y$。输入病历通常较长、叙述不规则，并可能同时包含既往史、检查结果、治疗过程和多个诊断；输出空间原则上覆盖完整 ICD-10 体系，而不应被限制在训练数据中频繁出现的少数代码。任务还隐含两个重要假设：代码选择必须由病历中的临床证据支持，并且必须满足 ICD 编码指南规定的约束。与直接生成代码不同，本文把 AMC 处理为“从病历提取证据、检索候选代码、依据定义和规则进行核验并作出最终选择”的过程。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入的临床病历或临床文本。

</div>
<div class="notation-item" markdown="1">

**$Y$**

与病历对应的真实或预测 ICD 代码集合。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{C}$**

完整的 ICD 代码空间或代码候选集合；本文强调其可以扩展到完整 ICD-10 标签空间。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{G}_{\mathrm{ICD}}$**

ICD 知识图谱，包含代码、定义、层级关系及编码规则等结构化知识。

</div>

</div>

**直接相关的工作**

- **基于 PLM 的极端多标签分类方法**: 这类方法使用神经编码器或预训练语言模型将临床病历直接映射到预定义代码集合，在数据集已观察到的有限标签空间中表现较强，但难以扩展到超过 70K 个代码的完整且持续变化的 ICD 分类体系，也容易忽略代码规则。KREL 不再直接在固定标签集合上分类，而是通过知识引导的候选检索和代码核验处理完整代码空间。
- **Code Like Humans 与 MedDCR 等基于 LLM 的工作流方法**: 这些方法将医疗编码拆分为多个步骤，并使用 ICD 资源或编码流程来提升可靠性，代表了从直接提示转向多步推理的重要进展。但根据本文给出的相关工作分析，它们尚未在一个统一框架中充分结合完整代码空间的候选检索、临床证据 grounding，以及受编码指南约束的最终核验；KREL 针对这一缺口设计了 Query Extractor、Candidate Selector 和 Code Verifier。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

自动医疗编码（AMC）需要将临床记录映射为标准化的国际疾病分类（ICD）代码，直接影响医疗报销、质量报告和临床研究。人工编码依赖专业人员按照复杂规则逐条判断，过程耗时且容易出错；因此，研究需要一种能够处理长篇临床叙述、覆盖大规模代码体系并遵守编码规范的自动化方法。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于预训练语言模型的极端多标签分类**：模型将临床记录编码为固定标签集合中的一个或多个代码，通常由神经编码器或预训练语言模型直接完成文本到代码的映射。这类方法在基准数据集上表现较强，但主要依赖预先定义的候选标签集合。
- **基于大语言模型的生成或多步推理**：模型通过提示、直接生成代码或执行多步推理来模拟人工编码流程，部分方法还会调用外部工具或编码指南。相比固定分类器，这类方法具有更灵活的文本理解和推理能力，但并不意味着模型已经可靠掌握完整的医学编码知识。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有预训练语言模型分类方法通常受限于规模较小的预定义标签集，难以扩展到包含超过$70\text{K}$个代码的完整且持续变化的ICD体系；而大语言模型在大标签空间中容易遗漏罕见或低频代码。
- 大语言模型通常并未针对AMC训练，也没有内生地编码复杂的ICD规则。面对长而非结构化的临床记录时，它们可能无法准确将临床概念对应到代码，并可能生成违反编码约束或标准的结果。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未充分解决“如何将大语言模型的临床文本理解与完整ICD知识、代码定义及编码规则紧密结合”这一问题。具体而言，仍缺少一种能够先从长记录中提取代码相关证据，再从完整代码空间检索和筛选候选项，最后依据结构化指南进行核验的方法，从而同时提升覆盖范围、推理可靠性与规则遵循性。

</div>
<div markdown="1"><span>核心问题</span>

能否构建一个由外部结构化ICD知识引导的大语言模型推理流程，使模型不再直接从临床记录自由生成代码，而是围绕临床证据完成候选代码检索、候选细化和最终核验，并因此在完整ICD代码空间中实现更准确、更符合规范的自动医疗编码？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把编码任务拆成证据定位、候选检索和结果核验三个相互衔接的阶段：先用大语言模型将冗长记录压缩为结构化查询，再利用由编码指南构建的知识图谱检索候选代码及其定义和规则，最后让模型结合原始记录与这些外部证据作出判断。直观上，外部知识为模型提供了可检查的候选范围和规则依据，既减少凭语言模型记忆猜测代码的机会，也使最终决策更接近人工编码流程。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

KREL将自动医疗编码从直接的极端多标签分类改写为“证据抽取—层级检索—规则增强—证据验证”的推理流程。输入是一份临床记录$x$，输出是预测的ICD代码集合$\hat{\mathcal{Y}}$；系统不让LLM在超过7万的代码空间中自由生成，而是先用临床证据缩小候选范围，再用ICD层级、代码描述和官方编码规则约束最终判断。直观地说，KREL先把病历中的可编码疾病和状态整理成问题，再像在目录树中查找答案，最后让LLM依据原文证据和规则逐项核对，减少幻觉及不合规编码。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 临床查询与证据抽取

系统首先对病历进行章节划分，再调用LLM识别与编码相关的诊断、病情和状态，并将自由文本改写为简洁的ICD导向查询。对每个查询保留其在原病历中的证据片段，形成$\mathcal{Q}(x)=\{(q_i,E_i)\}_{i=1}^{n}$。

<div class="method-step__io" markdown="1">

**输入**：临床记录$x$，其中可能包含多个章节、疾病描述、症状、临床状态和其他非编码信息。<br>
**输出**：查询—证据对集合$\mathcal{Q}(x)$，其中$q_i$是规范化后的临床查询，$E_i$是支持该查询的原文证据跨度。

</div>

**直观理解**：这一步把“病历里写了什么”整理成若干个可检索的问题，并同时保留答案在原文中的位置。例如，将“CKD stage 3b”改写为“Chronic kidney disease stage 3b”，避免仅凭缩写或模糊表述检索。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 基于ICD层级的候选召回与重排序

系统先计算查询嵌入与代码嵌入的相关性$r_{emb}(q_i,c)$，再用层级感知束搜索沿ICD树逐层向更具体的子代码扩展，得到候选集$\mathcal{R}_i$。随后，跨编码器LLM根据查询和代码描述重新评分并截断候选，形成受验证预算$K_V$约束的列表$\mathcal{L}_i$。

<div class="method-step__io" markdown="1">

**输入**：每个查询$q_i$，以及包含代码描述、包含术语和层级关系的ICD知识图谱$\mathcal{G}_{\mathrm{ICD}}$。<br>
**输出**：每个查询对应的预算化候选代码列表$\mathcal{L}_i$。

</div>

**直观理解**：系统不是把所有代码逐一比较，而是先在ICD目录树中保留若干有希望的分支，再用更精细的LLM判断代码名称、症状和包含术语是否匹配。这样既覆盖可能的细粒度代码，也控制后续验证的计算成本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 编码规则与组合代码增强

对候选代码，系统检索$codeFirst$、$useAdditionalCode$和$codeAlso$关系，将相关关系转写为供验证器阅读的规则提示$\mathcal{H}_i$。同时将所有查询的候选合并为$\mathcal{L}_x=\bigcup_{i=1}^{n_x}\mathcal{L}_i$；若某组合代码所需的全部代码均在该集合中，则建立组合规则集合$\Omega_x$。

<div class="method-step__io" markdown="1">

**输入**：候选列表$\{\mathcal{L}_i\}_{i=1}^{n}$，以及知识图谱中的层级边、成对规则边$\mathcal{E}_R$和多代码组合关系$\mathcal{E}_M$。<br>
**输出**：每个查询的规则提示$\mathcal{H}_i$，以及病历级组合规则集合$\Omega_x$。

</div>

**直观理解**：有些编码不能只看单个疾病名称决定，例如一个代码可能要求先编码另一疾病，或多个组成代码齐全后才可以使用组合代码。KREL把这些“编码说明书”提前整理出来，交给最后的判断环节。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 基于证据的最终代码验证

LLM验证器对每个查询的候选代码同时检查完整病历、局部证据、代码描述及跨查询规则依赖，并将代码评为$supported$、$possible$或$not\ supported$。随后单独核验$\Omega_x$中的组合规则，最后保留被评为$supported$或$possible$的代码作为$\hat{\mathcal{Y}}$。

<div class="method-step__io" markdown="1">

**输入**：完整病历$x$、查询与证据$(q_i,E_i)$、候选列表$\mathcal{L}_i$、规则提示$\mathcal{H}_i$和组合规则$\Omega_x$。<br>
**输出**：病历的最终预测代码集合$\hat{\mathcal{Y}}\subseteq\mathcal{C}$。

</div>

**直观理解**：这一步类似人工编码员的复核：局部证据帮助定位事实，完整病历防止断章取义，官方规则防止代码之间互相矛盾。允许“possible”代码保留，说明系统的最终输出并非只依赖单一最可能标签。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 查询—代码嵌入相关性

$$
r_{emb}(q_i,c)=\mathbf{z}_{q_i}^{\top}\mathbf{z}_c
$$

**符号说明**

- $q_i$：第$i$个临床查询。
- $c$：一个ICD代码。
- $\mathbf{z}_{q_i}$：由嵌入LLM生成的查询$q_i$向量。
- $\mathbf{z}_c$：由同一嵌入LLM生成的代码$c$向量。
- $r_{emb}(q_i,c)$：查询与代码的嵌入相关性分数，采用向量内积计算。

<div class="equation-explanation" markdown="1">

**直观理解**：该式用向量内积衡量查询和代码语义上有多接近，分数越高，代码越适合作为层级搜索的起点或候选。它提供的是快速召回信号，不是最终编码决定，因此后面还需要重排序和证据验证。<br>
**原文位置**：第3.4.2节“Hierarchy-aware Candidate Recall”

</div>

</div>

<div class="equation-block" markdown="1">

#### 层级感知束搜索的路径分数

$$
S(c)=\lambda S(c^{\prime})+(1-\lambda)r_{emb}(q_i,c)
$$

**符号说明**

- $S(c)$：当前子代码$c$的路径累计分数。
- $c^{\prime}$：代码$c$在ICD层级中的父代码。
- $S(c^{\prime})$：父代码的累计路径分数。
- $r_{emb}(q_i,c)$：查询$q_i$与当前代码$c$的局部嵌入相关性。
- $\lambda$：父路径信息与当前局部相关性的权衡系数，论文实现中设为$0.5$。

<div class="equation-explanation" markdown="1">

**直观理解**：该式同时考虑“上级分类路径是否合理”和“当前代码本身是否匹配”。因此，即使某个中间父节点的文本相似度略低，只要更具体的叶节点与查询匹配，也不必过早丢弃整条路径；这正是HBS相较于提前剪枝的贪心搜索所要保留的信息。<br>
**原文位置**：第3.4.2节“Hierarchy-aware Candidate Recall”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告KREL的专门参数训练目标、损失函数或端到端梯度优化过程。方法描述的是由嵌入LLM、重排序LLM和验证LLM按提示执行的推理框架；因此，在现有材料中应将其理解为提示驱动的模块化推理，而不是已明确给出训练损失的联合训练模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 查询提取器（Query Extractor）**

LLM接收章节化临床记录，抽取可编码的疾病、状况、症状和临床状态，并输出查询—证据对$\{(q_i,E_i)\}$. 该模块将自由文本表达转换为更接近ICD描述的检索语言，同时保留证据跨度以支持后续验证。

> 直观理解：临床记录的说法通常不等于标准代码名称；该模块先把缩写、叙述和上下文整理成标准化问题，并告诉系统依据来自病历的哪一段。

**2. 知识引导候选选择器（Candidate Selector）**

选择器使用离线构建的$\mathcal{G}_{\mathrm{ICD}}=(\mathcal{V}_C,\mathcal{E}_H,\mathcal{E}_R,\mathcal{E}_M)$。其中$\mathcal{E}_H$用于层级感知召回，代码文本属性用于重排序，$\mathcal{E}_R$和$\mathcal{E}_M$仅在候选确定后转化为规则提示和组合检查，而不直接扩展普通候选列表。

> 直观理解：它把ICD目录和编码规则分工使用：目录负责找到可能的代码，代码描述负责排除相似但错误的兄弟代码，规则负责提醒代码之间的依赖关系。

**3. 证据验证器（Code Verifier）**

验证器对每份病历调用一次，综合完整记录、局部证据、查询、候选代码、规则提示和组合规则进行多标签决策。它对单查询可选择多个代码，也可不选择代码，并对组合代码执行额外核验。

> 直观理解：最终决定不是“检索到就输出”，而是逐项回答：病历是否真的支持该代码、证据是否足够、相关代码是否满足官方组合或先后编码要求。

**训练与推理**

知识图谱在离线阶段由ICD-10-CM代码元数据、官方层级、代码描述、包含术语及编码规则构建，包含代码节点、层级关系、成对规则关系和多代码组合关系。推理时，系统先对输入病历章节化并抽取查询—证据对；随后用嵌入相关性和层级感知束搜索召回候选，用跨编码器LLM重排序并按病历级预算截断；再依据$codeFirst$、$useAdditionalCode$、$codeAlso$及组合关系生成规则上下文，最后由验证LLM检查候选与完整病历、局部证据和规则的一致性，保留$supported$或$possible$代码。原文未明确报告这些LLM是否经过针对AMC任务的进一步微调、各模块是否联合训练，以及推理阶段是否使用随机采样。

**复现信息**

研究主要针对ICD-10-CM；原文说明迁移到其他ICD版本需要重建相应代码层级和指南资源。知识图谱记为$\mathcal{G}_{\mathrm{ICD}}=(\mathcal{V}_C,\mathcal{E}_H,\mathcal{E}_R,\mathcal{E}_M)$：代码节点保存代码字符串、官方描述、包含术语和版本信息；层级边按子代码指向父代码；成对规则类型为$codeFirst$、$useAdditionalCode$和$codeAlso$；组合关系保存所需代码集合$\mathrm{Req}(m)$及目标组合代码$\mathrm{Tar}(m)$。HBS使用初始代码数$K_c$、束大小$B$、每个父节点最多扩展子节点数$M$、最大深度$D$和最终叶节点数$K_f$控制搜索，论文实现设$\lambda=0.5$；重排序后的候选再受病历级验证预算$K_V$限制。除$\lambda$外，所给材料未明确报告$K_c$、$B$、$M$、$D$、$K_f$、$K_a$和$K_V$的具体取值。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MDACE：人工标注的医疗编码数据集，包含临床记录、$ICD$代码分配及代码相关标注信息；实验使用官方数据划分和标签清单，并同时用于基准标签空间和完整标签空间评估。其作用是检验整体编码性能、组件消融和证据对齐。
- ACI-Bench：带有句子级文本片段—$ICD$代码链接的临床记录数据集；使用作者提供的官方划分和标签清单，在基准标签空间中评估性能。句子级链接还支持基于证据的分析。
- MIMIC-IV-Subset：来自大规模去标识化住院电子病历数据库$MIMIC$-IV的随机抽样子集，包含出院摘要和带$ICD$编码的诊断；在完整的$ICD$-$10$-$CM$标签空间中检验方法对大标签空间的适应性。原文未明确报告该子集的具体样本规模、划分方式和随机种子。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Micro-averaged Precision**

在所有临床记录及其代码预测上汇总计算，表示预测代码中有多少是正确的；$TP$为真阳性，$FP$为假阳性，公式为$\mathrm{Precision}=\frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FP}}$。 （越高越好，因为较高值表示错误添加的、不受临床证据支持的代码更少。）

</div>
<div class="metric-item" markdown="1">

**Micro-averaged Recall**

表示所有真实代码中有多少被找回；$FN$为假阴性，公式为$\mathrm{Recall}=\frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FN}}$。 （越高越好，因为较高值表示漏掉的可报告诊断更少。）

</div>
<div class="metric-item" markdown="1">

**F1-score**

精确率和召回率的调和平均，公式为$\mathrm{F1}=2\cdot\frac{\mathrm{Precision}\cdot\mathrm{Recall}}{\mathrm{Precision}+\mathrm{Recall}}$；它衡量少报代码与错报代码之间的综合平衡。 （越高越好；仅提高召回率但大量增加错误代码，或仅保持高精确率而漏掉许多代码，都不会带来同等程度的提升。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 基准标签空间：MDACE与ACI-Bench

<div class="result-value" markdown="1">

KREL在两个数据集上均取得最高$F1$：MDACE为$0.49\pm0.007$，ACI-Bench为$0.70\pm0.01$。在MDACE上，其相对于PLM基线的主要优势来自召回率；在ACI-Bench上，精确率和召回率均有更明显提升。

</div>

在代码清单已经被限制为基准提供的标签时，KREL不仅能找回更多真实代码，也能在ACI-Bench上更有效地利用句子级临床证据。该结果证明了基准条件下的竞争力，但不能单独说明方法已经解决完整$ICD$标签空间中的检索难题。

<div class="result-source" markdown="1">

来源：第5.1节Main Results；表1(a)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Panel (a) shows that KREL remains competitive in the benchmark setting. It achieves the best F1 on both datasets, reaching 0.49 on MDACE and 0.70 on ACI-BENCH.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 完整标签空间：MDACE与MIMIC-IV-Subset

<div class="result-value" markdown="1">

在完整的$ICD$-$10$-$CM$标签空间中，KREL在MDACE上的$F1$为$0.51\pm0.003$，最佳基线为$0.32$；在MIMIC-IV-Subset上，KREL的$F1$为$0.39\pm0.002$，最佳基线为$0.33$。MDACE上的召回率由最佳基线的$0.26$提高到$0.53$。

</div>

这是最直接检验研究目标的结果：当模型不能只在一个小型预定义清单中挑选代码，而要面对完整代码空间时，KREL仍能保持领先，尤其显著减少漏码。结果支持结构化编码知识与检索—验证流程的有效性，但两个数据集的差距和子集设置仍不足以证明对所有医院或编码体系都具有普适性。

<div class="result-source" markdown="1">

来源：第5.1节Main Results；表1(b)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On MDACE, KREL improves F1 from the best baseline score of 0.32 to 0.51, with recall increasing from 0.26 to 0.53. On MIMIC-IV-Subset, KREL also obtains the best F1, improving from 0.33 to 0.39.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 完整标签空间中的候选检索策略：MDACE

<div class="result-value" markdown="1">

HBS的候选检索召回率为$0.70$，高于平面稠密检索的$0.67$；贪心层次搜索的召回率降至$0.46$。HBS在相近候选预算下保留更多可能包含正确代码的层次分支。

</div>

平面检索忽略代码层次结构，贪心搜索则可能因早期选错父节点而丢弃整个正确子树。HBS通过束搜索同时保留多个高分分支，因此更适合先扩大覆盖范围；但候选召回率只是检索阶段指标，不能代替最终验证后的编码精度。

<div class="result-source" markdown="1">

来源：第5.3节Retrieval Strategy Analysis；图3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

HBS obtains the highest retrieval recall, improving over flat dense retrieval from 0.67 to 0.70 with a comparable candidate budget. Greedy hierarchical search performs much worse, dropping to 0.46 recall, which suggests that following only the locally best branch can prematurely discard relevant ICD subtrees.

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

- PLM-ICD：代表性的预训练语言模型极端多标签分类方法，在预定义代码空间中直接预测代码；用于比较传统监督分类范式。
- PLM-CA：另一种PLM分类基线，通过标签级设计增强临床记录与代码的对应关系；用于检验KREL是否超越已有的标签感知分类设计。
- CoT与CoT-SC：分别代表直接提示下的链式思考和链式思考自一致性方法，将编码视为生成或通用推理任务；用于比较不使用专门编码工作流的LLM推理。
- CLH与MedDCR：代表多步LLM工作流，结合外部工具或编码资源模拟人工编码流程；用于比较与KREL最接近的代理式或知识辅助方法。

**实验想回答的问题**

- 在基准标签空间与完整的超过$70K$个标签的$ICD$代码空间中，KREL能否比代表性的PLM分类方法、直接提示方法和多步LLM工作流取得更好的代码预测效果？
- KREL中的证据驱动查询、层次化候选检索、重排序、编码规则注入和验证器分别是否改善候选覆盖率、预测精确性及证据可靠性？

**实验实现**

KREL以GPT-4o同时实现查询提取器、候选选择器和验证器；知识图谱由ICD-10-CM Tabular List及2022版Official Coding Guidelines构建。候选选择阶段使用Qwen3-Embedding-8B进行嵌入、Qwen3-Reranker-8B进行重排序。层次感知束搜索（HBS）使用$K_c=200$、$B=200$、$M=8$、$D=6$和$K_f=30$，跨查询去重后每条记录最多保留$K_V=50$个代码供最终验证。流程先从临床记录提取与证据对应的查询，再在$ICD$层次结构中检索候选代码，随后重排序、注入编码规则并由验证器筛除缺乏证据支持的代码，最后转换为与既有工作一致的就诊级代码集合。基准标签空间实验在MDACE和ACI-Bench进行；完整标签空间实验在MDACE和MIMIC-IV-Subset进行。所有方法主要报告微平均精确率、召回率和$F1$。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| MDACE完整标签空间：替换查询提取器为medSpaCy NER | 将证据驱动的LLM查询提取器替换为medSpaCy的医学实体识别模块后，召回率从$0.53$降至$0.19$，$F1$从$0.51$降至$0.24$，精确率为$0.35$。 | 该替换保留了医学术语抽取，却移除了基于临床证据的查询改写。性能大幅下降说明仅把实体词直接用于检索不足以形成覆盖良好的代码查询；查询提取器需要把记录中的证据组织成更适合代码检索的表达。它同时改变了实现模块而非只删除功能，因此更准确地说是功能替代实验。 | 第5.2节Ablation Study；表2<br><span class="experiment-evidence">This replacement significantly degrades performance, reducing recall from 0.53 to 0.19 and F1 from 0.51 to 0.24, indicating that evidence-grounded query construction is crucial for achieving adequate candidate coverage.</span> |
| MDACE完整标签空间：移除验证器 | 移除验证器后，精确率从$0.49$降至$0.10$，召回率从$0.53$升至$0.62$，$F1$从$0.51$降至$0.19$。 | 没有验证器时，系统保留了更多检索到的候选，因而找回更多真实代码，但也输出了大量没有充分证据支持的代码。该结果把验证器的作用定位为精确率控制和错误过滤，而不是候选覆盖；同时说明高召回率本身并不代表编码质量更高。 | 第5.2节Ablation Study；表2<br><span class="experiment-evidence">We further examine the effect of removing the verifier, which leads to a substantial drop in precision from 0.49 to 0.10, despite an increase in recall to 0.62.</span> |

**定性案例**

- 错误模式分析显示，KREL在MDACE完整标签空间中平均每条记录预测$9.67$个代码，较LLM prompting的$5.98$和CLH的$5.11$更积极；但其假阴性数为$255$，低于两者的$398$和$416$。在组合代码召回上，KREL为$0.615$，两个基线均为$0.077$；同时其同级代码假阳性率为$0.227$，接近CLH的$0.219$。这表明KREL增加的预测并非主要来自无控制的同级代码扩张，而是更善于恢复需要结合多个条件或查询块才能确定的代码。原文还报告，在$286$个真阳性代码对中，证据覆盖率为$100\%$，包含人工标注临床提及的mention-anchor覆盖率为$90.6\%$，平均语义余弦相似度为$0.746$；这些证据对齐指标仅在真阳性预测上计算，不能证明假阳性也具有可靠证据。
- limitations

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops knowledge-guided reasoning with LLMs for complex clinical coding decisions.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`6fe26bcf99ae86f8e4c7cc89578f6a75993cf98c539d72daf6910947b4faa992`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
