---
title: "[论文解读] Chain of Spatial Thoughts: Modality-Agnostic Spatial Grounding for Vision Language Models"
description: "[arXiv 2608.10278][VLM Reasoning] 本文提出 Space Tokens，将场景级三维几何与物体级空间属性蒸馏为视觉语言模型可直接处理的连续潜在词元，使模型无需新增推理模块或修改架构，即可在思维链中利用显式空间知识。"
arxiv_id: "2608.10278"
announcement_date: "2026-08-12"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-12T03:04:37.789617+00:00"
source_sha256: "7c84a8f51cb41e23b0c5c3a8f8dc7c12d694698ec9e7f2bcaa413a40e5d1c002"
tags:
  - "VLM Reasoning"
  - "多模态 VLM"
  - "LLM Reasoning"
  - "视觉语言模型"
  - "空间智能"
  - "空间归因"
  - "连续潜在令牌"
  - "三维几何蒸馏"
  - "物体中心表示"
  - "思维链"
  - "具身智能"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.10278</p>

# Chain of Spatial Thoughts: Modality-Agnostic Spatial Grounding for Vision Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-12</span>
<span><strong>作者</strong> Hunter Schofield, Mohammed Elmahgiubi, Mohammad Mahdavian, Richard Shi, Jinjun Shan, Amir Rasouli, Dongfeng Bai</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> York University；Huawei Technologies Canada；University of Toronto</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.10278v1) · [PDF 下载](https://arxiv.org/pdf/2608.10278v1) · **关键词** 视觉语言模型, 空间智能, 空间归因, 连续潜在令牌, 三维几何蒸馏, 物体中心表示, 思维链, 具身智能<br>


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

本文提出 Space Tokens，将场景级三维几何与物体级空间属性蒸馏为视觉语言模型可直接处理的连续潜在词元，使模型无需新增推理模块或修改架构，即可在思维链中利用显式空间知识。

**不用术语来说**：视觉语言模型虽然能识别图像内容并回答问题，但对物体有多大、位于哪里、朝向何方以及场景如何在三维空间中组织，仍可能理解不足。现有改进办法往往需要扩大模型和空间数据规模，或在推理时额外运行三维重建等专用模块，因而训练或部署成本较高。本文关注的问题是：能否在训练阶段把这些空间知识压缩进模型内部，让原模型在回答空间问题时直接调用，而不再依赖外接几何系统。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出模型无关的 Space Tokens 框架，通过统一的连续词元接口，把场景级三维几何和物体级位置、朝向、尺寸等属性纳入视觉语言模型的自回归思维链，同时不要求推理阶段增加模块或修改原有架构。
- 使潜在空间表示能够被显式解码回可解释的三维模态，从而可以检查词元是否确实编码了有意义的几何信息，而不只依据最终问答准确率间接推断模型具备空间理解。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于视觉语言模型（VLM）的空间智能研究。VLM联合处理图像或视频与自然语言，但完成机器人操作、具身导航和自动驾驶等任务，还需要理解场景的三维几何结构，例如物体的位置、朝向、尺寸、相互关系以及房间尺度。现有能力主要来自两条路线：一是扩大模型、通用数据或空间监督数据的规模；二是在VLM之外接入三维重建编码器、几何连接器或关系推理模块。前者训练成本高，后者通常增加推理计算并削弱模型移植性。本文基于潜在令牌知识集成范式，研究能否把场景级三维几何与物体级空间属性压缩为VLM可直接处理的连续令牌，使几何信息进入自回归思维链，同时避免推理阶段继续运行额外的空间模型。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉语言模型（VLM）**

能够联合编码视觉输入与自然语言，并以文本形式回答问题或执行推理的多模态模型。本文关注的不是普通物体识别，而是VLM能否从图像或视频中推断三维布局和空间关系。

</div>
<div class="concept-item" markdown="1">

**连续潜在令牌**

由连续数值向量构成、可插入模型令牌序列的内部表示，不必对应可读文字。它可将外部几何模型提供的知识蒸馏进VLM，使模型在生成推理过程时直接使用这些表示。

</div>
<div class="concept-item" markdown="1">

**空间归纳偏置**

通过专用结构或表示，预先赋予模型处理三维位置、尺度、朝向或几何关系的倾向。专门的三维编码器能够提供这种偏置，但若推理时必须保留该模块，就会增加成本并限制对不同VLM架构的适配。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是包含空间信息的图像或视频，以及要求判断场景几何、物体属性或空间关系的自然语言问题；基础系统是能够进行自回归文本推理的既有VLM。训练阶段可利用外部三维重建模型产生场景级几何监督，也可利用三维边界框中的物体位置、朝向和尺寸等属性，将这些信息蒸馏为连续的Space Tokens。推理阶段的目标是不再调用额外三维编码器或修改基础架构，而由VLM在原生思维链中生成并使用这些令牌，最终输出空间问题的文本答案；令牌还应能够被显式解码回三维模态，以检验其是否确实携带可解释的几何信息。该设置假定训练数据能够提供或构造相应空间监督，但原文所给章节未明确限定输入视角数量、令牌维度及具体监督格式。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x_v$**

视觉输入，例如图像或视频；该符号是为清晰描述任务而作的概念性记号，原文节选未给出正式符号。

</div>
<div class="notation-item" markdown="1">

**$q$**

关于场景几何或空间关系的自然语言问题；原文节选未给出正式符号。

</div>
<div class="notation-item" markdown="1">

**$z_s$**

由场景级三维几何或物体级空间属性蒸馏得到的连续空间令牌表示；原文节选未给出正式符号。

</div>
<div class="notation-item" markdown="1">

**$y$**

VLM经过自回归空间推理后生成的文本答案；原文节选未给出正式符号。

</div>

</div>

**直接相关的工作**

- **Chain-of-Visual-Thought（Qin et al., 2025）**: 该工作以连续视觉令牌把视觉表示纳入VLM的思维过程，是本文采用“潜在令牌知识集成”路线的直接先例；本文将其关注点从一般视觉感知与二维推理扩展到显式三维几何和物体级空间属性。
- **VLM-3R（Fan et al., 2026）**: 该工作代表利用三维重建增强VLM空间推理的专门空间方法。本文同样借助三维重建知识，但试图在训练时将其蒸馏进VLM内部，使推理阶段无需保留额外的大型几何模块。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

机器人操作、具身导航、自动驾驶和人机交互不仅要求系统认出物体，还要求其理解物体之间的三维布局、尺度、方向及交互关系。空间判断一旦不可靠，模型便难以支持依赖连续几何推理的真实决策；原文特别指出，当前视觉语言模型在路线规划和物体出现顺序等长程任务上仍落后于人类。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基础模型与空间监督扩展**：通过增加模型参数、扩大互联网规模的多模态训练数据，或使用更大规模的空间专项监督数据，使空间能力随模型容量和训练覆盖面的增长而增强；SenseNova-SI 被原文列为依靠大规模空间监督的代表。
- **专用空间架构与潜在词元知识整合**：专用空间架构接入三维重建编码器、几何感知连接器、物体中心表示或场景关系推理模块，为模型提供明确的空间归纳偏置；另一条较轻量的路线则把外部知识蒸馏为连续潜在词元，在保留主体架构的情况下让视觉语言模型在生成过程中使用这些内部表示。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 扩展模型容量或空间监督规模需要更大的模型和大量专项训练数据，因而提高训练与数据成本，却仍不能保证模型获得可检查的显式三维表示。
- 专用几何方法通常在推理时保留额外空间模块，增加计算成本并降低跨模型迁移与部署的便利性；已有潜在词元方法虽可避开这一问题，但主要编码视觉或语义知识，对显式三维几何和物体中心空间属性探索不足。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未充分证明：场景级三维结构与物体级位置、朝向和尺寸能否被统一压缩为视觉语言模型原生可消费、同时又可解码验证的连续词元，并在不保留教师几何模型或其他附加推理组件的条件下改善空间推理。

</div>
<div markdown="1"><span>核心问题</span>

能否仅通过轻量训练，把外部三维重建模型和三维包围盒所包含的空间知识内化到现有视觉语言模型中，使这些知识成为其原生思维链的一部分，同时维持底层模型的推理效率、架构完整性与可移植性？

</div>
<div markdown="1"><span>作者直觉</span>

连续潜在词元可以看作模型内部的“空间草稿”：训练时由强大的外部几何表示提供指导，将复杂的三维场景或物体属性压缩到少量连续向量中；推理时，语言模型像读取普通上下文一样读取这些向量，因此无需再次运行昂贵的几何教师模型。若这些向量还能被解码回三维结构，就可以直接检查这份“草稿”是否保留了真实空间信息，并为将来接入其他模态提供统一接口。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Space Tokens 的核心目标是在不改变视觉语言模型（VLM）自回归架构、且不增加推理期外部空间编码器的前提下，把显式几何知识写入一组保留词表位置。给定图像或视频帧集合 $\mathcal{I}=\{I_1,\ldots,I_n\}$ 与提示 $\mathcal{P}$，模型仍按普通文本生成方式输出序列 $\mathcal{Y}$；当输出到专用空间 token 时，方法不依赖其离散编号表达空间含义，而是提取这些位置的末层隐藏状态，并将其训练为两类连续表示：描述整段场景几何的 3D 重建 token，以及描述对象中心、尺寸和朝向的 3D 包围盒 token。前者通过对齐 VGGT-Omega 的场景特征，并重建相机、深度图和点图来学习；后者通过固定槽位的集合回归来学习。两类信息分别覆盖全局场景结构和对象级空间属性。

训练分为表示学习、空间推理监督微调和强化学习细化三个阶段。第一阶段把空间 token 人工插入思维链式答案，只用几何对齐与重建损失建立隐藏状态和空间结构之间的对应关系；第二阶段冻结空间投影层，以教师强制和下一 token 预测训练模型在推理文本中生成并利用这些表示，同时保留空间损失作为正则化；第三阶段使用组相对策略优化（GRPO），依据答案奖励继续改善空间推理。训练结束后，模型可像生成普通词一样自行生成空间 token，并直接利用其隐藏状态继续作答，不需要在推理时运行 VGGT-Omega、输入 2D 框或安装额外空间模块。直观地说，该方法先为模型词表中的若干“空白词”赋予可验证的几何含义，再教模型在解题草稿中主动调用这些几何记忆。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 空间监督构造与 token 注入

从词表中保留专用位置作为 3D 重建 token 和 3D 包围盒 token，并把它们人工嵌入思维链式训练答案；模型生成这些位置后，提取对应的末层隐藏状态 $h_{3D}$ 或包围盒隐藏表示。2D 框特征仅在训练中提供对象定位引导，不属于推理输入。

<div class="method-step__io" markdown="1">

**输入**：视频或多图像输入 $\mathcal{I}$、问题提示 $\mathcal{P}$、VGGT-Omega 提供的场景级教师表示与重建目标，以及对象的 2D/3D 包围盒标注。<br>
**输出**：带有专用空间位置的训练序列，以及可接受几何监督的连续隐藏状态。

</div>

**直观理解**：这一步相当于先在模型的语言中预留几个“几何词”，并明确它们应该谈论整间房间还是某个物体。词本身只是占位符，真正承载空间信息的是该位置产生的连续向量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段一：连续空间表示学习

将 3D token 隐藏状态投影为 $\hat z$，用余弦距离对齐教师潜在空间，并通过轻量解码器重建相机、深度和点图；包围盒分支融合专用 token、视觉骨干特征和归一化 2D 框特征，随后进行匈牙利匹配和 12 维框回归。本阶段只反向传播空间对齐与重建损失，使投影和相关表示先学会几何含义，避免与答案生成目标竞争。

<div class="method-step__io" markdown="1">

**输入**：空间 token 的隐藏状态、VGGT-Omega 聚合特征 $z$、教师相机参数与深度图、由深度反投影得到的点图，以及对象级 3D 包围盒标注。<br>
**输出**：编码全局 3D 场景和对象级 3D 属性的连续空间 token，以及可将其解码为显式几何结果的投影层。

</div>

**直观理解**：教师模型和几何标注在这一阶段充当“空间课本”：一个 token 若确实理解场景，就应既接近教师的内部表示，也能还原相机、深度或物体框。这样避免 token 只记住一个与几何无关、却偶然有助于答题的捷径。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段二：空间 token 推理监督微调

冻结从 VLM 隐藏状态映射到空间特征空间的投影层，在教师强制下以交叉熵执行标准下一 token 预测，使模型学会生成空间 token、在后续推理中引用它们并输出答案；同时继续施加空间对齐损失作为正则项。方法只让模型基于选出的部分输入帧进行显式推理，原文称这比对全部帧推理更有效。

<div class="method-step__io" markdown="1">

**输入**：第一阶段学得的空间表示、保留空间 token 的思维链式目标序列，以及相应问题的正确答案。<br>
**输出**：既保持空间表示含义、又能在自回归推理链中使用这些表示的监督微调模型。

</div>

**直观理解**：第一阶段解决“几何词表示什么”，第二阶段解决“什么时候说这些词，以及说完后怎样据此回答”。冻结投影层类似于固定已经学好的词义，防止答题训练把它们重新改造成没有明确几何含义的暗号。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段三：GRPO 空间推理细化

以阶段二模型作为参考策略，对同一输入生成一组候选答案，按组内标准化奖励计算优势，并用裁剪概率比的策略目标更新模型；KL 散度项限制新策略偏离参考模型。奖励设计面向空间问答，具体组成位于原文附录，所给节选未展开。

<div class="method-step__io" markdown="1">

**输入**：阶段二模型、图像集合与提示对 $(\mathcal{I},\mathcal{P})$、每个输入采样得到的 $G$ 条输出序列及其奖励。<br>
**输出**：经过奖励信号细化、能够更稳定地利用空间 token 完成空间推理的最终策略。

</div>

**直观理解**：监督微调只模仿给定解题过程，强化学习则让同一道题的多种回答相互比较，增加高奖励推理路径的概率。裁剪和 KL 约束相当于限制每次调整幅度，避免模型为了追逐奖励而破坏第二阶段已经形成的语言与空间能力。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 3D 重建 token 联合目标

$$
\mathcal{L}_{3D}=\lambda_{sim}\mathcal{L}_{sim}+\lambda_{cam}\mathcal{L}_{cam}+\lambda_{dpt}\mathcal{L}_{dpt}+\lambda_{pt}\mathcal{L}_{pt}
$$

**符号说明**

- $\mathcal{L}_{3D}$：场景级 3D 表示 token 的总训练损失。
- $\mathcal{L}_{sim}$：预测表示与 VGGT-Omega 聚合特征之间的余弦距离，其中预测表示由 $\hat z=\operatorname{proj}(h_{3D})$ 得到。
- $\mathcal{L}_{cam}$：预测相机姿态编码与教师相机估计之间的 $\ell_1$ 重建损失。
- $\mathcal{L}_{dpt}$：深度图的数值回归与梯度一致性损失，并使用偶然不确定性图进行加权。
- $\mathcal{L}_{pt}$：相机坐标系三维点图的数值回归与梯度一致性损失。
- $\lambda_{sim},\lambda_{cam},\lambda_{dpt},\lambda_{pt}$：平衡潜在特征对齐、相机、深度和点图监督贡献的非负权重；具体取值在原文附录。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标同时约束“内部表示像教师”和“外部几何能被还原”。若只使用 $\mathcal{L}_{sim}$，token 可能仅复制教师特征而缺少直接可验证性；加入相机、深度和点图任务后，同一表示必须支持多个互补的 3D 预测，因此更有可能保留完整场景结构。<br>
**原文位置**：Methodology → Continuous Spatial Tokens → 3D Representation Tokens，式 (3)

</div>

</div>

<div class="equation-block" markdown="1">

#### GRPO 空间推理细化目标

$$
\mathcal{J}(\theta)=\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|\mathcal{Y}_i|}\sum_{t=1}^{|\mathcal{Y}_i|}\left\{\min\left[\operatorname{clip}\left(r_{i,t}\hat A_{i,t},1-\epsilon,1+\epsilon\right),r_{i,t}\hat A_{i,t}\right]-\beta\mathbb{D}_{KL}\left[M_\theta\|M_{\mathrm{ref}}\right]\right\},\quad r_{i,t}=\frac{M_\theta(y_{i,t}\mid y_{i,<t})}{M_{\theta_{\mathrm{old}}}(y_{i,t}\mid y_{i,<t})},\quad \hat A_{i,t}=\frac{R_{i,t}-\bar R_t}{\sigma_R}
$$

