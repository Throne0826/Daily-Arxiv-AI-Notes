---
title: "[论文解读] Slow to See, Slow to Suppress: Understanding the Effects of Modality in Context-Memory Conflicts"
description: "[arXiv 2609.00293][LLM 机制与可解释性] 本文研究视觉语言模型在上下文信息与参数记忆冲突时是否会因实体呈现模态不同而作出不同选择，并将视觉实体更易触发参数化答案的现象解释为跨模态表征对齐较晚、未能及时抑制事实回忆机制。"
arxiv_id: "2609.00293"
announcement_date: "2026-09-02"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:49:15.928390+00:00"
source_sha256: "01ea44debc034b59e0bfe7ee9c37e9551f7a4b80ce406a7b76b3c8b8ca1f88f7"
tags:
  - "LLM 机制与可解释性"
  - "多模态 VLM"
  - "LLM Reasoning"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2609.00293</p>

# Slow to See, Slow to Suppress: Understanding the Effects of Modality in Context-Memory Conflicts

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Athulith Paraselli, Etha Tianze Hua, Ellie Pavlick</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Brown University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00293v1) · [PDF 下载](https://arxiv.org/pdf/2609.00293v1) · **关键词** LLM 机制与可解释性<br>


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

本文研究视觉语言模型在上下文信息与参数记忆冲突时是否会因实体呈现模态不同而作出不同选择，并将视觉实体更易触发参数化答案的现象解释为跨模态表征对齐较晚、未能及时抑制事实回忆机制。

**不用术语来说**：当检索系统向模型提供一条比训练记忆更新或更可靠的信息时，模型本应依据这条上下文作答；但如果问题中的对象以图片而非文字出现，模型可能仍回答训练期间记住的旧事实。换言之，同一个对象只是换了一种呈现方式，模型对外部信息的信任程度就可能改变，这会降低多模态检索增强系统的可靠性与一致性。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者构建了一个受控的冲突事实检索数据集，包含三个领域的约 $37\mathrm{K}$ 个实例，用于比较同一实体以文本或图像出现时，视觉语言模型在上下文知识与参数知识之间的选择差异。
- 作者不仅记录了视觉实体更偏向参数知识的模态不对称，还提出并通过因果干预支持一种机制解释：文本实体可在早期层被解析，使注意力及时抑制负责参数事实提取的多层感知机；视觉实体的表征较晚才充分解析，因此这种抑制未能及时发生。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于视觉语言模型（VLM）与多模态知识检索的交叉领域。VLM 接收文本和图像，并根据这些输入生成答案；其参数中还保存了训练阶段学到的事实知识。论文关注二者发生冲突时的情形：上下文提供了一个与模型参数记忆不同的事实，而系统本应优先使用更具体、更新或更可靠的上下文信息。该问题直接关系到多模态检索增强生成（RAG）和工具调用系统的可靠性，因为这些系统可能同时向模型提供文本证据、图像证据以及模型内部已有的知识。理解这一问题需要区分“上下文知识”和“参数知识”，并进一步考察实体识别、知识检索及答案生成在不同模态下的时间关系。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉语言模型（VLM）**

VLM 是能够共同处理图像与文本的模型，例如根据图片中的人物或建筑回答相关事实问题。本文特别比较实体以文字出现和以图像出现时，模型如何选择信息来源。

</div>
<div class="concept-item" markdown="1">

**上下文知识与参数知识冲突**

上下文知识是当前输入中临时提供的信息，参数知识是模型在训练过程中写入其参数的长期记忆。当二者对同一实体给出不同事实时，模型需要判断应采信哪一个；本文称之为 context-memory conflict。

</div>
<div class="concept-item" markdown="1">

**多模态检索增强生成（RAG）**

RAG 先从外部来源检索资料，再把资料放入模型上下文，使模型能够利用比参数记忆更新或更具体的信息。本文用混合文本和图像的受控事实检索任务模拟这种多模态 RAG 场景。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文构造一个受控的事实检索任务：给定实体、与该实体有关的关系问题，以及一段与模型已知事实相矛盾的上下文信息；该上下文可以用文本呈现实体，也可以用图像呈现实体。模型需要输出与上下文一致的答案，而不是继续输出其参数中保存的原始事实。数据覆盖名人、建筑和艺术品三个领域，共 $37{,}970$ 个实体—矛盾上下文对；每个样本都将实体与一个否定或改变其已知事实的陈述配对。核心比较保持事实内容和任务形式尽量一致，仅改变实体在上下文中的呈现模态，从而测量文本实体和视觉实体在上下文知识、参数知识之间的选择差异。论文还考察增加图像上下文数量和加入链式思维提示是否会改变这种选择。最终输出是模型针对关系问题生成的事实答案，分析重点是答案更接近上下文提供的事实，还是模型参数中原有的事实。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$VLM$**

视觉语言模型，即同时处理图像与文本并生成答案的模型。

</div>
<div class="notation-item" markdown="1">

**$D_{\mathrm{conflict}}$**

本文的矛盾事实检索数据集；其包含实体、关系问题以及与参数知识相冲突的上下文。

</div>
<div class="notation-item" markdown="1">

**$K_{\mathrm{ctx}}$**

上下文知识，即当前输入的文本或图像所提供的事实信息。

</div>
<div class="notation-item" markdown="1">

**$K_{\mathrm{param}}$**

参数知识，即模型训练后储存在参数中的事实记忆。

</div>

</div>

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

检索增强生成与工具调用常把模型权重之外的当前、任务相关或更可信信息放入上下文，现代系统又越来越多地检索图片等非文本材料。如果视觉语言模型面对冲突时因模态不同而选择不同知识来源，那么即使检索结果正确，系统也可能忽略图像所指实体的上下文事实，继续输出参数权重中储存的旧信息，从而破坏知识更新的一致性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **语言模型中的上下文—参数知识冲突研究**：既有工作通过设置上下文事实与模型训练记忆不一致的任务，观察模型倾向调用哪一种知识；其中既包括用于定位参数回忆与上下文采用机制的简化实验，也包括更接近实际问答场景的偏置测量。
- **检索增强生成与多模态工具调用**：这类系统在推理时向模型补充外部检索内容，使模型能够使用权重中缺失、过时或不可靠的信息；随着系统扩展到多模态，补充内容及其所指实体可能同时来自文本和图像。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有冲突研究主要面向大型语言模型和文本信息，尚不足以说明当上下文或被询问实体跨越文本与视觉模态时，模型能否以相同方式识别并解决冲突；因此，文本场景中得到的知识采用规律不能直接用于判断多模态系统的可靠性。
- 仅测量最终答案偏好无法解释模态差异产生在何处，也无法区分它究竟源于一般性的图像理解困难，还是源于视觉实体解析较慢而错过对参数事实回忆的抑制；缺少机制解释会使提示设计或模型干预难以对准真正原因。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未系统回答两个相互关联的问题：同一实体以文字或图像呈现时，视觉语言模型解决上下文—参数记忆冲突的行为是否一致；若不一致，这种差异能否由模型内部的实体解析时序、注意力活动与多层感知机中的参数事实提取之间的因果关系解释。

</div>
<div markdown="1"><span>核心问题</span>

视觉语言模型在上下文事实与参数记忆冲突时，是否会因为被询问实体采用文本或视觉形式而改变知识来源偏好；如果视觉实体更容易引出参数化答案，那么较晚完成的视觉实体表征对齐是否导致模型未能及时抑制早期层中的参数事实回忆？

</div>
<div markdown="1"><span>作者直觉</span>

模型要采用冲突的上下文事实，必须先认出问题所指实体与上下文中的实体是同一个对象，随后才能阻止惯常的参数记忆被提取。文字名称在早期层便较容易对应起来，因此注意力可以及时发出“上下文发生冲突”的信号并压低后续参数回忆；图片所代表的对象需要更长的处理过程，等其身份表征充分形成时，参数事实可能已经被早期多层感知机推动。由此，比较两种模态并把晚层已解析的视觉表征回填到早层，可以直接检验“看得慢，所以抑制得慢”这一解释。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该研究不提出新的模型训练算法，而是以现成视觉语言模型为对象，构造“上下文信息与参数记忆冲突”的测试，并比较文本实体和视觉实体在冲突中的行为。给定一个实体的查询图像、与参数记忆相矛盾的上下文事实以及问题提示，模型需要在上下文事实和训练中存储的事实之间作答；研究通过标准提示、思维链提示和视觉上下文替换，观察参数化答案率及其跨模态差异。直观地说，作者测试模型在“眼前证据”和“脑中旧知识”不一致时更相信哪一方，并进一步检查让两种模态的实体表示更接近是否能改变这一选择。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造上下文—记忆冲突样本

为同一实体提供与模型通常事实知识相冲突的上下文，并按照实体模态划分文本实体条件和视觉实体条件。

<div class="method-step__io" markdown="1">

**输入**：包含实体查询、与参数记忆不同的上下文事实和待回答问题的数据样本；实体分别以文本或图像形式呈现。<br>
**输出**：可比较的文本实体与视觉实体冲突测试实例，以及模型最终回答所属的上下文答案或参数答案标签。

</div>

**直观理解**：相当于告诉模型“某建筑位于东京”，但模型训练中记得它位于巴黎，然后观察模型相信新提示还是旧知识。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 运行标准上下文提示

分别以文本实体和视觉实体作为查询对象运行模型，记录其回答，并计算参数化答案率；该指标表示模型仍回答训练中事实的比例。

<div class="method-step__io" markdown="1">

**输入**：冲突测试实例、待测视觉语言模型和标准文本上下文模板。<br>
**输出**：不同实体模态下的基线参数化答案率及其模态差异。

</div>

**直观理解**：这一步建立“未经额外干预时模型偏向哪一类信息”的参照线，便于判断后续提示是否真正缩小差距。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 测试思维链提示

要求模型先进行逐步推理再给出答案，并比较文本实体与视觉实体的参数化答案率相对于基线的变化及模态差异。

<div class="method-step__io" markdown="1">

**输入**：同一批冲突实例、视觉语言模型和附录所述的思维链提示模板。<br>
**输出**：思维链条件下的参数化答案率、相对基线变化和视觉减文本的模态差异。

</div>

**直观理解**：作者检验“让模型多想几步”能否先把图像中的实体认出来，再像处理文字一样解决冲突；结果显示这种做法跨模型并不稳定。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 测试视觉上下文替换

把原本描述实体的文本上下文替换为图像，并使用“图中实体位于某处”等提示；视觉条件进一步比较上下文图像与查询图像完全相同、或属于同一实体但图像不同的情况。

<div class="method-step__io" markdown="1">

**输入**：建筑位置和名人职业数据集中的冲突实例、实体查询图像，以及同一实体的相同图像或不同图像。<br>
**输出**：视觉上下文条件下各实体模态的参数化答案率及相对于文本上下文基线的变化。

</div>

**直观理解**：如果上下文和问题使用几乎同一张图，模型更容易认出它们指的是同一个对象；若只是同一对象的另一张照片，这种对应关系会变弱。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告新的训练目标或参数优化过程。该章节采用提示级、黑盒式干预，在推理时改变上下文形式或提示模板；因此不存在需要通过梯度下降优化的研究方法目标。文中提到的“参数化答案率”和模态差异是评测统计量，而不是训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 上下文—参数记忆冲突评测**

评测核心是比较模型在矛盾条件下输出上下文事实和参数化事实的比例，并按实体呈现模态分组。研究关注视觉实体相对于文本实体是否保留更高的参数化答案率。

> 直观理解：该模块不是训练模型，而是把“新证据”和“旧知识”故意设置成相反答案，再统计模型站在哪一边。

**2. 思维链提示干预**

思维链提示要求模型在最终回答前进行显式逐步推理；研究将其作为黑盒干预，比较其对文本和视觉条件参数化答案率的影响，而不改变模型内部参数。

> 直观理解：它相当于要求模型先写出推理过程，但实验目的不是提高一般推理能力，而是检查显式思考能否弥补视觉实体处理较慢或较晚的问题。

**3. 视觉上下文与表示对齐干预**

研究将文本上下文替换为实体图像，并区分查询图像与上下文图像完全相同、以及二者不同但属于同一实体的条件。作者据此检验查询表示与上下文表示的早期对齐是否影响对参数记忆的抑制。

> 直观理解：当问题中的图和上下文中的图完全一致时，模型更容易把两者连起来；换一张同一对象的图后，这种连接不再可靠。

**训练与推理**

研究阶段不对视觉语言模型进行训练或微调，而是在推理阶段输入预先构造的上下文—记忆冲突样本。首先运行标准文本上下文条件，得到文本实体和视觉实体的基线参数化答案率；随后分别加入思维链提示，或将文本上下文替换为相同实体的相同图像、不同图像，并重新记录答案。每个回答被归类为上下文答案或参数化答案，跨样本聚合后比较不同条件下的参数化答案率及视觉条件减文本条件的模态差异。摘录还指出，作者在附录中对多层感知机抑制的中介作用进行了因果验证，但未提供该验证的具体操作流程。

**复现信息**

为保证视觉上下文实验能够比较多张图像，研究仅使用建筑位置和名人职业数据集；历史艺术品数据集因难以为独特作品获取多张图像而被排除。实验比较同一图像和同一实体的不同图像两种视觉上下文，并以相应模态的标准文本上下文结果作为基线；具体模型规模、提示模板全文、样本数量、解码设置和参数化答案判定规则在所供章节摘录中未完整给出，原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Celebrity：包含2,856组冲突事实对，主要来自MMKC-bench，并以Wikimedia Commons的图像和事实补充。实体为名人，关系分为职业、出生年份和国籍；该子集测试人脸或人物图像条件下的上下文—记忆冲突，其中部分职业可能从服饰或场景直接推断。
- Building：包含16,230组冲突事实对，图像来自Google Landmarks Dataset v2，关系为所在国家、建成年份和建筑师。该子集用于检验模态差异能否推广到地标识别，以及答案通常不能仅凭局部视觉线索直接读出的关系。
- Artwork：包含18,884组来自Wikimedia Commons的冲突事实对，关系为艺术家和当前位置。它提供了与人物、建筑不同的视觉实体类型，并重点检验模型识别作品后调用作者等参数知识的行为。上述三个原始子集经过逐模型筛选：仅保留模型在无冲突条件下既能识别实体、又能正确回忆参数事实的样本；每个模型最终均有超过1,000组有效样本，因此不同模型实际接受评测的样本集合可能不同。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**参数答案报告率**

在上下文给出反事实答案而参数记忆支持通常事实时，模型最终输出参数事实的样本百分比。它直接刻画模型在冲突中偏向参数记忆还是检索上下文。 （该指标没有普遍意义上的越高越好；在应遵循所提供上下文的检索增强设定中，较低通常表示更能采用上下文，但本文主要将其作为行为偏好指标而非总体准确率。）

</div>
<div class="metric-item" markdown="1">

**模态差值**

定义为视觉条件参数答案报告率减去文本条件参数答案报告率，即$\Delta=\mathrm{Vision}-\mathrm{Text}$；正值表示图像实体比文本实体更容易触发参数答案。表2同时给出该差值的95% bootstrap置信区间。 （不存在单向优劣；接近零表示两种模态处理冲突较一致，显著正值则支持论文所称的视觉参数偏置。）

</div>
<div class="metric-item" markdown="1">

**答案偏好边际**

机制实验采用论文公式1定义的边际衡量参数答案相对上下文答案的偏好；正值偏向参数答案，负值偏向上下文答案。给定节选未提供公式1的具体表达式，因此不能进一步还原其计算方式。 （取决于实验目的：消融后向负方向移动表示被消融组件原本促进参数答案；向正方向移动则表示该组件可能促进上下文答案。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨模型与关系的总体模态比较

<div class="result-value" markdown="1">

表2显示，多数模型—关系组合的$\Delta$为正，尤其是职业、建筑所在国家和艺术家姓名等关系；作者据此主张，文本实体通常更易采用冲突上下文，而视觉实体更易报告参数答案。不过该规律并非无例外：部分关系接近零或出现负值，Gemma-3-27B在艺术家姓名上即为$-6.43$个百分点，95%置信区间为$[-9.76,-3.33]$。

</div>

同一个对象若写出名字，模型较容易让检索文本覆盖原有知识；若只给图片，模型在识别对象后更常回到训练中记住的事实。该结果支持“模态造成不对称偏好”，但不能说明视觉条件在每个模型、每种关系上都必然更参数化，也不能仅凭行为差值证明作者提出的内部机制。

<div class="result-source" markdown="1">

来源：表2，Gemma-3-27B—Artwork—Artist name行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Gemma-3-27B
Artwork
Artist name
13.10
6.67
-6.43 (-9.76, -3.33)

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Ministral-3-8B在艺术家姓名关系上的视觉—文本冲突

<div class="result-value" markdown="1">

Ministral-3-8B的文本实体条件参数答案报告率为25.93%，视觉实体条件为74.54%，视觉条件高出48.61个百分点，95%置信区间为$[42.13,55.10]$。这是表2中最明显的正向模态差异之一。

</div>

当问题要求回答作品作者时，只把作品名称换成作品图像，就使该模型从多数时候遵循上下文转为多数时候输出记忆中的作者。这说明差异不只是人物职业可从画面直接猜测造成的；但它仍只是特定模型和关系上的强效应，不能单独代表所有模型的平均表现。

<div class="result-source" markdown="1">

来源：表2，Ministral-3-8B—Artwork—Artist name行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Ministral-3-8B
Artwork
Artist name
25.93
74.54
+48.61 (42.13, 55.10)

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Gemma-3-12B在建筑所在国家关系上的视觉—文本冲突

<div class="result-value" markdown="1">

Gemma-3-12B在文本实体条件下仅有2.23%的参数答案报告率，而视觉实体条件达到83.04%，差值为80.80个百分点，95%置信区间为$[75.45,85.71]$，构成节选表格中极强的模态反转。

</div>

面对同一条冲突检索文本，写出建筑名称时模型几乎总采用上下文，给出建筑图片时却大多输出参数记忆中的国家。该结果表明视觉输入并非简单地增加噪声，而可能改变冲突解决路径；不过它没有排除模型架构、视觉编码质量或提示敏感性等其他解释，机制判断仍依赖后续干预实验。

<div class="result-source" markdown="1">

来源：表2，Gemma-3-12B—Building—Country loc.行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Gemma-3-12B
Building
Country loc.
2.23
83.04
+80.80 (75.45, 85.71)

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评测先筛除模型无法在无冲突条件下识别实体或回忆事实的样本，这提高了冲突测量的内部有效性，却使结论只适用于模型已经掌握的实体—事实对；而且筛选按模型分别进行，各模型结果不一定基于完全相同的样本，跨模型数值不宜直接视为严格同集排名。
- 提供的节选没有完整报告总体汇总统计、显著性检验规则、公式1的具体定义、解码配置及所有机制实验的数值结果。MLP消融、注意力遮蔽和激活回填支持作者的“视觉解析较晚、抑制较迟”解释，但这些干预可能同时扰动实体识别或一般计算，因而尚不能把观察到的模态差异唯一归因于该机制。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 文本实体条件：提示中的实体以名称出现，而检索式冲突上下文仍为文本。它是最关键的对照，因为除实体模态外，提示结构、问题和反事实上下文均保持一致；视觉—文本差值因而主要衡量实体呈现模态的影响。
- 视觉实体条件：以实体图像替代名称，其他提示组成不变。它既是主要实验条件，也与文本条件形成配对比较，用于判断视觉识别过程是否提高参数答案报告率。
- 无冲突事实回忆条件：不提供与参数记忆矛盾的上下文，用于确认模型确实可以识别实体并回忆目标事实。该条件主要承担数据过滤和行为校准作用，避免把“不认识实体”误判为冲突处理偏好。
- 跨模型族比较：实验覆盖Gemma-3-12B/27B、Qwen2.5-VL-7B/32B/72B和Ministral-3-8B/14B。不同规模和架构不是传统意义上的单一方法基线，而是用于检验模态差异是否只属于某个模型或参数规模。

**实验想回答的问题**

- 在检索文本与模型参数记忆冲突时，仅改变实体的呈现模态——文本名称或图像——是否会系统性改变视觉语言模型选择参数答案的概率？这种差异是否跨模型、领域与事实关系成立？
- 如果视觉条件更偏向参数答案，这一现象能否由“视觉实体解析较晚，因而上下文对参数知识调用的抑制来得太迟”解释？相关的多层感知机消融、注意力遮蔽与激活回填实验是否支持该机制，而非仅反映可从图像直接猜出答案？

**实验实现**

所有样本采用统一的检索增强生成式提示结构：[提供的文本上下文] + [文本名称或实体图像] + [事实问题]。冲突上下文始终保持为文本，以模拟常见的文本检索增强系统，并通过只替换实体模态构造较对称的因果比较。上下文给出合理但反事实的答案，模型参数记忆则预计包含通常事实。评测前按模型分别执行无冲突验证，只保留能正确识别实体并回忆参数事实的项目。行为实验报告各关系的参数答案百分比、视觉减文本的差值及95% bootstrap置信区间。机制实验进一步对实体位置对应的MLP跨层窗口进行消融，并使用注意力遮蔽和后层视觉激活回填；窗口实验测试1、3、5、8层跨度，视觉实体位置定义为图像patch token，文本实体位置则覆盖完整名称及“The artwork titled…”等上下文化token。节选仅报告窗口实验使用2张NVIDIA RTX A5000、每种窗口约运行24小时；解码参数、随机种子及bootstrap次数原文节选未明确报告。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 改变实体位置MLP消融窗口跨度：1、3、5和8层 | 作者报告5层和8层窗口在两种模态上产生最明显的行为移动；随着窗口扩大，视觉实体位置的MLP对最终参数信号更必要，而文本实体位置MLP的作用明显较弱。较小窗口在Gemma视觉条件中反而轻微推向参数答案，暗示局部MLP窗口可能促进冲突上下文。 | 该实验隔离“实体token上的MLP计算是否负责注入参数事实”。如果删除视觉实体位置的一段MLP后偏好转向上下文，说明这些MLP原本在帮助视觉实体调用参数知识。窗口越大效应越清楚，也表明机制可能分布在连续多层而非某个单层；但扩大窗口同时增加了干预范围，因此更强变化不等于已精确定位唯一因果层。 | 附录B，图9<br><span class="experiment-evidence">Our findings (shown in Figure
9
) show the most apparent shifts for either modality with window sizes of 5 and 8.</span> |
| 在模态差异很小的名人出生年份关系上重复MLP消融 | 消融两种模态的MLP均未使行为转向上下文答案。作者据此推测，出生年份可能没有通过同一种MLP参数促进机制编码，或者模型本身对该关系表现不佳、未形成稳定的参数知识调用。 | 这是一个重要的负对照：若所提MLP机制无论关系如何都会出现，它可能只是普遍的消融副作用；出生年份没有同样移动，说明机制与发生明显模态分歧的关系更相关。不过“没有移动”不能证明出生年份完全不存储于MLP中，也可能来自样本量、测量灵敏度或较弱的原始行为信号。 | 附录E，图17<br><span class="experiment-evidence">In Figure
17
we observe that ablating the MLPs in both modalities do not result in a shift towards the contextual answer, which implies that these MLPs likely do not result in parametric promotion.</span> |

**定性案例**

- 名人职业可能存在视觉捷径：例如LeBron James身穿篮球球衣时，模型可直接推断其为篮球运动员，而未必先识别身份再检索参数知识。作者因此把MLP消融、注意力遮蔽和激活回填结果按三个数据域拆分；Building与Artwork较难仅凭局部线索推断目标关系，却总体呈现与Celebrity相似的趋势。Gemma的Celebrity子集显示少量额外抑制，可能对应其较小的模态差异，但作者认为其幅度远小于文本条件，不足以改变总体结论。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The study analyzes internal cross-modal alignment and recall suppression mechanisms underlying VLM behavior during context-memory conflicts.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`01ea44debc034b59e0bfe7ee9c37e9551f7a4b80ce406a7b76b3c8b8ca1f88f7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
