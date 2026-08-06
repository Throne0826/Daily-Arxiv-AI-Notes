---
title: "[论文解读] Thinking with Anchors: Grounded and Efficient Document Reasoning"
description: "[arXiv 2608.04424][VLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.04424"
announcement_date: "2026-08-06"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T07:05:29.040074+00:00"
source_sha256: "24adfa6b18088be345d2f30663d36e370c4dc0571d195911730c8ab2ffee4af4"
tags:
  - "VLM Reasoning"
  - "多模态 VLM"
  - "LLM Reasoning"
  - "文档理解"
  - "视觉锚点"
  - "页面分解"
  - "视觉语言落地"
  - "区域语义标注"
  - "密集文档计数"
  - "可核验推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.04424</p>

# Thinking with Anchors: Grounded and Efficient Document Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Sichen Zhu, Yuchen Zhu, Wenzhuo Xu, Jason Kuen, Wanrong Zhu, Jing Shi, Xuan Shen, Quanyi Wang, Yiwei Wang, Yujun Cai, Bing Shuai, Qin Zhang, Yongxin Chen, Shilong Liu, Molei Tao, Jiuxiang Gu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> ZJU；Columbia University；real-world information exchange. Automating document understanding has motivated research on document</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04424v1) · [PDF 下载](https://arxiv.org/pdf/2608.04424v1) · **关键词** 文档理解, 视觉锚点, 页面分解, 视觉语言落地, 区域语义标注, 密集文档计数, 可核验推理<br>


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

文档理解旨在从海报、菜单、广告和信息图等页面中提取可供机器处理的信息。其基础能力包括光学字符识别、版面分析、目标检测与分割，但这些技术通常只回答“页面上有哪些区域、位于哪里”；实际应用还要求模型判断区域的语义角色及相互关系，例如把价格关联到正确商品、把图表连接到图例与标题，并用页面中的具体区域支撑答案。本文因此把文档理解设置为一种以视觉证据为中心的任务：模型不仅要输出最终判断，还要产生可定位、可赋予语义并可独立核验的中间证据。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**页面分解**

把完整文档页面拆分为文本块、图片、图表、装饰元素等区域，并用边界框或多边形描述其位置。它提供页面的结构化组成，但通常不充分说明各区域在具体语境中的作用。

</div>
<div class="concept-item" markdown="1">

**视觉锚点**

本文将文本块、视觉实体、语义标签、边界框和多边形掩码统一视为视觉锚点；一个锚点同时包含区域几何位置、语义角色、功能以及与其他区域的潜在关系。通俗地说，它是推理过程中能够被明确指向和检查的页面证据。

</div>
<div class="concept-item" markdown="1">

**视觉语言 grounding（视觉语言落地）**

它要求把语言中的实体或描述对应到图像中的具体区域，输出可包括区域名称、坐标或多边形轮廓。对于密集文档，模型既要正确理解语义，也要避免遗漏、错配和坐标格式错误。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是视觉结构多样、可能包含大量文字块与视觉实体的文档页面；监督信息继承自 ADOPD 2024 的页面元素标注，并增加人工清理的描述、实体语义标签以及与区域对应的思维链轨迹。模型需要完成三类相互衔接的能力：依据局部外观和整页上下文为区域赋予语义类型；统一生成文字区域、视觉实体及其边界框或多边形轮廓；在 DocCount 的密集计数场景中使用这些锚点形成可核验的推理证据。该设置假定页面区域可以被显式定位，并强调中间证据的空间精度和语义可解释性，而不只评价最终答案是否正确。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **ADOPD 2024**: ADOPD 2026 的直接数据基础；原数据集包含约 12 万张视觉多样的文档图像，覆盖 1000 多种文档类型，并提供页面分解标注。本文在其页面元素之上补充人工清理的描述、语义标签和锚点化思维链，使数据用途从区域定位扩展到有证据支撑的文档推理。
- **HoloCount**: 与本文的计数评测最直接相关：HoloCount 在自然图像上通过语义计数、分析计数和鲁棒性测试诊断多模态大模型，并主要使用最终计数的精确匹配准确率；本文派生的 DocCount 转向密集文档场景，同时暴露边界框、掩码和语义标签等中间锚点，以便分别核验感知与推理过程。

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