**符号说明**

- $\mathcal{J}(\theta)$：用于更新当前模型参数 $\theta$ 的 GRPO 优化目标。
- $G$：对同一图像集合与提示采样的候选输出序列数量。
- $\mathcal{Y}_i$：组内第 $i$ 条输出序列，$|\mathcal{Y}_i|$ 为其 token 数。
- $r_{i,t}$：当前策略与采样时旧策略在第 $i$ 条序列第 $t$ 个 token 上的条件概率比。
- $\hat A_{i,t}$：由奖励 $R_{i,t}$、组均值 $\bar R_t$ 和奖励标准差 $\sigma_R$ 得到的组内标准化优势。
- $\epsilon$：概率比裁剪范围的超参数，用于限制单次策略更新幅度。
- $\mathbb{D}_{KL}[M_\theta\|M_{\mathrm{ref}}]$：当前模型相对阶段二参考模型 $M_{\mathrm{ref}}$ 的 Kullback-Leibler 散度。
- $\beta$：KL 偏离惩罚的权重。
- $M_{\theta_{\mathrm{old}}}$：生成本轮候选序列时使用的旧策略模型。

<div class="equation-explanation" markdown="1">

**直观理解**：优势为正的回答会被提高概率，优势为负的回答会被抑制；组内标准化使更新依据同题候选之间的相对质量，而不依赖一个单独训练的价值模型。裁剪项防止新旧策略概率比变化过大，KL 项则把最终模型约束在阶段二模型附近，从而在优化空间任务奖励时尽量保留原有生成能力。<br>
**原文位置**：Methodology → Three-Stage Pipeline，式 (5)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：三个阶段采用职责分离的优化方式。阶段一仅优化空间表示：场景级分支最小化 $\mathcal{L}_{3D}$，其中潜在特征对齐、相机、深度和点图损失共同约束 3D token；对象级分支最小化 $\mathcal{L}_{\mathrm{3D\text{-}BB}}=\lambda_{\mathrm{obj}}\mathcal{L}_{\mathrm{obj}}+\lambda_{\mathrm{bg}}\mathcal{L}_{\mathrm{bg}}$，分别训练匹配对象和空槽位。作者明确说明本阶段只反向传播这些重建或对齐损失，目的是先建立 VLM 隐状态到空间潜变量的稳定映射，避免几何目标立即与下游答案生成竞争。

