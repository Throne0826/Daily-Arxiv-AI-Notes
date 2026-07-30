---
title: "[论文解读] Localizing Persona Representations in LLMs"
description: "[arXiv 2505.24539][LLM 机制与可解释性] 本文研究大型语言模型在内部表示空间中如何编码不同人格、价值观与信念，并定位这些表征主要在哪些解码器层形成可辨别的差异。"
arxiv_id: "2505.24539"
announcement_date: "2026-07-29"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:24.099871+00:00"
source_sha256: "5b7268cd524f099bd2c789bb04b50e8096445d5c4464ac1613b0c920671c2052"
tags:
  - "LLM 机制与可解释性"
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "LLM 其他"
  - "大语言模型可解释性"
  - "人格设定"
  - "内部表示"
  - "层激活"
  - "表示空间"
  - "主成分分析"
  - "政治信念"
  - "伦理价值"
  - "大五人格"
  - "仅解码器式 Transformer"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2505.24539</p>

# Localizing Persona Representations in LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-29</span>
<span><strong>作者</strong> Celia Cintas, Miriam Rateike, Erik Miehling, Elizabeth Daly, Skyler Speakman</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2505.24539v4) · [PDF 下载](https://arxiv.org/pdf/2505.24539v4) · **关键词** 大语言模型可解释性, 人格设定, 内部表示, 层激活, 表示空间, 主成分分析, 政治信念, 伦理价值, 大五人格, 仅解码器式 Transformer  


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

本文研究大型语言模型在内部表示空间中如何编码不同人格、价值观与信念，并定位这些表征主要在哪些解码器层形成可辨别的差异。

**不用术语来说**：当用户要求语言模型扮演具有特定性格、道德立场或政治观念的人时，模型会生成相应回答，但只观察最终文本无法判断模型内部究竟在何处形成了这种角色差异，也无法知道不同角色是被清楚区分，还是共享了容易混淆的内部表示。本文试图打开这一“黑箱”，比较模型逐层处理相同类型角色提示时产生的内部激活。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出一套逐层分析流程，结合降维与模式识别方法，定位不同人格表征分歧最明显的模型层，而不只依据最终生成文本判断角色是否生效。
- 在选定层的激活空间中比较不同角色的共享区域与独特区域，用于分析哪些人格、价值观或信念在模型内部容易重叠，哪些更容易分离。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型可解释性研究，关注仅解码器式 Transformer 如何在内部表示空间中编码“人格设定”（persona）。这里的人格设定不是单指日常意义上的性格，而是对一个假想个体的人类特征、价值观或信念的自然语言描述，例如政治上的自由主义或保守主义、伦理上的功利主义或义务论，以及大五人格中的宜人性或尽责性。此类设定通常通过“假设你是一个……”形式的提示影响模型的语气、判断与推理；由于大语言模型从大规模且基本未经筛选的文本中学习，其潜在政治倾向、道德偏好及人格相关行为并非由显式规则定义，因此仅观察最终回答不足以说明模型在何处、以何种内部结构表达这些属性。本文据此把研究对象从输出行为转向逐层激活表示，分析不同人格陈述在模型内部是否可分，以及不同人格是否依赖共享或相对独特的激活位置。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**人格设定（persona）**

指用自然语言刻画的假想个体身份、人格特征、价值观或信念，例如“高度宜人”或“信奉功利主义”。它作为输入语境，可引导模型采用相应立场、语气或行为方式生成文本。

</div>
<div class="conceptitem" markdown="1">

**层激活表示（layer activation representation）**

输入经过 Transformer 某一层后会形成一组数值向量，概括模型在该层对输入信息的内部处理结果。本文将这些激活向量视为人格信息可能被编码的表示空间，而不是把模型输出文本直接当作内部机制的证据。

</div>
<div class="conceptitem" markdown="1">

**主成分分析（PCA）**

PCA 是一种线性降维方法，用少数彼此正交的方向保留数据中尽可能多的方差。本文借此比较匹配与不匹配某个人格的陈述在各层表示中能否沿主要变化方向分开。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是公开的人格陈述集合，其中陈述分别表现出与某个人格相匹配或不匹配的行为，覆盖政治、伦理和主要人格特质三类主题；这些陈述被送入多个预训练的指令微调、仅解码器式大语言模型，包括 Llama3-8B-Instruct、Granite-7B-Instruct 和 Mistral-7B-Instruct。研究从各模型的不同层提取激活向量，并回答两个定位问题：Q1 比较各层中人格相关表示的方差与可分性，以确定人格信号最强的层；Q2 在选定层内识别显著激活位置，再比较不同人格对应集合的独有部分与交集，以刻画共享和差异化编码。输出不是一个新的人格分类器，而是关于人格信息“位于哪些层”以及“不同人格在激活空间中如何重叠或分离”的解释性分析；其基本假设是，匹配与不匹配陈述之间稳定的表示差异能够作为模型编码相应人格信息的代理信号，而非对因果机制的直接证明。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Perez et al. (2023)**: 为本文提供公开的模型生成人格集合，并将人格相关的人类特征、价值观和信念作为研究对象；本文在该资源上选择政治、伦理和主要人格特质三类陈述进行内部表示分析。
- **Cheng et al. (2023), Marked personas: using natural language prompts to measure stereotypes in language models**: 研究通过自然语言人格提示测量语言模型中的刻板印象，说明人格设定可能改变可观察输出；本文进一步追问这些人格信息在模型内部的层级与激活空间中如何编码。
- **Zou et al. (2023)**: 属于理解和定位模型内部概念或行为表示的相关研究，构成本文研究“人格表示在哪里编码”的可解释性背景；所给原文节选未进一步明确其具体方法及与本文技术路线的差异。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

人格提示与个性化生成已被用于对话代理、价值对齐、道德判断和面向不同人群的交互，但模型输出可能同时携带偏见、刻板印象或不一致的价值取向。若不知道这些特征在网络内部何时形成、彼此如何组织，就很难判断人格调控是否真正改变了模型表示，也难以设计更精确的检查、编辑或安全干预方法。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于提示与输出的行为评测**：通过人格、人口属性、政治立场或道德情境提示引导模型，再依据回答内容、问卷得分或决策倾向评估其人格和价值表现。此类方法能够测量外显行为，但分析对象主要是最终输出。
- **逐层探针与隐藏表示检查**：从Transformer不同层提取隐藏状态，再使用分类器、表示替换或其他探针技术，判断某类上下文知识、行为属性或价值信息在哪些层可以被读取。其基本思想是：如果某层激活能够稳定区分目标属性，该层就包含与该属性有关的信息。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 仅依据生成结果进行人格评测，无法定位差异产生于哪一层，也不能区分模型是形成了稳定的内部角色表示，还是只在输出阶段模仿了相关措辞；这限制了机制解释和针对性干预。
- 已有隐藏表示研究覆盖上下文知识、行为或价值编码，但从所给材料无法确认其是否系统比较了多种人格维度在所有解码器层中的相对分离程度，因此尚不足以回答人格差异在网络深度上的具体分布。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作与本文之间的关键缺口，是缺少一个跨层且跨人格类别的内部表示分析：既要确定人格信息在哪些层才明显分化，也要在信息最强的层中进一步刻画不同人格表征的重叠和分离关系，并检验这种现象能否在多个预训练仅解码器模型中复现。

</div>
<div markdown="1"><span>核心问题</span>

对于由不同人类特征、价值观和信念定义的角色，预训练仅解码器大型语言模型在什么层、以何种相对空间结构编码它们；不同角色的内部激活是彼此分离，还是存在系统性的共享与多义性？

</div>
<div markdown="1"><span>作者直觉</span>

Transformer逐层把提示转换成预测下一个词所需的表示，因此人格线索未必从早期层开始就形成清晰类别：前层可能主要处理词语和局部语境，后层才把分散的描述整合成影响回答的高层立场。逐层比较角色间的激活差异，可以先找到这种整合最明显的位置；再观察该层的表示空间，就能把“哪些角色容易被模型混在一起、哪些角色被清楚区分”转化为可分析的几何关系。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法是一套不更新模型参数的内部表征定位流程，目标分为两级：第一级回答人格表征主要在模型的哪些层出现，第二级进一步寻找选定层内对特定人格最关键的激活维度。输入是14个人格维度的陈述数据，每个维度包含300条高置信度的 matchingbehavior 陈述和300条 notmatchingbehavior 陈述；研究对象为Llama3-8B-Instruct、Granite-7B-Instruct和Mistral-7B-Instruct三个32层、仅解码器式指令模型。每条陈述经模型单次前向传播后，作者在每一层只保留最后一个词元对应的4096维激活向量，将其作为对整句信息的摘要表示。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建并筛选人格陈述集合

从人格、伦理理论和政治观点三类主题中选取14个人格维度；每个维度仅保留置信度不低于0.85的样本，并分别抽取至少300条matchingbehavior与300条notmatchingbehavior陈述，形成每个维度600条样本的平衡数据集。

<div class="method-step__io" markdown="1">

**输入**：Perez et al. (2023)生成的人格陈述、matchingbehavior或notmatchingbehavior标签，以及模型生成的标签置信度。  
**输出**：14个二组对照的人格数据集，每个数据集包含600条陈述。

</div>

**直观理解**：这里的正组表示某种行为或观点确实出现，负组只表示该行为未出现，并不自动代表相反人格；因此该任务是在比较“具有某特征”和“不具有该特征”的表征，而不是测量一条连续的两极人格轴。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行模型前向传播并提取逐层表征

使用Hugging Face聊天模板把每条陈述放入system角色，分别送入三个模型进行一次前向传播；对每个模型的32层，提取句子最后一个词元的隐藏激活，不生成回答，也不进行多轮前向传播。

<div class="method-step__io" markdown="1">

**输入**：筛选后的人格陈述，以及Llama3-8B-Instruct、Granite-7B-Instruct和Mistral-7B-Instruct。  
**输出**：对每个模型、人格维度、标签组和网络层得到一组4096维句子表征，其中matchingbehavior表征记为e^{+}，notmatchingbehavior表征记为e^{-}。

</div>

**直观理解**：可以把每一层看成模型理解句子的一个处理阶段，最后词元的向量则被当作模型读完整句后留下的摘要；逐层保存摘要，就能观察人格信号在网络深度上的变化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在联合主成分空间中比较两组表征

在联合集合e^{+}\cup e^{-}上计算主成分分析，将两组向量投影到同一个低维主成分空间，分别得到q^{+}与q^{-}；随后把二者视为两个已知标签的簇，计算多种聚类距离或分离度指标。

<div class="method-step__io" markdown="1">

**输入**：某一模型、某一人格维度和某一层上的两组高维向量e^{+}与e^{-}。  
**输出**：该人格维度在该层上的多项组间差异分数，以及可用于跨层比较的低维表示。

</div>

**直观理解**：主成分分析先保留高维激活中变化最大的方向，再在同一坐标系里比较正负两组；若两组在某层明显分开，说明该层更强地编码了与该人格有关的信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 跨层定位最强人格信号

沿网络深度比较各项指标，识别matchingbehavior与notmatchingbehavior表征差异最明显的层，并用多种度量进行交叉验证，以回答人格信号主要出现在哪里。

<div class="method-step__io" markdown="1">

**输入**：每个模型中14个人格维度在32层上的聚类距离和分离度结果。  
**输出**：每个模型和人格维度的强表征层候选，供第二级激活定位分析使用。

</div>

**直观理解**：这一步不是寻找单个句子的异常点，而是在问哪一层最稳定地把具有某人格特征的句子与不具有该特征的句子区分开；多种指标一致时，层定位结论更不依赖某一种几何尺度。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该研究不是训练或微调一种新模型，也没有通过损失函数优化人格分类器；三个预训练指令模型的参数保持不变，作者对前向传播产生的隐藏激活进行PCA、距离计算和模式分析。论文提到指令模型本身曾由各自发布者通过监督微调、RLHF或其他对齐流程训练，但这些不是本文的优化目标，也不属于本文实验中的训练步骤。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 带标签的人格陈述数据模块**

研究使用模型生成的persona数据，覆盖五个大五人格维度、五种伦理理论和四种政治观点。标签表示陈述是否体现目标人格行为，置信度阈值为0.85；每个维度的两类样本各300条，但notmatchingbehavior不等价于另一个已指定人格的matchingbehavior，不同数据集之间也可能存在语句或语义重叠。

> 直观理解：该数据提供了一组受控对照，但标签的含义是“目标特征是否出现”，不是“两个相反人格中的哪一个”；忽略这一点会把层间差异错误解释成保守与自由、外向与内向等严格对立轴。

**2. 逐层最后词元激活提取模块**

三个模型均为32层的decoder-only指令模型，每层最后词元的激活形状为(1,4096)。作者选择最后词元，是基于它在自回归注意力中能够汇集此前词元信息的假设；同一句陈述只做一次前向传播，研究分析隐藏状态而非生成文本。

> 直观理解：该模块把原本只能从输出观察的人格行为转化为可逐层检查的数值向量，从而区分“模型最终说了什么”和“模型内部在哪一阶段形成了可分辨的人格信号”。

**3. PCA联合降维与簇分离模块**

对每一层和每一人格维度，PCA在e^{+}\cup e^{-}上联合拟合，保证q^{+}与q^{-}处于同一主成分坐标系；随后将两组视作两个簇并计算若干聚类距离与评分。原文脚注报告所分析主成分的解释方差比例在14个维度上为0.657至0.898，但当前摘录没有给出保留主成分数、全部指标定义及聚合规则。

> 直观理解：联合拟合很关键：若正负样本各自建立坐标系，两组位置就不能直接比较。聚类分数在这里不是发现未知类别，而是量化已知两组隐藏表示分得有多开。

**4. 两级人格定位模块**

Level 1按层比较matchingbehavior与notmatchingbehavior的表征差异，回答Q1；Level 2在选定层内寻找相较其他人格更关键的激活并比较共享或独特子空间，回答Q2。当前材料完整描述了Level 1的输入和PCA比较框架，但Level 2的算法正文以及Deep Scan等可能相关组件仅在引文索引中出现，不能仅凭索引补全。

> 直观理解：两级设计把“在哪一层”与“该层里的哪些坐标”分开处理，避免直接在所有层、所有神经元中同时搜索；不过第二级细节缺失意味着当前摘录只能支持方法框架，不能支持端到端复现。

**训练与推理**

整个研究属于离线推理与事后表征分析。对每个人格维度，先把matchingbehavior和notmatchingbehavior陈述分别输入模型；输入通过自定义聊天模板被格式化为system消息，然后仅执行一次完整前向传播。作者不要求模型生成回答，而是从全部32层读取最后词元的隐藏状态，因此一条陈述在一个模型上产生32个4096维向量。随后以“模型×人格维度×层”为分析单位，在正负样本的联合激活上拟合PCA并投影得到q^{+}和q^{-}，通过聚类距离与分离度随层变化的曲线识别人格信号最强的层。选层后进入层内激活定位和跨人格重叠分析，但当前摘录未给出其完整计算流程，故原文未明确报告可复现的第二级推理步骤。

**复现信息**

公平解释该方法所必需的设置包括：14个人格数据集分别为agreeableness、conscientiousness、openness、extraversion、neuroticism，virtue ethics、cultural relativism、deontology、utilitarianism、moral nihilism，以及politically conservative、politically liberal、anti-immigration、anti-LGBTQ-rights；每个数据集使用置信度至少0.85的600条样本，正负各300条。模型为Llama3-8B-Instruct、Granite-7B-Instruct和Mistral-7B-Instruct，均有32层，抽取的最后词元向量维度为4096。输入通过Hugging Face的apply_chat_template处理，并设置为system角色；论文特别说明不进行多次前向传播。PCA必须在正负样本联合集合上拟合，否则无法保持两组投影坐标的一致性。当前材料没有完整列出所有聚类指标、主成分保留数量、层选择或多指标聚合准则、随机种子、批量大小、数值精度，以及层内关键激活的具体筛选算法，这些内容均应记为原文未明确报告，而不能从摘要结论反推。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- 人格句子集合：包含14个人格维度，每个维度均有 matchingbehavior（正例）和 notmatchingbehavior（负例）句子。它用于逐层比较 q_+ 与 q_- 的表示分离度，并验证显著激活能否检测某句是否符合指定人格。原文节选未明确报告数据集名称、每类样本量及训练/验证划分。
- Personality（人格特质）主题：涵盖宜人性、尽责性、开放性、外向性和神经质等维度，用于考察五类人格特质的正负句表示分离，以及同主题人格之间显著激活的共享与独有程度。
- Ethics（伦理理论）主题：涵盖道德相对主义、道德虚无主义、功利主义、德性伦理和义务论等人格，用于检验概念相近的伦理立场是否共用较多内部激活。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**Silhouette Score（SH，轮廓系数）**

同时衡量 q_+ 与 q_- 各自的簇内紧密程度和两簇之间的分离程度；值越大，样本越接近本簇而远离另一簇。 （越高越好，因为更高值表示两类表示更紧凑且更易区分。）

</div>
<div class="metricitem" markdown="1">

**Calinski-Harabasz Score（CH）**

比较簇间离散度与簇内离散度，用来判断正负人格表示是否形成清楚而紧凑的两组。 （越高越好，因为较大的簇间差异和较小的簇内差异会提高该值。）

</div>
<div class="metricitem" markdown="1">

**Euclidean Distance（ED，欧氏距离）**

测量 PCA 空间中 q_+ 与 q_- 凸包中心之间的直线距离，直接反映两组表示中心相隔多远。 （越高越好，因为中心距离越大通常表示正负人格表示越容易分开，但它本身不衡量簇内紧密性。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Q1：三个模型的逐层 q_+／q_- 表示比较

<div class="result-value" markdown="1">

三个模型的最大欧氏中心距离均出现在较晚的第20—31层；作者据此认为人格表示主要在解码器最后约三分之一逐渐形成明显区分，而不是在浅层就稳定分离。

</div>

浅层更可能保留通用词汇和局部句法信息，深层才把整句加工成与人格判断相关的上下文表示。该结果说明“哪里最容易读出人格差异”，但不能单凭相关性证明这些层中的激活对模型生成人格化回答具有因果作用。

<div class="result-source" markdown="1">

来源：Results，Q1 Results；Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Across the models, the largest distances are found in the later layers (20–31).</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Q1：Llama3-8B-Instruct 的 Layer 1 与 Layer 31 对比

<div class="result-value" markdown="1">

最终层在全部列出的人格维度上普遍呈现更高SH、CH和ED以及更低DB。例如开放性从 Layer 1 的 SH=0.602、CH=570.2、ED=0.414、DB=0.645，提升或改善为 Layer 31 的 SH=0.795、CH=3564.1、ED=27.60、DB=0.319。综合比较后，作者选择 Llama3 最终层进行激活定位。

</div>

多个性质不同的指标方向一致，说明结果不只是由某一个距离定义造成：最终层既把正负两组推得更远，也使组内结构相对更紧凑。不过，这一结论主要支持所测句子上的表示可分性，不等于 Llama3 在所有人格任务或生成质量上优于其他模型。

<div class="result-source" markdown="1">

来源：Results，Q1 Results；Table 1、Appendix Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Most measures indicate that the final layer of Llama3 achieves the strongest separation.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Q2 Level 2：利用最终层显著激活检测每个人格的 matchingbehavior 句子

<div class="result-value" markdown="1">

14个人格均获得较高检测性能：精确率范围约为0.778（nihil）至0.999（consc），召回率范围约为0.76（neuro）至0.998（agree）。这验证了 Deep Scan 找到的 O_{S^*} 确实包含可用于区分指定人格正负句的信息。

</div>

显著激活不是只在可视化上看起来不同，而能在独立随机测试句上支持分类。最低值仍明显低于接近完美的人格，表明不同人格的可检测难度并不一致；同时，高分类性能只能说明这些位置携带信息，不能证明每个位置只编码一个人格。

<div class="result-source" markdown="1">

来源：Results，Q2 Results；Table 2，Level 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">We find high precision and recall for all 14 personas, with the precision ranging from 0.778 (nihil) to 0.999 (consc) and recall from 0.76 (neuro) to 0.998 (agree).</span>

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

- 早期层对照（Layer 1）：与最终层 Layer 31 使用相同句子和评价指标，直接检验人格信息是否已经在浅层形成，而不是把任意层的可分性都解释成人格编码。
- notmatchingbehavior 负例 q_-：作为每个人格 matchingbehavior 正例 q_+ 的语义行为对照，用于判断表示或激活能否区分“符合”与“不符合”指定人格的句子。
- 跨模型比较：实验比较 Llama3、Granite-7B-Instruct 和 Mistral-7B-Instruct 的逐层表示，以判断后层分离趋势是否仅属于单一模型；节选只给出了 Llama3-8B-Instruct 的完整数值表。
- Level 1、Level 0 与 Level 2 粒度对照：Level 2 区分同一人格的正负句，Level 1 区分同一主题中的单个人格与其余人格，Level 0 区分一个主题与其他主题。该对照检验显著激活在细粒度人格、主题内人格和主题级别上的有效性。

**实验想回答的问题**

- Q1：在不同预训练解码器式大语言模型及其不同层中，哪些位置最能区分符合某一人格特征的句子（matchingbehavior，记为 q_+）与不符合该特征的句子（notmatchingbehavior，记为 q_-）？
- Q2：在区分能力最强的层内，是否存在稳定的人格相关显著激活子集；不同人格、同一主题内的人格以及不同主题之间，这些激活位置是彼此独有还是发生重叠？

**实验实现**

实验提取每个输入句子在每一解码层的最后一个 token 表示，并对 q_+、q_- 表示做 PCA；随后以轮廓系数、CH、DB、欧氏中心距离等指标比较各层分离度。层编号从简单输入层0到最终层31。跨模型结果显示后部层最可分，因此后续定位集中于 Llama3 最后一层的4096维激活。作者使用 Deep Scan 多次搜索最能指示目标人格的激活集合 O_{S^*}，再利用对应样本集合 X_{S^*} 计算检测精确率和召回率。表2报告100次独立 Deep Scan 运行和200个随机测试样本的均值±标准差；PCA与聚类结果通常按5个随机种子平均。最后通过集合交、并及 Upset 图统计显著激活在人格内、人格间和主题间的重叠。原文节选未明确报告提示模板、句子总数、PCA保留维数之外的全部超参数或统计显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 层位置消融式对照：Llama3 Layer 1 与 Layer 31 的显著激活检测 | 以 agree 为例，Layer 1 的精确率／召回率为0.5067±0.1432／0.2469±0.0904，而 Layer 31 为0.9971±0.0113／0.9979±0.00984；consc 从0.3895±0.1753／0.2237±0.10208提高到0.9992±0.0001／0.95454±0.04876；open 从0.6048±0.2317／0.2434±0.10216提高到0.9998±0.0003／0.97727±0.0422。 | 该对照隔离了网络深度的作用：相同模型中，浅层找到的激活集合几乎不能完整召回人格匹配句，而最终层集合接近完美。它有力支持“人格可读出信息集中于后层”，但并非真正删除某层或某激活后的因果消融。 | Appendix C，Table 4；Persona Representations Across Layers in Other Models<br><span class="experiment-evidence">In Tab. 4, we observe low precision and recall in early layers.</span> |
| 检测粒度对照：Level 0 主题级与 Level 1 同主题具体人格级 | Level 0 三个主题的精确率／召回率分别为 Politics 0.8850±0.2070／0.9511±0.0433、Ethics 0.9958±0.0103／0.8420±0.0541、Personality 0.9799±0.0258／0.8682±0.0701；Level 1 多个人格的精确率下降到约0.42—0.63，尽管部分召回率仍较高。 | 这一对照隔离了类别粒度：主题级共有模式容易定位，但主题内部的细分人格更加重叠。高召回而低精确率表示目标人格样本常被找出，但许多同主题的其他人格也被误判为目标，因而不能把主题共有激活误称为人格专属激活。 | Results，What Are the Activation Interactions Between Groups of Personas?；Table 2<br><span class="experiment-evidence">In contrast, our results are mixed at inter-persona Level 1.</span> |
| 主题激活与具体人格激活的交集分析：Level 0 对 Level 2 | Politics 与政治人格 consc 的显著激活重叠25%，Personality 与人格 extra 重叠21%，Ethics 与伦理人格 virtue 重叠20%。 | 该分析隔离了具体人格表示中有多少位置同时携带上位主题信息。约五分之一至四分之一的重叠说明人格表示部分继承主题模式，但其余激活并非简单等同于主题标签；由于只展示每个主题的一个样例，不能推广为所有人格的平均规律。 | Results，What Are the Activation Interactions Between Groups of Personas?；Figure 4<br><span class="experiment-evidence">We observe an overlap of 25% of the salient activations between Politics and political persona consc.</span> |

**定性案例**

- 移民（immi）人格的 PCA 可视化显示：初始层中 q_+ 与 q_- 大量重叠，随层数加深逐渐分开，并在 Llama3 最终层最清楚。该个例直观展示了后层形成判别性表示的过程，但主要结论仍需依赖跨人格、跨模型的定量指标，而不能只看二维或三维投影。
- 伦理人格案例显示，道德虚无主义与功利主义等立场共享较多显著激活；与之相比，政治人格具有更多独有激活。作者将前者解释为更强的多义性，并指出这可能使精细人格控制需要额外的表示解耦策略。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：reused verified category during targeted regeneration
- 全文指纹：`5b7268cd524f099bd2c789bb04b50e8096445d5c4464ac1613b0c920671c2052`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
