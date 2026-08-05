---
title: "[论文解读] CURV: Enhancing Chart Understanding Through Curriculum Visual Grounded Reasoning"
description: "[arXiv 2608.02833][VLM Reasoning] 本文针对图表问答中“推理过程与视觉证据脱节”的问题，提出课程学习框架 CURV，使多模态大语言模型逐步学会在每一步推理时动态关注相关图表区域，从而形成内在的视觉扎根推理能力。"
arxiv_id: "2608.02833"
announcement_date: "2026-08-05"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:37:55.436105+00:00"
source_sha256: "a7f327f1af1fc40eb38b0c80dd0da3f81216028a87762f3e4065c009037df6b3"
tags:
  - "VLM Reasoning"
  - "LLM 其他"
  - "LLM Reasoning"
  - "图表问答"
  - "多模态大语言模型"
  - "视觉落地推理"
  - "课程学习"
  - "思维链"
  - "动态视觉注意"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.02833</p>

# CURV: Enhancing Chart Understanding Through Curriculum Visual Grounded Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Xuehang Guo, Pingyue Zhang, Ruiyi Zhang, Zhenhailong Wang, Hanrui Lyu, Heng Ji, Tong Sun, Qingyun Wang, Manling Li</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.02833v1) · [PDF 下载](https://arxiv.org/pdf/2608.02833v1) · **关键词** 图表问答, 多模态大语言模型, 视觉落地推理, 课程学习, 思维链, 动态视觉注意<br>
**代码**: [https://xhguo7.github.io/CURV/](https://xhguo7.github.io/CURV/) · **项目页**: [https://xhguo7.github.io/CURV/](https://xhguo7.github.io/CURV/)

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

本文针对图表问答中“推理过程与视觉证据脱节”的问题，提出课程学习框架 CURV，使多模态大语言模型逐步学会在每一步推理时动态关注相关图表区域，从而形成内在的视觉扎根推理能力。

**不用术语来说**：回答复杂图表问题不仅要看清数值、图例和空间关系，还要把这些信息按正确顺序组合起来；现有模型即使能够写出看似合理的分析步骤，也可能看错数据、关注错误区域，或者让后续结论脱离先前看到的证据，因此在图中已有足够信息时仍会答错。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 CURV，将图表问答改写为多步视觉扎根推理，并通过从单操作到复杂嵌套推理的课程学习，使模型逐步内化“分解问题—定位证据—组合结论”的能力，而非依赖测试时的外部提示。
- 提出可扩展的合成数据生成方法并构建三层课程数据集 CCQA，以不同图表类型、推理模式和视觉扎根策略支持由浅入深的训练与多层次评估。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

图表问答（Chart Question Answering, CQA）是多模态推理任务：模型需要联合读取图表图像与自然语言问题，从柱、线、图例、坐标轴和数值标注等视觉元素中定位证据，再执行比较、聚合或多步计算并生成答案。本文关注的核心并非仅让多模态大语言模型输出正确结果，而是使其形成内在的视觉落地推理能力：把复杂问题分解为连续步骤，并在每一步随推理目标动态关注相应图表区域，使视觉证据、逻辑操作与最终结论保持一致。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多模态大语言模型（MLLM）**

能够同时处理图像和文本并生成语言答案的模型。在本文场景中，它接收图表与问题，需要兼顾视觉读取和逻辑推理。

</div>
<div class="concept-item" markdown="1">

**视觉落地（Visual Grounding）**

把语言中的对象或某一步推理与图像中的具体区域对应起来，例如将“2023 年的销售额”定位到正确柱形及其数值。视觉落地错误会使后续计算即使逻辑正确也得到错误答案。

</div>
<div class="concept-item" markdown="1">

**课程学习（Curriculum Learning）**

按照由易到难的顺序组织训练任务，使模型先掌握基础能力，再学习这些能力的复杂组合。CURV从单操作推理逐步过渡到多操作、嵌套及多图表组合任务。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一幅或多幅图表图像及其自然语言问题，模型需要识别相关图表元素和定量关系，将问题分解为多步推理，并在各步骤中动态聚焦支持该步骤的视觉区域；输出是由连贯推理链支持的最终答案。该设定假定答案所需信息存在于视觉输入中，但模型必须解决三个相互关联的问题：正确分解复杂问题、让每一步推理落地到恰当区域，以及把跨步骤的视觉证据与逻辑操作组合成一致结论。论文以CQA为主要训练和评测场景，同时考察这种内在能力能否迁移到真实世界图表及域外多模态推理任务。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Chain-of-Thought（CoT）推理**: 已有CoT方法通过显式提示将复杂问题拆成逐步推断，但本文指出，单纯的外部推理提示不能保证每一步都读取了正确的视觉证据；CURV试图把逐步推理及其视觉对齐内化为模型能力。
- **显式视觉提示与视觉引导方法**: 已有方法利用外部视觉线索帮助模型关注目标区域，可以改善多模态推理表现；本文转而研究无需持续依赖外部辅助的动态视觉落地，使注意区域随推理步骤变化。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

图表问答要求模型同时理解几何结构、空间关系与定量模式，并在多步计算或比较过程中不断切换到相关图表区域。视觉感知一旦出错，或中间推理未绑定到正确证据，错误就会沿推理链累积，最终造成答案不可靠。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **外部思维链提示**：在推理时显式要求模型把复杂问题拆成连续的中间步骤，以改善逻辑组织并减少直接作答造成的推断跳跃。
- **外部视觉提示或视觉引导**：通过额外标记、提示或指定关注区域，帮助模型定位图表中与当前问题相关的数值、线条或其他视觉元素。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有模型缺乏稳定的问题分解能力，中间步骤可能前后不一致或存在逻辑错误；即使生成了思维链，也不代表该推理链是连贯且正确的。
- 逻辑推理与视觉定位通常没有在每一步紧密耦合，模型可能误读数值、关注错误区域，或无法把跨步骤取得的视觉证据组合起来，导致感知、推理和结论彼此脱节。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有外部思维链和视觉线索能够辅助作答，但尚未解决如何把这种辅助转化为模型自身可持续执行的能力：模型需要在没有额外支持时，自主分解复杂问题，并让每个推理步骤动态对应到正确的图表区域，最后将这些有视觉依据的步骤组合成一致结论。

</div>
<div markdown="1"><span>核心问题</span>

能否通过由简单到复杂的课程训练，让多模态大语言模型内化多步视觉扎根推理，从而在每一步协调逻辑操作与动态视觉关注，并将这种能力泛化到真实图表及域外多模态任务？

</div>
<div markdown="1"><span>作者直觉</span>

若直接训练复杂的多图表、嵌套推理任务，模型必须同时学习看清图表、拆解问题和组合多步结论，容易混淆错误来源。CURV 先让模型掌握单一操作及其对应证据，再逐步增加操作数量和组合复杂度，相当于先学会“每一步该看哪里、做什么”，再学习把这些步骤串联起来；动态移动视觉关注还可使中间判断始终受到图中证据约束。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CURV将图表问答从直接映射$(I,Q)\rightarrow A$改写为带动态视觉定位的多步推理：模型不只输出最终答案$A$，还在第$t$步生成自然语言推理$R_t$及其对应的图表区域$V_t$，并把该区域转换为新的视觉状态$I_t$，供下一步推理使用。训练采用两阶段课程：阶段I先学习“某一步推理应看哪里”，阶段II再联合学习推理、视觉定位和答案预测；数据难度则沿图表视觉复杂度与推理深度$D$逐级增加。

直观地说，普通模型像是看完整张图后一次性猜答案；CURV要求模型写出解题步骤，并在每一步指出当前依据位于图中的什么位置。被指出的区域随后成为下一步的视觉提示，使注意位置能够随逻辑进展而改变，而不是依赖外部人工框选或仅生成与图像证据脱节的文本思维链。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造课程化视觉推理监督

CCQA把每个问题分解为$T$个推理步骤，并为第$t$步配对推理文本$R_t^*$、真实视觉区域$V_t^*$与二值掩码$M_t^*$；样本按照推理深度$D$、图表复杂度和操作复杂度组成三层课程与五个细粒度难度层级。模板实例化覆盖原子操作及嵌套操作，使训练目标可以从简单的单操作逐步过渡到复杂组合推理。

<div class="method-step__io" markdown="1">

**输入**：七类合成图表、模板化问题及其绘图数据；每张基础图表可派生多个问题实例。<br>
**输出**：监督样本包含图像$I$、问题$Q$、逐步推理与视觉定位序列$\{(R_t^*,V_t^*,M_t^*)\}_{t=1}^{T}$以及答案$A^*$。

</div>

**直观理解**：这一步相当于把只有最终答案的练习题改造成带分步解答和逐步图中标注的教材。课程排序让模型先学会识别基础图表元素，再处理需要嵌套计算或跨图组合的信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 阶段I：推理条件下的视觉定位

模型$f_\theta^{(S1)}$在给定当前推理语义和历史上下文后预测视觉焦点$V_t$，并用定位损失$L_V(V_t,V_t^*)$逐步监督。该阶段主要建立文本推理与图表空间区域之间的对应关系，而不是直接优化完整解题过程。

<div class="method-step__io" markdown="1">

**输入**：图表$I$、问题$Q$、当前真实推理步骤$R_t$以及此前的推理—定位对$\{(R_{t'},V_{t'})\}_{t'=1}^{t-1}$。<br>
**输出**：能够依据某一步推理内容，在图表中预测相应证据区域的视觉定位能力。

</div>

**直观理解**：模型先练习“读到这句话时应该看图中的哪里”。历史定位也作为上下文，可以减少连续步骤间关注对象不一致的问题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 将视觉焦点转换为可反馈的视觉状态

CURV通过applied、boxed或cropped三种策略把$V_t$映射为视觉状态$I_t$：它们分别以视觉提示作用于原图、用框标示目标区域，或裁剪目标区域；原文节选未进一步给出三者的像素级实现。该设计允许定位结果作为新的图像输入，而不只是作为文本坐标留在输出中。

<div class="method-step__io" markdown="1">

**输入**：原图$I$与第$t$步预测的视觉焦点$V_t$。<br>
**输出**：突出当前证据的视觉状态$I_t$，用于条件化后续推理步骤。

</div>

**直观理解**：这类似于解题时用高亮、画框或局部放大标出当前需要看的部分。下一步不必重新在整张复杂图表中搜索全部信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 阶段II：交错生成推理与动态定位

模型$f_\theta^{(S2)}$在每一步联合生成$(R_t,V_t)$，把$V_t$转换为$I_t$后反馈给下一步，并最终预测答案$A$。训练联合使用逐步推理损失、视觉定位损失和答案损失，使逻辑链、图像证据及最终任务目标共同约束参数$\theta$。

<div class="method-step__io" markdown="1">

**输入**：原始图表$I$、问题$Q$，以及此前的推理和视觉反馈历史$\{R_{t'},V_{t'}\rightarrow I_{t'}\}_{t'=1}^{t-1}$。<br>
**输出**：结构化视觉推理链$\{(R_t,V_t)\}_{t=1}^{T}$和最终答案$A$。

</div>

**直观理解**：模型形成“推理一句—在图上找证据—带着该证据继续推理”的循环。最终答案既要符合推理链，也应建立在逐步定位到的图像区域上。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 多步视觉定位推理的任务重构

$$
f_\theta:(I,Q)\rightarrow\{(R_1,V_1),(R_2,V_2),\ldots,(R_T,V_T)\}\rightarrow A
$$

**符号说明**

- $f_\theta$：参数为θ的多模态大语言模型。
- $I\in\mathbb{R}^{H\times W\times C}$：高度为H、宽度为W、通道数为C的输入图表图像。
- $Q$：关于图表的自然语言问题。
- $R_t$：第t步的自然语言推理内容。
- $V_t$：在图像空间中支撑第t步推理的视觉区域或视觉焦点。
- $T$：得到最终答案所使用的推理步骤总数。
- $A$：模型生成的最终答案。

<div class="equation-explanation" markdown="1">

**直观理解**：该式用可监督的中间链替代直接的$(I,Q)\rightarrow A$映射。核心不是单纯增加文本思维链，而是要求每个$R_t$都有对应的视觉证据$V_t$，从结构上减少推理与图像脱节。<br>
**原文位置**：第3.1节，公式(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 阶段II联合训练目标

$$
\mathcal{L}^{(S2)}=\sum_{t=1}^{T}\lambda_R\mathcal{L}_R(R_t,R_t^*)+\lambda_V\sum_{t=1}^{T}\mathcal{L}_V(V_t,V_t^*)+\lambda_A\mathcal{L}_A(A,A^*)
$$

**符号说明**

- $\mathcal{L}^{(S2)}$：阶段II需要最小化的总训练损失。
- $\mathcal{L}_R(R_t,R_t^*)$：第t步预测推理$R_t$与真实推理$R_t^*$之间的推理监督损失。
- $\mathcal{L}_V(V_t,V_t^*)$：第t步预测视觉焦点$V_t$与真实视觉焦点$V_t^*$之间的定位损失。
- $\mathcal{L}_A(A,A^*)$：预测答案A与真实答案A^*之间的答案损失。
- $\lambda_R,\lambda_V,\lambda_A$：分别控制推理、视觉定位和答案监督相对权重的系数。
- $R_t^*,V_t^*,A^*$：数据提供的第t步真实推理、真实视觉焦点和最终真实答案。
- $T$：该样本的推理步骤总数。

<div class="equation-explanation" markdown="1">

**直观理解**：总目标同时惩罚“推理步骤写错”“证据区域找错”和“最终答案答错”。这样即使答案偶然正确，中间定位或逻辑不可靠仍会产生训练信号；反之，模型也不能只学会框选区域而忽略最终问答任务。<br>
**原文位置**：第3.2节，公式(6)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：阶段I最小化$\mathcal{L}^{(S1)}=\sum_{t=1}^{T}\mathcal{L}_V(V_t,V_t^*)$，用于预先获得推理语义与视觉区域之间的对应能力；随后阶段II最小化联合目标$\mathcal{L}^{(S2)}$，把逐步推理、动态定位和最终答案统一到同一优化过程中。权重$\lambda_R$、$\lambda_V$和$\lambda_A$用于平衡三类监督，但所给章节未报告具体取值，也未明确给出$\mathcal{L}_R$、$\mathcal{L}_V$和$\mathcal{L}_A$各自采用的具体损失实现，因此不能据此假定其为交叉熵、边界框回归或掩码损失。

从优化作用看，阶段I降低了阶段II直接联合学习的难度，阶段II则防止模型把定位当成孤立任务：$V_t$必须能支撑$R_t$并经$I_t$影响后续步骤，最终还要服务于$A$。论文同时声称框架可兼容监督微调、强化学习及二者组合，但当前节选的核心流程和公式对应两阶段监督训练，未提供强化学习奖励函数或优化细节。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 动态视觉定位与反馈**

第$t$步定位$V_t$与推理$R_t$同步产生，并通过映射$V_t\rightarrow I_t$成为下一步的额外视觉条件；因此视觉注意可随推理进度动态迁移。框架支持applied、boxed和cropped三种定位呈现方式，并区分显式与隐式视觉定位设置。

> 直观理解：固定观察整张图容易把相近的柱、点或图例混淆；动态反馈使模型每完成一个逻辑步骤就重新确定当前证据。视觉定位在这里是连接图像和推理的中间指导，而非最终任务本身。

**2. 两阶段视觉推理训练**

阶段I只重点学习$R_t$到$V_t$的跨模态对应，阶段II在此基础上联合生成$R_t$与$V_t$并预测$A$。这种顺序把较容易检查的空间对齐能力作为前置技能，再优化完整的交错视觉推理。

> 直观理解：若一开始同时要求模型看准、想清楚并答正确，错误来源很难分离。先训练“看哪里”，再训练“如何利用看到的证据继续解题”，可降低联合任务的学习难度。

**3. 双维度课程与CCQA**

课程同时提高视觉维度和逻辑维度的难度：视觉上从低层图表组件走向复杂图表结构，逻辑上以嵌套函数的最大层数定义推理深度$D$；$D$不同于生成步骤数$T$，因为多个步骤可能处于同一逻辑层级。CCQA包含bar、histogram、scatter、line、heatmap、pie和radar七类图表，并以模板生成逐步定位监督。

> 直观理解：$T$表示模型写了多少步，$D$表示问题本身最深需要套几层操作；写得更细不一定让题目更难。区分二者可以避免把冗长答案误认为高复杂度推理。

**训练与推理**

训练时，首先按课程顺序向模型提供CCQA样本。阶段I在图像$I$、问题$Q$、当前推理$R_t$和历史配对条件下预测$V_t$，利用$V_t^*$监督每一步定位；阶段II加载或建立在该定位能力之上，从前序推理及视觉状态生成当前$(R_t,V_t)$，将$V_t$处理成$I_t$并交错反馈，最后生成$A$，再联合反向传播推理、定位和答案损失。课程从基础单操作和低层视觉组件逐渐扩展到更深的嵌套逻辑及更复杂图表，目的是让模型依次掌握可复用的视觉—逻辑技能。

推理时，输入仅需图表$I$和问题$Q$；模型从第一个步骤开始自行产生$R_t$与$V_t$，按选定的applied、boxed或cropped策略构造$I_t$，再以原图、问题、文本历史和演化后的视觉状态生成下一步，直至形成$T$步链并输出$A$。因此不需要测试时提供人工视觉标注或真实推理链；但节选未说明停止条件、答案格式约束，以及显式定位结果在部署时是否必须对用户可见。

**复现信息**

公平理解该方法所需的已知信息是：CCQA覆盖七种图表类型和30个领域类别，每种图表类型仅使用30张独特基础图，并通过模板从同一图像派生大量查询—推理—定位—答案实例；这一设计意在促使模型学习可迁移的操作，而不是记忆大量图像外观。视觉监督同时提供区域$V_t^*$和二值掩码$M_t^*$，模型规模与骨干可变化，表中实例包括InternVL3及Qwen2.5-VL，视觉反馈可选applied、boxed或cropped。

所给章节未明确报告图像分辨率、优化器、学习率、批大小、训练轮数、课程阶段采样比例、三项损失权重、定位输出编码方式、三种视觉变换的精确算法以及阶段间参数冻结策略。这些信息会影响严格复现；在没有附录相应内容时，不应从常规做法推断。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- CCQA：作者构造的三级课程数据集，被划分为互不重叠的训练集和测试集；三个测试集分别对应逐级增加的任务难度。它既用于微调CURV，也用于检验模型在课程内难度、复杂图表和多步视觉落地推理上的表现。节选未提供各划分的样本规模。
- 图表理解基准组：包括ChartQA、ChartQA-Pro、CharXiv的reasoning子集和ChartMuseum的visual子集。它们不承担CURV训练，而用于检验模型能否将CCQA上学习到的视觉落地推理迁移到真实或既有图表问答分布。
- 域外多模态基准组：MathVista与MMMU-Pro，覆盖跨学科的多模态推理。它们用于判断收益是否超出图表问答本身，而不是仅由对CCQA任务格式或图表模板的适配造成。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**推理质量：$acc@mic$与$acc@mac$**

$acc@mic$综合ROUGE-L、BLEU、METEOR、BERTScore和余弦相似度，从词面重合、语义相似性等角度比较生成推理与参考推理；$acc@mac$由GPT-4.1-mini依据三项标准对整体推理质量评分。前者偏细粒度文本匹配，后者偏整体连贯性与质量判断。 （越高越好，因为更高值表示生成的推理链与参考过程更一致，或被裁判模型判定为质量更高；但它们并不直接保证推理所引用的视觉证据正确。）

</div>
<div class="metric-item" markdown="1">

**视觉落地：CIOU与GIOU**

两者比较模型关注区域与目标视觉区域的空间重合。GIOU是广义交并比；CIOU按累计交集与累计并集评估多步或多个区域的总体定位质量，用来检查推理是否真正连接到图表中的相关证据。 （越高越好，因为更高的区域重合度意味着模型更准确地定位了支撑当前推理步骤的图表元素。）

</div>
<div class="metric-item" markdown="1">

**答案准确率：$acc@MLLM$与$acc@range$**

$acc@MLLM$使用GPT-4.1-mini对每个答案作True-or-False的pass@1判断；$acc@range$通过规则解析与评分，包含严格的$acc@0.0$以及逐步放宽的$acc@0.05$、$acc@0.1$和$acc@0.2$。规则指标用于降低单一MLLM裁判可能引入的偏差，并区分精确答案与容许一定数值误差的答案。 （越高越好，因为更高值表示更多测试样本的最终答案被判定正确；阈值越宽松通常越容易通过，因此不同阈值的数值不能直接视为同等严格的准确率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### CCQA三级课程测试集：CURV微调模型与基础MLLM、GPT模型比较

<div class="result-value" markdown="1">

作者报告，CURV在六项指标上均持续优于基线：单阶段训练的最大绝对增益为14.85个百分点，两阶段训练的最大绝对增益为20.92个百分点。最佳模型CURV@Applied（Qwen2.5-VL-7B）相对其基础模型最高提升15.65个百分点，相对GPT模型最高提升12.22个百分点。

</div>

这说明课程式视觉落地训练不仅改善最终答案，也能在作者采用的推理和定位指标上获得一致收益；两阶段训练的最大增益高于单阶段训练，支持逐步课程训练的有效性。不过“最高提升”是跨指标或设置选出的最大值，不能理解为每个难度级别、每个模型和每项指标都提升同样幅度；同时，节选未展示表2的完整逐项数值。

<div class="result-source" markdown="1">

来源：§5.3，Performance on CCQA；表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Compared with the baselines (Tab. 2), our finetuned models achieve consistently higher accuracy across all six metrics, with absolute gains of up to 14.85% and 20.92% for single-stage and two-stage training, respectively. The highest performance is achieved by CURV@Applied (Qwen2.5-VL-7B), with up to 15.65% higher than its base model. Compared with GPT models, it achieves up to 12.22% higher accuracy, demonstrating the effectiveness of CURV in enhancing MLLMs’ visual reasoning abilities.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 外部图表基准：ChartQA、ChartQA-Pro、CharXiv与ChartMuseum

<div class="result-value" markdown="1">

作者报告CURV在四个图表基准上的提升均至少为1.20个百分点。表3中，同规模模型经CURV训练后通常更强，例如Qwen2.5-VL-3B在ChartQA上由62.32提升至72.36，在CharXiv上由19.50提升至31.80；InternVL3-8B在ChartMuseum上由24.42提升至26.23。

</div>

这些结果表明，在CCQA上训练得到的能力可以迁移到多个外部图表数据集，而不是只在合成课程测试集上有效。不同模型规模和基准上的增益并不均匀，因此更稳妥的结论是“普遍正迁移”，而不是CURV对所有真实图表任务都有同等幅度的提升；实验也未排除CCQA与外部基准在图表类型或问答模式上的潜在相似性。

<div class="result-source" markdown="1">

来源：§5.3，Performance on Chart Benchmarks；表3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Results in Tab. 3 highlight the strong generalizability of CURV, with improvements≥↑1.20% across four chart benchmarks.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 域外多模态推理：MathVista与MMMU-Pro

<div class="result-value" markdown="1">

作者报告CURV在域外多模态推理上的准确率最高提升10.20个百分点。表3显示，InternVL3-8B在MathVista上由68.80提升至75.37、在MMMU-Pro上由26.99提升至30.81；Qwen2.5-VL-7B则分别由64.60提升至72.41和由28.21提升至32.08。

</div>

在不属于标准图表问答的MathVista和MMMU-Pro上仍有增益，支持CURV可能强化了较通用的视觉证据定位与推理协同能力。但这里只覆盖两个域外基准，而且没有与针对这些基准专门训练的方法进行充分因果控制，因此不能据此断言CURV已经获得普适的多模态推理能力。

<div class="result-source" markdown="1">

来源：§5.3，Generalizability to Out-of-Domain Multimodal Reasoning；表3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The advantage of CURV remains consistent in out-of-domain multimodal reasoning across diverse multimodal reasoning categories (§5.2), attaining up to↑10.20% accuracy improvements (Tab. 3).

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

- 未经CURV微调的Qwen2.5-VL，包括3B和7B版本；与对应CURV模型直接比较，可以控制基础架构与参数规模，从而衡量训练框架带来的增益。
- 未经CURV微调的InternVL3，包括1B、2B和8B版本；它用于检验CURV是否能跨模型家族和规模生效，而不只适用于Qwen2.5-VL。
- 闭源MLLM GPT-4o与GPT-4.1-mini；它们代表较强的通用多模态系统，用于判断经CURV微调的开源模型是否具有竞争力。GPT-4.1-mini还被用作宏观推理质量和答案正确性的裁判，因此相关结果可能受到裁判模型偏差影响。
- 其他开源MLLM，包括Llama-3.2-Vision、Gemma-3以及不同规模的Qwen2.5-VL和InternVL3；这些横向比较用于定位CURV相对于常用开源视觉语言模型的整体水平。

**实验想回答的问题**

- CURV的课程式显式视觉落地训练，能否在未见过的CCQA测试集上同时改善推理文本、视觉区域定位和最终答案，并优于基础模型、闭源模型及普通训练方式？
- 在主要使用单图表课程数据训练后，CURV获得的能力能否迁移到复杂多图表、真实图表问答基准以及域外多模态推理任务；这些收益是否确实来自显式视觉落地和由基础到复杂的课程安排？

**实验实现**

作者以Qwen2.5-VL 3B、7B和InternVL3 1B、2B、8B为基础模型，通过CURV进行微调；比较结果同时覆盖单阶段与两阶段训练，其中表3将两阶段方案标记为“Stage I + II”。CCQA训练集与测试集不重叠，所有微调模型均在训练时未见的测试集上评估。答案采用pass@1，并同时报告MLLM裁判和规则裁判；推理与视觉落地则使用互补指标。节选将具体超参数、训练资源和实现细节指向附录§G.1，但未给出学习率、批量大小、训练轮数或随机种子，因此无法仅据本节完整复现实验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 显式视觉落地与隐式视觉落地对比 | 显式视觉落地推理相对隐式方案持续更优，作者报告最高或汇总提升为8.78个百分点。 | 该对比隔离了“是否把视觉区域作为推理过程中的明确中间桥梁”这一设计。结果支持在每一步显式指出相关区域，比只让模型在内部隐式学习视觉—推理联系更有效。它说明显式监督形式重要，但不能单独证明提升全部来自更忠实的证据使用，因为两种训练表示也可能具有不同的学习难度。 | §5.4，Benefits of Explicit over Implicit Visual Grounded Reasoning；图7<br><span class="experiment-evidence">Comparing CURV with explicit and implicit visual grounded reasoning (§G.5), Fig. 7 demonstrates that explicit visual grounded reasoning consistently outperforms its implicit counterpart (↑ 8.78%).</span> |
| 课程等级组合：仅基础等级、基础加中级以及完整课程的比较 | 所有课程等级设置都改善总体准确率，但等级1与2联合训练在不同测试难度上产生最一致且显著的收益；相较之下，依赖等级3训练的效果较差。 | 该消融检验复杂样本是否可以替代基础课程。结果表明，模型需要先学习单操作和中等组合推理，才能形成可迁移到不同难度的视觉推理能力；直接依赖最复杂任务并非最佳策略。节选没有提供图9的逐项数值，因此只能确认趋势，不能量化各课程组合之间的差距或判断统计显著性。 | §5.4，Foundational Learning Drives More Balanced Gains；图9<br><span class="experiment-evidence">While all curriculum levels improve overall accuracy, training on levels 1+2 yields the most consistent and substantial gains across different levels (Fig. 9). In contrast, relying solely on level 3 is less effective, highlighting the significance of foundational learning in establishing adaptive and generalizable visual reasoning capabilities to support more robust chart understanding across varying difficulty levels (§G.8).</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过课程学习和动态视觉 grounding 训练多模态模型执行多步图表推理。; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`a7f327f1af1fc40eb38b0c80dd0da3f81216028a87762f3e4065c009037df6b3`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