阶段二固定上述空间投影层，并在教师强制下加入标准交叉熵下一 token 预测目标，使模型同时学习空间 token 的生成位置、使用方式和最终答案；空间对齐损失仍作为正则项参与训练，以抑制表示漂移。阶段三改用 GRPO 目标 $\mathcal{J}(\theta)$，根据组内相对奖励优化完整输出序列，并通过概率比裁剪与相对阶段二参考模型的 KL 惩罚控制更新。因节选未给出各项损失权重和奖励函数明细，不能据此复现其具体数值配置；这些信息由作者指向附录。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 词表保留式连续空间 token 接口**

方法在既有词表中保留一组 token，不增加新的推理架构；这些 token 与普通词一样由 $M_\theta$ 自回归生成，但其语义由生成位置的末层隐藏状态而非离散 token ID 承载。该统一接口允许不同空间模态嵌入同一推理序列，且理论上可继续扩展到其他可监督模态。

> 直观理解：普通 token 的编号通常直接对应某个词，而这里的编号主要用来标记“接下来这个隐藏向量应装载哪类空间知识”。因此模型仍可沿用原来的生成机制，却能在文本推理链中传递比离散文字更精细的连续几何信息。

**2. 场景级 3D 表示蒸馏与可解码监督**

投影器把 3D token 隐藏状态 $h_{3D}$ 映射到 VGGT-Omega 的潜在空间，余弦损失约束预测特征 $\hat z$ 与教师聚合特征 $z$ 的方向一致；相机 $\hat{\mathbf g}_i$、深度 $\hat D_i$ 和点图 $\hat P_i$ 的重建损失进一步要求潜变量保留显式几何。深度监督同时包含数值回归和梯度一致性，并由预测的不确定性图 $c_i^D$ 加权；点图由预测深度结合相机内参反投影到相机坐标系后监督。