论文的方法核心不是训练一个单一的端到端模型，而是把文档页面中的文本块、视觉实体、语义标签、边界框和任意多边形统一表示为可复用的“视觉锚点”，再围绕这些锚点组织数据构建、模型监督与可验证推理。完整流程从 ADOPD 2024 已有人绘实体多边形和 OCR 文本块出发，先人工重写页面级描述，再结合整页上下文为每个区域赋予细粒度语义角色；随后使用视觉语言模型校验候选类别并由人工复核，最后生成引用具体区域的自然语言思维链，形成 ADOPD 2026 及其密集计数子基准 DocCount。这样，每个页面不仅提供“区域在哪里”和“区域是什么”，还提供“答案如何由这些区域得到”的监督。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 继承并统一页面几何锚点

将视觉实体多边形与 OCR 文本区域视为同一套页面分解结果，并以“几何形状、模态、语义角色”作为后续锚点的统一数据接口。多边形保留实例的真实边界，OCR 块则把转写文本与局部区域显式关联。

<div class="method-step__io" markdown="1">

**输入**：ADOPD 2024 中约 $120\mathrm{k}$ 个视觉多样文档页面，以及对应的人绘实体多边形、OCR 文本块位置和原始页面描述。<br>
**输出**：由视觉区域和文本区域共同组成的稠密页面锚点集合，其中每个实例至少具有可定位的几何表示和模态信息。

</div>

**直观理解**：可以把页面看成一张由许多带编号零件组成的图：这一阶段先确定每个零件在哪里，以及它属于文字还是视觉内容，但暂不假设模型已经理解它的用途。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 人工清洗页面描述与区域语义标注

标注者首先重写页面级描述，使其覆盖文档类型、视觉风格、显著内容和整体意图；随后在阅读整页后，为每个实体多边形或 OCR 块赋予语义角色。视觉区域还需判断前景或背景，并标为 photograph、illustration、brand logo、background image、chart、icon 或 color block 等角色；文本区域则标为 title、body text、header、footer 或 image caption 等功能。

<div class="method-step__io" markdown="1">

**输入**：页面图像、继承的几何锚点和原始页面描述。<br>
**输出**：人工清洗的页面级描述，以及采用 $30$ 类体系标注的区域级语义锚点；每个锚点形成“geometry + modality + semantic role”的结构化证据单元。

</div>

**直观理解**：仅知道一个框的位置并不能判断它是商标、照片还是背景装饰，因此标注者必须像阅读者一样先理解整页，再说明每个局部在页面中承担什么功能。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 长尾类别消歧与锚点质量控制

论文采用人在环中的迭代过程建立类别体系：从数据提出候选标签，在真实页面上应用，再经复审调整含混的类别边界；之后使用消歧规则和后处理检查控制标注一致性。在 DocCount 构建阶段，视觉语言模型先验证多边形掩码的类别标签，再由人工进行最终检查。

<div class="method-step__io" markdown="1">

**输入**：初步语义标签、页面上下文、前景或背景层级判断，以及标注过程中暴露出的歧义案例。<br>
**输出**：经过类别边界修订、规则检查和人工复核的语义多边形或文本锚点，以及适合构造下游问题的可靠类别集合。

</div>

**直观理解**：文档中的角色不是固定物体类别，例如同一图形可能是正文插图，也可能是背景装饰；这一阶段相当于先制定判例，再让自动检查和人工复核共同排除明显误标。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造锚点化思维链与 DocCount

依据 Thinking-with-Visual-Primitives 范式生成密集计数问题，使答案必须先定位所有相关语义区域，再对这些实例执行计数；思维链生成器为每个相关锚点编写自然语言推理，并将推理中的对象与具体多边形绑定。最终样本同时保存问题、Anchor-CoT、实例级空间证据和标量答案。

<div class="method-step__io" markdown="1">

**输入**：文档页面、人工语义类别、经过校验的实例多边形，以及从数据准备阶段选出的计数类别。<br>
**输出**：具有 $442$ 个评测样本的 DocCount：计数对象是语义定义的文档区域，每个参与答案的实例具有多边形定位，并配有显式的锚点化推理表示和最终计数。

</div>

**直观理解**：普通计数题只检查模型最后说了几；DocCount 还要求模型指出自己数了哪些区域，从而可以区分“看漏了对象”“认错了类别”和“最后算错了数”三类失败。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 自回归验证的推测解码接受准则

