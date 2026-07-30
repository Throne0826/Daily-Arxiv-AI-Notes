---
title: "[论文解读] ARC-Encoder: learning compressed text representations for large language models"
description: "[arXiv 2510.20535][LLM 效率] ARC-Encoder旨在不修改目标大语言模型的前提下，将长文本压缩成可直接替代原始词元嵌入的连续表示，并通过轻量适配支持多个解码器。"
arxiv_id: "2510.20535"
announcement_date: "2026-07-30"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T07:32:04.551273+00:00"
source_sha256: "9d21f1ee222b0d052efa001762c2da7e0973ef669752c720f347d9a7a6bf7ae0"
tags:
  - "LLM 效率"
  - "LLM 其他"
  - "LLM Reasoning"
  - "大型语言模型"
  - "上下文压缩"
  - "软压缩"
  - "连续文本表示"
  - "冻结解码器"
  - "池化 token"
  - "上下文学习"
  - "长上下文扩展"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2510.20535</p>

# ARC-Encoder: learning compressed text representations for large language models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Hippolyte Pilchen, Edouard Grave, Patrick Pérez</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2510.20535v2) · [PDF 下载](https://arxiv.org/pdf/2510.20535v2) · **关键词** 大型语言模型, 上下文压缩, 软压缩, 连续文本表示, 冻结解码器, 池化 token, 上下文学习, 长上下文扩展  
**代码**: [https://github.com/kyutai-labs/ARC-Encoder](https://github.com/kyutai-labs/ARC-Encoder)  **项目页**: [https://huggingface.co/collections/kyutai/arc-encoders-68ee18787301407d60a57047](https://huggingface.co/collections/kyutai/arc-encoders-68ee18787301407d60a57047)  

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

ARC-Encoder旨在不修改目标大语言模型的前提下，将长文本压缩成可直接替代原始词元嵌入的连续表示，并通过轻量适配支持多个解码器。

**不用术语来说**：大语言模型读取的文本越长，推理所需的计算和显存通常越多，还可能因关键信息被大量内容稀释或超过上下文窗口而降低效果。现有压缩方法要么难以大幅缩短文本，要么需要专门改造或微调负责生成答案的模型，因此需要一种既能明显减少输入长度、又尽量保持原模型能力的方案。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出ARC-Encoder，将文本压缩为数量更少的池化连续表示，并在词嵌入层之后送入保持冻结且结构不变的解码器，从而兼顾上下文压缩与原有生成能力。
- 探索跨解码器的可移植压缩：一个共享编码器可通过参数量不足编码器参数1%的小型MLP适配不同解码器，并可通过并行压缩文档分块用于扩展上下文。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大型语言模型在检索增强生成（RAG）、上下文学习和长文档问答中需要处理大量输入 token，但 Transformer 自注意力的计算量随序列长度近似二次增长；过长上下文还可能稀释关键信息或超过模型的上下文窗口。上下文压缩因此试图在保留生成所需语义的同时缩短输入：硬压缩直接删除、筛选或概括文本，易解释且通常不依赖特定模型，但压缩能力有限；软压缩则把文本编码为少量连续向量，压缩率更高，却往往需要微调或修改目标解码器。本文研究后一种设定，并要求目标解码器保持冻结、架构不变，使压缩表示能够像普通 token 嵌入一样直接输入不同的大语言模型。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**上下文压缩（context compression）**

将原始长文本变成更短的输入，同时尽量保留回答问题或继续生成所需的信息。其直接目的，是减少解码器处理的序列长度，从而降低注意力计算与推理成本。

</div>
<div class="conceptitem" markdown="1">

**软压缩（soft compression）与连续表示**

软压缩不必保留可读文本，而是用编码器把多个 token 的信息汇聚成少量稠密向量。ARC-Encoder 输出的这类向量被放在解码器嵌入矩阵之后，替代对应原文 token 的嵌入。

</div>
<div class="conceptitem" markdown="1">

**冻结解码器（frozen decoder）**

训练压缩器时不更新目标大语言模型的参数，也不改变其网络结构。这样可降低模型因专项微调而遗忘原有能力的风险，并允许同一解码器在压缩输入和标准文本输入之间切换。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是需要即时处理的文本上下文，以及一个不允许修改参数或架构的自回归解码器大语言模型；输出是由独立编码器生成的一段更短的连续表示序列。每个“pooled token”汇聚一组原始 token 的信息，这些表示绕过解码器的词嵌入查表环节，直接作为输入嵌入供其生成答案或续写。论文通常采用 4 倍或 8 倍池化，即将输入表示长度压缩为原 token 数的约四分之一或八分之一；同时研究用不足编码器参数量 1% 的小型 MLP 接口，使一个编码器适配预先指定的多个解码器。应用设置包括少样本上下文学习、问答和长上下文扩展，其中长文档可分块并行压缩后再交给解码器。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$x$**

池化或压缩因子；编码器输出的连续表示数量约为原始文本 token 数的 1/x，文中典型取值为 x\in\{4,8\}。

</div>
<div class="notationitem" markdown="1">

**$x\times$**

表示相对于原始 token 序列的长度压缩倍数；例如 4\times 池化意味着约每四个原始 token 对应一个压缩表示。

</div>

</div>

**直接相关的工作**

- **Gist tokens 与 memory tokens（Mu et al., 2024；Chevalier et al., 2023；Ge et al., 2024）**: 这些方法同样以少量连续向量概括完整输入，说明软压缩可以显著减少解码器接收的序列长度；但通常需要改变注意力机制，或在对齐预训练后继续联合微调编码器与解码器。ARC-Encoder的关键区别是保持目标解码器参数与结构不变，并让压缩向量直接替代普通 token 嵌入。
- **Tang et al. (2025) 的 merged-token 压缩方法**: 该工作与本文的池化式表示最接近，也用合并后的 token 替代部分输入，而非仅在输入前附加 memory token；但其多个训练阶段还会训练解码器。ARC-Encoder把研究重点放在仅训练编码侧，并进一步支持通过小型 MLP 让单个编码器服务多个解码器。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

检索增强生成、思维链推理以及包含详细指令或外部文档的应用不断拉长模型输入。Transformer注意力的计算成本随序列长度呈二次增长，长上下文还可能稀释关键信息或触及模型的上下文窗口上限，因此在线处理文档时亟需减少实际送入解码器的表示数量。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **硬压缩**：通过删除、裁剪或摘要来减少原始词元，只把保留下来的离散文本交给模型；其结果可读、通常不依赖特定模型。
- **软压缩**：把一段文本编码为少量稠密连续向量，例如记忆词元或gist词元，再让解码器依据这些向量生成输出，通常能达到比硬压缩更高的压缩率。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 硬压缩虽然具有可解释性和模型无关性，但压缩幅度有限；删除或摘要文本也使其难以在高压缩率下完整保留后续任务所需语义。
- 多数现有软压缩方法需要微调甚至修改目标解码器，并常为每个解码器训练独立编码器；这既可能使模型遗忘原有通用能力，也增加了在多个大语言模型之间迁移和部署压缩器的成本。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前缺少一种面向动态、在线文档处理的软压缩机制：其连续表示既能被未经修改的解码器直接接收，又能保留少样本学习及跨任务能力，并可由同一编码器低成本适配多个解码器。

</div>
<div markdown="1"><span>核心问题</span>

能否只训练文本编码器及极小的接口模块，把上下文压缩为显著更短的连续表示，在冻结目标解码器的情况下维持接近完整文本输入的任务表现，同时支持上下文扩展和多解码器复用？

</div>
<div markdown="1"><span>作者直觉</span>

解码器本来就是从词嵌入向量而非字符本身开始计算，因此压缩器无需生成可读摘要；它可以学习把若干词元的信息汇聚为少量、维度和分布适合解码器的向量，并从词嵌入层之后注入。共享编码器负责提取通用语义，小型MLP只负责把这些语义“翻译”为不同解码器熟悉的表示空间，于是可在不动解码器主体的情况下减少输入长度并实现跨模型适配。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ARC-Encoder采用“可训练压缩器＋冻结解码器”的端到端结构。输入文本先由去除因果掩码和输出头的Transformer编码器进行双向表征；编码器最后一层自注意力将连续若干token的查询向量取平均，使长度从n降至约n/x，其中x为池化因子；随后，两层无激活MLP把压缩表示映射到目标解码器的词嵌入维度。所得连续向量直接替代原始token嵌入送入冻结的解码器，因此无需修改解码器架构或参数。
训练分为预训练与任务适配。预训练交替执行“重构”和“续写”：前者要求解码器从压缩表示恢复全文，保证表示保留信息；后者把自然文本片段替换为压缩表示，并要求模型预测其后的文本，使表示适合实际条件生成。任务微调仍只更新编码器、投影器及特殊标记，可加入少量上下文示例；多解码器版本进一步共享同一个编码器，但为每个解码器保留独立投影器和特殊标记。直观地说，ARC-Encoder把长文本制作成解码器能够直接读取的“连续速记”，既减少输入长度，又尽量不改变原模型本身。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 文本双向编码

使用基于LLM Transformer改造的编码器处理输入：移除语言模型输出头和因果注意力掩码，使各位置能够利用双向上下文形成隐藏状态。

<div class="method-step__io" markdown="1">

**输入**：长度为n的文本token序列及其初始嵌入。  
**输出**：包含上下文信息的长度为n的隐藏状态序列。

</div>

**直观理解**：普通生成式LLM通常只能向左看；取消因果掩码后，编码器可同时查看一个token前后的内容，先充分理解全文再进行压缩。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 查询池化压缩

在编码器最后一层自注意力中，将每x个连续位置对应的查询向量进行平均，而键和值保持未压缩；这些合并后的查询继续关注完整的键和值序列。

<div class="method-step__io" markdown="1">

**输入**：编码器前部各层处理后的隐藏状态，以及目标池化因子x。  
**输出**：长度由n缩短至约n/x的压缩隐藏状态序列。

</div>

**直观理解**：每组token只派出一个合并后的“提问者”，但它仍能查阅全部原始信息。把池化放在最后一层，是为了先让信息得到充分加工，再减少表示数量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 解码器空间对齐

使用一个带维度瓶颈、无激活函数的两层MLP，将编码器输出线性映射到目标解码器的嵌入空间；同时在压缩序列后附加用于区分任务的已学习特殊标记。

<div class="method-step__io" markdown="1">

**输入**：池化后的编码器隐藏状态，以及当前目标解码器要求的词嵌入维度。  
**输出**：可直接作为目标解码器输入嵌入的连续压缩表示。

</div>

**直观理解**：编码器和解码器使用的表示坐标系可能不同，投影器相当于一个轻量“转接头”；特殊标记则告诉模型接下来应恢复原文还是继续写作。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 冻结解码与任务输出

用压缩表示替代对应文本的token嵌入，并将其输入参数冻结、架构不变的自回归解码器；解码器按照教师强制训练或自回归推理生成目标token。

<div class="method-step__io" markdown="1">

**输入**：压缩连续表示、任务特殊标记，以及任务模板中可能存在的未压缩查询、示例或答案前缀。  
**输出**：重构文本、自然文本续写或下游任务答案。

</div>

**直观理解**：解码器把短得多的连续表示当作原文本来读取。模型的通用生成能力保留在冻结解码器中，任务适配主要由前端压缩器承担。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

这篇论文不以中心数学公式展开，或全文中未提取到可靠的关键公式。

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练采用标准token级交叉熵损失，但原文节选没有给出独立编号或显式数学公式，因此不额外构造方程。基础预训练在两个目标间交替：重构目标把整段文本压缩后交给解码器，并以原始全文token作为教师强制目标，用于训练信息可恢复的表示；续写目标则将自然文本中的子序列替换为压缩表示，只要求解码器预测紧随压缩片段之后的文本，使压缩表示适配推理时的条件生成。作者指出，单纯重构即使能在约128-token短序列上以16倍池化实现近乎完美恢复，也可能导致解码器机械复述上下文而不能提取下游任务所需信息，因此两个目标承担互补作用。
下游微调沿用续写式目标，并可把压缩文档、未压缩查询和答案交错组织成结构化提示。损失掩码覆盖除最后一个压缩序列后续token之外的所有位置；在少样本设置中，这些保留位置对应最终答案，从而让上下文示例参与条件构造但不直接贡献监督损失。多解码器训练也采用交替策略：每步均匀采样一个解码器，通过同一交叉熵目标更新共享编码器及被选解码器的专属投影器和特殊标记，以平衡各解码器的训练曝光。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双向Transformer编码器与末层查询池化**

编码器由LLM Transformer改造而来，移除输出头和因果掩码。池化嵌入最后一层自注意力：连续查询按池化因子x取平均，键和值维持原长度，因此输出位置数约为原来的1/x；作者报告更早插入池化会降低性能。

> 直观理解：该模块同时负责“理解”和“压缩”。只压缩查询而保留完整键和值，使每个压缩位置仍有机会读取全序列信息，比过早删除中间信息更稳妥。

**2. 瓶颈MLP投影器与任务特殊标记**

投影器是无激活函数的两层MLP，通过中间维度瓶颈把编码器输出映射到解码器嵌入维度。压缩序列后附加已学习的<Rec>或<Cont>标记以指示重构或续写；多解码器训练时，投影器和特殊标记均为解码器专属，这些专属参数合计少于编码器权重的1%。

> 直观理解：投影器解决编码器输出不能直接被不同解码器理解的问题，特殊标记则消除两种训练任务之间的歧义。专属部分很小，因此增加一个解码器不需要复制整个编码器。

**3. 冻结目标解码器**

训练和适配过程中不更新目标解码器，也不修改其网络结构；ARC-Encoder生成的连续表示直接取代相应原文token的输入嵌入。预训练、下游微调和多解码器训练的梯度均用于编码器、投影器及相关特殊标记。

> 直观理解：冻结解码器把风险限制在压缩前端：即使压缩器为特定任务学习，原LLM的参数和常规使用能力也不会因这次训练而被覆盖。

**训练与推理**

训练时，首先使用重构与续写任务交替预训练ARC-Encoder。重构样本将压缩序列与<Rec>标记送入冻结解码器并监督全文恢复；续写样本用压缩表示替换文本子段，附加<Cont>标记，再监督其紧邻后续token。完成预训练后，可针对上下文学习、长上下文理解或其他任务微调压缩器；少样本微调可混合压缩文档、全文查询及示例答案，并只在最终答案位置计算损失。预训练与微调可以采用不同池化因子，原文称预训练时使用比微调更高的因子可改善模型，但节选未给出该结论对应的具体配置和数值。
推理时，待压缩上下文经过双向编码、末层查询池化和MLP投影，形成约n/x个连续向量；这些向量代替原始n个上下文token的嵌入，与未压缩的查询或提示部分共同输入冻结解码器，随后按常规自回归方式生成答案。典型池化因子为4或8，即理论上将被压缩部分的表示数量缩至约四分之一或八分之一。对于多个目标解码器，推理时复用共享编码器并选择与当前解码器对应的投影器和特殊标记。

**复现信息**

公平理解该方法所需的关键实现选择有四点：第一，池化位于编码器最后一层自注意力而非输入端或较早层，且只平均连续查询，键和值不压缩；第二，两层MLP不使用激活函数，并通过瓶颈完成维度映射；第三，解码器在所有训练阶段均冻结，所谓参数量开销应区分共享编码器与解码器专属的投影器、特殊标记；第四，池化因子x决定压缩序列长度约为n/x，若n不能被x整除时如何处理边界，原文节选未明确报告。训练语料组成、优化器、学习率、批量大小、精确提示模板及损失权重等复现细节在所给节选中亦未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- 短上下文问答组：Natural Questions、TriviaQA、HotpotQA distractor和SQuAD。实验用NV-Embed v2从Atlas的Wikipedia切块中检索Top-5段落，以模拟RAG；平均文档长度随解码器分词器而异，约为133至185词元，但FLORES之外的HotpotQA表中长度约1285至1479词元。评测训练集被明确排除在微调数据之外，用于检验跨数据集泛化，而不是记忆基准训练样本。
- 短上下文生成组：FLORES覆盖英语到丹麦语、法语、德语和西班牙语四个翻译方向；CNN-DailyMail用于摘要。所有任务采用5-shot，每个示例由文档、问题或任务指令、答案组成，并压缩每个示例中的上下文。FLORES文本很短，平均不足30词元，因此也用于暴露固定数量记忆令牌方法可能实际扩张输入的问题。
- 长上下文组：ZeroSCROLLS中的NarrativeQA、QASPER、GovReport和QM-Sum验证集，分别检验长文问答与长文摘要。推理时原始上下文最多截断到32k词元，再按块并行压缩；长上下文微调数据则由Wikipedia切块、PG-19书籍和RedPajama中的ArXiv论文合成，每个上下文最多分为32个、每个1024词元的块。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**Exact Match（EM）**

问答预测经小写化、空白修正并移除标点和冠词后，与参考答案完全一致时记为1，否则为0。它强调答案格式和内容均准确，作者用它避免指令模型仅复述上下文却获得虚高评价。 （越高越好，因为更高比例的样本与标准答案严格匹配；但它不会给语义等价、措辞不同的答案部分得分。）

</div>
<div class="metricitem" markdown="1">

**BLEU**

衡量机器翻译输出与参考译文之间的词片段重合度；论文报告英语到四种欧洲语言方向的平均BLEU。 （越高越好，表示与参考译文的局部表达更接近，但不等同于完整的人类翻译质量判断。）

</div>
<div class="metricitem" markdown="1">

**F1与ROUGE-L**

长上下文问答的NarrativeQA和QASPER使用F1，兼顾答案词项的精确率与召回率；CNN-DailyMail、GovReport和QM-Sum使用ROUGE-L，依据预测摘要与参考摘要的最长公共子序列衡量覆盖程度。 （均为越高越好：F1表示答案内容重合更充分，ROUGE-L表示摘要与参考文本的序列覆盖更强；二者都不是事实正确性或人工偏好的完整替代。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 短上下文、4倍固定压缩：分别为Mistral 7B和Llama3.1 8B训练专用ARC-Encoder，与完整未压缩输入及其他压缩方法比较。

<div class="result-value" markdown="1">

专用ARC4-Encoder在Mistral上的六任务平均分为46.5，在Llama3.1上的平均分为48.0；相应open-book平均分分别为49.2和47.4。也就是说，ARC在Mistral上接近但未达到完整上下文，在Llama3.1上平均分略高于open-book，并分别优于表中最佳非ARC压缩基线平均分41.4和40.6。作者据此主张，冻结解码器可以从4倍压缩的连续表示中恢复有效任务信息。

</div>

这说明ARC在统一5-shot协议下实现了较好的信息保留，特别是在SQuAD等依赖文档内容的任务上优势明显。Llama3.1结果略超open-book不意味着压缩表示比原文普遍包含更多事实：压缩可能过滤噪声，且结果受微调任务分布、提示格式与截断方式影响；不同方法的参数量和实际压缩率也并不完全相等。

<div class="result-source" markdown="1">

来源：表1，Main comparison of ARC-Encoder and other models

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">ARC4-Encoder M 4× - 39.0 68.9 45.1 71.1 31.0 23.8 46.5
ARC4-Encoder L 4× - 39.7 70.1 46.9 74.0 33.7 23.7 48.0</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 一个编码器同时适配Mistral 7B与Llama3.1 8B：训练时交替采样解码器，并为每个解码器配置独立投影器和任务令牌。

<div class="result-value" markdown="1">

共享ARC4-Encoder在Mistral和Llama3.1上的平均分分别为45.6和47.5，对应专用版本为46.5和48.0，差距分别为0.9和0.5分；每增加一个解码器只需增加约15M个专用参数。该结果支持作者关于单个编码器可跨多个解码器复用的主张。

</div>

共享主干几乎保持了专用模型的平均性能，表明压缩器学到的主体表示具有一定可移植性，而小型投影器负责匹配不同解码器的隐藏空间。不过这里只联合训练了两个结构和规模相近的解码器，且都与Llama系编码器存在一定架构关联，不能据此推断可无损扩展到任意数量或任意家族的模型。

<div class="result-source" markdown="1">

来源：第4.2节“Encoder adaptation to multi-decoder”；数值见表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">We report results in Tab. 1, showing that on average, the common encoder, ARC-Encoder⊗, loses less than 1.0 point compared to its specialized counterparts.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 长上下文扩展：ARC8-Encoder把最多32k原始词元压缩为约4k连续词元，送入未修改的Llama2 7B Chat，并与CEPED和Llama2-32k Instruct比较。

<div class="result-value" markdown="1">

ARC在NarrativeQA和QASPER上的F1分别为27.5和28.3，高于CEPED的20.5和19.7、Llama2-32k Instruct的14.2和16.4；但在GovReport和QM-Sum上的ROUGE-L仅为14.1和19.1，低于Llama2-32k Instruct在GovReport上的17.8，也低于原始Llama2 Chat在QM-Sum上的19.8。结果体现出问答能力显著提升，但摘要收益不稳定。

</div>

8倍压缩使原本只有4k窗口的冻结解码器可以接收32k原始上下文，并在两项长文问答上取得最强结果，说明外部压缩器可以承担任务特定的窗口扩展。然而摘要任务没有同步改善，作者将其解释为合成微调数据与GovReport、QM-Sum分布不匹配；因此实验支持“面向匹配任务的数据驱动扩展”，而非通用长上下文理解已经解决。

<div class="result-source" markdown="1">

来源：表3，Long-context evaluation on long-context benchmarks

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Models Max. Tokens NQA Qspr GvRp QM-Sum
Llama2 Chat 4k 16.1 17.2 15.7 19.8
+ CEPED 2k+30k 20.5 19.7 12.7 19.7
Llama2-32k Instruct 32k 14.2 16.4 17.8 17.6
ARC8-Encoder + Llama2 Chat 4k (32k//8) 27.5 28.3 14.1 19.1</span>

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

- closed-book与open-book界定性能上下界：前者不给文档，只测解码器参数记忆；后者输入未压缩文档，测完整上下文可达到的参考性能。ARC超过closed-book才能说明压缩表示确实携带信息，接近open-book则说明压缩造成的信息损失较小。
- LLMLingua2是硬压缩基线，通过筛选离散文本词元缩短上下文；它与ARC的连续表示压缩形成直接对照，但其实际压缩率约为1.9至2.0倍，低于ARC常用的4倍或8倍。
- ICAE-like、xRAG-like与PISCO-like代表三类软压缩方案：记忆令牌、预计算检索嵌入，以及同时微调编码器和解码器。作者用相同解码器、微调数据和交错式5-shot格式重新实现，以减少协议差异；但这些是带修改的复现结果，不能直接等同于原论文报告值。
- 长上下文基线包括原始Llama2 7B Chat、通过位置插值和全模型微调得到的Llama2-32k Instruct，以及用并行编码器和新增交叉注意力连接解码器的CEPED。该对比测试ARC能否仅靠外部编码器扩展上下文，而不改变解码器参数或内部模块。

**实验想回答的问题**

- 在不微调、也不修改解码器架构的条件下，ARC-Encoder生成的连续压缩表示能否在问答、翻译、摘要等短上下文任务中保留足够信息，并在固定4倍或8倍压缩下优于硬压缩、记忆令牌和检索嵌入等方法？
- 同一压缩器能否服务多个冻结解码器、低成本适配新解码器，并把上下文窗口有限的Llama2 7B Chat扩展到最多32k原始输入；哪些预训练与微调设计是实现这些能力的关键？

**实验实现**

短上下文实验主要采用冻结的Mistral 7B或Llama3.1 8B基础模型作为解码器。ARC以Llama3.2 3B为骨干，移除最后两层并取消因果掩码；两层MLP先把3072维编码输出投影到2048维，再映射到解码器所需的4096维，推理时在每段压缩表示后加入<Cont>。默认训练整个编码器，包括嵌入矩阵，并使用AdamW；主模型在约2.6B个Common Crawl词元上预训练，再用不包含评测基准训练集的合成及监督任务混合微调。短上下文统一使用5-shot，以原始词元数除以压缩词元数定义池化因子。多解码器版本在训练每一步随机选择目标解码器，共享编码器但为每个解码器保留独立MLP和任务令牌。长上下文版本使用8倍池化和冻结的Llama2 7B Chat，把最多32个1024词元块并行编码后拼接其压缩表示，使32k原文对应约4k个送入解码器的压缩词元。消融实验为节省计算只预训练约2B词元，通常使用Mistral 7B和池化因子8，因此其绝对分数不应直接与2.6B词元主模型混为一谈。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 比较无预训练直接微调、预训练20k步和预训练80k步，以隔离预训练长度对编码器—解码器隐藏空间对齐的作用。 | 相对不做预训练、直接微调，20k步预训练使六项短上下文任务平均分约提升16分，80k步时提升约19分；作者同时指出若没有后续微调，翻译、阅读理解和摘要仍会大幅下降。因此预训练负责建立连续表示的基础对齐，任务微调负责教解码器如何在下游格式中使用这些表示，两者不能互相替代。 | 该消融直接反驳了“只靠下游微调即可学会压缩”的假设。早期预训练带来最大增益，继续训练仍有收益但边际变小。不过原文节选没有给出各训练步数对应的完整绝对分数表，也没有报告方差或多随机种子统计，因此只能确认作者报告的近似增量，不能判断差异的统计显著性。 | 第4.4节“Training objective”<br><span class="experiment-evidence">For example, after 20k pretraining steps, we observe an improvement of approximately +16 points on the average score, while after 80k steps, the improvement reaches +19 points, compared to directly fine-tuning without pretraining.</span> |
| 改变预训练批次中重建任务的占比：0%、20%、50%和100%，检验“重建文本”与“续写文本”两个目标是否需要组合。 | 重建占比为0%、20%、50%和100%时，平均分依次为39.8、41.6、41.5和37.5；20%取得最高分，比完全不重建高1.8分，比只做重建高4.1分。50%与20%几乎相同，说明适量重建即可，但完全取消续写目标损失最大。 | 重建目标帮助编码器和MLP先把压缩表示映射到解码器可理解的空间，续写目标则训练这些表示支持后续生成。两者混合优于单一目标，说明“能还原输入”与“能支持下游生成”不是同一能力。由于20%与50%只差0.1分且原文未给出误差条，不能断言20%严格优于50%，更稳妥的结论是中等重建比例表现最好。 | 表4，Impact of pretraining reconstruction ratio<br><span class="experiment-evidence">% Rec. Avg.
0% 39.8
20% 41.6
50% 41.5
100% 37.5</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Develops a continuous context-compression encoder that reduces LLM input representations and inference cost.; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`9d21f1ee222b0d052efa001762c2da7e0973ef669752c720f347d9a7a6bf7ae0`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