> 直观理解：仅模仿教师的内部向量可能学到不可解释的相似性，因此作者又要求同一向量能够还原具体的相机和三维结构。特征对齐负责传递教师的高层空间知识，重建任务则用可观察结果检查这些知识是否真的包含几何。

**3. 对象级 3D 包围盒集合回归**

包围盒解码器融合专用框 token、VLM 视觉骨干特征和训练期归一化 2D 框特征，并输出固定数量的预测槽位；每个对象框是 12 维向量，包含相机坐标系中心、三维尺寸和 6D 旋转表示。预测框与真值框采用基于 $\ell_1$ 代价的匈牙利算法进行一一匹配，匹配槽位使用参数为 $\beta=0.1$ 的 Smooth $\ell_1$ 损失，未匹配槽位回归到零背景目标。

> 直观理解：全局场景表示擅长描述房间整体，却未必精确区分每个物体的位置和朝向；对象框 token 补充了这一级信息。固定槽位允许对象数量变化，匈牙利匹配则先找出预测与真值之间最合理的一一对应，避免要求第一个槽位永远对应某一种物体。

**训练与推理**

训练时，模型接收多帧视觉输入、问题以及包含专用 token 的思维链式目标。阶段一利用 VGGT-Omega 教师特征、相机与稠密几何目标训练场景 token，并利用 2D 定位提示和 3D 框标注训练对象 token；阶段二保留同样的 token 格式，冻结空间投影器后进行 SFT，并让模型基于选出的部分帧显式推理；阶段三从当前旧策略为每个输入采样 $G$ 个候选，通过空间任务奖励执行 GRPO。LoRA 用于参数高效微调；进入 GRPO 前，前两阶段的 LoRA 适配器被合并到模型，再初始化一个配置相同的新适配器。