$$
p_{\mathrm{AR}}(t) \geq \tau \cdot \max_j p_{\mathrm{AR}}(j)
$$

**符号说明**

- $t$：多词元预测 drafter 提出的当前候选词元。
- $p_{\mathrm{AR}}(t)$：自回归验证器对候选词元 $t$ 给出的条件概率。
- $j$：验证器词表中的任意候选词元索引。
- $\max_j p_{\mathrm{AR}}(j)$：当前解码位置上自回归验证器能够给出的最大词元概率。
- $\tau$：接受阈值，用于连续调节输出忠实度与一次接受更多草稿词元所带来的潜在速度收益。

<div class="equation-explanation" markdown="1">

**直观理解**：只有当草稿词元的自回归概率达到当前最优词元概率的 $\tau$ 倍时才接受它。当 $\tau=1$ 时，只有与自回归最大概率选择一致的草稿才能通过，因此输出与标准自回归解码等价；降低 $\tau$ 会接受更多草稿，但可能破坏框或多边形坐标序列。<br>
**原文位置**：附录 A.10，公式 (3)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文主体是数据集与任务框架，所给章节没有定义一个用于联合优化 ADOPD 2026 全流程的中心损失函数。训练监督由清洗后的页面描述、区域级 $30$ 类语义标签、框或多边形序列以及 Anchor-CoT 构成，可分别支持语义分类、统一 grounding 和锚点化推理模型，但其具体损失权重与联合训练目标在所给原文中未明确报告。附录公式 (3) 也不是训练损失，而是推理时判断是否接受 drafter 词元的解码规则。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 统一视觉锚点表示**

该表示把 OCR 文本块、视觉实体、语义标签、轴对齐框和任意多边形放入共享的结构化输出空间。锚点的基本信息包括几何位置、区域模态和文档语义角色，因此检测、分割、区域分类及后续推理能够引用同一实例，而不再把框、掩码和标签作为互不关联的监督信号。

> 直观理解：它相当于给页面中的每个有意义区域建立一张统一身份证：位置说明“在哪”，模态说明“文字还是图像”，语义角色说明“在页面里做什么”。这样，下游答案可以直接指回证据，而不是只给出无法核对的一句话。

**2. Anchor-CoT 生成与校验**

DocCount 的问题被设计为必须对语义定义的区域进行实例级 grounding；类别先由视觉语言模型验证，再由人工检查，思维链生成器随后围绕已确认的多边形实例生成自然语言推理。所得 Anchor-CoT 与最终标量计数共同发布，使最终答案和中间空间证据均可独立评估。

> 直观理解：普通思维链可能写得流畅却没有真正看对区域；Anchor-CoT 把每一步所说的对象固定到多边形上，因此检查者可以逐个核对模型到底数了什么。

**3. 代理式候选分组与几何门控**

高召回检测器容易把一个人工意义上的文本块拆成多行或多项候选框。方法将每个候选框编号，让多模态代理输出形如 $[[1,2,3],[4],[5,6]]$ 的离散分组，再解析分组并执行几何约束下的合并；代理只决定候选编号之间的归属关系，不直接回归新坐标。

> 直观理解：让语言模型选择“哪些编号属于一组”比让它重新写精确坐标更稳定；几何门控随后检查被合并的框是否真的在空间上相容，减少把远距离区域错误拼接的问题。

**训练与推理**

数据和监督构建阶段先从 ADOPD 2024 继承人绘多边形与 OCR 区域，由人工重写整页描述并在完整页面上下文中标注每个实例的语义角色；类别体系通过人在环中的提出、试标、复审和消歧逐步确定。构造 DocCount 时，先选择适合计数的语义类别，由视觉语言模型检查多边形标签并交由人工复核，再让思维链生成器依据已经确认的区域生成 Anchor-CoT，最终保存可执行核验的实例证据和标量计数。论文使用该基准以 zero-shot 方式评估 $13$ 个先进视觉语言模型，而不是要求它们先在 DocCount 上训练。

在下游锚点整理中，RF-DETR-Large 一类并行检测器先提供高召回候选池；编号后的候选框及页面图像输入代理，代理分两轮推理并在最终行输出 JSON 分组，随后系统解析这些编号、合并同组框并施加几何门控。统一 grounding 的可选推测解码以多词元预测头作为低成本 drafter，每轮提出最多 $k$ 个词元，再执行一次自回归前向验证这些词元；符合公式 (3) 的连续前缀被接受，其余位置恢复可靠解码。$\tau=1$ 保持自回归等价，较小的 $\tau$ 则用潜在质量损失换取更长的接受序列。

