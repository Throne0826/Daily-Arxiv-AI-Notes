---
title: "[论文解读] Inhibitory Attention for Clinical Long-Context Reasoning: Characterizing and Mitigating Lost-in-the-Middle Effects in EHR Processing"
description: "[arXiv 2608.20348][LLM Reasoning] 本文研究电子健康记录中的临床“中间信息丢失”问题，并检验查询条件化的上下文抑制是否能比单纯提高证据句召回率更有效地支持长病历指令执行。"
arxiv_id: "2608.20348"
announcement_date: "2026-08-24"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-25T01:57:55.065820+00:00"
source_sha256: "eb122104f124d05ddec57a6526bb88ede2e86910e016cb96fb5ccce3bb17a67d"
tags:
  - "LLM Reasoning"
  - "电子健康记录"
  - "长上下文推理"
  - "临床中间遗失"
  - "位置检索偏差"
  - "抑制性注意力"
  - "查询条件化上下文选择"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.20348</p>

# Inhibitory Attention for Clinical Long-Context Reasoning: Characterizing and Mitigating Lost-in-the-Middle Effects in EHR Processing

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Sanjay Basu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Department of Medicine, University of California San Francisco, San Francisco, CA</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.20348) · [PDF 下载](https://arxiv.org/pdf/2608.20348) · **关键词** 电子健康记录, 长上下文推理, 临床中间遗失, 位置检索偏差, 抑制性注意力, 查询条件化上下文选择<br>
**代码**: [https://github.com/sanjaybasu/inhibitory-attention-ehr](https://github.com/sanjaybasu/inhibitory-attention-ehr)

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

本文研究电子健康记录中的临床“中间信息丢失”问题，并检验查询条件化的上下文抑制是否能比单纯提高证据句召回率更有效地支持长病历指令执行。

**不用术语来说**：患者病历可能长达十万余个词元；即使模型能够一次读入整份病历，也不等于它能同样可靠地利用每个位置的信息。模型往往容易找到开头或结尾的事实，却会漏掉位于中间的停药记录、异常化验或旧诊断，而这些信息可能直接改变临床判断。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将一般长上下文中的“中间信息丢失”具体化为临床场景中的 $CLitM$ 问题，并在真实电子健康记录上按信息位置及药物、诊断、化验和健康社会决定因素等事实领域进行系统刻画。
- 作者提出查询条件化临床抑制 $QCCS$：不以最大化金标准证据句召回为唯一目标，而是依据当前临床查询筛选并抑制不相关病历内容；论文同时比较其独立上下文选择形式与按词元接入差分注意力的形式。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

电子健康记录（EHR）是按时间累积的纵向临床文档，可能包含就诊记录、检验结果、用药史和社会史等信息，单名患者的完整记录可超过十万词元。尽管扩展上下文窗口等技术使大语言模型能够一次读入整份记录，但“能够容纳”并不等于“能够可靠利用”：模型对长上下文中部信息的检索准确率往往低于首尾位置，形成近似 U 形的位置—准确率曲线。本文将这种现象在临床场景中的表现称为临床中间遗失（CLitM）问题，关注模型能否不受证据位置影响，从单份纵向 EHR 中识别与临床指令相关的事实；其风险在于，中部遗漏的停药记录、异常检验值或既往诊断可能直接改变临床判断。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**中间遗失效应（Lost-in-the-Middle, LitM）**

大语言模型处理长输入时，对上下文开头和结尾的信息通常检索得更好，而对中间信息检索得更差。它反映的是模型内部的位置偏差，而不只是输入超过长度上限。

</div>
<div class="concept-item" markdown="1">

**抑制性注意力（inhibitory attention）**

标准注意力主要给不同词元分配非负关注权重；抑制性注意力则额外减去一部分由干扰信息获得的注意力质量。直观上，它不仅增强相关内容，还主动压低无关或重复内容。

</div>
<div class="concept-item" markdown="1">

**查询条件化上下文选择**

选择器依据当前临床查询为 EHR 中的句子评分，只把更符合查询意图的内容交给下游模型。本文研究的关键不只是找回某个标准答案句，而是构造整体上更利于完成指令的查询对齐上下文。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入由一条临床指令或查询以及同一患者按时间组织的长篇 EHR 构成，相关证据可能出现在记录的任意相对位置；输出是对该指令的正确临床回答，或在结构化实验中对后续实验室结局的预测。研究首先在 MedAlign 指令—回答数据上改变或分析证据位置，以刻画不同位置区间的检索准确率，并跨药物、诊断、实验室和健康社会决定因素四类事实及六个语言模型检验 CLitM；随后考察在有限上下文窗口下，是否可通过查询条件化句子筛选或抑制性注意力降低位置偏差。其基本假设是：单份 EHR 内存在大量与当前查询无关的句子，模型失败既可能来自未取回关键证据，也可能来自所选上下文与查询目标不一致，因此“标准证据句召回率”与最终指令完成准确率必须分开评价。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$Q_1,Q_2$**

差分注意力两条分支中的查询矩阵，用于分别计算正向关注和抑制性关注。

</div>
<div class="notation-item" markdown="1">

**$K_1,K_2$**

与两条查询分支对应的键矩阵；查询与键的相似度决定各位置获得的注意力。

</div>
<div class="notation-item" markdown="1">

**$d$**

查询与键的特征维度；注意力分数以其平方根进行缩放，避免点积数值过大。

</div>
<div class="notation-item" markdown="1">

**$\lambda$**

差分注意力中的可训练抑制系数，控制从正向注意力中减去第二个注意力分布的强度。

</div>

</div>

**直接相关的工作**

- **Liu et al. (2024), Lost in the Middle**: 该工作在非临床多文档问答中系统展示了长上下文准确率的 U 形曲线，并报告约 15–25 个百分点的中部低谷，是本文定义 CLitM 的直接基础；但其基准主要为合成或非临床任务，未检验真实纵向 EHR 中不同临床事实领域的位置偏差。
- **Ye et al. (2025), Differential Transformer**: 该工作提出差分注意力，以两个 softmax 注意力分布之差实现可训练的复制抑制。本文将其作为抑制性注意力基础，在 EHR 结构化预测任务中评估标量抑制，并进一步研究将查询条件化分数作为逐词元抑制权重的整合方式。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

电子健康记录通常由多年就诊笔记、药物史、实验室结果和社会史拼接而成，长度可超过十万词元。临床决策支持系统必须从任意时间位置取回关键事实，但标准长上下文模型存在位置偏差：相关信息落在序列中部时更容易被忽略。其后果并非一般问答中的轻微降分，而可能是遗漏已停用药物、关键异常指标或与当前治疗冲突的既往诊断。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **检索增强与提示压缩**：RAG、BM25、稠密检索、交叉编码器重排序及 LLMLingua 一类方法先依据查询寻找相关片段，或压缩原始提示，再把较短的候选上下文交给语言模型，以降低长序列中的噪声和计算负担。
- **注意力或键值缓存优化**：扩展上下文窗口、Flash Attention 和 Ring Attention 使模型能够处理更长输入；$H_2O$、SnapKV 等方法通过保留重要的键值缓存、淘汰较不重要的历史内容来节省推理资源。差分或抑制性注意力则进一步尝试从注意力分布中主动扣除无信息成分。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 能够容纳完整病历或降低长上下文计算成本，只解决了“能否输入”的工程问题，没有证明模型能从所有位置等概率地利用信息；标准 softmax 注意力仍可能偏向序列两端，使中部临床事实形成系统性盲区。
- 传统检索主要优化金标准证据句的召回或局部相似度，但召回到某一句并不保证下游模型能在其余噪声中正确理解并执行临床指令。提示压缩和 KV 缓存淘汰同样面向压缩或效率，并未直接针对与具体查询有关的临床上下文对齐。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前非临床多文档问答已观察到中间信息丢失，但尚不清楚该现象是否在真实纵向病历中跨临床事实领域稳定存在，也缺少对两类目标的直接区分：一种是尽可能召回含答案的证据句，另一种是为下游模型构造整体上与查询一致、噪声更少的上下文。因而，临床场景究竟应优先提高证据召回，还是应采用查询条件化抑制来改善端到端推理，仍未得到系统检验。

</div>
<div markdown="1"><span>核心问题</span>

本文要回答的是：关键事实在电子健康记录中的位置是否会系统性影响语言模型的临床检索与回答；若会，依据当前查询抑制无关内容的 $QCCS$，能否比标准检索、重排序、提示压缩及缓存压缩更有效地改善端到端临床指令执行，以及这种门控能否进一步作为逐词元抑制权重接入差分注意力。

</div>
<div markdown="1"><span>作者直觉</span>

长病历的困难不只是“找不到一根针”，还可能是模型在大量看似相关的片段之间无法保持正确关注。$QCCS$ 的思路类似于先按医生当前问题给病历做有选择的降噪：不要求保留字面上最像答案的单句，而是优先保留能共同界定药物、时间、疾病或化验语境的内容，并压低与问题无关的记录。这样即使没有精确命中金标准句，也可能为生成模型提供更连贯、更少干扰的证据环境；不过，附录所述单中心数据和小规模第二阶段试验意味着这一动机目前只得到概念验证，尚不能视为广泛临床有效性的定论。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文的方法围绕临床电子健康记录（EHR）的长上下文处理展开：先从临床记录数据集和指令中构造评测任务，再比较词法检索、密集检索、交叉编码器重排序、完整上下文以及查询条件上下文选择（QCCS）等处理方式，最后让大语言模型基于所提供的上下文重新作答，并用语义评判衡量结果。技术核心不是简单地检索包含答案的句子，而是根据当前查询选择并组织更有助于模型推理的上下文，以缓解信息位于长文本中部时的“中间遗失”现象。直观地说，方法试图把一份很长的病历变成一组与当前问题最相关、且更容易被模型有效利用的证据，而不是把整份病历原样塞给模型。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 数据与任务构造

从 MedAlign 等临床数据中建立长上下文问答或指令评测，并按照关键信息在文档中的位置划分中部与边缘位置。所给章节仅明确说明使用了 MedAlign 和留出的指令评测，完整的数据处理细节未提供。

<div class="method-step__io" markdown="1">

**输入**：临床电子健康记录、患者级长文本以及待回答的临床指令。<br>
**输出**：带有位置信息和目标答案的临床指令集合。

</div>

**直观理解**：先把问题放进真实病历中，并记录答案相关信息位于开头、结尾还是中间，以便判断模型是否会忽略长文本中部的内容。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选上下文检索或选择

生成多种上下文处理结果，包括 BM25 词法检索、排除标题后的 BM25、先用 BM25 筛选再用交叉编码器重排、密集向量检索，以及学习得到的 QCCS gate。QCCS 的具体网络结构和训练过程在所给章节中未明确报告。

<div class="method-step__io" markdown="1">

**输入**：临床指令与对应的长篇 EHR 文本。<br>
**输出**：供后续大语言模型使用的候选文本片段或查询条件上下文。

</div>

**直观理解**：不同方法像不同的资料管理员：BM25 按字面词匹配，密集检索按语义相似度匹配，交叉编码器进一步比较问题和片段；QCCS 则尝试选择更适合当前问题推理的上下文。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 大语言模型重新推理

将不同上下文版本分别输入 Qwen2.5-7B-Instruct，使模型重新生成答案；实验同时比较完整上下文、BM25、密集检索、交叉编码器和 QCCS 等条件。

<div class="method-step__io" markdown="1">

**输入**：原始完整上下文或上述方法筛选后的上下文，以及临床指令。<br>
**输出**：每个指令在不同上下文条件下生成的模型回答。

</div>

**直观理解**：不是只检查检索器有没有找到正确句子，而是把检索结果真正交给模型，看模型能否据此完成临床推理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 语义评判与位置分层分析

使用 LLM-as-judge 进行语义准确性评估，并按信息位于文档中部或边缘进行分层比较；另以 token-overlap 作为补充分析，并进行 gold sentence 检索条件下的控制分析。

<div class="method-step__io" markdown="1">

**输入**：模型回答、参考答案或目标指令，以及各回答对应的上下文位置和检索结果。<br>
**输出**：各方法的总体准确率、位置分层准确率，以及检索命中与最终回答质量之间的关系。

</div>

**直观理解**：评估重点是回答是否真正表达了正确含义，而不是是否碰巧复用了参考答案中的词；位置分层则帮助判断问题究竟来自检索，还是来自模型对长上下文的利用能力。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：所给章节没有提供 QCCS gate 或其他模型的明确训练目标、损失函数、监督信号和优化公式，因此无法可靠重建优化过程。现有内容只能确认 QCCS 被称为“learned” gate；其训练阶段与推理阶段的具体参数更新方式原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 多策略上下文检索基线**

比较 BM25 词法检索、排除标题后的 BM25、BM25 候选后交叉编码器重排，以及 all-MiniLM-L6-v2 密集检索。交叉编码器流程在所给结果中表示为 BM25-50 → CE → 20，但候选片段的具体表示、排序分数和最终截取规则未完整给出。

> 直观理解：这些模块用于测试“找到相关文本”是否足以解决长上下文问题，并区分字面匹配、语义匹配和二阶段重排的作用。

**2. 查询条件上下文选择（QCCS）**

QCCS 被描述为一个学习得到的 gate，用于进行查询条件的上下文选择；其下游评测显示，该选择机制不仅关注是否包含 gold sentence，还关注上下文是否与当前查询的推理需求对齐。所给章节未提供 gate 的输入特征、参数化形式、训练标签或损失函数。

> 直观理解：QCCS 的目标类似于为每个问题定制阅读提纲：重点不是机械地把标准答案所在句子找出来，而是挑出能帮助模型理解和推理的材料。

**3. 基于大语言模型的语义评估**

实验采用 Qwen2.5-7B-Instruct 进行重新推理，并采用 LLM-as-judge 评估回答准确性；token-overlap 仅作为辅助指标。章节还提到第二个独立评判者用于交叉验证，但所给文本未提供其完整协议和结果。

> 直观理解：该模块把“检索看起来相关”和“模型最后答对”分开测量，从而避免把检索命中误认为推理成功。

**训练与推理**

在推理评测时，给定临床指令和长篇 EHR，系统分别构造完整上下文、BM25 检索上下文、BM25 加交叉编码器重排上下文、密集检索上下文以及 QCCS 上下文，再将各版本输入 Qwen2.5-7B-Instruct 生成回答。随后使用 LLM-as-judge 评估语义准确性，并按信息位于中部或边缘进行比较；QCCS 的训练流程、是否使用独立训练集、训练期间是否冻结大语言模型，以及所有检索器的参数更新过程，原文未明确报告。

**复现信息**

所给章节明确涉及的可复现实验组件包括 MedAlign 数据集、Qwen2.5-7B-Instruct、BM25、all-MiniLM-L6-v2、BM25 候选后交叉编码器重排、QCCS gate、LLM-as-judge 和 token-overlap 辅助评估。检索文本的片段长度、top-$k$ 设置、提示模板、上下文拼接顺序、随机种子、QCCS 的模型结构与训练超参数，以及评判者提示词均未在所给材料中报告；不应据此假定具体实现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MedAlign：包含275名患者、约7.8万词元/患者和983个指令—回答对，来自单一学术医疗中心。实验1用其构造“干草堆中找针”检索任务，以测试正确答案证据位于不同EHR位置时的检索准确率；实验3则用其训练和评估$QCCS$门控器。经过可计算的位置标注后，实验1形成2,196个模型—指令观测。
- EHRSHOT：包含6,739名患者、4,170万条事件和15个二分类临床预测任务。实验2选取贫血、高钾血症、低血糖、低钠血症和血小板减少症五项实验室异常预测任务，使用官方训练/测试划分；由于$H^2O$运行超过7,200秒，低血糖未纳入主表。
- 实验3的门控器测试集：完整MedAlign测试人群包含74名测试患者、690行未去重的测试记录，用于查询条件化消融；主实验另使用按答案证据位置分组的检索与回答测试集。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**检索准确率/回答准确率**

检索准确率衡量系统是否找回包含正确答案证据的EHR位置；实验3的回答准确率由LLM-as-judge判断生成回答是否真正回答了问题，而非仅匹配若干词。 （越高越好，因为它同时反映证据定位或临床问题回答是否正确。）

</div>
<div class="metric-item" markdown="1">

**AUROC**

受试者工作特征曲线下面积，衡量模型区分阳性与阴性临床结局的排序能力，与具体分类阈值无关。 （越高越好；数值越大表示阳性病例通常获得更高风险分数。）

</div>
<div class="metric-item" markdown="1">

**AUPRC**

精确率—召回率曲线下面积，尤其适合评估类别不平衡的临床预测任务，因为它更直接关注阳性样本的查准率与召回率权衡。 （越高越好；在阳性病例较少时通常比AUROC更能反映实际识别能力。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 实验1：MedAlign六种模型的临床长上下文位置效应

<div class="result-value" markdown="1">

在2,196个模型—指令观测上，答案证据位置与检索准确率呈明显的$U$形关系：位于文档开头或结尾时较容易检索，位于中间时明显更困难。该结果说明临床EHR中的$LITM$效应不仅存在，而且幅度较大，并跨越不同模型规模和架构。

</div>

作者的结论是，模型并非均匀使用整份病历，而更依赖上下文边缘信息。它证明了位置敏感性这一现象，但单独不能证明某一种注意力机制或$QCCS$已经解决了该问题；还需要后续干预实验检验改进是否来自真正的证据定位。

<div class="result-source" markdown="1">

来源：Section 4.1, “CLitM is Real and Large in Clinical EHR”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across 2,196 instruction-response pairs and six model variants, retrieval accuracy exhibits a pronounced U-shaped curve as a function of answer position.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 实验2：EHRSHOT实验室异常预测中的注意力条件比较

<div class="result-value" markdown="1">

Differential Transformer相较标准注意力在贫血任务上的测试AUROC提高6.0个百分点，在高钾血症任务上提高4.2个百分点，并在贫血这一类别不平衡任务上改善AUPRC；$H^2O$在高钾血症AUROC上胜出。原文还指出低血糖因$H^2O$运行超过7,200秒而被排除，因此不能把该任务的缺失结果解释为模型性能失败。

</div>

结果支持“抑制或重构注意力可以帮助结构化临床预测”的方向，但并不表示一种方法在所有任务上都占优：Differential Transformer在多个任务上更好，而$H^2O$只在高钾血症AUROC上表现突出。由于这里的$H^2O$是基于嵌入范数的代理实现，结果不能直接验证完整原始算法。

<div class="result-source" markdown="1">

来源：Appendix G, Figure A3 description

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Differential Transformer outperforms standard attention on Anemia (+6.0 AUROC pts), Hyperkalemia (+4.2 pts), and on class-imbalanced AUPRC for Anemia; H2O wins on Hyperkalemia AUROC.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 实验3：Stage 2长上下文回答与LLMLingua-2压缩基线比较

<div class="result-value" markdown="1">

在按证据位置分组的Stage 2测试中，$QCCS$整体回答准确率为25.3%，中间位置（30%–70%）为16.7%，边缘位置为30.2%；对应的BM25、Map-Reduce和LLMLingua-2整体准确率分别为2.4%、14.5%和13.3%，中间位置分别为3.3%、20.0%和10.0%，边缘位置分别为1.9%、11.3%和15.1%。

</div>

$QCCS$相较BM25和LLMLingua-2在整体及边缘位置上更强，但Map-Reduce在中间位置达到20.0%，高于$QCCS$的16.7%。因此，该结果支持查询条件化筛选能够减少干扰，却不支持“$QCCS$在每个位置或每种策略上都最佳”；它更可能体现了检索保留与上下文压缩之间的权衡。

<div class="result-source" markdown="1">

来源：Appendix Q, Table A12, row “Middle (30–70%)”; column order: BM25, MR, LLMLingua-2, QCCS

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Middle (30–70%) 3.3 20.0 10.0 16.7

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- MedAlign仅包含275名患者且来自单一学术医疗中心，实验1的可计算位置标注进一步缩小到270个患者—问题对；因此$LITM$效应的普遍性以及$QCCS$在其他医院、病种和记录格式上的表现仍未得到充分验证。
- $H^2O$在实验2中使用编码器嵌入$
ackslash ell_2$范数作为重注意力代理，并非原始生成式算法的等价实现；同时低血糖任务因运行超时被排除，且实验3中不同测试人群存在去重差异，所以跨方法和跨任务的绝对性能比较应保持谨慎。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Standard Transformer：标准注意力模型，用于检验长上下文中未经特殊筛选的完整EHR处理效果。
- Differential Transformer：差分注意力模型，用于测试通过差分化注意力抑制部分干扰是否能改善结构化临床预测。
- $H^2O$ keep-50%：保留表示范数最高的50%位置并屏蔽其余位置，是原始$H^2O$重注意力保留方法在批量分类场景中的近似基线；它检验“保留高注意力代理位置”是否足够有效。
- BM25、Dense、Cross-Encoder（CE）和Map-Reduce：分别代表词法检索、向量检索、查询—文本交叉编码器重排序，以及先分块回答再汇总的长文档处理策略。它们用于区分$QCCS$的优势究竟来自检索、重排序、分块汇总，还是其查询条件化的抑制门控机制。

**实验想回答的问题**

- 临床电子健康记录（EHR）中的长上下文推理是否存在显著的“中间丢失”（Lost-in-the-Middle，简称$LITM$）效应，即答案证据位于文档中部时，模型检索和回答能力是否下降？
- 查询条件化的抑制性注意力方法$QCCS$能否在保留关键信息的同时减少无关临床文本干扰，并改善长上下文检索和下游临床预测？

**实验实现**

实验1在六个MedAlign发布模型上评估，包括GPT-4-32k、带多步精炼的GPT-4-32k、带Vicuna上下文格式的GPT-4-32k、MPT-7B-Instruct、Vicuna-13B和Vicuna-7B；六种模型共享相同指令，因此置信区间按$(患者,指令)$对进行聚类自助法抽样，而不是把2,196行当作相互独立样本，使用5,000次重采样和随机种子42。实验2比较三种注意力条件下的EHRSHOT预测，并以测试集AUROC和AUPRC为主要指标。实验3的Stage 2使用相同提示模板和LLM评审协议比较不同上下文筛选方法；附加的LLMLingua-2基线把完整时间顺序EHR压缩到约2,000词元，再交给Qwen2.5-7B-Instruct。原文明确说明，$H^2O$在分类任务中没有生成阶段，因此改用每个编码器嵌入的$
ackslash ell_2$范数作为“重注意力”代理，并保留范数最高的50%位置；这一做法是启发式近似，而非原始$$H^2O$$算法的等价实现。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 查询条件化消融：$QCCS$门控器保留查询与移除查询，$k=20$ | 在完整测试人群上，带查询的$QCCS$整体门控检索召回率为41.7%，中部位置为38.1%；去除查询后分别降至27.0%和14.3%，查询贡献为整体+14.7个百分点、中部+23.8个百分点。 | 该消融直接隔离了查询条件化输入的作用。性能显著下降表明门控器并非只学习一个与问题无关的“文本质量”分数，而是在利用当前问题判断哪些临床事件值得保留；不过绝对数值来自未去重测试人群，不能与主表数值直接混比。 | Appendix H, Table A1 description<br><span class="experiment-evidence">Query conditioning contributes +14.7 pp overall and +23.8 pp for middle-position recall, confirming that query context provides a meaningful training signal and that the gate is not simply learning a generic text-quality score.</span> |
| Stage 2评价指标消融：token-overlap与LLM-as-judge | 在中部30%–50%位置段，CE的token-overlap准确率为44.4%，但LLM评审准确率为0.0%；CE整体token-overlap为9.6%，LLM评审为1.2%。 | 这项消融检验的是评价指标而非模型结构。词元重叠会把“出现了相关词”误判为“回答正确”，尤其会高估交叉编码器；语义性的LLM评审更接近任务目标，但其本身也依赖评审模型和评审协议，仍需人工核查。 | Appendix H.1, Table A2 description<br><span class="experiment-evidence">CE token-overlap is substantially inflated vs. judge (9.6% vs. 1.2% overall), most severely at 30–50% (44.4% vs. 0.0%).</span> |

**定性案例**

- 原文选段未提供可核查的单个病例、问题、检索片段或生成答案的定性案例，因此不能据此分析某一具体病历中$QCCS$如何抑制干扰或找回中部证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It proposes an attention-based approach to characterize and mitigate lost-in-the-middle failures in long-context clinical reasoning.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`eb122104f124d05ddec57a6526bb88ede2e86910e016cb96fb5ccce3bb17a67d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