推理时只需最终 VLM、输入帧和自然语言问题。模型按照原有自回归过程生成空间 token 及后续文本，几何信息存在这些位置的连续隐藏状态中，因此 VGGT-Omega、训练期 2D 框和额外空间编码器均不再需要；这也是“无架构修改”和“无额外推理模块”的具体含义。若研究者需要解释或验证 token，可调用训练所得轻量投影、交叉注意力和 MLP 解码器生成场景重建或对象框，但论文明确把这种解码视为可选验证途径，而非回答问题的必要计算。

**复现信息**

模型以 Qwen3-VL-8B 和 SenseNova-SI-1.3 为基础，使用秩为 $16$、缩放因子为 $32$ 的 LoRA；SFT 与 GRPO 的学习率分别为 $5\times10^{-5}$ 和 $1\times10^{-6}$，并采用余弦学习率调度。阶段一和阶段二在 VICA-322K 上共同微调 $1$ 个 epoch，阶段三另使用 $8{,}000$ 个样本；该数据集包含多环境、多对象的教学视频序列，可同时支持场景级几何和对象级关系学习。每段视频均匀采样 $32$ 帧并缩放至 $448\times448$，而显式推理使用其中选出的 $6$ 帧；具体选择策略、损失权重、解码器结构和奖励设计在原文附录，当前节选不足以进一步确定。