**复现信息**

复现数据语义层时，关键条件是保留实例级任意多边形和区域关联 OCR，并让标注者在整页上下文下判断角色，不能只裁剪局部区域进行分类；论文采用 $30$ 类长尾体系，具体前景或背景定义、消歧规则、实例和类别分布位于附录 A.4。DocCount 的官方评测集合包含 $442$ 个文档页面样本，提供语义定义类别、实例多边形、Anchor-CoT 和最终计数；所给章节未明确报告其训练集划分或用于生成思维链的具体模型与提示参数。

代理分组的输入必须显示互异编号，输出约定为 JSON 列表的列表，并通过最终的几何 guard 后才执行合并。推测解码实验采用草稿长度 $k=6$；检测实验使用 $100$ 张图像的子集。附录结果表明，这个 $3\mathrm{B}$ 模型的草稿接受率仅约 $37\%$ 至 $50\%$，验证器额外前向计算抵消了大部分并行草稿收益，因此该机制是对速度与正确性的诊断性扩展，不能据此假定它在当前模型上优于普通自回归解码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ADOPD 2026：三个实验线程共用最终确定的8万/2万/2万训练、验证和测试划分，分别承担视觉锚点定位与实体级语义标注等评测。数据划分方法与类别平衡诊断位于附录A.1，但当前节选未给出页面数、区域数或类别分布，因此不能据此判断长尾类别的具体严重程度。
- DocCount：由ADOPD 2026派生的文档计数基准，用于零样本评估视觉语言模型是否能理解计数对象的定义、遵循标注策略，并扫描整页后输出精确数量。当前节选未报告其样本规模、题型构成及训练、验证、测试数量。
- Doc2Box与Doc2Mask：原文将二者分别作为边界框检测和掩码分割任务报告。它们用于检验模型能否把页面中的文本区域与视觉实体转化为可复用的空间锚点；当前节选没有说明二者是否作为独立数据集发布，故更准确地视为ADOPD 2026上的任务设置。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**AP及AP50/AP75**

AP衡量预测区域与真实区域在不同交并比阈值下的综合精确率；AP50和AP75分别在交并比阈值0.50和0.75处评估，后者对定位边界更严格。表3还列出按小、中、大目标划分的APS、APM和APL，但当前节选未给出其数值。 （越高越好，因为高值表示模型在控制误检的同时找回更多真实区域，并且预测边界与标注边界更加吻合。）

</div>
<div class="metric-item" markdown="1">

**mF1**

宏平均F1通常先对每个类别分别计算精确率与召回率的调和平均，再在类别间等权平均，因而比总体准确率更关注少数类。表3列出mF1，但当前节选没有明确其用于检测、分割还是标签评估，也未给出计算细节。 （越高越好，因为它表示各类别的精确率与召回率整体更均衡，尤其能减少高频类别掩盖长尾类别失败的情况。）

</div>
<div class="metric-item" markdown="1">

**Accuracy**

DocCount中的准确率衡量模型最终计数答案与标注答案完全一致的比例。它同时受目标识别、全页遍历、类别定义理解和标注策略遵循影响，因此不是纯粹的目标检测指标。 （越高越好，因为计数任务要求给出精确答案；少计或多计通常都会被判错。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### DocCount零样本文档计数的最佳评测条件

<div class="result-value" markdown="1">

最佳条件达到72.85%准确率；作者据此判断当前先进视觉语言模型仍难以稳定完成文档页面中的精确视觉枚举。

</div>

约四分之一以上样本仍未被精确回答，说明模型即使具备较强视觉问答能力，也可能漏扫区域、重复计数、混淆类别定义，或未遵循数据集的计数口径。该结果只说明最佳被测条件尚未解决DocCount，不能证明所有模型都低于这一水平，也不能单独区分错误究竟来自视觉感知还是计数策略。

<div class="result-source" markdown="1">

来源：第4节末尾Analysis；定性样例指向附录A.13

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The best condition reaches 72.85% accuracy, but the task remains far from solved (selected cases in A.13).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Doc2Box检测与Doc2Mask分割的主结果

<div class="result-value" markdown="1">

