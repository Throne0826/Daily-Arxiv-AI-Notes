---
title: "[论文解读] ANCHOR-RE: An Agentic Neuro-Symbolic Framework for Grounded Biomedical Relation Extraction"
description: "[arXiv 2608.03154][LLM Agent] 原文未明确报告。"
arxiv_id: "2608.03154"
announcement_date: "2026-08-05"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:42:17.600689+00:00"
source_sha256: "10f8089e986e7073bcf0142fad9318971d9fcfafb4b96a55b602706a33e9cc9c"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "LLM 其他"
  - "生物医学关系抽取"
  - "大语言模型"
  - "神经—符号人工智能"
  - "知识库 grounding"
  - "语义类型约束"
  - "推理时验证"
  - "SemRep"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.03154</p>

# ANCHOR-RE: An Agentic Neuro-Symbolic Framework for Grounded Biomedical Relation Extraction

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Shufan Ming, Yikun Han, Gibong Hong, Rui Zhang, Halil Kilicoglu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> aSchool of Information Sciences, University of Illinois Urbana-Champaign, 501 E Daniel；bDivision of Computational Health Sciences, Department of Surgery, University of</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03154v1) · [PDF 下载](https://arxiv.org/pdf/2608.03154v1) · **关键词** 生物医学关系抽取, 大语言模型, 神经—符号人工智能, 知识库 grounding, 语义类型约束, 推理时验证, SemRep<br>
**代码**: [https://github.com/COMBINI-Hub/Multi_Agent_Relation_Extraction](https://github.com/COMBINI-Hub/Multi_Agent_Relation_Extraction)

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

生物医学关系抽取（BioRE）旨在把论文中的非结构化叙述转换为实体之间的结构化关系，可服务于生物医学知识图谱构建、文献驱动发现和临床决策支持。该任务通常先识别药物、化学物质、蛋白质或疾病等实体，再判断给定实体对是否表达预定义关系；现实语料中多数候选实体对其实无关系，因此系统不仅要识别语言形式多样、可能跨越复杂语境的真关系，还必须抑制由实体共现引起的假阳性。规则系统（如 SemRep）利用词汇触发词和人工整理的语义类型约束，通常精度较高且预测依据可解释，但面对不同措辞和复杂篇章结构时召回受限；监督式 Transformer 能学习上下文表示，却依赖大规模任务标注和参数微调。生成式大语言模型可进行零样本或少样本推理，降低对标注数据的依赖，但容易把共现误判为关系并产生缺乏生物医学依据的预测。因此，本文关注一种无需更新模型参数的神经—符号方案：在大语言模型的上下文推理能力之外，引入知识库证据、实体语义类型兼容性和验证规则，以提高关系预测的可靠性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**生物医学关系抽取（BioRE）**

从生物医学文本中判断两个已识别实体之间是否存在某种预定义语义关系，例如药物相互作用或化学物质—蛋白质关系。其结果通常表示为“主体实体—关系类型—客体实体”的结构化三元组。

</div>
<div class="concept-item" markdown="1">

**神经—符号推理（Neuro-symbolic reasoning）**

将神经模型灵活的语言理解能力与知识库、 ontology（本体）、语义类型约束或规则等显式知识结合。直观地说，大语言模型负责提出和理解候选关系，符号知识负责限定哪些关系在生物医学上合理并检查预测。

</div>
<div class="concept-item" markdown="1">

**推理时方法（inference-only / training-free）**

在模型执行预测时通过提示、检索、约束或验证来改善输出，而不针对目标任务微调模型参数。该设置适合标注数据稀缺或需要快速迁移到新关系模式和新领域的场景。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是包含生物医学实体提及的文本、一个候选主体—客体实体对，以及具体数据集规定的关系标签集合；系统还可在推理时访问外部生物医学知识库、实体语义类型和从训练语料错误模式中得到的软验证规则。对于每个候选对 $(e_s,e_o)$，目标是在标签集合 $\mathcal{R}$ 中预测关系 $r$，或输出无关系标签 $r_{\varnothing}$；这里的关键假设是多数现实候选对并不表达有效关系，因此控制假阳性与找出真关系同等重要。本文采用训练自由设置：底层大语言模型不更新参数，而是先由 Decider 结合文本和外部证据提出关系假设，再以语义类型兼容性限制不合理标签，并由 Verifier 根据已观察到的错误模式复核候选预测。研究场景覆盖 SemRepGS、DDI 和 ChemProt 三种具有不同关系模式的基准，并使用发表于底层模型知识截止时间之后的 2026 年文献考察对未见文本的时间泛化；后者也用于降低基准内容可能已进入大语言模型预训练数据所造成的评估偏差。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$e_s$**

候选关系中的主体生物医学实体。

</div>
<div class="notation-item" markdown="1">

**$e_o$**

候选关系中的客体生物医学实体。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{R}$**

当前任务或数据集允许预测的关系标签集合。

</div>
<div class="notation-item" markdown="1">

**$r_{\varnothing}$**

表示候选实体对之间不存在目标关系的无关系标签。

</div>

</div>

**直接相关的工作**

- **ReOnto（Jain et al., 2023）**: ReOnto 将本体导出的关系路径并入 BioBERT 表示，在文本证据薄弱或含混时提供显式关系线索；它说明结构化本体知识可以辅助 BioRE，但依赖任务相关的神经表示学习。ANCHOR-RE 所针对的差距是无需额外模型训练、直接在推理阶段注入多种符号约束。
- **Olasunkanmi et al.（2025）的本体约束 LLM 框架**: 该方法先依据本体约束缩小候选谓词范围，再由大语言模型进行上下文推理，与本文利用符号知识限制预测空间的方向直接相关。论文指出，已有方案往往需要专门的多阶段推理流程；ANCHOR-RE 进一步联合知识库证据、实体语义类型兼容性和基于错误模式的验证规则，并保持底层模型参数不变。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ANCHOR-RE将句子级生物医学关系抽取表述为单标签分类：输入句子$s$、目标实体对$(e_1,e_2)$及其语义类型，从预定义关系集合$\mathcal{R}$中输出$\hat r$；集合包含表示不存在有效关系的$\textsc{norel}$。框架不更新大语言模型参数，而是把三类外部约束接入推理：从训练集检索的对比示例、来自生物医学知识库的结构化证据，以及根据模型历史假阳性错误归纳出的验证规则。

完整流程分为离线准备和在线推理。离线阶段将带标签训练样本编码为向量索引，并让冻结的大语言模型分析各关系上的系统性假阳性，建立按关系组织的错误模式知识库；在线阶段由Decider结合句子、检索示例、词汇触发线索和知识库证据提出候选关系，再由Verifier检查该候选是否符合已知过度预测模式。直观地说，系统先让模型在“相似案例和医学资料”的支持下作答，再安排一个专门寻找误判理由的复核者把缺乏文本依据的阳性预测退回$\textsc{norel}$。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 离线构建示例向量库

将上述字段序列化为模板文本，并用基于PubMedBERT的编码器映射为$d$维向量$h_{x_i}\in\mathbb{R}^d$，随后存入向量数据库。标签、实体名称与语义类型被共同编码，以同时表达关系语义和实体类型兼容性。

<div class="method-step__io" markdown="1">

**输入**：训练集中每个带标签实例，包括句子$s$、实体对$(e_1,e_2)$、实体语义类型和金标准关系$r$。<br>
**输出**：可按候选关系、语义类型和语义相似度查询的训练示例索引。

</div>

**直观理解**：这一步相当于建立一本可快速检索的案例手册；它不只寻找句子措辞相似的案例，也偏好实体类型和待判断关系相符的案例。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 离线学习错误模式与验证规则

先运行零样本分类，按关系$r$收集“模型预测为$r$、金标准却为$\textsc{norel}$”的失败池$\mathcal{F}_r$，同时保留预测正确的真阳性集合$\mathcal{T}_r$作为反例保护。Error Pattern Learner分批比较假阳性、真阳性、关系定义与已有规则，迭代新增、合并或修正规则，并以验证集micro-$F_1$选择最佳版本。

<div class="method-step__io" markdown="1">

**输入**：训练集的分层抽样子集、金标准标签、关系定义，以及不带检索增强的冻结Decider。<br>
**输出**：按关系组织、经验证集选择的错误模式知识库$K_{\mathrm{err}}$。

</div>

**直观理解**：系统不是手工规定所有禁用条件，而是复盘模型最常犯的“看起来有关、其实无关”错误。真阳性案例用于防止规则过宽，以免复核者把真正关系也一并否决。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按实例检索示例与外部知识

对每个候选关系$r\in\mathcal{R}(x)$分别检索案例，按向量余弦相似度和主客体语义类型是否完全匹配进行排序，并平衡选取标签为$r$的正例与标签为$\textsc{norel}$的负例。同时查询数据集对应知识库，序列化实体间直接关系、每个实体的邻接关系和知识库原有描述字段。

<div class="method-step__io" markdown="1">

**输入**：测试句子、目标实体对、实体语义类型，以及与该实体类型组合兼容的候选关系集合$\mathcal{R}(x)$。<br>
**输出**：对比式上下文示例$\mathcal{D}_{\mathrm{retr}}$与结构化知识证据$K_{\mathrm{ext}}$。

</div>

**直观理解**：正例告诉模型什么证据足以支持关系，负例则展示实体共现为何不一定构成关系；外部知识库提供另一条可核验的医学依据，但不会替代句内证据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成有依据的候选关系

Decider通过增强提示进行一次大语言模型推理；提示描述常见关系触发词、词法形式、典型句法模式和触发词到关系的映射。模型输出结构化候选，包括从原句复制的触发片段、简短解释和候选关系标签。

<div class="method-step__io" markdown="1">

**输入**：句子$s$、实体对$(e_1,e_2)$、候选关系定义、触发词指导、$\mathcal{D}_{\mathrm{retr}}$和$K_{\mathrm{ext}}$。<br>
**输出**：候选关系假设及其句内触发证据。

</div>

**直观理解**：这一模块像初审员：它必须指出原句中哪段文字支持判断，而不能只凭两个医学实体经常相关就猜测关系。触发词规则是软提示，因此模型仍可处理未被规则逐字覆盖的表达。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### ANCHOR-RE总体预测函数

$$
\hat{r}=g\!\left(f_{\theta}(s,e_{1},e_{2};\mathcal{D}_{\mathrm{retr}},K_{\mathrm{ext}}),K_{\mathrm{err}}\right)
$$

**符号说明**

- $\hat{r}$：系统输出的最终关系标签。
- $s$：包含目标实体对的输入句子。
- $e_1,e_2$：需要判断关系的两个目标实体。
- $f_{\theta}$：参数为θ的冻结Decider大语言模型，用于产生候选关系假设。
- $\mathcal{D}_{\mathrm{retr}}$：从训练语料检索出的正负对比式上下文示例。
- $K_{\mathrm{ext}}$：从外部生物医学知识库检索并序列化的结构化证据。
- $K_{\mathrm{err}}$：离线学习并经验证集选择的错误模式知识库。
- $g$：Verifier验证函数，用错误模式规则保留或否决候选关系。

<div class="equation-explanation" markdown="1">

**直观理解**：该式明确了两阶段决策结构：$f_\theta$先在示例和医学知识支持下提出候选，$g$再利用历史错误规律作最终复核。关键点不是训练一个新分类器，而是在冻结模型的推理前后接入可检索证据和显式拒绝机制。<br>
**原文位置**：第3.2节“Overview of ANCHOR-RE”，Figure 1之后的总体预测公式。

</div>

</div>

<div class="equation-block" markdown="1">

#### 关系条件化的示例检索评分

$$
\operatorname{score}_{r}(x,x_i)=\alpha\cdot\operatorname{sim}(h_x,h_{x_i})+\beta\cdot\mathbbm{1}\!\left[\operatorname{type}(x)=\operatorname{type}(x_i)\right]
$$

**符号说明**

- $\operatorname{score}_{r}(x,x_i)$：在候选关系r条件下，测试实例x与训练实例$x_i$的检索排序分数。
- $h_x,h_{x_i}$：测试实例与训练实例的向量表示。
- $\operatorname{sim}$：向量间的余弦相似度。
- $\operatorname{type}(x)$：实例x中主语实体与宾语实体构成的语义类型对。
- $\mathbbm{1}[\cdot]$：指示函数；括号内条件成立时取1，否则取0。
- $\alpha,\beta$：分别控制语义相似度和类型完全匹配奖励的权重。
- $r$：当前独立考虑的候选关系标签。

<div class="equation-explanation" markdown="1">

**直观理解**：检索分数由“文本和关系语义是否相近”与“主客体医学类型是否相同”两部分组成。这样可避免仅因句子措辞相似就取回类型不合适的示例，例如把药物—疾病关系案例用于化学物—蛋白质关系判断。<br>
**原文位置**：第3.3.1节“Demonstration Selection”的检索评分公式。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：该方法没有传统意义上的参数训练目标：Decider、Error Pattern Learner和Verifier使用的骨干大语言模型均保持冻结，不进行梯度下降、微调或提示参数优化。离线阶段优化的是外部资源而非模型权重：规则学习器从假阳性中迭代生成每个关系的软约束，随后以验证集micro-$F_1$作为模型选择准则，保留表现最好的错误模式知识库；检索示例数量$k$也依据验证集表现选择。因此，“优化”发生在规则版本和推理配置选择层面，而非神经网络参数空间。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Decider**

Decider是参数为$\theta$的冻结大语言模型$f_\theta$，通过提示同时接收任务定义、关系触发线索、对比式检索示例和外部知识证据。其结构化输出要求给出候选标签、简短推理以及从输入句子复制的触发片段，从而把关系判断锚定到可检查的文本证据。

> 直观理解：单纯提示的大语言模型容易把医学常识中的“可能有关”误当成句子实际陈述的关系。Decider加入案例、知识和触发线索，是为了让第一次判断既有上下文推理能力，又受到关系模式与证据来源的约束。

**2. Error Pattern Learner与错误模式知识库**

Error Pattern Learner是离线大语言模型模块，它从各关系的假阳性池$\mathcal{F}_r$归纳结构化验证问题，并参考真阳性集合$\mathcal{T}_r$、关系语义定义$\delta_r$和已有规则反复修订。每轮所得规则库在独立验证集上评估，最终采用验证micro-$F_1$最高的版本，而非直接选择规则最多的版本。

> 直观理解：该模块把具体误判概括成可复用的检查项，例如区分“两个实体仅在同一句共现”与“句子真正断言二者存在关系”。验证集选择用于约束规则复杂度，避免规则只记住训练错误或过度拒绝有效关系。

**3. Verifier**

Verifier是条件调用的二阶段判别模块$g(\cdot)$：它读取Decider给出的阳性关系及该关系专属规则，判断是否命中表面触发歧义、上下文共现等系统性过预测模式。命中任一规则即输出$\textsc{norel}$，否则维持候选关系，因此它本质上是面向假阳性的拒绝器。

> 直观理解：知识库可能缺失，初审模型也可能被看似因果的词误导，所以仅增加信息不一定足够。Verifier专门挑战阳性结论，相当于在写入生物医学知识图谱前增加一道质量控制。

**训练与推理**

离线准备首先把训练实例序列化并编码，建立可供近邻检索的向量数据库。随后在训练集分层子集上运行不带检索增强的零样本Decider：对每个关系$r$分别建立假阳性集合$\mathcal{F}_r=\{x\mid\hat y(x)=r\land y(x)=\textsc{norel}\}$和真阳性集合$\mathcal{T}_r$；Error Pattern Learner按批读取失败案例、真阳性、关系定义和现有规则，迭代执行规则提取与修订，直到没有新模式或达到最大轮数。所有关系的规则合并后，在验证集上选择micro-$F_1$最高的知识库版本；整个过程按数据集和骨干模型各执行一次。

在线推理时，系统先依据实体语义类型缩小可行关系集合；SemRepGS使用UMLS Semantic Network兼容性约束，而DDI因实体均为药物而不需要此约束。接着对每个候选关系检索平衡的正例和$\textsc{norel}$负例，并从相应知识库获取结构化证据；Decider生成带触发片段与解释的候选标签。若候选为阳性，Verifier读取该标签对应的规则进行拒绝判断；若候选已是$\textsc{norel}$则直接返回。ChemProt的评估设置不包含$\textsc{norel}$类，因此该数据集不启用Verifier。

**复现信息**

骨干模型方面，主要配置对Error Pattern Learner、Decider和Verifier统一使用$\texttt{gpt-5-mini-2025-08-07}$；为检验框架是否依赖专有模型，还使用Qwen3.5-2B与Qwen3-32B沿用相同提示和推理管线。开放权重模型采用确定性解码，温度为$0$、随机种子为$42$；其推理通过vLLM在单张NVIDIA H200 GPU上完成。

检索数量$k$按数据集通过验证集选择：SemRepGS为$3$、DDI为$4$、ChemProt为$2$。外部知识源与任务对应：SemRepGS查询UMLS Metathesaurus及其Semantic Network，DDI查询DrugBank，ChemProt查询CTD；证据包含可获得的实体间直接关系，以及每个实体最多$5$条邻接关系，并保留底层知识库已有的文本描述。证据块不再经过额外大语言模型生成，这一点有助于区分“知识库原始证据”与模型自行补写的内容。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- SemRepGS：包含 23 个标签，其中 22 种正关系及 $norel$；训练、开发和测试集分别有 8,084、756 和 3,211 个实例，测试集含 2,174 个 $norel$。它主要检验多关系、类别不均衡且负例较多时的抽取能力，并用于完整组件消融和开放权重模型泛化实验。
- DDI（SemEval-2013）：药物—药物相互作用数据，标签为 advise、effect、int、mechanism 与 $norel$；训练集和测试集分别有 27,792 与 5,716 个实例，无官方开发集，测试集含 4,737 个 $norel$。它检验系统能否从大量无关系候选中识别并细分药物相互作用。
- ChemProt：化学物—蛋白质关系数据，按评测所用 CPR 子类 cpr:3、cpr:4、cpr:5、cpr:6、cpr:9 统计；训练、验证和测试集分别有 4,169、2,427 和 3,469 个实例。该评测聚焦正关系标签之间的判别，因此检索阶段没有加入对比性的 $norel$ 示例，验证器也未应用。另设时间控制评测：从 2026 年发表的 100 篇生物医学文章构造 3,890 个候选实例，以测试训练截止时间之后的新文献。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Micro-$F_1$**

先跨类别汇总预测计数，再计算精确率与召回率的调和平均，更受高频类别影响。DDI 与 ChemProt 的单标签多分类评测包含全部标签，因此其 micro-precision、micro-recall 与 micro-$F_1$ 相同，只报告 micro-$F_1$。 （越高越好，表示总体错误与漏检之间取得更好的综合平衡。）

</div>
<div class="metric-item" markdown="1">

**Macro-$F_1$**

先分别计算各关系标签的 $F_1$，再对标签等权平均，因此比 Micro-$F_1$ 更能反映低频关系是否也得到改善。 （越高越好；若仅 Micro-$F_1$ 上升而 Macro-$F_1$ 不升，增益可能主要集中在高频类别。）

</div>
<div class="metric-item" markdown="1">

**Precision**

预测为正关系的实例中实际正确的比例。它是验证器和时间控制评测的关键指标，因为系统目标之一是压低大语言模型的假阳性。 （越高越好，表示输出关系更可信，但必须结合召回率理解，因为严格过滤也可能漏掉真实关系。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 专有骨干上的三个标准基准

<div class="result-value" markdown="1">

相对直接提示，最佳 ANCHOR-RE 配置将 SemRepGS 的 micro-$F_1$ 从 0.654 提升至 0.676，将 DDI 从 0.769 提升至 0.872；ChemProt 的摘要报告为从 0.939 提升至 0.941。

</div>

提升在 DDI 上最大、SemRepGS 上较小，ChemProt 上极弱。作者据此主张训练外的知识、示例和规则可改善推理可靠性；但 ChemProt 的差异没有统计显著性，而且正文、表格与摘要对其最佳值存在 0.941 与 0.943 的不一致，不能把该结果解释为稳定的大幅提升。

<div class="result-source" markdown="1">

来源：摘要；SemRepGS 见第 4.1 节表 2，DDI 与 ChemProt 见第 4.1 节表 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

With the proprietary backbone, ANCHOR-RE outperformed direct LLM prompting, improving micro-F1 from 0.654 to 0.676 on SemRepGS, from 0.769 to 0.872 on DDI, and from 0.939 to 0.941 on ChemProt.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 2026 年新发表文献的时间控制评测

<div class="result-value" markdown="1">

最佳配置在 3,890 个候选实例中输出 824 个正关系；专家随机评审其中 500 个正预测，69% 被判为正确。

</div>

该实验避免直接复用可能进入预训练语料的旧基准，说明系统在训练截止时间之后的文献上仍可得到约七成精度。它只评审预测为正的样本，因此估计的是 precision，而不是 recall 或 $F_1$；此外，新集合使用 PubTator3 识别实体，69% 不能与 SemRepGS 的精度作完全受控的直接比较。

<div class="result-source" markdown="1">

来源：第 4.2 节 Contamination-controlled Evaluation

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Using the best-performing configuration, ANCHOR-RE predicted 824 of the 3,890 candidate instances as containing a positive relation. Expert evaluation of 500 randomly sampled positive predictions showed that 69% were correct.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 开放权重模型上的跨骨干泛化

<div class="result-value" markdown="1">

在 DDI 上，完整框架使 Qwen3.5-2B 的 micro-$F_1$ 从 0.199 提升至 0.488，使 Qwen3-32B 从 0.567 提升至 0.772；SemRepGS 上对应最佳 micro-$F_1$ 分别为 0.465 和 0.577。

</div>

两个规模不同的开放权重模型都呈现组件加入后总体改善，尤其 DDI 上验证器贡献明显，支持框架收益并非专有 GPT 骨干独有。不过不同模型的绝对性能差距仍大，而且这些是同一组数据与提示流程内的结果，不能据此断言对所有开放模型或所有生物医学任务都能泛化。

<div class="result-source" markdown="1">

来源：第 4.3 节；详细数值见附录 E 表 6 与表 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The largest gains are achieved after introducing the Verifier, increasing micro-F1 from 0.199 to 0.488 for Qwen3.5-2B and from 0.567 to 0.772 for Qwen3-32B.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- ChemProt 报告存在内部不一致：表 3 所示“+ KB + Retrieval”为 0.941，正文称最佳 micro-$F_1$ 为 0.943，摘要又报告 0.941；且正文明确称差异不显著。最终引用该结果前必须核对原始表格、计算脚本或论文修订版。
- 时间控制评测只人工抽查 500 个正预测，未标注全部候选，因而无法计算召回率和 $F_1$，也未在同一新文献集合上报告直接提示或其他系统的受控基线；69% precision 还可能受到 PubTator3 实体标注质量与抽样误差影响。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Baseline：同一大语言模型骨干上的直接提示策略，不加入 KB 落地、检索示例或验证器。它控制了骨干模型能力，是判断神经—符号组件是否真正增益的核心参照。
- + KB：仅向模型提供结构化外部知识证据。与 Baseline 比较可隔离知识落地本身的效果，并检验“增加事实背景”是否足以改善关系判定。
- + KB + Retrieval：在 KB 证据上增加按候选标签检索的示例；SemRepGS 和 DDI 可包含支持与 $norel$ 对比示例。它检验模型是否需要具体正反判例来正确使用外部知识。
- 开放权重骨干 Qwen3.5-2B 与 Qwen3-32B：在相同组件递增设置下与专有 GPT 骨干形成跨模型比较，用于判断收益是否仅来自某个专有模型；原文还声称与既有推理式、监督式和指令微调方法比较，但所给节选未列出具体方法及完整分数。

**实验想回答的问题**

- 在不微调模型参数的条件下，ANCHOR-RE 将知识库（KB）落地、标签条件示例检索和规则验证器加入大语言模型推理后，能否在 SemRepGS、DDI 与 ChemProt 三个生物医学关系抽取基准上优于直接提示，并且各组件分别贡献了什么？
- 这种改进能否跨专有与开放权重模型成立，并能否在模型训练截止时间之后发表的文献上维持可用精度，从而降低预训练数据污染造成的评估偏差？

**实验实现**

主基准实验逐步加入 KB、检索和 Verifier，并在同一测试集上比较；报告的括号区间来自 $n=1{,}000$ 次 bootstrap，显著性使用配对 bootstrap，相对于 Baseline 或“+ KB + Retrieval”配置检验。时间控制实验采用最佳配置：系统在 3,890 个候选中预测 824 个正关系，再由专家人工评审其中随机抽取的 500 个正预测。开放权重泛化实验在 Qwen3.5-2B 和 Qwen3-32B 上重复组件递增比较。成本附录显示，专有骨干 gpt-5-mini-2025-08-07 在 SemRepGS、DDI、ChemProt 上平均每实例分别耗时 17.0、12.7、7.8 秒，总 API 成本分别为 5.71、9.17、5.97 美元；开放权重模型只报告推理延迟，未报告货币成本。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| SemRepGS：KB、检索与 Verifier 的递增消融 | 仅加入 KB 时，micro-$F_1$ 只由 0.654 增至 0.655，macro-$F_1$ 反而由 0.573 降至 0.569；加入标签条件检索后，两者升至 0.662 和 0.579；再加入 Verifier 后达到 0.676 和 0.597，相对 Baseline 分别达到 $p<0.01$ 与 $p<0.05$。 | 该序列隔离了三个组件：KB 单独没有实质收益，检索使知识与当前标签判定建立可模仿的联系，而 Verifier 提供最大额外提升。正文同时指出 Verifier 提高精度但降低召回率，因此它不是产生更多关系，而是删除较不可信的预测。 | 第 4.1 节 SemRepGS；表 2<br><span class="experiment-evidence">The best configuration (+ KB + Retrieval + Verifier) significantly increases micro F1 to 0.676 (p<0.01) and macro F1 to 0.597 (p<0.05) compared to the Baseline.</span> |
| DDI：KB、检索与 Verifier 的递增消融 | 仅加入 KB 时，micro-$F_1$ 从 0.769 微升至 0.774，macro-$F_1$ 从 0.595 微升至 0.596；加入检索后分别达到 0.839 和 0.661；加入 Verifier 后进一步达到 0.872 和 0.688，为该组最佳结果。 | DDI 的消融表明，大部分收益来自标签条件检索与验证，而非简单追加知识。由于测试集以 $norel$ 为主，检索到的正反示例有助于识别“看似相关但没有目标关系”的候选，Verifier 再进一步抑制假阳性；不过这只是根据数据构成和组件行为作出的分析，不是作者直接证明的因果机制。 | 第 4.1 节 DDI；表 3<br><span class="experiment-evidence">Applying the Verifier further increases micro F1 to 0.872 and macro F1 to 0.688, yielding the best overall performance.</span> |

**定性案例**

- 图 3 展示了供 Decider 使用的结构化证据块，例如“10074-G5 导致 AR 蛋白表达下降”以及“bicalutamide 导致 ABCB11 活性下降”。这些案例说明外部证据被整理为带实体方向、对象类型和作用变化的自然语言陈述，而不是只给模型一个无结构知识片段；但节选没有提供对应最终预测、金标或失败案例，因此只能用于理解输入形式，不能作为有效性证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：构建融合外部知识、 ontology约束和验证规则的训练无关LLM推理框架，用于可靠的生物医学关系抽取。; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`10f8089e986e7073bcf0142fad9318971d9fcfafb4b96a55b602706a33e9cc9c`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