公平解释该方法时需要区分训练期和推理期成本：VGGT-Omega 教师、显式重建目标、2D 框定位特征、匈牙利匹配及几何解码器都用于学习或检查表示，但正常推理不要求运行这些组件。另一方面，“没有额外推理模块”不等于完全没有训练增量，方法仍需三阶段微调、教师生成的几何监督和专用投影或解码结构；其计算优势主要发生在部署阶段。原文还指出对少于 $6$ 帧的输入会重复可用帧以维持预期结构，这意味着推理格式依赖训练时的固定帧组织，跨数据集比较时应考虑这种预处理差异。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- VSI-Bench完整划分：用于评估视觉语言模型的空间理解能力。原文给出的子任务包括物体计数、绝对距离、物体大小、房间大小、相对距离、相对方向、路线规划和接近顺序，并分别汇总数值题、多项选择题及总体平均成绩；数据规模与样本构成在所给章节中未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**VSI-Bench Avg.**

汇总多个空间理解子任务的总体平均成绩，用来衡量模型的综合空间推理能力；所给章节未明确说明各子任务的加权方式。 （越高越好，因为更高分表示模型在VSI-Bench涵盖的多类空间问题上总体回答更准确。）

</div>
<div class="metric-item" markdown="1">

**Numerical Questions**