原文明确设置了零样本与微调条件，并比较专用检测器或分割器和VLM定位器，但当前节选中的表3结果行被截断，无法可靠报告优胜模型或数值差距。

</div>

该实验本应回答统一视觉语言定位是否能达到任务特化模型的空间精度，以及微调带来多大收益。由于缺少完整表格，不能从表头或摘要推断LocateAnything、YOLOv12-M或智能体细化的排名。

<div class="result-source" markdown="1">

来源：第4节Experiments；表3结果未完整提供

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

First, we evaluate document decomposition and detection, comparing specialized non-VLM detectors/segmenters with the VLM-based LocateAnything [wang2026locateanything] grounder and an agentic grouping refinement.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 实体级语义标注实验

<div class="result-value" markdown="1">

原文说明该线程要求把第3节定义的分类体系标签赋给已定位文档区域，但当前节选没有报告模型、指标或结果，因此无法判断整体性能及长尾类别表现。

</div>

这一实验把“区域在哪里”与“区域是什么”分开考查，可揭示定位正确但语义理解错误的情况。现有材料只能确认任务目标，不能支持任何模型优劣、类别难度或统计显著性结论。

<div class="result-source" markdown="1">

来源：第4节Experiments

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Second, we study entity-level semantic tagging, in which the goal is to assign taxonomy labels defined in Sec. 3 to localized document regions.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前来源节选截断了表3及后续实验内容，只能核实DocCount最佳准确率72.85%；Doc2Box、Doc2Mask、语义标注、基线排名和智能体细化收益均无法可靠复原。任何更具体的数值结论都需要核对论文完整表格。
- 节选未提供DocCount规模、类别分布、模型名单、提示协议、重复次数、置信区间或显著性检验。72.85%的单点最佳结果因此不足以判断模型间差异是否稳健，也不能把计数错误严格分解为感知错误与策略错误。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- YOLOv12-M：专用的非视觉语言边界框检测基线。它提供传统检测模型参照，用来判断统一视觉语言定位器的优势是否来自语言建模与统一输出能力，而非单纯的检测容量；当前节选只显示其名称，未保留完整结果行。
- LocateAnything：基于视觉语言模型的grounder，用于与专用检测器或分割器比较。该比较直接检验统一视觉语言接口能否同时处理文本区域、视觉实体及其空间坐标。
- 专用非VLM检测器与分割器：作为一组任务特化方法参与视觉锚点定位比较，代表分别优化检测或分割目标的传统路线。除YOLOv12-M外，当前节选未提供其余模型名称，因此不作补充。
- 智能体式分组细化：在基础定位结果上执行分组修正的比较条件，用于检验后处理推理能否改善区域组织。当前节选未说明智能体模型、工具、提示词或迭代规则，也没有保留对应数值。

**实验想回答的问题**

- 在统一的文档页面数据划分上，专用检测器或分割器与基于视觉语言模型的定位方法，分别能多准确地生成文本块和视觉实体的边界框或多边形掩码；智能体式分组细化是否能进一步改善视觉锚点定位？
- 模型能否依据局部外观与整页上下文为已定位区域赋予语义标签，并在零样本条件下按照数据集的标注规则完成密集、精确的文档元素计数？

**实验实现**

实验采用同一套8万/2万/2万训练、验证、测试划分，沿三条线程展开：第一条评估Doc2Box检测和Doc2Mask分割，并比较零样本与微调条件、专用非VLM模型、LocateAnything以及智能体式分组细化；第二条在已经定位的文档区域上预测第3节定义的实体级语义标签；第三条在DocCount上测试视觉语言模型的零样本精确计数能力。表3的列设计表明定位实验报告AP、AP50、AP75、不同目标尺度AP和mF1，但当前节选没有保留完整模型结果、训练超参数、输入分辨率、解码方式、随机种子或重复实验信息。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 作者将DocCount的选定成功或失败案例放在附录A.13，并据类别分析概括出两类潜在失败来源：页面感知不足，以及对类别定义或标注政策执行不一致。当前节选没有包含具体页面、模型回答和真实标签，因而这一解释应视为作者的定性归因，尚不能据此量化两类错误各占多少。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：构建以视觉锚点为基础的文档视觉语言推理任务，联合区域语义、空间关系与结构理解。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`24adfa6b18088be345d2f30663d36e370c4dc0571d195911730c8ab2ffee4af4`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
