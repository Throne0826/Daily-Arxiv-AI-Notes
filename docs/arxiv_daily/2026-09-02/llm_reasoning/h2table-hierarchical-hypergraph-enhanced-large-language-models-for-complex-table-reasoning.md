---
title: "[论文解读] H2Table: Hierarchical Hypergraph-Enhanced Large Language Models for Complex Table Reasoning"
description: "[arXiv 2609.01216][LLM Reasoning] H2Table旨在通过层次嵌套超图显式保留复杂表格的多级表头结构，并将编码后的结构信息以轻量软提示注入大语言模型，从而改善复杂表格问答中的结构感知与推理能力。"
arxiv_id: "2609.01216"
announcement_date: "2026-09-02"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:43:16.932333+00:00"
source_sha256: "10e726aba804bf3117fa575ca9947649af911d2e15d818fdb5d11a32fc218413"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "复杂表格问答"
  - "层次化嵌套超图"
  - "多级表头"
  - "超图消息传递"
  - "可学习查询向量"
  - "软结构提示"
  - "大语言模型"
  - "LoRA"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.01216</p>

# H2Table: Hierarchical Hypergraph-Enhanced Large Language Models for Complex Table Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Jia Ling, Yangfan Wang, Chen Tang, Haoming Tan, Yang Yang, Yi Guan, Jingchi Jiang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Harbin Institute of Technology；Affiliation: AI Research Center, Midea Group (Shanghai) Co., Ltd；Affiliation: Changchun University of Science and Technology；Affiliation: State Key Laboratory of Smart Farm Technologies and Systems</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.01216v1) · [PDF 下载](https://arxiv.org/pdf/2609.01216v1) · **关键词** 复杂表格问答, 层次化嵌套超图, 多级表头, 超图消息传递, 可学习查询向量, 软结构提示, 大语言模型, LoRA<br>
**代码**: [https://github.com/lila120/h2table](https://github.com/lila120/h2table)

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

H2Table旨在通过层次嵌套超图显式保留复杂表格的多级表头结构，并将编码后的结构信息以轻量软提示注入大语言模型，从而改善复杂表格问答中的结构感知与推理能力。

**不用术语来说**：复杂表格中的表头往往不止一层：上层表头限定下层表头的含义，下层表头再限定具体单元格。若把整张表直接转成一串文字，或者把所有表头放在同一层处理，模型就难以判断一个数值究竟受哪些表头共同约束，因而容易在比较、聚合和多步问答中使用错误的单元格。本文关注的核心需求，是在不过度增加训练成本的前提下，让大语言模型真正利用这种逐层传递的表格语义。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出层次嵌套超图表示及其层次感知编码器：用超边表示表头与其覆盖对象之间的一对多关系，并显式连接父表头和直接子表头，以保留复杂表格中从高层表头到低层表头、再到数据单元格的语义蕴含链。
- 提出基于可学习查询向量的结构对齐机制：从超图编码结果中提取少量、与任务相关的结构嵌入，将其作为软结构提示加入序列化表格文本，并配合LoRA对大语言模型进行端到端轻量微调。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于复杂表格推理与表格问答领域：模型接收包含多级行首或列首的表格及自然语言问题，并生成答案。此类表格不仅具有二维行列关系，还存在“上级表头—下级表头—数据单元格”的层级语义，例如一个总类别表头可统辖若干子类别，而每个子类别再对应多个数据单元格。主流大语言模型通常将表格序列化为一维文本，但这一过程容易破坏二维拓扑和表头层级；普通图又只能通过边直接表示成对关系，难以自然表达一个表头关联多个单元格的高阶关系。因此，本文以层次化嵌套超图保存复杂表格结构，并将结构表示与大语言模型的文本推理能力结合。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**复杂表格问答（Complex TableQA）**

输入是带有合并单元格、多级表头或嵌套行列结构的表格以及自然语言问题，模型需要依据表中信息生成答案。与平坦表格相比，正确推理往往要求先确定不同层级表头的管辖范围，再定位和组合相关数据。

</div>
<div class="concept-item" markdown="1">

**超图与超边**

普通图的一条边通常只连接两个节点，而超图中的一条超边可以同时连接多个节点，因此适合表示“一个行表头或列表头统辖多个单元格”的一对多关系。本文进一步允许不同层级的超边发生父子连接，以保留嵌套表头之间的从属关系。

</div>
<div class="concept-item" markdown="1">

**消息传递与跨模态对齐**

消息传递是让相连的节点或超边交换并聚合表示，从而把局部结构关系编码进向量；跨模态对齐则把这些结构向量转换为大语言模型能够利用的连续表示。本文使用可学习查询向量从超图编码结果中提取固定数量的结构特征，并把它们作为软结构提示送入语言模型。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入由一张具有多级行表头或列表头的复杂表格、针对该表格提出的自然语言问题，以及表格的序列化文本组成；输出是大语言模型生成的答案。核心假设是复杂表格中的语义依赖沿表头层级向具体单元格传递，因此不能仅把所有表头及其单元格压平到同一层。H2Table先把单元格建模为节点、把表头及其管辖关系建模为层次化嵌套超边，再通过跨节点、超边和父子超边的消息传递获得结构嵌入；随后以少量可学习查询向量压缩这些嵌入，将所得固定数量的结构感知向量与序列化表格文本共同输入采用LoRA轻量微调的大语言模型。本文关注生成式复杂表格问答，而不是仅做表格分类或结构编码。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **HYTREL**: HYTREL将表格表示为超图，以超边表达表头与多个单元格之间的一对多关系，但其设计面向简单平坦表格，未显式建模多级表头之间的父子依赖，也未与大语言模型结合，因此不适合直接完成生成式复杂表格问答。
- **TAMO**: TAMO把HYTREL式超图编码器接入大语言模型，是H2Table最直接的结构化基线；但它会将复杂嵌套表头压平，把高层表头直接连接到相关单元格，忽略不同表头层级之间的交互。H2Table针对这一缺口引入嵌套超边、跨层消息传递和基于可学习查询的结构对齐。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

表格问答和Text-to-SQL等任务需要模型同时理解单元格内容与二维结构。真实复杂表格常含跨行、跨列以及多级嵌套表头，一个数据单元格的完整含义由其所在行列上的多层表头共同决定；如果模型不能追踪这些层次约束，就难以可靠完成定位、比较、汇总和生成式回答。同时，依靠大规模高质量指令数据和全参数微调来弥补结构缺失，会带来较高的数据与计算成本。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **序列化表格的大语言模型方法**：将二维表格转换为一维文本序列，利用预训练语言模型的语义与生成能力完成推理；TableLlama、TableGPT等方法还通过大规模指令数据进行全参数监督微调。
- **图或超图结构建模方法**：HeGTa将表格表示为异构图；HYTREL以超边连接一个表头及其多个相关单元格，从而表达一对多关系；TAMO进一步把HYTREL式超图编码器与大语言模型结合，使结构表示能够服务于生成式表格任务。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 一维序列化会弱化表格原有的行列关系和多级表头结构，而全参数监督微调又依赖大量高质量训练数据并产生较高计算开销；标准图的边只能连接两个对象，也难以自然表达“一个表头约束多个单元格”的一对多关系。
- 已有超图方法仍未完整处理复杂层次结构：HYTREL主要面向扁平表格且没有集成大语言模型，难以直接支持生成式TableQA；TAMO虽然连接了超图编码器与大语言模型，却把不同层级的表头超边压平，并让高层表头直接连接数据单元格，因而丢失父子表头之间的跨层依赖和语义传递路径。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚缺少一种同时满足三项要求的方案：忠实表示多级表头及其父子关系；在编码阶段让信息在不同表头层级与数据单元格之间充分传播；以较低参数和计算成本把所得结构信息对齐并注入具有生成能力的大语言模型。此外，本文仍假设表头层次能够预先准确获得，尚未解决从原始表格自动恢复层次结构的上游问题。

</div>
<div markdown="1"><span>核心问题</span>

能否把复杂表格建模为保留父表头、子表头和数据单元格依赖关系的层次嵌套超图，通过跨层消息传递得到结构表示，再利用少量可学习查询向量和LoRA将该表示有效注入大语言模型，从而提升其在深层嵌套表格上的问答推理与结构鲁棒性？

</div>
<div markdown="1"><span>作者直觉</span>

多级表头像一棵逐层缩小适用范围的目录树：上层标题先确定大类，下层标题进一步限定条件，叶端才对应具体数值。只要超图保留这条层次链，编码器便可先汇聚单元格与局部表头信息，再在父子表头之间上下传递，最终把完整上下文送回单元格。可学习查询向量则像一组面向当前任务的“结构摘要槽位”，从大量编码结果中选择最有用的关系并压缩成少量连续提示，使大语言模型无需仅靠序列化文本自行重建整张表的结构。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

H2Table将复杂表格表示为层次嵌套超图，并用专门的超图编码器在数据单元格与表头、不同层级表头之间传播信息。随后，模型通过少量可学习查询向量从超图表示中提取固定数量的结构特征，将其作为软结构提示添加到序列化表格文本前，最终交由大语言模型完成表格问答。直观地说，该方法不再把表格完全压扁成一串文字，而是同时保留“单元格属于哪些表头”和“高层表头统辖哪些低层表头”的组织关系，并用查询向量把这些关系压缩成语言模型可使用的结构提示。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 层次嵌套超图构建

将所有数据单元格构成节点集合$V$，将各级表头和表示整张表的虚拟全局根构成超边集合$E$；用层次关系$R$表示父表头到子表头的有向依赖，用关联关系$I$连接单元格与最低层叶子表头。叶子表头的作用域由直接关联的单元格决定，高层表头的作用域由其子表头作用域的并集递归得到。

<div class="method-step__io" markdown="1">

**输入**：复杂表格中的数据单元格、行表头、列表头及其层级关系。<br>
**输出**：层次嵌套超图$\mathcal{H}=(V,E,R,I)$及其初始节点、超边表示。

</div>

**直观理解**：把每个单元格看作一个点，把能够同时覆盖一组单元格的表头看作一条超边；高层表头再像文件夹一样包含多个低层表头，从而保留表格的分组和嵌套结构。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 层次感知超图编码

编码器依次执行四阶段消息传递：V2E利用集合注意力将单元格信息聚合到叶子表头；C2P沿$R$自底向上使用图注意力网络传播子表头信息；P2C沿$R$的反向方向自顶向下传递全局上下文；E2V再用集合注意力将增强后的表头信息返回单元格，并使用残差连接。

<div class="method-step__io" markdown="1">

**输入**：超图结构$\mathcal{H}$以及单元格和表头的初始嵌入。<br>
**输出**：同时包含单元格语义、表头层次关系和全局表格上下文的结构特征$H$。

</div>

**直观理解**：信息先从单元格汇总到最具体的表头，再逐层汇总到高层表头和根节点；之后全局信息反向下发，最后回到单元格，使局部数值能够结合所属行列及整张表来理解。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 查询式结构特征对齐

将查询向量输入多层Transformer解码器；每层先通过多头自注意力建模查询之间的依赖，再通过交叉注意力以$H$作为键和值提取重要结构信息，最后经前馈网络得到更新后的查询表示$Q^{(l)}$。该模块把数量可能很大的节点和超边表示压缩为固定数量的结构向量。

<div class="method-step__io" markdown="1">

**输入**：超图编码器输出的密集结构特征$H$和一组可学习查询向量$Q^{(0)}$。<br>
**输出**：经过多层对齐的查询嵌入，作为软结构提示。

</div>

**直观理解**：查询向量像一组主动提问的摘要器：它们从整张表的结构表示中挑出最有用的模式，而不是把所有图节点全部塞进语言模型的上下文。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 双流输入与语言模型推理

将查询嵌入预置在序列化表格文本之前，形成同时包含结构流和文本流的输入，并将其送入下游大语言模型进行表格问答；训练时通过端到端微调使查询向量、对齐模块及允许更新的模型参数适应任务。

<div class="method-step__io" markdown="1">

**输入**：查询嵌入和序列化后的表格文本、问题文本。<br>
**输出**：对问题的最终答案。

</div>

**直观理解**：语言模型仍然阅读文字化表格和问题，但在文字前面额外获得一组浓缩的“表格结构提示”，因此能同时利用内容和布局关系。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 查询向量的逐层更新

$$
Q^{(l)}=\operatorname{FFN}\left(\operatorname{MCA}\left(\operatorname{MSA}\left(Q^{(l-1)}\right),H,H\right)\right)
$$

**符号说明**

- $Q^{(l)}$：第$l$层输出的查询向量表示。
- $Q^{(l-1)}$：第$l-1$层输入的查询向量表示。
- $H$：层次感知超图编码器输出的结构特征，作为交叉注意力中的键和值。
- $\operatorname{MSA}$：多头自注意力，用于建模不同查询向量之间的依赖。
- $\operatorname{MCA}$：多头交叉注意力，使查询向量从结构特征$H$中提取信息。
- $\operatorname{FFN}$：前馈网络，用于进一步变换交叉注意力融合后的表示。
- $l$：查询对齐Transformer层的索引。

<div class="equation-explanation" markdown="1">

**直观理解**：每一层先让查询向量彼此交流，再让它们读取超图编码器产生的结构信息，最后进行非线性变换。反复执行后，查询向量会学习成为整张表的结构摘要，供语言模型作为软提示使用。<br>
**原文位置**：第3.3节，公式未编号

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告独立的损失函数或完整优化目标。方法描述表明，查询式对齐模块通过端到端微调进行优化，使查询向量能够提取对表格问答有用的结构特征；在实验设置中，部分模型采用LoRA微调。原文还声称“By updating merely 1% of the parameters”，即仅更新约$1\%$的参数，但所给章节未明确说明该比例对应的具体参数集合、损失形式或冻结策略。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 层次嵌套超图表示**

超图定义为$\mathcal{H}=(V,E,R,I)$。其中$V$是数据单元格节点，$E$包含叶子表头、高层表头和虚拟全局根，$R\subseteq E\times E$表示父子表头关系，$I\subseteq V\times E_{\mathrm{leaf}}$表示单元格与叶子表头的关联。对叶子表头，作用域为$S(e_{\mathrm{child}})=\{v\in V\mid(v,e_{\mathrm{child}})\in I\}$；对高层表头，作用域为其子表头作用域的并集。

> 直观理解：普通序列只能记录表格文字出现的先后顺序，而该表示显式记录每个单元格属于哪些最低层表头，以及这些表头又属于哪个更高层分组。这样可以表达多级列标题、行标题及其共同覆盖范围。

**2. 层次感知超图编码器**

单层编码器包含V2E、C2P、P2C和E2V四个阶段。V2E与E2V使用集合注意力处理单元格和超边之间的信息交换；C2P与P2C在表头层次图上使用图注意力网络，根据表头间的语义相关性动态决定消息权重，并通过自底向上和自顶向下传播实现层次信息交互。

> 直观理解：该模块既让单元格和表头互相影响，也让不同层级表头互相传递信息；图注意力网络相当于学习“哪些相关表头应当更值得参考”，而不是对所有关系一视同仁。

**3. 查询式参数高效特征对齐模块**

模块由多层Transformer解码器构成。查询向量先进行多头自注意力，再对超图特征$H$进行多头交叉注意力，随后通过前馈网络更新；最终查询嵌入被投影为软结构提示，并与序列化表格文本拼接后输入大语言模型。

> 直观理解：超图表示属于连续结构空间，语言模型主要在文本语义空间中推理，二者不能简单直接拼接。查询式模块充当轻量翻译器，只提取固定数量、最能帮助问答的结构信息，从而减少上下文长度和训练参数。

**训练与推理**

训练阶段首先将表格构造成层次嵌套超图，初始化节点、超边和查询向量表示；超图编码器经过V2E、C2P、P2C和E2V传播，产生结构特征$H$。随后，查询向量通过多层自注意力与交叉注意力从$H$中提取结构摘要，并将其置于序列化表格文本之前，与问题共同输入大语言模型，通过端到端任务微调更新允许训练的模块。推理阶段执行相同的超图构建、结构编码、查询特征提取和双流输入过程，由大语言模型生成表格问答答案；原文未明确报告解码策略。

**复现信息**

为公平解读结果，需要注意该方法使用固定数量的可学习查询向量来压缩结构信息，但所给章节未明确报告查询向量数量、超图编码器层数、隐藏维度或优化器等复现参数。对齐模块采用Transformer解码器，并省略了标准残差连接和层归一化的公式表示；实验表格中的H2Table结果标注为LoRA变体，原文说明该参数高效范式仅更新约$1\%$的参数，但未在所给章节进一步给出具体LoRA配置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HiTab：论文的主要复杂层次表格问答基准，用于主结果、按表头嵌套深度划分的评测，以及消融实验。任务是TableQA，核心指标为Accuracy；实验特别关注Depth-3和Depth-4等高复杂度表格。原文未明确报告完整的数据集规模与训练、验证、测试划分。
- TATQA：另一种表格问答基准。原始数据是扁平矩阵表，作者使用大语言模型将其转换为包含行表头树、列表头树和数据矩阵的层次格式；由于四层表头仅有12张表，作者将这些实例排除在主实验之外。该数据集用于检验方法在不同表格来源上的表现，但结构转换可能引入噪声。
- AITQA：未参与主要训练的复杂层次表格问答基准，用作跨域、分布外测试集。作者将其原有的父表头标注转换为与HiTab一致的层次格式，用来检验模型是否学习到跨领域的结构表示，而非只记忆训练域。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

回答正确的样本比例；作者对预测结果进行统一的数据清理和格式归一化后计算，而不是采用严格的Exact Match。 （越高越好，因为它表示更多表格问题得到正确回答。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### HiTab按嵌套深度评测，比较Llama3.1-8B上的纯文本、TAMO与H2Table表示

<div class="result-value" markdown="1">

在HiTab的Depth-4子集上，H2Table准确率为0.7143，高于纯文本表示的0.5714和TAMO的0.6286；这表明优势主要出现在层次结构最复杂的表格上。

</div>

该结果支持作者关于显式结构建模的主张：当表头需要跨多层关系组织时，超图表示比将表格压成一维文本更不容易丢失结构信息。它并不单独证明H2Table在所有表格任务或所有模型规模上都必然更优，因为这里的数值来自特定数据集、模型和深度子集。

<div class="result-source" markdown="1">

来源：第4.2节 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the HiTab dataset at Depth-4, Llama3.1-8B with H2Table achieves an accuracy of 0.7143, yielding a significant absolute improvement over the pure text (0.5714) and TAMO (0.6286) baselines.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 不同开源基础模型上的HiTab整体表现

<div class="result-value" markdown="1">

在Gemma2-9B上，H2Table的HiTab平均准确率为0.7596，并高于同一基础模型下的纯文本和TAMO表示；作者还报告H2Table在Llama2-7B、Llama3.1-8B和Gemma2-9B中均取得各自模型组的最高平均准确率。

</div>

该结果说明H2Table不是只针对某一个LLM架构设计的输入技巧，而可能作为跨基础模型的结构表示方案。与DeepseekV3和GPT-4o的比较提示参数规模并非唯一决定因素，但这类比较不能替代严格控制训练数据、提示方式和模型访问条件的因果实验。

<div class="result-source" markdown="1">

来源：第4.2节 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For instance, fine-tuning Gemma2-9B with H2Table achieves an average accuracy of 0.7596 on HiTab, substantially surpassing both the pure text and TAMO representations.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨域分布外TableQA，分别在HiTab或TATQA上训练并在AITQA等测试集上评测

<div class="result-value" markdown="1">

结构感知表示改善跨域表现：在HiTab训练、AITQA测试时，纯文本LoRA准确率为0.8330，TAMO为0.8634，H2Table为0.8673；表2中的完整结果还显示H2Table在作者报告的各项域内和跨域设置中均优于基线。

</div>

该实验测试的是结构表示能否学习更具领域不变性的表格关系，而不是仅在训练分布内拟合答案。H2Table相对TAMO的提升较小但方向一致，因此它支持稳定的泛化优势；不过跨域结果仍可能受到不同数据集规模、标注方式和表格结构转换质量的影响，不能据此断言完全消除了域偏移。

<div class="result-source" markdown="1">

来源：第4.4节 Out-of-Distribution Generalization；数值见表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Most importantly, our proposed H2Table consistently achieves the best performance across all settings, outperforming all baselines by a clear margin.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- TATQA的层次结构由大语言模型从扁平表格转换而来，存在结构噪声；作者抽查100张表发现9张有明显错误，且错误转换子集的准确率明显较低，因此TATQA上的结果部分依赖预处理质量。
- 实验主要报告Accuracy，且采用统一的宽松匹配和答案格式归一化；原文未明确报告完整数据规模、训练验证划分、统计显著性检验或更细致的误差类别，因此部分性能差异的稳定性和错误来源仍需进一步核验。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 零样本推理：不进行任务微调的基础模型设置，用于衡量模型在没有专门训练时的表格问答能力。
- 纯文本表示加LoRA微调：把表格表示为文本序列，再使用LoRA进行参数高效微调；这是检验显式层次结构是否优于传统线性化输入的直接基线。
- TableLlama：在多种表格数据上进行大规模监督微调、并在多个表格推理任务中取得较强表现的模型，作为具有代表性的强表格推理基线。
- TAMO：将表格视为独立模态的结构感知方法，论文称其在若干基准上优于TableLlama；与H2Table比较可以检验层次嵌套超图表示相对于另一种表格专用表示的价值。

**实验想回答的问题**

- 在具有多层嵌套表头的复杂表格问答中，H2Table是否比纯文本线性化和其他结构感知表示更能保持表格层次结构，并提升不同嵌套深度下的回答准确率？
- H2Table的层次超图编码器、基于GAT的消息传递和查询向量桥接分别是否有效，以及这种结构表示能否提升跨数据集的分布外泛化能力？

**实验实现**

所有比较方法均使用相同的答案清理和格式归一化协议，以保证准确率可比。主要实验以Llama2-7B为基础模型，并扩展到Llama3.1-8B和Gemma2-9B；H2Table的节点嵌入来自预训练RoBERTa-large的最后一层，超图编码器隐藏维度设为1024。基线和H2Table均采用端到端LoRA微调，LoRA秩为8，损失函数为二元交叉熵；附录进一步给出LoRA的$\r=8$、$\alpha=16$、dropout为0.05、AdamW优化器、学习率$1\times10^{-5}$以及最大推理上下文长度4096等设置。训练输入由图或查询嵌入、包含表格描述和问题的文本提示、以及目标答案拼接而成。TATQA的结构转换误差通过人工抽查100张测试表进行评估：其中91张转换正确、9张存在明显结构错误；所有方法在同一转换后的数据上训练和测试，因此相对比较仍保持一致。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| HiTab上以Llama3.1-8B为骨干，比较纯文本LoRA、TAMO LoRA与完整H2Table LoRA | 表2中，HiTab训练、HiTab测试的准确率依次为纯文本LoRA 0.6774、TAMO LoRA 0.7643、H2Table LoRA 0.7713；在HiTab训练、AITQA测试时，三者分别为0.8330、0.8634和0.8673。 | 该对照逐步增加表格结构建模，显示TAMO相对于纯文本已有收益，而完整H2Table在域内和跨域设置中进一步提升。由于不是逐个删除H2Table内部组件的严格因子实验，这一结果主要验证整体表示的有效性，不能单独确定每个模块的独立贡献。 | 表2；第4.3节 Ablation Study及第4.4节 Out-of-Distribution Generalization<br><span class="experiment-evidence">+pure text (LoRA) 0.6774 0.2548 0.8330 -；+TAMO (LoRA) 0.7643 0.3156 0.8634 0.4721 0.6086 0.7974；+ H2Table (LoRA) 0.7713 0.3225 0.8673 0.4745 0.6313 0.8220</span> |
| 移除H2Table的关键组件：文本特征模块、完整层次超图编码器、GAT消息传递或查询向量对齐 | 移除文本特征模块或完整编码器会导致严重性能下降；移除GAT或查询向量会在大多数子集上产生轻微但一致的下降。作者还报告无GAT版本在Depth-1上表现很强，但在Depth-3和Depth-4上的差距更明显。 | 文本模块提供单元格和问题的语义基础，编码器负责显式传播层次结构信息，GAT负责按层次进行超边到节点的消息聚合，查询向量则把结构编码结果对齐并压缩成LLM可使用的表示。无GAT在平面表格上仍有竞争力，说明复杂消息传递并非所有样本都需要；其在深层表格上的劣化更能支持GAT对层次推理的针对性作用。原文未明确报告各个删除组件对应的完整数值表。 | 第4.3节 Ablation Study；图4<br><span class="experiment-evidence">As visualized in Figure 4, removing the textual feature module (w/o text) causes a catastrophic performance collapse (represented by the blank row), underscoring that textual semantics remain the foundation of table understanding.</span> |

**定性案例**

- TATQA结构转换质量分析：作者随机人工检查测试集中的100张表（对应600个问题），发现91张转换正确、9张存在明显结构错误；在Gemma2-9B上的H2Table评测中，正确转换子集（546个问题）准确率为52.20%，错误转换子集（54个问题）为37.04%，完整测试集为52.07%。这说明结构抽取错误会直接损害后续问答，但由于错误率为9%，整体结果仍接近正确转换子集。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文通过层次超图结构增强LLM对复杂表格的结构化问答与推理能力，核心是语言模型推理。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`10e726aba804bf3117fa575ca9947649af911d2e15d818fdb5d11a32fc218413`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