汇总需要输出数值的空间问题表现，相关子任务包括物体计数、绝对距离、物体大小和房间大小，可检验模型估计数量、尺度及距离的能力。 （越高越好，因为更高分代表数值型空间判断更准确。）

</div>
<div class="metric-item" markdown="1">

**Multiple-Choice Questions**

汇总多项选择空间问题表现，相关子任务包括相对距离、相对方向、路线规划和接近顺序，用来评估关系判断与空间决策能力。 （越高越好，因为更高分代表模型选择正确空间关系或行动答案的比例更高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3-VL-8B加入Space Tokens，在VSI-Bench上与其原始模型比较

<div class="result-value" markdown="1">

作者报告VSI-Bench成绩提高4.3%，说明连续空间标记在较大视觉语言模型上带来了可测的总体增益。

</div>

这一结果支持Space Tokens能够补充模型原有视觉表示，而不只是适配SenseNova体系。由于所给材料没有表1的原始分数、方差或显著性检验，该增益不能单独证明所有子任务都改善，也不能排除训练数据或训练流程差异的影响。

<div class="result-source" markdown="1">

来源：摘要；实验节表1被提及，但所给节选未提供对应数据行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Experiments on VSI-Bench improve Qwen3-VL-8B by 4.3% and SenseNova-SI-1.3 by 1.3%, while achieving state-of-the-art performance on object size (79.2%) and room size estimation (75.7%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### SenseNova-SI-1.3加入Space Tokens，在VSI-Bench上与其原始模型比较

<div class="result-value" markdown="1">

作者报告VSI-Bench成绩提高1.3%，表明Space Tokens的收益并非只出现在Qwen3-VL-8B上。

</div>

跨两个基础模型均有提升，为架构无关性的主张提供了初步经验支持。不过1.3%的改进幅度较小，而节选未报告多次运行波动、统计显著性及完整对照条件，因此尚不能判断该提升在不同随机种子或训练配置下是否稳定。

<div class="result-source" markdown="1">

来源：摘要；实验节表1被提及，但所给节选未提供对应数据行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Experiments on VSI-Bench improve Qwen3-VL-8B by 4.3% and SenseNova-SI-1.3 by 1.3%, while achieving state-of-the-art performance on object size (79.2%) and room size estimation (75.7%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Space Tokens在VSI-Bench几何尺度估计子任务上的结果

<div class="result-value" markdown="1">

作者报告物体大小成绩为79.2%，房间大小估计成绩为75.7%，并称两项均达到当时最先进水平。

</div>

这两项任务直接依赖尺度和三维几何线索，因此结果与方法将场景级三维几何及物体中心空间属性压缩为空间标记的设计目标一致。该结果表明模型尤其可能受益于显式几何表示，但不能证明其所有空间推理能力都来自这些标记，也不能在缺少完整表1时核验领先幅度及比较模型是否使用同等额外信息。

<div class="result-source" markdown="1">

来源：摘要；实验节表1被提及，但所给节选未提供对应数据行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Experiments on VSI-Bench improve Qwen3-VL-8B by 4.3% and SenseNova-SI-1.3 by 1.3%, while achieving state-of-the-art performance on object size (79.2%) and room size estimation (75.7%).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验节选缺少表1的完整数据行、VSI-Bench规模、基础模型原始分数、训练与评测重复次数以及统计显著性，因此摘要中的4.3%、1.3%和最先进结论仍需对照原表核验，无法从当前材料判断提升的方差与公平比较条件。
- 注意力屏蔽实验因技术限制改用eager attention，而主模型使用Flash Attention 2训练。作者认为该变化同时影响屏蔽组和未屏蔽组，不改变组间结论，但绝对分数已发生系统性变化；此外，屏蔽可能同时改变注意力分配和生成动态，因而只能支持空间表示对预测具有因果贡献，不能精确量化其中每类几何信息的独立贡献。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Qwen3-VL-8B：作为较大规模预训练视觉语言模型，比较加入Space Tokens前后的VSI-Bench表现，用于检验该方法能否在已有强模型上提供额外空间能力。
- SenseNova-SI-1.3：作为另一种视觉语言模型及Space Tokens的主要承载模型，用于检验方法是否具有跨模型适用性；其Stage 3版本还用于标记替换和注意力屏蔽实验。
- CoVT：原文将其作为单图学习标记方法的代表，用于说明Token Replacement Test在固定标记语义的单图场景中为何较容易解释；所给章节未提供其VSI-Bench对比成绩。
- Mull-Tokens：作为多帧视觉输入方法，用于支持作者对Token Replacement Test局限性的判断，即多图模型即使使用潜在标记，也可能对初始标记嵌入扰动不敏感。

**实验想回答的问题**

- 在统一的VSI-Bench评测上，将连续空间标记（Space Tokens）引入视觉语言模型后，是否能稳定提升整体空间推理能力，并在物体大小、房间大小等依赖三维几何信息的任务上取得更强结果？
- 模型生成答案时是否真正使用了空间标记所承载的潜在表示，而不是仅依赖原始视觉信息、提示模板或空间标记的初始输入嵌入？

**实验实现**

主实验在VSI-Bench完整划分上比较不同模型类型及Space Tokens变体，但所给实验节选未包含表1的具体数据行、样本规模、提示方式和重复运行设置。补充实验使用SenseNova-SI-1.3 Stage 3：Token Replacement Test分别将空间标记的输入嵌入替换为零向量、随机向量或从潜在表示同分布采样的随机向量；因该测试只干预初始嵌入，作者进一步构造因果注意力掩码，在答案生成期间禁止模型关注空间标记，同时保持其他计算不变。注意力屏蔽实验使用eager attention，因为Flash Attention 2不支持任意注意力掩码；作者说明eager attention会使绝对表现略降，但屏蔽组与未屏蔽组采用相同设置，因此组间差异仍可用于判断空间标记的因果作用。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Token Replacement Test：将空间标记输入嵌入分别替换为零向量、普通随机向量和同分布随机向量 | 三种扰动下VSI-Bench平均分分别为68.82、68.55和68.69，差异很小。 | 该实验只隔离空间标记的初始输入嵌入是否重要。结果不能推出空间潜在表示未被使用，因为在多图输入中，同一个标记类型会跨图像复用，具体图像身份由提示中的位置信息指定。作者据此认为，Token Replacement Test主要测量模型对初始嵌入扰动的敏感性，并不足以探测后续形成的图像相关潜在表示。 | 表S4，Token replacement test results on VSI-Bench<br><span class="experiment-evidence">zero \| 68.82; random \| 68.55; random (same dist.) \| 68.69</span> |
| Token Attention Masking：生成答案时禁止模型关注空间标记，并与同一eager-attention设置下的未屏蔽模型比较 | 屏蔽后总体平均分从63.4降至55.3，下降8.1分；数值题从72.3降至60.4，多项选择题从55.8降至46.3；其中物体大小从79.0降至63.7，下降15.3分。 | 这一干预直接切断答案生成对空间潜在表示的访问，因此比替换初始嵌入更接近因果检验。显著下降说明模型预测确实使用了这些表示，物体大小的最大降幅也与空间标记编码几何尺度的设计相符。不过相对方向由30.9升至32.0，说明空间标记并非对每个子任务都同等有益，且单次屏蔽实验仍不能完全排除注意力分布变化带来的间接影响。 | 表S5及第C.2节 Token Attention Masking<br><span class="experiment-evidence">No masking \| 63.4 \| 72.3 \| 55.8 \| 79.0 \| 63.2 \| 62.0 \| 71.9 \| 30.9 \| 72.2; Spatial token masking \| 55.3 \| 60.4 \| 46.3 \| 63.7 \| 58.2 \| 50.8 \| 60.1 \| 32.0 \| 70.6</span> |

**定性案例**

- 原文用提示片段“Because the 3D feature of image 5 is <|3d_pad|> × 8”解释多图绑定机制：固定输入嵌入只声明后续标记属于三维空间类型，而“image 5”等模板位置文字负责把八个空间标记绑定到第5张图像。该例不是定性预测案例，但直接说明了为何初始嵌入替换几乎无效，而屏蔽最终潜在表示会明显损害推理。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Adds explicit continuous spatial representations to VLM chain-of-thought processing to improve geometric and spatial reasoning.; rule check: matched taxonomy keywords; top rule score=10.0
- 全文指纹：`7c84a8f51cb41e23b0c5c3a8f8dc7c12d694698ec9e7f2bcaa413a40e5d1c002`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
