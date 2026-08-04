---
title: "[论文解读] CoT-Edit: Let CoT Guide Instruction Video Editing"
description: "[arXiv 2608.01113][视频生成] 本文针对复杂场景中纯文本视频编辑难以准确定位目标、遵守运动轨迹和满足物理约束的问题，提出“规划—引导—编辑”框架，先把语言意图转化为时序边界框与增强指令，再据此生成掩码并驱动扩散编辑器完成编辑。"
arxiv_id: "2608.01113"
announcement_date: "2026-08-04"
primary_category: "video_generation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:05:12.496225+00:00"
source_sha256: "d09ee7181f315e9b5234025f919c39b21cad9bc10f5597d1cbbbac9ae8c6fc15"
tags:
  - "视频生成"
  - "VLM Reasoning"
  - "LLM 其他"
  - "LLM Reasoning"
  - "指令驱动的视频编辑"
  - "思维链"
  - "多模态大语言模型"
  - "空间定位"
  - "边界框条件掩码"
  - "扩散模型"
  - "时空一致性"
  - "物理合理性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">视频生成 · arXiv 2608.01113</p>

# CoT-Edit: Let CoT Guide Instruction Video Editing

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Sen Liang, Fengbin Guan, Youliang Zhang, Xin Li, Zhibo Chen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> University of Science and Technology of China；Zhongguancun Academy；Tsinghua University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01113v1) · [PDF 下载](https://arxiv.org/pdf/2608.01113v1) · **关键词** 指令驱动的视频编辑, 思维链, 多模态大语言模型, 空间定位, 边界框条件掩码, 扩散模型, 时空一致性, 物理合理性<br>
**代码**: [https://github.com/flying-sky999/CoT-Edit](https://github.com/flying-sky999/CoT-Edit)

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

本文针对复杂场景中纯文本视频编辑难以准确定位目标、遵守运动轨迹和满足物理约束的问题，提出“规划—引导—编辑”框架，先把语言意图转化为时序边界框与增强指令，再据此生成掩码并驱动扩散编辑器完成编辑。

**不用术语来说**：用户用自然语言修改视频时，指令通常只说明“要改什么”，却未精确说明每一帧应在“哪里改、改多大、如何移动”。例如，画面中有多只相似的狗时，“把黄色的狗变成橙色的猫”可能改错对象；要求新增不明飞行物并沿椭圆轨迹飞行时，模型也可能生成位置、大小或运动方式不合理的结果。因此，系统需要先理解目标身份及其跨帧位置和物理关系，再执行像素级修改。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出结构化的“规划—引导—编辑”范式：在生成视频之前，先由带思维链推理的多模态大语言模型分析视频关键帧和指令，输出目标的时序边界框及包含属性、交互倾向和场景约束的增强指令，从而将高层语义意图显式映射到具体时空位置。
- 设计边界框条件掩码分支，将规划器给出的粗粒度空间先验细化为时空一致的局部掩码，再由扩散编辑器联合利用掩码、增强指令和视频特征完成编辑；作者主张这种模块化设计能够改善定位、物理合理性与时间一致性，并降低对大规模对齐标注数据的依赖。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究自然语言指令驱动的视频编辑：用户提供原始视频和诸如“把黄色的狗变成橙色的猫”或“在天空中加入沿椭圆轨迹飞行的 UFO”之类的指令，模型据此生成完成修改的视频。该任务不仅要求理解指令中的编辑对象与动作，还要在连续帧中定位正确目标，并保持目标外观、运动轨迹、尺度、接触关系和前后帧一致性。现有纯文本方法通常让同一个生成模型隐式完成语义理解、空间定位和像素修改；在多目标、相似物体密集或动态交互场景中，文本本身难以精确表达“改哪一个”“放在哪里”和“如何运动”，因此容易出现目标选错、定位漂移、物理关系不合理及时间闪烁。本文所处的技术路线以扩散模型作为视频生成与编辑基础，同时引入多模态大语言模型进行视频—文本联合推理，并以边界框和掩码提供显式空间条件，从而把高层语言意图逐步落实到具体时空区域。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**指令驱动的视频编辑**

模型以原始视频和自然语言编辑指令为输入，在尽量保留无关内容的同时生成满足指令的新视频。与普通文本生成视频不同，它必须继承输入视频的主体、背景和运动，并只对指定内容实施修改。

</div>
<div class="concept-item" markdown="1">

**多模态大语言模型与思维链推理**

多模态大语言模型能够联合理解视频画面和文本；思维链推理是把一次隐式判断拆成目标识别、动作理解、空间定位和物理可行性分析等连续步骤。本文用这种规划过程先确定编辑意图及关键帧位置，再把结果交给后续生成模块。

</div>
<div class="concept-item" markdown="1">

**扩散式视频编辑与空间条件**

扩散模型通过逐步去除噪声来生成或修改视频，而边界框、掩码等空间条件用于明确规定应编辑的区域。边界框给出目标的大致位置与尺度，掩码进一步标出像素级区域，可降低模型仅凭文本在整幅画面中搜索目标的难度。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是一段包含多个连续帧的原始视频和一条自然语言编辑指令，输出是执行该指令后的完整视频。编辑类型包括修改已有对象以及添加新对象：前者需要在多个相似实体中选中正确目标，并跨帧持续跟踪该目标；后者还需要推断新对象合理的位置、尺度、运动轨迹及其与场景中其他物体的接触或遮挡关系。问题设定默认用户只提供视频与文本，不提供人工边界框或掩码，因此系统必须自行把语义意图转换为时序空间约束。本文进一步将这一过程分解为规划、引导和编辑：规划器依据视频关键帧与指令产生属性更完整的指令以及一系列关键帧边界框，引导分支据此预测时空一致的局部掩码，扩散编辑器最后融合文本、原视频特征和掩码生成编辑结果。该设定的核心评价要求不是仅让输出在语义上“看起来相关”，而是同时满足目标选择准确、空间位置匹配、物理行为合理和跨帧时间一致。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **InstructX**: 同属自然语言指令驱动的视频编辑方法，并利用多模态大模型增强语义泛化；但原文指出其空间约束主要依赖隐式注意力。CoT-Edit则先显式推理出时序边界框和增强指令，再通过掩码把空间约束传递给编辑器，重点弥补模糊指令下的目标定位问题。
- **Lucy-1.1**: 该端到端模型验证了直接接收视频与指令进行编辑的可行性，但原文称其在小目标或含糊指令下空间定位不足。CoT-Edit把目标解析与空间定位从最终扩散编辑中部分解耦，以规划器和边界框条件掩码分支提供更明确的编辑位置。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

指令式视频编辑希望让非专业用户通过自然语言直接修改动态内容，但复杂真实视频往往包含多个共存对象、密集分布的相似实例以及持续变化的交互关系。编辑系统不仅要理解指令，还必须跨帧识别正确目标、确定修改区域，并保持对象的尺度、接触关系和运动轨迹合理；其中任何一步出错，都会导致目标选错、编辑区域漂移、未编辑区域受损或前后帧不连贯。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **纯文本条件的视频编辑**：将原始自然语言指令直接作为主要控制信号输入视频生成或扩散编辑模型，由同一模型隐式完成语义理解、目标定位和像素生成。该路线接口简单，但空间位置和物理约束没有被显式表达，编辑器必须从含糊语言中同时推断“改什么”和“在哪里改”。
- **文本生成掩码后进行局部编辑**：先依据原始指令预测需要修改的掩码，再用掩码约束编辑区域，使全局语义检索转化为局部修改。掩码能提供比文本更直接的空间控制，但如果其生成过程仍只依赖原始指令，文本中的歧义和空间不确定性会继续传递到掩码。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 纯文本方法把跨帧理解、实例区分、空间定位和内容生成集中交给编辑模型；在多个相似对象或复杂运动条件下，容易出现定位漂移、编辑错误和时间不稳定。扩大模型或数据规模并未消除缺少显式空间锚点与物理约束这一根本问题。
- 仅从文本预测掩码无法可靠消解目标歧义；对于新增对象，原视频中还不存在可分割目标，因此文本掩码缺乏可执行的位置、尺度、接触关系和运动逻辑先验，可能造成新增内容悬空、大小失真或轨迹不符合指令。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种可执行的语义—空间接口：它既要保留自然语言表达复杂编辑意图的能力，又要在真正生成像素之前，将该意图转换为跨帧一致的目标位置、范围和物理关系；同时，这一接口还应能处理原视频中不存在目标的对象新增任务，并避免依赖大量视频—指令—空间标注。

</div>
<div markdown="1"><span>核心问题</span>

能否让多模态规划器先对视频与指令进行结构化、物理感知的逐步推理，生成时序边界框和增强语义指令，再把这些先验细化为掩码并交给扩散编辑器，从而比直接使用文本更准确地控制目标身份、空间位置、运动行为和跨帧一致性？

</div>
<div markdown="1"><span>作者直觉</span>

该切入点的直觉是把一个负担过重的生成任务拆成三个更明确的步骤：规划器先决定对象及其每个关键时刻的大致位置，掩码分支再把边界框细化为实际需要修改的像素区域，编辑器最后只需在受约束区域内渲染目标内容。边界框相当于先在视频中标出“施工范围”，增强指令补充对象应具备的属性和行为；两者共同减少编辑器自行猜测目标、位置与运动规律的空间。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CoT-Edit采用“规划—引导—编辑”（Plan–Guide–Edit）流水线，把原本需要扩散模型同时解决的语义理解、空间定位和内容生成拆成三个相互协作的问题。输入是原始视频$S$与用户编辑指令；Planner先基于按时间排序的关键帧进行显式思维链推理，将模糊指令转化为关键帧对齐的归一化框序列$B=\{b_t\}_{t=1}^{T}$和结构化增强指令$EI$；Guide以框为硬位置约束、以视频特征和$EI$为软语义约束，预测逐帧二值掩码$\{M_t\}$；Editor再将掩码、增强指令、原视频潜变量以及多模态模型特征融合进Wan2.2 5B扩散骨干，生成编辑内容，最后仅在掩码区域内合成结果并保留区域外的原视频。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 多模态语义—空间规划

Planner解析编辑类型与目标对象，跨帧区分相机运动和物体运动、识别并跟踪相关实例，再推断位移、尺度、可见性、接触、遮挡和重力等约束，并通过自检形成时间一致的规划。对于需要空间定位的任务，它输出每个关键帧上的归一化框$[t,x_1,y_1,x_2,y_2]$；对于风格化等非空间任务，输出空框序列。

<div class="method-step__io" markdown="1">

**输入**：按时间排序的关键帧$\{I_t\}_{t=1}^{T}$和用户编辑指令。<br>
**输出**：关键帧对齐的框序列$B=\{b_t\}_{t=1}^{T}$，以及包含目标属性、相对位置、交互、运动和镜头一致性提示的增强指令$EI$。

</div>

**直观理解**：这一阶段相当于先让系统写出可执行的剪辑计划：不仅说明“改什么”，还明确“每一时刻在哪里改、应满足哪些常识”。框负责给出可检查的位置锚点，增强指令负责补充框无法表达的语义与物理关系。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 框约束的时空掩码生成

Guide在与Editor相同的分层架构中进行跨时间、跨相邻尺度的自注意力，并通过交叉注意力融合全局视频上下文、$EI$和$B$；它把框作为硬约束，将全局目标检索转化为框内形状细化。Guide与Editor在多层双向交换特征：Editor的高层语义反向修正掩码特征，而掩码特征持续调制Editor。

<div class="method-step__io" markdown="1">

**输入**：框序列$B$、增强指令$EI$、原视频特征，以及Editor各层反馈的特征$Q_l^E$。<br>
**输出**：逐帧、时间有序且可直接监督的二值掩码$\{M_t\}$，以及供Editor使用的中间掩码特征$C_l^M$。

</div>

**直观理解**：框只圈出大致区域，掩码还要找出真正需要修改的像素，例如细长边缘、接触面或被部分遮挡的区域。让编辑分支把自己对任务的理解反馈给掩码分支，可减少仅凭局部外观造成的漏选和边界不稳。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 多条件扩散编辑与掩码合成

3D VAE先把$S$编码为$y_0$，模型将$y_{\text{noise}}$与$y_0$沿通道拼接后送入扩散骨干；Editor通过文本交叉注意力接收$EI$，并将投影后的$V$在$C_l^M$调制下注入各编辑块。扩散生成结束后，系统采用掩码引导合成，只在掩码内部应用编辑内容，掩码外沿用原视频。

<div class="method-step__io" markdown="1">

**输入**：原视频$S$的潜变量$y_0$、加噪潜变量$y_{\text{noise}}$、掩码$\{M_t\}$及其多层特征$C_l^M$、增强指令$EI$和Qwen-VL末层视觉—语言特征$V$。<br>
**输出**：空间位置与指令对齐、非编辑区域得到保留且跨帧连续的编辑视频。

</div>

**直观理解**：扩散模型负责真正“画出”修改后的画面，但绘制范围由掩码限定，内容含义由增强指令和多模态特征限定。最后的局部合成类似只在选区内落笔，从而减少背景或相似物体被意外改动。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### Guide与Editor的多层双向特征耦合

$$
\begin{aligned} C_l^M &\leftarrow C_l^M + \operatorname{Reverse\_Connector}(Q_l^E),\\ Q_l^E &\leftarrow Q_l^E + \operatorname{Mask\_Connector}(C_l^M). \end{aligned}
$$

**符号说明**

- $C_l^M$：Guide在第$l$层的时空掩码特征。
- $Q_l^E$：Editor在第$l$层的编辑特征。
- $l$：Guide和Editor交互所在的网络层索引。
- $\operatorname{Reverse\_Connector}(\cdot)$：将Editor高层语义映射到Guide特征空间的反向连接器。
- $\operatorname{Mask\_Connector}(\cdot)$：将Guide掩码特征投影为Editor特征加性调制的连接器。

<div class="equation-explanation" markdown="1">

**直观理解**：第一行让编辑分支依据自己对目标语义、遮挡和外观的理解反向纠正掩码；第二行又把更新后的空间信息送回编辑分支。两种连接可在多层重复，使边界级空间控制和高层语义生成不是彼此隔离的单向过程。<br>
**原文位置**：第3.2节，公式(2)和公式(3)

</div>

</div>

<div class="equation-block" markdown="1">

#### 掩码调制的MLLM特征注入

$$
Q_l^E \leftarrow Q_l^E + \operatorname{QVLcrossattn}\!\left(\operatorname{MLP}(V), C_l^M\right)
$$

**符号说明**

- $Q_l^E$：Editor第$l$层的特征；等式右侧为更新前特征，左侧为融合后的特征。
- $V$：Qwen-VL末层输出的视觉—语言token特征。
- $\operatorname{MLP}(\cdot)$：把Qwen-VL特征通道从3584维投影到Wan2.2 5B所用3072维的多层感知机。
- $C_l^M$：Guide在第$l$层产生的掩码特征，用于调制语义信息的空间作用范围。
- $\operatorname{QVLcrossattn}(\cdot,\cdot)$：Editor面向投影后Qwen-VL token的专用交叉注意力，并受掩码特征调制。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把多模态模型整理出的语义和世界知识加到Editor当前特征上，同时用掩码特征约束其空间作用。直观上，它让模型既理解“应该生成什么以及应符合何种关系”，又尽量只在应编辑的位置使用这些信息。<br>
**原文位置**：第3.3节，公式(4)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文摘要仅说明模型“先模块化训练，再联合训练”，第3节还指出逐帧显式掩码可被直接监督，并可参与联合优化以稳定骨干网络学习；但所给章节没有给出扩散去噪损失、掩码监督损失、联合目标的数学形式、各损失权重或Planner的具体训练目标。因此只能确认优化涉及可监督掩码学习以及Guide—Editor联合训练，不能据此补写未报告的目标函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. CoT增强的MLLM Planner**

Planner以多模态大语言模型为基础，将推理组织为任务解析与跨帧感知、物理与时间一致性建模、空间和语义指导生成三个相连阶段。其结构化输出将刚性的框序列$B$与较灵活的增强指令$EI$分离：前者规定位置，后者编码属性、关系、运动及场景约束。

> 直观理解：普通文本指令可能只说“在杯子旁加一个苹果”，却不说明是哪只杯子、苹果应放在哪一侧或如何接触桌面。Planner先结合视频逐帧消除这些歧义，使后续模型不必一边猜位置一边生成内容。

**2. 带双向连接器的Guide**

Guide共享Editor的分层结构，以时空自注意力维持跨帧和跨尺度连续性，并以交叉注意力联合使用全局视频特征、$EI$和$B$。Reverse-Connector把Editor特征$Q_l^E$映射回掩码特征$C_l^M$以修正薄结构和重遮挡区域，Mask-Connector则把$C_l^M$投影为对$Q_l^E$的多层加性调制；逐帧解码头最终输出与输入帧同空间分辨率的掩码。

> 直观理解：Guide不是一次性画完选区后退出，而是与Editor反复交换信息。掩码告诉Editor应修改哪里，Editor对物体和指令的高层理解又帮助Guide补回难辨认的边界，两者共同降低定位误差。

**3. 多条件扩散Editor**

Editor以Wan2.2 5B为扩散骨干，将原视频潜变量与加噪潜变量联合输入，并通过交叉注意力接收$EI$。Qwen-VL末层特征$V$保留前1024个token，再由MLP从3584维映射到Wan2.2 5B使用的3072维，并在掩码特征$C_l^M$调制下通过专用Qwen-VL交叉注意力注入各编辑块。

> 直观理解：原视频潜变量提供需要保留的画面基础，文本条件说明要生成什么，多模态特征补充Planner已经整理出的视觉和常识信息，掩码则约束这些信息主要作用于正确位置。多条件联合的目的，是同时控制内容、位置和未编辑区域的稳定性。

**训练与推理**

训练阶段先分别建立各模块能力：Planner学习或适配从关键帧与指令到$B$和$EI$的结构化规划，Guide利用可直接监督的$\{M_t\}$学习框内形状细化，Editor基于Wan2.2 5B学习条件扩散编辑；随后联合优化Guide与Editor，使Reverse-Connector和Mask-Connector的双向、多层交互能够共同调整掩码与生成特征。原文没有明确交代Planner是否参与最终端到端联合训练，也没有在所给章节中报告训练数据构造、优化器、学习率、扩散时间步采样或损失配比。

推理阶段，系统从视频中取得时间有序关键帧，与用户指令一起交给Planner；Planner输出$B$与$EI$，Guide据此生成完整视频上的时空掩码，并在生成过程中接收Editor反馈；Editor将$y_{\text{noise}}$、$y_0$、$EI$、$V$和$C_l^M$融合到扩散去噪过程中，得到编辑内容；最后按$\{M_t\}$逐帧合成，使掩码内采用编辑结果、掩码外保留原视频。非空间任务由Planner输出空框序列，但原文未进一步说明此时Guide及合成步骤的具体旁路规则。

**复现信息**

Guide和Editor均以Wan2.2 5B为基础，并共享同类分层架构。原视频$S$通过3D VAE编码为低维潜变量$y_0$，扩散时产生加噪潜变量$y_{\text{noise}}$，二者沿通道维拼接；为接收该联合输入，tokenizer $T$的输入通道扩展到32而输出维度保持不变，作者称此举可避免破坏原Wan2.2 5B分布。Qwen-VL条件仅使用末层特征$V$的前1024个token，并以MLP完成3584维到3072维的通道对齐。除此之外，所给方法章节没有明确报告关键帧数量$T$、帧分辨率、采样步数、框插值方式、阈值、连接器具体层结构或掩码监督标签的生成方法；这些信息仍需结合论文其余章节或公开代码核查。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 模块化训练阶段的 Mask 分支数据：ADE20K、PhraseCut、YouTube-VOS 和 OVIS 的混合数据。前两者提供图像级分割监督，后两者提供视频对象分割监督，用于学习由目标描述和框条件生成时空一致掩码。原文未明确报告各数据集的采样比例、样本数量或具体划分。
- Editor 分支训练数据：AnyEdit、UltraEdit、SEED-Data-Edit、EditWorld、Señorita-2M、Ditto，以及作者自建的指令式视频编辑数据。它们共同覆盖图像编辑、视频编辑和指令驱动编辑，用于训练扩散编辑器理解编辑要求并生成结果；原文未明确报告混合比例和各数据源的实际使用规模。
- 联合训练与评测数据：第二阶段使用约 10 万组带精确掩码标注的内部高质量视频编辑前后对进行联合训练；评测则从 Koala-36M 随机抽取 100 个视频，并人工配置对象添加、删除、属性修改、风格化及抛物线运动等指令。内部训练集与 Koala-36M 评测样本并非同一角色，前者检验联合优化，后者用于统一比较各编辑方法。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**FVD**

Fréchet Video Distance，用生成视频与参考视频在视频特征分布上的距离衡量整体视频真实性和分布接近程度。它关注统计层面的视觉质量，但不能单独判断某次编辑是否准确遵循了指令。 （越低越好，因为更小的特征分布距离通常表示生成视频更接近真实视频分布。）

</div>
<div class="metric-item" markdown="1">

**VBench 视觉质量指标组（BC、TC、MS、AES）**

BC 以 CLIP 特征的跨帧相似性评估全局背景保持；TC 比较相邻帧及首帧之间的 CLIP-B 相似性以衡量时间连贯；MS 借助视频插帧模型的运动先验判断运动是否连续自然；AES 使用 LAION 美学预测器评价逐帧美学质量。四项指标分别覆盖背景、时间、运动和外观，不能互相替代。 （均为越高越好，分别意味着背景更稳定、跨帧内容更连贯、运动更平滑以及画面美学评分更高。）

</div>
<div class="metric-item" markdown="1">

**指令与编辑质量指标组（CLIPScore 与 Gemini 评分）**

CLIPScore 使用 CLIP-B 衡量文本指令与生成视频的语义对齐；Gemini 从物理合理性、空间关系、指令遵循和整体编辑质量四方面评分。前者是自动特征相似度，后者是模型裁判评价，因此二者都可能受到预训练模型偏差影响。 （均为越高越好，因为更高分表示文本与视频更匹配，或模型裁判认为编辑在相应维度表现更好。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Koala-36M 的 100 个视频上，与六种开源指令式视频编辑基线比较整体视觉质量。

<div class="result-value" markdown="1">

CoT-Edit 的 FVD 为 1015.67，是表中最低值；BC、MS 和 AES 分别为 0.974、1.18 和 0.62，均为表中最高值。不过 TC 为 0.945，低于 Lucy-1.1 的 0.961、InsV2V 的 0.958 和 InsViE 的 0.957，因此“所有视觉维度全面领先”并不成立。

</div>

作者结果表明，该方法生成的视频在总体分布质量、背景保持、运动平滑和逐帧美学上具有优势，这与掩码定位和扩散编辑器的设计目标一致。需要注意，FVD 基于仅 100 个评测视频时可能对样本组成敏感，而 TC 未领先说明更准确的空间或物理编辑不必然带来最强的跨帧特征相似性。

<div class="result-source" markdown="1">

来源：Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Ours 0.974 0.445 1015.67 0.945 1.18 0.62 0.741 0.841 0.629 0.648

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 使用 CLIPScore 和 Gemini 裁判评估文本对齐、物理合理性、空间关系、指令遵循及整体编辑质量。

<div class="result-value" markdown="1">

CoT-Edit 的 CLIPScore 为 0.445；Gemini 给出的物理合理性、空间关系、指令遵循和整体编辑质量分数分别为 0.741、0.841、0.629 和 0.648，五项均为表中最高值。相较各项最强基线，其空间关系从 Lucy-1.1 的 0.769 提升到 0.841，物理合理性从 OmniVideo 的 0.590 提升到 0.741。

</div>

这些结果支持作者关于 CoT 规划和框到掩码引导有助于理解“改什么、在哪里改、应如何运动”的主张，尤其是空间关系和物理合理性的提升较明显。但四个编辑质量维度由 Gemini 评分，并非人工标注的客观真值；结果证明的是在当前模型裁判协议下更受认可，不能直接等同于真实用户偏好或严格物理正确性。

<div class="result-source" markdown="1">

来源：Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Ours 0.974 0.445 1015.67 0.945 1.18 0.62 0.741 0.841 0.629 0.648

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 在包含多个相似对象、非编辑区域保持和复杂多任务指令的案例中进行定性比较。

<div class="result-value" markdown="1">

作者报告 CoT-Edit 能在多个相似对象中准确定位指令指定目标，较好保持无需编辑的区域，并处理复杂指令和多任务编辑；图 4 还用于展示遵循抛物线运动或匀速直线运动等显式物理规律的编辑。

</div>

这类案例直接检查自动指标不容易覆盖的局部目标歧义和接触、轨迹等空间约束，因而能补充表 1。它仍属于作者选择的可视化样例，原文节选没有给出失败案例、完整样本覆盖率或盲评统计，不能据此判断所有复杂场景都能稳定成功。

<div class="result-source" markdown="1">

来源：Section 4.2, Figure 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

CoT-Edit demonstrates: (1) precise localization and editing of the target object specified in the instruction among multiple similar objects; (2) strong preservation of non-edited regions consistent with the original video; (3) robust understanding of complex editing instructions and high-quality multi-task editing.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评测规模只有随机抽取的 100 个 Koala-36M 视频，且原文节选未报告任务类别占比、随机种子、置信区间或显著性检验。因而表中优势可能受样本构成影响，尤其不能仅凭较小分差断言稳定领先。
- 物理合理性、空间关系、指令遵循和整体编辑质量均依赖 Gemini 裁判；用户研究的具体参与人数、盲评流程、统计结果仅称见补充材料，当前节选没有提供。模型裁判偏差、内部 100k 数据不可复现，以及缺少详细人工评测协议，共同限制了结论的独立验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- InsV2V：开源指令式视频编辑方法，作为该任务中直接依据文本修改视频的代表性基线，用于检验 CoT-Edit 的定位、保持和指令遵循是否优于常规方案。
- StableV2V：强调视频到视频生成稳定性的开源方法，是比较背景保持、跨帧一致性和整体视觉质量的有意义基线。
- OmniVideo：同样将 MLLM 与扩散模型结合，因此是判断提升是否仅来自“MLLM 加扩散模型”这一组合、还是来自 CoT 规划与显式空间引导的关键对照。
- Lucy-1.1：纯扩散式端到端视频编辑方法，并在表中取得较强的空间关系分数和时间一致性，用于比较显式规划框架与强端到端编辑器之间的差异。

**实验想回答的问题**

- 与现有指令式视频编辑方法相比，CoT-Edit 能否同时提升编辑后视频的视觉质量、文本指令遵循能力，以及对空间关系和物理规律的处理能力？
- 性能提升分别来自哪些设计：多模态大语言模型（MLLM）的指令增强、Mask 分支提供的空间定位信号，以及 Mask-Connector 和 Reverse-Connector 建立的双向分支交互？

**实验实现**

训练采用两阶段策略：第一阶段分别训练 Editor 与 Mask（Guide）分支，共 20k 步；第二阶段在约 10 万组内部视频编辑对上联合训练两个分支，共 10k 步。两个阶段的批量大小均为 64，训练分辨率为 $720\times1280$，Reverse-Connector 与 Mask-Connector 采用零初始化。评测从 Koala-36M 随机抽取 100 个视频，为每个视频配置多类编辑指令，并以相同指标比较 CoT-Edit 和开源基线。该协议覆盖多种任务类型，但原文节选未交代随机种子、每类指令数量、参考视频构造方式、Gemini 提示词与重复评分次数。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 固定为单独的 Editor 分支，比较不使用 MLLM 与注入 Qwen3-VL 特征。 | 加入 MLLM 后，PR 从 0.501 提升至 0.674，IF 从 0.575 提升至 0.598，OEQ 从 0.598 提升至 0.631；SR 仅从 0.754 增至 0.758。该变化表明 MLLM 的主要作用更接近指令语义增强和物理意图理解，而非单独解决精确空间定位。 | 该对照隔离了 Qwen3-VL 特征的作用，因为两行都没有加入 Mask 分支。较大的 PR 增益支持“更丰富的指令理解有助于物理合理性”，而 SR 增益很小则说明仅增强文本或视频语义不足以替代显式区域引导。原文未报告误差条或显著性检验。 | Table 2<br><span class="experiment-evidence">E w/o MLLM 0.501 0.754 0.575 0.598
E w/ MLLM 0.674 0.758 0.598 0.631</span> |
| 在 Editor、MLLM、Mask 分支和 Mask-Connector 均存在时，进一步加入 Reverse-Connector。 | 加入 Reverse-Connector 后，PR、SR、IF 和 OEQ 分别从 0.643、0.807、0.586、0.638 提升到 0.681、0.815、0.609、0.647，四项均改善；其中 IF 增加 0.023，PR 增加 0.038。 | 这个对照检验双向分支交互是否优于仅由 Mask-Connector 提供的单向空间引导。结果支持反向连接能让语义编辑信息与掩码定位进一步协调，但它没有把“新增连接参数带来的容量增长”与“信息流方向本身的价值”完全分离。 | Table 2<br><span class="experiment-evidence">E + M w/ Mc 0.643 0.807 0.586 0.638
E + M w/ Mc & Rc 0.681 0.815 0.609 0.647</span> |

**定性案例**

- 图 5 的乒乓球案例比较 Qwen3-VL-32B 和 Gemini 2.5 Pro 在有无 CoT 时的输出。作者称无 CoT 时乒乓球未呈现物理合理运动；加入 CoT 后，两种模型都生成了先沿抛物线运动、撞击球桌、再向上反弹的轨迹。该案例说明结构化中间推理可能帮助模型把高层指令转化为具体轨迹与碰撞顺序，但单个成功案例不能量化 CoT 在不同物体、碰撞条件或长视频中的平均收益。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The method centrally combines diffusion-based instruction video editing with structured multimodal reasoning that plans spatially grounded edit operations.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`d09ee7181f315e9b5234025f919c39b21cad9bc10f5597d1cbbbac9ae8c6fc15`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
